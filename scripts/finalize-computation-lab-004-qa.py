#!/usr/bin/env python3
"""Seal execution and independent-review closure for O012/D60 Lab 4."""
from __future__ import annotations

import hashlib
import json
import platform
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source/id-ID/labs/computation-lab-004-cross-invariant-comparison.md"
PROGRAM = ROOT / "source/id-ID/labs/o012_d60_lab04_cross_invariants.py"
TESTS = ROOT / "source/id-ID/labs/test_o012_d60_lab04_cross_invariants.py"
EXPECTED = ROOT / "source/id-ID/labs/expected-output-lab04.txt"
TERMINOLOGY = ROOT / "00_control/TERMINOLOGY.csv"
PREDECESSOR = ROOT / (
    "output/html/roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-"
    "ca02-ca03-lab01-lab02-lab03/index.html"
)
STATIC = ROOT / "qa/computation-lab-004/STATIC_QA.json"
CODE_REVIEW = ROOT / "qa/computation-lab-004/INDEPENDENT_CODE_REVIEW.json"
MATH_REVIEW = ROOT / "qa/computation-lab-004/INDEPENDENT_MATH_REVIEW.json"
LANGUAGE_REVIEW = ROOT / "qa/computation-lab-004/INDEPENDENT_SOURCE_LANGUAGE_REVIEW.json"
EXECUTION = ROOT / "qa/computation-lab-004/EXECUTION_RECEIPT.json"
COMBINED = ROOT / "qa/COMPUTATION_LAB_004_QA.json"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"
ROUTES = ["D60-R04", "D60-R05", "D60-R12", "D60-R13", "D60-R14"]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"Lab 4 QA finalizer FAIL: {message}")


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def disciplined(path: Path) -> bytes:
    require(path.is_file(), f"missing input: {path.relative_to(ROOT).as_posix()}")
    raw = path.read_bytes()
    require(raw and b"\r" not in raw and raw.endswith(b"\n"), f"non-LF or empty input: {path.name}")
    raw.decode("utf-8", errors="strict")
    return raw


def identity(path: Path) -> dict[str, Any]:
    if path == PREDECESSOR:
        require(path.is_file(), "missing predecessor HTML")
        raw = path.read_bytes()
        require(raw, "empty predecessor HTML")
        raw.decode("utf-8", errors="strict")
    else:
        raw = disciplined(path)
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "bytes": len(raw),
        "lf_lines": raw.count(b"\n"),
        "sha256": digest(raw),
    }


def verify_bound(review: dict[str, Any], current: dict[str, dict[str, Any]]) -> None:
    bound_rows = review.get("bound_artifacts", [])
    require(isinstance(bound_rows, list) and bound_rows, "review has no bound artifacts")
    bound = {item.get("path"): item for item in bound_rows if isinstance(item, dict)}
    require(len(bound) == len(bound_rows), "review has malformed or duplicate bindings")
    for relative, item in bound.items():
        require(relative in current, f"review binds undeclared input: {relative}")
        observed = current[relative]
        require(
            (item.get("bytes"), item.get("lf_lines"), item.get("sha256"))
            == (observed["bytes"], observed["lf_lines"], observed["sha256"]),
            f"stale independent review binding: {relative}",
        )


def run(command: list[str]) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        command, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        timeout=180, check=False,
    )


