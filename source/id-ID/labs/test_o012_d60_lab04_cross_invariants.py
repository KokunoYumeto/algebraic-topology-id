#!/usr/bin/env python3
"""Enam uji deterministik untuk Laboratorium D60-04."""
from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

from o012_d60_lab04_cross_invariants import (
    AbelianGroup,
    CupRing,
    SpaceProfile,
    compare_profiles,
    exponent_sums,
    fixtures,
    free_reduce,
)


HERE = Path(__file__).resolve().parent
PROGRAM = HERE / "o012_d60_lab04_cross_invariants.py"
EXPECTED = HERE / "expected-output-lab04.txt"


class CrossInvariantLabTests(unittest.TestCase):
    def setUp(self) -> None:
        self.spaces = fixtures()

    def test_fixtures_and_malformed_ring_fail_closed(self) -> None:
        self.assertEqual(set(self.spaces), {"torus", "wedge_a", "cp2", "wedge_b"})
        for profile in self.spaces.values():
            profile.validate()
        with self.assertRaisesRegex(ValueError, "derajat produk cup"):
            CupRing((("1", 0), ("x", 1), ("u", 3)), (("x", "x", 1, "u"),)).validate()
        with self.assertRaisesRegex(ValueError, "basis kohomologi berulang"):
            CupRing((("1", 0), ("1", 0)), ()).validate()
        with self.assertRaisesRegex(ValueError, "unit eksplisit"):
            CupRing((("1", 0), ("x", 2)), (("1", "x", 2, "x"),)).validate()
        with self.assertRaisesRegex(ValueError, "basis tidak dikenal"):
            CupRing((("1", 0), ("x", 2)), (("x", "x", 1, "u"),)).validate()
        with self.assertRaisesRegex(ValueError, "berulang"):
            CupRing(
                (("1", 0), ("x", 2), ("u", 4)),
                (("x", "x", 1, "u"), ("x", "x", -1, "u")),
            ).validate()
        with self.assertRaisesRegex(ValueError, "koefisien"):
            CupRing((("1", 0), ("x", 2), ("u", 4)), (("x", "x", True, "u"),)).validate()
        with self.assertRaisesRegex(ValueError, "komutatif bergradasi"):
            CupRing(
                (("1", 0), ("x", 2), ("y", 2), ("u", 4)),
                (("x", "y", 1, "u"),),
            ).validate()
        with self.assertRaisesRegex(ValueError, "tidak asosiatif"):
            CupRing(
                (("1", 0), ("a", 2), ("b", 2), ("u", 4), ("v", 4), ("w", 6)),
                (
                    ("a", "a", 1, "u"),
                    ("a", "b", 1, "v"),
                    ("b", "a", 1, "v"),
                    ("u", "b", 1, "w"),
                    ("b", "u", 1, "w"),
                ),
            ).validate()
        for malformed in (
            lambda: AbelianGroup(True),
            lambda: AbelianGroup(0, (True,)),
            lambda: free_reduce((), True),
            lambda: CupRing((("1", 0), ("x", True)), ()).validate(),
        ):
            with self.assertRaises(ValueError):
                malformed()

        base = self.spaces["torus"]
        with self.assertRaisesRegex(ValueError, "metadata ruang"):
            SpaceProfile(
                base.slug, base.display_name, base.pi1_signature,
                base.pi1_abelianization, base.generator_count, base.relators,
                base.cells, "", base.ring,
            ).validate()
        with self.assertRaisesRegex(ValueError, "banyak generator"):
            SpaceProfile(
                base.slug, base.display_name, base.pi1_signature,
                base.pi1_abelianization, True, base.relators,
                base.cells, base.attaching_code, base.ring,
            ).validate()
        with self.assertRaisesRegex(ValueError, "sensus atau banyak sel"):
            SpaceProfile(
                base.slug, base.display_name, base.pi1_signature,
                base.pi1_abelianization, base.generator_count, base.relators,
                ((0, 1), (1, True), (2, 1)), base.attaching_code, base.ring,
            ).validate()
        with self.assertRaisesRegex(ValueError, "relator tidak cocok"):
            SpaceProfile(
                base.slug, base.display_name, base.pi1_signature,
                base.pi1_abelianization, base.generator_count, ((1,),),
                base.cells, base.attaching_code, base.ring,
            ).validate()
        with self.assertRaisesRegex(ValueError, "abelianisasi pi1"):
            SpaceProfile(
                base.slug, base.display_name, base.pi1_signature,
                AbelianGroup(1), base.generator_count, base.relators,
                base.cells, base.attaching_code, base.ring,
            ).validate()

    def test_pair_a_cellular_homology_matches_exactly(self) -> None:
        torus = self.spaces["torus"]
        wedge = self.spaces["wedge_a"]
        self.assertEqual(torus.cells, ((0, 1), (1, 2), (2, 1)))
        self.assertEqual(torus.cells, wedge.cells)
        self.assertEqual(torus.homology(), wedge.homology())
        self.assertEqual(torus.euler_characteristic(), wedge.euler_characteristic())
        self.assertEqual(exponent_sums(torus.relators[0], 2), (0, 0))

    def test_pair_a_pi1_and_abelianization_witness(self) -> None:
        commutator = (1, 2, -1, -2)
        self.assertEqual(free_reduce(commutator, 2), commutator)
        self.assertEqual(exponent_sums(commutator, 2), (0, 0))
        torus = self.spaces["torus"]
        wedge = self.spaces["wedge_a"]
        self.assertNotEqual(torus.pi1_signature, wedge.pi1_signature)
        self.assertEqual(torus.pi1_abelianization, wedge.pi1_abelianization)
        self.assertEqual(torus.pi1_abelianization, dict(torus.homology())[1])

    def test_pair_a_cup_rings_obey_laws_and_differ(self) -> None:
        torus = self.spaces["torus"]
        wedge = self.spaces["wedge_a"]
        torus.ring.validate()
        wedge.ring.validate()
        self.assertEqual(torus.ring.multiply_basis("alpha", "beta"), {"omega": 1})
        self.assertEqual(torus.ring.multiply_basis("beta", "alpha"), {"omega": -1})
        self.assertEqual(wedge.ring.multiply_basis("alpha", "beta"), {})
        comparison = compare_profiles(torus, wedge)
        self.assertTrue(comparison["homology_equal"])
        self.assertTrue(comparison["additive_cohomology_equal"])
        self.assertFalse(comparison["cup_products_equal"])
        self.assertEqual(comparison["first_separator"], "pi1")

    def test_pair_b_only_cup_square_separates_recorded_invariants(self) -> None:
        cp2 = self.spaces["cp2"]
        wedge = self.spaces["wedge_b"]
        comparison = compare_profiles(cp2, wedge)
        self.assertTrue(comparison["pi1_equal"])
        self.assertTrue(comparison["homology_equal"])
        self.assertTrue(comparison["additive_cohomology_equal"])
        self.assertFalse(comparison["cup_products_equal"])
        self.assertEqual(comparison["first_separator"], "produk cup")
        self.assertEqual(cp2.ring.multiply_basis("x", "x"), {"u": 1})
        self.assertEqual(wedge.ring.multiply_basis("x", "x"), {})

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
