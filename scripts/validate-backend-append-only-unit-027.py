#!/usr/bin/env python3
"""Independent fail-closed validator for the Unit 027 semantic append."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

LANE = Path(__file__).resolve().parents[1]
BACKEND = LANE / "backend"
SOURCE = LANE / "source/id-ID/units/unit-027-lecture-027.md"
UPSTREAM = (LANE / "authority/upstream" /
            "AlgebraicTopology2019-b947ad2e9f9e301bfe24590a9db653bc54fa1a53" /
            "Notes.tex")
FILES = ("artifacts.jsonl", "assets.jsonl", "authority.jsonl", "concepts.jsonl",
         "corrections.jsonl", "qa.jsonl", "relations.jsonl", "rights.jsonl",
         "segments.jsonl", "terms.jsonl", "units.jsonl")
PREFIX = {
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
PREFIX_TOTAL = (4105, 4305218,
                "89556c5fa2224820837fc8956b1a48797929f28bef013baf9a613e73e6cf28eb")
DELTA = {"artifacts.jsonl": 3, "assets.jsonl": 1, "authority.jsonl": 0,
         "concepts.jsonl": 8, "corrections.jsonl": 16, "qa.jsonl": 3,
         "relations.jsonl": 24, "rights.jsonl": 3, "segments.jsonl": 46,
         "terms.jsonl": 8, "units.jsonl": 47}
FINAL = {
    "artifacts.jsonl": (151, 120648, "c16f1deaa3844a19ece5c112a4a556b6a31c1fe6a8065f1773aa123bdd0f5311"),
    "assets.jsonl": (29, 17911, "260fbded514ca70a5b54866bfc2b26cc770612876984cc81aae47516b8592449"),
    "authority.jsonl": (4, 2721, "f21af26912520ab34b38dff0e927ed46a546dbe5d318da0dc133e58330d0e368"),
    "concepts.jsonl": (341, 107533, "bf5b7bd06811e74e9d5139dfec4903e8f3429a98939fa106e45a3def519db473"),
    "corrections.jsonl": (361, 354746, "ffa733a7ac19745aa9d4ef67c98911e011a2ebc51e4353fa40fc1b337b9c0023"),
    "qa.jsonl": (125, 70471, "fc02b08c7ec19dba9654db5aa9d2bd2cfe9b855a222d5764a06fc93bffc2d319"),
    "relations.jsonl": (449, 183555, "e8a0831badaebbe47523f92ac1949f2266f544ad3baede0f35967d1764e959bf"),
    "rights.jsonl": (77, 71149, "5f4a0f6de1866c04f0d56d7f7ed508f4c41364c9626d357e94e6f4a135002767"),
    "segments.jsonl": (1183, 1643547, "2c0dacca32d6e92257c43b2d5c270ede72e257ff5d1dfde8b54e5858e9ac4602"),
    "terms.jsonl": (334, 209753, "c25a3834bed5b9a57624aae9c1d546a24ad08b4ae397e92e8a8e5f6b3d357735"),
    "units.jsonl": (1210, 1750960, "936f41c32c69ba73881038e39b9e33bb4baab39ac9dd5ad56409c370309eeda0"),
}
FINAL_TOTAL = (4264, 4532994,
               "09aa16e8d9387171445c4d465d00a5399e39517a210cb347e30d2d285c703f8c")
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"
COMMIT = "b947ad2e9f9e301bfe24590a9db653bc54fa1a53"
SOURCE_PATH = "source/id-ID/units/unit-027-lecture-027.md"
SOURCE_IDENTITY = (35879, 1175,
                   "a3238bbc429e4c3689bce3b3bb78c5514e0fae74f276c9efebe694730b2df2a0")
UPSTREAM_IDENTITY = (331447, 6368,
                     "cfe93e9dbe3e25bd96f711f59e6078ab97527682b58e1f8ad127f74357f665d7")
SPAN_IDENTITY = (5824, 5923, 7012,
                 "65d2c393ddf29183f36d6e9ab65c65f8030110334f89c7f68ba88461fc30afa1")
ROOT = "unit:o012-rbt-u027"
ROUTE = "D60-R13"
COMPANION_RIGHTS = "rights:o012-u027-companion-cc-by-4.0"
COMPOSITE_RIGHTS = "rights:o012-u027-composite-cc-by-4.0"
CUMULATIVE_RIGHTS = "rights:o012-units-001-027-composite-cc-by-4.0"
PRIOR_RIGHTS = "rights:o012-units-001-026-composite-cc-by-4.0"

ANCHORS = (
    "o012-rbt-l27-notice", "o012-rbt-l27", "o012-rbt-l27-s01",
    "o012-rbt-l27-mcheck-001", "o012-rbt-l27-hint-001", "o012-rbt-l27-sol-001",
    "o012-rbt-l27-audit-001", "o012-rbt-l27-def-001", "o012-rbt-l27-lem-001",
    "o012-rbt-l27-proof-001", "o012-rbt-l27-margin-001",
    "o012-rbt-l27-def-002", "o012-rbt-l27-exa-001", "o012-rbt-l27-audit-002",
    "o012-rbt-l27-exa-002", "o012-rbt-l27-s02", "o012-rbt-l27-fig-001",
    "o012-rbt-l27-eq-001", "o012-rbt-l27-audit-003",
    "o012-rbt-l27-prop-001", "o012-rbt-l27-proof-002",
    "o012-rbt-l27-s03", "o012-rbt-l27-thm-001", "o012-rbt-l27-proof-003",
    "o012-rbt-l27-audit-004", "o012-rbt-l27-s04", "o012-rbt-l27-exa-003",
    "o012-rbt-l27-eq-002", "o012-rbt-l27-audit-005",
    "o012-rbt-l27-mastery", "o012-rbt-l27-mcheck-002",
    "o012-rbt-l27-hint-002", "o012-rbt-l27-sol-002",
    "o012-rbt-l27-mcheck-003", "o012-rbt-l27-hint-003",
    "o012-rbt-l27-sol-003", "o012-rbt-l27-mcheck-004",
    "o012-rbt-l27-hint-004", "o012-rbt-l27-sol-004",
    "o012-rbt-l27-mcheck-005", "o012-rbt-l27-hint-005",
    "o012-rbt-l27-sol-005", "o012-rbt-l27-mcheck-006",
    "o012-rbt-l27-hint-006", "o012-rbt-l27-sol-006",
    "o012-rbt-l27-boundary-001",
)
SLUGS = {"left-splitting", "reduced-degree-zero-cohomology",
         "small-singular-chain-complex", "small-singular-cochain-complex",
         "barycentric-subdivision", "chain-homotopy-equivalence",
         "mayer-vietoris-long-exact-sequence", "sphere-cohomology"}
CORRECTION_IDS = {f"correction:o012-u027-dossier-{n:03d}" for n in range(1, 12)} | {
    "correction:o012-u027-resolved-math-001",
    "correction:o012-u027-resolved-a11y-002",
    "correction:o012-u027-resolved-proof-003",
    "correction:o012-u027-resolved-term-001",
    "correction:o012-u027-resolved-term-002",
}


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canon(obj: dict[str, Any]) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8") + b"\n"


def generic_module():
    path = LANE / "scripts/validate-backend.py"
    spec = importlib.util.spec_from_file_location("o012_generic_u027_validator", path)
    if spec is None or spec.loader is None:
        raise SystemExit("cannot load generic backend validator")
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


def expected_ids() -> dict[str, set[str]]:
    relations = {
        "relation:adapts:o012-rbt-u027:edition",
        "relation:precedes:o012-rbt-u026:o012-rbt-u027",
        "relation:precedes:o012-rbt-l27:mastery",
        "relation:boundary:o012-u027", "relation:route:d60-r13:o012-rbt-u027",
        "relation:depends-on:o012-rbt-l27-prop-001:eq-001",
        "relation:depends-on:o012-rbt-l27-thm-001:prop-001",
        "relation:depends-on:o012-rbt-l27-exa-003:thm-001",
        "relation:xref:o012-rbt-l27-mcheck-005:exa-002",
    }
    relations |= {f"relation:proves:o012-rbt-l27-proof-{n:03d}:closure"
                  for n in range(1, 4)}
    relations |= {f"relation:solves:l27-sol-{n:03d}:l27-mcheck-{n:03d}"
                  for n in range(1, 7)}
    relations |= {f"relation:hints:l27-hint-{n:03d}:l27-mcheck-{n:03d}"
                  for n in range(1, 7)}
    return {
        "artifacts.jsonl": {"artifact:o012-u027-source-audit",
                            "artifact:o012-u027-independent-review",
                            "artifact:o012-u027-qa"},
        "assets.jsonl": {"asset:o012-u027-source-markdown"},
        "authority.jsonl": set(),
        "concepts.jsonl": {f"concept:{slug}" for slug in SLUGS},
        "corrections.jsonl": CORRECTION_IDS,
        "qa.jsonl": {"qa:o012-u027-source-integrity", "qa:o012-u027-math",
                      "qa:o012-u027-language"},
        "relations.jsonl": relations,
        "rights.jsonl": {COMPANION_RIGHTS, COMPOSITE_RIGHTS, CUMULATIVE_RIGHTS},
        "segments.jsonl": {f"segment:{ident}" for ident in ANCHORS},
        "terms.jsonl": {f"term:{slug}:id-ID" for slug in SLUGS},
        "units.jsonl": {ROOT} | {f"unit:{ident}" for ident in ANCHORS},
    }


def load_and_partition() -> tuple[dict[str, list[dict[str, Any]]], dict[str, dict[str, Any]]]:
    expected = expected_ids()
    suffixes: dict[str, list[dict[str, Any]]] = {}
    records: list[dict[str, Any]] = []
    bundle = hashlib.sha256(); prefix_bundle = hashlib.sha256(); ids: set[str] = set()
    for name in FILES:
        raw = (BACKEND / name).read_bytes()
        if (len(raw.splitlines()), len(raw), digest(raw)) != FINAL[name]:
            raise SystemExit(f"{name}: final Unit 27 identity mismatch")
        prefix_count, prefix_bytes, prefix_sha = PREFIX[name]
        prefix = raw[:prefix_bytes]
        if (len(prefix.splitlines()), len(prefix), digest(prefix)) != (
                prefix_count, prefix_bytes, prefix_sha):
            raise SystemExit(f"{name}: Unit 26 byte prefix mismatch")
        prefix_objs = [json.loads(line.decode("utf-8"))
                       for line in prefix.splitlines(keepends=True)]
        suffix_lines = raw[prefix_bytes:].splitlines(keepends=True)
        suffix_objs: list[dict[str, Any]] = []
        for number, line in enumerate(suffix_lines, 1):
            obj = json.loads(line.decode("utf-8"))
            if canon(obj) != line:
                raise SystemExit(f"{name}: noncanonical suffix record {number}")
            suffix_objs.append(obj)
        suffix_ids = [obj["id"] for obj in suffix_objs]
        if (suffix_ids != sorted(suffix_ids)
                or set(suffix_ids) != expected[name]
                or len(suffix_objs) != DELTA[name]):
            raise SystemExit(f"{name}: Unit 27 suffix ID/order/count mismatch")
        for obj in prefix_objs + suffix_objs:
            if obj["id"] in ids:
                raise SystemExit(f"global duplicate ID: {obj['id']}")
            ids.add(obj["id"])
        suffixes[name] = suffix_objs; records.extend(prefix_objs + suffix_objs)
        prefix_bundle.update(name.encode()); prefix_bundle.update(b"\0"); prefix_bundle.update(prefix)
        bundle.update(name.encode()); bundle.update(b"\0"); bundle.update(raw)
    if (sum(PREFIX[name][0] for name in FILES), sum(PREFIX[name][1] for name in FILES),
        prefix_bundle.hexdigest()) != PREFIX_TOTAL:
        raise SystemExit("Unit 26 prefix total mismatch")
    if (len(records), sum(FINAL[name][1] for name in FILES), bundle.hexdigest()) != FINAL_TOTAL:
        raise SystemExit("Unit 27 final bundle total mismatch")
    return suffixes, {obj["id"]: obj for obj in records}


def verify_sources(by_id: dict[str, dict[str, Any]]) -> None:
    source_raw = SOURCE.read_bytes()
    if (len(source_raw), len(source_raw.splitlines()), digest(source_raw)) != SOURCE_IDENTITY:
        raise SystemExit("Unit 27 reader identity mismatch")
    if (source_raw.count(MODEL.encode()) != 1
            or re.search(rb"\bfunktorial\b|\bperpanjang\w*\b", source_raw, re.IGNORECASE)):
        raise SystemExit("Unit 27 provenance/terminology mismatch")
    upstream_raw = UPSTREAM.read_bytes()
    if (len(upstream_raw), len(upstream_raw.splitlines()), digest(upstream_raw)) != UPSTREAM_IDENTITY:
        raise SystemExit("frozen upstream identity mismatch")
    lines = upstream_raw.decode("utf-8").replace("\r\n", "\n").split("\n")
    start, end, size, sha = SPAN_IDENTITY
    span = ("\n".join(lines[start - 1:end]) + "\n").encode()
    if len(span) != size or digest(span) != sha:
        raise SystemExit("Unit 27 authority span mismatch")
    ids = re.findall(rb"\{[^}\n]*#(o012-rbt-l27(?:-[A-Za-z0-9-]+)?)[^}\n]*\}", source_raw)
    if tuple(item.decode() for item in ids) != ANCHORS or len(set(ids)) != 46:
        raise SystemExit("Unit 27 stable-ID order mismatch")
    source_lines = source_raw.splitlines(keepends=True)
    for ident in ANCHORS:
        unit = by_id[f"unit:{ident}"]; segment = by_id[f"segment:{ident}"]
        locator = unit["target_locator"]
        low, high = locator["line_start"], locator["line_end"]
        if (segment["target_locator"] != locator or locator["path"] != SOURCE_PATH
                or locator["file_sha256"] != SOURCE_IDENTITY[2]
                or digest(b"".join(source_lines[low - 1:high])) != locator["content_sha256"]
                or ident.encode() not in source_lines[low - 1]):
            raise SystemExit(f"Unit 27 target-locator mismatch: {ident}")


def verify_closure(suffixes: dict[str, list[dict[str, Any]]],
                   by_id: dict[str, dict[str, Any]]) -> None:
    units = suffixes["units.jsonl"]; segments = suffixes["segments.jsonl"]
    if len(units) != 47 or len(segments) != 46:
        raise SystemExit("Unit 27 unit/segment cardinality mismatch")
    for obj in units + segments:
        if (obj.get("edition_unit_id", ROOT) != ROOT
                or obj.get("course_route_unit_id", ROUTE) != ROUTE
                or obj.get("model_provenance", MODEL) != MODEL):
            raise SystemExit(f"route/provenance mismatch: {obj['id']}")
    root = by_id[ROOT]; locator = root["source_locator"]
    if (root["order"] != 27 or root["rights_component_id"] != COMPOSITE_RIGHTS
            or locator.get("commit_sha") != COMMIT
            or (locator.get("line_start"), locator.get("line_end"),
                locator.get("span_bytes"), locator.get("span_sha256")) != SPAN_IDENTITY
            or root["target_locator"]["content_sha256"] != SOURCE_IDENTITY[2]):
        raise SystemExit("Unit 27 root source/rights mismatch")
    aliases = {alias: obj["id"] for obj in units for alias in obj.get("source_aliases", [])}
    if aliases != {"eg:reduced_cohom_S0": "unit:o012-rbt-l27-exa-002",
                   "eq:restr_to_intersection": "unit:o012-rbt-l27-eq-001",
                   "thm:mayer-vietoris": "unit:o012-rbt-l27-thm-001",
                   "eq:sphere_cohomol_reduction": "unit:o012-rbt-l27-eq-002"}:
        raise SystemExit("Unit 27 source alias mismatch")
    figure = by_id["unit:o012-rbt-l27-fig-001"]
    if figure.get("source_formats") != ["xypic"] or figure.get("accessibility_status") != "semantic_reflow":
        raise SystemExit("Unit 27 Xy-pic accessibility mapping mismatch")
    if by_id["unit:o012-rbt-l27-boundary-001"].get("next_source_line") != 5924:
        raise SystemExit("Unit 27 terminal cursor mismatch")
    rights = by_id[CUMULATIVE_RIGHTS]
    if (rights["supersedes"] != PRIOR_RIGHTS
            or rights["component_scope"] != [f"unit:o012-rbt-u{n:03d}" for n in range(1, 28)]
            or rights["license_expression"] != "CC-BY-4.0"):
        raise SystemExit("Unit 27 cumulative rights closure mismatch")
    sibling: defaultdict[str, list[int]] = defaultdict(list)
    for unit in units:
        sibling[unit["parent_id"]].append(unit["order"])
        if unit["path"][-1] != unit["id"]:
            raise SystemExit(f"Unit 27 noncanonical path: {unit['id']}")
        if unit["parent_id"].startswith("unit:") and unit["path"][:-1] != by_id[unit["parent_id"]]["path"]:
            raise SystemExit(f"Unit 27 parent-path mismatch: {unit['id']}")
    if any(len(values) != len(set(values)) for values in sibling.values()):
        raise SystemExit("Unit 27 duplicate sibling order")
    relations = suffixes["relations.jsonl"]
    proofs = [obj for obj in units if obj.get("proof_status")]
    proof_relations = [obj for obj in relations if obj["relation_type"] == "proves"]
    if len(proofs) != 3 or len(proof_relations) != 3:
        raise SystemExit("Unit 27 proof closure mismatch")
    for n in range(1, 7):
        exercise = f"unit:o012-rbt-l27-mcheck-{n:03d}"
        solution = f"unit:o012-rbt-l27-sol-{n:03d}"
        hint = f"unit:o012-rbt-l27-hint-{n:03d}"
        if (sum(obj["relation_type"] == "solves" and obj["from_id"] == solution
                and obj["to_id"] == exercise for obj in relations) != 1
                or sum(obj["relation_type"] == "hints" and obj["from_id"] == hint
                       and obj["to_id"] == exercise for obj in relations) != 1
                or by_id[solution].get("solution_status") != "complete_checked_solution"):
            raise SystemExit(f"Unit 27 mastery closure mismatch: {n}")
    if by_id["unit:o012-rbt-l27-mcheck-001"]["rights_component_id"] != "rights:roberts-cc-by-4.0":
        raise SystemExit("Unit 27 preserved source exercise rights mismatch")
    corrections = suffixes["corrections.jsonl"]
    if ({obj["id"] for obj in corrections} != CORRECTION_IDS
            or any(obj["upstream_report_disposition"] != "not_contacted" for obj in corrections)):
        raise SystemExit("Unit 27 correction closure mismatch")
    terms = suffixes["terms.jsonl"]
    if ({obj["concept_id"].removeprefix("concept:") for obj in terms} != SLUGS
            or any(obj.get("terminology_status") != "unit_attested_reviewed" for obj in terms)
            or any(obj["evidence_segment_id"] not in by_id for obj in terms)):
        raise SystemExit("Unit 27 terminology closure mismatch")
    expected_evidence = {
        "artifact:o012-u027-source-audit": ("qa/UNIT_027_SOURCE_AUDIT.md", 7369,
            "67621ce38a69fe4e6afd24fa6572dfa6e9499a3e77db03e3943ce045dfa30138"),
        "artifact:o012-u027-independent-review": ("qa/UNIT_027_INDEPENDENT_REVIEW.md", 8560,
            "d464310e42fea0c199b49a6a9670d97cf8704b3c37b7cc79023fece21cb734b5"),
        "artifact:o012-u027-qa": ("qa/UNIT_027_QA.json", 8152,
            "1db997b0ddf1dee05583c8c8c482e68f59a9add7677b34fded034088f55e491f"),
    }
    for ident, triple in expected_evidence.items():
        obj = by_id[ident]
        if (obj["path"], obj["bytes"], obj["sha256"]) != triple:
            raise SystemExit(f"Unit 27 evidence mismatch: {ident}")
    for ident in ("qa:o012-u027-source-integrity", "qa:o012-u027-math",
                  "qa:o012-u027-language"):
        if by_id[ident]["result"] != "passed" or by_id[ident]["unit_id"] != ROOT:
            raise SystemExit(f"Unit 27 QA event mismatch: {ident}")
    if not any(obj["id"] == "relation:precedes:o012-rbt-u026:o012-rbt-u027"
               and obj["from_id"] == "unit:o012-rbt-u026" and obj["to_id"] == ROOT
               for obj in relations):
        raise SystemExit("Unit 27 contiguous predecessor relation missing")


def main() -> int:
    suffixes, by_id = load_and_partition()
    generic = generic_module(); records = list(by_id.values())
    generic.validate_shapes(records)
    generic.validate_references(records, by_id)
    generic.validate_artifact_manifests(records, LANE)
    verify_sources(by_id); verify_closure(suffixes, by_id)
    print("Unit 027 semantic append-only backend validation: PASS")
    print(f"prefix_records={PREFIX_TOTAL[0]}")
    print(f"prefix_bytes={PREFIX_TOTAL[1]}")
    print(f"prefix_bundle_sha256={PREFIX_TOTAL[2]}")
    print("records_added=159")
    print("records_added_by_file=" + json.dumps(DELTA, sort_keys=True))
    print(f"final_records={FINAL_TOTAL[0]}")
    print(f"final_bytes={FINAL_TOTAL[1]}")
    print(f"final_bundle_sha256={FINAL_TOTAL[2]}")
    print("stable_ids=46")
    print("proof_closures=3")
    print("mastery_triples=6")
    print("source_aliases=4")
    print("next_source_line=5924")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
