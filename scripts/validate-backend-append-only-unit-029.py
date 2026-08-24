#!/usr/bin/env python3
"""Independent fail-closed validator for the final Unit 029 semantic append."""
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
SOURCE = LANE / "source/id-ID/units/unit-029-lecture-029.md"
UPSTREAM = (LANE / "authority/upstream" /
            "AlgebraicTopology2019-b947ad2e9f9e301bfe24590a9db653bc54fa1a53" /
            "Notes.tex")
QA_JSON = LANE / "qa/UNIT_029_QA.json"
FILES = ("artifacts.jsonl", "assets.jsonl", "authority.jsonl", "concepts.jsonl",
         "corrections.jsonl", "qa.jsonl", "relations.jsonl", "rights.jsonl",
         "segments.jsonl", "terms.jsonl", "units.jsonl")
PREFIX = {
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
PREFIX_TOTAL = (4425, 4765453,
                "3a7492ee9755c85e89139bd6af84121747caa85f1f6421c7ec2e133b010a0b9f")
DELTA = {"artifacts.jsonl": 3, "assets.jsonl": 2, "authority.jsonl": 0,
         "concepts.jsonl": 7, "corrections.jsonl": 19, "qa.jsonl": 3,
         "relations.jsonl": 28, "rights.jsonl": 3, "segments.jsonl": 49,
         "terms.jsonl": 7, "units.jsonl": 50}
FINAL = {
    "artifacts.jsonl": (157, 125783, "11f677dc347348b8a91387e232b7eb18cbada0387d4eddda4f95a113ed241dc1"),
    "assets.jsonl": (32, 19939, "bd81863dd4eff456734abada1f2416727b70a5c54c7e9662a5cb2bac041884bb"),
    "authority.jsonl": (4, 2721, "f21af26912520ab34b38dff0e927ed46a546dbe5d318da0dc133e58330d0e368"),
    "concepts.jsonl": (354, 111822, "edd155b71045f574d4195af88d021c82a2c530e46fc6b61046276a783649f041"),
    "corrections.jsonl": (397, 387613, "82145855c9dec1c14f1be23bdf36394f0249798b7722c9ebd65afefd955ecfb4"),
    "qa.jsonl": (131, 73522, "10c3b5955c4c5a5f4f93d18a360705c0ee74286467d09e1549432c21b8c06c17"),
    "relations.jsonl": (504, 206282, "5a12459d1af20f6ba363f93c10104dedf714c24b8484c6f1b2a76004ddd2474f"),
    "rights.jsonl": (83, 76753, "6ab37eedf396adbd01ba4be763896d9a4926a0fc87af97d8ac2ad2022c3d35e1"),
    "segments.jsonl": (1279, 1829093, "13f59fd6db9e768c4d4b1a249bfcf86ccdb4312df5a74fadb53922266d985bdc"),
    "terms.jsonl": (347, 219627, "d16fc5166ee92ea654eb43b644dda4cb7acc59054194654b8e85b7bcdd3a1aa9"),
    "units.jsonl": (1308, 1948111, "19b50f4cee0cc968b538052ffaf87d7b2dc2199b64c44e1a12c4e4800dc99e04"),
}
FINAL_TOTAL = (4596, 5001266,
               "49c599010ebee2223225f643cd09a53bea882b8064024d5189e6e15f648195d8")
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"
COMMIT = "b947ad2e9f9e301bfe24590a9db653bc54fa1a53"
SOURCE_PATH = "source/id-ID/units/unit-029-lecture-029.md"
SOURCE_IDENTITY = (27687, 805,
                   "cfb8fa5c49593a187bed5df1d4173cc952100b18e5faa009cb8d57036c5726c4")
UPSTREAM_IDENTITY = (331447, 6368,
                     "cfe93e9dbe3e25bd96f711f59e6078ab97527682b58e1f8ad127f74357f665d7")
SPAN_IDENTITY = (6053, 6270, 11447,
                 "33c6b7bfe3216d271c6b1f9d0cb952e6ef02a5e27a57f686936e764bfc4a9233")
ROOT = "unit:o012-rbt-u029"
ROUTE = "D60-R14"
COMPANION_RIGHTS = "rights:o012-u029-companion-cc-by-4.0"
COMPOSITE_RIGHTS = "rights:o012-u029-composite-cc-by-4.0"
CUMULATIVE_RIGHTS = "rights:o012-units-001-029-composite-cc-by-4.0"
PRIOR_RIGHTS = "rights:o012-units-001-028-composite-cc-by-4.0"

ANCHORS = (
    "o012-rbt-l29-notice", "o012-rbt-l29", "o012-rbt-l29-s01",
    "o012-rbt-l29-lem-001", "o012-rbt-l29-proof-001",
    "o012-rbt-l29-audit-001", "o012-rbt-l29-s02",
    "o012-rbt-l29-fact-001", "o012-rbt-l29-proof-002",
    "o012-rbt-l29-audit-002", "o012-rbt-l29-s03",
    "o012-rbt-l29-thm-001", "o012-rbt-l29-proof-003",
    "o012-rbt-l29-cor-001", "o012-rbt-l29-proof-004",
    "o012-rbt-l29-audit-003", "o012-rbt-l29-s04",
    "o012-rbt-l29-def-001", "o012-rbt-l29-audit-004",
    "o012-rbt-l29-fig-001", "o012-rbt-l29-exa-001",
    "o012-rbt-l29-exa-002", "o012-rbt-l29-s05",
    "o012-rbt-l29-def-002", "o012-rbt-l29-exa-003",
    "o012-rbt-l29-audit-005", "o012-rbt-l29-s06",
    "o012-rbt-l29-thm-002", "o012-rbt-l29-audit-006",
    "o012-rbt-l29-mastery", "o012-rbt-l29-mcheck-001",
    "o012-rbt-l29-hint-001", "o012-rbt-l29-sol-001",
    "o012-rbt-l29-mcheck-002", "o012-rbt-l29-hint-002",
    "o012-rbt-l29-sol-002", "o012-rbt-l29-mcheck-003",
    "o012-rbt-l29-hint-003", "o012-rbt-l29-sol-003",
    "o012-rbt-l29-mcheck-004", "o012-rbt-l29-hint-004",
    "o012-rbt-l29-sol-004", "o012-rbt-l29-mcheck-005",
    "o012-rbt-l29-hint-005", "o012-rbt-l29-sol-005",
    "o012-rbt-l29-mcheck-006", "o012-rbt-l29-hint-006",
    "o012-rbt-l29-sol-006", "o012-rbt-l29-boundary-001",
)
SOURCE_RANGES = {
    "o012-rbt-l29": (6053, 6270), "o012-rbt-l29-s01": (6054, 6062),
    "o012-rbt-l29-lem-001": (6054, 6062), "o012-rbt-l29-s02": (6064, 6091),
    "o012-rbt-l29-fact-001": (6079, 6088), "o012-rbt-l29-s03": (6093, 6140),
    "o012-rbt-l29-thm-001": (6093, 6095), "o012-rbt-l29-proof-003": (6097, 6100),
    "o012-rbt-l29-cor-001": (6106, 6112), "o012-rbt-l29-s04": (6142, 6220),
    "o012-rbt-l29-def-001": (6151, 6168), "o012-rbt-l29-exa-001": (6211, 6213),
    "o012-rbt-l29-exa-002": (6217, 6220), "o012-rbt-l29-s05": (6222, 6244),
    "o012-rbt-l29-def-002": (6224, 6227), "o012-rbt-l29-s06": (6245, 6270),
    "o012-rbt-l29-thm-002": (6245, 6261),
}
SLUGS = {"cohomology-comparison-theorem", "cw-complex", "cw-pair",
         "cellular-filtration", "milnor-derived-limit-sequence",
         "eilenberg-steenrod-axioms", "strong-excision"}
CORRECTION_IDS = {f"correction:o012-u029-dossier-{n:03d}" for n in range(1, 12)} | {
    "correction:o012-u029-resolved-math-p2-001",
    "correction:o012-u029-resolved-math-p2-002",
    "correction:o012-u029-resolved-type-p2-003",
    "correction:o012-u029-resolved-reflow-p3-001",
    "correction:o012-u029-resolved-cw-p3-002",
    "correction:o012-u029-resolved-lang-p3-003",
    "correction:o012-u029-resolved-term-p3-004",
    "correction:o012-u029-resolved-qa-p3-005",
}
RESOLVED_FINDINGS = {"UNIT029-MATH-P2-001", "UNIT029-MATH-P2-002",
                     "UNIT029-TYPE-P2-003", "UNIT029-REFLOW-P3-001",
                     "UNIT029-CW-P3-002", "UNIT029-LANG-P3-003",
                     "UNIT029-TERM-P3-004", "UNIT029-QA-P3-005"}


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canon(obj: dict[str, Any]) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8") + b"\n"


def generic_module():
    path = LANE / "scripts/validate-backend.py"
    spec = importlib.util.spec_from_file_location("o012_generic_u029_validator", path)
    if spec is None or spec.loader is None:
        raise SystemExit("cannot load generic backend validator")
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


def expected_ids() -> dict[str, set[str]]:
    relations = {
        "relation:adapts:o012-rbt-u029:edition",
        "relation:precedes:o012-rbt-u028:o012-rbt-u029",
        "relation:precedes:o012-rbt-l29:mastery",
        "relation:boundary:o012-u029", "relation:route:d60-r14:o012-rbt-u029",
        "relation:depends-on:o012-rbt-l29-s01:l28-s05",
        "relation:depends-on:o012-rbt-l29-fact-001:l28-thm-002",
        "relation:depends-on:o012-rbt-l29-thm-001:fact-001",
        "relation:depends-on:o012-rbt-l29-cor-001:thm-001",
        "relation:depends-on:o012-rbt-l29-def-002:def-001",
        "relation:depends-on:o012-rbt-l29-thm-002:def-002",
        "relation:reflows:o012-rbt-l29-fig-001:diagram-asset",
    }
    relations |= {f"relation:proves:o012-rbt-l29-proof-{n:03d}:closure"
                  for n in range(1, 5)}
    relations |= {f"relation:solves:l29-sol-{n:03d}:l29-mcheck-{n:03d}"
                  for n in range(1, 7)}
    relations |= {f"relation:hints:l29-hint-{n:03d}:l29-mcheck-{n:03d}"
                  for n in range(1, 7)}
    return {
        "artifacts.jsonl": {"artifact:o012-u029-source-audit",
                            "artifact:o012-u029-independent-review",
                            "artifact:o012-u029-qa"},
        "assets.jsonl": {"asset:o012-u029-source-markdown",
                         "asset:o012-u029-semantic-diagram-layer"},
        "authority.jsonl": set(),
        "concepts.jsonl": {f"concept:{slug}" for slug in SLUGS},
        "corrections.jsonl": CORRECTION_IDS,
        "qa.jsonl": {"qa:o012-u029-source-integrity", "qa:o012-u029-math",
                      "qa:o012-u029-language"},
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
            raise SystemExit(f"{name}: final Unit 29 identity mismatch")
        prefix_count, prefix_bytes, prefix_sha = PREFIX[name]
        prefix = raw[:prefix_bytes]
        if (len(prefix.splitlines()), len(prefix), digest(prefix)) != (
                prefix_count, prefix_bytes, prefix_sha):
            raise SystemExit(f"{name}: Unit 28 byte prefix mismatch")
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
            raise SystemExit(f"{name}: Unit 29 suffix ID/order/count mismatch")
        for obj in prefix_objs + suffix_objs:
            if obj["id"] in ids:
                raise SystemExit(f"global duplicate ID: {obj['id']}")
            ids.add(obj["id"])
        suffixes[name] = suffix_objs; records.extend(prefix_objs + suffix_objs)
        prefix_bundle.update(name.encode()); prefix_bundle.update(b"\0"); prefix_bundle.update(prefix)
        bundle.update(name.encode()); bundle.update(b"\0"); bundle.update(raw)
    if (sum(PREFIX[name][0] for name in FILES), sum(PREFIX[name][1] for name in FILES),
        prefix_bundle.hexdigest()) != PREFIX_TOTAL:
        raise SystemExit("Unit 28 prefix total mismatch")
    if (len(records), sum(FINAL[name][1] for name in FILES), bundle.hexdigest()) != FINAL_TOTAL:
        raise SystemExit("Unit 29 final bundle total mismatch")
    return suffixes, {obj["id"]: obj for obj in records}


def verify_sources(by_id: dict[str, dict[str, Any]]) -> None:
    source_raw = SOURCE.read_bytes()
    if (len(source_raw), len(source_raw.splitlines()), digest(source_raw)) != SOURCE_IDENTITY:
        raise SystemExit("Unit 29 reader identity mismatch")
    if (source_raw.count(MODEL.encode()) != 1
            or re.search(rb"\b(funktor|funktorial|naturalitas|bola|perpanjangan)\b|bujur sangkar",
                         source_raw, re.IGNORECASE)):
        raise SystemExit("Unit 29 provenance/terminology mismatch")
    upstream_raw = UPSTREAM.read_bytes()
    if (len(upstream_raw), len(upstream_raw.splitlines()), digest(upstream_raw)) != UPSTREAM_IDENTITY:
        raise SystemExit("frozen upstream identity mismatch")
    lines = upstream_raw.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n").split("\n")
    start, end, size, sha = SPAN_IDENTITY
    span = ("\n".join(lines[start - 1:end]) + "\n").encode()
    if len(span) != size or digest(span) != sha or "\\lecturenum{30}" not in lines[end]:
        raise SystemExit("Unit 29 authority span/cursor mismatch")
    ids = re.findall(rb"\{[^}\n]*#(o012-rbt-l29(?:-[A-Za-z0-9-]+)?)[^}\n]*\}", source_raw)
    if tuple(item.decode() for item in ids) != ANCHORS or len(ids) != 49 or len(set(ids)) != 49:
        raise SystemExit("Unit 29 stable-ID order mismatch")
    source_lines = source_raw.splitlines(keepends=True)
    for ident in ANCHORS:
        unit = by_id[f"unit:{ident}"]; segment = by_id[f"segment:{ident}"]
        locator = unit["target_locator"]
        low, high = locator["line_start"], locator["line_end"]
        if (segment["target_locator"] != locator or locator["path"] != SOURCE_PATH
                or locator["file_sha256"] != SOURCE_IDENTITY[2]
                or digest(b"".join(source_lines[low - 1:high])) != locator["content_sha256"]
                or ident.encode() not in source_lines[low - 1]):
            raise SystemExit(f"Unit 29 target-locator mismatch: {ident}")
        source_locator = segment["source_locator"]
        if ident in SOURCE_RANGES:
            if (source_locator.get("commit_sha") != COMMIT
                    or (source_locator.get("line_start"), source_locator.get("line_end")) != SOURCE_RANGES[ident]
                    or source_locator.get("precision") != "exact_source_span"):
                raise SystemExit(f"Unit 29 exact source-locator mismatch: {ident}")
        elif (source_locator.get("kind") != "edition_original"
              or source_locator.get("precision") != "exact_target_span"):
            raise SystemExit(f"Unit 29 original source-locator mismatch: {ident}")
    qa = json.loads(QA_JSON.read_text(encoding="utf-8"))
    if (qa.get("status") != "PASS" or qa.get("unit", {}).get("stable_ids") != 49
            or qa.get("unit", {}).get("identified_headings") != 9
            or {item.get("finding_id") for item in qa.get("resolved_findings", [])} != RESOLVED_FINDINGS
            or any(item.get("status") != "RESOLVED_BEFORE_ADMISSION"
                   for item in qa.get("resolved_findings", []))):
        raise SystemExit("Unit 29 final QA finding/census closure mismatch")


def verify_closure(suffixes: dict[str, list[dict[str, Any]]],
                   by_id: dict[str, dict[str, Any]]) -> None:
    units = suffixes["units.jsonl"]; segments = suffixes["segments.jsonl"]
    if len(units) != 50 or len(segments) != 49:
        raise SystemExit("Unit 29 unit/segment cardinality mismatch")
    for obj in units + segments:
        if (obj.get("edition_unit_id", ROOT) != ROOT
                or obj.get("course_route_unit_id", ROUTE) != ROUTE
                or obj.get("model_provenance", MODEL) != MODEL):
            raise SystemExit(f"route/provenance mismatch: {obj['id']}")
    root = by_id[ROOT]; locator = root["source_locator"]
    if (root["order"] != 29 or root["rights_component_id"] != COMPOSITE_RIGHTS
            or locator.get("commit_sha") != COMMIT
            or (locator.get("line_start"), locator.get("line_end"),
                locator.get("span_bytes"), locator.get("span_sha256")) != SPAN_IDENTITY
            or root["target_locator"]["content_sha256"] != SOURCE_IDENTITY[2]):
        raise SystemExit("Unit 29 root source/rights mismatch")
    aliases = {alias: obj["id"] for obj in units for alias in obj.get("source_aliases", [])}
    if aliases != {"eq:comparison_iso_simplicial_singular": "unit:o012-rbt-l29-cor-001"}:
        raise SystemExit("Unit 29 source alias mismatch")
    if by_id["unit:o012-rbt-l29-boundary-001"].get("next_source_line") != 6271:
        raise SystemExit("Unit 29 terminal cursor mismatch")
    rights = by_id[CUMULATIVE_RIGHTS]
    if (rights["supersedes"] != PRIOR_RIGHTS
            or rights["component_scope"] != [f"unit:o012-rbt-u{n:03d}" for n in range(1, 30)]
            or rights["license_expression"] != "CC-BY-4.0"):
        raise SystemExit("Unit 29 cumulative rights closure mismatch")
    sibling: defaultdict[str, list[int]] = defaultdict(list)
    for unit in units:
        sibling[unit["parent_id"]].append(unit["order"])
        if unit["path"][-1] != unit["id"]:
            raise SystemExit(f"Unit 29 noncanonical path: {unit['id']}")
        if unit["parent_id"].startswith("unit:") and unit["path"][:-1] != by_id[unit["parent_id"]]["path"]:
            raise SystemExit(f"Unit 29 parent-path mismatch: {unit['id']}")
    if any(len(values) != len(set(values)) for values in sibling.values()):
        raise SystemExit("Unit 29 duplicate sibling order")
    relations = suffixes["relations.jsonl"]
    proofs = [obj for obj in units if obj.get("proof_status")]
    proof_relations = [obj for obj in relations if obj["relation_type"] == "proves"]
    if len(proofs) != 4 or len(proof_relations) != 4:
        raise SystemExit("Unit 29 proof closure mismatch")
    expected_status = {1: "complete_original_proof", 2: "complete_original_proof",
                       3: "complete_translated_proof", 4: "complete_original_proof"}
    for number, status in expected_status.items():
        if by_id[f"unit:o012-rbt-l29-proof-{number:03d}"].get("proof_status") != status:
            raise SystemExit(f"Unit 29 proof provenance mismatch: {number}")
    for n in range(1, 7):
        exercise = f"unit:o012-rbt-l29-mcheck-{n:03d}"
        solution = f"unit:o012-rbt-l29-sol-{n:03d}"
        hint = f"unit:o012-rbt-l29-hint-{n:03d}"
        if (sum(obj["relation_type"] == "solves" and obj["from_id"] == solution
                and obj["to_id"] == exercise for obj in relations) != 1
                or sum(obj["relation_type"] == "hints" and obj["from_id"] == hint
                       and obj["to_id"] == exercise for obj in relations) != 1
                or by_id[solution].get("solution_status") != "complete_checked_solution"
                or by_id[exercise]["rights_component_id"] != COMPANION_RIGHTS):
            raise SystemExit(f"Unit 29 mastery closure mismatch: {n}")
    corrections = suffixes["corrections.jsonl"]
    if ({obj["id"] for obj in corrections} != CORRECTION_IDS
            or any(obj["upstream_report_disposition"] != "not_contacted" for obj in corrections)):
        raise SystemExit("Unit 29 correction closure mismatch")
    resolved_corrections = {obj["id"] for obj in corrections if "-resolved-" in obj["id"]}
    if len(resolved_corrections) != 8:
        raise SystemExit("Unit 29 eight resolved-finding correction records missing")
    terms = suffixes["terms.jsonl"]
    if ({obj["concept_id"].removeprefix("concept:") for obj in terms} != SLUGS
            or any(obj.get("terminology_status") != "unit_attested_reviewed" for obj in terms)
            or any(obj["evidence_segment_id"] not in by_id for obj in terms)):
        raise SystemExit("Unit 29 terminology closure mismatch")
    asset = by_id["asset:o012-u029-source-markdown"]
    if (asset["path"], asset["bytes"], asset["sha256"], asset["rights_component_id"]) != (
            SOURCE_PATH, SOURCE_IDENTITY[0], SOURCE_IDENTITY[2], COMPOSITE_RIGHTS):
        raise SystemExit("Unit 29 reader asset mismatch")
    diagram = by_id["asset:o012-u029-semantic-diagram-layer"]
    if (diagram.get("source_format_counts") != {"tikz": 1, "xypic": 4}
            or len(diagram.get("semantic_unit_ids", [])) != 4
            or diagram.get("sha256") != SOURCE_IDENTITY[2]):
        raise SystemExit("Unit 29 semantic diagram asset mismatch")
    expected_evidence = {
        "artifact:o012-u029-source-audit": ("qa/UNIT_029_SOURCE_AUDIT.md", 5738,
            "6b3e96ca5a7d24a4f8182c46f02e99194c9538ca534b4b550ea23b666ad89afb"),
        "artifact:o012-u029-independent-review": ("qa/UNIT_029_INDEPENDENT_REVIEW.md", 8535,
            "873c21354acc83050e13f7236b361f29523b91d4907d9b0046ee061f7723547c"),
        "artifact:o012-u029-qa": ("qa/UNIT_029_QA.json", 11192,
            "66f5709282d890e24a20756b69d287305497011c8f6e39d7108a30d5b4b1ffd9"),
    }
    for ident, triple in expected_evidence.items():
        obj = by_id[ident]
        if (obj["path"], obj["bytes"], obj["sha256"]) != triple:
            raise SystemExit(f"Unit 29 evidence mismatch: {ident}")
        raw = (LANE / triple[0]).read_bytes()
        if (len(raw), digest(raw)) != (triple[1], triple[2]):
            raise SystemExit(f"Unit 29 live evidence mismatch: {ident}")
    for ident in ("qa:o012-u029-source-integrity", "qa:o012-u029-math",
                  "qa:o012-u029-language"):
        if by_id[ident]["result"] != "passed" or by_id[ident]["unit_id"] != ROOT:
            raise SystemExit(f"Unit 29 QA event mismatch: {ident}")
    if not any(obj["id"] == "relation:precedes:o012-rbt-u028:o012-rbt-u029"
               and obj["from_id"] == "unit:o012-rbt-u028" and obj["to_id"] == ROOT
               for obj in relations):
        raise SystemExit("Unit 29 contiguous predecessor relation missing")
    combined = b"".join((BACKEND / name).read_bytes() for name in FILES)
    if any(needle in combined for needle in (
            b"artifact:o012-units-001-029-html", b"artifact:o012-units-001-029-pdf",
            b"qa:o012-units-001-029-build", b"qa:o012-units-001-029-visual")):
        raise SystemExit("premature Unit 29 build claim detected")


def main() -> int:
    suffixes, by_id = load_and_partition()
    generic = generic_module(); records = list(by_id.values())
    generic.validate_shapes(records)
    generic.validate_references(records, by_id)
    generic.validate_artifact_manifests(records, LANE)
    verify_sources(by_id); verify_closure(suffixes, by_id)
    print("Unit 029 semantic append-only backend validation: PASS")
    print(f"prefix_records={PREFIX_TOTAL[0]}")
    print(f"prefix_bytes={PREFIX_TOTAL[1]}")
    print(f"prefix_bundle_sha256={PREFIX_TOTAL[2]}")
    print("records_added=171")
    print("records_added_by_file=" + json.dumps(DELTA, sort_keys=True))
    print(f"final_records={FINAL_TOTAL[0]}")
    print(f"final_bytes={FINAL_TOTAL[1]}")
    print(f"final_bundle_sha256={FINAL_TOTAL[2]}")
    print("stable_ids=49")
    print("proof_closures=4")
    print("mastery_triples=6")
    print("source_aliases=1")
    print("resolved_findings=8")
    print("next_source_line=6271")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
