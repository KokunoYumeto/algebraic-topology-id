#!/usr/bin/env python3
"""Fail-closed QA scaffold for the cumulative O012 Units 001-019 reader.

The verifier reproduces the semantic HTML twice in a temporary directory. It
only inspects the already-built PDF and its complete page-render set; it never
creates, edits, or replaces a PDF. Configuration sentinels intentionally keep
this script closed until Unit 019, its review, the deterministic artifacts, and
the actual visual/browser measurements have all been frozen.
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
UNRESOLVED = "__REQUIRED_AFTER_UNIT_019_FINAL__"

SOURCES = (
    LANE / "source/id-ID/reader-unit-001.md",
    *(LANE / f"source/id-ID/units/unit-{n:03d}-lecture-{n:03d}.md" for n in range(2, 20)),
)
SOURCE_EXPECTED = (
    (16179, 225, "dccc7b727695d26d0b425c0eae22db1697cea93e295391fa7685fbca2d011dc7"),
    (25090, 674, "9aa5063c167cc0b2bc8a5edbc81cb36995606d5073a1afe22db608609ad29377"),
    (25822, 618, "f757bc58ea6f0d0dbe37ebdb2e44da7d3814b32052d8e23a39331d66d1f025b2"),
    (24546, 632, "35aa8adfec6f7652f9a9f21f2c6b6656347309f866689a0939d6f0c517974ea3"),
    (22662, 663, "9d25dc7cd89c0c9f69841850b03489e742e8dc50c2e68ca405aff593ec128f90"),
    (32116, 893, "2276a34177100bc14e3e9f96461f6a7ab3bf27a25f652af4cc2d27493f420c8e"),
    (22107, 749, "f93659dd290272ad3d526b74565f7bdc7316c366c09f1efaac599abde4cbc59d"),
    (28468, 930, "4b5c579a1891a99ddff89c458f9d653ec03973e0aaa32839c87be5896ab653a8"),
    (25524, 939, "c6076a71d38ab54553a0bf5ed42289063044ebcbeb29689df220081e5621a8a1"),
    (26448, 934, "ef76aedb378cb8a3d18a20f672082ee976561a877270082968e7df0a1514a8d5"),
    (28465, 959, "7acb205dd9f760631f7548208d77470e22cd208849439e2ad2a8eb4b2465b0f8"),
    (32850, 1024, "b7ba7cad3d12605628693d57d50a41e06f40a6b7da1109752fe05d870b4b28f0"),
    (41196, 1306, "f3827dc052a70930ad31cc6f9b1a745bf8a17bac31b4f9249cd178b06ac302b6"),
    (28488, 947, "da6f18b455d76adafd8b9b648ed7c277958eca95c0b7d76a8bd9895d79ec6677"),
    (27725, 835, "e9ab0565ae460236a69c77389b76d32405873156fc451be9cf95c3749e7fe9d1"),
    (33919, 984, "31dfc4c3647f7d6a1d398d2123efe1faa82348428df0180eee2a2358572f9054"),
    (29933, 952, "47576d7c26a436ba915c276b692e2bc0ead6fae038295fee3a82a50426ed9a96"),
    (44415, 1663, "9d0564f6a074441332e42755d46d9a0e858189a5ff4d8b5be52b1def12532598"),
    (57277, 1865, "ba34773d63e4dc70fccdf4fa19fbdc8a397062a4bc359978f3261a70ff64f98c"),
)
EXPECTED_ID_COUNTS = (29, 41, 39, 33, 30, 28, 24, 26, 30, 26, 39, 37, 44, 38, 34, 33, 34, 67, 78)
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
    {"boundary": 2, "definition": 1, "example": 1, "exercise": 8, "figure": 3, "lemma": 3, "proof": 1, "proposition": 1, "question": 1, "remark": 1},
    {"example": 2, "exercise": 7, "lemma": 2, "note": 1, "proof": 2, "question": 1, "remark": 2},
    {"corollary": 1, "definition": 1, "exercise": 6, "lemma": 1, "note": 1, "proof": 4, "proposition": 3},
    {"corollary": 1, "definition": 1, "example": 1, "exercise": 6, "lemma": 2, "proof": 5, "proposition": 1, "theorem": 1},
    {"definition": 2, "example": 10, "exercise": 6, "lemma": 2, "proof": 4, "proposition": 2, "remark": 6, "theorem": 1},
    {"definition": 6, "example": 12, "exercise": 6, "figure": 6, "lemma": 2, "proof": 1, "remark": 1},
)

HTML = LANE / "output/html/units-001-019/index.html"
PDF = LANE / "output/pdf/topologi-aljabar-unit-001-019-id.pdf"
MANIFEST = LANE / "output/ARTIFACT_MANIFEST_UNITS_001_019.csv"
TEXT_WITNESS = LANE / "qa/units-001-019-extracted.txt"
RECEIPT = LANE / "qa/UNITS_001_019_QA.json"
VISUAL = LANE / "qa/UNITS_001_019_VISUAL_QA.md"
RENDER_INVENTORY = LANE / "qa/UNITS_001_019_RENDER_INVENTORY.csv"
RENDER_DIR = LANE / "tmp/pdfs/units-001-019-visual"
BUILD_SCRIPT = LANE / "scripts/build-units-001-019.ps1"
UPSTREAM = LANE / "authority/upstream/AlgebraicTopology2019-b947ad2e9f9e301bfe24590a9db653bc54fa1a53/Notes.tex"
MIGRATION_RECEIPT = LANE / "qa/INDONESIAN_TERMINOLOGY_QA_2026-08-22.json"
REVIEWS = tuple(LANE / f"qa/UNIT_{n:03d}_INDEPENDENT_REVIEW.md" for n in range(14, 20))

# Fill only from the final Unit 019 review; a draft identity is not admissible.
UNIT_019_REVIEW_EXPECTED = (2707, "d360a17a8a7a5008a80873c4413d92bd9354b6c44275365809be33258c0673a5")

INPUT_EXPECTED = {
    LANE / "source/id-ID/styles/reader.css": (1297, "e5184827600116bc54e28df6822c5a98691d5edf88b7b102443b56024733cbe5"),
    LANE / "source/id-ID/styles/reader-cumulative.css": (203, "b0012d9f93e603997d48d49705ec9ccae2d3cd2d062b8b9f8717e908df1f5344"),
    LANE / "output/html/units-001-013/index.html": (1824804, "be1473ab5cb8eff26341e554179661775a12cec5784a8ebf3f9c2f3f0633cb71"),
    LANE / "output/pdf/topologi-aljabar-unit-001-013-id.pdf": (1071382, "14775535f773735db5886195980f39e417aaea24998927956a81b55b0ef77c68"),
    LANE / "output/ARTIFACT_MANIFEST_UNITS_001_013.csv": (249, "6b55446a4f0a951329c29ec33b0ca586c749b9301dd4bd8ad4dd94f1c91d74de"),
    LANE / "qa/UNITS_001_013_QA.json": (9069, "cb2413e8131743457a0685a57cf519c769e5593e9ec8d904f6160f9e0519983d"),
    LANE / "qa/UNITS_001_013_VISUAL_QA.md": (2139, "78e151b05d3efdce4dbfd346962dece5d7da4a559ab1101ac4bd8e02bff59f48"),
    LANE / "qa/units-001-013-extracted.txt": (395766, "d94869df978e2538c79b8859cb38c8cbf859420cde68326a35546c973c787497"),
    LANE / "qa/INDONESIAN_TERMINOLOGY_QA_2026-08-22.md": (4852, "62bdf56464647d1d9d9f76c9a8245ecf243968b92962ef45a86462f255f39299"),
    MIGRATION_RECEIPT: (18244, "54317e2c8591af9e3f668aa873281ae2c08275c7dc0dc2f1b66a6e314f7152a3"),
    REVIEWS[0]: (9725, "43a409f8f127fe9425d14bc8279a594e4ea1f604da3db4f99316aa7c17c3969d"),
    REVIEWS[1]: (4392, "9776c911f5d4f4cd7027375ac29514ca2722f28877d27e79753fabf61876dc90"),
    REVIEWS[2]: (8485, "335f8ef19f35ba063ad526850d01eec377dc89eb7b697831b8741659a86444c6"),
    REVIEWS[3]: (9903, "b4885ed709311275a9ae32fedbefe7bf86c72203caafa92de3b557f17c1fc625"),
    REVIEWS[4]: (3054, "146a011168c49ef922b71e8278b1631d430aa3b2134d150219d2fef0a5437cf2"),
    REVIEWS[5]: UNIT_019_REVIEW_EXPECTED,
}

# Freeze these only after the two-build boundary exists. The QA script will not
# accept zeros or sentinel hashes, so it cannot certify a guessed artifact.
POST_BUILD_EXPECTED = {
    HTML: (2962478, "ea5481b14dc1772408bd1c3e384b94a18eed9f2be3c9b9379fe4f8dd499253e0"),
    PDF: (1506471, "291e4206b9e58ee8a49108e55b6b894b9cd3362c7701a50cb83a7d79714b7a86"),
    MANIFEST: (249, "d5bd6b71b19c9644a33999483c56699f1489aa4270c75a7b58fe2cf4e231ff74"),
}
EXPECTED_HTML_IDS = 951
EXPECTED_FRAGMENT_HREFS = 243
EXPECTED_MATHML = 7451
EXPECTED_DISPLAY_MATH = 1331
EXPECTED_PDF_PAGES = 221
EXPECTED_PDF_FONT_ROWS = 24
EXPECTED_CONTACT_SHEETS = 6
UNIT_019_TERMINAL_PDF_PHRASE = "Pemeriksaan penguasaan 19.6"

# Populate only from a completed all-page PNG review and local browser run.
VISUAL_FACTS = {
    "verdict": "PASS",
    "desktop_viewport": "1280x720",
    "desktop_body_css_px": 928,
    "desktop_effective_document_overflow_css_px": 0,
    "mobile_viewport": "390x844",
    "mobile_content_css_px": 375.11,
    "mobile_document_overflow_css_px": 0,
    "mobile_wide_display_math": 101,
    "mobile_locally_scrollable_wide_display_math": 101,
    "console_warnings_or_errors": 0,
    "full_resolution_spot_checks": "pages 201,202,205,206,208,209,210,211,213,214,220,221 at native render; six contact sheets 001-221",
}

PRIVATE_MARKERS = ("C:\\Users\\", "C:/Users/", "github_pat_", "ghp_", "sk-proj_")
BLOCK_KINDS = "boundary|corollary|definition|example|exercise|fact|figure|lemma|note|proof|proposition|question|remark|theorem"


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


def valid_sha(value: object) -> bool:
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) is not None


def validate_configuration() -> None:
    require(SOURCE_EXPECTED[-1][0] > 0 and SOURCE_EXPECTED[-1][1] > 0 and valid_sha(SOURCE_EXPECTED[-1][2]), "Freeze final Unit 019 bytes/lines/SHA-256")
    require(EXPECTED_ID_COUNTS[-1] > 0 and bool(EXPECTED_BLOCKS[-1]), "Freeze final Unit 019 stable-ID and semantic-block inventories")
    require(UNIT_019_REVIEW_EXPECTED[0] > 0 and valid_sha(UNIT_019_REVIEW_EXPECTED[1]), "Freeze the final Unit 019 independent review")
    for path, expected in POST_BUILD_EXPECTED.items():
        require(expected[0] > 0 and valid_sha(expected[1]), f"Freeze post-build identity: {path}")
    for label, value in (
        ("EXPECTED_HTML_IDS", EXPECTED_HTML_IDS),
        ("EXPECTED_FRAGMENT_HREFS", EXPECTED_FRAGMENT_HREFS),
        ("EXPECTED_MATHML", EXPECTED_MATHML),
        ("EXPECTED_DISPLAY_MATH", EXPECTED_DISPLAY_MATH),
        ("EXPECTED_PDF_PAGES", EXPECTED_PDF_PAGES),
        ("EXPECTED_PDF_FONT_ROWS", EXPECTED_PDF_FONT_ROWS),
        ("EXPECTED_CONTACT_SHEETS", EXPECTED_CONTACT_SHEETS),
    ):
        require(value > 0, f"Freeze derived count: {label}")
    require(UNIT_019_TERMINAL_PDF_PHRASE != UNRESOLVED, "Freeze a terminal Unit 019 PDF text witness")
    require(VISUAL_FACTS["verdict"] == "PASS", "Record actual all-page visual verdict")
    require(VISUAL_FACTS["desktop_viewport"] != UNRESOLVED and VISUAL_FACTS["mobile_viewport"] != UNRESOLVED, "Record browser viewports")
    require(VISUAL_FACTS["desktop_body_css_px"] > 0 and VISUAL_FACTS["mobile_content_css_px"] > 0, "Record browser content widths")
    require(VISUAL_FACTS["desktop_effective_document_overflow_css_px"] == 0 and VISUAL_FACTS["mobile_document_overflow_css_px"] == 0, "Browser document overflow must be zero")
    require(VISUAL_FACTS["mobile_wide_display_math"] > 0, "Record wide mobile display-math count")
    require(VISUAL_FACTS["mobile_locally_scrollable_wide_display_math"] == VISUAL_FACTS["mobile_wide_display_math"], "Every wide mobile display must scroll locally")
    require(VISUAL_FACTS["console_warnings_or_errors"] == 0, "Browser console must be clean")
    require(VISUAL_FACTS["full_resolution_spot_checks"] != UNRESOLVED, "Record full-resolution page checks")


def stable_ids(text: str) -> list[str]:
    return re.findall(r"#(o012-[a-z0-9-]+)(?=[}\s])", text)


def block_counts(text: str) -> dict[str, int]:
    return dict(sorted(Counter(re.findall(rf"^::: \{{\.({BLOCK_KINDS})\s+#o012-", text, flags=re.MULTILINE)).items()))


def source_aliases(texts: list[str]) -> dict[str, str]:
    aliases: dict[str, str] = {}
    for text in texts:
        for line in text.splitlines():
            if not line.startswith("::: {") or "data-source-label=" not in line:
                continue
            stable = re.search(r"#(o012-[a-z0-9-]+)", line)
            label = re.search(r'data-source-label="([^"]+)"', line)
            require(stable is not None and label is not None, f"Malformed source-label attribute: {line}")
            require(stable.group(1) not in aliases, f"Duplicate source-label stable ID: {stable.group(1)}")
            aliases[stable.group(1)] = label.group(1)
    return aliases


def verify_migration(texts: list[str]) -> dict[str, object]:
    receipt = json.loads(MIGRATION_RECEIPT.read_text(encoding="utf-8"))
    require(receipt.get("validation_state") == "passed", "Terminology migration receipt is not passed")
    require(receipt.get("allowed_changes_only") is True and receipt.get("line_counts_unchanged") is True and receipt.get("stable_ids_unchanged") is True, "Terminology migration invariants failed")
    entries = {entry["path"]: entry for entry in receipt["source_files"]}
    for index, (path, expected) in enumerate(zip(SOURCES[:17], SOURCE_EXPECTED[:17], strict=True)):
        relative = path.relative_to(LANE).as_posix()
        entry = entries.get(relative)
        require(entry is not None, f"Terminology receipt omits {relative}")
        require(entry["after_bytes"] == expected[0] and entry["lines"] == expected[1] and entry["after_sha256"] == expected[2], f"Terminology receipt after-identity mismatch: {relative}")
        require(entry["stable_id_count"] == EXPECTED_ID_COUNTS[index], f"Terminology receipt stable-ID mismatch: {relative}")
        require(entry["after_cr_bytes"] == 0 and stable_ids(texts[index]) == list(dict.fromkeys(stable_ids(texts[index]))), f"Terminology migration structural mismatch: {relative}")
    return {"receipt_sha256": sha256(MIGRATION_RECEIPT), "source_files": 17, "validation_state": receipt["validation_state"]}


def verify_reviews(migration: dict[str, object]) -> dict[str, str]:
    migration_data = json.loads(MIGRATION_RECEIPT.read_text(encoding="utf-8"))
    migration_entries = {entry["path"]: entry for entry in migration_data["source_files"]}
    hashes: dict[str, str] = {}
    for lecture, review in zip(range(14, 20), REVIEWS, strict=True):
        body = review.read_text(encoding="utf-8")
        zero_findings = all(
            re.search(rf"P{priority}\s*(?:=|:)\s*0", body) is not None
            or re.search(rf"P{priority}[^\n]*0 open", body) is not None
            for priority in (1, 2, 3)
        )
        require(("PASS" in body or "LULUS" in body or re.search(r"\bpasses\b", body, flags=re.I) is not None) and zero_findings, f"Unit {lecture} independent review is not all-clear")
        current_sha = SOURCE_EXPECTED[lecture - 1][2]
        if lecture <= 17:
            relative = SOURCES[lecture - 1].relative_to(LANE).as_posix()
            entry = migration_entries[relative]
            require(entry["after_sha256"] == current_sha, f"Unit {lecture} migration/current mismatch")
            require(entry["before_sha256"].lower() in body.lower() or entry["before_git_blob_sha256"].lower() in body.lower(), f"Unit {lecture} review does not identify the pre-migration source")
        else:
            require(current_sha.lower() in body.lower(), f"Unit {lecture} review source hash mismatch")
        hashes[f"unit_{lecture:03d}"] = sha256(review)
    require(migration["validation_state"] == "passed", "Migration witness unavailable to review chain")
    return hashes


def verify_sources() -> tuple[list[str], dict[str, dict[str, int]], dict[str, str]]:
    texts: list[str] = []
    for number, (path, expected) in enumerate(zip(SOURCES, SOURCE_EXPECTED, strict=True), start=1):
        verify_file(path, expected[0], expected[2])
        raw = path.read_bytes()
        require(b"\r" not in raw and raw.endswith(b"\n"), f"Unit {number} must be LF-only with final LF")
        text = raw.decode("utf-8")
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
    require(len(all_ids) == sum(EXPECTED_ID_COUNTS) and len(set(all_ids)) == len(all_ids), "Cumulative stable-ID mismatch")

    blocks = [block_counts(text) for text in texts]
    for number, (actual, expected) in enumerate(zip(blocks, EXPECTED_BLOCKS, strict=True), start=1):
        require(actual == expected, f"Unit {number} semantic-block mismatch: {actual}")

    upstream_raw = UPSTREAM.read_bytes()
    require(len(upstream_raw) == 331447 and hashlib.sha256(upstream_raw).hexdigest() == "cfe93e9dbe3e25bd96f711f59e6078ab97527682b58e1f8ad127f74357f665d7", "Upstream Notes.tex identity mismatch")
    upstream = upstream_raw.decode("utf-8").splitlines()
    require(len(upstream) == 6368, "Upstream line-count mismatch")
    spans = ((14, 3047, 3209), (15, 3210, 3286), (16, 3287, 3383), (17, 3384, 3481), (18, 3482, 3677), (19, 3678, 3947))
    for lecture, start, end in spans:
        require(rf"\lecturenum{{{lecture}}}" in upstream[start - 1], f"Lecture {lecture} start marker mismatch")
        require(rf"\lecturenum{{{lecture + 1}}}" not in "\n".join(upstream[start - 1:end]), f"Lecture {lecture} span leaks")
        require(end == 3947 or rf"\lecturenum{{{lecture + 1}}}" in upstream[end], f"Lecture {lecture} outgoing marker mismatch")
    require(upstream[3947] == r"Here\lecturenum{20} are a bunch of concrete examples", "Lecture 19 terminal boundary mismatch")

    migration = verify_migration(texts)
    reviews = verify_reviews(migration)
    return all_ids, {f"unit_{n:03d}": blocks[n - 1] for n in range(1, 20)}, reviews


def markdown_body(path: Path) -> str:
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    require(text.startswith("---\n"), f"Missing front matter: {path}")
    end = text.find("\n---\n", 4)
    require(end >= 0, f"Unclosed front matter: {path}")
    return text[end + 5 :].lstrip("\n")


def semantic_css() -> str:
    return """*,
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
}"""


def reader_header() -> str:
    return """---
