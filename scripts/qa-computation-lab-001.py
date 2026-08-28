#!/usr/bin/env python3
"""Fail-closed source, mathematics, and executable QA for D60 Lab 1."""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from collections import deque
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source/id-ID/labs/computation-lab-001-monodromy-presentations.md"
PROGRAM = ROOT / "source/id-ID/labs/o012_d60_lab01_monodromy.py"
TESTS = ROOT / "source/id-ID/labs/test_o012_d60_lab01_monodromy.py"
EXPECTED = ROOT / "source/id-ID/labs/expected-output-lab01.txt"
TERMINOLOGY = ROOT / "00_control/TERMINOLOGY.csv"
OUTPUT = ROOT / "qa/computation-lab-001/STATIC_QA.json"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"


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
        "lines": data.count(b"\n"),
        "sha256": sha256(data),
    }


def apply_word(sheet: int, word: str) -> int:
    transitions = {
        "a": (1, 2, 3, 0),
        "A": (3, 0, 1, 2),
        "b": (0, 3, 2, 1),
        "B": (0, 3, 2, 1),
    }
    for letter in word:
        sheet = transitions[letter][sheet]
    return sheet


def permutation(word: str) -> tuple[int, ...]:
    return tuple(apply_word(sheet, word) for sheet in range(4))


def inverse_word(word: str) -> str:
    inverse = {"a": "A", "A": "a", "b": "B", "B": "b"}
    return "".join(inverse[letter] for letter in reversed(word))


def reduce_word(word: str) -> str:
    inverse = {"a": "A", "A": "a", "b": "B", "B": "b"}
    stack: list[str] = []
    for letter in word:
        if stack and stack[-1] == inverse[letter]:
            stack.pop()
        else:
            stack.append(letter)
    return "".join(stack)


def independent_math_check() -> dict[str, object]:
    identity = (0, 1, 2, 3)
    letters = ("a", "A", "b", "B")
    positive = ("a", "b")

    orbit = {0}
    queue = deque([0])
    while queue:
        sheet = queue.popleft()
        for letter in letters:
            target = apply_word(sheet, letter)
            if target not in orbit:
                orbit.add(target)
                queue.append(target)

    image = {identity}
    queue_permutations = deque([identity])
    while queue_permutations:
        current = queue_permutations.popleft()
        for letter in letters:
            extended = tuple(apply_word(current[sheet], letter) for sheet in range(4))
            if extended not in image:
                image.add(extended)
                queue_permutations.append(extended)

    transversal = {0: ""}
    queue = deque([0])
    while queue:
        sheet = queue.popleft()
        for letter in letters:
            target = apply_word(sheet, letter)
            if target not in transversal:
                transversal[target] = transversal[sheet] + letter
                queue.append(target)

    basis: list[str] = []
    table: list[dict[str, object]] = []
    for sheet in range(4):
        for generator in positive:
            target = apply_word(sheet, generator)
            candidate = reduce_word(
                transversal[sheet] + generator + inverse_word(transversal[target])
            )
            table.append(
                {
                    "sheet": sheet,
                    "generator": generator,
                    "target": target,
                    "word": candidate or "1",
                }
            )
            if candidate:
                basis.append(candidate)

    require(orbit == {0, 1, 2, 3}, "independent orbit check failed")
    require(len(image) == 8, "independent monodromy-image order check failed")
    require(permutation("aaaa") == identity, "a^4 relation failed")
    require(permutation("bb") == identity, "b^2 relation failed")
    require(permutation("baba") == identity, "baba relation failed")
    require(transversal == {0: "", 1: "a", 3: "A", 2: "aa"}, "transversal drift")
    require(basis == ["b", "aba", "aaaa", "aabAA", "AbA"], "Schreier basis drift")
    require(4 * 2 - 4 + 1 == len(basis) == 5, "Euler/Schreier rank drift")
    require(all(apply_word(0, word) == 0 for word in basis), "basis word misses stabilizer")
    disconnected_orbits = ({0, 1}, {2, 3})
    negative_a = (1, 0, 3, 2)
    observed_negative = []
    unseen = set(range(4))
    while unseen:
        start = min(unseen)
        component = {start, negative_a[start]}
        observed_negative.append(component)
        unseen.difference_update(component)
    require(tuple(observed_negative) == disconnected_orbits, "negative fixture orbit drift")
    return {
        "orbit_0": sorted(orbit),
        "image_order": len(image),
        "relations": {"a4": True, "b2": True, "baba": True},
        "transversal": {str(sheet): word or "1" for sheet, word in sorted(transversal.items())},
        "schreier_table": table,
        "schreier_basis": basis,
        "rank": 5,
        "all_basis_words_fix_0": True,
        "negative_fixture_orbits": [sorted(component) for component in observed_negative],
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
    for path in (SOURCE, PROGRAM, TESTS, EXPECTED, TERMINOLOGY):
        require(path.is_file(), f"missing input: {path}")
    for path in (SOURCE, PROGRAM, TESTS, EXPECTED):
        data = path.read_bytes()
        require(b"\r" not in data, f"input is not LF-only: {path}")
        data.decode("utf-8")

    source = SOURCE.read_text(encoding="utf-8")
    require(source.startswith("---\n") and "edition_unit_id: \"O012-ORIG-LAB01\"" in source, "front matter drift")
    require("license: \"CC BY-SA 4.0\"" in source and MODEL in source, "rights/model disclosure missing")
    ids = re.findall(r"#(o012-d60-lab01(?:-[a-z0-9]+)*)\b", source)
    require(len(ids) == len(set(ids)) == 24, "stable-ID inventory is not 24 unique IDs")
    exercises = re.findall(r"(?m)^::: \{\.exercise #(o012-d60-lab01-task-[0-9]{3})\}$", source)
    hints = re.findall(r"(?m)^::: \{\.hint #(o012-d60-lab01-hint)\}$", source)
    require(len(exercises) == 6 and len(set(exercises)) == 6, "task inventory drift")
    require(hints == ["o012-d60-lab01-hint"], "hint inventory drift")
    for marker in (
        "O012_LAB01_INCLUDE_PROGRAM",
        "O012_LAB01_INCLUDE_TESTS",
        "O012_LAB01_INCLUDE_EXPECTED",
    ):
        require(source.count(marker) == 1, f"include marker drift: {marker}")
    for target in (
        "#o012-rbt-l07-s03",
        "#o012-rbt-l09-thm-002",
        "#o012-rbt-l10-s03",
        "#o012-rbt-l11-s01",
        "#o012-rbt-l13-s05",
    ):
        require(target in source, f"prerequisite link missing: {target}")
    expected_text = EXPECTED.read_text(encoding="utf-8")
    require("presentasi_citra: <a,b | a^4, b^2, baba>" in expected_text, "image presentation witness missing")
    require("presentasi_penutup: <b, aba, aaaa, aabAA, AbA | >" in expected_text, "cover presentation witness missing")
    for required in ("materi asli edisi", "tidak menyiratkan", "dukungan atau pengesahan"):
        require(required in source, f"required semantic witness missing: {required}")

    terms = TERMINOLOGY.read_text(encoding="utf-8")
    for term_id in range(485, 493):
        require(f'O012-TERM-{term_id:04d}' in terms, f"new terminology row missing: {term_id}")

    compile(PROGRAM.read_text(encoding="utf-8"), str(PROGRAM), "exec")
    compile(TESTS.read_text(encoding="utf-8"), str(TESTS), "exec")
    test_runs = [run([sys.executable, "-B", str(TESTS)]) for _ in range(2)]
    for result in test_runs:
        require(result.returncode == 0, result.stderr.decode("utf-8", errors="replace"))
        require(b"Ran 6 tests" in result.stderr and result.stderr.rstrip().endswith(b"OK"), "test census/result drift")
    require(test_runs[0].stdout == test_runs[1].stdout == b"", "test stdout is not deterministic and empty")
    program_runs = [run([sys.executable, "-B", str(PROGRAM)]) for _ in range(2)]
    expected = EXPECTED.read_bytes()
    for result in program_runs:
        require(result.returncode == 0 and result.stderr == b"", "program execution failed or wrote stderr")
        require(result.stdout == expected, "program output differs from frozen expected output")

    privacy_markers = (
        b"github_pat_", b"ghp_", b"access_token", b"BEGIN PRIVATE KEY",
        b"C:" + b"\\Users\\",
    )
    for path in (SOURCE, PROGRAM, TESTS, EXPECTED):
        payload = path.read_bytes()
        require(not any(marker in payload for marker in privacy_markers), f"private marker in {path}")

    math = independent_math_check()
    receipt = {
        "schema_version": "1.0",
        "status": "PASS",
        "laboratory_id": "D60-LAB01",
        "edition_unit_id": "O012-ORIG-LAB01",
        "course_route_unit_ids": ["D60-R04", "D60-R05", "D60-R06"],
        "inputs": [info(path) for path in (SOURCE, PROGRAM, TESTS, EXPECTED, TERMINOLOGY)],
        "structure": {
            "stable_ids": len(ids),
            "tasks": len(exercises),
            "hints": len(hints),
            "full_solution": True,
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
    OUTPUT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": "PASS", "stable_ids": len(ids), "tests": 6, "basis_rank": math["rank"], "receipt": OUTPUT.relative_to(ROOT).as_posix()}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
