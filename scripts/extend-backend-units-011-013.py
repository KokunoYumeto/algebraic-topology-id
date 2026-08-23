#!/usr/bin/env python3
"""Deterministically extend the O012/D60 backend through Units 011-013."""

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
TIMESTAMP = "2026-08-22T22:30:00Z"
PROGRAM_ID = "program:o012-id"
COURSE_ID = "course:o012-d60"
RESOURCE_ID = "resource:roberts-algebraic-topology-2019"
EDITION_ID = "edition:roberts-at-2019-b947ad2"
ROBERTS_RIGHTS = "rights:roberts-cc-by-4.0"
UPSTREAM_COMMIT = "b947ad2e9f9e301bfe24590a9db653bc54fa1a53"
CUMULATIVE_RIGHTS = "rights:o012-units-001-013-composite-cc-by-4.0"
JSONL_NAMES = (
    "artifacts.jsonl", "assets.jsonl", "authority.jsonl", "concepts.jsonl",
    "corrections.jsonl", "qa.jsonl", "relations.jsonl", "rights.jsonl",
    "segments.jsonl", "terms.jsonl", "units.jsonl",
)

SOURCE_SPECS = {
    11: {
        "relative": "source/id-ID/units/unit-011-lecture-011.md", "bytes": 28465,
        "lines": 959, "sha256": "1cdbe0cae239a4e60a72f25c8814c2e3b5ec26b9119da03624bda7f3ff1ae127",
        "upstream_start": 2273, "upstream_end": 2494, "expected_ids": 39,
        "root_concepts": ["free-product", "pushout", "fundamental-groupoid", "seifert-van-kampen-theorem"],
        "title": "Topologi Aljabar - Unit 11: Produk Bebas, Pushout, dan Teorema Seifert-van Kampen",
    },
    12: {
        "relative": "source/id-ID/units/unit-012-lecture-012.md", "bytes": 32850,
        "lines": 1024, "sha256": "429831df4a5600c59351516915fb787cd73402d8c11c411869210dbf8aaa7ada",
        "upstream_start": 2495, "upstream_end": 2726, "expected_ids": 37,
        "root_concepts": ["retract", "commutative-square", "relative-seifert-van-kampen-theorem", "trivial-group"],
        "title": "Topologi Aljabar - Unit 12: Penutupan Seifert-van Kampen, Retrak, dan Versi Grup",
    },
    13: {
        "relative": "source/id-ID/units/unit-013-lecture-013.md", "bytes": 41196,
        "lines": 1306, "sha256": "0aa68cb4ed31862d32aeff5a7106b4ac29c13cbc202f7dbc8381fc7cd31418c0",
        "upstream_start": 2727, "upstream_end": 3046, "expected_ids": 44,
        "root_concepts": ["free-product-with-amalgamation", "groupoid-congruence", "cyclic-group", "wedge-sum", "group-presentation", "surface-group"],
        "title": "Topologi Aljabar - Unit 13: Amalgamasi, Pushout Grupoid, Baji, dan Kompleks Presentasi",
    },
}

# terminology-control id -> (locale-neutral slug, exact evidence segment)
TERM_SPECS = {
    "O012-TERM-0172": ("group-presentation", "o012-rbt-l11-s01"),
    "O012-TERM-0173": ("relation", "o012-rbt-l11-s01"),
    "O012-TERM-0174": ("free-reduction", "o012-rbt-l11-s01"),
    "O012-TERM-0175": ("free-product-with-amalgamation", "o012-rbt-l11-s01"),
    "O012-TERM-0176": ("universal-property", "o012-rbt-l11-def-002"),
    "O012-TERM-0177": ("pushout", "o012-rbt-l11-def-003"),
    "O012-TERM-0178": ("pushout-square", "o012-rbt-l11-def-003"),
    "O012-TERM-0179": ("cover-by-neighbourhoods", "o012-rbt-l11-thm-001"),
    "O012-TERM-0180": ("commutative-square", "o012-rbt-l11-def-003"),
    "O012-TERM-0181": ("canonical-map", "o012-rbt-l11-fig-007"),
    "O012-TERM-0182": ("path-subdivision", "o012-rbt-l11-proof-subdivision"),
    "O012-TERM-0183": ("refinement", "o012-rbt-l11-proof-subdivision"),
    "O012-TERM-0184": ("lebesgue-covering-lemma", "o012-rbt-l11-proof-subdivision"),
    "O012-TERM-0185": ("seifert-van-kampen-theorem", "o012-rbt-l11-thm-001"),
    "O012-TERM-0186": ("retract", "o012-rbt-l12-def-001"),
    "O012-TERM-0187": ("category-of-commutative-squares", "o012-rbt-l12-s02"),
    "O012-TERM-0188": ("commutative-cube", "o012-rbt-l12-s02"),
    "O012-TERM-0189": ("relative-seifert-van-kampen-theorem", "o012-rbt-l12-thm-001"),
    "O012-TERM-0190": ("orthogonal-projection", "o012-rbt-l12-def-001"),
    "O012-TERM-0191": ("stereographic-projection", "o012-rbt-l12-exa-002"),
    "O012-TERM-0192": ("antipodal-points", "o012-rbt-l12-exa-002"),
    "O012-TERM-0193": ("trivial-group", "o012-rbt-l12-exa-002"),
    "O012-TERM-0194": ("algebraic-order-of-composition", "o012-rbt-l12-notice"),
    "O012-TERM-0195": ("normal-subgroup", "o012-rbt-l13-def-001"),
    "O012-TERM-0196": ("normal-closure", "o012-rbt-l13-def-001"),
    "O012-TERM-0197": ("finitely-generated-group", "o012-rbt-l13-exa-001"),
    "O012-TERM-0198": ("finitely-presented-group", "o012-rbt-l13-exa-002"),
    "O012-TERM-0199": ("one-relator-group", "o012-rbt-l13-exa-001"),
    "O012-TERM-0200": ("surface-group", "o012-rbt-l13-exa-002"),
    "O012-TERM-0201": ("modular-group", "o012-rbt-l13-rem-001"),
    "O012-TERM-0202": ("fractional-linear-transformation", "o012-rbt-l13-rem-001"),
    "O012-TERM-0203": ("orbifold-quotient", "o012-rbt-l13-rem-001"),
    "O012-TERM-0204": ("directed-graph", "o012-rbt-l13-s02"),
    "O012-TERM-0205": ("node", "o012-rbt-l13-s02"),
    "O012-TERM-0206": ("edge", "o012-rbt-l13-s02"),
    "O012-TERM-0207": ("groupoid-congruence", "o012-rbt-l13-s02"),
}

