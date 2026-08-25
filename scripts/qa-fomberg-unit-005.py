#!/usr/bin/env python3
"""Fail-closed source and static QA for Fomberg Unit 005."""
from __future__ import annotations

import csv
import hashlib
import json
import re
import shlex
import shutil
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any


LANE = Path(__file__).resolve().parents[1]
AUDIT_OUTPUT = LANE / "qa/FOMBERG_UNIT_005_SOURCE_AUDIT.json"
QA_OUTPUT = LANE / "qa/FOMBERG_UNIT_005_QA.json"

DATE = "2026-08-25"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"
COMMIT = "563194fae879178b9a6871b249513bfc27968975"
TREE = "fb678966d1533d529bdd72f49d8496a3bdc14a9b"
READER_PATH = (
    "source/id-ID/fomberg/units/"
    "fomberg-unit-005-degree-maps-local-degree.md"
)
ROBERTS_030_PATH = "source/id-ID/units/unit-030-lecture-030.md"
UPSTREAM_PATH = (
    "authority/upstream/"
    "math-notes-563194fae879178b9a6871b249513bfc27968975/"
    "tree/algebraic_topology.tex"
)
TERMINOLOGY_PATH = "00_control/TERMINOLOGY.csv"
ADVERSE_PATH = "00_control/ADVERSE_LEDGER.csv"
TERM_DRAFT_PATH = "qa/fomberg-unit-005/TERMINOLOGY_ROWS_DRAFT.csv"
ADVERSE_DRAFT_PATH = "qa/fomberg-unit-005/ADVERSE_ROWS_DRAFT.csv"
REVIEW_PATH = "qa/fomberg-unit-005/INDEPENDENT_REVIEW_FINAL.json"

READER_IDENTITY = {
    "bytes": 40274,
    "lf_lines": 1150,
    "sha256": "ad6e31291e3df97b81f7e5a30144ca27157f907291e74f4d49c09a0620487075",
}
ROBERTS_030_IDENTITY = {
    "bytes": 23008,
    "lf_lines": 729,
    "sha256": "88da8cf71d0f81328bdd65b0dea7d54c48655ed8836e230eaed821796b61b08d",
}
UPSTREAM_IDENTITY = {
    "bytes": 223886,
    "lf_lines": 6069,
    "sha256": "d27095de0f38f0c14b2d7716cb52d51d064f0594dd9f82f9d1b3e6af5b35a483",
}
SPAN_IDENTITY = {
    "line_start": 2847,
    "line_end": 3122,
    "lf_lines": 276,
    "bytes": 12203,
    "sha256": "9ac1d27872a09134b75bb077ad113716a9e828c2177ac296e7bf3331395da85a",
}
NEXT_LINE = 3123
NEXT_TEXT = r"\subsection{Cellular complexes}"
REVIEW_IDENTITY = {
    "bytes": 2878,
    "lf_lines": 91,
    "sha256": "bcf628eb480234d217c235727c2082289f0cc09d8062d822c1e33964c072a6e0",
}
CONTROL_IDENTITIES = {
    TERMINOLOGY_PATH: {
        "bytes": 56920,
        "lf_lines": 455,
        "sha256": "4f3ec0ee76769ac297b3ed820c1e46645277d87c4eb30cbde5358f2cca72b68f",
    },
    ADVERSE_PATH: {
        "bytes": 194914,
        "lf_lines": 534,
        "sha256": "ebf0157674a1db25690480defe4046e2e9a3e1d5322368af2b5a8f3e94597388",
    },
}
DRAFT_IDENTITIES = {
    TERM_DRAFT_PATH: {
        "bytes": 3608,
        "lf_lines": 21,
        "sha256": "e5c9b7fd4a7884728e0fea696a9fe3511b21adf92ccd827c713d6c1184de3ab7",
    },
    ADVERSE_DRAFT_PATH: {
        "bytes": 10140,
        "lf_lines": 12,
        "sha256": "e5398b2a644e475189f44bd031a11a8d8bbdb35bbbf581b583d60e6d88ac1428",
    },
}