def write_json(path: Path, payload: dict[str, Any]) -> None:
    raw = (json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(raw)


def main() -> int:
    learner = (SOURCE, PROGRAM, TESTS, EXPECTED)
    static_inputs = (*learner, TERMINOLOGY, PREDECESSOR)
    reviews = (CODE_REVIEW, MATH_REVIEW, LANGUAGE_REVIEW)
    all_inputs = (*static_inputs, STATIC, *reviews)
    current = {item["path"]: item for item in (identity(path) for path in all_inputs)}

    static = json.loads(disciplined(STATIC))
    require(static.get("status") == "PASS", "static QA is not PASS")
    require(static.get("laboratory_id") == "D60-LAB04", "static laboratory mismatch")
    require(static.get("course_route_unit_ids") == ROUTES, "static route mapping drift")
    require(static.get("severity_counts") == {"P1": 0, "P2": 0, "P3": 0}, "static findings remain")
    structure = static.get("structure", {})
    require(
        structure.get("stable_ids") == 25
        and structure.get("headings") == 18
        and structure.get("tasks") == 6
        and structure.get("hints") == 1
        and structure.get("solution_subsections") == 5,
        "learner-surface census drift",
    )
    for item in static.get("inputs", []):
        relative = item.get("path")
        require(relative in current, f"static QA binds unexpected input: {relative}")
        observed = current[relative]
        require(
            (item.get("bytes"), item.get("lf_lines"), item.get("sha256"))
            == (observed["bytes"], observed["lf_lines"], observed["sha256"]),
            f"static QA input drift: {relative}",
        )

    kinds = {
        CODE_REVIEW: "independent_code",
        MATH_REVIEW: "independent_mathematics",
        LANGUAGE_REVIEW: "independent_source_language",
    }
    for path, kind in kinds.items():
        receipt = json.loads(disciplined(path))
        require(receipt.get("status") == "PASS", f"{kind} review is not PASS")
        require(receipt.get("review_kind") == kind, f"{kind} review-kind mismatch")
        require(receipt.get("laboratory_id") == "D60-LAB04", f"{kind} laboratory mismatch")
        require(receipt.get("course_route_unit_ids") == ROUTES, f"{kind} route mismatch")
        require(receipt.get("independent_from_production") is True, f"{kind} is not independent")
        require(receipt.get("reader_sha256") == current[SOURCE.relative_to(ROOT).as_posix()]["sha256"], f"{kind} reader drift")
        require(receipt.get("severity_census") == {"P1": 0, "P2": 0, "P3": 0}, f"{kind} findings remain")
        require(receipt.get("human_review_claimed") is False, f"{kind} falsely claims human review")
        verify_bound(receipt, current)

    test_runs = [run([sys.executable, "-B", str(TESTS)]) for _ in range(2)]
    for result in test_runs:
        require(result.returncode == 0 and result.stdout == b"", "test suite failed or wrote stdout")
        require(b"Ran 6 tests" in result.stderr and result.stderr.rstrip().endswith(b"OK"), "test result drift")
    expected = disciplined(EXPECTED)
    program_runs = [run([sys.executable, "-B", str(PROGRAM)]) for _ in range(2)]
    for result in program_runs:
        require(result.returncode == 0 and result.stderr == b"", "program failed or wrote stderr")
        require(result.stdout == expected, "program stdout differs from expected output")
    require(program_runs[0].stdout == program_runs[1].stdout, "program stdout is nondeterministic")

    program_text = disciplined(PROGRAM).decode("utf-8")
    test_text = disciplined(TESTS).decode("utf-8")
    imports = re.findall(r"(?m)^(?:from|import)\s+([A-Za-z0-9_.]+)", program_text + "\n" + test_text)
    require(not any(name.split(".")[0] in {"requests", "numpy", "scipy", "sympy", "sage"} for name in imports), "non-standard import detected")
    require(not any(token in program_text for token in ("socket", "urlopen", "requests.", "subprocess", "random", "time.sleep")), "network/nondeterminism token in program")

    execution = {
        "schema_version": "1.0",
        "status": "PASS",
        "receipt_kind": "offline_deterministic_execution",
        "laboratory_id": "D60-LAB04",
        "edition_unit_id": "O012-ORIG-LAB04",
        "course_route_unit_ids": ROUTES,
        "runtime": {
            "implementation": platform.python_implementation(),
            "python_version": platform.python_version(),
            "standard_library_only": True,
            "network_used": False,
        },
        "commands": [
            "python -B source/id-ID/labs/test_o012_d60_lab04_cross_invariants.py",
            "python -B source/id-ID/labs/o012_d60_lab04_cross_invariants.py",
        ],
        "program_runs": 2,
        "test_runs": 2,
        "tests_per_run": 6,
        "all_exit_codes_zero": True,
        "program_stdout_byte_identical_between_runs": True,
        "program_stdout_matches_expected_output": True,
        "expected_output": current[EXPECTED.relative_to(ROOT).as_posix()],
        "learner_artifacts": [current[path.relative_to(ROOT).as_posix()] for path in learner],
        "model_provenance": MODEL,
        "severity_census": {"P1": 0, "P2": 0, "P3": 0},
    }
    write_json(EXECUTION, execution)
    execution_identity = identity(EXECUTION)

    combined_inputs = [current[path.relative_to(ROOT).as_posix()] for path in all_inputs]
    combined_inputs.append(execution_identity)
    joined = b"".join(
        path.read_bytes() if path == PREDECESSOR else disciplined(path)
        for path in (*all_inputs, EXECUTION)
    ).lower()
    private = (
        b"github_" + b"pat_", b"gh" + b"p_", b"access_" + b"token",
        b"authorization" + b": bearer", b"c:" + b"\\users\\",
    )
    require(not any(marker in joined for marker in private), "credential or private path marker detected")

    combined = {
        "schema_version": "1.0",
        "status": "PASS",
        "receipt_kind": "computation_laboratory_source_execution_review_closure",
        "laboratory_id": "D60-LAB04",
        "edition_unit_id": "O012-ORIG-LAB04",
        "course_route_unit_ids": ROUTES,
        "inputs": combined_inputs,
        "checks": {
            "stable_ids_25_unique": "PASS",
            "tasks_6_with_hint_and_complete_solution": "PASS",
            "offline_program_and_tests": "PASS",
            "two_program_runs_byte_identical": "PASS",
            "two_test_runs_6_of_6": "PASS",
            "expected_output_exact": "PASS",
            "independent_code": "PASS",
            "independent_mathematics": "PASS",
            "independent_source_language": "PASS",
            "route_scope_D60_R04_R05_R12_R13_R14": "PASS",
            "terminology_0515_0526": "PASS",
            "rights_origin_provenance_non_endorsement": "PASS",
            "excluded_fomberg_problem_bank_used": False,
            "privacy": "PASS",
        },
        "mathematical_result": static["independent_reference_calculation"],
        "model_provenance": MODEL,
        "upstream_contacted": False,
        "human_review_claimed": False,
        "severity_census": {"P1": 0, "P2": 0, "P3": 0},
    }
    write_json(COMBINED, combined)
    print(json.dumps({
        "status": "PASS", "laboratory_id": "D60-LAB04",
        "execution_receipt": identity(EXECUTION), "combined_receipt": identity(COMBINED),
    }, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