CORRECTION_TARGETS = {
    "O012-ADV-0143": ["o012-rbt-l11-s01"],
    "O012-ADV-0144": ["o012-rbt-l11-def-002"],
    "O012-ADV-0145": ["o012-rbt-l11-s01"],
    "O012-ADV-0146": [f"o012-rbt-l11-fig-{n:03d}" for n in range(1, 10)],
    "O012-ADV-0147": ["o012-rbt-l11-s01", "o012-rbt-l11-s02", "o012-rbt-l11-s03", "o012-rbt-l11-s04"],
    "O012-ADV-0148": ["o012-rbt-l11-exa-005"],
    "O012-ADV-0149": ["o012-rbt-l11-proof-local-paths"],
    "O012-ADV-0150": ["o012-rbt-l11-proof-001", "o012-rbt-l11-proof-subdivision"],
    "O012-ADV-0151": ["o012-rbt-l11-proof-subdivision"],
    "O012-ADV-0152": ["o012-rbt-l11-proof-subdivision"],
    "O012-ADV-0153": ["o012-rbt-l11-fig-010", "o012-rbt-l11-fig-011"],
    "O012-ADV-0154": ["o012-rbt-l11-proof-001"],
    "O012-ADV-0155": ["o012-rbt-l11-s02", "o012-rbt-l11-s03"],
    "O012-ADV-0156": ["o012-rbt-l12-notice", "o012-rbt-l12-proof-001"],
    "O012-ADV-0157": ["o012-rbt-l12-proof-001", "o012-rbt-l12-proof-descent"],
    "O012-ADV-0158": ["o012-rbt-l12-fig-001"],
    "O012-ADV-0159": ["o012-rbt-l12-notice"],
    "O012-ADV-0160": [f"o012-rbt-l12-fig-{n:03d}" for n in range(2, 7)],
    "O012-ADV-0161": ["o012-rbt-l12-s01", "o012-rbt-l12-s02", "o012-rbt-l12-s03"],
    "O012-ADV-0162": ["o012-rbt-l12-proof-003"],
    "O012-ADV-0163": ["o012-rbt-l12-s02", "o012-rbt-l12-fig-002"],
    "O012-ADV-0164": ["o012-rbt-l12-lem-001", "o012-rbt-l12-proof-002"],
    "O012-ADV-0165": ["o012-rbt-l12-proof-003"],
    "O012-ADV-0166": ["o012-rbt-l12-proof-003"],
    "O012-ADV-0167": ["o012-rbt-l12-proof-004"],
    "O012-ADV-0168": ["o012-rbt-l12-s03", "o012-rbt-l12-proof-005"],
    "O012-ADV-0169": ["o012-rbt-l13-s01"],
    "O012-ADV-0170": ["o012-rbt-l13-rem-001"],
    "O012-ADV-0171": ["o012-rbt-l13-rem-001"],
    "O012-ADV-0172": ["o012-rbt-l13-s02"],
    "O012-ADV-0173": ["o012-rbt-l13-fig-005"],
    "O012-ADV-0174": ["o012-rbt-l13-fig-005"],
    "O012-ADV-0175": ["o012-rbt-l13-s02", "o012-rbt-l13-exa-002"],
    "O012-ADV-0176": ["o012-rbt-l13-s03", "o012-rbt-l13-s04"],
    "O012-ADV-0177": ["o012-rbt-l13-fig-006", "o012-rbt-l13-fig-007", "o012-rbt-l13-fig-008"],
    "O012-ADV-0178": ["o012-rbt-l13-exa-003"],
    "O012-ADV-0179": ["o012-rbt-l13-s04", "o012-rbt-l13-s05"],
    "O012-ADV-0180": ["o012-rbt-l13-s04"],
    "O012-ADV-0181": ["o012-rbt-l13-s03", "o012-rbt-l13-s04"],
    "O012-ADV-0182": ["o012-rbt-l13-s05"],
    "O012-ADV-0183": ["o012-rbt-l13-s05", "o012-rbt-l13-mcheck-006"],
    "O012-ADV-0184": ["o012-rbt-l13-s05"],
    "O012-ADV-0185": ["o012-rbt-l13-fig-013"],
    "O012-ADV-0186": [f"o012-rbt-l13-fig-{n:03d}" for n in range(1, 14)],
    "O012-ADV-0187": ["o012-rbt-l13-s01", "o012-rbt-l13-s02", "o012-rbt-l13-s03", "o012-rbt-l13-s04", "o012-rbt-l13-s05"],
}

