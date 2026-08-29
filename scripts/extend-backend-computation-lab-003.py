#!/usr/bin/env python3
"""Fail-closed append-only backend admission for O012/D60 Lab 3."""
from __future__ import annotations

import importlib.util
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "scripts/extend-backend-computation-lab-002.py"
BASE_RAW = BASE.read_bytes()
BASE_IDENTITY = (
    len(BASE_RAW),
    BASE_RAW.count(b"\n"),
    hashlib.sha256(BASE_RAW).hexdigest(),
)
if BASE_IDENTITY != (
    51_323,
    879,
    "10b6fc03ba5b5a72dc8bd53ebe96fc1229763c77ee31a39a0b12b67155b36200",
):
    raise RuntimeError("frozen Lab 2 backend producer identity drift")
SPEC = importlib.util.spec_from_file_location("o012_lab02_backend_base", BASE)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot load the frozen Lab 2 backend producer")
m = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = m
SPEC.loader.exec_module(m)

m.LAB_ID = "D60-LAB03"
m.EDITION_UNIT_ID = "O012-ORIG-LAB03"
m.LOCAL_ROOT = "o012-d60-lab03"
m.ROOT_UNIT = "unit:o012-d60-lab03"
m.LAB_RIGHTS = "rights:o012-d60-lab03-original-cc-by-sa-4.0"
m.ROUTES = ("D60-R12", "D60-R14")
m.SOURCE_PATH = "source/id-ID/labs/computation-lab-003-cellular-boundaries-degree.md"
m.PROGRAM_PATH = "source/id-ID/labs/o012_d60_lab03_cellular_degree.py"
m.TEST_PATH = "source/id-ID/labs/test_o012_d60_lab03_cellular_degree.py"
m.EXPECTED_PATH = "source/id-ID/labs/expected-output-lab03.txt"
m.STATIC_PATH = "qa/computation-lab-003/STATIC_QA.json"
m.CODE_PATH = "qa/computation-lab-003/INDEPENDENT_CODE_REVIEW.json"
m.MATH_PATH = "qa/computation-lab-003/INDEPENDENT_MATH_REVIEW.json"
m.LANGUAGE_PATH = "qa/computation-lab-003/INDEPENDENT_SOURCE_LANGUAGE_REVIEW.json"
m.EXECUTION_PATH = "qa/computation-lab-003/EXECUTION_RECEIPT.json"
m.COMBINED_PATH = "qa/COMPUTATION_LAB_003_QA.json"
m.BASELINE_RECEIPT_PATH = "qa/BACKEND_APPEND_ONLY_COMPUTATION_LAB_002_CUMULATIVE_RECEIPT.json"
m.BASELINE_RECEIPT_IDENTITY = (
    10_039,
    280,
    "8c37c03b59ba638bb7c9533f4078cd75b5500bfaa408e8b816a5bef1b5bc522b",
)
m.PREFIX = {
    "artifacts.jsonl": (224, 185_068, "e28ed6e26a8f9812db1e54da035dc58675cd39303138fd85b6e00e9cffb06c94"),
    "assets.jsonl": (87, 64_692, "1df40f8f6ca4f2fbfbe8a7b924a68a153713a20a4eebe1d014d8fb04669945f7"),
    "authority.jsonl": (6, 4_374, "84c622f56dbbd5ba379361245ecfe07bc79c9f4fd6b18ba21b82b5f545211869"),
    "concepts.jsonl": (501, 158_569, "20a163b753cc00f018d9a8cd8f71c6467c7dab607a3b13e8eb5532d6b04ab44c"),
    "corrections.jsonl": (564, 594_720, "bd961fad5d83e96fec6ef83caa8447e2e5f282c603fd4983d79b5b4b54049fbb"),
    "qa.jsonl": (191, 105_671, "54372bca72f81e8dab6580af8db7ab350ff6dc2717fc067f87a6a0e00200a6da"),
    "relations.jsonl": (1_160, 526_730, "96d4d3cec3e42f87e21a5b245cd92f851d9122e4de02865166ed4a9e9c53c04a"),
    "rights.jsonl": (109, 103_393, "ebfcb9d92d9c1a097df404bc16b0abfe2e1c2a02ed5a359e0f615508025f22df"),
    "segments.jsonl": (2_090, 3_432_502, "c8ee822c289168ef7895788151a0f173365ea2a3caf606e3160d8407d18bd204"),
    "terms.jsonl": (494, 329_042, "e1b94dff63d858610b1ddc48cb248b0ca99f05303964c00163718bab12ba870a"),
    "units.jsonl": (2_120, 3_617_994, "fa1b11fb7231fcb5e765126dbbdba70365b63df544b0b65dcdd60d2c6ef21a7f"),
}
m.PREFIX_TOTAL = (
    7_546,
    9_122_755,
    "ac3a0377861ed2b728f9c7473579fdd4febe43e454a92f3ea06451e13d46c8f8",
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
    f"{m.LOCAL_ROOT}-cellular-boundaries": ("section", "derivation"),
    **{f"{m.LOCAL_ROOT}-task-{number:03d}": ("exercise", "exercise") for number in range(1, 7)},
    f"{m.LOCAL_ROOT}-hint": ("hint", "hint"),
    f"{m.LOCAL_ROOT}-program": ("source_code", "source_code"),
    f"{m.LOCAL_ROOT}-tests": ("test_suite", "test_suite"),
    f"{m.LOCAL_ROOT}-expected-output": ("expected_output", "expected_output"),
    f"{m.LOCAL_ROOT}-interpretation": ("interpretation", "interpretation"),
    f"{m.LOCAL_ROOT}-solution": ("solution", "solution"),
    f"{m.LOCAL_ROOT}-sol-execution": ("section", "solution_section"),
    f"{m.LOCAL_ROOT}-sol-x3": ("section", "solution_section"),
    f"{m.LOCAL_ROOT}-sol-torus": ("section", "solution_section"),
    f"{m.LOCAL_ROOT}-sol-degree": ("section", "solution_section"),
    f"{m.LOCAL_ROOT}-sol-negative": ("section", "solution_section"),
    f"{m.LOCAL_ROOT}-reproducibility": ("verification", "verification"),
    f"{m.LOCAL_ROOT}-rights": ("rights_notice", "rights_notice"),
}

