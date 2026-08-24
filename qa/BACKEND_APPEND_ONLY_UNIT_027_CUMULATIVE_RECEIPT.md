# Units 001--027 cumulative semantic-backend receipt

Date: 2026-08-24  
Status: **PASS**

The cumulative replay proves that the complete 4,105-record Unit 26 backend is
the unchanged byte prefix of the Unit 27 boundary and that the 159-record Unit
27 suffix matches its exact manifest and semantic receipt.

- Unit 26 prefix: 4,105 records; 4,305,218 bytes; bundle SHA-256
  `89556c5fa2224820837fc8956b1a48797929f28bef013baf9a613e73e6cf28eb`.
- Unit 27 suffix: 159 canonical records, sorted within the transaction.
- Current cumulative semantic backend: 4,264 records; 4,532,994 bytes;
  bundle SHA-256
  `09aa16e8d9387171445c4d465d00a5399e39517a210cb347e30d2d285c703f8c`.
- Semantic validator replay: **PASS**.
- Stable IDs / proof blocks / solved mastery triples / aliases: **46 / 3 / 6 / 4**.
- Terminal source cursor: Roberts `Notes.tex:5924`.

This is a source/semantic boundary. No Unit 27 HTML, PDF, build-QA, or
visual-QA record is asserted; the cumulative validator rejects those premature
claims. Existing Unit 25 build artifacts remain untouched.

No control file, reader, source audit, review, QA witness, HTML/PDF output,
Git or publication state, other unit, or upstream file changed in this backend
transaction.