ARTIFACT_META = {
    "artifact:o012-u011-independent-review": ("qa/UNIT_011_INDEPENDENT_REVIEW.md", 3351, "de0766d41ba901405881d8078830d74420f2b1012ef24ace8d3f481135cd5b25", "text/markdown; charset=utf-8", "unit:o012-rbt-u011", "mathematically_reviewed"),
    "artifact:o012-u012-independent-review": ("qa/UNIT_012_INDEPENDENT_REVIEW.md", 3374, "6ea34c30edfa208cc7e37a17f43ef4bf62b21ff4db222e534c97e027232e0ce7", "text/markdown; charset=utf-8", "unit:o012-rbt-u012", "mathematically_reviewed"),
    "artifact:o012-u013-independent-review": ("qa/UNIT_013_INDEPENDENT_REVIEW.md", 6665, "5903c7da7f57d5db15a2d94807860a816d15e7d3cb7b020a8a3ddcbb0df45c21", "text/markdown; charset=utf-8", "unit:o012-rbt-u013", "mathematically_reviewed"),
    "artifact:o012-units-001-013-html": ("output/html/units-001-013/index.html", 1824804, "be1473ab5cb8eff26341e554179661775a12cec5784a8ebf3f9c2f3f0633cb71", "text/html; charset=utf-8", "unit:o012-rbt-u013", "built"),
    "artifact:o012-units-001-013-manifest": ("output/ARTIFACT_MANIFEST_UNITS_001_013.csv", 249, "6b55446a4f0a951329c29ec33b0ca586c749b9301dd4bd8ad4dd94f1c91d74de", "text/csv; charset=utf-8", "unit:o012-rbt-u013", "built"),
    "artifact:o012-units-001-013-pdf": ("output/pdf/topologi-aljabar-unit-001-013-id.pdf", 1071382, "14775535f773735db5886195980f39e417aaea24998927956a81b55b0ef77c68", "application/pdf", "unit:o012-rbt-u013", "built"),
    "artifact:o012-units-001-013-qa-receipt": ("qa/UNITS_001_013_QA.json", 9069, "cb2413e8131743457a0685a57cf519c769e5593e9ec8d904f6160f9e0519983d", "application/json", "unit:o012-rbt-u013", "built"),
    "artifact:o012-units-001-013-qa-text": ("qa/units-001-013-extracted.txt", 395766, "d94869df978e2538c79b8859cb38c8cbf859420cde68326a35546c973c787497", "text/plain; charset=utf-8", "unit:o012-rbt-u013", "built"),
    "artifact:o012-units-001-013-visual-receipt": ("qa/UNITS_001_013_VISUAL_QA.md", 2139, "78e151b05d3efdce4dbfd346962dece5d7da4a559ab1101ac4bd8e02bff59f48", "text/markdown; charset=utf-8", "unit:o012-rbt-u013", "visually_checked"),
    "artifact:o012-units-001-013-render-inventory": ("qa/UNITS_001_013_RENDER_INVENTORY.csv", 16336, "71168ca32a0be0828c5d8b0b94328410c1f842913d4aab0ad833b4315bffd4ef", "text/csv; charset=utf-8", "unit:o012-rbt-u013", "visually_checked"),
}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def common(entity_type: str, record_id: str) -> dict[str, Any]:
    return {"entity_type": entity_type, "id": record_id, "schema": SCHEMA, "schema_version": SCHEMA_VERSION, "status": "active", "supersedes": None, "timestamp": TIMESTAMP, "workflow": WORKFLOW}


def canonical(record: dict[str, Any]) -> str:
    return json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def canonical_jsonl(records: dict[str, dict[str, Any]]) -> bytes:
    return "".join(canonical(records[key]) + "\n" for key in sorted(records)).encode("utf-8")


def load_jsonl(name: str) -> tuple[dict[str, dict[str, Any]], dict[str, str]]:
    records: dict[str, dict[str, Any]] = {}
    lines: dict[str, str] = {}
    for line in (BACKEND / name).read_text(encoding="utf-8").splitlines():
        record = json.loads(line)
        if record["id"] in records:
            raise SystemExit(f"duplicate existing backend id: {record['id']}")
        records[record["id"]] = record
        lines[record["id"]] = line
    return records, lines


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
allowed_modified_existing = {PROGRAM_ID, COURSE_ID, EDITION_ID, ROBERTS_RIGHTS, "term:universal-property:id-ID"}
owned_new_ids: set[str] = set()
unit_context: dict[int, dict[str, Any]] = {}
term_slugs_by_evidence: defaultdict[str, list[str]] = defaultdict(list)
for _, (slug, evidence) in TERM_SPECS.items():
    term_slugs_by_evidence[evidence].append(slug)


def concept_ids(slugs: list[str]) -> list[str]:
    return [f"concept:{slug}" for slug in dict.fromkeys(slugs)]


def infer_kind(local_id: str) -> str:
    if local_id.endswith("-notice"):
        return "notice"
    if re.fullmatch(r"o012-rbt-l\d{2}", local_id):
        return "lecture"
    if re.search(r"-s\d{2}$", local_id):
        return "section"
    if local_id.endswith("-mastery"):
        return "mastery_section"
    if "-mcheck-" in local_id or "-ex-" in local_id:
        return "exercise"
    if "-sol-" in local_id:
        return "solution"
    for token, kind in {
        "-exa-": "example", "-lem-": "lemma", "-def-": "definition", "-thm-": "theorem",
        "-proof-": "proof", "-rem-": "remark", "-prop-": "proposition", "-cor-": "corollary",
        "-fig-": "figure", "-fact-": "fact", "-boundary": "boundary",
    }.items():
        if token in local_id:
            return kind
    raise SystemExit(f"cannot infer unit kind: {local_id}")


def is_original(local_id: str, opening: str = "") -> bool:
    return 'data-origin="edition-original"' in opening or any(token in local_id for token in ("-notice", "-mastery", "-mcheck-", "-sol-", "-boundary"))


