#!/usr/bin/env python3
"""Fail-closed append-only semantic-backend admission for Roberts Unit 030."""
from __future__ import annotations

import hashlib
import importlib.util
import csv
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

LANE = Path(__file__).resolve().parents[1]
BACKEND = LANE / "backend"
SOURCE = LANE / "source/id-ID/units/unit-030-lecture-030.md"
UPSTREAM = (LANE / "authority/upstream" /
            "AlgebraicTopology2019-b947ad2e9f9e301bfe24590a9db653bc54fa1a53" /
            "Notes.tex")
AUDIT = LANE / "qa/UNIT_030_SOURCE_AUDIT.md"
REVIEW = LANE / "qa/UNIT_030_INDEPENDENT_REVIEW.md"
QA_JSON = LANE / "qa/UNIT_030_QA.json"
ADVERSE_LEDGER = LANE / "00_control/ADVERSE_LEDGER.csv"
TERMINOLOGY = LANE / "00_control/TERMINOLOGY.csv"
ADVERSE_IDENTITY = (127715, 408,
                    "30345e976fa973343e285295695454a873b8692e70f415dc7c3d009d0ca73375")
TERMINOLOGY_IDENTITY = (42186, 366,
                       "234f984b06a1a0f55679a1f0f283bd5592cb7b96e696c64ca667bc62fcd4258c")

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
COMPANION_RIGHTS = "rights:o012-u030-companion-cc-by-4.0"
COMPOSITE_RIGHTS = "rights:o012-u030-composite-cc-by-4.0"
CUMULATIVE_RIGHTS = "rights:o012-units-001-030-composite-cc-by-4.0"
PRIOR_RIGHTS = "rights:o012-units-001-029-composite-cc-by-4.0"
ROOT = "unit:o012-rbt-u030"
LECTURE = "unit:o012-rbt-l30"
MASTERY = "unit:o012-rbt-l30-mastery"
SOURCE_PATH = "source/id-ID/units/unit-030-lecture-030.md"
SOURCE_BYTES = 23008
SOURCE_LINES = 729
SOURCE_SHA = "88da8cf71d0f81328bdd65b0dea7d54c48655ed8836e230eaed821796b61b08d"
UPSTREAM_BYTES = 331447
UPSTREAM_LINES = 6368
UPSTREAM_SHA = "cfe93e9dbe3e25bd96f711f59e6078ab97527682b58e1f8ad127f74357f665d7"
UPSTREAM_START = 6271
UPSTREAM_END = 6368
UPSTREAM_SPAN_BYTES = 8290
UPSTREAM_SPAN_SHA = "c522b5ec0ba7d4c938be6588a070be648263d841e1db4f9905c9b388619b64b1"
NEXT_SOURCE_LINE = 6369

FILES = ("artifacts.jsonl", "assets.jsonl", "authority.jsonl", "concepts.jsonl",
         "corrections.jsonl", "qa.jsonl", "relations.jsonl", "rights.jsonl",
         "segments.jsonl", "terms.jsonl", "units.jsonl")
PREFIX = {
    "artifacts.jsonl": (157, 125783, "11f677dc347348b8a91387e232b7eb18cbada0387d4eddda4f95a113ed241dc1"),
    "assets.jsonl": (32, 19939, "bd81863dd4eff456734abada1f2416727b70a5c54c7e9662a5cb2bac041884bb"),
    "authority.jsonl": (4, 2721, "f21af26912520ab34b38dff0e927ed46a546dbe5d318da0dc133e58330d0e368"),
    "concepts.jsonl": (354, 111822, "edd155b71045f574d4195af88d021c82a2c530e46fc6b61046276a783649f041"),
    "corrections.jsonl": (397, 387613, "82145855c9dec1c14f1be23bdf36394f0249798b7722c9ebd65afefd955ecfb4"),
    "qa.jsonl": (131, 73522, "10c3b5955c4c5a5f4f93d18a360705c0ee74286467d09e1549432c21b8c06c17"),
    "relations.jsonl": (504, 206282, "5a12459d1af20f6ba363f93c10104dedf714c24b8484c6f1b2a76004ddd2474f"),
    "rights.jsonl": (83, 76753, "6ab37eedf396adbd01ba4be763896d9a4926a0fc87af97d8ac2ad2022c3d35e1"),
    "segments.jsonl": (1279, 1829093, "13f59fd6db9e768c4d4b1a249bfcf86ccdb4312df5a74fadb53922266d985bdc"),
    "terms.jsonl": (347, 219627, "d16fc5166ee92ea654eb43b644dda4cb7acc59054194654b8e85b7bcdd3a1aa9"),
    "units.jsonl": (1308, 1948111, "19b50f4cee0cc968b538052ffaf87d7b2dc2199b64c44e1a12c4e4800dc99e04"),
}
PREFIX_RECORDS = 4596
PREFIX_BYTES = 5001266
PREFIX_BUNDLE = "49c599010ebee2223225f643cd09a53bea882b8064024d5189e6e15f648195d8"

