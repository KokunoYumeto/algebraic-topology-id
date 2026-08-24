[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$lane = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$lf = [string][char]10
$tab = [string][char]9
$utf8 = [Text.UTF8Encoding]::new($false)
$baselineBuilder = Join-Path $PSScriptRoot 'build-units-001-030.ps1'
$robertsAuthority = Join-Path $lane 'authority\upstream\AlgebraicTopology2019-b947ad2e9f9e301bfe24590a9db653bc54fa1a53\Notes.tex'
$robertsLicense = Join-Path $lane 'authority\upstream\AlgebraicTopology2019-b947ad2e9f9e301bfe24590a9db653bc54fa1a53\LICENSE.md'
$fombergAuthority = Join-Path $lane 'authority\upstream\math-notes-563194fae879178b9a6871b249513bfc27968975\tree\algebraic_topology.tex'
$fombergLicense = Join-Path $lane 'authority\upstream\math-notes-563194fae879178b9a6871b249513bfc27968975\tree\LICENSE'
$fombergReader = Join-Path $lane 'source\id-ID\fomberg\units\fomberg-unit-001-delta-complexes-simplicial-homology.md'
$baseCss = Join-Path $lane 'source\id-ID\styles\reader.css'
$cumulativeCss = Join-Path $lane 'source\id-ID\styles\reader-cumulative.css'

$htmlDir = Join-Path $lane 'output\html\roberts-001-030-fomberg-001'
$pdfDir = Join-Path $lane 'output\pdf'
$scratch = Join-Path $lane 'tmp\pdfs\roberts-001-030-fomberg-001-build'
$html = Join-Path $htmlDir 'index.html'
$pdf = Join-Path $pdfDir 'topologi-aljabar-roberts-001-030-fomberg-001-id.pdf'
$manifest = Join-Path $lane 'output\ARTIFACT_MANIFEST_ROBERTS_001_030_FOMBERG_001.csv'

function Get-Sha256([byte[]]$bytes) {
    return [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($bytes)).ToLowerInvariant()
}

function Assert-Frozen([string]$path, [long]$bytes, [string]$sha256) {
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
        throw "Missing frozen input: $path"
    }
    $item = Get-Item -LiteralPath $path
    $actual = (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($item.Length -ne $bytes -or $actual -ne $sha256) {
        throw "Frozen input identity mismatch: $path"
    }
}

function Get-MarkdownBody([string]$path) {
    $bytes = [IO.File]::ReadAllBytes($path)
    if ($bytes -contains 13) { throw "CR byte in LF-frozen reader: $path" }
    $text = [Text.Encoding]::UTF8.GetString($bytes)
    if (-not $text.StartsWith("---$lf")) { throw "Missing YAML front matter: $path" }
    $end = $text.IndexOf("$lf---$lf", 4, [StringComparison]::Ordinal)
    if ($end -lt 0) { throw "Unclosed YAML front matter: $path" }
    return $text.Substring($end + 5).TrimStart([char]10)
}

# Verify the complete Roberts 30/30 boundary without invoking or rewriting it.
$baselineFrozen = @{
    $baselineBuilder = @(22753, '96c2d80c20c2900e63f0a18e2a4a5387b7b78d78be5864c2f973ba365c5a9c89')
    (Join-Path $lane 'output\html\units-001-030\index.html') = @(4861791, 'ed9da5653b3eacf7418d6e08760fcd2ecff4d75799c47f08689b940798099891')
    (Join-Path $lane 'output\pdf\topologi-aljabar-unit-001-030-id.pdf') = @(2257988, 'b9d37776c64541123345c7b28fd26df161b878e8c105c16670455fd532dc08a4')
    (Join-Path $lane 'output\ARTIFACT_MANIFEST_UNITS_001_030.csv') = @(249, '7a560c51d3dc3679893408a241c2d53f6875eed20c635a96673fa199f0bb40af')
    (Join-Path $lane 'qa\UNITS_001_030_BUILD_RECEIPT.json') = @(12488, '15ce778ae5b85934424b3da22dcbec99f15df30746bb01630aaa4494cb3eace7')
    (Join-Path $lane 'qa\UNITS_001_030_VISUAL_QA.md') = @(6060, '6e1c65d1ad2c6eeedb1a3e934489a8d21d0374985b81ec5708340537c1157727')
    (Join-Path $lane 'qa\UNITS_001_030_RENDER_INVENTORY.csv') = @(2059, 'b776c8bda19ccbb1fca9ad0fb2940e9bd6bb468cea98ac655d63210f832e137f')
    $baseCss = @(1297, 'e5184827600116bc54e28df6822c5a98691d5edf88b7b102443b56024733cbe5')
    $cumulativeCss = @(203, 'b0012d9f93e603997d48d49705ec9ccae2d3cd2d062b8b9f8717e908df1f5344')
}
foreach ($path in $baselineFrozen.Keys) {
    $want = $baselineFrozen[$path]
    Assert-Frozen $path $want[0] $want[1]
}

Assert-Frozen $robertsAuthority 331447 'cfe93e9dbe3e25bd96f711f59e6078ab97527682b58e1f8ad127f74357f665d7'
Assert-Frozen $robertsLicense 18696 '2ecfbc56ead071b6a93908f50b59c4186db6d139c8b7d0c56156bb0ad5fad3f5'
Assert-Frozen $fombergAuthority 223886 'd27095de0f38f0c14b2d7716cb52d51d064f0594dd9f82f9d1b3e6af5b35a483'
Assert-Frozen $fombergLicense 20140 '0b7fc2608b6d990314e908569407a6058b4a29175167c6d91ca0070c946661be'
Assert-Frozen $fombergReader 34773 'd9b64140f9340c75bc34c12bc02ee843d87de3566e331c50c2374075718aa2c6'

$baselineReceipt = [IO.File]::ReadAllText((Join-Path $lane 'qa\UNITS_001_030_BUILD_RECEIPT.json'))
if ($baselineReceipt -notmatch '"status"\s*:\s*"PASS"' -or
    -not $baselineReceipt.Contains('Roberts Indonesian reader Units 001-030') -or
    -not $baselineReceipt.Contains('terminal_source_eof') -or
    -not $baselineReceipt.Contains('b9d37776c64541123345c7b28fd26df161b878e8c105c16670455fd532dc08a4')) {
    throw 'Frozen Roberts 30/30 build receipt is not the passing terminal boundary.'
}

$robertsSources = @((Join-Path $lane 'source\id-ID\reader-unit-001.md')) + @(
    2..30 | ForEach-Object {
        Join-Path $lane ("source\id-ID\units\unit-{0:000}-lecture-{0:000}.md" -f $_)
    }
)
$sourceRows = foreach ($source in $robertsSources) {
    if (-not (Test-Path -LiteralPath $source -PathType Leaf)) { throw "Missing Roberts reader source: $source" }
    $bytes = [IO.File]::ReadAllBytes($source)
    if ($bytes -contains 13 -or $bytes.Length -eq 0 -or $bytes[-1] -ne 10) {
        throw "Roberts reader is not nonempty LF-frozen UTF-8: $source"
    }
    [void](Get-MarkdownBody $source)
    $relative = [IO.Path]::GetRelativePath($lane, $source).Replace('\', '/')
    "$relative$tab$($bytes.Length)$tab$(Get-Sha256 $bytes)"
}
$sourceManifestText = ($sourceRows -join $lf) + $lf
$sourceManifestBytes = $utf8.GetBytes($sourceManifestText)
$sourceTotalBytes = ($robertsSources | ForEach-Object { (Get-Item -LiteralPath $_).Length } | Measure-Object -Sum).Sum
$sourceTotalLf = ($robertsSources | ForEach-Object {
    ([regex]::Matches([IO.File]::ReadAllText($_), $lf)).Count
} | Measure-Object -Sum).Sum
if ($robertsSources.Count -ne 30 -or $sourceTotalBytes -ne 959341 -or $sourceTotalLf -ne 29430 -or
    $sourceManifestBytes.Length -ne 3409 -or
    (Get-Sha256 $sourceManifestBytes) -ne '73d72a7bcdcfb5f513c1cbc3930def67399da6a187babf0a7e09aae08d4b0977') {
    throw 'Ordered Roberts Units 001-030 reader bundle identity mismatch.'
}

$fombergAuthorityLines = [IO.File]::ReadAllLines($fombergAuthority)
$fombergSliceText = ($fombergAuthorityLines[30..613] -join $lf) + $lf
$fombergSliceBytes = $utf8.GetBytes($fombergSliceText)
if ($fombergSliceBytes.Length -ne 21875 -or
    (Get-Sha256 $fombergSliceBytes) -ne '68cb0dea7aa24a42e979877a95acf61b8152c87ed86d88ad7deac7cb5cea2fe3') {
    throw 'Frozen Fomberg lines 31-614 identity mismatch.'
}

$fombergText = [IO.File]::ReadAllText($fombergReader)
foreach ($marker in @('TODO', 'TBD', 'FILL_AFTER', 'C:\Users\', 'C:/Users/', 'github_pat_', 'ghp_', 'sk-proj_', 'access_token', 'Unit 31', 'Kuliah 31')) {
    if ($fombergText.Contains($marker)) { throw "Private, placeholder, or renumbering marker in Fomberg reader: $marker" }
}
$fombergIds = [regex]::Matches($fombergText, '#(o012-fom-[a-z0-9-]+)(?=[}\s])') |
    ForEach-Object { $_.Groups[1].Value }
if ($fombergIds.Count -ne 87 -or @($fombergIds | Sort-Object -Unique).Count -ne 87) {
    throw 'Fomberg stable-ID census mismatch.'
}
if (([regex]::Matches($fombergText, '(?m)^[ \t]*::: \{')).Count -ne 82 -or
    ([regex]::Matches($fombergText, '(?m)^[ \t]*:::\s*$')).Count -ne 82) {
    throw 'Fomberg semantic block balance mismatch.'
}
foreach ($pair in @(@('figure',10), @('exercise',6), @('hint',6), @('solution',6))) {
    $count = ([regex]::Matches($fombergText, "(?m)^[ \t]*::: \{\.$($pair[0])\s+#o012-fom-")).Count
    if ($count -ne $pair[1]) { throw "Fomberg $($pair[0]) census mismatch: $count" }
}
if (-not $fombergText.Contains('course_route_unit_id: "D60-R08"') -or
    -not $fombergText.Contains('CC BY-SA 4.0') -or
    -not $fombergText.Contains('OpenAI Codex gpt-5.6-sol, Ultra') -or
    -not [regex]::IsMatch($fombergText, 'Kursor komponen\s+berikutnya adalah baris 615')) {
    throw 'Fomberg route, rights, provenance, or cursor marker is missing.'
}

$pandoc = (Get-Command pandoc -ErrorAction Stop).Source
$pandocVersion = (& $pandoc --version | Select-Object -First 1)
if ($pandocVersion -ne 'pandoc 3.9.0.2') { throw "Expected pandoc 3.9.0.2; found: $pandocVersion" }
$pdfinfo = (Get-Command pdfinfo -ErrorAction Stop).Source
$pdffonts = (Get-Command pdffonts -ErrorAction Stop).Source
$pdftotext = (Get-Command pdftotext -ErrorAction Stop).Source

if (Test-Path -LiteralPath $scratch) { throw "Build scratch already exists: $scratch" }
foreach ($dir in @($htmlDir, $pdfDir, $scratch)) {
    New-Item -ItemType Directory -Path $dir -Force | Out-Null
}

$assembled = Join-Path $scratch 'reader-composite.md'
$header = @'
---
title: "Topologi Aljabar - Roberts 30/30 dan Fomberg 1.1-1.2"
subtitle: "Komponen Roberts lengkap; jembatan homologi Fomberg dimulai; jalur komposit masih parsial"
author:
  - "David Michael Roberts (materi sumber Roberts)"
  - "Yeheli Fomberg (catatan sumber Fomberg; berdasarkan kuliah Nir Lazarovich)"
  - "Edisi Bahasa Indonesia dengan pendamping penguasaan"
date: "24 Agustus 2026"
lang: id-ID
rights: "Pembaca terpadu: CC BY-SA 4.0; komponen Roberts tetap CC BY 4.0 dan komponen Fomberg tetap CC BY-SA 4.0."
provenance: "OpenAI Codex gpt-5.6-sol, Ultra; atas arahan pengguna; seluruh kredit penulis sumber dan kontributor manusia dipertahankan."
source_authorities: "Roberts@b947ad2e9f9e301bfe24590a9db653bc54fa1a53; Fomberg@563194fae879178b9a6871b249513bfc27968975"
---

# Status pembaca komposit {.unnumbered #o012-composite-status}

Checkpoint ini memuat komponen Roberts lengkap 30/30 dan komponen Fomberg
O012-FOM-001 yang menerjemahkan Bagian 1.1-1.2, baris sumber 31-614. Jalur
komposit masih parsial: jembatan Fomberg berikutnya dan lapisan penguasaan
lintas-rute belum selesai. Komponen Fomberg bukan kuliah Roberts tambahan dan
tidak mengubah penomoran tiga puluh kuliah Roberts.

Pembaca terpadu ini tersedia di bawah CC BY-SA 4.0. Di dalamnya, materi
Roberts tetap dikenali sebagai CC BY 4.0 dan materi Fomberg tetap dikenali
sebagai CC BY-SA 4.0, dengan atribusi, catatan perubahan, serta pernyataan
non-pengesahan pada masing-masing komponen. Edisi ini independen.

HTML mandiri yang reflow dengan MathML asli adalah permukaan aksesibilitas
utama. PDF A4 adalah permukaan cetak sekunder; seluruh font harus tersemat dan
memiliki peta ToUnicode, tetapi PDF ini belum ditag secara struktural.

'@
$robertsParts = foreach ($source in $robertsSources) {
    (Get-MarkdownBody $source).TrimEnd([char]10)
}
$fombergBody = (Get-MarkdownBody $fombergReader).TrimEnd([char]10)
$fombergBody = [regex]::Replace(
    $fombergBody,
    '(?m)^(#{1,6}[^\r\n]*\{)#(o012-fom-[^}\s]+)',
    '$1.unnumbered #$2'
)
$componentBoundary = @'

# Komponen Fomberg O012-FOM-001 {.unnumbered #o012-composite-fomberg-001}

Bagian berikut adalah komponen Fomberg yang terpisah, dipetakan ke D60-R08.
Ia tidak dinomori sebagai kuliah Roberts tambahan.

'@
$payload = $header.Replace(([char]13).ToString() + $lf, $lf) +
    $lf + $lf +
    ($robertsParts -join ($lf + $lf)) +
    $componentBoundary.Replace(([char]13).ToString() + $lf, $lf).TrimEnd([char]10) + $lf + $lf +
    $fombergBody + $lf
if ([regex]::IsMatch($payload, '(?im)^#{1,6}\s+(?:Unit|Kuliah)\s+31\b') -or
    [regex]::IsMatch($payload, '(?i)#[-a-z0-9]*unit-031(?:[-}\s]|$)')) {
    throw 'Transient composite payload renumbers Fomberg as Roberts Unit 31.'
}
[IO.File]::WriteAllText($assembled, $payload, $utf8)

$htmlAssembled = Join-Path $scratch 'reader-composite-html.md'
$htmlPayload = $payload.Replace('\big\downarrow', '\downarrow').Replace('\lhook\joinrel\longrightarrow', '\hookrightarrow')
[IO.File]::WriteAllText($htmlAssembled, $htmlPayload, $utf8)

$semanticCss = Join-Path $scratch 'semantic-composite.css'
$semanticRules = @'
*, *::before, *::after { box-sizing: border-box; }
body { width: min(100%, 72rem); max-width: 72rem; margin-inline: auto; overflow-wrap: anywhere; }
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
.source-audit { margin: 1.25rem 0; padding: .8rem 1rem; border: .1rem solid #6d7480; background: #f7f8fa; }
.boundary { margin: 1.25rem 0; padding: .8rem 1rem; border: .12rem solid #8a6a2f; background: #fffdf7; }
@media (max-width: 700px) { body { width: 100%; margin: 0; padding: 1.25rem 1.1rem 3rem; } }
@media (prefers-color-scheme: dark) { .theorem, .corollary, .fact, .lemma, .proposition, .remark, .source-margin, .aside, .figure, .hint, .solution, .source-audit, .boundary { background: #20242a; } }
'@
[IO.File]::WriteAllText($semanticCss, $semanticRules.Replace(([char]13).ToString() + $lf, $lf), $utf8)

$env:SOURCE_DATE_EPOCH = '1787529600'
$env:FORCE_SOURCE_DATE = '1'
$common = @(
    $htmlAssembled,
    '--from=markdown+fenced_divs+tex_math_dollars',
    '--standalone',
    '--toc',
    '--number-sections',
    '--metadata=lang:id-ID',
    '--metadata=pagetitle:Topologi Aljabar - Roberts 30/30 dan Fomberg 1.1-1.2',
    '--metadata=provenance:OpenAI Codex gpt-5.6-sol, Ultra',
    '--strip-comments'
)

$htmlA = Join-Path $scratch 'composite-a.html'
$htmlB = Join-Path $scratch 'composite-b.html'
$htmlArgs = @(
    '--to=html5',
    '--mathml',
    '--section-divs',
    '--fail-if-warnings',
    "--css=$baseCss",
    "--css=$cumulativeCss",
    "--css=$semanticCss",
    '--embed-resources'
)
& $pandoc @common @htmlArgs "--output=$htmlA"
if ($LASTEXITCODE -ne 0) { throw "Pandoc HTML build A failed with exit $LASTEXITCODE" }
& $pandoc @common @htmlArgs "--output=$htmlB"
if ($LASTEXITCODE -ne 0) { throw "Pandoc HTML build B failed with exit $LASTEXITCODE" }
$htmlHashA = (Get-FileHash -LiteralPath $htmlA -Algorithm SHA256).Hash.ToLowerInvariant()
$htmlHashB = (Get-FileHash -LiteralPath $htmlB -Algorithm SHA256).Hash.ToLowerInvariant()
if ($htmlHashA -ne $htmlHashB) { throw "HTML reproducibility failure: $htmlHashA != $htmlHashB" }

$htmlText = [IO.File]::ReadAllText($htmlA)
$domIds = [regex]::Matches($htmlText, '(?<=\s)id="(?<id>[^"]+)"') | ForEach-Object { $_.Groups['id'].Value }
$duplicates = @($domIds | Group-Object | Where-Object Count -gt 1)
if ($duplicates.Count -ne 0) { throw "Duplicate HTML IDs: $($duplicates.Name -join ', ')" }
$domIdSet = [Collections.Generic.HashSet[string]]::new([string[]]@($domIds))
$fragmentLinks = [regex]::Matches($htmlText, '\bhref="#(?<id>[^"]+)"') |
    ForEach-Object { [Uri]::UnescapeDataString($_.Groups['id'].Value) }
$missingFragments = @($fragmentLinks | Sort-Object -Unique | Where-Object { -not $domIdSet.Contains($_) })
if ($missingFragments.Count -ne 0) { throw "Unresolved HTML fragment targets: $($missingFragments -join ', ')" }
$missingFombergIds = @($fombergIds | Where-Object { -not $domIdSet.Contains($_) })
if ($missingFombergIds.Count -ne 0) { throw "Fomberg IDs missing from HTML: $($missingFombergIds -join ', ')" }
if (-not $domIdSet.Contains('o012-rbt-u001-notice')) {
    throw 'Roberts Unit 001 notice heading/anchor was lost at the composite boundary.'
}
if ($htmlText.Contains('# Tentang unit ini {.unnumbered #o012-rbt-u001-notice}')) {
    throw 'Literal Roberts Unit 001 Markdown leaked into HTML.'
}

$htmlPlain = [Net.WebUtility]::HtmlDecode([regex]::Replace($htmlText, '(?s)<[^>]+>', ' '))
$htmlNormalized = [regex]::Replace($htmlPlain, '\s+', ' ').Trim()
foreach ($required in @(
    'Roberts lengkap 30/30',
    'komponen Fomberg',
    'jalur komposit masih parsial',
    'CC BY 4.0',
    'CC BY-SA 4.0',
    'Edisi ini independen',
    'OpenAI Codex gpt-5.6-sol, Ultra',
    'belum ditag secara struktural'
)) {
    if (-not $htmlNormalized.Contains($required)) { throw "Required scope/rights/provenance marker missing from HTML: $required" }
}
if ($htmlText -notmatch '<html[^>]+lang="id-ID"' -or
    $htmlText -match '(?is)<script\b[^>]*\bsrc\s*=' -or
    $htmlText -match '(?is)<link\b[^>]*\bhref\s*=' -or
    $htmlText -match '(?is)<(?:img|iframe)\b[^>]*\bsrc\s*=\s*["'']https?://') {
    throw 'HTML language or self-contained runtime-dependency gate failed.'
}
foreach ($marker in @('C:\Users\', 'C:/Users/', 'github_pat_', 'ghp_', 'sk-proj_', 'access_token', 'FILL_AFTER')) {
    if ($htmlText.Contains($marker)) { throw "Private, placeholder, or renumbering marker in HTML: $marker" }
}
$mathmlNodes = ([regex]::Matches($htmlText, '<math\b')).Count
$semanticFigures = ([regex]::Matches($htmlText, 'class="[^"]*\bfigure\b[^"]*"')).Count
$rawMathFallbacks = ([regex]::Matches($htmlText, '<span class="math (?:display|inline)">')).Count
if ($mathmlNodes -le 11787 -or $semanticFigures -lt 75 -or $rawMathFallbacks -ne 0) {
    throw 'HTML lost composite MathML/semantic figures or retained raw-TeX math fallback.'
}
foreach ($cssMarker in @(
    'width: min(100%, 72rem)',
    'max-width: 72rem',
    'margin-inline: auto',
    '@media (max-width: 700px)',
    'math[display="block"]',
    'math[display="inline"]'
)) {
    if (-not $htmlText.Contains($cssMarker)) { throw "Responsive/centering CSS marker missing: $cssMarker" }
}
Copy-Item -LiteralPath $htmlA -Destination $html -Force

$pdfAssembled = Join-Path $scratch 'reader-composite-pdf.md'
$inDisplayMath = $false
$pdfLines = foreach ($line in ($payload -split $lf, 0, 'SimpleMatch')) {
    if ($line.StartsWith('[') -and $inDisplayMath) { '{}'+$line } else { $line }
    if (([regex]::Matches($line, '\$\$')).Count % 2 -eq 1) { $inDisplayMath = -not $inDisplayMath }
}
if ($inDisplayMath) { throw 'PDF transient assembly ended inside display math.' }
[IO.File]::WriteAllText($pdfAssembled, (($pdfLines -join $lf).TrimEnd([char]10) + $lf), $utf8)

$pdfHeader = Join-Path $scratch 'composite-header.tex'
[IO.File]::WriteAllText($pdfHeader, '\providecommand{\sslash}{/\mkern-6mu/}' + $lf, $utf8)
$pdfCommon = @($common)
$pdfCommon[0] = $pdfAssembled
$pdfA = Join-Path $scratch 'composite-a.pdf'
$pdfB = Join-Path $scratch 'composite-b.pdf'
$pdfArgs = @(
    '--pdf-engine=pdflatex',
    "--include-in-header=$pdfHeader",
    '--variable=papersize:a4',
    '--variable=geometry:margin=21mm',
    '--variable=fontsize:11pt',
    '--variable=colorlinks:true',
    '--variable=linkcolor:blue'
)
& $pandoc @pdfCommon @pdfArgs "--output=$pdfA"
if ($LASTEXITCODE -ne 0) { throw "Pandoc PDF build A failed with exit $LASTEXITCODE" }
& $pandoc @pdfCommon @pdfArgs "--output=$pdfB"
if ($LASTEXITCODE -ne 0) { throw "Pandoc PDF build B failed with exit $LASTEXITCODE" }
$pdfHashA = (Get-FileHash -LiteralPath $pdfA -Algorithm SHA256).Hash.ToLowerInvariant()
$pdfHashB = (Get-FileHash -LiteralPath $pdfB -Algorithm SHA256).Hash.ToLowerInvariant()
if ($pdfHashA -ne $pdfHashB) { throw "PDF reproducibility failure: $pdfHashA != $pdfHashB" }

$pdfInfoText = (& $pdfinfo $pdfA) -join $lf
$pagesMatch = [regex]::Match($pdfInfoText, '(?m)^Pages:\s+(\d+)\s*$')
if (-not $pagesMatch.Success -or
    $pdfInfoText -notmatch '(?m)^Page size:.*\(A4\)\s*$' -or
    $pdfInfoText -notmatch '(?m)^Tagged:\s+no\s*$' -or
    $pdfInfoText -notmatch '(?m)^Encrypted:\s+no\s*$') {
    throw 'PDF A4, page-count, untagged, or encryption gate failed.'
}
$pdfPages = [int]$pagesMatch.Groups[1].Value
$fontOutput = @(& $pdffonts $pdfA)
$fontRows = @($fontOutput | Select-Object -Skip 2 | Where-Object { $_.Trim().Length -gt 0 })
if ($fontRows.Count -eq 0) { throw 'PDF font inventory is empty.' }
foreach ($row in $fontRows) {
    $match = [regex]::Match($row, '\s+(yes|no)\s+(yes|no)\s+(yes|no)\s+\d+\s+\d+\s*$')
    if (-not $match.Success -or $match.Groups[1].Value -ne 'yes' -or
        $match.Groups[2].Value -ne 'yes' -or $match.Groups[3].Value -ne 'yes') {
        throw "PDF font is not embedded, subset, and ToUnicode-mapped: $row"
    }
}

$pdfTextPath = Join-Path $scratch 'composite.txt'
& $pdftotext '-enc' 'UTF-8' $pdfA $pdfTextPath
if ($LASTEXITCODE -ne 0) { throw "pdftotext failed with exit $LASTEXITCODE" }
$pdfText = [IO.File]::ReadAllText($pdfTextPath)
$pdfNormalized = [regex]::Replace($pdfText, '\s+', ' ').Trim()
foreach ($required in @('Roberts lengkap 30/30', 'komponen Fomberg', 'CC BY-SA 4.0', 'OpenAI Codex gpt-5.6-sol, Ultra')) {
    if (-not $pdfNormalized.Contains($required)) { throw "Required scope/rights/provenance marker missing from PDF text: $required" }
}
foreach ($marker in @('C:\Users\', 'C:/Users/', 'github_pat_', 'ghp_', 'sk-proj_', 'access_token', 'FILL_AFTER')) {
    if ($pdfText.Contains($marker)) { throw "Private, placeholder, or renumbering marker in PDF text: $marker" }
}
if ($pdfText.Contains('# Tentang unit ini {.unnumbered #o012-rbt-u001-notice}')) {
    throw 'Literal Roberts Unit 001 Markdown leaked into PDF text.'
}
Copy-Item -LiteralPath $pdfA -Destination $pdf -Force

$artifactRows = foreach ($artifact in @($html, $pdf)) {
    $item = Get-Item -LiteralPath $artifact
    $relative = [IO.Path]::GetRelativePath($lane, $item.FullName).Replace('\', '/')
    "$relative,$($item.Length),$((Get-FileHash -LiteralPath $artifact -Algorithm SHA256).Hash.ToLowerInvariant())"
}
[IO.File]::WriteAllText(
    $manifest,
    'path,bytes,sha256' + $lf + (($artifactRows | Sort-Object) -join $lf) + $lf,
    $utf8
)

$scratchFull = [IO.Path]::GetFullPath($scratch)
$allowedScratchRoot = [IO.Path]::GetFullPath((Join-Path $lane 'tmp\pdfs')) + [IO.Path]::DirectorySeparatorChar
if (-not $scratchFull.StartsWith($allowedScratchRoot, [StringComparison]::OrdinalIgnoreCase) -or
    [IO.Path]::GetFileName($scratchFull) -ne 'roberts-001-030-fomberg-001-build') {
    throw "Refusing to delete unresolved build scratch: $scratchFull"
}
Remove-Item -LiteralPath $scratchFull -Recurse -Force
if (Test-Path -LiteralPath $scratchFull) { throw 'Successful build scratch was not removed.' }

[pscustomobject]@{
    status = 'PASS'
    scope = 'Roberts 30/30 complete; Fomberg Sections 1.1-1.2; composite partial'
    html = $html
    html_bytes = (Get-Item -LiteralPath $html).Length
    html_sha256 = $htmlHashA
    html_dom_ids = $domIds.Count
    html_fragment_links = $fragmentLinks.Count
    html_mathml_nodes = $mathmlNodes
    html_semantic_figures = $semanticFigures
    fomberg_ids = $fombergIds.Count
    pdf = $pdf
    pdf_bytes = (Get-Item -LiteralPath $pdf).Length
    pdf_sha256 = $pdfHashA
    pdf_pages = $pdfPages
    pdf_fonts = $fontRows.Count
    pdf_fonts_embedded_subset_tounicode = $true
    pdf_tagged = $false
    manifest = $manifest
    manifest_sha256 = (Get-FileHash -LiteralPath $manifest -Algorithm SHA256).Hash.ToLowerInvariant()
    pandoc = $pandocVersion
    source_date_epoch = $env:SOURCE_DATE_EPOCH
    model_provenance = 'OpenAI Codex gpt-5.6-sol, Ultra'
    scratch_removed = $true
}
