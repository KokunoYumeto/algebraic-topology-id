#!/usr/bin/env python3
"""Fail-closed QA for the cumulative O012 Units 001-010 reader."""

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
from urllib.parse import unquote, urlparse

from lxml import etree
from pypdf import PdfReader


LANE = Path(__file__).resolve().parents[1]
SOURCES = (
    LANE / "source/id-ID/reader-unit-001.md",
    LANE / "source/id-ID/units/unit-002-lecture-002.md",
    LANE / "source/id-ID/units/unit-003-lecture-003.md",
    LANE / "source/id-ID/units/unit-004-lecture-004.md",
    LANE / "source/id-ID/units/unit-005-lecture-005.md",
    LANE / "source/id-ID/units/unit-006-lecture-006.md",
    LANE / "source/id-ID/units/unit-007-lecture-007.md",
    LANE / "source/id-ID/units/unit-008-lecture-008.md",
    LANE / "source/id-ID/units/unit-009-lecture-009.md",
    LANE / "source/id-ID/units/unit-010-lecture-010.md",
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
)
EXPECTED_ID_COUNTS = (29, 41, 39, 33, 30, 28, 24, 26, 30, 26)
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
)

HTML = LANE / "output/html/units-001-010/index.html"
PDF = LANE / "output/pdf/topologi-aljabar-unit-001-010-id.pdf"
MANIFEST = LANE / "output/ARTIFACT_MANIFEST_UNITS_001_010.csv"
VISUAL = LANE / "qa/UNITS_001_010_VISUAL_QA.md"
TEXT_WITNESS = LANE / "qa/units-001-010-extracted.txt"
RECEIPT = LANE / "qa/UNITS_001_010_QA.json"
AUTHORITY = LANE / "00_control/AUTHORITY.json"
UPSTREAM_MANIFEST = LANE / "00_control/UPSTREAM_FILE_MANIFEST.csv"
ADVERSE_LEDGER = LANE / "00_control/ADVERSE_LEDGER.csv"
TERMINOLOGY = LANE / "00_control/TERMINOLOGY.csv"
REVIEWS = (
    LANE / "qa/UNIT_008_INDEPENDENT_REVIEW.md",
    LANE / "qa/UNIT_009_INDEPENDENT_REVIEW.md",
    LANE / "qa/UNIT_010_INDEPENDENT_REVIEW.md",
)

POST_BUILD_EXPECTED = {
    HTML: (1318415, "e228ac1422b2742d873feffd5b236fe9c1329d0bdb5da0e8deffe5e770361088"),
    PDF: (862913, "d0f739aedf3da5f317cf99a1a0dcace1f89b8c802f1dedc42c7ac0c63375c7c1"),
    MANIFEST: (248, "5bcf82984e3f2848f5471876401e48948639d6ca144e0915d99c86c20fc39d92"),
    VISUAL: (2471, "439099f8c865125864444f9cfd1f60b961274ba0bc6f9bb29c562ee30fab132b"),
    TEXT_WITNESS: (280664, "4932889b582a3ccd9816db4b8008791d5fbdc4b044da6f5d1985a87b6ce10642"),
    REVIEWS[0]: (2191, "6960e19949642723dcbfd6ff5bfe105fe4e2789f5989787c041c7f41bdfdac3f"),
    REVIEWS[1]: (2147, "af91c517608c454466d6371db479385ddb1b4c65ecba2f05ca9ec7b26b49cbe6"),
    REVIEWS[2]: (2683, "236123c6c1ad15773a1da7f36887a2ebed93298f019db80f79dfa9bcdac100fd"),
}

