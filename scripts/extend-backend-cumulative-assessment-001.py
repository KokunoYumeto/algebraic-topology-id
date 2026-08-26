#!/usr/bin/env python3
"""Fail-closed append-only admission for original cumulative assessment D60-CA01.

The published Roberts-001-030/Fomberg-001-007 backend is an immutable prefix.
This producer verifies every prefix byte and every independent CA01 witness,
derives a canonical suffix, validates the merged graph in memory, and performs
only binary append writes.  It has no replacement or repair mode.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any


LANE = Path(__file__).resolve().parents[1]
BACKEND = LANE / "backend"
READER_PATH = "source/id-ID/mastery/cumulative-assessment-001-foundations-coverings-homotopy.md"
MATH_PATH = "qa/cumulative-assessment-001/INDEPENDENT_MATH_REVIEW.json"
LANGUAGE_PATH = "qa/cumulative-assessment-001/INDEPENDENT_SOURCE_LANGUAGE_REVIEW.json"
QA_PATH = "qa/CUMULATIVE_ASSESSMENT_001_QA.json"
READER_SHA256 = "5888df0410ad7e8ccf50d8ea8092e43a42f6df94c242f7c09abe0616d972e6f8"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"
SCHEMA = "curriculum.interop"
SCHEMA_VERSION = "0.1.0"
WORKFLOW = "o012-d60-id-reader-production"
TIMESTAMP = "2026-08-26T00:00:00Z"
ROOT = "unit:o012-d60-ca01"
ROOT_SEGMENT = "segment:o012-d60-ca01"
RIGHTS = "rights:o012-d60-ca01-original-cc-by-sa-4.0"
COURSE = "course:o012-d60"
PROGRAM = "program:o012-id"
EDITION_CONTEXT = "edition:roberts-at-2019-b947ad2"
RESOURCE_CONTEXT = "resource:roberts-algebraic-topology-2019"
INTEGRATED_RIGHTS = "rights:o012-d60-integrated-route-cc-by-sa-4.0"

FILES = (
    "artifacts.jsonl", "assets.jsonl", "authority.jsonl", "concepts.jsonl",
    "corrections.jsonl", "qa.jsonl", "relations.jsonl", "rights.jsonl",
    "segments.jsonl", "terms.jsonl", "units.jsonl",
)
PREFIX = {
    "artifacts.jsonl": (189, 153754, "7294792526f75a1ea2409f797fa25c28694e115c95541387482602447e6ba646"),
    "assets.jsonl": (87, 64692, "1df40f8f6ca4f2fbfbe8a7b924a68a153713a20a4eebe1d014d8fb04669945f7"),
    "authority.jsonl": (6, 4374, "84c622f56dbbd5ba379361245ecfe07bc79c9f4fd6b18ba21b82b5f545211869"),
    "concepts.jsonl": (483, 152695, "720d96a10a3c2abebab164e2181486743ef99efb50c6ef419faefbf528b8ead3"),
    "corrections.jsonl": (564, 594720, "bd961fad5d83e96fec6ef83caa8447e2e5f282c603fd4983d79b5b4b54049fbb"),
    "qa.jsonl": (162, 88999, "da5c09949d53c4f77ca0c4089d99ca6ba178bdc4b7a463eb8bf68a55e9853e19"),
    "relations.jsonl": (784, 329688, "1aea5c4f3e619718bda4c065f9d70d3281b4b35bcd712e8c98fcfbcf7509fefa"),
    "rights.jsonl": (103, 93018, "212673ced3907e59f8a38603f1c625a263a95656908c656a86e0d881b77f93b6"),
    "segments.jsonl": (1929, 3130165, "6078880c58c6b3194e874c85b4f2716b5436f0559f607f1b7551cd5140ffa376"),
    "terms.jsonl": (476, 315218, "4b82f9d582ba747829373a7935fcc3cae56b96fd6b7486969ebb6d54cf927c50"),
    "units.jsonl": (1959, 3286326, "e2855fe4bb13ce55f48b29bd7d3279d5db7023ef6207fd07bf7b98385d5ddb63"),
}
PREFIX_TOTAL = (6742, 8213649, "523b570517eb54720c50007aacc5d4eea525ea252b9ca1f6f45b027182354765")

INPUT_IDENTITIES = {
    READER_PATH: (15185, 389, READER_SHA256),
    MATH_PATH: (2446, 44, "4bfae9714bf6c5b5c936a7ccf2bf82ab4e5c063f8519e4122bd455740bf5307e"),
    LANGUAGE_PATH: (2303, 60, "79d8d17df956267af6a433735b0a610c46e5409e67259b74396878c50cf356ad"),
    QA_PATH: (1812, 64, "8dcd7bd124ce16acebef875b8294138caa91801b00d9a621919831bc1f09f602"),
}

ROUTES = {
    1: ("D60-R01", "unit:o012-rbt-u001", ()),
    2: ("D60-R02", "unit:o012-rbt-u003", ()),
    3: ("D60-R03", "unit:o012-rbt-u005", ()),
    4: ("D60-R04", "unit:o012-rbt-u007", ()),
    5: ("D60-R05", "unit:o012-rbt-u011", ()),
    6: ("D60-R06", "unit:o012-rbt-u014", ()),
    7: ("D60-R07", "unit:o012-rbt-u018", ()),
    8: ("D60-R06", "unit:o012-rbt-u014", (("D60-R04", "unit:o012-rbt-u007"), ("D60-R05", "unit:o012-rbt-u011"))),
}

CONCEPTS = {
    1: ["concept:quotient-map", "concept:quotient-space", "concept:quotient-topology", "concept:compactness"],
    2: ["concept:deformation-retract", "concept:homotopy-equivalence", "concept:fundamental-group"],
    3: ["concept:path-lifting", "concept:fundamental-group", "concept:covering-map"],
    4: ["concept:monodromy", "concept:covering-action", "concept:stabilizer-subgroup", "concept:connected-covering-space"],
    5: ["concept:cw-complex", "concept:seifert-van-kampen-theorem", "concept:group-presentation", "concept:normal-closure"],
    6: ["concept:classification-of-covering-spaces", "concept:connected-covering-space", "concept:fundamental-group"],
    7: ["concept:fibre-bundle", "concept:long-exact-sequence", "concept:higher-homotopy-group"],
    8: ["concept:covering-map", "concept:covering-space-classification", "concept:fundamental-group", "concept:path-lifting"],
}

TITLES = {
    1: "Hasil bagi interval dan lingkaran",
    2: "Retraksi deformasi kuat",
    3: "Pengangkatan lintasan dan bilangan lilit",
    4: "Monodromi penutup berhingga",
    5: "Van Kampen dan grup fundamental torus",
    6: "Klasifikasi penutup lingkaran",
    7: "Barisan eksak homotopi fibrasi Hopf",
    8: "Kriteria pengangkatan peta torus",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"CA01 backend producer FAIL: {message}")


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


def load_generic():
    path = LANE / "scripts/validate-backend.py"
    spec = importlib.util.spec_from_file_location("o012_generic_backend_for_ca01", path)
    require(spec is not None and spec.loader is not None, "cannot load generic backend validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def input_identity(relative: str) -> tuple[int, int, str]:
    path = LANE / relative
    require(path.is_file(), f"required input is missing: {relative}")
    raw = path.read_bytes()
    require(b"\r" not in raw and raw.endswith(b"\n"), f"input is not UTF-8/LF disciplined: {relative}")
    try:
        raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise SystemExit(f"CA01 backend producer FAIL: invalid UTF-8 in {relative}: {exc}")
    return len(raw), raw.count(b"\n"), digest(raw)


def verify_inputs() -> dict[str, Any]:
    identities = {relative: input_identity(relative) for relative in INPUT_IDENTITIES}
    require(identities == INPUT_IDENTITIES, f"sealed CA01 input identity drift: {identities!r}")
    reader_raw = (LANE / READER_PATH).read_bytes()
    reader_text = reader_raw.decode("utf-8")
    require(reader_text.count(MODEL) == 1, "model provenance must occur exactly once in the reader")
    require("materi edisi asli" in reader_text.lower(), "original-layer notice missing")
    require("bank masalah Fomberg" in reader_text, "excluded Fomberg-bank notice missing")
    for number, (route, _, secondary) in ROUTES.items():
        for kind in ("ex", "hint", "sol"):
            local_id = f"o012-d60-ca01-{kind}-{number:03d}"
            require(reader_text.count(f"#{local_id}") == 1, f"stable ID count drift: {local_id}")
            line = next(line for line in reader_text.splitlines() if f"#{local_id}" in line)
            require(f'data-course-route-unit-id="{route}"' in line, f"primary route mismatch: {local_id}")
            expected_secondary = ",".join(item[0] for item in secondary)
            if expected_secondary:
                require(f'data-secondary-route-unit-ids="{expected_secondary}"' in line, f"secondary routes mismatch: {local_id}")
            else:
                require("data-secondary-route-unit-ids" not in line, f"unexpected secondary route: {local_id}")

    reviews: dict[str, Any] = {}
    for relative, kind in ((MATH_PATH, "independent_mathematics"), (LANGUAGE_PATH, "independent_source_language")):
        receipt = json.loads((LANE / relative).read_text(encoding="utf-8"))
        require(receipt.get("review_kind") == kind, f"review kind mismatch: {relative}")
        require(str(receipt.get("status", "")).startswith("PASS"), f"review did not pass: {relative}")
        require(receipt.get("independent_from_production") is True, f"review independence missing: {relative}")
        require(receipt.get("reader_sha256") == READER_SHA256, f"review binds stale reader: {relative}")
        severity = receipt.get("severity_census", {})
        require((severity.get("P1"), severity.get("P2"), severity.get("P3")) == (0, 0, 0), f"review findings remain: {relative}")
        reviews[kind] = receipt
    qa = json.loads((LANE / QA_PATH).read_text(encoding="utf-8"))
    require(qa.get("status") == "PASS" and qa.get("assessment_id") == "D60-CA01", "CA01 QA is not a passing D60-CA01 receipt")
    require(qa.get("reader", {}).get("identity", {}).get("sha256") == READER_SHA256, "CA01 QA binds stale reader")
    require(qa.get("reader", {}).get("exercise_hint_solution_triples") == 8, "CA01 QA triple census mismatch")
    require(qa.get("reader", {}).get("complete_checked_solutions") == 8, "CA01 QA solution census mismatch")
    require(qa.get("rights", {}).get("license") == "CC BY-SA 4.0", "CA01 QA rights mismatch")
    for label, relative in (("mathematics", MATH_PATH), ("source_language", LANGUAGE_PATH)):
        expected = INPUT_IDENTITIES[relative]
        found = qa.get("independent_reviews", {}).get(label, {})
        require((found.get("bytes"), found.get("lf_lines"), found.get("sha256")) == expected, f"CA01 QA review binding mismatch: {label}")
    return {"identities": identities, "reader_raw": reader_raw, "reader_text": reader_text, "reviews": reviews, "qa": qa}


def parse_prefix_records(raw_by_file: dict[str, bytes]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for name in FILES:
        raw = raw_by_file[name]
        require(b"\r" not in raw and raw.endswith(b"\n"), f"prefix JSONL discipline mismatch: {name}")
        for line_number, line in enumerate(raw.splitlines(keepends=True), 1):
            try:
                record = json.loads(line.decode("utf-8", errors="strict"))
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                raise SystemExit(f"CA01 backend producer FAIL: {name}:{line_number}: {exc}")
            require(canon(record) == line, f"noncanonical prefix record: {name}:{line_number}")
            records.append(record)
    return records


def verify_prefix(backend: Path = BACKEND) -> tuple[dict[str, bytes], list[dict[str, Any]]]:
    raw_by_file: dict[str, bytes] = {}
    bundle = hashlib.sha256()
    total_records = total_bytes = 0
    for name in FILES:
        path = backend / name
        require(path.is_file(), f"backend file missing: {name}")
        raw = path.read_bytes()
        expected = PREFIX[name]
        observed = (len(raw.splitlines()), len(raw), digest(raw))
        require(observed == expected, f"immutable Unit 007 prefix mismatch: {name}: {observed!r}")
        raw_by_file[name] = raw
        bundle.update(name.encode("utf-8")); bundle.update(b"\0"); bundle.update(raw)
        total_records += observed[0]; total_bytes += observed[1]
    require((total_records, total_bytes, bundle.hexdigest()) == PREFIX_TOTAL, "immutable Unit 007 prefix bundle mismatch")
    return raw_by_file, parse_prefix_records(raw_by_file)


def locator(lines: list[bytes], start: int, end: int) -> dict[str, Any]:
    return {
        "content_sha256": digest(b"".join(lines[start - 1:end])),
        "file_sha256": READER_SHA256,
        "line_end": end,
        "line_start": start,
        "path": READER_PATH,
    }


def spans(reader_raw: bytes) -> dict[str, tuple[int, int]]:
    lines = reader_raw.splitlines(keepends=True)
    decoded = [line.decode("utf-8") for line in lines]
    out = {"o012-d60-ca01": (20, len(lines))}
    for number in range(1, 9):
        for kind in ("ex", "hint", "sol"):
            local_id = f"o012-d60-ca01-{kind}-{number:03d}"
            starts = [index for index, line in enumerate(decoded, 1) if f"#{local_id}" in line]
            require(len(starts) == 1, f"cannot locate one opening for {local_id}")
            start = starts[0]
            require(decoded[start - 1].startswith("::: {"), f"stable ID is not on a fenced-div opening: {local_id}")
            ends = [index for index in range(start + 1, len(lines) + 1) if decoded[index - 1].strip() == ":::" ]
            require(ends, f"cannot locate fenced-div close: {local_id}")
            out[local_id] = (start, ends[0])
    require(len(out) == 25, "root/triple span census mismatch")
    return out


def route_fields(number: int) -> dict[str, Any]:
    route, _, secondary = ROUTES[number]
    return {
        "course_route_unit_id": route,
        "course_route_unit_ids": [route] + [item[0] for item in secondary],
        "primary_course_route_unit_id": route,
        "secondary_course_route_unit_ids": [item[0] for item in secondary],
        "route_mapping_status": "explicit_primary_and_secondary",
    }


def unit_record(local_id: str, kind: str, title: str, order: int, span: tuple[int, int], concept_ids: list[str], number: int | None) -> dict[str, Any]:
    ident = f"unit:{local_id}"
    record = {
        **common("unit", ident),
        "assessment_id": "D60-CA01",
        "authority_context_ids": [COURSE, PROGRAM, EDITION_CONTEXT, RESOURCE_CONTEXT],
        "authority_context_only": True,
        "concept_ids": concept_ids,
        "course_id": COURSE,
        "display_title": title,
        "edition_context_only": True,
        "edition_id": EDITION_CONTEXT,
        "edition_unit_id": "O012-ORIG-CA01",
        "locale": "id-ID",
        "model_provenance": MODEL,
        "order": order,
        "original_layer": True,
        "parent_id": COURSE if kind == "reader_unit" else ROOT,
        "path": [ROOT] if kind == "reader_unit" else [ROOT, ident],
        "program_id": PROGRAM,
        "provenance_relation": "edition_original",
        "resource_context_only": True,
        "resource_id": RESOURCE_CONTEXT,
        "rights_component_id": RIGHTS,
        "source_corpus_used": False,
        "source_local_id": local_id,
        "source_locator": {"kind": "edition_original", "path": READER_PATH, "precision": "exact_target_span", "source_corpus_used": False},
        "target_locator": None,
        "translation_state": "structurally_verified",
        "unit_kind": kind,
    }
    record["target_locator"] = locator((LANE / READER_PATH).read_bytes().splitlines(keepends=True), *span)
    if kind == "reader_unit":
        record.update({
            "assessment_kind": "cumulative_assessment",
            "course_route_unit_ids": [f"D60-R{number:02d}" for number in range(1, 8)],
            "order": 38,
            "reader_scope": "eight_exercises_eight_hints_eight_complete_checked_solutions",
        })
    else:
        require(number is not None, "child record lacks item number")
        record.update(route_fields(number))
        record["assessment_item_number"] = number
        if kind == "solution":
            record["solution_status"] = "complete_checked_solution"
    return record


def segment_from_unit(unit: dict[str, Any]) -> dict[str, Any]:
    kind_map = {"reader_unit": "assessment", "exercise": "exercise", "hint": "hint", "solution": "solution"}
    optional = {
        key: unit[key]
        for key in (
            "assessment_id", "assessment_item_number", "authority_context_ids",
            "authority_context_only", "course_route_unit_id", "course_route_unit_ids",
            "edition_context_only", "edition_unit_id", "model_provenance", "original_layer",
            "primary_course_route_unit_id", "resource_context_only", "route_mapping_status",
            "secondary_course_route_unit_ids", "solution_status", "source_corpus_used",
        )
        if key in unit
    }
    return {
        **common("segment", unit["id"].replace("unit:", "segment:", 1)),
        **optional,
        "concept_ids": unit["concept_ids"],
        "edition_id": unit["edition_id"],
        "locale": "id-ID",
        "order": unit["order"],
        "provenance_relation": "edition_original",
        "resource_id": unit["resource_id"],
        "rights_component_id": RIGHTS,
        "segment_kind": kind_map[unit["unit_kind"]],
        "source_local_id": unit["source_local_id"],
        "source_locator": unit["source_locator"],
        "target_locator": unit["target_locator"],
        "translation_state": "structurally_verified",
        "unit_id": unit["id"],
    }


def relation(ident: str, relation_type: str, from_id: str, to_id: str, note: str, **extra: Any) -> dict[str, Any]:
    return {**common("relation", ident), "from_id": from_id, "note": note, "relation_type": relation_type, "to_id": to_id, **extra}


def artifact(ident: str, relative: str, media_type: str, qa_ids: list[str], state: str) -> dict[str, Any]:
    byte_count, _, sha = INPUT_IDENTITIES[relative]
    return {
        **common("artifact", ident),
        "assessment_id": "D60-CA01", "bytes": byte_count, "edition_unit_id": "O012-ORIG-CA01",
        "locale": "id-ID", "manifest_artifact_id": None, "media_type": media_type,
        "path": relative, "qa_event_ids": qa_ids, "rights_component_id": RIGHTS,
        "sha256": sha, "toolchain": f"Original D60-CA01 evidence; {MODEL}; reader {READER_SHA256}; semantic admission only.",
        "translation_state": state, "unit_id": ROOT,
    }


def build_additions(data: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    reader_raw = data["reader_raw"]
    reader_lines = reader_raw.splitlines(keepends=True)
    found_spans = spans(reader_raw)
    all_concepts = sorted({concept for values in CONCEPTS.values() for concept in values})
    units: list[dict[str, Any]] = [unit_record("o012-d60-ca01", "reader_unit", "Asesmen Kumulatif 1 — Fondasi sampai Barisan Eksak Homotopi", 38, found_spans["o012-d60-ca01"], all_concepts, None)]
    for number in range(1, 9):
        for offset, kind in enumerate(("exercise", "hint", "solution"), 1):
            token = {"exercise": "ex", "hint": "hint", "solution": "sol"}[kind]
            local_id = f"o012-d60-ca01-{token}-{number:03d}"
            label = {"exercise": "Soal", "hint": "Petunjuk", "solution": "Solusi lengkap"}[kind]
            units.append(unit_record(local_id, kind, f"{label} {number}: {TITLES[number]}", (number - 1) * 3 + offset, found_spans[local_id], CONCEPTS[number], number))
    segments = [segment_from_unit(record) for record in units]

    rights = [{
        **common("rights", RIGHTS),
        "attribution": "Original cumulative assessment prepared for the independent Indonesian O012/D60 edition.",
        "change_notice": "Edition-original assessment layer; Roberts and Fomberg source components are neither copied nor relicensed.",
        "component_scope": [record["id"] for record in units],
        "license_expression": "CC-BY-SA-4.0",
        "license_url": "https://creativecommons.org/licenses/by-sa/4.0/",
        "non_endorsement": "Independent Indonesian edition; no Roberts, Fomberg, Lazarovich, or source-author endorsement.",
        "third_party_status": "No Roberts or Fomberg prompt, solution, or expression is copied or adapted; existing authority IDs are edition/course context only.",
    }]

    qa_ids = {
        "structure": "qa:o012-d60-ca01-structure",
        "math": "qa:o012-d60-ca01-math",
        "language": "qa:o012-d60-ca01-language",
        "mastery": "qa:o012-d60-ca01-mastery",
    }
    artifacts = [
        artifact("artifact:o012-d60-ca01-reader-source", READER_PATH, "text/markdown", list(qa_ids.values()), "structurally_verified"),
        artifact("artifact:o012-d60-ca01-math-review", MATH_PATH, "application/json", [qa_ids["math"]], "mathematically_reviewed"),
        artifact("artifact:o012-d60-ca01-language-review", LANGUAGE_PATH, "application/json", [qa_ids["language"]], "language_reviewed"),
        artifact("artifact:o012-d60-ca01-qa-receipt", QA_PATH, "application/json", [qa_ids["structure"], qa_ids["mastery"], qa_ids["math"], qa_ids["language"]], "built"),
    ]
    qa_events = [
        {**common("qa_event", qa_ids["structure"]), "assessment_id": "D60-CA01", "note": "Stable-ID inventory, eight balanced triples, route metadata, LF/UTF-8, rights, provenance, and privacy checks passed.", "qa_type": "structure", "result": "passed", "unit_id": ROOT, "witness_artifact_ids": ["artifact:o012-d60-ca01-reader-source", "artifact:o012-d60-ca01-qa-receipt"]},
        {**common("qa_event", qa_ids["math"]), "assessment_id": "D60-CA01", "note": "Independent mathematics review passed all eight exercise/hint/solution triples with P1=P2=P3=0.", "qa_type": "math", "result": "passed", "unit_id": ROOT, "witness_artifact_ids": ["artifact:o012-d60-ca01-math-review", "artifact:o012-d60-ca01-qa-receipt"]},
        {**common("qa_event", qa_ids["language"]), "assessment_id": "D60-CA01", "note": "Independent id-ID source-language, terminology, accessibility, rights, and provenance review passed with P1=P2=P3=0.", "qa_type": "language", "result": "passed", "unit_id": ROOT, "witness_artifact_ids": ["artifact:o012-d60-ca01-language-review", "artifact:o012-d60-ca01-qa-receipt"]},
        {**common("qa_event", qa_ids["mastery"]), "assessment_id": "D60-CA01", "note": "Eight cumulative exercises each have one stable hint and one complete checked solution across D60-R01 through D60-R07.", "qa_type": "mastery", "result": "passed", "unit_id": ROOT, "witness_artifact_ids": ["artifact:o012-d60-ca01-reader-source", "artifact:o012-d60-ca01-qa-receipt"]},
    ]

    relations: list[dict[str, Any]] = [
        relation("relation:contains:o012-d60:ca01", "contains", COURSE, ROOT, "The O012/D60 course contains cumulative assessment D60-CA01 as an original learner surface.", assessment_id="D60-CA01", course_route_unit_ids=[f"D60-R{n:02d}" for n in range(1, 8)]),
        relation("relation:contains:o012-d60-ca01-rights:root", "contains", RIGHTS, ROOT, "The original CC BY-SA 4.0 component rights bind the complete CA01 reader graph.", assessment_id="D60-CA01", rights_mapping_role="direct_component_binding"),
        relation("relation:contains:o012-d60-integrated-rights:ca01-original", "contains", INTEGRATED_RIGHTS, RIGHTS, "The integrated route contains the independently licensed CA01 original component without altering source-component licenses.", assessment_id="D60-CA01", rights_mapping_role="integrated_route_component"),
    ]
    for number in range(1, 9):
        exercise = f"unit:o012-d60-ca01-ex-{number:03d}"
        hint = f"unit:o012-d60-ca01-hint-{number:03d}"
        solution = f"unit:o012-d60-ca01-sol-{number:03d}"
        for child, role in ((exercise, "exercise"), (hint, "hint"), (solution, "complete_checked_solution")):
            relations.append(relation(f"relation:contains:o012-d60-ca01:{child.removeprefix('unit:o012-d60-ca01-')}", "contains", ROOT, child, f"CA01 contains item {number} {role}.", assessment_id="D60-CA01", assessment_item_number=number, contained_role=role))
        relations.append(relation(f"relation:hints:o012-d60-ca01-hint-{number:03d}:ex-{number:03d}", "hints", hint, exercise, f"Stable hint for CA01 item {number}.", assessment_id="D60-CA01", assessment_item_number=number))
        relations.append(relation(f"relation:solves:o012-d60-ca01-sol-{number:03d}:ex-{number:03d}", "solves", solution, exercise, f"Complete checked solution for CA01 item {number}.", assessment_id="D60-CA01", assessment_item_number=number, solution_status="complete_checked_solution"))
        primary_route, primary_anchor, secondary = ROUTES[number]
        relations.append(relation(f"relation:xref:o012-d60-ca01-ex-{number:03d}:{primary_route.lower()}", "xref", exercise, primary_anchor, f"Primary course-route mapping for CA01 item {number}: {primary_route}.", assessment_id="D60-CA01", course_route_unit_id=primary_route, route_mapping_role="primary", route_source_anchor_id=primary_anchor))
        for route_id, anchor in secondary:
            relations.append(relation(f"relation:xref:o012-d60-ca01-ex-{number:03d}:{route_id.lower()}:secondary", "xref", exercise, anchor, f"Secondary synthesis mapping for CA01 item {number}: {route_id}.", assessment_id="D60-CA01", course_route_unit_id=route_id, route_mapping_role="secondary", route_source_anchor_id=anchor))

    additions = {name: [] for name in FILES}
    additions["units.jsonl"] = units
    additions["segments.jsonl"] = segments
    additions["rights.jsonl"] = rights
    additions["qa.jsonl"] = qa_events
    additions["artifacts.jsonl"] = artifacts
    additions["relations.jsonl"] = relations
    for name in FILES:
        additions[name] = sorted(additions[name], key=lambda record: record["id"])
    return additions


def suffixes(additions: dict[str, list[dict[str, Any]]]) -> dict[str, bytes]:
    return {name: b"".join(canon(record) for record in additions[name]) for name in FILES}


def record_plan(additions: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    raw = suffixes(additions)
    return {
        "assessment_id": "D60-CA01",
        "edition_unit_id": "O012-ORIG-CA01",
        "immutable_prefix": {"records": PREFIX_TOTAL[0], "bytes": PREFIX_TOTAL[1], "bundle_sha256": PREFIX_TOTAL[2]},
        "reader": {"path": READER_PATH, "bytes": INPUT_IDENTITIES[READER_PATH][0], "sha256": READER_SHA256},
        "records_by_file": {name: len(additions[name]) for name in FILES},
        "bytes_by_file": {name: len(raw[name]) for name in FILES},
        "record_ids_by_file": {name: [record["id"] for record in additions[name]] for name in FILES},
    }


def validate_semantics(prefix_records: list[dict[str, Any]], additions: dict[str, list[dict[str, Any]]], data: dict[str, Any]) -> dict[str, Any]:
    added_records = [record for name in FILES for record in additions[name]]
    records = prefix_records + added_records
    by_id = {record["id"]: record for record in records}
    require(len(by_id) == len(records), "global ID collision in merged graph")
    generic = load_generic()
    try:
        generic.validate_shapes(records)
        generic.validate_references(records, by_id)
        generic.validate_artifact_manifests(records, LANE)
    except Exception as exc:
        raise SystemExit(f"CA01 backend producer FAIL: merged generic schema/reference validation failed: {exc}")
    required_context = {COURSE, PROGRAM, EDITION_CONTEXT, RESOURCE_CONTEXT, INTEGRATED_RIGHTS}
    require(required_context <= by_id.keys(), "required existing authority/context IDs are absent")
    require(all(by_id[item]["entity_type"] == expected for item, expected in ((COURSE, "course"), (PROGRAM, "program"), (EDITION_CONTEXT, "edition"), (RESOURCE_CONTEXT, "resource"))), "authority/context entity type mismatch")

    units = additions["units.jsonl"]
    segments = additions["segments.jsonl"]
    require(len(units) == len(segments) == 25, "root plus 24 item unit/segment census mismatch")
    require(Counter(record["unit_kind"] for record in units) == Counter({"reader_unit": 1, "exercise": 8, "hint": 8, "solution": 8}), "unit-kind census mismatch")
    require(Counter(record["segment_kind"] for record in segments) == Counter({"assessment": 1, "exercise": 8, "hint": 8, "solution": 8}), "segment-kind census mismatch")
    require({record["source_local_id"] for record in units} == {record["source_local_id"] for record in segments}, "unit/segment stable-ID inventory mismatch")
    segment_by_local = {record["source_local_id"]: record for record in segments}
    for unit in units:
        segment = segment_by_local[unit["source_local_id"]]
        require(segment["unit_id"] == unit["id"] and segment["target_locator"] == unit["target_locator"], f"unit/segment mapping mismatch: {unit['id']}")
        require(unit["provenance_relation"] == "edition_original" and unit["source_corpus_used"] is False and unit["original_layer"] is True, f"source/original demarcation mismatch: {unit['id']}")
        require(unit["rights_component_id"] == RIGHTS and segment["rights_component_id"] == RIGHTS, f"rights mismatch: {unit['id']}")
    require(all(record.get("solution_status") == "complete_checked_solution" for record in units if record["unit_kind"] == "solution"), "solution status mismatch")

    relations = additions["relations.jsonl"]
    relation_counts = Counter(record["relation_type"] for record in relations)
    require(relation_counts == Counter({"contains": 27, "hints": 8, "solves": 8, "xref": 10}), f"relation census mismatch: {dict(relation_counts)}")
    for number, (primary_route, primary_anchor, secondary) in ROUTES.items():
        ex = by_id[f"unit:o012-d60-ca01-ex-{number:03d}"]
        require(ex["primary_course_route_unit_id"] == primary_route and ex["secondary_course_route_unit_ids"] == [item[0] for item in secondary], f"route fields mismatch: item {number}")
        route_links = [record for record in relations if record["from_id"] == ex["id"] and record.get("route_mapping_role")]
        require(len([record for record in route_links if record["route_mapping_role"] == "primary" and record["course_route_unit_id"] == primary_route and record["to_id"] == primary_anchor]) == 1, f"primary route relation mismatch: item {number}")
        require({(record["course_route_unit_id"], record["to_id"]) for record in route_links if record["route_mapping_role"] == "secondary"} == set(secondary), f"secondary route relation mismatch: item {number}")
        require(len([record for record in relations if record["relation_type"] == "hints" and record["to_id"] == ex["id"]]) == 1, f"hint link mismatch: item {number}")
        solves = [record for record in relations if record["relation_type"] == "solves" and record["to_id"] == ex["id"]]
        require(len(solves) == 1 and solves[0].get("solution_status") == "complete_checked_solution", f"solution link mismatch: item {number}")
    rights_record = additions["rights.jsonl"][0]
    require(rights_record["license_expression"] == "CC-BY-SA-4.0" and set(rights_record["component_scope"]) == {record["id"] for record in units}, "original rights closure mismatch")

    expected_paths = set(INPUT_IDENTITIES)
    artifacts = additions["artifacts.jsonl"]
    require({record["path"] for record in artifacts} == expected_paths, "artifact evidence set mismatch")
    for artifact_record in artifacts:
        relative = artifact_record["path"]
        expected = INPUT_IDENTITIES[relative]
        require((artifact_record["bytes"], artifact_record["sha256"]) == (expected[0], expected[2]), f"artifact identity mismatch: {relative}")
    require(Counter(record["qa_type"] for record in additions["qa.jsonl"]) == Counter({"structure": 1, "math": 1, "language": 1, "mastery": 1}), "QA event census mismatch")
    require(all(record["result"] == "passed" and record["witness_artifact_ids"] for record in additions["qa.jsonl"]), "QA witness closure mismatch")

    raw_suffixes = suffixes(additions)
    joined = b"".join(raw_suffixes[name] for name in FILES)
    lower = joined.lower()
    require(b"c:\\users" not in lower and b"github_pat_" not in lower and b"ghp_" not in lower and b"access_token" not in lower and b"authorization: bearer" not in lower, "private path or credential marker in suffix")
    return {
        "merged_records": len(records),
        "added_records": len(added_records),
        "unit_kind_counts": dict(Counter(record["unit_kind"] for record in units)),
        "segment_kind_counts": dict(Counter(record["segment_kind"] for record in segments)),
        "relation_type_counts": dict(relation_counts),
        "qa_type_counts": dict(Counter(record["qa_type"] for record in additions["qa.jsonl"])),
        "schema_shapes": "PASS", "global_references": "PASS", "artifact_evidence": "PASS",
        "original_source_demarcation": "PASS", "route_mapping": "PASS", "rights_closure": "PASS",
    }


def backend_totals(backend: Path) -> tuple[int, int, str]:
    bundle = hashlib.sha256(); record_count = byte_count = 0
    for name in FILES:
        raw = (backend / name).read_bytes()
        record_count += len(raw.splitlines()); byte_count += len(raw)
        bundle.update(name.encode("utf-8")); bundle.update(b"\0"); bundle.update(raw)
    return record_count, byte_count, bundle.hexdigest()


def append_suffix(backend: Path, prefix: dict[str, bytes], additions: dict[str, list[dict[str, Any]]]) -> dict[str, bytes]:
    raw_suffixes = suffixes(additions)
    for name in FILES:
        require((backend / name).read_bytes() == prefix[name], f"prefix changed immediately before append: {name}")
    for name in FILES:
        if raw_suffixes[name]:
            with (backend / name).open("ab") as stream:
                stream.write(raw_suffixes[name])
    for name in FILES:
        require((backend / name).read_bytes() == prefix[name] + raw_suffixes[name], f"exact binary append mismatch: {name}")
    return raw_suffixes


def main() -> int:
    require(sys.argv[1:] in ([], ["--plan"]), "accepted invocation is no arguments or --plan")
    data = verify_inputs()
    additions = build_additions(data)
    if sys.argv[1:] == ["--plan"]:
        print(json.dumps(record_plan(additions), ensure_ascii=False, sort_keys=True, indent=2))
        return 0
    baseline_validator = LANE / "scripts/validate-backend-append-only-fomberg-unit-007.py"
    baseline = subprocess.run(
        [sys.executable, "-B", str(baseline_validator)],
        cwd=LANE, capture_output=True, text=True, encoding="utf-8", errors="strict",
    )
    require(
        baseline.returncode == 0 and "Fomberg Unit 007 append-only backend validation: PASS" in baseline.stdout,
        "published Unit 007 append-only baseline validator did not pass before admission: "
        + (baseline.stdout + baseline.stderr).strip(),
    )
    prefix, prefix_records = verify_prefix(BACKEND)
    semantic = validate_semantics(prefix_records, additions, data)
    plan_before = record_plan(additions)
    refreshed = verify_inputs()
    refreshed_additions = build_additions(refreshed)
    require(record_plan(refreshed_additions) == plan_before and suffixes(refreshed_additions) == suffixes(additions), "sealed inputs changed the derived plan before append")
    raw_suffixes = append_suffix(BACKEND, prefix, additions)
    final = backend_totals(BACKEND)
    require(final[0] == PREFIX_TOTAL[0] + semantic["added_records"], "cumulative record count mismatch")
    print("CA01 append-only semantic backend extension: PASS")
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
