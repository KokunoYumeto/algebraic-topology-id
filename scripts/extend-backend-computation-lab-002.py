#!/usr/bin/env python3
"""Fail-closed append-only backend admission for O012/D60 computation Lab 2."""
from __future__ import annotations

import csv
import hashlib
import importlib.util
import io
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any


LANE = Path(__file__).resolve().parents[1]
BACKEND = LANE / "backend"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"
SCHEMA = "curriculum.interop"
SCHEMA_VERSION = "0.1.0"
WORKFLOW = "o012-d60-id-reader-production"
TIMESTAMP = "2026-08-28T00:00:00Z"
COURSE = "course:o012-d60"
PROGRAM = "program:o012-id"
FOMBERG_EDITION = "edition:fomberg-at-2025-563194f"
FOMBERG_RESOURCE = "resource:fomberg-algebraic-topology-2025"
INTEGRATED_RIGHTS = "rights:o012-d60-integrated-route-cc-by-sa-4.0"
LAB_ID = "D60-LAB02"
EDITION_UNIT_ID = "O012-ORIG-LAB02"
LOCAL_ROOT = "o012-d60-lab02"
ROOT_UNIT = f"unit:{LOCAL_ROOT}"
LAB_RIGHTS = f"rights:{LOCAL_ROOT}-original-cc-by-sa-4.0"
ROUTES = ("D60-R08",)
SOURCE_PATH = "source/id-ID/labs/computation-lab-002-chain-matrices-smith-normal-form.md"
PROGRAM_PATH = "source/id-ID/labs/o012_d60_lab02_smith_normal_form.py"
TEST_PATH = "source/id-ID/labs/test_o012_d60_lab02_smith_normal_form.py"
EXPECTED_PATH = "source/id-ID/labs/expected-output-lab02.txt"
TERMINOLOGY_PATH = "00_control/TERMINOLOGY.csv"
STATIC_PATH = "qa/computation-lab-002/STATIC_QA.json"
CODE_PATH = "qa/computation-lab-002/INDEPENDENT_CODE_REVIEW.json"
MATH_PATH = "qa/computation-lab-002/INDEPENDENT_MATH_REVIEW.json"
LANGUAGE_PATH = "qa/computation-lab-002/INDEPENDENT_SOURCE_LANGUAGE_REVIEW.json"
EXECUTION_PATH = "qa/computation-lab-002/EXECUTION_RECEIPT.json"
COMBINED_PATH = "qa/COMPUTATION_LAB_002_QA.json"
BASELINE_RECEIPT_PATH = "qa/BACKEND_APPEND_ONLY_COMPUTATION_LAB_001_CUMULATIVE_RECEIPT.json"
BASELINE_RECEIPT_IDENTITY = (
    9727,
    272,
    "90f445294eea58aca5bcebe6acaff7293251b21e32aa25f3b62705e64cf8ab74",
)

FILES = (
    "artifacts.jsonl", "assets.jsonl", "authority.jsonl", "concepts.jsonl",
    "corrections.jsonl", "qa.jsonl", "relations.jsonl", "rights.jsonl",
    "segments.jsonl", "terms.jsonl", "units.jsonl",
)

# This is the exact live Lab 1 cumulative boundary.  Every value was read from
# the named backend file; none is inferred from a receipt or aggregate alone.
PREFIX = {
    "artifacts.jsonl": (214, 176452, "b79da3c77f733a175cf900c655816d4a06fa3f060a495a2644d30b010ce5e8d0"),
    "assets.jsonl": (87, 64692, "1df40f8f6ca4f2fbfbe8a7b924a68a153713a20a4eebe1d014d8fb04669945f7"),
    "authority.jsonl": (6, 4374, "84c622f56dbbd5ba379361245ecfe07bc79c9f4fd6b18ba21b82b5f545211869"),
    "concepts.jsonl": (491, 155292, "c8ccbc4ee38e0a4f0b0d8ee6088774574a4138a7e611bbaa08133fa3ff2ad764"),
    "corrections.jsonl": (564, 594720, "bd961fad5d83e96fec6ef83caa8447e2e5f282c603fd4983d79b5b4b54049fbb"),
    "qa.jsonl": (184, 101370, "65a0890de4efa5051264900fa85dae8631e073148f3daf1d3fe7ce4132ebc5e9"),
    "relations.jsonl": (1106, 498962, "6d91e165cb79d4a03d1b21939f934a2155591f2bd2f7e91420a08b6178e485bf"),
    "rights.jsonl": (108, 101740, "aa6c6bf27d9636bbe22d16b6f550a75cce7e8ef7142dffc04f8f4aa3667af69b"),
    "segments.jsonl": (2065, 3387764, "8499116f271fca22b3f30aeba2e6d2410c3a480a1bc000120fc44c195ffd5806"),
    "terms.jsonl": (484, 321259, "908dd1dcdea9ca52acfc91c681a538a0599670d3d3f7ad25a1d9313b508a1740"),
    "units.jsonl": (2095, 3569075, "5ae55e8fc36311878a5209a4f9404faa16784bc22b98883a4dcbfaaf9f71fd22"),
}
PREFIX_TOTAL = (
    7404,
    8975700,
    "4740eb2ff83b4f9df3c0d90c2426ff77e652b23cad0bbe7763c54ebdefa60b4b",
)

INPUT_PATHS = (
    SOURCE_PATH, PROGRAM_PATH, TEST_PATH, EXPECTED_PATH, TERMINOLOGY_PATH,
    STATIC_PATH, CODE_PATH, MATH_PATH, LANGUAGE_PATH, EXECUTION_PATH,
    COMBINED_PATH,
)
LEARNER_PATHS = (SOURCE_PATH, PROGRAM_PATH, TEST_PATH, EXPECTED_PATH)
REVIEW_PATHS = (CODE_PATH, MATH_PATH, LANGUAGE_PATH)
EVIDENCE_PATHS = (STATIC_PATH, CODE_PATH, MATH_PATH, LANGUAGE_PATH, EXECUTION_PATH, COMBINED_PATH)

ID_KINDS = {
    LOCAL_ROOT: ("reader_unit", "laboratory"),
    f"{LOCAL_ROOT}-status": ("section", "status"),
    f"{LOCAL_ROOT}-prerequisites": ("section", "prerequisites"),
    f"{LOCAL_ROOT}-objectives": ("section", "objectives"),
    f"{LOCAL_ROOT}-data": ("section", "data"),
    f"{LOCAL_ROOT}-matrices": ("section", "derivation"),
    **{f"{LOCAL_ROOT}-task-{number:03d}": ("exercise", "exercise") for number in range(1, 7)},
    f"{LOCAL_ROOT}-hint": ("hint", "hint"),
    f"{LOCAL_ROOT}-program": ("source_code", "source_code"),
    f"{LOCAL_ROOT}-tests": ("test_suite", "test_suite"),
    f"{LOCAL_ROOT}-expected-output": ("expected_output", "expected_output"),
    f"{LOCAL_ROOT}-interpretation": ("interpretation", "interpretation"),
    f"{LOCAL_ROOT}-solution": ("solution", "solution"),
    f"{LOCAL_ROOT}-sol-surface": ("section", "solution_section"),
    f"{LOCAL_ROOT}-sol-boundaries": ("section", "solution_section"),
    f"{LOCAL_ROOT}-sol-smith": ("section", "solution_section"),
    f"{LOCAL_ROOT}-sol-torsion": ("section", "solution_section"),
    f"{LOCAL_ROOT}-sol-control": ("section", "solution_section"),
    f"{LOCAL_ROOT}-reproducibility": ("verification", "verification"),
    f"{LOCAL_ROOT}-rights": ("rights_notice", "rights_notice"),
}

