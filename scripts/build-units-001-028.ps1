[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$lane = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$baselineBuilder = Join-Path $PSScriptRoot 'build-units-001-027.ps1'
$authority = Join-Path $lane 'authority\upstream\AlgebraicTopology2019-b947ad2e9f9e301bfe24590a9db653bc54fa1a53\Notes.tex'
$unit028 = Join-Path $lane 'source\id-ID\units\unit-028-lecture-028.md'
$unit028Qa = Join-Path $lane 'qa\UNIT_028_QA.json'
$unit028Review = Join-Path $lane 'qa\UNIT_028_INDEPENDENT_REVIEW.md'
$unit028Audit = Join-Path $lane 'qa\UNIT_028_SOURCE_AUDIT.md'
$baseCss = Join-Path $lane 'source\id-ID\styles\reader.css'
$cumulativeCss = Join-Path $lane 'source\id-ID\styles\reader-cumulative.css'

$htmlDir = Join-Path $lane 'output\html\units-001-028'
$pdfDir = Join-Path $lane 'output\pdf'
$checkDir = Join-Path $lane 'tmp\pdfs\units-001-028-build'
$html = Join-Path $htmlDir 'index.html'
$pdf = Join-Path $pdfDir 'topologi-aljabar-unit-001-028-id.pdf'
$manifestPath = Join-Path $lane 'output\ARTIFACT_MANIFEST_UNITS_001_028.csv'

# Frozen Units 001-027 boundary. These inputs are verified but never invoked
# or rewritten by this cumulative builder.
$baselineFrozen = @{
    $baselineBuilder = @(22221, '6fa8ca886e502ed64cb5bdb01460edf182c80ae3dc42c56a93a788d230087355')
    (Join-Path $lane 'output\html\units-001-027\index.html') = @(4504569, 'd98c2c29344e1e3cc3e81863e426fbf775ca6b70c0a5534d888d80ad2269486d')
    (Join-Path $lane 'output\pdf\topologi-aljabar-unit-001-027-id.pdf') = @(2108928, 'c001b170d7f3bf3554e507350ef2c29652d265c0661c8cdcf407113f843705d7')
    (Join-Path $lane 'output\ARTIFACT_MANIFEST_UNITS_001_027.csv') = @(249, 'c843505221122e756db1fd091172e5cbf8b2cb5fdef247f879d3196ae4070beb')
    (Join-Path $lane 'qa\UNITS_001_027_BUILD_RECEIPT.json') = @(10619, '4c6eec8dac367d87d2aa2752de6ef1dc712f8f1f626c62715067fc4488355ba2')
    (Join-Path $lane 'qa\UNITS_001_027_VISUAL_QA.md') = @(5250, '9e4df75df439777c157ae12f269e331a6c6e1b3d111d0a722654a33c690d992c')
    (Join-Path $lane 'qa\UNITS_001_027_RENDER_INVENTORY.csv') = @(2892, 'f57b3d4e775b9c2314897e9d60d96294be01c6a3b24cb9e8721b971568b314ee')
    $baseCss = @(1297, 'e5184827600116bc54e28df6822c5a98691d5edf88b7b102443b56024733cbe5')
    $cumulativeCss = @(203, 'b0012d9f93e603997d48d49705ec9ccae2d3cd2d062b8b9f8717e908df1f5344')
}
foreach ($path in $baselineFrozen.Keys) {
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { throw "Missing frozen Units 001-027 baseline input: $path" }
    $want = $baselineFrozen[$path]
    $item = Get-Item -LiteralPath $path
    $digest = (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($item.Length -ne $want[0] -or $digest -ne $want[1]) { throw "Frozen Units 001-027 baseline mismatch: $path" }
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

# Freeze the exact upstream authority and physical cumulative source span.
if (-not (Test-Path -LiteralPath $authority -PathType Leaf)) { throw "Missing frozen authority: $authority" }
$authorityBytes = [IO.File]::ReadAllBytes($authority)
$authorityDigest = (Get-FileHash -LiteralPath $authority -Algorithm SHA256).Hash.ToLowerInvariant()
if ($authorityBytes.Length -ne 331447 -or $authorityDigest -ne 'cfe93e9dbe3e25bd96f711f59e6078ab97527682b58e1f8ad127f74357f665d7') {
    throw 'Frozen Notes.tex authority identity mismatch.'
}
if ($authorityBytes -contains 13) { throw 'CR byte in LF-frozen Notes.tex authority.' }
$authorityText = [Text.Encoding]::UTF8.GetString($authorityBytes)
if (([regex]::Matches($authorityText, "`n")).Count -ne 6368) { throw 'Frozen Notes.tex line census mismatch.' }
$authorityLines = $authorityText -split "`n", 0, 'SimpleMatch'
$authoritySpanText = ($authorityLines[133..6051] -join "`n") + "`n"
$authoritySpanBytes = [Text.UTF8Encoding]::new($false).GetBytes($authoritySpanText)
$sha256 = [Security.Cryptography.SHA256]::Create()
try { $authoritySpanDigest = [Convert]::ToHexString($sha256.ComputeHash($authoritySpanBytes)).ToLowerInvariant() }
finally { $sha256.Dispose() }
if ($authoritySpanBytes.Length -ne 308587 -or $authoritySpanDigest -ne '95df91553b5f0805e4041c433cc35dac1067cfe4b2036bfe45bffade61c8a953') {
    throw 'Frozen Notes.tex:134-6052 cumulative span mismatch.'
}
if ($authorityLines[6052] -notmatch '\\lecturenum\{29\}') { throw 'Notes.tex line 6053 is not the Unit 29 boundary.' }

$sources = @((Join-Path $lane 'source\id-ID\reader-unit-001.md')) + @(
    2..28 | ForEach-Object { Join-Path $lane ("source\id-ID\units\unit-{0:000}-lecture-{0:000}.md" -f $_) }
)
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
    @(57277, 1865, 'ba34773d63e4dc70fccdf4fa19fbdc8a397062a4bc359978f3261a70ff64f98c'),
    @(45786, 1425, 'ed086dfe2f26951d4a1d1c398ade0224ffbf4bd1a20a985d267ecd97bbd228d3'),
    @(26237, 786, '47fa3994dc59370fc464e9d150d62512a4602a3cffa5996f1027f93a427e0eec'),
    @(44066, 1349, '0857e51568d77c811d5d79255ac75bfddc87a04b27356ae457d4e66eeffb7d0d'),
    @(39176, 1094, '6f05ddbe6a720109797976c6929b0535f21a38353673cb42d9646a3196f56bd2'),
    @(43085, 1156, '993ad0c3493caff6bd15ab2bcf435f6cbb1f49ed9a1e11bc1009d649ae2d3647'),
    @(36578, 1104, 'df72add4e57236b51ff7d2a0c99af4b65299365874163cb334be5d0988c0f769'),
    @(38537, 1201, '7a2cf4ea31546b8258e3e91c819d3ad516973c8f861249fccc7334b9ade9d835'),
    @(35879, 1175, 'a3238bbc429e4c3689bce3b3bb78c5514e0fae74f276c9efebe694730b2df2a0'),
    @(26072, 814, 'b69036f5a0a8151942288f04197a9dc69c81d2902fe8a15a0e73601978fefe67')
)
for ($index = 0; $index -lt $sources.Count; $index++) {
    $path = $sources[$index]
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { throw "Missing cumulative source: $path" }
    $bytes = [IO.File]::ReadAllBytes($path)
    $text = [Text.Encoding]::UTF8.GetString($bytes)
    $want = $sourceExpected[$index]
    $digest = (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($bytes.Length -ne $want[0] -or ([regex]::Matches($text, "`n")).Count -ne $want[1] -or $digest -ne $want[2]) {
        throw "Cumulative source identity mismatch: $path"
    }
    if (-not $text.EndsWith("`n")) { throw "Missing final LF: $path" }
    [void](Get-MarkdownBody $path)
}

# Frozen Unit 028 reader and complete admission-evidence quartet.
$unit028Frozen = @{
    $unit028 = @(26072, 'b69036f5a0a8151942288f04197a9dc69c81d2902fe8a15a0e73601978fefe67')
    $unit028Audit = @(5660, '2b181bcd12c95210395b3aec8b866b69093d6636b89773d08d93cec41870fa4a')
    $unit028Review = @(6807, '92d81718580eded1daac0593fe2e13d7797c9ed2d8507e70fe5f7dd522fde505')
    $unit028Qa = @(9792, 'dd448f5d5d1a60f6b8e5815a1cb993946c7400f55b46d287f25a78d59f068c79')
}
foreach ($path in $unit028Frozen.Keys) {
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { throw "Missing frozen Unit 028 gate input: $path" }
    $want = $unit028Frozen[$path]
    if ((Get-Item -LiteralPath $path).Length -ne $want[0] -or (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $want[1]) {
        throw "Unit 028 gate identity mismatch: $path"
    }
}
$reviewText = [IO.File]::ReadAllText($unit028Review)
if (-not $reviewText.Contains('P1: 0, P2: 0, P3: 0') -or -not $reviewText.Contains('26.072 byte') -or
    -not $reviewText.Contains('261 simpul MathML')) {
    throw 'Unit 028 independent review is not the zero-finding final snapshot.'
}
$qaText = [IO.File]::ReadAllText($unit028Qa)
if ($qaText -notmatch '"status"\s*:\s*"PASS"' -or $qaText -notmatch '"model_provenance"\s*:\s*"OpenAI Codex gpt-5\.6-sol, Ultra"' -or
    -not $qaText.Contains('b69036f5a0a8151942288f04197a9dc69c81d2902fe8a15a0e73601978fefe67')) {
    throw 'Unit 028 QA is not a passing, source-bound, model-attributed receipt.'
}
$unit028Text = [IO.File]::ReadAllText($unit028)
foreach ($marker in @('TODO', 'TBD', 'FILL_AFTER', 'C:\Users\', 'C:/Users/', 'github_pat_', 'ghp_', 'sk-proj_', 'access_token')) {
    if ($unit028Text.Contains($marker)) { throw "Private or placeholder marker in Unit 028: $marker" }
}
if (([regex]::Matches($unit028Text, '(?m)^[ \t]*::: \{')).Count -ne 39 -or
    ([regex]::Matches($unit028Text, '(?m)^[ \t]*:::\s*$')).Count -ne 39) { throw 'Unit 028 fenced-div census or balance mismatch.' }
if (([regex]::Matches($unit028Text, '\$\$')).Count % 2 -ne 0) { throw 'Unit 028 has unbalanced display math.' }
$unit028Ids = [regex]::Matches($unit028Text, '#(o012-[a-z0-9-]+)(?=[}\s])') | ForEach-Object { $_.Groups[1].Value }
if ($unit028Ids.Count -ne 47 -or @($unit028Ids | Sort-Object -Unique).Count -ne 47) { throw 'Unit 028 stable-ID census mismatch.' }
$blockKinds = 'aside|boundary|corollary|definition|equation|example|exercise|figure|hint|lemma|proof|proposition|remark|solution|source-audit|source-margin|theorem'
$counts = @{}
foreach ($match in [regex]::Matches($unit028Text, "(?m)^[ \t]*::: \{\.(?<kind>$blockKinds)\s+#o012-")) {
    $kind = $match.Groups['kind'].Value
    if ($counts.ContainsKey($kind)) { $counts[$kind] += 1 } else { $counts[$kind] = 1 }
}
$signature = (($counts.GetEnumerator() | Sort-Object Name | ForEach-Object { "$($_.Name)=$($_.Value)" }) -join ',')
if ($signature -ne 'aside=3,boundary=1,corollary=1,definition=1,example=1,exercise=6,hint=6,proof=4,proposition=3,solution=6,source-audit=5,theorem=2') {
    throw "Unit 028 semantic-block mismatch: $signature"
}
if (-not $unit028Text.Contains('\rho_n:=\iota_n^*\colon') -or
    -not $unit028Text.Contains('Baris 6053')) {
    throw 'Unit 028 comparison-map or terminal cursor marker is missing.'
}

$pandoc = (Get-Command pandoc -ErrorAction Stop).Source
$versionLine = (& $pandoc --version | Select-Object -First 1)
if ($versionLine -ne 'pandoc 3.9.0.2') { throw "Expected pandoc 3.9.0.2; found: $versionLine" }
if (Test-Path -LiteralPath $checkDir) { throw "Build scratch directory already exists: $checkDir" }
foreach ($dir in @($htmlDir, $pdfDir, $checkDir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }

$assembled = Join-Path $checkDir 'reader-units-001-028.md'
$header = @'
---
title: "Topologi Aljabar - Unit 1-28"
subtitle: "Homotopi, Ruang Penutup, Grup Fundamental, Kohomologi Simpleksial dan Singular, Kohomologi Relatif dan Tereduksi, Lema Lima, Mayer--Vietoris, Kohomologi Sfera, Eksisi, serta Baji Sfera"
author:
  - "David Michael Roberts (materi sumber)"
  - "Edisi Bahasa Indonesia dengan pendamping penguasaan"
date: "24 Agustus 2026"
lang: id-ID
rights: "Materi adaptasi dan materi pendamping: CC BY 4.0; lihat atribusi pada setiap unit."
provenance: "OpenAI Codex gpt-5.6-sol, Ultra; atas arahan pengguna; kredit penulis sumber dan kontributor manusia dipertahankan."
source_authority: "DavidMichaelRoberts/AlgebraicTopology2019@b947ad2e9f9e301bfe24590a9db653bc54fa1a53"
---

'@
$parts = foreach ($source in $sources) { (Get-MarkdownBody $source).TrimEnd("`n") }
$payload = $header.Replace("`r`n", "`n") + ($parts -join "`n`n") + "`n"
[IO.File]::WriteAllText($assembled, $payload, [Text.UTF8Encoding]::new($false))

# Normalize two presentation-only arrow macro combinations only in the
# transient HTML input; source and PDF retain the frozen TeX exactly.
$htmlAssembled = Join-Path $checkDir 'reader-units-001-028-html.md'
$htmlPayload = $payload.Replace('\big\downarrow', '\downarrow').Replace('\lhook\joinrel\longrightarrow', '\hookrightarrow')
[IO.File]::WriteAllText($htmlAssembled, $htmlPayload, [Text.UTF8Encoding]::new($false))

$semanticCss = Join-Path $checkDir 'semantic-cumulative.css'
$semanticRules = @'
*, *::before, *::after { box-sizing: border-box; }
body { width: min(100%, 72rem); max-width: 72rem; margin-inline: auto; }
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
[IO.File]::WriteAllText($semanticCss, $semanticRules.Replace("`r`n", "`n"), [Text.UTF8Encoding]::new($false))

$env:SOURCE_DATE_EPOCH = '1787529600'
$env:FORCE_SOURCE_DATE = '1'
$common = @(
    $htmlAssembled,
    '--from=markdown+fenced_divs+tex_math_dollars', '--standalone', '--toc', '--number-sections',
    '--metadata=lang:id-ID', '--metadata=pagetitle:Topologi Aljabar - Unit 1-28',
    '--metadata=provenance:OpenAI Codex gpt-5.6-sol, Ultra',
    '--metadata=source-authority:DavidMichaelRoberts/AlgebraicTopology2019@b947ad2e9f9e301bfe24590a9db653bc54fa1a53',
    '--strip-comments'
)

$htmlA = Join-Path $checkDir 'units-001-028-a.html'
$htmlB = Join-Path $checkDir 'units-001-028-b.html'
$htmlArgs = @('--to=html5', '--mathml', '--section-divs', '--fail-if-warnings', "--css=$baseCss", "--css=$cumulativeCss", "--css=$semanticCss", '--embed-resources')
& $pandoc @common @htmlArgs "--output=$htmlA"
if ($LASTEXITCODE -ne 0) { throw "Pandoc HTML build A failed with exit $LASTEXITCODE" }
& $pandoc @common @htmlArgs "--output=$htmlB"
if ($LASTEXITCODE -ne 0) { throw "Pandoc HTML build B failed with exit $LASTEXITCODE" }
$htmlHashA = (Get-FileHash -LiteralPath $htmlA -Algorithm SHA256).Hash.ToLowerInvariant()
$htmlHashB = (Get-FileHash -LiteralPath $htmlB -Algorithm SHA256).Hash.ToLowerInvariant()
if ($htmlHashA -ne $htmlHashB) { throw "HTML reproducibility failure: $htmlHashA != $htmlHashB" }

$htmlText = [IO.File]::ReadAllText($htmlA)
$domIds = [regex]::Matches($htmlText, '\bid="(?<id>[^"]+)"') | ForEach-Object { $_.Groups['id'].Value }
$duplicateIds = @($domIds | Group-Object | Where-Object Count -gt 1)
if ($duplicateIds.Count -ne 0) { throw "Duplicate HTML IDs: $($duplicateIds.Name -join ', ')" }
$domIdSet = [Collections.Generic.HashSet[string]]::new([string[]]@($domIds))
$fragmentLinks = [regex]::Matches($htmlText, '\bhref="#(?<id>[^"]+)"') | ForEach-Object { [Uri]::UnescapeDataString($_.Groups['id'].Value) }
$missingFragments = @($fragmentLinks | Sort-Object -Unique | Where-Object { -not $domIdSet.Contains($_) })
if ($missingFragments.Count -ne 0) { throw "Unresolved HTML fragment targets: $($missingFragments -join ', ')" }
$missingUnit028Ids = @($unit028Ids | Where-Object { -not $domIdSet.Contains($_) })
if ($missingUnit028Ids.Count -ne 0) { throw "Unit 028 IDs missing from HTML: $($missingUnit028Ids -join ', ')" }
$htmlPlain = [Net.WebUtility]::HtmlDecode([regex]::Replace($htmlText, '(?s)<[^>]+>', ' '))
$htmlNormalized = [regex]::Replace($htmlPlain, '\s+', ' ').Trim()
if ($htmlText -notmatch '<html[^>]+lang="id-ID"' -or -not $htmlNormalized.Contains('OpenAI Codex gpt-5.6-sol, Ultra')) { throw 'HTML language or model provenance is missing.' }
if ($htmlText -match '(?is)<script\b[^>]*\bsrc\s*=' -or $htmlText -match '(?is)<link\b[^>]*\bhref\s*=' -or
    $htmlText -match '(?is)<(?:img|iframe)\b[^>]*\bsrc\s*=\s*["'']https?://') { throw 'HTML has a runtime external dependency.' }
foreach ($marker in @('C:\Users\', 'C:/Users/', 'github_pat_', 'ghp_', 'sk-proj_', 'access_token', 'FILL_AFTER')) {
    if ($htmlText.Contains($marker)) { throw "Private or placeholder marker in HTML: $marker" }
}
$mathmlNodes = ([regex]::Matches($htmlText, '<math\b')).Count
$semanticFigures = ([regex]::Matches($htmlText, 'class="[^"]*\bfigure\b[^"]*"')).Count
$rawMathFallbacks = ([regex]::Matches($htmlText, '<span class="math (?:display|inline)">')).Count
if ($mathmlNodes -le 0 -or $semanticFigures -le 0 -or $rawMathFallbacks -ne 0) { throw 'HTML lost MathML/semantic figures or retained raw-TeX math fallbacks.' }
foreach ($cssMarker in @('width: min(100%, 72rem)', 'margin-inline: auto', '@media (max-width: 700px)', 'math[display="block"]', 'math[display="inline"]')) {
    if (-not $htmlText.Contains($cssMarker)) { throw "HTML responsive/centering CSS marker is missing: $cssMarker" }
}
Copy-Item -LiteralPath $htmlA -Destination $html -Force

$pdfAssembled = Join-Path $checkDir 'reader-units-001-028-pdf.md'
$inDisplayMath = $false
$pdfLines = foreach ($line in ($payload -split "`n", 0, 'SimpleMatch')) {
    if ($line.StartsWith('[') -and $inDisplayMath) { '{}'+$line } else { $line }
    if (([regex]::Matches($line, '\$\$')).Count % 2 -eq 1) { $inDisplayMath = -not $inDisplayMath }
}
if ($inDisplayMath) { throw 'PDF transient assembly ended inside an unclosed display-math block.' }
[IO.File]::WriteAllText($pdfAssembled, (($pdfLines -join "`n").TrimEnd("`n") + "`n"), [Text.UTF8Encoding]::new($false))
$pdfCommon = @($common)
$pdfCommon[0] = $pdfAssembled
$pdfA = Join-Path $checkDir 'units-001-028-a.pdf'
$pdfB = Join-Path $checkDir 'units-001-028-b.pdf'
$pdfHeader = Join-Path $checkDir 'reader-units-001-028-header.tex'
[IO.File]::WriteAllText($pdfHeader, "\providecommand{\sslash}{/\mkern-6mu/}`n", [Text.UTF8Encoding]::new($false))
$pdfArgs = @('--pdf-engine=pdflatex', "--include-in-header=$pdfHeader", '--variable=papersize:a4', '--variable=geometry:margin=21mm', '--variable=fontsize:11pt', '--variable=colorlinks:true', '--variable=linkcolor:blue')
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
    $digest = (Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
    "$relative,$($item.Length),$digest"
}
[IO.File]::WriteAllText($manifestPath, "path,bytes,sha256`n" + (($rows | Sort-Object) -join "`n") + "`n", [Text.UTF8Encoding]::new($false))

Remove-Item -LiteralPath $htmlA, $htmlB, $pdfA, $pdfB, $assembled, $htmlAssembled, $pdfAssembled, $semanticCss, $pdfHeader -Force
Remove-Item -LiteralPath $checkDir -Force

[pscustomobject]@{
    status = 'PASS'
    html = $html
    html_bytes = (Get-Item -LiteralPath $html).Length
    html_sha256 = $htmlHashA
    html_unique_ids = @($domIds | Sort-Object -Unique).Count
    html_fragment_links = $fragmentLinks.Count
    html_mathml_nodes = $mathmlNodes
    html_semantic_figures = $semanticFigures
    html_raw_math_fallbacks = $rawMathFallbacks
    unit_028_ids = $unit028Ids.Count
    pdf = $pdf
    pdf_bytes = (Get-Item -LiteralPath $pdf).Length
    pdf_sha256 = $pdfHashA
    manifest = $manifestPath
    manifest_sha256 = (Get-FileHash -LiteralPath $manifestPath -Algorithm SHA256).Hash.ToLowerInvariant()
    pandoc = $versionLine
    source_date_epoch = $env:SOURCE_DATE_EPOCH
    model_provenance = 'OpenAI Codex gpt-5.6-sol, Ultra'
    source_authority = 'DavidMichaelRoberts/AlgebraicTopology2019@b947ad2e9f9e301bfe24590a9db653bc54fa1a53'
}
