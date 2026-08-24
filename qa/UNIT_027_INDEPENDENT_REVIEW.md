# Unit 027 — independent mathematical and structural review

Date: 2026-08-24

## Review scope

This review independently compared
`source/id-ID/units/unit-027-lecture-027.md` and
`qa/UNIT_027_SOURCE_AUDIT.md` against the frozen Roberts authority
`Notes.tex:5824–5923` at commit
`b947ad2e9f9e301bfe24590a9db653bc54fa1a53`. It checked the exact source
boundary and census; every source object, label, reference, formula, and
margin; the edition's mathematical repairs and proof closures; all six
exercise/hint/full-solution triples; Indonesian terminology against the
admitted glossary; stable-ID uniqueness and fenced structure; native-MathML
conversion; attribution, rights, non-endorsement, and model provenance; and
the terminal source cursor. No backend, ledger, build, control, Git, or other
unit was changed by this review.

## Final snapshot and fail-closed verdict

Final reader snapshot: **35,879 bytes, 1,175 LF lines, SHA-256
`a3238bbc429e4c3689bce3b3bb78c5514e0fae74f276c9efebe694730b2df2a0`**.
Source-audit snapshot: **7,369 bytes, 126 LF lines, SHA-256
`67621ce38a69fe4e6afd24fa6572dfa6e9499a3e77db03e3943ce045dfa30138`**.

- P1: 0
- P2: 0
- P3: 0
- Overall status: **PASS**.
- The active authority span is exactly 100 physical lines and 7,012
  LF-normalized UTF-8 bytes, SHA-256
  `65d2c393ddf29183f36d6e9ab65c65f8030110334f89c7f68ba88461fc30afa1`.
  It begins with the complete Lecture 27 marker at line 5824, includes the
  terminal blank line 5923, and excludes the complete Lecture 28 marker at
  line 5924. The exact next source cursor is line 5924.
- All 46 reader stable IDs are unique. Seven identified headings and 39
  balanced fenced semantic objects preserve the reader topology: two
  definitions, one lemma, one proposition, one theorem, three examples, three
  proof blocks, one semantic figure, two source-labeled equations, five audit
  records, one reflowed source margin, six exercises, six hints, six complete
  solutions, and one terminal boundary.

### Resolved pre-admission findings

Five defects found during independent review were corrected narrowly in the
Unit 27 reader before this final verdict. They remain recorded as transparent
history and are no longer open findings.

1. `UNIT027-MATH-P2-001` — **P2**, final reader locus line 481. The cochain
   comparison formula had lost the backslash before `longrightarrow`, turning
   an arrow into literal mathematical text. The missing backslash was restored;
   the map is now typed as
   `rho: C^bullet(X;R) -> C_U^bullet(X;R)`.
2. `UNIT027-A11Y-P2-002` — **P2**, final reader lines 369–373. The first
   semantic pushout array retained arrow syntax that Pandoc could not convert
   to native MathML under fatal warnings. It was replaced by an equivalent
   `mathop(longrightarrow)`/`downarrow` array while retaining all four arrow
   names and the separately stated commutativity and universal property.
3. `UNIT027-PROOF-P2-003` — **P2**, final reader lines 693–715. The first draft
   constructed the Mayer--Vietoris connector but summarized exactness as an
   unexpanded diagram chase. The proof now verifies image-equals-kernel at each
   of the three recurring types of term, including the required lift
   adjustments and the converse construction from `Phi(a)=delta b`.
4. `UNIT027-TERM-P3-001` — **P3**, final reader lines 38, 407–410, 455, 973,
   1050, and 1086. Variants based on *perpanjangan* were normalized to the
   admitted `O012-TERM-0314` term **perluasan dengan nol**, with grammatically
   corresponding verb forms. No mathematics, source identity, ID, or boundary
   changed.
5. `UNIT027-TERM-P3-002` — **P3**, final reader lines 60 and 317. The draft
   used the recognized but nonpreferred variant *funktorial*. Both occurrences
   were normalized to the admitted preferred form **fungtorial**, consistently
   derived from `O012-TERM-0004` (*fungtor*) and `O012-TERM-0072`
   (*fungtorialitas*). No mathematics, identifier, or boundary changed.

## Source closure and mathematical fidelity

