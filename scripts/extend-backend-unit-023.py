#!/usr/bin/env python3
"""Fail-closed append-only backend admission for frozen Roberts Unit 023.

The public Units 001--022 backend is an immutable 3,337-record prefix.  This
producer verifies that prefix, the exact Unit 23 reader/evidence/controls, and
the frozen upstream span before constructing the complete semantic suffix in
memory.  It writes only after referential, hierarchy, route, proof, mastery,
rights, and continuation closure pass.  No cumulative build or publication
artifact is admitted here.
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
SOURCE = LANE / "source/id-ID/units/unit-023-lecture-023.md"
UPSTREAM = (LANE / "authority/upstream" /
            "AlgebraicTopology2019-b947ad2e9f9e301bfe24590a9db653bc54fa1a53" /
            "Notes.tex")
AUDIT = LANE / "qa/UNIT_023_SOURCE_AUDIT.md"
REVIEW = LANE / "qa/UNIT_023_INDEPENDENT_REVIEW.md"
QA_JSON = LANE / "qa/UNIT_023_QA.json"
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
COMPANION_RIGHTS = "rights:o012-u023-companion-cc-by-4.0"
COMPOSITE_RIGHTS = "rights:o012-u023-composite-cc-by-4.0"
CUMULATIVE_RIGHTS = "rights:o012-units-001-023-composite-cc-by-4.0"
PRIOR_RIGHTS = "rights:o012-units-001-022-composite-cc-by-4.0-final-0857"
ROOT = "unit:o012-rbt-u023"
LECTURE = "unit:o012-rbt-l23"
MASTERY = "unit:o012-rbt-l23-mastery"
SOURCE_PATH = "source/id-ID/units/unit-023-lecture-023.md"
SOURCE_BYTES = 39176
SOURCE_LINES = 1094
SOURCE_SHA = "6f05ddbe6a720109797976c6929b0535f21a38353673cb42d9646a3196f56bd2"
UPSTREAM_BYTES = 331447
UPSTREAM_LINES = 6368
UPSTREAM_SHA = "cfe93e9dbe3e25bd96f711f59e6078ab97527682b58e1f8ad127f74357f665d7"
UPSTREAM_START = 4939
UPSTREAM_END = 5112
UPSTREAM_SPAN_BYTES = 9776
UPSTREAM_SPAN_SHA = "c7256a45621ad7a435277867298e4aeb8eb584dfce066cdae3b48c4ee0e0e3f4"
UPSTREAM_THROUGH_CLOSE_SHA = "b9b54862d6c462344ecdf0da9b9633f52b5ff185722c08444fb7022863b79dc3"
ANCHOR_ORDER_SHA = "77b2e8f91fe5bd7f4c76c83120b7619fa3b07d6dd59f934bcd55d458b98f5fc1"

FILES = ("artifacts.jsonl", "assets.jsonl", "authority.jsonl", "concepts.jsonl",
         "corrections.jsonl", "qa.jsonl", "relations.jsonl", "rights.jsonl",
         "segments.jsonl", "terms.jsonl", "units.jsonl")
PREFIX = {
    "artifacts.jsonl": (116, 91395, "05a9525a470df9a106ad785a026b45f8913c1dfc40d363eff12df5cea3d0a58e"),
    "assets.jsonl": (24, 14831, "69020caaf45628941c57ee5cf58f3c11a31505c3416ec9d65c9ac82b47ba97aa"),
    "authority.jsonl": (4, 2721, "f21af26912520ab34b38dff0e927ed46a546dbe5d318da0dc133e58330d0e368"),
    "concepts.jsonl": (297, 93358, "2e8f93bfa8b7622960716b8a6bd33811c630c877696c5cbf031cb14eadfa110b"),
    "corrections.jsonl": (302, 295241, "718a14732930b546a3c38bf2e131d23066b2f90f09d4dd80a781294296f5cbc6"),
    "qa.jsonl": (104, 59176, "b8c439539b4bd566bb3b46423e19ab925f2cbcb8075a77b5df6a76ba7b9cf516"),
    "relations.jsonl": (309, 124723, "2d58a794206f07915c18c98c220e143354429c57d14bc93f27eb1806a2277ab6"),
    "rights.jsonl": (59, 53720, "f734f3649cc4e8a40ec7d63bd92843c1d04cf835d46f9fcef9224168a9142bd2"),
    "segments.jsonl": (905, 1094552, "491b68e826f0221353d7a7782515be769fc8048e468bba5937c797ca0390bb8c"),
    "terms.jsonl": (290, 177339, "bf1c79fc4bbaf0a9bd71545f4d69d9dc36dcb728f23710ad33a9bf9791421695"),
    "units.jsonl": (927, 1169478, "56fdf925d6e547b4a936d4ac7fb483cdbd9d845ac292989a7162efae108fcf8f"),
}
PREFIX_RECORDS = 3337
PREFIX_BYTES = 3176534
PREFIX_BUNDLE = "38b98ca6258133036ded9e3cb72894f4181d4b6faa46af9e96a2128ab25c9df2"

FIXED_ARTIFACTS = {
    "artifact:o012-u023-independent-review": (
        "qa/UNIT_023_INDEPENDENT_REVIEW.md", 3149,
        "dce8f82872186285c85a42b61b1bbf8fb9fd8e809eea5bccd6367dc87958c880",
        "text/markdown; charset=utf-8", "mathematically_reviewed",
        ["qa:o012-u023-math", "qa:o012-u023-language"]),
    "artifact:o012-u023-source-audit": (
        "qa/UNIT_023_SOURCE_AUDIT.md", 5254,
        "4777f7c14d35e5fb977955818ff7ab133ecc91adb3575867f0e97f8ff00d28b3",
        "text/markdown; charset=utf-8", "source_frozen",
        ["qa:o012-u023-source-integrity"]),
}

TERM_SPECS = {
    "O012-TERM-0301": ("augmentation", "augmentasi", "augmentation", "o012-rbt-l23-s01", "homological_algebra"),
    "O012-TERM-0302": ("augmented module", "modul teraugmentasi", "augmented-module", "o012-rbt-l23-s01", "homological_algebra"),
    "O012-TERM-0303": ("direct sum", "jumlah langsung", "direct-sum", "o012-rbt-l23-s02", "algebra"),
    "O012-TERM-0304": ("product of modules", "produk modul", "product-of-modules", "o012-rbt-l23-margin-003", "algebra"),
    "O012-TERM-0305": ("direct product", "produk langsung", "direct-product", "o012-rbt-l23-s02", "algebra"),
    "O012-TERM-0306": ("restriction map", "pemetaan restriksi", "restriction-map", "o012-rbt-l23-s03", "homological_algebra"),
    "O012-TERM-0307": ("sub-Delta-set", "sub-himpunan-Delta", "sub-delta-set", "o012-rbt-l23-s03", "simplicial_topology"),
    "O012-TERM-0308": ("pair of Delta-sets", "pasangan himpunan-Delta", "pair-of-delta-sets", "o012-rbt-l23-exa-002", "simplicial_topology"),
    "O012-TERM-0309": ("quotient Delta-set", "himpunan-Delta hasil bagi", "quotient-delta-set", "o012-rbt-l23-exa-002", "simplicial_topology"),
    "O012-TERM-0310": ("reduced function module", "modul fungsi tereduksi", "reduced-function-module", "o012-rbt-l23-proof-004", "homological_algebra"),
    "O012-TERM-0311": ("reduced cochain", "korantai tereduksi", "reduced-cochain", "o012-rbt-l23-s04", "homological_algebra"),
    "O012-TERM-0312": ("relative simplicial cochain complex", "kompleks korantai simpleksial relatif", "relative-simplicial-cochain-complex", "o012-rbt-l23-exa-002", "homological_algebra"),
    "O012-TERM-0313": ("degreewise", "pada setiap derajat", "degreewise", "o012-rbt-l23-s03", "homological_algebra"),
    "O012-TERM-0314": ("extension by zero", "perluasan dengan nol", "extension-by-zero", "o012-rbt-l23-proof-003", "homological_algebra"),
    "O012-TERM-0315": ("cocycle", "kosiklus", "cocycle", "o012-rbt-l23-proof-002", "homological_algebra"),
}

EXPECTED_ADVERSE = {
    312: ("P1", "Notes.tex:4943-4951", "corrected_in_translation", ["fig-001", "audit-001"], "mathematical_correction"),
    313: ("P1", "Notes.tex:4954-4956", "corrected_in_translation", ["fig-001", "audit-002"], "mathematical_correction"),
    314: ("P2", "Notes.tex:4958-4959", "corrected_in_translation", ["audit-002"], "mathematical_correction"),
    315: ("P1", "Notes.tex:4974-4975", "corrected_in_translation", ["s02", "audit-003"], "mathematical_correction"),
    316: ("P2", "Notes.tex:5002-5006", "clarified_in_translation", ["margin-003", "audit-003"], "clarification"),
    317: ("P1", "Notes.tex:5023-5024", "corrected_in_translation", ["exa-001", "audit-004"], "mathematical_correction"),
    318: ("P2", "Notes.tex:5042-5061", "proof_completed_in_translation", ["proof-003", "audit-004"], "proof_completion"),
    319: ("P1", "Notes.tex:5078-5087,5111", "corrected_in_translation", ["exa-002", "audit-005", "boundary-001"], "mathematical_correction"),
    320: ("P1", "Notes.tex:5089-5109", "proof_completed_in_translation", ["proof-004", "audit-005"], "proof_completion"),
    321: ("P2", "Notes.tex:4944-4947,5045-5048,4952-4953,4974,5002,5033,5036,5078-5079", "accessibility_reflow", ["fig-001", "fig-002", *[f"margin-{n:03d}" for n in range(1, 7)], "audit-006"], "structural_adaptation"),
    322: ("P3", "Notes.tex:4941,4952-4953,4987,5002,5013,5050,5057", "corrected_in_translation", ["audit-007"], "editorial_correction"),
}

BASE_CONCEPTS = (
    "complex", "coboundary", "cohomologically-graded-complex",
    "contravariant-functor", "delta-set", "geometric-realisation",
    "module-over-r", "simplicial-cochain-complex",
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
            raise SystemExit(f"{name}: immutable Units 001-022 prefix mismatch")
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
    if sum(item[0] for item in PREFIX.values()) != PREFIX_RECORDS:
        raise SystemExit("prefix record constant mismatch")
    if sum(item[1] for item in PREFIX.values()) != PREFIX_BYTES:
        raise SystemExit("prefix byte constant mismatch")
    if bundle.hexdigest() != PREFIX_BUNDLE:
        raise SystemExit("Units 001-022 backend bundle identity mismatch")
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
    through_close = ("\n".join(lines[UPSTREAM_START - 1:5121]) + "\n").encode()
    if len(span) != UPSTREAM_SPAN_BYTES or digest(span) != UPSTREAM_SPAN_SHA:
        raise SystemExit("Unit 23 upstream span mismatch")
    if digest(through_close) != UPSTREAM_THROUGH_CLOSE_SHA:
        raise SystemExit("cross-unit source environment witness mismatch")
    if "\\lecturenum{24}" not in lines[5112] or "\\end{example}" not in lines[5120]:
        raise SystemExit("Unit 24 marker/example-close identity mismatch")


def structural_spans(lines: list[str]) -> tuple[list[str], dict[str, tuple[int, int, str]]]:
    opening = re.compile(r"^\s*:::\s+\{[^#}]*#(o012-rbt-l23(?:-[A-Za-z0-9-]+)?)(.*)\}\s*$")
    heading = re.compile(r"^#{1,6}\s+.*\{[^}]*#(o012-rbt-l23(?:-[A-Za-z0-9-]+)?)[^}]*\}\s*$")
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
        "o012-rbt-l23-notice": (12, 62), "o012-rbt-l23": (63, 732),
        "o012-rbt-l23-s01": (65, 202), "o012-rbt-l23-s02": (203, 375),
        "o012-rbt-l23-s03": (376, 578), "o012-rbt-l23-s04": (579, 732),
        "o012-rbt-l23-mastery": (733, 1086),
    }
    for ident, (start, end) in heading_spans.items():
        if ident not in ordered or ident not in lines[start - 1]:
            raise SystemExit(f"heading span identity mismatch: {ident}")
        spans[ident] = (start, end, lines[start - 1])
    if len(ordered) != 51 or len(set(ordered)) != 51 or set(ordered) != set(spans):
        raise SystemExit("Unit 23 stable-ID closure mismatch")
    if digest(("\n".join(ordered) + "\n").encode()) != ANCHOR_ORDER_SHA:
        raise SystemExit("Unit 23 stable-ID order mismatch")
    return ordered, spans


def unit_kind(ident: str, opener: str) -> str:
    if ident.endswith("-notice"): return "notice"
    if ident == "o012-rbt-l23": return "lecture"
    if ident.endswith("-mastery"): return "mastery_section"
    if re.fullmatch(r"o012-rbt-l23-s\d{2}", ident): return "section"
    match = re.search(r"\{\.([A-Za-z][A-Za-z0-9_-]*)", opener)
    kind = match.group(1).replace("source-audit", "source_audit").replace(
        "source-margin", "source_margin") if match else ""
    if kind not in {"example", "source_audit", "source_margin", "lemma",
                    "corollary", "proof", "figure", "remark", "exercise",
                    "hint", "solution", "boundary"}:
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
        text = line.strip().replace("**", "")
        if text and not text.startswith(":::") and not text.startswith(">"):
            return text[:180]
    return f"Unit 23 {kind} {ident.rsplit('-', 1)[-1]}"


def verify_qa() -> tuple[int, str]:
    if not QA_JSON.is_file():
        raise SystemExit("Unit 23 QA receipt absent; append is not authorized")
    raw = QA_JSON.read_bytes()
    qa = json.loads(raw.decode("utf-8"))
    if (qa.get("status") != "PASS"
            or qa.get("source", {}).get("line_start") != UPSTREAM_START
            or qa.get("source", {}).get("line_end") != UPSTREAM_END
            or qa.get("source", {}).get("span_bytes") != UPSTREAM_SPAN_BYTES
            or qa.get("source", {}).get("span_sha256") != UPSTREAM_SPAN_SHA
            or qa.get("unit", {}).get("bytes") != SOURCE_BYTES
            or qa.get("unit", {}).get("lines") != SOURCE_LINES
            or qa.get("unit", {}).get("sha256") != SOURCE_SHA
            or qa.get("unit", {}).get("stable_ids") != 51
            or qa.get("model_provenance") != MODEL):
        raise SystemExit("Unit 23 QA content/binding mismatch")
    checks = qa.get("checks")
    if not isinstance(checks, list) or not checks or any(
            item.get("status") != "PASS" for item in checks if isinstance(item, dict)):
        raise SystemExit("Unit 23 QA contains a non-passing check")
    return len(raw), digest(raw)


def main() -> None:
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
    if len(raw) != SOURCE_BYTES or digest(raw) != SOURCE_SHA or b"\r" in raw:
        raise SystemExit(f"Unit 23 identity mismatch: {len(raw)} {digest(raw)}")
    raw_lines = raw.splitlines(keepends=True)
    lines = [line.decode("utf-8").rstrip("\n") for line in raw_lines]
    if len(lines) != SOURCE_LINES or not raw.endswith(b"\n"):
        raise SystemExit("Unit 23 line/newline mismatch")
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
        raise SystemExit("Unit 23 concept closure mismatch")

    rights_specs = (
        (COMPANION_RIGHTS,
         "Indonesian original mastery, source-audit, proof-completion, and boundary layer for Roberts Unit 23.",
         "Original additions are CC BY 4.0; source-derived material remains separately attributed.",
         [ROOT], None),
        (COMPOSITE_RIGHTS,
         "David Michael Roberts source adaptation plus original Indonesian Unit 23 companions.",
         "Unit 23 source-derived and original layers remain component-distinguishable.",
         [ROOT], None),
        (CUMULATIVE_RIGHTS,
         "Cumulative Roberts Units 001-023 Indonesian reader source boundary.",
         "Source-stage cumulative pointer; the verified Units 001-022 public build remains immutable.",
         [f"unit:o012-rbt-u{number:03d}" for number in range(1, 24)], PRIOR_RIGHTS),
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
        ("o012-rbt-l23-s01", 65, 202), ("o012-rbt-l23-s02", 203, 375),
        ("o012-rbt-l23-s03", 376, 578), ("o012-rbt-l23-s04", 579, 732),
    )
    section_ids = {item[0] for item in section_ranges}

    def parent_local(ident: str, start: int) -> str:
        if ident in {"o012-rbt-l23-notice", "o012-rbt-l23",
                     "o012-rbt-l23-mastery", "o012-rbt-l23-boundary-001"}:
            return ROOT
        if ident in section_ids:
            return LECTURE
        if any(token in ident for token in ("-mcheck-", "-hint-", "-sol-")):
            return MASTERY
        for section, low, high in section_ranges:
            if low <= start <= high:
                return f"unit:{section}"
        raise SystemExit(f"cannot assign Unit 23 parent: {ident}")

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
        "display_title": "Topologi Aljabar - Unit 23: Evaluasi, Gabungan Saling Lepas, dan Perekatan Korantai",
        "edition_id": EDITION, "edition_unit_id": ROOT, "locale": "id-ID",
        "model_provenance": MODEL, "order": 23, "parent_id": COURSE,
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
        shared = {
            "component_source_commit": COMMIT, "component_source_id": RESOURCE,
            "course_route_unit_id": ROUTE, "edition_unit_id": ROOT,
            "model_provenance": MODEL,
        }
        unit = common("unit", unit_id)
        unit.update(shared)
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
        segment = common("segment", f"segment:{ident}")
        segment.update(shared)
        segment.update({
            "concept_ids": concept_ids, "edition_id": EDITION, "locale": "id-ID",
            "order": unit["order"], "provenance_relation": unit["provenance_relation"],
            "resource_id": RESOURCE, "rights_component_id": rights_id,
            "segment_kind": kind, "source_local_id": ident,
            "source_locator": source_locator(original), "target_locator": locator,
            "translation_state": "structurally_verified", "unit_id": unit_id,
        })
        aliases = re.findall(r'data-source-label="([^"]+)"', opener)
        if aliases:
            unit["source_aliases"] = aliases
            segment["source_aliases"] = aliases
        if ident in {"o012-rbt-l23-exa-002", "o012-rbt-l23-boundary-001"}:
            continuation = {
                "continuation_source_line_end": 5121,
                "continuation_source_line_start": 5113,
                "continuation_target_edition_unit_id": "unit:o012-rbt-u024",
                "source_environment_state": "open_at_unit_boundary",
            }
            unit.update(continuation); segment.update(continuation)
        if kind == "proof":
            unit["proof_status"] = "complete_original_proof"
            segment["proof_status"] = "complete_original_proof"
        if kind == "solution":
            unit["solution_status"] = "complete_checked_solution"
            segment["solution_status"] = "complete_checked_solution"
        add("units.jsonl", unit)
        add("segments.jsonl", segment)

    asset = common("asset", "asset:o012-u023-source-markdown")
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
        targets = [f"o012-rbt-l23-{suffix}" for suffix in suffixes]
        if any(target not in spans for target in targets):
            raise SystemExit(f"adverse target absent: {event_id}")
        correction = common("correction", f"correction:o012-u023-adv-{number:04d}")
        correction.update({
            "adverse_ledger_id": event_id,
            "affected_unit_ids": [f"unit:{target}" for target in targets],
            "correction_type": correction_type, "edition_id": EDITION,
            "evidence": source_location,
            "evidence_segment_id": "segment:o012-rbt-l23-notice",
            "severity": severity, "rationale": row["rationale"],
            "resource_id": RESOURCE, "source_defect": row["observed"],
            "target_change": row["action"], "unit_id": ROOT,
            "upstream_report_disposition": "not_contacted",
        })
        add("corrections.jsonl", correction)

    artifact_specs = dict(FIXED_ARTIFACTS)
    artifact_specs["artifact:o012-u023-qa"] = (
        "qa/UNIT_023_QA.json", qa_bytes, qa_sha, "application/json", "built",
        ["qa:o012-u023-source-integrity", "qa:o012-u023-language"])
    for ident, (relative, size, expected_sha, media_type, state, qa_ids) in artifact_specs.items():
        artifact_raw = (LANE / relative).read_bytes()
        if len(artifact_raw) != size or digest(artifact_raw) != expected_sha:
            raise SystemExit(f"evidence identity mismatch: {relative}")
        artifact = common("artifact", ident)
        artifact.update({
            "bytes": size, "locale": "id-ID", "manifest_artifact_id": None,
            "media_type": media_type, "path": relative, "qa_event_ids": qa_ids,
            "rights_component_id": COMPOSITE_RIGHTS, "sha256": expected_sha,
            "toolchain": (f"Bounded Unit 23 evidence; Notes.tex:4939-5112 span "
                          f"{UPSTREAM_SPAN_SHA}; {MODEL}; route {ROUTE}; "
                          "no cumulative-build/publication assertion."),
            "translation_state": state, "unit_id": ROOT,
        })
        add("artifacts.jsonl", artifact)

    qa_specs = (
        ("qa:o012-u023-source-integrity", "source",
         "Unit 23 reader/source identities, 51 stable IDs, source census, controls, and Pandoc structure passed.",
         ["artifact:o012-u023-source-audit", "artifact:o012-u023-qa"]),
        ("qa:o012-u023-math", "math",
         "Independent Unit 23 mathematical review passed with no open P1, P2, or P3 finding.",
         ["artifact:o012-u023-independent-review"]),
        ("qa:o012-u023-language", "language",
         "Independent Indonesian language, terminology, attribution, accessibility, and continuation review passed.",
         ["artifact:o012-u023-independent-review", "artifact:o012-u023-qa"]),
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

    relation("relation:adapts:o012-rbt-u023:edition", ROOT, "adapts", EDITION,
             "Unit 23 is the Indonesian adapted reader boundary for the frozen Roberts edition.")
    relation("relation:precedes:o012-rbt-u022:o012-rbt-u023",
             "unit:o012-rbt-u022", "precedes", ROOT,
             "Preserves contiguous Roberts lecture-unit order.")
    relation("relation:precedes:o012-rbt-l23:mastery", LECTURE, "precedes", MASTERY,
             "Lecture content precedes the Unit 23 mastery companion.")
    relation("relation:boundary:o012-u023", CUMULATIVE_RIGHTS, "contains", ROOT,
             "Additive cumulative Units 001-023 source boundary; prior verified public build retained.")
    relation("relation:route:d60-r13:o012-rbt-u023", COURSE, "contains", ROOT,
             "Roberts Lecture 23 is an edition unit in the non-destructive D60-R13 learner-route view.",
             course_route_unit_id=ROUTE, edition_unit_id=ROOT)
    relation("relation:xref:o012-rbt-l23-exa-002:u024-continuation",
             "unit:o012-rbt-l23-exa-002", "xref", EDITION,
             "The source example remains open across the Lecture 24 marker and resumes at Notes.tex:5113 before closing at 5121.",
             continuation_source_line_end=5121, continuation_source_line_start=5113,
             continuation_target_edition_unit_id="unit:o012-rbt-u024",
             source_environment_state="open_at_unit_boundary")
    proof_targets = {
        1: "unit:o012-rbt-l23-lem-001", 2: "unit:o012-rbt-l23-cor-001",
        3: "unit:o012-rbt-l23-s03", 4: "unit:o012-rbt-l23-exa-002",
    }
    for number, target in proof_targets.items():
        relation(f"relation:proves:o012-rbt-l23-proof-{number:03d}:closure",
                 f"unit:o012-rbt-l23-proof-{number:03d}", "proves", target,
                 f"Edition-original complete proof closure {number} for Unit 23.")
    for number in range(1, 7):
        relation(f"relation:solves:l23-sol-{number:03d}:l23-mcheck-{number:03d}",
                 f"unit:o012-rbt-l23-sol-{number:03d}", "solves",
                 f"unit:o012-rbt-l23-mcheck-{number:03d}",
                 f"Complete checked solution for Unit 23 mastery check {number}.")
        relation(f"relation:hints:l23-hint-{number:03d}:l23-mcheck-{number:03d}",
                 f"unit:o012-rbt-l23-hint-{number:03d}", "hints",
                 f"unit:o012-rbt-l23-mcheck-{number:03d}",
                 f"Bounded hint for Unit 23 mastery check {number}.")

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
            raise SystemExit(f"noncanonical Unit 23 path: {ident}")
        if unit["parent_id"].startswith("unit:"):
            parent = by_id[unit["parent_id"]]
            if unit["path"][:-1] != parent["path"]:
                raise SystemExit(f"Unit 23 parent path mismatch: {ident}")
        for obj in (unit, segment):
            if (obj["edition_unit_id"] != ROOT or obj["course_route_unit_id"] != ROUTE
                    or obj["model_provenance"] != MODEL):
                raise SystemExit(f"Unit 23 route/provenance mismatch: {ident}")
    sibling_orders: defaultdict[str, list[int]] = defaultdict(list)
    for obj in additions["units.jsonl"].values():
        sibling_orders[obj["parent_id"]].append(obj["order"])
    if any(len(values) != len(set(values)) for values in sibling_orders.values()):
        raise SystemExit("duplicate Unit 23 sibling order")
    for number in range(1, 7):
        check = f"unit:o012-rbt-l23-mcheck-{number:03d}"
        solves = [obj for obj in additions["relations.jsonl"].values()
                  if obj["relation_type"] == "solves" and obj["to_id"] == check]
        hints = [obj for obj in additions["relations.jsonl"].values()
                 if obj["relation_type"] == "hints" and obj["to_id"] == check]
        if len(solves) != 1 or len(hints) != 1:
            raise SystemExit(f"mastery closure mismatch: {number}")
    proof_units = [obj for obj in additions["units.jsonl"].values()
                   if obj.get("proof_status") == "complete_original_proof"]
    if len(proof_units) != 4:
        raise SystemExit("Unit 23 four-proof closure mismatch")
    correction_ids = {obj.get("adverse_ledger_id")
                      for obj in additions["corrections.jsonl"].values()}
    if correction_ids != {f"O012-ADV-{number:04d}" for number in range(312, 323)}:
        raise SystemExit("Unit 23 adverse closure mismatch")
    if additions["rights.jsonl"][CUMULATIVE_RIGHTS]["component_scope"] != [
            f"unit:o012-rbt-u{number:03d}" for number in range(1, 24)]:
        raise SystemExit("Unit 23 cumulative rights scope mismatch")
    exa = by_id["unit:o012-rbt-l23-exa-002"]
    if (exa.get("source_environment_state") != "open_at_unit_boundary"
            or exa.get("continuation_target_edition_unit_id") != "unit:o012-rbt-u024"):
        raise SystemExit("Unit 23/24 continuation closure mismatch")

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
    print("Unit 023 backend extension: PASS")
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


if __name__ == "__main__":
    main()
