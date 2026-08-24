#!/usr/bin/env python3
"""Independent fail-closed validator for Unit 024 semantic admission."""
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
SOURCE = LANE / "source/id-ID/units/unit-024-lecture-024.md"
UPSTREAM = (LANE / "authority/upstream" /
            "AlgebraicTopology2019-b947ad2e9f9e301bfe24590a9db653bc54fa1a53" /
            "Notes.tex")
QA_JSON = LANE / "qa/UNIT_024_QA.json"
TERMINOLOGY = LANE / "00_control/TERMINOLOGY.csv"
LEDGER = LANE / "00_control/ADVERSE_LEDGER.csv"
FILES = ("artifacts.jsonl", "assets.jsonl", "authority.jsonl", "concepts.jsonl",
         "corrections.jsonl", "qa.jsonl", "relations.jsonl", "rights.jsonl",
         "segments.jsonl", "terms.jsonl", "units.jsonl")
PREFIX = {
    "artifacts.jsonl": (125, 98770, "f8f4fc8b686554ce528bffe4ca31533d8f416ad34d9ed16b8f23b5b6d981c13c"),
    "assets.jsonl": (25, 15447, "752dfa957041664a1b3f32acdcf996511164d5c17ba6aa34619a100651dad3b1"),
    "authority.jsonl": (4, 2721, "f21af26912520ab34b38dff0e927ed46a546dbe5d318da0dc133e58330d0e368"),
    "concepts.jsonl": (312, 98079, "6fadff806dab54588f4984dd44ec745152841dbf44416ea881d9414f6b535830"),
    "corrections.jsonl": (313, 306801, "a0545c84efadc062f181356f9fa508b0da5f9077f52702da0750e3165c0b6244"),
    "qa.jsonl": (109, 61880, "3c8c741c0c50b56cd0d15b7616c3ebd3006fe368382cc14e7c50ee743eebb974"),
    "relations.jsonl": (337, 136702, "07f7ec67c251eb180f211b09da33ec165129c45646d1b08014de2f3e68b2882c"),
    "rights.jsonl": (63, 57648, "f39bd50ab5e33d7d3b0ae9063b2ed0adc9fc3986a8a034de4311876c3e810157"),
    "segments.jsonl": (956, 1193838, "1851199865ae823a7f155f1a33590290cafccb0f1cafe37d429fb7072a2d84c0"),
    "terms.jsonl": (305, 188007, "16ac428e76df5de2a97f475c9a80c7e63278bc57a15720047785e4ad217e82a9"),
    "units.jsonl": (979, 1274986, "e66891050013b595dbe972bee0d7ba3b88689a8a6a06a2c2885919194df036c9"),
}
APPEND_COUNTS = {
    "artifacts.jsonl": 3, "assets.jsonl": 1, "authority.jsonl": 0,
    "concepts.jsonl": 7, "corrections.jsonl": 9, "qa.jsonl": 3,
    "relations.jsonl": 24, "rights.jsonl": 3, "segments.jsonl": 60,
    "terms.jsonl": 7, "units.jsonl": 61,
}
FINAL = {
    "artifacts.jsonl": (128, 101337, "4bff9b72daf44201c97a7e3c3896e43d0174e79d040b0b88b9d4e31b828139c3"),
    "assets.jsonl": (26, 16063, "60d4f100505e27b28bc0642c8849dbc1842926d971642f2210c3a392e3f73eb4"),
    "authority.jsonl": (4, 2721, "f21af26912520ab34b38dff0e927ed46a546dbe5d318da0dc133e58330d0e368"),
    "concepts.jsonl": (319, 100311, "342c1cabc894a64d766dee238ded0a923ef655930421ddfe4d5fcf7f4569c17f"),
    "corrections.jsonl": (322, 316453, "acb12d317419c4df9f43e3743daa4001bf2a99a70c8ca4f55388401a211a488b"),
    "qa.jsonl": (112, 63331, "0c7af567ccfe67c0db7611f889511c8ede1730e3da339d04388ca87b835c9349"),
    "relations.jsonl": (361, 146819, "393554493bb45b01fe93045639ad8f6cf0ca65fc324adf87e3219d71a824985e"),
    "rights.jsonl": (66, 60332, "328bf2f3c0e1504d59150ef25af16e8e9de68a71e5f7eda9fcf2e154c3a5cd77"),
    "segments.jsonl": (1016, 1313231, "09210c2eaee49c9937ba555f1b18b26332c14297adbd70bcd17830b5ac75e620"),
    "terms.jsonl": (312, 193238, "68e6b19d70650fae488bf4ab7676dbc8e3d9efb1fb1b46de10a0169caafb1665"),
    "units.jsonl": (1040, 1401068, "ca605764e55f79126ac83d3313dd2d7a72626f4b3906573c7bc51ca9a3f1b95d"),
}
PREFIX_RECORDS = 3528
PREFIX_BYTES = 3434879
PREFIX_BUNDLE = "0c8b27890f8423fc3224c89f2bcf60ed6cbcb9d93fabef7b53c399784f0aaaef"
FINAL_BUNDLE = "b0a182615e96995b6afa9ad0d8b25f221b9ad6fb58feca01b284b08211db1066"
SOURCE_PATH = "source/id-ID/units/unit-024-lecture-024.md"
SOURCE_BYTES = 43085
SOURCE_LINES = 1156
SOURCE_SHA = "993ad0c3493caff6bd15ab2bcf435f6cbb1f49ed9a1e11bc1009d649ae2d3647"
ANCHOR_ORDER_SHA = "c38e06f24bba82aae0b16a4f75a4e87c6b7836038e08536a7e3d055982b0548a"
UPSTREAM_SHA = "cfe93e9dbe3e25bd96f711f59e6078ab97527682b58e1f8ad127f74357f665d7"
UPSTREAM_SPAN_SHA = "b2128930a56a0a8c04c327a397e72e21b215ffe742bb684e8dd166f0e04b0aea"
ROOT = "unit:o012-rbt-u024"
ROUTE = "D60-R13"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"
COMPANION_RIGHTS = "rights:o012-u024-companion-cc-by-4.0"
COMPOSITE_RIGHTS = "rights:o012-u024-composite-cc-by-4.0"
CUMULATIVE_RIGHTS = "rights:o012-units-001-024-composite-cc-by-4.0"
PRIOR_RIGHTS = "rights:o012-units-001-023-composite-cc-by-4.0-final-6f05"
EXPECTED_TERM_IDS = {f"O012-TERM-{number:04d}" for number in range(316, 323)}
EXPECTED_ADVERSE_IDS = {f"O012-ADV-{number:04d}" for number in range(323, 332)}
QA_BYTES = 6556
QA_SHA = "dad49400f3f19367cbcab119fcdeb95e6365e5995f2403c32881ddc35bfaff99"
FIXED_ARTIFACTS = {
    "artifact:o012-u024-independent-review": (
        "qa/UNIT_024_INDEPENDENT_REVIEW.md", 5570,
        "d06dc4a2d76eabbb8f4c115fd8f311c81e974415a186f8bff8269d30cb1672b2"),
    "artifact:o012-u024-source-audit": (
        "qa/UNIT_024_SOURCE_AUDIT.md", 4384,
        "0aeb3beae1b52099e97538083ef349590cca62b473ff1455b8c1fdaffbe2ba6b"),
    "artifact:o012-u024-qa": (
        "qa/UNIT_024_QA.json", QA_BYTES, QA_SHA),
}
EXPECTED_ALIASES = {
    "o012-rbt-l24-thm-001": ["thm:alg_Mayer-Vietoris"],
    "o012-rbt-l24-lem-002": ["snakeLemma"],
    "o012-rbt-l24-fig-002": ["fig:snake_lemma"],
    "o012-rbt-l24-lem-003": ["lemma:setup_for_algMV"],
}


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canon(obj: dict[str, Any]) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8") + b"\n"


