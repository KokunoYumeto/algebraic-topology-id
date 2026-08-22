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

## Deferred selected bridge and rejected benchmark

### MIT 18.905–18.906 notes

Reject `sanathdevalapurkar/algtop-notes` at `3f5d3189e2082716a69fccc1711d02ed848552d2` as a translation source. Its archive lacks the active 18.905 submodule closure; no `.gitmodules` survives; current PGF fails on the vendored spectral-sequence package; the root MIT notice names only Sanath although Haynes Miller rewrote Part I/preface and John/Xianglong Ni made images; six problem sets are PDF-only and unlicensed at component level. MIT OCW’s CC BY-NC-SA publication remains a coverage reference, not an editable donor.

### Fomberg notes — selected after Roberts

The former rejection is superseded. The official archive at commit `563194fae879178b9a6871b249513bfc27968975` does contain blob-verified `header.tex` and `LICENSE`; it is CC BY-SA 4.0. After the complete 30-lecture Roberts edition, translate only `algebraic_topology.tex:31–4185` (Sections 1.1–1.13 through cellular homology) as the selected homology bridge. The separate problem bank is excluded. A reproducible baseline remains an admission gate because the current local build stops at the unfrozen `commath.sty` dependency. Exact identities, the 14-unit non-destructive route, proof repairs, and mastery closure are frozen in `CURRICULUM_ROUTE_AND_FOMBERG_HANDOFF.md`.

## Production consequence

Translate Roberts contiguously, create stable locale-neutral IDs, and add solved mastery alongside each unit. After all 30 lectures, translate the bounded Fomberg bridge in its own source order, then add the separately identified original proof/mastery/lab/capstone closure. Preserve 30 Roberts `edition_unit_id` values and map them non-destructively to the 14-unit `course_route_unit_id` view.

## Edition decision versus curriculum admission

The Roberts edition and O012/D60 curriculum admission are separate decisions. Completion of translated units is not evidence that the source is the best curriculum design, and sunk work must not decide selection.

The bounded comparison nevertheless makes Roberts the strongest **single external design center**: its exact CC BY 4.0 authority, closed one-file TeX source, deterministic 119-page build, and coherent 30-lecture arc are stronger in combination than the serious alternatives. The admitted edition boundary is the complete 6,368-line `Notes.tex`, all eight sections from “What is it?” through “Classical applications”; `Notes_1-8.*` and `Möbius.pdf` remain excluded, and the two quarantined third-party-derived code spans require independent redraw.

Roberts alone is not the complete selected D60 course. Curricular admission is **full Roberts plus Fomberg lines 31–4185 plus the exact original closure** recorded in `CURRICULUM_ROUTE_AND_FOMBERG_HANDOFF.md`. Roberts has 19 formal exercises and four questions; the route closes 108 ordinary solution-bearing items, four reproducible labs, the named Fomberg proof omissions, and one cumulative capstone. MIT 18.905 remains proof-check reference only and contributes no copied expression.

Roberts’s opening topology recap overlaps O003 but remains native prerequisite review with a diagnostic-bypass option; it must not expand into a competing point-set text. Its complexes language remains topology-specific and must not duplicate O014’s general homological-algebra role.
