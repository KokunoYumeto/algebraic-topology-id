#!/usr/bin/env python3
"""Fail-closed append-only semantic-backend admission for Roberts Unit 029."""
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
SOURCE = LANE / "source/id-ID/units/unit-029-lecture-029.md"
UPSTREAM = (LANE / "authority/upstream" /
            "AlgebraicTopology2019-b947ad2e9f9e301bfe24590a9db653bc54fa1a53" /
            "Notes.tex")
AUDIT = LANE / "qa/UNIT_029_SOURCE_AUDIT.md"
REVIEW = LANE / "qa/UNIT_029_INDEPENDENT_REVIEW.md"
QA_JSON = LANE / "qa/UNIT_029_QA.json"

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
COMPANION_RIGHTS = "rights:o012-u029-companion-cc-by-4.0"
COMPOSITE_RIGHTS = "rights:o012-u029-composite-cc-by-4.0"
CUMULATIVE_RIGHTS = "rights:o012-units-001-029-composite-cc-by-4.0"
PRIOR_RIGHTS = "rights:o012-units-001-028-composite-cc-by-4.0"
ROOT = "unit:o012-rbt-u029"
LECTURE = "unit:o012-rbt-l29"
MASTERY = "unit:o012-rbt-l29-mastery"
SOURCE_PATH = "source/id-ID/units/unit-029-lecture-029.md"
SOURCE_BYTES = 27687
SOURCE_LINES = 805
SOURCE_SHA = "cfb8fa5c49593a187bed5df1d4173cc952100b18e5faa009cb8d57036c5726c4"
UPSTREAM_BYTES = 331447
UPSTREAM_LINES = 6368
UPSTREAM_SHA = "cfe93e9dbe3e25bd96f711f59e6078ab97527682b58e1f8ad127f74357f665d7"
UPSTREAM_START = 6053
UPSTREAM_END = 6270
UPSTREAM_SPAN_BYTES = 11447
UPSTREAM_SPAN_SHA = "33c6b7bfe3216d271c6b1f9d0cb952e6ef02a5e27a57f686936e764bfc4a9233"
NEXT_SOURCE_LINE = 6271

FILES = ("artifacts.jsonl", "assets.jsonl", "authority.jsonl", "concepts.jsonl",
         "corrections.jsonl", "qa.jsonl", "relations.jsonl", "rights.jsonl",
         "segments.jsonl", "terms.jsonl", "units.jsonl")
PREFIX = {
    "artifacts.jsonl": (154, 123215, "dcbe6a233ae2150054b6337fcbcde5a8429f36e13376fdc1e5cfe89319181934"),
    "assets.jsonl": (30, 18527, "33e5e928c08a45e019c5647baf76afc49febf66c91fe20bcb52ebaa903f1693d"),
    "authority.jsonl": (4, 2721, "f21af26912520ab34b38dff0e927ed46a546dbe5d318da0dc133e58330d0e368"),
    "concepts.jsonl": (347, 109564, "b65dbfd31c351d73b270eaf3054df7101a5cfac462a530492888fe6b1a845ae8"),
    "corrections.jsonl": (378, 370217, "bca78b345bd76599e3f62f79a41e4827754fa03b7c2fc63e207282651e71e27a"),
    "qa.jsonl": (128, 71958, "f288d793f7d9a2823cc266d3f1c6a6764647127ea0b941d80a6205d8cff06001"),
    "relations.jsonl": (476, 194744, "f9e351b32fdf3397e5b5cb47af3039da94585f3712369c69514ec46673b25f36"),
    "rights.jsonl": (80, 73939, "71f0dd345afdff972f389987a504dc8392a4e4d17d850dbb21f219053f515a9b"),
    "segments.jsonl": (1230, 1736383, "639756c98657d171553f581ec8d252dff48f99ce0b1411d7adc94fbbac56791d"),
    "terms.jsonl": (340, 214594, "f36b329242860f92bdd827594ca8f3bedc140daabc8dbfe5f895534a9de9dfa5"),
    "units.jsonl": (1258, 1849591, "6261024f22eb6b2e90d45f07ed0108fc009a6ebfb2d415e88afce3e411524a3d"),
}
PREFIX_RECORDS = 4425
PREFIX_BYTES = 4765453
PREFIX_BUNDLE = "3a7492ee9755c85e89139bd6af84121747caa85f1f6421c7ec2e133b010a0b9f"

EVIDENCE = {
    "artifact:o012-u029-source-audit": (
        "qa/UNIT_029_SOURCE_AUDIT.md", 5738,
        "6b3e96ca5a7d24a4f8182c46f02e99194c9538ca534b4b550ea23b666ad89afb",
        "text/markdown; charset=utf-8", "source_frozen",
        ["qa:o012-u029-source-integrity"]),
    "artifact:o012-u029-independent-review": (
        "qa/UNIT_029_INDEPENDENT_REVIEW.md", 8535,
        "873c21354acc83050e13f7236b361f29523b91d4907d9b0046ee061f7723547c",
        "text/markdown; charset=utf-8", "mathematically_reviewed",
        ["qa:o012-u029-math", "qa:o012-u029-language"]),
    "artifact:o012-u029-qa": (
        "qa/UNIT_029_QA.json", 11192,
        "66f5709282d890e24a20756b69d287305497011c8f6e39d7108a30d5b4b1ffd9",
        "application/json", "built",
        ["qa:o012-u029-source-integrity", "qa:o012-u029-language"]),
}

