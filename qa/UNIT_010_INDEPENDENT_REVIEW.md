# Unit 010 independent review

Date: 2026-08-22

Verdict: **PASS — P1 = 0, P2 = 0, P3 = 0**

## Frozen scope

- Edition source: `source/id-ID/units/unit-010-lecture-010.md`
- Size: 26,432 bytes; 934 lines
- SHA-256: `e1c6ef961ae2266db86baec6d701dd659a1bf78bdd3601cf5b1c6515bc7d0310`
- Upstream comparison: Roberts `Notes.tex:2094-2272` at commit `b947ad2e9f9e301bfe24590a9db653bc54fa1a53`; line 2273 was used only to confirm the Lecture 11 boundary.

## Review disposition

An independent source-and-mathematics review checked exact semantic closure, orbit-stabilizer maps for both action conventions, subgroup conjugacy under a basepoint change, endpoint-operator order, the full circle-group calculation, restricted fundamental groupoids, component decompositions, the wedge universal property, and the three-sheeted covering calculation. It also checked all six marginal elements in reading order, the source TikZ graph against the frozen upstream PDF, Indonesian terminology, stable identifiers, fence and display-math balance, and source-versus-edition labeling.

The edition uses `H\G` and `Hg -> z dot g` for direct right monodromy and uses `G/H` only after conversion by inversion to the corresponding left action. It keeps `H=pi_*(pi_1(Z,z))`, derives the correct conjugate stabilizers, and distinguishes the right endpoint antihomomorphism from the ordinary representation `lambda(g)=R_(g^-1)`. It repairs the source's changed point variable, omitted `pi_*`, unrestricted groupoid object variables, missing component hypothesis, mistaken `join`, ill-typed wedge composites, malformed wedge formula, missing command slash, and incomplete reduced-word conditions. The diagram is independently reflowed with the exact six directed edge labels verified against the source rendering.

The final current-byte recheck found no remaining P1, P2, or P3 issue. All 26 `o012-rbt-l10-*` stable IDs are unique; the source alias `cor:fibre_of_univ_cov_space` is preserved separately. All 15 semantic fences and all 142 display delimiters balance. Every upstream semantic environment is present: one continued proof, two corollaries, two examples, one theorem, one definition, and three proof environments total. Five edition-original mastery checks have complete solutions.

During review, an incorrectly formed Pandoc output argument transiently truncated this draft. The translator immediately restored the complete current version from its active production buffer; the independent reviewer then reread all 934 restored lines and recomputed the exact identity above. No other lane file was affected, and all subsequent parsing and structural checks used read-only stdout pipelines.
