[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$lane = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$source = Join-Path $lane 'source\id-ID\reader-unit-001.md'
$css = Join-Path $lane 'source\id-ID\styles\reader.css'
$htmlDir = Join-Path $lane 'output\html'
$pdfDir = Join-Path $lane 'output\pdf'
$checkDir = Join-Path $lane 'qa\.unit-001-build-check'

foreach ($path in @($source, $css)) {
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
        throw "Missing build input: $path"
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

$env:SOURCE_DATE_EPOCH = '1787270400'
$env:FORCE_SOURCE_DATE = '1'

$common = @(
    $source,
    '--from=markdown+fenced_divs+tex_math_dollars',
    '--standalone',
    '--toc',
    '--number-sections',
    '--metadata=lang:id-ID',
    '--metadata=pagetitle:Topologi Aljabar — Unit 1',
    '--strip-comments'
)

$html = Join-Path $htmlDir 'index.html'
& $pandoc @common '--to=html5' '--mathml' '--section-divs' "--css=$css" '--embed-resources' "--output=$html"
if ($LASTEXITCODE -ne 0) {
    throw "Pandoc HTML build failed with exit $LASTEXITCODE"
}

$pdfA = Join-Path $checkDir 'unit-001-a.pdf'
$pdfB = Join-Path $checkDir 'unit-001-b.pdf'
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

$pdf = Join-Path $pdfDir 'topologi-aljabar-unit-001-id.pdf'
Copy-Item -LiteralPath $pdfA -Destination $pdf -Force
Remove-Item -LiteralPath $pdfA, $pdfB -Force

$rows = foreach ($artifact in @($html, $pdf)) {
    $item = Get-Item -LiteralPath $artifact
    $relative = [IO.Path]::GetRelativePath($lane, $item.FullName).Replace('\', '/')
    $hash = (Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
    "$relative,$($item.Length),$hash"
}
$manifest = "path,bytes,sha256`n" + (($rows | Sort-Object) -join "`n") + "`n"
[IO.File]::WriteAllText((Join-Path $lane 'output\ARTIFACT_MANIFEST.csv'), $manifest, [Text.UTF8Encoding]::new($false))

[pscustomobject]@{
    html = $html
    pdf = $pdf
    pdf_sha256 = $hashA
    pandoc = $versionLine
    source_date_epoch = $env:SOURCE_DATE_EPOCH
}
