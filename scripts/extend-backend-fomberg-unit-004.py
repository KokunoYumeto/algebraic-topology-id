#!/usr/bin/env python3
"""Fail-closed append-only producer for the Fomberg Unit 004 backend suffix."""
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
COMMON_PATH = LANE / "scripts/fomberg-unit-004-common.py"


def load_common():
    spec = importlib.util.spec_from_file_location("o012_fomberg_u004_common_producer", COMMON_PATH)
    if spec is None or spec.loader is None:
        raise SystemExit("cannot load Fomberg Unit 004 common module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"Fomberg Unit 004 backend producer FAIL: {message}")


def pretty(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2)


def validate_record_plan(c, data: dict[str, Any], additions: dict[str, list[dict[str, Any]]]) -> None:
    exact = c.record_plan()
    expected_ids = {name: [record["id"] for record in additions[name]] for name in c.FILES}
    expected_paths = [record["path"] for record in additions["artifacts.jsonl"]]
    require(exact["record_ids_by_file"] == expected_ids, "planned IDs differ from frozen derivation")
    require(
        exact["artifact_evidence_paths_in_record_order"] == expected_paths,
        "artifact evidence order differs from frozen derivation",
    )
    for label, receipt in (("source audit", data["audit"]), ("static QA", data["qa"])):
        plan = receipt.get("record_plan", {})
        if not plan:
            continue
        require(plan.get("edition_unit_id") == c.ROOT, f"{label}: edition unit mismatch")
        require(plan.get("root_unit_id") == c.ROOT, f"{label}: root unit mismatch")
        require(plan.get("course_id") == c.COURSE, f"{label}: course mismatch")
        require(plan.get("course_route_unit_id") == c.ROUTE, f"{label}: route mismatch")
        require(plan.get("resource_id") == c.RESOURCE, f"{label}: resource mismatch")
        require(plan.get("edition_id") == c.EDITION, f"{label}: edition mismatch")
        require(plan.get("records_by_file") == c.DELTA, f"{label}: delta mismatch")
        require(plan.get("records_planned") == sum(c.DELTA.values()), f"{label}: total mismatch")
        require(plan.get("record_ids_by_file") == expected_ids, f"{label}: exact record-ID plan mismatch")
        require(
            plan.get("artifact_evidence_paths_in_record_order") == expected_paths,
            f"{label}: artifact record order mismatch",
        )
        prefix = plan.get("immutable_prefix", {})
        require(
            prefix.get("records") == c.PREFIX_TOTAL[0]
            and prefix.get("bytes") == c.PREFIX_TOTAL[1]
            and prefix.get("bundle_sha256") == c.PREFIX_TOTAL[2],
            f"{label}: immutable prefix identity mismatch",
        )


def validate_merged(
    c,
    data: dict[str, Any],
    identities: dict[str, tuple[int, str]],
    prefix_records: list[dict[str, Any]],
    additions: dict[str, list[dict[str, Any]]],
) -> tuple[dict[str, bytes], list[dict[str, Any]]]:
    suffix_records = [record for name in c.FILES for record in additions[name]]
    require(len(suffix_records) == sum(c.DELTA.values()) == 366, "suffix is not exactly 366 records")
    records = prefix_records + suffix_records
    by_id = {record["id"]: record for record in records}
    require(len(by_id) == len(records), "global ID collision before append")
    generic = c.load_generic()
    generic.validate_shapes(records)
    generic.validate_references(records, by_id)
    generic.validate_artifact_manifests(records, c.LANE)

    nodes = data["nodes"]
    node_ids = {node["id"] for node in nodes}
    units = additions["units.jsonl"]
    segments = additions["segments.jsonl"]
    require(
        len(units) == len(segments) == 117
        and {record["source_local_id"] for record in units} == node_ids
        and {record["source_local_id"] for record in segments} == node_ids,
        "one-to-one 117 unit/segment mapping mismatch",
    )
    root_unit = by_id.get(c.ROOT)
    root_segment = by_id.get("segment:o012-fom-u004")
    require(root_unit is not None and root_segment is not None, "root records missing")
    require(
        (
            root_unit.get("unit_kind"), root_unit.get("order"),
            root_unit.get("edition_order"), root_unit.get("route_order"),
            root_unit.get("source_local_id"), root_segment.get("segment_kind"),
            root_segment.get("source_local_id"),
        )
        == ("reader_unit", 34, 4, 11, "o012-fom-u004", "source_heading", "o012-fom-u004"),
        "root unit/segment architecture mismatch",
    )
    reader_raw = c.SOURCE.read_bytes()
    reader_lines = reader_raw.splitlines(keepends=True)
    for record in units + segments:
        locator = record.get("target_locator", {})
        start, end = locator.get("line_start"), locator.get("line_end")
        require(
            isinstance(start, int) and isinstance(end, int)
            and 1 <= start <= end <= c.SOURCE_IDENTITY[1]
            and locator.get("path") == c.SOURCE_PATH
            and locator.get("file_sha256") == c.SOURCE_IDENTITY[2]
            and locator.get("content_sha256") == c.digest(b"".join(reader_lines[start - 1:end])),
            f"target locator mismatch: {record.get('id')}",
        )
    require(
        root_unit["target_locator"]["line_start"] == 1
        and root_unit["target_locator"]["line_end"] == c.SOURCE_IDENTITY[1]
        and root_unit["target_locator"]["content_sha256"] == c.SOURCE_IDENTITY[2]
        and root_unit.get("provenance_relation") == "composite_translated_and_original"
        and root_unit.get("rights_component_id") == c.COMPOSITE_RIGHTS
        and root_segment.get("provenance_relation") == "composite_translated_and_original"
        and root_segment.get("rights_component_id") == c.COMPOSITE_RIGHTS,
        "root records do not bind the full composite reader",
    )

    aliases = {
        node["id"]: node["attrs"]["data-source-label"]
        for node in nodes if "data-source-label" in node["attrs"]
    }
    for record in units + segments:
        alias = aliases.get(record["source_local_id"])
        if alias:
            require(record.get("source_aliases") == [alias], f"source alias not bound: {record['id']}")

    corrections = additions["corrections.jsonl"]
    require(
        len(corrections) == 24
        and {record["id"] for record in corrections}
            == {f"correction:o012-fom-u004-adv-{number:04d}" for number in range(499, 523)}
        and {record.get("adverse_ledger_id") for record in corrections}
            == {f"O012-ADV-{number:04d}" for number in range(499, 523)},
        "24-record adverse correction closure mismatch",
    )
    require(
        all(
            record.get("affected_unit_ids")
            and all(target in by_id for target in record["affected_unit_ids"])
            and record.get("evidence_segment_id") in by_id
            for record in corrections
        ),
        "correction target/evidence reference mismatch",
    )
    pending = [record for record in corrections if record.get("resolution_status") == "pending_future_unit"]
    require(not pending, "Unit 004 contains an unexpected pending correction obligation")

    relation_counts = Counter(record["relation_type"] for record in additions["relations.jsonl"])
    require(
        relation_counts == Counter({
            "adapts": 1, "contains": 2, "depends-on": 1,
            "hints": 7, "illustrates": 22, "precedes": 2,
            "proves": 8, "solves": 7, "xref": 3,
        }),
        f"53-relation closure mismatch: {dict(relation_counts)}",
    )
    complete_repairs = Counter(
        record.get("repair_id") for record in units
        if record.get("proof_status") == "complete_original_repair"
    )
    named_omissions = Counter(
        record.get("repair_id") for record in units
        if record.get("proof_status") == "source_omission_named"
    )
    require(
        complete_repairs == Counter({
            "FOM-PR-05": 2, "FOM-PR-06": 1, "FOM-PR-07": 1,
            "FOM-PR-08": 1, "FOM-PR-09": 1, "FOM-PR-10": 1,
            "FOM-PR-11": 1,
        })
        and named_omissions == Counter({
            "FOM-PR-05": 2, "FOM-PR-06": 1, "FOM-PR-07": 1,
            "FOM-PR-08": 1, "FOM-PR-09": 1, "FOM-PR-10": 1,
            "FOM-PR-11": 1,
        }),
        "FOM-PR-05 through FOM-PR-11 omission/repair closure mismatch",
    )
    for number in range(1, 8):
        require(
            by_id[f"unit:o012-fom-u004-sol-{number:03d}"].get("solution_status")
                == "complete_checked_solution",
            f"mastery solution {number} status mismatch",
        )

    assets = {record["id"]: record for record in additions["assets.jsonl"]}
    require(len(assets) == 8, "asset record count mismatch")
    require(
        len([record for record in assets.values() if record.get("role") == "reader_linked_accessible_redraw"]) == 3
        and len([record for record in assets.values() if record.get("role") == "accessible_vector_source_companion"]) == 3,
        "three PNG/three SVG asset closure mismatch",
    )
    diagram = assets["asset:o012-fom-u004-semantic-diagram-layer"]
    require(
        diagram.get("source_diagram_count") == 20
        and diagram.get("semantic_figure_block_count") == 19
        and diagram.get("geometric_redraw_count") == 3
        and len(diagram.get("semantic_unit_ids", [])) == 19,
        "semantic diagram-layer closure mismatch",
    )

    artifacts = {record["id"]: record for record in additions["artifacts.jsonl"]}
    require(len(artifacts) == 3, "three-artifact evidence closure mismatch")
    for artifact in artifacts.values():
        relative = artifact["path"]
        raw = (c.LANE / relative).read_bytes()
        require(
            (artifact["bytes"], artifact["sha256"]) == (len(raw), c.digest(raw))
            and identities[relative] == (len(raw), c.digest(raw)),
            f"artifact identity mismatch: {artifact['id']}",
        )
    require(
        {record.get("terminology_control_id") for record in additions["terms.jsonl"]}
            == {f"O012-TERM-{number:04d}" for number in range(416, 435)},
        "term/control coverage mismatch",
    )

    suffixes = {
        name: b"".join(c.canon(record) for record in additions[name])
        for name in c.FILES
    }
    for name, raw in suffixes.items():
        require(len(raw.splitlines()) == c.DELTA[name], f"{name}: canonical suffix count mismatch")
    combined = b"".join(suffixes[name] for name in c.FILES)
    require(
        b"C:\\Users" not in combined
        and b"token" not in combined.lower()
        and b'"translation_state":"published"' not in combined,
        "private path, credential word, or premature publication claim in suffix",
    )
    require(reader_raw.count(c.MODEL.encode("utf-8")) == 1, "reader model-provenance count mismatch")
    return suffixes, records


def backend_totals(c) -> tuple[int, int, str]:
    bundle = hashlib.sha256()
    total_records = 0
    total_bytes = 0
    for name in c.FILES:
        raw = (BACKEND / name).read_bytes()
        total_records += len(raw.splitlines())
        total_bytes += len(raw)
        bundle.update(name.encode("utf-8"))
        bundle.update(b"\0")
        bundle.update(raw)
    return total_records, total_bytes, bundle.hexdigest()


def main() -> int:
    c = load_common()
    if sys.argv[1:] == ["--plan"]:
        print(pretty(c.record_plan()))
        return 0
    require(not sys.argv[1:], "accepted invocation is no arguments (append) or --plan (read-only)")

    identities = c.sealed_identities()
    data = c.verify_all_inputs(identities)
    prefix, prefix_records = c.verify_prefix(BACKEND)
    additions = c.build_additions(data, identities)
    validate_record_plan(c, data, additions)
    suffixes, _ = validate_merged(c, data, identities, prefix_records, additions)

    # Recheck every mutable dependency immediately before the only write step.
    for relative, expected in identities.items():
        c.require_identity(relative, expected)
    refreshed = c.verify_all_inputs(identities)
    refreshed_additions = c.build_additions(refreshed, identities)
    validate_record_plan(c, refreshed, refreshed_additions)
    refreshed_suffixes = {
        name: b"".join(c.canon(record) for record in refreshed_additions[name])
        for name in c.FILES
    }
    require(refreshed_suffixes == suffixes, "sealed inputs changed the derived suffix before append")
    for name in c.FILES:
        require((BACKEND / name).read_bytes() == prefix[name], f"{name}: prefix changed before append")

    for name in c.FILES:
        if suffixes[name]:
            with (BACKEND / name).open("ab") as stream:
                stream.write(suffixes[name])

    for name in c.FILES:
        live = (BACKEND / name).read_bytes()
        require(live == prefix[name] + suffixes[name], f"{name}: post-append bytes differ from exact prefix plus suffix")
        require(len(live[len(prefix[name]):].splitlines()) == c.DELTA[name], f"{name}: post-append suffix count mismatch")
    total_records, total_bytes, bundle_sha = backend_totals(c)
    require(total_records == c.PREFIX_TOTAL[0] + sum(c.DELTA.values()) == 6113, "cumulative record count mismatch")
    print("Fomberg Unit 004 semantic backend extension: PASS")
    print(f"prefix_records={c.PREFIX_TOTAL[0]}")
    print(f"prefix_bytes={c.PREFIX_TOTAL[1]}")
    print(f"prefix_bundle_sha256={c.PREFIX_TOTAL[2]}")
    print(f"records_added={sum(c.DELTA.values())}")
    print(f"cumulative_records={total_records}")
    print(f"cumulative_bytes={total_bytes}")
    print(f"backend_bundle_sha256={bundle_sha}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
