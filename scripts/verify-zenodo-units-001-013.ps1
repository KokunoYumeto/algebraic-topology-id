#requires -Version 7.0
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$ReleaseDirectory
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$releaseDir = [IO.Path]::GetFullPath($ReleaseDirectory)
if (-not (Test-Path -LiteralPath $releaseDir -PathType Container)) {
    throw "Release directory does not exist: $releaseDir"
}

$pdfName = '00_TOPOLOGI_ALJABAR_ID_UNIT_001_013_READER.pdf'
$htmlName = 'TOPOLOGI_ALJABAR_ID_UNIT_001_013_READER.html'
$sourceZipName = 'TOPOLOGI_ALJABAR_ID_UNIT_001_013_EDITABLE_SOURCE_BACKEND.zip'
$qaZipName = 'TOPOLOGI_ALJABAR_ID_UNIT_001_013_QA_PROVENANCE.zip'
$readmeName = 'README_RELEASE.md'
$rightsName = 'RELEASE_RIGHTS.md'
$manifestName = 'release-manifest.json'
$sumsName = 'SHA256SUMS'
$expectedNames = @($pdfName, $htmlName, $sourceZipName, $qaZipName, $readmeName, $rightsName, $manifestName, $sumsName)

function Get-Sha256([string]$Path) {
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}

function Get-StreamSha256([IO.Stream]$Stream) {
    $hasher = [Security.Cryptography.SHA256]::Create()
    try {
        return ([Convert]::ToHexString($hasher.ComputeHash($Stream))).ToLowerInvariant()
    } finally {
        $hasher.Dispose()
    }
}

function Get-BytesSha256([byte[]]$Bytes) {
    return ([Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($Bytes))).ToLowerInvariant()
}

function Assert-SafeText([string]$Text, [string]$Label) {
    $forbidden = @(
        '(?i)[A-Z]:[\\/](?:Users|Documents and Settings|Temp|ProgramData)[\\/]',
        '(?i)\\\\[A-Za-z0-9_.-]{3,}\\[A-Za-z0-9$_.-]{3,}\\[A-Za-z0-9$_. -]{3,}',
        '(?i)/(?:Users|home)/[^/\s]+/',
        '(?i)github_pat_',
        '(?i)\bghp_[A-Za-z0-9_]+',
        '(?i)\bglpat-[A-Za-z0-9_-]+',
        '(?i)\bsk-[A-Za-z0-9_-]{16,}',
        '(?i)\bAKIA[0-9A-Z]{16}\b',
        '(?i)\bxox[baprs]-[A-Za-z0-9-]{16,}',
        '(?i)-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
        '(?i)\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b',
        '(?i)access_token',
        '(?i)authorization\s*[:=]\s*["'']?bearer',
        '(?i)zenodo.{0,24}token',
        '(?i)figshare.{0,24}token',
        '(?i)api[_-]?key',
        '(?i)Translation and Transcription Project',
        '(?i)\bTTP\b'
    )
    foreach ($pattern in $forbidden) {
        if ($Text -match $pattern) {
            throw "Forbidden private/credential/umbrella text in $Label (pattern: $pattern)."
        }
    }
}

function Assert-SafeBinary([byte[]]$Bytes, [string]$Label) {
    # Binary artifacts are checked only for long credential/path signatures.
    # Short prose markers are deliberately omitted to avoid matches in random
    # compressed payload bytes.
    $text = [Text.Encoding]::Latin1.GetString($Bytes)
    $forbidden = @(
        '(?i)[A-Z]:[\\/](?:Users|Documents and Settings|Temp|ProgramData)[\\/]',
        '(?i)\\\\[A-Za-z0-9_.-]{3,}\\[A-Za-z0-9$_.-]{3,}\\[A-Za-z0-9$_. -]{3,}',
        '(?i)/(?:Users|home)/[^/\s]+/',
        '(?i)github_pat_[A-Za-z0-9_]{16,}',
        '(?i)\bghp_[A-Za-z0-9_]{16,}',
        '(?i)\bglpat-[A-Za-z0-9_-]{16,}',
        '(?i)\bsk-[A-Za-z0-9_-]{16,}',
        '(?i)\bAKIA[0-9A-Z]{16}\b',
        '(?i)\bxox[baprs]-[A-Za-z0-9-]{16,}',
        '(?i)-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
        '(?i)\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b',
        '(?i)authorization\s*[:=]\s*["'']?bearer\s+[A-Za-z0-9._~-]{16,}',
        '(?i)(?:access_token|api[_-]?key|zenodo[_ -]?token|figshare[_ -]?token)\s*[:=]\s*["'']?[A-Za-z0-9._~-]{16,}'
    )
    foreach ($pattern in $forbidden) {
        if ($text -match $pattern) {
            throw "Forbidden private/credential signature in binary artifact $Label."
        }
    }
}

