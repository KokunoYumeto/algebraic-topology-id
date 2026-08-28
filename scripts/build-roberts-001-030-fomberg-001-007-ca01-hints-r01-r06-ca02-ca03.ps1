[CmdletBinding()]
param()

# Deterministic additive build: frozen 482-page ordinary-mastery reader plus
# the two original eight-item cumulative assessments D60-CA02 and D60-CA03.
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$script:LASTEXITCODE = 0

$lane = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$lf = [string][char]10
$utf8 = [Text.UTF8Encoding]::new($false)
$priorHtml = Join-Path $lane 'output\html\roberts-001-030-fomberg-001-007-ca01-hints-r01-r06\index.html'
$priorPdf = Join-Path $lane 'output\pdf\topologi-aljabar-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-id.pdf'
$sourceA = Join-Path $lane 'source\id-ID\mastery\cumulative-assessment-002-homology-excision-cellular.md'
$sourceB = Join-Path $lane 'source\id-ID\mastery\cumulative-assessment-003-cohomology-degree-synthesis.md'
$sourceQa = Join-Path $lane 'qa\CUMULATIVE_ASSESSMENTS_002_003_QA.json'
$backendReceipt = Join-Path $lane 'qa\BACKEND_APPEND_ONLY_CUMULATIVE_ASSESSMENTS_002_003_CUMULATIVE_RECEIPT.json'
$merger = Join-Path $lane 'scripts\merge-cumulative-assessments-002-003.py'
$htmlDir = Join-Path $lane 'output\html\roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03'
$htmlOut = Join-Path $htmlDir 'index.html'
$pdfOut = Join-Path $lane 'output\pdf\topologi-aljabar-roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-id.pdf'
$manifestOut = Join-Path $lane 'output\ARTIFACT_MANIFEST_ROBERTS_001_030_FOMBERG_001_007_CA01_HINTS_R01_R06_CA02_CA03.csv'
$draftReceipt = Join-Path $lane 'qa\ROBERTS_001_030_FOMBERG_001_007_CA01_HINTS_R01_R06_CA02_CA03_BUILD_DRAFT.json'
$scratch = Join-Path $lane 'tmp\pdfs\roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-build'

