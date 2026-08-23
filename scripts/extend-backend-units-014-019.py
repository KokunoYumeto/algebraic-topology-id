#!/usr/bin/env python3
"""Fail-closed backend extension for the O012/D60 Units 014--019 boundary.

This file is deliberately a *plan-to-run* producer.  It does not execute on
import; invoking it reads the six frozen reader units, the two control ledgers,
and the existing eleven JSONL files, validates every input, builds new records
in memory, and only then replaces the JSONL files.  Existing record lines are
retained byte-for-byte.  The only pre-existing records allowed to change are
the four explicit authority/rights pointers which move the published staged
boundary from Units 001--013 to Units 001--019.

No generated build or publication artifact is asserted here.  Review and
source-audit files are added only when their exact frozen identities are listed
below; cumulative QA/build artifacts are intentionally absent until such files
exist with independently frozen hashes.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable


LANE = Path(__file__).resolve().parents[1]
BACKEND = LANE / "backend"
LEDGER = LANE / "00_control/ADVERSE_LEDGER.csv"
TERMINOLOGY = LANE / "00_control/TERMINOLOGY.csv"
SCHEMA = "curriculum.interop"
SCHEMA_VERSION = "0.1.0"
WORKFLOW = "o012-d60-id-reader-production"
TIMESTAMP = "2026-08-23T00:00:00Z"
PROGRAM_ID = "program:o012-id"
COURSE_ID = "course:o012-d60"
RESOURCE_ID = "resource:roberts-algebraic-topology-2019"
EDITION_ID = "edition:roberts-at-2019-b947ad2"
ROBERTS_RIGHTS = "rights:roberts-cc-by-4.0"
OLD_CUMULATIVE_RIGHTS = "rights:o012-units-001-013-composite-cc-by-4.0"
CUMULATIVE_RIGHTS = "rights:o012-units-001-019-composite-cc-by-4.0"
UPSTREAM_COMMIT = "b947ad2e9f9e301bfe24590a9db653bc54fa1a53"

JSONL_NAMES = (
    "artifacts.jsonl", "assets.jsonl", "authority.jsonl", "concepts.jsonl",
    "corrections.jsonl", "qa.jsonl", "relations.jsonl", "rights.jsonl",
    "segments.jsonl", "terms.jsonl", "units.jsonl",
)


# These are the identities supplied by the completed translation/review lane.
# A changed byte, line count, or hash aborts before any backend file is written.
SOURCE_SPECS: dict[int, dict[str, Any]] = {
    14: {
        "relative": "source/id-ID/units/unit-014-lecture-014.md",
        "bytes": 28488, "lines": 947,
        "sha256": "da6f18b455d76adafd8b9b648ed7c277958eca95c0b7d76a8bd9895d79ec6677",
        "upstream_start": 3047, "upstream_end": 3209, "expected_ids": 38,
        "title": "Topologi Aljabar - Unit 14: Menuju Klasifikasi Ruang Penutup",
        "root_concepts": ["covering-space-classification", "monodromy", "groupoid-action", "orbit-decomposition"],
    },
    15: {
        "relative": "source/id-ID/units/unit-015-lecture-015.md",
        "bytes": 27725, "lines": 835,
        "sha256": "e9ab0565ae460236a69c77389b76d32405873156fc451be9cf95c3749e7fe9d1",
        "upstream_start": 3210, "upstream_end": 3286, "expected_ids": 34,
        "title": "Topologi Aljabar - Unit 15: Komponen Ruang Penutup, Orbit Monodromi, dan Koset Kanan",
        "root_concepts": ["covering-space-classification", "covering-space", "orbit-decomposition", "group-action", "fibre-functor"],
    },
    16: {
        "relative": "source/id-ID/units/unit-016-lecture-016.md",
        "bytes": 33919, "lines": 984,
        "sha256": "31dfc4c3647f7d6a1d398d2123efe1faa82348428df0180eee2a2358572f9054",
        "upstream_start": 3287, "upstream_end": 3383, "expected_ids": 33,
        "title": "Topologi Aljabar - Unit 16: Penutup Universal, Hasil Bagi Subgrup, dan Surjektivitas Esensial",
        "root_concepts": ["fibrewise-action", "universal-covering-space", "path-class-space", "covering-basis", "monodromy"],
    },
    17: {
        "relative": "source/id-ID/units/unit-017-lecture-017.md",
        "bytes": 29933, "lines": 952,
        "sha256": "47576d7c26a436ba915c276b692e2bc0ead6fae038295fee3a82a50426ed9a96",
        "upstream_start": 3384, "upstream_end": 3481, "expected_ids": 34,
        "title": "Topologi Aljabar - Unit 17: Ekuivalensi Ruang Penutup dan Grup Homotopi Lebih Tinggi",
        "root_concepts": ["equivalence-of-categories", "higher-homotopy-group", "homotopy-relative", "topological-group", "loop-space"],
    },
    18: {
        "relative": "source/id-ID/units/unit-018-lecture-018.md",
        "bytes": 44415, "lines": 1663,
        "sha256": "9d0564f6a074441332e42755d46d9a0e858189a5ff4d8b5be52b1def12532598",
        "upstream_start": 3482, "upstream_end": 3677, "expected_ids": 67,
        "title": "Topologi Aljabar - Unit 18: Transpor Grup Homotopi, Bundel Serat, dan Barisan Eksak Panjang",
        "root_concepts": ["higher-homotopy-group", "fibre-bundle", "hopf-bundle", "exact-sequence", "long-exact-sequence"],
    },
    19: {
        "relative": "source/id-ID/units/unit-019-lecture-019.md",
        "bytes": 57277, "lines": 1865,
        "sha256": "ba34773d63e4dc70fccdf4fa19fbdc8a397062a4bc359978f3261a70ff64f98c",
        "upstream_start": 3678, "upstream_end": 3947, "expected_ids": 78,
        "title": "Topologi Aljabar - Unit 19: Bundel Homogen, Ekuivalensi Homotopi Lemah, dan Kompleks",
        "root_concepts": ["lie-group", "homogeneous-space", "weak-homotopy-equivalence", "euler-characteristic", "complex", "directed-graph"],
    },
}


# Every control in the current ledger is assigned to an actual stable anchor
# in its unit.  The source term and Indonesian form themselves remain sourced
# from TERMINOLOGY.csv; this table freezes only the semantic slug and evidence
# anchor, preventing a silently moved term from changing scope.
_TERM_ROWS: tuple[tuple[int, str, int, str], ...] = (
    (208, "reduced-arrow-word", 14, "s01"),
    (209, "basepoint-preserving-contraction", 14, "s02"),
    (210, "attaching-map", 14, "s03"),
    (211, "presentation-complex", 14, "s03"),
    (212, "weak-topology", 14, "s04"),
    (213, "genus", 14, "s05"),
    (214, "classification-of-covering-spaces", 14, "s06"),
    (215, "groupoid-representation", 15, "s01"),
    (216, "functor-category", 15, "s01"),
    (217, "restriction-functor", 15, "s01"),
    (218, "left-action", 15, "s03"),
    (219, "orbit", 15, "s03"),
    (220, "orbit-representative", 15, "s03"),
    (221, "locally-path-connected", 15, "s02"),
    (222, "symmetric-group", 15, "s03"),
    (223, "basepoint", 15, "s04"),
    (224, "subgroup", 15, "s05"),
    (225, "connected-covering-space", 15, "s04"),
    (226, "simply-connected-covering-space", 15, "s04"),
    (227, "universal-covering-space", 15, "s05"),
    (228, "classification-theorem", 15, "s05"),
    (229, "orbit-decomposition", 15, "s03"),
    (230, "covering-action", 15, "s03"),
    (231, "fibre-functor", 15, "s01"),
    (232, "product-category", 15, "s01"),
    (233, "essentially-surjective", 15, "s05"),
    (234, "fibrewise-action", 16, "s01"),
    (235, "covering-basis-topology", 16, "s03"),
    (236, "path-class-space", 16, "s03"),
    (237, "endpoint-projection", 16, "s03"),
    (238, "sheet-of-a-covering", 16, "s03"),
    (239, "closed-lift-criterion", 16, "s04"),
    (240, "commuting-actions", 16, "s02"),
    (241, "equivalence-of-categories", 17, "s02"),
    (242, "higher-homotopy-group", 17, "s03"),
    (243, "map-of-pairs", 17, "s04"),
    (244, "homotopy-relative-to-a", 17, "s04"),
    (245, "eckmann-hilton-argument", 17, "s06"),
    (246, "topological-group", 17, "s07"),
    (247, "pointwise-multiplication", 17, "s07"),
    (248, "interchange-law", 17, "s06"),
    (249, "commutative-monoid", 17, "s06"),
    (250, "abelian-group", 17, "s06"),
    (251, "iterated-loop-space", 17, "s07"),
    (252, "basepoint-transport", 18, "s02"),
    (253, "discrete-space", 18, "s01"),
    (254, "finite-set", 18, "s01"),
    (255, "module-over-r", 18, "s01"),
    (256, "fibre-bundle", 18, "s04"),
    (257, "total-space", 18, "s04"),
    (258, "local-trivialization", 18, "s04"),
    (259, "hopf-bundle", 18, "s04"),
    (260, "complex-projective-line", 18, "s04"),
    (261, "homogeneous-coordinates", 18, "s04"),
    (262, "exact-sequence", 18, "s05"),
    (263, "exact-at", 18, "s05"),
    (264, "short-exact-sequence", 18, "s05"),
    (265, "long-exact-sequence", 18, "s06"),
    (266, "connecting-map", 18, "s06"),
    (267, "kernel", 18, "s05"),
    (268, "image-of-a-map", 18, "s05"),
    (269, "local-system", 18, "s06"),
    (270, "orientation-preserving", 18, "s02"),
    (271, "pointed-fibre-bundle", 18, "s05"),
    (272, "transition-function", 18, "s04"),
    (273, "complex-hopf-bundle", 18, "s08"),
    (274, "quaternionic-hopf-bundle", 18, "s08"),
    (275, "lie-group", 19, "s01"),
    (276, "closed-subgroup", 19, "s01"),
    (277, "homogeneous-space", 19, "s01"),
    (278, "weak-homotopy-equivalence", 19, "s02"),
    (279, "warsaw-circle", 19, "s02"),
    (280, "euler-characteristic", 19, "s04"),
    (281, "cohomologically-graded-complex", 19, "s04"),
    (282, "morphism-of-complexes", 19, "s05"),
    (283, "gradient", 19, "s06"),
    (284, "curl", 19, "s06"),
    (285, "divergence", 19, "s06"),
    (286, "coboundary", 19, "s07"),
    (287, "cokernel", 19, "s07"),
)
TERM_SPECS = {
    f"O012-TERM-{number:04d}": (slug, f"o012-rbt-l{lecture:02d}-{suffix}")
    for number, slug, lecture, suffix in _TERM_ROWS
}


# All adverse rows 0188--0278 are expected.  Defaults make every row
# traceable even if a later control adds a new locator; the grouped overrides
# below record the actual section/figure anchors already present in the units.
EVENT_LECTURE_RANGES = (
    (range(188, 202), 14), (range(202, 215), 15),
    (range(215, 228), 16), (range(228, 240), 17),
    (range(240, 258), 18), (range(258, 279), 19),
)
EVENT_LECTURE: dict[int, int] = {
    number: lecture for numbers, lecture in EVENT_LECTURE_RANGES for number in numbers
}
EVENT_TARGETS: dict[int, list[str]] = {
    number: [f"o012-rbt-l{lecture:02d}-notice"]
    for number, lecture in EVENT_LECTURE.items()
}


def set_targets(numbers: Iterable[int], lecture: int, *suffixes: str) -> None:
    for number in numbers:
        EVENT_TARGETS[number] = [f"o012-rbt-l{lecture:02d}-{suffix}" for suffix in suffixes]


set_targets([188], 14, "s02")
set_targets([189, 190, 196], 14, "s05")
set_targets([191], 14, "s01", "fig-001", "proof-001")
set_targets([192], 14, "s02", "exa-001")
set_targets([193, 194, 195], 14, "s03", "s04")
set_targets([197], 14, "s03", "s04", "s05", "s06")
set_targets([198], 14, "s06", "rem-001")
set_targets([199], 14, "fig-001", "fig-002", "fig-003")
set_targets([200], 14, "s01", "s04", "s05")
set_targets([201], 14, "s01", "s02", "s04", "s05", "s06")

set_targets([202, 203], 15, "s01")
set_targets([204, 205], 15, "s02")
set_targets([206], 15, "s02", "s03", "s04")
set_targets([207, 208, 209], 15, "s03")
set_targets([210], 15, "s05")
set_targets([211], 15, "s01", "s03", "s04", "s05")
set_targets([212], 15, "s02", "s03", "s04")
set_targets([213], 15, "s02", "s05")
set_targets([214], 15, "s02", "s03", "s04", "s05")

set_targets([215], 16, "s01", "s02", "s04")
set_targets([216], 16, "s01")
set_targets([217], 16, "s02")
set_targets([218, 221], 16, "s03", "s04")
set_targets([219, 220], 16, "s03")
set_targets([222, 223, 224, 225], 16, "s04")
set_targets([226], 16, "s01", "s02", "s03", "s04")
set_targets([227], 16, "s02", "s04")

set_targets([228], 17, "s01")
set_targets([229, 230, 231], 17, "s02")
set_targets([232], 17, "s03", "s04")
set_targets([233], 17, "s03")
set_targets([234], 17, "s04")
set_targets([235], 17, "s05", "s06", "s07")
set_targets([236], 17, "s07")
set_targets([237], 17, "s02", "s03", "s06", "s07")
set_targets([238], 17, "s02", "s03", "s05")
set_targets([239], 17, "s04", "s06")

set_targets([240], 18, "s01")
set_targets([241, 242, 243, 244], 18, "s02")
set_targets([245, 246, 247], 18, "s03")
set_targets([248, 249], 18, "s04")
set_targets([250], 18, "s05")
set_targets([251, 252, 253], 18, "s06")
set_targets([254], 18, "s07")
set_targets([255, 256], 18, "s08")
set_targets([257], 18, "s02", "s03", "s04", "s05", "s06")

set_targets([258, 259, 260, 261], 19, "s01")
set_targets([262], 19, "s01", "s02")
set_targets([263, 264], 19, "s04")
set_targets([265, 266], 19, "s06")
set_targets([267, 268], 19, "s05")
set_targets([269, 270, 271], 19, "s06")
set_targets([272], 19, "s07")
set_targets([273], 19, "s01", "s02", "s04", "s05", "s06", "s07")
set_targets([274], 19, "s02")
set_targets([275], 19, "s01", "s06")
set_targets([276], 19, "sol-001")
set_targets([277], 19, "sol-001")
set_targets([278], 19, "ex-002", "fig-001", "sol-003", "sol-004", "sol-006")


# Exact review/source-audit artifacts currently on disk.  There are no entries
# for a cumulative build here because no Units 001--019 build receipt is yet
# frozen.  The script therefore cannot fabricate a build/artifact assertion.
ARTIFACT_META: dict[str, tuple[str, int, str, str, str, str]] = {
    "artifact:o012-u014-independent-review": ("qa/UNIT_014_INDEPENDENT_REVIEW.md", 9725, "43a409f8f127fe9425d14bc8279a594e4ea1f604da3db4f99316aa7c17c3969d", "text/markdown; charset=utf-8", "unit:o012-rbt-u014", "mathematically_reviewed"),
    "artifact:o012-u015-independent-review": ("qa/UNIT_015_INDEPENDENT_REVIEW.md", 4392, "9776c911f5d4f4cd7027375ac29514ca2722f28877d27e79753fabf61876dc90", "text/markdown; charset=utf-8", "unit:o012-rbt-u015", "mathematically_reviewed"),
    "artifact:o012-u016-independent-review": ("qa/UNIT_016_INDEPENDENT_REVIEW.md", 8485, "335f8ef19f35ba063ad526850d01eec377dc89eb7b697831b8741659a86444c6", "text/markdown; charset=utf-8", "unit:o012-rbt-u016", "mathematically_reviewed"),
    "artifact:o012-u017-independent-review": ("qa/UNIT_017_INDEPENDENT_REVIEW.md", 9903, "b4885ed709311275a9ae32fedbefe7bf86c72203caafa92de3b557f17c1fc625", "text/markdown; charset=utf-8", "unit:o012-rbt-u017", "mathematically_reviewed"),
    "artifact:o012-u018-independent-review": ("qa/UNIT_018_INDEPENDENT_REVIEW.md", 3054, "146a011168c49ef922b71e8278b1631d430aa3b2134d150219d2fef0a5437cf2", "text/markdown; charset=utf-8", "unit:o012-rbt-u018", "mathematically_reviewed"),
    "artifact:o012-u019-independent-review": ("qa/UNIT_019_INDEPENDENT_REVIEW.md", 2707, "d360a17a8a7a5008a80873c4413d92bd9354b6c44275365809be33258c0673a5", "text/markdown; charset=utf-8", "unit:o012-rbt-u019", "mathematically_reviewed"),
    "artifact:o012-u016-source-audit": ("qa/UNIT_016_SOURCE_AUDIT.md", 5898, "52476eb5e239fa4d752b8a9f533c8bc00b442fe27e5b5fe48925dc9b6eb3a288", "text/markdown; charset=utf-8", "unit:o012-rbt-u016", "source_frozen"),
    "artifact:o012-u017-source-audit": ("qa/UNIT_017_SOURCE_AUDIT.md", 12303, "31d984a617844f664bb7ddf35037d6b7f33041f08230c29cbcd301680e9566ce", "text/markdown; charset=utf-8", "unit:o012-rbt-u017", "source_frozen"),
    "artifact:o012-u018-source-audit": ("qa/UNIT_018_SOURCE_AUDIT.md", 8630, "66dbc4a480481edf8d89559b1ea4395d9d787e96ce03e9e348a5de50d4cca1ac", "text/markdown; charset=utf-8", "unit:o012-rbt-u018", "source_frozen"),
    "artifact:o012-u019-source-audit": ("qa/UNIT_019_SOURCE_AUDIT.md", 8956, "9ff651aa4a98f17f9ae67ce154cc531147bf212b2be03e53c3aced3994066f36", "text/markdown; charset=utf-8", "unit:o012-rbt-u019", "source_frozen"),
    "artifact:o012-u019-qa": ("qa/UNIT_019_QA.json", 3519, "a2ecc5dcc539c6434d2cb937ad7bb768c6ed434947b4cedcd313ce1bcfe8d1c3", "application/json", "unit:o012-rbt-u019", "built"),
}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def common(entity_type: str, record_id: str) -> dict[str, Any]:
    return {
        "entity_type": entity_type, "id": record_id, "schema": SCHEMA,
        "schema_version": SCHEMA_VERSION, "status": "active",
        "supersedes": None, "timestamp": TIMESTAMP, "workflow": WORKFLOW,
    }


def canonical(record: dict[str, Any]) -> str:
    return json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def load_jsonl(name: str) -> tuple[dict[str, dict[str, Any]], dict[str, bytes]]:
    path = BACKEND / name
    raw = path.read_bytes()
    if b"\r" in raw or not raw.endswith(b"\n"):
        raise SystemExit(f"{name}: expected LF-terminated canonical JSONL")
    records: dict[str, dict[str, Any]] = {}
    lines: dict[str, bytes] = {}
    ids: list[str] = []
    for line_number, line in enumerate(raw.splitlines(keepends=True), start=1):
        if not line.endswith(b"\n"):
            raise SystemExit(f"{name}:{line_number}: missing newline")
        try:
            record = json.loads(line.decode("utf-8"))
        except Exception as exc:  # pragma: no cover - fail-closed diagnostic
            raise SystemExit(f"{name}:{line_number}: invalid JSON: {exc}") from exc
        record_id = record.get("id")
        if not isinstance(record_id, str) or not record_id:
            raise SystemExit(f"{name}:{line_number}: missing id")
        if record_id in records:
            raise SystemExit(f"duplicate existing backend id: {record_id}")
        if canonical(record).encode("utf-8") + b"\n" != line:
            raise SystemExit(f"{name}:{line_number}: historical line is not canonical")
        records[record_id] = record
        lines[record_id] = line
        ids.append(record_id)
    if ids != sorted(ids):
        raise SystemExit(f"{name}: historical IDs are not sorted")
    return records, lines


def infer_kind(local_id: str, opening: str) -> str:
    if local_id.endswith("-notice"):
        return "notice"
    if re.fullmatch(r"o012-rbt-l\d{2}", local_id):
        return "lecture"
    if local_id.endswith("-mastery"):
        return "mastery_section"
    if re.search(r"-s\d{2}$", local_id):
        return "section"
    if local_id.endswith("-sol-001") or "-sol-" in local_id:
        return "solution"
    if "-mcheck-" in local_id:
        return "exercise"
    if "-hint-" in local_id:
        return "hint"
    if "-boundary-" in local_id:
        return "boundary"
    class_match = re.search(r"\{\.([A-Za-z][A-Za-z0-9_-]*)", opening)
    class_name = class_match.group(1) if class_match else ""
    class_kinds = {
        "proposition": "proposition", "proof": "proof", "example": "example",
        "question": "question", "lemma": "lemma", "definition": "definition",
        "remark": "remark", "equation": "equation", "note": "note",
        "construction": "construction", "corollary": "corollary", "theorem": "theorem",
        "figure": "figure", "diagram": "diagram", "source-audit": "source_audit",
        "source-margin": "source_margin", "audit": "source_audit", "margin": "source_margin",
        "exercise": "exercise", "hint": "hint", "solution": "solution",
    }
    if class_name in class_kinds:
        return class_kinds[class_name]
    if "-fig-" in local_id:
        return "figure"
    if "-dia-" in local_id:
        return "diagram"
    if "-ex-" in local_id:
        raise SystemExit(f"ambiguous example/exercise class for {local_id}")
    raise SystemExit(f"cannot infer unit kind: {local_id}")


def is_original(local_id: str, opening: str, kind: str) -> bool:
    if 'data-origin="edition-original"' in opening:
        return True
    if any(token in local_id for token in ("-notice", "-boundary-", "-mastery", "-mcheck-", "-hint-", "-sol-")):
        return True
    return kind in {"source_audit", "source_margin"}


def concept_ids(slugs: Iterable[str]) -> list[str]:
    return [f"concept:{slug}" for slug in dict.fromkeys(slugs)]


def parse_source_locations(location: str) -> list[int]:
    """Return every Notes.tex line named by an adverse-ledger locator."""
    values: list[int] = []
    for start, end in re.findall(r"Notes\.tex:(\d+)(?:-(\d+))?", location):
        first = int(start)
        last = int(end or start)
        values.extend(range(first, last + 1))
    return values


def unit_for_event(number: int) -> int:
    if number not in EVENT_LECTURE:
        raise SystemExit(f"unexpected adverse event number {number}")
    return EVENT_LECTURE[number]


def correction_type(status: str) -> str:
    return {
        "accessibility_reflow": "structural_adaptation",
        "clarified_in_translation": "clarification",
        "corrected_in_translation": "mathematical_correction",
        "corrected_after_independent_review": "mathematical_correction",
        "proof_completed_in_translation": "proof_completion",
        "proof_completed_after_independent_review": "proof_completion",
    }[status]


def build() -> None:
    record_sets: dict[str, dict[str, dict[str, Any]]] = {}
    prior_lines: dict[str, dict[str, bytes]] = {}
    for filename in JSONL_NAMES:
        record_sets[filename], prior_lines[filename] = load_jsonl(filename)

    # Global identity and schema checks happen before any mutation.
    all_records: dict[str, dict[str, Any]] = {}
    owner_file: dict[str, str] = {}
    for filename, records in record_sets.items():
        for record_id, record in records.items():
            if record_id in all_records:
                raise SystemExit(f"duplicate global backend id: {record_id}")
            if record.get("id") != record_id or record.get("schema") != SCHEMA or record.get("schema_version") != SCHEMA_VERSION:
                raise SystemExit(f"historical identity/schema mismatch: {filename}:{record_id}")
            all_records[record_id] = record
            owner_file[record_id] = filename

    units = record_sets["units.jsonl"]
    segments = record_sets["segments.jsonl"]
    concepts = record_sets["concepts.jsonl"]
    terms = record_sets["terms.jsonl"]
    relations = record_sets["relations.jsonl"]
    rights = record_sets["rights.jsonl"]
    assets = record_sets["assets.jsonl"]
    corrections = record_sets["corrections.jsonl"]
    qa_events = record_sets["qa.jsonl"]
    artifacts = record_sets["artifacts.jsonl"]
    authority = record_sets["authority.jsonl"]

    old_snapshot = {record_id: json.loads(json.dumps(record, ensure_ascii=False)) for record_id, record in all_records.items()}
    owned_new_ids: set[str] = set()
    unit_context: dict[int, dict[str, Any]] = {}

    def put_new(table: dict[str, dict[str, Any]], record: dict[str, Any]) -> None:
        record_id = record["id"]
        if record_id in all_records or record_id in owned_new_ids:
            raise SystemExit(f"new record collides with historical/global ID: {record_id}")
        table[record_id] = record
        all_records[record_id] = record
        owner_file[record_id] = next(name for name, values in record_sets.items() if values is table)
        owned_new_ids.add(record_id)

    def ensure_concept(slug: str, label: str, domain: str) -> str:
        record_id = f"concept:{slug}"
        existing = concepts.get(record_id)
        if existing is not None:
            if existing.get("entity_type") != "concept" or existing.get("locale_neutral") is not True:
                raise SystemExit(f"existing concept malformed: {record_id}")
            return record_id
        concept = common("concept", record_id)
        concept.update({"canonical_label": label, "domain": domain, "locale_neutral": True})
        put_new(concepts, concept)
        return record_id

    term_slugs_by_evidence: defaultdict[str, list[str]] = defaultdict(list)
    for _, (slug, evidence) in TERM_SPECS.items():
        term_slugs_by_evidence[evidence].append(slug)

    heading_re = re.compile(r"^(#{1,6})\s+(.+?)\s+\{")
    # Keep the regex braces literal; substitute only the lecture field.  Using
    # ``str.format`` here would treat the character-class braces as fields.
    anchor_re_template = r"\{[^}\n]*#(o012-rbt-l{lecture:02d}(?:-[a-z0-9]+)*)[^}\n]*\}"

    for lecture, spec in SOURCE_SPECS.items():
        source_path = LANE / spec["relative"]
        raw = source_path.read_bytes()
        if len(raw) != spec["bytes"] or digest(raw) != spec["sha256"]:
            raise SystemExit(f"Unit {lecture:03d} source identity mismatch")
        raw_lines = raw.splitlines(keepends=True)
        if len(raw_lines) != spec["lines"]:
            raise SystemExit(f"Unit {lecture:03d} line-count mismatch")
        text_lines = [line.decode("utf-8").rstrip("\r\n") for line in raw_lines]
        id_re = re.compile(anchor_re_template.replace("{lecture:02d}", f"{lecture:02d}"))
        anchor_start: dict[str, int] = {}
        aliases: dict[str, list[str]] = {}
        for line_number, text in enumerate(text_lines, start=1):
            found = id_re.findall(text)
            if len(found) > 1:
                raise SystemExit(f"multiple Unit {lecture:03d} stable IDs on line {line_number}")
            if found:
                local_id = found[0]
                if local_id in anchor_start:
                    raise SystemExit(f"duplicate stable ID: {local_id}")
                anchor_start[local_id] = line_number
                alias = re.search(r'data-source-label="([^"]+)"', text)
                if alias:
                    aliases[local_id] = [alias.group(1)]
        if len(anchor_start) != spec["expected_ids"]:
            raise SystemExit(f"Unit {lecture:03d} stable-ID mismatch: {len(anchor_start)} != {spec['expected_ids']}")

        def derive_span(local_id: str) -> tuple[int, int]:
            start = anchor_start[local_id]
            opening = text_lines[start - 1]
            heading = heading_re.match(opening)
            if heading:
                level = len(heading.group(1))
                end = len(text_lines)
                for candidate in range(start + 1, len(text_lines) + 1):
                    next_heading = heading_re.match(text_lines[candidate - 1])
                    if next_heading and len(next_heading.group(1)) <= level:
                        end = candidate - 1
                        break
                while end > start and not text_lines[end - 1].strip():
                    end -= 1
                return start, end
            if opening.lstrip().startswith(":::"):
                for candidate in range(start + 1, len(text_lines) + 1):
                    if text_lines[candidate - 1].strip() == ":::":
                        return start, candidate
            raise SystemExit(f"cannot derive structural span for {local_id}")

        spans = {local_id: derive_span(local_id) for local_id in anchor_start}

        def locator(start: int, end: int) -> dict[str, Any]:
            return {
                "content_sha256": digest(b"".join(raw_lines[start - 1:end])),
                "file_sha256": spec["sha256"], "line_end": end,
                "line_start": start, "path": spec["relative"],
            }

        root_id = f"unit:o012-rbt-u{lecture:03d}"
        companion_rights = f"rights:o012-u{lecture:03d}-companion-cc-by-4.0"
        composite_rights = f"rights:o012-u{lecture:03d}-composite-cc-by-4.0"
        root_concepts = list(spec["root_concepts"])
        for slug in root_concepts:
            ensure_concept(slug, slug.replace("-", " "), "algebraic_topology")
        root = common("unit", root_id)
        root.update({
            "concept_ids": concept_ids(root_concepts), "course_id": COURSE_ID,
            "display_title": spec["title"], "edition_id": EDITION_ID,
            "locale": "id-ID", "order": lecture, "parent_id": COURSE_ID,
            "path": [root_id], "program_id": PROGRAM_ID,
            "provenance_relation": "composite_translated_and_original",
            "resource_id": RESOURCE_ID, "rights_component_id": composite_rights,
            "source_local_id": None, "target_locator": locator(1, spec["lines"]),
            "translation_state": "structurally_verified", "unit_kind": "reader_unit",
        })
        put_new(units, root)

        ordered = sorted(anchor_start, key=anchor_start.get)
        lecture_local = f"o012-rbt-l{lecture:02d}"
        mastery_local = f"o012-rbt-l{lecture:02d}-mastery"
        current_section: str | None = None
        current_mode = "lecture"
        sibling_next: defaultdict[str, int] = defaultdict(lambda: 1)
        metadata: dict[str, dict[str, Any]] = {}
        for local_id in ordered:
            opening = text_lines[anchor_start[local_id] - 1]
            kind = infer_kind(local_id, opening)
            if kind in {"notice", "lecture", "mastery_section"}:
                parent = root_id
                order = sibling_next[parent]
                sibling_next[parent] += 1
                if kind == "mastery_section":
                    current_mode = "mastery"
            elif kind == "boundary":
                # A unit-entry boundary precedes the first section and is a
                # direct child of the reader unit; an exit boundary belongs to
                # the section it closes (matching Units 012–013).
                if current_section is None or current_mode == "mastery":
                    parent = root_id
                else:
                    parent = f"unit:{current_section}"
                order = sibling_next[parent]
                sibling_next[parent] += 1
            elif kind == "section" and current_mode == "lecture":
                parent = f"unit:{lecture_local}"
                order = sibling_next[parent]
                sibling_next[parent] += 1
                current_section = local_id
            elif kind == "boundary" and current_mode == "lecture":
                # Unit 14 has an inbound boundary immediately after the
                # lecture heading, before the first numbered section.  Keep
                # both boundary notices as direct lecture children rather than
                # pretending they belong to a section that does not exist yet.
                parent = f"unit:{lecture_local}"
                order = sibling_next[parent]
                sibling_next[parent] += 1
            elif current_mode == "mastery":
                parent = f"unit:{mastery_local}"
                order = sibling_next[parent]
                sibling_next[parent] += 1
            else:
                if current_section is None:
                    raise SystemExit(f"Unit {lecture:03d} child lacks section: {local_id}")
                parent = f"unit:{current_section}"
                order = sibling_next[parent]
                sibling_next[parent] += 1
            heading = heading_re.match(opening)
            if heading:
                display = re.sub(r"\s+\{.*$", "", heading.group(2)).strip()
            else:
                display = local_id
                for candidate in text_lines[anchor_start[local_id]:spans[local_id][1]]:
                    match = re.match(r"^\*\*(.+?)\*\*", candidate)
                    if match:
                        display = match.group(1).strip()
                        break
            slugs = list(root_concepts) + term_slugs_by_evidence.get(local_id, [])
            metadata[local_id] = {
                "display": display, "kind": kind, "parent": parent,
                "order": order, "concept_slugs": list(dict.fromkeys(slugs)),
            }

        def unit_path(local_id: str) -> list[str]:
            unit_id = f"unit:{local_id}"
            parent = metadata[local_id]["parent"]
            if parent == root_id:
                return [root_id, unit_id]
            return unit_path(parent.removeprefix("unit:")) + [unit_id]

        upstream_locator = {
            "commit_sha": UPSTREAM_COMMIT, "line_end": spec["upstream_end"],
            "line_start": spec["upstream_start"], "path": "Notes.tex",
            "precision": "unit_range_only",
        }
        original_ids: list[str] = []
        for local_id in ordered:
            item = metadata[local_id]
            start, end = spans[local_id]
            opening = text_lines[start - 1]
            original = is_original(local_id, opening, item["kind"])
            provenance = "edition_original" if original else "translated_adapted_from_upstream"
            component_rights = companion_rights if original else ROBERTS_RIGHTS
            extra = {"source_aliases": aliases[local_id]} if local_id in aliases else {}
            unit_id = f"unit:{local_id}"
            for slug in item["concept_slugs"]:
                ensure_concept(slug, slug.replace("-", " "), "algebraic_topology")
            unit = common("unit", unit_id)
            unit.update({
                "concept_ids": concept_ids(item["concept_slugs"]), "course_id": COURSE_ID,
                "display_title": item["display"], "edition_id": EDITION_ID,
                "locale": "id-ID", "order": item["order"], "parent_id": item["parent"],
                "path": unit_path(local_id), "program_id": PROGRAM_ID,
                "provenance_relation": provenance, "resource_id": RESOURCE_ID,
                "rights_component_id": component_rights, "source_local_id": local_id,
                "target_locator": locator(start, end),
                "translation_state": "structurally_verified", "unit_kind": item["kind"],
                **extra,
            })
            put_new(units, unit)
            segment_id = f"segment:{local_id}"
            segment = common("segment", segment_id)
            segment.update({
                "concept_ids": concept_ids(item["concept_slugs"]), "edition_id": EDITION_ID,
                "locale": "id-ID", "order": item["order"],
                "provenance_relation": provenance, "resource_id": RESOURCE_ID,
                "rights_component_id": component_rights, "segment_kind": item["kind"],
                "source_local_id": local_id,
                "source_locator": ({"kind": "edition_original", "path": spec["relative"], "precision": "exact_target_span"} if original else dict(upstream_locator)),
                "target_locator": locator(start, end), "translation_state": "structurally_verified",
                "unit_id": unit_id, **extra,
            })
            put_new(segments, segment)
            if original:
                original_ids.append(unit_id)

        companion = common("rights", companion_rights)
        companion.update({
            "attribution": f"Original Indonesian mastery, source-boundary, and accessibility companion for O012/D60 Unit {lecture:03d}.",
            "change_notice": "Newly authored material; not represented as source-author text.",
            "component_scope": original_ids, "license_expression": "CC-BY-4.0",
            "license_url": "https://creativecommons.org/licenses/by/4.0/",
            "non_endorsement": "No endorsement by David Michael Roberts or affiliated institutions is implied.",
            "third_party_status": "No external media component is asserted.",
        })
        put_new(rights, companion)
        composite = common("rights", composite_rights)
        composite.update({
            "attribution": f"Composite Unit {lecture:03d} reader: Roberts source adaptation plus independently authored Indonesian companion; component provenance remains separated.",
            "change_notice": "See component rights records for translated/adapted and original portions.",
            "component_scope": [root_id], "license_expression": "CC-BY-4.0",
            "license_url": "https://creativecommons.org/licenses/by/4.0/",
            "non_endorsement": "Independent edition; no source-author endorsement.",
            "third_party_status": "Component-scoped rights records control.",
        })
        put_new(rights, composite)
        asset_id = f"asset:o012-u{lecture:03d}-source-markdown"
        asset = common("asset", asset_id)
        asset.update({
            "bytes": spec["bytes"], "edition_id": EDITION_ID,
            "media_type": "text/markdown; charset=utf-8", "path": spec["relative"],
            "resource_id": RESOURCE_ID, "rights_component_id": composite_rights,
            "role": "canonical_reader_source", "sha256": spec["sha256"],
        })
        put_new(assets, asset)
        unit_context[lecture] = {
            "root_id": root_id, "anchor_start": anchor_start, "spans": spans,
            "text_lines": text_lines, "raw_lines": raw_lines, "spec": dict(spec),
            "original_ids": original_ids,
        }

    # Terminology controls are a closed contiguous boundary, not a best-effort
    # search.  Existing term records are never rewritten by this extension.
    with TERMINOLOGY.open("r", encoding="utf-8", newline="") as stream:
        terminology_rows = {row["term_id"]: row for row in csv.DictReader(stream) if row["term_id"] in TERM_SPECS}
    if set(terminology_rows) != set(TERM_SPECS):
        raise SystemExit(f"terminology subset mismatch: {sorted(set(TERM_SPECS) - set(terminology_rows))}")
    for control_id, (slug, evidence_local_id) in TERM_SPECS.items():
        row = terminology_rows[control_id]
        if row["status"] != "admitted":
            raise SystemExit(f"{control_id}: control status is not admitted")
        lecture = int(re.search(r"l(\d{2})", evidence_local_id).group(1))
        evidence_id = f"unit:{evidence_local_id}"
        if evidence_id not in units:
            raise SystemExit(f"{control_id}: evidence anchor absent: {evidence_local_id}")
        if evidence_id not in {f"unit:{item}" for item in unit_context[lecture]["anchor_start"]}:
            raise SystemExit(f"{control_id}: evidence anchor is outside Unit {lecture:03d}")
        concept_id = ensure_concept(slug, row["source_term"], row["scope"])
        term_id = f"term:{slug}:id-ID"
        if term_id in terms:
            raise SystemExit(f"{control_id}: term ID already exists; refusing historical mutation: {term_id}")
        term = common("term", term_id)
        term.update({
            "concept_id": concept_id, "evidence_segment_id": f"segment:{evidence_local_id}",
            "locale": "id-ID", "preferred": row["id_ID"], "register": "textbook",
            "rejected_forms": [], "rights_component_id": units[evidence_id]["rights_component_id"],
            "scope_unit_id": unit_context[lecture]["root_id"], "source_term": row["source_term"],
            "terminology_control_id": control_id, "terminology_status": row["status"],
            "usage_note": row["note"], "variants": [],
        })
        put_new(terms, term)

    def add_relation(record_id: str, from_id: str, relation_type: str, to_id: str, note: str) -> None:
        record = common("relation", record_id)
        record.update({"from_id": from_id, "note": note, "relation_type": relation_type, "to_id": to_id})
        put_new(relations, record)

    for lecture, spec in SOURCE_SPECS.items():
        add_relation(
            f"relation:adapts:o012-rbt-u{lecture:03d}:roberts-edition",
            f"unit:o012-rbt-u{lecture:03d}", "adapts", EDITION_ID,
            f"Unit {lecture:03d} adapts Notes.tex lines {spec['upstream_start']}-{spec['upstream_end']} and adds separately identified original companion material.",
        )
        add_relation(
            f"relation:precedes:l{lecture:02d}:mastery",
            f"unit:o012-rbt-l{lecture:02d}", "precedes", f"unit:o012-rbt-l{lecture:02d}-mastery",
            "The translated lecture precedes its separately identified mastery companion.",
        )
    for before, after in ((13, 14), (14, 15), (15, 16), (16, 17), (17, 18), (18, 19)):
        add_relation(
            f"relation:precedes:u{before:03d}:u{after:03d}",
            f"unit:o012-rbt-u{before:03d}", "precedes", f"unit:o012-rbt-u{after:03d}",
            "Cumulative reader order.",
        )
    for lecture, context in unit_context.items():
        checks = sorted(
            local_id for local_id in context["anchor_start"] if f"o012-rbt-l{lecture:02d}-mcheck-" in local_id
        )
        solutions = sorted(
            local_id for local_id in context["anchor_start"] if f"o012-rbt-l{lecture:02d}-sol-" in local_id
        )
        hints = sorted(
            local_id for local_id in context["anchor_start"] if f"o012-rbt-l{lecture:02d}-hint-" in local_id
        )
        if len(checks) != len(solutions) or any(f"{number:03d}" not in solution for number, solution in enumerate(solutions, 1) for _ in [0]):
            raise SystemExit(f"Unit {lecture:03d} mastery check/solution census mismatch")
        if hints and len(hints) != len(checks):
            raise SystemExit(f"Unit {lecture:03d} mastery hint census mismatch")
        for number, (check, solution) in enumerate(zip(checks, solutions), 1):
            add_relation(
                f"relation:solves:l{lecture:02d}-sol-{number:03d}:l{lecture:02d}-mcheck-{number:03d}",
                f"unit:{solution}", "solves", f"unit:{check}",
                f"Complete solution to Mastery Check {lecture}.{number}.",
            )
            if hints:
                add_relation(
                    f"relation:hints:l{lecture:02d}-hint-{number:03d}:l{lecture:02d}-mcheck-{number:03d}",
                    f"unit:{hints[number - 1]}", "hints", f"unit:{check}",
                    f"Bounded hint for Mastery Check {lecture}.{number}.",
                )
    # Unit 14 explicitly declares its two source exercises solved by checks
    # 14.2 and 14.3; this preserves the source/mastery mapping without treating
    # every original exercise as a newly authored prompt.
    for solution_number, source_number in ((2, 1), (3, 2)):
        add_relation(
            f"relation:solves:l14-sol-{solution_number:03d}:l14-ex-{source_number:03d}",
            f"unit:o012-rbt-l14-sol-{solution_number:03d}", "solves",
            f"unit:o012-rbt-l14-ex-{source_number:03d}",
            f"Mastery solution 14.{solution_number} closes source exercise 14.{source_number}.",
        )
    for context in unit_context.values():
        for local_id in context["anchor_start"]:
            unit_id = f"unit:{local_id}"
            for alias in units[unit_id].get("source_aliases", []):
                safe_alias = re.sub(r"[^a-z0-9]+", "-", alias.lower()).strip("-")
                add_relation(
                    f"relation:xref:{local_id}:{safe_alias}", unit_id, "xref", EDITION_ID,
                    f"Preserves the upstream source label {alias} for later cross-reference resolution.",
                )

    # Adverse-ledger closure and correction records.
    with LEDGER.open("r", encoding="utf-8", newline="") as stream:
        all_ledger_rows = list(csv.DictReader(stream))
    if any(None in row or len(row) != 7 for row in all_ledger_rows):
        raise SystemExit("adverse ledger contains a non-canonical row")
    selected_ids = {f"O012-ADV-{number:04d}" for number in EVENT_LECTURE}
    ledger_rows = {row["event_id"]: row for row in all_ledger_rows if row["event_id"] in selected_ids}
    if set(ledger_rows) != selected_ids:
        raise SystemExit(f"adverse subset mismatch: {sorted(selected_ids - set(ledger_rows))}")
    for event_id, row in ledger_rows.items():
        number = int(event_id[-4:])
        lecture = unit_for_event(number)
        context = unit_context[lecture]
        affected_local_ids = EVENT_TARGETS[number]
        for local_id in affected_local_ids:
            if local_id not in context["anchor_start"]:
                raise SystemExit(f"{event_id}: target anchor absent: {local_id}")
        source_lines = parse_source_locations(row["source_location"])
        if source_lines and not all(context["spec"]["upstream_start"] <= line <= context["spec"]["upstream_end"] for line in source_lines):
            raise SystemExit(f"{event_id}: Notes.tex locator escapes Unit {lecture:03d} source span")
        target_spans = [f"{context['spans'][local_id][0]}-{context['spans'][local_id][1]}" for local_id in affected_local_ids]
        record_id = f"correction:o012-u{lecture:03d}-adv-{number:04d}"
        record = common("correction", record_id)
        record.update({
            "adverse_ledger_id": event_id,
            "affected_unit_ids": [f"unit:{local_id}" for local_id in affected_local_ids],
            "correction_type": correction_type(row["status"]), "edition_id": EDITION_ID,
            "evidence": f"{row['source_location']}; target spans {', '.join(target_spans)}.",
            "evidence_segment_id": f"segment:o012-rbt-l{lecture:02d}-notice",
            "severity": row["severity"], "rationale": row["rationale"],
            "resource_id": RESOURCE_ID, "source_defect": row["observed"],
            "target_change": row["action"], "unit_id": context["root_id"],
            "upstream_report_disposition": "not_contacted",
        })
        put_new(corrections, record)

    # Add only the explicit review/source-audit artifacts that exist and match
    # their frozen identities.  No cumulative build placeholder is generated.
    review_artifact_ids: dict[int, str] = {}
    for artifact_id, (relative, expected_bytes, expected_sha, media_type, unit_id, state) in ARTIFACT_META.items():
        path = LANE / relative
        raw = path.read_bytes()
        if len(raw) != expected_bytes or digest(raw) != expected_sha:
            raise SystemExit(f"artifact identity mismatch: {relative}")
        record = common("artifact", artifact_id)
        record.update({
            "bytes": expected_bytes, "locale": "id-ID", "manifest_artifact_id": None,
            "media_type": media_type, "path": relative, "qa_event_ids": [],
            "rights_component_id": CUMULATIVE_RIGHTS, "sha256": expected_sha,
            "toolchain": "Independent bounded source/review evidence; no build assertion.",
            "translation_state": state, "unit_id": unit_id,
        })
        put_new(artifacts, record)
        match = re.search(r"artifact:o012-u(\d{3})-independent-review$", artifact_id)
        if match:
            review_artifact_ids[int(match.group(1))] = artifact_id

    for lecture in SOURCE_SPECS:
        review_id = review_artifact_ids[lecture]
        for kind, qa_type, note in (
            ("source-integrity", "source", f"Unit {lecture:03d} exact source identity, contiguous upstream span, stable IDs, structural closure, and adverse/terminology scope passed."),
            ("math-review", "math", f"Independent Unit {lecture:03d} review passed with no open P1, P2, or P3 finding."),
            ("language-review", "language", f"Independent Unit {lecture:03d} Indonesian-language and controlled-terminology review passed."),
        ):
            qa_id = f"qa:o012-u{lecture:03d}-{kind}"
            event = common("qa_event", qa_id)
            witnesses = [review_id]
            if kind == "source-integrity":
                for candidate in (f"artifact:o012-u{lecture:03d}-source-audit",):
                    if candidate in artifacts:
                        witnesses.append(candidate)
                qa_artifact = f"artifact:o012-u{lecture:03d}-qa"
                if qa_artifact in artifacts:
                    witnesses.append(qa_artifact)
            event.update({"note": note, "qa_type": qa_type, "result": "passed", "unit_id": f"unit:o012-rbt-u{lecture:03d}", "witness_artifact_ids": witnesses})
            put_new(qa_events, event)

    qa_by_artifact: dict[str, list[str]] = defaultdict(list)
    for record_id, event in qa_events.items():
        for witness in event.get("witness_artifact_ids", []):
            qa_by_artifact[witness].append(record_id)
    for artifact_id, record in artifacts.items():
        if artifact_id in ARTIFACT_META:
            record["qa_event_ids"] = sorted(set(qa_by_artifact.get(artifact_id, [])))

    # New cumulative rights boundary.  Existing authority/rights records may
    # change only in the exact fields below; all other historical bytes remain.
    expected_old = {
        PROGRAM_ID: {"rights_component_id": OLD_CUMULATIVE_RIGHTS},
        COURSE_ID: {"rights_component_id": OLD_CUMULATIVE_RIGHTS},
        EDITION_ID: {
            "source_line_end": 3046,
            "local_derivative_unit_ids": [f"unit:o012-rbt-u{n:03d}" for n in range(1, 14)],
        },
        ROBERTS_RIGHTS: {
            "component_scope": [f"unit:o012-rbt-l{n:02d}" for n in range(1, 14)],
        },
    }
    for record_id, fields in expected_old.items():
        if record_id not in all_records:
            raise SystemExit(f"missing authority/rights boundary record: {record_id}")
        for field, expected in fields.items():
            if all_records[record_id].get(field) != expected:
                raise SystemExit(f"unexpected pre-boundary value {record_id}.{field}")
    cumulative = common("rights", CUMULATIVE_RIGHTS)
    cumulative.update({
        "attribution": "Cumulative Units 001-019 reader: David Michael Roberts source adaptations plus independently authored Indonesian companions; component provenance remains separated.",
        "change_notice": "Cumulative staged boundary only; Units 001-019 component rights records remain controlling.",
        "component_scope": [f"unit:o012-rbt-u{n:03d}" for n in range(1, 20)],
        "license_expression": "CC-BY-4.0", "license_url": "https://creativecommons.org/licenses/by/4.0/",
        "non_endorsement": "Independent edition; no source-author endorsement.",
        "third_party_status": "Component-scoped rights records control.",
    })
    put_new(rights, cumulative)
    authority[PROGRAM_ID]["rights_component_id"] = CUMULATIVE_RIGHTS
    authority[COURSE_ID]["rights_component_id"] = CUMULATIVE_RIGHTS
    authority[EDITION_ID]["local_derivative_unit_ids"] = [f"unit:o012-rbt-u{n:03d}" for n in range(1, 20)]
    authority[EDITION_ID]["source_line_end"] = 3947
    rights[ROBERTS_RIGHTS]["component_scope"] = [f"unit:o012-rbt-l{n:02d}" for n in range(1, 20)]
    rights[ROBERTS_RIGHTS]["third_party_status"] = "No distinct third-party component is asserted within Units 001-019; the frozen archive remains authoritative for file-level review."
    for record_id in (PROGRAM_ID, COURSE_ID, EDITION_ID, ROBERTS_RIGHTS):
        authority.get(record_id, rights.get(record_id))["timestamp"] = TIMESTAMP

    # Referential integrity over all records, including every newly added
    # anchor, term, correction, relation, QA witness, and rights component.
    scalar_references = {"concept_id", "course_id", "edition_id", "evidence_segment_id", "from_id", "local_derivative_unit_id", "manifest_artifact_id", "parent_id", "program_id", "resource_id", "rights_component_id", "scope_unit_id", "to_id", "unit_id"}
    list_references = {"affected_unit_ids", "additional_evidence_segment_ids", "component_scope", "concept_ids", "local_derivative_unit_ids", "qa_event_ids", "witness_artifact_ids"}
    for record_id, record in all_records.items():
        for field in scalar_references:
            value = record.get(field)
            if value is not None and value not in all_records:
                raise SystemExit(f"unknown backend reference {record_id}.{field}={value}")
        for field in list_references:
            if field in record:
                value = record[field]
                if not isinstance(value, list) or any(item not in all_records for item in value):
                    raise SystemExit(f"unknown/list backend reference {record_id}.{field}")

    for lecture, context in unit_context.items():
        spec = context["spec"]
        for local_id in context["anchor_start"]:
            start, end = context["spans"][local_id]
            expected = {
                "content_sha256": digest(b"".join(context["raw_lines"][start - 1:end])),
                "file_sha256": spec["sha256"], "line_end": end, "line_start": start,
                "path": spec["relative"],
            }
            if units[f"unit:{local_id}"]["target_locator"] != expected or segments[f"segment:{local_id}"]["target_locator"] != expected:
                raise SystemExit(f"Unit {lecture:03d} target locator mismatch: {local_id}")
            if local_id not in context["text_lines"][start - 1]:
                raise SystemExit(f"Unit {lecture:03d} anchor mismatch: {local_id}")

    # Verify all mastery relations, source-exercise closure, and one-to-one
    # correction inventories before touching disk.
    for lecture, context in unit_context.items():
        checks = {f"unit:{local_id}" for local_id in context["anchor_start"] if f"o012-rbt-l{lecture:02d}-mcheck-" in local_id}
        solutions = {f"unit:{local_id}" for local_id in context["anchor_start"] if f"o012-rbt-l{lecture:02d}-sol-" in local_id}
        solved = [record for record in relations.values() if record.get("relation_type") == "solves" and record.get("to_id") in checks]
        if Counter(record["to_id"] for record in solved) != Counter({item: 1 for item in checks}):
            raise SystemExit(f"Unit {lecture:03d} mastery exercise closure mismatch")
        if {record["from_id"] for record in solved if record["from_id"] in solutions} != solutions:
            raise SystemExit(f"Unit {lecture:03d} mastery solution coverage mismatch")
    expected_by_unit = {lecture: {f"O012-ADV-{number:04d}" for number, owner in EVENT_LECTURE.items() if owner == lecture} for lecture in SOURCE_SPECS}
    for lecture, expected in expected_by_unit.items():
        actual = {record.get("adverse_ledger_id") for record in corrections.values() if record.get("unit_id") == f"unit:o012-rbt-u{lecture:03d}"}
        if actual != expected:
            raise SystemExit(f"Unit {lecture:03d} adverse inventory mismatch")

    # Ensure no historical record changed outside the explicit boundary.  For
    # allowed records only the listed fields plus timestamp may differ.
    allowed_existing = {PROGRAM_ID, COURSE_ID, EDITION_ID, ROBERTS_RIGHTS}
    allowed_fields = {
        PROGRAM_ID: {"rights_component_id", "timestamp"},
        COURSE_ID: {"rights_component_id", "timestamp"},
        EDITION_ID: {"local_derivative_unit_ids", "source_line_end", "timestamp"},
        ROBERTS_RIGHTS: {"component_scope", "third_party_status", "timestamp"},
    }
    for record_id, before in old_snapshot.items():
        after = all_records[record_id]
        if before == after:
            continue
        if record_id not in allowed_existing:
            raise SystemExit(f"historical record changed outside explicit boundary: {record_id}")
        changed = {key for key in set(before) | set(after) if before.get(key) != after.get(key)}
        if not changed <= allowed_fields[record_id]:
            raise SystemExit(f"unauthorized fields changed in historical record {record_id}: {sorted(changed)}")

    # Construct sorted JSONL bytes while retaining the original byte line for
    # every unchanged historical record.  This is the key non-destructive
    # invariant: canonicalization never rewrites old records merely because new
    # records were added.
    serialized: dict[str, bytes] = {}
    for filename, records in record_sets.items():
        old = prior_lines[filename]
        lines: list[bytes] = []
        for record_id in sorted(records):
            if record_id in old and record_id not in allowed_existing:
                lines.append(old[record_id])
            else:
                lines.append(canonical(records[record_id]).encode("utf-8") + b"\n")
        raw = b"".join(lines)
        if b"\r" in raw or not raw.endswith(b"\n"):
            raise SystemExit(f"noncanonical generated bytes: {filename}")
        if [json.loads(line)["id"] for line in raw.splitlines()] != sorted(records):
            raise SystemExit(f"generated ID order mismatch: {filename}")
        serialized[filename] = raw

    # No file is opened for writing before this final count/hash report has
    # been calculated.  The writes are intentionally the final operations.
    total_bytes = 0
    bundle = hashlib.sha256()
    for filename in JSONL_NAMES:
        total_bytes += len(serialized[filename])
        bundle.update(filename.encode("utf-8")); bundle.update(b"\0"); bundle.update(serialized[filename])
    for filename, raw in serialized.items():
        (BACKEND / filename).write_bytes(raw)
    print("Units 014-019 backend extension: PASS")
    for lecture, spec in SOURCE_SPECS.items():
        print(f"unit_{lecture:03d}_stable_ids: {spec['expected_ids']}")
    print(f"terminology_controls: {len(TERM_SPECS)}")
    print(f"adverse_ledger_records: {len(EVENT_LECTURE)}")
    print(f"review_source_artifacts: {len(ARTIFACT_META)}")
    print(f"new_records: {len(owned_new_ids)}")
    print(f"jsonl_files: {len(JSONL_NAMES)}")
    print(f"backend_bytes: {total_bytes}")
    print(f"backend_bundle_sha256: {bundle.hexdigest()}")


if __name__ == "__main__":
    build()
