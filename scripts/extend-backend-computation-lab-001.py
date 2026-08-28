#!/usr/bin/env python3
"""Fail-closed append-only backend admission for O012/D60 computation Lab 1."""
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
ROBERTS_EDITION = "edition:roberts-at-2019-b947ad2"
ROBERTS_RESOURCE = "resource:roberts-algebraic-topology-2019"
FOMBERG_EDITION = "edition:fomberg-at-2025-563194f"
FOMBERG_RESOURCE = "resource:fomberg-algebraic-topology-2025"
INTEGRATED_RIGHTS = "rights:o012-d60-integrated-route-cc-by-sa-4.0"
LAB_ID = "D60-LAB01"
EDITION_UNIT_ID = "O012-ORIG-LAB01"
LOCAL_ROOT = "o012-d60-lab01"
ROOT_UNIT = f"unit:{LOCAL_ROOT}"
LAB_RIGHTS = f"rights:{LOCAL_ROOT}-original-cc-by-sa-4.0"
ROUTES = ("D60-R04", "D60-R05", "D60-R06")
SOURCE_PATH = "source/id-ID/labs/computation-lab-001-monodromy-presentations.md"
PROGRAM_PATH = "source/id-ID/labs/o012_d60_lab01_monodromy.py"
TEST_PATH = "source/id-ID/labs/test_o012_d60_lab01_monodromy.py"
EXPECTED_PATH = "source/id-ID/labs/expected-output-lab01.txt"
TERMINOLOGY_PATH = "00_control/TERMINOLOGY.csv"
STATIC_PATH = "qa/computation-lab-001/STATIC_QA.json"
MATH_PATH = "qa/computation-lab-001/INDEPENDENT_MATH_REVIEW.json"
LANGUAGE_PATH = "qa/computation-lab-001/INDEPENDENT_SOURCE_LANGUAGE_REVIEW.json"
EXECUTION_PATH = "qa/computation-lab-001/EXECUTION_RECEIPT.json"
COMBINED_PATH = "qa/COMPUTATION_LAB_001_QA.json"
BASELINE_RECEIPT_PATH = "qa/BACKEND_APPEND_ONLY_CUMULATIVE_ASSESSMENTS_002_003_CUMULATIVE_RECEIPT.json"
BASELINE_RECEIPT_IDENTITY = (
    11073,
    329,
    "61e5a3791ca4cacf7a2fbe0c09f5b638afd1c2c427f8784d04b96331903d53c7",
)

FILES = (
    "artifacts.jsonl", "assets.jsonl", "authority.jsonl", "concepts.jsonl",
    "corrections.jsonl", "qa.jsonl", "relations.jsonl", "rights.jsonl",
    "segments.jsonl", "terms.jsonl", "units.jsonl",
)
PREFIX = {
    "artifacts.jsonl": (205, 168788, "0f126c6ff8ccc6344af42000ff7c48529211d6c9c8a46d712119630946a97e38"),
    "assets.jsonl": (87, 64692, "1df40f8f6ca4f2fbfbe8a7b924a68a153713a20a4eebe1d014d8fb04669945f7"),
    "authority.jsonl": (6, 4374, "84c622f56dbbd5ba379361245ecfe07bc79c9f4fd6b18ba21b82b5f545211869"),
    "concepts.jsonl": (483, 152695, "720d96a10a3c2abebab164e2181486743ef99efb50c6ef419faefbf528b8ead3"),
    "corrections.jsonl": (564, 594720, "bd961fad5d83e96fec6ef83caa8447e2e5f282c603fd4983d79b5b4b54049fbb"),
    "qa.jsonl": (178, 97769, "40a3e19ea3a4daae552d92c6c6b41486baced20cb172428c1dc255c3027e70cb"),
    "relations.jsonl": (1055, 473663, "9bef98e30bfbd17551f745a10814efabb349e58785961199791403cb9639b199"),
    "rights.jsonl": (107, 100112, "02e64d84b72eddba24f184544205de396e143d6fb96b09209e8e4c4837b234be"),
    "segments.jsonl": (2041, 3345425, "ccdaf7b3d80900a43a92423bc54446a556eaecdf5cce3bc4d40f21e6ad151cfe"),
    "terms.jsonl": (476, 315218, "4b82f9d582ba747829373a7935fcc3cae56b96fd6b7486969ebb6d54cf927c50"),
    "units.jsonl": (2071, 3522676, "5ecf2049dd4747a14d66c335a0d8579c45946a54e377129fc39cbe838c019219"),
}
PREFIX_TOTAL = (
    7273,
    8840132,
    "97edc6371a0bf670ebdaaa4fab8618ec138ae25c4bf54ca9172139934ba0b464",
)

