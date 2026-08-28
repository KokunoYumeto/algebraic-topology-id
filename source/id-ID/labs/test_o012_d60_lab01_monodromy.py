#!/usr/bin/env python3
"""Uji deterministik untuk O012-D60-LAB01.

SPDX-License-Identifier: CC-BY-SA-4.0
"""
from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

from o012_d60_lab01_monodromy import (
    CoveringAction,
    build_lab_action,
    inverse_word,
    reduce_word,
)


HERE = Path(__file__).resolve().parent
PROGRAM = HERE / "o012_d60_lab01_monodromy.py"
EXPECTED = HERE / "expected-output-lab01.txt"


class Lab01Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.action = build_lab_action()

    def test_inverse_transitions_and_free_reduction(self) -> None:
        for sheet in range(self.action.degree):
            self.assertEqual(self.action.act(sheet, "aA"), sheet)
            self.assertEqual(self.action.act(sheet, "Aa"), sheet)
            self.assertEqual(self.action.act(sheet, "bB"), sheet)
            self.assertEqual(self.action.act(sheet, "Bb"), sheet)
        self.assertEqual(inverse_word("abA"), "aBA")
        self.assertEqual(reduce_word("abBAaA"), "")

    def test_connected_orbit_image_and_relations(self) -> None:
        identity = tuple(range(4))
        self.assertEqual(self.action.orbit(0), (0, 1, 2, 3))
        self.assertEqual(len(self.action.image()), 8)
        self.assertEqual(self.action.permutation("aaaa"), identity)
        self.assertEqual(self.action.permutation("bb"), identity)
        self.assertEqual(self.action.permutation("baba"), identity)

    def test_transversal_basis_and_rank(self) -> None:
        self.assertEqual(
            self.action.schreier_transversal(0),
            {0: "", 1: "a", 3: "A", 2: "aa"},
        )
        basis = ("b", "aba", "aaaa", "aabAA", "AbA")
        self.assertEqual(self.action.schreier_basis(0), basis)
        self.assertEqual(self.action.graph_rank(), 5)
        self.assertTrue(all(self.action.act(0, word) == 0 for word in basis))

    def test_disconnected_fixture(self) -> None:
        disconnected = CoveringAction(
            {
                "a": (1, 0, 3, 2),
                "b": (0, 1, 2, 3),
            }
        )
        self.assertEqual(disconnected.orbits(), ((0, 1), (2, 3)))
        with self.assertRaisesRegex(ValueError, "transitif"):
            disconnected.schreier_basis(0)

    def test_invalid_permutation_and_word_are_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "bukan permutasi"):
            CoveringAction({"a": (0, 0), "b": (0, 1)})
        with self.assertRaisesRegex(ValueError, "huruf kata tidak sah"):
            self.action.act(0, "ac")

    def test_cli_matches_frozen_expected_output(self) -> None:
        process = subprocess.run(
            [sys.executable, "-B", str(PROGRAM)],
            cwd=HERE,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.assertEqual(process.stderr, b"")
        self.assertEqual(process.stdout, EXPECTED.read_bytes())


if __name__ == "__main__":
    unittest.main(verbosity=2)
