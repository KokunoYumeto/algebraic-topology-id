[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$lane = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$unit1 = Join-Path $lane 'source\id-ID\reader-unit-001.md'
$unit2 = Join-Path $lane 'source\id-ID\units\unit-002-lecture-002.md'
$baseCss = Join-Path $lane 'source\id-ID\styles\reader.css'
$cumulativeCss = Join-Path $lane 'source\id-ID\styles\reader-cumulative.css'
$unit1Html = Join-Path $lane 'output\html\index.html'
$unit1Pdf = Join-Path $lane 'output\pdf\topologi-aljabar-unit-001-id.pdf'
$htmlDir = Join-Path $lane 'output\html\units-001-002'
$pdfDir = Join-Path $lane 'output\pdf'
$checkDir = Join-Path $lane 'tmp\pdfs\units-001-002-build'

$frozen = @{
    $unit1 = @(16179, 'c80b51c22a2fa7ea116201028b78d5f8d708ef4d8355d34092ac7a9c88415e15')
    $unit2 = @(25090, '4d2acc43557db9b3c419ee177545d285b9fcf50b2aa2dd3b2c6c44182f3a6a01')
    $baseCss = @(1297, 'e5184827600116bc54e28df6822c5a98691d5edf88b7b102443b56024733cbe5')
    $unit1Html = @(85580, '5cc4a29f2c29b274328b574d6698a51d75af0939f9959937db8d679c38ad51b8')
    $unit1Pdf = @(321743, '6f71546a616c02ef81f8747ecfce3875784842065fc131cc82e5060b066a59c9')
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
if (-not (Test-Path -LiteralPath $cumulativeCss -PathType Leaf)) {
    throw "Missing cumulative CSS: $cumulativeCss"
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

$assembled = Join-Path $checkDir 'reader-units-001-002.md'
$header = @'
---
title: "Topologi Aljabar"
subtitle: "Unit 1–2 — Ruang Topologis, Perekatan, dan Keterhubungan"
author:
  - "David Michael Roberts (materi sumber)"
  - "Edisi Bahasa Indonesia dengan pendamping penguasaan"
date: "21 Agustus 2026"
lang: id-ID
rights: "Materi adaptasi dan materi pendamping: CC BY 4.0; lihat atribusi pada setiap unit."
---

'@
$payload = $header.Replace("`r`n", "`n") +
    (Get-MarkdownBody $unit1).TrimEnd("`n") + "`n`n" +
    (Get-MarkdownBody $unit2).TrimEnd("`n") + "`n"
[IO.File]::WriteAllText($assembled, $payload, [Text.UTF8Encoding]::new($false))

$env:SOURCE_DATE_EPOCH = '1787270400'
$env:FORCE_SOURCE_DATE = '1'

$common = @(
    $assembled,
    '--from=markdown+fenced_divs+tex_math_dollars',
    '--standalone',
    '--toc',
    '--number-sections',
    '--metadata=lang:id-ID',
    '--metadata=pagetitle:Topologi Aljabar — Unit 1–2',
    '--strip-comments'
)

$html = Join-Path $htmlDir 'index.html'
& $pandoc @common '--to=html5' '--mathml' '--section-divs' "--css=$baseCss" "--css=$cumulativeCss" '--embed-resources' "--output=$html"
if ($LASTEXITCODE -ne 0) {
    throw "Pandoc HTML build failed with exit $LASTEXITCODE"
}

$pdfA = Join-Path $checkDir 'units-001-002-a.pdf'
$pdfB = Join-Path $checkDir 'units-001-002-b.pdf'
$pdfArgs = @(
    '--pdf-engine=pdflatex',
    '--variable=papersize:a4',
    '--variable=geometry:margin=23mm',
    '--variable=fontsize:11pt',
    '--variable=colorlinks:true',
    '--variable=linkcolor:blue'
)

& $pandoc @common @pdfArgs "--output=$pdfA"
if ($LASTEXITCODE -ne 0) {
    throw "Pandoc PDF build A failed with exit $LASTEXITCODE"
}
& $pandoc @common @pdfArgs "--output=$pdfB"
if ($LASTEXITCODE -ne 0) {
    throw "Pandoc PDF build B failed with exit $LASTEXITCODE"
}

$hashA = (Get-FileHash -LiteralPath $pdfA -Algorithm SHA256).Hash.ToLowerInvariant()
$hashB = (Get-FileHash -LiteralPath $pdfB -Algorithm SHA256).Hash.ToLowerInvariant()
if ($hashA -ne $hashB) {
    throw "PDF reproducibility failure: $hashA != $hashB"
}

$pdf = Join-Path $pdfDir 'topologi-aljabar-unit-001-002-id.pdf'
Copy-Item -LiteralPath $pdfA -Destination $pdf -Force

$rows = foreach ($artifact in @($html, $pdf)) {
    $item = Get-Item -LiteralPath $artifact
    $relative = [IO.Path]::GetRelativePath($lane, $item.FullName).Replace('\', '/')
    $hash = (Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
    "$relative,$($item.Length),$hash"
}
$manifest = "path,bytes,sha256`n" + (($rows | Sort-Object) -join "`n") + "`n"
[IO.File]::WriteAllText((Join-Path $lane 'output\ARTIFACT_MANIFEST_UNITS_001_002.csv'), $manifest, [Text.UTF8Encoding]::new($false))

Remove-Item -LiteralPath $pdfA, $pdfB, $assembled -Force
Remove-Item -LiteralPath $checkDir -Force

[pscustomobject]@{
    html = $html
    pdf = $pdf
    pdf_sha256 = $hashA
    pandoc = $versionLine
    source_date_epoch = $env:SOURCE_DATE_EPOCH
}
