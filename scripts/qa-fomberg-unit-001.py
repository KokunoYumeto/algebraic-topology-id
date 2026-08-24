#!/usr/bin/env python3
"""Generate the fail-closed static QA receipt for Fomberg Unit 001."""
from __future__ import annotations

import importlib.util
import json
from collections import Counter
from pathlib import Path

LANE = Path(__file__).resolve().parents[1]
COMMON_PATH = LANE / "scripts/fomberg-unit-001-common.py"
OUTPUT = LANE / "qa/FOMBERG_UNIT_001_QA.json"


def load_common():
    spec = importlib.util.spec_from_file_location("o012_fomberg_u001_common_qa", COMMON_PATH)
    if spec is None or spec.loader is None:
        raise SystemExit("cannot load Fomberg Unit 001 common module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    c = load_common()
    data = c.verify_all_inputs()
    c.verify_prefix()
    identities = {relative: c.file_identity(relative) for relative in c.IDENTITIES}
    nodes = data["nodes"]
    receipt = {
        "schema_version": "1.0.0",
        "qa_id": "O012-FOMBERG-UNIT-001-STATIC-QA",
        "status": "PASS",
        "reader": c.file_identity(c.SOURCE_PATH),
        "authority": {
            "resource_id": c.RESOURCE,
            "edition_id": c.EDITION,
            "commit": c.COMMIT,
            "tree": c.TREE,
            "source": c.file_identity(c.UPSTREAM_PATH),
            "unit_span": {"line_start": 31, "line_end": 614, "lines": 584,
                          "bytes": 21875, "sha256": c.SPAN_IDENTITY[4]},
            "next_source_line": 615,
            "next_heading": c.NEXT_HEADING,
            "terminal_source_eof": False,
            "authority_build_checks": 55,
            "authority_build_status": "PASS",
        },
        "frozen_inputs": identities,
        "immutable_prefix": {
            "files": {name: {"records": values[0], "bytes": values[1], "sha256": values[2]}
                      for name, values in c.PREFIX.items()},
            "total_records": c.PREFIX_TOTAL[0],
            "total_bytes": c.PREFIX_TOTAL[1],
            "bundle_sha256": c.PREFIX_TOTAL[2],
        },
        "structure": {
            "stable_id_count": len(nodes),
            "stable_ids_in_reader_order": [node["id"] for node in nodes],
            "class_counts": dict(sorted(Counter(node["kind"] for node in nodes).items())),
            "identified_headings": [node["id"] for node in nodes if node["kind"] == "heading"],
            "fenced_semantic_objects": sum(node["kind"] != "heading" for node in nodes),
            "unit_records_required": 87,
            "segment_records_required": 87,
            "root_heading_is_edition_root": True,
            "root_id": c.ROOT,
            "target_spans": {node["id"]: [node["line_start"], node["line_end"]]
                             for node in nodes},
        },
        "source_aliases": c.ALIASES,
        "diagrams": {
            "source_diagram_count": 14,
            "semantic_figure_block_count": 10,
            "source_format_counts": {"tikzpicture": 6, "inline_tikz": 6, "tikzcd": 2},
            "figure_ids": [node["id"] for node in nodes if node["kind"] == "figure"],
        },
        "proof_closure": {
            "repair_id": "FOM-U001-PR-001",
            "lemma_id": "o012-fom-u001-lem-boundary-square",
            "proof_id": "o012-fom-u001-proof-001",
            "corollary_id": "o012-fom-u001-cor-001",
            "proof_status": "complete_original_repair",
            "standard_boundary_convention": "B_n=im(partial_{n+1})",
        },
        "mastery": {
            "triples": 6,
            "exercise_ids": [f"o012-fom-u001-mcheck-{n:03d}" for n in range(1, 7)],
            "hint_ids": [f"o012-fom-u001-hint-{n:03d}" for n in range(1, 7)],
            "solution_ids": [f"o012-fom-u001-sol-{n:03d}" for n in range(1, 7)],
            "solution_status": "complete_checked_solution",
        },
        "rights": {
            "component": c.SOURCE_RIGHTS,
            "overlay": c.OVERLAY_RIGHTS,
            "companion": c.COMPANION_RIGHTS,
            "composite": c.COMPOSITE_RIGHTS,
            "integrated_route": c.ROUTE_RIGHTS,
            "component_license": "CC-BY-SA-4.0",
            "integrated_route_license": "CC-BY-SA-4.0",
            "roberts_component_preserved_as": "CC-BY-4.0",
        },
        "controls": {
            "adverse_ledger": {"first": "O012-ADV-0408", "through": "O012-ADV-0425",
                               "records": 18, "all_resolved": True},
            "terminology": {"first": "O012-TERM-0366", "through": "O012-TERM-0393",
                            "records": 28, "all_admitted": True},
        },
        "independent_review": {
            "path": "qa/FOMBERG_UNIT_001_INDEPENDENT_REVIEW.md",
            "sha256": c.IDENTITIES["qa/FOMBERG_UNIT_001_INDEPENDENT_REVIEW.md"][1],
            "final_severity_counts": {"P1": 0, "P2": 0, "P3": 0},
        },
        "backend_plan": {"records_by_file": c.DELTA,
                         "records_added": sum(c.DELTA.values()),
                         "expected_total_records": c.PREFIX_TOTAL[0] + sum(c.DELTA.values())},
        "model_provenance": c.MODEL,
        "checks": {
            "reader_identity_lf_utf8": True,
            "exact_87_ids": True,
            "actual_descriptive_ids_preserved": True,
            "five_source_aliases": True,
            "source_span_and_cursor": True,
            "authority_gate_55_of_55": True,
            "independent_review_p1_p2_p3_zero": True,
            "fourteen_source_diagrams_in_ten_blocks": True,
            "six_mastery_triples_complete": True,
            "proof_repair_complete": True,
            "standard_boundary_convention": True,
            "component_rights_partition": True,
            "ledgers_closed": True,
            "immutable_unit30_prefix": True,
            "no_build_or_publication_claim": True,
        },
    }
    raw = json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2).encode("utf-8") + b"\n"
    OUTPUT.write_bytes(raw)
    print("Fomberg Unit 001 static QA: PASS")
    print(f"stable_ids={len(nodes)}")
    print(f"qa_bytes={len(raw)}")
    print(f"qa_sha256={c.digest(raw)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