EVIDENCE = {
    "artifact:o012-u030-source-audit": (
        "qa/UNIT_030_SOURCE_AUDIT.md", 7214,
        "177c4306e5db636e0294e85278904c186099d069f209474a472d2615b0d5a4cf",
        "text/markdown; charset=utf-8", "source_frozen",
        ["qa:o012-u030-source-integrity"]),
    "artifact:o012-u030-independent-review": (
        "qa/UNIT_030_INDEPENDENT_REVIEW.md", 8406,
        "58db70bbd6538961e8bfc0c809d00b7b539115147b2826dc46d97e5b77ba712e",
        "text/markdown; charset=utf-8", "mathematically_reviewed",
        ["qa:o012-u030-math", "qa:o012-u030-language"]),
    "artifact:o012-u030-qa": (
        "qa/UNIT_030_QA.json", 8378,
        "bef6fe6704084ac02386bb477b7b0082e02921d3d722955e1366e7d0b9247753",
        "application/json", "built",
        ["qa:o012-u030-source-integrity", "qa:o012-u030-language"]),
}

EXPECTED_ANCHORS = (
    "o012-rbt-l30-notice", "o012-rbt-l30", "o012-rbt-l30-s01",
    "o012-rbt-l30-s02", "o012-rbt-l30-aside-001",
    "o012-rbt-l30-def-001", "o012-rbt-l30-thm-001",
    "o012-rbt-l30-proof-001", "o012-rbt-l30-fig-001",
    "o012-rbt-l30-audit-001", "o012-rbt-l30-rem-001",
    "o012-rbt-l30-s03", "o012-rbt-l30-aside-002",
    "o012-rbt-l30-thm-002", "o012-rbt-l30-proof-002",
    "o012-rbt-l30-audit-002", "o012-rbt-l30-s04",
    "o012-rbt-l30-aside-003", "o012-rbt-l30-thm-003",
    "o012-rbt-l30-def-002", "o012-rbt-l30-prop-001",
    "o012-rbt-l30-lem-001", "o012-rbt-l30-aside-004",
    "o012-rbt-l30-cor-001", "o012-rbt-l30-proof-003",
    "o012-rbt-l30-proof-004", "o012-rbt-l30-audit-003",
    "o012-rbt-l30-mastery", "o012-rbt-l30-mcheck-001",
    "o012-rbt-l30-hint-001", "o012-rbt-l30-sol-001",
    "o012-rbt-l30-mcheck-002", "o012-rbt-l30-hint-002",
    "o012-rbt-l30-sol-002", "o012-rbt-l30-mcheck-003",
    "o012-rbt-l30-hint-003", "o012-rbt-l30-sol-003",
    "o012-rbt-l30-mcheck-004", "o012-rbt-l30-hint-004",
    "o012-rbt-l30-sol-004", "o012-rbt-l30-mcheck-005",
    "o012-rbt-l30-hint-005", "o012-rbt-l30-sol-005",
    "o012-rbt-l30-mcheck-006", "o012-rbt-l30-hint-006",
    "o012-rbt-l30-sol-006", "o012-rbt-l30-boundary-001",
)
SOURCE_RANGES = {
    "o012-rbt-l30": (6271, 6368), "o012-rbt-l30-s01": (6271, 6271),
    "o012-rbt-l30-s02": (6273, 6306), "o012-rbt-l30-aside-001": (6273, 6273),
    "o012-rbt-l30-def-001": (6273, 6273), "o012-rbt-l30-thm-001": (6275, 6277),
    "o012-rbt-l30-proof-001": (6279, 6302), "o012-rbt-l30-rem-001": (6304, 6306),
    "o012-rbt-l30-s03": (6308, 6316), "o012-rbt-l30-aside-002": (6308, 6308),
    "o012-rbt-l30-thm-002": (6310, 6312), "o012-rbt-l30-proof-002": (6314, 6316),
    "o012-rbt-l30-s04": (6318, 6365), "o012-rbt-l30-aside-003": (6318, 6318),
    "o012-rbt-l30-thm-003": (6320, 6322), "o012-rbt-l30-def-002": (6327, 6329),
    "o012-rbt-l30-prop-001": (6331, 6338), "o012-rbt-l30-lem-001": (6340, 6342),
    "o012-rbt-l30-aside-004": (6344, 6344), "o012-rbt-l30-cor-001": (6346, 6348),
    "o012-rbt-l30-proof-004": (6350, 6365),
}
DIAGRAMS = {
    "o012-rbt-l30-fig-001": (["tikz"], 1),
}
SOURCE_ALIASES = {"o012-rbt-l30-thm-003": ["thm:hairy_sphere"]}

