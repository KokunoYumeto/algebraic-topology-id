# Unit 030 — independent mathematical and structural review

Date: 2026-08-24

## Review scope

This review independently compared
`source/id-ID/units/unit-030-lecture-030.md` and
`qa/UNIT_030_SOURCE_AUDIT.md` against the frozen Roberts authority
`Notes.tex:6271–6368` at commit
`b947ad2e9f9e301bfe24590a9db653bc54fa1a53`. It checked the exact terminal
source boundary and literal census; every theorem, definition, lemma,
corollary, proof, formula, margin, side note, figure, label, and reference;
the repaired cohomological arrows, degree calculations, and the `n=0` cases;
all six exercise/hint/full-solution triples; natural Indonesian terminology;
stable-ID uniqueness and fenced structure; native-MathML conversion and link
resolution; attribution, rights, non-endorsement, human credit, and model
provenance. No backend, ledger, build, control, Git, publication, upstream, or
other unit was changed by this review.

## Final snapshot and fail-closed verdict

Final reader snapshot: **23,008 bytes, 729 LF lines, SHA-256
`88da8cf71d0f81328bdd65b0dea7d54c48655ed8836e230eaed821796b61b08d`**.
Source-audit snapshot: **7,214 bytes, 128 LF lines, SHA-256
`177c4306e5db636e0294e85278904c186099d069f209474a472d2615b0d5a4cf`**.

- P1: 0
- P2: 0
- P3: 0
- Overall status: **PASS**.
- The authority span is exactly 98 physical lines and 8,290 LF-normalized
  UTF-8 bytes, SHA-256
  `c522b5ec0ba7d4c938be6588a070be648263d841e1db4f9905c9b388619b64b1`.
  It begins with the embedded Lecture 30 marker on line 6271 and ends with
  `\end{document}` on line 6368. The file has no later source line; the exact
  terminal cursor is EOF after line 6368, nominal position 6369.
- All 47 reader stable IDs are unique. Seven identified headings and 40
  balanced fenced semantic objects preserve the reader topology: four asides,
  one boundary, one corollary, two definitions, six exercises, one semantic
  figure, six hints, one lemma, four proofs, one proposition, one remark, six
  solutions, three source-audit blocks, and three theorems.

### Resolved pre-admission finding

One defect found during independent review was corrected narrowly before this
final verdict. It remains recorded as transparent history and is no longer an
open finding.

1. `UNIT030-ED-P2-001` — **P2**, final reader line 639. The solution deriving
   multiplicativity of degree wrote the scalar action as `ed,u`. That comma
   made the displayed formula syntactically ambiguous and did not express the
   intended product on the generator. It now reads
   `(g composed with f)^*(u)=f^*(g^*(u))=f^*(eu)=(ed)u`, which agrees with
   contravariance and the separately stated result
   `Deg(g composed with f)=Deg(g)Deg(f)`. No map direction, source boundary,
   identifier, or mathematical conclusion changed.
2. `UNIT030-QA-P3-002` — **P3**, evidence-only. The initial census omitted the
   unnumbered notice heading and the lecture-root heading, so it reported 46
   IDs and five headings although the immutable reader contains 47 explicit
   unique IDs: seven identified headings plus 40 fenced semantic objects.
   The final review and QA now bind all 47 IDs, and a fresh Pandoc render
   preserves every one without duplication. The reader itself did not change.

## Source closure and mathematical fidelity

The literal source census is exact: one lecture marker, three theorem
environments, one formal definition, one inline definition, one lemma, one
corollary, one remark, three proof environments, one four-item enumeration,
six margin notes, one side note, one TikZ picture, one label, and one
cross-reference. There is no formal source exercise or question, Xy-pic,
external graphic, citation command, `input`, or `include`. Both textual
references to Hatcher are retained without converting them into false formal
citations. All reader material occurs in the same conceptual order, and the
single fixed-canvas TikZ construction is reflowed as an explicit reading-order
geometric description with all three points and the directed ray preserved.

