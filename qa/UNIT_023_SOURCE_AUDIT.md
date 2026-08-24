# Unit 023 source audit

## Scope and reproducible identity

- Authority: `authority/upstream/AlgebraicTopology2019-b947ad2e9f9e301bfe24590a9db653bc54fa1a53/Notes.tex`.
- Upstream commit: `b947ad2e9f9e301bfe24590a9db653bc54fa1a53`.
- Audited active span: physical source lines **4939–5112**, exactly 174
  LF-joined lines, 9,776 UTF-8 bytes, SHA-256
  `c7256a45621ad7a435277867298e4aeb8eb584dfce066cdae3b48c4ee0e0e3f4`.
- Line 5112 is blank. Line 5113 contains the Lecture 24 marker, but the source
  `example` opened at line 5076 does not close until line 5121. Unit 23 stops
  after line 5111, records the blank boundary line, and leaves that source
  environment explicitly open for Unit 24. Lines 5113–5121 are not imported.

## Reader artifact identity

- `source/id-ID/units/unit-023-lecture-023.md`: 39,176 UTF-8 bytes, 1,094 LF
  lines, SHA-256
  `6f05ddbe6a720109797976c6929b0535f21a38353673cb42d9646a3196f56bd2`.
- The reader contains 51 stable-ID occurrences and 51 unique stable IDs:
  7 identified headings and 44 identified fenced semantic objects. The fenced
  objects include exactly 6 mastery exercises, 6 hints, 6 complete solutions,
  4 edition proof closures, 8 source/accessibility audit records, 2 semantic
  figures, and 6 promoted source-margin notes. There are no duplicate IDs, and
  all 44 fenced blocks are balanced.

## Source census

The active span contains 1 remark, 1 lemma, 1 corollary, 2 `example`
environments (the second incomplete at this boundary), 2 `enumerate`
environments with 6 items total, 6 margin notes, 2 Xy-pic diagrams, 1 active
cross-reference, 9 display-math blocks, and 1 `align*` block. It contains no
definition, formal proof, source exercise, construction, label, citation,
TikZ picture, external graphic, `input`, or `include`.

## Translation and accessibility decisions

The reader preserves source order, every formal object and formula, the active
reference back to the simplex-name example, attribution, CC BY 4.0, process
provenance, and non-endorsement. Six margin notes are promoted into ordinary
reading order. Both Xy-pic diagrams become centered semantic figures whose
nodes, arrows, types, and equal composites are stated in text. The tetrahedron
example has a complete degreewise simplex table and a linear adjacency
description, so no conclusion depends on interpreting an unstated drawing.

## Mathematical/source corrections recorded in the unit

1. The degree-`n` cochain module is `R^{X_n}`, not the source's mistyped
   `R^{X_{n+1}}`; the induced map is typed as evaluation at `x`.
2. The entire cochain complex is not identified with its degree-zero component.
   The basepoint map has degree-zero evaluation and zero higher components.
3. Pointed functoriality is stated contravariantly, with
   `epsilon_x compose f^* = epsilon_y`.
4. `R^{P disjoint-union Q}` is corrected from `R^Q direct-sum R^Q` to
   `R^P direct-sum R^Q`, and cochain complexes use cohomological grading.
5. For a set-indexed infinite disjoint union, cochains form a product. The
   cohomology/product claim is restricted to `R`-modules in ordinary ZFC,
   with the choice-dependent simultaneous-preimage step exposed.
6. The malformed `H^(` at source line 5004 is corrected to `H^n`.
7. Simplices of the tetrahedral boundary are proper nonempty subsets, hence
   occur only in degrees 0 through 2. The census is made explicit.
8. Four separately identified proof closures establish restriction/gluing for
   the disjoint-union complex, the componentwise cycle/boundary quotient, the
   restriction-difference sequence, and the reduced-function isomorphism.
9. The short exact gluing sequence is fully proved degreewise: injection,
   zero composite, unique gluing of agreeing functions, surjectivity by zero
   extension, and commutation with both cochain differentials.
10. The general cover condition is quantified as `X_n = U_n union V_n` for
   every `n >= 0`, not left as an untyped global shorthand.
11. The quotient example uses `A` consistently instead of switching to `Y`.
    A canonical collapsed basepoint is asserted only for nonempty `A`; the
    empty case is handled separately.
12. The precise isomorphism is the restriction of `q^*` from
    `ker(ev_*)`—the reduced functions on `X/A`—onto `ker(i^*)`, not a claim
    about all of `R^{X/A}`. Both directions are proved.
13. The cross-lecture source example is not falsely closed: an explicit
    continuation record distinguishes Markdown balancing from the source
    environment, and fixes the next cursor at line 5113.

## Mastery and provenance closure

Exactly six edition-original mastery exercises each have one stable problem,
one hint, and one complete solution (`mcheck-001..006`, `hint-001..006`,
`sol-001..006`). They cover degree-`n` evaluation, pointed augmentation and
its splitting, finite sums versus infinite products, exactness by gluing,
the tetrahedral counts `X=(4,6,4)`, `U=(4,5,2)`, `V=(4,5,2)`,
`W=(4,4,0)`, and reduced quotient functions including empty `A`. The unit
credits **OpenAI Codex gpt-5.6-sol, Ultra** as process provenance while
preserving Roberts's authorship, contributor credit, CC BY 4.0, and
non-endorsement. This audit is read-only evidence and does not alter the
upstream authority.
