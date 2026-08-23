#!/usr/bin/env python3
"""Independent append-only validator for the final Unit 021 backend."""
from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

LANE = Path(__file__).resolve().parents[1]
BACKEND = LANE / "backend"
SOURCE = LANE / "source/id-ID/units/unit-021-lecture-021.md"
QA_JSON = LANE / "qa/UNIT_021_QA.json"
TERMINOLOGY = LANE / "00_control/TERMINOLOGY.csv"
LEDGER = LANE / "00_control/ADVERSE_LEDGER.csv"
FILES = ("artifacts.jsonl", "assets.jsonl", "authority.jsonl", "concepts.jsonl",
         "corrections.jsonl", "qa.jsonl", "relations.jsonl", "rights.jsonl",
         "segments.jsonl", "terms.jsonl", "units.jsonl")
PREFIX = {
    "artifacts.jsonl": (96, 75185, "5c3f5b0a92c5c742c057a0ac9f4d7153d5962c25c003666f1c75a0fd05868cda"),
    "assets.jsonl": (22, 13599, "96ee89e8509f8d32d7d042800ff7e958b04349468e9a97b4ec9bc527bf7a7607"),
    "authority.jsonl": (4, 2721, "f21af26912520ab34b38dff0e927ed46a546dbe5d318da0dc133e58330d0e368"),
    "concepts.jsonl": (286, 89861, "59258c4a1656d5caa4665755178a9336c6a5d3f63dd4c8643a34eec44f11d024"),
    "corrections.jsonl": (280, 272419, "e734dac689fc07a47bbcc2999430a90ee8d8b93e4995db5b49a930f460e0eb86"),
    "qa.jsonl": (94, 53524, "9cf2edfb4c738b5d7a2adfecd0b596529a181ca99e713eb3e0d9cd09c8b667b2"),
    "relations.jsonl": (261, 104751, "cf3fec76fcd3a0a4cd235dd173f95ca1fb4e17f7890c1d10a0d08d6a01ef0d04"),
    "rights.jsonl": (51, 46017, "d4650781f3f8b84dd8867d85bccec03f5216521989af89c7fc1db631d4fa6dde"),
    "segments.jsonl": (783, 924450, "dd04335b3bf58e572028cc90b1d8c78eae8c230d3c1a7c85913149e165b814d6"),
    "terms.jsonl": (279, 169425, "7afdf5384d61dadc4f9617578a4a26e66234773b45281e3ace71abdb04b409dd"),
    "units.jsonl": (803, 986808, "b0e16b8879173da18f1cd28e2c3d27752387cf81d61a35dce8c4049d42c6d37a"),
}
APPEND_COUNTS = {
    "artifacts.jsonl": 4, "assets.jsonl": 1, "authority.jsonl": 0,
    "concepts.jsonl": 3, "corrections.jsonl": 8, "qa.jsonl": 3,
    "relations.jsonl": 17, "rights.jsonl": 3, "segments.jsonl": 47,
    "terms.jsonl": 3, "units.jsonl": 48,
}
FINAL = {
    "artifacts.jsonl": (100, 78379, "f52ad11802bb22255344b1a01b35378a69f6d4eb26cfae3e1abe4890082a85bd"),
    "assets.jsonl": (23, 14215, "623f8d7948504405fb8f57379987136e5f89297f0152f3eb9408cab6a3ed153c"),
    "authority.jsonl": (4, 2721, "f21af26912520ab34b38dff0e927ed46a546dbe5d318da0dc133e58330d0e368"),
    "concepts.jsonl": (289, 90816, "b05d4ec9646338ea76991eb08d5a260a087699a76d51fde507b0c5583b5921bb"),
    "corrections.jsonl": (288, 280684, "7c06a04c7072051d28879297291d37bccca70c132339c8226e889701dc1de835"),
    "qa.jsonl": (97, 55033, "621ec0d75a3307b8acec242220c0fc39c06a4c978c89378405b4f9661f569c79"),
    "relations.jsonl": (278, 111666, "a262f8db2f816e7a1155b5749e1b18199bb1d62b7e232e9e8ee9ba365e3dbc3d"),
    "rights.jsonl": (54, 48609, "f217f667ddb845de00ce819f6facefdef0247305968d209d4b2422cdb25108b0"),
    "segments.jsonl": (830, 982695, "e3fc479798493bad011f36e302cd4da7b0daa48f45252d7095dc10adc50b3530"),
    "terms.jsonl": (282, 171661, "f6bb58da10c5970087c4ff2074b25163a3a3bd6e0f820f9df0782a4e00490deb"),
    "units.jsonl": (851, 1050067, "7851c5a529337802a6eb62f7aa51d107c38e18ecf8299fcfc86d6dc5b87c46a6"),
}
SOURCE_SHA = "47fa3994dc59370fc464e9d150d62512a4602a3cffa5996f1027f93a427e0eec"
QA_SHA = "8f3f11a101ea09c0321989594a4a505ba44f92b8bde732d9c493d3de66a423ca"
BUNDLE_SHA = "84920281207fc4088aa4f1f812d78333fd530e9f157eeebaa3b09cbfb53b431d"
ROOT = "unit:o012-rbt-u021"
CUMULATIVE_RIGHTS = "rights:o012-units-001-021-composite-cc-by-4.0"