INPUT_PATHS = (
    SOURCE_PATH, PROGRAM_PATH, TEST_PATH, EXPECTED_PATH, TERMINOLOGY_PATH,
    STATIC_PATH, MATH_PATH, LANGUAGE_PATH, EXECUTION_PATH, COMBINED_PATH,
)
LEARNER_PATHS = (SOURCE_PATH, PROGRAM_PATH, TEST_PATH, EXPECTED_PATH)
EVIDENCE_PATHS = (STATIC_PATH, MATH_PATH, LANGUAGE_PATH, EXECUTION_PATH, COMBINED_PATH)

ID_KINDS = {
    LOCAL_ROOT: ("reader_unit", "laboratory"),
    f"{LOCAL_ROOT}-status": ("section", "status"),
    f"{LOCAL_ROOT}-prerequisites": ("section", "prerequisites"),
    f"{LOCAL_ROOT}-objectives": ("section", "objectives"),
    f"{LOCAL_ROOT}-conventions": ("section", "conventions"),
    f"{LOCAL_ROOT}-data": ("section", "data"),
    **{f"{LOCAL_ROOT}-task-{number:03d}": ("exercise", "exercise") for number in range(1, 7)},
    f"{LOCAL_ROOT}-hint": ("hint", "hint"),
    f"{LOCAL_ROOT}-program": ("source_code", "source_code"),
    f"{LOCAL_ROOT}-tests": ("test_suite", "test_suite"),
    f"{LOCAL_ROOT}-expected-output": ("expected_output", "expected_output"),
    f"{LOCAL_ROOT}-interpretation": ("interpretation", "interpretation"),
    f"{LOCAL_ROOT}-solution": ("solution", "solution"),
    f"{LOCAL_ROOT}-sol-monodromy": ("section", "solution_section"),
    f"{LOCAL_ROOT}-sol-image-presentation": ("section", "solution_section"),
    f"{LOCAL_ROOT}-sol-schreier": ("section", "solution_section"),
    f"{LOCAL_ROOT}-sol-negative": ("section", "solution_section"),
    f"{LOCAL_ROOT}-reproducibility": ("verification", "verification"),
    f"{LOCAL_ROOT}-rights": ("rights_notice", "rights_notice"),
}

TERM_SPECS = (
    (485, "monodromy image", "citra monodromi", "covering_spaces", f"{LOCAL_ROOT}-interpretation", "the permutation-group image of the fibre action; distinguish it from the stabilizer subgroup and the covering-space fundamental group"),
    (486, "Schreier graph", "graf Schreier", "combinatorial_group_theory", f"{LOCAL_ROOT}-data", "labelled coset graph encoding generator transitions; capitalize the proper name"),
    (487, "Schreier transversal", "transversal Schreier", "combinatorial_group_theory", f"{LOCAL_ROOT}-sol-schreier", "a chosen representative word for each reached coset or sheet"),
    (488, "Schreier generator", "pembangkit Schreier", "combinatorial_group_theory", f"{LOCAL_ROOT}-sol-schreier", "the freely reduced word t*x*overline(tx)^-1 associated with a transversal and generator"),
    (489, "spanning tree", "pohon merentang", "graph_theory", f"{LOCAL_ROOT}-sol-schreier", "a connected cycle-free subgraph containing every vertex"),
    (490, "breadth-first search", "pencarian lebar-pertama", "algorithms", f"{LOCAL_ROOT}-sol-schreier", "deterministic graph traversal when the neighbour-letter order is frozen"),
    (491, "free basis", "basis bebas", "combinatorial_group_theory", f"{LOCAL_ROOT}-sol-schreier", "a generating set exhibiting a group as free with no nontrivial relators"),
    (492, "dihedral group", "grup dihedral", "group_theory", f"{LOCAL_ROOT}-sol-image-presentation", "state the order or polygon convention explicitly because D_n notation varies"),
)

