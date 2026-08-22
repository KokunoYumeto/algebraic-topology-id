# Unit 17 — bounded source audit and translator handoff

Date: 2026-08-22  
Authority: Roberts `Notes.tex` at commit `b947ad2e9f9e301bfe24590a9db653bc54fa1a53`  
Exact span: lines 3384–3481 inclusive; Lecture 18 starts at line 3482.

This durable file records a read-only source audit as a production handoff. It is not
a translation or a final review. The Unit 17 translator must preserve the
complete source sequence while applying the typed, logical, handedness, and
accessibility repairs below.

## Boundary and source census

The incoming boundary at line 3384 starts Lecture 17 immediately after the
essential-surjectivity proposition at lines 3376–3382. It therefore inherits the
course-SLSC hypothesis, the monodromy functor, the direct-right-action convention,
and the prior covering-space classification reductions. A short explicit recap
is needed at the standalone unit boundary because “We can say still more” is
otherwise an unresolved anaphor.

The outgoing boundary is the blank line 3481 following the proposition that
`pi_n(X,x)` is abelian for `n >= 2`. Lecture 18 begins at line 3482 and is not
part of Unit 17.

The exact 98-line span contains:

- two lemmas: uniqueness of maps into a covering space, and the
  Eckmann–Hilton argument;
- one corollary: faithfulness of the monodromy functor;
- one theorem: the equivalence
  `Cov_X -> [Pi_1(X), Set]` for course-SLSC `X`;
- one definition: the `n`th homotopy group;
- one example: the fundamental group of a topological group is abelian;
- one proposition: `pi_n(X,x)` is abelian for every `n >= 2`;
- three formal proof environments, plus an incomplete prose sketch of
  fullness rather than a proof;
- three `\[...\]` display blocks and one `align*` block containing two
  piecewise-defined concatenations;
- three substantive margin notes;
- no formal source exercise or question environment, no Xy-pic, TikZ,
  figure, external asset, label, or reference.

The sentence asking what `pi_n` should be is rhetorical rather than a source
exercise. The missing fullness proof and the suppressed higher-homotopy proof
steps must nevertheless receive solved mastery treatment.

## Non-negotiable action-handedness rules

Keep the established category `Set_G` of **right** `G`-sets throughout, with

\[
(z\mathbin{\cdot}g)\mathbin{\cdot}h=z\mathbin{\cdot}(gh),
\qquad
\varphi(z\mathbin{\cdot}g)=\varphi(z)\mathbin{\cdot}g.
\]

Consequently, the basepoint restriction in line 3405 and the fibre map in line
3414 are right-`G`-set constructions for `G = pi_1(X,x_0)`. They must not be
silently interpreted as left actions merely because the source uses bare
`pi_1(X,x_0) Set` notation.

Keep all three of the following notions visibly distinct:

1. **Direct monodromy:** right post-concatenation
   `[gamma] . g = [gamma # g]`.
2. **Inversion-converted notation for the same monodromy:** the optional left
   action `g star z = z . g^{-1}`.
3. **The genuinely different Unit 16 fibrewise/deck action:** left
   pre-concatenation `h triangleright [gamma] = [h # gamma]`. It commutes with
   direct right monodromy, and quotienting by its restricted `H`-action gives
   the right-coset fibre `H\G`.

No new left action occurs in lines 3384–3481. The fullness proof uses only the
direct right action/right-equivariance. It must not conflate that action with
the fibrewise/deck action inherited from Unit 16.

## Provisional adverse rows

The following rows are provisional and deliberately have no numerical IDs.
Allocate them only after Unit 16 has frozen its ledgers.

1. **P1 — `Notes.tex:3388–3395`.** The equations asserting that `f` and `g`
   lie over `X` are ill typed: the source writes `f o pi = p = g o pi`, although
   `pi: Z -> X` and `f,g: Y -> Z`. Use
   `pi o f = p = pi o g`. In the proof, replace the undefined
   `g(gamma(y_0))` by `g(gamma(0))`. This restores both domains and the unique
   path-lifting argument.

