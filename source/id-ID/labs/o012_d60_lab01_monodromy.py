#!/usr/bin/env python3
"""Laboratorium D60-01: monodromi, data Schreier, dan presentasi grup.

SPDX-License-Identifier: CC-BY-SA-4.0
Materi asli edisi diproduksi dengan OpenAI Codex gpt-5.6-sol, Ultra.
"""
from __future__ import annotations

import sys
from collections import deque
from collections.abc import Iterable, Mapping


INVERSE_LETTER = {"a": "A", "A": "a", "b": "B", "B": "b"}
LETTER_ORDER = ("a", "A", "b", "B")
POSITIVE_GENERATORS = ("a", "b")


def inverse_permutation(permutation: tuple[int, ...]) -> tuple[int, ...]:
    inverse = [0] * len(permutation)
    for source, target in enumerate(permutation):
        inverse[target] = source
    return tuple(inverse)


def inverse_word(word: str) -> str:
    """Kembalikan invers suatu kata pada alfabet a,A,b,B."""
    _validate_word(word)
    return "".join(INVERSE_LETTER[letter] for letter in reversed(word))


def reduce_word(word: str) -> str:
    """Reduksi bebas suatu kata dalam grup bebas F(a,b)."""
    _validate_word(word)
    stack: list[str] = []
    for letter in word:
        if stack and INVERSE_LETTER[letter] == stack[-1]:
            stack.pop()
        else:
            stack.append(letter)
    return "".join(stack)


def _validate_word(word: str) -> None:
    invalid = sorted(set(word) - set(LETTER_ORDER))
    if invalid:
        raise ValueError(f"huruf kata tidak sah: {invalid}")


def cycle_notation(permutation: tuple[int, ...]) -> str:
    """Tulis permutasi sebagai siklus-siklus taktrivial yang saling lepas."""
    seen: set[int] = set()
    cycles: list[str] = []
    for start in range(len(permutation)):
        if start in seen:
            continue
        cycle: list[int] = []
        current = start
        while current not in seen:
            seen.add(current)
            cycle.append(current)
            current = permutation[current]
        if len(cycle) > 1:
            cycles.append("(" + " ".join(str(value) for value in cycle) + ")")
    return "".join(cycles) or "()"


