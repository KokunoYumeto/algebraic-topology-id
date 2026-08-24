#!/usr/bin/env python3
"""Independent fail-closed validator for Unit 023 append-only admission.

FINAL and QA identity constants are deliberately filled only after the
producer's single authorized transaction.  Until then this validator refuses
to certify any state.
"""
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
SOURCE = LANE / "source/id-ID/units/unit-023-lecture-023.md"
UPSTREAM = (LANE / "authority/upstream" /
            "AlgebraicTopology2019-b947ad2e9f9e301bfe24590a9db653bc54fa1a53" /
            "Notes.tex")
QA_JSON = LANE / "qa/UNIT_023_QA.json"
TERMINOLOGY = LANE / "00_control/TERMINOLOGY.csv"
LEDGER = LANE / "00_control/ADVERSE_LEDGER.csv"
FILES = ("artifacts.jsonl", "assets.jsonl", "authority.jsonl", "concepts.jsonl",
         "corrections.jsonl", "qa.jsonl", "relations.jsonl", "rights.jsonl",
         "segments.jsonl", "terms.jsonl", "units.jsonl")
PREFIX = {
    "artifacts.jsonl": (116, 91395, "05a9525a470df9a106ad785a026b45f8913c1dfc40d363eff12df5cea3d0a58e"),
    "assets.jsonl": (24, 14831, "69020caaf45628941c57ee5cf58f3c11a31505c3416ec9d65c9ac82b47ba97aa"),
    "authority.jsonl": (4, 2721, "f21af26912520ab34b38dff0e927ed46a546dbe5d318da0dc133e58330d0e368"),
    "concepts.jsonl": (297, 93358, "2e8f93bfa8b7622960716b8a6bd33811c630c877696c5cbf031cb14eadfa110b"),
    "corrections.jsonl": (302, 295241, "718a14732930b546a3c38bf2e131d23066b2f90f09d4dd80a781294296f5cbc6"),
    "qa.jsonl": (104, 59176, "b8c439539b4bd566bb3b46423e19ab925f2cbcb8075a77b5df6a76ba7b9cf516"),
    "relations.jsonl": (309, 124723, "2d58a794206f07915c18c98c220e143354429c57d14bc93f27eb1806a2277ab6"),
    "rights.jsonl": (59, 53720, "f734f3649cc4e8a40ec7d63bd92843c1d04cf835d46f9fcef9224168a9142bd2"),
    "segments.jsonl": (905, 1094552, "491b68e826f0221353d7a7782515be769fc8048e468bba5937c797ca0390bb8c"),
    "terms.jsonl": (290, 177339, "bf1c79fc4bbaf0a9bd71545f4d69d9dc36dcb728f23710ad33a9bf9791421695"),
    "units.jsonl": (927, 1169478, "56fdf925d6e547b4a936d4ac7fb483cdbd9d845ac292989a7162efae108fcf8f"),
}
APPEND_COUNTS = {
    "artifacts.jsonl": 3, "assets.jsonl": 1, "authority.jsonl": 0,
    "concepts.jsonl": 15, "corrections.jsonl": 11, "qa.jsonl": 3,
    "relations.jsonl": 22, "rights.jsonl": 3, "segments.jsonl": 51,
    "terms.jsonl": 15, "units.jsonl": 52,
}
FINAL: dict[str, tuple[int, int, str]] = {
    "artifacts.jsonl": (119, 93962, "a439fbb383c0082b68f9ebee1ec988b92f910e595992bbe23a97c1844ab0c9a9"),
    "assets.jsonl": (25, 15447, "752dfa957041664a1b3f32acdcf996511164d5c17ba6aa34619a100651dad3b1"),
    "authority.jsonl": (4, 2721, "f21af26912520ab34b38dff0e927ed46a546dbe5d318da0dc133e58330d0e368"),
    "concepts.jsonl": (312, 98079, "6fadff806dab54588f4984dd44ec745152841dbf44416ea881d9414f6b535830"),
    "corrections.jsonl": (313, 306801, "a0545c84efadc062f181356f9fa508b0da5f9077f52702da0750e3165c0b6244"),
    "qa.jsonl": (107, 60615, "6c6a5c890596eb883daf5b30ddb3ed1ffc287fa91aca6eaa45312225a75e0a13"),
    "relations.jsonl": (331, 134073, "d85e492b275093cb807fa2ca407bca56c0ec758c1f5e7df2f2f0babc4baf8a30"),
    "rights.jsonl": (62, 56383, "b3d975821a277ec640297ce75cb44e2c6dd18383eff876361b1952a51449b7ff"),
    "segments.jsonl": (956, 1193838, "1851199865ae823a7f155f1a33590290cafccb0f1cafe37d429fb7072a2d84c0"),
    "terms.jsonl": (305, 188007, "16ac428e76df5de2a97f475c9a80c7e63278bc57a15720047785e4ad217e82a9"),
    "units.jsonl": (979, 1274986, "e66891050013b595dbe972bee0d7ba3b88689a8a6a06a2c2885919194df036c9"),
}
FINAL_BUNDLE = "2b31536824cea66fc186bd653354eea4eea45f9c68da7992a45d037c782672dc"
QA_BYTES = 6412
QA_SHA = "f4a156b709158e9a6312d0fe604b7ab7c60a70d7f7c6fb1423014df4d49f820b"