TERM_SPECS = (
    (493, "boundary matrix", "matriks batas", "homological_algebra", f"{LOCAL_ROOT}-matrices", "generic integer matrix of a boundary homomorphism after ordered oriented bases are fixed; use matriks batas simpleksial for the simplicial specialization"),
    (494, "Smith normal form", "bentuk normal Smith", "integer_linear_algebra", f"{LOCAL_ROOT}-interpretation", "capitalize the proper name; diagonal entries are nonnegative and each nonzero entry divides the next"),
    (495, "invariant factor", "faktor invarian", "integer_linear_algebra", f"{LOCAL_ROOT}-sol-smith", "nonzero diagonal factor in Smith normal form; factors greater than one detect finite cyclic torsion"),
    (496, "unimodular matrix", "matriks unimodular", "integer_linear_algebra", f"{LOCAL_ROOT}-sol-smith", "square integer matrix with determinant plus or minus one and hence an integer inverse"),
    (497, "Smith certificate", "sertifikat Smith", "integer_linear_algebra", f"{LOCAL_ROOT}-sol-smith", "exact integer data U,A,V,D with UAV=D, U and V unimodular, and D satisfying the divisibility convention"),
    (498, "torsion cycle", "siklus torsi", "homological_algebra", f"{LOCAL_ROOT}-sol-torsion", "cycle representing a finite-order nonzero homology class; prove both a multiple is a boundary and the cycle itself is not"),
    (499, "vertex link", "tautan simpul", "simplicial_topology", f"{LOCAL_ROOT}-sol-surface", "simplicial link of a vertex; in a closed triangulated surface it is a cycle"),
    (500, "signed permutation matrix", "matriks permutasi bertanda", "integer_linear_algebra", f"{LOCAL_ROOT}-sol-control", "basis-reordering matrix with one plus or minus one in every row and column; it is unimodular"),
    (501, "simplicial boundary matrix", "matriks batas simpleksial", "homological_algebra", f"{LOCAL_ROOT}-matrices", "matrix of the alternating-face boundary map in ordered oriented simplex bases"),
    (502, "torsion witness", "saksi torsi", "homological_algebra", f"{LOCAL_ROOT}-sol-torsion", "explicit cycle, multiple-filling chain, and non-boundary detector proving a homology class has specified finite order"),
)

EXISTING_CONCEPTS = {
    "concept:boundary-map", "concept:boundary-of-a-simplex", "concept:chain",
    "concept:chain-boundary", "concept:chain-complex", "concept:cocycle",
    "concept:cycle", "concept:delta-complex", "concept:free-abelian-group",
    "concept:homology", "concept:homology-class", "concept:orientation",
    "concept:real-projective-plane", "concept:simplex", "concept:simplex-face",
    "concept:simplicial-complex", "concept:simplicial-homology", "concept:vertex",
}
NEW_CONCEPTS = {number: f"concept:{LOCAL_ROOT}-term-{number:04d}" for number, *_ in TERM_SPECS}
ALL_LAB_CONCEPTS = tuple(sorted(EXISTING_CONCEPTS | set(NEW_CONCEPTS.values())))

ROUTE_ANCHORS = {"D60-R08": "unit:o012-fom-u001"}
R08_DEPENDENCY_ANCHORS = {
    "unit:o012-fom-u001",
    "unit:o012-fom-u001-def-007",
    "unit:o012-fom-u001-def-boundary",
    "unit:o012-fom-u001-exa-007",
    "unit:o012-fom-u001-lem-boundary-square",
    "unit:o012-fom-u001-def-008",
    "unit:o012-fom-u001-def-009",
    "unit:o012-fom-u001-def-010",
}
TASK_DEPENDENCIES = {
    1: ("unit:o012-fom-u001",),
    2: ("unit:o012-fom-u001-def-007", "unit:o012-fom-u001-exa-007"),
    3: ("unit:o012-fom-u001-def-007", "unit:o012-fom-u001-def-boundary", "unit:o012-fom-u001-lem-boundary-square"),
    4: ("unit:o012-fom-u001-def-008", "unit:o012-fom-u001-def-009", "unit:o012-fom-u001-def-010"),
    5: ("unit:o012-fom-u001-def-008", "unit:o012-fom-u001-def-009", "unit:o012-fom-u001-def-010"),
    6: ("unit:o012-fom-u001-def-boundary", "unit:o012-fom-u001-def-010"),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"Lab 2 backend producer FAIL: {message}")


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def identity(raw: bytes) -> tuple[int, int, str]:
    return len(raw), raw.count(b"\n"), digest(raw)


