[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# Boundary builder for the first twenty Roberts lectures.  The 001–019
# builder remains frozen and is invoked as a fail-closed baseline; this file
# owns only the new cumulative output paths and the Unit 020 gate.
$lane = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$legacyBuilder = Join-Path $PSScriptRoot 'build-units-001-019.ps1'
if (-not (Test-Path -LiteralPath $legacyBuilder -PathType Leaf)) {
    throw "Missing frozen baseline builder: $legacyBuilder"
}

$unit020 = Join-Path $lane 'source\id-ID\units\unit-020-lecture-020.md'
$unit020Review = Join-Path $lane 'qa\UNIT_020_INDEPENDENT_REVIEW.md'
$unit020Qa = Join-Path $lane 'qa\UNIT_020_QA.json'

# These values are the reviewed Unit 020 snapshot.  Keep this gate fail
# closed: any later source or review edit must update the identities together.
$unit020ExpectedBytes = 45786
$unit020ExpectedLines = 1425
$unit020ExpectedSha256 = 'ed086dfe2f26951d4a1d1c398ade0224ffbf4bd1a20a985d267ecd97bbd228d3'
$unit020ExpectedStableIds = 73
$unit020ExpectedBlockSignature = 'boundary=1,definition=2,example=8,exercise=10,figure=7,lemma=2,proof=2,remark=4'
$unit020ReviewBytes = 2663
$unit020ReviewSha256 = '2599d076e43ea8d826f3bfc98a68c9ec9eee3c1a1ca505cc9e53f5d4a7bbae3f'

if (
    $unit020ExpectedBytes -le 0 -or $unit020ExpectedLines -le 0 -or
    $unit020ExpectedSha256 -notmatch '^[0-9a-f]{64}$' -or
    $unit020ExpectedStableIds -le 0 -or
    $unit020ExpectedBlockSignature -notmatch '^[a-z]+=[0-9]+(,[a-z]+=[0-9]+)*$' -or
    $unit020ReviewBytes -le 0 -or $unit020ReviewSha256 -notmatch '^[0-9a-f]{64}$'
) {
    throw 'Units 001-020 build is locked: freeze Unit 020 and its independent review first.'
}

foreach ($path in @($unit020, $unit020Review, $unit020Qa)) {
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
        throw "Missing Unit 020 gate input: $path"
    }
}
$reviewItem = Get-Item -LiteralPath $unit020Review
$reviewHash = (Get-FileHash -LiteralPath $unit020Review -Algorithm SHA256).Hash.ToLowerInvariant()
if ($reviewItem.Length -ne $unit020ReviewBytes -or $reviewHash -ne $unit020ReviewSha256) {
    throw "Unit 020 independent-review identity mismatch: $unit020Review"
}
$reviewText = [IO.File]::ReadAllText($unit020Review)
if ($reviewText -notmatch '(?m)^- P1: 0\s*$' -or
    $reviewText -notmatch '(?m)^- P2: 0\s*$' -or
    $reviewText -notmatch '(?m)^- P3: 0\s*$' -or
    $reviewText -notmatch '45,786 bytes, 1,425 LF lines') {
    throw 'Unit 020 independent review is not a zero-finding final snapshot.'
}
$qaText = [IO.File]::ReadAllText($unit020Qa)
if ($qaText -notmatch '"status"\s*:\s*"PASS"' -or
    $qaText -notmatch '"model_provenance"\s*:\s*"OpenAI Codex gpt-5\.6-sol, Ultra"') {
    throw 'Unit 020 QA receipt is not a passing, model-attributed receipt.'
}