2. **P2 — `Notes.tex:3404–3405`.** The faithfulness proof uses the undefined
   restriction notation `f|_x` and silently assumes every path component of
   `Z_1` meets the fibre over `x_0`. Write the restriction to
   `(Z_1)_{x_0}` explicitly and invoke the already established path-lifting
   proof that each component of a cover over path-connected `X` maps
   surjectively to `X`. Cite the Unit 15 closure rather than duplicating it.

3. **P1 — `Notes.tex:3405,3414`.** Bare `pi_1(X,x_0)`-set notation can reverse
   the edition's chronological monodromy convention. Use `Set_G` for right
   `G`-sets and state
   `varphi(z . g) = varphi(z) . g` for the fibre map. This keeps fullness
   compatible with direct endpoint transport.

4. **P2 — `Notes.tex:3410–3414`.** The landmark equivalence theorem asserts
   fullness but supplies no construction or continuity proof. Close it in full.
   A concise direct proof starts from a natural transformation `eta` and defines
   `F(z) = eta_{pi_1(z)}(z)`. On path-connected evenly covered neighborhoods,
   naturality makes the induced sheet map constant in the discrete sheet
   coordinate, so `F` is continuous; it lies over `X` and induces `eta` on
   every fibre. If the source's base-fibre reduction is retained instead,
   construct endpoints by path transport and prove independence of every
   chosen path and component basepoint using right equivariance, then prove
   continuity in local trivializations.

5. **P1 — `Notes.tex:3420–3429`.** The range of `n` is not stated. The
   definition may include `n = 0` as a pointed homotopy set, but the claims
   `S^n ~= I^n / partial I^n ~= D^n / partial D^n`, the loop adjunction, and
   the group construction in this passage require `n >= 1`; the quotient
   model is false for `n = 0`. State the ranges at every relevant boundary.

6. **P2 — `Notes.tex:3429–3433`.** The group structure and functoriality are
   compressed into an assertion. Explain that coordinate concatenation passes
   to homotopy classes, that the constant class and reversal give identity and
   inverse, and that postcomposition preserves the operation. This yields
   `pi_n: Top_* -> Grp` for each fixed `n >= 1`.

7. **P1 — `Notes.tex:3435–3452`.** The stated Eckmann–Hilton hypotheses imply
   that the two operations coincide and form one associative commutative
   **monoid**, not an abelian group: no inverse hypothesis is present and no
   inverses are proved. For example, the two operations may both be addition
   on the natural numbers. Correct the lemma to the commutative-monoid
   conclusion; in the application to `pi_n`, the separately established group
   structure supplies inverses and hence yields an abelian group.

8. **P2 — `Notes.tex:3456–3457,3460–3478`.** Apply Eckmann–Hilton only after
   passing to homotopy classes. Raw loop concatenation has a unit and
   associativity only up to homotopy. State that the two coordinate operations
   descend to the relevant homotopy classes, share the constant class as unit,
   and satisfy interchange there. Also explain explicitly how the double-loop
   calculation applies to every `pi_n(X,x)` for `n >= 2`, rather than jumping
   from raw maps in `Omega_x^2 X` directly to the proposition.

9. **P1 — `Notes.tex:3470–3473`.** The second branch of
   `(f_1 #_2 f_2)(s,t)` incorrectly repeats `f_1(s,2t-1)`. It must be
   `f_2(s,2t-1)`. Verify agreement on the seam `t = 1/2` from the boundary
   condition.

10. **P3 — `Notes.tex:3414,3427,3462,3475`.** Normalize the fibre notation
    `(Z_i)_x` to `(Z_i)_{x_0}`, correct `basepint` to `basepoint`, retain the
    basepoint in `Omega_x^2 X` consistently, and replace the floating `$^2$`
    by `I^2`.

11. **P3 accessibility — `Notes.tex:3418,3427,3457`.** Move all three margin
    notes into the main reading order: the low-dimensional component-invariant
    observation, the definition of collapsing `A` in `Y/A`, and the extension
    from Lie groups to arbitrary topological groups.

