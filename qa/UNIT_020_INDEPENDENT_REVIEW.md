# Unit 020 — independent mathematical and structural review

Date: 2026-08-23

## Review scope

The review independently reread `source/id-ID/units/unit-020-lecture-020.md`
against Roberts `Notes.tex:3948–4345` at the frozen upstream commit
`b947ad2e9f9e301bfe24590a9db653bc54fa1a53`. It checked the source boundary,
all source structures and semantic figures, stable IDs, the six mastery
triples, the graph/coboundary matrices, the tetrahedron and Klein-bottle
Smith calculations, the cohomology-functor proof, Indonesian terminology, and
Pandoc structural parsing.

## Final snapshot and verdict

Final snapshot: **45,780 bytes, 1,425 LF lines, SHA-256
`b2592d9dd11d1e805ff2995f96604de35c5454bf2a1e5008163ec5a266d7ea50`**.

- P1: 0
- P2: 0
- P3: 0
- Source span and deferred Lecture 21 boundary are exact.
- All 73 declared structural IDs are unique and remain in the `o012-rbt-l20`
  namespace; all seven semantic figures, eleven margins, eight source-audit
  records, and the 6×(problem/hint/solution) closure are present.
- The triangle transpose/sign convention, graph kernel/cokernel, the
  `delta_1 delta_0=0` proof, tetrahedron cohomology, and Klein-bottle Smith
  form were recomputed. In particular, the Klein cokernel is `Z/2`, not a
  free-plus-torsion group.
- The same-field terminology QA is applied: `fungtor`, `morfisma`,
  `homomorfisma`, `isomorfisma`, `lembaran`, and `tertutup rata`; no
  `isomorfisme` spelling remains in reader-facing text.
- The final language pass corrected the isolated nonstandard spelling
  `bertelescop` to `berteleskop` without changing mathematics or identifiers.
- Pandoc 3.9.0.2 `--to=html5 --mathjax` exits 0 without warnings, and all
  structural IDs survive the parse.

## Attribution and process transparency

The unit retains Roberts's source credit, CC BY 4.0, the independent/non-
endorsement statement, and the exact process note **OpenAI Codex gpt-5.6-sol,
Ultra**. No upstream contact or publication was performed as part of this
review. Unit 20 passes the independent-review gate, subject to the cumulative
build/backend gates before admission.
