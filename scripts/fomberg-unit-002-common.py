#!/usr/bin/env python3
"""Frozen inputs and deterministic backend records for Fomberg Unit 002."""
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
STAMP = "2026-08-24T00:00:00Z"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"

SOURCE_PATH = (
    "source/id-ID/fomberg/units/"
    "fomberg-unit-002-singular-homology-homotopy-invariance.md"
)
SOURCE = LANE / SOURCE_PATH
SOURCE_IDENTITY = (
    44407,
    1342,
    "0851ab7d9f5ded1e836a0e73aa055fbd28b82998208d8136ec0cf4757747435c",
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
    615,
    1290,
    676,
    22924,
    "9b28e159825e020b262a51b9c50372b2fafc26270fab6480d860aaaeefdda84f",
)
NEXT_SOURCE_LINE = 1291
NEXT_HEADING = r"\subsection{Exact sequences}"
COMMIT = "563194fae879178b9a6871b249513bfc27968975"
TREE = "fb678966d1533d529bdd72f49d8496a3bdc14a9b"
RESOURCE = "resource:fomberg-algebraic-topology-2025"
EDITION = "edition:fomberg-at-2025-563194f"
ROOT = "unit:o012-fom-u002"
PROGRAM = "program:o012-id"
COURSE = "course:o012-d60"
ROUTE = "D60-R09"

SOURCE_RIGHTS = "rights:fomberg-cc-by-sa-4.0"
COMPANION_RIGHTS = "rights:o012-fom-u002-companion-cc-by-sa-4.0"
COMPOSITE_RIGHTS = "rights:o012-fom-u002-composite-cc-by-sa-4.0"
ROUTE_RIGHTS = "rights:o012-d60-integrated-route-cc-by-sa-4.0"

PREFIX = {
    "artifacts.jsonl": (166, 133601, "e1cc3611df5e84e465846d64623af7107709d93681049bcdae5ad01b314bc41f"),
    "assets.jsonl": (37, 23720, "a9cc6a83e0e7c771044f0984fefb32f3c0ee409b428bb626b043f6bff7264367"),
    "authority.jsonl": (6, 4374, "84c622f56dbbd5ba379361245ecfe07bc79c9f4fd6b18ba21b82b5f545211869"),
    "concepts.jsonl": (392, 123698, "e83c6047f4f934044bff8bb1a057d2db2ef4d878fad6a6ce9a54d1c490a194bf"),
    "corrections.jsonl": (425, 416934, "f0a124da975557b3871e5ce8fbe7226c595ff06a3357b4c5f8e13352e7038c54"),
    "qa.jsonl": (138, 77180, "98449c7de7856384cced4d4ed0bd5c0c01ea0bf7b292f679ba52ae8ccac83ce0"),
    "relations.jsonl": (564, 232018, "01047e8dd954fcbc0f8fbefaf8ae78415f1278d601de3ec733f4c20c9e895101"),
    "rights.jsonl": (91, 83493, "e81261979962c93827e0199126b7164dda25063f2700918697dc9ede54517053"),
    "segments.jsonl": (1413, 2094230, "6a6789c021494f6099c1e1b5b59edd9045fb08688b3ececda5d2f53000fb5a8c"),
    "terms.jsonl": (385, 246829, "c29a3f45f4e29b6741dc2fe6b70ea421f1edf1000a50e276d544aa731045fc8d"),
    "units.jsonl": (1443, 2222571, "ba9a464c3eb2ba995eca5b78e870c2d57f58896b86f94b54b40f8538106b954c"),
}
PREFIX_TOTAL = (
    5060,
    5658648,
    "17f57575a062025e434e79f7f3797d05de1a41e520202521ae39a409d4b6450d",
)

EXPECTED_CLASSES = {
    "heading": 5, "definition": 6, "remark": 12, "edition-note": 1,
    "source-audit": 6, "lemma": 3, "proof": 14, "figure": 14,
    "corollary": 7, "proposition": 3, "source-omission": 3,
    "theorem": 1, "example": 1, "exercise": 6, "hint": 6,
    "solution": 6, "boundary": 1,
}
DELTA = {
    "artifacts.jsonl": 5,
    "assets.jsonl": 2,
    "authority.jsonl": 0,
    "concepts.jsonl": 7,
    "corrections.jsonl": 31,
    "qa.jsonl": 4,
    "relations.jsonl": 34,
    "rights.jsonl": 2,
    "segments.jsonl": 95,
    "terms.jsonl": 7,
    "units.jsonl": 95,
}

ALIASES = {
    "lem:path-connected-then-hzero-z": "o012-fom-u002-lem-hzero",
    "prp:functoriality-of-induced-maps": "o012-fom-u002-prop-functoriality",
    "cor:injective-i-surjective-r": "o012-fom-u002-cor-retract",
    "thm:homotopic-maps-induce-same-homomorphism-on-homology":
        "o012-fom-u002-thm-homotopy-invariance",
    "cor:homotopy-equivalent-implies-same-homology":
        "o012-fom-u002-cor-homotopy-equivalent",
}

TERM_SPECS = (
    ("singular-chain", "O012-TERM-0394", "rem-augmented-complex"),
    ("singular-chain-complex", "O012-TERM-0395", "rem-augmented-complex"),
    ("chain-map", "O012-TERM-0396", "def-chain-map"),
    ("induced-map", "O012-TERM-0397", "prop-functoriality"),
    ("augmented-chain-complex", "O012-TERM-0398", "rem-augmented-complex"),
    ("reduced-homology", "O012-TERM-0399", "def-reduced-homology"),
    ("chain-homotopy", "O012-TERM-0400", "proof-homotopy-invariance"),
)