EXISTING_CONCEPTS = {
    "concept:monodromy", "concept:permutation-representation", "concept:covering-action",
    "concept:orbit-decomposition", "concept:connected-covering-space",
    "concept:stabilizer-subgroup", "concept:fundamental-group", "concept:free-group",
    "concept:group-presentation", "concept:normal-closure", "concept:right-action",
    "concept:graph-covering", "concept:free-reduction",
}
NEW_CONCEPTS = {number: f"concept:{LOCAL_ROOT}-term-{number:04d}" for number, *_ in TERM_SPECS}
ALL_LAB_CONCEPTS = tuple(sorted(EXISTING_CONCEPTS | set(NEW_CONCEPTS.values())))

ROUTE_ANCHORS = {
    "D60-R04": "unit:o012-rbt-u007",
    "D60-R05": "unit:o012-rbt-u011",
    "D60-R06": "unit:o012-rbt-u014",
}
TASK_DEPENDENCIES = {
    1: ("unit:o012-rbt-l10-s03",),
    2: ("unit:o012-rbt-l07-s03",),
    3: ("unit:o012-rbt-l11-s01", "unit:o012-rbt-l13-s05"),
    4: ("unit:o012-rbt-l09-thm-002", "unit:o012-rbt-l11-s01"),
    5: ("unit:o012-rbt-l09-thm-002", "unit:o012-rbt-l11-s01"),
    6: ("unit:o012-rbt-l07-s03", "unit:o012-rbt-l10-s03"),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"Lab 1 backend producer FAIL: {message}")


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


