#!/usr/bin/env python3
"""Fail-closed source, mathematics, and executable QA for D60 Lab 2."""
from __future__ import annotations

import ast
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict, deque
from fractions import Fraction
from itertools import combinations
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source/id-ID/labs/computation-lab-002-chain-matrices-smith-normal-form.md"
PROGRAM = ROOT / "source/id-ID/labs/o012_d60_lab02_smith_normal_form.py"
TESTS = ROOT / "source/id-ID/labs/test_o012_d60_lab02_smith_normal_form.py"
EXPECTED = ROOT / "source/id-ID/labs/expected-output-lab02.txt"
TERMINOLOGY = ROOT / "00_control/TERMINOLOGY.csv"
PREDECESSOR_HTML = ROOT / (
    "output/html/roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-"
    "ca02-ca03-lab01/index.html"
)
OUTPUT = ROOT / "qa/computation-lab-002/STATIC_QA.json"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"

FACES = (
    (0, 1, 2),
    (0, 1, 3),
    (0, 2, 4),
    (0, 3, 5),
    (0, 4, 5),
    (1, 2, 5),
    (1, 3, 4),
    (1, 4, 5),
    (2, 3, 4),
    (2, 3, 5),
)


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


def matrix_product(left: list[list[int]], right: list[list[int]]) -> list[list[int]]:
    require(bool(left) and bool(right), "independent matrix product received empty input")
    require(len(left[0]) == len(right), "independent matrix dimensions do not match")
    return [
        [
            sum(left[row][index] * right[index][column] for index in range(len(right)))
            for column in range(len(right[0]))
        ]
        for row in range(len(left))
    ]


def determinant(matrix: list[list[int]]) -> int:
    size = len(matrix)
    require(all(len(row) == size for row in matrix), "minor is not square")
    if size == 0:
        return 1
    work = [[Fraction(value) for value in row] for row in matrix]
    sign = 1
    result = Fraction(1)
    for column in range(size):
        pivot = next((row for row in range(column, size) if work[row][column]), None)
        if pivot is None:
            return 0
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            sign *= -1
        value = work[column][column]
        result *= value
        for index in range(column, size):
            work[column][index] /= value
        for row in range(column + 1, size):
            multiple = work[row][column]
            for index in range(column, size):
                work[row][index] -= multiple * work[column][index]
    require(result.denominator == 1, "integer determinant became nonintegral")
    return sign * result.numerator