CORRECTION_TARGETS = {
    426: ("rem-singular-chains", "audit-chain-group"),
    427: ("rem-singular-chains",),
    428: ("lem-components", "proof-components", "cor-path-components", "audit-components"),
    429: ("proof-hzero-first",),
    430: ("proof-hzero-augmentation",),
    431: ("rem-augmented-complex", "def-reduced-homology", "rem-empty-simplex"),
    432: ("rem-reduced-splitting", "audit-reduced-splitting"),
    433: ("rem-geometric", "fig-flow-balance", "audit-geometric-heuristic"),
    434: ("prop-chain-map", "omission-pr01", "proof-chain-map"),
    435: ("prop-induced-map", "proof-induced-map-source", "omission-pr02",
          "proof-induced-map-homomorphism"),
    436: ("prop-functoriality", "proof-functoriality"),
    437: ("proof-endpoints-not-retract",),
    438: ("cor-homotopy-equivalent", "omission-pr03", "proof-homotopy-equivalent"),
    439: ("exa-euclidean", "audit-euclidean-map"),
    440: ("proof-homotopy-invariance",),
    441: ("proof-homotopy-invariance", "audit-prism-indices"),
    442: ("cor-contractible",),
    443: ("proof-point",),
    444: ("lem-components", "proof-components", "cor-path-components", "audit-components"),
    445: ("rem-singular-chains", "proof-point", "proof-components",
          "proof-hzero-first", "proof-hzero-augmentation"),
    446: ("rem-geometric", "fig-flow-balance", "audit-geometric-heuristic"),
    447: ("sol-001", "sol-002", "sol-006"),
    448: ("proof-homotopy-invariance", "fig-chain-homotopy"),
    449: ("proof-hzero-first",),
    450: (
        "rem-homeomorphism", "prop-functoriality", "proof-homeomorphism",
        "proof-retract", "proof-homotopy-equivalent", "mastery", "hint-005",
        "sol-005", "proof-hzero-augmentation", "rem-reduced-splitting",
        "prop-chain-map", "def-chain-map", "hint-003", "sol-003",
        "proof-homotopy-invariance", "audit-geometric-heuristic",
    ),
    451: ("def-singular-simplex", "note-boundary-square", "omission-pr02"),
    452: ("fig-retract-spaces", "fig-retract-homology", "fig-chain-homotopy",
          "fig-composition", "fig-homotopy-prism", "fig-flow-balance"),
    453: ("sol-003",),
    454: ("hint-001",),
    455: ("sol-002",),
    456: ("proof-contractible",),
}


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canon(obj: dict[str, Any]) -> bytes:
    return json.dumps(
        obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8") + b"\n"


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


def verify_prefix(backend: Path = BACKEND) -> tuple[dict[str, bytes], list[dict[str, Any]]]:
    prefix: dict[str, bytes] = {}
    records: list[dict[str, Any]] = []
    seen: set[str] = set()
    bundle = hashlib.sha256()
    for name in FILES:
        raw = (backend / name).read_bytes()
        count, size, sha = PREFIX[name]
        if (len(raw.splitlines()), len(raw), digest(raw)) != (count, size, sha):
            raise SystemExit(f"{name}: immutable Unit 001 boundary mismatch")
        if b"\r" in raw or not raw.endswith(b"\n"):
            raise SystemExit(f"{name}: invalid LF discipline")
        for number, line in enumerate(raw.splitlines(keepends=True), 1):
            obj = json.loads(line.decode("utf-8"))
            if canon(obj) != line or obj["id"] in seen:
                raise SystemExit(f"{name}:{number}: noncanonical or duplicate prefix")
            seen.add(obj["id"])
            records.append(obj)
        prefix[name] = raw
        bundle.update(name.encode())
        bundle.update(b"\0")
        bundle.update(raw)
    observed_total = (
        len(records), sum(map(len, prefix.values())), bundle.hexdigest()
    )
    if observed_total != PREFIX_TOTAL:
        raise SystemExit(
            f"immutable Unit 001 bundle identity mismatch: {observed_total!r}"
        )
    return prefix, records


def _attrs(text: str) -> dict[str, str]:
    return {
        match.group(1): match.group(2)
        for match in re.finditer(r'(data-[a-z-]+)="([^"]*)"', text)
    }


def parse_reader() -> tuple[list[str], list[dict[str, Any]]]:
    raw = SOURCE.read_bytes()
    if (len(raw), raw.count(b"\n"), digest(raw)) != SOURCE_IDENTITY:
        raise SystemExit("Fomberg Unit 002 reader identity mismatch")
    if raw.startswith(b"\xef\xbb\xbf") or b"\r" in raw or not raw.endswith(b"\n"):
        raise SystemExit("reader must be UTF-8 without BOM and LF-only")
    text = raw.decode("utf-8")
    if "\ufffd" in text or text.count(MODEL) != 1:
        raise SystemExit("reader encoding/model-provenance mismatch")
    lines = text.splitlines()
    nodes: list[dict[str, Any]] = []
    heading_re = re.compile(r'^(#{1,6})\s+(.*?)\s*\{([^}]*)\}\s*$')
    for number, line in enumerate(lines, 1):
        match = heading_re.match(line)
        if not match:
            continue
        ident = re.search(r'#(o012-fom-u002(?:-[A-Za-z0-9-]+)?)', match.group(3))
        if ident:
            nodes.append({
                "id": ident.group(1), "kind": "heading", "line_start": number,
                "level": len(match.group(1)), "title": match.group(2),
                "attrs": _attrs(match.group(3)), "opener_end": number,
                "enclosing_div": None,
            })

    stack: list[dict[str, Any] | None] = []
    number = 1
    while number <= len(lines):
        stripped = lines[number - 1].strip()
        if stripped.startswith(":::") and stripped != ":::":
            opener_start = number
            opener = [lines[number - 1]]
            while "}" not in opener[-1] and number < len(lines):
                number += 1
                opener.append(lines[number - 1])
            joined = " ".join(opener)
            ident = re.search(r'#(o012-fom-u002(?:-[A-Za-z0-9-]+)?)', joined)
            kind = re.match(r'^:::\s*\{\.([^\s}]+)', opener[0].strip())
            node = None
            if ident and kind:
                enclosing = next(
                    (item["id"] for item in reversed(stack) if item is not None),
                    None,
                )
                node = {
                    "id": ident.group(1), "kind": kind.group(1),
                    "line_start": opener_start, "opener_end": number,
                    "attrs": _attrs(joined), "enclosing_div": enclosing,
                }
            stack.append(node)
        elif stripped == ":::":
            if not stack:
                raise SystemExit(f"unexpected fenced-div close at line {number}")
            node = stack.pop()
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
    required_headings = [
        "o012-fom-u002-notice", "o012-fom-u002", "o012-fom-u002-s03",
        "o012-fom-u002-s04", "o012-fom-u002-mastery",
    ]
    if any(ident not in by_local for ident in required_headings):
        raise SystemExit("reader heading set incomplete")
    boundary_start = by_local["o012-fom-u002-boundary-001"]["line_start"]
    by_local["o012-fom-u002-notice"]["line_end"] = by_local["o012-fom-u002"]["line_start"] - 1
    by_local["o012-fom-u002"]["line_end"] = by_local["o012-fom-u002-mastery"]["line_start"] - 1
    by_local["o012-fom-u002-s03"]["line_end"] = by_local["o012-fom-u002-s04"]["line_start"] - 1
    by_local["o012-fom-u002-s04"]["line_end"] = by_local["o012-fom-u002-mastery"]["line_start"] - 1
    by_local["o012-fom-u002-mastery"]["line_end"] = boundary_start - 1

    nodes.sort(key=lambda item: (
        item["line_start"], 0 if item["kind"] == "heading" else 1
    ))
    ids = [node["id"] for node in nodes]
    classes = Counter(node["kind"] for node in nodes)
    if len(ids) != 95 or len(set(ids)) != 95 or dict(classes) != EXPECTED_CLASSES:
        raise SystemExit(
            f"reader stable-ID/class census mismatch: {len(ids)}, {dict(classes)}"
        )
    if [node["id"] for node in nodes if node["kind"] == "heading"] != required_headings:
        raise SystemExit("reader heading identity/order mismatch")
    actual_aliases = {
        node["attrs"]["data-source-label"]: node["id"]
        for node in nodes if "data-source-label" in node["attrs"]
    }
    if actual_aliases != ALIASES:
        raise SystemExit(f"source alias mismatch: {actual_aliases}")
    return lines, nodes


def verify_upstream() -> None:
    raw = UPSTREAM.read_bytes()
    if (len(raw), raw.count(b"\n"), digest(raw)) != UPSTREAM_IDENTITY:
        raise SystemExit("frozen Fomberg authoring source mismatch")
    lines = raw.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n").splitlines()
    start, end, line_count, size, sha = SPAN_IDENTITY
    span = ("\n".join(lines[start - 1:end]) + "\n").encode("utf-8")
    if (len(span.splitlines()), len(span), digest(span)) != (line_count, size, sha):
        raise SystemExit("Fomberg Unit 002 upstream span mismatch")
    if lines[NEXT_SOURCE_LINE - 1].strip() != NEXT_HEADING:
        raise SystemExit("Fomberg Unit 002 next-source cursor mismatch")


def read_controls() -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    adverse = list(csv.DictReader(
        (LANE / "00_control/ADVERSE_LEDGER.csv").read_text(
            encoding="utf-8"
        ).splitlines()
    ))
    terms = list(csv.DictReader(
        (LANE / "00_control/TERMINOLOGY.csv").read_text(
            encoding="utf-8"
        ).splitlines()
    ))
    selected_adverse = [
        row for row in adverse
        if 426 <= int(row["event_id"].rsplit("-", 1)[1]) <= 456
    ]
    selected_terms = [
        row for row in terms
        if 394 <= int(row["term_id"].rsplit("-", 1)[1]) <= 400
    ]
    if (
        [row["event_id"] for row in selected_adverse]
        != [f"O012-ADV-{number:04d}" for number in range(426, 457)]
        or any(
            row["status"] not in {
                "corrected_in_translation", "proof_completed_in_translation",
                "clarified_in_translation", "resolved_before_admission",
            }
            for row in selected_adverse
        )
    ):
        raise SystemExit("adverse-ledger Unit 002 closure mismatch")
    if (
        [row["term_id"] for row in selected_terms]
        != [f"O012-TERM-{number:04d}" for number in range(394, 401)]
        or any(row["status"] != "admitted" for row in selected_terms)
    ):
        raise SystemExit("terminology-ledger Unit 002 closure mismatch")
    return selected_adverse, selected_terms


def verify_all_inputs(evidence_identities: dict[str, tuple[int, str]]) -> dict[str, Any]:
    expected_evidence = {
        "qa/FOMBERG_UNIT_002_SOURCE_AUDIT.json",
        "qa/FOMBERG_UNIT_002_QA.json",
        "qa/FOMBERG_UNIT_002_REVIEW_PART_A_DRAFT.md",
        "qa/FOMBERG_UNIT_002_REVIEW_PART_B_DRAFT.md",
        "qa/FOMBERG_UNIT_002_INDEPENDENT_REVIEW_DRAFT.md",
    }
    if set(evidence_identities) != expected_evidence:
        raise SystemExit("Unit 002 evidence inventory mismatch")
    for relative, expected in evidence_identities.items():
        require_identity(relative, expected)
    verify_upstream()
    lines, nodes = parse_reader()
    adverse, terms = read_controls()

    review_paths = (
        "qa/FOMBERG_UNIT_002_REVIEW_PART_A_DRAFT.md",
        "qa/FOMBERG_UNIT_002_REVIEW_PART_B_DRAFT.md",
        "qa/FOMBERG_UNIT_002_INDEPENDENT_REVIEW_DRAFT.md",
    )
    severity_re = re.compile(
        r'FINAL_SEVERITY_COUNTS.{0,16}'
        r'\{\s*"P1"\s*:\s*0\s*,\s*"P2"\s*:\s*0\s*,\s*"P3"\s*:\s*0\s*\}'
    )
    for relative in review_paths:
        review = (LANE / relative).read_text(encoding="utf-8")
        if (
            SOURCE_IDENTITY[2] not in review
            or "PASS" not in review
            or severity_re.search(review) is None
        ):
            raise SystemExit(f"review semantic PASS binding mismatch: {relative}")

    audit = json.loads(
        (LANE / "qa/FOMBERG_UNIT_002_SOURCE_AUDIT.json").read_text(
            encoding="utf-8"
        )
    )
    qa = json.loads(
        (LANE / "qa/FOMBERG_UNIT_002_QA.json").read_text(encoding="utf-8")
    )
    if (
        audit.get("status") != "PASS"
        or audit.get("audit_id") != "O012-FOMBERG-UNIT-002-SOURCE-AUDIT"
        or audit.get("reader", {}).get("sha256") != SOURCE_IDENTITY[2]
        or audit.get("unit", {}).get("sha256_preserving_lf") != SPAN_IDENTITY[4]
        or audit.get("unit", {}).get("next_line") != NEXT_SOURCE_LINE
        or audit.get("source_counts", {}).get("semantic_environments_total") != 42
        or audit.get("source_counts", {}).get("diagrams_total") != 14
        or audit.get("reader_structure", {}).get("stable_id_count") != 95
        or audit.get("reader_structure", {}).get("semantic_figure_blocks") != 14
        or audit.get("mastery", {}).get("triples") != 6
        or audit.get("record_plan", {}).get("records_by_file") != DELTA
        or audit.get("record_plan", {}).get("records_planned") != sum(DELTA.values())
        or not audit.get("checks")
        or not all(audit["checks"].values())
    ):
        raise SystemExit("Unit 002 source-audit semantic binding mismatch")
    review_bindings = audit.get("independent_reviews", {})
    if (
        set(review_bindings) != {"part_a", "part_b", "integrated"}
        or any(
            item.get("status") != "PASS"
            or item.get("final_severity_counts") != {"P1": 0, "P2": 0, "P3": 0}
            or item.get("reader_sha256") != SOURCE_IDENTITY[2]
            for item in review_bindings.values()
        )
    ):
        raise SystemExit("Unit 002 source-audit review binding mismatch")
    source_audit_raw = (
        LANE / "qa/FOMBERG_UNIT_002_SOURCE_AUDIT.json"
    ).read_bytes()
    if (
        qa.get("status") != "PASS"
        or qa.get("qa_id") != "O012-FOMBERG-UNIT-002-STATIC-QA"
        or qa.get("reader", {}).get("sha256") != SOURCE_IDENTITY[2]
        or qa.get("authority", {}).get("unit_span", {}).get("sha256") != SPAN_IDENTITY[4]
        or qa.get("authority", {}).get("next_source_line") != NEXT_SOURCE_LINE
        or qa.get("source_audit_output", {}).get("bytes") != len(source_audit_raw)
        or qa.get("source_audit_output", {}).get("sha256") != digest(source_audit_raw)
        or qa.get("structure", {}).get("stable_id_count") != 95
        or qa.get("structure", {}).get("semantic_figure_blocks") != 14
        or qa.get("mastery", {}).get("triples") != 6
        or qa.get("controls", {}).get("terminology", {}).get("through") != "O012-TERM-0400"
        or qa.get("controls", {}).get("adverse", {}).get("through") != "O012-ADV-0456"
        or qa.get("record_plan", {}).get("records_by_file") != DELTA
        or qa.get("record_plan", {}).get("records_planned") != sum(DELTA.values())
        or not qa.get("checks")
        or not all(qa["checks"].values())
    ):
        raise SystemExit("Unit 002 static-QA semantic binding mismatch")
    qa_review_bindings = qa.get("independent_reviews", {})
    if (
        set(qa_review_bindings) != {"part_a", "part_b", "integrated"}
        or any(
            item.get("status") != "PASS"
            or item.get("final_severity_counts") != {"P1": 0, "P2": 0, "P3": 0}
            or item.get("reader_sha256") != SOURCE_IDENTITY[2]
            for item in qa_review_bindings.values()
        )
    ):
        raise SystemExit("Unit 002 static-QA review binding mismatch")

    evidence_records = audit.get("evidence_records")
    if not isinstance(evidence_records, list) or len(evidence_records) != 95:
        raise SystemExit("Unit 002 source-audit evidence inventory mismatch")
    evidence_by_local = {
        record.get("stable_id"): record for record in evidence_records
    }
    node_by_local = {node["id"]: node for node in nodes}
    if set(evidence_by_local) != set(node_by_local):
        raise SystemExit("Unit 002 source-audit evidence stable-ID mismatch")
    reader_raw_lines = SOURCE.read_bytes().splitlines(keepends=True)

    def expected_evidence_target(start: int, end: int) -> dict[str, Any]:
        raw = b"".join(reader_raw_lines[start - 1:end])
        return {
            "path": SOURCE_PATH,
            "file_sha256": SOURCE_IDENTITY[2],
            "line_start": start,
            "line_end": end,
            "bytes": len(raw),
            "content_sha256": digest(raw),
            "precision": "exact_target_span",
        }

    for local, node in node_by_local.items():
        record = evidence_by_local[local]
        segment_target = expected_evidence_target(
            node["line_start"], node["line_end"]
        )
        unit_target = (
            expected_evidence_target(1, SOURCE_IDENTITY[1])
            if local == "o012-fom-u002" else segment_target
        )
        attrs = node["attrs"]
        source_derived = (
            local == "o012-fom-u002"
            or (
                attrs.get("data-origin") != "edition-original"
                and attrs.get("data-source-lines") is not None
            )
        )
        segment_provenance = (
            "translated_adapted_from_upstream"
            if source_derived
            else (
                "edition_original_proof_repair"
                if (
                    node["kind"] == "proof"
                    and attrs.get("data-repair-id") is not None
                )
                else "edition_original"
            )
        )
        unit_provenance = (
            "composite_translated_and_original"
            if local == "o012-fom-u002" else segment_provenance
        )
        segment_rights = SOURCE_RIGHTS if source_derived else COMPANION_RIGHTS
        unit_rights = COMPOSITE_RIGHTS if local == "o012-fom-u002" else segment_rights
        if (
            record.get("record_ids") != {
                "segment": f"segment:{local}", "unit": f"unit:{local}"
            }
            or record.get("target_locator") != segment_target
            or record.get("record_target_locators") != {
                "segment": segment_target, "unit": unit_target
            }
            or record.get("provenance_relation") != segment_provenance
            or record.get("record_provenance_relations") != {
                "segment": segment_provenance, "unit": unit_provenance
            }
            or record.get("record_rights_component_ids") != {
                "segment": segment_rights, "unit": unit_rights
            }
        ):
            raise SystemExit(
                f"Unit 002 source-audit exact record binding mismatch: {local}"
            )

    text = "\n".join(lines) + "\n"
    required = (
        r"\partial_0(\sigma^0)=0",
        r"\frac{\mathbb Z}{\mathbb Z}=0",
        r"\frac{0}{0}=0",
        "o012-fom-u002-cor-path-components",
        "data-source-lines=\"1034-1034\"",
        r"q-p=\partial P+P\partial",
        r"\partial P+P\partial=g_\#-f_\#",
        "FOM-PR-01", "FOM-PR-02", "FOM-PR-03",
    )
    if any(marker not in text for marker in required):
        raise SystemExit("required mathematical/provenance repair marker missing")
    forbidden = (
        "kefungtoran", ",qquad", ")cong", " komutatif dengan ",
        "berbeda sebesar batas", "titik dasar", "takmanifold",
    )
    if any(marker in text for marker in forbidden):
        raise SystemExit("rejected terminology or malformed TeX remains")
    ids = {node["id"] for node in nodes}
    for number in range(1, 7):
        for kind in ("mcheck", "hint", "sol"):
            if f"o012-fom-u002-{kind}-{number:03d}" not in ids:
                raise SystemExit(f"mastery triple {number} incomplete")
    if len([node for node in nodes if node["kind"] == "figure"]) != 14:
        raise SystemExit("semantic figure inventory mismatch")
    terms_by_id = {row["term_id"]: row for row in terms}
    for _, control_id, evidence_suffix in TERM_SPECS:
        node = node_by_local[f"o012-fom-u002-{evidence_suffix}"]
        evidence_text = "\n".join(
            lines[node["line_start"] - 1:node["line_end"]]
        ).casefold()
        if terms_by_id[control_id]["id_ID"].casefold() not in evidence_text:
            raise SystemExit(
                f"terminology evidence locator lacks exact admitted form: {control_id}"
            )
    return {
        "lines": lines, "nodes": nodes, "adverse": adverse, "terms": terms,
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
        start, end = map(int, source_range.split("-"))
        return {
            "path": "algebraic_topology.tex", "commit_sha": COMMIT,
            "line_start": start, "line_end": end,
            "precision": "exact_source_span",
        }
    return {
        "kind": "edition_original", "path": SOURCE_PATH,
        "precision": "exact_target_span",
    }


def clean_title(title: str, kind: str) -> str:
    value = re.sub(r"\*\*", "", title).strip()
    return value[:240] if value else kind


def parentage(nodes: list[dict[str, Any]]) -> dict[str, tuple[str, int, list[str]]]:
    by_local = {node["id"]: node for node in nodes}
    section_ids = (
        "o012-fom-u002-s03", "o012-fom-u002-s04", "o012-fom-u002-mastery"
    )
    raw_parent: dict[str, str] = {
        "o012-fom-u002-notice": ROOT,
        "o012-fom-u002-s03": ROOT,
        "o012-fom-u002-s04": ROOT,
        "o012-fom-u002-mastery": ROOT,
        "o012-fom-u002-boundary-001": ROOT,
    }
    for node in nodes:
        ident = node["id"]
        if ident == "o012-fom-u002" or ident in raw_parent:
            continue
        if node.get("enclosing_div"):
            raw_parent[ident] = f"unit:{node['enclosing_div']}"
            continue
        section = next(
            (
                local for local in section_ids
                if by_local[local]["line_start"] <= node["line_start"]
                <= by_local[local]["line_end"]
            ),
            None,
        )
        if section is None:
            raise SystemExit(f"cannot assign reader node parent: {ident}")
        raw_parent[ident] = f"unit:{section}"

    children: dict[str, list[str]] = defaultdict(list)
    for ident, parent in raw_parent.items():
        children[parent].append(ident)
    for parent, local_ids in children.items():
        local_ids.sort(key=lambda ident: by_local[ident]["line_start"])

    result: dict[str, tuple[str, int, list[str]]] = {}

    def path_for(ident: str) -> list[str]:
        uid = f"unit:{ident}"
        parent = raw_parent[ident]
        if parent == ROOT:
            return [ROOT, uid]
        parent_local = parent.removeprefix("unit:")
        return path_for(parent_local) + [uid]

    for ident, parent in raw_parent.items():
        result[ident] = (
            parent, children[parent].index(ident) + 1, path_for(ident)
        )
    return result


def load_generic():
    path = LANE / "scripts/validate-backend.py"
    spec = importlib.util.spec_from_file_location("o012_generic_fom002", path)
    if spec is None or spec.loader is None:
        raise SystemExit("cannot load generic backend validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build_additions(
    data: dict[str, Any],
    evidence_identities: dict[str, tuple[int, str]],
) -> dict[str, list[dict[str, Any]]]:
    lines: list[str] = data["lines"]
    nodes: list[dict[str, Any]] = data["nodes"]
    additions: dict[str, list[dict[str, Any]]] = {name: [] for name in FILES}
    all_concepts = [
        "concept:singular-homology",
        *[f"concept:{slug}" for slug, _, _ in TERM_SPECS],
    ]

    def add(name: str, record: dict[str, Any]) -> None:
        additions[name].append(record)

    rights_rows = (
        (
            COMPANION_RIGHTS,
            "Original Indonesian mastery, solutions, proof repairs, audits, and accessibility descriptions for Unit 002.",
            "Original additions are distinguished from the Fomberg source component.",
            "Original Unit 002 companion layer; source component remains separately attributed.",
        ),
        (
            COMPOSITE_RIGHTS,
            "Fomberg source adaptation plus original Indonesian Unit 002 companion layer.",
            "Integrated reader preserves exact source locators, change notices, and separate original additions.",
            "Composite Unit 002; component-scoped rights records control.",
        ),
    )
    for ident, attribution, change, third in rights_rows:
        rec = common("rights", ident)
        rec.update(
            attribution=attribution, change_notice=change,
            component_scope=[ROOT], license_expression="CC-BY-SA-4.0",
            license_url="https://creativecommons.org/licenses/by-sa/4.0/",
            non_endorsement=(
                "Independent Indonesian edition; no source-author or "
                "lecturer endorsement."
            ),
            third_party_status=third,
        )
        add("rights.jsonl", rec)

    terms_by_id = {row["term_id"]: row for row in data["terms"]}
    for slug, control_id, evidence_suffix in TERM_SPECS:
        row = terms_by_id[control_id]
        concept = common("concept", f"concept:{slug}")
        concept.update(
            canonical_label=row["source_term"], domain=row["scope"],
            locale_neutral=True,
        )
        term = common("term", f"term:{slug}:id-ID")
        term.update(
            concept_id=f"concept:{slug}",
            evidence_segment_id=f"segment:o012-fom-u002-{evidence_suffix}",
            locale="id-ID", preferred=row["id_ID"], register="textbook",
            rejected_forms=[], rights_component_id=COMPOSITE_RIGHTS,
            scope_unit_id=ROOT, source_term=row["source_term"],
            terminology_control_id=row["term_id"],
            terminology_status=row["status"], usage_note=row["note"],
            variants=[],
        )
        add("concepts.jsonl", concept)
        add("terms.jsonl", term)

    node_parents = parentage(nodes)
    source_heading_ids = {"o012-fom-u002-s03", "o012-fom-u002-s04"}
    root_local = "o012-fom-u002"
    source_kinds = {
        "definition", "remark", "lemma", "proof", "figure", "corollary",
        "proposition", "theorem", "example", "source-omission",
    }
    repair_targets = {
        "o012-fom-u002-prop-chain-map": "FOM-PR-01",
        "o012-fom-u002-prop-induced-map": "FOM-PR-02",
        "o012-fom-u002-cor-homotopy-equivalent": "FOM-PR-03",
    }
    for node in nodes:
        ident = node["id"]
        uid = f"unit:{ident}"
        kind = node["kind"]
        attrs = node["attrs"]
        is_root = ident == root_local
        source_range = attrs.get("data-source-lines")
        explicit_original = attrs.get("data-origin") == "edition-original"
        is_source = (
            not explicit_original
            and (
                ident in source_heading_ids
                or (kind in source_kinds and source_range is not None)
            )
        )
        if is_root:
            rights = COMPOSITE_RIGHTS
            provenance = "composite_translated_and_original"
            parent = COURSE
            order = 32
            path = [ROOT]
            display = (
                "Topologi Aljabar — Komponen Fomberg Unit 002: "
                "Homologi Singular dan Invariansi Homotopi"
            )
            locator = target_locator(lines, 1, len(lines))
        else:
            rights = SOURCE_RIGHTS if is_source else COMPANION_RIGHTS
            provenance = (
                "translated_adapted_from_upstream"
                if is_source else
                (
                    "edition_original_proof_repair"
                    if kind == "proof" and attrs.get("data-repair-id")
                    else "edition_original"
                )
            )
            parent, order, path = node_parents[ident]
            display = clean_title(node["title"], kind)
            locator = target_locator(lines, node["line_start"], node["line_end"])

        unit_kind = (
            "reader_unit" if is_root
            else ("section" if kind == "heading" else kind.replace("-", "_"))
        )
        unit = common("unit", uid)
        unit.update(
            component_source_commit=COMMIT, component_source_id=RESOURCE,
            concept_ids=all_concepts, course_id=COURSE,
            course_route_unit_id=ROUTE, display_title=display,
            edition_id=EDITION, edition_unit_id=ROOT, locale="id-ID",
            model_provenance=MODEL, order=order, parent_id=parent, path=path,
            program_id=PROGRAM, provenance_relation=provenance,
            resource_id=RESOURCE, rights_component_id=rights,
            source_local_id=ident, target_locator=locator,
            translation_state="structurally_verified", unit_kind=unit_kind,
        )
        if is_root:
            unit.update(
                edition_order=2, route_order=9,
                source_locator={
                    "path": "algebraic_topology.tex", "commit_sha": COMMIT,
                    "line_start": 615, "line_end": 1290,
                    "precision": "exact_unit_span", "span_bytes": 22924,
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
                if kind == "proof" else "source_omission_named"
            )
        if ident in repair_targets:
            unit["repair_id"] = repair_targets[ident]
            unit["proof_status"] = "statement_with_complete_repaired_proof"
        if kind == "solution":
            unit["solution_status"] = "complete_checked_solution"
        add("units.jsonl", unit)

        if is_root:
            segment_rights = SOURCE_RIGHTS
            segment_provenance = "translated_adapted_from_upstream"
            segment_locator = target_locator(
                lines, node["line_start"], node["line_end"]
            )
            segment_source_locator = {
                "path": "algebraic_topology.tex", "commit_sha": COMMIT,
                "line_start": 615, "line_end": 1290,
                "precision": "exact_unit_span",
            }
        else:
            segment_rights = rights
            segment_provenance = provenance
            segment_locator = locator
            segment_source_locator = source_locator(
                source_range if is_source else None
            )

        segment = common("segment", f"segment:{ident}")
        segment.update(
            component_source_commit=COMMIT, component_source_id=RESOURCE,
            concept_ids=all_concepts, course_route_unit_id=ROUTE,
            edition_id=EDITION, edition_unit_id=ROOT, locale="id-ID",
            model_provenance=MODEL, order=order,
            provenance_relation=segment_provenance, resource_id=RESOURCE,
            rights_component_id=segment_rights,
            segment_kind=("source_heading" if is_root else unit_kind),
            source_local_id=ident,
            source_locator=segment_source_locator,
            target_locator=segment_locator,
            translation_state="structurally_verified",
            unit_id=uid,
        )
        if alias:
            segment["source_aliases"] = [alias]
        for key in ("repair_id", "proof_status", "solution_status"):
            if key in unit:
                segment[key] = unit[key]
        add("segments.jsonl", segment)

    source_size, _, source_sha = SOURCE_IDENTITY
    assets = (
        (
            "asset:o012-fom-u002-source-markdown", "canonical_reader_source",
            COMPOSITE_RIGHTS, {},
        ),
        (
            "asset:o012-fom-u002-semantic-diagram-layer",
            "semantic_diagram_accessibility_layer", SOURCE_RIGHTS,
            {
                "source_diagram_count": 14,
                "semantic_figure_block_count": 14,
                "source_format_counts": {"tikzcd": 13, "tikzpicture": 1},
                "semantic_unit_ids": [
                    f"unit:{node['id']}" for node in nodes
                    if node["kind"] == "figure"
                ],
            },
        ),
    )
    for ident, role, rights, extra in assets:
        rec = common("asset", ident)
        rec.update(
            bytes=source_size, edition_id=EDITION,
            media_type="text/markdown; charset=utf-8", path=SOURCE_PATH,
            resource_id=RESOURCE, rights_component_id=rights, role=role,
            sha256=source_sha, **extra,
        )
        add("assets.jsonl", rec)

    evidence = (
        (
            "artifact:o012-fom-u002-source-audit",
            "qa/FOMBERG_UNIT_002_SOURCE_AUDIT.json",
            ["qa:o012-fom-u002-source-integrity"], "source_frozen",
            "application/json",
        ),
        (
            "artifact:o012-fom-u002-review-part-a",
            "qa/FOMBERG_UNIT_002_REVIEW_PART_A_DRAFT.md",
            ["qa:o012-fom-u002-math", "qa:o012-fom-u002-language"],
            "mathematically_reviewed", "text/markdown; charset=utf-8",
        ),
        (
            "artifact:o012-fom-u002-review-part-b",
            "qa/FOMBERG_UNIT_002_REVIEW_PART_B_DRAFT.md",
            ["qa:o012-fom-u002-math", "qa:o012-fom-u002-language"],
            "mathematically_reviewed", "text/markdown; charset=utf-8",
        ),
        (
            "artifact:o012-fom-u002-independent-review",
            "qa/FOMBERG_UNIT_002_INDEPENDENT_REVIEW_DRAFT.md",
            ["qa:o012-fom-u002-math", "qa:o012-fom-u002-language"],
            "mathematically_reviewed", "text/markdown; charset=utf-8",
        ),
        (
            "artifact:o012-fom-u002-qa",
            "qa/FOMBERG_UNIT_002_QA.json",
            ["qa:o012-fom-u002-source-integrity", "qa:o012-fom-u002-mastery"],
            "built", "application/json",
        ),
    )
    for ident, relative, qa_ids, state, media in evidence:
        size, sha = evidence_identities[relative]
        rec = common("artifact", ident)
        rec.update(
            bytes=size, locale="id-ID", manifest_artifact_id=None,
            media_type=media, path=relative, qa_event_ids=qa_ids,
            rights_component_id=COMPOSITE_RIGHTS, sha256=sha,
            toolchain=(
                "Fomberg Unit 002 evidence; algebraic_topology.tex:615-1290; "
                f"{SPAN_IDENTITY[4]}; {MODEL}; route D60-R09; "
                "semantic admission only."
            ),
            translation_state=state, unit_id=ROOT,
        )
        add("artifacts.jsonl", rec)

    qa_rows = (
        (
            "qa:o012-fom-u002-source-integrity", "source",
            "Exact lines 615-1290, cursor 1291, 95 IDs, five aliases, and fourteen semantic diagram blocks passed.",
            [
                "artifact:o012-fom-u002-source-audit",
                "artifact:o012-fom-u002-qa",
            ],
        ),
        (
            "qa:o012-fom-u002-math", "math",
            "Three independent reviews passed P1=P2=P3=0; FOM-PR-01 through FOM-PR-03 and the prism proof are complete.",
            [
                "artifact:o012-fom-u002-review-part-a",
                "artifact:o012-fom-u002-review-part-b",
                "artifact:o012-fom-u002-independent-review",
            ],
        ),
        (
            "qa:o012-fom-u002-language", "language",
            "Independent Indonesian reviews passed after terminology, provenance, and source-order repairs.",
            [
                "artifact:o012-fom-u002-review-part-a",
                "artifact:o012-fom-u002-review-part-b",
                "artifact:o012-fom-u002-independent-review",
            ],
        ),
        (
            "qa:o012-fom-u002-mastery", "mastery",
            "Six exercises, six hints, and six complete checked solutions passed.",
            ["artifact:o012-fom-u002-qa"],
        ),
    )
    for ident, kind, note, witnesses in qa_rows:
        rec = common("qa_event", ident)
        rec.update(
            note=note, qa_type=kind, result="passed", unit_id=ROOT,
            witness_artifact_ids=witnesses,
        )
        add("qa.jsonl", rec)

    type_map = {
        427: "source_typo", 431: "source_typo",
        434: "proof_completion", 435: "proof_completion",
        438: "proof_completion", 441: "proof_completion",
        443: "mathematical_correction", 447: "notation_correction",
        448: "source_clarification", 449: "proof_completion",
        450: "language_correction", 451: "provenance_correction",
        452: "diagram_fidelity", 453: "notation_correction",
        454: "mathematical_correction", 455: "language_correction",
        456: "proof_completion",
    }
    for row in data["adverse"]:
        number = int(row["event_id"].rsplit("-", 1)[1])
        suffixes = CORRECTION_TARGETS[number]
        affected = [f"unit:o012-fom-u002-{suffix}" for suffix in suffixes]
        rec = common("correction", f"correction:o012-fom-u002-adv-{number:04d}")
        rec.update(
            adverse_ledger_id=row["event_id"], affected_unit_ids=affected,
            correction_type=type_map.get(number, "mathematical_correction"),
            edition_id=EDITION, evidence=row["source_location"],
            evidence_segment_id=f"segment:o012-fom-u002-{suffixes[0]}",
            rationale=row["rationale"], resource_id=RESOURCE,
            source_defect=row["observed"], target_change=row["action"],
            unit_id=ROOT, upstream_report_disposition="not_contacted",
        )
        add("corrections.jsonl", rec)

    def relation(
        ident: str, from_id: str, to_id: str, kind: str, note: str,
        **extra: Any,
    ) -> None:
        rec = common("relation", ident)
        rec.update(
            from_id=from_id, to_id=to_id, relation_type=kind, note=note,
            **extra,
        )
        add("relations.jsonl", rec)

    relation(
        "relation:adapts:o012-fom-u002:fomberg-edition", ROOT, EDITION,
        "adapts", "Indonesian Unit 002 adapts exact Fomberg lines 615-1290."
    )
    relation(
        "relation:contains:o012-d60:fomberg-u002", COURSE, ROOT, "contains",
        "Course route D60-R09 contains Fomberg Unit 002.",
        course_route_unit_id=ROUTE,
    )
    relation(
        "relation:precedes:o012-fom-u001:o012-fom-u002",
        "unit:o012-fom-u001", ROOT, "precedes",
        "Fomberg Unit 001 precedes Unit 002 in source order.",
    )
    relation(
        "relation:contains:o012-d60-rights:fomberg-u002",
        ROUTE_RIGHTS, ROOT, "contains",
        "Integrated-route rights contain the Fomberg Unit 002 composite.",
    )
    relation(
        "relation:precedes:o012-fom-u002:mastery", ROOT,
        "unit:o012-fom-u002-mastery", "precedes",
        "Translated source body precedes the original solved mastery layer.",
    )
    for number, target in (
        (1, "prop-chain-map"), (2, "prop-induced-map"),
        (3, "cor-homotopy-equivalent"),
    ):
        relation(
            f"relation:proves:o012-fom-u002-pr{number:02d}:{target}",
            f"unit:o012-fom-u002-proof-"
            + (
                "chain-map" if number == 1
                else "induced-map-homomorphism" if number == 2
                else "homotopy-equivalent"
            ),
            f"unit:o012-fom-u002-{target}", "proves",
            f"Complete original repair FOM-PR-0{number} closes the named source omission.",
            repair_id=f"FOM-PR-0{number}",
        )
    for number in range(1, 7):
        relation(
            f"relation:hints:fom-u002-hint-{number:03d}:mcheck-{number:03d}",
            f"unit:o012-fom-u002-hint-{number:03d}",
            f"unit:o012-fom-u002-mcheck-{number:03d}", "hints",
            f"Hint for Fomberg Unit 002 mastery check {number}.",
        )
        relation(
            f"relation:solves:fom-u002-sol-{number:03d}:mcheck-{number:03d}",
            f"unit:o012-fom-u002-sol-{number:03d}",
            f"unit:o012-fom-u002-mcheck-{number:03d}", "solves",
            f"Complete checked solution for Unit 002 mastery check {number}.",
        )
    figure_nodes = [node for node in nodes if node["kind"] == "figure"]
    for number, node in enumerate(figure_nodes, 1):
        relation(
            f"relation:illustrates:fom-u002-fig-{number:03d}:diagram-asset",
            f"unit:{node['id']}",
            "asset:o012-fom-u002-semantic-diagram-layer", "illustrates",
            f"Semantic figure block {number} preserves its source diagram function.",
        )

    for name, records in additions.items():
        records.sort(key=lambda item: item["id"])
        if len(records) != DELTA[name]:
            raise SystemExit(
                f"{name}: derived suffix count mismatch "
                f"({len(records)} != {DELTA[name]})"
            )
        if len({item["id"] for item in records}) != len(records):
            raise SystemExit(f"{name}: duplicate derived IDs")
    return additions
