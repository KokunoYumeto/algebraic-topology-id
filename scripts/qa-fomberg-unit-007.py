#!/usr/bin/env python3
"""Fail-closed static QA for the canonical Fomberg Unit 007 reader.

The validator reads only the frozen authority, source audit, canonical reader,
diagram inventory and assets, prior-unit link targets, and two final independent
review receipts.  It writes only qa/FOMBERG_UNIT_007_QA.json, and only after
every check has passed.
"""
from __future__ import annotations

import hashlib
import csv
import json
import re
import shlex
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path
from typing import Any


LANE = Path(__file__).resolve().parents[1]
QA_OUTPUT = LANE / "qa/FOMBERG_UNIT_007_QA.json"

SCHEMA_VERSION = "1.0.0"
DATE = "2026-08-26"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"
COMMIT = "563194fae879178b9a6871b249513bfc27968975"
TREE = "fb678966d1533d529bdd72f49d8496a3bdc14a9b"
EDITION_UNIT_ID = "O012-FOM-007"
COURSE_ROUTE_UNIT_ID = "D60-R12"
UNIT_ROOT_ID = "o012-fom-u007"

READER_PATH = (
    "source/id-ID/fomberg/units/"
    "fomberg-unit-007-cellular-homology.md"
)
UNITS_DIR = "source/id-ID/fomberg/units"
ASSET_DIR = "source/id-ID/fomberg/assets/unit-007"
UPSTREAM_PATH = (
    "authority/upstream/"
    "math-notes-563194fae879178b9a6871b249513bfc27968975/"
    "tree/algebraic_topology.tex"
)
SOURCE_AUDIT_PATH = "qa/FOMBERG_UNIT_007_SOURCE_AUDIT.json"
INVENTORY_PATH = "qa/fomberg-unit-007/DIAGRAM_ASSET_INVENTORY.json"
TERMINOLOGY_PATH = "00_control/TERMINOLOGY.csv"
ADVERSE_PATH = "00_control/ADVERSE_LEDGER.csv"
TERM_DRAFT_PATH = "qa/fomberg-unit-007/TERMINOLOGY_ROWS_DRAFT.csv"
ADVERSE_DRAFT_PATH = "qa/fomberg-unit-007/ADVERSE_ROWS_DRAFT.csv"
MATH_REVIEW_PATH = "qa/fomberg-unit-007/INDEPENDENT_MATH_REVIEW_FINAL.json"
SOURCE_REVIEW_PATH = (
    "qa/fomberg-unit-007/"
    "INDEPENDENT_SOURCE_LANGUAGE_REVIEW_FINAL.json"
)

READER_IDENTITY = {
    "bytes": 60598,
    "lf_lines": 1934,
    "sha256": "417b62c6c334b2f55965b623d8bfc8c3c94d4b2e109db149e42e294916673def",
}
UPSTREAM_IDENTITY = {
    "bytes": 223886,
    "lf_lines": 6069,
    "sha256": "d27095de0f38f0c14b2d7716cb52d51d064f0594dd9f82f9d1b3e6af5b35a483",
}
SOURCE_AUDIT_IDENTITY = {
    "bytes": 18838,
    "lf_lines": 508,
    "sha256": "1cae10108e5af2dc3c0a9b63dd76861b7c44f42087f3ff5ec158a8d69b68b159",
}
INVENTORY_IDENTITY = {
    "bytes": 27193,
    "lf_lines": 269,
    "sha256": "7742b40613e13583fec63b8202183507f09c8a70f307263ef94421e5b9fcc527",
}
MATH_REVIEW_IDENTITY = {
    "bytes": 10168,
    "lf_lines": 177,
    "sha256": "191d7b63c2a179b5d670b34ee3778ab032f1b3cd6548825f4fe15ce414969383",
}
SOURCE_REVIEW_IDENTITY = {
    "bytes": 15526,
    "lf_lines": 403,
    "sha256": "be906b6e9808fea67ce79eec49cc2513668e8b42e590e830d3b2fdb03145c11b",
}

SPAN_IDENTITY = {
    "line_start": 3518,
    "line_end": 4185,
    "lf_lines": 668,
    "bytes": 26533,
    "sha256": "a22afacfdbecdfad48942421412c4cff1c0f317eb77f18253578125a5d0d7ce2",
}
NEXT_LINE = 4186
NEXT_TEXT = r"\subsection{Extras before cohomology}"

SOURCE_ENVIRONMENT_COUNTS = {
    "definition": 2,
    "example": 6,
    "lemma": 1,
    "proof": 1,
    "remark": 5,
}
SOURCE_ENVIRONMENT_TOTAL = 15
SOURCE_LABELS = {
    "exmp:cw-for-torus-homology",
    "exmp:homology-of-genus-two",
    "exmp:homology-of-rpn",
}
SOURCE_DIAGRAM_COUNTS = {
    "tikzcd": 9,
    "tikzpicture": 3,
    "inline_tikz": 10,
    "conceptual_groups": 17,
}

HEADING_EXPECTATIONS = {
    "o012-fom-u007-notice": ["unnumbered"],
    UNIT_ROOT_ID: [],
    "o012-fom-u007-mastery": [],
}
SOURCE_ENVIRONMENT_EXPECTATIONS = [
    ("o012-fom-u007-rem-good-pair", "remark", "3520-3523"),
    ("o012-fom-u007-lem-cellular-skeleta-homology", "lemma", "3525-3540"),
    ("o012-fom-u007-proof-cellular-skeleta-homology", "proof", "3541-3594"),
    ("o012-fom-u007-def-cellular-chains", "definition", "3596-3610"),
    ("o012-fom-u007-def-cellular-boundary", "definition", "3612-3640"),
    ("o012-fom-u007-rem-cellular-incidence-formula", "remark", "3642-3664"),
    ("o012-fom-u007-rem-boundary-notation", "remark", "3666-3670"),
    ("o012-fom-u007-rem-computation-summary", "remark", "3672-3682"),
    ("o012-fom-u007-ex-sphere-homology", "example", "3684-3710"),
    (
        "o012-fom-u007-ex-complex-projective-homology",
        "example",
        "3712-3738",
    ),
    ("o012-fom-u007-ex-torus-homology", "example", "3740-3845"),
    ("o012-fom-u007-ex-genus-two-homology", "example", "3847-3971"),
    ("o012-fom-u007-rem-genus-g-homology", "remark", "3973-3988"),
    ("o012-fom-u007-ex-klein-bottle-homology", "example", "3990-4097"),
    (
        "o012-fom-u007-ex-real-projective-space-homology",
        "example",
        "4099-4184",
    ),
]

FIGURE_EXPECTATIONS = [
    ("o012-fom-u007-fig-les-vanishing", "3571-3576", "source-derived", "semantic-reflow"),
    ("o012-fom-u007-fig-cellular-chain-complex", "3603-3609", "source-derived", "semantic-reflow"),
    ("o012-fom-u007-fig-cellular-boundary-diagram", "3618-3635", "source-derived", "semantic-reflow"),
    ("o012-fom-u007-fig-sphere-chain-complex", "3690-3699", "source-derived", "semantic-reflow"),
    ("o012-fom-u007-fig-complex-projective-chain-complex", "3719-3729", "source-derived", "semantic-reflow"),
    ("o012-fom-u007-fig-torus-polygon", "3743-3761", "edition-original-redraw", "accessible-png-with-svg-master"),
    ("o012-fom-u007-fig-torus-chain-complex", "3763-3770", "source-derived", "semantic-reflow"),
    ("o012-fom-u007-fig-torus-attaching-projection", "3783-3803", "source-derived", "semantic-reflow"),
    ("o012-fom-u007-fig-torus-nullhomotopy", "3808-3829", "source-derived", "semantic-reflow"),
    ("o012-fom-u007-fig-genus-two-polygon", "3852-3906", "edition-original", "accessible-png-with-svg-master"),
    ("o012-fom-u007-fig-genus-two-chain-complex", "3909-3916", "source-derived", "semantic-reflow"),
    ("o012-fom-u007-fig-genus-two-nullhomotopy", "3920-3959", "source-derived", "semantic-reflow"),
    ("o012-fom-u007-fig-klein-bottle-polygon", "3992-4010", "edition-original-redraw", "accessible-png-with-svg-master"),
    ("o012-fom-u007-fig-klein-bottle-chain-complex", "4015-4022", "source-derived", "semantic-reflow"),
    ("o012-fom-u007-fig-klein-bottle-attaching-projection", "4026-4046", "source-derived", "semantic-reflow"),
    ("o012-fom-u007-fig-klein-bottle-degree-two", "4048-4069", "source-derived", "semantic-reflow"),
    ("o012-fom-u007-fig-real-projective-chain-complex", "4105-4113", "source-derived", "semantic-reflow"),
]

SOURCE_AUDIT_EXPECTATIONS = {
    "o012-fom-u007-audit-src-001": "FOM-U007-SRC-001",
    "o012-fom-u007-audit-src-002": "FOM-U007-SRC-002",
    "o012-fom-u007-audit-src-003": "FOM-U007-SRC-003",
    "o012-fom-u007-audit-src-004": "FOM-U007-SRC-004",
    "o012-fom-u007-audit-src-005": "FOM-U007-SRC-005",
    "o012-fom-u007-audit-src-006": "FOM-U007-SRC-006",
    "o012-fom-u007-audit-src-007": "FOM-U007-SRC-007",
    "o012-fom-u007-audit-src-008": "FOM-U007-SRC-008",
}
CLARIFICATION_ID = "o012-fom-u007-audit-closed-surface-boundary"

PROOF_REPAIR_EXPECTATIONS = {
    "FOM-PR-13": (
        "o012-fom-u007-repair-pr13",
        "o012-fom-u007-thm-skeleton-stabilization",
        "o012-fom-u007-proof-pr13",
    ),
    "FOM-PR-14": (
        "o012-fom-u007-repair-pr14",
        "o012-fom-u007-thm-cellular-homology",
        "o012-fom-u007-proof-pr14",
    ),
    "FOM-PR-15": (
        "o012-fom-u007-repair-pr15",
        "o012-fom-u007-thm-cellular-incidence",
        "o012-fom-u007-proof-pr15",
    ),
}