m.TERM_SPECS = (
    (503, "one-column cellular boundary", "batas seluler satu kolom", "homological_algebra", f"{m.LOCAL_ROOT}-sol-x3", "boundary homomorphism from one top-dimensional cellular generator after oriented bases are fixed"),
    (504, "signed incidence vector", "vektor insidensi bertanda", "algebraic_topology", f"{m.LOCAL_ROOT}-cellular-boundaries", "ordered cellular-boundary coefficients computed with orientation signs; columns index top cells and rows index codimension-one cells"),
    (505, "unsigned-occurrence trap", "jebakan hitung tak bertanda", "computational_topology", f"{m.LOCAL_ROOT}-sol-torus", "diagnostic contrast showing that counting letters without inverse signs does not compute a cellular incidence degree"),
    (506, "integer torus endomorphism", "endomorfisme torus integral", "algebraic_topology", f"{m.LOCAL_ROOT}-data", "map on R^2/Z^2 induced by an integer 2-by-2 matrix; nonintegral columns do not descend to the quotient"),
    (507, "exact torus preimage", "prabayangan torus eksak", "computational_topology", f"{m.LOCAL_ROOT}-sol-degree", "canonical representative in [0,1)^2 obtained with exact rational arithmetic from Ax=y+k"),
    (508, "determinant degree formula", "rumus derajat-determinan", "algebraic_topology", f"{m.LOCAL_ROOT}-cellular-boundaries", "for an integer linear torus map the action on the oriented fundamental class and hence the degree is det(A)"),
    (509, "local-degree census", "sensus derajat lokal", "algebraic_topology", f"{m.LOCAL_ROOT}-sol-degree", "complete ordered list of regular preimages with orientation signs whose signed sum equals the global degree"),
    (510, "composition-order witness", "saksi urutan komposisi", "computational_topology", f"{m.LOCAL_ROOT}-sol-degree", "explicit matrices and fibers distinguishing f_N after f_M, represented by NM, from the reversed composition MN"),
    (511, "left-null obstruction", "obstruksi vektor null kiri", "integer_linear_algebra", f"{m.LOCAL_ROOT}-sol-negative", "integer row vector annihilating a singular matrix while pairing nonintegrally with a target, certifying that target is outside the torus-map image"),
    (512, "orientation-reversal control", "kontrol pembalikan orientasi", "homological_algebra", f"{m.LOCAL_ROOT}-sol-x3", "signed basis change that reverses a cellular-boundary column without changing the isomorphism class of homology"),
    (513, "cup product", "produk cup", "algebraic_topology", f"{m.LOCAL_ROOT}-cellular-boundaries", "graded cohomology product; retain cup in English rather than translating it as an ordinary vessel"),
    (514, "degree on oriented surfaces", "derajat pada permukaan berorientasi", "algebraic_topology", f"{m.LOCAL_ROOT}-cellular-boundaries", "integer defined by the action on the oriented top-dimensional fundamental class; the torus determinant formula is a specialization"),
)
m.EXISTING_CONCEPTS = {
    "concept:attaching-map", "concept:covering-map", "concept:degree-of-a-map",
    "concept:fundamental-class", "concept:homology", "concept:local-degree",
    "concept:local-to-global-degree-formula", "concept:orientation",
    "concept:o012-fom-u007-term-0474", "concept:o012-fom-u007-term-0475",
    "concept:o012-fom-u007-term-0476", "concept:o012-fom-u007-term-0481",
    "concept:o012-fom-u007-term-0482",
}
m.NEW_CONCEPTS = {
    number: f"concept:{m.LOCAL_ROOT}-term-{number:04d}" for number, *_ in m.TERM_SPECS
}
m.ALL_LAB_CONCEPTS = tuple(sorted(m.EXISTING_CONCEPTS | set(m.NEW_CONCEPTS.values())))
m.ROUTE_ANCHORS = {
    "D60-R12": "unit:o012-fom-u007",
    "D60-R14": "unit:o012-rbt-l30",
}
ANCHOR_ROUTES = {
    "unit:o012-fom-u007": "D60-R12",
    "unit:o012-fom-u007-def-cellular-boundary": "D60-R12",
    "unit:o012-fom-u007-thm-cellular-incidence": "D60-R12",
    "unit:o012-fom-u007-ex-torus-homology": "D60-R12",
    "unit:o012-fom-u005-ex-power-map": "D60-R12",
    "unit:o012-fom-u005-def-degree": "D60-R12",
    "unit:o012-fom-u005-def-local-degree": "D60-R12",
    "unit:o012-fom-u005-prop-local-to-global": "D60-R12",
    "unit:o012-rbt-l30": "D60-R14",
    "unit:o012-rbt-l30-s04": "D60-R14",
    "unit:o012-rbt-l30-def-002": "D60-R14",
    "unit:o012-rbt-l30-prop-001": "D60-R14",
}
TASK_DEPENDENCIES = {
    1: ("unit:o012-fom-u007", "unit:o012-rbt-l30-s04"),
    2: ("unit:o012-fom-u007-def-cellular-boundary", "unit:o012-fom-u007-thm-cellular-incidence", "unit:o012-fom-u005-ex-power-map"),
    3: ("unit:o012-fom-u007-thm-cellular-incidence", "unit:o012-fom-u007-ex-torus-homology"),
    4: ("unit:o012-fom-u007", "unit:o012-rbt-l30-def-002", "unit:o012-rbt-l30-prop-001"),
    5: ("unit:o012-fom-u005-prop-local-to-global", "unit:o012-rbt-l30-prop-001"),
    6: ("unit:o012-fom-u005-def-degree", "unit:o012-fom-u005-def-local-degree", "unit:o012-fom-u005-prop-local-to-global"),
}


