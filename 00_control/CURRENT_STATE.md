# Current state — O012/D60

Updated: 2026-08-29

Status: active production. Source admission, Roberts Units 001–030, Fomberg Units 001–007, all three cumulative assessments, and the 108/108 solution-bearing mastery layer remain closed. Computation Laboratory 3 is closed through learner/source, execution, independent review, append-only backend, deterministic reader build, 17-page visual inspection, desktop/mobile browser QA, and Zenodo publication/readback, all at P1/P2/P3 zero. The exact 7,546-record Lab 2 backend prefix is unchanged; Lab 3 adds 148 records/157,630 bytes and ends at 7,694 records/9,280,385 bytes with bundle SHA-256 `cddd65499da547e0c4f01b8a880f68d1c3d314c078a9179528e4a28b2c5f65a2`. The centered/reflowing self-contained HTML is 15,828,588 bytes/SHA-256 `c221955503cec820c7581c740a038ac1774999ac6a6014f8d0783da2cd08bf0d`; the deterministic PDF is 545 A4 pages/9,836,725 bytes/SHA-256 `b26b670db97facc9f5ab389eed69cf1f8b03f70e6047eacbd2bfa68c849ccd0d`. Zenodo `0.31.5` is public at record `22151513`, DOI `10.5281/zenodo.22151513`, in concept `10.5281/zenodo.22061489`; all nine files passed two anonymous byte/SHA-256 readback passes. Sanitized receipt `release/zenodo-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01-lab02-lab03/publication-receipt.json` is 11,691 bytes/SHA-256 `7fbf0e059ce9fdba120fc953a27ea2fcba4419420a94ea9e754ffe4b8741ed46`. The latest GitHub/Pages reader remains Lab 2 at content commit `8989fbd602f89d0a8d6c30bc7bac1980a74b2c99`; the exact next action is the narrow Lab 3 content push, Pages deployment, and anonymous public-byte verification, then Laboratory 4. Source line 4186 remains only the nominal post-Fomberg marker and is not authority to translate beyond the selected span. Model provenance remains `OpenAI Codex gpt-5.6-sol, Ultra` without diminishing source or human credit.

### Live recovery note — computation Laboratory 3 reader build closure, 2026-08-29

Two clean HTML, appendix-PDF, and merged-PDF writes are byte-identical. The
529-page predecessor is preserved by exact reconstruction, text-prefix, page-
structure, outline, and named-destination checks. Physical pages 529–545 were
rendered at 160 dpi and inspected at original detail; browser checks at
1440×900 and 375×812 found zero page-level overflow, zero unresolved fragments,
zero external runtime assets, local scrollers for all wide code/mathematics,
and zero console errors or warnings. Visual QA SHA-256 is
`43cccd44fc3cbfcf3b01542a32776dfbd37788bd011cd77115ed711bbbc934ba`;
browser QA SHA-256 is
`194f6da23dc3f299a8da8c3fc6cfa71f72de5ee202a82cce4a1b9bd460cca070`.
Do not rebuild this boundary absent a demonstrated defect. Zenodo v0.31.5 is
public and all nine files match twice under anonymous readback. Push and verify
the exact narrow Git/Pages delta, then begin `D60-LAB04`.

### Live recovery note — computation Laboratory 3 source and backend closure, 2026-08-29

`D60-LAB03` / `O012-ORIG-LAB03` maps to `D60-R12` and `D60-R14`. The reader `source/id-ID/labs/computation-lab-003-cellular-boundaries-degree.md` is 19,453 bytes/529 LF/SHA-256 `4c3d88ec7d28d14fd1594c59262a50923efbad3082d7796d947661c7012bdf27`; the program is 15,641 bytes/SHA-256 `2ef4f077a902459b93dcdaef6db1c608e97c89d64b8dacbb8cb378367150009e`; the test suite is 8,217 bytes/SHA-256 `c1bbe85ff16a76d2ea55dfcb0686d016b52634aa33687e6dd3f9ba4baf568159`; and the 1,201-byte expected output has SHA-256 `0ac6d4c262eb8088050b3562025e7156dd329832f8cb13b0fd57e4b7f6fe8381`. Combined QA `qa/COMPUTATION_LAB_003_QA.json` is 4,534 bytes/SHA-256 `a13bc301036c0d2cbfb6c92ab1423d2c2ca09a503bfa2a830a62832a0c4bf12f`. The backend suffix and eleven-file isolated replay pass exactly; next execute only the deterministic reader-build and publication sequence recorded in `00_control/CURSOR.json`.

### Live recovery note — computation Laboratory 2 source/execution/review closure, 2026-08-28

`D60-LAB02` / `O012-ORIG-LAB02` is closed at the source and executable layer.
The reader source
`source/id-ID/labs/computation-lab-002-chain-matrices-smith-normal-form.md`
is 16,529 bytes/548 LF lines/SHA-256
`532a1e4dacbfb33b680fbe7251accfc16fda933ed7f49f41e836fec15e096b5b`.
It contains 25 unique stable IDs, six tasks, one stable shared hint, and one
complete checked solution surface. Its only route mapping is `D60-R08`; it
does not claim singular-homology (`D60-R09`) or Laboratory 3 coverage.

The offline standard-library program is 22,052 bytes/SHA-256
`47735d76fb1c979d78daaa068a9a32f807ebb234c2da3e5e597f75861e27ae3c`;
the six-test suite is 7,891 bytes/SHA-256
`475872356d92f3f439ab353602c293b94db2324fe42209d30f2be6e51b13e2dc`;
and the 795-byte expected output has SHA-256
`965994efd39713b7591d43fab5d02bb43d200b68e67c4fa98a5b534452bb537c`.
Two test runs pass 6/6 and two program runs are byte-identical to the expected
output. Independent calculations certify the RP2 boundary matrices, Smith
diagonals `(1^5)` and `(1^9,2)`, homology `(Z,Z/2,0)`, exact `UAV=D`
certificates, the explicit order-two cycle, and the torsion-free sphere
control. Reordering faces or signed bases preserves the result; malformed
simplex and certificate inputs fail closed.

Static QA is 3,213 bytes/SHA-256
`7f8794282747fe30f3bd48fb0548f04f0fdbb6d3355d543c3e1cecb381360972`.
Independent code, mathematics, and source-language receipts have SHA-256
values `e213bd40b02007b194941f4d16b74dd8cd4661a30d0c0baa1390318fca2d7276`,
`a179756455bb4995183688897a9727d07b58ca30a07280057dd7882ed62068ce`,
and `5a564f57b75c499f792777f4ca6814158568372e6283531eed0ae33138aa0161`;
all finish at P1=P2=P3=0. Execution receipt SHA-256 is
`6af5e23469e32b5f98b3493c07e6a9beb4c5a18fd146cc3f211da9b9e56ad325`;
combined closure receipt `qa/COMPUTATION_LAB_002_QA.json` is 4,318 bytes with
SHA-256 `c084e575a621906ac7d8a1c6dca6f604de99b8e58a788409be17bb7392dd4319`.

Append-only admission is now closed: the exact 7,404-record predecessor is
preserved, the 142-record suffix is deterministic, and the cumulative backend
has 7,546 records/9,122,755 bytes with bundle SHA-256
`ac3a0377861ed2b728f9c7473579fdd4febe43e454a92f3ea06451e13d46c8f8`.
The 529-page reader build, Zenodo 0.31.4 publication/readback, and GitHub/Pages
integration at commit `8989fbd602f89d0a8d6c30bc7bac1980a74b2c99` are complete.
Begin D60-LAB03 without altering or republishing Laboratories 1–2 by themselves.

### Live recovery note — computation Laboratory 1 public in both lineages; Laboratory 2 next, 2026-08-28

`D60-LAB01` / `O012-ORIG-LAB01` is complete at
`source/id-ID/labs/computation-lab-001-monodromy-presentations.md`, 12,275
bytes/SHA-256
`165e2f9ba587714fb32a2f5a6432920a36493ebc6902d580f55df9c8ab4c65c4`.
The associated program, tests, and expected-output files are 8,818, 3,032, and
478 bytes with SHA-256 values
`a9c8875aeb2642921a2d152cd0ed316c6c67969a466240ada9836d3c42252628`,
`ae30ca6604b2a96b12c7df125fdcaa6deea00a9e4594f6b161d7d4785d9b949b`,
and `ddaa8015f314e53895c311e12be4d2d1dcaa1fa3f20def4ee112f28077a38717`.
Both program runs are byte-identical to the frozen output; both test runs pass
6/6. Aggregate source/execution/review QA is 4,258 bytes/SHA-256
`75dede0eaa0edbb22c75470dc641bdd10f95aac57c05331171ace4ac9e68aa2b`.

Append-only admission preserves the 7,273-record/8,840,132-byte prefix exactly,
adds 131 records/135,568 bytes, and ends at 7,404 records/8,975,700 bytes with
bundle SHA-256
`4740eb2ff83b4f9df3c0d90c2426ff77e652b23cad0bbe7763c54ebdefa60b4b`.
Cumulative receipt
`qa/BACKEND_APPEND_ONLY_COMPUTATION_LAB_001_CUMULATIVE_RECEIPT.json` is 9,727
bytes/SHA-256
`90f445294eea58aca5bcebe6acaff7293251b21e32aa25f3b62705e64cf8ab74`.

The successor HTML and PDF identities are stated in the status paragraph.
All ten appended PDF pages plus predecessor transition page 501 pass original-
detail inspection; desktop 1440×900 and mobile 375×812 browser checks show a
centered reader, zero page-level overflow, four local code scrollers on mobile,
zero unresolved fragments, zero external runtime assets, keyboard focus, and
zero console errors or warnings. Final build receipt is 6,798 bytes/SHA-256
`820019c2592c8af11d41a02215b4fb5805368760d926ecb06d4760f4dccf9106`.
Zenodo `0.31.3` is public at record `22142210`, DOI
`10.5281/zenodo.22142210`, in the existing concept DOI
`10.5281/zenodo.22061489`; all nine files passed two anonymous HTTP 200
byte/SHA-256 readback passes. Sanitized receipt
`release/zenodo-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-lab01/publication-receipt.json`
has SHA-256
`ef52c6362b65424c79991ffd35ede64b0ed64d96a0219577fe0df1016b25f830`.
GitHub content commit `a8311697800102ce65ce7f67752b0179ccaa9109`, tree
`4f438d7932f3576ae78be051ca210b5914e1eb30`, Pages run `33162255086`, job
`98819266824`, deployment `6139369092`, and successful status `17454891852`
pass. All 69 changed files/66,866,333 bytes, the commit-pinned reader, the
deployed Pages reader, and the predecessor matched exact anonymous bytes.
Sanitized receipt is 30,246 bytes/SHA-256
`bf9bb396135010ccdfe6ec950b46d84ec59eb6ddfc1c9624a841341fe15086bc`.
Begin `D60-LAB02`. Do not rebuild or reopen Laboratory 1 absent a newly
demonstrated defect.

### Live recovery note — mastery 108/108 and Zenodo 0.31.2 public, 2026-08-28

`D60-CA02` / `O012-ORIG-CA02` is complete at
`source/id-ID/mastery/cumulative-assessment-002-homology-excision-cellular.md`,
25,321 bytes/SHA-256
`2f8dc58eb4fb2da06e239d8e0979112c5f50c846f584900a2e7ea4999a8685ea`.
`D60-CA03` / `O012-ORIG-CA03` is complete at
`source/id-ID/mastery/cumulative-assessment-003-cohomology-degree-synthesis.md`,
26,074 bytes/SHA-256
`35c2c9a1b7edbeb1902245b567754e33f4720e11b48d2822bad7666a6a626894`.
Each contains exactly eight exercises, eight hints, and eight complete checked
solutions; both independent mathematics and source-language reviews pass with
P1/P2/P3 zero. Combined QA is 3,906 bytes/SHA-256
`24439975cfe1d877dbffdb2948afaa78839b43cd172b2a95cbf1bb0bee599932`.

