# Roberts 001-030 + Fomberg 001 composite visual and browser QA

Status: **PASS after two documented reader repairs.** The complete Roberts
component (30/30) is followed by the distinct Fomberg component O012-FOM-001
(Sections 1.1-1.2, source lines 31-614). The composite course remains partial.

Final artifacts at this boundary:

- self-contained HTML: 5,029,788 bytes, SHA-256
  `2b64e8bec1dd5e1689ef6569360fec896ef87a683c7ba291a3780e27084a7390`;
- PDF: 2,322,978 bytes, SHA-256
  `fb81f2b2c0f73c17c4e3be4eaae164eaeaeb0c4ff0661580acfc7aa9b6d5f749`;
- 362 A4 pages; 27/27 font rows embedded, subset, and ToUnicode-mapped;
- Pandoc 3.9.0.2 and MiKTeX pdfTeX under
  `SOURCE_DATE_EPOCH=1787529600`; two clean HTML builds and two clean PDF
  builds were byte-identical.

## Repairs proved at this boundary

The earlier mobile reflow repair remains in force: body-level
`overflow-wrap: anywhere` prevents raw source hashes from widening the page,
while wide MathML remains locally scrollable.

The final pre-publication audit found a second P1 defect: the first Roberts
notice heading was concatenated directly to the composite header, so its
Markdown heading and attribute syntax were printed literally. The builder now
inserts a blank Markdown boundary and fails closed unless the delivered HTML
contains `id="o012-rbt-u001-notice"`, or if the literal source marker appears
in HTML or extracted PDF text. The rebuilt HTML contains the real heading and
anchor; both HTML visible text and whole-PDF extracted text contain zero copies
of the literal marker.

## PDF visual inspection

Poppler 24.04.0 rendered physical pages **1, 9, 13, and 351-362** at 144 dpi
(1,191 by 1,684 pixels). These 15 pages cover the title and table of contents,
the repaired first Roberts notice and opening lecture, the transition to
Roberts Unit 2, the end of Roberts, the exact Roberts-to-Fomberg boundary, and
every Fomberg page.

All 15 PNGs were inspected at original resolution. Their exact paths, bytes,
dimensions, and hashes are recorded in
`qa/ROBERTS_001_030_FOMBERG_001_RENDER_INVENTORY.csv` (2,287 bytes, SHA-256
`6194ca5afdaf20190c5e3ada9435472da6680080b48e510f12b2f9b9d10b0b07`);
the PNG witnesses total 4,079,968 bytes.

No inspected page has clipping, overlap, broken or unreadable glyphs,
unreadable mathematics, a margin collision, an orphaned heading, or missing
content. Specifically:

- page 1 has a centered title, exact partial-status subtitle, complete source
  credits, and a table of contents whose first Roberts notice is a real entry;
- page 9 displays “Tentang unit ini” as a heading, followed by “1 Kuliah 1”;
  no Markdown attribute syntax is exposed;
- page 13 closes the Unit 1 mastery material and begins the Unit 2 notice
  cleanly;
- pages 351-352 preserve the end of Roberts, state that there is no Roberts
  Lecture 31, and introduce Fomberg as a separately named component; and
- pages 352-362 preserve the complete selected Fomberg theory, diagrams,
  source repairs, all six exercise/hint/full-solution triples, and the exact
  next cursor at source line 615.

## Static HTML verification

The delivered HTML has `lang="id-ID"`, the exact composite title, exact model
provenance, 12,220 native MathML nodes, 75 semantic figures, 1,747 unique
source DOM IDs with zero duplicates, 352 fragment links with zero unresolved
targets, and all 87 Fomberg stable IDs. It contains zero script tags, external
runtime asset references, private paths, credential/placeholder markers, or
raw-TeX math fallbacks. The body is centered at a maximum width of 72 rem; the
mobile rule activates below 700 px; MathML and tables have local overflow.

## Live layout-engine verification

The exact final HTML was loaded from a bounded local server in the in-app
browser. At a 390 by 844 viewport:

- inner width was 390 px; document/body client and scroll widths were all
  375 px, so page-level horizontal overflow was false;
- the repaired `#o012-rbt-u001-notice` existed, had the visible heading
  “Tentang unit ini”, and measured 340/340 px client/scroll width;
- 2,144 geometry candidates extended within local MathML scrollers, but zero
  elements were exposed outside the viewport without an overflow-containing
  ancestor;
- 268 wide MathML elements remained local scrollers;
- the live DOM had 1,748/1,748 unique IDs (one browser-environment ID beyond
  the 1,747 source IDs), all 87 Fomberg IDs, 352 fragment links, zero broken
  targets, 12,220 MathML nodes, zero scripts, and no literal heading marker;
- top-of-reader and Unit 1 notice screenshots showed readable reflow and no
  page-level horizontal scrollbar.

At 1,280 by 900, document client/scroll widths were 1,265/1,265 px, the body
was 1,152 px wide, and its centering delta was 0.056 px. The page emitted zero
current-load browser errors or warnings. The temporary viewport override was
reset, the test tab closed, and the local server stopped.

## PDF structure, rights, and limitations

The PDF is unencrypted, unrotated, has no form or JavaScript, and is not
structurally tagged (`Tagged: no`). The self-contained HTML is therefore the
primary reflowable surface. Extracted text preserves composite scope, source
credits, CC BY 4.0 / CC BY-SA 4.0 component notices, non-endorsement,
independent-edition status, and `OpenAI Codex gpt-5.6-sol, Ultra` provenance.

The separately identifiable Roberts-only translation and companions remain CC
BY 4.0. The Fomberg adaptation and the integrated Roberts-Fomberg arrangement
are CC BY-SA 4.0. The repository `LICENSE.md` records this scope explicitly;
full source license texts remain under the two frozen authority directories.
