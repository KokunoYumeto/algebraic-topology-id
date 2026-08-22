# Unit 14 independent review

Review date: 2026-08-22

## Scope and authority

- Reviewed artifact: `source/id-ID/units/unit-014-lecture-014.md`
- Sole source authority: `authority/upstream/AlgebraicTopology2019-b947ad2e9f9e301bfe24590a9db653bc54fa1a53/Notes.tex`, lines 3047--3209 inclusive
- The authority span contains 163 lines. The section heading on line 3045 belongs to the preceding unit boundary, and the Lecture 15 marker on line 3210 is outside scope.
- Review operations were confined to this unit and its named authority span. No Git, contact, publication, or external solution source was used.

## Frozen final identity

The reviewed Unit 14 bytes are:

- 28,504 bytes
- UTF-8 without BOM
- LF line endings only
- 947 LF-terminated lines
- SHA-256 `2A14CCB2ACBB0A001EA2DB2716F077925A90DBF4D18B0DC2B63A2D3E5E7F7C40`

The independent final reread found no remaining clear defect, so the review did not modify the unit file.

## Verdict

**PASS.** The final unit preserves the complete semantics and census of Notes.tex lines 3047--3209, repairs the source's type and handedness defects without changing the intended argument, supplies the required independently solved mastery material, and passes the structural and Pandoc checks below.

Open severity counts after review:

- P1: 0
- P2: 0
- P3: 0

## Source census and semantic coverage

The authority span contains:

- one proposition, at Notes.tex 3078--3083, with its proof at 3085--3090;
- one example, at 3092--3123;
- one guiding question, at 3126--3128;
- three lemmas, at 3147--3155, 3163--3168, and 3183--3185;
- two source proof blocks whose entire content is “Exercise”, at 3157--3159 and 3170--3172;
- one unproved source lemma, at 3183--3185;
- one remark, at 3203--3208;
- three Xy-pic diagrams, at 3055--3056, 3069--3074, and 3096--3101; and
- five margin notes, at 3055--3056, 3079, 3144, 3164, and 3176--3177.

All semantic stages occur in the final unit:

1. The monodromy functor on objects and path classes appears at unit lines 74--100.
2. A cover map induces fibre maps and a natural transformation at 102--182.
3. Functoriality on identities and composition is stated and proved at 184--220.
4. The exponential and power-map circle covers, their fibre map, and their monodromy are treated at 222--342.
5. The essential-image question and reduction strategy appear at 344--371.
6. One representative per path component and restriction to the equivalent full subgroupoid appear at 373--438.
7. Componentwise groupoid and functor-category decompositions appear at 440--477.
8. Right `G`-sets, evaluation at an object, and the one-object groupoid lemma appear at 479--543.
9. The combined algebraic reduction and correctly typed componentwise fibre action appear at 545--594.
10. Orbit--stabilizer decomposition by right cosets appears at 596--619.
11. The course-specific SLSC hypothesis and inherited local path connectedness of covers appear at 621--635.
12. The outgoing boundary at 638--644 correctly defers the topological reduction, universal-cover construction, essential surjectivity, and full classification to later units.

No source assertion in the 3047--3209 span is omitted. Added explanations are explicitly editorial or mastery material and do not claim that Unit 14 proves the later classification theorem.

## P1 disposition: type and handedness

All P1 defects are closed.

- Notes.tex 3113--3119 incorrectly types the based circle actions using the many-object groupoid and ambiguous `Aut` codomains. Unit lines 291--341 use the based group `\pi_1(S^1,1)\cong\mathbb Z`, explicit right actions, and `\operatorname{Sym}`. The reduction map is proved equivariant.
- Notes.tex 3174--3201 silently uses left actions and `G/H`. Unit lines 479--619 preserve the edition's chronological right-monodromy convention, use `\mathbf{Set}_G`, and use `H_j\backslash G` with right multiplication. The inverse-converted left action and `G/H_j` are stated separately at 617--619.
- Notes.tex 3193--3195 gives the ill-typed expression `\pi_1(X_i,a_i)\to Z_{a_i}`. Unit lines 568--594 replace it with the action map `Z_{a_i}\times\pi_1(X_i,a_i)\to Z_{a_i}`.
- The one-object groupoid proof at 793--831 checks directly that chronological multiplication gives `F(gh)=F(h)\circ F(g)` and hence a right action.
- The orbit proof at 894--938 checks well-definedness, injectivity, surjectivity, and equivariance of `Hg\mapsto p\cdot g` with the correct multiplication order.

## P2 disposition: proofs, choices, and logical order

All P2 issues are closed.

