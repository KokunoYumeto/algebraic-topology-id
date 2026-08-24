#!/usr/bin/env python3
"""Fail-closed append-only semantic-backend admission for Roberts Unit 027.

The complete 4,105-record Units 001--026 semantic backend is immutable. This
transaction verifies that exact byte prefix plus the final Unit 27 authority,
reader, audit, independent review, and QA witnesses, then appends only the
Unit 27 semantic slice. It does not mutate reader or build artifacts.
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
SOURCE = LANE / "source/id-ID/units/unit-027-lecture-027.md"
UPSTREAM = (LANE / "authority/upstream" /
            "AlgebraicTopology2019-b947ad2e9f9e301bfe24590a9db653bc54fa1a53" /
            "Notes.tex")
AUDIT = LANE / "qa/UNIT_027_SOURCE_AUDIT.md"
REVIEW = LANE / "qa/UNIT_027_INDEPENDENT_REVIEW.md"
QA_JSON = LANE / "qa/UNIT_027_QA.json"

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
COMPANION_RIGHTS = "rights:o012-u027-companion-cc-by-4.0"
COMPOSITE_RIGHTS = "rights:o012-u027-composite-cc-by-4.0"
CUMULATIVE_RIGHTS = "rights:o012-units-001-027-composite-cc-by-4.0"
PRIOR_RIGHTS = "rights:o012-units-001-026-composite-cc-by-4.0"
ROOT = "unit:o012-rbt-u027"
LECTURE = "unit:o012-rbt-l27"
MASTERY = "unit:o012-rbt-l27-mastery"
SOURCE_PATH = "source/id-ID/units/unit-027-lecture-027.md"
SOURCE_BYTES = 35879
SOURCE_LINES = 1175
SOURCE_SHA = "a3238bbc429e4c3689bce3b3bb78c5514e0fae74f276c9efebe694730b2df2a0"
UPSTREAM_BYTES = 331447
UPSTREAM_LINES = 6368
UPSTREAM_SHA = "cfe93e9dbe3e25bd96f711f59e6078ab97527682b58e1f8ad127f74357f665d7"
UPSTREAM_START = 5824
UPSTREAM_END = 5923
UPSTREAM_SPAN_BYTES = 7012
UPSTREAM_SPAN_SHA = "65d2c393ddf29183f36d6e9ab65c65f8030110334f89c7f68ba88461fc30afa1"
NEXT_SOURCE_LINE = 5924

FILES = ("artifacts.jsonl", "assets.jsonl", "authority.jsonl", "concepts.jsonl",
         "corrections.jsonl", "qa.jsonl", "relations.jsonl", "rights.jsonl",
         "segments.jsonl", "terms.jsonl", "units.jsonl")
PREFIX = {
    "artifacts.jsonl": (148, 118081, "75ca44ea07393c83d2cf57f50d8c8db7944921099f8ab43f64efbc166d714e0d"),
    "assets.jsonl": (28, 17295, "7f8953ab04264df0c9ee63db7e277f2b7e9e126fcb5514fcb3ad6eb142d72a68"),
    "authority.jsonl": (4, 2721, "f21af26912520ab34b38dff0e927ed46a546dbe5d318da0dc133e58330d0e368"),
    "concepts.jsonl": (333, 104854, "645061fd18b6ff32c1d9c773508259e97ca0b2fd8cbf1ec8fc22403e82b43acc"),
    "corrections.jsonl": (345, 339810, "9ddf73f800001c6f1c5f6b1e5a0fe2e1f33483101ea8855c106370976cbdba0b"),
    "qa.jsonl": (122, 68974, "177448acf95ac6a0988825fccf5b8d25288720b92f3234982acfb59e97915efb"),
    "relations.jsonl": (425, 173541, "fe2485035d5b488adede6d1926f334c3f41a7d57f36af2315e1bf64249a79b1b"),
    "rights.jsonl": (74, 68380, "47db4fd8e4d817368d00cf732de25b44163dead640b84292628f2a164a6ebfae"),
    "segments.jsonl": (1137, 1553154, "8ef04b73e87221da393f3dacdb5600c62dc3bd6dfe379f648b9498e795a69529"),
    "terms.jsonl": (326, 203570, "61f88694434a122038ce7f26fd1adef4c3ec4f145bf0f88466ba1b3ab1e62f8b"),
    "units.jsonl": (1163, 1654838, "df7a5ad97b5e6ea3551b8bb353e8a93620061e3c7219e656d0b5c3484d233fbf"),
}
PREFIX_RECORDS = 4105
PREFIX_BYTES = 4305218
PREFIX_BUNDLE = "89556c5fa2224820837fc8956b1a48797929f28bef013baf9a613e73e6cf28eb"

EVIDENCE = {
    "artifact:o012-u027-source-audit": (
        "qa/UNIT_027_SOURCE_AUDIT.md", 7369,
        "67621ce38a69fe4e6afd24fa6572dfa6e9499a3e77db03e3943ce045dfa30138",
        "text/markdown; charset=utf-8", "source_frozen",
        ["qa:o012-u027-source-integrity"]),
    "artifact:o012-u027-independent-review": (
        "qa/UNIT_027_INDEPENDENT_REVIEW.md", 8560,
        "d464310e42fea0c199b49a6a9670d97cf8704b3c37b7cc79023fece21cb734b5",
        "text/markdown; charset=utf-8", "mathematically_reviewed",
        ["qa:o012-u027-math", "qa:o012-u027-language"]),
    "artifact:o012-u027-qa": (
        "qa/UNIT_027_QA.json", 8152,
        "1db997b0ddf1dee05583c8c8c482e68f59a9add7677b34fded034088f55e491f",
        "application/json", "built",
        ["qa:o012-u027-source-integrity", "qa:o012-u027-language"]),
}

EXPECTED_ANCHORS = (
    "o012-rbt-l27-notice", "o012-rbt-l27", "o012-rbt-l27-s01",
    "o012-rbt-l27-mcheck-001", "o012-rbt-l27-hint-001",
    "o012-rbt-l27-sol-001", "o012-rbt-l27-audit-001",
    "o012-rbt-l27-def-001", "o012-rbt-l27-lem-001",
    "o012-rbt-l27-proof-001", "o012-rbt-l27-margin-001",
    "o012-rbt-l27-def-002", "o012-rbt-l27-exa-001",
    "o012-rbt-l27-audit-002", "o012-rbt-l27-exa-002",
    "o012-rbt-l27-s02", "o012-rbt-l27-fig-001", "o012-rbt-l27-eq-001",
    "o012-rbt-l27-audit-003", "o012-rbt-l27-prop-001",
    "o012-rbt-l27-proof-002", "o012-rbt-l27-s03",
    "o012-rbt-l27-thm-001", "o012-rbt-l27-proof-003",
    "o012-rbt-l27-audit-004", "o012-rbt-l27-s04",
    "o012-rbt-l27-exa-003", "o012-rbt-l27-eq-002",
    "o012-rbt-l27-audit-005", "o012-rbt-l27-mastery",
    "o012-rbt-l27-mcheck-002", "o012-rbt-l27-hint-002",
    "o012-rbt-l27-sol-002", "o012-rbt-l27-mcheck-003",
    "o012-rbt-l27-hint-003", "o012-rbt-l27-sol-003",
    "o012-rbt-l27-mcheck-004", "o012-rbt-l27-hint-004",
    "o012-rbt-l27-sol-004", "o012-rbt-l27-mcheck-005",
    "o012-rbt-l27-hint-005", "o012-rbt-l27-sol-005",
    "o012-rbt-l27-mcheck-006", "o012-rbt-l27-hint-006",
    "o012-rbt-l27-sol-006", "o012-rbt-l27-boundary-001",
)

NEW_TERMS = {
    "left-splitting": ("left splitting", "pembelahan kiri", "o012-rbt-l27-def-001", "homological_algebra"),
    "reduced-degree-zero-cohomology": ("reduced degree-zero cohomology", "kohomologi tereduksi derajat nol", "o012-rbt-l27-def-002", "algebraic_topology"),
    "small-singular-chain-complex": ("small singular chain complex", "kompleks rantai singular kecil", "o012-rbt-l27-prop-001", "algebraic_topology"),
    "small-singular-cochain-complex": ("small singular cochain complex", "kompleks korantai singular kecil", "o012-rbt-l27-audit-003", "algebraic_topology"),
    "barycentric-subdivision": ("barycentric subdivision", "subdivisi barisentris", "o012-rbt-l27-proof-002", "algebraic_topology"),
    "chain-homotopy-equivalence": ("chain-homotopy equivalence", "ekuivalensi homotopi rantai", "o012-rbt-l27-prop-001", "homological_algebra"),
    "mayer-vietoris-long-exact-sequence": ("Mayer--Vietoris long exact sequence", "barisan eksak panjang Mayer--Vietoris", "o012-rbt-l27-thm-001", "algebraic_topology"),
    "sphere-cohomology": ("sphere cohomology", "kohomologi sfera", "o012-rbt-l27-exa-003", "algebraic_topology"),
}

REUSED_CONCEPTS = (
    "concept:path-component", "concept:reduced-cohomology",
    "concept:singular-cohomology", "concept:extension-by-zero",
    "concept:quasi-isomorphism", "concept:pushout",
    "concept:long-exact-sequence", "concept:cochain-homotopy",
    "concept:contractible-space", "concept:cocycle", "concept:coboundary",
    "concept:kernel", "concept:cokernel", "concept:direct-sum",
    "concept:open-cover",
)

CORRECTIONS = {
    "correction:o012-u027-dossier-001": (
        "solution_completion", "Notes.tex:5825-5829",
        ["mcheck-001", "hint-001", "sol-001", "audit-001"],
        "The formal source exercise identifying degree-zero cohomology with functions on path components has no supplied solution.",
        "Supply a complete cocycle, coboundary, and functoriality argument.",
        "The preserved source exercise becomes usable for independent study."),
    "correction:o012-u027-dossier-002": (
        "mathematical_correction", "Notes.tex:5830-5833",
        ["audit-001"],
        "The source types the composite from a point back to a point as the identity on X.",
        "Restore the correctly typed identity on the one-point space and derive the split injection contravariantly.",
        "The map domains and codomains now agree."),
    "correction:o012-u027-dossier-003": (
        "proof_completion", "Notes.tex:5834-5842",
        ["def-001", "lem-001", "proof-001"],
        "The direct-sum consequence of a left splitting is stated without proof.",
        "Construct the isomorphism and its inverse, including the restriction to the kernel.",
        "The cokernel/kernel model is fully justified."),
    "correction:o012-u027-dossier-004": (
        "structural_adaptation", "Notes.tex:5843-5844 (margin)",
        ["margin-001"],
        "The basepoint-independence qualification is isolated in a source margin.",
        "Move it into reading order while preserving the distinction between canonical cokernel and chosen kernel model.",
        "Essential interpretation remains accessible in linear reading."),
    "correction:o012-u027-dossier-005": (
        "mathematical_correction", "Notes.tex:5845-5850",
        ["def-002", "exa-001", "audit-002"],
        "The source lets an all-degree phrase ambiguously modify a degree-zero reduced group.",
        "Restrict the path-connected assertion to degree zero and state contractible all-degree vanishing separately.",
        "The degree scope is mathematically explicit."),
    "correction:o012-u027-dossier-006": (
        "accessibility_reflow", "Notes.tex:5855-5865 (Xy-pic)",
        ["fig-001"],
        "The pushout is encoded by position-dependent Xy-pic layout.",
        "Replace it with a semantic arrow table, commutativity statement, and universal property.",
        "The same mathematics is available to reflowable and assistive readers."),
    "correction:o012-u027-dossier-007": (
        "mathematical_correction", "Notes.tex:5867-5880",
        ["eq-001", "audit-003", "prop-001", "proof-002"],
        "The source's zero-extension small-cochain subcomplex is not differential-stable, and its comparison arrow points the wrong way.",
        "Define small cochains as the dual of the small-chain subcomplex and use restriction from all cochains.",
        "The corrected complex is valid and contravariance fixes the arrow direction."),
    "correction:o012-u027-dossier-008": (
        "proof_completion", "Notes.tex:5874-5880",
        ["prop-001", "proof-002", "audit-003"],
        "The source relies on an external homology citation for the small-chain comparison.",
        "Give the barycentric subdivision, prism homotopy, Lebesgue-number, and inductive inverse construction.",
        "The quasi-isomorphism is proved internally for every coefficient ring."),
    "correction:o012-u027-dossier-009": (
        "proof_completion", "Notes.tex:5881-5908",
        ["thm-001", "proof-003", "audit-004"],
        "The Mayer--Vietoris connector and exactness are abbreviated, and the reduced opening zero lacks the nonempty-intersection hypothesis.",
        "Construct the connector, prove image equals kernel at all recurring term types, and type the reduced hypothesis.",
        "The complete long exact sequence is valid under the stated convention."),
    "correction:o012-u027-dossier-010": (
        "proof_completion", "Notes.tex:5909-5923",
        ["exa-003", "eq-002", "audit-005"],
        "The sphere calculation compresses the recurrence and omits parts of the all-degree conclusion.",
        "State the hemispherical cover, suspension recurrence, base case, and full induction.",
        "Every cohomology degree of each sphere is accounted for."),
    "correction:o012-u027-dossier-011": (
        "clarification", "Notes.tex:5910-5923",
        ["thm-001", "proof-003", "exa-003"],
        "Minor prose, a dangling comma, closed-disc wording, and negative horizontal spacing obscure the argument.",
        "Repair prose and geometry locally and reflow the wide sequence without negative spacing.",
        "The content remains source-faithful and readable."),
    "correction:o012-u027-resolved-math-001": (
        "mathematical_correction", "unit-027-lecture-027.md:481; UNIT027-MATH-P2-001",
        ["prop-001"],
        "The pre-admission comparison formula lost the command marker on its arrow.",
        "Restore the mathematical long arrow with its original objects and direction.",
        "The final formula renders and types correctly."),
    "correction:o012-u027-resolved-a11y-002": (
        "accessibility_reflow", "unit-027-lecture-027.md:369-373; UNIT027-A11Y-P2-002",
        ["fig-001"],
        "The first semantic pushout array still contained TeX arrow syntax rejected by fatal native-MathML conversion.",
        "Use an equivalent MathML-convertible semantic array.",
        "The final diagram preserves meaning and passes offline conversion."),
    "correction:o012-u027-resolved-proof-003": (
        "proof_completion", "unit-027-lecture-027.md:693-715; UNIT027-PROOF-P2-003",
        ["proof-003"],
        "The pre-admission proof constructed the connector but only asserted exactness at recurring term types.",
        "Add explicit lift and adjustment arguments in both directions.",
        "Every image-equals-kernel claim is now demonstrated."),
    "correction:o012-u027-resolved-term-001": (
        "terminology_correction", "unit-027-lecture-027.md pre-admission draft; UNIT027-TERM-P3-001",
        ["audit-003", "mcheck-004", "sol-005"],
        "The draft used perpanjangan-based variants for extension by zero.",
        "Normalize to perluasan dengan nol and corresponding grammatical verb forms.",
        "The final reader follows O012-TERM-0314."),
    "correction:o012-u027-resolved-term-002": (
        "terminology_correction", "unit-027-lecture-027.md pre-admission draft; UNIT027-TERM-P3-002",
        ["s01", "def-002"],
        "The draft used the recognized but nonpreferred funktorial form.",
        "Normalize to fungtorial before admission.",
        "The final reader follows the preferred fungtor/fungtorialitas family."),
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
    spec = importlib.util.spec_from_file_location("o012_generic_u027_producer", path)
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
            raise SystemExit(f"{name}: immutable Units 001-026 prefix mismatch")
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
        raise SystemExit("Units 001-026 backend bundle identity mismatch")
    if not {"unit:o012-rbt-u026", PRIOR_RIGHTS,
            "artifact:o012-u026-independent-review"} <= seen:
        raise SystemExit("Unit 26 prefix closure is incomplete")
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
        raise SystemExit("Unit 27 upstream span mismatch")
    if ("\\lecturenum{27}" not in lines[5823]
            or lines[5922].strip() != ""
            or "\\lecturenum{28}" not in lines[5923]):
        raise SystemExit("Unit 27 source boundary identity mismatch")


def structural_spans(lines: list[str]) -> dict[str, tuple[int, int, str]]:
    opening = re.compile(r"^\s*:::\s+\{[^#}]*#(o012-rbt-l27(?:-[A-Za-z0-9-]+)?)(.*)\}\s*$")
    heading = re.compile(r"^#{1,6}\s+.*\{[^}]*#(o012-rbt-l27(?:-[A-Za-z0-9-]+)?)[^}]*\}\s*$")
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
                raise SystemExit(f"unexpected div close at reader line {number}")
            ident, start, opener = stack.pop()
            if ident in spans:
                raise SystemExit(f"duplicate fenced anchor: {ident}")
            spans[ident] = (start, number, opener)
    if stack:
        raise SystemExit(f"unclosed div anchors: {[item[0] for item in stack]}")
    headings = {
        "o012-rbt-l27-notice": (12, 53), "o012-rbt-l27": (54, 841),
        "o012-rbt-l27-s01": (56, 357), "o012-rbt-l27-s02": (358, 614),
        "o012-rbt-l27-s03": (615, 744), "o012-rbt-l27-s04": (745, 841),
        "o012-rbt-l27-mastery": (842, 1168),
    }
    for ident, (start, end) in headings.items():
        if ident not in lines[start - 1]:
            raise SystemExit(f"heading span identity mismatch: {ident}")
        spans[ident] = (start, end, lines[start - 1])
    if tuple(ordered) != EXPECTED_ANCHORS or set(spans) != set(EXPECTED_ANCHORS):
        raise SystemExit("Unit 27 stable-ID inventory/order mismatch")
    return spans


def unit_kind(ident: str, opener: str) -> str:
    if ident.endswith("-notice"):
        return "notice"
    if ident == "o012-rbt-l27":
        return "lecture"
    if ident.endswith("-mastery"):
        return "mastery_section"
    if re.fullmatch(r"o012-rbt-l27-s\d{2}", ident):
        return "section"
    match = re.search(r"\{\.([A-Za-z][A-Za-z0-9_-]*)", opener)
    kind = (match.group(1).replace("source-audit", "source_audit")
            .replace("source-margin", "source_margin") if match else "")
    allowed = {"boundary", "definition", "equation", "example", "exercise",
               "figure", "hint", "lemma", "proof", "proposition", "solution",
               "source_audit", "source_margin", "theorem"}
    if kind not in allowed:
        raise SystemExit(f"cannot infer kind for {ident}: {kind!r}")
    return kind


def provenance(ident: str, kind: str, opener: str) -> tuple[str, str, bool]:
    if (kind in {"notice", "source_audit", "mastery_section", "boundary",
                 "hint", "solution"}
            or 'data-origin="edition-' in opener
            or ("-mcheck-" in ident and 'data-origin="source-' not in opener)):
        return "edition_original", COMPANION_RIGHTS, True
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
    return f"Unit 27 {kind} {ident.rsplit('-', 1)[-1]}"


def verify_evidence() -> dict[str, Any]:
    for _ident, (relative, size, expected_sha, _media, _state, _qas) in EVIDENCE.items():
        raw = (LANE / relative).read_bytes()
        if len(raw) != size or digest(raw) != expected_sha:
            raise SystemExit(f"Unit 27 evidence identity mismatch: {relative}")
    qa = json.loads(QA_JSON.read_text(encoding="utf-8"))
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
            or qa.get("unit", {}).get("stable_ids") != 46
            or qa.get("unit", {}).get("fenced_semantic_objects") != 39
            or qa.get("proof_closure", {}).get("mastery_solution_triples") != 6
            or qa.get("model_provenance") != MODEL):
        raise SystemExit("Unit 27 QA content/binding mismatch")
    expected = {"UNIT027-MATH-P2-001", "UNIT027-A11Y-P2-002",
                "UNIT027-PROOF-P2-003", "UNIT027-TERM-P3-001",
                "UNIT027-TERM-P3-002"}
    if (not isinstance(resolved, list)
            or {item.get("finding_id") for item in resolved} != expected
            or any(item.get("status") != "RESOLVED_BEFORE_ADMISSION" for item in resolved)):
        raise SystemExit("Unit 27 resolved-finding closure mismatch")
    if any(item.get("status") != "PASS" for item in qa.get("checks", [])):
        raise SystemExit("Unit 27 QA contains a non-passing check")
    return qa


def main() -> int:
    tables, prefix_raw = load_prefix()
    verify_upstream()
    qa_doc = verify_evidence()
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
        raise SystemExit("Unit 27 reader identity/newline mismatch")
    raw_lines = raw.splitlines(keepends=True)
    lines = [line.decode("utf-8").rstrip("\n") for line in raw_lines]
    text = raw.decode("utf-8")
    if (len(lines) != SOURCE_LINES or text.count(MODEL) != 1
            or re.search(r"\bfunktorial\b|\bperpanjang\w*\b", text, re.IGNORECASE)):
        raise SystemExit("Unit 27 reader line/provenance/terminology mismatch")
    spans = structural_spans(lines)

    for slug, (source_term, _preferred, _evidence, domain) in NEW_TERMS.items():
        concept = common("concept", f"concept:{slug}")
        concept.update({"canonical_label": source_term, "domain": domain,
                        "locale_neutral": True})
        add("concepts.jsonl", concept)
    concept_ids = list(REUSED_CONCEPTS) + [f"concept:{slug}" for slug in NEW_TERMS]
    if any(ident not in existing_ids and ident not in additions["concepts.jsonl"]
           for ident in concept_ids):
        raise SystemExit("Unit 27 concept closure mismatch")

    rights_specs = (
        (COMPANION_RIGHTS,
         "Indonesian original solutions, mastery, proof-completion, source-audit, and accessibility layer for Roberts Unit 27.",
         "Original additions are CC BY 4.0; source-derived material remains separately attributed.",
         [ROOT], None),
        (COMPOSITE_RIGHTS,
         "David Michael Roberts source adaptation plus original Indonesian Unit 27 companions.",
         "Translated, repaired, and original layers remain component-distinguishable.",
         [ROOT], None),
        (CUMULATIVE_RIGHTS,
         "Cumulative Roberts Units 001-027 Indonesian reader source boundary.",
         "Append-only semantic pointer; verified prior build artifacts remain immutable until separate build admission.",
         [f"unit:o012-rbt-u{number:03d}" for number in range(1, 28)], PRIOR_RIGHTS),
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

    section_ranges = (("o012-rbt-l27-s01", 56, 357),
                      ("o012-rbt-l27-s02", 358, 614),
                      ("o012-rbt-l27-s03", 615, 744),
                      ("o012-rbt-l27-s04", 745, 841))
    section_ids = {item[0] for item in section_ranges}

    def parent_local(ident: str, start: int) -> str:
        if ident in {"o012-rbt-l27-notice", "o012-rbt-l27",
                     "o012-rbt-l27-mastery", "o012-rbt-l27-boundary-001"}:
            return ROOT
        if ident in section_ids:
            return LECTURE
        if any(token in ident for token in ("-mcheck-", "-hint-", "-sol-")):
            if ident.endswith("-001") and start < 842:
                return "unit:o012-rbt-l27-s01"
            return MASTERY
        for section, low, high in section_ranges:
            if low <= start <= high:
                return f"unit:{section}"
        raise SystemExit(f"cannot assign Unit 27 parent: {ident}")

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
        "display_title": "Topologi Aljabar - Unit 27: Kohomologi Tereduksi, Korantai Kecil, dan Mayer--Vietoris",
        "edition_id": EDITION, "edition_unit_id": ROOT, "locale": "id-ID",
        "model_provenance": MODEL, "order": 27, "parent_id": COURSE,
        "path": [ROOT], "program_id": PROGRAM,
        "provenance_relation": "composite_translated_and_original",
        "resource_id": RESOURCE, "rights_component_id": COMPOSITE_RIGHTS,
        "source_local_id": None,
        "source_locator": {"commit_sha": COMMIT, "line_end": UPSTREAM_END,
                           "line_start": UPSTREAM_START, "path": "Notes.tex",
                           "precision": "exact_unit_span", "span_bytes": UPSTREAM_SPAN_BYTES,
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
        shared = {"component_source_commit": COMMIT, "component_source_id": RESOURCE,
                  "course_route_unit_id": ROUTE, "edition_unit_id": ROOT,
                  "model_provenance": MODEL}
        unit = common("unit", unit_id); unit.update(shared)
        unit.update({"concept_ids": concept_ids, "course_id": COURSE,
                     "display_title": display_title(ident, lines, start, kind),
                     "edition_id": EDITION, "locale": "id-ID",
                     "order": order_map[parent_id][ident], "parent_id": parent_id,
                     "path": path, "program_id": PROGRAM,
                     "provenance_relation": provenance_value,
                     "resource_id": RESOURCE, "rights_component_id": rights_id,
                     "source_local_id": ident, "target_locator": locator,
                     "translation_state": "structurally_verified", "unit_kind": kind})
        segment = common("segment", f"segment:{ident}"); segment.update(shared)
        segment.update({"concept_ids": concept_ids, "edition_id": EDITION,
                        "locale": "id-ID", "order": unit["order"],
                        "provenance_relation": provenance_value,
                        "resource_id": RESOURCE, "rights_component_id": rights_id,
                        "segment_kind": kind, "source_local_id": ident,
                        "source_locator": source_locator(edition_original),
                        "target_locator": locator,
                        "translation_state": "structurally_verified", "unit_id": unit_id})
        aliases = re.findall(r'data-source-label="([^"]+)"', opener)
        if aliases:
            unit["source_aliases"] = aliases; segment["source_aliases"] = aliases
        formats = re.findall(r'data-source-format="([^"]+)"', opener)
        if formats:
            unit["source_formats"] = formats; segment["source_formats"] = formats
            unit["accessibility_status"] = "semantic_reflow"
            segment["accessibility_status"] = "semantic_reflow"
        if ident == "o012-rbt-l27-boundary-001":
            unit["next_source_line"] = NEXT_SOURCE_LINE
            segment["next_source_line"] = NEXT_SOURCE_LINE
        if kind == "proof":
            unit["proof_status"] = "complete_original_proof"
            segment["proof_status"] = "complete_original_proof"
        if kind == "solution":
            unit["solution_status"] = "complete_checked_solution"
            segment["solution_status"] = "complete_checked_solution"
        add("units.jsonl", unit); add("segments.jsonl", segment)

    asset = common("asset", "asset:o012-u027-source-markdown")
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
                     "rejected_forms": [], "rights_component_id": COMPOSITE_RIGHTS,
                     "scope_unit_id": ROOT, "source_term": source_term,
                     "terminology_status": "unit_attested_reviewed",
                     "usage_note": "Attested in the independently reviewed Unit 27 reader; no global terminology control file was changed by this append.",
                     "variants": []})
        add("terms.jsonl", term)

    for ident, (correction_type, evidence, suffixes, defect, change, rationale) in CORRECTIONS.items():
        targets = [f"unit:o012-rbt-l27-{suffix}" for suffix in suffixes]
        if any(target.removeprefix("unit:") not in spans for target in targets):
            raise SystemExit(f"correction target absent: {ident}")
        correction = common("correction", ident)
        correction.update({"affected_unit_ids": targets,
                           "correction_type": correction_type, "edition_id": EDITION,
                           "evidence": evidence,
                           "evidence_segment_id": "segment:o012-rbt-l27-notice",
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
                         "toolchain": (f"Bounded Unit 27 evidence; Notes.tex:5824-5923 "
                                       f"span {UPSTREAM_SPAN_SHA}; {MODEL}; route {ROUTE}; "
                                       "no cumulative build/publication assertion."),
                         "translation_state": state, "unit_id": ROOT})
        add("artifacts.jsonl", artifact)

    qa_specs = (
        ("qa:o012-u027-source-integrity", "source",
         "Unit 27 authority and reader identities, 46 stable IDs, all aliases, source census, and native-MathML structure passed.",
         ["artifact:o012-u027-source-audit", "artifact:o012-u027-qa"]),
        ("qa:o012-u027-math", "math",
         "Independent Unit 27 mathematical review passed with no open P1, P2, or P3 finding and complete small-chain and Mayer--Vietoris proofs.",
         ["artifact:o012-u027-independent-review"]),
        ("qa:o012-u027-language", "language",
         "Independent Indonesian review passed after five P2/P3 findings were resolved before admission.",
         ["artifact:o012-u027-independent-review", "artifact:o012-u027-qa"]),
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
        item.update(extra); add("relations.jsonl", item)

    relation("relation:adapts:o012-rbt-u027:edition", ROOT, "adapts", EDITION,
             "Unit 27 is the Indonesian adapted reader boundary for the frozen Roberts edition.")
    relation("relation:precedes:o012-rbt-u026:o012-rbt-u027",
             "unit:o012-rbt-u026", "precedes", ROOT,
             "Preserves contiguous Roberts lecture-unit order.")
    relation("relation:precedes:o012-rbt-l27:mastery", LECTURE, "precedes", MASTERY,
             "Lecture content precedes the five edition-original advanced mastery items; the first solved source exercise remains in source order.")
    relation("relation:boundary:o012-u027", CUMULATIVE_RIGHTS, "contains", ROOT,
             "Additive cumulative Units 001-027 semantic source boundary.")
    relation("relation:route:d60-r13:o012-rbt-u027", COURSE, "contains", ROOT,
             "Roberts Lecture 27 remains an edition unit in the non-destructive D60-R13 route view.",
             course_route_unit_id=ROUTE, edition_unit_id=ROOT)
    relation("relation:depends-on:o012-rbt-l27-prop-001:eq-001",
             "unit:o012-rbt-l27-prop-001", "depends-on",
             "unit:o012-rbt-l27-eq-001",
             "The small-chain theorem uses the corrected difference-of-restrictions cochain model.")
    relation("relation:depends-on:o012-rbt-l27-thm-001:prop-001",
             "unit:o012-rbt-l27-thm-001", "depends-on",
             "unit:o012-rbt-l27-prop-001",
             "Mayer--Vietoris uses the small-chain comparison quasi-isomorphism.")
    relation("relation:depends-on:o012-rbt-l27-exa-003:thm-001",
             "unit:o012-rbt-l27-exa-003", "depends-on",
             "unit:o012-rbt-l27-thm-001",
             "The sphere computation applies the Mayer--Vietoris long exact sequence.")
    relation("relation:xref:o012-rbt-l27-mcheck-005:exa-002",
             "unit:o012-rbt-l27-mcheck-005", "xref",
             "unit:o012-rbt-l27-exa-002",
             "The circle exercise uses the zero-sphere reduced-cohomology base case.")
    proof_targets = {1: "unit:o012-rbt-l27-lem-001",
                     2: "unit:o012-rbt-l27-prop-001",
                     3: "unit:o012-rbt-l27-thm-001"}
    for number, target in proof_targets.items():
        relation(f"relation:proves:o012-rbt-l27-proof-{number:03d}:closure",
                 f"unit:o012-rbt-l27-proof-{number:03d}", "proves", target,
                 f"Complete proof closure {number} for Unit 27.")
    for number in range(1, 7):
        relation(f"relation:solves:l27-sol-{number:03d}:l27-mcheck-{number:03d}",
                 f"unit:o012-rbt-l27-sol-{number:03d}", "solves",
                 f"unit:o012-rbt-l27-mcheck-{number:03d}",
                 f"Complete checked solution for Unit 27 mastery check {number}.")
        relation(f"relation:hints:l27-hint-{number:03d}:l27-mcheck-{number:03d}",
                 f"unit:o012-rbt-l27-hint-{number:03d}", "hints",
                 f"unit:o012-rbt-l27-mcheck-{number:03d}",
                 f"Bounded hint for Unit 27 mastery check {number}.")

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
        unit = by_id[f"unit:{ident}"]; segment = by_id[f"segment:{ident}"]
        if unit["target_locator"] != segment["target_locator"]:
            raise SystemExit(f"unit/segment locator mismatch: {ident}")
        if unit["path"][-1] != unit["id"]:
            raise SystemExit(f"noncanonical Unit 27 path: {ident}")
        if unit["parent_id"].startswith("unit:") and unit["path"][:-1] != by_id[unit["parent_id"]]["path"]:
            raise SystemExit(f"Unit 27 parent path mismatch: {ident}")
        for obj in (unit, segment):
            if (obj["edition_unit_id"] != ROOT or obj["course_route_unit_id"] != ROUTE
                    or obj["model_provenance"] != MODEL):
                raise SystemExit(f"Unit 27 route/provenance mismatch: {ident}")
    sibling_orders: defaultdict[str, list[int]] = defaultdict(list)
    for obj in additions["units.jsonl"].values():
        sibling_orders[obj["parent_id"]].append(obj["order"])
    if any(len(values) != len(set(values)) for values in sibling_orders.values()):
        raise SystemExit("duplicate Unit 27 sibling order")
    for number in range(1, 7):
        check = f"unit:o012-rbt-l27-mcheck-{number:03d}"
        solves = [obj for obj in additions["relations.jsonl"].values()
                  if obj["relation_type"] == "solves" and obj["to_id"] == check]
        hints = [obj for obj in additions["relations.jsonl"].values()
                 if obj["relation_type"] == "hints" and obj["to_id"] == check]
        if len(solves) != 1 or len(hints) != 1:
            raise SystemExit(f"Unit 27 mastery closure mismatch: {number}")
    if len([obj for obj in additions["units.jsonl"].values()
            if obj.get("proof_status")]) != 3:
        raise SystemExit("Unit 27 three-proof closure mismatch")
    if len(additions["corrections.jsonl"]) != 16:
        raise SystemExit("Unit 27 correction dossier mismatch")
    if additions["rights.jsonl"][CUMULATIVE_RIGHTS]["component_scope"] != [
            f"unit:o012-rbt-u{number:03d}" for number in range(1, 28)]:
        raise SystemExit("Unit 27 cumulative rights scope mismatch")
    if by_id["unit:o012-rbt-l27-boundary-001"].get("next_source_line") != NEXT_SOURCE_LINE:
        raise SystemExit("Unit 27 terminal cursor mismatch")
    aliases = {alias: unit["id"] for unit in additions["units.jsonl"].values()
               for alias in unit.get("source_aliases", [])}
    if aliases != {
            "eg:reduced_cohom_S0": "unit:o012-rbt-l27-exa-002",
            "eq:restr_to_intersection": "unit:o012-rbt-l27-eq-001",
            "thm:mayer-vietoris": "unit:o012-rbt-l27-thm-001",
            "eq:sphere_cohomol_reduction": "unit:o012-rbt-l27-eq-002"}:
        raise SystemExit("Unit 27 source-label alias closure mismatch")
    if {item.get("finding_id") for item in qa_doc["resolved_findings"]} != {
            "UNIT027-MATH-P2-001", "UNIT027-A11Y-P2-002",
            "UNIT027-PROOF-P2-003", "UNIT027-TERM-P3-001",
            "UNIT027-TERM-P3-002"}:
        raise SystemExit("Unit 27 pre-admission finding set changed")

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
    print("Unit 027 semantic backend extension: PASS")
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
    print("stable_ids=46")
    print("proof_closures=3")
    print("mastery_triples=6")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
