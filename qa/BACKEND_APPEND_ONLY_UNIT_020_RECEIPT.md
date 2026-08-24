# O012 Unit 020 backend append-only control receipt

Date: 2026-08-23  
Validator: scripts/validate-backend-append-only-unit-020.py  
Validator SHA-256: b91a73aaafcc3762b7015d6acd680f4f3a1bbe2c202ee8a0bae4393258bd0e79

## Policy

The first 001–019 JSONL prefix is immutable evidence. New records are
append-only and are canonical JSONL, sorted within each producer transaction.
Separate transactions may begin with a lexically earlier identifier; the
validator treats each monotone suffix run as a batch. No Git index, global
lexical reorder, or historical record rewrite is allowed. The cda9 Unit 020
snapshot remains retained as superseded evidence; the ed086 source witness is
release-authoritative.

## Verified boundary

The validator passed generic shape, reference, and artifact-manifest checks,
the exact baseline-prefix byte hashes, final Unit 020 source binding, and
append-batch ordering.

At this checkpoint (before the cumulative Units 001–020 build records):

- 2,941 backend records; 2,727,509 JSONL bytes.
- Bundle SHA-256 (filename + NUL + bytes, lexical filename order):
  c600eaa7a0ac6c45b1b3fcbbfa60367f85ba9544dc7b149e48006177b38f8723.
- Final Unit 020 source: 45,786 bytes, 1,425 LF lines,
  ed086dfe2f26951d4a1d1c398ade0224ffbf4bd1a20a985d267ecd97bbd228d3.
- Final QA JSON: 3,717 bytes,
  05bc5a51420d15e044ae1c113616e9c371728593b6666886dba1cbf39beac24f.

| JSONL file | Immutable prefix lines | Prefix SHA-256 |
|---|---:|---|
| artifacts.jsonl | 82 | c0b0624b523e285b1a4c88143b44a06e28a80a9d38dd49ad4026ab80687517f0 |
| assets.jsonl | 20 | 756e93660931a20be8a8ea2048126e6f963184f3ac6fbb18c615fd58dbe385ae |
| authority.jsonl | 4 | f21af26912520ab34b38dff0e927ed46a546dbe5d318da0dc133e58330d0e368 |
| concepts.jsonl | 284 | b3afa6260276c68fe0d0bd8cbccaf55196caa05fa41acc4f1c58ea62001c1295 |
| corrections.jsonl | 268 | 769d7f611b07396465791d0d9a2319a18ce76da111ffbe10717f11b2c22f9512 |
| qa.jsonl | 86 | e7c13ac6bb006b4adb20dca233fb528a0b140226799d32606f7539f4c6c9826f |
| relations.jsonl | 219 | d8756f6d556d40986c3c8212a2e8f378950f2de1cb184463df5eb183e82bfbb5 |
| rights.jsonl | 47 | db374a45045aa674e68d9d104c736d55d874adbd9fa87bd0a7d5189e07e6f21c |
| segments.jsonl | 710 | ad3f8b3c45a2235e72af5fcfaa78cc639d601a0f6256df65e8d66cf83774025a |
| terms.jsonl | 277 | 6111794432f311984a3b4f2fbe4250d78873968f696ff66da867868fbc73b2ec |
| units.jsonl | 729 | e88c8dfca31e77a115e6251db21f4e485d569beec8d9f1909dafa9ad0a485cf3 |