Append-only admission preserves the 7,012-record/8,545,732-byte prefix exactly,
adds 261 records, and ends at 7,273 records/8,840,132 bytes with bundle
SHA-256 `97edc6371a0bf670ebdaaa4fab8618ec138ae25c4bf54ca9172139934ba0b464`.
Cumulative receipt
`qa/BACKEND_APPEND_ONLY_CUMULATIVE_ASSESSMENTS_002_003_CUMULATIVE_RECEIPT.json`
is 11,073 bytes/SHA-256
`61e5a3791ca4cacf7a2fbe0c09f5b638afd1c2c427f8784d04b96331903d53c7`.
`qa/ROUTE_MASTERY_CENSUS.json` is 141,526 bytes/SHA-256
`67a79a47f966d65862f5006e4255c620f7fc79a9fb02c51e4836cb578ff66977`:
84 ordinary items plus 24 cumulative items equal 108/108, with zero duplicate
solution IDs and zero validation errors.

The deterministic HTML
`output/html/roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03/index.html`
is 15,287,428 bytes/SHA-256
`417e50656ae0a61134c480f59df1bcd54d66a68c938d1d54f9c931ba37e2a5d6`.
The PDF is 8,915,996 bytes/501 A4 pages/SHA-256
`74ed9b5bf0f79a98693369dc7beba3e84ac81c711cc96b9951ae950ae9632a16`.
Final build receipt is 81,018 bytes/SHA-256
`596f0e89e8c4abe310019dca95f0e457e7b70983f490afba26291211af0f55b9`.
Desktop/mobile browser QA, 20-page visual and glyph-bound QA, deterministic
predecessor comparison, fonts, destinations, fragments, rights, privacy, and
hashes pass. The PDF remains untagged; native-MathML HTML is the primary
reflowable surface.

Zenodo `0.31.2` is public at record `22135136`, DOI
`10.5281/zenodo.22135136`, in concept `10.5281/zenodo.22061489`. Its exact
nine-file reader-first payload passed two anonymous HTTP 200 byte/SHA-256
readback passes. Sanitized receipt
`release/zenodo-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03/publication-receipt.json`
is 11,228 bytes/SHA-256
`d097cabe1c857b498ec0bf1dcca620e6cd957797ab70777ba229b6c3540a2871`;
transaction is 962 bytes/SHA-256
`66417a63b144f71fb356c9d42595178fdad6defc74e10c5df0b8d3448a38de69`.
No credential, authorization header, bucket URL, absolute local path, or
personal name is recorded. The privacy scanner's three credential-negative-test
literals were represented as semantically identical split byte expressions so
the release gate does not misclassify its own tests as leaked credentials.
GitHub content commit `657f21813ef39bd9e86558a2f4e16e79c23ce491`, tree
`2d7da6665cabbfe9ea8a0157cd533b53ff053b5c`, Pages run `33129294989`, job
`98714787548`, deployment `6133283357`, and status `17437766400` pass.
Anonymous codeload verification matched all 66 changed files/65,610,666 bytes
under delta-manifest SHA-256
`0df36a710e29600baa2978d99b60db030559e01bfc67d1f92951e491ffa2af94`;
the raw and Pages reader bytes match exactly and the predecessor remains exact.
Receipt
`00_control/GITHUB_PUBLICATION_RECEIPT_ROBERTS_001_030_FOMBERG_001_007_CA01_HINTS_R01_R06_CA02_CA03.json`
is 27,588 bytes/SHA-256
`b06804594412a9de0953120478ca8cf2d2e1c0f09f68cbce706e0930c02f2e6b`.
Begin computation lab 1 now.

### Live recovery note — ordinary mastery 84/84 public checkpoint, 2026-08-26

`O012-ORIG-HINTS-R01-R06` is complete and admitted. Source
`source/id-ID/mastery/ordinary-hints-r01-r06.md` is 28,698 bytes/410 LF
lines, contains 36 hint blocks and 43 stable IDs, and has SHA-256
`dc319cb191d709a5807f0c0792401f9faf2993ceede364764547f20bb4f69c2a`.
The static QA receipt is 16,616 bytes/SHA-256
`a0460dbed83242863fc1aab8290b76fac9cd39644276e132401e7d3e9198c33d`;
independent mathematics review is 19,289 bytes/SHA-256
`8ed5b3563976b415e1aa471f7cdeb3405888cbc70aec101bc02e4fab9e45de5a`;
independent source-language review is 18,324 bytes/SHA-256
`6c29009da4ee0380c878c3705dcd2a99cbe7a8495cc4b7f5ce456bb40f910968`.
All three pass with P1/P2/P3 zero. Each hint has one exact existing exercise
target and one exact existing complete solution; no prompt, solution, or solve
edge changed, and no Fomberg problem-bank expression was used.

Append-only admission preserves the 6,854-record/8,345,799-byte CA01 prefix
exactly, adds 158 records, and ends at 7,012 records/8,545,732 bytes with
bundle SHA-256
`7d723f9ef163303c7dde63d646dc8d5917c2450b1da5d24c87ef77bf4e4d664b`.
Receipt `qa/BACKEND_APPEND_ONLY_ORDINARY_HINTS_R01_R06_CUMULATIVE_RECEIPT.json`
is 10,252 bytes/SHA-256
`10e9d32848b950148983d0d8c38d6753a9956a674f657858b31dd257af5b2aa8`.
`qa/ROUTE_MASTERY_CENSUS.json` is 140,589 bytes/SHA-256
`068072d3c67aeed28d55fdb9947a3084e4028ba0b808e28f46c0657ba84d20ff`:
84/84 ordinary items, CA01 8/8, 92/108 total, 16 CA02/CA03 items remaining,
zero duplicate/reused solution IDs, and zero validation errors.

The deterministic successor HTML
`output/html/roberts-001-030-fomberg-001-007-ca01-hints-r01-r06/index.html`
is 15,026,881 bytes/SHA-256
`7ed278d73a324ba0a9e5acadedf448221b3791db7322fdf6d29225afd0124d2b`.
The PDF
`output/pdf/topologi-aljabar-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-id.pdf`
is 8,592,243 bytes/482 A4 pages/SHA-256
`4da7f1368c17423cd6845c36b7d5190dac98d515ecbd32467c0c59961dd9afcb`.
Final build receipt `qa/ROBERTS_001_030_FOMBERG_001_007_CA01_HINTS_R01_R06_BUILD_RECEIPT.json`
is 8,674 bytes/SHA-256
`e0192345c0a5bf75c508edb005c95e712ef6c70630e368feab01fcb7f9e0ce76`.
Desktop/mobile browser, visual, font, outline, named-destination, fragment,
language, rights, privacy, and deterministic-build checks pass. The PDF remains
untagged; the self-contained native-MathML HTML is the primary accessible
surface. GitHub commit `646769fb52a51e997f5409fc2148f8892508da1d`,
tree `5c70b30a7a3e2787a81932ae85d2a61878dd2e34`, Pages run `32933679761`,
job `98070707388`, deployment `6097650955`, and status `17342667144` pass.
Anonymous commit-pinned readback matched all 58 changed files/63,693,654 bytes
under delta-manifest SHA-256
`614dadebbe20a3c625ead1191e29ab704f7cd75981f84c92765406a24ec76ced`;
the new Pages HTML matches exactly and the predecessor CA01 HTML remains exact.
Receipt `00_control/GITHUB_PUBLICATION_RECEIPT_ROBERTS_001_030_FOMBERG_001_007_CA01_HINTS_R01_R06.json`
is 2,424 bytes/SHA-256
`8994550bcb000fdddaf9e348908acc9caa2166adae5b7419462c830b0c8260ba`.

Zenodo `0.31.1` is public at record `22106133`, DOI
`10.5281/zenodo.22106133`, in concept `10.5281/zenodo.22061489`. Its exact
nine-file, reader-first payload passed two complete anonymous HTTP 200
byte/SHA-256 readback passes. Sanitized receipt
`release/zenodo-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06/publication-receipt.json`
is 11,099 bytes/SHA-256
`c99b3d5c9c09fe719fdf64851ca584a6d6c8c570311d2312a164f76095252ebd`;
sanitized transaction is 952 bytes/SHA-256
`7b59ac5e6044e17eced4ec0b382c5cbf0fc903404717917b628b4a9deeb0f1ec`.
No credential, authorization header, bucket URL, absolute local path, or
personal name is recorded. Begin CA02 and CA03 next.

### Live recovery note — Cumulative Assessment 1 public checkpoint, 2026-08-26

`D60-CA01` / `O012-ORIG-CA01` is complete, frozen, and public. The reader source
`source/id-ID/mastery/cumulative-assessment-001-foundations-coverings-homotopy.md`
is 15,185 bytes/389 LF lines/34 stable IDs, SHA-256
`5888df0410ad7e8ccf50d8ea8092e43a42f6df94c242f7c09abe0616d972e6f8`.
It contains exactly eight original exercises, eight hints, and eight complete
solutions across `D60-R01`-`R07`; both independent reviews and static QA are
P1/P2/P3 zero. No Fomberg problem-bank prompt was copied or adapted.

The append-only extension preserves the exact 6,742-record Unit 007 prefix and
adds 112 records, ending at 6,854 records/8,345,799 bytes with bundle SHA-256
`51e75d06e620762e629e9e7408da4b0c32b3e337817d9d140fbbdfa438de2f57`.
The route census credits 56/108 required slots: 48 ordinary route slots and
eight CA01 slots. The remaining finite mastery work is 36 stable hints for
already solved `D60-R01`-`R06` pairs plus CA02 and CA03 (16 items); no new
ordinary prompts or solutions are required for that 36-slot closure.

The cumulative HTML is 14,958,219 bytes, SHA-256
`d71e2f3c0eb38b48fe4686a955ad555db3a407df8f18e41371d52908f0bdbbdf`.
The PDF is 8,358,561 bytes/477 A4 pages, SHA-256
`476b0de3bbb2cbfe03a151ac3060e121c5f89364e70b54d918ab270f4c965ade`.
Two deterministic builds agree; all 472 predecessor pages retain identical
visual/content signatures and extracted text. All 389 outline entries and all
2,873 named destinations resolve. Pages 472-477 pass 150 dpi visual inspection,
and the centered HTML passes 1440 x 900 plus 375 x 812 browser QA with no page
overflow or unresolved fragments. Final build receipt
`qa/ROBERTS_001_030_FOMBERG_001_007_CA01_BUILD_RECEIPT.json` is 7,842 bytes,
SHA-256 `22fef828b7963219759f85d11e409e0ebf957889d0fa76dc02ec04f3a707a9e0`.
GitHub commit `4b5f8f74bf361e45687d55fc31a95ea3e0c657ab`, tree
`7c5a24b240e62fb2fdb9679157ef045bd984630a`, Pages run `32924728855`, job
`98045214112`, and deployment `6096182721` are successful. The public Pages
reader and twelve commit-pinned witnesses match local bytes. Receipt
`00_control/GITHUB_PUBLICATION_RECEIPT_ROBERTS_001_030_FOMBERG_001_007_CA01.json`
is 5,039 bytes/SHA-256
`7361de7c9e08a2afa8c0565710828f7ea65e76c4cde0ff0958484621aed69987`.
Zenodo version `0.31.0`, record `22105179`, DOI
`10.5281/zenodo.22105179`, is published in unchanged concept
`10.5281/zenodo.22061489`; all nine files match local bytes anonymously.
Receipt
`release/zenodo-roberts-001-030-fomberg-001-007-ca01/publication-receipt.json`
is 5,080 bytes/SHA-256
`b55f98b6c7575fd1e3cc3b3afba3c1f348864cf3c32ec45f9c6b8b4dc8d7a625`.
Before hint admission, the route-census selector was corrected to reserve each
existing solution ID exactly once. The previous first-six rule advertised two
Route 6 prompt pairs that share one solution; no admitted graph or published
CA01 byte was affected. Corrected census
`qa/ROUTE_MASTERY_CENSUS.json` is 121,128 bytes/SHA-256
`d011e6f94eec2995d95ed2fe88833a94207a4087f50859d3a068d65c20ec4e41`
with zero validation errors; the exact decision receipt is
`qa/ROUTE_MASTERY_CENSUS_SELECTOR_CORRECTION.json`, 2,232 bytes/SHA-256
`96c293905148d511afce84805e4d47f59f1bc01480de9d0afde7636bb06d954f`.
Next executable action: begin the 36-hint ordinary-mastery closure. Source line
4186 remains the nominal post-Fomberg cursor; it is not authority to translate
beyond the selected span.

### Live recovery note — Fomberg Unit 007 local closure, 2026-08-26

