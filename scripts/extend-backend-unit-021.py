#!/usr/bin/env python3
"""Fail-closed append-only backend extension for final Roberts Unit 021.

Every byte of the 2,959-record Units 001--020 backend is an immutable prefix.
This producer verifies that prefix, the frozen Unit 21 reader and its four
evidence files, terminology controls 0290--0292, and adverse controls
0290--0297.  It builds all additions in memory, validates references and
mastery closure, and only then appends canonical sorted record batches.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

LANE = Path(__file__).resolve().parents[1]
BACKEND = LANE / "backend"
SOURCE = LANE / "source/id-ID/units/unit-021-lecture-021.md"
TERMINOLOGY = LANE / "00_control/TERMINOLOGY.csv"
LEDGER = LANE / "00_control/ADVERSE_LEDGER.csv"
SCHEMA = "curriculum.interop"
VERSION = "0.1.0"
WORKFLOW = "o012-d60-id-reader-production"
STAMP = "2026-08-23T00:00:00Z"
PROGRAM = "program:o012-id"
COURSE = "course:o012-d60"
RESOURCE = "resource:roberts-algebraic-topology-2019"
EDITION = "edition:roberts-at-2019-b947ad2"
COMMIT = "b947ad2e9f9e301bfe24590a9db653bc54fa1a53"
ROBERTS_RIGHTS = "rights:roberts-cc-by-4.0"
COMPANION_RIGHTS = "rights:o012-u021-companion-cc-by-4.0"
COMPOSITE_RIGHTS = "rights:o012-u021-composite-cc-by-4.0"
CUMULATIVE_RIGHTS = "rights:o012-units-001-021-composite-cc-by-4.0"
PRIOR_RIGHTS = "rights:o012-units-001-020-composite-cc-by-4.0-final-ed086"
ROOT = "unit:o012-rbt-u021"
LECTURE = "unit:o012-rbt-l21"
MASTERY = "unit:o012-rbt-l21-mastery"
SOURCE_BYTES = 26237
SOURCE_LINES = 786
SOURCE_SHA = "47fa3994dc59370fc464e9d150d62512a4602a3cffa5996f1027f93a427e0eec"
UPSTREAM_SPAN_SHA = "281ba27f0f52f35fd9842954c223546e84ce1a0909ee84c14b2081c38c11f150"
UPSTREAM_RAW_SHA = "8a3ab990ae87087dd259340b08cdb7ddb95068a5b9859de66f7e002115307e6f"
FILES = ("artifacts.jsonl", "assets.jsonl", "authority.jsonl", "concepts.jsonl",
         "corrections.jsonl", "qa.jsonl", "relations.jsonl", "rights.jsonl",
         "segments.jsonl", "terms.jsonl", "units.jsonl")
PREFIX = {
    "artifacts.jsonl": (96, 75185, "5c3f5b0a92c5c742c057a0ac9f4d7153d5962c25c003666f1c75a0fd05868cda"),
    "assets.jsonl": (22, 13599, "96ee89e8509f8d32d7d042800ff7e958b04349468e9a97b4ec9bc527bf7a7607"),
    "authority.jsonl": (4, 2721, "f21af26912520ab34b38dff0e927ed46a546dbe5d318da0dc133e58330d0e368"),
    "concepts.jsonl": (286, 89861, "59258c4a1656d5caa4665755178a9336c6a5d3f63dd4c8643a34eec44f11d024"),
    "corrections.jsonl": (280, 272419, "e734dac689fc07a47bbcc2999430a90ee8d8b93e4995db5b49a930f460e0eb86"),
    "qa.jsonl": (94, 53524, "9cf2edfb4c738b5d7a2adfecd0b596529a181ca99e713eb3e0d9cd09c8b667b2"),
    "relations.jsonl": (261, 104751, "cf3fec76fcd3a0a4cd235dd173f95ca1fb4e17f7890c1d10a0d08d6a01ef0d04"),
    "rights.jsonl": (51, 46017, "d4650781f3f8b84dd8867d85bccec03f5216521989af89c7fc1db631d4fa6dde"),
    "segments.jsonl": (783, 924450, "dd04335b3bf58e572028cc90b1d8c78eae8c230d3c1a7c85913149e165b814d6"),
    "terms.jsonl": (279, 169425, "7afdf5384d61dadc4f9617578a4a26e66234773b45281e3ace71abdb04b409dd"),
    "units.jsonl": (803, 986808, "b0e16b8879173da18f1cd28e2c3d27752387cf81d61a35dce8c4049d42c6d37a"),
}
ARTIFACTS = {
    "artifact:o012-u021-independent-review": (
        "qa/UNIT_021_INDEPENDENT_REVIEW.md", 2678,
        "44975beb96e04717fc92a9f2743a5fc73997f1d7139c75285743766fecfa9bfb",
        "text/markdown; charset=utf-8", "mathematically_reviewed",
        ["qa:o012-u021-math", "qa:o012-u021-language"]),
    "artifact:o012-u021-source-audit": (
        "qa/UNIT_021_SOURCE_AUDIT.md", 3331,
        "38ba068dcf96a58dd76e951b8250cec33798e6aac744244fb1cf0e6db18ea650",
        "text/markdown; charset=utf-8", "source_frozen",
        ["qa:o012-u021-source-integrity"]),
    "artifact:o012-u021-qa": (
        "qa/UNIT_021_QA.json", 3967,
        "8f3f11a101ea09c0321989594a4a505ba44f92b8bde732d9c493d3de66a423ca",
        "application/json", "built", ["qa:o012-u021-source-integrity"]),
    "artifact:o012-u021-translation-handoff": (
        "qa/UNIT_021_TRANSLATION_HANDOFF.md", 1935,
        "9fa065b56a70abec8c54112515cf3425407a8bb32823c40f1d745a7705e5d466",
        "text/markdown; charset=utf-8", "source_frozen",
        ["qa:o012-u021-source-integrity", "qa:o012-u021-language"]),
}
TERM_SPECS = {
    "O012-TERM-0290": ("geometric realisation", "realisasi geometrik",
                       "geometric-realisation", "o012-rbt-l21-def-002",
                       "algebraic_topology"),
    "O012-TERM-0291": ("standard n-simplex", "simpleks-n standar",
                       "standard-n-simplex", "o012-rbt-l21-def-001",
                       "simplicial_topology"),
    "O012-TERM-0292": ("triangulation", "triangulasi",
                       "triangulation", "o012-rbt-l21-def-003",
                       "surface_topology"),
}
EXPECTED_ADVERSE = {
    290: ("P1", "Notes.tex:4358-4360", "corrected_in_translation",
          ["s01", "audit-001"], "mathematical_correction"),
    291: ("P1", "Notes.tex:4393-4400", "corrected_in_translation",
          ["constr-002", "margin-001", "audit-002"], "mathematical_correction"),
    292: ("P1", "Notes.tex:4442-4444", "corrected_in_translation",
          ["exa-002", "fig-002", "audit-003"], "mathematical_correction"),
    293: ("P1", "Notes.tex:4463-4467", "corrected_in_translation",
          ["def-002", "audit-004"], "mathematical_correction"),
    294: ("P3", "Notes.tex:4379,4403,4414,4451", "corrected_in_translation",
          ["s01", "s02", "s03", "audit-005"], "editorial_correction"),
    295: ("P2", "Notes.tex:4393-4395,4429-4444,4470,4484", "accessibility_reflow",
          [*[f"margin-{n:03d}" for n in range(1, 5)],
           *[f"fig-{n:03d}" for n in range(1, 3)]], "structural_adaptation"),
    296: ("P2", "Notes.tex:4482-4496", "clarified_in_translation",
          ["def-003", "margin-004", "exa-004", "audit-005"], "clarification"),
    297: ("P2", "Unit21 mastery 21.1", "corrected_after_independent_review",
          ["mcheck-001", "sol-001"], "mathematical_correction"),
}
ANCHORS = [
    "o012-rbt-l21-notice", "o012-rbt-l21", "o012-rbt-l21-s01",
    "o012-rbt-l21-rem-001", "o012-rbt-l21-audit-001", "o012-rbt-l21-s02",
    "o012-rbt-l21-constr-001", "o012-rbt-l21-constr-002",
    "o012-rbt-l21-margin-001", "o012-rbt-l21-audit-002",
    "o012-rbt-l21-exa-001", "o012-rbt-l21-s03", "o012-rbt-l21-def-001",
    "o012-rbt-l21-exa-002", "o012-rbt-l21-margin-002",
    "o012-rbt-l21-fig-001", "o012-rbt-l21-fig-002",
    "o012-rbt-l21-audit-003", "o012-rbt-l21-exa-003", "o012-rbt-l21-s04",
    "o012-rbt-l21-def-002", "o012-rbt-l21-audit-004",
    "o012-rbt-l21-margin-003", "o012-rbt-l21-def-003",
    "o012-rbt-l21-margin-004", "o012-rbt-l21-exa-004",
    "o012-rbt-l21-audit-005", "o012-rbt-l21-mastery",
    "o012-rbt-l21-mcheck-001", "o012-rbt-l21-hint-001",
    "o012-rbt-l21-sol-001", "o012-rbt-l21-mcheck-002",
    "o012-rbt-l21-hint-002", "o012-rbt-l21-sol-002",
    "o012-rbt-l21-mcheck-003", "o012-rbt-l21-hint-003",
    "o012-rbt-l21-sol-003", "o012-rbt-l21-mcheck-004",
    "o012-rbt-l21-hint-004", "o012-rbt-l21-sol-004",
    "o012-rbt-l21-mcheck-005", "o012-rbt-l21-hint-005",
    "o012-rbt-l21-sol-005", "o012-rbt-l21-mcheck-006",
    "o012-rbt-l21-hint-006", "o012-rbt-l21-sol-006",
    "o012-rbt-l21-boundary-001",
]
BASE_CONCEPTS = (
    "complex", "coboundary", "euler-characteristic",
    "cohomologically-graded-complex", "geometric-realisation",
    "standard-n-simplex", "triangulation",
)

def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()

def canon(obj: dict[str, Any]) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8") + b"\n"

def common(kind: str, ident: str) -> dict[str, Any]:
    return {"entity_type": kind, "id": ident, "schema": SCHEMA,
            "schema_version": VERSION, "status": "active", "supersedes": None,
            "timestamp": STAMP, "workflow": WORKFLOW}

def load_backend() -> tuple[dict[str, dict[str, dict[str, Any]]], dict[str, bytes]]:
    tables: dict[str, dict[str, dict[str, Any]]] = {}
    raw_files: dict[str, bytes] = {}
    for name in FILES:
        raw = (BACKEND / name).read_bytes()
        raw_files[name] = raw
        count, size, expected_sha = PREFIX[name]
        if len(raw) != size or digest(raw) != expected_sha:
            raise SystemExit(f"{name}: immutable Units 001-020 prefix mismatch")
        lines = raw.splitlines(keepends=True)
        if len(lines) != count or b"\r" in raw or not raw.endswith(b"\n"):
            raise SystemExit(f"{name}: prefix count/newline mismatch")
        table: dict[str, dict[str, Any]] = {}
        for number, line in enumerate(lines, 1):
            obj = json.loads(line.decode("utf-8"))
            if not isinstance(obj.get("id"), str) or obj["id"] in table:
                raise SystemExit(f"{name}:{number}: invalid/duplicate ID")
            if canon(obj) != line:
                raise SystemExit(f"{name}:{number}: noncanonical prefix record")
            table[obj["id"]] = obj
        tables[name] = table
    h = hashlib.sha256()
    for name in FILES:
        h.update(name.encode()); h.update(b"\0"); h.update(raw_files[name])
    if h.hexdigest() != "7abd10e468c5f8b75853a67fcfb67d09f0470720fa88efcc84f5c3647cbb1fe5":
        raise SystemExit("Units 001-020 backend bundle identity mismatch")
    return tables, raw_files

def div_spans(lines: list[str]) -> dict[str, tuple[int, int, str]]:
    stack: list[tuple[str, int, str]] = []
    spans: dict[str, tuple[int, int, str]] = {}
    opening = re.compile(
        r"^:::\s+\{[^#]*#(o012-rbt-l21(?:-[A-Za-z0-9-]+)?)(.*)\}\s*$")
    for number, line in enumerate(lines, 1):
        match = opening.match(line)
        if match:
            stack.append((match.group(1), number, line))
        elif line.strip() == ":::":
            if not stack:
                raise SystemExit(f"unexpected div close at source line {number}")
            ident, start, opener = stack.pop()
            if ident in spans:
                raise SystemExit(f"duplicate div anchor: {ident}")
            spans[ident] = (start, number, opener)
    if stack:
        raise SystemExit(f"unclosed div anchors: {[x[0] for x in stack]}")
    return spans

def unit_kind(ident: str, opener: str) -> str:
    if ident.endswith("-notice"): return "notice"
    if ident == "o012-rbt-l21": return "lecture"
    if ident.endswith("-mastery"): return "mastery_section"
    if re.fullmatch(r"o012-rbt-l21-s\d{2}", ident): return "section"
    if ident.endswith("-boundary-001"): return "boundary"
    if "-mcheck-" in ident: return "exercise"
    if "-hint-" in ident: return "hint"
    if "-sol-" in ident: return "solution"
    match = re.search(r"\{\.([A-Za-z][A-Za-z0-9_-]*)", opener)
    class_name = match.group(1) if match else ""
    kinds = {
        "remark": "remark", "source-audit": "source_audit",
        "construction": "construction", "source-margin": "source_margin",
        "example": "example", "definition": "definition", "figure": "figure",
        "exercise": "exercise", "hint": "hint", "solution": "solution",
    }
    if class_name not in kinds:
        raise SystemExit(f"cannot infer kind for {ident}: {class_name!r}")
    return kinds[class_name]

def is_original(ident: str, kind: str) -> bool:
    return (kind in {"notice", "source_audit", "mastery_section", "boundary",
                     "hint", "solution"}
            or "-mcheck-" in ident)

def target_locator(path: str, start: int, end: int,
                   file_sha: str, raw_lines: list[bytes]) -> dict[str, Any]:
    return {"content_sha256": digest(b"".join(raw_lines[start - 1:end])),
            "file_sha256": file_sha, "line_end": end, "line_start": start,
            "path": path}

def source_locator(original: bool) -> dict[str, Any]:
    if original:
        return {"kind": "edition_original",
                "path": "source/id-ID/units/unit-021-lecture-021.md",
                "precision": "exact_target_span"}
    return {"commit_sha": COMMIT, "line_end": 4500, "line_start": 4346,
            "path": "Notes.tex", "precision": "unit_range_only"}

def display_title(ident: str, lines: list[str], start: int, kind: str) -> str:
    first = lines[start - 1].strip()
    if first.startswith("#"):
        return re.sub(r"\s*\{.*\}$", "",
                      re.sub(r"^#+\s*", "", first)).strip()
    for line in lines[start:min(start + 5, len(lines))]:
        text = line.strip().replace("**", "")
        if text and not text.startswith(":::"):
            return text[:180]
    return f"Unit 21 {kind} {ident.rsplit('-', 1)[-1]}"

def main() -> None:
    tables, prefix_raw = load_backend()
    existing_ids = {ident for table in tables.values() for ident in table}
    additions: dict[str, dict[str, dict[str, Any]]] = {name: {} for name in FILES}
    def add(name: str, obj: dict[str, Any]) -> None:
        ident = obj["id"]
        if (ident in existing_ids or ident in additions[name]
                or any(ident in table for table in additions.values())):
            raise SystemExit(f"duplicate new ID: {ident}")
        additions[name][ident] = obj

    raw = SOURCE.read_bytes()
    if len(raw) != SOURCE_BYTES or digest(raw) != SOURCE_SHA or b"\r" in raw:
        raise SystemExit(f"Unit 21 identity mismatch: {len(raw)} {digest(raw)}")
    raw_lines = raw.splitlines(keepends=True)
    lines = [line.decode("utf-8").rstrip("\n") for line in raw_lines]
    if len(lines) != SOURCE_LINES:
        raise SystemExit("Unit 21 line count mismatch")
    spans = div_spans(lines)
    structural: dict[str, tuple[int, int, str]] = dict(spans)
    structural.update({
        "o012-rbt-l21-notice": (12, 52, lines[11]),
        "o012-rbt-l21": (54, 470, lines[53]),
        "o012-rbt-l21-s01": (56, 120, lines[55]),
        "o012-rbt-l21-s02": (122, 238, lines[121]),
        "o012-rbt-l21-s03": (240, 355, lines[239]),
        "o012-rbt-l21-s04": (357, 470, lines[356]),
        "o012-rbt-l21-mastery": (472, 779, lines[471]),
    })
    if set(structural) != set(ANCHORS) or len(structural) != 47:
        raise SystemExit(
            f"stable-ID closure mismatch: {len(structural)} / {sorted(set(ANCHORS)-set(structural))}")
    if len(set(ANCHORS)) != 47:
        raise SystemExit("expected anchor list is not unique")

    # Add only genuinely new locale-neutral concepts.
    for control, (source_term, _preferred, slug, _evidence, domain) in TERM_SPECS.items():
        ident = f"concept:{slug}"
        if ident in existing_ids:
            raise SystemExit(f"{control}: concept unexpectedly pre-exists")
        concept = common("concept", ident)
        concept.update({"canonical_label": source_term, "domain": domain,
                        "locale_neutral": True})
        add("concepts.jsonl", concept)
    concept_ids = [f"concept:{slug}" for slug in BASE_CONCEPTS]
    if any(ident not in existing_ids and ident not in additions["concepts.jsonl"]
           for ident in concept_ids):
        raise SystemExit("Unit 21 concept closure mismatch")

    # Rights are additive; no existing authority or rights line is changed.
    rights_specs = (
        (COMPANION_RIGHTS,
         "Indonesian original mastery, audit, and boundary layer for Roberts Unit 21.",
         "Original additions are CC BY 4.0; source-derived material remains separately attributed.",
         [ROOT], None),
        (COMPOSITE_RIGHTS,
         "David Michael Roberts source adaptation plus original Indonesian Unit 21 companions.",
         "Unit 21 source-derived and original layers remain component-distinguishable.",
         [ROOT], None),
        (CUMULATIVE_RIGHTS,
         "Cumulative Roberts Units 001-021 Indonesian reader source boundary.",
         "Source-stage cumulative pointer; prior Units 001-020 build boundary remains immutable.",
         [f"unit:o012-rbt-u{number:03d}" for number in range(1, 22)],
         PRIOR_RIGHTS),
    )
    for ident, attribution, notice, scope, supersedes in rights_specs:
        right = common("rights", ident)
        right.update({"attribution": attribution, "change_notice": notice,
                      "component_scope": scope, "license_expression": "CC-BY-4.0",
                      "license_url": "https://creativecommons.org/licenses/by/4.0/",
                      "non_endorsement": "Independent edition; no source-author endorsement.",
                      "third_party_status": "Component-scoped rights records control.",
                      "supersedes": supersedes})
        add("rights.jsonl", right)

    section_ranges = (
        ("o012-rbt-l21-s01", 56, 120),
        ("o012-rbt-l21-s02", 122, 238),
        ("o012-rbt-l21-s03", 240, 355),
        ("o012-rbt-l21-s04", 357, 470),
    )
    section_ids = {item[0] for item in section_ranges}
    def parent_local(ident: str, start: int) -> str:
        if ident in {"o012-rbt-l21-notice", "o012-rbt-l21",
                     "o012-rbt-l21-mastery", "o012-rbt-l21-boundary-001"}:
            return ROOT
        if ident in section_ids:
            return LECTURE
        if any(token in ident for token in ("-mcheck-", "-hint-", "-sol-")):
            return MASTERY
        for section, low, high in section_ranges:
            if low <= start <= high:
                return f"unit:{section}"
        raise SystemExit(f"cannot assign Unit 21 parent: {ident}")
    children: defaultdict[str, list[str]] = defaultdict(list)
    for ident in ANCHORS:
        children[parent_local(ident, structural[ident][0])].append(ident)
    order_map = {
        parent: {ident: number for number, ident in enumerate(
            sorted(items, key=lambda item: structural[item][0]), 1)}
        for parent, items in children.items()
    }
    path_by_id: dict[str, list[str]] = {ROOT: [ROOT]}
    root = common("unit", ROOT)
    root.update({
        "concept_ids": concept_ids, "course_id": COURSE,
        "display_title": "Topologi Aljabar - Unit 21: Realisasi Geometrik dan Triangulasi",
        "edition_id": EDITION, "locale": "id-ID", "order": 21,
        "parent_id": COURSE, "path": [ROOT], "program_id": PROGRAM,
        "provenance_relation": "composite_translated_and_original",
        "resource_id": RESOURCE, "rights_component_id": COMPOSITE_RIGHTS,
        "source_local_id": None,
        "target_locator": target_locator(
            "source/id-ID/units/unit-021-lecture-021.md", 1, SOURCE_LINES,
            SOURCE_SHA, raw_lines),
        "translation_state": "structurally_verified", "unit_kind": "reader_unit",
    })
    add("units.jsonl", root)
    for ident in sorted(ANCHORS, key=lambda item: structural[item][0]):
        start, end, opener = structural[ident]
        kind = unit_kind(ident, opener)
        parent_id = parent_local(ident, start)
        if parent_id not in path_by_id:
            raise SystemExit(f"parent path not yet constructed: {ident} -> {parent_id}")
        unit_id = f"unit:{ident}"
        path = path_by_id[parent_id] + [unit_id]
        path_by_id[unit_id] = path
        original = is_original(ident, kind)
        rights_id = COMPANION_RIGHTS if original else ROBERTS_RIGHTS
        locator = target_locator(
            "source/id-ID/units/unit-021-lecture-021.md", start, end,
            SOURCE_SHA, raw_lines)
        unit = common("unit", unit_id)
        unit.update({
            "concept_ids": concept_ids, "course_id": COURSE,
            "display_title": display_title(ident, lines, start, kind),
            "edition_id": EDITION, "locale": "id-ID",
            "order": order_map[parent_id][ident], "parent_id": parent_id,
            "path": path, "program_id": PROGRAM,
            "provenance_relation": (
                "edition_original" if original
                else "translated_adapted_from_upstream"),
            "resource_id": RESOURCE, "rights_component_id": rights_id,
            "source_local_id": ident, "target_locator": locator,
            "translation_state": "structurally_verified", "unit_kind": kind,
        })
        aliases = re.findall(r'data-source-label="([^"]+)"', opener)
        if aliases:
            unit["source_aliases"] = aliases
        add("units.jsonl", unit)
        segment = common("segment", f"segment:{ident}")
        segment.update({
            "concept_ids": concept_ids, "edition_id": EDITION, "locale": "id-ID",
            "order": unit["order"], "provenance_relation": unit["provenance_relation"],
            "resource_id": RESOURCE, "rights_component_id": rights_id,
            "segment_kind": kind, "source_local_id": ident,
            "source_locator": source_locator(original), "target_locator": locator,
            "translation_state": "structurally_verified", "unit_id": unit_id,
        })
        add("segments.jsonl", segment)

    asset = common("asset", "asset:o012-u021-source-markdown")
    asset.update({
        "bytes": SOURCE_BYTES, "edition_id": EDITION,
        "media_type": "text/markdown; charset=utf-8",
        "path": "source/id-ID/units/unit-021-lecture-021.md",
        "resource_id": RESOURCE, "rights_component_id": COMPOSITE_RIGHTS,
        "role": "canonical_reader_source", "sha256": SOURCE_SHA,
    })
    add("assets.jsonl", asset)

    # Terminology controls are exact, and evidence anchors must exist.
    with TERMINOLOGY.open(encoding="utf-8", newline="") as stream:
        term_rows = {row["term_id"]: row for row in csv.DictReader(stream)}
    for control, (source_term, preferred, slug, evidence, _domain) in TERM_SPECS.items():
        row = term_rows.get(control)
        if (not row or row["source_term"] != source_term
                or row["id_ID"] != preferred or row["status"] != "admitted"):
            raise SystemExit(f"terminology control mismatch: {control}")
        if evidence not in structural:
            raise SystemExit(f"terminology evidence anchor absent: {control}")
        term = common("term", f"term:{slug}:id-ID")
        term.update({
            "concept_id": f"concept:{slug}",
            "evidence_segment_id": f"segment:{evidence}", "locale": "id-ID",
            "preferred": preferred, "register": "textbook", "rejected_forms": [],
            "rights_component_id": ROBERTS_RIGHTS, "scope_unit_id": ROOT,
            "source_term": source_term, "terminology_control_id": control,
            "terminology_status": "admitted", "usage_note": row["note"],
            "variants": [],
        })
        add("terms.jsonl", term)

    # Exact adverse rows and evidence-bound target anchors.
    with LEDGER.open(encoding="utf-8", newline="") as stream:
        adverse_rows = {row["event_id"]: row for row in csv.DictReader(stream)}
    for number, (severity, source_location, status, suffixes,
                 correction_type) in EXPECTED_ADVERSE.items():
        event_id = f"O012-ADV-{number:04d}"
        row = adverse_rows.get(event_id)
        if (not row or row["severity"] != severity
                or row["source_location"] != source_location
                or row["status"] != status):
            raise SystemExit(f"adverse control mismatch: {event_id}")
        local_targets = [f"o012-rbt-l21-{suffix}" for suffix in suffixes]
        if any(target not in structural for target in local_targets):
            raise SystemExit(f"adverse target absent: {event_id}")
        correction = common(
            "correction", f"correction:o012-u021-adv-{number:04d}")
        correction.update({
            "adverse_ledger_id": event_id,
            "affected_unit_ids": [f"unit:{target}" for target in local_targets],
            "correction_type": correction_type, "edition_id": EDITION,
            "evidence": source_location,
            "evidence_segment_id": "segment:o012-rbt-l21-notice",
            "severity": severity, "rationale": row["rationale"],
            "resource_id": RESOURCE, "source_defect": row["observed"],
            "target_change": row["action"], "unit_id": ROOT,
            "upstream_report_disposition": "not_contacted",
        })
        add("corrections.jsonl", correction)

    # Exact review/audit/QA/handoff artifacts.
    for ident, (relative, size, expected_sha, media_type, state,
                qa_ids) in ARTIFACTS.items():
        artifact_raw = (LANE / relative).read_bytes()
        if len(artifact_raw) != size or digest(artifact_raw) != expected_sha:
            raise SystemExit(f"evidence identity mismatch: {relative}")
        artifact = common("artifact", ident)
        artifact.update({
            "bytes": size, "locale": "id-ID", "manifest_artifact_id": None,
            "media_type": media_type, "path": relative, "qa_event_ids": qa_ids,
            "rights_component_id": COMPOSITE_RIGHTS, "sha256": expected_sha,
            "toolchain": (
                f"Bounded Unit 21 evidence; Notes.tex:4346-4500 span "
                f"{UPSTREAM_SPAN_SHA}; no build/publication assertion."),
            "translation_state": state, "unit_id": ROOT,
        })
        add("artifacts.jsonl", artifact)
    qa_specs = (
        ("qa:o012-u021-source-integrity", "source",
         "Unit 21 exact reader/source identities, 47 stable IDs, source census, terminology, adverse closure, and Pandoc structure passed.",
         ["artifact:o012-u021-source-audit", "artifact:o012-u021-qa",
          "artifact:o012-u021-translation-handoff"]),
        ("qa:o012-u021-math", "math",
         "Independent Unit 21 mathematical review passed with no open P1, P2, or P3 finding.",
         ["artifact:o012-u021-independent-review"]),
        ("qa:o012-u021-language", "language",
         "Independent Indonesian language, terminology, attribution, and accessibility review passed.",
         ["artifact:o012-u021-independent-review",
          "artifact:o012-u021-translation-handoff"]),
    )
    for ident, qa_type, note, witnesses in qa_specs:
        event = common("qa_event", ident)
        event.update({"note": note, "qa_type": qa_type, "result": "passed",
                      "unit_id": ROOT, "witness_artifact_ids": witnesses})
        add("qa.jsonl", event)

    # Route, source-label, and mastery relations.
    def relation(ident: str, source_id: str, relation_type: str,
                 target_id: str, note: str) -> None:
        item = common("relation", ident)
        item.update({"from_id": source_id, "note": note,
                     "relation_type": relation_type, "to_id": target_id})
        add("relations.jsonl", item)
    relation("relation:adapts:o012-rbt-u021:edition", ROOT, "adapts", EDITION,
             "Unit 21 is the Indonesian adapted reader boundary for the frozen Roberts edition.")
    relation("relation:precedes:o012-rbt-u020:o012-rbt-u021",
             "unit:o012-rbt-u020", "precedes", ROOT,
             "Preserves contiguous Roberts lecture-unit order.")
    relation("relation:precedes:o012-rbt-l21:mastery", LECTURE, "precedes",
             MASTERY, "Lecture content precedes the Unit 21 mastery companion.")
    relation("relation:boundary:o012-u021", CUMULATIVE_RIGHTS, "contains", ROOT,
             "Additive cumulative Units 001-021 source boundary; prior build boundary retained.")
    relation("relation:xref:o012-rbt-l21-exa-001:eg-join-interval-geom-real",
             "unit:o012-rbt-l21-exa-001", "xref", EDITION,
             "Preserves upstream source label eg:join_interval_geom_real.")
    for number in range(1, 7):
        relation(
            f"relation:solves:l21-sol-{number:03d}:l21-mcheck-{number:03d}",
            f"unit:o012-rbt-l21-sol-{number:03d}", "solves",
            f"unit:o012-rbt-l21-mcheck-{number:03d}",
            f"Complete solution for Unit 21 mastery check {number}.")
        relation(
            f"relation:hints:l21-hint-{number:03d}:l21-mcheck-{number:03d}",
            f"unit:o012-rbt-l21-hint-{number:03d}", "hints",
            f"unit:o012-rbt-l21-mcheck-{number:03d}",
            f"Bounded hint for Unit 21 mastery check {number}.")

    # Referential integrity and Unit 21-specific hierarchy/mastery checks.
    merged = {name: dict(tables[name]) for name in FILES}
    for name in FILES:
        merged[name].update(additions[name])
    by_id = {ident: obj for table in merged.values() for ident, obj in table.items()}
    if len(by_id) != sum(len(table) for table in merged.values()):
        raise SystemExit("global duplicate backend IDs")
    scalar_refs = {
        "concept_id", "course_id", "edition_id", "evidence_segment_id",
        "from_id", "manifest_artifact_id", "parent_id", "program_id",
        "resource_id", "rights_component_id", "scope_unit_id", "to_id",
        "unit_id", "supersedes",
    }
    list_refs = {
        "affected_unit_ids", "component_scope", "concept_ids",
        "local_derivative_unit_ids", "qa_event_ids", "witness_artifact_ids",
    }
    for ident, obj in by_id.items():
        for field in scalar_refs:
            value = obj.get(field)
            if value is not None and value not in by_id:
                raise SystemExit(f"unknown reference {ident}.{field}={value}")
        for field in list_refs:
            if field in obj and any(value not in by_id for value in obj[field]):
                raise SystemExit(f"unknown list reference {ident}.{field}")
    for ident in ANCHORS:
        unit = by_id[f"unit:{ident}"]
        segment = by_id[f"segment:{ident}"]
        if unit["target_locator"] != segment["target_locator"]:
            raise SystemExit(f"unit/segment locator mismatch: {ident}")
        if unit["path"][-1] != unit["id"]:
            raise SystemExit(f"noncanonical Unit 21 path: {ident}")
        if unit["parent_id"].startswith("unit:"):
            parent = by_id[unit["parent_id"]]
            if unit["path"][:-1] != parent["path"]:
                raise SystemExit(f"Unit 21 parent path mismatch: {ident}")
    sibling_orders: defaultdict[str, list[int]] = defaultdict(list)
    for obj in additions["units.jsonl"].values():
        sibling_orders[obj["parent_id"]].append(obj["order"])
    if any(len(values) != len(set(values)) for values in sibling_orders.values()):
        raise SystemExit("duplicate Unit 21 sibling order")
    for number in range(1, 7):
        check = f"unit:o012-rbt-l21-mcheck-{number:03d}"
        solution = f"unit:o012-rbt-l21-sol-{number:03d}"
        hint = f"unit:o012-rbt-l21-hint-{number:03d}"
        solves = [obj for obj in additions["relations.jsonl"].values()
                  if obj["relation_type"] == "solves" and obj["to_id"] == check]
        hints = [obj for obj in additions["relations.jsonl"].values()
                 if obj["relation_type"] == "hints" and obj["to_id"] == check]
        if len(solves) != 1 or solves[0]["from_id"] != solution:
            raise SystemExit(f"mastery solution closure mismatch: {number}")
        if len(hints) != 1 or hints[0]["from_id"] != hint:
            raise SystemExit(f"mastery hint closure mismatch: {number}")
    correction_ids = {
        obj.get("adverse_ledger_id")
        for obj in additions["corrections.jsonl"].values()
    }
    if correction_ids != {f"O012-ADV-{number:04d}" for number in range(290, 298)}:
        raise SystemExit("Unit 21 adverse closure mismatch")
    if additions["rights.jsonl"][CUMULATIVE_RIGHTS]["component_scope"] != [
            f"unit:o012-rbt-u{number:03d}" for number in range(1, 22)]:
        raise SystemExit("Unit 21 cumulative rights scope mismatch")

    # Append canonical sorted batches only after every check passes.
    output: dict[str, bytes] = {}
    for name in FILES:
        if (BACKEND / name).read_bytes() != prefix_raw[name]:
            raise SystemExit(f"{name}: prefix changed before write")
        suffix = b"".join(
            canon(additions[name][ident]) for ident in sorted(additions[name]))
        output[name] = prefix_raw[name] + suffix
    for name, generated in output.items():
        (BACKEND / name).write_bytes(generated)
    bundle = hashlib.sha256()
    for name in FILES:
        bundle.update(name.encode()); bundle.update(b"\0"); bundle.update(output[name])
    counts = {name: len(additions[name]) for name in FILES}
    print("Unit 021 backend extension: PASS")
    print("new_records_by_file=" + json.dumps(counts, sort_keys=True))
    print(f"new_records={sum(counts.values())}")
    print(f"backend_bytes={sum(len(raw) for raw in output.values())}")
    print(f"backend_bundle_sha256={bundle.hexdigest()}")
    print(f"source_sha256={SOURCE_SHA}")
    print(f"upstream_span_sha256={UPSTREAM_SPAN_SHA}")
    print(f"upstream_raw_sha256={UPSTREAM_RAW_SHA}")

if __name__ == "__main__":
    main()
