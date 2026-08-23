# Unit 022 source audit

## Scope and reproducible identity

- Authority: `authority/upstream/AlgebraicTopology2019-b947ad2e9f9e301bfe24590a9db653bc54fa1a53/Notes.tex`.
- Upstream commit: `b947ad2e9f9e301bfe24590a9db653bc54fa1a53`.
- Audited active span: physical source lines **4501–4938**, exactly 438
  LF-joined lines, 20,585 UTF-8 bytes, SHA-256
  `86275c590cfcdf8519d3ce8d077fc48619bb94c3fdf039ca805ae4b7df995b7f`.
- Raw through-next-marker witness: lines **4501–4939**, 439 lines, 20,668
  bytes, SHA-256
  `de8b63537d295d5a6d85591be81863ae4416a14323b13b1517153465f0cb9a12`.
- Line 4939 contains the Lecture 23 marker and starts new prose outside every
  active environment. It is deferred intact to Unit 23; no source environment
  is split at the boundary.

## Source census

The active span contains 6 definitions, 11 `example` environments, 5 lemmas,
3 proofs, 3 remarks, 5 margin notes, 2 TikZ pictures, 3 Xy-pic relationships,
2 labels, 1 cross-reference, 8 display-math blocks, 4 `align*` blocks,
1 `cases` block, and 1 `center` environment. It contains no source exercise,
construction, `enumerate`, unstarred `align`, citation, external graphic,
`input`, or `include`.

## Translation and accessibility decisions

The reader preserves source order, all formal environments and formulas, both
source labels and their one active reference, attribution, and the CC BY 4.0
non-endorsement notice. The five margin notes are promoted to ordinary reading
order. The two TikZ pictures and three Xy-pic relationships are represented by
five centered semantic figures. The infinite-cylinder figure is additionally
bound to complete endpoint and face tables, and every commutative diagram
states its equal composites in prose.

## Mathematical/source corrections recorded in the unit

1. A chosen simplex gives a canonical simplex-name map; it is called an
   inclusion only when its distinct faces remain distinct.
2. The infinite-cylinder picture is converted to typed incidence tables. The
   map to the torus does not by itself reconstruct its chosen indexed lift.
3. The realisation-functor proof types its prequotient map and verifies both
   identity and composition laws.
4. Infinite dimension means nonempty simplices in unbounded degrees; the
   empty Delta-set is treated separately.
5. General realisation relations and Delta-set morphisms quantify all
   variables and distinguish domain from codomain face maps.
6. The canonical map from `|Delta[n]|` is indexed by `Delta[n]_k`, not by the
   source's mistyped `Delta[k]`, and is exhibited as a homeomorphism.
7. The cochain differential sums from `i=0` through `n+1`, using all `n+2`
   faces. The source's “Exercise!” proof of `delta squared = 0` is completed by
   an explicit signed pairing.
8. The cochain-functor proof is expanded with typed differentials, identities,
   and contravariant composition.
9. Finite generation is stated over a Noetherian coefficient ring; for
   infinite face sets, `R^A` continues to mean the product of all functions.
10. “Singular cochain complex” in the coefficient paragraph is corrected to
    “simplicial cochain complex”.
11. The torsion-kernel and lattice conclusions for `Z -> R` are restricted to
    finite Delta-sets; the natural coefficient map remains valid generally.
12. The cylinder and torus homeomorphisms are explicitly identified as
    standard geometric source assertions rather than proofs supplied by this
    span.
13. Deterministic source spelling, article, and number-agreement errors at the
    recorded locators are normalized in natural Indonesian.
14. Independent review replaced an imprecise phrase in mastery hint 22.6 by
    the exact fact that the additive group of an `F_p`-vector space is
    annihilated by `p`.

These decisions are registered as `O012-ADV-0298..0311`. New admitted terms
are registered as `O012-TERM-0293..0300`.

## Mastery and provenance closure

Six edition-original mastery exercises each have a stable problem, hint, and
complete solution (`mcheck-001..006`, `hint-001..006`, `sol-001..006`). They
cover the cylinder-to-torus map, simplex-name maps, the staircase prism,
the corrected cochain differential, contravariance on a polygon, and change
of coefficients with its finiteness hypotheses. The unit credits **OpenAI
Codex gpt-5.6-sol, Ultra** as process provenance while preserving Roberts's
authorship, human direction, CC BY 4.0, and non-endorsement. This audit is
read-only evidence and does not alter the upstream authority.
