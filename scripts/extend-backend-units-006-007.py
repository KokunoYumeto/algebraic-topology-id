#!/usr/bin/env python3
"""Deterministically extend the O012/D60 backend through Units 006-007."""

from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


LANE = Path(__file__).resolve().parents[1]
BACKEND = LANE / "backend"
LEDGER = LANE / "00_control/ADVERSE_LEDGER.csv"
TERMINOLOGY = LANE / "00_control/TERMINOLOGY.csv"
SCHEMA = "curriculum.interop"
SCHEMA_VERSION = "0.1.0"
WORKFLOW = "o012-d60-id-reader-production"
TIMESTAMP = "2026-08-22T20:00:00Z"
PROGRAM_ID = "program:o012-id"
COURSE_ID = "course:o012-d60"
RESOURCE_ID = "resource:roberts-algebraic-topology-2019"
EDITION_ID = "edition:roberts-at-2019-b947ad2"
ROBERTS_RIGHTS = "rights:roberts-cc-by-4.0"
UPSTREAM_COMMIT = "b947ad2e9f9e301bfe24590a9db653bc54fa1a53"
CUMULATIVE_RIGHTS = "rights:o012-units-001-007-composite-cc-by-4.0"
JSONL_NAMES = (
    "artifacts.jsonl", "assets.jsonl", "authority.jsonl", "concepts.jsonl",
    "corrections.jsonl", "qa.jsonl", "relations.jsonl", "rights.jsonl",
    "segments.jsonl", "terms.jsonl", "units.jsonl",
)

SOURCE_SPECS = {
    6: {
        "relative": "source/id-ID/units/unit-006-lecture-006.md",
        "bytes": 32106,
        "lines": 893,
        "sha256": "3cb182fdf183bd67e45a898228b995a44d4638e808fdfbe6ea6d6a2a2b889e33",
        "upstream_start": 1305,
        "upstream_end": 1515,
        "expected_ids": 28,
        "root_concepts": ["path-space", "compact-open-topology", "lifting-operator", "semilocally-simply-connected"],
        "title": "Topologi Aljabar — Unit 6: Ruang Lintasan, Pengangkatan Kontinu, dan Keterhubungan Sederhana Semilokal",
    },
    7: {
        "relative": "source/id-ID/units/unit-007-lecture-007.md",
        "bytes": 22107,
        "lines": 749,
        "sha256": "556cea5445e1b0a51f86f1c0ea0e80c4e00a17d365d95fa530f063cc24856569",
        "upstream_start": 1516,
        "upstream_end": 1770,
        "expected_ids": 24,
        "root_concepts": ["concatenation", "loop-space", "fundamental-group", "right-action"],
        "title": "Topologi Aljabar — Unit 7: Konkatenasi Loop, Grup Fundamental, dan Funktorialitas",
    },
}

TERM_SPECS = {
    "O012-TERM-0115": ("path-space", "o012-rbt-l06-s02"),
    "O012-TERM-0116": ("compact-open-topology", "o012-rbt-l06-def-001"),
    "O012-TERM-0117": ("sup-metric", "o012-rbt-l06-def-001"),
    "O012-TERM-0118": ("loop-space", "o012-rbt-l06-s01"),
    "O012-TERM-0119": ("evaluation-map", "o012-rbt-l06-lem-002"),
    "O012-TERM-0120": ("postcomposition", "o012-rbt-l06-lem-002"),
    "O012-TERM-0121": ("exponential-law", "o012-rbt-l06-lem-002"),
    "O012-TERM-0122": ("lifting-operator", "o012-rbt-l06-thm-001"),
    "O012-TERM-0123": ("endpoint-fixed-homotopy", "o012-rbt-l06-s03"),
    "O012-TERM-0124": ("semilocally-simply-connected", "o012-rbt-l06-def-002"),
    "O012-TERM-0125": ("mapping-space", "o012-rbt-l06-s02"),
    "O012-TERM-0126": ("hawaiian-earring", "o012-rbt-l06-exa-003"),
    "O012-TERM-0127": ("concatenation", "o012-rbt-l07-s01"),
    "O012-TERM-0128": ("associative-up-to-homotopy", "o012-rbt-l07-s02"),
    "O012-TERM-0129": ("fundamental-group", "o012-rbt-l07-def-001"),
    "O012-TERM-0130": ("right-action", "o012-rbt-l07-s03"),
    "O012-TERM-0131": ("permutation-representation", "o012-rbt-l07-s03"),
    "O012-TERM-0132": ("pointed-homotopy-class", "o012-rbt-l07-s04"),
    "O012-TERM-0133": ("pinch-map", "o012-rbt-l07-sol-004"),
}

