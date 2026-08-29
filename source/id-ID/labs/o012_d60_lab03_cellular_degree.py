#!/usr/bin/env python3
"""Laboratorium D60-03: pemetaan batas seluler dan derajat.

SPDX-License-Identifier: CC-BY-SA-4.0
Materi asli edisi diproduksi dengan OpenAI Codex gpt-5.6-sol, Ultra.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass
from fractions import Fraction
from math import gcd
from typing import Iterable, Sequence


Letter = tuple[str, int]
Word = tuple[Letter, ...]
Matrix2 = tuple[tuple[int, int], tuple[int, int]]
Point = tuple[Fraction, Fraction]

TORUS_BASIS = ("a", "b")
TORUS_WORD: Word = (("a", 1), ("b", 1), ("a", -1), ("b", -1))
X3_BASIS = ("a",)
X3_WORD: Word = (("a", 1), ("a", 1), ("a", 1))
X3_REVERSED_WORD: Word = (("a", -1), ("a", -1), ("a", -1))

MATRIX_M: Matrix2 = ((2, 1), (-1, 2))
MATRIX_N: Matrix2 = ((0, 1), (1, 0))
MATRIX_C: Matrix2 = ((1, 1), (2, 2))
REGULAR_TARGET: Point = (Fraction(1, 7), Fraction(2, 7))
SINGULAR_TARGET: Point = (Fraction(0), Fraction(1, 3))
LEFT_NULL_C = (-2, 1)


def _is_plain_int(value: object) -> bool:
    return type(value) is int


def freeze_basis(basis: Iterable[str]) -> tuple[str, ...]:
    try:
        result = tuple(basis)
    except TypeError as error:
        raise ValueError("basis harus dapat diiterasi") from error
    if not result:
        raise ValueError("basis tidak boleh kosong")
    if any(type(label) is not str or not label for label in result):
        raise ValueError("setiap label basis harus berupa string takkosong")
    if len(set(result)) != len(result):
        raise ValueError("label basis harus unik")
    return result


def freeze_word(word: Iterable[Sequence[object]], basis: Iterable[str]) -> Word:
    frozen_basis = freeze_basis(basis)
    try:
        raw_tokens = tuple(word)
    except TypeError as error:
        raise ValueError("kata pelekatan harus dapat diiterasi") from error
    result: list[Letter] = []
    for token in raw_tokens:
        if isinstance(token, (str, bytes)):
            raise ValueError("setiap huruf harus berupa pasangan label dan tanda")
        try:
            pair = tuple(token)
        except TypeError as error:
            raise ValueError("setiap huruf harus berupa pasangan label dan tanda") from error
        if len(pair) != 2:
            raise ValueError("setiap huruf harus berupa pasangan label dan tanda")
        label, sign = pair
        if type(label) is not str or label not in frozen_basis:
            raise ValueError("kata memuat label yang tidak berada dalam basis")
        if not _is_plain_int(sign) or sign not in (-1, 1):
            raise ValueError("tanda huruf harus +1 atau -1")
        result.append((label, sign))
    return tuple(result)


def free_reduce(word: Iterable[Sequence[object]], basis: Iterable[str]) -> Word:
    frozen = freeze_word(word, basis)
    stack: list[Letter] = []
    for letter in frozen:
        if stack and stack[-1][0] == letter[0] and stack[-1][1] == -letter[1]:
            stack.pop()
        else:
            stack.append(letter)
    return tuple(stack)


def incidence_vector(word: Iterable[Sequence[object]], basis: Iterable[str]) -> tuple[int, ...]:
    frozen_basis = freeze_basis(basis)
    frozen_word = freeze_word(word, frozen_basis)
    return tuple(
        sum(sign for label, sign in frozen_word if label == generator)
        for generator in frozen_basis
    )


def unsigned_occurrence_vector(
    word: Iterable[Sequence[object]], basis: Iterable[str]
) -> tuple[int, ...]:
    """Return unsigned counts only as a deliberately incorrect control."""
    frozen_basis = freeze_basis(basis)
    frozen_word = freeze_word(word, frozen_basis)
    return tuple(
        sum(1 for label, _sign in frozen_word if label == generator)
        for generator in frozen_basis
    )


@dataclass(frozen=True)
class OneColumnHomology:
    h0_free_rank: int
    h1_free_rank: int
    h1_torsion: tuple[int, ...]
    h2_free_rank: int


def one_column_homology(boundary: Iterable[int]) -> OneColumnHomology:
    try:
        column = tuple(boundary)
    except TypeError as error:
        raise ValueError("kolom batas harus dapat diiterasi") from error
    if not column:
        raise ValueError("C_1 harus mempunyai sedikitnya satu pembangkit")
    if any(not _is_plain_int(value) for value in column):
        raise ValueError("koefisien batas harus berupa bilangan bulat")
    common_divisor = 0
    for value in column:
        common_divisor = gcd(common_divisor, abs(value))
    if common_divisor == 0:
        return OneColumnHomology(1, len(column), (), 1)
    torsion = (common_divisor,) if common_divisor > 1 else ()
    return OneColumnHomology(1, len(column) - 1, torsion, 0)


def _exact_fraction(value: object) -> Fraction:
    if isinstance(value, Fraction):
        return value
    if _is_plain_int(value):
        return Fraction(value)
    raise ValueError("koordinat harus berupa bilangan bulat atau Fraction eksak")


def mod_one(value: object) -> Fraction:
    exact = _exact_fraction(value)
    return exact - exact.numerator // exact.denominator


def power_map_preimages(degree: int, target: object) -> tuple[Fraction, ...]:
    if not _is_plain_int(degree):
        raise ValueError("derajat pemetaan pangkat harus berupa bilangan bulat")
    normalized_target = mod_one(target)
    if degree == 0:
        if normalized_target == 0:
            raise ValueError("serat pemetaan konstan pada nilainya sendiri tidak hingga")
        return ()
    count = abs(degree)
    points = {
        mod_one((normalized_target + index) / degree)
        for index in range(count)
    }
    if len(points) != count:
        raise ArithmeticError("pencacahan prabayangan pemetaan pangkat tidak lengkap")
    return tuple(sorted(points))


def power_map_local_degrees(degree: int, target: object) -> tuple[int, ...]:
    points = power_map_preimages(degree, target)
    if not points:
        return ()
    sign = 1 if degree > 0 else -1
    return tuple(sign for _point in points)


def freeze_matrix2(rows: Iterable[Iterable[int]]) -> Matrix2:
    try:
        matrix = tuple(tuple(row) for row in rows)
    except TypeError as error:
        raise ValueError("matriks harus berupa dua baris yang dapat diiterasi") from error
    if len(matrix) != 2 or any(len(row) != 2 for row in matrix):
        raise ValueError("matriks torus harus berukuran 2x2")
    if any(not _is_plain_int(value) for row in matrix for value in row):
        raise ValueError("matriks torus harus mempunyai entri bilangan bulat")
    return (matrix[0], matrix[1])


def determinant2(matrix: Iterable[Iterable[int]]) -> int:
    ((a, b), (c, d)) = freeze_matrix2(matrix)
    return a * d - b * c


def matmul2(
    left: Iterable[Iterable[int]], right: Iterable[Iterable[int]]
) -> Matrix2:
    frozen_left = freeze_matrix2(left)
    frozen_right = freeze_matrix2(right)
    return tuple(
        tuple(
            sum(frozen_left[row][index] * frozen_right[index][column] for index in range(2))
            for column in range(2)
        )
        for row in range(2)
    )  # type: ignore[return-value]


def freeze_point(point: Iterable[object]) -> Point:
    try:
        coordinates = tuple(point)
    except TypeError as error:
        raise ValueError("titik torus harus dapat diiterasi") from error
    if len(coordinates) != 2:
        raise ValueError("titik torus harus mempunyai dua koordinat")
    return (mod_one(coordinates[0]), mod_one(coordinates[1]))


def torus_preimages(matrix: Iterable[Iterable[int]], target: Iterable[object]) -> tuple[Point, ...]:
    frozen_matrix = freeze_matrix2(matrix)
    normalized_target = freeze_point(target)
    ((a, b), (c, d)) = frozen_matrix
    determinant = determinant2(frozen_matrix)
    if determinant == 0:
        raise ValueError("matriks singular tidak mempunyai serat hingga seragam")

    bound = 1 + max(sum(abs(value) for value in row) for row in frozen_matrix)
    points: set[Point] = set()
    for first_shift in range(-bound, bound + 1):
        for second_shift in range(-bound, bound + 1):
            first_rhs = normalized_target[0] + first_shift
            second_rhs = normalized_target[1] + second_shift
            first = (d * first_rhs - b * second_rhs) / determinant
            second = (-c * first_rhs + a * second_rhs) / determinant
            if 0 <= first < 1 and 0 <= second < 1:
                points.add((first, second))
    expected_count = abs(determinant)
    if len(points) != expected_count:
        raise ArithmeticError(
            f"ditemukan {len(points)} prabayangan, seharusnya {expected_count}"
        )
    return tuple(sorted(points))


def torus_local_degrees(
    matrix: Iterable[Iterable[int]], target: Iterable[object]
) -> tuple[int, ...]:
    frozen_matrix = freeze_matrix2(matrix)
    determinant = determinant2(frozen_matrix)
    if determinant == 0:
        raise ValueError("derajat lokal serat hingga tidak tersedia untuk kontrol singular")
    sign = 1 if determinant > 0 else -1
    return tuple(sign for _point in torus_preimages(frozen_matrix, target))


def nonimage_certificate(
    matrix: Iterable[Iterable[int]],
    target: Iterable[object],
    left_null_vector: Iterable[int],
) -> bool:
    frozen_matrix = freeze_matrix2(matrix)
    if determinant2(frozen_matrix) != 0:
        raise ValueError("sertifikat noncitra ini hanya berlaku untuk matriks singular")
    normalized_target = freeze_point(target)
    try:
        vector = tuple(left_null_vector)
    except TypeError as error:
        raise ValueError("vektor null kiri harus dapat diiterasi") from error
    if len(vector) != 2 or any(not _is_plain_int(value) for value in vector):
        raise ValueError("vektor null kiri harus berupa dua bilangan bulat")
    if vector == (0, 0):
        raise ValueError("vektor null kiri tidak boleh nol")
    if any(
        vector[0] * frozen_matrix[0][column]
        + vector[1] * frozen_matrix[1][column]
        != 0
        for column in range(2)
    ):
        raise ValueError("vektor yang diberikan bukan vektor null kiri")
    pairing = vector[0] * normalized_target[0] + vector[1] * normalized_target[1]
    return pairing.denominator != 1


def format_fraction(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def format_integer_vector(vector: Iterable[int]) -> str:
    return "[" + ", ".join(str(value) for value in vector) + "]"


def format_fraction_vector(vector: Iterable[Fraction]) -> str:
    return "[" + ", ".join(format_fraction(value) for value in vector) + "]"


def format_matrix(matrix: Iterable[Iterable[int]]) -> str:
    frozen = freeze_matrix2(matrix)
    return "[" + ", ".join(format_integer_vector(row) for row in frozen) + "]"


def format_points(points: Iterable[Point]) -> str:
    return "[" + ", ".join(
        f"({format_fraction(first)}, {format_fraction(second)})"
        for first, second in points
    ) + "]"


def format_group(free_rank: int, torsion: Iterable[int] = ()) -> str:
    if not _is_plain_int(free_rank) or free_rank < 0:
        raise ValueError("rank bebas harus berupa bilangan bulat taknegatif")
    frozen_torsion = tuple(torsion)
    if any(not _is_plain_int(value) or value <= 1 for value in frozen_torsion):
        raise ValueError("faktor torsi harus berupa bilangan bulat lebih besar dari satu")
    summands: list[str] = []
    if free_rank == 1:
        summands.append("Z")
    elif free_rank > 1:
        summands.append(f"Z^{free_rank}")
    summands.extend(f"Z/{value}" for value in frozen_torsion)
    return " + ".join(summands) if summands else "0"


def summary_lines() -> list[str]:
    torus_boundary = incidence_vector(TORUS_WORD, TORUS_BASIS)
    torus_unsigned = unsigned_occurrence_vector(TORUS_WORD, TORUS_BASIS)
    torus_homology = one_column_homology(torus_boundary)
    x3_boundary = incidence_vector(X3_WORD, X3_BASIS)
    x3_reversed_boundary = incidence_vector(X3_REVERSED_WORD, X3_BASIS)
    x3_homology = one_column_homology(x3_boundary)
    x3_reversed_homology = one_column_homology(x3_reversed_boundary)
    power_target = Fraction(1, 7)
    power_preimages = power_map_preimages(3, power_target)
    power_local = power_map_local_degrees(3, power_target)

    preimages_m = torus_preimages(MATRIX_M, REGULAR_TARGET)
    local_m = torus_local_degrees(MATRIX_M, REGULAR_TARGET)
    preimages_n = torus_preimages(MATRIX_N, REGULAR_TARGET)
    local_n = torus_local_degrees(MATRIX_N, REGULAR_TARGET)
    n_after_m = matmul2(MATRIX_N, MATRIX_M)
    m_after_n = matmul2(MATRIX_M, MATRIX_N)
    singular_certificate = nonimage_certificate(
        MATRIX_C, SINGULAR_TARGET, LEFT_NULL_C
    )

    return [
        "LABORATORIUM O012-D60-LAB03",
        "fixture_seluler_1: torus_minimal",
        "kata_pelekatan_torus: a b a^-1 b^-1",
        f"insidensi_torus_(a,b): {format_integer_vector(torus_boundary)}",
        f"hitung_tak_bertanda_torus: {format_integer_vector(torus_unsigned)}",
        "d1_torus_nol: true",
        f"H_0_torus: {format_group(torus_homology.h0_free_rank)}",
        f"H_1_torus: {format_group(torus_homology.h1_free_rank, torus_homology.h1_torsion)}",
        f"H_2_torus: {format_group(torus_homology.h2_free_rank)}",
        "fixture_seluler_2: X3",
        f"derajat_pelekatan_X3: {x3_boundary[0]}",
        f"d2_X3: {format_integer_vector(x3_boundary)}",
        f"H_0_X3: {format_group(x3_homology.h0_free_rank)}",
        f"H_1_X3: {format_group(x3_homology.h1_free_rank, x3_homology.h1_torsion)}",
        f"H_2_X3: {format_group(x3_homology.h2_free_rank)}",
        f"d2_X3_orientasi_dibalik: {format_integer_vector(x3_reversed_boundary)}",
        f"homologi_orientasi_dibalik_tetap: {str(x3_homology == x3_reversed_homology).lower()}",
        f"target_pangkat_3: {format_fraction(power_target)}",
        f"prabayangan_pangkat_3: {format_fraction_vector(power_preimages)}",
        f"kontribusi_lokal_pangkat_3: {format_integer_vector(power_local)}",
        f"jumlah_derajat_lokal_pangkat_3: {sum(power_local)}",
        f"matriks_M: {format_matrix(MATRIX_M)}",
        f"determinan_M: {determinant2(MATRIX_M)}",
        f"aksi_H1_M: {format_matrix(MATRIX_M)}",
        f"aksi_H2_M: kali_{determinant2(MATRIX_M)}",
        f"target_torus: {format_fraction_vector(REGULAR_TARGET)}",
        f"prabayangan_M: {format_points(preimages_m)}",
        f"jumlah_prabayangan_M: {len(preimages_m)}",
        f"kontribusi_lokal_M: {format_integer_vector(local_m)}",
        f"jumlah_derajat_lokal_M: {sum(local_m)}",
        f"matriks_N: {format_matrix(MATRIX_N)}",
        f"determinan_N: {determinant2(MATRIX_N)}",
        f"prabayangan_N: {format_points(preimages_n)}",
        f"jumlah_derajat_lokal_N: {sum(local_n)}",
        f"matriks_N_setelah_M: {format_matrix(n_after_m)}",
        f"matriks_M_setelah_N: {format_matrix(m_after_n)}",
        f"urutan_komposisi_berbeda: {str(n_after_m != m_after_n).lower()}",
        f"derajat_N_setelah_M: {determinant2(n_after_m)}",
        f"derajat_multiplikatif: {str(determinant2(n_after_m) == determinant2(MATRIX_N) * determinant2(MATRIX_M)).lower()}",
        f"matriks_C: {format_matrix(MATRIX_C)}",
        f"determinan_C: {determinant2(MATRIX_C)}",
        f"target_noncitra_C: {format_fraction_vector(SINGULAR_TARGET)}",
        f"vektor_null_kiri_C: {format_integer_vector(LEFT_NULL_C)}",
        f"sertifikat_noncitra_C: {str(singular_certificate).lower()}",
        "derajat_C: 0",
    ]


def main() -> int:
    payload = ("\n".join(summary_lines()) + "\n").encode("utf-8")
    sys.stdout.buffer.write(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
