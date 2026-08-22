# Current state — O012/D60

Updated: 2026-08-22

Status: active production. Source admission is closed. Units 001–004 remain translated, independently rereviewed, built, visually/browser checked, backend-complete, published, and anonymously byte-verified. Unit 005 is fully verified and ready for its cumulative publication transaction. Units 006–007 are translated and independently clean but are not yet built or backend-frozen. Every earlier reader remains byte-frozen. The next source cursor is Lecture 8.

## Frozen cumulative Units 001–002 boundary

- Source span: Roberts `Notes.tex:134–584` (Lectures 1–2).
- Reader sources: Unit 001 is 16,179 bytes/SHA-256 `c80b51c22a2fa7ea116201028b78d5f8d708ef4d8355d34092ac7a9c88415e15`; Unit 002 is 25,090 bytes/SHA-256 `4d2acc43557db9b3c419ee177545d285b9fcf50b2aa2dd3b2c6c44182f3a6a01`.
- Cumulative HTML: 220,035 bytes; SHA-256 `d3b5cbfaa3511823821ecf9ba26a4eaec7c84d937417927d11bde3f66abc9f54`.
- Cumulative PDF: 395,385 bytes; 15 A4 pages; SHA-256 `0413c3a3280955cc482a5c0c2d7615b78128dccba3b6b1901dee1bf34d133b8e`.
- Cumulative artifact manifest: 247 bytes; SHA-256 `93e98f6cbbc60775bb934df5b49141f63d7cd2c76582a26c61d4192ff320d721`.
- Backend: 315 canonical records in 11 JSONL files; bundle SHA-256 `f1999b5d33466ba9a15a32f50a16173fbb7659f1a7b28a3452bc5d2ec3094e6e`.
- Cumulative QA receipt: 2,690 bytes; SHA-256 `075546f6a856638dc420ed62b23ec78c7a57f839444e4f2101233d6421f776f0`.
- Independent final rereview: P1 = 0, P2 = 0, P3 = 0.
- Visual scope: all 15 physical pages plus Chromium at 1280×720 and 390×844; no clipping, overlap, page-level overflow, broken formula, missing glyph, blank object, or orphan page.
- Public cumulative reader: `https://kokunoyumeto.github.io/algebraic-topology-id/units-001-002/`; anonymous HTTP 200 readback is exactly 220,035 bytes with the frozen cumulative HTML SHA-256. The preserved Unit 001 root remains exactly 85,580 bytes with its frozen SHA-256.
- Repository: `https://github.com/KokunoYumeto/algebraic-topology-id`; deployed commit `d6cf20708d5f1582a100982b49325c1f3d341763`, tree `966b9749a946cf75f0294ad102d5f2a3afefb90d`, workflow run `32509014519`, job `96855555077`, deployment `6026268020`, all successful.
- Publication receipt: `PUBLICATION_RECEIPT_UNITS_001_002.json`, 6,236 bytes, SHA-256 `11bcee6697eb2ac34b080f74a13930f623b3657d459f7e8505695397854b22a6`; its anonymous readback binds the Pages HTML, PDF, Unit 2 source, manifest, QA receipt, commit, and complete public tree inventory.

The 70 stable IDs cover 43 semantic blocks. All nine source exercises have complete solutions and the source question has an answer; two added lemma proofs make the main universal-property and perekatan arguments explicit. Eight Unit 2 correction records disclose seven mathematical/source fixes and one marginal-exercise reflow. HTML is offline, self-contained, centered/reflowing, `lang=id-ID`, and native MathML; wide formulas scroll locally on narrow screens. PDF is secondary and explicitly untagged. Unit 001’s original HTML/PDF bytes remain unchanged.

## Authority and rights

The exact Roberts archive, commit/tree, seven-file manifest, CC BY 4.0 license, and reproducible upstream baseline remain frozen. MIT and Fomberg/Lazarovich are closed benchmarks, not donors. Two later StackExchange-derived code blocks remain quarantined for independent redraw.

## Frozen public cumulative Units 001–003 boundary

