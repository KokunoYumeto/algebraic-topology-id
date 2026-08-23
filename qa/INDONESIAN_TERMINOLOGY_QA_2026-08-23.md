# Indonesian same-field terminology QA — 2026-08-23

Status: **passed for source selection; one queued draft propagation**. This is
a bounded language check requested before scaling the next reader unit. It
does not change the Roberts source cursor or the selected O012 corpus.

## Primary search and fallback

The official arXiv search was checked for Indonesian/topology phrases. The
query `topologi aljabar` returned no results:

<https://arxiv.org/search/?query=topologi+aljabar&searchtype=all>

The bounded companion query `Bahasa Indonesia topology` also returned no
results:

<https://arxiv.org/search/?query=Bahasa+Indonesia+topology&searchtype=all>

The official arXiv API independently returned an Atom feed with
`totalResults=0` for the exact phrase query
<https://export.arxiv.org/api/query?search_query=all:%22topologi%20aljabar%22&start=0&max_results=20>.
Additional bounded API queries for `bahasa Indonesia` plus `topologi`,
`topologi kombinatorik`, and `aljabar topologi` also returned zero results.

No Indonesian-language algebraic-topology item with a downloadable TeX
source was therefore found on arXiv. This is a bounded no-hit, not a claim
that no such work exists.

The direct same-field fallback is the official journal PDF by Valentino
Risali and Indah Emilia Wijayanti, “Sifat-Sifat Morfisma di dalam Kategori
Ruang Penutup Ruang Topologis yang Terhubung Lintasan,” *Jurnal Matematika
Thales* 2(1) (2020), 23–35:

- article page: <https://journal.ugm.ac.id/jmt/article/view/56529>
- DOI: <https://doi.org/10.22146/jmt.56529>
- PDF: <https://journal.ugm.ac.id/jmt/article/download/56529/28321>
- local witness: `tmp/pdfs/terminology-qa/Risali_Wijayanti_2020_JMT_56529.pdf`
- 373,016 bytes, 13 pages, SHA-256
  `e520234d557737b7c7c64e4f76871875e3d72681b3a2acd7c7254bf088278b7f`

The PDF was downloaded from the journal and inspected with text extraction;
its main text is Bahasa Indonesia (the secondary abstract is English). The
article page identifies the work and authors and states the CC BY-SA 4.0
license. The editable TeX source is not exposed, so the PDF—not an inferred
source—is the terminology witness.

## Direct terminology comparison and decisions

The article uses `fungtor`, `morfisma`, `homomorfisma`, `isomorfisma`,
`ruang topologis`, `ruang penutup`, `grup fundamental`, `aksi kanan`,
`pemetaan penutup`, `pengangkatan`, `tertutup rata`, and `lembaran`. It also
uses `persekitaran` for neighbourhood and once uses the older spelling
`obyek`.

The existing reader choices already agree on the field-specific forms
`fungtor`, `morfisma`, `pemetaan penutup`, `tertutup rata`, `lembaran`,
`pengangkatan`, `aksi kanan`, and `terhubung lintasan lokal`. `lingkungan`
remains the reader-facing neighbourhood term, with `persekitaran` recorded as
a recognized variant; modern `objek` remains preferred over `obyek`.

Two missing control rows were added to `00_control/TERMINOLOGY.csv`:

1. `O012-TERM-0288`: *isomorphism* → `isomorfisma` (recognize
   `isomorfisme` only as a variant).
2. `O012-TERM-0289`: *homomorphism* → `homomorfisma`.

Completed Units 001–019 contain no `isomorfisme` spelling requiring a
retroactive rewrite. The current Lecture 20 draft contains three such
occurrences; they are queued for normalization to `isomorfisma` before the
unit is admitted, built, or added to the backend. No source formula or stable
identifier changes are implied.

## Provenance

This check was performed with **OpenAI Codex gpt-5.6-sol, Ultra**, at the
user’s direction. The note does not replace or diminish the Roberts source
authorship, the Risali–Wijayanti authorship, or any human contributor and
license notice. The comparison PDF is not redistributed by this QA note.
