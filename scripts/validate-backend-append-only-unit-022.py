#!/usr/bin/env python3
"""Independent fail-closed validator for Unit 022 append-only admission."""
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
SOURCE = LANE / "source/id-ID/units/unit-022-lecture-022.md"
QA_JSON = LANE / "qa/UNIT_022_QA.json"
TERMINOLOGY = LANE / "00_control/TERMINOLOGY.csv"
LEDGER = LANE / "00_control/ADVERSE_LEDGER.csv"
FILES = ("artifacts.jsonl", "assets.jsonl", "authority.jsonl", "concepts.jsonl",
         "corrections.jsonl", "qa.jsonl", "relations.jsonl", "rights.jsonl",
         "segments.jsonl", "terms.jsonl", "units.jsonl")
PREFIX = {
    "artifacts.jsonl": (106, 83103, "1708f7276cb28e295d578c8e4411618291c7294c8faee863c89461c63378a978"),
    "assets.jsonl": (23, 14215, "623f8d7948504405fb8f57379987136e5f89297f0152f3eb9408cab6a3ed153c"),
    "authority.jsonl": (4, 2721, "f21af26912520ab34b38dff0e927ed46a546dbe5d318da0dc133e58330d0e368"),
    "concepts.jsonl": (289, 90816, "b05d4ec9646338ea76991eb08d5a260a087699a76d51fde507b0c5583b5921bb"),
    "corrections.jsonl": (288, 280684, "7c06a04c7072051d28879297291d37bccca70c132339c8226e889701dc1de835"),
    "qa.jsonl": (99, 56340, "249c2f6110269d1daef7fff472e4fb17c2f7060b8cd39f662884fd8bba0f0145"),
    "relations.jsonl": (284, 114295, "3a1b930dbe14992819fcaeca39edb96e915641e62247a2e7ea879809a998c2e9"),
    "rights.jsonl": (55, 49832, "1dca76e63699015d393009a8ed263ea4f1adb4e9be3a9668aae8e19bdcf55524"),
    "segments.jsonl": (830, 982695, "e3fc479798493bad011f36e302cd4da7b0daa48f45252d7095dc10adc50b3530"),
    "terms.jsonl": (282, 171661, "f6bb58da10c5970087c4ff2074b25163a3a3bd6e0f820f9df0782a4e00490deb"),
    "units.jsonl": (851, 1050067, "7851c5a529337802a6eb62f7aa51d107c38e18ecf8299fcfc86d6dc5b87c46a6"),
}
APPEND_COUNTS = {
    "artifacts.jsonl": 4, "assets.jsonl": 1, "authority.jsonl": 0,
    "concepts.jsonl": 8, "corrections.jsonl": 14, "qa.jsonl": 3,
    "relations.jsonl": 19, "rights.jsonl": 3, "segments.jsonl": 75,
    "terms.jsonl": 8, "units.jsonl": 76,
}
FINAL = {
    "artifacts.jsonl": (110, 86473, "5d16598495a6df0a0855f6c413cc78def50cf653d30c6699bcef5b5455cb72ea"),
    "assets.jsonl": (24, 14831, "69020caaf45628941c57ee5cf58f3c11a31505c3416ec9d65c9ac82b47ba97aa"),
    "authority.jsonl": (4, 2721, "f21af26912520ab34b38dff0e927ed46a546dbe5d318da0dc133e58330d0e368"),
    "concepts.jsonl": (297, 93358, "2e8f93bfa8b7622960716b8a6bd33811c630c877696c5cbf031cb14eadfa110b"),
    "corrections.jsonl": (302, 295241, "718a14732930b546a3c38bf2e131d23066b2f90f09d4dd80a781294296f5cbc6"),
    "qa.jsonl": (102, 57849, "86591e4710dcf61a1cc29c1ad94187b5d4bd362f4df8d9e7d63ac14bbb88dfaf"),
    "relations.jsonl": (303, 122094, "8c28ab28cfbe752f32c95746355dde648fa7b005d0f1d4550c3933e1d804fa28"),
    "rights.jsonl": (58, 52476, "2aaf92fd5c0853ddaea495ca7e3a20caba6de445193d9f5888e38523bc359434"),
    "segments.jsonl": (905, 1094552, "491b68e826f0221353d7a7782515be769fc8048e468bba5937c797ca0390bb8c"),
    "terms.jsonl": (290, 177339, "bf1c79fc4bbaf0a9bd71545f4d69d9dc36dcb728f23710ad33a9bf9791421695"),
    "units.jsonl": (927, 1169478, "56fdf925d6e547b4a936d4ac7fb483cdbd9d845ac292989a7162efae108fcf8f"),
}
SOURCE_SHA = "0857e51568d77c811d5d79255ac75bfddc87a04b27356ae457d4e66eeffb7d0d"
QA_SHA = "4b9e62ca0912eb3cd989130a643fc07b9634ffa421f989d92ec3d8676eea8fe7"
BUNDLE_SHA = "2329606117578210ce927123ec01639390f2e493fcc995899606eaa38996f2bc"
PREFIX_BUNDLE = "cf5acacf3ad2351869297dd8d3827787377422fa30c8c1385e60833b23913db9"
ROOT = "unit:o012-rbt-u022"
CUMULATIVE_RIGHTS = "rights:o012-units-001-022-composite-cc-by-4.0"
COMPANION_RIGHTS = "rights:o012-u022-companion-cc-by-4.0"
EXPECTED_TERM_IDS = {f"O012-TERM-{number:04d}" for number in range(293, 301)}
EXPECTED_ADVERSE_IDS = {f"O012-ADV-{number:04d}" for number in range(298, 312)}
EXPECTED_ARTIFACTS = {
    "artifact:o012-u022-independent-review": (
        "qa/UNIT_022_INDEPENDENT_REVIEW.md", 2893,
        "6632c22c2aa9339c169382111c0c28750e91a61bbb7ed40d47fe4734cefc7004"),
    "artifact:o012-u022-source-audit": (
        "qa/UNIT_022_SOURCE_AUDIT.md", 4519,
        "50e0c9268f19c1fc3d6a9f865b6c338940e0edb1c336386566030a7595695801"),
    "artifact:o012-u022-qa": (
        "qa/UNIT_022_QA.json", 4167, QA_SHA),
    "artifact:o012-u022-translation-handoff": (
        "qa/UNIT_022_TRANSLATION_HANDOFF.md", 2045,
        "9804d4372f4dc80c963bd6dca86ab5f8e79c6959f334526adc4f02e92507ccbf"),
}


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canon(obj: dict[str, Any]) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8") + b"\n"


