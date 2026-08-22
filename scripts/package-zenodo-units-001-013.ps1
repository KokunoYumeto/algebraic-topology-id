#requires -Version 7.0
[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$lane = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$releaseRoot = Join-Path $lane 'release\zenodo-units-001-013'
$artifactsDir = Join-Path $releaseRoot 'artifacts'
$lockPath = Join-Path $releaseRoot '.release-operation.lock'
$stageDir = Join-Path $releaseRoot ('.artifacts-stage-' + [guid]::NewGuid().ToString('N'))
$backupDir = Join-Path $releaseRoot ('.artifacts-backup-' + [guid]::NewGuid().ToString('N'))
$snapshotDir = Join-Path $releaseRoot ('.release-provenance-' + [guid]::NewGuid().ToString('N'))
$verifyScript = Join-Path $PSScriptRoot 'verify-zenodo-units-001-013.ps1'

$pdfName = '00_TOPOLOGI_ALJABAR_ID_UNIT_001_013_READER.pdf'
$htmlName = 'TOPOLOGI_ALJABAR_ID_UNIT_001_013_READER.html'
$sourceZipName = 'TOPOLOGI_ALJABAR_ID_UNIT_001_013_EDITABLE_SOURCE_BACKEND.zip'
$qaZipName = 'TOPOLOGI_ALJABAR_ID_UNIT_001_013_QA_PROVENANCE.zip'
$readmeName = 'README_RELEASE.md'
$rightsName = 'RELEASE_RIGHTS.md'
$manifestName = 'release-manifest.json'
$sumsName = 'SHA256SUMS'

New-Item -ItemType Directory -Path $releaseRoot -Force | Out-Null
$lockStream = $null
try {
    $lockStream = [IO.File]::Open($lockPath, [IO.FileMode]::CreateNew, [IO.FileAccess]::ReadWrite, [IO.FileShare]::None)
} catch {
    throw "Another release operation is active or a stale lock needs inspection: $lockPath"
}

function Assert-ReleaseChild([string]$Path) {
    $full = [IO.Path]::GetFullPath($Path)
    $prefix = [IO.Path]::GetFullPath($releaseRoot).TrimEnd('\') + '\'
    if (-not $full.StartsWith($prefix, [StringComparison]::OrdinalIgnoreCase)) {
        throw "Refusing path outside the release root: $full"
    }
}

function Get-Sha256([string]$Path) {
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}

function Assert-SafeTextFile([string]$Path, [string]$Label) {
    $text = [IO.File]::ReadAllText($Path)
    $forbidden = @(
        '(?i)[A-Z]:[\\/](?:Users|Documents and Settings|Temp|ProgramData)[\\/]',
        '(?i)\\\\[A-Za-z0-9_.-]{3,}\\[A-Za-z0-9$_.-]{3,}\\[A-Za-z0-9$_. -]{3,}',
        '(?i)/(?:Users|home)/[^/\s]+/',
        '(?i)github_pat_', '(?i)\bghp_[A-Za-z0-9_]+', '(?i)\bglpat-[A-Za-z0-9_-]+',
        '(?i)\bsk-[A-Za-z0-9_-]{16,}', '(?i)\bAKIA[0-9A-Z]{16}\b',
        '(?i)\bxox[baprs]-[A-Za-z0-9-]{16,}', '(?i)-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
        '(?i)\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b',
        '(?i)access_token', '(?i)authorization\s*[:=]\s*["'']?bearer', '(?i)zenodo.{0,24}token',
        '(?i)figshare.{0,24}token', '(?i)api[_-]?key', '(?i)Translation and Transcription Project', '(?i)\bTTP\b'
    )
    foreach ($pattern in $forbidden) {
        if ($text -match $pattern) { throw "Forbidden private/credential/umbrella text in $Label" }
    }
}

function Assert-SafeBinaryFile([string]$Path, [string]$Label) {
    $text = [Text.Encoding]::Latin1.GetString([IO.File]::ReadAllBytes($Path))
    $forbidden = @(
        '(?i)[A-Z]:[\\/](?:Users|Documents and Settings|Temp|ProgramData)[\\/]',
        '(?i)\\\\[A-Za-z0-9_.-]{3,}\\[A-Za-z0-9$_.-]{3,}\\[A-Za-z0-9$_. -]{3,}',
        '(?i)/(?:Users|home)/[^/\s]+/',
        '(?i)github_pat_[A-Za-z0-9_]{16,}', '(?i)\bghp_[A-Za-z0-9_]{16,}', '(?i)\bglpat-[A-Za-z0-9_-]{16,}',
        '(?i)\bsk-[A-Za-z0-9_-]{16,}', '(?i)\bAKIA[0-9A-Z]{16}\b', '(?i)\bxox[baprs]-[A-Za-z0-9-]{16,}',
        '(?i)-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
        '(?i)\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b',
        '(?i)authorization\s*[:=]\s*["'']?bearer\s+[A-Za-z0-9._~-]{16,}',
        '(?i)(?:access_token|api[_-]?key|zenodo[_ -]?token|figshare[_ -]?token)\s*[:=]\s*["'']?[A-Za-z0-9._~-]{16,}'
    )
    foreach ($pattern in $forbidden) {
        if ($text -match $pattern) { throw "Forbidden private/credential signature in binary artifact $Label" }
    }
}

function New-Entry([string]$Source, [string]$ArchiveName) {
    if (-not (Test-Path -LiteralPath $Source -PathType Leaf)) { throw "Missing archive input: $Source" }
    return [pscustomobject]@{ Source = [IO.Path]::GetFullPath($Source); ArchiveName = $ArchiveName.Replace('\', '/') }
}

function New-BoundedLedgerSnapshot([string]$Source, [string]$Destination, [string]$Prefix, [int]$MaximumId) {
    $lines = [IO.File]::ReadAllLines($Source)
    if ($lines.Count -lt 2) { throw "Ledger is empty: $Source" }
    $selected = [Collections.Generic.List[string]]::new()
    $selected.Add($lines[0])
    $seen = [Collections.Generic.HashSet[int]]::new()
    foreach ($line in $lines[1..($lines.Count - 1)]) {
        if ($line -match ('^(?:"?)' + [regex]::Escape($Prefix) + '(\d{4})(?:"?),')) {
            $id = [int]$Matches[1]
            if ($id -le $MaximumId) {
                if (-not $seen.Add($id)) { throw "Duplicate bounded ledger ID $Prefix$($id.ToString('0000'))" }
                $selected.Add($line)
            }
        }
    }
    if ($seen.Count -ne $MaximumId -or -not $seen.Contains(1) -or -not $seen.Contains($MaximumId)) {
        throw "Bounded ledger snapshot is not contiguous through $Prefix$($MaximumId.ToString('0000'))."
    }
    [IO.File]::WriteAllText($Destination, ($selected -join "`n") + "`n", [Text.UTF8Encoding]::new($false))
}

function New-DeterministicZip([string]$ZipPath, [object[]]$Entries) {
    Add-Type -AssemblyName System.IO.Compression
    $duplicates = @($Entries | Group-Object ArchiveName | Where-Object Count -gt 1)
    if ($duplicates.Count -gt 0) { throw "Duplicate ZIP entry: $($duplicates[0].Name)" }
    if (Test-Path -LiteralPath $ZipPath) { Remove-Item -LiteralPath $ZipPath -Force }
    $fixedTime = [DateTimeOffset]::new(2026, 8, 22, 0, 0, 0, [TimeSpan]::Zero)
    $fileStream = [IO.File]::Open($ZipPath, [IO.FileMode]::CreateNew, [IO.FileAccess]::ReadWrite, [IO.FileShare]::None)
    try {
        $zip = [IO.Compression.ZipArchive]::new($fileStream, [IO.Compression.ZipArchiveMode]::Create, $true)
        try {
            foreach ($item in @($Entries | Sort-Object ArchiveName)) {
                $entry = $zip.CreateEntry($item.ArchiveName, [IO.Compression.CompressionLevel]::Optimal)
                $entry.LastWriteTime = $fixedTime
                $input = [IO.File]::OpenRead($item.Source)
                try {
                    $output = $entry.Open()
                    try { $input.CopyTo($output) } finally { $output.Dispose() }
                } finally { $input.Dispose() }
            }
        } finally { $zip.Dispose() }
    } finally { $fileStream.Dispose() }

    $expected = @{}
    foreach ($item in $Entries) {
        $sourceItem = Get-Item -LiteralPath $item.Source
        $expected[$item.ArchiveName] = [ordered]@{ bytes = [int64]$sourceItem.Length; sha256 = Get-Sha256 $item.Source }
    }
    $inventory = @()
    $readStream = [IO.File]::OpenRead($ZipPath)
    try {
        $readZip = [IO.Compression.ZipArchive]::new($readStream, [IO.Compression.ZipArchiveMode]::Read, $false)
        try {
            if ($readZip.Entries.Count -ne $Entries.Count) { throw "ZIP count mismatch: $ZipPath" }
            foreach ($entry in @($readZip.Entries | Sort-Object FullName)) {
                if (-not $expected.ContainsKey($entry.FullName)) { throw "Unexpected ZIP entry: $($entry.FullName)" }
                $entryStream = $entry.Open()
                try {
                    $hasher = [Security.Cryptography.SHA256]::Create()
                    try { $digest = ([Convert]::ToHexString($hasher.ComputeHash($entryStream))).ToLowerInvariant() }
                    finally { $hasher.Dispose() }
                } finally { $entryStream.Dispose() }
                $want = $expected[$entry.FullName]
                if ([int64]$entry.Length -ne [int64]$want.bytes -or $digest -cne [string]$want.sha256) {
                    throw "ZIP entry verification failed: $($entry.FullName)"
                }
                $inventory += [ordered]@{ path = $entry.FullName; bytes = [int64]$entry.Length; sha256 = $digest }
            }
        } finally { $readZip.Dispose() }
    } finally { $readStream.Dispose() }
    $zipItem = Get-Item -LiteralPath $ZipPath
    return [ordered]@{
        filename = $zipItem.Name; bytes = [int64]$zipItem.Length; sha256 = Get-Sha256 $ZipPath
        entry_count = $inventory.Count; entries = $inventory; verified = $true
    }
}

function Assert-DeterministicZip([string]$PrimaryPath, [object[]]$Entries) {
    $secondPath = "$PrimaryPath.reprocheck"
    Assert-ReleaseChild $secondPath
    try {
        $second = New-DeterministicZip $secondPath $Entries
        $primaryItem = Get-Item -LiteralPath $PrimaryPath
        if ([int64]$second.bytes -ne [int64]$primaryItem.Length -or
            [string]$second.sha256 -cne (Get-Sha256 $PrimaryPath)) {
            throw "ZIP byte reproducibility failed: $([IO.Path]::GetFileName($PrimaryPath))"
        }
    } finally {
        if (Test-Path -LiteralPath $secondPath) { Remove-Item -LiteralPath $secondPath -Force }
    }
}

function Get-ArtifactRow([string]$Path, [string]$Role, [string]$MediaType) {
    $item = Get-Item -LiteralPath $Path
    return [ordered]@{ filename = $item.Name; role = $Role; media_type = $MediaType; bytes = [int64]$item.Length; sha256 = Get-Sha256 $Path }
}

try {
    foreach ($path in @($stageDir, $backupDir, $snapshotDir)) { Assert-ReleaseChild $path }
    New-Item -ItemType Directory -Path $stageDir | Out-Null
    New-Item -ItemType Directory -Path $snapshotDir | Out-Null

    $htmlSource = Join-Path $lane 'output\html\units-001-013\index.html'
    $pdfSource = Join-Path $lane 'output\pdf\topologi-aljabar-unit-001-013-id.pdf'
    $qaPath = Join-Path $lane 'qa\UNITS_001_013_QA.json'
    $metadataPath = Join-Path $releaseRoot 'metadata.json'
    $readmeSource = Join-Path $releaseRoot $readmeName
    $rightsSource = Join-Path $releaseRoot $rightsName
    foreach ($path in @($htmlSource, $pdfSource, $qaPath, $metadataPath, $readmeSource, $rightsSource, $verifyScript)) {
        if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { throw "Missing release input: $path" }
    }
    $qaDocument = [IO.File]::ReadAllText($qaPath) | ConvertFrom-Json
    if ([string]$qaDocument.status -cne 'pass') { throw 'Cumulative QA receipt is not PASS.' }
    $qaArtifacts = @{}
    foreach ($row in @($qaDocument.artifacts)) { $qaArtifacts[[string]$row.path] = $row }
    foreach ($binding in @(
        @($htmlSource, 'output/html/units-001-013/index.html'),
        @($pdfSource, 'output/pdf/topologi-aljabar-unit-001-013-id.pdf')
    )) {
        $item = Get-Item -LiteralPath $binding[0]
        $row = $qaArtifacts[$binding[1]]
        if ($null -eq $row -or [int64]$row.bytes -ne [int64]$item.Length -or [string]$row.sha256 -cne (Get-Sha256 $binding[0])) {
            throw "Reader is not bound to QA receipt: $($binding[0])"
        }
    }

    $htmlPath = Join-Path $stageDir $htmlName
    $pdfPath = Join-Path $stageDir $pdfName
    $readmePath = Join-Path $stageDir $readmeName
    $rightsPath = Join-Path $stageDir $rightsName
    Copy-Item -LiteralPath $htmlSource -Destination $htmlPath
    Copy-Item -LiteralPath $pdfSource -Destination $pdfPath
    Copy-Item -LiteralPath $readmeSource -Destination $readmePath
    Copy-Item -LiteralPath $rightsSource -Destination $rightsPath

    $sourceEntries = [Collections.Generic.List[object]]::new()
    $sourceEntries.Add((New-Entry $readmeSource 'README_RELEASE.md'))
    $sourceEntries.Add((New-Entry $rightsSource 'RELEASE_RIGHTS.md'))
    $sourceEntries.Add((New-Entry (Join-Path $lane 'ATTRIBUTION.md') 'ATTRIBUTION.md'))
    $upstream = Join-Path $lane 'authority\upstream\AlgebraicTopology2019-b947ad2e9f9e301bfe24590a9db653bc54fa1a53'
    $sourceEntries.Add((New-Entry (Join-Path $upstream 'LICENSE.md') 'upstream/Roberts/LICENSE.md'))
    $sourceEntries.Add((New-Entry (Join-Path $upstream 'README.md') 'upstream/Roberts/README.md'))
    $sourceEntries.Add((New-Entry (Join-Path $upstream 'Notes.tex') 'upstream/Roberts/Notes.tex'))
    $sourceEntries.Add((New-Entry (Join-Path $lane 'source\id-ID\reader-unit-001.md') 'source/id-ID/reader-unit-001.md'))
    foreach ($number in 2..13) {
        $nnn = $number.ToString('000')
        $sourceEntries.Add((New-Entry (Join-Path $lane "source\id-ID\units\unit-$nnn-lecture-$nnn.md") "source/id-ID/units/unit-$nnn-lecture-$nnn.md"))
    }
    foreach ($name in @('reader.css','reader-cumulative.css')) {
        $sourceEntries.Add((New-Entry (Join-Path $lane "source\id-ID\styles\$name") "source/id-ID/styles/$name"))
    }
    $backendNames = @('artifacts.jsonl','assets.jsonl','authority.jsonl','concepts.jsonl','corrections.jsonl','qa.jsonl','relations.jsonl','rights.jsonl','segments.jsonl','terms.jsonl','units.jsonl')
    foreach ($name in $backendNames) { $sourceEntries.Add((New-Entry (Join-Path $lane "backend\$name") "backend/$name")) }
    $sourceEntries.Add((New-Entry (Join-Path $lane '00_control\AUTHORITY.json') 'provenance/AUTHORITY.json'))
    $sourceEntries.Add((New-Entry (Join-Path $lane '00_control\UPSTREAM_FILE_MANIFEST.csv') 'provenance/UPSTREAM_FILE_MANIFEST.csv'))

    $qaEntries = [Collections.Generic.List[object]]::new()
    $qaEntries.Add((New-Entry $readmeSource 'README_RELEASE.md'))
    $qaEntries.Add((New-Entry $rightsSource 'RELEASE_RIGHTS.md'))
    $qaEntries.Add((New-Entry $metadataPath 'zenodo/metadata.json'))
    foreach ($number in 1..13) {
        $nnn = $number.ToString('000')
        $qaEntries.Add((New-Entry (Join-Path $lane "qa\UNIT_${nnn}_INDEPENDENT_REVIEW.md") "qa/UNIT_${nnn}_INDEPENDENT_REVIEW.md"))
    }
    foreach ($name in @('UNITS_001_013_QA.json','UNITS_001_013_VISUAL_QA.md','UNITS_001_013_RENDER_INVENTORY.csv','units-001-013-extracted.txt')) {
        $qaEntries.Add((New-Entry (Join-Path $lane "qa\$name") "qa/$name"))
    }
    foreach ($name in @('contact-001-012.png','contact-013-024.png','contact-025-036.png','contact-037-048.png','contact-049-060.png','contact-061-072.png','contact-073-084.png','contact-085-096.png','contact-097-108.png','contact-109-120.png','contact-121-132.png','contact-133-138.png')) {
        $qaEntries.Add((New-Entry (Join-Path $lane "tmp\pdfs\units-001-013-visual\$name") "qa/visual-contact-sheets/$name"))
    }
    $qaEntries.Add((New-Entry (Join-Path $lane 'output\ARTIFACT_MANIFEST_UNITS_001_013.csv') 'output/ARTIFACT_MANIFEST_UNITS_001_013.csv'))
    foreach ($name in @('AUTHORITY.json','UPSTREAM_FILE_MANIFEST.csv')) {
        $qaEntries.Add((New-Entry (Join-Path $lane "00_control\$name") "provenance/$name"))
    }
    $adverseSnapshot = Join-Path $snapshotDir 'ADVERSE_LEDGER.csv'
    $terminologySnapshot = Join-Path $snapshotDir 'TERMINOLOGY.csv'
    New-BoundedLedgerSnapshot (Join-Path $lane '00_control\ADVERSE_LEDGER.csv') $adverseSnapshot 'O012-ADV-' 187
    New-BoundedLedgerSnapshot (Join-Path $lane '00_control\TERMINOLOGY.csv') $terminologySnapshot 'O012-TERM-' 213
    $qaEntries.Add((New-Entry $adverseSnapshot 'provenance/ADVERSE_LEDGER.csv'))
    $qaEntries.Add((New-Entry $terminologySnapshot 'provenance/TERMINOLOGY.csv'))

    foreach ($entry in @($sourceEntries.ToArray() + $qaEntries.ToArray())) {
        if ($entry.Source -match '\.(md|json|jsonl|csv|txt|tex|css|html)$') { Assert-SafeTextFile $entry.Source $entry.ArchiveName }
    }
    Assert-SafeTextFile $htmlPath $htmlName
    Assert-SafeTextFile $metadataPath 'metadata.json'
    Assert-SafeBinaryFile $pdfPath $pdfName
    foreach ($entry in @($sourceEntries.ToArray() + $qaEntries.ToArray())) {
        if ($entry.Source -notmatch '\.(md|json|jsonl|csv|txt|tex|css|html)$') {
            Assert-SafeBinaryFile $entry.Source $entry.ArchiveName
        }
    }

    $sourceZipPath = Join-Path $stageDir $sourceZipName
    $qaZipPath = Join-Path $stageDir $qaZipName
    $sourceZip = New-DeterministicZip $sourceZipPath $sourceEntries.ToArray()
    $qaZip = New-DeterministicZip $qaZipPath $qaEntries.ToArray()
    Assert-DeterministicZip $sourceZipPath $sourceEntries.ToArray()
    Assert-DeterministicZip $qaZipPath $qaEntries.ToArray()

    $backendInventory = @()
    $backendRecords = 0
    $backendBytes = 0
    $bundleStream = [IO.MemoryStream]::new()
    try {
        foreach ($name in ($backendNames | Sort-Object)) {
            $path = Join-Path $lane "backend\$name"
            $records = @([IO.File]::ReadLines($path) | Where-Object { -not [string]::IsNullOrWhiteSpace($_) }).Count
            $item = Get-Item -LiteralPath $path
            $backendRecords += $records; $backendBytes += [int64]$item.Length
            $backendInventory += [ordered]@{ filename=$name; records=$records; bytes=[int64]$item.Length; sha256=Get-Sha256 $path }
            $nameBytes = [Text.Encoding]::UTF8.GetBytes($name)
            $bundleStream.Write($nameBytes, 0, $nameBytes.Length); $bundleStream.WriteByte(0)
            $input = [IO.File]::OpenRead($path)
            try { $input.CopyTo($bundleStream) } finally { $input.Dispose() }
        }
        $bundleStream.Position = 0
        $hasher = [Security.Cryptography.SHA256]::Create()
        try { $backendBundle = ([Convert]::ToHexString($hasher.ComputeHash($bundleStream))).ToLowerInvariant() }
        finally { $hasher.Dispose() }
    } finally { $bundleStream.Dispose() }
    if ($backendRecords -ne 1762 -or $backendBundle -cne 'bb8512f56a8bbcf1283ae10ab69a9a7ecebb1bd39c425c1c021b5b848a1b2910') {
        throw 'Backend census/bundle identity mismatch.'
    }

    $manifest = [ordered]@{
        schema_version='1.0'; release_id='o012-roberts-id-units-001-013-v0.13.0'
        title='Topologi Aljabar: Edisi Bahasa Indonesia — Unit 1–13'; version='0.13.0'
        release_date='2026-08-22'; status='maintained_incomplete_checkpoint'
        metadata_sha256=Get-Sha256 $metadataPath
        source=[ordered]@{ author='David Michael Roberts'; repository='https://github.com/DavidMichaelRoberts/AlgebraicTopology2019'; commit='b947ad2e9f9e301bfe24590a9db653bc54fa1a53'; tree='aa1d3edb85818e7176e2d0bbc06d9b4bd1e247f5'; path='Notes.tex'; line_start=134; line_end=3046; units=13; license='CC BY 4.0' }
        reader_qa=[ordered]@{ status='pass'; receipt_sha256=Get-Sha256 $qaPath; html_stable_ids=[int]$qaDocument.html.stable_ids; html_ids=[int]$qaDocument.html.ids; html_mathml_nodes=[int]$qaDocument.html.mathml_nodes; pdf_pages=[int]$qaDocument.pdf.pages; pdf_tagged=[bool]$qaDocument.pdf.tagged; visual_review=[string]$qaDocument.gates.visual_review }
        backend=[ordered]@{ files=$backendNames.Count; records=$backendRecords; bytes=$backendBytes; validator_bundle_sha256=$backendBundle; inventory=$backendInventory }
        archives=@($sourceZip,$qaZip)
        artifacts=@(
            (Get-ArtifactRow $pdfPath 'secondary_print_reader_untagged' 'application/pdf'),
            (Get-ArtifactRow $htmlPath 'primary_offline_semantic_reader' 'text/html'),
            (Get-ArtifactRow $sourceZipPath 'editable_source_and_modular_backend' 'application/zip'),
            (Get-ArtifactRow $qaZipPath 'sanitized_qa_and_provenance' 'application/zip'),
            (Get-ArtifactRow $readmePath 'release_readme' 'text/markdown'),
            (Get-ArtifactRow $rightsPath 'component_rights_and_attribution' 'text/markdown')
        )
    }
    $manifestPath = Join-Path $stageDir $manifestName
    [IO.File]::WriteAllText($manifestPath, ($manifest | ConvertTo-Json -Depth 14) + "`n", [Text.UTF8Encoding]::new($false))
    $sumTargets = @($pdfPath,$htmlPath,$sourceZipPath,$qaZipPath,$readmePath,$rightsPath,$manifestPath)
    $sumLines = foreach ($path in $sumTargets) { "$(Get-Sha256 $path)  $([IO.Path]::GetFileName($path))" }
    [IO.File]::WriteAllText((Join-Path $stageDir $sumsName), ($sumLines -join "`n") + "`n", [Text.UTF8Encoding]::new($false))

    & (Get-Command pwsh -ErrorAction Stop).Source -NoProfile -File $verifyScript -ReleaseDirectory $stageDir | Out-Host
    if ($LASTEXITCODE -ne 0) { throw 'Independent staged release verification failed.' }

    $hadPrior = Test-Path -LiteralPath $artifactsDir -PathType Container
    $promotionSucceeded = $false
    $rollbackSucceeded = $false
    if ($hadPrior) { Move-Item -LiteralPath $artifactsDir -Destination $backupDir }
    try {
        Move-Item -LiteralPath $stageDir -Destination $artifactsDir
        & (Get-Command pwsh -ErrorAction Stop).Source -NoProfile -File $verifyScript -ReleaseDirectory $artifactsDir | Out-Host
        if ($LASTEXITCODE -ne 0) { throw 'Promoted release verification failed.' }
        $promotionSucceeded = $true
    } catch {
        if (Test-Path -LiteralPath $artifactsDir) { Remove-Item -LiteralPath $artifactsDir -Recurse -Force }
        if ($hadPrior -and (Test-Path -LiteralPath $backupDir)) {
            Move-Item -LiteralPath $backupDir -Destination $artifactsDir
            $rollbackSucceeded = $true
        }
        throw
    }
    if ($promotionSucceeded -and $hadPrior -and (Test-Path -LiteralPath $backupDir)) {
        try { Remove-Item -LiteralPath $backupDir -Recurse -Force }
        catch { Write-Warning "Promoted artifacts are valid, but the obsolete backup could not be removed: $backupDir" }
    }

    $final = foreach ($name in @($pdfName,$htmlName,$sourceZipName,$qaZipName,$readmeName,$rightsName,$manifestName,$sumsName)) {
        $path = Join-Path $artifactsDir $name; $item=Get-Item -LiteralPath $path
        [pscustomobject]@{Filename=$name;Bytes=[int64]$item.Length;SHA256=Get-Sha256 $path}
    }
    [pscustomobject]@{Status='PASS';ReleaseDirectory=$artifactsDir;FileCount=$final.Count;BackendRecords=$backendRecords;BackendBundleSHA256=$backendBundle}
    $final
} finally {
    try {
        if (Test-Path -LiteralPath $stageDir) {
            try { Assert-ReleaseChild $stageDir; Remove-Item -LiteralPath $stageDir -Recurse -Force }
            catch { Write-Warning "Retained a failed staging directory because cleanup failed: $stageDir" }
        }
        if (Test-Path -LiteralPath $snapshotDir) {
            try { Assert-ReleaseChild $snapshotDir; Remove-Item -LiteralPath $snapshotDir -Recurse -Force }
            catch { Write-Warning "Retained a release-provenance staging directory because cleanup failed: $snapshotDir" }
        }
        if (Test-Path -LiteralPath $backupDir) {
            Assert-ReleaseChild $backupDir
            if ($promotionSucceeded) {
                try { Remove-Item -LiteralPath $backupDir -Recurse -Force }
                catch { Write-Warning "Retained an obsolete backup that could not be removed after successful promotion: $backupDir" }
            } elseif ($rollbackSucceeded) {
                Write-Warning "Rollback reported success but the backup path still exists unexpectedly: $backupDir"
            } else {
                Write-Warning "Retained the prior artifact backup after an incomplete rollback: $backupDir"
            }
        }
    } finally {
        if ($null -ne $lockStream) { $lockStream.Dispose() }
        if (Test-Path -LiteralPath $lockPath) {
            try { Remove-Item -LiteralPath $lockPath -Force }
            catch { Write-Warning "Release operation ended but the stale lock could not be removed: $lockPath" }
        }
    }
}
