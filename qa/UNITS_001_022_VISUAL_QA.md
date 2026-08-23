# Units 001-022 cumulative visual QA

Status: **PASS** for the verified cumulative checkpoint.

The final deterministic reader is 261 A4 pages, 1,728,316 bytes, SHA-256
`5dabcbdc98fdc7203ca2fe4f42aff86b9e3cb761136f676e0dd43b350768fb77`.
Pandoc 3.9.0.2 and MiKTeX pdfTeX 1.40.29 produced byte-identical PDFs in
two independent passes under `SOURCE_DATE_EPOCH=1787443200`.

## Representative render inspection

Poppler `pdftoppm` rendered the following final-PDF pages at 120 dpi. Each PNG
was inspected at original render resolution:

| PDF page | Coverage | Render SHA-256 |
|---:|---|---|
| 1 | Title, expanded subtitle, authorship, and opening contents | `b9ef759e10034adcd5be7bb2e1110848cded931ab5c5c85717b6486efdad6a55` |
| 123 | Mid-reader prose, displays, hierarchy, and page furniture | `6c0f1eef79bb23caed2ae224d4da4391efa146f5c40a0f67cc976d44329baec4` |
| 246 | Late Unit 21 mastery solution, long formulas, and page flow | `a3ec87c6d8b239d9a948c84486a77bfb0aacc85b2f5bfce6e482c3780cff6023` |
| 247 | Unit 21/22 boundary, Unit 22 provenance, and opening definition | `50b45a3581bbbf66859b8b8ac308f07e68cbb2ae9d997cf39637295de76eba22` |
| 249 | Infinite-cylinder incidence tables and centered semantic Diagram 22.1 | `864e8568bc4e5f31026471c471317aa6972ba33d29e0de7e57faad7459b9150d` |
| 250 | Centered quotient square, proof close, and surrounding prose | `3712876ce153ea48dd28da27ea84e908832027113f0f65e0634c0894cb375e1d` |
| 253 | Centered skeleton triangle and naturality square, with long indexed formulas | `0b42c789fce17e4e1538fdd673cda32dc4fd122d3da896c0141b06da02187818` |
| 258 | Unit 22 source audit and first problem/hint/full-solution surface | `52a8f12b85c3875a6704d5ca482ce40817154e9d60d44f0bc5e80ccb41a481f1` |
| 260 | Mastery 22.4 and 22.5 with displays, sums, and solution prose | `a1904f820363bfd45711c345394d1694e6b3d3193d9a2b8f7243307ca7536c84` |
| 261 | Mastery 22.6, full solution, and terminal Unit 23 boundary | `ae000306fe7330a6fc17d741b348ee1ecab3f88b987ef1bcf9984a24065e08c8` |

No inspected page has clipping, overlap, broken glyphs, unreadable formulas,
positional-figure dependence, or margin/page-number collision. Page 247
continues the final Unit 21 solution before presenting its boundary and the
Unit 22 opening on the same page; this is coherent continuous flow, not a
missing-page defect. Page 261 closes cleanly with the complete safe source
cursor to Unit 23.

## Builder defects found and repaired

The first builder draft contained a one-character typo in the frozen Unit 17
SHA-256 literal. The source-identity gate failed before producing a candidate.
The literal was corrected to the previously frozen hash; no unit source or
earlier artifact changed.

The first successful HTML candidate, 3,516,753 bytes and SHA-256
`a7d3b832c0135398a5711eb1335d67bc90c465f32c657e637a8aca69129439f7`,
contained three literal-TeX fallbacks for Unit 22 semantic diagrams. Pandoc's
MathML reader did not admit `\big\downarrow` or
`\lhook\joinrel\longrightarrow` in those arrays. The new builder normalizes
only those presentation macros, only in the transient HTML input, to equivalent
supported arrows. It now treats Pandoc HTML warnings as fatal and rejects any
remaining raw-TeX math fallback. The final HTML has 8,701 MathML nodes and zero
fallbacks. Frozen Markdown and PDF input remain unchanged; the PDF hash was
unchanged by this HTML-only repair.

## PDF and HTML verification

- PDF metadata: title `Topologi Aljabar - Unit 1-22`, A4, 261 pages,
  `/Lang=id-ID`, no encryption/forms/widgets/JavaScript, no suspect flag, and
  zero rotation on every page.
- Fonts: 25 Poppler rows; every row is embedded, subset, and has a Unicode map.
- Structural tagging: the PDF is honestly **untagged**; the reflowable,
  self-contained HTML is the accessible primary structure.
- HTML: 1,167 unique DOM IDs with no duplicates, 264 resolving fragment links,
  8,701 MathML nodes, 55 semantic figures, all 75 Unit 22 stable IDs, and zero
  external runtime script or stylesheet dependencies.
- Reflow: the HTML reading column is centered at `min(100%, 72rem)`, figures
  center their semantic content, wide tables and display mathematics can scroll,
  links wrap, and the 700-pixel mobile rule removes the desktop frame.
- Privacy: the cumulative HTML gate and the extracted new-PDF span on pages
  247-261 contain no credential markers, placeholders, or absolute local user
  paths. Extracted text contains no stray empty TeX group before `Notes.tex`.
- Process provenance remains exactly **OpenAI Codex gpt-5.6-sol, Ultra**;
  source authorship, human direction, CC BY 4.0, and non-endorsement remain
  intact.

This is representative visual QA, not a claim that every one of the 261 pages
was manually inspected.
