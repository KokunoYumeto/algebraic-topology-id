#!/usr/bin/env python3
"""Fail-closed append-only semantic-backend admission for Roberts Unit 025.

The complete 3,723-record Units 001--024 cumulative backend is immutable.
This transaction verifies that exact prefix, the frozen authority span, the
corrected Unit 25 reader and evidence, and the new terminology/adverse ledger
tails before constructing and validating the semantic suffix in memory.  It
deliberately does not admit cumulative build or publication artifacts.
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
SOURCE = LANE / "source/id-ID/units/unit-025-lecture-025.md"
UPSTREAM = (LANE / "authority/upstream" /
            "AlgebraicTopology2019-b947ad2e9f9e301bfe24590a9db653bc54fa1a53" /
            "Notes.tex")
AUDIT = LANE / "qa/UNIT_025_SOURCE_AUDIT.md"
REVIEW = LANE / "qa/UNIT_025_INDEPENDENT_REVIEW.md"
QA_JSON = LANE / "qa/UNIT_025_QA.json"
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
COMPANION_RIGHTS = "rights:o012-u025-companion-cc-by-4.0"
COMPOSITE_RIGHTS = "rights:o012-u025-composite-cc-by-4.0"
CUMULATIVE_RIGHTS = "rights:o012-units-001-025-composite-cc-by-4.0"
PRIOR_RIGHTS = "rights:o012-units-001-024-composite-cc-by-4.0-final-993a"
ROOT = "unit:o012-rbt-u025"
LECTURE = "unit:o012-rbt-l25"
MASTERY = "unit:o012-rbt-l25-mastery"
SOURCE_PATH = "source/id-ID/units/unit-025-lecture-025.md"
SOURCE_BYTES = 36578
SOURCE_LINES = 1104
SOURCE_SHA = "df72add4e57236b51ff7d2a0c99af4b65299365874163cb334be5d0988c0f769"
UPSTREAM_BYTES = 331447
UPSTREAM_LINES = 6368
UPSTREAM_SHA = "cfe93e9dbe3e25bd96f711f59e6078ab97527682b58e1f8ad127f74357f665d7"
UPSTREAM_START = 5370
UPSTREAM_END = 5611
UPSTREAM_SPAN_BYTES = 12732
UPSTREAM_SPAN_SHA = "d05781ae58b1b6fd6174d030e52ca9ee6a08048be96f7c103e5be8de473b60b0"
ANCHOR_ORDER_SHA = "c8a52def0a0bce835100035a27bd394722880f09d5404c534dbafef014a0bce0"

FILES = ("artifacts.jsonl", "assets.jsonl", "authority.jsonl", "concepts.jsonl",
         "corrections.jsonl", "qa.jsonl", "relations.jsonl", "rights.jsonl",
         "segments.jsonl", "terms.jsonl", "units.jsonl")
PREFIX = {
    "artifacts.jsonl": (135, 107142, "6e0bee128eb762523c603ae31c2578325f171d61fbcd15ac6c861be6486917b5"),
    "assets.jsonl": (26, 16063, "60d4f100505e27b28bc0642c8849dbc1842926d971642f2210c3a392e3f73eb4"),
    "authority.jsonl": (4, 2721, "f21af26912520ab34b38dff0e927ed46a546dbe5d318da0dc133e58330d0e368"),
    "concepts.jsonl": (319, 100311, "342c1cabc894a64d766dee238ded0a923ef655930421ddfe4d5fcf7f4569c17f"),
    "corrections.jsonl": (322, 316453, "acb12d317419c4df9f43e3743daa4001bf2a99a70c8ca4f55388401a211a488b"),
    "qa.jsonl": (114, 64675, "87e517a10dc7b2295b469770c72ef7aef3f9cef87a6e88e1499eaa249590af45"),
    "relations.jsonl": (368, 149907, "77b3123aff933914316dc636ab0190916f8d922f4900ef5f6b3b79106148b268"),
    "rights.jsonl": (67, 61618, "1e31593a6d4004633f9b27581924ed24a4ab40f11b817df22a9298116eeeb185"),
    "segments.jsonl": (1016, 1313231, "09210c2eaee49c9937ba555f1b18b26332c14297adbd70bcd17830b5ac75e620"),
    "terms.jsonl": (312, 193238, "68e6b19d70650fae488bf4ab7676dbc8e3d9efb1fb1b46de10a0169caafb1665"),
    "units.jsonl": (1040, 1401068, "ca605764e55f79126ac83d3313dd2d7a72626f4b3906573c7bc51ca9a3f1b95d"),
}
PREFIX_RECORDS = 3723
PREFIX_BYTES = 3726427
PREFIX_BUNDLE = "ffa8c7cb45b6d8170d7bc83df24ec487fd0c2777297b55eff2d5e7b3ae63fe25"

FIXED_ARTIFACTS = {
    "artifact:o012-u025-independent-review": (
        "qa/UNIT_025_INDEPENDENT_REVIEW.md", 6933,
        "c7be12ea116b76ea2789b9e1d81cca973ea4d108e97f821eaeba4491ddcb7c08",
        "text/markdown; charset=utf-8", "mathematically_reviewed",
        ["qa:o012-u025-math", "qa:o012-u025-language"]),
    "artifact:o012-u025-source-audit": (
        "qa/UNIT_025_SOURCE_AUDIT.md", 6386,
        "f252e9f15e0980ed2a2c15dfbd1c22fd6fd99990333e2de9a9372f695523e903",
        "text/markdown; charset=utf-8", "source_frozen",
        ["qa:o012-u025-source-integrity"]),
}

TERM_SPECS = {
    "O012-TERM-0323": ("relative cohomology", "kohomologi relatif", "relative-cohomology", "o012-rbt-l25-def-001", "homological_algebra"),
    "O012-TERM-0324": ("reduced cohomology", "kohomologi tereduksi", "reduced-cohomology", "o012-rbt-l25-def-002", "homological_algebra"),
    "O012-TERM-0325": ("pointed Delta-set", "himpunan-Delta bertitik dasar", "pointed-delta-set", "o012-rbt-l25-def-002", "simplicial_topology"),
    "O012-TERM-0326": ("quasi-isomorphism", "kuasi-isomorfisma", "quasi-isomorphism", "o012-rbt-l25-def-003", "homological_algebra"),
    "O012-TERM-0327": ("Five Lemma", "Lema Lima", "five-lemma", "o012-rbt-l25-lem-002", "homological_algebra"),
    "O012-TERM-0328": ("cohomological Euler characteristic", "karakteristik Euler kohomologis", "cohomological-euler-characteristic", "o012-rbt-l25-s04", "algebraic_topology"),
}

EXPECTED_ADVERSE = {
    332: ("P1", "Notes.tex:5383-5395", "corrected_in_translation", ["exa-001", "audit-001"], "mathematical_correction"),
    333: ("P2", "Notes.tex:5398-5402", "proof_completed_in_translation", ["lem-001", "proof-001"], "proof_completion"),
    334: ("P1", "Notes.tex:5408-5419", "proof_completed_in_translation", ["prop-001", "fig-001", "proof-002", "audit-002"], "proof_completion"),
    335: ("P1", "Notes.tex:5449", "corrected_in_translation", ["exa-003", "audit-003"], "mathematical_correction"),
    336: ("P2", "Notes.tex:5556-5557", "clarified_in_translation", ["exa-006", "sol-006"], "clarification"),
    337: ("P1", "Notes.tex:5526-5530", "proof_completed_in_translation", ["lem-002", "fig-002", "proof-003", "audit-004"], "proof_completion"),
    338: ("P1", "Notes.tex:5574-5593", "corrected_in_translation", ["prop-002", "proof-004", "audit-005"], "mathematical_correction"),
    339: ("P1", "Notes.tex:5608", "corrected_in_translation", ["rem-001", "audit-006"], "mathematical_correction"),
    340: ("P2", "Notes.tex:5388,5406,5411-5417,5423-5424,5436,5468,5501,5507-5510,5535,5542", "accessibility_reflow", [*[f"aside-{n:03d}" for n in range(1, 8)], "fig-001", "fig-002"], "structural_adaptation"),
    341: ("P3", "unit-025-lecture-025.md:56 (pre-admission draft)", "resolved_before_admission", ["s01"], "terminology_correction"),
}

BASE_CONCEPTS = (
    "relative-simplicial-cochain-complex", "simplicial-cochain-complex",
    "cochain-map", "long-exact-sequence", "connecting-map", "functoriality",
    "k-skeleton", "euler-characteristic", "coboundary", "cocycle", "kernel",
    "cokernel", "complex", "morphism-of-complexes", "short-exact-sequence",
    "delta-set", "module-over-r", "exact-at",
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
    spec = importlib.util.spec_from_file_location("o012_generic_u025_producer", path)
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
            raise SystemExit(f"{name}: immutable Units 001-024 prefix mismatch")
        if b"\r" in raw or not raw.endswith(b"\n"):
            raise SystemExit(f"{name}: prefix newline mismatch")
        table: dict[str, dict[str, Any]] = {}
        for number, line in enumerate(lines, 1):
            obj = json.loads(line.decode("utf-8"))
            if not isinstance(obj.get("id"), str) or obj["id"] in seen or canon(obj) != line:
                raise SystemExit(f"{name}:{number}: noncanonical/duplicate prefix record")
            seen.add(obj["id"])
            table[obj["id"]] = obj
        tables[name] = table
        bundle.update(name.encode())
        bundle.update(b"\0")
        bundle.update(raw)
    if (len(seen) != PREFIX_RECORDS
            or sum(len(raw) for raw in raw_files.values()) != PREFIX_BYTES
            or bundle.hexdigest() != PREFIX_BUNDLE):
        raise SystemExit("Units 001-024 backend bundle identity mismatch")
    required = {"unit:o012-rbt-u024", PRIOR_RIGHTS,
                "artifact:o012-units-001-024-pdf",
                "qa:o012-units-001-024-build"}
    if not required <= seen:
        raise SystemExit("Unit 24 cumulative prefix closure is incomplete")
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
        raise SystemExit("Unit 25 upstream span mismatch")
    if ("\\lecturenum{25}" not in lines[5369]
            or lines[5610].strip() != ""
            or "\\lecturenum{26}" not in lines[5611]):
        raise SystemExit("Unit 25 source boundary identity mismatch")


def structural_spans(lines: list[str]) -> tuple[list[str], dict[str, tuple[int, int, str]]]:
    opening = re.compile(r"^\s*:::\s+\{[^#}]*#(o012-rbt-l25(?:-[A-Za-z0-9-]+)?)(.*)\}\s*$")
    heading = re.compile(r"^#{1,6}\s+.*\{[^}]*#(o012-rbt-l25(?:-[A-Za-z0-9-]+)?)[^}]*\}\s*$")
    stack: list[tuple[str, int, str]] = []
    spans: dict[str, tuple[int, int, str]] = {}
    ordered: list[str] = []
    for number, line in enumerate(lines, 1):
        hm = heading.match(line)
        if hm:
            ordered.append(hm.group(1))
        fm = opening.match(line)
        if fm:
            ordered.append(fm.group(1))
            stack.append((fm.group(1), number, line))
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
        "o012-rbt-l25-notice": (12, 51), "o012-rbt-l25": (52, 803),
        "o012-rbt-l25-s01": (54, 175), "o012-rbt-l25-s02": (176, 460),
        "o012-rbt-l25-s03": (461, 589), "o012-rbt-l25-s04": (590, 803),
        "o012-rbt-l25-mastery": (804, 1097),
    }
    for ident, (start, end) in heading_spans.items():
        if ident not in ordered or ident not in lines[start - 1]:
            raise SystemExit(f"heading span identity mismatch: {ident}")
        spans[ident] = (start, end, lines[start - 1])
    if (len(ordered) != 59 or len(set(ordered)) != 59
            or set(ordered) != set(spans)
            or digest(("\n".join(ordered) + "\n").encode()) != ANCHOR_ORDER_SHA):
        raise SystemExit("Unit 25 stable-ID inventory/order mismatch")
    return ordered, spans


def unit_kind(ident: str, opener: str) -> str:
    if ident.endswith("-notice"):
        return "notice"
    if ident == "o012-rbt-l25":
        return "lecture"
    if ident.endswith("-mastery"):
        return "mastery_section"
    if re.fullmatch(r"o012-rbt-l25-s\d{2}", ident):
        return "section"
    match = re.search(r"\{\.([A-Za-z][A-Za-z0-9_-]*)", opener)
    kind = (match.group(1).replace("source-audit", "source_audit")
            .replace("source-margin", "source_margin") if match else "")
    allowed = {"aside", "boundary", "definition", "example", "exercise",
               "figure", "hint", "lemma", "proof", "proposition", "remark",
               "solution", "source_audit", "source_margin", "theorem"}
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
    return f"Unit 25 {kind} {ident.rsplit('-', 1)[-1]}"


def verify_qa() -> tuple[int, str]:
    raw = QA_JSON.read_bytes()
    qa = json.loads(raw.decode("utf-8"))
    resolved = qa.get("resolved_findings")
    if (qa.get("status") != "PASS"
            or qa.get("source", {}).get("line_start") != UPSTREAM_START
            or qa.get("source", {}).get("line_end") != UPSTREAM_END
            or qa.get("source", {}).get("span_bytes") != UPSTREAM_SPAN_BYTES
            or qa.get("source", {}).get("span_sha256") != UPSTREAM_SPAN_SHA
            or qa.get("source", {}).get("next_line") != 5612
            or qa.get("unit", {}).get("bytes") != SOURCE_BYTES
            or qa.get("unit", {}).get("lines") != SOURCE_LINES
            or qa.get("unit", {}).get("sha256") != SOURCE_SHA
            or qa.get("unit", {}).get("stable_ids") != 59
            or qa.get("unit", {}).get("fenced_semantic_objects") != 52
            or qa.get("proof_closure", {}).get("mastery_solution_triples") != 6
            or qa.get("model_provenance") != MODEL):
        raise SystemExit("Unit 25 QA content/binding mismatch")
    if (not isinstance(resolved, list) or len(resolved) != 1
            or resolved[0].get("finding_id") != "UNIT025-TERM-P3-001"
            or resolved[0].get("status") != "RESOLVED_BEFORE_ADMISSION"):
        raise SystemExit("Unit 25 resolved terminology finding is not bound")
    checks = qa.get("checks")
    if not isinstance(checks, list) or not checks or any(
            not isinstance(item, dict) or item.get("status") != "PASS" for item in checks):
        raise SystemExit("Unit 25 QA contains a non-passing check")
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
        raise SystemExit("Unit 25 reader identity/newline mismatch")
    raw_lines = raw.splitlines(keepends=True)
    lines = [line.decode("utf-8").rstrip("\n") for line in raw_lines]
    if (len(lines) != SOURCE_LINES or raw.decode("utf-8").count(MODEL) != 1
            or "kompleks korantai simpleksial relatif" not in lines[55]
            or "kompleks korantai simplicial relatif" in raw.decode("utf-8")):
        raise SystemExit("Unit 25 reader line/provenance/terminology mismatch")
    anchors, spans = structural_spans(lines)

    for _control, (source_term, _preferred, slug, _evidence, domain) in TERM_SPECS.items():
        ident = f"concept:{slug}"
        if ident in existing_ids:
            raise SystemExit(f"new Unit 25 concept unexpectedly pre-exists: {ident}")
        concept = common("concept", ident)
        concept.update({"canonical_label": source_term, "domain": domain,
                        "locale_neutral": True})
        add("concepts.jsonl", concept)
    concept_ids = [f"concept:{slug}" for slug in BASE_CONCEPTS] + [
        f"concept:{spec[2]}" for spec in TERM_SPECS.values()]
    if (len(concept_ids) != len(set(concept_ids)) or any(
            ident not in existing_ids and ident not in additions["concepts.jsonl"]
            for ident in concept_ids)):
        raise SystemExit("Unit 25 concept closure mismatch")

    rights_specs = (
        (COMPANION_RIGHTS,
         "Indonesian original mastery, source-audit, proof-completion, and boundary layer for Roberts Unit 25.",
         "Original additions are CC BY 4.0; source-derived material remains separately attributed.",
         [ROOT], None),
        (COMPOSITE_RIGHTS,
         "David Michael Roberts source adaptation plus original Indonesian Unit 25 companions.",
         "Unit 25 source-derived and original layers remain component-distinguishable.",
         [ROOT], None),
        (CUMULATIVE_RIGHTS,
         "Cumulative Roberts Units 001-025 Indonesian reader source boundary.",
         "Source-stage cumulative pointer; the verified Units 001-024 public build remains immutable.",
         [f"unit:o012-rbt-u{number:03d}" for number in range(1, 26)], PRIOR_RIGHTS),
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
        ("o012-rbt-l25-s01", 54, 175), ("o012-rbt-l25-s02", 176, 460),
        ("o012-rbt-l25-s03", 461, 589), ("o012-rbt-l25-s04", 590, 803),
    )
    section_ids = {item[0] for item in section_ranges}

    def parent_local(ident: str, start: int) -> str:
        if ident in {"o012-rbt-l25-notice", "o012-rbt-l25",
                     "o012-rbt-l25-mastery", "o012-rbt-l25-boundary-001"}:
            return ROOT
        if ident in section_ids:
            return LECTURE
        if any(token in ident for token in ("-mcheck-", "-hint-", "-sol-")):
            return MASTERY
        for section, low, high in section_ranges:
            if low <= start <= high:
                return f"unit:{section}"
        raise SystemExit(f"cannot assign Unit 25 parent: {ident}")

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
        "display_title": "Topologi Aljabar - Unit 25: Kohomologi Relatif, Lema Lima, dan Karakteristik Euler",
        "edition_id": EDITION, "edition_unit_id": ROOT, "locale": "id-ID",
        "model_provenance": MODEL, "order": 25, "parent_id": COURSE,
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
        unit = common("unit", unit_id)
        unit.update(shared)
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
        segment = common("segment", f"segment:{ident}")
        segment.update(shared)
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
            unit["source_aliases"] = aliases
            segment["source_aliases"] = aliases
        if ident == "o012-rbt-l25-boundary-001":
            unit["next_source_line"] = 5612
            segment["next_source_line"] = 5612
        if kind == "proof":
            unit["proof_status"] = "complete_original_proof"
            segment["proof_status"] = "complete_original_proof"
        if kind == "solution":
            unit["solution_status"] = "complete_checked_solution"
            segment["solution_status"] = "complete_checked_solution"
        add("units.jsonl", unit)
        add("segments.jsonl", segment)

    asset = common("asset", "asset:o012-u025-source-markdown")
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
        targets = [f"o012-rbt-l25-{suffix}" for suffix in suffixes]
        if any(target not in spans for target in targets):
            raise SystemExit(f"adverse target absent: {event_id}")
        correction = common("correction", f"correction:o012-u025-adv-{number:04d}")
        correction.update({"adverse_ledger_id": event_id,
                           "affected_unit_ids": [f"unit:{target}" for target in targets],
                           "correction_type": correction_type, "edition_id": EDITION,
                           "evidence": source_location,
                           "evidence_segment_id": "segment:o012-rbt-l25-notice",
                           "severity": severity, "rationale": row["rationale"],
                           "resource_id": RESOURCE, "source_defect": row["observed"],
                           "target_change": row["action"], "unit_id": ROOT,
                           "upstream_report_disposition": "not_contacted"})
        add("corrections.jsonl", correction)

    artifact_specs = dict(FIXED_ARTIFACTS)
    artifact_specs["artifact:o012-u025-qa"] = (
        "qa/UNIT_025_QA.json", qa_bytes, qa_sha, "application/json", "built",
        ["qa:o012-u025-source-integrity", "qa:o012-u025-language"])
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
                         "toolchain": (f"Bounded Unit 25 evidence; Notes.tex:5370-5611 "
                                       f"span {UPSTREAM_SPAN_SHA}; {MODEL}; route {ROUTE}; "
                                       "no cumulative-build/publication assertion."),
                         "translation_state": state, "unit_id": ROOT})
        add("artifacts.jsonl", artifact)

    qa_specs = (
        ("qa:o012-u025-source-integrity", "source",
         "Unit 25 authority/reader identities, 59 stable IDs, source census, controls, and Pandoc structure passed.",
         ["artifact:o012-u025-source-audit", "artifact:o012-u025-qa"]),
        ("qa:o012-u025-math", "math",
         "Independent Unit 25 mathematical review passed with no open P1, P2, or P3 finding.",
         ["artifact:o012-u025-independent-review"]),
        ("qa:o012-u025-language", "language",
         "Independent Indonesian language and terminology review passed after resolving UNIT025-TERM-P3-001 before admission.",
         ["artifact:o012-u025-independent-review", "artifact:o012-u025-qa"]),
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
        item.update(extra)
        add("relations.jsonl", item)

    relation("relation:adapts:o012-rbt-u025:edition", ROOT, "adapts", EDITION,
             "Unit 25 is the Indonesian adapted reader boundary for the frozen Roberts edition.")
    relation("relation:precedes:o012-rbt-u024:o012-rbt-u025",
             "unit:o012-rbt-u024", "precedes", ROOT,
             "Preserves contiguous Roberts lecture-unit order.")
    relation("relation:precedes:o012-rbt-l25:mastery", LECTURE, "precedes", MASTERY,
             "Lecture content precedes the Unit 25 mastery companion.")
    relation("relation:boundary:o012-u025", CUMULATIVE_RIGHTS, "contains", ROOT,
             "Additive cumulative Units 001-025 semantic source boundary.")
    relation("relation:route:d60-r13:o012-rbt-u025", COURSE, "contains", ROOT,
             "Roberts Lecture 25 is an edition unit in the non-destructive D60-R13 learner-route view.",
             course_route_unit_id=ROUTE, edition_unit_id=ROOT)
    relation("relation:xref:o012-rbt-l25-exa-002:o012-rbt-l25-exa-001",
             "unit:o012-rbt-l25-exa-002", "xref", "unit:o012-rbt-l25-exa-001",
             "Resolves the source label eg:dim_minus_one_skeleton_rel_cochains to the stable Unit 25 example.")
    proof_targets = {
        1: "unit:o012-rbt-l25-lem-001",
        2: "unit:o012-rbt-l25-prop-001",
        3: "unit:o012-rbt-l25-lem-002",
        4: "unit:o012-rbt-l25-prop-002",
    }
    for number, target in proof_targets.items():
        relation(f"relation:proves:o012-rbt-l25-proof-{number:03d}:closure",
                 f"unit:o012-rbt-l25-proof-{number:03d}", "proves", target,
                 f"Complete proof closure {number} for Unit 25.")
    for number in range(1, 7):
        relation(f"relation:solves:l25-sol-{number:03d}:l25-mcheck-{number:03d}",
                 f"unit:o012-rbt-l25-sol-{number:03d}", "solves",
                 f"unit:o012-rbt-l25-mcheck-{number:03d}",
                 f"Complete checked solution for Unit 25 mastery check {number}.")
        relation(f"relation:hints:l25-hint-{number:03d}:l25-mcheck-{number:03d}",
                 f"unit:o012-rbt-l25-hint-{number:03d}", "hints",
                 f"unit:o012-rbt-l25-mcheck-{number:03d}",
                 f"Bounded hint for Unit 25 mastery check {number}.")

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
        unit = by_id[f"unit:{ident}"]
        segment = by_id[f"segment:{ident}"]
        if unit["target_locator"] != segment["target_locator"]:
            raise SystemExit(f"unit/segment locator mismatch: {ident}")
        if unit["path"][-1] != unit["id"]:
            raise SystemExit(f"noncanonical Unit 25 path: {ident}")
        if unit["parent_id"].startswith("unit:"):
            if unit["path"][:-1] != by_id[unit["parent_id"]]["path"]:
                raise SystemExit(f"Unit 25 parent path mismatch: {ident}")
        for obj in (unit, segment):
            if (obj["edition_unit_id"] != ROOT or obj["course_route_unit_id"] != ROUTE
                    or obj["model_provenance"] != MODEL):
                raise SystemExit(f"Unit 25 route/provenance mismatch: {ident}")
    sibling_orders: defaultdict[str, list[int]] = defaultdict(list)
    for obj in additions["units.jsonl"].values():
        sibling_orders[obj["parent_id"]].append(obj["order"])
    if any(len(values) != len(set(values)) for values in sibling_orders.values()):
        raise SystemExit("duplicate Unit 25 sibling order")
    for number in range(1, 7):
        check = f"unit:o012-rbt-l25-mcheck-{number:03d}"
        solves = [obj for obj in additions["relations.jsonl"].values()
                  if obj["relation_type"] == "solves" and obj["to_id"] == check]
        hints = [obj for obj in additions["relations.jsonl"].values()
                 if obj["relation_type"] == "hints" and obj["to_id"] == check]
        if len(solves) != 1 or len(hints) != 1:
            raise SystemExit(f"Unit 25 mastery closure mismatch: {number}")
    proofs = [obj for obj in additions["units.jsonl"].values()
              if obj.get("proof_status") == "complete_original_proof"]
    if len(proofs) != 4:
        raise SystemExit("Unit 25 four-proof closure mismatch")
    correction_ids = {obj.get("adverse_ledger_id")
                      for obj in additions["corrections.jsonl"].values()}
    if correction_ids != {f"O012-ADV-{number:04d}" for number in range(332, 342)}:
        raise SystemExit("Unit 25 adverse closure mismatch")
    if additions["rights.jsonl"][CUMULATIVE_RIGHTS]["component_scope"] != [
            f"unit:o012-rbt-u{number:03d}" for number in range(1, 26)]:
        raise SystemExit("Unit 25 cumulative rights scope mismatch")
    if by_id["unit:o012-rbt-l25-boundary-001"].get("next_source_line") != 5612:
        raise SystemExit("Unit 25 terminal cursor mismatch")

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
        bundle.update(name.encode())
        bundle.update(b"\0")
        bundle.update(outputs[name])
    counts = {name: len(additions[name]) for name in FILES}
    print("Unit 025 semantic backend extension: PASS")
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
