#!/usr/bin/env python3
"""Laboratorium D60-04: perbandingan lintas-invarian yang eksak.

Program ini memverifikasi empat model CW yang dibekukan untuk laboratorium;
ia bukan pemecah umum masalah isomorfisma grup atau gelanggang.

SPDX-License-Identifier: CC-BY-SA-4.0
Materi asli edisi diproduksi dengan OpenAI Codex gpt-5.6-sol, Ultra.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import Iterable, Mapping


Word = tuple[int, ...]
ProductRow = tuple[str, str, int, str]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


@dataclass(frozen=True, order=True)
class AbelianGroup:
    """Grup abelian terbangkit hingga dalam bentuk Z^r plus faktor torsi."""

    free_rank: int
    torsion: tuple[int, ...] = ()

    def __post_init__(self) -> None:
        require(
            isinstance(self.free_rank, int)
            and not isinstance(self.free_rank, bool)
            and self.free_rank >= 0,
            "rank bebas tidak sah",
        )
        require(
            all(
                isinstance(order, int)
                and not isinstance(order, bool)
                and order > 1
                for order in self.torsion
            ),
            "orde torsi tidak sah",
        )
        require(tuple(sorted(self.torsion)) == self.torsion, "faktor torsi harus kanonis")

    def label(self) -> str:
        pieces: list[str] = []
        if self.free_rank == 1:
            pieces.append("Z")
        elif self.free_rank > 1:
            pieces.append(f"Z^{self.free_rank}")
        pieces.extend(f"Z/{order}" for order in self.torsion)
        return " + ".join(pieces) if pieces else "0"


def free_reduce(word: Iterable[int], generator_count: int) -> Word:
    """Reduksi kata bebas; generator i ditulis i dan inversnya -i."""

    require(
        isinstance(generator_count, int)
        and not isinstance(generator_count, bool)
        and generator_count >= 0,
        "banyak generator tidak sah",
    )
    stack: list[int] = []
    for letter in word:
        require(
            isinstance(letter, int)
            and not isinstance(letter, bool)
            and 1 <= abs(letter) <= generator_count,
            "huruf kata bebas tidak sah",
        )
        if stack and stack[-1] == -letter:
            stack.pop()
        else:
            stack.append(letter)
    return tuple(stack)


def exponent_sums(word: Iterable[int], generator_count: int) -> tuple[int, ...]:
    reduced = free_reduce(word, generator_count)
    return tuple(
        sum(1 if letter == index else -1 if letter == -index else 0 for letter in reduced)
        for index in range(1, generator_count + 1)
    )


@dataclass(frozen=True)
class CupRing:
    """Tabel produk cup jarang pada basis homogen kohomologi bebas."""

    basis_degrees: tuple[tuple[str, int], ...]
    products: tuple[ProductRow, ...]

    def degrees(self) -> dict[str, int]:
        result = dict(self.basis_degrees)
        require(len(result) == len(self.basis_degrees), "basis kohomologi berulang")
        require(result.get("1") == 0, "basis harus memuat unit berderajat nol")
        require(
            all(
                isinstance(basis, str)
                and basis
                and isinstance(degree, int)
                and not isinstance(degree, bool)
                and degree >= 0
                for basis, degree in result.items()
            ),
            "derajat basis tidak sah",
        )
        return result

    def multiply_basis(self, left: str, right: str) -> dict[str, int]:
        degrees = self.degrees()
        require(left in degrees and right in degrees, "elemen basis tidak dikenal")
        if left == "1":
            return {right: 1}
        if right == "1":
            return {left: 1}
        matches = [(coefficient, target) for a, b, coefficient, target in self.products if (a, b) == (left, right)]
        require(len(matches) <= 1, "entri produk basis berulang")
        return {matches[0][1]: matches[0][0]} if matches and matches[0][0] else {}

    def multiply(
        self,
        left: Mapping[str, int],
        right: Mapping[str, int],
    ) -> dict[str, int]:
        result: dict[str, int] = {}
        for left_basis, left_coefficient in left.items():
            for right_basis, right_coefficient in right.items():
                for target, coefficient in self.multiply_basis(left_basis, right_basis).items():
                    result[target] = result.get(target, 0) + left_coefficient * right_coefficient * coefficient
        return {basis: coefficient for basis, coefficient in sorted(result.items()) if coefficient}

    def validate(self) -> None:
        degrees = self.degrees()
        seen: set[tuple[str, str]] = set()
        for left, right, coefficient, target in self.products:
            require(left in degrees and right in degrees and target in degrees, "produk memakai basis tidak dikenal")
            require((left, right) not in seen, "entri produk basis berulang")
            seen.add((left, right))
            require(left != "1" and right != "1", "produk unit eksplisit bertentangan dengan unit implisit")
            require(
                isinstance(coefficient, int)
                and not isinstance(coefficient, bool)
                and coefficient != 0,
                "koefisien produk harus bulat tak nol",
            )
            require(degrees[target] == degrees[left] + degrees[right], "derajat produk cup tidak cocok")

        basis = tuple(degrees)
        for left in basis:
            for right in basis:
                lhs = self.multiply_basis(left, right)
                rhs = {
                    key: ((-1) ** (degrees[left] * degrees[right])) * value
                    for key, value in self.multiply_basis(right, left).items()
                }
                require(lhs == rhs, "tabel tidak komutatif bergradasi")
                for third in basis:
                    left_assoc = self.multiply(lhs, {third: 1})
                    right_assoc = self.multiply({left: 1}, self.multiply_basis(right, third))
                    require(left_assoc == right_assoc, "tabel produk cup tidak asosiatif")

    def additive_ranks(self) -> tuple[tuple[int, int], ...]:
        counts: dict[int, int] = {}
        for _basis, degree in self.basis_degrees:
            counts[degree] = counts.get(degree, 0) + 1
        return tuple(sorted(counts.items()))

    def positive_product_signature(self) -> tuple[ProductRow, ...]:
        degrees = self.degrees()
        return tuple(
            sorted(
                row
                for row in self.products
                if degrees[row[0]] > 0 and degrees[row[1]] > 0
            )
        )


@dataclass(frozen=True)
class SpaceProfile:
    slug: str
    display_name: str
    pi1_signature: str
    pi1_abelianization: AbelianGroup
    generator_count: int
    relators: tuple[Word, ...]
    cells: tuple[tuple[int, int], ...]
    attaching_code: str
    ring: CupRing

    def homology(self) -> tuple[tuple[int, AbelianGroup], ...]:
        """Semua model beku mempunyai diferensial seluler nol."""

        return tuple((degree, AbelianGroup(count)) for degree, count in self.cells if count)

    def euler_characteristic(self) -> int:
        return sum(((-1) ** degree) * count for degree, count in self.cells)

    def validate(self) -> None:
        require(
            all(isinstance(value, str) and value.strip() for value in (
                self.slug, self.display_name, self.pi1_signature, self.attaching_code,
            )),
            "metadata ruang tidak lengkap",
        )
        require(
            isinstance(self.generator_count, int)
            and not isinstance(self.generator_count, bool)
            and self.generator_count >= 0,
            "banyak generator tidak sah",
        )
        require(tuple(sorted(self.cells)) == self.cells, "sensus sel tidak kanonis")
        require(self.cells and self.cells[0] == (0, 1), "model harus terhubung dengan satu sel nol")
        require(
            all(
                isinstance(degree, int)
                and not isinstance(degree, bool)
                and degree >= 0
                and isinstance(count, int)
                and not isinstance(count, bool)
                and count > 0
                for degree, count in self.cells
            ),
            "sensus atau banyak sel tidak sah",
        )
        require(len({degree for degree, _count in self.cells}) == len(self.cells), "dimensi sel berulang")
        for relator in self.relators:
            free_reduce(relator, self.generator_count)
        require(
            all(
                exponent_sums(relator, self.generator_count)
                == (0,) * self.generator_count
                for relator in self.relators
            ),
            "relator tidak cocok dengan abelianisasi bebas model beku",
        )
        require(
            self.pi1_abelianization == AbelianGroup(self.generator_count),
            "abelianisasi pi1 tidak cocok dengan presentasi model beku",
        )
        self.ring.validate()
        homology_ranks = tuple((degree, group.free_rank) for degree, group in self.homology())
        require(homology_ranks == self.ring.additive_ranks(), "homologi dan kohomologi aditif tidak cocok")
        h1 = dict(self.homology()).get(1, AbelianGroup(0))
        require(h1 == self.pi1_abelianization, "H1 tidak cocok dengan abelianisasi pi1")


def fixtures() -> dict[str, SpaceProfile]:
    commutator = (1, 2, -1, -2)
    torus_ring = CupRing(
        (("1", 0), ("alpha", 1), ("beta", 1), ("omega", 2)),
        (("alpha", "beta", 1, "omega"), ("beta", "alpha", -1, "omega")),
    )
    wedge_a_ring = CupRing(
        (("1", 0), ("alpha", 1), ("beta", 1), ("omega", 2)),
        (),
    )
    cp2_ring = CupRing(
        (("1", 0), ("x", 2), ("u", 4)),
        (("x", "x", 1, "u"),),
    )
    wedge_b_ring = CupRing(
        (("1", 0), ("x", 2), ("u", 4)),
        (),
    )
    spaces = {
        "torus": SpaceProfile(
            "torus", "T^2", "Z^2", AbelianGroup(2), 2, (commutator,),
            ((0, 1), (1, 2), (2, 1)), "commutator", torus_ring,
        ),
        "wedge_a": SpaceProfile(
            "wedge_a", "S^1 v S^1 v S^2", "F_2", AbelianGroup(2), 2, (),
            ((0, 1), (1, 2), (2, 1)), "constant_2_cell", wedge_a_ring,
        ),
        "cp2": SpaceProfile(
            "cp2", "CP^2", "1", AbelianGroup(0), 0, (),
            ((0, 1), (2, 1), (4, 1)), "hopf_eta", cp2_ring,
        ),
        "wedge_b": SpaceProfile(
            "wedge_b", "S^2 v S^4", "1", AbelianGroup(0), 0, (),
            ((0, 1), (2, 1), (4, 1)), "constant_4_cell", wedge_b_ring,
        ),
    }
    for profile in spaces.values():
        profile.validate()
    return spaces


def homology_label(profile: SpaceProfile) -> str:
    return ", ".join(f"H{degree}={group.label()}" for degree, group in profile.homology())


def compare_profiles(left: SpaceProfile, right: SpaceProfile) -> dict[str, object]:
    left.validate()
    right.validate()
    comparison = {
        "pi1_equal": left.pi1_signature == right.pi1_signature,
        "homology_equal": left.homology() == right.homology(),
        "additive_cohomology_equal": left.ring.additive_ranks() == right.ring.additive_ranks(),
        "cup_products_equal": left.ring.positive_product_signature() == right.ring.positive_product_signature(),
        "euler_equal": left.euler_characteristic() == right.euler_characteristic(),
    }
    order = (
        ("pi1_equal", "pi1"),
        ("homology_equal", "homologi"),
        ("additive_cohomology_equal", "kohomologi aditif"),
        ("cup_products_equal", "produk cup"),
    )
    comparison["first_separator"] = next((label for key, label in order if comparison[key] is False), "tidak ada")
    return comparison


def render_report() -> str:
    spaces = fixtures()
    torus, wedge_a = spaces["torus"], spaces["wedge_a"]
    cp2, wedge_b = spaces["cp2"], spaces["wedge_b"]
    pair_a = compare_profiles(torus, wedge_a)
    pair_b = compare_profiles(cp2, wedge_b)
    commutator = torus.relators[0]
    reduced = free_reduce(commutator, 2)
    sums = exponent_sums(commutator, 2)
    lines = [
        "D60-LAB04 | sintesis lintas-invarian",
        "Pasangan A: T^2 vs S^1 v S^1 v S^2",
        f"  pi1: {torus.pi1_signature} vs {wedge_a.pi1_signature}; komutator bebas={reduced}; jumlah eksponen={sums}",
        f"  homologi: sama ({homology_label(torus)}); chi={torus.euler_characteristic()}",
        "  cup: torus alpha cup beta=omega, beta cup alpha=-omega; baji=0",
        f"  pemisah pertama: {pair_a['first_separator']}",
        "Pasangan B: CP^2 vs S^2 v S^4",
        f"  pi1: {cp2.pi1_signature} vs {wedge_b.pi1_signature}; homologi sama ({homology_label(cp2)})",
        "  pelekatan sel-4: Hopf eta vs konstan; x cup x: u vs 0",
        f"  pemisah pertama: {pair_b['first_separator']}",
        "Audit: H1 adalah abelianisasi pi1; diferensial seluler tidak menyimpan seluruh peta pelekatan.",
        "Audit: kesamaan daftar invarian bukan bukti ekuivalensi homotopi umum.",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    sys.stdout.buffer.write(render_report().encode("utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
