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
    (Join-Path $lane 'source\id-ID\units\unit-013-lecture-013.md'),
    (Join-Path $lane 'source\id-ID\units\unit-014-lecture-014.md'),
    (Join-Path $lane 'source\id-ID\units\unit-015-lecture-015.md'),
    (Join-Path $lane 'source\id-ID\units\unit-016-lecture-016.md'),
    (Join-Path $lane 'source\id-ID\units\unit-017-lecture-017.md'),
    (Join-Path $lane 'source\id-ID\units\unit-018-lecture-018.md'),
    (Join-Path $lane 'source\id-ID\units\unit-019-lecture-019.md')
)
$baseCss = Join-Path $lane 'source\id-ID\styles\reader.css'
$cumulativeCss = Join-Path $lane 'source\id-ID\styles\reader-cumulative.css'

$htmlDir = Join-Path $lane 'output\html\units-001-019'
$pdfDir = Join-Path $lane 'output\pdf'
$checkDir = Join-Path $lane 'tmp\pdfs\units-001-019-build'
$html = Join-Path $htmlDir 'index.html'
$pdf = Join-Path $pdfDir 'topologi-aljabar-unit-001-019-id.pdf'
$manifestPath = Join-Path $lane 'output\ARTIFACT_MANIFEST_UNITS_001_019.csv'

# Fail-closed completion gate. Replace all six values only after Unit 019 and
# its independent review are final. Do not copy values from a working draft.
$unit019Bytes = 57277
$unit019Lines = 1865
$unit019Sha256 = 'ba34773d63e4dc70fccdf4fa19fbdc8a397062a4bc359978f3261a70ff64f98c'
$unit019StableIds = 78
$unit019BlockSignature = 'definition=6,example=12,exercise=6,figure=6,lemma=2,proof=1,remark=1'
$unit019ReviewBytes = 2707
$unit019ReviewSha256 = 'd360a17a8a7a5008a80873c4413d92bd9354b6c44275365809be33258c0673a5'

if (
    $unit019Bytes -le 0 -or
    $unit019Lines -le 0 -or
    $unit019Sha256 -notmatch '^[0-9a-f]{64}$' -or
    $unit019StableIds -le 0 -or
    $unit019BlockSignature -notmatch '^[a-z]+=[0-9]+(,[a-z]+=[0-9]+)*$' -or
    $unit019ReviewBytes -le 0 -or
    $unit019ReviewSha256 -notmatch '^[0-9a-f]{64}$'
) {
    throw 'Units 001-019 build is intentionally locked: freeze the final Unit 019 and independent-review identities first.'
}

