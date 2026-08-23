#!/usr/bin/env python3
"""Fail-closed append-only backend admission for frozen Roberts Unit 022.

The public Units 001--021 backend is an immutable 3,111-record prefix.  This
producer verifies every prefix file, the frozen Unit 22 reader/evidence and the
exact terminology/adverse controls, constructs the semantic suffix entirely in
memory, validates its closure, and only then appends canonical sorted JSONL.
It deliberately records no cumulative build or publication artifact.
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
SOURCE = LANE / "source/id-ID/units/unit-022-lecture-022.md"
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
COMPANION_RIGHTS = "rights:o012-u022-companion-cc-by-4.0"
COMPOSITE_RIGHTS = "rights:o012-u022-composite-cc-by-4.0"
CUMULATIVE_RIGHTS = "rights:o012-units-001-022-composite-cc-by-4.0"
PRIOR_RIGHTS = "rights:o012-units-001-021-composite-cc-by-4.0-final-47fa"
ROOT = "unit:o012-rbt-u022"
LECTURE = "unit:o012-rbt-l22"
MASTERY = "unit:o012-rbt-l22-mastery"
SOURCE_BYTES = 44066
SOURCE_LINES = 1349
SOURCE_SHA = "0857e51568d77c811d5d79255ac75bfddc87a04b27356ae457d4e66eeffb7d0d"
UPSTREAM_SPAN_SHA = "86275c590cfcdf8519d3ce8d077fc48619bb94c3fdf039ca805ae4b7df995b7f"
UPSTREAM_RAW_SHA = "de8b63537d295d5a6d85591be81863ae4416a14323b13b1517153465f0cb9a12"
ANCHOR_ORDER_SHA = "0d184ad4d848e50b4e8f73f8f44e314f0fe2a3dd1a2ec3f31476f730fea31099"
FILES = ("artifacts.jsonl", "assets.jsonl", "authority.jsonl", "concepts.jsonl",
         "corrections.jsonl", "qa.jsonl", "relations.jsonl", "rights.jsonl",
         "segments.jsonl", "terms.jsonl", "units.jsonl")
PREFIX = {
    "artifacts.jsonl": (106, 83103, "1708f7276cb28e295d578c8e4411618291c7294c8faee863c89461c63378a978"),
    "assets.jsonl": (23, 14215, "623f8d7948504405fb8f57379987136e5f89297f0152f3eb9408cab6a3ed153c"),
    "authority.jsonl": (4, 2721, "f21af26912520ab34b38dff0e927ed46a546dbe5d318da0dc133e58330d0e368"),
    "concepts.jsonl": (289, 90816, "b05d4ec9646338ea76991eb08d5a260a087699a76d51fde507b0c5583b5921bb"),
    "corrections.jsonl": (288, 280684, "7c06a04c7072051d28879297291d37bccca70c132339c8226e889701dc1de835"),
    "qa.jsonl": (99, 56340, "249c2f6110269d1daef7fff472e4fb17c2f7060b8cd39f662884fd8bba0f0145"),
    "relations.jsonl": (284, 114295, "3a1b930dbe14992819fcaeca39edb96e915641e62247a2e7ea879809a998c2e9"),
    "rights.jsonl": (55, 49832, "1dca76e63699015d393009a8ed263ea4f1adb4e9be3a9668aae8e19bdcf55524"),
    "segments.jsonl": (830, 982695, "e3fc479798493bad011f36e302cd4da7b0daa48f45252d7095dc10adc50b3530"),
    "terms.jsonl": (282, 171661, "f6bb58da10c5970087c4ff2074b25163a3a3bd6e0f820f9df0782a4e00490deb"),
    "units.jsonl": (851, 1050067, "7851c5a529337802a6eb62f7aa51d107c38e18ecf8299fcfc86d6dc5b87c46a6"),
}
PREFIX_BUNDLE = "cf5acacf3ad2351869297dd8d3827787377422fa30c8c1385e60833b23913db9"
ARTIFACTS = {
    "artifact:o012-u022-independent-review": (
        "qa/UNIT_022_INDEPENDENT_REVIEW.md", 2893,
        "6632c22c2aa9339c169382111c0c28750e91a61bbb7ed40d47fe4734cefc7004",
        "text/markdown; charset=utf-8", "mathematically_reviewed",
        ["qa:o012-u022-math", "qa:o012-u022-language"]),
    "artifact:o012-u022-source-audit": (
        "qa/UNIT_022_SOURCE_AUDIT.md", 4519,
        "50e0c9268f19c1fc3d6a9f865b6c338940e0edb1c336386566030a7595695801",
        "text/markdown; charset=utf-8", "source_frozen",
        ["qa:o012-u022-source-integrity"]),
    "artifact:o012-u022-qa": (
        "qa/UNIT_022_QA.json", 4167,
        "4b9e62ca0912eb3cd989130a643fc07b9634ffa421f989d92ec3d8676eea8fe7",
        "application/json", "built", ["qa:o012-u022-source-integrity"]),
    "artifact:o012-u022-translation-handoff": (
        "qa/UNIT_022_TRANSLATION_HANDOFF.md", 2045,
        "9804d4372f4dc80c963bd6dca86ab5f8e79c6959f334526adc4f02e92507ccbf",
        "text/markdown; charset=utf-8", "source_frozen",
        ["qa:o012-u022-source-integrity", "qa:o012-u022-language"]),
}
TERM_SPECS = {
    "O012-TERM-0293": ("Delta-set", "himpunan-Delta", "delta-set",
                        "o012-rbt-l22-def-002", "simplicial_topology"),
    "O012-TERM-0294": ("k-skeleton", "k-kerangka", "k-skeleton",
                        "o012-rbt-l22-exa-001", "simplicial_topology"),
    "O012-TERM-0295": ("simplicial cochain complex", "kompleks korantai simpleksial",
                        "simplicial-cochain-complex", "o012-rbt-l22-s05",
                        "homological_algebra"),
    "O012-TERM-0296": ("opposite category", "kategori lawan", "opposite-category",
                        "o012-rbt-l22-s05", "category_theory"),
    "O012-TERM-0297": ("contravariant functor", "fungtor kontravarian",
                        "contravariant-functor", "o012-rbt-l22-lem-004",
                        "category_theory"),
    "O012-TERM-0298": ("change of coefficients", "perubahan koefisien",
                        "change-of-coefficients", "o012-rbt-l22-lem-005",
                        "homological_algebra"),
    "O012-TERM-0299": ("Betti number", "bilangan Betti", "betti-number",
                        "o012-rbt-l22-rem-003", "algebraic_topology"),
    "O012-TERM-0300": ("torsion coefficient", "koefisien torsi",
                        "torsion-coefficient", "o012-rbt-l22-rem-003",
                        "algebraic_topology"),
}
EXPECTED_ADVERSE = {
    298: ("P2", "Notes.tex:4522-4523", "corrected_in_translation",
          ["exa-002", "audit-001"], "mathematical_correction"),
    299: ("P1", "Notes.tex:4537-4598", "corrected_in_translation",
          ["exa-004", "fig-001", "audit-002"], "structural_adaptation"),
    300: ("P2", "Notes.tex:4608-4632", "proof_completed_in_translation",
          ["lem-001", "proof-001", "audit-003"], "proof_completion"),
    301: ("P2", "Notes.tex:4692-4701", "clarified_in_translation",
          ["def-002", "audit-004"], "clarification"),
    302: ("P2", "Notes.tex:4703-4715", "corrected_in_translation",
          ["def-003", "def-004", "audit-005"], "mathematical_correction"),
    303: ("P1", "Notes.tex:4764-4767", "corrected_in_translation",
          ["exa-009", "audit-006"], "mathematical_correction"),
    304: ("P1", "Notes.tex:4830-4845", "proof_completed_in_translation",
          ["audit-007", "lem-003", "proof-002"], "proof_completion"),
    305: ("P2", "Notes.tex:4858-4865", "proof_completed_in_translation",
          ["lem-004", "proof-003"], "proof_completion"),
    306: ("P1", "Notes.tex:4879-4880", "corrected_in_translation",
          ["def-006", "audit-008"], "mathematical_correction"),
    307: ("P3", "Notes.tex:4899-4900", "corrected_in_translation",
          ["audit-008"], "editorial_correction"),
    308: ("P1", "Notes.tex:4911-4916", "clarified_in_translation",
          ["exa-010", "audit-009"], "clarification"),
    309: ("P2", "Notes.tex:4528-4529,4543-4594,4623-4630,4645-4647,4720-4730,4783-4815,4880",
          "accessibility_reflow",
          [*[f"margin-{n:03d}" for n in range(1, 6)],
           *[f"fig-{n:03d}" for n in range(1, 6)]], "structural_adaptation"),
    310: ("P3", "Notes.tex:4512,4529,4532,4598,4700,4747,4765,4815,4887,4890",
          "corrected_in_translation", ["audit-010"], "editorial_correction"),
    311: ("P2", "Unit22 mastery hint 22.6", "corrected_after_independent_review",
          ["hint-006", "sol-006"], "mathematical_correction"),
}
BASE_CONCEPTS = (
    "complex", "coboundary", "cohomologically-graded-complex",
    "euler-characteristic", "geometric-realisation", "module-over-r",
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


def load_prefix() -> tuple[dict[str, dict[str, dict[str, Any]]], dict[str, bytes]]:
    tables: dict[str, dict[str, dict[str, Any]]] = {}
    raw_files: dict[str, bytes] = {}
    bundle = hashlib.sha256()
    for name in FILES:
        raw = (BACKEND / name).read_bytes()
        raw_files[name] = raw
        count, size, expected_sha = PREFIX[name]
        if len(raw) != size or digest(raw) != expected_sha:
            raise SystemExit(f"{name}: immutable Units 001-021 prefix mismatch")
        lines = raw.splitlines(keepends=True)
        if len(lines) != count or b"\r" in raw or not raw.endswith(b"\n"):
            raise SystemExit(f"{name}: prefix count/newline mismatch")
        table: dict[str, dict[str, Any]] = {}
        for number, line in enumerate(lines, 1):
            obj = json.loads(line.decode("utf-8"))
            if not isinstance(obj.get("id"), str) or obj["id"] in table or canon(obj) != line:
                raise SystemExit(f"{name}:{number}: noncanonical/duplicate prefix record")
            table[obj["id"]] = obj
        tables[name] = table
        bundle.update(name.encode()); bundle.update(b"\0"); bundle.update(raw)
    if bundle.hexdigest() != PREFIX_BUNDLE:
        raise SystemExit("Units 001-021 backend bundle identity mismatch")
    return tables, raw_files


def structural_spans(lines: list[str]) -> tuple[list[str], dict[str, tuple[int, int, str]]]:
    opening = re.compile(r"^:::\s+\{[^#}]*#(o012-rbt-l22(?:-[A-Za-z0-9-]+)?)(.*)\}\s*$")
    heading = re.compile(r"^#{1,6}\s+.*\{[^}]*#(o012-rbt-l22(?:-[A-Za-z0-9-]+)?)[^}]*\}\s*$")
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
                raise SystemExit(f"unexpected div close at source line {number}")
            ident, start, opener = stack.pop()
            if ident in spans:
                raise SystemExit(f"duplicate fenced anchor: {ident}")
            spans[ident] = (start, number, opener)
    if stack:
        raise SystemExit(f"unclosed div anchors: {[item[0] for item in stack]}")
    heading_spans = {
        "o012-rbt-l22-notice": (12, 58), "o012-rbt-l22": (60, 1027),
        "o012-rbt-l22-s01": (62, 347), "o012-rbt-l22-s02": (349, 469),
        "o012-rbt-l22-s03": (471, 672), "o012-rbt-l22-s04": (674, 723),
        "o012-rbt-l22-s05": (725, 1027), "o012-rbt-l22-mastery": (1029, 1342),
    }
    for ident, (start, end) in heading_spans.items():
        if ident not in ordered or ident not in lines[start - 1]:
            raise SystemExit(f"heading span identity mismatch: {ident}")
        spans[ident] = (start, end, lines[start - 1])
    if len(ordered) != 75 or len(set(ordered)) != 75 or set(ordered) != set(spans):
        raise SystemExit("Unit 22 stable-ID closure mismatch")
    order_sha = digest(("\n".join(ordered) + "\n").encode())
    if order_sha != ANCHOR_ORDER_SHA:
        raise SystemExit(f"Unit 22 stable-ID order mismatch: {order_sha}")
    return ordered, spans


def unit_kind(ident: str, opener: str) -> str:
    if ident.endswith("-notice"): return "notice"
    if ident == "o012-rbt-l22": return "lecture"
    if ident.endswith("-mastery"): return "mastery_section"
    if re.fullmatch(r"o012-rbt-l22-s\d{2}", ident): return "section"
    match = re.search(r"\{\.([A-Za-z][A-Za-z0-9_-]*)", opener)
    kind = match.group(1).replace("source-audit", "source_audit").replace(
        "source-margin", "source_margin") if match else ""
    if kind not in {"definition", "example", "source_audit", "source_margin",
                    "lemma", "proof", "figure", "remark", "exercise", "hint",
                    "solution", "boundary"}:
        raise SystemExit(f"cannot infer kind for {ident}: {kind!r}")
    return kind


def is_original(ident: str, kind: str) -> bool:
    return (kind in {"notice", "source_audit", "mastery_section", "boundary",
                     "hint", "solution"}
            or "-mcheck-" in ident or ident == "o012-rbt-l22-proof-002")


def target_locator(path: str, start: int, end: int, file_sha: str,
                   raw_lines: list[bytes]) -> dict[str, Any]:
    return {"content_sha256": digest(b"".join(raw_lines[start - 1:end])),
            "file_sha256": file_sha, "line_end": end, "line_start": start,
            "path": path}


def source_locator(original: bool) -> dict[str, Any]:
    if original:
        return {"kind": "edition_original",
                "path": "source/id-ID/units/unit-022-lecture-022.md",
                "precision": "exact_target_span"}
    return {"commit_sha": COMMIT, "line_end": 4938, "line_start": 4501,
            "path": "Notes.tex", "precision": "unit_range_only"}


def display_title(ident: str, lines: list[str], start: int, kind: str) -> str:
    first = lines[start - 1].strip()
    if first.startswith("#"):
        return re.sub(r"\s*\{.*\}$", "", re.sub(r"^#+\s*", "", first)).strip()
    for line in lines[start:min(start + 6, len(lines))]:
        text = line.strip().replace("**", "")
        if text and not text.startswith(":::"):
            return text[:180]
    return f"Unit 22 {kind} {ident.rsplit('-', 1)[-1]}"


def main() -> None:
    tables, prefix_raw = load_prefix()
    existing_ids = {ident for table in tables.values() for ident in table}
    additions: dict[str, dict[str, dict[str, Any]]] = {name: {} for name in FILES}

    def add(name: str, obj: dict[str, Any]) -> None:
        ident = obj["id"]
        if ident in existing_ids or any(ident in table for table in additions.values()):
            raise SystemExit(f"duplicate new ID: {ident}")
        additions[name][ident] = obj

    raw = SOURCE.read_bytes()
    if len(raw) != SOURCE_BYTES or digest(raw) != SOURCE_SHA or b"\r" in raw:
        raise SystemExit(f"Unit 22 identity mismatch: {len(raw)} {digest(raw)}")
    raw_lines = raw.splitlines(keepends=True)
    lines = [line.decode("utf-8").rstrip("\n") for line in raw_lines]
    if len(lines) != SOURCE_LINES:
        raise SystemExit("Unit 22 line count mismatch")
    anchors, spans = structural_spans(lines)

    for control, (source_term, _preferred, slug, _evidence, domain) in TERM_SPECS.items():
        ident = f"concept:{slug}"
        if ident in existing_ids:
            raise SystemExit(f"{control}: concept unexpectedly pre-exists")
        concept = common("concept", ident)
        concept.update({"canonical_label": source_term, "domain": domain,
                        "locale_neutral": True})
        add("concepts.jsonl", concept)
    concept_ids = [f"concept:{slug}" for slug in BASE_CONCEPTS] + [
        f"concept:{spec[2]}" for spec in TERM_SPECS.values()]
    if len(concept_ids) != len(set(concept_ids)) or any(
            ident not in existing_ids and ident not in additions["concepts.jsonl"]
            for ident in concept_ids):
        raise SystemExit("Unit 22 concept closure mismatch")

    rights_specs = (
        (COMPANION_RIGHTS,
         "Indonesian original mastery, source-audit, proof-completion, and boundary layer for Roberts Unit 22.",
         "Original additions are CC BY 4.0; source-derived material remains separately attributed.",
         [ROOT], None),
        (COMPOSITE_RIGHTS,
         "David Michael Roberts source adaptation plus original Indonesian Unit 22 companions.",
         "Unit 22 source-derived and original layers remain component-distinguishable.",
         [ROOT], None),
        (CUMULATIVE_RIGHTS,
         "Cumulative Roberts Units 001-022 Indonesian reader source boundary.",
         "Source-stage cumulative pointer; the verified Units 001-021 build boundary remains immutable.",
         [f"unit:o012-rbt-u{number:03d}" for number in range(1, 23)], PRIOR_RIGHTS),
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
        ("o012-rbt-l22-s01", 62, 347), ("o012-rbt-l22-s02", 349, 469),
        ("o012-rbt-l22-s03", 471, 672), ("o012-rbt-l22-s04", 674, 723),
        ("o012-rbt-l22-s05", 725, 1027),
    )
    section_ids = {item[0] for item in section_ranges}

    def parent_local(ident: str, start: int) -> str:
        if ident in {"o012-rbt-l22-notice", "o012-rbt-l22",
                     "o012-rbt-l22-mastery", "o012-rbt-l22-boundary-001"}:
            return ROOT
        if ident in section_ids:
            return LECTURE
        if any(token in ident for token in ("-mcheck-", "-hint-", "-sol-")):
            return MASTERY
        for section, low, high in section_ranges:
            if low <= start <= high:
                return f"unit:{section}"
        raise SystemExit(f"cannot assign Unit 22 parent: {ident}")

    children: defaultdict[str, list[str]] = defaultdict(list)
    for ident in anchors:
        children[parent_local(ident, spans[ident][0])].append(ident)
    order_map = {parent: {ident: number for number, ident in enumerate(
        sorted(items, key=lambda item: spans[item][0]), 1)}
        for parent, items in children.items()}
    path_by_id: dict[str, list[str]] = {ROOT: [ROOT]}
    root = common("unit", ROOT)
    root.update({
        "concept_ids": concept_ids, "course_id": COURSE,
        "display_title": "Topologi Aljabar - Unit 22: Himpunan-Delta, Realisasi, dan Korantai",
        "edition_id": EDITION, "locale": "id-ID", "order": 22,
        "parent_id": COURSE, "path": [ROOT], "program_id": PROGRAM,
        "provenance_relation": "composite_translated_and_original",
        "resource_id": RESOURCE, "rights_component_id": COMPOSITE_RIGHTS,
        "source_local_id": None,
        "target_locator": target_locator(
            "source/id-ID/units/unit-022-lecture-022.md", 1, SOURCE_LINES,
            SOURCE_SHA, raw_lines),
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
        locator = target_locator(
            "source/id-ID/units/unit-022-lecture-022.md", start, end,
            SOURCE_SHA, raw_lines)
        unit = common("unit", unit_id)
        unit.update({
            "concept_ids": concept_ids, "course_id": COURSE,
            "display_title": display_title(ident, lines, start, kind),
            "edition_id": EDITION, "locale": "id-ID",
            "order": order_map[parent_id][ident], "parent_id": parent_id,
            "path": path, "program_id": PROGRAM,
            "provenance_relation": ("edition_original" if original
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

    asset = common("asset", "asset:o012-u022-source-markdown")
    asset.update({"bytes": SOURCE_BYTES, "edition_id": EDITION,
                  "media_type": "text/markdown; charset=utf-8",
                  "path": "source/id-ID/units/unit-022-lecture-022.md",
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
                     "preferred": preferred, "register": "textbook", "rejected_forms": [],
                     "rights_component_id": ROBERTS_RIGHTS, "scope_unit_id": ROOT,
                     "source_term": source_term, "terminology_control_id": control,
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
        targets = [f"o012-rbt-l22-{suffix}" for suffix in suffixes]
        if any(target not in spans for target in targets):
            raise SystemExit(f"adverse target absent: {event_id}")
        correction = common("correction", f"correction:o012-u022-adv-{number:04d}")
        correction.update({
            "adverse_ledger_id": event_id,
            "affected_unit_ids": [f"unit:{target}" for target in targets],
            "correction_type": correction_type, "edition_id": EDITION,
            "evidence": source_location,
            "evidence_segment_id": "segment:o012-rbt-l22-notice",
            "severity": severity, "rationale": row["rationale"],
            "resource_id": RESOURCE, "source_defect": row["observed"],
            "target_change": row["action"], "unit_id": ROOT,
            "upstream_report_disposition": "not_contacted",
        })
        add("corrections.jsonl", correction)

    for ident, (relative, size, expected_sha, media_type, state, qa_ids) in ARTIFACTS.items():
        artifact_raw = (LANE / relative).read_bytes()
        if len(artifact_raw) != size or digest(artifact_raw) != expected_sha:
            raise SystemExit(f"evidence identity mismatch: {relative}")
        artifact = common("artifact", ident)
        artifact.update({
            "bytes": size, "locale": "id-ID", "manifest_artifact_id": None,
            "media_type": media_type, "path": relative, "qa_event_ids": qa_ids,
            "rights_component_id": COMPOSITE_RIGHTS, "sha256": expected_sha,
            "toolchain": (f"Bounded Unit 22 evidence; Notes.tex:4501-4938 span "
                          f"{UPSTREAM_SPAN_SHA}; OpenAI Codex gpt-5.6-sol, Ultra; "
                          "no cumulative-build/publication assertion."),
            "translation_state": state, "unit_id": ROOT,
        })
        add("artifacts.jsonl", artifact)
    qa_specs = (
        ("qa:o012-u022-source-integrity", "source",
         "Unit 22 exact reader/source identities, 75 stable IDs, source census, terminology, adverse closure, and Pandoc structure passed.",
         ["artifact:o012-u022-source-audit", "artifact:o012-u022-qa",
          "artifact:o012-u022-translation-handoff"]),
        ("qa:o012-u022-math", "math",
         "Independent Unit 22 mathematical review passed with no open P1, P2, or P3 finding.",
         ["artifact:o012-u022-independent-review"]),
        ("qa:o012-u022-language", "language",
         "Independent Indonesian language, terminology, attribution, and accessibility review passed.",
         ["artifact:o012-u022-independent-review",
          "artifact:o012-u022-translation-handoff"]),
    )
    for ident, qa_type, note, witnesses in qa_specs:
        event = common("qa_event", ident)
        event.update({"note": note, "qa_type": qa_type, "result": "passed",
                      "unit_id": ROOT, "witness_artifact_ids": witnesses})
        add("qa.jsonl", event)

    def relation(ident: str, source_id: str, relation_type: str,
                 target_id: str, note: str) -> None:
        item = common("relation", ident)
        item.update({"from_id": source_id, "note": note,
                     "relation_type": relation_type, "to_id": target_id})
        add("relations.jsonl", item)

    relation("relation:adapts:o012-rbt-u022:edition", ROOT, "adapts", EDITION,
             "Unit 22 is the Indonesian adapted reader boundary for the frozen Roberts edition.")
    relation("relation:precedes:o012-rbt-u021:o012-rbt-u022",
             "unit:o012-rbt-u021", "precedes", ROOT,
             "Preserves contiguous Roberts lecture-unit order.")
    relation("relation:precedes:o012-rbt-l22:mastery", LECTURE, "precedes", MASTERY,
             "Lecture content precedes the Unit 22 mastery companion.")
    relation("relation:boundary:o012-u022", CUMULATIVE_RIGHTS, "contains", ROOT,
             "Additive cumulative Units 001-022 source boundary; prior verified build retained.")
    relation("relation:xref:o012-rbt-l22-exa-004:eg-infinite-cylinder",
             "unit:o012-rbt-l22-exa-004", "xref", EDITION,
             "Preserves upstream source label eg:infinite_cylinder.")
    relation("relation:xref:o012-rbt-l22-exa-008:eg-name-of-simplex",
             "unit:o012-rbt-l22-exa-008", "xref", EDITION,
             "Preserves upstream source label eg:name_of_simplex and its active reference.")
    relation("relation:proves:o012-rbt-l22-proof-002:lem-003",
             "unit:o012-rbt-l22-proof-002", "proves", "unit:o012-rbt-l22-lem-003",
             "Edition-original complete signed-cancellation proof closes the source Exercise! omission.")
    for number in range(1, 7):
        relation(f"relation:solves:l22-sol-{number:03d}:l22-mcheck-{number:03d}",
                 f"unit:o012-rbt-l22-sol-{number:03d}", "solves",
                 f"unit:o012-rbt-l22-mcheck-{number:03d}",
                 f"Complete solution for Unit 22 mastery check {number}.")
        relation(f"relation:hints:l22-hint-{number:03d}:l22-mcheck-{number:03d}",
                 f"unit:o012-rbt-l22-hint-{number:03d}", "hints",
                 f"unit:o012-rbt-l22-mcheck-{number:03d}",
                 f"Bounded hint for Unit 22 mastery check {number}.")

    merged = {name: dict(tables[name]) for name in FILES}
    for name in FILES:
        merged[name].update(additions[name])
    by_id = {ident: obj for table in merged.values() for ident, obj in table.items()}
    if len(by_id) != sum(len(table) for table in merged.values()):
        raise SystemExit("global duplicate backend IDs")
    scalar_refs = {"concept_id", "course_id", "edition_id", "evidence_segment_id",
                   "from_id", "manifest_artifact_id", "parent_id", "program_id",
                   "resource_id", "rights_component_id", "scope_unit_id", "to_id",
                   "unit_id", "supersedes"}
    list_refs = {"affected_unit_ids", "component_scope", "concept_ids",
                 "local_derivative_unit_ids", "qa_event_ids", "witness_artifact_ids"}
    for ident, obj in by_id.items():
        for field in scalar_refs:
            value = obj.get(field)
            if value is not None and value not in by_id:
                raise SystemExit(f"unknown reference {ident}.{field}={value}")
        for field in list_refs:
            if field in obj and any(value not in by_id for value in obj[field]):
                raise SystemExit(f"unknown list reference {ident}.{field}")
    for ident in anchors:
        unit = by_id[f"unit:{ident}"]
        segment = by_id[f"segment:{ident}"]
        if unit["target_locator"] != segment["target_locator"]:
            raise SystemExit(f"unit/segment locator mismatch: {ident}")
        if unit["path"][-1] != unit["id"]:
            raise SystemExit(f"noncanonical Unit 22 path: {ident}")
        if unit["parent_id"].startswith("unit:"):
            parent = by_id[unit["parent_id"]]
            if unit["path"][:-1] != parent["path"]:
                raise SystemExit(f"Unit 22 parent path mismatch: {ident}")
    sibling_orders: defaultdict[str, list[int]] = defaultdict(list)
    for obj in additions["units.jsonl"].values():
        sibling_orders[obj["parent_id"]].append(obj["order"])
    if any(len(values) != len(set(values)) for values in sibling_orders.values()):
        raise SystemExit("duplicate Unit 22 sibling order")
    for number in range(1, 7):
        check = f"unit:o012-rbt-l22-mcheck-{number:03d}"
        solves = [obj for obj in additions["relations.jsonl"].values()
                  if obj["relation_type"] == "solves" and obj["to_id"] == check]
        hints = [obj for obj in additions["relations.jsonl"].values()
                 if obj["relation_type"] == "hints" and obj["to_id"] == check]
        if len(solves) != 1 or len(hints) != 1:
            raise SystemExit(f"mastery closure mismatch: {number}")
    correction_ids = {obj.get("adverse_ledger_id")
                      for obj in additions["corrections.jsonl"].values()}
    if correction_ids != {f"O012-ADV-{number:04d}" for number in range(298, 312)}:
        raise SystemExit("Unit 22 adverse closure mismatch")
    if additions["rights.jsonl"][CUMULATIVE_RIGHTS]["component_scope"] != [
            f"unit:o012-rbt-u{number:03d}" for number in range(1, 23)]:
        raise SystemExit("Unit 22 cumulative rights scope mismatch")

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
    print("Unit 022 backend extension: PASS")
    print("new_records_by_file=" + json.dumps(counts, sort_keys=True))
    print(f"new_records={sum(counts.values())}")
    print(f"total_records={sum(PREFIX[name][0] + counts[name] for name in FILES)}")
    print(f"backend_bytes={sum(len(raw) for raw in outputs.values())}")
    print(f"backend_bundle_sha256={bundle.hexdigest()}")
    print(f"source_sha256={SOURCE_SHA}")
    print(f"upstream_span_sha256={UPSTREAM_SPAN_SHA}")
    print(f"upstream_raw_sha256={UPSTREAM_RAW_SHA}")


if __name__ == "__main__":
    main()
