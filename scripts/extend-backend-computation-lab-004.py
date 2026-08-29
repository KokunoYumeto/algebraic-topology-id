#!/usr/bin/env python3
"""Build a fail-closed, isolated append-only backend candidate for D60-LAB04.

This producer never writes to ``backend/``.  It seals the exact cumulative
Lab 3 boundary, builds the Lab 4 semantic suffix twice in isolated directories,
validates each merged candidate, and proves byte-identical replay.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "scripts/extend-backend-computation-lab-003.py"
BASE_RAW = BASE.read_bytes()
BASE_IDENTITY = (
    len(BASE_RAW),
    BASE_RAW.count(b"\n"),
    hashlib.sha256(BASE_RAW).hexdigest(),
)
if BASE_IDENTITY != (
    36_992,
    520,
    "8e1c6cfd56a3ad9c73302a54e08d3147a03c9c68f46af32bb3b27e4a701828b2",
):
    raise RuntimeError("frozen Lab 3 backend producer identity drift")
SPEC = importlib.util.spec_from_file_location("o012_lab03_backend_base", BASE)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot load the frozen Lab 3 backend producer")
base = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = base
SPEC.loader.exec_module(base)
m = base.m


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"Lab 4 backend candidate FAIL: {message}")


m.require = require
m.TIMESTAMP = "2026-08-29T00:00:00Z"
m.LAB_ID = "D60-LAB04"
m.EDITION_UNIT_ID = "O012-ORIG-LAB04"
m.LOCAL_ROOT = "o012-d60-lab04"
m.ROOT_UNIT = "unit:o012-d60-lab04"
m.LAB_RIGHTS = "rights:o012-d60-lab04-original-cc-by-sa-4.0"
m.ROUTES = ("D60-R04", "D60-R05", "D60-R12", "D60-R13", "D60-R14")
m.SOURCE_PATH = "source/id-ID/labs/computation-lab-004-cross-invariant-comparison.md"
m.PROGRAM_PATH = "source/id-ID/labs/o012_d60_lab04_cross_invariants.py"
m.TEST_PATH = "source/id-ID/labs/test_o012_d60_lab04_cross_invariants.py"
m.EXPECTED_PATH = "source/id-ID/labs/expected-output-lab04.txt"
m.STATIC_PATH = "qa/computation-lab-004/STATIC_QA.json"
m.CODE_PATH = "qa/computation-lab-004/INDEPENDENT_CODE_REVIEW.json"
m.MATH_PATH = "qa/computation-lab-004/INDEPENDENT_MATH_REVIEW.json"
m.LANGUAGE_PATH = "qa/computation-lab-004/INDEPENDENT_SOURCE_LANGUAGE_REVIEW.json"
m.EXECUTION_PATH = "qa/computation-lab-004/EXECUTION_RECEIPT.json"
m.COMBINED_PATH = "qa/COMPUTATION_LAB_004_QA.json"
m.BASELINE_RECEIPT_PATH = "qa/BACKEND_APPEND_ONLY_COMPUTATION_LAB_003_CUMULATIVE_RECEIPT.json"
m.BASELINE_RECEIPT_IDENTITY = (
    10_047,
    280,
    "7ee69a9291368d407e38de4c63440d599b5cd13ec5fc288f5468084bc7774c80",
)
m.PREFIX = {
    "artifacts.jsonl": (234, 193_675, "1535c6096f79fcd84878dca9d918e16e130571fa1f5423a210db55e3b62a782f"),
    "assets.jsonl": (87, 64_692, "1df40f8f6ca4f2fbfbe8a7b924a68a153713a20a4eebe1d014d8fb04669945f7"),
    "authority.jsonl": (6, 4_374, "84c622f56dbbd5ba379361245ecfe07bc79c9f4fd6b18ba21b82b5f545211869"),
    "concepts.jsonl": (513, 162_561, "5b921e4bb055fa53cd7f017d5d72b43a0122e5a31b5b8ec760b6efc4ca7e7fcc"),
    "corrections.jsonl": (564, 594_720, "bd961fad5d83e96fec6ef83caa8447e2e5f282c603fd4983d79b5b4b54049fbb"),
    "qa.jsonl": (198, 109_899, "1a1eb9f45ea992496a536a0f9bac0c439bfda9d6e10de1a292329727372e0a54"),
    "relations.jsonl": (1_216, 555_459, "0504529956092a8d78f334f6cdf2dbceaa5a319ac09f812d1ccfa09d9b4f2cf0"),
    "rights.jsonl": (110, 105_027, "73fdb740a3867d2cf74c6c84c9cce4f99b8feef39ccf5d5b900425cc46cdf872"),
    "segments.jsonl": (2_115, 3_480_791, "24d76e94204df4d87100ce4394e4c534c0cbdf45897d6f29c9ef0bc66418de67"),
    "terms.jsonl": (506, 338_679, "394f877bcd0e0e537cdf09d1634185425d3fa2af6ba2c4fd955ff392dfc79214"),
    "units.jsonl": (2_145, 3_670_508, "93fc6a9bde31abf13d909e2dad66ad18d57738c326706897fd271c80fec70ecc"),
}
m.PREFIX_TOTAL = (
    7_694,
    9_280_385,
    "cddd65499da547e0c4f01b8a880f68d1c3d314c078a9179528e4a28b2c5f65a2",
)
m.LEARNER_PATHS = (m.SOURCE_PATH, m.PROGRAM_PATH, m.TEST_PATH, m.EXPECTED_PATH)
m.REVIEW_PATHS = (m.CODE_PATH, m.MATH_PATH, m.LANGUAGE_PATH)
m.EVIDENCE_PATHS = (
    m.STATIC_PATH, m.CODE_PATH, m.MATH_PATH, m.LANGUAGE_PATH,
    m.EXECUTION_PATH, m.COMBINED_PATH,
)
m.INPUT_PATHS = (*m.LEARNER_PATHS, m.TERMINOLOGY_PATH, *m.EVIDENCE_PATHS)

m.ID_KINDS = {
    m.LOCAL_ROOT: ("reader_unit", "laboratory"),
    f"{m.LOCAL_ROOT}-status": ("section", "status"),
    f"{m.LOCAL_ROOT}-prerequisites": ("section", "prerequisites"),
    f"{m.LOCAL_ROOT}-objectives": ("section", "objectives"),
    f"{m.LOCAL_ROOT}-data": ("section", "data"),
    f"{m.LOCAL_ROOT}-comparison-principles": ("section", "derivation"),
    **{f"{m.LOCAL_ROOT}-task-{number:03d}": ("exercise", "exercise") for number in range(1, 7)},
    f"{m.LOCAL_ROOT}-hint": ("hint", "hint"),
    f"{m.LOCAL_ROOT}-program": ("source_code", "source_code"),
    f"{m.LOCAL_ROOT}-tests": ("test_suite", "test_suite"),
    f"{m.LOCAL_ROOT}-expected-output": ("expected_output", "expected_output"),
    f"{m.LOCAL_ROOT}-interpretation": ("interpretation", "interpretation"),
    f"{m.LOCAL_ROOT}-solution": ("solution", "solution"),
    f"{m.LOCAL_ROOT}-sol-execution": ("section", "solution_section"),
    f"{m.LOCAL_ROOT}-sol-cellular-pair-a": ("section", "solution_section"),
    f"{m.LOCAL_ROOT}-sol-pi1-cup-pair-a": ("section", "solution_section"),
    f"{m.LOCAL_ROOT}-sol-pair-b": ("section", "solution_section"),
    f"{m.LOCAL_ROOT}-sol-negative": ("section", "solution_section"),
    f"{m.LOCAL_ROOT}-reproducibility": ("verification", "verification"),
    f"{m.LOCAL_ROOT}-rights": ("rights_notice", "rights_notice"),
}

m.TERM_SPECS = (
    (515, "cross-invariant comparison", "perbandingan lintas-invarian", "algebraic_topology", f"{m.LOCAL_ROOT}-comparison-principles", "controlled comparison that keeps fundamental-group, homology, additive-cohomology, and ring evidence separately typed"),
    (516, "free reduction", "reduksi bebas", "combinatorial_group_theory", f"{m.LOCAL_ROOT}-comparison-principles", "cancellation of adjacent inverse letters in a free-group word without commuting unrelated letters"),
    (517, "exponent-sum vector", "vektor jumlah eksponen", "combinatorial_group_theory", f"{m.LOCAL_ROOT}-sol-cellular-pair-a", "signed total of each generator in a relator; it records the induced abelian relation and cellular incidence in the one-vertex two-complex"),
    (518, "abelianization information loss", "kehilangan informasi akibat abelianisasi", "algebraic_topology", f"{m.LOCAL_ROOT}-sol-pi1-cup-pair-a", "passage from pi1 to H1 retains the maximal abelian quotient but can erase nontrivial commutators"),
    (519, "additive cohomology", "kohomologi aditif", "algebraic_topology", f"{m.LOCAL_ROOT}-comparison-principles", "the graded cohomology groups considered without their cup-product multiplication"),
    (520, "cohomology ring", "gelanggang kohomologi", "algebraic_topology", f"{m.LOCAL_ROOT}-comparison-principles", "graded ring comprising cohomology groups together with the unit and cup product"),
    (521, "sparse cup-product table", "tabel produk cup jarang", "computational_topology", f"{m.LOCAL_ROOT}-objectives", "deterministic basis table that stores only nonzero products while still checking unit, degree, associativity, and graded commutativity"),
    (522, "Hopf invariant", "invarian Hopf", "algebraic_topology", f"{m.LOCAL_ROOT}-sol-pair-b", "integer H(f) characterized here by x cup x = H(f)u for the two-cell complex S^2 with a 4-cell attached by f"),
    (523, "cup-square coefficient", "koefisien kuadrat cup", "algebraic_topology", f"{m.LOCAL_ROOT}-sol-pair-b", "integer multiplying the oriented top class in the square of a degree-two cohomology generator"),
    (524, "attaching-map information loss", "hilangnya informasi peta pelekatan", "cellular_homology", f"{m.LOCAL_ROOT}-sol-negative", "phenomenon that a cellular differential can vanish because the adjacent chain group is zero even when the attaching map is non-null-homotopic"),
    (525, "first separating invariant", "invarian pemisah pertama", "computational_topology", f"{m.LOCAL_ROOT}-interpretation", "first unequal entry in an explicitly declared audit order; it is not a universal ranking of invariants"),
    (526, "finite-invariant inference boundary", "batas inferensi daftar invarian terbatas", "mathematical_method", f"{m.LOCAL_ROOT}-interpretation", "rule that disagreement proves non-equivalence while agreement of a finite selected signature does not prove homotopy equivalence"),
)
m.EXISTING_CONCEPTS = {
    "concept:abelianization", "concept:attaching-map", "concept:fundamental-class",
    "concept:fundamental-group", "concept:group-presentation", "concept:homology",
    "concept:homotopy-equivalence", "concept:o012-d60-lab03-term-0513",
    "concept:wedge-sum",
}
m.NEW_CONCEPTS = {
    number: f"concept:{m.LOCAL_ROOT}-term-{number:04d}" for number, *_ in m.TERM_SPECS
}
m.ALL_LAB_CONCEPTS = tuple(sorted(m.EXISTING_CONCEPTS | set(m.NEW_CONCEPTS.values())))
m.ROUTE_ANCHORS = {
    "D60-R04": "unit:o012-rbt-l10",
    "D60-R05": "unit:o012-rbt-l13",
    "D60-R12": "unit:o012-fom-u007",
    "D60-R13": "unit:o012-rbt-l26",
    "D60-R14": "unit:o012-rbt-l30",
}
ANCHOR_ROUTES: dict[str, tuple[str, ...]] = {
    "unit:o012-d60-lab03": ("D60-R12", "D60-R14"),
    "unit:o012-d60-lab03-cellular-boundaries": ("D60-R12", "D60-R14"),
    "unit:o012-fom-u001-rem-013": ("D60-R08",),
    "unit:o012-fom-u006-mcheck-001": ("D60-R12",),
    "unit:o012-fom-u007": ("D60-R12",),
    "unit:o012-rbt-l10": ("D60-R04",),
    "unit:o012-rbt-l13": ("D60-R05",),
    "unit:o012-rbt-l13-s04": ("D60-R05",),
    "unit:o012-rbt-l13-s05": ("D60-R05",),
    "unit:o012-rbt-l26": ("D60-R13",),
    "unit:o012-rbt-l26-s02": ("D60-R13",),
    "unit:o012-rbt-l30": ("D60-R14",),
}
TASK_DEPENDENCIES: dict[int, tuple[str, ...]] = {
    1: ("unit:o012-d60-lab03",),
    2: ("unit:o012-rbt-l13-s05", "unit:o012-fom-u007", "unit:o012-d60-lab03-cellular-boundaries"),
    3: ("unit:o012-rbt-l10", "unit:o012-rbt-l13-s04", "unit:o012-fom-u001-rem-013"),
    4: ("unit:o012-rbt-l26-s02", "unit:o012-d60-lab03-cellular-boundaries"),
    5: ("unit:o012-fom-u006-mcheck-001", "unit:o012-rbt-l26-s02", "unit:o012-d60-lab03-cellular-boundaries"),
    6: ("unit:o012-rbt-l10", "unit:o012-rbt-l13", "unit:o012-fom-u007", "unit:o012-rbt-l26", "unit:o012-rbt-l30"),
}


def verify_baseline_receipt() -> dict[str, Any]:
    raw = m.disciplined(m.BASELINE_RECEIPT_PATH)
    require(m.identity(raw) == m.BASELINE_RECEIPT_IDENTITY, "baseline cumulative receipt identity drift")
    baseline = json.loads(raw)
    cumulative = baseline.get("cumulative", {})
    replay = baseline.get("replay", {})
    require(
        baseline.get("status") == "PASS"
        and baseline.get("receipt_kind") == "cumulative_backend_boundary"
        and baseline.get("laboratory_id") == "D60-LAB03"
        and (cumulative.get("records"), cumulative.get("bytes"), cumulative.get("bundle_sha256")) == m.PREFIX_TOTAL
        and cumulative.get("computation_laboratories_complete") == 3
        and cumulative.get("computation_laboratories_required") == 4
        and replay.get("status") == "PASS"
        and replay.get("exact_file_matches") == len(m.FILES)
        and replay.get("temporary_replay_removed") is True,
        "baseline receipt does not prove the exact Lab 3 cumulative boundary",
    )
    return baseline


def verify_inputs(sealed: dict[str, tuple[int, int, str]] | None = None) -> dict[str, Any]:
    raw = {relative: m.disciplined(relative) for relative in m.INPUT_PATHS}
    identities = {relative: m.identity(value) for relative, value in raw.items()}
    if sealed is not None:
        require(identities == sealed, "sealed input identity drift")
    combined = json.loads(raw[m.COMBINED_PATH])
    require(
        combined.get("status") == "PASS"
        and combined.get("receipt_kind") == "computation_laboratory_source_execution_review_closure"
        and combined.get("laboratory_id") == m.LAB_ID
        and combined.get("edition_unit_id") == m.EDITION_UNIT_ID
        and combined.get("course_route_unit_ids") == list(m.ROUTES)
        and combined.get("model_provenance") == m.MODEL
        and combined.get("human_review_claimed") is False,
        "combined QA is not the final Lab 4 closure",
    )
    require(combined.get("severity_census") == {"P1": 0, "P2": 0, "P3": 0}, "combined QA findings remain")
    checks = combined.get("checks", {})
    require(checks.get("excluded_fomberg_problem_bank_used") is False, "excluded problem-bank use claimed")
    require(checks.get("route_scope_D60_R04_R05_R12_R13_R14") == "PASS", "combined QA route scope incomplete")
    require(checks.get("stable_ids_25_unique") == "PASS" and checks.get("tasks_6_with_hint_and_complete_solution") == "PASS", "combined QA mastery closure incomplete")
    bound: dict[str, tuple[int, int, str]] = {}
    m.identity_index(combined, bound)
    for relative in (*m.LEARNER_PATHS, m.TERMINOLOGY_PATH, m.STATIC_PATH, *m.REVIEW_PATHS, m.EXECUTION_PATH):
        require(bound.get(relative) == identities[relative], f"combined QA does not bind current {relative}")
    static = json.loads(raw[m.STATIC_PATH])
    require(
        static.get("status") == "PASS"
        and static.get("laboratory_id") == m.LAB_ID
        and static.get("edition_unit_id") == m.EDITION_UNIT_ID
        and static.get("course_route_unit_ids") == list(m.ROUTES)
        and static.get("severity_counts") == {"P1": 0, "P2": 0, "P3": 0}
        and static.get("structure", {}).get("stable_ids") == 25
        and static.get("structure", {}).get("tasks") == 6,
        "static QA mismatch",
    )
    review_contracts = {
        m.CODE_PATH: ("independent_code", {m.SOURCE_PATH, m.PROGRAM_PATH, m.TEST_PATH, m.EXPECTED_PATH, m.STATIC_PATH}),
        m.MATH_PATH: ("independent_mathematics", {m.SOURCE_PATH, m.PROGRAM_PATH, m.TEST_PATH, m.EXPECTED_PATH, m.STATIC_PATH}),
        m.LANGUAGE_PATH: ("independent_source_language", {m.SOURCE_PATH, m.PROGRAM_PATH, m.TEST_PATH, m.EXPECTED_PATH, m.TERMINOLOGY_PATH}),
    }
    for relative, (kind, expected_paths) in review_contracts.items():
        receipt = json.loads(raw[relative])
        require(
            receipt.get("status") == "PASS"
            and receipt.get("review_kind") == kind
            and receipt.get("laboratory_id") == m.LAB_ID
            and (
                receipt.get("edition_unit_id") == m.EDITION_UNIT_ID
                or (kind == "independent_code" and "edition_unit_id" not in receipt)
            )
            and receipt.get("course_route_unit_ids") == list(m.ROUTES)
            and receipt.get("independent_from_production") is True
            and receipt.get("reader_sha256") == identities[m.SOURCE_PATH][2]
            and receipt.get("human_review_claimed") is False
            and receipt.get("model_provenance") == m.MODEL
            and receipt.get("severity_census") == {"P1": 0, "P2": 0, "P3": 0},
            f"{kind} review mismatch",
        )
        review_bound: dict[str, tuple[int, int, str]] = {}
        for item in receipt.get("bound_artifacts", []):
            path = item.get("path")
            require(path in expected_paths and path not in review_bound, f"{kind} bound-artifact scope mismatch")
            review_bound[path] = (item.get("bytes"), item.get("lf_lines"), item.get("sha256"))
        require(review_bound == {path: identities[path] for path in expected_paths}, f"{kind} exact artifact binding mismatch")
    execution = json.loads(raw[m.EXECUTION_PATH])
    runtime = execution.get("runtime", {})
    require(
        execution.get("status") == "PASS"
        and execution.get("receipt_kind") == "offline_deterministic_execution"
        and execution.get("laboratory_id") == m.LAB_ID
        and execution.get("edition_unit_id") == m.EDITION_UNIT_ID
        and execution.get("course_route_unit_ids") == list(m.ROUTES)
        and execution.get("program_runs") == execution.get("test_runs") == 2
        and execution.get("tests_per_run") == 6
        and execution.get("all_exit_codes_zero") is True
        and execution.get("program_stdout_matches_expected_output") is True
        and execution.get("program_stdout_byte_identical_between_runs") is True
        and runtime.get("standard_library_only") is True
        and runtime.get("network_used") is False
        and execution.get("model_provenance") == m.MODEL
        and execution.get("severity_census") == {"P1": 0, "P2": 0, "P3": 0},
        "execution closure mismatch",
    )
    return {"raw": raw, "identities": identities, "combined": combined}


def concepts_for(local_id: str) -> list[str]:
    n = m.NEW_CONCEPTS
    exact: dict[str, tuple[str, ...]] = {
        f"{m.LOCAL_ROOT}-status": ("concept:fundamental-group", "concept:homology", n[515], n[518], n[519], n[520], n[524], n[526]),
        f"{m.LOCAL_ROOT}-prerequisites": ("concept:abelianization", "concept:attaching-map", "concept:group-presentation", "concept:o012-d60-lab03-term-0513", "concept:wedge-sum"),
        f"{m.LOCAL_ROOT}-objectives": (n[515], n[517], n[518], n[519], n[520], n[521], n[526]),
        f"{m.LOCAL_ROOT}-data": ("concept:attaching-map", "concept:fundamental-group", "concept:wedge-sum", n[522], n[524]),
        f"{m.LOCAL_ROOT}-comparison-principles": ("concept:abelianization", "concept:fundamental-group", "concept:homology", "concept:homotopy-equivalence", "concept:o012-d60-lab03-term-0513", n[515], n[516], n[517], n[518], n[519], n[520], n[522], n[523]),
        f"{m.LOCAL_ROOT}-task-001": (n[515], n[526]),
        f"{m.LOCAL_ROOT}-task-002": ("concept:group-presentation", "concept:homology", n[517], n[524]),
        f"{m.LOCAL_ROOT}-task-003": ("concept:abelianization", "concept:fundamental-group", n[516], n[518]),
        f"{m.LOCAL_ROOT}-task-004": ("concept:o012-d60-lab03-term-0513", n[519], n[520], n[521], n[525]),
        f"{m.LOCAL_ROOT}-task-005": ("concept:attaching-map", "concept:homology", n[522], n[523], n[524]),
        f"{m.LOCAL_ROOT}-task-006": ("concept:homotopy-equivalence", n[518], n[524], n[526]),
        f"{m.LOCAL_ROOT}-program": (n[515], n[516], n[517], n[521], n[525], n[526]),
        f"{m.LOCAL_ROOT}-tests": (n[516], n[517], n[521], n[523], n[526]),
        f"{m.LOCAL_ROOT}-expected-output": (n[515], n[517], n[522], n[525]),
        f"{m.LOCAL_ROOT}-interpretation": ("concept:abelianization", "concept:homotopy-equivalence", n[515], n[518], n[519], n[520], n[525], n[526]),
        f"{m.LOCAL_ROOT}-sol-cellular-pair-a": ("concept:attaching-map", "concept:homology", "concept:group-presentation", n[517], n[524]),
        f"{m.LOCAL_ROOT}-sol-pi1-cup-pair-a": ("concept:abelianization", "concept:fundamental-group", "concept:o012-d60-lab03-term-0513", n[516], n[518], n[519], n[520]),
        f"{m.LOCAL_ROOT}-sol-pair-b": ("concept:attaching-map", "concept:o012-d60-lab03-term-0513", n[522], n[523], n[524]),
        f"{m.LOCAL_ROOT}-sol-negative": ("concept:homology", "concept:homotopy-equivalence", n[518], n[524], n[526]),
        f"{m.LOCAL_ROOT}-rights": ("concept:homotopy-equivalence",),
    }
    if local_id in (m.LOCAL_ROOT, f"{m.LOCAL_ROOT}-hint", f"{m.LOCAL_ROOT}-solution", f"{m.LOCAL_ROOT}-sol-execution", f"{m.LOCAL_ROOT}-reproducibility"):
        return list(m.ALL_LAB_CONCEPTS)
    return list(exact.get(local_id, (n[515],)))


base_unit_record = m.unit_record


def unit_record(local_id: str, order: int, parsed: dict[str, Any]) -> dict[str, Any]:
    record = base_unit_record(local_id, order, parsed)
    record["course_route_unit_ids"] = list(m.ROUTES)
    record["authority_context_ids"] = [
        m.COURSE, m.PROGRAM, m.FOMBERG_EDITION, m.FOMBERG_RESOURCE,
        "edition:roberts-at-2019-b947ad2", "resource:roberts-algebraic-topology-2019",
    ]
    route_by_task = {
        1: ("D60-R04", ("D60-R05", "D60-R12", "D60-R13", "D60-R14")),
        2: ("D60-R12", ("D60-R05", "D60-R14")),
        3: ("D60-R04", ("D60-R05",)),
        4: ("D60-R13", ("D60-R14",)),
        5: ("D60-R12", ("D60-R13", "D60-R14")),
        6: ("D60-R14", ("D60-R04", "D60-R05", "D60-R12", "D60-R13")),
    }
    if local_id == m.LOCAL_ROOT:
        record["order"] = 45
        record["primary_course_route_unit_id"] = "D60-R04"
        record["secondary_course_route_unit_ids"] = ["D60-R05", "D60-R12", "D60-R13", "D60-R14"]
        record["reader_scope"] = "six_tasks_one_hint_full_solution_program_tests_expected_output_cross_invariant_synthesis"
    task = re.fullmatch(re.escape(m.LOCAL_ROOT) + r"-task-(\d{3})", local_id)
    if task:
        primary, secondary = route_by_task[int(task.group(1))]
        record["primary_course_route_unit_id"] = primary
        record["secondary_course_route_unit_ids"] = list(secondary)
    return record


def build_additions(data: dict[str, Any], parsed: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    order = {local_id: number for number, local_id in enumerate(m.ID_KINDS, 1)}
    units = [unit_record(local_id, order[local_id], parsed) for local_id in m.ID_KINDS]
    segments = [m.segment_from_unit(unit) for unit in units]
    concepts = [
        {**m.common("concept", m.NEW_CONCEPTS[number]), "canonical_label": source_term, "domain": domain, "locale_neutral": True}
        for number, source_term, _preferred, domain, _evidence, _note in m.TERM_SPECS
    ]
    terms = [
        {
            **m.common("term", f"term:{m.LOCAL_ROOT}-term-{number:04d}:id-ID"),
            "concept_id": m.NEW_CONCEPTS[number], "evidence_segment_id": f"segment:{evidence}",
            "locale": "id-ID", "preferred": preferred, "register": "textbook",
            "rejected_forms": [], "rights_component_id": m.LAB_RIGHTS,
            "scope_unit_id": m.ROOT_UNIT, "source_term": source_term,
            "terminology_control_id": f"O012-TERM-{number:04d}",
            "terminology_status": "admitted", "usage_note": note, "variants": [],
        }
        for number, source_term, preferred, _domain, evidence, note in m.TERM_SPECS
    ]
    rights = [{
        **m.common("rights", m.LAB_RIGHTS),
        "attribution": "Original D60-LAB04 computation laboratory prepared for the independent Indonesian O012/D60 edition.",
        "change_notice": "Edition-original laboratory layer; Roberts and Fomberg source components are neither copied nor relicensed.",
        "component_scope": [unit["id"] for unit in units],
        "license_expression": "CC-BY-SA-4.0",
        "license_url": "https://creativecommons.org/licenses/by-sa/4.0/",
        "non_endorsement": "Independent Indonesian edition; no source-author or institutional endorsement.",
        "third_party_status": "No excluded problem-bank expression is used; admitted authority IDs are mathematical context only.",
    }]
    qa_ids = {kind: f"qa:{m.LOCAL_ROOT}-{kind}" for kind in ("structure", "execution", "code", "math", "language", "mastery", "terminology")}
    artifacts = [
        m.artifact(f"artifact:{m.LOCAL_ROOT}-reader-source", m.SOURCE_PATH, "text/markdown", list(qa_ids.values()), "structurally_verified", data["identities"]),
        m.artifact(f"artifact:{m.LOCAL_ROOT}-python-source", m.PROGRAM_PATH, "text/x-python", [qa_ids["execution"], qa_ids["code"], qa_ids["mastery"]], "built", data["identities"]),
        m.artifact(f"artifact:{m.LOCAL_ROOT}-tests", m.TEST_PATH, "text/x-python", [qa_ids["execution"], qa_ids["code"]], "built", data["identities"]),
        m.artifact(f"artifact:{m.LOCAL_ROOT}-expected-output", m.EXPECTED_PATH, "text/plain", [qa_ids["execution"], qa_ids["code"]], "built", data["identities"]),
        m.artifact(f"artifact:{m.LOCAL_ROOT}-static-qa", m.STATIC_PATH, "application/json", [qa_ids["structure"], qa_ids["mastery"], qa_ids["terminology"]], "built", data["identities"]),
        m.artifact(f"artifact:{m.LOCAL_ROOT}-code-review", m.CODE_PATH, "application/json", [qa_ids["code"]], "built", data["identities"]),
        m.artifact(f"artifact:{m.LOCAL_ROOT}-math-review", m.MATH_PATH, "application/json", [qa_ids["math"]], "mathematically_reviewed", data["identities"]),
        m.artifact(f"artifact:{m.LOCAL_ROOT}-language-review", m.LANGUAGE_PATH, "application/json", [qa_ids["language"], qa_ids["terminology"]], "language_reviewed", data["identities"]),
        m.artifact(f"artifact:{m.LOCAL_ROOT}-execution-receipt", m.EXECUTION_PATH, "application/json", [qa_ids["execution"]], "built", data["identities"]),
        m.artifact(f"artifact:{m.LOCAL_ROOT}-qa-receipt", m.COMBINED_PATH, "application/json", list(qa_ids.values()), "built", data["identities"]),
    ]
    qa_events = [
        {**m.common("qa_event", qa_ids["structure"]), "laboratory_id": m.LAB_ID, "note": "Twenty-five stable IDs, six tasks, one hint, complete solutions, exact five-route scope, rights, provenance, and privacy checks passed.", "qa_type": "structure", "result": "passed", "unit_id": m.ROOT_UNIT, "witness_artifact_ids": [f"artifact:{m.LOCAL_ROOT}-reader-source", f"artifact:{m.LOCAL_ROOT}-static-qa", f"artifact:{m.LOCAL_ROOT}-qa-receipt"]},
        {**m.common("qa_event", qa_ids["execution"]), "laboratory_id": m.LAB_ID, "note": "The standard-library program and six-test suite each ran twice; stdout was deterministic and exact against frozen output.", "qa_type": "execution", "result": "passed", "unit_id": m.ROOT_UNIT, "witness_artifact_ids": [f"artifact:{m.LOCAL_ROOT}-python-source", f"artifact:{m.LOCAL_ROOT}-tests", f"artifact:{m.LOCAL_ROOT}-expected-output", f"artifact:{m.LOCAL_ROOT}-execution-receipt"]},
        {**m.common("qa_event", qa_ids["code"]), "laboratory_id": m.LAB_ID, "note": "Independent code review checked exact integer models, malformed-input rejection, ring-law validation, deterministic order, and offline execution with P1=P2=P3=0.", "qa_type": "code", "result": "passed", "unit_id": m.ROOT_UNIT, "witness_artifact_ids": [f"artifact:{m.LOCAL_ROOT}-code-review", f"artifact:{m.LOCAL_ROOT}-qa-receipt"]},
        {**m.common("qa_event", qa_ids["math"]), "laboratory_id": m.LAB_ID, "note": "Independent mathematics review recomputed both frozen comparison pairs, abelianizations, homology, Hopf and cup-product claims, and inference guardrails with P1=P2=P3=0.", "qa_type": "math", "result": "passed", "unit_id": m.ROOT_UNIT, "witness_artifact_ids": [f"artifact:{m.LOCAL_ROOT}-math-review", f"artifact:{m.LOCAL_ROOT}-qa-receipt"]},
        {**m.common("qa_event", qa_ids["language"]), "laboratory_id": m.LAB_ID, "note": "Independent final id-ID review passed the exact five-route scope, links, controlled terminology, executable claims, rights, and provenance.", "qa_type": "language", "result": "passed", "unit_id": m.ROOT_UNIT, "witness_artifact_ids": [f"artifact:{m.LOCAL_ROOT}-language-review", f"artifact:{m.LOCAL_ROOT}-qa-receipt"]},
        {**m.common("qa_event", qa_ids["mastery"]), "laboratory_id": m.LAB_ID, "note": "Six tasks share one stable hint and complete checked solutions covering cellular information loss, abelianization, cohomology rings, Hopf attachment, and negative inference controls.", "qa_type": "mastery", "result": "passed", "unit_id": m.ROOT_UNIT, "witness_artifact_ids": [f"artifact:{m.LOCAL_ROOT}-reader-source", f"artifact:{m.LOCAL_ROOT}-python-source", f"artifact:{m.LOCAL_ROOT}-static-qa"]},
        {**m.common("qa_event", qa_ids["terminology"]), "laboratory_id": m.LAB_ID, "note": "O012-TERM-0515 through O012-TERM-0526 map twelve controlled id-ID terms to locale-neutral concepts and exact evidence segments.", "qa_type": "terminology", "result": "passed", "unit_id": m.ROOT_UNIT, "witness_artifact_ids": [f"artifact:{m.LOCAL_ROOT}-language-review", f"artifact:{m.LOCAL_ROOT}-static-qa"]},
    ]
    relations = [
        m.relation("relation:contains:o012-d60:lab04", "contains", m.COURSE, m.ROOT_UNIT, "The O012/D60 course contains D60-LAB04 as an original computation laboratory.", laboratory_id=m.LAB_ID, course_route_unit_ids=list(m.ROUTES)),
        m.relation(f"relation:contains:{m.LOCAL_ROOT}-rights:root", "contains", m.LAB_RIGHTS, m.ROOT_UNIT, "The original CC BY-SA 4.0 component rights bind the complete D60-LAB04 graph.", laboratory_id=m.LAB_ID, rights_mapping_role="direct_component_binding"),
        m.relation("relation:contains:o012-d60-integrated-rights:lab04-original", "contains", m.INTEGRATED_RIGHTS, m.LAB_RIGHTS, "The integrated route contains the independently licensed D60-LAB04 component without altering source licenses.", laboratory_id=m.LAB_ID, rights_mapping_role="integrated_route_component"),
    ]
    for local_id in m.ID_KINDS:
        if local_id != m.LOCAL_ROOT:
            relations.append(m.relation(f"relation:contains:{m.LOCAL_ROOT}:{local_id.removeprefix(m.LOCAL_ROOT + '-')}", "contains", m.ROOT_UNIT, f"unit:{local_id}", f"D60-LAB04 contains learner surface {local_id}.", laboratory_id=m.LAB_ID))
    hint = f"unit:{m.LOCAL_ROOT}-hint"
    solution = f"unit:{m.LOCAL_ROOT}-solution"
    for number in range(1, 7):
        exercise = f"unit:{m.LOCAL_ROOT}-task-{number:03d}"
        relations.append(m.relation(f"relation:hints:{m.LOCAL_ROOT}-hint:task-{number:03d}", "hints", hint, exercise, f"Shared stable hint for D60-LAB04 task {number}.", laboratory_id=m.LAB_ID, laboratory_task_number=number))
        relations.append(m.relation(f"relation:solves:{m.LOCAL_ROOT}-solution:task-{number:03d}", "solves", solution, exercise, f"Complete checked solution for D60-LAB04 task {number}.", laboratory_id=m.LAB_ID, laboratory_task_number=number, solution_status="complete_checked_solution"))
        for dep_order, anchor in enumerate(TASK_DEPENDENCIES[number], 1):
            slug = re.sub(r"[^a-z0-9]+", "-", anchor.lower()).strip("-")
            routes = list(ANCHOR_ROUTES[anchor])
            relations.append(m.relation(
                f"relation:depends-on:{m.LOCAL_ROOT}-task-{number:03d}:{dep_order:02d}:{slug}",
                "depends-on", exercise, anchor,
                f"D60-LAB04 task {number} requires admitted prerequisite {anchor}.",
                laboratory_id=m.LAB_ID, laboratory_task_number=number,
                dependency_order=dep_order, dependency_role="laboratory_prerequisite",
                dependency_course_route_unit_ids=routes,
            ))
    for route, anchor in m.ROUTE_ANCHORS.items():
        relations.append(m.relation(
            f"relation:xref:{m.LOCAL_ROOT}:{route.lower()}", "xref", m.ROOT_UNIT, anchor,
            f"Route mapping for D60-LAB04: {route}.", laboratory_id=m.LAB_ID,
            course_route_unit_id=route, route_mapping_role="primary" if route == "D60-R04" else "secondary",
            route_source_anchor_id=anchor,
        ))
    additions = {name: [] for name in m.FILES}
    additions.update({
        "units.jsonl": units, "segments.jsonl": segments,
        "concepts.jsonl": concepts, "terms.jsonl": terms,
        "rights.jsonl": rights, "artifacts.jsonl": artifacts,
        "qa.jsonl": qa_events, "relations.jsonl": relations,
    })
    for name in m.FILES:
        additions[name] = sorted(additions[name], key=lambda record: record["id"])
    return additions


def validate_semantics(prefix_records: list[dict[str, Any]], additions: dict[str, list[dict[str, Any]]], data: dict[str, Any], parsed: dict[str, Any]) -> dict[str, Any]:
    added = [record for name in m.FILES for record in additions[name]]
    records = prefix_records + added
    by_id = {record["id"]: record for record in records}
    require(len(by_id) == len(records), "global ID collision")
    generic = m.load_generic()
    try:
        generic.validate_shapes(records)
        generic.validate_references(records, by_id)
        generic.validate_artifact_manifests(records, ROOT)
    except Exception as exc:
        raise SystemExit(f"Lab 4 backend candidate FAIL: merged validation failed: {exc}")
    required = {
        m.COURSE, m.PROGRAM, m.FOMBERG_EDITION, m.FOMBERG_RESOURCE,
        m.INTEGRATED_RIGHTS, "edition:roberts-at-2019-b947ad2",
        "resource:roberts-algebraic-topology-2019", *m.EXISTING_CONCEPTS,
        *m.ROUTE_ANCHORS.values(), *ANCHOR_ROUTES,
    }
    require(required <= by_id.keys(), f"required context absent: {sorted(required - by_id.keys())}")
    expected_counts = {
        "artifacts.jsonl": 10, "assets.jsonl": 0, "authority.jsonl": 0,
        "concepts.jsonl": 12, "corrections.jsonl": 0, "qa.jsonl": 7,
        "relations.jsonl": 61, "rights.jsonl": 1, "segments.jsonl": 25,
        "terms.jsonl": 12, "units.jsonl": 25,
    }
    actual_counts = {name: len(additions[name]) for name in m.FILES}
    require(actual_counts == expected_counts, f"suffix record census mismatch: {actual_counts}")
    units = additions["units.jsonl"]
    segments = additions["segments.jsonl"]
    require({record["source_local_id"] for record in units} == set(m.ID_KINDS), "unit stable-ID mapping mismatch")
    require({record["source_local_id"] for record in segments} == set(m.ID_KINDS), "segment stable-ID mapping mismatch")
    require(all(record.get("course_route_unit_ids") == list(m.ROUTES) for record in units + segments), "unit/segment five-route scope drift")
    segments_by_local = {record["source_local_id"]: record for record in segments}
    for unit in units:
        segment = segments_by_local[unit["source_local_id"]]
        require(segment["unit_id"] == unit["id"] and segment["target_locator"] == unit["target_locator"], f"unit/segment mismatch: {unit['id']}")
        start = unit["target_locator"]["line_start"]
        require(unit["source_local_id"].encode() in parsed["lines"][start - 1], f"target locator drift: {unit['id']}")
        require(unit["rights_component_id"] == segment["rights_component_id"] == m.LAB_RIGHTS, f"rights mismatch: {unit['id']}")
        require(unit["original_layer"] is True and unit["source_corpus_used"] is False, f"origin mismatch: {unit['id']}")
        require(unit["model_provenance"] == segment["model_provenance"] == m.MODEL, f"model provenance mismatch: {unit['id']}")
        require(all(concept in by_id and by_id[concept]["entity_type"] == "concept" for concept in unit["concept_ids"]), f"unresolved concept: {unit['id']}")
    rights = additions["rights.jsonl"][0]
    require(rights["license_expression"] == "CC-BY-SA-4.0" and set(rights["component_scope"]) == {unit["id"] for unit in units}, "rights scope mismatch")
    tasks = {f"unit:{m.LOCAL_ROOT}-task-{number:03d}" for number in range(1, 7)}
    hint_edges = [r for r in additions["relations.jsonl"] if r["relation_type"] == "hints"]
    solve_edges = [r for r in additions["relations.jsonl"] if r["relation_type"] == "solves"]
    require({r["to_id"] for r in hint_edges} == tasks and len(hint_edges) == 6, "hint closure mismatch")
    require({r["to_id"] for r in solve_edges} == tasks and len(solve_edges) == 6, "solution closure mismatch")
    route_edges = [r for r in additions["relations.jsonl"] if r["relation_type"] == "xref"]
    require({(r["course_route_unit_id"], r["to_id"]) for r in route_edges} == set(m.ROUTE_ANCHORS.items()), "five-route xref mismatch")
    dependencies = [r for r in additions["relations.jsonl"] if r["relation_type"] == "depends-on"]
    expected_dependencies = {(f"unit:{m.LOCAL_ROOT}-task-{n:03d}", a) for n, anchors in TASK_DEPENDENCIES.items() for a in anchors}
    require({(r["from_id"], r["to_id"]) for r in dependencies} == expected_dependencies, "dependency graph mismatch")
    require(all(r["dependency_course_route_unit_ids"] == list(ANCHOR_ROUTES[r["to_id"]]) for r in dependencies), "dependency route metadata mismatch")
    require({r["terminology_control_id"] for r in additions["terms.jsonl"]} == {f"O012-TERM-{n:04d}" for n, *_ in m.TERM_SPECS}, "term mapping mismatch")
    require(all(r["evidence_segment_id"] in by_id for r in additions["terms.jsonl"]), "term evidence segment missing")
    require(Counter(r["qa_type"] for r in additions["qa.jsonl"]) == Counter({"structure": 1, "execution": 1, "code": 1, "math": 1, "language": 1, "mastery": 1, "terminology": 1}), "QA census mismatch")
    for artifact in additions["artifacts.jsonl"]:
        expected = data["identities"][artifact["path"]]
        require((artifact["bytes"], artifact["sha256"]) == (expected[0], expected[2]), f"artifact identity mismatch: {artifact['path']}")
    joined = b"".join(m.suffixes(additions)[name] for name in m.FILES).lower()
    markers = (b"c:" + b"\\users\\", b"github_" + b"pat_", b"gh" + b"p_", b"access_" + b"token", b"authorization" + b": bearer")
    require(not any(marker in joined for marker in markers), "private marker in suffix")
    return {
        "added_records": len(added), "merged_records": len(records),
        "stable_ids": 25, "tasks": 6, "hints": 1, "complete_solutions": 1,
        "program_sources": 1, "test_suites": 1, "expected_outputs": 1,
        "new_concepts": 12, "new_terms": 12, "dependency_edges": len(dependencies),
        "dependency_scope": "five_assigned_routes_plus_explicit_R08_prerequisite",
        "route_edges": len(route_edges), "independent_reviews": 3,
        "schema_shapes": "PASS", "global_references": "PASS",
        "artifact_evidence": "PASS", "rights_and_provenance": "PASS",
        "append_only_candidate_ready": "PASS",
    }


m.verify_baseline_receipt = verify_baseline_receipt
m.verify_inputs = verify_inputs
m.concepts_for = concepts_for
m.unit_record = unit_record
m.build_additions = build_additions
m.validate_semantics = validate_semantics


def json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def identity_record(path: str, raw: bytes) -> dict[str, Any]:
    return {"path": path, "records": len(raw.splitlines()), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def candidate_receipt(prefix: dict[str, bytes], additions: dict[str, list[dict[str, Any]]], semantic: dict[str, Any]) -> tuple[dict[str, bytes], dict[str, Any]]:
    suffix = m.suffixes(additions)
    final = {name: prefix[name] + suffix[name] for name in m.FILES}
    for name in m.FILES:
        require(final[name].startswith(prefix[name]) and final[name][len(prefix[name]):] == suffix[name], f"candidate append identity mismatch: {name}")
    final_bundle = m.bundle(final)
    suffix_bundle = m.bundle(suffix)
    require(final_bundle == (semantic["merged_records"], sum(len(raw) for raw in final.values()), final_bundle[2]), "candidate record/byte census mismatch")
    records = m.parse_records(final)
    by_id = {record["id"]: record for record in records}
    require(len(by_id) == len(records), "candidate global ID collision")
    generic = m.load_generic()
    generic.validate_shapes(records)
    generic.validate_references(records, by_id)
    generic.validate_artifact_manifests(records, ROOT)
    files = []
    for name in m.FILES:
        files.append({
            **identity_record(f"backend/{name}", final[name]),
            "prefix_bytes": len(prefix[name]),
            "prefix_sha256": hashlib.sha256(prefix[name]).hexdigest(),
            "prefix_preserved": True,
            "records_added": len(additions[name]),
            "suffix_bytes": len(suffix[name]),
            "suffix_sha256": hashlib.sha256(suffix[name]).hexdigest(),
        })
    script_raw = Path(__file__).read_bytes()
    receipt = {
        "status": "PASS",
        "schema_version": "1.0",
        "receipt_kind": "isolated_backend_candidate",
        "laboratory_id": m.LAB_ID,
        "edition_unit_id": m.EDITION_UNIT_ID,
        "course_route_unit_ids": list(m.ROUTES),
        "not_promoted_to_live_backend": True,
        "immutable_prefix": {"records": m.PREFIX_TOTAL[0], "bytes": m.PREFIX_TOTAL[1], "bundle_sha256": m.PREFIX_TOTAL[2], "preserved_exactly": True},
        "delta": {"records": suffix_bundle[0], "bytes": suffix_bundle[1], "bundle_sha256": suffix_bundle[2], "records_by_file": {name: len(additions[name]) for name in m.FILES}, "bytes_by_file": {name: len(suffix[name]) for name in m.FILES}},
        "candidate": {"records": final_bundle[0], "bytes": final_bundle[1], "bundle_sha256": final_bundle[2]},
        "files": files,
        "semantic_checks": semantic,
        "producer": {"path": "scripts/extend-backend-computation-lab-004.py", "bytes": len(script_raw), "lf_lines": script_raw.count(b"\n"), "sha256": hashlib.sha256(script_raw).hexdigest()},
        "baseline_receipt": {"path": m.BASELINE_RECEIPT_PATH, "bytes": m.BASELINE_RECEIPT_IDENTITY[0], "lf_lines": m.BASELINE_RECEIPT_IDENTITY[1], "sha256": m.BASELINE_RECEIPT_IDENTITY[2]},
    }
    return final, receipt


def write_run(run_dir: Path, final: dict[str, bytes], plan: dict[str, Any], receipt: dict[str, Any]) -> dict[str, tuple[int, int, str]]:
    require(not run_dir.exists(), f"candidate run path already exists: {run_dir.name}")
    backend_dir = run_dir / "backend"
    backend_dir.mkdir(parents=True)
    for name in m.FILES:
        (backend_dir / name).write_bytes(final[name])
    (run_dir / "PLAN.json").write_bytes(json_bytes(plan))
    (run_dir / "RUN_RECEIPT.json").write_bytes(json_bytes(receipt))
    inventory: dict[str, tuple[int, int, str]] = {}
    for relative in [*(f"backend/{name}" for name in m.FILES), "PLAN.json", "RUN_RECEIPT.json"]:
        raw = (run_dir / relative).read_bytes()
        inventory[relative] = m.identity(raw)
    return inventory


def main() -> int:
    require(len(sys.argv) == 3 and sys.argv[1] == "--candidate-root", "usage: extend-backend-computation-lab-004.py --candidate-root qa/computation-lab-004/NAME")
    allowed = (ROOT / "qa/computation-lab-004").resolve()
    supplied = Path(sys.argv[2])
    candidate_root = (supplied if supplied.is_absolute() else ROOT / supplied).resolve()
    require(candidate_root.is_relative_to(allowed) and candidate_root != allowed, "candidate root must be a new child of qa/computation-lab-004")
    require(not candidate_root.exists(), "candidate root already exists; refusing overwrite")

    verify_baseline_receipt()
    m.validate_terminology_csv()
    data_a = verify_inputs()
    parsed_a = m.parse_reader(data_a["raw"][m.SOURCE_PATH])
    prefix_a, prefix_records_a = m.verify_prefix()
    additions_a = build_additions(data_a, parsed_a)
    semantic_a = validate_semantics(prefix_records_a, additions_a, data_a, parsed_a)
    plan_a = m.record_plan(additions_a, data_a, semantic_a)
    final_a, receipt_a = candidate_receipt(prefix_a, additions_a, semantic_a)

    verify_baseline_receipt()
    data_b = verify_inputs(data_a["identities"])
    parsed_b = m.parse_reader(data_b["raw"][m.SOURCE_PATH])
    prefix_b, prefix_records_b = m.verify_prefix()
    additions_b = build_additions(data_b, parsed_b)
    semantic_b = validate_semantics(prefix_records_b, additions_b, data_b, parsed_b)
    plan_b = m.record_plan(additions_b, data_b, semantic_b)
    final_b, receipt_b = candidate_receipt(prefix_b, additions_b, semantic_b)
    require(prefix_a == prefix_b and m.suffixes(additions_a) == m.suffixes(additions_b), "two-run prefix or suffix drift")
    require(plan_a == plan_b and receipt_a == receipt_b and final_a == final_b, "two-run candidate metadata drift")

    candidate_root.mkdir(parents=True)
    inventory_a = write_run(candidate_root / "run-a", final_a, plan_a, receipt_a)
    inventory_b = write_run(candidate_root / "run-b", final_b, plan_b, receipt_b)
    require(inventory_a == inventory_b, "two-run written inventory drift")
    replay = {
        "status": "PASS",
        "schema_version": "1.0",
        "receipt_kind": "isolated_exact_backend_candidate_replay",
        "laboratory_id": m.LAB_ID,
        "edition_unit_id": m.EDITION_UNIT_ID,
        "course_route_unit_ids": list(m.ROUTES),
        "not_promoted_to_live_backend": True,
        "runs": 2,
        "exact_file_matches": len(inventory_a),
        "candidate": receipt_a["candidate"],
        "delta": receipt_a["delta"],
        "inventory": [
            {"path": path, "bytes": identity[0], "lf_lines": identity[1], "sha256": identity[2]}
            for path, identity in sorted(inventory_a.items())
        ],
    }
    replay_raw = json_bytes(replay)
    replay_path = candidate_root / "REPLAY_RECEIPT.json"
    replay_path.write_bytes(replay_raw)
    require(replay_path.read_bytes() == replay_raw, "replay receipt write/read mismatch")

    print("Lab 4 isolated append-only backend candidate: PASS")
    print(f"candidate_root={candidate_root.relative_to(ROOT).as_posix()}")
    print(f"prefix_records={m.PREFIX_TOTAL[0]}")
    print(f"prefix_bytes={m.PREFIX_TOTAL[1]}")
    print(f"prefix_bundle_sha256={m.PREFIX_TOTAL[2]}")
    print(f"records_added={semantic_a['added_records']}")
    print(f"suffix_bytes={receipt_a['delta']['bytes']}")
    print(f"suffix_bundle_sha256={receipt_a['delta']['bundle_sha256']}")
    print(f"candidate_records={receipt_a['candidate']['records']}")
    print(f"candidate_bytes={receipt_a['candidate']['bytes']}")
    print(f"candidate_bundle_sha256={receipt_a['candidate']['bundle_sha256']}")
    print(f"replay_exact_file_matches={len(inventory_a)}")
    print(f"replay_receipt_sha256={hashlib.sha256(replay_raw).hexdigest()}")
    print("live_backend_modified=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
