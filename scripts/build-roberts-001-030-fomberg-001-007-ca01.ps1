[CmdletBinding()]
param()

# Deterministic additive build for the sealed Roberts 001-030 + Fomberg
# 001-007 reader followed by the original cumulative assessment D60-CA01.
# The predecessor artifacts are immutable inputs.  This script changes no
# source/backend/control file and writes only its named HTML/PDF/manifest and
# bounded draft build receipt.
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$lane = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$lf = [string][char]10
$utf8 = [Text.UTF8Encoding]::new($false)

$priorHtml = Join-Path $lane 'output\html\roberts-001-030-fomberg-001-007\index.html'
$priorPdf = Join-Path $lane 'output\pdf\topologi-aljabar-roberts-001-030-fomberg-001-007-id.pdf'
$priorManifest = Join-Path $lane 'output\ARTIFACT_MANIFEST_ROBERTS_001_030_FOMBERG_001_007.csv'
$priorReceipt = Join-Path $lane 'qa\ROBERTS_001_030_FOMBERG_001_007_BUILD_RECEIPT.json'
$assessment = Join-Path $lane 'source\id-ID\mastery\cumulative-assessment-001-foundations-coverings-homotopy.md'
$assessmentQa = Join-Path $lane 'qa\CUMULATIVE_ASSESSMENT_001_QA.json'
$backendReceipt = Join-Path $lane 'qa\BACKEND_APPEND_ONLY_CUMULATIVE_ASSESSMENT_001_CUMULATIVE_RECEIPT.json'

$htmlDir = Join-Path $lane 'output\html\roberts-001-030-fomberg-001-007-ca01'
$htmlOut = Join-Path $htmlDir 'index.html'
$pdfOut = Join-Path $lane 'output\pdf\topologi-aljabar-roberts-001-030-fomberg-001-007-ca01-id.pdf'
$manifestOut = Join-Path $lane 'output\ARTIFACT_MANIFEST_ROBERTS_001_030_FOMBERG_001_007_CA01.csv'
$draftReceipt = Join-Path $lane 'qa\ROBERTS_001_030_FOMBERG_001_007_CA01_BUILD_DRAFT.json'
$finalizer = Join-Path $lane 'scripts\finalize-build-roberts-001-030-fomberg-001-007-ca01.py'
$scratch = Join-Path $lane 'tmp\pdfs\roberts-001-030-fomberg-001-007-ca01-build'

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
    Require ($bytes.Length -gt 0) "Empty UTF-8 input: $path"
    Require (-not ($bytes -contains 13)) "CR byte found in LF-only input: $path"
    return $utf8.GetString($bytes)
}

function Read-NormalizedGeneratedUtf8([string]$path) {
    $bytes = [IO.File]::ReadAllBytes($path)
    Require ($bytes.Length -gt 0) "Empty generated UTF-8 input: $path"
    $text = $utf8.GetString($bytes)
    $withoutCrLf = $text.Replace("`r`n", "`n")
    Require (-not $withoutCrLf.Contains("`r")) "Bare CR byte found in generated input: $path"
    return $withoutCrLf
}