Do not translate Fomberg lines 3518–4185 again. `O012-FOM-007`/`D60-R12`
translates the selected Section 1.13 cellular-homology span contiguously and
closes the admitted Fomberg source at exact line 4186. Reader
`source/id-ID/fomberg/units/fomberg-unit-007-cellular-homology.md` is 60,598
bytes/1,934 LF lines/72 stable IDs, SHA-256
`417b62c6c334b2f55965b623d8bfc8c3c94d4b2e109db149e42e294916673def`.
It preserves 15/15 source environments, 17 diagram groups, six verified
asset files, three proof repairs (`FOM-PR-13`–`15`), and six complete
exercise/hint/solution triples. The final independent math and
source/language reviews are P1/P2/P3 zero; static QA receipt
`qa/FOMBERG_UNIT_007_QA.json` is 16,998 bytes/SHA-256
`3db0476e5f954402a3f704090b5fea0d1a4a0d04e889b3062b048dbea8f51f1f`.

The append-only backend preserves the exact Unit 006 prefix (6,512 records,
7,855,910 bytes, bundle SHA-256
`377be644a38e6db06f8992113ea47b8fc172953254c9b1005493e0ad3b7bd4ad`) and
appends 230 records, ending at 6,742 records/8,213,649 bytes with cumulative
bundle SHA-256 `523b570517eb54720c50007aacc5d4eea525ea252b9ca1f6f45b027182354765`.
Semantic, cumulative, and deterministic replay validators pass; cumulative
receipt `qa/BACKEND_APPEND_ONLY_FOMBERG_UNIT_007_CUMULATIVE_RECEIPT.json` is
8,954 bytes/SHA-256 `6d1bf89439d0c4dae64005a64da2a2d9848153f229a2292b530c688a19cce364`.

The deterministic cumulative HTML is
`output/html/roberts-001-030-fomberg-001-007/index.html`, 14,885,069 bytes,
SHA-256 `87d58a5955954125c424ab1220a9c6aa7967a782a9bd739094a31ae0a50af5f6`.
The PDF is
`output/pdf/topologi-aljabar-roberts-001-030-fomberg-001-007-id.pdf`,
8,326,404 bytes, 472 A4 pages, SHA-256
`1beca2d03f04c1fcca7eb01bd2654567908febc1ba7941b459c06b90ef865c22`.
Two clean builds are byte-identical. Visual inventory and report cover PDF
pages 438–472 with zero clipping/overlap/margin defects; local browser checks
pass at desktop and mobile with zero page overflow, 440 resolved fragments,
15,945 MathML nodes, 159 figures, 19 embedded PNGs, zero console errors, and
two non-fatal instrumentation warnings. Build receipt
`qa/ROBERTS_001_030_FOMBERG_001_007_BUILD_RECEIPT.json` is 7,042 bytes/SHA-256
`bef3d7fbd0aa1290a34f6a942c0559130fd5b32a66531afb7f56d91cb148cc8e`.
Zenodo version `0.30.7`, record `22104150`, DOI
`10.5281/zenodo.22104150`, is published in concept
`10.5281/zenodo.22061489`; all nine public files match local bytes under
anonymous readback. Receipt
`release/zenodo-roberts-001-030-fomberg-001-007/publication-receipt.json` has
SHA-256 `3145ad59d3eae2935319e502b30e30fe62c31b1d7eaebab087b5f24b220f874f`.
GitHub commit `1c25c0b43ba605ff16cf95363f405455f78f29eb`, tree
`814d6d5a8ea5164928709a60e16ee13946970f52`, Pages run `32919363394`, job
`98029663052`, deployment `6095315253`, and status `17336537558` succeeded.
The public Pages reader and nine commit-pinned witnesses match local bytes.
Receipt
`00_control/GITHUB_PUBLICATION_RECEIPT_ROBERTS_001_030_FOMBERG_001_007.json`
is 4,214 bytes/SHA-256
`51eb8da851deb5aa6aba12b6655e16a54e321811b543e34c772bfa11fdb3fa98`.
The next executable work is the original proof/mastery/laboratory/capstone
closure; source line 4186 remains the resume cursor.

### Live recovery note — Fomberg Unit 006 closure and publication, 2026-08-26

Do not translate Fomberg lines 3123–3517 again. `O012-FOM-006`/`D60-R12`
translates Section 1.12 contiguously and closes at exact line 3518,
`\subsection{Cellular homology}`. Reader
`source/id-ID/fomberg/units/fomberg-unit-006-cellular-complexes.md` is 41,416
bytes/1,053 LF lines/55 stable IDs, SHA-256
`e8d4d5391f8cdf4e62a019f7a991d09e4b610633e8e660dec4e0ea2b61c538f7`.
It preserves all fourteen source environments, supplies seven independent
accessible SVG/PNG redraw pairs and six exercise/hint/full-solution triples,
and records thirteen correction/provenance events plus fifteen terminology
decisions. The final independent source-and-reader review is P1/P2/P3 zero;
static QA receipt `qa/FOMBERG_UNIT_006_QA.json` is 11,837 bytes/SHA-256
`ff9cdd26fadc775c485f64aa2b6e5ae1444a6925c73897386bcb2d75db4db5de`.

The append-only backend preserves the exact 6,309-record Unit 005 prefix and
appends 203 records, ending at 6,512 records/7,855,910 bytes/bundle SHA-256
`377be644a38e6db06f8992113ea47b8fc172953254c9b1005493e0ad3b7bd4ad`.
The cumulative receipt is
`qa/BACKEND_APPEND_ONLY_FOMBERG_UNIT_006_CUMULATIVE_RECEIPT.json`, 10,567
bytes/SHA-256
`2962fc0a5584c64a27aca24929e9f8b5ac4333ef311207af1c6725b7b94d4909`;
exact-prefix, semantic, cumulative, and deterministic producer replay pass.

Composite HTML
`output/html/roberts-001-030-fomberg-001-006/index.html` is 12,555,960
bytes/SHA-256
`80a7d092cb786e4d4f7ecab31ba40746cf59398db50f0adca50f2431746f7c92`;
PDF `output/pdf/topologi-aljabar-roberts-001-030-fomberg-001-006-id.pdf` is
6,723,586 bytes/452 A4 pages/SHA-256
`136dc7f6fa744e87fe067a96a36a8fbee8098aad9167629653bc085f6a718c37`.
Two clean builds are byte-identical. Desktop centering, phone-width reflow with
zero exposed page overflow, 15,273 MathML nodes, 142 semantic figures, PDF
pages 438–452, 27 embedded/subset/ToUnicode fonts, rights, privacy, and the
disclosed untagged-PDF limitation pass. Build receipt
`qa/ROBERTS_001_030_FOMBERG_001_006_BUILD_RECEIPT.json` is 10,169 bytes/SHA-256
`0347abd8312f8058a769a2b0b01c4d3605798c544c832e0fff82d84ade912829`.

Zenodo version `0.30.6`, record `22102865`, DOI
`10.5281/zenodo.22102865`, is published within concept
`10.5281/zenodo.22061489`; all nine public files match local bytes under
anonymous readback. Receipt
`release/zenodo-roberts-001-030-fomberg-001-006/publication-receipt.json` is
4,986 bytes/SHA-256
`ea94756cb1770d4627a55e374728de411fa710d65db69c1ed5d176b15c6acb0a`.
GitHub release commit `372f9d01d691393760779dc840b6d8c36ea2b025`, tree
`772a52a3150f0f1a654818e6c1031e715acd5228`, Pages run `32906265163`, job
`97990960689`, deployment `6093297209`, and status `17329343917` succeeded;
the public Pages HTML and nine commit-pinned source/release witnesses match
local bytes. Receipt
`00_control/GITHUB_PUBLICATION_RECEIPT_ROBERTS_001_030_FOMBERG_001_006.json`
is 4,195 bytes/SHA-256
`b6e1b10c91aeca726c60132eca46a53e9fbc57ba0a788fbeda7010fb50382d19`.
Unit 007 is now closed and must not be repeated. Its source audit
`qa/FOMBERG_UNIT_007_SOURCE_AUDIT.json` is 18,838
bytes/SHA-256
`1cae10108e5af2dc3c0a9b63dd76861b7c44f42087f3ff5ec158a8d69b68b159`.
It binds exact lines 3518–4185 (26,533 bytes/SHA-256
`a22afacfdbecdfad48942421412c4cff1c0f317eb77f18253578125a5d0d7ce2`),
15 semantic environments, 17 conceptual diagram groups, zero source
exercises, eight exact correction flags, and mandatory repairs `FOM-PR-13`–15.
The next source text after this terminal selected bridge is line 4186,
`\subsection{Extras before cohomology}`. All three repairs and six original
mastery triples passed independent review; line 4186 is the resume cursor for
the original proof/mastery/laboratory/capstone closure, not a further Fomberg
translation unit.

### Live recovery note — Fomberg Unit 005 closure and publication, 2026-08-25

Do not translate Fomberg lines 2847–3122 again. `O012-FOM-005`/`D60-R12`
translates Section 1.11 contiguously as an optional degree cross-check while
retaining the additive local-degree material. It closes at exact line 3123,
`\subsection{Cellular complexes}`. Reader
`source/id-ID/fomberg/units/fomberg-unit-005-degree-maps-local-degree.md` is
40,274 bytes/1,150 LF lines/52 stable IDs, SHA-256
`ad6e31291e3df97b81f7e5a30144ca27157f907291e74f4d49c09a0620487075`.
It supplies complete separately marked repair `FOM-PR-12`, six
exercise/hint/full-solution triples, one reflowing semantic diagram, eleven
deduplicated correction/proof-omission events, and twenty terminology
decisions. The final independent source-and-reader review is P1/P2/P3 zero;
static QA receipt `qa/FOMBERG_UNIT_005_QA.json` is 6,268 bytes/SHA-256
`874d9ef02875d4fbc28458e56b2c2894be8c990a9fd1c333a0327ccd2d3c4964`.

The append-only backend preserves the exact 6,113-record Unit 004 prefix and
appends 196 records, ending at 6,309 records/7,565,974 bytes/bundle SHA-256
`c7b153cd217ac7dee87f4c399815c4d2bb51cff872c71665fe395efb3ffd95fa`.
The cumulative receipt is
`qa/BACKEND_APPEND_ONLY_FOMBERG_UNIT_005_CUMULATIVE_RECEIPT.json`, 7,558
bytes/SHA-256
`0e7e3a4595697e55d2451314481be971b9b7a95555309a596ec4155660028b9f`;
exact-prefix, semantic, cumulative, and deterministic producer replay all pass.

Composite HTML
`output/html/roberts-001-030-fomberg-001-005/index.html` is 8,353,769
bytes/SHA-256
`d726c8d8a565172fb620233080f60e2ccbde4386d6fa03b099bf6219645aea90`;
PDF `output/pdf/topologi-aljabar-roberts-001-030-fomberg-001-005-id.pdf` is
4,035,750 bytes/437 A4 pages/SHA-256
`b0b0441ae16ad0065dc50dfc3ba36df49932efbdf939dc048cd332dc881f931a`.
Two clean HTML/PDF builds are byte-identical. Desktop centering, phone-width
reflow with zero exposed page overflow, 14,883 MathML nodes, 135 semantic
figures, PDF pages 425–437, nine image/smask pairs, 27
embedded/subset/ToUnicode fonts, rights, privacy, and the disclosed untagged-PDF
limitation pass. The build receipt is
`qa/ROBERTS_001_030_FOMBERG_001_005_BUILD_RECEIPT.json`, 10,205 bytes/SHA-256
`0d9d947a65982b84c5b0e2d2922fda2ab091c4ee627d7249abfd2aa948b79993`.