EXPECTED_ANCHORS = (
    "o012-rbt-l29-notice", "o012-rbt-l29", "o012-rbt-l29-s01",
    "o012-rbt-l29-lem-001", "o012-rbt-l29-proof-001",
    "o012-rbt-l29-audit-001", "o012-rbt-l29-s02",
    "o012-rbt-l29-fact-001", "o012-rbt-l29-proof-002",
    "o012-rbt-l29-audit-002", "o012-rbt-l29-s03",
    "o012-rbt-l29-thm-001", "o012-rbt-l29-proof-003",
    "o012-rbt-l29-cor-001", "o012-rbt-l29-proof-004",
    "o012-rbt-l29-audit-003", "o012-rbt-l29-s04",
    "o012-rbt-l29-def-001", "o012-rbt-l29-audit-004",
    "o012-rbt-l29-fig-001", "o012-rbt-l29-exa-001",
    "o012-rbt-l29-exa-002", "o012-rbt-l29-s05",
    "o012-rbt-l29-def-002", "o012-rbt-l29-exa-003",
    "o012-rbt-l29-audit-005", "o012-rbt-l29-s06",
    "o012-rbt-l29-thm-002", "o012-rbt-l29-audit-006",
    "o012-rbt-l29-mastery", "o012-rbt-l29-mcheck-001",
    "o012-rbt-l29-hint-001", "o012-rbt-l29-sol-001",
    "o012-rbt-l29-mcheck-002", "o012-rbt-l29-hint-002",
    "o012-rbt-l29-sol-002", "o012-rbt-l29-mcheck-003",
    "o012-rbt-l29-hint-003", "o012-rbt-l29-sol-003",
    "o012-rbt-l29-mcheck-004", "o012-rbt-l29-hint-004",
    "o012-rbt-l29-sol-004", "o012-rbt-l29-mcheck-005",
    "o012-rbt-l29-hint-005", "o012-rbt-l29-sol-005",
    "o012-rbt-l29-mcheck-006", "o012-rbt-l29-hint-006",
    "o012-rbt-l29-sol-006", "o012-rbt-l29-boundary-001",
)
SOURCE_RANGES = {
    "o012-rbt-l29": (6053, 6270),
    "o012-rbt-l29-s01": (6054, 6062),
    "o012-rbt-l29-lem-001": (6054, 6062),
    "o012-rbt-l29-s02": (6064, 6091),
    "o012-rbt-l29-fact-001": (6079, 6088),
    "o012-rbt-l29-s03": (6093, 6140),
    "o012-rbt-l29-thm-001": (6093, 6095),
    "o012-rbt-l29-proof-003": (6097, 6100),
    "o012-rbt-l29-cor-001": (6106, 6112),
    "o012-rbt-l29-s04": (6142, 6220),
    "o012-rbt-l29-def-001": (6151, 6168),
    "o012-rbt-l29-exa-001": (6211, 6213),
    "o012-rbt-l29-exa-002": (6217, 6220),
    "o012-rbt-l29-s05": (6222, 6244),
    "o012-rbt-l29-def-002": (6224, 6227),
    "o012-rbt-l29-s06": (6245, 6270),
    "o012-rbt-l29-thm-002": (6245, 6261),
}
DIAGRAMS = {
    "o012-rbt-l29-lem-001": (["xypic"], 1),
    "o012-rbt-l29-s02": (["xypic"], 2),
    "o012-rbt-l29-def-001": (["xypic"], 1),
    "o012-rbt-l29-fig-001": (["tikz"], 1),
}

NEW_TERMS = {
    "cohomology-comparison-theorem": ("cohomology comparison theorem", "teorema perbandingan kohomologi", "o012-rbt-l29-thm-001", "algebraic_topology"),
    "cw-complex": ("CW complex", "kompleks CW", "o012-rbt-l29-def-001", "algebraic_topology"),
    "cw-pair": ("CW pair", "pasangan CW", "o012-rbt-l29-def-002", "algebraic_topology"),
    "cellular-filtration": ("cellular filtration", "filtrasi seluler", "o012-rbt-l29-def-001", "algebraic_topology"),
    "milnor-derived-limit-sequence": ("Milnor derived-limit sequence", "barisan eksak limit turunan Milnor", "o012-rbt-l29-proof-004", "homological_algebra"),
    "eilenberg-steenrod-axioms": ("Eilenberg--Steenrod axioms", "aksioma Eilenberg--Steenrod", "o012-rbt-l29-thm-002", "algebraic_topology"),
    "strong-excision": ("strong excision", "eksisi kuat", "o012-rbt-l29-thm-002", "algebraic_topology"),
}
REUSED_CONCEPTS = (
    "concept:singular-simplicial-cochain-comparison", "concept:naturality",
    "concept:five-lemma", "concept:k-skeleton", "concept:wedge-sum",
    "concept:reduced-cohomology", "concept:relative-cohomology",
    "concept:cochain-map", "concept:long-exact-sequence",
    "concept:attaching-map", "concept:homotopy-category",
    "concept:excision", "concept:relative-cohomology-quotient-isomorphism",
)

