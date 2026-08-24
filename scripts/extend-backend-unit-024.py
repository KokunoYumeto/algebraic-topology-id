#!/usr/bin/env python3
"""Fail-closed append-only semantic-backend admission for Roberts Unit 024.

The complete 3,528-record Units 001--023 cumulative backend is immutable.
This transaction verifies that exact prefix, the frozen authority span, the
Unit 24 reader and QA witnesses, and its terminology/adverse controls before
constructing and validating the semantic suffix in memory.  It deliberately
does not admit cumulative build or publication artifacts.
"""
from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

LANE = Path(__file__).resolve().parents[1]
BACKEND = LANE / "backend"
SOURCE = LANE / "source/id-ID/units/unit-024-lecture-024.md"
UPSTREAM = (LANE / "authority/upstream" /
            "AlgebraicTopology2019-b947ad2e9f9e301bfe24590a9db653bc54fa1a53" /
            "Notes.tex")
AUDIT = LANE / "qa/UNIT_024_SOURCE_AUDIT.md"
REVIEW = LANE / "qa/UNIT_024_INDEPENDENT_REVIEW.md"
QA_JSON = LANE / "qa/UNIT_024_QA.json"
TERMINOLOGY = LANE / "00_control/TERMINOLOGY.csv"
LEDGER = LANE / "00_control/ADVERSE_LEDGER.csv"

SCHEMA = "curriculum.interop"
VERSION = "0.1.0"
WORKFLOW = "o012-d60-id-reader-production"
STAMP = "2026-08-24T00:00:00Z"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"
PROGRAM = "program:o012-id"
COURSE = "course:o012-d60"
ROUTE = "D60-R13"
RESOURCE = "resource:roberts-algebraic-topology-2019"
EDITION = "edition:roberts-at-2019-b947ad2"
COMMIT = "b947ad2e9f9e301bfe24590a9db653bc54fa1a53"
ROBERTS_RIGHTS = "rights:roberts-cc-by-4.0"
COMPANION_RIGHTS = "rights:o012-u024-companion-cc-by-4.0"
COMPOSITE_RIGHTS = "rights:o012-u024-composite-cc-by-4.0"
CUMULATIVE_RIGHTS = "rights:o012-units-001-024-composite-cc-by-4.0"
PRIOR_RIGHTS = "rights:o012-units-001-023-composite-cc-by-4.0-final-6f05"
ROOT = "unit:o012-rbt-u024"
LECTURE = "unit:o012-rbt-l24"
MASTERY = "unit:o012-rbt-l24-mastery"
SOURCE_PATH = "source/id-ID/units/unit-024-lecture-024.md"
SOURCE_BYTES = 43085
SOURCE_LINES = 1156
SOURCE_SHA = "993ad0c3493caff6bd15ab2bcf435f6cbb1f49ed9a1e11bc1009d649ae2d3647"
UPSTREAM_BYTES = 331447
UPSTREAM_LINES = 6368
UPSTREAM_SHA = "cfe93e9dbe3e25bd96f711f59e6078ab97527682b58e1f8ad127f74357f665d7"
UPSTREAM_START = 5113
UPSTREAM_END = 5369
UPSTREAM_SPAN_BYTES = 12837
UPSTREAM_SPAN_SHA = "b2128930a56a0a8c04c327a397e72e21b215ffe742bb684e8dd166f0e04b0aea"
ANCHOR_ORDER_SHA = "c38e06f24bba82aae0b16a4f75a4e87c6b7836038e08536a7e3d055982b0548a"

FILES = ("artifacts.jsonl", "assets.jsonl", "authority.jsonl", "concepts.jsonl",
         "corrections.jsonl", "qa.jsonl", "relations.jsonl", "rights.jsonl",
         "segments.jsonl", "terms.jsonl", "units.jsonl")
PREFIX = {
    "artifacts.jsonl": (125, 98770, "f8f4fc8b686554ce528bffe4ca31533d8f416ad34d9ed16b8f23b5b6d981c13c"),
    "assets.jsonl": (25, 15447, "752dfa957041664a1b3f32acdcf996511164d5c17ba6aa34619a100651dad3b1"),
    "authority.jsonl": (4, 2721, "f21af26912520ab34b38dff0e927ed46a546dbe5d318da0dc133e58330d0e368"),
    "concepts.jsonl": (312, 98079, "6fadff806dab54588f4984dd44ec745152841dbf44416ea881d9414f6b535830"),
    "corrections.jsonl": (313, 306801, "a0545c84efadc062f181356f9fa508b0da5f9077f52702da0750e3165c0b6244"),
    "qa.jsonl": (109, 61880, "3c8c741c0c50b56cd0d15b7616c3ebd3006fe368382cc14e7c50ee743eebb974"),
    "relations.jsonl": (337, 136702, "07f7ec67c251eb180f211b09da33ec165129c45646d1b08014de2f3e68b2882c"),
    "rights.jsonl": (63, 57648, "f39bd50ab5e33d7d3b0ae9063b2ed0adc9fc3986a8a034de4311876c3e810157"),
    "segments.jsonl": (956, 1193838, "1851199865ae823a7f155f1a33590290cafccb0f1cafe37d429fb7072a2d84c0"),
    "terms.jsonl": (305, 188007, "16ac428e76df5de2a97f475c9a80c7e63278bc57a15720047785e4ad217e82a9"),
    "units.jsonl": (979, 1274986, "e66891050013b595dbe972bee0d7ba3b88689a8a6a06a2c2885919194df036c9"),
}
PREFIX_RECORDS = 3528
PREFIX_BYTES = 3434879
PREFIX_BUNDLE = "0c8b27890f8423fc3224c89f2bcf60ed6cbcb9d93fabef7b53c399784f0aaaef"