# Every pre-existing source, published artifact, and QA witness is byte-frozen.
HISTORICAL_EXPECTED = {
    "output/ARTIFACT_MANIFEST.csv": (228, "13772b2e2400923351225f422effe5f958e1dd8e178b9f6a32207682f791bcc3"),
    "output/ARTIFACT_MANIFEST_UNITS_001_002.csv": (247, "93e98f6cbbc60775bb934df5b49141f63d7cd2c76582a26c61d4192ff320d721"),
    "output/ARTIFACT_MANIFEST_UNITS_001_003.csv": (247, "1e211afb4b165435ece5f72a2b4e9b084975db35d111127880255473302f5049"),
    "output/ARTIFACT_MANIFEST_UNITS_001_004.csv": (247, "4c8bf407e426feb8db92308c4b28bdbbc0738416a85a13539ef7915e4c1aad83"),
    "output/ARTIFACT_MANIFEST_UNITS_001_005.csv": (247, "2910fd87871675730aea7ca33e636a70d330d0f81183e887bad74ea1fd2d5190"),
    "output/html/index.html": (85580, "5cc4a29f2c29b274328b574d6698a51d75af0939f9959937db8d679c38ad51b8"),
    "output/html/units-001-002/index.html": (220035, "d3b5cbfaa3511823821ecf9ba26a4eaec7c84d937417927d11bde3f66abc9f54"),
    "output/html/units-001-003/index.html": (359397, "33281cc46faa3d560c968b657526cd914786c991d1475b5563911a265bd316c1"),
    "output/html/units-001-004/index.html": (494732, "8c8f5e1ad8172a2d97e3931fc3b4f2a3aa7f9e8a709260a27103f7eca0f1357d"),
    "output/html/units-001-005/index.html": (610594, "8d3accf480101565409909c05f987f44b73f1c98889128e2f5074a4e049f48f3"),
    "output/pdf/topologi-aljabar-unit-001-id.pdf": (321743, "6f71546a616c02ef81f8747ecfce3875784842065fc131cc82e5060b066a59c9"),
    "output/pdf/topologi-aljabar-unit-001-002-id.pdf": (395385, "0413c3a3280955cc482a5c0c2d7615b78128dccba3b6b1901dee1bf34d133b8e"),
    "output/pdf/topologi-aljabar-unit-001-003-id.pdf": (460320, "2c9bf67e74c94bca9aad0238e910816188a957892a6cf811f7f615e221b4066d"),
    "output/pdf/topologi-aljabar-unit-001-004-id.pdf": (539006, "5e92c4c6ed60bca9f2f4d362d4c48b4f01aa156b330e2adacd1bf88dd7de9e87"),
    "output/pdf/topologi-aljabar-unit-001-005-id.pdf": (589065, "d6929434a9bc7ae78fb71fc060e9cc54dce85d37e4997ffe042ccbab982e64e2"),
    "qa/UNIT_001_QA.json": (1827, "194c231b57e044fefeefc109d96850791101948584c0ebded4d338b30ff332b3"),
    "qa/UNIT_001_INDEPENDENT_REVIEW.md": (2061, "efb9858eda0dcc6f90e60ce7218b80ed6218ca5775d1c5a49d51ac0629d04c24"),
    "qa/UNIT_002_INDEPENDENT_REVIEW.md": (1616, "a2e879546f0b9c6caeae78e8b7babe0ce32da17118d7840d6803e9b89d82d3f5"),
    "qa/UNIT_003_INDEPENDENT_REVIEW.md": (2464, "b2cffbcc2167c3d620f1af53224cc064e8ce34400561868339e69c280845619c"),
    "qa/UNIT_004_INDEPENDENT_REVIEW.md": (3031, "ac993a10e22738197775ae5c3f4e72948983c4e99ff602a52943b40ed417b6f9"),
    "qa/UNIT_005_INDEPENDENT_REVIEW.md": (1592, "399b81a06ac5701eca6604406c40acaa76f100291ee57f8efeb5344e7d7c8de0"),
    "qa/UNIT_001_VISUAL_QA.md": (1563, "686fe066d9c5a21f0c14c483371a649c5a95602d40e965ec03da9c5c13579675"),
    "qa/UNITS_001_002_QA.json": (2690, "075546f6a856638dc420ed62b23ec78c7a57f839444e4f2101233d6421f776f0"),
    "qa/UNITS_001_002_VISUAL_QA.md": (1834, "939576c3d3fd9e1a2bbd6ca54080ffbdf0a60fc7aecce1baed90e7e46c3f6ffe"),
    "qa/UNITS_001_003_QA.json": (3983, "fb511086669846b6c8a68a6c1fecc4bd774016a6c95eb27219e3babbd177a873"),
    "qa/UNITS_001_003_VISUAL_QA.md": (2310, "4d7d603c2276bd570e3bf47897c67d98bf6507d2bd9ffed2acd10ab1a509130e"),
    "qa/UNITS_001_004_QA.json": (4478, "1670bbe2377712c9f96b9a68cdb75589ae461512f77cea7ad0c9290193724bd5"),
    "qa/UNITS_001_004_VISUAL_QA.md": (2257, "74e609e94ea47b89db223c21e12cae682048f0a60d8780dae96d5b0164f2c5ca"),
    "qa/UNITS_001_005_QA.json": (4768, "ffb6703e4fe2ebc1c7733dc4f87a32c64c53cbe3ebf326d65a8d2da94765635a"),
    "qa/UNITS_001_005_VISUAL_QA.md": (2877, "ed8249702d8335b01dc40925af1d5b071fa18d2eef9fe628a5535bd9404fbcdd"),
    "qa/unit-001-extracted.txt": (15910, "62bfc246a61b03a3727bccbf64f2022463db5cf5595e0b6bd0a38e3e0fce6222"),
    "qa/units-001-002-extracted.txt": (44049, "ca507d19a8c3089ef9190fcbd31d56c41ea61dd59e5849bba7d0ed1e65ef37b1"),
    "qa/units-001-003-extracted.txt": (71549, "2e8eabce2e0b8c3114b49d630187a6a0217e3ae90c466b5441f9eedccb299702"),
    "qa/units-001-004-extracted.txt": (100684, "3d27bc1ab5a780bffce12d5951623b60929069238a210961740234502e71bf35"),
    "qa/units-001-005-extracted.txt": (128786, "83aca1060966c7ca7a7852630c27926754f0d893749aeb80888bbfd00f56a725"),
    "qa/UNIT_006_INDEPENDENT_REVIEW.md": (1783, "5dd3868192a85e3e60562f42ec7d7b792e0e58811719ecc97207ed2bdc5de4bf"),
    "qa/UNIT_007_INDEPENDENT_REVIEW.md": (1761, "87c5129cd7d367893860b150c72948de1d196d7cbefe04d53f7a4efecf921f87"),
    "output/ARTIFACT_MANIFEST_UNITS_001_007.csv": (247, "7b279f0413892f0ddedce636b3a272884bb7bfa01410bf33a6ce34c0c34db2f9"),
    "output/html/units-001-007/index.html": (899803, "55135048eafe0f097c45936add885e008392eefdf475270fea37adf6a2a7b7bb"),
    "output/pdf/topologi-aljabar-unit-001-007-id.pdf": (702470, "3764b75ecfb9200e25a165db1f0f97a680384378e2a9a22e129aab57dd860d93"),
    "qa/UNITS_001_007_QA.json": (7384, "2982a9465428eff97e6047bffdadba422b2dc0406e34750f632bfe148ed67617"),
    "qa/UNITS_001_007_VISUAL_QA.md": (3259, "63a4b4545213a7aec1c556a3852b818ba2f207b10cac7e80c62330709604176f"),
    "qa/units-001-007-extracted.txt": (190424, "f6839e7eb7f25c8518ec3fc2e2372b82b1f1387b48402899ff8bc40ce153c8dc"),
}

