#!/usr/bin/env python3
"""Independent fail-closed validator for the Unit 025 semantic append.

This validator does not import either Unit 25 producer. It proves the frozen
Units 001--024 cumulative prefix and the exact 173-record Unit 25 semantic
slice inside the current cumulative backend. It then permits only the exact
17-record build suffix sealed by the cumulative receipt, so replay remains
strict after cumulative admission without weakening the semantic identities.
"""
from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

LANE = Path(__file__).resolve().parents[1]
BACKEND = LANE / "backend"
READER = LANE / "source/id-ID/units/unit-025-lecture-025.md"
AUTHORITY = (LANE / "authority/upstream" /
             "AlgebraicTopology2019-b947ad2e9f9e301bfe24590a9db653bc54fa1a53" /
             "Notes.tex")
TERM_LEDGER = LANE / "00_control/TERMINOLOGY.csv"
ADVERSE_LEDGER = LANE / "00_control/ADVERSE_LEDGER.csv"

MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"
ROOT = "unit:o012-rbt-u025"
ROUTE = "D60-R13"
SOURCE_SHA = "df72add4e57236b51ff7d2a0c99af4b65299365874163cb334be5d0988c0f769"
SPAN_SHA = "d05781ae58b1b6fd6174d030e52ca9ee6a08048be96f7c103e5be8de473b60b0"
ANCHOR_ORDER_SHA = "c8a52def0a0bce835100035a27bd394722880f09d5404c534dbafef014a0bce0"
PREFIX_TOTAL_RECORDS = 3723
PREFIX_TOTAL_BYTES = 3726427
PREFIX_BUNDLE = "ffa8c7cb45b6d8170d7bc83df24ec487fd0c2777297b55eff2d5e7b3ae63fe25"
SEMANTIC_TOTAL_RECORDS = 3896
SEMANTIC_TOTAL_BYTES = 3996359
SEMANTIC_BUNDLE = "55372b9c2853fa479e731c73c407b234ad2f1219e07efbedbad2a99f1e2abf47"
LIVE_TOTAL_RECORDS = 3913
LIVE_TOTAL_BYTES = 4007903
LIVE_BUNDLE = "8b50629f25c5fcbedb6d5547f8f7151c622aa90e04f71583008bd176058a4f78"

FILES = ("artifacts.jsonl", "assets.jsonl", "authority.jsonl", "concepts.jsonl",
         "corrections.jsonl", "qa.jsonl", "relations.jsonl", "rights.jsonl",
         "segments.jsonl", "terms.jsonl", "units.jsonl")