Zenodo version `0.30.5`, record `22098820`, DOI
`10.5281/zenodo.22098820`, is published within concept
`10.5281/zenodo.22061489`; all nine public files match local bytes under
anonymous readback. Receipt
`release/zenodo-roberts-001-030-fomberg-001-005/publication-receipt.json` is
4,962 bytes/SHA-256
`635a2b4afbdbd6c39853481c422dce2eee0f19282f47857f65a62289fc0af6a9`.
GitHub commit `5f089fc8ea886f72b1723ec4101e36ee819c11ee`, tree
`c2e4d2add843378cfd3f96f92c049e614316f95e`, Pages run `32865486189`, job
`97859601129`, deployment `6086351300`, and status `17311157789` succeeded.
The Pages reader and nine commit-pinned witnesses match local bytes. Receipt
`00_control/GITHUB_PUBLICATION_RECEIPT_ROBERTS_001_030_FOMBERG_001_005.json`
is 4,146 bytes/SHA-256
`3611bc8e244267fee516ce24284b38895fc614f1411657e417882b587f8b2b0a`.
Continue with Section 1.12 at line 3123 as the cellular-complexes/homology
bridge in `D60-R12`.

### Live recovery note — Fomberg Unit 004 local closure, 2026-08-25

Do not translate Fomberg lines 1923–2846 again. `O012-FOM-004`/`D60-R11`
translates Sections 1.7–1.10 contiguously and closes at exact line 2847,
`\subsection{Degree maps}`. Reader
`source/id-ID/fomberg/units/fomberg-unit-004-excision-mayer-vietoris-naturality-comparison.md`
is 87,293 bytes/2,364 LF lines/117 stable IDs, SHA-256
`2c04d647b58afe044f5549bcba9ad3572075775711bb3aaec45d0e94fe3d3e91`.
It supplies complete separately marked repairs `FOM-PR-05`–`FOM-PR-11`, seven
exercise/hint/full-solution triples, three original SVG masters plus accessible
PNG reader assets, and 24 deduplicated correction/proof-omission events. The
final independent source-and-reader review finishes at P1/P2/P3 zero; static
source/reader QA receipt is `qa/FOMBERG_UNIT_004_QA.json`, 7,910 bytes/SHA-256
`d4c86d7efbd9837330c4e24121d5dbd49252c11f1c29daa77e13e64bc3ff0c21`.

The append-only backend preserves the exact 5,747-record Unit 003 prefix and
appends 366 records, ending at 6,113 records/7,284,299 bytes/bundle SHA-256
`902eb71aa8a8b25e824ebe9ddae556e914e370d603382f28860392d6e186baba`.
The cumulative receipt is
`qa/BACKEND_APPEND_ONLY_FOMBERG_UNIT_004_CUMULATIVE_RECEIPT.json`, 6,915
bytes/SHA-256
`1cfc03c48d504ae7a9a39e1ea17819ae0cd462135fcb885168f2f48a5e0717f4`;
exact-prefix, semantic, cumulative, and deterministic producer replay all pass.

Composite HTML
`output/html/roberts-001-030-fomberg-001-004/index.html` is 8,155,605
bytes/SHA-256
`cd620d5557ff05fb81fb9cf044e8bd4848a6f92ef8fcd06078b8a124f6e79326`;
PDF `output/pdf/topologi-aljabar-roberts-001-030-fomberg-001-004-id.pdf` is
3,964,018 bytes/424 A4 pages/SHA-256
`bbe4b2392991ace6922230374833bf0982e00a8b6d2fddb94a990b663c8440bf`.
Three clean HTML/PDF builds are byte-identical. Desktop centering, phone-width
reflow with zero exposed overflow, 14,396 MathML nodes, 134 semantic figures,
all PDF pages 398–424, nine image/smask pairs, 27 embedded/subset/ToUnicode
fonts, rights, privacy, and the disclosed untagged-PDF limitation pass. The
build receipt is `qa/ROBERTS_001_030_FOMBERG_001_004_BUILD_RECEIPT.json`,
10,029 bytes/SHA-256
`d59e54ab6b9d370a8335a20564b5c2998ef1555f0b5d41a69cf3d0c8405527e1`.
Zenodo version `0.30.4`, record `22097007`, DOI
`10.5281/zenodo.22097007`, is published within concept
`10.5281/zenodo.22061489`; all nine public files match local bytes under
anonymous readback. Receipt
`release/zenodo-roberts-001-030-fomberg-001-004/publication-receipt.json` is
4,946 bytes/SHA-256
`006a57953f58455da6f175233186e987e9ec37d9f9d80c23eab9c89d2532e4f7`.
GitHub commit `465160690dcc3b8c92f0a7df2016027ee1b0d118`, tree
`43175e49e17a52018279b70e09942786ac728990`, Pages run `32854329469`, job
`97822496048`, deployment `6084317344`, and status `17305874189` succeeded.
The Pages reader and nine commit-pinned witnesses match local bytes. Receipt
`00_control/GITHUB_PUBLICATION_RECEIPT_ROBERTS_001_030_FOMBERG_001_004.json`
is 4,376 bytes/SHA-256
`24bbfacc99e67f314c5168d5ae073b399840a91c23e859d03035a55d49e74c09`.
Continue with Section 1.11 at line 2847 as the optional degree cross-check in
`D60-R12`.

### Live recovery note — Fomberg Unit 003 closure and publication, 2026-08-25

Do not translate Fomberg lines 1291–1922 again. `O012-FOM-003`/`D60-R10`
translates Sections 1.5–1.6 contiguously and closes at exact line 1923,
`\subsection{Excisions}`. Reader
`source/id-ID/fomberg/units/fomberg-unit-003-exact-sequences-relative-homology.md`
is 65,540 bytes/1,773 LF lines/125 stable IDs, SHA-256
`2571f62b977c00bff20e04756925a73497c0129f8c987940db0e1a649177f6b9`.
It supplies the complete `FOM-PR-04` long-exact-sequence repair, six
exercise/hint/full-solution triples, six original SVG masters plus PNG reader
assets, and retains one explicit forward proof dependency that closes only
after excision. Exact, relative, and integrated independent reviews finish at
P1/P2/P3 zero; the authoritative 125-ID reconciliation is
`qa/fomberg-unit-003/INTEGRATED_REVIEW_COUNT_RECONCILIATION.json`.

The append-only backend preserves the 5,342-record Unit 002 prefix and appends
405 records, ending at 5,747 records/6,649,486 bytes/bundle SHA-256
`9e416c70e69dea1601bd79a259c278a9cfdfe5dca10d40b7bbc8e67d9ffba76b`.
The cumulative receipt is
`qa/BACKEND_APPEND_ONLY_FOMBERG_UNIT_003_CUMULATIVE_RECEIPT.json`, 7,362
bytes/SHA-256
`219bd0a43509cf2be98eefb19a13cd033db4a2e2e0deafeee9e3d80a532dc157`;
static QA, exact-prefix validation, semantic validation, and deterministic
producer replay all pass.

Composite HTML
`output/html/roberts-001-030-fomberg-001-003/index.html` is 7,190,228
bytes/SHA-256
`484a2a501df79b1810567810d0b454a18298a4cb43ef466c4e082622216b9542`;
PDF `output/pdf/topologi-aljabar-roberts-001-030-fomberg-001-003-id.pdf` is
3,550,987 bytes/397 A4 pages/SHA-256
`57382750a561667bf02eb98bd7f4806618c3a785f4ca18ceb4c6679c46543b4b`.
Two clean HTML and PDF builds are byte-identical. Desktop and mobile reflow,
zero exposed page overflow, 13,466 MathML nodes, 115 semantic figures, all new
PDF pages 377–397, six image/smask pairs, 27 embedded/subset/ToUnicode fonts,
rights, privacy, and the disclosed untagged-PDF limitation pass.

GitHub commit `c8fcc0e575de9ac902a6ca79eee479462cff2f27`, tree
`4d84a447edcd8995333f3be10eabb9173bacd426`, Pages run `32797456049`, job
`97651554751`, deployment `6074581337`, and status `17279967348` succeeded.
The Pages reader plus nine critical commit-pinned source/release witnesses
matched local bytes; receipt
`GITHUB_PUBLICATION_RECEIPT_ROBERTS_001_030_FOMBERG_001_003.json` records the
checks. Zenodo version `0.30.3` is record `22088708`, DOI
`10.5281/zenodo.22088708`, within existing concept
`10.5281/zenodo.22061489`; all nine public files matched local bytes and the
organization appears exactly once, only in contributor metadata. Continue at
Fomberg line 1923 through Sections 1.7–1.10 (`D60-R11`, through line 2846).

### Live recovery note — Fomberg Unit 002 closure and publication, 2026-08-24

Do not translate Fomberg lines 615–1290 again. `O012-FOM-002`/`D60-R09`
translates Sections 1.3–1.4 contiguously and closes at the exact next cursor,
line 1291 (`\subsection{Exact sequences}`). Reader
`source/id-ID/fomberg/units/fomberg-unit-002-singular-homology-homotopy-invariance.md`
is 44,407 bytes/1,342 LF lines/95 stable IDs, SHA-256
`0851ab7d9f5ded1e836a0e73aa055fbd28b82998208d8136ec0cf4757747435c`.
It closes `FOM-PR-01`–`FOM-PR-03`, contains six solved mastery triples, and
has three independent P1/P2/P3-zero reviews. The adverse ledger ends at
`O012-ADV-0456` and terminology at `O012-TERM-0400`.

The append-only backend preserves the 5,060-record Unit 001 prefix and appends
282 records, ending at 5,342 records/6,040,123 bytes/bundle
`83d98f1b271c5e62334a072354f1be1c4a1535ed26c8a403223e89773bb1eba1`.
The controlling cumulative receipt is
`qa/BACKEND_APPEND_ONLY_FOMBERG_UNIT_002_CUMULATIVE_RECEIPT.json`, SHA-256
`6c821ced04e7ba57f396089939994344522b26817f43c195d1fc8c4a365dbcc1`;
static, semantic, prefix, and deterministic replay all pass.

Composite HTML
`output/html/roberts-001-030-fomberg-001-002/index.html` is 5,254,038
bytes/SHA-256
`1f7618003e3ff273a4f1e2d97b5a81fd320f76640c475cae845ed38793fbeccd`;
PDF `output/pdf/topologi-aljabar-roberts-001-030-fomberg-001-002-id.pdf` is
2,399,760 bytes/SHA-256
`7dc8ac1db0b03ed1d9d94fe2c3491b631d3fb8bcec869997889d67d70236ef82`,
376 A4 pages. Build receipt SHA-256 is
`2339089281ebf3be33592cb484e7e0951a87ec66d458d8c278870202897f2f0c`.
Desktop centering, zero exposed mobile page overflow, offline MathML, links,
all new PDF pages, fonts/ToUnicode, rights, privacy, and disclosed PDF tagging
limitation pass.

GitHub commit `085934c001a5acde8b3279de5bea6a69803e2c95`, tree
`4dd6e21cfafd582c7362c1448d85c414f2dcf59b`, Pages run `32781982738`, job
`97605825173`, and deployment `6072165217` succeeded; the Pages reader, raw
PDF and source, and all nine commit-pinned release artifacts match local bytes.
Zenodo version `0.30.2` is record `22087423`, DOI
`10.5281/zenodo.22087423`, in concept `10.5281/zenodo.22061489`; all nine
public files match local size and SHA-256. Continue with Fomberg Sections
1.5–1.6 at line 1291 as `D60-R10`; do not reopen this boundary.

The requested cleanup gate archived and then removed only two superseded
Fomberg Unit 001 render directories (29 files/10,932,554 bytes); current Unit
002 renders, the terminology witness, sources, releases, and all controlling
evidence were retained. The verified ZIP is recorded in
`CLEANUP_RECEIPT_2026-08-24_SUPERSEDED_FOMBERG_001_RENDERS.json`.

### Live recovery note — Fomberg Unit 001 local closure, 2026-08-24

Do not translate Fomberg lines 31–614 again. `O012-FOM-001`/`D60-R08`
translates Sections 1.1–1.2 contiguously and closes at the exact next cursor,
line 615. Reader
`source/id-ID/fomberg/units/fomberg-unit-001-delta-complexes-simplicial-homology.md`
is 34,773 bytes/1,073 LF lines/87 stable IDs, SHA-256
`d9b64140f9340c75bc34c12bc02ee843d87de3566e331c50c2374075718aa2c6`.
Its audit is admissible after documented repairs; independent review and final
QA are P1/P2/P3 zero. The adverse ledger ends at `O012-ADV-0425` and the
terminology ledger at `O012-TERM-0393`.