for lecture, spec in SOURCE_SPECS.items():
    source_path = LANE / spec["relative"]
    raw = source_path.read_bytes()
    if len(raw) != spec["bytes"] or digest(raw) != spec["sha256"]:
        raise SystemExit(f"Unit {lecture:03d} source identity mismatch")
    raw_lines = raw.splitlines(keepends=True)
    if len(raw_lines) != spec["lines"]:
        raise SystemExit(f"Unit {lecture:03d} line-count mismatch")
    text_lines = [line.decode("utf-8").rstrip("\r\n") for line in raw_lines]
    id_re = re.compile(rf"\{{[^}}\n]*#(o012-rbt-l{lecture:02d}(?:-[a-z0-9]+)*)[^}}\n]*\}}")
    anchor_start: dict[str, int] = {}
    aliases: dict[str, list[str]] = {}
    for number, text in enumerate(text_lines, start=1):
        found = id_re.findall(text)
        if len(found) > 1:
            raise SystemExit(f"multiple stable IDs on Unit {lecture} line {number}")
        if found:
            if found[0] in anchor_start:
                raise SystemExit(f"duplicate stable ID: {found[0]}")
            anchor_start[found[0]] = number
            alias = re.search(r'data-source-label="([^"]+)"', text)
            if alias:
                aliases[found[0]] = [alias.group(1)]
    if len(anchor_start) != spec["expected_ids"]:
        raise SystemExit(f"Unit {lecture} stable-ID mismatch: {len(anchor_start)}")

    heading_re = re.compile(r"^(#{1,6})\s+(.+?)\s+\{")

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
            while end > start and not text_lines[end - 1].strip():
                end -= 1
            return start, end
        if opening.startswith(":::"):
            for candidate in range(start + 1, len(text_lines) + 1):
                if text_lines[candidate - 1].strip() == ":::":
                    return start, candidate
        raise SystemExit(f"cannot derive span for {local_id}")

    spans = {local_id: derive_span(local_id) for local_id in anchor_start}

    def locator(start: int, end: int) -> dict[str, Any]:
        return {"content_sha256": digest(b"".join(raw_lines[start - 1:end])), "file_sha256": spec["sha256"], "line_end": end, "line_start": start, "path": spec["relative"]}

    root_id = f"unit:o012-rbt-u{lecture:03d}"
    companion_rights = f"rights:o012-u{lecture:03d}-companion-cc-by-4.0"
    composite_rights = f"rights:o012-u{lecture:03d}-composite-cc-by-4.0"
    root = common("unit", root_id)
    root.update({"concept_ids": concept_ids(spec["root_concepts"]), "course_id": COURSE_ID, "display_title": spec["title"], "edition_id": EDITION_ID, "locale": "id-ID", "order": lecture, "parent_id": COURSE_ID, "path": [root_id], "program_id": PROGRAM_ID, "provenance_relation": "composite_translated_and_original", "resource_id": RESOURCE_ID, "rights_component_id": composite_rights, "source_local_id": None, "target_locator": locator(1, spec["lines"]), "translation_state": "structurally_verified", "unit_kind": "reader_unit"})
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
            order = {"notice": 1, "lecture": 2, "mastery_section": 3}[kind]
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
        opening = text_lines[anchor_start[local_id] - 1]
        heading = heading_re.match(opening)
        if heading:
            display = re.sub(r"\s+\{.*$", "", heading.group(2)).strip()
        else:
            display = local_id
            for candidate in text_lines[anchor_start[local_id]:spans[local_id][1]]:
                match = re.match(r"^\*\*(.+?)\*\*", candidate)
                if match:
                    display = match.group(1).strip()
                    break
        slugs = list(spec["root_concepts"]) + term_slugs_by_evidence.get(local_id, [])
        metadata[local_id] = {"display": display, "kind": kind, "parent": parent, "order": order, "concept_slugs": list(dict.fromkeys(slugs))}

    def unit_path(local_id: str) -> list[str]:
        unit_id = f"unit:{local_id}"
        parent = metadata[local_id]["parent"]
        if parent == root_id:
            return [root_id, unit_id]
        return unit_path(parent.removeprefix("unit:")) + [unit_id]

    upstream_locator = {"commit_sha": UPSTREAM_COMMIT, "line_end": spec["upstream_end"], "line_start": spec["upstream_start"], "path": "Notes.tex", "precision": "unit_range_only"}
    original_ids: list[str] = []
    for local_id in ordered:
        item = metadata[local_id]
        start, end = spans[local_id]
        opening = text_lines[start - 1]
        original = is_original(local_id, opening)
        provenance = "edition_original" if original else "translated_adapted_from_upstream"
        component_rights = companion_rights if original else ROBERTS_RIGHTS
        extra = {"source_aliases": aliases[local_id]} if local_id in aliases else {}
        unit_id = f"unit:{local_id}"
        unit = common("unit", unit_id)
        unit.update({"concept_ids": concept_ids(item["concept_slugs"]), "course_id": COURSE_ID, "display_title": item["display"], "edition_id": EDITION_ID, "locale": "id-ID", "order": item["order"], "parent_id": item["parent"], "path": unit_path(local_id), "program_id": PROGRAM_ID, "provenance_relation": provenance, "resource_id": RESOURCE_ID, "rights_component_id": component_rights, "source_local_id": local_id, "target_locator": locator(start, end), "translation_state": "structurally_verified", "unit_kind": item["kind"], **extra})
        units[unit_id] = unit
        owned_new_ids.add(unit_id)
        segment_id = f"segment:{local_id}"
        segment = common("segment", segment_id)
        segment.update({"concept_ids": concept_ids(item["concept_slugs"]), "edition_id": EDITION_ID, "locale": "id-ID", "order": item["order"], "provenance_relation": provenance, "resource_id": RESOURCE_ID, "rights_component_id": component_rights, "segment_kind": item["kind"], "source_local_id": local_id, "source_locator": ({"kind": "edition_original", "path": spec["relative"], "precision": "exact_target_span"} if original else dict(upstream_locator)), "target_locator": locator(start, end), "translation_state": "structurally_verified", "unit_id": unit_id, **extra})
        segments[segment_id] = segment
        owned_new_ids.add(segment_id)
        if original:
            original_ids.append(unit_id)

    companion = common("rights", companion_rights)
    companion.update({"attribution": f"Original Indonesian mastery companion, edition notice, and source-boundary notes for O012/D60 Unit {lecture:03d}.", "change_notice": "Newly authored material; not represented as source-author text.", "component_scope": original_ids, "license_expression": "CC-BY-4.0", "license_url": "https://creativecommons.org/licenses/by/4.0/", "non_endorsement": "No endorsement by David Michael Roberts or affiliated institutions is implied.", "third_party_status": "No external media component."})
    rights[companion_rights] = companion
    owned_new_ids.add(companion_rights)
    composite = common("rights", composite_rights)
    composite.update({"attribution": f"Composite Unit {lecture:03d} reader: Roberts source adaptation plus independently authored Indonesian mastery companion; component provenance remains separated.", "change_notice": "See component rights records for translated/adapted and original portions.", "component_scope": [root_id], "license_expression": "CC-BY-4.0", "license_url": "https://creativecommons.org/licenses/by/4.0/", "non_endorsement": "Independent edition; no source-author endorsement.", "third_party_status": "Component-scoped rights records control."})
    rights[composite_rights] = composite
    owned_new_ids.add(composite_rights)
    asset_id = f"asset:o012-u{lecture:03d}-source-markdown"
    asset = common("asset", asset_id)
    asset.update({"bytes": spec["bytes"], "edition_id": EDITION_ID, "media_type": "text/markdown; charset=utf-8", "path": spec["relative"], "resource_id": RESOURCE_ID, "rights_component_id": composite_rights, "role": "canonical_reader_source", "sha256": spec["sha256"]})
    assets[asset_id] = asset
    owned_new_ids.add(asset_id)
    unit_context[lecture] = {"root_id": root_id, "anchor_start": anchor_start, "spans": spans, "text_lines": text_lines, "raw_lines": raw_lines, "spec": dict(spec), "original_ids": original_ids}