FIXED_ARTIFACTS = {
    "artifact:o012-u024-independent-review": (
        "qa/UNIT_024_INDEPENDENT_REVIEW.md", 5570,
        "d06dc4a2d76eabbb8f4c115fd8f311c81e974415a186f8bff8269d30cb1672b2",
        "text/markdown; charset=utf-8", "mathematically_reviewed",
        ["qa:o012-u024-math", "qa:o012-u024-language"]),
    "artifact:o012-u024-source-audit": (
        "qa/UNIT_024_SOURCE_AUDIT.md", 4384,
        "0aeb3beae1b52099e97538083ef349590cca62b473ff1455b8c1fdaffbe2ba6b",
        "text/markdown; charset=utf-8", "source_frozen",
        ["qa:o012-u024-source-integrity"]),
}

TERM_SPECS = {
    "O012-TERM-0316": ("cochain map", "pemetaan korantai", "cochain-map", "o012-rbt-l24-proof-001", "homological_algebra"),
    "O012-TERM-0317": ("homological algebra", "aljabar homologis", "homological-algebra", "o012-rbt-l24-s03", "homological_algebra"),
    "O012-TERM-0318": ("algebraic Mayer--Vietoris theorem", "teorema Mayer--Vietoris aljabar", "algebraic-mayer-vietoris-theorem", "o012-rbt-l24-thm-001", "homological_algebra"),
    "O012-TERM-0319": ("Snake Lemma", "Lema Ular", "snake-lemma", "o012-rbt-l24-lem-002", "homological_algebra"),
    "O012-TERM-0320": ("diagram chase", "pengejaran diagram", "diagram-chase", "o012-rbt-l24-proof-003", "homological_algebra"),
    "O012-TERM-0321": ("naturality", "kealamian", "naturality", "o012-rbt-l24-proof-006", "category_theory"),
    "O012-TERM-0322": ("splicing exact sequences", "penyambungan barisan eksak", "splicing-exact-sequences", "o012-rbt-l24-proof-005", "homological_algebra"),
}

EXPECTED_ADVERSE = {
    323: ("P2", "Notes.tex:5113-5120", "proof_completed_in_translation", ["exa-001", "proof-001", "audit-001"], "proof_completion"),
    324: ("P2", "Notes.tex:5125-5129", "proof_completed_in_translation", ["lem-001", "proof-002", "audit-002"], "proof_completion"),
    325: ("P1", "Notes.tex:5173", "corrected_in_translation", ["thm-001", "audit-003"], "mathematical_correction"),
    326: ("P1", "Notes.tex:5186-5189", "corrected_in_translation", ["fig-001", "audit-004"], "mathematical_correction"),
    327: ("P1", "Notes.tex:5247-5311", "proof_completed_in_translation", ["lem-002", "proof-003", "audit-005"], "proof_completion"),
    328: ("P1", "Notes.tex:5332-5334", "proof_completed_in_translation", ["lem-003", "fig-003", "proof-004", "audit-006"], "proof_completion"),
    329: ("P1", "Notes.tex:5338-5354", "proof_completed_in_translation", ["proof-005", "audit-007"], "proof_completion"),
    330: ("P2", "Notes.tex:5357-5367", "clarified_in_translation", ["proof-006", "audit-008"], "clarification"),
    331: ("P2", "Notes.tex:5148-5162,5166,5179,5186-5244,5323-5327,5340,5348-5352,5360", "accessibility_reflow", [*[f"margin-{n:03d}" for n in range(1, 8)], *[f"fig-{n:03d}" for n in range(1, 4)], "audit-004", "audit-006"], "structural_adaptation"),
}