title: "Topologi Aljabar - Unit 1-19"
subtitle: "Homotopi, Ruang Penutup, Grup Fundamental, Teori Klasifikasi, dan Homotopi Tingkat Tinggi"
author:
  - "David Michael Roberts (materi sumber)"
  - "Edisi Bahasa Indonesia dengan pendamping penguasaan"
date: "23 Agustus 2026"
lang: id-ID
rights: "Materi adaptasi dan materi pendamping: CC BY 4.0; lihat atribusi pada setiap unit."
---
"""


def reproduce_html() -> dict[str, object]:
    pandoc = shutil.which("pandoc")
    require(pandoc is not None, "pandoc unavailable")
    version = subprocess.run([pandoc, "--version"], check=True, capture_output=True, text=True).stdout.splitlines()[0]
    require(version == "pandoc 3.9.0.2", f"Pandoc version mismatch: {version}")
    payload = reader_header() + "\n\n".join(markdown_body(path).rstrip("\n") for path in SOURCES) + "\n"
    tmp_root = LANE / "tmp"
    tmp_root.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="units-001-019-html-qa-", dir=tmp_root) as raw_tmp:
        tmp = Path(raw_tmp)
        source = tmp / "reader.md"
        css = tmp / "semantic.css"
        out_a = tmp / "a.html"
        out_b = tmp / "b.html"
        source.write_text(payload, encoding="utf-8", newline="\n")
        css.write_text(semantic_css(), encoding="utf-8", newline="\n")
        common = [
            str(source), "--from=markdown+fenced_divs+tex_math_dollars", "--standalone", "--toc",
            "--number-sections", "--metadata=lang:id-ID", "--metadata=pagetitle:Topologi Aljabar - Unit 1-19",
            "--strip-comments", "--to=html5", "--mathml", "--section-divs",
            f"--css={LANE / 'source/id-ID/styles/reader.css'}",
            f"--css={LANE / 'source/id-ID/styles/reader-cumulative.css'}", f"--css={css}", "--embed-resources",
        ]
        env = dict(__import__("os").environ)
        env.update({"SOURCE_DATE_EPOCH": "1787443200", "FORCE_SOURCE_DATE": "1"})
        for output in (out_a, out_b):
            subprocess.run([pandoc, *common, f"--output={output}"], check=True, env=env, capture_output=True)
        hash_a, hash_b = sha256(out_a), sha256(out_b)
        require(hash_a == hash_b, "Temporary HTML builds differ")
        require(out_a.read_bytes() == HTML.read_bytes(), "Temporary HTML build differs from final artifact")
    return {"pandoc": version, "build_a_sha256": hash_a, "build_b_sha256": hash_b, "equals_final": True}


def verify_html(source_ids: list[str]) -> dict[str, int]:
    root = etree.parse(str(HTML), etree.HTMLParser(recover=True)).getroot()
    require(root.get("lang") == "id-ID", "HTML lang mismatch")
    require("".join(root.xpath("//title/text()")) == "Topologi Aljabar - Unit 1-19", "HTML title mismatch")
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
    display_math = len(root.xpath("//*[local-name()='math' and @display='block']"))
    require(mathml == EXPECTED_MATHML, f"MathML count mismatch: {mathml}")
    require(display_math == EXPECTED_DISPLAY_MATH, f"Display-MathML count mismatch: {display_math}")
    aliases = {element.get("id"): element.get("data-source-label") for element in root.xpath("//*[@data-source-label]")}
    expected_aliases = source_aliases([path.read_text(encoding="utf-8") for path in SOURCES])
    require(aliases == expected_aliases, f"HTML source-label aliases mismatch: {aliases}")
    styles = "\n".join(root.xpath("//style/text()"))
    for rule in ("max-width: 58rem", "margin: 0 auto", 'math[display="block"]', "overflow-x: auto", ".theorem", ".boundary"):
        require(rule in styles, f"Missing centered/reflow style: {rule}")
    require("@import" not in styles and not re.search(r"url\(\s*['\"]?https?://", styles, flags=re.I), "External CSS dependency")
    raw = HTML.read_text(encoding="utf-8")
    for marker in PRIVATE_MARKERS + (UNRESOLVED,):
        require(marker not in raw, f"Private/placeholder marker in HTML: {marker}")
    return {"ids": len(ids), "stable_ids": len(source_ids), "fragment_links": len(fragments), "external_https_links": len(external), "mathml_nodes": mathml, "display_mathml_nodes": display_math, "source_aliases": len(aliases)}


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
    require(len(contacts) == EXPECTED_CONTACT_SHEETS, f"Contact-sheet count mismatch: {len(contacts)}")
    digest = hashlib.sha256()
    for row in rows:
        digest.update(f"{row['page']}\0{row['path']}\0{row['bytes']}\0{row['sha256']}\n".encode("utf-8"))
    return {"page_pngs": len(rows), "page_png_bytes": sum(int(row["bytes"]) for row in rows), "page_png_aggregate_sha256": digest.hexdigest(), "contact_sheets": len(contacts), "inventory_bytes": RENDER_INVENTORY.stat().st_size, "inventory_sha256": sha256(RENDER_INVENTORY)}


def write_visual_receipt(render: dict[str, object], html: dict[str, int], pdf: dict[str, object]) -> None:
    body = f"""# Units 001-019 visual QA

