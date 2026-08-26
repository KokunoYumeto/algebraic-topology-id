[CmdletBinding()]
param()

# Deterministic, reader-first composite build for the Roberts 30/30 edition
# followed by Fomberg Sections 1.1-1.13.  This script deliberately writes only
# the new 001-007 HTML/PDF/manifest outputs; visual/publication receipts are
# sealed by their bounded follow-up tools.
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$lane = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$lf = [string][char]10
$utf8 = [Text.UTF8Encoding]::new($false)

$robertsAuthority = Join-Path $lane 'authority\upstream\AlgebraicTopology2019-b947ad2e9f9e301bfe24590a9db653bc54fa1a53\Notes.tex'
$fombergAuthority = Join-Path $lane 'authority\upstream\math-notes-563194fae879178b9a6871b249513bfc27968975\tree\algebraic_topology.tex'
$fombergLicense = Join-Path $lane 'authority\upstream\math-notes-563194fae879178b9a6871b249513bfc27968975\tree\LICENSE'
$robertsReaders = @(
    (Join-Path $lane 'source\id-ID\reader-unit-001.md')
    2..30 | ForEach-Object {
        Join-Path $lane ("source\id-ID\units\unit-{0:000}-lecture-{0:000}.md" -f $_)
    }
)
$fombergReaders = @(
    (Join-Path $lane 'source\id-ID\fomberg\units\fomberg-unit-001-delta-complexes-simplicial-homology.md')
    (Join-Path $lane 'source\id-ID\fomberg\units\fomberg-unit-002-singular-homology-homotopy-invariance.md')
    (Join-Path $lane 'source\id-ID\fomberg\units\fomberg-unit-003-exact-sequences-relative-homology.md')
    (Join-Path $lane 'source\id-ID\fomberg\units\fomberg-unit-004-excision-mayer-vietoris-naturality-comparison.md')
    (Join-Path $lane 'source\id-ID\fomberg\units\fomberg-unit-005-degree-maps-local-degree.md')
    (Join-Path $lane 'source\id-ID\fomberg\units\fomberg-unit-006-cellular-complexes.md')
    (Join-Path $lane 'source\id-ID\fomberg\units\fomberg-unit-007-cellular-homology.md')
)
$unit007QaPath = Join-Path $lane 'qa\FOMBERG_UNIT_007_QA.json'
$unit007SourceAuditPath = Join-Path $lane 'qa\FOMBERG_UNIT_007_SOURCE_AUDIT.json'
$unit007MathReviewPath = Join-Path $lane 'qa\fomberg-unit-007\INDEPENDENT_MATH_REVIEW_FINAL.json'
$unit007SourceReviewPath = Join-Path $lane 'qa\fomberg-unit-007\INDEPENDENT_SOURCE_LANGUAGE_REVIEW_FINAL.json'
$unit007AssetDir = Join-Path $lane 'source\id-ID\fomberg\assets\unit-007'
$fombergUnitDir = Join-Path $lane 'source\id-ID\fomberg\units'
$baseCss = Join-Path $lane 'source\id-ID\styles\reader.css'
$cumulativeCss = Join-Path $lane 'source\id-ID\styles\reader-cumulative.css'

$priorComposite = [ordered]@{
    (Join-Path $lane 'output\html\roberts-001-030-fomberg-001-006\index.html') = @(12555960, '80a7d092cb786e4d4f7ecab31ba40746cf59398db50f0adca50f2431746f7c92')
    (Join-Path $lane 'output\pdf\topologi-aljabar-roberts-001-030-fomberg-001-006-id.pdf') = @(6723586, '136dc7f6fa744e87fe067a96a36a8fbee8098aad9167629653bc085f6a718c37')
    (Join-Path $lane 'output\ARTIFACT_MANIFEST_ROBERTS_001_030_FOMBERG_001_006.csv') = @(287, 'a6a507bb89af051904d54629738f9f9c355eeadade5bf6c1a7d62ad48bd0858c')
    (Join-Path $lane 'qa\ROBERTS_001_030_FOMBERG_001_006_BUILD_RECEIPT.json') = @(10169, '0347abd8312f8058a769a2b0b01c4d3605798c544c832e0fff82d84ade912829')
}