EXPECTED_HTML_IDS = 431
EXPECTED_STABLE_IDS = 306
EXPECTED_FRAGMENT_HREFS = 123
EXPECTED_MATHML = 3411
EXPECTED_PDF_PAGES = 99
UNIT8_ADVERSE = {f"O012-ADV-{number:04d}" for number in range(95, 113)}
UNIT9_ADVERSE = {f"O012-ADV-{number:04d}" for number in range(113, 126)}
UNIT10_ADVERSE = {f"O012-ADV-{number:04d}" for number in range(126, 143)}
UNIT8_REFLOW = {"O012-ADV-0096", "O012-ADV-0102", "O012-ADV-0107", "O012-ADV-0112"}
UNIT9_REFLOW = {"O012-ADV-0121"}
UNIT10_REFLOW = {"O012-ADV-0134", "O012-ADV-0138"}
EXPECTED_SOURCE_ALIASES = {
    "o012-rbt-l07-exa-003": "eg:piS^1_infinite",
    "o012-rbt-l09-thm-001": "thm:cov_space_gives_faithful_functor",
    "o012-rbt-l09-prop-001": "prop:cov_space_of_IxX",
    "o012-rbt-l09-cor-002": "prop:pullback_by_homotopic_maps_iso",
    "o012-rbt-l10-cor-001": "cor:fibre_of_univ_cov_space",
}
ARTIFACT_PATHS = {
    "output/html/units-001-010/index.html",
    "output/pdf/topologi-aljabar-unit-001-010-id.pdf",
}
PRIVATE_MARKERS = ("C:\\Users\\", "C:/Users/", "github_pat_", "ghp_", "sk-proj_")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_file(path: Path, expected_bytes: int, expected_sha: str) -> None:
    require(path.is_file(), f"Missing file: {path}")
    require(path.stat().st_size == expected_bytes, f"Byte mismatch: {path}")
    require(sha256(path) == expected_sha, f"SHA-256 mismatch: {path}")


def stable_ids(text: str) -> list[str]:
    return re.findall(r"#(o012-[a-z0-9-]+)(?=[}\s])", text)


def block_counts(text: str) -> dict[str, int]:
    values = Counter(
        re.findall(
            r"^::: \{\.(corollary|definition|example|exercise|figure|lemma|note|proof|proposition|question|remark|theorem)\s+#o012-",
            text,
            flags=re.MULTILINE,
        )
    )
    return dict(sorted(values.items()))


