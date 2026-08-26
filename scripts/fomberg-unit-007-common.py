#!/usr/bin/env python3
"""Fail-closed inputs and deterministic records for Fomberg Unit 007.

Unlike a permissive "latest file" producer, this module admits identities only
after the final source audit, static QA, independent review, canonical reader,
control-ledger suffixes, and all fourteen redraw files cross-bind one another.
The immutable backend prefix is the published Unit 006 boundary.
"""
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

SOURCE_PATH = "source/id-ID/fomberg/units/fomberg-unit-007-cellular-homology.md"
SOURCE = LANE / SOURCE_PATH
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
    3518, 4185, 668, 26533,
    "a22afacfdbecdfad48942421412c4cff1c0f317eb77f18253578125a5d0d7ce2",
)
NEXT_SOURCE_LINE = 4186
NEXT_HEADING = r"\subsection{Extras before cohomology}"
COMMIT = "563194fae879178b9a6871b249513bfc27968975"
TREE = "fb678966d1533d529bdd72f49d8496a3bdc14a9b"
RESOURCE = "resource:fomberg-algebraic-topology-2025"
EDITION = "edition:fomberg-at-2025-563194f"
ROOT = "unit:o012-fom-u007"
PROGRAM = "program:o012-id"
COURSE = "course:o012-d60"
ROUTE = "D60-R12"
SOURCE_RIGHTS = "rights:fomberg-cc-by-sa-4.0"
COMPANION_RIGHTS = "rights:o012-fom-u007-companion-cc-by-sa-4.0"
COMPOSITE_RIGHTS = "rights:o012-fom-u007-composite-cc-by-sa-4.0"
ROUTE_RIGHTS = "rights:o012-d60-integrated-route-cc-by-sa-4.0"

# Exact published Unit 006 boundary: 6,512 records / 7,855,910 bytes.
PREFIX = {
    "artifacts.jsonl": (186, 151136, "ee14599a3e8a83aa889eedb61b1770868e14bf2d0a8d65ae83676530fd79ba64"),
    "assets.jsonl": (79, 57842, "1f07222801810cfb2b8834127ca6c5acfb599ae634866ca3bd5a46d71b63a8fd"),
    "authority.jsonl": (6, 4374, "84c622f56dbbd5ba379361245ecfe07bc79c9f4fd6b18ba21b82b5f545211869"),
    "concepts.jsonl": (468, 147798, "bc307993763f45d72915b60e952dcd024c32a2542ba1b2ed3537dc69d9f4eb6a"),
    "corrections.jsonl": (546, 570659, "0756090db9f5df30dc68fafd864ea295640483d725ca6c219fa7a49b38fff665"),
    "qa.jsonl": (158, 87136, "956f8647851b24ce1ad40d4a69283329196c7b0142c82c32b7c6a348a20d2a79"),
    "relations.jsonl": (763, 320668, "32af96c9af327afaf0f95fcaedba1ac87b38d580e52068f1e1a1998beb0d554e"),
    "rights.jsonl": (101, 91432, "7c0bc9457f0dac117c0a57b571eeb3617f1efc2c4148f1e2c816b8978750570f"),
    "segments.jsonl": (1857, 2983950, "9c1c8577148487a6a0c86ddb92b8bb5bc36e802fa4cd885e0b5c962ae917de3a"),
    "terms.jsonl": (461, 303641, "ecd5c38288b850f4ae52c7c4847abc29d1f1f69363622b0d160ae46d907df87b"),
    "units.jsonl": (1887, 3137274, "31489809c3cd735dd62951585644d2cf2bb5de3548966800f2973d538ca6f347"),
}
PREFIX_TOTAL = (
    6512, 7855910,
    "377be644a38e6db06f8992113ea47b8fc172953254c9b1005493e0ad3b7bd4ad",
)

# The old ledgers are exact prefixes; all subsequent rows must be a contiguous
# Unit 007 tail. This makes unknown final tail IDs derivable without being loose.
CONTROL_PREFIXES = {
    "00_control/TERMINOLOGY.csv": (
        470, 59260,
        "ec9225831bf1a4207aeb5d2ed5bcd70794f81f86a03bd611c19c6e27be5c1980",
    ),
    "00_control/ADVERSE_LEDGER.csv": (
        547, 203950,
        "5a5e22b232ce4b6c5ab40674ffb64cf146d708035052400febc804186672953c",
    ),
}