def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()

def canon(obj: dict[str, Any]) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8") + b"\n"

def load_generic():
    path = LANE / "scripts/validate-backend.py"
    spec = importlib.util.spec_from_file_location("o012_generic_validator", path)
    if spec is None or spec.loader is None:
        raise SystemExit("cannot load generic backend validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def main() -> int:
    records: list[dict[str, Any]] = []
    by_file: dict[str, list[dict[str, Any]]] = {}
    raw_by_file: dict[str, bytes] = {}
    suffix_ids: dict[str, list[str]] = {}
    for name in FILES:
        raw = (BACKEND / name).read_bytes()
        raw_by_file[name] = raw
        final_count, final_bytes, final_sha = FINAL[name]
        if len(raw) != final_bytes or digest(raw) != final_sha:
            raise SystemExit(f"{name}: final identity mismatch")
        lines = raw.splitlines(keepends=True)
        if len(lines) != final_count or b"\r" in raw or not raw.endswith(b"\n"):
            raise SystemExit(f"{name}: count/newline mismatch")
        prefix_count, prefix_bytes, prefix_sha = PREFIX[name]
        prefix = b"".join(lines[:prefix_count])
        if len(prefix) != prefix_bytes or digest(prefix) != prefix_sha:
            raise SystemExit(f"{name}: immutable Units 001-020 prefix mismatch")
        suffix = lines[prefix_count:]
        if len(suffix) != APPEND_COUNTS[name]:
            raise SystemExit(f"{name}: Unit 21 append count mismatch")
        parsed: list[dict[str, Any]] = []
        for number, line in enumerate(lines, 1):
            obj = json.loads(line.decode("utf-8"))
            if not isinstance(obj.get("id"), str) or canon(obj) != line:
                raise SystemExit(f"{name}:{number}: noncanonical record")
            parsed.append(obj)
        ids = [obj["id"] for obj in parsed]
        if len(ids) != len(set(ids)):
            raise SystemExit(f"{name}: duplicate IDs")
        appended = ids[prefix_count:]
        if appended != sorted(appended):
            raise SystemExit(f"{name}: Unit 21 suffix is not sorted")
        suffix_ids[name] = appended
        by_file[name] = parsed
        records.extend(parsed)
    by_id: dict[str, dict[str, Any]] = {}
    for obj in records:
        if obj["id"] in by_id:
            raise SystemExit(f"duplicate global ID: {obj['id']}")
        by_id[obj["id"]] = obj
    generic = load_generic()
    generic.validate_shapes(records)
    generic.validate_references(records, by_id)
    generic.validate_artifact_manifests(records, LANE)

    source = SOURCE.read_bytes()
    if len(source) != 26237 or len(source.splitlines()) != 786 or digest(source) != SOURCE_SHA:
        raise SystemExit("Unit 21 source identity mismatch")
    qa_raw = QA_JSON.read_bytes()
    if len(qa_raw) != 3967 or digest(qa_raw) != QA_SHA:
        raise SystemExit("Unit 21 QA JSON identity mismatch")
    qa = json.loads(qa_raw.decode("utf-8"))
    if (qa.get("status") != "PASS"
            or qa.get("source", {}).get("span_sha256")
            != "281ba27f0f52f35fd9842954c223546e84ce1a0909ee84c14b2081c38c11f150"
            or qa.get("unit", {}).get("sha256") != SOURCE_SHA
            or qa.get("unit", {}).get("stable_ids") != 47):
        raise SystemExit("Unit 21 QA content/binding mismatch")
    raw_lines = source.splitlines(keepends=True)
    unit_records = [
        obj for obj in by_file["units.jsonl"]
        if obj.get("id") == ROOT or (obj.get("source_local_id") or "").startswith("o012-rbt-l21")
    ]
    segment_records = [
        obj for obj in by_file["segments.jsonl"]
        if (obj.get("source_local_id") or "").startswith("o012-rbt-l21")
    ]
    if len(unit_records) != 48 or len(segment_records) != 47:
        raise SystemExit("Unit 21 unit/segment count mismatch")
    unit_by_local = {
        obj["source_local_id"]: obj for obj in unit_records
        if obj.get("source_local_id") is not None
    }
    segment_by_local = {obj["source_local_id"]: obj for obj in segment_records}
    if set(unit_by_local) != set(segment_by_local) or len(unit_by_local) != 47:
        raise SystemExit("Unit 21 stable-ID unit/segment bijection mismatch")
    for local_id, unit in unit_by_local.items():
        segment = segment_by_local[local_id]
        if unit["target_locator"] != segment["target_locator"]:
            raise SystemExit(f"target locator mismatch: {local_id}")
        locator = unit["target_locator"]
        start, end = locator["line_start"], locator["line_end"]
        if (locator["path"] != "source/id-ID/units/unit-021-lecture-021.md"
                or locator["file_sha256"] != SOURCE_SHA
                or not (1 <= start <= end <= 786)
                or locator["content_sha256"] != digest(b"".join(raw_lines[start - 1:end]))):
            raise SystemExit(f"invalid target locator: {local_id}")
        if local_id not in raw_lines[start - 1].decode("utf-8"):
            raise SystemExit(f"anchor absent at locator start: {local_id}")
        if unit["path"][-1] != unit["id"]:
            raise SystemExit(f"path tail mismatch: {local_id}")
        parent_id = unit["parent_id"]
        if parent_id.startswith("unit:"):
            parent = by_id[parent_id]
            if unit["path"][:-1] != parent["path"]:
                raise SystemExit(f"path does not extend parent: {local_id}")
    root = by_id[ROOT]
    root_locator = root["target_locator"]
    if (root_locator["file_sha256"] != SOURCE_SHA
            or root_locator["line_start"] != 1 or root_locator["line_end"] != 786
            or root_locator["content_sha256"] != digest(source)):
        raise SystemExit("Unit 21 root locator mismatch")
    siblings: defaultdict[str, list[int]] = defaultdict(list)
    for unit in unit_records:
        siblings[unit["parent_id"]].append(unit["order"])
    if any(len(items) != len(set(items)) for items in siblings.values()):
        raise SystemExit("Unit 21 sibling order collision")

    relations = by_file["relations.jsonl"]
    for number in range(1, 7):
        check = f"unit:o012-rbt-l21-mcheck-{number:03d}"
        solution = f"unit:o012-rbt-l21-sol-{number:03d}"
        hint = f"unit:o012-rbt-l21-hint-{number:03d}"
        solves = [obj for obj in relations
                  if obj.get("relation_type") == "solves" and obj.get("to_id") == check]
        hints = [obj for obj in relations
                 if obj.get("relation_type") == "hints" and obj.get("to_id") == check]
        if len(solves) != 1 or solves[0]["from_id"] != solution:
            raise SystemExit(f"Unit 21 solution closure mismatch: {number}")
        if len(hints) != 1 or hints[0]["from_id"] != hint:
            raise SystemExit(f"Unit 21 hint closure mismatch: {number}")

    with TERMINOLOGY.open(encoding="utf-8", newline="") as stream:
        controls = {row["term_id"]: row for row in csv.DictReader(stream)}
    terms = {
        obj.get("terminology_control_id"): obj for obj in by_file["terms.jsonl"]
        if obj.get("terminology_control_id") in {
            "O012-TERM-0290", "O012-TERM-0291", "O012-TERM-0292"}
    }
    if set(terms) != {"O012-TERM-0290", "O012-TERM-0291", "O012-TERM-0292"}:
        raise SystemExit("Unit 21 terminology backend closure mismatch")
    for control, term in terms.items():
        if (controls[control]["status"] != "admitted"
                or term["source_term"] != controls[control]["source_term"]
                or term["preferred"] != controls[control]["id_ID"]):
            raise SystemExit(f"Unit 21 terminology mismatch: {control}")

    with LEDGER.open(encoding="utf-8", newline="") as stream:
        adverse = {row["event_id"]: row for row in csv.DictReader(stream)}
    corrections = {
        obj.get("adverse_ledger_id"): obj for obj in by_file["corrections.jsonl"]
        if obj.get("unit_id") == ROOT
    }
    expected_events = {f"O012-ADV-{number:04d}" for number in range(290, 298)}
    if set(corrections) != expected_events:
        raise SystemExit("Unit 21 adverse backend closure mismatch")
    for event in expected_events:
        if (event not in adverse or corrections[event]["source_defect"] != adverse[event]["observed"]
                or corrections[event]["target_change"] != adverse[event]["action"]
                or corrections[event]["upstream_report_disposition"] != "not_contacted"):
            raise SystemExit(f"Unit 21 adverse mismatch: {event}")
    expected_scope = [f"unit:o012-rbt-u{number:03d}" for number in range(1, 22)]
    if by_id[CUMULATIVE_RIGHTS]["component_scope"] != expected_scope:
        raise SystemExit("Unit 21 cumulative rights scope mismatch")

    evidence = {
        "artifact:o012-u021-independent-review": (
            "qa/UNIT_021_INDEPENDENT_REVIEW.md", 2678,
            "44975beb96e04717fc92a9f2743a5fc73997f1d7139c75285743766fecfa9bfb"),
        "artifact:o012-u021-source-audit": (
            "qa/UNIT_021_SOURCE_AUDIT.md", 3331,
            "38ba068dcf96a58dd76e951b8250cec33798e6aac744244fb1cf0e6db18ea650"),
        "artifact:o012-u021-qa": (
            "qa/UNIT_021_QA.json", 3967, QA_SHA),
        "artifact:o012-u021-translation-handoff": (
            "qa/UNIT_021_TRANSLATION_HANDOFF.md", 1935,
            "9fa065b56a70abec8c54112515cf3425407a8bb32823c40f1d745a7705e5d466"),
    }
    for ident, (relative, size, expected_sha) in evidence.items():
        raw = (LANE / relative).read_bytes()
        record = by_id.get(ident)
        if (len(raw) != size or digest(raw) != expected_sha or not record
                or record["bytes"] != size or record["sha256"] != expected_sha):
            raise SystemExit(f"Unit 21 evidence mismatch: {ident}")
    for qa_id in ("qa:o012-u021-source-integrity", "qa:o012-u021-math",
                  "qa:o012-u021-language"):
        if by_id.get(qa_id, {}).get("result") != "passed":
            raise SystemExit(f"Unit 21 QA event not passed: {qa_id}")

    bundle = hashlib.sha256()
    for name in FILES:
        bundle.update(name.encode()); bundle.update(b"\0"); bundle.update(raw_by_file[name])
    if bundle.hexdigest() != BUNDLE_SHA:
        raise SystemExit("Unit 21 backend bundle mismatch")
    output = {
        "status": "PASS", "total_records": len(records),
        "backend_bytes": sum(len(raw) for raw in raw_by_file.values()),
        "backend_bundle_sha256": bundle.hexdigest(),
        "source_sha256": SOURCE_SHA, "source_bytes": len(source),
        "source_lines": len(source.splitlines()), "stable_ids": 47,
        "new_records": sum(APPEND_COUNTS.values()),
        "records": {name: len(by_file[name]) for name in FILES},
        "per_file_sha256": {name: digest(raw_by_file[name]) for name in FILES},
    }
    print(json.dumps(output, ensure_ascii=False, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