- Source span: Roberts `Notes.tex:134–877` (Lectures 1–3).
- Unit 003 source: 25,822 bytes, 618 lines, 39 stable IDs, SHA-256 `993e5941895a9b6f4b197b4c236f5a4990f6ae621e2bb7911353b28a5e1abffd`.
- Unit 003 independent review: 2,464 bytes, SHA-256 `b2cffbcc2167c3d620f1af53224cc064e8ce34400561868339e69c280845619c`; P1/P2/P3 are zero.
- Cumulative HTML: 359,397 bytes, SHA-256 `33281cc46faa3d560c968b657526cd914786c991d1475b5563911a265bd316c1`.
- Cumulative PDF: 460,320 bytes, 25 A4 pages, SHA-256 `2c9bf67e74c94bca9aad0238e910816188a957892a6cf811f7f615e221b4066d`.
- Cumulative manifest: 247 bytes, SHA-256 `1e211afb4b165435ece5f72a2b4e9b084975db35d111127880255473302f5049`.
- Cumulative QA receipt: 3,983 bytes, SHA-256 `fb511086669846b6c8a68a6c1fecc4bd774016a6c95eb27219e3babbd177a873`.
- Visual/browser receipt: 2,310 bytes, SHA-256 `4d7d603c2276bd570e3bf47897c67d98bf6507d2bd9ffed2acd10ab1a509130e`.
- Backend: 496 canonical records in 11 JSONL files, bundle SHA-256 `0c08bebf7cbac289e94a7de571d3c2bab4d161c8a6a75c35b8a997f07ff6c939`.
- Public reader: `https://kokunoyumeto.github.io/algebraic-topology-id/units-001-003/`; anonymous HTTP 200 readback is exactly 359,397 bytes with the frozen HTML SHA-256. The preserved Unit 001 and Units 001–002 Pages readers also remain exact.
- Repository boundary: commit `9ffa736df82eaaa0c8ea70f2b35942ef4119afcb`, tree `b4695fd8e7e38d861dfa295d3bb2ea31b7d41099`, Pages workflow run `32551934416`, job `96979992402`, deployment `6033213187`, status `17152322493`; all successful.
- Publication receipt: `PUBLICATION_RECEIPT_UNITS_001_003.json`, 9,579 bytes, SHA-256 `4658845496597e34cee7fc83f641d68faf88acc9b2a62804f89b99c33fbcba07`. Anonymous raw readback covered every one of the 30 changed release files with exact byte count and SHA-256 identity.

The 109 stable IDs cover 68 semantic blocks. All 14 exercises have complete solutions; the source question has an answer; all added checks are supplied. Ten Unit 3 source corrections and four accessibility reflows are disclosed one-to-one in the adverse ledger and backend. HTML is self-contained, centered/reflowing, `lang=id-ID`, and native MathML; all 41 fragments resolve and wide formulas scroll locally at mobile width. All 25 PDF pages and the HTML at 1280 x 720 and 390 x 844 passed visual inspection with no P1/P2/P3 finding. The PDF is secondary and explicitly untagged.

## Current production

### Verified cumulative Units 001–005 release candidate

- Source span: Roberts `Notes.tex:134–1304` (Lectures 1–5).
- Unit 005 source: 22,662 bytes, 663 lines, 30 stable IDs, SHA-256 `7333a7b7a92b9618016412abb5c9b2b2a398538f690d0109d4282289a0719852`.
- Unit 005 independent review: P1/P2/P3 are zero.
- Cumulative HTML: 610,594 bytes, SHA-256 `8d3accf480101565409909c05f987f44b73f1c98889128e2f5074a4e049f48f3`.
- Cumulative PDF: 589,065 bytes, 44 A4 pages, SHA-256 `d6929434a9bc7ae78fb71fc060e9cc54dce85d37e4997ffe042ccbab982e64e2`.
- Cumulative manifest: 247 bytes, SHA-256 `2910fd87871675730aea7ca33e636a70d330d0f81183e887bad74ea1fd2d5190`.
- Cumulative QA receipt: 4,768 bytes, SHA-256 `ffb6703e4fe2ebc1c7733dc4f87a32c64c53cbe3ebf326d65a8d2da94765635a`.
- Visual/browser receipt: 2,877 bytes, SHA-256 `ed8249702d8335b01dc40925af1d5b071fa18d2eef9fe628a5535bd9404fbcdd`.
- Structural closure: 172 stable IDs, 106 fenced semantic blocks, 1,659 native MathML nodes; all fragment links resolve.
- Backend: 785 canonical records in 11 JSONL files, bundle SHA-256 `c36095ba31dcdbc8db52e327902bfbfd419a65a3c827da41e847aa8dc55bc5e2`.
- Final browser QA at 1280 x 720 and 390 x 844 found zero document overflow, 17 formula-local scrollers, centered/reflowing content, and no console warning or error. Fresh Poppler rendering and inspection covered all 44 pages; no clipping, overlap, broken glyph, blank object, or orphan continuation page remains. PDF remains secondary and intentionally untagged.

