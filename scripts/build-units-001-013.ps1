[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$lane = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$sources = @(
    (Join-Path $lane 'source\id-ID\reader-unit-001.md'),
    (Join-Path $lane 'source\id-ID\units\unit-002-lecture-002.md'),
    (Join-Path $lane 'source\id-ID\units\unit-003-lecture-003.md'),
    (Join-Path $lane 'source\id-ID\units\unit-004-lecture-004.md'),
    (Join-Path $lane 'source\id-ID\units\unit-005-lecture-005.md'),
    (Join-Path $lane 'source\id-ID\units\unit-006-lecture-006.md'),
    (Join-Path $lane 'source\id-ID\units\unit-007-lecture-007.md'),
    (Join-Path $lane 'source\id-ID\units\unit-008-lecture-008.md'),
    (Join-Path $lane 'source\id-ID\units\unit-009-lecture-009.md'),
    (Join-Path $lane 'source\id-ID\units\unit-010-lecture-010.md'),
    (Join-Path $lane 'source\id-ID\units\unit-011-lecture-011.md'),
    (Join-Path $lane 'source\id-ID\units\unit-012-lecture-012.md'),
    (Join-Path $lane 'source\id-ID\units\unit-013-lecture-013.md')
)
$baseCss = Join-Path $lane 'source\id-ID\styles\reader.css'
$cumulativeCss = Join-Path $lane 'source\id-ID\styles\reader-cumulative.css'

$htmlDir = Join-Path $lane 'output\html\units-001-013'
$pdfDir = Join-Path $lane 'output\pdf'
$checkDir = Join-Path $lane 'tmp\pdfs\units-001-013-build'
$html = Join-Path $htmlDir 'index.html'
$pdf = Join-Path $pdfDir 'topologi-aljabar-unit-001-013-id.pdf'
$manifestPath = Join-Path $lane 'output\ARTIFACT_MANIFEST_UNITS_001_013.csv'

$frozen = @{
    $sources[0] = @(16179, 'c80b51c22a2fa7ea116201028b78d5f8d708ef4d8355d34092ac7a9c88415e15')
    $sources[1] = @(25090, '4d2acc43557db9b3c419ee177545d285b9fcf50b2aa2dd3b2c6c44182f3a6a01')
    $sources[2] = @(25822, '993e5941895a9b6f4b197b4c236f5a4990f6ae621e2bb7911353b28a5e1abffd')
    $sources[3] = @(24582, '826fcb368275cdad02f72a5cec951fc8466ba68b09ca0139d72c81a4c5591fea')
    $sources[4] = @(22662, '7333a7b7a92b9618016412abb5c9b2b2a398538f690d0109d4282289a0719852')
    $sources[5] = @(32106, '3cb182fdf183bd67e45a898228b995a44d4638e808fdfbe6ea6d6a2a2b889e33')
    $sources[6] = @(22107, '556cea5445e1b0a51f86f1c0ea0e80c4e00a17d365d95fa530f063cc24856569')
    $sources[7] = @(28466, '8369e74c80e391d73575bbcb7844d3bfa62dd771dbca6258eed02360b20529cc')
    $sources[8] = @(25524, '16da25dea2f8ac5415b02738663046fb619c27e685042a734059e3150ed5ff18')
    $sources[9] = @(26432, 'e1c6ef961ae2266db86baec6d701dd659a1bf78bdd3601cf5b1c6515bc7d0310')
    $sources[10] = @(28465, '1cdbe0cae239a4e60a72f25c8814c2e3b5ec26b9119da03624bda7f3ff1ae127')
    $sources[11] = @(32850, '429831df4a5600c59351516915fb787cd73402d8c11c411869210dbf8aaa7ada')
    $sources[12] = @(41196, '0aa68cb4ed31862d32aeff5a7106b4ac29c13cbc202f7dbc8381fc7cd31418c0')
    $baseCss = @(1297, 'e5184827600116bc54e28df6822c5a98691d5edf88b7b102443b56024733cbe5')
    $cumulativeCss = @(203, 'b0012d9f93e603997d48d49705ec9ccae2d3cd2d062b8b9f8717e908df1f5344')
    (Join-Path $lane 'output\html\units-001-005\index.html') = @(610594, '8d3accf480101565409909c05f987f44b73f1c98889128e2f5074a4e049f48f3')
    (Join-Path $lane 'output\pdf\topologi-aljabar-unit-001-005-id.pdf') = @(589065, 'd6929434a9bc7ae78fb71fc060e9cc54dce85d37e4997ffe042ccbab982e64e2')
    (Join-Path $lane 'output\ARTIFACT_MANIFEST_UNITS_001_005.csv') = @(247, '2910fd87871675730aea7ca33e636a70d330d0f81183e887bad74ea1fd2d5190')
    (Join-Path $lane 'qa\UNITS_001_005_QA.json') = @(4768, 'ffb6703e4fe2ebc1c7733dc4f87a32c64c53cbe3ebf326d65a8d2da94765635a')
    (Join-Path $lane 'qa\UNITS_001_005_VISUAL_QA.md') = @(2877, 'ed8249702d8335b01dc40925af1d5b071fa18d2eef9fe628a5535bd9404fbcdd')
    (Join-Path $lane 'qa\units-001-005-extracted.txt') = @(128786, '83aca1060966c7ca7a7852630c27926754f0d893749aeb80888bbfd00f56a725')
    (Join-Path $lane 'qa\UNIT_006_INDEPENDENT_REVIEW.md') = @(1783, '5dd3868192a85e3e60562f42ec7d7b792e0e58811719ecc97207ed2bdc5de4bf')
    (Join-Path $lane 'qa\UNIT_007_INDEPENDENT_REVIEW.md') = @(1761, '87c5129cd7d367893860b150c72948de1d196d7cbefe04d53f7a4efecf921f87')
    (Join-Path $lane 'output\html\units-001-007\index.html') = @(899803, '55135048eafe0f097c45936add885e008392eefdf475270fea37adf6a2a7b7bb')
    (Join-Path $lane 'output\pdf\topologi-aljabar-unit-001-007-id.pdf') = @(702470, '3764b75ecfb9200e25a165db1f0f97a680384378e2a9a22e129aab57dd860d93')
    (Join-Path $lane 'output\ARTIFACT_MANIFEST_UNITS_001_007.csv') = @(247, '7b279f0413892f0ddedce636b3a272884bb7bfa01410bf33a6ce34c0c34db2f9')
    (Join-Path $lane 'qa\UNITS_001_007_QA.json') = @(7384, '2982a9465428eff97e6047bffdadba422b2dc0406e34750f632bfe148ed67617')
    (Join-Path $lane 'qa\UNITS_001_007_VISUAL_QA.md') = @(3259, '63a4b4545213a7aec1c556a3852b818ba2f207b10cac7e80c62330709604176f')
    (Join-Path $lane 'qa\units-001-007-extracted.txt') = @(190424, 'f6839e7eb7f25c8518ec3fc2e2372b82b1f1387b48402899ff8bc40ce153c8dc')
    (Join-Path $lane 'qa\UNIT_008_INDEPENDENT_REVIEW.md') = @(2191, '6960e19949642723dcbfd6ff5bfe105fe4e2789f5989787c041c7f41bdfdac3f')
    (Join-Path $lane 'qa\UNIT_009_INDEPENDENT_REVIEW.md') = @(2147, 'af91c517608c454466d6371db479385ddb1b4c65ecba2f05ca9ec7b26b49cbe6')
    (Join-Path $lane 'qa\UNIT_010_INDEPENDENT_REVIEW.md') = @(2683, '236123c6c1ad15773a1da7f36887a2ebed93298f019db80f79dfa9bcdac100fd')
    (Join-Path $lane 'output\html\units-001-010\index.html') = @(1318415, 'e228ac1422b2742d873feffd5b236fe9c1329d0bdb5da0e8deffe5e770361088')
    (Join-Path $lane 'output\pdf\topologi-aljabar-unit-001-010-id.pdf') = @(862913, 'd0f739aedf3da5f317cf99a1a0dcace1f89b8c802f1dedc42c7ac0c63375c7c1')
    (Join-Path $lane 'output\ARTIFACT_MANIFEST_UNITS_001_010.csv') = @(248, '5bcf82984e3f2848f5471876401e48948639d6ca144e0915d99c86c20fc39d92')
    (Join-Path $lane 'qa\UNITS_001_010_QA.json') = @(9808, '4189663021e6bd7e8822198a79bb3d7c59c7e0cca777054fbc370e77a300da5c')
    (Join-Path $lane 'qa\UNITS_001_010_VISUAL_QA.md') = @(2471, '439099f8c865125864444f9cfd1f60b961274ba0bc6f9bb29c562ee30fab132b')
    (Join-Path $lane 'qa\units-001-010-extracted.txt') = @(280664, '4932889b582a3ccd9816db4b8008791d5fbdc4b044da6f5d1985a87b6ce10642')
    (Join-Path $lane 'qa\UNIT_011_INDEPENDENT_REVIEW.md') = @(3351, 'de0766d41ba901405881d8078830d74420f2b1012ef24ace8d3f481135cd5b25')
    (Join-Path $lane 'qa\UNIT_012_INDEPENDENT_REVIEW.md') = @(3374, '6ea34c30edfa208cc7e37a17f43ef4bf62b21ff4db222e534c97e027232e0ce7')
    (Join-Path $lane 'qa\UNIT_013_INDEPENDENT_REVIEW.md') = @(6665, '5903c7da7f57d5db15a2d94807860a816d15e7d3cb7b020a8a3ddcbb0df45c21')
}

foreach ($path in $frozen.Keys) {
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
        throw "Missing frozen input: $path"
    }
    $expected = $frozen[$path]
    $item = Get-Item -LiteralPath $path
    $digest = (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($item.Length -ne $expected[0] -or $digest -ne $expected[1]) {
        throw "Frozen-byte mismatch: $path"
    }
}

$pandoc = (Get-Command pandoc -ErrorAction Stop).Source
$versionLine = (& $pandoc --version | Select-Object -First 1)
if ($versionLine -ne 'pandoc 3.9.0.2') {
    throw "Expected pandoc 3.9.0.2; found: $versionLine"
}

foreach ($dir in @($htmlDir, $pdfDir, $checkDir)) {
    New-Item -ItemType Directory -Path $dir -Force | Out-Null
}

function Get-MarkdownBody([string]$path) {
    $text = [IO.File]::ReadAllText($path).Replace("`r`n", "`n")
    if (-not $text.StartsWith("---`n")) {
        throw "Missing YAML front matter: $path"
    }
    $end = $text.IndexOf("`n---`n", 4, [StringComparison]::Ordinal)
    if ($end -lt 0) {
        throw "Unclosed YAML front matter: $path"
    }
    return $text.Substring($end + 5).TrimStart("`n")
}

$assembled = Join-Path $checkDir 'reader-units-001-013.md'
$header = @'
---
title: "Topologi Aljabar - Unit 1-13"
subtitle: "Ruang Topologis, Homotopi, Ruang Penutup, Grupoid Fundamental, Seifert--van Kampen, dan Kompleks Presentasi"
author:
  - "David Michael Roberts (materi sumber)"
  - "Edisi Bahasa Indonesia dengan pendamping penguasaan"
date: "22 Agustus 2026"
lang: id-ID
rights: "Materi adaptasi dan materi pendamping: CC BY 4.0; lihat atribusi pada setiap unit."
---

'@
$parts = foreach ($source in $sources) {
    (Get-MarkdownBody $source).TrimEnd("`n")
}
$payload = $header.Replace("`r`n", "`n") + ($parts -join "`n`n") + "`n"
[IO.File]::WriteAllText($assembled, $payload, [Text.UTF8Encoding]::new($false))

# New-boundary-only semantic styles complete the visual grammar without
# changing any previously published stylesheet or artifact.
$semanticCss = Join-Path $checkDir 'semantic-cumulative.css'
$semanticRules = @'
*,
*::before,
*::after {
  box-sizing: border-box;
}

a,
code {
  overflow-wrap: anywhere;
}

.theorem,
.corollary,
.fact {
  margin: 1.25rem 0;
  padding: 0.8rem 1rem;
  border-left: 0.3rem solid #315f8c;
  background: #f3f7fc;
}

.remark {
  margin: 1.25rem 0;
  padding: 0.8rem 1rem;
  border-left: 0.3rem solid #8a6a2f;
  background: #fffaf0;
}

.figure {
  margin: 1.25rem 0;
  padding: 0.8rem 1rem;
  border-left: 0.3rem solid #5d477a;
  background: #f8f5fc;
}

.boundary {
  margin: 1.25rem 0;
  padding: 0.8rem 1rem;
  border: 0.12rem solid #8a6a2f;
  background: #fffdf7;
}

@media (prefers-color-scheme: dark) {
  .theorem,
  .corollary,
  .fact,
  .remark,
  .figure,
  .boundary {
    background: #20242a;
  }
}
'@
[IO.File]::WriteAllText($semanticCss, $semanticRules.Replace("`r`n", "`n"), [Text.UTF8Encoding]::new($false))

$env:SOURCE_DATE_EPOCH = '1787356800'
$env:FORCE_SOURCE_DATE = '1'

$common = @(
    $assembled,
    '--from=markdown+fenced_divs+tex_math_dollars',
    '--standalone',
    '--toc',
    '--number-sections',
    '--metadata=lang:id-ID',
    '--metadata=pagetitle:Topologi Aljabar - Unit 1-13',
    '--strip-comments'
)

$htmlA = Join-Path $checkDir 'units-001-013-a.html'
$htmlB = Join-Path $checkDir 'units-001-013-b.html'
$htmlArgs = @('--to=html5', '--mathml', '--section-divs', "--css=$baseCss", "--css=$cumulativeCss", "--css=$semanticCss", '--embed-resources')
& $pandoc @common @htmlArgs "--output=$htmlA"
if ($LASTEXITCODE -ne 0) { throw "Pandoc HTML build A failed with exit $LASTEXITCODE" }
& $pandoc @common @htmlArgs "--output=$htmlB"
if ($LASTEXITCODE -ne 0) { throw "Pandoc HTML build B failed with exit $LASTEXITCODE" }
$htmlHashA = (Get-FileHash -LiteralPath $htmlA -Algorithm SHA256).Hash.ToLowerInvariant()
$htmlHashB = (Get-FileHash -LiteralPath $htmlB -Algorithm SHA256).Hash.ToLowerInvariant()
if ($htmlHashA -ne $htmlHashB) {
    throw "HTML reproducibility failure: $htmlHashA != $htmlHashB"
}
Copy-Item -LiteralPath $htmlA -Destination $html -Force

# TeX reads a bracketed first array cell immediately following `\\` as the
# optional vertical-space argument of the row break.  Keep the canonical
# Markdown untouched and add an empty TeX group only in the transient PDF
# assembly before bracket-led mathematical lines (Markdown links are excluded).
$pdfAssembled = Join-Path $checkDir 'reader-units-001-013-pdf.md'
$pdfLines = foreach ($line in ($payload -split "`n", 0, 'SimpleMatch')) {
    if ($line.StartsWith('[') -and $line -notmatch '^\[[^]]+\]\(') {
        '{}'+$line
    }
    else {
        $line
    }
}
[IO.File]::WriteAllText(
    $pdfAssembled,
    (($pdfLines -join "`n").TrimEnd("`n") + "`n"),
    [Text.UTF8Encoding]::new($false)
)
$pdfCommon = @($common)
$pdfCommon[0] = $pdfAssembled

$pdfA = Join-Path $checkDir 'units-001-013-a.pdf'
$pdfB = Join-Path $checkDir 'units-001-013-b.pdf'
$pdfHeader = Join-Path $checkDir 'reader-units-001-013-header.tex'
[IO.File]::WriteAllText(
    $pdfHeader,
    "\providecommand{\sslash}{/\mkern-6mu/}`n",
    [Text.UTF8Encoding]::new($false)
)
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
if ($pdfHashA -ne $pdfHashB) {
    throw "PDF reproducibility failure: $pdfHashA != $pdfHashB"
}
Copy-Item -LiteralPath $pdfA -Destination $pdf -Force

$rows = foreach ($artifact in @($html, $pdf)) {
    $item = Get-Item -LiteralPath $artifact
    $relative = [IO.Path]::GetRelativePath($lane, $item.FullName).Replace('\', '/')
    $hash = (Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
    "$relative,$($item.Length),$hash"
}
$manifest = "path,bytes,sha256`n" + (($rows | Sort-Object) -join "`n") + "`n"
[IO.File]::WriteAllText($manifestPath, $manifest, [Text.UTF8Encoding]::new($false))

Remove-Item -LiteralPath $htmlA, $htmlB, $pdfA, $pdfB, $assembled, $pdfAssembled, $semanticCss, $pdfHeader -Force
Remove-Item -LiteralPath $checkDir -Force

[pscustomobject]@{
    html = $html
    html_sha256 = $htmlHashA
    pdf = $pdf
    pdf_sha256 = $pdfHashA
    pandoc = $versionLine
    source_date_epoch = $env:SOURCE_DATE_EPOCH
}