function Get-ZipEntryBytes([string]$ZipPath, [string]$EntryName) {
    $stream = [IO.File]::OpenRead($ZipPath)
    try {
        $archive = [IO.Compression.ZipArchive]::new($stream, [IO.Compression.ZipArchiveMode]::Read, $false)
        try {
            $entry = $archive.GetEntry($EntryName)
            if ($null -eq $entry) { throw "ZIP lacks required entry: $EntryName" }
            $entryStream = $entry.Open()
            try {
                $memory = [IO.MemoryStream]::new()
                try {
                    $entryStream.CopyTo($memory)
                    return $memory.ToArray()
                } finally { $memory.Dispose() }
            } finally { $entryStream.Dispose() }
        } finally { $archive.Dispose() }
    } finally { $stream.Dispose() }
}

$actualNames = @(Get-ChildItem -LiteralPath $releaseDir -File | ForEach-Object Name | Sort-Object)
if (($actualNames -join "`n") -cne (($expectedNames | Sort-Object) -join "`n")) {
    throw "Release inventory mismatch. Found: $($actualNames -join ', ')"
}

foreach ($name in $expectedNames) {
    $path = Join-Path $releaseDir $name
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
        throw "Missing release artifact: $name"
    }
}

$sumTargets = @($pdfName, $htmlName, $sourceZipName, $qaZipName, $readmeName, $rightsName, $manifestName)
$sumRows = @{}
foreach ($line in [IO.File]::ReadAllLines((Join-Path $releaseDir $sumsName))) {
    if ([string]::IsNullOrWhiteSpace($line)) { continue }
    if ($line -notmatch '^([0-9a-f]{64})  ([A-Za-z0-9_.-]+)$') {
        throw "Malformed SHA256SUMS line: $line"
    }
    if ($sumRows.ContainsKey($Matches[2])) { throw "Duplicate SHA256SUMS filename: $($Matches[2])" }
    $sumRows[$Matches[2]] = $Matches[1]
}
if ((($sumRows.Keys | Sort-Object) -join "`n") -cne (($sumTargets | Sort-Object) -join "`n")) {
    throw 'SHA256SUMS does not cover exactly the seven non-checksum release files.'
}
foreach ($name in $sumTargets) {
    $actual = Get-Sha256 (Join-Path $releaseDir $name)
    if ($actual -cne [string]$sumRows[$name]) { throw "SHA256SUMS mismatch for $name" }
}

$manifestPath = Join-Path $releaseDir $manifestName
$manifestText = [IO.File]::ReadAllText($manifestPath)
Assert-SafeText $manifestText $manifestName
$manifest = $manifestText | ConvertFrom-Json
if ([string]$manifest.schema_version -cne '1.0' -or
    [string]$manifest.release_id -cne 'o012-roberts-id-units-001-013-v0.13.0' -or
    [string]$manifest.title -cne 'Topologi Aljabar: Edisi Bahasa Indonesia — Unit 1–13' -or
    [string]$manifest.version -cne '0.13.0' -or
    [string]$manifest.release_date -cne '2026-08-22' -or
    [string]$manifest.status -cne 'maintained_incomplete_checkpoint') {
    throw 'Release manifest identity/status mismatch.'
}
if ([string]$manifest.metadata_sha256 -notmatch '^[0-9a-f]{64}$') {
    throw 'Release manifest lacks a canonical metadata hash.'
}
if ([string]$manifest.source.author -cne 'David Michael Roberts' -or
    [string]$manifest.source.repository -cne 'https://github.com/DavidMichaelRoberts/AlgebraicTopology2019' -or
    [string]$manifest.source.commit -cne 'b947ad2e9f9e301bfe24590a9db653bc54fa1a53' -or
    [string]$manifest.source.tree -cne 'aa1d3edb85818e7176e2d0bbc06d9b4bd1e247f5' -or
    [string]$manifest.source.path -cne 'Notes.tex' -or
    [int]$manifest.source.line_start -ne 134 -or [int]$manifest.source.line_end -ne 3046) {
    throw 'Release manifest source authority mismatch.'
}
if ([int]$manifest.source.units -ne 13 -or [string]$manifest.source.license -cne 'CC BY 4.0') {
    throw 'Release manifest source scope/license mismatch.'
}

