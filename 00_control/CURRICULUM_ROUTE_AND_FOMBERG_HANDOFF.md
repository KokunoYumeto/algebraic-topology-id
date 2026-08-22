# O012/D60 selected composite route and Fomberg handoff

Decision date: 2026-08-22  
Status: selected/configured; Roberts production remains first and contiguous.

## Non-destructive architecture

1. Finish David Michael Roberts's complete 30-lecture Indonesian edition in
   exact source order. Preserve every existing `edition_unit_id`; do not restart,
   discard, renumber, or compress the edition into the learner route.
2. Only after all 30 Roberts lectures are complete, translate Yeheli Fomberg's
   `algebraic_topology.tex:31–4185`, Sections 1.1–1.13 through cellular homology.
   Section 1.11 (degree) stays in the component source order as an optional
   cross-check; Roberts supplies the required degree route. Do not import the
   separate Fomberg problem bank.
3. Add a separately identified original CC BY-SA 4.0 closure: the proof repairs
   below, solved mastery, four reproducible computation laboratories, three
   cumulative assessments, and the proof-reconstruction/cross-invariant capstone.

The Roberts edition retains 30 `edition_unit_id` values. A separate, non-destructive
14-unit `course_route_unit_id` view groups those lectures and inserts the Fomberg
bridge. Completion of the edition and curriculum admission remain distinct facts.

## Frozen authorities

Roberts authority is governed by `AUTHORITY.json`: official repository
`DavidMichaelRoberts/AlgebraicTopology2019`, commit
`b947ad2e9f9e301bfe24590a9db653bc54fa1a53`, tree
`aa1d3edb85818e7176e2d0bbc06d9b4bd1e247f5`, `Notes.tex` 331,447 bytes,
6,368 lines, SHA-256
`cfe93e9dbe3e25bd96f711f59e6078ab97527682b58e1f8ad127f74357f665d7`,
CC BY 4.0.

Fomberg authority selected for the later bridge:

- official notes page: <https://yp.srht.site/notes/>;
- official repository: <https://git.sr.ht/~yp/math-notes>;
- commit `563194fae879178b9a6871b249513bfc27968975`, tree
  `fb678966d1533d529bdd72f49d8496a3bdc14a9b`;
- archive: 2,236,609 bytes, 63 tracked files, SHA-256
  `423c2c34b62a1b443e63be72e80a5c35d5cd6daf4e5b3be8e48dad1d1f897443`;
- `algebraic_topology.tex`: 223,886 bytes, 6,069 lines, SHA-256
  `d27095de0f38f0c14b2d7716cb52d51d064f0594dd9f82f9d1b3e6af5b35a483`;
- `header.tex`: 14,097 bytes, 444 lines, SHA-256
  `7c4c5cbe901c1b6c7ae8d6053d42cd28110ece34dd90bc60c5bcb7423e45e28e`;
- `LICENSE`: 20,140 bytes, SHA-256
  `0b7fc2608b6d990314e908569407a6058b4a29175167c6d91ca0070c946661be`;
- official PDF: 383,089 bytes, 57 A4 pages, SHA-256
  `148aba71473e3201993e562c5e5d0f05f1a0417f4bcbd4593bead5ab236e43cd`;
- selected source witness: lines 31–4185, physical PDF pages 1–39; Section
  1.14 starts on physical page 40; license CC BY-SA 4.0.

The earlier claim that the official archive lacks `header.tex` or `LICENSE` is
false. Both are frozen and blob-verified. Admission still requires a reproducible
two-build baseline: the current source expects an unfrozen TeX Live environment
and local building stopped at missing `commath.sty`, which must be lawfully vendored
or replaced. Selected-file diagrams are inline TikZ/TikZ-CD with no external figures.

MIT OCW 18.905 is a CC BY-NC-SA 4.0 proof-check comparator only. It is not the
selected bridge, because it lacks the needed simplicial development and its current
editable repository closure is less exact. No MIT expression enters this edition.

## Exact 14-unit learner route

