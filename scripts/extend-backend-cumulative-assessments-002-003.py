#!/usr/bin/env python3
"""Fail-closed append-only admission for D60 cumulative assessments 2 and 3.

The verified Roberts/Fomberg/CA01/ordinary-hint backend is an immutable binary
prefix.  This producer reads two original assessment readers and their four
independent reviews, uses the combined QA receipt as the input seal, derives a
canonical suffix, validates the merged graph in memory, rechecks all seven
inputs, and only then performs binary append writes.  There is deliberately no
replacement, repair, or partial-assessment mode.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any


LANE = Path(__file__).resolve().parents[1]
BACKEND = LANE / "backend"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"
SCHEMA = "curriculum.interop"
SCHEMA_VERSION = "0.1.0"
WORKFLOW = "o012-d60-id-reader-production"
TIMESTAMP = "2026-08-27T00:00:00Z"
COURSE = "course:o012-d60"
PROGRAM = "program:o012-id"
ROBERTS_EDITION = "edition:roberts-at-2019-b947ad2"
ROBERTS_RESOURCE = "resource:roberts-algebraic-topology-2019"
FOMBERG_EDITION = "edition:fomberg-at-2025-563194f"
FOMBERG_RESOURCE = "resource:fomberg-algebraic-topology-2025"
INTEGRATED_RIGHTS = "rights:o012-d60-integrated-route-cc-by-sa-4.0"
COMBINED_QA_PATH = "qa/CUMULATIVE_ASSESSMENTS_002_003_QA.json"
BASELINE_RECEIPT_PATH = "qa/BACKEND_APPEND_ONLY_ORDINARY_HINTS_R01_R06_CUMULATIVE_RECEIPT.json"
BASELINE_RECEIPT_IDENTITY = (
    10252,
    284,
    "10e9d32848b950148983d0d8c38d6753a9956a674f657858b31dd257af5b2aa8",
)

FILES = (
    "artifacts.jsonl", "assets.jsonl", "authority.jsonl", "concepts.jsonl",
    "corrections.jsonl", "qa.jsonl", "relations.jsonl", "rights.jsonl",
    "segments.jsonl", "terms.jsonl", "units.jsonl",
)

# Exact public ordinary-hint boundary: 7,012 records, 8,545,732 bytes.
PREFIX = {
    "artifacts.jsonl": (197, 161333, "64d050e7abb6c61e27f4bd8659c3c5ab7899be43032592cb5e3b0c15cbeb18f6"),
    "assets.jsonl": (87, 64692, "1df40f8f6ca4f2fbfbe8a7b924a68a153713a20a4eebe1d014d8fb04669945f7"),
    "authority.jsonl": (6, 4374, "84c622f56dbbd5ba379361245ecfe07bc79c9f4fd6b18ba21b82b5f545211869"),
    "concepts.jsonl": (483, 152695, "720d96a10a3c2abebab164e2181486743ef99efb50c6ef419faefbf528b8ead3"),
    "corrections.jsonl": (564, 594720, "bd961fad5d83e96fec6ef83caa8447e2e5f282c603fd4983d79b5b4b54049fbb"),
    "qa.jsonl": (170, 93377, "05c2660f74b7ba462cbad260a5067f41c8ec0d451b4bd6229f53a95de4f9c70a"),
    "relations.jsonl": (912, 399529, "37b0ef08c48f34f7a7b9abef523ab548bcefb3a16ba5dba99b6ccec4f58cee6f"),
    "rights.jsonl": (105, 96960, "3788fae643c94198e10b49465ad313c166abaf08bc42da71553051922054de49"),
    "segments.jsonl": (1991, 3247261, "25c31b936b1c53ae39337d1059ec5889782e21da698521041194c6bb37058a79"),
    "terms.jsonl": (476, 315218, "4b82f9d582ba747829373a7935fcc3cae56b96fd6b7486969ebb6d54cf927c50"),
    "units.jsonl": (2021, 3415573, "08c9f3e5886e9a3cd6b12737d8ffff238caf4b24116d08da4f85f12e7049e86f"),
}
PREFIX_TOTAL = (7012, 8545732, "7d723f9ef163303c7dde63d646dc8d5917c2450b1da5d24c87ef77bf4e4d664b")

ROUTE_ANCHORS = {
    "D60-R03": "unit:o012-rbt-u005",
    "D60-R05": "unit:o012-rbt-u011",
    "D60-R08": "unit:o012-fom-u001",
    "D60-R09": "unit:o012-fom-u002",
    "D60-R10": "unit:o012-fom-u003",
    "D60-R11": "unit:o012-fom-u004",
    "D60-R12": "unit:o012-fom-u005",
    "D60-R13": "unit:o012-rbt-u020",
    "D60-R14": "unit:o012-rbt-u028",
}


@dataclass(frozen=True)
class AssessmentSpec:
    number: int
    code: str
    assessment_id: str
    edition_unit_id: str
    reader_path: str
    math_path: str
    language_path: str
    expected_routes: tuple[str, ...]
    order: int
    primary_edition: str
    primary_resource: str
    dependencies: dict[int, tuple[str, ...]]
    default_concepts: dict[int, tuple[str, ...]]

    @property
    def local_root(self) -> str:
        return f"o012-d60-{self.code}"

    @property
    def root(self) -> str:
        return f"unit:{self.local_root}"

    @property
    def rights(self) -> str:
        return f"rights:{self.local_root}-original-cc-by-sa-4.0"


SPECS = (
    AssessmentSpec(
        number=2,
        code="ca02",
        assessment_id="D60-CA02",
        edition_unit_id="O012-ORIG-CA02",
        reader_path="source/id-ID/mastery/cumulative-assessment-002-homology-excision-cellular.md",
        math_path="qa/cumulative-assessment-002/INDEPENDENT_MATH_REVIEW.json",
        language_path="qa/cumulative-assessment-002/INDEPENDENT_SOURCE_LANGUAGE_REVIEW.json",
        expected_routes=("D60-R08", "D60-R09", "D60-R10", "D60-R11", "D60-R12"),
        order=40,
        primary_edition=FOMBERG_EDITION,
        primary_resource=FOMBERG_RESOURCE,
        dependencies={
            1: ("unit:o012-fom-u001",),
            2: ("unit:o012-fom-u002", "unit:o012-fom-u002-thm-homotopy-invariance"),
            3: ("unit:o012-fom-u003", "unit:o012-fom-u003-thm-long-exact"),
            4: ("unit:o012-fom-u004", "unit:o012-fom-u004-thm-mayer-vietoris"),
            5: ("unit:o012-fom-u003-thm-les-quotient", "unit:o012-fom-u004-thm-relative-quotient"),
            6: ("unit:o012-fom-u006",),
            7: ("unit:o012-fom-u007-thm-cellular-homology", "unit:o012-fom-u007-thm-cellular-incidence"),
            8: (
                "unit:o012-fom-u005-prop-local-to-global", "unit:o012-fom-u001",
                "unit:o012-fom-u002", "unit:o012-fom-u004",
            ),
        },
        default_concepts={
            1: ("concept:delta-complex", "concept:orientation", "concept:boundary-map", "concept:simplicial-homology"),
            2: ("concept:chain-map", "concept:induced-map", "concept:chain-homotopy", "concept:singular-homology"),
            3: ("concept:relative-homology", "concept:long-exact-sequence", "concept:connecting-map"),
            4: ("concept:excision", "concept:mayer-vietoris-long-exact-sequence", "concept:reduced-homology", "concept:naturality"),
            5: ("concept:relative-homology", "concept:relative-homology-quotient-theorem", "concept:good-pair"),
            6: ("concept:cw-complex", "concept:attaching-map", "concept:characteristic-map", "concept:weak-topology"),
            7: ("concept:cw-complex", "concept:homology", "concept:orientation", "concept:boundary-map"),
            8: ("concept:degree-of-a-map", "concept:local-degree", "concept:homology", "concept:naturality"),
        },
    ),
    AssessmentSpec(
        number=3,
        code="ca03",
        assessment_id="D60-CA03",
        edition_unit_id="O012-ORIG-CA03",
        reader_path="source/id-ID/mastery/cumulative-assessment-003-cohomology-degree-synthesis.md",
        math_path="qa/cumulative-assessment-003/INDEPENDENT_MATH_REVIEW.json",
        language_path="qa/cumulative-assessment-003/INDEPENDENT_SOURCE_LANGUAGE_REVIEW.json",
        expected_routes=("D60-R13", "D60-R14"),
        order=41,
        primary_edition=ROBERTS_EDITION,
        primary_resource=ROBERTS_RESOURCE,
        dependencies={
            1: ("unit:o012-rbt-u020", "unit:o012-rbt-u022"),
            2: ("unit:o012-rbt-l23-lem-001",),
            3: ("unit:o012-rbt-l24-lem-002", "unit:o012-rbt-l24-proof-003"),
            4: ("unit:o012-rbt-l25-prop-001", "unit:o012-rbt-l26-prop-002"),
            5: ("unit:o012-rbt-l27-thm-001",),
            6: ("unit:o012-rbt-l29-lem-001", "unit:o012-rbt-l28-thm-001"),
            7: ("unit:o012-rbt-l30-prop-001", "unit:o012-rbt-l30-cor-001", "unit:o012-rbt-l30-thm-003"),
            8: ("unit:o012-rbt-u029", "unit:o012-rbt-u020", "unit:o012-rbt-u011", "unit:o012-fom-u007"),
        },
        default_concepts={
            1: ("concept:cohomologically-graded-complex", "concept:coboundary", "concept:cohomological-euler-characteristic"),
            2: ("concept:coproduct-preservation", "concept:product-of-modules", "concept:contravariant-functor"),
            3: ("concept:snake-lemma", "concept:connecting-map", "concept:diagram-chase"),
            4: ("concept:relative-cohomology", "concept:reduced-cohomology", "concept:long-exact-sequence"),
            5: ("concept:mayer-vietoris-long-exact-sequence", "concept:small-singular-cochain-complex", "concept:sphere-cohomology"),
            6: ("concept:singular-simplicial-cochain-comparison", "concept:naturality", "concept:five-lemma", "concept:k-skeleton"),
            7: ("concept:degree-of-a-map", "concept:antipodal-map", "concept:hairy-sphere-theorem"),
            8: ("concept:fundamental-group", "concept:homology", "concept:singular-cohomology", "concept:euler-characteristic"),
        },
    ),
)

INPUT_PATHS = tuple(
    path
    for spec in SPECS
    for path in (spec.reader_path, spec.math_path, spec.language_path)
) + (COMBINED_QA_PATH,)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"CA02+CA03 backend producer FAIL: {message}")


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canon(record: dict[str, Any]) -> bytes:
    return (json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def common(entity_type: str, ident: str) -> dict[str, Any]:
    return {
        "entity_type": entity_type,
        "id": ident,
        "schema": SCHEMA,
        "schema_version": SCHEMA_VERSION,
        "status": "active",
        "supersedes": None,
        "timestamp": TIMESTAMP,
        "workflow": WORKFLOW,
    }


def load_generic():
    path = LANE / "scripts/validate-backend.py"
    spec = importlib.util.spec_from_file_location("o012_generic_backend_for_ca02_ca03", path)
    require(spec is not None and spec.loader is not None, "cannot load generic backend validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def identity(raw: bytes) -> tuple[int, int, str]:
    return len(raw), raw.count(b"\n"), digest(raw)


def read_disciplined(relative: str) -> bytes:
    path = LANE / relative
    require(path.is_file(), f"required input is missing: {relative}")
    raw = path.read_bytes()
    require(raw and b"\r" not in raw and raw.endswith(b"\n"), f"input is not nonempty UTF-8/LF: {relative}")
    try:
        raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise SystemExit(f"CA02+CA03 backend producer FAIL: invalid UTF-8 in {relative}: {exc}")
    return raw


def normalized_relative(value: str) -> str:
    return value.replace("\\", "/").removeprefix("./")


def collect_identity_objects(node: Any, out: dict[str, tuple[int, int, str]]) -> None:
    if isinstance(node, dict):
        path = node.get("path")
        byte_count = node.get("bytes")
        sha = node.get("sha256")
        lines = node.get("lf_lines", node.get("lf_count", node.get("lines")))
        if isinstance(path, str) and isinstance(byte_count, int) and isinstance(lines, int) and isinstance(sha, str):
            key = normalized_relative(path)
            value = (byte_count, lines, sha.lower())
            require(key not in out or out[key] == value, f"combined QA has conflicting identities for {key}")
            out[key] = value
        for value in node.values():
            collect_identity_objects(value, out)
    elif isinstance(node, list):
        for value in node:
            collect_identity_objects(value, out)


def verify_review(spec: AssessmentSpec, kind: str, receipt: dict[str, Any], reader_sha: str) -> None:
    expected_kind = "independent_mathematics" if kind == "math" else "independent_source_language"
    require(receipt.get("review_kind") == expected_kind, f"{spec.assessment_id} {kind} review kind mismatch")
    require(str(receipt.get("status", "")).startswith("PASS"), f"{spec.assessment_id} {kind} review did not pass")
    require(receipt.get("independent_from_production") is True, f"{spec.assessment_id} {kind} review is not independent")
    require(receipt.get("reader_sha256") == reader_sha, f"{spec.assessment_id} {kind} review binds stale reader")
    assessment_marker = str(receipt.get("assessment_id", "")) + " " + str(receipt.get("review_id", ""))
    require(spec.assessment_id in assessment_marker, f"{spec.assessment_id} absent from {kind} review identity")
    severity = receipt.get("severity_census", {})
    require((severity.get("P1"), severity.get("P2"), severity.get("P3")) == (0, 0, 0), f"{spec.assessment_id} {kind} findings remain")
    item_results = receipt.get("item_results")
    if item_results is not None:
        require(isinstance(item_results, list) and len(item_results) == 8, f"{spec.assessment_id} {kind} item-result census mismatch")
        require(all(str(item.get("result", "")).startswith("PASS") for item in item_results), f"{spec.assessment_id} {kind} has a failing item")


def verify_inputs(sealed: dict[str, tuple[int, int, str]] | None = None) -> dict[str, Any]:
    raw = {relative: read_disciplined(relative) for relative in INPUT_PATHS}
    identities = {relative: identity(value) for relative, value in raw.items()}
    if sealed is not None:
        require(identities == sealed, f"sealed seven-file identity drift: {identities!r}")

    combined = json.loads(raw[COMBINED_QA_PATH].decode("utf-8"))
    require(str(combined.get("status", "")).startswith("PASS"), "combined CA02+CA03 QA did not pass")
    serialized_combined = json.dumps(combined, ensure_ascii=False, sort_keys=True)
    require(all(spec.assessment_id in serialized_combined for spec in SPECS), "combined QA does not identify both assessments")
    bound: dict[str, tuple[int, int, str]] = {}
    collect_identity_objects(combined, bound)
    for spec in SPECS:
        for relative in (spec.reader_path, spec.math_path, spec.language_path):
            require(relative in bound, f"combined QA does not bind {relative}")
            require(bound[relative] == identities[relative], f"combined QA identity mismatch: {relative}")

    reviews: dict[str, dict[str, dict[str, Any]]] = {}
    for spec in SPECS:
        reader_sha = identities[spec.reader_path][2]
        math = json.loads(raw[spec.math_path].decode("utf-8"))
        language = json.loads(raw[spec.language_path].decode("utf-8"))
        verify_review(spec, "math", math, reader_sha)
        verify_review(spec, "language", language, reader_sha)
        reviews[spec.code] = {"math": math, "language": language}
    return {"raw": raw, "identities": identities, "combined_qa": combined, "reviews": reviews}


def parse_scalar(frontmatter: str, key: str) -> str:
    match = re.search(rf"(?m)^{re.escape(key)}:\s*(.+?)\s*$", frontmatter)
    require(match is not None, f"frontmatter field missing: {key}")
    value = match.group(1).strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        value = value[1:-1]
    return value


def parse_frontmatter_routes(frontmatter: str) -> tuple[str, ...]:
    lines = frontmatter.splitlines()
    starts = [i for i, line in enumerate(lines) if line.strip() == "course_route_unit_ids:"]
    require(len(starts) == 1, "frontmatter course_route_unit_ids block missing or duplicated")
    routes: list[str] = []
    for line in lines[starts[0] + 1:]:
        match = re.match(r"^\s+-\s+(D60-R\d{2})\s*$", line)
        if match:
            routes.append(match.group(1))
            continue
        if line.strip():
            break
    require(routes and len(routes) == len(set(routes)), "frontmatter route list is empty or duplicated")
    return tuple(routes)


def parse_attrs(line: str) -> dict[str, str]:
    return {key: value for key, value in re.findall(r'\b(data-[a-z0-9-]+)="([^"]*)"', line)}


def parse_list_attr(value: str | None) -> tuple[str, ...]:
    if not value:
        return ()
    return tuple(part for part in re.split(r"[\s,]+", value.strip()) if part)


def source_locator(spec: AssessmentSpec) -> dict[str, Any]:
    return {
        "kind": "edition_original",
        "path": spec.reader_path,
        "precision": "exact_target_span",
        "source_corpus_used": False,
    }


def target_locator(spec: AssessmentSpec, reader_sha: str, lines: list[bytes], span: tuple[int, int]) -> dict[str, Any]:
    start, end = span
    return {
        "content_sha256": digest(b"".join(lines[start - 1:end])),
        "file_sha256": reader_sha,
        "line_end": end,
        "line_start": start,
        "path": spec.reader_path,
    }


def parse_reader(spec: AssessmentSpec, raw: bytes) -> dict[str, Any]:
    text = raw.decode("utf-8")
    lines = raw.splitlines(keepends=True)
    decoded = [line.decode("utf-8") for line in lines]
    require(text.startswith("---\n"), f"{spec.assessment_id} frontmatter does not start at byte zero")
    close = text.find("\n---\n", 4)
    require(close > 4, f"{spec.assessment_id} frontmatter is not closed")
    frontmatter = text[4:close]
    require(parse_scalar(frontmatter, "lang") == "id-ID", f"{spec.assessment_id} locale mismatch")
    require(parse_scalar(frontmatter, "course_id") == "D60", f"{spec.assessment_id} course mismatch")
    require(parse_scalar(frontmatter, "assessment_id") == spec.assessment_id, f"{spec.assessment_id} frontmatter assessment mismatch")
    require(parse_scalar(frontmatter, "edition_unit_id") == spec.edition_unit_id, f"{spec.assessment_id} edition-unit mismatch")
    require(parse_frontmatter_routes(frontmatter) == spec.expected_routes, f"{spec.assessment_id} frontmatter route boundary mismatch")
    require(parse_scalar(frontmatter, "rights") == "CC BY-SA 4.0", f"{spec.assessment_id} rights mismatch")
    require("materi edisi asli" in parse_scalar(frontmatter, "origin").lower(), f"{spec.assessment_id} original-layer notice missing")
    require(parse_scalar(frontmatter, "provenance").startswith(MODEL), f"{spec.assessment_id} model provenance mismatch")
    require(MODEL in text, f"{spec.assessment_id} model provenance absent")
    require(re.search(r"bank (masalah|soal) Fomberg", text, re.IGNORECASE) is not None, f"{spec.assessment_id} excluded-bank notice missing")

    root_pattern = re.compile(rf"^# .+ \{{#{re.escape(spec.local_root)}\}}\s*$")
    root_starts = [i for i, line in enumerate(decoded, 1) if root_pattern.match(line.rstrip("\n"))]
    require(len(root_starts) == 1, f"{spec.assessment_id} root heading missing or duplicated")
    section_titles: dict[int, str] = {}
    section_ids: set[str] = set()
    for line in decoded:
        match = re.match(rf"^## Soal ([1-8])\s+[—-]\s+(.+?) \{{#({re.escape(spec.local_root)}-s(0[1-8]))\}}\s*$", line.rstrip("\n"))
        if match:
            number = int(match.group(1))
            require(int(match.group(4)) == number, f"{spec.assessment_id} section-number/ID mismatch")
            require(number not in section_titles, f"{spec.assessment_id} duplicate problem heading {number}")
            section_titles[number] = match.group(2).strip()
            section_ids.add(match.group(3))
    require(set(section_titles) == set(range(1, 9)), f"{spec.assessment_id} problem-heading census mismatch")
    coverage_id = f"{spec.local_root}-coverage"
    require(sum(coverage_id in line and line.lstrip().startswith("##") for line in decoded) == 1, f"{spec.assessment_id} coverage heading missing or duplicated")

    blocks: dict[int, dict[str, dict[str, Any]]] = {number: {} for number in range(1, 9)}
    opening_ids: set[str] = set()
    fence = re.compile(r"^::: \{\.(exercise|hint|solution)\s+#([^\s}]+)(.*?)\}\s*$")
    for index, line in enumerate(decoded, 1):
        match = fence.match(line.rstrip("\n"))
        if not match:
            continue
        kind, local_id = match.group(1), match.group(2)
        token = {"exercise": "ex", "hint": "hint", "solution": "sol"}[kind]
        id_match = re.fullmatch(rf"{re.escape(spec.local_root)}-{token}-(00[1-8])", local_id)
        require(id_match is not None, f"{spec.assessment_id} malformed {kind} ID: {local_id}")
        number = int(id_match.group(1))
        require(kind not in blocks[number], f"{spec.assessment_id} duplicate {kind} for item {number}")
        ends = [end for end in range(index + 1, len(decoded) + 1) if decoded[end - 1].strip() == ":::"]
        require(ends, f"{spec.assessment_id} unclosed {kind} item {number}")
        attrs = parse_attrs(line)
        require(attrs.get("data-origin") == "edition-original", f"{spec.assessment_id} item {number} {kind} origin mismatch")
        require(attrs.get("data-assessment-id") == spec.assessment_id, f"{spec.assessment_id} item {number} {kind} assessment mismatch")
        if "data-edition-unit-id" in attrs:
            require(attrs["data-edition-unit-id"] == spec.edition_unit_id, f"{spec.assessment_id} item {number} {kind} edition mismatch")
        primary = attrs.get("data-course-route-unit-id")
        require(primary in ROUTE_ANCHORS, f"{spec.assessment_id} item {number} {kind} primary route invalid")
        secondary = parse_list_attr(attrs.get("data-secondary-route-unit-ids"))
        require(len(secondary) == len(set(secondary)) and primary not in secondary, f"{spec.assessment_id} item {number} {kind} secondary routes invalid")
        require(all(route in ROUTE_ANCHORS for route in secondary), f"{spec.assessment_id} item {number} {kind} secondary route unknown")
        concepts = parse_list_attr(attrs.get("data-concept-ids", attrs.get("data-concept-id")))
        require(all(value.startswith("concept:") for value in concepts), f"{spec.assessment_id} item {number} {kind} concept ID malformed")
        blocks[number][kind] = {
            "attrs": attrs,
            "concepts": concepts,
            "local_id": local_id,
            "primary": primary,
            "secondary": secondary,
            "span": (index, ends[0]),
        }
        require(local_id not in opening_ids, f"{spec.assessment_id} duplicate stable ID: {local_id}")
        opening_ids.add(local_id)

    for number in range(1, 9):
        require(set(blocks[number]) == {"exercise", "hint", "solution"}, f"{spec.assessment_id} item {number} triple incomplete")
        exercise = blocks[number]["exercise"]
        for kind in ("hint", "solution"):
            member = blocks[number][kind]
            require(member["primary"] == exercise["primary"], f"{spec.assessment_id} item {number} primary route differs within triple")
            require(member["secondary"] == exercise["secondary"], f"{spec.assessment_id} item {number} secondary routes differ within triple")
        explicit_concepts = {member["concepts"] for member in blocks[number].values() if member["concepts"]}
        require(len(explicit_concepts) <= 1, f"{spec.assessment_id} item {number} concept IDs differ within triple")
        concepts = next(iter(explicit_concepts), spec.default_concepts[number])
        require(concepts, f"{spec.assessment_id} item {number} has no concept mapping")
        for member in blocks[number].values():
            member["secondary"] = exercise["secondary"]
            member["concepts"] = concepts

    expected_ids = {spec.local_root, coverage_id, *section_ids, *opening_ids}
    require(len(expected_ids) == 34, f"{spec.assessment_id} stable-ID inventory is not exactly 34")
    return {
        "blocks": blocks,
        "concepts": sorted({concept for number in blocks.values() for member in number.values() for concept in member["concepts"]}),
        "frontmatter_title": parse_scalar(frontmatter, "title"),
        "reader_sha256": digest(raw),
        "root_span": (root_starts[0], len(lines)),
        "section_titles": section_titles,
    }


def parse_prefix_records(raw_by_file: dict[str, bytes]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for name in FILES:
        raw = raw_by_file[name]
        require(b"\r" not in raw and raw.endswith(b"\n"), f"prefix JSONL discipline mismatch: {name}")
        for line_number, line in enumerate(raw.splitlines(keepends=True), 1):
            try:
                record = json.loads(line.decode("utf-8", errors="strict"))
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                raise SystemExit(f"CA02+CA03 backend producer FAIL: {name}:{line_number}: {exc}")
            require(isinstance(record, dict) and canon(record) == line, f"noncanonical prefix record: {name}:{line_number}")
            records.append(record)
    return records


def verify_prefix(backend: Path = BACKEND) -> tuple[dict[str, bytes], list[dict[str, Any]]]:
    raw_by_file: dict[str, bytes] = {}
    bundle = hashlib.sha256()
    total_records = total_bytes = 0
    for name in FILES:
        path = backend / name
        require(path.is_file(), f"backend file missing: {name}")
        raw = path.read_bytes()
        observed = (len(raw.splitlines()), len(raw), digest(raw))
        require(observed == PREFIX[name], f"immutable 7,012-record prefix mismatch: {name}: {observed!r}")
        raw_by_file[name] = raw
        bundle.update(name.encode("utf-8")); bundle.update(b"\0"); bundle.update(raw)
        total_records += observed[0]; total_bytes += observed[1]
    require((total_records, total_bytes, bundle.hexdigest()) == PREFIX_TOTAL, "immutable prefix bundle mismatch")
    return raw_by_file, parse_prefix_records(raw_by_file)


def route_fields(block: dict[str, Any]) -> dict[str, Any]:
    primary = block["primary"]
    secondary = list(block["secondary"])
    return {
        "course_route_unit_id": primary,
        "course_route_unit_ids": [primary, *secondary],
        "primary_course_route_unit_id": primary,
        "secondary_course_route_unit_ids": secondary,
        "route_mapping_status": "explicit_primary_and_secondary",
    }


def authority_context() -> list[str]:
    return [COURSE, PROGRAM, ROBERTS_EDITION, ROBERTS_RESOURCE, FOMBERG_EDITION, FOMBERG_RESOURCE]


def unit_record(
    spec: AssessmentSpec,
    parsed: dict[str, Any],
    reader_lines: list[bytes],
    local_id: str,
    kind: str,
    title: str,
    order: int,
    span: tuple[int, int],
    concepts: list[str] | tuple[str, ...],
    number: int | None,
    block: dict[str, Any] | None,
) -> dict[str, Any]:
    ident = f"unit:{local_id}"
    record = {
        **common("unit", ident),
        "assessment_id": spec.assessment_id,
        "authority_context_ids": authority_context(),
        "authority_context_only": True,
        "concept_ids": list(concepts),
        "course_id": COURSE,
        "display_title": title,
        "edition_context_only": True,
        "edition_id": spec.primary_edition,
        "edition_unit_id": spec.edition_unit_id,
        "locale": "id-ID",
        "model_provenance": MODEL,
        "order": order,
        "original_layer": True,
        "parent_id": COURSE if kind == "reader_unit" else spec.root,
        "path": [spec.root] if kind == "reader_unit" else [spec.root, ident],
        "program_id": PROGRAM,
        "provenance_relation": "edition_original",
        "resource_context_only": True,
        "resource_id": spec.primary_resource,
        "rights_component_id": spec.rights,
        "source_corpus_used": False,
        "source_local_id": local_id,
        "source_locator": source_locator(spec),
        "target_locator": target_locator(spec, parsed["reader_sha256"], reader_lines, span),
        "translation_state": "structurally_verified",
        "unit_kind": kind,
    }
    if kind == "reader_unit":
        record.update({
            "assessment_kind": "cumulative_assessment",
            "course_route_unit_ids": list(spec.expected_routes),
            "reader_scope": "eight_exercises_eight_hints_eight_complete_checked_solutions",
        })
    else:
        require(number is not None and block is not None, "child record lacks assessment item metadata")
        record.update(route_fields(block))
        record["assessment_item_number"] = number
        if kind == "solution":
            record["solution_status"] = "complete_checked_solution"
    return record


def segment_from_unit(unit: dict[str, Any], rights: str) -> dict[str, Any]:
    kind_map = {"reader_unit": "assessment", "exercise": "exercise", "hint": "hint", "solution": "solution"}
    optional = {
        key: unit[key]
        for key in (
            "assessment_id", "assessment_item_number", "authority_context_ids", "authority_context_only",
            "course_route_unit_id", "course_route_unit_ids", "edition_context_only", "edition_unit_id",
            "model_provenance", "original_layer", "primary_course_route_unit_id", "resource_context_only",
            "route_mapping_status", "secondary_course_route_unit_ids", "solution_status", "source_corpus_used",
        )
        if key in unit
    }
    return {
        **common("segment", unit["id"].replace("unit:", "segment:", 1)),
        **optional,
        "concept_ids": unit["concept_ids"],
        "edition_id": unit["edition_id"],
        "locale": "id-ID",
        "order": unit["order"],
        "provenance_relation": "edition_original",
        "resource_id": unit["resource_id"],
        "rights_component_id": rights,
        "segment_kind": kind_map[unit["unit_kind"]],
        "source_local_id": unit["source_local_id"],
        "source_locator": unit["source_locator"],
        "target_locator": unit["target_locator"],
        "translation_state": "structurally_verified",
        "unit_id": unit["id"],
    }


def relation(ident: str, relation_type: str, from_id: str, to_id: str, note: str, **extra: Any) -> dict[str, Any]:
    return {**common("relation", ident), "from_id": from_id, "note": note, "relation_type": relation_type, "to_id": to_id, **extra}


def artifact(
    spec: AssessmentSpec,
    identities: dict[str, tuple[int, int, str]],
    ident: str,
    relative: str,
    media_type: str,
    qa_ids: list[str],
    state: str,
) -> dict[str, Any]:
    byte_count, _, sha = identities[relative]
    reader_sha = identities[spec.reader_path][2]
    return {
        **common("artifact", ident),
        "assessment_id": spec.assessment_id,
        "bytes": byte_count,
        "edition_unit_id": spec.edition_unit_id,
        "locale": "id-ID",
        "manifest_artifact_id": None,
        "media_type": media_type,
        "path": relative,
        "qa_event_ids": qa_ids,
        "rights_component_id": spec.rights,
        "sha256": sha,
        "toolchain": f"Original {spec.assessment_id} evidence; {MODEL}; reader {reader_sha}; semantic admission only.",
        "translation_state": state,
        "unit_id": spec.root,
    }


def dependency_slug(ident: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", ident.lower()).strip("-")


def assessment_additions(spec: AssessmentSpec, data: dict[str, Any], parsed: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    reader_lines = data["raw"][spec.reader_path].splitlines(keepends=True)
    units: list[dict[str, Any]] = [
        unit_record(
            spec, parsed, reader_lines, spec.local_root, "reader_unit", parsed["frontmatter_title"],
            spec.order, parsed["root_span"], parsed["concepts"], None, None,
        )
    ]
    for number in range(1, 9):
        for offset, kind in enumerate(("exercise", "hint", "solution"), 1):
            block = parsed["blocks"][number][kind]
            token = {"exercise": "ex", "hint": "hint", "solution": "sol"}[kind]
            label = {"exercise": "Soal", "hint": "Petunjuk", "solution": "Solusi lengkap"}[kind]
            units.append(unit_record(
                spec, parsed, reader_lines, f"{spec.local_root}-{token}-{number:03d}", kind,
                f"{label} {number}: {parsed['section_titles'][number]}", (number - 1) * 3 + offset,
                block["span"], block["concepts"], number, block,
            ))
    segments = [segment_from_unit(record, spec.rights) for record in units]
    rights = [{
        **common("rights", spec.rights),
        "attribution": f"Original {spec.assessment_id} cumulative assessment prepared for the independent Indonesian O012/D60 edition.",
        "change_notice": "Edition-original assessment layer; Roberts and Fomberg source components are neither copied nor relicensed.",
        "component_scope": [record["id"] for record in units],
        "license_expression": "CC-BY-SA-4.0",
        "license_url": "https://creativecommons.org/licenses/by-sa/4.0/",
        "non_endorsement": "Independent Indonesian edition; no Roberts, Fomberg, Lazarovich, or source-author endorsement.",
        "third_party_status": "No Roberts or Fomberg prompt, solution, or expression is copied or adapted; existing authority IDs are context only.",
    }]

    qa_ids = {kind: f"qa:{spec.local_root}-{kind}" for kind in ("structure", "math", "language", "mastery")}
    source_artifact = f"artifact:{spec.local_root}-reader-source"
    math_artifact = f"artifact:{spec.local_root}-math-review"
    language_artifact = f"artifact:{spec.local_root}-language-review"
    qa_artifact = f"artifact:{spec.local_root}-qa-receipt"
    artifacts = [
        artifact(spec, data["identities"], source_artifact, spec.reader_path, "text/markdown", list(qa_ids.values()), "structurally_verified"),
        artifact(spec, data["identities"], math_artifact, spec.math_path, "application/json", [qa_ids["math"]], "mathematically_reviewed"),
        artifact(spec, data["identities"], language_artifact, spec.language_path, "application/json", [qa_ids["language"]], "language_reviewed"),
        artifact(spec, data["identities"], qa_artifact, COMBINED_QA_PATH, "application/json", list(qa_ids.values()), "built"),
    ]
    qa_events = [
        {**common("qa_event", qa_ids["structure"]), "assessment_id": spec.assessment_id, "note": "Stable-ID inventory, eight balanced triples, explicit route metadata, LF/UTF-8, rights, provenance, and privacy checks passed.", "qa_type": "structure", "result": "passed", "unit_id": spec.root, "witness_artifact_ids": [source_artifact, qa_artifact]},
        {**common("qa_event", qa_ids["math"]), "assessment_id": spec.assessment_id, "note": "Independent mathematics review passed all eight exercise/hint/solution triples with P1=P2=P3=0.", "qa_type": "math", "result": "passed", "unit_id": spec.root, "witness_artifact_ids": [math_artifact, qa_artifact]},
        {**common("qa_event", qa_ids["language"]), "assessment_id": spec.assessment_id, "note": "Independent id-ID source-language, terminology, accessibility, rights, and provenance review passed with P1=P2=P3=0.", "qa_type": "language", "result": "passed", "unit_id": spec.root, "witness_artifact_ids": [language_artifact, qa_artifact]},
        {**common("qa_event", qa_ids["mastery"]), "assessment_id": spec.assessment_id, "note": "Eight cumulative exercises each have one stable hint and one complete checked solution with explicit prerequisite mappings.", "qa_type": "mastery", "result": "passed", "unit_id": spec.root, "witness_artifact_ids": [source_artifact, qa_artifact]},
    ]

    relations: list[dict[str, Any]] = [
        relation(f"relation:contains:o012-d60:{spec.code}", "contains", COURSE, spec.root, f"The O012/D60 course contains {spec.assessment_id} as an original learner surface.", assessment_id=spec.assessment_id, course_route_unit_ids=list(spec.expected_routes)),
        relation(f"relation:contains:{spec.local_root}-rights:root", "contains", spec.rights, spec.root, f"The original CC BY-SA 4.0 component rights bind the complete {spec.assessment_id} reader graph.", assessment_id=spec.assessment_id, rights_mapping_role="direct_component_binding"),
        relation(f"relation:contains:o012-d60-integrated-rights:{spec.code}-original", "contains", INTEGRATED_RIGHTS, spec.rights, f"The integrated route contains the independently licensed {spec.assessment_id} component without altering source licenses.", assessment_id=spec.assessment_id, rights_mapping_role="integrated_route_component"),
    ]
    for number in range(1, 9):
        exercise = f"unit:{spec.local_root}-ex-{number:03d}"
        hint = f"unit:{spec.local_root}-hint-{number:03d}"
        solution = f"unit:{spec.local_root}-sol-{number:03d}"
        for child, role in ((exercise, "exercise"), (hint, "hint"), (solution, "complete_checked_solution")):
            suffix = child.removeprefix(f"unit:{spec.local_root}-")
            relations.append(relation(f"relation:contains:{spec.local_root}:{suffix}", "contains", spec.root, child, f"{spec.assessment_id} contains item {number} {role}.", assessment_id=spec.assessment_id, assessment_item_number=number, contained_role=role))
        relations.append(relation(f"relation:hints:{spec.local_root}-hint-{number:03d}:ex-{number:03d}", "hints", hint, exercise, f"Stable hint for {spec.assessment_id} item {number}.", assessment_id=spec.assessment_id, assessment_item_number=number))
        relations.append(relation(f"relation:solves:{spec.local_root}-sol-{number:03d}:ex-{number:03d}", "solves", solution, exercise, f"Complete checked solution for {spec.assessment_id} item {number}.", assessment_id=spec.assessment_id, assessment_item_number=number, solution_status="complete_checked_solution"))
        block = parsed["blocks"][number]["exercise"]
        for role, route_id in [("primary", block["primary"]), *(("secondary", route) for route in block["secondary"])]:
            anchor = ROUTE_ANCHORS[route_id]
            marker = "" if role == "primary" else ":secondary"
            relations.append(relation(f"relation:xref:{spec.local_root}-ex-{number:03d}:{route_id.lower()}{marker}", "xref", exercise, anchor, f"{role.title()} course-route mapping for {spec.assessment_id} item {number}: {route_id}.", assessment_id=spec.assessment_id, assessment_item_number=number, course_route_unit_id=route_id, route_mapping_role=role, route_source_anchor_id=anchor))
        for dep_order, anchor in enumerate(spec.dependencies[number], 1):
            relations.append(relation(f"relation:depends-on:{spec.local_root}-ex-{number:03d}:{dep_order:02d}:{dependency_slug(anchor)}", "depends-on", exercise, anchor, f"{spec.assessment_id} item {number} requires the admitted result or unit {anchor}.", assessment_id=spec.assessment_id, assessment_item_number=number, dependency_order=dep_order, dependency_role="assessment_prerequisite"))

    out = {name: [] for name in FILES}
    out["units.jsonl"] = units
    out["segments.jsonl"] = segments
    out["rights.jsonl"] = rights
    out["qa.jsonl"] = qa_events
    out["artifacts.jsonl"] = artifacts
    out["relations.jsonl"] = relations
    return out


def build_additions(data: dict[str, Any]) -> tuple[dict[str, list[dict[str, Any]]], dict[str, dict[str, Any]]]:
    parsed = {spec.code: parse_reader(spec, data["raw"][spec.reader_path]) for spec in SPECS}
    additions = {name: [] for name in FILES}
    for spec in SPECS:
        part = assessment_additions(spec, data, parsed[spec.code])
        for name in FILES:
            additions[name].extend(part[name])
    for name in FILES:
        additions[name] = sorted(additions[name], key=lambda record: record["id"])
    return additions, parsed


def suffixes(additions: dict[str, list[dict[str, Any]]]) -> dict[str, bytes]:
    return {name: b"".join(canon(record) for record in additions[name]) for name in FILES}


def record_plan(additions: dict[str, list[dict[str, Any]]], data: dict[str, Any]) -> dict[str, Any]:
    raw = suffixes(additions)
    return {
        "assessment_ids": [spec.assessment_id for spec in SPECS],
        "edition_unit_ids": [spec.edition_unit_id for spec in SPECS],
        "immutable_prefix": {"records": PREFIX_TOTAL[0], "bytes": PREFIX_TOTAL[1], "bundle_sha256": PREFIX_TOTAL[2]},
        "input_identities": {
            relative: {"bytes": value[0], "lf_lines": value[1], "sha256": value[2]}
            for relative, value in sorted(data["identities"].items())
        },
        "records_by_file": {name: len(additions[name]) for name in FILES},
        "bytes_by_file": {name: len(raw[name]) for name in FILES},
        "record_ids_by_file": {name: [record["id"] for record in additions[name]] for name in FILES},
    }


def validate_assessment_semantics(
    spec: AssessmentSpec,
    additions: dict[str, list[dict[str, Any]]],
    parsed: dict[str, Any],
    by_id: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    units = [record for record in additions["units.jsonl"] if record.get("assessment_id") == spec.assessment_id]
    segments = [record for record in additions["segments.jsonl"] if record.get("assessment_id") == spec.assessment_id]
    relations = [record for record in additions["relations.jsonl"] if record.get("assessment_id") == spec.assessment_id]
    artifacts = [record for record in additions["artifacts.jsonl"] if record.get("assessment_id") == spec.assessment_id]
    qa_events = [record for record in additions["qa.jsonl"] if record.get("assessment_id") == spec.assessment_id]
    rights = [record for record in additions["rights.jsonl"] if record["id"] == spec.rights]
    require(len(units) == len(segments) == 25, f"{spec.assessment_id} root-plus-triples census mismatch")
    require(Counter(record["unit_kind"] for record in units) == Counter({"reader_unit": 1, "exercise": 8, "hint": 8, "solution": 8}), f"{spec.assessment_id} unit-kind census mismatch")
    require(Counter(record["segment_kind"] for record in segments) == Counter({"assessment": 1, "exercise": 8, "hint": 8, "solution": 8}), f"{spec.assessment_id} segment-kind census mismatch")
    segment_by_local = {record["source_local_id"]: record for record in segments}
    require({record["source_local_id"] for record in units} == set(segment_by_local), f"{spec.assessment_id} unit/segment inventory mismatch")
    for unit in units:
        segment = segment_by_local[unit["source_local_id"]]
        require(segment["unit_id"] == unit["id"] and segment["target_locator"] == unit["target_locator"], f"{spec.assessment_id} unit/segment locator mismatch: {unit['id']}")
        require(unit["original_layer"] is True and unit["source_corpus_used"] is False and unit["provenance_relation"] == "edition_original", f"{spec.assessment_id} original/source demarcation mismatch")
        require(unit["rights_component_id"] == spec.rights and segment["rights_component_id"] == spec.rights, f"{spec.assessment_id} rights binding mismatch")
        require(unit["model_provenance"] == MODEL and unit["locale"] == "id-ID", f"{spec.assessment_id} locale/model provenance mismatch")
        require(all(concept in by_id and by_id[concept]["entity_type"] == "concept" for concept in unit["concept_ids"]), f"{spec.assessment_id} unresolved concept mapping: {unit['id']}")
    require(all(record.get("solution_status") == "complete_checked_solution" for record in units if record["unit_kind"] == "solution"), f"{spec.assessment_id} solution status mismatch")

    for number in range(1, 9):
        exercise_id = f"unit:{spec.local_root}-ex-{number:03d}"
        exercise = by_id[exercise_id]
        block = parsed["blocks"][number]["exercise"]
        require(exercise["primary_course_route_unit_id"] == block["primary"] and exercise["secondary_course_route_unit_ids"] == list(block["secondary"]), f"{spec.assessment_id} item {number} route fields mismatch")
        require(exercise["concept_ids"] == list(block["concepts"]), f"{spec.assessment_id} item {number} concept fields mismatch")
        route_links = [record for record in relations if record["from_id"] == exercise_id and record["relation_type"] == "xref"]
        expected_routes = {("primary", block["primary"], ROUTE_ANCHORS[block["primary"]]), *(("secondary", route, ROUTE_ANCHORS[route]) for route in block["secondary"])}
        observed_routes = {(record["route_mapping_role"], record["course_route_unit_id"], record["to_id"]) for record in route_links}
        require(observed_routes == expected_routes, f"{spec.assessment_id} item {number} xref closure mismatch")
        dependencies = [record for record in relations if record["from_id"] == exercise_id and record["relation_type"] == "depends-on"]
        require([record["to_id"] for record in sorted(dependencies, key=lambda item: item["dependency_order"])] == list(spec.dependencies[number]), f"{spec.assessment_id} item {number} dependency closure mismatch")
        require(all(record["to_id"] in by_id for record in dependencies), f"{spec.assessment_id} item {number} dependency target absent")
        hints = [record for record in relations if record["relation_type"] == "hints" and record["to_id"] == exercise_id]
        solves = [record for record in relations if record["relation_type"] == "solves" and record["to_id"] == exercise_id]
        require(len(hints) == len(solves) == 1 and solves[0].get("solution_status") == "complete_checked_solution", f"{spec.assessment_id} item {number} triple graph mismatch")

    require(len(rights) == 1 and rights[0]["license_expression"] == "CC-BY-SA-4.0", f"{spec.assessment_id} rights record mismatch")
    require(set(rights[0]["component_scope"]) == {record["id"] for record in units}, f"{spec.assessment_id} rights component scope mismatch")
    require(len(artifacts) == 4 and {record["path"] for record in artifacts} == {spec.reader_path, spec.math_path, spec.language_path, COMBINED_QA_PATH}, f"{spec.assessment_id} artifact evidence set mismatch")
    require(Counter(record["qa_type"] for record in qa_events) == Counter({"structure": 1, "math": 1, "language": 1, "mastery": 1}), f"{spec.assessment_id} QA event census mismatch")
    require(all(record["result"] == "passed" and record["witness_artifact_ids"] for record in qa_events), f"{spec.assessment_id} QA witness closure mismatch")
    return {
        "assessment_id": spec.assessment_id,
        "units": 25,
        "segments": 25,
        "exercises": 8,
        "hints": 8,
        "complete_solutions": 8,
        "route_coverage": sorted({parsed["blocks"][number]["exercise"]["primary"] for number in range(1, 9)}),
        "dependency_edges": sum(len(value) for value in spec.dependencies.values()),
    }


def validate_semantics(
    prefix_records: list[dict[str, Any]],
    additions: dict[str, list[dict[str, Any]]],
    data: dict[str, Any],
    parsed: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    added_records = [record for name in FILES for record in additions[name]]
    records = prefix_records + added_records
    by_id = {record["id"]: record for record in records}
    require(len(by_id) == len(records), "global ID collision in merged graph")
    generic = load_generic()
    try:
        generic.validate_shapes(records)
        generic.validate_references(records, by_id)
        generic.validate_artifact_manifests(records, LANE)
    except Exception as exc:
        raise SystemExit(f"CA02+CA03 backend producer FAIL: merged generic schema/reference validation failed: {exc}")
    required_context = {
        COURSE, PROGRAM, ROBERTS_EDITION, ROBERTS_RESOURCE, FOMBERG_EDITION,
        FOMBERG_RESOURCE, INTEGRATED_RIGHTS, *ROUTE_ANCHORS.values(),
        *(anchor for spec in SPECS for anchors in spec.dependencies.values() for anchor in anchors),
    }
    require(required_context <= by_id.keys(), f"required authority/prerequisite IDs absent: {sorted(required_context - by_id.keys())}")
    assessment_results = [validate_assessment_semantics(spec, additions, parsed[spec.code], by_id) for spec in SPECS]
    require(sum(result["exercises"] for result in assessment_results) == 16, "combined assessment exercise census mismatch")
    require(sum(result["hints"] for result in assessment_results) == 16, "combined assessment hint census mismatch")
    require(sum(result["complete_solutions"] for result in assessment_results) == 16, "combined assessment solution census mismatch")
    for artifact_record in additions["artifacts.jsonl"]:
        expected = data["identities"][artifact_record["path"]]
        require((artifact_record["bytes"], artifact_record["sha256"]) == (expected[0], expected[2]), f"artifact identity mismatch: {artifact_record['path']}")
    joined = b"".join(suffixes(additions)[name] for name in FILES).lower()
    credential_markers = (
        b"c:\\users",
        b"github_pat_",
        b"ghp_",
        b"access_token",
        b"authorization" + b": bearer",
    )
    require(all(marker not in joined for marker in credential_markers), "private path or credential marker in suffix")
    relation_counts = Counter(record["relation_type"] for record in additions["relations.jsonl"])
    return {
        "merged_records": len(records),
        "added_records": len(added_records),
        "assessment_results": assessment_results,
        "assessment_items_added": 16,
        "cumulative_assessment_items_after_append": 24,
        "required_solution_bearing_slots_after_append": 108,
        "unit_kind_counts": dict(Counter(record["unit_kind"] for record in additions["units.jsonl"])),
        "segment_kind_counts": dict(Counter(record["segment_kind"] for record in additions["segments.jsonl"])),
        "relation_type_counts": dict(relation_counts),
        "qa_type_counts": dict(Counter(record["qa_type"] for record in additions["qa.jsonl"])),
        "schema_shapes": "PASS",
        "global_references": "PASS",
        "artifact_evidence": "PASS",
        "concept_closure": "PASS",
        "original_source_demarcation": "PASS",
        "route_and_prerequisite_mapping": "PASS",
        "rights_and_provenance_closure": "PASS",
        "global_id_uniqueness": "PASS",
    }


def backend_totals(backend: Path) -> tuple[int, int, str]:
    bundle = hashlib.sha256()
    record_count = byte_count = 0
    for name in FILES:
        raw = (backend / name).read_bytes()
        record_count += len(raw.splitlines()); byte_count += len(raw)
        bundle.update(name.encode("utf-8")); bundle.update(b"\0"); bundle.update(raw)
    return record_count, byte_count, bundle.hexdigest()


def append_suffix(backend: Path, prefix: dict[str, bytes], additions: dict[str, list[dict[str, Any]]]) -> dict[str, bytes]:
    raw_suffixes = suffixes(additions)
    for name in FILES:
        require((backend / name).read_bytes() == prefix[name], f"prefix changed immediately before append: {name}")
    for name in FILES:
        if raw_suffixes[name]:
            with (backend / name).open("ab") as stream:
                stream.write(raw_suffixes[name])
    for name in FILES:
        require((backend / name).read_bytes() == prefix[name] + raw_suffixes[name], f"exact binary append mismatch: {name}")
    return raw_suffixes


def main() -> int:
    require(sys.argv[1:] in ([], ["--plan"]), "accepted invocation is no arguments or --plan")
    data = verify_inputs()
    additions, parsed = build_additions(data)
    plan = record_plan(additions, data)
    if sys.argv[1:] == ["--plan"]:
        print(json.dumps(plan, ensure_ascii=False, sort_keys=True, indent=2))
        return 0

    baseline_raw = read_disciplined(BASELINE_RECEIPT_PATH)
    require(
        identity(baseline_raw) == BASELINE_RECEIPT_IDENTITY,
        "ordinary-hint cumulative receipt identity drift",
    )
    baseline = json.loads(baseline_raw)
    require(
        baseline.get("status") == "PASS"
        and baseline.get("receipt_kind") == "cumulative_backend_boundary"
        and baseline.get("cumulative")
        == {"records": PREFIX_TOTAL[0], "bytes": PREFIX_TOTAL[1], "bundle_sha256": PREFIX_TOTAL[2]}
        and baseline.get("replay", {}).get("status") == "PASS"
        and baseline.get("replay", {}).get("exact_file_matches") == len(FILES)
        and baseline.get("replay", {}).get("temporary_replay_removed") is True
        and baseline.get("replay", {}).get("final")
        == {"records": PREFIX_TOTAL[0], "bytes": PREFIX_TOTAL[1], "bundle_sha256": PREFIX_TOTAL[2]},
        "ordinary-hint cumulative receipt does not prove the exact immutable baseline",
    )
    prefix, prefix_records = verify_prefix(BACKEND)
    semantic = validate_semantics(prefix_records, additions, data, parsed)
    refreshed = verify_inputs(data["identities"])
    refreshed_additions, refreshed_parsed = build_additions(refreshed)
    require(record_plan(refreshed_additions, refreshed) == plan, "sealed inputs changed the deterministic plan before append")
    require(suffixes(refreshed_additions) == suffixes(additions) and refreshed_parsed == parsed, "sealed inputs changed the derived suffix before append")
    raw_suffixes = append_suffix(BACKEND, prefix, additions)
    final = backend_totals(BACKEND)
    require(final[0] == PREFIX_TOTAL[0] + semantic["added_records"], "cumulative record count mismatch")
    print("CA02+CA03 append-only semantic backend extension: PASS")
    print(f"prefix_records={PREFIX_TOTAL[0]}")
    print(f"prefix_bytes={PREFIX_TOTAL[1]}")
    print(f"prefix_bundle_sha256={PREFIX_TOTAL[2]}")
    print(f"records_added={semantic['added_records']}")
    print(f"suffix_bytes={sum(len(raw_suffixes[name]) for name in FILES)}")
    print(f"cumulative_records={final[0]}")
    print(f"cumulative_bytes={final[1]}")
    print(f"backend_bundle_sha256={final[2]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
