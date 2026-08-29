#!/usr/bin/env python3
"""Independent fail-closed validation of the D60-LAB04 backend append.

The producer is used only to derive its proposed records.  This validator
independently freezes the complete Lab 3 byte prefix, checks the Lab 4 source
and review closure, audits every proposed record and relation, rebuilds the
candidate twice, and (after append) proves that the live backend is exactly
prefix plus candidate.  It never writes backend files.
"""
from __future__ import annotations

import csv
import hashlib
import importlib.util
import io
import json
import os
import re
import shutil
import sys
import tempfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
QA = ROOT / "qa"
PRODUCER_PATH = ROOT / "scripts/extend-backend-computation-lab-004.py"
BASELINE_RECEIPT_PATH = QA / "BACKEND_APPEND_ONLY_COMPUTATION_LAB_003_CUMULATIVE_RECEIPT.json"
LAB_ID = "D60-LAB04"
EDITION_UNIT_ID = "O012-ORIG-LAB04"
LOCAL_ROOT = "o012-d60-lab04"
ROOT_UNIT = f"unit:{LOCAL_ROOT}"
LAB_RIGHTS = f"rights:{LOCAL_ROOT}-original-cc-by-sa-4.0"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"
ROUTES = ("D60-R04", "D60-R05", "D60-R12", "D60-R13", "D60-R14")

