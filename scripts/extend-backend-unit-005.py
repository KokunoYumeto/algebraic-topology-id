#!/usr/bin/env python3
"""Deterministically register O012/D60 Unit 005 in the interop backend.

The operation is bounded to the eleven canonical backend JSONL files. It binds
every record to the reviewed Unit 005 source, preserves unrelated records,
replaces only Unit 005/cumulative records it owns, validates references, source
spans, mastery closure, rights, correction closure, and artifacts in memory,
then writes canonical sorted UTF-8/LF JSONL.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


LANE_ROOT = Path(__file__).resolve().parent.parent
BACKEND = LANE_ROOT / "backend"
SOURCE_RELATIVE = "source/id-ID/units/unit-005-lecture-005.md"
SOURCE_PATH = LANE_ROOT / SOURCE_RELATIVE
LEDGER_PATH = LANE_ROOT / "00_control/ADVERSE_LEDGER.csv"
EXPECTED_SOURCE_BYTES = 22662
EXPECTED_SOURCE_LINES = 663
EXPECTED_SOURCE_SHA256 = "7333a7b7a92b9618016412abb5c9b2b2a398538f690d0109d4282289a0719852"
TIMESTAMP = "2026-08-22T18:00:00Z"
SCHEMA = "curriculum.interop"
SCHEMA_VERSION = "0.1.0"
WORKFLOW = "o012-d60-id-reader-production"
PROGRAM_ID = "program:o012-id"
COURSE_ID = "course:o012-d60"
RESOURCE_ID = "resource:roberts-algebraic-topology-2019"
EDITION_ID = "edition:roberts-at-2019-b947ad2"
ROBERTS_RIGHTS = "rights:roberts-cc-by-4.0"
UNIT_ROOT_ID = "unit:o012-rbt-u005"
UNIT_COMPOSITE_RIGHTS = "rights:o012-u005-composite-cc-by-4.0"
UNIT_COMPANION_RIGHTS = "rights:o012-u005-companion-cc-by-4.0"
CUMULATIVE_RIGHTS = "rights:o012-units-001-005-composite-cc-by-4.0"
UPSTREAM_COMMIT = "b947ad2e9f9e301bfe24590a9db653bc54fa1a53"

JSONL_NAMES = (
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
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def common(entity_type: str, record_id: str) -> dict[str, Any]:
    return {
        "entity_type": entity_type,
        "id": record_id,
        "schema": SCHEMA,
        "schema_version": SCHEMA_VERSION,
        "status": "active",
        "supersedes": None,
        "timestamp": TIMESTAMP,
        "workflow": WORKFLOW,
    }


def load_jsonl(name: str) -> dict[str, dict[str, Any]]:
    path = BACKEND / name
    records: dict[str, dict[str, Any]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        record = json.loads(line)
        if record["id"] in records:
            raise SystemExit(f"duplicate existing backend id: {record['id']}")
        records[record["id"]] = record
    return records


def canonical_jsonl(records: dict[str, dict[str, Any]]) -> bytes:
    return "".join(
        json.dumps(records[record_id], ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
        for record_id in sorted(records)
    ).encode("utf-8")


SOURCE_RAW = SOURCE_PATH.read_bytes()
if len(SOURCE_RAW) != EXPECTED_SOURCE_BYTES or sha256(SOURCE_RAW) != EXPECTED_SOURCE_SHA256:
    raise SystemExit("Unit 005 source identity mismatch")
SOURCE_LINES = SOURCE_RAW.splitlines(keepends=True)
if len(SOURCE_LINES) != EXPECTED_SOURCE_LINES:
    raise SystemExit(f"Unit 005 source line-count mismatch: {len(SOURCE_LINES)}")
SOURCE_TEXT_LINES = [line.decode("utf-8").rstrip("\r\n") for line in SOURCE_LINES]


def target_span(start: int, end: int) -> dict[str, Any]:
    return {
        "content_sha256": sha256(b"".join(SOURCE_LINES[start - 1 : end])),
        "file_sha256": EXPECTED_SOURCE_SHA256,
        "line_end": end,
        "line_start": start,
        "path": SOURCE_RELATIVE,
    }


ID_RE = re.compile(r"#(o012-rbt-l05(?:-[a-z0-9]+)*)")
HEADING_RE = re.compile(r"^(#{1,6})\s")
anchor_start: dict[str, int] = {}
for number, text in enumerate(SOURCE_TEXT_LINES, start=1):
    matches = ID_RE.findall(text)
    if len(matches) > 1:
        raise SystemExit(f"more than one Unit 005 stable id at line {number}")
    if matches:
        local_id = matches[0]
        if local_id in anchor_start:
            raise SystemExit(f"duplicate Unit 005 stable id: {local_id}")
        anchor_start[local_id] = number
if len(anchor_start) != 30:
    raise SystemExit(f"expected 30 Unit 005 stable ids, found {len(anchor_start)}")


def trim_blank_end(end: int, start: int) -> int:
    while end > start and not SOURCE_TEXT_LINES[end - 1].strip():
        end -= 1
    return end


def derive_span(local_id: str) -> tuple[int, int]:
    start = anchor_start[local_id]
    opening = SOURCE_TEXT_LINES[start - 1]
    heading = HEADING_RE.match(opening)
    if heading:
        level = len(heading.group(1))
        end = len(SOURCE_TEXT_LINES)
        for candidate in range(start + 1, len(SOURCE_TEXT_LINES) + 1):
            next_heading = HEADING_RE.match(SOURCE_TEXT_LINES[candidate - 1])
            if next_heading and len(next_heading.group(1)) <= level:
                end = candidate - 1
                break
        return start, trim_blank_end(end, start)
    if opening.startswith(":::"):
        for candidate in range(start + 1, len(SOURCE_TEXT_LINES) + 1):
            if SOURCE_TEXT_LINES[candidate - 1].strip() == ":::":
                return start, candidate
        raise SystemExit(f"unclosed fenced block for {local_id}")
    raise SystemExit(f"unsupported stable-id anchor at line {start}: {local_id}")


SPANS = {local_id: derive_span(local_id) for local_id in anchor_start}


NEW_CONCEPTS = {
    "branched-map": "branched map",
    "category-of-covering-spaces": "category of covering spaces",
    "compactness": "compactness",
    "critical-value": "critical value",
    "fiber-product": "fiber product",
    "fiber-transport": "fiber transport",
    "lebesgue-number": "Lebesgue number",
    "lifted-path": "lifted path",
    "monodromy": "monodromy",
    "pasting-lemma": "pasting lemma",
    "path-lifting": "path lifting",
    "path-reversal": "path reversal",
    "pointed-covering-space": "pointed covering space",
    "pullback": "pullback",
    "reparameterization": "reparameterization",
    "riemann-surface": "Riemann surface",
    "section": "section",
    "slice-category": "slice category",
    "trivial-covering-space": "trivial covering space",
    "typical-fiber": "typical fiber",
}

# display title, kind, parent id, sibling order, concept slugs
UNIT_META: dict[str, tuple[str, str, str, int, list[str]]] = {
    "o012-rbt-l05-notice": ("Tentang unit ini", "notice", UNIT_ROOT_ID, 1, []),
    "o012-rbt-l05": ("Kuliah 5", "lecture", UNIT_ROOT_ID, 2, ["covering-space", "pullback", "path-lifting", "fiber-transport"]),
    "o012-rbt-l05-s01": ("Serat ruang penutup di sepanjang lintasan", "section", "unit:o012-rbt-l05", 1, ["fiber", "typical-fiber", "pointed-covering-space", "category-of-covering-spaces"]),
    "o012-rbt-l05-proof-001": ("Bukti pertama Proposisi 4.3", "proof", "unit:o012-rbt-l05-s01", 1, ["fiber", "lebesgue-number", "evenly-covered-neighborhood"]),
    "o012-rbt-l05-exa-001": ("Contoh 5.1 (monodromi pada bidang kompleks berlubang)", "example", "unit:o012-rbt-l05-s01", 2, ["monodromy", "riemann-surface", "branched-map", "critical-value"]),
    "o012-rbt-l05-s02": ("Tarik balik ruang penutup", "section", "unit:o012-rbt-l05", 2, ["pullback", "fiber-product", "slice-category"]),
    "o012-rbt-l05-def-001": ("Definisi 5.1 (tarik balik)", "definition", "unit:o012-rbt-l05-s02", 1, ["pullback", "fiber-product", "covering-map"]),
    "o012-rbt-l05-prop-001": ("Proposisi 5.1 (sifat tarik balik)", "proposition", "unit:o012-rbt-l05-s02", 2, ["pullback", "functor", "slice-category"]),
    "o012-rbt-l05-cor-001": ("Akibat 5.1 (serat tarik balik)", "corollary", "unit:o012-rbt-l05-s02", 3, ["pullback", "fiber"]),
    "o012-rbt-l05-s03": ("Ruang penutup dari interval", "section", "unit:o012-rbt-l05", 3, ["trivial-covering-space", "section", "pasting-lemma"]),
    "o012-rbt-l05-prop-002": ("Proposisi 5.2 (trivialisasi interval)", "proposition", "unit:o012-rbt-l05-s03", 1, ["trivial-covering-space", "fiber", "homeomorphism"]),
    "o012-rbt-l05-lem-001": ("Lema 5.1 (sampul trivial berhingga)", "lemma", "unit:o012-rbt-l05-s03", 2, ["covering-map", "compactness"]),
    "o012-rbt-l05-proof-002": ("Bukti Proposisi 5.2", "proof", "unit:o012-rbt-l05-s03", 3, ["trivial-covering-space", "lebesgue-number", "pasting-lemma"]),
    "o012-rbt-l05-cor-002": ("Akibat 5.2 (penampang tunggal dengan nilai awal)", "corollary", "unit:o012-rbt-l05-s03", 4, ["section", "trivial-covering-space"]),
    "o012-rbt-l05-proof-003": ("Bukti Akibat 5.2", "proof", "unit:o012-rbt-l05-s03", 5, ["section", "discrete-topology", "connectedness"]),
    "o012-rbt-l05-s04": ("Pengangkatan lintasan dan transpor serat", "section", "unit:o012-rbt-l05", 4, ["path-lifting", "lifted-path", "fiber-transport", "reparameterization"]),
    "o012-rbt-l05-thm-001": ("Teorema 5.1 (pengangkatan lintasan tunggal)", "theorem", "unit:o012-rbt-l05-s04", 1, ["path-lifting", "lifted-path", "pullback"]),
    "o012-rbt-l05-proof-004": ("Bukti Teorema 5.1", "proof", "unit:o012-rbt-l05-s04", 2, ["path-lifting", "section", "pullback"]),
    "o012-rbt-l05-cor-003": ("Akibat 5.3 (transpor sepanjang lintasan)", "corollary", "unit:o012-rbt-l05-s04", 3, ["fiber-transport", "path-lifting"]),
    "o012-rbt-l05-proof-005": ("Bukti Akibat 5.3", "proof", "unit:o012-rbt-l05-s04", 4, ["fiber-transport", "path-reversal"]),
    "o012-rbt-l05-mastery": ("Pendamping penguasaan: pemeriksaan dan solusi lengkap", "mastery_section", UNIT_ROOT_ID, 3, ["pullback", "path-lifting", "fiber-transport"]),
    "o012-rbt-l05-mcheck-001": ("Pemeriksaan penguasaan 5.1", "exercise", "unit:o012-rbt-l05-mastery", 1, ["typical-fiber", "fiber-transport"]),
    "o012-rbt-l05-sol-001": ("Solusi Pemeriksaan 5.1", "solution", "unit:o012-rbt-l05-mastery", 2, ["typical-fiber", "fiber-transport"]),
    "o012-rbt-l05-mcheck-002": ("Pemeriksaan penguasaan 5.2", "exercise", "unit:o012-rbt-l05-mastery", 3, ["pullback", "fiber-product", "functor"]),
    "o012-rbt-l05-sol-002": ("Solusi Pemeriksaan 5.2", "solution", "unit:o012-rbt-l05-mastery", 4, ["pullback", "fiber-product", "functor"]),
    "o012-rbt-l05-check-001": ("Bukti Lema 5.1", "proof_check", "unit:o012-rbt-l05-mastery", 5, ["compactness", "covering-map"]),
    "o012-rbt-l05-mcheck-003": ("Pemeriksaan penguasaan 5.3", "exercise", "unit:o012-rbt-l05-mastery", 6, ["path-lifting", "fiber-transport", "monodromy"]),
    "o012-rbt-l05-sol-003": ("Solusi Pemeriksaan 5.3", "solution", "unit:o012-rbt-l05-mastery", 7, ["path-lifting", "fiber-transport", "monodromy"]),
    "o012-rbt-l05-mcheck-004": ("Pemeriksaan penguasaan 5.4", "exercise", "unit:o012-rbt-l05-mastery", 8, ["fiber-transport", "covering-map"]),
    "o012-rbt-l05-sol-004": ("Solusi Pemeriksaan 5.4", "solution", "unit:o012-rbt-l05-mastery", 9, ["fiber-transport", "path-lifting"]),
}
if set(UNIT_META) != set(anchor_start):
    raise SystemExit(
        f"Unit 005 metadata/stable-id mismatch: missing={sorted(set(anchor_start)-set(UNIT_META))}, "
        f"extra={sorted(set(UNIT_META)-set(anchor_start))}"
    )


def concept_ids(slugs: list[str]) -> list[str]:
    return [f"concept:{slug}" for slug in slugs]


def is_original(local_id: str) -> bool:
    return any(token in local_id for token in ("-notice", "-mastery", "-mcheck-", "-sol-", "-check-"))


def path_for(local_id: str) -> list[str]:
    unit_id = f"unit:{local_id}"
    parent_id = UNIT_META[local_id][2]
    if parent_id == UNIT_ROOT_ID:
        return [UNIT_ROOT_ID, unit_id]
    return path_for(parent_id.removeprefix("unit:")) + [unit_id]


units = load_jsonl("units.jsonl")
segments = load_jsonl("segments.jsonl")

root_locator = target_span(1, EXPECTED_SOURCE_LINES)
root = common("unit", UNIT_ROOT_ID)
root.update(
    {
        "concept_ids": concept_ids(["covering-space", "pullback", "path-lifting", "fiber-transport"]),
        "course_id": COURSE_ID,
        "display_title": "Topologi Aljabar — Unit 5: Tarik Balik, Trivialisasi Interval, dan Pengangkatan Lintasan",
        "edition_id": EDITION_ID,
        "locale": "id-ID",
        "order": 5,
        "parent_id": COURSE_ID,
        "path": [UNIT_ROOT_ID],
        "program_id": PROGRAM_ID,
        "provenance_relation": "composite_translated_and_original",
        "resource_id": RESOURCE_ID,
        "rights_component_id": UNIT_COMPOSITE_RIGHTS,
        "source_local_id": None,
        "target_locator": root_locator,
        "translation_state": "structurally_verified",
        "unit_kind": "reader_unit",
    }
)
units[UNIT_ROOT_ID] = root

upstream_locator = {
    "commit_sha": UPSTREAM_COMMIT,
    "line_end": 1304,
    "line_start": 1132,
    "path": "Notes.tex",
    "precision": "unit_range_only",
}

for local_id, (display, kind, parent_id, order, slugs) in UNIT_META.items():
    unit_id = f"unit:{local_id}"
    start, end = SPANS[local_id]
    locator = target_span(start, end)
    original = is_original(local_id)
    provenance = "edition_original" if original else "translated_adapted_from_upstream"
    rights_id = UNIT_COMPANION_RIGHTS if original else ROBERTS_RIGHTS
    unit = common("unit", unit_id)
    unit.update(
        {
            "concept_ids": concept_ids(slugs),
            "course_id": COURSE_ID,
            "display_title": display,
            "edition_id": EDITION_ID,
            "locale": "id-ID",
            "order": order,
            "parent_id": parent_id,
            "path": path_for(local_id),
            "program_id": PROGRAM_ID,
            "provenance_relation": provenance,
            "resource_id": RESOURCE_ID,
            "rights_component_id": rights_id,
            "source_local_id": local_id,
            "target_locator": locator,
            "translation_state": "structurally_verified",
            "unit_kind": kind,
        }
    )
    units[unit_id] = unit

    segment_id = f"segment:{local_id}"
    segment = common("segment", segment_id)
    segment.update(
        {
            "concept_ids": concept_ids(slugs),
            "edition_id": EDITION_ID,
            "locale": "id-ID",
            "order": order,
            "provenance_relation": provenance,
            "resource_id": RESOURCE_ID,
            "rights_component_id": rights_id,
            "segment_kind": kind,
            "source_local_id": local_id,
            "source_locator": (
                {"kind": "edition_original", "path": SOURCE_RELATIVE, "precision": "exact_target_span"}
                if original
                else dict(upstream_locator)
            ),
            "target_locator": locator,
            "translation_state": "structurally_verified",
            "unit_id": unit_id,
        }
    )
    segments[segment_id] = segment


concepts = load_jsonl("concepts.jsonl")
for slug, label in NEW_CONCEPTS.items():
    record_id = f"concept:{slug}"
    record = common("concept", record_id)
    record.update({"canonical_label": label, "domain": "algebraic_topology", "locale_neutral": True})
    concepts[record_id] = record


TERM_META = {
    "branched-map": ("pemetaan bercabang", "o012-rbt-l05-exa-001", []),
    "category-of-covering-spaces": ("kategori ruang penutup", "o012-rbt-l05-s01", []),
    "critical-value": ("nilai kritis", "o012-rbt-l05-exa-001", []),
    "fiber-product": ("hasil kali serat", "o012-rbt-l05-def-001", []),
    "fiber-transport": ("transpor serat", "o012-rbt-l05-cor-003", []),
    "lebesgue-number": ("bilangan Lebesgue", "o012-rbt-l05-proof-001", []),
    "lifted-path": ("lintasan terangkat", "o012-rbt-l05-thm-001", []),
    "monodromy": ("monodromi", "o012-rbt-l05-exa-001", []),
    "pasting-lemma": ("lema penempelan", "o012-rbt-l05-proof-002", []),
    "path-lifting": ("pengangkatan lintasan", "o012-rbt-l05-thm-001", []),
    "path-reversal": ("lintasan balik", "o012-rbt-l05-proof-005", []),
    "pointed-covering-space": ("ruang penutup bertitik", "o012-rbt-l05-s01", []),
    "pullback": ("tarik balik", "o012-rbt-l05-def-001", []),
    "reparameterization": ("reparameterisasi", "o012-rbt-l05-s04", []),
    "riemann-surface": ("permukaan Riemann", "o012-rbt-l05-exa-001", []),
    "section": ("penampang", "o012-rbt-l05-cor-002", []),
    "slice-category": ("kategori irisan", "o012-rbt-l05-prop-001", []),
    "trivial-covering-space": ("ruang penutup trivial", "o012-rbt-l05-prop-002", []),
    "typical-fiber": ("serat tipikal", "o012-rbt-l05-s01", []),
}

terms = load_jsonl("terms.jsonl")
for slug, (preferred, evidence_local_id, variants) in TERM_META.items():
    record_id = f"term:{slug}:id-ID"
    record = common("term", record_id)
    record.update(
        {
            "concept_id": f"concept:{slug}",
            "evidence_segment_id": f"segment:{evidence_local_id}",
            "locale": "id-ID",
            "preferred": preferred,
            "register": "textbook",
            "rejected_forms": [],
            "rights_component_id": ROBERTS_RIGHTS,
            "scope_unit_id": UNIT_ROOT_ID,
            "variants": variants,
        }
    )
    terms[record_id] = record


rights = load_jsonl("rights.jsonl")
companion = common("rights", UNIT_COMPANION_RIGHTS)
companion.update(
    {
        "attribution": "Original Indonesian mastery companion and edition notice for O012/D60 Unit 005.",
        "change_notice": "Newly authored material; not represented as source-author text.",
        "component_scope": ["unit:o012-rbt-l05-notice", "unit:o012-rbt-l05-mastery"],
        "license_expression": "CC-BY-4.0",
        "license_url": "https://creativecommons.org/licenses/by/4.0/",
        "non_endorsement": "No endorsement by David Michael Roberts or affiliated institutions is implied.",
        "third_party_status": "No external media component.",
    }
)
rights[UNIT_COMPANION_RIGHTS] = companion

unit_composite = common("rights", UNIT_COMPOSITE_RIGHTS)
unit_composite.update(
    {
        "attribution": "Composite Unit 005 reader: Roberts source adaptation plus independently authored Indonesian mastery companion; component provenance remains separated.",
        "change_notice": "See component rights records for the translated/adapted and original portions.",
        "component_scope": [UNIT_ROOT_ID],
        "license_expression": "CC-BY-4.0",
        "license_url": "https://creativecommons.org/licenses/by/4.0/",
        "non_endorsement": "Independent edition; no source-author endorsement.",
        "third_party_status": "Component-scoped rights records control.",
    }
)
rights[UNIT_COMPOSITE_RIGHTS] = unit_composite

cumulative = common("rights", CUMULATIVE_RIGHTS)
cumulative.update(
    {
        "attribution": "Cumulative Units 001-005 reader: David Michael Roberts source adaptations plus independently authored Indonesian mastery companions; component provenance remains separated.",
        "change_notice": "Cumulative staged boundary only; Unit 001 through Unit 005 component rights records remain controlling.",
        "component_scope": [f"unit:o012-rbt-u{number:03d}" for number in range(1, 6)],
        "license_expression": "CC-BY-4.0",
        "license_url": "https://creativecommons.org/licenses/by/4.0/",
        "non_endorsement": "Independent edition; no source-author endorsement.",
        "third_party_status": "Component-scoped rights records control.",
    }
)
rights[CUMULATIVE_RIGHTS] = cumulative

roberts = rights[ROBERTS_RIGHTS]
roberts["component_scope"] = [f"unit:o012-rbt-l{number:02d}" for number in range(1, 6)]
roberts["third_party_status"] = "No distinct third-party component is asserted within Units 001-005; the frozen archive remains authoritative for file-level review."
roberts["timestamp"] = TIMESTAMP


authority = load_jsonl("authority.jsonl")
for authority_id in (PROGRAM_ID, COURSE_ID):
    authority[authority_id]["rights_component_id"] = CUMULATIVE_RIGHTS
    authority[authority_id]["timestamp"] = TIMESTAMP
edition = authority[EDITION_ID]
edition["local_derivative_unit_ids"] = [f"unit:o012-rbt-u{number:03d}" for number in range(1, 6)]
edition["source_line_end"] = 1304
edition["timestamp"] = TIMESTAMP


assets = load_jsonl("assets.jsonl")
asset_id = "asset:o012-u005-source-markdown"
asset = common("asset", asset_id)
asset.update(
    {
        "bytes": EXPECTED_SOURCE_BYTES,
        "edition_id": EDITION_ID,
        "media_type": "text/markdown; charset=utf-8",
        "path": SOURCE_RELATIVE,
        "resource_id": RESOURCE_ID,
        "rights_component_id": UNIT_COMPOSITE_RIGHTS,
        "role": "canonical_reader_source",
        "sha256": EXPECTED_SOURCE_SHA256,
    }
)
assets[asset_id] = asset


relations = load_jsonl("relations.jsonl")


def add_relation(record_id: str, from_id: str, relation_type: str, to_id: str, note: str) -> None:
    record = common("relation", record_id)
    record.update({"from_id": from_id, "note": note, "relation_type": relation_type, "to_id": to_id})
    relations[record_id] = record


add_relation("relation:adapts:o012-rbt-u005:roberts-edition", UNIT_ROOT_ID, "adapts", EDITION_ID, "Unit 005 adapts Notes.tex lines 1132-1304 and adds an original solved mastery companion.")
add_relation("relation:precedes:l05:mastery", "unit:o012-rbt-l05", "precedes", "unit:o012-rbt-l05-mastery", "The translated lecture precedes its original solved mastery companion.")
add_relation("relation:precedes:u004:u005", "unit:o012-rbt-u004", "precedes", UNIT_ROOT_ID, "Cumulative reader order.")
add_relation("relation:proves:l05-proof-001:l04-prop-003", "unit:o012-rbt-l05-proof-001", "proves", "unit:o012-rbt-l04-prop-003", "First proof that fibers over endpoints of a path are isomorphic.")
add_relation("relation:proves:l05-proof-002:l05-prop-002", "unit:o012-rbt-l05-proof-002", "proves", "unit:o012-rbt-l05-prop-002", "Proof that every covering over the interval is trivial.")
add_relation("relation:proves:l05-proof-003:l05-cor-002", "unit:o012-rbt-l05-proof-003", "proves", "unit:o012-rbt-l05-cor-002", "Proof of the unique normalized section over the interval.")
add_relation("relation:proves:l05-proof-004:l05-thm-001", "unit:o012-rbt-l05-proof-004", "proves", "unit:o012-rbt-l05-thm-001", "Proof of unique path lifting through the pullback covering.")
add_relation("relation:proves:l05-proof-005:l05-cor-003", "unit:o012-rbt-l05-proof-005", "proves", "unit:o012-rbt-l05-cor-003", "Proof that reverse-path transport is the inverse.")
add_relation("relation:proves:l05-check-001:l05-lem-001", "unit:o012-rbt-l05-check-001", "proves", "unit:o012-rbt-l05-lem-001", "The original companion supplies the omitted compactness proof.")
for number in range(1, 5):
    add_relation(
        f"relation:solves:l05-sol-{number:03d}:l05-mcheck-{number:03d}",
        f"unit:o012-rbt-l05-sol-{number:03d}",
        "solves",
        f"unit:o012-rbt-l05-mcheck-{number:03d}",
        f"Complete solution to Mastery Check 5.{number}.",
    )


# correction type, affected stable IDs, record slug
CORRECTION_META: dict[str, tuple[str, list[str], str]] = {
    "O012-ADV-0054": ("mathematical_correction", ["o012-rbt-l05-proof-001"], "path-subdivision-proof"),
    "O012-ADV-0055": ("clarification", ["o012-rbt-l05-proof-001"], "path-endpoint-equations"),
    "O012-ADV-0056": ("clarification", ["o012-rbt-l05-s01"], "typical-fiber-noncanonicity"),
    "O012-ADV-0057": ("mathematical_correction", ["o012-rbt-l05-s01"], "pointed-covering-types"),
    "O012-ADV-0058": ("clarification", ["o012-rbt-l05-s01"], "empty-fiber-convention"),
    "O012-ADV-0059": ("clarification", ["o012-rbt-l05-s01"], "covering-category-morphisms"),
    "O012-ADV-0060": ("mathematical_correction", ["o012-rbt-l05-exa-001"], "complex-monodromy-scope"),
    "O012-ADV-0061": ("mathematical_correction", ["o012-rbt-l05-def-001"], "fiber-product-scope"),
    "O012-ADV-0062": ("clarification", ["o012-rbt-l05-prop-001"], "pullback-proof-closure"),
    "O012-ADV-0063": ("clarification", ["o012-rbt-l05-proof-002"], "interval-chain-gluing"),
    "O012-ADV-0064": ("mathematical_correction", ["o012-rbt-l05-proof-002", "o012-rbt-l05-proof-003"], "normalized-trivialization"),
    "O012-ADV-0065": ("mathematical_correction", ["o012-rbt-l05-proof-002"], "transition-first-projection"),
    "O012-ADV-0066": ("mathematical_correction", ["o012-rbt-l05-proof-002"], "actual-gluing-maps"),
    "O012-ADV-0067": ("mathematical_correction", ["o012-rbt-l05-proof-003"], "section-uniqueness"),
    "O012-ADV-0068": ("mathematical_correction", ["o012-rbt-l05-proof-004"], "path-lift-notation"),
    "O012-ADV-0069": ("mathematical_correction", ["o012-rbt-l05-proof-005"], "reverse-path-variable"),
    "O012-ADV-0070": ("structural_adaptation", ["o012-rbt-l05-s04"], "reparameterization-reflow"),
}

with LEDGER_PATH.open("r", encoding="utf-8", newline="") as stream:
    all_ledger_rows = list(csv.DictReader(stream))
if any(None in row for row in all_ledger_rows):
    raise SystemExit("adverse ledger contains a non-canonical CSV row")
ledger_rows = {row["event_id"]: row for row in all_ledger_rows if row["event_id"] in CORRECTION_META}
if set(ledger_rows) != set(CORRECTION_META):
    raise SystemExit(f"Unit 005 adverse ledger mismatch: {sorted(set(CORRECTION_META)-set(ledger_rows))}")
if any(len(row) != 7 for row in ledger_rows.values()):
    raise SystemExit("Unit 005 adverse ledger rows must each have exactly seven columns")

corrections = load_jsonl("corrections.jsonl")
for event_id, (correction_type, affected_local_ids, slug) in CORRECTION_META.items():
    row = ledger_rows[event_id]
    affected_unit_ids = [f"unit:{local_id}" for local_id in affected_local_ids]
    target_locations = [f"{SPANS[local_id][0]}-{SPANS[local_id][1]}" for local_id in affected_local_ids]
    record_id = f"correction:o012-u005-adv-{event_id[-4:]}-{slug}"
    record = common("correction", record_id)
    record.update(
        {
            "adverse_ledger_id": event_id,
            "affected_unit_ids": affected_unit_ids,
            "correction_type": correction_type,
            "edition_id": EDITION_ID,
            "evidence": f"{row['source_location']}; target spans {', '.join(target_locations)}.",
            "evidence_segment_id": "segment:o012-rbt-l05-notice",
            "rationale": row["rationale"],
            "resource_id": RESOURCE_ID,
            "source_defect": row["observed"],
            "target_change": row["action"],
            "unit_id": UNIT_ROOT_ID,
            "upstream_report_disposition": "not_contacted",
        }
    )
    corrections[record_id] = record


QA_SOURCE = "qa:o012-u005-source-integrity"
QA_MATH = "qa:o012-u005-math-review"
QA_LANGUAGE = "qa:o012-u005-language-review"
QA_BUILD = "qa:o012-units-001-005-build"
QA_ACCESSIBILITY = "qa:o012-units-001-005-accessibility"
QA_VISUAL = "qa:o012-units-001-005-visual"
ARTIFACT_MANIFEST_ID = "artifact:o012-units-001-005-manifest"

ARTIFACT_META = {
    "artifact:o012-u005-independent-review": {
        "bytes": 1592,
        "manifest_artifact_id": None,
        "media_type": "text/markdown; charset=utf-8",
        "path": "qa/UNIT_005_INDEPENDENT_REVIEW.md",
        "qa_event_ids": [QA_LANGUAGE, QA_MATH, QA_SOURCE],
        "sha256": "399b81a06ac5701eca6604406c40acaa76f100291ee57f8efeb5344e7d7c8de0",
        "toolchain": "Independent read-only exact-span, mathematical, Indonesian-language, and structural final review.",
        "translation_state": "mathematically_reviewed",
    },
    "artifact:o012-units-001-005-html": {
        "bytes": 610594,
        "manifest_artifact_id": ARTIFACT_MANIFEST_ID,
        "media_type": "text/html; charset=utf-8",
        "path": "output/html/units-001-005/index.html",
        "qa_event_ids": [QA_ACCESSIBILITY, QA_BUILD, QA_VISUAL],
        "sha256": "8d3accf480101565409909c05f987f44b73f1c98889128e2f5074a4e049f48f3",
        "toolchain": "Pandoc 3.9.0.2 standalone HTML5 with embedded CSS and native MathML.",
        "translation_state": "built",
    },
    ARTIFACT_MANIFEST_ID: {
        "bytes": 247,
        "manifest_artifact_id": None,
        "media_type": "text/csv; charset=utf-8",
        "path": "output/ARTIFACT_MANIFEST_UNITS_001_005.csv",
        "qa_event_ids": [QA_BUILD],
        "sha256": "2910fd87871675730aea7ca33e636a70d330d0f81183e887bad74ea1fd2d5190",
        "toolchain": "Cumulative Units 001-005 deterministic artifact manifest.",
        "translation_state": "built",
    },
    "artifact:o012-units-001-005-pdf": {
        "bytes": 589065,
        "manifest_artifact_id": ARTIFACT_MANIFEST_ID,
        "media_type": "application/pdf",
        "path": "output/pdf/topologi-aljabar-unit-001-005-id.pdf",
        "qa_event_ids": [QA_ACCESSIBILITY, QA_BUILD, QA_VISUAL],
        "sha256": "d6929434a9bc7ae78fb71fc060e9cc54dce85d37e4997ffe042ccbab982e64e2",
        "toolchain": "Pandoc 3.9.0.2 with pdflatex; two 21 mm fixed-epoch builds were byte-identical.",
        "translation_state": "built",
    },
    "artifact:o012-units-001-005-qa-receipt": {
        "bytes": 4768,
        "manifest_artifact_id": None,
        "media_type": "application/json",
        "path": "qa/UNITS_001_005_QA.json",
        "qa_event_ids": [QA_LANGUAGE, QA_MATH, QA_SOURCE, QA_ACCESSIBILITY, QA_BUILD, QA_VISUAL],
        "sha256": "ffb6703e4fe2ebc1c7733dc4f87a32c64c53cbe3ebf326d65a8d2da94765635a",
        "toolchain": "Unit 005 independent review, cumulative structural QA, Poppler PDF checks, and manual browser/PDF review.",
        "translation_state": "built",
    },
    "artifact:o012-units-001-005-qa-text": {
        "bytes": 128786,
        "manifest_artifact_id": None,
        "media_type": "text/plain; charset=utf-8",
        "path": "qa/units-001-005-extracted.txt",
        "qa_event_ids": [QA_MATH, QA_BUILD],
        "sha256": "83aca1060966c7ca7a7852630c27926754f0d893749aeb80888bbfd00f56a725",
        "toolchain": "Poppler pdftotext with layout preservation and UTF-8 output.",
        "translation_state": "built",
    },
    "artifact:o012-units-001-005-visual-receipt": {
        "bytes": 2877,
        "manifest_artifact_id": None,
        "media_type": "text/markdown; charset=utf-8",
        "path": "qa/UNITS_001_005_VISUAL_QA.md",
        "qa_event_ids": [QA_ACCESSIBILITY, QA_VISUAL],
        "sha256": "ed8249702d8335b01dc40925af1d5b071fa18d2eef9fe628a5535bd9404fbcdd",
        "toolchain": "Poppler all-page PDF rendering plus Codex in-app Chromium desktop/mobile responsive inspection.",
        "translation_state": "visually_checked",
    },
}

artifacts = load_jsonl("artifacts.jsonl")
for artifact_id, metadata in ARTIFACT_META.items():
    artifact_path = LANE_ROOT / metadata["path"]
    if not artifact_path.is_file():
        raise SystemExit(f"missing final Unit 001-005 artifact: {metadata['path']}")
    raw = artifact_path.read_bytes()
    if len(raw) != metadata["bytes"] or sha256(raw) != metadata["sha256"]:
        raise SystemExit(f"final Unit 001-005 artifact identity mismatch: {metadata['path']}")
    record = common("artifact", artifact_id)
    record.update(
        {
            **metadata,
            "locale": "id-ID",
            "rights_component_id": CUMULATIVE_RIGHTS,
            "unit_id": UNIT_ROOT_ID,
        }
    )
    artifacts[artifact_id] = record


QA_META = {
    QA_SOURCE: {
        "qa_type": "source",
        "note": "The cumulative validator binds Roberts Notes.tex lines 1132-1304 to all 30 Unit 5 stable IDs, preserves 172 stable IDs across Units 001-005, and verifies the one-to-one O012-ADV-0054 through O012-ADV-0070 correction/reflow inventory.",
        "witness_artifact_ids": ["artifact:o012-u005-independent-review", "artifact:o012-units-001-005-qa-receipt"],
    },
    QA_MATH: {
        "qa_type": "math",
        "note": "Independent exact-span mathematical replay passed after sixteen disclosed source corrections and one accessibility reflow; all four mastery checks, the omitted compactness proof, and the omitted pullback proof have complete checked companions, with P1, P2, and P3 all zero.",
        "witness_artifact_ids": ["artifact:o012-u005-independent-review", "artifact:o012-units-001-005-qa-receipt", "artifact:o012-units-001-005-qa-text"],
    },
    QA_LANGUAGE: {
        "qa_type": "language",
        "note": "Independent final Indonesian-language replay found no P1, P2, or P3 issue and no active English prose outside protected names, notation, URLs, and markup.",
        "witness_artifact_ids": ["artifact:o012-u005-independent-review"],
    },
    QA_BUILD: {
        "qa_type": "build",
        "note": "Two fixed-epoch cumulative PDF builds were byte-identical; HTML, PDF, manifest, extracted-text witness, and QA receipt are hash-consistent while every earlier release artifact remains unchanged.",
        "witness_artifact_ids": ["artifact:o012-units-001-005-html", ARTIFACT_MANIFEST_ID, "artifact:o012-units-001-005-pdf", "artifact:o012-units-001-005-qa-receipt", "artifact:o012-units-001-005-qa-text"],
    },
    QA_ACCESSIBILITY: {
        "qa_type": "accessibility",
        "note": "Semantic HTML passed with lang=id-ID, 1659 native MathML nodes, 240 unique HTML IDs, all 66 local fragment links resolving, no scripts or external runtime dependency, desktop centering, mobile reflow, and 17 formula-local horizontal-scroll surfaces. PDF remains explicitly secondary and untagged.",
        "witness_artifact_ids": ["artifact:o012-units-001-005-html", "artifact:o012-units-001-005-qa-receipt", "artifact:o012-units-001-005-visual-receipt"],
    },
    QA_VISUAL: {
        "qa_type": "visual",
        "note": "All 44 PDF pages and the cumulative HTML title, contents, Unit 5, and mastery surfaces at 1280x720 and 390x844 were inspected; the cumulative-only 21 mm geometry removed an isolated continuation page without clipping or readability loss.",
        "witness_artifact_ids": ["artifact:o012-units-001-005-html", "artifact:o012-units-001-005-pdf", "artifact:o012-units-001-005-visual-receipt"],
    },
}

qa_events = load_jsonl("qa.jsonl")
for qa_id, metadata in QA_META.items():
    record = common("qa_event", qa_id)
    record.update({**metadata, "result": "passed", "unit_id": UNIT_ROOT_ID})
    qa_events[qa_id] = record


record_sets = {
    "artifacts.jsonl": artifacts,
    "assets.jsonl": assets,
    "authority.jsonl": authority,
    "concepts.jsonl": concepts,
    "corrections.jsonl": corrections,
    "qa.jsonl": qa_events,
    "relations.jsonl": relations,
    "rights.jsonl": rights,
    "segments.jsonl": segments,
    "terms.jsonl": terms,
    "units.jsonl": units,
}
if tuple(record_sets) != JSONL_NAMES:
    raise SystemExit("backend JSONL inventory/order mismatch")

all_records: dict[str, dict[str, Any]] = {}
for filename, records in record_sets.items():
    for record_id, record in records.items():
        if record_id in all_records:
            raise SystemExit(f"duplicate global backend id after extension: {record_id}")
        if record.get("id") != record_id:
            raise SystemExit(f"backend key/id mismatch in {filename}: {record_id}")
        if record.get("schema") != SCHEMA or record.get("schema_version") != SCHEMA_VERSION:
            raise SystemExit(f"schema/version mismatch: {record_id}")
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
        if field in record:
            value = record[field]
            if not isinstance(value, list) or any(item not in all_records for item in value):
                raise SystemExit(f"unknown/list backend reference in {record_id}.{field}")

for local_id in UNIT_META:
    unit = units[f"unit:{local_id}"]
    segment = segments[f"segment:{local_id}"]
    if unit["target_locator"] != segment["target_locator"]:
        raise SystemExit(f"Unit 005 unit/segment locator mismatch: {local_id}")
    locator = unit["target_locator"]
    start, end = locator["line_start"], locator["line_end"]
    if locator != target_span(start, end) or local_id not in SOURCE_TEXT_LINES[start - 1]:
        raise SystemExit(f"Unit 005 target span mismatch: {local_id}")
    if unit["path"] != path_for(local_id) or unit["path"][-1] != unit["id"]:
        raise SystemExit(f"Unit 005 hierarchy mismatch: {local_id}")
if units[UNIT_ROOT_ID]["target_locator"] != root_locator:
    raise SystemExit("Unit 005 root locator mismatch")

new_exercises = {f"unit:o012-rbt-l05-mcheck-{number:03d}" for number in range(1, 5)}
new_solutions = {f"unit:o012-rbt-l05-sol-{number:03d}" for number in range(1, 5)}
new_solves = [
    relation for relation in relations.values()
    if relation["entity_type"] == "relation"
    and relation["relation_type"] == "solves"
    and (relation["from_id"] in new_solutions or relation["to_id"] in new_exercises)
]
if (
    Counter(relation["from_id"] for relation in new_solves) != Counter({item: 1 for item in new_solutions})
    or Counter(relation["to_id"] for relation in new_solves) != Counter({item: 1 for item in new_exercises})
):
    raise SystemExit("Unit 005 exercise/solution closure mismatch")

unit5_corrections = [record for record in corrections.values() if record.get("unit_id") == UNIT_ROOT_ID]
if len(unit5_corrections) != 17 or {record.get("adverse_ledger_id") for record in unit5_corrections} != set(CORRECTION_META):
    raise SystemExit("Unit 005 one-to-one correction inventory mismatch")
if {record["adverse_ledger_id"] for record in unit5_corrections if record["correction_type"] == "structural_adaptation"} != {"O012-ADV-0070"}:
    raise SystemExit("Unit 005 structural reflow inventory mismatch")

for artifact_id, metadata in ARTIFACT_META.items():
    record = artifacts[artifact_id]
    path = LANE_ROOT / record["path"]
    raw = path.read_bytes()
    if len(raw) != record["bytes"] or sha256(raw) != record["sha256"]:
        raise SystemExit(f"Unit 005 artifact validation mismatch: {artifact_id}")
for qa_id in QA_META:
    record = qa_events[qa_id]
    if record["result"] != "passed" or any(witness not in artifacts for witness in record["witness_artifact_ids"]):
        raise SystemExit(f"Unit 005 QA linkage mismatch: {qa_id}")

serialized = {name: canonical_jsonl(records) for name, records in record_sets.items()}
for name, raw in serialized.items():
    if b"\r" in raw or not raw.endswith(b"\n"):
        raise SystemExit(f"noncanonical JSONL bytes generated for {name}")
    decoded = raw.decode("utf-8").splitlines()
    ids = [json.loads(line)["id"] for line in decoded]
    if ids != sorted(ids) or len(ids) != len(set(ids)):
        raise SystemExit(f"noncanonical JSONL ordering generated for {name}")

for name, raw in serialized.items():
    (BACKEND / name).write_bytes(raw)

bundle = hashlib.sha256()
total_bytes = 0
for name in JSONL_NAMES:
    raw = (BACKEND / name).read_bytes()
    if raw != serialized[name]:
        raise SystemExit(f"backend post-write readback mismatch: {name}")
    bundle.update(name.encode("utf-8"))
    bundle.update(b"\0")
    bundle.update(raw)
    total_bytes += len(raw)

print("Unit 005 backend extension: PASS")
print(f"stable_ids: {len(anchor_start)}")
print(f"source_sha256: {EXPECTED_SOURCE_SHA256}")
print(f"adverse_ledger_records: {len(CORRECTION_META)}")
print(f"records: {len(all_records)}")
print(f"jsonl_files: {len(JSONL_NAMES)}")
print(f"backend_bytes: {total_bytes}")
print(f"backend_bundle_sha256: {bundle.hexdigest()}")