NEW_TERMS = {
    "free-self-map": ("free self-map", "fungsi-diri bebas", "o012-rbt-l30-def-001", "algebraic_topology", "O012-TERM-0356", "continuous self-map with no fixed point"),
    "brouwer-fixed-point-theorem": ("Brouwer fixed-point theorem", "teorema titik tetap Brouwer", "o012-rbt-l30-thm-001", "algebraic_topology", "O012-TERM-0357", "retain the proper name and use titik tetap for fixed point"),
    "real-closed-field": ("real-closed field", "medan tertutup-real", "o012-rbt-l30-aside-002", "algebra", "O012-TERM-0358", "hyphenation distinguishes the compound mathematical property"),
    "fundamental-theorem-of-algebra": ("fundamental theorem of algebra", "teorema dasar aljabar", "o012-rbt-l30-thm-002", "algebra", "O012-TERM-0359", "the monic nonconstant complex-polynomial root theorem in Unit 30"),
    "tangent-vector-field": ("tangent vector field", "medan vektor tangen", "o012-rbt-l30-s04", "differential_topology", "O012-TERM-0360", "distinguish the tangent fibre from the ambient unit-sphere target used in the proof"),
    "dot-product": ("dot product", "hasil kali titik", "o012-rbt-l30-proof-004", "linear_algebra", "O012-TERM-0361", "Euclidean inner product in the coordinate tangency check"),
    "degree-of-a-map": ("degree of a map", "derajat pemetaan", "o012-rbt-l30-def-002", "algebraic_topology", "O012-TERM-0362", "defined here by the scalar action on reduced top cohomology"),
    "antipodal-map": ("antipodal map", "peta antipodal", "o012-rbt-l30-cor-001", "algebraic_topology", "O012-TERM-0363", "map x to -x on a sphere"),
    "monoid-homomorphism": ("monoid homomorphism", "homomorfisma monoid", "o012-rbt-l30-prop-001", "algebra", "O012-TERM-0364", "degree sends composition to multiplication"),
    "hairy-sphere-theorem": ("hairy sphere theorem", "teorema sfera berbulu", "o012-rbt-l30-thm-003", "algebraic_topology", "O012-TERM-0365", "use sfera rather than bola because the theorem concerns S^n"),
}
REUSED_CONCEPTS = (
    "concept:reduced-cohomology", "concept:homotopy", "concept:disk",
    "concept:fundamental-group", "concept:covering-map", "concept:retract",
    "concept:homotopy-invariance",
)

CORRECTIONS = {
    "correction:o012-u030-adv-0398": ("O012-ADV-0398", "mathematical_correction", "Notes.tex:6273", ["s02", "audit-001"], "A function constant on a small region is claimed to have many fixed points.", "Replace it with a function equal to the identity on that region.", "An identity region supplies the intended family of fixed points."),
    "correction:o012-u030-adv-0399": ("O012-ADV-0399", "proof_completion", "Notes.tex:6279-6301", ["proof-001", "fig-001", "audit-001"], "The Brouwer argument omits the free-map contradiction hypothesis and reverses unreduced cohomology arrows.", "State the free-map hypothesis, construct the continuous outward retraction, and use reduced cohomology contravariantly.", "The proof is defined and valid for n equals zero and one as well as higher dimensions."),
    "correction:o012-u030-adv-0400": ("O012-ADV-0400", "omitted_hypothesis", "Notes.tex:6308", ["aside-002", "audit-002"], "The real-closed-field characterization omits that every positive element is a square.", "State the ordering, positive-square, and odd-degree-root conditions before adjoining square root of minus one.", "The algebraic-closure remark uses the standard complete characterization."),
    "correction:o012-u030-adv-0401": ("O012-ADV-0401", "proof_completion", "Notes.tex:6314-6316", ["proof-002", "audit-002"], "The large-circle polynomial comparison is informal and concludes with contraction instead of contradiction.", "Choose an explicit leading-term bound and apply the reverse triangle inequality throughout the straight-line homotopy.", "The homotopy remains in the nonzero complex numbers and yields the intended contradiction."),
    "correction:o012-u030-adv-0402": ("O012-ADV-0402", "clarification", "Notes.tex:6318", ["s04", "audit-003"], "Translation of the unit tangent vector can be misread as Euclidean translation.", "Identify it as left translation in the circle group and retain the coordinate rotation formula.", "The group operation is explicit without changing the mathematics."),
    "correction:o012-u030-adv-0403": ("O012-ADV-0403", "mathematical_correction", "Notes.tex:6324-6329", ["s04", "def-002", "audit-003"], "The tangent-fibre unit sphere is conflated with the ambient target and degree uses ordinary cohomology at n equals zero.", "Distinguish fibre and ambient spheres and define degree with reduced cohomology.", "Dimensions and degree are correct uniformly for every nonnegative n."),
    "correction:o012-u030-adv-0404": ("O012-ADV-0404", "mathematical_correction", "Notes.tex:6358-6362", ["proof-004", "audit-003"], "The odd-dimensional field has a malformed terminal index and claims dot product one.", "Use x sub 2k minus 1 and verify dot product zero and norm one pairwise.", "The displayed formula is tangent, unit length, and never zero."),
    "correction:o012-u030-adv-0405": ("O012-ADV-0405", "source_typo", "Notes.tex:6297,6301,6324,6351,6356", ["proof-001", "s04", "proof-004"], "Several deterministic spelling, grammar, and sphere-notation defects interrupt the source.", "Normalize the spelling, prose, and S superscript n notation without changing content.", "The edition is readable and mathematically unchanged at those sites."),
    "correction:o012-u030-adv-0406": ("O012-ADV-0406", "mathematical_correction", "UNIT030-ED-P2-001", ["sol-004"], "The pre-admission degree-multiplicativity solution wrote scalar multiplication ambiguously as ed comma u.", "Write the scalar action as open-parenthesis ed close-parenthesis u.", "The product of degrees is unambiguous and contravariant composition is preserved."),
    "correction:o012-u030-adv-0407": ("O012-ADV-0407", "metadata_correction", "O012-ADV-0407", ["__root__"], "The initial QA census omitted the notice and lecture-root heading IDs and reported 46 IDs.", "Bind 47 explicit unique IDs across seven identified headings and 40 fenced objects.", "All machine-addressable reader structures are preserved without changing reader bytes."),
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
    spec = importlib.util.spec_from_file_location("o012_generic_u030_producer", path)
    if spec is None or spec.loader is None:
        raise SystemExit("cannot load generic backend validator")
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


def load_prefix() -> tuple[dict[str, dict[str, dict[str, Any]]], dict[str, bytes]]:
    tables: dict[str, dict[str, dict[str, Any]]] = {}
    raw_files: dict[str, bytes] = {}
    seen: set[str] = set(); bundle = hashlib.sha256()
    for name in FILES:
        full_raw = (BACKEND / name).read_bytes(); count, size, expected_sha = PREFIX[name]
        if len(full_raw) < size:
            raise SystemExit(f"{name}: shorter than immutable Units 001-029 prefix")
        raw = full_raw[:size]
        lines = raw.splitlines(keepends=True)
        if (len(raw), len(lines), digest(raw)) != (size, count, expected_sha):
            raise SystemExit(f"{name}: immutable Units 001-029 prefix mismatch")
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
        raise SystemExit("Units 001-029 backend bundle identity mismatch")
    if not {"unit:o012-rbt-u029", PRIOR_RIGHTS,
            "artifact:o012-u029-independent-review"} <= seen:
        raise SystemExit("Unit 29 prefix closure is incomplete")
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
        raise SystemExit("Unit 30 upstream span mismatch")
    if ("\\lecturenum{30}" not in lines[6270]
            or lines[6367].strip() != "\\end{document}"
            or len(lines) != UPSTREAM_LINES + 1):
        raise SystemExit("Unit 30 source boundary identity mismatch")


def structural_spans(lines: list[str]) -> dict[str, tuple[int, int, str]]:
    opening = re.compile(r"^\s*:::\s+\{[^#}]*#(o012-rbt-l30(?:-[A-Za-z0-9-]+)?)(.*)\}\s*$")
    heading = re.compile(r"^#{1,6}\s+.*\{[^}]*#(o012-rbt-l30(?:-[A-Za-z0-9-]+)?)[^}]*\}\s*$")
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
        "o012-rbt-l30-notice": (12, 50), "o012-rbt-l30": (51, 511),
        "o012-rbt-l30-s01": (53, 61), "o012-rbt-l30-s02": (62, 205),
        "o012-rbt-l30-s03": (206, 306), "o012-rbt-l30-s04": (307, 511),
        "o012-rbt-l30-mastery": (512, 723),
    }
    for ident, (start, end) in headings.items():
        if ident not in lines[start - 1]: raise SystemExit(f"heading mismatch: {ident}")
        spans[ident] = (start, end, lines[start - 1])
    if tuple(ordered) != EXPECTED_ANCHORS or set(spans) != set(EXPECTED_ANCHORS):
        raise SystemExit("Unit 30 stable-ID inventory/order mismatch")
    return spans


