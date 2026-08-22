# Unit 16 — bounded source audit and translator handoff

Date: 2026-08-22  
Authority: Roberts `Notes.tex` at commit `b947ad2e9f9e301bfe24590a9db653bc54fa1a53`  
Exact span: lines 3287–3383 inclusive; Lecture 17 starts at line 3384.

This audit is a production handoff, not a translation or final review. Unit 16 must
preserve the complete source sequence while repairing the typed and topological
defects below. It must not copy prose from the comparison reference.

## Source census

The span contains the inline Lecture 16 marker; one definition (fibrewise action);
one quotient-cover proposition with proof; one equivariance lemma whose proof is
only `Exercise`; one two-part problem inventory; one path-class-space construction;
one universal-cover proposition with proof; and one essential-surjectivity
proposition. It contains two Xy-pic triangles (one in a margin), four margin notes,
the local-trivialisation display, the final functor display, and no formal exercise
environment.

## Required P1 repairs

1. **Handedness and quotient side (`3287`, `3305`, `3308`, `3374`).** Direct
   chronological monodromy is a right action. The universal fibre is the right
   torsor (G=\pi_1(X,x_0)), and the cover attached to (H\leq G) has fibre
   (H\backslash G), not (G/H). The universal-cover construction also has a
   separate commuting **left** fibrewise action
   (h\cdot[\gamma]=[h\gamma]). Quotient by that left (H)-action and write
   (H\backslash\widetilde X). State explicitly that its quotient map is
   equivariant for the commuting right monodromy action.

2. **Wrong topology/proof route (`3324–3359`).** The source calls
   (P_{x_0}X/{\sim}) a quotient space and then cites Hatcher for a proof that in
   fact defines a different topology. Hatcher’s official text, pages 64–65,
   equips the set of endpoint-fixed path classes with basis sets
   (U_{[\gamma]}=\{[\gamma\eta]:\eta\text{ is a path in }U\}\), for
   path-connected open (U) whose fundamental group maps trivially to that of
   (X): <https://pi.math.cornell.edu/~hatcher/AT/AT%2B.pdf>. The edition must
   define and prove this covering-basis topology directly. It must not claim,
   without a separate proof, that it is the compact-open quotient topology.

3. **Nonexistent continuous path selector (`3343–3350`).** Course-SLSC does not
   supply one continuously varying choice (x'\mapsto\eta_{x'}). Replace that
   argument by the basis-set proof: endpoint projection maps each
   (U_{[\gamma]}) bijectively and homeomorphically to (U), and these sheets
   partition the inverse image of (U).

4. **Missing connectedness (`3337`).** Restate that (X) is path-connected and
   course-SLSC. Without path-connectedness, paths beginning at (x_0) cover only
   its component. The later componentwise conclusion may then handle general
   course-SLSC (X).

5. **Conflated actions in simple-connectivity proof (`3363–3371`).** The free
   left fibrewise action and the right monodromy stabilizer are different actions.
   Prove simple connectivity without conflating them: construct the lift
   (t\mapsto[\gamma_t]), use the closed-lift criterion to show the image of
   (p_*\) is trivial, then use injectivity of (p_*\) for a covering.

6. **Wrong subgroup conclusion (`3374`).** The source says
   (\pi_1(X^{(1)},*)=H), although (X^{(1)}) was just proved simply connected.
   The correct statement is
   
   \[
   (p_H)_*\pi_1(H\backslash\widetilde X,H[c_{x_0}])=H
   \leq\pi_1(X,x_0).
   \]

7. **Quotient-cover proposition (`3295–3303`).** Treat the acting group as
   discrete and the action as a left action by covering automorphisms. Use a
   path-connected evenly covered neighbourhood (available under the standing
   course-SLSC hypothesis), show every group element permutes whole sheets, and
   identify the quotient locally with (U\times(G\backslash F)). Do not leave
   the restriction/quotient identification to “Assignment 4.”

## P2 proof closures

- Prove the source’s exercise: the quotient map on every fibre commutes with
  right path transport because left prefixing and right concatenation commute.
- Prove the basis axioms, sheet partition, endpoint homeomorphism, continuity of
  the left action, path connectedness of the constructed cover, and simple
  connectivity in reading order; the source’s “details later” is not a proof.
- Complete essential surjectivity rather than saying merely “work backwards”:
  decompose a right (G)-set (S) into orbits, choose representatives (s_i),
  put (H_i=\operatorname{Stab}(s_i)), build
  \(\bigsqcup_i H_i\backslash\widetilde X\), and exhibit the fibre isomorphism
  \(H_i g\mapsto s_i\cdot g\). Then repeat independently over every open path
  component of a general course-SLSC base.
- Keep the logical claim exact: this unit proves essential surjectivity of the
  monodromy functor, not full faithfulness or categorical equivalence.

## Deterministic and accessibility repairs

Repair `equvariant`, `path lifing`, `We have have`, and `we can the take`; make all
maps and basepoints typed; distinguish the universal cover from its subgroup
quotient. Reflow both Xy-pic triangles with linear arrow inventories and commuting
equations. Move all four margins into the main reading sequence: quotient triangle,
constant-path notation, the source’s Hatcher/deferred-proof note, and the explicit
path (s\mapsto(t\mapsto\gamma(st))). No relationship may depend on placement.

## Bounded mastery layer

Supply complete solutions for: (1) quotient of a cover by a fibrewise left action;
(2) commuting left quotient/right monodromy; (3) the covering-basis axioms and
local sheets; (4) the lifted-path and simple-connectivity proof; (5) subgroup
realisation and the (p_*\)-image; and (6) orbitwise/componentwise essential
surjectivity. Do not introduce deck-transformation classification or full
faithfulness from later lectures.

