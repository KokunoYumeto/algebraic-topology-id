#!/usr/bin/env python3
"""Frozen inputs and deterministic backend records for Fomberg Unit 005."""
from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


LANE = Path(__file__).resolve().parents[1]
BACKEND = LANE / "backend"
FILES = (
    "artifacts.jsonl", "assets.jsonl", "authority.jsonl", "concepts.jsonl",
    "corrections.jsonl", "qa.jsonl", "relations.jsonl", "rights.jsonl",
    "segments.jsonl", "terms.jsonl", "units.jsonl",
)
SCHEMA = "curriculum.interop"
VERSION = "0.1.0"
WORKFLOW = "o012-d60-id-reader-production"
STAMP = "2026-08-25T00:00:00Z"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"

SOURCE_PATH = "source/id-ID/fomberg/units/fomberg-unit-005-degree-maps-local-degree.md"
SOURCE = LANE / SOURCE_PATH
SOURCE_IDENTITY = (
    40274, 1150,
    "ad6e31291e3df97b81f7e5a30144ca27157f907291e74f4d49c09a0620487075",
)
UPSTREAM_PATH = (
    "authority/upstream/math-notes-563194fae879178b9a6871b249513bfc27968975/"
    "tree/algebraic_topology.tex"
)
UPSTREAM = LANE / UPSTREAM_PATH
UPSTREAM_IDENTITY = (
    223886, 6069,
    "d27095de0f38f0c14b2d7716cb52d51d064f0594dd9f82f9d1b3e6af5b35a483",
)
SPAN_IDENTITY = (
    2847, 3122, 276, 12203,
    "9ac1d27872a09134b75bb077ad113716a9e828c2177ac296e7bf3331395da85a",
)
NEXT_SOURCE_LINE = 3123
NEXT_HEADING = r"\subsection{Cellular complexes}"
COMMIT = "563194fae879178b9a6871b249513bfc27968975"
TREE = "fb678966d1533d529bdd72f49d8496a3bdc14a9b"
RESOURCE = "resource:fomberg-algebraic-topology-2025"
EDITION = "edition:fomberg-at-2025-563194f"
ROOT = "unit:o012-fom-u005"
PROGRAM = "program:o012-id"
COURSE = "course:o012-d60"
ROUTE = "D60-R12"

SOURCE_RIGHTS = "rights:fomberg-cc-by-sa-4.0"
COMPANION_RIGHTS = "rights:o012-fom-u005-companion-cc-by-sa-4.0"
COMPOSITE_RIGHTS = "rights:o012-fom-u005-composite-cc-by-sa-4.0"
ROUTE_RIGHTS = "rights:o012-d60-integrated-route-cc-by-sa-4.0"

PREFIX = {
    "artifacts.jsonl": (180, 145936, "9aaa2a823b1b5747081948e6131e36f03e28ddd22e604fb36f7be1001fbe0f14"),
    "assets.jsonl": (61, 44168, "4017d02b4dc8c40577d09b01438908fd291273623d0e7490521a56f5760cf6a5"),
    "authority.jsonl": (6, 4374, "84c622f56dbbd5ba379361245ecfe07bc79c9f4fd6b18ba21b82b5f545211869"),
    "concepts.jsonl": (433, 136682, "e6de4c97fa43fd753157a665c7206f9a8cbe3eaa3159bfc423afc2f351c2a0fc"),
    "corrections.jsonl": (522, 534044, "5885a6375d4f9b8952f27642f47a0c2615a4aaa5f8f1dcc0976210b8fe23806d"),
    "qa.jsonl": (150, 83298, "19e53f8c8507cd91ba4e0352d57fac792920c0385555513ea6a20592e916b656"),
    "relations.jsonl": (708, 296800, "699d81f5e04ca3243b2450e1845f8dd668785ecc1090bb9a4ad2835e17a01c41"),
    "rights.jsonl": (97, 88270, "82805c95a8cb20a2d1b82f8a9a1f39e5769876d4e608064d4d1915ea282a2d69"),
    "segments.jsonl": (1750, 2763398, "6e7c86912f88f3851bbd8d459cb324a21e14fae10b4b20b7f76a4e287e9c2cef"),
    "terms.jsonl": (426, 277358, "b851b7b07fc9bdd3d4eb4864934d5eee5682f7d2a50854d4ac1c2eb2aa30e645"),
    "units.jsonl": (1780, 2909971, "d488eb464eae4a09d557e1628fd8b2f721373acf31b818eb9f1e6036562d2b74"),
}
PREFIX_TOTAL = (
    6113, 7284299,
    "902eb71aa8a8b25e824ebe9ddae556e914e370d603382f28860392d6e186baba",
)

EXPECTED_CLASSES = {
    "boundary": 1, "definition": 2, "example": 1, "exercise": 6,
    "figure": 1, "heading": 6, "hint": 6, "proof": 3,
    "proof-supplement": 1, "proposition": 2, "remark": 4,
    "solution": 6, "source-audit": 11, "source-omission": 1,
    "theorem": 1,
}
DELTA = {
    "artifacts.jsonl": 3,
    "assets.jsonl": 2,
    "authority.jsonl": 0,
    "concepts.jsonl": 20,
    "corrections.jsonl": 11,
    "qa.jsonl": 4,
    "relations.jsonl": 30,
    "rights.jsonl": 2,
    "segments.jsonl": 52,
    "terms.jsonl": 20,
    "units.jsonl": 52,
}