with TERMINOLOGY.open("r", encoding="utf-8", newline="") as stream:
    terminology_rows = {row["term_id"]: row for row in csv.DictReader(stream) if row["term_id"] in TERM_SPECS}
if set(terminology_rows) != set(TERM_SPECS):
    raise SystemExit(f"Units 11-13 terminology subset mismatch: {sorted(set(TERM_SPECS)-set(terminology_rows))}")
for control_id, (slug, evidence_local_id) in TERM_SPECS.items():
    row = terminology_rows[control_id]
    concept_id = f"concept:{slug}"
    term_id = f"term:{slug}:id-ID"
    lecture = int(re.search(r"l(\d{2})", evidence_local_id).group(1))
    if concept_id not in concepts:
        concept = common("concept", concept_id)
        concept.update({"canonical_label": row["source_term"], "domain": row["scope"], "locale_neutral": True})
        concepts[concept_id] = concept
        owned_new_ids.add(concept_id)
    elif slug != "universal-property":
        owned_new_ids.add(concept_id)
    if term_id in terms and slug == "universal-property":
        term = terms[term_id]
        term.update({"source_term": row["source_term"], "terminology_control_id": control_id, "terminology_status": row["status"], "usage_note": row["note"], "additional_evidence_segment_ids": [f"segment:{evidence_local_id}"], "timestamp": TIMESTAMP})
    else:
        evidence_unit = units[f"unit:{evidence_local_id}"]
        term = common("term", term_id)
        term.update({"concept_id": concept_id, "evidence_segment_id": f"segment:{evidence_local_id}", "locale": "id-ID", "preferred": row["id_ID"], "register": "textbook", "rejected_forms": [], "rights_component_id": evidence_unit["rights_component_id"], "scope_unit_id": unit_context[lecture]["root_id"], "source_term": row["source_term"], "terminology_control_id": control_id, "terminology_status": row["status"], "usage_note": row["note"], "variants": []})
        terms[term_id] = term
        owned_new_ids.add(term_id)


def add_relation(record_id: str, from_id: str, relation_type: str, to_id: str, note: str) -> None:
    record = common("relation", record_id)
    record.update({"from_id": from_id, "note": note, "relation_type": relation_type, "to_id": to_id})
    relations[record_id] = record
    owned_new_ids.add(record_id)


for lecture in (11, 12, 13):
    spec = SOURCE_SPECS[lecture]
    add_relation(f"relation:adapts:o012-rbt-u{lecture:03d}:roberts-edition", f"unit:o012-rbt-u{lecture:03d}", "adapts", EDITION_ID, f"Unit {lecture:03d} adapts Notes.tex lines {spec['upstream_start']}-{spec['upstream_end']} and adds an original solved mastery companion.")
    add_relation(f"relation:precedes:l{lecture:02d}:mastery", f"unit:o012-rbt-l{lecture:02d}", "precedes", f"unit:o012-rbt-l{lecture:02d}-mastery", "The translated lecture precedes its original solved mastery companion.")
for before, after in ((10, 11), (11, 12), (12, 13)):
    add_relation(f"relation:precedes:u{before:03d}:u{after:03d}", f"unit:o012-rbt-u{before:03d}", "precedes", f"unit:o012-rbt-u{after:03d}", "Cumulative reader order.")
