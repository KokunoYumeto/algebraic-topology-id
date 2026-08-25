#!/usr/bin/env python3
"""Fail-closed source and static-QA receipts for Fomberg Unit 003.

The program reads but never alters its authority, reader, control, asset, or
review inputs.  It writes the two declared JSON receipts only after every
check has passed.  The frozen integrated review's one counting defect (124
instead of 125 IDs) is preserved and superseded only for that field by a
separate, hash-bound reconciliation.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import shlex
import shutil
import struct
import subprocess
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path
from typing import Any


LANE = Path(__file__).resolve().parents[1]
AUDIT_OUTPUT = LANE / "qa/FOMBERG_UNIT_003_SOURCE_AUDIT.json"
QA_OUTPUT = LANE / "qa/FOMBERG_UNIT_003_QA.json"

SCHEMA_VERSION = "1.0.0"
AUDIT_DATE = "2026-08-25"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"
COMMIT = "563194fae879178b9a6871b249513bfc27968975"
TREE = "fb678966d1533d529bdd72f49d8496a3bdc14a9b"
RESOURCE = "resource:fomberg-algebraic-topology-2025"
EDITION = "edition:fomberg-at-2025-563194f"
ROOT = "unit:o012-fom-u003"
COURSE = "course:o012-d60"
ROUTE = "D60-R10"

READER_PATH = (
    "source/id-ID/fomberg/units/"
    "fomberg-unit-003-exact-sequences-relative-homology.md"
)
PRIOR_READER_PATH = (
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
DRAFT_AUDIT_PATH = "qa/FOMBERG_UNIT_003_SOURCE_AUDIT_DRAFT.json"
RECONCILIATION_PATH = (
    "qa/fomberg-unit-003/INTEGRATED_REVIEW_COUNT_RECONCILIATION.json"
)

READER_IDENTITY = {
    "bytes": 65540,
    "lf_lines": 1773,
    "sha256": "2571f62b977c00bff20e04756925a73497c0129f8c987940db0e1a649177f6b9",
}
PRIOR_READER_IDENTITY = {
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
    "line_start": 1291,
    "line_end": 1922,
    "lines": 632,
    "bytes": 24270,
    "sha256": "870e617b30b82eb8a557b0733096623a73375ed079601e7e7938ce489d0ce064",
}
EXACT_SPAN_IDENTITY = {
    "line_start": 1291,
    "line_end": 1564,
    "lines": 274,
    "bytes": 10012,
    "sha256": "61767c5ad71ecc9a19eca96a65b1c56e02a5a6f0d3f38e51783bd07fc10f2f0a",
}
RELATIVE_SPAN_IDENTITY = {
    "line_start": 1565,
    "line_end": 1922,
    "lines": 358,
    "bytes": 14258,
    "sha256": "e5b4d4a1e1f927ba6cf8859e262a419205a84d133523e6bb6c65ac532d9abd35",
}
NEXT_SOURCE_LINE = 1923
NEXT_HEADING = r"\subsection{Excisions}"

CONTROL_IDENTITIES = {
    TERMINOLOGY_PATH: {
        "bytes": 49864,
        "lf_lines": 416,
        "sha256": "5374b6073eadda56e8ad752fd7ec65c1459f58054125f53a7343ecdd0adaf9a1",
    },
    ADVERSE_PATH: {
        "bytes": 167596,
        "lf_lines": 499,
        "sha256": "0eee620b74dbfb3f6ee4d2030f6ca77c7ae4cf169fd09a604c82bb29895e5a3b",
    },
}
DRAFT_AUDIT_IDENTITY = {
    "bytes": 53271,
    "lf_lines": 1365,
    "sha256": "3e3fcaf430f456bf9c926cbd159185a118e1a64d3dfa363c974c82eb6f077e99",
}
RECONCILIATION_IDENTITY = {
    "bytes": 2013,
    "lf_lines": 59,
    "sha256": "48fd3133d1136d6c102960f0e269ed6090fd8cb62ec353bf2f69853bb8415243",
}

EXPECTED_ID_SEQUENCE_SHA256 = (
    "402c61516d156e8106990cc5f26d77f8eba66049603f9280206801d53173d5ff"
)
EXPECTED_HEADING_IDS = [
    "o012-fom-u003-notice",
    "o012-fom-u003",
    "o012-fom-u003-s05",
    "o012-fom-u003-source-corrections",
    "o012-fom-u003-s06",
    "o012-fom-u003-mastery",
]
EXPECTED_HEADING_CLASSES = {
    "o012-fom-u003-notice": ["unnumbered"],
    "o012-fom-u003": [],
    "o012-fom-u003-s05": [],
    "o012-fom-u003-source-corrections": ["unnumbered"],
    "o012-fom-u003-s06": [],
    "o012-fom-u003-mastery": [],
}
EXPECTED_CLASS_COUNTS = {
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
FIGURE_IDS = [
    "o012-fom-u003-fig-exact-sequence",
    "o012-fom-u003-fig-injective",
    "o012-fom-u003-fig-surjective",
    "o012-fom-u003-fig-isomorphism",
    "o012-fom-u003-fig-short-exact",
    "o012-fom-u003-fig-les-quotient",
    "o012-fom-u003-fig-disk-boundary-les",
    "o012-fom-u003-fig-sphere-short-exact-first",
    "o012-fom-u003-fig-sphere-short-exact",
    "o012-fom-u003-fig-circle-cone",
    "o012-fom-u003-fig-circle-suspension",
    "o012-fom-u003-fig-cone-les",
    "o012-fom-u003-fig-suspension-short-exact",
    "o012-fom-u003-fig-brouwer-retraction",
    "o012-fom-u003-fig-relative-cycle",
    "o012-fom-u003-fig-relative-boundary",
    "o012-fom-u003-fig-formal-relative-chains",
    "o012-fom-u003-fig-relative-chain-square",
    "o012-fom-u003-fig-short-exact-complexes",
    "o012-fom-u003-fig-long-exact-statement",
    "o012-fom-u003-fig-pair-long-exact",
    "o012-fom-u003-fig-chain-complex-ladder",
    "o012-fom-u003-fig-cycle-target-check",
    "o012-fom-u003-fig-reduced-point-sequence",
    "o012-fom-u003-fig-triple-long-exact",
    "o012-fom-u003-fig-triple-short-exact",
]

SOURCE_ENVIRONMENT_COUNTS = {
    "definition": 7,
    "theorem": 2,
    "corollary": 4,
    "proposition": 1,
    "lemma": 0,
    "proof": 4,
    "proofof": 1,
    "example": 7,
    "remark": 13,
}
SOURCE_DEFINED_ALIASES = {
    "exmp:short-exact-sequence-isomorphism": "o012-fom-u003-ex-isomorphism",
    "thm:les-of-quotient-space": "o012-fom-u003-thm-les-quotient",
    "cor:homologies-of-spheres": "o012-fom-u003-cor-sphere-homology",
    "thm:long-exact-consequence": "o012-fom-u003-thm-long-exact",
}
ALL_SOURCE_ALIASES = {
    **SOURCE_DEFINED_ALIASES,
    "cor:injective-i-surjective-r": "o012-fom-u002-cor-retract",
    "thm:homotopic-maps-induce-same-homomorphism-on-homology":
        "o012-fom-u002-thm-homotopy-invariance",
}
EXPECTED_SOURCE_REF_TARGET_COUNTS = Counter({
    "o012-fom-u003-thm-les-quotient": 2,
    "o012-fom-u003-ex-isomorphism": 2,
    "o012-fom-u003-cor-sphere-homology": 1,
    "o012-fom-u002-cor-retract": 1,
    "o012-fom-u002-thm-homotopy-invariance": 1,
    "o012-fom-u003-thm-long-exact": 3,
})
EXPECTED_READER_LINK_TARGET_COUNTS = Counter({
    "o012-fom-u003-thm-les-quotient": 2,
    "o012-fom-u003-ex-isomorphism": 2,
    "o012-fom-u003-cor-sphere-homology": 1,
    "o012-fom-u003-thm-long-exact": 4,
    "o012-fom-u002-thm-homotopy-invariance": 1,
})

TERM_ROWS_SHA256 = "e9a4c8fd4e36bc80cea6d29f87ed309dda3ee05bd4e8fd1e3db14f5423631b7a"
ADVERSE_ROWS_SHA256 = "c584c4286ff2e27c15e990f47b333ed2b332b69993e638380ff140ce076c7e8c"
EXPECTED_TERM_ROWS = [
    {"term_id": "O012-TERM-0401", "source_term": "good pair", "id_ID": "pasangan baik", "scope": "algebraic_topology", "status": "admitted", "note": "A has an open neighborhood in X that deformation-retracts onto A"},
    {"term_id": "O012-TERM-0402", "source_term": "cone", "id_ID": "kerucut", "scope": "algebraic_topology", "status": "admitted", "note": "CX is X times the unit interval with the top face collapsed to the cone vertex"},
    {"term_id": "O012-TERM-0403", "source_term": "suspension", "id_ID": "suspensi", "scope": "algebraic_topology", "status": "admitted", "note": "SX is the cone with its base also collapsed; distinguish from the cone itself"},
    {"term_id": "O012-TERM-0404", "source_term": "relative chain group", "id_ID": "grup rantai relatif", "scope": "homological_algebra", "status": "admitted", "note": "quotient C_n(X) modulo C_n(A)"},
    {"term_id": "O012-TERM-0405", "source_term": "relative homology", "id_ID": "homologi relatif", "scope": "algebraic_topology", "status": "admitted", "note": "homology of the relative chain complex C_*(X,A)"},
    {"term_id": "O012-TERM-0406", "source_term": "relative cycle", "id_ID": "siklus relatif", "scope": "homological_algebra", "status": "admitted", "note": "a relative chain whose boundary vanishes modulo chains in A"},
    {"term_id": "O012-TERM-0407", "source_term": "relative boundary", "id_ID": "batas relatif", "scope": "homological_algebra", "status": "admitted", "note": "a boundary in the quotient chain complex C_*(X,A)"},
    {"term_id": "O012-TERM-0408", "source_term": "homotopy through maps of pairs", "id_ID": "homotopi melalui peta pasangan", "scope": "algebraic_topology", "status": "admitted", "note": "requires F(A times I) to be contained in B; unlike homotopy relative to A it need not fix A pointwise"},
    {"term_id": "O012-TERM-0409", "source_term": "commutative diagram", "id_ID": "diagram komutatif", "scope": "category_theory", "status": "admitted", "note": "a diagram in which all directed path composites with common endpoints agree"},
    {"term_id": "O012-TERM-0410", "source_term": "injective", "id_ID": "injektif", "scope": "algebra", "status": "admitted", "note": "a map with trivial equality fibres"},
    {"term_id": "O012-TERM-0411", "source_term": "surjective", "id_ID": "surjektif", "scope": "algebra", "status": "admitted", "note": "a map whose image is the entire codomain"},
    {"term_id": "O012-TERM-0412", "source_term": "inclusion map", "id_ID": "pemetaan inklusi", "scope": "topology", "status": "admitted", "note": "the canonical map of a subspace into its ambient space"},
    {"term_id": "O012-TERM-0413", "source_term": "basis", "id_ID": "basis", "scope": "algebra", "status": "admitted", "note": "a generating family with unique finite linear expressions"},
    {"term_id": "O012-TERM-0414", "source_term": "topological boundary", "id_ID": "batas topologis", "scope": "topology", "status": "admitted", "note": "use when needed to distinguish the boundary of D^n from the chain boundary operator"},
    {"term_id": "O012-TERM-0415", "source_term": "long exact sequence of a triple", "id_ID": "barisan eksak panjang tripel", "scope": "homological_algebra", "status": "admitted", "note": "the long exact sequence associated with B contained in A contained in X"},
]
TERM_SLUGS = [
    "good-pair", "cone", "suspension", "relative-chain-group",
    "relative-homology", "relative-cycle", "relative-boundary",
    "homotopy-through-maps-of-pairs", "commutative-diagram", "injective",
    "surjective", "inclusion-map", "basis", "topological-boundary",
    "long-exact-sequence-of-triple",
]

REVIEW_SPECS = {
    "exact_initial": {
        "path": "qa/fomberg-unit-003/INDEPENDENT_REVIEW_EXACT.json",
        "bytes": 14012, "lf_lines": 314,
        "sha256": "58001c6a54d1328f5bacae65e26fdcef5043e4c03c1732a2eaad274825e770bf",
        "status": "P2_REPAIR_REQUIRED", "phase": "initial",
    },
    "exact_final": {
        "path": "qa/fomberg-unit-003/INDEPENDENT_REVIEW_EXACT_FINAL.json",
        "bytes": 11017, "lf_lines": 257,
        "sha256": "360d84f2deb75445e698050c9e968284612ec087bfec606dfc63427b069c5e5d",
        "status": "PASS_ZERO_FINDINGS", "phase": "final",
    },
    "relative_initial": {
        "path": "qa/fomberg-unit-003/INDEPENDENT_REVIEW_RELATIVE.json",
        "bytes": 8734, "lf_lines": 203,
        "sha256": "2de6d94e4ac9dc5353cdb9d54687ee01f45aae4eb30f3ccf6dcab62910f12dec",
        "status": "PASS_WITH_REQUIRED_P2_CORRECTION", "phase": "initial",
    },
    "relative_final": {
        "path": "qa/fomberg-unit-003/INDEPENDENT_REVIEW_RELATIVE_FINAL.json",
        "bytes": 11409, "lf_lines": 278,
        "sha256": "5471e6ee304713da288d075fb1e506c6b2125f4e7090740044f181fb31bf97fb",
        "status": "PASS_ZERO_FINDINGS", "phase": "final",
    },
    "integrated_initial": {
        "path": "qa/fomberg-unit-003/INDEPENDENT_REVIEW_INTEGRATED.json",
        "bytes": 9103, "lf_lines": 167,
        "sha256": "e680d802b4125909d670100079dc8cd09c4766742879382e72e5c695c604d9d4",
        "status": "CHANGES_REQUESTED", "phase": "initial",
    },
    "integrated_final": {
        "path": "qa/fomberg-unit-003/INDEPENDENT_REVIEW_INTEGRATED_FINAL.json",
        "bytes": 12424, "lf_lines": 269,
        "sha256": "eec178895fde82ffd3dfff04f3167bdf3fa276f5352c11e5db2a4cf7ea8f06f5",
        "status": "PASS_ZERO_FINDINGS", "phase": "final",
    },
}

ASSET_SPECS = {
    "brouwer-radial-retraction.png": (180164, "97b0745e2b31b911fa777bdade3d51d88f5247a4d1d9cf29bf1c4aedc5f287c1", (1018, 800)),
    "brouwer-radial-retraction.svg": (1359, "34170760d9179f61ec3ece881e21e83a5a1556ddc86a781d163ff76d796b0885", None),
    "cone-circle.png": (37062, "40b452e48da782626b1b75425e57d4dd3ee202d337f3d8189db395077a1eaf35", (960, 720)),
    "cone-circle.svg": (1092, "ee45855df1ad90ea6e2fdf26f3a4790ab60e1c3fab194a597a612f1a9ddb7b83", None),
    "relative-boundary.png": (291686, "20393edd49cb9fa29dade8fbae82387ee7eaa955ed1161648f9292f40e9af6f9", (1200, 759)),
    "relative-boundary.svg": (1899, "ec7af0378a1a92ddecda8cf27fd13cd73a68079e6286d845c441434e7a945eb4", None),
    "relative-chains-formal.png": (297867, "c9789bf829f308bbd3b80350d510f9c26c2c03d2878e7133dfa46b0395cbdefa", (1200, 737)),
    "relative-chains-formal.svg": (2565, "ca5e9d78c07579b0bf5b162fbe21769d2eb16bc590179d3a6765e3ad973e57b9", None),
    "relative-cycle.png": (260456, "e7057f0cc58dbe48eac8369e04f61fea9c5974dc1882f4ca53a3532c5ccc9e7f", (1200, 741)),
    "relative-cycle.svg": (1671, "e3ef9ef498f8e379cca12b4d769c35f5b90d4c823860b8ef7249ace19d12e459", None),
    "suspension-circle.png": (148311, "ad79445d601905192911cc3ee7e8457bb00bae17e7ece767798c2316709cfa3d", (800, 800)),
    "suspension-circle.svg": (1350, "2c31c274111fc3a059868a58e39035782fcbae73389975bacab65c8797a8cdef", None),
}
REDRAW_MAP = {
    "o012-fom-u003-fig-circle-cone": "cone-circle.png",
    "o012-fom-u003-fig-circle-suspension": "suspension-circle.png",
    "o012-fom-u003-fig-brouwer-retraction": "brouwer-radial-retraction.png",
    "o012-fom-u003-fig-relative-cycle": "relative-cycle.png",
    "o012-fom-u003-fig-relative-boundary": "relative-boundary.png",
    "o012-fom-u003-fig-formal-relative-chains": "relative-chains-formal.png",
}


def die(message: str) -> None:
    raise SystemExit(f"Fomberg Unit 003 QA FAIL: {message}")


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
        if field in expected:
            require(
                actual[field] == expected[field],
                f"{relative}: {field} {actual[field]!r} != {expected[field]!r}",
            )
    return actual


def no_duplicate_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    obj: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in obj, f"JSON duplicate key {key!r}")
        obj[key] = value
    return obj


def strict_json(relative: str, expected: dict[str, Any]) -> tuple[bytes, dict[str, Any]]:
    raw, text = strict_input(relative)
    ident = require_identity(relative, raw, expected)
    try:
        obj = json.loads(text, object_pairs_hook=no_duplicate_object)
    except json.JSONDecodeError as exc:
        die(f"{relative}: malformed JSON ({exc})")
    require(isinstance(obj, dict), f"{relative}: top-level JSON object required")
    return raw, {"identity": ident, "object": obj}


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
            require(key and key not in attrs, f"{where}: duplicate/empty attribute")
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
            ident, classes, attrs = parse_attributes(
                opener_match.group(2)[1:-1].strip(),
                f"reader line {number} fenced div",
            )
            require(len(classes) == 1, f"reader line {number}: one semantic class required")
            node = {
                "id": ident,
                "kind": classes[0],
                "classes": classes,
                "attrs": attrs,
                "title": "",
                "line_start": number,
                "line_end": 0,
                "fence_length": len(opener_match.group(1)),
            }
            stack.append(node)
            opens += 1
            continue

        close_match = re.match(r"^(:{3,})[ \t]*$", line)
        if close_match:
            require(bool(stack), f"reader line {number}: unmatched fenced-div close")
            node = stack.pop()
            require(
                len(close_match.group(1)) == node["fence_length"],
                f"reader line {number}: nested fenced-div delimiter mismatch",
            )
            node["line_end"] = number
            del node["fence_length"]
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

    boundary_nodes = [node for node in fences if node["id"] == "o012-fom-u003-boundary-001"]
    require(len(boundary_nodes) == 1, "reader cursor-boundary census mismatch")
    heading_by_id = {node["id"]: node for node in headings}
    heading_by_id["o012-fom-u003-mastery"]["line_end"] = (
        boundary_nodes[0]["line_start"] - 1
    )

    nodes = sorted(headings + fences, key=lambda node: (node["line_start"], node["line_end"]))
    ids = [node["id"] for node in nodes]
    require(len(ids) == 125, f"reader declares {len(ids)} IDs, expected 125")
    require(len(ids) == len(set(ids)), "reader stable IDs are not unique")
    require(all(ident.startswith("o012-fom-u003") for ident in ids),
            "reader contains an ID outside the Unit 003 namespace")
    require(digest(canonical(ids)) == EXPECTED_ID_SEQUENCE_SHA256,
            "reader ordered stable-ID inventory hash mismatch")
    require(opens == 119 and closes == 119, "reader fenced-div count is not 119/119")
    class_counts = dict(sorted(Counter(node["kind"] for node in nodes).items()))
    require(class_counts == EXPECTED_CLASS_COUNTS, "reader semantic-class census mismatch")
    require([node["id"] for node in headings] == EXPECTED_HEADING_IDS,
            "reader heading-ID order mismatch")
    require({node["id"]: node["classes"] for node in headings} == EXPECTED_HEADING_CLASSES,
            "reader heading-class declarations mismatch")

    for node in nodes:
        source_range = node["attrs"].get("data-source-lines")
        if source_range is not None:
            match = re.fullmatch(r"([0-9]+)-([0-9]+)", source_range)
            require(match is not None, f"{node['id']}: malformed source locator")
            start, end = map(int, match.groups())
            require(1291 <= start <= end <= 1922, f"{node['id']}: locator out of span")
        origin = node["attrs"].get("data-origin")
        require(origin in (None, "edition-original"), f"{node['id']}: invalid origin")

    raw_lines = raw.splitlines(keepends=True)
    for node in nodes:
        payload = b"".join(raw_lines[node["line_start"] - 1:node["line_end"]])
        node["target_content_bytes"] = len(payload)
        node["target_content_sha256"] = digest(payload)
    return lines, nodes, opens, closes


def node_text(lines: list[str], node: dict[str, Any]) -> str:
    return "\n".join(lines[node["line_start"] - 1:node["line_end"]]) + "\n"


def environment_ranges(lines: list[str], kind: str, absolute_start: int) -> list[str]:
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


def normalized_span(lines: list[str], start: int, end: int) -> bytes:
    return ("\n".join(lines[start - 1:end]) + "\n").encode("utf-8")


def verify_span(raw: bytes, expected: dict[str, Any], label: str) -> None:
    require(raw.count(b"\n") == expected["lines"], f"{label}: line mismatch")
    require(len(raw) == expected["bytes"], f"{label}: byte mismatch")
    require(digest(raw) == expected["sha256"], f"{label}: hash mismatch")


def verify_source(raw: bytes, text: str) -> dict[str, Any]:
    source_identity = require_identity(UPSTREAM_PATH, raw, UPSTREAM_IDENTITY)
    lines = text.splitlines()
    require(len(lines) == 6069, "authority physical-line count mismatch")
    require(lines[1290] == r"\subsection{Exact sequences}", "source line 1291 mismatch")
    require(lines[1563] == "", "source line 1564 is not the frozen blank boundary")
    require(lines[1564] == r"\subsection{Relative homology}", "source line 1565 mismatch")
    require(lines[1922] == NEXT_HEADING, "source cursor line 1923 mismatch")

    span_raw = normalized_span(lines, 1291, 1922)
    exact_raw = normalized_span(lines, 1291, 1564)
    relative_raw = normalized_span(lines, 1565, 1922)
    verify_span(span_raw, SPAN_IDENTITY, "source unit span")
    verify_span(exact_raw, EXACT_SPAN_IDENTITY, "source exact-sequence span")
    verify_span(relative_raw, RELATIVE_SPAN_IDENTITY, "source relative-homology span")
    span_lines = lines[1290:1922]
    span_text = span_raw.decode("utf-8")

    ranges = {kind: environment_ranges(span_lines, kind, 1291)
              for kind in SOURCE_ENVIRONMENT_COUNTS}
    counts = {kind: len(values) for kind, values in ranges.items()}
    require(counts == SOURCE_ENVIRONMENT_COUNTS, "source environment census mismatch")
    require(sum(counts.values()) == 39, "source semantic-environment total mismatch")

    labels = re.findall(r"\\label\{([^{}]+)\}", span_text)
    require(labels == list(SOURCE_DEFINED_ALIASES), "source label inventory/order mismatch")
    cref_payloads = re.findall(r"\\Cref\{([^{}]+)\}", span_text)
    require(len(cref_payloads) == 10, "source Cref-command count mismatch")
    ref_labels = [key.strip() for payload in cref_payloads for key in payload.split(",") if key.strip()]
    require(len(ref_labels) == 10, "source Cref target count mismatch")
    require(all(key in ALL_SOURCE_ALIASES for key in ref_labels), "unknown source Cref target")
    mapped = Counter(ALL_SOURCE_ALIASES[key] for key in ref_labels)
    require(mapped == EXPECTED_SOURCE_REF_TARGET_COUNTS, "source Cref multiplicity mismatch")

    diagrams = {
        "tikzcd": len(re.findall(r"\\begin\{tikzcd\}", span_text)),
        "tikzpicture": len(re.findall(r"\\begin\{tikzpicture\}", span_text)),
        "inline_tikz": len(re.findall(r"\\tikz\[", span_text)),
    }
    require(diagrams == {"tikzcd": 23, "tikzpicture": 4, "inline_tikz": 2},
            "source diagram census mismatch")
    require(span_text.count(r"\end{tikzcd}") == 23
            and span_text.count(r"\end{tikzpicture}") == 4,
            "source diagram environment is unbalanced")
    require(not re.search(r"\\begin\{exercise\}", span_text),
            "source span unexpectedly contains a formal exercise")

    prefix_raw = normalized_span(lines, 1, 1290)
    require(len(prefix_raw) == 45470, "source unit start-byte offset mismatch")
    require(len(prefix_raw) + len(span_raw) - 1 == 69739,
            "source unit inclusive end-byte offset mismatch")
    return {
        "identity": source_identity,
        "span_raw": span_raw,
        "span_lines": span_lines,
        "span": {
            **SPAN_IDENTITY,
            "start_byte_offset": len(prefix_raw),
            "end_byte_offset_inclusive": len(prefix_raw) + len(span_raw) - 1,
        },
        "exact_span": EXACT_SPAN_IDENTITY,
        "relative_span": RELATIVE_SPAN_IDENTITY,
        "environment_counts": counts,
        "environment_ranges": ranges,
        "labels": labels,
        "cref_payloads": cref_payloads,
        "mapped_ref_counts": dict(sorted(mapped.items())),
        "diagram_counts": diagrams,
    }


def verify_draft_audit(source: dict[str, Any]) -> dict[str, Any]:
    raw, result = strict_json(DRAFT_AUDIT_PATH, DRAFT_AUDIT_IDENTITY)
    obj = result["object"]
    require(obj.get("status") == "DRAFT_SOURCE_AUDIT_COMPLETE", "draft audit status mismatch")
    require(obj.get("translation_performed") is False, "draft audit phase mismatch")
    require(obj.get("authority", {}).get("commit") == COMMIT, "draft audit commit mismatch")
    unit = obj.get("unit", {})
    require(unit.get("source_lines") == "1291-1922 inclusive", "draft audit span mismatch")
    require(unit.get("sha256_preserving_lf") == SPAN_IDENTITY["sha256"],
            "draft audit source-span hash mismatch")
    require(unit.get("next_line_exact_text") == NEXT_HEADING, "draft audit cursor mismatch")
    counts = obj.get("source_counts", {})
    for kind, value in SOURCE_ENVIRONMENT_COUNTS.items():
        require(counts.get(kind) == value, f"draft audit source count mismatch: {kind}")
    require(counts.get("semantic_environments_total") == 39, "draft semantic total mismatch")
    require(counts.get("diagrams_total") == 29, "draft diagram total mismatch")
    require(counts.get("formal_exercises") == 0, "draft exercise count mismatch")

    ordered = obj.get("ordered_semantic_census")
    require(isinstance(ordered, list) and len(ordered) == 39,
            "draft ordered semantic census mismatch")
    require([item.get("order") for item in ordered] == list(range(1, 40)),
            "draft semantic census order mismatch")
    for item in ordered:
        kind = item.get("kind")
        source_kind = "proofof" if kind == "proofof" else kind
        require(source_kind in source["environment_ranges"], "draft census has unknown kind")
        require(item.get("lines") in source["environment_ranges"][source_kind],
                f"draft semantic locator mismatch at order {item.get('order')}")

    equations = obj.get("ordered_equation_diagram_census")
    require(isinstance(equations, list) and len(equations) == 31,
            "draft equation/diagram census mismatch")
    require([item.get("order") for item in equations] == list(range(1, 32)),
            "draft equation/diagram order mismatch")
    defects = obj.get("source_defects")
    require(isinstance(defects, list) and len(defects) == 33, "draft defect census mismatch")
    require([item.get("defect_id") for item in defects]
            == [f"FOM-U003-SRC-{n:03d}" for n in range(1, 34)],
            "draft defect-ID sequence mismatch")
    repair = obj.get("mandatory_proof_repair", {})
    require(repair.get("repair_id") == "FOM-PR-04", "draft mandatory repair ID mismatch")
    require(repair.get("source_omission_lines") == "1869-1872",
            "draft mandatory repair locator mismatch")
    return {
        "identity": result["identity"],
        "status": obj["status"],
        "ordered_semantic_census": ordered,
        "ordered_equation_diagram_census": equations,
        "source_defects": defects,
        "mandatory_proof_repair_at_draft": repair,
    }


def png_dimensions(raw: bytes) -> tuple[int, int]:
    require(raw[:8] == b"\x89PNG\r\n\x1a\n", "invalid PNG signature")
    require(raw[12:16] == b"IHDR", "PNG does not begin with IHDR")
    return struct.unpack(">II", raw[16:24])


def verify_assets() -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    for name, (expected_bytes, expected_sha, expected_dimensions) in sorted(ASSET_SPECS.items()):
        relative = f"source/id-ID/fomberg/assets/unit-003/{name}"
        path = LANE / relative
        require(path.is_file(), f"missing redraw asset {relative}")
        raw = path.read_bytes()
        require(len(raw) == expected_bytes, f"{relative}: byte mismatch")
        require(digest(raw) == expected_sha, f"{relative}: hash mismatch")
        record: dict[str, Any] = {
            "path": relative,
            "bytes": len(raw),
            "sha256": digest(raw),
            "media_type": "image/png" if name.endswith(".png") else "image/svg+xml",
        }
        if name.endswith(".png"):
            dimensions = png_dimensions(raw)
            require(dimensions == expected_dimensions, f"{relative}: dimension mismatch")
            record["width_px"], record["height_px"] = dimensions
        else:
            require(not raw.startswith(b"\xef\xbb\xbf") and b"\r" not in raw,
                    f"{relative}: SVG must be strict UTF-8 LF")
            try:
                root = ET.fromstring(raw.decode("utf-8", errors="strict"))
            except (UnicodeDecodeError, ET.ParseError) as exc:
                die(f"{relative}: invalid SVG/XML ({exc})")
            require(root.tag.endswith("svg"), f"{relative}: SVG root missing")
            require(root.attrib.get("role") == "img", f"{relative}: role=img missing")
            labelled = root.attrib.get("aria-labelledby", "").split()
            require(len(labelled) == 2, f"{relative}: aria-labelledby mismatch")
            ids = {element.attrib.get("id") for element in root.iter()}
            require(all(value in ids for value in labelled), f"{relative}: ARIA targets unresolved")
            titles = [element for element in root.iter() if element.tag.endswith("title")]
            descs = [element for element in root.iter() if element.tag.endswith("desc")]
            require(len(titles) == 1 and len(descs) == 1,
                    f"{relative}: exactly one title and desc required")
            require(bool("".join(titles[0].itertext()).strip())
                    and bool("".join(descs[0].itertext()).strip()),
                    f"{relative}: empty accessible title/description")
            record["viewBox"] = root.attrib.get("viewBox")
            record["accessibility"] = "role_img_title_desc_aria_bound"
        records.append(record)
    return {"records": records, "count": len(records), "all_exact": True}


def verify_reader(
    raw: bytes, text: str, source: dict[str, Any], assets: dict[str, Any]
) -> dict[str, Any]:
    reader_identity = require_identity(READER_PATH, raw, READER_IDENTITY)
    require(text.count(MODEL) == 1, "model provenance must occur exactly once")
    for fragment in (
        "lang: id-ID",
        'edition_unit_id: "O012-FOM-003"',
        'course_route_unit_id: "D60-R10"',
        COMMIT,
        SPAN_IDENTITY["sha256"],
        "baris 1923",
        "CC BY-SA 4.0",
        "tidak menyiratkan dukungan",
        "Tidak ada prosa dari",
    ):
        require(fragment in text, f"reader metadata/provenance fragment missing: {fragment}")
    require("TTP" not in text and "Translation and Transcription Project" not in text,
            "reader contains forbidden umbrella branding")

    lines, nodes, opens, closes = parse_reader(raw, text)
    by_id = {node["id"]: node for node in nodes}
    aliases = {
        node["attrs"]["data-source-label"]: node["id"]
        for node in nodes if "data-source-label" in node["attrs"]
    }
    require(aliases == SOURCE_DEFINED_ALIASES, "reader source-alias map mismatch")

    links = re.findall(r"\]\(#([A-Za-z0-9][A-Za-z0-9_.:-]*)\)", text)
    require(len(links) == 10, "reader internal-link count mismatch")
    require(Counter(links) == EXPECTED_READER_LINK_TARGET_COUNTS,
            "reader internal-link multiplicity mismatch")
    prior_raw, prior_text = strict_input(PRIOR_READER_PATH)
    prior_identity = require_identity(PRIOR_READER_PATH, prior_raw, PRIOR_READER_IDENTITY)
    for target in links:
        if target.startswith("o012-fom-u003"):
            require(target in by_id, f"reader unresolved local fragment: {target}")
        else:
            require(re.search(rf"(?:#|\s){re.escape(target)}(?:\s|\}})", prior_text) is not None,
                    f"reader unresolved prior-unit fragment: {target}")

    figures = [node for node in nodes if node["kind"] == "figure"]
    require([node["id"] for node in figures] == FIGURE_IDS,
            "reader semantic-figure order mismatch")
    for node in figures:
        require(node["attrs"].get("data-source-lines") is not None,
                f"{node['id']}: source-derived figure lacks locator")
        require("diagram semantik" in node_text(lines, node).casefold(),
                f"{node['id']}: semantic description missing")

    media_pattern = re.compile(
        r"!\[([^\]\r\n]+)\]\((\.\./assets/unit-003/([^)]+\.png))\)"
        r"\{\.semantic-redraw[ \t]+width=([0-9]+)%\}"
    )
    media_matches = media_pattern.findall(text)
    require(len(media_matches) == 6, "reader linked-redraw count mismatch")
    linked_names = [match[2] for match in media_matches]
    require(Counter(linked_names) == Counter(REDRAW_MAP.values()),
            "reader linked-redraw filenames mismatch")
    for figure_id, filename in REDRAW_MAP.items():
        body = node_text(lines, by_id[figure_id])
        require(f"../assets/unit-003/{filename}" in body,
                f"{figure_id}: expected redraw not linked")
        require(len(body.split("![", 1)[1].split("]", 1)[0].strip()) >= 40,
                f"{figure_id}: redraw alt text too short")
    require(assets["count"] == 12, "redraw asset-pair count mismatch")

    omission = by_id.get("o012-fom-u003-omission-pr04")
    proof = by_id.get("o012-fom-u003-proof-long-exact-repair")
    require(omission is not None and omission["kind"] == "source-omission",
            "FOM-PR-04 source-omission object missing")
    require(omission["attrs"].get("data-source-lines") == "1869-1872"
            and omission["attrs"].get("data-repair-id") == "FOM-PR-04",
            "FOM-PR-04 omission locator/binding mismatch")
    require(proof is not None and proof["kind"] == "proof",
            "FOM-PR-04 proof object missing")
    require(proof["attrs"].get("data-origin") == "edition-original"
            and proof["attrs"].get("data-repair-id") == "FOM-PR-04"
            and "data-source-lines" not in proof["attrs"],
            "FOM-PR-04 proof provenance/binding mismatch")
    proof_body = node_text(lines, proof)
    for fragment in (
        r"\delta_n([c]):=[a]",
        r"b'-b=i(x)",
        r"c'=c+\partial d",
        "konstruksi juga aditif",
        r"Eksak pada $H_n(\mathcal B)$",
        r"Eksak pada $H_n(\mathcal C)$",
        r"Eksak pada $H_{n-1}(\mathcal A)$",
        r"\operatorname{im}i_*\subseteq\ker j_*",
        r"\operatorname{im}j_*\subseteq\ker\delta_n",
        r"\operatorname{im}\delta_n\subseteq\ker i_*",
        "Ketiga pemeriksaan berlaku untuk setiap $n$",
    ):
        require(fragment in proof_body, f"FOM-PR-04 proof fragment missing: {fragment}")

    forward = by_id.get("o012-fom-u003-forward-quotient-les")
    require(forward is not None and forward["kind"] == "source-omission",
            "quotient-LES forward-proof marker missing")
    require(forward["attrs"].get("data-proof-status") == "forward-proof"
            and forward["attrs"].get("data-repair-id") == "FOM-U003-QUOTIENT-LES",
            "quotient-LES forward dependency is not explicit")

    main_relative = node_text(lines, by_id["o012-fom-u003-rem-relative-induced-map"])
    require(r"\partial P+P\partial=g_\#-f_\#" in main_relative,
            "relative prism identity does not use the required difference")
    require("homotopi melalui peta pasangan" in re.sub(r"\s+", " ", main_relative),
            "pair-preserving homotopy terminology missing")
    nonretract = node_text(lines, by_id["o012-fom-u003-proof-boundary-not-retract"])
    require(r"\widetilde H_{n-1}(\mathbb D^n)" in nonretract and r"n\geq1" in nonretract,
            "non-retraction proof lacks reduced-homology degree scope")
    sphere = node_text(lines, by_id["o012-fom-u003-proof-sphere-homology"])
    require(r"n\geq1" in sphere and r"\widetilde H_k(S^0)" in sphere,
            "sphere induction/base-case repair missing")
    pointed = node_text(lines, by_id["o012-fom-u003-exa-pointed-relative"])
    require(r"H_n(X,\{x_0\})" in pointed and r"n\geq1" in pointed,
            "pointed relative-homology notation/degree repair missing")
    pointed_zero = node_text(lines, by_id["o012-fom-u003-proof-pointed-degree-zero"])
    require(r"H_0(X,\{x_0\})" in pointed_zero
            and r"\widetilde H_0(X)" in pointed_zero
            and r"H_0(X)/\mathbb Z e_0" in pointed_zero,
            "pointed degree-zero supplement missing")

    exercise_ids = [f"o012-fom-u003-mcheck-{n:03d}" for n in range(1, 7)]
    hint_ids = [f"o012-fom-u003-hint-{n:03d}" for n in range(1, 7)]
    solution_ids = [f"o012-fom-u003-sol-{n:03d}" for n in range(1, 7)]
    for kind, expected_ids in (("exercise", exercise_ids), ("hint", hint_ids), ("solution", solution_ids)):
        actual = [node["id"] for node in nodes if node["kind"] == kind]
        require(actual == expected_ids, f"{kind} mastery-ID sequence mismatch")
        for ident in expected_ids:
            node = by_id[ident]
            require(node["attrs"].get("data-origin") == "edition-original",
                    f"{ident}: mastery origin mismatch")
            require(len(node_text(lines, node).strip()) >= 100, f"{ident}: empty/trivial block")
    for ident in exercise_ids:
        require(by_id[ident]["attrs"].get("data-course-route-unit-id") == ROUTE,
                f"{ident}: route binding mismatch")
    for ident in ("o012-fom-u003-mcheck-004", "o012-fom-u003-sol-004",
                  "o012-fom-u003-mcheck-005", "o012-fom-u003-sol-005"):
        require(by_id[ident]["attrs"].get("data-repair-id") == "FOM-PR-04",
                f"{ident}: mastery repair binding mismatch")

    require(sum(line.strip() == "$$" for line in lines) == 202,
            "reader display-math marker census mismatch")
    non_audit_lines = list(lines)
    for audit_node in (node for node in nodes if node["kind"] == "source-audit"):
        for index in range(audit_node["line_start"] - 1, audit_node["line_end"]):
            non_audit_lines[index] = ""
    non_audit_text = "\n".join(non_audit_lines)
    rejected_patterns = [
        r"(?i)\btakkosong\b", r"(?i)\bpris, operator\b", r"(?i)\bhomotop\b",
        r"(?i)\bcontracible\b", r"(?i)\bequialent\b", r"(?i)\barguemnts\b",
        r"(?i)\bhas to fixed points\b", r"(?<!\\)\bq{2,}uad\b",
        r"(?<!\\)\bcong\b",
    ]
    found_rejected = [
        pattern for pattern in rejected_patterns if re.search(pattern, non_audit_text)
    ]
    require(not found_rejected, f"reader contains rejected form(s): {found_rejected}")
    normalized_reader_text = re.sub(r"\s+", " ", text.casefold())
    for row in EXPECTED_TERM_ROWS:
        if row["term_id"] != "O012-TERM-0414":
            require(row["id_ID"].casefold() in normalized_reader_text,
                    f"admitted term absent from reader: {row['id_ID']}")

    privacy_patterns = {
        "absolute_windows_home": r"(?i)[A-Z]:\\Users\\",
        "email_address": r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b",
        "credential_prefix": r"(?i)\b(?:ghp_|github_pat_|bearer\s+|api[_-]?key\s*[:=])",
        "token_assignment": r"(?i)\btoken\s*[:=]\s*[A-Za-z0-9_-]{12,}",
    }
    privacy_hits = {name: bool(re.search(pattern, text))
                    for name, pattern in privacy_patterns.items()}
    require(not any(privacy_hits.values()), f"reader privacy/credential leak: {privacy_hits}")

    boundary = by_id.get("o012-fom-u003-boundary-001")
    require(boundary is not None and boundary["kind"] == "boundary",
            "source-cursor boundary object missing")
    require("baris 1923" in node_text(lines, boundary)
            and "eksisi" in node_text(lines, boundary).casefold(),
            "source-cursor boundary content mismatch")
    return {
        "identity": reader_identity,
        "prior_reader_identity": prior_identity,
        "lines": lines,
        "nodes": nodes,
        "by_id": by_id,
        "opens": opens,
        "closes": closes,
        "aliases": aliases,
        "links": links,
        "linked_redraws": [
            {"alt": alt, "relative_path": relative, "filename": filename, "width_percent": int(width)}
            for alt, relative, filename, width in media_matches
        ],
        "proof_closure": {
            "FOM-PR-04": {
                "omission_id": omission["id"],
                "source_lines": "1869-1872",
                "proof_id": proof["id"],
                "proof_status": "complete_original_repair",
                "choice_checks": ["lift", "cycle_representative", "additivity"],
                "exactness_positions": ["H_n(A)", "H_n(B)", "H_n(C)"],
            },
            "FOM-U003-QUOTIENT-LES": {
                "marker_id": forward["id"],
                "status": "declared_forward_proof_dependency",
            },
        },
        "exercise_ids": exercise_ids,
        "hint_ids": hint_ids,
        "solution_ids": solution_ids,
        "display_markers": 202,
        "privacy_scan": privacy_hits,
    }


def read_control_rows() -> dict[str, Any]:
    term_raw, term_text = strict_input(TERMINOLOGY_PATH)
    adverse_raw, adverse_text = strict_input(ADVERSE_PATH)
    term_identity = require_identity(TERMINOLOGY_PATH, term_raw, CONTROL_IDENTITIES[TERMINOLOGY_PATH])
    adverse_identity = require_identity(ADVERSE_PATH, adverse_raw, CONTROL_IDENTITIES[ADVERSE_PATH])

    term_reader = csv.DictReader(term_text.splitlines())
    require(term_reader.fieldnames == ["term_id", "source_term", "id_ID", "scope", "status", "note"],
            "terminology CSV schema mismatch")
    all_terms = list(term_reader)
    require(len(all_terms) == 415, "terminology sealed row count mismatch")
    require(len({row["term_id"] for row in all_terms}) == len(all_terms),
            "terminology CSV has duplicate IDs")
    terms = [row for row in all_terms if 401 <= int(row["term_id"].rsplit("-", 1)[1]) <= 415]
    require(terms == EXPECTED_TERM_ROWS, "terminology rows 0401-0415 mismatch")
    require(digest(canonical(terms)) == TERM_ROWS_SHA256,
            "terminology rows 0401-0415 canonical hash mismatch")

    adverse_reader = csv.DictReader(adverse_text.splitlines())
    require(adverse_reader.fieldnames == [
        "event_id", "severity", "source_location", "observed", "action", "status", "rationale"
    ], "adverse-ledger CSV schema mismatch")
    all_adverse = list(adverse_reader)
    require(len(all_adverse) == 498, "adverse-ledger sealed row count mismatch")
    require(len({row["event_id"] for row in all_adverse}) == len(all_adverse),
            "adverse ledger has duplicate IDs")
    adverse = [row for row in all_adverse if 457 <= int(row["event_id"].rsplit("-", 1)[1]) <= 498]
    require([row["event_id"] for row in adverse]
            == [f"O012-ADV-{number:04d}" for number in range(457, 499)],
            "adverse rows 0457-0498 are missing, duplicated, or reordered")
    require(digest(canonical(adverse)) == ADVERSE_ROWS_SHA256,
            "adverse rows 0457-0498 canonical hash mismatch")
    require(all(row["severity"] in {"P1", "P2", "P3"} for row in adverse),
            "adverse rows include invalid severity")
    allowed_status = {
        "corrected_in_translation", "clarified_in_translation",
        "proof_completed_in_translation", "resolved_before_admission",
        "hypothesis_repaired_in_translation", "pending_future_unit",
    }
    require(all(row["status"] in allowed_status for row in adverse),
            "adverse rows include unknown status")
    pending = [row for row in adverse if row["status"] == "pending_future_unit"]
    require([row["event_id"] for row in pending] == ["O012-ADV-0460"],
            "adverse ledger has an undeclared/unexpected pending item")
    require(all(all(row[field].strip() for field in adverse_reader.fieldnames) for row in adverse),
            "adverse rows contain an empty field")
    return {
        "terminology": {
            "identity": term_identity,
            "first": terms[0]["term_id"], "through": terms[-1]["term_id"],
            "records": len(terms), "selected_rows_sha256": TERM_ROWS_SHA256,
            "rows": terms, "all_admitted": True,
        },
        "adverse": {
            "identity": adverse_identity,
            "first": adverse[0]["event_id"], "through": adverse[-1]["event_id"],
            "records": len(adverse), "selected_rows_sha256": ADVERSE_ROWS_SHA256,
            "severity_counts": dict(sorted(Counter(row["severity"] for row in adverse).items())),
            "status_counts": dict(sorted(Counter(row["status"] for row in adverse).items())),
            "pending_forward_dependency_ids": [row["event_id"] for row in pending],
            "rows": adverse,
        },
    }


def nested_contains(obj: Any, needle: str) -> bool:
    return needle in json.dumps(obj, ensure_ascii=False, sort_keys=True)


def verify_reviews() -> dict[str, Any]:
    results: dict[str, Any] = {}
    for slot, spec in REVIEW_SPECS.items():
        raw, result = strict_json(spec["path"], spec)
        obj = result["object"]
        require(obj.get("status") == spec["status"], f"{slot}: status mismatch")
        if spec["phase"] == "final":
            require(nested_contains(obj, READER_IDENTITY["sha256"]),
                    f"{slot}: final review does not bind reader hash")
            if slot == "relative_final":
                counts = obj.get("final_finding_counts")
                require(counts == {"P1": 0, "P2": 0, "P3": 0, "total": 0},
                        "relative final review is not zero-finding")
            else:
                counts = obj.get("final_findings", {}).get("counts")
                require(counts == {"p1": 0, "p2": 0, "p3": 0, "total": 0},
                        f"{slot}: final review is not zero-finding")
        results[slot] = {
            "identity": result["identity"],
            "phase": spec["phase"],
            "status": spec["status"],
        }

    pairs = (("exact_initial", "exact_final"),
             ("relative_initial", "relative_final"),
             ("integrated_initial", "integrated_final"))
    for initial, final in pairs:
        _, final_result = strict_json(REVIEW_SPECS[final]["path"], REVIEW_SPECS[final])
        require(nested_contains(final_result["object"], REVIEW_SPECS[initial]["sha256"]),
                f"{final}: does not bind initial-review hash")

    _, reconciliation = strict_json(RECONCILIATION_PATH, RECONCILIATION_IDENTITY)
    recon = reconciliation["object"]
    require(recon.get("status") == "PASS_RECOMPUTED_COUNT_SUPERSEDES_REVIEW_COUNT_FIELD_ONLY",
            "review-count reconciliation status mismatch")
    recomputed = recon.get("independent_recomputation", {})
    require(recomputed.get("heading_ids") == 6
            and recomputed.get("fenced_div_ids") == 119
            and recomputed.get("stable_ids_total") == 125
            and recomputed.get("stable_ids_unique") == 125
            and recomputed.get("duplicates") == 0,
            "review-count reconciliation values mismatch")
    require(recon.get("review", {}).get("sha256") == REVIEW_SPECS["integrated_final"]["sha256"],
            "review-count reconciliation is not bound to integrated final review")
    results["count_reconciliation"] = {
        "identity": reconciliation["identity"],
        "status": recon["status"],
        "review_reported_count": 124,
        "authoritative_recomputed_count": 125,
        "scope": "integrated_review_stable_id_count_field_only",
    }
    return results


def verify_pandoc() -> dict[str, Any]:
    executable = shutil.which("pandoc")
    require(executable is not None, "Pandoc is unavailable")
    try:
        version = subprocess.run(
            [executable, "--version"], check=False, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="replace", timeout=30,
        )
        parsed = subprocess.run(
            [executable, "--from=markdown+fenced_divs+tex_math_dollars",
             "--to=native", "--wrap=none", str(LANE / READER_PATH)],
            check=False, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
            text=True, encoding="utf-8", errors="replace", timeout=60, cwd=LANE,
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


def source_locator(source_lines: list[bytes], source_range: str) -> dict[str, Any]:
    start, end = map(int, source_range.split("-"))
    payload = b"".join(source_lines[start - 1:end])
    return {
        "path": "algebraic_topology.tex", "authority_path": UPSTREAM_PATH,
        "commit_sha": COMMIT, "tree_sha": TREE,
        "file_sha256": UPSTREAM_IDENTITY["sha256"],
        "line_start": start, "line_end": end,
        "bytes": len(payload), "content_sha256": digest(payload),
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
            "path": READER_PATH, "file_sha256": READER_IDENTITY["sha256"],
            "line_start": start, "line_end": end, "bytes": len(payload),
            "content_sha256": digest(payload), "precision": "exact_target_span",
        }

    original_classes = {
        "source-audit", "proof-supplement", "exercise", "hint", "solution", "boundary"
    }
    records: list[dict[str, Any]] = []
    for node in reader["nodes"]:
        attrs = dict(sorted(node["attrs"].items()))
        source_range = attrs.get("data-source-lines")
        explicit_original = attrs.get("data-origin") == "edition-original"
        is_original = explicit_original or node["kind"] in original_classes
        if node["id"] == "o012-fom-u003":
            origin = "composite_translated_and_original"
        elif is_original:
            origin = (
                "edition_original_proof_repair" if attrs.get("data-repair-id") == "FOM-PR-04"
                else "edition_original"
            )
        elif source_range:
            origin = "translated_adapted_from_upstream"
        else:
            origin = "edition_original"

        if source_range:
            source = source_locator(source_lines, source_range)
        elif node["id"] == "o012-fom-u003":
            source = {
                "path": "algebraic_topology.tex", "authority_path": UPSTREAM_PATH,
                "commit_sha": COMMIT, "tree_sha": TREE,
                "file_sha256": UPSTREAM_IDENTITY["sha256"],
                "line_start": 1291, "line_end": 1922,
                "bytes": SPAN_IDENTITY["bytes"],
                "content_sha256": SPAN_IDENTITY["sha256"],
                "precision": "exact_unit_span",
            }
        else:
            source = {"kind": "edition_original", "path": READER_PATH,
                      "precision": "exact_target_span"}

        segment_target = target(node["line_start"], node["line_end"])
        unit_target = target(1, len(reader_lines)) if node["id"] == "o012-fom-u003" else segment_target
        segment_origin = "translated_adapted_from_upstream" if node["id"] == "o012-fom-u003" else origin
        segment_rights = (
            "rights:fomberg-cc-by-sa-4.0"
            if segment_origin == "translated_adapted_from_upstream"
            else "rights:o012-fom-u003-companion-cc-by-sa-4.0"
        )
        unit_rights = (
            "rights:o012-fom-u003-composite-cc-by-sa-4.0"
            if node["id"] == "o012-fom-u003" else segment_rights
        )
        records.append({
            "stable_id": node["id"],
            "record_ids": {"segment": f"segment:{node['id']}", "unit": f"unit:{node['id']}"},
            "semantic_class": node["kind"], "declared_classes": node["classes"],
            "attributes": attrs, "provenance_relation": segment_origin,
            "record_provenance_relations": {"segment": segment_origin, "unit": origin},
            "record_rights_component_ids": {"segment": segment_rights, "unit": unit_rights},
            "source_locator": source, "target_locator": segment_target,
            "record_target_locators": {"segment": segment_target, "unit": unit_target},
        })
    require(len(records) == 125, "node evidence record count mismatch")
    return records


def build_record_plan(reader: dict[str, Any], reviews: dict[str, Any]) -> dict[str, Any]:
    del reviews  # Review identities are independently bound above.
    planner = LANE / "scripts/extend-backend-fomberg-unit-003.py"
    require(planner.is_file(), "Unit 003 backend planner is missing")
    try:
        completed = subprocess.run(
            [sys.executable, "-B", str(planner), "--plan"],
            check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, encoding="utf-8", errors="strict", timeout=60, cwd=LANE,
        )
    except (OSError, subprocess.TimeoutExpired, UnicodeError) as exc:
        die(f"backend planner invocation failed ({exc})")
    require(completed.returncode == 0,
            f"backend planner failed: {completed.stderr[-1000:].strip()}")
    try:
        plan = json.loads(completed.stdout, object_pairs_hook=no_duplicate_object)
    except json.JSONDecodeError as exc:
        die(f"backend planner emitted malformed JSON ({exc})")
    require(isinstance(plan, dict), "backend planner did not emit an object")
    require(plan.get("edition_unit_id") == ROOT and plan.get("root_unit_id") == ROOT,
            "backend planner Unit 003 identity mismatch")
    require(plan.get("course_id") == COURSE and plan.get("course_route_unit_id") == ROUTE,
            "backend planner course binding mismatch")
    require(plan.get("resource_id") == RESOURCE and plan.get("edition_id") == EDITION,
            "backend planner authority binding mismatch")
    require(plan.get("records_planned") == 405
            and plan.get("cumulative_records_planned") == 5747,
            "backend planner record total mismatch")
    require(plan.get("stable_ids") == len(reader["nodes"]) == 125,
            "backend planner stable-ID count mismatch")
    require(plan.get("asset_records") == 14 and plan.get("real_redraw_files") == 12,
            "backend planner asset count mismatch")
    require(plan.get("immutable_prefix") == {
        "records": 5342,
        "bytes": 6040123,
        "bundle_sha256": "83d98f1b271c5e62334a072354f1be1c4a1535ed26c8a403223e89773bb1eba1",
    }, "backend planner immutable-prefix binding mismatch")
    require(digest(canonical(plan.get("records_by_file")))
            == "55afcd9c6e68d7825849c3599fe8470ff5bcaeb179c3ef41f618b9e1142d9a4d",
            "backend planner per-file counts hash mismatch")
    require(digest(canonical(plan.get("record_ids_by_file")))
            == "78f82d76aaae261d8e689370cf3b2de8625ab1cd993c453b4dea60a4b18d4558",
            "backend planner record-ID inventory hash mismatch")
    require(digest(canonical(plan.get("artifact_evidence_paths_in_record_order")))
            == "f0d1e12019850a1b75c8ed6ce149714f57151adf2fbd8b9c1375657f7b290d2c",
            "backend planner artifact-path inventory hash mismatch")
    unsealed = plan.pop("unsealed_identity_paths", None)
    require(isinstance(unsealed, list)
            and set(unsealed).issubset({
                "qa/FOMBERG_UNIT_003_SOURCE_AUDIT.json",
                "qa/FOMBERG_UNIT_003_QA.json",
            }), "backend planner unsealed-output declaration mismatch")
    return {
        **plan,
        "binding_status": "verified_external_plan_not_written",
        "backend_write_performed": False,
        "records_by_file_sha256": digest(canonical(plan["records_by_file"])),
        "record_ids_by_file_sha256": digest(canonical(plan["record_ids_by_file"])),
        "artifact_evidence_paths_sha256": digest(
            canonical(plan["artifact_evidence_paths_in_record_order"])
        ),
    }


def build_source_audit(
    source: dict[str, Any], draft: dict[str, Any], reader: dict[str, Any],
    controls: dict[str, Any], reviews: dict[str, Any], assets: dict[str, Any],
    pandoc: dict[str, Any], records: dict[str, Any], evidence: list[dict[str, Any]],
) -> dict[str, Any]:
    class_counts = dict(sorted(Counter(node["kind"] for node in reader["nodes"]).items()))
    return {
        "schema_version": SCHEMA_VERSION,
        "audit_id": "O012-FOMBERG-UNIT-003-SOURCE-AUDIT",
        "audit_date": AUDIT_DATE, "status": "PASS",
        "translation_performed": True, "backend_modified": False,
        "authority": {
            "repository": "https://git.sr.ht/~yp/math-notes", "resource_id": RESOURCE,
            "edition_id": EDITION, "commit": COMMIT, "tree": TREE,
            "source": source["identity"], "license": "CC BY-SA 4.0",
            "notes_author": "Yeheli Fomberg", "based_on_lectures_by": "Nir Lazarovich",
            "nonendorsement_notice_required": True,
        },
        "unit": {
            "component_unit_id": "FOMBERG_UNIT_003", "edition_unit_id": "O012-FOM-003",
            "course_route_unit_id": ROUTE, "source_lines": "1291-1922 inclusive",
            "line_count": SPAN_IDENTITY["lines"], "bytes_preserving_lf": SPAN_IDENTITY["bytes"],
            "sha256_preserving_lf": SPAN_IDENTITY["sha256"],
            "start_byte_offset": source["span"]["start_byte_offset"],
            "end_byte_offset_inclusive": source["span"]["end_byte_offset_inclusive"],
            "subspans": {"exact_sequences": source["exact_span"],
                         "relative_homology": source["relative_span"]},
            "headings": [
                {"line": 1291, "level": "subsection", "title": "Exact sequences"},
                {"line": 1565, "level": "subsection", "title": "Relative homology"},
            ],
            "next_line": NEXT_SOURCE_LINE, "next_heading": "Excisions",
            "next_line_exact_text": NEXT_HEADING, "terminal_source_eof": False,
        },
        "source_counts": {
            **source["environment_counts"],
            "semantic_environments_total": sum(source["environment_counts"].values()),
            "labels": len(source["labels"]), "cross_references": len(source["cref_payloads"]),
            **source["diagram_counts"], "diagrams_total": sum(source["diagram_counts"].values()),
            "formal_exercises": 0,
        },
        "source_object_ranges": source["environment_ranges"],
        "ordered_semantic_census": draft["ordered_semantic_census"],
        "ordered_equation_diagram_census": draft["ordered_equation_diagram_census"],
        "source_aliases": ALL_SOURCE_ALIASES,
        "source_reference_target_counts": source["mapped_ref_counts"],
        "source_defects": draft["source_defects"],
        "source_audit_draft": draft["identity"],
        "reader": reader["identity"],
        "reader_structure": {
            "stable_id_count": len(reader["nodes"]),
            "stable_ids_unique": len({node["id"] for node in reader["nodes"]}),
            "ordered_stable_ids_sha256": EXPECTED_ID_SEQUENCE_SHA256,
            "stable_ids_in_reader_order": [node["id"] for node in reader["nodes"]],
            "class_counts": class_counts, "identified_headings": EXPECTED_HEADING_IDS,
            "fenced_semantic_objects": reader["opens"], "fenced_div_opens": reader["opens"],
            "fenced_div_closes": reader["closes"], "source_labels": len(reader["aliases"]),
            "internal_links": len(reader["links"]), "display_math_markers": reader["display_markers"],
            "source_derived_figure_blocks": len(FIGURE_IDS), "figure_ids": FIGURE_IDS,
            "linked_accessible_redraws": len(reader["linked_redraws"]),
        },
        "proof_closure": reader["proof_closure"],
        "mandatory_proof_repair": {
            "repair_id": "FOM-PR-04",
            "status": "complete_original_repair",
            "source_omission_lines": "1869-1872",
            "omission_id": "o012-fom-u003-omission-pr04",
            "proof_id": "o012-fom-u003-proof-long-exact-repair",
            "choice_checks": ["lift", "cycle_representative", "additivity"],
            "exactness_positions": ["H_n(A)", "H_n(B)", "H_n(C)"],
        },
        "mastery": {
            "triples": 6, "exercise_ids": reader["exercise_ids"],
            "hint_ids": reader["hint_ids"], "solution_ids": reader["solution_ids"],
            "solution_status": "complete_checked_solution",
        },
        "controls": controls, "independent_reviews": reviews,
        "review_count_discrepancy": reviews["count_reconciliation"],
        "assets": assets, "pandoc": pandoc, "evidence_records": evidence,
        "record_plan": records, "model_provenance": MODEL,
        "checks": {
            "reader_identity_lf_utf8": True, "authority_full_source_identity": True,
            "source_span_1291_1922_identity": True, "cursor_line_1923_exact": True,
            "source_semantic_object_census_39": True, "source_diagram_functions_29": True,
            "source_figure_blocks_26": True, "linked_redraws_6_and_asset_files_12": True,
            "stable_ids_125_unique_and_hash_bound": True,
            "integrated_review_124_count_scoped_and_reconciled": True,
            "source_aliases_and_links_resolve": True, "fom_pr_04_complete": True,
            "one_declared_forward_proof_dependency": True,
            "six_mastery_triples_complete": True, "terminology_rows_0401_0415_exact": True,
            "adverse_rows_0457_0498_exact": True,
            "three_initial_and_three_final_reviews_bound": True,
            "three_final_reviews_zero_findings": True, "pandoc_parse_pass": True,
            "rights_provenance_nonendorsement_present": True,
            "privacy_and_credential_scan_zero": True, "backend_unchanged": True,
            "no_build_or_publication_claim": True,
        },
    }


def build_qa(
    source: dict[str, Any], reader: dict[str, Any], controls: dict[str, Any],
    reviews: dict[str, Any], assets: dict[str, Any], pandoc: dict[str, Any],
    records: dict[str, Any], audit_raw: bytes,
) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "qa_id": "O012-FOMBERG-UNIT-003-STATIC-QA", "audit_date": AUDIT_DATE,
        "status": "PASS", "reader": reader["identity"],
        "authority": {
            "resource_id": RESOURCE, "edition_id": EDITION, "commit": COMMIT, "tree": TREE,
            "source": source["identity"], "unit_span": SPAN_IDENTITY,
            "next_source_line": NEXT_SOURCE_LINE, "next_heading": NEXT_HEADING,
            "terminal_source_eof": False,
        },
        "source_audit_output": {
            "path": "qa/FOMBERG_UNIT_003_SOURCE_AUDIT.json",
            "bytes": len(audit_raw), "sha256": digest(audit_raw),
            "encoding": "UTF-8", "newline": "LF",
        },
        "evidence": {
            "authority_source": source["identity"], "reader": reader["identity"],
            "prior_reader_for_cross_unit_link": reader["prior_reader_identity"],
            "terminology_control": controls["terminology"]["identity"],
            "adverse_control": controls["adverse"]["identity"],
            "independent_reviews": {slot: value["identity"] for slot, value in reviews.items()},
            "redraw_assets": assets["records"],
        },
        "structure": {
            "stable_id_count": len(reader["nodes"]), "stable_id_unique_count": 125,
            "ordered_stable_ids_sha256": EXPECTED_ID_SEQUENCE_SHA256,
            "class_counts": dict(sorted(Counter(node["kind"] for node in reader["nodes"]).items())),
            "fenced_semantic_objects": reader["opens"], "source_aliases": SOURCE_DEFINED_ALIASES,
            "internal_link_target_counts": dict(sorted(EXPECTED_READER_LINK_TARGET_COUNTS.items())),
            "source_diagram_functions": 29, "source_derived_figure_blocks": 26,
            "linked_accessible_redraws": 6, "redraw_asset_files": 12,
        },
        "proof_closure": {"FOM-PR-04": "complete_original_repair"},
        "proof_closure_detail": reader["proof_closure"],
        "mastery": {"triples": 6, "exercise_ids": reader["exercise_ids"],
                    "hint_ids": reader["hint_ids"], "solution_ids": reader["solution_ids"]},
        "controls": {
            "terminology": {"first": "O012-TERM-0401", "through": "O012-TERM-0415",
                            "records": 15, "selected_rows_sha256": TERM_ROWS_SHA256,
                            "all_admitted": True},
            "adverse": {"first": "O012-ADV-0457", "through": "O012-ADV-0498",
                        "records": 42, "selected_rows_sha256": ADVERSE_ROWS_SHA256,
                        "declared_forward_dependency": "O012-ADV-0460"},
        },
        "independent_reviews": reviews, "review_count_discrepancy": reviews["count_reconciliation"],
        "pandoc": pandoc, "record_plan": records, "model_provenance": MODEL,
        "checks": {
            "reader_identity_65540_bytes_1773_lf_lines": True,
            "reader_sha256_2571f62b": True, "strict_utf8_lf_and_model_provenance": True,
            "source_full_and_three_span_identities": True, "cursor_line_1923": True,
            "unique_125_stable_ids": True, "exact_semantic_class_census": True,
            "balanced_119_fenced_divs": True, "four_source_labels_and_ten_reader_links": True,
            "twenty_nine_source_diagrams_twenty_six_figures": True,
            "six_png_svg_redraw_pairs_exact_and_accessible": True,
            "fom_pr_04_choice_additivity_and_exactness_closed": True,
            "six_exercise_hint_solution_triples": True, "rejected_forms_absent": True,
            "privacy_and_credentials_absent": True, "terminology_0401_0415_exact": True,
            "adverse_0457_0498_exact": True, "three_final_reviews_zero_and_pass": True,
            "review_count_124_superseded_by_independent_125": True,
            "pandoc_parse_available_and_pass": True, "inputs_not_modified": True,
            "backend_write_deferred": True,
        },
    }


def main() -> int:
    upstream_raw, upstream_text = strict_input(UPSTREAM_PATH)
    reader_raw, reader_text = strict_input(READER_PATH)
    source = verify_source(upstream_raw, upstream_text)
    draft = verify_draft_audit(source)
    assets = verify_assets()
    reader = verify_reader(reader_raw, reader_text, source, assets)
    controls = read_control_rows()
    reviews = verify_reviews()
    pandoc = verify_pandoc()
    evidence = node_evidence(reader, upstream_raw, reader_raw)
    records = build_record_plan(reader, reviews)
    audit = build_source_audit(
        source, draft, reader, controls, reviews, assets, pandoc, records, evidence
    )
    audit_raw = receipt_bytes(audit)
    qa = build_qa(source, reader, controls, reviews, assets, pandoc, records, audit_raw)
    qa_raw = receipt_bytes(qa)

    # Catch any mutation between validation and receipt publication.
    require(identity(UPSTREAM_PATH) == source["identity"], "authority changed during QA")
    require(identity(READER_PATH) == reader["identity"], "reader changed during QA")
    require(identity(PRIOR_READER_PATH) == reader["prior_reader_identity"],
            "prior reader changed during QA")
    require(identity(TERMINOLOGY_PATH) == controls["terminology"]["identity"],
            "terminology control changed during QA")
    require(identity(ADVERSE_PATH) == controls["adverse"]["identity"],
            "adverse control changed during QA")
    require(identity(DRAFT_AUDIT_PATH) == draft["identity"], "draft audit changed during QA")
    for slot, review in reviews.items():
        require(identity(review["identity"]["path"]) == review["identity"],
                f"{slot}: review/reconciliation changed during QA")
    for record in assets["records"]:
        payload = (LANE / record["path"]).read_bytes()
        require(len(payload) == record["bytes"] and digest(payload) == record["sha256"],
                f"{record['path']}: asset changed during QA")

    AUDIT_OUTPUT.write_bytes(audit_raw)
    QA_OUTPUT.write_bytes(qa_raw)
    print("Fomberg Unit 003 source audit and static QA: PASS")
    print(f"stable_ids={len(reader['nodes'])}")
    print(f"source_audit_bytes={len(audit_raw)}")
    print(f"source_audit_sha256={digest(audit_raw)}")
    print(f"qa_bytes={len(qa_raw)}")
    print(f"qa_sha256={digest(qa_raw)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