PREFIX_RECORDS = 3337
PREFIX_BYTES = 3176534
PREFIX_BUNDLE = "38b98ca6258133036ded9e3cb72894f4181d4b6faa46af9e96a2128ab25c9df2"
SOURCE_PATH = "source/id-ID/units/unit-023-lecture-023.md"
SOURCE_BYTES = 39176
SOURCE_LINES = 1094
SOURCE_SHA = "6f05ddbe6a720109797976c6929b0535f21a38353673cb42d9646a3196f56bd2"
ANCHOR_ORDER_SHA = "77b2e8f91fe5bd7f4c76c83120b7619fa3b07d6dd59f934bcd55d458b98f5fc1"
UPSTREAM_SHA = "cfe93e9dbe3e25bd96f711f59e6078ab97527682b58e1f8ad127f74357f665d7"
UPSTREAM_SPAN_SHA = "c7256a45621ad7a435277867298e4aeb8eb584dfce066cdae3b48c4ee0e0e3f4"
UPSTREAM_THROUGH_CLOSE_SHA = "b9b54862d6c462344ecdf0da9b9633f52b5ff185722c08444fb7022863b79dc3"
ROOT = "unit:o012-rbt-u023"
ROUTE = "D60-R13"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"
COMPANION_RIGHTS = "rights:o012-u023-companion-cc-by-4.0"
CUMULATIVE_RIGHTS = "rights:o012-units-001-023-composite-cc-by-4.0"
EXPECTED_TERM_IDS = {f"O012-TERM-{number:04d}" for number in range(301, 316)}
EXPECTED_ADVERSE_IDS = {f"O012-ADV-{number:04d}" for number in range(312, 323)}
FIXED_ARTIFACTS = {
    "artifact:o012-u023-independent-review": (
        "qa/UNIT_023_INDEPENDENT_REVIEW.md", 3149,
        "dce8f82872186285c85a42b61b1bbf8fb9fd8e809eea5bccd6367dc87958c880"),
    "artifact:o012-u023-source-audit": (
        "qa/UNIT_023_SOURCE_AUDIT.md", 5254,
        "4777f7c14d35e5fb977955818ff7ab133ecc91adb3575867f0e97f8ff00d28b3"),
}


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canon(obj: dict[str, Any]) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8") + b"\n"