function Require([bool]$condition, [string]$message) { if (-not $condition) { throw $message } }
function Digest([string]$path) { return (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() }
function Assert-Identity([string]$path, [long]$bytes, [string]$sha256) {
    Require (Test-Path -LiteralPath $path -PathType Leaf) "Missing frozen input: $path"
    $item = Get-Item -LiteralPath $path
    Require ($item.Length -eq $bytes -and (Digest $path) -eq $sha256) "Frozen identity mismatch: $path"
}
function Read-LfUtf8([string]$path) {
    $raw = [IO.File]::ReadAllBytes($path)
    Require ($raw.Length -gt 0 -and -not ($raw -contains 13)) "Expected nonempty LF-only UTF-8: $path"
    return $utf8.GetString($raw)
}
function Read-GeneratedUtf8([string]$path) {
    $text = $utf8.GetString([IO.File]::ReadAllBytes($path)).Replace("`r`n", "`n")
    Require (-not $text.Contains("`r")) "Generated file contains bare CR: $path"
    return $text
}
function Relative([string]$path) {
    $full = [IO.Path]::GetFullPath($path)
    $prefix = $lane.TrimEnd([IO.Path]::DirectorySeparatorChar) + [IO.Path]::DirectorySeparatorChar
    Require ($full.StartsWith($prefix, [StringComparison]::OrdinalIgnoreCase)) "Path outside lane: $full"
    return $full.Substring($prefix.Length).Replace('\', '/')
}
function Assert-Native([string]$name) { if ($LASTEXITCODE -ne 0) { throw "$name failed with exit code $LASTEXITCODE" } }
function Count-OutlineRows([string]$text) { return @(($text -split $lf) | Where-Object { $_ -match '^(?:\+|\||-)' }).Count }
function Digest-Lines([string[]]$values) {
    $hasher = [Security.Cryptography.SHA256]::Create()
    try {
        $bytes = $utf8.GetBytes((($values -join $lf) + $lf))
        return ([BitConverter]::ToString($hasher.ComputeHash($bytes))).Replace('-', '').ToLowerInvariant()
    }
    finally { $hasher.Dispose() }
}
function Render-Prefix([string]$pdf, [string]$directory, [int]$pages, [string]$renderer) {
    Require (-not (Test-Path -LiteralPath $directory)) "Render scratch exists: $directory"
    New-Item -ItemType Directory -Path $directory | Out-Null
    $pattern = Join-Path $directory 'page-%03d.png'
    & $renderer 'draw' '-q' '-F' 'png' '-r' '72' '-c' 'rgb' '-A' '8' '-o' $pattern $pdf "1-$pages" | Out-Null
    Assert-Native "mutool render $pdf"
    $files = @(Get-ChildItem -LiteralPath $directory -File -Filter 'page-*.png' | Sort-Object Name)
    Require ($files.Count -eq $pages) "Rendered page census drift for $pdf"
    $hashes = @()
    for ($index = 0; $index -lt $files.Count; $index++) {
        $expectedName = 'page-{0:D3}.png' -f ($index + 1)
        Require ($files[$index].Name -eq $expectedName) "Rendered page filename drift: $($files[$index].Name)"
        $hashes += Digest $files[$index].FullName
    }
    return [pscustomobject]@{ page_sha256=$hashes; aggregate_sha256=(Digest-Lines $hashes) }
}
function Prepare-AtomicPromotion([string]$source, [string]$destination, [string]$transaction, [string]$scratchRoot) {
    Require (Test-Path -LiteralPath $source -PathType Leaf) "Missing staged artifact: $source"
    $sourceFull = [IO.Path]::GetFullPath($source)
    $scratchPrefix = $scratchRoot.TrimEnd([IO.Path]::DirectorySeparatorChar) + [IO.Path]::DirectorySeparatorChar
    Require ($sourceFull.StartsWith($scratchPrefix, [StringComparison]::OrdinalIgnoreCase)) "Promotion source is outside scratch: $sourceFull"
    $destinationFull = [IO.Path]::GetFullPath($destination)
    Relative $destinationFull | Out-Null
    $parent = Split-Path -Parent $destinationFull
    New-Item -ItemType Directory -Path $parent -Force | Out-Null
    $leaf = [IO.Path]::GetFileName($destinationFull)
    $pending = Join-Path $parent ".$leaf.$transaction.pending"
    $backup = Join-Path $parent ".$leaf.$transaction.rollback"
    Require (-not (Test-Path -LiteralPath $pending) -and -not (Test-Path -LiteralPath $backup)) "Atomic promotion temporary path collision for $destinationFull"
    [IO.File]::Copy($sourceFull, $pending, $false)
    Require ((Get-Item -LiteralPath $pending).Length -eq (Get-Item -LiteralPath $sourceFull).Length -and (Digest $pending) -eq (Digest $sourceFull)) "Staged promotion copy mismatch: $destinationFull"
    $hadExisting = Test-Path -LiteralPath $destinationFull -PathType Leaf
    if ($hadExisting) { [IO.File]::Copy($destinationFull, $backup, $false) }
    return [pscustomobject]@{ source=$sourceFull; destination=$destinationFull; pending=$pending; backup=$backup; had_existing=$hadExisting }
}
function Commit-AtomicPromotions([object[]]$entries) {
    $promoted = @()
    try {
        foreach ($entry in $entries) {
            if ($entry.had_existing) { [IO.File]::Replace($entry.pending, $entry.destination, $null, $true) }
            else { [IO.File]::Move($entry.pending, $entry.destination) }
            $promoted += $entry
        }
        foreach ($entry in $entries) {
            Require ((Get-Item -LiteralPath $entry.destination).Length -eq (Get-Item -LiteralPath $entry.source).Length -and (Digest $entry.destination) -eq (Digest $entry.source)) "Promoted artifact identity mismatch: $($entry.destination)"
        }
    }
    catch {
        $failure = $_
        $rollbackFailures = @()
        for ($index = $promoted.Count - 1; $index -ge 0; $index--) {
            $entry = $promoted[$index]
            try {
                if ($entry.had_existing) {
                    if (Test-Path -LiteralPath $entry.destination -PathType Leaf) { [IO.File]::Replace($entry.backup, $entry.destination, $null, $true) }
                    else { [IO.File]::Move($entry.backup, $entry.destination) }
                }
                elseif (Test-Path -LiteralPath $entry.destination -PathType Leaf) { [IO.File]::Delete($entry.destination) }
            }
            catch { $rollbackFailures += "$($entry.destination): $($_.Exception.Message)" }
        }
        if ($rollbackFailures.Count -gt 0) { throw "Atomic promotion failed and rollback was incomplete: $($rollbackFailures -join '; '). Original failure: $($failure.Exception.Message)" }
        foreach ($entry in $entries) { if (Test-Path -LiteralPath $entry.backup -PathType Leaf) { [IO.File]::Delete($entry.backup) } }
        throw $failure
    }
    foreach ($entry in $entries) { if (Test-Path -LiteralPath $entry.backup -PathType Leaf) { [IO.File]::Delete($entry.backup) } }
}

Assert-Identity $priorHtml 15026881 '7ed278d73a324ba0a9e5acadedf448221b3791db7322fdf6d29225afd0124d2b'
Assert-Identity $priorPdf 8592243 '4da7f1368c17423cd6845c36b7d5190dac98d515ecbd32467c0c59961dd9afcb'
foreach ($required in @($sourceA, $sourceB, $sourceQa, $backendReceipt, $merger)) { Require (Test-Path -LiteralPath $required -PathType Leaf) "Missing required input: $required" }
$qaRaw = Read-LfUtf8 $sourceQa
$qa = $qaRaw | ConvertFrom-Json
Require ($qa.status -eq 'PASS' -and $qa.cumulative_items_added -eq 16 -and $qa.exercise_hint_solution_triples -eq 16 -and $qa.complete_checked_solutions -eq 16 -and $qa.mastery_postcondition.total -eq 108) 'CA02/CA03 source QA gate failed.'
$qaBindings = @(@('D60-CA02', $sourceA), @('D60-CA03', $sourceB))
foreach ($binding in $qaBindings) {
    $assessmentId = $binding[0]; $source = $binding[1]
    $rows = @($qa.assessments | Where-Object { $_.assessment_id -eq $assessmentId })
    Require ($rows.Count -eq 1) "QA source binding missing/duplicated: $assessmentId"
    $identity = $rows[0].reader.identity
    $sourceItem = Get-Item -LiteralPath $source
    Require ($identity.path -eq (Relative $source) -and [long]$identity.bytes -eq $sourceItem.Length -and $identity.sha256 -eq (Digest $source)) "QA source identity mismatch: $assessmentId"
}
$backendRaw = Read-LfUtf8 $backendReceipt
$backend = $backendRaw | ConvertFrom-Json
Require ($backend.status -eq 'PASS' -and $backend.receipt_kind -eq 'cumulative_backend_boundary') 'CA02/CA03 cumulative backend gate failed.'
Require ($backend.immutable_prefix.preserved_exactly -eq $true -and $backend.immutable_prefix.records -eq 7012 -and $backend.immutable_prefix.bytes -eq 8545732 -and $backend.immutable_prefix.bundle_sha256 -eq '7d723f9ef163303c7dde63d646dc8d5917c2450b1da5d24c87ef77bf4e4d664b') 'CA02/CA03 backend prefix gate failed.'
Require ($backend.replay.status -eq 'PASS' -and $backend.replay.exact_file_matches -eq 11 -and $backend.replay.temporary_replay_removed -eq $true) 'CA02/CA03 backend replay gate failed.'
$sourceTextA = Read-LfUtf8 $sourceA
$sourceTextB = Read-LfUtf8 $sourceB
foreach ($pair in @(@($sourceTextA, 'ca02'), @($sourceTextB, 'ca03'))) {
    $text = $pair[0]; $token = $pair[1]
    $ids = @([regex]::Matches($text, "(?<=#)(o012-d60-$token(?:-[a-z0-9]+)*)(?=[}\s])") | ForEach-Object { $_.Groups[1].Value })
    Require ($ids.Count -eq 34 -and @($ids | Sort-Object -Unique).Count -eq 34) "$token stable-ID census drift."
    foreach ($kind in @('exercise', 'hint', 'solution')) { Require (([regex]::Matches($text, "(?m)^::: \{\.$kind #o012-d60-$token-")).Count -eq 8) "$token $kind census drift." }
}

$scratchFull = [IO.Path]::GetFullPath($scratch)
$allowedScratch = [IO.Path]::GetFullPath((Join-Path $lane 'tmp\pdfs')) + [IO.Path]::DirectorySeparatorChar
Require ($scratchFull.StartsWith($allowedScratch, [StringComparison]::OrdinalIgnoreCase) -and [IO.Path]::GetFileName($scratchFull) -eq 'roberts-001-030-fomberg-001-007-ca01-hints-r01-r06-ca02-ca03-build') 'Unsafe scratch path.'
Require (-not (Test-Path -LiteralPath $scratchFull)) "Bounded scratch exists: $scratchFull"
New-Item -ItemType Directory -Path $scratchFull | Out-Null
$promotionTemps = @()

try {
    $pandoc = (Get-Command pandoc -ErrorAction Stop).Source
    $mutool = (Get-Command mutool -ErrorAction Stop).Source
    $pdfinfo = (Get-Command pdfinfo -ErrorAction Stop).Source
    $pdffonts = (Get-Command pdffonts -ErrorAction Stop).Source
    $pdftotext = (Get-Command pdftotext -ErrorAction Stop).Source
    $python = (Get-Command python -ErrorAction Stop).Source
    $pandocVersion = (& $pandoc --version | Select-Object -First 1)
    Require ($pandocVersion -eq 'pandoc 3.9.0.2') "Expected pandoc 3.9.0.2; got $pandocVersion"
    $mutoolVersion = ((& $mutool -v 2>&1 | Select-Object -First 1).ToString()).Trim()
    Assert-Native 'mutool version'
    Require ($mutoolVersion -eq 'mutool version 1.23.0') "Expected mutool 1.23.0; got $mutoolVersion"
    $env:SOURCE_DATE_EPOCH = '1787788800'
    $env:FORCE_SOURCE_DATE = '1'

    $fragments = @()
    foreach ($spec in @(@($sourceA, 'ca02'), @($sourceB, 'ca03'))) {
        $source = $spec[0]; $token = $spec[1]
        $a = Join-Path $scratchFull "$token-a.html"; $b = Join-Path $scratchFull "$token-b.html"
        $args = @($source, '--from=markdown+fenced_divs+tex_math_dollars', '--to=html5', '--mathml', '--section-divs', '--strip-comments', '--fail-if-warnings')
        & $pandoc @args "--output=$a"; Assert-Native "Pandoc $token HTML A"
        & $pandoc @args "--output=$b"; Assert-Native "Pandoc $token HTML B"
        Require ((Digest $a) -eq (Digest $b)) "$token HTML fragment builds differ."
        $fragment = Read-GeneratedUtf8 $a
        Require (-not $fragment.Contains('<html') -and -not $fragment.Contains('<body')) "$token fragment unexpectedly has shell."
        Require (([regex]::Matches($fragment, 'class="[^"]*\bexercise\b')).Count -eq 8 -and ([regex]::Matches($fragment, 'class="[^"]*\bhint\b')).Count -eq 8 -and ([regex]::Matches($fragment, 'class="[^"]*\bsolution\b')).Count -eq 8) "$token fragment triple census drift."
        Require (([regex]::Matches($fragment, '<math\b')).Count -gt 0 -and -not $fragment.Contains('$')) "$token fragment math conversion failed."
        $fragments += [pscustomobject]@{ token=$token; text=$fragment; sha256=(Digest $a) }
    }

    $prior = [IO.File]::ReadAllText($priorHtml, $utf8)
    $htmlNl = if ($prior.Contains("`r`n")) { "`r`n" } else { $lf }
    Require (-not $prior.Replace("`r`n", '').Contains("`r")) 'Predecessor HTML contains bare CR.'
    $oldTitle = '<title>Topologi Aljabar — Roberts 30/30, Fomberg 1.1–1.13, Asesmen Kumulatif 1, dan Petunjuk Rute 1–6</title>'
    $newTitle = '<title>Topologi Aljabar — Roberts 30/30, Fomberg 1.1–1.13, dan Asesmen Kumulatif 1–3</title>'
    $oldHeading = '<h1 class="title">Topologi Aljabar — Roberts 30/30, Fomberg' + $htmlNl + '1.1–1.13, Asesmen Kumulatif 1, dan Petunjuk Rute 1–6</h1>'
    $newHeading = '<h1 class="title">Topologi Aljabar — Roberts 30/30, Fomberg' + $htmlNl + '1.1–1.13, dan Asesmen Kumulatif 1–3</h1>'
    $oldSubtitle = '<p class="subtitle">Komponen Roberts lengkap; jembatan Fomberg melalui' + $htmlNl + 'homologi seluler; Asesmen Kumulatif 1; 36 petunjuk penguasaan Rute 1–6; checkpoint komposit parsial</p>'
    $newSubtitle = '<p class="subtitle">Komponen Roberts lengkap; jembatan Fomberg melalui' + $htmlNl + 'homologi seluler; 84 soal rute dan 24 soal asesmen kumulatif dengan petunjuk serta solusi lengkap; checkpoint komposit parsial</p>'
    foreach ($needle in @($oldTitle,$oldHeading,$oldSubtitle)) { Require ($prior.IndexOf($needle,[StringComparison]::Ordinal) -ge 0 -and $prior.LastIndexOf($needle,[StringComparison]::Ordinal) -eq $prior.IndexOf($needle,[StringComparison]::Ordinal)) "HTML anchor missing/duplicated: $needle" }
    $combined = $prior.Replace($oldTitle,$newTitle).Replace($oldHeading,$newHeading).Replace($oldSubtitle,$newSubtitle)
    $navClose = $htmlNl + '</ul>' + $htmlNl + '</nav>'
    $navPos = $combined.LastIndexOf($navClose,[StringComparison]::Ordinal)
    Require ($navPos -gt 0) 'Top-level ToC close missing.'
    $tocInsert = $htmlNl + '<li><a href="#o012-d60-ca02" id="toc-o012-d60-ca02">Asesmen Kumulatif 2 — Homologi, Eksisi, dan Homologi Seluler</a></li>' + $htmlNl + '<li><a href="#o012-d60-ca03" id="toc-o012-d60-ca03">Asesmen Kumulatif 3 — Kohomologi, Derajat, dan Sintesis Invarian</a></li>'
    $combined = $combined.Insert($navPos,$tocInsert)
    $statusEnd = $combined.IndexOf($htmlNl + '</section>', $combined.IndexOf('<section id="o012-composite-status"',[StringComparison]::Ordinal), [StringComparison]::Ordinal)
    Require ($statusEnd -gt 0) 'Composite status close missing.'
    $statusInsert = $htmlNl + '<aside id="o012-d60-ca02-ca03-status" class="note" data-origin="edition-original">' + $htmlNl + '<p><strong>Tambahan checkpoint.</strong> Asesmen Kumulatif 2 dan 3 masing-masing menambahkan delapan soal asli edisi, delapan petunjuk, dan delapan solusi lengkap. Bersama 84 soal penguasaan rute dan Asesmen Kumulatif 1, pembaca kini menutup 108 dari 108 slot wajib bersolusi. Lapisan CC BY-SA 4.0 ini tidak memakai bank masalah Fomberg.</p>' + $htmlNl + '</aside>'
    $combined = $combined.Insert($statusEnd,$statusInsert)
    $bodyClose = $htmlNl + '</body>'
    $bodyPos = $combined.LastIndexOf($bodyClose,[StringComparison]::Ordinal)
    Require ($bodyPos -gt 0) 'HTML body close missing.'
    $fragmentInsert = ''
    foreach ($fragment in $fragments) { $fragmentInsert += $htmlNl + $(if($htmlNl -eq "`r`n"){$fragment.text.Replace($lf,"`r`n")}else{$fragment.text}).TrimEnd([char]13,[char]10) }
    $combined = $combined.Insert($bodyPos,$fragmentInsert)
    $reconstructed = $combined
    foreach ($insert in @($fragmentInsert,$statusInsert,$tocInsert)) { $pos=$reconstructed.LastIndexOf($insert,[StringComparison]::Ordinal);Require($pos -ge 0)'Cannot reverse HTML insertion.';$reconstructed=$reconstructed.Remove($pos,$insert.Length) }
    $reconstructed = $reconstructed.Replace($newTitle,$oldTitle).Replace($newHeading,$oldHeading).Replace($newSubtitle,$oldSubtitle)
    $reconstructedPath = Join-Path $scratchFull 'reconstructed-predecessor.html'
    [IO.File]::WriteAllText($reconstructedPath,$reconstructed,$utf8)
    Require ((Get-Item $reconstructedPath).Length -eq 15026881 -and (Digest $reconstructedPath) -eq '7ed278d73a324ba0a9e5acadedf448221b3791db7322fdf6d29225afd0124d2b') 'Exact HTML predecessor reconstruction failed.'
    $htmlA=Join-Path $scratchFull 'combined-a.html';$htmlB=Join-Path $scratchFull 'combined-b.html'
    [IO.File]::WriteAllText($htmlA,$combined,$utf8);[IO.File]::WriteAllText($htmlB,$combined,$utf8)
    Require ((Digest $htmlA) -eq (Digest $htmlB)) 'Combined HTML writes differ.'
    $allIds=@([regex]::Matches($combined,'(?<=\s)id="([^"]+)"')|ForEach-Object{$_.Groups[1].Value});Require(@($allIds|Group-Object|Where-Object Count -gt 1).Count -eq 0)'Duplicate HTML IDs.'
    $idSet=[Collections.Generic.HashSet[string]]::new([string[]]$allIds);$links=@([regex]::Matches($combined,'\bhref="#([^"]+)"')|ForEach-Object{[Net.WebUtility]::HtmlDecode($_.Groups[1].Value)});Require(@($links|Sort-Object -Unique|Where-Object{-not $idSet.Contains($_)}).Count -eq 0)'Unresolved HTML fragment.'
    Require ($combined.Contains($newTitle) -and $combined.Contains('id="toc-o012-d60-ca02"') -and $combined.Contains('id="toc-o012-d60-ca03"')) 'HTML title/ToC gate failed.'
    $privateMarkers = @('C:\Users\','github_pat_','ghp_','access_token','FILL_AFTER','BEGIN PRIVATE KEY')
    foreach($marker in $privateMarkers){Require(-not $combined.Contains($marker))"Private/transient marker in HTML: $marker"}

    $stripFront = [regex]::new('\A---\n.*?\n---\n', [Text.RegularExpressions.RegexOptions]::Singleline)
    $pdfText = $stripFront.Replace($sourceTextA,'',1) + $lf + $stripFront.Replace($sourceTextB,'',1)
    $fence = [regex]::new('(?m)^(::: \{\.(?:exercise|hint|solution) )#(o012-d60-ca0[23]-(?:ex|hint|sol)-\d{3})([^\r\n]*\})$')
    Require ($fence.Matches($pdfText).Count -eq 48) 'PDF fenced stable-ID transform census drift.'
    $pdfText = $fence.Replace($pdfText,('$1$3'+$lf+$lf+'```{=latex}'+$lf+'\hypertarget{$2}{}'+$lf+'\par\noindent'+$lf+'```'))
    $heading = [regex]::new('(?m)^(#{1,2})\s+(.+?)\s+\{#(o012-d60-ca0[23](?:-[a-z0-9]+)*)\}\s*$')
    Require ($heading.Matches($pdfText).Count -eq 20) 'PDF heading stable-ID transform census drift.'
    $pdfText = $heading.Replace($pdfText,('$1 $2'+$lf+$lf+'```{=latex}'+$lf+'\hypertarget{$3}{}'+$lf+'```'))
    $pdfSource=Join-Path $scratchFull 'assessments-layout.md';[IO.File]::WriteAllText($pdfSource,$pdfText,$utf8)
    $pdfHeader=Join-Path $scratchFull 'assessments-header.tex';[IO.File]::WriteAllText($pdfHeader,("\AddToHook{begindocument/end}{\pdftrailerid{}}$lf"),$utf8)
    $work=Join-Path $scratchFull 'assessments-work.pdf';$appendA=Join-Path $scratchFull 'assessments-a.pdf';$appendB=Join-Path $scratchFull 'assessments-b.pdf'
    $pdfArgs=@($pdfSource,'--from=markdown+fenced_divs+tex_math_dollars','--standalone','--number-sections','--strip-comments','--metadata=lang:id-ID','--metadata=pagetitle:Asesmen Kumulatif 2 dan 3','--metadata=date:27 Agustus 2026','--pdf-engine=pdflatex',"--include-in-header=$pdfHeader",'--variable=papersize:a4','--variable=geometry:margin=21mm','--variable=fontsize:11pt','--variable=colorlinks:true','--variable=linkcolor:blue','--variable=pdf-trailer-id:')
    & $pandoc @pdfArgs "--output=$work";Assert-Native 'Pandoc assessment PDF A';Copy-Item -LiteralPath $work -Destination $appendA -Force
    & $pandoc @pdfArgs "--output=$work";Assert-Native 'Pandoc assessment PDF B';Copy-Item -LiteralPath $work -Destination $appendB -Force
    Require ((Digest $appendA) -eq (Digest $appendB)) 'Assessment appendix PDF builds differ.'
    $appendInfo=(& $pdfinfo $appendA)-join $lf;Assert-Native 'pdfinfo appendix';Require($appendInfo -match '(?m)^Page size:.*\(A4\)\s*$' -and $appendInfo -match '(?m)^Encrypted:\s+no\s*$')'Appendix PDF gate failed.'
    $appendPages=[int]([regex]::Match($appendInfo,'(?m)^Pages:\s+(\d+)\s*$').Groups[1].Value);Require($appendPages -gt 0)'Appendix page count missing.'
    $appendTrailer = (& $mutool show $appendA trailer) -join $lf; Assert-Native 'mutool appendix trailer'
    Require($appendTrailer -notmatch '(?m)^\s*/ID\s')'Appendix trailer contains /ID.'
    $appendOutline = (& $mutool show $appendA outline) -join $lf; Assert-Native 'mutool appendix outline'
    Require((Count-OutlineRows $appendOutline) -eq 20)'Appendix outline census drift.'
    $mergedA=Join-Path $scratchFull 'combined-a.pdf';$mergedB=Join-Path $scratchFull 'combined-b.pdf'
    $mergeStdoutA = @(& $python '-B' $merger '--prior' $priorPdf '--append' $appendA '--output' $mergedA '--source-a' $sourceA '--source-b' $sourceB '--scratch-root' $scratchFull);Assert-Native 'assessment PDF merge A'
    $mergeResultA = (($mergeStdoutA | ForEach-Object { $_.ToString() }) -join $lf) | ConvertFrom-Json
    $mergeStdoutB = @(& $python '-B' $merger '--prior' $priorPdf '--append' $appendB '--output' $mergedB '--source-a' $sourceA '--source-b' $sourceB '--scratch-root' $scratchFull);Assert-Native 'assessment PDF merge B'
    $mergeResultB = (($mergeStdoutB | ForEach-Object { $_.ToString() }) -join $lf) | ConvertFrom-Json
    Require ((Digest $mergedA) -eq (Digest $mergedB)) 'Merged assessment PDFs differ.'
    $structureHashes = @($mergeResultA.predecessor_page_structure_sha256)
    Require ($mergeResultA.status -eq 'PASS' -and $mergeResultA.pypdf -eq '6.12.2' -and $structureHashes.Count -eq 482 -and (Digest-Lines ([string[]]$structureHashes)) -eq $mergeResultA.predecessor_page_structure_aggregate_sha256) 'Merged predecessor structural evidence is invalid.'
    Require ($mergeResultB.predecessor_page_structure_aggregate_sha256 -eq $mergeResultA.predecessor_page_structure_aggregate_sha256) 'Merged predecessor structural evidence differs across deterministic builds.'
    $priorText=Join-Path $scratchFull 'prior-001-482.txt';$mergedPrefix=Join-Path $scratchFull 'merged-001-482.txt';$mergedText=Join-Path $scratchFull 'merged-all.txt'
    & $pdftotext '-enc' 'UTF-8' '-f' '1' '-l' '482' $priorPdf $priorText;Assert-Native 'pdftotext predecessor'
    & $pdftotext '-enc' 'UTF-8' '-f' '1' '-l' '482' $mergedA $mergedPrefix;Assert-Native 'pdftotext merged prefix'
    Require ((Digest $priorText) -eq (Digest $mergedPrefix)) 'Extracted predecessor text changed.'
    & $pdftotext '-enc' 'UTF-8' $mergedA $mergedText;Assert-Native 'pdftotext merged'
    $allPdfText=[IO.File]::ReadAllText($mergedText);foreach($required in @('Asesmen Kumulatif 2','Asesmen Kumulatif 3','D60-R08','D60-R14','CC BY-SA 4.0')){Require($allPdfText.Contains($required))"Required PDF text missing: $required"}
    foreach($marker in $privateMarkers){Require(-not $allPdfText.Contains($marker))"Private/transient marker in PDF text: $marker"}
    $fontOutput=@(& $pdffonts $mergedA);Assert-Native 'pdffonts merged'
    $fontRows=@($fontOutput|Select-Object -Skip 2|Where-Object{$_.Trim().Length -gt 0});Require($fontRows.Count -gt 0)'PDF font inventory empty.'
    foreach($row in $fontRows){$m=[regex]::Match($row,'\s+(yes|no)\s+(yes|no)\s+(yes|no)\s+\d+\s+\d+\s*$');Require($m.Success -and $m.Groups[1].Value -eq 'yes' -and $m.Groups[2].Value -eq 'yes' -and $m.Groups[3].Value -eq 'yes')"PDF font gate failed: $row"}
    $mergedTrailer = (& $mutool show $mergedA trailer) -join $lf; Assert-Native 'mutool merged trailer'
    Require($mergedTrailer -notmatch '(?m)^\s*/ID\s')'Merged PDF trailer contains /ID.'
    $finalInfo=(& $pdfinfo $mergedA)-join $lf;Assert-Native 'pdfinfo merged final'
    $pageMatch=[regex]::Match($finalInfo,'(?m)^Pages:\s+(\d+)\s*$');Require($pageMatch.Success)'Merged PDF page count missing.'
    $pages=[int]$pageMatch.Groups[1].Value;Require($pages -eq 482 + $appendPages)'Merged PDF page count is not predecessor plus appendix.'
    foreach($marker in $privateMarkers){Require(-not $finalInfo.Contains($marker))"Private/transient marker in PDF metadata: $marker"}

    $priorRender = Render-Prefix $priorPdf (Join-Path $scratchFull 'render-prior-001-482') 482 $mutool
    $mergedRender = Render-Prefix $mergedA (Join-Path $scratchFull 'render-merged-001-482') 482 $mutool
    Require ($priorRender.page_sha256.Count -eq 482 -and $mergedRender.page_sha256.Count -eq 482) 'Rendered predecessor page census drift.'
    for($index=0;$index -lt 482;$index++){Require($priorRender.page_sha256[$index] -eq $mergedRender.page_sha256[$index])"Rendered predecessor page changed: $($index + 1)"}
    Require ($priorRender.aggregate_sha256 -eq $mergedRender.aggregate_sha256) 'Rendered predecessor aggregate changed.'

    $stagedManifest=Join-Path $scratchFull 'artifact-manifest.csv'
    $manifest=@('path,bytes,sha256');foreach($artifact in @(@($htmlOut,$htmlA),@($pdfOut,$mergedA))){$item=Get-Item $artifact[1];$manifest += "$(Relative $artifact[0]),$($item.Length),$(Digest $artifact[1])"};[IO.File]::WriteAllText($stagedManifest,(($manifest -join $lf)+$lf),$utf8)
    $receipt=[ordered]@{
        status='PASS_DETERMINISTIC_BUILD_PENDING_VISUAL_BROWSER_QA';source_date_epoch=[int64]$env:SOURCE_DATE_EPOCH;model_provenance='OpenAI Codex gpt-5.6-sol, Ultra';pandoc=$pandocVersion;mutool=$mutoolVersion;pypdf=$mergeResultA.pypdf
        sources=@([ordered]@{path=(Relative $sourceA);bytes=(Get-Item $sourceA).Length;sha256=(Digest $sourceA)},[ordered]@{path=(Relative $sourceB);bytes=(Get-Item $sourceB).Length;sha256=(Digest $sourceB)})
        frozen_predecessor=[ordered]@{html_bytes=15026881;html_sha256='7ed278d73a324ba0a9e5acadedf448221b3791db7322fdf6d29225afd0124d2b';pdf_bytes=8592243;pdf_sha256='4da7f1368c17423cd6845c36b7d5190dac98d515ecbd32467c0c59961dd9afcb';pdf_pages=482;html_exact_reconstruction=$true;pdf_extracted_text_prefix_identical=$true;pdf_page_structure_algorithm=$mergeResultA.predecessor_page_structure_algorithm;pdf_page_structure_aggregate_sha256=$mergeResultA.predecessor_page_structure_aggregate_sha256;pdf_page_structure_sha256=$structureHashes;render_engine=$mutoolVersion;render_contract='PNG RGB 72 dpi antialiasing 8';render_aggregate_sha256=$priorRender.aggregate_sha256;render_page_sha256=$priorRender.page_sha256}
        html=[ordered]@{path=(Relative $htmlOut);bytes=(Get-Item $htmlA).Length;sha256=(Digest $htmlA);dom_ids=$allIds.Count;fragment_links=$links.Count;stable_ids_added=68;assessment_triples_added=16;deterministic_writes=2}
        pdf=[ordered]@{path=(Relative $pdfOut);bytes=(Get-Item $mergedA).Length;sha256=(Digest $mergedA);pages=$pages;appendix_pages=$appendPages;stable_id_destinations_added=68;outline_entries_added=20;fonts=$fontRows.Count;all_fonts_embedded_subset_tounicode=$true;trailer_id_suppressed=$true;deterministic_appendix_builds=2;deterministic_merged_builds=2}
        manifest=[ordered]@{path=(Relative $manifestOut);bytes=(Get-Item $stagedManifest).Length;sha256=(Digest $stagedManifest)}
        qa=[ordered]@{path=(Relative $sourceQa);bytes=(Get-Item $sourceQa).Length;sha256=(Digest $sourceQa)}
        backend_receipt=[ordered]@{path=(Relative $backendReceipt);bytes=(Get-Item $backendReceipt).Length;sha256=(Digest $backendReceipt)}
    }
    $stagedReceipt=Join-Path $scratchFull 'build-draft.json';[IO.File]::WriteAllText($stagedReceipt,(($receipt|ConvertTo-Json -Depth 10)+$lf),$utf8)
    $transaction=[Guid]::NewGuid().ToString('N')
    $promotions=@(
        (Prepare-AtomicPromotion $htmlA $htmlOut $transaction $scratchFull),
        (Prepare-AtomicPromotion $mergedA $pdfOut $transaction $scratchFull),
        (Prepare-AtomicPromotion $stagedManifest $manifestOut $transaction $scratchFull),
        (Prepare-AtomicPromotion $stagedReceipt $draftReceipt $transaction $scratchFull)
    )
    $promotionTemps=@($promotions|ForEach-Object{$_.pending})
    Commit-AtomicPromotions $promotions
    $receipt|ConvertTo-Json -Depth 8
}
finally {
    foreach($temporary in $promotionTemps){if(Test-Path -LiteralPath $temporary -PathType Leaf){[IO.File]::Delete($temporary)}}
    if(Test-Path -LiteralPath $scratchFull){Remove-Item -LiteralPath $scratchFull -Recurse -Force}
    Require(-not(Test-Path -LiteralPath $scratchFull))'Bounded scratch removal failed.'
}
