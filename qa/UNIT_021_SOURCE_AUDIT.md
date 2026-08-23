# Unit 021 source audit

## Scope and reproducible identity

- Authority: `authority/upstream/AlgebraicTopology2019-b947ad2e9f9e301bfe24590a9db653bc54fa1a53/Notes.tex`.
- Upstream commit: `b947ad2e9f9e301bfe24590a9db653bc54fa1a53`.
- Audited active span: physical source lines **4346–4500**, exactly 155
  LF-joined lines, 7,267 UTF-8 bytes, SHA-256
  `281ba27f0f52f35fd9842954c223546e84ce1a0909ee84c14b2081c38c11f150`.
- Raw through-next-marker witness: lines **4346–4501**, 156 lines, 7,359
  bytes, SHA-256
  `8a3ab990ae87087dd259340b08cdb7ddb95068a5b9859de66f7e002115307e6f`.
- Line 4501 contains the Lecture 22 marker and begins new prose outside every
  active source environment. It is deferred intact to Unit 22; no environment
  is split at the boundary.

## Source census

The active span contains 4 `example` environments, 3 definitions, 1 remark,
2 construction environments (`constr` and `construction`), 4 margin notes,
2 TikZ panels, 1 label, 5 display-math blocks, 1 `align*` block, 2 `cases`
blocks, and 1 `enumerate` block. It contains no source exercises, lemmas,
proofs, `align` block, Xy-pic, external graphics, citations, cross-references,
`input`, or `include`.

## Translation and accessibility decisions

The reader preserves source order, formulas, the source label, attribution,
and the CC BY 4.0/non-endorsement notice. Both TikZ panels are represented by
centered semantic descriptions of their ambient coordinate spaces, vertices,
sides, and affine equations. All four margin notes are promoted into ordinary
reading-order callouts. Endpoint orientation is explicit:
`d_1(e)` is glued to `0=partial_1(*)`, while `d_0(e)` is glued to
`1=partial_0(*)`.

## Mathematical/source corrections recorded in the unit

1. The claim after the displayed cohomology groups is restricted to
   `n<0` or `n>2`; the three displayed degrees are not generally zero.
2. The graph quotient relation replaces the source's unbound singleton
   variable by `*` and quantifies the edge and endpoint index.
3. The malformed `Delta^1` set builder is repaired, and “positive octant” is
   corrected to the nonnegative orthant required by the weak inequalities.
4. Every variable and index in the geometric-realisation gluing relation is
   typed, so both related points lie in the declared coproduct.
5. Deterministic punctuation, spelling, and grammar slips at source lines
   4379, 4403, 4414, and 4451 are corrected in natural Indonesian.
6. A triangulation's homeomorphism is typed explicitly. The sphere and torus
   identifications in the final example remain clearly marked as standard
   geometric facts asserted, but not proved, in the active source span.

## Mastery and provenance closure

Six edition-original mastery exercises each have a stable problem, hint, and
complete solution (`mcheck-001..006`, `hint-001..006`, `sol-001..006`). They
cover the truncated cohomology complex, isolated graph vertices, coface
identities, the realisation of `Delta[2]`, circle triangulations, and the
logical distinction between combinatorial data, realisation, and
triangulation. The unit credits **OpenAI Codex gpt-5.6-sol, Ultra** as process
provenance while preserving Roberts's authorship, human direction, CC BY 4.0,
and non-endorsement. This audit is read-only evidence and does not alter the
upstream authority.
