#!/usr/bin/env python3
"""Laboratorium D60-02: matriks batas dan bentuk normal Smith.

SPDX-License-Identifier: CC-BY-SA-4.0
Materi asli edisi diproduksi dengan OpenAI Codex gpt-5.6-sol, Ultra.
"""
from __future__ import annotations

import sys
from collections import Counter, defaultdict, deque
from dataclasses import dataclass
from itertools import combinations


Matrix = tuple[tuple[int, ...], ...]
Simplex = tuple[int, ...]

RP2_FACES: tuple[Simplex, ...] = (
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

S2_FACES: tuple[Simplex, ...] = tuple(combinations(range(4), 3))


def freeze(rows: list[list[int]] | tuple[tuple[int, ...], ...]) -> Matrix:
    result = tuple(tuple(int(value) for value in row) for row in rows)
    if result and any(len(row) != len(result[0]) for row in result):
        raise ValueError("semua baris matriks harus sama panjang")
    return result


def shape(matrix: Matrix) -> tuple[int, int]:
    if not matrix:
        return 0, 0
    columns = len(matrix[0])
    if any(len(row) != columns for row in matrix):
        raise ValueError("semua baris matriks harus sama panjang")
    return len(matrix), columns


def identity(size: int) -> Matrix:
    if size < 0:
        raise ValueError("ukuran identitas tidak boleh negatif")
    return tuple(
        tuple(1 if row == column else 0 for column in range(size))
        for row in range(size)
    )


def transpose(matrix: Matrix) -> Matrix:
    rows, columns = shape(matrix)
    return tuple(tuple(matrix[row][column] for row in range(rows)) for column in range(columns))


def matmul(left: Matrix, right: Matrix) -> Matrix:
    left_rows, left_columns = shape(left)
    right_rows, right_columns = shape(right)
    if left_columns != right_rows:
        raise ValueError(
            f"ukuran matriks tidak cocok untuk perkalian: "
            f"{left_rows}x{left_columns} dan {right_rows}x{right_columns}"
        )
    return tuple(
        tuple(
            sum(left[row][index] * right[index][column] for index in range(left_columns))
            for column in range(right_columns)
        )
        for row in range(left_rows)
    )


def matvec(matrix: Matrix, vector: tuple[int, ...]) -> tuple[int, ...]:
    rows, columns = shape(matrix)
    if columns != len(vector):
        raise ValueError("panjang vektor tidak cocok dengan domain matriks")
    return tuple(
        sum(matrix[row][column] * vector[column] for column in range(columns))
        for row in range(rows)
    )


def is_zero_matrix(matrix: Matrix) -> bool:
    return all(value == 0 for row in matrix for value in row)


def determinant_bareiss(matrix: Matrix) -> int:
    rows, columns = shape(matrix)
    if rows != columns:
        raise ValueError("determinan hanya didefinisikan untuk matriks persegi")
    if rows == 0:
        return 1
    work = [list(row) for row in matrix]
    sign = 1
    previous = 1
    for pivot_index in range(rows - 1):
        pivot_row = next(
            (row for row in range(pivot_index, rows) if work[row][pivot_index] != 0),
            None,
        )
        if pivot_row is None:
            return 0
        if pivot_row != pivot_index:
            work[pivot_index], work[pivot_row] = work[pivot_row], work[pivot_index]
            sign *= -1
        pivot = work[pivot_index][pivot_index]
        for row in range(pivot_index + 1, rows):
            for column in range(pivot_index + 1, rows):
                numerator = (
                    work[row][column] * pivot
                    - work[row][pivot_index] * work[pivot_index][column]
                )
                if numerator % previous != 0:
                    raise ArithmeticError("pembagian Bareiss tidak eksak")
                work[row][column] = numerator // previous
        for row in range(pivot_index + 1, rows):
            work[row][pivot_index] = 0
        previous = pivot
    return sign * work[-1][-1]


@dataclass(frozen=True)
class SmithResult:
    diagonal: tuple[int, ...]
    transformed: Matrix
    left: Matrix
    right: Matrix

    @property
    def rank(self) -> int:
        return len(self.diagonal)


def smith_normal_form(matrix: Matrix) -> SmithResult:
    """Hitung U A V = D dengan U,V unimodular dan D bentuk normal Smith."""
    matrix = freeze(matrix)
    rows, columns = shape(matrix)
    work = [list(row) for row in matrix]
    left = [list(row) for row in identity(rows)]
    right = [list(row) for row in identity(columns)]

    def swap_rows(first: int, second: int) -> None:
        work[first], work[second] = work[second], work[first]
        left[first], left[second] = left[second], left[first]

    def swap_columns(first: int, second: int) -> None:
        for target in (work, right):
            for row in target:
                row[first], row[second] = row[second], row[first]

    def add_row(target: int, source: int, multiple: int) -> None:
        work[target] = [
            value + multiple * source_value
            for value, source_value in zip(work[target], work[source], strict=True)
        ]
        left[target] = [
            value + multiple * source_value
            for value, source_value in zip(left[target], left[source], strict=True)
        ]

    def add_column(target: int, source: int, multiple: int) -> None:
        for table in (work, right):
            for row in table:
                row[target] += multiple * row[source]

    def negate_row(row: int) -> None:
        work[row] = [-value for value in work[row]]
        left[row] = [-value for value in left[row]]

    pivot_index = 0
    while pivot_index < rows and pivot_index < columns:
        candidates = [
            (abs(work[row][column]), row, column)
            for row in range(pivot_index, rows)
            for column in range(pivot_index, columns)
            if work[row][column] != 0
        ]
        if not candidates:
            break
        _, pivot_row, pivot_column = min(candidates)
        swap_rows(pivot_index, pivot_row)
        swap_columns(pivot_index, pivot_column)

        while True:
            changed = False
            pivot = work[pivot_index][pivot_index]
            for row in range(pivot_index + 1, rows):
                if work[row][pivot_index] == 0:
                    continue
                quotient = work[row][pivot_index] // pivot
                add_row(row, pivot_index, -quotient)
                if work[row][pivot_index] != 0:
                    swap_rows(row, pivot_index)
                changed = True
                break
            if changed:
                continue

            pivot = work[pivot_index][pivot_index]
            for column in range(pivot_index + 1, columns):
                if work[pivot_index][column] == 0:
                    continue
                quotient = work[pivot_index][column] // pivot
                add_column(column, pivot_index, -quotient)
                if work[pivot_index][column] != 0:
                    swap_columns(column, pivot_index)
                changed = True
                break
            if changed:
                continue

            pivot = work[pivot_index][pivot_index]
            offending = next(
                (
                    (row, column)
                    for row in range(pivot_index + 1, rows)
                    for column in range(pivot_index + 1, columns)
                    if work[row][column] % pivot != 0
                ),
                None,
            )
            if offending is None:
                break
            row, _ = offending
            add_row(pivot_index, row, 1)

        if work[pivot_index][pivot_index] < 0:
            negate_row(pivot_index)
        pivot_index += 1

    transformed = freeze(work)
    diagonal = tuple(
        transformed[index][index]
        for index in range(min(rows, columns))
        if transformed[index][index] != 0
    )
    return SmithResult(diagonal, transformed, freeze(left), freeze(right))


def smith_certificate(matrix: Matrix, result: SmithResult) -> bool:
    try:
        rows, columns = shape(matrix)
        if shape(result.left) != (rows, rows) or shape(result.right) != (columns, columns):
            return False
        if shape(result.transformed) != (rows, columns):
            return False
        if matmul(matmul(result.left, matrix), result.right) != result.transformed:
            return False
        for row in range(rows):
            for column in range(columns):
                if row != column and result.transformed[row][column] != 0:
                    return False
        full_diagonal = tuple(
            result.transformed[index][index] for index in range(min(rows, columns))
        )
        nonzero = tuple(value for value in full_diagonal if value != 0)
        if nonzero != result.diagonal or any(value < 0 for value in nonzero):
            return False
        if any(value == 0 for value in full_diagonal[: len(nonzero)]):
            return False
        if any(
            next_value % value != 0
            for value, next_value in zip(nonzero, nonzero[1:])
        ):
            return False
        return abs(determinant_bareiss(result.left)) == 1 and abs(
            determinant_bareiss(result.right)
        ) == 1
    except (ArithmeticError, IndexError, ValueError):
        return False


def validate_simplices(simplices: tuple[Simplex, ...], dimension: int) -> None:
    if len(set(simplices)) != len(simplices):
        raise ValueError("basis simpleks memuat duplikat")
    for simplex in simplices:
        if (
            len(simplex) != dimension + 1
            or any(first >= second for first, second in zip(simplex, simplex[1:]))
        ):
            raise ValueError(
                "simpul setiap simpleks harus terurut naik secara ketat dan berdimensi benar"
            )


def simplex_boundary_matrix(
    domain: tuple[Simplex, ...], codomain: tuple[Simplex, ...]
) -> Matrix:
    if not domain:
        if codomain:
            validate_simplices(codomain, len(codomain[0]) - 1)
        return tuple(tuple() for _ in codomain)
    dimension = len(domain[0]) - 1
    validate_simplices(domain, dimension)
    validate_simplices(codomain, dimension - 1)
    codomain_index = {simplex: index for index, simplex in enumerate(codomain)}
    matrix = [[0 for _ in domain] for _ in codomain]
    for column, simplex in enumerate(domain):
        for deleted in range(len(simplex)):
            face = simplex[:deleted] + simplex[deleted + 1 :]
            if face not in codomain_index:
                raise ValueError(f"muka {face} tidak ada dalam basis kodomain")
            matrix[codomain_index[face]][column] += -1 if deleted % 2 else 1
    return freeze(matrix)


@dataclass(frozen=True)
class SurfaceComplex:
    vertices: tuple[Simplex, ...]
    edges: tuple[Simplex, ...]
    faces: tuple[Simplex, ...]
    d1: Matrix
    d2: Matrix


def build_surface(faces: tuple[Simplex, ...]) -> SurfaceComplex:
    validate_simplices(faces, 2)
    vertex_values = tuple(sorted({vertex for face in faces for vertex in face}))
    vertices = tuple((vertex,) for vertex in vertex_values)
    edges = tuple(
        sorted({edge for face in faces for edge in combinations(face, 2)})
    )
    return SurfaceComplex(
        vertices,
        edges,
        faces,
        simplex_boundary_matrix(edges, vertices),
        simplex_boundary_matrix(faces, edges),
    )


def edge_incidence_counts(faces: tuple[Simplex, ...]) -> Counter[Simplex]:
    return Counter(edge for face in faces for edge in combinations(face, 2))


def vertex_links_are_cycles(faces: tuple[Simplex, ...]) -> bool:
    vertices = sorted({vertex for face in faces for vertex in face})
    for vertex in vertices:
        adjacency: dict[int, set[int]] = defaultdict(set)
        for face in faces:
            if vertex not in face:
                continue
            other = [value for value in face if value != vertex]
            adjacency[other[0]].add(other[1])
            adjacency[other[1]].add(other[0])
        if not adjacency or any(len(neighbours) != 2 for neighbours in adjacency.values()):
            return False
        start = min(adjacency)
        reached = {start}
        queue = deque([start])
        while queue:
            current = queue.popleft()
            for neighbour in adjacency[current]:
                if neighbour not in reached:
                    reached.add(neighbour)
                    queue.append(neighbour)
        if reached != set(adjacency):
            return False
    return True


def boundary_coefficient(face: Simplex, edge: Simplex) -> int:
    for deleted in range(3):
        if face[:deleted] + face[deleted + 1 :] == edge:
            return -1 if deleted % 2 else 1
    raise ValueError("sisi bukan muka dari simpleks-2")


def is_orientable_closed_surface(faces: tuple[Simplex, ...]) -> bool:
    incidence: dict[Simplex, list[tuple[int, int]]] = defaultdict(list)
    for face_index, face in enumerate(faces):
        for edge in combinations(face, 2):
            incidence[edge].append((face_index, boundary_coefficient(face, edge)))
    if any(len(entries) != 2 for entries in incidence.values()):
        raise ValueError("uji orientabilitas memerlukan tepat dua muka per sisi")
    neighbours: dict[int, list[tuple[int, int]]] = defaultdict(list)
    for entries in incidence.values():
        (first, first_coefficient), (second, second_coefficient) = entries
        ratio = -first_coefficient * second_coefficient
        neighbours[first].append((second, ratio))
        neighbours[second].append((first, ratio))
    signs: dict[int, int] = {}
    for start in range(len(faces)):
        if start in signs:
            continue
        signs[start] = 1
        queue = deque([start])
        while queue:
            current = queue.popleft()
            for neighbour, ratio in neighbours[current]:
                required = signs[current] * ratio
                if neighbour in signs and signs[neighbour] != required:
                    return False
                if neighbour not in signs:
                    signs[neighbour] = required
                    queue.append(neighbour)
    return True


def homology_invariants(
    chain_rank: int,
    current_boundary: SmithResult | None,
    next_boundary: SmithResult | None,
) -> tuple[int, tuple[int, ...]]:
    current_rank = 0 if current_boundary is None else current_boundary.rank
    next_rank = 0 if next_boundary is None else next_boundary.rank
    free_rank = chain_rank - current_rank - next_rank
    if free_rank < 0:
        raise ValueError("rank batas tidak mungkin bagi suatu kompleks rantai")
    torsion = (
        ()
        if next_boundary is None
        else tuple(value for value in next_boundary.diagonal if value > 1)
    )
    return free_rank, torsion


def group_notation(invariants: tuple[int, tuple[int, ...]]) -> str:
    free_rank, torsion = invariants
    summands: list[str] = []
    if free_rank == 1:
        summands.append("Z")
    elif free_rank > 1:
        summands.append(f"Z^{free_rank}")
    summands.extend(f"Z/{value}" for value in torsion)
    return " + ".join(summands) if summands else "0"


def format_chain(coefficients: tuple[int, ...], labels: tuple[str, ...]) -> str:
    terms: list[str] = []
    for coefficient, label in zip(coefficients, labels, strict=True):
        if coefficient == 0:
            continue
        magnitude = abs(coefficient)
        body = label if magnitude == 1 else f"{magnitude}{label}"
        if not terms:
            terms.append(body if coefficient > 0 else f"-{body}")
        else:
            terms.append((" + " if coefficient > 0 else " - ") + body)
    return "".join(terms) if terms else "0"


def rp2_torsion_witness(surface: SurfaceComplex) -> dict[str, object]:
    if set(surface.faces) != set(RP2_FACES) or len(surface.faces) != len(RP2_FACES):
        raise ValueError("saksi torsi ini hanya berlaku untuk triangulasi RP2 yang dibekukan")
    cycle_by_edge = {(0, 1): 1, (0, 4): -1, (1, 4): 1}
    filling_by_face = {
        (0, 1, 2): 1,
        (0, 1, 3): 1,
        (0, 2, 4): 1,
        (0, 3, 5): 1,
        (0, 4, 5): -1,
        (1, 2, 5): -1,
        (1, 3, 4): -1,
        (1, 4, 5): 1,
        (2, 3, 4): 1,
        (2, 3, 5): -1,
    }
    cycle = tuple(cycle_by_edge.get(edge, 0) for edge in surface.edges)
    filling = tuple(filling_by_face[face] for face in surface.faces)
    mod2_cocycle = tuple(
        1 if edge in {(0, 1), (0, 2), (1, 3), (2, 4), (3, 4)} else 0
        for edge in surface.edges
    )
    doubled_cycle = tuple(2 * value for value in cycle)
    d1_cycle = matvec(surface.d1, cycle)
    d2_filling = matvec(surface.d2, filling)
    cocycle_on_boundaries = tuple(
        sum(mod2_cocycle[row] * surface.d2[row][column] for row in range(len(surface.edges)))
        % 2
        for column in range(len(surface.faces))
    )
    cocycle_on_cycle = sum(
        coefficient * value
        for coefficient, value in zip(mod2_cocycle, cycle, strict=True)
    ) % 2
    twice_is_boundary = d2_filling == doubled_cycle
    not_boundary = all(value == 0 for value in cocycle_on_boundaries) and cocycle_on_cycle == 1
    return {
        "cycle": cycle,
        "filling": filling,
        "mod2_cocycle": mod2_cocycle,
        "is_cycle": all(value == 0 for value in d1_cycle),
        "twice_is_boundary": twice_is_boundary,
        "mod2_annihilates_boundaries": all(value == 0 for value in cocycle_on_boundaries),
        "mod2_detects_cycle": cocycle_on_cycle == 1,
        "not_boundary": not_boundary,
    }


def analyse_surface(faces: tuple[Simplex, ...]) -> dict[str, object]:
    surface = build_surface(faces)
    d1_smith = smith_normal_form(surface.d1)
    d2_smith = smith_normal_form(surface.d2)
    chain_condition = is_zero_matrix(matmul(surface.d1, surface.d2))
    homology = (
        homology_invariants(len(surface.vertices), None, d1_smith),
        homology_invariants(len(surface.edges), d1_smith, d2_smith),
        homology_invariants(len(surface.faces), d2_smith, None),
    )
    incidence = edge_incidence_counts(surface.faces)
    return {
        "surface": surface,
        "d1_smith": d1_smith,
        "d2_smith": d2_smith,
        "d1_certificate": smith_certificate(surface.d1, d1_smith),
        "d2_certificate": smith_certificate(surface.d2, d2_smith),
        "chain_condition": chain_condition,
        "every_edge_twice": bool(incidence) and all(value == 2 for value in incidence.values()),
        "vertex_links_are_cycles": vertex_links_are_cycles(surface.faces),
        "orientable": is_orientable_closed_surface(surface.faces),
        "euler_characteristic": (
            len(surface.vertices) - len(surface.edges) + len(surface.faces)
        ),
        "homology": homology,
    }


def summary_lines() -> list[str]:
    rp2 = analyse_surface(RP2_FACES)
    sphere = analyse_surface(S2_FACES)
    surface = rp2["surface"]
    assert isinstance(surface, SurfaceComplex)
    d1_smith = rp2["d1_smith"]
    d2_smith = rp2["d2_smith"]
    assert isinstance(d1_smith, SmithResult)
    assert isinstance(d2_smith, SmithResult)
    homology = rp2["homology"]
    assert isinstance(homology, tuple)
    witness = rp2_torsion_witness(surface)
    edge_labels = tuple(f"e{edge[0]}{edge[1]}" for edge in surface.edges)
    face_labels = tuple("f" + "".join(map(str, face)) for face in surface.faces)
    sphere_d1 = sphere["d1_smith"]
    sphere_d2 = sphere["d2_smith"]
    sphere_homology = sphere["homology"]
    assert isinstance(sphere_d1, SmithResult)
    assert isinstance(sphere_d2, SmithResult)
    assert isinstance(sphere_homology, tuple)

    return [
        "LABORATORIUM O012-D60-LAB02",
        "kompleks: triangulasi_6_simpul_RP2",
        f"simpul: {len(surface.vertices)}",
        f"sisi: {len(surface.edges)}",
        f"muka: {len(surface.faces)}",
        f"karakteristik_euler: {rp2['euler_characteristic']}",
        f"setiap_sisi_dua_muka: {str(rp2['every_edge_twice']).lower()}",
        f"tautan_simpul_siklus: {str(rp2['vertex_links_are_cycles']).lower()}",
        f"terorientasi: {str(rp2['orientable']).lower()}",
        f"bentuk_d1: {shape(surface.d1)[0]}x{shape(surface.d1)[1]}",
        f"bentuk_d2: {shape(surface.d2)[0]}x{shape(surface.d2)[1]}",
        f"d1_d2_nol: {str(rp2['chain_condition']).lower()}",
        f"rank_d1: {d1_smith.rank}",
        f"snf_d1: {list(d1_smith.diagonal)}",
        f"rank_d2: {d2_smith.rank}",
        f"snf_d2: {list(d2_smith.diagonal)}",
        f"sertifikat_d1: {str(rp2['d1_certificate']).lower()}",
        f"sertifikat_d2: {str(rp2['d2_certificate']).lower()}",
        f"H_0: {group_notation(homology[0])}",
        f"H_1: {group_notation(homology[1])}",
        f"H_2: {group_notation(homology[2])}",
        f"siklus_torsi_z: {format_chain(witness['cycle'], edge_labels)}",
        f"rantai_pengisi_2z: {format_chain(witness['filling'], face_labels)}",
        f"z_adalah_siklus: {str(witness['is_cycle']).lower()}",
        f"dua_z_adalah_batas: {str(witness['twice_is_boundary']).lower()}",
        f"kosiklus_mod2_mematikan_batas: {str(witness['mod2_annihilates_boundaries']).lower()}",
        f"kosiklus_mod2_mendeteksi_z: {str(witness['mod2_detects_cycle']).lower()}",
        f"z_bukan_batas: {str(witness['not_boundary']).lower()}",
        "kontrol: batas_tetrahedron_S2",
        f"kontrol_terorientasi: {str(sphere['orientable']).lower()}",
        f"kontrol_snf_d1: {list(sphere_d1.diagonal)}",
        f"kontrol_snf_d2: {list(sphere_d2.diagonal)}",
        f"kontrol_H_0: {group_notation(sphere_homology[0])}",
        f"kontrol_H_1: {group_notation(sphere_homology[1])}",
        f"kontrol_H_2: {group_notation(sphere_homology[2])}",
    ]


def main() -> int:
    payload = ("\n".join(summary_lines()) + "\n").encode("utf-8")
    sys.stdout.buffer.write(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
