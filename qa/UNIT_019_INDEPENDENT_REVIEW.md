# Unit 19 — independent mathematical and structural review

Date: 2026-08-23
Scope: `source/id-ID/units/unit-019-lecture-019.md` only
Authority checked: Roberts `Notes.tex:3678–3947`, commit
`b947ad2e9f9e301bfe24590a9db653bc54fa1a53`
Review mode: independent read-only review followed by a bounded post-repair
rereview.

## Initial review

The independent review began on the 56,647-byte authoring snapshot and was
restarted when a terminology normalization changed its hash. The first stable
review snapshot was 56,657 bytes, 1,853 lines, SHA-256
`35dc70834b92c7196bcd44288524431972d9e191c77e24b2719f2d01f87a13ca`.
That pass found P1 = 0, P2 = 2, and P3 = 4:

1. The draft called `gH` a right coset. It is a left coset, although it is an
   orbit of the right `H`-action. The unit and source audit now distinguish
   those two handedness statements.
2. The first homogeneous-space mastery proof established a bijection but
   merely invoked the homeomorphism. It now factors the continuous orbit map
   through the quotient and applies the compact-domain/Hausdorff-codomain
   criterion for `SO(n+1)` and `SU(n+1)`.
3. The Hopf quotient `SU(2)/U(1) ≅ S²` is now explicitly marked as a standard
   external fact used without proof.
4. The substantive source sentence explaining that the exact sequence also
   determines induced maps has been restored in source order.
5. The unnatural phrase for trivial homotopy groups in the Warsaw-circle
   example was replaced by natural Indonesian.
6. A line break that produced `Serat- serat` was removed.

## Final verdict

Final snapshot: 57,277 bytes, 1,865 lines, SHA-256
`ba34773d63e4dc70fccdf4fa19fbdc8a397062a4bc359978f3261a70ff64f98c`.

- P1: 0
- P2: 0
- P3: 0
- Pandoc: all 78 unique textual ID declarations are structural IDs; parsing
  passes without warnings.
- Source closure: all six definitions, twelve examples, two lemmas, one
  remark, one source proof/exercise, thirteen margins, four Xy-pic semantic
  equivalents, two TikZ semantic equivalents, and two source labels remain in
  source order.
- Mastery closure: six prompts, six hints, and six complete solutions.
- Delicate conventions: `gH` is a left coset formed as a right-action orbit;
  the connecting map is `×(±2)` before generator choices; SLPC retains the
  course meaning; complexes use cohomological grading; de Rham exactness is
  correctly scoped; and graph coboundaries use target minus source.
- Process provenance: the exact model identification is present and source,
  author, human-direction, licence, and non-endorsement credits remain intact.
- Boundary: no Lecture 20 content is present; the next source line is 3948.

Unit 19 passes the independent-review gate.
