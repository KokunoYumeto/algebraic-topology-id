#!/usr/bin/env python3
"""Fail-closed append-only producer for the Fomberg Unit 007 backend suffix."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any


LANE = Path(__file__).resolve().parents[1]
BACKEND = LANE / "backend"
COMMON_PATH = LANE / "scripts/fomberg-unit-007-common.py"


def load_common():
    spec = importlib.util.spec_from_file_location("o012_fomberg_u007_common_producer", COMMON_PATH)
    if spec is None or spec.loader is None:
        raise SystemExit("cannot load Fomberg Unit 007 common module")
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"Fomberg Unit 007 backend producer FAIL: {message}")


def pretty(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2)


def validate_record_plan(c, data: dict[str, Any], additions: dict[str, list[dict[str, Any]]]) -> None:
    exact = c.record_plan(); counts = c.delta(additions)
    expected_ids = {name: [record["id"] for record in additions[name]] for name in c.FILES}
    expected_paths = [record["path"] for record in additions["artifacts.jsonl"]]
    require(exact["records_by_file"] == counts, "planned counts differ from derivation")
    require(exact["record_ids_by_file"] == expected_ids, "planned IDs differ from derivation")
    require(exact["artifact_evidence_paths_in_record_order"] == expected_paths, "artifact evidence order differs")
    for label, receipt in (("source audit", data["audit"]), ("static QA", data["qa"])):
        plan = receipt.get("record_plan", {})
        if not plan:
            continue
        require(plan.get("edition_unit_id") == c.ROOT, f"{label}: edition unit mismatch")
        require(plan.get("course_route_unit_id") == c.ROUTE, f"{label}: route mismatch")
        require(plan.get("records_by_file") == counts, f"{label}: delta mismatch")
        require(plan.get("record_ids_by_file") == expected_ids, f"{label}: record-ID plan mismatch")
        prefix = plan.get("immutable_prefix", {})
        require(
            (prefix.get("records"), prefix.get("bytes"), prefix.get("bundle_sha256")) == c.PREFIX_TOTAL,
            f"{label}: immutable prefix mismatch",
        )


def validate_merged(c, data, identities, prefix_records, additions):
    counts = c.delta(additions)
    suffix_records = [record for name in c.FILES for record in additions[name]]
    require(len(suffix_records) == sum(counts.values()), "suffix count mismatch")
    records = prefix_records + suffix_records
    by_id = {record["id"]: record for record in records}
    require(len(by_id) == len(records), "global ID collision before append")
    generic = c.load_generic()
    generic.validate_shapes(records)
    generic.validate_references(records, by_id)
    generic.validate_artifact_manifests(records, c.LANE)

    nodes = data["nodes"]; node_ids = {node["id"] for node in nodes}
    units = additions["units.jsonl"]; segments = additions["segments.jsonl"]
    require(
        len(units) == len(segments) == c.EXPECTED_STABLE_IDS
        and {record["source_local_id"] for record in units} == node_ids
        and {record["source_local_id"] for record in segments} == node_ids,
        f"one-to-one {c.EXPECTED_STABLE_IDS} unit/segment mapping mismatch",
    )
    root_unit = by_id.get(c.ROOT); root_segment = by_id.get("segment:o012-fom-u007")
    require(root_unit is not None and root_segment is not None, "root records missing")
    require(
        (
            root_unit.get("unit_kind"), root_unit.get("order"),
            root_unit.get("edition_order"), root_unit.get("route_order"),
            root_unit.get("source_local_id"), root_segment.get("segment_kind"),
            root_segment.get("source_local_id"),
        ) == ("reader_unit", 37, 7, 12, "o012-fom-u007", "source_heading", "o012-fom-u007"),
        "root unit/segment architecture mismatch",
    )
    source_raw = c.SOURCE.read_bytes(); reader_lines = source_raw.splitlines(keepends=True)
    source_identity = data["source_identity"]
    for record in units + segments:
        locator = record.get("target_locator", {})
        start, end = locator.get("line_start"), locator.get("line_end")
        require(
            isinstance(start, int) and isinstance(end, int)
            and 1 <= start <= end <= source_raw.count(b"\n")
            and locator.get("path") == c.SOURCE_PATH
            and locator.get("file_sha256") == source_identity[1]
            and locator.get("content_sha256") == c.digest(b"".join(reader_lines[start - 1:end])),
            f"target locator mismatch: {record.get('id')}",
        )
    require(
        root_unit["target_locator"]["line_start"] == 1
        and root_unit["target_locator"]["line_end"] == source_raw.count(b"\n")
        and root_unit["target_locator"]["content_sha256"] == source_identity[1]
        and root_unit.get("rights_component_id") == c.COMPOSITE_RIGHTS
        and root_segment.get("rights_component_id") == c.COMPOSITE_RIGHTS,
        "root records do not bind full composite reader",
    )

    aliases = {node["id"]: node["attrs"]["data-source-label"] for node in nodes if "data-source-label" in node["attrs"]}
    for record in units + segments:
        alias = aliases.get(record["source_local_id"])
        if alias:
            require(record.get("source_aliases") == [alias], f"source alias not bound: {record['id']}")
    for number in range(1, 7):
        require(by_id[f"unit:o012-fom-u007-sol-{number:03d}"].get("solution_status") == "complete_checked_solution", f"mastery solution {number} status mismatch")

    corrections = additions["corrections.jsonl"]
    expected_adverse = {row["event_id"] for row in data["adverse"]}
    require(
        len(corrections) == len(expected_adverse)
        and {record.get("adverse_ledger_id") for record in corrections} == expected_adverse,
        "adverse correction closure mismatch",
    )
    require(
        all(record.get("affected_unit_ids") and all(target in by_id for target in record["affected_unit_ids"])
            and record.get("evidence_segment_id") in by_id for record in corrections),
        "correction target/evidence reference mismatch",
    )
    require(not [record for record in corrections if record.get("resolution_status") == "pending_future_unit"], "pending correction obligation")

    terms = additions["terms.jsonl"]
    require(
        len(terms) == len(data["terms"])
        and {record.get("terminology_control_id") for record in terms} == {row["term_id"] for row in data["terms"]},
        "terminology/control closure mismatch",
    )
    assets = {record["id"]: record for record in additions["assets.jsonl"]}
    require(len(assets) == 8, "asset census is not source + layer + three PNG/SVG pairs")
    layer = assets["asset:o012-fom-u007-semantic-diagram-layer"]
    require(
        layer.get("source_diagram_count") == 17
        and layer.get("semantic_figure_block_count") == 14
        and layer.get("geometric_redraw_count") == 3
        and len(layer.get("semantic_unit_ids", [])) == 17,
        "semantic redraw layer closure mismatch",
    )
    for slug, figure_id in c.ASSET_SPECS:
        for ext in ("png", "svg"):
            asset = assets[f"asset:o012-fom-u007-{slug}-{ext}"]
            relative = f"{c.ASSET_DIR}/{slug}.{ext}"
            raw = (c.LANE / relative).read_bytes()
            require(
                (asset["bytes"], asset["sha256"]) == (len(raw), c.digest(raw))
                and asset.get("source_figure_unit_id") == f"unit:{figure_id}",
                f"paired redraw asset mismatch: {relative}",
            )

    relation_counts = Counter(record["relation_type"] for record in additions["relations.jsonl"])
    require(
        relation_counts == Counter({
            "adapts": 1, "contains": 2, "hints": 6, "illustrates": 3,
            "precedes": 2, "solves": 6, "xref": 1,
        }),
        f"relation closure mismatch: {dict(relation_counts)}",
    )
    artifacts = additions["artifacts.jsonl"]
    require(len(artifacts) == 3, "three-artifact evidence closure mismatch")
    for artifact in artifacts:
        relative = artifact["path"]; raw = (c.LANE / relative).read_bytes()
        require(
            (artifact["bytes"], artifact["sha256"]) == (len(raw), c.digest(raw))
            and identities[relative] == (len(raw), c.digest(raw)),
            f"artifact identity mismatch: {artifact['id']}",
        )

    suffixes = {name: b"".join(c.canon(record) for record in additions[name]) for name in c.FILES}
    for name, raw in suffixes.items():
        require(len(raw.splitlines()) == counts[name], f"{name}: canonical suffix count mismatch")
    combined = b"".join(suffixes[name] for name in c.FILES)
    lower_combined = combined.lower()
    require(
        b"c:\\users" not in lower_combined
        and b"github token:" not in lower_combined
        and b"zenodo token:" not in lower_combined
        and b"figshare token:" not in lower_combined
        and b"authorization: bearer " not in lower_combined
        and b'"translation_state":"published"' not in combined,
        "private path, credential material, or premature publication claim in suffix",
    )
    require(source_raw.count(c.MODEL.encode("utf-8")) == 1, "reader model-provenance count mismatch")
    return suffixes, records


def backend_totals(c) -> tuple[int, int, str]:
    bundle = hashlib.sha256(); total_records = 0; total_bytes = 0
    for name in c.FILES:
        raw = (BACKEND / name).read_bytes()
        total_records += len(raw.splitlines()); total_bytes += len(raw)
        bundle.update(name.encode("utf-8")); bundle.update(b"\0"); bundle.update(raw)
    return total_records, total_bytes, bundle.hexdigest()


def main() -> int:
    c = load_common()
    if sys.argv[1:] == ["--plan"]:
        print(pretty(c.record_plan())); return 0
    require(not sys.argv[1:], "accepted invocation is no arguments (append) or --plan (read-only)")
    identities = c.discover_identities(); data = c.verify_all_inputs(identities)
    prefix, prefix_records = c.verify_prefix(BACKEND)
    additions = c.build_additions(data)
    validate_record_plan(c, data, additions)
    suffixes, _ = validate_merged(c, data, identities, prefix_records, additions)
    refreshed_identities = c.discover_identities()
    require(refreshed_identities == identities, "discovered inputs changed before append")
    refreshed = c.verify_all_inputs(refreshed_identities)
    refreshed_additions = c.build_additions(refreshed)
    validate_record_plan(c, refreshed, refreshed_additions)
    refreshed_suffixes = {name: b"".join(c.canon(record) for record in refreshed_additions[name]) for name in c.FILES}
    require(refreshed_suffixes == suffixes, "sealed inputs changed derived suffix before append")
    for name in c.FILES:
        require((BACKEND / name).read_bytes() == prefix[name], f"{name}: prefix changed before append")
    for name in c.FILES:
        if suffixes[name]:
            with (BACKEND / name).open("ab") as stream:
                stream.write(suffixes[name])
    for name in c.FILES:
        live = (BACKEND / name).read_bytes()
        require(live == prefix[name] + suffixes[name], f"{name}: exact append mismatch")
    total_records, total_bytes, bundle_sha = backend_totals(c)
    counts = c.delta(additions)
    require(total_records == c.PREFIX_TOTAL[0] + sum(counts.values()), "cumulative record count mismatch")
    print("Fomberg Unit 007 semantic backend extension: PASS")
    print(f"prefix_records={c.PREFIX_TOTAL[0]}")
    print(f"prefix_bytes={c.PREFIX_TOTAL[1]}")
    print(f"prefix_bundle_sha256={c.PREFIX_TOTAL[2]}")
    print(f"records_added={sum(counts.values())}")
    print(f"cumulative_records={total_records}")
    print(f"cumulative_bytes={total_bytes}")
    print(f"backend_bundle_sha256={bundle_sha}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
