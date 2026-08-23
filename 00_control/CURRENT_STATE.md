# Current state — O012/D60

Updated: 2026-08-23

Status: active production. Source admission and composite route selection are closed. Units 001–019 now translate Roberts `Notes.tex:134–3947` contiguously; all are independently reviewed with P1/P2/P3 zero. Unit 19 is 57,277 bytes, 1,865 lines, 78 structural stable IDs, SHA-256 `ba34773d63e4dc70fccdf4fa19fbdc8a397062a4bc359978f3261a70ff64f98c`; its bounded QA passes and the next source cursor is Lecture 20 at line 3948. The cumulative Units 001–019 reader passed the fail-closed build, structural, rights, terminology, PDF, all-page render, and desktop/mobile browser gates. Its primary HTML is 2,962,478 bytes/SHA-256 `ea5481b14dc1772408bd1c3e384b94a18eed9f2be3c9b9379fe4f8dd499253e0`; its secondary PDF is 1,506,471 bytes/SHA-256 `291e4206b9e58ee8a49108e55b6b894b9cd3362c7701a50cb83a7d79714b7a86` and 221 A4 pages; the cumulative QA receipt is 12,097 bytes/SHA-256 `38f8f3084f6031fe3670667e7e9a11f2b526a07eb69d32772194c3ff0ffeb02d`. The backend now has 2,726 canonical records in 11 JSONL files, 710 stable source IDs, 91 new adverse-ledger records, and bundle SHA-256 `fe590ceefd18081e9a2dad3510946e97a29375a0a82e2a8e26cd78b871d33b14`; the independent 001–019 validator passes. The existing Units 001–013 reader remains anonymously byte-verified on GitHub Pages, Zenodo (`10.5281/zenodo.22061490`), and Figshare (`10.6084/m9.figshare.33314982.v1`); this new boundary is ready for a narrow push and update of those existing Zenodo/Figshare lineages, with public readback still pending. The same-field Indonesian terminology QA governs the live glossary and records `OpenAI Codex gpt-5.6-sol, Ultra`. After all 30 Roberts lectures, the selected Fomberg lines 31–4185 and exact original closure follow; see `CURRICULUM_ROUTE_AND_FOMBERG_HANDOFF.md`.

## Current verified Units 001–019 checkpoint (2026-08-23)

