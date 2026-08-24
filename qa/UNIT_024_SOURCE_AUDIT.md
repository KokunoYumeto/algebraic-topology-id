# Unit 024 source audit

Date: 2026-08-24
Status: source frozen; translation not yet admitted

## Exact authority and boundary

- Authority: `authority/upstream/AlgebraicTopology2019-b947ad2e9f9e301bfe24590a9db653bc54fa1a53/Notes.tex`.
- Upstream commit: `b947ad2e9f9e301bfe24590a9db653bc54fa1a53`.
- Active span: physical lines **5113–5369**, 257 LF-normalized lines,
  12,837 UTF-8 bytes, SHA-256
  `b2128930a56a0a8c04c327a397e72e21b215ffe742bb684e8dd166f0e04b0aea`.
- Line 5113 contains `\lecturenum{24}` inside the example opened at line
  5076. Lines 5113–5121 finish that same example; Unit 24 must resume it under
  the Unit 23 parent relation before beginning new source objects.
- Line 5370 begins `\lecturenum{25}` and is excluded intact.

## Source census

The span contains one lecture marker, one closing `example` and no opening
`example`, one definition, one theorem, three lemmas, one remark, three proof
environments, one six-item enumeration, seven margin notes, two Xy-pic
diagrams, one TikZ figure, four labels, four references, and eight display
math blocks. It contains no formal source exercise, citation, external image,
`input`, or `include`. One of the three proof environments is only the word
`Exercise`; the Snake Lemma proof explicitly leaves three of its six
exactness/homomorphism obligations to the reader.

## Mathematical repair and completion dossier

1. Prove that restriction
   `C^bullet(X;R) -> C^bullet(A;R)` is a cochain map and degreewise
   surjective, that its kernel is stable under the differential, and hence
   that the displayed sequence is short exact. State that degreewise
   extension by zero is generally not a cochain-map splitting.
2. Supply the omitted proof that degreewise kernels of a morphism of
   complexes form a complex; type every restricted differential.
3. In the algebraic Mayer–Vietoris theorem, source line 5173 writes the term
   after `H^(k+1)(i)` merely as `(B_bullet)`. Restore
   `H^(k+1)(B_bullet)` and verify every map in the long exact sequence.
4. In the Snake Lemma diagram, the lower-right module must be `C'`, not `C`.
   Replace both positional diagrams and the colored snake route with
   centered semantic arrow data plus a complete linear element chase.
5. Complete all six obligations listed in the Snake Lemma proof: construct
   the connector, prove it is well defined and `R`-linear, and prove
   exactness at all six kernel/cokernel positions. Correct the deterministic
   `a_b`/`a'_b` notation slips and missing punctuation without changing the
   argument.
6. Replace the empty proof of `lemma:setup_for_algMV` with a complete proof
   that both quotient/kernel rows are exact and that the vertical
   differentials are well defined and commute.
7. In the theorem proof, repair the missing parenthesis in the image formula,
   prove the two kernel/cokernel identifications marked as exercises, and
   justify how the six-term sequences for consecutive `k` splice into one
   long exact sequence.
8. Clarify the final naturality paragraph: a morphism between short exact
   sequences induces a morphism between the resulting **long exact
   sequences**, not merely an unspecified map between complexes.
9. Move all seven margins into reading order. The animal-name aside remains
   visibly ancillary; no theorem statement or map direction may depend on
   color, geometry, or arrow position.

## Planned mastery and stable structure

The edition-original mastery layer should contain six independently solved
items: relative cochains and the non-cochain zero-extension example; kernels
of complex morphisms; construction/well-definedness of the Snake connector;
the connector's linearity and the three omitted exactness positions; exactness
of the setup diagram; and assembly/naturality of the long exact sequence.
Every prompt must have a hint and complete solution. Preserve source labels
`thm:alg_Mayer-Vietoris`, `snakeLemma`, `fig:snake_lemma`, and
`lemma:setup_for_algMV` as aliases while assigning Unit 24 stable IDs.

Reader-facing terminology should retain `fungtor`, `morfisma`, `kosiklus`,
`kobatas`, `kernel`, `kokernel`, `barisan eksak pendek`, `barisan eksak
panjang`, `aljabar homologis`, `Lema Ular`, and `pengejaran diagram`, subject
to the admitted terminology ledger. This audit does not translate or advance
the cursor; it fixes the exact next production surface.