EXPECTED_HEADING_IDS = [
    "o012-fom-u005-notice",
    "o012-fom-u005",
    "o012-fom-u005-s11a",
    "o012-fom-u005-s11b",
    "o012-fom-u005-local-degree",
    "o012-fom-u005-mastery",
]
EXPECTED_CLASS_COUNTS = {
    "boundary": 1,
    "definition": 2,
    "example": 1,
    "exercise": 6,
    "figure": 1,
    "heading": 6,
    "hint": 6,
    "proof": 3,
    "proof-supplement": 1,
    "proposition": 2,
    "remark": 4,
    "solution": 6,
    "source-audit": 11,
    "source-omission": 1,
    "theorem": 1,
}
EXPECTED_ID_SEQUENCE_SHA256 = (
    "e85b618bcffc24fd8a802834a352ee73b0b76ced4eef751d3edf3e98e3c5f503"
)
EXPECTED_LINK_TARGET_COUNTS = Counter({
    "o012-fom-u005-mcheck-001": 1,
    "o012-rbt-l30-cor-001": 1,
    "o012-rbt-l30-def-002": 1,
    "o012-rbt-l30-lem-001": 1,
    "o012-rbt-l30-proof-002": 2,
    "o012-rbt-l30-proof-004": 1,
    "o012-rbt-l30-prop-001": 1,
    "o012-rbt-l30-thm-003": 1,
})
SOURCE_ENVIRONMENT_COUNTS = {
    "definition": 2,
    "example": 1,
    "proof": 3,
    "proposition": 2,
    "remark": 4,
    "theorem": 1,
}
SOURCE_ENVIRONMENT_TOTAL = 13
ALIASES = {
    "def:local-degree": "o012-fom-u005-def-local-degree",
    "prop:local-degree-for-global-degree": "o012-fom-u005-prop-local-to-global",
}
TERM_IDS = [f"O012-TERM-{number:04d}" for number in range(435, 455)]
ADVERSE_IDS = [f"O012-ADV-{number:04d}" for number in range(523, 534)]


def die(message: str) -> None:
    raise SystemExit(f"Fomberg Unit 005 QA FAIL: {message}")


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
        opener = re.match(r"^(:{3,})\s+(\{.*\})\s*$", line)
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
        closer = re.match(r"^(:{3,})\s*$", line)
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
            2847 <= start <= end <= 3122,
            f"{where}: locator {start}-{end} outside admitted span",
        )
        ranges.append((start, end))
    return ranges


def verify_source() -> dict[str, Any]:
    raw, _, upstream_identity = require_identity(UPSTREAM_PATH, UPSTREAM_IDENTITY)
    lines = raw.splitlines(keepends=True)
    require(len(lines) == 6069, "upstream physical-line count mismatch")
    span = b"".join(lines[2846:3122])
    span_actual = {
        "line_start": 2847,
        "line_end": 3122,
        "lf_lines": span.count(b"\n"),
        "bytes": len(span),
        "sha256": sha256(span),
    }
    require(span_actual == SPAN_IDENTITY, "frozen source-span identity mismatch")
    require(
        lines[3122].decode("utf-8").rstrip("\n") == NEXT_TEXT,
        "exact next source line mismatch",
    )
    span_text = span.decode("utf-8")
    env_counts = Counter(re.findall(r"\\begin\{([^}]+)\}", span_text))
    mathematical = {key: env_counts[key] for key in SOURCE_ENVIRONMENT_COUNTS}
    require(
        mathematical == SOURCE_ENVIRONMENT_COUNTS,
        f"source mathematical environment census mismatch: {mathematical}",
    )
    require(
        sum(mathematical.values()) == SOURCE_ENVIRONMENT_TOTAL,
        "source mathematical environment total mismatch",
    )
    require(
        len(re.findall(r"^\\subsection\{", span_text, flags=re.MULTILINE)) == 1,
        "source subsection count mismatch",
    )
    require(span_text.count(r"\begin{tikzcd}") == 2, "source TikZ-CD count mismatch")
    return {
        "authority_identity": upstream_identity,
        "commit": COMMIT,
        "tree": TREE,
        "selected_span": span_actual,
        "subsections": 1,
        "mathematical_environments": mathematical,
        "mathematical_environment_total": SOURCE_ENVIRONMENT_TOTAL,
        "source_tikzcd_occurrences": 2,
        "next_line": NEXT_LINE,
        "next_line_text": NEXT_TEXT,
    }


