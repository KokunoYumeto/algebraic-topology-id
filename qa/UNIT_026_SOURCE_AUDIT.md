# Unit 026 source audit

Date: 2026-08-24
Status: source frozen; translation not yet admitted

## Exact authority and boundary

- Authority: `authority/upstream/AlgebraicTopology2019-b947ad2e9f9e301bfe24590a9db653bc54fa1a53/Notes.tex`.
- Upstream commit: `b947ad2e9f9e301bfe24590a9db653bc54fa1a53`.
- Active span: physical lines **5612--5823**, 212 LF-normalized lines,
  9,763 UTF-8 bytes, SHA-256
  `52663b3e60d5d6f3041b8ede449c52a04700ee670c201ef5674c4aa3973203a9`.
- Line 5612 contains the complete `\lecturenum{26}` marker and is included.
  Line 5823 is the final blank line after the homotopy-invariance proof
  sketch. Line 5824 begins `Let\lecturenum{27} us consider ...` and is
  excluded intact. The exact next source cursor is therefore line 5824.

The byte and hash identity above was recomputed directly from the frozen
authority by joining physical lines 5612--5823 with LF and preserving the
terminal LF. It agrees exactly with the assigned authority packet.

## Direct source census

The active span contains one lecture marker, three definitions, two
propositions, two theorems, one lemma, three corollaries, one remark, two
examples, three proof environments, three margin notes, two labels, and two
references. It contains no formal source
exercise or question, Xy-pic, TikZ, external figure, citation, `input`, or
`include`.

The source objects, in order, are: the geometric-realisation reminder;
integration of differential forms over smooth simplices; the singular
cochain-complex and singular-cohomology definition; the size warning; the
one-point computation; the relative singular cochain-complex and cohomology
definition; the long exact sequence of a pair and its proof; reduced
cohomology, a remark about degree one, and the pointed discrete-space example;
pointed functoriality; the coproduct proposition and proof; homotopy invariance;
three corollaries; cochain homotopy; the induced-map lemma and proof; and the
strong cochain-level homotopy-invariance theorem with a prism-triangulation
sketch.

## Mathematical repair and completion dossier

1. Make the differential-form motivation precise. For the displayed Stokes
   identity, assume that `f` is smooth up to the boundary (for example, the
   restriction of a smooth map on a neighbourhood of the simplex). Smoothness
   only on the interior plus continuous extension, as allowed by the source
   margin, does not by itself guarantee the hypotheses of Stokes's theorem.
   Under the stated regularity, Stokes gives
   `int_(Delta^(k+1)) f^*(d omega) = int_(boundary Delta^(k+1)) f^* omega`,
   i.e. compatibility of exterior differentiation with the alternating-face
   coboundary. This replaces the source's ambiguous wording about “the
   restriction of the primitive of an exact form to the boundary” without
   altering its motivation.
2. In the definition of singular cochains, prove that `delta^2=0` using the
   cosimplicial face relation. Also type the contravariant map induced by
   `f:X->Y` explicitly: postcomposition sends
   `Top(Delta^k,X)->Top(Delta^k,Y)`, and precomposition of functions gives
   `f^*:C^k(Y;R)->C^k(X;R)`. Source line 5646 omits the comma in
   `Top(Delta^k,Y)` and leaves the sentence grammatically incomplete.
3. Preserve the point computation and make its alternating differential
   transparent. The interval-cardinality example remains a size illustration;
   its claim `H^1(I;Z/2)=0` is justified later by contractibility rather than
   treated as a direct calculation.
4. Complete the long-exact-sequence proof: restriction of arbitrary functions
   is degreewise surjective because a cochain on `A` extends by zero outside
   the singular simplices landing in `A`. Hence the relative complex is the
   kernel in a short exact sequence of cochain complexes. Type the connecting
   homomorphism and naturality, and preserve source label
   `prop:les_of_pair_of_spaces`.
5. Repair the reduced-cohomology discussion. The restriction
   `H^0(X;R)->H^0({x};R)=R` is always surjective, since constant cocycles lift
   every scalar. Exactness therefore makes the connecting map
   `R->H^1(X,x;R)` zero and gives
   `H^k(X,x;R) ~= H^k(X;R)` for **every** `k>=1`, not merely `k>1`.
   Source lines 5711--5713 formally call ordinary `H^1` a quotient but leave
   the image unresolved; the image is zero. Record this as an edition repair.
6. Close the margin exercise asserting pointed functoriality. A pointed map
   is a map of pairs, so contravariant relative cohomology supplies the induced
   map; identity and composition follow from the relative-cochain functor.
7. In the coproduct proposition, repair both occurrences of the delimiter
   typo `C^bullet(X,A:R)` to `C^bullet(X,A;R)`. State the hidden reason for
   source line 5741: each simplex `Delta^k` is connected, so every map into
   `X sqcup Y` lands wholly in one summand. Decompose absolute cochains,
   restrictions, kernels, and differentials to prove the relative statement.
8. In the contractibility corollary, source line 5768 says both that
   `H^k(X;R)=0` for `k>0` and, without a degree, that `H^k(X;R)~=R`.
   Restore the intended typed assertion `H^0(X;R)~=R`.
9. Supply proofs of all three corollaries from functoriality and homotopy
   invariance, including the contravariant order of `f^*` and `g^*` and the
   path-induced equality of evaluations.
10. In the cochain-homotopy lemma, source line 5801 ends with
    `h_(k+1)(delta^A_k(x))` although the cocycle was named `c`. Repair `x` to
    `c` and spell out why a coboundary represents zero.
11. The principal missing proof is the final theorem. Define the signed prism
    operator from the standard triangulation of `Delta^n times I`, establish
    `partial P+P partial=g_#-f_#` by face cancellation, and dualise with
    `h(phi)=-phi composed with P` to obtain
    `delta h+h delta=f^*-g^*`. This proves the labelled homotopy-invariance
    theorem. The source sketch is retained as intuition, but no theorem is
    left resting on “messy combinatorics.”
12. Move all three margins into ordinary reading order: the regularity
    convention for smooth simplex maps; the “seen before” cross-reference for
    the point complex; and the pointed-functoriality exercise, which becomes a
    proved proposition/audit rather than an inaccessible aside.

## Planned mastery and stable structure

The edition-original mastery layer will contain six independently solved
items: verification that the singular coboundary squares to zero; the point
and contractible-space calculations; the long exact sequence computation of
`H^*(I,partial I;R)`; reduced degree-zero cohomology of a finite pointed
discrete space; coproduct decomposition with the connected-domain condition;
and construction/dualisation of a prism operator. Every prompt will have its
own hint and complete solution.

Preserve source labels `prop:les_of_pair_of_spaces` and
`thm:homotopy_invariance_cohom` as aliases of stable Unit 26 IDs. Use stable
IDs under `o012-rbt-l26-*` for every reader-facing object. Reader terminology
follows the admitted lane convention: `himpunan-Delta`, `realisasi geometrik`,
`simpleks singular`, `korantai singular`, `kohomologi singular`, `kohomologi
relatif`, `kohomologi tereduksi`, `bertitik dasar`, `homotopi korantai`,
`operator prisma`, and `invariansi homotopi`.

The reader must identify Roberts's CC BY 4.0 source, describe all
edition-original proofs and mastery material as CC BY 4.0, preserve
non-endorsement, and state the production provenance exactly as
`OpenAI Codex gpt-5.6-sol, Ultra`. This audit does not advance any control
cursor; the terminal reader boundary must name Notes.tex line 5824 as the next
source line.
