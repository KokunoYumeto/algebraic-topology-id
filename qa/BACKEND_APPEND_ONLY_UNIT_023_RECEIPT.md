# Unit 023 append-only backend receipt

Date: 2026-08-24  
Status: **PASS**  
Scope: frozen Unit 23 semantic/source/rights/QA admission only; no cumulative
build, release, publication, source, control, cursor, or current-state change.

## Immutable boundary

The producer and independent validator proved that every byte of the public
Units 001–022 backend remained an immutable prefix:

- records: **3,337**;
- bytes: **3,176,534**;
- ordered-file bundle SHA-256:
  `38b98ca6258133036ded9e3cb72894f4181d4b6faa46af9e96a2128ab25c9df2`.

The transaction appended 176 canonical records: 3 artifacts, 1 source asset,
15 concepts, 11 corrections, 3 QA events, 22 relations, 3 rights records,
51 segments, 15 terms, and 52 units. `authority.jsonl` received no record.

## Frozen evidence and semantic closure

- Indonesian source: `source/id-ID/units/unit-023-lecture-023.md` — 39,176
  bytes, 1,094 LF lines, 51 stable IDs, SHA-256
  `6f05ddbe6a720109797976c6929b0535f21a38353673cb42d9646a3196f56bd2`.
- Authority: Roberts `Notes.tex:4939–5112` — 9,776 LF-normalized bytes,
  SHA-256
  `c7256a45621ad7a435277867298e4aeb8eb584dfce066cdae3b48c4ee0e0e3f4`.
- Terminology closure: `O012-TERM-0301..0315`.
- Adverse/correction closure: `O012-ADV-0312..0322`.
- Edition-unit identity: `unit:o012-rbt-u023`; non-destructive curriculum
  route identity: `D60-R13`. Every Unit 23 unit and segment carries both.
- Four edition-original proof closures are explicitly marked and linked to
  their claims. All six mastery problems have exactly one hint and one complete
  checked solution.
- The example opened at `Notes.tex:5076` is recorded as open at the Unit 23
  boundary, resumes in `unit:o012-rbt-u024` at line 5113, and closes at line
  5121. No Unit 24 source line is represented as Unit 23 content.
- QA receipt: `qa/UNIT_023_QA.json` — 6,412 bytes, SHA-256
  `f4a156b709158e9a6312d0fe604b7ab7c60a70d7f7c6fb1423014df4d49f820b`.
- Model/process provenance: `OpenAI Codex gpt-5.6-sol, Ultra`.

## Final backend

- records: **3,513**;
- bytes: **3,424,912**;
- ordered-file bundle SHA-256:
  `2b31536824cea66fc186bd653354eea4eea45f9c68da7992a45d037c782672dc`.

| File | Records | Bytes | SHA-256 |
|---|---:|---:|---|
| `artifacts.jsonl` | 119 | 93,962 | `a439fbb383c0082b68f9ebee1ec988b92f910e595992bbe23a97c1844ab0c9a9` |
| `assets.jsonl` | 25 | 15,447 | `752dfa957041664a1b3f32acdcf996511164d5c17ba6aa34619a100651dad3b1` |
| `authority.jsonl` | 4 | 2,721 | `f21af26912520ab34b38dff0e927ed46a546dbe5d318da0dc133e58330d0e368` |
| `concepts.jsonl` | 312 | 98,079 | `6fadff806dab54588f4984dd44ec745152841dbf44416ea881d9414f6b535830` |
| `corrections.jsonl` | 313 | 306,801 | `a0545c84efadc062f181356f9fa508b0da5f9077f52702da0750e3165c0b6244` |
| `qa.jsonl` | 107 | 60,615 | `6c6a5c890596eb883daf5b30ddb3ed1ffc287fa91aca6eaa45312225a75e0a13` |
| `relations.jsonl` | 331 | 134,073 | `d85e492b275093cb807fa2ca407bca56c0ec758c1f5e7df2f2f0babc4baf8a30` |
| `rights.jsonl` | 62 | 56,383 | `b3d975821a277ec640297ce75cb44e2c6dd18383eff876361b1952a51449b7ff` |
| `segments.jsonl` | 956 | 1,193,838 | `1851199865ae823a7f155f1a33590290cafccb0f1cafe37d429fb7072a2d84c0` |
| `terms.jsonl` | 305 | 188,007 | `16ac428e76df5de2a97f475c9a80c7e63278bc57a15720047785e4ad217e82a9` |
| `units.jsonl` | 979 | 1,274,986 | `e66891050013b595dbe972bee0d7ba3b88689a8a6a06a2c2885919194df036c9` |

## Deterministic transaction

- Producer: `scripts/extend-backend-unit-023.py` — 38,719 bytes, 703 lines,
  SHA-256
  `dc018c038511919f4f89a8d090e55c6e95847d9c651649ab007956c03fec51a2`.
- Independent validator:
  `scripts/validate-backend-append-only-unit-023.py` — 20,480 bytes, 374
  lines, SHA-256
  `980687034b34e4e5c07054f7abf29889651c6333f03bb25e01d8f45f7c956425`.
- Validator result: **PASS**; generic shape, references, artifact manifests,
  exact prefix, canonical suffix, stable-ID/locator bijection, hierarchy,
  route, continuation, rights, terminology, correction, proof, and mastery
  closure all passed.
- Cumulative build artifacts added: **0**.

