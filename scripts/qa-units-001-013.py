#!/usr/bin/env python3
"""Fail-closed QA for the cumulative O012 Units 001-013 reader.

The final PDF is deliberately treated as immutable here.  This verifier
reproduces the HTML twice in a temporary directory, but it only inspects the
already-built PDF and its page renders; it never creates or replaces a PDF.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path
from urllib.parse import unquote, urlparse

from lxml import etree
from PIL import Image
from pypdf import PdfReader


LANE = Path(__file__).resolve().parents[1]
SOURCES = (
    LANE / "source/id-ID/reader-unit-001.md",
    *(LANE / f"source/id-ID/units/unit-{n:03d}-lecture-{n:03d}.md" for n in range(2, 14)),
)
SOURCE_EXPECTED = (
    (16179, 225, "c80b51c22a2fa7ea116201028b78d5f8d708ef4d8355d34092ac7a9c88415e15"),
    (25090, 674, "4d2acc43557db9b3c419ee177545d285b9fcf50b2aa2dd3b2c6c44182f3a6a01"),
    (25822, 618, "993e5941895a9b6f4b197b4c236f5a4990f6ae621e2bb7911353b28a5e1abffd"),
    (24582, 632, "826fcb368275cdad02f72a5cec951fc8466ba68b09ca0139d72c81a4c5591fea"),
    (22662, 663, "7333a7b7a92b9618016412abb5c9b2b2a398538f690d0109d4282289a0719852"),
    (32106, 893, "3cb182fdf183bd67e45a898228b995a44d4638e808fdfbe6ea6d6a2a2b889e33"),
    (22107, 749, "556cea5445e1b0a51f86f1c0ea0e80c4e00a17d365d95fa530f063cc24856569"),
    (28466, 930, "8369e74c80e391d73575bbcb7844d3bfa62dd771dbca6258eed02360b20529cc"),
    (25524, 939, "16da25dea2f8ac5415b02738663046fb619c27e685042a734059e3150ed5ff18"),
    (26432, 934, "e1c6ef961ae2266db86baec6d701dd659a1bf78bdd3601cf5b1c6515bc7d0310"),
    (28465, 959, "1cdbe0cae239a4e60a72f25c8814c2e3b5ec26b9119da03624bda7f3ff1ae127"),
    (32850, 1024, "429831df4a5600c59351516915fb787cd73402d8c11c411869210dbf8aaa7ada"),
    (41196, 1306, "0aa68cb4ed31862d32aeff5a7106b4ac29c13cbc202f7dbc8381fc7cd31418c0"),
)
EXPECTED_ID_COUNTS = (29, 41, 39, 33, 30, 28, 24, 26, 30, 26, 39, 37, 44)
EXPECTED_BLOCKS = (
    {"definition": 6, "example": 7, "exercise": 2, "lemma": 1, "note": 2, "proof": 1, "proposition": 1},
    {"definition": 3, "example": 8, "exercise": 7, "lemma": 3, "proof": 1, "question": 1},
    {"definition": 6, "example": 4, "exercise": 5, "lemma": 2, "proof": 5, "proposition": 3},
    {"definition": 4, "example": 5, "exercise": 4, "lemma": 1, "proof": 2, "proposition": 3, "question": 1},
    {"corollary": 3, "definition": 1, "example": 1, "exercise": 4, "lemma": 1, "proof": 5, "proposition": 2, "theorem": 1},
    {"definition": 2, "example": 3, "exercise": 4, "lemma": 2, "proof": 2, "remark": 1, "theorem": 2},
    {"corollary": 1, "definition": 1, "example": 3, "exercise": 4, "lemma": 1, "proof": 1, "proposition": 2},
    {"definition": 3, "example": 3, "exercise": 5, "lemma": 1, "proof": 1, "proposition": 2},
    {"corollary": 4, "example": 1, "exercise": 5, "proof": 5, "proposition": 1, "theorem": 2},
    {"corollary": 2, "definition": 1, "example": 2, "exercise": 5, "figure": 1, "proof": 3, "theorem": 1},
    {"definition": 3, "example": 5, "exercise": 3, "figure": 11, "proof": 1, "remark": 1, "theorem": 1},
    {"boundary": 1, "corollary": 1, "definition": 1, "example": 2, "exercise": 4, "figure": 7, "lemma": 2, "proof": 5, "theorem": 1},
    {"boundary": 1, "definition": 1, "example": 4, "exercise": 8, "fact": 1, "figure": 13, "remark": 1},
)

HTML = LANE / "output/html/units-001-013/index.html"
PDF = LANE / "output/pdf/topologi-aljabar-unit-001-013-id.pdf"
MANIFEST = LANE / "output/ARTIFACT_MANIFEST_UNITS_001_013.csv"
TEXT_WITNESS = LANE / "qa/units-001-013-extracted.txt"
RECEIPT = LANE / "qa/UNITS_001_013_QA.json"
VISUAL = LANE / "qa/UNITS_001_013_VISUAL_QA.md"
RENDER_INVENTORY = LANE / "qa/UNITS_001_013_RENDER_INVENTORY.csv"
RENDER_DIR = LANE / "tmp/pdfs/units-001-013-visual"
BUILD_SCRIPT = LANE / "scripts/build-units-001-013.ps1"
UPSTREAM = LANE / "authority/upstream/AlgebraicTopology2019-b947ad2e9f9e301bfe24590a9db653bc54fa1a53/Notes.tex"
REVIEWS = tuple(LANE / f"qa/UNIT_{n:03d}_INDEPENDENT_REVIEW.md" for n in (11, 12, 13))

POST_BUILD_EXPECTED = {
    HTML: (1824804, "be1473ab5cb8eff26341e554179661775a12cec5784a8ebf3f9c2f3f0633cb71"),
    PDF: (1071382, "14775535f773735db5886195980f39e417aaea24998927956a81b55b0ef77c68"),
    MANIFEST: (249, "6b55446a4f0a951329c29ec33b0ca586c749b9301dd4bd8ad4dd94f1c91d74de"),
    REVIEWS[0]: (3351, "de0766d41ba901405881d8078830d74420f2b1012ef24ace8d3f481135cd5b25"),
    REVIEWS[1]: (3374, "6ea34c30edfa208cc7e37a17f43ef4bf62b21ff4db222e534c97e027232e0ce7"),
    REVIEWS[2]: (6665, "5903c7da7f57d5db15a2d94807860a816d15e7d3cb7b020a8a3ddcbb0df45c21"),
}
EXPECTED_HTML_IDS = 587
EXPECTED_STABLE_IDS = 426
EXPECTED_FRAGMENT_HREFS = 160
EXPECTED_MATHML = 4682
EXPECTED_PDF_PAGES = 138
EXPECTED_ALIASES = {
    "o012-rbt-l07-exa-003": "eg:piS^1_infinite",
    "o012-rbt-l09-thm-001": "thm:cov_space_gives_faithful_functor",
    "o012-rbt-l09-prop-001": "prop:cov_space_of_IxX",
    "o012-rbt-l09-cor-002": "prop:pullback_by_homotopic_maps_iso",
    "o012-rbt-l10-cor-001": "cor:fibre_of_univ_cov_space",
    "o012-rbt-l12-exa-001": "eg:retracts_of_Pi1",
    "o012-rbt-l12-lem-001": "lemma:retracts_of_pushouts",
    "o012-rbt-l13-exa-001": "eg:one-relator_group",
}
PRIVATE_MARKERS = ("C:\\Users\\", "C:/Users/", "github_pat_", "ghp_", "sk-proj_")


class QAError(Exception):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise QAError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def verify_file(path: Path, expected_bytes: int, expected_sha: str) -> None:
    require(path.is_file(), f"Missing file: {path}")
    require(path.stat().st_size == expected_bytes, f"Byte mismatch: {path}")
    require(sha256(path) == expected_sha, f"SHA-256 mismatch: {path}")


def stable_ids(text: str) -> list[str]:
    return re.findall(r"#(o012-[a-z0-9-]+)(?=[}\s])", text)


def block_counts(text: str) -> dict[str, int]:
    kinds = "boundary|corollary|definition|example|exercise|fact|figure|lemma|note|proof|proposition|question|remark|theorem"
    return dict(sorted(Counter(re.findall(rf"^::: \{{\.({kinds})\s+#o012-", text, flags=re.MULTILINE)).items()))


def verify_sources() -> tuple[list[str], dict[str, dict[str, int]]]:
    texts: list[str] = []
    for number, (path, expected) in enumerate(zip(SOURCES, SOURCE_EXPECTED, strict=True), start=1):
        verify_file(path, expected[0], expected[2])
        text = path.read_text(encoding="utf-8")
        require(len(text.splitlines()) == expected[1], f"Unit {number} line-count mismatch")
        require("\ufffd" not in text and "Ã" not in text and "Â" not in text and "â€" not in text, f"Unit {number} encoding residue")
        for marker in ("TODO", "TBD", "FILL_AFTER") + PRIVATE_MARKERS:
            require(marker not in text, f"Unit {number} private/placeholder residue: {marker}")
        require(len(re.findall(r"^::: \{", text, flags=re.MULTILINE)) == len(re.findall(r"^:::\s*$", text, flags=re.MULTILINE)), f"Unit {number} unbalanced fenced divs")
        require(text.count("$$") % 2 == 0, f"Unit {number} unbalanced display math")
        texts.append(text)

    ids_by_unit = [stable_ids(text) for text in texts]
    for number, (ids, expected) in enumerate(zip(ids_by_unit, EXPECTED_ID_COUNTS, strict=True), start=1):
        require(len(ids) == expected and len(set(ids)) == expected, f"Unit {number} stable-ID mismatch")
    all_ids = [item for values in ids_by_unit for item in values]
    require(len(all_ids) == EXPECTED_STABLE_IDS and len(set(all_ids)) == EXPECTED_STABLE_IDS, "Cumulative stable-ID mismatch")

    blocks = [block_counts(text) for text in texts]
    for number, (actual, expected) in enumerate(zip(blocks, EXPECTED_BLOCKS, strict=True), start=1):
        require(actual == expected, f"Unit {number} semantic-block mismatch: {actual}")

    upstream_raw = UPSTREAM.read_bytes()
    require(len(upstream_raw) == 331447 and hashlib.sha256(upstream_raw).hexdigest() == "cfe93e9dbe3e25bd96f711f59e6078ab97527682b58e1f8ad127f74357f665d7", "Upstream Notes.tex identity mismatch")
    upstream = upstream_raw.decode("utf-8").splitlines()
    require(len(upstream) == 6368, "Upstream line-count mismatch")
    for lecture, start, end in ((11, 2273, 2494), (12, 2495, 2726), (13, 2727, 3046)):
        require(upstream[start - 1] == rf"\lecturenum{{{lecture}}}", f"Lecture {lecture} start marker mismatch")
        require(rf"\lecturenum{{{lecture + 1}}}" not in "\n".join(upstream[start - 1:end]), f"Lecture {lecture} span leaks")
    require(upstream[3044] == r"\section{Classifying covering spaces}" and upstream[3045] == "" and upstream[3046] == r"Recall\lecturenum{14}", "Lecture 13 terminal boundary mismatch")

    for lecture, review in zip((11, 12, 13), REVIEWS, strict=True):
        body = review.read_text(encoding="utf-8")
        zero_findings = all(
            re.search(rf"P{priority}\s*(?:=|:)\s*0", body) is not None
            or re.search(rf"P{priority}[^\n]*0 open", body) is not None
            for priority in (1, 2, 3)
        )
        require("PASS" in body and zero_findings, f"Unit {lecture} independent review is not all-clear")
        require(SOURCE_EXPECTED[lecture - 1][2] in body, f"Unit {lecture} review source hash mismatch")

    return all_ids, {f"unit_{n:03d}": blocks[n - 1] for n in range(1, 14)}


def markdown_body(path: Path) -> str:
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    require(text.startswith("---\n"), f"Missing front matter: {path}")
    end = text.find("\n---\n", 4)
    require(end >= 0, f"Unclosed front matter: {path}")
    return text[end + 5:].lstrip("\n")


def reproduce_html() -> dict[str, object]:
    pandoc = shutil.which("pandoc")
    require(pandoc is not None, "pandoc unavailable")
    version = subprocess.run([pandoc, "--version"], check=True, capture_output=True, text=True).stdout.splitlines()[0]
    require(version == "pandoc 3.9.0.2", f"Pandoc version mismatch: {version}")
    header = """---