- Transport maps carry cover superscripts, and the naturality equation is explicit at 151--175. Identity and composition are proved at 200--220 and checked again at 654--696.
- The circle-cover fibres are typed without literal-identification ambiguity at 264--289: general fibres are integer torsors, `p^{-1}(1)=\mathbb Z`, and `q_n^{-1}(1)` is identified with `\mathbb Z/n` through an explicit root-of-unity bijection.
- The component index `I`, section `s`, and selected subset `A=s(I)` are separated at 375--401. Openness of path components and the topology on `I` are stated.
- The full-subgroupoid equivalence is justified in the main reading order at 403--412, with choice dependence recorded at 560--564.
- The restriction lemma and coproduct-functor lemma retain both source exercises at 434--438 and 473--477. Their independent solutions occur at 698--748 and 750--780.
- The source's unproved `[\mathbf BG,\mathbf{Set}]` lemma is proved independently at 782--831.
- The first arrow in the combined chain is explicitly the equivalence `i^*` at 545--558.
- The course's SLSC convention and the evenly covered, path-connected neighbourhood argument are supplied at 623--635 and completed again at 940--947.
- None of the six solutions invokes the later universal-cover construction, topological component equivalence, essential-surjectivity theorem, or classification theorem. They use only path lifting, elementary category constructions, the definitions of a group action and one-object groupoid, orbit--stabilizer algebra, and the already established SLPC/SLSC properties.

## P3 disposition: language, diagrams, and margin reflow

All P3 issues are closed.

- Deterministic source grammar defects at Notes.tex 3079, 3087, 3110, 3140, 3164, and 3199 are normalized in clear Indonesian.
- The three source diagrams are represented exactly once:
  - the cover-map triangle is Figure `o012-rbt-l14-fig-001`, unit lines 106--125;
  - the naturality square is Figure `o012-rbt-l14-fig-002`, lines 157--177; and
  - the exponential/power-map triangle is Figure `o012-rbt-l14-fig-003`, lines 240--262.
- Every diagram includes a linear arrow inventory or commuting equation, so no relationship depends solely on two-dimensional placement.
- All five source margins are in reading order:
  - the margin triangle is Figure 14.1 at 106--125;
  - the functor-category definition is at 179--182;
  - the Assignment 2 subgroupoid note is at 409--412;
  - the product-category description is at 468--470; and
  - the equivariance condition is at 508--514.
- No `\marginnote`, `\xymatrix`, or Xy-pic arrow command remains.
- The final notation for the lifted path is consistent at 140 and 144, the circle-cover wording is type-correct at 236--238, and the right-coset proof begins directly with `g'=hg` at 911--927.

## Exercises and mastery material

- Source exercises: exactly 2, both marked `data-origin="source"`.
- Mastery checks: exactly 6, all marked `data-origin="edition-original"`.
- Mastery solution headings: exactly 6.
- The six solved checks cover:
  1. naturality and functoriality;
  2. restriction along an equivalent full subcategory;
  3. functors from a categorical coproduct;
  4. `[\mathbf BG,\mathbf{Set}]\cong\mathbf{Set}_G` for right actions;
  5. the circle example's types, equivariance, and hidden handedness; and
  6. component reduction, the right-coset orbit model, and the SLSC consequence for covers.

The mastery section identifies itself as independently authored edition material. No external solution citation, quotation, or borrowed proof appears.

## Structural and parser validation

Checks against the frozen bytes produced:

- fenced-div openings: 23
- fenced-div closings: 23
- declared identifiers: 38 (23 fenced semantic blocks plus 15 heading or equation anchors)
- unique identifiers: 38
- duplicate identifiers: 0
- internal fragment links: 3
- unresolved internal fragments: 0
- display-math delimiter lines: 132, forming 66 balanced blocks
- tab characters: 0
- disallowed control characters: 0
- semantic figure blocks: 3
- source exercise blocks: 2
- edition-original mastery blocks: 6
- solution headings: 6

Pandoc 3.9.0.2 parsed the unit as standalone HTML5 with MathJax and `--fail-if-warnings`; exit status was 0 and no warning was emitted.

## Rights, attribution, and independence

The front matter and notice provide the original title and author, David Michael Roberts's 2019 copyright, the exact upstream repository, commit, and source-line link, the CC BY 4.0 license link, and an explicit description of translation, accessibility reflow, source corrections, and added mastery material. The new mastery material is separately identified and licensed CC BY 4.0. The notice also states that the edition is independent and is not sponsored, endorsed, approved, or official. These elements satisfy the attribution, change-indication, license, and non-endorsement requirements for this unit.

## Final disposition

Unit 14 is ready at the frozen identity recorded above. There are no unresolved P1, P2, P3, semantic-coverage, handedness, accessibility, exercise, circularity, structural, parser, rights, or provenance findings.