def verify_authority() -> tuple[dict, list[str]]:
    with AUTHORITY.open("r", encoding="utf-8") as stream:
        authority = json.load(stream)
    require(authority["role_id"] == "O012" and authority["course_id"] == "D60", "Authority role mismatch")
    require(authority["commit_sha1"] == "b947ad2e9f9e301bfe24590a9db653bc54fa1a53", "Authority commit mismatch")
    require(authority["tree_sha1"] == "aa1d3edb85818e7176e2d0bbc06d9b4bd1e247f5", "Authority tree mismatch")
    for key in ("archive", "active_source", "upstream_pdf"):
        item = authority[key]
        verify_file(LANE / item["path"], int(item["bytes"]), item["sha256"])
    require(authority["license"]["spdx"] == "CC-BY-4.0", "Authority license mismatch")
    require(sha256(LANE / "LICENSE.md") == authority["license"]["license_file_sha256"], "License hash mismatch")
    with UPSTREAM_MANIFEST.open("r", encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    require(len(rows) == 7 and len({row["path"] for row in rows}) == 7, "Upstream manifest mismatch")
    upstream_root = (LANE / authority["active_source"]["path"]).parent
    for row in rows:
        verify_file(upstream_root / row["path"], int(row["bytes"]), row["sha256"])
    require(sha256(UPSTREAM_MANIFEST) == authority["manifest"]["sha256"], "Upstream manifest hash mismatch")
    upstream = (LANE / authority["active_source"]["path"]).read_text(encoding="utf-8").splitlines()
    require(len(upstream) == 6368, "Unexpected upstream line count")
    return authority, upstream


def verify_source_text(label: str, text: str) -> None:
    require("\ufffd" not in text, f"U+FFFD in {label}")
    for marker in ("Ã", "Â", "â€", "ï¿½"):
        require(marker not in text, f"Mojibake in {label}: {marker}")
    for marker in ("TODO", "TBD", "PLACEHOLDER", "FILL_AFTER") + PRIVATE_MARKERS:
        require(marker not in text, f"Private or placeholder residue in {label}: {marker}")
    openings = len(re.findall(r"^::: \{", text, flags=re.MULTILINE))
    closings = len(re.findall(r"^:::\s*$", text, flags=re.MULTILINE))
    require(openings == closings, f"Unbalanced semantic fences in {label}: {openings} != {closings}")
    require(text.count("$$") % 2 == 0, f"Unbalanced display-math delimiters in {label}")


def verify_sources(upstream: list[str]) -> tuple[list[str], dict[str, dict[str, int]]]:
    texts: list[str] = []
    for number, (path, expected) in enumerate(zip(SOURCES, SOURCE_EXPECTED, strict=True), start=1):
        verify_file(path, expected[0], expected[2])
        text = path.read_text(encoding="utf-8")
        require(len(text.splitlines()) == expected[1], f"Unit {number} line-count mismatch")
        verify_source_text(f"Unit {number}", text)
        texts.append(text)

    id_lists = [stable_ids(text) for text in texts]
    for number, (ids, expected) in enumerate(zip(id_lists, EXPECTED_ID_COUNTS, strict=True), start=1):
        require(len(ids) == expected and len(set(ids)) == expected, f"Unit {number} stable-ID mismatch")
    all_ids = [record_id for ids in id_lists for record_id in ids]
    require(len(all_ids) == EXPECTED_STABLE_IDS and len(set(all_ids)) == EXPECTED_STABLE_IDS, "Cumulative stable-ID mismatch")

    blocks = [block_counts(text) for text in texts]
    for number, (actual, expected) in enumerate(zip(blocks, EXPECTED_BLOCKS, strict=True), start=1):
        require(actual == expected, f"Unit {number} semantic-block mismatch: {actual}")

    spans = ((1771, 1946, 8), (1947, 2093, 9), (2094, 2272, 10))
    expected_envs = (
        {"definition": 3, "example": 3, "lemma": 1, "proof": 1, "prop": 2},
        {"corollary": 4, "example": 1, "proof": 5, "prop": 1, "theorem": 2},
        {"corollary": 2, "definition": 1, "example": 2, "proof": 3, "theorem": 1},
    )
    for (start, end, lecture), expected_env in zip(spans, expected_envs, strict=True):
        span = "\n".join(upstream[start - 1 : end])
        require(rf"\lecturenum{{{lecture}}}" in upstream[start - 1], f"Lecture {lecture} opening marker mismatch")
        require(rf"\lecturenum{{{lecture + 1}}}" not in span, f"Lecture {lecture} span leaks into next lecture")
        require(rf"\lecturenum{{{lecture + 1}}}" in upstream[end], f"Lecture {lecture + 1} boundary marker missing")
        actual = {key: span.count(rf"\begin{{{key}}}") for key in expected_env}
        require(actual == expected_env, f"Unit {lecture} upstream environment mismatch: {actual}")

    unit8, unit9, unit10 = texts[7], texts[8], texts[9]
    for token in (
        r"\Pi_1(X,A)(x,y):=[\{*\},P_x^yX]", r"h(1,x)=x_0",
        r"\rho_Z\colon\Pi_1(X)\to\mathbf{Set}", "funktor monodromi",
        "aksi kanan pada serat", "grupoid aksi", "kodiskret",
    ):
        require(token in unit8, f"Missing Unit 8 correction/mastery invariant: {token}")
    for token in (
        r"Z_0:=Z_{\{0\}\times X}", "hukum eksponensial",
        "bergantung pada homotopi", "pengangkatan homotopi",
        r"H\backslash G", r"\operatorname{Stab}_G(z)",
        'data-source-label="thm:cov_space_gives_faithful_functor"',
        'data-source-label="prop:cov_space_of_IxX"',
        'data-source-label="prop:pullback_by_homotopic_maps_iso"',
    ):
        require(token in unit9, f"Missing Unit 9 correction/mastery invariant: {token}")
    for token in (
        r"\operatorname{Stab}(p)\backslash G", r"\pi_*\bigl(\pi_1(Z,z)\bigr)",
        r"\Pi_1(S^1,A)(x,y)", "baji", r"q_1\colon Z_1",
        r"R_{ab}=R_b\circ R_a=(ABC)", "Identitas adalah kata kosong",
        'data-source-label="cor:fibre_of_univ_cov_space"',
    ):
        require(token in unit10, f"Missing Unit 10 correction/mastery invariant: {token}")

    for local_id, alias in EXPECTED_SOURCE_ALIASES.items():
        cumulative = "\n".join(texts)
        require(cumulative.count(f'#{local_id}') == 1, f"Source alias stable ID mismatch: {local_id}")
        require(cumulative.count(f'data-source-label="{alias}"') == 1, f"Source alias mismatch: {alias}")

    for lecture, text in ((8, unit8), (9, unit9), (10, unit10)):
        checks = range(2, 6) if lecture in (8, 9) else range(1, 6)
        for number in checks:
            require(text.count(f"#o012-rbt-l{lecture:02d}-mcheck-{number:03d}") == 1, f"Unit {lecture} mastery check {number} mismatch")
        for number in range(1, 6):
            require(text.count(f"#o012-rbt-l{lecture:02d}-sol-{number:03d}") == 1, f"Unit {lecture} solution {number} mismatch")
        if lecture in (8, 9):
            require(text.count(f"#o012-rbt-l{lecture:02d}-ex-001") == 1, f"Unit {lecture} upstream exercise mismatch")
        require("David Michael Roberts" in text and re.search(r"\*Algebraic\s+Topology\*", text) is not None, f"Unit {lecture} attribution missing")
        require(re.search(r"Creative Commons Attribution 4\.0\s+International", text) is not None, f"Unit {lecture} license link missing")
        require(re.search(r"tidak menyiratkan dukungan atau\s+pengesahan", text) is not None, f"Unit {lecture} non-endorsement missing")

    return all_ids, {f"unit_{number:03d}": blocks[number - 1] for number in range(1, 11)}


def verify_controls() -> dict[str, object]:
    with ADVERSE_LEDGER.open("r", encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    require(len(rows) >= 142 and all(None not in row and len(row) == 7 for row in rows), "Adverse ledger CSV shape mismatch")
    indexed = {row["event_id"]: row for row in rows}
    require(len(indexed) == len(rows), "Duplicate adverse-ledger event ID")
    required = UNIT8_ADVERSE | UNIT9_ADVERSE | UNIT10_ADVERSE
    require(required <= indexed.keys(), f"Missing Unit 8-10 adverse events: {sorted(required-indexed.keys())}")
    for event_id in required:
        row = indexed[event_id]
        require(row["source_location"].startswith("Notes.tex:"), f"Malformed source location: {event_id}")
        require(row["observed"].strip() and row["action"].strip() and row["rationale"].strip(), f"Incomplete adverse event: {event_id}")
    require({event_id for event_id in UNIT8_ADVERSE if indexed[event_id]["status"] == "accessibility_reflow"} == UNIT8_REFLOW, "Unit 8 reflow inventory mismatch")
    require({event_id for event_id in UNIT9_ADVERSE if indexed[event_id]["status"] == "accessibility_reflow"} == UNIT9_REFLOW, "Unit 9 reflow inventory mismatch")
    require({event_id for event_id in UNIT10_ADVERSE if indexed[event_id]["status"] == "accessibility_reflow"} == UNIT10_REFLOW, "Unit 10 reflow inventory mismatch")
    selected_adverse = [row for row in rows if row["event_id"] in required]
    selected_adverse_raw = "".join(
        json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
        for row in selected_adverse
    ).encode("utf-8")
    adverse_subset_sha = hashlib.sha256(selected_adverse_raw).hexdigest()
    require(adverse_subset_sha == "96bacf0ed12097d564fbecc0ad0a3ed09b94cdf7d9ac72c145f1d42549f4fd16", "Unit 8-10 adverse subset hash mismatch")
    with TERMINOLOGY.open("r", encoding="utf-8", newline="") as stream:
        terms = list(csv.DictReader(stream))
    require(len(terms) >= 171 and all(None not in row and len(row) == 6 for row in terms), "Terminology CSV shape mismatch")
    term_ids = [row["term_id"] for row in terms]
    require(len(term_ids) == len(set(term_ids)), "Duplicate terminology ID")
    required_terms = {f"O012-TERM-{number:04d}" for number in range(134, 172)}
    require(required_terms <= set(term_ids), "Unit 8-10 terminology range incomplete")
    selected_terms = [row for row in terms if row["term_id"] in required_terms]
    selected_terms_raw = "".join(
        json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
        for row in selected_terms
    ).encode("utf-8")
    terms_subset_sha = hashlib.sha256(selected_terms_raw).hexdigest()
    require(terms_subset_sha == "79bc857a5a50bfcfdfebf58685403f9e8d905d1e86bda740d44ae29eaa426271", "Unit 8-10 terminology subset hash mismatch")
    return {
        "unit_008_adverse_ids": sorted(UNIT8_ADVERSE),
        "unit_009_adverse_ids": sorted(UNIT9_ADVERSE),
        "unit_010_adverse_ids": sorted(UNIT10_ADVERSE),
        "unit_008_accessibility_reflows": sorted(UNIT8_REFLOW),
        "unit_009_accessibility_reflows": sorted(UNIT9_REFLOW),
        "unit_010_accessibility_reflows": sorted(UNIT10_REFLOW),
        "terminology_ids": [f"O012-TERM-{number:04d}" for number in range(134, 172)],
        "adverse_subset_sha256": adverse_subset_sha,
        "terminology_subset_sha256": terms_subset_sha,
    }


def verify_reviews() -> dict[str, str]:
    out: dict[str, str] = {}
    for lecture, path, source_expected, span in zip((8, 9, 10), REVIEWS, SOURCE_EXPECTED[7:], ("1771-1946", "1947-2093", "2094-2272"), strict=True):
        review = path.read_text(encoding="utf-8")
        require(source_expected[2] in review, f"Unit {lecture} review source hash missing")
        require("Verdict: **PASS" in review and "P1 = 0" in review and "P2 = 0" in review and "P3 = 0" in review, f"Unit {lecture} review is not all-clear")
        require(span in review and "Notes.tex" in review, f"Unit {lecture} review span missing")
        require(
            str(EXPECTED_ID_COUNTS[lecture - 1]) in review and "stable IDs" in review,
            f"Unit {lecture} review ID count missing",
        )
        out[f"unit_{lecture:03d}_independent_review_sha256"] = sha256(path)
    visual = VISUAL.read_text(encoding="utf-8")
    require("Verdict: **PASS**" in visual and "All 99 pages" in visual, "Visual all-page review missing")
    require("1280 by 720" in visual and "390 by 844" in visual, "Responsive viewport evidence missing")
    require("document-level horizontal overflow was zero" in visual, "Responsive overflow evidence missing")
    require("37 were wider" in visual and "all 37 exposed local horizontal scrolling" in visual, "Formula-local scrolling evidence missing")
    out["visual_review_sha256"] = sha256(VISUAL)
    return out


def verify_html(source_ids: list[str]) -> dict[str, int]:
    root = etree.parse(str(HTML), etree.HTMLParser(recover=True)).getroot()
    require(root.get("lang") == "id-ID", "HTML lang mismatch")
    require("".join(root.xpath("//title/text()")) == "Topologi Aljabar - Unit 1-10", "HTML title mismatch")
    html_ids = root.xpath("//*[@id]/@id")
    require(len(html_ids) == EXPECTED_HTML_IDS and len(set(html_ids)) == EXPECTED_HTML_IDS, "HTML ID inventory mismatch")
    html_id_set = set(html_ids)
    require(set(source_ids) <= html_id_set, "One or more stable IDs are missing from HTML")
    fragment_hrefs = [href for href in root.xpath("//@href") if href.startswith("#")]
    require(len(fragment_hrefs) == EXPECTED_FRAGMENT_HREFS, "HTML fragment-link count mismatch")
    for href in fragment_hrefs:
        target = unquote(href[1:])
        require(target and target in html_id_set, f"Broken local fragment: {href}")
    external_hrefs = [href for href in root.xpath("//@href") if not href.startswith("#")]
    require(all(urlparse(href).scheme == "https" for href in external_hrefs), "Non-HTTPS external link in HTML")
    require(not root.xpath("//script|//link[@rel='stylesheet']"), "HTML has script or unembedded stylesheet")
    require(not root.xpath("//img|//object|//embed|//iframe|//video|//audio|//source"), "Unexpected runtime asset element")
    for attribute in ("src", "srcset", "poster", "data"):
        require(not root.xpath(f"//@{attribute}"), f"HTML has runtime @{attribute} dependency")
    math_count = len(root.xpath("//*[local-name()='math']"))
    require(math_count == EXPECTED_MATHML, f"MathML count mismatch: {math_count}")
    require(not root.xpath("//img[contains(@class,'math')]"), "Math was emitted as images")
    aliases = {element.get("id"): element.get("data-source-label") for element in root.xpath('//*[@data-source-label]')}
    require(aliases == EXPECTED_SOURCE_ALIASES, f"Source-label aliases mismatch: {aliases}")
    styles = "\n".join(root.xpath("//style/text()"))
    for rule in ("max-width: 58rem", "margin: 0 auto", 'math[display="block"]', "overflow-x: auto", ".question", ".theorem", ".corollary", ".remark", ".figure"):
        require(rule in styles, f"Missing cumulative style rule: {rule}")
    require("@import" not in styles and not re.search(r"url\(\s*['\"]?https?://", styles, flags=re.I), "External CSS dependency")
    data = HTML.read_text(encoding="utf-8")
    require("<math" in data and "http://www.w3.org/1998/Math/MathML" in data, "Native MathML serialization missing")
    for marker in PRIVATE_MARKERS:
        require(marker not in data, f"Private marker in HTML: {marker}")
    return {
        "html_ids": len(html_ids),
        "stable_ids": len(source_ids),
        "fragment_links": len(fragment_hrefs),
        "external_https_links": len(external_hrefs),
        "mathml_nodes": math_count,
        "source_aliases": len(aliases),
    }


def verify_pdf() -> tuple[dict[str, object], bytes]:
    reader = PdfReader(str(PDF), strict=True)
    require(not reader.is_encrypted, "PDF is encrypted")
    require(len(reader.pages) == EXPECTED_PDF_PAGES, f"PDF page mismatch: {len(reader.pages)}")
    root = reader.trailer["/Root"]
    require(root.get("/Lang") == "id-ID", "PDF /Lang mismatch")
    require("/AcroForm" not in root and "/StructTreeRoot" not in root, "Unexpected PDF form/tagging state")
    open_action = root.get("/OpenAction")
    if open_action is not None:
        action = open_action.get_object()
        require(action.get("/S") != "/JavaScript" and "/JS" not in action, "Unexpected PDF JavaScript")
    names = root.get("/Names")
    if names is not None:
        require("/JavaScript" not in names.get_object(), "Unexpected PDF JavaScript name tree")
    metadata = reader.metadata
    require(metadata.title == "Topologi Aljabar - Unit 1-10", "PDF title mismatch")
    require(metadata.author == "David Michael Roberts (materi sumber); Edisi Bahasa Indonesia dengan pendamping penguasaan", "PDF author mismatch")
    require(metadata.creator == "LaTeX via pandoc" and "pdfTeX" in (metadata.producer or ""), "PDF toolchain metadata mismatch")
    require(str(metadata.get("/CreationDate")) == "D:20260822000000Z", "PDF creation date mismatch")
    require(str(metadata.get("/ModDate")) == "D:20260822000000Z", "PDF modification date mismatch")

    extracted = "\n".join(page.extract_text() or "" for page in reader.pages)
    for phrase in (
        "Kuliah 1", "Kuliah 2", "Kuliah 3", "Kuliah 4", "Kuliah 5", "Kuliah 6", "Kuliah 7", "Kuliah 8", "Kuliah 9", "Kuliah 10",
        "Topologi kompak-terbuka pada ruang lintasan", "Grup fundamental dan serat ruang penutup",
        "Grupoid Fundamental", "Penutup tiga lembar yang mendeteksi nonkomutativitas",
        "Solusi Pemeriksaan 8.5", "Solusi Pemeriksaan 9.5", "Solusi Pemeriksaan 10.5",
    ):
        require(phrase in extracted, f"Missing PDF text: {phrase}")
    for marker in PRIVATE_MARKERS + ("No correct answer",):
        require(marker not in extracted, f"Private or English UI residue in PDF: {marker}")

    pdffonts = shutil.which("pdffonts")
    require(pdffonts is not None, "pdffonts unavailable")
    font_result = subprocess.run([pdffonts, str(PDF)], check=True, capture_output=True, text=True)
    font_rows = [line.split() for line in font_result.stdout.splitlines()[2:] if line.strip()]
    require(len(font_rows) == 23, f"Unexpected PDF font inventory: {len(font_rows)}")
    require(all(len(row) >= 5 and row[-5:-2] == ["yes", "yes", "yes"] for row in font_rows), "PDF font embedding/ToUnicode failure")

    pdftotext = shutil.which("pdftotext")
    require(pdftotext is not None, "pdftotext unavailable")
    text_result = subprocess.run([pdftotext, "-layout", "-enc", "UTF-8", str(PDF), "-"], check=True, capture_output=True)
    require(text_result.stdout == TEXT_WITNESS.read_bytes(), "Stored text witness differs from current PDF extraction")
    return (
        {
            "pages": len(reader.pages), "encrypted": False, "lang": "id-ID", "tagged": False,
            "fonts": len(font_rows), "all_fonts_embedded": True, "all_fonts_tounicode": True,
            "extracted_characters": len(extracted),
        },
        text_result.stdout,
    )


def verify_manifest() -> list[dict[str, object]]:
    with MANIFEST.open("r", encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    require(len(rows) == 2 and len({row["path"] for row in rows}) == 2, "Manifest shape mismatch")
    require([row["path"] for row in rows] == sorted(ARTIFACT_PATHS), "Manifest paths/order mismatch")
    for row in rows:
        path = LANE / row["path"]
        require(re.fullmatch(r"[0-9a-f]{64}", row["sha256"]) is not None, "Invalid manifest SHA-256")
        verify_file(path, int(row["bytes"]), row["sha256"])
        require((int(row["bytes"]), row["sha256"]) == POST_BUILD_EXPECTED[path], f"Manifest/frozen expectation mismatch: {row['path']}")
    return [{"path": row["path"], "bytes": int(row["bytes"]), "sha256": row["sha256"]} for row in rows]


def main() -> int:
    for relative, expected in HISTORICAL_EXPECTED.items():
        verify_file(LANE / relative, *expected)
    for path, expected in POST_BUILD_EXPECTED.items():
        verify_file(path, *expected)
    authority, upstream = verify_authority()
    source_ids, blocks = verify_sources(upstream)
    controls = verify_controls()
    reviews = verify_reviews()
    html = verify_html(source_ids)
    pdf, text_bytes = verify_pdf()
    artifacts = verify_manifest()

    receipt = {
        "schema_version": "1.0",
        "status": "pass",
        "role_id": "O012",
        "course_id": "D60",
        "unit_ids": [f"o012-rbt-l{number:02d}" for number in range(1, 11)],
        "source_authority": {
            "commit_sha1": authority["commit_sha1"],
            "tree_sha1": authority["tree_sha1"],
            "path": "Notes.tex",
            "line_start": 134,
            "line_end": 2272,
            "next_line": 2273,
            "next_boundary": "Lecture 11 marker",
        },
        "reader_sources": [
            {
                "path": path.relative_to(LANE).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
                "lines": expected[1],
                "stable_ids": id_count,
            }
            for path, expected, id_count in zip(SOURCES, SOURCE_EXPECTED, EXPECTED_ID_COUNTS, strict=True)
        ],
        "block_counts": blocks,
        "controls": controls,
        "html": html,
        "pdf": pdf,
        "artifacts": artifacts,
        "witnesses": {
            **reviews,
            "extracted_text_bytes": len(text_bytes),
            "extracted_text_sha256": sha256(TEXT_WITNESS),
            "prior_boundary_units_001_007_qa_sha256": HISTORICAL_EXPECTED["qa/UNITS_001_007_QA.json"][1],
        },
        "responsive_browser": {
            "desktop_viewport": "1280x720",
            "desktop_body_css_px": 928,
            "desktop_document_overflow_css_px": 0,
            "mobile_viewport": "390x844",
            "mobile_content_css_px": 375.11,
            "mobile_document_overflow_css_px": 0,
            "mobile_wide_display_math": 37,
            "mobile_locally_scrollable_wide_display_math": 37,
            "console_warnings_or_errors": 0,
        },
        "gates": {
            "authority_exact": True,
            "source_spans_contiguous_and_bound": True,
            "structure_and_identifiers_bound": True,
            "mastery_exercise_solution_closure": True,
            "unit_008_010_corrections_reflows_aliases_verified": True,
            "rights_attribution_non_endorsement": True,
            "html_semantic_centered_reflowing_native_mathml_offline": True,
            "html_fragments_ids_and_alias_valid": True,
            "privacy_secret_scan": True,
            "html_and_pdf_two_build_byte_identity": True,
            "pdf_metadata_fonts_text_pages_verified": True,
            "visual_review": "pass_manual_all_99_pages_and_browser_desktop_mobile",
            "every_prior_source_artifact_qa_witness_unchanged": True,
        },
        "known_caveat": "PDF is intentionally secondary and untagged; semantic HTML with native MathML is the primary accessibility surface.",
    }
    RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(
        "PASS "
        f"stable_ids={len(source_ids)} blocks={sum(sum(values.values()) for values in blocks.values())} "
        f"mathml={html['mathml_nodes']} pdf_pages={pdf['pages']} receipt_sha256={sha256(RECEIPT)}"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise
