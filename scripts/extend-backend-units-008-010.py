#!/usr/bin/env python3
"""Deterministically extend the O012/D60 backend through Units 008-010."""

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
TIMESTAMP = "2026-08-22T21:00:00Z"
PROGRAM_ID = "program:o012-id"
COURSE_ID = "course:o012-d60"
RESOURCE_ID = "resource:roberts-algebraic-topology-2019"
EDITION_ID = "edition:roberts-at-2019-b947ad2"
ROBERTS_RIGHTS = "rights:roberts-cc-by-4.0"
UPSTREAM_COMMIT = "b947ad2e9f9e301bfe24590a9db653bc54fa1a53"
CUMULATIVE_RIGHTS = "rights:o012-units-001-010-composite-cc-by-4.0"
JSONL_NAMES = (
    "artifacts.jsonl", "assets.jsonl", "authority.jsonl", "concepts.jsonl",
    "corrections.jsonl", "qa.jsonl", "relations.jsonl", "rights.jsonl",
    "segments.jsonl", "terms.jsonl", "units.jsonl",
)

SOURCE_SPECS = {
    8: {
        "relative": "source/id-ID/units/unit-008-lecture-008.md",
        "bytes": 28466,
        "lines": 930,
        "sha256": "8369e74c80e391d73575bbcb7844d3bfa62dd771dbca6258eed02360b20529cc",
        "upstream_start": 1771,
        "upstream_end": 1946,
        "expected_ids": 26,
        "root_concepts": ["groupoid", "fundamental-groupoid", "simply-connected", "right-action"],
        "title": "Topologi Aljabar - Unit 8: Grupoid Fundamental dan Keterhubungan Sederhana",
    },
    9: {
        "relative": "source/id-ID/units/unit-009-lecture-009.md",
        "bytes": 25524,
        "lines": 939,
        "sha256": "16da25dea2f8ac5415b02738663046fb619c27e685042a734059e3150ed5ff18",
        "upstream_start": 1947,
        "upstream_end": 2093,
        "expected_ids": 30,
        "root_concepts": ["faithful-functor", "homotopy-invariance", "homotopy-lifting", "coset-space"],
        "title": "Topologi Aljabar - Unit 9: Kesetiaan, Invariansi Homotopi, dan Pengangkatan Homotopi",
    },
    10: {
        "relative": "source/id-ID/units/unit-010-lecture-010.md",
        "bytes": 26432,
        "lines": 934,
        "sha256": "e1c6ef961ae2266db86baec6d701dd659a1bf78bdd3601cf5b1c6515bc7d0310",
        "upstream_start": 2094,
        "upstream_end": 2272,
        "expected_ids": 26,
        "root_concepts": ["regular-action", "cyclic-group", "wedge-sum", "graph-covering", "free-group"],
        "title": "Topologi Aljabar - Unit 10: Penutup Terhubung Sederhana, Lingkaran, dan Baji",
    },
}

# term-control id -> (locale-neutral slug, exact evidence segment)
TERM_SPECS = {
    "O012-TERM-0134": ("groupoid", "o012-rbt-l08-def-001"),
    "O012-TERM-0135": ("small-groupoid", "o012-rbt-l08-def-001"),
    "O012-TERM-0136": ("locally-small", "o012-rbt-l08-def-001"),
    "O012-TERM-0137": ("discrete-groupoid", "o012-rbt-l08-exa-001"),
    "O012-TERM-0138": ("codiscrete-groupoid", "o012-rbt-l08-exa-001"),
    "O012-TERM-0139": ("action-groupoid", "o012-rbt-l08-exa-001"),
    "O012-TERM-0140": ("one-object-groupoid", "o012-rbt-l08-exa-001"),
    "O012-TERM-0141": ("conjugation", "o012-rbt-l08-lem-001"),
    "O012-TERM-0142": ("free-action", "o012-rbt-l08-lem-001"),
    "O012-TERM-0143": ("transitive-action", "o012-rbt-l08-lem-001"),
    "O012-TERM-0144": ("torsor", "o012-rbt-l08-lem-001"),
    "O012-TERM-0145": ("fundamental-groupoid", "o012-rbt-l08-def-002"),
    "O012-TERM-0146": ("simply-connected", "o012-rbt-l08-def-003"),
    "O012-TERM-0147": ("star-shaped-region", "o012-rbt-l08-ex-001"),
    "O012-TERM-0148": ("convex-subset", "o012-rbt-l08-ex-001"),
    "O012-TERM-0149": ("faithful-functor", "o012-rbt-l09-thm-001"),
    "O012-TERM-0150": ("full-functor", "o012-rbt-l09-mcheck-002"),
    "O012-TERM-0151": ("homotopy-invariance", "o012-rbt-l09-cor-002"),
    "O012-TERM-0152": ("homotopy-lifting", "o012-rbt-l09-cor-004"),
    "O012-TERM-0153": ("unit-sphere", "o012-rbt-l09-exa-001"),
    "O012-TERM-0154": ("infinite-dimensional-stiefel-manifold", "o012-rbt-l09-exa-001"),
    "O012-TERM-0155": ("coset-space", "o012-rbt-l09-thm-002"),
    "O012-TERM-0156": ("stabilizer-subgroup", "o012-rbt-l09-sol-005"),
    "O012-TERM-0157": ("equivariant", "o012-rbt-l09-sol-005"),
    "O012-TERM-0158": ("left-coset", "o012-rbt-l09-sol-005"),
    "O012-TERM-0159": ("right-coset", "o012-rbt-l09-thm-002"),
    "O012-TERM-0160": ("g-set", "o012-rbt-l10-proof-001"),
    "O012-TERM-0161": ("regular-action", "o012-rbt-l10-cor-001"),
    "O012-TERM-0162": ("countable", "o012-rbt-l10-exa-001"),
    "O012-TERM-0163": ("permutation-group", "o012-rbt-l10-exa-001"),
    "O012-TERM-0164": ("faithful-permutation-representation", "o012-rbt-l10-exa-001"),
    "O012-TERM-0165": ("cyclic-group", "o012-rbt-l10-thm-001"),
    "O012-TERM-0166": ("generator", "o012-rbt-l10-thm-001"),
    "O012-TERM-0167": ("free-product", "o012-rbt-l10-s03"),
    "O012-TERM-0168": ("free-group", "o012-rbt-l10-s03"),
    "O012-TERM-0169": ("reduced-word", "o012-rbt-l10-s03"),
    "O012-TERM-0170": ("conjugacy-class", "o012-rbt-l10-sol-001"),
    "O012-TERM-0171": ("graph-covering", "o012-rbt-l10-fig-001"),
}

CORRECTION_TARGETS = {
    "O012-ADV-0095": ["o012-rbt-l08-s01"],
    "O012-ADV-0096": ["o012-rbt-l08"],
    "O012-ADV-0097": ["o012-rbt-l08-exa-001"],
    "O012-ADV-0098": ["o012-rbt-l08-exa-001"],
    "O012-ADV-0099": ["o012-rbt-l08-lem-001"],
    "O012-ADV-0100": ["o012-rbt-l08-lem-001"],
    "O012-ADV-0101": ["o012-rbt-l08-def-002"],
    "O012-ADV-0102": ["o012-rbt-l08-def-002"],
    "O012-ADV-0103": ["o012-rbt-l08-def-002"],
    "O012-ADV-0104": ["o012-rbt-l08-prop-001"],
    "O012-ADV-0105": ["o012-rbt-l08-prop-001"],
    "O012-ADV-0106": ["o012-rbt-l08-def-003"],
    "O012-ADV-0107": ["o012-rbt-l08-ex-001"],
    "O012-ADV-0108": ["o012-rbt-l08-prop-002"],
    "O012-ADV-0109": ["o012-rbt-l08-prop-002"],
    "O012-ADV-0110": ["o012-rbt-l08-exa-003"],
    "O012-ADV-0111": ["o012-rbt-l08-exa-003"],
    "O012-ADV-0112": ["o012-rbt-l08-prop-001", "o012-rbt-l08-exa-003"],
    "O012-ADV-0113": ["o012-rbt-l09"],
    "O012-ADV-0114": ["o012-rbt-l09-prop-001"],
    "O012-ADV-0115": ["o012-rbt-l09-proof-001"],
    "O012-ADV-0116": ["o012-rbt-l09-proof-001"],
    "O012-ADV-0117": ["o012-rbt-l09-proof-001"],
    "O012-ADV-0118": ["o012-rbt-l09-cor-002"],
    "O012-ADV-0119": ["o012-rbt-l09-ex-001", "o012-rbt-l09-sol-001"],
    "O012-ADV-0120": ["o012-rbt-l09-exa-001"],
    "O012-ADV-0121": ["o012-rbt-l09-cor-004"],
    "O012-ADV-0122": ["o012-rbt-l09-proof-004"],
    "O012-ADV-0123": ["o012-rbt-l09-proof-005"],
    "O012-ADV-0124": ["o012-rbt-l09-proof-005"],
    "O012-ADV-0125": ["o012-rbt-l09-thm-002"],
    "O012-ADV-0126": ["o012-rbt-l10-proof-001"],
    "O012-ADV-0127": ["o012-rbt-l10-proof-001"],
    "O012-ADV-0128": ["o012-rbt-l10-proof-001"],
    "O012-ADV-0129": ["o012-rbt-l10-exa-001"],
    "O012-ADV-0130": ["o012-rbt-l10-thm-001"],
    "O012-ADV-0131": ["o012-rbt-l10-thm-001"],
    "O012-ADV-0132": ["o012-rbt-l10-s01"],
    "O012-ADV-0133": ["o012-rbt-l10-s01"],
    "O012-ADV-0134": ["o012-rbt-l10-s02"],
    "O012-ADV-0135": ["o012-rbt-l10-def-001"],
    "O012-ADV-0136": ["o012-rbt-l10-def-001"],
    "O012-ADV-0137": ["o012-rbt-l10-s02"],
    "O012-ADV-0138": ["o012-rbt-l10-fig-001"],
    "O012-ADV-0139": ["o012-rbt-l10-fig-001"],
    "O012-ADV-0140": ["o012-rbt-l10-fig-001"],
    "O012-ADV-0141": ["o012-rbt-l10-fig-001"],
    "O012-ADV-0142": ["o012-rbt-l10-s03", "o012-rbt-l10-mcheck-005"],
}

ARTIFACT_META = {
    "artifact:o012-u008-independent-review": ("qa/UNIT_008_INDEPENDENT_REVIEW.md", 2191, "6960e19949642723dcbfd6ff5bfe105fe4e2789f5989787c041c7f41bdfdac3f", "text/markdown; charset=utf-8", "unit:o012-rbt-u008", "mathematically_reviewed"),
    "artifact:o012-u009-independent-review": ("qa/UNIT_009_INDEPENDENT_REVIEW.md", 2147, "af91c517608c454466d6371db479385ddb1b4c65ecba2f05ca9ec7b26b49cbe6", "text/markdown; charset=utf-8", "unit:o012-rbt-u009", "mathematically_reviewed"),
    "artifact:o012-u010-independent-review": ("qa/UNIT_010_INDEPENDENT_REVIEW.md", 2683, "236123c6c1ad15773a1da7f36887a2ebed93298f019db80f79dfa9bcdac100fd", "text/markdown; charset=utf-8", "unit:o012-rbt-u010", "mathematically_reviewed"),
    "artifact:o012-units-001-010-html": ("output/html/units-001-010/index.html", 1318415, "e228ac1422b2742d873feffd5b236fe9c1329d0bdb5da0e8deffe5e770361088", "text/html; charset=utf-8", "unit:o012-rbt-u010", "built"),
    "artifact:o012-units-001-010-manifest": ("output/ARTIFACT_MANIFEST_UNITS_001_010.csv", 248, "5bcf82984e3f2848f5471876401e48948639d6ca144e0915d99c86c20fc39d92", "text/csv; charset=utf-8", "unit:o012-rbt-u010", "built"),
    "artifact:o012-units-001-010-pdf": ("output/pdf/topologi-aljabar-unit-001-010-id.pdf", 862913, "d0f739aedf3da5f317cf99a1a0dcace1f89b8c802f1dedc42c7ac0c63375c7c1", "application/pdf", "unit:o012-rbt-u010", "built"),
    "artifact:o012-units-001-010-qa-receipt": ("qa/UNITS_001_010_QA.json", 9808, "4189663021e6bd7e8822198a79bb3d7c59c7e0cca777054fbc370e77a300da5c", "application/json", "unit:o012-rbt-u010", "built"),
    "artifact:o012-units-001-010-qa-text": ("qa/units-001-010-extracted.txt", 280664, "4932889b582a3ccd9816db4b8008791d5fbdc4b044da6f5d1985a87b6ce10642", "text/plain; charset=utf-8", "unit:o012-rbt-u010", "built"),
    "artifact:o012-units-001-010-visual-receipt": ("qa/UNITS_001_010_VISUAL_QA.md", 2471, "439099f8c865125864444f9cfd1f60b961274ba0bc6f9bb29c562ee30fab132b", "text/markdown; charset=utf-8", "unit:o012-rbt-u010", "visually_checked"),
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def common(entity_type: str, record_id: str) -> dict[str, Any]:
    return {
        "entity_type": entity_type, "id": record_id, "schema": SCHEMA,
        "schema_version": SCHEMA_VERSION, "status": "active", "supersedes": None,
        "timestamp": TIMESTAMP, "workflow": WORKFLOW,
    }


def canonical_record(record: dict[str, Any]) -> str:
    return json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def canonical_jsonl(records: dict[str, dict[str, Any]]) -> bytes:
    return "".join(canonical_record(records[key]) + "\n" for key in sorted(records)).encode("utf-8")


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

allowed_modified_existing = {PROGRAM_ID, COURSE_ID, EDITION_ID, ROBERTS_RIGHTS}
owned_new_ids: set[str] = set()
unit_context: dict[int, dict[str, Any]] = {}
term_slugs_by_evidence: defaultdict[str, list[str]] = defaultdict(list)
for _, (slug, evidence_local_id) in TERM_SPECS.items():
    term_slugs_by_evidence[evidence_local_id].append(slug)


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
    tokens = {
        "-exa-": "example", "-lem-": "lemma", "-def-": "definition",
        "-thm-": "theorem", "-proof-": "proof", "-rem-": "remark",
        "-prop-": "proposition", "-cor-": "corollary", "-fig-": "figure",
    }
    for token, kind in tokens.items():
        if token in local_id:
            return kind
    raise SystemExit(f"cannot infer unit kind: {local_id}")


def is_original(local_id: str) -> bool:
    return any(token in local_id for token in ("-notice", "-mastery", "-mcheck-", "-sol-"))


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
    aliases: dict[str, list[str]] = {}
    for number, text in enumerate(text_lines, start=1):
        found = id_re.findall(text)
        if len(found) > 1:
            raise SystemExit(f"multiple stable IDs on Unit {lecture} line {number}")
        if found:
            if found[0] in anchor_start:
                raise SystemExit(f"duplicate stable ID: {found[0]}")
            anchor_start[found[0]] = number
            alias_match = re.search(r'data-source-label="([^"]+)"', text)
            if alias_match:
                aliases[found[0]] = [alias_match.group(1)]
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
            for candidate in text_lines[anchor_start[local_id] : spans[local_id][1]]:
                match = re.match(r"^\*\*(.+?)\*\*", candidate)
                if match:
                    display = match.group(1).strip()
                    break
        slugs = list(spec["root_concepts"]) + term_slugs_by_evidence.get(local_id, [])
        metadata[local_id] = {
            "display": display, "kind": kind, "parent": parent, "order": order,
            "concept_slugs": list(dict.fromkeys(slugs)),
        }

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
        extra = {"source_aliases": aliases[local_id]} if local_id in aliases else {}
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
        "root_id": root_id, "anchor_start": anchor_start, "spans": spans,
        "text_lines": text_lines, "raw_lines": raw_lines, "spec": dict(spec),
    }


with TERMINOLOGY.open("r", encoding="utf-8", newline="") as stream:
    terminology_rows = {row["term_id"]: row for row in csv.DictReader(stream) if row["term_id"] in TERM_SPECS}
if set(terminology_rows) != set(TERM_SPECS):
    raise SystemExit(f"Unit 8-10 terminology subset mismatch: {sorted(set(TERM_SPECS)-set(terminology_rows))}")
for term_control_id, (slug, evidence_local_id) in TERM_SPECS.items():
    row = terminology_rows[term_control_id]
    concept_id = f"concept:{slug}"
    term_id = f"term:{slug}:id-ID"
    if concept_id in concepts or term_id in terms:
        raise SystemExit(f"new terminology id collides with prior backend: {slug}")
    concept = common("concept", concept_id)
    concept.update({"canonical_label": row["source_term"], "domain": row["scope"], "locale_neutral": True})
    concepts[concept_id] = concept
    owned_new_ids.add(concept_id)
    lecture = int(re.search(r"l(\d{2})", evidence_local_id).group(1))
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


for lecture in (8, 9, 10):
    spec = SOURCE_SPECS[lecture]
    add_relation(
        f"relation:adapts:o012-rbt-u{lecture:03d}:roberts-edition",
        f"unit:o012-rbt-u{lecture:03d}", "adapts", EDITION_ID,
        f"Unit {lecture:03d} adapts Notes.tex lines {spec['upstream_start']}-{spec['upstream_end']} and adds an original solved mastery companion.",
    )
    add_relation(
        f"relation:precedes:l{lecture:02d}:mastery", f"unit:o012-rbt-l{lecture:02d}",
        "precedes", f"unit:o012-rbt-l{lecture:02d}-mastery",
        "The translated lecture precedes its original solved mastery companion.",
    )
add_relation("relation:precedes:u007:u008", "unit:o012-rbt-u007", "precedes", "unit:o012-rbt-u008", "Cumulative reader order.")
add_relation("relation:precedes:u008:u009", "unit:o012-rbt-u008", "precedes", "unit:o012-rbt-u009", "Cumulative reader order.")
add_relation("relation:precedes:u009:u010", "unit:o012-rbt-u009", "precedes", "unit:o012-rbt-u010", "Cumulative reader order.")
for lecture in (8, 9):
    add_relation(
        f"relation:solves:l{lecture:02d}-sol-001:l{lecture:02d}-ex-001",
        f"unit:o012-rbt-l{lecture:02d}-sol-001", "solves", f"unit:o012-rbt-l{lecture:02d}-ex-001",
        f"Complete solution to the source exercise in Lecture {lecture}.",
    )
    for number in range(2, 6):
        add_relation(
            f"relation:solves:l{lecture:02d}-sol-{number:03d}:l{lecture:02d}-mcheck-{number:03d}",
            f"unit:o012-rbt-l{lecture:02d}-sol-{number:03d}", "solves",
            f"unit:o012-rbt-l{lecture:02d}-mcheck-{number:03d}",
            f"Complete solution to Mastery Check {lecture}.{number}.",
        )
for number in range(1, 6):
    add_relation(
        f"relation:solves:l10-sol-{number:03d}:l10-mcheck-{number:03d}",
        f"unit:o012-rbt-l10-sol-{number:03d}", "solves", f"unit:o012-rbt-l10-mcheck-{number:03d}",
        f"Complete solution to Mastery Check 10.{number}.",
    )
for lecture, context in unit_context.items():
    for local_id in context["anchor_start"]:
        aliases = units[f"unit:{local_id}"].get("source_aliases", [])
        for alias in aliases:
            safe_alias = re.sub(r"[^a-z0-9]+", "-", alias.lower()).strip("-")
            add_relation(
                f"relation:xref:{local_id}:{safe_alias}", f"unit:{local_id}", "xref", EDITION_ID,
                f"Preserves the upstream source label {alias} for later cross-reference resolution.",
            )


with LEDGER.open("r", encoding="utf-8", newline="") as stream:
    all_ledger_rows = list(csv.DictReader(stream))
if any(None in row or len(row) != 7 for row in all_ledger_rows):
    raise SystemExit("adverse ledger contains a non-canonical CSV row")
ledger_rows = {row["event_id"]: row for row in all_ledger_rows if row["event_id"] in CORRECTION_TARGETS}
if set(ledger_rows) != set(CORRECTION_TARGETS):
    raise SystemExit(f"Unit 8-10 adverse subset mismatch: {sorted(set(CORRECTION_TARGETS)-set(ledger_rows))}")
for event_id, affected_local_ids in CORRECTION_TARGETS.items():
    row = ledger_rows[event_id]
    number = int(event_id[-4:])
    lecture = 8 if number <= 112 else 9 if number <= 125 else 10
    context = unit_context[lecture]
    target_locations = [f"{context['spans'][local_id][0]}-{context['spans'][local_id][1]}" for local_id in affected_local_ids]
    correction_type = {
        "accessibility_reflow": "structural_adaptation",
        "identifier_preservation": "identifier_preservation",
        "clarified_in_translation": "clarification",
        "corrected_in_translation": "mathematical_correction",
    }[row["status"]]
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


cumulative = common("rights", CUMULATIVE_RIGHTS)
cumulative.update({
    "attribution": "Cumulative Units 001-010 reader: David Michael Roberts source adaptations plus independently authored Indonesian mastery companions; component provenance remains separated.",
    "change_notice": "Cumulative staged boundary only; Unit 001 through Unit 010 component rights records remain controlling.",
    "component_scope": [f"unit:o012-rbt-u{number:03d}" for number in range(1, 11)],
    "license_expression": "CC-BY-4.0", "license_url": "https://creativecommons.org/licenses/by/4.0/",
    "non_endorsement": "Independent edition; no source-author endorsement.",
    "third_party_status": "Component-scoped rights records control.",
})
rights[CUMULATIVE_RIGHTS] = cumulative
owned_new_ids.add(CUMULATIVE_RIGHTS)
roberts = rights[ROBERTS_RIGHTS]
roberts["component_scope"] = [f"unit:o012-rbt-l{number:02d}" for number in range(1, 11)]
roberts["third_party_status"] = "No distinct third-party component is asserted within Units 001-010; the frozen archive remains authoritative for file-level review."
roberts["timestamp"] = TIMESTAMP
for authority_id in (PROGRAM_ID, COURSE_ID):
    authority[authority_id]["rights_component_id"] = CUMULATIVE_RIGHTS
    authority[authority_id]["timestamp"] = TIMESTAMP
edition = authority[EDITION_ID]
edition["local_derivative_unit_ids"] = [f"unit:o012-rbt-u{number:03d}" for number in range(1, 11)]
edition["source_line_end"] = 2272
edition["timestamp"] = TIMESTAMP