CONCEPT_OVERRIDES = {
    "o012-rbt-l06": ["path-space", "loop-space", "lifting-operator", "semilocally-simply-connected"],
    "o012-rbt-l06-s01": ["loop-space", "fiber-transport", "covering-space"],
    "o012-rbt-l06-exa-001": ["loop-space", "fiber-transport", "covering-space"],
    "o012-rbt-l06-s02": ["path-space", "mapping-space", "compact-open-topology"],
    "o012-rbt-l06-lem-001": ["compact-open-topology", "path-space"],
    "o012-rbt-l06-def-001": ["path-space", "compact-open-topology", "sup-metric"],
    "o012-rbt-l06-lem-002": ["evaluation-map", "postcomposition", "exponential-law"],
    "o012-rbt-l06-s03": ["lifting-operator", "compact-open-topology", "endpoint-fixed-homotopy"],
    "o012-rbt-l06-thm-001": ["lifting-operator", "covering-space"],
    "o012-rbt-l06-proof-001": ["lifting-operator", "covering-space", "compact-open-topology"],
    "o012-rbt-l06-rem-001": ["fiber-transport", "endpoint-fixed-homotopy"],
    "o012-rbt-l06-s04": ["semilocally-simply-connected", "mapping-space", "path-space"],
    "o012-rbt-l06-def-002": ["semilocally-simply-connected"],
    "o012-rbt-l06-exa-002": ["semilocally-simply-connected"],
    "o012-rbt-l06-exa-003": ["semilocally-simply-connected", "hawaiian-earring"],
    "o012-rbt-l06-thm-002": ["semilocally-simply-connected", "mapping-space", "path-space", "loop-space"],
    "o012-rbt-l06-check-001": ["semilocally-simply-connected", "mapping-space", "path-space", "loop-space"],
    "o012-rbt-l07": ["concatenation", "loop-space", "fundamental-group", "right-action"],
    "o012-rbt-l07-s01": ["concatenation", "fiber-transport", "loop-space"],
    "o012-rbt-l07-lem-001": ["concatenation", "fiber-transport"],
    "o012-rbt-l07-exa-001": ["concatenation", "fiber-transport", "covering-space"],
    "o012-rbt-l07-s02": ["concatenation", "loop-space", "associative-up-to-homotopy"],
    "o012-rbt-l07-prop-001": ["loop-space", "fundamental-group", "concatenation"],
    "o012-rbt-l07-proof-001": ["loop-space", "concatenation", "associative-up-to-homotopy"],
    "o012-rbt-l07-def-001": ["fundamental-group", "loop-space"],
    "o012-rbt-l07-s03": ["fundamental-group", "right-action", "permutation-representation", "covering-space"],
    "o012-rbt-l07-exa-002": ["fundamental-group", "right-action", "covering-space"],
    "o012-rbt-l07-exa-003": ["fundamental-group", "right-action", "covering-space"],
    "o012-rbt-l07-s04": ["loop-space", "fundamental-group", "pointed-homotopy-class"],
    "o012-rbt-l07-prop-002": ["loop-space", "functor"],
    "o012-rbt-l07-cor-001": ["fundamental-group", "functor"],
    "o012-rbt-l07-sol-004": ["fundamental-group", "pointed-homotopy-class", "pinch-map"],
}

CORRECTION_TARGETS = {
    "O012-ADV-0071": ["o012-rbt-l06-exa-001"],
    "O012-ADV-0072": ["o012-rbt-l06-s01"],
    "O012-ADV-0073": ["o012-rbt-l06-s02", "o012-rbt-l06-mcheck-002", "o012-rbt-l06-sol-002"],
    "O012-ADV-0074": ["o012-rbt-l06-s03"],
    "O012-ADV-0075": ["o012-rbt-l06-proof-001"],
    "O012-ADV-0076": ["o012-rbt-l06-s03"],
    "O012-ADV-0077": ["o012-rbt-l06-def-002"],
    "O012-ADV-0078": ["o012-rbt-l06-exa-002"],
    "O012-ADV-0079": ["o012-rbt-l06-exa-003"],
    "O012-ADV-0080": ["o012-rbt-l06-thm-002", "o012-rbt-l06-proof-002", "o012-rbt-l06-check-001"],
    "O012-ADV-0081": ["o012-rbt-l06"],
    "O012-ADV-0082": ["o012-rbt-l06"],
    "O012-ADV-0083": ["o012-rbt-l07-s01"],
    "O012-ADV-0084": ["o012-rbt-l07-lem-001"],
    "O012-ADV-0085": ["o012-rbt-l07-s02"],
    "O012-ADV-0086": ["o012-rbt-l07-s02"],
    "O012-ADV-0087": ["o012-rbt-l07-s02"],
    "O012-ADV-0088": ["o012-rbt-l07-s02"],
    "O012-ADV-0089": ["o012-rbt-l07-s02", "o012-rbt-l07-mcheck-002", "o012-rbt-l07-sol-002"],
    "O012-ADV-0090": ["o012-rbt-l07-s03"],
    "O012-ADV-0091": ["o012-rbt-l07-exa-002"],
    "O012-ADV-0092": ["o012-rbt-l07-s04", "o012-rbt-l07-mcheck-004", "o012-rbt-l07-sol-004"],
    "O012-ADV-0093": ["o012-rbt-l07-s04", "o012-rbt-l07-sol-004"],
    "O012-ADV-0094": ["o012-rbt-l07-exa-003"],
}

