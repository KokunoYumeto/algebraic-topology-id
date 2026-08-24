# Visual QA — Roberts 001–030 plus Fomberg 001–002

Status: **PASS**  
Date: 2026-08-24  
Model provenance: OpenAI Codex gpt-5.6-sol, Ultra

## Frozen reader artifacts

- HTML: `output/html/roberts-001-030-fomberg-001-002/index.html`; 5,254,038 bytes; SHA-256 `1f7618003e3ff273a4f1e2d97b5a81fd320f76640c475cae845ed38793fbeccd`.
- PDF: `output/pdf/topologi-aljabar-roberts-001-030-fomberg-001-002-id.pdf`; 2,399,760 bytes; 376 A4 pages; SHA-256 `7dc8ac1db0b03ed1d9d94fe2c3491b631d3fb8bcec869997889d67d70236ef82`.

## Browser geometry and reflow

The offline HTML was served only from the task-local build and inspected in the Codex in-app browser. At the default 1280 × 720 viewport, the document client width was 1,265 px and the body was exactly 1,152 px wide with symmetric 56.4444 px left and right margins. Document scroll width equalled client width; no element escaped the viewport. The page contained 12,720 native MathML nodes, 1,850 identified DOM elements including the document root, 368 fragment links, and no duplicate IDs.

At a temporary 375 × 812 mobile viewport, the document client and scroll widths were both 360 px, the body occupied the full 360 px content width, and page-level horizontal overflow was zero. All 2,832 descendants whose visual boxes extended beyond the viewport belonged to one of 345 local horizontal scrollers (344 MathML containers and one table); exposed overflow count was zero. The Unit 002 heading and the chain-complex diagram region were visually inspected at this breakpoint. Text reflowed naturally, semantic blocks filled the available width, and formula overflow remained locally scrollable. Browser warning/error log count was zero. The temporary viewport override was reset and the test tab was closed.

## PDF rendering

Poppler rendered the title page, the Unit 001→002 transition page 362, and every Unit 002 page 363–376 at 120 dpi. The 14-page contact sheet and original-resolution pages 1, 362, 363, 368, 372, and 376 were visually inspected. Margins, typography, page numbers, headings, inline and display mathematics, semantic diagram descriptions, proof repairs, mastery exercises, hints, solutions, and the terminal source boundary are legible and unclipped. No overlap, missing glyph, black square, truncated formula, or broken page transition was found. The PDF remains intentionally untagged; that accessibility limitation is disclosed, while the HTML is the primary accessible/reflowable reader.

Exact render filenames, byte counts, dimensions, and SHA-256 values are recorded in `qa/ROBERTS_001_030_FOMBERG_001_002_RENDER_INVENTORY.csv`.

FINAL_SEVERITY_COUNTS {"P1":0,"P2":0,"P3":0}