function Read-ExactUtf8([string]$path) {
    $bytes = [IO.File]::ReadAllBytes($path)
    Require ($bytes.Length -gt 0) "Empty UTF-8 input: $path"
    return $utf8.GetString($bytes)
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

# Freeze the exact predecessor and the corrected, independently reviewed CA01.
Assert-Identity $priorHtml 14885069 '87d58a5955954125c424ab1220a9c6aa7967a782a9bd739094a31ae0a50af5f6'
Assert-Identity $priorPdf 8326404 '1beca2d03f04c1fcca7eb01bd2654567908febc1ba7941b459c06b90ef865c22'
Assert-Identity $priorManifest 287 '6a5a49c1a7179c27bb21f9bced2517ff38cf79953d566f75eb3143b6a3039aaa'
Assert-Identity $priorReceipt 7042 'bef3d7fbd0aa1290a34f6a942c0559130fd5b32a66531afb7f56d91cb148cc8e'
Assert-Identity $assessment 15185 '5888df0410ad7e8ccf50d8ea8092e43a42f6df94c242f7c09abe0616d972e6f8'
Assert-Identity $assessmentQa 1812 '8dcd7bd124ce16acebef875b8294138caa91801b00d9a621919831bc1f09f602'
Assert-Identity $backendReceipt 9934 '79fc0c7afde5f72b9eaf3809b08ab27cfd696c9d0269905608a1336ae4cd7e13'
Require (Test-Path -LiteralPath $finalizer -PathType Leaf) "Missing build finalizer: $finalizer"
if (Test-Path -LiteralPath $draftReceipt -PathType Leaf) {
    # Never leave an earlier draft apparently current while replacing outputs.
    # Only the finalizer recreates this exact file after all live gates pass.
    Remove-Item -LiteralPath $draftReceipt -Force
}

$qa = Get-Content -LiteralPath $assessmentQa -Raw | ConvertFrom-Json
Require ($qa.status -eq 'PASS') 'CA01 static/review QA is not PASS.'
Require ($qa.qa_id -eq 'O012-D60-CUMULATIVE-ASSESSMENT-001') 'CA01 QA id drift.'
Require ($qa.assessment_id -eq 'D60-CA01' -and $qa.edition_unit_id -eq 'O012-ORIG-CA01') 'CA01 identity drift.'
Require ($qa.reader.identity.path -eq 'source/id-ID/mastery/cumulative-assessment-001-foundations-coverings-homotopy.md') 'CA01 reader path drift.'
Require ([long]$qa.reader.identity.bytes -eq 15185 -and $qa.reader.identity.sha256 -eq '5888df0410ad7e8ccf50d8ea8092e43a42f6df94c242f7c09abe0616d972e6f8') 'CA01 reader identity in QA drifted.'
Require ([int]$qa.reader.stable_ids -eq 34 -and [int]$qa.reader.exercise_hint_solution_triples -eq 8 -and [int]$qa.reader.complete_checked_solutions -eq 8) 'CA01 QA census drift.'
Require ($qa.rights.license -eq 'CC BY-SA 4.0' -and -not [bool]$qa.rights.source_problem_bank_used) 'CA01 rights gate failed.'

$backendText = Read-LfUtf8 $backendReceipt
$backend = $backendText | ConvertFrom-Json
Require ($backend.status -eq 'PASS') 'CA01 cumulative backend receipt is not PASS.'
Require ($backend.receipt_kind -eq 'cumulative_backend_boundary' -and $backend.assessment_id -eq 'D60-CA01' -and $backend.edition_unit_id -eq 'O012-ORIG-CA01') 'CA01 backend semantic identity drift.'
Require ([bool]$backend.immutable_prefix.preserved_exactly -and [int]$backend.immutable_prefix.records -eq 6742 -and [long]$backend.immutable_prefix.bytes -eq 8213649 -and $backend.immutable_prefix.bundle_sha256 -eq '523b570517eb54720c50007aacc5d4eea525ea252b9ca1f6f45b027182354765') 'Exact nested Unit007 backend prefix changed.'
Require ([int]$backend.delta.records -eq 112 -and [long]$backend.delta.bytes -eq 132150 -and $backend.delta.bundle_sha256 -eq '00e682b92f1897fb309eb76c3e9554df3bf65c29d17527d3cc8c0c4181d917d8') 'CA01 backend delta identity drift.'
Require ([int]$backend.cumulative.records -eq 6854 -and [long]$backend.cumulative.bytes -eq 8345799 -and $backend.cumulative.bundle_sha256 -eq '51e75d06e620762e629e9e7408da4b0c32b3e337817d9d140fbbdfa438de2f57') 'CA01 cumulative backend identity drift.'
Require ($backend.replay.status -eq 'PASS' -and [int]$backend.replay.exact_file_matches -eq 11 -and [bool]$backend.replay.temporary_replay_removed) 'CA01 backend replay gate failed.'
Require ([int]$backend.semantic_checks.added_records -eq 112 -and [int]$backend.semantic_checks.segment_kind_counts.assessment -eq 1 -and [int]$backend.semantic_checks.segment_kind_counts.exercise -eq 8 -and [int]$backend.semantic_checks.segment_kind_counts.hint -eq 8 -and [int]$backend.semantic_checks.segment_kind_counts.solution -eq 8 -and $backend.semantic_checks.rights_closure -eq 'PASS' -and $backend.semantic_checks.route_mapping -eq 'PASS') 'CA01 backend semantic census gate failed.'

$scratchFull = [IO.Path]::GetFullPath($scratch)
$allowedScratch = [IO.Path]::GetFullPath((Join-Path $lane 'tmp\pdfs')) + [IO.Path]::DirectorySeparatorChar
Require ($scratchFull.StartsWith($allowedScratch, [StringComparison]::OrdinalIgnoreCase) -and [IO.Path]::GetFileName($scratchFull) -eq 'roberts-001-030-fomberg-001-007-ca01-build') 'Unsafe scratch path.'
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
    $env:SOURCE_DATE_EPOCH = '1787616000'
    $env:FORCE_SOURCE_DATE = '1'

    # Independently convert the assessment twice to a native-MathML fragment.
    $fragmentA = Join-Path $scratchFull 'ca01-a.html'
    $fragmentB = Join-Path $scratchFull 'ca01-b.html'
    $fragmentArgs = @(
        $assessment,
        '--from=markdown+fenced_divs+tex_math_dollars',
        '--to=html5',
        '--mathml',
        '--section-divs',
        '--strip-comments',
        '--fail-if-warnings'
    )
    & $pandoc @fragmentArgs "--output=$fragmentA"; Assert-Native 'Pandoc CA01 HTML fragment A'
    & $pandoc @fragmentArgs "--output=$fragmentB"; Assert-Native 'Pandoc CA01 HTML fragment B'
    $fragmentHashA = Digest $fragmentA
    $fragmentHashB = Digest $fragmentB
    Require ($fragmentHashA -eq $fragmentHashB) "CA01 HTML fragment builds differ: $fragmentHashA != $fragmentHashB"
    # Pandoc on Windows emits CRLF; canonical reader artifacts remain LF-only.
    $fragment = Read-NormalizedGeneratedUtf8 $fragmentA
    Require (-not $fragment.Contains('<html') -and -not $fragment.Contains('<body')) 'CA01 fragment unexpectedly contains a document shell.'

    $sourceText = Read-LfUtf8 $assessment
    $sourceIds = @([regex]::Matches($sourceText, '(?<=#)(o012-d60-ca01(?:-[a-z0-9]+)*)(?=[}\s])') | ForEach-Object { $_.Groups[1].Value })
    Require ($sourceIds.Count -eq 34 -and @($sourceIds | Sort-Object -Unique).Count -eq 34) 'CA01 stable-ID source census drift.'
    $fragmentIds = @([regex]::Matches($fragment, '(?<=\s)id="([^"]+)"') | ForEach-Object { $_.Groups[1].Value })
    $fragmentSet = [Collections.Generic.HashSet[string]]::new([string[]]$fragmentIds)
    Require (@($sourceIds | Where-Object { -not $fragmentSet.Contains($_) }).Count -eq 0) 'A CA01 stable ID is absent from the HTML fragment.'
    Require (([regex]::Matches($fragment, '<math\b')).Count -gt 0) 'CA01 HTML fragment lacks native MathML.'
    Require (-not $fragment.Contains('$') -and -not $fragment.Contains('\(') -and -not $fragment.Contains('\[')) 'CA01 HTML fragment contains a raw math fallback.'

    # Preserve the predecessor bytes as a provably reversible logical prefix.
    $prior = Read-ExactUtf8 $priorHtml
    $htmlNl = if ($prior.Contains("`r`n")) { "`r`n" } else { $lf }
    Require (-not $prior.Replace("`r`n", "").Contains("`r")) 'Predecessor HTML contains a bare CR byte.'
    $oldTitle = '<title>Topologi Aljabar — Roberts 30/30 dan Fomberg 1.1–1.13</title>'
    $newTitle = '<title>Topologi Aljabar — Roberts 30/30, Fomberg 1.1–1.13, dan Asesmen Kumulatif 1</title>'
    $oldHeading = '<h1 class="title">Topologi Aljabar — Roberts 30/30 dan Fomberg' + $htmlNl + '1.1–1.13</h1>'
    $newHeading = '<h1 class="title">Topologi Aljabar — Roberts 30/30, Fomberg' + $htmlNl + '1.1–1.13, dan Asesmen Kumulatif 1</h1>'
    $oldSubtitle = '<p class="subtitle">Komponen Roberts lengkap; jembatan Fomberg melalui' + $htmlNl + 'homologi seluler; checkpoint komposit parsial</p>'
    $newSubtitle = '<p class="subtitle">Komponen Roberts lengkap; jembatan Fomberg melalui' + $htmlNl + 'homologi seluler; Asesmen Kumulatif 1; checkpoint komposit parsial</p>'
    foreach ($needle in @($oldTitle, $oldHeading, $oldSubtitle)) {
        Require ($prior.IndexOf($needle, [StringComparison]::Ordinal) -ge 0 -and $prior.LastIndexOf($needle, [StringComparison]::Ordinal) -eq $prior.IndexOf($needle, [StringComparison]::Ordinal)) "Predecessor HTML replacement anchor missing/duplicated: $needle"
    }
    $combined = $prior.Replace($oldTitle, $newTitle).Replace($oldHeading, $newHeading).Replace($oldSubtitle, $newSubtitle)

    $navClose = $htmlNl + '</ul>' + $htmlNl + '</nav>'
    $navPos = $combined.LastIndexOf($navClose, [StringComparison]::Ordinal)
    Require ($navPos -gt 0) 'Top-level ToC close anchor missing.'
    $tocInsert = $htmlNl + '<li><a href="#o012-d60-ca01" id="toc-o012-d60-ca01">Asesmen Kumulatif 1 — fondasi hingga barisan eksak homotopi</a></li>'
    $combined = $combined.Insert($navPos, $tocInsert)

    $statusStart = $combined.IndexOf('<section id="o012-composite-status"', [StringComparison]::Ordinal)
    $statusEnd = $combined.IndexOf($htmlNl + '</section>', $statusStart, [StringComparison]::Ordinal)
    Require ($statusStart -ge 0 -and $statusEnd -gt $statusStart) 'Composite status section anchor missing.'
    $statusInsert = $htmlNl + '<aside id="o012-d60-ca01-status" class="note" data-origin="edition-original">' + $htmlNl +
        '<p><strong>Tambahan checkpoint.</strong> Pembaca ini kini juga memuat Asesmen Kumulatif 1 (D60-CA01): delapan soal asli edisi, delapan petunjuk, dan delapan solusi lengkap untuk D60-R01–D60-R07. Lapisan ini berlisensi CC BY-SA 4.0, tidak berasal dari bank masalah Fomberg, dan tidak mengubah urutan maupun penomoran komponen Roberts atau Fomberg.</p>' + $htmlNl + '</aside>'
    $combined = $combined.Insert($statusEnd, $statusInsert)

    $bodyClose = $htmlNl + '</body>'
    $bodyPos = $combined.LastIndexOf($bodyClose, [StringComparison]::Ordinal)
    Require ($bodyPos -gt 0) 'HTML body close anchor missing.'
    $fragmentForDocument = if ($htmlNl -eq "`r`n") { $fragment.Replace($lf, "`r`n") } else { $fragment }
    $fragmentInsert = $htmlNl + $fragmentForDocument.TrimEnd([char]13, [char]10)
    $combined = $combined.Insert($bodyPos, $fragmentInsert)

    # Reverse only the declared additive edits and prove exact predecessor bytes.
    $reconstructed = $combined
    $fragmentPos = $reconstructed.LastIndexOf($fragmentInsert, [StringComparison]::Ordinal)
    Require ($fragmentPos -ge 0) 'Cannot reverse CA01 fragment insertion.'
    $reconstructed = $reconstructed.Remove($fragmentPos, $fragmentInsert.Length)
    $statusPos = $reconstructed.IndexOf($statusInsert, [StringComparison]::Ordinal)
    Require ($statusPos -ge 0) 'Cannot reverse status insertion.'
    $reconstructed = $reconstructed.Remove($statusPos, $statusInsert.Length)
    $tocPos = $reconstructed.IndexOf($tocInsert, [StringComparison]::Ordinal)
    Require ($tocPos -ge 0) 'Cannot reverse ToC insertion.'
    $reconstructed = $reconstructed.Remove($tocPos, $tocInsert.Length)
    $reconstructed = $reconstructed.Replace($newTitle, $oldTitle).Replace($newHeading, $oldHeading).Replace($newSubtitle, $oldSubtitle)
    $reconstructedBytes = $utf8.GetBytes($reconstructed)
    $reconstructedPath = Join-Path $scratchFull 'reconstructed-unit007.html'
    [IO.File]::WriteAllBytes($reconstructedPath, $reconstructedBytes)
    Require ($reconstructedBytes.Length -eq 14885069 -and (Digest $reconstructedPath) -eq '87d58a5955954125c424ab1220a9c6aa7967a782a9bd739094a31ae0a50af5f6') 'Logical-prefix reconstruction does not recover exact Unit007 HTML bytes.'

    $htmlA = Join-Path $scratchFull 'combined-a.html'
    $htmlB = Join-Path $scratchFull 'combined-b.html'
    [IO.File]::WriteAllText($htmlA, $combined, $utf8)
    [IO.File]::WriteAllText($htmlB, $combined, $utf8)
    Require ((Digest $htmlA) -eq (Digest $htmlB)) 'Combined HTML writes are not byte-identical.'

    $allIds = @([regex]::Matches($combined, '(?<=\s)id="([^"]+)"') | ForEach-Object { $_.Groups[1].Value })
    Require (@($allIds | Group-Object | Where-Object Count -gt 1).Count -eq 0) 'Combined HTML has duplicate IDs.'
    $idSet = [Collections.Generic.HashSet[string]]::new([string[]]$allIds)
    $fragments = @([regex]::Matches($combined, '\bhref="#([^"]+)"') | ForEach-Object { $_.Groups[1].Value })
    Require (@($fragments | Sort-Object -Unique | Where-Object { -not $idSet.Contains($_) }).Count -eq 0) 'Combined HTML has an unresolved fragment link.'
    $mathml = ([regex]::Matches($combined, '<math\b')).Count
    Require ($mathml -gt 15945) 'Combined HTML MathML census did not grow.'
    $exerciseCount = ([regex]::Matches($fragment, 'class="[^"]*\bexercise\b[^"]*"')).Count
    $hintCount = ([regex]::Matches($fragment, 'class="[^"]*\bhint\b[^"]*"')).Count
    $solutionCount = ([regex]::Matches($fragment, 'class="[^"]*\bsolution\b[^"]*"')).Count
    Require ((@($exerciseCount, $hintCount, $solutionCount) -join ',') -eq '8,8,8') "CA01 HTML mastery census mismatch: $exerciseCount,$hintCount,$solutionCount"
    Require ($combined.Contains($newTitle) -and $combined.Contains('Tambahan checkpoint.') -and $combined.Contains('id="toc-o012-d60-ca01"')) 'HTML title/status/ToC update missing.'
    Require ($combined -match '<html[^>]+lang="id-ID"' -and $combined -notmatch '(?is)<(?:script|link)\b[^>]*(?:src|href)\s*=' -and $combined -notmatch '(?is)<img\b[^>]*\bsrc\s*=\s*[''\"]https?://') 'Combined HTML language/self-contained gate failed.'
    foreach ($cssMarker in @('width: min(100%, 72rem)', 'max-width: 72rem', 'margin-inline: auto', '@media (max-width: 700px)', 'math[display="block"]', 'math[display="inline"]')) {
        Require ($combined.Contains($cssMarker)) "Responsive CSS marker missing: $cssMarker"
    }
    foreach ($marker in @('C:\Users\', 'github_pat_', 'ghp_', 'access_token', 'FILL_AFTER', 'BEGIN PRIVATE KEY')) {
        Require (-not $combined.Contains($marker)) "Private/transient marker in HTML: $marker"
    }

    # Build only the additive CA01 PDF twice with a fixed epoch and no trailer ID.
    $pdfHeader = Join-Path $scratchFull 'ca01-header.tex'
    [IO.File]::WriteAllText($pdfHeader, ("\AddToHook{begindocument/end}{\pdftrailerid{}}$lf"), $utf8)
    # Pandoc emits a \phantomsection label for each fenced exercise div.  When
    # that label immediately follows a subsection heading, LaTeX consumes the
    # heading's after-skip and runs the prompt into the heading line.  Insert a
    # build-only paragraph boundary after each of the eight exercise anchors;
    # canonical source prose, IDs, order, and mathematics remain untouched.
    $assessmentPdf = Join-Path $scratchFull 'ca01-pdf-layout.md'
    $assessmentPdfText = Read-LfUtf8 $assessment
    $exerciseOpen = [regex]::new('(?m)^(::: \{\.exercise[^\r\n]*\})$')
    Require ($exerciseOpen.Matches($assessmentPdfText).Count -eq 8) 'CA01 exercise-anchor layout-transform census drift.'
    $layoutBoundary = '$1' + $lf + $lf + '```{=latex}' + $lf + '\par\noindent' + $lf + '```'
    $assessmentPdfText = $exerciseOpen.Replace($assessmentPdfText, $layoutBoundary)
    [IO.File]::WriteAllText($assessmentPdf, $assessmentPdfText, $utf8)
    $caPdfWork = Join-Path $scratchFull 'ca01-work.pdf'
    $caPdfA = Join-Path $scratchFull 'ca01-a.pdf'
    $caPdfB = Join-Path $scratchFull 'ca01-b.pdf'
    $pdfArgs = @(
        $assessmentPdf,
        '--from=markdown+fenced_divs+tex_math_dollars',
        '--standalone',
        '--number-sections',
        '--strip-comments',
        '--metadata=lang:id-ID',
        '--metadata=pagetitle:Asesmen Kumulatif 1 — Topologi Dasar, Ruang Penutup, dan Homotopi',
        '--metadata=date:26 Agustus 2026',
        '--pdf-engine=pdflatex',
        "--include-in-header=$pdfHeader",
        '--variable=papersize:a4',
        '--variable=geometry:margin=21mm',
        '--variable=fontsize:11pt',
        '--variable=colorlinks:true',
        '--variable=linkcolor:blue',
        '--variable=pdf-trailer-id:'
    )
    & $pandoc @pdfArgs "--output=$caPdfWork"; Assert-Native 'Pandoc CA01 PDF A'
    Copy-Item -LiteralPath $caPdfWork -Destination $caPdfA -Force
    & $pandoc @pdfArgs "--output=$caPdfWork"; Assert-Native 'Pandoc CA01 PDF B'
    Copy-Item -LiteralPath $caPdfWork -Destination $caPdfB -Force
    $caPdfHashA = Digest $caPdfA
    $caPdfHashB = Digest $caPdfB
    Require ($caPdfHashA -eq $caPdfHashB) "CA01 PDF builds differ: $caPdfHashA != $caPdfHashB"
    $caInfo = (& $pdfinfo $caPdfA) -join $lf; Assert-Native 'pdfinfo CA01'
    Require ($caInfo -match '(?m)^Pages:\s+5\s*$' -and $caInfo -match '(?m)^Page size:.*\(A4\)\s*$' -and $caInfo -match '(?m)^Tagged:\s+no\s*$' -and $caInfo -match '(?m)^Encrypted:\s+no\s*$') 'CA01 PDF metadata/page gate failed.'
    $caTrailer = (& $mutool show $caPdfA trailer) -join $lf; Assert-Native 'mutool CA01 trailer'
    Require ($caTrailer -notmatch '(?m)^\s*/ID\s') 'CA01 PDF trailer unexpectedly contains /ID.'

    # Append through pypdf's deterministic object-copy path. Unlike mutool
    # merge, this preserves the predecessor name tree, imports both outlines,
    # and rewrites their destinations to explicit live page references.
    $mergedA = Join-Path $scratchFull 'combined-a.pdf'
    $mergedB = Join-Path $scratchFull 'combined-b.pdf'
    & $python '-B' $finalizer '--merge-pdfs' '--prior' $priorPdf '--append' $caPdfA '--output' $mergedA; Assert-Native 'pypdf deterministic merge A'
    & $python '-B' $finalizer '--merge-pdfs' '--prior' $priorPdf '--append' $caPdfB '--output' $mergedB; Assert-Native 'pypdf deterministic merge B'
    $mergedHashA = Digest $mergedA
    $mergedHashB = Digest $mergedB
    Require ($mergedHashA -eq $mergedHashB) "Merged PDF builds differ: $mergedHashA != $mergedHashB"
    $mergedInfo = (& $pdfinfo $mergedA) -join $lf; Assert-Native 'pdfinfo merged PDF'
    Require ($mergedInfo -match '(?m)^Pages:\s+477\s*$' -and $mergedInfo -match '(?m)^Page size:.*\(A4\)\s*$' -and $mergedInfo -match '(?m)^Tagged:\s+no\s*$' -and $mergedInfo -match '(?m)^Encrypted:\s+no\s*$') 'Merged PDF metadata/page gate failed.'
    $mergedTrailer = (& $mutool show $mergedA trailer) -join $lf; Assert-Native 'mutool merged trailer'
    Require ($mergedTrailer -notmatch '(?m)^\s*/ID\s') 'Merged PDF trailer unexpectedly contains /ID.'

    $fontRows = @((& $pdffonts $mergedA) | Select-Object -Skip 2 | Where-Object { $_.Trim().Length -gt 0 }); Assert-Native 'pdffonts merged PDF'
    Require ($fontRows.Count -gt 0) 'Merged PDF font inventory is empty.'
    foreach ($row in $fontRows) {
        $m = [regex]::Match($row, '\s+(yes|no)\s+(yes|no)\s+(yes|no)\s+\d+\s+\d+\s*$')
        Require ($m.Success -and $m.Groups[1].Value -eq 'yes' -and $m.Groups[2].Value -eq 'yes' -and $m.Groups[3].Value -eq 'yes') "PDF font embedding/ToUnicode failure: $row"
    }

    $priorText = Join-Path $scratchFull 'prior-pages-001-472.txt'
    $mergedPrefixText = Join-Path $scratchFull 'merged-pages-001-472.txt'
    $mergedAllText = Join-Path $scratchFull 'merged-all.txt'
    & $pdftotext '-enc' 'UTF-8' '-f' '1' '-l' '472' $priorPdf $priorText; Assert-Native 'pdftotext predecessor prefix'
    & $pdftotext '-enc' 'UTF-8' '-f' '1' '-l' '472' $mergedA $mergedPrefixText; Assert-Native 'pdftotext merged prefix'
    Require ((Digest $priorText) -eq (Digest $mergedPrefixText)) 'Extracted text of predecessor pages changed after merge.'
    & $pdftotext '-enc' 'UTF-8' $mergedA $mergedAllText; Assert-Native 'pdftotext merged full'
    $pdfText = [IO.File]::ReadAllText($mergedAllText)
    $pdfNorm = [regex]::Replace($pdfText, '\s+', ' ').Trim()
    foreach ($required in @('Roberts lengkap 30/30', 'Fomberg O012-FOM-007', 'Asesmen Kumulatif 1', 'Soal 8', 'Peta cakupan asesmen', 'delapan soal', 'CC BY-SA 4.0')) {
        Require ($pdfNorm.Contains($required)) "Required merged PDF text missing: $required"
    }
    foreach ($marker in @('C:\Users\', 'github_pat_', 'ghp_', 'access_token', 'FILL_AFTER', 'BEGIN PRIVATE KEY')) {
        Require (-not $pdfText.Contains($marker)) "Private/transient marker in PDF: $marker"
    }

    $priorOutlineText = (& $mutool show $priorPdf outline) -join $lf; Assert-Native 'mutool predecessor outline'
    $mergedOutlineText = (& $mutool show $mergedA outline) -join $lf; Assert-Native 'mutool merged outline'
    $priorOutlineCount = Count-OutlineRows $priorOutlineText
    $mergedOutlineCount = Count-OutlineRows $mergedOutlineText

    New-Item -ItemType Directory -Path $htmlDir -Force | Out-Null
    New-Item -ItemType Directory -Path (Split-Path -Parent $pdfOut) -Force | Out-Null
    Copy-Item -LiteralPath $htmlA -Destination $htmlOut -Force
    Copy-Item -LiteralPath $mergedA -Destination $pdfOut -Force

    $manifestLines = @('path,bytes,sha256')
    foreach ($artifact in @($htmlOut, $pdfOut)) {
        $item = Get-Item -LiteralPath $artifact
        $manifestLines += "$(Relative $artifact),$($item.Length),$(Digest $artifact)"
    }
    [IO.File]::WriteAllText($manifestOut, (($manifestLines -join $lf) + $lf), $utf8)

    $evidencePath = Join-Path $scratchFull 'deterministic-build-evidence.json'
    $evidence = [ordered]@{
        status = 'PASS'
        source_date_epoch = [int64]$env:SOURCE_DATE_EPOCH
        pandoc = $pandocVersion
        html = [ordered]@{
            fragment_builds_byte_identical = $true
            fragment_bytes = (Get-Item -LiteralPath $fragmentA).Length
            fragment_sha256 = $fragmentHashA
            combined_builds_byte_identical = $true
            combined_bytes = (Get-Item -LiteralPath $htmlOut).Length
            combined_sha256 = (Digest $htmlOut)
            predecessor_exact_reconstruction = $true
            predecessor_reconstructed_bytes = $reconstructedBytes.Length
            predecessor_reconstructed_sha256 = (Digest $reconstructedPath)
            dom_ids = $allIds.Count
            fragment_links = $fragments.Count
            mathml_nodes = $mathml
            ca01_stable_ids = $sourceIds.Count
            ca01_exercises = $exerciseCount
            ca01_hints = $hintCount
            ca01_solutions = $solutionCount
        }
        pdf = [ordered]@{
            ca01_builds_byte_identical = $true
            ca01_bytes = (Get-Item -LiteralPath $caPdfA).Length
            ca01_sha256 = $caPdfHashA
            ca01_pages = 5
            build_only_exercise_paragraph_boundaries = 8
            merged_builds_byte_identical = $true
            merged_bytes = (Get-Item -LiteralPath $pdfOut).Length
            merged_sha256 = (Digest $pdfOut)
            merged_pages = 477
            predecessor_pages = 472
            predecessor_text_prefix_byte_identical = $true
            predecessor_text_prefix_sha256 = (Digest $priorText)
            fonts = $fontRows.Count
            all_fonts_embedded_subset_tounicode = $true
            trailer_id_suppressed = $true
            predecessor_outline_entries = $priorOutlineCount
            merged_outline_entries = $mergedOutlineCount
            predecessor_outline_prefix_expected = ($priorOutlineCount -eq 379 -and $mergedOutlineCount -eq 389)
            merger = 'pypdf 6.12.2 object-copy append; predecessor outline/name tree preserved; 10 CA01 outline destinations rebuilt explicitly against appended pages'
        }
        backend_receipt = [ordered]@{ path = (Relative $backendReceipt); bytes = (Get-Item -LiteralPath $backendReceipt).Length; sha256 = (Digest $backendReceipt) }
    }
    [IO.File]::WriteAllText($evidencePath, (($evidence | ConvertTo-Json -Depth 8) + $lf), $utf8)

    & $python '-B' $finalizer '--evidence' $evidencePath; Assert-Native 'CA01 build finalizer'
    Require (Test-Path -LiteralPath $draftReceipt -PathType Leaf) 'Draft build receipt was not written.'

    [ordered]@{
        status = 'PASS_DETERMINISTIC_BUILD_PENDING_MANUAL_VISUAL_AND_BROWSER_QA'
        html = [ordered]@{ path = (Relative $htmlOut); bytes = (Get-Item -LiteralPath $htmlOut).Length; sha256 = (Digest $htmlOut) }
        pdf = [ordered]@{ path = (Relative $pdfOut); bytes = (Get-Item -LiteralPath $pdfOut).Length; sha256 = (Digest $pdfOut); pages = 477 }
        manifest = [ordered]@{ path = (Relative $manifestOut); bytes = (Get-Item -LiteralPath $manifestOut).Length; sha256 = (Digest $manifestOut) }
        draft_receipt = [ordered]@{ path = (Relative $draftReceipt); bytes = (Get-Item -LiteralPath $draftReceipt).Length; sha256 = (Digest $draftReceipt) }
    } | ConvertTo-Json -Depth 5
}
finally {
    if (Test-Path -LiteralPath $scratchFull) {
        Remove-Item -LiteralPath $scratchFull -Recurse -Force
    }
    Require (-not (Test-Path -LiteralPath $scratchFull)) 'Bounded build scratch removal failed.'
}