def load_generic():
    path = LANE / "scripts/validate-backend.py"
    spec = importlib.util.spec_from_file_location("o012_generic_validator_u023", path)
    if spec is None or spec.loader is None:
        raise SystemExit("cannot load generic backend validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def source_ids(text: str) -> list[str]:
    pattern = re.compile(
        r"(?m)^(?:#{1,6} .*?\{[^}]*#|\s*:::\s+\{[^#}]*#)"
        r"(o012-rbt-l23(?:-[A-Za-z0-9-]+)?)[^}]*\}\s*$")
    return pattern.findall(text)


def main() -> int:
    if set(FINAL) != set(FILES) or not re.fullmatch(r"[0-9a-f]{64}", FINAL_BUNDLE):
        raise SystemExit("validator final-identity constants have not been admitted")
    if QA_BYTES <= 0 or not re.fullmatch(r"[0-9a-f]{64}", QA_SHA):
        raise SystemExit("validator QA identity constants have not been admitted")
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
            raise SystemExit(f"{name}: immutable Units 001-022 prefix mismatch")
        prefix_bundle.update(name.encode()); prefix_bundle.update(b"\0"); prefix_bundle.update(prefix)
        suffix = lines[prefix_count:]
        if len(suffix) != APPEND_COUNTS[name]:
            raise SystemExit(f"{name}: Unit 23 append count mismatch")
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
            raise SystemExit(f"{name}: Unit 23 suffix is not sorted")
        suffix_ids[name] = appended
        by_file[name] = parsed
        records.extend(parsed)
    if prefix_bundle.hexdigest() != PREFIX_BUNDLE:
        raise SystemExit("immutable prefix bundle mismatch")
    if sum(APPEND_COUNTS.values()) != 176:
        raise SystemExit("append-count constant mismatch")

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
    if (len(source) != SOURCE_BYTES or len(source.splitlines()) != SOURCE_LINES
            or digest(source) != SOURCE_SHA or b"\r" in source or not source.endswith(b"\n")):
        raise SystemExit("Unit 23 source identity mismatch")
    ids = source_ids(source.decode("utf-8"))
    if len(ids) != 51 or len(set(ids)) != 51:
        raise SystemExit("Unit 23 source stable-ID inventory mismatch")
    if digest(("\n".join(ids) + "\n").encode()) != ANCHOR_ORDER_SHA:
        raise SystemExit("Unit 23 source stable-ID order mismatch")
    if source.decode("utf-8").count(MODEL) != 1:
        raise SystemExit("Unit 23 model provenance occurrence mismatch")

    upstream = UPSTREAM.read_bytes()
    if len(upstream) != 331447 or digest(upstream) != UPSTREAM_SHA:
        raise SystemExit("frozen Notes.tex identity mismatch")
    text = upstream.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")
    lines = text.split("\n")
    span = ("\n".join(lines[4938:5112]) + "\n").encode()
    through_close = ("\n".join(lines[4938:5121]) + "\n").encode()
    if len(span) != 9776 or digest(span) != UPSTREAM_SPAN_SHA:
        raise SystemExit("Unit 23 upstream span mismatch")
    if digest(through_close) != UPSTREAM_THROUGH_CLOSE_SHA:
        raise SystemExit("Unit 23/24 source environment witness mismatch")

    qa_raw = QA_JSON.read_bytes()
    if len(qa_raw) != QA_BYTES or digest(qa_raw) != QA_SHA:
        raise SystemExit("Unit 23 QA JSON identity mismatch")
    qa = json.loads(qa_raw.decode("utf-8"))
    if (qa.get("status") != "PASS"
            or qa.get("source", {}).get("line_start") != 4939
            or qa.get("source", {}).get("line_end") != 5112
            or qa.get("source", {}).get("span_bytes") != 9776
            or qa.get("source", {}).get("span_sha256") != UPSTREAM_SPAN_SHA
            or qa.get("unit", {}).get("sha256") != SOURCE_SHA
            or qa.get("unit", {}).get("stable_ids") != 51
            or qa.get("model_provenance") != MODEL):
        raise SystemExit("Unit 23 QA content/binding mismatch")

    raw_lines = source.splitlines(keepends=True)
    unit_records = [obj for obj in by_file["units.jsonl"]
                    if obj.get("id") == ROOT or
                    (obj.get("source_local_id") or "").startswith("o012-rbt-l23")]
    segment_records = [obj for obj in by_file["segments.jsonl"]
                       if (obj.get("source_local_id") or "").startswith("o012-rbt-l23")]
    if len(unit_records) != 52 or len(segment_records) != 51:
        raise SystemExit("Unit 23 unit/segment count mismatch")
    unit_by_local = {obj["source_local_id"]: obj for obj in unit_records
                     if obj.get("source_local_id") is not None}
    segment_by_local = {obj["source_local_id"]: obj for obj in segment_records}
    if set(unit_by_local) != set(ids) or set(segment_by_local) != set(ids):
        raise SystemExit("Unit 23 stable-ID unit/segment bijection mismatch")
    for local_id in ids:
        unit = unit_by_local[local_id]
        segment = segment_by_local[local_id]
        if unit["target_locator"] != segment["target_locator"]:
            raise SystemExit(f"target locator mismatch: {local_id}")
        locator = unit["target_locator"]
        start, end = locator["line_start"], locator["line_end"]
        if (locator["path"] != SOURCE_PATH or locator["file_sha256"] != SOURCE_SHA
                or not (1 <= start <= end <= SOURCE_LINES)
                or locator["content_sha256"] != digest(b"".join(raw_lines[start - 1:end]))
                or local_id not in raw_lines[start - 1].decode("utf-8")):
            raise SystemExit(f"invalid target locator: {local_id}")
        if unit["path"][-1] != unit["id"]:
            raise SystemExit(f"path tail mismatch: {local_id}")
        if unit["parent_id"].startswith("unit:") and unit["path"][:-1] != by_id[unit["parent_id"]]["path"]:
            raise SystemExit(f"path does not extend parent: {local_id}")
        for obj in (unit, segment):
            if (obj.get("edition_unit_id") != ROOT
                    or obj.get("course_route_unit_id") != ROUTE
                    or obj.get("model_provenance") != MODEL
                    or obj.get("component_source_commit") !=
                    "b947ad2e9f9e301bfe24590a9db653bc54fa1a53"):
                raise SystemExit(f"route/provenance mismatch: {local_id}")
    root_locator = by_id[ROOT]["target_locator"]
    if (root_locator["file_sha256"] != SOURCE_SHA or root_locator["line_start"] != 1
            or root_locator["line_end"] != SOURCE_LINES
            or root_locator["content_sha256"] != digest(source)
            or by_id[ROOT].get("edition_unit_id") != ROOT
            or by_id[ROOT].get("course_route_unit_id") != ROUTE):
        raise SystemExit("Unit 23 root locator/route mismatch")
    siblings: defaultdict[str, list[int]] = defaultdict(list)
    for unit in unit_records:
        siblings[unit["parent_id"]].append(unit["order"])
    if any(len(items) != len(set(items)) for items in siblings.values()):
        raise SystemExit("Unit 23 sibling order collision")

    relations = by_file["relations.jsonl"]
    for number in range(1, 7):
        check = f"unit:o012-rbt-l23-mcheck-{number:03d}"
        solution = f"unit:o012-rbt-l23-sol-{number:03d}"
        hint = f"unit:o012-rbt-l23-hint-{number:03d}"
        solves = [obj for obj in relations if obj.get("relation_type") == "solves"
                  and obj.get("to_id") == check]
        hints = [obj for obj in relations if obj.get("relation_type") == "hints"
                 and obj.get("to_id") == check]
        if len(solves) != 1 or solves[0]["from_id"] != solution:
            raise SystemExit(f"Unit 23 solution closure mismatch: {number}")
        if len(hints) != 1 or hints[0]["from_id"] != hint:
            raise SystemExit(f"Unit 23 hint closure mismatch: {number}")
    proofs = [obj for obj in unit_records
              if obj.get("proof_status") == "complete_original_proof"]
    proves = [obj for obj in relations
              if obj.get("id", "").startswith("relation:proves:o012-rbt-l23-proof-")]
    if (len(proofs) != 4 or len(proves) != 4
            or any(obj["rights_component_id"] != COMPANION_RIGHTS for obj in proofs)):
        raise SystemExit("Unit 23 proof closure mismatch")
    continuation = by_id["unit:o012-rbt-l23-exa-002"]
    boundary = by_id["unit:o012-rbt-l23-boundary-001"]
    route_relation = by_id.get("relation:route:d60-r13:o012-rbt-u023", {})
    continuation_relation = by_id.get(
        "relation:xref:o012-rbt-l23-exa-002:u024-continuation", {})
    for obj in (continuation, boundary, continuation_relation):
        if (obj.get("source_environment_state") != "open_at_unit_boundary"
                or obj.get("continuation_target_edition_unit_id") != "unit:o012-rbt-u024"
                or obj.get("continuation_source_line_start") != 5113
                or obj.get("continuation_source_line_end") != 5121):
            raise SystemExit("Unit 23/24 continuation metadata mismatch")
    if (route_relation.get("course_route_unit_id") != ROUTE
            or route_relation.get("edition_unit_id") != ROOT):
        raise SystemExit("D60-R13 route binding mismatch")

    with TERMINOLOGY.open(encoding="utf-8", newline="") as stream:
        controls = {row["term_id"]: row for row in csv.DictReader(stream)}
    terms = {obj.get("terminology_control_id"): obj for obj in by_file["terms.jsonl"]
             if obj.get("terminology_control_id") in EXPECTED_TERM_IDS}
    if set(terms) != EXPECTED_TERM_IDS:
        raise SystemExit("Unit 23 terminology backend closure mismatch")
    for control, term in terms.items():
        if (controls[control]["status"] != "admitted"
                or term["source_term"] != controls[control]["source_term"]
                or term["preferred"] != controls[control]["id_ID"]
                or term["evidence_segment_id"] not in by_id):
            raise SystemExit(f"Unit 23 terminology mismatch: {control}")

    with LEDGER.open(encoding="utf-8", newline="") as stream:
        adverse = {row["event_id"]: row for row in csv.DictReader(stream)}
    corrections = {obj.get("adverse_ledger_id"): obj
                   for obj in by_file["corrections.jsonl"] if obj.get("unit_id") == ROOT}
    if set(corrections) != EXPECTED_ADVERSE_IDS:
        raise SystemExit("Unit 23 adverse backend closure mismatch")
    for event in EXPECTED_ADVERSE_IDS:
        if (event not in adverse or corrections[event]["source_defect"] != adverse[event]["observed"]
                or corrections[event]["target_change"] != adverse[event]["action"]
                or corrections[event]["upstream_report_disposition"] != "not_contacted"):
            raise SystemExit(f"Unit 23 adverse mismatch: {event}")

    right = by_id[CUMULATIVE_RIGHTS]
    expected_scope = [f"unit:o012-rbt-u{number:03d}" for number in range(1, 24)]
    if (right["component_scope"] != expected_scope
            or right["supersedes"] !=
            "rights:o012-units-001-022-composite-cc-by-4.0-final-0857"):
        raise SystemExit("Unit 23 cumulative rights mismatch")
    expected_artifacts = dict(FIXED_ARTIFACTS)
    expected_artifacts["artifact:o012-u023-qa"] = (
        "qa/UNIT_023_QA.json", QA_BYTES, QA_SHA)
    for ident, (relative, size, expected_sha) in expected_artifacts.items():
        artifact_raw = (LANE / relative).read_bytes()
        record = by_id.get(ident)
        if (len(artifact_raw) != size or digest(artifact_raw) != expected_sha or not record
                or record["bytes"] != size or record["sha256"] != expected_sha
                or MODEL not in record["toolchain"] or ROUTE not in record["toolchain"]):
            raise SystemExit(f"Unit 23 evidence mismatch: {ident}")
    if set(suffix_ids["artifacts.jsonl"]) != set(expected_artifacts):
        raise SystemExit("Unit 23 suffix contains an unapproved/build artifact")
    for qa_id in ("qa:o012-u023-source-integrity", "qa:o012-u023-math",
                  "qa:o012-u023-language"):
        if by_id.get(qa_id, {}).get("result") != "passed":
            raise SystemExit(f"Unit 23 QA event not passed: {qa_id}")

    bundle = hashlib.sha256()
    for name in FILES:
        bundle.update(name.encode()); bundle.update(b"\0"); bundle.update(raw_by_file[name])
    if bundle.hexdigest() != FINAL_BUNDLE:
        raise SystemExit("Unit 23 backend bundle mismatch")
    output = {
        "status": "PASS", "prefix_records": PREFIX_RECORDS,
        "prefix_bytes": PREFIX_BYTES, "prefix_bundle_sha256": PREFIX_BUNDLE,
        "prefix_preserved_byte_for_byte": True,
        "new_records": sum(APPEND_COUNTS.values()), "total_records": len(records),
        "backend_bytes": sum(len(raw) for raw in raw_by_file.values()),
        "backend_bundle_sha256": bundle.hexdigest(), "source_sha256": SOURCE_SHA,
        "source_bytes": len(source), "source_lines": len(source.splitlines()),
        "stable_ids": 51, "proof_closures": 4, "mastery_triples": 6,
        "course_route_unit_id": ROUTE, "records_added_by_file": APPEND_COUNTS,
        "records": {name: len(by_file[name]) for name in FILES},
        "per_file_bytes": {name: len(raw_by_file[name]) for name in FILES},
        "per_file_sha256": {name: digest(raw_by_file[name]) for name in FILES},
        "qa_bytes": QA_BYTES, "qa_sha256": QA_SHA,
        "cumulative_build_artifacts_added": 0,
    }
    print(json.dumps(output, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