The append-only backend preserves the immutable Roberts terminal prefix at
4,761 records/5,213,679 bytes/bundle
`51b8c7f611560b9b5e88e97b3a943b54e0eb687c703f0cd34c1a3d164e4fb920`.
It appends exactly 299 Fomberg Unit 001 records and finishes at 5,060
records/5,658,648 bytes/bundle
`17f57575a062025e434e79f7f3797d05de1a41e520202521ae39a409d4b6450d`.
Static QA, semantic validation, prefix preservation, producer replay, and
cumulative deterministic replay pass; controlling receipt is
`qa/BACKEND_APPEND_ONLY_FOMBERG_UNIT_001_CUMULATIVE_RECEIPT.json`, SHA-256
`d110ce29513a9a9a789d6baf5e2b513d8c971c7d4e6d67e5943eed440c48bc50`.

Composite HTML
`output/html/roberts-001-030-fomberg-001/index.html` is 5,029,788 bytes/SHA-256
`2b64e8bec1dd5e1689ef6569360fec896ef87a683c7ba291a3780e27084a7390`;
PDF `output/pdf/topologi-aljabar-roberts-001-030-fomberg-001-id.pdf` is
2,322,978 bytes/SHA-256
`fb81f2b2c0f73c17c4e3be4eaae164eaeaeb0c4ff0661580acfc7aa9b6d5f749`,
362 A4 pages. Two builds are byte-identical. Live browser QA first exposed a
586/587-pixel page-overflow failure at a 375-pixel mobile content width; the
builder-only body-wrap repair was then rerun and now passes at 375/375 with
zero exposed contributors while preserving 268 local MathML scrollers. A
final audit also caught literal Markdown at the first Roberts notice boundary;
the builder now inserts the missing blank separator and fails closed unless
the real `o012-rbt-u001-notice` anchor survives in both readers. The root
license is now an explicit Roberts-only CC BY 4.0 / Fomberg-and-integrated CC
BY-SA 4.0 scope matrix rather than a misleading repository-wide Roberts notice.
Desktop centering, links, native MathML, offline closure, PDF title/transition
and every Fomberg page, fonts/ToUnicode, rights, privacy, and disclosed PDF
tagging limitation pass. Build receipt SHA-256 is
`a830567918c16d12bebaef3da8f8ad1a05f79f28c332d57f101a5b0d7f79bde9`.
This boundary is public on GitHub commit
`3371ae5b169c8face819b366aff2be4f198d73ec`, tree
`e003fc2efb5945486ef09655a80b4eea5c76e32f`, and successful Pages run
`32748430067`; the deployed reader and all nine commit-pinned release files
match local bytes and hashes. GitHub receipt
`00_control/GITHUB_PUBLICATION_RECEIPT_ROBERTS_001_030_FOMBERG_001.json` is
3,230 bytes/SHA-256
`86674fc0bff2d05cbc714ac396fdfb803838c85813275fc00282808fedc55363`.
Zenodo version `0.30.1` is public as record `22084021`, DOI
`10.5281/zenodo.22084021`, in the existing concept DOI
`10.5281/zenodo.22061489`; all nine files passed anonymous exact-byte readback.
Zenodo receipt
`release/zenodo-roberts-001-030-fomberg-001/publication-receipt.json` is 4,877
bytes/SHA-256
`32b616b6f2f2932d21299cee1ec9cd663d5c29447a068d416510a702e3e91c97`.
The next executable action is translating Fomberg lines 615–1290.

### Live recovery note — Roberts local closure, 2026-08-24

Do not translate any Roberts span again. Units 26–30 are admitted in order and
the Roberts cursor is at EOF after `Notes.tex:6368`; nominal next line is 6369.
Final append-only backend: 4,761 records, 5,213,679 bytes, bundle SHA-256
`51b8c7f611560b9b5e88e97b3a943b54e0eb687c703f0cd34c1a3d164e4fb920`.
Its semantic and cumulative validators both replay PASS; controlling receipt
`qa/BACKEND_APPEND_ONLY_UNIT_030_CUMULATIVE_RECEIPT.json` is 3,976 bytes,
SHA-256
`d4f7c7310ae22b8fc53d354b72beefad637ac353be418b9fbc56ddd8cd0a65f7`.
Final reader HTML is 4,861,791 bytes/SHA-256
`ed9da5653b3eacf7418d6e08760fcd2ecff4d75799c47f08689b940798099891`;
PDF is 2,257,988 bytes/SHA-256
`b9d37776c64541123345c7b28fd26df161b878e8c105c16670455fd532dc08a4`,
351 A4 pages. Two clean builds are byte-identical. Desktop and mobile browser
geometry, every Unit 30 page, links, IDs, assets, MathML, PDF fonts, rights,
privacy, and disclosed PDF tagging limitation pass. Build receipt
`qa/UNITS_001_030_BUILD_RECEIPT.json` is 12,488 bytes/SHA-256
`15ce778ae5b85934424b3da22dcbec99f15df30746bb01630aaa4494cb3eace7`.
The existing-lineage GitHub/Pages and Zenodo publication plus anonymous byte
readback is complete. The next executable action is Fomberg line 31, translating
Sections 1.1–1.2 through line 614 as the first coherent component unit.

The task-local cleanup requested on 2026-08-24 is complete and independently
reverified. Archive
`<workspace>/old stuff/algebraic-topology-id_disposable-render-readback-caches_20260824T0630_CEST.zip`
is 135,697,838 bytes/SHA-256
`ddd9d608b630bea5596c53935ee93f2f100018fca910cac15d1697fe8e5b7906`.
It contains 522 disposable source entries plus its manifest; all entry paths,
sizes, and SHA-256 values match. All 20 archived loose roots are absent, while
canonical sources, authorities, backend, controls, receipts, current readers,
and publication artifacts remain. Exact details are in
`CLEANUP_RECEIPT_2026-08-24.json`.

Three Python bytecode files were recreated by later bounded validation and
were separately closed before production resumed. Archive
`<workspace>/old stuff/algebraic-topology-id_recreated-python-cache_20260824T095607_CEST.zip`
is 93,895 bytes/SHA-256
`f570c5885bed9231576df78cf084a9d4e0b7bd059f6e929812660a3c0d35ed66`;
all three entries were reopened and matched by path, size, and SHA-256 before
their exact loose files and now-empty `scripts/__pycache__` directory were
deleted. The current composite visual-QA renders were retained because they
remain active evidence. Exact details are in
`CLEANUP_RECEIPT_2026-08-24_RECREATED_CACHE.json`.

The Fomberg authority/build gate is now genuinely closed at 55/55 PASS. The
old PASS was rejected because the provisional CC0 `commath` shim printed
literal optional-size syntax for `\del[4]` and `\del[1]` on pages 10 and 35.
The repaired 1,346-byte overlay supports every enumerated manual size 1–4;
two independent clean three-pass builds are byte-identical at 664,609 bytes,
SHA-256
`f0f8f815423dbdc3b368b48a5972bfc62be87ae8b5c4bfcd1b7a74b8871417ff`.
Final passes have zero tracked warnings/errors, the malformed literals are
absent, and official-versus-rebuilt pages 1, 3, 10, 20, 30, 35, 39, 40, and
57 pass visual comparison. Exact gate receipt:
`qa/FOMBERG_AUTHORITY_BUILD_GATE_QA.json`, 3,402 bytes/SHA-256
`110ae5058f254f780812fa12e51e73cc6d1f1e6e03a319dbdfb18ecedf79fe71`.
The selected translation witness remains exactly lines 31–4185, Sections
1.1–1.13, physical pages 1–39; Section 1.14 begins on page 40.

## Current verified Roberts Units 001–030 local boundary (2026-08-24)

- Units 26–30 cover `Notes.tex:5612–6368`; the cumulative Roberts edition covers lines 134–6368 and ends at `\end{document}`. Final Unit 30 reader `source/id-ID/units/unit-030-lecture-030.md` is 23,008 bytes/729 LF lines/47 stable IDs, SHA-256 `88da8cf71d0f81328bdd65b0dea7d54c48655ed8836e230eaed821796b61b08d`. Its audit is SHA-256 `177c4306e5db636e0294e85278904c186099d069f209474a472d2615b0d5a4cf`; independent review is SHA-256 `58db70bbd6538961e8bfc0c809d00b7b539115147b2826dc46d97e5b77ba712e`; final `qa/UNIT_030_QA.json` is P1/P2/P3 zero at 8,378 bytes/SHA-256 `bef6fe6704084ac02386bb477b7b0082e02921d3d722955e1366e7d0b9247753`.
- Append-only replay preserves the immutable Unit 29 prefix at 4,596 records/5,001,266 bytes/bundle `49c599010ebee2223225f643cd09a53bea882b8064024d5189e6e15f648195d8`, appends exactly 165 canonical Unit 30 records, and finishes at 4,761 records/5,213,679 bytes/bundle `51b8c7f611560b9b5e88e97b3a943b54e0eb687c703f0cd34c1a3d164e4fb920`. Both live validators and producer replay pass; 4,761 IDs are globally unique and 50,822 reference edges resolve.
- Cumulative HTML `output/html/units-001-030/index.html` is 4,861,791 bytes/SHA-256 `ed9da5653b3eacf7418d6e08760fcd2ecff4d75799c47f08689b940798099891`: 1,651 unique DOM IDs, 337 resolved fragment links, 11,787 native MathML nodes, 65 semantic figures, no runtime external assets or raw-TeX fallback, centered desktop geometry, and zero page-level mobile overflow. PDF `output/pdf/topologi-aljabar-unit-001-030-id.pdf` is 2,257,988 bytes/SHA-256 `b9d37776c64541123345c7b28fd26df161b878e8c105c16670455fd532dc08a4`, 351 A4 pages, `/Lang=id-ID`, all 27 font objects embedded/subset/ToUnicode, with its untagged limitation disclosed. Two clean builds are byte-identical; title and pages 343–351 pass original-resolution visual QA.
- GitHub content commit `dd46acdeb222a4cb4b8879af05e7c929111372ff`, tree `465e6d7daf67f2bdadf3474d120deb3d834e82ae`, is public. Pages run `32699844696`, job `97348985094`, succeeded. A commit-pinned anonymous codeload reconstruction matched all 131 release-delta files (48,420,823 bytes) under canonical delta-manifest SHA-256 `1555583be9a2ee05125a594629f38e49eeb876912209b83c035f8011d5aa2c95`; commit-pinned raw and deployed Pages HTML both match 4,861,791 bytes/SHA-256 `ed9da5653b3eacf7418d6e08760fcd2ecff4d75799c47f08689b940798099891`. Receipt `00_control/GITHUB_PUBLICATION_RECEIPT_UNITS_001_030.json` is 3,650 bytes/SHA-256 `d9cc893df5206fe82b3ec70ce74e702320a8016597e24e1ab7ccd316be4e2e67`.
- Zenodo version `0.30.0` is public at record `22077025`, DOI `10.5281/zenodo.22077025`, within existing concept `10.5281/zenodo.22061489`. Its nine reader-first files total 8,060,582 bytes; PDF, HTML, source/backend ZIP, QA/provenance ZIP, LICENSE, README, rights, manifest, and checksums each passed two anonymous HTTP 200 byte/SHA-256 readbacks. Metadata is CC BY 4.0, `ind`, exact Roberts-30/30/composite-partial scope, source creator/editor/provenance/non-endorsement intact, and no umbrella-title pollution. Receipt `release/zenodo-units-001-030/publication-receipt.json` is 4,059 bytes/SHA-256 `30f8c191eaf6a75cf5a96a0d301357959a2f53089a2f30af6b0ad65cdd025187`.

## Preserved Units 001–025 boundary (2026-08-24)