- Roberts authority: commit `b947ad2e9f9e301bfe24590a9db653bc54fa1a53`, tree `aa1d3edb85818e7176e2d0bbc06d9b4bd1e247f5`, `Notes.tex:134–3947`; next source line 3948 (`\\lecturenum{20}`).
- Unit 019: `source/id-ID/units/unit-019-lecture-019.md`, 57,277 bytes, 1,865 LF lines, 78 stable IDs, SHA-256 `ba34773d63e4dc70fccdf4fa19fbdc8a397062a4bc359978f3261a70ff64f98c`; independent review `qa/UNIT_019_INDEPENDENT_REVIEW.md`, 2,707 bytes/SHA-256 `d360a17a8a7a5008a80873c4413d92bd9354b6c44275365809be33258c0673a`; source audit `qa/UNIT_019_SOURCE_AUDIT.md`, 8,956 bytes/SHA-256 `9ff651aa4a98f17f9ae67ce154cc531147bf212b2be03e53c3aced3994066f36`; unit QA `qa/UNIT_019_QA.json`, 3,519 bytes/SHA-256 `a2ecc5dcc539c6434d2cb937ad7bb768c6ed434947b4cedcd313ce1bcfe8d1c3`.
- Cumulative HTML: `output/html/units-001-019/index.html`, 2,962,478 bytes, SHA-256 `ea5481b14dc1772408bd1c3e384b94a18eed9f2be3c9b9379fe4f8dd499253e0`; native MathML 7,451, display MathML 1,331, artifact IDs 951, resolving fragments 243, no runtime assets/scripts/stylesheets, offline/self-contained.
- Cumulative PDF: `output/pdf/topologi-aljabar-unit-001-019-id.pdf`, 1,506,471 bytes, 221 A4 pages, SHA-256 `291e4206b9e58ee8a49108e55b6b894b9cd3362c7701a50cb83a7d79714b7a86`; 24 embedded/subset/ToUnicode font rows; `/Lang=id-ID`; intentionally secondary and untagged.
- Cumulative QA: `qa/UNITS_001_019_QA.json`, 12,097 bytes/SHA-256 `38f8f3084f6031fe3670667e7e9a11f2b526a07eb69d32772194c3ff0ffeb02d`; visual receipt `qa/UNITS_001_019_VISUAL_QA.md`, 1,780 bytes/SHA-256 `29d69abe6399976a206ef28c96d01df5fdb3f9f2c8510db95fe73f2b35b0b064`; render inventory 26,213 bytes/SHA-256 `017f151a1bd06a4e2649b37ad551c973789d502897b358967bd216cd74c61783`. All 221 pages and browser 1280×720/390×844 surfaces passed; desktop body 928 px, mobile content 375.11 px, zero document overflow, 101/101 wide mobile displays locally scrollable, zero console warnings/errors.
- Backend: `scripts/validate-backend-units-001-019.py` passes; 2,726 records, 11 JSONL files, 2,480,537 bytes, bundle SHA-256 `fe590ceefd18081e9a2dad3510946e97a29375a0a82e2a8e26cd78b871d33b14`. The release artifact extension adds ten exact artifacts and five passed QA events; no raw render dump is asserted as a public release file. The sanitized backend receipt is `qa/BACKEND_UNITS_001_019_RECEIPT.json` (2,377 bytes, SHA-256 `b7733961574b0db40904687d0eb6ff04c51bb3dd813fce15694b7646fa6d2b59`).
- Next executable action: update the existing Zenodo concept/version and Figshare article/collection lineages (no duplicate records), preserving partial/finishing truth and exact licenses. GitHub commit `3a9db22813fc93e9cbd7f65a418ba634a24af959` (tree `56df67af20c581a5ab277350ba597c149b242407`) and Pages URL `https://kokunoyumeto.github.io/algebraic-topology-id/units-001-019/` were anonymously read back byte-for-byte; receipt `00_control/GITHUB_PUBLICATION_RECEIPT_UNITS_001_019.json` is 2,087 bytes/SHA-256 `d6d29345cfc0fcd17bd5c1b2b33dd00f04c3be3b754ce25a298df8467a05550e`. After Zenodo/Figshare receipts, resume contiguous translation at `Notes.tex:3948`.

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

The exact Roberts archive, commit/tree, seven-file manifest, CC BY 4.0 license, and reproducible upstream baseline remain frozen. MIT 18.905 remains a proof-check reference only. Fomberg `algebraic_topology.tex:31–4185` is the selected post-Roberts CC BY-SA 4.0 homology bridge, with admission deferred until its dependency replacement and two-build gate pass; the separate Fomberg problem bank remains excluded. Two later StackExchange-derived code blocks remain quarantined for independent redraw.

## Same-field Indonesian terminology QA boundary

- No suitable Indonesian algebraic-topology arXiv TeX source appeared in the bounded exact search. The truthful fallback is Valentino Risali and Indah Emilia Wijayanti, *Sifat-Sifat Morfisma di dalam Kategori Ruang Penutup Ruang Topologis yang Terhubung Lintasan*, DOI `10.22146/jmt.56529`, an Indonesian 13-page LaTeX/pdfTeX-generated journal PDF whose editable source is not exposed.
- Direct page inspection supports `fungtor`, `morfisma`, `lembaran`, and `tertutup rata`. The live Unit 001–017 sources and canonical backend now use those preferred forms. `funktor`, `morfisme`, `lembar`, `diliputi secara merata`, and `persekitaran` remain discoverable as variants where appropriate; modern `objek`, reader-facing `lingkungan`, and translated `penuh dan setia` are retained deliberately.
- Migration closure: 17 source files; 193 fungtor-family, 327 morfisma-family, 61 lembaran, and six tertutup-rata substitutions; line counts and stable IDs unchanged; formulas, source locators, authority, and frozen public artifacts untouched.
- Live Unit hashes after the migration are recorded exhaustively in `qa/INDONESIAN_TERMINOLOGY_QA_2026-08-22.json`. Units 014–017 are respectively `da6f18b455d76adafd8b9b648ed7c277958eca95c0b7d76a8bd9895d79ec6677`, `e9ab0565ae460236a69c77389b76d32405873156fc451be9cf95c3749e7fe9d1`, `31dfc4c3647f7d6a1d398d2123efe1faa82348428df0180eee2a2358572f9054`, and `47576d7c26a436ba915c276b692e2bc0ead6fae038295fee3a82a50426ed9a96`.
- Backend validation passes at 1,762 records in 11 JSONL files, bundle SHA-256 `c5ac458a7f4723460ccebccaf3e5738544883c685a54c9a3cfbef854f2db83c5`. The terminology boundary is public at commit `13df3a00b3016d717428078ee451f2b43c398e7d`; five representative files passed anonymous raw-byte readback, recorded in `GITHUB_TERMINOLOGY_QA_RECEIPT_2026-08-22.json`. The published Units 001–013 backend snapshot remains separately bound to its original `bb8512f56a8b…` hash.
- Exact process provenance: `OpenAI Codex gpt-5.6-sol, Ultra`. Source author, comparison-paper authors, human direction, licenses, and non-endorsement remain explicit and unchanged.

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

