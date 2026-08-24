#!/usr/bin/env python3
"""Fail-closed append-only producer for the Fomberg Unit 002 backend suffix."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any


LANE = Path(__file__).resolve().parents[1]
BACKEND = LANE / "backend"
COMMON_PATH = LANE / "scripts/fomberg-unit-002-common.py"

AUDIT_PATH = "qa/FOMBERG_UNIT_002_SOURCE_AUDIT.json"
QA_PATH = "qa/FOMBERG_UNIT_002_QA.json"
REVIEW_PATHS = {
    "integrated": "qa/FOMBERG_UNIT_002_INDEPENDENT_REVIEW_DRAFT.md",
    "part_a": "qa/FOMBERG_UNIT_002_REVIEW_PART_A_DRAFT.md",
    "part_b": "qa/FOMBERG_UNIT_002_REVIEW_PART_B_DRAFT.md",
}
EVIDENCE_PATHS = (
    AUDIT_PATH,
    REVIEW_PATHS["part_a"],
    REVIEW_PATHS["part_b"],
    REVIEW_PATHS["integrated"],
    QA_PATH,
)
ZERO_COUNTS = {"P1": 0, "P2": 0, "P3": 0}


def load_common():
    spec = importlib.util.spec_from_file_location(
        "o012_fomberg_u002_common_producer", COMMON_PATH
    )
    if spec is None or spec.loader is None:
        raise SystemExit("cannot load Fomberg Unit 002 common module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"Fomberg Unit 002 backend producer FAIL: {message}")


def pretty_json(obj: dict[str, Any]) -> bytes:
    return (
        json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2).encode("utf-8")
        + b"\n"
    )


def strict_text(c, relative: str) -> tuple[bytes, str, dict[str, Any]]:
    path = LANE / relative
    require(path.is_file(), f"missing evidence file {relative}")
    raw = path.read_bytes()
    require(not raw.startswith(b"\xef\xbb\xbf"), f"{relative}: UTF-8 BOM forbidden")
    require(b"\r" not in raw and raw.endswith(b"\n"), f"{relative}: LF discipline mismatch")
    try:
        text = raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise SystemExit(f"{relative}: invalid UTF-8 ({exc})")
    require("\ufffd" not in text, f"{relative}: replacement character forbidden")
    descriptor = {
        "path": relative,
        "bytes": len(raw),
        "sha256": c.digest(raw),
        "lf_lines": raw.count(b"\n"),
        "encoding": "UTF-8",
        "newline": "LF",
    }
    return raw, text, descriptor


def actual_descriptor(c, relative: str) -> dict[str, Any]:
    raw, _, descriptor = strict_text(c, relative)
    return descriptor


def load_json_receipt(c, relative: str) -> tuple[bytes, dict[str, Any], dict[str, Any]]:
    raw, text, descriptor = strict_text(c, relative)
    try:
        obj = json.loads(text)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"{relative}: invalid JSON ({exc})")
    require(isinstance(obj, dict), f"{relative}: top level must be an object")
    require(raw == pretty_json(obj), f"{relative}: receipt is not deterministic sorted JSON")
    return raw, obj, descriptor


def review_gate(c, relative: str) -> tuple[bytes, dict[str, Any]]:
    raw, text, descriptor = strict_text(c, relative)
    require(c.SOURCE_IDENTITY[2] in text, f"{relative}: frozen reader hash absent")
    matches = re.findall(
        r'["\x60]?FINAL_SEVERITY_COUNTS["\x60]?\s*[:=]\s*(\{[^{}\r\n]+\})',
        text,
    )
    require(bool(matches), f"{relative}: final severity counts absent")
    try:
        counts = json.loads(matches[-1])
    except json.JSONDecodeError as exc:
        raise SystemExit(f"{relative}: malformed severity JSON ({exc})")
    require(counts == ZERO_COUNTS, f"{relative}: final severity counts are nonzero")
    tail = text[-5000:]
    explicit_pass = (
        re.search(r"(?im)^[ \t]*\*\*PASS\*\*[ \t]*$", tail)
        or re.search(r'(?i)"STATUS"\s*:\s*"PASS"', tail)
        or re.search(
            r"(?is)(?:putusan akhir|final verdict|verdict|status)"
            r"[^\r\n]{0,200}(?:\*|\x60|\")*PASS",
            tail,
        )
    )
    require(bool(explicit_pass), f"{relative}: explicit final PASS absent")
    return raw, {
        "identity": descriptor,
        "status": "PASS",
        "final_severity_counts": ZERO_COUNTS,
        "reader_sha256": c.SOURCE_IDENTITY[2],
    }


def freeze_evidence(c) -> dict[str, Any]:
    audit_raw, audit, audit_identity = load_json_receipt(c, AUDIT_PATH)
    qa_raw, qa, qa_identity = load_json_receipt(c, QA_PATH)
    reviews: dict[str, Any] = {}
    review_raw: dict[str, bytes] = {}
    for slot, relative in REVIEW_PATHS.items():
        raw, result = review_gate(c, relative)
        reviews[slot] = result
        review_raw[slot] = raw
    identities = {
        AUDIT_PATH: (len(audit_raw), c.digest(audit_raw)),
        REVIEW_PATHS["part_a"]: (
            len(review_raw["part_a"]), c.digest(review_raw["part_a"])
        ),
        REVIEW_PATHS["part_b"]: (
            len(review_raw["part_b"]), c.digest(review_raw["part_b"])
        ),
        REVIEW_PATHS["integrated"]: (
            len(review_raw["integrated"]), c.digest(review_raw["integrated"])
        ),
        QA_PATH: (len(qa_raw), c.digest(qa_raw)),
    }
    require(tuple(identities) == EVIDENCE_PATHS, "evidence allowlist/order mismatch")
    return {
        "audit_raw": audit_raw,
        "audit": audit,
        "audit_identity": audit_identity,
        "qa_raw": qa_raw,
        "qa": qa,
        "qa_identity": qa_identity,
        "reviews": reviews,
        "identities": identities,
    }


def selected_rows_hash(c, rows: list[dict[str, str]]) -> str:
    raw = json.dumps(
        rows, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return c.digest(raw)


def validate_evidence(c, data: dict[str, Any], frozen: dict[str, Any]) -> None:
    audit = frozen["audit"]
    qa = frozen["qa"]
    reviews = frozen["reviews"]
    reader_descriptor = actual_descriptor(c, c.SOURCE_PATH)
    upstream_descriptor = actual_descriptor(c, c.UPSTREAM_PATH)
    terminology_descriptor = actual_descriptor(c, "00_control/TERMINOLOGY.csv")
    adverse_descriptor = actual_descriptor(c, "00_control/ADVERSE_LEDGER.csv")

    require(
        audit.get("schema_version") == "1.0.0"
        and audit.get("audit_id") == "O012-FOMBERG-UNIT-002-SOURCE-AUDIT"
        and audit.get("status") == "PASS"
        and audit.get("translation_performed") is True
        and audit.get("backend_modified") is False,
        "source-audit status/scope mismatch",
    )
    authority = audit.get("authority", {})
    require(
        authority.get("resource_id") == c.RESOURCE
        and authority.get("edition_id") == c.EDITION
        and authority.get("commit") == c.COMMIT
        and authority.get("tree") == c.TREE
        and authority.get("source") == upstream_descriptor,
        "source-audit authority binding mismatch",
    )
    unit = audit.get("unit", {})
    require(
        unit.get("edition_unit_id") == "O012-FOM-002"
        and unit.get("course_route_unit_id") == c.ROUTE
        and unit.get("line_count") == c.SPAN_IDENTITY[2]
        and unit.get("bytes_preserving_lf") == c.SPAN_IDENTITY[3]
        and unit.get("sha256_preserving_lf") == c.SPAN_IDENTITY[4]
        and unit.get("next_line") == c.NEXT_SOURCE_LINE
        and unit.get("terminal_source_eof") is False,
        "source-audit unit span/cursor mismatch",
    )
    nodes = data["nodes"]
    node_ids = [node["id"] for node in nodes]
    structure = audit.get("reader_structure", {})
    require(
        audit.get("reader") == reader_descriptor
        and structure.get("stable_id_count") == 95
        and structure.get("stable_ids_in_reader_order") == node_ids
        and structure.get("class_counts") == dict(sorted(c.EXPECTED_CLASSES.items()))
        and structure.get("fenced_semantic_objects") == 90
        and structure.get("fenced_div_opens") == 90
        and structure.get("fenced_div_closes") == 90
        and structure.get("source_labels") == 5
        and structure.get("internal_links") == 10
        and structure.get("semantic_figure_blocks") == 14,
        "source-audit reader structure mismatch",
    )
    require(audit.get("source_aliases") == c.ALIASES, "source-audit alias mismatch")
    require(
        set(audit.get("proof_closure", {})) == {"FOM-PR-01", "FOM-PR-02", "FOM-PR-03"},
        "source-audit proof closure mismatch",
    )
    require(
        audit.get("mastery", {}).get("triples") == 6
        and audit.get("mastery", {}).get("solution_status")
            == "complete_checked_solution",
        "source-audit mastery closure mismatch",
    )

    term_rows = data["terms"]
    adverse_rows = data["adverse"]
    controls = audit.get("controls", {})
    term_control = controls.get("terminology", {})
    adverse_control = controls.get("adverse", {})
    require(
        term_control.get("identity") == terminology_descriptor
        and term_control.get("first") == "O012-TERM-0394"
        and term_control.get("through") == "O012-TERM-0400"
        and term_control.get("records") == 7
        and term_control.get("rows") == term_rows
        and term_control.get("selected_rows_sha256")
            == selected_rows_hash(c, term_rows)
        and term_control.get("all_admitted") is True,
        "source-audit terminology binding mismatch",
    )
    require(
        adverse_control.get("identity") == adverse_descriptor
        and adverse_control.get("first") == "O012-ADV-0426"
        and adverse_control.get("through") == "O012-ADV-0456"
        and adverse_control.get("records") == 31
        and adverse_control.get("rows") == adverse_rows
        and adverse_control.get("selected_rows_sha256")
            == selected_rows_hash(c, adverse_rows)
        and adverse_control.get("all_resolved") is True,
        "source-audit adverse-ledger binding mismatch",
    )
    require(
        audit.get("independent_reviews") == reviews,
        "source-audit review identities/results mismatch",
    )
    require(
        audit.get("pandoc", {}).get("reader_parse") == "PASS"
        and audit.get("model_provenance") == c.MODEL
        and audit.get("checks")
        and all(value is True for value in audit["checks"].values()),
        "source-audit deterministic check set mismatch",
    )

    evidence_records = audit.get("evidence_records", [])
    require(len(evidence_records) == 95, "source-audit evidence-record count mismatch")
    evidence_by_id = {record.get("stable_id"): record for record in evidence_records}
    require(set(evidence_by_id) == set(node_ids), "source-audit evidence stable IDs mismatch")
    source_raw_lines = c.SOURCE.read_bytes().splitlines(keepends=True)
    for record in evidence_records:
        target = record.get("target_locator", {})
        start, end = target.get("line_start"), target.get("line_end")
        require(
            isinstance(start, int) and isinstance(end, int)
            and 1 <= start <= end <= c.SOURCE_IDENTITY[1]
            and target.get("path") == c.SOURCE_PATH
            and target.get("file_sha256") == c.SOURCE_IDENTITY[2]
            and target.get("content_sha256")
                == c.digest(b"".join(source_raw_lines[start - 1:end])),
            f"source-audit target evidence mismatch: {record.get('stable_id')}",
        )

    require(
        qa.get("schema_version") == "1.0.0"
        and qa.get("qa_id") == "O012-FOMBERG-UNIT-002-STATIC-QA"
        and qa.get("status") == "PASS"
        and qa.get("reader") == reader_descriptor
        and qa.get("model_provenance") == c.MODEL,
        "static-QA status/reader/model mismatch",
    )
    qa_authority = qa.get("authority", {})
    require(
        qa_authority.get("resource_id") == c.RESOURCE
        and qa_authority.get("edition_id") == c.EDITION
        and qa_authority.get("commit") == c.COMMIT
        and qa_authority.get("tree") == c.TREE
        and qa_authority.get("source") == upstream_descriptor
        and qa_authority.get("unit_span", {}).get("sha256") == c.SPAN_IDENTITY[4]
        and qa_authority.get("next_source_line") == c.NEXT_SOURCE_LINE,
        "static-QA authority mismatch",
    )
    audit_output = qa.get("source_audit_output", {})
    require(
        audit_output.get("path") == AUDIT_PATH
        and audit_output.get("bytes") == len(frozen["audit_raw"])
        and audit_output.get("sha256") == c.digest(frozen["audit_raw"])
        and audit_output.get("encoding") == "UTF-8"
        and audit_output.get("newline") == "LF",
        "static-QA does not bind the exact source-audit bytes",
    )
    expected_qa_evidence = {
        "authority_source": upstream_descriptor,
        "reader": reader_descriptor,
        "terminology_control": terminology_descriptor,
        "adverse_control": adverse_descriptor,
        "independent_reviews": {
            slot: result["identity"] for slot, result in reviews.items()
        },
    }
    require(
        qa.get("evidence") == expected_qa_evidence
        and qa.get("independent_reviews") == reviews,
        "static-QA exact evidence binding mismatch",
    )
    qa_structure = qa.get("structure", {})
    require(
        qa_structure.get("stable_id_count") == 95
        and qa_structure.get("class_counts") == dict(sorted(c.EXPECTED_CLASSES.items()))
        and qa_structure.get("fenced_semantic_objects") == 90
        and qa_structure.get("source_aliases") == c.ALIASES
        and qa_structure.get("source_diagram_functions") == 14
        and qa_structure.get("semantic_figure_blocks") == 14
        and qa.get("mastery", {}).get("triples") == 6
        and set(qa.get("proof_closure", {}))
            == {"FOM-PR-01", "FOM-PR-02", "FOM-PR-03"},
        "static-QA structural/proof/mastery mismatch",
    )
    require(
        qa.get("pandoc", {}).get("reader_parse") == "PASS"
        and qa.get("checks")
        and all(value is True for value in qa["checks"].values()),
        "static-QA deterministic check set mismatch",
    )

    exact_artifact_paths = [
        REVIEW_PATHS["integrated"],
        QA_PATH,
        REVIEW_PATHS["part_a"],
        REVIEW_PATHS["part_b"],
        AUDIT_PATH,
    ]
    for receipt in (audit, qa):
        plan = receipt.get("record_plan", {})
        require(
            plan.get("backend_write_performed") is False
            and plan.get("records_by_file") == c.DELTA
            and plan.get("records_planned") == sum(c.DELTA.values()) == 282
            and plan.get("artifact_evidence_paths_in_record_order")
                == exact_artifact_paths,
            "receipt backend record plan mismatch",
        )


def validate_record_plan(c, frozen: dict[str, Any], additions: dict[str, list[dict[str, Any]]]) -> None:
    expected_ids = {
        name: [record["id"] for record in additions[name]] for name in c.FILES
    }
    expected_paths = [
        record["path"] for record in additions["artifacts.jsonl"]
    ]
    for label, receipt in (("source audit", frozen["audit"]), ("static QA", frozen["qa"])):
        plan = receipt.get("record_plan", {})
        require(
            plan.get("edition_unit_id") == c.ROOT
            and plan.get("root_unit_id") == c.ROOT
            and plan.get("course_id") == c.COURSE
            and plan.get("course_route_unit_id") == c.ROUTE
            and plan.get("resource_id") == c.RESOURCE
            and plan.get("edition_id") == c.EDITION
            and plan.get("record_ids_by_file") == expected_ids
            and plan.get("artifact_evidence_paths_in_record_order") == expected_paths,
            f"{label} exact derived-record plan mismatch",
        )


def validate_merged(
    c,
    data: dict[str, Any],
    frozen: dict[str, Any],
    prefix_records: list[dict[str, Any]],
    additions: dict[str, list[dict[str, Any]]],
) -> tuple[dict[str, bytes], list[dict[str, Any]]]:
    suffix_records = [record for name in c.FILES for record in additions[name]]
    require(len(suffix_records) == 282, "derived suffix is not exactly 282 records")
    records = prefix_records + suffix_records
    by_id = {record["id"]: record for record in records}
    require(len(by_id) == len(records), "global ID collision before append")
    generic = c.load_generic()
    generic.validate_shapes(records)
    generic.validate_references(records, by_id)
    generic.validate_artifact_manifests(records, c.LANE)

    node_ids = {node["id"] for node in data["nodes"]}
    units = additions["units.jsonl"]
    segments = additions["segments.jsonl"]
    require(
        len(units) == len(segments) == 95
        and {record["source_local_id"] for record in units} == node_ids
        and {record["source_local_id"] for record in segments} == node_ids,
        "one-to-one 95 unit/segment mapping mismatch",
    )
    root_unit = by_id.get(c.ROOT)
    root_segment = by_id.get("segment:o012-fom-u002")
    require(root_unit is not None and root_segment is not None, "root records missing")
    require(
        (
            root_unit.get("unit_kind"),
            root_unit.get("order"),
            root_unit.get("edition_order"),
            root_unit.get("route_order"),
            root_unit.get("source_local_id"),
            root_segment.get("segment_kind"),
            root_segment.get("source_local_id"),
        )
        == (
            "reader_unit", 32, 2, 9, "o012-fom-u002",
            "source_heading", "o012-fom-u002",
        ),
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
            and locator.get("content_sha256")
                == c.digest(b"".join(reader_lines[start - 1:end])),
            f"target locator mismatch: {record.get('id')}",
        )
    unit_locator = root_unit["target_locator"]
    require(
        unit_locator["line_start"] == 1
        and unit_locator["line_end"] == c.SOURCE_IDENTITY[1]
        and unit_locator["content_sha256"] == c.SOURCE_IDENTITY[2]
        and root_unit.get("provenance_relation")
            == "composite_translated_and_original"
        and root_unit.get("rights_component_id") == c.COMPOSITE_RIGHTS,
        "root unit does not cover the full composite reader",
    )
    source_root = next(
        node for node in data["nodes"] if node["id"] == "o012-fom-u002"
    )
    segment_locator = root_segment["target_locator"]
    require(
        segment_locator["line_start"] == source_root["line_start"]
        and segment_locator["line_end"] == source_root["line_end"]
        and root_segment.get("provenance_relation")
            == "translated_adapted_from_upstream"
        and root_segment.get("rights_component_id") == c.SOURCE_RIGHTS,
        "root segment does not isolate the translated source-body span",
    )

    for local in ("omission-pr01", "omission-pr02", "omission-pr03"):
        for prefix in ("unit:", "segment:"):
            record = by_id[f"{prefix}o012-fom-u002-{local}"]
            require(
                record.get("provenance_relation")
                    == "translated_adapted_from_upstream"
                and record.get("rights_component_id") == c.SOURCE_RIGHTS,
                f"{local}: source-omission provenance/rights mismatch",
            )

    aliases = {
        node["id"]: node["attrs"]["data-source-label"]
        for node in data["nodes"] if "data-source-label" in node["attrs"]
    }
    for record in units + segments:
        alias = aliases.get(record["source_local_id"])
        if alias:
            require(record.get("source_aliases") == [alias],
                    f"source alias not bound: {record['id']}")

    corrections = additions["corrections.jsonl"]
    require(
        len(corrections) == 31
        and {record["id"] for record in corrections}
            == {
                f"correction:o012-fom-u002-adv-{number:04d}"
                for number in range(426, 457)
            }
        and {record.get("adverse_ledger_id") for record in corrections}
            == {f"O012-ADV-{number:04d}" for number in range(426, 457)},
        "31-record adverse correction closure mismatch",
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

    relation_counts = Counter(
        record["relation_type"] for record in additions["relations.jsonl"]
    )
    require(
        relation_counts == Counter({
            "adapts": 1,
            "contains": 2,
            "hints": 6,
            "illustrates": 14,
            "precedes": 2,
            "proves": 3,
            "solves": 6,
        }),
        f"34-relation closure mismatch: {dict(relation_counts)}",
    )

    expected_artifacts = {
        "artifact:o012-fom-u002-source-audit": AUDIT_PATH,
        "artifact:o012-fom-u002-review-part-a": REVIEW_PATHS["part_a"],
        "artifact:o012-fom-u002-review-part-b": REVIEW_PATHS["part_b"],
        "artifact:o012-fom-u002-independent-review": REVIEW_PATHS["integrated"],
        "artifact:o012-fom-u002-qa": QA_PATH,
    }
    artifacts = {record["id"]: record for record in additions["artifacts.jsonl"]}
    require(set(artifacts) == set(expected_artifacts), "five-artifact ID set mismatch")
    for ident, relative in expected_artifacts.items():
        raw = (LANE / relative).read_bytes()
        artifact = artifacts[ident]
        require(
            artifact.get("path") == relative
            and artifact.get("bytes") == len(raw)
            and artifact.get("sha256") == c.digest(raw),
            f"artifact identity/path mismatch: {ident}",
        )

    diagram = by_id.get("asset:o012-fom-u002-semantic-diagram-layer", {})
    require(
        diagram.get("source_diagram_count") == 14
        and diagram.get("semantic_figure_block_count") == 14
        and diagram.get("source_format_counts")
            == {"tikzcd": 13, "tikzpicture": 1}
        and len(diagram.get("semantic_unit_ids", [])) == 14,
        "diagram asset closure mismatch",
    )
    for number, proof_local, target_local in (
        (1, "proof-chain-map", "prop-chain-map"),
        (2, "proof-induced-map-homomorphism", "prop-induced-map"),
        (3, "proof-homotopy-equivalent", "cor-homotopy-equivalent"),
    ):
        repair = f"FOM-PR-0{number}"
        proof = by_id[f"unit:o012-fom-u002-{proof_local}"]
        target = by_id[f"unit:o012-fom-u002-{target_local}"]
        require(
            proof.get("repair_id") == repair
            and proof.get("proof_status") == "complete_original_repair"
            and target.get("repair_id") == repair
            and target.get("proof_status") == "statement_with_complete_repaired_proof",
            f"{repair}: backend proof binding mismatch",
        )
    for number in range(1, 7):
        require(
            by_id[f"unit:o012-fom-u002-sol-{number:03d}"].get("solution_status")
                == "complete_checked_solution",
            f"mastery solution {number} status mismatch",
        )
    require(
        {record.get("terminology_control_id") for record in additions["terms.jsonl"]}
        == {f"O012-TERM-{number:04d}" for number in range(394, 401)},
        "term/control coverage mismatch",
    )

    suffixes = {
        name: b"".join(c.canon(record) for record in additions[name])
        for name in c.FILES
    }
    for name, raw in suffixes.items():
        require(
            len(raw.splitlines()) == c.DELTA[name],
            f"{name}: canonical suffix record count mismatch",
        )
    combined = b"".join(suffixes[name] for name in c.FILES)
    require(
        b"C:\\Users" not in combined
        and b"token" not in combined.lower()
        and b"published" not in combined.lower(),
        "private path, credential word, or premature publication claim in suffix",
    )
    require(reader_raw.count(c.MODEL.encode("utf-8")) == 1,
            "reader model-provenance count mismatch")
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
    require(not sys.argv[1:], "this producer accepts no modes or replacement flags")
    c = load_common()
    frozen = freeze_evidence(c)
    data = c.verify_all_inputs(frozen["identities"])
    validate_evidence(c, data, frozen)
    prefix, prefix_records = c.verify_prefix(BACKEND)
    additions = c.build_additions(data, frozen["identities"])
    validate_record_plan(c, frozen, additions)
    suffixes, _ = validate_merged(
        c, data, frozen, prefix_records, additions
    )

    # Recheck every mutable dependency immediately before the append.
    for relative, expected in frozen["identities"].items():
        c.require_identity(relative, expected)
    refreshed_data = c.verify_all_inputs(frozen["identities"])
    validate_evidence(c, refreshed_data, frozen)
    refreshed_additions = c.build_additions(
        refreshed_data, frozen["identities"]
    )
    validate_record_plan(c, frozen, refreshed_additions)
    refreshed_suffixes = {
        name: b"".join(c.canon(record) for record in refreshed_additions[name])
        for name in c.FILES
    }
    require(
        refreshed_suffixes == suffixes,
        "reader, controls, or evidence changed the derived suffix before append",
    )
    for name in c.FILES:
        require(
            (BACKEND / name).read_bytes() == prefix[name],
            f"{name}: prefix changed before append",
        )

    for name in c.FILES:
        if suffixes[name]:
            with (BACKEND / name).open("ab") as stream:
                stream.write(suffixes[name])

    for name in c.FILES:
        live = (BACKEND / name).read_bytes()
        require(
            live == prefix[name] + suffixes[name],
            f"{name}: post-append bytes differ from exact prefix plus suffix",
        )
        require(
            len(live[len(prefix[name]):].splitlines()) == c.DELTA[name],
            f"{name}: post-append suffix count mismatch",
        )
    total_records, total_bytes, bundle_sha = backend_totals(c)
    require(
        total_records == c.PREFIX_TOTAL[0] + sum(c.DELTA.values()) == 5342,
        "cumulative record count mismatch",
    )
    print("Fomberg Unit 002 semantic backend extension: PASS")
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
