# Unit 13 — independent final review

Date: 2026-08-22  
Disposition: **PASS after bounded corrections; no open P1/P2/P3 findings**

## Frozen identities reviewed

- Authority: David Michael Roberts, `AlgebraicTopology2019`, commit
  `b947ad2e9f9e301bfe24590a9db653bc54fa1a53`.
- Upstream witness: `authority/upstream/AlgebraicTopology2019-b947ad2e9f9e301bfe24590a9db653bc54fa1a53/Notes.tex`,
  331,447 bytes, SHA-256
  `cfe93e9dbe3e25bd96f711f59e6078ab97527682b58e1f8ad127f74357f665d7`.
- Exact source boundary checked line by line: Notes.tex lines 2727--3046 inclusive.
  Line 2727 is `\lecturenum{13}`; line 3045 is the heading
  `\section{Classifying covering spaces}`; line 3046 is blank. No prose from
  line 3047 or later occurs in this unit.
- Final reviewed edition file:
  `source/id-ID/units/unit-013-lecture-013.md`, **41,196 bytes, 1,306 lines**,
  SHA-256
  **`0aa68cb4ed31862d32aeff5a7106b4ac29c13cbc202f7dbc8381fc7cd31418c0`**.

## Source-closure and translation review

The complete 320-line source interval was compared against the Indonesian file,
not sampled. The edition contains the lecture marker; the definition and
universal property of the free product with amalgamation; the presentation
formula and its unbounded-presentation margin note; the one-relator example and
source label `eg:one-relator_group`; the closed-surface presentation; the
general finitely presented pushout; the modular-group remark and inherited
Alperin citation; the groupoid pushout construction; the Seifert--van Kampen
setup; the circle calculation; the wedge calculation; the finite and infinite
presentation-complex constructions; the genus-g surface example; and the final
forward section heading.

The source census is closed:

- one definition, four formal examples, one remark, one fact, and both source
  exercises are present;
- all 18 source display blocks are represented, with expanded typed formulas
  where a source formula was defective;
- all eleven Xy-pic diagrams and both TikZ pictures are represented by thirteen
  captioned semantic figure blocks;
- all eleven margin notes are integrated into reading order: unbounded
  presentations, one-relator context, the Alperin reference, capital `H`, the
  category-to-graph observation, omitted composites, the discrete-amalgam
  analogy, the pointed wedge contraction, finite-wedge notation, the CW wedge
  versus Hawaiian earring, and the genus-2 octagon placeholder.

The Indonesian prose was reread continuously. It is natural and internally
consistent after the terminology corrections below. Mathematical symbols,
object/source/target types, and the chronological arrow-product convention are
stated explicitly. No source identifier needed later was lost.

## Mathematical correction audit

Every required source repair is present and correct:

1. The matrix `[[1,-1],[1,0]]` acts by `z -> (z-1)/z`; the source's
   `(1-z)/z` is not retained.
2. The modular action has elliptic stabilizers, so the upper-half-plane quotient
   is described as an orbifold quotient rather than an ordinary covering.
3. `F: Lambda -> H` and `G: Lambda -> Gamma` have their correct codomains.
4. The repaired relation uses parallel arrows
   `G(lambda)=gamma_3`, `F(lambda)=eta_1`; the resulting word equality is
   composable at every junction.
5. The quotient is by the smallest groupoid congruence, stable under both-sided
   composition and inversion, not merely unrelated hom-set equivalences.
6. In the circle computation, `gamma:+1 -> -1` and `eta:-1 -> +1`; the
   chronological generator is `gamma eta`, with the correctly ordered inverse.
7. The source's word “join” is corrected to wedge, and path-connectedness of
   `X` and `Y` is included where the one-object group version of van Kampen is
   invoked.
8. Attaching maps satisfy `[f_i]=R_i`; collars and the CW/weak topology are
   made explicit, including the infinite wedge.
9. Missing `Pi_1` subscripts, the malformed free-group presentation, missing
   relation/isomorphism signs, English typographical defects, and the ordinal
   wording are repaired. The octagon placeholder is replaced by the complete
   directed boundary word.

The two source exercises remain visibly source exercises. Six separately
marked edition-original mastery checks have six complete solutions. In
particular, the solutions establish the groupoid operations and inverses,
prove the pushout universal property, enumerate all four circle hom-sets,
justify the pointed wedge deformation retractions and hypotheses, and derive
the normal-closure quotient and genus-2 surface presentation. The cell-attachment
solution now explicitly uses a collared cover retracting to `W`, `D^2`, and
the boundary circle, so the van Kampen maps and the normal closure are fully
accounted for.

## Accessibility, reflow, provenance, and mechanical validation

- Thirteen figure blocks have thirteen textual captions and explicit semantic
  arrow data. There is no raw Xy-pic, TikZ, raster image, or color-dependent
  mathematics in the edition file.
- Factor membership is carried by textual `[Gamma]`/`[H]` tags. The underlying
  graph paragraph now distinguishes the full directed graph from the one-edge-
  per-inverse-pair schematic, eliminating an earlier internal ambiguity.
- The only named secondary source is the Alperin article already supplied by
  the upstream margin note, and it is cited with its DOI. No unattributed
  third-party passage or solution was found. Edition-original exercises and
  solutions carry `data-origin="edition-original"`; the source/adaptation
  notice and CC BY 4.0 provenance remain explicit.
- Pandoc native parsing with warnings treated as errors: PASS.
- Pandoc standalone HTML5 plus MathML with warnings treated as errors: PASS.
- Fenced divs: 29 opens / 29 closes.
- Stable definitions: 44 / 44 unique; duplicate definitions: 0.
- Internal fragment references: 1; missing targets: 0.
- Display-math delimiters: 176 lines (88 balanced displays).
- Forbidden control characters: 0.

## Findings and bounded corrections

- **P1: 0 found; 0 open.**
- **P2: 3 found and fixed; 0 open.** The graph prose no longer equates the
  complete underlying directed graph with its inverse-pair schematic; the
  established locale term `grupoid kodiskret` replaces `grupoid indiskret`;
  and the cell-attachment mastery solution now identifies the three collared
  deformation retracts and both induced boundary maps explicitly.
- **P3: 1 found and fixed; 0 open.** The Anglicism `topologi weak` is now
  `topologi lemah (weak topology)` in both occurrences.

No ledger, cursor, control file, Git state, or upstream file was touched during
this review.