### Published cumulative Units 001–013 preservation boundary

- Source span: Roberts `Notes.tex:134–3046` (Lectures 1–13).
- HTML: 1,824,804 bytes; SHA-256 `be1473ab5cb8eff26341e554179661775a12cec5784a8ebf3f9c2f3f0633cb71`.
- PDF: 1,071,382 bytes; 138 A4 pages; SHA-256 `14775535f773735db5886195980f39e417aaea24998927956a81b55b0ef77c68`.
- Artifact manifest: 249 bytes; SHA-256 `6b55446a4f0a951329c29ec33b0ca586c749b9301dd4bd8ad4dd94f1c91d74de`.
- QA receipt: 9,069 bytes; SHA-256 `cb2413e8131743457a0685a57cf519c769e5593e9ec8d904f6160f9e0519983d`.
- Visual/browser receipt: 2,139 bytes; SHA-256 `78e151b05d3efdce4dbfd346962dece5d7da4a559ab1101ac4bd8e02bff59f48`.
- Extracted-text witness: 395,766 bytes; SHA-256 `d94869df978e2538c79b8859cb38c8cbf859420cde68326a35546c973c787497`.
- Structural closure: 426 stable IDs, 261 semantic blocks, 587 unique artifact IDs, eight aliases, 160/160 resolving fragments, and 4,682 native MathML nodes.
- Backend: 1,762 canonical records in 11 JSONL files, 1,540,725 bytes, validator bundle SHA-256 `bb8512f56a8bbcf1283ae10ab69a9a7ecebb1bd39c425c1c021b5b848a1b2910`.
- Two direct HTML builds are byte-identical. The frozen builder's two PDF builds compare hashes fail-closed; final recovery did not rebuild or remark the PDF. Both validators pass independently.
- All 138 PDF pages and the HTML at 1280 x 720 and 390 x 844 passed visual inspection. The desktop body is centered at 928 px; mobile document overflow is zero and all 54 wide formulas scroll locally; browser warnings/errors are zero. All 24 PDF fonts are embedded, subset, and ToUnicode. PDF remains secondary and intentionally untagged.
- The release package contains exactly eight files and passes fixed semantic allowlists, decompressed-entry hashes, reader/QA/backend bindings, two-build ZIP byte comparison, credential/path scans, and atomic promotion verification. Frozen package hashes: source/backend ZIP `cbc60263dd30d7b392702a7d9463b62f5cc60506d58d3029fbd36d71b8644dd5`; QA/provenance ZIP `a6dd37e925487c9c622e0a02ff051ab0d1b4f5aed4c21364ea72b70273955827`; release manifest `0a927209212615d196d084af825f2c81dc0941fc720c361713ddfa81a97964dc`. It is public at Zenodo record `22061490`, DOI `10.5281/zenodo.22061490`, concept DOI `10.5281/zenodo.22061489`; the exact eight public files were anonymously downloaded and SHA-256 verified. Its compact seven-file reader-first mirror is public at Figshare article `33314982`, DOI `10.6084/m9.figshare.33314982.v1`, project `280296`, and Indonesian collection version `10.6084/m9.figshare.c.8668413.v35`; every Figshare file also passed anonymous byte readback.

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