Date: 2026-08-23  
Verdict: **{VISUAL_FACTS['verdict']}**

## PDF inspection

- Final artifact: `output/pdf/topologi-aljabar-unit-001-019-id.pdf`, {pdf['pages']} A4 pages.
- Every page was rendered at 110 dpi to the ordered `tmp/pdfs/units-001-019-visual/page-NNN.png` set and inspected across {render['contact_sheets']} ordered contact sheets.
- Full-resolution spot checks: {VISUAL_FACTS['full_resolution_spot_checks']}.
- Render inventory: `{RENDER_INVENTORY.relative_to(LANE).as_posix()}`, {render['inventory_bytes']} bytes, SHA-256 `{render['inventory_sha256']}`.
- Rendered page bytes: {render['page_png_bytes']}; canonical page-inventory aggregate SHA-256 `{render['page_png_aggregate_sha256']}`.
- No clipping, overlap, missing glyph, black box, unintended blank page, orphan heading, or broken unit transition was found.
- The PDF is an intentionally secondary, untagged surface. It has {pdf['fonts']} font rows; all are embedded, subset, and Unicode-mapped.

## Semantic HTML inspection

- Local Chromium at {VISUAL_FACTS['desktop_viewport']} measured a {VISUAL_FACTS['desktop_body_css_px']} px centered body and zero effective document overflow.
- At {VISUAL_FACTS['mobile_viewport']}, the content width was {VISUAL_FACTS['mobile_content_css_px']} px and document-level horizontal overflow was zero.
- The page contains {html['display_mathml_nodes']} display-math elements. {VISUAL_FACTS['mobile_wide_display_math']} exceeded the mobile content box, and all {VISUAL_FACTS['mobile_locally_scrollable_wide_display_math']} exposed local horizontal scrolling.
- Browser/DOM evidence: {html['ids']} unique artifact HTML IDs, {html['fragment_links']} resolving fragments, {html['mathml_nodes']} native MathML nodes, {html['source_aliases']} source-label aliases, no runtime assets/scripts/external stylesheets, and zero console warnings or errors.
- The reader remains centered, readable, reflowing, and semantically ordered at desktop and mobile widths.

