# Unit 18 — independent mathematical and structural review

Date: 2026-08-22
Scope: `source/id-ID/units/unit-018-lecture-018.md` only
Authority checked: Roberts `Notes.tex:3482–3677`, commit
`b947ad2e9f9e301bfe24590a9db653bc54fa1a53`
Review mode: independent read-only review followed by a bounded post-repair
rereview.

## Initial review

Initial snapshot: 42,320 bytes, 1,606 lines, SHA-256
`9123e5078e3fa3b178da5f522dc8273b9feec66344e16b4aae48b459f38aadc2`.
The initial review found P1 = 1, P2 = 5, and P3 = 2:

1. The solution for the antipodal cover incorrectly inferred injectivity of
   the pointed map from pointed-set exactness. Pointed-set exactness supplies
   only the preimage of the basepoint. The repaired proof now uses the right
   action and `H\backslash G`: here
   `H=q_*\pi_1(S^m)=1` and `H\backslash G\cong\{+,-\}`, so the underlying set
   of `G=\pi_1(\mathbb{RP}^m)` has two elements.
2. Five source-margin IDs were literal Pandoc text rather than structural
   anchors. Each margin is now an attributed fenced Div.
3. The covering-classification qualification was initially vague, then was
   briefly over-narrowed by adding global path connectedness. The final prose
   states the course-SLSC hypothesis and explicitly treats a disconnected
   space componentwise.
4. The connecting-map explanation chose a lift without explaining its
   existence. It now invokes homotopy lifting for a fibre bundle and lifts a
   contraction of the disk relative to the chosen boundary basepoint.
5. Mastery 18.1 omitted canonical independence of transport. Its prompt,
   hint, and complete solution now compare endpoint-preserving homotopies of
   paths in a simply connected path component.
6. The two lemmas, homotopy-invariance proposition, and first three mastery
   items left the range of `n` implicit. Each formal use now states
   `n\geq1`.
7. Reader terminology was aligned with the admitted glossary: `modul atas
   R`, first-occurrence `fibre bundle`, `garis projektif kompleks`,
   `koordinat homogen`, explicit complex/quaternionic Hopf qualifiers, and
   `homotopi yang mempertahankan titik ujung`.
8. A four-term quaternionic-Hopf fragment was called five terms. The final
   text calls it the relevant fragment.

The rereview also confirmed that the Hopf quotient is written using the image
of the displayed injection, rather than treating the source group as a
literal subgroup without identification.

## Final verdict

Final snapshot: 44,415 bytes, 1,663 lines, SHA-256
`9d0564f6a074441332e42755d46d9a0e858189a5ff4d8b5be52b1def12532598`.

- P1: 0
- P2: 0
- P3: 0
- Pandoc: all 67 unique textual ID declarations are structural IDs; no
  source-margin ID leaks as visible text.
- Source closure: two propositions, two lemmas, one theorem, two definitions,
  ten active examples, six remarks, and all five margins are preserved.
- Mastery closure: six prompts, six hints, and six complete solutions.
- Boundary: no Lecture 19 content is present; the next source line is 3678.

Unit 18 passes the independent-review gate.
