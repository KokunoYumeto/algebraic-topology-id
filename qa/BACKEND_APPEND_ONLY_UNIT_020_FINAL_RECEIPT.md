# O012 Unit 020 backend final append-only receipt

Date: 2026-08-23  
Validator: scripts/validate-backend-append-only-unit-020.py  
Validator SHA-256: b91a73aaafcc3762b7015d6acd680f4f3a1bbe2c202ee8a0bae4393258bd0e79

The immutable 001–019 prefixes remain byte-identical. The cda9 Unit 020
records are retained as superseded historical evidence; final source and
cumulative build witnesses bind the ed086 source boundary. No global lexical
reorder or historical JSONL rewrite was performed. Generic shape, reference,
artifact-manifest, source-binding, and append-batch checks all pass.

## Final counts and bundle

- 2,959 records; 2,738,760 JSONL bytes.
- Bundle SHA-256 (lexical filename order, filename + NUL + bytes):
  7abd10e468c5f8b75853a67fcfb67d09f0470720fa88efcc84f5c3647cbb1fe5.
- Unit 020 final source: 45,786 bytes, 1,425 LF lines,
  ed086dfe2f26951d4a1d1c398ade0224ffbf4bd1a20a985d267ecd97bbd228d3.
- Cumulative PDF: 1,598,235 bytes, 237 A4 pages,
  30fdde6ddfc937df3e93bb59d58e72e593c87262d6a2535214113e5ebab64457.
- Cumulative HTML: 3,190,086 bytes,
  59cb765f2291fc835ca629c774505303745983baacf5379efc97c49da6205c03.
- Final Unit 020 QA JSON (after ADV-0288/0289): 3,717 bytes,
  4638ac3e2a01c1f212c2b60133f78f1fdd4a1f9c21a9a4cb12e32ff10ba8653e.
- Cumulative manifest: 249 bytes,
  d69c37838da4174ebb7dc4576392e813040d7f6ebbe1a13fe1c922e1271672da.
- Build receipt: 2,812 bytes,
  3c39b5546b2aced0a443c753e69824807c8e2f8c91903fe4eb3cca04741ecef1.
- Visual receipt: 1,392 bytes,
  6a8b4d8e31c4adf38fcf51606542f59366f6c5f58d878df65e49677376bf58f9.

| File | Records |
|---|---:|
| artifacts.jsonl | 96 |
| assets.jsonl | 22 |
| authority.jsonl | 4 |
| concepts.jsonl | 286 |
| corrections.jsonl | 280 |
| qa.jsonl | 94 |
| relations.jsonl | 261 |
| rights.jsonl | 51 |
| segments.jsonl | 783 |
| terms.jsonl | 279 |
| units.jsonl | 803 |

The ledger tails O012-ADV-0288 and O012-ADV-0289 are closed by canonical
correction records with supersession links and upstream disposition
not_contacted. The superseding 4638ac QA artifact/event preserves the earlier
05bc QA witness as historical evidence.