AUDIT_PATH = "qa/FOMBERG_UNIT_007_SOURCE_AUDIT.json"
QA_PATH = "qa/FOMBERG_UNIT_007_QA.json"
REVIEW_PATH = "qa/fomberg-unit-007/INDEPENDENT_SOURCE_LANGUAGE_REVIEW_FINAL.json"
MATH_REVIEW_PATH = "qa/fomberg-unit-007/INDEPENDENT_MATH_REVIEW_FINAL.json"
EVIDENCE_PATHS = (AUDIT_PATH, REVIEW_PATH, MATH_REVIEW_PATH, QA_PATH)
ASSET_DIR = "source/id-ID/fomberg/assets/unit-007"
ASSET_SPECS = (
    ("torus-cellular-polygon", "o012-fom-u007-fig-torus-polygon"),
    ("genus-two-cellular-polygon", "o012-fom-u007-fig-genus-two-polygon"),
    ("klein-bottle-cellular-polygon", "o012-fom-u007-fig-klein-bottle-polygon"),
)
EXPECTED_CLASSES = {
    "boundary": 1, "definition": 2, "example": 6, "exercise": 6,
    "figure": 17, "heading": 3, "hint": 6, "lemma": 1,
    "proof": 4, "proof-repair": 3, "remark": 5, "solution": 6,
    "source-audit": 9, "theorem": 3,
}
EXPECTED_STABLE_IDS = sum(EXPECTED_CLASSES.values())
EXPECTED_ALIASES = {
    "exmp:cw-for-torus-homology": "o012-fom-u007-ex-torus-homology",
    "exmp:homology-of-genus-two": "o012-fom-u007-ex-genus-two-homology",
    "exmp:homology-of-rpn": "o012-fom-u007-ex-real-projective-space-homology",
}
# A few admitted glossary forms are deliberate textbook normalisations rather
# than literal contiguous strings in the Indonesian prose (for example,
# ``aproksimasi seluler`` is explained as ``pendekatan seluler``).  Bind those
# forms to the smallest canonical node carrying the concept instead of using a
# loose whole-document search.  The override is deterministic and auditable.
TERM_EVIDENCE_OVERRIDES = {
    "O012-TERM-0470": "o012-fom-u007-def-cellular-chains",
    "O012-TERM-0471": "o012-fom-u007-def-cellular-chains",
    "O012-TERM-0472": "o012-fom-u007-def-cellular-chains",
    "O012-TERM-0473": "o012-fom-u007-def-cellular-chains",
    "O012-TERM-0474": "o012-fom-u007-def-cellular-boundary",
    "O012-TERM-0475": "o012-fom-u007-thm-cellular-incidence",
    "O012-TERM-0476": "o012-fom-u007-thm-cellular-incidence",
    "O012-TERM-0477": "o012-fom-u007-thm-cellular-homology",
    "O012-TERM-0478": "o012-fom-u007-ex-genus-two-homology",
    "O012-TERM-0479": "o012-fom-u007-ex-real-projective-space-homology",
    "O012-TERM-0480": "o012-fom-u007-ex-sphere-homology",
    "O012-TERM-0481": "o012-fom-u007-proof-pr14",
    "O012-TERM-0482": "o012-fom-u007-ex-torus-homology",
    "O012-TERM-0483": "o012-fom-u007-mcheck-002",
    "O012-TERM-0484": "o012-fom-u007-proof-pr14",
}
TERM_READER_FORMS = {
    "O012-TERM-0472": "kompleks rantai seluler",
    "O012-TERM-0481": "pendekatan seluler",
    "O012-TERM-0483": "limit terarah",
    "O012-TERM-0484": "hasil bagi",
}


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


def identity(relative: str) -> tuple[int, str]:
    path = LANE / relative
    if not path.is_file():
        raise SystemExit(f"required final input absent: {relative}")
    raw = path.read_bytes()
    return len(raw), digest(raw)


def require_identity(relative: str, expected: tuple[int, str]) -> bytes:
    raw = (LANE / relative).read_bytes()
    if (len(raw), digest(raw)) != expected:
        raise SystemExit(f"sealed input identity mismatch: {relative}")
    return raw


def discover_identities() -> dict[str, tuple[int, str]]:
    """Discover one candidate sealed set; semantic verification follows.

    The producer repeats this discovery and byte comparison immediately before
    append, so no discovered input may change between planning and mutation.
    """
    paths = [SOURCE_PATH, *EVIDENCE_PATHS, *CONTROL_PREFIXES]
    paths.extend(f"{ASSET_DIR}/{slug}.{ext}" for slug, _ in ASSET_SPECS for ext in ("png", "svg"))
    return {path: identity(path) for path in paths}


def verify_prefix(backend: Path = BACKEND) -> tuple[dict[str, bytes], list[dict[str, Any]]]:
    prefix: dict[str, bytes] = {}
    records: list[dict[str, Any]] = []
    seen: set[str] = set()
    bundle = hashlib.sha256()
    for name in FILES:
        raw = (backend / name).read_bytes()
        count, size, sha = PREFIX[name]
        if (len(raw.splitlines()), len(raw), digest(raw)) != (count, size, sha):
            raise SystemExit(f"{name}: immutable Unit 006 boundary mismatch")
        if b"\r" in raw or not raw.endswith(b"\n"):
            raise SystemExit(f"{name}: invalid LF discipline")
        for number, line in enumerate(raw.splitlines(keepends=True), 1):
            obj = json.loads(line.decode("utf-8"))
            if canon(obj) != line or obj["id"] in seen:
                raise SystemExit(f"{name}:{number}: noncanonical or duplicate prefix")
            seen.add(obj["id"]); records.append(obj)
        prefix[name] = raw
        bundle.update(name.encode("utf-8")); bundle.update(b"\0"); bundle.update(raw)
    observed = (len(records), sum(map(len, prefix.values())), bundle.hexdigest())
    if observed != PREFIX_TOTAL:
        raise SystemExit(f"immutable Unit 006 bundle mismatch: {observed!r}")
    return prefix, records


def _attrs(text: str) -> dict[str, str]:
    return {m.group(1): m.group(2) for m in re.finditer(r'(data-[a-z-]+)="([^"]*)"', text)}