Publication is the immediate remaining action for this boundary.

### Translated and independently reviewed Units 006–007

- Unit 006: `Notes.tex:1305–1515`; 32,106 bytes; 893 lines; 28 unique stable IDs; SHA-256 `3cb182fdf183bd67e45a898228b995a44d4638e808fdfbe6ea6d6a2a2b889e33`; independent review P1/P2/P3 zero.
- Unit 007: `Notes.tex:1516–1770`; 22,107 bytes; 749 lines; 23 unique stable IDs; SHA-256 `556cea5445e1b0a51f86f1c0ea0e80c4e00a17d365d95fa530f063cc24856569`; independent review P1/P2/P3 zero.
- These two sources preserve all admitted semantic content and marginal diagrams accessibly, and their added mastery material closes the identified proof gaps. They are source-frozen drafts only: no cumulative reader/backend/publication claim is made yet.
- Next exact source cursor: `Notes.tex:1771`, the Lecture 8 marker on its opening sentence.

### Verified cumulative Units 001–004 boundary

- Source span: Roberts `Notes.tex:134–1131` (Lectures 1–4).
- Unit 004 source: 24,582 bytes, 632 lines, 33 stable IDs, SHA-256 `826fcb368275cdad02f72a5cec951fc8466ba68b09ca0139d72c81a4c5591fea`.
- Unit 004 independent review: 3,031 bytes, SHA-256 `ac993a10e22738197775ae5c3f4e72948983c4e99ff602a52943b40ed417b6f9`; P1/P2/P3 are zero.
- Cumulative HTML: 494,732 bytes, SHA-256 `8c8f5e1ad8172a2d97e3931fc3b4f2a3aa7f9e8a709260a27103f7eca0f1357d`.
- Cumulative PDF: 539,006 bytes, 35 A4 pages, SHA-256 `5e92c4c6ed60bca9f2f4d362d4c48b4f01aa156b330e2adacd1bf88dd7de9e87`.
- Cumulative manifest: 247 bytes, SHA-256 `4c8bf407e426feb8db92308c4b28bdbbc0738416a85a13539ef7915e4c1aad83`.
- Cumulative QA receipt: 4,478 bytes, SHA-256 `1670bbe2377712c9f96b9a68cdb75589ae461512f77cea7ad0c9290193724bd5`.
- Visual/browser receipt: 2,257 bytes, SHA-256 `74e609e94ea47b89db223c21e12cae682048f0a60d8780dae96d5b0164f2c5ca`.
- Structural closure: 142 stable IDs, 88 fenced semantic blocks, 18 exercise-solution pairs, two question-answer pairs, 1,384 native MathML nodes, and 54 resolving local fragment links.
- Backend: 638 canonical records in 11 JSONL files; bundle SHA-256 `590d28189a06cb46b47151de5359b245914a0a51f172e5e0cba6595f29712589`.
- Public reader: `https://kokunoyumeto.github.io/algebraic-topology-id/units-001-004/`; anonymous HTTP readback is exactly 494,732 bytes with the frozen HTML SHA-256. The preserved Unit 1, Units 1–2, and Units 1–3 readers also remain exact.
- Repository boundary: commit `365dff08d41d6a78a8e712504c9f871b6b386094`, tree `f1284946e6622e80a16c90daaabc210f7d99f6ed`, Pages run `32554998308`, job `96987657938`, deployment `6033695000`, success status `17153629829`.
- Publication receipt: `PUBLICATION_RECEIPT_UNITS_001_004.json`, 18,957 bytes, SHA-256 `3dc601b8ba540bcafee21127535af879506880d6c8f349738d59b9e1168a2e8a`. Anonymous raw readback matched all 33 files in the release commit; all four Pages readers matched their frozen local bytes.

1. Publish and anonymously byte-verify the frozen cumulative Units 001–005 reader; persist its sanitized receipt.
2. Build Units 001–007 cumulatively with the same source-ID/backend/QA discipline, then continue contiguously from line 1771.
3. After the Roberts core, write the separately identified homology/cellular bridge and solved mastery layer.

## Non-overlap boundary

O003 owns the standalone point-set-topology corpus. This lane translates only the prerequisite review occurring natively in Roberts and will not expand it into a competing point-set text or touch O003 paths.

## Recovery

Read `CURRENT_GOAL_AND_WORKFLOW.md`, then this file and `CURSOR.json`; next read authority/rights controls, terminology/adverse ledgers, backend JSONL, and the latest QA/publication receipts. Treat chat summaries as non-authoritative.