$htmlDir = Join-Path $lane 'output\html\roberts-001-030-fomberg-001-007'
$pdfDir = Join-Path $lane 'output\pdf'
$html = Join-Path $htmlDir 'index.html'
$pdf = Join-Path $pdfDir 'topologi-aljabar-roberts-001-030-fomberg-001-007-id.pdf'
$manifest = Join-Path $lane 'output\ARTIFACT_MANIFEST_ROBERTS_001_030_FOMBERG_001_007.csv'
$scratch = Join-Path $lane 'tmp\pdfs\roberts-001-030-fomberg-001-007-build'

function Sha256([byte[]]$bytes) {
    $h = [Security.Cryptography.SHA256]::Create()
    try { return [BitConverter]::ToString($h.ComputeHash($bytes)).Replace('-', '').ToLowerInvariant() }
    finally { $h.Dispose() }
}

function AssertIdentity([string]$path, [long]$bytes, [string]$sha) {
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { throw "Missing frozen input: $path" }
    $item = Get-Item -LiteralPath $path
    $actual = (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($item.Length -ne $bytes -or $actual -ne $sha) { throw "Frozen identity mismatch: $path ($($item.Length), $actual)" }
}

function Relative([string]$path) {
    $full = [IO.Path]::GetFullPath($path)
    $prefix = $lane.TrimEnd([IO.Path]::DirectorySeparatorChar) + [IO.Path]::DirectorySeparatorChar
    if (-not $full.StartsWith($prefix, [StringComparison]::OrdinalIgnoreCase)) { throw "Outside lane: $full" }
    return $full.Substring($prefix.Length).Replace('\', '/')
}

function MarkdownBody([string]$path) {
    $bytes = [IO.File]::ReadAllBytes($path)
    if ($bytes.Length -eq 0 -or ($bytes -contains 13)) { throw "Reader is empty or has CR bytes: $path" }
    $text = $utf8.GetString($bytes)
    if (-not $text.StartsWith("---$lf", [StringComparison]::Ordinal)) { throw "Reader lacks YAML front matter: $path" }
    $end = $text.IndexOf("$lf---$lf", 4, [StringComparison]::Ordinal)
    if ($end -lt 0) { throw "Reader front matter is not closed: $path" }
    return $text.Substring($end + 5).TrimStart([char]10).TrimEnd([char]10)
}

foreach ($entry in $priorComposite.GetEnumerator()) { AssertIdentity $entry.Key $entry.Value[0] $entry.Value[1] }
AssertIdentity $robertsAuthority 331447 'cfe93e9dbe3e25bd96f711f59e6078ab97527682b58e1f8ad127f74357f665d7'
AssertIdentity $fombergAuthority 223886 'd27095de0f38f0c14b2d7716cb52d51d064f0594dd9f82f9d1b3e6af5b35a483'
AssertIdentity $fombergLicense 20140 '0b7fc2608b6d990314e908569407a6058b4a29175167c6d91ca0070c946661be'
AssertIdentity $baseCss 1297 'e5184827600116bc54e28df6822c5a98691d5edf88b7b102443b56024733cbe5'
AssertIdentity $cumulativeCss 203 'b0012d9f93e603997d48d49705ec9ccae2d3cd2d062b8b9f8717e908df1f5344'

# Unit 007 is admitted only after its bounded source/static/review gates pass.
foreach ($p in @($unit007QaPath, $unit007SourceAuditPath, $unit007MathReviewPath, $unit007SourceReviewPath)) {
    if (-not (Test-Path -LiteralPath $p -PathType Leaf)) { throw "Missing Unit 007 QA input: $p" }
}
$u7qa = Get-Content -LiteralPath $unit007QaPath -Raw | ConvertFrom-Json
$u7audit = Get-Content -LiteralPath $unit007SourceAuditPath -Raw | ConvertFrom-Json
$u7math = Get-Content -LiteralPath $unit007MathReviewPath -Raw | ConvertFrom-Json
$u7source = Get-Content -LiteralPath $unit007SourceReviewPath -Raw | ConvertFrom-Json
if ($u7qa.status -ne 'PASS' -or $u7qa.qa_id -ne 'O012-FOMBERG-UNIT-007-STATIC-QA' -or
    $u7qa.model_provenance -ne 'OpenAI Codex gpt-5.6-sol, Ultra' -or
    [int]$u7qa.source.selected_span.line_start -ne 3518 -or [int]$u7qa.source.selected_span.line_end -ne 4185 -or
    [int]$u7qa.source.next_line -ne 4186 -or [int]$u7qa.reader.mastery.exercise_hint_solution_triples -ne 6 -or
    [int]$u7qa.reader.mastery.complete_solutions -ne 6 -or [int]$u7qa.reader.assets.semantic_figures -ne 17 -or
    [int]$u7qa.reader.assets.png_fallbacks -ne 3) { throw 'Unit 007 static QA is not the passing 3518-4185 boundary.' }
if ($u7audit.status -notin @('PASS', 'PASS_WITH_MANDATORY_REPAIRS_IDENTIFIED') -or
    $u7audit.edition_unit_id -ne 'O012-FOM-007' -or [int]$u7audit.source.selected_span.line_start -ne 3518 -or
    [int]$u7audit.source.selected_span.line_end -ne 4185 -or [int]$u7audit.next_cursor.next_exact_cursor -ne 4186) { throw 'Unit 007 source audit boundary mismatch.' }
foreach ($r in @($u7math, $u7source)) {
    if ($r.status -notmatch '^PASS' -or [int]$r.severity_census.P1 -ne 0 -or [int]$r.severity_census.P2 -ne 0 -or [int]$r.severity_census.P3 -ne 0) { throw 'Unit 007 independent review is not zero-defect.' }
}

$unit007Reader = $fombergReaders[-1]
if ([string]$u7qa.reader.identity.path -ne (Relative $unit007Reader)) { throw 'Unit 007 QA reader identity path mismatch.' }
AssertIdentity $unit007Reader ([long]$u7qa.reader.identity.bytes) ([string]$u7qa.reader.identity.sha256)
AssertIdentity $unit007SourceAuditPath ([long]$u7qa.source_audit.bytes) ([string]$u7qa.source_audit.sha256)
if ($null -ne $u7qa.independent_review -and $null -ne $u7qa.independent_review.identity) {
    $integratedReviewPath = Join-Path $lane ([string]$u7qa.independent_review.identity.path.Replace('/', '\'))
    if (Test-Path -LiteralPath $integratedReviewPath -PathType Leaf) {
        AssertIdentity $integratedReviewPath ([long]$u7qa.independent_review.identity.bytes) ([string]$u7qa.independent_review.identity.sha256)
    }
}

$u7AssetNames = @('genus-two-cellular-polygon.png','genus-two-cellular-polygon.svg','klein-bottle-cellular-polygon.png','klein-bottle-cellular-polygon.svg','torus-cellular-polygon.png','torus-cellular-polygon.svg')
foreach ($name in $u7AssetNames) {
    $asset = Join-Path $unit007AssetDir $name
    $assetKey = "source/id-ID/fomberg/assets/unit-007/$name"
    $binding = $u7qa.reader.assets.identities.$assetKey
    if ($null -eq $binding) { throw "Unit 007 asset binding missing: $name" }
    AssertIdentity $asset ([long]$binding.bytes) ([string]$binding.sha256)
}

$sourceLines = [IO.File]::ReadAllLines($fombergAuthority)
if ($sourceLines.Count -lt 4186 -or $sourceLines[3517] -ne '\subsection{Cellular homology}' -or $sourceLines[4184] -ne '' -or $sourceLines[4185] -ne '\subsection{Extras before cohomology}') { throw 'Fomberg source cursor witness mismatch.' }
$slice007 = $utf8.GetBytes((($sourceLines[3517..4184] -join $lf) + $lf))
if ($slice007.Length -ne 26533 -or (Sha256 $slice007) -ne 'a22afacfdbecdfad48942421412c4cff1c0f317eb77f18253578125a5d0d7ce2') { throw 'Fomberg Unit 007 source span identity mismatch.' }
$selected = $utf8.GetBytes((($sourceLines[30..4184] -join $lf) + $lf))
if ($selected.Length -ne 161848 -or (Sha256 $selected) -ne '4b96191b5e3cf5006d82175d609a4be8bba567458f7ee1c9f01cfe53490a645c') { throw 'Cumulative Fomberg source witness identity mismatch.' }

$readerBodies = foreach ($p in $robertsReaders + $fombergReaders) { MarkdownBody $p }
$fombergIds = @()
foreach ($p in $fombergReaders) {
    $body = MarkdownBody $p
    $ids = @([regex]::Matches($body, '(?<=#)(o012-fom-[a-z0-9-]+)(?=[}\s])') | ForEach-Object { $_.Groups[1].Value })
    if ($ids.Count -eq 0 -or @($ids | Sort-Object -Unique).Count -ne $ids.Count) { throw "Missing/duplicate Fomberg IDs: $p" }
    $fombergIds += $ids
    foreach ($bad in @('TODO','TBD','FILL_AFTER','C:\Users\','github_pat_','ghp_','access_token')) { if ($body.Contains($bad)) { throw "Forbidden marker $bad in $p" } }
}
if (@($fombergIds | Sort-Object -Unique).Count -ne $fombergIds.Count) { throw 'Cumulative Fomberg IDs collide.' }

$status = @'
# Status pembaca komposit {.unnumbered #o012-composite-status}

Checkpoint ini memuat komponen Roberts lengkap 30/30 serta jembatan Fomberg
Bagian 1.1–1.13 dalam urutan sumber, sampai baris sumber 4185. Fomberg
O012-FOM-007 menerjemahkan Bagian 1.13 (homologi seluler), baris 3518–4185,
dan dipetakan ke D60-R12. Komponen Fomberg bukan kuliah Roberts tambahan dan
tidak mengubah penomoran tiga puluh kuliah Roberts. Jalur komposit masih
parsial karena lapisan penguasaan lintas-rute, laboratorium, dan capstone
belum selesai; kursor sumber berikutnya tepat pada baris 4186.

Pembaca terpadu ini tersedia di bawah CC BY-SA 4.0. Materi Roberts tetap
diidentifikasi sebagai CC BY 4.0 dan materi Fomberg sebagai CC BY-SA 4.0,
dengan atribusi, catatan perubahan, dan pernyataan non-pengesahan masing-masing.
Edisi ini independen. HTML mandiri dengan MathML asli adalah permukaan akses
utama yang reflow; PDF A4 adalah permukaan cetak sekunder dan belum ditag
secara struktural.
'@
$header = @'
---
title: "Topologi Aljabar — Roberts 30/30 dan Fomberg 1.1–1.13"
subtitle: "Komponen Roberts lengkap; jembatan Fomberg melalui homologi seluler; checkpoint komposit parsial"
author:
  - "David Michael Roberts (materi sumber Roberts)"
  - "Yeheli Fomberg (catatan sumber Fomberg; berdasarkan kuliah Nir Lazarovich)"
  - "Edisi Bahasa Indonesia dengan pendamping penguasaan"
date: "26 Agustus 2026"
lang: id-ID
rights: "Pembaca terpadu: CC BY-SA 4.0; komponen Roberts tetap CC BY 4.0 dan komponen Fomberg tetap CC BY-SA 4.0."
provenance: "OpenAI Codex gpt-5.6-sol, Ultra; atas arahan pengguna; seluruh kredit penulis sumber dan kontributor manusia dipertahankan."
source_authorities: "Roberts@b947ad2e9f9e301bfe24590a9db653bc54fa1a53; Fomberg@563194fae879178b9a6871b249513bfc27968975"
---
'@
$boundaries = @(
    "# Komponen Fomberg O012-FOM-001 {.unnumbered #o012-composite-fomberg-001}`n`nBagian 1.1–1.2; dipetakan ke D60-R08.",
    "# Komponen Fomberg O012-FOM-002 {.unnumbered #o012-composite-fomberg-002}`n`nBagian 1.3–1.4; dipetakan ke D60-R09.",
    "# Komponen Fomberg O012-FOM-003 {.unnumbered #o012-composite-fomberg-003}`n`nBagian 1.5–1.6; dipetakan ke D60-R10.",
    "# Komponen Fomberg O012-FOM-004 {.unnumbered #o012-composite-fomberg-004}`n`nBagian 1.7–1.10; dipetakan ke D60-R11.",
    "# Komponen Fomberg O012-FOM-005 {.unnumbered #o012-composite-fomberg-005}`n`nBagian 1.11; dipetakan ke D60-R12 sebagai lapisan derajat opsional.",
    "# Komponen Fomberg O012-FOM-006 {.unnumbered #o012-composite-fomberg-006}`n`nBagian 1.12; dipetakan ke D60-R12 sebagai fondasi kompleks CW.",
    "# Komponen Fomberg O012-FOM-007 {.unnumbered #o012-composite-fomberg-007}`n`nBagian 1.13; dipetakan ke D60-R12 sebagai homologi seluler."
)
$payload = ($header.TrimEnd() + $lf + $lf + $status.Trim() + $lf + $lf)
$payload += $readerBodies[0]
for ($i = 1; $i -lt $robertsReaders.Count; $i++) { $payload += $lf + $lf + $readerBodies[$i] }
for ($j = 0; $j -lt $fombergReaders.Count; $j++) {
    $payload += $lf + $lf + $boundaries[$j] + $lf + $lf + $readerBodies[$robertsReaders.Count + $j]
}
$payload += $lf

if ($payload.IndexOf('#o012-composite-fomberg-001', [StringComparison]::Ordinal) -lt 0 -or
    $payload.IndexOf('#o012-composite-fomberg-007', [StringComparison]::Ordinal) -le $payload.IndexOf('#o012-composite-fomberg-006', [StringComparison]::Ordinal)) { throw 'Composite component order is invalid.' }
if ([regex]::IsMatch($payload, '(?im)^#{1,6}\s+(?:Unit|Kuliah)\s+(?:31|32|33|34|35|36)\b')) { throw 'Fomberg was renumbered as Roberts lectures.' }

if (Test-Path -LiteralPath $scratch) { throw "Build scratch already exists: $scratch" }
foreach ($d in @($htmlDir, $pdfDir, $scratch)) { New-Item -ItemType Directory -Path $d -Force | Out-Null }
$assembled = Join-Path $scratch 'reader-composite.md'
# Pandoc's native TeX reader cannot parse two legacy arrow macros in the
# Roberts source arrays; these build-only substitutions preserve the displayed
# maps while keeping the canonical reader bytes untouched.
$payloadForPandoc = $payload.Replace('\big\downarrow', '\downarrow').Replace('\lhook\joinrel\longrightarrow', '\hookrightarrow')
[IO.File]::WriteAllText($assembled, $payloadForPandoc, $utf8)
$semanticCss = Join-Path $scratch 'semantic-composite.css'
$css = @'
*, *::before, *::after { box-sizing: border-box; }
body { width: min(100%, 72rem); max-width: 72rem; margin-inline: auto; padding: 0 1.25rem 3rem; overflow-wrap: anywhere; }
main, nav, header { max-width: 72rem; margin-inline: auto; }
a, code { overflow-wrap: anywhere; }
math[display="inline"] { display: inline-block; max-width: 100%; overflow-x: auto; overflow-y: hidden; vertical-align: middle; }
table { display: block; max-width: 100%; overflow-x: auto; margin-inline: auto; }
img, svg { display: block; max-width: 100%; height: auto; margin-inline: auto; }
.theorem, .corollary, .fact, .lemma, .proposition { margin: 1.25rem 0; padding: .8rem 1rem; border-left: .3rem solid #315f8c; background: #f3f7fc; }
.remark, .source-margin, .aside { margin: 1.25rem 0; padding: .8rem 1rem; border-left: .3rem solid #8a6a2f; background: #fffaf0; }
.figure { margin: 1.25rem auto; padding: .8rem 1rem; border-left: .3rem solid #5d477a; background: #f8f5fc; text-align: center; }
.figure > * { margin-left: auto; margin-right: auto; }
.hint { margin: 1.25rem 0; padding: .8rem 1rem; border-left: .3rem solid #9a5d20; background: #fff8ef; }
.solution { margin: 1.25rem 0; padding: .8rem 1rem; border-left: .3rem solid #4c7f5d; background: #f5faf6; }
.source-audit, .proof-repair { margin: 1.25rem 0; padding: .8rem 1rem; border: .1rem solid #6d7480; background: #f7f8fa; }
@media (max-width: 700px) { body { width: 100%; margin: 0; padding: 1.25rem 1.1rem 3rem; } }
@media (prefers-color-scheme: dark) { .theorem, .corollary, .fact, .lemma, .proposition, .remark, .source-margin, .aside, .figure, .hint, .solution, .source-audit, .proof-repair { background: #20242a; } }
'@
[IO.File]::WriteAllText($semanticCss, $css.Replace(([char]13).ToString() + $lf, $lf), $utf8)

$pandoc = (Get-Command pandoc -ErrorAction Stop).Source
$pandocVersion = (& $pandoc --version | Select-Object -First 1)
if ($pandocVersion -ne 'pandoc 3.9.0.2') { throw "Expected pandoc 3.9.0.2; found $pandocVersion" }
$pdfinfo = (Get-Command pdfinfo -ErrorAction Stop).Source
$pdffonts = (Get-Command pdffonts -ErrorAction Stop).Source
$pdftotext = (Get-Command pdftotext -ErrorAction Stop).Source
$pdfimages = (Get-Command pdfimages -ErrorAction Stop).Source
$env:SOURCE_DATE_EPOCH = '1787616000'
$env:FORCE_SOURCE_DATE = '1'
$common = @($assembled, '--from=markdown+fenced_divs+tex_math_dollars', '--standalone', '--toc', '--number-sections', '--metadata=lang:id-ID', '--metadata=pagetitle:Topologi Aljabar — Roberts 30/30 dan Fomberg 1.1–1.13', "--resource-path=$fombergUnitDir", '--metadata=provenance:OpenAI Codex gpt-5.6-sol, Ultra', '--strip-comments')

$htmlA = Join-Path $scratch 'composite-a.html'; $htmlB = Join-Path $scratch 'composite-b.html'
$htmlArgs = @('--to=html5', '--mathml', '--section-divs', '--fail-if-warnings', "--css=$baseCss", "--css=$cumulativeCss", "--css=$semanticCss", '--embed-resources')
& $pandoc @common @htmlArgs "--output=$htmlA"; if ($LASTEXITCODE -ne 0) { throw "Pandoc HTML A failed: $LASTEXITCODE" }
& $pandoc @common @htmlArgs "--output=$htmlB"; if ($LASTEXITCODE -ne 0) { throw "Pandoc HTML B failed: $LASTEXITCODE" }
$htmlHashA = (Get-FileHash -LiteralPath $htmlA -Algorithm SHA256).Hash.ToLowerInvariant(); $htmlHashB = (Get-FileHash -LiteralPath $htmlB -Algorithm SHA256).Hash.ToLowerInvariant()
if ($htmlHashA -ne $htmlHashB) { throw "HTML builds are not byte-identical: $htmlHashA != $htmlHashB" }
$htmlText = [IO.File]::ReadAllText($htmlA)
$domIds = @([regex]::Matches($htmlText, '(?<=\s)id="([^"]+)"') | ForEach-Object { $_.Groups[1].Value })
if (@($domIds | Group-Object | Where-Object Count -gt 1).Count -ne 0) { throw 'Duplicate HTML IDs.' }
$domSet = [Collections.Generic.HashSet[string]]::new([string[]]$domIds)
$fragments = @([regex]::Matches($htmlText, '\bhref="#([^"]+)"') | ForEach-Object { $_.Groups[1].Value })
if (@($fragments | Sort-Object -Unique | Where-Object { -not $domSet.Contains($_) }).Count -ne 0) { throw 'Unresolved HTML fragment.' }
if (@($fombergIds | Where-Object { -not $domSet.Contains($_) }).Count -ne 0) { throw 'Fomberg stable ID missing from HTML.' }
$mathml = ([regex]::Matches($htmlText, '<math\b')).Count; $figures = ([regex]::Matches($htmlText, 'class="[^"]*\bfigure\b[^"]*"')).Count
$images = @([regex]::Matches($htmlText, '(?is)<img\b[^>]*>')); $embedded = @([regex]::Matches($htmlText, 'data:image/png;base64,([A-Za-z0-9+/=]+)'))
if ($mathml -le 15273 -or $figures -lt 159 -or $images.Count -ne 19 -or $embedded.Count -ne 19) { throw "HTML census regressed (MathML=$mathml figures=$figures images=$($images.Count) embedded=$($embedded.Count))." }
if ($htmlText -notmatch '<html[^>]+lang="id-ID"' -or $htmlText -match '(?is)<(?:script|link)\b[^>]*(?:src|href)\s*=' -or $htmlText -match '(?is)<img\b[^>]*\bsrc\s*=\s*[''\"]https?://') { throw 'HTML language/self-contained gate failed.' }
foreach ($marker in @('C:\Users\','github_pat_','ghp_','access_token','FILL_AFTER')) { if ($htmlText.Contains($marker)) { throw "Private marker in HTML: $marker" } }
foreach ($cssMarker in @('width: min(100%, 72rem)','max-width: 72rem','margin-inline: auto','@media (max-width: 700px)','math[display="block"]','math[display="inline"]')) { if (-not $htmlText.Contains($cssMarker)) { throw "Responsive CSS marker missing: $cssMarker" } }
if (@($images | Where-Object { $_.Value -notmatch '\balt="[^"]+"' }).Count -ne 0) { throw 'An embedded image lacks alt text.' }
Copy-Item -LiteralPath $htmlA -Destination (Join-Path $htmlDir 'index.html') -Force

$pdfAssembled = Join-Path $scratch 'reader-composite-pdf.md'
# A few legacy display-math lines begin with ``[`` (for example ``[\Gamma]``);
# TeX interprets those as optional-argument syntax at column one.  Bracing
# only those lines while inside ``$$`` preserves their math and avoids the
# MiKTeX "Illegal unit of measure" parse path.
$inDisplayMath = $false
$pdfLines = foreach ($line in ($payloadForPandoc -split $lf, 0, 'SimpleMatch')) {
    if ($line.StartsWith('[') -and $inDisplayMath) { '{}'+$line } else { $line }
    if (([regex]::Matches($line, '\$\$')).Count % 2 -eq 1) { $inDisplayMath = -not $inDisplayMath }
}
if ($inDisplayMath) { throw 'PDF transient assembly ended inside display math.' }
[IO.File]::WriteAllText($pdfAssembled, (($pdfLines -join $lf).TrimEnd([char]10) + $lf), $utf8)
$pdfHeader = Join-Path $scratch 'composite-header.tex'; [IO.File]::WriteAllText($pdfHeader, ("\providecommand{\sslash}{/\mkern-6mu/}$lf\AddToHook{begindocument/end}{\pdftrailerid{}}$lf"), $utf8)
$pdfCommon = @($common); $pdfCommon[0] = $pdfAssembled
$pdfArgs = @('--pdf-engine=pdflatex', "--include-in-header=$pdfHeader", '--variable=papersize:a4', '--variable=geometry:margin=21mm', '--variable=fontsize:11pt', '--variable=colorlinks:true', '--variable=linkcolor:blue', '--variable=pdf-trailer-id:')
$pdfWork = Join-Path $scratch 'composite-work.pdf'; $pdfA = Join-Path $scratch 'composite-a.pdf'; $pdfB = Join-Path $scratch 'composite-b.pdf'
& $pandoc @pdfCommon @pdfArgs "--output=$pdfWork"; if ($LASTEXITCODE -ne 0) { throw "Pandoc PDF A failed: $LASTEXITCODE" }; Copy-Item -LiteralPath $pdfWork -Destination $pdfA -Force
& $pandoc @pdfCommon @pdfArgs "--output=$pdfWork"; if ($LASTEXITCODE -ne 0) { throw "Pandoc PDF B failed: $LASTEXITCODE" }; Copy-Item -LiteralPath $pdfWork -Destination $pdfB -Force
$pdfHashA = (Get-FileHash -LiteralPath $pdfA -Algorithm SHA256).Hash.ToLowerInvariant(); $pdfHashB = (Get-FileHash -LiteralPath $pdfB -Algorithm SHA256).Hash.ToLowerInvariant()
if ($pdfHashA -ne $pdfHashB) { throw "PDF builds are not byte-identical: $pdfHashA != $pdfHashB" }
$pdfInfo = (& $pdfinfo $pdfA) -join $lf; $pm = [regex]::Match($pdfInfo, '(?m)^Pages:\s+(\d+)\s*$')
if (-not $pm.Success -or $pdfInfo -notmatch '(?m)^Page size:.*\(A4\)\s*$' -or $pdfInfo -notmatch '(?m)^Tagged:\s+no\s*$' -or $pdfInfo -notmatch '(?m)^Encrypted:\s+no\s*$') { throw 'PDF metadata gate failed.' }
$pdfPages = [int]$pm.Groups[1].Value; if ($pdfPages -le 452) { throw "PDF did not grow beyond Unit 006 (pages=$pdfPages)." }
$fontRows = @((& $pdffonts $pdfA) | Select-Object -Skip 2 | Where-Object { $_.Trim().Length -gt 0 }); if ($fontRows.Count -eq 0) { throw 'PDF font inventory empty.' }
foreach ($row in $fontRows) { $m = [regex]::Match($row, '\s+(yes|no)\s+(yes|no)\s+(yes|no)\s+\d+\s+\d+\s*$'); if (-not $m.Success -or $m.Groups[1].Value -ne 'yes' -or $m.Groups[2].Value -ne 'yes' -or $m.Groups[3].Value -ne 'yes') { throw "PDF font embedding/ToUnicode failure: $row" } }
$pdfTextPath = Join-Path $scratch 'composite.txt'; & $pdftotext '-enc' 'UTF-8' $pdfA $pdfTextPath; if ($LASTEXITCODE -ne 0) { throw 'pdftotext failed.' }; $pdfText = [IO.File]::ReadAllText($pdfTextPath); $pdfNorm = [regex]::Replace($pdfText, '\s+', ' ').Trim()
foreach ($required in @('Roberts lengkap 30/30','Fomberg O012-FOM-001','Fomberg O012-FOM-002','Fomberg O012-FOM-003','Fomberg O012-FOM-004','Fomberg O012-FOM-005','Fomberg O012-FOM-006','Fomberg O012-FOM-007','Bagian 1.1–1.13','baris sumber 4185','CC BY 4.0','CC BY-SA 4.0','OpenAI Codex gpt-5.6-sol, Ultra')) { if (-not $pdfNorm.Contains($required)) { throw "Required PDF text missing: $required" } }
foreach ($marker in @('C:\Users\','github_pat_','ghp_','access_token','FILL_AFTER')) { if ($pdfText.Contains($marker)) { throw "Private marker in PDF: $marker" } }
$pdfImageRows = @((& $pdfimages '-list' $pdfA) | Where-Object { $_ -match '^\s*\d+\s+\d+\s+' })
$pdfPrimaryRows = @($pdfImageRows | Where-Object { $_ -match '^\s*\d+\s+\d+\s+image\s+' })
# The three Unit-007 redraw PNGs are opaque RGB assets and therefore do not
# receive separate soft-mask rows; prior transparent assets do.  Bind the
# primary-image census exactly and accept the resulting 16*2+3 row total.
if ($pdfPrimaryRows.Count -ne 19 -or $pdfImageRows.Count -lt 35) { throw "PDF image inventory mismatch (rows=$($pdfImageRows.Count), primary=$($pdfPrimaryRows.Count))." }
Copy-Item -LiteralPath $pdfA -Destination $pdf -Force

$manifestLines = @('path,bytes,sha256')
foreach ($artifact in @((Join-Path $htmlDir 'index.html'), $pdf)) { $item = Get-Item -LiteralPath $artifact; $manifestLines += "$(Relative $artifact),$($item.Length),$((Get-FileHash -LiteralPath $artifact -Algorithm SHA256).Hash.ToLowerInvariant())" }
[IO.File]::WriteAllText($manifest, (($manifestLines -join $lf) + $lf), $utf8)

$result = [ordered]@{
    status = 'PASS'; scope = 'Roberts 30/30; Fomberg Sections 1.1-1.13 through source line 4185; composite partial'
    html = [ordered]@{ path = (Relative (Join-Path $htmlDir 'index.html')); bytes = (Get-Item -LiteralPath (Join-Path $htmlDir 'index.html')).Length; sha256 = (Get-FileHash -LiteralPath (Join-Path $htmlDir 'index.html') -Algorithm SHA256).Hash.ToLowerInvariant(); byte_identical_builds = 2; dom_ids = $domIds.Count; fragment_links = $fragments.Count; mathml_nodes = $mathml; semantic_figures = $figures; embedded_pngs = $embedded.Count }
    pdf = [ordered]@{ path = (Relative $pdf); bytes = (Get-Item -LiteralPath $pdf).Length; sha256 = (Get-FileHash -LiteralPath $pdf -Algorithm SHA256).Hash.ToLowerInvariant(); byte_identical_builds = 2; pages = $pdfPages; fonts = $fontRows.Count; image_rows = $pdfImageRows.Count; tagged = $false }
    manifest = [ordered]@{ path = (Relative $manifest); bytes = (Get-Item -LiteralPath $manifest).Length; sha256 = (Get-FileHash -LiteralPath $manifest -Algorithm SHA256).Hash.ToLowerInvariant() }
    source = [ordered]@{ roberts = 'Notes.tex@b947ad2e9f9e301bfe24590a9db653bc54fa1a53'; fomberg = 'algebraic_topology.tex@563194fae879178b9a6871b249513bfc27968975'; selected_span = '31-4185'; next_line = 4186; selected_bytes = $selected.Length; selected_sha256 = (Sha256 $selected) }
    toolchain = [ordered]@{ pandoc = $pandocVersion; source_date_epoch = [int64]$env:SOURCE_DATE_EPOCH; model_provenance = 'OpenAI Codex gpt-5.6-sol, Ultra'; html_builds_byte_identical = $true; pdf_builds_byte_identical = $true }
}
$result | ConvertTo-Json -Depth 6

$scratchFull = [IO.Path]::GetFullPath($scratch); $allowed = [IO.Path]::GetFullPath((Join-Path $lane 'tmp\pdfs')) + [IO.Path]::DirectorySeparatorChar
if (-not $scratchFull.StartsWith($allowed, [StringComparison]::OrdinalIgnoreCase) -or [IO.Path]::GetFileName($scratchFull) -ne 'roberts-001-030-fomberg-001-007-build') { throw 'Refusing scratch deletion outside bounded path.' }
Remove-Item -LiteralPath $scratchFull -Recurse -Force
if (Test-Path -LiteralPath $scratchFull) { throw 'Build scratch removal failed.' }