QA_IDS = {
    **{f"u{lecture}_{kind}": f"qa:o012-u{lecture:03d}-{kind}" for lecture in (8, 9, 10) for kind in ("source-integrity", "math-review", "language-review")},
    "build": "qa:o012-units-001-010-build",
    "accessibility": "qa:o012-units-001-010-accessibility",
    "visual": "qa:o012-units-001-010-visual",
}
review_artifacts = {lecture: f"artifact:o012-u{lecture:03d}-independent-review" for lecture in (8, 9, 10)}
unit_qa = {
    lecture: [QA_IDS[f"u{lecture}_source-integrity"], QA_IDS[f"u{lecture}_math-review"], QA_IDS[f"u{lecture}_language-review"]]
    for lecture in (8, 9, 10)
}
artifact_qa = {
    **{review_artifacts[lecture]: unit_qa[lecture] for lecture in (8, 9, 10)},
    "artifact:o012-units-001-010-html": [QA_IDS["build"], QA_IDS["accessibility"], QA_IDS["visual"]],
    "artifact:o012-units-001-010-manifest": [QA_IDS["build"]],
    "artifact:o012-units-001-010-pdf": [QA_IDS["build"], QA_IDS["accessibility"], QA_IDS["visual"]],
    "artifact:o012-units-001-010-qa-receipt": list(QA_IDS.values()),
    "artifact:o012-units-001-010-qa-text": [QA_IDS["build"], QA_IDS["u8_math-review"], QA_IDS["u9_math-review"], QA_IDS["u10_math-review"]],
    "artifact:o012-units-001-010-visual-receipt": [QA_IDS["accessibility"], QA_IDS["visual"]],
}
manifest_id = "artifact:o012-units-001-010-manifest"
toolchains = {
    **{review_artifacts[lecture]: "Independent exact-span mathematical, structural, and Indonesian-language review." for lecture in (8, 9, 10)},
    "artifact:o012-units-001-010-html": "Pandoc 3.9.0.2 standalone HTML5 with embedded CSS and native MathML; two builds byte-identical.",
    "artifact:o012-units-001-010-manifest": "Deterministic cumulative Units 001-010 artifact manifest.",
    "artifact:o012-units-001-010-pdf": "Pandoc 3.9.0.2 with pdflatex; fixed epoch and two builds byte-identical.",
    "artifact:o012-units-001-010-qa-receipt": "Fail-closed source, correction, rights, structure, HTML, PDF, link, language, and accessibility QA.",
    "artifact:o012-units-001-010-qa-text": "Poppler pdftotext with layout preservation and UTF-8 output.",
    "artifact:o012-units-001-010-visual-receipt": "Poppler all-page rendering plus Codex in-app Chromium desktop/mobile review.",
}
for artifact_id, (relative, expected_bytes, expected_sha, media_type, unit_id, state) in ARTIFACT_META.items():
    path = LANE / relative
    raw = path.read_bytes()
    if len(raw) != expected_bytes or sha256(raw) != expected_sha:
        raise SystemExit(f"final artifact identity mismatch: {relative}")
    artifact = common("artifact", artifact_id)
    artifact.update({
        "bytes": expected_bytes, "locale": "id-ID",
        "manifest_artifact_id": (manifest_id if artifact_id in {"artifact:o012-units-001-010-html", "artifact:o012-units-001-010-pdf"} else None),
        "media_type": media_type, "path": relative, "qa_event_ids": artifact_qa[artifact_id],
        "rights_component_id": CUMULATIVE_RIGHTS, "sha256": expected_sha,
        "toolchain": toolchains[artifact_id], "translation_state": state, "unit_id": unit_id,
    })
    artifacts[artifact_id] = artifact
    owned_new_ids.add(artifact_id)

for lecture in (8, 9, 10):
    review_id = review_artifacts[lecture]
    for kind, qa_type, note in (
        ("source-integrity", "source", f"Unit {lecture:03d} exact source identity, upstream span, stable IDs, semantic environments, corrections, and aliases passed."),
        ("math-review", "math", f"Independent Unit {lecture:03d} review passed with P1, P2, and P3 all zero; every exercise has a complete solution."),
        ("language-review", "language", f"Independent Unit {lecture:03d} Indonesian-language and terminology review passed."),
    ):
        qa_id = QA_IDS[f"u{lecture}_{kind}"]
        event = common("qa_event", qa_id)
        event.update({
            "note": note, "qa_type": qa_type, "result": "passed",
            "unit_id": f"unit:o012-rbt-u{lecture:03d}",
            "witness_artifact_ids": [review_id, "artifact:o012-units-001-010-qa-receipt"],
        })
        qa_events[qa_id] = event
        owned_new_ids.add(qa_id)