AUDIT_PATH = "qa/FOMBERG_UNIT_005_SOURCE_AUDIT.json"
QA_PATH = "qa/FOMBERG_UNIT_005_QA.json"
REVIEW_PATH = "qa/fomberg-unit-005/INDEPENDENT_REVIEW_FINAL.json"
ROBERTS_WITNESS_PATH = "source/id-ID/units/unit-030-lecture-030.md"
EVIDENCE_PATHS = (AUDIT_PATH, REVIEW_PATH, QA_PATH)
SEALED_IDENTITIES: dict[str, tuple[int, str]] = {
    AUDIT_PATH: (4190, "2c8280c954bdad90995c8d209b94e9355962e3c724ffedbd1ad84675828b2135"),
    REVIEW_PATH: (2878, "bcf628eb480234d217c235727c2082289f0cc09d8062d822c1e33964c072a6e0"),
    QA_PATH: (6268, "874d9ef02875d4fbc28458e56b2c2894be8c990a9fd1c333a0327ccd2d3c4964"),
    "00_control/TERMINOLOGY.csv": (56920, "4f3ec0ee76769ac297b3ed820c1e46645277d87c4eb30cbde5358f2cca72b68f"),
    "00_control/ADVERSE_LEDGER.csv": (194914, "ebf0157674a1db25690480defe4046e2e9a3e1d5322368af2b5a8f3e94597388"),
    ROBERTS_WITNESS_PATH: (23008, "88da8cf71d0f81328bdd65b0dea7d54c48655ed8836e230eaed821796b61b08d"),
}

ALIASES = {
    "def:local-degree": "o012-fom-u005-def-local-degree",
    "prop:local-degree-for-global-degree": "o012-fom-u005-prop-local-to-global",
}
TERM_SPECS = (
    ("sphere-reflection", "O012-TERM-0435", "prop-degree-properties"),
    ("induced-homomorphism", "O012-TERM-0436", "def-degree"),
    ("orientation-generator", "O012-TERM-0437", "def-degree"),
    ("top-homology", "O012-TERM-0438", "proof-degree-properties"),
    ("hopf-theorem", "O012-TERM-0439", "rem-hopf-theorem"),
    ("homological-degree", "O012-TERM-0440", "local-degree"),
    ("cohomological-degree", "O012-TERM-0441", "local-degree"),
    ("local-degree", "O012-TERM-0442", "def-local-degree"),
    ("local-orientation", "O012-TERM-0443", "rem-local-homeomorphism"),
    ("local-homeomorphism", "O012-TERM-0444", "rem-piecewise-degree"),
    ("orientation-reversing", "O012-TERM-0445", "mcheck-004"),
    ("local-to-global-degree-formula", "O012-TERM-0446", "prop-local-to-global"),
    ("fundamental-class", "O012-TERM-0447", "proof-local-to-global"),
    ("power-map", "O012-TERM-0448", "ex-power-map"),
    ("angular-coordinates", "O012-TERM-0449", "ex-power-map"),
    ("signed-local-contribution", "O012-TERM-0450", "rem-piecewise-degree"),
    ("kronecker-pairing", "O012-TERM-0451", "mcheck-001"),
    ("dual-generator", "O012-TERM-0452", "mcheck-001"),
    ("fixed-point-criterion", "O012-TERM-0453", "mcheck-002"),
    ("angular-lift", "O012-TERM-0454", "mcheck-006"),
)


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canon(obj: dict[str, Any]) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8") + b"\n"


def common(kind: str, ident: str) -> dict[str, Any]:
    return {
        "entity_type": kind, "id": ident, "schema": SCHEMA,
        "schema_version": VERSION, "status": "active", "supersedes": None,
        "timestamp": STAMP, "workflow": WORKFLOW,
    }


def require_identity(relative: str, expected: tuple[int, str]) -> bytes:
    raw = (LANE / relative).read_bytes()
    if (len(raw), digest(raw)) != expected:
        raise SystemExit(f"frozen input identity mismatch: {relative}")
    return raw


def sealed_identities() -> dict[str, tuple[int, str]]:
    return dict(SEALED_IDENTITIES)


def verify_prefix(backend: Path = BACKEND) -> tuple[dict[str, bytes], list[dict[str, Any]]]:
    prefix: dict[str, bytes] = {}
    records: list[dict[str, Any]] = []
    seen: set[str] = set()
    bundle = hashlib.sha256()
    for name in FILES:
        raw = (backend / name).read_bytes()
        count, size, sha = PREFIX[name]
        if (len(raw.splitlines()), len(raw), digest(raw)) != (count, size, sha):
            raise SystemExit(f"{name}: immutable Unit 004 boundary mismatch")
        if b"\r" in raw or not raw.endswith(b"\n"):
            raise SystemExit(f"{name}: invalid LF discipline")
        for number, line in enumerate(raw.splitlines(keepends=True), 1):
            obj = json.loads(line.decode("utf-8"))
            if canon(obj) != line or obj["id"] in seen:
                raise SystemExit(f"{name}:{number}: noncanonical or duplicate prefix")
            seen.add(obj["id"])
            records.append(obj)
        prefix[name] = raw
        bundle.update(name.encode("utf-8")); bundle.update(b"\0"); bundle.update(raw)
    observed = (len(records), sum(map(len, prefix.values())), bundle.hexdigest())
    if observed != PREFIX_TOTAL:
        raise SystemExit(f"immutable Unit 004 bundle mismatch: {observed!r}")
    return prefix, records


def _attrs(text: str) -> dict[str, str]:
    return {m.group(1): m.group(2) for m in re.finditer(r'(data-[a-z-]+)="([^"]*)"', text)}


