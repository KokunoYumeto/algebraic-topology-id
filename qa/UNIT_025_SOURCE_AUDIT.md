# Unit 025 source audit

Date: 2026-08-24
Status: source frozen; translation not yet admitted

## Exact authority and boundary

- Authority: `authority/upstream/AlgebraicTopology2019-b947ad2e9f9e301bfe24590a9db653bc54fa1a53/Notes.tex`.
- Upstream commit: `b947ad2e9f9e301bfe24590a9db653bc54fa1a53`.
- Active span: physical lines **5370–5611**, 242 LF-normalized lines,
  12,732 UTF-8 bytes, SHA-256
  `d05781ae58b1b6fd6174d030e52ca9ee6a08048be96f7c103e5be8de473b60b0`.
- Line 5370 begins `\lecturenum{25}` and is included intact. Line 5611 is
  the blank line after the closing remark.
- Line 5612 begins `Recall\lecturenum{26} the geometric realisation ...` and
  is excluded intact. The exact next source cursor is therefore line 5612.

The byte and hash identity above was recomputed directly from the frozen
authority by joining physical lines 5370–5611 with LF and preserving the
terminal LF; it agrees with the assigned authority packet.

## Direct source census

The active span contains one lecture marker, three definitions, two lemmas,
two propositions, six examples, two proof environments, one two-item
enumeration, eight margin notes, two Xy-pic diagrams, one label, one reference,
and no formal source exercise or question. The Xy-pic diagrams are the long
exact sequence for relative cohomology and the Five Lemma diagram. No external
figure, citation, `input`, or `include` occurs in the span.

The source objects, in order, are: relative-cohomology definition; top-skeleton
example; skeleton-stability lemma; relative-cohomology long exact sequence;
the simplex/boundary example; the two-point relative example; reduced-
cohomology definition; the fat-point example; quasi-isomorphism definition;
fat-point quasi-isomorphism example; Five Lemma and proof; cohomological Euler
characteristic discussion; infinite-line example; equality of the two Euler
characteristics and proof; and the closing finite-complex remark.

## Mathematical repair and completion dossier

1. In the top-skeleton example, the displayed complex starts at `C^1` even
   though the argument concerns every degree below `n`. Restore the full
   degree range `C^0 -> ... -> C^n`; prove directly that every term below
   degree `n` is zero and that the degree-`n` term is `R^{X_n}`. Retain the
   source convention `R^{X_n}[n]` as an aside rather than silently changing
   the result.
2. Supply the omitted proof of
   `H^k(sk_n X;R) ~= H^k(X;R)` for `k<n`: the cochain groups and both
   differentials adjacent to degree `k` agree because `k+1<=n`.
3. The long exact sequence proposition has no source proof. Derive it from
   the degreewise short exact sequence of cochain complexes established in
   Unit 24, type the connecting map, and state exactness and naturality. Redraw
   the positional Xy-pic snake as consecutive, line-break-safe semantic
   sequence fragments.
4. In the two-point example, source line 5449 calls restriction to `{x_0}`
   `pr_2`, which is coordinate-order dependent and conflicts with the usual
   `(x_0,x_1)` ordering. Replace it by the unambiguous restriction map
   `rho_{x_0}(a_0,a_1)=a_0`; its kernel is the functions vanishing at `x_0`.
5. In the infinite-line example, spell out the backward as well as forward
   recursion needed to solve `g(n+1)-g(n)=h(n)` for all integers. This closes
   a terse but correct source step without changing the result.
6. In the Five Lemma proof, source line 5527 types the lifted element `b'` as
   belonging to `B`; it belongs to `B'`. Correct that deterministic type slip.
   More importantly, the source leaves the entire injectivity half as an
   exercise. Supply the full element chase using surjectivity of `alpha` and
   injectivity of `beta` and `delta`. Redraw the positional diagram as two
   exact rows plus an explicit list of the five vertical morphisms, so neither
   meaning nor reading order depends on geometry.
7. Repair the proof of the Euler-characteristic proposition. Source line 5576
   writes the ill-typed direct sum
   `R^{X_d}=ker(delta_d) direct-sum im(delta_d)`, although
   `im(delta_d)` lies in the next cochain group. Use rank–nullity, or choose a
   complement mapped isomorphically onto `im(delta_d)`, and separately split
   `ker(delta_d)` into `im(delta_{d-1})` plus cohomology representatives.
   Replace source `dim delta_d` by `dim im(delta_d)` and source `|X_bullet|`
   by `|X_d|`. Then show cancellation of the two finite alternating rank sums
   with an explicit index shift.
8. In the closing remark, source line 5608 omits the exponent `d` on the left
   sign and omits both `dim` and the exponent on the right. Restore the typed
   identity
   `sum (-1)^d dim V_d = sum (-1)^d dim H^d(V)` for a bounded finite-
   dimensional cochain complex.
9. Move all eight margins into the ordinary reading order: shifted-complex
   notation; finite-approximation caveat; boundary/skeleton cross-reference;
   the not-yet-proved vanishing claim; the infinite dimension of `Pt`; the
   animal-name aside; termination of the Euler sum; and the characteristic-
   zero-field generalisation.

## Planned mastery and stable structure

The edition-original mastery layer will contain six independently solved
items: the top-skeleton relative complex; extraction of information from the
long exact sequence of `(Delta[n],boundary Delta[n])`; reduced cohomology of a
finite pointed discrete Delta-set; the fat-point quasi-isomorphism; both halves
of the Five Lemma chase; and Euler-characteristic cancellation plus the
infinite-line calculation. Every prompt has its own hint and complete solution.

Preserve source label `eg:dim_minus_one_skeleton_rel_cochains` as an alias of
the stable Unit 25 example ID. Use stable IDs under `o012-rbt-l25-*` for every
reader-facing object. Reader terminology follows the admitted lane convention:
`himpunan-Delta`, `kerangka`, `korantai`, `kohomologi relatif`, `kohomologi
tereduksi`, `bertitik dasar`, `kuasi-isomorfisma`, `barisan eksak panjang`,
`Lema Lima`, and `karakteristik Euler`.

The reader must identify Roberts's CC BY 4.0 source, describe all edition-
original proof and mastery material as CC BY 4.0, preserve non-endorsement, and
state the production provenance exactly as `OpenAI Codex gpt-5.6-sol, Ultra`.
This audit does not advance any control cursor; the terminal reader boundary
must name Notes.tex line 5612 as the next source line.