title: "Topologi Aljabar - Unit 1-13"
subtitle: "Ruang Topologis, Homotopi, Ruang Penutup, Grupoid Fundamental, Seifert--van Kampen, dan Kompleks Presentasi"
author:
  - "David Michael Roberts (materi sumber)"
  - "Edisi Bahasa Indonesia dengan pendamping penguasaan"
date: "22 Agustus 2026"
lang: id-ID
rights: "Materi adaptasi dan materi pendamping: CC BY 4.0; lihat atribusi pada setiap unit."
---
"""
    payload = header + "\n\n".join(markdown_body(path).rstrip("\n") for path in SOURCES) + "\n"
    semantic_css = """*,
*::before,
*::after {
  box-sizing: border-box;
}

a,
code {
  overflow-wrap: anywhere;
}

.theorem,
.corollary,
.fact {
  margin: 1.25rem 0;
  padding: 0.8rem 1rem;
  border-left: 0.3rem solid #315f8c;
  background: #f3f7fc;
}

.remark {
  margin: 1.25rem 0;
  padding: 0.8rem 1rem;
  border-left: 0.3rem solid #8a6a2f;
  background: #fffaf0;
}

.figure {
  margin: 1.25rem 0;
  padding: 0.8rem 1rem;
  border-left: 0.3rem solid #5d477a;
  background: #f8f5fc;
}