$artifactMap = @{}
foreach ($artifact in @($manifest.artifacts)) {
    $name = [string]$artifact.filename
    if ($artifactMap.ContainsKey($name)) { throw "Duplicate manifest artifact: $name" }
    $artifactMap[$name] = $artifact
}
$manifestArtifactNames = @($pdfName, $htmlName, $sourceZipName, $qaZipName, $readmeName, $rightsName)
if ((($artifactMap.Keys | Sort-Object) -join "`n") -cne (($manifestArtifactNames | Sort-Object) -join "`n")) {
    throw 'Manifest artifact inventory is not exact.'
}
foreach ($name in $manifestArtifactNames) {
    $path = Join-Path $releaseDir $name
    $item = Get-Item -LiteralPath $path
    $row = $artifactMap[$name]
    if ([int64]$row.bytes -ne [int64]$item.Length -or [string]$row.sha256 -cne (Get-Sha256 $path)) {
        throw "Manifest byte/hash mismatch for $name"
    }
}
$artifactSpecs = @{
    $pdfName = @('secondary_print_reader_untagged', 'application/pdf')
    $htmlName = @('primary_offline_semantic_reader', 'text/html')
    $sourceZipName = @('editable_source_and_modular_backend', 'application/zip')
    $qaZipName = @('sanitized_qa_and_provenance', 'application/zip')
    $readmeName = @('release_readme', 'text/markdown')
    $rightsName = @('component_rights_and_attribution', 'text/markdown')
}
foreach ($name in $artifactSpecs.Keys) {
    $row = $artifactMap[$name]
    if ([string]$row.role -cne [string]$artifactSpecs[$name][0] -or
        [string]$row.media_type -cne [string]$artifactSpecs[$name][1]) {
        throw "Manifest role/media-type mismatch for $name"
    }
}

Add-Type -AssemblyName System.IO.Compression
$archiveMap = @{}
$archiveRows = @($manifest.archives)
if ($archiveRows.Count -ne 2) { throw 'Manifest must declare exactly two ZIP archives.' }
foreach ($archive in $archiveRows) {
    $name = [string]$archive.filename
    if ($archiveMap.ContainsKey($name)) { throw "Duplicate manifest ZIP archive: $name" }
    $archiveMap[$name] = $archive
}
if ((($archiveMap.Keys | Sort-Object) -join "`n") -cne ((@($sourceZipName, $qaZipName) | Sort-Object) -join "`n")) {
    throw 'Manifest ZIP archive inventory is not exact.'
}
$sourceExpected = [Collections.Generic.List[string]]::new()
foreach ($name in @('README_RELEASE.md','RELEASE_RIGHTS.md','ATTRIBUTION.md','upstream/Roberts/LICENSE.md','upstream/Roberts/README.md','upstream/Roberts/Notes.tex','source/id-ID/reader-unit-001.md')) { $sourceExpected.Add($name) }
foreach ($number in 2..13) {
    $nnn = $number.ToString('000')
    $sourceExpected.Add("source/id-ID/units/unit-$nnn-lecture-$nnn.md")
}
foreach ($name in @('reader.css','reader-cumulative.css')) { $sourceExpected.Add("source/id-ID/styles/$name") }
foreach ($name in @('artifacts.jsonl','assets.jsonl','authority.jsonl','concepts.jsonl','corrections.jsonl','qa.jsonl','relations.jsonl','rights.jsonl','segments.jsonl','terms.jsonl','units.jsonl')) { $sourceExpected.Add("backend/$name") }
foreach ($name in @('AUTHORITY.json','UPSTREAM_FILE_MANIFEST.csv')) { $sourceExpected.Add("provenance/$name") }