The direct source census is exact: one lecture marker, one definition, one
lemma, one proposition, one theorem, one formal source exercise, three
examples, one proof environment, one margin, one Xy-pic diagram, four labels,
and two references. There is no TikZ, external graphic, citation, `input`, or
`include`. The reader preserves the source order and closes every object.
Aliases retain `eg:reduced_cohom_S0`, `eq:restr_to_intersection`,
`thm:mayer-vietoris`, and `eq:sphere_cohomol_reduction`; both source references
resolve semantically to the immediately identified equation and Example 27.2.

- The source exercise is solved from the singular zero-cochain differential:
  zero-cocycles are exactly functions constant on path-components, there are
  no degree-minus-one coboundaries in the chosen complex, and pullback is
  precomposition on `pi_0`.
- The source's ill-typed `!_X composed with x = id_X` is correctly repaired to
  `id_pt`. Contravariance then gives `ev_x composed with const = id_R`.
- The splitting lemma is proved constructively in both directions and its
  restriction to `ker(r)` is handled. This justifies the basepoint-dependent
  kernel model and the canonical basepoint-free cokernel model of reduced
  degree-zero cohomology.
- The path-connected statement is correctly limited to reduced degree zero;
  contractibility supplies the separate all-degree vanishing claim. The
  zero-sphere quotient by the diagonal is correct over an arbitrary
  coefficient ring.
- The positional pushout is reflowed with complete arrow data, commutativity,
  and universal property. Degreewise zero extension is used only to prove the
  surjectivity of the difference-of-restrictions map and is not misrepresented
  as a cochain-map splitting.
- The edition correctly replaces the source's invalid zero-extension
  subcomplex by `Hom_R(C_*^U(X;R),R)`, reverses the comparison map by
  contravariance, and proves the small-chain theorem using barycentric
  subdivision, the prism homotopy, the Lebesgue number lemma, and an explicit
  inductive chain-homotopy inverse. The formulas for `r`, `K`, and their duals
  have the correct degrees, directions, and signs.
- Mayer--Vietoris is derived from the correct degreewise short exact sequence
  of cochain complexes. The connecting morphism is well defined, exactness is
  proved at all recurring positions, and the reduced sequence beginning with
  zero is explicitly restricted to nonempty intersection under the edition's
  nonnegative-degree convention.
- The hemispherical calculation uses open, contractible pieces and obtains the
  correct suspension recurrence. Its induction gives `H^0(S^n;R)=R`,
  `H^n(S^n;R)=R`, and zero in every other positive degree for `n>=1`.

All six mastery items have exactly one hint and one complete solution. They
cover the source exercise, an explicit inverse to a left splitting, reduced
degree-zero cohomology for finitely many path-components, the zero-extension
counterexample, the Mayer--Vietoris generator of `H^1(S^1;R)`, and the full
cohomology of spheres. The last noncontractibility conclusion explicitly uses
a nonzero coefficient ring.

## Terminology, accessibility, rights, and provenance

Admitted forms are used consistently, including `kohomologi tereduksi`,
`komponen lintasan`, `terhubung lintasan`, `korantai`, `kobatas`, `kosiklus`,
`barisan eksak pendek/panjang`, `kernel`, `kokernel`, `isomorfisma`,
`homomorfisma`, `sampul terbuka`, `pemetaan restriksi`, `perluasan dengan nol`,
`fungtorial`, and `kuasi-isomorfisma`. No rejected *simplicial*, *isomorfisme*,
*homomorfisme*, or *perpanjangan* variant remains.

Pandoc 3.9.0.2 converts the final reader to standalone HTML5 with native
MathML and warnings fatal at exit zero. The result contains 459 MathML nodes,
all 46 reader IDs, no duplicate DOM ID, no raw-TeX fallback, and no runtime
script or external stylesheet dependency. The Xy-pic diagram and margin note
are represented in reading order without raw layout commands.

The unit retains David Michael Roberts's source credit, exact commit and line
span, CC BY 4.0, an explicit independent/non-endorsement statement, preserved
human-contributor credit, and the exact model note **OpenAI Codex
gpt-5.6-sol, Ultra**. No private path, credential marker, placeholder, or claim
of official status is present. The exact next cursor is Notes.tex line 5924.
The corrected final evidence package is **PASS** and this review does not
advance the source cursor or claim backend admission or publication.
