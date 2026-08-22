#!/usr/bin/env python3
"""Validate the locale-neutral Units 001-007 interoperability backend.

The validator is deliberately self-contained and offline.  It checks canonical
JSONL serialization, referential integrity, source-span hashes, artifact hashes,
the historical manifests, the frozen Units 001-007 manifest, and complete
mastery linkage.
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
    "local_derivative_unit_ids",
    "qa_event_ids",
    "witness_artifact_ids",
}
KEY_RE = re.compile(r"^[a-z][a-z0-9_]*$")
HEX64_RE = re.compile(r"^[0-9a-f]{64}$")
HEX40_RE = re.compile(r"^[0-9a-f]{40}$")
TIMESTAMP_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
SOURCE_ID_RE = re.compile(r"\{[^}\n]*#([A-Za-z0-9-]+)[^}\n]*\}")
SOURCE_FILES = {
    "source/id-ID/reader-unit-001.md": "c80b51c22a2fa7ea116201028b78d5f8d708ef4d8355d34092ac7a9c88415e15",
    "source/id-ID/units/unit-002-lecture-002.md": "4d2acc43557db9b3c419ee177545d285b9fcf50b2aa2dd3b2c6c44182f3a6a01",
    "source/id-ID/units/unit-003-lecture-003.md": "993e5941895a9b6f4b197b4c236f5a4990f6ae621e2bb7911353b28a5e1abffd",
    "source/id-ID/units/unit-004-lecture-004.md": "826fcb368275cdad02f72a5cec951fc8466ba68b09ca0139d72c81a4c5591fea",
    "source/id-ID/units/unit-005-lecture-005.md": "7333a7b7a92b9618016412abb5c9b2b2a398538f690d0109d4282289a0719852",
    "source/id-ID/units/unit-006-lecture-006.md": "3cb182fdf183bd67e45a898228b995a44d4638e808fdfbe6ea6d6a2a2b889e33",
    "source/id-ID/units/unit-007-lecture-007.md": "556cea5445e1b0a51f86f1c0ea0e80c4e00a17d365d95fa530f063cc24856569",
}
SOURCE_LINE_COUNTS = {
    "source/id-ID/reader-unit-001.md": 225,
    "source/id-ID/units/unit-002-lecture-002.md": 674,
    "source/id-ID/units/unit-003-lecture-003.md": 618,
    "source/id-ID/units/unit-004-lecture-004.md": 632,
    "source/id-ID/units/unit-005-lecture-005.md": 663,
    "source/id-ID/units/unit-006-lecture-006.md": 893,
    "source/id-ID/units/unit-007-lecture-007.md": 749,
}
EXPECTED_SOURCE_ID_COUNT = 224
ARTIFACT_MANIFESTS = {
    "output/ARTIFACT_MANIFEST.csv": {
        "required": True,
        "outputs": {
            "output/html/index.html",
            "output/pdf/topologi-aljabar-unit-001-id.pdf",
        },
    },
    "output/ARTIFACT_MANIFEST_UNITS_001_002.csv": {
        "required": True,
        "outputs": {
            "output/html/units-001-002/index.html",
            "output/pdf/topologi-aljabar-unit-001-002-id.pdf",
        },
    },
    "output/ARTIFACT_MANIFEST_UNITS_001_003.csv": {
        "required": True,
        "outputs": {
            "output/html/units-001-003/index.html",
            "output/pdf/topologi-aljabar-unit-001-003-id.pdf",
        },
    },
    "output/ARTIFACT_MANIFEST_UNITS_001_004.csv": {
        "required": True,
        "outputs": {
            "output/html/units-001-004/index.html",
            "output/pdf/topologi-aljabar-unit-001-004-id.pdf",
        },
    },
    "output/ARTIFACT_MANIFEST_UNITS_001_005.csv": {
        "required": True,
        "outputs": {
            "output/html/units-001-005/index.html",
            "output/pdf/topologi-aljabar-unit-001-005-id.pdf",
        },
    },
    "output/ARTIFACT_MANIFEST_UNITS_001_007.csv": {
        "required": True,
        "outputs": {
            "output/html/units-001-007/index.html",
            "output/pdf/topologi-aljabar-unit-001-007-id.pdf",
        },
    },
}
EXPECTED_UNIT3_ADVERSE_IDS = {f"O012-ADV-{number:04d}" for number in range(21, 35)}
EXPECTED_UNIT3_REFLOW_IDS = {f"O012-ADV-{number:04d}" for number in range(30, 34)}
EXPECTED_UNIT4_ADVERSE_IDS = {f"O012-ADV-{number:04d}" for number in range(35, 54)}
EXPECTED_UNIT4_REFLOW_IDS = {"O012-ADV-0038"}
EXPECTED_UNIT5_ADVERSE_IDS = {f"O012-ADV-{number:04d}" for number in range(54, 71)}
EXPECTED_UNIT5_REFLOW_IDS = {"O012-ADV-0070"}
EXPECTED_UNIT6_ADVERSE_IDS = {f"O012-ADV-{number:04d}" for number in range(71, 83)}
EXPECTED_UNIT6_REFLOW_IDS = {"O012-ADV-0082"}
EXPECTED_UNIT7_ADVERSE_IDS = {f"O012-ADV-{number:04d}" for number in range(83, 95)}
EXPECTED_UNIT7_REFLOW_IDS = {"O012-ADV-0087", "O012-ADV-0088"}
EXPECTED_UNIT7_ALIAS_IDS = {"O012-ADV-0094"}


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

    source_id_paths: dict[str, str] = {}
    for relative, expected_hash in SOURCE_FILES.items():
        source_path = safe_path(lane_root, relative)
        raw, file_hash, _ = cached(source_path)
        if file_hash != expected_hash:
            fail(f"frozen source hash mismatch for {relative}")
        try:
            source_text = raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            fail(f"{relative}: source is not valid UTF-8: {exc}")
        local_ids = SOURCE_ID_RE.findall(source_text)
        duplicates = sorted(record_id for record_id, count in Counter(local_ids).items() if count != 1)
        if duplicates:
            fail(f"{relative}: duplicate stable source ids {duplicates}")
        for source_id in local_ids:
            if source_id in source_id_paths:
                fail(f"stable source id occurs in two source files: {source_id}")
            source_id_paths[source_id] = relative

    source_ids = set(source_id_paths)
    if len(source_ids) != EXPECTED_SOURCE_ID_COUNT:
        fail(f"expected {EXPECTED_SOURCE_ID_COUNT} stable source ids, found {len(source_ids)}")

    for entity_type in ("unit", "segment"):
        local_ids = [
            record["source_local_id"]
            for record in records
            if record["entity_type"] == entity_type and record["source_local_id"] is not None
        ]
        counts = Counter(local_ids)
        mapped_ids = set(counts)
        duplicates = sorted(record_id for record_id, count in counts.items() if count != 1)
        if duplicates:
            fail(f"duplicate {entity_type} mappings for stable source ids: {duplicates}")
        if mapped_ids != source_ids:
            fail(
                f"stable source ids vs {entity_type} records differ: "
                f"missing={sorted(source_ids-mapped_ids)}, extra={sorted(mapped_ids-source_ids)}"
            )

    for record in records:
        if record["entity_type"] not in {"unit", "segment"}:
            continue
        source_local_id = record["source_local_id"]
        if source_local_id is None:
            if record["entity_type"] != "unit" or record["unit_kind"] != "reader_unit":
                fail(f"{record['id']}: only reader_unit roots may omit source_local_id")
            continue
        expected_path = source_id_paths[source_local_id]
        if record["target_locator"]["path"] != expected_path:
            fail(f"{record['id']}: target source does not contain its stable source id")

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
    root_paths = [record["target_locator"]["path"] for record in roots]
    if len(roots) != len(SOURCE_FILES) or set(root_paths) != set(SOURCE_FILES):
        fail(
            "expected exactly one reader_unit root for each frozen source file; "
            f"found roots for {sorted(root_paths)}"
        )
    for root in roots:
        locator = root["target_locator"]
        relative = locator["path"]
        if root["parent_id"] != root["course_id"] or by_id[root["parent_id"]]["entity_type"] != "course":
            fail(f"{root['id']}: reader_unit root must be parented by its course")
        if (
            locator["line_start"] != 1
            or locator["line_end"] != SOURCE_LINE_COUNTS[relative]
            or locator["content_sha256"] != SOURCE_FILES[relative]
        ):
            fail(f"{root['id']}: reader_unit root must span its complete frozen source file")

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
        elif len(path) != 1 or unit["unit_kind"] != "reader_unit":
            fail(f"{record_id}: only reader_unit roots may have a non-unit parent")
        if not isinstance(unit["order"], int) or unit["order"] < 1:
            fail(f"{record_id}: order must be a positive integer")
        sibling_orders[parent_id].append(unit["order"])

        root = unit_by_id[path[0]]
        if root["unit_kind"] != "reader_unit":
            fail(f"{record_id}: unit path does not begin at a reader_unit root")
        if unit["target_locator"]["path"] != root["target_locator"]["path"]:
            fail(f"{record_id}: unit target source differs from its reader_unit root")
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

    answers = [record for record in relations if record["relation_type"] == "answers"]
    questions = {record["id"] for record in units if record["unit_kind"] == "question"}
    answer_units = {record["id"] for record in units if record["unit_kind"] == "answer"}
    question_links: Counter[str] = Counter()
    answer_links: Counter[str] = Counter()
    for relation in answers:
        if relation["from_id"] not in answer_units or relation["to_id"] not in questions:
            fail(f"{relation['id']}: answers must link answer -> question")
        answer_links[relation["from_id"]] += 1
        question_links[relation["to_id"]] += 1
    if set(question_links) != questions or any(count != 1 for count in question_links.values()):
        fail("every formal question must have exactly one answers relation")
    if set(answer_links) != answer_units or any(count != 1 for count in answer_links.values()):
        fail("every answer must answer exactly one formal question")


def validate_unit7_boundary(records: list[dict[str, Any]], by_id: dict[str, dict[str, Any]]) -> None:
    edition = by_id["edition:roberts-at-2019-b947ad2"]
    expected_roots = {
        "unit:o012-rbt-u001",
        "unit:o012-rbt-u002",
        "unit:o012-rbt-u003",
        "unit:o012-rbt-u004",
        "unit:o012-rbt-u005",
        "unit:o012-rbt-u006",
        "unit:o012-rbt-u007",
    }
    if edition["source_line_start"] != 134 or edition["source_line_end"] != 1770:
        fail("Roberts edition coverage must be the contiguous admitted range Notes.tex:134-1770")
    derivative_roots = edition.get("local_derivative_unit_ids")
    if not isinstance(derivative_roots, list) or set(derivative_roots) != expected_roots:
        fail("Roberts edition must enumerate the seven local derivative reader roots")

    expected_source_assets = {
        "asset:o012-u001-source-markdown": "source/id-ID/reader-unit-001.md",
        "asset:o012-u002-source-markdown": "source/id-ID/units/unit-002-lecture-002.md",
        "asset:o012-u003-source-markdown": "source/id-ID/units/unit-003-lecture-003.md",
        "asset:o012-u004-source-markdown": "source/id-ID/units/unit-004-lecture-004.md",
        "asset:o012-u005-source-markdown": "source/id-ID/units/unit-005-lecture-005.md",
        "asset:o012-u006-source-markdown": "source/id-ID/units/unit-006-lecture-006.md",
        "asset:o012-u007-source-markdown": "source/id-ID/units/unit-007-lecture-007.md",
    }
    for asset_id, expected_path in expected_source_assets.items():
        asset = by_id.get(asset_id)
        if asset is None or asset.get("path") != expected_path or asset.get("role") != "canonical_reader_source":
            fail(f"{asset_id}: missing or malformed canonical reader-source asset")

    unit3_corrections = [
        record
        for record in records
        if record["entity_type"] == "correction" and record["unit_id"] == "unit:o012-rbt-u003"
    ]
    adverse_ids = {record.get("adverse_ledger_id") for record in unit3_corrections}
    if adverse_ids != EXPECTED_UNIT3_ADVERSE_IDS or len(unit3_corrections) != len(EXPECTED_UNIT3_ADVERSE_IDS):
        fail("Unit 003 corrections must map one-to-one to O012-ADV-0021 through O012-ADV-0034")
    reflow_ids = {
        record["adverse_ledger_id"]
        for record in unit3_corrections
        if record["correction_type"] == "structural_adaptation"
    }
    if reflow_ids != EXPECTED_UNIT3_REFLOW_IDS:
        fail("Unit 003 structural reflows must be exactly O012-ADV-0030 through O012-ADV-0033")

    unit4_corrections = [
        record
        for record in records
        if record["entity_type"] == "correction" and record["unit_id"] == "unit:o012-rbt-u004"
    ]
    adverse_ids = {record.get("adverse_ledger_id") for record in unit4_corrections}
    if adverse_ids != EXPECTED_UNIT4_ADVERSE_IDS or len(unit4_corrections) != len(EXPECTED_UNIT4_ADVERSE_IDS):
        fail("Unit 004 corrections must map one-to-one to O012-ADV-0035 through O012-ADV-0053")
    reflow_ids = {
        record["adverse_ledger_id"]
        for record in unit4_corrections
        if record["correction_type"] == "structural_adaptation"
    }
    if reflow_ids != EXPECTED_UNIT4_REFLOW_IDS:
        fail("Unit 004 structural reflow must be exactly O012-ADV-0038")

    unit4_path = "source/id-ID/units/unit-004-lecture-004.md"
    expected_upstream_locator = {
        "commit_sha": "b947ad2e9f9e301bfe24590a9db653bc54fa1a53",
        "line_end": 1131,
        "line_start": 878,
        "path": "Notes.tex",
        "precision": "unit_range_only",
    }
    expected_original_locator = {
        "kind": "edition_original",
        "path": unit4_path,
        "precision": "exact_target_span",
    }
    unit4_segments = [
        record
        for record in records
        if record["entity_type"] == "segment" and record["target_locator"]["path"] == unit4_path
    ]
    if len(unit4_segments) != 33:
        fail(f"Unit 004 must have 33 stable-id segments; found {len(unit4_segments)}")
    for segment in unit4_segments:
        expected = (
            expected_original_locator
            if segment["provenance_relation"] == "edition_original"
            else expected_upstream_locator
        )
        if segment["source_locator"] != expected:
            fail(f"{segment['id']}: malformed Unit 004 source authority locator")

    unit5_corrections = [
        record
        for record in records
        if record["entity_type"] == "correction" and record["unit_id"] == "unit:o012-rbt-u005"
    ]
    adverse_ids = {record.get("adverse_ledger_id") for record in unit5_corrections}
    if adverse_ids != EXPECTED_UNIT5_ADVERSE_IDS or len(unit5_corrections) != len(EXPECTED_UNIT5_ADVERSE_IDS):
        fail("Unit 005 corrections must map one-to-one to O012-ADV-0054 through O012-ADV-0070")
    reflow_ids = {
        record["adverse_ledger_id"]
        for record in unit5_corrections
        if record["correction_type"] == "structural_adaptation"
    }
    if reflow_ids != EXPECTED_UNIT5_REFLOW_IDS:
        fail("Unit 005 structural reflow must be exactly O012-ADV-0070")

    unit5_path = "source/id-ID/units/unit-005-lecture-005.md"
    expected_unit5_upstream_locator = {
        "commit_sha": "b947ad2e9f9e301bfe24590a9db653bc54fa1a53",
        "line_end": 1304,
        "line_start": 1132,
        "path": "Notes.tex",
        "precision": "unit_range_only",
    }
    expected_unit5_original_locator = {
        "kind": "edition_original",
        "path": unit5_path,
        "precision": "exact_target_span",
    }
    unit5_segments = [
        record
        for record in records
        if record["entity_type"] == "segment" and record["target_locator"]["path"] == unit5_path
    ]
    if len(unit5_segments) != 30:
        fail(f"Unit 005 must have 30 stable-id segments; found {len(unit5_segments)}")
    for segment in unit5_segments:
        expected = (
            expected_unit5_original_locator
            if segment["provenance_relation"] == "edition_original"
            else expected_unit5_upstream_locator
        )
        if segment["source_locator"] != expected:
            fail(f"{segment['id']}: malformed Unit 005 source authority locator")

    unit6_corrections = [
        record for record in records
        if record["entity_type"] == "correction" and record["unit_id"] == "unit:o012-rbt-u006"
    ]
    adverse_ids = {record.get("adverse_ledger_id") for record in unit6_corrections}
    if adverse_ids != EXPECTED_UNIT6_ADVERSE_IDS or len(unit6_corrections) != len(EXPECTED_UNIT6_ADVERSE_IDS):
        fail("Unit 006 corrections must map one-to-one to O012-ADV-0071 through O012-ADV-0082")
    reflow_ids = {
        record["adverse_ledger_id"] for record in unit6_corrections
        if record["correction_type"] == "structural_adaptation"
    }
    if reflow_ids != EXPECTED_UNIT6_REFLOW_IDS:
        fail("Unit 006 structural reflow must be exactly O012-ADV-0082")

    unit7_corrections = [
        record for record in records
        if record["entity_type"] == "correction" and record["unit_id"] == "unit:o012-rbt-u007"
    ]
    adverse_ids = {record.get("adverse_ledger_id") for record in unit7_corrections}
    if adverse_ids != EXPECTED_UNIT7_ADVERSE_IDS or len(unit7_corrections) != len(EXPECTED_UNIT7_ADVERSE_IDS):
        fail("Unit 007 corrections must map one-to-one to O012-ADV-0083 through O012-ADV-0094")
    reflow_ids = {
        record["adverse_ledger_id"] for record in unit7_corrections
        if record["correction_type"] == "structural_adaptation"
    }
    if reflow_ids != EXPECTED_UNIT7_REFLOW_IDS:
        fail("Unit 007 structural reflows must be exactly O012-ADV-0087 and O012-ADV-0088")
    alias_ids = {
        record["adverse_ledger_id"] for record in unit7_corrections
        if record["correction_type"] == "identifier_preservation"
    }
    if alias_ids != EXPECTED_UNIT7_ALIAS_IDS:
        fail("Unit 007 identifier preservation must be exactly O012-ADV-0094")

    for lecture, path, upstream_start, upstream_end, expected_count in (
        (6, "source/id-ID/units/unit-006-lecture-006.md", 1305, 1515, 28),
        (7, "source/id-ID/units/unit-007-lecture-007.md", 1516, 1770, 24),
    ):
        expected_upstream = {
            "commit_sha": "b947ad2e9f9e301bfe24590a9db653bc54fa1a53",
            "line_end": upstream_end,
            "line_start": upstream_start,
            "path": "Notes.tex",
            "precision": "unit_range_only",
        }
        expected_original = {"kind": "edition_original", "path": path, "precision": "exact_target_span"}
        lecture_segments = [
            record for record in records
            if record["entity_type"] == "segment" and record["target_locator"]["path"] == path
        ]
        if len(lecture_segments) != expected_count:
            fail(f"Unit {lecture:03d} must have {expected_count} stable-id segments; found {len(lecture_segments)}")
        for segment in lecture_segments:
            expected = expected_original if segment["provenance_relation"] == "edition_original" else expected_upstream
            if segment["source_locator"] != expected:
                fail(f"{segment['id']}: malformed Unit {lecture:03d} source authority locator")

    alias_unit = by_id.get("unit:o012-rbt-l07-exa-003")
    alias_segment = by_id.get("segment:o012-rbt-l07-exa-003")
    if alias_unit is None or alias_unit.get("source_aliases") != ["eg:piS^1_infinite"]:
        fail("Unit 007 source alias missing from unit record")
    if alias_segment is None or alias_segment.get("source_aliases") != ["eg:piS^1_infinite"]:
        fail("Unit 007 source alias missing from segment record")

    expected_term_controls = {f"O012-TERM-{number:04d}" for number in range(115, 134)}
    unit67_terms = [
        record for record in records
        if record["entity_type"] == "term" and record.get("terminology_control_id") in expected_term_controls
    ]
    if len(unit67_terms) != 19 or {record.get("terminology_control_id") for record in unit67_terms} != expected_term_controls:
        fail("Units 006-007 terminology controls must map one-to-one to O012-TERM-0115 through O012-TERM-0133")

    cumulative_rights_id = "rights:o012-units-001-007-composite-cc-by-4.0"
    for authority_id in ("program:o012-id", "course:o012-d60"):
        if by_id[authority_id]["rights_component_id"] != cumulative_rights_id:
            fail(f"{authority_id}: must point at the cumulative Units 001-007 rights record")
    cumulative_rights = by_id.get(cumulative_rights_id)
    if cumulative_rights is None or set(cumulative_rights["component_scope"]) != expected_roots:
        fail("cumulative Units 001-007 rights scope is missing or incomplete")

    unit4_cumulative_rights_id = "rights:o012-units-001-004-composite-cc-by-4.0"
    unit5_cumulative_rights_id = "rights:o012-units-001-005-composite-cc-by-4.0"

    manifest_id = "artifact:o012-units-001-004-manifest"
    source_qa = "qa:o012-u004-source-integrity"
    math_qa = "qa:o012-u004-math-review"
    language_qa = "qa:o012-u004-language-review"
    build_qa = "qa:o012-units-001-004-build"
    accessibility_qa = "qa:o012-units-001-004-accessibility"
    visual_qa = "qa:o012-units-001-004-visual"
    expected_artifacts = {
        "artifact:o012-u004-independent-review": {
            "bytes": 3031,
            "manifest_artifact_id": None,
            "path": "qa/UNIT_004_INDEPENDENT_REVIEW.md",
            "qa_event_ids": {language_qa, math_qa, source_qa},
            "sha256": "ac993a10e22738197775ae5c3f4e72948983c4e99ff602a52943b40ed417b6f9",
        },
        "artifact:o012-units-001-004-html": {
            "bytes": 494732,
            "manifest_artifact_id": manifest_id,
            "path": "output/html/units-001-004/index.html",
            "qa_event_ids": {accessibility_qa, build_qa, visual_qa},
            "sha256": "8c8f5e1ad8172a2d97e3931fc3b4f2a3aa7f9e8a709260a27103f7eca0f1357d",
        },
        manifest_id: {
            "bytes": 247,
            "manifest_artifact_id": None,
            "path": "output/ARTIFACT_MANIFEST_UNITS_001_004.csv",
            "qa_event_ids": {build_qa},
            "sha256": "4c8bf407e426feb8db92308c4b28bdbbc0738416a85a13539ef7915e4c1aad83",
        },
        "artifact:o012-units-001-004-pdf": {
            "bytes": 539006,
            "manifest_artifact_id": manifest_id,
            "path": "output/pdf/topologi-aljabar-unit-001-004-id.pdf",
            "qa_event_ids": {accessibility_qa, build_qa, visual_qa},
            "sha256": "5e92c4c6ed60bca9f2f4d362d4c48b4f01aa156b330e2adacd1bf88dd7de9e87",
        },
        "artifact:o012-units-001-004-qa-receipt": {
            "bytes": 4478,
            "manifest_artifact_id": None,
            "path": "qa/UNITS_001_004_QA.json",
            "qa_event_ids": {language_qa, math_qa, source_qa, accessibility_qa, build_qa, visual_qa},
            "sha256": "1670bbe2377712c9f96b9a68cdb75589ae461512f77cea7ad0c9290193724bd5",
        },
        "artifact:o012-units-001-004-qa-text": {
            "bytes": 100684,
            "manifest_artifact_id": None,
            "path": "qa/units-001-004-extracted.txt",
            "qa_event_ids": {math_qa, build_qa},
            "sha256": "3d27bc1ab5a780bffce12d5951623b60929069238a210961740234502e71bf35",
        },
        "artifact:o012-units-001-004-visual-receipt": {
            "bytes": 2257,
            "manifest_artifact_id": None,
            "path": "qa/UNITS_001_004_VISUAL_QA.md",
            "qa_event_ids": {accessibility_qa, visual_qa},
            "sha256": "74e609e94ea47b89db223c21e12cae682048f0a60d8780dae96d5b0164f2c5ca",
        },
    }
    unit4_artifact_ids = {
        record["id"]
        for record in records
        if record["entity_type"] == "artifact" and record["unit_id"] == "unit:o012-rbt-u004"
    }
    if unit4_artifact_ids != set(expected_artifacts):
        fail(
            "Unit 004 final artifact inventory differs: "
            f"missing={sorted(set(expected_artifacts)-unit4_artifact_ids)}, "
            f"extra={sorted(unit4_artifact_ids-set(expected_artifacts))}"
        )
    for artifact_id, expected in expected_artifacts.items():
        artifact = by_id[artifact_id]
        for field in ("bytes", "manifest_artifact_id", "path", "sha256"):
            if artifact[field] != expected[field]:
                fail(f"{artifact_id}: final boundary {field} mismatch")
        if set(artifact["qa_event_ids"]) != expected["qa_event_ids"]:
            fail(f"{artifact_id}: final boundary QA linkage mismatch")
        if artifact["rights_component_id"] != unit4_cumulative_rights_id:
            fail(f"{artifact_id}: must use cumulative Units 001-004 rights")

    expected_qa = {
        source_qa: ("source", {"artifact:o012-u004-independent-review", "artifact:o012-units-001-004-qa-receipt"}),
        math_qa: ("math", {"artifact:o012-u004-independent-review", "artifact:o012-units-001-004-qa-receipt", "artifact:o012-units-001-004-qa-text"}),
        language_qa: ("language", {"artifact:o012-u004-independent-review"}),
        build_qa: ("build", {"artifact:o012-units-001-004-html", manifest_id, "artifact:o012-units-001-004-pdf", "artifact:o012-units-001-004-qa-receipt", "artifact:o012-units-001-004-qa-text"}),
        accessibility_qa: ("accessibility", {"artifact:o012-units-001-004-html", "artifact:o012-units-001-004-qa-receipt", "artifact:o012-units-001-004-visual-receipt"}),
        visual_qa: ("visual", {"artifact:o012-units-001-004-html", "artifact:o012-units-001-004-pdf", "artifact:o012-units-001-004-visual-receipt"}),
    }
    unit4_qa_ids = {
        record["id"]
        for record in records
        if record["entity_type"] == "qa_event" and record["unit_id"] == "unit:o012-rbt-u004"
    }
    if unit4_qa_ids != set(expected_qa):
        fail(
            "Unit 004 final QA-event inventory differs: "
            f"missing={sorted(set(expected_qa)-unit4_qa_ids)}, extra={sorted(unit4_qa_ids-set(expected_qa))}"
        )
    for qa_id, (qa_type, witnesses) in expected_qa.items():
        qa_event = by_id[qa_id]
        if qa_event["qa_type"] != qa_type or qa_event["result"] != "passed":
            fail(f"{qa_id}: final QA result/type mismatch")
        if set(qa_event["witness_artifact_ids"]) != witnesses:
            fail(f"{qa_id}: final witness inventory mismatch")

    manifest5 = "artifact:o012-units-001-005-manifest"
    source5_qa = "qa:o012-u005-source-integrity"
    math5_qa = "qa:o012-u005-math-review"
    language5_qa = "qa:o012-u005-language-review"
    build5_qa = "qa:o012-units-001-005-build"
    accessibility5_qa = "qa:o012-units-001-005-accessibility"
    visual5_qa = "qa:o012-units-001-005-visual"
    expected_artifacts5 = {
        "artifact:o012-u005-independent-review": {
            "bytes": 1592,
            "manifest_artifact_id": None,
            "path": "qa/UNIT_005_INDEPENDENT_REVIEW.md",
            "qa_event_ids": {language5_qa, math5_qa, source5_qa},
            "sha256": "399b81a06ac5701eca6604406c40acaa76f100291ee57f8efeb5344e7d7c8de0",
        },
        "artifact:o012-units-001-005-html": {
            "bytes": 610594,
            "manifest_artifact_id": manifest5,
            "path": "output/html/units-001-005/index.html",
            "qa_event_ids": {accessibility5_qa, build5_qa, visual5_qa},
            "sha256": "8d3accf480101565409909c05f987f44b73f1c98889128e2f5074a4e049f48f3",
        },
        manifest5: {
            "bytes": 247,
            "manifest_artifact_id": None,
            "path": "output/ARTIFACT_MANIFEST_UNITS_001_005.csv",
            "qa_event_ids": {build5_qa},
            "sha256": "2910fd87871675730aea7ca33e636a70d330d0f81183e887bad74ea1fd2d5190",
        },
        "artifact:o012-units-001-005-pdf": {
            "bytes": 589065,
            "manifest_artifact_id": manifest5,
            "path": "output/pdf/topologi-aljabar-unit-001-005-id.pdf",
            "qa_event_ids": {accessibility5_qa, build5_qa, visual5_qa},
            "sha256": "d6929434a9bc7ae78fb71fc060e9cc54dce85d37e4997ffe042ccbab982e64e2",
        },
        "artifact:o012-units-001-005-qa-receipt": {
            "bytes": 4768,
            "manifest_artifact_id": None,
            "path": "qa/UNITS_001_005_QA.json",
            "qa_event_ids": {language5_qa, math5_qa, source5_qa, accessibility5_qa, build5_qa, visual5_qa},
            "sha256": "ffb6703e4fe2ebc1c7733dc4f87a32c64c53cbe3ebf326d65a8d2da94765635a",
        },
        "artifact:o012-units-001-005-qa-text": {
            "bytes": 128786,
            "manifest_artifact_id": None,
            "path": "qa/units-001-005-extracted.txt",
            "qa_event_ids": {math5_qa, build5_qa},
            "sha256": "83aca1060966c7ca7a7852630c27926754f0d893749aeb80888bbfd00f56a725",
        },
        "artifact:o012-units-001-005-visual-receipt": {
            "bytes": 2877,
            "manifest_artifact_id": None,
            "path": "qa/UNITS_001_005_VISUAL_QA.md",
            "qa_event_ids": {accessibility5_qa, visual5_qa},
            "sha256": "ed8249702d8335b01dc40925af1d5b071fa18d2eef9fe628a5535bd9404fbcdd",
        },
    }
    unit5_artifact_ids = {
        record["id"]
        for record in records
        if record["entity_type"] == "artifact" and record["unit_id"] == "unit:o012-rbt-u005"
    }
    if unit5_artifact_ids != set(expected_artifacts5):
        fail(
            "Unit 005 final artifact inventory differs: "
            f"missing={sorted(set(expected_artifacts5)-unit5_artifact_ids)}, "
            f"extra={sorted(unit5_artifact_ids-set(expected_artifacts5))}"
        )
    for artifact_id, expected in expected_artifacts5.items():
        artifact = by_id[artifact_id]
        for field in ("bytes", "manifest_artifact_id", "path", "sha256"):
            if artifact[field] != expected[field]:
                fail(f"{artifact_id}: final Unit 005 boundary {field} mismatch")
        if set(artifact["qa_event_ids"]) != expected["qa_event_ids"]:
            fail(f"{artifact_id}: final Unit 005 boundary QA linkage mismatch")
        if artifact["rights_component_id"] != unit5_cumulative_rights_id:
            fail(f"{artifact_id}: must use cumulative Units 001-005 rights")

    expected_qa5 = {
        source5_qa: ("source", {"artifact:o012-u005-independent-review", "artifact:o012-units-001-005-qa-receipt"}),
        math5_qa: ("math", {"artifact:o012-u005-independent-review", "artifact:o012-units-001-005-qa-receipt", "artifact:o012-units-001-005-qa-text"}),
        language5_qa: ("language", {"artifact:o012-u005-independent-review"}),
        build5_qa: ("build", {"artifact:o012-units-001-005-html", manifest5, "artifact:o012-units-001-005-pdf", "artifact:o012-units-001-005-qa-receipt", "artifact:o012-units-001-005-qa-text"}),
        accessibility5_qa: ("accessibility", {"artifact:o012-units-001-005-html", "artifact:o012-units-001-005-qa-receipt", "artifact:o012-units-001-005-visual-receipt"}),
        visual5_qa: ("visual", {"artifact:o012-units-001-005-html", "artifact:o012-units-001-005-pdf", "artifact:o012-units-001-005-visual-receipt"}),
    }
    unit5_qa_ids = {
        record["id"]
        for record in records
        if record["entity_type"] == "qa_event" and record["unit_id"] == "unit:o012-rbt-u005"
    }
    if unit5_qa_ids != set(expected_qa5):
        fail(
            "Unit 005 final QA-event inventory differs: "
            f"missing={sorted(set(expected_qa5)-unit5_qa_ids)}, extra={sorted(unit5_qa_ids-set(expected_qa5))}"
        )
    for qa_id, (qa_type, witnesses) in expected_qa5.items():
        qa_event = by_id[qa_id]
        if qa_event["qa_type"] != qa_type or qa_event["result"] != "passed":
            fail(f"{qa_id}: final Unit 005 QA result/type mismatch")
        if set(qa_event["witness_artifact_ids"]) != witnesses:
            fail(f"{qa_id}: final Unit 005 witness inventory mismatch")

    manifest7 = "artifact:o012-units-001-007-manifest"
    source6_qa = "qa:o012-u006-source-integrity"
    math6_qa = "qa:o012-u006-math-review"
    language6_qa = "qa:o012-u006-language-review"
    source7_qa = "qa:o012-u007-source-integrity"
    math7_qa = "qa:o012-u007-math-review"
    language7_qa = "qa:o012-u007-language-review"
    build7_qa = "qa:o012-units-001-007-build"
    accessibility7_qa = "qa:o012-units-001-007-accessibility"
    visual7_qa = "qa:o012-units-001-007-visual"
    expected_artifacts67 = {
        "artifact:o012-u006-independent-review": {
            "bytes": 1783, "manifest_artifact_id": None,
            "path": "qa/UNIT_006_INDEPENDENT_REVIEW.md",
            "qa_event_ids": {source6_qa, math6_qa, language6_qa},
            "sha256": "5dd3868192a85e3e60562f42ec7d7b792e0e58811719ecc97207ed2bdc5de4bf",
            "unit_id": "unit:o012-rbt-u006",
        },
        "artifact:o012-u007-independent-review": {
            "bytes": 1761, "manifest_artifact_id": None,
            "path": "qa/UNIT_007_INDEPENDENT_REVIEW.md",
            "qa_event_ids": {source7_qa, math7_qa, language7_qa},
            "sha256": "87c5129cd7d367893860b150c72948de1d196d7cbefe04d53f7a4efecf921f87",
            "unit_id": "unit:o012-rbt-u007",
        },
        "artifact:o012-units-001-007-html": {
            "bytes": 899803, "manifest_artifact_id": manifest7,
            "path": "output/html/units-001-007/index.html",
            "qa_event_ids": {build7_qa, accessibility7_qa, visual7_qa},
            "sha256": "55135048eafe0f097c45936add885e008392eefdf475270fea37adf6a2a7b7bb",
            "unit_id": "unit:o012-rbt-u007",
        },
        manifest7: {
            "bytes": 247, "manifest_artifact_id": None,
            "path": "output/ARTIFACT_MANIFEST_UNITS_001_007.csv",
            "qa_event_ids": {build7_qa},
            "sha256": "7b279f0413892f0ddedce636b3a272884bb7bfa01410bf33a6ce34c0c34db2f9",
            "unit_id": "unit:o012-rbt-u007",
        },
        "artifact:o012-units-001-007-pdf": {
            "bytes": 702470, "manifest_artifact_id": manifest7,
            "path": "output/pdf/topologi-aljabar-unit-001-007-id.pdf",
            "qa_event_ids": {build7_qa, accessibility7_qa, visual7_qa},
            "sha256": "3764b75ecfb9200e25a165db1f0f97a680384378e2a9a22e129aab57dd860d93",
            "unit_id": "unit:o012-rbt-u007",
        },
        "artifact:o012-units-001-007-qa-receipt": {
            "bytes": 7384, "manifest_artifact_id": None,
            "path": "qa/UNITS_001_007_QA.json",
            "qa_event_ids": {source6_qa, math6_qa, language6_qa, source7_qa, math7_qa, language7_qa, build7_qa, accessibility7_qa, visual7_qa},
            "sha256": "2982a9465428eff97e6047bffdadba422b2dc0406e34750f632bfe148ed67617",
            "unit_id": "unit:o012-rbt-u007",
        },
        "artifact:o012-units-001-007-qa-text": {
            "bytes": 190424, "manifest_artifact_id": None,
            "path": "qa/units-001-007-extracted.txt",
            "qa_event_ids": {build7_qa, math6_qa, math7_qa},
            "sha256": "f6839e7eb7f25c8518ec3fc2e2372b82b1f1387b48402899ff8bc40ce153c8dc",
            "unit_id": "unit:o012-rbt-u007",
        },
        "artifact:o012-units-001-007-visual-receipt": {
            "bytes": 3259, "manifest_artifact_id": None,
            "path": "qa/UNITS_001_007_VISUAL_QA.md",
            "qa_event_ids": {accessibility7_qa, visual7_qa},
            "sha256": "63a4b4545213a7aec1c556a3852b818ba2f207b10cac7e80c62330709604176f",
            "unit_id": "unit:o012-rbt-u007",
        },
    }
    boundary_artifact_ids = {
        record["id"] for record in records
        if record["entity_type"] == "artifact" and record["id"] in expected_artifacts67
    }
    if boundary_artifact_ids != set(expected_artifacts67):
        fail(
            "Units 006-007 final artifact inventory differs: "
            f"missing={sorted(set(expected_artifacts67)-boundary_artifact_ids)}, "
            f"extra={sorted(boundary_artifact_ids-set(expected_artifacts67))}"
        )
    for artifact_id, expected in expected_artifacts67.items():
        artifact = by_id[artifact_id]
        for field in ("bytes", "manifest_artifact_id", "path", "sha256", "unit_id"):
            if artifact[field] != expected[field]:
                fail(f"{artifact_id}: final Units 006-007 boundary {field} mismatch")
        if set(artifact["qa_event_ids"]) != expected["qa_event_ids"]:
            fail(f"{artifact_id}: final Units 006-007 QA linkage mismatch")
        if artifact["rights_component_id"] != cumulative_rights_id:
            fail(f"{artifact_id}: must use cumulative Units 001-007 rights")

    expected_qa67 = {
        source6_qa: ("source", {"artifact:o012-u006-independent-review", "artifact:o012-units-001-007-qa-receipt"}, "unit:o012-rbt-u006"),
        math6_qa: ("math", {"artifact:o012-u006-independent-review", "artifact:o012-units-001-007-qa-receipt", "artifact:o012-units-001-007-qa-text"}, "unit:o012-rbt-u006"),
        language6_qa: ("language", {"artifact:o012-u006-independent-review"}, "unit:o012-rbt-u006"),
        source7_qa: ("source", {"artifact:o012-u007-independent-review", "artifact:o012-units-001-007-qa-receipt"}, "unit:o012-rbt-u007"),
        math7_qa: ("math", {"artifact:o012-u007-independent-review", "artifact:o012-units-001-007-qa-receipt", "artifact:o012-units-001-007-qa-text"}, "unit:o012-rbt-u007"),
        language7_qa: ("language", {"artifact:o012-u007-independent-review"}, "unit:o012-rbt-u007"),
        build7_qa: ("build", {"artifact:o012-units-001-007-html", manifest7, "artifact:o012-units-001-007-pdf", "artifact:o012-units-001-007-qa-receipt", "artifact:o012-units-001-007-qa-text"}, "unit:o012-rbt-u007"),
        accessibility7_qa: ("accessibility", {"artifact:o012-units-001-007-html", "artifact:o012-units-001-007-qa-receipt", "artifact:o012-units-001-007-visual-receipt"}, "unit:o012-rbt-u007"),
        visual7_qa: ("visual", {"artifact:o012-units-001-007-html", "artifact:o012-units-001-007-pdf", "artifact:o012-units-001-007-visual-receipt"}, "unit:o012-rbt-u007"),
    }
    boundary_qa_ids = {
        record["id"] for record in records
        if record["entity_type"] == "qa_event" and record["id"] in expected_qa67
    }
    if boundary_qa_ids != set(expected_qa67):
        fail(
            "Units 006-007 final QA-event inventory differs: "
            f"missing={sorted(set(expected_qa67)-boundary_qa_ids)}, extra={sorted(boundary_qa_ids-set(expected_qa67))}"
        )
    for qa_id, (qa_type, witnesses, unit_id) in expected_qa67.items():
        qa_event = by_id[qa_id]
        if qa_event["qa_type"] != qa_type or qa_event["result"] != "passed" or qa_event["unit_id"] != unit_id:
            fail(f"{qa_id}: final Units 006-007 QA result/type/unit mismatch")
        if set(qa_event["witness_artifact_ids"]) != witnesses:
            fail(f"{qa_id}: final Units 006-007 witness inventory mismatch")


def validate_artifact_manifests(records: list[dict[str, Any]], lane_root: Path) -> None:
    artifacts = {record["path"]: record for record in records if record["entity_type"] == "artifact"}
    for manifest_relative, specification in ARTIFACT_MANIFESTS.items():
        required_outputs = specification["outputs"]
        required = specification["required"]
        manifest_path = safe_path(lane_root, manifest_relative)
        declared = manifest_relative in artifacts
        exists = manifest_path.is_file()
        if not exists and not required and not declared:
            continue
        if not exists:
            fail(f"artifact manifest file is missing: {manifest_relative}")
        if required and not declared:
            fail(f"artifact manifest lacks its own backend artifact record: {manifest_relative}")
        staged_without_backend_record = not declared
        manifest_artifact = artifacts.get(manifest_relative)
        raw = manifest_path.read_text(encoding="utf-8-sig")
        reader = csv.DictReader(io.StringIO(raw))
        if reader.fieldnames != ["path", "bytes", "sha256"]:
            fail(f"{manifest_relative}: header must be path,bytes,sha256")
        seen: set[str] = set()
        for row in reader:
            relative = row["path"]
            if relative in seen:
                fail(f"{manifest_relative}: duplicate output {relative}")
            seen.add(relative)
            path = safe_path(lane_root, relative)
            if not path.is_file():
                fail(f"{manifest_relative}: output is missing: {relative}")
            try:
                expected_bytes = int(row["bytes"])
            except ValueError:
                fail(f"{manifest_relative}: invalid byte count for {relative}")
            if path.stat().st_size != expected_bytes or sha256_file(path) != row["sha256"]:
                fail(f"{manifest_relative}: output mismatch for {relative}")
            if relative not in artifacts:
                if staged_without_backend_record:
                    continue
                fail(f"{manifest_relative}: output lacks backend artifact record: {relative}")
            artifact = artifacts[relative]
            if artifact["bytes"] != expected_bytes or artifact["sha256"] != row["sha256"]:
                fail(f"backend artifact disagrees with {manifest_relative} for {relative}")
            if manifest_artifact is not None and artifact["manifest_artifact_id"] != manifest_artifact["id"]:
                fail(f"{relative}: backend artifact points to the wrong manifest")
        if seen != required_outputs:
            fail(
                f"{manifest_relative}: output set differs; "
                f"missing={sorted(required_outputs-seen)}, extra={sorted(seen-required_outputs)}"
            )


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
        validate_unit7_boundary(records, by_id)
        validate_artifact_manifests(records, lane_root)
        summarize(records, backend_dir)
    except (OSError, ValidationError) as exc:
        print(f"backend validation: FAIL: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
