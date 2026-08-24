# Unit 025 semantic-validator replay compatibility receipt

Date: 2026-08-24  
Status: **PASS**

## Reason for this additive receipt

The original semantic transaction validator was intentionally fail-closed at
the 3,896-record semantic boundary. After the separately validated cumulative
build transaction appended 17 records, replaying that historical validator on
the live backend rejected the larger `artifacts.jsonl` identity even though
the semantic slice itself remained exact.

The validator is now final-state compatible without weakening any boundary:

1. it verifies the complete immutable Units 001--024 cumulative prefix:
   3,723 records, 3,726,427 bytes, bundle SHA-256
   `ffa8c7cb45b6d8170d7bc83df24ec487fd0c2777297b55eff2d5e7b3ae63fe25`;
2. it slices and verifies the exact 173-record Unit 25 semantic transaction,
   giving 3,896 records, 3,996,359 bytes, bundle SHA-256
   `55372b9c2853fa479e731c73c407b234ad2f1219e07efbedbad2a99f1e2abf47`;
3. it accepts no arbitrary trailing data: the only permitted suffix is the
   exact canonical 17-record cumulative tail—seven artifacts, two QA events,
   seven relations, and one rights record—bound by cumulative receipt SHA-256
   `eacee8cad8ffe460af5f50a9be16f5c02b0671a686209e7d0073e10b2a98a2c1`;
4. it independently verifies the resulting live backend at 3,913 records,
   4,007,903 bytes, bundle SHA-256
   `8b50629f25c5fcbedb6d5547f8f7151c622aa90e04f71583008bd176058a4f78`;
5. all prior source, stable-ID, topology, route, terminology, correction,
   proof, mastery, evidence, rights, and cursor checks still run unchanged.

The updated validator is
`scripts/validate-backend-append-only-unit-025.py`, 25,281 bytes, 442 LF
lines, SHA-256
`49b21e6a66ddd3606b324f50e3bf11d44b8d762736178cbe859b2bee41188bab`.

Both replay commands pass on the live tree:

- semantic validator: **PASS**;
- cumulative validator: **PASS**.

The original semantic receipts remain byte-identical historical transaction
evidence because the cumulative validator cryptographically pins their exact
bytes. They were not rewritten:

- `qa/BACKEND_APPEND_ONLY_UNIT_025_RECEIPT.json`: 6,957 bytes, SHA-256
  `7814c3586ab5e25989ddbed45ab8569d8406fb9022c5fa52e74e5b8b1aef37aa`;
- `qa/BACKEND_APPEND_ONLY_UNIT_025_RECEIPT.md`: 2,961 bytes, SHA-256
  `43f11a856d9c169884853b8e64fc9adc2c461694d8b795d2a47789d1a0d32af9`.

No backend record, control, source, reader, output, Git state, publication
state, or later unit was changed by this compatibility repair.

Model/process provenance: OpenAI Codex gpt-5.6-sol, Ultra.
