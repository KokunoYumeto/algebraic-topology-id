#!/usr/bin/env python3
"""Independent fail-closed validator for the Unit 026 semantic append.

This validator does not import the Unit 26 producer.  It proves the complete
Units 001--025 cumulative byte prefix, the exact per-file Unit 26 suffix, the
frozen evidence, and semantic, rights, provenance, proof, solution, alias,
dependency, and cursor closure on the live backend.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

LANE = Path(__file__).resolve().parents[1]
BACKEND = LANE / "backend"
SOURCE = LANE / "source/id-ID/units/unit-026-lecture-026.md"
UPSTREAM = (LANE / "authority/upstream" /
            "AlgebraicTopology2019-b947ad2e9f9e301bfe24590a9db653bc54fa1a53" /
            "Notes.tex")
FILES = ("artifacts.jsonl", "assets.jsonl", "authority.jsonl", "concepts.jsonl",
         "corrections.jsonl", "qa.jsonl", "relations.jsonl", "rights.jsonl",
         "segments.jsonl", "terms.jsonl", "units.jsonl")
PREFIX = {
    "artifacts.jsonl": (145, 115514, "ac0633eb616f2d0bd412bfb076a482d6ef6a402683d35da67bf6c1ed290ea40e"),
    "assets.jsonl": (27, 16679, "aa569a900426a9e2cfd56777f3e52f07b35a1a72f211847bafd71ec638043462"),
    "authority.jsonl": (4, 2721, "f21af26912520ab34b38dff0e927ed46a546dbe5d318da0dc133e58330d0e368"),
    "concepts.jsonl": (325, 102250, "0ce28594cd511c1a20aff74053b7c74c6c4c6a0505c7c8c5804dd7acd2dae77d"),
    "corrections.jsonl": (332, 327054, "40791f1db8da9ba81083bad0bb4ac183094c3151b9007bb34e5fc637a1790893"),
    "qa.jsonl": (119, 67471, "7b90c07af1561b6356a3249f396a97aaf10265989f4d7ba2b1493f87bac60b93"),
    "relations.jsonl": (397, 162048, "62f67c2ede76bcd24e9ad87db7968dd92649aba6e284c4829042941dd7ea8a50"),
    "rights.jsonl": (71, 65630, "7e54a0f51dd951aecadbc3767173308dc02c12ada6c121b9703c9ec2fb7f2ac7"),
    "segments.jsonl": (1075, 1428116, "d47404ea94dfa7347fbf6f6e0e0e8c5f4fb60e2634c066b87967a4468fff644a"),
    "terms.jsonl": (318, 197648, "dda9013d863bc39ec81f9936167ad24d0cfa2ebba6de0aa2c768743dc09b8503"),
    "units.jsonl": (1100, 1522772, "7fe9d4abfae9389db7cb99240b553d62b66144086c3f2097e9f64d5b2fe14318"),
}
PREFIX_TOTAL = (3913, 4007903,
                "8b50629f25c5fcbedb6d5547f8f7151c622aa90e04f71583008bd176058a4f78")
DELTA = {"artifacts.jsonl": 3, "assets.jsonl": 1, "authority.jsonl": 0,
         "concepts.jsonl": 8, "corrections.jsonl": 13, "qa.jsonl": 3,
         "relations.jsonl": 28, "rights.jsonl": 3, "segments.jsonl": 62,
         "terms.jsonl": 8, "units.jsonl": 63}
FINAL = {
    "artifacts.jsonl": (148, 118081, "75ca44ea07393c83d2cf57f50d8c8db7944921099f8ab43f64efbc166d714e0d"),
    "assets.jsonl": (28, 17295, "7f8953ab04264df0c9ee63db7e277f2b7e9e126fcb5514fcb3ad6eb142d72a68"),
    "authority.jsonl": (4, 2721, "f21af26912520ab34b38dff0e927ed46a546dbe5d318da0dc133e58330d0e368"),
    "concepts.jsonl": (333, 104854, "645061fd18b6ff32c1d9c773508259e97ca0b2fd8cbf1ec8fc22403e82b43acc"),
    "corrections.jsonl": (345, 339810, "9ddf73f800001c6f1c5f6b1e5a0fe2e1f33483101ea8855c106370976cbdba0b"),
    "qa.jsonl": (122, 68974, "177448acf95ac6a0988825fccf5b8d25288720b92f3234982acfb59e97915efb"),
    "relations.jsonl": (425, 173541, "fe2485035d5b488adede6d1926f334c3f41a7d57f36af2315e1bf64249a79b1b"),
    "rights.jsonl": (74, 68380, "47db4fd8e4d817368d00cf732de25b44163dead640b84292628f2a164a6ebfae"),
    "segments.jsonl": (1137, 1553154, "8ef04b73e87221da393f3dacdb5600c62dc3bd6dfe379f648b9498e795a69529"),
    "terms.jsonl": (326, 203570, "61f88694434a122038ce7f26fd1adef4c3ec4f145bf0f88466ba1b3ab1e62f8b"),
    "units.jsonl": (1163, 1654838, "df7a5ad97b5e6ea3551b8bb353e8a93620061e3c7219e656d0b5c3484d233fbf"),
}
FINAL_TOTAL = (4105, 4305218,
               "89556c5fa2224820837fc8956b1a48797929f28bef013baf9a613e73e6cf28eb")
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"
COMMIT = "b947ad2e9f9e301bfe24590a9db653bc54fa1a53"
SOURCE_PATH = "source/id-ID/units/unit-026-lecture-026.md"
SOURCE_IDENTITY = (38537, 1201,
                   "7a2cf4ea31546b8258e3e91c819d3ad516973c8f861249fccc7334b9ade9d835")
UPSTREAM_IDENTITY = (331447, 6368,
                     "cfe93e9dbe3e25bd96f711f59e6078ab97527682b58e1f8ad127f74357f665d7")
SPAN_IDENTITY = (5612, 5823, 9763,
                 "52663b3e60d5d6f3041b8ede449c52a04700ee670c201ef5674c4aa3973203a9")
ROOT = "unit:o012-rbt-u026"
ROUTE = "D60-R13"
COMPANION_RIGHTS = "rights:o012-u026-companion-cc-by-4.0"
COMPOSITE_RIGHTS = "rights:o012-u026-composite-cc-by-4.0"
CUMULATIVE_RIGHTS = "rights:o012-units-001-026-composite-cc-by-4.0"
PRIOR_RIGHTS = "rights:o012-units-001-025-composite-cc-by-4.0-final-df72"

ANCHORS = (
    "o012-rbt-l26-notice", "o012-rbt-l26", "o012-rbt-l26-s01",
    "o012-rbt-l26-aside-001", "o012-rbt-l26-audit-001",
    "o012-rbt-l26-s02", "o012-rbt-l26-def-001", "o012-rbt-l26-prop-001",
    "o012-rbt-l26-proof-001", "o012-rbt-l26-audit-002",
    "o012-rbt-l26-exa-001", "o012-rbt-l26-aside-002",
    "o012-rbt-l26-s03", "o012-rbt-l26-def-002", "o012-rbt-l26-prop-002",
    "o012-rbt-l26-proof-002", "o012-rbt-l26-rem-001",
    "o012-rbt-l26-audit-003", "o012-rbt-l26-exa-002",
    "o012-rbt-l26-prop-003", "o012-rbt-l26-proof-003",
    "o012-rbt-l26-aside-003", "o012-rbt-l26-s04",
    "o012-rbt-l26-prop-004", "o012-rbt-l26-proof-004",
    "o012-rbt-l26-audit-004", "o012-rbt-l26-s05", "o012-rbt-l26-thm-001",
    "o012-rbt-l26-cor-001", "o012-rbt-l26-proof-005",
    "o012-rbt-l26-cor-002", "o012-rbt-l26-proof-006",
    "o012-rbt-l26-audit-005", "o012-rbt-l26-cor-003",
    "o012-rbt-l26-proof-007", "o012-rbt-l26-def-003",
    "o012-rbt-l26-lem-001", "o012-rbt-l26-proof-008",
    "o012-rbt-l26-audit-006", "o012-rbt-l26-thm-002",
    "o012-rbt-l26-proof-009", "o012-rbt-l26-audit-007",
    "o012-rbt-l26-mastery", "o012-rbt-l26-mcheck-001",
    "o012-rbt-l26-hint-001", "o012-rbt-l26-sol-001",
    "o012-rbt-l26-mcheck-002", "o012-rbt-l26-hint-002",
    "o012-rbt-l26-sol-002", "o012-rbt-l26-mcheck-003",
    "o012-rbt-l26-hint-003", "o012-rbt-l26-sol-003",
    "o012-rbt-l26-mcheck-004", "o012-rbt-l26-hint-004",
    "o012-rbt-l26-sol-004", "o012-rbt-l26-mcheck-005",
    "o012-rbt-l26-hint-005", "o012-rbt-l26-sol-005",
    "o012-rbt-l26-mcheck-006", "o012-rbt-l26-hint-006",
    "o012-rbt-l26-sol-006", "o012-rbt-l26-boundary-001",
)
SLUGS = {"singular-simplex", "singular-cochain-complex",
         "singular-cohomology", "relative-singular-cochain-complex",
         "cochain-homotopy", "prism-operator",
         "finite-coproduct-cohomology", "stokes-theorem"}
CORRECTION_IDS = {f"correction:o012-u026-dossier-{n:03d}" for n in range(1, 13)} | {
    "correction:o012-u026-resolved-term-001"}


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canon(obj: dict[str, Any]) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8") + b"\n"


def generic_module():
    path = LANE / "scripts/validate-backend.py"
    spec = importlib.util.spec_from_file_location("o012_generic_u026_validator", path)
    if spec is None or spec.loader is None:
        raise SystemExit("cannot load generic backend validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def expected_ids() -> dict[str, set[str]]:
    relations = {
        "relation:adapts:o012-rbt-u026:edition",
        "relation:precedes:o012-rbt-u025:o012-rbt-u026",
        "relation:precedes:o012-rbt-l26:mastery",
        "relation:boundary:o012-u026",
        "relation:route:d60-r13:o012-rbt-u026",
        "relation:depends-on:o012-rbt-l26-proof-002:l24-thm-001",
        "relation:proves:o012-rbt-l26-thm-002:thm-001",
    }
    relations |= {f"relation:proves:o012-rbt-l26-proof-{n:03d}:closure"
                  for n in range(1, 10)}
    relations |= {f"relation:solves:l26-sol-{n:03d}:l26-mcheck-{n:03d}"
                  for n in range(1, 7)}
    relations |= {f"relation:hints:l26-hint-{n:03d}:l26-mcheck-{n:03d}"
                  for n in range(1, 7)}
    return {
        "artifacts.jsonl": {"artifact:o012-u026-source-audit",
                            "artifact:o012-u026-independent-review",
                            "artifact:o012-u026-qa"},
        "assets.jsonl": {"asset:o012-u026-source-markdown"},
        "authority.jsonl": set(),
        "concepts.jsonl": {f"concept:{slug}" for slug in SLUGS},
        "corrections.jsonl": CORRECTION_IDS,
        "qa.jsonl": {"qa:o012-u026-source-integrity", "qa:o012-u026-math",
                      "qa:o012-u026-language"},
        "relations.jsonl": relations,
        "rights.jsonl": {COMPANION_RIGHTS, COMPOSITE_RIGHTS, CUMULATIVE_RIGHTS},
        "segments.jsonl": {f"segment:{ident}" for ident in ANCHORS},
        "terms.jsonl": {f"term:{slug}:id-ID" for slug in SLUGS},
        "units.jsonl": {ROOT} | {f"unit:{ident}" for ident in ANCHORS},
    }


def load_and_partition() -> tuple[dict[str, list[dict[str, Any]]],
                                  dict[str, list[dict[str, Any]]],
                                  dict[str, dict[str, Any]]]:
    expected = expected_ids()
    prefixes: dict[str, list[dict[str, Any]]] = {}
    suffixes: dict[str, list[dict[str, Any]]] = {}
    all_records: list[dict[str, Any]] = []
    bundle = hashlib.sha256()
    prefix_bundle = hashlib.sha256()
    global_ids: set[str] = set()
    for name in FILES:
        raw = (BACKEND / name).read_bytes()
        final_count, final_bytes, final_sha = FINAL[name]
        if (len(raw), len(raw.splitlines()), digest(raw)) != (
                final_bytes, final_count, final_sha):
            raise SystemExit(f"{name}: final Unit 26 identity mismatch")
        prefix_count, prefix_bytes, prefix_sha = PREFIX[name]
        prefix_raw = raw[:prefix_bytes]
        if (len(prefix_raw.splitlines()), digest(prefix_raw)) != (prefix_count, prefix_sha):
            raise SystemExit(f"{name}: Units 001-025 byte prefix mismatch")
        if raw[prefix_bytes:prefix_bytes + 1] in {b"\n", b"\r"}:
            raise SystemExit(f"{name}: suffix begins with an extra newline")
        prefix_objs = [json.loads(line.decode("utf-8"))
                       for line in prefix_raw.splitlines(keepends=True)]
        suffix_raw = raw[prefix_bytes:]
        suffix_lines = suffix_raw.splitlines(keepends=True) if suffix_raw else []
        suffix_objs: list[dict[str, Any]] = []
        for number, line in enumerate(suffix_lines, 1):
            obj = json.loads(line.decode("utf-8"))
            if canon(obj) != line:
                raise SystemExit(f"{name}: noncanonical suffix record {number}")
            suffix_objs.append(obj)
        suffix_ids = [obj["id"] for obj in suffix_objs]
        if suffix_ids != sorted(suffix_ids) or set(suffix_ids) != expected[name]:
            raise SystemExit(f"{name}: Unit 26 suffix ID/order mismatch")
        if len(suffix_objs) != DELTA[name]:
            raise SystemExit(f"{name}: Unit 26 suffix count mismatch")
        for obj in prefix_objs + suffix_objs:
            if obj["id"] in global_ids:
                raise SystemExit(f"global duplicate ID: {obj['id']}")
            global_ids.add(obj["id"])
        prefixes[name] = prefix_objs
        suffixes[name] = suffix_objs
        all_records.extend(prefix_objs + suffix_objs)
        prefix_bundle.update(name.encode()); prefix_bundle.update(b"\0"); prefix_bundle.update(prefix_raw)
        bundle.update(name.encode()); bundle.update(b"\0"); bundle.update(raw)
    if (sum(len(items) for items in prefixes.values()),
        sum(PREFIX[name][1] for name in FILES), prefix_bundle.hexdigest()) != PREFIX_TOTAL:
        raise SystemExit("Units 001-025 cumulative prefix total mismatch")
    if (len(all_records), sum(FINAL[name][1] for name in FILES),
        bundle.hexdigest()) != FINAL_TOTAL:
        raise SystemExit("Unit 26 final bundle total mismatch")
    return prefixes, suffixes, {obj["id"]: obj for obj in all_records}


def verify_sources(by_id: dict[str, dict[str, Any]]) -> None:
    source_raw = SOURCE.read_bytes()
    if (len(source_raw), len(source_raw.splitlines()), digest(source_raw)) != SOURCE_IDENTITY:
        raise SystemExit("Unit 26 reader identity mismatch")
    if source_raw.count(MODEL.encode()) != 1 or re.search(
            rb"\bfunktor(?:ialitas)?\b", source_raw, re.IGNORECASE):
        raise SystemExit("Unit 26 provenance/terminology identity mismatch")
    upstream_raw = UPSTREAM.read_bytes()
    if (len(upstream_raw), len(upstream_raw.splitlines()), digest(upstream_raw)) != UPSTREAM_IDENTITY:
        raise SystemExit("frozen upstream identity mismatch")
    upstream_lines = upstream_raw.decode("utf-8").replace("\r\n", "\n").split("\n")
    start, end, size, sha = SPAN_IDENTITY
    span = ("\n".join(upstream_lines[start - 1:end]) + "\n").encode()
    if len(span) != size or digest(span) != sha:
        raise SystemExit("Unit 26 authority span mismatch")
    ids = re.findall(rb"\{[^}\n]*#(o012-rbt-l26(?:-[A-Za-z0-9-]+)?)[^}\n]*\}", source_raw)
    decoded = tuple(item.decode() for item in ids)
    if decoded != ANCHORS or len(set(decoded)) != 62:
        raise SystemExit("Unit 26 reader stable-ID order mismatch")
    source_lines = source_raw.splitlines(keepends=True)
    for ident in ANCHORS:
        unit = by_id[f"unit:{ident}"]
        segment = by_id[f"segment:{ident}"]
        locator = unit["target_locator"]
        if segment["target_locator"] != locator or locator["path"] != SOURCE_PATH:
            raise SystemExit(f"Unit 26 unit/segment target mismatch: {ident}")
        low, high = locator["line_start"], locator["line_end"]
        if (locator["file_sha256"] != SOURCE_IDENTITY[2]
                or digest(b"".join(source_lines[low - 1:high])) != locator["content_sha256"]
                or ident.encode() not in source_lines[low - 1]):
            raise SystemExit(f"Unit 26 target-locator mismatch: {ident}")


def verify_closure(suffixes: dict[str, list[dict[str, Any]]],
                   by_id: dict[str, dict[str, Any]]) -> None:
    new_units = suffixes["units.jsonl"]
    new_segments = suffixes["segments.jsonl"]
    if len(new_units) != 63 or len(new_segments) != 62:
        raise SystemExit("Unit 26 unit/segment cardinality mismatch")
    for obj in new_units + new_segments:
        if (obj.get("edition_unit_id", ROOT) != ROOT
                or obj.get("course_route_unit_id", ROUTE) != ROUTE
                or obj.get("model_provenance", MODEL) != MODEL):
            raise SystemExit(f"route/provenance mismatch: {obj['id']}")
    root = by_id[ROOT]
    locator = root["source_locator"]
    if (root["order"] != 26 or root["rights_component_id"] != COMPOSITE_RIGHTS
            or locator.get("commit_sha") != COMMIT
            or (locator.get("line_start"), locator.get("line_end"),
                locator.get("span_bytes"), locator.get("span_sha256")) != SPAN_IDENTITY
            or root["target_locator"]["content_sha256"] != SOURCE_IDENTITY[2]):
        raise SystemExit("Unit 26 root source/rights identity mismatch")
    aliases = {alias: obj["id"] for obj in new_units
               for alias in obj.get("source_aliases", [])}
    if aliases != {"prop:les_of_pair_of_spaces": "unit:o012-rbt-l26-prop-002",
                   "thm:homotopy_invariance_cohom": "unit:o012-rbt-l26-thm-001"}:
        raise SystemExit("Unit 26 source-label alias mismatch")
    boundary = by_id["unit:o012-rbt-l26-boundary-001"]
    if boundary.get("next_source_line") != 5824:
        raise SystemExit("Unit 26 terminal cursor mismatch")
    rights = by_id[CUMULATIVE_RIGHTS]
    if (rights["supersedes"] != PRIOR_RIGHTS
            or rights["component_scope"] != [f"unit:o012-rbt-u{n:03d}" for n in range(1, 27)]
            or rights["license_expression"] != "CC-BY-4.0"):
        raise SystemExit("Unit 26 cumulative rights closure mismatch")
    for ident in (COMPANION_RIGHTS, COMPOSITE_RIGHTS):
        if by_id[ident]["component_scope"] != [ROOT]:
            raise SystemExit(f"Unit 26 component rights mismatch: {ident}")
    sibling_orders: defaultdict[str, list[int]] = defaultdict(list)
    for unit in new_units:
        sibling_orders[unit["parent_id"]].append(unit["order"])
        if unit["path"][-1] != unit["id"]:
            raise SystemExit(f"Unit 26 noncanonical path: {unit['id']}")
        if unit["parent_id"].startswith("unit:") and unit["path"][:-1] != by_id[unit["parent_id"]]["path"]:
            raise SystemExit(f"Unit 26 parent-path mismatch: {unit['id']}")
    if any(len(values) != len(set(values)) for values in sibling_orders.values()):
        raise SystemExit("Unit 26 duplicate sibling order")
    relations = suffixes["relations.jsonl"]
    proofs = [obj for obj in new_units if obj.get("proof_status")]
    proof_relations = [obj for obj in relations
                       if obj["relation_type"] == "proves"
                       and obj["from_id"].startswith("unit:o012-rbt-l26-proof-")]
    if len(proofs) != 9 or len(proof_relations) != 9:
        raise SystemExit("Unit 26 proof closure mismatch")
    for n in range(1, 7):
        exercise = f"unit:o012-rbt-l26-mcheck-{n:03d}"
        solution = f"unit:o012-rbt-l26-sol-{n:03d}"
        hint = f"unit:o012-rbt-l26-hint-{n:03d}"
        solves = [obj for obj in relations if obj["relation_type"] == "solves"
                  and obj["from_id"] == solution and obj["to_id"] == exercise]
        hints = [obj for obj in relations if obj["relation_type"] == "hints"
                 and obj["from_id"] == hint and obj["to_id"] == exercise]
        if len(solves) != 1 or len(hints) != 1 or by_id[solution].get(
                "solution_status") != "complete_checked_solution":
            raise SystemExit(f"Unit 26 mastery closure mismatch: {n}")
    corrections = suffixes["corrections.jsonl"]
    if ({obj["id"] for obj in corrections} != CORRECTION_IDS
            or any(obj["upstream_report_disposition"] != "not_contacted"
                   for obj in corrections)
            or Counter(obj["correction_type"] for obj in corrections)["proof_completion"] < 4):
        raise SystemExit("Unit 26 correction/provenance closure mismatch")
    terms = suffixes["terms.jsonl"]
    if ({obj["concept_id"].removeprefix("concept:") for obj in terms} != SLUGS
            or any(obj.get("terminology_status") != "unit_attested_reviewed" for obj in terms)
            or any(obj["evidence_segment_id"] not in by_id for obj in terms)):
        raise SystemExit("Unit 26 terminology evidence closure mismatch")
    expected_evidence = {
        "artifact:o012-u026-source-audit": ("qa/UNIT_026_SOURCE_AUDIT.md", 7693,
            "658a2586c58fd4149cf4959bc9b405d67896984f61621b1533f873836a9c8bb5"),
        "artifact:o012-u026-independent-review": ("qa/UNIT_026_INDEPENDENT_REVIEW.md", 7718,
            "b00eb4de7d29e9833539d0086ebc12e5d7339137ebc2b74874d9cfc72c4e3111"),
        "artifact:o012-u026-qa": ("qa/UNIT_026_QA.json", 7310,
            "3a25fc42dfa4353e8ba50a5f619684196a73fcb350e39a9d539568c0542bf835"),
    }
    for ident, triple in expected_evidence.items():
        artifact = by_id[ident]
        if (artifact["path"], artifact["bytes"], artifact["sha256"]) != triple:
            raise SystemExit(f"Unit 26 evidence artifact mismatch: {ident}")
    for ident in ("qa:o012-u026-source-integrity", "qa:o012-u026-math",
                  "qa:o012-u026-language"):
        if by_id[ident]["result"] != "passed" or by_id[ident]["unit_id"] != ROOT:
            raise SystemExit(f"Unit 26 QA event mismatch: {ident}")
    if not any(obj["id"] == "relation:precedes:o012-rbt-u025:o012-rbt-u026"
               and obj["from_id"] == "unit:o012-rbt-u025" and obj["to_id"] == ROOT
               for obj in relations):
        raise SystemExit("Unit 26 contiguous dependency relation missing")


def main() -> int:
    _prefixes, suffixes, by_id = load_and_partition()
    generic = generic_module()
    records = list(by_id.values())
    generic.validate_shapes(records)
    generic.validate_references(records, by_id)
    generic.validate_artifact_manifests(records, LANE)
    verify_sources(by_id)
    verify_closure(suffixes, by_id)
    print("Unit 026 semantic append-only backend validation: PASS")
    print(f"prefix_records={PREFIX_TOTAL[0]}")
    print(f"prefix_bytes={PREFIX_TOTAL[1]}")
    print(f"prefix_bundle_sha256={PREFIX_TOTAL[2]}")
    print("records_added=192")
    print("records_added_by_file=" + json.dumps(DELTA, sort_keys=True))
    print(f"final_records={FINAL_TOTAL[0]}")
    print(f"final_bytes={FINAL_TOTAL[1]}")
    print(f"final_bundle_sha256={FINAL_TOTAL[2]}")
    print("stable_ids=62")
    print("proof_closures=9")
    print("mastery_triples=6")
    print("source_aliases=2")
    print("next_source_line=5824")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