CORRECTIONS = {
    "correction:o012-u029-dossier-001": (
        "mathematical_correction", "Notes.tex:6054-6122",
        ["lem-001", "s02", "fact-001", "thm-001", "cor-001", "audit-001"],
        "The source reverses every comparison map induced by distinguished simplex inclusion.",
        "Use restriction from singular to Delta-set cochains and cohomology throughout all diagrams and results.",
        "Every comparison now follows contravariant precomposition consistently."),
    "correction:o012-u029-dossier-002": (
        "mathematical_correction", "Notes.tex:6079-6088",
        ["fact-001", "proof-002", "audit-002"],
        "The relative sphere factor is unreduced and its factor map is reversed, including a dimension-zero defect.",
        "Use reduced sphere cohomology and the pullback of the quotient map of pairs.",
        "The factor comparison is correct in every dimension."),
    "correction:o012-u029-dossier-003": (
        "proof_completion", "Notes.tex:6097-6100",
        ["thm-001", "proof-003"],
        "The finite-dimensional comparison proof only invokes induction and the Five Lemma.",
        "Supply the base case, skeletal induction, four surrounding isomorphisms, and five-term application.",
        "The comparison theorem has a complete internal proof."),
    "correction:o012-u029-dossier-004": (
        "proof_completion", "Notes.tex:6114-6122",
        ["cor-001", "proof-004", "audit-003"],
        "The infinite-dimensional case appeals to filtered colimits without closing the inverse-limit issue.",
        "Prove stabilization in degrees k and k-1 and vanishing of the Milnor derived-limit term.",
        "Passage from finite skeletons to the full realization is justified."),
    "correction:o012-u029-dossier-005": (
        "clarification", "Notes.tex:6106-6112",
        ["cor-001"],
        "The corollary omits R and contains local typographic defects.",
        "Restore coefficients and normalize punctuation and spelling.",
        "The comparison is fully typed and readable."),
    "correction:o012-u029-dossier-006": (
        "mathematical_correction", "Notes.tex:6151-6168",
        ["def-001", "audit-004"],
        "The source attachment index starts at n at least one and therefore omits one-cells.",
        "Start at n equals zero and index J by the dimension of the attached n-plus-one cell.",
        "The definition builds graphs and all higher CW complexes."),
    "correction:o012-u029-dossier-007": (
        "accessibility_reflow", "Notes.tex:6056-6077,6160-6165,6171-6200",
        ["lem-001", "s02", "def-001", "fig-001"],
        "Four Xy-pic diagrams and one TikZ picture depend on fixed visual position.",
        "Reflow the complete naturality, exact-sequence, pushout, and attachment semantics in reading order.",
        "All diagram functions remain available on narrow screens and to assistive readers."),
    "correction:o012-u029-dossier-008": (
        "mathematical_correction", "Notes.tex:6217-6220",
        ["exa-002"],
        "The manifold example risks conflating literal CW structure with finite CW homotopy type across categories.",
        "State the safe smooth compact structure result and the topological compact homotopy-type result separately.",
        "No universal triangulability claim remains."),
    "correction:o012-u029-dossier-009": (
        "clarification", "Notes.tex:6240-6243",
        ["s05", "audit-005"],
        "Homotopy equivalence classes of maps is ambiguous about which maps are admitted.",
        "Define morphisms as homotopy classes of pair maps.",
        "The homotopy category has the intended objects and morphisms."),
    "correction:o012-u029-dossier-010": (
        "mathematical_correction", "Notes.tex:6245-6261",
        ["thm-002", "audit-006"],
        "The excision axiom evaluates a complement pair not guaranteed to lie in the stated CW-pair domain.",
        "Type complement excision on actual CW pairs and add the strong quotient form as a map of CW pairs.",
        "The cohomology theory is never evaluated outside its domain."),
    "correction:o012-u029-dossier-011": (
        "clarification", "Notes.tex:6245-6266",
        ["thm-002"],
        "Variance, additivity, exactness, dimension, and homotopy-category normalization are compressed.",
        "State the opposite-category variance once and preserve the complete normalized axiom package.",
        "The uniqueness theorem is fully reconstructible from the reader."),
    "correction:o012-u029-resolved-math-p2-001": (
        "mathematical_correction", "UNIT029-MATH-P2-001",
        ["fact-001", "proof-002"],
        "The pre-admission relative factor used unreduced sphere cohomology.",
        "Use reduced cohomology and identify the factor as quotient-pair pullback.",
        "The dimension-zero case is now correct."),
    "correction:o012-u029-resolved-math-p2-002": (
        "proof_completion", "UNIT029-MATH-P2-002",
        ["proof-004", "audit-003"],
        "Degree-k stabilization alone did not remove the derived-limit obstruction.",
        "Record stabilization in degrees k and k-1 and the resulting Milnor lim-one vanishing.",
        "The infinite-dimensional extension is closed."),
    "correction:o012-u029-resolved-type-p2-003": (
        "mathematical_correction", "UNIT029-TYPE-P2-003",
        ["thm-002", "audit-006"],
        "An unspecified CW replacement left excision objects and morphisms untyped.",
        "Restrict complement excision and state strong quotient excision through typed CW pairs.",
        "Every fungtor evaluation has a declared domain object."),
    "correction:o012-u029-resolved-reflow-p3-001": (
        "accessibility_reflow", "UNIT029-REFLOW-P3-001",
        ["s02", "fig-001"],
        "The first reflow omitted two terms from a five-term source diagram.",
        "Restore both full rows and all five vertical maps; inventory four Xy-pic diagrams and one TikZ redraw.",
        "The semantic reflow preserves the complete diagram census."),
    "correction:o012-u029-resolved-cw-p3-002": (
        "clarification", "UNIT029-CW-P3-002",
        ["def-001", "exa-003"],
        "Two CW margins and the sphere-boundary edge case were implicit.",
        "Restore disk/sphere and filtration-colimit explanations and separate n equals one from n at least two.",
        "The CW definition and pair example cover their boundary cases."),
    "correction:o012-u029-resolved-lang-p3-003": (
        "terminology_correction", "UNIT029-LANG-P3-003",
        ["s01", "thm-002"],
        "The draft used nonpreferred Indonesian variants for functoriality, naturality, square, and additivity.",
        "Normalize to fungtor, fungtorial, kealamian, persegi, and aditivitas.",
        "The reader follows the admitted glossary."),
    "correction:o012-u029-resolved-term-p3-004": (
        "terminology_correction", "UNIT029-TERM-P3-004",
        ["audit-002", "audit-003"],
        "The final source-audit draft retained bola for sphere and perpanjangan for extension.",
        "Normalize audit-only control prose to sfera and perluasan.",
        "The reader remains unchanged while the control witness follows admitted terminology."),
    "correction:o012-u029-resolved-qa-p3-005": (
        "metadata_correction", "UNIT029-QA-P3-005",
        ["__root__"],
        "The initial structural census omitted the root lecture ID and reported 48 stable IDs.",
        "Count the root lecture ID and bind the final census to 49 unique stable IDs and nine identified headings.",
        "The backend and QA evidence describe the complete final reader structure without changing reader bytes."),
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
    spec = importlib.util.spec_from_file_location("o012_generic_u029_producer", path)
    if spec is None or spec.loader is None:
        raise SystemExit("cannot load generic backend validator")
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


def load_prefix() -> tuple[dict[str, dict[str, dict[str, Any]]], dict[str, bytes]]:
    tables: dict[str, dict[str, dict[str, Any]]] = {}
    raw_files: dict[str, bytes] = {}
    seen: set[str] = set(); bundle = hashlib.sha256()
    for name in FILES:
        raw = (BACKEND / name).read_bytes(); count, size, expected_sha = PREFIX[name]
        lines = raw.splitlines(keepends=True)
        if (len(raw), len(lines), digest(raw)) != (size, count, expected_sha):
            raise SystemExit(f"{name}: immutable Units 001-028 prefix mismatch")
        if b"\r" in raw or not raw.endswith(b"\n"):
            raise SystemExit(f"{name}: prefix newline mismatch")
        table: dict[str, dict[str, Any]] = {}
        for number, line in enumerate(lines, 1):
            obj = json.loads(line.decode("utf-8"))
            if not isinstance(obj.get("id"), str) or obj["id"] in seen or canon(obj) != line:
                raise SystemExit(f"{name}:{number}: noncanonical/duplicate prefix record")
            seen.add(obj["id"]); table[obj["id"]] = obj
        tables[name] = table; raw_files[name] = raw
        bundle.update(name.encode()); bundle.update(b"\0"); bundle.update(raw)
    if (len(seen) != PREFIX_RECORDS
            or sum(len(raw) for raw in raw_files.values()) != PREFIX_BYTES
            or bundle.hexdigest() != PREFIX_BUNDLE):
        raise SystemExit("Units 001-028 backend bundle identity mismatch")
    if not {"unit:o012-rbt-u028", PRIOR_RIGHTS,
            "artifact:o012-u028-independent-review"} <= seen:
        raise SystemExit("Unit 28 prefix closure is incomplete")
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
        raise SystemExit("Unit 29 upstream span mismatch")
    if (lines[6052].strip() != "\\lecturenum{29}"
            or lines[6269].strip() != ""
            or "\\lecturenum{30}" not in lines[6270]):
        raise SystemExit("Unit 29 source boundary identity mismatch")


def structural_spans(lines: list[str]) -> dict[str, tuple[int, int, str]]:
    opening = re.compile(r"^\s*:::\s+\{[^#}]*#(o012-rbt-l29(?:-[A-Za-z0-9-]+)?)(.*)\}\s*$")
    heading = re.compile(r"^#{1,6}\s+.*\{[^}]*#(o012-rbt-l29(?:-[A-Za-z0-9-]+)?)[^}]*\}\s*$")
    stack: list[tuple[str, int, str]] = []
    spans: dict[str, tuple[int, int, str]] = {}; ordered: list[str] = []
    for number, line in enumerate(lines, 1):
        hm = heading.match(line)
        if hm: ordered.append(hm.group(1))
        fm = opening.match(line)
        if fm:
            ordered.append(fm.group(1)); stack.append((fm.group(1), number, line))
        elif line.strip() == ":::":
            if not stack: raise SystemExit(f"unexpected div close at reader line {number}")
            ident, start, opener = stack.pop(); spans[ident] = (start, number, opener)
    if stack: raise SystemExit(f"unclosed div anchors: {[item[0] for item in stack]}")
    headings = {
        "o012-rbt-l29-notice": (12, 51), "o012-rbt-l29": (52, 592),
        "o012-rbt-l29-s01": (54, 110), "o012-rbt-l29-s02": (111, 225),
        "o012-rbt-l29-s03": (226, 339), "o012-rbt-l29-s04": (340, 449),
        "o012-rbt-l29-s05": (450, 508), "o012-rbt-l29-s06": (509, 592),
        "o012-rbt-l29-mastery": (593, 799),
    }
    for ident, (start, end) in headings.items():
        if ident not in lines[start - 1]: raise SystemExit(f"heading mismatch: {ident}")
        spans[ident] = (start, end, lines[start - 1])
    if tuple(ordered) != EXPECTED_ANCHORS or set(spans) != set(EXPECTED_ANCHORS):
        raise SystemExit("Unit 29 stable-ID inventory/order mismatch")
    return spans


def unit_kind(ident: str, opener: str) -> str:
    if ident.endswith("-notice"): return "notice"
    if ident == "o012-rbt-l29": return "lecture"
    if ident.endswith("-mastery"): return "mastery_section"
    if re.fullmatch(r"o012-rbt-l29-s\d{2}", ident): return "section"
    match = re.search(r"\{\.([A-Za-z][A-Za-z0-9_-]*)", opener)
    kind = match.group(1).replace("source-audit", "source_audit") if match else ""
    allowed = {"boundary", "corollary", "definition", "example", "exercise",
               "fact", "figure", "hint", "lemma", "proof", "solution",
               "source_audit", "theorem"}
    if kind not in allowed: raise SystemExit(f"cannot infer kind for {ident}: {kind!r}")
    return kind


def provenance(ident: str, kind: str, opener: str) -> tuple[str, str, bool]:
    if (kind in {"notice", "source_audit", "mastery_section", "boundary",
                 "hint", "solution", "figure"}
            or 'data-origin="edition-original"' in opener
            or "-mcheck-" in ident or ident == "o012-rbt-l29-exa-003"):
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
    if ident not in SOURCE_RANGES: raise SystemExit(f"missing source locator: {ident}")
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
    return f"Unit 29 {kind} {ident.rsplit('-', 1)[-1]}"


def verify_evidence() -> dict[str, Any]:
    for _ident, (relative, size, expected_sha, _media, _state, _qas) in EVIDENCE.items():
        raw = (LANE / relative).read_bytes()
        if len(raw) != size or digest(raw) != expected_sha:
            raise SystemExit(f"Unit 29 evidence identity mismatch: {relative}")
    qa = json.loads(QA_JSON.read_text(encoding="utf-8"))
    expected = {"UNIT029-MATH-P2-001", "UNIT029-MATH-P2-002",
                "UNIT029-TYPE-P2-003", "UNIT029-REFLOW-P3-001",
                "UNIT029-CW-P3-002", "UNIT029-LANG-P3-003",
                "UNIT029-TERM-P3-004", "UNIT029-QA-P3-005"}
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
            or qa.get("unit", {}).get("stable_ids") != 49
            or qa.get("unit", {}).get("fenced_semantic_objects") != 40
            or qa.get("proof_closure", {}).get("mastery_solution_triples") != 6
            or qa.get("model_provenance") != MODEL
            or not isinstance(resolved, list)
            or {item.get("finding_id") for item in resolved} != expected
            or any(item.get("status") != "RESOLVED_BEFORE_ADMISSION" for item in resolved)
            or any(item.get("status") != "PASS" for item in qa.get("checks", []))):
        raise SystemExit("Unit 29 QA content/binding mismatch")
    audit_text = AUDIT.read_text(encoding="utf-8")
    if re.search(r"\b(bola|perpanjangan)\b", audit_text, re.IGNORECASE):
        raise SystemExit("Unit 29 audit-only preferred terminology finding regressed")
    return qa