def load_generic():
    path = LANE / "scripts/validate-backend.py"
    spec = importlib.util.spec_from_file_location("o012_generic_u024_validator", path)
    if spec is None or spec.loader is None:
        raise SystemExit("cannot load generic backend validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def source_ids(text: str) -> list[str]:
    pattern = re.compile(
        r"(?m)^(?:#{1,6} .*?\{[^}]*#|\s*:::\s+\{[^#}]*#)"
        r"(o012-rbt-l24(?:-[A-Za-z0-9-]+)?)[^}]*\}\s*$")
    return pattern.findall(text)


def main() -> int:
    records: list[dict[str, Any]] = []
    by_file: dict[str, list[dict[str, Any]]] = {}
    raw_by_file: dict[str, bytes] = {}
    suffix_ids: dict[str, list[str]] = {}
    prefix_bundle = hashlib.sha256()
    for name in FILES:
        raw = (BACKEND / name).read_bytes(); raw_by_file[name] = raw
        final_count, final_bytes, final_sha = FINAL[name]
        lines = raw.splitlines(keepends=True)
        if (len(raw), len(lines), digest(raw)) != (final_bytes, final_count, final_sha):
            raise SystemExit(f"{name}: final identity mismatch")
        if b"\r" in raw or not raw.endswith(b"\n"):
            raise SystemExit(f"{name}: count/newline mismatch")
        prefix_count, prefix_bytes, prefix_sha = PREFIX[name]
        prefix = b"".join(lines[:prefix_count])
        if len(prefix) != prefix_bytes or digest(prefix) != prefix_sha:
            raise SystemExit(f"{name}: immutable Units 001-023 prefix mismatch")
        prefix_bundle.update(name.encode()); prefix_bundle.update(b"\0"); prefix_bundle.update(prefix)
        suffix = lines[prefix_count:]
        if len(suffix) != APPEND_COUNTS[name]:
            raise SystemExit(f"{name}: Unit 24 append count mismatch")
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
            raise SystemExit(f"{name}: Unit 24 suffix is not sorted")
        suffix_ids[name] = appended; by_file[name] = parsed; records.extend(parsed)
    if (prefix_bundle.hexdigest() != PREFIX_BUNDLE
            or sum(APPEND_COUNTS.values()) != 178
            or sum(item[0] for item in PREFIX.values()) != PREFIX_RECORDS
            or sum(item[1] for item in PREFIX.values()) != PREFIX_BYTES):
        raise SystemExit("immutable prefix/count constants mismatch")

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
            or digest(source) != SOURCE_SHA or b"\r" in source
            or not source.endswith(b"\n")):
        raise SystemExit("Unit 24 source identity mismatch")
    text = source.decode("utf-8")
    ids = source_ids(text)
    if (len(ids) != 60 or len(set(ids)) != 60
            or digest(("\n".join(ids) + "\n").encode()) != ANCHOR_ORDER_SHA
            or text.count(MODEL) != 1):
        raise SystemExit("Unit 24 source stable-ID/model inventory mismatch")

    upstream = UPSTREAM.read_bytes()
    if len(upstream) != 331447 or digest(upstream) != UPSTREAM_SHA:
        raise SystemExit("frozen Notes.tex identity mismatch")
    upstream_text = upstream.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")
    lines = upstream_text.split("\n")
    span = ("\n".join(lines[5112:5369]) + "\n").encode()
    if (len(span) != 12837 or digest(span) != UPSTREAM_SPAN_SHA
            or "\\lecturenum{24}" not in lines[5112]
            or lines[5120].strip() != "\\end{example}"
            or "\\lecturenum{25}" not in lines[5369]):
        raise SystemExit("Unit 24 upstream boundary/span mismatch")

    qa_raw = QA_JSON.read_bytes()
    if len(qa_raw) != QA_BYTES or digest(qa_raw) != QA_SHA:
        raise SystemExit("Unit 24 QA JSON identity mismatch")
    qa = json.loads(qa_raw.decode("utf-8"))
    if (qa.get("status") != "PASS"
            or qa.get("source", {}).get("line_start") != 5113
            or qa.get("source", {}).get("line_end") != 5369
            or qa.get("source", {}).get("span_bytes") != 12837
            or qa.get("source", {}).get("span_sha256") != UPSTREAM_SPAN_SHA
            or qa.get("source", {}).get("next_line") != 5370
            or qa.get("unit", {}).get("sha256") != SOURCE_SHA
            or qa.get("unit", {}).get("stable_ids") != 60
            or qa.get("unit", {}).get("fenced_semantic_objects") != 50
            or qa.get("proof_closure", {}).get("mastery_solution_triples") != 6
            or qa.get("model_provenance") != MODEL
            or any(item.get("status") != "PASS" for item in qa.get("checks", []))):
        raise SystemExit("Unit 24 QA content/binding mismatch")

    raw_lines = source.splitlines(keepends=True)
    unit_records = [obj for obj in by_file["units.jsonl"]
                    if obj.get("id") == ROOT or
                    (obj.get("source_local_id") or "").startswith("o012-rbt-l24")]
    segment_records = [obj for obj in by_file["segments.jsonl"]
                       if (obj.get("source_local_id") or "").startswith("o012-rbt-l24")]
    if len(unit_records) != 61 or len(segment_records) != 60:
        raise SystemExit("Unit 24 unit/segment count mismatch")
    unit_by_local = {obj["source_local_id"]: obj for obj in unit_records
                     if obj.get("source_local_id") is not None}
    segment_by_local = {obj["source_local_id"]: obj for obj in segment_records}
    if set(unit_by_local) != set(ids) or set(segment_by_local) != set(ids):
        raise SystemExit("Unit 24 stable-ID unit/segment bijection mismatch")
    for local_id in ids:
        unit = unit_by_local[local_id]; segment = segment_by_local[local_id]
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
        if (unit["parent_id"].startswith("unit:")
                and unit["path"][:-1] != by_id[unit["parent_id"]]["path"]):
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
            or by_id[ROOT].get("course_route_unit_id") != ROUTE
            or by_id[ROOT].get("order") != 24):
        raise SystemExit("Unit 24 root locator/route/order mismatch")
    siblings: defaultdict[str, list[int]] = defaultdict(list)
    for unit in unit_records:
        siblings[unit["parent_id"]].append(unit["order"])
    if any(len(items) != len(set(items)) for items in siblings.values()):
        raise SystemExit("Unit 24 sibling order collision")
    root_orders = [obj["order"] for obj in by_file["units.jsonl"]
                   if obj.get("parent_id") == "course:o012-d60"
                   and obj.get("id", "").startswith("unit:o012-rbt-u")]
    if len(root_orders) != len(set(root_orders)) or 24 not in root_orders:
        raise SystemExit("course-level edition unit order collision")

    for local_id, aliases in EXPECTED_ALIASES.items():
        if (unit_by_local[local_id].get("source_aliases") != aliases
                or segment_by_local[local_id].get("source_aliases") != aliases):
            raise SystemExit(f"Unit 24 source alias mismatch: {local_id}")
    unexpected_aliases = {ident for ident, obj in unit_by_local.items()
                          if obj.get("source_aliases") and ident not in EXPECTED_ALIASES}
    if unexpected_aliases:
        raise SystemExit(f"unexpected Unit 24 source aliases: {sorted(unexpected_aliases)}")

    relations = by_file["relations.jsonl"]
    for number in range(1, 7):
        check = f"unit:o012-rbt-l24-mcheck-{number:03d}"
        solution = f"unit:o012-rbt-l24-sol-{number:03d}"
        hint = f"unit:o012-rbt-l24-hint-{number:03d}"
        solves = [obj for obj in relations if obj.get("relation_type") == "solves"
                  and obj.get("to_id") == check]
        hints = [obj for obj in relations if obj.get("relation_type") == "hints"
                 and obj.get("to_id") == check]
        if len(solves) != 1 or solves[0]["from_id"] != solution:
            raise SystemExit(f"Unit 24 solution closure mismatch: {number}")
        if len(hints) != 1 or hints[0]["from_id"] != hint:
            raise SystemExit(f"Unit 24 hint closure mismatch: {number}")
    proofs = [obj for obj in unit_records
              if obj.get("proof_status") == "complete_original_proof"]
    proves = [obj for obj in relations
              if obj.get("id", "").startswith("relation:proves:o012-rbt-l24-proof-")]
    if (len(proofs) != 6 or len(proves) != 6
            or any(obj["rights_component_id"] != COMPANION_RIGHTS for obj in proofs)):
        raise SystemExit("Unit 24 proof closure mismatch")

    continued = by_id["unit:o012-rbt-l24-exa-001"]
    continued_segment = by_id["segment:o012-rbt-l24-exa-001"]
    closure_relation = by_id.get(
        "relation:xref:o012-rbt-l24-exa-001:u023-continuation", {})
    prior_relation = by_id.get(
        "relation:xref:o012-rbt-l23-exa-002:u024-continuation", {})
    for obj in (continued, continued_segment, closure_relation):
        if (obj.get("source_environment_state") != "closed_in_this_unit"
                or obj.get("continuation_from_edition_unit_id") != "unit:o012-rbt-u023"
                or obj.get("continuation_source_line_start") != 5113
                or obj.get("continuation_source_line_end") != 5121):
            raise SystemExit("Unit 23/24 continuation closure metadata mismatch")
    if (closure_relation.get("to_id") != "unit:o012-rbt-l23-exa-002"
            or prior_relation.get("continuation_target_edition_unit_id") != ROOT
            or prior_relation.get("source_environment_state") != "open_at_unit_boundary"
            or by_id["unit:o012-rbt-l24-boundary-001"].get("next_source_line") != 5370):
        raise SystemExit("Unit 23 open pointer / Unit 24 close / next cursor mismatch")
    route_relation = by_id.get("relation:route:d60-r13:o012-rbt-u024", {})
    if (route_relation.get("course_route_unit_id") != ROUTE
            or route_relation.get("edition_unit_id") != ROOT):
        raise SystemExit("D60-R13 Unit 24 route binding mismatch")

    with TERMINOLOGY.open(encoding="utf-8", newline="") as stream:
        controls = {row["term_id"]: row for row in csv.DictReader(stream)}
    terms = {obj.get("terminology_control_id"): obj for obj in by_file["terms.jsonl"]
             if obj.get("terminology_control_id") in EXPECTED_TERM_IDS}
    if set(terms) != EXPECTED_TERM_IDS:
        raise SystemExit("Unit 24 terminology backend closure mismatch")
    for control, term in terms.items():
        if (controls.get(control, {}).get("status") != "admitted"
                or term["source_term"] != controls[control]["source_term"]
                or term["preferred"] != controls[control]["id_ID"]
                or term["evidence_segment_id"] not in by_id
                or term["scope_unit_id"] != ROOT):
            raise SystemExit(f"Unit 24 terminology mismatch: {control}")

    with LEDGER.open(encoding="utf-8", newline="") as stream:
        adverse = {row["event_id"]: row for row in csv.DictReader(stream)}
    corrections = {obj.get("adverse_ledger_id"): obj
                   for obj in by_file["corrections.jsonl"] if obj.get("unit_id") == ROOT}
    if set(corrections) != EXPECTED_ADVERSE_IDS:
        raise SystemExit("Unit 24 adverse backend closure mismatch")
    expected_types = {
        "O012-ADV-0323": "proof_completion", "O012-ADV-0324": "proof_completion",
        "O012-ADV-0325": "mathematical_correction",
        "O012-ADV-0326": "mathematical_correction",
        "O012-ADV-0327": "proof_completion", "O012-ADV-0328": "proof_completion",
        "O012-ADV-0329": "proof_completion", "O012-ADV-0330": "clarification",
        "O012-ADV-0331": "structural_adaptation",
    }
    for event, correction in corrections.items():
        if (event not in adverse
                or correction["source_defect"] != adverse[event]["observed"]
                or correction["target_change"] != adverse[event]["action"]
                or correction["correction_type"] != expected_types[event]
                or correction["upstream_report_disposition"] != "not_contacted"
                or any(target not in by_id for target in correction["affected_unit_ids"])):
            raise SystemExit(f"Unit 24 adverse mismatch: {event}")

    right = by_id[CUMULATIVE_RIGHTS]
    if (right["component_scope"] != [
            f"unit:o012-rbt-u{number:03d}" for number in range(1, 25)]
            or right["supersedes"] != PRIOR_RIGHTS
            or by_id[COMPOSITE_RIGHTS]["component_scope"] != [ROOT]
            or by_id[COMPANION_RIGHTS]["component_scope"] != [ROOT]):
        raise SystemExit("Unit 24 cumulative/component rights mismatch")

    for ident, (relative, size, expected_sha) in FIXED_ARTIFACTS.items():
        artifact_raw = (LANE / relative).read_bytes(); record = by_id.get(ident)
        if (len(artifact_raw) != size or digest(artifact_raw) != expected_sha or not record
                or record["bytes"] != size or record["sha256"] != expected_sha
                or MODEL not in record["toolchain"] or ROUTE not in record["toolchain"]
                or record["unit_id"] != ROOT or record["rights_component_id"] != COMPOSITE_RIGHTS):
            raise SystemExit(f"Unit 24 evidence mismatch: {ident}")
    if set(suffix_ids["artifacts.jsonl"]) != set(FIXED_ARTIFACTS):
        raise SystemExit("Unit 24 suffix contains an unapproved/build artifact")
    if suffix_ids["assets.jsonl"] != ["asset:o012-u024-source-markdown"]:
        raise SystemExit("Unit 24 asset suffix mismatch")
    for qa_id in ("qa:o012-u024-source-integrity", "qa:o012-u024-math",
                  "qa:o012-u024-language"):
        if by_id.get(qa_id, {}).get("result") != "passed":
            raise SystemExit(f"Unit 24 QA event not passed: {qa_id}")

    bundle = hashlib.sha256()
    for name in FILES:
        bundle.update(name.encode()); bundle.update(b"\0"); bundle.update(raw_by_file[name])
    if bundle.hexdigest() != FINAL_BUNDLE:
        raise SystemExit("Unit 24 backend bundle mismatch")
    output = {
        "status": "PASS", "prefix_records": PREFIX_RECORDS,
        "prefix_bytes": PREFIX_BYTES, "prefix_bundle_sha256": PREFIX_BUNDLE,
        "prefix_preserved_byte_for_byte": True,
        "new_records": sum(APPEND_COUNTS.values()), "total_records": len(records),
        "backend_bytes": sum(len(raw) for raw in raw_by_file.values()),
        "backend_bundle_sha256": bundle.hexdigest(), "source_sha256": SOURCE_SHA,
        "source_bytes": len(source), "source_lines": len(source.splitlines()),
        "stable_ids": 60, "fenced_semantic_objects": 50,
        "proof_closures": 6, "mastery_triples": 6,
        "course_route_unit_id": ROUTE, "records_added_by_file": APPEND_COUNTS,
        "records": {name: len(by_file[name]) for name in FILES},
        "per_file_bytes": {name: len(raw_by_file[name]) for name in FILES},
        "per_file_sha256": {name: digest(raw_by_file[name]) for name in FILES},
        "qa_bytes": QA_BYTES, "qa_sha256": QA_SHA,
        "terminology_controls": sorted(EXPECTED_TERM_IDS),
        "adverse_controls": sorted(EXPECTED_ADVERSE_IDS),
        "continuation_closed": True, "next_source_line": 5370,
        "cumulative_build_artifacts_added": 0,
    }
    print(json.dumps(output, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