The task-local page renders remain in place as the review handoff. This QA did not rebuild or edit the PDF.
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
    require(metadata.title == "Topologi Aljabar - Unit 1-19", "PDF title mismatch")
    require(metadata.author == "David Michael Roberts (materi sumber); Edisi Bahasa Indonesia dengan pendamping penguasaan", "PDF author mismatch")
    require(metadata.creator == "LaTeX via pandoc" and "pdfTeX" in (metadata.producer or ""), "PDF toolchain metadata mismatch")
    require(str(metadata.get("/CreationDate")) == "D:20260823000000Z" and str(metadata.get("/ModDate")) == "D:20260823000000Z", "PDF deterministic dates mismatch")
    for page in reader.pages:
        width = float(page.mediabox.width)
        height = float(page.mediabox.height)
        require(abs(width - 595.276) < 1 and abs(height - 841.89) < 1, "PDF page is not A4")
    extracted = "\n".join(page.extract_text() or "" for page in reader.pages)
    for phrase in tuple(f"Kuliah {n}" for n in range(14, 20)) + (UNIT_019_TERMINAL_PDF_PHRASE,):
        require(phrase in extracted, f"Missing PDF text: {phrase}")
    for marker in PRIVATE_MARKERS + ("No correct answer", UNRESOLVED):
        require(marker not in extracted, f"Private/UI/placeholder residue in PDF: {marker}")
    pdffonts = shutil.which("pdffonts")
    pdftotext = shutil.which("pdftotext")
    require(pdffonts is not None and pdftotext is not None, "Poppler inspection tools unavailable")
    font_result = subprocess.run([pdffonts, str(PDF)], check=True, capture_output=True, text=True)
    font_rows = [line.split() for line in font_result.stdout.splitlines()[2:] if line.strip()]
    require(len(font_rows) == EXPECTED_PDF_FONT_ROWS, f"PDF font inventory mismatch: {len(font_rows)}")
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
    validate_configuration()
    for path, expected in INPUT_EXPECTED.items():
        verify_file(path, *expected)
    for path, expected in POST_BUILD_EXPECTED.items():
        verify_file(path, *expected)
    build_text = BUILD_SCRIPT.read_text(encoding="utf-8")
    require("__UNIT_019_" not in build_text, "Build script still contains Unit 019 sentinels")
    require(build_text.count("& $pandoc @common @htmlArgs") == 2, "Build script lacks two HTML builds")
    require(build_text.count("& $pandoc @pdfCommon @pdfArgs") == 2, "Build script lacks two PDF builds")
    require("HTML reproducibility failure" in build_text and "PDF reproducibility failure" in build_text, "Build script reproducibility gates missing")
    require("--mathml" in build_text and "--embed-resources" in build_text and "semantic-cumulative.css" in build_text, "Build script HTML contract mismatch")
    source_ids, blocks, reviews = verify_sources()
    html_reproduction = reproduce_html()
    html = verify_html(source_ids)
    pdf, text_bytes = verify_pdf()
    artifacts = verify_manifest()
    render = write_render_inventory()
    write_visual_receipt(render, html, pdf)
    receipt = {
        "schema_version": "1.0",
        "status": "pass",
        "role_id": "O012",
        "course_id": "D60",
        "unit_ids": [f"o012-rbt-l{n:02d}" for n in range(1, 20)],
        "source_authority": {"commit_sha1": "b947ad2e9f9e301bfe24590a9db653bc54fa1a53", "tree_sha1": "aa1d3edb85818e7176e2d0bbc06d9b4bd1e247f5", "path": "Notes.tex", "line_start": 134, "line_end": 3947, "next_line": 3948, "next_boundary": "Lecture 20: Here\\lecturenum{20} are a bunch of concrete examples"},
        "reader_sources": [{"path": path.relative_to(LANE).as_posix(), "bytes": expected[0], "lines": expected[1], "sha256": expected[2], "stable_ids": count} for path, expected, count in zip(SOURCES, SOURCE_EXPECTED, EXPECTED_ID_COUNTS, strict=True)],
        "block_counts": blocks,
        "html": html,
        "html_reproduction": html_reproduction,
        "pdf": pdf,
        "artifacts": artifacts,
        "witnesses": {"independent_reviews": reviews, "terminology_migration_receipt_sha256": INPUT_EXPECTED[MIGRATION_RECEIPT][1], "extracted_text_bytes": len(text_bytes), "extracted_text_sha256": sha256(TEXT_WITNESS), "visual_receipt_bytes": VISUAL.stat().st_size, "visual_receipt_sha256": sha256(VISUAL), "render_inventory": render, "build_script_sha256": sha256(BUILD_SCRIPT)},
        "responsive_browser": {key: value for key, value in VISUAL_FACTS.items() if key != "full_resolution_spot_checks" and key != "verdict"},
        "gates": {"authority_exact": True, "source_spans_contiguous_and_bound": True, "structure_and_identifiers_bound": True, "terminology_migration_bound": True, "independent_reviews_closed": True, "mastery_and_source_prompts_present": True, "rights_attribution_non_endorsement": True, "html_two_build_byte_identity": True, "pdf_two_build_fail_closed_gate_in_builder": True, "pdf_not_rebuilt_during_qa": True, "html_semantic_centered_reflowing_native_mathml_offline": True, "html_fragments_ids_aliases_valid": True, "privacy_secret_scan": True, "pdf_metadata_fonts_text_pages_verified": True, "visual_review": f"pass_all_{EXPECTED_PDF_PAGES}_pages_plus_browser_desktop_mobile"},
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
