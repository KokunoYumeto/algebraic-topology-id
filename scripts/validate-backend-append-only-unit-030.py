#!/usr/bin/env python3
"""Independent fail-closed validator for the final Unit 030 semantic append."""
from __future__ import annotations

import hashlib
import importlib.util
import csv
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

LANE = Path(__file__).resolve().parents[1]
BACKEND = LANE / "backend"
SOURCE = LANE / "source/id-ID/units/unit-030-lecture-030.md"
UPSTREAM = (LANE / "authority/upstream" /
            "AlgebraicTopology2019-b947ad2e9f9e301bfe24590a9db653bc54fa1a53" /
            "Notes.tex")
QA_JSON = LANE / "qa/UNIT_030_QA.json"
ADVERSE_LEDGER = LANE / "00_control/ADVERSE_LEDGER.csv"
TERMINOLOGY = LANE / "00_control/TERMINOLOGY.csv"
FILES = ("artifacts.jsonl", "assets.jsonl", "authority.jsonl", "concepts.jsonl",
         "corrections.jsonl", "qa.jsonl", "relations.jsonl", "rights.jsonl",
         "segments.jsonl", "terms.jsonl", "units.jsonl")
PREFIX = {
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
PREFIX_TOTAL = (4596, 5001266,
                "49c599010ebee2223225f643cd09a53bea882b8064024d5189e6e15f648195d8")
DELTA = {"artifacts.jsonl": 3, "assets.jsonl": 2, "authority.jsonl": 0,
         "concepts.jsonl": 10, "corrections.jsonl": 10, "qa.jsonl": 3,
         "relations.jsonl": 29, "rights.jsonl": 3, "segments.jsonl": 47,
         "terms.jsonl": 10, "units.jsonl": 48}
FINAL = {
    "artifacts.jsonl": (160, 128377, "dcafca44e0fdd9daea5534f9cb6e12ddc85d66e83657cf7905f0c76287d99356"),
    "assets.jsonl": (34, 21271, "70623b74c22df743708785dd6a213d8086dd4280db983ea14b8f08075b3e8ee6"),
    "authority.jsonl": (4, 2721, "f21af26912520ab34b38dff0e927ed46a546dbe5d318da0dc133e58330d0e368"),
    "concepts.jsonl": (364, 114998, "0ba79f3eb7f33775e2fc1e9897de40652522ebb426688617521f226cf5ee159b"),
    "corrections.jsonl": (407, 397287, "39c7fbc05989e947f4de409ef43b50f55534fecb04d6c662501401c3e295d0d8"),
    "qa.jsonl": (134, 75118, "2cdfe9c1a159e2d6b1c80e158b16a991814983f07d704c30776c2ccc54108706"),
    "relations.jsonl": (533, 218443, "cc56f5be615b567baf381505a883b6dd2344f8eaf1318f3f0ec4f5b4d70c418e"),
    "rights.jsonl": (86, 79588, "2540e545302261e342f8a41211295e7c435e870ad52e267485d4a66f5b439d0e"),
    "segments.jsonl": (1326, 1912371, "054699f1e9d902de23f5dff26d3ecee7b7e1da502fb971468bb17975c7ca65eb"),
    "terms.jsonl": (357, 226725, "27c19bbacd1fd21fc371b29c64cf7e3b1f37bae6472e3670697830a98279c67f"),
    "units.jsonl": (1356, 2036780, "53b5f8d6a688a71bc7f38f80bda670141109b974742dec7e9428ad43de0f495e"),
}
FINAL_TOTAL = (4761, 5213679,
               "51b8c7f611560b9b5e88e97b3a943b54e0eb687c703f0cd34c1a3d164e4fb920")
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"
COMMIT = "b947ad2e9f9e301bfe24590a9db653bc54fa1a53"
SOURCE_PATH = "source/id-ID/units/unit-030-lecture-030.md"
SOURCE_IDENTITY = (23008, 729,
                   "88da8cf71d0f81328bdd65b0dea7d54c48655ed8836e230eaed821796b61b08d")
UPSTREAM_IDENTITY = (331447, 6368,
                     "cfe93e9dbe3e25bd96f711f59e6078ab97527682b58e1f8ad127f74357f665d7")
SPAN_IDENTITY = (6271, 6368, 8290,
                 "c522b5ec0ba7d4c938be6588a070be648263d841e1db4f9905c9b388619b64b1")
AUDIT_IDENTITY = (7214, 128,
                  "177c4306e5db636e0294e85278904c186099d069f209474a472d2615b0d5a4cf")
REVIEW_IDENTITY = (8406, 148,
                   "58db70bbd6538961e8bfc0c809d00b7b539115147b2826dc46d97e5b77ba712e")
QA_IDENTITY = (8378, 233,
               "bef6fe6704084ac02386bb477b7b0082e02921d3d722955e1366e7d0b9247753")
ADVERSE_IDENTITY = (127715, 408,
                    "30345e976fa973343e285295695454a873b8692e70f415dc7c3d009d0ca73375")
TERMINOLOGY_IDENTITY = (42186, 366,
                        "234f984b06a1a0f55679a1f0f283bd5592cb7b96e696c64ca667bc62fcd4258c")
ROOT = "unit:o012-rbt-u030"
ROUTE = "D60-R14"
COMPANION_RIGHTS = "rights:o012-u030-companion-cc-by-4.0"
COMPOSITE_RIGHTS = "rights:o012-u030-composite-cc-by-4.0"
CUMULATIVE_RIGHTS = "rights:o012-units-001-030-composite-cc-by-4.0"
PRIOR_RIGHTS = "rights:o012-units-001-029-composite-cc-by-4.0"

ANCHORS = (
    "o012-rbt-l30-notice", "o012-rbt-l30", "o012-rbt-l30-s01",
    "o012-rbt-l30-s02", "o012-rbt-l30-aside-001",
    "o012-rbt-l30-def-001", "o012-rbt-l30-thm-001",
    "o012-rbt-l30-proof-001", "o012-rbt-l30-fig-001",
    "o012-rbt-l30-audit-001", "o012-rbt-l30-rem-001",
    "o012-rbt-l30-s03", "o012-rbt-l30-aside-002",
    "o012-rbt-l30-thm-002", "o012-rbt-l30-proof-002",
    "o012-rbt-l30-audit-002", "o012-rbt-l30-s04",
    "o012-rbt-l30-aside-003", "o012-rbt-l30-thm-003",
    "o012-rbt-l30-def-002", "o012-rbt-l30-prop-001",
    "o012-rbt-l30-lem-001", "o012-rbt-l30-aside-004",
    "o012-rbt-l30-cor-001", "o012-rbt-l30-proof-003",
    "o012-rbt-l30-proof-004", "o012-rbt-l30-audit-003",
    "o012-rbt-l30-mastery", "o012-rbt-l30-mcheck-001",
    "o012-rbt-l30-hint-001", "o012-rbt-l30-sol-001",
    "o012-rbt-l30-mcheck-002", "o012-rbt-l30-hint-002",
    "o012-rbt-l30-sol-002", "o012-rbt-l30-mcheck-003",
    "o012-rbt-l30-hint-003", "o012-rbt-l30-sol-003",
    "o012-rbt-l30-mcheck-004", "o012-rbt-l30-hint-004",
    "o012-rbt-l30-sol-004", "o012-rbt-l30-mcheck-005",
    "o012-rbt-l30-hint-005", "o012-rbt-l30-sol-005",
    "o012-rbt-l30-mcheck-006", "o012-rbt-l30-hint-006",
    "o012-rbt-l30-sol-006", "o012-rbt-l30-boundary-001",
)
SOURCE_RANGES = {
    "o012-rbt-l30": (6271, 6368), "o012-rbt-l30-s01": (6271, 6271),
    "o012-rbt-l30-s02": (6273, 6306), "o012-rbt-l30-aside-001": (6273, 6273),
    "o012-rbt-l30-def-001": (6273, 6273), "o012-rbt-l30-thm-001": (6275, 6277),
    "o012-rbt-l30-proof-001": (6279, 6302), "o012-rbt-l30-rem-001": (6304, 6306),
    "o012-rbt-l30-s03": (6308, 6316), "o012-rbt-l30-aside-002": (6308, 6308),
    "o012-rbt-l30-thm-002": (6310, 6312), "o012-rbt-l30-proof-002": (6314, 6316),
    "o012-rbt-l30-s04": (6318, 6365), "o012-rbt-l30-aside-003": (6318, 6318),
    "o012-rbt-l30-thm-003": (6320, 6322), "o012-rbt-l30-def-002": (6327, 6329),
    "o012-rbt-l30-prop-001": (6331, 6338), "o012-rbt-l30-lem-001": (6340, 6342),
    "o012-rbt-l30-aside-004": (6344, 6344), "o012-rbt-l30-cor-001": (6346, 6348),
    "o012-rbt-l30-proof-004": (6350, 6365),
}
SLUGS = {"free-self-map", "brouwer-fixed-point-theorem", "real-closed-field",
         "fundamental-theorem-of-algebra", "tangent-vector-field", "dot-product",
         "degree-of-a-map", "antipodal-map", "monoid-homomorphism",
         "hairy-sphere-theorem"}
CORRECTION_IDS = {f"correction:o012-u030-adv-{n:04d}" for n in range(398, 408)}
RESOLVED_FINDINGS = {"UNIT030-ED-P2-001", "UNIT030-QA-P3-002"}


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canon(obj: dict[str, Any]) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8") + b"\n"


def generic_module():
    path = LANE / "scripts/validate-backend.py"
    spec = importlib.util.spec_from_file_location("o012_generic_u030_validator", path)
    if spec is None or spec.loader is None:
        raise SystemExit("cannot load generic backend validator")
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


def expected_ids() -> dict[str, set[str]]:
    relations = {
        "relation:adapts:o012-rbt-u030:edition",
        "relation:precedes:o012-rbt-u029:o012-rbt-u030",
        "relation:precedes:o012-rbt-l30:mastery",
        "relation:boundary:o012-u030", "relation:route:d60-r14:o012-rbt-u030",
        "relation:depends-on:o012-rbt-l30-s02:l12-retract",
        "relation:depends-on:o012-rbt-l30-proof-001:l25-reduced",
        "relation:depends-on:o012-rbt-l30-proof-002:l10-pi1",
        "relation:depends-on:o012-rbt-l30-def-002:l25-reduced",
        "relation:depends-on:o012-rbt-l30-thm-003:l29-axioms",
        "relation:depends-on:o012-rbt-l30-cor-001:lem-001",
        "relation:depends-on:o012-rbt-l30-proof-004:cor-001",
        "relation:reflows:o012-rbt-l30-fig-001:diagram-asset",
    }
    relations |= {f"relation:proves:o012-rbt-l30-proof-{n:03d}:closure"
                  for n in range(1, 5)}
    relations |= {f"relation:solves:l30-sol-{n:03d}:l30-mcheck-{n:03d}"
                  for n in range(1, 7)}
    relations |= {f"relation:hints:l30-hint-{n:03d}:l30-mcheck-{n:03d}"
                  for n in range(1, 7)}
    return {
        "artifacts.jsonl": {"artifact:o012-u030-source-audit",
                            "artifact:o012-u030-independent-review",
                            "artifact:o012-u030-qa"},
        "assets.jsonl": {"asset:o012-u030-source-markdown",
                         "asset:o012-u030-semantic-diagram-layer"},
        "authority.jsonl": set(),
        "concepts.jsonl": {f"concept:{slug}" for slug in SLUGS},
        "corrections.jsonl": CORRECTION_IDS,
        "qa.jsonl": {"qa:o012-u030-source-integrity", "qa:o012-u030-math",
                      "qa:o012-u030-language"},
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
            raise SystemExit(f"{name}: final Unit 30 identity mismatch")
        prefix_count, prefix_bytes, prefix_sha = PREFIX[name]
        prefix = raw[:prefix_bytes]
        if (len(prefix.splitlines()), len(prefix), digest(prefix)) != (
                prefix_count, prefix_bytes, prefix_sha):
            raise SystemExit(f"{name}: Unit 29 byte prefix mismatch")
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
            raise SystemExit(f"{name}: Unit 30 suffix ID/order/count mismatch")
        for obj in prefix_objs + suffix_objs:
            if obj["id"] in ids:
                raise SystemExit(f"global duplicate ID: {obj['id']}")
            ids.add(obj["id"])
        suffixes[name] = suffix_objs; records.extend(prefix_objs + suffix_objs)
        prefix_bundle.update(name.encode()); prefix_bundle.update(b"\0"); prefix_bundle.update(prefix)
        bundle.update(name.encode()); bundle.update(b"\0"); bundle.update(raw)
    if (sum(PREFIX[name][0] for name in FILES), sum(PREFIX[name][1] for name in FILES),
        prefix_bundle.hexdigest()) != PREFIX_TOTAL:
        raise SystemExit("Unit 29 prefix total mismatch")
    if (len(records), sum(FINAL[name][1] for name in FILES), bundle.hexdigest()) != FINAL_TOTAL:
        raise SystemExit("Unit 30 final bundle total mismatch")
    return suffixes, {obj["id"]: obj for obj in records}


def verify_sources(by_id: dict[str, dict[str, Any]]) -> None:
    source_raw = SOURCE.read_bytes()
    if (len(source_raw), len(source_raw.splitlines()), digest(source_raw)) != SOURCE_IDENTITY:
        raise SystemExit("Unit 30 reader identity mismatch")
    if (source_raw.count(MODEL.encode()) != 1
            or re.search(rb"\b(funktor|funktorial|naturalitas|bola|perpanjangan)\b|bujur sangkar",
                         source_raw, re.IGNORECASE)):
        raise SystemExit("Unit 30 provenance/terminology mismatch")
    upstream_raw = UPSTREAM.read_bytes()
    if (len(upstream_raw), len(upstream_raw.splitlines()), digest(upstream_raw)) != UPSTREAM_IDENTITY:
        raise SystemExit("frozen upstream identity mismatch")
    lines = upstream_raw.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n").split("\n")
    start, end, size, sha = SPAN_IDENTITY
    span = ("\n".join(lines[start - 1:end]) + "\n").encode()
    if (len(span) != size or digest(span) != sha
            or "\\lecturenum{30}" not in lines[start - 1]
            or lines[end - 1].strip() != "\\end{document}"
            or len(lines) != end + 1):
        raise SystemExit("Unit 30 authority span/cursor mismatch")
    ids = re.findall(rb"\{[^}\n]*#(o012-rbt-l30(?:-[A-Za-z0-9-]+)?)[^}\n]*\}", source_raw)
    heading_ids = re.findall(
        rb"(?m)^#{1,6}[^\n]*\{[^}\n]*#(o012-rbt-l30(?:-[A-Za-z0-9-]+)?)[^}\n]*\}\s*$",
        source_raw)
    fenced_ids = re.findall(
        rb"(?m)^:::[^\n]*\{[^}\n]*#(o012-rbt-l30(?:-[A-Za-z0-9-]+)?)[^}\n]*\}\s*$",
        source_raw)
    if (tuple(item.decode() for item in ids) != ANCHORS
            or len(ids) != 47 or len(set(ids)) != 47
            or len(heading_ids) != 7 or len(fenced_ids) != 40
            or set(ids) != set(heading_ids) | set(fenced_ids)
            or set(heading_ids) & set(fenced_ids)):
        raise SystemExit("Unit 30 stable-ID order mismatch")
    source_lines = source_raw.splitlines(keepends=True)
    for ident in ANCHORS:
        unit = by_id[f"unit:{ident}"]; segment = by_id[f"segment:{ident}"]
        locator = unit["target_locator"]
        low, high = locator["line_start"], locator["line_end"]
        if (segment["target_locator"] != locator or locator["path"] != SOURCE_PATH
                or locator["file_sha256"] != SOURCE_IDENTITY[2]
                or digest(b"".join(source_lines[low - 1:high])) != locator["content_sha256"]
                or ident.encode() not in source_lines[low - 1]):
            raise SystemExit(f"Unit 30 target-locator mismatch: {ident}")
        source_locator = segment["source_locator"]
        if ident in SOURCE_RANGES:
            if (source_locator.get("commit_sha") != COMMIT
                    or (source_locator.get("line_start"), source_locator.get("line_end")) != SOURCE_RANGES[ident]
                    or source_locator.get("precision") != "exact_source_span"):
                raise SystemExit(f"Unit 30 exact source-locator mismatch: {ident}")
        elif (source_locator.get("kind") != "edition_original"
              or source_locator.get("precision") != "exact_target_span"):
            raise SystemExit(f"Unit 30 original source-locator mismatch: {ident}")
    qa_raw = QA_JSON.read_bytes()
    if (len(qa_raw), len(qa_raw.splitlines()), digest(qa_raw)) != QA_IDENTITY:
        raise SystemExit("Unit 30 final QA identity mismatch")
    qa = json.loads(qa_raw.decode("utf-8"))
    review_control = qa.get("controls", {}).get("independent_review", {})
    audit_control = qa.get("controls", {}).get("source_audit", {})
    if (qa.get("status") != "PASS" or qa.get("unit", {}).get("stable_ids") != 47
            or qa.get("unit", {}).get("identified_headings") != 7
            or qa.get("unit", {}).get("fenced_semantic_objects") != 40
            or qa.get("rendering", {}).get("reader_ids_preserved") != 47
            or qa.get("rendering", {}).get("missing_reader_ids") != 0
            or qa.get("rendering", {}).get("duplicate_dom_ids") != 0
            or qa.get("source", {}).get("terminal_eof") is not True
            or qa.get("source", {}).get("next_nominal_line") != 6369
            or (audit_control.get("bytes"), audit_control.get("lines"),
                audit_control.get("sha256")) != AUDIT_IDENTITY
            or (review_control.get("bytes"), review_control.get("lines"),
                review_control.get("sha256")) != REVIEW_IDENTITY
            or {item.get("finding_id") for item in qa.get("resolved_findings", [])} != RESOLVED_FINDINGS
            or any(item.get("status") != "RESOLVED_BEFORE_ADMISSION"
                   for item in qa.get("resolved_findings", []))):
        raise SystemExit("Unit 30 final QA finding/census closure mismatch")


def verify_controls(corrections: list[dict[str, Any]],
                    terms: list[dict[str, Any]]) -> None:
    adverse_raw = ADVERSE_LEDGER.read_bytes()
    terminology_raw = TERMINOLOGY.read_bytes()
    if ((len(adverse_raw), len(adverse_raw.splitlines()), digest(adverse_raw))
            != ADVERSE_IDENTITY):
        raise SystemExit("Unit 30 adverse-ledger identity mismatch")
    if ((len(terminology_raw), len(terminology_raw.splitlines()), digest(terminology_raw))
            != TERMINOLOGY_IDENTITY):
        raise SystemExit("Unit 30 terminology-control identity mismatch")
    with ADVERSE_LEDGER.open(encoding="utf-8", newline="") as handle:
        adverse_rows = list(csv.DictReader(handle))
    with TERMINOLOGY.open(encoding="utf-8", newline="") as handle:
        terminology_rows = list(csv.DictReader(handle))
    adverse = {row["event_id"]: row for row in adverse_rows}
    terminology = {row["term_id"]: row for row in terminology_rows}
    expected_adverse = {f"O012-ADV-{number:04d}" for number in range(398, 408)}
    expected_terms = {f"O012-TERM-{number:04d}" for number in range(356, 366)}
    if (len(adverse_rows) != 407 or adverse_rows[-1]["event_id"] != "O012-ADV-0407"
            or not expected_adverse <= adverse.keys()):
        raise SystemExit("Unit 30 adverse-ledger endpoint/coverage mismatch")
    if (len(terminology_rows) != 365
            or terminology_rows[-1]["term_id"] != "O012-TERM-0365"
            or not expected_terms <= terminology.keys()):
        raise SystemExit("Unit 30 terminology endpoint/coverage mismatch")
    if ({obj.get("adverse_ledger_id") for obj in corrections} != expected_adverse
            or any(obj.get("unit_id") != ROOT
                   or obj.get("upstream_report_disposition") != "not_contacted"
                   for obj in corrections)):
        raise SystemExit("Unit 30 adverse-ledger correction mapping mismatch")
    for obj in terms:
        control_id = obj.get("terminology_control_id")
        row = terminology.get(control_id)
        if (control_id not in expected_terms or row is None
                or row["status"] != "admitted"
                or obj.get("terminology_status") != "admitted"
                or obj.get("source_term") != row["source_term"]
                or obj.get("preferred") != row["id_ID"]):
            raise SystemExit(f"Unit 30 terminology mapping mismatch: {obj['id']}")


def verify_closure(suffixes: dict[str, list[dict[str, Any]]],
                   by_id: dict[str, dict[str, Any]]) -> None:
    units = suffixes["units.jsonl"]; segments = suffixes["segments.jsonl"]
    if len(units) != 48 or len(segments) != 47:
        raise SystemExit("Unit 30 unit/segment cardinality mismatch")
    for obj in units + segments:
        if (obj.get("edition_unit_id", ROOT) != ROOT
                or obj.get("course_route_unit_id", ROUTE) != ROUTE
                or obj.get("model_provenance", MODEL) != MODEL):
            raise SystemExit(f"route/provenance mismatch: {obj['id']}")
    root = by_id[ROOT]; locator = root["source_locator"]
    if (root["order"] != 30 or root["rights_component_id"] != COMPOSITE_RIGHTS
            or locator.get("commit_sha") != COMMIT
            or (locator.get("line_start"), locator.get("line_end"),
                locator.get("span_bytes"), locator.get("span_sha256")) != SPAN_IDENTITY
            or root["target_locator"]["content_sha256"] != SOURCE_IDENTITY[2]):
        raise SystemExit("Unit 30 root source/rights mismatch")
    aliases = {alias: obj["id"] for obj in units for alias in obj.get("source_aliases", [])}
    if aliases != {"thm:hairy_sphere": "unit:o012-rbt-l30-thm-003"}:
        raise SystemExit("Unit 30 source alias mismatch")
    boundary = by_id["unit:o012-rbt-l30-boundary-001"]
    if (boundary.get("next_source_line") != 6369
            or boundary.get("terminal_source_eof") is not True):
        raise SystemExit("Unit 30 terminal cursor mismatch")
    rights = by_id[CUMULATIVE_RIGHTS]
    if (rights["supersedes"] != PRIOR_RIGHTS
            or rights["component_scope"] != [f"unit:o012-rbt-u{n:03d}" for n in range(1, 31)]
            or rights["license_expression"] != "CC-BY-4.0"):
        raise SystemExit("Unit 30 cumulative rights closure mismatch")
    sibling: defaultdict[str, list[int]] = defaultdict(list)
    for unit in units:
        sibling[unit["parent_id"]].append(unit["order"])
        if unit["path"][-1] != unit["id"]:
            raise SystemExit(f"Unit 30 noncanonical path: {unit['id']}")
        if unit["parent_id"].startswith("unit:") and unit["path"][:-1] != by_id[unit["parent_id"]]["path"]:
            raise SystemExit(f"Unit 30 parent-path mismatch: {unit['id']}")
    if any(len(values) != len(set(values)) for values in sibling.values()):
        raise SystemExit("Unit 30 duplicate sibling order")
    relations = suffixes["relations.jsonl"]
    proofs = [obj for obj in units if obj.get("proof_status")]
    proof_relations = [obj for obj in relations if obj["relation_type"] == "proves"]
    if len(proofs) != 4 or len(proof_relations) != 4:
        raise SystemExit("Unit 30 proof closure mismatch")
    expected_status = {1: "complete_translated_proof", 2: "complete_translated_proof",
                       3: "complete_original_proof", 4: "complete_translated_proof"}
    for number, status in expected_status.items():
        if by_id[f"unit:o012-rbt-l30-proof-{number:03d}"].get("proof_status") != status:
            raise SystemExit(f"Unit 30 proof provenance mismatch: {number}")
    for n in range(1, 7):
        exercise = f"unit:o012-rbt-l30-mcheck-{n:03d}"
        solution = f"unit:o012-rbt-l30-sol-{n:03d}"
        hint = f"unit:o012-rbt-l30-hint-{n:03d}"
        if (sum(obj["relation_type"] == "solves" and obj["from_id"] == solution
                and obj["to_id"] == exercise for obj in relations) != 1
                or sum(obj["relation_type"] == "hints" and obj["from_id"] == hint
                       and obj["to_id"] == exercise for obj in relations) != 1
                or by_id[solution].get("solution_status") != "complete_checked_solution"
                or by_id[exercise]["rights_component_id"] != COMPANION_RIGHTS):
            raise SystemExit(f"Unit 30 mastery closure mismatch: {n}")
    corrections = suffixes["corrections.jsonl"]
    if ({obj["id"] for obj in corrections} != CORRECTION_IDS
            or any(obj["upstream_report_disposition"] != "not_contacted" for obj in corrections)):
        raise SystemExit("Unit 30 correction closure mismatch")
    terms = suffixes["terms.jsonl"]
    if ({obj["concept_id"].removeprefix("concept:") for obj in terms} != SLUGS
            or any(obj.get("terminology_status") != "admitted" for obj in terms)
            or any(obj["evidence_segment_id"] not in by_id for obj in terms)):
        raise SystemExit("Unit 30 terminology closure mismatch")
    verify_controls(corrections, terms)
    asset = by_id["asset:o012-u030-source-markdown"]
    if (asset["path"], asset["bytes"], asset["sha256"], asset["rights_component_id"]) != (
            SOURCE_PATH, SOURCE_IDENTITY[0], SOURCE_IDENTITY[2], COMPOSITE_RIGHTS):
        raise SystemExit("Unit 30 reader asset mismatch")
    diagram = by_id["asset:o012-u030-semantic-diagram-layer"]
    if (diagram.get("source_format_counts") != {"tikz": 1, "xypic": 0}
            or diagram.get("semantic_unit_ids") != ["unit:o012-rbt-l30-fig-001"]
            or diagram.get("sha256") != SOURCE_IDENTITY[2]):
        raise SystemExit("Unit 30 semantic diagram asset mismatch")
    expected_evidence = {
        "artifact:o012-u030-source-audit": ("qa/UNIT_030_SOURCE_AUDIT.md", *AUDIT_IDENTITY[::2]),
        "artifact:o012-u030-independent-review": ("qa/UNIT_030_INDEPENDENT_REVIEW.md", *REVIEW_IDENTITY[::2]),
        "artifact:o012-u030-qa": ("qa/UNIT_030_QA.json", *QA_IDENTITY[::2]),
    }
    for ident, triple in expected_evidence.items():
        obj = by_id[ident]
        if (obj["path"], obj["bytes"], obj["sha256"]) != triple:
            raise SystemExit(f"Unit 30 evidence mismatch: {ident}")
        raw = (LANE / triple[0]).read_bytes()
        if (len(raw), digest(raw)) != (triple[1], triple[2]):
            raise SystemExit(f"Unit 30 live evidence mismatch: {ident}")
    for ident in ("qa:o012-u030-source-integrity", "qa:o012-u030-math",
                  "qa:o012-u030-language"):
        if by_id[ident]["result"] != "passed" or by_id[ident]["unit_id"] != ROOT:
            raise SystemExit(f"Unit 30 QA event mismatch: {ident}")
    if not any(obj["id"] == "relation:precedes:o012-rbt-u029:o012-rbt-u030"
               and obj["from_id"] == "unit:o012-rbt-u029" and obj["to_id"] == ROOT
               for obj in relations):
        raise SystemExit("Unit 30 contiguous predecessor relation missing")
    combined = b"".join((BACKEND / name).read_bytes() for name in FILES)
    if any(needle in combined for needle in (
            b"artifact:o012-units-001-030-html", b"artifact:o012-units-001-030-pdf",
            b"qa:o012-units-001-030-build", b"qa:o012-units-001-030-visual")):
        raise SystemExit("premature Unit 30 build claim detected")


def main() -> int:
    suffixes, by_id = load_and_partition()
    generic = generic_module(); records = list(by_id.values())
    generic.validate_shapes(records)
    generic.validate_references(records, by_id)
    generic.validate_artifact_manifests(records, LANE)
    verify_sources(by_id); verify_closure(suffixes, by_id)
    print("Unit 030 semantic append-only backend validation: PASS")
    print(f"prefix_records={PREFIX_TOTAL[0]}")
    print(f"prefix_bytes={PREFIX_TOTAL[1]}")
    print(f"prefix_bundle_sha256={PREFIX_TOTAL[2]}")
    print("records_added=165")
    print("records_added_by_file=" + json.dumps(DELTA, sort_keys=True))
    print(f"final_records={FINAL_TOTAL[0]}")
    print(f"final_bytes={FINAL_TOTAL[1]}")
    print(f"final_bundle_sha256={FINAL_TOTAL[2]}")
    print("stable_ids=47")
    print("identified_headings=7")
    print("fenced_semantic_objects=40")
    print("proof_closures=4")
    print("mastery_triples=6")
    print("source_aliases=1")
    print("resolved_findings=2")
    print("source_diagrams=1")
    print("adverse_ledger_through=O012-ADV-0407")
    print("terminology_through=O012-TERM-0365")
    print("next_source_line=6369")
    print("terminal_source_eof=true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
