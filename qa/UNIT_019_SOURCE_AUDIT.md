# Unit 019 source audit

## Scope and reproducible identity

- Frozen source: `authority/upstream/AlgebraicTopology2019-b947ad2e9f9e301bfe24590a9db653bc54fa1a53/Notes.tex`.
- Audited span: physical source lines 3678--3947 inclusive, exactly 270 lines. Lecture 19 starts at line 3678; Lecture 20 starts at line 3948.
- Census text contains 2,427 whitespace-delimited tokens and 16,723 UTF-8 bytes after joining the 270 lines with LF and omitting a final newline.
- SHA-256 of that explicitly LF-normalized span: `15feb1cca535c90df280e232ce23cb44719a4cf863c6ee17f8c29da5c4f462ab`.
- This audit is read-only source analysis. It does not silently amend the frozen authority.

## Formal and asset census

- 1 lecture marker and 1 section marker (`Complexes`).
- 6 definitions, 12 examples, 2 lemmas, 1 remark, and 1 proof environment.
- Exactly 1 upstream exercise: the proof marked `Exercise` at lines 3767--3773. There are no formal `ex` or `q` environments.
- 15 `\[...\]` display blocks and 1 `align*` block; the triangle map also contains 1 `cases` environment.
- 4 inline `xymatrix` diagrams, 2 inline TikZ diagrams, 13 marginal notes, and 2 source labels.
- No citation, cross-reference, external graphic, `input`, or `include` occurs in the span. All graphical content is inline source.
- The unit boundary is structurally clean: line 3946 closes the graph-complex definition, line 3947 is blank, and line 3948 begins Lecture 20.

## Corrections and mathematical cautions

1. Line 3678: repair subject--verb agreement in "A large source ... arise".
2. Line 3680: state that `G/H` is formed by the right action `g . h = gh`. A fibre is an `H`-torsor and is homeomorphic to `H` after a choice; it is not canonically an identified copy. The margin's subgroup-nesting summary should not imply that every listed matrix group belongs to one inclusion chain.
3. Line 3692: "assuming >= 3" is missing the variable `n`.
4. Line 3704: exactness determines `im(delta)=2Z`, so `delta: Z -> Z` is multiplication by `+/-2`; it becomes `+2` only after compatible generator choices. Repair the duplicated grammar in the same sentence.
5. Line 3714: `whose story` must be `whole story`.
6. Lines 3789--3793: restrict the elementary Euler-characteristic formula and dimension reconstruction to suitable finite polyhedra/finite-dimensional data. Alternating infinite cardinalities are not automatically an Euler characteristic. For infinite `S`, the function module `R^S` is a product and its vector-space dimension need not equal `|S|`.
7. Line 3793: `vertx` must be `vertex`.
8. Line 3830: require `U` to be an open subset of `R^3`, not arbitrary `R^n`, because the displayed vector fields, curl, and divergence are three-dimensional.
9. Line 3833: repair `acomplex` to `a complex`.
10. Lines 3840--3851: the definition is syntactically incomplete; explicitly say that every displayed square commutes.
11. Lines 3853--3861: repair "There is map" and label or explain the vertical maps: zero, quotient, identity, and the induced map `B-bar`. This is required to make the claimed morphism independently checkable.
12. Lines 3874--3879: the displayed unaugmented vector-calculus complex is not exact at its first `C^infinity(R^3)` because `ker(gradient)` is the constants. Say that it is exact in positive degrees, or augment it by the constant inclusion `R -> C^infinity(R^3)`.
13. Lines 3880--3886: de Rham cohomology over `R` and `pi_2(S^2)=Z` both detect the sphere's topology, but they are not literally the same invariant; keep the comparison qualitative.
14. Line 3892: repair "the image gradient" to "the image of the gradient".
15. Lines 3905--3912: injectivity permits at most one edge per ordered pair. It still permits two oppositely directed edges between an unordered pair, so "no more than one edge between any two vertices" is too broad.

## Results used without proof or with incomplete proof

- The closed-subgroup quotient bundle theorem at line 3680, the sphere homogeneous-space identifications, and the double-cover facts about the low-dimensional matrix groups are invoked without proof.
- The assertion that every finite-dimensional Lie group has trivial second homotopy group is explicitly presented as a hard external fact.
- The weak contractibility and noncontractibility of the Warsaw circle are asserted; the brief path sentence is not a complete proof.
- Functoriality of `slpc(-)` is the span's sole explicit exercise and needs a full solution.
- Both statements about the canonical map `slpc(X) -> X` are unproved: weak equivalence, and failure to be a homotopy equivalence when `X` is not SLPC.
- The vector-calculus exactness statements rely on the Poincare lemma or equivalent analysis and need their scope stated precisely.