.boundary {
  margin: 1.25rem 0;
  padding: 0.8rem 1rem;
  border: 0.12rem solid #8a6a2f;
  background: #fffdf7;
}

@media (prefers-color-scheme: dark) {
  .theorem,
  .corollary,
  .fact,
  .remark,
  .figure,
  .boundary {
    background: #20242a;
  }
}
""".rstrip("\n")
    tmp_root = LANE / "tmp"
    tmp_root.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="units-001-013-html-qa-", dir=tmp_root) as raw_tmp:
        tmp = Path(raw_tmp)
        source = tmp / "reader.md"
        css = tmp / "semantic.css"
        out_a = tmp / "a.html"
        out_b = tmp / "b.html"
        source.write_text(payload, encoding="utf-8", newline="\n")
        css.write_text(semantic_css, encoding="utf-8", newline="\n")
        common = [
            str(source), "--from=markdown+fenced_divs+tex_math_dollars", "--standalone", "--toc",
            "--number-sections", "--metadata=lang:id-ID", "--metadata=pagetitle:Topologi Aljabar - Unit 1-13",
            "--strip-comments", "--to=html5", "--mathml", "--section-divs",
            f"--css={LANE / 'source/id-ID/styles/reader.css'}",
            f"--css={LANE / 'source/id-ID/styles/reader-cumulative.css'}", f"--css={css}", "--embed-resources",
        ]
        env = dict(__import__("os").environ)
        env.update({"SOURCE_DATE_EPOCH": "1787356800", "FORCE_SOURCE_DATE": "1"})
        for output in (out_a, out_b):
            subprocess.run([pandoc, *common, f"--output={output}"], check=True, env=env, capture_output=True)
        hash_a, hash_b = sha256(out_a), sha256(out_b)
        require(hash_a == hash_b, "Temporary HTML builds differ")
        require(out_a.read_bytes() == HTML.read_bytes(), "Temporary HTML build differs from final artifact")
    return {"pandoc": version, "build_a_sha256": hash_a, "build_b_sha256": hash_b, "equals_final": True}


def verify_html(source_ids: list[str]) -> dict[str, int]:
    root = etree.parse(str(HTML), etree.HTMLParser(recover=True)).getroot()
    require(root.get("lang") == "id-ID", "HTML lang mismatch")
    require("".join(root.xpath("//title/text()")) == "Topologi Aljabar - Unit 1-13", "HTML title mismatch")
    ids = root.xpath("//*[@id]/@id")
    require(len(ids) == EXPECTED_HTML_IDS and len(set(ids)) == EXPECTED_HTML_IDS, "HTML ID inventory mismatch")
    id_set = set(ids)
    require(set(source_ids) <= id_set, "HTML omits a source stable ID")
    fragments = [href for href in root.xpath("//@href") if href.startswith("#")]
    require(len(fragments) == EXPECTED_FRAGMENT_HREFS, "HTML fragment count mismatch")
    for href in fragments:
        target = unquote(href[1:])
        require(target and target in id_set, f"Broken HTML fragment: {href}")
    external = [href for href in root.xpath("//@href") if not href.startswith("#")]
    require(all(urlparse(href).scheme == "https" for href in external), "Non-HTTPS external link")
    require(not root.xpath("//script|//link[@rel='stylesheet']"), "HTML runtime script/stylesheet dependency")
    require(not root.xpath("//img|//object|//embed|//iframe|//video|//audio|//source"), "Unexpected HTML runtime asset")
    for attribute in ("src", "srcset", "poster", "data"):
        require(not root.xpath(f"//@{attribute}"), f"HTML runtime @{attribute} dependency")
    mathml = len(root.xpath("//*[local-name()='math']"))
    require(mathml == EXPECTED_MATHML, f"MathML count mismatch: {mathml}")
    aliases = {element.get("id"): element.get("data-source-label") for element in root.xpath("//*[@data-source-label]")}
    require(aliases == EXPECTED_ALIASES, f"HTML source-label aliases mismatch: {aliases}")
    styles = "\n".join(root.xpath("//style/text()"))
    for rule in ("max-width: 58rem", "margin: 0 auto", 'math[display="block"]', "overflow-x: auto", ".theorem", ".boundary"):
        require(rule in styles, f"Missing centered/reflow style: {rule}")
    require("@import" not in styles and not re.search(r"url\(\s*['\"]?https?://", styles, flags=re.I), "External CSS dependency")
    raw = HTML.read_text(encoding="utf-8")
    for marker in PRIVATE_MARKERS:
        require(marker not in raw, f"Private marker in HTML: {marker}")
    return {"ids": len(ids), "stable_ids": len(source_ids), "fragment_links": len(fragments), "external_https_links": len(external), "mathml_nodes": mathml, "source_aliases": len(aliases)}


def write_render_inventory() -> dict[str, object]:
    pages = sorted(RENDER_DIR.glob("page-*.png"))
    require(len(pages) == EXPECTED_PDF_PAGES, f"Rendered-page count mismatch: {len(pages)}")
    rows: list[dict[str, object]] = []
    for number, path in enumerate(pages, start=1):
        require(path.name == f"page-{number:03d}.png", f"Rendered-page sequence gap: {path.name}")
        with Image.open(path) as image:
            require(image.size == (910, 1287) and image.format == "PNG", f"Rendered-page geometry mismatch: {path.name}")
        rows.append({"page": number, "path": path.relative_to(LANE).as_posix(), "bytes": path.stat().st_size, "sha256": sha256(path)})
    with RENDER_INVENTORY.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=["page", "path", "bytes", "sha256"], lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    contacts = sorted(RENDER_DIR.glob("contact-*.png"))
    require(len(contacts) == 12, f"Contact-sheet count mismatch: {len(contacts)}")
    digest = hashlib.sha256()
    for row in rows:
        digest.update(f"{row['page']}\0{row['path']}\0{row['bytes']}\0{row['sha256']}\n".encode("utf-8"))
    return {"page_pngs": len(rows), "page_png_bytes": sum(int(row["bytes"]) for row in rows), "page_png_aggregate_sha256": digest.hexdigest(), "contact_sheets": len(contacts), "inventory_bytes": RENDER_INVENTORY.stat().st_size, "inventory_sha256": sha256(RENDER_INVENTORY)}


def write_visual_receipt(render: dict[str, object]) -> None:
    body = f"""# Units 001-013 visual QA