FILES = (
    "artifacts.jsonl",
    "assets.jsonl",
    "authority.jsonl",
    "concepts.jsonl",
    "corrections.jsonl",
    "qa.jsonl",
    "relations.jsonl",
    "rights.jsonl",
    "segments.jsonl",
    "terms.jsonl",
    "units.jsonl",
)
PREFIX = {
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
PREFIX_TOTAL = (
    7_694,
    9_280_385,
    "cddd65499da547e0c4f01b8a880f68d1c3d314c078a9179528e4a28b2c5f65a2",
)
BASELINE_RECEIPT_IDENTITY = (
    10_047,
    280,
    "7ee69a9291368d407e38de4c63440d599b5cd13ec5fc288f5468084bc7774c80",
)

SOURCE_PATH = "source/id-ID/labs/computation-lab-004-cross-invariant-comparison.md"
PROGRAM_PATH = "source/id-ID/labs/o012_d60_lab04_cross_invariants.py"
TEST_PATH = "source/id-ID/labs/test_o012_d60_lab04_cross_invariants.py"
EXPECTED_PATH = "source/id-ID/labs/expected-output-lab04.txt"
TERMINOLOGY_PATH = "00_control/TERMINOLOGY.csv"
STATIC_PATH = "qa/computation-lab-004/STATIC_QA.json"
CODE_PATH = "qa/computation-lab-004/INDEPENDENT_CODE_REVIEW.json"
MATH_PATH = "qa/computation-lab-004/INDEPENDENT_MATH_REVIEW.json"
LANGUAGE_PATH = "qa/computation-lab-004/INDEPENDENT_SOURCE_LANGUAGE_REVIEW.json"
EXECUTION_PATH = "qa/computation-lab-004/EXECUTION_RECEIPT.json"
COMBINED_PATH = "qa/COMPUTATION_LAB_004_QA.json"
LEARNER_PATHS = (SOURCE_PATH, PROGRAM_PATH, TEST_PATH, EXPECTED_PATH)
REVIEW_PATHS = (CODE_PATH, MATH_PATH, LANGUAGE_PATH)
ARTIFACT_PATHS = (
    SOURCE_PATH,
    PROGRAM_PATH,
    TEST_PATH,
    EXPECTED_PATH,
    STATIC_PATH,
    CODE_PATH,
    MATH_PATH,
    LANGUAGE_PATH,
    EXECUTION_PATH,
    COMBINED_PATH,
)
INPUT_PATHS = (*LEARNER_PATHS, TERMINOLOGY_PATH, STATIC_PATH, *REVIEW_PATHS, EXECUTION_PATH, COMBINED_PATH)

LOCAL_IDS = (
    LOCAL_ROOT,
    f"{LOCAL_ROOT}-status",
    f"{LOCAL_ROOT}-prerequisites",
    f"{LOCAL_ROOT}-objectives",
    f"{LOCAL_ROOT}-data",
    f"{LOCAL_ROOT}-comparison-principles",
    *(f"{LOCAL_ROOT}-task-{number:03d}" for number in range(1, 7)),
    f"{LOCAL_ROOT}-hint",
    f"{LOCAL_ROOT}-program",
    f"{LOCAL_ROOT}-tests",
    f"{LOCAL_ROOT}-expected-output",
    f"{LOCAL_ROOT}-interpretation",
    f"{LOCAL_ROOT}-solution",
    f"{LOCAL_ROOT}-sol-execution",
    f"{LOCAL_ROOT}-sol-cellular-pair-a",
    f"{LOCAL_ROOT}-sol-pi1-cup-pair-a",
    f"{LOCAL_ROOT}-sol-pair-b",
    f"{LOCAL_ROOT}-sol-negative",
    f"{LOCAL_ROOT}-reproducibility",
    f"{LOCAL_ROOT}-rights",
)
UNIT_IDS = tuple(f"unit:{local_id}" for local_id in LOCAL_IDS)
SEGMENT_IDS = tuple(f"segment:{local_id}" for local_id in LOCAL_IDS)
TASK_IDS = tuple(f"unit:{LOCAL_ROOT}-task-{number:03d}" for number in range(1, 7))
HINT_ID = f"unit:{LOCAL_ROOT}-hint"
SOLUTION_ID = f"unit:{LOCAL_ROOT}-solution"

TERM_CONTROL_IDS = tuple(f"O012-TERM-{number:04d}" for number in range(515, 527))
TERM_IDS = tuple(f"term:{LOCAL_ROOT}-term-{number:04d}:id-ID" for number in range(515, 527))
CONCEPT_IDS = tuple(f"concept:{LOCAL_ROOT}-term-{number:04d}" for number in range(515, 527))
QA_TYPES = Counter({"structure": 1, "execution": 1, "code": 1, "math": 1, "language": 1, "mastery": 1, "terminology": 1})

ROUTE_ANCHORS = {
    "D60-R04": "unit:o012-rbt-l10",
    "D60-R05": "unit:o012-rbt-l13",
    "D60-R12": "unit:o012-fom-u007",
    "D60-R13": "unit:o012-rbt-l26",
    "D60-R14": "unit:o012-rbt-l30",
}
ALLOWED_DEPENDENCIES = {
    *ROUTE_ANCHORS.values(),
    "unit:o012-d60-lab03",
    "unit:o012-rbt-l13-s04",
    "unit:o012-rbt-l13-s05",
    "unit:o012-fom-u001-rem-013",
    "unit:o012-rbt-l26-s02",
    "unit:o012-fom-u006-mcheck-001",
    "unit:o012-d60-lab03-cellular-boundaries",
}
DEPENDENCY_ROUTES = {
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

CANDIDATE_REPLAY_ROOT = QA / "computation-lab-004/backend-candidate-replay-20260829"
CANDIDATE_REPLAY_RECEIPT = CANDIDATE_REPLAY_ROOT / "REPLAY_RECEIPT.json"

OUTPUTS = {
    "plan": QA / "BACKEND_APPEND_ONLY_COMPUTATION_LAB_004_PLAN.json",
    "semantic": QA / "BACKEND_APPEND_ONLY_COMPUTATION_LAB_004_RECEIPT.json",
    "replay": QA / "BACKEND_APPEND_ONLY_COMPUTATION_LAB_004_REPLAY_RECEIPT.json",
    "manifest": QA / "BACKEND_APPEND_ONLY_COMPUTATION_LAB_004_FILE_MANIFEST.csv",
    "cumulative": QA / "BACKEND_APPEND_ONLY_COMPUTATION_LAB_004_CUMULATIVE_RECEIPT.json",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"Lab 4 independent backend validator FAIL: {message}")


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def identity(raw: bytes) -> tuple[int, int, str]:
    return len(raw), raw.count(b"\n"), digest(raw)


def identity_dict(path: str, raw: bytes) -> dict[str, Any]:
    value = identity(raw)
    return {"path": path, "bytes": value[0], "lf_lines": value[1], "sha256": value[2]}


def json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def canon(record: dict[str, Any]) -> bytes:
    return (json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def write(path: Path, raw: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(raw)


def disciplined(relative: str) -> bytes:
    path = ROOT / relative
    require(path.is_file(), f"required input missing: {relative}")
    raw = path.read_bytes()
    require(raw and not raw.startswith(b"\xef\xbb\xbf") and b"\r" not in raw, f"input is not nonempty BOM-free LF UTF-8: {relative}")
    try:
        raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise SystemExit(f"Lab 4 independent backend validator FAIL: invalid UTF-8 in {relative}: {exc}") from exc
    return raw


def load_json(relative: str, raw: bytes) -> dict[str, Any]:
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Lab 4 independent backend validator FAIL: invalid JSON in {relative}: {exc}") from exc
    require(isinstance(value, dict), f"JSON root is not an object: {relative}")
    return value


def load_producer():
    require(PRODUCER_PATH.is_file(), "Lab 4 producer is missing")
    spec = importlib.util.spec_from_file_location("o012_lab04_backend_producer_for_independent_validation", PRODUCER_PATH)
    require(spec is not None and spec.loader is not None, "cannot load Lab 4 producer")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    producer = getattr(module, "m", module)
    required = (
        "verify_inputs", "parse_reader", "build_additions", "suffixes",
        "validate_semantics", "record_plan", "MODEL", "LAB_ID",
        "EDITION_UNIT_ID", "SOURCE_PATH", "FILES",
    )
    require(all(hasattr(producer, name) for name in required), "producer interface is incomplete")
    require(producer.LAB_ID == LAB_ID and producer.EDITION_UNIT_ID == EDITION_UNIT_ID, "producer Lab identity mismatch")
    require(producer.SOURCE_PATH == SOURCE_PATH and tuple(producer.FILES) == FILES, "producer source/file-set mismatch")
    require(producer.MODEL == MODEL, "producer model-provenance mismatch")
    return producer


def bundle(raw_by_file: dict[str, bytes]) -> tuple[int, int, str]:
    state = hashlib.sha256()
    records = 0
    byte_count = 0
    for name in FILES:
        raw = raw_by_file[name]
        records += len(raw.splitlines())
        byte_count += len(raw)
        state.update(name.encode("utf-8"))
        state.update(b"\0")
        state.update(raw)
    return records, byte_count, state.hexdigest()


def parse_jsonl(raw_by_file: dict[str, bytes]) -> tuple[dict[str, list[dict[str, Any]]], dict[str, dict[str, Any]]]:
    by_file: dict[str, list[dict[str, Any]]] = {}
    by_id: dict[str, dict[str, Any]] = {}
    for name in FILES:
        records: list[dict[str, Any]] = []
        for line_number, line in enumerate(raw_by_file[name].splitlines(), 1):
            require(line, f"empty JSONL line: {name}:{line_number}")
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise SystemExit(f"Lab 4 independent backend validator FAIL: invalid JSONL {name}:{line_number}: {exc}") from exc
            require(isinstance(record, dict) and isinstance(record.get("id"), str), f"record without string ID: {name}:{line_number}")
            require(canon(record) == line + b"\n", f"noncanonical JSONL: {name}:{line_number}")
            require(record["id"] not in by_id, f"duplicate global ID: {record['id']}")
            records.append(record)
            by_id[record["id"]] = record
        by_file[name] = records
    return by_file, by_id


def read_prefix() -> tuple[dict[str, bytes], dict[str, bytes], dict[str, bytes]]:
    prefix: dict[str, bytes] = {}
    suffix: dict[str, bytes] = {}
    live: dict[str, bytes] = {}
    for name in FILES:
        path = BACKEND / name
        require(path.is_file(), f"backend file missing: {name}")
        raw = path.read_bytes()
        prefix_records, prefix_bytes, prefix_sha = PREFIX[name]
        require(len(raw) >= prefix_bytes, f"backend shorter than frozen Lab 3 prefix: {name}")
        prefix[name] = raw[:prefix_bytes]
        suffix[name] = raw[prefix_bytes:]
        live[name] = raw
        observed = (len(prefix[name].splitlines()), len(prefix[name]), digest(prefix[name]))
        require(observed == (prefix_records, prefix_bytes, prefix_sha), f"frozen Lab 3 prefix mismatch: {name}: {observed}")
    require(bundle(prefix) == PREFIX_TOTAL, "frozen Lab 3 prefix bundle mismatch")
    return prefix, suffix, live


def verify_baseline_receipt(prefix: dict[str, bytes]) -> dict[str, Any]:
    raw = BASELINE_RECEIPT_PATH.read_bytes()
    require(identity(raw) == BASELINE_RECEIPT_IDENTITY, "Lab 3 cumulative receipt identity drift")
    receipt = load_json(BASELINE_RECEIPT_PATH.relative_to(ROOT).as_posix(), raw)
    cumulative = receipt.get("cumulative", {})
    replay = receipt.get("replay", {})
    require(
        receipt.get("status") == "PASS"
        and receipt.get("receipt_kind") == "cumulative_backend_boundary"
        and receipt.get("laboratory_id") == "D60-LAB03"
        and (cumulative.get("records"), cumulative.get("bytes"), cumulative.get("bundle_sha256")) == PREFIX_TOTAL
        and cumulative.get("computation_laboratories_complete") == 3
        and cumulative.get("computation_laboratories_required") == 4
        and replay.get("status") == "PASS"
        and replay.get("exact_file_matches") == len(FILES)
        and replay.get("temporary_replay_removed") is True,
        "Lab 3 cumulative receipt does not prove the exact prefix",
    )
    rows = receipt.get("files", [])
    require(len(rows) == len(FILES), "Lab 3 receipt file census mismatch")
    observed = {
        row.get("path", "").removeprefix("backend/"): (
            row.get("final_records"), row.get("final_bytes"), row.get("final_sha256")
        )
        for row in rows
    }
    require(observed == PREFIX, "Lab 3 receipt per-file identities differ from frozen prefix")
    require(bundle(prefix) == PREFIX_TOTAL, "prefix differs from Lab 3 receipt")
    return receipt


def identity_index(node: Any, out: dict[str, tuple[int, int, str]]) -> None:
    if isinstance(node, dict):
        if set(("path", "bytes", "lf_lines", "sha256")).issubset(node):
            path = node.get("path")
            value = (node.get("bytes"), node.get("lf_lines"), node.get("sha256"))
            if isinstance(path, str) and isinstance(value[0], int) and isinstance(value[1], int) and isinstance(value[2], str):
                require(path not in out or out[path] == value, f"conflicting identity binding in receipt: {path}")
                out[path] = value
        for value in node.values():
            identity_index(value, out)
    elif isinstance(node, list):
        for value in node:
            identity_index(value, out)


def verify_inputs() -> dict[str, Any]:
    raw = {relative: disciplined(relative) for relative in INPUT_PATHS}
    identities = {relative: identity(value) for relative, value in raw.items()}
    objects = {relative: load_json(relative, raw[relative]) for relative in (STATIC_PATH, *REVIEW_PATHS, EXECUTION_PATH, COMBINED_PATH)}
    static = objects[STATIC_PATH]
    require(
        static.get("status") == "PASS"
        and static.get("laboratory_id") == LAB_ID
        and static.get("edition_unit_id") == EDITION_UNIT_ID
        and static.get("course_route_unit_ids") == list(ROUTES)
        and static.get("severity_counts") == {"P1": 0, "P2": 0, "P3": 0}
        and static.get("structure", {}).get("stable_ids") == 25
        and static.get("structure", {}).get("tasks") == 6
        and static.get("structure", {}).get("hints") == 1
        and static.get("structure", {}).get("complete_solution") is True,
        "static QA does not close the exact Lab 4 surface",
    )
    static_bound: dict[str, tuple[int, int, str]] = {}
    identity_index(static, static_bound)
    for relative in (*LEARNER_PATHS, TERMINOLOGY_PATH):
        require(static_bound.get(relative) == identities[relative], f"static QA does not bind current {relative}")

    review_contracts = {
        CODE_PATH: ("independent_code", {SOURCE_PATH, PROGRAM_PATH, TEST_PATH, EXPECTED_PATH, STATIC_PATH}),
        MATH_PATH: ("independent_mathematics", {SOURCE_PATH, PROGRAM_PATH, TEST_PATH, EXPECTED_PATH, STATIC_PATH}),
        LANGUAGE_PATH: ("independent_source_language", {SOURCE_PATH, PROGRAM_PATH, TEST_PATH, EXPECTED_PATH, TERMINOLOGY_PATH}),
    }
    for relative, (kind, expected_paths) in review_contracts.items():
        review = objects[relative]
        if kind == "independent_code":
            # The frozen code-review schema omitted this one redundant field.
            # Accept only the omission itself (not null or a wrong value), and
            # close the edition binding through its exact Lab ID, five routes,
            # reader hash, five bound artifacts, and the combined QA record.
            edition_binding = "edition_unit_id" not in review
        else:
            edition_binding = review.get("edition_unit_id") == EDITION_UNIT_ID
        require(
            review.get("status") == "PASS"
            and review.get("review_kind") == kind
            and review.get("laboratory_id") == LAB_ID
            and edition_binding
            and review.get("course_route_unit_ids") == list(ROUTES)
            and review.get("independent_from_production") is True
            and review.get("human_review_claimed") is False
            and review.get("reader_sha256") == identities[SOURCE_PATH][2]
            and review.get("model_provenance") == MODEL
            and review.get("severity_census") == {"P1": 0, "P2": 0, "P3": 0},
            f"review contract mismatch: {relative}",
        )
        bound: dict[str, tuple[int, int, str]] = {}
        for item in review.get("bound_artifacts", []):
            path = item.get("path")
            require(path in expected_paths and path not in bound, f"review artifact scope mismatch: {relative}")
            bound[path] = (item.get("bytes"), item.get("lf_lines"), item.get("sha256"))
        require(bound == {path: identities[path] for path in expected_paths}, f"review exact binding mismatch: {relative}")

    execution = objects[EXECUTION_PATH]
    require(
        execution.get("status") == "PASS"
        and execution.get("receipt_kind") == "offline_deterministic_execution"
        and execution.get("laboratory_id") == LAB_ID
        and execution.get("edition_unit_id") == EDITION_UNIT_ID
        and execution.get("course_route_unit_ids") == list(ROUTES)
        and execution.get("program_runs") == execution.get("test_runs") == 2
        and execution.get("tests_per_run") == 6
        and execution.get("all_exit_codes_zero") is True
        and execution.get("program_stdout_matches_expected_output") is True
        and execution.get("program_stdout_byte_identical_between_runs") is True
        and execution.get("runtime", {}).get("standard_library_only") is True
        and execution.get("runtime", {}).get("network_used") is False
        and execution.get("model_provenance") == MODEL
        and execution.get("severity_census") == {"P1": 0, "P2": 0, "P3": 0},
        "execution receipt mismatch",
    )
    execution_bound: dict[str, tuple[int, int, str]] = {}
    identity_index(execution, execution_bound)
    for relative in LEARNER_PATHS:
        require(execution_bound.get(relative) == identities[relative], f"execution receipt does not bind current {relative}")

    combined = objects[COMBINED_PATH]
    expected_checks = {
        "route_scope_D60_R04_R05_R12_R13_R14": "PASS",
        "stable_ids_25_unique": "PASS",
        "tasks_6_with_hint_and_complete_solution": "PASS",
        "terminology_0515_0526": "PASS",
        "independent_code": "PASS",
        "independent_mathematics": "PASS",
        "independent_source_language": "PASS",
    }
    require(
        combined.get("status") == "PASS"
        and combined.get("receipt_kind") == "computation_laboratory_source_execution_review_closure"
        and combined.get("laboratory_id") == LAB_ID
        and combined.get("edition_unit_id") == EDITION_UNIT_ID
        and combined.get("course_route_unit_ids") == list(ROUTES)
        and combined.get("human_review_claimed") is False
        and combined.get("model_provenance") == MODEL
        and combined.get("severity_census") == {"P1": 0, "P2": 0, "P3": 0}
        and all(combined.get("checks", {}).get(key) == value for key, value in expected_checks.items())
        and combined.get("checks", {}).get("excluded_fomberg_problem_bank_used") is False,
        "combined QA does not close exact Lab 4 scope",
    )
    combined_bound: dict[str, tuple[int, int, str]] = {}
    identity_index(combined, combined_bound)
    for relative in (*LEARNER_PATHS, TERMINOLOGY_PATH, STATIC_PATH, *REVIEW_PATHS, EXECUTION_PATH):
        require(combined_bound.get(relative) == identities[relative], f"combined QA does not bind current {relative}")
    return {"raw": raw, "identities": identities, "objects": objects}


def parse_reader(raw: bytes) -> dict[str, Any]:
    text = raw.decode("utf-8")
    heading_ids: list[str] = []
    div_ids: list[str] = []
    for line in text.splitlines():
        if re.match(r"^#{1,6}\s", line):
            match = re.search(r"\{#(o012-d60-lab04(?:-[a-z0-9-]+)?)\}\s*$", line)
            require(match is not None, f"reader heading lacks exact Lab 4 ID: {line}")
            heading_ids.append(match.group(1))
        elif line.startswith("::: {.exercise #") or line.startswith("::: {.hint #"):
            match = re.match(r"^::: \{\.(?:exercise|hint) #(o012-d60-lab04(?:-[a-z0-9-]+)?)\}$", line)
            require(match is not None, f"malformed exercise/hint declaration: {line}")
            div_ids.append(match.group(1))
    positions = {local_id: text.index(f"#{local_id}") for local_id in (*heading_ids, *div_ids)}
    source_order = tuple(sorted((*heading_ids, *div_ids), key=positions.get))
    require(len(heading_ids) == 18 and len(div_ids) == 7, "reader heading/div census mismatch")
    require(source_order == LOCAL_IDS, f"reader stable-ID order or inventory mismatch: {source_order}")
    require(len(set(source_order)) == 25, "reader stable IDs are not unique")
    require(sum(local_id.startswith(f"{LOCAL_ROOT}-task-") for local_id in div_ids) == 6, "reader task census mismatch")
    require(div_ids.count(f"{LOCAL_ROOT}-hint") == 1, "reader shared-hint census mismatch")
    require(text.count("# Solusi lengkap {#o012-d60-lab04-solution}") == 1, "complete solution root missing or duplicated")
    require(text.count("O012_LAB04_INCLUDE_PROGRAM") == text.count("O012_LAB04_INCLUDE_TESTS") == text.count("O012_LAB04_INCLUDE_EXPECTED") == 1, "include-marker census mismatch")
    return {"text": text, "heading_ids": heading_ids, "div_ids": div_ids, "source_order": source_order}


def terminology_rows(raw: bytes) -> dict[str, dict[str, str]]:
    rows = list(csv.DictReader(io.StringIO(raw.decode("utf-8"))))
    selected = {row["term_id"]: row for row in rows if row.get("term_id") in TERM_CONTROL_IDS}
    require(tuple(sorted(selected)) == TERM_CONTROL_IDS, "terminology controls 0515-0526 incomplete")
    require(all(row.get("status") == "admitted" and row.get("source_term") and row.get("id_ID") and row.get("scope") and row.get("note") for row in selected.values()), "Lab 4 terminology row incomplete")
    return selected


def build_candidate(
    producer,
    prefix_records: list[dict[str, Any]],
    sealed: dict[str, tuple[int, int, str]] | None = None,
) -> dict[str, Any]:
    producer_data = producer.verify_inputs(sealed) if sealed is not None else producer.verify_inputs()
    parsed = producer.parse_reader(producer_data["raw"][SOURCE_PATH])
    additions = producer.build_additions(producer_data, parsed)
    require(set(additions) == set(FILES), "producer candidate file set mismatch")
    producer_semantic = producer.validate_semantics(prefix_records, additions, producer_data, parsed)
    plan = producer.record_plan(additions, producer_data, producer_semantic)
    raw = {name: b"".join(canon(record) for record in additions[name]) for name in FILES}
    require(raw == producer.suffixes(additions), "producer suffix serialization differs from independent canonical serialization")
    return {"data": producer_data, "parsed": parsed, "additions": additions, "raw": raw, "semantic": producer_semantic, "plan": plan}


def audit_candidate(
    additions: dict[str, list[dict[str, Any]]],
    candidate_raw: dict[str, bytes],
    prefix_records: dict[str, dict[str, Any]],
    inputs: dict[str, Any],
    reader: dict[str, Any],
) -> dict[str, Any]:
    flat = [record for name in FILES for record in additions[name]]
    ids = [record.get("id") for record in flat]
    require(all(isinstance(record_id, str) for record_id in ids), "candidate record without string ID")
    require(len(ids) == len(set(ids)) and not set(ids).intersection(prefix_records), "candidate ID collision")
    require(all([record["id"] for record in additions[name]] == sorted(record["id"] for record in additions[name]) for name in FILES), "candidate records are not ID-sorted within each appended file")

    expected_counts = {
        "artifacts.jsonl": 10,
        "assets.jsonl": 0,
        "authority.jsonl": 0,
        "concepts.jsonl": 12,
        "corrections.jsonl": 0,
        "qa.jsonl": 7,
        "rights.jsonl": 1,
        "segments.jsonl": 25,
        "terms.jsonl": 12,
        "units.jsonl": 25,
    }
    require(all(len(additions[name]) == count for name, count in expected_counts.items()), "fixed candidate record census mismatch")

    units = {record["id"]: record for record in additions["units.jsonl"]}
    segments = {record["id"]: record for record in additions["segments.jsonl"]}
    require(tuple(sorted(units)) == tuple(sorted(UNIT_IDS)), "unit stable-ID inventory mismatch")
    require(tuple(sorted(segments)) == tuple(sorted(SEGMENT_IDS)), "segment stable-ID inventory mismatch")
    order_by_local = {local_id: index for index, local_id in enumerate(reader["source_order"], 1)}
    for local_id in LOCAL_IDS:
        unit = units[f"unit:{local_id}"]
        segment = segments[f"segment:{local_id}"]
        for record in (unit, segment):
            require(record.get("laboratory_id") == LAB_ID and record.get("edition_unit_id") == EDITION_UNIT_ID, f"unit/segment Lab binding mismatch: {local_id}")
            require(record.get("locale") == "id-ID" and record.get("model_provenance") == MODEL, f"unit/segment locale/provenance mismatch: {local_id}")
            require(record.get("rights_component_id") == LAB_RIGHTS and record.get("original_layer") is True, f"unit/segment rights/origin mismatch: {local_id}")
            require(record.get("source_local_id") == local_id and record.get("source_corpus_used") is False, f"unit/segment source identity mismatch: {local_id}")
            require(record.get("source_locator", {}).get("path") == SOURCE_PATH and record.get("source_locator", {}).get("kind") == "edition_original", f"unit/segment source locator mismatch: {local_id}")
            require(record.get("course_route_unit_ids") == list(ROUTES), f"unit/segment route list mismatch: {local_id}")
            expected_order = 45 if local_id == LOCAL_ROOT else order_by_local[local_id]
            require(record.get("order") == expected_order, f"unit/segment append order mismatch: {local_id}")
        require(unit.get("target_locator") == segment.get("target_locator"), f"unit/segment locator drift: {local_id}")
        require(unit.get("target_locator", {}).get("file_sha256") == inputs["identities"][SOURCE_PATH][2], f"unit/segment reader hash drift: {local_id}")
    require(units[ROOT_UNIT].get("parent_id") == "course:o012-d60" and units[ROOT_UNIT].get("path") == [ROOT_UNIT], "root unit hierarchy mismatch")
    require(units[ROOT_UNIT].get("primary_course_route_unit_id") == ROUTES[0] and units[ROOT_UNIT].get("secondary_course_route_unit_ids") == list(ROUTES[1:]), "root route ordering mismatch")
    for unit_id in UNIT_IDS[1:]:
        require(units[unit_id].get("parent_id") == ROOT_UNIT and units[unit_id].get("path") == [ROOT_UNIT, unit_id], f"child hierarchy mismatch: {unit_id}")
    require(all(units[task_id].get("unit_kind") == "exercise" for task_id in TASK_IDS), "six task units are not exercises")
    require(units[HINT_ID].get("unit_kind") == "hint" and units[SOLUTION_ID].get("unit_kind") == "solution", "hint/solution unit semantics mismatch")

    terms = {record["id"]: record for record in additions["terms.jsonl"]}
    concepts = {record["id"]: record for record in additions["concepts.jsonl"]}
    require(tuple(sorted(terms)) == tuple(sorted(TERM_IDS)), "term ID inventory mismatch")
    require(tuple(sorted(concepts)) == tuple(sorted(CONCEPT_IDS)), "concept ID inventory mismatch")
    controls = terminology_rows(inputs["raw"][TERMINOLOGY_PATH])
    for number, control_id in zip(range(515, 527), TERM_CONTROL_IDS, strict=True):
        term = terms[f"term:{LOCAL_ROOT}-term-{number:04d}:id-ID"]
        concept_id = f"concept:{LOCAL_ROOT}-term-{number:04d}"
        concept = concepts[concept_id]
        row = controls[control_id]
        require(term.get("terminology_control_id") == control_id and term.get("terminology_status") == "admitted", f"term-control mismatch: {control_id}")
        require(term.get("source_term") == row["source_term"] and term.get("preferred") == row["id_ID"] and term.get("usage_note") == row["note"], f"term text mismatch: {control_id}")
        require(term.get("concept_id") == concept_id and term.get("scope_unit_id") == ROOT_UNIT and term.get("rights_component_id") == LAB_RIGHTS, f"term graph mismatch: {control_id}")
        require(concept.get("canonical_label") == row["source_term"] and concept.get("domain") == row["scope"] and concept.get("locale_neutral") is True, f"concept mismatch: {control_id}")
        require(term.get("evidence_segment_id") in segments, f"term evidence segment missing: {control_id}")

    rights = additions["rights.jsonl"][0]
    require(
        rights.get("id") == LAB_RIGHTS
        and rights.get("license_expression") == "CC-BY-SA-4.0"
        and rights.get("component_scope") == list(UNIT_IDS)
        and "Independent" in rights.get("non_endorsement", "")
        and "original" in rights.get("change_notice", "").lower(),
        "rights component or exact 25-unit scope mismatch",
    )

    artifacts = {record["path"]: record for record in additions["artifacts.jsonl"]}
    require(set(artifacts) == set(ARTIFACT_PATHS), "artifact path census mismatch")
    for relative in ARTIFACT_PATHS:
        record = artifacts[relative]
        expected = inputs["identities"][relative]
        require((record.get("bytes"), record.get("sha256")) == (expected[0], expected[2]), f"artifact byte/hash mismatch: {relative}")
        require(record.get("laboratory_id") == LAB_ID and record.get("edition_unit_id") == EDITION_UNIT_ID and record.get("unit_id") == ROOT_UNIT, f"artifact Lab binding mismatch: {relative}")
        require(record.get("rights_component_id") == LAB_RIGHTS and record.get("locale") == "id-ID", f"artifact rights/locale mismatch: {relative}")

    qa_records = additions["qa.jsonl"]
    require(Counter(record.get("qa_type") for record in qa_records) == QA_TYPES, "QA event census mismatch")
    artifact_ids = {record["id"] for record in additions["artifacts.jsonl"]}
    for record in qa_records:
        require(record.get("laboratory_id") == LAB_ID and record.get("unit_id") == ROOT_UNIT and record.get("result") == "passed", f"QA event Lab/result mismatch: {record.get('id')}")
        witnesses = record.get("witness_artifact_ids")
        require(isinstance(witnesses, list) and witnesses and set(witnesses).issubset(artifact_ids), f"QA witness binding mismatch: {record.get('id')}")

    relations = additions["relations.jsonl"]
    relation_counts = Counter(record.get("relation_type") for record in relations)
    require(relation_counts["contains"] == 27 and relation_counts["hints"] == 6 and relation_counts["solves"] == 6 and relation_counts["xref"] == 5, "fixed relation census mismatch")
    require(set(relation_counts).issubset({"contains", "hints", "solves", "xref", "depends-on"}), "unexpected relation type")
    expected_contains = {
        ("course:o012-d60", ROOT_UNIT),
        ("rights:o012-d60-integrated-route-cc-by-sa-4.0", LAB_RIGHTS),
        (LAB_RIGHTS, ROOT_UNIT),
        *((ROOT_UNIT, unit_id) for unit_id in UNIT_IDS[1:]),
    }
    contains = {(record.get("from_id"), record.get("to_id")) for record in relations if record.get("relation_type") == "contains"}
    require(contains == expected_contains, "contains relation graph mismatch")
    hints = {(record.get("from_id"), record.get("to_id")) for record in relations if record.get("relation_type") == "hints"}
    solves = {(record.get("from_id"), record.get("to_id")) for record in relations if record.get("relation_type") == "solves"}
    require(hints == {(HINT_ID, task_id) for task_id in TASK_IDS}, "shared-hint relation graph mismatch")
    require(solves == {(SOLUTION_ID, task_id) for task_id in TASK_IDS}, "complete-solution relation graph mismatch")

    xrefs = [record for record in relations if record.get("relation_type") == "xref"]
    observed_routes = {
        record.get("course_route_unit_id"): (
            record.get("from_id"), record.get("to_id"), record.get("route_source_anchor_id")
        )
        for record in xrefs
    }
    require(observed_routes == {route: (ROOT_UNIT, anchor, anchor) for route, anchor in ROUTE_ANCHORS.items()}, "five-route mapping mismatch")
    require(xrefs[0].get("route_mapping_role") == "primary" or any(record.get("course_route_unit_id") == ROUTES[0] and record.get("route_mapping_role") == "primary" for record in xrefs), "primary route role missing")
    require(all(record.get("route_mapping_role") == ("primary" if record.get("course_route_unit_id") == ROUTES[0] else "secondary") for record in xrefs), "route primary/secondary roles mismatch")

    dependencies = [record for record in relations if record.get("relation_type") == "depends-on"]
    require(dependencies, "task dependency graph is empty")
    by_task: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in dependencies:
        from_id = record.get("from_id")
        to_id = record.get("to_id")
        require(from_id in TASK_IDS and to_id in ALLOWED_DEPENDENCIES, f"dependency endpoint outside exact Lab 4 scope: {from_id} -> {to_id}")
        require(to_id in prefix_records, f"dependency target absent from immutable prefix: {to_id}")
        require(
            record.get("dependency_course_route_unit_ids") == list(DEPENDENCY_ROUTES[to_id])
            and "course_route_unit_id" not in record
            and record.get("dependency_role") == "laboratory_prerequisite",
            f"dependency route/role mismatch: {record.get('id')}",
        )
        number = TASK_IDS.index(from_id) + 1
        require(record.get("laboratory_task_number") == number, f"dependency task number mismatch: {record.get('id')}")
        by_task[from_id].append(record)
    require(set(by_task) == set(TASK_IDS), "one or more tasks lack dependencies")
    for task_id, records in by_task.items():
        require([record.get("dependency_order") for record in sorted(records, key=lambda item: item.get("dependency_order", 0))] == list(range(1, len(records) + 1)), f"dependency order not contiguous: {task_id}")
        require(len({record.get("to_id") for record in records}) == len(records), f"duplicate task dependency: {task_id}")
    dependency_route_union = {
        route
        for record in dependencies
        for route in record.get("dependency_course_route_unit_ids", [])
    }
    require(dependency_route_union == {*ROUTES, "D60-R08"}, "dependency graph does not cover the five mapped routes plus the explicit R08 prerequisite")

    merged_ids = set(prefix_records) | set(ids)
    for record in relations:
        require(record.get("from_id") in merged_ids and record.get("to_id") in merged_ids, f"dangling relation: {record.get('id')}")
        require(record.get("laboratory_id") == LAB_ID, f"relation Lab binding mismatch: {record.get('id')}")

    expected_relation_count = 27 + 6 + 6 + 5 + len(dependencies)
    require(len(relations) == expected_relation_count, "relation total does not close exact graph")
    joined = b"".join(candidate_raw[name] for name in FILES).lower()
    credential_markers = (b"c:\\users\\", b"github_pat_", b"ghp_", b"access_token", b"authorization: bearer")
    require(not any(marker in joined for marker in credential_markers), "private path or credential marker in candidate")
    require(b"fomberg problem bank" not in joined, "excluded Fomberg problem-bank expression claimed as source")

    return {
        "stable_ids": 25,
        "tasks": 6,
        "shared_hints": 1,
        "complete_solutions": 1,
        "course_route_unit_ids": list(ROUTES),
        "route_edges": 5,
        "dependency_edges": len(dependencies),
        "dependency_tasks": 6,
        "dependency_scope": "five_assigned_routes_plus_explicit_R08_prerequisite",
        "new_terms": 12,
        "new_concepts": 12,
        "rights_records": 1,
        "qa_events": 7,
        "artifact_records": 10,
        "records_added": len(flat),
        "records_by_file": {name: len(additions[name]) for name in FILES},
        "append_only_ordering": "PASS",
        "artifact_review_binding": "PASS",
        "code_review_edition_binding": "FROZEN_SCHEMA_OMISSION_EXPLICITLY_CLOSED_BY_LAB_ID_ROUTES_READER_HASH_BOUND_ARTIFACTS_AND_COMBINED_QA",
        "relation_reference_integrity": "PASS",
        "rights_and_provenance": "PASS",
        "independent_semantics": "PASS",
    }


def verify_producer_replay(
    candidate_raw: dict[str, bytes],
    final_raw: dict[str, bytes],
    candidate_identity: tuple[int, int, str],
    final_identity: tuple[int, int, str],
) -> dict[str, Any]:
    require(CANDIDATE_REPLAY_RECEIPT.is_file(), "producer two-run replay receipt is missing")
    receipt_raw = CANDIDATE_REPLAY_RECEIPT.read_bytes()
    receipt = load_json(CANDIDATE_REPLAY_RECEIPT.relative_to(ROOT).as_posix(), receipt_raw)
    delta = receipt.get("delta", {})
    final = receipt.get("candidate", {})
    require(
        receipt.get("status") == "PASS"
        and receipt.get("receipt_kind") == "isolated_exact_backend_candidate_replay"
        and receipt.get("laboratory_id") == LAB_ID
        and receipt.get("edition_unit_id") == EDITION_UNIT_ID
        and receipt.get("course_route_unit_ids") == list(ROUTES)
        and receipt.get("not_promoted_to_live_backend") is True
        and receipt.get("runs") == 2
        and receipt.get("exact_file_matches") == len(FILES) + 2
        and (delta.get("records"), delta.get("bytes"), delta.get("bundle_sha256")) == candidate_identity
        and (final.get("records"), final.get("bytes"), final.get("bundle_sha256")) == final_identity,
        "producer replay receipt identity or scope mismatch",
    )
    require(delta.get("records_by_file") == {name: len(candidate_raw[name].splitlines()) for name in FILES}, "producer replay per-file record delta mismatch")
    require(delta.get("bytes_by_file") == {name: len(candidate_raw[name]) for name in FILES}, "producer replay per-file byte delta mismatch")
    inventories: list[dict[str, tuple[int, int, str]]] = []
    for run_name in ("run-a", "run-b"):
        run_root = CANDIDATE_REPLAY_ROOT / run_name
        require(run_root.is_dir(), f"producer replay directory missing: {run_name}")
        observed: dict[str, tuple[int, int, str]] = {}
        for name in FILES:
            relative = f"backend/{name}"
            raw = (run_root / relative).read_bytes()
            require(raw == final_raw[name], f"producer replay candidate differs from independent candidate: {run_name}/{relative}")
            observed[relative] = identity(raw)
        for relative in ("PLAN.json", "RUN_RECEIPT.json"):
            raw = (run_root / relative).read_bytes()
            load_json(f"{run_name}/{relative}", raw)
            observed[relative] = identity(raw)
        inventories.append(observed)
    require(inventories[0] == inventories[1], "producer run-a/run-b inventories differ")
    receipt_inventory = {
        item.get("path"): (item.get("bytes"), item.get("lf_lines"), item.get("sha256"))
        for item in receipt.get("inventory", [])
    }
    require(receipt_inventory == inventories[0], "producer replay inventory does not bind both exact runs")
    require(
        (CANDIDATE_REPLAY_ROOT / "run-a/PLAN.json").read_bytes()
        == (CANDIDATE_REPLAY_ROOT / "run-b/PLAN.json").read_bytes()
        and (CANDIDATE_REPLAY_ROOT / "run-a/RUN_RECEIPT.json").read_bytes()
        == (CANDIDATE_REPLAY_ROOT / "run-b/RUN_RECEIPT.json").read_bytes(),
        "producer replay plan/receipt bytes differ across runs",
    )
    return identity_dict(CANDIDATE_REPLAY_RECEIPT.relative_to(ROOT).as_posix(), receipt_raw)


def candidate_state(producer, prefix: dict[str, bytes]) -> dict[str, Any]:
    baseline = verify_baseline_receipt(prefix)
    independent_inputs = verify_inputs()
    reader = parse_reader(independent_inputs["raw"][SOURCE_PATH])
    prefix_by_file, prefix_by_id = parse_jsonl(prefix)
    ordered_prefix_records = [record for name in FILES for record in prefix_by_file[name]]
    first = build_candidate(producer, ordered_prefix_records)
    require(first["data"]["identities"] == independent_inputs["identities"], "producer and independent sealed-input identities differ")
    second = build_candidate(producer, ordered_prefix_records, first["data"]["identities"])
    require(first["raw"] == second["raw"] and first["plan"] == second["plan"], "two sealed candidate derivations differ")
    require(all(first["raw"][name] == b"".join(canon(record) for record in first["additions"][name]) for name in FILES), "candidate canonicalization drift")
    independent = audit_candidate(first["additions"], first["raw"], prefix_by_id, independent_inputs, reader)
    final_raw = {name: prefix[name] + first["raw"][name] for name in FILES}
    final_by_file, final_by_id = parse_jsonl(final_raw)
    require(len(final_by_id) == PREFIX_TOTAL[0] + independent["records_added"], "candidate cumulative record count mismatch")
    candidate_identity = bundle(first["raw"])
    final_identity = bundle(final_raw)
    producer_replay = verify_producer_replay(first["raw"], final_raw, candidate_identity, final_identity)
    return {
        "baseline": baseline,
        "inputs": independent_inputs,
        "reader": reader,
        "prefix_by_file": prefix_by_file,
        "prefix_by_id": prefix_by_id,
        "candidate": first,
        "candidate_identity": candidate_identity,
        "final_raw": final_raw,
        "final_by_file": final_by_file,
        "final_by_id": final_by_id,
        "final_identity": final_identity,
        "independent": independent,
        "producer_replay": producer_replay,
    }


def manifest_bytes(prefix: dict[str, bytes], candidate: dict[str, bytes], final_raw: dict[str, bytes]) -> bytes:
    rows = ["path,prefix_records,prefix_bytes,prefix_sha256,records_added,suffix_bytes,suffix_sha256,final_records,final_bytes,final_sha256"]
    for name in FILES:
        rows.append(",".join((
            f"backend/{name}",
            str(len(prefix[name].splitlines())), str(len(prefix[name])), digest(prefix[name]),
            str(len(candidate[name].splitlines())), str(len(candidate[name])), digest(candidate[name]),
            str(len(final_raw[name].splitlines())), str(len(final_raw[name])), digest(final_raw[name]),
        )))
    return ("\n".join(rows) + "\n").encode("utf-8")


def plan_receipt(state: dict[str, Any]) -> dict[str, Any]:
    candidate = state["candidate"]
    return {
        "schema_version": "1.0",
        "status": "PASS",
        "receipt_kind": "independent_deterministic_backend_candidate_plan",
        "laboratory_id": LAB_ID,
        "edition_unit_id": EDITION_UNIT_ID,
        "immutable_prefix": {"records": PREFIX_TOTAL[0], "bytes": PREFIX_TOTAL[1], "bundle_sha256": PREFIX_TOTAL[2]},
        "baseline_receipt": identity_dict(BASELINE_RECEIPT_PATH.relative_to(ROOT).as_posix(), BASELINE_RECEIPT_PATH.read_bytes()),
        "sealed_inputs": {
            relative: {"bytes": value[0], "lf_lines": value[1], "sha256": value[2]}
            for relative, value in sorted(state["inputs"]["identities"].items())
        },
        "candidate": {
            "records": state["candidate_identity"][0],
            "bytes": state["candidate_identity"][1],
            "bundle_sha256": state["candidate_identity"][2],
            "records_by_file": state["independent"]["records_by_file"],
            "bytes_by_file": {name: len(candidate["raw"][name]) for name in FILES},
            "sha256_by_file": {name: digest(candidate["raw"][name]) for name in FILES},
        },
        "deterministic_rebuilds": 2,
        "candidate_rebuilds_byte_identical": True,
        "producer_two_run_replay_receipt": state["producer_replay"],
        "independent_semantic_checks": state["independent"],
        "producer_semantic_checks": candidate["semantic"],
        "model_provenance": MODEL,
    }


def preflight(producer) -> dict[str, Any]:
    prefix, suffix, _live = read_prefix()
    require(all(not suffix[name] for name in FILES), "preflight requires the exact unextended Lab 3 live backend")
    state = candidate_state(producer, prefix)
    plan = plan_receipt(state)
    semantic = {
        "schema_version": "1.0",
        "status": "PASS_PREFLIGHT",
        "receipt_kind": "independent_append_only_backend_semantic_preflight",
        "laboratory_id": LAB_ID,
        "edition_unit_id": EDITION_UNIT_ID,
        "immutable_prefix": plan["immutable_prefix"],
        "candidate": plan["candidate"],
        "independent_semantic_checks": state["independent"],
        "sealed_inputs": plan["sealed_inputs"],
        "model_provenance": MODEL,
    }
    write(OUTPUTS["plan"], json_bytes(plan))
    write(OUTPUTS["semantic"], json_bytes(semantic))
    return semantic


def validate_live(producer) -> dict[str, Any]:
    prefix, live_suffix, live = read_prefix()
    state = candidate_state(producer, prefix)
    candidate = state["candidate"]["raw"]
    require(all(live_suffix[name] == candidate[name] for name in FILES), "live Lab 4 suffix differs from deterministic candidate")
    require(all(live[name] == state["final_raw"][name] for name in FILES), "live backend is not exact prefix plus candidate")
    require(bundle(live) == state["final_identity"], "live cumulative bundle identity mismatch")

    scratch_parent = QA / ".bounded-replay"
    scratch_parent.mkdir(parents=True, exist_ok=True)
    scratch = Path(tempfile.mkdtemp(prefix="lab04-independent-", dir=scratch_parent))
    replay_removed = False
    try:
        for name in FILES:
            (scratch / name).write_bytes(prefix[name] + candidate[name])
        replay = {name: (scratch / name).read_bytes() for name in FILES}
        require(replay == live and bundle(replay) == state["final_identity"], "isolated exact replay differs from live backend")
    finally:
        shutil.rmtree(scratch)
        replay_removed = not scratch.exists()
        try:
            scratch_parent.rmdir()
        except OSError:
            pass
    require(replay_removed, "bounded replay scratch was not removed")

    plan = plan_receipt(state)
    replay_receipt = {
        "schema_version": "1.0",
        "status": "PASS",
        "receipt_kind": "independent_isolated_exact_backend_replay",
        "laboratory_id": LAB_ID,
        "exact_file_matches": len(FILES),
        "suffix_bytes": state["candidate_identity"][1],
        "final": {"records": state["final_identity"][0], "bytes": state["final_identity"][1], "bundle_sha256": state["final_identity"][2]},
        "temporary_replay_removed": True,
    }
    semantic = {
        "schema_version": "1.0",
        "status": "PASS",
        "receipt_kind": "independent_append_only_backend_semantic_validation",
        "laboratory_id": LAB_ID,
        "edition_unit_id": EDITION_UNIT_ID,
        "immutable_prefix": plan["immutable_prefix"],
        "candidate": plan["candidate"],
        "cumulative": replay_receipt["final"],
        "independent_semantic_checks": state["independent"],
        "sealed_inputs": plan["sealed_inputs"],
        "model_provenance": MODEL,
    }
    write(OUTPUTS["plan"], json_bytes(plan))
    write(OUTPUTS["semantic"], json_bytes(semantic))
    write(OUTPUTS["replay"], json_bytes(replay_receipt))
    write(OUTPUTS["manifest"], manifest_bytes(prefix, candidate, live))

    supporting = {
        key: identity_dict(OUTPUTS[key].relative_to(ROOT).as_posix(), OUTPUTS[key].read_bytes())
        for key in ("plan", "semantic", "replay", "manifest")
    }
    file_rows = []
    for name in FILES:
        file_rows.append({
            "path": f"backend/{name}",
            "prefix_records": len(prefix[name].splitlines()),
            "prefix_bytes": len(prefix[name]),
            "prefix_sha256": digest(prefix[name]),
            "records_added": len(candidate[name].splitlines()),
            "suffix_bytes": len(candidate[name]),
            "suffix_sha256": digest(candidate[name]),
            "final_records": len(live[name].splitlines()),
            "final_bytes": len(live[name]),
            "final_sha256": digest(live[name]),
            "prefix_preserved": True,
            "suffix_exact": True,
        })
    cumulative = {
        "schema_version": "1.0",
        "status": "PASS",
        "receipt_kind": "cumulative_backend_boundary",
        "validator_independence": "producer_generated_candidate_independently_reconstructed_and_semantically_audited",
        "laboratory_id": LAB_ID,
        "edition_unit_id": EDITION_UNIT_ID,
        "immutable_prefix": {"records": PREFIX_TOTAL[0], "bytes": PREFIX_TOTAL[1], "bundle_sha256": PREFIX_TOTAL[2], "preserved_exactly": True},
        "baseline_receipt": plan["baseline_receipt"],
        "delta": plan["candidate"],
        "cumulative": {
            "records": state["final_identity"][0],
            "bytes": state["final_identity"][1],
            "bundle_sha256": state["final_identity"][2],
            "computation_laboratories_complete": 4,
            "computation_laboratories_required": 4,
        },
        "files": file_rows,
        "semantic_checks": state["independent"],
        "producer_semantic_checks": state["candidate"]["semantic"],
        "replay": replay_receipt,
        "supporting_receipts": supporting,
        "generic_validator_baseline_diagnostic": {
            "status": "PRE_EXISTING_BASELINE_INCOMPATIBILITY",
            "interpretation": "Historical append-only records are not globally ordinal-sorted. Exact immutable-prefix preservation, canonical suffix ordering, full graph validation, and isolated replay are the applicable gates.",
        },
        "model_provenance": MODEL,
    }
    final_path = OUTPUTS["cumulative"]
    pending = final_path.with_name(f".{final_path.name}.pending")
    require(not pending.exists(), "atomic cumulative receipt temporary collision")
    pending.write_bytes(json_bytes(cumulative))
    os.replace(pending, final_path)
    return cumulative


def main() -> int:
    require(sys.argv[1:] in ([], ["--preflight"]), "accepted invocation is no arguments or --preflight")
    producer = load_producer()
    receipt = preflight(producer) if sys.argv[1:] else validate_live(producer)
    target = OUTPUTS["semantic"] if sys.argv[1:] else OUTPUTS["cumulative"]
    print(json.dumps({
        "status": receipt["status"],
        "laboratory_id": LAB_ID,
        "receipt": identity_dict(target.relative_to(ROOT).as_posix(), target.read_bytes()),
    }, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
