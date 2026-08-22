# O012 source decision

Decision date: 2026-08-21

## Admitted core

Admit David Michael Roberts, *Algebraic Topology*, at exact commit [`b947ad2e9f9e301bfe24590a9db653bc54fa1a53`](https://github.com/DavidMichaelRoberts/AlgebraicTopology2019/commit/b947ad2e9f9e301bfe24590a9db653bc54fa1a53) as the compact translated core.

Why it passes:

- the author, date, CC BY 4.0 license, and editable source are explicit;
- `Notes.tex` is the complete current authored body and has no project-level includes, bibliography, or external figure files;
- it contains 32 inline TikZ pictures and 69 Xy-pic matrices;
- two clean fixed-epoch two-pass builds are byte-identical at 119 pages;
- it provides strong fundamental-group/groupoid, covering-space, Seifert–van Kampen, classification, higher-homotopy, Delta-set/cohomology, exact-sequence, and Mayer–Vietoris material.

This is a lawful **core**, not complete D60 coverage. It lacks a conventional homology development, cellular computation, cup products, and a solved mastery corpus. Those gaps are filled only with independently authored, separately identified companion material.

## Component exclusions and redraws

- `Notes_1-8.tex` and `Notes_1-8.pdf` are obsolete subsets and are not translation inputs.
- `Möbius.pdf` is a rights-clear CC BY 4.0 handout but lacks editable source and is not referenced by `Notes.tex`; it is excluded from the active closure.
- `Notes.tex:4783–4812` credits a TeX StackExchange TikZ technique, and `Notes.tex:5411–5417` adapts an Xy-pic answer. Their mathematics may be retained, but their code must be independently redrawn and verified rather than copied into the edition.

## Rejected benchmarks

### MIT 18.905–18.906 notes

Reject `sanathdevalapurkar/algtop-notes` at `3f5d3189e2082716a69fccc1711d02ed848552d2` as a translation source. Its archive lacks the active 18.905 submodule closure; no `.gitmodules` survives; current PGF fails on the vendored spectral-sequence package; the root MIT notice names only Sanath although Haynes Miller rewrote Part I/preface and John/Xianglong Ni made images; six problem sets are PDF-only and unlicensed at component level. MIT OCW’s CC BY-NC-SA publication remains a coverage reference, not an editable donor.

### Fomberg/Lazarovich notes

Reject Yeheli Fomberg’s 2025 algebraic-topology notes as the spine or donor at this boundary. The published TeX requires an unavailable `header.tex`, its advertised source archive cannot be verified against the displayed commit, it assumes fundamental groups/coverings rather than teaching them, and it has two exercises with no solutions. Its homology/cohomology sequence remains a terminology and coverage benchmark only.

## Production consequence

Translate Roberts contiguously, create stable locale-neutral IDs, add solved mastery alongside each unit, and author the missing homology/cellular bridge without copying rejected-source expression.

## Edition decision versus curriculum admission

The Roberts edition and O012/D60 curriculum admission are separate decisions. Completion of translated units is not evidence that the source is the best curriculum design, and sunk work must not decide selection.

The bounded comparison nevertheless makes Roberts the strongest **single external design center**: its exact CC BY 4.0 authority, closed one-file TeX source, deterministic 119-page build, and coherent 30-lecture arc are stronger in combination than the serious alternatives. The admitted edition boundary is the complete 6,368-line `Notes.tex`, all eight sections from “What is it?” through “Classical applications”; `Notes_1-8.*` and `Möbius.pdf` remain excluded, and the two quarantined third-party-derived code spans require independent redraw.

Roberts alone is not a complete D60 course. Curricular admission is a qualified go only for **full Roberts plus a separately identified companion** containing conventional singular, simplicial, and cellular homology; CW boundary computations; cup products; any required UCT/Künneth connective material; and a graded 30–50-problem mastery layer with hints, answers, and full solutions. Roberts has 19 formal exercises and four questions without solutions. Bai Chapters 4–7 are a lawful coverage/terminology benchmark or separately provenanced bounded donor, not a second narrative spine; the Napkin is intentionally proof-light; MIT 18.905/906 remains inadmissible as a translation package for the rights and closure reasons above.

Roberts’s opening topology recap overlaps O003 but remains native prerequisite review with a diagnostic-bypass option; it must not expand into a competing point-set text. Its complexes language remains topology-specific and must not duplicate O014’s general homological-algebra role.