for lecture, count in ((11, 3), (12, 4), (13, 6)):
    for number in range(1, count + 1):
        add_relation(f"relation:solves:l{lecture:02d}-sol-{number:03d}:l{lecture:02d}-mcheck-{number:03d}", f"unit:o012-rbt-l{lecture:02d}-sol-{number:03d}", "solves", f"unit:o012-rbt-l{lecture:02d}-mcheck-{number:03d}", f"Complete solution to Mastery Check {lecture}.{number}.")
for solution, source_exercise in ((2, 1), (3, 2)):
    add_relation(f"relation:solves:l13-sol-{solution:03d}:l13-ex-{source_exercise:03d}", f"unit:o012-rbt-l13-sol-{solution:03d}", "solves", f"unit:o012-rbt-l13-ex-{source_exercise:03d}", f"The bounded mastery solution also closes Source Exercise 13.{source_exercise}.")
for lecture, context in unit_context.items():
    for local_id in context["anchor_start"]:
        for alias in units[f"unit:{local_id}"].get("source_aliases", []):
            safe_alias = re.sub(r"[^a-z0-9]+", "-", alias.lower()).strip("-")
            add_relation(f"relation:xref:{local_id}:{safe_alias}", f"unit:{local_id}", "xref", EDITION_ID, f"Preserves the upstream source label {alias} for later cross-reference resolution.")


with LEDGER.open("r", encoding="utf-8", newline="") as stream:
    all_ledger_rows = list(csv.DictReader(stream))
if any(None in row or len(row) != 7 for row in all_ledger_rows):
    raise SystemExit("adverse ledger contains a non-canonical row")
ledger_rows = {row["event_id"]: row for row in all_ledger_rows if row["event_id"] in CORRECTION_TARGETS}
if set(ledger_rows) != set(CORRECTION_TARGETS):
    raise SystemExit(f"Units 11-13 adverse subset mismatch: {sorted(set(CORRECTION_TARGETS)-set(ledger_rows))}")
for event_id, affected_local_ids in CORRECTION_TARGETS.items():
    row = ledger_rows[event_id]
    number = int(event_id[-4:])
    lecture = 11 if number <= 155 else 12 if number <= 168 else 13
    context = unit_context[lecture]
    target_spans = [f"{context['spans'][local_id][0]}-{context['spans'][local_id][1]}" for local_id in affected_local_ids]
    correction_type = {"accessibility_reflow": "structural_adaptation", "identifier_preservation": "identifier_preservation", "clarified_in_translation": "clarification", "corrected_in_translation": "mathematical_correction"}[row["status"]]
    record_id = f"correction:o012-u{lecture:03d}-adv-{event_id[-4:]}"
    record = common("correction", record_id)
    record.update({"adverse_ledger_id": event_id, "affected_unit_ids": [f"unit:{item}" for item in affected_local_ids], "correction_type": correction_type, "edition_id": EDITION_ID, "evidence": f"{row['source_location']}; target spans {', '.join(target_spans)}.", "evidence_segment_id": f"segment:o012-rbt-l{lecture:02d}-notice", "severity": row["severity"], "rationale": row["rationale"], "resource_id": RESOURCE_ID, "source_defect": row["observed"], "target_change": row["action"], "unit_id": context["root_id"], "upstream_report_disposition": "not_contacted"})
    corrections[record_id] = record
    owned_new_ids.add(record_id)


cumulative = common("rights", CUMULATIVE_RIGHTS)
cumulative.update({"attribution": "Cumulative Units 001-013 reader: David Michael Roberts source adaptations plus independently authored Indonesian mastery companions; component provenance remains separated.", "change_notice": "Cumulative staged boundary only; Unit 001 through Unit 013 component rights records remain controlling.", "component_scope": [f"unit:o012-rbt-u{n:03d}" for n in range(1, 14)], "license_expression": "CC-BY-4.0", "license_url": "https://creativecommons.org/licenses/by/4.0/", "non_endorsement": "Independent edition; no source-author endorsement.", "third_party_status": "Component-scoped rights records control."})
rights[CUMULATIVE_RIGHTS] = cumulative
owned_new_ids.add(CUMULATIVE_RIGHTS)
roberts = rights[ROBERTS_RIGHTS]
roberts.update({"component_scope": [f"unit:o012-rbt-l{n:02d}" for n in range(1, 14)], "third_party_status": "No distinct third-party component is asserted within Units 001-013; the frozen archive remains authoritative for file-level review.", "timestamp": TIMESTAMP})
for authority_id in (PROGRAM_ID, COURSE_ID):
    authority[authority_id].update({"rights_component_id": CUMULATIVE_RIGHTS, "timestamp": TIMESTAMP})
authority[EDITION_ID].update({"local_derivative_unit_ids": [f"unit:o012-rbt-u{n:03d}" for n in range(1, 14)], "source_line_end": 3046, "timestamp": TIMESTAMP})


