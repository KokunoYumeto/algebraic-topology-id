# Unit 030 semantic-backend append receipt

Date: 2026-08-24  
Status: **PASS**

## Immutable prefix

- Boundary: verified cumulative Units 001--029 semantic backend.
- Records: 4,596.
- Bytes: 5,001,266.
- Bundle SHA-256: `49c599010ebee2223225f643cd09a53bea882b8064024d5189e6e15f648195d8`.
- All eleven JSONL prefixes were preserved byte-for-byte.

## Unit 030 append

- Added 165 canonical, transaction-sorted records.
- Final backend: 4,761 records; 5,213,679 bytes.
- Final bundle SHA-256: `51b8c7f611560b9b5e88e97b3a943b54e0eb687c703f0cd34c1a3d164e4fb920`.
- Reader: 23,008 bytes; SHA-256 `88da8cf71d0f81328bdd65b0dea7d54c48655ed8836e230eaed821796b61b08d`.
- Authority span: `Notes.tex:6271-6368`, 8,290 bytes; SHA-256 `c522b5ec0ba7d4c938be6588a070be648263d841e1db4f9905c9b388619b64b1`.
- Terminal source boundary: EOF after `Notes.tex:6368`; nominal next cursor `Notes.tex:6369`.
- Closure: 47 stable source IDs across seven headings and 40 fenced objects, four complete proofs, six exercise/hint/full-solution triples, one preserved source-label alias, two resolved pre-admission findings, one semantically reflowed source diagram, and ten correction records tied one-to-one to `O012-ADV-0398`--`O012-ADV-0407`.
- Terminology: ten admitted records tied one-to-one to `O012-TERM-0356`--`O012-TERM-0365`.
- Rights: source-derived and edition-original layers remain component-distinguishable under CC BY 4.0 with attribution and non-endorsement.

## Validation boundary

The independent semantic validator replayed the final backend, verified every
prefix/suffix identity, exact source and target locator, stable-ID topology,
source alias, assets, rights, terminology controls, adverse-ledger corrections,
relations, QA evidence, proofs, mastery closure, terminal EOF, and absence of
premature Unit 030 HTML/PDF claims. No reader, audit, review, QA witness, build
artifact, control, Git state, publication state, other unit, or upstream source
was changed by this transaction.

Model provenance: OpenAI Codex gpt-5.6-sol, Ultra.