$qaExpected = [Collections.Generic.List[string]]::new()
foreach ($name in @('README_RELEASE.md','RELEASE_RIGHTS.md','zenodo/metadata.json')) { $qaExpected.Add($name) }
foreach ($number in 1..13) {
    $nnn = $number.ToString('000')
    $qaExpected.Add("qa/UNIT_${nnn}_INDEPENDENT_REVIEW.md")
}
foreach ($name in @('UNITS_001_013_QA.json','UNITS_001_013_VISUAL_QA.md','UNITS_001_013_RENDER_INVENTORY.csv','units-001-013-extracted.txt')) { $qaExpected.Add("qa/$name") }
foreach ($name in @('contact-001-012.png','contact-013-024.png','contact-025-036.png','contact-037-048.png','contact-049-060.png','contact-061-072.png','contact-073-084.png','contact-085-096.png','contact-097-108.png','contact-109-120.png','contact-121-132.png','contact-133-138.png')) { $qaExpected.Add("qa/visual-contact-sheets/$name") }
$qaExpected.Add('output/ARTIFACT_MANIFEST_UNITS_001_013.csv')
foreach ($name in @('AUTHORITY.json','UPSTREAM_FILE_MANIFEST.csv','ADVERSE_LEDGER.csv','TERMINOLOGY.csv')) { $qaExpected.Add("provenance/$name") }
$expectedArchiveEntries = @{
    $sourceZipName = @($sourceExpected)
    $qaZipName = @($qaExpected)
}
$archiveFacts = @{}
foreach ($zipName in @($sourceZipName, $qaZipName)) {
    if (-not $archiveMap.ContainsKey($zipName)) { throw "Manifest lacks ZIP inventory for $zipName" }
    $zipPath = Join-Path $releaseDir $zipName
    $zipItem = Get-Item -LiteralPath $zipPath
    $declared = $archiveMap[$zipName]
    if (-not [bool]$declared.verified) { throw "Manifest ZIP is not marked verified: $zipName" }
    if ([int64]$declared.bytes -ne [int64]$zipItem.Length -or [string]$declared.sha256 -cne (Get-Sha256 $zipPath)) {
        throw "Manifest ZIP identity mismatch for $zipName"
    }
    $declaredEntries = @{}
    foreach ($row in @($declared.entries)) {
        $entryName = [string]$row.path
        if ($declaredEntries.ContainsKey($entryName)) { throw "Duplicate declared ZIP entry: $entryName" }
        $declaredEntries[$entryName] = $row
    }
    if ((($declaredEntries.Keys | Sort-Object) -join "`n") -cne (($expectedArchiveEntries[$zipName] | Sort-Object) -join "`n")) {
        throw "ZIP semantic allowlist mismatch for $zipName"
    }
    $facts = @{}
    $actualEntryNames = [Collections.Generic.HashSet[string]]::new([StringComparer]::Ordinal)
    $stream = [IO.File]::OpenRead($zipPath)
    try {
        $zip = [IO.Compression.ZipArchive]::new($stream, [IO.Compression.ZipArchiveMode]::Read, $false)
        try {
            if ($zip.Entries.Count -ne [int]$declared.entry_count -or $zip.Entries.Count -ne $declaredEntries.Count) {
                throw "ZIP entry-count mismatch for $zipName"
            }
            foreach ($entry in $zip.Entries) {
                if (-not $actualEntryNames.Add($entry.FullName)) { throw "Duplicate actual ZIP entry: $($entry.FullName)" }
                if (-not $declaredEntries.ContainsKey($entry.FullName)) { throw "Unexpected ZIP entry: $($entry.FullName)" }
                $entryStream = $entry.Open()
                try {
                    $digest = Get-StreamSha256 $entryStream
                } finally { $entryStream.Dispose() }
                $want = $declaredEntries[$entry.FullName]
                if ([int64]$entry.Length -ne [int64]$want.bytes -or $digest -cne [string]$want.sha256) {
                    throw "ZIP entry byte/hash mismatch: $($entry.FullName)"
                }
                $facts[$entry.FullName] = [ordered]@{
                    bytes = [int64]$entry.Length
                    sha256 = $digest
                }
                if ($entry.FullName -match '\.(md|json|jsonl|csv|txt|tex|css|html)$') {
                    $textStream = $entry.Open()
                    try {
                        $reader = [IO.StreamReader]::new($textStream, [Text.UTF8Encoding]::new($false), $true)
                        try { $text = $reader.ReadToEnd() } finally { $reader.Dispose() }
                    } finally { $textStream.Dispose() }
                    Assert-SafeText $text "$zipName::$($entry.FullName)"
                } else {
                    Assert-SafeBinary (Get-ZipEntryBytes $zipPath $entry.FullName) "$zipName::$($entry.FullName)"
                }
            }
        } finally { $zip.Dispose() }
    } finally { $stream.Dispose() }
    if ((($actualEntryNames | Sort-Object) -join "`n") -cne (($expectedArchiveEntries[$zipName] | Sort-Object) -join "`n")) {
        throw "Actual ZIP entry set does not equal the semantic allowlist for $zipName"
    }
    $archiveFacts[$zipName] = $facts
}