PREFIX = {
    "artifacts.jsonl": (135, 107142, "6e0bee128eb762523c603ae31c2578325f171d61fbcd15ac6c861be6486917b5"),
    "assets.jsonl": (26, 16063, "60d4f100505e27b28bc0642c8849dbc1842926d971642f2210c3a392e3f73eb4"),
    "authority.jsonl": (4, 2721, "f21af26912520ab34b38dff0e927ed46a546dbe5d318da0dc133e58330d0e368"),
    "concepts.jsonl": (319, 100311, "342c1cabc894a64d766dee238ded0a923ef655930421ddfe4d5fcf7f4569c17f"),
    "corrections.jsonl": (322, 316453, "acb12d317419c4df9f43e3743daa4001bf2a99a70c8ca4f55388401a211a488b"),
    "qa.jsonl": (114, 64675, "87e517a10dc7b2295b469770c72ef7aef3f9cef87a6e88e1499eaa249590af45"),
    "relations.jsonl": (368, 149907, "77b3123aff933914316dc636ab0190916f8d922f4900ef5f6b3b79106148b268"),
    "rights.jsonl": (67, 61618, "1e31593a6d4004633f9b27581924ed24a4ab40f11b817df22a9298116eeeb185"),
    "segments.jsonl": (1016, 1313231, "09210c2eaee49c9937ba555f1b18b26332c14297adbd70bcd17830b5ac75e620"),
    "terms.jsonl": (312, 193238, "68e6b19d70650fae488bf4ab7676dbc8e3d9efb1fb1b46de10a0169caafb1665"),
    "units.jsonl": (1040, 1401068, "ca605764e55f79126ac83d3313dd2d7a72626f4b3906573c7bc51ca9a3f1b95d"),
}
ADDED = {
    "artifacts.jsonl": 3, "assets.jsonl": 1, "authority.jsonl": 0,
    "concepts.jsonl": 6, "corrections.jsonl": 10, "qa.jsonl": 3,
    "relations.jsonl": 22, "rights.jsonl": 3, "segments.jsonl": 59,
    "terms.jsonl": 6, "units.jsonl": 60,
}
SEMANTIC = {
    "artifacts.jsonl": (138, 109709, "bab1f9ba40f5114ad42692947e23c485f59e66d8be22f83690c0784a51d9eb9f"),
    "assets.jsonl": (27, 16679, "aa569a900426a9e2cfd56777f3e52f07b35a1a72f211847bafd71ec638043462"),
    "authority.jsonl": (4, 2721, "f21af26912520ab34b38dff0e927ed46a546dbe5d318da0dc133e58330d0e368"),
    "concepts.jsonl": (325, 102250, "0ce28594cd511c1a20aff74053b7c74c6c4c6a0505c7c8c5804dd7acd2dae77d"),
    "corrections.jsonl": (332, 327054, "40791f1db8da9ba81083bad0bb4ac183094c3151b9007bb34e5fc637a1790893"),
    "qa.jsonl": (117, 66127, "743c34c79a2dde2e8595737821bd9ade984cf9cb8610eede028bcdfaaf25bc3b"),
    "relations.jsonl": (390, 158960, "a21a397f9f29c38b4ac424895a2f7f98ad6b9723e37ec47e1bf7dae213f57182"),
    "rights.jsonl": (70, 64323, "a09f281a39c910c4aaff1e10bbc1536a03f14489f68a98681f218f56ad06c453"),
    "segments.jsonl": (1075, 1428116, "d47404ea94dfa7347fbf6f6e0e0e8c5f4fb60e2634c066b87967a4468fff644a"),
    "terms.jsonl": (318, 197648, "dda9013d863bc39ec81f9936167ad24d0cfa2ebba6de0aa2c768743dc09b8503"),
    "units.jsonl": (1100, 1522772, "7fe9d4abfae9389db7cb99240b553d62b66144086c3f2097e9f64d5b2fe14318"),
}
LIVE = {
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
CUMULATIVE_ADDED = {
    "artifacts.jsonl": 7, "assets.jsonl": 0, "authority.jsonl": 0,
    "concepts.jsonl": 0, "corrections.jsonl": 0, "qa.jsonl": 2,
    "relations.jsonl": 7, "rights.jsonl": 1, "segments.jsonl": 0,
    "terms.jsonl": 0, "units.jsonl": 0,
}
CUMULATIVE_RECEIPT = LANE / "qa/BACKEND_APPEND_ONLY_UNIT_025_CUMULATIVE_RECEIPT.json"
CUMULATIVE_RECEIPT_BYTES = 7562
CUMULATIVE_RECEIPT_SHA = "eacee8cad8ffe460af5f50a9be16f5c02b0671a686209e7d0073e10b2a98a2c1"

TERM_IDS = {f"O012-TERM-{number:04d}" for number in range(323, 329)}
ADVERSE_IDS = {f"O012-ADV-{number:04d}" for number in range(332, 342)}
CONCEPT_IDS = {
    "concept:relative-cohomology", "concept:reduced-cohomology",
    "concept:pointed-delta-set", "concept:quasi-isomorphism",
    "concept:five-lemma", "concept:cohomological-euler-characteristic",
}


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canon(obj: dict[str, Any]) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8") + b"\n"


def load_generic():
    path = LANE / "scripts/validate-backend.py"
    spec = importlib.util.spec_from_file_location("o012_generic_u025_validator", path)
    if spec is None or spec.loader is None:
        raise SystemExit("cannot load generic backend validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def parse_reader() -> tuple[list[bytes], list[str], list[str], dict[str, tuple[int, int]]]:
    raw = READER.read_bytes()
    if (len(raw) != 36578 or digest(raw) != SOURCE_SHA or b"\r" in raw
            or not raw.endswith(b"\n")):
        raise SystemExit("Unit 25 reader identity/newline mismatch")
    raw_lines = raw.splitlines(keepends=True)
    lines = [line.decode("utf-8").rstrip("\n") for line in raw_lines]
    if (len(lines) != 1104 or raw.decode().count(MODEL) != 1
            or "kompleks korantai simpleksial relatif" not in lines[55]
            or "kompleks korantai simplicial relatif" in raw.decode()):
        raise SystemExit("Unit 25 resolved terminology/provenance mismatch")
    opening = re.compile(r"^\s*:::\s+\{[^#}]*#(o012-rbt-l25(?:-[A-Za-z0-9-]+)?)(.*)\}\s*$")
    heading = re.compile(r"^#{1,6}\s+.*\{[^}]*#(o012-rbt-l25(?:-[A-Za-z0-9-]+)?)[^}]*\}\s*$")
    stack: list[tuple[str, int]] = []
    ordered: list[str] = []
    spans: dict[str, tuple[int, int]] = {}
    for number, line in enumerate(lines, 1):
        hm = heading.match(line)
        if hm:
            ordered.append(hm.group(1))
        fm = opening.match(line)
        if fm:
            ordered.append(fm.group(1))
            stack.append((fm.group(1), number))
        elif line.strip() == ":::":
            if not stack:
                raise SystemExit(f"reader close without opener at line {number}")
            ident, start = stack.pop()
            spans[ident] = (start, number)
    if stack:
        raise SystemExit("reader contains unclosed fenced objects")
    headings = {
        "o012-rbt-l25-notice": (12, 51), "o012-rbt-l25": (52, 803),
        "o012-rbt-l25-s01": (54, 175), "o012-rbt-l25-s02": (176, 460),
        "o012-rbt-l25-s03": (461, 589), "o012-rbt-l25-s04": (590, 803),
        "o012-rbt-l25-mastery": (804, 1097),
    }
    spans.update(headings)
    if (len(ordered) != 59 or len(set(ordered)) != 59 or set(ordered) != set(spans)
            or digest(("\n".join(ordered) + "\n").encode()) != ANCHOR_ORDER_SHA):
        raise SystemExit("Unit 25 reader stable topology mismatch")
    return raw_lines, lines, ordered, spans


def verify_authority() -> None:
    raw = AUTHORITY.read_bytes()
    if (len(raw) != 331447
            or digest(raw) != "cfe93e9dbe3e25bd96f711f59e6078ab97527682b58e1f8ad127f74357f665d7"):
        raise SystemExit("Notes.tex authority identity mismatch")
    lines = raw.decode().replace("\r\n", "\n").replace("\r", "\n").split("\n")
    span = ("\n".join(lines[5369:5611]) + "\n").encode()
    if len(span) != 12732 or digest(span) != SPAN_SHA:
        raise SystemExit("Notes.tex Unit 25 span mismatch")
    if ("\\lecturenum{25}" not in lines[5369]
            or "\\lecturenum{26}" not in lines[5611]):
        raise SystemExit("Notes.tex Unit 25/26 boundary mismatch")


def verify_ledgers() -> None:
    with TERM_LEDGER.open(encoding="utf-8", newline="") as stream:
        rows = {row["term_id"]: row for row in csv.DictReader(stream)}
    expected = {
        "O012-TERM-0323": ("relative cohomology", "kohomologi relatif"),
        "O012-TERM-0324": ("reduced cohomology", "kohomologi tereduksi"),
        "O012-TERM-0325": ("pointed Delta-set", "himpunan-Delta bertitik dasar"),
        "O012-TERM-0326": ("quasi-isomorphism", "kuasi-isomorfisma"),
        "O012-TERM-0327": ("Five Lemma", "Lema Lima"),
        "O012-TERM-0328": ("cohomological Euler characteristic", "karakteristik Euler kohomologis"),
    }
    for ident, pair in expected.items():
        row = rows.get(ident)
        if not row or (row["source_term"], row["id_ID"]) != pair or row["status"] != "admitted":
            raise SystemExit(f"terminology ledger mismatch: {ident}")
    with ADVERSE_LEDGER.open(encoding="utf-8", newline="") as stream:
        adverse = {row["event_id"]: row for row in csv.DictReader(stream)}
    if not ADVERSE_IDS <= set(adverse):
        raise SystemExit("Unit 25 adverse ledger tail incomplete")
    resolved = adverse["O012-ADV-0341"]
    if (resolved["severity"] != "P3" or resolved["status"] != "resolved_before_admission"
            or "O012-TERM-0312" not in resolved["observed"]
            or "simpleksial" not in resolved["action"]):
        raise SystemExit("resolved Unit 25 terminology finding not transparent")


def main() -> int:
    raw_lines, _lines, anchors, spans = parse_reader()
    verify_authority()
    verify_ledgers()

    prefix_bundle = hashlib.sha256()
    semantic_bundle = hashlib.sha256()
    live_bundle = hashlib.sha256()
    tables: dict[str, list[dict[str, Any]]] = {}
    suffixes: dict[str, list[dict[str, Any]]] = {}
    cumulative_suffixes: dict[str, list[dict[str, Any]]] = {}
    global_ids: set[str] = set()
    for name in FILES:
        raw = (BACKEND / name).read_bytes()
        live_count, live_bytes, live_sha = LIVE[name]
        if (len(raw), len(raw.splitlines()), digest(raw)) != (live_bytes, live_count, live_sha):
            raise SystemExit(f"{name}: live cumulative identity mismatch")
        semantic_count, semantic_bytes, semantic_sha = SEMANTIC[name]
        semantic = raw[:semantic_bytes]
        if (len(semantic), len(semantic.splitlines()), digest(semantic)) != (
                semantic_bytes, semantic_count, semantic_sha):
            raise SystemExit(f"{name}: Unit 25 semantic boundary mismatch")
        prefix_count, prefix_bytes, prefix_sha = PREFIX[name]
        prefix = semantic[:prefix_bytes]
        if (len(prefix.splitlines()), digest(prefix)) != (prefix_count, prefix_sha):
            raise SystemExit(f"{name}: immutable prefix was not preserved byte-for-byte")
        suffix_raw = semantic[prefix_bytes:]
        suffix_lines = suffix_raw.splitlines(keepends=True)
        if len(suffix_lines) != ADDED[name] or b"\r" in suffix_raw:
            raise SystemExit(f"{name}: semantic suffix count/newline mismatch")
        suffix_objs: list[dict[str, Any]] = []
        suffix_ids: list[str] = []
        for line in suffix_lines:
            obj = json.loads(line.decode("utf-8"))
            if canon(obj) != line:
                raise SystemExit(f"{name}: noncanonical suffix record")
            suffix_objs.append(obj)
            suffix_ids.append(obj["id"])
        if suffix_ids != sorted(suffix_ids) or len(suffix_ids) != len(set(suffix_ids)):
            raise SystemExit(f"{name}: semantic suffix is not sorted/unique")
        cumulative_raw = raw[semantic_bytes:]
        cumulative_lines = cumulative_raw.splitlines(keepends=True)
        if len(cumulative_lines) != CUMULATIVE_ADDED[name] or b"\r" in cumulative_raw:
            raise SystemExit(f"{name}: cumulative suffix count/newline mismatch")
        cumulative_objs: list[dict[str, Any]] = []
        cumulative_ids: list[str] = []
        for line in cumulative_lines:
            obj = json.loads(line.decode("utf-8"))
            if canon(obj) != line:
                raise SystemExit(f"{name}: noncanonical cumulative suffix record")
            cumulative_objs.append(obj)
            cumulative_ids.append(obj["id"])
        if cumulative_ids != sorted(cumulative_ids) or len(cumulative_ids) != len(set(cumulative_ids)):
            raise SystemExit(f"{name}: cumulative suffix is not sorted/unique")
        objs = [json.loads(line) for line in raw.decode("utf-8").splitlines()]
        for obj in objs:
            if obj["id"] in global_ids:
                raise SystemExit(f"global duplicate ID: {obj['id']}")
            global_ids.add(obj["id"])
        tables[name] = objs
        suffixes[name] = suffix_objs
        cumulative_suffixes[name] = cumulative_objs
        prefix_bundle.update(name.encode()); prefix_bundle.update(b"\0"); prefix_bundle.update(prefix)
        semantic_bundle.update(name.encode()); semantic_bundle.update(b"\0"); semantic_bundle.update(semantic)
        live_bundle.update(name.encode()); live_bundle.update(b"\0"); live_bundle.update(raw)
    if (sum(PREFIX[name][0] for name in FILES) != PREFIX_TOTAL_RECORDS
            or sum(PREFIX[name][1] for name in FILES) != PREFIX_TOTAL_BYTES
            or prefix_bundle.hexdigest() != PREFIX_BUNDLE):
        raise SystemExit("cumulative prefix bundle mismatch")
    if (sum(SEMANTIC[name][0] for name in FILES) != SEMANTIC_TOTAL_RECORDS
            or sum(SEMANTIC[name][1] for name in FILES) != SEMANTIC_TOTAL_BYTES
            or semantic_bundle.hexdigest() != SEMANTIC_BUNDLE):
        raise SystemExit("Unit 25 semantic backend bundle mismatch")
    if (len(global_ids) != LIVE_TOTAL_RECORDS
            or sum(LIVE[name][1] for name in FILES) != LIVE_TOTAL_BYTES
            or live_bundle.hexdigest() != LIVE_BUNDLE):
        raise SystemExit("Unit 25 live cumulative backend bundle mismatch")

    cumulative_receipt_raw = CUMULATIVE_RECEIPT.read_bytes()
    if (len(cumulative_receipt_raw) != CUMULATIVE_RECEIPT_BYTES
            or digest(cumulative_receipt_raw) != CUMULATIVE_RECEIPT_SHA):
        raise SystemExit("Unit 25 cumulative receipt identity mismatch")
    cumulative_receipt = json.loads(cumulative_receipt_raw)
    if (cumulative_receipt.get("status") != "PASS"
            or cumulative_receipt.get("append", {}).get("records_by_file") != CUMULATIVE_ADDED
            or cumulative_receipt.get("nested_immutability", {}).get(
                "unit_025_semantic", {}).get("bundle_sha256") != SEMANTIC_BUNDLE
            or cumulative_receipt.get("current", {}).get("total_records") != LIVE_TOTAL_RECORDS
            or cumulative_receipt.get("current", {}).get("total_bytes") != LIVE_TOTAL_BYTES
            or cumulative_receipt.get("current", {}).get("bundle_sha256") != LIVE_BUNDLE):
        raise SystemExit("Unit 25 cumulative receipt does not bind the permitted suffix")
    cumulative_types = Counter(
        obj["entity_type"] for name in FILES for obj in cumulative_suffixes[name])
    if cumulative_types != Counter({"artifact": 7, "qa_event": 2,
                                    "relation": 7, "rights": 1}):
        raise SystemExit("Unit 25 cumulative suffix entity census mismatch")
    if {obj["id"] for obj in cumulative_suffixes["qa.jsonl"]} != {
            "qa:o012-units-001-025-build", "qa:o012-units-001-025-visual"}:
        raise SystemExit("Unit 25 cumulative suffix QA identity mismatch")
    if {obj["id"] for obj in cumulative_suffixes["rights.jsonl"]} != {
            "rights:o012-units-001-025-composite-cc-by-4.0-final-df72"}:
        raise SystemExit("Unit 25 cumulative suffix rights identity mismatch")

    by_id = {obj["id"]: obj for name in FILES for obj in tables[name]}
    generic = load_generic()
    records = [obj for name in FILES for obj in tables[name]]
    generic.validate_shapes(records)
    generic.validate_references(records, by_id)
    generic.validate_artifact_manifests(records, LANE)

    expected_units = {ROOT} | {f"unit:{ident}" for ident in anchors}
    expected_segments = {f"segment:{ident}" for ident in anchors}
    if {obj["id"] for obj in suffixes["units.jsonl"]} != expected_units:
        raise SystemExit("Unit 25 unit inventory mismatch")
    if {obj["id"] for obj in suffixes["segments.jsonl"]} != expected_segments:
        raise SystemExit("Unit 25 segment inventory mismatch")
    for ident in anchors:
        unit = by_id[f"unit:{ident}"]
        segment = by_id[f"segment:{ident}"]
        start, end = spans[ident]
        expected_hash = digest(b"".join(raw_lines[start - 1:end]))
        for obj in (unit, segment):
            locator = obj["target_locator"]
            if (locator["line_start"], locator["line_end"], locator["content_sha256"],
                    locator["file_sha256"]) != (start, end, expected_hash, SOURCE_SHA):
                raise SystemExit(f"target locator mismatch: {ident}")
            if (obj["edition_unit_id"] != ROOT or obj["course_route_unit_id"] != ROUTE
                    or obj["model_provenance"] != MODEL):
                raise SystemExit(f"route/model binding mismatch: {ident}")
        if unit["path"][-1] != unit["id"] or segment["unit_id"] != unit["id"]:
            raise SystemExit(f"unit/segment bijection mismatch: {ident}")
        if unit["parent_id"].startswith("unit:") and unit["path"][:-1] != by_id[unit["parent_id"]]["path"]:
            raise SystemExit(f"parent path mismatch: {ident}")
    root = by_id[ROOT]
    if (root["order"] != 25 or root["course_route_unit_id"] != ROUTE
            or root["source_locator"]["line_start"] != 5370
            or root["source_locator"]["line_end"] != 5611
            or root["source_locator"]["span_sha256"] != SPAN_SHA):
        raise SystemExit("Unit 25 root authority/route mismatch")
    if by_id["unit:o012-rbt-l25-boundary-001"].get("next_source_line") != 5612:
        raise SystemExit("Unit 25 next cursor mismatch")
    if by_id["unit:o012-rbt-l25-exa-001"].get("source_aliases") != ["eg:dim_minus_one_skeleton_rel_cochains"]:
        raise SystemExit("Unit 25 source alias mismatch")

    suffix_counts = Counter(obj["entity_type"] for name in FILES for obj in suffixes[name])
    if suffix_counts != Counter({"unit": 60, "segment": 59, "relation": 22,
                                 "correction": 10, "concept": 6, "term": 6,
                                 "artifact": 3, "qa_event": 3, "rights": 3,
                                 "asset": 1}):
        raise SystemExit(f"Unit 25 semantic entity census mismatch: {suffix_counts}")
    if {obj["id"] for obj in suffixes["concepts.jsonl"]} != CONCEPT_IDS:
        raise SystemExit("Unit 25 concept suffix mismatch")
    if {obj.get("terminology_control_id") for obj in suffixes["terms.jsonl"]} != TERM_IDS:
        raise SystemExit("Unit 25 term-control suffix mismatch")
    if {obj.get("adverse_ledger_id") for obj in suffixes["corrections.jsonl"]} != ADVERSE_IDS:
        raise SystemExit("Unit 25 correction-control suffix mismatch")
    resolved = by_id["correction:o012-u025-adv-0341"]
    if (resolved["correction_type"] != "terminology_correction"
            or resolved["affected_unit_ids"] != ["unit:o012-rbt-l25-s01"]):
        raise SystemExit("Unit 25 resolved terminology correction binding mismatch")
    if {obj["path"] for obj in suffixes["artifacts.jsonl"]} != {
            "qa/UNIT_025_SOURCE_AUDIT.md", "qa/UNIT_025_INDEPENDENT_REVIEW.md",
            "qa/UNIT_025_QA.json"}:
        raise SystemExit("Unit 25 semantic artifact boundary includes a build/output artifact")
    for artifact in suffixes["artifacts.jsonl"]:
        raw = (LANE / artifact["path"]).read_bytes()
        if len(raw) != artifact["bytes"] or digest(raw) != artifact["sha256"]:
            raise SystemExit(f"Unit 25 evidence artifact mismatch: {artifact['id']}")
    qa = json.loads((LANE / "qa/UNIT_025_QA.json").read_text(encoding="utf-8"))
    if (qa["status"] != "PASS" or qa["source"]["next_line"] != 5612
            or qa["resolved_findings"][0]["finding_id"] != "UNIT025-TERM-P3-001"
            or qa["resolved_findings"][0]["status"] != "RESOLVED_BEFORE_ADMISSION"):
        raise SystemExit("Unit 25 QA/resolved-finding closure mismatch")
    review = (LANE / "qa/UNIT_025_INDEPENDENT_REVIEW.md").read_text(encoding="utf-8")
    if ("P1: 0" not in review or "P2: 0" not in review or "P3: 0" not in review
            or "UNIT025-TERM-P3-001" not in review):
        raise SystemExit("Unit 25 independent-review closure mismatch")

    rels = suffixes["relations.jsonl"]
    if sum(obj["relation_type"] == "proves" for obj in rels) != 4:
        raise SystemExit("Unit 25 proof relation closure mismatch")
    for number in range(1, 7):
        check = f"unit:o012-rbt-l25-mcheck-{number:03d}"
        if (sum(obj["relation_type"] == "hints" and obj["to_id"] == check for obj in rels) != 1
                or sum(obj["relation_type"] == "solves" and obj["to_id"] == check for obj in rels) != 1):
            raise SystemExit(f"Unit 25 mastery relation closure mismatch: {number}")
    proof_units = [obj for obj in suffixes["units.jsonl"]
                   if obj.get("proof_status") == "complete_original_proof"]
    solution_units = [obj for obj in suffixes["units.jsonl"]
                      if obj.get("solution_status") == "complete_checked_solution"]
    if len(proof_units) != 4 or len(solution_units) != 6:
        raise SystemExit("Unit 25 proof/solution status closure mismatch")
    rights = by_id["rights:o012-units-001-025-composite-cc-by-4.0"]
    if (rights["supersedes"] != "rights:o012-units-001-024-composite-cc-by-4.0-final-993a"
            or rights["component_scope"] != [f"unit:o012-rbt-u{number:03d}" for number in range(1, 26)]
            or rights["license_expression"] != "CC-BY-4.0"):
        raise SystemExit("Unit 25 cumulative rights closure mismatch")
    sibling_orders: defaultdict[str, list[int]] = defaultdict(list)
    for unit in suffixes["units.jsonl"]:
        sibling_orders[unit["parent_id"]].append(unit["order"])
    if any(len(values) != len(set(values)) for values in sibling_orders.values()):
        raise SystemExit("Unit 25 sibling order collision")

    print("Unit 025 append-only semantic backend validation: PASS")
    print(f"prefix_records={PREFIX_TOTAL_RECORDS}")
    print(f"prefix_bytes={PREFIX_TOTAL_BYTES}")
    print(f"prefix_bundle_sha256={PREFIX_BUNDLE}")
    print(f"records_added={sum(ADDED.values())}")
    print("records_added_by_file=" + json.dumps(ADDED, sort_keys=True))
    print(f"semantic_total_records={SEMANTIC_TOTAL_RECORDS}")
    print(f"semantic_total_bytes={SEMANTIC_TOTAL_BYTES}")
    print(f"semantic_bundle_sha256={SEMANTIC_BUNDLE}")
    print(f"permitted_cumulative_records={sum(CUMULATIVE_ADDED.values())}")
    print(f"live_total_records={LIVE_TOTAL_RECORDS}")
    print(f"live_total_bytes={LIVE_TOTAL_BYTES}")
    print(f"live_bundle_sha256={LIVE_BUNDLE}")
    print(f"cumulative_receipt_sha256={CUMULATIVE_RECEIPT_SHA}")
    print("stable_ids=59")
    print("proof_closures=4")
    print("mastery_triples=6")
    print("resolved_terminology_finding=UNIT025-TERM-P3-001")
    print("next_source_line=5612")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