def verify_controls() -> dict[str, Any]:
    identities: dict[str, Any] = {}
    texts: dict[str, str] = {}
    for relative, expected in {**CONTROL_IDENTITIES, **DRAFT_IDENTITIES}.items():
        _, text, ident = require_identity(relative, expected)
        identities[relative] = ident
        texts[relative] = text

    term_rows = list(csv.DictReader(texts[TERMINOLOGY_PATH].splitlines()))
    term_draft = list(csv.DictReader(texts[TERM_DRAFT_PATH].splitlines()))
    adverse_rows = list(csv.DictReader(texts[ADVERSE_PATH].splitlines()))
    adverse_draft = list(csv.DictReader(texts[ADVERSE_DRAFT_PATH].splitlines()))
    require(len(term_rows) == 454 and len(term_draft) == 20,
            "terminology row count mismatch")
    require(len(adverse_rows) == 533 and len(adverse_draft) == 11,
            "adverse row count mismatch")
    require(term_rows[-20:] == term_draft,
            "terminology tail differs from reviewed draft")
    require(adverse_rows[-11:] == adverse_draft,
            "adverse tail differs from reviewed draft")
    require([row["term_id"] for row in term_draft] == TERM_IDS,
            "Unit 005 terminology IDs are not consecutive")
    require([row["event_id"] for row in adverse_draft] == ADVERSE_IDS,
            "Unit 005 adverse IDs are not consecutive")
    require(len({row["term_id"] for row in term_rows}) == 454,
            "duplicate terminology ID")
    require(len({row["event_id"] for row in adverse_rows}) == 533,
            "duplicate adverse ID")
    require(all(row["status"] == "admitted" for row in term_draft),
            "Unit 005 terminology not fully admitted")
    allowed = {
        "clarified_in_translation",
        "corrected_in_translation",
        "hypothesis_repaired_in_translation",
        "proof_completed_in_translation",
        "resolved_before_admission",
    }
    require(all(row["status"] in allowed for row in adverse_draft),
            "Unit 005 adverse status mismatch")
    require(any("FOM-PR-12" in row["observed"] for row in adverse_draft),
            "FOM-PR-12 adverse evidence absent")
    return {
        "identities": identities,
        "terminology": {
            "rows": 454,
            "unit_rows": 20,
            "terminal_id": "O012-TERM-0454",
            "unit_tail_matches_reviewed_draft": True,
        },
        "adverse": {
            "rows": 533,
            "unit_rows": 11,
            "terminal_id": "O012-ADV-0533",
            "unit_tail_matches_reviewed_draft": True,
        },
    }


def verify_review() -> dict[str, Any]:
    _, text, ident = require_identity(REVIEW_PATH, REVIEW_IDENTITY)
    try:
        review = json.loads(text)
    except json.JSONDecodeError as exc:
        die(f"independent review malformed ({exc})")
    require(review.get("status") == "PASS_P1_P2_P3_ZERO",
            "independent review not final PASS")
    require(review.get("severity_census") == {"P1": 0, "P2": 0, "P3": 0},
            "independent review severity census not zero")
    require(review.get("canonical", {}).get("sha256") == READER_IDENTITY["sha256"],
            "independent review canonical hash mismatch")
    require(review.get("upstream_span", {}).get("sha256") == SPAN_IDENTITY["sha256"],
            "independent review source-span hash mismatch")
    require(review.get("file_mutations_by_reviewer") == 0,
            "independent review was not read-only")
    return {
        "identity": ident,
        "status": review["status"],
        "severity_census": review["severity_census"],
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
        text=True, encoding="utf-8", errors="replace", timeout=60, cwd=LANE,
    )
    html = subprocess.run(
        [executable, "--from=markdown+fenced_divs+tex_math_dollars",
         "--to=html5", "--mathml", "--wrap=none", str(LANE / READER_PATH)],
        check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, encoding="utf-8", errors="replace", timeout=60, cwd=LANE,
    )
    require(version.returncode == 0 and version.stdout.splitlines(),
            "Pandoc version probe failed")
    require(native.returncode == 0,
            f"Pandoc native parse failed: {native.stderr[-800:]}")
    require(html.returncode == 0,
            f"Pandoc MathML render failed: {html.stderr[-800:]}")
    require(not native.stderr.strip() and not html.stderr.strip(),
            "Pandoc emitted warnings")
    math_count = html.stdout.count("<math")
    display_count = html.stdout.count('<math display="block"')
    require(math_count == 487, f"Pandoc MathML count mismatch ({math_count})")
    require(display_count == 78,
            f"Pandoc display-MathML count mismatch ({display_count})")
    return {
        "version": version.stdout.splitlines()[0].strip(),
        "native_parse": "PASS",
        "mathml_render": "PASS",
        "mathml_nodes": math_count,
        "display_mathml_nodes": display_count,
        "warnings": 0,
    }