def parse_reader() -> tuple[list[str], list[dict[str, Any]]]:
    raw = SOURCE.read_bytes()
    if (len(raw), raw.count(b"\n"), digest(raw)) != SOURCE_IDENTITY:
        raise SystemExit("Fomberg Unit 005 reader identity mismatch")
    if raw.startswith(b"\xef\xbb\xbf") or b"\r" in raw or not raw.endswith(b"\n"):
        raise SystemExit("reader must be UTF-8 without BOM and LF-only")
    text = raw.decode("utf-8", errors="strict")
    if "\ufffd" in text or text.count(MODEL) != 1:
        raise SystemExit("reader encoding/model-provenance mismatch")
    lines = text.splitlines()
    nodes: list[dict[str, Any]] = []
    heading_re = re.compile(r'^(#{1,6})\s+(.*?)\s*\{([^}]*)\}\s*$')
    for number, line in enumerate(lines, 1):
        match = heading_re.match(line)
        if not match:
            continue
        ident = re.search(r'#(o012-fom-u005(?:-[A-Za-z0-9-]+)?)', match.group(3))
        if ident:
            nodes.append({
                "id": ident.group(1), "kind": "heading", "line_start": number,
                "level": len(match.group(1)), "title": match.group(2),
                "attrs": _attrs(match.group(3)), "opener_end": number,
                "enclosing_div": None,
            })
    stack: list[tuple[int, dict[str, Any] | None]] = []
    number = 1
    while number <= len(lines):
        stripped = lines[number - 1].strip()
        opener_match = re.match(r'^(:{3,})\s+\{', stripped)
        closer_match = re.fullmatch(r'(:{3,})', stripped)
        if opener_match:
            width = len(opener_match.group(1))
            opener_start = number
            opener = [lines[number - 1]]
            while "}" not in opener[-1] and number < len(lines):
                number += 1; opener.append(lines[number - 1])
            joined = " ".join(opener)
            ident = re.search(r'#(o012-fom-u005(?:-[A-Za-z0-9-]+)?)', joined)
            kind = re.match(r'^:{3,}\s*\{\.([^\s}]+)', opener[0].strip())
            node = None
            if ident and kind:
                enclosing = next((item[1]["id"] for item in reversed(stack) if item[1] is not None), None)
                node = {
                    "id": ident.group(1), "kind": kind.group(1),
                    "line_start": opener_start, "opener_end": number,
                    "attrs": _attrs(joined), "enclosing_div": enclosing,
                }
            stack.append((width, node))
        elif closer_match:
            width = len(closer_match.group(1))
            if not stack or stack[-1][0] != width:
                raise SystemExit(f"fenced-div close mismatch at reader line {number}")
            _, node = stack.pop()
            if node:
                node["line_end"] = number
                body = [item.strip() for item in lines[node["opener_end"]:number - 1] if item.strip()]
                node["title"] = body[0] if body else node["kind"]
                nodes.append(node)
        number += 1
    if stack:
        raise SystemExit("reader has unclosed fenced div")
    by_local = {node["id"]: node for node in nodes}
    headings = [
        "o012-fom-u005-notice", "o012-fom-u005", "o012-fom-u005-s11a",
        "o012-fom-u005-s11b", "o012-fom-u005-local-degree",
        "o012-fom-u005-mastery",
    ]
    if any(ident not in by_local for ident in headings):
        raise SystemExit("reader heading set incomplete")
    boundary_start = by_local["o012-fom-u005-boundary-001"]["line_start"]
    by_local["o012-fom-u005-notice"]["line_end"] = by_local["o012-fom-u005"]["line_start"] - 1
    by_local["o012-fom-u005"]["line_end"] = by_local["o012-fom-u005-mastery"]["line_start"] - 1
    by_local["o012-fom-u005-s11a"]["line_end"] = by_local["o012-fom-u005-s11b"]["line_start"] - 1
    by_local["o012-fom-u005-s11b"]["line_end"] = by_local["o012-fom-u005-local-degree"]["line_start"] - 1
    by_local["o012-fom-u005-local-degree"]["line_end"] = by_local["o012-fom-u005-mastery"]["line_start"] - 1
    by_local["o012-fom-u005-mastery"]["line_end"] = boundary_start - 1
    nodes.sort(key=lambda item: (item["line_start"], 0 if item["kind"] == "heading" else 1))
    ids = [node["id"] for node in nodes]
    classes = Counter(node["kind"] for node in nodes)
    if len(ids) != 52 or len(set(ids)) != 52 or dict(sorted(classes.items())) != EXPECTED_CLASSES:
        raise SystemExit(f"reader stable-ID/class census mismatch: {len(ids)}, {dict(classes)}")
    if [node["id"] for node in nodes if node["kind"] == "heading"] != headings:
        raise SystemExit("reader heading identity/order mismatch")
    aliases = {node["attrs"]["data-source-label"]: node["id"] for node in nodes if "data-source-label" in node["attrs"]}
    if aliases != ALIASES:
        raise SystemExit(f"source alias mismatch: {aliases}")
    return lines, nodes


def verify_upstream() -> None:
    raw = UPSTREAM.read_bytes()
    if (len(raw), raw.count(b"\n"), digest(raw)) != UPSTREAM_IDENTITY:
        raise SystemExit("frozen Fomberg authoring source mismatch")
    lines = raw.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n").splitlines()
    start, end, count, size, sha = SPAN_IDENTITY
    span = ("\n".join(lines[start - 1:end]) + "\n").encode("utf-8")
    if (len(span.splitlines()), len(span), digest(span)) != (count, size, sha):
        raise SystemExit("Fomberg Unit 005 upstream span mismatch")
    if lines[NEXT_SOURCE_LINE - 1].strip() != NEXT_HEADING:
        raise SystemExit("Fomberg Unit 005 next-source cursor mismatch")


def _read_csv_strict(relative: str, expected: tuple[int, str]) -> list[dict[str, str]]:
    raw = require_identity(relative, expected)
    if raw.startswith(b"\xef\xbb\xbf") or b"\r" in raw or not raw.endswith(b"\n"):
        raise SystemExit(f"control file encoding/newline mismatch: {relative}")
    return list(csv.DictReader(raw.decode("utf-8").splitlines()))