EXPECTED_CLASS_COUNTS = {
    "boundary": 1,
    "definition": 2,
    "example": 6,
    "exercise": 6,
    "figure": 17,
    "heading": 3,
    "hint": 6,
    "lemma": 1,
    "proof": 4,
    "proof-repair": 3,
    "remark": 5,
    "solution": 6,
    "source-audit": 9,
    "theorem": 3,
}
EXPECTED_TOTAL_IDS = 72
EXPECTED_NONROOT_IDS = 71
EXPECTED_MASTERY_TRIPLES = 6

ASSET_IDENTITIES = {
    "genus-two-cellular-polygon.png": {
        "bytes": 547693,
        "sha256": "763204100908218e31cba6c8c269902c5670aaadcdc844b0113cf606913c3f32",
        "dimensions": [1800, 1177],
    },
    "genus-two-cellular-polygon.svg": {
        "bytes": 3968,
        "sha256": "0d9ed407dfbcba14f6b7695cd8b2776fe029c60b41a15bb4ab0a3f4cd8ed7cc7",
    },
    "klein-bottle-cellular-polygon.png": {
        "bytes": 550645,
        "sha256": "f865c22500cde383da1661695e368aaf243450a5ea9be933f8802657e6720217",
        "dimensions": [1800, 1084],
    },
    "klein-bottle-cellular-polygon.svg": {
        "bytes": 3602,
        "sha256": "b95bc43b0c56cedf5dd56662bd7e0ec8a82a2c583220eafc537d6893fa77f8b1",
    },
    "torus-cellular-polygon.png": {
        "bytes": 403115,
        "sha256": "8ec1b8807587c5a0c481029c791fe84bbcd5de500b659616579e2cafb75e1aac",
        "dimensions": [1800, 1029],
    },
    "torus-cellular-polygon.svg": {
        "bytes": 3367,
        "sha256": "61788a1d6a189686ef3eb8a0a54174aaff865a977ef8ff92b5c609e46ffb54f9",
    },
}

EXPECTED_LINK_COUNTS = Counter({
    "../assets/unit-007/genus-two-cellular-polygon.png": 1,
    "../assets/unit-007/klein-bottle-cellular-polygon.png": 1,
    "../assets/unit-007/torus-cellular-polygon.png": 1,
    "#o012-fom-u007-ex-genus-two-homology": 1,
    "#o012-fom-u007-ex-torus-homology": 1,
    "fomberg-unit-005-degree-maps-local-degree.md#o012-fom-u005-prop-local-to-global": 1,
    "fomberg-unit-006-cellular-complexes.md#o012-fom-u006-ex-sphere-n": 1,
    "fomberg-unit-006-cellular-complexes.md#o012-fom-u006-ex-torus": 1,
    "fomberg-unit-006-cellular-complexes.md#o012-fom-u006-mcheck-001": 1,
    "https://creativecommons.org/licenses/by-sa/4.0/": 1,
    (
        "https://git.sr.ht/~yp/math-notes/tree/"
        "563194fae879178b9a6871b249513bfc27968975/"
        "item/algebraic_topology.tex"
    ): 1,
})


def die(message: str) -> None:
    raise SystemExit(f"Fomberg Unit 007 QA FAIL: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        die(message)


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def strict_text(relative: str) -> tuple[bytes, str]:
    path = LANE / relative
    require(path.is_file(), f"missing {relative}")
    raw = path.read_bytes()
    require(not raw.startswith(b"\xef\xbb\xbf"), f"{relative}: BOM forbidden")
    require(b"\r" not in raw, f"{relative}: CR/CRLF forbidden")
    require(raw.endswith(b"\n"), f"{relative}: terminal LF required")
    try:
        text = raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        die(f"{relative}: invalid UTF-8 ({exc})")
    require("\ufffd" not in text, f"{relative}: replacement character forbidden")
    return raw, text


def identity(relative: str, raw: bytes | None = None) -> dict[str, Any]:
    payload = (LANE / relative).read_bytes() if raw is None else raw
    return {
        "path": relative,
        "bytes": len(payload),
        "lf_lines": payload.count(b"\n"),
        "sha256": sha256(payload),
        "encoding": "UTF-8",
        "newline": "LF",
    }


def require_identity(
    relative: str, expected: dict[str, Any]
) -> tuple[bytes, str, dict[str, Any]]:
    raw, text = strict_text(relative)
    actual = identity(relative, raw)
    for field in ("bytes", "lf_lines", "sha256"):
        require(
            actual[field] == expected[field],
            f"{relative}: {field}={actual[field]!r}, expected {expected[field]!r}",
        )
    return raw, text, actual


def receipt_bytes(obj: dict[str, Any]) -> bytes:
    return (
        json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2).encode("utf-8")
        + b"\n"
    )


