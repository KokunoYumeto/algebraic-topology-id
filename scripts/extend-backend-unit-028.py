#!/usr/bin/env python3
"""Fail-closed append-only semantic-backend admission for Roberts Unit 028.

The complete 4,264-record Units 001--027 semantic backend is immutable. This
transaction verifies that exact byte prefix plus the final Unit 28 authority,
reader, audit, independent review, and QA witnesses, then appends only the
Unit 28 semantic slice. It does not mutate reader or build artifacts.
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
SOURCE = LANE / "source/id-ID/units/unit-028-lecture-028.md"
UPSTREAM = (LANE / "authority/upstream" /
            "AlgebraicTopology2019-b947ad2e9f9e301bfe24590a9db653bc54fa1a53" /
            "Notes.tex")
AUDIT = LANE / "qa/UNIT_028_SOURCE_AUDIT.md"
REVIEW = LANE / "qa/UNIT_028_INDEPENDENT_REVIEW.md"
QA_JSON = LANE / "qa/UNIT_028_QA.json"

SCHEMA = "curriculum.interop"
VERSION = "0.1.0"
WORKFLOW = "o012-d60-id-reader-production"
STAMP = "2026-08-24T00:00:00Z"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"
PROGRAM = "program:o012-id"
COURSE = "course:o012-d60"
ROUTE = "D60-R14"
RESOURCE = "resource:roberts-algebraic-topology-2019"
EDITION = "edition:roberts-at-2019-b947ad2"
COMMIT = "b947ad2e9f9e301bfe24590a9db653bc54fa1a53"
ROBERTS_RIGHTS = "rights:roberts-cc-by-4.0"
COMPANION_RIGHTS = "rights:o012-u028-companion-cc-by-4.0"
COMPOSITE_RIGHTS = "rights:o012-u028-composite-cc-by-4.0"
CUMULATIVE_RIGHTS = "rights:o012-units-001-028-composite-cc-by-4.0"
PRIOR_RIGHTS = "rights:o012-units-001-027-composite-cc-by-4.0"
ROOT = "unit:o012-rbt-u028"
LECTURE = "unit:o012-rbt-l28"
MASTERY = "unit:o012-rbt-l28-mastery"
SOURCE_PATH = "source/id-ID/units/unit-028-lecture-028.md"
SOURCE_BYTES = 26072
SOURCE_LINES = 814
SOURCE_SHA = "b69036f5a0a8151942288f04197a9dc69c81d2902fe8a15a0e73601978fefe67"
UPSTREAM_BYTES = 331447
UPSTREAM_LINES = 6368
UPSTREAM_SHA = "cfe93e9dbe3e25bd96f711f59e6078ab97527682b58e1f8ad127f74357f665d7"
UPSTREAM_START = 5924
UPSTREAM_END = 6052
UPSTREAM_SPAN_BYTES = 8257
UPSTREAM_SPAN_SHA = "f3e4a526fa2e504a449a606150c399520c255a98a91d60c934737f87497b4b51"
NEXT_SOURCE_LINE = 6053

FILES = ("artifacts.jsonl", "assets.jsonl", "authority.jsonl", "concepts.jsonl",
         "corrections.jsonl", "qa.jsonl", "relations.jsonl", "rights.jsonl",
         "segments.jsonl", "terms.jsonl", "units.jsonl")
PREFIX = {
    "artifacts.jsonl": (151, 120648, "c16f1deaa3844a19ece5c112a4a556b6a31c1fe6a8065f1773aa123bdd0f5311"),
    "assets.jsonl": (29, 17911, "260fbded514ca70a5b54866bfc2b26cc770612876984cc81aae47516b8592449"),
    "authority.jsonl": (4, 2721, "f21af26912520ab34b38dff0e927ed46a546dbe5d318da0dc133e58330d0e368"),
    "concepts.jsonl": (341, 107533, "bf5b7bd06811e74e9d5139dfec4903e8f3429a98939fa106e45a3def519db473"),
    "corrections.jsonl": (361, 354746, "ffa733a7ac19745aa9d4ef67c98911e011a2ebc51e4353fa40fc1b337b9c0023"),
    "qa.jsonl": (125, 70471, "fc02b08c7ec19dba9654db5aa9d2bd2cfe9b855a222d5764a06fc93bffc2d319"),
    "relations.jsonl": (449, 183555, "e8a0831badaebbe47523f92ac1949f2266f544ad3baede0f35967d1764e959bf"),
    "rights.jsonl": (77, 71149, "5f4a0f6de1866c04f0d56d7f7ed508f4c41364c9626d357e94e6f4a135002767"),
    "segments.jsonl": (1183, 1643547, "2c0dacca32d6e92257c43b2d5c270ede72e257ff5d1dfde8b54e5858e9ac4602"),
    "terms.jsonl": (334, 209753, "c25a3834bed5b9a57624aae9c1d546a24ad08b4ae397e92e8a8e5f6b3d357735"),
    "units.jsonl": (1210, 1750960, "936f41c32c69ba73881038e39b9e33bb4baab39ac9dd5ad56409c370309eeda0"),
}
PREFIX_RECORDS = 4264
PREFIX_BYTES = 4532994
PREFIX_BUNDLE = "09aa16e8d9387171445c4d465d00a5399e39517a210cb347e30d2d285c703f8c"

EVIDENCE = {
    "artifact:o012-u028-source-audit": (
        "qa/UNIT_028_SOURCE_AUDIT.md", 5660,
        "2b181bcd12c95210395b3aec8b866b69093d6636b89773d08d93cec41870fa4a",
        "text/markdown; charset=utf-8", "source_frozen",
        ["qa:o012-u028-source-integrity"]),
    "artifact:o012-u028-independent-review": (
        "qa/UNIT_028_INDEPENDENT_REVIEW.md", 6807,
        "92d81718580eded1daac0593fe2e13d7797c9ed2d8507e70fe5f7dd522fde505",
        "text/markdown; charset=utf-8", "mathematically_reviewed",
        ["qa:o012-u028-math", "qa:o012-u028-language"]),
    "artifact:o012-u028-qa": (
        "qa/UNIT_028_QA.json", 9792,
        "dd448f5d5d1a60f6b8e5815a1cb993946c7400f55b46d287f25a78d59f068c79",
        "application/json", "built",
        ["qa:o012-u028-source-integrity", "qa:o012-u028-language"]),
}

EXPECTED_ANCHORS = (
    "o012-rbt-l28-notice", "o012-rbt-l28", "o012-rbt-l28-s01",
    "o012-rbt-l28-aside-001", "o012-rbt-l28-aside-002",
    "o012-rbt-l28-prop-001", "o012-rbt-l28-s02",
    "o012-rbt-l28-aside-003", "o012-rbt-l28-prop-002",
    "o012-rbt-l28-proof-001", "o012-rbt-l28-audit-001",
    "o012-rbt-l28-s03", "o012-rbt-l28-thm-001",
    "o012-rbt-l28-thm-002", "o012-rbt-l28-proof-002",
    "o012-rbt-l28-audit-002", "o012-rbt-l28-cor-001",
    "o012-rbt-l28-proof-003", "o012-rbt-l28-s04",
    "o012-rbt-l28-def-001", "o012-rbt-l28-audit-003",
    "o012-rbt-l28-prop-003", "o012-rbt-l28-proof-004",
    "o012-rbt-l28-audit-004", "o012-rbt-l28-exa-001",
    "o012-rbt-l28-s05", "o012-rbt-l28-audit-005",
    "o012-rbt-l28-mastery", "o012-rbt-l28-mcheck-001",
    "o012-rbt-l28-hint-001", "o012-rbt-l28-sol-001",
    "o012-rbt-l28-mcheck-002", "o012-rbt-l28-hint-002",
    "o012-rbt-l28-sol-002", "o012-rbt-l28-mcheck-003",
    "o012-rbt-l28-hint-003", "o012-rbt-l28-sol-003",
    "o012-rbt-l28-mcheck-004", "o012-rbt-l28-hint-004",
    "o012-rbt-l28-sol-004", "o012-rbt-l28-mcheck-005",
    "o012-rbt-l28-hint-005", "o012-rbt-l28-sol-005",
    "o012-rbt-l28-mcheck-006", "o012-rbt-l28-hint-006",
    "o012-rbt-l28-sol-006", "o012-rbt-l28-boundary-001",
)

SOURCE_RANGES = {
    "o012-rbt-l28": (5924, 6052),
    "o012-rbt-l28-s01": (5924, 5947),
    "o012-rbt-l28-aside-001": (5924, 5924),
    "o012-rbt-l28-aside-002": (5927, 5927),
    "o012-rbt-l28-prop-001": (5939, 5947),
    "o012-rbt-l28-s02": (5949, 5958),
    "o012-rbt-l28-aside-003": (5949, 5949),
    "o012-rbt-l28-prop-002": (5951, 5953),
    "o012-rbt-l28-proof-001": (5955, 5957),
    "o012-rbt-l28-s03": (5959, 5997),
    "o012-rbt-l28-thm-001": (5961, 5967),
    "o012-rbt-l28-thm-002": (5973, 5979),
    "o012-rbt-l28-cor-001": (5987, 5992),
    "o012-rbt-l28-proof-003": (5994, 5996),
    "o012-rbt-l28-s04": (5998, 6042),
    "o012-rbt-l28-def-001": (6009, 6011),
    "o012-rbt-l28-prop-003": (6025, 6031),
    "o012-rbt-l28-exa-001": (6033, 6041),
    "o012-rbt-l28-s05": (6043, 6052),
}

NEW_TERMS = {
    "excision": ("excision", "eksisi", "o012-rbt-l28-thm-001", "algebraic_topology"),
    "cohomological-dimension-invariance": ("cohomological dimension invariance", "invariansi dimensi melalui kohomologi", "o012-rbt-l28-prop-002", "algebraic_topology"),
    "relative-cohomology-quotient-isomorphism": ("relative-cohomology quotient isomorphism", "isomorfisma kohomologi relatif--hasil bagi", "o012-rbt-l28-thm-002", "algebraic_topology"),
    "infinite-wedge-cohomology": ("infinite-wedge cohomology", "kohomologi baji tak berhingga", "o012-rbt-l28-prop-003", "algebraic_topology"),
    "singular-simplicial-cochain-comparison": ("singular--simplicial cochain comparison", "pembandingan korantai singular--simpleksial", "o012-rbt-l28-s05", "algebraic_topology"),
    "well-pointed-space": ("well-pointed space", "ruang bertitik dasar baik", "o012-rbt-l28-prop-003", "algebraic_topology"),
}

REUSED_CONCEPTS = (
    "concept:sphere-cohomology", "concept:reduced-cohomology",
    "concept:relative-cohomology", "concept:quotient-space",
    "concept:quotient-map", "concept:wedge-sum", "concept:k-skeleton",
    "concept:delta-set", "concept:unit-sphere", "concept:cochain-map",
    "concept:singular-cochain-complex", "concept:simplicial-cochain-complex",
    "concept:homotopy-equivalence", "concept:contractible-space",
    "concept:long-exact-sequence", "concept:coproduct-preservation",
)

CORRECTIONS = {
    "correction:o012-u028-dossier-001": (
        "structural_adaptation", "Notes.tex:5924-5937",
        ["s01", "prop-001"],
        "Lecture 28 begins inside an example opened in Lecture 27.",
        "Mark the continuation explicitly and preserve both reduction cases and the source example close.",
        "The cross-unit example remains contiguous and comprehensible."),
    "correction:o012-u028-dossier-002": (
        "mathematical_correction", "Notes.tex:5927,5951-5956",
        ["s01", "prop-002", "proof-001", "audit-001"],
        "Detection by a nonzero copy of R is asserted without excluding the zero coefficient ring, and dimension zero is omitted.",
        "State nonzero coefficients for detection and close the zero-dimensional case separately.",
        "Every detection argument is valid for its stated coefficient choice."),
    "correction:o012-u028-dossier-003": (
        "direction_preservation", "Notes.tex:5961-5967",
        ["thm-001"],
        "The source excision arrow is contravariant and must not be reversed during adaptation.",
        "Preserve j-star from H^k(X,A) to H^k(X minus Z,A minus Z).",
        "The induced cohomology map follows the space inclusion contravariantly."),
    "correction:o012-u028-dossier-004": (
        "mathematical_correction", "Notes.tex:5973-5979",
        ["thm-002", "audit-002"],
        "The source labels the forward relative-to-quotient isomorphism as induced by the quotient map.",
        "Write q-star in the contravariant quotient-to-relative direction and reserve the reverse arrow for its inverse.",
        "The map direction now agrees with cohomological contravariance."),
    "correction:o012-u028-dossier-005": (
        "proof_completion", "Notes.tex:5981-5983",
        ["thm-002", "proof-002", "audit-002"],
        "The source replaces the quotient theorem proof with a one-line external Hatcher reference.",
        "Supply the neighborhood, triple LES, two excisions, complement homeomorphism, contraction, and naturality proof.",
        "The theorem is independently learnable and its induced direction is justified."),
    "correction:o012-u028-dossier-006": (
        "mathematical_correction", "Notes.tex:6004-6013",
        ["def-001", "audit-003"],
        "The source calls the quotient denoted by a vee a join.",
        "Use baji (wedge sum), preserving the displayed quotient construction.",
        "The terminology now names the actual topological construction."),
    "correction:o012-u028-dossier-007": (
        "hypothesis_repair", "Notes.tex:6025-6031",
        ["prop-003", "proof-004", "audit-004"],
        "The arbitrary infinite-family claim omits the quotient theorem hypotheses used in its proof.",
        "Require a nonempty index set and closed basepoints that deformation retract from open neighborhoods.",
        "The coproduct pair satisfies the quotient theorem and covers the intended CW applications."),
    "correction:o012-u028-dossier-008": (
        "mathematical_correction", "Notes.tex:6025-6029",
        ["prop-003"],
        "The left side of the wedge formula omits its coefficient ring.",
        "Restore the coefficient R on both sides.",
        "The isomorphism has one consistent coefficient system."),
    "correction:o012-u028-dossier-009": (
        "mathematical_correction", "Notes.tex:6043-6050",
        ["s05", "audit-005"],
        "The source reverses the cochain map induced by inclusion of distinguished simplices.",
        "Define restriction from singular cochains to Delta-set cochains and prove differential compatibility.",
        "Precomposition now has the unique canonical direction."),
    "correction:o012-u028-dossier-010": (
        "mathematical_correction", "Notes.tex:5969 (margin)",
        ["thm-002", "audit-002"],
        "The source identifies X minus the empty set with X plus a disjoint basepoint.",
        "Replace it by the pointed quotient convention X/emptyset equals X-plus.",
        "Set difference and quotient notation are no longer conflated."),
    "correction:o012-u028-dossier-011": (
        "clarification", "Notes.tex:5969,5985,6022",
        ["s03", "s04"],
        "Local typos and malformed skeleton notation obscure otherwise unchanged content.",
        "Normalize prose and restore the intended skeleton expression.",
        "The translation preserves the mathematics without inherited typographic defects."),
    "correction:o012-u028-resolved-math-p2-001": (
        "hypothesis_repair", "UNIT028-MATH-P2-001",
        ["prop-003", "proof-004", "audit-004"],
        "The pre-admission wedge statement lacked nonemptiness and closed-basepoint hypotheses.",
        "Add the exact hypotheses and prove the quotient theorem applies to the coproduct pair.",
        "The independently reviewed final statement is valid."),
    "correction:o012-u028-resolved-audit-p3-001": (
        "audit_correction", "UNIT028-AUDIT-P3-001",
        ["audit-002"],
        "The reader repair of the impossible empty-set convention was absent from the source audit.",
        "Record the source form and the X/emptyset equals X-plus repair on both audit surfaces.",
        "The semantic correction is now provenance-visible."),
    "correction:o012-u028-resolved-prov-p3-002": (
        "provenance_correction", "UNIT028-PROV-P3-002",
        ["s03", "proof-002"],
        "The audit conflated no TeX cite command with no bibliographic reference and omitted Hatcher A.4 from the reader.",
        "Distinguish command census from two textual references and restore Proposition A.4 in reading order.",
        "Both source references are preserved accurately."),
    "correction:o012-u028-resolved-math-p3-003": (
        "mathematical_correction", "UNIT028-MATH-P3-003",
        ["s01", "prop-002", "proof-001"],
        "A sphere-detection claim preceded an explicit nonzero coefficient choice.",
        "Separate the all-ring formula from every detection argument and choose nonzero R for the latter.",
        "The zero ring is no longer asked to distinguish dimensions."),
    "correction:o012-u028-resolved-term-p3-004": (
        "terminology_correction", "UNIT028-TERM-P3-004",
        ["s01", "exa-001"],
        "The pre-admission draft used bola for sphere referents S-to-the-n.",
        "Normalize sphere referents to sfera while reserving bola for genuine balls.",
        "The final reader follows the admitted lane distinction."),
    "correction:o012-u028-resolved-term-p3-005": (
        "terminology_correction", "UNIT028-TERM-P3-005",
        ["sol-001"],
        "One pre-admission sentence retained the nonpreferred funktor spelling.",
        "Normalize it to the admitted preferred form fungtor.",
        "The final reader follows O012-TERM-0004."),
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
    spec = importlib.util.spec_from_file_location("o012_generic_u028_producer", path)
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
            raise SystemExit(f"{name}: immutable Units 001-027 prefix mismatch")
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
        raise SystemExit("Units 001-027 backend bundle identity mismatch")
    if not {"unit:o012-rbt-u027", PRIOR_RIGHTS,
            "artifact:o012-u027-independent-review"} <= seen:
        raise SystemExit("Unit 27 prefix closure is incomplete")
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
        raise SystemExit("Unit 28 upstream span mismatch")
    if ("\\lecturenum{28}" not in lines[5923]
            or lines[6051].strip() != ""
            or "\\lecturenum{29}" not in lines[6052]):
        raise SystemExit("Unit 28 source boundary identity mismatch")


def structural_spans(lines: list[str]) -> dict[str, tuple[int, int, str]]:
    opening = re.compile(r"^\s*:::\s+\{[^#}]*#(o012-rbt-l28(?:-[A-Za-z0-9-]+)?)(.*)\}\s*$")
    heading = re.compile(r"^#{1,6}\s+.*\{[^}]*#(o012-rbt-l28(?:-[A-Za-z0-9-]+)?)[^}]*\}\s*$")
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
        "o012-rbt-l28-notice": (12, 52), "o012-rbt-l28": (53, 572),
        "o012-rbt-l28-s01": (55, 140), "o012-rbt-l28-s02": (141, 207),
        "o012-rbt-l28-s03": (208, 357), "o012-rbt-l28-s04": (358, 507),
        "o012-rbt-l28-s05": (508, 572), "o012-rbt-l28-mastery": (573, 806),
    }
    for ident, (start, end) in headings.items():
        if ident not in lines[start - 1]:
            raise SystemExit(f"heading span identity mismatch: {ident}")
        spans[ident] = (start, end, lines[start - 1])
    if tuple(ordered) != EXPECTED_ANCHORS or set(spans) != set(EXPECTED_ANCHORS):
        raise SystemExit("Unit 28 stable-ID inventory/order mismatch")
    return spans


def unit_kind(ident: str, opener: str) -> str:
    if ident.endswith("-notice"):
        return "notice"
    if ident == "o012-rbt-l28":
        return "lecture"
    if ident.endswith("-mastery"):
        return "mastery_section"
    if re.fullmatch(r"o012-rbt-l28-s\d{2}", ident):
        return "section"
    match = re.search(r"\{\.([A-Za-z][A-Za-z0-9_-]*)", opener)
    kind = match.group(1).replace("source-audit", "source_audit") if match else ""
    allowed = {"aside", "boundary", "corollary", "definition", "example",
               "exercise", "hint", "proof", "proposition", "solution",
               "source_audit", "theorem"}
    if kind not in allowed:
        raise SystemExit(f"cannot infer kind for {ident}: {kind!r}")
    return kind


def provenance(ident: str, kind: str, opener: str) -> tuple[str, str, bool]:
    if (kind in {"notice", "source_audit", "mastery_section", "boundary",
                 "hint", "solution"}
            or 'data-origin="edition-original"' in opener
            or "-mcheck-" in ident):
        return "edition_original", COMPANION_RIGHTS, True
    return "translated_adapted_from_upstream", ROBERTS_RIGHTS, False


def target_locator(start: int, end: int, raw_lines: list[bytes]) -> dict[str, Any]:
    return {"content_sha256": digest(b"".join(raw_lines[start - 1:end])),
            "file_sha256": SOURCE_SHA, "line_end": end, "line_start": start,
            "path": SOURCE_PATH}


def source_locator(ident: str, edition_original: bool) -> dict[str, Any]:
    if edition_original:
        return {"kind": "edition_original", "path": SOURCE_PATH,
                "precision": "exact_target_span"}
    if ident not in SOURCE_RANGES:
        raise SystemExit(f"missing exact Unit 28 source locator: {ident}")
    start, end = SOURCE_RANGES[ident]
    return {"commit_sha": COMMIT, "line_end": end, "line_start": start,
            "path": "Notes.tex", "precision": "exact_source_span"}


def display_title(ident: str, lines: list[str], start: int, kind: str) -> str:
    first = lines[start - 1].strip()
    if first.startswith("#"):
        return re.sub(r"\s*\{.*\}$", "", re.sub(r"^#+\s*", "", first)).strip()
    for line in lines[start:min(start + 7, len(lines))]:
        value = line.strip().replace("**", "")
        if value and not value.startswith(":::") and not value.startswith(">"):
            return value[:180]
    return f"Unit 28 {kind} {ident.rsplit('-', 1)[-1]}"


def verify_evidence() -> dict[str, Any]:
    for _ident, (relative, size, expected_sha, _media, _state, _qas) in EVIDENCE.items():
        raw = (LANE / relative).read_bytes()
        if len(raw) != size or digest(raw) != expected_sha:
            raise SystemExit(f"Unit 28 evidence identity mismatch: {relative}")
    qa = json.loads(QA_JSON.read_text(encoding="utf-8"))
    resolved = qa.get("resolved_findings")
    expected = {"UNIT028-MATH-P2-001", "UNIT028-AUDIT-P3-001",
                "UNIT028-PROV-P3-002", "UNIT028-MATH-P3-003",
                "UNIT028-TERM-P3-004", "UNIT028-TERM-P3-005"}
    if (qa.get("status") != "PASS"
            or qa.get("source", {}).get("line_start") != UPSTREAM_START
            or qa.get("source", {}).get("line_end") != UPSTREAM_END
            or qa.get("source", {}).get("span_bytes") != UPSTREAM_SPAN_BYTES
            or qa.get("source", {}).get("span_sha256") != UPSTREAM_SPAN_SHA
            or qa.get("source", {}).get("next_line") != NEXT_SOURCE_LINE
            or qa.get("unit", {}).get("bytes") != SOURCE_BYTES
            or qa.get("unit", {}).get("lines") != SOURCE_LINES
            or qa.get("unit", {}).get("sha256") != SOURCE_SHA
            or qa.get("unit", {}).get("stable_ids") != 47
            or qa.get("unit", {}).get("fenced_semantic_objects") != 39
            or qa.get("proof_closure", {}).get("mastery_solution_triples") != 6
            or qa.get("model_provenance") != MODEL
            or not isinstance(resolved, list)
            or {item.get("finding_id") for item in resolved} != expected
            or any(item.get("status") != "RESOLVED_BEFORE_ADMISSION" for item in resolved)
            or any(item.get("status") != "PASS" for item in qa.get("checks", []))):
        raise SystemExit("Unit 28 QA content/binding mismatch")
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
        raise SystemExit("Unit 28 reader identity/newline mismatch")
    raw_lines = raw.splitlines(keepends=True)
    lines = [line.decode("utf-8").rstrip("\n") for line in raw_lines]
    text = raw.decode("utf-8")
    if (len(lines) != SOURCE_LINES or text.count(MODEL) != 1
            or re.search(r"\bfunktor\b", text, re.IGNORECASE)
            or re.search(r"\bbola\b", text, re.IGNORECASE)):
        raise SystemExit("Unit 28 reader line/provenance/terminology mismatch")
    spans = structural_spans(lines)

    for slug, (source_term, _preferred, _evidence, domain) in NEW_TERMS.items():
        concept = common("concept", f"concept:{slug}")
        concept.update({"canonical_label": source_term, "domain": domain,
                        "locale_neutral": True})
        add("concepts.jsonl", concept)
    concept_ids = list(REUSED_CONCEPTS) + [f"concept:{slug}" for slug in NEW_TERMS]
    if any(ident not in existing_ids and ident not in additions["concepts.jsonl"]
           for ident in concept_ids):
        raise SystemExit("Unit 28 concept closure mismatch")

    rights_specs = (
        (COMPANION_RIGHTS,
         "Indonesian original solutions, mastery, proof-completion, source-audit, and accessibility layer for Roberts Unit 28.",
         "Original additions are CC BY 4.0; source-derived material remains separately attributed.",
         [ROOT], None),
        (COMPOSITE_RIGHTS,
         "David Michael Roberts source adaptation plus original Indonesian Unit 28 companions.",
         "Translated, repaired, and original layers remain component-distinguishable.",
         [ROOT], None),
        (CUMULATIVE_RIGHTS,
         "Cumulative Roberts Units 001-028 Indonesian reader source boundary.",
         "Append-only semantic pointer; verified prior build artifacts remain immutable until separate build admission.",
         [f"unit:o012-rbt-u{number:03d}" for number in range(1, 29)], PRIOR_RIGHTS),
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

    section_ranges = (("o012-rbt-l28-s01", 55, 140),
                      ("o012-rbt-l28-s02", 141, 207),
                      ("o012-rbt-l28-s03", 208, 357),
                      ("o012-rbt-l28-s04", 358, 507),
                      ("o012-rbt-l28-s05", 508, 572))
    section_ids = {item[0] for item in section_ranges}

    def parent_local(ident: str, start: int) -> str:
        if ident in {"o012-rbt-l28-notice", "o012-rbt-l28",
                     "o012-rbt-l28-mastery", "o012-rbt-l28-boundary-001"}:
            return ROOT
        if ident in section_ids:
            return LECTURE
        if any(token in ident for token in ("-mcheck-", "-hint-", "-sol-")):
            return MASTERY
        for section, low, high in section_ranges:
            if low <= start <= high:
                return f"unit:{section}"
        raise SystemExit(f"cannot assign Unit 28 parent: {ident}")

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
        "display_title": "Topologi Aljabar - Unit 28: Kohomologi Sfera, Eksisi, dan Baji Kerangka",
        "edition_id": EDITION, "edition_unit_id": ROOT, "locale": "id-ID",
        "model_provenance": MODEL, "order": 28, "parent_id": COURSE,
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
                        "source_locator": source_locator(ident, edition_original),
                        "target_locator": locator,
                        "translation_state": "structurally_verified", "unit_id": unit_id})
        if ident == "o012-rbt-l28-thm-002":
            unit["source_aliases"] = ["thm:collapse"]
            segment["source_aliases"] = ["thm:collapse"]
        if ident == "o012-rbt-l28-boundary-001":
            unit["next_source_line"] = NEXT_SOURCE_LINE
            segment["next_source_line"] = NEXT_SOURCE_LINE
        if kind == "proof":
            proof_status = ("complete_original_proof" if edition_original
                            else "complete_translated_proof")
            unit["proof_status"] = proof_status
            segment["proof_status"] = proof_status
        if kind == "solution":
            unit["solution_status"] = "complete_checked_solution"
            segment["solution_status"] = "complete_checked_solution"
        add("units.jsonl", unit); add("segments.jsonl", segment)

    asset = common("asset", "asset:o012-u028-source-markdown")
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
                     "usage_note": "Attested in the independently reviewed Unit 28 reader; admitted lane terminology is preserved without changing the global terminology control.",
                     "variants": []})
        add("terms.jsonl", term)

    for ident, (correction_type, evidence, suffixes, defect, change, rationale) in CORRECTIONS.items():
        targets = [f"unit:o012-rbt-l28-{suffix}" for suffix in suffixes]
        if any(target.removeprefix("unit:") not in spans for target in targets):
            raise SystemExit(f"correction target absent: {ident}")
        correction = common("correction", ident)
        correction.update({"affected_unit_ids": targets,
                           "correction_type": correction_type, "edition_id": EDITION,
                           "evidence": evidence,
                           "evidence_segment_id": "segment:o012-rbt-l28-notice",
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
                         "toolchain": (f"Bounded Unit 28 evidence; Notes.tex:5924-6052 "
                                       f"span {UPSTREAM_SPAN_SHA}; {MODEL}; route {ROUTE}; "
                                       "no cumulative build/publication assertion."),
                         "translation_state": state, "unit_id": ROOT})
        add("artifacts.jsonl", artifact)

    qa_specs = (
        ("qa:o012-u028-source-integrity", "source",
         "Unit 28 authority and reader identities, 47 stable IDs, exact source label, source census, and native-MathML structure passed.",
         ["artifact:o012-u028-source-audit", "artifact:o012-u028-qa"]),
        ("qa:o012-u028-math", "math",
         "Independent Unit 28 mathematical review passed with no open P1, P2, or P3 finding and four complete proof objects.",
         ["artifact:o012-u028-independent-review"]),
        ("qa:o012-u028-language", "language",
         "Independent Indonesian review passed after all six P2/P3 findings were resolved before admission.",
         ["artifact:o012-u028-independent-review", "artifact:o012-u028-qa"]),
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

    relation("relation:adapts:o012-rbt-u028:edition", ROOT, "adapts", EDITION,
             "Unit 28 is the Indonesian adapted reader boundary for the frozen Roberts edition.")
    relation("relation:precedes:o012-rbt-u027:o012-rbt-u028",
             "unit:o012-rbt-u027", "precedes", ROOT,
             "Preserves contiguous Roberts lecture-unit order.")
    relation("relation:precedes:o012-rbt-l28:mastery", LECTURE, "precedes", MASTERY,
             "Lecture content precedes the six edition-original mastery items.")
    relation("relation:boundary:o012-u028", CUMULATIVE_RIGHTS, "contains", ROOT,
             "Additive cumulative Units 001-028 semantic source boundary.")
    relation("relation:route:d60-r14:o012-rbt-u028", COURSE, "contains", ROOT,
             "Roberts Lecture 28 is an edition unit in the non-destructive D60-R14 route view.",
             course_route_unit_id=ROUTE, edition_unit_id=ROOT)
    relation("relation:xref:o012-rbt-l28-s01:l27-eq-002",
             "unit:o012-rbt-l28-s01", "xref", "unit:o012-rbt-l27-eq-002",
             "The continued sphere calculation starts from the Unit 27 Mayer--Vietoris reduction.")
    relation("relation:depends-on:o012-rbt-l28-cor-001:thm-002",
             "unit:o012-rbt-l28-cor-001", "depends-on", "unit:o012-rbt-l28-thm-002",
             "The quotient theorem converts the relative long exact sequence.")
    relation("relation:depends-on:o012-rbt-l28-proof-003:thm-002",
             "unit:o012-rbt-l28-proof-003", "depends-on", "unit:o012-rbt-l28-thm-002",
             "The corollary proof substitutes the quotient isomorphism.")
    relation("relation:xref:o012-rbt-l28-proof-003:l26-prop-002",
             "unit:o012-rbt-l28-proof-003", "xref", "unit:o012-rbt-l26-prop-002",
             "The source cross-reference points to the long exact sequence of a pair.")
    relation("relation:depends-on:o012-rbt-l28-prop-003:thm-002",
             "unit:o012-rbt-l28-prop-003", "depends-on", "unit:o012-rbt-l28-thm-002",
             "The infinite-wedge proof applies the quotient theorem to a coproduct pair.")
    relation("relation:depends-on:o012-rbt-l28-exa-001:prop-003",
             "unit:o012-rbt-l28-exa-001", "depends-on", "unit:o012-rbt-l28-prop-003",
             "The sphere-wedge calculation applies the wedge-cohomology proposition.")
    proof_targets = {1: "unit:o012-rbt-l28-prop-002",
                     2: "unit:o012-rbt-l28-thm-002",
                     3: "unit:o012-rbt-l28-cor-001",
                     4: "unit:o012-rbt-l28-prop-003"}
    for number, target in proof_targets.items():
        relation(f"relation:proves:o012-rbt-l28-proof-{number:03d}:closure",
                 f"unit:o012-rbt-l28-proof-{number:03d}", "proves", target,
                 f"Complete proof closure {number} for Unit 28.")
    for number in range(1, 7):
        relation(f"relation:solves:l28-sol-{number:03d}:l28-mcheck-{number:03d}",
                 f"unit:o012-rbt-l28-sol-{number:03d}", "solves",
                 f"unit:o012-rbt-l28-mcheck-{number:03d}",
                 f"Complete checked solution for Unit 28 mastery check {number}.")
        relation(f"relation:hints:l28-hint-{number:03d}:l28-mcheck-{number:03d}",
                 f"unit:o012-rbt-l28-hint-{number:03d}", "hints",
                 f"unit:o012-rbt-l28-mcheck-{number:03d}",
                 f"Bounded hint for Unit 28 mastery check {number}.")

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
            raise SystemExit(f"noncanonical Unit 28 path: {ident}")
        if unit["parent_id"].startswith("unit:") and unit["path"][:-1] != by_id[unit["parent_id"]]["path"]:
            raise SystemExit(f"Unit 28 parent path mismatch: {ident}")
        for obj in (unit, segment):
            if (obj["edition_unit_id"] != ROOT or obj["course_route_unit_id"] != ROUTE
                    or obj["model_provenance"] != MODEL):
                raise SystemExit(f"Unit 28 route/provenance mismatch: {ident}")
    sibling_orders: defaultdict[str, list[int]] = defaultdict(list)
    for obj in additions["units.jsonl"].values():
        sibling_orders[obj["parent_id"]].append(obj["order"])
    if any(len(values) != len(set(values)) for values in sibling_orders.values()):
        raise SystemExit("duplicate Unit 28 sibling order")
    for number in range(1, 7):
        check = f"unit:o012-rbt-l28-mcheck-{number:03d}"
        solves = [obj for obj in additions["relations.jsonl"].values()
                  if obj["relation_type"] == "solves" and obj["to_id"] == check]
        hints = [obj for obj in additions["relations.jsonl"].values()
                 if obj["relation_type"] == "hints" and obj["to_id"] == check]
        if len(solves) != 1 or len(hints) != 1:
            raise SystemExit(f"Unit 28 mastery closure mismatch: {number}")
    if len([obj for obj in additions["units.jsonl"].values()
            if obj.get("proof_status")]) != 4:
        raise SystemExit("Unit 28 four-proof closure mismatch")
    if len(additions["corrections.jsonl"]) != 17:
        raise SystemExit("Unit 28 correction dossier mismatch")
    if additions["rights.jsonl"][CUMULATIVE_RIGHTS]["component_scope"] != [
            f"unit:o012-rbt-u{number:03d}" for number in range(1, 29)]:
        raise SystemExit("Unit 28 cumulative rights scope mismatch")
    if by_id["unit:o012-rbt-l28-boundary-001"].get("next_source_line") != NEXT_SOURCE_LINE:
        raise SystemExit("Unit 28 terminal cursor mismatch")
    aliases = {alias: unit["id"] for unit in additions["units.jsonl"].values()
               for alias in unit.get("source_aliases", [])}
    if aliases != {"thm:collapse": "unit:o012-rbt-l28-thm-002"}:
        raise SystemExit("Unit 28 source-label alias closure mismatch")
    expected_findings = {"UNIT028-MATH-P2-001", "UNIT028-AUDIT-P3-001",
                         "UNIT028-PROV-P3-002", "UNIT028-MATH-P3-003",
                         "UNIT028-TERM-P3-004", "UNIT028-TERM-P3-005"}
    if {item.get("finding_id") for item in qa_doc["resolved_findings"]} != expected_findings:
        raise SystemExit("Unit 28 pre-admission finding set changed")

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
    print("Unit 028 semantic backend extension: PASS")
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
    print("stable_ids=47")
    print("proof_closures=4")
    print("mastery_triples=6")
    print("source_aliases=1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
