#!/usr/bin/env python3
"""Deterministically register O012/D60 Unit 004 in the interop backend.

This script is intentionally bounded to the eleven backend JSONL files.  It
verifies the frozen Unit 004 source, derives exact target spans from stable
Markdown identifiers, preserves all unrelated records, replaces only the
records it owns, and writes canonical sorted UTF-8/LF JSONL.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
from pathlib import Path
from typing import Any


LANE_ROOT = Path(__file__).resolve().parent.parent
BACKEND = LANE_ROOT / "backend"
SOURCE_RELATIVE = "source/id-ID/units/unit-004-lecture-004.md"
SOURCE_PATH = LANE_ROOT / SOURCE_RELATIVE
LEDGER_PATH = LANE_ROOT / "00_control/ADVERSE_LEDGER.csv"
EXPECTED_SOURCE_BYTES = 24582
EXPECTED_SOURCE_LINES = 632
EXPECTED_SOURCE_SHA256 = "826fcb368275cdad02f72a5cec951fc8466ba68b09ca0139d72c81a4c5591fea"
TIMESTAMP = "2026-08-22T12:00:00Z"
SCHEMA = "curriculum.interop"
SCHEMA_VERSION = "0.1.0"
WORKFLOW = "o012-d60-id-reader-production"
PROGRAM_ID = "program:o012-id"
COURSE_ID = "course:o012-d60"
RESOURCE_ID = "resource:roberts-algebraic-topology-2019"
EDITION_ID = "edition:roberts-at-2019-b947ad2"
ROBERTS_RIGHTS = "rights:roberts-cc-by-4.0"
UNIT_ROOT_ID = "unit:o012-rbt-u004"
UNIT_COMPOSITE_RIGHTS = "rights:o012-u004-composite-cc-by-4.0"
UNIT_COMPANION_RIGHTS = "rights:o012-u004-companion-cc-by-4.0"
CUMULATIVE_RIGHTS = "rights:o012-units-001-004-composite-cc-by-4.0"
UPSTREAM_COMMIT = "b947ad2e9f9e301bfe24590a9db653bc54fa1a53"


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
        records[record["id"]] = record
    return records


def write_jsonl(name: str, records: dict[str, dict[str, Any]]) -> None:
    path = BACKEND / name
    text = "".join(
        json.dumps(records[record_id], ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
        for record_id in sorted(records)
    )
    path.write_text(text, encoding="utf-8", newline="\n")


SOURCE_RAW = SOURCE_PATH.read_bytes()
if len(SOURCE_RAW) != EXPECTED_SOURCE_BYTES:
    raise SystemExit(f"Unit 004 source byte mismatch: {len(SOURCE_RAW)}")
if sha256(SOURCE_RAW) != EXPECTED_SOURCE_SHA256:
    raise SystemExit("Unit 004 source SHA-256 mismatch")
SOURCE_LINES = SOURCE_RAW.splitlines(keepends=True)
if len(SOURCE_LINES) != EXPECTED_SOURCE_LINES:
    raise SystemExit(f"Unit 004 source line-count mismatch: {len(SOURCE_LINES)}")
SOURCE_TEXT_LINES = [line.decode("utf-8").rstrip("\r\n") for line in SOURCE_LINES]


def target_span(start: int, end: int) -> dict[str, Any]:
    return {
        "content_sha256": sha256(b"".join(SOURCE_LINES[start - 1 : end])),
        "file_sha256": EXPECTED_SOURCE_SHA256,
        "line_end": end,
        "line_start": start,
        "path": SOURCE_RELATIVE,
    }


ID_RE = re.compile(r"#(o012-rbt-l04(?:-[a-z0-9]+)*)")
HEADING_RE = re.compile(r"^(#{1,6})\s")
anchor_start: dict[str, int] = {}
for number, text in enumerate(SOURCE_TEXT_LINES, start=1):
    matches = ID_RE.findall(text)
    if len(matches) > 1:
        raise SystemExit(f"more than one Unit 004 stable id at line {number}")
    if matches:
        local_id = matches[0]
        if local_id in anchor_start:
            raise SystemExit(f"duplicate Unit 004 stable id: {local_id}")
        anchor_start[local_id] = number

if len(anchor_start) != 33:
    raise SystemExit(f"expected 33 Unit 004 stable ids, found {len(anchor_start)}")


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
    "base-space": "base space",
    "coproduct-preservation": "preservation of coproducts",
    "covering-composition": "composition of covering maps",
    "covering-map": "covering map",
    "evenly-covered-neighborhood": "evenly covered neighborhood",
    "fiber": "fiber",
    "natural-isomorphism": "natural isomorphism",
    "natural-transformation": "natural transformation",
    "pointed-homotopy": "pointed homotopy",
    "pointed-space": "pointed space",
    "quotient-map": "quotient map",
    "semilocally-path-connected-space": "semilocally path-connected space",
    "topologist-sine-curve": "topologist's sine curve",
    "wedge-sum": "wedge sum",
}


# display title, kind, parent id, sibling order, concept slugs
UNIT_META: dict[str, tuple[str, str, str, int, list[str]]] = {
    "o012-rbt-l04-notice": ("Tentang unit ini", "notice", UNIT_ROOT_ID, 1, []),
    "o012-rbt-l04": ("Kuliah 4", "lecture", UNIT_ROOT_ID, 2, ["homotopy-category", "natural-transformation", "semilocally-path-connected-space", "pointed-space", "covering-space"]),
    "o012-rbt-l04-s01": ("Funktor pada kategori homotopi", "section", "unit:o012-rbt-l04", 1, ["functor", "homotopy-category", "connected-component-set", "path-component", "natural-transformation", "coproduct-preservation"]),
    "o012-rbt-l04-prop-001": ("Proposisi 4.1 (π₀ pada kategori homotopi)", "proposition", "unit:o012-rbt-l04-s01", 1, ["connected-component-set", "functor", "homotopy-category", "homotopy"]),
    "o012-rbt-l04-proof-001": ("Bukti Proposisi 4.1", "proof", "unit:o012-rbt-l04-s01", 2, ["connected-component-set", "homotopy", "connected-component"]),
    "o012-rbt-l04-ex-001": ("Latihan 4.1", "exercise", "unit:o012-rbt-l04-s01", 3, ["path-component", "functor", "homotopy-category", "homotopy-class"]),
    "o012-rbt-l04-lem-001": ("Lema 4.1 (pelestarian koproduk)", "lemma", "unit:o012-rbt-l04-s01", 4, ["coproduct-preservation", "disjoint-union", "connected-component-set", "path-component"]),
    "o012-rbt-l04-exa-001": ("Contoh 4.1 (kardinalitas komponen)", "example", "unit:o012-rbt-l04-s01", 5, ["connected-component-set", "continuity"]),
    "o012-rbt-l04-exa-002": ("Contoh 4.2 (kurva sinus topolog)", "example", "unit:o012-rbt-l04-s01", 6, ["topologist-sine-curve", "connectedness", "path-connectedness", "path-component", "subspace-topology"]),
    "o012-rbt-l04-ex-002": ("Latihan 4.2", "exercise", "unit:o012-rbt-l04-s01", 7, ["topologist-sine-curve", "path", "intermediate-value-theorem"]),
    "o012-rbt-l04-def-001": ("Definisi 4.1 (transformasi natural)", "definition", "unit:o012-rbt-l04-s01", 8, ["natural-transformation", "natural-isomorphism", "functor", "category"]),
    "o012-rbt-l04-s02": ("Ruang terhubung lintasan semilokal", "section", "unit:o012-rbt-l04", 2, ["semilocally-path-connected-space", "path-component", "connected-component"]),
    "o012-rbt-l04-def-002": ("Definisi 4.2 (terhubung lintasan semilokal)", "definition", "unit:o012-rbt-l04-s02", 1, ["semilocally-path-connected-space", "neighborhood-basis", "path"]),
    "o012-rbt-l04-prop-002": ("Proposisi 4.2 (komponen lintasan dan komponen terhubung)", "proposition", "unit:o012-rbt-l04-s02", 2, ["semilocally-path-connected-space", "path-component", "connected-component"]),
    "o012-rbt-l04-proof-002": ("Bukti Proposisi 4.2", "proof", "unit:o012-rbt-l04-s02", 3, ["semilocally-path-connected-space", "path-component", "connected-component", "characteristic-function"]),
    "o012-rbt-l04-exa-003": ("Contoh 4.3", "example", "unit:o012-rbt-l04-s02", 4, ["path-connectedness", "semilocally-path-connected-space"]),
    "o012-rbt-l04-ex-003": ("Latihan 4.3", "exercise", "unit:o012-rbt-l04-s02", 5, ["semilocally-path-connected-space", "product-topology"]),
    "o012-rbt-l04-exa-004": ("Contoh 4.4 (manifold)", "example", "unit:o012-rbt-l04-s02", 6, ["semilocally-path-connected-space", "manifold-atlas", "euclidean-topology"]),
    "o012-rbt-l04-q-001": ("Pertanyaan 4.1", "question", "unit:o012-rbt-l04-s02", 7, ["semilocally-path-connected-space", "quotient-map", "final-topology"]),
    "o012-rbt-l04-s03": ("Ruang dan homotopi bertitik", "section", "unit:o012-rbt-l04", 3, ["pointed-space", "pointed-map", "pointed-homotopy", "pointed-set"]),
    "o012-rbt-l04-def-003": ("Definisi 4.3 (ruang bertitik)", "definition", "unit:o012-rbt-l04-s03", 1, ["pointed-space", "pointed-map", "pointed-homotopy", "pointed-set", "homotopy-class"]),
    "o012-rbt-l04-s04": ("Ruang penutup", "section", "unit:o012-rbt-l04", 4, ["covering-space", "covering-map", "fiber", "base-space", "evenly-covered-neighborhood", "wedge-sum"]),
    "o012-rbt-l04-exa-005": ("Contoh 4.5 (akar kuadrat pada bidang kompleks berlubang)", "example", "unit:o012-rbt-l04-s04", 1, ["covering-map", "quotient-map", "continuity"]),
    "o012-rbt-l04-def-004": ("Definisi 4.4 (ruang penutup)", "definition", "unit:o012-rbt-l04-s04", 2, ["covering-space", "covering-map", "fiber", "base-space", "evenly-covered-neighborhood", "discrete-topology", "homeomorphism"]),
    "o012-rbt-l04-ex-004": ("Latihan 4.4", "exercise", "unit:o012-rbt-l04-s04", 3, ["covering-composition", "covering-map"]),
    "o012-rbt-l04-prop-003": ("Proposisi 4.3 (serat di sepanjang lintasan)", "proposition", "unit:o012-rbt-l04-s04", 4, ["covering-map", "fiber", "path", "homeomorphism"]),
    "o012-rbt-l04-mastery": ("Pendamping penguasaan: solusi lengkap", "mastery_section", UNIT_ROOT_ID, 3, ["homotopy-category", "semilocally-path-connected-space", "covering-space"]),
    "o012-rbt-l04-sol-001": ("Solusi Latihan 4.1", "solution", "unit:o012-rbt-l04-mastery", 1, ["path-component", "functor", "homotopy-category", "homotopy-class"]),
    "o012-rbt-l04-check-001": ("Bukti Lema 4.1", "proof_check", "unit:o012-rbt-l04-mastery", 2, ["coproduct-preservation", "disjoint-union", "connected-component", "path-component"]),
    "o012-rbt-l04-sol-002": ("Solusi Latihan 4.2", "solution", "unit:o012-rbt-l04-mastery", 3, ["topologist-sine-curve", "path", "intermediate-value-theorem"]),
    "o012-rbt-l04-sol-003": ("Solusi Latihan 4.3", "solution", "unit:o012-rbt-l04-mastery", 4, ["semilocally-path-connected-space", "product-topology"]),
    "o012-rbt-l04-ans-001": ("Jawaban Pertanyaan 4.1", "answer", "unit:o012-rbt-l04-mastery", 5, ["semilocally-path-connected-space", "quotient-map", "final-topology"]),
    "o012-rbt-l04-sol-004": ("Solusi Latihan 4.4", "solution", "unit:o012-rbt-l04-mastery", 6, ["covering-composition", "covering-map", "evenly-covered-neighborhood"]),
}

if set(UNIT_META) != set(anchor_start):
    raise SystemExit(
        f"Unit 004 metadata/stable-id mismatch: missing={sorted(set(anchor_start)-set(UNIT_META))}, "
        f"extra={sorted(set(UNIT_META)-set(anchor_start))}"
    )


def concept_ids(slugs: list[str]) -> list[str]:
    return [f"concept:{slug}" for slug in slugs]


def is_original(local_id: str) -> bool:
    return any(token in local_id for token in ("-notice", "-mastery", "-sol-", "-check-", "-ans-"))


def path_for(local_id: str) -> list[str]:
    unit_id = f"unit:{local_id}"
    parent_id = UNIT_META[local_id][2]
    if parent_id == UNIT_ROOT_ID:
        return [UNIT_ROOT_ID, unit_id]
    parent_local_id = parent_id.removeprefix("unit:")
    return path_for(parent_local_id) + [unit_id]


units = load_jsonl("units.jsonl")
segments = load_jsonl("segments.jsonl")

root_locator = target_span(1, EXPECTED_SOURCE_LINES)
root = common("unit", UNIT_ROOT_ID)
root.update(
    {
        "concept_ids": concept_ids(["homotopy-category", "natural-transformation", "semilocally-path-connected-space", "pointed-space", "covering-space"]),
        "course_id": COURSE_ID,
        "display_title": "Topologi Aljabar — Unit 4: Invarian Homotopi, Transformasi Natural, dan Ruang Penutup",
        "edition_id": EDITION_ID,
        "locale": "id-ID",
        "order": 4,
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
    "line_end": 1131,
    "line_start": 878,
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
                {
                    "kind": "edition_original",
                    "path": SOURCE_RELATIVE,
                    "precision": "exact_target_span",
                }
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
    "base-space": ("ruang dasar", "o012-rbt-l04-s04", []),
    "coproduct-preservation": ("pelestarian koproduk", "o012-rbt-l04-lem-001", []),
    "covering-composition": ("komposisi pemetaan penutup", "o012-rbt-l04-ex-004", []),
    "covering-map": ("pemetaan penutup", "o012-rbt-l04-def-004", []),
    "evenly-covered-neighborhood": ("lingkungan yang tertutup secara merata", "o012-rbt-l04-def-004", ["lingkungan tertutup secara merata"]),
    "fiber": ("serat", "o012-rbt-l04-s04", []),
    "natural-isomorphism": ("isomorfisme natural", "o012-rbt-l04-def-001", []),
    "natural-transformation": ("transformasi natural", "o012-rbt-l04-def-001", []),
    "pointed-homotopy": ("homotopi bertitik", "o012-rbt-l04-def-003", []),
    "pointed-space": ("ruang bertitik", "o012-rbt-l04-def-003", []),
    "quotient-map": ("pemetaan hasil bagi", "o012-rbt-l04-exa-005", []),
    "semilocally-path-connected-space": ("ruang terhubung lintasan semilokal", "o012-rbt-l04-def-002", ["SLPC"]),
    "topologist-sine-curve": ("kurva sinus topolog", "o012-rbt-l04-exa-002", []),
    "wedge-sum": ("baji", "o012-rbt-l04-s04", ["jumlah baji"]),
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
        "attribution": "Original Indonesian mastery companion and edition notice for O012/D60 Unit 004.",
        "change_notice": "Newly authored material; not represented as source-author text.",
        "component_scope": ["unit:o012-rbt-l04-notice", "unit:o012-rbt-l04-mastery"],
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
        "attribution": "Composite Unit 004 reader: Roberts source adaptation plus independently authored Indonesian mastery companion; component provenance remains separated.",
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
        "attribution": "Cumulative Units 001-004 reader: David Michael Roberts source adaptations plus independently authored Indonesian mastery companions; component provenance remains separated.",
        "change_notice": "Cumulative staged boundary only; Unit 001 through Unit 004 component rights records remain controlling.",
        "component_scope": [f"unit:o012-rbt-u{number:03d}" for number in range(1, 5)],
        "license_expression": "CC-BY-4.0",
        "license_url": "https://creativecommons.org/licenses/by/4.0/",
        "non_endorsement": "Independent edition; no source-author endorsement.",
        "third_party_status": "Component-scoped rights records control.",
    }
)
rights[CUMULATIVE_RIGHTS] = cumulative

roberts = rights[ROBERTS_RIGHTS]
roberts["component_scope"] = [f"unit:o012-rbt-l{number:02d}" for number in range(1, 5)]
roberts["third_party_status"] = "No distinct third-party component is asserted within Units 001-004; the frozen archive remains authoritative for file-level review."
roberts["timestamp"] = TIMESTAMP


authority = load_jsonl("authority.jsonl")
for authority_id in (PROGRAM_ID, COURSE_ID):
    authority[authority_id]["rights_component_id"] = CUMULATIVE_RIGHTS
    authority[authority_id]["timestamp"] = TIMESTAMP
edition = authority[EDITION_ID]
edition["local_derivative_unit_ids"] = [f"unit:o012-rbt-u{number:03d}" for number in range(1, 5)]
edition["source_line_end"] = 1131
edition["timestamp"] = TIMESTAMP


assets = load_jsonl("assets.jsonl")
asset_id = "asset:o012-u004-source-markdown"
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


add_relation("relation:adapts:o012-rbt-u004:roberts-edition", UNIT_ROOT_ID, "adapts", EDITION_ID, "Unit 004 adapts Notes.tex lines 878-1131 and adds an original solved mastery companion.")
add_relation("relation:precedes:l04:mastery", "unit:o012-rbt-l04", "precedes", "unit:o012-rbt-l04-mastery", "The translated lecture precedes its original solved mastery companion.")
add_relation("relation:precedes:u003:u004", "unit:o012-rbt-u003", "precedes", UNIT_ROOT_ID, "Cumulative reader order.")
add_relation("relation:proves:l04-proof-001:l04-prop-001", "unit:o012-rbt-l04-proof-001", "proves", "unit:o012-rbt-l04-prop-001", "Proof that π₀ descends to the homotopy category.")
add_relation("relation:proves:l04-proof-002:l04-prop-002", "unit:o012-rbt-l04-proof-002", "proves", "unit:o012-rbt-l04-prop-002", "Global proof that path and connected components coincide in an SLPC space.")
add_relation("relation:proves:l04-check-001:l04-lem-001", "unit:o012-rbt-l04-check-001", "proves", "unit:o012-rbt-l04-lem-001", "The original companion supplies the source-omitted proof of coproduct preservation.")
for number in range(1, 5):
    add_relation(
        f"relation:solves:l04-sol-{number:03d}:l04-ex-{number:03d}",
        f"unit:o012-rbt-l04-sol-{number:03d}",
        "solves",
        f"unit:o012-rbt-l04-ex-{number:03d}",
        f"Complete solution to Exercise 4.{number}.",
    )
add_relation("relation:answers:l04-ans-001:l04-q-001", "unit:o012-rbt-l04-ans-001", "answers", "unit:o012-rbt-l04-q-001", "Complete answer to Question 4.1.")


CORRECTION_META = {
    "O012-ADV-0035": ("clarification", "o012-rbt-l04-proof-001", "homotopy-component-argument"),
    "O012-ADV-0036": ("mathematical_correction", "o012-rbt-l04-lem-001", "coproduct-map-direction"),
    "O012-ADV-0037": ("mathematical_correction", "o012-rbt-l04-exa-002", "topologist-sine-formula"),
    "O012-ADV-0038": ("structural_adaptation", "o012-rbt-l04-ex-002", "no-path-margin-reflow"),
    "O012-ADV-0039": ("mathematical_correction", "o012-rbt-l04-def-001", "naturality-square-target"),
    "O012-ADV-0040": ("mathematical_correction", "o012-rbt-l04-def-001", "natural-transformation-codomain"),
    "O012-ADV-0041": ("mathematical_correction", "o012-rbt-l04-def-002", "slpc-characterization"),
    "O012-ADV-0042": ("mathematical_correction", "o012-rbt-l04-proof-002", "slpc-global-proof"),
    "O012-ADV-0043": ("mathematical_correction", "o012-rbt-l04-proof-002", "chi-preimage-notation"),
    "O012-ADV-0044": ("clarification", "o012-rbt-l04-proof-002", "slpc-basis-path-location"),
    "O012-ADV-0045": ("clarification", "o012-rbt-l04-exa-004", "manifold-coordinate-ball"),
    "O012-ADV-0046": ("mathematical_correction", "o012-rbt-l04-def-003", "pointed-map-definition"),
    "O012-ADV-0047": ("clarification", "o012-rbt-l04-def-003", "pointed-homotopy-endpoints"),
    "O012-ADV-0048": ("clarification", "o012-rbt-l04-exa-005", "square-map-quotient-continuity"),
    "O012-ADV-0049": ("mathematical_correction", "o012-rbt-l04-def-004", "covering-local-homeomorphism"),
    "O012-ADV-0050": ("clarification", "o012-rbt-l04-s04", "power-map-range"),
    "O012-ADV-0051": ("mathematical_correction", "o012-rbt-l04-s04", "figure-eight-wedge"),
    "O012-ADV-0052": ("clarification", "o012-rbt-l04-prop-003", "fiber-bijection-choice"),
    "O012-ADV-0053": ("clarification", "o012-rbt-l04-def-004", "covering-open-neighborhood"),
}

with LEDGER_PATH.open("r", encoding="utf-8", newline="") as stream:
    ledger_rows = {row["event_id"]: row for row in csv.DictReader(stream) if row["event_id"] in CORRECTION_META}
if set(ledger_rows) != set(CORRECTION_META):
    raise SystemExit(f"Unit 004 adverse ledger mismatch: {sorted(set(CORRECTION_META)-set(ledger_rows))}")

corrections = load_jsonl("corrections.jsonl")
for event_id, (correction_type, affected_local_id, slug) in CORRECTION_META.items():
    row = ledger_rows[event_id]
    start, end = SPANS[affected_local_id]
    record_id = f"correction:o012-u004-adv-{event_id[-4:]}-{slug}"
    record = common("correction", record_id)
    record.update(
        {
            "adverse_ledger_id": event_id,
            "affected_unit_ids": [f"unit:{affected_local_id}"],
            "correction_type": correction_type,
            "edition_id": EDITION_ID,
            "evidence": f"{row['source_location']}; target lines {start}-{end}.",
            "evidence_segment_id": "segment:o012-rbt-l04-notice",
            "rationale": row["rationale"],
            "resource_id": RESOURCE_ID,
            "source_defect": row["observed"],
            "target_change": row["action"],
            "unit_id": UNIT_ROOT_ID,
            "upstream_report_disposition": "not_contacted",
        }
    )
    corrections[record_id] = record


QA_SOURCE = "qa:o012-u004-source-integrity"
QA_MATH = "qa:o012-u004-math-review"
QA_LANGUAGE = "qa:o012-u004-language-review"
QA_BUILD = "qa:o012-units-001-004-build"
QA_ACCESSIBILITY = "qa:o012-units-001-004-accessibility"
QA_VISUAL = "qa:o012-units-001-004-visual"
ARTIFACT_MANIFEST_ID = "artifact:o012-units-001-004-manifest"

ARTIFACT_META = {
    "artifact:o012-u004-independent-review": {
        "bytes": 3031,
        "manifest_artifact_id": None,
        "media_type": "text/markdown; charset=utf-8",
        "path": "qa/UNIT_004_INDEPENDENT_REVIEW.md",
        "qa_event_ids": [QA_LANGUAGE, QA_MATH, QA_SOURCE],
        "sha256": "ac993a10e22738197775ae5c3f4e72948983c4e99ff602a52943b40ed417b6f9",
        "toolchain": "Independent read-only exact-span, mathematical, Indonesian-language, and structural final review.",
        "translation_state": "mathematically_reviewed",
    },
    "artifact:o012-units-001-004-html": {
        "bytes": 494732,
        "manifest_artifact_id": ARTIFACT_MANIFEST_ID,
        "media_type": "text/html; charset=utf-8",
        "path": "output/html/units-001-004/index.html",
        "qa_event_ids": [QA_ACCESSIBILITY, QA_BUILD, QA_VISUAL],
        "sha256": "8c8f5e1ad8172a2d97e3931fc3b4f2a3aa7f9e8a709260a27103f7eca0f1357d",
        "toolchain": "Pandoc 3.9.0.2 standalone HTML5 with embedded CSS and native MathML.",
        "translation_state": "built",
    },
    ARTIFACT_MANIFEST_ID: {
        "bytes": 247,
        "manifest_artifact_id": None,
        "media_type": "text/csv; charset=utf-8",
        "path": "output/ARTIFACT_MANIFEST_UNITS_001_004.csv",
        "qa_event_ids": [QA_BUILD],
        "sha256": "4c8bf407e426feb8db92308c4b28bdbbc0738416a85a13539ef7915e4c1aad83",
        "toolchain": "Cumulative Units 001-004 deterministic artifact manifest.",
        "translation_state": "built",
    },
    "artifact:o012-units-001-004-pdf": {
        "bytes": 539006,
        "manifest_artifact_id": ARTIFACT_MANIFEST_ID,
        "media_type": "application/pdf",
        "path": "output/pdf/topologi-aljabar-unit-001-004-id.pdf",
        "qa_event_ids": [QA_ACCESSIBILITY, QA_BUILD, QA_VISUAL],
        "sha256": "5e92c4c6ed60bca9f2f4d362d4c48b4f01aa156b330e2adacd1bf88dd7de9e87",
        "toolchain": "Pandoc 3.9.0.2 with pdflatex; two fixed-epoch builds were byte-identical.",
        "translation_state": "built",
    },
    "artifact:o012-units-001-004-qa-receipt": {
        "bytes": 4478,
        "manifest_artifact_id": None,
        "media_type": "application/json",
        "path": "qa/UNITS_001_004_QA.json",
        "qa_event_ids": [QA_LANGUAGE, QA_MATH, QA_SOURCE, QA_ACCESSIBILITY, QA_BUILD, QA_VISUAL],
        "sha256": "1670bbe2377712c9f96b9a68cdb75589ae461512f77cea7ad0c9290193724bd5",
        "toolchain": "Unit 004 independent review, cumulative structural QA, Poppler PDF checks, and manual browser/PDF review.",
        "translation_state": "built",
    },
    "artifact:o012-units-001-004-qa-text": {
        "bytes": 100684,
        "manifest_artifact_id": None,
        "media_type": "text/plain; charset=utf-8",
        "path": "qa/units-001-004-extracted.txt",
        "qa_event_ids": [QA_MATH, QA_BUILD],
        "sha256": "3d27bc1ab5a780bffce12d5951623b60929069238a210961740234502e71bf35",
        "toolchain": "Poppler pdftotext with layout preservation and UTF-8 output.",
        "translation_state": "built",
    },
    "artifact:o012-units-001-004-visual-receipt": {
        "bytes": 2257,
        "manifest_artifact_id": None,
        "media_type": "text/markdown; charset=utf-8",
        "path": "qa/UNITS_001_004_VISUAL_QA.md",
        "qa_event_ids": [QA_ACCESSIBILITY, QA_VISUAL],
        "sha256": "74e609e94ea47b89db223c21e12cae682048f0a60d8780dae96d5b0164f2c5ca",
        "toolchain": "Poppler all-page PDF rendering plus Codex in-app Chromium desktop/mobile responsive inspection.",
        "translation_state": "visually_checked",
    },
}

artifacts = load_jsonl("artifacts.jsonl")
for artifact_id, metadata in ARTIFACT_META.items():
    artifact_path = LANE_ROOT / metadata["path"]
    if not artifact_path.is_file():
        raise SystemExit(f"missing final Unit 001-004 artifact: {metadata['path']}")
    raw = artifact_path.read_bytes()
    if len(raw) != metadata["bytes"] or sha256(raw) != metadata["sha256"]:
        raise SystemExit(f"final Unit 001-004 artifact identity mismatch: {metadata['path']}")
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
        "note": "The cumulative validator binds Roberts Notes.tex lines 878-1131 to all 33 Unit 4 stable IDs, preserves 142 stable IDs across Units 001-004, and verifies the one-to-one O012-ADV-0035 through O012-ADV-0053 correction/reflow inventory.",
        "witness_artifact_ids": [
            "artifact:o012-u004-independent-review",
            "artifact:o012-units-001-004-qa-receipt",
        ],
    },
    QA_MATH: {
        "qa_type": "math",
        "note": "Independent exact-span mathematical replay passed after eighteen disclosed source corrections and one accessibility reflow; all four exercises, the formal question, and the source-omitted lemma proof have complete checked companions, with P1, P2, and P3 all zero.",
        "witness_artifact_ids": [
            "artifact:o012-u004-independent-review",
            "artifact:o012-units-001-004-qa-receipt",
            "artifact:o012-units-001-004-qa-text",
        ],
    },
    QA_LANGUAGE: {
        "qa_type": "language",
        "note": "Independent final Indonesian-language replay found no P1, P2, or P3 issue and no active English prose outside protected names, notation, URLs, and markup.",
        "witness_artifact_ids": ["artifact:o012-u004-independent-review"],
    },
    QA_BUILD: {
        "qa_type": "build",
        "note": "Two fixed-epoch cumulative PDF builds were byte-identical; HTML, PDF, manifest, extracted-text witness, and QA receipt are hash-consistent while all earlier release artifacts remain unchanged.",
        "witness_artifact_ids": [
            "artifact:o012-units-001-004-html",
            ARTIFACT_MANIFEST_ID,
            "artifact:o012-units-001-004-pdf",
            "artifact:o012-units-001-004-qa-receipt",
            "artifact:o012-units-001-004-qa-text",
        ],
    },
    QA_ACCESSIBILITY: {
        "qa_type": "accessibility",
        "note": "Semantic HTML passed with lang=id-ID, 1384 native MathML nodes, 198 unique HTML IDs, all 54 local fragment links resolving, no scripts or external runtime dependency, desktop centering, mobile reflow, and formula-local horizontal scrolling. PDF remains explicitly secondary and untagged.",
        "witness_artifact_ids": [
            "artifact:o012-units-001-004-html",
            "artifact:o012-units-001-004-qa-receipt",
            "artifact:o012-units-001-004-visual-receipt",
        ],
    },
    QA_VISUAL: {
        "qa_type": "visual",
        "note": "All 35 PDF pages and the cumulative HTML title, contents, Unit 4, and mastery surfaces at 1280x720 and 390x844 were inspected; no clipping, overlap, page overflow, broken formula, missing glyph, blank object, or orphan page remained.",
        "witness_artifact_ids": [
            "artifact:o012-units-001-004-html",
            "artifact:o012-units-001-004-pdf",
            "artifact:o012-units-001-004-visual-receipt",
        ],
    },
}

qa_events = load_jsonl("qa.jsonl")
for qa_id, metadata in QA_META.items():
    record = common("qa_event", qa_id)
    record.update({**metadata, "result": "passed", "unit_id": UNIT_ROOT_ID})
    qa_events[qa_id] = record


for filename, records in (
    ("artifacts.jsonl", artifacts),
    ("assets.jsonl", assets),
    ("authority.jsonl", authority),
    ("concepts.jsonl", concepts),
    ("corrections.jsonl", corrections),
    ("qa.jsonl", qa_events),
    ("relations.jsonl", relations),
    ("rights.jsonl", rights),
    ("segments.jsonl", segments),
    ("terms.jsonl", terms),
    ("units.jsonl", units),
):
    write_jsonl(filename, records)

print("Unit 004 backend extension written")
print(f"stable_ids: {len(anchor_start)}")
print(f"source_sha256: {EXPECTED_SOURCE_SHA256}")
print(f"adverse_ledger_records: {len(CORRECTION_META)}")
