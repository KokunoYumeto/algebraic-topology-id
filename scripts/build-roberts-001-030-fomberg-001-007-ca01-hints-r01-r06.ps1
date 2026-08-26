[CmdletBinding()]
param()

# Deterministic additive build: sealed CA01 reader + 36 original ordinary
# hints for D60-R01-D60-R06.  The script writes only its named reader
# artifacts, manifest, and draft receipt; source/backend/control inputs remain
# immutable.
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$lane = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$lf = [string][char]10
$utf8 = [Text.UTF8Encoding]::new($false)
$sourceSha = 'dc319cb191d709a5807f0c0792401f9faf2993ceede364764547f20bb4f69c2a'
$sourceRel = 'source/id-ID/mastery/ordinary-hints-r01-r06.md'

$priorHtml = Join-Path $lane 'output\html\roberts-001-030-fomberg-001-007-ca01\index.html'
$priorPdf = Join-Path $lane 'output\pdf\topologi-aljabar-roberts-001-030-fomberg-001-007-ca01-id.pdf'
$priorManifest = Join-Path $lane 'output\ARTIFACT_MANIFEST_ROBERTS_001_030_FOMBERG_001_007_CA01.csv'
$priorReceipt = Join-Path $lane 'qa\ROBERTS_001_030_FOMBERG_001_007_CA01_BUILD_RECEIPT.json'
$source = Join-Path $lane $sourceRel
$sourceQa = Join-Path $lane 'qa\ORDINARY_HINTS_R01_R06_QA.json'
$backendReceipt = Join-Path $lane 'qa\BACKEND_APPEND_ONLY_ORDINARY_HINTS_R01_R06_CUMULATIVE_RECEIPT.json'
$semanticBackendRel = 'qa/BACKEND_APPEND_ONLY_ORDINARY_HINTS_R01_R06_RECEIPT.json'

$htmlDir = Join-Path $lane 'output\html\roberts-001-030-fomberg-001-007-ca01-hints-r01-r06'
$htmlOut = Join-Path $htmlDir 'index.html'
$pdfOut = Join-Path $lane 'output\pdf\topologi-aljabar-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-id.pdf'
$manifestOut = Join-Path $lane 'output\ARTIFACT_MANIFEST_ROBERTS_001_030_FOMBERG_001_007_CA01_HINTS_R01_R06.csv'
$draftReceipt = Join-Path $lane 'qa\ROBERTS_001_030_FOMBERG_001_007_CA01_HINTS_R01_R06_BUILD_DRAFT.json'
$finalizer = Join-Path $lane 'scripts\finalize-build-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06.py'
$scratch = Join-Path $lane 'tmp\pdfs\roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-build'