def verify_inputs(sealed: dict[str, tuple[int, int, str]] | None = None) -> dict[str, Any]:
    raw = {relative: disciplined(relative) for relative in INPUT_PATHS}
    identities = {relative: identity(value) for relative, value in raw.items()}
    if sealed is not None:
        require(identities == sealed, "sealed input identity drift")

    combined = json.loads(raw[COMBINED_PATH].decode("utf-8"))
    require(combined.get("status") == "PASS" and combined.get("laboratory_id") == LAB_ID, "combined QA is not a Lab 1 PASS")
    require(combined.get("severity_census") == {"P1": 0, "P2": 0, "P3": 0}, "combined QA findings remain")
    bound: dict[str, tuple[int, int, str]] = {}
    identity_index(combined, bound)
    for relative in (*LEARNER_PATHS, TERMINOLOGY_PATH, STATIC_PATH, MATH_PATH, LANGUAGE_PATH, EXECUTION_PATH):
        require(bound.get(relative) == identities[relative], f"combined QA does not bind current {relative}")

    static = json.loads(raw[STATIC_PATH].decode("utf-8"))
    require(static.get("status") == "PASS" and static.get("structure", {}).get("stable_ids") == 24, "static QA mismatch")
    for relative, kind in ((MATH_PATH, "independent_mathematics"), (LANGUAGE_PATH, "independent_source_language")):
        receipt = json.loads(raw[relative].decode("utf-8"))
        require(receipt.get("status") == "PASS" and receipt.get("review_kind") == kind, f"{kind} review mismatch")
        require(receipt.get("independent_from_production") is True, f"{kind} review not independent")
        require(receipt.get("reader_sha256") == identities[SOURCE_PATH][2], f"{kind} review binds stale reader")
        require(receipt.get("severity_census") == {"P1": 0, "P2": 0, "P3": 0}, f"{kind} findings remain")
    execution = json.loads(raw[EXECUTION_PATH].decode("utf-8"))
    require(execution.get("status") == "PASS" and execution.get("program_runs") == execution.get("test_runs") == 2, "execution receipt mismatch")
    require(execution.get("tests_per_run") == 6 and execution.get("program_stdout_matches_expected_output") is True, "execution closure mismatch")
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
    require(observed == set(ID_KINDS) and len(observed) == 24, f"stable-ID inventory mismatch: {sorted(set(ID_KINDS)-observed)}")

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
        f"{LOCAL_ROOT}-status": ("concept:monodromy", "concept:stabilizer-subgroup", "concept:fundamental-group"),
        f"{LOCAL_ROOT}-prerequisites": ("concept:covering-action", "concept:fundamental-group", "concept:free-group", "concept:group-presentation"),
        f"{LOCAL_ROOT}-objectives": (NEW_CONCEPTS[485], NEW_CONCEPTS[487], NEW_CONCEPTS[491], "concept:connected-covering-space"),
        f"{LOCAL_ROOT}-conventions": ("concept:right-action", "concept:permutation-representation", "concept:free-group"),
        f"{LOCAL_ROOT}-data": (NEW_CONCEPTS[486], "concept:covering-action", "concept:permutation-representation"),
        f"{LOCAL_ROOT}-task-001": ("concept:covering-action", "concept:permutation-representation"),
        f"{LOCAL_ROOT}-task-002": ("concept:orbit-decomposition", "concept:connected-covering-space", NEW_CONCEPTS[485]),
        f"{LOCAL_ROOT}-task-003": ("concept:group-presentation", NEW_CONCEPTS[492], "concept:normal-closure"),
        f"{LOCAL_ROOT}-task-004": (NEW_CONCEPTS[487], NEW_CONCEPTS[488], NEW_CONCEPTS[490], "concept:free-reduction"),
        f"{LOCAL_ROOT}-task-005": (NEW_CONCEPTS[489], NEW_CONCEPTS[491], "concept:stabilizer-subgroup", "concept:fundamental-group"),
        f"{LOCAL_ROOT}-task-006": ("concept:orbit-decomposition", "concept:graph-covering"),
        f"{LOCAL_ROOT}-program": ("concept:covering-action", NEW_CONCEPTS[487], NEW_CONCEPTS[488]),
        f"{LOCAL_ROOT}-tests": ("concept:permutation-representation", "concept:orbit-decomposition", NEW_CONCEPTS[491]),
        f"{LOCAL_ROOT}-expected-output": (NEW_CONCEPTS[485], NEW_CONCEPTS[491], NEW_CONCEPTS[492]),
        f"{LOCAL_ROOT}-interpretation": (NEW_CONCEPTS[485], "concept:stabilizer-subgroup", "concept:normal-closure"),
        f"{LOCAL_ROOT}-sol-monodromy": ("concept:monodromy", "concept:orbit-decomposition", "concept:connected-covering-space"),
        f"{LOCAL_ROOT}-sol-image-presentation": ("concept:group-presentation", NEW_CONCEPTS[492]),
        f"{LOCAL_ROOT}-sol-schreier": (NEW_CONCEPTS[487], NEW_CONCEPTS[488], NEW_CONCEPTS[489], NEW_CONCEPTS[491]),
        f"{LOCAL_ROOT}-sol-negative": ("concept:orbit-decomposition", "concept:graph-covering"),
        f"{LOCAL_ROOT}-reproducibility": ("concept:permutation-representation", NEW_CONCEPTS[490]),
        f"{LOCAL_ROOT}-rights": ("concept:monodromy", "concept:fundamental-group"),
    }
    if local_id in (LOCAL_ROOT, f"{LOCAL_ROOT}-hint", f"{LOCAL_ROOT}-solution"):
        return list(ALL_LAB_CONCEPTS)
    return list(exact.get(local_id, ("concept:monodromy",)))