foreach ($name in @($htmlName, $readmeName, $rightsName, $manifestName, $sumsName)) {
    Assert-SafeText ([IO.File]::ReadAllText((Join-Path $releaseDir $name))) $name
}
Assert-SafeBinary ([IO.File]::ReadAllBytes((Join-Path $releaseDir $pdfName))) $pdfName

foreach ($name in @($readmeName, $rightsName)) {
    $topHash = Get-Sha256 (Join-Path $releaseDir $name)
    foreach ($zipName in @($sourceZipName, $qaZipName)) {
        if ([string]$archiveFacts[$zipName][$name].sha256 -cne $topHash) {
            throw "$name is not byte-identical between the top-level release and $zipName."
        }
    }
}

$qaZipPath = Join-Path $releaseDir $qaZipName
$sourceZipPath = Join-Path $releaseDir $sourceZipName
$qaReceiptEntry = 'qa/UNITS_001_013_QA.json'
$metadataEntry = 'zenodo/metadata.json'
$qaBytes = Get-ZipEntryBytes $qaZipPath $qaReceiptEntry
$metadataBytes = Get-ZipEntryBytes $qaZipPath $metadataEntry
$qaDocument = [Text.Encoding]::UTF8.GetString($qaBytes) | ConvertFrom-Json
$metadataDocument = [Text.Encoding]::UTF8.GetString($metadataBytes) | ConvertFrom-Json

if ((Get-BytesSha256 $qaBytes) -cne [string]$manifest.reader_qa.receipt_sha256) {
    throw 'Manifest QA receipt hash does not bind the embedded QA receipt.'
}
if ((Get-BytesSha256 $metadataBytes) -cne [string]$manifest.metadata_sha256) {
    throw 'Manifest metadata hash does not bind the embedded Zenodo metadata.'
}
if ([string]$metadataDocument.metadata.title -cne [string]$manifest.title -or
    [string]$metadataDocument.metadata.version -cne [string]$manifest.version -or
    [string]$metadataDocument.metadata.license -cne 'cc-by-4.0' -or
    [string]$metadataDocument.metadata.language -cne 'ind') {
    throw 'Embedded Zenodo metadata identity/license/language mismatch.'
}

if ([string]$qaDocument.status -cne 'pass' -or
    -not [bool]$qaDocument.gates.html_two_build_byte_identity -or
    -not [bool]$qaDocument.gates.pdf_two_build_fail_closed_gate_in_builder -or
    [string]$qaDocument.gates.visual_review -cne 'pass_all_138_pages_plus_browser_desktop_mobile') {
    throw 'Embedded cumulative QA receipt does not close every release gate.'
}
if ([string]$manifest.reader_qa.status -cne 'pass' -or
    [int]$manifest.reader_qa.html_stable_ids -ne [int]$qaDocument.html.stable_ids -or
    [int]$manifest.reader_qa.html_ids -ne [int]$qaDocument.html.ids -or
    [int]$manifest.reader_qa.html_mathml_nodes -ne [int]$qaDocument.html.mathml_nodes -or
    [int]$manifest.reader_qa.pdf_pages -ne [int]$qaDocument.pdf.pages -or
    [bool]$manifest.reader_qa.pdf_tagged -ne [bool]$qaDocument.pdf.tagged -or
    [string]$manifest.reader_qa.visual_review -cne [string]$qaDocument.gates.visual_review) {
    throw 'Manifest reader-QA census is not bound to the embedded QA receipt.'
}
$qaArtifacts = @{}
foreach ($row in @($qaDocument.artifacts)) { $qaArtifacts[[string]$row.path] = $row }
$qaHtml = $qaArtifacts['output/html/units-001-013/index.html']
$qaPdf = $qaArtifacts['output/pdf/topologi-aljabar-unit-001-013-id.pdf']
if ($null -eq $qaHtml -or $null -eq $qaPdf) { throw 'QA receipt lacks reader artifacts.' }
if ([int64]$qaHtml.bytes -ne (Get-Item -LiteralPath (Join-Path $releaseDir $htmlName)).Length -or
    [string]$qaHtml.sha256 -cne (Get-Sha256 (Join-Path $releaseDir $htmlName)) -or
    [int64]$qaPdf.bytes -ne (Get-Item -LiteralPath (Join-Path $releaseDir $pdfName)).Length -or
    [string]$qaPdf.sha256 -cne (Get-Sha256 (Join-Path $releaseDir $pdfName))) {
    throw 'Published-reader candidates are not the bytes bound by cumulative QA.'
}