def unit_kind(ident: str, opener: str) -> str:
    if ident.endswith("-notice"): return "notice"
    if ident == "o012-rbt-l30": return "lecture"
    if ident.endswith("-mastery"): return "mastery_section"
    if re.fullmatch(r"o012-rbt-l30-s\d{2}", ident): return "section"
    match = re.search(r"\{\.([A-Za-z][A-Za-z0-9_-]*)", opener)
    kind = match.group(1).replace("source-audit", "source_audit") if match else ""
    allowed = {"aside", "boundary", "corollary", "definition", "example",
               "exercise", "fact", "figure", "hint", "lemma", "proof",
               "proposition", "remark", "solution", "source_audit", "theorem"}
    if kind not in allowed: raise SystemExit(f"cannot infer kind for {ident}: {kind!r}")
    return kind


def provenance(ident: str, kind: str, opener: str) -> tuple[str, str, bool]:
    if (kind in {"notice", "source_audit", "mastery_section", "boundary",
                 "hint", "solution", "figure"}
            or 'data-origin="edition-original"' in opener
            or "-mcheck-" in ident or ident == "o012-rbt-l30-exa-003"):
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
    return f"Unit 30 {kind} {ident.rsplit('-', 1)[-1]}"


def verify_controls() -> None:
    adverse_raw = ADVERSE_LEDGER.read_bytes()
    terminology_raw = TERMINOLOGY.read_bytes()
    if (len(adverse_raw), len(adverse_raw.splitlines()), digest(adverse_raw)) != ADVERSE_IDENTITY:
        raise SystemExit("Unit 30 adverse-ledger identity mismatch")
    if (len(terminology_raw), len(terminology_raw.splitlines()), digest(terminology_raw)) != TERMINOLOGY_IDENTITY:
        raise SystemExit("Unit 30 terminology-control identity mismatch")
    adverse_rows = list(csv.DictReader(adverse_raw.decode("utf-8-sig").splitlines()))
    terminology_rows = list(csv.DictReader(terminology_raw.decode("utf-8-sig").splitlines()))
    adverse_by_id = {row["event_id"]: row for row in adverse_rows}
    term_by_id = {row["term_id"]: row for row in terminology_rows}
    expected_adverse = {f"O012-ADV-{number:04d}" for number in range(398, 408)}
    if (adverse_rows[-1].get("event_id") != "O012-ADV-0407"
            or not expected_adverse <= set(adverse_by_id)
            or any(adverse_by_id[ident].get("status") not in {
                "corrected_in_translation", "clarified_in_translation",
                "resolved_before_admission"} for ident in expected_adverse)):
        raise SystemExit("Unit 30 adverse-ledger closure mismatch")
    for _slug, (source_term, preferred, _evidence, scope, control_id, note) in NEW_TERMS.items():
        row = term_by_id.get(control_id)
        if row is None or (row.get("source_term"), row.get("id_ID"), row.get("scope"),
                           row.get("status"), row.get("note")) != (
                source_term, preferred, scope, "admitted", note):
            raise SystemExit(f"Unit 30 terminology-control mismatch: {control_id}")
    if terminology_rows[-1].get("term_id") != "O012-TERM-0365":
        raise SystemExit("Unit 30 terminology endpoint mismatch")