def unit_record(local_id: str, order: int, parsed: dict[str, Any]) -> dict[str, Any]:
    kind, _ = ID_KINDS[local_id]
    ident = f"unit:{local_id}"
    record = {
        **common("unit", ident),
        "authority_context_ids": [COURSE, PROGRAM, ROBERTS_EDITION, ROBERTS_RESOURCE],
        "authority_context_only": True,
        "concept_ids": concepts_for(local_id),
        "course_id": COURSE,
        "course_route_unit_ids": list(ROUTES),
        "display_title": parsed["items"][local_id]["title"],
        "edition_context_only": True,
        "edition_id": ROBERTS_EDITION,
        "edition_unit_id": EDITION_UNIT_ID,
        "laboratory_id": LAB_ID,
        "locale": "id-ID",
        "model_provenance": MODEL,
        "order": 42 if local_id == LOCAL_ROOT else order,
        "original_layer": True,
        "parent_id": COURSE if local_id == LOCAL_ROOT else ROOT_UNIT,
        "path": [ROOT_UNIT] if local_id == LOCAL_ROOT else [ROOT_UNIT, ident],
        "program_id": PROGRAM,
        "provenance_relation": "edition_original",
        "resource_context_only": True,
        "resource_id": ROBERTS_RESOURCE,
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
            "primary_course_route_unit_id": "D60-R04",
            "reader_scope": "six_tasks_one_hint_full_solution_program_tests_expected_output_interpretation",
            "secondary_course_route_unit_ids": ["D60-R05", "D60-R06"],
        })
    task = re.fullmatch(re.escape(LOCAL_ROOT) + r"-task-(\d{3})", local_id)
    if task:
        record["laboratory_task_number"] = int(task.group(1))
        record["primary_course_route_unit_id"] = "D60-R04"
        record["secondary_course_route_unit_ids"] = ["D60-R05", "D60-R06"]
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
        "edition_id": ROBERTS_EDITION,
        "locale": "id-ID",
        "order": unit["order"],
        "provenance_relation": "edition_original",
        "resource_id": ROBERTS_RESOURCE,
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
        "third_party_status": "No excluded Fomberg problem-bank expression is used; admitted authority IDs are mathematical context only.",
    }]

    qa_ids = {kind: f"qa:{LOCAL_ROOT}-{kind}" for kind in ("structure", "execution", "math", "language", "mastery", "terminology")}
    artifacts = [
        artifact(f"artifact:{LOCAL_ROOT}-reader-source", SOURCE_PATH, "text/markdown", list(qa_ids.values()), "structurally_verified", data["identities"]),
        artifact(f"artifact:{LOCAL_ROOT}-python-source", PROGRAM_PATH, "text/x-python", [qa_ids["execution"], qa_ids["mastery"]], "built", data["identities"]),
        artifact(f"artifact:{LOCAL_ROOT}-tests", TEST_PATH, "text/x-python", [qa_ids["execution"]], "built", data["identities"]),
        artifact(f"artifact:{LOCAL_ROOT}-expected-output", EXPECTED_PATH, "text/plain", [qa_ids["execution"]], "built", data["identities"]),
        artifact(f"artifact:{LOCAL_ROOT}-static-qa", STATIC_PATH, "application/json", [qa_ids["structure"], qa_ids["mastery"], qa_ids["terminology"]], "built", data["identities"]),
        artifact(f"artifact:{LOCAL_ROOT}-math-review", MATH_PATH, "application/json", [qa_ids["math"]], "mathematically_reviewed", data["identities"]),
        artifact(f"artifact:{LOCAL_ROOT}-language-review", LANGUAGE_PATH, "application/json", [qa_ids["language"], qa_ids["terminology"]], "language_reviewed", data["identities"]),
        artifact(f"artifact:{LOCAL_ROOT}-execution-receipt", EXECUTION_PATH, "application/json", [qa_ids["execution"]], "built", data["identities"]),
        artifact(f"artifact:{LOCAL_ROOT}-qa-receipt", COMBINED_PATH, "application/json", list(qa_ids.values()), "built", data["identities"]),
    ]
    qa_events = [
        {**common("qa_event", qa_ids["structure"]), "laboratory_id": LAB_ID, "note": "Twenty-four stable IDs, six tasks, one hint, a full solution, explicit route metadata, LF/UTF-8, rights, provenance, and privacy checks passed.", "qa_type": "structure", "result": "passed", "unit_id": ROOT_UNIT, "witness_artifact_ids": [f"artifact:{LOCAL_ROOT}-reader-source", f"artifact:{LOCAL_ROOT}-static-qa", f"artifact:{LOCAL_ROOT}-qa-receipt"]},
        {**common("qa_event", qa_ids["execution"]), "laboratory_id": LAB_ID, "note": "The standard-library program and six-test suite each ran twice; program stdout was deterministic and byte-identical to the expected output.", "qa_type": "execution", "result": "passed", "unit_id": ROOT_UNIT, "witness_artifact_ids": [f"artifact:{LOCAL_ROOT}-python-source", f"artifact:{LOCAL_ROOT}-tests", f"artifact:{LOCAL_ROOT}-expected-output", f"artifact:{LOCAL_ROOT}-execution-receipt"]},
        {**common("qa_event", qa_ids["math"]), "laboratory_id": LAB_ID, "note": "Independent mathematics review recomputed the image, relations, transversal, Schreier basis, graph rank, and negative fixture with P1=P2=P3=0.", "qa_type": "math", "result": "passed", "unit_id": ROOT_UNIT, "witness_artifact_ids": [f"artifact:{LOCAL_ROOT}-math-review", f"artifact:{LOCAL_ROOT}-qa-receipt"]},
        {**common("qa_event", qa_ids["language"]), "laboratory_id": LAB_ID, "note": "Independent final id-ID source-language review passed after reader-visible program output and all remaining terminology were localized.", "qa_type": "language", "result": "passed", "unit_id": ROOT_UNIT, "witness_artifact_ids": [f"artifact:{LOCAL_ROOT}-language-review", f"artifact:{LOCAL_ROOT}-qa-receipt"]},
        {**common("qa_event", qa_ids["mastery"]), "laboratory_id": LAB_ID, "note": "Six tasks share a stable hint and one complete checked solution, with source, tests, expected output, and interpretation.", "qa_type": "mastery", "result": "passed", "unit_id": ROOT_UNIT, "witness_artifact_ids": [f"artifact:{LOCAL_ROOT}-reader-source", f"artifact:{LOCAL_ROOT}-python-source", f"artifact:{LOCAL_ROOT}-static-qa"]},
        {**common("qa_event", qa_ids["terminology"]), "laboratory_id": LAB_ID, "note": "O012-TERM-0485 through O012-TERM-0492 are mapped to eight locale-neutral concepts and exact learner evidence segments.", "qa_type": "terminology", "result": "passed", "unit_id": ROOT_UNIT, "witness_artifact_ids": [f"artifact:{LOCAL_ROOT}-language-review", f"artifact:{LOCAL_ROOT}-static-qa"]},
    ]

    relations = [
        relation(f"relation:contains:o012-d60:lab01", "contains", COURSE, ROOT_UNIT, f"The O012/D60 course contains {LAB_ID} as an original computation laboratory.", laboratory_id=LAB_ID, course_route_unit_ids=list(ROUTES)),
        relation(f"relation:contains:{LOCAL_ROOT}-rights:root", "contains", LAB_RIGHTS, ROOT_UNIT, f"The original CC BY-SA 4.0 component rights bind the complete {LAB_ID} graph.", laboratory_id=LAB_ID, rights_mapping_role="direct_component_binding"),
        relation(f"relation:contains:o012-d60-integrated-rights:lab01-original", "contains", INTEGRATED_RIGHTS, LAB_RIGHTS, f"The integrated route contains the independently licensed {LAB_ID} component without altering source licenses.", laboratory_id=LAB_ID, rights_mapping_role="integrated_route_component"),
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
            relations.append(relation(f"relation:depends-on:{LOCAL_ROOT}-task-{number:03d}:{dep_order:02d}:{slug}", "depends-on", exercise, anchor, f"{LAB_ID} task {number} requires the admitted result or unit {anchor}.", laboratory_id=LAB_ID, laboratory_task_number=number, dependency_order=dep_order, dependency_role="laboratory_prerequisite"))
    for role, route_id in (("primary", "D60-R04"), ("secondary", "D60-R05"), ("secondary", "D60-R06")):
        relations.append(relation(f"relation:xref:{LOCAL_ROOT}:{route_id.lower()}", "xref", ROOT_UNIT, ROUTE_ANCHORS[route_id], f"{role.title()} route mapping for {LAB_ID}: {route_id}.", laboratory_id=LAB_ID, course_route_unit_id=route_id, route_mapping_role=role, route_source_anchor_id=ROUTE_ANCHORS[route_id]))

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
    spec = importlib.util.spec_from_file_location("o012_generic_backend_for_lab01", path)
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
        raise SystemExit(f"Lab 1 backend producer FAIL: merged schema/reference validation failed: {exc}")

    required_context = {
        COURSE, PROGRAM, ROBERTS_EDITION, ROBERTS_RESOURCE, FOMBERG_EDITION,
        FOMBERG_RESOURCE, INTEGRATED_RIGHTS, *EXISTING_CONCEPTS,
        *ROUTE_ANCHORS.values(),
        *(anchor for anchors in TASK_DEPENDENCIES.values() for anchor in anchors),
    }
    require(required_context <= by_id.keys(), f"required context IDs absent: {sorted(required_context - by_id.keys())}")
    expected_counts = {
        "artifacts.jsonl": 9,
        "assets.jsonl": 0,
        "authority.jsonl": 0,
        "concepts.jsonl": 8,
        "corrections.jsonl": 0,
        "qa.jsonl": 6,
        "relations.jsonl": 51,
        "rights.jsonl": 1,
        "segments.jsonl": 24,
        "terms.jsonl": 8,
        "units.jsonl": 24,
    }
    actual_counts = {name: len(additions[name]) for name in FILES}
    require(actual_counts == expected_counts, f"suffix record census mismatch: {actual_counts}")

    units = additions["units.jsonl"]
    segments = additions["segments.jsonl"]
    require({record["source_local_id"] for record in units} == set(ID_KINDS), "unit stable-ID mapping mismatch")
    require({record["source_local_id"] for record in segments} == set(ID_KINDS), "segment stable-ID mapping mismatch")
    segments_by_local = {record["source_local_id"]: record for record in segments}
    for unit in units:
        segment = segments_by_local[unit["source_local_id"]]
        require(segment["unit_id"] == unit["id"] and segment["target_locator"] == unit["target_locator"], f"unit/segment mismatch: {unit['id']}")
        start = unit["target_locator"]["line_start"]
        require(unit["source_local_id"].encode("utf-8") in parsed["lines"][start - 1], f"target locator does not start at stable ID: {unit['id']}")
        require(unit["rights_component_id"] == segment["rights_component_id"] == LAB_RIGHTS, f"rights mismatch: {unit['id']}")
        require(unit["original_layer"] is True and unit["source_corpus_used"] is False, f"original/source demarcation mismatch: {unit['id']}")
        require(all(concept in by_id and by_id[concept]["entity_type"] == "concept" for concept in unit["concept_ids"]), f"unresolved concept mapping: {unit['id']}")

    rights = additions["rights.jsonl"][0]
    require(rights["license_expression"] == "CC-BY-SA-4.0" and set(rights["component_scope"]) == {unit["id"] for unit in units}, "rights component scope mismatch")
    tasks = {f"unit:{LOCAL_ROOT}-task-{number:03d}" for number in range(1, 7)}
    hint_edges = [record for record in additions["relations.jsonl"] if record["relation_type"] == "hints"]
    solve_edges = [record for record in additions["relations.jsonl"] if record["relation_type"] == "solves"]
    require({record["to_id"] for record in hint_edges} == tasks and len(hint_edges) == 6, "hint closure mismatch")
    require({record["to_id"] for record in solve_edges} == tasks and len(solve_edges) == 6, "solution closure mismatch")
    require(all(record.get("solution_status") == "complete_checked_solution" for record in solve_edges), "solution status mismatch")
    route_edges = [record for record in additions["relations.jsonl"] if record["relation_type"] == "xref"]
    require({(record["course_route_unit_id"], record["to_id"]) for record in route_edges} == set(ROUTE_ANCHORS.items()), "route xref mismatch")
    dependency_edges = [record for record in additions["relations.jsonl"] if record["relation_type"] == "depends-on"]
    require(len(dependency_edges) == sum(len(value) for value in TASK_DEPENDENCIES.values()), "dependency census mismatch")

    term_controls = {record["terminology_control_id"] for record in additions["terms.jsonl"]}
    require(term_controls == {f"O012-TERM-{number:04d}" for number, *_ in TERM_SPECS}, "term-control mapping mismatch")
    require(all(record["evidence_segment_id"] in by_id for record in additions["terms.jsonl"]), "term evidence segment missing")
    require(Counter(record["qa_type"] for record in additions["qa.jsonl"]) == Counter({"structure": 1, "execution": 1, "math": 1, "language": 1, "mastery": 1, "terminology": 1}), "QA event census mismatch")
    for record in additions["artifacts.jsonl"]:
        expected = data["identities"][record["path"]]
        require((record["bytes"], record["sha256"]) == (expected[0], expected[2]), f"artifact identity mismatch: {record['path']}")

    joined = b"".join(suffixes(additions)[name] for name in FILES).lower()
    markers = (b"c:" + b"\\users\\", b"github_" + b"pat_", b"gh" + b"p_", b"access_" + b"token", b"authorization" + b": bearer")
    require(not any(marker in joined for marker in markers), "private path or credential marker in suffix")
    return {
        "added_records": len(added),
        "merged_records": len(records),
        "stable_ids": 24,
        "tasks": 6,
        "hints": 1,
        "complete_solutions": 1,
        "program_sources": 1,
        "test_suites": 1,
        "expected_outputs": 1,
        "new_concepts": 8,
        "new_terms": 8,
        "dependency_edges": len(dependency_edges),
        "route_edges": len(route_edges),
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

    baseline_raw = disciplined(BASELINE_RECEIPT_PATH)
    require(identity(baseline_raw) == BASELINE_RECEIPT_IDENTITY, "baseline cumulative receipt identity drift")
    baseline = json.loads(baseline_raw)
    require(
        baseline.get("status") == "PASS"
        and baseline.get("receipt_kind") == "cumulative_backend_boundary"
        and baseline.get("cumulative", {}).get("records") == PREFIX_TOTAL[0]
        and baseline.get("cumulative", {}).get("bytes") == PREFIX_TOTAL[1]
        and baseline.get("cumulative", {}).get("bundle_sha256") == PREFIX_TOTAL[2]
        and baseline.get("replay", {}).get("status") == "PASS"
        and baseline.get("replay", {}).get("exact_file_matches") == len(FILES)
        and baseline.get("replay", {}).get("temporary_replay_removed") is True,
        "baseline receipt does not prove the immutable prefix",
    )
    refreshed = verify_inputs(data["identities"])
    refreshed_parsed = parse_reader(refreshed["raw"][SOURCE_PATH])
    refreshed_additions = build_additions(refreshed, refreshed_parsed)
    require(record_plan(refreshed_additions, refreshed, semantic) == plan, "sealed inputs changed deterministic plan")
    require(suffixes(refreshed_additions) == suffixes(additions), "sealed inputs changed derived suffix")
    raw_suffixes = append_suffix(prefix, additions)
    final_raw = {name: (BACKEND / name).read_bytes() for name in FILES}
    final = bundle(final_raw)
    require(final[0] == PREFIX_TOTAL[0] + semantic["added_records"], "cumulative record-count mismatch")
    print("Lab 1 append-only semantic backend extension: PASS")
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
