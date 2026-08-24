# Units 001-023 cumulative append-only backend receipt

Date: 2026-08-24  
Status: **PASS**  
Scope: exact cumulative Units 001–023 build artifacts, build/visual QA,
relations, and the final built-rights pointer only.

## Immutable semantic boundary

The cumulative producer and independent validator proved that the complete
Unit 23 semantic backend remained byte-for-byte unchanged as the transaction
prefix:

- records: **3,513**;
- bytes: **3,424,912**;
- ordered-file bundle SHA-256:
  `2b31536824cea66fc186bd653354eea4eea45f9c68da7992a45d037c782672dc`.

The transaction appended exactly 15 canonical records: 6 artifact records,
2 QA events, 6 relations, and 1 final rights record. No asset, authority,
concept, correction, segment, term, or unit record changed.

## Frozen cumulative artifacts

| Role | Path | Bytes | SHA-256 |
|---|---|---:|---|
| Builder | `scripts/build-units-001-023.ps1` | 19,688 | `2fd88a027775678ec359037923df604ecb2444e527ba8bda61731f68a6691f88` |
| HTML | `output/html/units-001-023/index.html` | 3,707,037 | `536fbe19e295424d12198bf1b221be3e2f0170f87fa810a9125bcca9f742264b` |
| PDF | `output/pdf/topologi-aljabar-unit-001-023-id.pdf` | 1,801,983 | `e51aa739eefaa12f4b1d7a4fe99073c525775f113aa62e4506395a01fe1fcbaf` |
| Manifest | `output/ARTIFACT_MANIFEST_UNITS_001_023.csv` | 249 | `f12629f0929eeec100c6fc769c239c64bcc1fb72283be4abee9daec691561f34` |
| Build receipt | `qa/UNITS_001_023_BUILD_RECEIPT.json` | 5,775 | `a09fde0e147756c35fe4ba9ff5a212625bdbe96d19400409b14214e67afb4cf8` |
| Visual receipt | `qa/UNITS_001_023_VISUAL_QA.md` | 4,278 | `784bc1b77b65e3e91c1de34a2e14d42a2202861a04e24f8eb3c130f480dbd35e` |

The deterministic PDF has 273 A4 pages. Both HTML and PDF passed two-build
byte identity; the independent rerun passed; HTML contains all 51 Unit 23 IDs,
9,167 native MathML nodes, no raw-TeX fallback, no unresolved fragment, and no
external runtime dependency. Every Unit 23 PDF page (261–273) plus title and
transition witnesses passed visual inspection. The PDF’s untagged limitation
is disclosed; the self-contained reflowable HTML is the primary accessible
surface. Process provenance is `OpenAI Codex gpt-5.6-sol, Ultra`.

## Final backend

- records: **3,528**;
- bytes: **3,434,879**;
- ordered-file bundle SHA-256:
  `0c8b27890f8423fc3224c89f2bcf60ed6cbcb9d93fabef7b53c399784f0aaaef`.

| File | Records | Bytes | SHA-256 |
|---|---:|---:|---|
| `artifacts.jsonl` | 125 | 98,770 | `f8f4fc8b686554ce528bffe4ca31533d8f416ad34d9ed16b8f23b5b6d981c13c` |
| `assets.jsonl` | 25 | 15,447 | `752dfa957041664a1b3f32acdcf996511164d5c17ba6aa34619a100651dad3b1` |
| `authority.jsonl` | 4 | 2,721 | `f21af26912520ab34b38dff0e927ed46a546dbe5d318da0dc133e58330d0e368` |
| `concepts.jsonl` | 312 | 98,079 | `6fadff806dab54588f4984dd44ec745152841dbf44416ea881d9414f6b535830` |
| `corrections.jsonl` | 313 | 306,801 | `a0545c84efadc062f181356f9fa508b0da5f9077f52702da0750e3165c0b6244` |
| `qa.jsonl` | 109 | 61,880 | `3c8c741c0c50b56cd0d15b7616c3ebd3006fe368382cc14e7c50ee743eebb974` |
| `relations.jsonl` | 337 | 136,702 | `07f7ec67c251eb180f211b09da33ec165129c45646d1b08014de2f3e68b2882c` |
| `rights.jsonl` | 63 | 57,648 | `f39bd50ab5e33d7d3b0ae9063b2ed0adc9fc3986a8a034de4311876c3e810157` |
| `segments.jsonl` | 956 | 1,193,838 | `1851199865ae823a7f155f1a33590290cafccb0f1cafe37d429fb7072a2d84c0` |
| `terms.jsonl` | 305 | 188,007 | `16ac428e76df5de2a97f475c9a80c7e63278bc57a15720047785e4ad217e82a9` |
| `units.jsonl` | 979 | 1,274,986 | `e66891050013b595dbe972bee0d7ba3b88689a8a6a06a2c2885919194df036c9` |

## Deterministic transaction

- Producer: `scripts/append-cumulative-unit-023-artifacts.py` — 16,901
  bytes, 320 lines, SHA-256
  `93425c4f4c676127b45c814e044a7750a79c063a66b872f16a6ecb8d41c4cc86`.
- Independent validator:
  `scripts/validate-backend-append-only-unit-023-cumulative.py` — 14,956
  bytes, 280 lines, SHA-256
  `612f3878a0b622045bca33116826ee1023773cc14be29b236d2f322910e98442`.
- Validator result: **PASS**. Exact prefix, canonical suffix, artifact bytes,
  manifest rows, build receipt, reproducibility gates, visual receipt, rights,
  QA witnesses, relation inventory, references, and final bundle all passed.