- Unit 25 covers Roberts `Notes.tex:5370–5611`; the 12,732-byte LF-normalized source span has SHA-256 `d05781ae58b1b6fd6174d030e52ca9ee6a08048be96f7c103e5be8de473b60b0`. Reader `source/id-ID/units/unit-025-lecture-025.md` is 36,578 bytes/1,104 LF lines/59 stable IDs, SHA-256 `df72add4e57236b51ff7d2a0c99af4b65299365874163cb334be5d0988c0f769`. The sole independent finding was a terminology P3, resolved before admission; final review and `qa/UNIT_025_QA.json` are P1/P2/P3 zero.
- Cumulative HTML `output/html/units-001-025/index.html` is 4,112,563 bytes/SHA-256 `38cd8437f3b4235ac6269f4e3365123fa06485269d35a424ad4f5ddd589025c1`: 1,361 unique IDs, 296 resolving fragments, 10,118 native MathML nodes, 62 semantic figures, no raw fallback or external runtime dependency, centered desktop layout, and zero page-level mobile overflow with 201 wide MathML objects contained in local scrollers. PDF `output/pdf/topologi-aljabar-unit-001-025-id.pdf` is 1,972,209 bytes/SHA-256 `581d62162633a6624687517c5cf1595f5fc02a2701c2222b279711e0520b9a3f`, 298 A4 pages, `/Lang=id-ID`, all 27 font rows embedded/subset/ToUnicode, with its untagged limitation disclosed. Two builds are byte-identical; every Unit 25 page plus title/transition passed visual inspection, and root independently inspected pages 287, 292, and 298.
- Final append-only backend validation passes with three nested immutable boundaries: Unit 24 cumulative 3,723 records/3,726,427 bytes/bundle `ffa8c7cb45b6d8170d7bc83df24ec487fd0c2777297b55eff2d5e7b3ae63fe25`; Unit 25 semantic 3,896 records/3,996,359 bytes/bundle `55372b9c2853fa479e731c73c407b234ad2f1219e07efbedbad2a99f1e2abf47`; and Unit 25 cumulative 3,913 records/4,007,903 bytes/bundle `8b50629f25c5fcbedb6d5547f8f7151c622aa90e04f71583008bd176058a4f78`. The final receipt is `qa/BACKEND_APPEND_ONLY_UNIT_025_CUMULATIVE_RECEIPT.json`, 7,562 bytes/SHA-256 `eacee8cad8ffe460af5f50a9be16f5c02b0671a686209e7d0073e10b2a98a2c1`; the replay-compatibility receipt is SHA-256 `6b4ef92a4c3ad4ec2190d7f1bedac6c118ff9033a1bb6257bd96d48f86dae1f2`. Both semantic and cumulative validators pass on the live final tree. The build receipt is `qa/UNITS_001_025_BUILD_RECEIPT.json`, 7,729 bytes/SHA-256 `dd2fa5b52ed84ac939c33cfa5b9f68be4b904b014321abcb54c2ae664d0f9727`.
- GitHub commit `24aee490d52d44e5b56d6fc4a9b337dcf3573ae5`, tree `aad55b5d0c47b60f77d0517b09c47efbd1ebda91`, is public. Pages run `32684818822`, job `97307868869`, deployment `6055747095`, and status `17211657786` succeeded. The 38-file release delta was anonymously reconstructed from commit-pinned codeload archives under manifest SHA-256 `1d4680573cc060b8c7939393f1b4e0699e4a0262ef95f59f79158b1892845738`; raw and deployed HTML both match 4,112,563 bytes/SHA-256 `38cd8437f3b4235ac6269f4e3365123fa06485269d35a424ad4f5ddd589025c1`. Receipt `00_control/GITHUB_PUBLICATION_RECEIPT_UNITS_001_025.json` is 14,515 bytes/SHA-256 `b23867e93ebeba1e101f285f1d9bf47f2fd6e7f08af105c930810eb16d88f70f`. Zenodo remains clean through Unit 24 at DOI `10.5281/zenodo.22074233`; no duplicate concept or unnecessary one-unit version has been created.

## Preserved Units 001–024 and Zenodo boundary (2026-08-24)

- Unit 24 covers Roberts `Notes.tex:5113–5369`; the 12,837-byte LF-normalized source span has SHA-256 `b2128930a56a0a8c04c327a397e72e21b215ffe742bb684e8dd166f0e04b0aea`. Reader `source/id-ID/units/unit-024-lecture-024.md` is 43,085 bytes/1,156 LF lines/60 stable IDs, SHA-256 `993ad0c3493caff6bd15ab2bcf435f6cbb1f49ed9a1e11bc1009d649ae2d3647`. The sole independent finding was an audit-only line locator (`5182` instead of `5173`), repaired and recorded before admission; the reader remained mathematically unchanged. Final independent review is P1/P2/P3 zero and `qa/UNIT_024_QA.json` passes all 14 gates.
- Cumulative HTML `output/html/units-001-024/index.html` is 3,927,104 bytes/SHA-256 `28a84406de9e196070965920a7f7937177197977f9ddf118f0f8b07d464cbf0f`: 1,295 unique IDs, 288 resolving fragments, 9,669 native MathML nodes, 60 semantic figures, no raw fallback/runtime dependency, centered desktop layout, and zero mobile document overflow after two long inline formulas were constrained to local scrollers. PDF `output/pdf/topologi-aljabar-unit-001-024-id.pdf` is 1,907,368 bytes/SHA-256 `5189b04f2f28d7e8192c16e8ef070e23bbf98085d150d1f2124d15c071ccf9b8`, 286 A4 pages, `/Lang=id-ID`, all 27 font rows embedded/subset/ToUnicode, with its untagged limitation disclosed. Two builds are byte-identical; every Unit 24 page plus title/transition passed visual inspection.
- Final append-only backend validation passes with 3,723 records/3,726,427 JSONL bytes and bundle SHA-256 `ffa8c7cb45b6d8170d7bc83df24ec487fd0c2777297b55eff2d5e7b3ae63fe25`. The final cumulative receipt is `qa/BACKEND_APPEND_ONLY_UNIT_024_CUMULATIVE_RECEIPT.json`, 6,692 bytes/SHA-256 `4f77c57c62eba9b031873898cb073be9c9c3772b472088c4fd8c5ee8cc20648e`; build receipt `qa/UNITS_001_024_BUILD_RECEIPT.json` is 7,560 bytes/SHA-256 `a050b3d282d43033ccdd7565bc6ee301eee6c30014ef6d8b84c5ec490406129a`.
- GitHub commit `8d3484aa2a3f8f611d90d1efa45bb454bcd03676`, tree `ac64588f4000ff40fa5cd334b258c96ad90cca17`, is public. Pages run `32682942914`, job `97302647322`, deployment `6055441517`, and status `17210867247` succeeded. The 52-file release delta was anonymously recovered from commit-pinned codeload archives under manifest SHA-256 `588a4d3bb36a90d6ba16d19eda955438f3b199c9d21cbdd64a5a37883fd5a906`; raw and deployed HTML both match 3,927,104 bytes/SHA-256 `28a84406de9e196070965920a7f7937177197977f9ddf118f0f8b07d464cbf0f`. Receipt `00_control/GITHUB_PUBLICATION_RECEIPT_UNITS_001_024.json` is 19,090 bytes/SHA-256 `e8fddd2edf8237de4c0b9a3ee543a3bc6f7ba79b8ddd43d06a2a06236e1ddbeb`.
- Zenodo version `0.24.0` is public at record `22074233`, DOI `10.5281/zenodo.22074233`, in concept `10.5281/zenodo.22061489`. The reader-first eight-file payload totals 6,573,935 bytes; every PDF, HTML, source/backend ZIP, QA/provenance ZIP, README, rights, manifest, and checksum file passed two anonymous HTTP 200 byte/hash readbacks. Public metadata is CC BY 4.0, `ind`, exact partial scope, no umbrella-title pollution, and preserves source authorship/non-endorsement. Sanitized receipt `release/zenodo-units-001-024/publication-receipt.json` is 3,762 bytes/SHA-256 `4bbf756556876c8299b03446c7afe6b08f2a03b80e424d3d5dddb98a7c59f2a8`.
- This boundary is superseded for local production by the verified Unit 25 boundary above, but remains the current Zenodo public version until a later substantial coherent update.

## Current verified and public GitHub Units 001–023 boundary (2026-08-24)

- Unit 23 covers Roberts `Notes.tex:4939–5112`; the 9,776-byte LF-normalized source span has SHA-256 `c7256a45621ad7a435277867298e4aeb8eb584dfce066cdae3b48c4ee0e0e3f4`. Reader `source/id-ID/units/unit-023-lecture-023.md` is 39,176 bytes/1,094 LF lines/51 stable IDs, SHA-256 `6f05ddbe6a720109797976c6929b0535f21a38353673cb42d9646a3196f56bd2`; it explicitly carries the source example across the Lecture 24 marker. Independent review is P1/P2/P3 zero and `qa/UNIT_023_QA.json` passes all 18 gates.
- Cumulative HTML `output/html/units-001-023/index.html` is 3,707,037 bytes/SHA-256 `536fbe19e295424d12198bf1b221be3e2f0170f87fa810a9125bcca9f742264b`: 1,225 unique IDs, 272 resolving fragments, 9,167 native MathML nodes, 57 semantic figures, no raw fallback or runtime dependency, centered desktop layout, and mobile-local scrolling only for wide mathematics. PDF `output/pdf/topologi-aljabar-unit-001-023-id.pdf` is 1,801,983 bytes/SHA-256 `e51aa739eefaa12f4b1d7a4fe99073c525775f113aa62e4506395a01fe1fcbaf`, 273 A4 pages, `/Lang=id-ID`, all 26 font rows embedded/subset/ToUnicode, with its untagged limitation disclosed. Two builds are byte-identical; every Unit 23 page plus the title and transition passed visual inspection.
- Final append-only backend validation passes with 3,528 records/3,434,879 JSONL bytes and bundle SHA-256 `0c8b27890f8423fc3224c89f2bcf60ed6cbcb9d93fabef7b53c399784f0aaaef`. It preserves the 3,513-record semantic prefix byte-for-byte and appends exactly 15 cumulative artifact/QA/relation/rights records. Superseding receipt `qa/BACKEND_APPEND_ONLY_UNIT_023_CUMULATIVE_RECEIPT.json` is 6,847 bytes/SHA-256 `c2224f527343cf6cff558918c3b7fa90a265f25da7587ac4f8f33b14af38fbdd`; build receipt `qa/UNITS_001_023_BUILD_RECEIPT.json` is 5,775 bytes/SHA-256 `a09fde0e147756c35fe4ba9ff5a212625bdbe96d19400409b14214e67afb4cf8`.
- GitHub content commit `1b47b73c6fa39c96b4c73d84e815b0cede3ba2b7` and release commit `d4cc478aa569d112c5fd69a0534f3e9c6870b51a`, tree `b142b7f0ef4b192bcb640083a21866d1309f2c85`, are public. Pages run `32680930628`, job `97297391262`, deployment `6055125762`, and status `17210066449` succeeded. The 36-file release delta was anonymously recovered from commit-pinned codeload archives; manifest SHA-256 is `1422f9122af56bfbd4424bb4383c5144741b16b2707f5e9d49a8228797ced656`. Raw and deployed Pages reader bytes both match 3,707,037 bytes/SHA-256 `536fbe19e295424d12198bf1b221be3e2f0170f87fa810a9125bcca9f742264b`. Receipt `00_control/GITHUB_PUBLICATION_RECEIPT_UNITS_001_023.json` is 13,848 bytes/SHA-256 `bdd596c98d71654da9ab7308eecde2a6187e8b49b112153d79dc8985a511c6b1`.
- Unit 24 spans `Notes.tex:5113–5369`, 12,837 LF bytes/SHA-256 `b2128930a56a0a8c04c327a397e72e21b215ffe742bb684e8dd166f0e04b0aea`. Its translated reader is 43,085 bytes/1,156 LF lines/60 stable IDs, SHA-256 `993ad0c3493caff6bd15ab2bcf435f6cbb1f49ed9a1e11bc1009d649ae2d3647`; independent review and fail-closed QA are in progress, so it is not yet in the admitted cursor or backend.
- Immediate actions: update the existing Zenodo lineage to the verified Unit 23 checkpoint with anonymous byte readback; finish Unit 24 backend/build admission; independently admit Unit 25 and continue without changing the selected Roberts/Fomberg architecture.

## Current verified Units 001–022 GitHub boundary (2026-08-23)