class CoveringAction:
    """Aksi monodromi kanan berhingga F(a,b) pada lembaran bernomor."""

    def __init__(self, positive: Mapping[str, Iterable[int]]) -> None:
        if tuple(positive) != POSITIVE_GENERATORS:
            raise ValueError("pembangkit positif harus diberikan dalam urutan a,b")
        converted = {name: tuple(values) for name, values in positive.items()}
        degree = len(converted["a"])
        if degree == 0 or len(converted["b"]) != degree:
            raise ValueError("kedua permutasi harus mempunyai derajat positif yang sama")
        expected = tuple(range(degree))
        for name, permutation in converted.items():
            if tuple(sorted(permutation)) != expected:
                raise ValueError(f"R_{name} bukan permutasi lembaran 0,...,{degree - 1}")
        self.degree = degree
        self.transitions = {
            "a": converted["a"],
            "A": inverse_permutation(converted["a"]),
            "b": converted["b"],
            "B": inverse_permutation(converted["b"]),
        }

    def act(self, sheet: int, word: str) -> int:
        """Terapkan aksi kanan langsung menurut urutan kronologis kata."""
        if sheet not in range(self.degree):
            raise ValueError(f"lembaran di luar rentang: {sheet}")
        _validate_word(word)
        current = sheet
        for letter in word:
            current = self.transitions[letter][current]
        return current

    def permutation(self, word: str) -> tuple[int, ...]:
        return tuple(self.act(sheet, word) for sheet in range(self.degree))

    def orbit(self, start: int) -> tuple[int, ...]:
        if start not in range(self.degree):
            raise ValueError(f"lembaran di luar rentang: {start}")
        reached = {start}
        queue = deque([start])
        while queue:
            current = queue.popleft()
            for letter in LETTER_ORDER:
                target = self.transitions[letter][current]
                if target not in reached:
                    reached.add(target)
                    queue.append(target)
        return tuple(sorted(reached))

    def orbits(self) -> tuple[tuple[int, ...], ...]:
        unseen = set(range(self.degree))
        result: list[tuple[int, ...]] = []
        while unseen:
            orbit = self.orbit(min(unseen))
            result.append(orbit)
            unseen.difference_update(orbit)
        return tuple(result)

    def image(self) -> tuple[tuple[int, ...], ...]:
        """Daftarkan citra hingga yang dibangkitkan oleh operator transisi."""
        identity = tuple(range(self.degree))
        reached = {identity}
        queue = deque([identity])
        while queue:
            current = queue.popleft()
            for letter in LETTER_ORDER:
                transition = self.transitions[letter]
                extended = tuple(transition[current[sheet]] for sheet in range(self.degree))
                if extended not in reached:
                    reached.add(extended)
                    queue.append(extended)
        return tuple(sorted(reached))

    def schreier_transversal(self, start: int = 0) -> dict[int, str]:
        """Pilih transversal deterministik yang tertutup terhadap prefiks."""
        if start not in range(self.degree):
            raise ValueError(f"lembaran di luar rentang: {start}")
        words = {start: ""}
        queue = deque([start])
        while queue:
            current = queue.popleft()
            for letter in LETTER_ORDER:
                target = self.transitions[letter][current]
                if target not in words:
                    words[target] = words[current] + letter
                    queue.append(target)
        return words

    def schreier_basis(self, start: int = 0) -> tuple[str, ...]:
        """Kembalikan pembangkit Schreier taktrivial t*x*overline(tx)^-1."""
        transversal = self.schreier_transversal(start)
        if len(transversal) != self.degree:
            raise ValueError("pembentukan basis bebas memerlukan aksi transitif")
        basis: list[str] = []
        for sheet in range(self.degree):
            representative = transversal[sheet]
            for generator in POSITIVE_GENERATORS:
                target = self.act(sheet, generator)
                word = reduce_word(
                    representative + generator + inverse_word(transversal[target])
                )
                if word:
                    basis.append(word)
        return tuple(basis)

    def graph_rank(self) -> int:
        if len(self.orbits()) != 1:
            raise ValueError("rumus rank tunggal ini memerlukan graf terhubung")
        vertices = self.degree
        positive_edges = self.degree * len(POSITIVE_GENERATORS)
        return positive_edges - vertices + 1


def build_lab_action() -> CoveringAction:
    return CoveringAction(
        {
            "a": (1, 2, 3, 0),
            "b": (0, 3, 2, 1),
        }
    )


def summary_lines(action: CoveringAction) -> list[str]:
    orbit = action.orbit(0)
    transversal = action.schreier_transversal(0)
    basis = action.schreier_basis(0)
    relations = {
        "a4": action.permutation("aaaa") == tuple(range(action.degree)),
        "b2": action.permutation("bb") == tuple(range(action.degree)),
        "baba": action.permutation("baba") == tuple(range(action.degree)),
    }
    lines = [
        "LABORATORIUM O012-D60-LAB01",
        f"jumlah_lembaran: {action.degree}",
        f"R_a: {cycle_notation(action.transitions['a'])}",
        f"R_b: {cycle_notation(action.transitions['b'])}",
        f"orbit_lembaran_0: {list(orbit)}",
        f"terhubung: {str(len(orbit) == action.degree).lower()}",
        f"orde_citra_monodromi: {len(action.image())}",
        f"relasi_a4: {str(relations['a4']).lower()}",
        f"relasi_b2: {str(relations['b2']).lower()}",
        f"relasi_baba: {str(relations['baba']).lower()}",
        f"indeks_stabilisator: {len(orbit)}",
        f"simpul_graf: {action.degree}",
        f"sisi_graf: {action.degree * len(POSITIVE_GENERATORS)}",
        f"rank_grup_penutup: {action.graph_rank()}",
        "transversal_schreier:",
    ]
    for sheet in range(action.degree):
        lines.append(f"  {sheet}: {transversal[sheet] or '1'}")
    lines.append("basis_bebas:")
    lines.extend(f"  {word}" for word in basis)
    lines.extend(
        [
            f"basis_memperbaiki_0: {str(all(action.act(0, word) == 0 for word in basis)).lower()}",
            "presentasi_citra: <a,b | a^4, b^2, baba>",
            "presentasi_penutup: <b, aba, aaaa, aabAA, AbA | >",
        ]
    )
    return lines


def main() -> int:
    payload = ("\n".join(summary_lines(build_lab_action())) + "\n").encode("utf-8")
    sys.stdout.buffer.write(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