def read_controls(identities: dict[str, tuple[int, str]]) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    adverse = _read_csv_strict("00_control/ADVERSE_LEDGER.csv", identities["00_control/ADVERSE_LEDGER.csv"])
    terms = _read_csv_strict("00_control/TERMINOLOGY.csv", identities["00_control/TERMINOLOGY.csv"])
    selected_adverse = [row for row in adverse if 523 <= int(row["event_id"].rsplit("-", 1)[1]) <= 533]
    selected_terms = [row for row in terms if 435 <= int(row["term_id"].rsplit("-", 1)[1]) <= 454]
    if [row["event_id"] for row in selected_adverse] != [f"O012-ADV-{n:04d}" for n in range(523, 534)]:
        raise SystemExit("adverse-ledger Unit 005 identity closure mismatch")
    allowed = {
        "clarified_in_translation", "corrected_in_translation",
        "hypothesis_repaired_in_translation", "proof_completed_in_translation",
        "resolved_before_admission",
    }
    if any(row["status"] not in allowed for row in selected_adverse):
        raise SystemExit("adverse-ledger Unit 005 status mismatch")
    if [row["term_id"] for row in selected_terms] != [f"O012-TERM-{n:04d}" for n in range(435, 455)]:
        raise SystemExit("terminology-ledger Unit 005 identity closure mismatch")
    if any(row["status"] != "admitted" for row in selected_terms):
        raise SystemExit("terminology-ledger Unit 005 admission mismatch")
    return selected_adverse, selected_terms


def _load_json(relative: str, expected: tuple[int, str]) -> tuple[bytes, dict[str, Any]]:
    raw = require_identity(relative, expected)
    if raw.startswith(b"\xef\xbb\xbf") or b"\r" in raw or not raw.endswith(b"\n"):
        raise SystemExit(f"JSON evidence encoding/newline mismatch: {relative}")
    obj = json.loads(raw.decode("utf-8", errors="strict"))
    if not isinstance(obj, dict):
        raise SystemExit(f"JSON evidence top level is not an object: {relative}")
    return raw, obj


def verify_all_inputs(identities: dict[str, tuple[int, str]]) -> dict[str, Any]:
    if identities != SEALED_IDENTITIES:
        raise SystemExit("Unit 005 sealed-input inventory mismatch")
    verify_upstream()
    lines, nodes = parse_reader()
    adverse, terms = read_controls(identities)
    evidence = {path: _load_json(path, identities[path]) for path in EVIDENCE_PATHS}
    require_identity(ROBERTS_WITNESS_PATH, identities[ROBERTS_WITNESS_PATH])
    audit = evidence[AUDIT_PATH][1]
    qa = evidence[QA_PATH][1]
    review = evidence[REVIEW_PATH][1]
    if (
        review.get("status") != "PASS_P1_P2_P3_ZERO"
        or review.get("canonical", {}).get("sha256") != SOURCE_IDENTITY[2]
        or review.get("canonical", {}).get("lf_lines") != SOURCE_IDENTITY[1]
        or review.get("upstream_span", {}).get("sha256") != SPAN_IDENTITY[4]
        or review.get("upstream_span", {}).get("next_line") != NEXT_SOURCE_LINE
        or review.get("severity_census") != {"P1": 0, "P2": 0, "P3": 0}
        or review.get("checks", {}).get("structure", {}).get("stable_ids") != 52
        or review.get("checks", {}).get("mastery", {}).get("exercise_hint_solution_triples") != 6
    ):
        raise SystemExit("Unit 005 final independent-review binding mismatch")
    if (
        audit.get("schema_version") != "1.0.0"
        or audit.get("audit_id") != "O012-FOMBERG-UNIT-005-SOURCE-AUDIT"
        or audit.get("status") != "PASS"
        or audit.get("reader", {}).get("sha256") != SOURCE_IDENTITY[2]
        or audit.get("source", {}).get("selected_span", {}).get("sha256") != SPAN_IDENTITY[4]
        or audit.get("source", {}).get("next_line") != NEXT_SOURCE_LINE
        or audit.get("source", {}).get("mathematical_environment_total") != 13
        or audit.get("translation_closure", {}).get("mastery_triples_complete") != 6
        or audit.get("translation_closure", {}).get("proof_repairs_complete") != ["FOM-PR-12"]
        or audit.get("course_route_unit_id") != ROUTE
        or audit.get("model_provenance") != MODEL
    ):
        raise SystemExit("Unit 005 source-audit semantic binding mismatch")
    reader_qa = qa.get("reader", {})
    if (
        qa.get("schema_version") != "1.0.0"
        or qa.get("qa_id") != "O012-FOMBERG-UNIT-005-STATIC-QA"
        or qa.get("status") != "PASS"
        or reader_qa.get("identity", {}).get("sha256") != SOURCE_IDENTITY[2]
        or qa.get("source", {}).get("selected_span", {}).get("sha256") != SPAN_IDENTITY[4]
        or qa.get("source", {}).get("next_line") != NEXT_SOURCE_LINE
        or reader_qa.get("stable_ids") != 52
        or reader_qa.get("stable_ids_unique") != 52
        or reader_qa.get("semantic_class_counts") != EXPECTED_CLASSES
        or reader_qa.get("mastery", {}).get("exercise_hint_solution_triples") != 6
        or reader_qa.get("mastery", {}).get("complete_solutions") != 6
        or reader_qa.get("proof_repairs") != ["FOM-PR-12"]
        or reader_qa.get("assets", {}).get("semantic_figures") != 1
        or reader_qa.get("assets", {}).get("raster_redraws") != 0
        or reader_qa.get("fragment_links", {}).get("count") != 9
        or qa.get("model_provenance") != MODEL
        or not qa.get("gates")
        or not all(value == "PASS" for value in qa["gates"].values())
    ):
        raise SystemExit("Unit 005 static-QA semantic binding mismatch")
    audit_raw = evidence[AUDIT_PATH][0]
    audit_binding = qa.get("source_audit", {})
    if (
        audit_binding.get("path") != AUDIT_PATH
        or audit_binding.get("bytes") != len(audit_raw)
        or audit_binding.get("sha256") != digest(audit_raw)
    ):
        raise SystemExit("static-QA does not bind exact source-audit bytes")
    node_by_id = {node["id"]: node for node in nodes}
    ids = set(node_by_id)
    for number in range(1, 7):
        for kind in ("mcheck", "hint", "sol"):
            if f"o012-fom-u005-{kind}-{number:03d}" not in ids:
                raise SystemExit(f"mastery triple {number} incomplete")
    joined = "\n".join(lines)
    for marker in (
        "FOM-PR-12", "o012-fom-u005-proof-local-degree-independence",
        "o012-fom-u005-proof-local-to-global",
    ):
        if marker not in joined:
            raise SystemExit(f"required Unit 005 marker missing: {marker}")
    terms_by_id = {row["term_id"]: row for row in terms}
    for _, control_id, evidence_suffix in TERM_SPECS:
        node = node_by_id[f"o012-fom-u005-{evidence_suffix}"]
        evidence_text = "\n".join(lines[node["line_start"] - 1:node["line_end"]]).casefold()
        if terms_by_id[control_id]["id_ID"].casefold() not in evidence_text:
            raise SystemExit(f"terminology evidence lacks admitted form: {control_id}")
    return {
        "lines": lines, "nodes": nodes, "adverse": adverse, "terms": terms,
        "audit": audit, "qa": qa, "review": review,
    }


def target_locator(lines: list[str], start: int, end: int) -> dict[str, Any]:
    raw_lines = SOURCE.read_bytes().splitlines(keepends=True)
    return {
        "path": SOURCE_PATH, "line_start": start, "line_end": end,
        "file_sha256": SOURCE_IDENTITY[2],
        "content_sha256": digest(b"".join(raw_lines[start - 1:end])),
    }


def source_locator(source_range: str | None) -> dict[str, Any]:
    if source_range:
        spans = []
        for part in source_range.split(","):
            bounds = [int(value) for value in part.strip().split("-")]
            start, end = (bounds[0], bounds[0]) if len(bounds) == 1 else bounds
            spans.append({"line_start": start, "line_end": end})
        locator: dict[str, Any] = {
            "path": "algebraic_topology.tex", "commit_sha": COMMIT,
            "precision": "exact_source_span" if len(spans) == 1 else "exact_source_spans",
        }
        if len(spans) == 1:
            locator.update(spans[0])
        else:
            locator["spans"] = spans
        return locator
    return {"kind": "edition_original", "path": SOURCE_PATH, "precision": "exact_target_span"}


def clean_title(title: str, kind: str) -> str:
    value = re.sub(r"\*\*", "", title).strip()
    return value[:240] if value else kind


def parentage(nodes: list[dict[str, Any]]) -> dict[str, tuple[str, int, list[str]]]:
    by_local = {node["id"]: node for node in nodes}
    sections = (
        "o012-fom-u005-s11a", "o012-fom-u005-s11b",
        "o012-fom-u005-local-degree", "o012-fom-u005-mastery",
    )
    raw_parent: dict[str, str] = {
        "o012-fom-u005-notice": ROOT,
        "o012-fom-u005-s11a": ROOT,
        "o012-fom-u005-s11b": ROOT,
        "o012-fom-u005-local-degree": ROOT,
        "o012-fom-u005-mastery": ROOT,
        "o012-fom-u005-boundary-001": ROOT,
    }
    for node in nodes:
        ident = node["id"]
        if ident == "o012-fom-u005" or ident in raw_parent:
            continue
        if node.get("enclosing_div"):
            raw_parent[ident] = f"unit:{node['enclosing_div']}"
            continue
        section = next((sid for sid in sections if by_local[sid]["line_start"] <= node["line_start"] <= by_local[sid]["line_end"]), None)
        if section is None:
            raise SystemExit(f"cannot assign reader-node parent: {ident}")
        raw_parent[ident] = f"unit:{section}"
    children: dict[str, list[str]] = defaultdict(list)
    for ident, parent in raw_parent.items():
        children[parent].append(ident)
    for parent, local_ids in children.items():
        local_ids.sort(key=lambda ident: by_local[ident]["line_start"])

    def path_for(ident: str) -> list[str]:
        uid = f"unit:{ident}"
        parent = raw_parent[ident]
        if parent == ROOT:
            return [ROOT, uid]
        return path_for(parent.removeprefix("unit:")) + [uid]

    return {ident: (parent, children[parent].index(ident) + 1, path_for(ident)) for ident, parent in raw_parent.items()}


def load_generic():
    path = LANE / "scripts/validate-backend.py"
    raw = path.read_bytes()
    if (len(raw), digest(raw)) != (76924, "f90d19fbfb4b0525902316dd5c26550fc25c66054cddf32b385bc97f6d526b6e"):
        raise SystemExit("generic backend validator identity mismatch")
    spec = importlib.util.spec_from_file_location("o012_generic_fom005", path)
    if spec is None or spec.loader is None:
        raise SystemExit("cannot load generic backend validator")
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


def _correction_targets(row: dict[str, str], node_ids: set[str]) -> list[str]:
    targets = sorted(set(re.findall(r'#(o012-fom-u005(?:-[A-Za-z0-9-]+)?)', row["source_location"])))
    if not targets or any(target not in node_ids for target in targets):
        raise SystemExit(f"adverse row target resolution failed: {row['event_id']}")
    return targets


def build_additions(data: dict[str, Any], evidence_identities: dict[str, tuple[int, str]]) -> dict[str, list[dict[str, Any]]]:
    lines: list[str] = data["lines"]
    nodes: list[dict[str, Any]] = data["nodes"]
    additions: dict[str, list[dict[str, Any]]] = {name: [] for name in FILES}
    all_concepts = [
        "concept:degree-of-a-map", "concept:hairy-sphere-theorem",
        "concept:homology", "concept:orientation", "concept:reduced-homology",
        *[f"concept:{slug}" for slug, _, _ in TERM_SPECS],
    ]

    def add(name: str, record: dict[str, Any]) -> None:
        additions[name].append(record)

    for ident, attribution, change, third in (
        (
            COMPANION_RIGHTS,
            "Original Indonesian mastery, solutions, proof repairs, and source audits for Fomberg Unit 005.",
            "Original additions are distinguished from the Fomberg source component.",
            "Original Unit 005 companion layer; source content remains separately attributed.",
        ),
        (
            COMPOSITE_RIGHTS,
            "Fomberg source adaptation plus original Indonesian Unit 005 companion layer.",
            "Integrated reader preserves exact locators, change notices, proof-repair identity, and semantic diagram provenance.",
            "Composite Unit 005; component-scoped rights records control.",
        ),
    ):
        rec = common("rights", ident)
        rec.update(
            attribution=attribution, change_notice=change, component_scope=[ROOT],
            license_expression="CC-BY-SA-4.0",
            license_url="https://creativecommons.org/licenses/by-sa/4.0/",
            non_endorsement="Independent Indonesian edition; no source-author or lecturer endorsement.",
            third_party_status=third,
        )
        add("rights.jsonl", rec)

    terms_by_id = {row["term_id"]: row for row in data["terms"]}
    for slug, control_id, evidence_suffix in TERM_SPECS:
        row = terms_by_id[control_id]
        concept = common("concept", f"concept:{slug}")
        concept.update(canonical_label=row["source_term"], domain=row["scope"], locale_neutral=True)
        add("concepts.jsonl", concept)
        term = common("term", f"term:{slug}:id-ID")
        term.update(
            concept_id=f"concept:{slug}", evidence_segment_id=f"segment:o012-fom-u005-{evidence_suffix}",
            locale="id-ID", preferred=row["id_ID"], register="textbook",
            rejected_forms=[], rights_component_id=COMPOSITE_RIGHTS,
            scope_unit_id=ROOT, source_term=row["source_term"],
            terminology_control_id=row["term_id"], terminology_status=row["status"],
            usage_note=row["note"], variants=[],
        )
        add("terms.jsonl", term)

    parents = parentage(nodes)
    for node in nodes:
        ident = node["id"]
        uid = f"unit:{ident}"
        kind = node["kind"]
        attrs = node["attrs"]
        is_root = ident == "o012-fom-u005"
        source_range = attrs.get("data-source-lines")
        explicit_original = attrs.get("data-origin") == "edition-original"
        is_source = attrs.get("data-origin") == "source-derived"
        repair_id = attrs.get("data-repair-id")
        hybrid = is_source and repair_id is not None
        if is_root:
            rights = COMPOSITE_RIGHTS
            provenance = "composite_translated_and_original"
            parent = COURSE; order = 35; path = [ROOT]
            display = "Topologi Aljabar — Komponen Fomberg Unit 005: Derajat Pemetaan dan Derajat Lokal"
            locator = target_locator(lines, 1, len(lines))
        else:
            rights = COMPOSITE_RIGHTS if hybrid else SOURCE_RIGHTS if is_source else COMPANION_RIGHTS
            provenance = (
                "translated_with_original_proof_repair" if hybrid
                else "translated_adapted_from_upstream" if is_source
                else "edition_original_proof_repair" if repair_id and kind in {"proof", "proof-supplement", "source-omission"}
                else "edition_original"
            )
            parent, order, path = parents[ident]
            display = clean_title(node["title"], kind)
            locator = target_locator(lines, node["line_start"], node["line_end"])
        unit_kind = "reader_unit" if is_root else ("section" if kind == "heading" else kind.replace("-", "_"))
        unit = common("unit", uid)
        unit.update(
            component_source_commit=COMMIT, component_source_id=RESOURCE,
            concept_ids=all_concepts, course_id=COURSE,
            course_route_unit_id=ROUTE, display_title=display, edition_id=EDITION,
            edition_unit_id=ROOT, locale="id-ID", model_provenance=MODEL,
            order=order, parent_id=parent, path=path, program_id=PROGRAM,
            provenance_relation=provenance, resource_id=RESOURCE,
            rights_component_id=rights, source_local_id=ident,
            target_locator=locator, translation_state="structurally_verified",
            unit_kind=unit_kind,
        )
        if is_root:
            unit.update(
                edition_order=5, route_order=12,
                source_locator={
                    "path": "algebraic_topology.tex", "commit_sha": COMMIT,
                    "line_start": 2847, "line_end": 3122,
                    "precision": "exact_unit_span", "span_bytes": 12203,
                    "span_sha256": SPAN_IDENTITY[4],
                },
            )
        alias = attrs.get("data-source-label")
        if alias:
            unit["source_aliases"] = [alias]
        if repair_id:
            unit["repair_id"] = repair_id
            if kind == "source-omission":
                unit["proof_status"] = "source_omission_named"
            elif kind in {"proof", "proof-supplement", "theorem", "proposition", "definition"}:
                unit["proof_status"] = attrs.get("data-proof-status", "repair_support")
        if kind == "solution":
            unit["solution_status"] = "complete_checked_solution"
        add("units.jsonl", unit)

        if is_root:
            segment_rights = COMPOSITE_RIGHTS
            segment_provenance = "composite_translated_and_original"
            segment_locator = target_locator(lines, node["line_start"], node["line_end"])
            segment_source_locator = {
                "path": "algebraic_topology.tex", "commit_sha": COMMIT,
                "line_start": 2847, "line_end": 3122,
                "precision": "exact_unit_span",
            }
        else:
            segment_rights = rights; segment_provenance = provenance; segment_locator = locator
            segment_source_locator = source_locator(source_range if is_source or hybrid else None)
        segment = common("segment", f"segment:{ident}")
        segment.update(
            component_source_commit=COMMIT, component_source_id=RESOURCE,
            concept_ids=all_concepts, course_route_unit_id=ROUTE,
            edition_id=EDITION, edition_unit_id=ROOT, locale="id-ID",
            model_provenance=MODEL, order=order,
            provenance_relation=segment_provenance, resource_id=RESOURCE,
            rights_component_id=segment_rights,
            segment_kind="source_heading" if is_root else unit_kind,
            source_local_id=ident, source_locator=segment_source_locator,
            target_locator=segment_locator, translation_state="structurally_verified",
            unit_id=uid,
        )
        for key in ("source_aliases", "repair_id", "proof_status", "solution_status"):
            if key in unit:
                segment[key] = unit[key]
        add("segments.jsonl", segment)

    source_size, _, source_sha = SOURCE_IDENTITY
    source_asset = common("asset", "asset:o012-fom-u005-source-markdown")
    source_asset.update(
        bytes=source_size, edition_id=EDITION,
        media_type="text/markdown; charset=utf-8", path=SOURCE_PATH,
        resource_id=RESOURCE, rights_component_id=COMPOSITE_RIGHTS,
        role="canonical_reader_source", sha256=source_sha, unit_id=ROOT,
    )
    add("assets.jsonl", source_asset)
    figures = [node for node in nodes if node["kind"] == "figure"]
    diagram_asset = common("asset", "asset:o012-fom-u005-semantic-diagram-layer")
    diagram_asset.update(
        bytes=source_size, edition_id=EDITION,
        media_type="text/markdown; charset=utf-8", path=SOURCE_PATH,
        resource_id=RESOURCE, rights_component_id=COMPOSITE_RIGHTS,
        role="semantic_diagram_accessibility_layer", sha256=source_sha,
        source_diagram_count=2, semantic_figure_block_count=1,
        geometric_redraw_count=0,
        semantic_unit_ids=[f"unit:{node['id']}" for node in figures],
        unit_id=ROOT,
    )
    add("assets.jsonl", diagram_asset)

    artifact_specs = (
        ("artifact:o012-fom-u005-source-audit", AUDIT_PATH, ["qa:o012-fom-u005-source-integrity"], "source_frozen"),
        ("artifact:o012-fom-u005-review-final", REVIEW_PATH, ["qa:o012-fom-u005-math", "qa:o012-fom-u005-language"], "mathematically_reviewed"),
        ("artifact:o012-fom-u005-qa", QA_PATH, ["qa:o012-fom-u005-source-integrity", "qa:o012-fom-u005-mastery"], "built"),
    )
    for ident, relative, qa_ids, state in artifact_specs:
        size, sha = evidence_identities[relative]
        rec = common("artifact", ident)
        rec.update(
            bytes=size, locale="id-ID", manifest_artifact_id=None,
            media_type="application/json", path=relative, qa_event_ids=qa_ids,
            rights_component_id=COMPOSITE_RIGHTS, sha256=sha,
            toolchain=(
                "Fomberg Unit 005 evidence; algebraic_topology.tex:2847-3122; "
                f"{SPAN_IDENTITY[4]}; {MODEL}; route D60-R12; semantic admission only."
            ),
            translation_state=state, unit_id=ROOT,
        )
        add("artifacts.jsonl", rec)

    for ident, kind, note, witnesses in (
        (
            "qa:o012-fom-u005-source-integrity", "source",
            "Exact lines 2847-3122, cursor 3123, 52 stable IDs, two source TikZ-CD occurrences, one semantic figure block, and nine resolved links passed.",
            ["artifact:o012-fom-u005-source-audit", "artifact:o012-fom-u005-review-final", "artifact:o012-fom-u005-qa"],
        ),
        (
            "qa:o012-fom-u005-math", "math",
            "The final independent review passed P1=P2=P3=0; FOM-PR-12 is complete, including choice independence and local-to-global degree.",
            ["artifact:o012-fom-u005-review-final"],
        ),
        (
            "qa:o012-fom-u005-language", "language",
            "Final Indonesian reviews passed after terminology, provenance, notation, and source-order repairs.",
            ["artifact:o012-fom-u005-review-final"],
        ),
        (
            "qa:o012-fom-u005-mastery", "mastery",
            "Six exercises, six hints, and six complete checked solutions passed.",
            ["artifact:o012-fom-u005-qa"],
        ),
    ):
        rec = common("qa_event", ident)
        rec.update(note=note, qa_type=kind, result="passed", unit_id=ROOT, witness_artifact_ids=witnesses)
        add("qa.jsonl", rec)

    node_ids = {node["id"] for node in nodes}
    correction_type = {
        523: "hypothesis_repair", 524: "mathematical_correction",
        525: "mathematical_correction", 526: "hypothesis_repair",
        527: "source_typo", 528: "source_asset_clarification",
        529: "proof_completion", 530: "mathematical_correction",
        531: "internal_consistency_correction", 532: "provenance_and_terminology_correction",
        533: "proof_completion",
    }
    for row in data["adverse"]:
        number = int(row["event_id"].rsplit("-", 1)[1])
        targets = _correction_targets(row, node_ids)
        rec = common("correction", f"correction:o012-fom-u005-adv-{number:04d}")
        rec.update(
            adverse_ledger_id=row["event_id"], affected_unit_ids=[f"unit:{target}" for target in targets],
            correction_type=correction_type[number], edition_id=EDITION,
            evidence=row["source_location"], evidence_segment_id=f"segment:{targets[0]}",
            rationale=row["rationale"], resource_id=RESOURCE,
            source_defect=row["observed"], target_change=row["action"],
            unit_id=ROOT, upstream_report_disposition="not_contacted",
            resolution_status=row["status"],
        )
        add("corrections.jsonl", rec)

    def relation(ident: str, from_id: str, to_id: str, kind: str, note: str, **extra: Any) -> None:
        rec = common("relation", ident)
        rec.update(from_id=from_id, to_id=to_id, relation_type=kind, note=note, **extra)
        add("relations.jsonl", rec)

    relation("relation:adapts:o012-fom-u005:fomberg-edition", ROOT, EDITION, "adapts", "Indonesian Unit 005 adapts exact Fomberg lines 2847-3122.")
    relation("relation:contains:o012-d60:fomberg-u005", COURSE, ROOT, "contains", "Course route D60-R12 contains Fomberg Unit 005 as an optional degree cross-check and additive local-degree layer.", course_route_unit_id=ROUTE)
    relation("relation:precedes:o012-fom-u004:o012-fom-u005", "unit:o012-fom-u004", ROOT, "precedes", "Fomberg Unit 004 precedes Unit 005 in source order.")
    relation("relation:contains:o012-d60-rights:fomberg-u005", ROUTE_RIGHTS, ROOT, "contains", "Integrated-route rights contain the Fomberg Unit 005 composite.")
    relation("relation:precedes:o012-fom-u005:mastery", ROOT, "unit:o012-fom-u005-mastery", "precedes", "Translated source body and repair dossier precede the solved mastery layer.")
    relation(
        "relation:proves:o012-fom-u005-pr12:local-degree-independence",
        "unit:o012-fom-u005-proof-local-degree-independence",
        "unit:o012-fom-u005-def-local-degree", "proves",
        "The original common-refinement and naturality argument proves neighborhood-choice independence.", repair_id="FOM-PR-12",
    )
    relation(
        "relation:proves:o012-fom-u005-pr12:local-to-global",
        "unit:o012-fom-u005-proof-local-to-global",
        "unit:o012-fom-u005-prop-local-to-global", "proves",
        "The repaired typed source argument proves the local-to-global degree formula.", repair_id="FOM-PR-12",
    )
    relation(
        "relation:depends-on:o012-fom-u005-local-to-global:choice-independence",
        "unit:o012-fom-u005-proof-local-to-global",
        "unit:o012-fom-u005-proof-local-degree-independence", "depends-on",
        "The local-to-global argument uses the choice-independent local-degree construction.",
    )
    for number in range(1, 7):
        relation(
            f"relation:hints:fom-u005-hint-{number:03d}:mcheck-{number:03d}",
            f"unit:o012-fom-u005-hint-{number:03d}",
            f"unit:o012-fom-u005-mcheck-{number:03d}", "hints",
            f"Hint for Fomberg Unit 005 mastery check {number}.",
        )
        relation(
            f"relation:solves:fom-u005-sol-{number:03d}:mcheck-{number:03d}",
            f"unit:o012-fom-u005-sol-{number:03d}",
            f"unit:o012-fom-u005-mcheck-{number:03d}", "solves",
            f"Complete checked solution for Unit 005 mastery check {number}.",
        )
    relation(
        "relation:illustrates:fom-u005-fig-001:diagram-layer",
        "unit:o012-fom-u005-fig-local-degree",
        "asset:o012-fom-u005-semantic-diagram-layer", "illustrates",
        "The semantic reflow preserves both source TikZ-CD maps in one accessible figure block.",
    )
    xrefs = (
        ("notice:def-002", "unit:o012-fom-u005-notice", "unit:o012-rbt-l30-def-002", "The notice links the Roberts degree definition."),
        ("notice:prop-001", "unit:o012-fom-u005-notice", "unit:o012-rbt-l30-prop-001", "The notice links the Roberts degree properties."),
        ("notice:lem-001", "unit:o012-fom-u005-notice", "unit:o012-rbt-l30-lem-001", "The notice links the Roberts technical lemma."),
        ("notice:cor-001", "unit:o012-fom-u005-notice", "unit:o012-rbt-l30-cor-001", "The notice links the Roberts corollary."),
        ("notice:thm-003", "unit:o012-fom-u005-notice", "unit:o012-rbt-l30-thm-003", "The notice links the Roberts hairy-sphere theorem."),
        ("notice:proof-004", "unit:o012-fom-u005-notice", "unit:o012-rbt-l30-proof-004", "The notice links the Roberts hairy-sphere proof."),
        ("notice:proof-002", "unit:o012-fom-u005-notice", "unit:o012-rbt-l30-proof-002", "The notice links the Roberts fundamental-theorem-of-algebra proof."),
        ("fundamental-theorem:proof-002", "unit:o012-fom-u005-rem-fundamental-theorem-algebra", "unit:o012-rbt-l30-proof-002", "The source remark delegates to the independently proved Roberts result."),
        ("local-degree:mcheck-001", "unit:o012-fom-u005-local-degree", "unit:o012-fom-u005-mcheck-001", "The local-degree introduction links the solved equivalence check."),
    )
    for suffix, from_id, to_id, note in xrefs:
        relation(f"relation:xref:o012-fom-u005-{suffix}", from_id, to_id, "xref", note)

    for name, records in additions.items():
        records.sort(key=lambda item: item["id"])
        if len(records) != DELTA[name]:
            raise SystemExit(f"{name}: derived suffix count mismatch ({len(records)} != {DELTA[name]})")
        if len({record["id"] for record in records}) != len(records):
            raise SystemExit(f"{name}: duplicate derived IDs")
    return additions


def planned_additions() -> dict[str, list[dict[str, Any]]]:
    lines, nodes = parse_reader()
    adverse, terms = read_controls(SEALED_IDENTITIES)
    synthetic_evidence = {path: SEALED_IDENTITIES[path] for path in EVIDENCE_PATHS}
    return build_additions(
        {"lines": lines, "nodes": nodes, "adverse": adverse, "terms": terms},
        synthetic_evidence,
    )


def record_plan() -> dict[str, Any]:
    additions = planned_additions()
    artifact_paths = [record["path"] for record in additions["artifacts.jsonl"]]
    return {
        "edition_unit_id": ROOT, "root_unit_id": ROOT,
        "course_id": COURSE, "course_route_unit_id": ROUTE,
        "resource_id": RESOURCE, "edition_id": EDITION,
        "immutable_prefix": {
            "records": PREFIX_TOTAL[0], "bytes": PREFIX_TOTAL[1],
            "bundle_sha256": PREFIX_TOTAL[2],
        },
        "records_by_file": DELTA, "records_planned": sum(DELTA.values()),
        "record_ids_by_file": {name: [record["id"] for record in additions[name]] for name in FILES},
        "cumulative_records_planned": PREFIX_TOTAL[0] + sum(DELTA.values()),
        "stable_ids": 52, "asset_records": 2, "real_redraw_files": 0,
        "artifact_evidence_paths_in_record_order": artifact_paths,
        "unsealed_identity_paths": [],
    }