$backendNames = @('artifacts.jsonl','assets.jsonl','authority.jsonl','concepts.jsonl','corrections.jsonl','qa.jsonl','relations.jsonl','rights.jsonl','segments.jsonl','terms.jsonl','units.jsonl')
if ([int]$manifest.backend.files -ne $backendNames.Count -or [int]$manifest.backend.records -ne 1762 -or
    [string]$manifest.backend.validator_bundle_sha256 -cne 'bb8512f56a8bbcf1283ae10ab69a9a7ecebb1bd39c425c1c021b5b848a1b2910') {
    throw 'Manifest backend census/bundle identity mismatch.'
}
$backendRows = @{}
foreach ($row in @($manifest.backend.inventory)) {
    $name = [string]$row.filename
    if ($backendRows.ContainsKey($name)) { throw "Duplicate backend inventory row: $name" }
    $backendRows[$name] = $row
}
if ((($backendRows.Keys | Sort-Object) -join "`n") -cne (($backendNames | Sort-Object) -join "`n")) {
    throw 'Manifest backend file inventory is not exact.'
}
$backendBytesTotal = 0L
$backendRecordsTotal = 0
$bundleStream = [IO.MemoryStream]::new()
try {
    foreach ($name in ($backendNames | Sort-Object)) {
        $entryName = "backend/$name"
        $bytes = Get-ZipEntryBytes $sourceZipPath $entryName
        $digest = Get-BytesSha256 $bytes
        $text = [Text.Encoding]::UTF8.GetString($bytes)
        $recordCount = @($text -split "\r?\n" | Where-Object { -not [string]::IsNullOrWhiteSpace($_) }).Count
        $row = $backendRows[$name]
        if ([int64]$row.bytes -ne [int64]$bytes.Length -or [string]$row.sha256 -cne $digest -or
            [int]$row.records -ne $recordCount) {
            throw "Manifest backend row mismatch for $name"
        }
        $backendBytesTotal += [int64]$bytes.Length
        $backendRecordsTotal += $recordCount
        $nameBytes = [Text.Encoding]::UTF8.GetBytes($name)
        $bundleStream.Write($nameBytes, 0, $nameBytes.Length)
        $bundleStream.WriteByte(0)
        $bundleStream.Write($bytes, 0, $bytes.Length)
    }
    $bundleStream.Position = 0
    $bundleHash = Get-StreamSha256 $bundleStream
} finally { $bundleStream.Dispose() }
if ($backendBytesTotal -ne [int64]$manifest.backend.bytes -or
    $backendRecordsTotal -ne [int]$manifest.backend.records -or
    $bundleHash -cne [string]$manifest.backend.validator_bundle_sha256) {
    throw 'Embedded backend does not reproduce the manifest census/bundle hash.'
}

[pscustomobject]@{
    Status = 'PASS'
    ReleaseDirectory = $releaseDir
    FileCount = $expectedNames.Count
    HtmlSHA256 = Get-Sha256 (Join-Path $releaseDir $htmlName)
    PdfSHA256 = Get-Sha256 (Join-Path $releaseDir $pdfName)
    SourceZipSHA256 = Get-Sha256 (Join-Path $releaseDir $sourceZipName)
    QaZipSHA256 = Get-Sha256 (Join-Path $releaseDir $qaZipName)
    ManifestSHA256 = Get-Sha256 $manifestPath
}
