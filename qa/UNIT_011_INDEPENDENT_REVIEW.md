# Unit 011 independent review

Date: 2026-08-22

Verdict: **PASS — P1 = 0, P2 = 0, P3 = 0**

## Frozen scope

- Edition source: `source/id-ID/units/unit-011-lecture-011.md`
- Size: 28,465 bytes; 959 lines
- SHA-256: `1cdbe0cae239a4e60a72f25c8814c2e3b5ec26b9119da03624bda7f3ff1ae127`
- Upstream comparison: Roberts `Notes.tex:2273-2494` at commit `b947ad2e9f9e301bfe24590a9db653bc54fa1a53`; line 2495 was used only to confirm the Lecture 12 boundary.

## Source closure

The exact upstream span contains three definitions, five examples, one theorem, one remark, and the first part of one proof that deliberately crosses the lecture boundary. It contains nine Xy-pic matrices, two TikZ figures, six margin elements, and no source exercise, hint, solution, label, or cross-reference. The edition preserves that complete census and sequence, exposes all eleven diagrams as semantic figures, incorporates every margin element into the reading order, and stops honestly before the Lecture 12 continuation.

The edition adds three clearly identified mastery checks with complete solutions. They verify the universal properties of free groups and free products, the topological and vector-space pushouts, subdivision independence, and the explicit endpoint-fixed homotopy between the two square-boundary paths. Added material is separated from the Roberts source and remains under CC BY 4.0.

## Mathematical disposition

The review independently checked the free-product presentation and mapping property, every pushout example, the groupoid pushout into `B Z`, the groupoid Seifert--van Kamp statement, the object map, local path map, Lebesgue-number subdivision, common-refinement argument, and the square-boundary homotopy. It also checked the lane's convention that algebraic juxtaposition records chronological left-to-right composition while `\circ` has its standard right-to-left meaning.

The edition repairs the source's reversed free-product composites, raw-word multiplication, swapped presentation prose, raw-path inputs to `F_1` and `G_1`, and premature reuse of `K_1` before descent. It names the provisional raw-path function `\widetilde K_1`, states the exact endpoint-preserving reparameterisation condition, supplies the compactness/Lebesgue-number step, and gives a direct universal-property proof for the groupoid example. The two position-dependent square pictures are replaced by explicit paths `p_0`, `p_1`, and the convex endpoint-fixed homotopy `P(s,u)`.

The proof boundary is not overstated. Unit 12 must still prove global homotopy invariance, descend `\widetilde K_1` to `K_1`, verify the identity and composition laws, show the restrictions are `F` and `G`, and prove the source-implicit uniqueness of the resulting universal functor. These obligations are stated at the end of Unit 11 and recorded in the adverse ledger.

## Structural checks

The current-byte recheck found 39 stable identifiers in the Unit 11 namespace, all unique: the root identifier `o012-rbt-l11` plus 38 suffixed identifiers. It also found 25 balanced fenced-div pairs and 140 balanced display-math delimiter lines. Pandoc parsed the complete file to both its native representation and HTML with MathML through read-only stdout pipelines without warning or error. The independent source-and-mathematics review found no remaining P1, P2, or P3 issue.
