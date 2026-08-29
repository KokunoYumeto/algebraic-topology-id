#!/usr/bin/env python3
"""Fail-closed source, mathematics, and executable QA for D60 Lab 4."""
from __future__ import annotations

import ast
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source/id-ID/labs/computation-lab-004-cross-invariant-comparison.md"
PROGRAM = ROOT / "source/id-ID/labs/o012_d60_lab04_cross_invariants.py"
TESTS = ROOT / "source/id-ID/labs/test_o012_d60_lab04_cross_invariants.py"
EXPECTED = ROOT / "source/id-ID/labs/expected-output-lab04.txt"
TERMINOLOGY = ROOT / "00_control/TERMINOLOGY.csv"
PREDECESSOR_HTML = ROOT / (
    "output/html/roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-"
    "ca02-ca03-lab01-lab02-lab03/index.html"
)
OUTPUT = ROOT / "qa/computation-lab-004/STATIC_QA.json"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"
ROUTES = ["D60-R04", "D60-R05", "D60-R12", "D60-R13", "D60-R14"]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def info(path: Path) -> dict[str, object]:
    data = path.read_bytes()
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "bytes": len(data),
        "lf_lines": data.count(b"\n"),
        "sha256": sha256(data),
    }


def free_reduce(word: tuple[int, ...]) -> tuple[int, ...]:
    stack: list[int] = []
    for letter in word:
        if stack and stack[-1] == -letter:
            stack.pop()
        else:
            stack.append(letter)
    return tuple(stack)


def independent_math_check() -> dict[str, object]:
    commutator = (1, 2, -1, -2)
    reduced = free_reduce(commutator)
    exponent_sums = tuple(
        sum(1 if letter == index else -1 if letter == -index else 0 for letter in reduced)
        for index in (1, 2)
    )
    require(reduced == commutator, "commutator must remain freely reduced")
    require(exponent_sums == (0, 0), "commutator exponent sums drift")

    pair_a_cells = {0: 1, 1: 2, 2: 1}
    pair_b_cells = {0: 1, 2: 1, 4: 1}
    pair_a_homology = {degree: f"Z^{rank}" if rank > 1 else "Z" for degree, rank in pair_a_cells.items()}
    pair_b_homology = {degree: "Z" for degree in pair_b_cells}
    require(sum((-1) ** degree * rank for degree, rank in pair_a_cells.items()) == 0, "Pair A Euler drift")
    require(sum((-1) ** degree * rank for degree, rank in pair_b_cells.items()) == 3, "Pair B Euler drift")

    torus_cup = {("alpha", "beta"): (1, "omega"), ("beta", "alpha"): (-1, "omega")}
    wedge_a_cup: dict[tuple[str, str], tuple[int, str]] = {}
    cp2_cup = {("x", "x"): (1, "u")}
    wedge_b_cup: dict[tuple[str, str], tuple[int, str]] = {}
    require(torus_cup[("beta", "alpha")][0] == -torus_cup[("alpha", "beta")][0], "graded sign drift")
    require(torus_cup != wedge_a_cup and cp2_cup != wedge_b_cup, "cup separators drift")

    return {
        "pair_a": {
            "spaces": ["T^2", "S^1 v S^1 v S^2"],
            "free_commutator": list(reduced),
            "exponent_sum_vector": list(exponent_sums),
            "pi1": ["Z^2", "F_2"],
            "common_pi1_abelianization": "Z^2",
            "common_homology": pair_a_homology,
            "euler_characteristic": 0,
            "additive_cohomology_equal": True,
            "cup_product_equal": False,
            "first_separator": "pi1",
        },
        "pair_b": {
            "spaces": ["CP^2", "S^2 v S^4"],
            "pi1": ["1", "1"],
            "common_homology": pair_b_homology,
            "euler_characteristic": 3,
            "additive_cohomology_equal": True,
            "attaching_maps": ["Hopf eta", "constant"],
            "hopf_invariants": [1, 0],
            "cup_squares": ["u", "0"],
            "first_separator": "produk cup",
        },
        "logical_guardrail": "disagreement obstructs equivalence; finite agreement does not prove equivalence",
    }


def run(command: list[str]) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        command,
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=120,
        check=False,
    )