$sourceExpected = @(
    @(16179, 225, 'dccc7b727695d26d0b425c0eae22db1697cea93e295391fa7685fbca2d011dc7'),
    @(25090, 674, '9aa5063c167cc0b2bc8a5edbc81cb36995606d5073a1afe22db608609ad29377'),
    @(25822, 618, 'f757bc58ea6f0d0dbe37ebdb2e44da7d3814b32052d8e23a39331d66d1f025b2'),
    @(24546, 632, '35aa8adfec6f7652f9a9f21f2c6b6656347309f866689a0939d6f0c517974ea3'),
    @(22662, 663, '9d25dc7cd89c0c9f69841850b03489e742e8dc50c2e68ca405aff593ec128f90'),
    @(32116, 893, '2276a34177100bc14e3e9f96461f6a7ab3bf27a25f652af4cc2d27493f420c8e'),
    @(22107, 749, 'f93659dd290272ad3d526b74565f7bdc7316c366c09f1efaac599abde4cbc59d'),
    @(28468, 930, '4b5c579a1891a99ddff89c458f9d653ec03973e0aaa32839c87be5896ab653a8'),
    @(25524, 939, 'c6076a71d38ab54553a0bf5ed42289063044ebcbeb29689df220081e5621a8a1'),
    @(26448, 934, 'ef76aedb378cb8a3d18a20f672082ee976561a877270082968e7df0a1514a8d5'),
    @(28465, 959, '7acb205dd9f760631f7548208d77470e22cd208849439e2ad2a8eb4b2465b0f8'),
    @(32850, 1024, 'b7ba7cad3d12605628693d57d50a41e06f40a6b7da1109752fe05d870b4b28f0'),
    @(41196, 1306, 'f3827dc052a70930ad31cc6f9b1a745bf8a17bac31b4f9249cd178b06ac302b6'),
    @(28488, 947, 'da6f18b455d76adafd8b9b648ed7c277958eca95c0b7d76a8bd9895d79ec6677'),
    @(27725, 835, 'e9ab0565ae460236a69c77389b76d32405873156fc451be9cf95c3749e7fe9d1'),
    @(33919, 984, '31dfc4c3647f7d6a1d398d2123efe1faa82348428df0180eee2a2358572f9054'),
    @(29933, 952, '47576d7c26a436ba915c276b692e2bc0ead6fae038295fee3a82a50426ed9a96'),
    @(44415, 1663, '9d0564f6a074441332e42755d46d9a0e858189a5ff4d8b5be52b1def12532598'),
    @($unit019Bytes, $unit019Lines, $unit019Sha256)
)
$expectedStableIds = @(29, 41, 39, 33, 30, 28, 24, 26, 30, 26, 39, 37, 44, 38, 34, 33, 34, 67, $unit019StableIds)
$expectedBlockSignatures = @(
    'definition=6,example=7,exercise=2,lemma=1,note=2,proof=1,proposition=1',
    'definition=3,example=8,exercise=7,lemma=3,proof=1,question=1',
    'definition=6,example=4,exercise=5,lemma=2,proof=5,proposition=3',
    'definition=4,example=5,exercise=4,lemma=1,proof=2,proposition=3,question=1',
    'corollary=3,definition=1,example=1,exercise=4,lemma=1,proof=5,proposition=2,theorem=1',
    'definition=2,example=3,exercise=4,lemma=2,proof=2,remark=1,theorem=2',
    'corollary=1,definition=1,example=3,exercise=4,lemma=1,proof=1,proposition=2',
    'definition=3,example=3,exercise=5,lemma=1,proof=1,proposition=2',
    'corollary=4,example=1,exercise=5,proof=5,proposition=1,theorem=2',
    'corollary=2,definition=1,example=2,exercise=5,figure=1,proof=3,theorem=1',
    'definition=3,example=5,exercise=3,figure=11,proof=1,remark=1,theorem=1',
    'boundary=1,corollary=1,definition=1,example=2,exercise=4,figure=7,lemma=2,proof=5,theorem=1',
    'boundary=1,definition=1,example=4,exercise=8,fact=1,figure=13,remark=1',
    'boundary=2,definition=1,example=1,exercise=8,figure=3,lemma=3,proof=1,proposition=1,question=1,remark=1',
    'example=2,exercise=7,lemma=2,note=1,proof=2,question=1,remark=2',
    'corollary=1,definition=1,exercise=6,lemma=1,note=1,proof=4,proposition=3',
    'corollary=1,definition=1,example=1,exercise=6,lemma=2,proof=5,proposition=1,theorem=1',
    'definition=2,example=10,exercise=6,lemma=2,proof=4,proposition=2,remark=6,theorem=1',
    $unit019BlockSignature
)