cumulative_qa = {
    QA_IDS["build"]: (
        "build",
        "Two fixed-epoch HTML builds and two fixed-epoch PDF builds were byte-identical; manifest, text witness, and every prior source/artifact/QA witness are hash-consistent.",
        ["artifact:o012-units-001-010-html", manifest_id, "artifact:o012-units-001-010-pdf", "artifact:o012-units-001-010-qa-receipt", "artifact:o012-units-001-010-qa-text"],
    ),
    QA_IDS["accessibility"]: (
        "accessibility",
        "Semantic HTML passed with lang=id-ID, 3,411 native MathML nodes, 431 unique IDs, all 123 fragments resolving, no runtime assets, desktop centering, mobile reflow, and all 37 wide formulae locally scrollable; PDF is secondary and untagged.",
        ["artifact:o012-units-001-010-html", "artifact:o012-units-001-010-qa-receipt", "artifact:o012-units-001-010-visual-receipt"],
    ),
    QA_IDS["visual"]: (
        "visual",
        "All 99 PDF pages and representative Unit 8-10 HTML surfaces at 1280x720 and 390x844 were inspected with no clipping, overlap, orphan page, or document-level overflow.",
        ["artifact:o012-units-001-010-html", "artifact:o012-units-001-010-pdf", "artifact:o012-units-001-010-visual-receipt"],
    ),
}
for qa_id, (qa_type, note, witnesses) in cumulative_qa.items():
    event = common("qa_event", qa_id)
    event.update({"note": note, "qa_type": qa_type, "result": "passed", "unit_id": "unit:o012-rbt-u010", "witness_artifact_ids": witnesses})
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
    spec = context["spec"]
    for local_id in context["anchor_start"]:
        unit = units[f"unit:{local_id}"]
        segment = segments[f"segment:{local_id}"]
        start, end = context["spans"][local_id]
        expected_locator = context_locator(context, start, end)
        if unit["target_locator"] != expected_locator or segment["target_locator"] != expected_locator:
            raise SystemExit(f"Unit {lecture} unit/segment locator mismatch: {local_id}")
        if local_id not in context["text_lines"][start - 1]:
            raise SystemExit(f"Unit {lecture} anchor mismatch: {local_id}")
        if unit["path"][-1] != unit["id"] or any(node not in units for node in unit["path"]):
            raise SystemExit(f"Unit {lecture} hierarchy mismatch: {local_id}")
    root = units[context["root_id"]]
    if root["target_locator"] != context_locator(context, 1, spec["lines"]):
        raise SystemExit(f"Unit {lecture} root locator mismatch")
    expected_adverse = {
        8: {f"O012-ADV-{number:04d}" for number in range(95, 113)},
        9: {f"O012-ADV-{number:04d}" for number in range(113, 126)},
        10: {f"O012-ADV-{number:04d}" for number in range(126, 143)},
    }[lecture]
    actual_corrections = [record for record in corrections.values() if record.get("unit_id") == context["root_id"]]
    if {record.get("adverse_ledger_id") for record in actual_corrections} != expected_adverse:
        raise SystemExit(f"Unit {lecture} one-to-one correction inventory mismatch")

new_exercises = {
    record["id"] for record in units.values()
    if record.get("unit_kind") == "exercise" and any(f"l{lecture:02d}" in record["id"] for lecture in (8, 9, 10))
}
new_solutions = {
    record["id"] for record in units.values()
    if record.get("unit_kind") == "solution" and any(f"l{lecture:02d}" in record["id"] for lecture in (8, 9, 10))
}
new_solves = [
    record for record in relations.values()
    if record.get("relation_type") == "solves" and (record["from_id"] in new_solutions or record["to_id"] in new_exercises)
]
if Counter(record["from_id"] for record in new_solves) != Counter({item: 1 for item in new_solutions}):
    raise SystemExit("Unit 8-10 solution closure mismatch")
if Counter(record["to_id"] for record in new_solves) != Counter({item: 1 for item in new_exercises}):
    raise SystemExit("Unit 8-10 exercise closure mismatch")

for artifact_id in ARTIFACT_META:
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

print("Units 008-010 backend extension: PASS")
print(f"unit_008_stable_ids: {SOURCE_SPECS[8]['expected_ids']}")
print(f"unit_009_stable_ids: {SOURCE_SPECS[9]['expected_ids']}")
print(f"unit_010_stable_ids: {SOURCE_SPECS[10]['expected_ids']}")
print(f"terminology_records: {len(TERM_SPECS)}")
print(f"adverse_ledger_records: {len(CORRECTION_TARGETS)}")
print(f"new_or_owned_records: {len(owned_new_ids)}")
print(f"records: {len(all_records)}")
print(f"jsonl_files: {len(JSONL_NAMES)}")
print(f"backend_bytes: {total_bytes}")
print(f"backend_bundle_sha256: {bundle.hexdigest()}")