QA_IDS = {
    **{f"u{lecture}_{kind}": f"qa:o012-u{lecture:03d}-{kind}" for lecture in (11, 12, 13) for kind in ("source-integrity", "math-review", "language-review")},
    "build": "qa:o012-units-001-013-build", "accessibility": "qa:o012-units-001-013-accessibility", "visual": "qa:o012-units-001-013-visual",
}
review_artifacts = {lecture: f"artifact:o012-u{lecture:03d}-independent-review" for lecture in (11, 12, 13)}
unit_qa = {lecture: [QA_IDS[f"u{lecture}_source-integrity"], QA_IDS[f"u{lecture}_math-review"], QA_IDS[f"u{lecture}_language-review"]] for lecture in (11, 12, 13)}
manifest_id = "artifact:o012-units-001-013-manifest"
artifact_qa = {
    **{review_artifacts[lecture]: unit_qa[lecture] for lecture in (11, 12, 13)},
    "artifact:o012-units-001-013-html": [QA_IDS["build"], QA_IDS["accessibility"], QA_IDS["visual"]],
    manifest_id: [QA_IDS["build"]],
    "artifact:o012-units-001-013-pdf": [QA_IDS["build"], QA_IDS["accessibility"], QA_IDS["visual"]],
    "artifact:o012-units-001-013-qa-receipt": list(QA_IDS.values()),
    "artifact:o012-units-001-013-qa-text": [QA_IDS["build"], QA_IDS["u11_math-review"], QA_IDS["u12_math-review"], QA_IDS["u13_math-review"]],
    "artifact:o012-units-001-013-visual-receipt": [QA_IDS["accessibility"], QA_IDS["visual"]],
    "artifact:o012-units-001-013-render-inventory": [QA_IDS["accessibility"], QA_IDS["visual"]],
}
toolchains = {
    **{review_artifacts[lecture]: "Independent exact-span mathematical, structural, and Indonesian-language review." for lecture in (11, 12, 13)},
    "artifact:o012-units-001-013-html": "Pandoc 3.9.0.2 standalone HTML5 with embedded CSS and native MathML; two builds byte-identical.",
    manifest_id: "Deterministic cumulative Units 001-013 artifact manifest.",
    "artifact:o012-units-001-013-pdf": "Pandoc 3.9.0.2 with pdflatex; fixed epoch and builder-enforced two-build byte identity.",
    "artifact:o012-units-001-013-qa-receipt": "Fail-closed source, correction, rights, structure, HTML, PDF, link, language, and accessibility QA.",
    "artifact:o012-units-001-013-qa-text": "Poppler pdftotext with layout preservation and UTF-8 output.",
    "artifact:o012-units-001-013-visual-receipt": "Poppler all-page rendering plus Chromium desktop/mobile review.",
    "artifact:o012-units-001-013-render-inventory": "Canonical SHA-256 inventory of 138 ordered 110-dpi Poppler page renders.",
}
for artifact_id, (relative, expected_bytes, expected_sha, media_type, unit_id, state) in ARTIFACT_META.items():
    path = LANE / relative
    raw = path.read_bytes()
    if len(raw) != expected_bytes or digest(raw) != expected_sha:
        raise SystemExit(f"artifact identity mismatch: {relative}")
    record = common("artifact", artifact_id)
    record.update({"bytes": expected_bytes, "locale": "id-ID", "manifest_artifact_id": (manifest_id if artifact_id in {"artifact:o012-units-001-013-html", "artifact:o012-units-001-013-pdf"} else None), "media_type": media_type, "path": relative, "qa_event_ids": artifact_qa[artifact_id], "rights_component_id": CUMULATIVE_RIGHTS, "sha256": expected_sha, "toolchain": toolchains[artifact_id], "translation_state": state, "unit_id": unit_id})
    artifacts[artifact_id] = record
    owned_new_ids.add(artifact_id)

for lecture in (11, 12, 13):
    review_id = review_artifacts[lecture]
    for kind, qa_type, note in (
        ("source-integrity", "source", f"Unit {lecture:03d} exact source identity, contiguous upstream span, stable IDs, semantic environments, corrections, and aliases passed."),
        ("math-review", "math", f"Independent Unit {lecture:03d} review passed with no open P1, P2, or P3 finding; source prompts and mastery solutions are closed."),
        ("language-review", "language", f"Independent Unit {lecture:03d} Indonesian-language and terminology review passed."),
    ):
        qa_id = QA_IDS[f"u{lecture}_{kind}"]
        event = common("qa_event", qa_id)
        witnesses = [review_id] if qa_type == "language" else [review_id, "artifact:o012-units-001-013-qa-receipt"]
        if qa_type == "math":
            witnesses.append("artifact:o012-units-001-013-qa-text")
        event.update({"note": note, "qa_type": qa_type, "result": "passed", "unit_id": f"unit:o012-rbt-u{lecture:03d}", "witness_artifact_ids": witnesses})
        qa_events[qa_id] = event
        owned_new_ids.add(qa_id)

cumulative_qa = {
    QA_IDS["build"]: ("build", "Two fixed-epoch HTML builds were independently reproduced byte-identically and equal the final artifact; the existing builder fail-closes on two byte-identical PDF builds before copying the final PDF. Manifest, text witness, and prior boundaries remain hash-consistent.", ["artifact:o012-units-001-013-html", manifest_id, "artifact:o012-units-001-013-pdf", "artifact:o012-units-001-013-qa-receipt", "artifact:o012-units-001-013-qa-text"]),
    QA_IDS["accessibility"]: ("accessibility", "Semantic HTML passed with lang=id-ID, 4,682 native MathML nodes, 587 artifact IDs, all 160 fragments resolving, no runtime assets, desktop centering, mobile reflow, and all 54 wide mobile display formulae locally scrollable; PDF is secondary and untagged.", ["artifact:o012-units-001-013-html", "artifact:o012-units-001-013-qa-receipt", "artifact:o012-units-001-013-visual-receipt", "artifact:o012-units-001-013-render-inventory"]),
    QA_IDS["visual"]: ("visual", "All 138 PDF pages and the Unit 13 HTML surface at 1280x720 and 390x844 were inspected with no clipping, overlap, broken glyph, unintended blank page, or document-level overflow.", ["artifact:o012-units-001-013-html", "artifact:o012-units-001-013-pdf", "artifact:o012-units-001-013-visual-receipt", "artifact:o012-units-001-013-render-inventory"]),
}
for qa_id, (qa_type, note, witnesses) in cumulative_qa.items():
    event = common("qa_event", qa_id)
    event.update({"note": note, "qa_type": qa_type, "result": "passed", "unit_id": "unit:o012-rbt-u013", "witness_artifact_ids": witnesses})
    qa_events[qa_id] = event
    owned_new_ids.add(qa_id)


