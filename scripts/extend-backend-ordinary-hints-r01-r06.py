#!/usr/bin/env python3
"""Fail-closed append-only admission for the original D60 R01--R06 hint layer.

The published CA01 backend is an immutable 6,854-record prefix.  This tool
derives a 158-record suffix from the sealed 36-hint source and its independent
reviews, validates the complete graph in memory, and has only binary-append
write semantics.  It never creates or changes prompts, solutions, or solves
relations.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


LANE = Path(__file__).resolve().parents[1]
BACKEND = LANE / "backend"
SOURCE_PATH = "source/id-ID/mastery/ordinary-hints-r01-r06.md"
MATH_PATH = "qa/ordinary-hints-r01-r06/INDEPENDENT_MATH_REVIEW.json"
LANGUAGE_PATH = "qa/ordinary-hints-r01-r06/INDEPENDENT_SOURCE_LANGUAGE_REVIEW.json"
QA_PATH = "qa/ORDINARY_HINTS_R01_R06_QA.json"
SOURCE_SHA256 = "dc319cb191d709a5807f0c0792401f9faf2993ceede364764547f20bb4f69c2a"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"
SCHEMA = "curriculum.interop"
SCHEMA_VERSION = "0.1.0"
WORKFLOW = "o012-d60-id-reader-production"
TIMESTAMP = "2026-08-26T00:00:00Z"
ROOT = "unit:o012-d60-hints-r01-r06"
RIGHTS = "rights:o012-d60-hints-r01-r06-original-cc-by-sa-4.0"
COURSE = "course:o012-d60"
PROGRAM = "program:o012-id"
EDITION_CONTEXT = "edition:roberts-at-2019-b947ad2"
RESOURCE_CONTEXT = "resource:roberts-algebraic-topology-2019"
INTEGRATED_RIGHTS = "rights:o012-d60-integrated-route-cc-by-sa-4.0"
EDITION_UNIT_ID = "O012-ORIG-HINTS-R01-R06"

FILES = (
    "artifacts.jsonl", "assets.jsonl", "authority.jsonl", "concepts.jsonl",
    "corrections.jsonl", "qa.jsonl", "relations.jsonl", "rights.jsonl",
    "segments.jsonl", "terms.jsonl", "units.jsonl",
)
PREFIX = {
    "artifacts.jsonl": (193, 157480, "c50a3140513a5d243a6ce9f7256a29e97e3fab776764be476c9bfe9949a83b93"),
    "assets.jsonl": (87, 64692, "1df40f8f6ca4f2fbfbe8a7b924a68a153713a20a4eebe1d014d8fb04669945f7"),
    "authority.jsonl": (6, 4374, "84c622f56dbbd5ba379361245ecfe07bc79c9f4fd6b18ba21b82b5f545211869"),
    "concepts.jsonl": (483, 152695, "720d96a10a3c2abebab164e2181486743ef99efb50c6ef419faefbf528b8ead3"),
    "corrections.jsonl": (564, 594720, "bd961fad5d83e96fec6ef83caa8447e2e5f282c603fd4983d79b5b4b54049fbb"),
    "qa.jsonl": (166, 91181, "25d3dae94c3c117e6aeb8a020fb5076199d25e71e2184ad5bf7c59ab3db722d4"),
    "relations.jsonl": (837, 355526, "64aeedd8836ccae7a9fa9418a4a8b83f93c026432bc8c00dd0ba53a8d0e65ba9"),
    "rights.jsonl": (104, 94600, "2a034be29f7d544de52f4a0a1970bd4923531d4ac13180eaa45b432dc999b404"),
    "segments.jsonl": (1954, 3177411, "d17646479e4a8d91b618de5c4995c083dec5c208ef755d203a876645f7ab9d54"),
    "terms.jsonl": (476, 315218, "4b82f9d582ba747829373a7935fcc3cae56b96fd6b7486969ebb6d54cf927c50"),
    "units.jsonl": (1984, 3337902, "26cf11a2ba912bd8e22983204641ff22ffb0152128f20ca166195cb2abd41f3f"),
}
PREFIX_TOTAL = (6854, 8345799, "51e75d06e620762e629e9e7408da4b0c32b3e337817d9d140fbbdfa438de2f57")
INPUT_PATHS = (SOURCE_PATH, MATH_PATH, LANGUAGE_PATH, QA_PATH)
INPUT_IDENTITIES = {
    SOURCE_PATH: (28698, 410, SOURCE_SHA256),
    MATH_PATH: (19289, 447, "8ed5b3563976b415e1aa471f7cdeb3405888cbc70aec101bc02e4fab9e45de5a"),
    LANGUAGE_PATH: (18324, 221, "6c29009da4ee0380c878c3705dcd2a99cbe7a8495cc4b7f5ce456bb40f910968"),
    QA_PATH: (16616, 398, "a0460dbed83242863fc1aab8290b76fac9cd39644276e132401e7d3e9198c33d"),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"ordinary-hint backend producer FAIL: {message}")


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canon(record: dict[str, Any]) -> bytes:
    return (json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def common(entity_type: str, ident: str) -> dict[str, Any]:
    return {
        "entity_type": entity_type, "id": ident, "schema": SCHEMA,
        "schema_version": SCHEMA_VERSION, "status": "active", "supersedes": None,
        "timestamp": TIMESTAMP, "workflow": WORKFLOW,
    }


def load_module(relative: str, module_name: str):
    path = LANE / relative
    spec = importlib.util.spec_from_file_location(module_name, path)
    require(spec is not None and spec.loader is not None, f"cannot load {relative}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def input_identity(relative: str) -> tuple[int, int, str]:
    path = LANE / relative
    require(path.is_file(), f"required input missing: {relative}")
    raw = path.read_bytes()
    require(raw and b"\r" not in raw and raw.endswith(b"\n"), f"input is not UTF-8/LF disciplined: {relative}")
    try:
        raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise SystemExit(f"ordinary-hint backend producer FAIL: invalid UTF-8 in {relative}: {exc}")
    return len(raw), raw.count(b"\n"), digest(raw)


def verify_inputs() -> dict[str, Any]:
    q = load_module("scripts/qa-ordinary-hints-r01-r06.py", "o012_hint_source_qa_for_backend")
    identities = {relative: input_identity(relative) for relative in INPUT_PATHS}
    require(identities == INPUT_IDENTITIES, f"sealed hint input identity drift: {identities!r}")
    source_raw = (LANE / SOURCE_PATH).read_bytes()
    source_text = source_raw.decode("utf-8")
    blocks = q.parse_blocks(source_text)
    require(len(blocks) == 36, "source does not expose exactly 36 parsed hint blocks")

    math = json.loads((LANE / MATH_PATH).read_text(encoding="utf-8"))
    language = json.loads((LANE / LANGUAGE_PATH).read_text(encoding="utf-8"))
    q.review_binding(math, LANE / MATH_PATH, "independent_mathematics_and_binding")
    q.review_binding(language, LANE / LANGUAGE_PATH, "independent_source_language_and_binding")
    qa = json.loads((LANE / QA_PATH).read_text(encoding="utf-8"))
    require(qa.get("status") == "PASS" and qa.get("edition_unit_id") == EDITION_UNIT_ID, "source QA is not the passing hint-layer receipt")
    require(qa.get("source", {}).get("sha256") == SOURCE_SHA256 and qa.get("source", {}).get("hint_blocks") == 36, "source QA binds stale source")
    require(qa.get("binding_census", {}).get("distinct_target_exercises") == 36, "source QA target census mismatch")
    require(qa.get("binding_census", {}).get("distinct_existing_solutions") == 36, "source QA solution census mismatch")
    for label, relative in (("mathematics", MATH_PATH), ("source_language", LANGUAGE_PATH)):
        found = qa.get("independent_reviews", {}).get(label, {})
        expected = identities[relative]
        require((found.get("bytes"), found.get("lf_lines"), found.get("sha256")) == expected, f"source QA review binding mismatch: {label}")

    binding_by_stable = {item["stable_id"]: item for item in qa.get("bindings", [])}
    require(len(binding_by_stable) == 36, "source QA does not contain 36 unique binding receipts")
    parsed: list[dict[str, Any]] = []
    for block in blocks:
        stable_id = block["stable_id"]
        attrs = block["attributes"]
        match = re.fullmatch(r"o012-d60-r(\d{2})-hint-(\d{3})", stable_id)
        require(match is not None, f"malformed hint stable ID: {stable_id}")
        route = f"D60-R{int(match.group(1)):02d}"
        number = int(match.group(2))
        target = attrs.get("data-target-exercise-id")
        solution = attrs.get("data-existing-solution-id")
        component = attrs.get("data-component-id")
        source_path = attrs.get("data-source-path")
        require((target, solution) == q.EXPECTED_BINDINGS[route][number - 1], f"source deterministic binding drift: {stable_id}")
        receipt = binding_by_stable.get(stable_id, {})
        require((receipt.get("target_exercise_id"), receipt.get("existing_solution_id"), receipt.get("component_id"), receipt.get("source_path")) == (target, solution, component, source_path), f"QA/source binding disagreement: {stable_id}")
        parsed.append({
            "stable_id": stable_id, "route": route, "number": number,
            "target_id": target, "solution_id": solution,
            "component_id": component, "source_path": source_path,
        })
    require(len({item["target_id"] for item in parsed}) == len({item["solution_id"] for item in parsed}) == 36, "source target/solution bindings are not one-to-one")
    return {"identities": identities, "source_raw": source_raw, "source_text": source_text, "blocks": blocks, "bindings": parsed, "qa": qa}


def parse_prefix_records(raw_by_file: dict[str, bytes]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for name in FILES:
        raw = raw_by_file[name]
        require(b"\r" not in raw and raw.endswith(b"\n"), f"prefix JSONL discipline mismatch: {name}")
        for number, line in enumerate(raw.splitlines(keepends=True), 1):
            try:
                record = json.loads(line.decode("utf-8", errors="strict"))
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                raise SystemExit(f"ordinary-hint backend producer FAIL: {name}:{number}: {exc}")
            require(canon(record) == line, f"noncanonical prefix record: {name}:{number}")
            records.append(record)
    return records


def verify_prefix(backend: Path = BACKEND) -> tuple[dict[str, bytes], list[dict[str, Any]]]:
    raw_by_file: dict[str, bytes] = {}
    bundle = hashlib.sha256(); total_records = total_bytes = 0
    for name in FILES:
        path = backend / name
        require(path.is_file(), f"backend file missing: {name}")
        raw = path.read_bytes()
        observed = (len(raw.splitlines()), len(raw), digest(raw))
        require(observed == PREFIX[name], f"immutable CA01 prefix mismatch: {name}: {observed!r}")
        raw_by_file[name] = raw
        bundle.update(name.encode("utf-8")); bundle.update(b"\0"); bundle.update(raw)
        total_records += observed[0]; total_bytes += observed[1]
    require((total_records, total_bytes, bundle.hexdigest()) == PREFIX_TOTAL, "immutable CA01 prefix bundle mismatch")
    return raw_by_file, parse_prefix_records(raw_by_file)


def locator(lines: list[bytes], start: int, end: int) -> dict[str, Any]:
    return {"content_sha256": digest(b"".join(lines[start - 1:end])), "file_sha256": SOURCE_SHA256, "line_end": end, "line_start": start, "path": SOURCE_PATH}


def spans(source_raw: bytes) -> dict[str, tuple[int, int]]:
    lines = source_raw.splitlines(keepends=True)
    decoded = [line.decode("utf-8") for line in lines]
    out: dict[str, tuple[int, int]] = {"o012-d60-hints-r01-r06": (18, len(lines))}
    for route in range(1, 7):
        for number in range(1, 7):
            stable_id = f"o012-d60-r{route:02d}-hint-{number:03d}"
            starts = [index for index, line in enumerate(decoded, 1) if f"#{stable_id}" in line and line.startswith("::: {")]
            require(len(starts) == 1, f"cannot locate one hint opening: {stable_id}")
            start = starts[0]
            ends = [index for index in range(start + 1, len(lines) + 1) if decoded[index - 1].strip() == ":::" ]
            require(ends, f"cannot locate hint close: {stable_id}")
            out[stable_id] = (start, ends[0])
    require(len(out) == 37, "root/hint span census mismatch")
    return out


def backend_hint_id(binding: dict[str, Any]) -> str:
    return f"unit:{binding['component_id']}-route-hint-r{int(binding['route'][-2:]):02d}-{binding['number']:03d}"


def source_locator() -> dict[str, Any]:
    return {"kind": "edition_original", "path": SOURCE_PATH, "precision": "exact_target_span", "source_corpus_used": False}


def root_unit(span: tuple[int, int], concepts: list[str]) -> dict[str, Any]:
    lines = (LANE / SOURCE_PATH).read_bytes().splitlines(keepends=True)
    return {
        **common("unit", ROOT), "authority_context_ids": [COURSE, PROGRAM, EDITION_CONTEXT, RESOURCE_CONTEXT],
        "authority_context_only": True, "concept_ids": concepts, "course_id": COURSE,
        "course_route_unit_ids": [f"D60-R{route:02d}" for route in range(1, 7)],
        "display_title": "Petunjuk Penguasaan Rute 1–6", "edition_context_only": True,
        "edition_id": EDITION_CONTEXT, "edition_unit_id": EDITION_UNIT_ID, "locale": "id-ID",
        "model_provenance": MODEL, "order": 39, "original_layer": True, "parent_id": COURSE,
        "path": [ROOT], "program_id": PROGRAM, "provenance_relation": "edition_original",
        "reader_scope": "thirty_six_hints_for_existing_exercise_complete_solution_pairs",
        "resource_context_only": True, "resource_id": RESOURCE_CONTEXT, "rights_component_id": RIGHTS,
        "source_corpus_used": False, "source_local_id": "o012-d60-hints-r01-r06",
        "source_locator": source_locator(), "target_locator": locator(lines, *span),
        "translation_state": "structurally_verified", "unit_kind": "reader_unit",
    }


def hint_unit(binding: dict[str, Any], span: tuple[int, int], target: dict[str, Any], order: int) -> dict[str, Any]:
    ident = backend_hint_id(binding)
    lines = (LANE / SOURCE_PATH).read_bytes().splitlines(keepends=True)
    return {
        **common("unit", ident), "authority_context_ids": [COURSE, PROGRAM, EDITION_CONTEXT, RESOURCE_CONTEXT],
        "authority_context_only": True, "component_id": binding["component_id"],
        "concept_ids": target.get("concept_ids", []), "course_id": COURSE,
        "course_route_unit_id": binding["route"], "course_route_unit_ids": [binding["route"]],
        "display_title": f"Petunjuk penguasaan {binding['route']}.{binding['number']}: {target.get('display_title', binding['target_id'])}",
        "edition_context_only": True, "edition_id": EDITION_CONTEXT, "edition_unit_id": EDITION_UNIT_ID,
        "existing_solution_id": binding["solution_id"], "locale": "id-ID", "model_provenance": MODEL,
        "order": order, "original_layer": True, "parent_id": ROOT, "path": [ROOT, ident],
        "primary_course_route_unit_id": binding["route"], "program_id": PROGRAM,
        "provenance_relation": "edition_original", "resource_context_only": True,
        "resource_id": RESOURCE_CONTEXT, "rights_component_id": RIGHTS,
        "route_mapping_status": "explicit_primary", "secondary_course_route_unit_ids": [],
        "source_corpus_used": False, "source_local_id": binding["stable_id"],
        "source_locator": source_locator(), "target_exercise_id": binding["target_id"],
        "target_locator": locator(lines, *span), "translation_state": "structurally_verified", "unit_kind": "hint",
    }


def segment_from_unit(unit: dict[str, Any]) -> dict[str, Any]:
    optional_keys = (
        "authority_context_ids", "authority_context_only", "component_id", "course_route_unit_id",
        "course_route_unit_ids", "edition_context_only", "edition_unit_id", "existing_solution_id",
        "model_provenance", "original_layer", "primary_course_route_unit_id", "resource_context_only",
        "route_mapping_status", "secondary_course_route_unit_ids", "source_corpus_used", "target_exercise_id",
    )
    optional = {key: unit[key] for key in optional_keys if key in unit}
    return {
        **common("segment", unit["id"].replace("unit:", "segment:", 1)), **optional,
        "concept_ids": unit["concept_ids"], "edition_id": unit["edition_id"], "locale": "id-ID",
        "order": unit["order"], "provenance_relation": "edition_original",
        "resource_id": unit["resource_id"], "rights_component_id": RIGHTS,
        "segment_kind": "mastery_support" if unit["unit_kind"] == "reader_unit" else "hint",
        "source_local_id": unit["source_local_id"], "source_locator": unit["source_locator"],
        "target_locator": unit["target_locator"], "translation_state": "structurally_verified", "unit_id": unit["id"],
    }


def relation(ident: str, relation_type: str, from_id: str, to_id: str, note: str, **extra: Any) -> dict[str, Any]:
    return {**common("relation", ident), "from_id": from_id, "note": note, "relation_type": relation_type, "to_id": to_id, **extra}


def artifact(ident: str, relative: str, media_type: str, qa_ids: list[str], state: str, identities: dict[str, tuple[int, int, str]]) -> dict[str, Any]:
    byte_count, _, sha = identities[relative]
    return {
        **common("artifact", ident), "bytes": byte_count, "edition_unit_id": EDITION_UNIT_ID,
        "locale": "id-ID", "manifest_artifact_id": None, "media_type": media_type,
        "path": relative, "qa_event_ids": qa_ids, "rights_component_id": RIGHTS,
        "sha256": sha, "toolchain": f"Original R01--R06 hint evidence; {MODEL}; source {SOURCE_SHA256}; append-only semantic admission.",
        "translation_state": state, "unit_id": ROOT,
    }


def build_additions(data: dict[str, Any], prefix_records: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    by_id = {record["id"]: record for record in prefix_records}
    found_spans = spans(data["source_raw"])
    concepts = sorted({concept for binding in data["bindings"] for concept in by_id[binding["target_id"]].get("concept_ids", [])})
    units = [root_unit(found_spans["o012-d60-hints-r01-r06"], concepts)]
    for order, binding in enumerate(data["bindings"], 1):
        units.append(hint_unit(binding, found_spans[binding["stable_id"]], by_id[binding["target_id"]], order))
    segments = [segment_from_unit(unit) for unit in units]
    rights = [{
        **common("rights", RIGHTS),
        "attribution": "Original Indonesian mastery hints prepared for the independent O012/D60 edition.",
        "change_notice": "Edition-original hint layer; existing Roberts-derived prompts and edition-original solutions are referenced by stable ID but neither copied nor relicensed.",
        "component_scope": [unit["id"] for unit in units], "license_expression": "CC-BY-SA-4.0",
        "license_url": "https://creativecommons.org/licenses/by-sa/4.0/",
        "non_endorsement": "Independent Indonesian edition; no Roberts, Fomberg, Lazarovich, or source-author endorsement.",
        "third_party_status": "No prompt or complete solution is copied or modified in this layer; all 36 hints are edition-original and reference immutable existing records.",
    }]
    qa_ids = {
        "structure": "qa:o012-d60-hints-r01-r06-structure", "math": "qa:o012-d60-hints-r01-r06-math",
        "language": "qa:o012-d60-hints-r01-r06-language", "mastery": "qa:o012-d60-hints-r01-r06-mastery",
    }
    artifacts = [
        artifact("artifact:o012-d60-hints-r01-r06-source", SOURCE_PATH, "text/markdown", list(qa_ids.values()), "structurally_verified", data["identities"]),
        artifact("artifact:o012-d60-hints-r01-r06-math-review", MATH_PATH, "application/json", [qa_ids["math"]], "mathematically_reviewed", data["identities"]),
        artifact("artifact:o012-d60-hints-r01-r06-language-review", LANGUAGE_PATH, "application/json", [qa_ids["language"]], "language_reviewed", data["identities"]),
        artifact("artifact:o012-d60-hints-r01-r06-qa-receipt", QA_PATH, "application/json", list(qa_ids.values()), "built", data["identities"]),
    ]
    qa_events = [
        {**common("qa_event", qa_ids["structure"]), "note": "Sealed identity, 36 stable hint blocks, exact exercise/solution/source bindings, LF/UTF-8, rights, provenance, and privacy passed.", "qa_type": "structure", "result": "passed", "unit_id": ROOT, "witness_artifact_ids": ["artifact:o012-d60-hints-r01-r06-source", "artifact:o012-d60-hints-r01-r06-qa-receipt"]},
        {**common("qa_event", qa_ids["math"]), "note": "Independent mathematics-and-binding review passed all 36 hints with P1=P2=P3=0.", "qa_type": "math", "result": "passed", "unit_id": ROOT, "witness_artifact_ids": ["artifact:o012-d60-hints-r01-r06-math-review", "artifact:o012-d60-hints-r01-r06-qa-receipt"]},
        {**common("qa_event", qa_ids["language"]), "note": "Independent id-ID source-language-and-binding review passed all 36 hints with P1=P2=P3=0.", "qa_type": "language", "result": "passed", "unit_id": ROOT, "witness_artifact_ids": ["artifact:o012-d60-hints-r01-r06-language-review", "artifact:o012-d60-hints-r01-r06-qa-receipt"]},
        {**common("qa_event", qa_ids["mastery"]), "note": "Six exact hints per D60-R01 through D60-R06 close 36 pre-existing exercise/full-solution pairs without prompt, solution, or solves mutation.", "qa_type": "mastery", "result": "passed", "unit_id": ROOT, "witness_artifact_ids": ["artifact:o012-d60-hints-r01-r06-source", "artifact:o012-d60-hints-r01-r06-qa-receipt"]},
    ]
    relations = [
        relation("relation:contains:o012-d60:hints-r01-r06", "contains", COURSE, ROOT, "The O012/D60 course contains the original R01--R06 hint layer.", course_route_unit_ids=[f"D60-R{route:02d}" for route in range(1, 7)]),
        relation("relation:contains:o012-d60-hints-r01-r06-rights:root", "contains", RIGHTS, ROOT, "The original CC BY-SA 4.0 component rights bind the complete hint layer.", rights_mapping_role="direct_component_binding"),
        relation("relation:contains:o012-d60-integrated-rights:hints-r01-r06-original", "contains", INTEGRATED_RIGHTS, RIGHTS, "The integrated route contains the independently licensed original hint component.", rights_mapping_role="integrated_route_component"),
    ]
    for binding in data["bindings"]:
        hint = backend_hint_id(binding)
        token = hint.removeprefix("unit:")
        relations.append(relation(f"relation:contains:o012-d60-hints-r01-r06:{token}", "contains", ROOT, hint, f"The mastery layer contains {binding['stable_id']}.", contained_role="hint", course_route_unit_id=binding["route"], component_id=binding["component_id"]))
        relations.append(relation(f"relation:hints:{token}:{binding['target_id'].removeprefix('unit:')}", "hints", hint, binding["target_id"], f"Original stable hint for the exact existing exercise/full-solution pair {binding['stable_id']}.", course_route_unit_id=binding["route"], component_id=binding["component_id"], existing_solution_id=binding["solution_id"], source_local_id=binding["stable_id"]))

    additions = {name: [] for name in FILES}
    additions["units.jsonl"] = units; additions["segments.jsonl"] = segments
    additions["rights.jsonl"] = rights; additions["qa.jsonl"] = qa_events
    additions["artifacts.jsonl"] = artifacts; additions["relations.jsonl"] = relations
    for name in FILES:
        additions[name] = sorted(additions[name], key=lambda record: record["id"])
    return additions


def suffixes(additions: dict[str, list[dict[str, Any]]]) -> dict[str, bytes]:
    return {name: b"".join(canon(record) for record in additions[name]) for name in FILES}


def record_plan(additions: dict[str, list[dict[str, Any]]], identities: dict[str, tuple[int, int, str]]) -> dict[str, Any]:
    raw = suffixes(additions)
    return {
        "edition_unit_id": EDITION_UNIT_ID,
        "immutable_prefix": {"records": PREFIX_TOTAL[0], "bytes": PREFIX_TOTAL[1], "bundle_sha256": PREFIX_TOTAL[2]},
        "inputs": {path: {"bytes": value[0], "lf_lines": value[1], "sha256": value[2]} for path, value in identities.items()},
        "records_by_file": {name: len(additions[name]) for name in FILES},
        "bytes_by_file": {name: len(raw[name]) for name in FILES},
        "record_ids_by_file": {name: [record["id"] for record in additions[name]] for name in FILES},
    }


def validate_graph(records: list[dict[str, Any]]) -> dict[str, Any]:
    units = {record["id"]: record for record in records if record.get("entity_type") == "unit" and record.get("status") == "active"}
    relations = [record for record in records if record.get("entity_type") == "relation" and record.get("status") == "active"]
    hints = [record for record in units.values() if record.get("unit_kind") == "hint"]
    hint_edges = [record for record in relations if record.get("relation_type") == "hints"]
    solve_edges = [record for record in relations if record.get("relation_type") == "solves"]
    require((len(hints), len(hint_edges), len(solve_edges)) == (165, 165, 221), "active hint/hints/solves postcondition mismatch")
    hints_by_exercise: dict[str, list[dict[str, Any]]] = defaultdict(list)
    solves_by_exercise: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for edge in hint_edges: hints_by_exercise[edge["to_id"]].append(edge)
    for edge in solve_edges: solves_by_exercise[edge["to_id"]].append(edge)
    triples: list[tuple[str, str, str]] = []
    for exercise_id, edges in hints_by_exercise.items():
        require(len(edges) == 1, f"exercise has non-unique hint edge: {exercise_id}")
        solves = solves_by_exercise.get(exercise_id, [])
        require(len(solves) == 1, f"hinted exercise has non-unique solution edge: {exercise_id}")
        hint_id = edges[0]["from_id"]; solution_id = solves[0]["from_id"]
        require(units.get(hint_id, {}).get("unit_kind") == "hint", f"wrong hint endpoint kind: {hint_id}")
        require(units.get(exercise_id, {}).get("unit_kind") == "exercise", f"wrong exercise endpoint kind: {exercise_id}")
        require(units.get(solution_id, {}).get("unit_kind") == "solution", f"wrong solution endpoint kind: {solution_id}")
        triples.append((exercise_id, hint_id, solution_id))
    require(len(triples) == 165, "graph-complete triple count is not 165")
    solution_ids = [item[2] for item in triples]
    require(len(solution_ids) == len(set(solution_ids)), "duplicate/reused solution across graph-complete triples")
    assessment_triples = [item for item in triples if any(units[entity].get("assessment_id") for entity in item)]
    ordinary = [item for item in triples if item not in assessment_triples]
    require(len(assessment_triples) == 8 and len(ordinary) == 157, "ordinary/assessment triple partition mismatch")
    route_counts: Counter[str] = Counter()
    for _, hint_id, _ in ordinary:
        match = re.search(r"unit:o012-rbt-l(\d{2})", hint_id)
        if match:
            lecture = int(match.group(1))
            for start, end, route in ((1,2,1),(3,4,2),(5,6,3),(7,10,4),(11,13,5),(14,17,6),(18,19,7),(20,27,13),(28,30,14)):
                if start <= lecture <= end: route_counts[f"D60-R{route:02d}"] += 1; break
        else:
            fmatch = re.search(r"unit:o012-fom-u(\d{3})", hint_id)
            require(fmatch is not None, f"cannot infer ordinary hint route: {hint_id}")
            unit = int(fmatch.group(1)); route_counts[{1: "D60-R08", 2: "D60-R09", 3: "D60-R10", 4: "D60-R11", 5: "D60-R12", 6: "D60-R12", 7: "D60-R12"}[unit]] += 1
    capped = sum(min(route_counts[f"D60-R{route:02d}"], 6) for route in range(1, 15))
    require(capped == 84, f"ordinary mastery capped credit is {capped}, expected 84")
    return {"active_hint_units": 165, "active_hint_relations": 165, "active_solves_relations": 221, "graph_complete_triples": 165, "ordinary_graph_complete_triples": 157, "ordinary_capped_route_credit": 84, "ca01_items": 8, "credited_total": 92, "duplicate_or_reused_solution_ids": 0}


def validate_semantics(prefix_records: list[dict[str, Any]], additions: dict[str, list[dict[str, Any]]], data: dict[str, Any]) -> dict[str, Any]:
    added = [record for name in FILES for record in additions[name]]
    require(len(added) == 158, f"suffix record count is {len(added)}, expected 158")
    records = prefix_records + added
    by_id = {record["id"]: record for record in records}
    require(len(by_id) == len(records), "global ID collision in merged graph")
    generic = load_module("scripts/validate-backend.py", "o012_generic_backend_for_hint_layer")
    try:
        generic.validate_shapes(records); generic.validate_references(records, by_id); generic.validate_artifact_manifests(records, LANE)
    except Exception as exc:
        raise SystemExit(f"ordinary-hint backend producer FAIL: merged generic schema/reference validation failed: {exc}")
    require({COURSE, PROGRAM, EDITION_CONTEXT, RESOURCE_CONTEXT, INTEGRATED_RIGHTS} <= by_id.keys(), "required context IDs absent")
    require(Counter(record["unit_kind"] for record in additions["units.jsonl"]) == Counter({"reader_unit": 1, "hint": 36}), "unit-kind census mismatch")
    require(Counter(record["segment_kind"] for record in additions["segments.jsonl"]) == Counter({"mastery_support": 1, "hint": 36}), "segment-kind census mismatch")
    require(Counter(record["relation_type"] for record in additions["relations.jsonl"]) == Counter({"contains": 39, "hints": 36}), "relation census mismatch")
    require(len(additions["rights.jsonl"]) == 1 and len(additions["artifacts.jsonl"]) == len(additions["qa.jsonl"]) == 4, "rights/artifact/QA census mismatch")
    require(not additions["assets.jsonl"] and not additions["authority.jsonl"] and not additions["concepts.jsonl"] and not additions["corrections.jsonl"] and not additions["terms.jsonl"], "unexpected record class in suffix")
    require(not any(record.get("unit_kind") in {"exercise", "solution"} for record in additions["units.jsonl"]), "prompt or solution unit introduced")
    require(not any(record.get("relation_type") == "solves" for record in additions["relations.jsonl"]), "solves relation introduced")
    source_locals = {record["source_local_id"] for record in additions["units.jsonl"] if record["unit_kind"] == "hint"}
    require(source_locals == {item["stable_id"] for item in data["bindings"]}, "source/backend hint stable-ID inventory mismatch")
    for binding in data["bindings"]:
        hint_id = backend_hint_id(binding)
        hint = by_id[hint_id]
        require((hint["course_route_unit_id"], hint["component_id"], hint["target_exercise_id"], hint["existing_solution_id"]) == (binding["route"], binding["component_id"], binding["target_id"], binding["solution_id"]), f"hint backend binding mismatch: {binding['stable_id']}")
        edges = [record for record in additions["relations.jsonl"] if record["relation_type"] == "hints" and record["from_id"] == hint_id]
        require(len(edges) == 1 and edges[0]["to_id"] == binding["target_id"] and edges[0]["existing_solution_id"] == binding["solution_id"], f"hint relation binding mismatch: {binding['stable_id']}")
    rights = additions["rights.jsonl"][0]
    require(rights["license_expression"] == "CC-BY-SA-4.0" and set(rights["component_scope"]) == {record["id"] for record in additions["units.jsonl"]}, "original rights closure mismatch")
    expected_paths = set(INPUT_PATHS)
    require({record["path"] for record in additions["artifacts.jsonl"]} == expected_paths, "artifact evidence set mismatch")
    require(Counter(record["qa_type"] for record in additions["qa.jsonl"]) == Counter({"structure":1,"math":1,"language":1,"mastery":1}), "QA event census mismatch")
    graph = validate_graph(records)
    joined = b"".join(suffixes(additions).values()).lower()
    for marker in (b"c:\\users", b"github_pat_", b"ghp_", b"access_token", b"authorization: bearer"):
        require(marker not in joined, f"private path or credential marker in suffix: {marker!r}")
    return {"merged_records": len(records), "added_records": len(added), "schema_shapes": "PASS", "global_references": "PASS", "artifact_evidence": "PASS", "prompt_solution_solves_immutability": "PASS", "route_mapping": "PASS", "rights_closure": "PASS", "graph_postconditions": graph}


def backend_totals(backend: Path) -> tuple[int, int, str]:
    bundle = hashlib.sha256(); records = byte_count = 0
    for name in FILES:
        raw = (backend / name).read_bytes(); records += len(raw.splitlines()); byte_count += len(raw)
        bundle.update(name.encode("utf-8")); bundle.update(b"\0"); bundle.update(raw)
    return records, byte_count, bundle.hexdigest()


def append_suffix(backend: Path, prefix: dict[str, bytes], additions: dict[str, list[dict[str, Any]]]) -> dict[str, bytes]:
    raw_suffixes = suffixes(additions)
    for name in FILES: require((backend / name).read_bytes() == prefix[name], f"prefix changed immediately before append: {name}")
    for name in FILES:
        if raw_suffixes[name]:
            with (backend / name).open("ab") as stream: stream.write(raw_suffixes[name])
    for name in FILES: require((backend / name).read_bytes() == prefix[name] + raw_suffixes[name], f"exact binary append mismatch: {name}")
    return raw_suffixes


def main() -> int:
    require(sys.argv[1:] in ([], ["--plan"]), "accepted invocation is no arguments or --plan")
    prefix, prefix_records = verify_prefix(BACKEND)
    data = verify_inputs(); additions = build_additions(data, prefix_records)
    semantic = validate_semantics(prefix_records, additions, data)
    plan = record_plan(additions, data["identities"])
    if sys.argv[1:] == ["--plan"]:
        print(json.dumps(plan, ensure_ascii=False, sort_keys=True, indent=2)); return 0
    refreshed = verify_inputs(); refreshed_additions = build_additions(refreshed, prefix_records)
    require(record_plan(refreshed_additions, refreshed["identities"]) == plan and suffixes(refreshed_additions) == suffixes(additions), "sealed inputs changed derived plan before append")
    raw_suffixes = append_suffix(BACKEND, prefix, additions)
    final = backend_totals(BACKEND)
    require(final[0] == 7012, "cumulative record count is not 7,012")
    print("ordinary-hint append-only semantic backend extension: PASS")
    print(f"prefix_records={PREFIX_TOTAL[0]}"); print(f"prefix_bytes={PREFIX_TOTAL[1]}"); print(f"prefix_bundle_sha256={PREFIX_TOTAL[2]}")
    print(f"records_added={semantic['added_records']}"); print(f"suffix_bytes={sum(len(raw_suffixes[name]) for name in FILES)}")
    print(f"cumulative_records={final[0]}"); print(f"cumulative_bytes={final[1]}"); print(f"backend_bundle_sha256={final[2]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
