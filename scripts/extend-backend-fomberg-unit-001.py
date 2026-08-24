#!/usr/bin/env python3
"""Fail-closed append-only producer for the Fomberg Unit 001 semantic backend."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

LANE = Path(__file__).resolve().parents[1]
BACKEND = LANE / "backend"
COMMON_PATH = LANE / "scripts/fomberg-unit-001-common.py"
QA_PATH = LANE / "qa/FOMBERG_UNIT_001_QA.json"
QA_IDENTITY = (21253, "b3b0ebc9430b80d45c64a6c528e0e36f46ca0d646a50e7b9c9c5d68285369b7a")
PRE_REPAIR_SEGMENTS_IDENTITY = (
    2094228, "64352bcb7cc2b7e09944bdea3f5c0eecb591ae24895862b6760e1968bd26d76f")
FINAL_BEFORE_EVIDENCE_REBIND = {
    "artifacts.jsonl": (166, 133601, "fd83de24320bbd44f3716edd04d7944964b8624bbce7ac1c8a8230bc3141f220"),
    "assets.jsonl": (37, 23720, "a9cc6a83e0e7c771044f0984fefb32f3c0ee409b428bb626b043f6bff7264367"),
    "authority.jsonl": (6, 4374, "84c622f56dbbd5ba379361245ecfe07bc79c9f4fd6b18ba21b82b5f545211869"),
    "concepts.jsonl": (392, 123698, "e83c6047f4f934044bff8bb1a057d2db2ef4d878fad6a6ce9a54d1c490a194bf"),
    "corrections.jsonl": (425, 416934, "f0a124da975557b3871e5ce8fbe7226c595ff06a3357b4c5f8e13352e7038c54"),
    "qa.jsonl": (138, 77180, "98449c7de7856384cced4d4ed0bd5c0c01ea0bf7b292f679ba52ae8ccac83ce0"),
    "relations.jsonl": (564, 232018, "01047e8dd954fcbc0f8fbefaf8ae78415f1278d601de3ec733f4c20c9e895101"),
    "rights.jsonl": (91, 83493, "e81261979962c93827e0199126b7164dda25063f2700918697dc9ede54517053"),
    "segments.jsonl": (1413, 2094230, "6a6789c021494f6099c1e1b5b59edd9045fb08688b3ececda5d2f53000fb5a8c"),
    "terms.jsonl": (385, 246829, "c29a3f45f4e29b6741dc2fe6b70ea421f1edf1000a50e276d544aa731045fc8d"),
    "units.jsonl": (1443, 2222571, "ba9a464c3eb2ba995eca5b78e870c2d57f58896b86f94b54b40f8538106b954c"),
}


def load_common():
    spec = importlib.util.spec_from_file_location("o012_fomberg_u001_common_producer", COMMON_PATH)
    if spec is None or spec.loader is None:
        raise SystemExit("cannot load Fomberg Unit 001 common module")
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


def validate_qa(c, data) -> None:
    raw = QA_PATH.read_bytes()
    if (len(raw), c.digest(raw)) != QA_IDENTITY:
        raise SystemExit("Fomberg Unit 001 QA identity mismatch")
    qa = json.loads(raw.decode("utf-8"))
    if (qa.get("status") != "PASS"
            or qa.get("qa_id") != "O012-FOMBERG-UNIT-001-STATIC-QA"
            or qa.get("reader", {}).get("sha256") != c.SOURCE_IDENTITY[2]
            or qa.get("structure", {}).get("stable_ids_in_reader_order")
                != [node["id"] for node in data["nodes"]]
            or qa.get("structure", {}).get("unit_records_required") != 87
            or qa.get("structure", {}).get("segment_records_required") != 87
            or not qa.get("structure", {}).get("root_heading_is_edition_root")
            or qa.get("source_aliases") != c.ALIASES
            or qa.get("diagrams", {}).get("source_diagram_count") != 14
            or qa.get("diagrams", {}).get("semantic_figure_block_count") != 10
            or qa.get("proof_closure", {}).get("repair_id") != "FOM-U001-PR-001"
            or qa.get("proof_closure", {}).get("standard_boundary_convention") != "B_n=im(partial_{n+1})"
            or qa.get("mastery", {}).get("triples") != 6
            or qa.get("controls", {}).get("adverse_ledger", {}).get("through") != "O012-ADV-0425"
            or qa.get("controls", {}).get("terminology", {}).get("through") != "O012-TERM-0393"
            or qa.get("independent_review", {}).get("final_severity_counts") != {"P1": 0, "P2": 0, "P3": 0}
            or qa.get("backend_plan", {}).get("records_by_file") != c.DELTA):
        raise SystemExit("Fomberg Unit 001 QA semantic binding mismatch")


def validate_merged(c, prefix_records, additions) -> tuple[list[dict], str, int]:
    suffix_records = [record for name in c.FILES for record in additions[name]]
    records = prefix_records + suffix_records
    by_id = {record["id"]: record for record in records}
    if len(by_id) != len(records):
        raise SystemExit("global ID collision before append")
    generic = c.load_generic()
    generic.validate_shapes(records)
    generic.validate_references(records, by_id)
    generic.validate_artifact_manifests(records, c.LANE)
    nodes = c.parse_reader()[1]
    node_ids = {node["id"] for node in nodes}
    if ({record["source_local_id"] for record in additions["units.jsonl"]} != node_ids
            or {record["source_local_id"] for record in additions["segments.jsonl"]} != node_ids):
        raise SystemExit("one-to-one stable-ID unit/segment mapping mismatch")
    root_units = [record for record in additions["units.jsonl"] if record["id"] == c.ROOT]
    root_segments = [record for record in additions["segments.jsonl"]
                     if record["id"] == "segment:o012-fom-u001"]
    if (len(root_units), len(root_segments)) != (1, 1):
        raise SystemExit("root heading/root architecture mismatch")
    if (root_units[0]["unit_kind"] != "reader_unit"
            or root_units[0]["source_local_id"] != "o012-fom-u001"
            or root_segments[0]["segment_kind"] != "source_heading"):
        raise SystemExit("root heading dual semantics mismatch")
    source_raw = c.SOURCE.read_bytes(); source_lines = source_raw.splitlines(keepends=True)
    for record in additions["units.jsonl"] + additions["segments.jsonl"]:
        locator = record["target_locator"]
        start, end = locator["line_start"], locator["line_end"]
        if (locator["path"] != c.SOURCE_PATH or locator["file_sha256"] != c.SOURCE_IDENTITY[2]
                or not (1 <= start <= end <= c.SOURCE_IDENTITY[1])
                or locator["content_sha256"] != c.digest(b"".join(source_lines[start - 1:end]))):
            raise SystemExit(f"target locator mismatch: {record['id']}")
    relation_types = {}
    for record in additions["relations.jsonl"]:
        relation_types.setdefault(record["relation_type"], 0)
        relation_types[record["relation_type"]] += 1
    if relation_types != {"adapts": 1, "contains": 2, "depends-on": 2,
                          "hints": 6, "illustrates": 10, "precedes": 2,
                          "proves": 1, "solves": 6, "xref": 1}:
        raise SystemExit(f"relation closure mismatch: {relation_types}")
    combined = b"".join(c.canon(record) for record in suffix_records)
    forbidden = (b"published", b"artifact:o012-fomberg-unit-001-html",
                 b"artifact:o012-fomberg-unit-001-pdf", b"FOM-PR-01")
    if any(item in combined for item in forbidden):
        raise SystemExit("premature build/publication/later-repair claim detected")
    return records, c.digest(combined), len(combined)


def main() -> int:
    c = load_common()
    data = c.verify_all_inputs()
    validate_qa(c, data)
    prefix, prefix_records = c.verify_prefix(BACKEND)
    additions = c.build_additions(data, QA_IDENTITY)
    validate_merged(c, prefix_records, additions)
    locator_replacement = "--replace-unfinalized-proof-locator-suffix" in sys.argv[1:]
    evidence_rebind = "--rebind-frozen-evidence-suffix" in sys.argv[1:]
    if locator_replacement and evidence_rebind:
        raise SystemExit("choose exactly one bounded replacement mode")
    if evidence_rebind:
        for name in c.FILES:
            live = (BACKEND / name).read_bytes()
            observed = (len(live.splitlines()), len(live), c.digest(live))
            if observed != FINAL_BEFORE_EVIDENCE_REBIND[name]:
                raise SystemExit(f"{name}: pre-evidence-rebind final identity mismatch")
            if live[:len(prefix[name])] != prefix[name]:
                raise SystemExit(f"{name}: immutable prefix mismatch before evidence rebind")
        for name in c.FILES:
            rebound = prefix[name] + b"".join(c.canon(record) for record in additions[name])
            (BACKEND / name).write_bytes(rebound)
    elif locator_replacement:
        for name in c.FILES:
            live = (BACKEND / name).read_bytes()
            expected = prefix[name] + b"".join(c.canon(record) for record in additions[name])
            if name == "segments.jsonl":
                if (len(live), c.digest(live)) != PRE_REPAIR_SEGMENTS_IDENTITY:
                    raise SystemExit("segments.jsonl: pre-repair suffix identity mismatch")
            elif live != expected:
                raise SystemExit(f"{name}: non-segment backend differs during bounded locator repair")
        repaired = prefix["segments.jsonl"] + b"".join(
            c.canon(record) for record in additions["segments.jsonl"])
        (BACKEND / "segments.jsonl").write_bytes(repaired)
    else:
        for name in c.FILES:
            if len((BACKEND / name).read_bytes()) != c.PREFIX[name][1]:
                raise SystemExit(f"{name}: producer requires exact unextended Unit 30 boundary")
        for name in c.FILES:
            suffix = b"".join(c.canon(record) for record in additions[name])
            with (BACKEND / name).open("ab") as stream:
                stream.write(suffix)
    bundle = hashlib.sha256(); total_records = total_bytes = 0
    for name in c.FILES:
        live = (BACKEND / name).read_bytes()
        if live[:len(prefix[name])] != prefix[name]:
            raise SystemExit(f"{name}: immutable prefix changed during append")
        suffix_lines = live[len(prefix[name]):].splitlines(keepends=True)
        if len(suffix_lines) != c.DELTA[name]:
            raise SystemExit(f"{name}: appended record count mismatch")
        expected = b"".join(c.canon(record) for record in additions[name])
        if live[len(prefix[name]):] != expected:
            raise SystemExit(f"{name}: appended bytes mismatch")
        total_records += len(live.splitlines()); total_bytes += len(live)
        bundle.update(name.encode()); bundle.update(b"\0"); bundle.update(live)
    print("Fomberg Unit 001 semantic backend extension: PASS")
    print(f"records_added={sum(c.DELTA.values())}")
    print(f"cumulative_records={total_records}")
    print(f"cumulative_bytes={total_bytes}")
    print(f"backend_bundle_sha256={bundle.hexdigest()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