# Fail closed before replacing any backend file.
all_records: dict[str, dict[str, Any]] = {}
for filename, records in record_sets.items():
    for record_id, record in records.items():
        if record_id in all_records:
            raise SystemExit(f"duplicate global backend id after extension: {record_id}")
        if record.get("id") != record_id or record.get("schema") != SCHEMA or record.get("schema_version") != SCHEMA_VERSION:
            raise SystemExit(f"backend identity/schema mismatch in {filename}: {record_id}")
        all_records[record_id] = record

scalar_references = {"concept_id", "course_id", "edition_id", "evidence_segment_id", "from_id", "local_derivative_unit_id", "manifest_artifact_id", "parent_id", "program_id", "resource_id", "rights_component_id", "scope_unit_id", "to_id", "unit_id"}
list_references = {"affected_unit_ids", "additional_evidence_segment_ids", "component_scope", "concept_ids", "local_derivative_unit_ids", "qa_event_ids", "witness_artifact_ids"}
for record_id, record in all_records.items():
    for field in scalar_references:
        value = record.get(field)
        if value is not None and value not in all_records:
            raise SystemExit(f"unknown backend reference {record_id}.{field}={value}")
    for field in list_references:
        if field in record and (not isinstance(record[field], list) or any(value not in all_records for value in record[field])):
            raise SystemExit(f"unknown/list backend reference {record_id}.{field}")

for lecture, context in unit_context.items():
    spec = context["spec"]
    for local_id in context["anchor_start"]:
        start, end = context["spans"][local_id]
        expected = {"content_sha256": digest(b"".join(context["raw_lines"][start - 1:end])), "file_sha256": spec["sha256"], "line_end": end, "line_start": start, "path": spec["relative"]}
        if units[f"unit:{local_id}"]["target_locator"] != expected or segments[f"segment:{local_id}"]["target_locator"] != expected:
            raise SystemExit(f"Unit {lecture} target locator mismatch: {local_id}")
        if local_id not in context["text_lines"][start - 1]:
            raise SystemExit(f"Unit {lecture} anchor mismatch: {local_id}")
    expected_adverse = {11: {f"O012-ADV-{n:04d}" for n in range(143, 156)}, 12: {f"O012-ADV-{n:04d}" for n in range(156, 169)}, 13: {f"O012-ADV-{n:04d}" for n in range(169, 188)}}[lecture]
    actual = {record.get("adverse_ledger_id") for record in corrections.values() if record.get("unit_id") == context["root_id"]}
    if actual != expected_adverse:
        raise SystemExit(f"Unit {lecture} one-to-one correction inventory mismatch")

new_exercises = {record["id"] for record in units.values() if record.get("unit_kind") == "exercise" and any(f"l{lecture:02d}" in record["id"] for lecture in (11, 12, 13))}
new_solutions = {record["id"] for record in units.values() if record.get("unit_kind") == "solution" and any(f"l{lecture:02d}" in record["id"] for lecture in (11, 12, 13))}
new_solves = [record for record in relations.values() if record.get("relation_type") == "solves" and (record["from_id"] in new_solutions or record["to_id"] in new_exercises)]
if Counter(record["to_id"] for record in new_solves) != Counter({item: 1 for item in new_exercises}):
    raise SystemExit("Units 11-13 exercise closure mismatch")
if set(record["from_id"] for record in new_solves) != new_solutions:
    raise SystemExit("Units 11-13 solution coverage mismatch")

serialized = {name: canonical_jsonl(records) for name, records in record_sets.items()}
for filename, old_lines in prior_lines.items():
    for record_id, old_line in old_lines.items():
        if record_id in allowed_modified_existing:
            continue
        if canonical(record_sets[filename][record_id]) != old_line:
            raise SystemExit(f"prior record changed outside explicit cumulative update: {record_id}")
for name, raw in serialized.items():
    if b"\r" in raw or not raw.endswith(b"\n"):
        raise SystemExit(f"noncanonical JSONL bytes generated for {name}")
    ids = [json.loads(line)["id"] for line in raw.decode("utf-8").splitlines()]
    if ids != sorted(ids) or len(ids) != len(set(ids)):
        raise SystemExit(f"noncanonical JSONL ordering for {name}")

for name, raw in serialized.items():
    (BACKEND / name).write_bytes(raw)

bundle = hashlib.sha256()
total_bytes = 0
for name in JSONL_NAMES:
    raw = (BACKEND / name).read_bytes()
    if raw != serialized[name]:
        raise SystemExit(f"backend post-write mismatch: {name}")
    bundle.update(name.encode("utf-8")); bundle.update(b"\0"); bundle.update(raw)
    total_bytes += len(raw)

print("Units 011-013 backend extension: PASS")
for lecture in (11, 12, 13):
    print(f"unit_{lecture:03d}_stable_ids: {SOURCE_SPECS[lecture]['expected_ids']}")
print(f"terminology_controls: {len(TERM_SPECS)}")
print(f"adverse_ledger_records: {len(CORRECTION_TARGETS)}")
print(f"new_or_owned_records: {len(owned_new_ids)}")
print(f"records: {len(all_records)}")
print(f"jsonl_files: {len(JSONL_NAMES)}")
print(f"backend_bytes: {total_bytes}")
print(f"backend_bundle_sha256: {bundle.hexdigest()}")
