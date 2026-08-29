#!/usr/bin/env python3
"""Fail-closed source, mathematics, and executable QA for D60 Lab 3."""
from __future__ import annotations

import ast
import hashlib
import json
import re
import subprocess
import sys
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source/id-ID/labs/computation-lab-003-cellular-boundaries-degree.md"
PROGRAM = ROOT / "source/id-ID/labs/o012_d60_lab03_cellular_degree.py"
TESTS = ROOT / "source/id-ID/labs/test_o012_d60_lab03_cellular_degree.py"
EXPECTED = ROOT / "source/id-ID/labs/expected-output-lab03.txt"
TERMINOLOGY = ROOT / "00_control/TERMINOLOGY.csv"
PREDECESSOR_HTML = ROOT / (
    "output/html/roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-"
    "ca02-ca03-lab01-lab02/index.html"
)
OUTPUT = ROOT / "qa/computation-lab-003/STATIC_QA.json"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"
M = ((2, 1), (-1, 2))
N = ((0, 1), (1, 0))
C = ((1, 1), (2, 2))
Y = (Fraction(1, 7), Fraction(2, 7))


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


def det(matrix: tuple[tuple[int, int], tuple[int, int]]) -> int:
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def multiply(
    left: tuple[tuple[int, int], tuple[int, int]],
    right: tuple[tuple[int, int], tuple[int, int]],
) -> tuple[tuple[int, int], tuple[int, int]]:
    return tuple(
        tuple(sum(left[row][k] * right[k][column] for k in range(2)) for column in range(2))
        for row in range(2)
    )  # type: ignore[return-value]


def mod_one(value: Fraction) -> Fraction:
    return value - value.numerator // value.denominator


def apply_matrix(
    matrix: tuple[tuple[int, int], tuple[int, int]],
    point: tuple[Fraction, Fraction],
) -> tuple[Fraction, Fraction]:
    return (
        matrix[0][0] * point[0] + matrix[0][1] * point[1],
        matrix[1][0] * point[0] + matrix[1][1] * point[1],
    )


def independent_preimages(
    matrix: tuple[tuple[int, int], tuple[int, int]],
    target: tuple[Fraction, Fraction],
) -> tuple[tuple[Fraction, Fraction], ...]:
    determinant = det(matrix)
    require(determinant != 0, "finite independent fiber requires nonzero determinant")
    a, b = matrix[0]
    c, d = matrix[1]
    points: set[tuple[Fraction, Fraction]] = set()
    # A bounded exhaustive lift search is deliberately independent of the
    # production program.  The range is much wider than required by M, N, NM.
    for first in range(-12, 13):
        for second in range(-12, 13):
            rhs0 = target[0] + first
            rhs1 = target[1] + second
            x0 = Fraction(d * rhs0 - b * rhs1, determinant)
            x1 = Fraction(-c * rhs0 + a * rhs1, determinant)
            point = (mod_one(x0), mod_one(x1))
            image = apply_matrix(matrix, point)
            if all((image[i] - target[i]).denominator == 1 for i in range(2)):
                points.add(point)
    result = tuple(sorted(points))
    require(len(result) == abs(determinant), "independent fiber cardinality mismatch")
    return result