## Convention, prerequisite, and handedness hazards

- The source's generic complex has differential `d_n: A_n -> A_(n+1)`: this is cohomological grading. Do not silently reverse the arrows or mechanically label it with the existing homological `chain complex` term.
- A map of complexes must preserve degree and commute with the differentials. The source margin says `chain map`, but the displayed grading raises degree.
- A directed edge points from `d_1(e)` to `d_0(e)`, while the graph coboundary is `delta(f)(e)=f(d_0(e))-f(d_1(e))`, target minus source. The example intentionally writes `(d_1,d_0)` although the definition tests injectivity of `(d_0,d_1)`.
- `R^S` means all functions `S -> R`, hence a product for infinite `S`; it is not the finite-support free module.
- `G/H` uses right cosets and right multiplication.
- The sign of a connecting homomorphism depends on generator and orientation conventions.
- Preserve the course's distinction between path components `[pt,X]` and connected components `pi_0(X)`.
- Here SLPC means the course-defined semilocally path-connected condition. Do not conflate it with SLSC or ordinary local path-connectedness.
- Prerequisites are the preceding fibre-bundle long exact sequence, based higher homotopy groups, covering spaces, fundamental groupoids, quotient topology, modules, elementary matrix algebra, vector calculus, and Euler characteristic.
- Terminology candidates for controlled admission are `grup Lie`, `subgrup tertutup`, `ekuivalensi homotopi lemah`, `lingkaran Warsawa`, `karakteristik Euler`, neutral `kompleks`, `morfisma kompleks`, `gradien`, `rotor (curl)`, and `divergensi`. Existing controlled forms `topologi hasil bagi`, `graf berarah`, `simpul`, and `sisi` should remain consistent.

## Accessibility and reflow requirements

- Move both TikZ drawings from marginal notes into centered block figures; do not leave essential geometry in a narrow margin.
- Give the Warsaw-circle figure semantic text describing the oscillating sine curve, limiting vertical segment, and added closing arc.
- Give the triangle figure semantic text identifying vertices `A,B,C` and arrows `a: A -> B`, `b: B -> C`, and `c: A -> C`.
- Give all four `xymatrix` diagrams text or table equivalents that preserve every object, arrow, arrow direction, and map label.
- Reflow the six-column matrix-complex morphism and the long vector-calculus complexes to the full reader width. HTML may use an accessible horizontally scrollable math container; PDF must remain centered and legible without margin clipping.
- Convert the long marginal notes at lines 3680, 3690, 3717, and 3734--3744 into ordinary readable asides placed beside the relevant prose in source order.
- Do not communicate orientation solely by arrowhead placement or colour; repeat source and target in the surrounding text.

## Six nonduplicative solved-mastery targets

1. **Homogeneous-space bundles.** Identify the transitive actions and stabilizers that yield `SO(n+1)/SO(n) ~= S^n` and `SU(n+1)/SU(n) ~= S^(2n+1)`, and explain the fibre of each quotient map.
2. **Exact-sequence computation.** Use `SO(n) -> SO(n+1) -> S^n` to derive `pi_1(SO(n)) ~= Z/2` for `n >= 3`, show `pi_2(SO(3))=0`, and explain why the connecting map is only canonically `+/-2` before choosing generators.
3. **Weak versus ordinary homotopy equivalence.** Verify that the two-point representative map into the topologist's sine curve is a weak homotopy equivalence, then prove it cannot be a homotopy equivalence.
4. **The SLPC replacement.** Construct the morphism `slpc(f)`, prove functoriality, prove `slpc(X) -> X` is a weak homotopy equivalence, and prove that it can be a homotopy equivalence only when the path components of `X` are open.
5. **Complexes and morphisms.** Compute all cohomology groups of `0 -> Z --x4--> Z --mod2--> Z/2 -> 0`; then name the missing vertical maps in the matrix diagram and verify every square commutes.
6. **Directed-triangle coboundary.** For the oriented triangle, write the matrix of `delta: Z^V -> Z^E` in stated bases, track the `d_1 -> d_0` sign convention, and compute its kernel and cokernel.
