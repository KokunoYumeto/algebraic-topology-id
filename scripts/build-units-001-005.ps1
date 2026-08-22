[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$lane = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$unit1 = Join-Path $lane 'source\id-ID\reader-unit-001.md'
$unit2 = Join-Path $lane 'source\id-ID\units\unit-002-lecture-002.md'
$unit3 = Join-Path $lane 'source\id-ID\units\unit-003-lecture-003.md'
$unit4 = Join-Path $lane 'source\id-ID\units\unit-004-lecture-004.md'
$unit5 = Join-Path $lane 'source\id-ID\units\unit-005-lecture-005.md'
$baseCss = Join-Path $lane 'source\id-ID\styles\reader.css'
$cumulativeCss = Join-Path $lane 'source\id-ID\styles\reader-cumulative.css'

$unit1Html = Join-Path $lane 'output\html\index.html'
$unit1Pdf = Join-Path $lane 'output\pdf\topologi-aljabar-unit-001-id.pdf'
$unit1Manifest = Join-Path $lane 'output\ARTIFACT_MANIFEST.csv'
$units12Html = Join-Path $lane 'output\html\units-001-002\index.html'
$units12Pdf = Join-Path $lane 'output\pdf\topologi-aljabar-unit-001-002-id.pdf'
$units12Manifest = Join-Path $lane 'output\ARTIFACT_MANIFEST_UNITS_001_002.csv'
$units123Html = Join-Path $lane 'output\html\units-001-003\index.html'
$units123Pdf = Join-Path $lane 'output\pdf\topologi-aljabar-unit-001-003-id.pdf'
$units123Manifest = Join-Path $lane 'output\ARTIFACT_MANIFEST_UNITS_001_003.csv'
$units1234Html = Join-Path $lane 'output\html\units-001-004\index.html'
$units1234Pdf = Join-Path $lane 'output\pdf\topologi-aljabar-unit-001-004-id.pdf'
$units1234Manifest = Join-Path $lane 'output\ARTIFACT_MANIFEST_UNITS_001_004.csv'

$htmlDir = Join-Path $lane 'output\html\units-001-005'
$pdfDir = Join-Path $lane 'output\pdf'
$checkDir = Join-Path $lane 'tmp\pdfs\units-001-005-build'

# Fail closed until the independent Unit 5 review freezes these values.
$unit5ExpectedBytes = 22662
$unit5ExpectedSha256 = '7333a7b7a92b9618016412abb5c9b2b2a398538f690d0109d4282289a0719852'
if ($unit5ExpectedBytes -le 0 -or $unit5ExpectedSha256 -notmatch '^[0-9a-f]{64}$') {
    throw 'Fill the exact reviewed Unit 5 byte count and SHA-256 before building.'
}

$frozen = @{
    $unit1 = @(16179, 'c80b51c22a2fa7ea116201028b78d5f8d708ef4d8355d34092ac7a9c88415e15')
    $unit2 = @(25090, '4d2acc43557db9b3c419ee177545d285b9fcf50b2aa2dd3b2c6c44182f3a6a01')
    $unit3 = @(25822, '993e5941895a9b6f4b197b4c236f5a4990f6ae621e2bb7911353b28a5e1abffd')
    $unit4 = @(24582, '826fcb368275cdad02f72a5cec951fc8466ba68b09ca0139d72c81a4c5591fea')
    $unit5 = @($unit5ExpectedBytes, $unit5ExpectedSha256)
    $baseCss = @(1297, 'e5184827600116bc54e28df6822c5a98691d5edf88b7b102443b56024733cbe5')
    $cumulativeCss = @(203, 'b0012d9f93e603997d48d49705ec9ccae2d3cd2d062b8b9f8717e908df1f5344')
    $unit1Html = @(85580, '5cc4a29f2c29b274328b574d6698a51d75af0939f9959937db8d679c38ad51b8')
    $unit1Pdf = @(321743, '6f71546a616c02ef81f8747ecfce3875784842065fc131cc82e5060b066a59c9')
    $unit1Manifest = @(228, '13772b2e2400923351225f422effe5f958e1dd8e178b9f6a32207682f791bcc3')
    $units12Html = @(220035, 'd3b5cbfaa3511823821ecf9ba26a4eaec7c84d937417927d11bde3f66abc9f54')
    $units12Pdf = @(395385, '0413c3a3280955cc482a5c0c2d7615b78128dccba3b6b1901dee1bf34d133b8e')
    $units12Manifest = @(247, '93e98f6cbbc60775bb934df5b49141f63d7cd2c76582a26c61d4192ff320d721')
    $units123Html = @(359397, '33281cc46faa3d560c968b657526cd914786c991d1475b5563911a265bd316c1')
    $units123Pdf = @(460320, '2c9bf67e74c94bca9aad0238e910816188a957892a6cf811f7f615e221b4066d')
    $units123Manifest = @(247, '1e211afb4b165435ece5f72a2b4e9b084975db35d111127880255473302f5049')
    $units1234Html = @(494732, '8c8f5e1ad8172a2d97e3931fc3b4f2a3aa7f9e8a709260a27103f7eca0f1357d')
    $units1234Pdf = @(539006, '5e92c4c6ed60bca9f2f4d362d4c48b4f01aa156b330e2adacd1bf88dd7de9e87')
    $units1234Manifest = @(247, '4c8bf407e426feb8db92308c4b28bdbbc0738416a85a13539ef7915e4c1aad83')
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

$assembled = Join-Path $checkDir 'reader-units-001-005.md'
$header = @'
---
title: "Topologi Aljabar - Unit 1-5"
subtitle: "Ruang Topologis, Keterhubungan, Homotopi, Funktor, Ruang Penutup, Tarik Balik, dan Pengangkatan Lintasan"
author:
  - "David Michael Roberts (materi sumber)"
  - "Edisi Bahasa Indonesia dengan pendamping penguasaan"
date: "22 Agustus 2026"
lang: id-ID
rights: "Materi adaptasi dan materi pendamping: CC BY 4.0; lihat atribusi pada setiap unit."
---

'@
$payload = $header.Replace("`r`n", "`n") +
    (Get-MarkdownBody $unit1).TrimEnd("`n") + "`n`n" +
    (Get-MarkdownBody $unit2).TrimEnd("`n") + "`n`n" +
    (Get-MarkdownBody $unit3).TrimEnd("`n") + "`n`n" +
    (Get-MarkdownBody $unit4).TrimEnd("`n") + "`n`n" +
    (Get-MarkdownBody $unit5).TrimEnd("`n") + "`n"
[IO.File]::WriteAllText($assembled, $payload, [Text.UTF8Encoding]::new($false))

$env:SOURCE_DATE_EPOCH = '1787356800'
$env:FORCE_SOURCE_DATE = '1'

$common = @(
    $assembled,
    '--from=markdown+fenced_divs+tex_math_dollars',
    '--standalone',
    '--toc',
    '--number-sections',
    '--metadata=lang:id-ID',
    '--metadata=pagetitle:Topologi Aljabar - Unit 1-5',
    '--strip-comments'
)

$html = Join-Path $htmlDir 'index.html'
& $pandoc @common '--to=html5' '--mathml' '--section-divs' "--css=$baseCss" "--css=$cumulativeCss" '--embed-resources' "--output=$html"
if ($LASTEXITCODE -ne 0) {
    throw "Pandoc HTML build failed with exit $LASTEXITCODE"
}

$pdfA = Join-Path $checkDir 'units-001-005-a.pdf'
$pdfB = Join-Path $checkDir 'units-001-005-b.pdf'
$pdfArgs = @(
    '--pdf-engine=pdflatex',
    '--variable=papersize:a4',
    '--variable=geometry:margin=21mm',
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

$pdf = Join-Path $pdfDir 'topologi-aljabar-unit-001-005-id.pdf'
Copy-Item -LiteralPath $pdfA -Destination $pdf -Force

$rows = foreach ($artifact in @($html, $pdf)) {
    $item = Get-Item -LiteralPath $artifact
    $relative = [IO.Path]::GetRelativePath($lane, $item.FullName).Replace('\', '/')
    $hash = (Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
    "$relative,$($item.Length),$hash"
}
$manifest = "path,bytes,sha256`n" + (($rows | Sort-Object) -join "`n") + "`n"
[IO.File]::WriteAllText((Join-Path $lane 'output\ARTIFACT_MANIFEST_UNITS_001_005.csv'), $manifest, [Text.UTF8Encoding]::new($false))

Remove-Item -LiteralPath $pdfA, $pdfB, $assembled -Force
Remove-Item -LiteralPath $checkDir -Force

[pscustomobject]@{
    html = $html
    pdf = $pdf
    pdf_sha256 = $hashA
    pandoc = $versionLine
    source_date_epoch = $env:SOURCE_DATE_EPOCH
}