def verify_reader() -> dict[str, Any]:
    _, text, reader_identity = require_identity(READER_PATH, READER_IDENTITY)
    _, roberts_text, roberts_identity = require_identity(
        ROBERTS_030_PATH, ROBERTS_030_IDENTITY
    )
    nodes, opens, closes = parse_reader(text)
    ids = [node["id"] for node in nodes]
    require(len(ids) == 52 and len(set(ids)) == 52,
            "stable ID count/uniqueness mismatch")
    require(all(re.fullmatch(r"[a-z0-9][a-z0-9-]*", ident) for ident in ids),
            "non-locale-neutral stable ID syntax")
    sequence_sha = sha256(("\n".join(ids) + "\n").encode("utf-8"))
    require(sequence_sha == EXPECTED_ID_SEQUENCE_SHA256,
            "ordered stable-ID sequence mismatch")
    headings = [node["id"] for node in nodes if node["kind"] == "heading"]
    require(headings == EXPECTED_HEADING_IDS, "heading topology/order mismatch")
    class_counts = Counter(node["kind"] for node in nodes)
    require(dict(sorted(class_counts.items())) == EXPECTED_CLASS_COUNTS,
            f"semantic class census mismatch: {dict(class_counts)}")

    locators: list[dict[str, Any]] = []
    for node in nodes:
        value = node["attrs"].get("data-source-lines")
        if value is not None:
            ranges = parse_source_locator(value, node["id"])
            locators.append({
                "id": node["id"], "value": value,
                "ranges": [list(item) for item in ranges],
            })
    require(len(locators) == 31, "source locator count mismatch")

    aliases = {
        node["attrs"]["data-source-label"]: node["id"]
        for node in nodes if "data-source-label" in node["attrs"]
    }
    require(aliases == ALIASES, f"source alias mismatch: {aliases}")
    link_counts = Counter(re.findall(r"\]\(#([^)]+)\)", text))
    require(link_counts == EXPECTED_LINK_TARGET_COUNTS,
            f"fragment-link census mismatch: {link_counts}")
    for target in link_counts:
        if target.startswith("o012-fom-u005-"):
            require(target in ids, f"unresolved same-unit fragment #{target}")
        else:
            require(f"#{target}" in roberts_text,
                    f"unresolved Roberts Unit 30 fragment #{target}")

    node_by_id = {node["id"]: node for node in nodes}
    for number in range(1, 7):
        suffix = f"{number:03d}"
        exercise = node_by_id.get(f"o012-fom-u005-mcheck-{suffix}")
        hint = node_by_id.get(f"o012-fom-u005-hint-{suffix}")
        solution = node_by_id.get(f"o012-fom-u005-sol-{suffix}")
        require(exercise is not None and hint is not None and solution is not None,
                f"mastery triple {suffix} incomplete")
        require(exercise["line_start"] < hint["line_start"] < solution["line_start"],
                f"mastery triple {suffix} order invalid")
        require(solution["line_end"] - solution["line_start"] >= 8,
                f"solution {suffix} is not complete enough for admission")

    required_markers = [
        "FOM-PR-12",
        "#o012-fom-u005-proof-local-degree-independence",
        "data-proof-status=\"complete_original_repair\"",
        "#o012-fom-u005-audit-local-degree-range",
        "Creative Commons Attribution-ShareAlike 4.0 International",
        MODEL,
        "Tidak ada prosa dari bank soal Fomberg terpisah",
        "tidak menyiratkan dukungan, pengesahan, atau",
        "afiliasi dengan Yeheli Fomberg",
        "edition_unit_id: \"O012-FOM-005\"",
        "course_route_unit_id: \"D60-R12\"",
        "route_status: \"pembandingan derajat opsional; jembatan derajat lokal aditif\"",
    ]
    flat_text = " ".join(text.split())
    for phrase in required_markers:
        require(
            phrase in text or phrase in flat_text,
            f"required marker absent: {phrase}",
        )
    origins = Counter(re.findall(r'data-origin="([^"]+)"', text))
    require(set(origins) == {"source-derived", "edition-original"},
            f"uncontrolled provenance value: {origins}")
    require(
        'source-omission #o012-fom-u005-omission-pr12 data-origin="edition-original"'
        in text,
        "source-omission provenance missing",
    )
    require(text.count('data-rendering="semantic-reflow"') == 1,
            "semantic reflow marker mismatch")
    require(text.count("{.figure") == 1 and "![" not in text,
            "Unit 005 must have one semantic figure and no raster reference")

    forbidden = [
        "Translation and Transcription Project",
        "TTP",
        "C:\\Users\\",
        "AppData",
        "github_pat_",
        "ghp_",
        "Bearer ",
        "api_token",
        "edition-original-navigation",
        "source-semantic-reflow",
        "pemetaan pasangan",
        "generator",
        "dikalikankan",
        "di bagian A",
    ]
    for phrase in forbidden:
        require(phrase not in text, f"forbidden/private/stale string present: {phrase}")
    require("lang: id-ID" in text, "id-ID locale declaration missing")
    require("$$" in text, "mathematics surface unexpectedly absent")

    term_rows = list(csv.DictReader((LANE / TERM_DRAFT_PATH).read_text(
        encoding="utf-8"
    ).splitlines()))
    folded_text = text.casefold()
    for row in term_rows:
        require(row["id_ID"].casefold() in folded_text,
                f"terminology evidence lacks admitted form: {row['term_id']}")

    pandoc = verify_pandoc()
    return {
        "identity": reader_identity,
        "roberts_unit_030_crosslink_witness": roberts_identity,
        "stable_ids": 52,
        "stable_ids_unique": 52,
        "ordered_stable_ids_sha256": sequence_sha,
        "semantic_class_counts": dict(sorted(class_counts.items())),
        "fenced_divs": {"opened": opens, "closed": closes, "balanced": True},
        "source_locators": {"count": len(locators), "valid": len(locators)},
        "source_aliases": aliases,
        "fragment_links": {
            "count": sum(link_counts.values()),
            "distinct_targets": len(link_counts),
            "resolved": sum(link_counts.values()),
            "target_counts": dict(sorted(link_counts.items())),
        },
        "proof_repairs": ["FOM-PR-12"],
        "mastery": {
            "exercise_hint_solution_triples": 6,
            "complete_solutions": 6,
        },
        "assets": {
            "source_tikzcd_occurrences": 2,
            "semantic_figures": 1,
            "raster_redraws": 0,
            "semantic_reflow_provenance_present": True,
        },
        "pandoc": pandoc,
        "rights_provenance_privacy": "PASS",
    }