def load_generic():
    path = LANE / "scripts/validate-backend.py"
    spec = importlib.util.spec_from_file_location("o012_generic_validator_u022", path)
    if spec is None or spec.loader is None:
        raise SystemExit("cannot load generic backend validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def source_ids(text: str) -> list[str]:
    pattern = re.compile(
        r"(?m)^(?:#{1,6} .*?\{[^}]*#|:::\s+\{[^#}]*#)"
        r"(o012-rbt-l22(?:-[A-Za-z0-9-]+)?)[^}]*\}\s*$")
    return pattern.findall(text)


def main() -> int:
    records: list[dict[str, Any]] = []
    by_file: dict[str, list[dict[str, Any]]] = {}
    raw_by_file: dict[str, bytes] = {}
    suffix_ids: dict[str, list[str]] = {}
    prefix_bundle = hashlib.sha256()
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
            raise SystemExit(f"{name}: immutable Units 001-021 prefix mismatch")
        prefix_bundle.update(name.encode()); prefix_bundle.update(b"\0"); prefix_bundle.update(prefix)
        suffix = lines[prefix_count:]
        if len(suffix) != APPEND_COUNTS[name]:
            raise SystemExit(f"{name}: Unit 22 append count mismatch")
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
            raise SystemExit(f"{name}: Unit 22 suffix is not sorted")
        suffix_ids[name] = appended
        by_file[name] = parsed
        records.extend(parsed)
    if prefix_bundle.hexdigest() != PREFIX_BUNDLE:
        raise SystemExit("immutable prefix bundle mismatch")

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
    if len(source) != 44066 or len(source.splitlines()) != 1349 or digest(source) != SOURCE_SHA:
        raise SystemExit("Unit 22 source identity mismatch")
    text = source.decode("utf-8")
    ids = source_ids(text)
    if len(ids) != 75 or len(set(ids)) != 75:
        raise SystemExit("Unit 22 source stable-ID inventory mismatch")
    if digest(("\n".join(ids) + "\n").encode()) != (
            "0d184ad4d848e50b4e8f73f8f44e314f0fe2a3dd1a2ec3f31476f730fea31099"):
        raise SystemExit("Unit 22 source stable-ID order mismatch")
    if text.count('data-source-label="eg:infinite_cylinder"') != 1 or text.count(
            'data-source-label="eg:name_of_simplex"') != 1:
        raise SystemExit("Unit 22 source-label preservation mismatch")

    qa_raw = QA_JSON.read_bytes()
    if len(qa_raw) != 4167 or digest(qa_raw) != QA_SHA:
        raise SystemExit("Unit 22 QA JSON identity mismatch")
    qa = json.loads(qa_raw.decode("utf-8"))
    if (qa.get("status") != "PASS"
            or qa.get("source", {}).get("line_start") != 4501
            or qa.get("source", {}).get("line_end") != 4938
            or qa.get("source", {}).get("span_bytes") != 20585
            or qa.get("source", {}).get("span_sha256") !=
            "86275c590cfcdf8519d3ce8d077fc48619bb94c3fdf039ca805ae4b7df995b7f"
            or qa.get("unit", {}).get("sha256") != SOURCE_SHA
            or qa.get("unit", {}).get("stable_ids") != 75
            or qa.get("model_provenance") != "OpenAI Codex gpt-5.6-sol, Ultra"):
        raise SystemExit("Unit 22 QA content/binding mismatch")

    raw_lines = source.splitlines(keepends=True)
    unit_records = [obj for obj in by_file["units.jsonl"]
                    if obj.get("id") == ROOT or
                    (obj.get("source_local_id") or "").startswith("o012-rbt-l22")]
    segment_records = [obj for obj in by_file["segments.jsonl"]
                       if (obj.get("source_local_id") or "").startswith("o012-rbt-l22")]
    if len(unit_records) != 76 or len(segment_records) != 75:
        raise SystemExit("Unit 22 unit/segment count mismatch")
    unit_by_local = {obj["source_local_id"]: obj for obj in unit_records
                     if obj.get("source_local_id") is not None}
    segment_by_local = {obj["source_local_id"]: obj for obj in segment_records}
    if set(unit_by_local) != set(ids) or set(segment_by_local) != set(ids):
        raise SystemExit("Unit 22 stable-ID unit/segment bijection mismatch")
    for local_id in ids:
        unit = unit_by_local[local_id]
        segment = segment_by_local[local_id]
        if unit["target_locator"] != segment["target_locator"]:
            raise SystemExit(f"target locator mismatch: {local_id}")
        locator = unit["target_locator"]
        start, end = locator["line_start"], locator["line_end"]
        if (locator["path"] != "source/id-ID/units/unit-022-lecture-022.md"
                or locator["file_sha256"] != SOURCE_SHA
                or not (1 <= start <= end <= 1349)
                or locator["content_sha256"] != digest(b"".join(raw_lines[start - 1:end]))
                or local_id not in raw_lines[start - 1].decode("utf-8")):
            raise SystemExit(f"invalid target locator: {local_id}")
        if unit["path"][-1] != unit["id"]:
            raise SystemExit(f"path tail mismatch: {local_id}")
        parent_id = unit["parent_id"]
        if parent_id.startswith("unit:") and unit["path"][:-1] != by_id[parent_id]["path"]:
            raise SystemExit(f"path does not extend parent: {local_id}")
    root_locator = by_id[ROOT]["target_locator"]
    if (root_locator["file_sha256"] != SOURCE_SHA or root_locator["line_start"] != 1
            or root_locator["line_end"] != 1349 or root_locator["content_sha256"] != digest(source)):
        raise SystemExit("Unit 22 root locator mismatch")
    siblings: defaultdict[str, list[int]] = defaultdict(list)
    for unit in unit_records:
        siblings[unit["parent_id"]].append(unit["order"])
    if any(len(items) != len(set(items)) for items in siblings.values()):
        raise SystemExit("Unit 22 sibling order collision")

    relations = by_file["relations.jsonl"]
    for number in range(1, 7):
        check = f"unit:o012-rbt-l22-mcheck-{number:03d}"
        solution = f"unit:o012-rbt-l22-sol-{number:03d}"
        hint = f"unit:o012-rbt-l22-hint-{number:03d}"
        solves = [obj for obj in relations if obj.get("relation_type") == "solves"
                  and obj.get("to_id") == check]
        hints = [obj for obj in relations if obj.get("relation_type") == "hints"
                 and obj.get("to_id") == check]
        if len(solves) != 1 or solves[0]["from_id"] != solution:
            raise SystemExit(f"Unit 22 solution closure mismatch: {number}")
        if len(hints) != 1 or hints[0]["from_id"] != hint:
            raise SystemExit(f"Unit 22 hint closure mismatch: {number}")
    proves = [obj for obj in relations if obj.get("id") ==
              "relation:proves:o012-rbt-l22-proof-002:lem-003"]
    if (len(proves) != 1 or proves[0]["from_id"] != "unit:o012-rbt-l22-proof-002"
            or proves[0]["to_id"] != "unit:o012-rbt-l22-lem-003"
            or by_id["unit:o012-rbt-l22-proof-002"]["rights_component_id"] != COMPANION_RIGHTS
            or by_id["segment:o012-rbt-l22-proof-002"]["source_locator"].get("kind") !=
            "edition_original"):
        raise SystemExit("Unit 22 source-omission proof closure mismatch")

    with TERMINOLOGY.open(encoding="utf-8", newline="") as stream:
        controls = {row["term_id"]: row for row in csv.DictReader(stream)}
    terms = {obj.get("terminology_control_id"): obj for obj in by_file["terms.jsonl"]
             if obj.get("terminology_control_id") in EXPECTED_TERM_IDS}
    if set(terms) != EXPECTED_TERM_IDS:
        raise SystemExit("Unit 22 terminology backend closure mismatch")
    for control, term in terms.items():
        if (controls[control]["status"] != "admitted"
                or term["source_term"] != controls[control]["source_term"]
                or term["preferred"] != controls[control]["id_ID"]
                or term["evidence_segment_id"] not in by_id):
            raise SystemExit(f"Unit 22 terminology mismatch: {control}")

    with LEDGER.open(encoding="utf-8", newline="") as stream:
        adverse = {row["event_id"]: row for row in csv.DictReader(stream)}
    corrections = {obj.get("adverse_ledger_id"): obj
                   for obj in by_file["corrections.jsonl"] if obj.get("unit_id") == ROOT}
    if set(corrections) != EXPECTED_ADVERSE_IDS:
        raise SystemExit("Unit 22 adverse backend closure mismatch")
    for event in EXPECTED_ADVERSE_IDS:
        if (event not in adverse or corrections[event]["source_defect"] != adverse[event]["observed"]
                or corrections[event]["target_change"] != adverse[event]["action"]
                or corrections[event]["upstream_report_disposition"] != "not_contacted"):
            raise SystemExit(f"Unit 22 adverse mismatch: {event}")

    expected_scope = [f"unit:o012-rbt-u{number:03d}" for number in range(1, 23)]
    right = by_id[CUMULATIVE_RIGHTS]
    if (right["component_scope"] != expected_scope
            or right["supersedes"] !=
            "rights:o012-units-001-021-composite-cc-by-4.0-final-47fa"):
        raise SystemExit("Unit 22 cumulative rights mismatch")
    for ident, (relative, size, expected_sha) in EXPECTED_ARTIFACTS.items():
        artifact_raw = (LANE / relative).read_bytes()
        record = by_id.get(ident)
        if (len(artifact_raw) != size or digest(artifact_raw) != expected_sha or not record
                or record["bytes"] != size or record["sha256"] != expected_sha
                or "OpenAI Codex gpt-5.6-sol, Ultra" not in record["toolchain"]):
            raise SystemExit(f"Unit 22 evidence mismatch: {ident}")
    if set(suffix_ids["artifacts.jsonl"]) != set(EXPECTED_ARTIFACTS):
        raise SystemExit("Unit 22 suffix contains an unapproved/build artifact")
    for qa_id in ("qa:o012-u022-source-integrity", "qa:o012-u022-math",
                  "qa:o012-u022-language"):
        if by_id.get(qa_id, {}).get("result") != "passed":
            raise SystemExit(f"Unit 22 QA event not passed: {qa_id}")

    bundle = hashlib.sha256()
    for name in FILES:
        bundle.update(name.encode()); bundle.update(b"\0"); bundle.update(raw_by_file[name])
    if bundle.hexdigest() != BUNDLE_SHA:
        raise SystemExit("Unit 22 backend bundle mismatch")
    output = {
        "status": "PASS", "prefix_records": 3111, "prefix_bytes": 2896429,
        "prefix_bundle_sha256": PREFIX_BUNDLE, "prefix_preserved_byte_for_byte": True,
        "new_records": sum(APPEND_COUNTS.values()), "total_records": len(records),
        "backend_bytes": sum(len(raw) for raw in raw_by_file.values()),
        "backend_bundle_sha256": bundle.hexdigest(), "source_sha256": SOURCE_SHA,
        "source_bytes": len(source), "source_lines": len(source.splitlines()),
        "stable_ids": 75, "records_added_by_file": APPEND_COUNTS,
        "records": {name: len(by_file[name]) for name in FILES},
        "per_file_bytes": {name: len(raw_by_file[name]) for name in FILES},
        "per_file_sha256": {name: digest(raw_by_file[name]) for name in FILES},
        "cumulative_build_artifacts_added": 0,
    }
    print(json.dumps(output, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