- The Brouwer proof treats `n=0` directly and assumes `n>=1` before using
  `S^(n-1)`. Under the contradiction hypothesis, `d=x-f(x)` is nonzero. The
  displayed quadratic formula gives the unique outward intersection, is
  continuous on the free-map domain, has parameter at least one, and restricts
  to the identity on the boundary.
- For `i:S^(n-1)->D^n` and `g_f:D^n->S^(n-1)`, contravariance is correctly
  represented by `g_f^*` followed by `i^*`. Reduced cohomology makes the middle
  group zero also when `n=1`; ordinary degree-zero cohomology would not. The
  composite is correctly identified with `(g_f composed with i)^*=id`, giving
  the contradiction.
- The fundamental-theorem-of-algebra proof replaces the source's informal
  approximation by the quantitative leading-term bound
  `sum_(j<n)|a_j|R^j<R^n`. The reverse triangle inequality proves that the
  straight-line homotopy avoids zero, while radial contraction in the domain
  would null-homotope the same winding class if the polynomial had no root.
  All endpoints, codomains, and the lifted winding change `2 pi i n` are
  consistent.
- The normalized tangent field is correctly a map into the ambient unit
  sphere, not an identification of each fibre's unit sphere with `S^n`. The
  condition `v(x) dot x=0` and unit length make the cosine-sine homotopy stay
  on `S^n`.
- Degree is defined with reduced cohomology, so the definition and antipodal
  calculation remain valid for `S^0`. The non-surjective, identity,
  multiplicative, and homotopy-invariant properties have the right hypotheses
  and directions. The antipodal map is the composite of all `n+1` coordinate
  reflections, hence has degree `(-1)^(n+1)`.
- The even-dimensional obstruction includes `n=0`, both cohomologically and
  geometrically. Conversely, for `n=2k-1` with `k>=1`, the repaired paired
  coordinate formula ends in `x_(2k-1)`, has dot product zero and norm one,
  and therefore supplies a continuous nonvanishing tangent field.

The audit accurately records the source's fixed-point example error, omitted
free-map hypothesis, reversed cohomology labels, unreduced `n=1` and `n=0`
issues, informal polynomial estimate, fibre/ambient-sphere conflation,
coordinate typo, incorrect dot product, and textual typographical errors. The
edition's corrections are explicit and do not misattribute them to Roberts.
The source deliberately omits a proof of the reflection-degree lemma; the
reader says so, preserves the Hatcher provenance, and supplies only the
corollary proof that follows from that lemma.

All six mastery items have exactly one hint and one complete solution. They
cover the explicit Brouwer retraction, reduced degree-zero cohomology and arrow
direction, the large-circle polynomial argument, multiplicativity and the
antipodal degree, the even-dimensional obstruction including `n=0`, and the
odd-dimensional field. The formulas and conclusions in every solution were
checked against their prompts.

## Terminology, accessibility, rights, and provenance

The reader consistently uses the admitted forms `sfera`, `fungsi`, `fungtor`,
and natural related expressions. No rejected `bola`, English `sphere`,
`functor`, or source typo `funtor` remains. Terms such as `fungsi-diri`,
`kohomologi tereduksi`, `medan vektor tangen`, `hasil kali titik`, `derajat`,
`peta antipodal`, and `homomorfisma monoid` are mathematically unambiguous and
natural in context.

Pandoc 3.9.0.2 converts the final reader to standalone HTML5 with native
MathML and warnings fatal at exit zero. The output contains 268 MathML nodes,
all 47 reader IDs, no missing or duplicate reader ID, no raw TeX AST node, no
runtime script, and no external stylesheet. The semantic figure and all source
notes are in reading order. The three public links—the exact pinned source
span, official repository, and CC BY 4.0 deed—each returned HTTP 200 during
this review.

The unit retains David Michael Roberts's source credit, exact commit and line
span, CC BY 4.0, an explicit independent/non-endorsement statement, preserved
human-contributor credit, and the exact model note **OpenAI Codex
gpt-5.6-sol, Ultra**. No private path, credential marker, placeholder, or claim
of official status is present. This review does not advance the cursor, claim
backend admission, or claim publication. The corrected final evidence package
is **PASS**.
