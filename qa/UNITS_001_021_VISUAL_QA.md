# Units 001-021 cumulative visual QA

Status: **PASS** for the verified cumulative checkpoint.

The final deterministic reader is 246 A4 pages, 1,645,350 bytes, SHA-256
`aee3f74109bafd1614d01d6593b8b2edbcbfdbf3b841b6beee878a01d7ddec16`.
Pandoc 3.9.0.2 and MiKTeX pdfTeX 1.40.29 produced byte-identical PDFs in
two independent passes under `SOURCE_DATE_EPOCH=1787443200`.

## Representative render inspection

Poppler `pdftoppm` rendered the following final-PDF pages at 120 dpi. Each PNG
was inspected at original render resolution:

| PDF page | Coverage | Render SHA-256 |
|---:|---|---|
| 1 | Title, subtitle, authorship, and opening contents | `3fa19b8824d23a6250512f0d05bf111b959a80dd720723bfe1d2989680d3b708` |
| 123 | Mid-reader prose, equations, diagram, and page furniture | `2c30dbbf83d89e094d1dca0d16c9ae503c7b9cd84a137433aca936989d58af38` |
| 237 | Unit 20/21 boundary and multiline source-link repair | `e64d2882cbd5551868d66a06db7ccb61eea0dce977bc2c241c972f4b6a1e1f0b` |
| 238 | Unit 21 opening, provenance, cohomology display, and audit note | `e25c4a3e422f7ff2cbc6291af38f9debb97b13001499147892419f0ab7b50b15` |
| 240 | Standard simplices and both centered semantic figure descriptions | `a0540c5a0084297a847220c8733e28be352f2602a9cd5794fd2f47cd30132aa3` |
| 243 | Mastery problem, hint, solution, and long formulas | `660a4c773086905d45b4f53117560bc940c734701abcca4b20a89d4b090ad9c4` |
| 246 | Final Unit 22 boundary and terminal page furniture | `4c044ca5129e0acbf4db67972e3f138ae4b0ce2a2408a2aafed200a541deb099` |

No inspected page has clipping, overlap, broken glyphs, unreadable formulas,
positional-figure dependence, or margin/page-number collision. Page 246 ends
early because the source unit's final boundary notice is short; its whitespace
is intentional, not missing content.

## Defect found and repaired at the builder layer

The first cumulative candidate, SHA-256
`abeec1de6f12b4ff78b4accaa75363780f3b9e2291f0ea32eb69ad3e60a19309`,
showed a literal empty TeX group before the multiline `Notes.tex` link on page
237. The inherited PDF-only bracket safeguard had mistaken a Markdown link
line for a bracket-led array cell. The new Units 001-021 builder now applies
that safeguard only inside dollar-delimited display-math blocks. The Unit 21
source and every earlier source remained byte-identical. The repaired page 237
was re-rendered and inspected, and extracted final-PDF text contains no visible
`{}Notes.tex` sequence.

## PDF and HTML verification

- PDF metadata: title `Topologi Aljabar - Unit 1-21`, A4, 246 pages,
  `/Lang=id-ID`, no encryption/forms/JavaScript, and no suspect flag.
- Fonts: 25 rows; every row is embedded, subset, and has a Unicode map.
- Structural tagging: the PDF is honestly **untagged**; the reflowable HTML is
  the accessible primary structure.
- HTML: 1,084 unique DOM IDs with no duplicates, 256 resolving fragment links,
  8,208 MathML nodes, 50 semantic figures, and all 47 Unit 21 stable IDs.
- Privacy: targeted HTML and extracted-PDF scans found no credential markers,
  placeholders, or absolute local user paths.
- Process provenance remains exactly **OpenAI Codex gpt-5.6-sol, Ultra**; source
  authorship, human direction, CC BY 4.0, and non-endorsement remain intact.

This is representative visual QA, not a claim that every one of the 246 pages
was manually inspected.
