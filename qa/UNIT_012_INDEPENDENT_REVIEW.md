# Unit 012 independent review

Date: 2026-08-22

Verdict: **PASS — P1 = 0, P2 = 0, P3 = 0**

## Frozen scope

- Edition source: `source/id-ID/units/unit-012-lecture-012.md`
- Size: 32,850 bytes; 1,024 lines
- SHA-256: `429831df4a5600c59351516915fb787cd73402d8c11c411869210dbf8aaa7ada`
- Upstream comparison: Roberts `Notes.tex:2495-2726` at commit `b947ad2e9f9e301bfe24590a9db653bc54fa1a53`; line 2727 was used only to confirm the Lecture 13 boundary.

## Source closure

The exact upstream span contains the inherited tail of the groupoid Seifert--van Kampen proof; the construction of the category of commutative squares; one definition; four examples, two of them inline; two lemmas; one theorem; one corollary; five proof units; one source exercise; one TikZ grid; six Xy-pic diagrams; six margin notes; and two source labels. The edition preserves the complete sequence and both labels, represents all seven diagrams semantically, moves every margin qualification into reading order, and closes precisely before Lecture 13.

Four clearly identified mastery checks have complete solutions. They include the source exercise proving that a retract of a pushout square is a pushout and also verify the cell-swap descent, functor laws and uniqueness, the fundamental-groupoid retraction, cube coherence, the full-subcategory argument, and the sphere application. Added material is separated from the Roberts source and remains under CC BY 4.0.

## Mathematical disposition

The review checked the two-dimensional Lebesgue-number construction, finite one-cell interchange, descent from `\widetilde K_1` to `K_1`, identity and composition laws, restrictions to `F` and `G`, and the uniqueness of the universal functor. The argument is noncircular: every cell equality is obtained inside one member of the cover before global homotopy invariance is concluded.

The categorical portion now distinguishes four unrelated vertexwise splittings from a genuine retraction in `\mathcal C^\square`. It constructs the fundamental-groupoid retraction by

```
R([gamma: x -> y]) = [bar(eta_x) # gamma # eta_y],
```

checks representatives, identities, composition, and the retraction equation, and chooses paths coherently by treating the intersection first. The source's exercise-only retract lemma receives a complete universal-property proof. The full-subcategory lemma is repaired so the universal arrow is first constructed in the ambient category and then belongs to the full subcategory by fullness. The fully faithful one-object groupoid functor `B` is explicit.

The sphere example states every path-connectedness hypothesis, verifies that the two open sets cover, derives the trivial pushout for `n > 1`, and correctly explains that only the one-object group version fails for `n = 1`; the groupoid theorem remains available. The lane's chronological algebraic product convention and standard right-to-left `\circ` convention are used consistently throughout.

## Structural checks

The final current-byte recheck found 37 stable identifiers in the Unit 12 namespace, all unique; 24 balanced fenced-div pairs; and 130 balanced display-math delimiter lines. Pandoc parsed the complete file through both native and HTML-with-MathML read-only stdout pipelines with warnings treated as errors. The independent source-and-mathematics review found no remaining P1, P2, or P3 issue.