def verify_evidence() -> dict[str, Any]:
    for _ident, (relative, size, expected_sha, _media, _state, _qas) in EVIDENCE.items():
        raw = (LANE / relative).read_bytes()
        if len(raw) != size or digest(raw) != expected_sha:
            raise SystemExit(f"Unit 30 evidence identity mismatch: {relative}")
    qa = json.loads(QA_JSON.read_text(encoding="utf-8"))
    expected = {"UNIT030-ED-P2-001", "UNIT030-QA-P3-002"}
    resolved = qa.get("resolved_findings")
    if (qa.get("status") != "PASS"
            or qa.get("source", {}).get("line_start") != UPSTREAM_START
            or qa.get("source", {}).get("line_end") != UPSTREAM_END
            or qa.get("source", {}).get("span_bytes") != UPSTREAM_SPAN_BYTES
            or qa.get("source", {}).get("span_sha256") != UPSTREAM_SPAN_SHA
            or qa.get("source", {}).get("next_nominal_line") != NEXT_SOURCE_LINE
            or not qa.get("source", {}).get("terminal_eof")
            or qa.get("unit", {}).get("bytes") != SOURCE_BYTES
            or qa.get("unit", {}).get("lines") != SOURCE_LINES
            or qa.get("unit", {}).get("sha256") != SOURCE_SHA
            or qa.get("unit", {}).get("stable_ids") != 47
            or qa.get("unit", {}).get("identified_headings") != 7
            or qa.get("unit", {}).get("fenced_semantic_objects") != 40
            or qa.get("proof_closure", {}).get("mastery_solution_triples") != 6
            or qa.get("model_provenance") != MODEL
            or not isinstance(resolved, list)
            or {item.get("finding_id") for item in resolved} != expected
            or any(item.get("status") != "RESOLVED_BEFORE_ADMISSION" for item in resolved)
            or any(item.get("status") != "PASS" for item in qa.get("checks", []))):
        raise SystemExit("Unit 30 QA content/binding mismatch")
    return qa