def verify_baseline_receipt() -> dict[str, Any]:
    raw = m.disciplined(m.BASELINE_RECEIPT_PATH)
    m.require(m.identity(raw) == m.BASELINE_RECEIPT_IDENTITY, "baseline cumulative receipt identity drift")
    baseline = json.loads(raw)
    cumulative = baseline.get("cumulative", {})
    replay = baseline.get("replay", {})
    m.require(
        baseline.get("status") == "PASS"
        and baseline.get("receipt_kind") == "cumulative_backend_boundary"
        and baseline.get("laboratory_id") == "D60-LAB02"
        and (cumulative.get("records"), cumulative.get("bytes"), cumulative.get("bundle_sha256")) == m.PREFIX_TOTAL
        and replay.get("status") == "PASS"
        and replay.get("exact_file_matches") == len(m.FILES)
        and replay.get("temporary_replay_removed") is True,
        "baseline receipt does not prove the exact Lab 2 cumulative boundary",
    )
    return baseline


def verify_inputs(sealed: dict[str, tuple[int, int, str]] | None = None) -> dict[str, Any]:
    raw = {relative: m.disciplined(relative) for relative in m.INPUT_PATHS}
    identities = {relative: m.identity(value) for relative, value in raw.items()}
    if sealed is not None:
        m.require(identities == sealed, "sealed input identity drift")
    combined = json.loads(raw[m.COMBINED_PATH])
    m.require(
        combined.get("status") == "PASS"
        and combined.get("receipt_kind") == "computation_laboratory_source_execution_review_closure"
        and combined.get("laboratory_id") == m.LAB_ID
        and combined.get("edition_unit_id") == m.EDITION_UNIT_ID
        and combined.get("course_route_unit_ids") == list(m.ROUTES),
        "combined QA is not the final Lab 3 closure",
    )
    m.require(combined.get("severity_census") == {"P1": 0, "P2": 0, "P3": 0}, "combined QA findings remain")
    checks = combined.get("checks", {})
    m.require(checks.get("excluded_fomberg_problem_bank_used") is False, "excluded problem-bank use claimed")
    m.require(checks.get("route_scope_D60_R12_R14") == "PASS", "combined QA route scope incomplete")
    bound: dict[str, tuple[int, int, str]] = {}
    m.identity_index(combined, bound)
    for relative in (*m.LEARNER_PATHS, m.TERMINOLOGY_PATH, m.STATIC_PATH, *m.REVIEW_PATHS, m.EXECUTION_PATH):
        m.require(bound.get(relative) == identities[relative], f"combined QA does not bind current {relative}")
    static = json.loads(raw[m.STATIC_PATH])
    m.require(
        static.get("status") == "PASS"
        and static.get("laboratory_id") == m.LAB_ID
        and static.get("course_route_unit_ids") == list(m.ROUTES)
        and static.get("severity_counts") == {"P1": 0, "P2": 0, "P3": 0},
        "static QA mismatch",
    )
    review_contracts = {
        m.CODE_PATH: (
            "independent_code",
            {m.SOURCE_PATH, m.PROGRAM_PATH, m.TEST_PATH, m.EXPECTED_PATH, m.STATIC_PATH},
        ),
        m.MATH_PATH: (
            "independent_mathematics",
            {m.SOURCE_PATH, m.PROGRAM_PATH, m.TEST_PATH, m.EXPECTED_PATH, m.STATIC_PATH},
        ),
        m.LANGUAGE_PATH: (
            "independent_source_language",
            {m.SOURCE_PATH, m.PROGRAM_PATH, m.TEST_PATH, m.EXPECTED_PATH, m.TERMINOLOGY_PATH},
        ),
    }
    for relative, (kind, expected_paths) in review_contracts.items():
        receipt = json.loads(raw[relative])
        m.require(
            receipt.get("status") == "PASS"
            and receipt.get("review_kind") == kind
            and receipt.get("laboratory_id") == m.LAB_ID
            and receipt.get("edition_unit_id") == m.EDITION_UNIT_ID
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
            m.require(path in expected_paths and path not in review_bound, f"{kind} bound-artifact scope mismatch")
            review_bound[path] = (item.get("bytes"), item.get("lf_lines"), item.get("sha256"))
        m.require(review_bound == {path: identities[path] for path in expected_paths}, f"{kind} exact artifact binding mismatch")
    execution = json.loads(raw[m.EXECUTION_PATH])
    runtime = execution.get("runtime", {})
    m.require(
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
        f"{m.LOCAL_ROOT}-status": ("concept:homology", "concept:degree-of-a-map", n[504], n[509]),
        f"{m.LOCAL_ROOT}-prerequisites": ("concept:attaching-map", "concept:fundamental-class", "concept:local-degree", "concept:o012-fom-u007-term-0474"),
        f"{m.LOCAL_ROOT}-objectives": (n[503], n[506], n[508], n[509], n[510], n[511]),
        f"{m.LOCAL_ROOT}-data": ("concept:orientation", n[506], n[507]),
        f"{m.LOCAL_ROOT}-cellular-boundaries": ("concept:attaching-map", "concept:fundamental-class", "concept:o012-fom-u007-term-0474", "concept:o012-fom-u007-term-0475", "concept:o012-fom-u007-term-0481", n[504], n[508], n[513], n[514]),
        f"{m.LOCAL_ROOT}-task-001": (n[507], n[509]),
        f"{m.LOCAL_ROOT}-task-002": ("concept:degree-of-a-map", "concept:o012-fom-u007-term-0474", n[503], n[512]),
        f"{m.LOCAL_ROOT}-task-003": ("concept:o012-fom-u007-term-0475", "concept:o012-fom-u007-term-0482", n[504], n[505]),
        f"{m.LOCAL_ROOT}-task-004": ("concept:fundamental-class", "concept:o012-fom-u007-term-0481", n[506], n[508], n[513], n[514]),
        f"{m.LOCAL_ROOT}-task-005": ("concept:local-degree", "concept:local-to-global-degree-formula", n[507], n[509], n[510]),
        f"{m.LOCAL_ROOT}-task-006": (n[505], n[511]),
        f"{m.LOCAL_ROOT}-program": (n[503], n[506], n[507], n[509], n[511]),
        f"{m.LOCAL_ROOT}-tests": (n[505], n[509], n[510], n[511], n[512]),
        f"{m.LOCAL_ROOT}-expected-output": (n[503], n[507], n[509], n[510], n[511]),
        f"{m.LOCAL_ROOT}-interpretation": ("concept:homology", "concept:degree-of-a-map", n[508], n[509]),
        f"{m.LOCAL_ROOT}-sol-x3": ("concept:o012-fom-u007-term-0474", n[503], n[512]),
        f"{m.LOCAL_ROOT}-sol-torus": ("concept:o012-fom-u007-term-0475", "concept:o012-fom-u007-term-0482", n[504], n[505]),
        f"{m.LOCAL_ROOT}-sol-degree": ("concept:fundamental-class", "concept:local-degree", n[507], n[508], n[509], n[510], n[513], n[514]),
        f"{m.LOCAL_ROOT}-sol-negative": (n[506], n[511]),
        f"{m.LOCAL_ROOT}-reproducibility": tuple(n.values()),
        f"{m.LOCAL_ROOT}-rights": ("concept:degree-of-a-map", "concept:o012-fom-u007-term-0474"),
    }
    if local_id in (m.LOCAL_ROOT, f"{m.LOCAL_ROOT}-hint", f"{m.LOCAL_ROOT}-solution", f"{m.LOCAL_ROOT}-sol-execution"):
        return list(m.ALL_LAB_CONCEPTS)
    return list(exact.get(local_id, ("concept:degree-of-a-map",)))


original_unit_record = m.unit_record


def unit_record(local_id: str, order: int, parsed: dict[str, Any]) -> dict[str, Any]:
    record = original_unit_record(local_id, order, parsed)
    record["course_route_unit_ids"] = list(m.ROUTES)
    record["authority_context_ids"] = [
        m.COURSE, m.PROGRAM, m.FOMBERG_EDITION, m.FOMBERG_RESOURCE,
        "edition:roberts-at-2019-b947ad2", "resource:roberts-algebraic-topology-2019",
    ]
    if local_id == m.LOCAL_ROOT:
        record["order"] = 44
        record["primary_course_route_unit_id"] = "D60-R12"
        record["secondary_course_route_unit_ids"] = ["D60-R14"]
    if re.fullmatch(re.escape(m.LOCAL_ROOT) + r"-task-\d{3}", local_id):
        record["primary_course_route_unit_id"] = "D60-R12"
        record["secondary_course_route_unit_ids"] = ["D60-R14"]
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
            "concept_id": m.NEW_CONCEPTS[number],
            "evidence_segment_id": f"segment:{evidence}",
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
        "attribution": "Original D60-LAB03 computation laboratory prepared for the independent Indonesian O012/D60 edition.",
        "change_notice": "Edition-original laboratory layer; Roberts and Fomberg source components are neither copied nor relicensed.",
        "component_scope": [unit["id"] for unit in units],
        "license_expression": "CC-BY-SA-4.0",
        "license_url": "https://creativecommons.org/licenses/by-sa/4.0/",
        "non_endorsement": "Independent Indonesian edition; no source-author or institutional endorsement.",
        "third_party_status": "No excluded problem-bank expression is used; admitted R12/R14 authority IDs are mathematical context only.",
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
        {**m.common("qa_event", qa_ids["structure"]), "laboratory_id": m.LAB_ID, "note": "Twenty-five stable IDs, six tasks, one hint, a full solution, exact R12/R14 routing, rights, provenance, and privacy checks passed.", "qa_type": "structure", "result": "passed", "unit_id": m.ROOT_UNIT, "witness_artifact_ids": [f"artifact:{m.LOCAL_ROOT}-reader-source", f"artifact:{m.LOCAL_ROOT}-static-qa", f"artifact:{m.LOCAL_ROOT}-qa-receipt"]},
        {**m.common("qa_event", qa_ids["execution"]), "laboratory_id": m.LAB_ID, "note": "The standard-library program and six-test suite each ran twice; stdout was deterministic and exact against frozen output.", "qa_type": "execution", "result": "passed", "unit_id": m.ROOT_UNIT, "witness_artifact_ids": [f"artifact:{m.LOCAL_ROOT}-python-source", f"artifact:{m.LOCAL_ROOT}-tests", f"artifact:{m.LOCAL_ROOT}-expected-output", f"artifact:{m.LOCAL_ROOT}-execution-receipt"]},
        {**m.common("qa_event", qa_ids["code"]), "laboratory_id": m.LAB_ID, "note": "Independent code review checked exact rational fibers, validation, composition order, singular controls, deterministic output, and offline execution with P1=P2=P3=0.", "qa_type": "code", "result": "passed", "unit_id": m.ROOT_UNIT, "witness_artifact_ids": [f"artifact:{m.LOCAL_ROOT}-code-review", f"artifact:{m.LOCAL_ROOT}-qa-receipt"]},
        {**m.common("qa_event", qa_ids["math"]), "laboratory_id": m.LAB_ID, "note": "Independent mathematics review recomputed cellular boundaries, homology, determinants, exact fibers, local signs, surface degree, and singular obstruction with P1=P2=P3=0.", "qa_type": "math", "result": "passed", "unit_id": m.ROOT_UNIT, "witness_artifact_ids": [f"artifact:{m.LOCAL_ROOT}-math-review", f"artifact:{m.LOCAL_ROOT}-qa-receipt"]},
        {**m.common("qa_event", qa_ids["language"]), "laboratory_id": m.LAB_ID, "note": "Independent final id-ID review passed exact R12/R14 scope, links, terminology, executable claims, rights, and provenance.", "qa_type": "language", "result": "passed", "unit_id": m.ROOT_UNIT, "witness_artifact_ids": [f"artifact:{m.LOCAL_ROOT}-language-review", f"artifact:{m.LOCAL_ROOT}-qa-receipt"]},
        {**m.common("qa_event", qa_ids["mastery"]), "laboratory_id": m.LAB_ID, "note": "Six tasks share one stable hint and complete checked solution covering cellular incidence, homology, degree, exact fibers, composition, and negative controls.", "qa_type": "mastery", "result": "passed", "unit_id": m.ROOT_UNIT, "witness_artifact_ids": [f"artifact:{m.LOCAL_ROOT}-reader-source", f"artifact:{m.LOCAL_ROOT}-python-source", f"artifact:{m.LOCAL_ROOT}-static-qa"]},
        {**m.common("qa_event", qa_ids["terminology"]), "laboratory_id": m.LAB_ID, "note": "O012-TERM-0503 through O012-TERM-0514 map twelve controlled id-ID terms to locale-neutral concepts and exact evidence segments.", "qa_type": "terminology", "result": "passed", "unit_id": m.ROOT_UNIT, "witness_artifact_ids": [f"artifact:{m.LOCAL_ROOT}-language-review", f"artifact:{m.LOCAL_ROOT}-static-qa"]},
    ]
    relations = [
        m.relation("relation:contains:o012-d60:lab03", "contains", m.COURSE, m.ROOT_UNIT, "The O012/D60 course contains D60-LAB03 as an original computation laboratory.", laboratory_id=m.LAB_ID, course_route_unit_ids=list(m.ROUTES)),
        m.relation(f"relation:contains:{m.LOCAL_ROOT}-rights:root", "contains", m.LAB_RIGHTS, m.ROOT_UNIT, "The original CC BY-SA 4.0 component rights bind the complete D60-LAB03 graph.", laboratory_id=m.LAB_ID, rights_mapping_role="direct_component_binding"),
        m.relation("relation:contains:o012-d60-integrated-rights:lab03-original", "contains", m.INTEGRATED_RIGHTS, m.LAB_RIGHTS, "The integrated route contains the independently licensed D60-LAB03 component without altering source licenses.", laboratory_id=m.LAB_ID, rights_mapping_role="integrated_route_component"),
    ]
    for local_id in m.ID_KINDS:
        if local_id != m.LOCAL_ROOT:
            relations.append(m.relation(f"relation:contains:{m.LOCAL_ROOT}:{local_id.removeprefix(m.LOCAL_ROOT + '-')}", "contains", m.ROOT_UNIT, f"unit:{local_id}", f"D60-LAB03 contains learner surface {local_id}.", laboratory_id=m.LAB_ID))
    hint = f"unit:{m.LOCAL_ROOT}-hint"
    solution = f"unit:{m.LOCAL_ROOT}-solution"
    for number in range(1, 7):
        exercise = f"unit:{m.LOCAL_ROOT}-task-{number:03d}"
        relations.append(m.relation(f"relation:hints:{m.LOCAL_ROOT}-hint:task-{number:03d}", "hints", hint, exercise, f"Shared stable hint for D60-LAB03 task {number}.", laboratory_id=m.LAB_ID, laboratory_task_number=number))
        relations.append(m.relation(f"relation:solves:{m.LOCAL_ROOT}-solution:task-{number:03d}", "solves", solution, exercise, f"Complete checked solution for D60-LAB03 task {number}.", laboratory_id=m.LAB_ID, laboratory_task_number=number, solution_status="complete_checked_solution"))
        for dep_order, anchor in enumerate(TASK_DEPENDENCIES[number], 1):
            route = ANCHOR_ROUTES[anchor]
            slug = re.sub(r"[^a-z0-9]+", "-", anchor.lower()).strip("-")
            relations.append(m.relation(f"relation:depends-on:{m.LOCAL_ROOT}-task-{number:03d}:{dep_order:02d}:{slug}", "depends-on", exercise, anchor, f"D60-LAB03 task {number} requires the admitted {route} result {anchor}.", laboratory_id=m.LAB_ID, laboratory_task_number=number, dependency_order=dep_order, dependency_role="laboratory_prerequisite", course_route_unit_id=route))
    for route, anchor in m.ROUTE_ANCHORS.items():
        relations.append(m.relation(f"relation:xref:{m.LOCAL_ROOT}:{route.lower()}", "xref", m.ROOT_UNIT, anchor, f"Route mapping for D60-LAB03: {route}.", laboratory_id=m.LAB_ID, course_route_unit_id=route, route_mapping_role="primary" if route == "D60-R12" else "secondary", route_source_anchor_id=anchor))
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
    m.require(len(by_id) == len(records), "global ID collision")
    generic = m.load_generic()
    try:
        generic.validate_shapes(records)
        generic.validate_references(records, by_id)
        generic.validate_artifact_manifests(records, ROOT)
    except Exception as exc:
        raise SystemExit(f"Lab 3 backend producer FAIL: merged validation failed: {exc}")
    required = {
        m.COURSE, m.PROGRAM, m.FOMBERG_EDITION, m.FOMBERG_RESOURCE,
        m.INTEGRATED_RIGHTS, "edition:roberts-at-2019-b947ad2",
        "resource:roberts-algebraic-topology-2019", *m.EXISTING_CONCEPTS,
        *m.ROUTE_ANCHORS.values(), *ANCHOR_ROUTES,
    }
    m.require(required <= by_id.keys(), f"required context absent: {sorted(required - by_id.keys())}")
    expected_counts = {
        "artifacts.jsonl": 10, "assets.jsonl": 0, "authority.jsonl": 0,
        "concepts.jsonl": 12, "corrections.jsonl": 0, "qa.jsonl": 7,
        "relations.jsonl": 56, "rights.jsonl": 1, "segments.jsonl": 25,
        "terms.jsonl": 12, "units.jsonl": 25,
    }
    actual_counts = {name: len(additions[name]) for name in m.FILES}
    m.require(actual_counts == expected_counts, f"suffix record census mismatch: {actual_counts}")
    units = additions["units.jsonl"]
    segments = additions["segments.jsonl"]
    m.require({record["source_local_id"] for record in units} == set(m.ID_KINDS), "unit stable-ID mapping mismatch")
    m.require({record["source_local_id"] for record in segments} == set(m.ID_KINDS), "segment stable-ID mapping mismatch")
    m.require(all(record.get("course_route_unit_ids") == list(m.ROUTES) for record in units + segments), "unit/segment route scope drift")
    segments_by_local = {record["source_local_id"]: record for record in segments}
    for unit in units:
        segment = segments_by_local[unit["source_local_id"]]
        m.require(segment["unit_id"] == unit["id"] and segment["target_locator"] == unit["target_locator"], f"unit/segment mismatch: {unit['id']}")
        start = unit["target_locator"]["line_start"]
        m.require(unit["source_local_id"].encode() in parsed["lines"][start - 1], f"target locator drift: {unit['id']}")
        m.require(unit["rights_component_id"] == segment["rights_component_id"] == m.LAB_RIGHTS, f"rights mismatch: {unit['id']}")
        m.require(unit["original_layer"] is True and unit["source_corpus_used"] is False, f"origin mismatch: {unit['id']}")
        m.require(all(concept in by_id and by_id[concept]["entity_type"] == "concept" for concept in unit["concept_ids"]), f"unresolved concept: {unit['id']}")
    rights = additions["rights.jsonl"][0]
    m.require(rights["license_expression"] == "CC-BY-SA-4.0" and set(rights["component_scope"]) == {unit["id"] for unit in units}, "rights scope mismatch")
    tasks = {f"unit:{m.LOCAL_ROOT}-task-{number:03d}" for number in range(1, 7)}
    hint_edges = [r for r in additions["relations.jsonl"] if r["relation_type"] == "hints"]
    solve_edges = [r for r in additions["relations.jsonl"] if r["relation_type"] == "solves"]
    m.require({r["to_id"] for r in hint_edges} == tasks and len(hint_edges) == 6, "hint closure mismatch")
    m.require({r["to_id"] for r in solve_edges} == tasks and len(solve_edges) == 6, "solution closure mismatch")
    route_edges = [r for r in additions["relations.jsonl"] if r["relation_type"] == "xref"]
    m.require({(r["course_route_unit_id"], r["to_id"]) for r in route_edges} == set(m.ROUTE_ANCHORS.items()), "route xref mismatch")
    dependencies = [r for r in additions["relations.jsonl"] if r["relation_type"] == "depends-on"]
    expected_dependencies = {(f"unit:{m.LOCAL_ROOT}-task-{n:03d}", a) for n, anchors in TASK_DEPENDENCIES.items() for a in anchors}
    m.require({(r["from_id"], r["to_id"]) for r in dependencies} == expected_dependencies, "dependency graph mismatch")
    m.require(all(r["course_route_unit_id"] == ANCHOR_ROUTES[r["to_id"]] for r in dependencies), "dependency route mismatch")
    m.require({r["terminology_control_id"] for r in additions["terms.jsonl"]} == {f"O012-TERM-{n:04d}" for n, *_ in m.TERM_SPECS}, "term mapping mismatch")
    m.require(Counter(r["qa_type"] for r in additions["qa.jsonl"]) == Counter({"structure": 1, "execution": 1, "code": 1, "math": 1, "language": 1, "mastery": 1, "terminology": 1}), "QA census mismatch")
    for artifact in additions["artifacts.jsonl"]:
        expected = data["identities"][artifact["path"]]
        m.require((artifact["bytes"], artifact["sha256"]) == (expected[0], expected[2]), f"artifact identity mismatch: {artifact['path']}")
    joined = b"".join(m.suffixes(additions)[name] for name in m.FILES).lower()
    markers = (b"c:" + b"\\users\\", b"github_" + b"pat_", b"gh" + b"p_", b"access_" + b"token", b"authorization" + b": bearer")
    m.require(not any(marker in joined for marker in markers), "private marker in suffix")
    return {
        "added_records": len(added), "merged_records": len(records),
        "stable_ids": 25, "tasks": 6, "hints": 1, "complete_solutions": 1,
        "program_sources": 1, "test_suites": 1, "expected_outputs": 1,
        "new_concepts": 12, "new_terms": 12, "dependency_edges": len(dependencies),
        "dependency_scope": "D60-R12_and_D60-R14", "route_edges": len(route_edges),
        "independent_reviews": 3, "schema_shapes": "PASS", "global_references": "PASS",
        "artifact_evidence": "PASS", "rights_and_provenance": "PASS", "append_only_ready": "PASS",
    }


