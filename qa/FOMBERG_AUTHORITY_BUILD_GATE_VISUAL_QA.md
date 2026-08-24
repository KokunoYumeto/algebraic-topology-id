# Fomberg authority build-gate visual QA

Date: 2026-08-24  
Status: **PASS**

## Compared artifacts

- official PDF: `authority/upstream/math-notes-563194fae879178b9a6871b249513bfc27968975/official/algebraic_topology.pdf`, 383,089 bytes, SHA-256 `148aba71473e3201993e562c5e5d0f05f1a0417f4bcbd4593bead5ab236e43cd`;
- clean local baseline: `authority/upstream/math-notes-563194fae879178b9a6871b249513bfc27968975/build-baseline/algebraic_topology-baseline.pdf`, 664,609 bytes, SHA-256 `f0f8f815423dbdc3b368b48a5972bfc62be87ae8b5c4bfcd1b7a74b8871417ff`.

Both artifacts are 57-page A4 PDFs. The byte-size difference is expected: the
official artifact was produced by `xdvipdfmx`, while the reproducible baseline
uses MiKTeX pdfTeX and embeds its own font subsets.

## Inspection

Poppler/Cairo rendered pages 1, 3, 10, 20, 30, 35, 39, 40, and 57 from both
PDFs at 120 dpi. Each official page was compared side by side with the
corresponding baseline page. The sample covers the title/non-endorsement notice,
opening definitions, prose/proofs, displayed algebra, short and long
commutative diagrams, the two manual `commath` delimiter sizes, dense
cellular-homology calculations, the selected-source endpoint, the first
excluded section, and the final page.

This comparison supersedes the earlier same-date visual claim. That earlier
baseline exposed the optional arguments of `\del[4]{...}` and `\del[1]{...}` as
literal `([) 4]` and `([) 1]` output on physical pages 10 and 35. The corrected
CC0 overlay implements sizes 1 through 4. The rebuilt pages now agree with the
official formulas, and full-PDF text extraction contains zero occurrences of
either malformed literal.

No clipping, overlap, missing glyph, black box, broken arrow, displaced diagram,
margin collision, header/footer defect, page-number defect, or leaked optional
delimiter token was observed in the corrected comparison. Typography and some
line breaks differ slightly between the two TeX engines, but the layout remains
legible and the mathematical content is present.

Physical page 39 contains the end of Example 1.33 in Section 1.13. Physical page
40 starts `1.14 Extras before cohomology`. This visually confirms that selected
source lines 31-4185 correspond to physical pages 1-39 and that line 4186/page
40 is outside the selected bridge.

## Accessibility disclosure

All 23 detected fonts are embedded. The PDF is untagged, and its BBM glyph is an
embedded Type 3 font without a Unicode map. The baseline proves source/build
closure; it is not itself the final accessible Indonesian reader.

Temporary page renders and contact sheets were removed after this receipt was
written and the final visual comparison passed.