function Require([bool]$condition, [string]$message) {
    if (-not $condition) { throw $message }
}
function Digest([string]$path) {
    return (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()
}
function Assert-Identity([string]$path, [long]$bytes, [string]$sha256) {
    Require (Test-Path -LiteralPath $path -PathType Leaf) "Missing frozen input: $path"
    $item = Get-Item -LiteralPath $path
    $actual = Digest $path
    Require ($item.Length -eq $bytes -and $actual -eq $sha256) "Frozen identity mismatch: $path ($($item.Length), $actual)"
}
function Read-LfUtf8([string]$path) {
    $bytes = [IO.File]::ReadAllBytes($path)
    Require ($bytes.Length -gt 0 -and -not ($bytes -contains 13)) "Input is empty or not LF-only: $path"
    return $utf8.GetString($bytes)
}
function Read-NormalizedGeneratedUtf8([string]$path) {
    $text = $utf8.GetString([IO.File]::ReadAllBytes($path)).Replace("`r`n", "`n")
    Require (-not $text.Contains("`r")) "Generated input contains a bare CR: $path"
    return $text
}
function Relative([string]$path) {
    $full = [IO.Path]::GetFullPath($path)
    $prefix = $lane.TrimEnd([IO.Path]::DirectorySeparatorChar) + [IO.Path]::DirectorySeparatorChar
    Require ($full.StartsWith($prefix, [StringComparison]::OrdinalIgnoreCase)) "Outside lane: $full"
    return $full.Substring($prefix.Length).Replace('\', '/')
}
function Assert-Native([string]$name) {
    if ($LASTEXITCODE -ne 0) { throw "$name failed with exit code $LASTEXITCODE" }
}
function Count-OutlineRows([string]$text) {
    return @(($text -split $lf) | Where-Object { $_ -match '^(?:\+|\||-)' }).Count
}

# Freeze the complete CA01 predecessor and the exact reviewed hint source.
Assert-Identity $priorHtml 14958219 'd71e2f3c0eb38b48fe4686a955ad555db3a407df8f18e41371d52908f0bdbbdf'
Assert-Identity $priorPdf 8358561 '476b0de3bbb2cbfe03a151ac3060e121c5f89364e70b54d918ab270f4c965ade'
Assert-Identity $priorManifest 297 'eac46f939ac99da1479c7826a350eb926c30f91d4c74fdfe785a597f7a58803d'
Assert-Identity $priorReceipt 7842 '22fef828b7963219759f85d11e409e0ebf957889d0fa76dc02ec04f3a707a9e0'
Assert-Identity $source 28698 $sourceSha
Require (Test-Path -LiteralPath $sourceQa -PathType Leaf) "Missing static hint QA: $sourceQa"
Require (Test-Path -LiteralPath $backendReceipt -PathType Leaf) "Missing cumulative hint backend receipt: $backendReceipt"
Require (Test-Path -LiteralPath $finalizer -PathType Leaf) "Missing build finalizer: $finalizer"

$qaRaw = Read-LfUtf8 $sourceQa
$qa = $qaRaw | ConvertFrom-Json
Require ($qa.status -eq 'PASS' -and $qaRaw.Contains($sourceSha) -and $qaRaw.Replace('\', '/').Contains($sourceRel)) 'Static hint QA is not PASS or does not bind the live source.'
$backendRaw = Read-LfUtf8 $backendReceipt
$backend = $backendRaw | ConvertFrom-Json
Require ($backend.status -eq 'PASS' -and $backend.receipt_kind -eq 'cumulative_backend_boundary' -and $backend.replay.status -eq 'PASS') 'Cumulative hint backend/replay gate failed.'
Require ($backend.immutable_prefix.preserved_exactly -eq $true -and $backend.immutable_prefix.records -eq 6854 -and $backend.immutable_prefix.bytes -eq 8345799 -and $backend.immutable_prefix.bundle_sha256 -eq '51e75d06e620762e629e9e7408da4b0c32b3e337817d9d140fbbdfa438de2f57') 'Cumulative backend immutable-prefix identity drift.'
Require ($backend.delta.records -eq 158 -and $backend.delta.bytes -eq 199933 -and $backend.delta.bundle_sha256 -eq 'a4ec1979000ba447ffa2a2534279de0b9ed374c1c560461b6a69b2ee5e6ceb6e') 'Cumulative backend delta identity drift.'
Require ($backend.cumulative.records -eq 7012 -and $backend.cumulative.bytes -eq 8545732 -and $backend.cumulative.bundle_sha256 -eq '7d723f9ef163303c7dde63d646dc8d5917c2450b1da5d24c87ef77bf4e4d664b') 'Cumulative backend identity drift.'
Require ($backend.replay.final.records -eq 7012 -and $backend.replay.final.bytes -eq 8545732 -and $backend.replay.final.bundle_sha256 -eq '7d723f9ef163303c7dde63d646dc8d5917c2450b1da5d24c87ef77bf4e4d664b' -and $backend.replay.exact_file_matches -eq 11 -and $backend.replay.suffix_bytes -eq 199933 -and $backend.replay.temporary_replay_removed -eq $true) 'Cumulative backend replay identity drift.'
$graph = $backend.semantic_checks.graph_postconditions
Require ($backend.semantic_checks.added_records -eq 158 -and $backend.semantic_checks.merged_records -eq 7012 -and $backend.semantic_checks.artifact_evidence -eq 'PASS' -and $backend.semantic_checks.global_references -eq 'PASS' -and $backend.semantic_checks.prompt_solution_solves_immutability -eq 'PASS' -and $backend.semantic_checks.rights_closure -eq 'PASS' -and $backend.semantic_checks.route_mapping -eq 'PASS' -and $backend.semantic_checks.schema_shapes -eq 'PASS') 'Cumulative backend semantic gate failed.'
Require ($graph.active_hint_relations -eq 165 -and $graph.active_hint_units -eq 165 -and $graph.active_solves_relations -eq 221 -and $graph.ca01_items -eq 8 -and $graph.credited_total -eq 92 -and $graph.ordinary_capped_route_credit -eq 84 -and $graph.ordinary_graph_complete_triples -eq 157 -and $graph.graph_complete_triples -eq 165 -and $graph.duplicate_or_reused_solution_ids -eq 0) 'Cumulative backend semantic graph gate failed.'
$routeCensus = $backend.route_mastery_census
Require ($routeCensus.status -eq 'PASS' -and $routeCensus.path -eq 'qa/ROUTE_MASTERY_CENSUS.json' -and $routeCensus.bytes -eq 140589 -and $routeCensus.sha256 -eq '068072d3c67aeed28d55fdb9947a3084e4028ba0b808e28f46c0657ba84d20ff' -and $routeCensus.ordinary_capped_credit -eq 84 -and $routeCensus.ca01_credit -eq 8 -and $routeCensus.total_credit -eq 92 -and $routeCensus.validation_errors -eq 0 -and @($routeCensus.duplicate_or_reused_solution_ids).Count -eq 0) 'Cumulative backend route-mastery census gate failed.'

# The cumulative receipt seals its semantic receipt by path, size, and digest;
# that supporting receipt, in turn, seals the reviewed source input.  Follow
# this authenticated receipt chain instead of requiring the cumulative JSON to
# repeat a source path that it deliberately does not duplicate.
$semanticRef = $backend.supporting_receipts.semantic
Require ($semanticRef.path -eq $semanticBackendRel -and $semanticRef.bytes -eq 2615 -and $semanticRef.lf_lines -eq 71 -and $semanticRef.sha256 -eq '6ea98f4a65a6104e7d115a892e9906103e5434f6c10375959cd09b762df8c0c5') 'Cumulative backend semantic-receipt reference drift.'
$semanticBackendReceipt = Join-Path $lane ($semanticBackendRel.Replace('/', '\'))
Assert-Identity $semanticBackendReceipt 2615 $semanticRef.sha256
$semanticRaw = Read-LfUtf8 $semanticBackendReceipt
$semantic = $semanticRaw | ConvertFrom-Json
Require (([regex]::Matches($semanticRaw, $lf)).Count -eq 71) 'Supporting semantic backend receipt LF-line count drift.'
Require ($semantic.status -eq 'PASS' -and $semantic.receipt_kind -eq 'semantic_append_validation' -and $semantic.edition_unit_id -eq 'O012-ORIG-HINTS-R01-R06' -and $semantic.source_sha256 -eq $sourceSha) 'Supporting semantic backend receipt failed.'
$expectedSemanticInputs = [ordered]@{
    'source/id-ID/mastery/ordinary-hints-r01-r06.md' = @{ bytes = 28698; lf_lines = 410; sha256 = $sourceSha }
    'qa/ORDINARY_HINTS_R01_R06_QA.json' = @{ bytes = 16616; lf_lines = 398; sha256 = 'a0460dbed83242863fc1aab8290b76fac9cd39644276e132401e7d3e9198c33d' }
    'qa/ordinary-hints-r01-r06/INDEPENDENT_MATH_REVIEW.json' = @{ bytes = 19289; lf_lines = 447; sha256 = '8ed5b3563976b415e1aa471f7cdeb3405888cbc70aec101bc02e4fab9e45de5a' }
    'qa/ordinary-hints-r01-r06/INDEPENDENT_SOURCE_LANGUAGE_REVIEW.json' = @{ bytes = 18324; lf_lines = 221; sha256 = '6c29009da4ee0380c878c3705dcd2a99cbe7a8495cc4b7f5ce456bb40f910968' }
}
foreach ($inputRel in $expectedSemanticInputs.Keys) {
    $expected = $expectedSemanticInputs[$inputRel]
    $property = $semantic.input_identities.PSObject.Properties[$inputRel]
    Require ($null -ne $property) "Supporting semantic backend receipt omits input: $inputRel"
    $sealed = $property.Value
    Require ($sealed.bytes -eq $expected.bytes -and $sealed.lf_lines -eq $expected.lf_lines -and $sealed.sha256 -eq $expected.sha256) "Supporting semantic input identity drift: $inputRel"
    $inputPath = Join-Path $lane ($inputRel.Replace('/', '\'))
    Assert-Identity $inputPath $expected.bytes $expected.sha256
    $inputRaw = Read-LfUtf8 $inputPath
    Require (([regex]::Matches($inputRaw, $lf)).Count -eq $expected.lf_lines) "Supporting semantic input LF-line count drift: $inputRel"
}

$sourceText = Read-LfUtf8 $source
$sourceIds = @([regex]::Matches($sourceText, '(?<=#)(o012-d60-(?:hints-r01-r06|hints-r0[1-6]|r0[1-6]-hint-\d{3}))(?=[}\s])') | ForEach-Object { $_.Groups[1].Value })
Require ($sourceIds.Count -eq 43 -and @($sourceIds | Sort-Object -Unique).Count -eq 43) 'Ordinary-hint stable-ID census drift.'
$hintBlocks = ([regex]::Matches($sourceText, '(?m)^::: \{\.hint #o012-d60-r0[1-6]-hint-\d{3}\b')).Count
$targetIds = @([regex]::Matches($sourceText, 'data-target-exercise-id="unit:([^"]+)"') | ForEach-Object { $_.Groups[1].Value })
$solutionIds = @([regex]::Matches($sourceText, 'data-existing-solution-id="unit:([^"]+)"') | ForEach-Object { $_.Groups[1].Value })
$sourceLinks = @([regex]::Matches($sourceText, '\]\(#([^)]+)\)') | ForEach-Object { $_.Groups[1].Value })
Require ($hintBlocks -eq 36 -and $targetIds.Count -eq 36 -and $solutionIds.Count -eq 36 -and $sourceLinks.Count -eq 72) 'Ordinary-hint binding/link census drift.'
$expectedLinks = @($targetIds + $solutionIds | Sort-Object)
$actualLinks = @($sourceLinks | Sort-Object)
Require (($expectedLinks -join $lf) -eq ($actualLinks -join $lf)) 'Visible source links do not exactly match exercise/solution bindings.'

if (Test-Path -LiteralPath $draftReceipt -PathType Leaf) { Remove-Item -LiteralPath $draftReceipt -Force }
$scratchFull = [IO.Path]::GetFullPath($scratch)
$allowedScratch = [IO.Path]::GetFullPath((Join-Path $lane 'tmp\pdfs')) + [IO.Path]::DirectorySeparatorChar
Require ($scratchFull.StartsWith($allowedScratch, [StringComparison]::OrdinalIgnoreCase) -and [IO.Path]::GetFileName($scratchFull) -eq 'roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-build') 'Unsafe scratch path.'
Require (-not (Test-Path -LiteralPath $scratchFull)) "Bounded scratch already exists: $scratchFull"
New-Item -ItemType Directory -Path $scratchFull | Out-Null

try {
    $pandoc = (Get-Command pandoc -ErrorAction Stop).Source
    $mutool = (Get-Command mutool -ErrorAction Stop).Source
    $pdfinfo = (Get-Command pdfinfo -ErrorAction Stop).Source
    $pdffonts = (Get-Command pdffonts -ErrorAction Stop).Source
    $pdftotext = (Get-Command pdftotext -ErrorAction Stop).Source
    $python = (Get-Command python -ErrorAction Stop).Source
    $pandocVersion = (& $pandoc --version | Select-Object -First 1)
    Require ($pandocVersion -eq 'pandoc 3.9.0.2') "Expected pandoc 3.9.0.2; found $pandocVersion"
    $env:SOURCE_DATE_EPOCH = '1787702400'
    $env:FORCE_SOURCE_DATE = '1'

    # Convert the additive source twice to a native-MathML fragment.
    $fragmentA = Join-Path $scratchFull 'hints-a.html'
    $fragmentB = Join-Path $scratchFull 'hints-b.html'
    $fragmentArgs = @($source, '--from=markdown+fenced_divs+tex_math_dollars', '--to=html5', '--mathml', '--section-divs', '--strip-comments', '--fail-if-warnings')
    & $pandoc @fragmentArgs "--output=$fragmentA"; Assert-Native 'Pandoc hints HTML fragment A'
    & $pandoc @fragmentArgs "--output=$fragmentB"; Assert-Native 'Pandoc hints HTML fragment B'
    $fragmentHash = Digest $fragmentA
    Require ($fragmentHash -eq (Digest $fragmentB)) 'Hint HTML fragment builds are not byte-identical.'
    $fragment = Read-NormalizedGeneratedUtf8 $fragmentA
    Require (-not $fragment.Contains('<html') -and -not $fragment.Contains('<body')) 'Hint fragment unexpectedly contains a document shell.'
    $fragmentIds = @([regex]::Matches($fragment, '(?<=\s)id="([^"]+)"') | ForEach-Object { $_.Groups[1].Value })
    $fragmentSet = [Collections.Generic.HashSet[string]]::new([string[]]$fragmentIds)
    Require (@($sourceIds | Where-Object { -not $fragmentSet.Contains($_) }).Count -eq 0) 'A hint stable ID is absent from the HTML fragment.'
    $fragmentHints = ([regex]::Matches($fragment, 'class="[^"]*\bhint\b[^"]*"')).Count
    $fragmentLinks = @([regex]::Matches($fragment, '\bhref="#([^"]+)"') | ForEach-Object { $_.Groups[1].Value })
    Require ($fragmentHints -eq 36 -and $fragmentLinks.Count -eq 72) 'Hint HTML fragment census drift.'
    Require (([regex]::Matches($fragment, '<math\b')).Count -gt 0 -and -not $fragment.Contains('$') -and -not $fragment.Contains('\(') -and -not $fragment.Contains('\[')) 'Hint fragment lacks native MathML or retains raw math.'

    # Add title/status/ToC/fragment edits, then reverse them exactly.
    $prior = [IO.File]::ReadAllText($priorHtml, $utf8)
    $htmlNl = if ($prior.Contains("`r`n")) { "`r`n" } else { $lf }
    Require (-not $prior.Replace("`r`n", '').Contains("`r")) 'Predecessor HTML contains a bare CR.'
    $oldTitle = '<title>Topologi Aljabar — Roberts 30/30, Fomberg 1.1–1.13, dan Asesmen Kumulatif 1</title>'
    $newTitle = '<title>Topologi Aljabar — Roberts 30/30, Fomberg 1.1–1.13, Asesmen Kumulatif 1, dan Petunjuk Rute 1–6</title>'
    $oldHeading = '<h1 class="title">Topologi Aljabar — Roberts 30/30, Fomberg' + $htmlNl + '1.1–1.13, dan Asesmen Kumulatif 1</h1>'
    $newHeading = '<h1 class="title">Topologi Aljabar — Roberts 30/30, Fomberg' + $htmlNl + '1.1–1.13, Asesmen Kumulatif 1, dan Petunjuk Rute 1–6</h1>'
    $oldSubtitle = '<p class="subtitle">Komponen Roberts lengkap; jembatan Fomberg melalui' + $htmlNl + 'homologi seluler; Asesmen Kumulatif 1; checkpoint komposit parsial</p>'
    $newSubtitle = '<p class="subtitle">Komponen Roberts lengkap; jembatan Fomberg melalui' + $htmlNl + 'homologi seluler; Asesmen Kumulatif 1; 36 petunjuk penguasaan Rute 1–6; checkpoint komposit parsial</p>'
    foreach ($needle in @($oldTitle, $oldHeading, $oldSubtitle)) {
        Require ($prior.IndexOf($needle, [StringComparison]::Ordinal) -ge 0 -and $prior.LastIndexOf($needle, [StringComparison]::Ordinal) -eq $prior.IndexOf($needle, [StringComparison]::Ordinal)) "Predecessor replacement anchor missing/duplicated: $needle"
    }
    $combined = $prior.Replace($oldTitle, $newTitle).Replace($oldHeading, $newHeading).Replace($oldSubtitle, $newSubtitle)
    $navClose = $htmlNl + '</ul>' + $htmlNl + '</nav>'
    $navPos = $combined.LastIndexOf($navClose, [StringComparison]::Ordinal)
    Require ($navPos -gt 0) 'Top-level ToC close anchor missing.'
    $tocInsert = $htmlNl + '<li><a href="#o012-d60-hints-r01-r06" id="toc-o012-d60-hints-r01-r06">Petunjuk penguasaan Rute 1–6 — 36 pasangan soal–solusi</a></li>'
    $combined = $combined.Insert($navPos, $tocInsert)
    $statusStart = $combined.IndexOf('<section id="o012-composite-status"', [StringComparison]::Ordinal)
    $statusEnd = $combined.IndexOf($htmlNl + '</section>', $statusStart, [StringComparison]::Ordinal)
    Require ($statusStart -ge 0 -and $statusEnd -gt $statusStart) 'Composite status section anchor missing.'
    $statusInsert = $htmlNl + '<aside id="o012-d60-hints-r01-r06-status" class="note" data-origin="edition-original">' + $htmlNl + '<p><strong>Tambahan checkpoint.</strong> Pembaca ini kini memuat 36 petunjuk asli edisi, masing-masing terikat tepat ke satu soal dan satu solusi lengkap yang sudah ada, enam per rute untuk D60-R01–D60-R06. Lapisan CC BY-SA 4.0 ini tidak menyalin atau mengubah soal maupun solusi sumber.</p>' + $htmlNl + '</aside>'
    $combined = $combined.Insert($statusEnd, $statusInsert)
    $bodyClose = $htmlNl + '</body>'
    $bodyPos = $combined.LastIndexOf($bodyClose, [StringComparison]::Ordinal)
    Require ($bodyPos -gt 0) 'HTML body close anchor missing.'
    $fragmentForDocument = if ($htmlNl -eq "`r`n") { $fragment.Replace($lf, "`r`n") } else { $fragment }
    $fragmentInsert = $htmlNl + $fragmentForDocument.TrimEnd([char]13, [char]10)
    $combined = $combined.Insert($bodyPos, $fragmentInsert)

    $reconstructed = $combined
    foreach ($insert in @($fragmentInsert, $statusInsert, $tocInsert)) {
        $pos = $reconstructed.LastIndexOf($insert, [StringComparison]::Ordinal)
        Require ($pos -ge 0) 'Cannot reverse an additive HTML insertion.'
        $reconstructed = $reconstructed.Remove($pos, $insert.Length)
    }
    $reconstructed = $reconstructed.Replace($newTitle, $oldTitle).Replace($newHeading, $oldHeading).Replace($newSubtitle, $oldSubtitle)
    $reconstructedPath = Join-Path $scratchFull 'reconstructed-ca01.html'
    [IO.File]::WriteAllText($reconstructedPath, $reconstructed, $utf8)
    Require ((Get-Item -LiteralPath $reconstructedPath).Length -eq 14958219 -and (Digest $reconstructedPath) -eq 'd71e2f3c0eb38b48fe4686a955ad555db3a407df8f18e41371d52908f0bdbbdf') 'Exact CA01 HTML reconstruction failed.'

    $htmlA = Join-Path $scratchFull 'combined-a.html'
    $htmlB = Join-Path $scratchFull 'combined-b.html'
    [IO.File]::WriteAllText($htmlA, $combined, $utf8)
    [IO.File]::WriteAllText($htmlB, $combined, $utf8)
    Require ((Digest $htmlA) -eq (Digest $htmlB)) 'Combined HTML writes differ.'
    $allIds = @([regex]::Matches($combined, '(?<=\s)id="([^"]+)"') | ForEach-Object { $_.Groups[1].Value })
    Require (@($allIds | Group-Object | Where-Object Count -gt 1).Count -eq 0) 'Combined HTML has duplicate IDs.'
    $idSet = [Collections.Generic.HashSet[string]]::new([string[]]$allIds)
    $allFragments = @([regex]::Matches($combined, '\bhref="#([^"]+)"') | ForEach-Object { [Net.WebUtility]::HtmlDecode($_.Groups[1].Value) })
    Require (@($allFragments | Sort-Object -Unique | Where-Object { -not $idSet.Contains($_) }).Count -eq 0) 'Combined HTML has an unresolved fragment.'
    $mathml = ([regex]::Matches($combined, '<math\b')).Count
    Require ($mathml -gt 16130 -and $combined.Contains($newTitle) -and $combined.Contains('id="toc-o012-d60-hints-r01-r06"')) 'Combined HTML title/ToC/MathML gate failed.'
    Require ($combined -match '<html[^>]+lang="id-ID"' -and $combined -notmatch '(?is)<(?:script|link)\b[^>]*(?:src|href)\s*=' -and $combined -notmatch '(?is)<img\b[^>]*\bsrc\s*=\s*[''\"]https?://') 'Combined HTML language/self-contained gate failed.'
    foreach ($cssMarker in @('width: min(100%, 72rem)', 'max-width: 72rem', 'margin-inline: auto', '@media (max-width: 700px)', 'math[display="block"]', 'math[display="inline"]')) { Require ($combined.Contains($cssMarker)) "Responsive CSS marker missing: $cssMarker" }
    foreach ($marker in @('C:\Users\', 'github_pat_', 'ghp_', 'access_token', 'FILL_AFTER', 'BEGIN PRIVATE KEY')) { Require (-not $combined.Contains($marker)) "Private/transient marker in HTML: $marker" }

    # Build the hint appendix twice.  The build-only transform removes Pandoc's
    # implicit identifiers and emits explicit \hypertarget anchors for all 43
    # source IDs, so the merged PDF can preserve the entire semantic surface.
    # Paragraph boundaries also prevent fenced-div anchors from consuming
    # heading/paragraph spacing.
    $pdfHeader = Join-Path $scratchFull 'hints-header.tex'
    [IO.File]::WriteAllText($pdfHeader, ("\AddToHook{begindocument/end}{\pdftrailerid{}}$lf"), $utf8)
    $pdfSource = Join-Path $scratchFull 'hints-layout.md'
    $hintOpen = [regex]::new('(?m)^(::: \{\.hint )#(o012-d60-r0[1-6]-hint-\d{3})([^\r\n]*\})$')
    Require ($hintOpen.Matches($sourceText).Count -eq 36) 'Hint layout-transform census drift.'
    $pdfSourceText = $hintOpen.Replace($sourceText, ('$1$3' + $lf + $lf + '```{=latex}' + $lf + '\hypertarget{$2}{}' + $lf + '\par\noindent' + $lf + '```'))
    $headingOpen = [regex]::new('(?m)^(#{1,2})\s+(.+?)\s+\{#(o012-d60-hints-(?:r01-r06|r0[1-6]))\}\s*$')
    Require ($headingOpen.Matches($pdfSourceText).Count -eq 7) 'Hint heading destination-transform census drift.'
    $pdfSourceText = $headingOpen.Replace($pdfSourceText, ('$1 $2' + $lf + $lf + '```{=latex}' + $lf + '\hypertarget{$3}{}' + $lf + '```'))
    # The target anchors live in the separately built, frozen predecessor PDF.
    # Pandoc's ordinary internal-link form suppresses annotations when a target
    # is absent from the appendix compilation. Emit explicit named GoTo links;
    # the deterministic merger supplies and verifies all 72 destinations.
    $pdfLink = [regex]::new('\[([^\]]+)\]\(#(o012-rbt-[^)]+)\)')
    Require ($pdfLink.Matches($pdfSourceText).Count -eq 72) 'Hint PDF named-link transform census drift.'
    $pdfSourceText = $pdfLink.Replace($pdfSourceText, '\hyperlink{$2}{$1}')
    [IO.File]::WriteAllText($pdfSource, $pdfSourceText, $utf8)
    $appendWork = Join-Path $scratchFull 'hints-work.pdf'
    $appendA = Join-Path $scratchFull 'hints-a.pdf'
    $appendB = Join-Path $scratchFull 'hints-b.pdf'
    $pdfArgs = @($pdfSource, '--from=markdown+fenced_divs+tex_math_dollars', '--standalone', '--number-sections', '--strip-comments', '--metadata=lang:id-ID', '--metadata=pagetitle:Petunjuk Penguasaan Rute 1–6', '--metadata=date:26 Agustus 2026', '--pdf-engine=pdflatex', "--include-in-header=$pdfHeader", '--variable=papersize:a4', '--variable=geometry:margin=21mm', '--variable=fontsize:11pt', '--variable=colorlinks:true', '--variable=linkcolor:blue', '--variable=pdf-trailer-id:')
    & $pandoc @pdfArgs "--output=$appendWork"; Assert-Native 'Pandoc hint PDF A'
    Copy-Item -LiteralPath $appendWork -Destination $appendA -Force
    & $pandoc @pdfArgs "--output=$appendWork"; Assert-Native 'Pandoc hint PDF B'
    Copy-Item -LiteralPath $appendWork -Destination $appendB -Force
    $appendHash = Digest $appendA
    Require ($appendHash -eq (Digest $appendB)) 'Hint appendix PDF builds differ.'
    $appendInfo = (& $pdfinfo $appendA) -join $lf; Assert-Native 'pdfinfo hint appendix'
    $appendPageMatch = [regex]::Match($appendInfo, '(?m)^Pages:\s+(\d+)\s*$')
    Require ($appendPageMatch.Success -and [int]$appendPageMatch.Groups[1].Value -gt 0 -and $appendInfo -match '(?m)^Page size:.*\(A4\)\s*$' -and $appendInfo -match '(?m)^Encrypted:\s+no\s*$') 'Hint appendix PDF page/A4 gate failed.'
    $appendPages = [int]$appendPageMatch.Groups[1].Value
    $appendTrailer = (& $mutool show $appendA trailer) -join $lf; Assert-Native 'mutool hint trailer'
    Require ($appendTrailer -notmatch '(?m)^\s*/ID\s') 'Hint appendix trailer unexpectedly contains /ID.'
    $appendOutline = (& $mutool show $appendA outline) -join $lf; Assert-Native 'mutool hint outline'
    Require ((Count-OutlineRows $appendOutline) -eq 7) 'Hint appendix outline must contain the source heading plus six route headings.'

    $mergedA = Join-Path $scratchFull 'combined-a.pdf'
    $mergedB = Join-Path $scratchFull 'combined-b.pdf'
    & $python '-B' $finalizer '--merge-pdfs' '--prior' $priorPdf '--append' $appendA '--output' $mergedA; Assert-Native 'pypdf deterministic hint merge A'
    & $python '-B' $finalizer '--merge-pdfs' '--prior' $priorPdf '--append' $appendB '--output' $mergedB; Assert-Native 'pypdf deterministic hint merge B'
    $mergedHash = Digest $mergedA
    Require ($mergedHash -eq (Digest $mergedB)) 'Merged hint PDF builds differ.'
    $mergedPages = 477 + $appendPages
    $mergedInfo = (& $pdfinfo $mergedA) -join $lf; Assert-Native 'pdfinfo merged hint PDF'
    Require ($mergedInfo -match "(?m)^Pages:\s+$mergedPages\s*`$" -and $mergedInfo -match '(?m)^Page size:.*\(A4\)\s*$' -and $mergedInfo -match '(?m)^Encrypted:\s+no\s*$') 'Merged PDF page/A4 gate failed.'
    $mergedTrailer = (& $mutool show $mergedA trailer) -join $lf; Assert-Native 'mutool merged hint trailer'
    Require ($mergedTrailer -notmatch '(?m)^\s*/ID\s') 'Merged hint PDF trailer unexpectedly contains /ID.'
    $fontRows = @((& $pdffonts $mergedA) | Select-Object -Skip 2 | Where-Object { $_.Trim().Length -gt 0 }); Assert-Native 'pdffonts merged hint PDF'
    Require ($fontRows.Count -gt 0) 'Merged PDF font inventory is empty.'
    foreach ($row in $fontRows) {
        $m = [regex]::Match($row, '\s+(yes|no)\s+(yes|no)\s+(yes|no)\s+\d+\s+\d+\s*$')
        Require ($m.Success -and $m.Groups[1].Value -eq 'yes' -and $m.Groups[2].Value -eq 'yes' -and $m.Groups[3].Value -eq 'yes') "PDF font embedding/ToUnicode failure: $row"
    }
    $priorText = Join-Path $scratchFull 'prior-pages-001-477.txt'
    $mergedPrefixText = Join-Path $scratchFull 'merged-pages-001-477.txt'
    $mergedText = Join-Path $scratchFull 'merged-all.txt'
    & $pdftotext '-enc' 'UTF-8' '-f' '1' '-l' '477' $priorPdf $priorText; Assert-Native 'pdftotext CA01 predecessor'
    & $pdftotext '-enc' 'UTF-8' '-f' '1' '-l' '477' $mergedA $mergedPrefixText; Assert-Native 'pdftotext merged predecessor prefix'
    Require ((Digest $priorText) -eq (Digest $mergedPrefixText)) 'Extracted text of CA01 predecessor pages changed.'
    & $pdftotext '-enc' 'UTF-8' $mergedA $mergedText; Assert-Native 'pdftotext merged full'
    $pdfText = [IO.File]::ReadAllText($mergedText)
    $pdfNorm = [regex]::Replace($pdfText, '\s+', ' ').Trim()
    foreach ($required in @('Asesmen Kumulatif 1', 'Petunjuk penguasaan untuk Rute 1–6', 'D60-R01', 'D60-R06', '36 soal', 'CC BY-SA 4.0')) { Require ($pdfNorm.Contains($required)) "Required merged PDF text missing: $required" }
    foreach ($marker in @('C:\Users\', 'github_pat_', 'ghp_', 'access_token', 'FILL_AFTER', 'BEGIN PRIVATE KEY')) { Require (-not $pdfText.Contains($marker)) "Private/transient marker in PDF: $marker" }
    $priorOutline = (& $mutool show $priorPdf outline) -join $lf; Assert-Native 'mutool CA01 predecessor outline'
    $mergedOutline = (& $mutool show $mergedA outline) -join $lf; Assert-Native 'mutool merged hint outline'
    Require ((Count-OutlineRows $priorOutline) -eq 389 -and (Count-OutlineRows $mergedOutline) -eq 396) 'Merged PDF outline census drift.'

    New-Item -ItemType Directory -Path $htmlDir -Force | Out-Null
    New-Item -ItemType Directory -Path (Split-Path -Parent $pdfOut) -Force | Out-Null
    Copy-Item -LiteralPath $htmlA -Destination $htmlOut -Force
    Copy-Item -LiteralPath $mergedA -Destination $pdfOut -Force
    $manifestLines = @('path,bytes,sha256')
    foreach ($artifact in @($htmlOut, $pdfOut)) { $item = Get-Item -LiteralPath $artifact; $manifestLines += "$(Relative $artifact),$($item.Length),$(Digest $artifact)" }
    [IO.File]::WriteAllText($manifestOut, (($manifestLines -join $lf) + $lf), $utf8)

    $evidencePath = Join-Path $scratchFull 'deterministic-build-evidence.json'
    $evidence = [ordered]@{
        status = 'PASS'; source_date_epoch = [int64]$env:SOURCE_DATE_EPOCH; pandoc = $pandocVersion
        html = [ordered]@{ fragment_sha256 = $fragmentHash; combined_bytes = (Get-Item -LiteralPath $htmlOut).Length; combined_sha256 = (Digest $htmlOut); predecessor_exact_reconstruction = $true; predecessor_reconstructed_bytes = (Get-Item -LiteralPath $reconstructedPath).Length; predecessor_reconstructed_sha256 = (Digest $reconstructedPath); dom_ids = $allIds.Count; fragment_links = $allFragments.Count; mathml_nodes = $mathml; hint_stable_ids = 43; hint_blocks = 36; visible_predecessor_links = 72 }
        pdf = [ordered]@{ appendix_bytes = (Get-Item -LiteralPath $appendA).Length; appendix_sha256 = $appendHash; appendix_pages = $appendPages; build_only_hint_paragraph_boundaries = 36; build_only_explicit_stable_id_destinations = 43; build_only_external_named_link_transforms = 72; merged_bytes = (Get-Item -LiteralPath $pdfOut).Length; merged_sha256 = (Digest $pdfOut); merged_pages = $mergedPages; predecessor_pages = 477; predecessor_text_prefix_byte_identical = $true; predecessor_text_prefix_sha256 = (Digest $priorText); fonts = $fontRows.Count; all_fonts_embedded_subset_tounicode = $true; trailer_id_suppressed = $true; predecessor_outline_entries = 389; merged_outline_entries = 396; predecessor_named_destinations = 2873; predecessor_stable_id_destinations_added = 72; merged_named_destinations = 2988; source_stable_id_destinations_added = 43; visible_predecessor_links = 72; merger = 'pypdf 6.12.2 object-copy append; 477-page CA01 outline/name tree preserved; 72 reviewed predecessor stable-ID destinations added; seven source-derived outline entries and all 43 source stable-ID destinations rebuilt; 72 visible predecessor links resolved' }
        qa = [ordered]@{ path = (Relative $sourceQa); bytes = (Get-Item -LiteralPath $sourceQa).Length; sha256 = (Digest $sourceQa) }
        backend_receipt = [ordered]@{ path = (Relative $backendReceipt); bytes = (Get-Item -LiteralPath $backendReceipt).Length; sha256 = (Digest $backendReceipt) }
    }
    [IO.File]::WriteAllText($evidencePath, (($evidence | ConvertTo-Json -Depth 8) + $lf), $utf8)
    & $python '-B' $finalizer '--evidence' $evidencePath; Assert-Native 'Hint reader build finalizer'
    Require (Test-Path -LiteralPath $draftReceipt -PathType Leaf) 'Draft hint build receipt was not written.'
    [ordered]@{ status = 'PASS_DETERMINISTIC_BUILD_PENDING_MANUAL_VISUAL_AND_BROWSER_QA'; html = [ordered]@{ path = (Relative $htmlOut); bytes = (Get-Item -LiteralPath $htmlOut).Length; sha256 = (Digest $htmlOut) }; pdf = [ordered]@{ path = (Relative $pdfOut); bytes = (Get-Item -LiteralPath $pdfOut).Length; sha256 = (Digest $pdfOut); pages = $mergedPages }; manifest = [ordered]@{ path = (Relative $manifestOut); bytes = (Get-Item -LiteralPath $manifestOut).Length; sha256 = (Digest $manifestOut) }; draft_receipt = [ordered]@{ path = (Relative $draftReceipt); bytes = (Get-Item -LiteralPath $draftReceipt).Length; sha256 = (Digest $draftReceipt) } } | ConvertTo-Json -Depth 5
}
finally {
    if (Test-Path -LiteralPath $scratchFull) { Remove-Item -LiteralPath $scratchFull -Recurse -Force }
    Require (-not (Test-Path -LiteralPath $scratchFull)) 'Bounded build scratch removal failed.'
}