def main() -> int:
    tables, prefix_raw = load_prefix(); verify_upstream(); verify_controls()
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
            or not raw.endswith(b"\n")): raise SystemExit("Unit 30 reader identity/newline mismatch")
    raw_lines = raw.splitlines(keepends=True)
    lines = [line.decode("utf-8").rstrip("\n") for line in raw_lines]
    text = raw.decode("utf-8")
    if (len(lines) != SOURCE_LINES or text.count(MODEL) != 1
            or re.search(r"\b(funktor|funktorial|naturalitas|bola|perpanjangan)\b|bujur sangkar", text, re.IGNORECASE)):
        raise SystemExit("Unit 30 reader line/provenance/terminology mismatch")
    spans = structural_spans(lines)

    for slug, (source_term, _preferred, _evidence, domain, _control_id, _note) in NEW_TERMS.items():
        concept = common("concept", f"concept:{slug}")
        concept.update({"canonical_label": source_term, "domain": domain, "locale_neutral": True})
        add("concepts.jsonl", concept)
    concept_ids = list(REUSED_CONCEPTS) + [f"concept:{slug}" for slug in NEW_TERMS]
    if any(ident not in existing_ids and ident not in additions["concepts.jsonl"] for ident in concept_ids):
        raise SystemExit("Unit 30 concept closure mismatch")

    rights_specs = (
        (COMPANION_RIGHTS,
         "Indonesian original solutions, mastery, proof-completion, source-audit, and semantic diagram layer for Roberts Unit 30.",
         "Original additions are CC BY 4.0; source-derived material remains separately attributed.", [ROOT], None),
        (COMPOSITE_RIGHTS,
         "David Michael Roberts source adaptation plus original Indonesian Unit 30 companions.",
         "Translated, repaired, and original layers remain component-distinguishable.", [ROOT], None),
        (CUMULATIVE_RIGHTS,
         "Cumulative Roberts Units 001-030 Indonesian reader source boundary.",
         "Append-only semantic pointer; prior verified build artifacts remain immutable until separate build admission.",
         [f"unit:o012-rbt-u{number:03d}" for number in range(1, 31)], PRIOR_RIGHTS),
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

    section_ranges = (("o012-rbt-l30-s01", 53, 61), ("o012-rbt-l30-s02", 62, 205),
                      ("o012-rbt-l30-s03", 206, 306), ("o012-rbt-l30-s04", 307, 511))
    section_ids = {item[0] for item in section_ranges}

    def parent_local(ident: str, start: int) -> str:
        if ident in {"o012-rbt-l30-notice", "o012-rbt-l30", "o012-rbt-l30-mastery",
                     "o012-rbt-l30-boundary-001"}: return ROOT
        if ident in section_ids: return LECTURE
        if any(token in ident for token in ("-mcheck-", "-hint-", "-sol-")): return MASTERY
        for section, low, high in section_ranges:
            if low <= start <= high: return f"unit:{section}"
        raise SystemExit(f"cannot assign Unit 30 parent: {ident}")

    children: defaultdict[str, list[str]] = defaultdict(list)
    for ident in EXPECTED_ANCHORS: children[parent_local(ident, spans[ident][0])].append(ident)
    order_map = {parent: {ident: number for number, ident in enumerate(
        sorted(items, key=lambda item: spans[item][0]), 1)} for parent, items in children.items()}
    path_by_id: dict[str, list[str]] = {ROOT: [ROOT]}
    root = common("unit", ROOT)
    root.update({"component_source_commit": COMMIT, "component_source_id": RESOURCE,
                 "concept_ids": concept_ids, "course_id": COURSE, "course_route_unit_id": ROUTE,
                 "display_title": "Topologi Aljabar - Unit 30: Titik Tetap, Teorema Dasar Aljabar, dan Medan Vektor pada Sfera",
                 "edition_id": EDITION, "edition_unit_id": ROOT, "locale": "id-ID",
                 "model_provenance": MODEL, "order": 30, "parent_id": COURSE,
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
        aliases = re.findall(r'data-source-label="([^"]+)"', opener) + SOURCE_ALIASES.get(ident, [])
        if aliases: unit["source_aliases"] = aliases; segment["source_aliases"] = aliases
        if ident in DIAGRAMS:
            formats, count = DIAGRAMS[ident]
            for obj in (unit, segment):
                obj["source_formats"] = formats; obj["source_diagram_count"] = count
                obj["accessibility_status"] = "semantic_reflow"
        if ident == "o012-rbt-l30-boundary-001":
            unit["next_source_line"] = NEXT_SOURCE_LINE; segment["next_source_line"] = NEXT_SOURCE_LINE
            unit["terminal_source_eof"] = True; segment["terminal_source_eof"] = True
        if kind == "proof":
            status = "complete_original_proof" if edition_original else "complete_translated_proof"
            unit["proof_status"] = status; segment["proof_status"] = status
        if kind == "solution":
            unit["solution_status"] = "complete_checked_solution"
            segment["solution_status"] = "complete_checked_solution"
        add("units.jsonl", unit); add("segments.jsonl", segment)

    asset = common("asset", "asset:o012-u030-source-markdown")
    asset.update({"bytes": SOURCE_BYTES, "edition_id": EDITION,
                  "media_type": "text/markdown; charset=utf-8", "path": SOURCE_PATH,
                  "resource_id": RESOURCE, "rights_component_id": COMPOSITE_RIGHTS,
                  "role": "canonical_reader_source", "sha256": SOURCE_SHA})
    add("assets.jsonl", asset)
    diagram_asset = common("asset", "asset:o012-u030-semantic-diagram-layer")
    diagram_asset.update({"bytes": SOURCE_BYTES, "edition_id": EDITION,
                          "media_type": "text/markdown; charset=utf-8", "path": SOURCE_PATH,
                          "resource_id": RESOURCE, "rights_component_id": COMPANION_RIGHTS,
                          "role": "semantic_diagram_layer", "sha256": SOURCE_SHA,
                           "source_format_counts": {"tikz": 1, "xypic": 0},
                          "semantic_unit_ids": [f"unit:{ident}" for ident in DIAGRAMS]})
    add("assets.jsonl", diagram_asset)

    for slug, (source_term, preferred, evidence, _domain, control_id, usage_note) in NEW_TERMS.items():
        term = common("term", f"term:{slug}:id-ID")
        term.update({"concept_id": f"concept:{slug}", "evidence_segment_id": f"segment:{evidence}",
                     "locale": "id-ID", "preferred": preferred, "register": "textbook",
                     "rejected_forms": [], "rights_component_id": COMPOSITE_RIGHTS,
                     "scope_unit_id": ROOT, "source_term": source_term,
                     "terminology_control_id": control_id, "terminology_status": "admitted",
                     "usage_note": usage_note,
                     "variants": []})
        add("terms.jsonl", term)

    for ident, (adverse_id, correction_type, evidence, suffixes, defect, change, rationale) in CORRECTIONS.items():
        targets = [ROOT if suffix == "__root__" else f"unit:o012-rbt-l30-{suffix}"
                   for suffix in suffixes]
        if any(target != ROOT and target.removeprefix("unit:") not in spans for target in targets):
            raise SystemExit(f"correction target absent: {ident}")
        correction = common("correction", ident)
        correction.update({"adverse_ledger_id": adverse_id, "affected_unit_ids": targets,
                           "correction_type": correction_type,
                           "edition_id": EDITION, "evidence": evidence,
                           "evidence_segment_id": "segment:o012-rbt-l30-notice",
                           "rationale": rationale, "resource_id": RESOURCE,
                           "source_defect": defect, "target_change": change, "unit_id": ROOT,
                           "upstream_report_disposition": "not_contacted"})
        add("corrections.jsonl", correction)

    for ident, (relative, size, expected_sha, media_type, state, qa_ids) in EVIDENCE.items():
        artifact = common("artifact", ident)
        artifact.update({"bytes": size, "locale": "id-ID", "manifest_artifact_id": None,
                         "media_type": media_type, "path": relative, "qa_event_ids": qa_ids,
                         "rights_component_id": COMPOSITE_RIGHTS, "sha256": expected_sha,
                         "toolchain": (f"Bounded Unit 30 evidence; Notes.tex:6271-6368 terminal span "
                                       f"{UPSTREAM_SPAN_SHA}; {MODEL}; route {ROUTE}; "
                                       "no cumulative build/publication assertion."),
                         "translation_state": state, "unit_id": ROOT})
        add("artifacts.jsonl", artifact)

    qa_specs = (
        ("qa:o012-u030-source-integrity", "source",
         "Unit 30 terminal authority and reader identities, 47 explicit stable IDs across seven headings and 40 fenced objects, one source label, one TikZ semantic reflow, census, and native-MathML structure passed.",
         ["artifact:o012-u030-source-audit", "artifact:o012-u030-qa"]),
        ("qa:o012-u030-math", "math",
         "Independent Unit 30 mathematical review passed with no open P1, P2, or P3 finding and four complete proof objects.",
         ["artifact:o012-u030-independent-review"]),
        ("qa:o012-u030-language", "language",
         "Independent Indonesian review passed after both pre-admission findings, including the structural-census finding, were resolved.",
         ["artifact:o012-u030-independent-review", "artifact:o012-u030-qa"]),
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

    relation("relation:adapts:o012-rbt-u030:edition", ROOT, "adapts", EDITION,
             "Unit 30 is the Indonesian adapted reader boundary for the frozen Roberts edition.")
    relation("relation:precedes:o012-rbt-u029:o012-rbt-u030", "unit:o012-rbt-u029",
             "precedes", ROOT, "Preserves contiguous Roberts lecture-unit order.")
    relation("relation:precedes:o012-rbt-l30:mastery", LECTURE, "precedes", MASTERY,
             "Lecture content precedes the six edition-original mastery items.")
    relation("relation:boundary:o012-u030", CUMULATIVE_RIGHTS, "contains", ROOT,
             "Additive cumulative Units 001-030 semantic source boundary.")
    relation("relation:route:d60-r14:o012-rbt-u030", COURSE, "contains", ROOT,
             "Roberts Lecture 30 is an edition unit in the non-destructive D60-R14 route view.",
             course_route_unit_id=ROUTE, edition_unit_id=ROOT)
    relation("relation:depends-on:o012-rbt-l30-s02:l12-retract", "unit:o012-rbt-l30-s02",
             "depends-on", "unit:o012-rbt-l12-def-001", "The Brouwer contradiction constructs a retraction of the disk onto its boundary.")
    relation("relation:depends-on:o012-rbt-l30-proof-001:l25-reduced", "unit:o012-rbt-l30-proof-001",
             "depends-on", "unit:o012-rbt-l25-def-002", "Reduced cohomology closes the low-dimensional Brouwer cases.")
    relation("relation:depends-on:o012-rbt-l30-proof-002:l10-pi1", "unit:o012-rbt-l30-proof-002",
             "depends-on", "unit:o012-rbt-l10-thm-001", "The polynomial winding obstruction uses the fundamental group of the punctured plane.")
    relation("relation:depends-on:o012-rbt-l30-def-002:l25-reduced", "unit:o012-rbt-l30-def-002",
             "depends-on", "unit:o012-rbt-l25-def-002", "Degree is normalized through reduced top cohomology, including S zero.")
    relation("relation:depends-on:o012-rbt-l30-thm-003:l29-axioms", "unit:o012-rbt-l30-thm-003",
             "depends-on", "unit:o012-rbt-l29-thm-002", "The obstruction uses homotopy invariance and reduced cohomology from the axiomatic theory.")
    relation("relation:depends-on:o012-rbt-l30-cor-001:lem-001", "unit:o012-rbt-l30-cor-001",
             "depends-on", "unit:o012-rbt-l30-lem-001", "The antipodal degree is the product of coordinate-reflection degrees.")
    relation("relation:depends-on:o012-rbt-l30-proof-004:cor-001", "unit:o012-rbt-l30-proof-004",
             "depends-on", "unit:o012-rbt-l30-cor-001", "The even-dimensional obstruction compares identity and antipodal degrees.")
    relation("relation:reflows:o012-rbt-l30-fig-001:diagram-asset", "unit:o012-rbt-l30-fig-001",
             "illustrates", "asset:o012-u030-semantic-diagram-layer",
             "The semantic figure preserves the sole fixed-canvas TikZ construction in reading order.")
    proof_targets = {1: "unit:o012-rbt-l30-thm-001", 2: "unit:o012-rbt-l30-thm-002",
                     3: "unit:o012-rbt-l30-cor-001", 4: "unit:o012-rbt-l30-thm-003"}
    for number, target in proof_targets.items():
        relation(f"relation:proves:o012-rbt-l30-proof-{number:03d}:closure",
                 f"unit:o012-rbt-l30-proof-{number:03d}", "proves", target,
                 f"Complete proof closure {number} for Unit 30.")
    for number in range(1, 7):
        relation(f"relation:solves:l30-sol-{number:03d}:l30-mcheck-{number:03d}",
                 f"unit:o012-rbt-l30-sol-{number:03d}", "solves",
                 f"unit:o012-rbt-l30-mcheck-{number:03d}",
                 f"Complete checked solution for Unit 30 mastery check {number}.")
        relation(f"relation:hints:l30-hint-{number:03d}:l30-mcheck-{number:03d}",
                 f"unit:o012-rbt-l30-hint-{number:03d}", "hints",
                 f"unit:o012-rbt-l30-mcheck-{number:03d}",
                 f"Bounded hint for Unit 30 mastery check {number}.")

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
        check = f"unit:o012-rbt-l30-mcheck-{number:03d}"
        solves = [obj for obj in additions["relations.jsonl"].values()
                  if obj["relation_type"] == "solves" and obj["to_id"] == check]
        hints = [obj for obj in additions["relations.jsonl"].values()
                 if obj["relation_type"] == "hints" and obj["to_id"] == check]
        if len(solves) != 1 or len(hints) != 1: raise SystemExit(f"mastery mismatch: {number}")
    if len([obj for obj in additions["units.jsonl"].values() if obj.get("proof_status")]) != 4:
        raise SystemExit("four-proof closure mismatch")
    if len(additions["corrections.jsonl"]) != 10: raise SystemExit("correction dossier mismatch")
    if additions["rights.jsonl"][CUMULATIVE_RIGHTS]["component_scope"] != [
            f"unit:o012-rbt-u{number:03d}" for number in range(1, 31)]:
        raise SystemExit("cumulative rights mismatch")
    if by_id["unit:o012-rbt-l30-boundary-001"].get("next_source_line") != NEXT_SOURCE_LINE:
        raise SystemExit("terminal cursor mismatch")
    aliases = {alias: unit["id"] for unit in additions["units.jsonl"].values()
               for alias in unit.get("source_aliases", [])}
    if aliases != {"thm:hairy_sphere": "unit:o012-rbt-l30-thm-003"}:
        raise SystemExit("source alias mismatch")
    if sum(obj.get("source_diagram_count", 0) for obj in additions["units.jsonl"].values()) != 1:
        raise SystemExit("diagram census mismatch")
    expected_findings = {"UNIT030-ED-P2-001", "UNIT030-QA-P3-002"}
    if {item.get("finding_id") for item in qa_doc["resolved_findings"]} != expected_findings:
        raise SystemExit("resolved finding set changed")

    outputs: dict[str, bytes] = {}
    for name in FILES:
        if (BACKEND / name).read_bytes()[:len(prefix_raw[name])] != prefix_raw[name]:
            raise SystemExit(f"prefix changed: {name}")
        suffix = b"".join(canon(additions[name][ident]) for ident in sorted(additions[name]))
        outputs[name] = prefix_raw[name] + suffix
    for name, generated in outputs.items(): (BACKEND / name).write_bytes(generated)
    bundle = hashlib.sha256()
    for name in FILES:
        bundle.update(name.encode()); bundle.update(b"\0"); bundle.update(outputs[name])
    counts = {name: len(additions[name]) for name in FILES}
    print("Unit 030 semantic backend extension: PASS")
    print("new_records_by_file=" + json.dumps(counts, sort_keys=True))
    print(f"new_records={sum(counts.values())}")
    print(f"total_records={sum(PREFIX[name][0] + counts[name] for name in FILES)}")
    print(f"backend_bytes={sum(len(item) for item in outputs.values())}")
    print(f"backend_bundle_sha256={bundle.hexdigest()}")
    for name in FILES:
        print(f"file={name} records={PREFIX[name][0] + counts[name]} bytes={len(outputs[name])} sha256={digest(outputs[name])}")
    print(f"source_sha256={SOURCE_SHA}"); print(f"upstream_span_sha256={UPSTREAM_SPAN_SHA}")
    print("actual_stable_ids=47"); print("qa_declared_stable_ids=47")
    print("proof_closures=4"); print("mastery_triples=6")
    print("source_aliases=1"); print("resolved_findings=2"); print("source_diagrams=1")
    print("adverse_ledger_through=O012-ADV-0407")
    print("terminology_through=O012-TERM-0365"); print("terminal_source_eof=true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
