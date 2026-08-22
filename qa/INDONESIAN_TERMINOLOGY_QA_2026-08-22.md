# Indonesian same-field terminology QA — 2026-08-22

Status: **passed**. This is a bounded language QA at the safe boundary after
Roberts Lecture 17 and before Lecture 18. It does not reopen source selection,
change the mathematical cursor, or modify any frozen reader/release byte.

## Search result and fallback authority

Exact arXiv searches for `all:"topologi aljabar"`, `all:"grup fundamental"`,
`all:"ruang penutup"`, and `all:"ruang topologis"`, followed by arXiv-restricted
full-text searches, found no suitable Indonesian algebraic-topology item with
downloadable TeX. This is a bounded no-hit, not proof that no such item exists.

The fallback is unusually close to this edition's current subject matter:

- Valentino Risali and Indah Emilia Wijayanti, “Sifat-Sifat Morfisma di dalam
  Kategori Ruang Penutup Ruang Topologis yang Terhubung Lintasan,” *Jurnal
  Matematika Thales* 2(1), 2020, pp. 23–35.
- DOI: <https://doi.org/10.22146/jmt.56529>.
- Official article page:
  <https://journal.ugm.ac.id/jmt/article/view/56529>.
- Official PDF:
  <https://journal.ugm.ac.id/jmt/article/download/56529/28321>.
- PDF witness: 373,016 bytes, 13 A4 pages, SHA-256
  `e520234d557737b7c7c64e4f76871875e3d72681b3a2acd7c7254bf088278b7f`.
- The main text is Bahasa Indonesia; only the secondary abstract is English.
  PDF metadata identifies a LaTeX/pdfTeX build, but the journal exposes no
  editable source. The PDF was therefore inspected as the truthful fallback.

Direct page inspection found the comparison terms in the article itself, not
merely in search snippets: `ruang topologis`, `ruang penutup`, `grup
fundamental`, `aksi kanan`, `fungtor`, and `morfisma` on pp. 23–24; `homotopi`,
`titik basis`, `terhubung lintasan lokal`, `persekitaran`, `tertutup rata`, and
the bilingual `lembaran (sheet)` definition on p. 25; `pemetaan penutup` and
further uses of `tertutup rata` on p. 26; and `pengangkatan` on p. 27.

## Decisions

| Concept | Prior live form | Same-field evidence | Decision |
|---|---|---|---|
| functor / functoriality | `funktor`, `funktorialitas` | `fungtor` throughout the article | Prefer `fungtor`, `fungtorialitas`; keep prior spellings as backend variants. |
| morphism family | `morfisme`, including derived forms | `morfisma`, `homomorfisma`, `homeomorfisma` | Prefer the `-morfisma` family; keep prior spellings as backend variants. |
| covering sheet | `lembar` | explicit `lembaran (sheet)` | Prefer `lembaran`. |
| evenly covered | `tertutup secara merata` | `tertutup rata` five times | Prefer `tertutup rata`; retain `diliputi secara merata` as explanatory prose where grammatical. |
| neighbourhood | `lingkungan` | `persekitaran` | Retain reader-facing `lingkungan`; record `persekitaran` as a recognized variant. |
| object | `objek` | older `obyek` | Retain modern spelling `objek`. |
| fully faithful | `penuh dan setia` | English left untranslated | Retain the clearer Indonesian translation. |

The fallback contains no usable evidence for `retrak deformasi`, `monodromi`,
`grupoid fundamental`, Seifert–van Kampen, `pushout`, `tarik balik`, quotient,
fibre bundles, or exact sequences. Those choices were not changed by this QA.

## Propagation and invariants

The controlled migration changed only the 17 live Indonesian Markdown sources,
`TERMINOLOGY.csv`, and the canonical Units 001–013 backend. Across the live
sources it made 193 `fungtor`-family, 327 `morfisma`-family, 61 `lembaran`, and
six `tertutup rata` substitutions. All 17 line counts and every stable-ID
inventory are unchanged. Upstream authority files, formulas, source locators,
published HTML/PDF files, release packages, transactions, and publication
receipts were not edited. Historical release hashes therefore remain truthful;
the next cumulative reader will carry the refined spelling.

The canonical backend remains 1,762 records in 11 JSONL files and passes the
offline validator with bundle SHA-256
`c5ac458a7f4723460ccebccaf3e5738544883c685a54c9a3cfbef854f2db83c5`.
The machine receipt `INDONESIAN_TERMINOLOGY_QA_2026-08-22.json` records every
source's before/after bytes and SHA-256, replacement counts, the fallback
identity, the decisions, and backend changes. Unit 015 was also normalized
from its pre-existing mixed CRLF/LF working copy to the repository's required
LF form; its 835 logical lines and all stable IDs are unchanged, and the receipt
separately records the pre-migration working hash and prior Git-blob hash.

## Process provenance

This terminology comparison, migration, and validation were performed with
**OpenAI Codex gpt-5.6-sol, Ultra**, acting at the user's direction. That process
credit does not replace or diminish David Michael Roberts's source authorship,
Risali and Wijayanti's authorship of the comparison paper, the user's direction,
or any component license and attribution.
