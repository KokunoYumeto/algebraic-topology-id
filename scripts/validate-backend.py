#!/usr/bin/env python3
"""Validate the locale-neutral Unit 001 interoperability backend.

The validator is deliberately self-contained and offline.  It checks canonical
JSONL serialization, referential integrity, source-span hashes, artifact hashes,
the existing artifact manifest, and complete exercise-to-solution linkage.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable


SCHEMA = "curriculum.interop"
SCHEMA_VERSION = "0.1.0"
EXPECTED_FILES = {
    "artifacts.jsonl",
    "assets.jsonl",
    "authority.jsonl",
    "concepts.jsonl",
    "corrections.jsonl",
    "qa.jsonl",
    "relations.jsonl",
    "rights.jsonl",
    "segments.jsonl",
    "terms.jsonl",
    "units.jsonl",
}
COMMON_FIELDS = {
    "entity_type",
    "id",
    "schema",
    "schema_version",
    "status",
    "supersedes",
    "timestamp",
    "workflow",
}
REQUIRED_BY_TYPE = {
    "program": {"language", "locale", "rights_component_id", "title", "translation_state"},
    "course": {"curriculum_role", "prerequisite_text", "program_id", "rights_component_id", "title", "translation_state"},
    "resource": {"author", "license_expression", "rights_component_id", "source_locale", "source_url", "title", "translation_state"},
    "edition": {"archive_bytes", "archive_path", "archive_sha256", "commit_sha", "local_derivative_unit_id", "resource_id", "rights_component_id", "source_line_end", "source_line_start", "source_path", "translation_state", "tree_identity_status"},
    "unit": {"concept_ids", "course_id", "display_title", "edition_id", "locale", "order", "parent_id", "path", "program_id", "provenance_relation", "resource_id", "rights_component_id", "source_local_id", "target_locator", "translation_state", "unit_kind"},
    "segment": {"concept_ids", "edition_id", "locale", "order", "provenance_relation", "resource_id", "rights_component_id", "segment_kind", "source_local_id", "source_locator", "target_locator", "translation_state", "unit_id"},
    "concept": {"canonical_label", "domain", "locale_neutral"},
    "term": {"concept_id", "evidence_segment_id", "locale", "preferred", "register", "rejected_forms", "rights_component_id", "scope_unit_id", "variants"},
    "relation": {"from_id", "note", "relation_type", "to_id"},
    "rights": {"attribution", "change_notice", "component_scope", "license_expression", "license_url", "non_endorsement", "third_party_status"},
    "asset": {"bytes", "edition_id", "media_type", "path", "resource_id", "rights_component_id", "role", "sha256"},
    "qa_event": {"note", "qa_type", "result", "unit_id", "witness_artifact_ids"},
    "artifact": {"bytes", "locale", "manifest_artifact_id", "media_type", "path", "qa_event_ids", "rights_component_id", "sha256", "toolchain", "translation_state", "unit_id"},
    "correction": {"affected_unit_ids", "correction_type", "edition_id", "evidence", "evidence_segment_id", "rationale", "resource_id", "source_defect", "target_change", "unit_id", "upstream_report_disposition"},
}
ID_PREFIX = {
    "program": "program:",
    "course": "course:",
    "resource": "resource:",
    "edition": "edition:",
    "unit": "unit:",
    "segment": "segment:",
    "concept": "concept:",
    "term": "term:",
    "relation": "relation:",
    "rights": "rights:",
    "asset": "asset:",
    "qa_event": "qa:",
    "artifact": "artifact:",
    "correction": "correction:",
}
ALLOWED_TRANSLATION_STATES = {
    "blocked",
    "built",
    "draft",
    "language_reviewed",
    "mathematically_reviewed",
    "published",
    "queued",
    "source_frozen",
    "structurally_verified",
    "superseded",
    "translated",
    "visually_checked",
}
ALLOWED_RELATIONS = {
    "adapts",
    "answers",
    "contains",
    "corrects",
    "depends-on",
    "exercises",
    "hints",
    "illustrates",
    "precedes",
    "prerequisite",
    "proves",
    "solves",
    "supersedes",
    "translates",
    "xref",
}
SCALAR_REFERENCE_FIELDS = {
    "concept_id",
    "course_id",
    "edition_id",
    "evidence_segment_id",
    "from_id",
    "local_derivative_unit_id",
    "manifest_artifact_id",
    "parent_id",
    "program_id",
    "resource_id",
    "rights_component_id",
    "scope_unit_id",
    "to_id",
    "unit_id",
}
LIST_REFERENCE_FIELDS = {
    "affected_unit_ids",
    "component_scope",
    "concept_ids",
    "qa_event_ids",
    "witness_artifact_ids",
}
KEY_RE = re.compile(r"^[a-z][a-z0-9_]*$")
HEX64_RE = re.compile(r"^[0-9a-f]{64}$")
HEX40_RE = re.compile(r"^[0-9a-f]{40}$")
TIMESTAMP_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
SOURCE_ID_RE = re.compile(r"\{[^}\n]*#([A-Za-z0-9-]+)[^}\n]*\}")


class ValidationError(Exception):
    """One or more backend invariants failed."""


def fail(message: str) -> None:
    raise ValidationError(message)


def no_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            fail(f"duplicate JSON key: {key}")
        out[key] = value
    return out


def canonical_json(record: dict[str, Any]) -> str:
    return json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def safe_path(lane_root: Path, relative: str) -> Path:
    rel = Path(relative)
    if rel.is_absolute() or ".." in rel.parts:
        fail(f"unsafe backend path: {relative!r}")
    resolved = (lane_root / rel).resolve()
    try:
        resolved.relative_to(lane_root)
    except ValueError:
        fail(f"backend path escapes lane root: {relative!r}")
    return resolved


def check_keys(value: Any, context: str) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if not KEY_RE.fullmatch(key):
                fail(f"{context}: non-locale-neutral key {key!r}")
            check_keys(child, f"{context}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            check_keys(child, f"{context}[{index}]")


def load_records(backend_dir: Path) -> tuple[list[dict[str, Any]], dict[str, str]]:
    present = {path.name for path in backend_dir.glob("*.jsonl")}
    missing = EXPECTED_FILES - present
    if missing:
        fail(f"missing required JSONL files: {sorted(missing)}")

    records: list[dict[str, Any]] = []
    owner_file: dict[str, str] = {}
    for path in sorted(backend_dir.glob("*.jsonl"), key=lambda item: item.name):
        raw = path.read_bytes()
        if raw.startswith(b"\xef\xbb\xbf"):
            fail(f"{path.name}: UTF-8 BOM is forbidden")
        if b"\r" in raw:
            fail(f"{path.name}: CR bytes are forbidden; JSONL must use LF")
        if not raw.endswith(b"\n"):
            fail(f"{path.name}: missing final LF")
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            fail(f"{path.name}: not valid UTF-8: {exc}")
        lines = text.splitlines()
        if any(not line for line in lines):
            fail(f"{path.name}: blank JSONL line")

        file_records: list[dict[str, Any]] = []
        for number, line in enumerate(lines, start=1):
            try:
                record = json.loads(line, object_pairs_hook=no_duplicate_keys)
            except (json.JSONDecodeError, ValidationError) as exc:
                fail(f"{path.name}:{number}: invalid JSON: {exc}")
            if not isinstance(record, dict):
                fail(f"{path.name}:{number}: record must be an object")
            if canonical_json(record) != line:
                fail(f"{path.name}:{number}: record is not canonical sorted compact JSON")
            check_keys(record, f"{path.name}:{number}")
            record_id = record.get("id")
            if not isinstance(record_id, str) or not record_id:
                fail(f"{path.name}:{number}: missing string id")
            if record_id in owner_file:
                fail(f"duplicate global id {record_id!r} in {owner_file[record_id]} and {path.name}")
            owner_file[record_id] = path.name
            file_records.append(record)

        ids = [record["id"] for record in file_records]
        if ids != sorted(ids):
            fail(f"{path.name}: records are not sorted by ordinal id")
        records.extend(file_records)
    return records, owner_file


def validate_shapes(records: list[dict[str, Any]]) -> None:
    for record in records:
        record_id = record["id"]
        entity_type = record.get("entity_type")
        if entity_type not in REQUIRED_BY_TYPE:
            fail(f"{record_id}: unknown entity_type {entity_type!r}")
        required = COMMON_FIELDS | REQUIRED_BY_TYPE[entity_type]
        missing = required - record.keys()
        if missing:
            fail(f"{record_id}: missing required fields {sorted(missing)}")
        if record["schema"] != SCHEMA or record["schema_version"] != SCHEMA_VERSION:
            fail(f"{record_id}: schema/version mismatch")
        if not record_id.startswith(ID_PREFIX[entity_type]):
            fail(f"{record_id}: wrong id prefix for {entity_type}")
        if record["status"] not in {"active", "pending"}:
            fail(f"{record_id}: unsupported status {record['status']!r}")
        if not isinstance(record["workflow"], str) or not record["workflow"]:
            fail(f"{record_id}: workflow must be non-empty")
        if record["supersedes"] is not None and not isinstance(record["supersedes"], str):
            fail(f"{record_id}: supersedes must be null or an id")
        if not isinstance(record["timestamp"], str) or not TIMESTAMP_RE.fullmatch(record["timestamp"]):
            fail(f"{record_id}: timestamp must be UTC second precision")
        if "translation_state" in record and record["translation_state"] not in ALLOWED_TRANSLATION_STATES:
            fail(f"{record_id}: invalid translation_state {record['translation_state']!r}")
        if "sha256" in record and not HEX64_RE.fullmatch(record["sha256"]):
            fail(f"{record_id}: invalid sha256")
        if entity_type == "edition" and not HEX40_RE.fullmatch(record["commit_sha"]):
            fail(f"{record_id}: invalid commit_sha")
        if entity_type == "concept" and record["locale_neutral"] is not True:
            fail(f"{record_id}: concept identity must be locale-neutral")
        if entity_type == "term" and record["locale"] != "id-ID":
            fail(f"{record_id}: term locale must be id-ID")
        if entity_type == "relation" and record["relation_type"] not in ALLOWED_RELATIONS:
            fail(f"{record_id}: unsupported relation type {record['relation_type']!r}")
        if entity_type == "qa_event":
            if record["status"] == "pending" and record["result"] != "not_run":
                fail(f"{record_id}: pending QA must have result not_run")
            if record["status"] == "active" and record["result"] != "passed":
                fail(f"{record_id}: completed QA must have result passed")


def validate_references(records: list[dict[str, Any]], by_id: dict[str, dict[str, Any]]) -> None:
    for record in records:
        record_id = record["id"]
        for field in SCALAR_REFERENCE_FIELDS:
            if field not in record or record[field] is None:
                continue
            value = record[field]
            if not isinstance(value, str):
                fail(f"{record_id}.{field}: expected id string")
            if value not in by_id:
                fail(f"{record_id}.{field}: unknown reference {value!r}")
        for field in LIST_REFERENCE_FIELDS:
            if field not in record:
                continue
            value = record[field]
            if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
                fail(f"{record_id}.{field}: expected list of ids")
            for item in value:
                if item not in by_id:
                    fail(f"{record_id}.{field}: unknown reference {item!r}")
        if record.get("supersedes") is not None and record["supersedes"] not in by_id:
            fail(f"{record_id}.supersedes: unknown reference")


def validate_files_and_spans(
    records: list[dict[str, Any]], by_id: dict[str, dict[str, Any]], lane_root: Path
) -> None:
    file_cache: dict[Path, tuple[bytes, str, list[bytes]]] = {}

    def cached(path: Path) -> tuple[bytes, str, list[bytes]]:
        if path not in file_cache:
            raw = path.read_bytes()
            file_cache[path] = (raw, sha256_bytes(raw), raw.splitlines(keepends=True))
        return file_cache[path]

    for record in records:
        record_id = record["id"]
        if record["entity_type"] in {"asset", "artifact"}:
            path = safe_path(lane_root, record["path"])
            if not path.is_file():
                fail(f"{record_id}: missing file {record['path']}")
            if path.stat().st_size != record["bytes"]:
                fail(f"{record_id}: byte count mismatch")
            if sha256_file(path) != record["sha256"]:
                fail(f"{record_id}: file hash mismatch")

        if record["entity_type"] == "edition":
            path = safe_path(lane_root, record["archive_path"])
            if not path.is_file():
                fail(f"{record_id}: missing frozen archive")
            if path.stat().st_size != record["archive_bytes"]:
                fail(f"{record_id}: archive byte count mismatch")
            if sha256_file(path) != record["archive_sha256"]:
                fail(f"{record_id}: archive hash mismatch")

        if record["entity_type"] not in {"unit", "segment"}:
            continue
        locator = record["target_locator"]
        needed = {"content_sha256", "file_sha256", "line_end", "line_start", "path"}
        if not isinstance(locator, dict) or needed - locator.keys():
            fail(f"{record_id}: incomplete target_locator")
        path = safe_path(lane_root, locator["path"])
        if not path.is_file():
            fail(f"{record_id}: missing target source {locator['path']}")
        raw, file_hash, lines = cached(path)
        if file_hash != locator["file_sha256"]:
            fail(f"{record_id}: target file hash mismatch")
        start, end = locator["line_start"], locator["line_end"]
        if not isinstance(start, int) or not isinstance(end, int) or not (1 <= start <= end <= len(lines)):
            fail(f"{record_id}: invalid target line span {start}-{end}")
        span_hash = sha256_bytes(b"".join(lines[start - 1 : end]))
        if span_hash != locator["content_sha256"]:
            fail(f"{record_id}: target span hash mismatch")
        source_local_id = record["source_local_id"]
        if source_local_id is not None:
            first_line = lines[start - 1].decode("utf-8")
            if source_local_id not in first_line:
                fail(f"{record_id}: source_local_id not anchored at target line_start")

    source_path = safe_path(lane_root, "source/id-ID/reader-unit-001.md")
    source_text = source_path.read_text(encoding="utf-8")
    source_ids = set(SOURCE_ID_RE.findall(source_text))
    unit_ids = {
        record["source_local_id"]
        for record in records
        if record["entity_type"] == "unit" and record["source_local_id"] is not None
    }
    segment_ids = {
        record["source_local_id"]
        for record in records
        if record["entity_type"] == "segment"
    }
    if unit_ids != source_ids:
        fail(f"stable source ids vs unit records differ: missing={sorted(source_ids-unit_ids)}, extra={sorted(unit_ids-source_ids)}")
    if segment_ids != source_ids:
        fail(f"stable source ids vs segment records differ: missing={sorted(source_ids-segment_ids)}, extra={sorted(segment_ids-source_ids)}")

    segments_by_local = {
        record["source_local_id"]: record
        for record in records
        if record["entity_type"] == "segment"
    }
    for unit in (record for record in records if record["entity_type"] == "unit" and record["source_local_id"]):
        segment = segments_by_local[unit["source_local_id"]]
        if segment["unit_id"] != unit["id"]:
            fail(f"{segment['id']}: unit linkage mismatch")
        if segment["target_locator"] != unit["target_locator"]:
            fail(f"{segment['id']}: segment/unit locator mismatch")


def validate_hierarchy_and_mastery(records: list[dict[str, Any]], by_id: dict[str, dict[str, Any]]) -> None:
    units = [record for record in records if record["entity_type"] == "unit"]
    unit_by_id = {record["id"]: record for record in units}
    roots = [record for record in units if record["unit_kind"] == "reader_unit"]
    if len(roots) != 1:
        fail(f"expected exactly one reader_unit root, found {len(roots)}")

    sibling_orders: defaultdict[str, list[int]] = defaultdict(list)
    for unit in units:
        record_id = unit["id"]
        path = unit["path"]
        if not isinstance(path, list) or not path or path[-1] != record_id:
            fail(f"{record_id}: invalid unit path")
        if any(item not in unit_by_id for item in path):
            fail(f"{record_id}: unit path contains non-unit id")
        parent_id = unit["parent_id"]
        if parent_id in unit_by_id:
            if path[:-1] != unit_by_id[parent_id]["path"]:
                fail(f"{record_id}: path does not extend parent path")
        elif len(path) != 1:
            fail(f"{record_id}: non-unit parent requires a root-length path")
        if not isinstance(unit["order"], int) or unit["order"] < 1:
            fail(f"{record_id}: order must be a positive integer")
        sibling_orders[parent_id].append(unit["order"])
    for parent_id, orders in sibling_orders.items():
        if len(orders) != len(set(orders)):
            fail(f"{parent_id}: duplicate child order values")

    relations = [record for record in records if record["entity_type"] == "relation"]
    solves = [record for record in relations if record["relation_type"] == "solves"]
    exercises = {record["id"] for record in units if record["unit_kind"] == "exercise"}
    solutions = {record["id"] for record in units if record["unit_kind"] == "solution"}
    exercise_links: Counter[str] = Counter()
    solution_links: Counter[str] = Counter()
    for relation in solves:
        if relation["from_id"] not in solutions or relation["to_id"] not in exercises:
            fail(f"{relation['id']}: solves must link solution -> exercise")
        solution_links[relation["from_id"]] += 1
        exercise_links[relation["to_id"]] += 1
    if set(exercise_links) != exercises or any(count != 1 for count in exercise_links.values()):
        fail("every exercise must have exactly one solves relation")
    if set(solution_links) != solutions or any(count != 1 for count in solution_links.values()):
        fail("every solution must solve exactly one exercise")


def validate_artifact_manifest(records: list[dict[str, Any]], lane_root: Path) -> None:
    artifacts = {record["path"]: record for record in records if record["entity_type"] == "artifact"}
    manifest_path = safe_path(lane_root, "output/ARTIFACT_MANIFEST.csv")
    raw = manifest_path.read_text(encoding="utf-8-sig")
    reader = csv.DictReader(io.StringIO(raw))
    if reader.fieldnames != ["path", "bytes", "sha256"]:
        fail("artifact manifest header must be path,bytes,sha256")
    seen: set[str] = set()
    for row in reader:
        relative = row["path"]
        if relative in seen:
            fail(f"artifact manifest duplicates {relative}")
        seen.add(relative)
        path = safe_path(lane_root, relative)
        if not path.is_file():
            fail(f"artifact manifest path is missing: {relative}")
        try:
            expected_bytes = int(row["bytes"])
        except ValueError:
            fail(f"artifact manifest has invalid byte count for {relative}")
        if path.stat().st_size != expected_bytes or sha256_file(path) != row["sha256"]:
            fail(f"artifact manifest mismatch for {relative}")
        if relative not in artifacts:
            fail(f"artifact manifest path lacks backend artifact record: {relative}")
        artifact = artifacts[relative]
        if artifact["bytes"] != expected_bytes or artifact["sha256"] != row["sha256"]:
            fail(f"backend artifact disagrees with manifest for {relative}")
    required_outputs = {"output/html/index.html", "output/pdf/topologi-aljabar-unit-001-id.pdf"}
    if seen != required_outputs:
        fail(f"artifact manifest output set differs: {sorted(seen)}")


def summarize(records: Iterable[dict[str, Any]], backend_dir: Path) -> None:
    counts = Counter(record["entity_type"] for record in records)
    files = sorted(backend_dir.glob("*.jsonl"), key=lambda item: item.name)
    digest = hashlib.sha256()
    for path in files:
        digest.update(path.name.encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
    print("backend validation: PASS")
    print(f"schema: {SCHEMA} {SCHEMA_VERSION}")
    print(f"records: {sum(counts.values())}")
    print("entities: " + ", ".join(f"{key}={counts[key]}" for key in sorted(counts)))
    print(f"jsonl_files: {len(files)}")
    print(f"backend_bundle_sha256: {digest.hexdigest()}")


def main() -> int:
    script_path = Path(__file__).resolve()
    lane_root = script_path.parent.parent.resolve()
    backend_dir = lane_root / "backend"
    try:
        records, _ = load_records(backend_dir)
        by_id = {record["id"]: record for record in records}
        validate_shapes(records)
        validate_references(records, by_id)
        validate_files_and_spans(records, by_id, lane_root)
        validate_hierarchy_and_mastery(records, by_id)
        validate_artifact_manifest(records, lane_root)
        summarize(records, backend_dir)
    except (OSError, ValidationError) as exc:
        print(f"backend validation: FAIL: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