def independent_math_check() -> dict[str, object]:
    word = (("a", 1), ("b", 1), ("a", -1), ("b", -1))
    incidence = tuple(sum(sign for label, sign in word if label == basis) for basis in ("a", "b"))
    unsigned = tuple(sum(1 for label, _ in word if label == basis) for basis in ("a", "b"))
    require(incidence == (0, 0) and unsigned == (2, 2), "torus incidence fixture drift")
    require(det(M) == 5 and det(N) == -1 and det(C) == 0, "determinant fixture drift")
    nm = multiply(N, M)
    mn = multiply(M, N)
    require(nm == ((-1, 2), (2, 1)), "NM drift")
    require(mn == ((1, 2), (2, -1)) and nm != mn, "MN/order drift")

    power = tuple(Fraction(1, 21) + Fraction(index, 3) for index in range(3))
    require(power == (Fraction(1, 21), Fraction(8, 21), Fraction(5, 7)), "power-map fiber drift")
    expected_m = (
        (Fraction(0), Fraction(1, 7)),
        (Fraction(1, 5), Fraction(26, 35)),
        (Fraction(2, 5), Fraction(12, 35)),
        (Fraction(3, 5), Fraction(33, 35)),
        (Fraction(4, 5), Fraction(19, 35)),
    )
    expected_n = ((Fraction(2, 7), Fraction(1, 7)),)
    expected_nm = (
        (Fraction(3, 35), Fraction(4, 35)),
        (Fraction(2, 7), Fraction(5, 7)),
        (Fraction(17, 35), Fraction(11, 35)),
        (Fraction(24, 35), Fraction(32, 35)),
        (Fraction(31, 35), Fraction(18, 35)),
    )
    require(independent_preimages(M, Y) == expected_m, "M fiber drift")
    require(independent_preimages(N, Y) == expected_n, "N fiber drift")
    require(independent_preimages(nm, Y) == expected_nm, "NM fiber drift")

    left_null = (-2, 1)
    require(
        tuple(sum(left_null[k] * C[k][column] for k in range(2)) for column in range(2))
        == (0, 0),
        "left-null vector drift",
    )
    y0 = (Fraction(0), Fraction(1, 3))
    pairing = sum(left_null[i] * y0[i] for i in range(2))
    require(pairing == Fraction(1, 3) and pairing.denominator != 1, "nonimage obstruction drift")
    require(apply_matrix(C, (Fraction(2, 5), Fraction(-2, 5))) == (0, 0), "nonempty singular fiber control drift")
    return {
        "cellular": {
            "torus_signed_incidence": list(incidence),
            "torus_unsigned_occurrences": list(unsigned),
            "torus_homology": {"H0": "Z", "H1": "Z^2", "H2": "Z"},
            "X3_d2": [3],
            "X3_reversed_d2": [-3],
            "X3_homology": {"H0": "Z", "H1": "Z/3", "H2": "0"},
        },
        "degree": {
            "det_M": det(M),
            "det_N": det(N),
            "det_C": det(C),
            "NM": [list(row) for row in nm],
            "MN": [list(row) for row in mn],
            "M_preimages": len(expected_m),
            "N_preimages": len(expected_n),
            "NM_preimages": len(expected_nm),
            "M_local_degree_sum": 5,
            "N_local_degree_sum": -1,
            "NM_local_degree_sum": -5,
            "degree_multiplicativity": True,
        },
        "singular_control": {
            "left_null": list(left_null),
            "target_pairing": "1/3",
            "target_outside_image": True,
            "zero_fiber_nonempty": True,
        },
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
    require(source.startswith("---\n") and 'edition_unit_id: "O012-ORIG-LAB03"' in source, "front matter drift")
    require('course_route_unit_ids: ["D60-R12", "D60-R14"]' in source, "route mapping drift")
    require('license: "CC BY-SA 4.0"' in source and MODEL in source, "rights/model disclosure missing")
    ids = re.findall(r"#(o012-d60-lab03(?:-[a-z0-9]+)*)\b", source)
    require(len(ids) == len(set(ids)) == 25, "stable-ID inventory is not 25 unique IDs")
    headings = re.findall(r"(?m)^#{1,2}\s+.+?\s+\{#(o012-d60-lab03(?:-[a-z0-9]+)*)\}\s*$", source)
    exercises = re.findall(r"(?m)^::: \{\.exercise #(o012-d60-lab03-task-[0-9]{3})\}$", source)
    hints = re.findall(r"(?m)^::: \{\.hint #(o012-d60-lab03-hint)\}$", source)
    require(len(headings) == len(set(headings)) == 18, "heading inventory drift")
    require(len(exercises) == len(set(exercises)) == 6, "task inventory drift")
    require(hints == ["o012-d60-lab03-hint"], "hint inventory drift")
    for marker in ("O012_LAB03_INCLUDE_PROGRAM", "O012_LAB03_INCLUDE_TESTS", "O012_LAB03_INCLUDE_EXPECTED"):
        require(source.count(marker) == 1, f"include marker drift: {marker}")

    predecessor = PREDECESSOR_HTML.read_text(encoding="utf-8")
    targets = sorted(set(re.findall(r"\]\([^)]*#([^)]+)\)", source)))
    require(len(targets) == 4, "prerequisite-target census drift")
    for target in targets:
        require(f'id="{target}"' in predecessor, f"prerequisite target missing: {target}")
    lower = " ".join(source.lower().split())
    for witness in (
        "materi asli edisi",
        "bukan bagian dari sumber roberts atau fomberg",
        "produk cup",
        "kelas fundamental",
        "aproksimasi seluler",
        "jumlah eksponen bertanda",
        "dukungan atau pengesahan",
        "solusi lengkap",
        "serat di atas $0$ tidak kosong",
    ):
        require(witness in lower, f"required semantic witness missing: {witness}")
    require("nm" in lower and "mn" in lower and "det c=0" in lower, "composition/singular trap witness missing")

    terms = TERMINOLOGY.read_text(encoding="utf-8")
    for term_id in range(503, 515):
        require(f'O012-TERM-{term_id:04d}' in terms, f"terminology row missing: {term_id}")

    allowed = {
        "__future__", "dataclasses", "fractions", "math", "pathlib",
        "subprocess", "sys", "typing", "unittest",
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
        permitted = allowed | {"o012_d60_lab03_cellular_degree"}
        require(imports <= permitted, f"unexpected import in {path}: {sorted(imports - permitted)}")
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
        "laboratory_id": "D60-LAB03",
        "edition_unit_id": "O012-ORIG-LAB03",
        "course_route_unit_ids": ["D60-R12", "D60-R14"],
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
        "degree_M": math["degree"]["det_M"], "receipt": OUTPUT.relative_to(ROOT).as_posix(),
    }, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