BASE_CONCEPTS = (
    "coboundary", "cocycle", "cohomologically-graded-complex", "cokernel",
    "commutative-cube", "complex", "connecting-map", "delta-set", "exact-at",
    "extension-by-zero", "functoriality", "kernel", "long-exact-sequence",
    "module-over-r", "morphism-of-complexes", "relative-simplicial-cochain-complex",
    "short-exact-sequence", "simplicial-cochain-complex",
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


def load_generic():
    path = LANE / "scripts/validate-backend.py"
    spec = importlib.util.spec_from_file_location("o012_generic_u024_producer", path)
    if spec is None or spec.loader is None:
        raise SystemExit("cannot load generic backend validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_prefix() -> tuple[dict[str, dict[str, dict[str, Any]]], dict[str, bytes]]:
    tables: dict[str, dict[str, dict[str, Any]]] = {}
    raw_files: dict[str, bytes] = {}
    bundle = hashlib.sha256()
    seen: set[str] = set()
    for name in FILES:
        raw = (BACKEND / name).read_bytes()
        raw_files[name] = raw
        count, size, expected_sha = PREFIX[name]
        lines = raw.splitlines(keepends=True)
        if (len(raw), len(lines), digest(raw)) != (size, count, expected_sha):
            raise SystemExit(f"{name}: immutable Units 001-023 prefix mismatch")
        if b"\r" in raw or not raw.endswith(b"\n"):
            raise SystemExit(f"{name}: prefix newline mismatch")
        table: dict[str, dict[str, Any]] = {}
        for number, line in enumerate(lines, 1):
            obj = json.loads(line.decode("utf-8"))
            if not isinstance(obj.get("id"), str) or obj["id"] in seen or canon(obj) != line:
                raise SystemExit(f"{name}:{number}: noncanonical/duplicate prefix record")
            seen.add(obj["id"]); table[obj["id"]] = obj
        tables[name] = table
        bundle.update(name.encode()); bundle.update(b"\0"); bundle.update(raw)
    if (len(seen) != PREFIX_RECORDS or sum(len(raw) for raw in raw_files.values()) != PREFIX_BYTES
            or bundle.hexdigest() != PREFIX_BUNDLE):
        raise SystemExit("Units 001-023 backend bundle identity mismatch")
    required = {"unit:o012-rbt-u023", PRIOR_RIGHTS,
                "unit:o012-rbt-l23-exa-002",
                "relation:xref:o012-rbt-l23-exa-002:u024-continuation"}
    if not required <= seen:
        raise SystemExit("Unit 23 continuation/prefix authority is incomplete")
    return tables, raw_files


def verify_upstream() -> None:
    raw = UPSTREAM.read_bytes()
    if len(raw) != UPSTREAM_BYTES or digest(raw) != UPSTREAM_SHA:
        raise SystemExit("frozen Notes.tex identity mismatch")
    text = raw.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")
    lines = text.split("\n")
    if len(lines) - 1 != UPSTREAM_LINES:
        raise SystemExit("frozen Notes.tex line count mismatch")
    span = ("\n".join(lines[UPSTREAM_START - 1:UPSTREAM_END]) + "\n").encode()
    if len(span) != UPSTREAM_SPAN_BYTES or digest(span) != UPSTREAM_SPAN_SHA:
        raise SystemExit("Unit 24 upstream span mismatch")
    if ("\\lecturenum{24}" not in lines[5112]
            or lines[5120].strip() != "\\end{example}"
            or "\\lecturenum{25}" not in lines[5369]):
        raise SystemExit("Unit 24 boundary/continued-example identity mismatch")


def structural_spans(lines: list[str]) -> tuple[list[str], dict[str, tuple[int, int, str]]]:
    opening = re.compile(r"^\s*:::\s+\{[^#}]*#(o012-rbt-l24(?:-[A-Za-z0-9-]+)?)(.*)\}\s*$")
    heading = re.compile(r"^#{1,6}\s+.*\{[^}]*#(o012-rbt-l24(?:-[A-Za-z0-9-]+)?)[^}]*\}\s*$")
    stack: list[tuple[str, int, str]] = []
    spans: dict[str, tuple[int, int, str]] = {}
    ordered: list[str] = []
    for number, line in enumerate(lines, 1):
        hm = heading.match(line)
        if hm:
            ordered.append(hm.group(1))
        fm = opening.match(line)
        if fm:
            ordered.append(fm.group(1)); stack.append((fm.group(1), number, line))
        elif line.strip() == ":::":
            if not stack:
                raise SystemExit(f"unexpected div close at reader line {number}")
            ident, start, opener = stack.pop()
            if ident in spans:
                raise SystemExit(f"duplicate fenced anchor: {ident}")
            spans[ident] = (start, number, opener)
    if stack:
        raise SystemExit(f"unclosed div anchors: {[item[0] for item in stack]}")
    heading_spans = {
        "o012-rbt-l24-notice": (12, 53), "o012-rbt-l24": (54, 810),
        "o012-rbt-l24-s01": (56, 139), "o012-rbt-l24-s02": (140, 205),
        "o012-rbt-l24-s03": (206, 292), "o012-rbt-l24-s04": (293, 559),
        "o012-rbt-l24-s05": (560, 660), "o012-rbt-l24-s06": (661, 757),
        "o012-rbt-l24-s07": (758, 810), "o012-rbt-l24-mastery": (811, 1148),
    }
    for ident, (start, end) in heading_spans.items():
        if ident not in ordered or ident not in lines[start - 1]:
            raise SystemExit(f"heading span identity mismatch: {ident}")
        spans[ident] = (start, end, lines[start - 1])
    if (len(ordered) != 60 or len(set(ordered)) != 60 or set(ordered) != set(spans)
            or digest(("\n".join(ordered) + "\n").encode()) != ANCHOR_ORDER_SHA):
        raise SystemExit("Unit 24 stable-ID inventory/order mismatch")
    return ordered, spans


def unit_kind(ident: str, opener: str) -> str:
    if ident.endswith("-notice"): return "notice"
    if ident == "o012-rbt-l24": return "lecture"
    if ident.endswith("-mastery"): return "mastery_section"
    if re.fullmatch(r"o012-rbt-l24-s\d{2}", ident): return "section"
    match = re.search(r"\{\.([A-Za-z][A-Za-z0-9_-]*)", opener)
    kind = (match.group(1).replace("source-audit", "source_audit")
            .replace("source-margin", "source_margin") if match else "")
    allowed = {"boundary", "definition", "example", "exercise", "figure", "hint",
               "lemma", "proof", "remark", "solution", "source_audit", "source_margin",
               "theorem"}
    if kind not in allowed:
        raise SystemExit(f"cannot infer kind for {ident}: {kind!r}")
    return kind


def is_original(ident: str, kind: str) -> bool:
    return (kind in {"notice", "source_audit", "mastery_section", "boundary",
                     "hint", "solution", "proof"} or "-mcheck-" in ident)


def target_locator(start: int, end: int, raw_lines: list[bytes]) -> dict[str, Any]:
    return {"content_sha256": digest(b"".join(raw_lines[start - 1:end])),
            "file_sha256": SOURCE_SHA, "line_end": end, "line_start": start,
            "path": SOURCE_PATH}


def source_locator(original: bool) -> dict[str, Any]:
    if original:
        return {"kind": "edition_original", "path": SOURCE_PATH,
                "precision": "exact_target_span"}
    return {"commit_sha": COMMIT, "line_end": UPSTREAM_END,
            "line_start": UPSTREAM_START, "path": "Notes.tex",
            "precision": "unit_range_only"}


def display_title(ident: str, lines: list[str], start: int, kind: str) -> str:
    first = lines[start - 1].strip()
    if first.startswith("#"):
        return re.sub(r"\s*\{.*\}$", "", re.sub(r"^#+\s*", "", first)).strip()
    for line in lines[start:min(start + 7, len(lines))]:
        value = line.strip().replace("**", "")
        if value and not value.startswith(":::") and not value.startswith(">"):
            return value[:180]
    return f"Unit 24 {kind} {ident.rsplit('-', 1)[-1]}"


def verify_qa() -> tuple[int, str]:
    raw = QA_JSON.read_bytes()
    qa = json.loads(raw.decode("utf-8"))
    if (qa.get("status") != "PASS"
            or qa.get("source", {}).get("line_start") != UPSTREAM_START
            or qa.get("source", {}).get("line_end") != UPSTREAM_END
            or qa.get("source", {}).get("span_bytes") != UPSTREAM_SPAN_BYTES
            or qa.get("source", {}).get("span_sha256") != UPSTREAM_SPAN_SHA
            or qa.get("source", {}).get("next_line") != 5370
            or qa.get("unit", {}).get("bytes") != SOURCE_BYTES
            or qa.get("unit", {}).get("lines") != SOURCE_LINES
            or qa.get("unit", {}).get("sha256") != SOURCE_SHA
            or qa.get("unit", {}).get("stable_ids") != 60
            or qa.get("unit", {}).get("fenced_semantic_objects") != 50
            or qa.get("proof_closure", {}).get("mastery_solution_triples") != 6
            or qa.get("model_provenance") != MODEL):
        raise SystemExit("Unit 24 QA content/binding mismatch")
    checks = qa.get("checks")
    if not isinstance(checks, list) or not checks or any(
            not isinstance(item, dict) or item.get("status") != "PASS" for item in checks):
        raise SystemExit("Unit 24 QA contains a non-passing check")
    return len(raw), digest(raw)


def main() -> int:
    tables, prefix_raw = load_prefix()
    verify_upstream()
    qa_bytes, qa_sha = verify_qa()
    existing_ids = {ident for table in tables.values() for ident in table}
    additions: dict[str, dict[str, dict[str, Any]]] = {name: {} for name in FILES}

    def add(name: str, obj: dict[str, Any]) -> None:
        ident = obj["id"]
        if ident in existing_ids or any(ident in table for table in additions.values()):
            raise SystemExit(f"duplicate new ID: {ident}")
        additions[name][ident] = obj

    raw = SOURCE.read_bytes()
    if (len(raw) != SOURCE_BYTES or digest(raw) != SOURCE_SHA or b"\r" in raw
            or not raw.endswith(b"\n")):
        raise SystemExit("Unit 24 reader identity/newline mismatch")
    raw_lines = raw.splitlines(keepends=True)
    lines = [line.decode("utf-8").rstrip("\n") for line in raw_lines]
    if len(lines) != SOURCE_LINES or raw.decode("utf-8").count(MODEL) != 1:
        raise SystemExit("Unit 24 reader line/model-provenance mismatch")
    anchors, spans = structural_spans(lines)

    for _control, (source_term, _preferred, slug, _evidence, domain) in TERM_SPECS.items():
        ident = f"concept:{slug}"
        if ident in existing_ids:
            raise SystemExit(f"new Unit 24 concept unexpectedly pre-exists: {ident}")
        concept = common("concept", ident)
        concept.update({"canonical_label": source_term, "domain": domain,
                        "locale_neutral": True})
        add("concepts.jsonl", concept)
    concept_ids = [f"concept:{slug}" for slug in BASE_CONCEPTS] + [
        f"concept:{spec[2]}" for spec in TERM_SPECS.values()]
    if (len(concept_ids) != len(set(concept_ids)) or any(
            ident not in existing_ids and ident not in additions["concepts.jsonl"]
            for ident in concept_ids)):
        raise SystemExit("Unit 24 concept closure mismatch")

    rights_specs = (
        (COMPANION_RIGHTS,
         "Indonesian original mastery, source-audit, proof-completion, and boundary layer for Roberts Unit 24.",
         "Original additions are CC BY 4.0; source-derived material remains separately attributed.",
         [ROOT], None),
        (COMPOSITE_RIGHTS,
         "David Michael Roberts source adaptation plus original Indonesian Unit 24 companions.",
         "Unit 24 source-derived and original layers remain component-distinguishable.",
         [ROOT], None),
        (CUMULATIVE_RIGHTS,
         "Cumulative Roberts Units 001-024 Indonesian reader source boundary.",
         "Source-stage cumulative pointer; the verified Units 001-023 public build remains immutable.",
         [f"unit:o012-rbt-u{number:03d}" for number in range(1, 25)], PRIOR_RIGHTS),
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
        ("o012-rbt-l24-s01", 56, 139), ("o012-rbt-l24-s02", 140, 205),
        ("o012-rbt-l24-s03", 206, 292), ("o012-rbt-l24-s04", 293, 559),
        ("o012-rbt-l24-s05", 560, 660), ("o012-rbt-l24-s06", 661, 757),
        ("o012-rbt-l24-s07", 758, 810),
    )
    section_ids = {item[0] for item in section_ranges}

    def parent_local(ident: str, start: int) -> str:
        if ident in {"o012-rbt-l24-notice", "o012-rbt-l24",
                     "o012-rbt-l24-mastery", "o012-rbt-l24-boundary-001"}:
            return ROOT
        if ident in section_ids:
            return LECTURE
        if any(token in ident for token in ("-mcheck-", "-hint-", "-sol-")):
            return MASTERY
        for section, low, high in section_ranges:
            if low <= start <= high:
                return f"unit:{section}"
        raise SystemExit(f"cannot assign Unit 24 parent: {ident}")

    children: defaultdict[str, list[str]] = defaultdict(list)
    for ident in anchors:
        children[parent_local(ident, spans[ident][0])].append(ident)
    order_map = {parent: {ident: number for number, ident in enumerate(
        sorted(items, key=lambda item: spans[item][0]), 1)}
        for parent, items in children.items()}
    path_by_id: dict[str, list[str]] = {ROOT: [ROOT]}
    root = common("unit", ROOT)
    root.update({
        "component_source_commit": COMMIT, "component_source_id": RESOURCE,
        "concept_ids": concept_ids, "course_id": COURSE,
        "course_route_unit_id": ROUTE,
        "display_title": "Topologi Aljabar - Unit 24: Korantai Relatif, Lema Ular, dan Barisan Eksak Panjang",
        "edition_id": EDITION, "edition_unit_id": ROOT, "locale": "id-ID",
        "model_provenance": MODEL, "order": 24, "parent_id": COURSE,
        "path": [ROOT], "program_id": PROGRAM,
        "provenance_relation": "composite_translated_and_original",
        "resource_id": RESOURCE, "rights_component_id": COMPOSITE_RIGHTS,
        "source_local_id": None,
        "source_locator": {"commit_sha": COMMIT, "line_end": UPSTREAM_END,
                           "line_start": UPSTREAM_START, "path": "Notes.tex",
                           "precision": "exact_unit_span",
                           "span_bytes": UPSTREAM_SPAN_BYTES,
                           "span_sha256": UPSTREAM_SPAN_SHA},
        "target_locator": target_locator(1, SOURCE_LINES, raw_lines),
        "translation_state": "structurally_verified", "unit_kind": "reader_unit",
    })
    add("units.jsonl", root)
    for ident in anchors:
        start, end, opener = spans[ident]
        kind = unit_kind(ident, opener)
        parent_id = parent_local(ident, start)
        if parent_id not in path_by_id:
            raise SystemExit(f"parent path not yet constructed: {ident} -> {parent_id}")
        unit_id = f"unit:{ident}"
        path = path_by_id[parent_id] + [unit_id]
        path_by_id[unit_id] = path
        original = is_original(ident, kind)
        rights_id = COMPANION_RIGHTS if original else ROBERTS_RIGHTS
        locator = target_locator(start, end, raw_lines)
        shared = {"component_source_commit": COMMIT,
                  "component_source_id": RESOURCE,
                  "course_route_unit_id": ROUTE, "edition_unit_id": ROOT,
                  "model_provenance": MODEL}
        unit = common("unit", unit_id); unit.update(shared)
        unit.update({"concept_ids": concept_ids, "course_id": COURSE,
                     "display_title": display_title(ident, lines, start, kind),
                     "edition_id": EDITION, "locale": "id-ID",
                     "order": order_map[parent_id][ident], "parent_id": parent_id,
                     "path": path, "program_id": PROGRAM,
                     "provenance_relation": ("edition_original" if original else
                                               "translated_adapted_from_upstream"),
                     "resource_id": RESOURCE, "rights_component_id": rights_id,
                     "source_local_id": ident, "target_locator": locator,
                     "translation_state": "structurally_verified", "unit_kind": kind})
        segment = common("segment", f"segment:{ident}"); segment.update(shared)
        segment.update({"concept_ids": concept_ids, "edition_id": EDITION,
                        "locale": "id-ID", "order": unit["order"],
                        "provenance_relation": unit["provenance_relation"],
                        "resource_id": RESOURCE, "rights_component_id": rights_id,
                        "segment_kind": kind, "source_local_id": ident,
                        "source_locator": source_locator(original),
                        "target_locator": locator,
                        "translation_state": "structurally_verified",
                        "unit_id": unit_id})
        aliases = re.findall(r'data-source-label="([^"]+)"', opener)
        if aliases:
            unit["source_aliases"] = aliases; segment["source_aliases"] = aliases
        if ident == "o012-rbt-l24-exa-001":
            continuation = {
                "continuation_from_edition_unit_id": "unit:o012-rbt-u023",
                "continuation_source_line_end": 5121,
                "continuation_source_line_start": 5113,
                "source_environment_state": "closed_in_this_unit",
            }
            unit.update(continuation); segment.update(continuation)
        if ident == "o012-rbt-l24-boundary-001":
            unit["next_source_line"] = 5370; segment["next_source_line"] = 5370
        if kind == "proof":
            unit["proof_status"] = "complete_original_proof"
            segment["proof_status"] = "complete_original_proof"
        if kind == "solution":
            unit["solution_status"] = "complete_checked_solution"
            segment["solution_status"] = "complete_checked_solution"
        add("units.jsonl", unit); add("segments.jsonl", segment)

    asset = common("asset", "asset:o012-u024-source-markdown")
    asset.update({"bytes": SOURCE_BYTES, "edition_id": EDITION,
                  "media_type": "text/markdown; charset=utf-8", "path": SOURCE_PATH,
                  "resource_id": RESOURCE, "rights_component_id": COMPOSITE_RIGHTS,
                  "role": "canonical_reader_source", "sha256": SOURCE_SHA})
    add("assets.jsonl", asset)

    with TERMINOLOGY.open(encoding="utf-8", newline="") as stream:
        term_rows = {row["term_id"]: row for row in csv.DictReader(stream)}
    for control, (source_term, preferred, slug, evidence, _domain) in TERM_SPECS.items():
        row = term_rows.get(control)
        if (not row or row["source_term"] != source_term or row["id_ID"] != preferred
                or row["status"] != "admitted" or evidence not in spans):
            raise SystemExit(f"terminology control mismatch: {control}")
        term = common("term", f"term:{slug}:id-ID")
        term.update({"concept_id": f"concept:{slug}",
                     "evidence_segment_id": f"segment:{evidence}", "locale": "id-ID",
                     "preferred": preferred, "register": "textbook",
                     "rejected_forms": [], "rights_component_id": ROBERTS_RIGHTS,
                     "scope_unit_id": ROOT, "source_term": source_term,
                     "terminology_control_id": control,
                     "terminology_status": "admitted", "usage_note": row["note"],
                     "variants": []})
        add("terms.jsonl", term)

    with LEDGER.open(encoding="utf-8", newline="") as stream:
        adverse_rows = {row["event_id"]: row for row in csv.DictReader(stream)}
    for number, (severity, source_location, status, suffixes,
                 correction_type) in EXPECTED_ADVERSE.items():
        event_id = f"O012-ADV-{number:04d}"
        row = adverse_rows.get(event_id)
        if (not row or row["severity"] != severity
                or row["source_location"] != source_location or row["status"] != status):
            raise SystemExit(f"adverse control mismatch: {event_id}")
        targets = [f"o012-rbt-l24-{suffix}" for suffix in suffixes]
        if any(target not in spans for target in targets):
            raise SystemExit(f"adverse target absent: {event_id}")
        correction = common("correction", f"correction:o012-u024-adv-{number:04d}")
        correction.update({"adverse_ledger_id": event_id,
                           "affected_unit_ids": [f"unit:{target}" for target in targets],
                           "correction_type": correction_type, "edition_id": EDITION,
                           "evidence": source_location,
                           "evidence_segment_id": "segment:o012-rbt-l24-notice",
                           "severity": severity, "rationale": row["rationale"],
                           "resource_id": RESOURCE, "source_defect": row["observed"],
                           "target_change": row["action"], "unit_id": ROOT,
                           "upstream_report_disposition": "not_contacted"})
        add("corrections.jsonl", correction)

    artifact_specs = dict(FIXED_ARTIFACTS)
    artifact_specs["artifact:o012-u024-qa"] = (
        "qa/UNIT_024_QA.json", qa_bytes, qa_sha, "application/json", "built",
        ["qa:o012-u024-source-integrity", "qa:o012-u024-language"])
    for ident, (relative, size, expected_sha, media_type, state, qa_ids) in artifact_specs.items():
        artifact_raw = (LANE / relative).read_bytes()
        if len(artifact_raw) != size or digest(artifact_raw) != expected_sha:
            raise SystemExit(f"evidence identity mismatch: {relative}")
        artifact = common("artifact", ident)
        artifact.update({"bytes": size, "locale": "id-ID",
                         "manifest_artifact_id": None, "media_type": media_type,
                         "path": relative, "qa_event_ids": qa_ids,
                         "rights_component_id": COMPOSITE_RIGHTS,
                         "sha256": expected_sha,
                         "toolchain": (f"Bounded Unit 24 evidence; Notes.tex:5113-5369 "
                                       f"span {UPSTREAM_SPAN_SHA}; {MODEL}; route {ROUTE}; "
                                       "no cumulative-build/publication assertion."),
                         "translation_state": state, "unit_id": ROOT})
        add("artifacts.jsonl", artifact)

    qa_specs = (
        ("qa:o012-u024-source-integrity", "source",
         "Unit 24 authority/reader identities, 60 stable IDs, source census, controls, and Pandoc structure passed.",
         ["artifact:o012-u024-source-audit", "artifact:o012-u024-qa"]),
        ("qa:o012-u024-math", "math",
         "Independent Unit 24 mathematical review passed with no open P1, P2, or P3 finding.",
         ["artifact:o012-u024-independent-review"]),
        ("qa:o012-u024-language", "language",
         "Independent Indonesian language, terminology, attribution, accessibility, continuation, and mastery review passed.",
         ["artifact:o012-u024-independent-review", "artifact:o012-u024-qa"]),
    )
    for ident, qa_type, note, witnesses in qa_specs:
        event = common("qa_event", ident)
        event.update({"note": note, "qa_type": qa_type, "result": "passed",
                      "unit_id": ROOT, "witness_artifact_ids": witnesses})
        add("qa.jsonl", event)

    def relation(ident: str, source_id: str, relation_type: str,
                 target_id: str, note: str, **extra: Any) -> None:
        item = common("relation", ident)
        item.update({"from_id": source_id, "note": note,
                     "relation_type": relation_type, "to_id": target_id})
        item.update(extra); add("relations.jsonl", item)

    relation("relation:adapts:o012-rbt-u024:edition", ROOT, "adapts", EDITION,
             "Unit 24 is the Indonesian adapted reader boundary for the frozen Roberts edition.")
    relation("relation:precedes:o012-rbt-u023:o012-rbt-u024",
             "unit:o012-rbt-u023", "precedes", ROOT,
             "Preserves contiguous Roberts lecture-unit order.")
    relation("relation:precedes:o012-rbt-l24:mastery", LECTURE, "precedes", MASTERY,
             "Lecture content precedes the Unit 24 mastery companion.")
    relation("relation:boundary:o012-u024", CUMULATIVE_RIGHTS, "contains", ROOT,
             "Additive cumulative Units 001-024 semantic source boundary.")
    relation("relation:route:d60-r13:o012-rbt-u024", COURSE, "contains", ROOT,
             "Roberts Lecture 24 is an edition unit in the non-destructive D60-R13 learner-route view.",
             course_route_unit_id=ROUTE, edition_unit_id=ROOT)
    relation("relation:xref:o012-rbt-l24-exa-001:u023-continuation",
             "unit:o012-rbt-l24-exa-001", "xref", "unit:o012-rbt-l23-exa-002",
             "Unit 24 resumes at Notes.tex:5113 and closes at 5121 the source example opened in Unit 23.",
             continuation_from_edition_unit_id="unit:o012-rbt-u023",
             continuation_source_line_end=5121, continuation_source_line_start=5113,
             source_environment_state="closed_in_this_unit")
    proof_targets = {
        1: "unit:o012-rbt-l24-exa-001", 2: "unit:o012-rbt-l24-lem-001",
        3: "unit:o012-rbt-l24-lem-002", 4: "unit:o012-rbt-l24-lem-003",
        5: "unit:o012-rbt-l24-thm-001", 6: "unit:o012-rbt-l24-s07",
    }
    for number, target in proof_targets.items():
        relation(f"relation:proves:o012-rbt-l24-proof-{number:03d}:closure",
                 f"unit:o012-rbt-l24-proof-{number:03d}", "proves", target,
                 f"Edition-original complete proof closure {number} for Unit 24.")
    for number in range(1, 7):
        relation(f"relation:solves:l24-sol-{number:03d}:l24-mcheck-{number:03d}",
                 f"unit:o012-rbt-l24-sol-{number:03d}", "solves",
                 f"unit:o012-rbt-l24-mcheck-{number:03d}",
                 f"Complete checked solution for Unit 24 mastery check {number}.")
        relation(f"relation:hints:l24-hint-{number:03d}:l24-mcheck-{number:03d}",
                 f"unit:o012-rbt-l24-hint-{number:03d}", "hints",
                 f"unit:o012-rbt-l24-mcheck-{number:03d}",
                 f"Bounded hint for Unit 24 mastery check {number}.")

    merged = {name: dict(tables[name]) for name in FILES}
    for name in FILES:
        merged[name].update(additions[name])
    by_id = {ident: obj for table in merged.values() for ident, obj in table.items()}
    if len(by_id) != sum(len(table) for table in merged.values()):
        raise SystemExit("global duplicate backend IDs")
    records = [obj for name in FILES for obj in merged[name].values()]
    generic = load_generic()
    generic.validate_shapes(records)
    generic.validate_references(records, by_id)
    generic.validate_artifact_manifests(records, LANE)

    for ident in anchors:
        unit = by_id[f"unit:{ident}"]; segment = by_id[f"segment:{ident}"]
        if unit["target_locator"] != segment["target_locator"]:
            raise SystemExit(f"unit/segment locator mismatch: {ident}")
        if unit["path"][-1] != unit["id"]:
            raise SystemExit(f"noncanonical Unit 24 path: {ident}")
        if unit["parent_id"].startswith("unit:"):
            if unit["path"][:-1] != by_id[unit["parent_id"]]["path"]:
                raise SystemExit(f"Unit 24 parent path mismatch: {ident}")
        for obj in (unit, segment):
            if (obj["edition_unit_id"] != ROOT or obj["course_route_unit_id"] != ROUTE
                    or obj["model_provenance"] != MODEL):
                raise SystemExit(f"Unit 24 route/provenance mismatch: {ident}")
    sibling_orders: defaultdict[str, list[int]] = defaultdict(list)
    for obj in additions["units.jsonl"].values():
        sibling_orders[obj["parent_id"]].append(obj["order"])
    if any(len(values) != len(set(values)) for values in sibling_orders.values()):
        raise SystemExit("duplicate Unit 24 sibling order")
    for number in range(1, 7):
        check = f"unit:o012-rbt-l24-mcheck-{number:03d}"
        solves = [obj for obj in additions["relations.jsonl"].values()
                  if obj["relation_type"] == "solves" and obj["to_id"] == check]
        hints = [obj for obj in additions["relations.jsonl"].values()
                 if obj["relation_type"] == "hints" and obj["to_id"] == check]
        if len(solves) != 1 or len(hints) != 1:
            raise SystemExit(f"Unit 24 mastery closure mismatch: {number}")
    proofs = [obj for obj in additions["units.jsonl"].values()
              if obj.get("proof_status") == "complete_original_proof"]
    if len(proofs) != 6:
        raise SystemExit("Unit 24 six-proof closure mismatch")
    correction_ids = {obj.get("adverse_ledger_id")
                      for obj in additions["corrections.jsonl"].values()}
    if correction_ids != {f"O012-ADV-{number:04d}" for number in range(323, 332)}:
        raise SystemExit("Unit 24 adverse closure mismatch")
    if additions["rights.jsonl"][CUMULATIVE_RIGHTS]["component_scope"] != [
            f"unit:o012-rbt-u{number:03d}" for number in range(1, 25)]:
        raise SystemExit("Unit 24 cumulative rights scope mismatch")
    continued = by_id["unit:o012-rbt-l24-exa-001"]
    if (continued.get("source_environment_state") != "closed_in_this_unit"
            or continued.get("continuation_from_edition_unit_id") != "unit:o012-rbt-u023"
            or continued.get("continuation_source_line_start") != 5113
            or continued.get("continuation_source_line_end") != 5121):
        raise SystemExit("Unit 23/24 continuation closure mismatch")
    if by_id["unit:o012-rbt-l24-boundary-001"].get("next_source_line") != 5370:
        raise SystemExit("Unit 24 terminal cursor mismatch")

    outputs: dict[str, bytes] = {}
    for name in FILES:
        if (BACKEND / name).read_bytes() != prefix_raw[name]:
            raise SystemExit(f"{name}: prefix changed before write")
        suffix = b"".join(canon(additions[name][ident])
                          for ident in sorted(additions[name]))
        outputs[name] = prefix_raw[name] + suffix
    for name, generated in outputs.items():
        (BACKEND / name).write_bytes(generated)
    bundle = hashlib.sha256()
    for name in FILES:
        bundle.update(name.encode()); bundle.update(b"\0"); bundle.update(outputs[name])
    counts = {name: len(additions[name]) for name in FILES}
    print("Unit 024 semantic backend extension: PASS")
    print("new_records_by_file=" + json.dumps(counts, sort_keys=True))
    print(f"new_records={sum(counts.values())}")
    print(f"total_records={sum(PREFIX[name][0] + counts[name] for name in FILES)}")
    print(f"backend_bytes={sum(len(item) for item in outputs.values())}")
    print(f"backend_bundle_sha256={bundle.hexdigest()}")
    for name in FILES:
        print(f"file={name} records={PREFIX[name][0] + counts[name]} "
              f"bytes={len(outputs[name])} sha256={digest(outputs[name])}")
    print(f"source_sha256={SOURCE_SHA}")
    print(f"upstream_span_sha256={UPSTREAM_SPAN_SHA}")
    print(f"qa_bytes={qa_bytes}")
    print(f"qa_sha256={qa_sha}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