12. **P3 accessibility — `Notes.tex:3430–3432,3465–3475`.** Reflow the very
    long group-operation display and the piecewise definitions. Accompany the
    MathML with a linear verbal description of first-coordinate and
    second-coordinate concatenation and an explicit four-quadrant inventory.
    No information here requires a bitmap or position-dependent diagram.

## Required proof closure for fullness

For a reader-independent closure, the preferred natural-transformation proof is:

1. Let `eta: rho_{Z_1} => rho_{Z_2}` be a natural transformation.
2. For `z in Z_1` with `pi_1(z) = x`, set `F(z) = eta_x(z)`.
3. This immediately gives `pi_2 F = pi_1` and the required restriction on
   every fibre.
4. Around any `x`, choose a path-connected evenly covered neighborhood `U`
   for both covers. For a fixed sheet of `Z_1|_U`, naturality along paths in
   `U` forces `eta_u` to send the corresponding sheet label to one fixed sheet
   label of `Z_2|_U`.
5. In the two local trivializations, `F` is therefore the identity on `U`
   together with a fixed map between discrete sheet sets, hence is continuous.
6. Uniqueness follows from faithfulness, or directly from the fact that the
   fibre components of `eta` already prescribe `F` pointwise.

This proves fullness without introducing a left action and, together with the
already proved essential surjectivity and faithfulness, completes the categorical
equivalence.

## Solved mastery requirements

The source contains no formal exercise to solve, but it leaves essential proof
and computation skills uncovered. Add bounded, fully solved checks for:

1. the uniqueness-of-lifts lemma and why it is applied componentwise when the
   domain cover is disconnected;
2. the omitted fullness construction, including right equivariance,
   well-definedness in the base-fibre version if used, and continuity;
3. the sphere–cube–disk models, their relative-homotopy correspondence, and
   the `n = 0` exception;
4. the corrected Eckmann–Hilton theorem, including a counterexample showing
   why the unital-interchange hypotheses alone do not provide inverses;
5. seam continuity and the quadrant-by-quadrant interchange identity for
   `#_1` and `#_2`;
6. the pointwise-multiplication proof for a topological group and the passage
   from double loops to abelianness of every `pi_n`, `n >= 2`.

Each solution must use the edition's chronological concatenation convention and
must distinguish equalities of raw maps from equalities of homotopy classes.

## Terminology guidance

The current terminology ledger already contains the following; do not add
duplicates: `quotient space` (0027), `homotopy class` (0077), `natural
transformation` (0083), `loop space` (0118), `endpoint-fixed homotopy` (0123),
`concatenation` (0127), `right action` (0130), `pointed homotopy class` (0132),
`faithful functor` (0149), `full functor` (0150), `functor category` (0216),
`left action` (0218), and `essentially surjective` (0233).

The following terms are provisional. Re-run an exact duplicate check after
Unit 16 freezes, then allocate IDs only for genuinely new entries:

| English | Indonesian | Domain / note |
|---|---|---|
| equivalence of categories | ekuivalensi kategori | category theory |
| higher homotopy group | grup homotopi lebih tinggi | homotopy theory |
| map of pairs | peta pasangan | topology |
| homotopy relative to `A` | homotopi relatif terhadap `A` | fix `A` throughout |
| Eckmann–Hilton argument | argumen Eckmann–Hilton | homotopy theory |
| topological group | grup topologis | topological groups |
| pointwise multiplication | perkalian titik demi titik | topological groups |
| interchange law | hukum pertukaran | algebra / homotopy theory |
| commutative monoid | monoid komutatif | algebra |
| abelian group | grup abelian | group theory |
| iterated loop space | ruang loop teriterasi | homotopy theory |

## Translator exit gate

Unit 17 is not frozen until its translation preserves all source content and
sequence; makes the right-action convention explicit; completes fullness;
corrects the Eckmann–Hilton statement and the `#_2` formula; states all ranges
of `n`; moves every margin note into reading order; supplies the solved mastery
layer above; and passes independent mathematical, structural, language,
accessibility, and deterministic build checks.