| Route ID | Required material | Edition mapping |
|---|---|---|
| D60-R01 | Entry diagnostics and point-set review; bypass allowed | Roberts L1–L2, lines 136–584 |
| D60-R02 | Homotopy, deformation, categories, basic invariants | Roberts L3–L4, lines 585–1131 |
| D60-R03 | Coverings, pullbacks, lifting, initial monodromy | Roberts L5–L6, lines 1132–1515 |
| D60-R04 | Monodromy, fundamental groups/groupoids, computations | Roberts L7–L10, lines 1516–2272 |
| D60-R05 | Seifert–van Kampen, pushouts, presentations | Roberts L11–L13, lines 2273–3046 |
| D60-R06 | Classification of covering spaces | Roberts L14–L17, lines 3047–3481 |
| D60-R07 | Higher homotopy, fibre bundles, homotopy LES | Roberts L18–L19, lines 3482–3947 |
| D60-R08 | Delta/simplicial complexes and simplicial homology | Fomberg §§1.1–1.2, lines 31–614 |
| D60-R09 | Singular homology, functoriality, homotopy invariance | Fomberg §§1.3–1.4, lines 615–1290 |
| D60-R10 | Exact and relative homology | Fomberg §§1.5–1.6, lines 1291–1922 |
| D60-R11 | Excision, Mayer–Vietoris, comparison | Fomberg §§1.7–1.10, lines 1923–2846 |
| D60-R12 | CW and cellular homology; optional degree cross-check | Fomberg §§1.12–1.13, lines 3123–4185; optional §1.11, lines 2847–3122 |
| D60-R13 | Complexes, combinatorial cohomology, exact/relative/reduced theory | Roberts L20–L27, lines 3948–5923 |
| D60-R14 | Comparison, axioms, degree, classical applications, capstone | Roberts L28–L30, lines 5924–6368 plus original synthesis |

The route is a view. Each component edition stays in its own source order.

## Mandatory Fomberg proof repairs

Every selected result receives `proof_status`, exact locator, and `repair_id`.
At minimum supply original complete proofs/solutions for:

- `FOM-PR-01`, 1001–1003: induced singular-chain map commutes with boundary;
- `FOM-PR-02`, 1034: induced homology map is a homomorphism;
- `FOM-PR-03`, 1121–1128: homotopy equivalence induces homology isomorphism;
- `FOM-PR-04`, 1869–1872: exactness of the long homology sequence;
- `FOM-PR-05`, 2068–2071: geometric subdivision and arbitrarily small chains
  (two omissions);
- `FOM-PR-06`, 2160–2161: excision;
- `FOM-PR-07`, 2807–2810: five lemma;
- `FOM-PR-08`, 2838–2844: injectivity in simplicial/singular comparison.

The census may add repairs but may not waive these nine incomplete loci.

## Mastery and computation closure

The final route must contain at least six ordinary problems per route unit with
hints and complete checked solutions (84), plus three cumulative assessments of
eight items each (24): **108 ordinary solution-bearing items**. Reusable source
prompts count only after exact mapping and full solution closure. Add four offline,
reproducible labs with source, tests, expected output, interpretation, and solution:
covering monodromy/group presentations; chain matrices/Smith normal form; cellular
boundary maps/degree; and comparison of fundamental-group, homology, and
cohomology invariants. Finish with one proof-reconstruction/cross-invariant
capstone and an explicit oral-proof rubric.

## Backend, rights, and publication

Every segment records component identity, commit and line locator,
`edition_unit_id`, `course_route_unit_id`, stable semantic ID, locale,
translation/proof/solution status, dependencies, component rights, QA, and hashes.
Roberts (CC BY 4.0), Fomberg (CC BY-SA 4.0), and original layers remain distinct.
The integrated route is CC BY-SA 4.0 with complete component attribution, change,
non-endorsement, and license notices. Current Roberts-only checkpoints keep their
exact CC BY 4.0 component licensing.

Publish substantial verified checkpoints under standing authorization. GitHub
suspension must not trigger repeated pushes or a duplicate repository; Zenodo is
the maintained preservation route while access is unavailable. No upstream contact
during production. After complete-corpus closure only, at most one concise,
deduplicated, high-confidence report may be sent, signed
“Codex, acting on Floris's request.”