Publication was attempted at 2026-08-22T09:00:00+02:00 from local commit `8498730cbe0e382e955dae4543b2875c3c9b827f`, tree `3f7f33482426002b0fa02c8d8264b546ae66bf41`. GitHub rejected the push with HTTP 403 because the only authenticating account is suspended. Of the two user-supplied credential candidates, one reaches that suspended account and the other is invalid or expired; the credential manager exposes no alternate account and no SSH identity is configured. Anonymous follow-up found repository API HTTP 403 and Pages HTTP 404 even for the formerly verified Unit 1–4 surfaces. No token is stored in the receipt. See `PUBLISH_ATTEMPT_UNITS_001_005.json`. The boundary remains locally committed and publication-ready; production continues without falsely claiming a public release.

### Verified cumulative Units 001–007 local release candidate

- Source span: Roberts `Notes.tex:134–1770` (Lectures 1–7).
- Cumulative HTML: 899,803 bytes; SHA-256 `55135048eafe0f097c45936add885e008392eefdf475270fea37adf6a2a7b7bb`.
- Cumulative PDF: 702,470 bytes; 66 A4 pages; SHA-256 `3764b75ecfb9200e25a165db1f0f97a680384378e2a9a22e129aab57dd860d93`.
- Manifest: 247 bytes; SHA-256 `7b279f0413892f0ddedce636b3a272884bb7bfa01410bf33a6ce34c0c34db2f9`.
- QA receipt: 7,384 bytes; SHA-256 `2982a9465428eff97e6047bffdadba422b2dc0406e34750f632bfe148ed67617`.
- Visual/browser receipt: 3,259 bytes; SHA-256 `63a4b4545213a7aec1c556a3852b818ba2f207b10cac7e80c62330709604176f`.
- Structural closure: 224 stable IDs, 135 semantic blocks, 2,344 native MathML nodes, 89 resolving fragments, all 30 exercise-solution pairs, both question-answer pairs, and the preserved `eg:piS^1_infinite` source alias.
- Backend: 995 canonical records in 11 JSONL files; bundle SHA-256 `0acf007e732682268d904699b4fbcf12c5f1a757b98938b776a72614b432df64`.
- Two HTML builds and two PDF builds are byte-identical. Independent reruns of both QA validators passed. Root visual review covered all 66 Poppler-rendered pages, full-size pages 1, 45, 57, and 66, HTML at 1280 x 720 and 390 x 844, 32 formula-local mobile scrollers, zero document overflow, and zero browser warning/error. PDF remains secondary and intentionally untagged.
- This boundary and the independently frozen Units 008–010 sources are preserved in local commit `a3dc793ec3a7f0b1c4c0c4211115ff9caf847be0`, tree `61dc29f02dc6b20a04ec17bd7d491afc0a20d29a`, parent `8498730cbe0e382e955dae4543b2875c3c9b827f`. It is not publicly released; it still needs a successful push after GitHub accepts the account again.

### Verified cumulative Units 001–010 local release candidate

- Source span: Roberts `Notes.tex:134–2272` (Lectures 1–10).
- Cumulative HTML: 1,318,415 bytes; SHA-256 `e228ac1422b2742d873feffd5b236fe9c1329d0bdb5da0e8deffe5e770361088`.
- Cumulative PDF: 862,913 bytes; 99 A4 pages; SHA-256 `d0f739aedf3da5f317cf99a1a0dcace1f89b8c802f1dedc42c7ac0c63375c7c1`.
- Manifest: 248 bytes; SHA-256 `5bcf82984e3f2848f5471876401e48948639d6ca144e0915d99c86c20fc39d92`.
- QA receipt: 9,808 bytes; SHA-256 `4189663021e6bd7e8822198a79bb3d7c59c7e0cca777054fbc370e77a300da5c`.
- Visual/browser receipt: 2,471 bytes; SHA-256 `439099f8c865125864444f9cfd1f60b961274ba0bc6f9bb29c562ee30fab132b`.
- Extracted-text witness: 280,664 bytes; SHA-256 `4932889b582a3ccd9816db4b8008791d5fbdc4b044da6f5d1985a87b6ce10642`.
- Structural closure: 306 unique stable IDs, 183 semantic blocks, 3,411 native MathML nodes, 431 unique content HTML IDs plus the document root, 123 resolving fragments, and all five source-label aliases.
- Backend: 1,345 canonical records in 11 JSONL files; 1,131,189 bytes; bundle SHA-256 `ca6ff5b776594f5b3c1408accfc6129b876fbcdc6d029279dbbbbc1d9a40bbdf`.
- Both HTML builds and both PDF builds are byte-identical. Both validators pass independently. All 99 Poppler-rendered pages were inspected; an independent root sample covered pages 1, 68, 79, 89, 93–95, and 99. Browser readback at 1280 x 720 and 390 x 844 confirms a centered 928 px desktop body, zero document overflow, 37/37 locally scrollable wide formulas, and zero warning/error. PDF is secondary and intentionally untagged.
- This boundary and the Unit 011 source freeze are preserved in local commit `d27c7b7dd784ec4fbbc33a4490759869a6929f89`, tree `945e13bff783a90068560827f72fe54e05ff66f9`, parent `a3dc793ec3a7f0b1c4c0c4211115ff9caf847be0`. It is ready for a subsequent push when GitHub accepts the account again; no public-release claim is made.
- A single push of the new boundary was attempted from receipt commit `d4a9143efabf62eebf01a369e1ebe63c5e01046b` on 2026-08-22 at 18:05 +02:00. GitHub again returned authenticated HTTP 403 with the explicit account-suspended response; anonymous repository API, Pages root, and Units 001–010 reader checks each returned HTTP 404. No credential or secret is recorded. See `PUBLISH_ATTEMPT_UNITS_001_010.json`; do not loop retries without a changed access state or a later substantial boundary.

