# Unit 025 — independent mathematical and structural review

Date: 2026-08-24

## Review scope

This review independently compared
`source/id-ID/units/unit-025-lecture-025.md` and
`qa/UNIT_025_SOURCE_AUDIT.md` against the frozen Roberts authority
`Notes.tex:5370–5611` at commit
`b947ad2e9f9e301bfe24590a9db653bc54fa1a53`. It checked the exact boundary,
source order and census, every definition, lemma, proposition, example, proof,
margin, label/reference, and diagram; all edition-supplied proof closures; all
six mastery solutions; semantic reflow; Indonesian terminology; stable
structure; rights and provenance; and the terminal cursor.

## Snapshot and fail-closed verdict

Final reader snapshot: **36,578 bytes, 1,104 LF lines, SHA-256
`df72add4e57236b51ff7d2a0c99af4b65299365874163cb334be5d0988c0f769`**.
Source-audit snapshot: **6,386 bytes, 109 LF lines, SHA-256
`f252e9f15e0980ed2a2c15dfbd1c22fd6fd99990333e2de9a9372f695523e903`**.

- P1: 0
- P2: 0
- P3: 0
- Overall status: **PASS**.
- The active source span is exactly 242 physical lines and 12,732
  LF-normalized UTF-8 bytes, SHA-256
  `d05781ae58b1b6fd6174d030e52ca9ee6a08048be96f7c103e5be8de473b60b0`.
  Line 5370 contains the complete Lecture 25 marker, line 5611 is the retained
  terminal blank line, and line 5612 begins Lecture 26 and remains excluded.
- All 59 reader stable IDs are unique. Seven identified headings and 52
  balanced fenced semantic objects preserve the exact structural inventory:
  three definitions, two lemmas, two propositions, six examples, four proof
  blocks, two semantic figures, seven ordinary-flow asides carrying all eight
  source margins, six audit records, one remark, six problem/hint/full-solution
  triples, and one terminal boundary.

### Resolved pre-admission finding

The initial independent review identified `UNIT025-TERM-P3-001` — **P3**,
reader line 56. The phrase
`kompleks korantai simplicial relatif` uses `simplicial`, while the admitted
lane term for *relative simplicial cochain complex* is
`kompleks korantai simpleksial relatif` (`backend/terms.jsonl`, terminology
control `O012-TERM-0312`), and Unit 24 already uses that form consistently.
The owning task replaced only `simplicial` with `simpleksial` before admission.
The correction changed the reader by one byte and did not alter its line count,
mathematics, IDs, or topology. The exact final reader identity above includes
the correction. The finding is retained here as transparent history and is no
longer counted as open.

## Source topology and mathematical fidelity

The direct source census is exact: one lecture marker, three definitions, two
lemmas, two propositions, six examples, two source proof environments, one
two-item enumeration, eight margins, two Xy-pic diagrams, one label, one
reference, and no source exercise, question, external figure, citation,
`input`, or `include`. Reader objects remain in source order. The source label
`eg:dim_minus_one_skeleton_rel_cochains` is preserved on Contoh 25.1, and the
source reference resolves to that stable reader object.

- The top-skeleton example correctly restores the omitted degree-zero term,
  proves that every relative cochain group below degree `n` vanishes, identifies
  the degree-`n` group with `R^{X_n}`, and retains `R^{X_n}[n]` as an aside.
- The previously omitted skeleton lemma proof correctly observes that
  `k<n` implies `k+1<=n`, so the three cochain groups and two adjacent
  differentials determining `H^k` agree. It also handles degree zero.
- The relative long exact sequence is correctly derived from the degreewise
  short exact sequence of cochain complexes. The connector has the right
  degree, is independent of both lift and cocycle representative, is linear,
  and exactness is checked at each of the three recurring types of term.
  Naturality is stated and justified.
- The two-point example repairs the ambiguous source `pr_2` to the typed
  restriction `rho_{x_0}(a_0,a_1)=a_0`, with the correct kernel.
- The fat-point calculation, reduced cohomology, and induced
  quasi-isomorphism have the correct complexes, differential parity, direction,
  and cohomology. The text correctly limits the claim that the cochain map is
  not an isomorphism to `R` nonzero.
- Both Five Lemma rows, all five vertical maps, and all four commutativity
  identities are preserved semantically. The source's `b' in B` type slip is
  corrected to `b' in B'`. The complete injectivity half uses exactly the
  surjectivity of `alpha` and injectivity of `beta` and `delta`; the retained
  surjectivity half is also correct.
- The infinite-line example supplies both the forward and backward recursion,
  proving surjectivity of the coboundary on all integers.
- The Euler proof replaces the ill-typed direct sum in the source by two valid
  dimension identities, uses `dim im(delta_d)`, restores `|X_d|`, and makes the
  alternating-rank cancellation explicit by an index shift. The closing
  finite-complex identity restores both missing exponents and dimensions.

Each of the six edition-original exercises has exactly one hint and a complete
solution. Together they cover the top-skeleton relative complex, the long
exact sequence of a simplex and its boundary, reduced cohomology of a pointed
finite discrete object, the fat-point quasi-isomorphism, the omitted
injectivity half of the Five Lemma, and the infinite-line/Euler cancellation
calculation. No unproved step needed by a requested solution remains.

## Accessibility, rendering, rights, and provenance

The two positional Xy-pic diagrams are replaced by consecutive exact-sequence
fragments plus explicit object, arrow, and commutativity data. Every one of the
eight source margins appears in ordinary reading order; two related margins in
the simplex-boundary example share one aside without losing content. No raw
Xy-pic, margin-placement, TikZ, float-positioning, or external-graphic command
survives.

Pandoc 3.9.0.2 converts the frozen reader to standalone HTML5 with native
MathML, warnings fatal, at exit zero. The result contains all 59 reader IDs,
449 MathML nodes, 60 unique DOM IDs in total, one resolved same-file fragment,
no raw-TeX math fallback, and no runtime script or stylesheet dependency.

The unit retains David Michael Roberts's source credit, exact commit and line
span, CC BY 4.0, an explicit independent/non-endorsement statement,
human-contributor credit, and the exact process note **OpenAI Codex
gpt-5.6-sol, Ultra**. No private path, credential marker, placeholder, or claim
of official status is present.

The next source cursor is stated exactly as Notes.tex line 5612. Mathematics,
source completeness, terminology, stable structure, rendering, accessibility,
rights, and provenance have no open P1, P2, or P3 finding. The corrected frozen
evidence package is **PASS**. This review does not itself advance the source
cursor, admit a backend append, or claim publication.