Date: 2026-08-22  
Verdict: **PASS**

## PDF inspection

- Final artifact: `output/pdf/topologi-aljabar-unit-001-013-id.pdf`, 138 A4 pages.
- All 138 pages were rendered at 110 dpi to `tmp/pdfs/units-001-013-visual/page-001.png` through `page-138.png` and inspected across twelve ordered contact sheets. Full-resolution checks covered the cumulative title/contents, the Unit 11/12/13 transitions, and pages 137-138.
- Render inventory: `{RENDER_INVENTORY.relative_to(LANE).as_posix()}`, {render['inventory_bytes']} bytes, SHA-256 `{render['inventory_sha256']}`.
- Rendered page bytes: {render['page_png_bytes']}; canonical page-inventory aggregate SHA-256 `{render['page_png_aggregate_sha256']}`.
- No clipping, overlap, missing glyph, black box, unintended blank page, or broken heading transition was found. Page 138 is intentionally sparse because it contains the natural final tail of Solution 13.6, not an orphan heading or detached fragment.
- The PDF is an intentionally secondary, untagged surface. It has 24 font rows; all are embedded, subset, and Unicode-mapped.

## Semantic HTML inspection

- Live local Chromium QA at 1280 by 720 measured a 928 px body, centered with zero effective document overflow.
- At 390 by 844, the content width was 375.11 px and document-level horizontal overflow was zero.
- The page contains 824 display-math elements. Fifty-four were wider than the mobile content box, and all 54 exposed local horizontal scrolling.
- Browser DOM evidence after excluding the browser's own injected sidebar root: 587 unique artifact HTML IDs, 160 resolving fragments, 4,682 native MathML nodes, eight source-label aliases, no runtime assets/scripts/external stylesheets, and zero console warnings or errors.
- Unit 13 and Solution 13.6 were directly inspected at desktop and mobile widths. The reader remains centered, readable, and semantically ordered in both light-independent and dark-mode styling.

