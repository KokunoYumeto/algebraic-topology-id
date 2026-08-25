#!/usr/bin/env python3
"""Frozen inputs and deterministic backend records for Fomberg Unit 003.

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
    "fomberg-unit-003-exact-sequences-relative-homology.md"
)
SOURCE = LANE / SOURCE_PATH
SOURCE_IDENTITY = (
    65540,
    1773,
    "2571f62b977c00bff20e04756925a73497c0129f8c987940db0e1a649177f6b9",
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
    1291,
    1922,
    632,
    24270,
    "870e617b30b82eb8a557b0733096623a73375ed079601e7e7938ce489d0ce064",
)
NEXT_SOURCE_LINE = 1923
NEXT_HEADING = r"\subsection{Excisions}"
COMMIT = "563194fae879178b9a6871b249513bfc27968975"
TREE = "fb678966d1533d529bdd72f49d8496a3bdc14a9b"
RESOURCE = "resource:fomberg-algebraic-topology-2025"
EDITION = "edition:fomberg-at-2025-563194f"
ROOT = "unit:o012-fom-u003"
PROGRAM = "program:o012-id"
COURSE = "course:o012-d60"
ROUTE = "D60-R10"

SOURCE_RIGHTS = "rights:fomberg-cc-by-sa-4.0"
COMPANION_RIGHTS = "rights:o012-fom-u003-companion-cc-by-sa-4.0"
COMPOSITE_RIGHTS = "rights:o012-fom-u003-composite-cc-by-sa-4.0"
ROUTE_RIGHTS = "rights:o012-d60-integrated-route-cc-by-sa-4.0"

# The exact live Unit 002 boundary.  Every byte must remain unchanged.
PREFIX = {
    "artifacts.jsonl": (171, 138011, "a00faf7b551c78877ac3ccb63bea6c41acfb99b44650b7252d3ff712f82f30bf"),
    "assets.jsonl": (39, 25764, "6e42327b00c646ab51244617b4134ccc3ab485d9a6ed0958f021b09f5c34e437"),
    "authority.jsonl": (6, 4374, "84c622f56dbbd5ba379361245ecfe07bc79c9f4fd6b18ba21b82b5f545211869"),
    "concepts.jsonl": (399, 125910, "519471339231312fbf1212c6715fcba8ecbd80bda78fc8093efbfc9557eee063"),
    "corrections.jsonl": (456, 450915, "c472b154d819accbaf3112faef219abe44144d2e25d74cbf2882b3e8682c7a74"),
    "qa.jsonl": (142, 79219, "80774625c28219f47197f1052bf0c6e9e9f037bc5742d29cd69f1bb470409e33"),
    "relations.jsonl": (598, 246923, "84e3eacd1aa9494520b9209884e5dea24af327802ad097f42997ac23b74902c6"),
    "rights.jsonl": (93, 85068, "ba42ccf15296173d6f6f7f120bc12799865336e040602c2fc864c729f3f3c17b"),
    "segments.jsonl": (1508, 2249492, "4a1b83ec9f62eda12a665eede822b72f3629722d8a87007b71ddf2f6ad4ed22f"),
    "terms.jsonl": (392, 251976, "c019c3ef89ebec9a14a7d2aa85e3bacbe149938b9a147b3c09cf333fccc1e091"),
    "units.jsonl": (1538, 2382471, "1158a33c29e6542b98ed773eaf8016e80d7a5b0a54adfaad89da334e1828e2df"),
}
PREFIX_TOTAL = (
    5342,
    6040123,
    "83d98f1b271c5e62334a072354f1be1c4a1535ed26c8a403223e89773bb1eba1",
)

EXPECTED_CLASSES = {
    "boundary": 1,
    "corollary": 4,
    "definition": 7,
    "example": 7,
    "exercise": 6,
    "figure": 26,
    "heading": 6,
    "hint": 6,
    "proof": 7,
    "proof-supplement": 4,
    "proposition": 1,
    "remark": 13,
    "solution": 6,
    "source-audit": 27,
    "source-omission": 2,
    "theorem": 2,
}

# 125 units + 125 segments; 42 corrections; 15 terms/concepts; six frozen
# evidence artifacts; 14 assets (reader, semantic layer, six PNG/SVG pairs);
# four QA events; two rights rows; and 57 semantic relations.
DELTA = {
    "artifacts.jsonl": 6,
    "assets.jsonl": 14,
    "authority.jsonl": 0,
    "concepts.jsonl": 15,
    "corrections.jsonl": 42,
    "qa.jsonl": 4,
    "relations.jsonl": 57,
    "rights.jsonl": 2,
    "segments.jsonl": 125,
    "terms.jsonl": 15,
    "units.jsonl": 125,
}

AUDIT_PATH = "qa/FOMBERG_UNIT_003_SOURCE_AUDIT.json"
QA_PATH = "qa/FOMBERG_UNIT_003_QA.json"
REVIEW_PATHS = {
    "exact": "qa/fomberg-unit-003/INDEPENDENT_REVIEW_EXACT_FINAL.json",
    "relative": "qa/fomberg-unit-003/INDEPENDENT_REVIEW_RELATIVE_FINAL.json",
    "integrated": "qa/fomberg-unit-003/INDEPENDENT_REVIEW_INTEGRATED_FINAL.json",
}
RECONCILIATION_PATH = (
    "qa/fomberg-unit-003/INTEGRATED_REVIEW_COUNT_RECONCILIATION.json"
)
EVIDENCE_PATHS = (
    AUDIT_PATH,
    REVIEW_PATHS["exact"],
    REVIEW_PATHS["relative"],
    REVIEW_PATHS["integrated"],
    RECONCILIATION_PATH,
    QA_PATH,
)

# Replace only the four None values after the corresponding files are final.
# Tuple values are (bytes, sha256).  The producer refuses to append otherwise.
SEALED_IDENTITIES: dict[str, tuple[int, str] | None] = {
    AUDIT_PATH: (
        443845,
        "e9bde4987e24e8d3839208f3d70c76a3362702f0f6e6b8e0eefb5467c80e80b2",
    ),
    REVIEW_PATHS["exact"]: (
        11017,
        "360d84f2deb75445e698050c9e968284612ec087bfec606dfc63427b069c5e5d",
    ),
    REVIEW_PATHS["relative"]: (
        11409,
        "5471e6ee304713da288d075fb1e506c6b2125f4e7090740044f181fb31bf97fb",
    ),
    REVIEW_PATHS["integrated"]: (
        12424,
        "eec178895fde82ffd3dfff04f3167bdf3fa276f5352c11e5db2a4cf7ea8f06f5",
    ),
    RECONCILIATION_PATH: (
        2013,
        "48fd3133d1136d6c102960f0e269ed6090fd8cb62ec353bf2f69853bb8415243",
    ),
    QA_PATH: (
        39281,
        "1ec779739012e45e098786d6d8f9d9f5fb3b456146bd769d535cdaf4342c5963",
    ),
    "00_control/TERMINOLOGY.csv": (
        49864,
        "5374b6073eadda56e8ad752fd7ec65c1459f58054125f53a7343ecdd0adaf9a1",
    ),
    "00_control/ADVERSE_LEDGER.csv": (
        167596,
        "0eee620b74dbfb3f6ee4d2030f6ca77c7ae4cf169fd09a604c82bb29895e5a3b",
    ),
}

ALIASES = {
    "exmp:short-exact-sequence-isomorphism": "o012-fom-u003-ex-isomorphism",
    "thm:les-of-quotient-space": "o012-fom-u003-thm-les-quotient",
    "cor:homologies-of-spheres": "o012-fom-u003-cor-sphere-homology",
    "thm:long-exact-consequence": "o012-fom-u003-thm-long-exact",
}

TERM_SPECS = (
    ("good-pair", "O012-TERM-0401", "def-good-pair"),
    ("cone", "O012-TERM-0402", "def-cone"),
    ("suspension", "O012-TERM-0403", "def-suspension"),
    ("relative-chain-group", "O012-TERM-0404", "def-relative-chain-group"),
    ("relative-homology", "O012-TERM-0405", "def-relative-homology"),
    ("relative-cycle", "O012-TERM-0406", "rem-relative-cycle"),
    ("relative-boundary", "O012-TERM-0407", "rem-relative-boundary"),
    ("homotopy-through-maps-of-pairs", "O012-TERM-0408", "audit-pair-homotopy"),
    ("commutative-diagram", "O012-TERM-0409", "rem-short-exact-chain-complexes"),
    ("injective", "O012-TERM-0410", "ex-injective"),
    ("surjective", "O012-TERM-0411", "ex-surjective"),
    ("inclusion-map", "O012-TERM-0412", "thm-les-quotient"),
    ("basis", "O012-TERM-0413", "def-relative-chain-group"),
    ("topological-boundary", "O012-TERM-0414", "fig-brouwer-retraction"),
    ("long-exact-sequence-of-a-triple", "O012-TERM-0415", "rem-triple-long-exact"),
)

ASSET_SPECS = (
    ("brouwer-radial-retraction.png", 180164, "97b0745e2b31b911fa777bdade3d51d88f5247a4d1d9cf29bf1c4aedc5f287c1", "image/png", "fig-brouwer-retraction"),
    ("brouwer-radial-retraction.svg", 1359, "34170760d9179f61ec3ece881e21e83a5a1556ddc86a781d163ff76d796b0885", "image/svg+xml", "fig-brouwer-retraction"),
    ("cone-circle.png", 37062, "40b452e48da782626b1b75425e57d4dd3ee202d337f3d8189db395077a1eaf35", "image/png", "fig-circle-cone"),
    ("cone-circle.svg", 1092, "ee45855df1ad90ea6e2fdf26f3a4790ab60e1c3fab194a597a612f1a9ddb7b83", "image/svg+xml", "fig-circle-cone"),
    ("relative-boundary.png", 291686, "20393edd49cb9fa29dade8fbae82387ee7eaa955ed1161648f9292f40e9af6f9", "image/png", "fig-relative-boundary"),
    ("relative-boundary.svg", 1899, "ec7af0378a1a92ddecda8cf27fd13cd73a68079e6286d845c441434e7a945eb4", "image/svg+xml", "fig-relative-boundary"),
    ("relative-chains-formal.png", 297867, "c9789bf829f308bbd3b80350d510f9c26c2c03d2878e7133dfa46b0395cbdefa", "image/png", "fig-formal-relative-chains"),
    ("relative-chains-formal.svg", 2565, "ca5e9d78c07579b0bf5b162fbe21769d2eb16bc590179d3a6765e3ad973e57b9", "image/svg+xml", "fig-formal-relative-chains"),
    ("relative-cycle.png", 260456, "e7057f0cc58dbe48eac8369e04f61fea9c5974dc1882f4ca53a3532c5ccc9e7f", "image/png", "fig-relative-cycle"),
    ("relative-cycle.svg", 1671, "e3ef9ef498f8e379cca12b4d769c35f5b90d4c823860b8ef7249ace19d12e459", "image/svg+xml", "fig-relative-cycle"),
    ("suspension-circle.png", 148311, "ad79445d601905192911cc3ee7e8457bb00bae17e7ece767798c2316709cfa3d", "image/png", "fig-circle-suspension"),
    ("suspension-circle.svg", 1350, "2c31c274111fc3a059868a58e39035782fcbae73389975bacab65c8797a8cdef", "image/svg+xml", "fig-circle-suspension"),
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
            "Fomberg Unit 003 backend is intentionally unarmed; freeze byte/hash "
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
            raise SystemExit(f"{name}: immutable Unit 002 boundary mismatch")
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
        raise SystemExit(f"immutable Unit 002 bundle mismatch: {observed!r}")
    return prefix, records


def _attrs(text: str) -> dict[str, str]:
    return {
        match.group(1): match.group(2)
        for match in re.finditer(r'(data-[a-z-]+)="([^"]*)"', text)
    }


def parse_reader() -> tuple[list[str], list[dict[str, Any]]]:
    raw = SOURCE.read_bytes()
    if (len(raw), raw.count(b"\n"), digest(raw)) != SOURCE_IDENTITY:
        raise SystemExit("Fomberg Unit 003 reader identity mismatch")
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
        ident = re.search(r'#(o012-fom-u003(?:-[A-Za-z0-9-]+)?)', match.group(3))
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
            ident = re.search(r'#(o012-fom-u003(?:-[A-Za-z0-9-]+)?)', joined)
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
        "o012-fom-u003-notice",
        "o012-fom-u003",
        "o012-fom-u003-s05",
        "o012-fom-u003-source-corrections",
        "o012-fom-u003-s06",
        "o012-fom-u003-mastery",
    ]
    if any(ident not in by_local for ident in headings):
        raise SystemExit("reader heading set incomplete")
    boundary_start = by_local["o012-fom-u003-boundary-001"]["line_start"]
    by_local["o012-fom-u003-notice"]["line_end"] = by_local["o012-fom-u003"]["line_start"] - 1
    by_local["o012-fom-u003"]["line_end"] = by_local["o012-fom-u003-mastery"]["line_start"] - 1
    by_local["o012-fom-u003-s05"]["line_end"] = by_local["o012-fom-u003-source-corrections"]["line_start"] - 1
    by_local["o012-fom-u003-source-corrections"]["line_end"] = by_local["o012-fom-u003-s06"]["line_start"] - 1
    by_local["o012-fom-u003-s06"]["line_end"] = by_local["o012-fom-u003-mastery"]["line_start"] - 1
    by_local["o012-fom-u003-mastery"]["line_end"] = boundary_start - 1

    nodes.sort(key=lambda item: (item["line_start"], 0 if item["kind"] == "heading" else 1))
    ids = [node["id"] for node in nodes]
    classes = Counter(node["kind"] for node in nodes)
    if len(ids) != 125 or len(set(ids)) != 125 or dict(sorted(classes.items())) != EXPECTED_CLASSES:
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
        raise SystemExit("Fomberg Unit 003 upstream span mismatch")
    if lines[NEXT_SOURCE_LINE - 1].strip() != NEXT_HEADING:
        raise SystemExit("Fomberg Unit 003 next-source cursor mismatch")


def verify_assets() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    reader = SOURCE.read_text(encoding="utf-8")
    base = "source/id-ID/fomberg/assets/unit-003"
    for filename, size, sha, media, figure_suffix in ASSET_SPECS:
        relative = f"{base}/{filename}"
        raw = require_identity(relative, (size, sha))
        if media == "image/png":
            if not raw.startswith(b"\x89PNG\r\n\x1a\n"):
                raise SystemExit(f"invalid PNG signature: {relative}")
            link = f"../assets/unit-003/{filename}"
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
    selected_adverse = [row for row in adverse if 457 <= int(row["event_id"].rsplit("-", 1)[1]) <= 498]
    selected_terms = [row for row in terms if 401 <= int(row["term_id"].rsplit("-", 1)[1]) <= 415]
    if [row["event_id"] for row in selected_adverse] != [f"O012-ADV-{n:04d}" for n in range(457, 499)]:
        raise SystemExit("adverse-ledger Unit 003 identity closure mismatch")
    allowed = {
        "clarified_in_translation", "corrected_in_translation",
        "hypothesis_repaired_in_translation", "pending_future_unit",
        "proof_completed_in_translation", "resolved_before_admission",
    }
    if any(row["status"] not in allowed for row in selected_adverse):
        raise SystemExit("adverse-ledger Unit 003 status mismatch")
    pending = [row["event_id"] for row in selected_adverse if row["status"] == "pending_future_unit"]
    if pending != ["O012-ADV-0460"]:
        raise SystemExit(f"unexpected Unit 003 pending obligations: {pending}")
    if [row["term_id"] for row in selected_terms] != [f"O012-TERM-{n:04d}" for n in range(401, 416)]:
        raise SystemExit("terminology-ledger Unit 003 identity closure mismatch")
    if any(row["status"] != "admitted" for row in selected_terms):
        raise SystemExit("terminology-ledger Unit 003 admission mismatch")
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
        raise SystemExit("Unit 003 sealed-input inventory mismatch")
    verify_upstream()
    lines, nodes = parse_reader()
    assets = verify_assets()
    adverse, terms = read_controls(identities)
    evidence: dict[str, tuple[bytes, dict[str, Any]]] = {
        path: _load_json(path, identities[path]) for path in EVIDENCE_PATHS
    }
    audit = evidence[AUDIT_PATH][1]
    qa = evidence[QA_PATH][1]
    reviews = {slot: evidence[path][1] for slot, path in REVIEW_PATHS.items()}
    for slot, review in reviews.items():
        if not _zero_review(review) or SOURCE_IDENTITY[2] not in json.dumps(review):
            raise SystemExit(f"final {slot} review PASS/reader binding mismatch")
    reconciliation = evidence[RECONCILIATION_PATH][1]
    recount = reconciliation.get("independent_recomputation", {})
    audit_repair = audit.get("proof_closure", {}).get("FOM-PR-04", {})
    if (
        reconciliation.get("status")
            != "PASS_RECOMPUTED_COUNT_SUPERSEDES_REVIEW_COUNT_FIELD_ONLY"
        or reconciliation.get("reader", {}).get("sha256") != SOURCE_IDENTITY[2]
        or reconciliation.get("review", {}).get("sha256")
            != SEALED_IDENTITIES[REVIEW_PATHS["integrated"]][1]
        or recount.get("stable_ids_total") != 125
        or recount.get("stable_ids_unique") != 125
        or recount.get("duplicates") != 0
    ):
        raise SystemExit("integrated-review count reconciliation mismatch")
    if (
        audit.get("schema_version") != "1.0.0"
        or audit.get("audit_id") != "O012-FOMBERG-UNIT-003-SOURCE-AUDIT"
        or audit.get("status") != "PASS"
        or audit.get("reader", {}).get("sha256") != SOURCE_IDENTITY[2]
        or audit.get("unit", {}).get("sha256_preserving_lf") != SPAN_IDENTITY[4]
        or audit.get("unit", {}).get("next_line") != NEXT_SOURCE_LINE
        or audit.get("reader_structure", {}).get("stable_id_count") != 125
        or audit.get("reader_structure", {}).get("class_counts") != EXPECTED_CLASSES
        or audit.get("source_counts", {}).get("semantic_environments_total") != 39
        or audit.get("source_counts", {}).get("diagrams_total") != 29
        or audit.get("mastery", {}).get("triples") != 6
        or audit_repair.get("omission_id") != "o012-fom-u003-omission-pr04"
        or audit_repair.get("proof_id") != "o012-fom-u003-proof-long-exact-repair"
        or audit_repair.get("proof_status") != "complete_original_repair"
        or audit.get("record_plan", {}).get("records_by_file") != DELTA
        or audit.get("record_plan", {}).get("records_planned") != sum(DELTA.values())
        or not audit.get("checks")
        or not all(value is True for value in audit["checks"].values())
    ):
        raise SystemExit("Unit 003 source-audit semantic binding mismatch")
    qa_repair = qa.get("proof_closure", {}).get("FOM-PR-04")
    qa_repair_status = (
        qa_repair.get("proof_status", qa_repair.get("status"))
        if isinstance(qa_repair, dict) else qa_repair
    )
    if (
        qa.get("schema_version") != "1.0.0"
        or qa.get("qa_id") != "O012-FOMBERG-UNIT-003-STATIC-QA"
        or qa.get("status") != "PASS"
        or qa.get("reader", {}).get("sha256") != SOURCE_IDENTITY[2]
        or qa.get("authority", {}).get("unit_span", {}).get("sha256") != SPAN_IDENTITY[4]
        or qa.get("authority", {}).get("next_source_line") != NEXT_SOURCE_LINE
        or qa.get("structure", {}).get("stable_id_count") != 125
        or qa.get("structure", {}).get("class_counts") != EXPECTED_CLASSES
        or qa.get("mastery", {}).get("triples") != 6
        or qa_repair_status != "complete_original_repair"
        or qa.get("record_plan", {}).get("records_by_file") != DELTA
        or qa.get("record_plan", {}).get("records_planned") != sum(DELTA.values())
        or not qa.get("checks")
        or not all(value is True for value in qa["checks"].values())
    ):
        raise SystemExit("Unit 003 static-QA semantic binding mismatch")
    audit_raw = evidence[AUDIT_PATH][0]
    audit_binding = qa.get("source_audit_output", {})
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
            if f"o012-fom-u003-{kind}-{number:03d}" not in ids:
                raise SystemExit(f"mastery triple {number} incomplete")
    required_text = (
        "FOM-PR-04",
        r"g_\#-f_\#",
        "o012-fom-u003-proof-long-exact-repair",
        "o012-fom-u003-proof-pointed-degree-zero",
        "o012-fom-u002-thm-homotopy-invariance",
    )
    joined = "\n".join(lines)
    if any(marker not in joined for marker in required_text):
        raise SystemExit("required Unit 003 mathematical/provenance marker missing")
    terms_by_id = {row["term_id"]: row for row in terms}
    for _, control_id, evidence_suffix in TERM_SPECS:
        node = node_by_id[f"o012-fom-u003-{evidence_suffix}"]
        evidence_text = "\n".join(lines[node["line_start"] - 1:node["line_end"]]).casefold()
        preferred_present = terms_by_id[control_id]["id_ID"].casefold() in evidence_text
        if control_id == "O012-TERM-0414":
            preferred_present = preferred_present or (
                "batas" in evidence_text and "cakram" in evidence_text
            )
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
        "reviews": reviews,
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
        start, end = map(int, source_range.split("-"))
        return {
            "path": "algebraic_topology.tex",
            "commit_sha": COMMIT,
            "line_start": start,
            "line_end": end,
            "precision": "exact_source_span",
        }
    return {"kind": "edition_original", "path": SOURCE_PATH, "precision": "exact_target_span"}


def clean_title(title: str, kind: str) -> str:
    value = re.sub(r"\*\*", "", title).strip()
    return value[:240] if value else kind


def parentage(nodes: list[dict[str, Any]]) -> dict[str, tuple[str, int, list[str]]]:
    by_local = {node["id"]: node for node in nodes}
    sections = (
        "o012-fom-u003-s05",
        "o012-fom-u003-source-corrections",
        "o012-fom-u003-s06",
        "o012-fom-u003-mastery",
    )
    raw_parent: dict[str, str] = {
        "o012-fom-u003-notice": ROOT,
        "o012-fom-u003-s05": ROOT,
        "o012-fom-u003-source-corrections": ROOT,
        "o012-fom-u003-s06": ROOT,
        "o012-fom-u003-mastery": ROOT,
        "o012-fom-u003-boundary-001": ROOT,
    }
    for node in nodes:
        ident = node["id"]
        if ident == "o012-fom-u003" or ident in raw_parent:
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
    spec = importlib.util.spec_from_file_location("o012_generic_fom003", path)
    if spec is None or spec.loader is None:
        raise SystemExit("cannot load generic backend validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _correction_targets(row: dict[str, str], node_ids: set[str]) -> list[str]:
    targets = sorted(set(re.findall(r'#(o012-fom-u003(?:-[A-Za-z0-9-]+)?)', row["source_location"])))
    if not targets and row["event_id"] == "O012-ADV-0498":
        targets = ["o012-fom-u003-notice"]
    if not targets or any(target not in node_ids for target in targets):
        raise SystemExit(f"adverse row target resolution failed: {row['event_id']}")
    return targets


def build_additions(data: dict[str, Any], evidence_identities: dict[str, tuple[int, str]]) -> dict[str, list[dict[str, Any]]]:
    lines: list[str] = data["lines"]
    nodes: list[dict[str, Any]] = data["nodes"]
    additions: dict[str, list[dict[str, Any]]] = {name: [] for name in FILES}
    all_concepts = [
        "concept:exact-sequence", "concept:long-exact-sequence",
        "concept:singular-homology", "concept:reduced-homology",
        "concept:chain-map", "concept:chain-homotopy",
        *[f"concept:{slug}" for slug, _, _ in TERM_SPECS],
    ]

    def add(name: str, record: dict[str, Any]) -> None:
        additions[name].append(record)

    for ident, attribution, change, third in (
        (
            COMPANION_RIGHTS,
            "Original Indonesian mastery, solutions, proof repairs, source audits, and accessible redraws for Fomberg Unit 003.",
            "Original additions and redraws are distinguished from the Fomberg source component.",
            "Original Unit 003 companion layer; source content remains separately attributed.",
        ),
        (
            COMPOSITE_RIGHTS,
            "Fomberg source adaptation plus original Indonesian Unit 003 companion layer.",
            "Integrated reader preserves exact locators, change notices, proof-repair identity, and per-asset provenance.",
            "Composite Unit 003; component-scoped rights records control.",
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
            evidence_segment_id=f"segment:o012-fom-u003-{evidence_suffix}",
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
    source_headings = {"o012-fom-u003-s05", "o012-fom-u003-s06"}
    source_kinds = {
        "definition", "remark", "example", "theorem", "corollary",
        "proposition", "proof", "figure", "source-omission",
    }
    for node in nodes:
        ident = node["id"]
        uid = f"unit:{ident}"
        kind = node["kind"]
        attrs = node["attrs"]
        is_root = ident == "o012-fom-u003"
        source_range = attrs.get("data-source-lines")
        explicit_original = attrs.get("data-origin") == "edition-original"
        is_source = not explicit_original and (
            ident in source_headings or (kind in source_kinds and source_range is not None)
        )
        if is_root:
            rights = COMPOSITE_RIGHTS
            provenance = "composite_translated_and_original"
            parent = COURSE
            order = 33
            path = [ROOT]
            display = "Topologi Aljabar — Komponen Fomberg Unit 003: Barisan Eksak dan Homologi Relatif"
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
                edition_order=3,
                route_order=10,
                source_locator={
                    "path": "algebraic_topology.tex", "commit_sha": COMMIT,
                    "line_start": 1291, "line_end": 1922,
                    "precision": "exact_unit_span", "span_bytes": 24270,
                    "span_sha256": SPAN_IDENTITY[4],
                },
            )
        alias = attrs.get("data-source-label")
        if alias:
            unit["source_aliases"] = [alias]
        repair_id = attrs.get("data-repair-id")
        if repair_id:
            unit["repair_id"] = repair_id
            unit["proof_status"] = (
                "complete_original_repair"
                if ident == "o012-fom-u003-proof-long-exact-repair"
                else attrs.get("data-proof-status", "forward_proof_obligation")
                if ident == "o012-fom-u003-forward-quotient-les"
                else "source_omission_named" if kind == "source-omission"
                else attrs.get("data-proof-status", "repair_support")
            )
        if ident == "o012-fom-u003-thm-long-exact":
            unit.update(repair_id="FOM-PR-04", proof_status="statement_with_complete_repaired_proof")
        if kind == "solution":
            unit["solution_status"] = "complete_checked_solution"
        add("units.jsonl", unit)

        if is_root:
            segment_rights = COMPOSITE_RIGHTS
            segment_provenance = "composite_translated_and_original"
            segment_locator = target_locator(lines, node["line_start"], node["line_end"])
            segment_source_locator = {
                "path": "algebraic_topology.tex", "commit_sha": COMMIT,
                "line_start": 1291, "line_end": 1922,
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
    source_asset = common("asset", "asset:o012-fom-u003-source-markdown")
    source_asset.update(
        bytes=source_size, edition_id=EDITION,
        media_type="text/markdown; charset=utf-8", path=SOURCE_PATH,
        resource_id=RESOURCE, rights_component_id=COMPOSITE_RIGHTS,
        role="canonical_reader_source", sha256=source_sha, unit_id=ROOT,
    )
    add("assets.jsonl", source_asset)
    figures = [node for node in nodes if node["kind"] == "figure"]
    diagram_asset = common("asset", "asset:o012-fom-u003-semantic-diagram-layer")
    diagram_asset.update(
        bytes=source_size, edition_id=EDITION,
        media_type="text/markdown; charset=utf-8", path=SOURCE_PATH,
        resource_id=RESOURCE, rights_component_id=COMPOSITE_RIGHTS,
        role="semantic_diagram_accessibility_layer", sha256=source_sha,
        source_diagram_count=29, semantic_figure_block_count=26,
        geometric_redraw_count=6,
        semantic_unit_ids=[f"unit:{node['id']}" for node in figures],
        unit_id=ROOT,
    )
    add("assets.jsonl", diagram_asset)
    for asset in data["assets"]:
        slug = asset["filename"].replace(".", "-")
        rec = common("asset", f"asset:o012-fom-u003-{slug}")
        rec.update(
            bytes=asset["bytes"], edition_id=EDITION,
            media_type=asset["media_type"], path=asset["path"],
            resource_id=RESOURCE, rights_component_id=COMPANION_RIGHTS,
            role=("reader_linked_accessible_redraw" if asset["media_type"] == "image/png" else "accessible_vector_source_companion"),
            sha256=asset["sha256"],
            source_figure_unit_id=f"unit:o012-fom-u003-{asset['figure_suffix']}",
            unit_id=ROOT,
        )
        add("assets.jsonl", rec)

    artifact_specs = (
        ("artifact:o012-fom-u003-source-audit", AUDIT_PATH, ["qa:o012-fom-u003-source-integrity"], "source_frozen"),
        ("artifact:o012-fom-u003-review-exact", REVIEW_PATHS["exact"], ["qa:o012-fom-u003-math", "qa:o012-fom-u003-language"], "mathematically_reviewed"),
        ("artifact:o012-fom-u003-review-relative", REVIEW_PATHS["relative"], ["qa:o012-fom-u003-math", "qa:o012-fom-u003-language"], "mathematically_reviewed"),
        ("artifact:o012-fom-u003-review-integrated", REVIEW_PATHS["integrated"], ["qa:o012-fom-u003-math", "qa:o012-fom-u003-language"], "mathematically_reviewed"),
        ("artifact:o012-fom-u003-review-count-reconciliation", RECONCILIATION_PATH, ["qa:o012-fom-u003-source-integrity"], "structurally_verified"),
        ("artifact:o012-fom-u003-qa", QA_PATH, ["qa:o012-fom-u003-source-integrity", "qa:o012-fom-u003-mastery"], "built"),
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
                "Fomberg Unit 003 evidence; algebraic_topology.tex:1291-1922; "
                f"{SPAN_IDENTITY[4]}; {MODEL}; route D60-R10; semantic admission only."
            ),
            translation_state=state, unit_id=ROOT,
        )
        add("artifacts.jsonl", rec)

    for ident, kind, note, witnesses in (
        (
            "qa:o012-fom-u003-source-integrity", "source",
            "Exact lines 1291-1922, cursor 1923, 125 stable IDs, 29 source diagram functions, 26 semantic figure blocks, and twelve redraw files passed.",
            ["artifact:o012-fom-u003-source-audit", "artifact:o012-fom-u003-review-count-reconciliation", "artifact:o012-fom-u003-qa"],
        ),
        (
            "qa:o012-fom-u003-math", "math",
            "Three final independent reviews passed P1=P2=P3=0; FOM-PR-04 is complete and degree-zero edge cases are closed.",
            ["artifact:o012-fom-u003-review-exact", "artifact:o012-fom-u003-review-relative", "artifact:o012-fom-u003-review-integrated"],
        ),
        (
            "qa:o012-fom-u003-language", "language",
            "Final Indonesian reviews passed after terminology, provenance, notation, and source-order repairs.",
            ["artifact:o012-fom-u003-review-exact", "artifact:o012-fom-u003-review-relative", "artifact:o012-fom-u003-review-integrated"],
        ),
        (
            "qa:o012-fom-u003-mastery", "mastery",
            "Six exercises, six hints, and six complete checked solutions passed.",
            ["artifact:o012-fom-u003-qa"],
        ),
    ):
        rec = common("qa_event", ident)
        rec.update(note=note, qa_type=kind, result="passed", unit_id=ROOT, witness_artifact_ids=witnesses)
        add("qa.jsonl", rec)

    node_ids = {node["id"] for node in nodes}
    correction_type = {
        460: "proof_completion", 461: "proof_completion", 462: "mathematical_correction",
        470: "mathematical_correction", 473: "proof_completion",
        479: "mathematical_correction", 484: "proof_completion",
        486: "proof_completion", 490: "mathematical_correction",
        491: "mathematical_correction", 492: "mathematical_correction",
        493: "diagram_fidelity", 494: "provenance_correction",
        495: "language_correction", 496: "mathematical_correction",
        497: "language_correction", 498: "provenance_correction",
    }
    for row in data["adverse"]:
        number = int(row["event_id"].rsplit("-", 1)[1])
        targets = _correction_targets(row, node_ids)
        rec = common("correction", f"correction:o012-fom-u003-adv-{number:04d}")
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

    relation("relation:adapts:o012-fom-u003:fomberg-edition", ROOT, EDITION, "adapts", "Indonesian Unit 003 adapts exact Fomberg lines 1291-1922.")
    relation("relation:contains:o012-d60:fomberg-u003", COURSE, ROOT, "contains", "Course route D60-R10 contains Fomberg Unit 003.", course_route_unit_id=ROUTE)
    relation("relation:precedes:o012-fom-u002:o012-fom-u003", "unit:o012-fom-u002", ROOT, "precedes", "Fomberg Unit 002 precedes Unit 003 in source order.")
    relation("relation:contains:o012-d60-rights:fomberg-u003", ROUTE_RIGHTS, ROOT, "contains", "Integrated-route rights contain the Fomberg Unit 003 composite.")
    relation("relation:precedes:o012-fom-u003:mastery", ROOT, "unit:o012-fom-u003-mastery", "precedes", "Translated source body and repair dossier precede the solved mastery layer.")
    relation(
        "relation:proves:o012-fom-u003-pr04:thm-long-exact",
        "unit:o012-fom-u003-proof-long-exact-repair",
        "unit:o012-fom-u003-thm-long-exact",
        "proves", "Complete original repair FOM-PR-04 closes construction, well-definedness, additivity, and exactness.", repair_id="FOM-PR-04",
    )
    for number in range(1, 7):
        relation(
            f"relation:hints:fom-u003-hint-{number:03d}:mcheck-{number:03d}",
            f"unit:o012-fom-u003-hint-{number:03d}",
            f"unit:o012-fom-u003-mcheck-{number:03d}", "hints",
            f"Hint for Fomberg Unit 003 mastery check {number}.",
        )
        relation(
            f"relation:solves:fom-u003-sol-{number:03d}:mcheck-{number:03d}",
            f"unit:o012-fom-u003-sol-{number:03d}",
            f"unit:o012-fom-u003-mcheck-{number:03d}", "solves",
            f"Complete checked solution for Unit 003 mastery check {number}.",
        )
    for number, node in enumerate(figures, 1):
        relation(
            f"relation:illustrates:fom-u003-fig-{number:03d}:diagram-layer",
            f"unit:{node['id']}", "asset:o012-fom-u003-semantic-diagram-layer",
            "illustrates", f"Semantic figure block {number} preserves its source diagram function.",
        )
    png_by_figure = {
        asset["figure_suffix"]: asset for asset in data["assets"]
        if asset["media_type"] == "image/png"
    }
    for suffix, asset in sorted(png_by_figure.items()):
        png_id = f"asset:o012-fom-u003-{asset['filename'].replace('.', '-')}"
        svg_name = asset["filename"].removesuffix(".png") + ".svg"
        svg_id = f"asset:o012-fom-u003-{svg_name.replace('.', '-')}"
        relation(
            f"relation:illustrates:o012-fom-u003-{suffix}:{asset['filename'].removesuffix('.png')}",
            f"unit:o012-fom-u003-{suffix}", png_id, "illustrates",
            "Reader-linked PNG is the raster rendering of the independently authored accessible redraw.",
        )
        relation(
            f"relation:xref:{asset['filename'].removesuffix('.png')}:svg-source",
            png_id, svg_id, "xref", "PNG redraw has this accessible SVG source companion.",
        )
    relation(
        "relation:xref:o012-fom-u003-relative-induced-map:u002-homotopy-invariance",
        "unit:o012-fom-u003-rem-relative-induced-map",
        "unit:o012-fom-u002-thm-homotopy-invariance", "xref",
        "Relative pair-homotopy argument invokes the preceding singular-homology invariance theorem.",
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
        raise SystemExit("Unit 003 control ledgers must be sealed before planning")
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
        "stable_ids": 125,
        "asset_records": 14,
        "real_redraw_files": 12,
        "artifact_evidence_paths_in_record_order": artifact_paths,
        "unsealed_identity_paths": [path for path, value in SEALED_IDENTITIES.items() if value is None],
    }