def main() -> int:
    tables, prefix_raw = load_prefix(); verify_upstream(); qa_doc = verify_evidence()
    existing_ids = {ident for table in tables.values() for ident in table}
    additions: dict[str, dict[str, dict[str, Any]]] = {name: {} for name in FILES}

    def add(name: str, obj: dict[str, Any]) -> None:
        ident = obj["id"]
        if ident in existing_ids or any(ident in table for table in additions.values()):
            raise SystemExit(f"duplicate new ID: {ident}")
        additions[name][ident] = obj

    raw = SOURCE.read_bytes()
    if (len(raw) != SOURCE_BYTES or digest(raw) != SOURCE_SHA or b"\r" in raw
            or not raw.endswith(b"\n")): raise SystemExit("Unit 29 reader identity/newline mismatch")
    raw_lines = raw.splitlines(keepends=True)
    lines = [line.decode("utf-8").rstrip("\n") for line in raw_lines]
    text = raw.decode("utf-8")
    if (len(lines) != SOURCE_LINES or text.count(MODEL) != 1
            or re.search(r"\b(funktor|funktorial|naturalitas|bola|perpanjangan)\b|bujur sangkar", text, re.IGNORECASE)):
        raise SystemExit("Unit 29 reader line/provenance/terminology mismatch")
    spans = structural_spans(lines)

    for slug, (source_term, _preferred, _evidence, domain) in NEW_TERMS.items():
        concept = common("concept", f"concept:{slug}")
        concept.update({"canonical_label": source_term, "domain": domain, "locale_neutral": True})
        add("concepts.jsonl", concept)
    concept_ids = list(REUSED_CONCEPTS) + [f"concept:{slug}" for slug in NEW_TERMS]
    if any(ident not in existing_ids and ident not in additions["concepts.jsonl"] for ident in concept_ids):
        raise SystemExit("Unit 29 concept closure mismatch")

    rights_specs = (
        (COMPANION_RIGHTS,
         "Indonesian original solutions, mastery, proof-completion, source-audit, and semantic diagram layer for Roberts Unit 29.",
         "Original additions are CC BY 4.0; source-derived material remains separately attributed.", [ROOT], None),
        (COMPOSITE_RIGHTS,
         "David Michael Roberts source adaptation plus original Indonesian Unit 29 companions.",
         "Translated, repaired, and original layers remain component-distinguishable.", [ROOT], None),
        (CUMULATIVE_RIGHTS,
         "Cumulative Roberts Units 001-029 Indonesian reader source boundary.",
         "Append-only semantic pointer; prior verified build artifacts remain immutable until separate build admission.",
         [f"unit:o012-rbt-u{number:03d}" for number in range(1, 30)], PRIOR_RIGHTS),
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

    section_ranges = (("o012-rbt-l29-s01", 54, 110), ("o012-rbt-l29-s02", 111, 225),
                      ("o012-rbt-l29-s03", 226, 339), ("o012-rbt-l29-s04", 340, 449),
                      ("o012-rbt-l29-s05", 450, 508), ("o012-rbt-l29-s06", 509, 592))
    section_ids = {item[0] for item in section_ranges}

    def parent_local(ident: str, start: int) -> str:
        if ident in {"o012-rbt-l29-notice", "o012-rbt-l29", "o012-rbt-l29-mastery",
                     "o012-rbt-l29-boundary-001"}: return ROOT
        if ident in section_ids: return LECTURE
        if any(token in ident for token in ("-mcheck-", "-hint-", "-sol-")): return MASTERY
        for section, low, high in section_ranges:
            if low <= start <= high: return f"unit:{section}"
        raise SystemExit(f"cannot assign Unit 29 parent: {ident}")

    children: defaultdict[str, list[str]] = defaultdict(list)
    for ident in EXPECTED_ANCHORS: children[parent_local(ident, spans[ident][0])].append(ident)
    order_map = {parent: {ident: number for number, ident in enumerate(
        sorted(items, key=lambda item: spans[item][0]), 1)} for parent, items in children.items()}
    path_by_id: dict[str, list[str]] = {ROOT: [ROOT]}
    root = common("unit", ROOT)
    root.update({"component_source_commit": COMMIT, "component_source_id": RESOURCE,
                 "concept_ids": concept_ids, "course_id": COURSE, "course_route_unit_id": ROUTE,
                 "display_title": "Topologi Aljabar - Unit 29: Perbandingan Kohomologi dan Aksioma Eilenberg--Steenrod",
                 "edition_id": EDITION, "edition_unit_id": ROOT, "locale": "id-ID",
                 "model_provenance": MODEL, "order": 29, "parent_id": COURSE,
                 "path": [ROOT], "program_id": PROGRAM,
                 "provenance_relation": "composite_translated_and_original",
                 "resource_id": RESOURCE, "rights_component_id": COMPOSITE_RIGHTS,
                 "source_local_id": None,
                 "source_locator": {"commit_sha": COMMIT, "line_end": UPSTREAM_END,
                                    "line_start": UPSTREAM_START, "path": "Notes.tex",
                                    "precision": "exact_unit_span", "span_bytes": UPSTREAM_SPAN_BYTES,
                                    "span_sha256": UPSTREAM_SPAN_SHA},
                 "target_locator": target_locator(1, SOURCE_LINES, raw_lines),
                 "translation_state": "structurally_verified", "unit_kind": "reader_unit"})
    add("units.jsonl", root)

    for ident in EXPECTED_ANCHORS:
        start, end, opener = spans[ident]; kind = unit_kind(ident, opener)
        parent_id = parent_local(ident, start)
        if parent_id not in path_by_id: raise SystemExit(f"parent missing: {ident}")
        unit_id = f"unit:{ident}"; path = path_by_id[parent_id] + [unit_id]; path_by_id[unit_id] = path
        provenance_value, rights_id, edition_original = provenance(ident, kind, opener)
        locator = target_locator(start, end, raw_lines)
        shared = {"component_source_commit": COMMIT, "component_source_id": RESOURCE,
                  "course_route_unit_id": ROUTE, "edition_unit_id": ROOT, "model_provenance": MODEL}
        unit = common("unit", unit_id); unit.update(shared)
        unit.update({"concept_ids": concept_ids, "course_id": COURSE,
                     "display_title": display_title(ident, lines, start, kind),
                     "edition_id": EDITION, "locale": "id-ID", "order": order_map[parent_id][ident],
                     "parent_id": parent_id, "path": path, "program_id": PROGRAM,
                     "provenance_relation": provenance_value, "resource_id": RESOURCE,
                     "rights_component_id": rights_id, "source_local_id": ident,
                     "target_locator": locator, "translation_state": "structurally_verified",
                     "unit_kind": kind})
        segment = common("segment", f"segment:{ident}"); segment.update(shared)
        segment.update({"concept_ids": concept_ids, "edition_id": EDITION, "locale": "id-ID",
                        "order": unit["order"], "provenance_relation": provenance_value,
                        "resource_id": RESOURCE, "rights_component_id": rights_id,
                        "segment_kind": kind, "source_local_id": ident,
                        "source_locator": source_locator(ident, edition_original),
                        "target_locator": locator, "translation_state": "structurally_verified",
                        "unit_id": unit_id})
        aliases = re.findall(r'data-source-label="([^"]+)"', opener)
        if aliases: unit["source_aliases"] = aliases; segment["source_aliases"] = aliases
        if ident in DIAGRAMS:
            formats, count = DIAGRAMS[ident]
            for obj in (unit, segment):
                obj["source_formats"] = formats; obj["source_diagram_count"] = count
                obj["accessibility_status"] = "semantic_reflow"
        if ident == "o012-rbt-l29-boundary-001":
            unit["next_source_line"] = NEXT_SOURCE_LINE; segment["next_source_line"] = NEXT_SOURCE_LINE
        if kind == "proof":
            status = "complete_original_proof" if edition_original else "complete_translated_proof"
            unit["proof_status"] = status; segment["proof_status"] = status
        if kind == "solution":
            unit["solution_status"] = "complete_checked_solution"
            segment["solution_status"] = "complete_checked_solution"
        add("units.jsonl", unit); add("segments.jsonl", segment)

    asset = common("asset", "asset:o012-u029-source-markdown")
    asset.update({"bytes": SOURCE_BYTES, "edition_id": EDITION,
                  "media_type": "text/markdown; charset=utf-8", "path": SOURCE_PATH,
                  "resource_id": RESOURCE, "rights_component_id": COMPOSITE_RIGHTS,
                  "role": "canonical_reader_source", "sha256": SOURCE_SHA})
    add("assets.jsonl", asset)
    diagram_asset = common("asset", "asset:o012-u029-semantic-diagram-layer")
    diagram_asset.update({"bytes": SOURCE_BYTES, "edition_id": EDITION,
                          "media_type": "text/markdown; charset=utf-8", "path": SOURCE_PATH,
                          "resource_id": RESOURCE, "rights_component_id": COMPANION_RIGHTS,
                          "role": "semantic_diagram_layer", "sha256": SOURCE_SHA,
                          "source_format_counts": {"tikz": 1, "xypic": 4},
                          "semantic_unit_ids": [f"unit:{ident}" for ident in DIAGRAMS]})
    add("assets.jsonl", diagram_asset)

    for slug, (source_term, preferred, evidence, _domain) in NEW_TERMS.items():
        term = common("term", f"term:{slug}:id-ID")
        term.update({"concept_id": f"concept:{slug}", "evidence_segment_id": f"segment:{evidence}",
                     "locale": "id-ID", "preferred": preferred, "register": "textbook",
                     "rejected_forms": [], "rights_component_id": COMPOSITE_RIGHTS,
                     "scope_unit_id": ROOT, "source_term": source_term,
                     "terminology_status": "unit_attested_reviewed",
                     "usage_note": "Attested in the independently reviewed Unit 29 reader and its preferred-term control QA.",
                     "variants": []})
        add("terms.jsonl", term)

    for ident, (correction_type, evidence, suffixes, defect, change, rationale) in CORRECTIONS.items():
        targets = [ROOT if suffix == "__root__" else f"unit:o012-rbt-l29-{suffix}"
                   for suffix in suffixes]
        if any(target != ROOT and target.removeprefix("unit:") not in spans for target in targets):
            raise SystemExit(f"correction target absent: {ident}")
        correction = common("correction", ident)
        correction.update({"affected_unit_ids": targets, "correction_type": correction_type,
                           "edition_id": EDITION, "evidence": evidence,
                           "evidence_segment_id": "segment:o012-rbt-l29-notice",
                           "rationale": rationale, "resource_id": RESOURCE,
                           "source_defect": defect, "target_change": change, "unit_id": ROOT,
                           "upstream_report_disposition": "not_contacted"})
        add("corrections.jsonl", correction)

    for ident, (relative, size, expected_sha, media_type, state, qa_ids) in EVIDENCE.items():
        artifact = common("artifact", ident)
        artifact.update({"bytes": size, "locale": "id-ID", "manifest_artifact_id": None,
                         "media_type": media_type, "path": relative, "qa_event_ids": qa_ids,
                         "rights_component_id": COMPOSITE_RIGHTS, "sha256": expected_sha,
                         "toolchain": (f"Bounded Unit 29 evidence; Notes.tex:6053-6270 span "
                                       f"{UPSTREAM_SPAN_SHA}; {MODEL}; route {ROUTE}; "
                                       "no cumulative build/publication assertion."),
                         "translation_state": state, "unit_id": ROOT})
        add("artifacts.jsonl", artifact)

    qa_specs = (
        ("qa:o012-u029-source-integrity", "source",
         "Unit 29 authority and reader identities, 49 stable IDs including the root, source label, five source diagrams, census, and native-MathML structure passed.",
         ["artifact:o012-u029-source-audit", "artifact:o012-u029-qa"]),
        ("qa:o012-u029-math", "math",
         "Independent Unit 29 mathematical review passed with no open P1, P2, or P3 finding and four complete proof objects.",
         ["artifact:o012-u029-independent-review"]),
        ("qa:o012-u029-language", "language",
         "Independent Indonesian review passed after all eight findings, including the audit-only terminology and structural-census findings, were resolved.",
         ["artifact:o012-u029-independent-review", "artifact:o012-u029-qa"]),
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

    relation("relation:adapts:o012-rbt-u029:edition", ROOT, "adapts", EDITION,
             "Unit 29 is the Indonesian adapted reader boundary for the frozen Roberts edition.")
    relation("relation:precedes:o012-rbt-u028:o012-rbt-u029", "unit:o012-rbt-u028",
             "precedes", ROOT, "Preserves contiguous Roberts lecture-unit order.")
    relation("relation:precedes:o012-rbt-l29:mastery", LECTURE, "precedes", MASTERY,
             "Lecture content precedes the six edition-original mastery items.")
    relation("relation:boundary:o012-u029", CUMULATIVE_RIGHTS, "contains", ROOT,
             "Additive cumulative Units 001-029 semantic source boundary.")
    relation("relation:route:d60-r14:o012-rbt-u029", COURSE, "contains", ROOT,
             "Roberts Lecture 29 is an edition unit in the non-destructive D60-R14 route view.",
             course_route_unit_id=ROUTE, edition_unit_id=ROOT)
    relation("relation:depends-on:o012-rbt-l29-s01:l28-s05", "unit:o012-rbt-l29-s01",
             "depends-on", "unit:o012-rbt-l28-s05", "Naturality extends the canonical Unit 28 restriction map.")
    relation("relation:depends-on:o012-rbt-l29-fact-001:l28-thm-002", "unit:o012-rbt-l29-fact-001",
             "depends-on", "unit:o012-rbt-l28-thm-002", "The relative factor uses quotient-pair cohomology.")
    relation("relation:depends-on:o012-rbt-l29-thm-001:fact-001", "unit:o012-rbt-l29-thm-001",
             "depends-on", "unit:o012-rbt-l29-fact-001", "The Five Lemma proof uses relative comparison.")
    relation("relation:depends-on:o012-rbt-l29-cor-001:thm-001", "unit:o012-rbt-l29-cor-001",
             "depends-on", "unit:o012-rbt-l29-thm-001", "Skeleton stabilization reduces to finite dimension.")
    relation("relation:depends-on:o012-rbt-l29-def-002:def-001", "unit:o012-rbt-l29-def-002",
             "depends-on", "unit:o012-rbt-l29-def-001", "A CW pair selects a CW subcomplex.")
    relation("relation:depends-on:o012-rbt-l29-thm-002:def-002", "unit:o012-rbt-l29-thm-002",
             "depends-on", "unit:o012-rbt-l29-def-002", "The axiom system is typed on the homotopy category of CW pairs.")
    relation("relation:reflows:o012-rbt-l29-fig-001:diagram-asset", "unit:o012-rbt-l29-fig-001",
             "illustrates", "asset:o012-u029-semantic-diagram-layer",
             "The semantic figure is one component of the five-diagram accessibility layer.")
    proof_targets = {1: "unit:o012-rbt-l29-lem-001", 2: "unit:o012-rbt-l29-fact-001",
                     3: "unit:o012-rbt-l29-thm-001", 4: "unit:o012-rbt-l29-cor-001"}
    for number, target in proof_targets.items():
        relation(f"relation:proves:o012-rbt-l29-proof-{number:03d}:closure",
                 f"unit:o012-rbt-l29-proof-{number:03d}", "proves", target,
                 f"Complete proof closure {number} for Unit 29.")
    for number in range(1, 7):
        relation(f"relation:solves:l29-sol-{number:03d}:l29-mcheck-{number:03d}",
                 f"unit:o012-rbt-l29-sol-{number:03d}", "solves",
                 f"unit:o012-rbt-l29-mcheck-{number:03d}",
                 f"Complete checked solution for Unit 29 mastery check {number}.")
        relation(f"relation:hints:l29-hint-{number:03d}:l29-mcheck-{number:03d}",
                 f"unit:o012-rbt-l29-hint-{number:03d}", "hints",
                 f"unit:o012-rbt-l29-mcheck-{number:03d}",
                 f"Bounded hint for Unit 29 mastery check {number}.")

    merged = {name: dict(tables[name]) for name in FILES}
    for name in FILES: merged[name].update(additions[name])
    by_id = {ident: obj for table in merged.values() for ident, obj in table.items()}
    if len(by_id) != sum(len(table) for table in merged.values()): raise SystemExit("global duplicate IDs")
    records = [obj for name in FILES for obj in merged[name].values()]
    generic = load_generic(); generic.validate_shapes(records)
    generic.validate_references(records, by_id); generic.validate_artifact_manifests(records, LANE)

    for ident in EXPECTED_ANCHORS:
        unit = by_id[f"unit:{ident}"]; segment = by_id[f"segment:{ident}"]
        if unit["target_locator"] != segment["target_locator"]: raise SystemExit(f"locator mismatch: {ident}")
        if unit["path"][-1] != unit["id"]: raise SystemExit(f"path mismatch: {ident}")
        if unit["parent_id"].startswith("unit:") and unit["path"][:-1] != by_id[unit["parent_id"]]["path"]:
            raise SystemExit(f"parent path mismatch: {ident}")
        for obj in (unit, segment):
            if (obj["edition_unit_id"] != ROOT or obj["course_route_unit_id"] != ROUTE
                    or obj["model_provenance"] != MODEL): raise SystemExit(f"route mismatch: {ident}")
    sibling: defaultdict[str, list[int]] = defaultdict(list)
    for obj in additions["units.jsonl"].values(): sibling[obj["parent_id"]].append(obj["order"])
    if any(len(values) != len(set(values)) for values in sibling.values()): raise SystemExit("duplicate order")
    for number in range(1, 7):
        check = f"unit:o012-rbt-l29-mcheck-{number:03d}"
        solves = [obj for obj in additions["relations.jsonl"].values()
                  if obj["relation_type"] == "solves" and obj["to_id"] == check]
        hints = [obj for obj in additions["relations.jsonl"].values()
                 if obj["relation_type"] == "hints" and obj["to_id"] == check]
        if len(solves) != 1 or len(hints) != 1: raise SystemExit(f"mastery mismatch: {number}")
    if len([obj for obj in additions["units.jsonl"].values() if obj.get("proof_status")]) != 4:
        raise SystemExit("four-proof closure mismatch")
    if len(additions["corrections.jsonl"]) != 19: raise SystemExit("correction dossier mismatch")
    if additions["rights.jsonl"][CUMULATIVE_RIGHTS]["component_scope"] != [
            f"unit:o012-rbt-u{number:03d}" for number in range(1, 30)]:
        raise SystemExit("cumulative rights mismatch")
    if by_id["unit:o012-rbt-l29-boundary-001"].get("next_source_line") != NEXT_SOURCE_LINE:
        raise SystemExit("terminal cursor mismatch")
    aliases = {alias: unit["id"] for unit in additions["units.jsonl"].values()
               for alias in unit.get("source_aliases", [])}
    if aliases != {"eq:comparison_iso_simplicial_singular": "unit:o012-rbt-l29-cor-001"}:
        raise SystemExit("source alias mismatch")
    if sum(obj.get("source_diagram_count", 0) for obj in additions["units.jsonl"].values()) != 5:
        raise SystemExit("diagram census mismatch")
    expected_findings = {"UNIT029-MATH-P2-001", "UNIT029-MATH-P2-002",
                         "UNIT029-TYPE-P2-003", "UNIT029-REFLOW-P3-001",
                         "UNIT029-CW-P3-002", "UNIT029-LANG-P3-003",
                         "UNIT029-TERM-P3-004", "UNIT029-QA-P3-005"}
    if {item.get("finding_id") for item in qa_doc["resolved_findings"]} != expected_findings:
        raise SystemExit("resolved finding set changed")

    outputs: dict[str, bytes] = {}
    for name in FILES:
        if (BACKEND / name).read_bytes() != prefix_raw[name]: raise SystemExit(f"prefix changed: {name}")
        suffix = b"".join(canon(additions[name][ident]) for ident in sorted(additions[name]))
        outputs[name] = prefix_raw[name] + suffix
    for name, generated in outputs.items(): (BACKEND / name).write_bytes(generated)
    bundle = hashlib.sha256()
    for name in FILES:
        bundle.update(name.encode()); bundle.update(b"\0"); bundle.update(outputs[name])
    counts = {name: len(additions[name]) for name in FILES}
    print("Unit 029 semantic backend extension: PASS")
    print("new_records_by_file=" + json.dumps(counts, sort_keys=True))
    print(f"new_records={sum(counts.values())}")
    print(f"total_records={sum(PREFIX[name][0] + counts[name] for name in FILES)}")
    print(f"backend_bytes={sum(len(item) for item in outputs.values())}")
    print(f"backend_bundle_sha256={bundle.hexdigest()}")
    for name in FILES:
        print(f"file={name} records={PREFIX[name][0] + counts[name]} bytes={len(outputs[name])} sha256={digest(outputs[name])}")
    print(f"source_sha256={SOURCE_SHA}"); print(f"upstream_span_sha256={UPSTREAM_SPAN_SHA}")
    print("actual_stable_ids=49"); print("qa_declared_stable_ids=49")
    print("proof_closures=4"); print("mastery_triples=6")
    print("source_aliases=1"); print("resolved_findings=8"); print("source_diagrams=5")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