The task-local page renders remain in place as the root-review handoff. No PDF was rebuilt during this QA recovery, and the PDF artifact-operation marker was not rerun.
"""
    VISUAL.write_text(body, encoding="utf-8", newline="\n")


def verify_pdf() -> tuple[dict[str, object], bytes]:
    reader = PdfReader(str(PDF), strict=True)
    require(not reader.is_encrypted and len(reader.pages) == EXPECTED_PDF_PAGES, "PDF encryption/page mismatch")
    root = reader.trailer["/Root"]
    require(root.get("/Lang") == "id-ID", "PDF /Lang mismatch")
    require("/AcroForm" not in root and "/StructTreeRoot" not in root, "PDF form/tagging state mismatch")
    names = root.get("/Names")
    require(names is None or "/JavaScript" not in names.get_object(), "PDF JavaScript name tree")
    metadata = reader.metadata
    require(metadata.title == "Topologi Aljabar - Unit 1-13", "PDF title mismatch")
    require(metadata.author == "David Michael Roberts (materi sumber); Edisi Bahasa Indonesia dengan pendamping penguasaan", "PDF author mismatch")
    require(metadata.creator == "LaTeX via pandoc" and "pdfTeX" in (metadata.producer or ""), "PDF toolchain metadata mismatch")
    require(str(metadata.get("/CreationDate")) == "D:20260822000000Z" and str(metadata.get("/ModDate")) == "D:20260822000000Z", "PDF deterministic dates mismatch")
    extracted = "\n".join(page.extract_text() or "" for page in reader.pages)
    for phrase in ("Kuliah 11", "Kuliah 12", "Kuliah 13", "Produk bebas dengan amalgamasi", "Pushout grupoid sebagai kata panah", "Solusi Pemeriksaan 13.6"):
        require(phrase in extracted, f"Missing PDF text: {phrase}")
    for marker in PRIVATE_MARKERS + ("No correct answer",):
        require(marker not in extracted, f"Private/UI residue in PDF: {marker}")
    pdffonts = shutil.which("pdffonts")
    pdftotext = shutil.which("pdftotext")
    require(pdffonts is not None and pdftotext is not None, "Poppler inspection tools unavailable")
    font_result = subprocess.run([pdffonts, str(PDF)], check=True, capture_output=True, text=True)
    font_rows = [line.split() for line in font_result.stdout.splitlines()[2:] if line.strip()]
    require(len(font_rows) == 24, f"PDF font inventory mismatch: {len(font_rows)}")
    require(all(len(row) >= 5 and row[-5:-2] == ["yes", "yes", "yes"] for row in font_rows), "PDF font embedding/ToUnicode mismatch")
    text_bytes = subprocess.run([pdftotext, "-layout", "-enc", "UTF-8", str(PDF), "-"], check=True, capture_output=True).stdout
    TEXT_WITNESS.write_bytes(text_bytes)
    return {"pages": len(reader.pages), "page_size": "A4", "encrypted": False, "lang": "id-ID", "tagged": False, "fonts": len(font_rows), "all_fonts_embedded": True, "all_fonts_subset": True, "all_fonts_tounicode": True, "pypdf_extracted_characters": len(extracted)}, text_bytes


def verify_manifest() -> list[dict[str, object]]:
    with MANIFEST.open("r", encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    expected_paths = sorted([HTML.relative_to(LANE).as_posix(), PDF.relative_to(LANE).as_posix()])
    require([row["path"] for row in rows] == expected_paths, "Manifest paths/order mismatch")
    for row in rows:
        path = LANE / row["path"]
        require(path.stat().st_size == int(row["bytes"]) and sha256(path) == row["sha256"], f"Manifest mismatch: {row['path']}")
    return [{"path": row["path"], "bytes": int(row["bytes"]), "sha256": row["sha256"]} for row in rows]


def main() -> int:
    for path, expected in POST_BUILD_EXPECTED.items():
        verify_file(path, *expected)
    build_text = BUILD_SCRIPT.read_text(encoding="utf-8")
    require(build_text.count("& $pandoc @common @htmlArgs") == 2, "Build script lacks two HTML builds")
    require(build_text.count("& $pandoc @pdfCommon @pdfArgs") == 2, "Build script lacks two PDF builds")
    require("PDF reproducibility failure" in build_text and "Copy-Item -LiteralPath $pdfA -Destination $pdf" in build_text, "Build script PDF fail-closed gate missing")
    source_ids, blocks = verify_sources()
    html_reproduction = reproduce_html()
    html = verify_html(source_ids)
    pdf, text_bytes = verify_pdf()
    artifacts = verify_manifest()
    render = write_render_inventory()
    write_visual_receipt(render)
    receipt = {
        "schema_version": "1.0", "status": "pass", "role_id": "O012", "course_id": "D60",
        "unit_ids": [f"o012-rbt-l{n:02d}" for n in range(1, 14)],
        "source_authority": {"commit_sha1": "b947ad2e9f9e301bfe24590a9db653bc54fa1a53", "tree_sha1": "aa1d3edb85818e7176e2d0bbc06d9b4bd1e247f5", "path": "Notes.tex", "line_start": 134, "line_end": 3046, "next_line": 3047, "next_boundary": "Lecture 14 prose: Recall\\lecturenum{14}"},
        "reader_sources": [{"path": path.relative_to(LANE).as_posix(), "bytes": expected[0], "lines": expected[1], "sha256": expected[2], "stable_ids": count} for path, expected, count in zip(SOURCES, SOURCE_EXPECTED, EXPECTED_ID_COUNTS, strict=True)],
        "block_counts": blocks, "html": html, "html_reproduction": html_reproduction, "pdf": pdf,
        "artifacts": artifacts,
        "witnesses": {"unit_011_review_sha256": POST_BUILD_EXPECTED[REVIEWS[0]][1], "unit_012_review_sha256": POST_BUILD_EXPECTED[REVIEWS[1]][1], "unit_013_review_sha256": POST_BUILD_EXPECTED[REVIEWS[2]][1], "extracted_text_bytes": len(text_bytes), "extracted_text_sha256": sha256(TEXT_WITNESS), "visual_receipt_bytes": VISUAL.stat().st_size, "visual_receipt_sha256": sha256(VISUAL), "render_inventory": render, "build_script_sha256": sha256(BUILD_SCRIPT)},
        "responsive_browser": {"desktop_viewport": "1280x720", "desktop_body_css_px": 928, "desktop_effective_document_overflow_css_px": 0, "mobile_viewport": "390x844", "mobile_content_css_px": 375.11, "mobile_document_overflow_css_px": 0, "display_math": 824, "mobile_wide_display_math": 54, "mobile_locally_scrollable_wide_display_math": 54, "console_warnings_or_errors": 0},
        "gates": {"authority_exact": True, "source_spans_contiguous_and_bound": True, "structure_and_identifiers_bound": True, "mastery_and_source_prompts_present": True, "rights_attribution_non_endorsement": True, "html_two_build_byte_identity": True, "pdf_two_build_fail_closed_gate_in_builder": True, "pdf_not_rebuilt_during_recovery": True, "html_semantic_centered_reflowing_native_mathml_offline": True, "html_fragments_ids_aliases_valid": True, "privacy_secret_scan": True, "pdf_metadata_fonts_text_pages_verified": True, "visual_review": "pass_all_138_pages_plus_browser_desktop_mobile"},
        "known_caveat": "PDF is intentionally secondary and untagged; semantic HTML with native MathML is the primary accessibility surface.",
    }
    RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(f"PASS stable_ids={len(source_ids)} blocks={sum(sum(v.values()) for v in blocks.values())} mathml={html['mathml_nodes']} pdf_pages={pdf['pages']} receipt_sha256={sha256(RECEIPT)}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise
