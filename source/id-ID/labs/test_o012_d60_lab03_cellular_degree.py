#!/usr/bin/env python3
"""Uji deterministik untuk O012-D60-LAB03.

SPDX-License-Identifier: CC-BY-SA-4.0
"""
from __future__ import annotations

import subprocess
import sys
import unittest
from fractions import Fraction
from pathlib import Path

from o012_d60_lab03_cellular_degree import (
    LEFT_NULL_C,
    MATRIX_C,
    MATRIX_M,
    MATRIX_N,
    REGULAR_TARGET,
    SINGULAR_TARGET,
    TORUS_BASIS,
    TORUS_WORD,
    X3_BASIS,
    X3_REVERSED_WORD,
    X3_WORD,
    determinant2,
    free_reduce,
    freeze_basis,
    freeze_matrix2,
    freeze_word,
    incidence_vector,
    matmul2,
    nonimage_certificate,
    one_column_homology,
    power_map_local_degrees,
    power_map_preimages,
    torus_local_degrees,
    torus_preimages,
    unsigned_occurrence_vector,
)


HERE = Path(__file__).resolve().parent
PROGRAM = HERE / "o012_d60_lab03_cellular_degree.py"
EXPECTED = HERE / "expected-output-lab03.txt"


class Lab03Tests(unittest.TestCase):
    def test_incidence_degrees_and_unsigned_control(self) -> None:
        self.assertEqual(free_reduce(TORUS_WORD, TORUS_BASIS), TORUS_WORD)
        self.assertEqual(incidence_vector(TORUS_WORD, TORUS_BASIS), (0, 0))
        self.assertEqual(unsigned_occurrence_vector(TORUS_WORD, TORUS_BASIS), (2, 2))
        self.assertEqual(incidence_vector(X3_WORD, X3_BASIS), (3,))
        self.assertEqual(incidence_vector(X3_REVERSED_WORD, X3_BASIS), (-3,))
        self.assertEqual(
            free_reduce((("a", 1), ("a", -1), ("b", 1)), TORUS_BASIS),
            (("b", 1),),
        )
        with self.assertRaisesRegex(ValueError, "unik"):
            freeze_basis(("a", "a"))
        with self.assertRaisesRegex(ValueError, "tidak berada"):
            freeze_word((("c", 1),), TORUS_BASIS)
        with self.assertRaisesRegex(ValueError, r"\+1 atau -1"):
            freeze_word((("a", 0),), TORUS_BASIS)
        with self.assertRaisesRegex(ValueError, r"\+1 atau -1"):
            freeze_word((("a", True),), TORUS_BASIS)

    def test_one_column_cellular_homology_and_orientation(self) -> None:
        torus = one_column_homology(incidence_vector(TORUS_WORD, TORUS_BASIS))
        self.assertEqual((torus.h0_free_rank, torus.h1_free_rank, torus.h1_torsion, torus.h2_free_rank), (1, 2, (), 1))
        x3 = one_column_homology(incidence_vector(X3_WORD, X3_BASIS))
        reversed_x3 = one_column_homology(
            incidence_vector(X3_REVERSED_WORD, X3_BASIS)
        )
        self.assertEqual((x3.h0_free_rank, x3.h1_free_rank, x3.h1_torsion, x3.h2_free_rank), (1, 0, (3,), 0))
        self.assertEqual(x3, reversed_x3)
        self.assertEqual(one_column_homology((1,)).h1_torsion, ())
        self.assertEqual(one_column_homology((0,)).h2_free_rank, 1)
        with self.assertRaisesRegex(ValueError, "sedikitnya satu"):
            one_column_homology(())
        with self.assertRaisesRegex(ValueError, "bilangan bulat"):
            one_column_homology((Fraction(3, 1),))

    def test_integer_torus_endomorphisms_and_induced_actions(self) -> None:
        self.assertEqual(freeze_matrix2(MATRIX_M), MATRIX_M)
        self.assertEqual(determinant2(MATRIX_M), 5)
        self.assertEqual(determinant2(MATRIX_N), -1)
        self.assertEqual(determinant2(MATRIX_C), 0)
        self.assertEqual(matmul2(MATRIX_N, MATRIX_M), ((-1, 2), (2, 1)))
        self.assertEqual(matmul2(MATRIX_M, MATRIX_N), ((1, 2), (2, -1)))
        self.assertNotEqual(matmul2(MATRIX_N, MATRIX_M), matmul2(MATRIX_M, MATRIX_N))
        self.assertEqual(
            determinant2(matmul2(MATRIX_N, MATRIX_M)),
            determinant2(MATRIX_N) * determinant2(MATRIX_M),
        )
        with self.assertRaisesRegex(ValueError, "2x2"):
            freeze_matrix2(((1, 0, 0), (0, 1, 0)))
        with self.assertRaisesRegex(ValueError, "bilangan bulat"):
            freeze_matrix2(((1, 0), (0, Fraction(1, 2))))
        with self.assertRaisesRegex(ValueError, "bilangan bulat"):
            freeze_matrix2(((1, 0), (0, True)))

    def test_exact_preimages_local_degrees_and_composition(self) -> None:
        self.assertEqual(
            power_map_preimages(3, Fraction(1, 7)),
            (Fraction(1, 21), Fraction(8, 21), Fraction(5, 7)),
        )
        self.assertEqual(power_map_local_degrees(3, Fraction(1, 7)), (1, 1, 1))
        self.assertEqual(
            power_map_preimages(-3, Fraction(1, 7)),
            (Fraction(2, 7), Fraction(13, 21), Fraction(20, 21)),
        )
        self.assertEqual(power_map_local_degrees(-3, Fraction(1, 7)), (-1, -1, -1))
        expected_m = (
            (Fraction(0), Fraction(1, 7)),
            (Fraction(1, 5), Fraction(26, 35)),
            (Fraction(2, 5), Fraction(12, 35)),
            (Fraction(3, 5), Fraction(33, 35)),
            (Fraction(4, 5), Fraction(19, 35)),
        )
        self.assertEqual(torus_preimages(MATRIX_M, REGULAR_TARGET), expected_m)
        self.assertEqual(torus_local_degrees(MATRIX_M, REGULAR_TARGET), (1,) * 5)
        self.assertEqual(sum(torus_local_degrees(MATRIX_M, REGULAR_TARGET)), 5)
        self.assertEqual(
            torus_preimages(MATRIX_N, REGULAR_TARGET),
            ((Fraction(2, 7), Fraction(1, 7)),),
        )
        self.assertEqual(torus_local_degrees(MATRIX_N, REGULAR_TARGET), (-1,))
        composite = matmul2(MATRIX_N, MATRIX_M)
        expected_composite = (
            (Fraction(3, 35), Fraction(4, 35)),
            (Fraction(2, 7), Fraction(5, 7)),
            (Fraction(17, 35), Fraction(11, 35)),
            (Fraction(24, 35), Fraction(32, 35)),
            (Fraction(31, 35), Fraction(18, 35)),
        )
        self.assertEqual(torus_preimages(composite, REGULAR_TARGET), expected_composite)
        self.assertEqual(
            tuple(
                (
                    composite[0][0] * point[0]
                    + composite[0][1] * point[1]
                    - REGULAR_TARGET[0],
                    composite[1][0] * point[0]
                    + composite[1][1] * point[1]
                    - REGULAR_TARGET[1],
                )
                for point in expected_composite
            ),
            ((0, 0), (1, 1), (0, 1), (1, 2), (0, 2)),
        )
        self.assertEqual(sum(torus_local_degrees(composite, REGULAR_TARGET)), -5)

    def test_singular_and_malformed_inputs_fail_closed(self) -> None:
        self.assertTrue(nonimage_certificate(MATRIX_C, SINGULAR_TARGET, LEFT_NULL_C))
        self.assertFalse(
            nonimage_certificate(MATRIX_C, (Fraction(0), Fraction(0)), LEFT_NULL_C)
        )
        parameter = Fraction(1, 7)
        zero_fiber_point = (parameter, -parameter)
        self.assertEqual(
            tuple(
                sum(MATRIX_C[row][column] * zero_fiber_point[column] for column in range(2))
                for row in range(2)
            ),
            (0, 0),
        )
        with self.assertRaisesRegex(ValueError, "singular"):
            torus_preimages(MATRIX_C, SINGULAR_TARGET)
        with self.assertRaisesRegex(ValueError, "kontrol singular"):
            torus_local_degrees(MATRIX_C, SINGULAR_TARGET)
        with self.assertRaisesRegex(ValueError, "bukan vektor null kiri"):
            nonimage_certificate(MATRIX_C, SINGULAR_TARGET, (1, 0))
        with self.assertRaisesRegex(ValueError, "hanya berlaku"):
            nonimage_certificate(MATRIX_M, REGULAR_TARGET, (1, 0))
        with self.assertRaisesRegex(ValueError, "Fraction eksak"):
            torus_preimages(MATRIX_M, (1 / 7, Fraction(2, 7)))
        with self.assertRaisesRegex(ValueError, "tidak hingga"):
            power_map_preimages(0, Fraction(0))
        self.assertEqual(power_map_preimages(0, Fraction(1, 7)), ())
        with self.assertRaisesRegex(ValueError, "bilangan bulat"):
            power_map_preimages(True, Fraction(1, 7))

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