### Translated and independently reviewed Units 006–018

- Unit 006: `Notes.tex:1305–1515`; 32,106 bytes; 893 lines; 28 unique stable IDs; SHA-256 `3cb182fdf183bd67e45a898228b995a44d4638e808fdfbe6ea6d6a2a2b889e33`; independent review P1/P2/P3 zero.
- Unit 007: `Notes.tex:1516–1770`; 22,107 bytes; 749 lines; 24 unique stable IDs; SHA-256 `556cea5445e1b0a51f86f1c0ea0e80c4e00a17d365d95fa530f063cc24856569`; independent review P1/P2/P3 zero.
- Unit 008: `Notes.tex:1771–1946`; 28,466 bytes; 930 lines; 26 unique stable IDs; SHA-256 `8369e74c80e391d73575bbcb7844d3bfa62dd771dbca6258eed02360b20529cc`; independent review P1/P2/P3 zero.
- Unit 009: `Notes.tex:1947–2093`; 25,524 bytes; 939 lines; 30 unique stable IDs; SHA-256 `16da25dea2f8ac5415b02738663046fb619c27e685042a734059e3150ed5ff18`; independent review P1/P2/P3 zero.
- Unit 010: `Notes.tex:2094–2272`; 26,432 bytes; 934 lines; 26 unique stable IDs; SHA-256 `e1c6ef961ae2266db86baec6d701dd659a1bf78bdd3601cf5b1c6515bc7d0310`; independent review P1/P2/P3 zero.
- Unit 011: `Notes.tex:2273–2494`; 28,465 bytes; 959 lines; 39 unique stable IDs; SHA-256 `1cdbe0cae239a4e60a72f25c8814c2e3b5ec26b9119da03624bda7f3ff1ae127`; independent review P1/P2/P3 zero.
- Unit 012: `Notes.tex:2495–2726`; 32,850 bytes; 1,024 lines; 37 unique stable IDs; SHA-256 `429831df4a5600c59351516915fb787cd73402d8c11c411869210dbf8aaa7ada`; independent review P1/P2/P3 zero.
- The Unit 012 source, review, and ledger boundary are preserved in local commit `b20292177577ceb91beedb24e64d90f71c41264a`, tree `7281da2df029f4f9936fd8075829e251c75b94be`, parent `1b030e4dd667b4d138bcff9b01942bdea73f35c8`.
- Unit 013: `Notes.tex:2727–3046`; 41,196 bytes; 1,306 lines; 44 unique stable IDs; SHA-256 `0aa68cb4ed31862d32aeff5a7106b4ac29c13cbc202f7dbc8381fc7cd31418c0`; independent review 6,665 bytes/SHA-256 `5903c7da7f57d5db15a2d94807860a816d15e7d3cb7b020a8a3ddcbb0df45c21`; P1/P2/P3 zero after bounded fixes; adverse ledger through `O012-ADV-0187`; terminology ledger through `O012-TERM-0213`.
- Unit 014: `Notes.tex:3047–3209`; 28,488 bytes; 947 lines; 38 unique stable IDs; SHA-256 `da6f18b455d76adafd8b9b648ed7c277958eca95c0b7d76a8bd9895d79ec6677`; independent review 9,725 bytes/SHA-256 `43a409f8f127fe9425d14bc8279a594e4ea1f604da3db4f99316aa7c17c3969d`; P1/P2/P3 zero.
- Unit 015: `Notes.tex:3210–3286`; 27,725 bytes; 835 lines; 34 unique stable IDs; SHA-256 `e9ab0565ae460236a69c77389b76d32405873156fc451be9cf95c3749e7fe9d1`; independent review 4,392 bytes/SHA-256 `9776c911f5d4f4cd7027375ac29514ca2722f28877d27e79753fabf61876dc90`; P1/P2/P3 zero; adverse ledger through `O012-ADV-0215`; terminology through `O012-TERM-0233`.
- Unit 016: `Notes.tex:3287–3383`; 33,919 bytes; 984 lines; 33 unique stable IDs; SHA-256 `31dfc4c3647f7d6a1d398d2123efe1faa82348428df0180eee2a2358572f9054`; independent review 8,485 bytes/SHA-256 `335f8ef19f35ba063ad526850d01eec377dc89eb7b697831b8741659a86444c6`; P1/P2/P3 zero; adverse ledger through `O012-ADV-0227`; terminology through `O012-TERM-0240`.
- Unit 017: `Notes.tex:3384–3481`; 29,933 bytes; 952 lines; 34 unique stable IDs; SHA-256 `47576d7c26a436ba915c276b692e2bc0ead6fae038295fee3a82a50426ed9a96`; independent review 9,903 bytes/SHA-256 `b4885ed709311275a9ae32fedbefe7bf86c72203caafa92de3b557f17c1fc625`; P1/P2/P3 zero; adverse ledger through `O012-ADV-0239`; terminology through `O012-TERM-0251`.
- Unit 018: `Notes.tex:3482–3677`; 44,415 bytes; 1,663 lines; 67 unique structural stable IDs; SHA-256 `9d0564f6a074441332e42755d46d9a0e858189a5ff4d8b5be52b1def12532598`; independent review P1/P2/P3 zero; cumulative QA now supersedes its earlier standalone receipt; adverse ledger through `O012-ADV-0257`; terminology through `O012-TERM-0274`.
- Unit 019: `Notes.tex:3678–3947`; 57,277 bytes; 1,865 lines; 78 unique structural stable IDs; SHA-256 `ba34773d63e4dc70fccdf4fa19fbdc8a397062a4bc359978f3261a70ff64f98c`; independent review P1/P2/P3 zero; adverse ledger through `O012-ADV-0278`; terminology through `O012-TERM-0287`.
- These fourteen source units preserve all admitted semantic content and marginal diagrams accessibly, and their added mastery material closes the identified proof gaps available at each source boundary. Units 006–010 are frozen in an earlier cumulative reader/backend; the current cumulative Units 001–019 checkpoint supersedes the former Units 011–018 source-only boundary.
- Historical source-cursor note: this section records the pre-checkpoint Unit 18 boundary. The live cursor is now `Notes.tex:3948` (Lecture 20), recorded in `CURSOR.json` and the current verified checkpoint above.

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

1. Continue contiguously from `Notes.tex:3482` (Lecture 18) and extend the next cumulative reader/backend at a coherent boundary; do not repeat the closed GitHub/Zenodo/Figshare Unit 001–013 preservation transaction.
2. After all 30 Roberts lectures, admit and translate Fomberg `algebraic_topology.tex:31–4185`, then create the exact separately identified proof/mastery/lab/capstone closure and 14-unit route view.

## Non-overlap boundary

O003 owns the standalone point-set-topology corpus. This lane translates only the prerequisite review occurring natively in Roberts and will not expand it into a competing point-set text or touch O003 paths.

## Recovery

Read `CURRENT_GOAL_AND_WORKFLOW.md`, then this file and `CURSOR.json`; next read authority/rights controls, terminology/adverse ledgers, backend JSONL, and the latest QA/publication receipts. Treat chat summaries as non-authoritative.
