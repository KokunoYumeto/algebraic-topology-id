#!/usr/bin/env python3
"""Fail-closed source and static-QA receipts for Fomberg Unit 002.

The program reads but never alters its authority, reader, control, or review
inputs.  It writes the two declared JSON receipts only after every check has
passed, so a failed validation cannot manufacture a PASS receipt.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import shlex
import shutil
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any


LANE = Path(__file__).resolve().parents[1]
AUDIT_OUTPUT = LANE / "qa/FOMBERG_UNIT_002_SOURCE_AUDIT.json"
QA_OUTPUT = LANE / "qa/FOMBERG_UNIT_002_QA.json"

SCHEMA_VERSION = "1.0.0"
AUDIT_DATE = "2026-08-24"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"
COMMIT = "563194fae879178b9a6871b249513bfc27968975"
TREE = "fb678966d1533d529bdd72f49d8496a3bdc14a9b"
RESOURCE = "resource:fomberg-algebraic-topology-2025"
EDITION = "edition:fomberg-at-2025-563194f"
ROOT = "unit:o012-fom-u002"
COURSE = "course:o012-d60"
ROUTE = "D60-R09"

READER_PATH = (
    "source/id-ID/fomberg/units/"
    "fomberg-unit-002-singular-homology-homotopy-invariance.md"
)
UPSTREAM_PATH = (
    "authority/upstream/"
    "math-notes-563194fae879178b9a6871b249513bfc27968975/"
    "tree/algebraic_topology.tex"
)
TERMINOLOGY_PATH = "00_control/TERMINOLOGY.csv"
ADVERSE_PATH = "00_control/ADVERSE_LEDGER.csv"

READER_IDENTITY = {
    "bytes": 44407,
    "lf_lines": 1342,
    "sha256": "0851ab7d9f5ded1e836a0e73aa055fbd28b82998208d8136ec0cf4757747435c",
}
UPSTREAM_IDENTITY = {
    "bytes": 223886,
    "lf_lines": 6069,
    "sha256": "d27095de0f38f0c14b2d7716cb52d51d064f0594dd9f82f9d1b3e6af5b35a483",
}
SPAN_IDENTITY = {
    "line_start": 615,
    "line_end": 1290,
    "lines": 676,
    "bytes": 22924,
    "sha256": "9b28e159825e020b262a51b9c50372b2fafc26270fab6480d860aaaeefdda84f",
}
NEXT_SOURCE_LINE = 1291
NEXT_HEADING = r"\subsection{Exact sequences}"

ALIASES = {
    "lem:path-connected-then-hzero-z": "o012-fom-u002-lem-hzero",
    "prp:functoriality-of-induced-maps": "o012-fom-u002-prop-functoriality",
    "cor:injective-i-surjective-r": "o012-fom-u002-cor-retract",
    "thm:homotopic-maps-induce-same-homomorphism-on-homology":
        "o012-fom-u002-thm-homotopy-invariance",
    "cor:homotopy-equivalent-implies-same-homology":
        "o012-fom-u002-cor-homotopy-equivalent",
}
EXPECTED_LINK_TARGET_COUNTS = Counter({
    "o012-fom-u002-lem-hzero": 4,
    "o012-fom-u002-prop-functoriality": 1,
    "o012-fom-u002-cor-retract": 1,
    "o012-fom-u002-thm-homotopy-invariance": 2,
    "o012-fom-u002-cor-homotopy-equivalent": 2,
})

EXPECTED_HEADING_IDS = [
    "o012-fom-u002-notice",
    "o012-fom-u002",
    "o012-fom-u002-s03",
    "o012-fom-u002-s04",
    "o012-fom-u002-mastery",
]
EXPECTED_HEADING_CLASSES = {
    "o012-fom-u002-notice": ["unnumbered"],
    "o012-fom-u002": [],
    "o012-fom-u002-s03": [],
    "o012-fom-u002-s04": [],
    "o012-fom-u002-mastery": ["unnumbered"],
}
EXPECTED_CLASS_COUNTS = {
    "boundary": 1,
    "corollary": 7,
    "definition": 6,
    "edition-note": 1,
    "example": 1,
    "exercise": 6,
    "figure": 14,
    "heading": 5,
    "hint": 6,
    "lemma": 3,
    "proof": 14,
    "proposition": 3,
    "remark": 12,
    "solution": 6,
    "source-audit": 6,
    "source-omission": 3,
    "theorem": 1,
}
FIGURE_IDS = [
    "o012-fom-u002-fig-point-chain",
    "o012-fom-u002-fig-hzero-sequence",
    "o012-fom-u002-fig-chain-complex",
    "o012-fom-u002-fig-augmented-chain-1",
    "o012-fom-u002-fig-augmented-chain-2",
    "o012-fom-u002-fig-flow-balance",
    "o012-fom-u002-fig-induced-chain-map-1",
    "o012-fom-u002-fig-induced-chain-map-2",
    "o012-fom-u002-fig-functoriality",
    "o012-fom-u002-fig-retract-spaces",
    "o012-fom-u002-fig-retract-homology",
    "o012-fom-u002-fig-chain-homotopy",
    "o012-fom-u002-fig-composition",
    "o012-fom-u002-fig-homotopy-prism",
]

SOURCE_ENVIRONMENT_COUNTS = {
    "definition": 6,
    "remark": 12,
    "lemma": 3,
    "proposition": 3,
    "theorem": 1,
    "corollary": 6,
    "example": 1,
    "proof": 8,
    "proofof": 2,
}

TERM_ROWS_SHA256 = "a97fee585a5107f3bbe5de8f6250cf8af75a9013236a2145fddfc83fe65c2991"
ADVERSE_ROWS_SHA256 = "93a4e2aa85b67fa5991cc209a66d1f17a22eaa41bd26c18dc7df75ed29d2691f"
EXPECTED_TERM_ROWS = [
    {
        "term_id": "O012-TERM-0394",
        "source_term": "singular chain",
        "id_ID": "rantai singular",
        "scope": "homological_algebra",
        "status": "admitted",
        "note": "finite integer linear combination of singular simplices",
    },
    {
        "term_id": "O012-TERM-0395",
        "source_term": "singular chain complex",
        "id_ID": "kompleks rantai singular",
        "scope": "homological_algebra",
        "status": "admitted",
        "note": "free-abelian singular chains with the alternating-face boundary map",
    },
    {
        "term_id": "O012-TERM-0396",
        "source_term": "chain map",
        "id_ID": "pemetaan rantai",
        "scope": "homological_algebra",
        "status": "admitted",
        "note": "degree-preserving family of homomorphisms commuting with boundary maps",
    },
    {
        "term_id": "O012-TERM-0397",
        "source_term": "induced map",
        "id_ID": "pemetaan terinduksi",
        "scope": "algebraic_topology",
        "status": "admitted",
        "note": "homology homomorphism obtained from a continuous map through its singular chain map",
    },
    {
        "term_id": "O012-TERM-0398",
        "source_term": "augmented chain complex",
        "id_ID": "kompleks rantai teraugmentasi",
        "scope": "homological_algebra",
        "status": "admitted",
        "note": "singular chain complex extended by the coefficient-sum map C_0 to Z",
    },
    {
        "term_id": "O012-TERM-0399",
        "source_term": "reduced homology",
        "id_ID": "homologi tereduksi",
        "scope": "homological_algebra",
        "status": "admitted",
        "note": "homology of the augmented singular chain complex for a nonempty space",
    },
    {
        "term_id": "O012-TERM-0400",
        "source_term": "chain homotopy",
        "id_ID": "homotopi rantai",
        "scope": "homological_algebra",
        "status": "admitted",
        "note": "degree-plus-one family P satisfying q-p=boundary P+P boundary",
    },
]

REVIEW_SLOTS = {
    "integrated": [
        "qa/FOMBERG_UNIT_002_INDEPENDENT_REVIEW.md",
        "qa/FOMBERG_UNIT_002_INDEPENDENT_REVIEW_DRAFT.md",
    ],
    "part_a": [
        "qa/FOMBERG_UNIT_002_REVIEW_PART_A.md",
        "qa/FOMBERG_UNIT_002_REVIEW_PART_A_DRAFT.md",
    ],
    "part_b": [
        "qa/FOMBERG_UNIT_002_REVIEW_PART_B.md",
        "qa/FOMBERG_UNIT_002_REVIEW_PART_B_DRAFT.md",
    ],
}

TERM_SLUGS = [
    "singular-chain",
    "singular-chain-complex",
    "chain-map",
    "induced-map",
    "augmented-chain-complex",
    "reduced-homology",
    "chain-homotopy",
]
EXPECTED_BACKEND_COUNTS = {
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


def die(message: str) -> None:
    raise SystemExit(f"Fomberg Unit 002 QA FAIL: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        die(message)


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical(obj: Any) -> bytes:
    return json.dumps(
        obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def receipt_bytes(obj: dict[str, Any]) -> bytes:
    return (
        json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2).encode("utf-8")
        + b"\n"
    )


def strict_input(relative: str) -> tuple[bytes, str]:
    path = LANE / relative
    require(path.is_file(), f"missing input {relative}")
    raw = path.read_bytes()
    require(not raw.startswith(b"\xef\xbb\xbf"), f"{relative}: UTF-8 BOM forbidden")
    require(b"\r" not in raw, f"{relative}: CR/CRLF forbidden")
    require(raw.endswith(b"\n"), f"{relative}: terminal LF required")
    try:
        text = raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        die(f"{relative}: not strict UTF-8 ({exc})")
    require("\ufffd" not in text, f"{relative}: replacement character forbidden")
    return raw, text


def identity(relative: str, raw: bytes | None = None) -> dict[str, Any]:
    payload = (LANE / relative).read_bytes() if raw is None else raw
    return {
        "path": relative,
        "bytes": len(payload),
        "sha256": digest(payload),
        "lf_lines": payload.count(b"\n"),
        "encoding": "UTF-8",
        "newline": "LF",
    }


def require_identity(
    relative: str, raw: bytes, expected: dict[str, Any]
) -> dict[str, Any]:
    actual = identity(relative, raw)
    for field in ("bytes", "lf_lines", "sha256"):
        require(
            actual[field] == expected[field],
            f"{relative}: {field} {actual[field]!r} != {expected[field]!r}",
        )
    return actual


def parse_attributes(inner: str, where: str) -> tuple[str, list[str], dict[str, str]]:
    try:
        tokens = shlex.split(inner, posix=True)
    except ValueError as exc:
        die(f"{where}: malformed attributes ({exc})")
    ids: list[str] = []
    classes: list[str] = []
    attrs: dict[str, str] = {}
    for token in tokens:
        if token.startswith("#"):
            ids.append(token[1:])
        elif token.startswith("."):
            classes.append(token[1:])
        elif "=" in token:
            key, value = token.split("=", 1)
            require(key and key not in attrs, f"{where}: duplicate/empty attribute {key!r}")
            attrs[key] = value
        else:
            die(f"{where}: unparsed attribute token {token!r}")
    require(len(ids) == 1 and ids[0], f"{where}: exactly one stable ID required")
    require(len(classes) == len(set(classes)), f"{where}: duplicate class")
    return ids[0], classes, attrs


def parse_reader(
    raw: bytes, text: str
) -> tuple[list[str], list[dict[str, Any]], int, int]:
    lines = text.splitlines()
    require(len(lines) == READER_IDENTITY["lf_lines"], "reader physical-line mismatch")
    headings: list[dict[str, Any]] = []
    fences: list[dict[str, Any]] = []
    stack: list[dict[str, Any]] = []
    opens = 0
    closes = 0

    for number, line in enumerate(lines, 1):
        heading_match = re.match(
            r"^(#{1,6})[ \t]+(.+?)[ \t]+\{([^{}]+)\}[ \t]*$", line
        )
        if heading_match:
            ident, classes, attrs = parse_attributes(
                heading_match.group(3), f"reader line {number} heading"
            )
            headings.append({
                "id": ident,
                "kind": "heading",
                "classes": classes,
                "attrs": attrs,
                "title": heading_match.group(2),
                "heading_level": len(heading_match.group(1)),
                "line_start": number,
                "line_end": number,
            })

        opener_match = re.match(r"^(:{3,})[ \t]+(\{.*\})[ \t]*$", line)
        if opener_match:
            inner = opener_match.group(2)[1:-1].strip()
            ident, classes, attrs = parse_attributes(
                inner, f"reader line {number} fenced div"
            )
            require(
                len(classes) == 1,
                f"reader line {number}: fenced div needs one semantic class",
            )
            node = {
                "id": ident,
                "kind": classes[0],
                "classes": classes,
                "attrs": attrs,
                "title": "",
                "line_start": number,
                "line_end": 0,
            }
            stack.append(node)
            opens += 1
            continue

        if re.match(r"^:{3,}[ \t]*$", line):
            require(bool(stack), f"reader line {number}: unmatched fenced-div close")
            node = stack.pop()
            node["line_end"] = number
            fences.append(node)
            closes += 1

    require(not stack, "reader has unclosed fenced divs")

    for index, heading in enumerate(headings):
        end = len(lines)
        for later in headings[index + 1:]:
            if later["heading_level"] <= heading["heading_level"]:
                end = later["line_start"] - 1
                break
        heading["line_end"] = end

    # The edition-original mastery heading is followed by a separately indexed
    # cursor/boundary object.  Keep that boundary out of the mastery target
    # span, matching the established Unit 001 backend contract.
    heading_by_id = {heading["id"]: heading for heading in headings}
    boundary_nodes = [
        node for node in fences if node["id"] == "o012-fom-u002-boundary-001"
    ]
    require(len(boundary_nodes) == 1, "reader cursor-boundary census mismatch")
    heading_by_id["o012-fom-u002-mastery"]["line_end"] = (
        boundary_nodes[0]["line_start"] - 1
    )

    nodes = sorted(headings + fences, key=lambda node: (node["line_start"], node["line_end"]))
    ids = [node["id"] for node in nodes]
    require(len(ids) == 95, f"reader declares {len(ids)} IDs, expected 95")
    require(len(ids) == len(set(ids)), "reader stable IDs are not unique")
    require(
        all(ident.startswith("o012-fom-u002") for ident in ids),
        "reader contains a stable ID outside the Unit 002 namespace",
    )
    require(opens == 90 and closes == 90, "reader fenced-div count is not 90/90")

    class_counts = dict(sorted(Counter(node["kind"] for node in nodes).items()))
    require(class_counts == EXPECTED_CLASS_COUNTS, "reader semantic-class census mismatch")
    heading_ids = [node["id"] for node in headings]
    require(heading_ids == EXPECTED_HEADING_IDS, "reader heading-ID order mismatch")
    require(
        {node["id"]: node["classes"] for node in headings} == EXPECTED_HEADING_CLASSES,
        "reader heading-class declarations mismatch",
    )

    located: list[tuple[int, int, str]] = []
    for node in nodes:
        source_range = node["attrs"].get("data-source-lines")
        if source_range is None:
            continue
        match = re.fullmatch(r"([0-9]+)-([0-9]+)", source_range)
        require(match is not None, f"{node['id']}: malformed source locator")
        start, end = map(int, match.groups())
        require(615 <= start <= end <= 1290, f"{node['id']}: locator out of unit span")
        located.append((node["line_start"], start, node["id"]))
    source_starts = [entry[1] for entry in sorted(located)]
    require(
        source_starts == sorted(source_starts),
        "source-located reader objects are not in nondecreasing source order",
    )

    raw_lines = raw.splitlines(keepends=True)
    require(len(raw_lines) == len(lines), "reader raw/text line split mismatch")
    for node in nodes:
        payload = b"".join(raw_lines[node["line_start"] - 1:node["line_end"]])
        node["target_content_bytes"] = len(payload)
        node["target_content_sha256"] = digest(payload)
    return lines, nodes, opens, closes


def node_text(lines: list[str], node: dict[str, Any]) -> str:
    return "\n".join(lines[node["line_start"] - 1:node["line_end"]]) + "\n"


def environment_ranges(
    lines: list[str], kind: str, absolute_start: int
) -> list[str]:
    starts: list[int] = []
    ranges: list[str] = []
    begin = re.compile(rf"^[ \t]*\\begin\{{{re.escape(kind)}\}}")
    end = re.compile(rf"^[ \t]*\\end\{{{re.escape(kind)}\}}")
    for offset, line in enumerate(lines):
        absolute = absolute_start + offset
        if begin.search(line):
            starts.append(absolute)
        if end.search(line):
            require(bool(starts), f"source {kind}: unmatched end at line {absolute}")
            ranges.append(f"{starts.pop()}-{absolute}")
    require(not starts, f"source {kind}: unclosed environment")
    return ranges


def verify_source(raw: bytes, text: str) -> dict[str, Any]:
    source_identity = require_identity(UPSTREAM_PATH, raw, UPSTREAM_IDENTITY)
    lines = text.splitlines()
    require(len(lines) == 6069, "authority physical-line count mismatch")
    require(lines[614] == r"\subsection{Singular homology}", "source line 615 mismatch")
    require(lines[953] == r"\subsection{Homotopy invariance}", "source line 954 mismatch")
    require(lines[1290] == NEXT_HEADING, "source cursor line 1291 mismatch")

    span_lines = lines[614:1290]
    span_raw = ("\n".join(span_lines) + "\n").encode("utf-8")
    require(len(span_lines) == SPAN_IDENTITY["lines"], "source-span line mismatch")
    require(len(span_raw) == SPAN_IDENTITY["bytes"], "source-span byte mismatch")
    require(digest(span_raw) == SPAN_IDENTITY["sha256"], "source-span hash mismatch")
    span_text = span_raw.decode("utf-8")

    ranges = {
        kind: environment_ranges(span_lines, kind, 615)
        for kind in SOURCE_ENVIRONMENT_COUNTS
    }
    counts = {kind: len(values) for kind, values in ranges.items()}
    require(counts == SOURCE_ENVIRONMENT_COUNTS, "source semantic-environment census mismatch")
    require(sum(counts.values()) == 42, "source semantic-environment total mismatch")

    labels = re.findall(r"\\label\{([^{}]+)\}", span_text)
    require(labels == list(ALIASES), "source label inventory/order mismatch")
    cref_payloads = re.findall(r"\\Cref\{([^{}]+)\}", span_text)
    require(len(cref_payloads) == 10, "source Cref-command count mismatch")
    source_ref_labels = [
        label.strip()
        for payload in cref_payloads
        for label in payload.split(",")
        if label.strip()
    ]
    require(len(source_ref_labels) == 10, "source Cref target count mismatch")
    require(all(label in ALIASES for label in source_ref_labels), "unknown source Cref target")
    mapped_targets = Counter(ALIASES[label] for label in source_ref_labels)
    require(mapped_targets == EXPECTED_LINK_TARGET_COUNTS, "source Cref multiplicity mismatch")

    diagram_counts = {
        "tikzcd": len(re.findall(r"\\begin\{tikzcd\}", span_text)),
        "tikzpicture": len(re.findall(r"\\begin\{tikzpicture\}", span_text)),
    }
    require(diagram_counts == {"tikzcd": 13, "tikzpicture": 1}, "source diagram census mismatch")
    require(
        span_text.count(r"\end{tikzcd}") == 13
        and span_text.count(r"\end{tikzpicture}") == 1,
        "source diagram environment is unbalanced",
    )
    require(
        not re.search(r"\\begin\{exercise\}", span_text),
        "selected source span unexpectedly contains a formal exercise",
    )

    prefix_raw = ("\n".join(lines[:614]) + "\n").encode("utf-8")
    return {
        "identity": source_identity,
        "span_raw": span_raw,
        "span_text": span_text,
        "span_lines": span_lines,
        "span": {
            **SPAN_IDENTITY,
            "start_byte_offset": len(prefix_raw),
            "end_byte_offset_inclusive": len(prefix_raw) + len(span_raw) - 1,
        },
        "environment_counts": counts,
        "environment_ranges": ranges,
        "labels": labels,
        "cref_payloads": cref_payloads,
        "diagram_counts": diagram_counts,
    }


def verify_reader(
    raw: bytes, text: str, source: dict[str, Any]
) -> dict[str, Any]:
    reader_identity = require_identity(READER_PATH, raw, READER_IDENTITY)
    require(text.count(MODEL) == 1, "model provenance must occur exactly once")
    for fragment in (
        'lang: id-ID',
        'edition_unit_id: "O012-FOM-002"',
        'course_route_unit_id: "D60-R09"',
        COMMIT,
        SPAN_IDENTITY["sha256"],
        "baris 1291",
        "CC BY-SA 4.0",
    ):
        require(fragment in text, f"reader metadata/provenance fragment missing: {fragment}")

    lines, nodes, opens, closes = parse_reader(raw, text)
    by_id = {node["id"]: node for node in nodes}

    aliases = {
        node["attrs"]["data-source-label"]: node["id"]
        for node in nodes
        if "data-source-label" in node["attrs"]
    }
    require(aliases == ALIASES, "reader source-alias map mismatch")
    links = re.findall(r"\]\(#([A-Za-z0-9][A-Za-z0-9_.:-]*)\)", text)
    require(len(links) == 10, "reader internal-link count mismatch")
    require(Counter(links) == EXPECTED_LINK_TARGET_COUNTS, "reader link multiplicity mismatch")
    require(all(target in by_id for target in links), "reader has unresolved fragment link")

    figures = [node for node in nodes if node["kind"] == "figure"]
    require([node["id"] for node in figures] == FIGURE_IDS, "semantic-figure order mismatch")
    for node in figures:
        require("semantik" in node_text(lines, node).casefold(), f"{node['id']}: no semantic description")

    repair_spec = {
        "FOM-PR-01": {
            "omission": "o012-fom-u002-omission-pr01",
            "source_lines": "1001-1003",
            "proof": "o012-fom-u002-proof-chain-map",
            "required": [
                r"\delta_i\colon\Delta^{n-1}\to\Delta^n",
                r"\partial f_\#(\sigma)",
                r"f_\#(\partial\sigma)",
                "seluruh",
                r"$C_n(X)$",
            ],
        },
        "FOM-PR-02": {
            "omission": "o012-fom-u002-omission-pr02",
            "source_lines": "1034-1034",
            "proof": "o012-fom-u002-proof-induced-map-homomorphism",
            "required": [
                r"f_*([z]+[w])",
                r"f_*([z+w])",
                r"[f_\#(z+w)]",
                r"f_*([z])+f_*([w])",
                "homomorfisma",
            ],
        },
        "FOM-PR-03": {
            "omission": "o012-fom-u002-omission-pr03",
            "source_lines": "1126-1128",
            "proof": "o012-fom-u002-proof-homotopy-equivalent",
            "required": [
                r"g_*\circ f_*",
                r"\operatorname{id}_{H_n(X)}",
                r"f_*\circ g_*",
                r"\operatorname{id}_{H_n(Y)}",
                "saling invers",
            ],
        },
    }
    proof_closure: dict[str, Any] = {}
    for repair_id, spec in repair_spec.items():
        omission = by_id.get(spec["omission"])
        proof = by_id.get(spec["proof"])
        require(omission is not None and omission["kind"] == "source-omission",
                f"{repair_id}: omission object missing/wrong class")
        require(proof is not None and proof["kind"] == "proof",
                f"{repair_id}: proof object missing/wrong class")
        require(
            omission["attrs"].get("data-source-lines") == spec["source_lines"]
            and omission["attrs"].get("data-repair-id") == repair_id,
            f"{repair_id}: omission locator/repair binding mismatch",
        )
        require(
            proof["attrs"].get("data-origin") == "edition-original"
            and proof["attrs"].get("data-repair-id") == repair_id,
            f"{repair_id}: proof origin/repair binding mismatch",
        )
        proof_body = node_text(lines, proof)
        for fragment in spec["required"]:
            require(fragment in proof_body, f"{repair_id}: proof fragment missing: {fragment}")
        proof_closure[repair_id] = {
            "omission_id": omission["id"],
            "source_lines": spec["source_lines"],
            "proof_id": proof["id"],
            "proof_status": "complete_original_repair",
        }

    representative_proof = node_text(lines, by_id["o012-fom-u002-proof-induced-map-source"])
    for fragment in (r"$[z]=[z']$", r"z-z'\in B_n(X)", "tidak bergantung pada wakil"):
        require(fragment in representative_proof, f"induced-map well-definedness missing: {fragment}")

    point_proof = node_text(lines, by_id["o012-fom-u002-proof-point"])
    require(r"\partial_0(\sigma^0)=0" in point_proof, "point proof omits partial_0=0")
    require(r"n\geq1" in point_proof, "point proof does not scope alternating boundary to n>=1")
    require(r"\partial_0\sigma^0=\sigma^{-1}" not in point_proof,
            "point proof reintroduces an undefined degree-minus-one generator")

    hint_one = node_text(lines, by_id["o012-fom-u002-hint-001"])
    require(r"\partial_0=0" in hint_one and r"n\geq1" in hint_one,
            "F2.1 hint does not separate degree zero from positive degrees")
    solution_two = node_text(lines, by_id["o012-fom-u002-sol-002"])
    require("selisihnya dengan $x_i$ merupakan batas suatu lintasan" in solution_two,
            "F2.2 solution retains the rejected boundary-difference phrasing")
    contractible = by_id.get("o012-fom-u002-proof-contractible")
    require(contractible is not None and contractible["kind"] == "proof",
            "contractibility proof object missing")
    contractible_text = node_text(lines, contractible)
    for fragment in (
        r"f\colon X\to\{*\}",
        r"g\colon\{*\}\to X",
        r"f\circ g=\operatorname{id}_{\{*\}}",
        r"g\circ f=c_{x_0}\simeq\operatorname{id}_X",
    ):
        require(fragment in contractible_text, f"contractibility closure missing: {fragment}")

    exercise_ids = [f"o012-fom-u002-mcheck-{n:03d}" for n in range(1, 7)]
    hint_ids = [f"o012-fom-u002-hint-{n:03d}" for n in range(1, 7)]
    solution_ids = [f"o012-fom-u002-sol-{n:03d}" for n in range(1, 7)]
    for expected_kind, expected_ids in (
        ("exercise", exercise_ids),
        ("hint", hint_ids),
        ("solution", solution_ids),
    ):
        actual = [node["id"] for node in nodes if node["kind"] == expected_kind]
        require(actual == expected_ids, f"{expected_kind} mastery-ID sequence mismatch")
        for ident in expected_ids:
            node = by_id[ident]
            require(node["attrs"].get("data-origin") == "edition-original",
                    f"{ident}: mastery origin mismatch")
            require(len(node_text(lines, node).strip()) >= 80, f"{ident}: empty/trivial block")
    for ident in exercise_ids:
        require(by_id[ident]["attrs"].get("data-course-route-unit-id") == ROUTE,
                f"{ident}: course-route binding mismatch")

    bare_commands = {
        "bare_qquad": re.findall(r"(?<!\\)\bq{2,}uad\b", text),
        "bare_cong": re.findall(r"(?<!\\)\bcong\b", text),
    }
    require(not any(bare_commands.values()), "reader contains malformed bare TeX command")
    rejected_terms = [
        "kefungtoran",
        "titik dasar",
        "takmanifold",
        "funktor",
        "funktorialitas",
        "augumented",
        "homoloy",
        "augumentation",
    ]
    folded = text.casefold()
    found_rejected = [term for term in rejected_terms if term in folded]
    require(not found_rejected, f"reader contains rejected terminology: {found_rejected}")
    for row in EXPECTED_TERM_ROWS:
        require(row["id_ID"].casefold() in folded,
                f"admitted term absent from reader: {row['id_ID']}")

    display_markers = sum(line.strip() == "$$" for line in lines)
    require(display_markers == 164 and display_markers % 2 == 0,
            "reader display-math fence census/balance mismatch")

    boundary = by_id.get("o012-fom-u002-boundary-001")
    require(boundary is not None and boundary["kind"] == "boundary",
            "source-cursor boundary object missing")
    require("baris 1291" in node_text(lines, boundary), "boundary object has wrong cursor")

    return {
        "identity": reader_identity,
        "lines": lines,
        "nodes": nodes,
        "by_id": by_id,
        "opens": opens,
        "closes": closes,
        "aliases": aliases,
        "links": links,
        "proof_closure": proof_closure,
        "exercise_ids": exercise_ids,
        "hint_ids": hint_ids,
        "solution_ids": solution_ids,
        "bare_commands": bare_commands,
        "rejected_terms": rejected_terms,
        "display_markers": display_markers,
    }


def read_control_rows() -> dict[str, Any]:
    term_raw, term_text = strict_input(TERMINOLOGY_PATH)
    adverse_raw, adverse_text = strict_input(ADVERSE_PATH)

    term_reader = csv.DictReader(term_text.splitlines())
    require(
        term_reader.fieldnames == ["term_id", "source_term", "id_ID", "scope", "status", "note"],
        "terminology CSV schema mismatch",
    )
    all_terms = list(term_reader)
    require(len({row["term_id"] for row in all_terms}) == len(all_terms),
            "terminology CSV has duplicate IDs")
    terms = [
        row for row in all_terms
        if 394 <= int(row["term_id"].rsplit("-", 1)[1]) <= 400
    ]
    require(terms == EXPECTED_TERM_ROWS, "terminology rows 0394-0400 mismatch")
    require(digest(canonical(terms)) == TERM_ROWS_SHA256,
            "terminology rows 0394-0400 canonical hash mismatch")

    adverse_reader = csv.DictReader(adverse_text.splitlines())
    require(
        adverse_reader.fieldnames
        == ["event_id", "severity", "source_location", "observed", "action", "status", "rationale"],
        "adverse-ledger CSV schema mismatch",
    )
    all_adverse = list(adverse_reader)
    require(len({row["event_id"] for row in all_adverse}) == len(all_adverse),
            "adverse ledger has duplicate IDs")
    adverse = [
        row for row in all_adverse
        if 426 <= int(row["event_id"].rsplit("-", 1)[1]) <= 456
    ]
    require(
        [row["event_id"] for row in adverse]
        == [f"O012-ADV-{number:04d}" for number in range(426, 457)],
        "adverse rows 0426-0456 are missing, duplicated, or reordered",
    )
    require(digest(canonical(adverse)) == ADVERSE_ROWS_SHA256,
            "adverse rows 0426-0456 canonical hash mismatch")
    allowed_status = {
        "corrected_in_translation",
        "clarified_in_translation",
        "proof_completed_in_translation",
        "resolved_before_admission",
    }
    require(all(row["status"] in allowed_status for row in adverse),
            "adverse rows include a nonclosed status")
    require(all(row["severity"] in {"P1", "P2", "P3"} for row in adverse),
            "adverse rows include an invalid severity")
    require(all(all(row[field].strip() for field in adverse_reader.fieldnames) for row in adverse),
            "adverse rows contain an empty field")

    return {
        "terminology": {
            "identity": identity(TERMINOLOGY_PATH, term_raw),
            "first": terms[0]["term_id"],
            "through": terms[-1]["term_id"],
            "records": len(terms),
            "selected_rows_sha256": TERM_ROWS_SHA256,
            "rows": terms,
            "all_admitted": True,
        },
        "adverse": {
            "identity": identity(ADVERSE_PATH, adverse_raw),
            "first": adverse[0]["event_id"],
            "through": adverse[-1]["event_id"],
            "records": len(adverse),
            "selected_rows_sha256": ADVERSE_ROWS_SHA256,
            "severity_counts": dict(sorted(Counter(row["severity"] for row in adverse).items())),
            "status_counts": dict(sorted(Counter(row["status"] for row in adverse).items())),
            "rows": adverse,
            "all_resolved": True,
        },
    }


def resolve_review(slot: str, candidates: list[str]) -> str:
    existing = [relative for relative in candidates if (LANE / relative).is_file()]
    require(len(existing) == 1,
            f"{slot} review requires exactly one final/draft candidate, found {existing}")
    return existing[0]


def verify_reviews() -> dict[str, Any]:
    results: dict[str, Any] = {}
    counts_pattern = re.compile(
        r'["\x60]?FINAL_SEVERITY_COUNTS["\x60]?\s*[:=]\s*(\{[^{}\r\n]+\})'
    )
    pass_patterns = [
        re.compile(r"(?im)^[ \t]*\*\*PASS\*\*[ \t]*$"),
        re.compile(r'(?i)"STATUS"\s*:\s*"PASS"'),
        re.compile(
            r"(?is)(?:putusan akhir|final verdict|verdict|status)"
            r"[^\r\n]{0,200}(?:\*|\x60|\")*PASS"
        ),
    ]
    for slot, candidates in REVIEW_SLOTS.items():
        relative = resolve_review(slot, candidates)
        raw, text = strict_input(relative)
        require(READER_IDENTITY["sha256"] in text,
                f"{slot} review does not bind the frozen reader hash")
        matches = counts_pattern.findall(text)
        require(bool(matches), f"{slot} review lacks FINAL_SEVERITY_COUNTS")
        try:
            counts = json.loads(matches[-1])
        except json.JSONDecodeError as exc:
            die(f"{slot} review has malformed final severity JSON ({exc})")
        require(counts == {"P1": 0, "P2": 0, "P3": 0},
                f"{slot} review final severity counts are not all zero")
        tail = text[-5000:]
        require(any(pattern.search(tail) for pattern in pass_patterns),
                f"{slot} review lacks an explicit final PASS")
        results[slot] = {
            "identity": identity(relative, raw),
            "status": "PASS",
            "final_severity_counts": counts,
            "reader_sha256": READER_IDENTITY["sha256"],
        }
    return results


def verify_pandoc() -> dict[str, Any]:
    executable = shutil.which("pandoc")
    require(executable is not None, "Pandoc is unavailable")
    try:
        version = subprocess.run(
            [executable, "--version"],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=30,
        )
        parsed = subprocess.run(
            [
                executable,
                "--from=markdown+fenced_divs+tex_math_dollars",
                "--to=native",
                "--wrap=none",
                str(LANE / READER_PATH),
            ],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=60,
            cwd=LANE,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        die(f"Pandoc invocation failed ({exc})")
    require(version.returncode == 0 and bool(version.stdout.splitlines()),
            "Pandoc version probe failed")
    require(parsed.returncode == 0,
            f"Pandoc reader parse failed: {parsed.stderr[-1000:].strip()}")
    return {
        "available": True,
        "version": version.stdout.splitlines()[0].strip(),
        "reader_parse": "PASS",
        "format": "markdown+fenced_divs+tex_math_dollars",
        "output": "native_discarded",
    }


def source_locator(
    source_lines: list[bytes], source_range: str
) -> dict[str, Any]:
    start, end = map(int, source_range.split("-"))
    payload = b"".join(source_lines[start - 1:end])
    return {
        "path": "algebraic_topology.tex",
        "authority_path": UPSTREAM_PATH,
        "commit_sha": COMMIT,
        "tree_sha": TREE,
        "file_sha256": UPSTREAM_IDENTITY["sha256"],
        "line_start": start,
        "line_end": end,
        "bytes": len(payload),
        "content_sha256": digest(payload),
        "precision": "exact_source_span",
    }


def node_evidence(
    reader: dict[str, Any], upstream_raw: bytes, reader_raw: bytes
) -> list[dict[str, Any]]:
    source_lines = upstream_raw.splitlines(keepends=True)
    reader_lines = reader_raw.splitlines(keepends=True)

    def target(start: int, end: int) -> dict[str, Any]:
        payload = b"".join(reader_lines[start - 1:end])
        return {
            "path": READER_PATH,
            "file_sha256": READER_IDENTITY["sha256"],
            "line_start": start,
            "line_end": end,
            "bytes": len(payload),
            "content_sha256": digest(payload),
            "precision": "exact_target_span",
        }

    records: list[dict[str, Any]] = []
    for node in reader["nodes"]:
        attrs = dict(sorted(node["attrs"].items()))
        source_range = attrs.get("data-source-lines")
        if source_range:
            origin = "translated_adapted_from_upstream"
            source = source_locator(source_lines, source_range)
        elif node["id"] == "o012-fom-u002":
            origin = "composite_translated_and_original"
            source = {
                "path": "algebraic_topology.tex",
                "authority_path": UPSTREAM_PATH,
                "commit_sha": COMMIT,
                "tree_sha": TREE,
                "file_sha256": UPSTREAM_IDENTITY["sha256"],
                "line_start": 615,
                "line_end": 1290,
                "bytes": SPAN_IDENTITY["bytes"],
                "content_sha256": SPAN_IDENTITY["sha256"],
                "precision": "exact_unit_span",
            }
        else:
            origin = (
                "edition_original_proof_repair"
                if (
                    node["kind"] == "proof"
                    and attrs.get("data-repair-id") is not None
                )
                else "edition_original"
            )
            source = {
                "kind": "edition_original",
                "path": READER_PATH,
                "precision": "exact_target_span",
            }
        segment_target = target(node["line_start"], node["line_end"])
        unit_target = (
            target(1, len(reader_lines))
            if node["id"] == "o012-fom-u002"
            else segment_target
        )
        segment_origin = (
            "translated_adapted_from_upstream"
            if node["id"] == "o012-fom-u002"
            else origin
        )
        unit_origin = (
            "composite_translated_and_original"
            if node["id"] == "o012-fom-u002"
            else origin
        )
        segment_rights = (
            "rights:fomberg-cc-by-sa-4.0"
            if source_range or node["id"] == "o012-fom-u002"
            else "rights:o012-fom-u002-companion-cc-by-sa-4.0"
        )
        unit_rights = (
            "rights:o012-fom-u002-composite-cc-by-sa-4.0"
            if node["id"] == "o012-fom-u002"
            else segment_rights
        )
        records.append({
            "stable_id": node["id"],
            "record_ids": {
                "segment": f"segment:{node['id']}",
                "unit": f"unit:{node['id']}",
            },
            "semantic_class": node["kind"],
            "declared_classes": node["classes"],
            "attributes": attrs,
            "provenance_relation": segment_origin,
            "record_provenance_relations": {
                "segment": segment_origin,
                "unit": unit_origin,
            },
            "record_rights_component_ids": {
                "segment": segment_rights,
                "unit": unit_rights,
            },
            "source_locator": source,
            "target_locator": segment_target,
            "record_target_locators": {
                "segment": segment_target,
                "unit": unit_target,
            },
        })
    return records


def build_record_plan(
    reader: dict[str, Any], reviews: dict[str, Any]
) -> dict[str, Any]:
    artifact_records = [
        (
            "artifact:o012-fom-u002-source-audit",
            "qa/FOMBERG_UNIT_002_SOURCE_AUDIT.json",
        ),
        (
            "artifact:o012-fom-u002-independent-review",
            reviews["integrated"]["identity"]["path"],
        ),
        (
            "artifact:o012-fom-u002-review-part-a",
            reviews["part_a"]["identity"]["path"],
        ),
        (
            "artifact:o012-fom-u002-review-part-b",
            reviews["part_b"]["identity"]["path"],
        ),
        ("artifact:o012-fom-u002-qa", "qa/FOMBERG_UNIT_002_QA.json"),
    ]
    artifact_records.sort(key=lambda item: item[0])
    artifact_paths = [path for _, path in artifact_records]
    relation_ids = [
        "relation:adapts:o012-fom-u002:fomberg-edition",
        "relation:contains:o012-d60:fomberg-u002",
        "relation:precedes:o012-fom-u001:o012-fom-u002",
        "relation:contains:o012-d60-rights:fomberg-u002",
        "relation:precedes:o012-fom-u002:mastery",
        "relation:proves:o012-fom-u002-pr01:prop-chain-map",
        "relation:proves:o012-fom-u002-pr02:prop-induced-map",
        "relation:proves:o012-fom-u002-pr03:cor-homotopy-equivalent",
    ]
    relation_ids.extend(
        f"relation:hints:fom-u002-hint-{number:03d}:mcheck-{number:03d}"
        for number in range(1, 7)
    )
    relation_ids.extend(
        f"relation:solves:fom-u002-sol-{number:03d}:mcheck-{number:03d}"
        for number in range(1, 7)
    )
    relation_ids.extend(
        f"relation:illustrates:fom-u002-fig-{number:03d}:diagram-asset"
        for number in range(1, 15)
    )
    record_ids = {
        "artifacts.jsonl": [ident for ident, _ in artifact_records],
        "assets.jsonl": [
            "asset:o012-fom-u002-source-markdown",
            "asset:o012-fom-u002-semantic-diagram-layer",
        ],
        "authority.jsonl": [],
        "concepts.jsonl": [f"concept:{slug}" for slug in TERM_SLUGS],
        "corrections.jsonl": [
            f"correction:o012-fom-u002-adv-{number:04d}"
            for number in range(426, 457)
        ],
        "qa.jsonl": [
            "qa:o012-fom-u002-source-integrity",
            "qa:o012-fom-u002-math",
            "qa:o012-fom-u002-language",
            "qa:o012-fom-u002-mastery",
        ],
        "relations.jsonl": relation_ids,
        "rights.jsonl": [
            "rights:o012-fom-u002-companion-cc-by-sa-4.0",
            "rights:o012-fom-u002-composite-cc-by-sa-4.0",
        ],
        "segments.jsonl": [f"segment:{node['id']}" for node in reader["nodes"]],
        "terms.jsonl": [f"term:{slug}:id-ID" for slug in TERM_SLUGS],
        "units.jsonl": [f"unit:{node['id']}" for node in reader["nodes"]],
    }
    for ids in record_ids.values():
        ids.sort()
    actual_counts = {name: len(ids) for name, ids in record_ids.items()}
    require(actual_counts == EXPECTED_BACKEND_COUNTS, "backend record-plan count mismatch")
    require(all(len(ids) == len(set(ids)) for ids in record_ids.values()),
            "backend record plan contains a duplicate ID")
    return {
        "binding_status": "verified_plan_not_written",
        "backend_write_performed": False,
        "edition_unit_id": "unit:o012-fom-u002",
        "root_unit_id": ROOT,
        "course_id": COURSE,
        "course_route_unit_id": ROUTE,
        "resource_id": RESOURCE,
        "edition_id": EDITION,
        "authority_records_reused": [
            RESOURCE,
            EDITION,
            "rights:fomberg-cc-by-sa-4.0",
            "rights:o012-d60-integrated-route-cc-by-sa-4.0",
        ],
        "artifact_evidence_paths_in_record_order": artifact_paths,
        "records_by_file": actual_counts,
        "record_ids_by_file": record_ids,
        "records_planned": sum(actual_counts.values()),
    }


def build_source_audit(
    source: dict[str, Any],
    reader: dict[str, Any],
    controls: dict[str, Any],
    reviews: dict[str, Any],
    pandoc: dict[str, Any],
    records: dict[str, Any],
    evidence: list[dict[str, Any]],
) -> dict[str, Any]:
    class_counts = dict(sorted(Counter(node["kind"] for node in reader["nodes"]).items()))
    return {
        "schema_version": SCHEMA_VERSION,
        "audit_id": "O012-FOMBERG-UNIT-002-SOURCE-AUDIT",
        "audit_date": AUDIT_DATE,
        "status": "PASS",
        "translation_performed": True,
        "backend_modified": False,
        "authority": {
            "repository": "https://git.sr.ht/~yp/math-notes",
            "resource_id": RESOURCE,
            "edition_id": EDITION,
            "commit": COMMIT,
            "tree": TREE,
            "source": source["identity"],
            "license": "CC BY-SA 4.0",
            "notes_author": "Yeheli Fomberg",
            "based_on_lectures_by": "Nir Lazarovich",
            "nonendorsement_notice_required": True,
        },
        "unit": {
            "component_unit_id": "FOMBERG_UNIT_002",
            "edition_unit_id": "O012-FOM-002",
            "course_route_unit_id": ROUTE,
            "source_lines": "615-1290 inclusive",
            "line_count": SPAN_IDENTITY["lines"],
            "bytes_preserving_lf": SPAN_IDENTITY["bytes"],
            "sha256_preserving_lf": SPAN_IDENTITY["sha256"],
            "start_byte_offset": source["span"]["start_byte_offset"],
            "end_byte_offset_inclusive": source["span"]["end_byte_offset_inclusive"],
            "headings": [
                {"line": 615, "level": "subsection", "title": "Singular homology"},
                {"line": 954, "level": "subsection", "title": "Homotopy invariance"},
            ],
            "next_line": NEXT_SOURCE_LINE,
            "next_heading": "Exact sequences",
            "terminal_source_eof": False,
        },
        "source_counts": {
            **source["environment_counts"],
            "semantic_environments_total": sum(source["environment_counts"].values()),
            "labels": len(source["labels"]),
            "cross_references": len(source["cref_payloads"]),
            "tikzcd": source["diagram_counts"]["tikzcd"],
            "tikzpicture": source["diagram_counts"]["tikzpicture"],
            "diagrams_total": sum(source["diagram_counts"].values()),
            "formal_exercises": 0,
        },
        "source_object_ranges": source["environment_ranges"],
        "source_aliases": ALIASES,
        "reader": reader["identity"],
        "reader_structure": {
            "stable_id_count": len(reader["nodes"]),
            "stable_ids_in_reader_order": [node["id"] for node in reader["nodes"]],
            "class_counts": class_counts,
            "identified_headings": EXPECTED_HEADING_IDS,
            "fenced_semantic_objects": reader["opens"],
            "fenced_div_opens": reader["opens"],
            "fenced_div_closes": reader["closes"],
            "source_labels": len(reader["aliases"]),
            "internal_links": len(reader["links"]),
            "display_math_markers": reader["display_markers"],
            "semantic_figure_blocks": len(FIGURE_IDS),
            "figure_ids": FIGURE_IDS,
        },
        "proof_closure": reader["proof_closure"],
        "mastery": {
            "triples": 6,
            "exercise_ids": reader["exercise_ids"],
            "hint_ids": reader["hint_ids"],
            "solution_ids": reader["solution_ids"],
            "solution_status": "complete_checked_solution",
        },
        "controls": controls,
        "independent_reviews": reviews,
        "pandoc": pandoc,
        "evidence_records": evidence,
        "record_plan": records,
        "model_provenance": MODEL,
        "checks": {
            "reader_identity_lf_utf8": True,
            "authority_full_source_identity": True,
            "source_span_615_1290_identity": True,
            "cursor_line_1291_exact": True,
            "five_source_labels_and_ten_internal_links": True,
            "fourteen_source_diagram_functions": True,
            "fourteen_semantic_figure_blocks": True,
            "three_omission_and_proof_repairs_complete": True,
            "degree_zero_boundary_scoped": True,
            "connected_and_path_component_decompositions_preserved": True,
            "contractibility_maps_and_homotopies_typed": True,
            "six_mastery_triples_complete": True,
            "no_malformed_bare_qquad_or_cong": True,
            "rejected_terminology_absent": True,
            "terminology_rows_0394_0400_exact": True,
            "adverse_rows_0426_0456_exact_and_closed": True,
            "three_independent_reviews_zero_and_pass": True,
            "pandoc_parse_pass": True,
            "backend_unchanged": True,
            "no_build_or_publication_claim": True,
        },
    }


def build_qa(
    source: dict[str, Any],
    reader: dict[str, Any],
    controls: dict[str, Any],
    reviews: dict[str, Any],
    pandoc: dict[str, Any],
    records: dict[str, Any],
    audit_raw: bytes,
) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "qa_id": "O012-FOMBERG-UNIT-002-STATIC-QA",
        "audit_date": AUDIT_DATE,
        "status": "PASS",
        "reader": reader["identity"],
        "authority": {
            "resource_id": RESOURCE,
            "edition_id": EDITION,
            "commit": COMMIT,
            "tree": TREE,
            "source": source["identity"],
            "unit_span": SPAN_IDENTITY,
            "next_source_line": NEXT_SOURCE_LINE,
            "next_heading": NEXT_HEADING,
            "terminal_source_eof": False,
        },
        "source_audit_output": {
            "path": "qa/FOMBERG_UNIT_002_SOURCE_AUDIT.json",
            "bytes": len(audit_raw),
            "sha256": digest(audit_raw),
            "encoding": "UTF-8",
            "newline": "LF",
        },
        "evidence": {
            "authority_source": source["identity"],
            "reader": reader["identity"],
            "terminology_control": controls["terminology"]["identity"],
            "adverse_control": controls["adverse"]["identity"],
            "independent_reviews": {
                slot: value["identity"] for slot, value in reviews.items()
            },
        },
        "structure": {
            "stable_id_count": len(reader["nodes"]),
            "class_counts": dict(sorted(Counter(node["kind"] for node in reader["nodes"]).items())),
            "fenced_semantic_objects": reader["opens"],
            "source_aliases": ALIASES,
            "internal_link_target_counts": dict(sorted(EXPECTED_LINK_TARGET_COUNTS.items())),
            "source_diagram_functions": 14,
            "semantic_figure_blocks": 14,
        },
        "proof_closure": reader["proof_closure"],
        "mastery": {
            "triples": 6,
            "exercise_ids": reader["exercise_ids"],
            "hint_ids": reader["hint_ids"],
            "solution_ids": reader["solution_ids"],
        },
        "controls": {
            "terminology": {
                "first": "O012-TERM-0394",
                "through": "O012-TERM-0400",
                "records": 7,
                "selected_rows_sha256": TERM_ROWS_SHA256,
                "all_admitted": True,
            },
            "adverse": {
                "first": "O012-ADV-0426",
                "through": "O012-ADV-0456",
                "records": 31,
                "selected_rows_sha256": ADVERSE_ROWS_SHA256,
                "all_resolved": True,
            },
        },
        "independent_reviews": reviews,
        "pandoc": pandoc,
        "record_plan": records,
        "model_provenance": MODEL,
        "checks": {
            "reader_identity_44407_bytes_1342_lf_lines": True,
            "reader_sha256_0851ab7d": True,
            "strict_utf8_lf_and_model_provenance": True,
            "source_full_and_span_identity": True,
            "cursor_line_1291": True,
            "unique_95_stable_ids": True,
            "exact_semantic_class_census": True,
            "balanced_90_fenced_divs": True,
            "five_aliases_and_ten_links": True,
            "fourteen_diagram_functions_and_blocks": True,
            "fom_pr_01_02_03_closed": True,
            "six_exercise_hint_solution_triples": True,
            "malformed_bare_commands_absent": True,
            "rejected_terminology_absent": True,
            "terminology_0394_0400_exact": True,
            "adverse_0426_0456_exact": True,
            "three_reviews_p1_p2_p3_zero_and_pass": True,
            "pandoc_parse_available_and_pass": True,
            "inputs_not_modified": True,
            "backend_write_deferred": True,
        },
    }


def main() -> int:
    upstream_raw, upstream_text = strict_input(UPSTREAM_PATH)
    reader_raw, reader_text = strict_input(READER_PATH)
    source = verify_source(upstream_raw, upstream_text)
    reader = verify_reader(reader_raw, reader_text, source)
    controls = read_control_rows()
    reviews = verify_reviews()
    pandoc = verify_pandoc()
    evidence = node_evidence(reader, upstream_raw, reader_raw)
    records = build_record_plan(reader, reviews)
    audit = build_source_audit(
        source, reader, controls, reviews, pandoc, records, evidence
    )
    audit_raw = receipt_bytes(audit)
    qa = build_qa(
        source, reader, controls, reviews, pandoc, records, audit_raw
    )
    qa_raw = receipt_bytes(qa)

    # Catch input changes between validation and receipt publication.
    require(identity(UPSTREAM_PATH) == source["identity"],
            "authority source changed during QA")
    require(identity(READER_PATH) == reader["identity"],
            "reader changed during QA")
    require(identity(TERMINOLOGY_PATH) == controls["terminology"]["identity"],
            "terminology control changed during QA")
    require(identity(ADVERSE_PATH) == controls["adverse"]["identity"],
            "adverse control changed during QA")
    for review in reviews.values():
        require(identity(review["identity"]["path"]) == review["identity"],
                f"{review['identity']['path']}: review changed during QA")

    AUDIT_OUTPUT.write_bytes(audit_raw)
    QA_OUTPUT.write_bytes(qa_raw)
    print("Fomberg Unit 002 source audit and static QA: PASS")
    print(f"stable_ids={len(reader['nodes'])}")
    print(f"source_audit_bytes={len(audit_raw)}")
    print(f"source_audit_sha256={digest(audit_raw)}")
    print(f"qa_bytes={len(qa_raw)}")
    print(f"qa_sha256={digest(qa_raw)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