def main() -> None:
    source = verify_source()
    controls = verify_controls()
    review = verify_review()
    reader = verify_reader()

    audit = {
        "schema_version": "1.0.0",
        "audit_id": "O012-FOMBERG-UNIT-005-SOURCE-AUDIT",
        "date": DATE,
        "status": "PASS",
        "role_id": "O012",
        "course_id": "D60",
        "edition_unit_id": "O012-FOM-005",
        "course_route_unit_id": "D60-R12",
        "component": "Fomberg Algebraic Topology Section 1.11",
        "route_status": "optional degree cross-check plus additive local-degree layer",
        "license": "CC BY-SA 4.0",
        "model_provenance": MODEL,
        "source": source,
        "reader": reader["identity"],
        "translation_closure": {
            "contiguous_span": "2847-3122",
            "subsections_complete_in_source_order": 1,
            "source_mathematical_environments_represented": 13,
            "proof_repairs_complete": ["FOM-PR-12"],
            "choice_independence_proved": True,
            "dimension_range_repair_disclosed": True,
            "mastery_triples_complete": 6,
            "next_exact_cursor": 3123,
            "next_exact_text": NEXT_TEXT,
        },
        "correction_and_terminology_ledgers": controls,
        "independent_review": review,
    }
    audit_raw = receipt_bytes(audit)
    AUDIT_OUTPUT.write_bytes(audit_raw)

    qa = {
        "schema_version": "1.0.0",
        "qa_id": "O012-FOMBERG-UNIT-005-STATIC-QA",
        "date": DATE,
        "status": "PASS",
        "model_provenance": MODEL,
        "source_audit": {
            "path": "qa/FOMBERG_UNIT_005_SOURCE_AUDIT.json",
            "bytes": len(audit_raw),
            "sha256": sha256(audit_raw),
        },
        "source": source,
        "reader": reader,
        "controls": controls,
        "independent_review": review,
        "gates": {
            "source_identity_and_contiguity": "PASS",
            "source_order_and_environment_census": "PASS",
            "stable_structure_aliases_and_links": "PASS",
            "mathematics_and_proof_repair": "PASS",
            "mastery_solution_closure": "PASS",
            "terminology_and_correction_ledgers": "PASS",
            "semantic_diagram_reflow_and_accessibility": "PASS",
            "pandoc_native_and_mathml": "PASS",
            "license_attribution_nonendorsement_model_and_privacy": "PASS",
            "independent_review_p1_p2_p3_zero": "PASS",
        },
    }
    qa_raw = receipt_bytes(qa)
    QA_OUTPUT.write_bytes(qa_raw)
    print(json.dumps({
        "status": "PASS",
        "source_audit": {"bytes": len(audit_raw), "sha256": sha256(audit_raw)},
        "qa": {"bytes": len(qa_raw), "sha256": sha256(qa_raw)},
        "reader": reader["identity"],
        "stable_ids": reader["stable_ids"],
        "source_locators": reader["source_locators"]["count"],
        "proof_repairs": ["FOM-PR-12"],
        "mastery_triples": 6,
    }, ensure_ascii=False, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