def rank_mod2(matrix: list[list[int]]) -> int:
    work = [[value % 2 for value in row] for row in matrix]
    rows = len(work)
    columns = len(work[0]) if work else 0
    pivot_row = 0
    for column in range(columns):
        pivot = next((row for row in range(pivot_row, rows) if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        for row in range(rows):
            if row != pivot_row and work[row][column]:
                work[row] = [a ^ b for a, b in zip(work[row], work[pivot_row], strict=True)]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def boundary_coefficient(face: tuple[int, int, int], edge: tuple[int, int]) -> int:
    for deleted in range(3):
        if face[:deleted] + face[deleted + 1 :] == edge:
            return -1 if deleted % 2 else 1
    raise RuntimeError("independent fixture edge is not a face")


def independent_math_check() -> dict[str, object]:
    vertices = tuple(range(6))
    edges = tuple(combinations(vertices, 2))
    edge_index = {edge: index for index, edge in enumerate(edges)}
    d1 = [[0 for _ in edges] for _ in vertices]
    for column, (source, target) in enumerate(edges):
        d1[source][column] = -1
        d1[target][column] = 1
    d2 = [[0 for _ in FACES] for _ in edges]
    for column, face in enumerate(FACES):
        for deleted in range(3):
            edge = face[:deleted] + face[deleted + 1 :]
            d2[edge_index[edge]][column] = -1 if deleted % 2 else 1
    require(all(value == 0 for row in matrix_product(d1, d2) for value in row), "independent chain condition failed")

    incidence = Counter(edge for face in FACES for edge in combinations(face, 2))
    require(len(incidence) == 15 and set(incidence.values()) == {2}, "closed-surface incidence failed")
    links: dict[int, list[int]] = {}
    for vertex in vertices:
        adjacency: dict[int, set[int]] = defaultdict(set)
        for face in FACES:
            if vertex in face:
                other = [value for value in face if value != vertex]
                adjacency[other[0]].add(other[1])
                adjacency[other[1]].add(other[0])
        require(len(adjacency) == 5 and all(len(value) == 2 for value in adjacency.values()), "vertex link is not 2-regular")
        start = min(adjacency)
        reached = {start}
        queue = deque([start])
        while queue:
            current = queue.popleft()
            for neighbour in adjacency[current]:
                if neighbour not in reached:
                    reached.add(neighbour)
                    queue.append(neighbour)
        require(reached == set(adjacency), "vertex link is disconnected")
        links[vertex] = sorted(reached)

    orientation_cycle = (0, 1, 3, 9, 5, 0)
    orientation_edges = ((0, 1), (0, 3), (3, 5), (2, 5), (1, 2))
    ratios = []
    for first, second, edge in zip(
        orientation_cycle[:-1], orientation_cycle[1:], orientation_edges, strict=True
    ):
        ratios.append(-boundary_coefficient(FACES[first], edge) * boundary_coefficient(FACES[second], edge))
    orientation_product = 1
    for ratio in ratios:
        orientation_product *= ratio
    require(orientation_product == -1, "nonorientability witness drift")

    d1_minor = [[d1[row][column] for column in (0, 1, 2, 3, 4)] for row in (0, 1, 2, 3, 4)]
    d2_minor9 = [[d2[row][column] for column in range(9)] for row in (0, 1, 2, 3, 5, 6, 7, 9, 10)]
    d2_minor10 = [[d2[row][column] for column in range(10)] for row in (0, 1, 2, 3, 5, 6, 7, 9, 10, 12)]
    require(determinant(d1_minor) == -1, "d1 rank/SNF witness drift")
    require(determinant(d2_minor9) == 1, "d2 ninth determinantal divisor witness drift")
    require(determinant(d2_minor10) == -2, "d2 maximal-minor witness drift")
    require(rank_mod2(d2) == 9, "d2 mod-2 rank drift")

    z = [0] * 15
    z[edge_index[(0, 1)]] = 1
    z[edge_index[(0, 4)]] = -1
    z[edge_index[(1, 4)]] = 1
    filling = (1, 1, 1, 1, -1, -1, -1, 1, 1, -1)
    require(
        all(
            value == 0
            for row in matrix_product(d1, [[value] for value in z])
            for value in row
        ),
        "z is not a cycle",
    )
    require(
        [row[0] for row in matrix_product(d2, [[value] for value in filling])] == [2 * value for value in z],
        "2z filling drift",
    )
    alpha_support = {(0, 1), (0, 2), (1, 3), (2, 4), (3, 4)}
    alpha = [1 if edge in alpha_support else 0 for edge in edges]
    require(
        all(sum(alpha[row] * d2[row][column] for row in range(15)) % 2 == 0 for column in range(10)),
        "mod-2 detector is not a cocycle",
    )
    require(sum(alpha[row] * z[row] for row in range(15)) % 2 == 1, "mod-2 detector misses z")

    sphere_faces = tuple(combinations(range(4), 3))
    sphere_edges = tuple(combinations(range(4), 2))
    sphere_edge_index = {edge: index for index, edge in enumerate(sphere_edges)}
    sphere_d1 = [[0 for _ in sphere_edges] for _ in range(4)]
    for column, (source, target) in enumerate(sphere_edges):
        sphere_d1[source][column] = -1
        sphere_d1[target][column] = 1
    sphere_d2 = [[0 for _ in sphere_faces] for _ in sphere_edges]
    for column, face in enumerate(sphere_faces):
        for deleted in range(3):
            edge = face[:deleted] + face[deleted + 1 :]
            sphere_d2[sphere_edge_index[edge]][column] = -1 if deleted % 2 else 1
    require(rank_mod2(sphere_d2) == 3, "sphere control d2 rank drift")

    return {
        "vertices": 6,
        "edges": 15,
        "faces": 10,
        "euler_characteristic": 1,
        "every_edge_has_two_faces": True,
        "vertex_links_are_connected_5_cycles": True,
        "orientation_constraint_product": orientation_product,
        "chain_condition": True,
        "rank_d1": 5,
        "rank_d2": 10,
        "rank_mod2_d2": 9,
        "d1_unit_minor": -1,
        "d2_unit_9_minor": 1,
        "d2_maximal_minor": -2,
        "smith_d1_nonzero": [1, 1, 1, 1, 1],
        "smith_d2": [1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
        "homology": {"H0": "Z", "H1": "Z/2", "H2": "0"},
        "torsion_witness": {
            "z_is_cycle": True,
            "two_z_is_boundary": True,
            "mod2_cocycle_annihilates_boundaries": True,
            "mod2_cocycle_detects_z": True,
        },
        "sphere_control_homology": {"H0": "Z", "H1": "0", "H2": "Z"},
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
    for path in (SOURCE, PROGRAM, TESTS, EXPECTED, TERMINOLOGY, PREDECESSOR_HTML):
        require(path.is_file(), f"missing input: {path}")
    for path in (SOURCE, PROGRAM, TESTS, EXPECTED):
        raw = path.read_bytes()
        require(raw and b"\r" not in raw and raw.endswith(b"\n"), f"non-LF or empty input: {path}")
        raw.decode("utf-8", errors="strict")

    source = SOURCE.read_text(encoding="utf-8")
    require(source.startswith("---\n") and 'edition_unit_id: "O012-ORIG-LAB02"' in source, "front matter drift")
    require('course_route_unit_ids: ["D60-R08"]' in source, "route mapping drift")
    require('license: "CC BY-SA 4.0"' in source and MODEL in source, "rights/model disclosure missing")
    ids = re.findall(r"#(o012-d60-lab02(?:-[a-z0-9]+)*)\b", source)
    require(len(ids) == len(set(ids)) == 25, "stable-ID inventory is not 25 unique IDs")
    headings = re.findall(r"(?m)^#{1,2}\s+.+?\s+\{#(o012-d60-lab02(?:-[a-z0-9]+)*)\}\s*$", source)
    require(len(headings) == 18 and len(set(headings)) == 18, "heading inventory drift")
    exercises = re.findall(r"(?m)^::: \{\.exercise #(o012-d60-lab02-task-[0-9]{3})\}$", source)
    hints = re.findall(r"(?m)^::: \{\.hint #(o012-d60-lab02-hint)\}$", source)
    require(len(exercises) == len(set(exercises)) == 6, "task inventory drift")
    require(hints == ["o012-d60-lab02-hint"], "hint inventory drift")
    for marker in (
        "O012_LAB02_INCLUDE_PROGRAM",
        "O012_LAB02_INCLUDE_TESTS",
        "O012_LAB02_INCLUDE_EXPECTED",
    ):
        require(source.count(marker) == 1, f"include marker drift: {marker}")
    prerequisite_targets = sorted(set(re.findall(r"\]\(#([^)]+)\)", source)))
    predecessor = PREDECESSOR_HTML.read_text(encoding="utf-8")
    require(len(prerequisite_targets) == 8, "prerequisite-target census drift")
    for target in prerequisite_targets:
        require(f'id="{target}"' in predecessor, f"prerequisite target missing from predecessor: {target}")
    source_lower = source.lower()
    for required in (
        "materi asli edisi",
        "tidak menyiratkan",
        "dukungan atau pengesahan",
        "solusi lengkap",
        "kosiklus modulo $2$",
    ):
        require(required in source_lower, f"required semantic witness missing: {required}")

    terms = TERMINOLOGY.read_text(encoding="utf-8")
    for term_id in range(493, 503):
        require(f'O012-TERM-{term_id:04d}' in terms, f"terminology row missing: {term_id}")

    program_tree = ast.parse(PROGRAM.read_text(encoding="utf-8"), str(PROGRAM))
    tests_tree = ast.parse(TESTS.read_text(encoding="utf-8"), str(TESTS))
    imports = {
        node.names[0].name.split(".")[0]
        for tree in (program_tree, tests_tree)
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
    } | {
        (node.module or "").split(".")[0]
        for tree in (program_tree, tests_tree)
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom)
    }
    require(not (imports & {"numpy", "scipy", "sympy", "sage", "requests"}), "non-standard dependency detected")
    program_text = PROGRAM.read_text(encoding="utf-8")
    require(not any(token in program_text for token in ("socket", "urlopen", "subprocess", "random", "time.sleep")), "network/nondeterminism token in program")

    test_runs = [run([sys.executable, "-B", str(TESTS)]) for _ in range(2)]
    for result in test_runs:
        require(result.returncode == 0 and result.stdout == b"", "test suite failed or wrote stdout")
        require(b"Ran 6 tests" in result.stderr and result.stderr.rstrip().endswith(b"OK"), "test census/result drift")
    program_runs = [run([sys.executable, "-B", str(PROGRAM)]) for _ in range(2)]
    expected = EXPECTED.read_bytes()
    for result in program_runs:
        require(result.returncode == 0 and result.stderr == b"", "program failed or wrote stderr")
        require(result.stdout == expected, "program stdout differs from frozen expected output")
    require(program_runs[0].stdout == program_runs[1].stdout, "program output is nondeterministic")

    privacy_markers = (
        b"github_" + b"pat_",
        b"gh" + b"p_",
        b"access_" + b"token",
        b"BEGIN PRIVATE KEY",
        b"C:" + b"\\Users\\",
    )
    for path in (SOURCE, PROGRAM, TESTS, EXPECTED):
        payload = path.read_bytes()
        require(not any(marker in payload for marker in privacy_markers), f"private marker in {path}")

    math = independent_math_check()
    receipt = {
        "schema_version": "1.0",
        "status": "PASS",
        "laboratory_id": "D60-LAB02",
        "edition_unit_id": "O012-ORIG-LAB02",
        "course_route_unit_ids": ["D60-R08"],
        "inputs": [info(path) for path in (SOURCE, PROGRAM, TESTS, EXPECTED, TERMINOLOGY, PREDECESSOR_HTML)],
        "structure": {
            "stable_ids": len(ids),
            "headings": len(headings),
            "tasks": len(exercises),
            "hints": len(hints),
            "complete_solution": True,
            "program_source": True,
            "tests": 6,
            "expected_output": True,
            "interpretation": True,
            "offline_standard_library_only": True,
        },
        "executable_qa": {
            "test_runs": 2,
            "program_runs": 2,
            "byte_exact_expected_output": True,
            "expected_output_bytes": len(expected),
            "expected_output_sha256": sha256(expected),
        },
        "independent_reference_calculation": math,
        "rights": "CC BY-SA 4.0 original edition material",
        "excluded_fomberg_problem_bank_used": False,
        "model_provenance": MODEL,
        "upstream_contacted": False,
        "severity_counts": {"P1": 0, "P2": 0, "P3": 0},
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps({
        "status": "PASS",
        "stable_ids": len(ids),
        "tests": 6,
        "homology": math["homology"],
        "receipt": OUTPUT.relative_to(ROOT).as_posix(),
    }, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