$frozen = @{
    $baseCss = @(1297, 'e5184827600116bc54e28df6822c5a98691d5edf88b7b102443b56024733cbe5')
    $cumulativeCss = @(203, 'b0012d9f93e603997d48d49705ec9ccae2d3cd2d062b8b9f8717e908df1f5344')
    (Join-Path $lane 'output\html\units-001-013\index.html') = @(1824804, 'be1473ab5cb8eff26341e554179661775a12cec5784a8ebf3f9c2f3f0633cb71')
    (Join-Path $lane 'output\pdf\topologi-aljabar-unit-001-013-id.pdf') = @(1071382, '14775535f773735db5886195980f39e417aaea24998927956a81b55b0ef77c68')
    (Join-Path $lane 'output\ARTIFACT_MANIFEST_UNITS_001_013.csv') = @(249, '6b55446a4f0a951329c29ec33b0ca586c749b9301dd4bd8ad4dd94f1c91d74de')
    (Join-Path $lane 'qa\UNITS_001_013_QA.json') = @(9069, 'cb2413e8131743457a0685a57cf519c769e5593e9ec8d904f6160f9e0519983d')
    (Join-Path $lane 'qa\UNITS_001_013_VISUAL_QA.md') = @(2139, '78e151b05d3efdce4dbfd346962dece5d7da4a559ab1101ac4bd8e02bff59f48')
    (Join-Path $lane 'qa\units-001-013-extracted.txt') = @(395766, 'd94869df978e2538c79b8859cb38c8cbf859420cde68326a35546c973c787497')
    (Join-Path $lane 'qa\INDONESIAN_TERMINOLOGY_QA_2026-08-22.md') = @(4852, '62bdf56464647d1d9d9f76c9a8245ecf243968b92962ef45a86462f255f39299')
    (Join-Path $lane 'qa\INDONESIAN_TERMINOLOGY_QA_2026-08-22.json') = @(18244, '54317e2c8591af9e3f668aa873281ae2c08275c7dc0dc2f1b66a6e314f7152a3')
    (Join-Path $lane 'qa\UNIT_014_INDEPENDENT_REVIEW.md') = @(9725, '43a409f8f127fe9425d14bc8279a594e4ea1f604da3db4f99316aa7c17c3969d')
    (Join-Path $lane 'qa\UNIT_015_INDEPENDENT_REVIEW.md') = @(4392, '9776c911f5d4f4cd7027375ac29514ca2722f28877d27e79753fabf61876dc90')
    (Join-Path $lane 'qa\UNIT_016_INDEPENDENT_REVIEW.md') = @(8485, '335f8ef19f35ba063ad526850d01eec377dc89eb7b697831b8741659a86444c6')
    (Join-Path $lane 'qa\UNIT_017_INDEPENDENT_REVIEW.md') = @(9903, 'b4885ed709311275a9ae32fedbefe7bf86c72203caafa92de3b557f17c1fc625')
    (Join-Path $lane 'qa\UNIT_018_INDEPENDENT_REVIEW.md') = @(3054, '146a011168c49ef922b71e8278b1631d430aa3b2134d150219d2fef0a5437cf2')
    (Join-Path $lane 'qa\UNIT_019_INDEPENDENT_REVIEW.md') = @($unit019ReviewBytes, $unit019ReviewSha256)
}
for ($index = 0; $index -lt $sources.Count; $index++) {
    $frozen[$sources[$index]] = @($sourceExpected[$index][0], $sourceExpected[$index][2])
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

for ($index = 0; $index -lt $sources.Count; $index++) {
    $text = [IO.File]::ReadAllText($sources[$index]).Replace("`r`n", "`n")
    if (-not $text.EndsWith("`n")) { throw "Missing final LF: $($sources[$index])" }
    $actualLines = ([regex]::Matches($text, "`n")).Count
    if ($actualLines -ne $sourceExpected[$index][1]) { throw "Line-count mismatch: $($sources[$index])" }
    foreach ($marker in @('TODO', 'TBD', 'FILL_AFTER', 'C:\Users\', 'C:/Users/', 'github_pat_', 'ghp_', 'sk-proj_')) {
        if ($text.Contains($marker)) { throw "Private or placeholder marker in source $($sources[$index]): $marker" }
    }
    if (([regex]::Matches($text, '(?m)^::: \{')).Count -ne ([regex]::Matches($text, '(?m)^:::\s*$')).Count) {
        throw "Unbalanced fenced divs: $($sources[$index])"
    }
    if (([regex]::Matches($text, '\$\$')).Count % 2 -ne 0) { throw "Unbalanced display math: $($sources[$index])" }
    $ids = [regex]::Matches($text, '#(o012-[a-z0-9-]+)(?=[}\s])') | ForEach-Object { $_.Groups[1].Value }
    if ($ids.Count -ne $expectedStableIds[$index] -or @($ids | Sort-Object -Unique).Count -ne $expectedStableIds[$index]) {
        throw "Stable-ID mismatch: $($sources[$index])"
    }
    $signature = Get-BlockSignature $text
    if ($signature -ne $expectedBlockSignatures[$index]) { throw "Semantic-block mismatch: $($sources[$index]) ($signature)" }
    [void](Get-MarkdownBody $sources[$index])
}

$pandoc = (Get-Command pandoc -ErrorAction Stop).Source
$versionLine = (& $pandoc --version | Select-Object -First 1)
if ($versionLine -ne 'pandoc 3.9.0.2') { throw "Expected pandoc 3.9.0.2; found: $versionLine" }

foreach ($dir in @($htmlDir, $pdfDir, $checkDir)) {
    New-Item -ItemType Directory -Path $dir -Force | Out-Null
}

$assembled = Join-Path $checkDir 'reader-units-001-019.md'
$header = @'
---
title: "Topologi Aljabar - Unit 1-19"
subtitle: "Homotopi, Ruang Penutup, Grup Fundamental, Teori Klasifikasi, dan Homotopi Tingkat Tinggi"
author:
  - "David Michael Roberts (materi sumber)"
  - "Edisi Bahasa Indonesia dengan pendamping penguasaan"
date: "23 Agustus 2026"
lang: id-ID
rights: "Materi adaptasi dan materi pendamping: CC BY 4.0; lihat atribusi pada setiap unit."
---

'@
$parts = foreach ($source in $sources) { (Get-MarkdownBody $source).TrimEnd("`n") }
$payload = $header.Replace("`r`n", "`n") + ($parts -join "`n`n") + "`n"
[IO.File]::WriteAllText($assembled, $payload, [Text.UTF8Encoding]::new($false))

# Boundary-local styles keep the reader centered, reflowing, offline, and
# readable without changing any previously published stylesheet or artifact.
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

$env:SOURCE_DATE_EPOCH = '1787443200'
$env:FORCE_SOURCE_DATE = '1'

$common = @(
    $assembled,
    '--from=markdown+fenced_divs+tex_math_dollars',
    '--standalone',
    '--toc',
    '--number-sections',
    '--metadata=lang:id-ID',
    '--metadata=pagetitle:Topologi Aljabar - Unit 1-19',
    '--strip-comments'
)

$htmlA = Join-Path $checkDir 'units-001-019-a.html'
$htmlB = Join-Path $checkDir 'units-001-019-b.html'
$htmlArgs = @('--to=html5', '--mathml', '--section-divs', "--css=$baseCss", "--css=$cumulativeCss", "--css=$semanticCss", '--embed-resources')
& $pandoc @common @htmlArgs "--output=$htmlA"
if ($LASTEXITCODE -ne 0) { throw "Pandoc HTML build A failed with exit $LASTEXITCODE" }
& $pandoc @common @htmlArgs "--output=$htmlB"
if ($LASTEXITCODE -ne 0) { throw "Pandoc HTML build B failed with exit $LASTEXITCODE" }
$htmlHashA = (Get-FileHash -LiteralPath $htmlA -Algorithm SHA256).Hash.ToLowerInvariant()
$htmlHashB = (Get-FileHash -LiteralPath $htmlB -Algorithm SHA256).Hash.ToLowerInvariant()
if ($htmlHashA -ne $htmlHashB) { throw "HTML reproducibility failure: $htmlHashA != $htmlHashB" }
Copy-Item -LiteralPath $htmlA -Destination $html -Force

# TeX interprets a bracketed first array cell immediately after `\\` as the
# row break's optional spacing. Keep canonical Markdown untouched and protect
# only bracket-led mathematical lines in the transient PDF assembly.
$pdfAssembled = Join-Path $checkDir 'reader-units-001-019-pdf.md'
$pdfLines = foreach ($line in ($payload -split "`n", 0, 'SimpleMatch')) {
    if ($line.StartsWith('[') -and $line -notmatch '^\[[^]]+\]\(') { '{}'+$line } else { $line }
}
[IO.File]::WriteAllText($pdfAssembled, (($pdfLines -join "`n").TrimEnd("`n") + "`n"), [Text.UTF8Encoding]::new($false))
$pdfCommon = @($common)
$pdfCommon[0] = $pdfAssembled

$pdfA = Join-Path $checkDir 'units-001-019-a.pdf'
$pdfB = Join-Path $checkDir 'units-001-019-b.pdf'
$pdfHeader = Join-Path $checkDir 'reader-units-001-019-header.tex'
[IO.File]::WriteAllText($pdfHeader, "\providecommand{\sslash}{/\mkern-6mu/}`n", [Text.UTF8Encoding]::new($false))
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