m.verify_baseline_receipt = verify_baseline_receipt
m.verify_inputs = verify_inputs
m.concepts_for = concepts_for
m.unit_record = unit_record
m.build_additions = build_additions
m.validate_semantics = validate_semantics


def main() -> int:
    m.require(sys.argv[1:] in ([], ["--plan"]), "accepted invocation is no arguments or --plan")
    verify_baseline_receipt()
    m.validate_terminology_csv()
    data = verify_inputs()
    parsed = m.parse_reader(data["raw"][m.SOURCE_PATH])
    prefix, prefix_records = m.verify_prefix()
    additions = build_additions(data, parsed)
    semantic = validate_semantics(prefix_records, additions, data, parsed)
    plan = m.record_plan(additions, data, semantic)
    if sys.argv[1:] == ["--plan"]:
        print(json.dumps(plan, ensure_ascii=False, sort_keys=True, indent=2))
        return 0
    verify_baseline_receipt()
    refreshed = verify_inputs(data["identities"])
    refreshed_parsed = m.parse_reader(refreshed["raw"][m.SOURCE_PATH])
    refreshed_additions = build_additions(refreshed, refreshed_parsed)
    refreshed_semantic = validate_semantics(prefix_records, refreshed_additions, refreshed, refreshed_parsed)
    m.require(m.record_plan(refreshed_additions, refreshed, refreshed_semantic) == plan, "sealed inputs changed deterministic plan")
    m.require(m.suffixes(refreshed_additions) == m.suffixes(additions), "sealed inputs changed suffix")
    raw_suffixes = m.append_suffix(prefix, additions)
    final_raw = {name: (m.BACKEND / name).read_bytes() for name in m.FILES}
    final = m.bundle(final_raw)
    m.require(final[0] == m.PREFIX_TOTAL[0] + semantic["added_records"], "cumulative record count mismatch")
    print("Lab 3 append-only semantic backend extension: PASS")
    print(f"prefix_records={m.PREFIX_TOTAL[0]}")
    print(f"prefix_bytes={m.PREFIX_TOTAL[1]}")
    print(f"prefix_bundle_sha256={m.PREFIX_TOTAL[2]}")
    print(f"records_added={semantic['added_records']}")
    print(f"suffix_bytes={sum(len(raw_suffixes[name]) for name in m.FILES)}")
    print(f"cumulative_records={final[0]}")
    print(f"cumulative_bytes={final[1]}")
    print(f"backend_bundle_sha256={final[2]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