- Unit 22 covers Roberts `Notes.tex:4501–4938`; the 20,585-byte LF-normalized source span has SHA-256 `86275c590cfcdf8519d3ce8d077fc48619bb94c3fdf039ca805ae4b7df995b7f`. The next intact marker is Lecture 23 at line 4939.
- Reader source `source/id-ID/units/unit-022-lecture-022.md` is 44,066 bytes/1,349 LF lines/75 unique stable IDs, SHA-256 `0857e51568d77c811d5d79255ac75bfddc87a04b27356ae457d4e66eeffb7d0d`. It preserves the six definitions, eleven examples, five lemmas, three proofs, three remarks, and all source diagram functions; five positional source diagrams are semantic/reflowable. Six original mastery items each have a hint and full solution. Independent QA is P1/P2/P3 zero; `qa/UNIT_022_QA.json` is 4,167 bytes/SHA-256 `4b9e62ca0912eb3cd989130a643fc07b9634ffa421f989d92ec3d8676eea8fe7`.
- Self-contained HTML `output/html/units-001-022/index.html` is 3,520,527 bytes/SHA-256 `15938aac7515e4ad7de66f8cf2d825744f9eb08b654165b835bfeace31aef8f4`, with 1,167 unique IDs, 264 resolving fragments, 8,701 MathML nodes, 55 semantic figures, every Unit 22 ID, zero raw-TeX fallback, and no runtime dependency. PDF `output/pdf/topologi-aljabar-unit-001-022-id.pdf` is 1,728,316 bytes/SHA-256 `5dabcbdc98fdc7203ca2fe4f42aff86b9e3cb761136f676e0dd43b350768fb77`, 261 A4 pages, `/Lang=id-ID`, with 25/25 font rows embedded/subset/ToUnicode and an honest untagged limitation. Both formats were byte-identical across two builds. Root re-rendered and visually inspected pages 1, 247, 249, 253, 258, and 261; their hashes match the recorded render receipt and no clipping, overlap, missing glyph, diagram failure, or boundary defect appears.
- Manifest `output/ARTIFACT_MANIFEST_UNITS_001_022.csv` is 249 bytes/SHA-256 `3a79a520d0281504edd2449fdfd13c5a874ec675f8187a9e6cb516a760ef35c8`; builder is 18,956 bytes/SHA-256 `6d3ada82dbc5afbcec8b394c64694e392ceae55db165a8363d88b8c57b1464b7`; build receipt is 5,315 bytes/SHA-256 `347569120a698d2738472fb6d194fa6109f8b638b9e16b08c473fc9e793312b5`; visual receipt is 4,747 bytes/SHA-256 `35a5b00b6bdda6b77041ff568f14c91702818be3f939d9e3df36829ae168251b`.
- Final append-only backend validation passes with 3,337 records/3,176,534 JSONL bytes and bundle SHA-256 `38b98ca6258133036ded9e3cb72894f4181d4b6faa46af9e96a2128ab25c9df2`. The immutable 3,111-record Unit 21 prefix is preserved byte-for-byte; Unit 22 adds 211 semantic records, then 15 cumulative artifact/QA/rights records. Superseding receipt `qa/BACKEND_APPEND_ONLY_UNIT_022_CUMULATIVE_RECEIPT.json` is 6,539 bytes/SHA-256 `d0caab27696fb48ce4137f1f62b2258d4f7daa551b543daac2aabbfee48fad7d`.
- GitHub commit `e2b3c015c6b3dcc66b2e4741a740de6f1972d6f2`, tree `4ac0e8d9988663e6379cbb72e90bbb3d01ace12e`, is public. Workflow run `32665215550`, job `97257447080`, deployment `6052521271`, and status `17202625006` succeeded. All 36 changed files matched anonymous commit-pinned raw bytes and Git tree identities under manifest SHA-256 `17d046f349cf3218b784f9f17622d720b220d0564c6dc3743b4528c691306bc9`; the Pages reader matched 3,520,527 bytes/SHA-256 `15938aac7515e4ad7de66f8cf2d825744f9eb08b654165b835bfeace31aef8f4`. Receipt `00_control/GITHUB_PUBLICATION_RECEIPT_UNITS_001_022.json` is 17,334 bytes/SHA-256 `bf5ef437a51cae964e29d5ec05f0ff79c9c8abc9bd1ecc3815fff3343adff87c` and was reproduced identically by a second anonymous run.
- Zenodo version `0.22.0` is public at record `22072347`, DOI `10.5281/zenodo.22072347`, in concept `10.5281/zenodo.22061489`. The eight-file, reader-first payload totals 5,919,060 bytes; the PDF, HTML, source/backend ZIP, QA/provenance ZIP, README, rights, manifest, and checksum file were all anonymously downloaded and matched their local byte counts and SHA-256 hashes repeatedly. Sanitized LF-only receipt `release/zenodo-units-001-022/publication-receipt.json` is 3,762 bytes/SHA-256 `a73927c1f683cceefbec424a8bf08a51678b3a11ae81acf0b6582853c8bd1c8b`; transaction `release/zenodo-units-001-022/transaction.json` is 550 bytes/SHA-256 `90f136143bd9a71c649d8ae86d28c5003d31204ef8c0fcf66155cdf135f88486`.
- Lecture 23 has a read-only audit only. Its nominal span is `Notes.tex:4939–5112`, 9,776 LF bytes/SHA-256 `c7256a45621ad7a435277867298e4aeb8eb584dfce066cdae3b48c4ee0e0e3f4`; however, the example opened at line 5076 crosses the Lecture 24 marker at line 5113 and closes at line 5121. Production must preserve that continuation explicitly across edition units and must not call line 5112 an environment-safe close.
- Immediate action: translate Unit 23 contiguously from its audited line 4939 boundary, preserve the cross-marker example explicitly, and close its proof/mastery/accessibility defects before backend/build admission.

## Current verified and public Units 001–021 boundary (2026-08-23)

- Authority remains Roberts commit `b947ad2e9f9e301bfe24590a9db653bc54fa1a53`, tree `aa1d3edb85818e7176e2d0bbc06d9b4bd1e247f5`. Unit 21 covers `Notes.tex:4346–4500`; the 7,267-byte span has SHA-256 `281ba27f0f52f35fd9842954c223546e84ce1a0909ee84c14b2081c38c11f150`. The next intact marker is Lecture 22 at line 4501.
- Unit source `source/id-ID/units/unit-021-lecture-021.md` is 26,237 bytes/786 LF lines/47 unique stable IDs, SHA-256 `47fa3994dc59370fc464e9d150d62512a4602a3cffa5996f1027f93a427e0eec`. It preserves all source objects and supplies six separately identified mastery/hint/full-solution triples. `scripts/qa-unit-021.py` is hardened against later ledger-tail growth, 19,783 bytes/SHA-256 `6039f254104d713c31f95650b627135154e08541a7d596643118977447002837`; its receipt remains 3,967 bytes/SHA-256 `8f3f11a101ea09c0321989594a4a505ba44f92b8bde732d9c493d3de66a423ca` and PASS.
- Cumulative HTML `output/html/units-001-021/index.html` is 3,306,661 bytes/SHA-256 `aec7e94d3697a7feeae87134da983c59faaf29dc8d961bca28b6bfa9c53cdfa6`; it is offline/self-contained with 1,084 unique IDs, 256 resolving fragments, 8,208 MathML nodes, 50 semantic figures, and all 47 Unit 21 IDs. Cumulative PDF `output/pdf/topologi-aljabar-unit-001-021-id.pdf` is 1,645,350 bytes/SHA-256 `aee3f74109bafd1614d01d6593b8b2edbcbfdbf3b841b6beee878a01d7ddec16`, 246 A4 pages, `/Lang=id-ID`, with all 25 font rows embedded/subset/ToUnicode and an honest untagged limitation. Both formats were byte-identical across two builds; representative pages 1, 237, 238, 240, 243, and 246 passed visual inspection after the builder-level stray-`{}` defect was repaired.
- Manifest `output/ARTIFACT_MANIFEST_UNITS_001_021.csv` is 249 bytes/SHA-256 `40386b62066854272e8902c1f2c886a78de2c98f0dce845cbf6179c845bf1498`; build receipt `qa/UNITS_001_021_BUILD_RECEIPT.json` is 3,850 bytes/SHA-256 `e3afdb61c3787eac1b84601609a89eadb34e9eee5b9c5481ba18c5e441a51032`; visual receipt is 3,350 bytes/SHA-256 `f42bc668ab68a3f05993ac4d56a565160f4a94a417f656dd3f29f1e12475c6fa`.
- Append-only backend validation passes with 3,111 records/2,896,429 JSONL bytes and bundle SHA-256 `cf5acacf3ad2351869297dd8d3827787377422fa30c8c1385e60833b23913db9`. The immutable 3,096-record Unit 21 semantic prefix remains bundle `84920281207fc4088aa4f1f812d78333fd530e9f157eeebaa3b09cbfb53b431d`; the final 15 records bind the cumulative builder, readers, manifest, QA, visual evidence, rights, and relations. Superseding receipt: `qa/BACKEND_APPEND_ONLY_UNIT_021_CUMULATIVE_RECEIPT.json`, 6,803 bytes/SHA-256 `b6411739c9a13090f45c3db276af443e8a0f7ff61f9a6b2f0611c2ce77b09437`.
- GitHub content commit `dced81432b21edd7bffeae33a25e0c678de4d896`, tree `758121e256ae28da17f0968dbffc2fbafd2ecdc6`, is public. Pages run `32662474151`, job `97250635604`, deployment `6052011091`, and deployment status `17201415972` all succeeded. All 38 content-commit files matched anonymous raw GitHub bytes under manifest SHA-256 `f9c38dc87e9a69a1c6ea6b005c07eb3ac0328707921b863306bfbc558d4d984b`; the Pages reader matched 3,306,661 bytes/SHA-256 `aec7e94d3697a7feeae87134da983c59faaf29dc8d961bca28b6bfa9c53cdfa6`. Receipt: `00_control/GITHUB_PUBLICATION_RECEIPT_UNITS_001_021.json`, 9,450 bytes/SHA-256 `6d6fc560cd08df83c3f3cd108bfee5cbb4cde2a1d6d0af6479b11f9d59fc5102`. Zenodo remains at Unit 20 because a single-unit delta is not a substantial DOI boundary. Immediate action: admit the already frozen Unit 22 backend and cumulative readers.

## Historical pre-admission Unit 22 boundary (superseded by the verified boundary above)

- Unit 22 covers `Notes.tex:4501–4938`; source span 20,585 bytes/SHA-256 `86275c590cfcdf8519d3ce8d077fc48619bb94c3fdf039ca805ae4b7df995b7f`; next intact Lecture 23 marker line 4939.
- Reader `source/id-ID/units/unit-022-lecture-022.md` is 44,066 bytes/1,349 LF lines/75 unique IDs/SHA-256 `0857e51568d77c811d5d79255ac75bfddc87a04b27356ae457d4e66eeffb7d0d`. Independent QA passes 17/17 with P1/P2/P3 zero and six mastery/hint/full-solution triples. Evidence hashes: QA JSON `4b9e62ca0912eb3cd989130a643fc07b9634ffa421f989d92ec3d8676eea8fe7`; source audit `50e0c9268f19c1fc3d6a9f865b6c338940e0edb1c336386566030a7595695801`; independent review `6632c22c2aa9339c169382111c0c28750e91a61bbb7ed40d47fe4734cefc7004`; handoff `9804d4372f4dc80c963bd6dca86ab5f8e79c6959f334526adc4f02e92507ccbf`. The hardened QA script is SHA-256 `7f7d9be18b882843327ca25f3a42baa9f59b336a929e727ebc5f07cb1697f14f`.
- Unit 22 ledger rows are `O012-TERM-0293..0300` and `O012-ADV-0298..0311`; the rejected terminology variants do not occur. The former Unit 21 staging constraint is closed. Unit 22 has since passed backend/build admission as recorded at the top of this file; Unit 23 has only a read-only source audit and no translated file yet.

## Current verified Units 001–019 checkpoint (2026-08-23)