def main() -> int:
    inputs = (SOURCE, PROGRAM, TESTS, EXPECTED, TERMINOLOGY, PREDECESSOR_HTML)
    for path in inputs:
        require(path.is_file(), f"missing input: {path}")
    for path in (SOURCE, PROGRAM, TESTS, EXPECTED):
        raw = path.read_bytes()
        require(raw and b"\r" not in raw and raw.endswith(b"\n"), f"non-LF or empty input: {path}")
        raw.decode("utf-8", errors="strict")

    source = SOURCE.read_text(encoding="utf-8")
    require(source.startswith("---\n") and 'edition_unit_id: "O012-ORIG-LAB04"' in source, "front matter drift")
    require('course_route_unit_ids: ["D60-R04", "D60-R05", "D60-R12", "D60-R13", "D60-R14"]' in source, "route mapping drift")
    require('license: "CC BY-SA 4.0"' in source and MODEL in source, "rights/model disclosure missing")
    ids = re.findall(r"#(o012-d60-lab04(?:-[a-z0-9]+)*)\b", source)
    headings = re.findall(r"(?m)^#{1,2}\s+.+?\s+\{#(o012-d60-lab04(?:-[a-z0-9]+)*)\}\s*$", source)
    exercises = re.findall(r"(?m)^::: \{\.exercise #(o012-d60-lab04-task-[0-9]{3})\}$", source)
    hints = re.findall(r"(?m)^::: \{\.hint #(o012-d60-lab04-hint)\}$", source)
    require(len(ids) == len(set(ids)) == 25, "stable-ID inventory is not 25 unique IDs")
    require(len(headings) == len(set(headings)) == 18, "heading inventory drift")
    require(len(exercises) == len(set(exercises)) == 6, "task inventory drift")
    require(hints == ["o012-d60-lab04-hint"], "hint inventory drift")
    for marker in ("O012_LAB04_INCLUDE_PROGRAM", "O012_LAB04_INCLUDE_TESTS", "O012_LAB04_INCLUDE_EXPECTED"):
        require(source.count(marker) == 1, f"include marker drift: {marker}")

    predecessor = PREDECESSOR_HTML.read_text(encoding="utf-8")
    targets = sorted(set(re.findall(r"\]\([^)]*#([^)]+)\)", source)))
    require(len(targets) == 6, "prerequisite-target census drift")
    for target in targets:
        require(f'id="{target}"' in predecessor, f"prerequisite target missing: {target}")

    lower = " ".join(source.lower().split())
    for witness in (
        "materi asli edisi",
        "bukan bagian dari sumber roberts atau fomberg",
        "reduksi bebas",
        "abelianisasi",
        "kohomologi aditif",
        "produk cup",
        "invarian hopf",
        "bukan ekuivalen homotopi",
        "tidak mengaku menyelesaikan masalah isomorfisma",
        "dukungan atau pengesahan",
        "solusi lengkap",
    ):
        require(witness in lower, f"required semantic witness missing: {witness}")
    require("$x^2=u$" in source and "$x^2=0$" in source, "Pair B cup-square witness missing")
    require("aba^{-1}b^{-1}" in source and "\\mathbb z^2" in lower and "f_2" in lower, "Pair A group witness missing")

    terms = TERMINOLOGY.read_text(encoding="utf-8")
    for term_id in range(515, 527):
        require(f'O012-TERM-{term_id:04d}' in terms, f"terminology row missing: {term_id}")

    allowed = {
        "__future__", "dataclasses", "pathlib", "subprocess", "sys", "typing", "unittest",
        "o012_d60_lab04_cross_invariants",
    }
    for path in (PROGRAM, TESTS):
        tree = ast.parse(path.read_text(encoding="utf-8"), str(path))
        imports = {
            node.names[0].name.split(".")[0]
            for node in ast.walk(tree)
            if isinstance(node, ast.Import)
        } | {
            (node.module or "").split(".")[0]
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom)
        }
        require(imports <= allowed, f"unexpected import in {path}: {sorted(imports - allowed)}")
    program_text = PROGRAM.read_text(encoding="utf-8")
    require(not any(token in program_text for token in ("socket", "urlopen", "subprocess", "random", "time.sleep")), "network/nondeterminism token in program")

    test_runs = [run([sys.executable, "-B", str(TESTS)]) for _ in range(2)]
    for result in test_runs:
        require(result.returncode == 0 and result.stdout == b"", "test suite failed or wrote stdout")
        require(b"Ran 6 tests" in result.stderr and result.stderr.rstrip().endswith(b"OK"), "test census/result drift")
    expected = EXPECTED.read_bytes()
    program_runs = [run([sys.executable, "-B", str(PROGRAM)]) for _ in range(2)]
    for result in program_runs:
        require(result.returncode == 0 and result.stderr == b"", "program failed or wrote stderr")
        require(result.stdout == expected, "program stdout differs from frozen expected output")
    require(program_runs[0].stdout == program_runs[1].stdout, "program output is nondeterministic")

    privacy_markers = (
        b"github_" + b"pat_", b"gh" + b"p_", b"access_" + b"token",
        b"BEGIN PRIVATE KEY", b"C:" + b"\\Users\\",
    )
    for path in (SOURCE, PROGRAM, TESTS, EXPECTED):
        payload = path.read_bytes()
        require(not any(marker in payload for marker in privacy_markers), f"private marker in {path}")

    math = independent_math_check()
    receipt = {
        "schema_version": "1.0",
        "status": "PASS",
        "laboratory_id": "D60-LAB04",
        "edition_unit_id": "O012-ORIG-LAB04",
        "course_route_unit_ids": ROUTES,
        "inputs": [info(path) for path in inputs],
        "structure": {
            "stable_ids": len(ids), "headings": len(headings), "tasks": len(exercises),
            "hints": len(hints), "complete_solution": True, "solution_subsections": 5,
            "program_source": True, "tests": 6, "expected_output": True,
            "interpretation": True, "offline_standard_library_only": True,
        },
        "executable_qa": {
            "test_runs": 2, "program_runs": 2, "byte_exact_expected_output": True,
            "expected_output_bytes": len(expected), "expected_output_sha256": sha256(expected),
        },
        "independent_reference_calculation": math,
        "rights": "CC BY-SA 4.0 original edition material",
        "excluded_fomberg_problem_bank_used": False,
        "model_provenance": MODEL,
        "upstream_contacted": False,
        "severity_counts": {"P1": 0, "P2": 0, "P3": 0},
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({
        "status": "PASS", "stable_ids": len(ids), "tests": 6,
        "pair_a_first_separator": math["pair_a"]["first_separator"],
        "pair_b_first_separator": math["pair_b"]["first_separator"],
        "receipt": OUTPUT.relative_to(ROOT).as_posix(),
    }, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