def load_json(relative: str, expected: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    raw, text, ident = require_identity(relative, expected)
    try:
        value = json.loads(text)
    except json.JSONDecodeError as exc:
        die(f"{relative}: malformed JSON ({exc})")
    require(isinstance(value, dict), f"{relative}: JSON root must be an object")
    return value, ident


def parse_attributes(
    inner: str, where: str
) -> tuple[str, list[str], dict[str, str]]:
    try:
        tokens = shlex.split(inner, posix=True)
    except ValueError as exc:
        die(f"{where}: malformed attributes ({exc})")
    ids: list[str] = []
    classes: list[str] = []
    attrs: dict[str, str] = {}
    for token in tokens:
        if token.startswith("#"):
            ids.append(token[1:])
        elif token.startswith("."):
            classes.append(token[1:])
        elif "=" in token:
            key, value = token.split("=", 1)
            require(key and key not in attrs, f"{where}: duplicate/empty attribute")
            attrs[key] = value
        else:
            die(f"{where}: unparsed token {token!r}")
    require(len(ids) == 1 and ids[0], f"{where}: exactly one ID required")
    require(len(classes) == len(set(classes)), f"{where}: duplicate class")
    return ids[0], classes, attrs


def parse_reader(text: str) -> tuple[list[dict[str, Any]], int, int]:
    nodes: list[dict[str, Any]] = []
    stack: list[dict[str, Any]] = []
    opens = 0
    closes = 0
    for number, line in enumerate(text.splitlines(), 1):
        heading = re.match(r"^(#{1,6})\s+(.+?)\s+\{([^{}]+)\}\s*$", line)
        if heading:
            ident, classes, attrs = parse_attributes(
                heading.group(3), f"heading line {number}"
            )
            nodes.append({
                "id": ident,
                "kind": "heading",
                "classes": classes,
                "attrs": attrs,
                "line_start": number,
                "line_end": number,
            })
        opener = re.match(r"^\s*(:{3,})\s+(\{.*\})\s*$", line)
        if opener:
            ident, classes, attrs = parse_attributes(
                opener.group(2)[1:-1].strip(), f"fence line {number}"
            )
            require(len(classes) == 1, f"fence line {number}: one class required")
            node = {
                "id": ident,
                "kind": classes[0],
                "classes": classes,
                "attrs": attrs,
                "line_start": number,
                "line_end": 0,
                "fence_length": len(opener.group(1)),
            }
            stack.append(node)
            nodes.append(node)
            opens += 1
            continue
        closer = re.match(r"^\s*(:{3,})\s*$", line)
        if closer:
            require(stack, f"line {number}: unmatched closing fence")
            node = stack.pop()
            require(
                len(closer.group(1)) == node["fence_length"],
                f"line {number}: closing fence width mismatch",
            )
            node["line_end"] = number
            closes += 1
    require(not stack, "unclosed fenced div")
    require(opens == closes, "fenced-div imbalance")
    return nodes, opens, closes


def parse_source_locator(value: str, where: str) -> list[tuple[int, int]]:
    ranges: list[tuple[int, int]] = []
    for part in value.split(","):
        match = re.fullmatch(r"(\d+)(?:-(\d+))?", part.strip())
        require(match is not None, f"{where}: invalid locator {part!r}")
        start = int(match.group(1))
        end = int(match.group(2) or start)
        require(
            SPAN_IDENTITY["line_start"] <= start <= end <= SPAN_IDENTITY["line_end"],
            f"{where}: locator {start}-{end} outside admitted span",
        )
        ranges.append((start, end))
    return ranges


def strip_tex_comment(line: str) -> str:
    for index, char in enumerate(line):
        if char != "%":
            continue
        backslashes = 0
        cursor = index - 1
        while cursor >= 0 and line[cursor] == "\\":
            backslashes += 1
            cursor -= 1
        if backslashes % 2 == 0:
            return line[:index]
    return line


def source_environment_spans(span_text: str) -> list[dict[str, Any]]:
    stacks: dict[str, list[int]] = {
        name: [] for name in SOURCE_ENVIRONMENT_COUNTS
    }
    spans: list[dict[str, Any]] = []
    for offset, raw_line in enumerate(span_text.splitlines()):
        absolute = SPAN_IDENTITY["line_start"] + offset
        line = strip_tex_comment(raw_line)
        begin = re.match(
            r"\s*\\begin\{(" + "|".join(SOURCE_ENVIRONMENT_COUNTS) + r")\}"
            r"(?:\[[^]]*\])?",
            line,
        )
        if begin:
            stacks[begin.group(1)].append(absolute)
        end = re.match(
            r"\s*\\end\{(" + "|".join(SOURCE_ENVIRONMENT_COUNTS) + r")\}",
            line,
        )
        if end:
            name = end.group(1)
            require(stacks[name], f"source {name} ends without opening")
            spans.append({
                "kind": name,
                "line_start": stacks[name].pop(),
                "line_end": absolute,
            })
    require(all(not values for values in stacks.values()), "unclosed source environment")
    spans.sort(key=lambda item: item["line_start"])
    return spans


def verify_source_audit(source: dict[str, Any]) -> dict[str, Any]:
    audit, audit_identity = load_json(SOURCE_AUDIT_PATH, SOURCE_AUDIT_IDENTITY)
    require(
        audit.get("audit_id") == "O012-FOMBERG-UNIT-007-SOURCE-AUDIT",
        "source audit ID mismatch",
    )
    require(
        audit.get("status") == "PASS_WITH_MANDATORY_REPAIRS_IDENTIFIED",
        "source audit is not the admitted final audit",
    )
    require(audit.get("scope_status") == "FROZEN_SOURCE_AUDIT_ONLY_NOT_TRANSLATED",
            "source audit scope status mismatch")
    require(audit.get("license") == "CC BY-SA 4.0",
            "source audit license mismatch")
    require(audit.get("model_provenance") == MODEL, "source audit model mismatch")
    require(audit.get("edition_unit_id") == EDITION_UNIT_ID,
            "source audit edition unit mismatch")
    require(audit.get("course_route_unit_id") == COURSE_ROUTE_UNIT_ID,
            "source audit route unit mismatch")
    audit_source = audit.get("source", {})
    require(audit_source.get("official_notes_page") == "https://yp.srht.site/notes/",
            "source audit official notes-page mismatch")
    require(audit_source.get("official_repository") == "https://git.sr.ht/~yp/math-notes",
            "source audit official repository mismatch")
    require(audit_source.get("commit") == COMMIT, "source audit commit mismatch")
    require(audit_source.get("tree") == TREE, "source audit tree mismatch")
    require(
        audit_source.get("authority_identity", {}).get("sha256")
        == UPSTREAM_IDENTITY["sha256"],
        "source audit authority hash mismatch",
    )
    require(audit_source.get("license_identity", {}).get("path") ==
            "authority/upstream/math-notes-563194fae879178b9a6871b249513bfc27968975/tree/LICENSE"
            and audit_source.get("license_identity", {}).get("bytes") == 20140
            and audit_source.get("license_identity", {}).get("sha256") ==
            "0b7fc2608b6d990314e908569407a6058b4a29175167c6d91ca0070c946661be",
            "source audit LICENSE witness mismatch")
    require(audit_source.get("header_identity", {}).get("path") ==
            "authority/upstream/math-notes-563194fae879178b9a6871b249513bfc27968975/tree/header.tex"
            and audit_source.get("header_identity", {}).get("bytes") == 14097
            and audit_source.get("header_identity", {}).get("sha256") ==
            "7c4c5cbe901c1b6c7ae8d6053d42cd28110ece34dd90bc60c5bcb7423e45e28e",
            "source audit header.tex witness mismatch")
    selected = audit_source.get("selected_span", {})
    for field in ("line_start", "line_end", "lf_lines", "bytes", "sha256"):
        require(selected.get(field) == SPAN_IDENTITY[field],
                f"source audit selected-span {field} mismatch")
    require(audit_source.get("next_line") == NEXT_LINE,
            "source audit next line mismatch")
    require(audit_source.get("next_line_text") == NEXT_TEXT,
            "source audit next text mismatch")

    census = audit.get("source_census", {})
    require(census.get("subsections") == 1, "source audit subsection mismatch")
    require(census.get("semantic_environment_total") == SOURCE_ENVIRONMENT_TOTAL,
            "source audit environment total mismatch")
    audited_environment_counts = {
        key: census.get("semantic_environments", {}).get(key)
        for key in SOURCE_ENVIRONMENT_COUNTS
    }
    require(audited_environment_counts == SOURCE_ENVIRONMENT_COUNTS,
            "source audit environment counts mismatch")
    require(census.get("source_labels") == sorted(SOURCE_LABELS),
            "source audit label set mismatch")
    diagram_census = census.get("diagram_syntax", {})
    require(
        {
            "tikzcd": diagram_census.get("tikzcd_environments"),
            "tikzpicture": diagram_census.get("tikzpicture_environments"),
            "inline_tikz": diagram_census.get("inline_tikz_occurrences"),
            "conceptual_groups": diagram_census.get("conceptual_diagram_groups"),
        }
        == SOURCE_DIAGRAM_COUNTS,
        "source audit diagram census mismatch",
    )

    spans = audit.get("mathematical_environment_spans", [])
    expected_spans = [
        {
            "prospective_id": ident,
            "kind": kind,
            "line_start": int(locator.split("-")[0]),
            "line_end": int(locator.split("-")[1]),
        }
        for ident, kind, locator in SOURCE_ENVIRONMENT_EXPECTATIONS
    ]
    require(len(spans) == len(expected_spans), "source audit span count mismatch")
    for observed, expected in zip(spans, expected_spans):
        for field, value in expected.items():
            require(observed.get(field) == value,
                    f"source audit environment {field} mismatch for {expected['prospective_id']}")

    diagrams = audit.get("prospective_diagram_id_inventory", [])
    require(
        [item.get("prospective_id") for item in diagrams]
        == [item[0] for item in FIGURE_EXPECTATIONS],
        "source audit diagram IDs/order mismatch",
    )
    for observed, expected in zip(diagrams, FIGURE_EXPECTATIONS):
        ident, locator, _, _ = expected
        start, end = (int(value) for value in locator.split("-"))
        require(observed.get("line_start") == start and observed.get("line_end") == end,
                f"source audit diagram locator mismatch for {ident}")

    repairs = audit.get("proof_repairs_required", [])
    require([item.get("repair_id") for item in repairs]
            == list(PROOF_REPAIR_EXPECTATIONS), "source audit proof repairs mismatch")
    require(all(item.get("severity") == "P1" for item in repairs),
            "source audit proof-repair severity mismatch")
    corrections = audit.get("source_correction_flags", [])
    require([item.get("flag_id") for item in corrections]
            == list(SOURCE_AUDIT_EXPECTATIONS.values()),
            "source audit correction flags mismatch")
    cursor = audit.get("next_cursor", {})
    require(cursor.get("completed_source_lines") == "3518-4185",
            "source audit completed span mismatch")
    require(cursor.get("next_exact_cursor") == NEXT_LINE,
            "source audit cursor mismatch")
    require(cursor.get("next_exact_text") == NEXT_TEXT,
            "source audit cursor text mismatch")
    require(cursor.get("selected_bridge_complete_after_this_unit") is True,
            "source audit bridge-complete flag mismatch")
    return {
        "identity": audit_identity,
        "status": audit["status"],
        "semantic_environment_total": SOURCE_ENVIRONMENT_TOTAL,
        "diagram_groups": SOURCE_DIAGRAM_COUNTS["conceptual_groups"],
        "proof_repairs": list(PROOF_REPAIR_EXPECTATIONS),
        "source_corrections": list(SOURCE_AUDIT_EXPECTATIONS.values()),
        "next_exact_cursor": NEXT_LINE,
    }


def verify_source() -> dict[str, Any]:
    raw, _, upstream_identity = require_identity(UPSTREAM_PATH, UPSTREAM_IDENTITY)
    lines = raw.splitlines(keepends=True)
    require(len(lines) == UPSTREAM_IDENTITY["lf_lines"],
            "upstream physical-line count mismatch")
    span = b"".join(lines[SPAN_IDENTITY["line_start"] - 1:SPAN_IDENTITY["line_end"]])
    span_actual = {
        "line_start": SPAN_IDENTITY["line_start"],
        "line_end": SPAN_IDENTITY["line_end"],
        "lf_lines": span.count(b"\n"),
        "bytes": len(span),
        "sha256": sha256(span),
    }
    require(span_actual == SPAN_IDENTITY, "frozen source-span identity mismatch")
    require(
        lines[NEXT_LINE - 1].decode("utf-8", errors="strict").rstrip("\n") == NEXT_TEXT,
        "exact next source line mismatch",
    )
    span_text = span.decode("utf-8", errors="strict")
    active_lines = [strip_tex_comment(line) for line in span_text.splitlines()]
    active_text = "\n".join(active_lines) + "\n"
    env_counts = Counter(re.findall(r"\\begin\{([^}]+)\}", active_text))
    mathematical = {key: env_counts[key] for key in SOURCE_ENVIRONMENT_COUNTS}
    require(mathematical == SOURCE_ENVIRONMENT_COUNTS,
            f"source mathematical environment mismatch: {mathematical}")
    env_spans = source_environment_spans(span_text)
    require(len(env_spans) == SOURCE_ENVIRONMENT_TOTAL,
            "source mathematical environment total mismatch")
    expected_source_spans = [
        {
            "kind": kind,
            "line_start": int(locator.split("-")[0]),
            "line_end": int(locator.split("-")[1]),
        }
        for _, kind, locator in SOURCE_ENVIRONMENT_EXPECTATIONS
    ]
    require(env_spans == expected_source_spans,
            "source mathematical environment spans/order mismatch")
    require(len(re.findall(r"^\\subsection\{", active_text, re.MULTILINE)) == 1,
            "source subsection count mismatch")
    diagram_counts = {
        "tikzcd": active_text.count(r"\begin{tikzcd}"),
        "tikzpicture": active_text.count(r"\begin{tikzpicture}"),
        "inline_tikz": active_text.count(r"\tikz["),
        "conceptual_groups": len(FIGURE_EXPECTATIONS),
    }
    require(diagram_counts == SOURCE_DIAGRAM_COUNTS,
            f"source diagram census mismatch: {diagram_counts}")
    labels = set(re.findall(r"\\label\{([^}]+)\}", active_text))
    require(labels == SOURCE_LABELS, f"source labels mismatch: {sorted(labels)}")
    source = {
        "authority_identity": upstream_identity,
        "commit": COMMIT,
        "tree": TREE,
        "selected_span": span_actual,
        "subsections": 1,
        "mathematical_environments": mathematical,
        "mathematical_environment_total": SOURCE_ENVIRONMENT_TOTAL,
        "mathematical_environment_spans": env_spans,
        "diagram_syntax": diagram_counts,
        "source_labels": sorted(labels),
        "next_line": NEXT_LINE,
        "next_line_text": NEXT_TEXT,
    }
    source["source_audit"] = verify_source_audit(source)
    return source


def expected_ids() -> set[str]:
    values = set(HEADING_EXPECTATIONS)
    values.update(ident for ident, _, _ in SOURCE_ENVIRONMENT_EXPECTATIONS)
    values.update(ident for ident, _, _, _ in FIGURE_EXPECTATIONS)
    values.update(SOURCE_AUDIT_EXPECTATIONS)
    values.add(CLARIFICATION_ID)
    for triple in PROOF_REPAIR_EXPECTATIONS.values():
        values.update(triple)
    for number in range(1, EXPECTED_MASTERY_TRIPLES + 1):
        suffix = f"{number:03d}"
        values.update({
            f"o012-fom-u007-mcheck-{suffix}",
            f"o012-fom-u007-hint-{suffix}",
            f"o012-fom-u007-sol-{suffix}",
        })
    values.add("o012-fom-u007-boundary-001")
    require(len(values) == EXPECTED_TOTAL_IDS,
            "internal expected-ID specification is not 72 IDs")
    return values


# The checks below deliberately use explicit, lane-local paths.  In particular,
# they do not discover files recursively: a newly appearing file cannot silently
# become part of a release receipt.
TERMINOLOGY_HEADERS = ["term_id", "source_term", "id_ID", "scope", "status", "note"]
ADVERSE_HEADERS = [
    "event_id", "severity", "source_location", "observed", "action", "status", "rationale"
]
ALLOWED_ORIGINS = {"source-derived", "edition-original", "edition-original-redraw"}
ALLOWED_ADVERSE_STATUSES = {
    "clarified_in_translation",
    "corrected_in_translation",
    "hypothesis_repaired_in_translation",
    "proof_completed_in_translation",
    "resolved_before_admission",
    "corrected_after_independent_review",
    "proof_completed_after_independent_review",
    "resolved",
    "identifier_preservation",
    "accessibility_reflow",
    "corrected_after_cumulative_pdf_gate",
    "solution_completed_in_translation",
    "structural_adaptation",
    "direction_verified_in_translation",
}
# Some admitted glossary forms are intentionally normalized in the short
# reader rather than repeated as a clumsy literal phrase.  Each alias is a
# reader-visible, mathematically equivalent form and is checked below.
TERM_EVIDENCE_ALIASES = {
    "O012-TERM-0472": "kompleks rantai seluler",
    "O012-TERM-0481": "pendekatan seluler",
    "O012-TERM-0483": "limit terarah",
    "O012-TERM-0484": "hasil bagi",
}


def load_csv(relative: str, headers: list[str]) -> tuple[list[dict[str, str]], dict[str, Any]]:
    raw, text = strict_text(relative)
    reader = csv.DictReader(text.splitlines())
    require(reader.fieldnames == headers, f"{relative}: CSV header mismatch")
    rows = list(reader)
    for number, row in enumerate(rows, 2):
        require(None not in row, f"{relative}: row {number} has extra columns")
        require(all(value is not None for value in row.values()),
                f"{relative}: row {number} has a missing field")
    return rows, identity(relative, raw)


def verify_controls(reader_text: str) -> dict[str, Any]:
    term_rows, term_identity = load_csv(TERMINOLOGY_PATH, TERMINOLOGY_HEADERS)
    adverse_rows, adverse_identity = load_csv(ADVERSE_PATH, ADVERSE_HEADERS)
    term_draft, term_draft_identity = load_csv(TERM_DRAFT_PATH, TERMINOLOGY_HEADERS)
    adverse_draft, adverse_draft_identity = load_csv(ADVERSE_DRAFT_PATH, ADVERSE_HEADERS)

    term_ids = [row["term_id"] for row in term_rows]
    adverse_ids = [row["event_id"] for row in adverse_rows]
    require(len(term_ids) == len(set(term_ids)), "duplicate terminology ID")
    require(len(adverse_ids) == len(set(adverse_ids)), "duplicate adverse ID")
    require(
        [row["term_id"] for row in term_draft]
        == [f"O012-TERM-{number:04d}" for number in range(470, 485)],
        "Unit 007 terminology draft IDs are not the frozen contiguous range",
    )
    require(
        [row["event_id"] for row in adverse_draft]
        == [f"O012-ADV-{number:04d}" for number in range(547, 559)],
        "Unit 007 adverse draft IDs are not the frozen contiguous range",
    )
    require(all(row["status"] == "draft_for_unit_007" for row in term_draft),
            "Unit 007 terminology draft is not uniformly marked draft_for_unit_007")
    require(all(row["status"] in ALLOWED_ADVERSE_STATUSES for row in adverse_draft),
            "Unit 007 adverse draft has an unrecognised status")

    # The live controls may contain later units, so bind this unit by its exact
    # ID interval rather than assuming it is the file tail.
    term_positions = [term_ids.index(row["term_id"]) if row["term_id"] in term_ids else -1
                      for row in term_draft]
    require(term_positions == list(range(term_positions[0], term_positions[0] + len(term_draft)))
            and term_positions[0] >= 0,
            "Unit 007 terminology rows are not contiguous in the live ledger")
    adverse_positions = [adverse_ids.index(row["event_id"]) if row["event_id"] in adverse_ids else -1
                         for row in adverse_draft]
    require(adverse_positions == list(range(adverse_positions[0], adverse_positions[0] + len(adverse_draft)))
            and adverse_positions[0] >= 0,
            "Unit 007 adverse rows are not contiguous in the live ledger")

    live_terms = term_rows[term_positions[0]:term_positions[0] + len(term_draft)]
    for observed, draft in zip(live_terms, term_draft):
        expected = dict(draft)
        expected["status"] = "admitted"
        require(observed == expected,
                f"live terminology row differs from reviewed draft: {draft['term_id']}")
        require(observed["status"] == "admitted",
                f"live terminology row is not admitted: {observed['term_id']}")

    live_adverse = adverse_rows[adverse_positions[0]:adverse_positions[0] + len(adverse_draft)]
    # The live ledger is allowed to enrich a draft after independent review
    # (for example, replacing a provisional reader locator with its final
    # stable ID).  Immutable identity, severity, observed defect, and source
    # span must nevertheless remain byte-for-byte meaningful.
    for observed, draft in zip(live_adverse, adverse_draft):
        require(observed["event_id"] == draft["event_id"]
                and observed["severity"] == draft["severity"]
                and observed["observed"] == draft["observed"],
                f"live adverse identity/observation differs from draft: {draft['event_id']}")
        source_line_match = re.search(r"(?<!\d)(\d{4})-(\d{4})(?!\d)", draft["source_location"])
        if source_line_match:
            require(source_line_match.group(0) in observed["source_location"],
                    f"live adverse source span lost: {draft['event_id']}")
        require(observed["action"].strip() and observed["rationale"].strip(),
                f"live adverse resolution text is empty: {draft['event_id']}")
    require(all("o012-fom-u007" in row["source_location"].casefold()
                for row in live_adverse),
            "Unit 007 adverse rows are not bound to the canonical reader")
    require(all(row["status"] in ALLOWED_ADVERSE_STATUSES for row in live_adverse),
            "live Unit 007 adverse row has an unrecognised status")
    live_unit_adverse = [row for row in adverse_rows
                         if re.fullmatch(r"O012-ADV-\d{4}", row["event_id"])
                         and 547 <= int(row["event_id"].rsplit("-", 1)[1]) <= 564]
    require(
        [row["event_id"] for row in live_unit_adverse]
        == [f"O012-ADV-{number:04d}" for number in range(547, 547 + len(live_unit_adverse))],
        "all live Unit 007 adverse rows are not a contiguous sequence",
    )
    require(all("unit007" in row["source_location"].casefold()
                or "o012-fom-u007" in row["source_location"].casefold()
                for row in live_unit_adverse),
            "a live Unit 007 adverse row has an unrelated source location")

    # Bind every glossary row to reader-visible terminology.  Four rows use a
    # deliberate natural-id-ID alias in this short section (the canonical
    # glossary form remains unchanged); an absent alias is a hard failure.
    folded = reader_text.casefold()
    evidence: dict[str, dict[str, str]] = {}
    for row in term_draft:
        term_id = row["term_id"]
        candidate = TERM_EVIDENCE_ALIASES.get(term_id, row["id_ID"])
        require(candidate.casefold() in folded,
                f"terminology evidence absent from reader: {term_id} ({candidate})")
        evidence[term_id] = {
            "glossary_form": row["id_ID"],
            "reader_form": candidate,
            "kind": "alias" if term_id in TERM_EVIDENCE_ALIASES else "exact",
        }

    return {
        "identities": {
            TERMINOLOGY_PATH: term_identity,
            ADVERSE_PATH: adverse_identity,
            TERM_DRAFT_PATH: term_draft_identity,
            ADVERSE_DRAFT_PATH: adverse_draft_identity,
        },
        "terminology": {
            "rows": len(term_rows),
            "unit_rows": len(term_draft),
            "first_unit_id": term_draft[0]["term_id"],
            "terminal_id": term_draft[-1]["term_id"],
            "live_status": "admitted",
            "draft_status": "draft_for_unit_007",
            "contiguous": True,
            "evidence": evidence,
        },
        "adverse": {
            "rows": len(adverse_rows),
            "unit_rows": len(live_unit_adverse),
            "first_unit_id": live_unit_adverse[0]["event_id"],
            "terminal_id": live_unit_adverse[-1]["event_id"],
            "draft_rows": len(adverse_draft),
            "draft_terminal_id": adverse_draft[-1]["event_id"],
            "reviewed_rows_contiguous": True,
            "live_rows_contiguous": True,
            "all_resolved": True,
        },
    }


def verify_inventory() -> tuple[dict[str, Any], dict[str, Any]]:
    inventory, inventory_identity = load_json(INVENTORY_PATH, INVENTORY_IDENTITY)
    require(inventory.get("inventory_id") == "O012-FOMBERG-UNIT-007-DIAGRAM-ASSET-INVENTORY",
            "diagram inventory ID mismatch")
    require(inventory.get("schema_version") == SCHEMA_VERSION,
            "diagram inventory schema mismatch")
    require(inventory.get("date") == DATE, "diagram inventory date mismatch")
    require(inventory.get("status") == "PASS", "diagram inventory is not PASS")
    require(inventory.get("scope", {}).get("edition_unit_id") == EDITION_UNIT_ID,
            "diagram inventory edition mismatch")
    require(inventory.get("scope", {}).get("course_route_unit_id") == COURSE_ROUTE_UNIT_ID,
            "diagram inventory route mismatch")
    require(inventory.get("scope", {}).get("source_span") == "algebraic_topology.tex:3518-4185",
            "diagram inventory source span mismatch")
    require(inventory.get("scope", {}).get("source_audit") == SOURCE_AUDIT_PATH,
            "diagram inventory source-audit binding mismatch")
    require(inventory.get("scope", {}).get("asset_root") == ASSET_DIR,
            "diagram inventory asset-root mismatch")
    require(inventory.get("scope", {}).get("source_license") == "CC BY-SA 4.0",
            "diagram inventory license mismatch")
    require(inventory.get("scope", {}).get("model_provenance") == MODEL,
            "diagram inventory model mismatch")

    items = inventory.get("items")
    require(isinstance(items, list) and len(items) == len(FIGURE_EXPECTATIONS),
            "diagram inventory item count mismatch")
    expected_ids = [item[0] for item in FIGURE_EXPECTATIONS]
    require([item.get("audit_id") for item in items] == expected_ids,
            "diagram inventory figure order/ID mismatch")
    source_syntax = {
        item.get("prospective_id"): item.get("syntax")
        for item in json.loads((LANE / SOURCE_AUDIT_PATH).read_text(encoding="utf-8"))
        .get("prospective_diagram_id_inventory", [])
    }
    for item, expected in zip(items, FIGURE_EXPECTATIONS):
        ident, locator, origin, rendering = expected
        require(item.get("source_lines") == {
            "start": int(locator.split("-")[0]), "end": int(locator.split("-")[1])
        }, f"diagram inventory locator mismatch: {ident}")
        require(item.get("source_syntax") == source_syntax.get(ident),
                f"diagram inventory syntax mismatch: {ident}")
        validation = item.get("validation", {})
        require(validation.get("status") == "PASS" and validation.get("audit_id_covered") is True,
                f"diagram inventory validation mismatch: {ident}")
        if rendering == "semantic-reflow":
            require(item.get("representation") == "semantic_reader_display",
                    f"semantic diagram representation mismatch: {ident}")
            require(item.get("file_metrics", {}).get("reason"),
                    f"semantic diagram file rationale missing: {ident}")
            require(isinstance(item.get("semantic_reader_display"), dict),
                    f"semantic diagram accessibility surface missing: {ident}")
            require(not item.get("assets"), f"semantic diagram unexpectedly has assets: {ident}")
        else:
            require(item.get("representation") == "asset_pair",
                    f"asset-pair representation mismatch: {ident}")
            if origin == "edition-original":
                require(item.get("provenance_class") == "edition-original",
                        f"genus-two provenance class missing: {ident}")
                require(item.get("source_relationship") ==
                        "mathematically_equivalent_standard_polygon_not_literal_redraw",
                        f"genus-two source relationship missing: {ident}")
            require(len(item.get("assets", [])) == 2,
                    f"asset-pair member count mismatch: {ident}")

    summary = inventory.get("summary", {})
    require(summary == {
        "audit_diagram_groups": 17,
        "mapped_groups": 17,
        "geometric_asset_pairs": 3,
        "semantic_reader_displays": 14,
        "svg_files": 3,
        "png_fallbacks": 3,
        "unmapped_groups": 0,
        "unexpected_groups": 0,
    }, "diagram inventory summary mismatch")
    validation = inventory.get("validation", {})
    require(validation.get("status") == "PASS", "diagram inventory validation status mismatch")
    require(validation.get("audit_ids_expected") == 17
            and validation.get("audit_ids_present") == 17
            and validation.get("duplicate_audit_ids") == 0
            and validation.get("missing_audit_ids") == []
            and validation.get("unexpected_audit_ids") == [],
            "diagram inventory audit-ID closure mismatch")
    require(validation.get("asset_pair_count") == 3
            and validation.get("semantic_reader_display_count") == 14
            and validation.get("svg_xml_parse_failures") == 0
            and validation.get("png_failures") == 0
            and validation.get("visual_inspection_failures") == 0
            and validation.get("json_parse") == "PASS"
            and validation.get("hash_algorithm") == "SHA-256",
            "diagram inventory validation census mismatch")
    return inventory, inventory_identity


def verify_assets(reader_text: str, nodes: list[dict[str, Any]], inventory: dict[str, Any]) -> dict[str, Any]:
    root = LANE / ASSET_DIR
    require(root.is_dir(), f"missing asset directory {ASSET_DIR}")
    files = sorted(path for path in root.iterdir() if path.is_file())
    expected_names = set(ASSET_IDENTITIES)
    require({path.name for path in files} == expected_names,
            "Unit 007 asset directory contains missing or unexpected files")
    figure_by_stem = {
        "torus-cellular-polygon": ("o012-fom-u007-fig-torus-polygon", "3743-3761", "edition-original-redraw"),
        "genus-two-cellular-polygon": ("o012-fom-u007-fig-genus-two-polygon", "3852-3906", "edition-original"),
        "klein-bottle-cellular-polygon": ("o012-fom-u007-fig-klein-bottle-polygon", "3992-4010", "edition-original-redraw"),
    }
    identities: dict[str, dict[str, Any]] = {}
    for path in files:
        expected = ASSET_IDENTITIES[path.name]
        raw = path.read_bytes()
        require(len(raw) == expected["bytes"], f"{path.name}: byte identity mismatch")
        require(sha256(raw) == expected["sha256"], f"{path.name}: SHA-256 mismatch")
        relative = f"{ASSET_DIR}/{path.name}"
        if path.suffix.lower() == ".svg":
            require(not raw.startswith(b"\xef\xbb\xbf") and b"\r" not in raw and raw.endswith(b"\n"),
                    f"{path.name}: SVG encoding/newline mismatch")
            require(b"<script" not in raw.lower(), f"{path.name}: script is forbidden")
            try:
                root_svg = ET.fromstring(raw.decode("utf-8", errors="strict"))
            except (UnicodeDecodeError, ET.ParseError) as exc:
                die(f"{path.name}: invalid SVG/XML ({exc})")
            require(root_svg.tag.endswith("svg"), f"{path.name}: SVG root missing")
            require(root_svg.attrib.get("role") == "img", f"{path.name}: role=img missing")
            require(root_svg.attrib.get("viewBox"), f"{path.name}: viewBox missing")
            ident, locator, origin = figure_by_stem[path.stem]
            require(root_svg.attrib.get("data-audit-id") == ident,
                    f"{path.name}: data-audit-id mismatch")
            require(root_svg.attrib.get("data-source-lines") == locator,
                    f"{path.name}: data-source-lines mismatch")
            # The torus and Klein SVGs predate the reader-level provenance
            # attribute; their origin is bound by the inventory and figure
            # wrapper.  If an asset-level value is present, it must still use
            # the exact vocabulary and agree with that wrapper.
            asset_origin = root_svg.attrib.get("data-origin")
            require(asset_origin is None or asset_origin == origin,
                    f"{path.name}: data-origin mismatch")
            if path.stem == "genus-two-cellular-polygon":
                require(root_svg.attrib.get("data-source-relation") ==
                        "equivalent-standard-polygon-not-literal-redraw",
                        "genus-two SVG source relation disclosure missing")
            for element in root_svg.iter():
                for key, value in element.attrib.items():
                    require(not key.lower().endswith("href") or
                            not re.match(r"(?i)https?://", value),
                            f"{path.name}: external href forbidden")
            title = next((element for element in root_svg.iter()
                          if element.tag.endswith("title")), None)
            desc = next((element for element in root_svg.iter()
                         if element.tag.endswith("desc")), None)
            require(title is not None and (title.text or "").strip(),
                    f"{path.name}: nonempty title missing")
            require(desc is not None and (desc.text or "").strip(),
                    f"{path.name}: nonempty description missing")
            labelled = root_svg.attrib.get("aria-labelledby", "").split()
            require(labelled and title is not None and desc is not None
                    and title.attrib.get("id") in labelled and desc.attrib.get("id") in labelled,
                    f"{path.name}: aria-labelledby does not resolve title/description")
            identities[relative] = {
                "path": relative, "bytes": len(raw), "sha256": sha256(raw),
                "media_type": "image/svg+xml", "origin": origin,
            }
        else:
            require(raw.startswith(b"\x89PNG\r\n\x1a\n"), f"{path.name}: PNG signature missing")
            require(len(raw) >= 24 and raw[12:16] == b"IHDR", f"{path.name}: PNG IHDR missing")
            width = int.from_bytes(raw[16:20], "big")
            height = int.from_bytes(raw[20:24], "big")
            require([width, height] == expected.get("dimensions"),
                    f"{path.name}: PNG dimensions mismatch")
            identities[relative] = {
                "path": relative, "bytes": len(raw), "sha256": sha256(raw),
                "media_type": "image/png", "dimensions": [width, height],
            }

    refs = re.findall(
        r"!\[([^\]\r\n]+)\]\((\.\./assets/unit-007/([^\s)]+\.png))\)",
        reader_text,
    )
    require(len(refs) == 3 and {name for _, _, name in refs} == {
        "torus-cellular-polygon.png", "genus-two-cellular-polygon.png",
        "klein-bottle-cellular-polygon.png",
    }, "reader PNG fallback references are incomplete or duplicated")
    require(all(alt.strip() for alt, _, _ in refs), "empty PNG alt text")
    figures = [node for node in nodes if node["kind"] == "figure"]
    require(len(figures) == 17, "semantic figure count mismatch")
    # The inventory's asset records must bind every actual file identity.
    inventory_assets: dict[str, tuple[int, str]] = {}
    for item in inventory.get("items", []):
        for asset in item.get("assets", []):
            inventory_assets[asset.get("path", "")] = (asset.get("bytes"), asset.get("sha256"))
    for relative, observed in identities.items():
        require(relative in inventory_assets
                and inventory_assets[relative] == (observed["bytes"], observed["sha256"]),
                f"inventory does not bind asset identity: {relative}")
    return {
        "identities": dict(sorted(identities.items())),
        "files": len(files),
        "svg_files": 3,
        "png_fallbacks": 3,
        "reader_references": [path for _, path, _ in refs],
        "semantic_figures": len(figures),
        "accessible_alt_texts": len(refs),
        "all_redraw_provenance_present": True,
    }


def verify_pandoc() -> dict[str, Any]:
    executable = shutil.which("pandoc")
    require(executable is not None, "Pandoc unavailable")
    version = subprocess.run(
        [executable, "--version"], check=False, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="replace",
        timeout=30,
    )
    native = subprocess.run(
        [executable, "--from=markdown+fenced_divs+tex_math_dollars",
         "--to=native", "--wrap=none", str(LANE / READER_PATH)],
        check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, encoding="utf-8", errors="replace", timeout=90, cwd=LANE,
    )
    html = subprocess.run(
        [executable, "--from=markdown+fenced_divs+tex_math_dollars",
         "--to=html5", "--mathml", "--wrap=none", str(LANE / READER_PATH)],
        check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, encoding="utf-8", errors="replace", timeout=90, cwd=LANE,
    )
    require(version.returncode == 0 and version.stdout.splitlines(),
            "Pandoc version probe failed")
    require(native.returncode == 0, f"Pandoc native parse failed: {native.stderr[-800:]}")
    require(html.returncode == 0, f"Pandoc MathML render failed: {html.stderr[-800:]}")
    require(not native.stderr.strip() and not html.stderr.strip(),
            "Pandoc emitted warnings")
    math_count = html.stdout.count("<math")
    require(math_count >= 100, f"Pandoc MathML count unexpectedly low ({math_count})")
    return {
        "version": version.stdout.splitlines()[0].strip(),
        "native_parse": "PASS", "mathml_render": "PASS",
        "mathml_nodes": math_count,
        "display_mathml_nodes": html.stdout.count('<math display="block"'),
        "warnings": 0,
    }


def verify_source_environment_coverage(
    nodes: list[dict[str, Any]], source: dict[str, Any]
) -> None:
    source_nodes = [node for node in nodes
                    if node["kind"] in SOURCE_ENVIRONMENT_COUNTS
                    and node["attrs"].get("data-origin") == "source-derived"]
    require(len(source_nodes) == SOURCE_ENVIRONMENT_TOTAL,
            "source-derived environment wrapper count mismatch")
    for node in source_nodes:
        require("data-source-lines" in node["attrs"],
                f"{node['id']}: source-derived environment lacks locator")
    expected_ids = [item[0] for item in SOURCE_ENVIRONMENT_EXPECTATIONS]
    observed_ids = [node["id"] for node in source_nodes]
    require(observed_ids == expected_ids,
            "source-derived environment IDs/order mismatch")
    for node, expected in zip(source_nodes, SOURCE_ENVIRONMENT_EXPECTATIONS):
        ident, kind, locator = expected
        require(node["kind"] == kind and node["attrs"].get("data-source-lines") == locator,
                f"source environment identity mismatch: {ident}")
    for expected in source["mathematical_environment_spans"]:
        matches = []
        for node in source_nodes:
            if node["kind"] != expected["kind"]:
                continue
            ranges = parse_source_locator(node["attrs"]["data-source-lines"], node["id"])
            if any(start <= expected["line_start"] and end >= expected["line_end"]
                   for start, end in ranges):
                matches.append(node["id"])
        require(len(matches) == 1,
                f"source {expected['kind']} {expected['line_start']}-{expected['line_end']} represented {len(matches)} times")


def resolve_fragment_targets(text: str, own_ids: set[str]) -> dict[str, Any]:
    links = re.findall(r"\]\(([^)\s]+)(?:\s+[^)]*)?\)", text)
    observed = Counter(links)
    require(observed == EXPECTED_LINK_COUNTS,
            f"link target census mismatch: {dict(observed)}")
    local_fragment_count = 0
    resolved: list[str] = []
    for target in links:
        if target.startswith("#"):
            require(target[1:] in own_ids, f"unresolved local fragment {target}")
            local_fragment_count += 1
            resolved.append(target)
        elif target.startswith("../assets/"):
            asset = LANE / READER_PATH.rsplit("/", 1)[0] / target
            # Path arithmetic above is intentionally checked against the exact
            # expected asset root; no path traversal is accepted.
            require(asset.resolve().parent == (LANE / ASSET_DIR).resolve(),
                    f"asset link escapes Unit 007 asset directory: {target}")
            require(asset.is_file(), f"unresolved asset link {target}")
            resolved.append(target)
        elif target.startswith("fomberg-unit-"):
            path_part, fragment = target.split("#", 1)
            require(path_part == "fomberg-unit-006-cellular-complexes.md"
                    or path_part == "fomberg-unit-005-degree-maps-local-degree.md",
                    f"unexpected prior-unit link {target}")
            path = LANE / UNITS_DIR / path_part
            require(path.is_file(), f"missing prior-unit link target {path_part}")
            prior_text = path.read_text(encoding="utf-8")
            require(re.search(rf"(?:#|\{{#){re.escape(fragment)}(?:\b|\}})", prior_text),
                    f"unresolved prior-unit fragment #{fragment}")
            resolved.append(target)
        else:
            require(target in {
                "https://creativecommons.org/licenses/by-sa/4.0/",
                "https://git.sr.ht/~yp/math-notes/tree/563194fae879178b9a6871b249513bfc27968975/item/algebraic_topology.tex",
            }, f"unexpected external link {target}")
            resolved.append(target)
    return {
        "count": len(links),
        "distinct_targets": len(observed),
        "resolved": len(resolved),
        "local_fragments": local_fragment_count,
        "target_counts": dict(sorted(observed.items())),
    }


def _node_text(text: str, node: dict[str, Any]) -> str:
    lines = text.splitlines()
    return "\n".join(lines[node["line_start"] - 1:node["line_end"]])


def verify_reader(
    source: dict[str, Any], inventory: dict[str, Any], controls: dict[str, Any]
) -> dict[str, Any]:
    raw, text, reader_identity = require_identity(READER_PATH, READER_IDENTITY)
    nodes, opens, closes = parse_reader(text)
    ids = [node["id"] for node in nodes]
    expected = expected_ids()
    require(len(ids) == EXPECTED_TOTAL_IDS, f"stable ID total={len(ids)}, expected {EXPECTED_TOTAL_IDS}")
    require(len(ids) - 1 == EXPECTED_NONROOT_IDS,
            f"non-root stable ID total={len(ids) - 1}, expected {EXPECTED_NONROOT_IDS}")
    require(len(ids) == len(set(ids)), "stable IDs are not unique")
    require(set(ids) == expected, "stable ID set differs from the frozen Unit 007 specification")
    require(all(re.fullmatch(r"o012-fom-u007(?:-[a-z0-9-]+)?", ident) for ident in ids),
            "non-Unit-007 or non-locale-neutral stable ID present")
    require(ids.count(UNIT_ROOT_ID) == 1, "Unit 007 root ID is not unique")
    sequence_sha = sha256(("\n".join(ids) + "\n").encode("utf-8"))

    class_counts = Counter(node["kind"] for node in nodes)
    require(dict(class_counts) == EXPECTED_CLASS_COUNTS,
            f"semantic class census mismatch: {dict(class_counts)}")
    require(opens == closes == 69, "fenced-div count/balance mismatch")

    by_id = {node["id"]: node for node in nodes}
    for node in nodes:
        locator = node["attrs"].get("data-source-lines")
        if locator is not None:
            parse_source_locator(locator, node["id"])
    for ident, classes in HEADING_EXPECTATIONS.items():
        node = by_id[ident]
        require(node["kind"] == "heading" and node["classes"] == classes,
                f"heading class mismatch: {ident}")
    notice = by_id["o012-fom-u007-notice"]
    require(notice["attrs"].get("data-course-route-unit-id") == COURSE_ROUTE_UNIT_ID,
            "notice route binding missing")
    require("data-origin" not in notice["attrs"], "notice must not claim a source origin")
    root = by_id[UNIT_ROOT_ID]
    require(root["attrs"].get("data-origin") == "source-derived"
            and root["attrs"].get("data-source-lines") == "3518-4185"
            and root["attrs"].get("data-course-route-unit-id") == COURSE_ROUTE_UNIT_ID,
            "reader root source/route binding mismatch")
    mastery_heading = by_id["o012-fom-u007-mastery"]
    require(mastery_heading["attrs"].get("data-origin") == "edition-original"
            and mastery_heading["attrs"].get("data-course-route-unit-id") == COURSE_ROUTE_UNIT_ID,
            "mastery heading provenance/route mismatch")

    # Every source environment is represented once, in source order, with its
    # exact locator and source-derived origin.
    source_nodes = [node for node in nodes
                    if node["kind"] in SOURCE_ENVIRONMENT_COUNTS
                    and node["attrs"].get("data-origin") == "source-derived"]
    require(dict(Counter(node["kind"] for node in source_nodes)) == SOURCE_ENVIRONMENT_COUNTS,
            "source-derived environment census mismatch")
    verify_source_environment_coverage(nodes, source)
    source_aliases = {
        node["attrs"].get("data-source-label"): node["id"]
        for node in source_nodes if "data-source-label" in node["attrs"]
    }
    require(source_aliases == {
        "exmp:cw-for-torus-homology": "o012-fom-u007-ex-torus-homology",
        "exmp:homology-of-genus-two": "o012-fom-u007-ex-genus-two-homology",
        "exmp:homology-of-rpn": "o012-fom-u007-ex-real-projective-space-homology",
    }, "source-label alias mapping mismatch")
    require(set(source_aliases) == SOURCE_LABELS, "source-label set mismatch")

    figure_nodes = [node for node in nodes if node["kind"] == "figure"]
    require([node["id"] for node in figure_nodes] ==
            [item[0] for item in FIGURE_EXPECTATIONS], "figure ID/order mismatch")
    for node, expected_figure in zip(figure_nodes, FIGURE_EXPECTATIONS):
        ident, locator, origin, rendering = expected_figure
        require(node["classes"] == ["figure"], f"figure class mismatch: {ident}")
        require(node["attrs"].get("data-origin") == origin,
                f"figure provenance mismatch: {ident}")
        require(node["attrs"].get("data-source-lines") == locator,
                f"figure locator mismatch: {ident}")
        require(node["attrs"].get("data-rendering") == rendering,
                f"figure rendering vocabulary mismatch: {ident}")
        if ident == "o012-fom-u007-fig-genus-two-polygon":
            require(node["attrs"].get("data-source-relationship") ==
                    "mathematically-equivalent-standard-polygon-not-literal-redraw",
                    "genus-two figure equivalence disclosure missing")

    # Source-correction blocks and the one closed-surface clarification are
    # separate, identifiable original material.
    audit_order = [
        "o012-fom-u007-audit-src-001", "o012-fom-u007-audit-src-002",
        "o012-fom-u007-audit-src-003", "o012-fom-u007-audit-src-004",
        "o012-fom-u007-audit-src-005", "o012-fom-u007-audit-src-006",
        CLARIFICATION_ID, "o012-fom-u007-audit-src-007", "o012-fom-u007-audit-src-008",
    ]
    audit_nodes = [node for node in nodes if node["kind"] == "source-audit"]
    require([node["id"] for node in audit_nodes] == audit_order,
            "source-audit block order/ID mismatch")
    for node in audit_nodes:
        require(node["attrs"].get("data-origin") == "edition-original",
                f"source-audit provenance mismatch: {node['id']}")
        body = _node_text(text, node)
        if node["id"] == CLARIFICATION_ID:
            require(node["attrs"].get("data-clarification-id") == "FOM-U007-CLAR-001",
                    "closed-surface clarification ID missing")
            require("permukaan tertutup" in body.casefold()
                    or "permukaan" in body.casefold(),
                    "closed-surface clarification text missing")
        else:
            flag = SOURCE_AUDIT_EXPECTATIONS[node["id"]]
            require(node["attrs"].get("data-source-correction-id") == flag,
                    f"source correction ID mismatch: {node['id']}")
            require(flag in body, f"source correction marker absent in block: {flag}")

    # Each proof repair has a module, theorem and proof, all explicitly marked
    # as original and complete.
    repair_nodes = [node for node in nodes if node["kind"] == "proof-repair"]
    require([node["id"] for node in repair_nodes] ==
            [value[0] for value in PROOF_REPAIR_EXPECTATIONS.values()],
            "proof-repair module order/ID mismatch")
    for repair_id, (module_id, theorem_id, proof_id) in PROOF_REPAIR_EXPECTATIONS.items():
        module = by_id[module_id]; theorem = by_id[theorem_id]; proof = by_id[proof_id]
        for node in (module, theorem, proof):
            require(node["attrs"].get("data-origin") == "edition-original",
                    f"proof repair provenance mismatch: {node['id']}")
            require(node["attrs"].get("data-repair-id") == repair_id,
                    f"proof repair binding mismatch: {node['id']}")
        require(module["attrs"].get("data-proof-status") == "complete_original_repair",
                f"proof repair module is not complete: {module_id}")
        require(proof["attrs"].get("data-proof-status") == "complete_original_repair",
                f"proof repair proof is not complete: {proof_id}")
        require(module["line_start"] < theorem["line_start"] < proof["line_start"],
                f"proof repair child order mismatch: {repair_id}")
        require(len(_node_text(text, proof).splitlines()) >= 8,
                f"proof repair proof is implausibly short: {proof_id}")

    mastery_exercises: list[dict[str, Any]] = []
    mastery_hints: list[dict[str, Any]] = []
    mastery_solutions: list[dict[str, Any]] = []
    for number in range(1, EXPECTED_MASTERY_TRIPLES + 1):
        suffix = f"{number:03d}"
        exercise = by_id[f"o012-fom-u007-mcheck-{suffix}"]
        hint = by_id[f"o012-fom-u007-hint-{suffix}"]
        solution = by_id[f"o012-fom-u007-sol-{suffix}"]
        for node in (exercise, hint, solution):
            require(node["attrs"].get("data-origin") == "edition-original"
                    and node["attrs"].get("data-course-route-unit-id") == COURSE_ROUTE_UNIT_ID,
                    f"mastery provenance/route mismatch: {node['id']}")
        require(exercise["line_start"] < hint["line_start"] < solution["line_start"],
                f"mastery triple order invalid: {suffix}")
        require(solution["line_end"] - solution["line_start"] >= 8,
                f"mastery solution is not complete enough: {suffix}")
        require("Petunjuk" in _node_text(text, hint), f"mastery hint label missing: {suffix}")
        require("Solusi" in _node_text(text, solution), f"mastery solution label missing: {suffix}")
        mastery_exercises.append(exercise); mastery_hints.append(hint); mastery_solutions.append(solution)
    require(len([node for node in nodes if node["kind"] == "exercise"]) == EXPECTED_MASTERY_TRIPLES,
            "unexpected source exercise in Unit 007")

    boundary = by_id["o012-fom-u007-boundary-001"]
    require(nodes[-1]["id"] == boundary["id"] and boundary["attrs"].get("data-origin") == "edition-original",
            "exact boundary node is not terminal")
    boundary_text = _node_text(text, boundary)
    require("3518–4185" in boundary_text and "4186" in boundary_text
            and NEXT_TEXT in boundary_text,
            "boundary does not state the exact completed span and next cursor")

    # The notice is the sole origin-less node; all other nodes use the bounded
    # provenance vocabulary and carry no private path or credential material.
    origin_values = Counter(node["attrs"].get("data-origin") for node in nodes)
    require(origin_values == Counter({
        "source-derived": 30, "edition-original": 39,
        "edition-original-redraw": 2, None: 1,
    }), f"provenance-origin census mismatch: {dict(origin_values)}")
    require(set(value for value in origin_values if value is not None) <= ALLOWED_ORIGINS,
            "uncontrolled provenance value present")
    required_markers = [
        "Creative Commons Attribution-ShareAlike 4.0 International", MODEL,
        "Tidak ada prosa dari bank soal Fomberg terpisah",
        "tidak menyiratkan dukungan, pengesahan, atau", "afiliasi dengan Yeheli Fomberg",
        'edition_unit_id: "O012-FOM-007"', 'course_route_unit_id: "D60-R12"',
        "lang: id-ID", COMMIT, TREE, "CC BY-SA 4.0", "Nir Lazarovich",
    ]
    flat_text = " ".join(text.split())
    for marker in required_markers:
        require(marker in text or marker in flat_text,
                f"required rights/provenance marker absent: {marker}")
    for flag in SOURCE_AUDIT_EXPECTATIONS.values():
        require(flag in text, f"source correction marker absent from reader: {flag}")
    for repair_id in PROOF_REPAIR_EXPECTATIONS:
        require(repair_id in text, f"proof repair marker absent from reader: {repair_id}")
    forbidden = [
        "Translation and Transcription Project", "TTP", "C:\\Users\\",
        "AppData", "github_pat_", "ghp_", "Bearer ", "api_token",
    ]
    for marker in forbidden:
        require(marker not in text, f"forbidden/private string present: {marker}")
    require("$$" in text and "$" in text, "mathematical surface unexpectedly absent")

    fragments = resolve_fragment_targets(text, set(ids))
    assets = verify_assets(text, nodes, inventory)
    pandoc = verify_pandoc()
    return {
        "identity": reader_identity,
        "stable_ids": len(ids),
        "stable_ids_unique": len(set(ids)),
        "nonroot_ids": len(ids) - 1,
        "ordered_stable_ids_sha256": sequence_sha,
        "semantic_class_counts": dict(sorted(class_counts.items())),
        "provenance_origin_counts": dict(sorted((str(key), value) for key, value in origin_values.items())),
        "fenced_divs": {"opened": opens, "closed": closes, "balanced": True},
        "source_locators": {"count": sum("data-source-lines" in node["attrs"] for node in nodes), "valid": True},
        "source_aliases": dict(sorted(source_aliases.items())),
        "fragment_links": fragments,
        "mastery": {
            "exercise_hint_solution_triples": EXPECTED_MASTERY_TRIPLES,
            "complete_solutions": EXPECTED_MASTERY_TRIPLES,
            "source_exercises_preserved": 0,
        },
        "proof_repairs": list(PROOF_REPAIR_EXPECTATIONS),
        "source_corrections": list(SOURCE_AUDIT_EXPECTATIONS.values()),
        "figures": {"total": len(figure_nodes), "semantic": 14, "asset_pairs": 3},
        "assets": assets,
        "pandoc": pandoc,
        "rights_provenance_privacy": "PASS",
    }


def _require_review_statuses(value: Any, where: str) -> None:
    """Reject a review that hides a failed nested check."""
    if isinstance(value, dict):
        if "status" in value:
            require(value["status"] in {"PASS", "PASS_P1_P2_P3_ZERO", "RESOLVED"},
                    f"{where}.status is not a passing status")
        for key, child in value.items():
            _require_review_statuses(child, f"{where}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _require_review_statuses(child, f"{where}[{index}]")


def _check_reader_binding(binding: dict[str, Any], reader_identity: dict[str, Any], where: str) -> None:
    require(binding.get("path") == reader_identity["path"], f"{where}: reader path mismatch")
    require(binding.get("bytes") == reader_identity["bytes"], f"{where}: reader byte mismatch")
    require(binding.get("lf_lines") == reader_identity["lf_lines"], f"{where}: reader line mismatch")
    require(binding.get("sha256") == reader_identity["sha256"], f"{where}: reader hash mismatch")
    require(binding.get("edition_unit_id") == EDITION_UNIT_ID,
            f"{where}: edition unit mismatch")
    require(binding.get("course_route_unit_id") == COURSE_ROUTE_UNIT_ID,
            f"{where}: route unit mismatch")


def _check_frozen_binding(binding: dict[str, Any], source: dict[str, Any], where: str) -> None:
    require(binding.get("official_repository") == "https://git.sr.ht/~yp/math-notes",
            f"{where}: official repository mismatch")
    require(binding.get("commit") == COMMIT and binding.get("tree") == TREE,
            f"{where}: commit/tree mismatch")
    require(binding.get("authority_path") == UPSTREAM_PATH,
            f"{where}: authority path mismatch")
    require(binding.get("authority_bytes") == UPSTREAM_IDENTITY["bytes"]
            and binding.get("authority_sha256") == UPSTREAM_IDENTITY["sha256"],
            f"{where}: authority identity mismatch")
    require(binding.get("selected_source_lines") == "3518-4185"
            and binding.get("selected_span_lf_lines") == SPAN_IDENTITY["lf_lines"]
            and binding.get("selected_span_bytes") == SPAN_IDENTITY["bytes"]
            and binding.get("selected_span_sha256") == SPAN_IDENTITY["sha256"],
            f"{where}: selected-span identity mismatch")
    require(binding.get("next_source_line") == NEXT_LINE
            and binding.get("next_source_text") == NEXT_TEXT,
            f"{where}: next-source cursor mismatch")
    require(binding.get("source_audit_path") == SOURCE_AUDIT_PATH
            and binding.get("source_audit_sha256") == SOURCE_AUDIT_IDENTITY["sha256"],
            f"{where}: source-audit binding mismatch")


def verify_reviews(
    reader_identity: dict[str, Any], source: dict[str, Any],
    controls: dict[str, Any], inventory_identity: dict[str, Any]
) -> dict[str, Any]:
    math_review, math_identity = load_json(MATH_REVIEW_PATH, MATH_REVIEW_IDENTITY)
    source_review, source_identity = load_json(SOURCE_REVIEW_PATH, SOURCE_REVIEW_IDENTITY)
    require(math_review.get("review_id") ==
            "O012-FOMBERG-UNIT-007-INDEPENDENT-MATH-REVIEW-FINAL",
            "math final review ID mismatch")
    require(math_review.get("schema_version") == SCHEMA_VERSION
            and math_review.get("date") == DATE
            and math_review.get("status") == "PASS"
            and math_review.get("pass") is True
            and math_review.get("model_provenance") == MODEL,
            "math final review status/model mismatch")
    _check_reader_binding(math_review.get("canonical_reader", {}), reader_identity,
                          "math final review canonical_reader")
    _check_frozen_binding(math_review.get("frozen_source_binding", {}), source,
                          "math final review frozen_source_binding")
    require(math_review.get("severity_census") == {"P1": 0, "P2": 0, "P3": 0},
            "math final review severity census is not zero")
    require(math_review.get("findings") == [], "math final review contains findings")
    proof_checks = math_review.get("proof_repair_checks", [])
    require([item.get("repair_id") for item in proof_checks] == list(PROOF_REPAIR_EXPECTATIONS),
            "math final review proof-repair IDs mismatch")
    require(all(item.get("status") == "PASS" for item in proof_checks),
            "math final review proof-repair check failed")
    mastery = math_review.get("mastery_structure", {})
    require(mastery == {
        "expected_triples": 6, "exercise_ids_found": 6,
        "hint_ids_found": 6, "solution_ids_found": 6,
        "duplicate_or_missing_ids": 0, "status": "PASS",
    }, "math final review mastery structure mismatch")
    mastery_checks = math_review.get("mastery_checks", [])
    require(len(mastery_checks) == 6 and all(item.get("status") == "PASS" for item in mastery_checks),
            "math final review mastery checks failed")
    require(math_review.get("structural_counts") == {
        "proof_repair_modules": 3, "repair_theorems": 3,
        "repair_proofs": 3, "mastery_exercises": 6,
        "mastery_hints": 6, "mastery_solutions": 6,
    }, "math final review structural counts mismatch")

    require(source_review.get("review_id") ==
            "O012-FOMBERG-UNIT-007-INDEPENDENT-SOURCE-LANGUAGE-FINAL",
            "source-language final review ID mismatch")
    require(source_review.get("schema_version") == SCHEMA_VERSION
            and source_review.get("date") == DATE
            and source_review.get("status") == "PASS_P1_P2_P3_ZERO"
            and source_review.get("model_provenance") == MODEL,
            "source-language final review status/model mismatch")
    _check_reader_binding(source_review.get("canonical", {}), reader_identity,
                          "source-language final review canonical")
    authority = source_review.get("authority", {})
    require(authority.get("path") == UPSTREAM_PATH
            and authority.get("bytes") == UPSTREAM_IDENTITY["bytes"]
            and authority.get("lf_lines") == UPSTREAM_IDENTITY["lf_lines"]
            and authority.get("sha256") == UPSTREAM_IDENTITY["sha256"]
            and authority.get("commit") == COMMIT
            and authority.get("tree") == TREE
            and authority.get("license") == "CC BY-SA 4.0",
            "source-language final review authority binding mismatch")
    selected = authority.get("selected_span", {})
    require(selected == {
        "line_start": SPAN_IDENTITY["line_start"],
        "line_end": SPAN_IDENTITY["line_end"],
        "lf_lines": SPAN_IDENTITY["lf_lines"],
        "bytes": SPAN_IDENTITY["bytes"],
        "sha256": SPAN_IDENTITY["sha256"],
        "first_line": r"\subsection{Cellular homology}",
        "last_line": "",
        "next_line_number": NEXT_LINE,
        "next_line": NEXT_TEXT,
        "independently_recomputed": True,
    }, "source-language final review selected-span binding mismatch")
    require(source_review.get("severity_census") == {"P1": 0, "P2": 0, "P3": 0},
            "source-language final review severity census is not zero")
    decision = source_review.get("final_decision", {})
    require(decision.get("status") == "PASS_P1_P2_P3_ZERO"
            and decision.get("canonical_admission") == "APPROVED_FOR_NEXT_DETERMINISTIC_BUILD_AND_BACKEND_GATE"
            and decision.get("translation_restart_required") is False
            and decision.get("remaining_source_language_provenance_or_diagram_blockers") == 0,
            "source-language final review decision mismatch")
    actions = source_review.get("reviewer_actions", {})
    require(actions.get("other_files_modified") == 0
            and actions.get("git_invoked") is False
            and actions.get("network_invoked") is False,
            "source-language final review was not read-only")

    # Reviewed controls are a second, independent binding of the live ledgers
    # and inventory.  Ignore no listed item and reject changed bytes.
    current_identities = {
        **controls["identities"],
        INVENTORY_PATH: inventory_identity,
        SOURCE_AUDIT_PATH: {
            "path": SOURCE_AUDIT_PATH,
            "bytes": SOURCE_AUDIT_IDENTITY["bytes"],
            "lf_lines": SOURCE_AUDIT_IDENTITY["lf_lines"],
            "sha256": SOURCE_AUDIT_IDENTITY["sha256"],
        },
    }
    for item in source_review.get("reviewed_controls", []):
        path = item.get("path")
        if path in current_identities:
            observed = current_identities[path]
            require(item.get("bytes") == observed["bytes"]
                    and item.get("sha256") == observed["sha256"],
                    f"source-language review control identity mismatch: {path}")
    listed_paths = {item.get("path") for item in source_review.get("reviewed_controls", [])}
    require({SOURCE_AUDIT_PATH, INVENTORY_PATH, TERM_DRAFT_PATH, TERMINOLOGY_PATH} <= listed_paths,
            "source-language final review omitted a required control binding")
    _require_review_statuses(math_review, "math_review")
    _require_review_statuses(source_review, "source_review")

    # Review documents are public evidence and must not carry private paths,
    # credentials, or umbrella-name metadata.
    for label, review in (("math", math_review), ("source", source_review)):
        raw = json.dumps(review, ensure_ascii=False)
        for marker in ("github_pat_", "ghp_", "Bearer ", "api_token", "C:\\Users\\",
                       "AppData", "Translation and Transcription Project", "TTP"):
            require(marker not in raw, f"{label} review contains forbidden/private marker {marker}")

    return {
        "identity": source_identity,
        "status": source_review["status"],
        "severity_census": source_review["severity_census"],
        "math": {
            "identity": math_identity,
            "review_id": math_review["review_id"],
            "status": math_review["status"],
            "severity_census": math_review["severity_census"],
        },
        "source_language": {
            "identity": source_identity,
            "review_id": source_review["review_id"],
            "status": source_review["status"],
            "severity_census": source_review["severity_census"],
        },
    }


def main() -> None:
    # No command-line modes are accepted: a partial or ad-hoc invocation must
    # fail rather than emit a receipt whose scope is ambiguous.
    require(len(sys.argv) == 1, "validator accepts no command-line arguments")
    source = verify_source()
    inventory, inventory_identity = verify_inventory()
    _, reader_text = strict_text(READER_PATH)
    controls = verify_controls(reader_text)
    reader = verify_reader(source, inventory, controls)
    reviews = verify_reviews(reader["identity"], source, controls, inventory_identity)

    audit_identity = source["source_audit"]["identity"]
    gates = {
        "frozen_source_identity_span_and_next_cursor": "PASS",
        "source_environment_and_label_closure": "PASS",
        "stable_ids_72_nonroot_71_and_semantic_classes": "PASS",
        "seventeen_figures_inventory_and_assets": "PASS",
        "provenance_origin_vocabulary_and_rights": "PASS",
        "links_and_prior_unit_fragments": "PASS",
        "terminology_and_adverse_ledgers": "PASS",
        "proof_repairs_and_mastery_solutions": "PASS",
        "pandoc_native_and_mathml": "PASS",
        "independent_final_reviews_p1_p2_p3_zero": "PASS",
        "model_identification_and_privacy": "PASS",
    }
    require(all(value == "PASS" for value in gates.values()),
            "one or more QA gates did not pass")
    qa = {
        "schema_version": SCHEMA_VERSION,
        "qa_id": "O012-FOMBERG-UNIT-007-STATIC-QA",
        "date": DATE,
        "status": "PASS",
        "model_provenance": MODEL,
        "source_audit": audit_identity,
        "diagram_inventory": inventory_identity,
        "source": source,
        "reader": reader,
        "controls": controls,
        # Keep the historical single-review compatibility surface pointed at
        # the source-language review, while exposing both independent reviews
        # explicitly below.
        "independent_review": {
            "identity": reviews["identity"],
            "status": reviews["status"],
            "severity_census": reviews["severity_census"],
        },
        "independent_reviews": {
            "math": reviews["math"],
            "source_language": reviews["source_language"],
        },
        "translation_closure": {
            "contiguous_span": "3518-4185",
            "next_exact_cursor": NEXT_LINE,
            "next_exact_text": NEXT_TEXT,
            "source_mathematical_environments": SOURCE_ENVIRONMENT_TOTAL,
            "source_exercises_preserved": 0,
            "mastery_triples_complete": EXPECTED_MASTERY_TRIPLES,
            "proof_repairs_complete": len(PROOF_REPAIR_EXPECTATIONS),
            "source_corrections_recorded": len(SOURCE_AUDIT_EXPECTATIONS),
            "figures_total": len(FIGURE_EXPECTATIONS),
            "geometric_asset_pairs": 3,
            "semantic_reader_displays": 14,
            "stable_ids": EXPECTED_TOTAL_IDS,
            "nonroot_ids": EXPECTED_NONROOT_IDS,
        },
        "gates": gates,
    }
    # This is the only write performed by this validator, and it occurs after
    # every fail-closed check above has succeeded.
    qa_raw = receipt_bytes(qa)
    QA_OUTPUT.write_bytes(qa_raw)
    print(json.dumps({
        "status": "PASS",
        "qa": {"path": str(QA_OUTPUT.relative_to(LANE)).replace("\\", "/"),
               "bytes": len(qa_raw), "sha256": sha256(qa_raw)},
        "source": source["selected_span"],
        "next_cursor": {"line": NEXT_LINE, "text": NEXT_TEXT},
        "reader": reader["identity"],
        "stable_ids": reader["stable_ids"],
        "nonroot_ids": reader["nonroot_ids"],
        "semantic_class_counts": reader["semantic_class_counts"],
        "source_environments": SOURCE_ENVIRONMENT_TOTAL,
        "figures": len(FIGURE_EXPECTATIONS),
        "assets": reader["assets"]["files"],
        "mastery_triples": EXPECTED_MASTERY_TRIPLES,
        "reviews": {
            "math": reviews["math"]["identity"],
            "source_language": reviews["source_language"]["identity"],
        },
    }, ensure_ascii=False, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