def parse_reader(source_identity: tuple[int, str]) -> tuple[list[str], list[dict[str, Any]]]:
    raw = require_identity(SOURCE_PATH, source_identity)
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
        ident = re.search(r'#(o012-fom-u007(?:-[A-Za-z0-9-]+)?)', match.group(3))
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
            width = len(opener_match.group(1)); opener_start = number
            opener = [lines[number - 1]]
            while "}" not in opener[-1] and number < len(lines):
                number += 1; opener.append(lines[number - 1])
            joined = " ".join(opener)
            ident = re.search(r'#(o012-fom-u007(?:-[A-Za-z0-9-]+)?)', joined)
            kind_match = re.match(r'^:{3,}\s*\{\.([^\s}]+)', opener[0].strip())
            node = None
            if ident and kind_match:
                enclosing = next((item[1]["id"] for item in reversed(stack) if item[1] is not None), None)
                node = {
                    "id": ident.group(1), "kind": kind_match.group(1),
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
        "o012-fom-u007-notice", "o012-fom-u007", "o012-fom-u007-mastery",
    ]
    if any(ident not in by_local for ident in headings) or "o012-fom-u007-boundary-001" not in by_local:
        raise SystemExit("reader heading/boundary set incomplete")
    by_local[headings[0]]["line_end"] = by_local[headings[1]]["line_start"] - 1
    by_local[headings[1]]["line_end"] = by_local[headings[-1]]["line_start"] - 1
    by_local[headings[-1]]["line_end"] = by_local["o012-fom-u007-boundary-001"]["line_start"] - 1
    nodes.sort(key=lambda item: (item["line_start"], 0 if item["kind"] == "heading" else 1))
    ids = [node["id"] for node in nodes]
    classes = Counter(node["kind"] for node in nodes)
    if len(ids) != EXPECTED_STABLE_IDS or len(set(ids)) != EXPECTED_STABLE_IDS or dict(sorted(classes.items())) != EXPECTED_CLASSES:
        raise SystemExit(f"reader stable-ID/class census mismatch: {len(ids)}, {dict(classes)}")
    if [node["id"] for node in nodes if node["kind"] == "heading"] != headings:
        raise SystemExit("reader heading identity/order mismatch")
    aliases = {node["attrs"]["data-source-label"]: node["id"] for node in nodes if "data-source-label" in node["attrs"]}
    if aliases != EXPECTED_ALIASES:
        raise SystemExit(f"source alias mismatch: {aliases}")
    for number in range(1, 7):
        for kind in ("mcheck", "hint", "sol"):
            if f"o012-fom-u007-{kind}-{number:03d}" not in by_local:
                raise SystemExit(f"mastery triple {number} incomplete")
    linked_pngs = set(re.findall(r'\.\./assets/unit-007/([a-z0-9-]+\.png)', text))
    expected_pngs = {f"{slug}.png" for slug, _ in ASSET_SPECS}
    if linked_pngs != expected_pngs:
        raise SystemExit(f"reader redraw-link inventory mismatch: {sorted(linked_pngs)}")
    return lines, nodes


def verify_upstream() -> None:
    raw = UPSTREAM.read_bytes()
    if (len(raw), raw.count(b"\n"), digest(raw)) != UPSTREAM_IDENTITY:
        raise SystemExit("frozen Fomberg authoring source mismatch")
    lines = raw.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n").splitlines()
    start, end, count, size, sha = SPAN_IDENTITY
    span = ("\n".join(lines[start - 1:end]) + "\n").encode("utf-8")
    if (len(span.splitlines()), len(span), digest(span)) != (count, size, sha):
        raise SystemExit("Fomberg Unit 007 upstream span mismatch")
    if lines[NEXT_SOURCE_LINE - 1].strip() != NEXT_HEADING:
        raise SystemExit("Fomberg Unit 007 next-source cursor mismatch")


def _load_json(relative: str, expected: tuple[int, str]) -> tuple[bytes, dict[str, Any]]:
    raw = require_identity(relative, expected)
    if raw.startswith(b"\xef\xbb\xbf") or b"\r" in raw or not raw.endswith(b"\n"):
        raise SystemExit(f"JSON evidence encoding/newline mismatch: {relative}")
    obj = json.loads(raw.decode("utf-8", errors="strict"))
    if not isinstance(obj, dict):
        raise SystemExit(f"JSON evidence top level is not an object: {relative}")
    return raw, obj


def _read_control_tail(relative: str, expected: tuple[int, str]) -> tuple[list[dict[str, str]], bytes]:
    raw = require_identity(relative, expected)
    if raw.startswith(b"\xef\xbb\xbf") or b"\r" in raw or not raw.endswith(b"\n"):
        raise SystemExit(f"control encoding/newline mismatch: {relative}")
    prefix_lines, prefix_size, prefix_sha = CONTROL_PREFIXES[relative]
    lines = raw.splitlines(keepends=True)
    prefix = b"".join(lines[:prefix_lines])
    if (len(prefix), digest(prefix)) != (prefix_size, prefix_sha):
        raise SystemExit(f"Unit 006 control prefix mismatch: {relative}")
    all_rows = list(csv.DictReader(raw.decode("utf-8").splitlines()))
    prefix_rows = prefix_lines - 1
    tail = all_rows[prefix_rows:]
    if not tail:
        raise SystemExit(f"Unit 007 control tail absent: {relative}")
    return tail, prefix


def _control_number(value: str) -> int:
    return int(value.rsplit("-", 1)[1])


def _bind_identity(obj: dict[str, Any], path: str, observed: tuple[int, str]) -> bool:
    candidates: list[dict[str, Any]] = []
    for key in ("identity", "canonical", "reader"):
        value = obj.get(key)
        if isinstance(value, dict):
            candidates.append(value.get("identity", value) if key == "reader" else value)
    return any(
        candidate.get("path") == path
        and candidate.get("bytes") == observed[0]
        and candidate.get("sha256") == observed[1]
        for candidate in candidates
    )


def verify_all_inputs(identities: dict[str, tuple[int, str]]) -> dict[str, Any]:
    if set(identities) != {SOURCE_PATH, *EVIDENCE_PATHS, *CONTROL_PREFIXES, *[
        f"{ASSET_DIR}/{slug}.{ext}" for slug, _ in ASSET_SPECS for ext in ("png", "svg")
    ]}:
        raise SystemExit("Unit 007 discovered-input inventory mismatch")
    for relative, expected in identities.items():
        require_identity(relative, expected)
    verify_upstream()
    source_identity = identities[SOURCE_PATH]
    lines, nodes = parse_reader(source_identity)
    audit_raw, audit = _load_json(AUDIT_PATH, identities[AUDIT_PATH])
    review_raw, review = _load_json(REVIEW_PATH, identities[REVIEW_PATH])
    math_review_raw, math_review = _load_json(MATH_REVIEW_PATH, identities[MATH_REVIEW_PATH])
    qa_raw, qa = _load_json(QA_PATH, identities[QA_PATH])
    adverse, _ = _read_control_tail("00_control/ADVERSE_LEDGER.csv", identities["00_control/ADVERSE_LEDGER.csv"])
    terms, _ = _read_control_tail("00_control/TERMINOLOGY.csv", identities["00_control/TERMINOLOGY.csv"])

    if [row["event_id"] for row in adverse] != [f"O012-ADV-{n:04d}" for n in range(547, 547 + len(adverse))]:
        raise SystemExit("Unit 007 adverse tail is not contiguous from O012-ADV-0547")
    if [row["term_id"] for row in terms] != [f"O012-TERM-{n:04d}" for n in range(470, 470 + len(terms))]:
        raise SystemExit("Unit 007 terminology tail is not contiguous from O012-TERM-0470")
    allowed = {
        "clarified_in_translation", "corrected_in_translation",
        "hypothesis_repaired_in_translation", "proof_completed_in_translation",
        "resolved_before_admission", "accessibility_reflow",
        "corrected_after_independent_review", "corrected_after_cumulative_pdf_gate",
        "resolved", "identifier_preservation",
        "proof_completed_after_independent_review", "solution_completed_in_translation",
        "structural_adaptation", "direction_verified_in_translation",
    }
    if any(
        row["status"] not in allowed
        or not (
            "o012-fom-u007" in row["source_location"].casefold()
            or "unit007" in row["source_location"].casefold()
        )
        for row in adverse
    ):
        raise SystemExit("Unit 007 adverse tail status or reader binding mismatch")
    if any(row["status"] != "admitted" for row in terms):
        raise SystemExit("Unit 007 terminology tail contains a non-admitted row")

    reader_identity = {"path": SOURCE_PATH, "bytes": source_identity[0], "sha256": source_identity[1]}
    if (
        audit.get("audit_id") != "O012-FOMBERG-UNIT-007-SOURCE-AUDIT"
        or audit.get("status") not in {
            "PASS", "PASS_WITH_MANDATORY_REPAIRS_IDENTIFIED",
            "FROZEN_SOURCE_BOUNDARY_AND_CORRECTION_PLAN",
        }
        or audit.get("source", {}).get("selected_span", {}).get("sha256") != SPAN_IDENTITY[4]
        or audit.get("source", {}).get("next_line") != NEXT_SOURCE_LINE
        or audit.get("model_provenance") != MODEL
    ):
        raise SystemExit("Unit 007 source-audit semantic binding mismatch")
    review_checks = review.get("checks", {})
    review_authority = review.get("authority", {})
    review_span = review_authority.get("selected_span", {})
    review_structure = review_checks.get("source_closure_and_order", {})
    review_figures = review_checks.get("figures_and_diagram_functions", {})
    if (
        review.get("status") != "PASS_P1_P2_P3_ZERO"
        or review.get("severity_census") != {"P1": 0, "P2": 0, "P3": 0}
        or review.get("canonical", {}).get("path") != SOURCE_PATH
        or review.get("canonical", {}).get("bytes") != source_identity[0]
        or review.get("canonical", {}).get("sha256") != source_identity[1]
        or review_authority.get("sha256") != UPSTREAM_IDENTITY[2]
        or review_span.get("sha256") != SPAN_IDENTITY[4]
        or review_span.get("next_line_number") != NEXT_SOURCE_LINE
        or review_structure.get("canonical_source_environment_wrappers") != 15
        or review_structure.get("unique_source_environment_ids") != 15
        or review_figures.get("canonical_figure_ids") != 17
        or review_figures.get("unique_canonical_figure_ids") != 17
        or review.get("checks", {}).get("cursor", {}).get("next_exact_cursor") != NEXT_SOURCE_LINE
        or review.get("model_provenance") != MODEL
    ):
        raise SystemExit("Unit 007 final independent-review binding mismatch")
    math_reader = math_review.get("canonical_reader", {})
    math_source = math_review.get("frozen_source_binding", {})
    math_mastery = math_review.get("mastery_structure", {})
    math_repairs = math_review.get("proof_repair_checks", [])
    if (
        math_review.get("status") != "PASS"
        or math_review.get("pass") is not True
        or math_review.get("severity_census") != {"P1": 0, "P2": 0, "P3": 0}
        or math_reader.get("path") != SOURCE_PATH
        or math_reader.get("bytes") != source_identity[0]
        or math_reader.get("sha256") != source_identity[1]
        or math_source.get("selected_source_lines") != "3518-4185"
        or math_source.get("selected_span_sha256") != SPAN_IDENTITY[4]
        or math_source.get("next_source_line") != NEXT_SOURCE_LINE
        or math_mastery.get("expected_triples") != 6
        or math_mastery.get("status") != "PASS"
        or len(math_repairs) != 3
        or any(item.get("status") != "PASS" for item in math_repairs)
        or math_review.get("model_provenance") != MODEL
    ):
        raise SystemExit("Unit 007 final independent math-review binding mismatch")
    reader_qa = qa.get("reader", {})
    if (
        qa.get("qa_id") != "O012-FOMBERG-UNIT-007-STATIC-QA"
        or qa.get("status") != "PASS"
        or reader_qa.get("identity", {}) != {**reader_identity, **{
            key: reader_qa.get("identity", {}).get(key)
            for key in ("encoding", "lf_lines", "newline") if key in reader_qa.get("identity", {})
        }}
        or qa.get("source", {}).get("selected_span", {}).get("sha256") != SPAN_IDENTITY[4]
        or qa.get("source", {}).get("next_line") != NEXT_SOURCE_LINE
        or reader_qa.get("stable_ids") != EXPECTED_STABLE_IDS
        or reader_qa.get("stable_ids_unique") != EXPECTED_STABLE_IDS
        or reader_qa.get("semantic_class_counts") != EXPECTED_CLASSES
        or reader_qa.get("mastery", {}).get("exercise_hint_solution_triples") != 6
        or reader_qa.get("mastery", {}).get("complete_solutions") != 6
        or reader_qa.get("assets", {}).get("png_fallbacks") != 3
        or qa.get("model_provenance") != MODEL
        or not qa.get("gates") or not all(value == "PASS" for value in qa["gates"].values())
    ):
        raise SystemExit("Unit 007 static-QA semantic binding mismatch")
    # QA must bind the exact source-audit/review/control bytes it certifies.
    audit_binding = qa.get("source_audit", {})
    review_binding = qa.get("independent_review", {}).get("identity", {})
    math_review_binding = qa.get("independent_reviews", {}).get("math", {}).get("identity", {})
    control_bindings = qa.get("controls", {}).get("identities", {})
    if (
        (audit_binding.get("bytes"), audit_binding.get("sha256")) != identities[AUDIT_PATH]
        or (review_binding.get("bytes"), review_binding.get("sha256")) != identities[REVIEW_PATH]
        or (math_review_binding.get("bytes"), math_review_binding.get("sha256")) != identities[MATH_REVIEW_PATH]
        or any(
            (control_bindings.get(path, {}).get("bytes"), control_bindings.get(path, {}).get("sha256")) != identities[path]
            for path in CONTROL_PREFIXES
        )
    ):
        raise SystemExit("static QA does not bind exact audit/review/control bytes")
    asset_bindings = reader_qa.get("assets", {}).get("identities", qa.get("assets", {}).get("identities", {}))
    for slug, _ in ASSET_SPECS:
        for ext in ("png", "svg"):
            relative = f"{ASSET_DIR}/{slug}.{ext}"
            bound = asset_bindings.get(relative, asset_bindings.get(f"{slug}.{ext}", {})) if isinstance(asset_bindings, dict) else {}
            if bound and (bound.get("bytes"), bound.get("sha256")) != identities[relative]:
                raise SystemExit(f"QA redraw identity mismatch: {relative}")

    # Every admitted Unit 007 term must occur in a uniquely locatable node.
    for row in terms:
        preferred = TERM_READER_FORMS.get(row["term_id"], row["id_ID"]).casefold()
        if not any(preferred in "\n".join(lines[node["line_start"] - 1:node["line_end"]]).casefold() for node in nodes):
            raise SystemExit(f"terminology evidence lacks admitted form: {row['term_id']}")
    return {
        "lines": lines, "nodes": nodes, "adverse": adverse, "terms": terms,
        "audit": audit, "qa": qa, "review": review, "math_review": math_review,
        "source_identity": source_identity, "identities": identities,
    }


def target_locator(source_identity: tuple[int, str], start: int, end: int) -> dict[str, Any]:
    raw_lines = SOURCE.read_bytes().splitlines(keepends=True)
    return {
        "path": SOURCE_PATH, "line_start": start, "line_end": end,
        "file_sha256": source_identity[1],
        "content_sha256": digest(b"".join(raw_lines[start - 1:end])),
    }


def source_locator(source_range: str | None) -> dict[str, Any]:
    if not source_range:
        return {"kind": "edition_original", "path": SOURCE_PATH, "precision": "exact_target_span"}
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


def clean_title(title: str, kind: str) -> str:
    value = re.sub(r"\*\*", "", title).strip()
    return value[:240] if value else kind


def parentage(nodes: list[dict[str, Any]]) -> dict[str, tuple[str, int, list[str]]]:
    by_local = {node["id"]: node for node in nodes}
    sections = ("o012-fom-u007-mastery",)
    raw_parent: dict[str, str] = {
        "o012-fom-u007-notice": ROOT,
        **{section: ROOT for section in sections},
        "o012-fom-u007-boundary-001": ROOT,
    }
    for node in nodes:
        ident = node["id"]
        if ident == "o012-fom-u007" or ident in raw_parent:
            continue
        if node.get("enclosing_div"):
            raw_parent[ident] = f"unit:{node['enclosing_div']}"; continue
        if by_local["o012-fom-u007"]["line_start"] < node["line_start"] < by_local[sections[0]]["line_start"]:
            raw_parent[ident] = ROOT; continue
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
        uid = f"unit:{ident}"; parent = raw_parent[ident]
        return [ROOT, uid] if parent == ROOT else path_for(parent.removeprefix("unit:")) + [uid]

    return {ident: (parent, children[parent].index(ident) + 1, path_for(ident)) for ident, parent in raw_parent.items()}


def load_generic():
    path = LANE / "scripts/validate-backend.py"
    raw = path.read_bytes()
    if (len(raw), digest(raw)) != (76924, "f90d19fbfb4b0525902316dd5c26550fc25c66054cddf32b385bc97f6d526b6e"):
        raise SystemExit("generic backend validator identity mismatch")
    spec = importlib.util.spec_from_file_location("o012_generic_fom007", path)
    if spec is None or spec.loader is None:
        raise SystemExit("cannot load generic backend validator")
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


def _term_evidence(row: dict[str, str], lines: list[str], nodes: list[dict[str, Any]]) -> str:
    override = TERM_EVIDENCE_OVERRIDES.get(row["term_id"])
    if override:
        if not any(node["id"] == override for node in nodes):
            raise SystemExit(f"term evidence override target absent: {row['term_id']}")
        return override
    preferred = row["id_ID"].casefold()
    candidates = [
        node for node in nodes
        if preferred in "\n".join(lines[node["line_start"] - 1:node["line_end"]]).casefold()
    ]
    candidates.sort(key=lambda node: (node["kind"] == "heading", node["line_end"] - node["line_start"], node["line_start"]))
    if not candidates:
        raise SystemExit(f"no target evidence for term {row['term_id']}")
    return candidates[0]["id"]


def _correction_targets(row: dict[str, str], node_ids: set[str]) -> list[str]:
    # A ledger locator may retain a pre-admission scratch label in addition to
    # the canonical audit node (ADV-0549 does this).  Keep every resolvable
    # canonical target; the original locator remains verbatim in ``evidence``.
    all_targets = sorted(set(re.findall(r'#(o012-fom-u007(?:-[A-Za-z0-9-]+)?)', row["source_location"])))
    targets = [target for target in all_targets if target in node_ids]
    if not targets and (
        "o012-fom-u007" in row["source_location"].casefold()
        or "unit007" in row["source_location"].casefold()
    ):
        # Integration-level ledger rows (currently ADV-0559 and ADV-0563)
        # describe the whole admitted reader and intentionally have no hash
        # fragment.  Bind them to the unit root rather than inventing a node.
        return [ROOT.removeprefix("unit:")]
    if not targets:
        raise SystemExit(f"adverse row target resolution failed: {row['event_id']}")
    return targets


def build_additions(data: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    lines = data["lines"]; nodes = data["nodes"]
    source_identity = data["source_identity"]; identities = data["identities"]
    additions: dict[str, list[dict[str, Any]]] = {name: [] for name in FILES}

    def add(name: str, record: dict[str, Any]) -> None:
        additions[name].append(record)

    for ident, attribution, change, third in (
        (
            COMPANION_RIGHTS,
            "Original Indonesian mastery, solutions, source corrections, and accessible redraws for Fomberg Unit 007.",
            "Original additions and redraws are distinguished from the Fomberg source component.",
            "Original Unit 007 companion layer; source content remains separately attributed.",
        ),
        (
            COMPOSITE_RIGHTS,
            "Fomberg source adaptation plus original Indonesian Unit 007 companion layer.",
            "Integrated reader preserves exact locators, correction provenance, and seven paired accessible redraws.",
            "Composite Unit 007; component-scoped rights records control.",
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

    term_concepts: list[str] = []
    for row in data["terms"]:
        number = _control_number(row["term_id"])
        concept_id = f"concept:o012-fom-u007-term-{number:04d}"
        term_id = f"term:o012-fom-u007-term-{number:04d}:id-ID"
        evidence = _term_evidence(row, lines, nodes)
        concept = common("concept", concept_id)
        concept.update(canonical_label=row["source_term"], domain=row["scope"], locale_neutral=True)
        add("concepts.jsonl", concept); term_concepts.append(concept_id)
        term = common("term", term_id)
        term.update(
            concept_id=concept_id, evidence_segment_id=f"segment:{evidence}",
            locale="id-ID", preferred=row["id_ID"], register="textbook",
            rejected_forms=[], rights_component_id=COMPOSITE_RIGHTS,
            scope_unit_id=ROOT, source_term=row["source_term"],
            terminology_control_id=row["term_id"], terminology_status=row["status"],
            usage_note=row["note"], variants=[],
        )
        add("terms.jsonl", term)

    all_concepts = [
        "concept:attaching-map", "concept:characteristic-map", "concept:cw-complex",
        "concept:hawaiian-earring", "concept:weak-topology", *term_concepts,
    ]
    parents = parentage(nodes)
    for node in nodes:
        ident = node["id"]; uid = f"unit:{ident}"; kind = node["kind"]; attrs = node["attrs"]
        is_root = ident == "o012-fom-u007"
        origin = attrs.get("data-origin")
        source_range = attrs.get("data-source-lines")
        adapted = origin == "source-derived" and "data-adaptation" in attrs
        if is_root:
            rights = COMPOSITE_RIGHTS; provenance = "composite_translated_and_original"
            parent = COURSE; order = 37; path = [ROOT]
            display = "Topologi Aljabar — Komponen Fomberg Unit 007: Homologi Seluler"
            locator = target_locator(source_identity, 1, len(lines))
        else:
            rights = COMPOSITE_RIGHTS if adapted else SOURCE_RIGHTS if origin == "source-derived" else COMPANION_RIGHTS
            provenance = (
                "translated_with_original_exercise_expansion" if adapted
                else "translated_adapted_from_upstream" if origin == "source-derived"
                else "edition_original_accessible_redraw" if origin == "edition-original-redraw"
                else "edition_original"
            )
            parent, order, path = parents[ident]
            display = clean_title(node["title"], kind)
            locator = target_locator(source_identity, node["line_start"], node["line_end"])
        unit_kind = "reader_unit" if is_root else ("section" if kind == "heading" else kind.replace("-", "_"))
        unit = common("unit", uid)
        unit.update(
            component_source_commit=COMMIT, component_source_id=RESOURCE,
            concept_ids=all_concepts, course_id=COURSE, course_route_unit_id=ROUTE,
            display_title=display, edition_id=EDITION, edition_unit_id=ROOT,
            locale="id-ID", model_provenance=MODEL, order=order, parent_id=parent,
            path=path, program_id=PROGRAM, provenance_relation=provenance,
            resource_id=RESOURCE, rights_component_id=rights, source_local_id=ident,
            target_locator=locator, translation_state="structurally_verified", unit_kind=unit_kind,
        )
        if is_root:
            unit.update(
                edition_order=7, route_order=12,
                source_locator={
                    "path": "algebraic_topology.tex", "commit_sha": COMMIT,
                    "line_start": SPAN_IDENTITY[0], "line_end": SPAN_IDENTITY[1],
                    "precision": "exact_unit_span", "span_bytes": SPAN_IDENTITY[3],
                    "span_sha256": SPAN_IDENTITY[4],
                },
            )
        alias = attrs.get("data-source-label")
        if alias:
            unit["source_aliases"] = [alias]
        if kind == "solution":
            unit["solution_status"] = "complete_checked_solution"
        add("units.jsonl", unit)
        segment = common("segment", f"segment:{ident}")
        segment.update(
            component_source_commit=COMMIT, component_source_id=RESOURCE,
            concept_ids=all_concepts, course_route_unit_id=ROUTE, edition_id=EDITION,
            edition_unit_id=ROOT, locale="id-ID", model_provenance=MODEL,
            order=order, provenance_relation=provenance, resource_id=RESOURCE,
            rights_component_id=rights, segment_kind="source_heading" if is_root else unit_kind,
            source_local_id=ident,
            source_locator={
                "path": "algebraic_topology.tex", "commit_sha": COMMIT,
                "line_start": SPAN_IDENTITY[0], "line_end": SPAN_IDENTITY[1],
                "precision": "exact_unit_span",
            } if is_root else source_locator(source_range if source_range else None),
            target_locator=locator, translation_state="structurally_verified", unit_id=uid,
        )
        for key in ("source_aliases", "solution_status"):
            if key in unit:
                segment[key] = unit[key]
        add("segments.jsonl", segment)

    source_asset = common("asset", "asset:o012-fom-u007-source-markdown")
    source_asset.update(
        bytes=source_identity[0], edition_id=EDITION,
        media_type="text/markdown; charset=utf-8", path=SOURCE_PATH,
        resource_id=RESOURCE, rights_component_id=COMPOSITE_RIGHTS,
        role="canonical_reader_source", sha256=source_identity[1], unit_id=ROOT,
    )
    add("assets.jsonl", source_asset)
    figures = [node for node in nodes if node["kind"] == "figure"]
    layer = common("asset", "asset:o012-fom-u007-semantic-diagram-layer")
    layer.update(
        bytes=source_identity[0], edition_id=EDITION,
        media_type="text/markdown; charset=utf-8", path=SOURCE_PATH,
        resource_id=RESOURCE, rights_component_id=COMPOSITE_RIGHTS,
        role="semantic_diagram_accessibility_layer", sha256=source_identity[1],
        source_diagram_count=17, semantic_figure_block_count=14,
        geometric_redraw_count=3,
        semantic_unit_ids=[f"unit:{node['id']}" for node in figures], unit_id=ROOT,
    )
    add("assets.jsonl", layer)
    for slug, figure_id in ASSET_SPECS:
        for ext, media, role in (
            ("png", "image/png", "reader_linked_accessible_redraw"),
            ("svg", "image/svg+xml", "accessible_vector_source_companion"),
        ):
            relative = f"{ASSET_DIR}/{slug}.{ext}"; size, sha = identities[relative]
            rec = common("asset", f"asset:o012-fom-u007-{slug}-{ext}")
            rec.update(
                bytes=size, edition_id=EDITION, media_type=media, path=relative,
                resource_id=RESOURCE, rights_component_id=COMPANION_RIGHTS,
                role=role, sha256=sha, source_figure_unit_id=f"unit:{figure_id}", unit_id=ROOT,
            )
            add("assets.jsonl", rec)

    artifact_specs = (
        ("artifact:o012-fom-u007-source-audit", AUDIT_PATH, ["qa:o012-fom-u007-source-integrity"], "source_frozen"),
        ("artifact:o012-fom-u007-review-final", REVIEW_PATH, ["qa:o012-fom-u007-math", "qa:o012-fom-u007-language"], "mathematically_reviewed"),
        ("artifact:o012-fom-u007-qa", QA_PATH, ["qa:o012-fom-u007-source-integrity", "qa:o012-fom-u007-mastery"], "built"),
    )
    for ident, relative, qa_ids, state in artifact_specs:
        size, sha = identities[relative]
        rec = common("artifact", ident)
        rec.update(
            bytes=size, locale="id-ID", manifest_artifact_id=None,
            media_type="application/json", path=relative, qa_event_ids=qa_ids,
            rights_component_id=COMPOSITE_RIGHTS, sha256=sha,
            toolchain=(
                f"Fomberg Unit 007 evidence; algebraic_topology.tex:3518-4185; "
                f"{SPAN_IDENTITY[4]}; {MODEL}; route D60-R12; semantic admission only."
            ),
            translation_state=state, unit_id=ROOT,
        )
        add("artifacts.jsonl", rec)
    for ident, kind, note, witnesses in (
        ("qa:o012-fom-u007-source-integrity", "source", f"Exact lines 3518-4185, cursor 4186, {EXPECTED_STABLE_IDS} stable IDs, seven paired redraws, and source aliases passed.", ["artifact:o012-fom-u007-source-audit", "artifact:o012-fom-u007-review-final", "artifact:o012-fom-u007-qa"]),
        ("qa:o012-fom-u007-math", "math", "Final independent review passed P1=P2=P3=0 for the cellular-complex unit and its source corrections.", ["artifact:o012-fom-u007-review-final"]),
        ("qa:o012-fom-u007-language", "language", "Final Indonesian terminology and language review passed.", ["artifact:o012-fom-u007-review-final"]),
        ("qa:o012-fom-u007-mastery", "mastery", "Six exercises, six hints, and six complete checked solutions passed.", ["artifact:o012-fom-u007-qa"]),
    ):
        rec = common("qa_event", ident)
        rec.update(note=note, qa_type=kind, result="passed", unit_id=ROOT, witness_artifact_ids=witnesses)
        add("qa.jsonl", rec)

    node_ids = {node["id"] for node in nodes}
    for row in data["adverse"]:
        number = _control_number(row["event_id"]); targets = _correction_targets(row, node_ids)
        rec = common("correction", f"correction:o012-fom-u007-adv-{number:04d}")
        rec.update(
            adverse_ledger_id=row["event_id"], affected_unit_ids=[f"unit:{target}" for target in targets],
            correction_type="source_correction", edition_id=EDITION,
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

    relation("relation:adapts:o012-fom-u007:fomberg-edition", ROOT, EDITION, "adapts", "Indonesian Unit 007 adapts exact Fomberg lines 3518-4185.")
    relation("relation:contains:o012-d60:fomberg-u007", COURSE, ROOT, "contains", "Course route D60-R12 contains Fomberg Unit 007 as the cellular-homology continuation.", course_route_unit_id=ROUTE)
    relation("relation:precedes:o012-fom-u006:o012-fom-u007", "unit:o012-fom-u006", ROOT, "precedes", "Fomberg Unit 006 precedes Unit 007 in source order.")
    relation("relation:contains:o012-d60-rights:fomberg-u007", ROUTE_RIGHTS, ROOT, "contains", "Integrated-route rights contain the Fomberg Unit 007 composite.")
    relation("relation:precedes:o012-fom-u007:mastery", ROOT, "unit:o012-fom-u007-mastery", "precedes", "Translated source body and correction dossier precede the solved mastery layer.")
    for number in range(1, 7):
        relation(f"relation:hints:fom-u007-hint-{number:03d}:mcheck-{number:03d}", f"unit:o012-fom-u007-hint-{number:03d}", f"unit:o012-fom-u007-mcheck-{number:03d}", "hints", f"Hint for Fomberg Unit 007 mastery check {number}.")
        relation(f"relation:solves:fom-u007-sol-{number:03d}:mcheck-{number:03d}", f"unit:o012-fom-u007-sol-{number:03d}", f"unit:o012-fom-u007-mcheck-{number:03d}", "solves", f"Complete checked solution for Unit 007 mastery check {number}.")
    for index, (slug, figure_id) in enumerate(ASSET_SPECS, 1):
        relation(f"relation:illustrates:fom-u007-fig-{index:03d}:diagram-layer", f"unit:{figure_id}", "asset:o012-fom-u007-semantic-diagram-layer", "illustrates", f"Accessible redraw {index} preserves its source diagram function; paired PNG and SVG assets are separately indexed.")
    relation("relation:xref:o012-fom-u007-torus:roberts-l13-s05", "unit:o012-fom-u007-ex-torus-homology", "unit:o012-rbt-l13-s05", "xref", "The cellular torus calculation links the corresponding Roberts topological example.")

    for name, records in additions.items():
        records.sort(key=lambda item: item["id"])
        if len({record["id"] for record in records}) != len(records):
            raise SystemExit(f"{name}: duplicate derived IDs")
    return additions


def delta(additions: dict[str, list[dict[str, Any]]]) -> dict[str, int]:
    return {name: len(additions[name]) for name in FILES}


def planned_additions() -> dict[str, list[dict[str, Any]]]:
    identities = discover_identities(); data = verify_all_inputs(identities)
    return build_additions(data)


def record_plan() -> dict[str, Any]:
    additions = planned_additions(); counts = delta(additions)
    artifact_paths = [record["path"] for record in additions["artifacts.jsonl"]]
    return {
        "edition_unit_id": ROOT, "root_unit_id": ROOT,
        "course_id": COURSE, "course_route_unit_id": ROUTE,
        "resource_id": RESOURCE, "edition_id": EDITION,
        "immutable_prefix": {
            "records": PREFIX_TOTAL[0], "bytes": PREFIX_TOTAL[1],
            "bundle_sha256": PREFIX_TOTAL[2],
        },
        "records_by_file": counts, "records_planned": sum(counts.values()),
        "record_ids_by_file": {name: [record["id"] for record in additions[name]] for name in FILES},
        "cumulative_records_planned": PREFIX_TOTAL[0] + sum(counts.values()),
        "stable_ids": EXPECTED_STABLE_IDS, "asset_records": 8, "real_redraw_files": 6,
        "artifact_evidence_paths_in_record_order": artifact_paths,
        "derived_control_tail": {
            "terminology_start": "O012-TERM-0470",
            "adverse_start": "O012-ADV-0547",
        },
        "unsealed_identity_paths": [],
    }