def canon(record: dict[str, Any]) -> bytes:
    return (json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def common(entity_type: str, ident: str) -> dict[str, Any]:
    return {
        "entity_type": entity_type,
        "id": ident,
        "schema": SCHEMA,
        "schema_version": SCHEMA_VERSION,
        "status": "active",
        "supersedes": None,
        "timestamp": TIMESTAMP,
        "workflow": WORKFLOW,
    }


def disciplined(relative: str) -> bytes:
    path = LANE / relative
    require(path.is_file(), f"missing input: {relative}")
    raw = path.read_bytes()
    require(raw and b"\r" not in raw and raw.endswith(b"\n"), f"input is not nonempty UTF-8/LF: {relative}")
    raw.decode("utf-8", errors="strict")
    return raw


def normalized(value: str) -> str:
    return value.replace("\\", "/").removeprefix("./")


def identity_index(node: Any, out: dict[str, tuple[int, int, str]]) -> None:
    if isinstance(node, dict):
        path = node.get("path")
        byte_count = node.get("bytes")
        lines = node.get("lf_lines", node.get("lines"))
        sha = node.get("sha256")
        if isinstance(path, str) and isinstance(byte_count, int) and isinstance(lines, int) and isinstance(sha, str):
            key = normalized(path)
            value = (byte_count, lines, sha.lower())
            require(key not in out or out[key] == value, f"conflicting identity in QA for {key}")
            out[key] = value
        for value in node.values():
            identity_index(value, out)
    elif isinstance(node, list):
        for value in node:
            identity_index(value, out)


def verify_baseline_receipt() -> dict[str, Any]:
    raw = disciplined(BASELINE_RECEIPT_PATH)
    require(identity(raw) == BASELINE_RECEIPT_IDENTITY, "baseline cumulative receipt identity drift")
    baseline = json.loads(raw)
    require(
        baseline.get("status") == "PASS"
        and baseline.get("receipt_kind") == "cumulative_backend_boundary"
        and baseline.get("laboratory_id") == "D60-LAB01"
        and baseline.get("cumulative", {}).get("records") == PREFIX_TOTAL[0]
        and baseline.get("cumulative", {}).get("bytes") == PREFIX_TOTAL[1]
        and baseline.get("cumulative", {}).get("bundle_sha256") == PREFIX_TOTAL[2]
        and baseline.get("replay", {}).get("status") == "PASS"
        and baseline.get("replay", {}).get("exact_file_matches") == len(FILES)
        and baseline.get("replay", {}).get("temporary_replay_removed") is True,
        "baseline receipt does not prove the exact Lab 1 cumulative boundary",
    )
    return baseline


def verify_inputs(sealed: dict[str, tuple[int, int, str]] | None = None) -> dict[str, Any]:
    raw = {relative: disciplined(relative) for relative in INPUT_PATHS}
    identities = {relative: identity(value) for relative, value in raw.items()}
    if sealed is not None:
        require(identities == sealed, "sealed input identity drift")

    combined = json.loads(raw[COMBINED_PATH].decode("utf-8"))
    require(
        combined.get("status") == "PASS"
        and combined.get("receipt_kind") == "computation_laboratory_source_execution_review_closure"
        and combined.get("laboratory_id") == LAB_ID
        and combined.get("edition_unit_id") == EDITION_UNIT_ID,
        "combined QA is not the final Lab 2 closure",
    )
    require(combined.get("course_route_unit_ids") == list(ROUTES), "combined QA route scope drift")
    require(combined.get("severity_census") == {"P1": 0, "P2": 0, "P3": 0}, "combined QA findings remain")
    require(combined.get("checks", {}).get("excluded_fomberg_problem_bank_used") is False, "excluded Fomberg problem-bank use claimed")
    require(combined.get("checks", {}).get("route_scope_D60_R08_only") == "PASS", "combined QA does not close R08-only scope")
    bound: dict[str, tuple[int, int, str]] = {}
    identity_index(combined, bound)
    for relative in (*LEARNER_PATHS, TERMINOLOGY_PATH, STATIC_PATH, *REVIEW_PATHS, EXECUTION_PATH):
        require(bound.get(relative) == identities[relative], f"combined QA does not bind current {relative}")

    static = json.loads(raw[STATIC_PATH].decode("utf-8"))
    require(static.get("status") == "PASS" and static.get("laboratory_id") == LAB_ID, "static QA mismatch")
    require(static.get("course_route_unit_ids") == list(ROUTES), "static QA route mismatch")
    require(static.get("excluded_fomberg_problem_bank_used") is False, "static QA reports excluded source use")
    require(static.get("severity_counts") == {"P1": 0, "P2": 0, "P3": 0}, "static QA findings remain")
    structure = static.get("structure", {})
    require(
        structure.get("stable_ids") == 25
        and structure.get("tasks") == 6
        and structure.get("hints") == 1
        and structure.get("complete_solution") is True
        and structure.get("tests") == 6,
        "static QA learner-surface census mismatch",
    )

    review_kinds = {
        CODE_PATH: "independent_code",
        MATH_PATH: "independent_mathematics",
        LANGUAGE_PATH: "independent_source_language",
    }
    for relative, kind in review_kinds.items():
        receipt = json.loads(raw[relative].decode("utf-8"))
        require(
            receipt.get("status") == "PASS"
            and receipt.get("review_kind") == kind
            and receipt.get("laboratory_id") == LAB_ID,
            f"{kind} review mismatch",
        )
        require(receipt.get("course_route_unit_ids") == list(ROUTES), f"{kind} route scope drift")
        require(receipt.get("independent_from_production") is True, f"{kind} review not independent")
        require(receipt.get("reader_sha256") == identities[SOURCE_PATH][2], f"{kind} review binds stale reader")
        require(receipt.get("severity_census") == {"P1": 0, "P2": 0, "P3": 0}, f"{kind} findings remain")

    execution = json.loads(raw[EXECUTION_PATH].decode("utf-8"))
    require(
        execution.get("status") == "PASS"
        and execution.get("receipt_kind") == "offline_deterministic_execution"
        and execution.get("laboratory_id") == LAB_ID
        and execution.get("course_route_unit_ids") == list(ROUTES),
        "execution receipt mismatch",
    )
    require(execution.get("program_runs") == execution.get("test_runs") == 2, "execution run census mismatch")
    require(
        execution.get("tests_per_run") == 6
        and execution.get("all_exit_codes_zero") is True
        and execution.get("program_stdout_matches_expected_output") is True
        and execution.get("program_stdout_byte_identical_between_runs") is True,
        "execution closure mismatch",
    )
    require(
        execution.get("runtime", {}).get("network_used") is False
        and execution.get("runtime", {}).get("standard_library_only") is True,
        "execution is not closed offline/standard-library evidence",
    )
    return {"raw": raw, "identities": identities, "combined": combined}


def parse_frontmatter(text: str) -> str:
    require(text.startswith("---\n"), "source frontmatter does not start at byte zero")
    close = text.find("\n---\n", 4)
    require(close > 4, "source frontmatter is not closed")
    frontmatter = text[4:close]
    for key, expected in (
        ("lang", "id-ID"), ("course_id", "D60"), ("laboratory_id", LAB_ID),
        ("edition_unit_id", EDITION_UNIT_ID), ("license", "CC BY-SA 4.0"),
    ):
        match = re.search(rf"(?m)^{re.escape(key)}:\s*[\"']?([^\"'\n]+?)[\"']?\s*$", frontmatter)
        require(match is not None and match.group(1).strip() == expected, f"frontmatter mismatch: {key}")
    route_match = re.search(r"(?m)^course_route_unit_ids:\s*(\[[^\n]+\])\s*$", frontmatter)
    require(route_match is not None and tuple(json.loads(route_match.group(1))) == ROUTES, "frontmatter route mismatch")
    require("Materi asli edisi" in frontmatter and "bukan bagian dari sumber Roberts atau Fomberg" in frontmatter, "original/source demarcation absent")
    require(MODEL in frontmatter, "model provenance absent from frontmatter")
    return frontmatter


def parse_reader(raw: bytes) -> dict[str, Any]:
    text = raw.decode("utf-8")
    parse_frontmatter(text)
    lines = raw.splitlines(keepends=True)
    decoded = [line.decode("utf-8").rstrip("\n") for line in lines]
    heading_re = re.compile(r"^(#{1,6})\s+(.+?)\s+\{#(" + re.escape(LOCAL_ROOT) + r"(?:-[a-z0-9]+)*)\}\s*$")
    fence_re = re.compile(r"^:::\s+\{\.(exercise|hint)\s+#(" + re.escape(LOCAL_ROOT) + r"(?:-[a-z0-9]+)*)\}\s*$")
    headings: list[tuple[int, int, str, str]] = []
    fences: list[tuple[int, str, str]] = []
    for number, line in enumerate(decoded, 1):
        heading = heading_re.match(line)
        if heading:
            headings.append((number, len(heading.group(1)), heading.group(3), heading.group(2)))
        fence = fence_re.match(line)
        if fence:
            fences.append((number, fence.group(2), fence.group(1)))
    observed = {item[2] for item in headings} | {item[1] for item in fences}
    require(observed == set(ID_KINDS) and len(observed) == 25, f"stable-ID inventory mismatch: {sorted(set(ID_KINDS) - observed)}")

    items: dict[str, dict[str, Any]] = {}
    for index, (start, level, local_id, title) in enumerate(headings):
        if local_id == LOCAL_ROOT:
            end = len(lines)
        else:
            following = [line_no for line_no, next_level, _, _ in headings[index + 1:] if next_level <= level]
            end = (following[0] - 1) if following else len(lines)
        items[local_id] = {"span": (start, end), "title": title, "source_role": "heading"}
    for start, local_id, fence_kind in fences:
        closing = next((line_no for line_no in range(start + 1, len(lines) + 1) if decoded[line_no - 1] == ":::"), None)
        require(closing is not None, f"unclosed fenced block: {local_id}")
        first_content = next((decoded[line_no - 1] for line_no in range(start + 1, closing) if decoded[line_no - 1].strip()), local_id)
        title = re.sub(r"[*`]", "", first_content).strip().rstrip(".")
        items[local_id] = {"span": (start, closing), "title": title, "source_role": fence_kind}
    require(set(items) == set(ID_KINDS), "parsed item inventory mismatch")
    for local_id, item in items.items():
        start, end = item["span"]
        require(local_id in decoded[start - 1] and 1 <= start <= end <= len(lines), f"invalid anchored span: {local_id}")
        item["target_locator"] = {
            "content_sha256": digest(b"".join(lines[start - 1:end])),
            "file_sha256": digest(raw),
            "line_end": end,
            "line_start": start,
            "path": SOURCE_PATH,
        }
    return {"items": items, "lines": lines, "reader_sha256": digest(raw)}


def source_locator() -> dict[str, Any]:
    return {
        "kind": "edition_original",
        "path": SOURCE_PATH,
        "precision": "exact_target_span",
        "source_corpus_used": False,
    }


def concepts_for(local_id: str) -> list[str]:
    exact: dict[str, tuple[str, ...]] = {
        f"{LOCAL_ROOT}-status": ("concept:simplicial-homology", "concept:boundary-map", "concept:real-projective-plane", NEW_CONCEPTS[494], NEW_CONCEPTS[502]),
        f"{LOCAL_ROOT}-prerequisites": ("concept:chain", "concept:boundary-map", "concept:cycle", "concept:homology"),
        f"{LOCAL_ROOT}-objectives": (NEW_CONCEPTS[493], NEW_CONCEPTS[494], NEW_CONCEPTS[495], NEW_CONCEPTS[497], NEW_CONCEPTS[498]),
        f"{LOCAL_ROOT}-data": ("concept:simplex", "concept:simplex-face", "concept:simplicial-complex", NEW_CONCEPTS[499]),
        f"{LOCAL_ROOT}-matrices": ("concept:boundary-map", "concept:boundary-of-a-simplex", NEW_CONCEPTS[493], NEW_CONCEPTS[501]),
        f"{LOCAL_ROOT}-task-001": ("concept:chain-complex", NEW_CONCEPTS[497]),
        f"{LOCAL_ROOT}-task-002": ("concept:simplicial-complex", "concept:orientation", NEW_CONCEPTS[499]),
        f"{LOCAL_ROOT}-task-003": ("concept:chain", "concept:boundary-map", "concept:chain-boundary", NEW_CONCEPTS[501]),
        f"{LOCAL_ROOT}-task-004": ("concept:homology", NEW_CONCEPTS[494], NEW_CONCEPTS[495], NEW_CONCEPTS[496], NEW_CONCEPTS[497]),
        f"{LOCAL_ROOT}-task-005": ("concept:cycle", "concept:cocycle", "concept:homology-class", NEW_CONCEPTS[498], NEW_CONCEPTS[502]),
        f"{LOCAL_ROOT}-task-006": ("concept:orientation", NEW_CONCEPTS[494], NEW_CONCEPTS[500]),
        f"{LOCAL_ROOT}-program": ("concept:chain-complex", NEW_CONCEPTS[494], NEW_CONCEPTS[497], NEW_CONCEPTS[502]),
        f"{LOCAL_ROOT}-tests": ("concept:boundary-map", "concept:homology", NEW_CONCEPTS[497], NEW_CONCEPTS[500]),
        f"{LOCAL_ROOT}-expected-output": ("concept:real-projective-plane", "concept:homology", NEW_CONCEPTS[494], NEW_CONCEPTS[502]),
        f"{LOCAL_ROOT}-interpretation": ("concept:free-abelian-group", "concept:homology", NEW_CONCEPTS[494], NEW_CONCEPTS[495], NEW_CONCEPTS[496]),
        f"{LOCAL_ROOT}-sol-surface": ("concept:simplicial-complex", "concept:orientation", "concept:real-projective-plane", NEW_CONCEPTS[499]),
        f"{LOCAL_ROOT}-sol-boundaries": ("concept:boundary-map", "concept:chain-boundary", NEW_CONCEPTS[493], NEW_CONCEPTS[501]),
        f"{LOCAL_ROOT}-sol-smith": ("concept:homology", NEW_CONCEPTS[494], NEW_CONCEPTS[495], NEW_CONCEPTS[496], NEW_CONCEPTS[497]),
        f"{LOCAL_ROOT}-sol-torsion": ("concept:cycle", "concept:cocycle", "concept:homology-class", NEW_CONCEPTS[498], NEW_CONCEPTS[502]),
        f"{LOCAL_ROOT}-sol-control": ("concept:orientation", "concept:simplicial-homology", NEW_CONCEPTS[494], NEW_CONCEPTS[500]),
        f"{LOCAL_ROOT}-reproducibility": ("concept:chain-complex", NEW_CONCEPTS[497], NEW_CONCEPTS[502]),
        f"{LOCAL_ROOT}-rights": ("concept:simplicial-homology", "concept:homology"),
    }
    if local_id in (LOCAL_ROOT, f"{LOCAL_ROOT}-hint", f"{LOCAL_ROOT}-solution"):
        return list(ALL_LAB_CONCEPTS)
    return list(exact.get(local_id, ("concept:simplicial-homology",)))


def unit_record(local_id: str, order: int, parsed: dict[str, Any]) -> dict[str, Any]:
    kind, _ = ID_KINDS[local_id]
    ident = f"unit:{local_id}"
    record = {
        **common("unit", ident),
        "authority_context_ids": [COURSE, PROGRAM, FOMBERG_EDITION, FOMBERG_RESOURCE],
        "authority_context_only": True,
        "concept_ids": concepts_for(local_id),
        "course_id": COURSE,
        "course_route_unit_ids": list(ROUTES),
        "display_title": parsed["items"][local_id]["title"],
        "edition_context_only": True,
        "edition_id": FOMBERG_EDITION,
        "edition_unit_id": EDITION_UNIT_ID,
        "laboratory_id": LAB_ID,
        "locale": "id-ID",
        "model_provenance": MODEL,
        "order": 43 if local_id == LOCAL_ROOT else order,
        "original_layer": True,
        "parent_id": COURSE if local_id == LOCAL_ROOT else ROOT_UNIT,
        "path": [ROOT_UNIT] if local_id == LOCAL_ROOT else [ROOT_UNIT, ident],
        "program_id": PROGRAM,
        "provenance_relation": "edition_original",
        "resource_context_only": True,
        "resource_id": FOMBERG_RESOURCE,
        "rights_component_id": LAB_RIGHTS,
        "source_corpus_used": False,
        "source_local_id": local_id,
        "source_locator": source_locator(),
        "target_locator": parsed["items"][local_id]["target_locator"],
        "translation_state": "structurally_verified",
        "unit_kind": kind,
    }
    if local_id == LOCAL_ROOT:
        record.update({
            "execution_mode": "offline",
            "laboratory_kind": "computation_laboratory",
            "primary_course_route_unit_id": "D60-R08",
            "reader_scope": "six_tasks_one_hint_full_solution_program_tests_expected_output_interpretation",
            "secondary_course_route_unit_ids": [],
        })
    task = re.fullmatch(re.escape(LOCAL_ROOT) + r"-task-(\d{3})", local_id)
    if task:
        record["laboratory_task_number"] = int(task.group(1))
        record["primary_course_route_unit_id"] = "D60-R08"
        record["secondary_course_route_unit_ids"] = []
    if kind == "solution":
        record["solution_status"] = "complete_checked_solution"
    return record


def segment_from_unit(unit: dict[str, Any]) -> dict[str, Any]:
    local_id = unit["source_local_id"]
    _, segment_kind = ID_KINDS[local_id]
    optional = {
        key: unit[key]
        for key in (
            "authority_context_ids", "authority_context_only", "course_route_unit_ids",
            "edition_context_only", "edition_unit_id", "laboratory_id",
            "laboratory_task_number", "model_provenance", "original_layer",
            "primary_course_route_unit_id", "resource_context_only",
            "secondary_course_route_unit_ids", "solution_status", "source_corpus_used",
        )
        if key in unit
    }
    return {
        **common("segment", unit["id"].replace("unit:", "segment:", 1)),
        **optional,
        "concept_ids": unit["concept_ids"],
        "edition_id": FOMBERG_EDITION,
        "locale": "id-ID",
        "order": unit["order"],
        "provenance_relation": "edition_original",
        "resource_id": FOMBERG_RESOURCE,
        "rights_component_id": LAB_RIGHTS,
        "segment_kind": segment_kind,
        "source_local_id": local_id,
        "source_locator": unit["source_locator"],
        "target_locator": unit["target_locator"],
        "translation_state": "structurally_verified",
        "unit_id": unit["id"],
    }


def relation(ident: str, relation_type: str, from_id: str, to_id: str, note: str, **extra: Any) -> dict[str, Any]:
    return {**common("relation", ident), "from_id": from_id, "note": note, "relation_type": relation_type, "to_id": to_id, **extra}


def artifact(ident: str, relative: str, media_type: str, qa_ids: list[str], state: str, identities: dict[str, tuple[int, int, str]]) -> dict[str, Any]:
    byte_count, _, sha = identities[relative]
    return {
        **common("artifact", ident),
        "bytes": byte_count,
        "edition_unit_id": EDITION_UNIT_ID,
        "laboratory_id": LAB_ID,
        "locale": "id-ID",
        "manifest_artifact_id": None,
        "media_type": media_type,
        "path": relative,
        "qa_event_ids": qa_ids,
        "rights_component_id": LAB_RIGHTS,
        "sha256": sha,
        "toolchain": f"Original {LAB_ID} evidence; {MODEL}; semantic admission only.",
        "translation_state": state,
        "unit_id": ROOT_UNIT,
    }


def build_additions(data: dict[str, Any], parsed: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    order = {local_id: number for number, local_id in enumerate(ID_KINDS, 1)}
    units = [unit_record(local_id, order[local_id], parsed) for local_id in ID_KINDS]
    segments = [segment_from_unit(unit) for unit in units]

    concepts = [
        {
            **common("concept", NEW_CONCEPTS[number]),
            "canonical_label": source_term,
            "domain": domain,
            "locale_neutral": True,
        }
        for number, source_term, _, domain, _, _ in TERM_SPECS
    ]
    terms = [
        {
            **common("term", f"term:{LOCAL_ROOT}-term-{number:04d}:id-ID"),
            "concept_id": NEW_CONCEPTS[number],
            "evidence_segment_id": f"segment:{evidence_local_id}",
            "locale": "id-ID",
            "preferred": preferred,
            "register": "textbook",
            "rejected_forms": [],
            "rights_component_id": LAB_RIGHTS,
            "scope_unit_id": ROOT_UNIT,
            "source_term": source_term,
            "terminology_control_id": f"O012-TERM-{number:04d}",
            "terminology_status": "admitted",
            "usage_note": usage_note,
            "variants": [],
        }
        for number, source_term, preferred, _, evidence_local_id, usage_note in TERM_SPECS
    ]
    rights = [{
        **common("rights", LAB_RIGHTS),
        "attribution": f"Original {LAB_ID} computation laboratory prepared for the independent Indonesian O012/D60 edition.",
        "change_notice": "Edition-original laboratory layer; Roberts and Fomberg source components are neither copied nor relicensed.",
        "component_scope": [unit["id"] for unit in units],
        "license_expression": "CC-BY-SA-4.0",
        "license_url": "https://creativecommons.org/licenses/by-sa/4.0/",
        "non_endorsement": "Independent Indonesian edition; no Roberts, Fomberg, Lazarovich, or source-author endorsement.",
        "third_party_status": "No excluded Fomberg problem-bank expression is used; admitted D60-R08 authority IDs are mathematical context only.",
    }]

    qa_ids = {kind: f"qa:{LOCAL_ROOT}-{kind}" for kind in ("structure", "execution", "code", "math", "language", "mastery", "terminology")}
    artifacts = [
        artifact(f"artifact:{LOCAL_ROOT}-reader-source", SOURCE_PATH, "text/markdown", list(qa_ids.values()), "structurally_verified", data["identities"]),
        artifact(f"artifact:{LOCAL_ROOT}-python-source", PROGRAM_PATH, "text/x-python", [qa_ids["execution"], qa_ids["code"], qa_ids["mastery"]], "built", data["identities"]),
        artifact(f"artifact:{LOCAL_ROOT}-tests", TEST_PATH, "text/x-python", [qa_ids["execution"], qa_ids["code"]], "built", data["identities"]),
        artifact(f"artifact:{LOCAL_ROOT}-expected-output", EXPECTED_PATH, "text/plain", [qa_ids["execution"], qa_ids["code"]], "built", data["identities"]),
        artifact(f"artifact:{LOCAL_ROOT}-static-qa", STATIC_PATH, "application/json", [qa_ids["structure"], qa_ids["mastery"], qa_ids["terminology"]], "built", data["identities"]),
        artifact(f"artifact:{LOCAL_ROOT}-code-review", CODE_PATH, "application/json", [qa_ids["code"]], "built", data["identities"]),
        artifact(f"artifact:{LOCAL_ROOT}-math-review", MATH_PATH, "application/json", [qa_ids["math"]], "mathematically_reviewed", data["identities"]),
        artifact(f"artifact:{LOCAL_ROOT}-language-review", LANGUAGE_PATH, "application/json", [qa_ids["language"], qa_ids["terminology"]], "language_reviewed", data["identities"]),
        artifact(f"artifact:{LOCAL_ROOT}-execution-receipt", EXECUTION_PATH, "application/json", [qa_ids["execution"]], "built", data["identities"]),
        artifact(f"artifact:{LOCAL_ROOT}-qa-receipt", COMBINED_PATH, "application/json", list(qa_ids.values()), "built", data["identities"]),
    ]
    qa_events = [
        {**common("qa_event", qa_ids["structure"]), "laboratory_id": LAB_ID, "note": "Twenty-five stable IDs, six tasks, one hint, a full solution, D60-R08-only route metadata, LF/UTF-8, rights, provenance, and privacy checks passed.", "qa_type": "structure", "result": "passed", "unit_id": ROOT_UNIT, "witness_artifact_ids": [f"artifact:{LOCAL_ROOT}-reader-source", f"artifact:{LOCAL_ROOT}-static-qa", f"artifact:{LOCAL_ROOT}-qa-receipt"]},
        {**common("qa_event", qa_ids["execution"]), "laboratory_id": LAB_ID, "note": "The standard-library program and six-test suite each ran twice; program stdout was deterministic and byte-identical to the expected output.", "qa_type": "execution", "result": "passed", "unit_id": ROOT_UNIT, "witness_artifact_ids": [f"artifact:{LOCAL_ROOT}-python-source", f"artifact:{LOCAL_ROOT}-tests", f"artifact:{LOCAL_ROOT}-expected-output", f"artifact:{LOCAL_ROOT}-execution-receipt"]},
        {**common("qa_event", qa_ids["code"]), "laboratory_id": LAB_ID, "note": "Independent code review checked Smith oracles, malformed certificates, basis changes, isolated execution, standard-library scope, and absence of post-import file or network access with P1=P2=P3=0.", "qa_type": "code", "result": "passed", "unit_id": ROOT_UNIT, "witness_artifact_ids": [f"artifact:{LOCAL_ROOT}-code-review", f"artifact:{LOCAL_ROOT}-qa-receipt"]},
        {**common("qa_event", qa_ids["math"]), "laboratory_id": LAB_ID, "note": "Independent mathematics review recomputed boundary ranks, Smith factors, homology, torsion witnesses, surface checks, and sphere control with P1=P2=P3=0.", "qa_type": "math", "result": "passed", "unit_id": ROOT_UNIT, "witness_artifact_ids": [f"artifact:{LOCAL_ROOT}-math-review", f"artifact:{LOCAL_ROOT}-qa-receipt"]},
        {**common("qa_event", qa_ids["language"]), "laboratory_id": LAB_ID, "note": "Independent final id-ID source-language review passed with exact R08 scope, resolved links, natural terminology, rights, and provenance.", "qa_type": "language", "result": "passed", "unit_id": ROOT_UNIT, "witness_artifact_ids": [f"artifact:{LOCAL_ROOT}-language-review", f"artifact:{LOCAL_ROOT}-qa-receipt"]},
        {**common("qa_event", qa_ids["mastery"]), "laboratory_id": LAB_ID, "note": "Six tasks share one stable hint and one complete checked solution, with source, tests, expected output, interpretation, exact certificates, a torsion witness, and a sphere control.", "qa_type": "mastery", "result": "passed", "unit_id": ROOT_UNIT, "witness_artifact_ids": [f"artifact:{LOCAL_ROOT}-reader-source", f"artifact:{LOCAL_ROOT}-python-source", f"artifact:{LOCAL_ROOT}-static-qa"]},
        {**common("qa_event", qa_ids["terminology"]), "laboratory_id": LAB_ID, "note": "O012-TERM-0493 through O012-TERM-0502 are mapped to ten locale-neutral concepts and exact learner evidence segments.", "qa_type": "terminology", "result": "passed", "unit_id": ROOT_UNIT, "witness_artifact_ids": [f"artifact:{LOCAL_ROOT}-language-review", f"artifact:{LOCAL_ROOT}-static-qa"]},
    ]

    relations = [
        relation(f"relation:contains:o012-d60:lab02", "contains", COURSE, ROOT_UNIT, f"The O012/D60 course contains {LAB_ID} as an original computation laboratory.", laboratory_id=LAB_ID, course_route_unit_ids=list(ROUTES)),
        relation(f"relation:contains:{LOCAL_ROOT}-rights:root", "contains", LAB_RIGHTS, ROOT_UNIT, f"The original CC BY-SA 4.0 component rights bind the complete {LAB_ID} graph.", laboratory_id=LAB_ID, rights_mapping_role="direct_component_binding"),
        relation(f"relation:contains:o012-d60-integrated-rights:lab02-original", "contains", INTEGRATED_RIGHTS, LAB_RIGHTS, f"The integrated route contains the independently licensed {LAB_ID} component without altering source licenses.", laboratory_id=LAB_ID, rights_mapping_role="integrated_route_component"),
    ]
    for local_id in ID_KINDS:
        if local_id == LOCAL_ROOT:
            continue
        relations.append(relation(f"relation:contains:{LOCAL_ROOT}:{local_id.removeprefix(LOCAL_ROOT + '-')}", "contains", ROOT_UNIT, f"unit:{local_id}", f"{LAB_ID} contains the stable learner surface {local_id}.", laboratory_id=LAB_ID))
    hint = f"unit:{LOCAL_ROOT}-hint"
    solution = f"unit:{LOCAL_ROOT}-solution"
    for number in range(1, 7):
        exercise = f"unit:{LOCAL_ROOT}-task-{number:03d}"
        relations.append(relation(f"relation:hints:{LOCAL_ROOT}-hint:task-{number:03d}", "hints", hint, exercise, f"Shared stable hint for {LAB_ID} task {number}.", laboratory_id=LAB_ID, laboratory_task_number=number))
        relations.append(relation(f"relation:solves:{LOCAL_ROOT}-solution:task-{number:03d}", "solves", solution, exercise, f"Complete checked solution for {LAB_ID} task {number}.", laboratory_id=LAB_ID, laboratory_task_number=number, solution_status="complete_checked_solution"))
        for dep_order, anchor in enumerate(TASK_DEPENDENCIES[number], 1):
            slug = re.sub(r"[^a-z0-9]+", "-", anchor.lower()).strip("-")
            relations.append(relation(f"relation:depends-on:{LOCAL_ROOT}-task-{number:03d}:{dep_order:02d}:{slug}", "depends-on", exercise, anchor, f"{LAB_ID} task {number} requires the admitted D60-R08 result or unit {anchor}.", laboratory_id=LAB_ID, laboratory_task_number=number, dependency_order=dep_order, dependency_role="laboratory_prerequisite", course_route_unit_id="D60-R08"))
    relations.append(relation(f"relation:xref:{LOCAL_ROOT}:d60-r08", "xref", ROOT_UNIT, ROUTE_ANCHORS["D60-R08"], f"Primary route mapping for {LAB_ID}: D60-R08.", laboratory_id=LAB_ID, course_route_unit_id="D60-R08", route_mapping_role="primary", route_source_anchor_id=ROUTE_ANCHORS["D60-R08"]))

    additions = {name: [] for name in FILES}
    additions["units.jsonl"] = units
    additions["segments.jsonl"] = segments
    additions["concepts.jsonl"] = concepts
    additions["terms.jsonl"] = terms
    additions["rights.jsonl"] = rights
    additions["artifacts.jsonl"] = artifacts
    additions["qa.jsonl"] = qa_events
    additions["relations.jsonl"] = relations
    for name in FILES:
        additions[name] = sorted(additions[name], key=lambda record: record["id"])
    return additions


def suffixes(additions: dict[str, list[dict[str, Any]]]) -> dict[str, bytes]:
    return {name: b"".join(canon(record) for record in additions[name]) for name in FILES}


def bundle(raw_by_file: dict[str, bytes]) -> tuple[int, int, str]:
    state = hashlib.sha256()
    records = byte_count = 0
    for name in FILES:
        raw = raw_by_file[name]
        records += len(raw.splitlines())
        byte_count += len(raw)
        state.update(name.encode("utf-8"))
        state.update(b"\0")
        state.update(raw)
    return records, byte_count, state.hexdigest()


def parse_records(raw_by_file: dict[str, bytes]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    seen: set[str] = set()
    for name in FILES:
        for line_number, line in enumerate(raw_by_file[name].splitlines(), 1):
            require(line and canon(json.loads(line)) == line + b"\n", f"noncanonical JSON at {name}:{line_number}")
            record = json.loads(line)
            require(record["id"] not in seen, f"duplicate prefix ID: {record['id']}")
            seen.add(record["id"])
            records.append(record)
    return records


def verify_prefix(backend: Path = BACKEND) -> tuple[dict[str, bytes], list[dict[str, Any]]]:
    raw_by_file: dict[str, bytes] = {}
    for name in FILES:
        path = backend / name
        require(path.is_file(), f"backend file missing: {name}")
        raw = path.read_bytes()
        expected_records, expected_bytes, expected_sha = PREFIX[name]
        observed = (len(raw.splitlines()), len(raw), digest(raw))
        require(observed == (expected_records, expected_bytes, expected_sha), f"immutable prefix mismatch: {name}: {observed}")
        raw_by_file[name] = raw
    require(bundle(raw_by_file) == PREFIX_TOTAL, f"immutable bundle mismatch: {bundle(raw_by_file)}")
    return raw_by_file, parse_records(raw_by_file)


def load_generic():
    path = LANE / "scripts/validate-backend.py"
    spec = importlib.util.spec_from_file_location("o012_generic_backend_for_lab02", path)
    require(spec is not None and spec.loader is not None, "cannot load generic backend validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_terminology_csv() -> None:
    rows = list(csv.DictReader(io.StringIO(disciplined(TERMINOLOGY_PATH).decode("utf-8"))))
    by_id = {row["term_id"]: row for row in rows}
    for number, source_term, preferred, domain, _, usage_note in TERM_SPECS:
        control = f"O012-TERM-{number:04d}"
        require(control in by_id, f"terminology control missing: {control}")
        row = by_id[control]
        require(
            (row["source_term"], row["id_ID"], row["scope"], row["status"], row["note"])
            == (source_term, preferred, domain, "admitted", usage_note),
            f"terminology control drift: {control}",
        )


def validate_semantics(prefix_records: list[dict[str, Any]], additions: dict[str, list[dict[str, Any]]], data: dict[str, Any], parsed: dict[str, Any]) -> dict[str, Any]:
    added = [record for name in FILES for record in additions[name]]
    records = prefix_records + added
    by_id = {record["id"]: record for record in records}
    require(len(by_id) == len(records), "global ID collision")
    generic = load_generic()
    try:
        generic.validate_shapes(records)
        generic.validate_references(records, by_id)
        generic.validate_artifact_manifests(records, LANE)
    except Exception as exc:
        raise SystemExit(f"Lab 2 backend producer FAIL: merged schema/reference validation failed: {exc}")

    required_context = {
        COURSE, PROGRAM, FOMBERG_EDITION, FOMBERG_RESOURCE, INTEGRATED_RIGHTS,
        *EXISTING_CONCEPTS, *ROUTE_ANCHORS.values(), *R08_DEPENDENCY_ANCHORS,
    }
    require(required_context <= by_id.keys(), f"required context IDs absent: {sorted(required_context - by_id.keys())}")
    expected_counts = {
        "artifacts.jsonl": 10,
        "assets.jsonl": 0,
        "authority.jsonl": 0,
        "concepts.jsonl": 10,
        "corrections.jsonl": 0,
        "qa.jsonl": 7,
        "relations.jsonl": 54,
        "rights.jsonl": 1,
        "segments.jsonl": 25,
        "terms.jsonl": 10,
        "units.jsonl": 25,
    }
    actual_counts = {name: len(additions[name]) for name in FILES}
    require(actual_counts == expected_counts, f"suffix record census mismatch: {actual_counts}")

    units = additions["units.jsonl"]
    segments = additions["segments.jsonl"]
    require({record["source_local_id"] for record in units} == set(ID_KINDS), "unit stable-ID mapping mismatch")
    require({record["source_local_id"] for record in segments} == set(ID_KINDS), "segment stable-ID mapping mismatch")
    require(all(record.get("course_route_unit_ids") == ["D60-R08"] for record in units + segments), "Lab 2 unit/segment route scope is not R08-only")
    segments_by_local = {record["source_local_id"]: record for record in segments}
    for unit in units:
        segment = segments_by_local[unit["source_local_id"]]
        require(segment["unit_id"] == unit["id"] and segment["target_locator"] == unit["target_locator"], f"unit/segment mismatch: {unit['id']}")
        start = unit["target_locator"]["line_start"]
        require(unit["source_local_id"].encode("utf-8") in parsed["lines"][start - 1], f"target locator does not start at stable ID: {unit['id']}")
        require(unit["rights_component_id"] == segment["rights_component_id"] == LAB_RIGHTS, f"rights mismatch: {unit['id']}")
        require(unit["original_layer"] is True and unit["source_corpus_used"] is False, f"original/source demarcation mismatch: {unit['id']}")
        require(unit["model_provenance"] == segment["model_provenance"] == MODEL, f"model provenance mismatch: {unit['id']}")
        require(all(concept in by_id and by_id[concept]["entity_type"] == "concept" for concept in unit["concept_ids"]), f"unresolved concept mapping: {unit['id']}")

    rights = additions["rights.jsonl"][0]
    require(rights["license_expression"] == "CC-BY-SA-4.0" and set(rights["component_scope"]) == {unit["id"] for unit in units}, "rights component scope mismatch")
    require("neither copied nor relicensed" in rights["change_notice"], "source-license demarcation weakened")
    tasks = {f"unit:{LOCAL_ROOT}-task-{number:03d}" for number in range(1, 7)}
    hint_edges = [record for record in additions["relations.jsonl"] if record["relation_type"] == "hints"]
    solve_edges = [record for record in additions["relations.jsonl"] if record["relation_type"] == "solves"]
    require({record["to_id"] for record in hint_edges} == tasks and len(hint_edges) == 6, "hint closure mismatch")
    require({record["to_id"] for record in solve_edges} == tasks and len(solve_edges) == 6, "solution closure mismatch")
    require(all(record.get("solution_status") == "complete_checked_solution" for record in solve_edges), "solution status mismatch")
    route_edges = [record for record in additions["relations.jsonl"] if record["relation_type"] == "xref"]
    require({(record["course_route_unit_id"], record["to_id"]) for record in route_edges} == set(ROUTE_ANCHORS.items()), "route xref mismatch")
    dependency_edges = [record for record in additions["relations.jsonl"] if record["relation_type"] == "depends-on"]
    expected_dependencies = {
        (f"unit:{LOCAL_ROOT}-task-{number:03d}", anchor)
        for number, anchors in TASK_DEPENDENCIES.items()
        for anchor in anchors
    }
    require({(record["from_id"], record["to_id"]) for record in dependency_edges} == expected_dependencies, "dependency graph mismatch")
    require(all(record["to_id"] in R08_DEPENDENCY_ANCHORS and record.get("course_route_unit_id") == "D60-R08" for record in dependency_edges), "dependency escapes admitted R08 anchors")
    require(all(by_id[record["to_id"]].get("course_route_unit_id") == "D60-R08" for record in dependency_edges), "dependency target is not an admitted R08 unit")

    term_controls = {record["terminology_control_id"] for record in additions["terms.jsonl"]}
    require(term_controls == {f"O012-TERM-{number:04d}" for number, *_ in TERM_SPECS}, "term-control mapping mismatch")
    require(all(record["evidence_segment_id"] in by_id for record in additions["terms.jsonl"]), "term evidence segment missing")
    require(Counter(record["qa_type"] for record in additions["qa.jsonl"]) == Counter({"structure": 1, "execution": 1, "code": 1, "math": 1, "language": 1, "mastery": 1, "terminology": 1}), "QA event census mismatch")
    for record in additions["artifacts.jsonl"]:
        expected = data["identities"][record["path"]]
        require((record["bytes"], record["sha256"]) == (expected[0], expected[2]), f"artifact identity mismatch: {record['path']}")

    joined = b"".join(suffixes(additions)[name] for name in FILES)
    joined_lower = joined.lower()
    markers = (b"c:" + b"\\users\\", b"github_" + b"pat_", b"gh" + b"p_", b"access_" + b"token", b"authorization" + b": bearer")
    require(not any(marker in joined_lower for marker in markers), "private path or credential marker in suffix")
    require(b"D60-R09" not in joined, "Lab 2 suffix overclaims D60-R09")
    return {
        "added_records": len(added),
        "merged_records": len(records),
        "stable_ids": 25,
        "tasks": 6,
        "hints": 1,
        "complete_solutions": 1,
        "program_sources": 1,
        "test_suites": 1,
        "expected_outputs": 1,
        "new_concepts": 10,
        "new_terms": 10,
        "dependency_edges": len(dependency_edges),
        "dependency_scope": "D60-R08_only",
        "route_edges": len(route_edges),
        "independent_reviews": 3,
        "schema_shapes": "PASS",
        "global_references": "PASS",
        "artifact_evidence": "PASS",
        "rights_and_provenance": "PASS",
        "append_only_ready": "PASS",
    }


def record_plan(additions: dict[str, list[dict[str, Any]]], data: dict[str, Any], semantic: dict[str, Any]) -> dict[str, Any]:
    raw = suffixes(additions)
    return {
        "laboratory_id": LAB_ID,
        "edition_unit_id": EDITION_UNIT_ID,
        "immutable_prefix": {"records": PREFIX_TOTAL[0], "bytes": PREFIX_TOTAL[1], "bundle_sha256": PREFIX_TOTAL[2]},
        "baseline_receipt": {
            "path": BASELINE_RECEIPT_PATH,
            "bytes": BASELINE_RECEIPT_IDENTITY[0],
            "lf_lines": BASELINE_RECEIPT_IDENTITY[1],
            "sha256": BASELINE_RECEIPT_IDENTITY[2],
        },
        "input_identities": {
            relative: {"bytes": value[0], "lf_lines": value[1], "sha256": value[2]}
            for relative, value in sorted(data["identities"].items())
        },
        "records_by_file": {name: len(additions[name]) for name in FILES},
        "bytes_by_file": {name: len(raw[name]) for name in FILES},
        "record_ids_by_file": {name: [record["id"] for record in additions[name]] for name in FILES},
        "semantic": semantic,
    }


def append_suffix(prefix: dict[str, bytes], additions: dict[str, list[dict[str, Any]]]) -> dict[str, bytes]:
    raw_suffixes = suffixes(additions)
    for name in FILES:
        require((BACKEND / name).read_bytes() == prefix[name], f"prefix changed immediately before append: {name}")
    for name in FILES:
        if raw_suffixes[name]:
            with (BACKEND / name).open("ab") as stream:
                stream.write(raw_suffixes[name])
    for name in FILES:
        require((BACKEND / name).read_bytes() == prefix[name] + raw_suffixes[name], f"exact binary append mismatch: {name}")
    return raw_suffixes


def main() -> int:
    require(sys.argv[1:] in ([], ["--plan"]), "accepted invocation is no arguments or --plan")
    verify_baseline_receipt()
    validate_terminology_csv()
    data = verify_inputs()
    parsed = parse_reader(data["raw"][SOURCE_PATH])
    prefix, prefix_records = verify_prefix()
    additions = build_additions(data, parsed)
    semantic = validate_semantics(prefix_records, additions, data, parsed)
    plan = record_plan(additions, data, semantic)
    if sys.argv[1:] == ["--plan"]:
        print(json.dumps(plan, ensure_ascii=False, sort_keys=True, indent=2))
        return 0

    verify_baseline_receipt()
    refreshed = verify_inputs(data["identities"])
    refreshed_parsed = parse_reader(refreshed["raw"][SOURCE_PATH])
    refreshed_additions = build_additions(refreshed, refreshed_parsed)
    refreshed_semantic = validate_semantics(prefix_records, refreshed_additions, refreshed, refreshed_parsed)
    require(record_plan(refreshed_additions, refreshed, refreshed_semantic) == plan, "sealed inputs changed deterministic plan")
    require(suffixes(refreshed_additions) == suffixes(additions), "sealed inputs changed derived suffix")
    raw_suffixes = append_suffix(prefix, additions)
    final_raw = {name: (BACKEND / name).read_bytes() for name in FILES}
    final = bundle(final_raw)
    require(final[0] == PREFIX_TOTAL[0] + semantic["added_records"], "cumulative record-count mismatch")
    print("Lab 2 append-only semantic backend extension: PASS")
    print(f"prefix_records={PREFIX_TOTAL[0]}")
    print(f"prefix_bytes={PREFIX_TOTAL[1]}")
    print(f"prefix_bundle_sha256={PREFIX_TOTAL[2]}")
    print(f"records_added={semantic['added_records']}")
    print(f"suffix_bytes={sum(len(raw_suffixes[name]) for name in FILES)}")
    print(f"cumulative_records={final[0]}")
    print(f"cumulative_bytes={final[1]}")
    print(f"backend_bundle_sha256={final[2]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
