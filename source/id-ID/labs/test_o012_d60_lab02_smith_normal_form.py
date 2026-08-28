#!/usr/bin/env python3
"""Uji deterministik untuk O012-D60-LAB02.

SPDX-License-Identifier: CC-BY-SA-4.0
"""
from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

from o012_d60_lab02_smith_normal_form import (
    RP2_FACES,
    S2_FACES,
    SurfaceComplex,
    analyse_surface,
    build_surface,
    determinant_bareiss,
    edge_incidence_counts,
    freeze,
    homology_invariants,
    identity,
    is_orientable_closed_surface,
    is_zero_matrix,
    matmul,
    rp2_torsion_witness,
    shape,
    simplex_boundary_matrix,
    smith_certificate,
    smith_normal_form,
    SmithResult,
    transpose,
    vertex_links_are_cycles,
)


HERE = Path(__file__).resolve().parent
PROGRAM = HERE / "o012_d60_lab02_smith_normal_form.py"
EXPECTED = HERE / "expected-output-lab02.txt"


def signed_permutation(order: tuple[int, ...], signs: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    if sorted(order) != list(range(len(order))) or len(signs) != len(order):
        raise ValueError("data permutasi bertanda tidak sah")
    if any(sign not in (-1, 1) for sign in signs):
        raise ValueError("tanda basis harus +1 atau -1")
    rows = [[0 for _ in order] for _ in order]
    for row, column in enumerate(order):
        rows[row][column] = signs[row]
    return freeze(rows)


class Lab02Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.surface = build_surface(RP2_FACES)

    def test_closed_nonorientable_surface_fixture(self) -> None:
        self.assertEqual(len(self.surface.vertices), 6)
        self.assertEqual(len(self.surface.edges), 15)
        self.assertEqual(len(self.surface.faces), 10)
        self.assertEqual(6 - 15 + 10, 1)
        self.assertEqual(set(edge_incidence_counts(RP2_FACES).values()), {2})
        self.assertTrue(vertex_links_are_cycles(RP2_FACES))
        self.assertFalse(is_orientable_closed_surface(RP2_FACES))
        with self.assertRaisesRegex(ValueError, "dua muka"):
            is_orientable_closed_surface(RP2_FACES[:-1])
        with self.assertRaisesRegex(ValueError, "duplikat"):
            build_surface(RP2_FACES + (RP2_FACES[0],))
        with self.assertRaisesRegex(ValueError, "terurut naik secara ketat"):
            build_surface(((0, 0, 1),))
        with self.assertRaisesRegex(ValueError, "terurut naik secara ketat"):
            simplex_boundary_matrix((), ((2, 1),))

    def test_boundary_matrices_and_chain_condition(self) -> None:
        self.assertEqual(shape(self.surface.d1), (6, 15))
        self.assertEqual(shape(self.surface.d2), (15, 10))
        edge_index = {edge: index for index, edge in enumerate(self.surface.edges)}
        self.assertEqual(
            tuple(self.surface.d1[row][edge_index[(0, 1)]] for row in range(6)),
            (-1, 1, 0, 0, 0, 0),
        )
        first_face_boundary = tuple(self.surface.d2[row][0] for row in range(15))
        self.assertEqual(first_face_boundary[edge_index[(0, 1)]], 1)
        self.assertEqual(first_face_boundary[edge_index[(0, 2)]], -1)
        self.assertEqual(first_face_boundary[edge_index[(1, 2)]], 1)
        self.assertTrue(is_zero_matrix(matmul(self.surface.d1, self.surface.d2)))

        damaged = [list(row) for row in self.surface.d2]
        damaged[edge_index[(0, 1)]][0] += 1
        self.assertFalse(is_zero_matrix(matmul(self.surface.d1, freeze(damaged))))

    def test_smith_certificates_and_invariant_factors(self) -> None:
        d1 = smith_normal_form(self.surface.d1)
        d2 = smith_normal_form(self.surface.d2)
        self.assertEqual(d1.diagonal, (1, 1, 1, 1, 1))
        self.assertEqual(d2.diagonal, (1, 1, 1, 1, 1, 1, 1, 1, 1, 2))
        self.assertTrue(smith_certificate(self.surface.d1, d1))
        self.assertTrue(smith_certificate(self.surface.d2, d2))
        self.assertEqual(abs(determinant_bareiss(d1.left)), 1)
        self.assertEqual(abs(determinant_bareiss(d1.right)), 1)
        self.assertEqual(abs(determinant_bareiss(d2.left)), 1)
        self.assertEqual(abs(determinant_bareiss(d2.right)), 1)

        rank_one = freeze([[2, 4], [4, 8]])
        rank_one_smith = smith_normal_form(rank_one)
        self.assertEqual(rank_one_smith.diagonal, (2,))
        self.assertTrue(smith_certificate(rank_one, rank_one_smith))
        malformed = SmithResult(
            diagonal=(1,),
            transformed=((1, 0), (0, 0)),
            left=((1, 0), (0,)),
            right=((1, 0), (0, 1)),
        )
        self.assertFalse(smith_certificate(((1, 0), (0, 0)), malformed))

    def test_rp2_homology_and_explicit_torsion_cycle(self) -> None:
        analysis = analyse_surface(RP2_FACES)
        self.assertEqual(analysis["homology"], ((1, ()), (0, (2,)), (0, ())))
        witness = rp2_torsion_witness(self.surface)
        self.assertTrue(witness["is_cycle"])
        self.assertTrue(witness["twice_is_boundary"])
        self.assertTrue(witness["mod2_annihilates_boundaries"])
        self.assertTrue(witness["mod2_detects_cycle"])
        self.assertTrue(witness["not_boundary"])
        self.assertEqual(
            tuple(
                self.surface.edges[index]
                for index, coefficient in enumerate(witness["mod2_cocycle"])
                if coefficient
            ),
            ((0, 1), (0, 2), (1, 3), (2, 4), (3, 4)),
        )
        self.assertEqual(
            witness["filling"],
            (1, 1, 1, 1, -1, -1, -1, 1, 1, -1),
        )
        reordered_surface = build_surface(tuple(reversed(RP2_FACES)))
        reordered_witness = rp2_torsion_witness(reordered_surface)
        self.assertTrue(reordered_witness["twice_is_boundary"])
        self.assertTrue(reordered_witness["not_boundary"])
        zero_d2 = tuple(tuple(0 for _ in reordered_surface.faces) for _ in reordered_surface.edges)
        altered_surface = SurfaceComplex(
            reordered_surface.vertices,
            reordered_surface.edges,
            reordered_surface.faces,
            reordered_surface.d1,
            zero_d2,
        )
        altered_witness = rp2_torsion_witness(altered_surface)
        self.assertFalse(altered_witness["twice_is_boundary"])
        self.assertTrue(altered_witness["not_boundary"])

    def test_signed_basis_invariance_and_sphere_control(self) -> None:
        edge_order = tuple(reversed(range(15)))
        edge_signs = tuple(-1 if index % 2 else 1 for index in range(15))
        face_order = (3, 1, 9, 0, 7, 5, 2, 8, 4, 6)
        face_signs = tuple(-1 if index in (0, 4, 7) else 1 for index in range(10))
        edge_change = signed_permutation(edge_order, edge_signs)
        face_change = signed_permutation(face_order, face_signs)
        changed_d2 = matmul(matmul(edge_change, self.surface.d2), face_change)
        changed_d1 = matmul(self.surface.d1, transpose(edge_change))
        self.assertEqual(matmul(edge_change, transpose(edge_change)), identity(15))
        self.assertTrue(is_zero_matrix(matmul(changed_d1, changed_d2)))
        d1 = smith_normal_form(changed_d1)
        d2 = smith_normal_form(changed_d2)
        self.assertEqual(d1.diagonal, (1, 1, 1, 1, 1))
        self.assertEqual(d2.diagonal, (1, 1, 1, 1, 1, 1, 1, 1, 1, 2))
        self.assertEqual(
            homology_invariants(15, d1, d2),
            (0, (2,)),
        )

        sphere = analyse_surface(S2_FACES)
        self.assertTrue(sphere["orientable"])
        self.assertEqual(sphere["homology"], ((1, ()), (0, ()), (1, ())))

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
