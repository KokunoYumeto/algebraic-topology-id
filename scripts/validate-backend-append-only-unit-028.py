#!/usr/bin/env python3
"""Independent fail-closed validator for the Unit 028 semantic append."""
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
SOURCE = LANE / "source/id-ID/units/unit-028-lecture-028.md"
UPSTREAM = (LANE / "authority/upstream" /
            "AlgebraicTopology2019-b947ad2e9f9e301bfe24590a9db653bc54fa1a53" /
            "Notes.tex")
QA_JSON = LANE / "qa/UNIT_028_QA.json"
FILES = ("artifacts.jsonl", "assets.jsonl", "authority.jsonl", "concepts.jsonl",
         "corrections.jsonl", "qa.jsonl", "relations.jsonl", "rights.jsonl",
         "segments.jsonl", "terms.jsonl", "units.jsonl")
PREFIX = {
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
PREFIX_TOTAL = (4264, 4532994,
                "09aa16e8d9387171445c4d465d00a5399e39517a210cb347e30d2d285c703f8c")
DELTA = {"artifacts.jsonl": 3, "assets.jsonl": 1, "authority.jsonl": 0,
         "concepts.jsonl": 6, "corrections.jsonl": 17, "qa.jsonl": 3,
         "relations.jsonl": 27, "rights.jsonl": 3, "segments.jsonl": 47,
         "terms.jsonl": 6, "units.jsonl": 48}
FINAL = {
    "artifacts.jsonl": (154, 123215, "dcbe6a233ae2150054b6337fcbcde5a8429f36e13376fdc1e5cfe89319181934"),
    "assets.jsonl": (30, 18527, "33e5e928c08a45e019c5647baf76afc49febf66c91fe20bcb52ebaa903f1693d"),
    "authority.jsonl": (4, 2721, "f21af26912520ab34b38dff0e927ed46a546dbe5d318da0dc133e58330d0e368"),
    "concepts.jsonl": (347, 109564, "b65dbfd31c351d73b270eaf3054df7101a5cfac462a530492888fe6b1a845ae8"),
    "corrections.jsonl": (378, 370217, "bca78b345bd76599e3f62f79a41e4827754fa03b7c2fc63e207282651e71e27a"),
    "qa.jsonl": (128, 71958, "f288d793f7d9a2823cc266d3f1c6a6764647127ea0b941d80a6205d8cff06001"),
    "relations.jsonl": (476, 194744, "f9e351b32fdf3397e5b5cb47af3039da94585f3712369c69514ec46673b25f36"),
    "rights.jsonl": (80, 73939, "71f0dd345afdff972f389987a504dc8392a4e4d17d850dbb21f219053f515a9b"),
    "segments.jsonl": (1230, 1736383, "639756c98657d171553f581ec8d252dff48f99ce0b1411d7adc94fbbac56791d"),
    "terms.jsonl": (340, 214594, "f36b329242860f92bdd827594ca8f3bedc140daabc8dbfe5f895534a9de9dfa5"),
    "units.jsonl": (1258, 1849591, "6261024f22eb6b2e90d45f07ed0108fc009a6ebfb2d415e88afce3e411524a3d"),
}
FINAL_TOTAL = (4425, 4765453,
               "3a7492ee9755c85e89139bd6af84121747caa85f1f6421c7ec2e133b010a0b9f")
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"
COMMIT = "b947ad2e9f9e301bfe24590a9db653bc54fa1a53"
SOURCE_PATH = "source/id-ID/units/unit-028-lecture-028.md"
SOURCE_IDENTITY = (26072, 814,
                   "b69036f5a0a8151942288f04197a9dc69c81d2902fe8a15a0e73601978fefe67")
UPSTREAM_IDENTITY = (331447, 6368,
                     "cfe93e9dbe3e25bd96f711f59e6078ab97527682b58e1f8ad127f74357f665d7")
SPAN_IDENTITY = (5924, 6052, 8257,
                 "f3e4a526fa2e504a449a606150c399520c255a98a91d60c934737f87497b4b51")
ROOT = "unit:o012-rbt-u028"
ROUTE = "D60-R14"
COMPANION_RIGHTS = "rights:o012-u028-companion-cc-by-4.0"
COMPOSITE_RIGHTS = "rights:o012-u028-composite-cc-by-4.0"
CUMULATIVE_RIGHTS = "rights:o012-units-001-028-composite-cc-by-4.0"
PRIOR_RIGHTS = "rights:o012-units-001-027-composite-cc-by-4.0"

ANCHORS = (
    "o012-rbt-l28-notice", "o012-rbt-l28", "o012-rbt-l28-s01",
    "o012-rbt-l28-aside-001", "o012-rbt-l28-aside-002",
    "o012-rbt-l28-prop-001", "o012-rbt-l28-s02",
    "o012-rbt-l28-aside-003", "o012-rbt-l28-prop-002",
    "o012-rbt-l28-proof-001", "o012-rbt-l28-audit-001",
    "o012-rbt-l28-s03", "o012-rbt-l28-thm-001",
    "o012-rbt-l28-thm-002", "o012-rbt-l28-proof-002",
    "o012-rbt-l28-audit-002", "o012-rbt-l28-cor-001",
    "o012-rbt-l28-proof-003", "o012-rbt-l28-s04",
    "o012-rbt-l28-def-001", "o012-rbt-l28-audit-003",
    "o012-rbt-l28-prop-003", "o012-rbt-l28-proof-004",
    "o012-rbt-l28-audit-004", "o012-rbt-l28-exa-001",
    "o012-rbt-l28-s05", "o012-rbt-l28-audit-005",
    "o012-rbt-l28-mastery", "o012-rbt-l28-mcheck-001",
    "o012-rbt-l28-hint-001", "o012-rbt-l28-sol-001",
    "o012-rbt-l28-mcheck-002", "o012-rbt-l28-hint-002",
    "o012-rbt-l28-sol-002", "o012-rbt-l28-mcheck-003",
    "o012-rbt-l28-hint-003", "o012-rbt-l28-sol-003",
    "o012-rbt-l28-mcheck-004", "o012-rbt-l28-hint-004",
    "o012-rbt-l28-sol-004", "o012-rbt-l28-mcheck-005",
    "o012-rbt-l28-hint-005", "o012-rbt-l28-sol-005",
    "o012-rbt-l28-mcheck-006", "o012-rbt-l28-hint-006",
    "o012-rbt-l28-sol-006", "o012-rbt-l28-boundary-001",
)
SOURCE_RANGES = {
    "o012-rbt-l28": (5924, 6052), "o012-rbt-l28-s01": (5924, 5947),
    "o012-rbt-l28-aside-001": (5924, 5924), "o012-rbt-l28-aside-002": (5927, 5927),
    "o012-rbt-l28-prop-001": (5939, 5947), "o012-rbt-l28-s02": (5949, 5958),
    "o012-rbt-l28-aside-003": (5949, 5949), "o012-rbt-l28-prop-002": (5951, 5953),
    "o012-rbt-l28-proof-001": (5955, 5957), "o012-rbt-l28-s03": (5959, 5997),
    "o012-rbt-l28-thm-001": (5961, 5967), "o012-rbt-l28-thm-002": (5973, 5979),
    "o012-rbt-l28-cor-001": (5987, 5992), "o012-rbt-l28-proof-003": (5994, 5996),
    "o012-rbt-l28-s04": (5998, 6042), "o012-rbt-l28-def-001": (6009, 6011),
    "o012-rbt-l28-prop-003": (6025, 6031), "o012-rbt-l28-exa-001": (6033, 6041),
    "o012-rbt-l28-s05": (6043, 6052),
}
SLUGS = {"excision", "cohomological-dimension-invariance",
         "relative-cohomology-quotient-isomorphism", "infinite-wedge-cohomology",
         "singular-simplicial-cochain-comparison", "well-pointed-space"}
CORRECTION_IDS = {f"correction:o012-u028-dossier-{n:03d}" for n in range(1, 12)} | {
    "correction:o012-u028-resolved-math-p2-001",
    "correction:o012-u028-resolved-audit-p3-001",
    "correction:o012-u028-resolved-prov-p3-002",
    "correction:o012-u028-resolved-math-p3-003",
    "correction:o012-u028-resolved-term-p3-004",
    "correction:o012-u028-resolved-term-p3-005",
}
RESOLVED_FINDINGS = {"UNIT028-MATH-P2-001", "UNIT028-AUDIT-P3-001",
                     "UNIT028-PROV-P3-002", "UNIT028-MATH-P3-003",
                     "UNIT028-TERM-P3-004", "UNIT028-TERM-P3-005"}


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canon(obj: dict[str, Any]) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8") + b"\n"


def generic_module():
    path = LANE / "scripts/validate-backend.py"
    spec = importlib.util.spec_from_file_location("o012_generic_u028_validator", path)
    if spec is None or spec.loader is None:
        raise SystemExit("cannot load generic backend validator")
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


def expected_ids() -> dict[str, set[str]]:
    relations = {
        "relation:adapts:o012-rbt-u028:edition",
        "relation:precedes:o012-rbt-u027:o012-rbt-u028",
        "relation:precedes:o012-rbt-l28:mastery",
        "relation:boundary:o012-u028", "relation:route:d60-r14:o012-rbt-u028",
        "relation:xref:o012-rbt-l28-s01:l27-eq-002",
        "relation:depends-on:o012-rbt-l28-cor-001:thm-002",
        "relation:depends-on:o012-rbt-l28-proof-003:thm-002",
        "relation:xref:o012-rbt-l28-proof-003:l26-prop-002",
        "relation:depends-on:o012-rbt-l28-prop-003:thm-002",
        "relation:depends-on:o012-rbt-l28-exa-001:prop-003",
    }
    relations |= {f"relation:proves:o012-rbt-l28-proof-{n:03d}:closure"
                  for n in range(1, 5)}
    relations |= {f"relation:solves:l28-sol-{n:03d}:l28-mcheck-{n:03d}"
                  for n in range(1, 7)}
    relations |= {f"relation:hints:l28-hint-{n:03d}:l28-mcheck-{n:03d}"
                  for n in range(1, 7)}
    return {
        "artifacts.jsonl": {"artifact:o012-u028-source-audit",
                            "artifact:o012-u028-independent-review",
                            "artifact:o012-u028-qa"},
        "assets.jsonl": {"asset:o012-u028-source-markdown"},
        "authority.jsonl": set(),
        "concepts.jsonl": {f"concept:{slug}" for slug in SLUGS},
        "corrections.jsonl": CORRECTION_IDS,
        "qa.jsonl": {"qa:o012-u028-source-integrity", "qa:o012-u028-math",
                      "qa:o012-u028-language"},
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
            raise SystemExit(f"{name}: final Unit 28 identity mismatch")
        prefix_count, prefix_bytes, prefix_sha = PREFIX[name]
        prefix = raw[:prefix_bytes]
        if (len(prefix.splitlines()), len(prefix), digest(prefix)) != (
                prefix_count, prefix_bytes, prefix_sha):
            raise SystemExit(f"{name}: Unit 27 byte prefix mismatch")
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
            raise SystemExit(f"{name}: Unit 28 suffix ID/order/count mismatch")
        for obj in prefix_objs + suffix_objs:
            if obj["id"] in ids:
                raise SystemExit(f"global duplicate ID: {obj['id']}")
            ids.add(obj["id"])
        suffixes[name] = suffix_objs; records.extend(prefix_objs + suffix_objs)
        prefix_bundle.update(name.encode()); prefix_bundle.update(b"\0"); prefix_bundle.update(prefix)
        bundle.update(name.encode()); bundle.update(b"\0"); bundle.update(raw)
    if (sum(PREFIX[name][0] for name in FILES), sum(PREFIX[name][1] for name in FILES),
        prefix_bundle.hexdigest()) != PREFIX_TOTAL:
        raise SystemExit("Unit 27 prefix total mismatch")
    if (len(records), sum(FINAL[name][1] for name in FILES), bundle.hexdigest()) != FINAL_TOTAL:
        raise SystemExit("Unit 28 final bundle total mismatch")
    return suffixes, {obj["id"]: obj for obj in records}


def verify_sources(by_id: dict[str, dict[str, Any]]) -> None:
    source_raw = SOURCE.read_bytes()
    if (len(source_raw), len(source_raw.splitlines()), digest(source_raw)) != SOURCE_IDENTITY:
        raise SystemExit("Unit 28 reader identity mismatch")
    if (source_raw.count(MODEL.encode()) != 1
            or re.search(rb"\bfunktor\b|\bbola\b", source_raw, re.IGNORECASE)):
        raise SystemExit("Unit 28 provenance/terminology mismatch")
    upstream_raw = UPSTREAM.read_bytes()
    if (len(upstream_raw), len(upstream_raw.splitlines()), digest(upstream_raw)) != UPSTREAM_IDENTITY:
        raise SystemExit("frozen upstream identity mismatch")
    lines = upstream_raw.decode("utf-8").replace("\r\n", "\n").split("\n")
    start, end, size, sha = SPAN_IDENTITY
    span = ("\n".join(lines[start - 1:end]) + "\n").encode()
    if len(span) != size or digest(span) != sha:
        raise SystemExit("Unit 28 authority span mismatch")
    ids = re.findall(rb"\{[^}\n]*#(o012-rbt-l28(?:-[A-Za-z0-9-]+)?)[^}\n]*\}", source_raw)
    if tuple(item.decode() for item in ids) != ANCHORS or len(set(ids)) != 47:
        raise SystemExit("Unit 28 stable-ID order mismatch")
    source_lines = source_raw.splitlines(keepends=True)
    for ident in ANCHORS:
        unit = by_id[f"unit:{ident}"]; segment = by_id[f"segment:{ident}"]
        locator = unit["target_locator"]
        low, high = locator["line_start"], locator["line_end"]
        if (segment["target_locator"] != locator or locator["path"] != SOURCE_PATH
                or locator["file_sha256"] != SOURCE_IDENTITY[2]
                or digest(b"".join(source_lines[low - 1:high])) != locator["content_sha256"]
                or ident.encode() not in source_lines[low - 1]):
            raise SystemExit(f"Unit 28 target-locator mismatch: {ident}")
        source_locator = segment["source_locator"]
        if ident in SOURCE_RANGES:
            if (source_locator.get("commit_sha") != COMMIT
                    or (source_locator.get("line_start"), source_locator.get("line_end")) != SOURCE_RANGES[ident]
                    or source_locator.get("precision") != "exact_source_span"):
                raise SystemExit(f"Unit 28 exact source-locator mismatch: {ident}")
        elif (source_locator.get("kind") != "edition_original"
              or source_locator.get("precision") != "exact_target_span"):
            raise SystemExit(f"Unit 28 original source-locator mismatch: {ident}")
    qa = json.loads(QA_JSON.read_text(encoding="utf-8"))
    if (qa.get("status") != "PASS"
            or {item.get("finding_id") for item in qa.get("resolved_findings", [])} != RESOLVED_FINDINGS
            or any(item.get("status") != "RESOLVED_BEFORE_ADMISSION"
                   for item in qa.get("resolved_findings", []))):
        raise SystemExit("Unit 28 final QA finding closure mismatch")


def verify_closure(suffixes: dict[str, list[dict[str, Any]]],
                   by_id: dict[str, dict[str, Any]]) -> None:
    units = suffixes["units.jsonl"]; segments = suffixes["segments.jsonl"]
    if len(units) != 48 or len(segments) != 47:
        raise SystemExit("Unit 28 unit/segment cardinality mismatch")
    for obj in units + segments:
        if (obj.get("edition_unit_id", ROOT) != ROOT
                or obj.get("course_route_unit_id", ROUTE) != ROUTE
                or obj.get("model_provenance", MODEL) != MODEL):
            raise SystemExit(f"route/provenance mismatch: {obj['id']}")
    root = by_id[ROOT]; locator = root["source_locator"]
    if (root["order"] != 28 or root["rights_component_id"] != COMPOSITE_RIGHTS
            or locator.get("commit_sha") != COMMIT
            or (locator.get("line_start"), locator.get("line_end"),
                locator.get("span_bytes"), locator.get("span_sha256")) != SPAN_IDENTITY
            or root["target_locator"]["content_sha256"] != SOURCE_IDENTITY[2]):
        raise SystemExit("Unit 28 root source/rights mismatch")
    aliases = {alias: obj["id"] for obj in units for alias in obj.get("source_aliases", [])}
    if aliases != {"thm:collapse": "unit:o012-rbt-l28-thm-002"}:
        raise SystemExit("Unit 28 source alias mismatch")
    if by_id["unit:o012-rbt-l28-boundary-001"].get("next_source_line") != 6053:
        raise SystemExit("Unit 28 terminal cursor mismatch")
    rights = by_id[CUMULATIVE_RIGHTS]
    if (rights["supersedes"] != PRIOR_RIGHTS
            or rights["component_scope"] != [f"unit:o012-rbt-u{n:03d}" for n in range(1, 29)]
            or rights["license_expression"] != "CC-BY-4.0"):
        raise SystemExit("Unit 28 cumulative rights closure mismatch")
    sibling: defaultdict[str, list[int]] = defaultdict(list)
    for unit in units:
        sibling[unit["parent_id"]].append(unit["order"])
        if unit["path"][-1] != unit["id"]:
            raise SystemExit(f"Unit 28 noncanonical path: {unit['id']}")
        if unit["parent_id"].startswith("unit:") and unit["path"][:-1] != by_id[unit["parent_id"]]["path"]:
            raise SystemExit(f"Unit 28 parent-path mismatch: {unit['id']}")
    if any(len(values) != len(set(values)) for values in sibling.values()):
        raise SystemExit("Unit 28 duplicate sibling order")
    relations = suffixes["relations.jsonl"]
    proofs = [obj for obj in units if obj.get("proof_status")]
    proof_relations = [obj for obj in relations if obj["relation_type"] == "proves"]
    if len(proofs) != 4 or len(proof_relations) != 4:
        raise SystemExit("Unit 28 proof closure mismatch")
    expected_status = {1: "complete_translated_proof", 2: "complete_original_proof",
                       3: "complete_translated_proof", 4: "complete_original_proof"}
    for number, status in expected_status.items():
        if by_id[f"unit:o012-rbt-l28-proof-{number:03d}"].get("proof_status") != status:
            raise SystemExit(f"Unit 28 proof provenance mismatch: {number}")
    for n in range(1, 7):
        exercise = f"unit:o012-rbt-l28-mcheck-{n:03d}"
        solution = f"unit:o012-rbt-l28-sol-{n:03d}"
        hint = f"unit:o012-rbt-l28-hint-{n:03d}"
        if (sum(obj["relation_type"] == "solves" and obj["from_id"] == solution
                and obj["to_id"] == exercise for obj in relations) != 1
                or sum(obj["relation_type"] == "hints" and obj["from_id"] == hint
                       and obj["to_id"] == exercise for obj in relations) != 1
                or by_id[solution].get("solution_status") != "complete_checked_solution"
                or by_id[exercise]["rights_component_id"] != COMPANION_RIGHTS):
            raise SystemExit(f"Unit 28 mastery closure mismatch: {n}")
    corrections = suffixes["corrections.jsonl"]
    if ({obj["id"] for obj in corrections} != CORRECTION_IDS
            or any(obj["upstream_report_disposition"] != "not_contacted" for obj in corrections)):
        raise SystemExit("Unit 28 correction closure mismatch")
    resolved_corrections = {obj["id"] for obj in corrections if "-resolved-" in obj["id"]}
    if len(resolved_corrections) != 6:
        raise SystemExit("Unit 28 six resolved-finding correction records missing")
    terms = suffixes["terms.jsonl"]
    if ({obj["concept_id"].removeprefix("concept:") for obj in terms} != SLUGS
            or any(obj.get("terminology_status") != "unit_attested_reviewed" for obj in terms)
            or any(obj["evidence_segment_id"] not in by_id for obj in terms)):
        raise SystemExit("Unit 28 terminology closure mismatch")
    asset = by_id["asset:o012-u028-source-markdown"]
    if (asset["path"], asset["bytes"], asset["sha256"], asset["rights_component_id"]) != (
            SOURCE_PATH, SOURCE_IDENTITY[0], SOURCE_IDENTITY[2], COMPOSITE_RIGHTS):
        raise SystemExit("Unit 28 reader asset mismatch")
    expected_evidence = {
        "artifact:o012-u028-source-audit": ("qa/UNIT_028_SOURCE_AUDIT.md", 5660,
            "2b181bcd12c95210395b3aec8b866b69093d6636b89773d08d93cec41870fa4a"),
        "artifact:o012-u028-independent-review": ("qa/UNIT_028_INDEPENDENT_REVIEW.md", 6807,
            "92d81718580eded1daac0593fe2e13d7797c9ed2d8507e70fe5f7dd522fde505"),
        "artifact:o012-u028-qa": ("qa/UNIT_028_QA.json", 9792,
            "dd448f5d5d1a60f6b8e5815a1cb993946c7400f55b46d287f25a78d59f068c79"),
    }
    for ident, triple in expected_evidence.items():
        obj = by_id[ident]
        if (obj["path"], obj["bytes"], obj["sha256"]) != triple:
            raise SystemExit(f"Unit 28 evidence mismatch: {ident}")
    for ident in ("qa:o012-u028-source-integrity", "qa:o012-u028-math",
                  "qa:o012-u028-language"):
        if by_id[ident]["result"] != "passed" or by_id[ident]["unit_id"] != ROOT:
            raise SystemExit(f"Unit 28 QA event mismatch: {ident}")
    if not any(obj["id"] == "relation:precedes:o012-rbt-u027:o012-rbt-u028"
               and obj["from_id"] == "unit:o012-rbt-u027" and obj["to_id"] == ROOT
               for obj in relations):
        raise SystemExit("Unit 28 contiguous predecessor relation missing")
    combined = b"".join((BACKEND / name).read_bytes() for name in FILES)
    if any(needle in combined for needle in (
            b"artifact:o012-units-001-028-html", b"artifact:o012-units-001-028-pdf",
            b"qa:o012-units-001-028-build", b"qa:o012-units-001-028-visual")):
        raise SystemExit("premature Unit 28 build claim detected")


def main() -> int:
    suffixes, by_id = load_and_partition()
    generic = generic_module(); records = list(by_id.values())
    generic.validate_shapes(records)
    generic.validate_references(records, by_id)
    generic.validate_artifact_manifests(records, LANE)
    verify_sources(by_id); verify_closure(suffixes, by_id)
    print("Unit 028 semantic append-only backend validation: PASS")
    print(f"prefix_records={PREFIX_TOTAL[0]}")
    print(f"prefix_bytes={PREFIX_TOTAL[1]}")
    print(f"prefix_bundle_sha256={PREFIX_TOTAL[2]}")
    print("records_added=161")
    print("records_added_by_file=" + json.dumps(DELTA, sort_keys=True))
    print(f"final_records={FINAL_TOTAL[0]}")
    print(f"final_bytes={FINAL_TOTAL[1]}")
    print(f"final_bundle_sha256={FINAL_TOTAL[2]}")
    print("stable_ids=47")
    print("proof_closures=4")
    print("mastery_triples=6")
    print("source_aliases=1")
    print("resolved_findings=6")
    print("next_source_line=6053")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
