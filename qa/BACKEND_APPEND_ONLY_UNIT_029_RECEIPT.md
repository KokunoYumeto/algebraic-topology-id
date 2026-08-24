# Unit 029 semantic-backend append receipt

Date: 2026-08-24  
Status: **PASS**

## Immutable prefix

- Boundary: verified cumulative Units 001--028 semantic backend.
- Records: 4,425.
- Bytes: 4,765,453.
- Bundle SHA-256: `3a7492ee9755c85e89139bd6af84121747caa85f1f6421c7ec2e133b010a0b9f`.
- All eleven JSONL prefixes were preserved byte-for-byte.

## Unit 029 append

- Added 171 canonical, transaction-sorted records.
- Final backend: 4,596 records; 5,001,266 bytes.
- Final bundle SHA-256: `49c599010ebee2223225f643cd09a53bea882b8064024d5189e6e15f648195d8`.
- Reader: 27,687 bytes; SHA-256 `cfb8fa5c49593a187bed5df1d4173cc952100b18e5faa009cb8d57036c5726c4`.
- Authority span: `Notes.tex:6053-6270`, 11,447 bytes; SHA-256 `33c6b7bfe3216d271c6b1f9d0cb952e6ef02a5e27a57f686936e764bfc4a9233`.
- Next source cursor: `Notes.tex:6271`.
- Closure: 49 stable IDs including the root lecture ID, four complete proofs, six exercise/hint/full-solution triples, one preserved source-label alias, eight resolved pre-admission findings, five semantically reflowed source diagrams, and 19 correction records.
- Rights: source-derived and edition-original layers remain component-distinguishable under CC BY 4.0 with attribution and non-endorsement.

## Validation boundary

The independent semantic validator replayed the final backend, verified every
prefix/suffix identity, exact source and target locator, stable-ID topology,
source alias, assets, rights, terminology, relations, corrections, QA evidence,
proofs, mastery closure, and absence of premature Unit 029 HTML/PDF claims.
No reader, audit, review, QA witness, build artifact, control, Git state,
publication state, other unit, or upstream source was changed by this transaction.

Model provenance: OpenAI Codex gpt-5.6-sol, Ultra.
