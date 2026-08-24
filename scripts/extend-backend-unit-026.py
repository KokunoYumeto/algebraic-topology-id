#!/usr/bin/env python3
"""Fail-closed append-only semantic-backend admission for Roberts Unit 026.

The complete 3,913-record Units 001--025 cumulative backend is immutable.
This transaction verifies that exact byte prefix plus the frozen Unit 26
authority, reader, audit, review, and QA witnesses, then appends only the
Unit 26 semantic slice.  It does not build or mutate reader artifacts.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

LANE = Path(__file__).resolve().parents[1]
BACKEND = LANE / "backend"
SOURCE = LANE / "source/id-ID/units/unit-026-lecture-026.md"
UPSTREAM = (LANE / "authority/upstream" /
            "AlgebraicTopology2019-b947ad2e9f9e301bfe24590a9db653bc54fa1a53" /
            "Notes.tex")
AUDIT = LANE / "qa/UNIT_026_SOURCE_AUDIT.md"
REVIEW = LANE / "qa/UNIT_026_INDEPENDENT_REVIEW.md"
QA_JSON = LANE / "qa/UNIT_026_QA.json"

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
COMPANION_RIGHTS = "rights:o012-u026-companion-cc-by-4.0"
COMPOSITE_RIGHTS = "rights:o012-u026-composite-cc-by-4.0"
CUMULATIVE_RIGHTS = "rights:o012-units-001-026-composite-cc-by-4.0"
PRIOR_RIGHTS = "rights:o012-units-001-025-composite-cc-by-4.0-final-df72"
ROOT = "unit:o012-rbt-u026"
LECTURE = "unit:o012-rbt-l26"
MASTERY = "unit:o012-rbt-l26-mastery"
SOURCE_PATH = "source/id-ID/units/unit-026-lecture-026.md"
SOURCE_BYTES = 38537
SOURCE_LINES = 1201
SOURCE_SHA = "7a2cf4ea31546b8258e3e91c819d3ad516973c8f861249fccc7334b9ade9d835"
UPSTREAM_BYTES = 331447
UPSTREAM_LINES = 6368
UPSTREAM_SHA = "cfe93e9dbe3e25bd96f711f59e6078ab97527682b58e1f8ad127f74357f665d7"
UPSTREAM_START = 5612
UPSTREAM_END = 5823
UPSTREAM_SPAN_BYTES = 9763
UPSTREAM_SPAN_SHA = "52663b3e60d5d6f3041b8ede449c52a04700ee670c201ef5674c4aa3973203a9"
NEXT_SOURCE_LINE = 5824

FILES = ("artifacts.jsonl", "assets.jsonl", "authority.jsonl", "concepts.jsonl",
         "corrections.jsonl", "qa.jsonl", "relations.jsonl", "rights.jsonl",
         "segments.jsonl", "terms.jsonl", "units.jsonl")
PREFIX = {
    "artifacts.jsonl": (145, 115514, "ac0633eb616f2d0bd412bfb076a482d6ef6a402683d35da67bf6c1ed290ea40e"),
    "assets.jsonl": (27, 16679, "aa569a900426a9e2cfd56777f3e52f07b35a1a72f211847bafd71ec638043462"),
    "authority.jsonl": (4, 2721, "f21af26912520ab34b38dff0e927ed46a546dbe5d318da0dc133e58330d0e368"),
    "concepts.jsonl": (325, 102250, "0ce28594cd511c1a20aff74053b7c74c6c4c6a0505c7c8c5804dd7acd2dae77d"),
    "corrections.jsonl": (332, 327054, "40791f1db8da9ba81083bad0bb4ac183094c3151b9007bb34e5fc637a1790893"),
    "qa.jsonl": (119, 67471, "7b90c07af1561b6356a3249f396a97aaf10265989f4d7ba2b1493f87bac60b93"),
    "relations.jsonl": (397, 162048, "62f67c2ede76bcd24e9ad87db7968dd92649aba6e284c4829042941dd7ea8a50"),
    "rights.jsonl": (71, 65630, "7e54a0f51dd951aecadbc3767173308dc02c12ada6c121b9703c9ec2fb7f2ac7"),
    "segments.jsonl": (1075, 1428116, "d47404ea94dfa7347fbf6f6e0e0e8c5f4fb60e2634c066b87967a4468fff644a"),
    "terms.jsonl": (318, 197648, "dda9013d863bc39ec81f9936167ad24d0cfa2ebba6de0aa2c768743dc09b8503"),
    "units.jsonl": (1100, 1522772, "7fe9d4abfae9389db7cb99240b553d62b66144086c3f2097e9f64d5b2fe14318"),
}
PREFIX_RECORDS = 3913
PREFIX_BYTES = 4007903
PREFIX_BUNDLE = "8b50629f25c5fcbedb6d5547f8f7151c622aa90e04f71583008bd176058a4f78"

EVIDENCE = {
    "artifact:o012-u026-source-audit": (
        "qa/UNIT_026_SOURCE_AUDIT.md", 7693,
        "658a2586c58fd4149cf4959bc9b405d67896984f61621b1533f873836a9c8bb5",
        "text/markdown; charset=utf-8", "source_frozen",
        ["qa:o012-u026-source-integrity"]),
    "artifact:o012-u026-independent-review": (
        "qa/UNIT_026_INDEPENDENT_REVIEW.md", 7718,
        "b00eb4de7d29e9833539d0086ebc12e5d7339137ebc2b74874d9cfc72c4e3111",
        "text/markdown; charset=utf-8", "mathematically_reviewed",
        ["qa:o012-u026-math", "qa:o012-u026-language"]),
    "artifact:o012-u026-qa": (
        "qa/UNIT_026_QA.json", 7310,
        "3a25fc42dfa4353e8ba50a5f619684196a73fcb350e39a9d539568c0542bf835",
        "application/json", "built",
        ["qa:o012-u026-source-integrity", "qa:o012-u026-language"]),
}

EXPECTED_ANCHORS = (
    "o012-rbt-l26-notice", "o012-rbt-l26", "o012-rbt-l26-s01",
    "o012-rbt-l26-aside-001", "o012-rbt-l26-audit-001",
    "o012-rbt-l26-s02", "o012-rbt-l26-def-001",
    "o012-rbt-l26-prop-001", "o012-rbt-l26-proof-001",
    "o012-rbt-l26-audit-002", "o012-rbt-l26-exa-001",
    "o012-rbt-l26-aside-002", "o012-rbt-l26-s03",
    "o012-rbt-l26-def-002", "o012-rbt-l26-prop-002",
    "o012-rbt-l26-proof-002", "o012-rbt-l26-rem-001",
    "o012-rbt-l26-audit-003", "o012-rbt-l26-exa-002",
    "o012-rbt-l26-prop-003", "o012-rbt-l26-proof-003",
    "o012-rbt-l26-aside-003", "o012-rbt-l26-s04",
    "o012-rbt-l26-prop-004", "o012-rbt-l26-proof-004",
    "o012-rbt-l26-audit-004", "o012-rbt-l26-s05",
    "o012-rbt-l26-thm-001", "o012-rbt-l26-cor-001",
    "o012-rbt-l26-proof-005", "o012-rbt-l26-cor-002",
    "o012-rbt-l26-proof-006", "o012-rbt-l26-audit-005",
    "o012-rbt-l26-cor-003", "o012-rbt-l26-proof-007",
    "o012-rbt-l26-def-003", "o012-rbt-l26-lem-001",
    "o012-rbt-l26-proof-008", "o012-rbt-l26-audit-006",
    "o012-rbt-l26-thm-002", "o012-rbt-l26-proof-009",
    "o012-rbt-l26-audit-007", "o012-rbt-l26-mastery",
    "o012-rbt-l26-mcheck-001", "o012-rbt-l26-hint-001",
    "o012-rbt-l26-sol-001", "o012-rbt-l26-mcheck-002",
    "o012-rbt-l26-hint-002", "o012-rbt-l26-sol-002",
    "o012-rbt-l26-mcheck-003", "o012-rbt-l26-hint-003",
    "o012-rbt-l26-sol-003", "o012-rbt-l26-mcheck-004",
    "o012-rbt-l26-hint-004", "o012-rbt-l26-sol-004",
    "o012-rbt-l26-mcheck-005", "o012-rbt-l26-hint-005",
    "o012-rbt-l26-sol-005", "o012-rbt-l26-mcheck-006",
    "o012-rbt-l26-hint-006", "o012-rbt-l26-sol-006",
    "o012-rbt-l26-boundary-001",
)

NEW_TERMS = {
    "singular-simplex": ("singular simplex", "simpleks singular", "o012-rbt-l26-s01", "algebraic_topology"),
    "singular-cochain-complex": ("singular cochain complex", "kompleks korantai singular", "o012-rbt-l26-def-001", "homological_algebra"),
    "singular-cohomology": ("singular cohomology", "kohomologi singular", "o012-rbt-l26-def-001", "algebraic_topology"),
    "relative-singular-cochain-complex": ("relative singular cochain complex", "kompleks korantai singular relatif", "o012-rbt-l26-def-002", "homological_algebra"),
    "cochain-homotopy": ("cochain homotopy", "homotopi korantai", "o012-rbt-l26-def-003", "homological_algebra"),
    "prism-operator": ("prism operator", "operator prisma", "o012-rbt-l26-proof-009", "algebraic_topology"),
    "finite-coproduct-cohomology": ("finite coproduct cohomology", "kohomologi koproduk hingga", "o012-rbt-l26-prop-004", "algebraic_topology"),
    "stokes-theorem": ("Stokes theorem", "Teorema Stokes", "o012-rbt-l26-aside-001", "differential_topology"),
}

REUSED_CONCEPTS = (
    "concept:geometric-realisation", "concept:standard-n-simplex",
    "concept:cochain-map", "concept:coboundary", "concept:cocycle",
    "concept:connecting-map", "concept:exact-sequence",
    "concept:long-exact-sequence", "concept:relative-cohomology",
    "concept:reduced-cohomology", "concept:pointed-space",
    "concept:pointed-map", "concept:homotopy",
    "concept:homotopy-equivalence", "concept:homotopy-invariance",
    "concept:contractible-space", "concept:coproduct-preservation",
)

# correction id -> (type, source evidence, affected local IDs, defect, change, rationale)
CORRECTIONS = {
    "correction:o012-u026-dossier-001": (
        "hypothesis_repair", "Notes.tex:5620-5633",
        ["aside-001", "audit-001"],
        "The source margin permits interior smoothness plus continuous boundary extension, which is insufficient by itself for the displayed Stokes identity.",
        "Require smoothness up to the simplex boundary for the Stokes display while retaining the weaker convention as a labeled source note.",
        "This states the exact regularity used by the mathematical argument."),
    "correction:o012-u026-dossier-002": (
        "proof_completion", "Notes.tex:5638-5650",
        ["def-001", "prop-001", "proof-001", "audit-002"],
        "The source calls the construction a cochain complex without proving delta squared is zero and leaves the induced contravariant map incompletely typed.",
        "Supply the face-cancellation proof and type postcomposition and pullback explicitly.",
        "The complex and variance are now independently checkable."),
    "correction:o012-u026-dossier-003": (
        "clarification", "Notes.tex:5651-5673",
        ["exa-001", "aside-002"],
        "The alternating point differential and the later justification of interval vanishing are compressed.",
        "Expose the alternating zero/identity calculation and identify contractibility as the later reason for interval vanishing.",
        "The example no longer reads as an unsupported direct computation."),
    "correction:o012-u026-dossier-004": (
        "proof_completion", "Notes.tex:5674-5694",
        ["prop-002", "proof-002"],
        "The source proof omits the degreewise surjectivity argument, connecting morphism, and naturality details.",
        "Give extension by zero, the short exact sequence of cochain complexes, the connecting map, and naturality.",
        "This closes the full long exact sequence assertion."),
    "correction:o012-u026-dossier-005": (
        "mathematical_correction", "Notes.tex:5695-5713",
        ["def-002", "rem-001", "audit-003"],
        "The source leaves the degree-one quotient image unresolved and states the relative-to-ordinary isomorphism only for degrees above one.",
        "Use constant cocycles to prove H0(X)->R surjective, hence the connecting image is zero and the isomorphism holds for every degree at least one.",
        "Exactness determines the omitted degree-one case."),
    "correction:o012-u026-dossier-006": (
        "proof_completion", "Notes.tex:5720-5722 (margin)",
        ["prop-003", "proof-003", "aside-003"],
        "Pointed functoriality is left as a margin exercise.",
        "State and prove it via maps of pairs and contravariant relative cohomology.",
        "A structural property is no longer hidden or unproved."),
    "correction:o012-u026-dossier-007": (
        "mathematical_correction", "Notes.tex:5728-5750",
        ["prop-004", "proof-004", "audit-004"],
        "Two relative-cochain delimiters are mistyped and the coproduct decomposition suppresses connectedness of the simplex domain.",
        "Restore semicolons and prove the decomposition using connectedness of every standard simplex.",
        "The formula and its necessary topological premise are explicit."),
    "correction:o012-u026-dossier-008": (
        "mathematical_correction", "Notes.tex:5763-5771",
        ["cor-002", "proof-006", "audit-005"],
        "The source writes an untyped H^k isomorphic to R after separately treating positive degrees.",
        "Restore the intended degree-zero assertion H^0(X;R) isomorphic to R.",
        "The contractible-space calculation is degree-correct."),
    "correction:o012-u026-dossier-009": (
        "proof_completion", "Notes.tex:5754-5787",
        ["cor-001", "proof-005", "cor-002", "proof-006", "cor-003", "proof-007"],
        "The three consequences of homotopy invariance are stated without complete proofs.",
        "Supply proofs with the contravariant order of induced maps and the path argument for basepoint evaluation.",
        "Every corollary now has complete inferential closure."),
    "correction:o012-u026-dossier-010": (
        "mathematical_correction", "Notes.tex:5790-5803",
        ["lem-001", "proof-008", "audit-006"],
        "The source proof changes the cocycle variable from c to x in its terminal term.",
        "Restore c and explicitly identify the remaining expression as a coboundary.",
        "The proof is type- and variable-consistent."),
    "correction:o012-u026-dossier-011": (
        "proof_completion", "Notes.tex:5805-5823",
        ["thm-002", "proof-009", "audit-007"],
        "The homotopy-invariance theorem ends with only a prism-triangulation sketch and an omitted combinatorial verification.",
        "Construct the signed prism operator, prove its boundary identity by face cancellation, and dualise with the correct sign.",
        "The principal theorem no longer depends on an omitted proof."),
    "correction:o012-u026-dossier-012": (
        "structural_adaptation", "Notes.tex:5620-5624,5668-5669,5720-5722 (margins)",
        ["aside-001", "aside-002", "aside-003", "prop-003"],
        "Three source margins interrupt or hide required reading, including an unproved functoriality exercise.",
        "Reflow all margins into reading order and close the mathematical exercise in the main text.",
        "The adaptation preserves content while improving reader accessibility."),
    "correction:o012-u026-resolved-term-001": (
        "terminology_correction", "unit-026-lecture-026.md pre-admission draft; UNIT026-TERM-P3-001",
        ["def-001", "def-002", "prop-003"],
        "The pre-admission draft used funktor and funktorialitas against admitted lane controls.",
        "Normalize every occurrence to fungtor and fungtorialitas before admission.",
        "The final reader follows O012-TERM-0004, O012-TERM-0072, and O012-TERM-0297."),
}


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canon(obj: dict[str, Any]) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8") + b"\n"


def common(kind: str, ident: str) -> dict[str, Any]:
    return {"entity_type": kind, "id": ident, "schema": SCHEMA,
            "schema_version": VERSION, "status": "active", "supersedes": None,
            "timestamp": STAMP, "workflow": WORKFLOW}


def load_generic():
    path = LANE / "scripts/validate-backend.py"
    spec = importlib.util.spec_from_file_location("o012_generic_u026_producer", path)
    if spec is None or spec.loader is None:
        raise SystemExit("cannot load generic backend validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_prefix() -> tuple[dict[str, dict[str, dict[str, Any]]], dict[str, bytes]]:
    tables: dict[str, dict[str, dict[str, Any]]] = {}
    raw_files: dict[str, bytes] = {}
    bundle = hashlib.sha256()
    seen: set[str] = set()
    for name in FILES:
        raw = (BACKEND / name).read_bytes()
        count, size, expected_sha = PREFIX[name]
        lines = raw.splitlines(keepends=True)
        if (len(raw), len(lines), digest(raw)) != (size, count, expected_sha):
            raise SystemExit(f"{name}: immutable Units 001-025 prefix mismatch")
        if b"\r" in raw or not raw.endswith(b"\n"):
            raise SystemExit(f"{name}: prefix newline mismatch")
        table: dict[str, dict[str, Any]] = {}
        for number, line in enumerate(lines, 1):
            obj = json.loads(line.decode("utf-8"))
            if not isinstance(obj.get("id"), str) or obj["id"] in seen or canon(obj) != line:
                raise SystemExit(f"{name}:{number}: noncanonical/duplicate prefix record")
            seen.add(obj["id"])
            table[obj["id"]] = obj
        tables[name] = table
        raw_files[name] = raw
        bundle.update(name.encode()); bundle.update(b"\0"); bundle.update(raw)
    if (len(seen) != PREFIX_RECORDS
            or sum(len(raw) for raw in raw_files.values()) != PREFIX_BYTES
            or bundle.hexdigest() != PREFIX_BUNDLE):
        raise SystemExit("Units 001-025 backend bundle identity mismatch")
    required = {"unit:o012-rbt-u025", PRIOR_RIGHTS,
                "artifact:o012-units-001-025-pdf",
                "qa:o012-units-001-025-build"}
    if not required <= seen:
        raise SystemExit("Unit 25 cumulative prefix closure is incomplete")
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
    if len(span) != UPSTREAM_SPAN_BYTES or digest(span) != UPSTREAM_SPAN_SHA:
        raise SystemExit("Unit 26 upstream span mismatch")
    if ("\\lecturenum{26}" not in lines[5611]
            or lines[5822].strip() != ""
            or "\\lecturenum{27}" not in lines[5823]):
        raise SystemExit("Unit 26 source boundary identity mismatch")


def structural_spans(lines: list[str]) -> dict[str, tuple[int, int, str]]:
    opening = re.compile(r"^\s*:::\s+\{[^#}]*#(o012-rbt-l26(?:-[A-Za-z0-9-]+)?)(.*)\}\s*$")
    heading = re.compile(r"^#{1,6}\s+.*\{[^}]*#(o012-rbt-l26(?:-[A-Za-z0-9-]+)?)[^}]*\}\s*$")
    stack: list[tuple[str, int, str]] = []
    spans: dict[str, tuple[int, int, str]] = {}
    ordered: list[str] = []
    for number, line in enumerate(lines, 1):
        hm = heading.match(line)
        if hm:
            ordered.append(hm.group(1))
        fm = opening.match(line)
        if fm:
            ordered.append(fm.group(1))
            stack.append((fm.group(1), number, line))
        elif line.strip() == ":::":
            if not stack:
                raise SystemExit(f"unexpected div close at reader line {number}")
            ident, start, opener = stack.pop()
            if ident in spans:
                raise SystemExit(f"duplicate fenced anchor: {ident}")
            spans[ident] = (start, number, opener)
    if stack:
        raise SystemExit(f"unclosed div anchors: {[item[0] for item in stack]}")
    headings = {
        "o012-rbt-l26-notice": (12, 51), "o012-rbt-l26": (52, 853),
        "o012-rbt-l26-s01": (54, 137), "o012-rbt-l26-s02": (138, 293),
        "o012-rbt-l26-s03": (294, 495), "o012-rbt-l26-s04": (496, 570),
        "o012-rbt-l26-s05": (571, 853),
        "o012-rbt-l26-mastery": (854, 1194),
    }
    for ident, (start, end) in headings.items():
        if ident not in lines[start - 1]:
            raise SystemExit(f"heading span identity mismatch: {ident}")
        spans[ident] = (start, end, lines[start - 1])
    if tuple(ordered) != EXPECTED_ANCHORS or set(spans) != set(EXPECTED_ANCHORS):
        raise SystemExit("Unit 26 stable-ID inventory/order mismatch")
    return spans


def unit_kind(ident: str, opener: str) -> str:
    if ident.endswith("-notice"):
        return "notice"
    if ident == "o012-rbt-l26":
        return "lecture"
    if ident.endswith("-mastery"):
        return "mastery_section"
    if re.fullmatch(r"o012-rbt-l26-s\d{2}", ident):
        return "section"
    match = re.search(r"\{\.([A-Za-z][A-Za-z0-9_-]*)", opener)
    kind = (match.group(1).replace("source-audit", "source_audit")
            .replace("source-margin", "source_margin") if match else "")
    allowed = {"aside", "boundary", "corollary", "definition", "example",
               "exercise", "hint", "lemma", "proof", "proposition", "remark",
               "solution", "source_audit", "theorem"}
    if kind not in allowed:
        raise SystemExit(f"cannot infer kind for {ident}: {kind!r}")
    return kind


def provenance(ident: str, kind: str, opener: str) -> tuple[str, str, bool]:
    if (kind in {"notice", "source_audit", "mastery_section", "boundary",
                 "hint", "solution"} or "-mcheck-" in ident
            or 'data-origin="edition-' in opener):
        return "edition_original", COMPANION_RIGHTS, True
    if 'data-origin="source-' in opener:
        return "translated_source_with_edition_completion", COMPOSITE_RIGHTS, False
    return "translated_adapted_from_upstream", ROBERTS_RIGHTS, False


def target_locator(start: int, end: int, raw_lines: list[bytes]) -> dict[str, Any]:
    return {"content_sha256": digest(b"".join(raw_lines[start - 1:end])),
            "file_sha256": SOURCE_SHA, "line_end": end, "line_start": start,
            "path": SOURCE_PATH}


def source_locator(edition_original: bool) -> dict[str, Any]:
    if edition_original:
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
        value = line.strip().replace("**", "")
        if value and not value.startswith(":::") and not value.startswith(">"):
            return value[:180]
    return f"Unit 26 {kind} {ident.rsplit('-', 1)[-1]}"


def verify_evidence() -> tuple[dict[str, Any], dict[str, tuple[int, str]]]:
    identities: dict[str, tuple[int, str]] = {}
    for ident, (relative, size, expected_sha, _media, _state, _qas) in EVIDENCE.items():
        raw = (LANE / relative).read_bytes()
        if len(raw) != size or digest(raw) != expected_sha:
            raise SystemExit(f"Unit 26 evidence identity mismatch: {relative}")
        identities[ident] = (size, expected_sha)
    qa_raw = QA_JSON.read_bytes()
    qa = json.loads(qa_raw.decode("utf-8"))
    resolved = qa.get("resolved_findings")
    if (qa.get("status") != "PASS"
            or qa.get("source", {}).get("line_start") != UPSTREAM_START
            or qa.get("source", {}).get("line_end") != UPSTREAM_END
            or qa.get("source", {}).get("span_bytes") != UPSTREAM_SPAN_BYTES
            or qa.get("source", {}).get("span_sha256") != UPSTREAM_SPAN_SHA
            or qa.get("source", {}).get("next_line") != NEXT_SOURCE_LINE
            or qa.get("unit", {}).get("bytes") != SOURCE_BYTES
            or qa.get("unit", {}).get("lines") != SOURCE_LINES
            or qa.get("unit", {}).get("sha256") != SOURCE_SHA
            or qa.get("unit", {}).get("stable_ids") != 62
            or qa.get("unit", {}).get("fenced_semantic_objects") != 54
            or qa.get("proof_closure", {}).get("mastery_solution_triples") != 6
            or qa.get("model_provenance") != MODEL):
        raise SystemExit("Unit 26 QA content/binding mismatch")
    expected_resolved = {"UNIT026-MATH-P2-001", "UNIT026-TERM-P3-001"}
    if (not isinstance(resolved, list)
            or {item.get("finding_id") for item in resolved} != expected_resolved
            or any(item.get("status") != "RESOLVED_BEFORE_ADMISSION" for item in resolved)):
        raise SystemExit("Unit 26 resolved-finding closure mismatch")
    checks = qa.get("checks")
    if not isinstance(checks, list) or not checks or any(
            not isinstance(item, dict) or item.get("status") != "PASS" for item in checks):
        raise SystemExit("Unit 26 QA contains a non-passing check")
    return qa, identities


def main() -> int:
    tables, prefix_raw = load_prefix()
    verify_upstream()
    qa_doc, _identities = verify_evidence()
    existing_ids = {ident for table in tables.values() for ident in table}
    additions: dict[str, dict[str, dict[str, Any]]] = {name: {} for name in FILES}

    def add(name: str, obj: dict[str, Any]) -> None:
        ident = obj["id"]
        if ident in existing_ids or any(ident in table for table in additions.values()):
            raise SystemExit(f"duplicate new ID: {ident}")
        additions[name][ident] = obj

    raw = SOURCE.read_bytes()
    if (len(raw) != SOURCE_BYTES or digest(raw) != SOURCE_SHA or b"\r" in raw
            or not raw.endswith(b"\n")):
        raise SystemExit("Unit 26 reader identity/newline mismatch")
    raw_lines = raw.splitlines(keepends=True)
    lines = [line.decode("utf-8").rstrip("\n") for line in raw_lines]
    text = raw.decode("utf-8")
    if (len(lines) != SOURCE_LINES or text.count(MODEL) != 1
            or re.search(r"\bfunktor(?:ialitas)?\b", text, re.IGNORECASE)):
        raise SystemExit("Unit 26 reader line/provenance/terminology mismatch")
    spans = structural_spans(lines)

    for slug, (source_term, _preferred, _evidence, domain) in NEW_TERMS.items():
        concept = common("concept", f"concept:{slug}")
        concept.update({"canonical_label": source_term, "domain": domain,
                        "locale_neutral": True})
        add("concepts.jsonl", concept)
    concept_ids = list(REUSED_CONCEPTS) + [f"concept:{slug}" for slug in NEW_TERMS]
    if any(ident not in existing_ids and ident not in additions["concepts.jsonl"]
           for ident in concept_ids):
        raise SystemExit("Unit 26 concept closure mismatch")

    rights_specs = (
        (COMPANION_RIGHTS,
         "Indonesian original mastery, source-audit, proof-completion, and accessibility layer for Roberts Unit 26.",
         "Original additions are CC BY 4.0; source-derived material remains separately attributed.",
         [ROOT], None),
        (COMPOSITE_RIGHTS,
         "David Michael Roberts source adaptation plus original Indonesian Unit 26 companions.",
         "Translated, repaired, and original layers remain component-distinguishable.",
         [ROOT], None),
        (CUMULATIVE_RIGHTS,
         "Cumulative Roberts Units 001-026 Indonesian reader source boundary.",
         "Append-only semantic pointer; verified prior build artifacts remain immutable until a separate build admission.",
         [f"unit:o012-rbt-u{number:03d}" for number in range(1, 27)], PRIOR_RIGHTS),
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
        ("o012-rbt-l26-s01", 54, 137), ("o012-rbt-l26-s02", 138, 293),
        ("o012-rbt-l26-s03", 294, 495), ("o012-rbt-l26-s04", 496, 570),
        ("o012-rbt-l26-s05", 571, 853),
    )
    section_ids = {item[0] for item in section_ranges}

    def parent_local(ident: str, start: int) -> str:
        if ident in {"o012-rbt-l26-notice", "o012-rbt-l26",
                     "o012-rbt-l26-mastery", "o012-rbt-l26-boundary-001"}:
            return ROOT
        if ident in section_ids:
            return LECTURE
        if any(token in ident for token in ("-mcheck-", "-hint-", "-sol-")):
            return MASTERY
        for section, low, high in section_ranges:
            if low <= start <= high:
                return f"unit:{section}"
        raise SystemExit(f"cannot assign Unit 26 parent: {ident}")

    children: defaultdict[str, list[str]] = defaultdict(list)
    for ident in EXPECTED_ANCHORS:
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
        "display_title": "Topologi Aljabar - Unit 26: Korantai Singular, Kohomologi Tereduksi, dan Invariansi Homotopi",
        "edition_id": EDITION, "edition_unit_id": ROOT, "locale": "id-ID",
        "model_provenance": MODEL, "order": 26, "parent_id": COURSE,
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

    for ident in EXPECTED_ANCHORS:
        start, end, opener = spans[ident]
        kind = unit_kind(ident, opener)
        parent_id = parent_local(ident, start)
        if parent_id not in path_by_id:
            raise SystemExit(f"parent path not yet constructed: {ident} -> {parent_id}")
        unit_id = f"unit:{ident}"
        path = path_by_id[parent_id] + [unit_id]
        path_by_id[unit_id] = path
        provenance_value, rights_id, edition_original = provenance(ident, kind, opener)
        locator = target_locator(start, end, raw_lines)
        shared = {"component_source_commit": COMMIT,
                  "component_source_id": RESOURCE,
                  "course_route_unit_id": ROUTE, "edition_unit_id": ROOT,
                  "model_provenance": MODEL}
        unit = common("unit", unit_id)
        unit.update(shared)
        unit.update({"concept_ids": concept_ids, "course_id": COURSE,
                     "display_title": display_title(ident, lines, start, kind),
                     "edition_id": EDITION, "locale": "id-ID",
                     "order": order_map[parent_id][ident], "parent_id": parent_id,
                     "path": path, "program_id": PROGRAM,
                     "provenance_relation": provenance_value,
                     "resource_id": RESOURCE, "rights_component_id": rights_id,
                     "source_local_id": ident, "target_locator": locator,
                     "translation_state": "structurally_verified", "unit_kind": kind})
        segment = common("segment", f"segment:{ident}")
        segment.update(shared)
        segment.update({"concept_ids": concept_ids, "edition_id": EDITION,
                        "locale": "id-ID", "order": unit["order"],
                        "provenance_relation": provenance_value,
                        "resource_id": RESOURCE, "rights_component_id": rights_id,
                        "segment_kind": kind, "source_local_id": ident,
                        "source_locator": source_locator(edition_original),
                        "target_locator": locator,
                        "translation_state": "structurally_verified",
                        "unit_id": unit_id})
        aliases = re.findall(r'data-source-label="([^"]+)"', opener)
        if aliases:
            unit["source_aliases"] = aliases
            segment["source_aliases"] = aliases
        if ident == "o012-rbt-l26-boundary-001":
            unit["next_source_line"] = NEXT_SOURCE_LINE
            segment["next_source_line"] = NEXT_SOURCE_LINE
        if kind == "proof":
            proof_status = ({"edition_original": "complete_original_proof",
                             "translated_source_with_edition_completion":
                                 "complete_source_proof_with_edition_completion"}
                            .get(provenance_value, "complete_translated_source_proof"))
            unit["proof_status"] = proof_status
            segment["proof_status"] = proof_status
        if kind == "solution":
            unit["solution_status"] = "complete_checked_solution"
            segment["solution_status"] = "complete_checked_solution"
        add("units.jsonl", unit)
        add("segments.jsonl", segment)

    asset = common("asset", "asset:o012-u026-source-markdown")
    asset.update({"bytes": SOURCE_BYTES, "edition_id": EDITION,
                  "media_type": "text/markdown; charset=utf-8", "path": SOURCE_PATH,
                  "resource_id": RESOURCE, "rights_component_id": COMPOSITE_RIGHTS,
                  "role": "canonical_reader_source", "sha256": SOURCE_SHA})
    add("assets.jsonl", asset)

    for slug, (source_term, preferred, evidence, _domain) in NEW_TERMS.items():
        term = common("term", f"term:{slug}:id-ID")
        term.update({"concept_id": f"concept:{slug}",
                     "evidence_segment_id": f"segment:{evidence}", "locale": "id-ID",
                     "preferred": preferred, "register": "textbook",
                     "rejected_forms": [], "rights_component_id": ROBERTS_RIGHTS,
                     "scope_unit_id": ROOT, "source_term": source_term,
                     "terminology_status": "unit_attested_reviewed",
                     "usage_note": "Attested in the independently reviewed Unit 26 reader; no global terminology control file was changed by this append.",
                     "variants": []})
        add("terms.jsonl", term)

    for ident, (correction_type, evidence, suffixes, defect, change, rationale) in CORRECTIONS.items():
        targets = [f"unit:o012-rbt-l26-{suffix}" for suffix in suffixes]
        if any(target.removeprefix("unit:") not in spans for target in targets):
            raise SystemExit(f"correction target absent: {ident}")
        correction = common("correction", ident)
        correction.update({"affected_unit_ids": targets,
                           "correction_type": correction_type,
                           "edition_id": EDITION, "evidence": evidence,
                           "evidence_segment_id": "segment:o012-rbt-l26-notice",
                           "rationale": rationale, "resource_id": RESOURCE,
                           "source_defect": defect, "target_change": change,
                           "unit_id": ROOT,
                           "upstream_report_disposition": "not_contacted"})
        add("corrections.jsonl", correction)

    for ident, (relative, size, expected_sha, media_type, state, qa_ids) in EVIDENCE.items():
        artifact = common("artifact", ident)
        artifact.update({"bytes": size, "locale": "id-ID",
                         "manifest_artifact_id": None, "media_type": media_type,
                         "path": relative, "qa_event_ids": qa_ids,
                         "rights_component_id": COMPOSITE_RIGHTS,
                         "sha256": expected_sha,
                         "toolchain": (f"Bounded Unit 26 evidence; Notes.tex:5612-5823 "
                                       f"span {UPSTREAM_SPAN_SHA}; {MODEL}; route {ROUTE}; "
                                       "no cumulative build/publication assertion."),
                         "translation_state": state, "unit_id": ROOT})
        add("artifacts.jsonl", artifact)

    qa_specs = (
        ("qa:o012-u026-source-integrity", "source",
         "Unit 26 authority and reader identities, 62 stable IDs, source census, controls, and structural render passed.",
         ["artifact:o012-u026-source-audit", "artifact:o012-u026-qa"]),
        ("qa:o012-u026-math", "math",
         "Independent Unit 26 mathematical review passed with no open P1, P2, or P3 finding and nine complete proof objects.",
         ["artifact:o012-u026-independent-review"]),
        ("qa:o012-u026-language", "language",
         "Independent Indonesian review passed after the Stokes-regularity and fungtor terminology findings were resolved before admission.",
         ["artifact:o012-u026-independent-review", "artifact:o012-u026-qa"]),
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

    relation("relation:adapts:o012-rbt-u026:edition", ROOT, "adapts", EDITION,
             "Unit 26 is the Indonesian adapted reader boundary for the frozen Roberts edition.")
    relation("relation:precedes:o012-rbt-u025:o012-rbt-u026",
             "unit:o012-rbt-u025", "precedes", ROOT,
             "Preserves contiguous Roberts lecture-unit order.")
    relation("relation:precedes:o012-rbt-l26:mastery", LECTURE, "precedes", MASTERY,
             "Lecture content precedes the Unit 26 mastery companion.")
    relation("relation:boundary:o012-u026", CUMULATIVE_RIGHTS, "contains", ROOT,
             "Additive cumulative Units 001-026 semantic source boundary.")
    relation("relation:route:d60-r13:o012-rbt-u026", COURSE, "contains", ROOT,
             "Roberts Lecture 26 remains an edition unit in the non-destructive D60-R13 route view.",
             course_route_unit_id=ROUTE, edition_unit_id=ROOT)
    relation("relation:depends-on:o012-rbt-l26-proof-002:l24-thm-001",
             "unit:o012-rbt-l26-proof-002", "depends-on",
             "unit:o012-rbt-l24-thm-001",
             "The pair long exact sequence invokes the previously admitted algebraic long-exact-sequence theorem.")
    relation("relation:proves:o012-rbt-l26-thm-002:thm-001",
             "unit:o012-rbt-l26-thm-002", "proves",
             "unit:o012-rbt-l26-thm-001",
             "The cochain-level theorem supplies the announced homotopy invariance on cohomology.")
    proof_targets = {
        1: "unit:o012-rbt-l26-prop-001", 2: "unit:o012-rbt-l26-prop-002",
        3: "unit:o012-rbt-l26-prop-003", 4: "unit:o012-rbt-l26-prop-004",
        5: "unit:o012-rbt-l26-cor-001", 6: "unit:o012-rbt-l26-cor-002",
        7: "unit:o012-rbt-l26-cor-003", 8: "unit:o012-rbt-l26-lem-001",
        9: "unit:o012-rbt-l26-thm-002",
    }
    for number, target in proof_targets.items():
        relation(f"relation:proves:o012-rbt-l26-proof-{number:03d}:closure",
                 f"unit:o012-rbt-l26-proof-{number:03d}", "proves", target,
                 f"Complete proof closure {number} for Unit 26.")
    for number in range(1, 7):
        relation(f"relation:solves:l26-sol-{number:03d}:l26-mcheck-{number:03d}",
                 f"unit:o012-rbt-l26-sol-{number:03d}", "solves",
                 f"unit:o012-rbt-l26-mcheck-{number:03d}",
                 f"Complete checked solution for Unit 26 mastery check {number}.")
        relation(f"relation:hints:l26-hint-{number:03d}:l26-mcheck-{number:03d}",
                 f"unit:o012-rbt-l26-hint-{number:03d}", "hints",
                 f"unit:o012-rbt-l26-mcheck-{number:03d}",
                 f"Bounded hint for Unit 26 mastery check {number}.")

    merged = {name: dict(tables[name]) for name in FILES}
    for name in FILES:
        merged[name].update(additions[name])
    by_id = {ident: obj for table in merged.values() for ident, obj in table.items()}
    if len(by_id) != sum(len(table) for table in merged.values()):
        raise SystemExit("global duplicate backend IDs")
    records = [obj for name in FILES for obj in merged[name].values()]
    generic = load_generic()
    generic.validate_shapes(records)
    generic.validate_references(records, by_id)
    generic.validate_artifact_manifests(records, LANE)

    for ident in EXPECTED_ANCHORS:
        unit = by_id[f"unit:{ident}"]
        segment = by_id[f"segment:{ident}"]
        if unit["target_locator"] != segment["target_locator"]:
            raise SystemExit(f"unit/segment locator mismatch: {ident}")
        if unit["path"][-1] != unit["id"]:
            raise SystemExit(f"noncanonical Unit 26 path: {ident}")
        if unit["parent_id"].startswith("unit:"):
            if unit["path"][:-1] != by_id[unit["parent_id"]]["path"]:
                raise SystemExit(f"Unit 26 parent path mismatch: {ident}")
        for obj in (unit, segment):
            if (obj["edition_unit_id"] != ROOT or obj["course_route_unit_id"] != ROUTE
                    or obj["model_provenance"] != MODEL):
                raise SystemExit(f"Unit 26 route/provenance mismatch: {ident}")
    sibling_orders: defaultdict[str, list[int]] = defaultdict(list)
    for obj in additions["units.jsonl"].values():
        sibling_orders[obj["parent_id"]].append(obj["order"])
    if any(len(values) != len(set(values)) for values in sibling_orders.values()):
        raise SystemExit("duplicate Unit 26 sibling order")
    for number in range(1, 7):
        check = f"unit:o012-rbt-l26-mcheck-{number:03d}"
        solves = [obj for obj in additions["relations.jsonl"].values()
                  if obj["relation_type"] == "solves" and obj["to_id"] == check]
        hints = [obj for obj in additions["relations.jsonl"].values()
                 if obj["relation_type"] == "hints" and obj["to_id"] == check]
        if len(solves) != 1 or len(hints) != 1:
            raise SystemExit(f"Unit 26 mastery closure mismatch: {number}")
    proofs = [obj for obj in additions["units.jsonl"].values()
              if obj.get("proof_status")]
    if len(proofs) != 9:
        raise SystemExit("Unit 26 nine-proof closure mismatch")
    if len(additions["corrections.jsonl"]) != len(CORRECTIONS):
        raise SystemExit("Unit 26 correction dossier mismatch")
    if additions["rights.jsonl"][CUMULATIVE_RIGHTS]["component_scope"] != [
            f"unit:o012-rbt-u{number:03d}" for number in range(1, 27)]:
        raise SystemExit("Unit 26 cumulative rights scope mismatch")
    if by_id["unit:o012-rbt-l26-boundary-001"].get("next_source_line") != NEXT_SOURCE_LINE:
        raise SystemExit("Unit 26 terminal cursor mismatch")
    aliases = {alias: unit["id"] for unit in additions["units.jsonl"].values()
               for alias in unit.get("source_aliases", [])}
    if aliases != {"prop:les_of_pair_of_spaces": "unit:o012-rbt-l26-prop-002",
                   "thm:homotopy_invariance_cohom": "unit:o012-rbt-l26-thm-001"}:
        raise SystemExit("Unit 26 source-label alias closure mismatch")
    if {item.get("finding_id") for item in qa_doc["resolved_findings"]} != {
            "UNIT026-MATH-P2-001", "UNIT026-TERM-P3-001"}:
        raise SystemExit("Unit 26 pre-admission finding set changed")

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
    print("Unit 026 semantic backend extension: PASS")
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
    print(f"stable_ids={len(EXPECTED_ANCHORS)}")
    print("proof_closures=9")
    print("mastery_triples=6")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
