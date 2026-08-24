# Cumulative Units 001--028 semantic-backend receipt

Date: 2026-08-24  
Status: **PASS**

The cumulative semantic boundary replays the independently validated Unit 028
append over the byte-identical Units 001--027 prefix.

- Prefix: 4,264 records; 4,532,994 bytes; bundle SHA-256
  `09aa16e8d9387171445c4d465d00a5399e39517a210cb347e30d2d285c703f8c`.
- Unit 028 suffix: 161 canonical transaction-sorted records.
- Current backend: 4,425 records; 4,765,453 bytes; bundle SHA-256
  `3a7492ee9755c85e89139bd6af84121747caa85f1f6421c7ec2e133b010a0b9f`.
- Unit 028 closure: 47 stable IDs, four proofs, six solved mastery triples,
  one source alias, six resolved findings, and next cursor `Notes.tex:6053`.
- Cumulative rights pointer: `rights:o012-units-001-028-composite-cc-by-4.0`,
  superseding the corresponding Units 001--027 pointer without altering it.

Both semantic and cumulative validators replay successfully. No Unit 028
HTML, PDF, build-QA, visual-QA, Git, or publication claim is admitted by this
semantic-only boundary.

Model provenance: OpenAI Codex gpt-5.6-sol, Ultra.