- Roberts authority: commit `b947ad2e9f9e301bfe24590a9db653bc54fa1a53`, tree `aa1d3edb85818e7176e2d0bbc06d9b4bd1e247f5`, `Notes.tex:134–3947`; next source line 3948 (`\\lecturenum{20}`).
- Unit 019: `source/id-ID/units/unit-019-lecture-019.md`, 57,277 bytes, 1,865 LF lines, 78 stable IDs, SHA-256 `ba34773d63e4dc70fccdf4fa19fbdc8a397062a4bc359978f3261a70ff64f98c`; independent review `qa/UNIT_019_INDEPENDENT_REVIEW.md`, 2,707 bytes/SHA-256 `d360a17a8a7a5008a80873c4413d92bd9354b6c44275365809be33258c0673a`; source audit `qa/UNIT_019_SOURCE_AUDIT.md`, 8,956 bytes/SHA-256 `9ff651aa4a98f17f9ae67ce154cc531147bf212b2be03e53c3aced3994066f36`; unit QA `qa/UNIT_019_QA.json`, 3,519 bytes/SHA-256 `a2ecc5dcc539c6434d2cb937ad7bb768c6ed434947b4cedcd313ce1bcfe8d1c3`.
- Cumulative HTML: `output/html/units-001-019/index.html`, 2,962,478 bytes, SHA-256 `ea5481b14dc1772408bd1c3e384b94a18eed9f2be3c9b9379fe4f8dd499253e0`; native MathML 7,451, display MathML 1,331, artifact IDs 951, resolving fragments 243, no runtime assets/scripts/stylesheets, offline/self-contained.
- Cumulative PDF: `output/pdf/topologi-aljabar-unit-001-019-id.pdf`, 1,506,471 bytes, 221 A4 pages, SHA-256 `291e4206b9e58ee8a49108e55b6b894b9cd3362c7701a50cb83a7d79714b7a86`; 24 embedded/subset/ToUnicode font rows; `/Lang=id-ID`; intentionally secondary and untagged.
- Cumulative QA: `qa/UNITS_001_019_QA.json`, 12,097 bytes/SHA-256 `38f8f3084f6031fe3670667e7e9a11f2b526a07eb69d32772194c3ff0ffeb02d`; visual receipt `qa/UNITS_001_019_VISUAL_QA.md`, 1,780 bytes/SHA-256 `29d69abe6399976a206ef28c96d01df5fdb3f9f2c8510db95fe73f2b35b0b064`; render inventory 26,213 bytes/SHA-256 `017f151a1bd06a4e2649b37ad551c973789d502897b358967bd216cd74c61783`. All 221 pages and browser 1280×720/390×844 surfaces passed; desktop body 928 px, mobile content 375.11 px, zero document overflow, 101/101 wide mobile displays locally scrollable, zero console warnings/errors.
- Backend: `scripts/validate-backend-units-001-019.py` passes; 2,726 records, 11 JSONL files, 2,480,537 bytes, bundle SHA-256 `fe590ceefd18081e9a2dad3510946e97a29375a0a82e2a8e26cd78b871d33b14`. The release artifact extension adds ten exact artifacts and five passed QA events; no raw render dump is asserted as a public release file. The sanitized backend receipt is `qa/BACKEND_UNITS_001_019_RECEIPT.json` (2,377 bytes, SHA-256 `b7733961574b0db40904687d0eb6ff04c51bb3dd813fce15694b7646fa6d2b59`).
- Next executable action: resume contiguous translation at `Notes.tex:3948` (Lecture 20), while retaining the Figshare authentication blocker for a later authorized retry. The reader publication commit is `3a9db22813fc93e9cbd7f65a418ba634a24af959`; the latest control/receipt commit is `1f029861a7e330dbb2f708b18e66e580a28fd6f3` (terminology QA refresh; receipt `00_control/GITHUB_TERMINOLOGY_QA_RECEIPT_2026-08-23.json`). Pages URL `https://kokunoyumeto.github.io/algebraic-topology-id/units-001-019/` and all new raw controls were anonymously read back byte-for-byte. Zenodo receipt `00_control/ZENODO_PUBLICATION_RECEIPT_UNITS_001_019.json` records the eight public files and exact hashes; GitHub receipt remains `00_control/GITHUB_PUBLICATION_RECEIPT_UNITS_001_019.json`.

## External publication checkpoint (2026-08-23)

- Zenodo existing concept lineage updated in place: record `22070794`, DOI `10.5281/zenodo.22070794`, concept DOI `10.5281/zenodo.22061489`. The public metadata is title `Topologi Aljabar: Edisi Bahasa Indonesia — Unit 1–19`, version `0.19.0`, `cc-by-4.0`, language `ind`, and explicitly states that Kuliah 20–30, the Fomberg bridge, and original closure remain pending. Eight files were anonymously downloaded and matched byte-for-byte; receipt `00_control/ZENODO_PUBLICATION_RECEIPT_UNITS_001_019.json` is 3,693 bytes, SHA-256 `ad9692d31934dd000a9ff44cbd0a34febaf4b23b440ccc216c8fb59fb5c783c9`.
- Local Zenodo release package is `release/zenodo-units-001-019/artifacts/`; reader PDF is 1,506,471 bytes/SHA-256 `291e4206b9e58ee8a49108e55b6b894b9cd3362c7701a50cb83a7d79714b7a86`, reader HTML is 2,962,478 bytes/SHA-256 `ea5481b14dc1772408bd1c3e384b94a18eed9f2be3c9b9379fe4f8dd499253e0`, source/backend ZIP is 507,727 bytes/SHA-256 `6c8a62d69375f66ff614938973a2a0d7a623b678ff18b4ce148c241fd9ea2082`, and QA/provenance ZIP is 282,239 bytes/SHA-256 `8f6df16c1429d7d061e1e428a6bdae241635d7b8c02943d98104c8bced01609c`.
- Figshare was not mutated: four bounded read-only/API checks returned authenticated `403 InactiveAccount`, public article `404`, and empty public project/collection article lists. No duplicate item was created; the prepared ≤5,000,000-byte reader-first payload and exact blocker are recorded in `00_control/FIGSHARE_PUBLICATION_RECEIPT_UNITS_001_019.json` (2,444 bytes, SHA-256 `3a3dee2f5bcabda5d2ab019db478fe39e2838561c632dadd9d330229db9056f`).

## Same-field terminology QA refresh (2026-08-23)

- Official arXiv searches for `topologi aljabar` and `Bahasa Indonesia topology` returned no results; no suitable Indonesian algebraic-topology TeX source was found in this bounded check.
- Direct PDF fallback: Risali–Wijayanti, DOI `10.22146/jmt.56529`, 13 pages/373,016 bytes, SHA-256 `e520234d557737b7c7c64e4f76871875e3d72681b3a2acd7c7254bf088278b7f`; local witness and decisions are recorded in `qa/INDONESIAN_TERMINOLOGY_QA_2026-08-23.{md,json}`.
- Same-field forms confirm `fungtor`, `morfisma`, `homomorfisma`, `isomorfisma`, `lembaran`, and `tertutup rata`; glossary controls `O012-TERM-0288` and `O012-TERM-0289` were added. Units 001–019 required no change; the three queued Unit 20 draft occurrences were normalized before admission and the final QA forbids the variants. Updated QA Markdown is 3,956 bytes/SHA-256 `00af36c1eea14c5fc56203c76825a198e06ca3b49038b13dec77fc71cdba18c6`; JSON is 3,802 bytes/SHA-256 `52cc8b4da52bccb9db9e7f492412d8235c53e62faaf286e5c65372e0eee54592`.

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

## Current verified Units 001–020 boundary (2026-08-23)

- Roberts authority remains `DavidMichaelRoberts/AlgebraicTopology2019` at commit `b947ad2e9f9e301bfe24590a9db653bc54fa1a53`; Unit 020 covers `Notes.tex:3948–4345`, with the next cursor at line 4346 (`\\begin{rem}` opening Lecture 21).
- Final Unit 020 source: `source/id-ID/units/unit-020-lecture-020.md`, 45,786 bytes, 1,425 LF lines, 73 stable IDs, SHA-256 `ed086dfe2f26951d4a1d1c398ade0224ffbf4bd1a20a985d267ecd97bbd228d3`. The two proof-delimiter and one Unicode-TeX portability repairs are recorded as adverse items O012-ADV-0288 and O012-ADV-0289; the bounded QA script passes every gate, including `math_delimiter_sanity`.
- Cumulative HTML: `output/html/units-001-020/index.html`, 3,190,086 bytes, SHA-256 `59cb765f2291fc835ca629c774505303745983baacf5379efc97c49da6205c03`; it is self-contained, native MathML, has 1,030 unique DOM IDs, 7,944 MathML nodes, 48 semantic figures, 245 TOC links, and all 73 Unit 020 IDs.
- Cumulative PDF: `output/pdf/topologi-aljabar-unit-001-020-id.pdf`, 1,598,235 bytes, SHA-256 `30fdde6ddfc937df3e93bb59d58e72e593c87262d6a2535214113e5ebab64457`, 237 A4 pages. Deterministic HTML and PDF builds were byte-identical on both runs under Pandoc 3.9.0.2 and `SOURCE_DATE_EPOCH=1787443200`. Representative visual QA covered pages 1, 119, 222, 224, 227, 230, and 237 with no clipping, overlap, or unreadable glyphs.
- Manifest: `output/ARTIFACT_MANIFEST_UNITS_001_020.csv`, 249 bytes, SHA-256 `d69c37838da4174ebb7dc4576392e813040d7f6ebbe1a13fe1c922e1271672da`. Machine receipts are `qa/UNITS_001_020_BUILD_RECEIPT.json` (2,812 bytes, SHA-256 `3c39b5546b2aced0a443c753e69824807c8e2f8c91903fe4eb3cca04741ecef1`), `qa/UNITS_001_020_VISUAL_QA.md` (1,392 bytes, SHA-256 `6a8b4d8e31c4adf38fcf51606542f59366f6c5f58d878df65e49677376bf58f9`), and `qa/BACKEND_APPEND_ONLY_UNIT_020_FINAL_RECEIPT.md` (2,113 bytes, SHA-256 `6f64eebb653fadb1dd34f0d802f1bda55d482ce9ac47df2c8a88715a100c26c9`). The final Unit 020 QA JSON is 3,717 bytes/SHA-256 `4638ac3e2a01c1f212c2b60133f78f1fdd4a1f9c21a9a4cb12e32ff10ba8653e`.
- Backend append-only validation passes with 2,959 records, 2,738,760 JSONL bytes, and bundle SHA-256 `7abd10e468c5f8b75853a67fcfb67d09f0470720fa88efcc84f5c3647cbb1fe5`; immutable Units 001–019 prefixes remain byte-identical and the cda9 Unit 020 records are explicitly superseded historical evidence. The validator is `scripts/validate-backend-append-only-unit-020.py` (7,090 bytes, SHA-256 `b91a73aaafcc3762b7015d6acd680f4f3a1bbe2c202ee8a0bae4393258bd0e79`).
- The bounded same-field terminology QA is passed and remains bound to `qa/INDONESIAN_TERMINOLOGY_QA_2026-08-23.json`, fallback DOI `10.22146/jmt.56529`, and model provenance `OpenAI Codex gpt-5.6-sol, Ultra`; its live cursor pointer now uses the final 7abd… backend bundle.
- GitHub content commit `1ee885eec3605bc832e8e6b031c0b4f5c6928fa5` published all 32 boundary files; every raw file matched anonymously under canonical manifest SHA-256 `826c1575fe5a3db6c46e77e91627d818e26a8378c26dc271d793cefa264cf37e`. Deployment-control commit `f4be63261447c1c09593321d2cf07174e82596e8` passed Pages run `32659798003`; `https://kokunoyumeto.github.io/algebraic-topology-id/units-001-020/` read back as 3,190,086 exact bytes/SHA-256 `59cb765f2291fc835ca629c774505303745983baacf5379efc97c49da6205c03`. The sanitized evidence is `00_control/GITHUB_PUBLICATION_RECEIPT_UNITS_001_020.json`.
- The same checkpoint is public as Zenodo version `0.20.0`, record `22071667`, DOI `10.5281/zenodo.22071667`, within the existing concept DOI `10.5281/zenodo.22061489`. Its eight reader-first files total 5,374,007 bytes and all passed anonymous byte/SHA-256 readback. The record page exposes `00_TOPOLOGI_ALJABAR_ID_UNITS_001_020_READER.pdf` as the primary visible preview, preserves Roberts as creator, labels the edition incomplete, retains CC BY 4.0, includes exact model provenance, and contains no TTP marker. See `00_control/ZENODO_PUBLICATION_RECEIPT_UNITS_001_020.json`.
- The next executable production action is contiguous Roberts translation at source line 4346; after Roberts Lecture 30, add the bounded Fomberg bridge and original closure exactly as frozen in `CURRICULUM_ROUTE_AND_FOMBERG_HANDOFF.md`.

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
