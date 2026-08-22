#!/usr/bin/env python3
"""Strict QA for the cumulative O012 Units 001-003 reader.

The post-build values marked ``FILL_AFTER_BUILD`` are deliberately fail-closed.
Populate them only after the cumulative artifacts and review witnesses are final.
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
BASE_CSS = LANE / "source" / "id-ID" / "styles" / "reader.css"
CUMULATIVE_CSS = LANE / "source" / "id-ID" / "styles" / "reader-cumulative.css"

HTML = LANE / "output" / "html" / "units-001-003" / "index.html"
PDF = LANE / "output" / "pdf" / "topologi-aljabar-unit-001-003-id.pdf"
MANIFEST = LANE / "output" / "ARTIFACT_MANIFEST_UNITS_001_003.csv"
AUTHORITY = LANE / "00_control" / "AUTHORITY.json"
UPSTREAM_MANIFEST = LANE / "00_control" / "UPSTREAM_FILE_MANIFEST.csv"
ADVERSE_LEDGER = LANE / "00_control" / "ADVERSE_LEDGER.csv"
VISUAL = LANE / "qa" / "UNITS_001_003_VISUAL_QA.md"
INDEPENDENT_3 = LANE / "qa" / "UNIT_003_INDEPENDENT_REVIEW.md"
TEXT_WITNESS = LANE / "qa" / "units-001-003-extracted.txt"
RECEIPT = LANE / "qa" / "UNITS_001_003_QA.json"

# These files are immutable historical witnesses at the Unit 3 boundary. This is
# intentionally broader than the cumulative build's direct inputs: a new build
# must not silently rewrite an earlier source, artifact, manifest, or QA record.
HISTORICAL_EXPECTED = {
    SOURCE_1: (16179, "c80b51c22a2fa7ea116201028b78d5f8d708ef4d8355d34092ac7a9c88415e15"),
    SOURCE_2: (25090, "4d2acc43557db9b3c419ee177545d285b9fcf50b2aa2dd3b2c6c44182f3a6a01"),
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
    LANE / "qa" / "UNIT_001_INDEPENDENT_REVIEW.md": (
        2061,
        "efb9858eda0dcc6f90e60ce7218b80ed6218ca5775d1c5a49d51ac0629d04c24",
    ),
    LANE / "qa" / "UNIT_001_VISUAL_QA.md": (
        1563,
        "686fe066d9c5a21f0c14c483371a649c5a95602d40e965ec03da9c5c13579675",
    ),
    LANE / "qa" / "unit-001-extracted.txt": (
        15910,
        "62bfc246a61b03a3727bccbf64f2022463db5cf5595e0b6bd0a38e3e0fce6222",
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
    LANE / "qa" / "UNIT_002_INDEPENDENT_REVIEW.md": (
        1616,
        "a2e879546f0b9c6caeae78e8b7babe0ce32da17118d7840d6803e9b89d82d3f5",
    ),
    LANE / "qa" / "UNITS_001_002_VISUAL_QA.md": (
        1834,
        "939576c3d3fd9e1a2bbd6ca54080ffbdf0a60fc7aecce1baed90e7e46c3f6ffe",
    ),
    LANE / "qa" / "units-001-002-extracted.txt": (
        44049,
        "ca507d19a8c3089ef9190fcbd31d56c41ea61dd59e5849bba7d0ed1e65ef37b1",
    ),
    LANE / "qa" / "UNITS_001_002_QA.json": (
        2690,
        "075546f6a856638dc420ed62b23ec78c7a57f839444e4f2101233d6421f776f0",
    ),
}

SOURCE_3_EXPECTED = (
    25822,
    "993e5941895a9b6f4b197b4c236f5a4990f6ae621e2bb7911353b28a5e1abffd",
)

# FILL_AFTER_BUILD: replace every ``None`` below with a literal exact value.
# The verifier refuses to run while any placeholder remains.
POST_BUILD_EXPECTED: dict[Path, tuple[int | None, str | None]] = {
    HTML: (359397, "33281cc46faa3d560c968b657526cd914786c991d1475b5563911a265bd316c1"),
    PDF: (460320, "2c9bf67e74c94bca9aad0238e910816188a957892a6cf811f7f615e221b4066d"),
    MANIFEST: (247, "1e211afb4b165435ece5f72a2b4e9b084975db35d111127880255473302f5049"),
    VISUAL: (2310, "4d7d603c2276bd570e3bf47897c67d98bf6507d2bd9ffed2acd10ab1a509130e"),
    INDEPENDENT_3: (2464, "b2cffbcc2167c3d620f1af53224cc064e8ce34400561868339e69c280845619c"),
    TEXT_WITNESS: (71549, "2e8eabce2e0b8c3114b49d630187a6a0217e3ae90c466b5441f9eedccb299702"),
}
EXPECTED_HTML_MATHML_NODES: int | None = 1007
EXPECTED_HTML_IDS: int | None = 152
EXPECTED_HTML_FRAGMENT_HREFS: int | None = 41
EXPECTED_PDF_PAGES: int | None = 25

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
ARTIFACT_PATHS = {
    "output/html/units-001-003/index.html",
    "output/pdf/topologi-aljabar-unit-001-003-id.pdf",
}
SOURCE_CORRECTION_IDS = {
    *(f"O012-ADV-{number:04d}" for number in range(21, 30)),
    "O012-ADV-0034",
}
REFLOW_IDS = {f"O012-ADV-{number:04d}" for number in range(30, 34)}
CORRECTION_LOCATIONS = {
    "O012-ADV-0021": "Notes.tex:625-627",
    "O012-ADV-0022": "Notes.tex:609",
    "O012-ADV-0023": "Notes.tex:669-671",
    "O012-ADV-0024": "Notes.tex:674-675",
    "O012-ADV-0025": "Notes.tex:676",
    "O012-ADV-0026": "Notes.tex:694-712",
    "O012-ADV-0027": "Notes.tex:764-776",
    "O012-ADV-0028": "Notes.tex:814-818",
    "O012-ADV-0029": "Notes.tex:839-856",
    "O012-ADV-0030": "Notes.tex:585-587",
    "O012-ADV-0031": "Notes.tex:598-601",
    "O012-ADV-0032": "Notes.tex:695-697",
    "O012-ADV-0033": "Notes.tex:872-875",
    "O012-ADV-0034": "Notes.tex:591-607",
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


def verify_post_build_values_ready() -> None:
    missing: list[str] = []
    for path, (expected_bytes, expected_sha) in POST_BUILD_EXPECTED.items():
        label = path.relative_to(LANE).as_posix()
        if not isinstance(expected_bytes, int) or expected_bytes <= 0:
            missing.append(f"POST_BUILD_EXPECTED[{label}].bytes")
        if not isinstance(expected_sha, str) or not re.fullmatch(r"[0-9a-f]{64}", expected_sha):
            missing.append(f"POST_BUILD_EXPECTED[{label}].sha256")
    if not isinstance(EXPECTED_HTML_MATHML_NODES, int) or EXPECTED_HTML_MATHML_NODES <= 0:
        missing.append("EXPECTED_HTML_MATHML_NODES")
    if not isinstance(EXPECTED_HTML_IDS, int) or EXPECTED_HTML_IDS <= 0:
        missing.append("EXPECTED_HTML_IDS")
    if not isinstance(EXPECTED_HTML_FRAGMENT_HREFS, int) or EXPECTED_HTML_FRAGMENT_HREFS <= 0:
        missing.append("EXPECTED_HTML_FRAGMENT_HREFS")
    if not isinstance(EXPECTED_PDF_PAGES, int) or EXPECTED_PDF_PAGES <= 0:
        missing.append("EXPECTED_PDF_PAGES")
    require(not missing, "Fill exact post-build QA placeholders: " + ", ".join(missing))


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
    require(len(rows) == 7, "Upstream manifest row mismatch")
    require(len({row["path"] for row in rows}) == 7, "Duplicate upstream manifest path")
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
    for placeholder in ("TODO", "TBD", "PLACEHOLDER"):
        require(placeholder not in text, f"Placeholder in {label}: {placeholder}")
    for secret in PRIVATE_MARKERS:
        require(secret not in text, f"Private/control residue in {label}: {secret}")
    openings = len(re.findall(r"^::: \{", text, flags=re.MULTILINE))
    closings = len(re.findall(r"^:::\s*$", text, flags=re.MULTILINE))
    require(openings == closings, f"Semantic fences are unbalanced in {label}: {openings} != {closings}")


def verify_sources(upstream: list[str]) -> tuple[list[str], dict[str, dict[str, int]]]:
    text1 = SOURCE_1.read_text(encoding="utf-8")
    text2 = SOURCE_2.read_text(encoding="utf-8")
    text3 = SOURCE_3.read_text(encoding="utf-8")
    require(len(text3.splitlines()) == 618, "Unit 3 source line-count mismatch")
    for label, text in (("Unit 1", text1), ("Unit 2", text2), ("Unit 3", text3)):
        verify_source_text(label, text)

    ids1, ids2, ids3 = stable_ids(text1), stable_ids(text2), stable_ids(text3)
    require(len(ids1) == 29 and len(set(ids1)) == 29, "Unit 1 stable-ID mismatch")
    require(len(ids2) == 41 and len(set(ids2)) == 41, "Unit 2 stable-ID mismatch")
    require(len(ids3) == 39 and len(set(ids3)) == 39, "Unit 3 stable-ID mismatch")
    require(all(value.startswith("o012-rbt-l03-") or value == "o012-rbt-l03" for value in ids3), "Unit 3 ID namespace mismatch")
    all_ids = ids1 + ids2 + ids3
    require(len(all_ids) == 109 and len(set(all_ids)) == 109, "Cumulative stable-ID mismatch")
    require(block_counts(text1) == BLOCKS_1, f"Unit 1 block mismatch: {block_counts(text1)}")
    require(block_counts(text2) == BLOCKS_2, f"Unit 2 block mismatch: {block_counts(text2)}")
    require(block_counts(text3) == BLOCKS_3, f"Unit 3 block mismatch: {block_counts(text3)}")

    span1 = "\n".join(upstream[133:348])
    span2 = "\n".join(upstream[348:584])
    span3 = "\n".join(upstream[584:877])
    require(span1.count(r"\lecturenum{1}") == 1, "Lecture 1 marker mismatch")
    require(span2.count(r"\lecturenum{2}") == 1, "Lecture 2 marker mismatch")
    require(span3.count(r"\lecturenum{3}") == 1 and r"\lecturenum{4}" not in span3, "Lecture 3 marker mismatch")
    require(upstream[877].strip() == r"\begin{prop}", "Line 878 must be the deferred proposition opening")
    require(r"\lecturenum{4}" in upstream[878], "Line 879 must contain the Lecture 4 marker")

    expected_env2 = {"definition": 3, "example": 8, "ex": 6, "lemma": 3, "proof": 1, "q": 1}
    actual_env2 = {key: span2.count(rf"\begin{{{key}}}") for key in expected_env2}
    require(actual_env2 == expected_env2, f"Unit 2 authority environment mismatch: {actual_env2}")
    expected_env3 = {"definition": 6, "example": 4, "ex": 1, "lemma": 2, "proof": 5, "prop": 3}
    actual_env3 = {key: span3.count(rf"\begin{{{key}}}") for key in expected_env3}
    require(actual_env3 == expected_env3, f"Unit 3 authority environment mismatch: {actual_env3}")
    require(span3.count(r"\xymatrix") == 3, "Unit 3 authority diagram count mismatch")

    # Preserve all previously verified Unit 2 correction and mastery invariants.
    require(r"\bigsqcup_\beta X\times Z_\beta" in span2, "Promoted marginal exercise missing from authority")
    require(r"\{x\in \RR^n\mod |x|\leq 1\}" in span2, "Disk source defect witness missing")
    require("(t,x_i) \\ar@{|->}[r] & tx_i" in span2, "Contraction coordinate source defect missing")
    require(r"x\in Z_\beta" in span2 and r"g_\beta(z) = x" in span2, "Joint-surjectivity source defect missing")
    for token in (
        r"D^n:=\bigl\{x\in\mathbb{R}^n\mid\lVert x\rVert\le 1\bigr\}",
        r"\longmapsto(1-t)x_i",
        "citranya harus memuat setiap nilai di antara $0$ dan $1$, suatu kontradiksi",
        "citra yang memuat paling banyak satu titik",
        "yaitu pemetaan kontinu",
        "maka setiap fungsi kontinu $f",
        "#o012-rbt-l02-sol-007",
        "#o012-rbt-l02-answer-001",
    ):
        require(token in text2, f"Missing Unit 2 invariant: {token}")

    # Each phrase below witnesses one or more of the ten admitted Unit 3 source
    # corrections, the four reflows, or the two added mastery checks.
    for token in (
        "Subset tak kosong $Y\\subseteq X$",
        "Setiap ruang terhubung tak kosong $X$",
        "Ambil $0<r<R$ dan anulus",
        "$H''$ merupakan homotopi dari $H_0$ ke $H'_1$",
        r"H'(2t-1,x),&\tfrac12\le t\le1.",
        r"\widetilde H",
        "Ruang tak kosong $Y$ disebut *terhubung lintasan*",
        "Untuk setiap objek $X$ dari $\\mathcal{C}$",
        "citra $g$ juga memuat paling banyak satu titik",
        "Andaikan semua objek yang dipakai dalam argumen ini terhubung secara lokal",
        "#o012-rbt-l03-check-001",
        "#o012-rbt-l03-check-002",
    ):
        require(token in text3, f"Missing Unit 3 invariant: {token}")

    for number in range(1, 3):
        require(f"#o012-rbt-l01-ex-{number:03d}" in text1, "Unit 1 exercise missing")
        require(f"#o012-rbt-l01-sol-{number:03d}" in text1, "Unit 1 solution missing")
    for number in range(1, 8):
        require(f"#o012-rbt-l02-ex-{number:03d}" in text2, "Unit 2 exercise missing")
        require(f"#o012-rbt-l02-sol-{number:03d}" in text2, "Unit 2 solution missing")
    require("#o012-rbt-l02-q-001" in text2 and "#o012-rbt-l02-answer-001" in text2, "Question-answer closure missing")
    for number in range(1, 6):
        require(text3.count(f"#o012-rbt-l03-ex-{number:03d}") == 1, f"Unit 3 exercise {number} mismatch")
        require(text3.count(f"#o012-rbt-l03-sol-{number:03d}") == 1, f"Unit 3 solution {number} mismatch")
    require(text3.count("#o012-rbt-l03-check-") == 2, "Unit 3 mastery-check count mismatch")

    for phrase in (
        "This is our first example",
        "A space $Y$ is",
        "The whole point of categories",
        "Show that $[",
        "Another important example of a category",
    ):
        require(phrase not in text3, f"Active English residue in Unit 3: {phrase}")
    require("David Michael Roberts" in text3 and "*Algebraic Topology*" in text3, "Protected source attribution missing")
    return all_ids, {"unit_001": BLOCKS_1, "unit_002": BLOCKS_2, "unit_003": BLOCKS_3}


def verify_correction_inventory() -> dict[str, list[str]]:
    with ADVERSE_LEDGER.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    require(rows, "Adverse ledger is empty")
    event_ids = [row["event_id"] for row in rows]
    require(len(event_ids) == len(set(event_ids)), "Duplicate adverse-ledger event ID")
    indexed = {row["event_id"]: row for row in rows}
    required_ids = SOURCE_CORRECTION_IDS | REFLOW_IDS
    require(required_ids <= indexed.keys(), f"Missing Unit 3 ledger events: {sorted(required_ids - indexed.keys())}")
    for event_id in SOURCE_CORRECTION_IDS:
        row = indexed[event_id]
        require(row["source_location"] == CORRECTION_LOCATIONS[event_id], f"Correction location mismatch: {event_id}")
        require(row["status"] in {"corrected_in_translation", "clarified_in_translation"}, f"Correction status mismatch: {event_id}")
        require(row["rationale"].strip(), f"Correction rationale missing: {event_id}")
    for event_id in REFLOW_IDS:
        row = indexed[event_id]
        require(row["source_location"] == CORRECTION_LOCATIONS[event_id], f"Reflow location mismatch: {event_id}")
        require(row["status"] == "accessibility_reflow", f"Reflow status mismatch: {event_id}")
        require(row["rationale"].strip(), f"Reflow rationale missing: {event_id}")
    return {
        "source_corrections": sorted(SOURCE_CORRECTION_IDS),
        "accessibility_reflows": sorted(REFLOW_IDS),
    }


def verify_reviews() -> dict[str, str]:
    review = INDEPENDENT_3.read_text(encoding="utf-8")
    require(SOURCE_3_EXPECTED[1] in review, "Independent review does not bind the frozen Unit 3 source")
    require("PASS. P1 = 0, P2 = 0, P3 = 0." in review, "Independent review is not an all-clear")
    require("Notes.tex" in review and "585" in review and "877" in review, "Independent review source-span witness missing")
    visual = VISUAL.read_text(encoding="utf-8")
    require("PASS" in visual, "Visual review is not marked PASS")
    require("browser" in visual.lower(), "Responsive browser review is missing")
    require(str(EXPECTED_PDF_PAGES) in visual, "Visual review does not name the exact PDF page count")
    return {
        "unit_003_independent_review_sha256": sha256(INDEPENDENT_3),
        "visual_review_sha256": sha256(VISUAL),
    }


def verify_html(source_ids: list[str]) -> dict[str, int]:
    parser = etree.HTMLParser(recover=True)
    root = etree.parse(str(HTML), parser).getroot()
    require(root.get("lang") == "id-ID", "HTML lang mismatch")
    title = "".join(root.xpath("//title/text()"))
    require(title == "Topologi Aljabar - Unit 1-3", f"HTML title mismatch: {title!r}")
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
    require(metadata.title == "Topologi Aljabar - Unit 1-3", "PDF title mismatch")
    require(metadata.author == "David Michael Roberts (materi sumber); Edisi Bahasa Indonesia dengan pendamping penguasaan", "PDF author mismatch")
    require(metadata.creator == "LaTeX via pandoc", "PDF creator mismatch")
    require("pdfTeX" in (metadata.producer or ""), "PDF producer mismatch")
    require(str(metadata.get("/CreationDate")) == "D:20260822000000Z", "PDF creation date mismatch")
    require(str(metadata.get("/ModDate")) == "D:20260822000000Z", "PDF modification date mismatch")
    require("/StructTreeRoot" not in reader.trailer["/Root"], "Unexpected tagging-state change; update the disclosed accessibility model")

    extracted = "\n".join(page.extract_text() or "" for page in reader.pages)
    for phrase in (
        "Kuliah 1",
        "Kuliah 2",
        "Kuliah 3",
        "Komponen terhubung dan himpunan",
        "Kategori homotopi",
        "Solusi Latihan 3.5",
        "Bukti Proposisi 3.2",
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
    for phrase in (b"Kuliah 1", b"Kuliah 2", b"Kuliah 3"):
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
    require(set(paths) == ARTIFACT_PATHS, "Cumulative manifest set mismatch")
    require(paths == sorted(paths), "Cumulative manifest is not deterministically sorted")
    for row in rows:
        require(re.fullmatch(r"[0-9a-f]{64}", row["sha256"]) is not None, f"Invalid manifest SHA-256: {row['path']}")
        verify_file(LANE / row["path"], int(row["bytes"]), row["sha256"])
        expected_bytes, expected_sha = POST_BUILD_EXPECTED[LANE / row["path"]]
        require(int(row["bytes"]) == expected_bytes and row["sha256"] == expected_sha, f"Manifest disagrees with frozen expectation: {row['path']}")
    return [{"path": row["path"], "bytes": int(row["bytes"]), "sha256": row["sha256"]} for row in rows]


def main() -> int:
    verify_post_build_values_ready()
    for path, (size, digest) in HISTORICAL_EXPECTED.items():
        verify_file(path, size, digest)
    verify_file(SOURCE_3, *SOURCE_3_EXPECTED)
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
        "unit_ids": ["o012-rbt-l01", "o012-rbt-l02", "o012-rbt-l03"],
        "source_authority": {
            "commit_sha1": authority["commit_sha1"],
            "tree_sha1": authority["tree_sha1"],
            "path": "Notes.tex",
            "line_start": 134,
            "line_end": 877,
            "next_line": 878,
            "next_boundary": "deferred proposition opening followed by Lecture 4 marker on line 879",
        },
        "reader_sources": [
            {"path": SOURCE_1.relative_to(LANE).as_posix(), "bytes": SOURCE_1.stat().st_size, "sha256": sha256(SOURCE_1), "stable_ids": 29},
            {"path": SOURCE_2.relative_to(LANE).as_posix(), "bytes": SOURCE_2.stat().st_size, "sha256": sha256(SOURCE_2), "stable_ids": 41},
            {"path": SOURCE_3.relative_to(LANE).as_posix(), "bytes": SOURCE_3.stat().st_size, "sha256": sha256(SOURCE_3), "stable_ids": 39},
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
            "prior_units_001_002_qa_sha256": HISTORICAL_EXPECTED[LANE / "qa" / "UNITS_001_002_QA.json"][1],
        },
        "gates": {
            "authority_exact": True,
            "source_spans_bound": True,
            "structure_bound": True,
            "exercise_solution_closure": True,
            "two_mastery_checks_present": True,
            "ten_source_corrections_verified": True,
            "four_accessibility_reflows_verified": True,
            "html_semantic_native_mathml_offline": True,
            "html_fragments_and_ids_valid": True,
            "privacy_secret_scan": True,
            "pdf_reproducible_by_build_script": True,
            "pdf_metadata_fonts_text_pages_verified": True,
            "visual_review": f"pass_manual_all_{EXPECTED_PDF_PAGES}_pages_and_browser_desktop_mobile",
            "unit_001_artifacts_unchanged": True,
            "units_001_002_artifacts_and_qa_unchanged": True,
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
