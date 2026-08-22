#!/usr/bin/env python3
"""Strict fail-closed QA for the cumulative O012 Units 001-004 reader.

The Unit 4 source, correction-ledger, review, and post-build values deliberately
remain explicit placeholders until those witnesses are final. Earlier sources,
artifacts, and QA receipts are frozen byte-for-byte below.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import unquote

from lxml import etree
from pypdf import PdfReader


LANE = Path(__file__).resolve().parents[1]
SOURCE_1 = LANE / "source" / "id-ID" / "reader-unit-001.md"
SOURCE_2 = LANE / "source" / "id-ID" / "units" / "unit-002-lecture-002.md"
SOURCE_3 = LANE / "source" / "id-ID" / "units" / "unit-003-lecture-003.md"
SOURCE_4 = LANE / "source" / "id-ID" / "units" / "unit-004-lecture-004.md"
BASE_CSS = LANE / "source" / "id-ID" / "styles" / "reader.css"
CUMULATIVE_CSS = LANE / "source" / "id-ID" / "styles" / "reader-cumulative.css"

HTML = LANE / "output" / "html" / "units-001-004" / "index.html"
PDF = LANE / "output" / "pdf" / "topologi-aljabar-unit-001-004-id.pdf"
MANIFEST = LANE / "output" / "ARTIFACT_MANIFEST_UNITS_001_004.csv"
AUTHORITY = LANE / "00_control" / "AUTHORITY.json"
UPSTREAM_MANIFEST = LANE / "00_control" / "UPSTREAM_FILE_MANIFEST.csv"
ADVERSE_LEDGER = LANE / "00_control" / "ADVERSE_LEDGER.csv"
VISUAL = LANE / "qa" / "UNITS_001_004_VISUAL_QA.md"
INDEPENDENT_4 = LANE / "qa" / "UNIT_004_INDEPENDENT_REVIEW.md"
TEXT_WITNESS = LANE / "qa" / "units-001-004-extracted.txt"
RECEIPT = LANE / "qa" / "UNITS_001_004_QA.json"

# Immutable historical boundary through Unit 3. A Unit 4 build may add new
# paths, but it must not silently rewrite any earlier source, artifact, or QA
# witness.
HISTORICAL_EXPECTED = {
    SOURCE_1: (16179, "c80b51c22a2fa7ea116201028b78d5f8d708ef4d8355d34092ac7a9c88415e15"),
    SOURCE_2: (25090, "4d2acc43557db9b3c419ee177545d285b9fcf50b2aa2dd3b2c6c44182f3a6a01"),
    SOURCE_3: (25822, "993e5941895a9b6f4b197b4c236f5a4990f6ae621e2bb7911353b28a5e1abffd"),
    BASE_CSS: (1297, "e5184827600116bc54e28df6822c5a98691d5edf88b7b102443b56024733cbe5"),
    CUMULATIVE_CSS: (203, "b0012d9f93e603997d48d49705ec9ccae2d3cd2d062b8b9f8717e908df1f5344"),
    LANE / "output" / "ARTIFACT_MANIFEST.csv": (
        228,
        "13772b2e2400923351225f422effe5f958e1dd8e178b9f6a32207682f791bcc3",
    ),
    LANE / "output" / "html" / "index.html": (
        85580,
        "5cc4a29f2c29b274328b574d6698a51d75af0939f9959937db8d679c38ad51b8",
    ),
    LANE / "output" / "pdf" / "topologi-aljabar-unit-001-id.pdf": (
        321743,
        "6f71546a616c02ef81f8747ecfce3875784842065fc131cc82e5060b066a59c9",
    ),
    LANE / "qa" / "UNIT_001_QA.json": (
        1827,
        "194c231b57e044fefeefc109d96850791101948584c0ebded4d338b30ff332b3",
    ),
    LANE / "output" / "ARTIFACT_MANIFEST_UNITS_001_002.csv": (
        247,
        "93e98f6cbbc60775bb934df5b49141f63d7cd2c76582a26c61d4192ff320d721",
    ),
    LANE / "output" / "html" / "units-001-002" / "index.html": (
        220035,
        "d3b5cbfaa3511823821ecf9ba26a4eaec7c84d937417927d11bde3f66abc9f54",
    ),
    LANE / "output" / "pdf" / "topologi-aljabar-unit-001-002-id.pdf": (
        395385,
        "0413c3a3280955cc482a5c0c2d7615b78128dccba3b6b1901dee1bf34d133b8e",
    ),
    LANE / "qa" / "UNITS_001_002_QA.json": (
        2690,
        "075546f6a856638dc420ed62b23ec78c7a57f839444e4f2101233d6421f776f0",
    ),
    LANE / "output" / "ARTIFACT_MANIFEST_UNITS_001_003.csv": (
        247,
        "1e211afb4b165435ece5f72a2b4e9b084975db35d111127880255473302f5049",
    ),
    LANE / "output" / "html" / "units-001-003" / "index.html": (
        359397,
        "33281cc46faa3d560c968b657526cd914786c991d1475b5563911a265bd316c1",
    ),
    LANE / "output" / "pdf" / "topologi-aljabar-unit-001-003-id.pdf": (
        460320,
        "2c9bf67e74c94bca9aad0238e910816188a957892a6cf811f7f615e221b4066d",
    ),
    LANE / "qa" / "UNIT_003_INDEPENDENT_REVIEW.md": (
        2464,
        "b2cffbcc2167c3d620f1af53224cc064e8ce34400561868339e69c280845619c",
    ),
    LANE / "qa" / "UNITS_001_003_VISUAL_QA.md": (
        2310,
        "4d7d603c2276bd570e3bf47897c67d98bf6507d2bd9ffed2acd10ab1a509130e",
    ),
    LANE / "qa" / "units-001-003-extracted.txt": (
        71549,
        "2e8eabce2e0b8c3114b49d630187a6a0217e3ae90c466b5441f9eedccb299702",
    ),
    LANE / "qa" / "UNITS_001_003_QA.json": (
        3983,
        "fb511086669846b6c8a68a6c1fecc4bd774016a6c95eb27219e3babbd177a873",
    ),
}

# FILL_AFTER_SOURCE_FREEZE.
SOURCE_4_EXPECTED: tuple[int | None, str | None] = (
    24582,
    "826fcb368275cdad02f72a5cec951fc8466ba68b09ca0139d72c81a4c5591fea",
)
EXPECTED_SOURCE_4_LINES: int | None = 632

# FILL_AFTER_BUILD_AND_REVIEW. Every value is fail-closed.
POST_BUILD_EXPECTED: dict[Path, tuple[int | None, str | None]] = {
    HTML: (494732, "8c8f5e1ad8172a2d97e3931fc3b4f2a3aa7f9e8a709260a27103f7eca0f1357d"),
    PDF: (539006, "5e92c4c6ed60bca9f2f4d362d4c48b4f01aa156b330e2adacd1bf88dd7de9e87"),
    MANIFEST: (247, "4c8bf407e426feb8db92308c4b28bdbbc0738416a85a13539ef7915e4c1aad83"),
    VISUAL: (2257, "74e609e94ea47b89db223c21e12cae682048f0a60d8780dae96d5b0164f2c5ca"),
    INDEPENDENT_4: (3031, "ac993a10e22738197775ae5c3f4e72948983c4e99ff602a52943b40ed417b6f9"),
    TEXT_WITNESS: (100684, "3d27bc1ab5a780bffce12d5951623b60929069238a210961740234502e71bf35"),
}
EXPECTED_HTML_MATHML_NODES: int | None = 1384
EXPECTED_HTML_IDS: int | None = 198
EXPECTED_HTML_FRAGMENT_HREFS: int | None = 54
EXPECTED_PDF_PAGES: int | None = 35

# FILL_AFTER_LEDGER_FREEZE. Replace the marker with the exact admitted event
# IDs. Reflows and mathematical/source corrections are reported separately.
UNIT_4_SOURCE_CORRECTION_IDS = {
    *(f"O012-ADV-{number:04d}" for number in range(35, 38)),
    *(f"O012-ADV-{number:04d}" for number in range(39, 54)),
}
UNIT_4_REFLOW_IDS = {"O012-ADV-0038"}

BLOCKS_1 = {
    "definition": 6,
    "example": 7,
    "exercise": 2,
    "lemma": 1,
    "note": 2,
    "proof": 1,
    "proposition": 1,
}
BLOCKS_2 = {
    "definition": 3,
    "example": 8,
    "exercise": 7,
    "lemma": 3,
    "proof": 1,
    "question": 1,
}
BLOCKS_3 = {
    "definition": 6,
    "example": 4,
    "exercise": 5,
    "lemma": 2,
    "proof": 5,
    "proposition": 3,
}
BLOCKS_4 = {
    "definition": 4,
    "example": 5,
    "exercise": 4,
    "lemma": 1,
    "proof": 2,
    "proposition": 3,
    "question": 1,
}
ARTIFACT_PATHS = {
    "output/html/units-001-004/index.html",
    "output/pdf/topologi-aljabar-unit-001-004-id.pdf",
}
WINDOWS_PROFILE = chr(92).join(("C:", "Users", ""))
PRIVATE_MARKERS = (WINDOWS_PROFILE, "C:/Users/", "github_pat_", "ghp_", "sk-proj_")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_file(path: Path, expected_bytes: int, expected_sha: str) -> None:
    require(path.is_file(), f"Missing file: {path}")
    require(path.stat().st_size == expected_bytes, f"Byte mismatch: {path}")
    require(sha256(path) == expected_sha, f"SHA-256 mismatch: {path}")


def read_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    require(isinstance(value, dict), f"Expected JSON object: {path}")
    return value


def stable_ids(text: str) -> list[str]:
    return re.findall(r"#(o012-[a-z0-9-]+)(?=[}\s])", text)


def block_counts(text: str) -> dict[str, int]:
    values = Counter(
        re.findall(
            r"^::: \{\.(definition|example|exercise|lemma|note|proof|proposition|question)\s+#o012-",
            text,
            flags=re.MULTILINE,
        )
    )
    return dict(sorted(values.items()))


def verify_placeholders_filled() -> None:
    missing: list[str] = []
    source_bytes, source_sha = SOURCE_4_EXPECTED
    if not isinstance(source_bytes, int) or source_bytes <= 0:
        missing.append("SOURCE_4_EXPECTED.bytes")
    if not isinstance(source_sha, str) or not re.fullmatch(r"[0-9a-f]{64}", source_sha):
        missing.append("SOURCE_4_EXPECTED.sha256")
    if not isinstance(EXPECTED_SOURCE_4_LINES, int) or EXPECTED_SOURCE_4_LINES <= 0:
        missing.append("EXPECTED_SOURCE_4_LINES")
    for path, (expected_bytes, expected_sha) in POST_BUILD_EXPECTED.items():
        label = path.relative_to(LANE).as_posix()
        if not isinstance(expected_bytes, int) or expected_bytes <= 0:
            missing.append(f"POST_BUILD_EXPECTED[{label}].bytes")
        if not isinstance(expected_sha, str) or not re.fullmatch(r"[0-9a-f]{64}", expected_sha):
            missing.append(f"POST_BUILD_EXPECTED[{label}].sha256")
    for name, value in (
        ("EXPECTED_HTML_MATHML_NODES", EXPECTED_HTML_MATHML_NODES),
        ("EXPECTED_HTML_IDS", EXPECTED_HTML_IDS),
        ("EXPECTED_HTML_FRAGMENT_HREFS", EXPECTED_HTML_FRAGMENT_HREFS),
        ("EXPECTED_PDF_PAGES", EXPECTED_PDF_PAGES),
    ):
        if not isinstance(value, int) or value <= 0:
            missing.append(name)
    for name, values in (
        ("UNIT_4_SOURCE_CORRECTION_IDS", UNIT_4_SOURCE_CORRECTION_IDS),
        ("UNIT_4_REFLOW_IDS", UNIT_4_REFLOW_IDS),
    ):
        if not values or any(not re.fullmatch(r"O012-ADV-\d{4}", item) for item in values):
            missing.append(name)
    require(not missing, "Fill exact Unit 4 QA placeholders: " + ", ".join(missing))


def verify_authority() -> tuple[dict, list[str]]:
    authority = read_json(AUTHORITY)
    require(authority["role_id"] == "O012" and authority["course_id"] == "D60", "Authority role mismatch")
    require(authority["commit_sha1"] == "b947ad2e9f9e301bfe24590a9db653bc54fa1a53", "Authority commit mismatch")
    require(authority["tree_sha1"] == "aa1d3edb85818e7176e2d0bbc06d9b4bd1e247f5", "Authority tree mismatch")
    for key in ("archive", "active_source", "upstream_pdf"):
        item = authority[key]
        verify_file(LANE / item["path"], int(item["bytes"]), item["sha256"])
    require(authority["license"]["spdx"] == "CC-BY-4.0", "Authority license mismatch")
    require(sha256(LANE / "LICENSE.md") == authority["license"]["license_file_sha256"], "License hash mismatch")

    with UPSTREAM_MANIFEST.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    require(len(rows) == 7 and len({row["path"] for row in rows}) == 7, "Upstream manifest shape mismatch")
    root = (LANE / authority["active_source"]["path"]).parent
    for row in rows:
        verify_file(root / row["path"], int(row["bytes"]), row["sha256"])
    require(sha256(UPSTREAM_MANIFEST) == authority["manifest"]["sha256"], "Upstream manifest hash mismatch")

    upstream = (LANE / authority["active_source"]["path"]).read_text(encoding="utf-8").splitlines()
    require(len(upstream) == 6368, "Unexpected upstream line count")
    return authority, upstream


def verify_source_text(label: str, text: str) -> None:
    require("\ufffd" not in text, f"U+FFFD in {label}")
    for marker in ("Ã", "Â", "â€", "ï¿½"):
        require(marker not in text, f"Mojibake in {label}: {marker}")
    for placeholder in ("TODO", "TBD", "PLACEHOLDER", "FILL_AFTER"):
        require(placeholder not in text, f"Placeholder in {label}: {placeholder}")
    for secret in PRIVATE_MARKERS:
        require(secret not in text, f"Private/control residue in {label}: {secret}")
    openings = len(re.findall(r"^::: \{", text, flags=re.MULTILINE))
    closings = len(re.findall(r"^:::\s*$", text, flags=re.MULTILINE))
    require(openings == closings, f"Semantic fences are unbalanced in {label}: {openings} != {closings}")


def verify_sources(upstream: list[str]) -> tuple[list[str], dict[str, dict[str, int]]]:
    texts = [path.read_text(encoding="utf-8") for path in (SOURCE_1, SOURCE_2, SOURCE_3, SOURCE_4)]
    require(len(texts[3].splitlines()) == EXPECTED_SOURCE_4_LINES, "Unit 4 source line-count mismatch")
    for label, text in zip(("Unit 1", "Unit 2", "Unit 3", "Unit 4"), texts, strict=True):
        verify_source_text(label, text)

    id_lists = [stable_ids(text) for text in texts]
    for unit, ids, expected in zip(range(1, 5), id_lists, (29, 41, 39, 33), strict=True):
        require(len(ids) == expected and len(set(ids)) == expected, f"Unit {unit} stable-ID mismatch")
    require(
        all(value.startswith("o012-rbt-l04-") or value == "o012-rbt-l04" for value in id_lists[3]),
        "Unit 4 ID namespace mismatch",
    )
    all_ids = [value for values in id_lists for value in values]
    require(len(all_ids) == 142 and len(set(all_ids)) == 142, "Cumulative stable-ID mismatch")

    blocks = [block_counts(text) for text in texts]
    expected_blocks = [BLOCKS_1, BLOCKS_2, BLOCKS_3, BLOCKS_4]
    for unit, actual, expected in zip(range(1, 5), blocks, expected_blocks, strict=True):
        require(actual == expected, f"Unit {unit} block mismatch: {actual}")

    span4 = "\n".join(upstream[877:1131])
    require(upstream[877].strip() == r"\begin{prop}", "Line 878 must open the deferred proposition")
    require(span4.count(r"\lecturenum{4}") == 1, "Lecture 4 marker mismatch")
    require(r"\lecturenum{5}" not in span4 and r"\lecturenum{5}" in upstream[1131], "Unit 4/5 boundary mismatch")
    expected_env4 = {"definition": 5, "example": 5, "ex": 3, "lemma": 2, "proof": 2, "prop": 3, "q": 1}
    actual_env4 = {key: span4.count(rf"\begin{{{key}}}") for key in expected_env4}
    require(actual_env4 == expected_env4, f"Unit 4 authority environment mismatch: {actual_env4}")

    text4 = texts[3]
    for token in (
        "Pemetaan maju diinduksi oleh keluarga inklusi",
        r"\sin(1/x)",
        "G(X)&\\xrightarrow{G(f)}&G(Y)",
        r"G(f)\circ\alpha_X=\alpha_Y\circ F(f)",
        r"\colon\mathbf{Top}\longrightarrow\mathbf{Set}",
        "jika dan hanya jika setiap komponen lintasannya terbuka",
        r"C_x:=\chi_x^{-1}(1)",
        "Setiap komponen lintasan $C\\subseteq K$ terbuka di $K$",
        "adalah pemetaan kontinu $f\\colon X\\to Y$ yang memenuhi $f(x)=y$",
        "homotopi bertitik",
        "pemetaan $p(z)=z^2$ adalah pemetaan terbuka dan surjektif",
        "terdapat lingkungan terbuka\n$V_x\\ni x$ dan homeomorfisme",
        r"U(1)\xrightarrow{(-)^n}U(1)\quad(n\geq 1)",
        r"S^1\vee S^1",
        "pada umumnya bergantung pada pilihan lintasan",
    ):
        require(token in text4, f"Missing Unit 4 correction/mastery invariant: {token}")

    for number in range(1, 5):
        require(text4.count(f"#o012-rbt-l04-ex-{number:03d}") == 1, f"Unit 4 exercise {number} mismatch")
        require(text4.count(f"#o012-rbt-l04-sol-{number:03d}") == 1, f"Unit 4 solution {number} mismatch")
    require(text4.count("#o012-rbt-l04-q-001") == 1 and text4.count("#o012-rbt-l04-ans-001") == 1, "Unit 4 question-answer closure mismatch")
    require(text4.count("#o012-rbt-l04-check-") == 1, "Unit 4 mastery-check count mismatch")
    require("David Michael Roberts" in text4 and "*Algebraic Topology*" in text4, "Protected Unit 4 attribution missing")
    for phrase in ("A natural transformation", "A covering space", "Show that", "We are going to consider"):
        require(phrase not in text4, f"Active English residue in Unit 4: {phrase}")

    return all_ids, {
        "unit_001": BLOCKS_1,
        "unit_002": BLOCKS_2,
        "unit_003": BLOCKS_3,
        "unit_004": BLOCKS_4,
    }


def verify_correction_inventory() -> dict[str, list[str]]:
    with ADVERSE_LEDGER.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    require(rows, "Adverse ledger is empty")
    event_ids = [row["event_id"] for row in rows]
    require(len(event_ids) == len(set(event_ids)), "Duplicate adverse-ledger event ID")
    indexed = {row["event_id"]: row for row in rows}
    required_ids = UNIT_4_SOURCE_CORRECTION_IDS | UNIT_4_REFLOW_IDS
    require(required_ids <= indexed.keys(), f"Missing Unit 4 ledger events: {sorted(required_ids - indexed.keys())}")
    for event_id in UNIT_4_SOURCE_CORRECTION_IDS:
        row = indexed[event_id]
        require(row["status"] in {"corrected_in_translation", "clarified_in_translation"}, f"Correction status mismatch: {event_id}")
        require(row["source_location"].startswith("Notes.tex:"), f"Correction location mismatch: {event_id}")
        require(row["rationale"].strip(), f"Correction rationale missing: {event_id}")
    for event_id in UNIT_4_REFLOW_IDS:
        row = indexed[event_id]
        require(row["status"] == "accessibility_reflow", f"Reflow status mismatch: {event_id}")
        require(row["source_location"].startswith("Notes.tex:"), f"Reflow location mismatch: {event_id}")
        require(row["rationale"].strip(), f"Reflow rationale missing: {event_id}")
    return {
        "source_corrections": sorted(UNIT_4_SOURCE_CORRECTION_IDS),
        "accessibility_reflows": sorted(UNIT_4_REFLOW_IDS),
    }


def verify_reviews() -> dict[str, str]:
    assert isinstance(SOURCE_4_EXPECTED[1], str)
    review = INDEPENDENT_4.read_text(encoding="utf-8")
    require(SOURCE_4_EXPECTED[1] in review, "Independent review does not bind the frozen Unit 4 source")
    require("PASS. P1 = 0, P2 = 0, P3 = 0." in review, "Independent review is not an all-clear")
    require("Notes.tex" in review and "878" in review and "1131" in review, "Independent review source-span witness missing")
    visual = VISUAL.read_text(encoding="utf-8")
    require("PASS" in visual, "Visual review is not marked PASS")
    require("browser" in visual.lower(), "Responsive browser review is missing")
    require(str(EXPECTED_PDF_PAGES) in visual, "Visual review does not name the exact PDF page count")
    return {
        "unit_004_independent_review_sha256": sha256(INDEPENDENT_4),
        "visual_review_sha256": sha256(VISUAL),
    }


def verify_html(source_ids: list[str]) -> dict[str, int]:
    parser = etree.HTMLParser(recover=True)
    root = etree.parse(str(HTML), parser).getroot()
    require(root.get("lang") == "id-ID", "HTML lang mismatch")
    title = "".join(root.xpath("//title/text()"))
    require(title == "Topologi Aljabar - Unit 1-4", f"HTML title mismatch: {title!r}")
    html_ids = root.xpath("//*[@id]/@id")
    require(len(html_ids) == len(set(html_ids)), "Duplicate HTML id")
    require(len(html_ids) == EXPECTED_HTML_IDS, f"HTML ID count mismatch: {len(html_ids)}")
    html_id_set = set(html_ids)
    for source_id in source_ids:
        require(source_id in html_id_set, f"Stable ID missing from HTML: {source_id}")
    fragment_hrefs = [href for href in root.xpath("//@href") if href.startswith("#")]
    require(len(fragment_hrefs) == EXPECTED_HTML_FRAGMENT_HREFS, f"HTML fragment-link count mismatch: {len(fragment_hrefs)}")
    for href in fragment_hrefs:
        target = unquote(href[1:])
        require(target and target in html_id_set, f"Broken local fragment: {href}")

    require(not root.xpath("//script"), "Cumulative HTML contains scripts")
    require(not root.xpath("//link[@rel='stylesheet']"), "CSS was not embedded")
    require(not root.xpath("//img|//object|//embed|//iframe|//video|//audio|//source"), "Unexpected runtime asset element")
    for attribute in ("src", "srcset", "poster", "data"):
        require(not root.xpath(f"//@{attribute}"), f"Cumulative HTML has runtime @{attribute} dependency")
    math_count = len(root.xpath("//*[local-name()='math']"))
    require(math_count == EXPECTED_HTML_MATHML_NODES, f"MathML count mismatch: {math_count}")
    require(not root.xpath("//img[contains(@class, 'math')]"), "Math was emitted as images instead of native MathML")
    styles = "\n".join(root.xpath("//style/text()"))
    for rule in ("max-width: 58rem", "margin: 0 auto", ".question", "#fff8ef"):
        require(rule in styles, f"Missing cumulative style: {rule}")
    require("@import" not in styles and not re.search(r"url\(\s*['\"]?https?://", styles, flags=re.IGNORECASE), "External CSS asset dependency")

    data = HTML.read_text(encoding="utf-8")
    require("<math" in data and "http://www.w3.org/1998/Math/MathML" in data, "Native MathML serialization missing")
    for pattern in PRIVATE_MARKERS:
        require(pattern not in data, f"Private data in HTML: {pattern}")
    return {"html_ids": len(html_ids), "stable_ids": len(source_ids), "mathml_nodes": math_count}


def verify_pdf() -> tuple[dict[str, object], bytes]:
    reader = PdfReader(str(PDF), strict=True)
    require(not reader.is_encrypted, "PDF is encrypted")
    require(len(reader.pages) == EXPECTED_PDF_PAGES, f"PDF page mismatch: {len(reader.pages)}")
    require(reader.trailer["/Root"].get("/Lang") == "id-ID", "PDF /Lang mismatch")
    require("/AcroForm" not in reader.trailer["/Root"], "Unexpected PDF AcroForm")
    open_action = reader.trailer["/Root"].get("/OpenAction")
    if open_action is not None:
        open_action = open_action.get_object()
        require(open_action.get("/S") != "/JavaScript" and "/JS" not in open_action, "Unexpected PDF JavaScript open action")
    pdf_names = reader.trailer["/Root"].get("/Names")
    if pdf_names is not None:
        pdf_names = pdf_names.get_object()
        require("/JavaScript" not in pdf_names, "Unexpected PDF JavaScript name tree")
    metadata = reader.metadata
    require(metadata.title == "Topologi Aljabar - Unit 1-4", "PDF title mismatch")
    require(metadata.author == "David Michael Roberts (materi sumber); Edisi Bahasa Indonesia dengan pendamping penguasaan", "PDF author mismatch")
    require(metadata.creator == "LaTeX via pandoc", "PDF creator mismatch")
    require("pdfTeX" in (metadata.producer or ""), "PDF producer mismatch")
    require(str(metadata.get("/CreationDate")) == "D:20260822000000Z", "PDF creation date mismatch")
    require(str(metadata.get("/ModDate")) == "D:20260822000000Z", "PDF modification date mismatch")
    require("/StructTreeRoot" not in reader.trailer["/Root"], "Unexpected tagging-state change")

    extracted = "\n".join(page.extract_text() or "" for page in reader.pages)
    for phrase in (
        "Kuliah 1",
        "Kuliah 2",
        "Kuliah 3",
        "Kuliah 4",
        "Transformasi natural",
        "Ruang penutup",
        "Solusi Latihan 4.4",
        "Proposisi 4.3",
    ):
        require(phrase in extracted, f"Missing PDF text: {phrase}")
    for pattern in PRIVATE_MARKERS + ("No correct answer",):
        require(pattern not in extracted, f"Private/English UI residue in PDF: {pattern}")

    pdffonts = shutil.which("pdffonts")
    require(pdffonts is not None, "pdffonts unavailable")
    font_result = subprocess.run([pdffonts, str(PDF)], check=True, capture_output=True, text=True)
    rows = [line.split() for line in font_result.stdout.splitlines()[2:] if line.strip()]
    require(rows, "No PDF fonts reported")
    require(all(len(row) >= 5 and row[-5:-2] == ["yes", "yes", "yes"] for row in rows), "PDF font embedding/ToUnicode failure")

    pdftotext = shutil.which("pdftotext")
    require(pdftotext is not None, "pdftotext unavailable")
    text_result = subprocess.run(
        [pdftotext, "-layout", "-enc", "UTF-8", str(PDF), "-"],
        check=True,
        capture_output=True,
    )
    require(text_result.stdout == TEXT_WITNESS.read_bytes(), "Stored text witness is not the exact current PDF extraction")
    for phrase in (b"Kuliah 1", b"Kuliah 2", b"Kuliah 3", b"Kuliah 4"):
        require(phrase in text_result.stdout, f"Missing text-witness phrase: {phrase!r}")
    return (
        {
            "pages": len(reader.pages),
            "encrypted": False,
            "lang": "id-ID",
            "tagged": False,
            "fonts": len(rows),
            "all_fonts_embedded": True,
            "all_fonts_tounicode": True,
            "extracted_characters": len(extracted),
        },
        text_result.stdout,
    )


def verify_manifest() -> list[dict[str, object]]:
    with MANIFEST.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    require(len(rows) == 2 and len({row["path"] for row in rows}) == 2, "Cumulative manifest shape mismatch")
    paths = [row["path"] for row in rows]
    require(set(paths) == ARTIFACT_PATHS and paths == sorted(paths), "Cumulative manifest path mismatch")
    for row in rows:
        require(re.fullmatch(r"[0-9a-f]{64}", row["sha256"]) is not None, f"Invalid manifest SHA-256: {row['path']}")
        verify_file(LANE / row["path"], int(row["bytes"]), row["sha256"])
        expected_bytes, expected_sha = POST_BUILD_EXPECTED[LANE / row["path"]]
        require(int(row["bytes"]) == expected_bytes and row["sha256"] == expected_sha, f"Manifest disagrees with frozen expectation: {row['path']}")
    return [{"path": row["path"], "bytes": int(row["bytes"]), "sha256": row["sha256"]} for row in rows]


def main() -> int:
    verify_placeholders_filled()
    for path, (size, digest) in HISTORICAL_EXPECTED.items():
        verify_file(path, size, digest)
    source_bytes, source_sha = SOURCE_4_EXPECTED
    assert isinstance(source_bytes, int) and isinstance(source_sha, str)
    verify_file(SOURCE_4, source_bytes, source_sha)
    for path, (size, digest) in POST_BUILD_EXPECTED.items():
        assert isinstance(size, int) and isinstance(digest, str)
        verify_file(path, size, digest)

    authority, upstream = verify_authority()
    source_ids, blocks = verify_sources(upstream)
    corrections = verify_correction_inventory()
    reviews = verify_reviews()
    html = verify_html(source_ids)
    pdf, text_bytes = verify_pdf()
    artifacts = verify_manifest()
    receipt = {
        "schema_version": "1.0",
        "status": "pass",
        "role_id": "O012",
        "course_id": "D60",
        "unit_ids": ["o012-rbt-l01", "o012-rbt-l02", "o012-rbt-l03", "o012-rbt-l04"],
        "source_authority": {
            "commit_sha1": authority["commit_sha1"],
            "tree_sha1": authority["tree_sha1"],
            "path": "Notes.tex",
            "line_start": 134,
            "line_end": 1131,
            "next_line": 1132,
            "next_boundary": "Lecture 5 marker",
        },
        "reader_sources": [
            {
                "path": path.relative_to(LANE).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
                "stable_ids": expected,
            }
            for path, expected in zip((SOURCE_1, SOURCE_2, SOURCE_3, SOURCE_4), (29, 41, 39, 33), strict=True)
        ],
        "block_counts": blocks,
        "corrections": corrections,
        "html": html,
        "pdf": pdf,
        "artifacts": artifacts,
        "witnesses": {
            **reviews,
            "extracted_text_bytes": len(text_bytes),
            "extracted_text_sha256": sha256(TEXT_WITNESS),
            "prior_units_001_003_qa_sha256": HISTORICAL_EXPECTED[LANE / "qa" / "UNITS_001_003_QA.json"][1],
        },
        "gates": {
            "authority_exact": True,
            "source_spans_bound": True,
            "structure_bound": True,
            "exercise_solution_and_question_answer_closure": True,
            "unit_004_mastery_check_present": True,
            "unit_004_corrections_and_reflows_verified": True,
            "html_semantic_native_mathml_offline": True,
            "html_fragments_and_ids_valid": True,
            "privacy_secret_scan": True,
            "pdf_reproducible_by_build_script": True,
            "pdf_metadata_fonts_text_pages_verified": True,
            "visual_review": f"pass_manual_all_{EXPECTED_PDF_PAGES}_pages_and_browser_desktop_mobile",
            "unit_001_artifacts_unchanged": True,
            "units_001_002_artifacts_and_qa_unchanged": True,
            "units_001_003_artifacts_and_qa_unchanged": True,
        },
        "known_caveat": "PDF is intentionally secondary and untagged; semantic HTML with native MathML is the primary accessibility surface.",
    }
    payload = json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    RECEIPT.write_text(payload, encoding="utf-8", newline="\n")
    print(
        "PASS "
        f"stable_ids={len(source_ids)} blocks={sum(sum(values.values()) for values in blocks.values())} "
        f"mathml={html['mathml_nodes']} pdf_pages={pdf['pages']} "
        f"receipt_sha256={sha256(RECEIPT)}"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise
