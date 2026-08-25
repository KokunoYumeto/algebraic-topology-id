#!/usr/bin/env python3
"""Frozen inputs and deterministic backend records for Fomberg Unit 004.

The module is deliberately fail closed.  The reader, upstream span, reviews,
and redraws are frozen below.  The final source-audit, static-QA, terminology
ledger, and adverse ledger identities remain explicit ``None`` placeholders
until those files are sealed.  The append producer refuses to write while any
placeholder remains.
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

SOURCE_PATH = (
    "source/id-ID/fomberg/units/"
    "fomberg-unit-004-excision-mayer-vietoris-naturality-comparison.md"
)
SOURCE = LANE / SOURCE_PATH
SOURCE_IDENTITY = (
    87293,
    2364,
    "2c04d647b58afe044f5549bcba9ad3572075775711bb3aaec45d0e94fe3d3e91",
)
UPSTREAM_PATH = (
    "authority/upstream/math-notes-563194fae879178b9a6871b249513bfc27968975/"
    "tree/algebraic_topology.tex"
)
UPSTREAM = LANE / UPSTREAM_PATH
UPSTREAM_IDENTITY = (
    223886,
    6069,
    "d27095de0f38f0c14b2d7716cb52d51d064f0594dd9f82f9d1b3e6af5b35a483",
)
SPAN_IDENTITY = (
    1923,
    2846,
    924,
    38503,
    "ddde995b54154623ccc565117aee63cce8361d2ada1c3c9f2852775b1aaac638",
)
NEXT_SOURCE_LINE = 2847
NEXT_HEADING = r"\subsection{Degree maps}"
COMMIT = "563194fae879178b9a6871b249513bfc27968975"
TREE = "fb678966d1533d529bdd72f49d8496a3bdc14a9b"
RESOURCE = "resource:fomberg-algebraic-topology-2025"
EDITION = "edition:fomberg-at-2025-563194f"
ROOT = "unit:o012-fom-u004"
PROGRAM = "program:o012-id"
COURSE = "course:o012-d60"
ROUTE = "D60-R11"

SOURCE_RIGHTS = "rights:fomberg-cc-by-sa-4.0"
COMPANION_RIGHTS = "rights:o012-fom-u004-companion-cc-by-sa-4.0"
COMPOSITE_RIGHTS = "rights:o012-fom-u004-composite-cc-by-sa-4.0"
ROUTE_RIGHTS = "rights:o012-d60-integrated-route-cc-by-sa-4.0"

# The exact live Unit 003 boundary.  Every byte must remain unchanged.
PREFIX = {
    "artifacts.jsonl": (177, 143337, "6452e6190d2505913d546a1b956b1acebcafdc45af3e535840b02fd323cd426f"),
    "assets.jsonl": (53, 37270, "03091c88d8276bf834e9a39aefccf6c68e285e5747f77027f4e4598f2e322d0e"),
    "authority.jsonl": (6, 4374, "84c622f56dbbd5ba379361245ecfe07bc79c9f4fd6b18ba21b82b5f545211869"),
    "concepts.jsonl": (414, 130574, "ee995d610ddc86d3b61a436be851b1063055a1dcb4b0f75eaad136a2705a710d"),
    "corrections.jsonl": (498, 499984, "6bc8c0a3e49f943aaa9fd4ce060da4b9247458c9ad329bd51ef25343bd64341c"),
    "qa.jsonl": (146, 81358, "be3b1a0ad285ba7d3ab8ded44caffcd935da859117e0d9eabc062b6b7e18cf88"),
    "relations.jsonl": (655, 272700, "72db0a89c3b09bae0559af3189b35cd51062600f160e1ac37f72173cf845f9ce"),
    "rights.jsonl": (95, 86669, "68d7a7a5bfebad6414a6a6b7761aca29d3f28498b0a6b4457e660915123d5880"),
    "segments.jsonl": (1633, 2494755, "dce882c74e5ff52fd9a94a5a034b2aa0f90d2b7e7f407ee80cff08a48161e4a9"),
    "terms.jsonl": (407, 262803, "bada6c6904eedfdbd5f215ea2d88e68dc326ea1aa5ac41e2cf33e739d0c47594"),
    "units.jsonl": (1663, 2635662, "15b9062f5b5e943ec85e724ab8b189318052bf1c1f51dff357ae0dcf4831b3ab"),
}
PREFIX_TOTAL = (
    5747,
    6649486,
    "9e416c70e69dea1601bd79a259c278a9cfdfe5dca10d40b7bbc8e67d9ffba76b",
)

EXPECTED_CLASSES = {
    "boundary": 1,
    "corollary": 1,
    "definition": 3,
    "example": 2,
    "exercise": 7,
    "figure": 19,
    "heading": 7,
    "hint": 7,
    "lemma": 2,
    "proof": 14,
    "proof-supplement": 3,
    "proposition": 4,
    "remark": 10,
    "solution": 7,
    "source-audit": 17,
    "source-omission": 8,
    "theorem": 5,
}

# 117 units + 117 segments; 24 corrections; 19 terms/concepts; three frozen
# evidence artifacts; eight assets (reader, semantic layer, three PNG/SVG
# pairs); four QA events; two rights rows; and 53 semantic relations.
DELTA = {
    "artifacts.jsonl": 3,
    "assets.jsonl": 8,
    "authority.jsonl": 0,
    "concepts.jsonl": 19,
    "corrections.jsonl": 24,
    "qa.jsonl": 4,
    "relations.jsonl": 53,
    "rights.jsonl": 2,
    "segments.jsonl": 117,
    "terms.jsonl": 19,
    "units.jsonl": 117,
}

AUDIT_PATH = "qa/FOMBERG_UNIT_004_SOURCE_AUDIT.json"
QA_PATH = "qa/FOMBERG_UNIT_004_QA.json"
REVIEW_PATH = "qa/fomberg-unit-004/INDEPENDENT_REVIEW_FINAL.json"
EVIDENCE_PATHS = (
    AUDIT_PATH,
    REVIEW_PATH,
    QA_PATH,
)

# Replace only the four None values after the corresponding files are final.
# Tuple values are (bytes, sha256).  The producer refuses to append otherwise.
SEALED_IDENTITIES: dict[str, tuple[int, str] | None] = {
    AUDIT_PATH: (
        4154,
        "55b065d20fbc2d449c68afa99a062d7afb6039496c2a2befe1665332b5c4c6ac",
    ),
    REVIEW_PATH: (
        2524,
        "3c43a86f24adcb042b0ccc43d2e5031478ba622acd8925eca92721cf2cd5d102",
    ),
    QA_PATH: (
        7910,
        "d4c86d7efbd9837330c4e24121d5dbd49252c11f1c29daa77e13e64bc3ff0c21",
    ),
    "00_control/TERMINOLOGY.csv": (
        53356,
        "cf974537fd20758cbe5bdfba7561c81df8db0ec34de3d2b61f4347d02093c9e7",
    ),
    "00_control/ADVERSE_LEDGER.csv": (
        184841,
        "c2ae75371712f74541f3a96539ec601e40fee6d788dbb22989c99cf49d85d83f",
    ),
}

ALIASES = {
    "cor:cor": "o012-fom-u004-cor-good-pair-quotient",
    "thm:reduced-and-relative-homologies": "o012-fom-u004-thm-relative-quotient",
    "thm:invariance-of-dimension": "o012-fom-u004-thm-invariance-dimension",
    "prop:sing-simp": "o012-fom-u004-prop-sing-simp",
    "lem:five-lemma": "o012-fom-u004-lem-five",
    "lem:sing-simp": "o012-fom-u004-lem-compact-finite-simplices",
}

TERM_SPECS = (
    ("u-small-singular-simplex", "O012-TERM-0416", "def-u-chains"),
    ("u-chain", "O012-TERM-0417", "def-u-chains"),
    ("small-chain-theorem", "O012-TERM-0418", "prop-small-chains"),
    ("barycenter", "O012-TERM-0419", "proof-pr05a"),
    ("diameter", "O012-TERM-0420", "proof-pr05a"),
    ("subdivision-operator", "O012-TERM-0421", "proof-pr05b"),
    ("acyclic-chain-complex", "O012-TERM-0422", "proof-pr05b"),
    ("contracting-homotopy", "O012-TERM-0423", "proof-pr05b"),
    ("relative-homology-quotient-theorem", "O012-TERM-0424", "thm-relative-quotient"),
    ("invariance-of-dimension", "O012-TERM-0425", "thm-invariance-dimension"),
    ("local-homology", "O012-TERM-0426", "rem-local-homology"),
    ("reduced-homology-of-a-wedge-sum", "O012-TERM-0427", "prop-wedge-homology"),
    ("mobius-band", "O012-TERM-0428", "ex-rp2-mayer-vietoris"),
    ("simplicial-singular-homology-comparison", "O012-TERM-0429", "prop-sing-simp"),
    ("open-simplex", "O012-TERM-0430", "proof-compact-finite-simplices-source"),
    ("closed-simplex", "O012-TERM-0431", "proof-compact-finite-simplices-repair"),
    ("support-of-a-chain", "O012-TERM-0432", "proof-injectivity-comparison-repair"),
    ("finite-dimensional-complex", "O012-TERM-0433", "proof-sing-simp-finite"),
    ("comparison-map", "O012-TERM-0434", "omission-pr10"),
)

ASSET_SPECS = (
    ("excision-equivalence.png", 139672, "8d4e0aa9ffe93edbe3d3eb3def640ace8d2ffbcc45044cd5dcd3a1de1124b650", "image/png", "fig-excision-equivalence"),
    ("excision-equivalence.svg", 3613, "e69df6490440c5c81416fe0c713d160e91d01216c944bb146aba94540234c3ad", "image/svg+xml", "fig-excision-equivalence"),
    ("mayer-vietoris-cover.png", 111228, "55ca7d82c34c8381a0ff6d9a2cb89a04ed9c364298277cb3f2a22d5d98e00769", "image/png", "fig-mayer-vietoris-cover"),
    ("mayer-vietoris-cover.svg", 2699, "73da09f59c7b27bcc5ef5dd7b568c97f8bb9da846cf4d0c77d5bfa6536adf733", "image/svg+xml", "fig-mayer-vietoris-cover"),
    ("rp2-mayer-vietoris-cover.png", 154975, "d086a936b73046b2d505204cd016e5b2e6db539245a0f40b77e4d79ee2c85525", "image/png", "fig-rp2-cover"),
    ("rp2-mayer-vietoris-cover.svg", 3039, "fe2eed2d863ee12a01e982cb5158481601216a337d91e79aa3316ffc7b6252e0", "image/svg+xml", "fig-rp2-cover"),
)


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canon(obj: dict[str, Any]) -> bytes:
    return json.dumps(
        obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8") + b"\n"


def common(kind: str, ident: str) -> dict[str, Any]:
    return {
        "entity_type": kind,
        "id": ident,
        "schema": SCHEMA,
        "schema_version": VERSION,
        "status": "active",
        "supersedes": None,
        "timestamp": STAMP,
        "workflow": WORKFLOW,
    }


def require_identity(relative: str, expected: tuple[int, str]) -> bytes:
    raw = (LANE / relative).read_bytes()
    if (len(raw), digest(raw)) != expected:
        raise SystemExit(f"frozen input identity mismatch: {relative}")
    return raw


def sealed_identities() -> dict[str, tuple[int, str]]:
    missing = [path for path, value in SEALED_IDENTITIES.items() if value is None]
    if missing:
        raise SystemExit(
            "Fomberg Unit 004 backend is intentionally unarmed; freeze byte/hash "
            "constants for: " + ", ".join(missing)
        )
    return {path: value for path, value in SEALED_IDENTITIES.items() if value is not None}


def verify_prefix(backend: Path = BACKEND) -> tuple[dict[str, bytes], list[dict[str, Any]]]:
    prefix: dict[str, bytes] = {}
    records: list[dict[str, Any]] = []
    seen: set[str] = set()
    bundle = hashlib.sha256()
    for name in FILES:
        raw = (backend / name).read_bytes()
        count, size, sha = PREFIX[name]
        if (len(raw.splitlines()), len(raw), digest(raw)) != (count, size, sha):
            raise SystemExit(f"{name}: immutable Unit 003 boundary mismatch")
        if b"\r" in raw or not raw.endswith(b"\n"):
            raise SystemExit(f"{name}: invalid LF discipline")
        for number, line in enumerate(raw.splitlines(keepends=True), 1):
            obj = json.loads(line.decode("utf-8"))
            if canon(obj) != line or obj["id"] in seen:
                raise SystemExit(f"{name}:{number}: noncanonical or duplicate prefix")
            seen.add(obj["id"])
            records.append(obj)
        prefix[name] = raw
        bundle.update(name.encode("utf-8"))
        bundle.update(b"\0")
        bundle.update(raw)
    observed = (len(records), sum(map(len, prefix.values())), bundle.hexdigest())
    if observed != PREFIX_TOTAL:
        raise SystemExit(f"immutable Unit 003 bundle mismatch: {observed!r}")
    return prefix, records


def _attrs(text: str) -> dict[str, str]:
    return {
        match.group(1): match.group(2)
        for match in re.finditer(r'(data-[a-z-]+)="([^"]*)"', text)
    }


def parse_reader() -> tuple[list[str], list[dict[str, Any]]]:
    raw = SOURCE.read_bytes()
    if (len(raw), raw.count(b"\n"), digest(raw)) != SOURCE_IDENTITY:
        raise SystemExit("Fomberg Unit 004 reader identity mismatch")
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
        ident = re.search(r'#(o012-fom-u004(?:-[A-Za-z0-9-]+)?)', match.group(3))
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
                number += 1
                opener.append(lines[number - 1])
            joined = " ".join(opener)
            ident = re.search(r'#(o012-fom-u004(?:-[A-Za-z0-9-]+)?)', joined)
            kind = re.match(r'^:{3,}\s*\{\.([^\s}]+)', opener[0].strip())
            node = None
            if ident and kind:
                enclosing = next(
                    (item[1]["id"] for item in reversed(stack) if item[1] is not None),
                    None,
                )
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
                body = [
                    item.strip()
                    for item in lines[node["opener_end"]:number - 1]
                    if item.strip()
                ]
                node["title"] = body[0] if body else node["kind"]
                nodes.append(node)
        number += 1
    if stack:
        raise SystemExit("reader has unclosed fenced div")

    by_local = {node["id"]: node for node in nodes}
    headings = [
        "o012-fom-u004-notice",
        "o012-fom-u004",
        "o012-fom-u004-s07",
        "o012-fom-u004-s08",
        "o012-fom-u004-s09",
        "o012-fom-u004-s10",
        "o012-fom-u004-mastery",
    ]
    if any(ident not in by_local for ident in headings):
        raise SystemExit("reader heading set incomplete")
    boundary_start = by_local["o012-fom-u004-boundary-001"]["line_start"]
    by_local["o012-fom-u004-notice"]["line_end"] = by_local["o012-fom-u004"]["line_start"] - 1
    by_local["o012-fom-u004"]["line_end"] = by_local["o012-fom-u004-mastery"]["line_start"] - 1
    by_local["o012-fom-u004-s07"]["line_end"] = by_local["o012-fom-u004-s08"]["line_start"] - 1
    by_local["o012-fom-u004-s08"]["line_end"] = by_local["o012-fom-u004-s09"]["line_start"] - 1
    by_local["o012-fom-u004-s09"]["line_end"] = by_local["o012-fom-u004-s10"]["line_start"] - 1
    by_local["o012-fom-u004-s10"]["line_end"] = by_local["o012-fom-u004-mastery"]["line_start"] - 1
    by_local["o012-fom-u004-mastery"]["line_end"] = boundary_start - 1

    nodes.sort(key=lambda item: (item["line_start"], 0 if item["kind"] == "heading" else 1))
    ids = [node["id"] for node in nodes]
    classes = Counter(node["kind"] for node in nodes)
    if len(ids) != 117 or len(set(ids)) != 117 or dict(sorted(classes.items())) != EXPECTED_CLASSES:
        raise SystemExit(f"reader stable-ID/class census mismatch: {len(ids)}, {dict(classes)}")
    if [node["id"] for node in nodes if node["kind"] == "heading"] != headings:
        raise SystemExit("reader heading identity/order mismatch")
    aliases = {
        node["attrs"]["data-source-label"]: node["id"]
        for node in nodes if "data-source-label" in node["attrs"]
    }
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
        raise SystemExit("Fomberg Unit 004 upstream span mismatch")
    if lines[NEXT_SOURCE_LINE - 1].strip() != NEXT_HEADING:
        raise SystemExit("Fomberg Unit 004 next-source cursor mismatch")


def verify_assets() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    reader = SOURCE.read_text(encoding="utf-8")
    base = "source/id-ID/fomberg/assets/unit-004"
    for filename, size, sha, media, figure_suffix in ASSET_SPECS:
        relative = f"{base}/{filename}"
        raw = require_identity(relative, (size, sha))
        if media == "image/png":
            if not raw.startswith(b"\x89PNG\r\n\x1a\n"):
                raise SystemExit(f"invalid PNG signature: {relative}")
            link = f"../assets/unit-004/{filename}"
            if reader.count(link) != 1:
                raise SystemExit(f"reader PNG link count mismatch: {relative}")
        else:
            text = raw.decode("utf-8", errors="strict")
            if (
                text.count("<title") != 1 or text.count("<desc") != 1
                or 'role="img"' not in text or "viewBox=" not in text
                or re.search(r'<(?:script|image|foreignObject)\b', text, re.I)
                or re.search(r'\b(?:href|xlink:href)\s*=', text, re.I)
            ):
                raise SystemExit(f"SVG accessibility/self-containment mismatch: {relative}")
        records.append({
            "filename": filename,
            "path": relative,
            "bytes": size,
            "sha256": sha,
            "media_type": media,
            "figure_suffix": figure_suffix,
        })
    return records


def _read_csv_strict(relative: str, expected: tuple[int, str]) -> list[dict[str, str]]:
    raw = require_identity(relative, expected)
    if raw.startswith(b"\xef\xbb\xbf") or b"\r" in raw or not raw.endswith(b"\n"):
        raise SystemExit(f"control file encoding/newline mismatch: {relative}")
    return list(csv.DictReader(raw.decode("utf-8").splitlines()))


def read_controls(identities: dict[str, tuple[int, str]]) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    adverse = _read_csv_strict("00_control/ADVERSE_LEDGER.csv", identities["00_control/ADVERSE_LEDGER.csv"])
    terms = _read_csv_strict("00_control/TERMINOLOGY.csv", identities["00_control/TERMINOLOGY.csv"])
    selected_adverse = [row for row in adverse if 499 <= int(row["event_id"].rsplit("-", 1)[1]) <= 522]
    selected_terms = [row for row in terms if 416 <= int(row["term_id"].rsplit("-", 1)[1]) <= 434]
    if [row["event_id"] for row in selected_adverse] != [f"O012-ADV-{n:04d}" for n in range(499, 523)]:
        raise SystemExit("adverse-ledger Unit 004 identity closure mismatch")
    allowed = {
        "clarified_in_translation", "corrected_in_translation",
        "hypothesis_repaired_in_translation", "pending_future_unit",
        "proof_completed_in_translation", "resolved_before_admission",
    }
    if any(row["status"] not in allowed for row in selected_adverse):
        raise SystemExit("adverse-ledger Unit 004 status mismatch")
    pending = [row["event_id"] for row in selected_adverse if row["status"] == "pending_future_unit"]
    if pending:
        raise SystemExit(f"unexpected Unit 004 pending obligations: {pending}")
    if [row["term_id"] for row in selected_terms] != [f"O012-TERM-{n:04d}" for n in range(416, 435)]:
        raise SystemExit("terminology-ledger Unit 004 identity closure mismatch")
    if any(row["status"] != "admitted" for row in selected_terms):
        raise SystemExit("terminology-ledger Unit 004 admission mismatch")
    return selected_adverse, selected_terms


def _load_json(relative: str, expected: tuple[int, str]) -> tuple[bytes, dict[str, Any]]:
    raw = require_identity(relative, expected)
    if raw.startswith(b"\xef\xbb\xbf") or b"\r" in raw or not raw.endswith(b"\n"):
        raise SystemExit(f"JSON evidence encoding/newline mismatch: {relative}")
    obj = json.loads(raw.decode("utf-8", errors="strict"))
    if not isinstance(obj, dict):
        raise SystemExit(f"JSON evidence top level is not an object: {relative}")
    return raw, obj


def _zero_review(review: dict[str, Any]) -> bool:
    if review.get("status") != "PASS_ZERO_FINDINGS":
        return False
    candidates = [
        review.get("final_finding_counts"),
        review.get("final_findings", {}).get("counts"),
    ]
    for counts in candidates:
        if not isinstance(counts, dict):
            continue
        folded = {str(key).upper(): value for key, value in counts.items()}
        if all(folded.get(key) == 0 for key in ("P1", "P2", "P3")):
            return True
    return False


def verify_all_inputs(identities: dict[str, tuple[int, str]]) -> dict[str, Any]:
    required = set(EVIDENCE_PATHS) | {
        "00_control/TERMINOLOGY.csv", "00_control/ADVERSE_LEDGER.csv"
    }
    if set(identities) != required:
        raise SystemExit("Unit 004 sealed-input inventory mismatch")
    verify_upstream()
    lines, nodes = parse_reader()
    assets = verify_assets()
    adverse, terms = read_controls(identities)
    evidence: dict[str, tuple[bytes, dict[str, Any]]] = {
        path: _load_json(path, identities[path]) for path in EVIDENCE_PATHS
    }
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
        or review.get("checks", {}).get("structure", {}).get("stable_ids") != 117
        or review.get("checks", {}).get("mastery", {}).get("exercise_hint_solution_triples") != 7
    ):
        raise SystemExit("Unit 004 final independent-review binding mismatch")
    expected_repairs = [f"FOM-PR-{number:02d}" for number in range(5, 12)]
    if (
        audit.get("schema_version") != "1.0.0"
        or audit.get("audit_id") != "O012-FOMBERG-UNIT-004-SOURCE-AUDIT"
        or audit.get("status") != "PASS"
        or audit.get("reader", {}).get("sha256") != SOURCE_IDENTITY[2]
        or audit.get("source", {}).get("selected_span", {}).get("sha256") != SPAN_IDENTITY[4]
        or audit.get("source", {}).get("next_line") != NEXT_SOURCE_LINE
        or audit.get("source", {}).get("mathematical_environment_total") != 37
        or audit.get("translation_closure", {}).get("mastery_triples_complete") != 7
        or audit.get("translation_closure", {}).get("proof_repairs_complete") != expected_repairs
        or audit.get("course_route_unit_id") != ROUTE
        or audit.get("model_provenance") != MODEL
    ):
        raise SystemExit("Unit 004 source-audit semantic binding mismatch")
    reader_qa = qa.get("reader", {})
    if (
        qa.get("schema_version") != "1.0.0"
        or qa.get("qa_id") != "O012-FOMBERG-UNIT-004-STATIC-QA"
        or qa.get("status") != "PASS"
        or reader_qa.get("identity", {}).get("sha256") != SOURCE_IDENTITY[2]
        or qa.get("source", {}).get("selected_span", {}).get("sha256") != SPAN_IDENTITY[4]
        or qa.get("source", {}).get("next_line") != NEXT_SOURCE_LINE
        or reader_qa.get("stable_ids") != 117
        or reader_qa.get("stable_ids_unique") != 117
        or reader_qa.get("semantic_class_counts") != EXPECTED_CLASSES
        or reader_qa.get("mastery", {}).get("exercise_hint_solution_triples") != 7
        or reader_qa.get("mastery", {}).get("complete_solutions") != 7
        or reader_qa.get("proof_repairs") != expected_repairs
        or reader_qa.get("assets", {}).get("semantic_figures") != 19
        or reader_qa.get("assets", {}).get("raster_redraws") != 3
        or qa.get("model_provenance") != MODEL
        or not qa.get("gates")
        or not all(value == "PASS" for value in qa["gates"].values())
    ):
        raise SystemExit("Unit 004 static-QA semantic binding mismatch")
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
    for number in range(1, 8):
        for kind in ("mcheck", "hint", "sol"):
            if f"o012-fom-u004-{kind}-{number:03d}" not in ids:
                raise SystemExit(f"mastery triple {number} incomplete")
    required_text = (
        *[f"FOM-PR-{number:02d}" for number in range(5, 12)],
        "o012-fom-u004-proof-pr05a",
        "o012-fom-u004-proof-pr05b",
        "o012-fom-u004-proof-pr06",
        "o012-fom-u004-proof-five-lemma-repair",
        "o012-fom-u004-proof-injectivity-comparison-repair",
        "o012-fom-u004-proof-naturality-repair",
        "o012-fom-u004-proof-relative-generator-repair",
        "o012-fom-u004-proof-compact-finite-simplices-repair",
    )
    joined = "\n".join(lines)
    if any(marker not in joined for marker in required_text):
        raise SystemExit("required Unit 004 mathematical/provenance marker missing")
    terms_by_id = {row["term_id"]: row for row in terms}
    terminology_token_overrides = {
        "O012-TERM-0422": ("kompleks", "asiklik"),
        "O012-TERM-0424": ("homologi relatif", "hasil bagi"),
        "O012-TERM-0429": ("simpleksial", "singular", "perbandingan"),
        "O012-TERM-0432": ("dukungan", "rantai"),
    }

    def fold(value: str) -> str:
        value = value.casefold().replace("–", "-").replace("—", "-")
        value = re.sub(r"\\mathcal\s*\{?u\}?", "u", value)
        value = re.sub(r"[`*$\\{}_[\]()]", "", value)
        value = re.sub(r"\s+", " ", value)
        return value.strip()

    for _, control_id, evidence_suffix in TERM_SPECS:
        node = node_by_id[f"o012-fom-u004-{evidence_suffix}"]
        evidence_text = fold("\n".join(lines[node["line_start"] - 1:node["line_end"]]))
        preferred_present = fold(terms_by_id[control_id]["id_ID"]) in evidence_text
        if control_id in terminology_token_overrides:
            preferred_present = all(token in evidence_text for token in terminology_token_overrides[control_id])
        if not preferred_present:
            raise SystemExit(f"terminology evidence lacks admitted form: {control_id}")
    return {
        "lines": lines,
        "nodes": nodes,
        "assets": assets,
        "adverse": adverse,
        "terms": terms,
        "audit": audit,
        "qa": qa,
        "review": review,
    }


def target_locator(lines: list[str], start: int, end: int) -> dict[str, Any]:
    raw_lines = SOURCE.read_bytes().splitlines(keepends=True)
    return {
        "path": SOURCE_PATH,
        "line_start": start,
        "line_end": end,
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
        locator = {
            "path": "algebraic_topology.tex",
            "commit_sha": COMMIT,
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
        "o012-fom-u004-s07",
        "o012-fom-u004-s08",
        "o012-fom-u004-s09",
        "o012-fom-u004-s10",
        "o012-fom-u004-mastery",
    )
    raw_parent: dict[str, str] = {
        "o012-fom-u004-notice": ROOT,
        "o012-fom-u004-s07": ROOT,
        "o012-fom-u004-s08": ROOT,
        "o012-fom-u004-s09": ROOT,
        "o012-fom-u004-s10": ROOT,
        "o012-fom-u004-mastery": ROOT,
        "o012-fom-u004-boundary-001": ROOT,
    }
    for node in nodes:
        ident = node["id"]
        if ident == "o012-fom-u004" or ident in raw_parent:
            continue
        if node.get("enclosing_div"):
            raw_parent[ident] = f"unit:{node['enclosing_div']}"
            continue
        section = next(
            (sid for sid in sections if by_local[sid]["line_start"] <= node["line_start"] <= by_local[sid]["line_end"]),
            None,
        )
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

    return {
        ident: (parent, children[parent].index(ident) + 1, path_for(ident))
        for ident, parent in raw_parent.items()
    }


def load_generic():
    path = LANE / "scripts/validate-backend.py"
    spec = importlib.util.spec_from_file_location("o012_generic_fom004", path)
    if spec is None or spec.loader is None:
        raise SystemExit("cannot load generic backend validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _correction_targets(row: dict[str, str], node_ids: set[str]) -> list[str]:
    targets = sorted(set(re.findall(r'#(o012-fom-u004(?:-[A-Za-z0-9-]+)?)', row["source_location"])))
    if not targets or any(target not in node_ids for target in targets):
        raise SystemExit(f"adverse row target resolution failed: {row['event_id']}")
    return targets


def build_additions(data: dict[str, Any], evidence_identities: dict[str, tuple[int, str]]) -> dict[str, list[dict[str, Any]]]:
    lines: list[str] = data["lines"]
    nodes: list[dict[str, Any]] = data["nodes"]
    additions: dict[str, list[dict[str, Any]]] = {name: [] for name in FILES}
    all_concepts = [
        "concept:excision", "concept:mayer-vietoris-long-exact-sequence",
        "concept:naturality", "concept:five-lemma",
        "concept:singular-homology", "concept:simplicial-homology",
        "concept:relative-homology", "concept:reduced-homology",
        "concept:chain-map", "concept:chain-homotopy-equivalence",
        *[f"concept:{slug}" for slug, _, _ in TERM_SPECS],
    ]

    def add(name: str, record: dict[str, Any]) -> None:
        additions[name].append(record)

    for ident, attribution, change, third in (
        (
            COMPANION_RIGHTS,
            "Original Indonesian mastery, solutions, proof repairs, source audits, and accessible redraws for Fomberg Unit 004.",
            "Original additions and redraws are distinguished from the Fomberg source component.",
            "Original Unit 004 companion layer; source content remains separately attributed.",
        ),
        (
            COMPOSITE_RIGHTS,
            "Fomberg source adaptation plus original Indonesian Unit 004 companion layer.",
            "Integrated reader preserves exact locators, change notices, proof-repair identity, and per-asset provenance.",
            "Composite Unit 004; component-scoped rights records control.",
        ),
    ):
        rec = common("rights", ident)
        rec.update(
            attribution=attribution,
            change_notice=change,
            component_scope=[ROOT],
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
            concept_id=f"concept:{slug}",
            evidence_segment_id=f"segment:o012-fom-u004-{evidence_suffix}",
            locale="id-ID",
            preferred=row["id_ID"],
            register="textbook",
            rejected_forms=[],
            rights_component_id=COMPOSITE_RIGHTS,
            scope_unit_id=ROOT,
            source_term=row["source_term"],
            terminology_control_id=row["term_id"],
            terminology_status=row["status"],
            usage_note=row["note"],
            variants=[],
        )
        add("terms.jsonl", term)

    parents = parentage(nodes)
    source_headings = {
        "o012-fom-u004-s07", "o012-fom-u004-s08",
        "o012-fom-u004-s09", "o012-fom-u004-s10",
    }
    source_kinds = {
        "definition", "remark", "example", "theorem", "corollary",
        "proposition", "lemma", "proof", "figure", "source-omission",
    }
    for node in nodes:
        ident = node["id"]
        uid = f"unit:{ident}"
        kind = node["kind"]
        attrs = node["attrs"]
        is_root = ident == "o012-fom-u004"
        source_range = attrs.get("data-source-lines")
        explicit_original = attrs.get("data-origin") == "edition-original"
        is_source = not explicit_original and (
            ident in source_headings or (kind in source_kinds and source_range is not None)
        )
        if is_root:
            rights = COMPOSITE_RIGHTS
            provenance = "composite_translated_and_original"
            parent = COURSE
            order = 34
            path = [ROOT]
            display = "Topologi Aljabar — Komponen Fomberg Unit 004: Eksisi, Mayer–Vietoris, Kealamian, dan Pembandingan Homologi"
            locator = target_locator(lines, 1, len(lines))
        else:
            rights = SOURCE_RIGHTS if is_source else COMPANION_RIGHTS
            provenance = (
                "translated_adapted_from_upstream" if is_source
                else "edition_original_proof_repair"
                if kind in {"proof", "proof-supplement"} and attrs.get("data-repair-id")
                else "edition_original"
            )
            parent, order, path = parents[ident]
            display = clean_title(node["title"], kind)
            locator = target_locator(lines, node["line_start"], node["line_end"])
        unit_kind = "reader_unit" if is_root else ("section" if kind == "heading" else kind.replace("-", "_"))
        unit = common("unit", uid)
        unit.update(
            component_source_commit=COMMIT,
            component_source_id=RESOURCE,
            concept_ids=all_concepts,
            course_id=COURSE,
            course_route_unit_id=ROUTE,
            display_title=display,
            edition_id=EDITION,
            edition_unit_id=ROOT,
            locale="id-ID",
            model_provenance=MODEL,
            order=order,
            parent_id=parent,
            path=path,
            program_id=PROGRAM,
            provenance_relation=provenance,
            resource_id=RESOURCE,
            rights_component_id=rights,
            source_local_id=ident,
            target_locator=locator,
            translation_state="structurally_verified",
            unit_kind=unit_kind,
        )
        if is_root:
            unit.update(
                edition_order=4,
                route_order=11,
                source_locator={
                    "path": "algebraic_topology.tex", "commit_sha": COMMIT,
                    "line_start": 1923, "line_end": 2846,
                    "precision": "exact_unit_span", "span_bytes": 38503,
                    "span_sha256": SPAN_IDENTITY[4],
                },
            )
        alias = attrs.get("data-source-label")
        if alias:
            unit["source_aliases"] = [alias]
        repair_id = attrs.get("data-repair-id")
        if repair_id:
            unit["repair_id"] = repair_id
            if kind == "source-omission":
                unit["proof_status"] = "source_omission_named"
            elif kind in {"proof", "proof-supplement", "theorem", "proposition", "lemma"}:
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
                "line_start": 1923, "line_end": 2846,
                "precision": "exact_unit_span",
            }
        else:
            segment_rights = rights
            segment_provenance = provenance
            segment_locator = locator
            segment_source_locator = source_locator(source_range if is_source else None)
        segment = common("segment", f"segment:{ident}")
        segment.update(
            component_source_commit=COMMIT,
            component_source_id=RESOURCE,
            concept_ids=all_concepts,
            course_route_unit_id=ROUTE,
            edition_id=EDITION,
            edition_unit_id=ROOT,
            locale="id-ID",
            model_provenance=MODEL,
            order=order,
            provenance_relation=segment_provenance,
            resource_id=RESOURCE,
            rights_component_id=segment_rights,
            segment_kind="source_heading" if is_root else unit_kind,
            source_local_id=ident,
            source_locator=segment_source_locator,
            target_locator=segment_locator,
            translation_state="structurally_verified",
            unit_id=uid,
        )
        for key in ("source_aliases", "repair_id", "proof_status", "solution_status"):
            if key in unit:
                segment[key] = unit[key]
        add("segments.jsonl", segment)

    source_size, _, source_sha = SOURCE_IDENTITY
    source_asset = common("asset", "asset:o012-fom-u004-source-markdown")
    source_asset.update(
        bytes=source_size, edition_id=EDITION,
        media_type="text/markdown; charset=utf-8", path=SOURCE_PATH,
        resource_id=RESOURCE, rights_component_id=COMPOSITE_RIGHTS,
        role="canonical_reader_source", sha256=source_sha, unit_id=ROOT,
    )
    add("assets.jsonl", source_asset)
    figures = [node for node in nodes if node["kind"] == "figure"]
    diagram_asset = common("asset", "asset:o012-fom-u004-semantic-diagram-layer")
    diagram_asset.update(
        bytes=source_size, edition_id=EDITION,
        media_type="text/markdown; charset=utf-8", path=SOURCE_PATH,
        resource_id=RESOURCE, rights_component_id=COMPOSITE_RIGHTS,
        role="semantic_diagram_accessibility_layer", sha256=source_sha,
        source_diagram_count=20, semantic_figure_block_count=19,
        geometric_redraw_count=3,
        semantic_unit_ids=[f"unit:{node['id']}" for node in figures],
        unit_id=ROOT,
    )
    add("assets.jsonl", diagram_asset)
    for asset in data["assets"]:
        slug = asset["filename"].replace(".", "-")
        rec = common("asset", f"asset:o012-fom-u004-{slug}")
        rec.update(
            bytes=asset["bytes"], edition_id=EDITION,
            media_type=asset["media_type"], path=asset["path"],
            resource_id=RESOURCE, rights_component_id=COMPANION_RIGHTS,
            role=("reader_linked_accessible_redraw" if asset["media_type"] == "image/png" else "accessible_vector_source_companion"),
            sha256=asset["sha256"],
            source_figure_unit_id=f"unit:o012-fom-u004-{asset['figure_suffix']}",
            unit_id=ROOT,
        )
        add("assets.jsonl", rec)

    artifact_specs = (
        ("artifact:o012-fom-u004-source-audit", AUDIT_PATH, ["qa:o012-fom-u004-source-integrity"], "source_frozen"),
        ("artifact:o012-fom-u004-review-final", REVIEW_PATH, ["qa:o012-fom-u004-math", "qa:o012-fom-u004-language"], "mathematically_reviewed"),
        ("artifact:o012-fom-u004-qa", QA_PATH, ["qa:o012-fom-u004-source-integrity", "qa:o012-fom-u004-mastery"], "built"),
    )
    for ident, relative, qa_ids, state in artifact_specs:
        size, sha = evidence_identities[relative]
        rec = common("artifact", ident)
        rec.update(
            bytes=size, locale="id-ID", manifest_artifact_id=None,
            media_type="application/json", path=relative,
            qa_event_ids=qa_ids, rights_component_id=COMPOSITE_RIGHTS,
            sha256=sha,
            toolchain=(
                "Fomberg Unit 004 evidence; algebraic_topology.tex:1923-2846; "
                f"{SPAN_IDENTITY[4]}; {MODEL}; route D60-R11; semantic admission only."
            ),
            translation_state=state, unit_id=ROOT,
        )
        add("artifacts.jsonl", rec)

    for ident, kind, note, witnesses in (
        (
            "qa:o012-fom-u004-source-integrity", "source",
            "Exact lines 1923-2846, cursor 2847, 117 stable IDs, 20 source diagram environments, 19 semantic figure blocks, and six redraw files passed.",
            ["artifact:o012-fom-u004-source-audit", "artifact:o012-fom-u004-review-final", "artifact:o012-fom-u004-qa"],
        ),
        (
            "qa:o012-fom-u004-math", "math",
            "The final independent review passed P1=P2=P3=0; FOM-PR-05 through FOM-PR-11 are complete.",
            ["artifact:o012-fom-u004-review-final"],
        ),
        (
            "qa:o012-fom-u004-language", "language",
            "Final Indonesian reviews passed after terminology, provenance, notation, and source-order repairs.",
            ["artifact:o012-fom-u004-review-final"],
        ),
        (
            "qa:o012-fom-u004-mastery", "mastery",
            "Seven exercises, seven hints, and seven complete checked solutions passed.",
            ["artifact:o012-fom-u004-qa"],
        ),
    ):
        rec = common("qa_event", ident)
        rec.update(note=note, qa_type=kind, result="passed", unit_id=ROOT, witness_artifact_ids=witnesses)
        add("qa.jsonl", rec)

    node_ids = {node["id"] for node in nodes}
    correction_type = {
        499: "mathematical_correction", 500: "proof_completion",
        501: "notation_correction", 502: "proof_completion",
        503: "hypothesis_repair", 504: "hypothesis_repair",
        505: "mathematical_correction", 506: "mathematical_correction",
        507: "mathematical_correction", 508: "mathematical_correction",
        509: "mathematical_clarification", 510: "diagram_fidelity",
        511: "mathematical_correction", 512: "proof_completion",
        513: "proof_completion", 514: "source_typo",
        515: "mathematical_correction", 516: "proof_completion",
        517: "mathematical_correction", 518: "notation_correction",
        519: "proof_completion", 520: "proof_completion",
        521: "mathematical_correction", 522: "proof_completion",
    }
    for row in data["adverse"]:
        number = int(row["event_id"].rsplit("-", 1)[1])
        targets = _correction_targets(row, node_ids)
        rec = common("correction", f"correction:o012-fom-u004-adv-{number:04d}")
        rec.update(
            adverse_ledger_id=row["event_id"],
            affected_unit_ids=[f"unit:{target}" for target in targets],
            correction_type=correction_type.get(number, "source_typo" if row["severity"] == "P3" else "mathematical_correction"),
            edition_id=EDITION,
            evidence=row["source_location"],
            evidence_segment_id=f"segment:{targets[0]}",
            rationale=row["rationale"],
            resource_id=RESOURCE,
            source_defect=row["observed"],
            target_change=row["action"],
            unit_id=ROOT,
            upstream_report_disposition="not_contacted",
            resolution_status=row["status"],
        )
        add("corrections.jsonl", rec)

    def relation(ident: str, from_id: str, to_id: str, kind: str, note: str, **extra: Any) -> None:
        rec = common("relation", ident)
        rec.update(from_id=from_id, to_id=to_id, relation_type=kind, note=note, **extra)
        add("relations.jsonl", rec)

    relation("relation:adapts:o012-fom-u004:fomberg-edition", ROOT, EDITION, "adapts", "Indonesian Unit 004 adapts exact Fomberg lines 1923-2846.")
    relation("relation:contains:o012-d60:fomberg-u004", COURSE, ROOT, "contains", "Course route D60-R11 contains Fomberg Unit 004.", course_route_unit_id=ROUTE)
    relation("relation:precedes:o012-fom-u003:o012-fom-u004", "unit:o012-fom-u003", ROOT, "precedes", "Fomberg Unit 003 precedes Unit 004 in source order.")
    relation("relation:contains:o012-d60-rights:fomberg-u004", ROUTE_RIGHTS, ROOT, "contains", "Integrated-route rights contain the Fomberg Unit 004 composite.")
    relation("relation:precedes:o012-fom-u004:mastery", ROOT, "unit:o012-fom-u004-mastery", "precedes", "Translated source body and repair dossier precede the solved mastery layer.")
    for suffix, proof_id, target_id, repair_id, note in (
        ("pr05a:small-chain-theorem", "proof-pr05a", "prop-small-chains", "FOM-PR-05", "The original diameter-and-iteration repair proves the quantitative subdivision part of the small-chain theorem."),
        ("pr05b:small-chain-theorem", "proof-pr05b", "prop-small-chains", "FOM-PR-05", "The original subdivision and contracting-homotopy repair completes the small-chain theorem."),
        ("pr06:excision", "proof-pr06", "thm-excision-cover", "FOM-PR-06", "The original quotient-chain and Five-Lemma argument completes excision."),
        ("pr07:five-lemma", "proof-five-lemma-repair", "lem-five", "FOM-PR-07", "The original element chase proves injectivity and surjectivity in the Five Lemma."),
        ("pr08:comparison-injectivity", "proof-injectivity-comparison-repair", "prop-sing-simp", "FOM-PR-08", "The original finite-support argument closes injectivity of simplicial-to-singular comparison."),
        ("pr09:naturality", "proof-naturality-repair", "rem-naturality-chain-complexes", "FOM-PR-09", "The original chain-level calculation proves naturality of the connecting homomorphism."),
        ("pr10:relative-generator", "proof-relative-generator-repair", "prop-sing-simp", "FOM-PR-10", "The original generator calculation identifies the actual comparison map on relative summands."),
        ("pr11:compact-support", "proof-compact-finite-simplices-repair", "lem-compact-finite-simplices", "FOM-PR-11", "The original weak-topology argument completes the compact finite-simplices lemma."),
    ):
        relation(
            f"relation:proves:o012-fom-u004-{suffix}",
            f"unit:o012-fom-u004-{proof_id}",
            f"unit:o012-fom-u004-{target_id}",
            "proves", note, repair_id=repair_id,
        )
    relation(
        "relation:depends-on:o012-fom-u004-pr06:small-chain-theorem",
        "unit:o012-fom-u004-proof-pr06",
        "unit:o012-fom-u004-prop-small-chains",
        "depends-on", "The excision repair uses the small-chain theorem and its complete FOM-PR-05 proof.",
    )
    for number in range(1, 8):
        relation(
            f"relation:hints:fom-u004-hint-{number:03d}:mcheck-{number:03d}",
            f"unit:o012-fom-u004-hint-{number:03d}",
            f"unit:o012-fom-u004-mcheck-{number:03d}", "hints",
            f"Hint for Fomberg Unit 004 mastery check {number}.",
        )
        relation(
            f"relation:solves:fom-u004-sol-{number:03d}:mcheck-{number:03d}",
            f"unit:o012-fom-u004-sol-{number:03d}",
            f"unit:o012-fom-u004-mcheck-{number:03d}", "solves",
            f"Complete checked solution for Unit 004 mastery check {number}.",
        )
    for number, node in enumerate(figures, 1):
        relation(
            f"relation:illustrates:fom-u004-fig-{number:03d}:diagram-layer",
            f"unit:{node['id']}", "asset:o012-fom-u004-semantic-diagram-layer",
            "illustrates", f"Semantic figure block {number} preserves its source diagram function.",
        )
    png_by_figure = {
        asset["figure_suffix"]: asset for asset in data["assets"]
        if asset["media_type"] == "image/png"
    }
    for suffix, asset in sorted(png_by_figure.items()):
        png_id = f"asset:o012-fom-u004-{asset['filename'].replace('.', '-')}"
        svg_name = asset["filename"].removesuffix(".png") + ".svg"
        svg_id = f"asset:o012-fom-u004-{svg_name.replace('.', '-')}"
        relation(
            f"relation:illustrates:o012-fom-u004-{suffix}:{asset['filename'].removesuffix('.png')}",
            f"unit:o012-fom-u004-{suffix}", png_id, "illustrates",
            "Reader-linked PNG is the raster rendering of the independently authored accessible redraw.",
        )
        relation(
            f"relation:xref:{asset['filename'].removesuffix('.png')}:svg-source",
            png_id, svg_id, "xref", "PNG redraw has this accessible SVG source companion.",
        )

    for name, records in additions.items():
        records.sort(key=lambda item: item["id"])
        if len(records) != DELTA[name]:
            raise SystemExit(f"{name}: derived suffix count mismatch ({len(records)} != {DELTA[name]})")
        if len({record["id"] for record in records}) != len(records):
            raise SystemExit(f"{name}: duplicate derived IDs")
    return additions


def planned_additions() -> dict[str, list[dict[str, Any]]]:
    """Derive the exact record-ID plan without reading unsealed audit/QA files."""
    lines, nodes = parse_reader()
    assets = verify_assets()
    control_identities = {
        key: value for key, value in SEALED_IDENTITIES.items()
        if key.startswith("00_control/") and value is not None
    }
    if len(control_identities) != 2:
        raise SystemExit("Unit 004 control ledgers must be sealed before planning")
    adverse, terms = read_controls(control_identities)
    synthetic_evidence = {
        path: (
            SEALED_IDENTITIES[path]
            if SEALED_IDENTITIES[path] is not None
            else (0, "0" * 64)
        )
        for path in EVIDENCE_PATHS
    }
    return build_additions(
        {
            "lines": lines, "nodes": nodes, "assets": assets,
            "adverse": adverse, "terms": terms,
        },
        synthetic_evidence,
    )


def record_plan() -> dict[str, Any]:
    additions = planned_additions()
    artifact_paths = [record["path"] for record in additions["artifacts.jsonl"]]
    return {
        "edition_unit_id": ROOT,
        "root_unit_id": ROOT,
        "course_id": COURSE,
        "course_route_unit_id": ROUTE,
        "resource_id": RESOURCE,
        "edition_id": EDITION,
        "immutable_prefix": {
            "records": PREFIX_TOTAL[0], "bytes": PREFIX_TOTAL[1],
            "bundle_sha256": PREFIX_TOTAL[2],
        },
        "records_by_file": DELTA,
        "records_planned": sum(DELTA.values()),
        "record_ids_by_file": {
            name: [record["id"] for record in additions[name]] for name in FILES
        },
        "cumulative_records_planned": PREFIX_TOTAL[0] + sum(DELTA.values()),
        "stable_ids": 117,
        "asset_records": 8,
        "real_redraw_files": 6,
        "artifact_evidence_paths_in_record_order": artifact_paths,
        "unsealed_identity_paths": [path for path, value in SEALED_IDENTITIES.items() if value is None],
    }