ARTIFACT_META = {
    "artifact:o012-u006-independent-review": ("qa/UNIT_006_INDEPENDENT_REVIEW.md", 1783, "5dd3868192a85e3e60562f42ec7d7b792e0e58811719ecc97207ed2bdc5de4bf", "text/markdown; charset=utf-8", "unit:o012-rbt-u006", "mathematically_reviewed"),
    "artifact:o012-u007-independent-review": ("qa/UNIT_007_INDEPENDENT_REVIEW.md", 1761, "87c5129cd7d367893860b150c72948de1d196d7cbefe04d53f7a4efecf921f87", "text/markdown; charset=utf-8", "unit:o012-rbt-u007", "mathematically_reviewed"),
    "artifact:o012-units-001-007-html": ("output/html/units-001-007/index.html", 899803, "55135048eafe0f097c45936add885e008392eefdf475270fea37adf6a2a7b7bb", "text/html; charset=utf-8", "unit:o012-rbt-u007", "built"),
    "artifact:o012-units-001-007-manifest": ("output/ARTIFACT_MANIFEST_UNITS_001_007.csv", 247, "7b279f0413892f0ddedce636b3a272884bb7bfa01410bf33a6ce34c0c34db2f9", "text/csv; charset=utf-8", "unit:o012-rbt-u007", "built"),
    "artifact:o012-units-001-007-pdf": ("output/pdf/topologi-aljabar-unit-001-007-id.pdf", 702470, "3764b75ecfb9200e25a165db1f0f97a680384378e2a9a22e129aab57dd860d93", "application/pdf", "unit:o012-rbt-u007", "built"),
    "artifact:o012-units-001-007-qa-receipt": ("qa/UNITS_001_007_QA.json", 7384, "2982a9465428eff97e6047bffdadba422b2dc0406e34750f632bfe148ed67617", "application/json", "unit:o012-rbt-u007", "built"),
    "artifact:o012-units-001-007-qa-text": ("qa/units-001-007-extracted.txt", 190424, "f6839e7eb7f25c8518ec3fc2e2372b82b1f1387b48402899ff8bc40ce153c8dc", "text/plain; charset=utf-8", "unit:o012-rbt-u007", "built"),
    "artifact:o012-units-001-007-visual-receipt": ("qa/UNITS_001_007_VISUAL_QA.md", 3259, "63a4b4545213a7aec1c556a3852b818ba2f207b10cac7e80c62330709604176f", "text/markdown; charset=utf-8", "unit:o012-rbt-u007", "visually_checked"),
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def common(entity_type: str, record_id: str) -> dict[str, Any]:
    return {
        "entity_type": entity_type, "id": record_id, "schema": SCHEMA,
        "schema_version": SCHEMA_VERSION, "status": "active", "supersedes": None,
        "timestamp": TIMESTAMP, "workflow": WORKFLOW,
    }


def load_jsonl(name: str) -> tuple[dict[str, dict[str, Any]], dict[str, str]]:
    records: dict[str, dict[str, Any]] = {}
    lines: dict[str, str] = {}
    for line in (BACKEND / name).read_text(encoding="utf-8").splitlines():
        record = json.loads(line)
        record_id = record["id"]
        if record_id in records:
            raise SystemExit(f"duplicate existing backend id: {record_id}")
        records[record_id] = record
        lines[record_id] = line
    return records, lines


def canonical_record(record: dict[str, Any]) -> str:
    return json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def canonical_jsonl(records: dict[str, dict[str, Any]]) -> bytes:
    return "".join(canonical_record(records[record_id]) + "\n" for record_id in sorted(records)).encode("utf-8")


record_sets: dict[str, dict[str, dict[str, Any]]] = {}
prior_lines: dict[str, dict[str, str]] = {}
for filename in JSONL_NAMES:
    record_sets[filename], prior_lines[filename] = load_jsonl(filename)

artifacts = record_sets["artifacts.jsonl"]
assets = record_sets["assets.jsonl"]
authority = record_sets["authority.jsonl"]
concepts = record_sets["concepts.jsonl"]
corrections = record_sets["corrections.jsonl"]
qa_events = record_sets["qa.jsonl"]
relations = record_sets["relations.jsonl"]
rights = record_sets["rights.jsonl"]
segments = record_sets["segments.jsonl"]
terms = record_sets["terms.jsonl"]
units = record_sets["units.jsonl"]

allowed_modified_existing = {PROGRAM_ID, COURSE_ID, EDITION_ID, ROBERTS_RIGHTS}
owned_new_ids: set[str] = set()
unit_context: dict[int, dict[str, Any]] = {}


def concept_ids(slugs: list[str]) -> list[str]:
    return [f"concept:{slug}" for slug in slugs]


def infer_kind(local_id: str) -> str:
    if local_id.endswith("-notice"):
        return "notice"
    if re.fullmatch(r"o012-rbt-l\d{2}", local_id):
        return "lecture"
    if re.search(r"-s\d{2}$", local_id):
        return "section"
    if local_id.endswith("-mastery"):
        return "mastery_section"
    if "-mcheck-" in local_id:
        return "exercise"
    if "-sol-" in local_id:
        return "solution"
    if "-check-" in local_id:
        return "proof_check"
    tokens = {
        "-exa-": "example", "-lem-": "lemma", "-def-": "definition",
        "-thm-": "theorem", "-proof-": "proof", "-rem-": "remark",
        "-prop-": "proposition", "-cor-": "corollary",
    }
    for token, kind in tokens.items():
        if token in local_id:
            return kind
    raise SystemExit(f"cannot infer unit kind: {local_id}")


def is_original(local_id: str) -> bool:
    return any(token in local_id for token in ("-notice", "-mastery", "-mcheck-", "-sol-", "-check-"))


for lecture, spec in SOURCE_SPECS.items():
    source_path = LANE / spec["relative"]
    raw = source_path.read_bytes()
    if len(raw) != spec["bytes"] or sha256(raw) != spec["sha256"]:
        raise SystemExit(f"Unit {lecture:03d} source identity mismatch")
    raw_lines = raw.splitlines(keepends=True)
    if len(raw_lines) != spec["lines"]:
        raise SystemExit(f"Unit {lecture:03d} source line-count mismatch")
    text_lines = [line.decode("utf-8").rstrip("\r\n") for line in raw_lines]
    id_re = re.compile(rf"#(o012-rbt-l{lecture:02d}(?:-[a-z0-9]+)*)")
    anchor_start: dict[str, int] = {}
    for number, text in enumerate(text_lines, start=1):
        found = id_re.findall(text)
        if len(found) > 1:
            raise SystemExit(f"multiple stable IDs on Unit {lecture} line {number}")
        if found:
            if found[0] in anchor_start:
                raise SystemExit(f"duplicate stable ID: {found[0]}")
            anchor_start[found[0]] = number
    if len(anchor_start) != spec["expected_ids"]:
        raise SystemExit(f"Unit {lecture} stable-ID count mismatch: {len(anchor_start)}")

    heading_re = re.compile(r"^(#{1,6})\s+(.+?)\s+\{")

    def trim_blank_end(end: int, start: int) -> int:
        while end > start and not text_lines[end - 1].strip():
            end -= 1
        return end

    def derive_span(local_id: str) -> tuple[int, int]:
        start = anchor_start[local_id]
        opening = text_lines[start - 1]
        heading = heading_re.match(opening)
        if heading:
            level = len(heading.group(1))
            end = len(text_lines)
            for candidate in range(start + 1, len(text_lines) + 1):
                next_heading = heading_re.match(text_lines[candidate - 1])
                if next_heading and len(next_heading.group(1)) <= level:
                    end = candidate - 1
                    break
            return start, trim_blank_end(end, start)
        if opening.startswith(":::"):
            for candidate in range(start + 1, len(text_lines) + 1):
                if text_lines[candidate - 1].strip() == ":::":
                    return start, candidate
        raise SystemExit(f"cannot derive span for {local_id}")

    spans = {local_id: derive_span(local_id) for local_id in anchor_start}

    def locator(start: int, end: int) -> dict[str, Any]:
        return {
            "content_sha256": sha256(b"".join(raw_lines[start - 1 : end])),
            "file_sha256": spec["sha256"], "line_end": end, "line_start": start,
            "path": spec["relative"],
        }

    root_id = f"unit:o012-rbt-u{lecture:03d}"
    companion_rights = f"rights:o012-u{lecture:03d}-companion-cc-by-4.0"
    composite_rights = f"rights:o012-u{lecture:03d}-composite-cc-by-4.0"
    root = common("unit", root_id)
    root.update({
        "concept_ids": concept_ids(spec["root_concepts"]), "course_id": COURSE_ID,
        "display_title": spec["title"], "edition_id": EDITION_ID, "locale": "id-ID",
        "order": lecture, "parent_id": COURSE_ID, "path": [root_id], "program_id": PROGRAM_ID,
        "provenance_relation": "composite_translated_and_original", "resource_id": RESOURCE_ID,
        "rights_component_id": composite_rights, "source_local_id": None,
        "target_locator": locator(1, spec["lines"]), "translation_state": "structurally_verified",
        "unit_kind": "reader_unit",
    })
    units[root_id] = root
    owned_new_ids.add(root_id)

    ordered = sorted(anchor_start, key=anchor_start.get)
    lecture_local = f"o012-rbt-l{lecture:02d}"
    mastery_local = f"o012-rbt-l{lecture:02d}-mastery"
    current_section: str | None = None
    current_mode = "lecture"
    sibling_next: defaultdict[str, int] = defaultdict(lambda: 1)
    metadata: dict[str, dict[str, Any]] = {}

    for local_id in ordered:
        kind = infer_kind(local_id)
        if kind in {"notice", "lecture", "mastery_section"}:
            parent = root_id
            fixed_order = {"notice": 1, "lecture": 2, "mastery_section": 3}[kind]
            order = fixed_order
            if kind == "mastery_section":
                current_mode = "mastery"
        elif kind == "section" and current_mode == "lecture":
            parent = f"unit:{lecture_local}"
            order = sibling_next[parent]
            sibling_next[parent] += 1
            current_section = local_id
        elif current_mode == "mastery":
            parent = f"unit:{mastery_local}"
            order = sibling_next[parent]
            sibling_next[parent] += 1
        else:
            if current_section is None:
                raise SystemExit(f"Unit {lecture} child lacks section: {local_id}")
            parent = f"unit:{current_section}"
            order = sibling_next[parent]
            sibling_next[parent] += 1

        line = text_lines[anchor_start[local_id] - 1]
        heading = heading_re.match(line)
        if heading:
            display = re.sub(r"\s+\{.*$", "", heading.group(2)).strip()
        else:
            display = local_id
            for candidate in text_lines[anchor_start[local_id] : spans[local_id][1]]:
                match = re.match(r"^\*\*(.+?)\*\*", candidate)
                if match:
                    display = match.group(1).strip()
                    break
        inherited = []
        if parent.startswith("unit:o012-rbt-l"):
            parent_local = parent.removeprefix("unit:")
            inherited = metadata.get(parent_local, {}).get("concept_slugs", [])
        slugs = CONCEPT_OVERRIDES.get(local_id, list(inherited))
        metadata[local_id] = {"display": display, "kind": kind, "parent": parent, "order": order, "concept_slugs": slugs}

    def unit_path(local_id: str) -> list[str]:
        unit_id = f"unit:{local_id}"
        parent = metadata[local_id]["parent"]
        if parent == root_id:
            return [root_id, unit_id]
        return unit_path(parent.removeprefix("unit:")) + [unit_id]

    upstream_locator = {
        "commit_sha": UPSTREAM_COMMIT, "line_end": spec["upstream_end"],
        "line_start": spec["upstream_start"], "path": "Notes.tex",
        "precision": "unit_range_only",
    }
    for local_id in ordered:
        item = metadata[local_id]
        start, end = spans[local_id]
        original = is_original(local_id)
        provenance = "edition_original" if original else "translated_adapted_from_upstream"
        component_rights = companion_rights if original else ROBERTS_RIGHTS
        extra: dict[str, Any] = {}
        if local_id == "o012-rbt-l07-exa-003":
            extra["source_aliases"] = ["eg:piS^1_infinite"]
        unit_id = f"unit:{local_id}"
        unit = common("unit", unit_id)
        unit.update({
            "concept_ids": concept_ids(item["concept_slugs"]), "course_id": COURSE_ID,
            "display_title": item["display"], "edition_id": EDITION_ID, "locale": "id-ID",
            "order": item["order"], "parent_id": item["parent"], "path": unit_path(local_id),
            "program_id": PROGRAM_ID, "provenance_relation": provenance,
            "resource_id": RESOURCE_ID, "rights_component_id": component_rights,
            "source_local_id": local_id, "target_locator": locator(start, end),
            "translation_state": "structurally_verified", "unit_kind": item["kind"], **extra,
        })
        units[unit_id] = unit
        owned_new_ids.add(unit_id)
        segment_id = f"segment:{local_id}"
        segment = common("segment", segment_id)
        segment.update({
            "concept_ids": concept_ids(item["concept_slugs"]), "edition_id": EDITION_ID,
            "locale": "id-ID", "order": item["order"], "provenance_relation": provenance,
            "resource_id": RESOURCE_ID, "rights_component_id": component_rights,
            "segment_kind": item["kind"], "source_local_id": local_id,
            "source_locator": ({"kind": "edition_original", "path": spec["relative"], "precision": "exact_target_span"} if original else dict(upstream_locator)),
            "target_locator": locator(start, end), "translation_state": "structurally_verified",
            "unit_id": unit_id, **extra,
        })
        segments[segment_id] = segment
        owned_new_ids.add(segment_id)

    companion = common("rights", companion_rights)
    companion.update({
        "attribution": f"Original Indonesian mastery companion and edition notice for O012/D60 Unit {lecture:03d}.",
        "change_notice": "Newly authored material; not represented as source-author text.",
        "component_scope": [f"unit:{lecture_local}-notice", f"unit:{lecture_local}-mastery"],
        "license_expression": "CC-BY-4.0", "license_url": "https://creativecommons.org/licenses/by/4.0/",
        "non_endorsement": "No endorsement by David Michael Roberts or affiliated institutions is implied.",
        "third_party_status": "No external media component.",
    })
    rights[companion_rights] = companion
    owned_new_ids.add(companion_rights)
    composite = common("rights", composite_rights)
    composite.update({
        "attribution": f"Composite Unit {lecture:03d} reader: Roberts source adaptation plus independently authored Indonesian mastery companion; component provenance remains separated.",
        "change_notice": "See component rights records for translated/adapted and original portions.",
        "component_scope": [root_id], "license_expression": "CC-BY-4.0",
        "license_url": "https://creativecommons.org/licenses/by/4.0/",
        "non_endorsement": "Independent edition; no source-author endorsement.",
        "third_party_status": "Component-scoped rights records control.",
    })
    rights[composite_rights] = composite
    owned_new_ids.add(composite_rights)

    asset_id = f"asset:o012-u{lecture:03d}-source-markdown"
    asset = common("asset", asset_id)
    asset.update({
        "bytes": spec["bytes"], "edition_id": EDITION_ID,
        "media_type": "text/markdown; charset=utf-8", "path": spec["relative"],
        "resource_id": RESOURCE_ID, "rights_component_id": composite_rights,
        "role": "canonical_reader_source", "sha256": spec["sha256"],
    })
    assets[asset_id] = asset
    owned_new_ids.add(asset_id)

    unit_context[lecture] = {
        "root_id": root_id, "companion_rights": companion_rights, "composite_rights": composite_rights,
        "anchor_start": anchor_start, "spans": spans, "text_lines": text_lines,
        "metadata": metadata, "raw_lines": raw_lines, "spec": dict(spec),
    }


# Locale-neutral concepts and Indonesian terms are bound to the exact control subset.
with TERMINOLOGY.open("r", encoding="utf-8", newline="") as stream:
    terminology_rows = {row["term_id"]: row for row in csv.DictReader(stream) if row["term_id"] in TERM_SPECS}
if set(terminology_rows) != set(TERM_SPECS):
    raise SystemExit(f"Unit 6/7 terminology subset mismatch: {sorted(set(TERM_SPECS)-set(terminology_rows))}")
for term_control_id, (slug, evidence_local_id) in TERM_SPECS.items():
    row = terminology_rows[term_control_id]
    concept_id = f"concept:{slug}"
    concept = common("concept", concept_id)
    concept.update({"canonical_label": row["source_term"], "domain": row["scope"], "locale_neutral": True})
    concepts[concept_id] = concept
    owned_new_ids.add(concept_id)
    lecture = int(re.search(r"l(\d{2})", evidence_local_id).group(1))
    term_id = f"term:{slug}:id-ID"
    term = common("term", term_id)
    term.update({
        "concept_id": concept_id, "evidence_segment_id": f"segment:{evidence_local_id}",
        "locale": "id-ID", "preferred": row["id_ID"], "register": "textbook",
        "rejected_forms": [], "rights_component_id": ROBERTS_RIGHTS,
        "scope_unit_id": unit_context[lecture]["root_id"], "source_term": row["source_term"],
        "terminology_control_id": term_control_id, "terminology_status": row["status"],
        "usage_note": row["note"], "variants": [],
    })
    terms[term_id] = term
    owned_new_ids.add(term_id)


def add_relation(record_id: str, from_id: str, relation_type: str, to_id: str, note: str) -> None:
    relation = common("relation", record_id)
    relation.update({"from_id": from_id, "note": note, "relation_type": relation_type, "to_id": to_id})
    relations[record_id] = relation
    owned_new_ids.add(record_id)


add_relation("relation:adapts:o012-rbt-u006:roberts-edition", "unit:o012-rbt-u006", "adapts", EDITION_ID, "Unit 006 adapts Notes.tex lines 1305-1515 and adds an original solved mastery companion.")
add_relation("relation:adapts:o012-rbt-u007:roberts-edition", "unit:o012-rbt-u007", "adapts", EDITION_ID, "Unit 007 adapts Notes.tex lines 1516-1770 and adds an original solved mastery companion.")
add_relation("relation:precedes:u005:u006", "unit:o012-rbt-u005", "precedes", "unit:o012-rbt-u006", "Cumulative reader order.")
add_relation("relation:precedes:u006:u007", "unit:o012-rbt-u006", "precedes", "unit:o012-rbt-u007", "Cumulative reader order.")
for lecture in (6, 7):
    add_relation(f"relation:precedes:l{lecture:02d}:mastery", f"unit:o012-rbt-l{lecture:02d}", "precedes", f"unit:o012-rbt-l{lecture:02d}-mastery", "The translated lecture precedes its original solved mastery companion.")
    for number in range(1, 5):
        add_relation(
            f"relation:solves:l{lecture:02d}-sol-{number:03d}:l{lecture:02d}-mcheck-{number:03d}",
            f"unit:o012-rbt-l{lecture:02d}-sol-{number:03d}", "solves",
            f"unit:o012-rbt-l{lecture:02d}-mcheck-{number:03d}",
            f"Complete solution to Mastery Check {lecture}.{number}.",
        )
add_relation("relation:proves:l06-proof-001:l06-thm-001", "unit:o012-rbt-l06-proof-001", "proves", "unit:o012-rbt-l06-thm-001", "Proof of continuity of the covering-space lifting operator.")
add_relation("relation:proves:l06-check-001:l06-thm-002", "unit:o012-rbt-l06-check-001", "proves", "unit:o012-rbt-l06-thm-002", "Edition-original self-study proof of the n=1 Wada-Roberts mapping-space result.")
add_relation("relation:proves:l07-proof-001:l07-prop-001", "unit:o012-rbt-l07-proof-001", "proves", "unit:o012-rbt-l07-prop-001", "Proof that path components of the loop space form a group.")
add_relation("relation:xref:l07-exa-003:source-alias", "unit:o012-rbt-l07-exa-003", "xref", EDITION_ID, "Preserves the upstream source label eg:piS^1_infinite for later cross-reference resolution.")


# One correction record for each exact Unit 6/7 adverse-ledger event.
with LEDGER.open("r", encoding="utf-8", newline="") as stream:
    all_ledger_rows = list(csv.DictReader(stream))
if any(None in row or len(row) != 7 for row in all_ledger_rows):
    raise SystemExit("adverse ledger contains a non-canonical CSV row")
ledger_rows = {row["event_id"]: row for row in all_ledger_rows if row["event_id"] in CORRECTION_TARGETS}
if set(ledger_rows) != set(CORRECTION_TARGETS):
    raise SystemExit(f"Unit 6/7 adverse subset mismatch: {sorted(set(CORRECTION_TARGETS)-set(ledger_rows))}")
for event_id, affected_local_ids in CORRECTION_TARGETS.items():
    row = ledger_rows[event_id]
    lecture = 6 if int(event_id[-4:]) <= 82 else 7
    context = unit_context[lecture]
    target_locations = [f"{context['spans'][local_id][0]}-{context['spans'][local_id][1]}" for local_id in affected_local_ids]
    status_to_type = {
        "accessibility_reflow": "structural_adaptation",
        "identifier_preservation": "identifier_preservation",
        "clarified_in_translation": "clarification",
        "corrected_in_translation": "mathematical_correction",
    }
    correction_type = status_to_type[row["status"]]
    record_id = f"correction:o012-u{lecture:03d}-adv-{event_id[-4:]}"
    correction = common("correction", record_id)
    correction.update({
        "adverse_ledger_id": event_id,
        "affected_unit_ids": [f"unit:{local_id}" for local_id in affected_local_ids],
        "correction_type": correction_type, "edition_id": EDITION_ID,
        "evidence": f"{row['source_location']}; target spans {', '.join(target_locations)}.",
        "evidence_segment_id": f"segment:o012-rbt-l{lecture:02d}-notice",
        "severity": row["severity"], "rationale": row["rationale"], "resource_id": RESOURCE_ID,
        "source_defect": row["observed"], "target_change": row["action"],
        "unit_id": context["root_id"], "upstream_report_disposition": "not_contacted",
    })
    corrections[record_id] = correction
    owned_new_ids.add(record_id)


# Component and cumulative rights updates.
cumulative = common("rights", CUMULATIVE_RIGHTS)
cumulative.update({
    "attribution": "Cumulative Units 001-007 reader: David Michael Roberts source adaptations plus independently authored Indonesian mastery companions; component provenance remains separated.",
    "change_notice": "Cumulative staged boundary only; Unit 001 through Unit 007 component rights records remain controlling.",
    "component_scope": [f"unit:o012-rbt-u{number:03d}" for number in range(1, 8)],
    "license_expression": "CC-BY-4.0", "license_url": "https://creativecommons.org/licenses/by/4.0/",
    "non_endorsement": "Independent edition; no source-author endorsement.",
    "third_party_status": "Component-scoped rights records control.",
})
rights[CUMULATIVE_RIGHTS] = cumulative
owned_new_ids.add(CUMULATIVE_RIGHTS)
roberts = rights[ROBERTS_RIGHTS]
roberts["component_scope"] = [f"unit:o012-rbt-l{number:02d}" for number in range(1, 8)]
roberts["third_party_status"] = "No distinct third-party component is asserted within Units 001-007; the frozen archive remains authoritative for file-level review."
roberts["timestamp"] = TIMESTAMP
for authority_id in (PROGRAM_ID, COURSE_ID):
    authority[authority_id]["rights_component_id"] = CUMULATIVE_RIGHTS
    authority[authority_id]["timestamp"] = TIMESTAMP
edition = authority[EDITION_ID]
edition["local_derivative_unit_ids"] = [f"unit:o012-rbt-u{number:03d}" for number in range(1, 8)]
edition["source_line_end"] = 1770
edition["timestamp"] = TIMESTAMP


# Final artifact and QA graph.
QA_IDS = {
    "u6_source": "qa:o012-u006-source-integrity", "u6_math": "qa:o012-u006-math-review",
    "u6_language": "qa:o012-u006-language-review", "u7_source": "qa:o012-u007-source-integrity",
    "u7_math": "qa:o012-u007-math-review", "u7_language": "qa:o012-u007-language-review",
    "build": "qa:o012-units-001-007-build", "accessibility": "qa:o012-units-001-007-accessibility",
    "visual": "qa:o012-units-001-007-visual",
}
artifact_qa = {
    "artifact:o012-u006-independent-review": [QA_IDS["u6_source"], QA_IDS["u6_math"], QA_IDS["u6_language"]],
    "artifact:o012-u007-independent-review": [QA_IDS["u7_source"], QA_IDS["u7_math"], QA_IDS["u7_language"]],
    "artifact:o012-units-001-007-html": [QA_IDS["build"], QA_IDS["accessibility"], QA_IDS["visual"]],
    "artifact:o012-units-001-007-manifest": [QA_IDS["build"]],
    "artifact:o012-units-001-007-pdf": [QA_IDS["build"], QA_IDS["accessibility"], QA_IDS["visual"]],
    "artifact:o012-units-001-007-qa-receipt": list(QA_IDS.values()),
    "artifact:o012-units-001-007-qa-text": [QA_IDS["build"], QA_IDS["u6_math"], QA_IDS["u7_math"]],
    "artifact:o012-units-001-007-visual-receipt": [QA_IDS["accessibility"], QA_IDS["visual"]],
}
manifest_id = "artifact:o012-units-001-007-manifest"
for artifact_id, (relative, expected_bytes, expected_sha, media_type, unit_id, state) in ARTIFACT_META.items():
    path = LANE / relative
    raw = path.read_bytes()
    if len(raw) != expected_bytes or sha256(raw) != expected_sha:
        raise SystemExit(f"final artifact identity mismatch: {relative}")
    toolchain = {
        "artifact:o012-u006-independent-review": "Independent exact-span mathematical, structural, and Indonesian-language review.",
        "artifact:o012-u007-independent-review": "Independent exact-span mathematical, structural, identifier-alias, and Indonesian-language review.",
        "artifact:o012-units-001-007-html": "Pandoc 3.9.0.2 standalone HTML5 with embedded CSS and native MathML; two builds byte-identical.",
        "artifact:o012-units-001-007-manifest": "Deterministic cumulative Units 001-007 artifact manifest.",
        "artifact:o012-units-001-007-pdf": "Pandoc 3.9.0.2 with pdflatex; two 21 mm fixed-epoch builds byte-identical.",
        "artifact:o012-units-001-007-qa-receipt": "Fail-closed source, correction, rights, structure, HTML, PDF, link, language, and accessibility QA.",
        "artifact:o012-units-001-007-qa-text": "Poppler pdftotext with layout preservation and UTF-8 output.",
        "artifact:o012-units-001-007-visual-receipt": "Poppler all-page rendering plus Codex in-app Chromium desktop/mobile review.",
    }[artifact_id]
    artifact = common("artifact", artifact_id)
    artifact.update({
        "bytes": expected_bytes, "locale": "id-ID",
        "manifest_artifact_id": (manifest_id if artifact_id in {"artifact:o012-units-001-007-html", "artifact:o012-units-001-007-pdf"} else None),
        "media_type": media_type, "path": relative, "qa_event_ids": artifact_qa[artifact_id],
        "rights_component_id": CUMULATIVE_RIGHTS, "sha256": expected_sha,
        "toolchain": toolchain, "translation_state": state, "unit_id": unit_id,
    })
    artifacts[artifact_id] = artifact
    owned_new_ids.add(artifact_id)

qa_meta = {
    QA_IDS["u6_source"]: ("source", "Unit 006 source identity, Notes.tex lines 1305-1515, all 28 stable IDs, semantic environments, and the one-to-one O012-ADV-0071 through O012-ADV-0082 inventory passed.", ["artifact:o012-u006-independent-review", "artifact:o012-units-001-007-qa-receipt"]),
    QA_IDS["u6_math"]: ("math", "Independent Unit 006 review passed with P1, P2, and P3 all zero; four solved mastery checks and the edition-original n=1 mapping-space proof close the declared self-study gaps.", ["artifact:o012-u006-independent-review", "artifact:o012-units-001-007-qa-receipt", "artifact:o012-units-001-007-qa-text"]),
    QA_IDS["u6_language"]: ("language", "Independent Unit 006 Indonesian-language and terminology review passed with no active English prose outside protected names, notation, URLs, and markup.", ["artifact:o012-u006-independent-review"]),
    QA_IDS["u7_source"]: ("source", "Unit 007 source identity, Notes.tex lines 1516-1770, all 24 stable IDs, semantic environments, and the one-to-one O012-ADV-0083 through O012-ADV-0094 inventory passed; source alias eg:piS^1_infinite is preserved.", ["artifact:o012-u007-independent-review", "artifact:o012-units-001-007-qa-receipt"]),
    QA_IDS["u7_math"]: ("math", "Independent Unit 007 review passed with P1, P2, and P3 all zero; four solved mastery checks close transport, concatenation continuity, group-action, functoriality, and pointed-circle-model gaps.", ["artifact:o012-u007-independent-review", "artifact:o012-units-001-007-qa-receipt", "artifact:o012-units-001-007-qa-text"]),
    QA_IDS["u7_language"]: ("language", "Independent Unit 007 Indonesian-language, terminology, and accessible-diagram reflow review passed.", ["artifact:o012-u007-independent-review"]),
    QA_IDS["build"]: ("build", "Two fixed-epoch HTML builds and two fixed-epoch PDF builds were byte-identical; manifest, PDF text witness, and every prior source/artifact/QA witness are hash-consistent.", ["artifact:o012-units-001-007-html", manifest_id, "artifact:o012-units-001-007-pdf", "artifact:o012-units-001-007-qa-receipt", "artifact:o012-units-001-007-qa-text"]),
    QA_IDS["accessibility"]: ("accessibility", "Semantic HTML passed with lang=id-ID, 2,344 native MathML nodes, 315 unique IDs, all 89 fragments resolving, no scripts/runtime assets, exact desktop centering, mobile reflow, and all 32 wide formulae locally scrollable. PDF is secondary and untagged.", ["artifact:o012-units-001-007-html", "artifact:o012-units-001-007-qa-receipt", "artifact:o012-units-001-007-visual-receipt"]),
    QA_IDS["visual"]: ("visual", "All 66 PDF pages and the HTML title, contents, and Unit 7 surfaces at 1280x720 and 390x844 were inspected with no clipping, overlap, orphan page, or document-level overflow.", ["artifact:o012-units-001-007-html", "artifact:o012-units-001-007-pdf", "artifact:o012-units-001-007-visual-receipt"]),
}
for qa_id, (qa_type, note, witnesses) in qa_meta.items():
    unit_id = "unit:o012-rbt-u006" if "-u006-" in qa_id else "unit:o012-rbt-u007"
    event = common("qa_event", qa_id)
    event.update({"note": note, "qa_type": qa_type, "result": "passed", "unit_id": unit_id, "witness_artifact_ids": witnesses})
    qa_events[qa_id] = event
    owned_new_ids.add(qa_id)


# Global referential, hierarchy, source-span, mastery, correction, artifact, and
# canonical-byte validation before any backend file is replaced.
all_records: dict[str, dict[str, Any]] = {}
for filename, records in record_sets.items():
    for record_id, record in records.items():
        if record_id in all_records:
            raise SystemExit(f"duplicate global backend id after extension: {record_id}")
        if record.get("id") != record_id or record.get("schema") != SCHEMA or record.get("schema_version") != SCHEMA_VERSION:
            raise SystemExit(f"backend identity/schema mismatch in {filename}: {record_id}")
        all_records[record_id] = record

scalar_references = {
    "concept_id", "course_id", "edition_id", "evidence_segment_id", "from_id",
    "local_derivative_unit_id", "manifest_artifact_id", "parent_id", "program_id",
    "resource_id", "rights_component_id", "scope_unit_id", "to_id", "unit_id",
}
list_references = {
    "affected_unit_ids", "component_scope", "concept_ids", "local_derivative_unit_ids",
    "qa_event_ids", "witness_artifact_ids",
}
for record_id, record in all_records.items():
    for field in scalar_references:
        value = record.get(field)
        if value is not None and value not in all_records:
            raise SystemExit(f"unknown backend reference {record_id}.{field}={value}")
    for field in list_references:
        if field in record and (not isinstance(record[field], list) or any(value not in all_records for value in record[field])):
            raise SystemExit(f"unknown/list backend reference {record_id}.{field}")

def context_locator(context: dict[str, Any], start: int, end: int) -> dict[str, Any]:
    spec = context["spec"]
    return {
        "content_sha256": sha256(b"".join(context["raw_lines"][start - 1 : end])),
        "file_sha256": spec["sha256"], "line_end": end, "line_start": start,
        "path": spec["relative"],
    }


for lecture, context in unit_context.items():
    spec = SOURCE_SPECS[lecture]
    for local_id in context["anchor_start"]:
        unit = units[f"unit:{local_id}"]
        segment = segments[f"segment:{local_id}"]
        if unit["target_locator"] != segment["target_locator"]:
            raise SystemExit(f"Unit {lecture} unit/segment locator mismatch: {local_id}")
        start, end = context["spans"][local_id]
        if unit["target_locator"] != context_locator(context, start, end) or local_id not in context["text_lines"][start - 1]:
            raise SystemExit(f"Unit {lecture} target-span mismatch: {local_id}")
        if unit["path"][-1] != unit["id"] or any(node not in units for node in unit["path"]):
            raise SystemExit(f"Unit {lecture} hierarchy mismatch: {local_id}")
    root = units[context["root_id"]]
    if root["target_locator"] != context_locator(context, 1, spec["lines"]):
        raise SystemExit(f"Unit {lecture} root locator mismatch")
    exercises = {f"unit:o012-rbt-l{lecture:02d}-mcheck-{number:03d}" for number in range(1, 5)}
    solutions = {f"unit:o012-rbt-l{lecture:02d}-sol-{number:03d}" for number in range(1, 5)}
    solves = [record for record in relations.values() if record.get("relation_type") == "solves" and (record["from_id"] in solutions or record["to_id"] in exercises)]
    if Counter(record["from_id"] for record in solves) != Counter({item: 1 for item in solutions}) or Counter(record["to_id"] for record in solves) != Counter({item: 1 for item in exercises}):
        raise SystemExit(f"Unit {lecture} exercise/solution closure mismatch")
    expected_adverse = {f"O012-ADV-{number:04d}" for number in (range(71, 83) if lecture == 6 else range(83, 95))}
    actual_corrections = [record for record in corrections.values() if record.get("unit_id") == context["root_id"]]
    if len(actual_corrections) != 12 or {record.get("adverse_ledger_id") for record in actual_corrections} != expected_adverse:
        raise SystemExit(f"Unit {lecture} one-to-one correction inventory mismatch")

alias_unit = units["unit:o012-rbt-l07-exa-003"]
alias_segment = segments["segment:o012-rbt-l07-exa-003"]
if alias_unit.get("source_aliases") != ["eg:piS^1_infinite"] or alias_segment.get("source_aliases") != ["eg:piS^1_infinite"]:
    raise SystemExit("Unit 007 source alias mismatch")

for artifact_id, metadata in ARTIFACT_META.items():
    record = artifacts[artifact_id]
    raw = (LANE / record["path"]).read_bytes()
    if len(raw) != record["bytes"] or sha256(raw) != record["sha256"]:
        raise SystemExit(f"artifact validation mismatch: {artifact_id}")
for qa_id in QA_IDS.values():
    record = qa_events[qa_id]
    if record["result"] != "passed" or any(witness not in artifacts for witness in record["witness_artifact_ids"]):
        raise SystemExit(f"QA linkage mismatch: {qa_id}")

serialized = {name: canonical_jsonl(records) for name, records in record_sets.items()}
for filename, old_lines in prior_lines.items():
    new_records = record_sets[filename]
    for record_id, old_line in old_lines.items():
        if record_id in allowed_modified_existing or record_id in owned_new_ids:
            continue
        if canonical_record(new_records[record_id]) != old_line:
            raise SystemExit(f"prior record changed outside explicit cumulative authority update: {record_id}")
for name, raw in serialized.items():
    if b"\r" in raw or not raw.endswith(b"\n"):
        raise SystemExit(f"noncanonical JSONL bytes generated for {name}")
    ids = [json.loads(line)["id"] for line in raw.decode("utf-8").splitlines()]
    if ids != sorted(ids) or len(ids) != len(set(ids)):
        raise SystemExit(f"noncanonical JSONL order generated for {name}")

for name, raw in serialized.items():
    (BACKEND / name).write_bytes(raw)

bundle = hashlib.sha256()
total_bytes = 0
for name in JSONL_NAMES:
    raw = (BACKEND / name).read_bytes()
    if raw != serialized[name]:
        raise SystemExit(f"backend post-write mismatch: {name}")
    bundle.update(name.encode("utf-8"))
    bundle.update(b"\0")
    bundle.update(raw)
    total_bytes += len(raw)

print("Units 006-007 backend extension: PASS")
print(f"unit_006_stable_ids: {SOURCE_SPECS[6]['expected_ids']}")
print(f"unit_007_stable_ids: {SOURCE_SPECS[7]['expected_ids']}")
print(f"terminology_records: {len(TERM_SPECS)}")
print(f"adverse_ledger_records: {len(CORRECTION_TARGETS)}")
print(f"new_or_owned_records: {len(owned_new_ids)}")
print(f"records: {len(all_records)}")
print(f"jsonl_files: {len(JSONL_NAMES)}")
print(f"backend_bytes: {total_bytes}")
print(f"backend_bundle_sha256: {bundle.hexdigest()}")