$blockKinds = 'boundary|corollary|definition|example|exercise|fact|figure|lemma|note|proof|proposition|question|remark|theorem'
function Get-BlockSignature([string]$text) {
    $counts = @{}
    foreach ($match in [regex]::Matches($text, "(?m)^::: \{\.(?<kind>$blockKinds)\s+#o012-")) {
        $kind = $match.Groups['kind'].Value
        if ($counts.ContainsKey($kind)) { $counts[$kind] += 1 } else { $counts[$kind] = 1 }
    }
    return (($counts.GetEnumerator() | Sort-Object Name | ForEach-Object { "$($_.Name)=$($_.Value)" }) -join ',')
}
function Get-MarkdownBody([string]$path) {
    $bytes = [IO.File]::ReadAllBytes($path)
    if ($bytes -contains 13) { throw "CR byte in LF-frozen source: $path" }
    $text = [Text.Encoding]::UTF8.GetString($bytes)
    if (-not $text.StartsWith("---`n")) { throw "Missing YAML front matter: $path" }
    $end = $text.IndexOf("`n---`n", 4, [StringComparison]::Ordinal)
    if ($end -lt 0) { throw "Unclosed YAML front matter: $path" }
    return $text.Substring($end + 5).TrimStart("`n")
}

$unit020Item = Get-Item -LiteralPath $unit020
$unit020Text = [IO.File]::ReadAllText($unit020)
$unit020Hash = (Get-FileHash -LiteralPath $unit020 -Algorithm SHA256).Hash.ToLowerInvariant()
if ($unit020Item.Length -ne $unit020ExpectedBytes -or $unit020Hash -ne $unit020ExpectedSha256) {
    throw "Unit 020 frozen-byte mismatch: $unit020"
}
if (-not $unit020Text.EndsWith("`n")) { throw 'Unit 020 is missing its final LF.' }
$unit020Lines = ([regex]::Matches($unit020Text, "`n")).Count
if ($unit020Lines -ne $unit020ExpectedLines) { throw "Unit 020 line-count mismatch: $unit020Lines" }
foreach ($marker in @('TODO', 'TBD', 'FILL_AFTER', 'C:\Users\', 'C:/Users/', 'github_pat_', 'ghp_', 'sk-proj_')) {
    if ($unit020Text.Contains($marker)) { throw "Private or placeholder marker in Unit 020: $marker" }
}
if (([regex]::Matches($unit020Text, '(?m)^::: \{')).Count -ne ([regex]::Matches($unit020Text, '(?m)^:::\s*$')).Count) {
    throw 'Unit 020 has unbalanced fenced divs.'
}
if (([regex]::Matches($unit020Text, '\$\$')).Count % 2 -ne 0) { throw 'Unit 020 has unbalanced display math.' }
if ([regex]::IsMatch($unit020Text, '(?m)(?<!\$)\\square\$')) { throw 'Unit 020 has a bare \\square$ proof delimiter.' }
$unit020Ids = [regex]::Matches($unit020Text, '#(o012-[a-z0-9-]+)(?=[}\s])') | ForEach-Object { $_.Groups[1].Value }
if ($unit020Ids.Count -ne $unit020ExpectedStableIds -or @($unit020Ids | Sort-Object -Unique).Count -ne $unit020ExpectedStableIds) {
    throw 'Unit 020 stable-ID census mismatch.'
}
$unit020Signature = Get-BlockSignature $unit020Text
if ($unit020Signature -ne $unit020ExpectedBlockSignature) { throw "Unit 020 semantic-block mismatch: $unit020Signature" }
[void](Get-MarkdownBody $unit020)

$sources = @((Join-Path $lane 'source\id-ID\reader-unit-001.md')) + @(
    2..20 | ForEach-Object { Join-Path $lane ("source\id-ID\units\unit-{0:000}-lecture-{0:000}.md" -f $_) }
)
foreach ($source in $sources) {
    if (-not (Test-Path -LiteralPath $source -PathType Leaf)) { throw "Missing cumulative source: $source" }
    [void](Get-MarkdownBody $source)
}

# Do not spend a 001–019 build if the new Unit 020 gate is stale.  Once all
# Unit 020 identities and exact source paths pass, invoke the frozen baseline
# unchanged before assembling the new cumulative reader.
& $legacyBuilder | Out-Null

$baseCss = Join-Path $lane 'source\id-ID\styles\reader.css'
$cumulativeCss = Join-Path $lane 'source\id-ID\styles\reader-cumulative.css'
$htmlDir = Join-Path $lane 'output\html\units-001-020'
$pdfDir = Join-Path $lane 'output\pdf'
$checkDir = Join-Path $lane 'tmp\pdfs\units-001-020-build'
$html = Join-Path $htmlDir 'index.html'
$pdf = Join-Path $pdfDir 'topologi-aljabar-unit-001-020-id.pdf'
$manifestPath = Join-Path $lane 'output\ARTIFACT_MANIFEST_UNITS_001_020.csv'

$pandoc = (Get-Command pandoc -ErrorAction Stop).Source
$versionLine = (& $pandoc --version | Select-Object -First 1)
if ($versionLine -ne 'pandoc 3.9.0.2') { throw "Expected pandoc 3.9.0.2; found: $versionLine" }
foreach ($dir in @($htmlDir, $pdfDir, $checkDir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }

$assembled = Join-Path $checkDir 'reader-units-001-020.md'
$header = @'
---
title: "Topologi Aljabar - Unit 1-20"
subtitle: "Homotopi, Ruang Penutup, Grup Fundamental, Teori Klasifikasi, Homotopi Tingkat Tinggi, dan Kohomologi"
author:
  - "David Michael Roberts (materi sumber)"
  - "Edisi Bahasa Indonesia dengan pendamping penguasaan"
date: "23 Agustus 2026"
lang: id-ID
rights: "Materi adaptasi dan materi pendamping: CC BY 4.0; lihat atribusi pada setiap unit."
provenance: "OpenAI Codex gpt-5.6-sol, Ultra; atas arahan pengguna; kredit penulis sumber dan kontributor manusia dipertahankan."
source_authority: "DavidMichaelRoberts/AlgebraicTopology2019@b947ad2e9f9e301bfe24590a9db653bc54fa1a53"
---

'@
$parts = foreach ($source in $sources) { (Get-MarkdownBody $source).TrimEnd("`n") }
$payload = $header.Replace("`r`n", "`n") + ($parts -join "`n`n") + "`n"
[IO.File]::WriteAllText($assembled, $payload, [Text.UTF8Encoding]::new($false))

$semanticCss = Join-Path $checkDir 'semantic-cumulative.css'
$semanticRules = @'
*, *::before, *::after { box-sizing: border-box; }
a, code { overflow-wrap: anywhere; }
.theorem, .corollary, .fact { margin: 1.25rem 0; padding: .8rem 1rem; border-left: .3rem solid #315f8c; background: #f3f7fc; }
.remark { margin: 1.25rem 0; padding: .8rem 1rem; border-left: .3rem solid #8a6a2f; background: #fffaf0; }
.figure { margin: 1.25rem 0; padding: .8rem 1rem; border-left: .3rem solid #5d477a; background: #f8f5fc; }
.boundary { margin: 1.25rem 0; padding: .8rem 1rem; border: .12rem solid #8a6a2f; background: #fffdf7; }
@media (prefers-color-scheme: dark) { .theorem, .corollary, .fact, .remark, .figure, .boundary { background: #20242a; } }
'@
[IO.File]::WriteAllText($semanticCss, $semanticRules.Replace("`r`n", "`n"), [Text.UTF8Encoding]::new($false))

$env:SOURCE_DATE_EPOCH = '1787443200'
$env:FORCE_SOURCE_DATE = '1'
$common = @(
    $assembled,
    '--from=markdown+fenced_divs+tex_math_dollars', '--standalone', '--toc', '--number-sections',
    '--metadata=lang:id-ID', '--metadata=pagetitle:Topologi Aljabar - Unit 1-20',
    '--metadata=provenance:OpenAI Codex gpt-5.6-sol, Ultra',
    '--metadata=source-authority:DavidMichaelRoberts/AlgebraicTopology2019@b947ad2e9f9e301bfe24590a9db653bc54fa1a53',
    '--strip-comments'
)

$htmlA = Join-Path $checkDir 'units-001-020-a.html'; $htmlB = Join-Path $checkDir 'units-001-020-b.html'
$htmlArgs = @('--to=html5', '--mathml', '--section-divs', "--css=$baseCss", "--css=$cumulativeCss", "--css=$semanticCss", '--embed-resources')
& $pandoc @common @htmlArgs "--output=$htmlA"; if ($LASTEXITCODE -ne 0) { throw "Pandoc HTML build A failed with exit $LASTEXITCODE" }
& $pandoc @common @htmlArgs "--output=$htmlB"; if ($LASTEXITCODE -ne 0) { throw "Pandoc HTML build B failed with exit $LASTEXITCODE" }
$htmlHashA = (Get-FileHash -LiteralPath $htmlA -Algorithm SHA256).Hash.ToLowerInvariant(); $htmlHashB = (Get-FileHash -LiteralPath $htmlB -Algorithm SHA256).Hash.ToLowerInvariant()
if ($htmlHashA -ne $htmlHashB) { throw "HTML reproducibility failure: $htmlHashA != $htmlHashB" }
Copy-Item -LiteralPath $htmlA -Destination $html -Force

$pdfAssembled = Join-Path $checkDir 'reader-units-001-020-pdf.md'
$pdfLines = foreach ($line in ($payload -split "`n", 0, 'SimpleMatch')) { if ($line.StartsWith('[') -and $line -notmatch '^\[[^]]+\]\(') { '{}'+$line } else { $line } }
[IO.File]::WriteAllText($pdfAssembled, (($pdfLines -join "`n").TrimEnd("`n") + "`n"), [Text.UTF8Encoding]::new($false))
$pdfCommon = @($common); $pdfCommon[0] = $pdfAssembled
$pdfA = Join-Path $checkDir 'units-001-020-a.pdf'; $pdfB = Join-Path $checkDir 'units-001-020-b.pdf'; $pdfHeader = Join-Path $checkDir 'reader-units-001-020-header.tex'
[IO.File]::WriteAllText($pdfHeader, "\providecommand{\sslash}{/\mkern-6mu/}`n", [Text.UTF8Encoding]::new($false))
$pdfArgs = @('--pdf-engine=pdflatex', "--include-in-header=$pdfHeader", '--variable=papersize:a4', '--variable=geometry:margin=21mm', '--variable=fontsize:11pt', '--variable=colorlinks:true', '--variable=linkcolor:blue')
& $pandoc @pdfCommon @pdfArgs "--output=$pdfA"; if ($LASTEXITCODE -ne 0) { throw "Pandoc PDF build A failed with exit $LASTEXITCODE" }
& $pandoc @pdfCommon @pdfArgs "--output=$pdfB"; if ($LASTEXITCODE -ne 0) { throw "Pandoc PDF build B failed with exit $LASTEXITCODE" }
$pdfHashA = (Get-FileHash -LiteralPath $pdfA -Algorithm SHA256).Hash.ToLowerInvariant(); $pdfHashB = (Get-FileHash -LiteralPath $pdfB -Algorithm SHA256).Hash.ToLowerInvariant()
if ($pdfHashA -ne $pdfHashB) { throw "PDF reproducibility failure: $pdfHashA != $pdfHashB" }
Copy-Item -LiteralPath $pdfA -Destination $pdf -Force

$rows = foreach ($artifact in @($html, $pdf)) {
    $item = Get-Item -LiteralPath $artifact
    $relative = [IO.Path]::GetRelativePath($lane, $item.FullName).Replace('\', '/')
    $hash = (Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
    "$relative,$($item.Length),$hash"
}
[IO.File]::WriteAllText($manifestPath, "path,bytes,sha256`n" + (($rows | Sort-Object) -join "`n") + "`n", [Text.UTF8Encoding]::new($false))

Remove-Item -LiteralPath $htmlA, $htmlB, $pdfA, $pdfB, $assembled, $pdfAssembled, $semanticCss, $pdfHeader -Force
Remove-Item -LiteralPath $checkDir -Force

[pscustomobject]@{
    html = $html; html_sha256 = $htmlHashA
    pdf = $pdf; pdf_sha256 = $pdfHashA
    manifest = $manifestPath
    pandoc = $versionLine; source_date_epoch = $env:SOURCE_DATE_EPOCH
    model_provenance = 'OpenAI Codex gpt-5.6-sol, Ultra'
    source_authority = 'DavidMichaelRoberts/AlgebraicTopology2019@b947ad2e9f9e301bfe24590a9db653bc54fa1a53'
}
