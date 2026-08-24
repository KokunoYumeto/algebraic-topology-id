# Unit 024 — independent mathematical and structural review

Date: 2026-08-24

## Review scope

This review independently compared
`source/id-ID/units/unit-024-lecture-024.md` and
`qa/UNIT_024_SOURCE_AUDIT.md` against the frozen Roberts authority
`Notes.tex:5113–5369` at commit
`b947ad2e9f9e301bfe24590a9db653bc54fa1a53`. It checked the exact boundary,
source order and census, the example resumed from Unit 23, all source labels
and references, every displayed map, the two deterministic source corrections,
all edition proof closures, all six mastery solutions, semantic diagram
reflows, Indonesian terminology, stable structure, rights, provenance, and
the terminal cursor.

## Final snapshot and verdict

Final reader snapshot: **43,085 bytes, 1,156 LF lines, SHA-256
`993ad0c3493caff6bd15ab2bcf435f6cbb1f49ed9a1e11bc1009d649ae2d3647`**.
Source-audit snapshot: **4,384 bytes, 78 LF lines, SHA-256
`0aeb3beae1b52099e97538083ef349590cca62b473ff1455b8c1fdaffbe2ba6b`**.

- P1: 0
- P2: 0
- P3: 0
- The active source span is exactly 257 physical lines and 12,837
  LF-normalized UTF-8 bytes, SHA-256
  `b2128930a56a0a8c04c327a397e72e21b215ffe742bb684e8dd166f0e04b0aea`.
  Line 5113 resumes the example opened at line 5076, line 5121 closes it, and
  line 5370 begins Lecture 25 and remains excluded.
- All 60 reader stable IDs are unique. Ten identified headings and 50 balanced
  fenced semantic objects preserve the exact structural inventory: one
  continued example, one definition, one theorem, three lemmas, one remark,
  six proof blocks, three semantic figures, seven source margins, eight audit
  records, six problem/hint/full-solution triples, and one terminal boundary.

### Corrected pre-admission evidence defect

The initial independent review identified `UNIT024-AUDIT-P3-001`: source-audit
line 38 had attributed the malformed Mayer--Vietoris term to `Notes.tex:5182`,
although the exact authority locus is `Notes.tex:5173` and line 5182 begins the
Snake Lemma. The owning task corrected that locator from 5182 to 5173 before
admission without changing the reader. This final review binds the corrected
audit identity above; the defect is closed and is retained here as transparent
history rather than counted as an open finding.

## Mathematical fidelity

- Restriction is correctly proved to be a degreewise-surjective cochain map;
  its kernel is differential-stable and gives the relative cochain complex.
  The edition correctly warns that degreewise extension by zero generally is
  not a cochain-map splitting and supplies a valid `Delta[1]` counterexample.
- The degreewise-kernel lemma types the restricted differential and proves it
  squares to zero.
- The algebraic Mayer–Vietoris sequence restores the malformed source term to
  `H^{k+1}(B_bullet)` and keeps every induced-map direction correct.
- The lower-right object in the source Snake diagram is correctly repaired
  from `C` to `C'`. Both commutative squares and every induced kernel/cokernel
  map are typed. The proof constructs the connector, proves lift-independence
  and `R`-linearity, and proves exactness at all four internal terms—thereby
  closing all six obligations enumerated by the source.
- The setup lemma proves that the vertical quotient-to-cycle maps are well
  defined, land in the stated kernels, and commute; it proves precisely the
  top-row and bottom-row exactness required by the Snake Lemma.
- The theorem proof gives canonical kernel/cokernel identifications with
  `H^k` and `H^{k+1}`, identifies the induced maps, and justifies both splicing
  across consecutive degrees and naturality of the resulting long exact
  sequence.
- Each of the six edition-original exercises has one hint and a complete,
  correct solution covering relative cochains, kernel complexes, connector
  construction, Snake exactness and linearity, setup exactness, and
  splicing/naturality.

## Source topology, language, and rendering

The four source aliases—`thm:alg_Mayer-Vietoris`, `snakeLemma`,
`fig:snake_lemma`, and `lemma:setup_for_algMV`—are preserved once each, and
their four source references are represented by stable reader links. The two
links back to `o012-rbt-l23-exa-002` deliberately target the preceding unit;
all same-file fragments resolve.

Both Xy-pic diagrams and the TikZ snake figure are replaced by centered
semantic arrow data and explanatory prose. All seven margins occur in reading
order; no claim depends on color, geometry, or margin placement. No raw
Xy-pic, TikZ, margin, float-positioning, or drawing command survives.
Terminology consistently uses the admitted id-ID forms `fungtor`, `morfisma`,
`kosiklus`, `kobatas`, `kernel`, `kokernel`, `barisan eksak pendek`, `barisan
eksak panjang`, `aljabar homologis`, `Lema Ular`, and `pengejaran diagram`.

Pandoc 3.9.0.2 converts the frozen reader to standalone HTML5 with native
MathML, warnings fatal, at exit zero. The result contains all 60 reader IDs,
502 MathML nodes, no duplicate DOM ID, no raw-TeX math fallback, and no runtime
script or stylesheet dependency.

## Attribution and process transparency

The unit retains David Michael Roberts's source credit, exact commit and line
span, CC BY 4.0, the independent/non-endorsement statement, human-contributor
credit, and the exact process note **OpenAI Codex gpt-5.6-sol, Ultra**. No
upstream contact occurred. The reader has no mathematical or structural
finding, and the corrected frozen evidence package is **PASS**. This review
does not itself advance the source cursor, admit the backend append, or claim
publication.
