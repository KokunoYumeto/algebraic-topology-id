#!/usr/bin/env python3
"""Fail-closed, append-only backend extension for Roberts Unit 020.

The producer validates the frozen reader, control rows, and evidence files
before writing.  Existing JSONL bytes are never re-serialized or rewritten;
new canonical records are appended only.  No build or publication claim is
created here.
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
SOURCE = LANE / "source/id-ID/units/unit-020-lecture-020.md"
LEDGER = LANE / "00_control/ADVERSE_LEDGER.csv"
TERMS = LANE / "00_control/TERMINOLOGY.csv"
TIMESTAMP = "2026-08-23T00:00:00Z"
SCHEMA = "curriculum.interop"
VERSION = "0.1.0"
WORKFLOW = "o012-d60-id-reader-production"
PROGRAM = "program:o012-id"
COURSE = "course:o012-d60"
RESOURCE = "resource:roberts-algebraic-topology-2019"
EDITION = "edition:roberts-at-2019-b947ad2"
ROBERTS_RIGHTS = "rights:roberts-cc-by-4.0"
COMPANION_RIGHTS = "rights:o012-u020-companion-cc-by-4.0"
COMPOSITE_RIGHTS = "rights:o012-u020-composite-cc-by-4.0"
CUMULATIVE_RIGHTS = "rights:o012-units-001-020-composite-cc-by-4.0"
COMMIT = "b947ad2e9f9e301bfe24590a9db653bc54fa1a53"
SOURCE_BYTES = 45782
SOURCE_LINES = 1425
SOURCE_SHA = "cda9ba7d3651feb45a4fa9b595a29772d86ef2c8dc5a5b799489b76b14032595"
UPSTREAM_ACTIVE_SHA = "1fa7d0ea4ecd567ae8975da5b9b41495a1757913942102f223d1234168366e88"
UPSTREAM_RAW_SHA = "6af488776f936d7a3ef17a30a8af94e6955df91e3a3057b92b048e1b38ca1917"
JSONL = ("artifacts.jsonl", "assets.jsonl", "authority.jsonl", "concepts.jsonl",
         "corrections.jsonl", "qa.jsonl", "relations.jsonl", "rights.jsonl",
         "segments.jsonl", "terms.jsonl", "units.jsonl")
ROOT = "unit:o012-rbt-u020"
LECTURE = "unit:o012-rbt-l20"
BASE_CONCEPTS = ["complex", "directed-graph", "chain-complex", "coboundary",
                 "kernel", "cokernel", "euler-characteristic", "functoriality",
                 "finite-set", "cohomologically-graded-complex",
                 "morphism-of-complexes"]
ANCHORS = [
    "o012-rbt-l20", "o012-rbt-l20-notice", "o012-rbt-l20-s01",
    "o012-rbt-l20-exa-001", "o012-rbt-l20-exa-002", "o012-rbt-l20-audit-001",
    "o012-rbt-l20-rem-001", "o012-rbt-l20-exa-003", "o012-rbt-l20-margin-001",
    "o012-rbt-l20-fig-001", "o012-rbt-l20-audit-002", "o012-rbt-l20-exa-004",
    "o012-rbt-l20-margin-002", "o012-rbt-l20-fig-002", "o012-rbt-l20-ex-001",
    "o012-rbt-l20-ex-002", "o012-rbt-l20-audit-003", "o012-rbt-l20-audit-004",
    "o012-rbt-l20-rem-002", "o012-rbt-l20-margin-003", "o012-rbt-l20-fig-003",
    "o012-rbt-l20-s02", "o012-rbt-l20-margin-004", "o012-rbt-l20-exa-005",
    "o012-rbt-l20-margin-005", "o012-rbt-l20-fig-004", "o012-rbt-l20-def-001",
    "o012-rbt-l20-margin-006", "o012-rbt-l20-margin-007", "o012-rbt-l20-margin-008",
    "o012-rbt-l20-fig-005", "o012-rbt-l20-exa-006", "o012-rbt-l20-exa-007",
    "o012-rbt-l20-fig-006", "o012-rbt-l20-audit-005", "o012-rbt-l20-margin-009",
    "o012-rbt-l20-rem-003", "o012-rbt-l20-exa-008", "o012-rbt-l20-lem-001",
    "o012-rbt-l20-proof-001", "o012-rbt-l20-margin-010", "o012-rbt-l20-rem-004",
    "o012-rbt-l20-ex-003", "o012-rbt-l20-ex-004", "o012-rbt-l20-fig-007",
    "o012-rbt-l20-margin-011", "o012-rbt-l20-audit-006", "o012-rbt-l20-audit-007",
    "o012-rbt-l20-def-002", "o012-rbt-l20-audit-008", "o012-rbt-l20-lem-002",
    "o012-rbt-l20-proof-002", "o012-rbt-l20-s04", "o012-rbt-l20-mastery",
    "o012-rbt-l20-mcheck-001", "o012-rbt-l20-hint-001", "o012-rbt-l20-sol-001",
    "o012-rbt-l20-mcheck-002", "o012-rbt-l20-hint-002", "o012-rbt-l20-sol-002",
    "o012-rbt-l20-mcheck-003", "o012-rbt-l20-hint-003", "o012-rbt-l20-sol-003",
    "o012-rbt-l20-mcheck-004", "o012-rbt-l20-hint-004", "o012-rbt-l20-sol-004",
    "o012-rbt-l20-mcheck-005", "o012-rbt-l20-hint-005", "o012-rbt-l20-sol-005",
    "o012-rbt-l20-mcheck-006", "o012-rbt-l20-hint-006", "o012-rbt-l20-sol-006",
    "o012-rbt-l20-boundary-001",
]
TARGETS = {
    279: ["exa-002", "audit-001"],
    280: ["exa-003", "audit-002"],
    281: ["rem-001", "ex-001", "ex-002", "audit-003", "audit-004", "rem-002"],
    282: ["def-001", "proof-001", "audit-005"],
    283: ["ex-004", "fig-007", "audit-006", "sol-005"],
    284: ["def-002", "lem-002", "proof-002", "audit-008", "sol-006"],
    285: ["s01", "s02", "s04", "audit-007"],
    286: [f"fig-{n:03d}" for n in range(1, 8)] + [f"margin-{n:03d}" for n in range(1, 12)],
    287: ["mcheck-001", "mcheck-002", "mcheck-006"],
}
EXPECTED_EVENT = {
    279: ("P1", "corrected_in_translation", "Notes.tex:3974-3981"),
    280: ("P3", "corrected_in_translation", "Notes.tex:4004"),
    281: ("P1", "clarified_in_translation", "Notes.tex:4040-4057"),
    282: ("P1", "proof_completed_in_translation", "Notes.tex:4228-4251"),
    283: ("P1", "corrected_in_translation", "Notes.tex:4305"),
    284: ("P1", "proof_completed_in_translation", "Notes.tex:4273,4311-4340"),
    285: ("P3", "corrected_in_translation", "Notes.tex:4040-4341"),
    286: ("P2", "accessibility_reflow", "Notes.tex:3990-4278"),
    287: ("P3", "corrected_after_independent_review", "Notes.tex:4280-4340"),
}
ARTIFACTS = {
    "artifact:o012-u020-independent-review": ("qa/UNIT_020_INDEPENDENT_REVIEW.md", 2521, "e01dfdfbdcacf232086c2bee06eed2efc93fd71af56cdfb6798dc15514c73e19", "text/markdown; charset=utf-8", "mathematically_reviewed"),
    "artifact:o012-u020-source-audit": ("qa/UNIT_020_SOURCE_AUDIT.md", 3099, "da7b9b7d8129d43d4d264bf3a040b1c7da851ca1bf6a83512c884e76cf35276d", "text/markdown; charset=utf-8", "source_frozen"),
    "artifact:o012-u020-qa": ("qa/UNIT_020_QA.json", 3717, "d3785ba5b3bc77ee6bab1b926a9dba290c2b4a6ab1e6a416e29a90270533f736", "application/json", "built"),
    "artifact:o012-u020-translation-handoff": ("qa/UNIT_020_TRANSLATION_HANDOFF.md", 1778, "0668e42373924fa5a605c38ecd846216261c9793bfc91f9cc16669ca73be9fde", "text/markdown; charset=utf-8", "source_frozen"),
}

def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()

def canon(obj: dict[str, Any]) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8") + b"\n"

def common(kind: str, ident: str) -> dict[str, Any]:
    return {"entity_type": kind, "id": ident, "schema": SCHEMA, "schema_version": VERSION,
            "status": "active", "supersedes": None, "timestamp": TIMESTAMP, "workflow": WORKFLOW}

def load_backend() -> tuple[dict[str, dict[str, dict[str, Any]]], dict[str, dict[str, bytes]]]:
    recs: dict[str, dict[str, dict[str, Any]]] = {}
    old: dict[str, dict[str, bytes]] = {}
    for name in JSONL:
        raw = (BACKEND / name).read_bytes()
        if b"\r" in raw or not raw.endswith(b"\n"):
            raise SystemExit(f"{name}: non-LF or unterminated historical JSONL")
        table: dict[str, dict[str, Any]] = {}
        lines: dict[str, bytes] = {}
        for number, line in enumerate(raw.splitlines(keepends=True), 1):
            obj = json.loads(line.decode("utf-8"))
            ident = obj.get("id")
            if not isinstance(ident, str) or ident in table:
                raise SystemExit(f"{name}:{number}: duplicate/missing id")
            if canon(obj) != line:
                raise SystemExit(f"{name}:{number}: historical line is not canonical")
            table[ident] = obj
            lines[ident] = line
        recs[name] = table
        old[name] = lines
    return recs, old

def block_spans(lines: list[str]) -> dict[str, tuple[int, int, str]]:
    stack: list[tuple[str, int, str]] = []
    spans: dict[str, tuple[int, int, str]] = {}
    opening = re.compile(r"^:::\s+\{[^#]*#(o012-rbt-l20(?:-[A-Za-z0-9-]+)?)(.*)\}\s*$")
    for n, line in enumerate(lines, 1):
        m = opening.match(line)
        if m:
            stack.append((m.group(1), n, line))
        elif line.strip() == ":::":
            if not stack:
                raise SystemExit(f"unexpected div close at line {n}")
            ident, start, opener = stack.pop()
            if ident in spans:
                raise SystemExit(f"duplicate block anchor {ident}")
            spans[ident] = (start, n, opener)
    if stack:
        raise SystemExit(f"unclosed divs: {[x[0] for x in stack]}")
    return spans

def kind_for(ident: str, opener: str = "") -> str:
    if ident.endswith("-notice"): return "notice"
    if ident == "o012-rbt-l20": return "lecture"
    if ident.endswith("-mastery"): return "mastery_section"
    if re.fullmatch(r"o012-rbt-l20-s\d{2}", ident): return "section"
    if ident.endswith("-boundary-001"): return "boundary"
    if "-mcheck-" in ident: return "exercise"
    if "-hint-" in ident: return "hint"
    if "-sol-" in ident: return "solution"
    m = re.search(r"\{\.([A-Za-z][A-Za-z0-9_-]*)", opener)
    return {"example": "example", "exercise": "exercise", "definition": "definition",
            "lemma": "lemma", "proof": "proof", "remark": "remark",
            "figure": "figure", "source-audit": "source_audit",
            "source-margin": "source_margin"}.get(m.group(1) if m else "", "source_audit")

def original(ident: str, kind: str) -> bool:
    return (kind in {"notice", "boundary", "mastery_section", "source_audit", "source_margin",
                     "figure", "proof", "hint", "solution"} or "-mcheck-" in ident)

def locator(path: str, start: int, end: int, file_sha: str, lines: list[bytes]) -> dict[str, Any]:
    return {"content_sha256": sha(b"".join(lines[start-1:end])), "file_sha256": file_sha,
            "line_end": end, "line_start": start, "path": path}

def source_locator(is_orig: bool) -> dict[str, Any]:
    if is_orig:
        return {"kind": "edition_original", "path": "source/id-ID/units/unit-020-lecture-020.md", "precision": "exact_target_span"}
    return {"commit_sha": COMMIT, "line_end": 4345, "line_start": 3948, "path": "Notes.tex", "precision": "unit_range_only"}

def title_for(ident: str, lines: list[str], start: int, kind: str) -> str:
    line = lines[start-1].strip()
    if line.startswith("#"):
        return re.sub(r"\s*\{.*\}$", "", re.sub(r"^#+\s*", "", line)).strip()
    for text in lines[start: min(start + 4, len(lines))]:
        text = text.strip()
        if text and not text.startswith(":::"):
            return text[:180]
    return f"Unit 20 {kind} {ident.rsplit('-', 1)[-1]}"

def build() -> None:
    recs, old = load_backend()
    all_ids = {ident for table in recs.values() for ident in table}
    new: dict[str, dict[str, dict[str, Any]]] = {name: {} for name in JSONL}
    def add(name: str, obj: dict[str, Any]) -> None:
        ident = obj["id"]
        if ident in all_ids or ident in new[name] or any(ident in t for t in new.values()):
            raise SystemExit(f"duplicate new backend id: {ident}")
        new[name][ident] = obj
    raw = SOURCE.read_bytes()
    if len(raw) != SOURCE_BYTES or sha(raw) != SOURCE_SHA or b"\r" in raw:
        raise SystemExit(f"Unit20 reader identity mismatch: {len(raw)} bytes {sha(raw)}")
    lines_b = raw.splitlines(keepends=True)
    lines = [x.decode("utf-8").rstrip("\n") for x in lines_b]
    if len(lines) != SOURCE_LINES:
        raise SystemExit("Unit20 line count mismatch")
    spans = block_spans(lines)
    heading = {
        "o012-rbt-l20-notice": (12, 64, "# Tentang unit ini {.unnumbered #o012-rbt-l20-notice}"),
        "o012-rbt-l20": (65, 950, "# Kuliah 20 {#o012-rbt-l20}"),
        "o012-rbt-l20-s01": (67, 391, "## Contoh konkret kompleks graf {#o012-rbt-l20-s01}"),
        "o012-rbt-l20-s02": (394, 924, "## Permukaan kombinatorik dan kompleks dua dimensi {#o012-rbt-l20-s02}"),
        "o012-rbt-l20-s04": (926, 950, "## Dari ruang ke kompleks: gagasan besar dan batas unit {#o012-rbt-l20-s04}"),
        "o012-rbt-l20-mastery": (952, 1417, "# Pendamping penguasaan: pemeriksaan, petunjuk, dan solusi lengkap {.unnumbered #o012-rbt-l20-mastery}"),
        "o012-rbt-l20-boundary-001": spans["o012-rbt-l20-boundary-001"],
    }
    for ident, (start, end, opener) in spans.items():
        heading[ident] = (start, end, opener)
    if set(ANCHORS) != set(heading):
        raise SystemExit(f"stable anchor closure mismatch: expected {len(ANCHORS)}, got {len(heading)}")
    # Ensure all existing concept references used below exist; add only the two
    # terminology concepts that are absent from the historical corpus.
    concepts = recs["concepts.jsonl"]
    for slug, label in (("isomorphism", "isomorphism"), ("homomorphism", "homomorphism")):
        ident = f"concept:{slug}"
        if ident not in all_ids:
            c = common("concept", ident)
            c.update({"canonical_label": label, "domain": "algebra", "locale_neutral": True})
            add("concepts.jsonl", c)
    concept_ids = [f"concept:{x}" for x in BASE_CONCEPTS] + ["concept:isomorphism", "concept:homomorphism"]
    if any(x not in all_ids and x not in new["concepts.jsonl"] for x in concept_ids):
        raise SystemExit("missing base concept")
    # Rights are additive; prior 001-019 rights and authority pointers are
    # deliberately untouched.
    for ident, attribution, notice, scope in (
        (COMPANION_RIGHTS, "Indonesian original mastery, accessibility, and audit layer for Roberts Unit 20.", "Original additions are CC BY 4.0; source component remains separately attributed.", [ROOT]),
        (COMPOSITE_RIGHTS, "David Michael Roberts source adaptation plus original Indonesian Unit 20 companions.", "Unit 20 source and original layers remain component-distinguishable.", [ROOT]),
        (CUMULATIVE_RIGHTS, "Cumulative Roberts Units 001-020 Indonesian reader boundary.", "New cumulative pointer only; prior component records remain controlling.", [f"unit:o012-rbt-u{n:03d}" for n in range(1, 21)]),
    ):
        r = common("rights", ident)
        r.update({"attribution": attribution, "change_notice": notice, "component_scope": scope,
                  "license_expression": "CC-BY-4.0", "license_url": "https://creativecommons.org/licenses/by/4.0/",
                  "non_endorsement": "Independent edition; no source-author endorsement.",
                  "third_party_status": "Component-scoped rights records control."})
        add("rights.jsonl", r)
    # Root and all 73 stable anchors.
    section_ranges = [("o012-rbt-l20-s01", 67, 391), ("o012-rbt-l20-s02", 394, 924), ("o012-rbt-l20-s04", 926, 950)]
    section_ids = {x[0] for x in section_ranges}
    def parent_for(ident: str, start: int) -> str:
        if ident == "o012-rbt-l20": return ROOT
        if ident in {"o012-rbt-l20-notice", "o012-rbt-l20-mastery", "o012-rbt-l20-boundary-001"}: return ROOT
        if ident in section_ids: return LECTURE
        if ident.startswith("o012-rbt-l20-mcheck-") or ident.startswith("o012-rbt-l20-hint-") or ident.startswith("o012-rbt-l20-sol-"):
            return "unit:o012-rbt-l20-mastery"
        for sid, lo, hi in section_ranges:
            if lo <= start <= hi: return f"unit:{sid}"
        raise SystemExit(f"cannot assign parent for {ident}")
    # Child order is source order within each parent, preventing duplicate
    # sibling order values without changing historical records.
    children: defaultdict[str, list[str]] = defaultdict(list)
    for ident in ANCHORS:
        if ident == "o012-rbt-l20": continue
        children[parent_for(ident, heading[ident][0])].append(ident)
    order_map = {p: {x: i + 1 for i, x in enumerate(sorted(xs, key=lambda z: heading[z][0]))} for p, xs in children.items()}
    root_record = common("unit", ROOT)
    root_record.update({"concept_ids": concept_ids, "course_id": COURSE, "display_title": "Topologi Aljabar - Unit 20: Kompleks Kombinatorik dan Kohomologi",
                        "edition_id": EDITION, "locale": "id-ID", "order": 20, "parent_id": COURSE,
                        "path": [ROOT], "program_id": PROGRAM, "provenance_relation": "composite_translated_and_original",
                        "resource_id": RESOURCE, "rights_component_id": COMPOSITE_RIGHTS, "source_local_id": None,
                        "target_locator": locator("source/id-ID/units/unit-020-lecture-020.md", 1, SOURCE_LINES, SOURCE_SHA, lines_b),
                        "translation_state": "structurally_verified", "unit_kind": "reader_unit"})
    add("units.jsonl", root_record)
    for ident in ANCHORS:
        start, end, opener = heading[ident]
        k = kind_for(ident, opener)
        parent = parent_for(ident, start)
        pid = parent if parent.startswith("unit:") else parent
        parent_path = [ROOT] if pid == ROOT else None
        if parent_path is None:
            # all non-root parents are newly created and have a deterministic
            # path obtainable from their role.
            if pid == LECTURE: parent_path = [ROOT, LECTURE[5:]]
            elif pid == "unit:o012-rbt-l20-mastery": parent_path = [ROOT, LECTURE[5:], "o012-rbt-l20-mastery"]
            else: parent_path = [ROOT, LECTURE[5:], pid[5:]]
        local = ident
        uid = f"unit:{local}"
        is_orig = original(local, k)
        rights = COMPANION_RIGHTS if is_orig else ROBERTS_RIGHTS
        path = parent_path + [local]
        target = locator("source/id-ID/units/unit-020-lecture-020.md", start, end, SOURCE_SHA, lines_b)
        u = common("unit", uid)
        u.update({"concept_ids": concept_ids, "course_id": COURSE, "display_title": title_for(local, lines, start, k),
                  "edition_id": EDITION, "locale": "id-ID", "order": 2 if local == "o012-rbt-l20" else order_map[parent][local],
                  "parent_id": parent, "path": path, "program_id": PROGRAM,
                  "provenance_relation": "edition_original" if is_orig else "translated_adapted_from_upstream",
                  "resource_id": RESOURCE, "rights_component_id": rights, "source_local_id": local,
                  "target_locator": target, "translation_state": "structurally_verified",
                  "unit_kind": k})
        # Preserve upstream data labels for later source cross-reference.
        aliases = re.findall(r'data-(?:source-(?:ref|label)|source-environment)="([^"]+)"', opener)
        if aliases: u["source_aliases"] = aliases
        add("units.jsonl", u)
        s = common("segment", f"segment:{local}")
        s.update({"concept_ids": concept_ids, "edition_id": EDITION, "locale": "id-ID",
                  "order": u["order"], "provenance_relation": "edition_original" if is_orig else "translated_adapted_from_upstream",
                  "resource_id": RESOURCE, "rights_component_id": rights, "segment_kind": k,
                  "source_local_id": local, "source_locator": source_locator(is_orig), "target_locator": target,
                  "translation_state": "structurally_verified", "unit_id": uid})
        add("segments.jsonl", s)
    # Canonical source asset.
    a = common("asset", "asset:o012-u020-source-markdown")
    a.update({"bytes": SOURCE_BYTES, "edition_id": EDITION, "media_type": "text/markdown; charset=utf-8",
              "path": "source/id-ID/units/unit-020-lecture-020.md", "resource_id": RESOURCE,
              "rights_component_id": COMPOSITE_RIGHTS, "role": "canonical_reader_source",
              "sha256": SOURCE_SHA})
    add("assets.jsonl", a)
    # Terminology controls 0288 and 0289 are checked against the ledger before
    # being admitted as backend terms.
    with TERMS.open(encoding="utf-8", newline="") as stream:
        term_rows = {r["term_id"]: r for r in csv.DictReader(stream)}
    for control, source_term, preferred, concept, evidence in (
        ("O012-TERM-0288", "isomorphism", "isomorfisma", "concept:isomorphism", "segment:o012-rbt-l20-mcheck-001"),
        ("O012-TERM-0289", "homomorphism", "homomorfisma", "concept:homomorphism", "segment:o012-rbt-l20-mcheck-006"),
    ):
        row = term_rows.get(control)
        if not row or row["source_term"] != source_term or row["id_ID"] != preferred or row["status"] != "admitted":
            raise SystemExit(f"terminology control mismatch: {control}")
        t = common("term", f"term:{source_term}:id-ID")
        t.update({"concept_id": concept, "evidence_segment_id": evidence, "locale": "id-ID",
                  "preferred": preferred, "register": "textbook", "rejected_forms": [], "rights_component_id": ROBERTS_RIGHTS,
                  "scope_unit_id": ROOT, "source_term": source_term, "terminology_control_id": control,
                  "terminology_status": "admitted", "usage_note": row["note"], "variants": ["isomorfisme"] if source_term == "isomorphism" else []})
        add("terms.jsonl", t)
    # Nine exact adverse rows, with evidence-bound target anchors.
    with LEDGER.open(encoding="utf-8", newline="") as stream:
        rows = {r["event_id"]: r for r in csv.DictReader(stream)}
    for n, (severity, status, evidence) in EXPECTED_EVENT.items():
        eid = f"O012-ADV-{n:04d}"
        row = rows.get(eid)
        if not row or row["severity"] != severity or row["status"] != status or evidence not in row["source_location"]:
            raise SystemExit(f"adverse control mismatch: {eid}")
        local_targets = [f"o012-rbt-l20-{x}" for x in TARGETS[n]]
        if any(x not in heading for x in local_targets):
            raise SystemExit(f"adverse target absent: {eid}")
        ctype = {"accessibility_reflow": "structural_adaptation", "clarified_in_translation": "clarification",
                 "corrected_in_translation": "mathematical_correction",
                 "corrected_after_independent_review": "mathematical_correction",
                 "proof_completed_in_translation": "proof_completion"}[status]
        c = common("correction", f"correction:o012-u020-adv-{n:04d}")
        c.update({"adverse_ledger_id": eid, "affected_unit_ids": [f"unit:{x}" for x in local_targets],
                  "correction_type": ctype, "edition_id": EDITION, "evidence": row["source_location"],
                  "evidence_segment_id": "segment:o012-rbt-l20-notice", "severity": severity,
                  "rationale": row["rationale"], "resource_id": RESOURCE, "source_defect": row["observed"],
                  "target_change": row["action"], "unit_id": ROOT, "upstream_report_disposition": "not_contacted"})
        add("corrections.jsonl", c)
    # Evidence artifacts and three bounded QA events.
    for ident, (path, size, expected, media, state) in ARTIFACTS.items():
        data = (LANE / path).read_bytes()
        if len(data) != size or sha(data) != expected:
            raise SystemExit(f"artifact identity mismatch: {path}")
        a = common("artifact", ident)
        a.update({"bytes": size, "locale": "id-ID", "manifest_artifact_id": None, "media_type": media,
                  "path": path, "qa_event_ids": [], "rights_component_id": COMPOSITE_RIGHTS,
                  "sha256": expected, "toolchain": "Independent bounded Unit 020 evidence; no cumulative build assertion.",
                  "translation_state": state, "unit_id": ROOT})
        add("artifacts.jsonl", a)
    qa_specs = (
        ("qa:o012-u020-source-integrity", "source", "Unit 020 source identity, contiguous span, stable anchors, and adverse closure passed.", ["artifact:o012-u020-source-audit", "artifact:o012-u020-qa"]),
        ("qa:o012-u020-math", "math", "Independent Unit 020 mathematical review passed with no open P1/P2/P3 finding.", ["artifact:o012-u020-independent-review"]),
        ("qa:o012-u020-language", "language", "Unit 020 Indonesian terminology and language review passed.", ["artifact:o012-u020-independent-review", "artifact:o012-u020-translation-handoff"]),
    )
    for ident, qtype, note, witnesses in qa_specs:
        q = common("qa_event", ident)
        q.update({"note": note, "qa_type": qtype, "result": "passed", "unit_id": ROOT, "witness_artifact_ids": witnesses})
        add("qa.jsonl", q)
    # Relations: route continuity, aliases, and complete Unit 20 mastery.
    def relation(ident: str, source: str, typ: str, target: str, note: str) -> None:
        r = common("relation", ident)
        r.update({"from_id": source, "note": note, "relation_type": typ, "to_id": target})
        add("relations.jsonl", r)
    relation("relation:adapts:o012-rbt-u020:edition", ROOT, "adapts", EDITION, "Unit 20 is the Indonesian adapted reader boundary for the frozen Roberts edition.")
    relation("relation:precedes:o012-rbt-u019:o012-rbt-u020", "unit:o012-rbt-u019", "precedes", ROOT, "Preserves contiguous lecture-unit order.")
    relation("relation:precedes:o012-rbt-l20:mastery", LECTURE, "precedes", "unit:o012-rbt-l20-mastery", "Lecture content precedes its mastery companion.")
    relation("relation:boundary:o012-u020", CUMULATIVE_RIGHTS, "contains", ROOT, "New cumulative 001-020 rights boundary pointer; prior pointer retained.")
    for ident, (start, end, opener) in spans.items():
        aliases = re.findall(r'data-(?:source-(?:ref|label)|source-environment)="([^"]+)"', opener)
        for alias in aliases:
            safe = re.sub(r"[^a-z0-9]+", "-", alias.lower()).strip("-")
            relation(f"relation:xref:{ident}:{safe}", f"unit:{ident}", "xref", EDITION, f"Preserves upstream source label {alias}.")
    for n in range(1, 7):
        relation(f"relation:solves:l20-sol-{n:03d}:l20-mcheck-{n:03d}", f"unit:o012-rbt-l20-sol-{n:03d}", "solves", f"unit:o012-rbt-l20-mcheck-{n:03d}", f"Complete solution for Unit 20 mastery check {n}.")
        relation(f"relation:hints:l20-hint-{n:03d}:l20-mcheck-{n:03d}", f"unit:o012-rbt-l20-hint-{n:03d}", "hints", f"unit:o012-rbt-l20-mcheck-{n:03d}", f"Bounded hint for Unit 20 mastery check {n}.")
    for sol, ex in ((1, 1), (2, 1), (3, 2), (4, 3), (5, 4)):
        relation(f"relation:solves:l20-sol-{sol:03d}:l20-ex-{ex:03d}", f"unit:o012-rbt-l20-sol-{sol:03d}", "solves", f"unit:o012-rbt-l20-ex-{ex:03d}", "Mastery solution closes the corresponding source exercise.")
    # Referential closure for all old and new records.
    merged = {name: dict(recs[name]) for name in JSONL}
    for name in JSONL: merged[name].update(new[name])
    by_id = {ident: obj for table in merged.values() for ident, obj in table.items()}
    if len(by_id) != sum(len(t) for t in merged.values()):
        raise SystemExit("global duplicate IDs")
    scalar = {"concept_id", "course_id", "edition_id", "evidence_segment_id", "from_id", "manifest_artifact_id",
              "parent_id", "program_id", "resource_id", "rights_component_id", "scope_unit_id", "to_id", "unit_id"}
    lists = {"affected_unit_ids", "component_scope", "concept_ids", "local_derivative_unit_ids", "qa_event_ids", "witness_artifact_ids"}
    for ident, obj in by_id.items():
        for field in scalar:
            if field in obj and obj[field] is not None and obj[field] not in by_id:
                raise SystemExit(f"unknown reference {ident}.{field}={obj[field]}")
        for field in lists:
            if field in obj and any(x not in by_id for x in obj[field]):
                raise SystemExit(f"unknown list reference {ident}.{field}")
    # Back-fill QA witness IDs only in new artifact objects (never old ones).
    for aid in ARTIFACTS:
        qids = [q["id"] for q in new["qa.jsonl"].values() if aid in q["witness_artifact_ids"]]
        new["artifacts.jsonl"][aid]["qa_event_ids"] = sorted(qids)
    # Verify all planned additions and append bytes.  Historical byte slices
    # are compared immediately before writing.
    output: dict[str, bytes] = {}
    for name in JSONL:
        old_raw = (BACKEND / name).read_bytes()
        if old_raw != b"".join(old[name].values()):
            raise SystemExit(f"historical bytes changed before write: {name}")
        additions = b"".join(canon(new[name][ident]) for ident in sorted(new[name]))
        output[name] = old_raw + additions
    for name, raw_out in output.items():
        (BACKEND / name).write_bytes(raw_out)
    total = sum(len(x) for x in output.values())
    bundle = hashlib.sha256()
    for name in JSONL:
        bundle.update(name.encode()); bundle.update(b"\0"); bundle.update(output[name])
    counts = {name: len(new[name]) for name in JSONL}
    print("Unit 020 backend extension: PASS")
    print("new_records_by_file=" + json.dumps(counts, sort_keys=True))
    print(f"new_records={sum(counts.values())}")
    print(f"backend_bytes={total}")
    print(f"backend_bundle_sha256={bundle.hexdigest()}")
    print(f"source_sha256={SOURCE_SHA}")

if __name__ == "__main__":
    build()
