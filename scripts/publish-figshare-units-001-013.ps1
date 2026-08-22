#requires -Version 7.0
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$SecretPath
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$lane = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$zenodoReleaseRoot = Join-Path $lane 'release\zenodo-units-001-013'
$artifactsDir = Join-Path $zenodoReleaseRoot 'artifacts'
$metadataPath = Join-Path $zenodoReleaseRoot 'metadata.json'
$verifyScript = Join-Path $PSScriptRoot 'verify-zenodo-units-001-013.ps1'
$zenodoReceiptPath = Join-Path $lane '00_control\ZENODO_PUBLICATION_RECEIPT_UNITS_001_013.json'
$figshareReleaseRoot = Join-Path $lane 'release\figshare-units-001-013'
$transactionPath = Join-Path $figshareReleaseRoot 'transaction.json'
$receiptPath = Join-Path $lane '00_control\FIGSHARE_PUBLICATION_RECEIPT_UNITS_001_013.json'
$sharedLockPath = Join-Path $zenodoReleaseRoot '.release-operation.lock'
$secretPath = [IO.Path]::GetFullPath($SecretPath)

$apiRoot = 'https://api.figshare.com/v2'
$projectId = 280296
$collectionId = 8668413
$expectedProjectTitle = 'Open and Share-Alike Educational Materials — Translations'
$expectedCollectionTitle = 'Indonesian Open Mathematics Editions'
$releaseId = 'o012-roberts-id-units-001-013-v0.13.0'
$workTag = 'o012-roberts-id'
$expectedTitle = 'Topologi Aljabar: Edisi Bahasa Indonesia — Unit 1–13'
$expectedVersion = '0.13.0'
$expectedLicenseName = 'CC BY 4.0'
$expectedLicenseUrl = 'https://creativecommons.org/licenses/by/4.0/'
$expectedLicenseId = 1
$sourceUrl = 'https://github.com/DavidMichaelRoberts/AlgebraicTopology2019/tree/b947ad2e9f9e301bfe24590a9db653bc54fa1a53'
$zenodoReleaseNames = @(
    '00_TOPOLOGI_ALJABAR_ID_UNIT_001_013_READER.pdf',
    'TOPOLOGI_ALJABAR_ID_UNIT_001_013_READER.html',
    'TOPOLOGI_ALJABAR_ID_UNIT_001_013_EDITABLE_SOURCE_BACKEND.zip',
    'TOPOLOGI_ALJABAR_ID_UNIT_001_013_QA_PROVENANCE.zip',
    'README_RELEASE.md',
    'RELEASE_RIGHTS.md',
    'release-manifest.json',
    'SHA256SUMS'
)
$releaseNames = @(
    '00_TOPOLOGI_ALJABAR_ID_UNIT_001_013_READER.pdf',
    'TOPOLOGI_ALJABAR_ID_UNIT_001_013_READER.html',
    'TOPOLOGI_ALJABAR_ID_UNIT_001_013_EDITABLE_SOURCE_BACKEND.zip',
    'RELEASE_RIGHTS.md',
    'release-manifest.json',
    'SHA256SUMS',
    'README_RELEASE.md'
)
$maximumFigsharePayloadBytes = [int64]500000000
$maximumProjectBytes = [int64]20000000000
$transactionSchemaVersion = '2.0'
$transactionMode = 'create_new_in_project'
$transactionStates = @(
    'create_request_intent',
    'created_in_project',
    'metadata_verified',
    'files_verified',
    'article_publish_intent',
    'article_published',
    'collection_append_intent',
    'collection_membership_appended',
    'collection_publish_intent',
    'collection_published',
    'published_collected_and_anonymously_verified'
)
$irreversibleIntentStates = @(
    'create_request_intent',
    'article_publish_intent',
    'collection_append_intent',
    'collection_publish_intent'
)
$script:activeToken = $null
$script:activeTokenBytes = $null
$script:activeTokenPrefix = $null

function Get-Sha256([string]$Path) {
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}

function Get-Md5([string]$Path) {
    return (Get-FileHash -LiteralPath $Path -Algorithm MD5).Hash.ToLowerInvariant()
}

function Get-TextSha256([string]$Text) {
    $bytes = [Text.Encoding]::UTF8.GetBytes($Text)
    $hash = [Security.Cryptography.SHA256]::HashData($bytes)
    return [Convert]::ToHexString($hash).ToLowerInvariant()
}

function Get-PropertyValue([object]$Object, [string]$Name) {
    if ($null -eq $Object) { return $null }
    $property = $Object.PSObject.Properties[$Name]
    if ($null -eq $property) { return $null }
    return $property.Value
}

function Set-PropertyValue([object]$Object, [string]$Name, [object]$Value) {
    if ($Object -is [Collections.IDictionary]) {
        $Object[$Name] = $Value
    } else {
        $Object | Add-Member -NotePropertyName $Name -NotePropertyValue $Value -Force
    }
}

function Write-JsonAtomic([string]$Path, [object]$Value) {
    $directory = Split-Path -Parent $Path
    if (-not (Test-Path -LiteralPath $directory -PathType Container)) {
        New-Item -ItemType Directory -Path $directory | Out-Null
    }
    $json = ($Value | ConvertTo-Json -Depth 30) + "`n"
    Assert-TextDoesNotContainToken $json 'JSON persistence payload'
    $temporary = "$Path.$([guid]::NewGuid().ToString('N')).tmp"
    try {
        [IO.File]::WriteAllText(
            $temporary,
            $json,
            [Text.UTF8Encoding]::new($false)
        )
        Move-Item -LiteralPath $temporary -Destination $Path -Force
    } finally {
        if (Test-Path -LiteralPath $temporary) { Remove-Item -LiteralPath $temporary -Force }
    }
}

function Assert-FigshareReleaseChild([string]$Path) {
    $full = [IO.Path]::GetFullPath($Path)
    $prefix = [IO.Path]::GetFullPath($figshareReleaseRoot).TrimEnd('\') + '\'
    if (-not $full.StartsWith($prefix, [StringComparison]::OrdinalIgnoreCase)) {
        throw "Refusing temporary path outside the Figshare release root: $full"
    }
}

function Get-SecretToken([string]$Path) {
    $text = [IO.File]::ReadAllText($Path)
    $candidates = [Collections.Generic.List[string]]::new()
    foreach ($line in ($text -split "\r?\n")) {
        $trimmed = $line.Trim().Trim('`')
        if ($trimmed -match '^(?i)(?:[-*]\s*)?(?:figshare\s+)?(?:personal\s+access\s+|access\s+)?token\s*[:=]\s*([A-Za-z0-9._~-]{30,})\s*$') {
            $candidates.Add($Matches[1])
        } elseif ($trimmed -match '^[A-Za-z0-9][A-Za-z0-9._~-]{39,}$') {
            $candidates.Add($trimmed)
        }
    }
    $unique = @($candidates | Sort-Object -Unique)
    if ($unique.Count -ne 1) {
        throw 'Figshare credential file must contain exactly one unambiguous token value.'
    }
    return $unique[0]
}

function Set-ActiveTokenScanner([string]$Token) {
    if ([string]::IsNullOrEmpty($Token)) { throw 'Cannot initialize an empty credential scanner.' }
    $script:activeToken = $Token
    $script:activeTokenBytes = [Text.Encoding]::UTF8.GetBytes($Token)
    $prefix = [int[]]::new($script:activeTokenBytes.Length)
    $matched = 0
    for ($index = 1; $index -lt $script:activeTokenBytes.Length; $index++) {
        while ($matched -gt 0 -and $script:activeTokenBytes[$index] -ne $script:activeTokenBytes[$matched]) {
            $matched = $prefix[$matched - 1]
        }
        if ($script:activeTokenBytes[$index] -eq $script:activeTokenBytes[$matched]) { $matched++ }
        $prefix[$index] = $matched
    }
    $script:activeTokenPrefix = $prefix
}

function Assert-StreamDoesNotContainToken([IO.Stream]$Stream, [string]$Label) {
    if ($null -eq $script:activeTokenBytes) { return }
    $buffer = [byte[]]::new(65536)
    $matched = 0
    while (($count = $Stream.Read($buffer, 0, $buffer.Length)) -gt 0) {
        for ($index = 0; $index -lt $count; $index++) {
            while ($matched -gt 0 -and $buffer[$index] -ne $script:activeTokenBytes[$matched]) {
                $matched = $script:activeTokenPrefix[$matched - 1]
            }
            if ($buffer[$index] -eq $script:activeTokenBytes[$matched]) { $matched++ }
            if ($matched -eq $script:activeTokenBytes.Length) {
                throw "Credential material is present in $Label."
            }
        }
    }
}

function Assert-BytesDoNotContainToken([byte[]]$Bytes, [string]$Label) {
    if ($null -eq $script:activeTokenBytes) { return }
    $stream = [IO.MemoryStream]::new($Bytes, $false)
    try { Assert-StreamDoesNotContainToken $stream $Label }
    finally { $stream.Dispose() }
}

function Assert-TextDoesNotContainToken([string]$Text, [string]$Label) {
    if ($null -eq $script:activeTokenBytes -or $null -eq $Text) { return }
    Assert-BytesDoNotContainToken ([Text.Encoding]::UTF8.GetBytes($Text)) $Label
}

function Assert-FileDoesNotContainToken([string]$Path, [string]$Label) {
    if ($null -eq $script:activeTokenBytes) { return }
    $stream = [IO.File]::Open($Path, [IO.FileMode]::Open, [IO.FileAccess]::Read, [IO.FileShare]::Read)
    try { Assert-StreamDoesNotContainToken $stream $Label }
    finally { $stream.Dispose() }
}

function Assert-ZipEntriesDoNotContainToken([string]$Path, [string]$ArchiveLabel) {
    $archive = [IO.Compression.ZipFile]::OpenRead($Path)
    try {
        foreach ($entry in $archive.Entries) {
            if ([string]::IsNullOrEmpty($entry.Name)) { continue }
            $stream = $entry.Open()
            try { Assert-StreamDoesNotContainToken $stream "$ArchiveLabel decompressed ZIP entry" }
            finally { $stream.Dispose() }
        }
    } finally {
        $archive.Dispose()
    }
}

function Assert-AllLocalTextAndPayloadTokenFree(
    [string]$MetadataText,
    [string]$ReceiptText,
    [string]$TransactionText,
    [string]$ArticleBody
) {
    foreach ($name in $zenodoReleaseNames) {
        $path = Join-Path $artifactsDir $name
        Assert-FileDoesNotContainToken $path "top-level release artifact $name"
        if ([IO.Path]::GetExtension($name) -ceq '.zip') {
            Assert-ZipEntriesDoNotContainToken $path $name
        }
    }
    Assert-TextDoesNotContainToken $MetadataText 'external metadata.json text'
    Assert-TextDoesNotContainToken $ReceiptText 'Zenodo receipt text'
    if ($null -ne $TransactionText) { Assert-TextDoesNotContainToken $TransactionText 'Figshare transaction text' }
    Assert-TextDoesNotContainToken $ArticleBody 'derived Figshare article body'
}

function Assert-ExactLocalInventory {
    $actual = @(Get-ChildItem -LiteralPath $artifactsDir -File | ForEach-Object Name | Sort-Object)
    if (($actual -join "`n") -cne (($zenodoReleaseNames | Sort-Object) -join "`n")) {
        throw 'Local release inventory is not the exact eight-file allowlist.'
    }
}

function Get-ExpectedLocalFiles([array]$Names) {
    return @($Names | ForEach-Object {
        $path = Join-Path $artifactsDir $_
        [ordered]@{
            filename = $_
            bytes = [int64](Get-Item -LiteralPath $path).Length
            md5 = Get-Md5 $path
            sha256 = Get-Sha256 $path
        }
    })
}

function Get-ImmutableInputSnapshot {
    foreach ($path in @($metadataPath, $verifyScript, $zenodoReceiptPath)) {
        if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { throw "Missing required release input: $path" }
    }
    if (-not (Test-Path -LiteralPath $artifactsDir -PathType Container)) {
        throw "Missing packaged release directory: $artifactsDir"
    }
    Assert-ExactLocalInventory
    return [ordered]@{
        schema_version = '1.0'
        artifacts = @(Get-ExpectedLocalFiles $zenodoReleaseNames)
        metadata = [ordered]@{
            bytes = [int64](Get-Item -LiteralPath $metadataPath).Length
            sha256 = Get-Sha256 $metadataPath
        }
        zenodo_receipt = [ordered]@{
            bytes = [int64](Get-Item -LiteralPath $zenodoReceiptPath).Length
            sha256 = Get-Sha256 $zenodoReceiptPath
        }
        verifier = [ordered]@{
            bytes = [int64](Get-Item -LiteralPath $verifyScript).Length
            sha256 = Get-Sha256 $verifyScript
        }
    }
}

function Convert-SnapshotToCanonicalText([object]$Snapshot) {
    return ($Snapshot | ConvertTo-Json -Depth 20 -Compress)
}

function Assert-ZenodoReceipt([object]$Receipt, [array]$ExpectedFiles) {
    if ([string](Get-PropertyValue $Receipt 'release_id') -cne $releaseId -or
        [string](Get-PropertyValue $Receipt 'title') -cne $expectedTitle -or
        [string](Get-PropertyValue $Receipt 'version') -cne $expectedVersion -or
        [string](Get-PropertyValue $Receipt 'license') -cne $expectedLicenseName -or
        -not [bool](Get-PropertyValue $Receipt 'incomplete_checkpoint') -or
        [int](Get-PropertyValue $Receipt 'public_file_count') -ne $zenodoReleaseNames.Count) {
        throw 'Zenodo receipt identity, scope, license, or file-count gate failed.'
    }
    $verification = Get-PropertyValue $Receipt 'verification'
    foreach ($gate in @('exact_public_inventory','anonymous_byte_readback','all_sha256_match_local')) {
        if (-not [bool](Get-PropertyValue $verification $gate)) {
            throw "Zenodo receipt lacks required verified gate: $gate"
        }
    }
    $doi = [string](Get-PropertyValue $Receipt 'doi')
    $recordUrl = [string](Get-PropertyValue $Receipt 'public_record_url')
    if ($doi -notmatch '^10\.5281/zenodo\.[0-9]+$') { throw 'Zenodo receipt DOI is missing or malformed.' }
    $recordUri = [uri]$recordUrl
    if ($recordUri.Scheme -cne 'https' -or $recordUri.Host -cne 'zenodo.org') {
        throw 'Zenodo receipt public URL is not an HTTPS zenodo.org record URL.'
    }
    $receiptFiles = @((Get-PropertyValue $Receipt 'files') | Sort-Object filename)
    $expectedSorted = @($ExpectedFiles | Sort-Object filename)
    $receiptNames = (($receiptFiles | ForEach-Object filename) -join "`n")
    $expectedNames = (($expectedSorted | ForEach-Object filename) -join "`n")
    if ($receiptNames -cne $expectedNames) {
        throw 'Zenodo receipt file inventory does not match the exact local release.'
    }
    for ($index = 0; $index -lt $expectedSorted.Count; $index++) {
        $expected = $expectedSorted[$index]
        $remote = $receiptFiles[$index]
        if ([int64]$remote.bytes -ne [int64]$expected.bytes -or
            [string]$remote.sha256 -cne [string]$expected.sha256 -or
            -not [bool]$remote.verified) {
            throw "Zenodo receipt byte/SHA-256 gate failed for $($expected.filename)."
        }
    }
}

$script:headers = $null
$script:lastRequestAt = [DateTimeOffset]::MinValue

function Wait-RequestSlot {
    $minimumIntervalMs = 1100
    $elapsed = ([DateTimeOffset]::UtcNow - $script:lastRequestAt).TotalMilliseconds
    if ($elapsed -lt $minimumIntervalMs) {
        Start-Sleep -Milliseconds ([int][Math]::Ceiling($minimumIntervalMs - $elapsed))
    }
    $script:lastRequestAt = [DateTimeOffset]::UtcNow
}

function Convert-ResponseJson([object]$Response, [string]$Label) {
    if ([string]::IsNullOrWhiteSpace([string]$Response.Content)) { return $null }
    try { return ([string]$Response.Content | ConvertFrom-Json) }
    catch { throw "Figshare returned non-JSON content for $Label (HTTP $([int]$Response.StatusCode))." }
}

function Invoke-FigshareRequest {
    param(
        [Parameter(Mandatory = $true)][ValidateSet('GET','POST','PUT','DELETE')][string]$Method,
        [Parameter(Mandatory = $true)][string]$Uri,
        [Parameter(Mandatory = $true)][string]$Label,
        [bool]$Authenticated = $true,
        [string]$JsonBody,
        [int[]]$AllowedStatus = @(200)
    )
    Assert-TextDoesNotContainToken $Uri 'Figshare request URI'
    Assert-TextDoesNotContainToken $Label 'Figshare request label'
    if ($PSBoundParameters.ContainsKey('JsonBody')) {
        Assert-TextDoesNotContainToken $JsonBody 'Figshare JSON request body'
    }
    $parsed = [uri]$Uri
    if ($parsed.Scheme -cne 'https' -or $parsed.Host -cne 'api.figshare.com') {
        throw "Refusing non-API Figshare URI for $Label."
    }
    $arguments = @{
        Method = $Method
        Uri = $Uri
        SkipHttpErrorCheck = $true
        MaximumRedirection = 0
        TimeoutSec = 120
    }
    if ($Authenticated) { $arguments.Headers = $script:headers }
    if ($PSBoundParameters.ContainsKey('JsonBody')) {
        $arguments.ContentType = 'application/json; charset=utf-8'
        $arguments.Body = [Text.Encoding]::UTF8.GetBytes($JsonBody)
    }
    Wait-RequestSlot
    $response = Invoke-WebRequest @arguments
    if ($AllowedStatus -notcontains [int]$response.StatusCode) {
        throw "Figshare request failed for $Label (HTTP $([int]$response.StatusCode))."
    }
    return [pscustomobject]@{
        StatusCode = [int]$response.StatusCode
        Json = Convert-ResponseJson $response $Label
        Headers = $response.Headers
    }
}

function Invoke-UploadServiceRequest {
    param(
        [Parameter(Mandatory = $true)][ValidateSet('GET','PUT')][string]$Method,
        [Parameter(Mandatory = $true)][string]$Uri,
        [Parameter(Mandatory = $true)][string]$Label,
        [byte[]]$Bytes,
        [int[]]$AllowedStatus = @(200)
    )
    Assert-TextDoesNotContainToken $Uri 'Figshare upload-service request URI'
    Assert-TextDoesNotContainToken $Label 'Figshare upload-service request label'
    if ($PSBoundParameters.ContainsKey('Bytes')) {
        Assert-BytesDoNotContainToken $Bytes 'Figshare upload-service request bytes'
    }
    $parsed = [uri]$Uri
    if ($parsed.Scheme -cne 'https' -or $parsed.Host -cne 'uploads.figshare.com') {
        throw "Refusing unexpected Figshare upload-service URI for $Label."
    }
    $arguments = @{
        Method = $Method
        Uri = $Uri
        Headers = $script:headers
        SkipHttpErrorCheck = $true
        MaximumRedirection = 0
        TimeoutSec = 120
    }
    if ($PSBoundParameters.ContainsKey('Bytes')) {
        $arguments.ContentType = 'application/octet-stream'
        $arguments.Body = $Bytes
    }
    Wait-RequestSlot
    $response = Invoke-WebRequest @arguments
    if ($AllowedStatus -notcontains [int]$response.StatusCode) {
        throw "Figshare upload request failed for $Label (HTTP $([int]$response.StatusCode))."
    }
    return [pscustomobject]@{
        StatusCode = [int]$response.StatusCode
        Json = Convert-ResponseJson $response $Label
    }
}

function Invoke-AnonymousDownload([string]$Uri, [string]$Destination, [string]$Label) {
    Assert-TextDoesNotContainToken $Uri 'anonymous Figshare download URI'
    Assert-TextDoesNotContainToken $Label 'anonymous Figshare download label'
    $parsed = [uri]$Uri
    if ($parsed.Scheme -cne 'https' -or $parsed.Host -cne 'ndownloader.figshare.com') {
        throw "Refusing unexpected anonymous download URI for $Label."
    }
    Wait-RequestSlot
    $response = Invoke-WebRequest -Method GET -Uri $Uri -OutFile $Destination -PassThru -SkipHttpErrorCheck -MaximumRedirection 5 -TimeoutSec 120
    if ([int]$response.StatusCode -notin @(200,206)) {
        throw "Anonymous Figshare download failed for $Label (HTTP $([int]$response.StatusCode))."
    }
}

function Get-ObjectId([object]$Object) {
    foreach ($name in @('id','entity_id','article_id')) {
        $value = [string](Get-PropertyValue $Object $name)
        if ($value -match '^[0-9]+$') { return [int64]$value }
    }
    return [int64]0
}

function Get-ResponseEntityId([object]$Response) {
    $id = Get-ObjectId $Response.Json
    if ($id -gt 0) { return $id }
    $location = [string](Get-PropertyValue $Response.Json 'location')
    if ([string]::IsNullOrWhiteSpace($location)) {
        $location = [string](Get-PropertyValue $Response.Headers 'Location')
    }
    if ($location -match '/([0-9]+)(?:/)?$') { return [int64]$Matches[1] }
    throw 'Figshare create response did not expose a usable entity ID.'
}

function Get-AllProjectArticles([bool]$Authenticated) {
    $items = [Collections.Generic.List[object]]::new()
    for ($page = 1; $page -le 100; $page++) {
        $path = if ($Authenticated) { 'account/projects' } else { 'projects' }
        $response = Invoke-FigshareRequest -Method GET -Uri "$apiRoot/$path/$projectId/articles?page=$page&page_size=100" -Label 'bounded project article listing' -Authenticated $Authenticated
        $batch = @($response.Json)
        foreach ($item in $batch) { if ($null -ne $item) { $items.Add($item) } }
        if ($batch.Count -lt 100) { break }
        if ($page -eq 100) { throw 'Project article listing exceeded its bounded pagination limit.' }
    }
    return @($items)
}

function Get-AllAuthenticatedArticleFiles([int64]$ArticleId) {
    $items = [Collections.Generic.List[object]]::new()
    for ($page = 1; $page -le 100; $page++) {
        $response = Invoke-FigshareRequest -Method GET -Uri "$apiRoot/account/articles/$ArticleId/files?page=$page&page_size=100" -Label 'bounded authenticated project-article file listing'
        $batch = @($response.Json)
        foreach ($item in $batch) { if ($null -ne $item) { $items.Add($item) } }
        if ($batch.Count -lt 100) { break }
        if ($page -eq 100) { throw 'Authenticated article file listing exceeded its bounded pagination limit.' }
    }
    return @($items)
}

function Get-AuthenticatedProjectByteInventory {
    $articles = @(Get-AllProjectArticles $true)
    $seen = @{}
    $totalBytes = [int64]0
    $articleRows = [Collections.Generic.List[object]]::new()
    foreach ($article in $articles) {
        $id = Get-ObjectId $article
        if ($id -le 0 -or $seen.ContainsKey([string]$id)) {
            throw 'Authenticated project inventory contains a missing or duplicate article ID.'
        }
        $seen[[string]$id] = $true
        $articleBytes = [int64]0
        $files = @(Get-AllAuthenticatedArticleFiles $id)
        foreach ($file in $files) {
            $size = Get-RemoteFileBytes $file
            if ($size -lt 0) { throw 'Authenticated project inventory exposed a negative file size.' }
            $articleBytes += $size
        }
        $totalBytes += $articleBytes
        $articleRows.Add([pscustomobject]@{
            ArticleId = [int64]$id
            Bytes = [int64]$articleBytes
            FileCount = [int]$files.Count
        })
    }
    return [pscustomobject]@{
        ArticleCount = $articles.Count
        Bytes = $totalBytes
        Articles = @($articleRows)
    }
}

function Assert-AuthenticatedProjectCapacity([int64]$ArticleId, [int64]$PayloadBytes) {
    $inventory = Get-AuthenticatedProjectByteInventory
    $targetRows = @($inventory.Articles | Where-Object { $_.ArticleId -eq $ArticleId })
    if ($ArticleId -gt 0 -and $targetRows.Count -ne 1) {
        throw 'Target article is not represented exactly once in authenticated project quota inventory.'
    }
    if ($ArticleId -le 0 -and $targetRows.Count -ne 0) {
        throw 'Unbound target unexpectedly appears in authenticated project quota inventory.'
    }
    $targetCurrentBytes = if ($targetRows.Count -eq 1) { [int64]$targetRows[0].Bytes } else { [int64]0 }
    $projected = [int64]$inventory.Bytes - $targetCurrentBytes + $PayloadBytes
    if ($projected -ge $maximumProjectBytes) {
        throw 'Publishing this payload would make authenticated project 280296 reach or exceed the strict 20,000,000,000-byte ceiling.'
    }
    return [pscustomobject]@{
        CurrentBytes = [int64]$inventory.Bytes
        ProjectedBytes = $projected
        TargetCurrentBytes = $targetCurrentBytes
        ArticleCount = [int]$inventory.ArticleCount
    }
}

function Get-AllCollectionArticles([bool]$Authenticated) {
    $items = [Collections.Generic.List[object]]::new()
    for ($page = 1; $page -le 100; $page++) {
        $path = if ($Authenticated) { 'account/collections' } else { 'collections' }
        $response = Invoke-FigshareRequest -Method GET -Uri "$apiRoot/$path/$collectionId/articles?page=$page&page_size=100" -Label 'bounded collection article listing' -Authenticated $Authenticated
        $batch = @($response.Json)
        foreach ($item in $batch) { if ($null -ne $item) { $items.Add($item) } }
        if ($batch.Count -lt 100) { break }
        if ($page -eq 100) { throw 'Collection article listing exceeded its bounded pagination limit.' }
    }
    return @($items)
}

function Search-OwnArticles([string]$Term) {
    $items = [Collections.Generic.List[object]]::new()
    for ($page = 1; $page -le 20; $page++) {
        $body = [ordered]@{
            search_for = $Term
            page = $page
            page_size = 100
            order = 'created_date'
            order_direction = 'desc'
        } | ConvertTo-Json -Compress
        $response = Invoke-FigshareRequest -Method POST -Uri "$apiRoot/account/articles/search" -Label 'bounded authenticated own-article search' -JsonBody $body
        $batch = @($response.Json)
        foreach ($item in $batch) { if ($null -ne $item) { $items.Add($item) } }
        if ($batch.Count -lt 100) { break }
        if ($page -eq 20) { throw 'Own-article search exceeded its bounded pagination limit.' }
    }
    return @($items)
}

function Get-ArticleAuthorNames([object]$Article) {
    return @((Get-PropertyValue $Article 'authors') | ForEach-Object {
        $fullName = [string](Get-PropertyValue $_ 'full_name')
        if (-not [string]::IsNullOrWhiteSpace($fullName)) { $fullName }
        else { [string](Get-PropertyValue $_ 'name') }
    })
}

function Test-SameWork([object]$Article, [string]$ZenodoUrl) {
    $title = [string](Get-PropertyValue $Article 'title')
    $tags = @((Get-PropertyValue $Article 'tags') | ForEach-Object { [string]$_ })
    $references = @((Get-PropertyValue $Article 'references') | ForEach-Object { [string]$_ })
    $authors = @(Get-ArticleAuthorNames $Article)
    $hasRoberts = @($authors | Where-Object { $_ -in @('David Michael Roberts','Roberts, David Michael') }).Count -gt 0
    $hasIdentity = ($tags -ccontains $workTag) -or ($tags -ccontains $releaseId) -or ($references -ccontains $sourceUrl) -or ($references -ccontains $ZenodoUrl)
    return (
        $title.StartsWith('Topologi Aljabar:', [StringComparison]::Ordinal) -and
        $hasRoberts -and
        $hasIdentity
    )
}

function Test-SuspiciousCandidate([object]$Article) {
    $title = [string](Get-PropertyValue $Article 'title')
    $tags = @((Get-PropertyValue $Article 'tags') | ForEach-Object { [string]$_ })
    return $title.StartsWith('Topologi Aljabar', [StringComparison]::OrdinalIgnoreCase) -or
        ($tags -contains $workTag) -or ($tags -contains $releaseId)
}

function Get-PublicArticle([int64]$ArticleId, [int[]]$AllowedStatus = @(200,404)) {
    return Invoke-FigshareRequest -Method GET -Uri "$apiRoot/articles/$ArticleId" -Label 'anonymous article readback' -Authenticated $false -AllowedStatus $AllowedStatus
}

function Get-RemoteFileName([object]$File) {
    return [string](Get-PropertyValue $File 'name')
}

function Get-RemoteFileBytes([object]$File) {
    return [int64](Get-PropertyValue $File 'size')
}

function Get-RemoteFileMd5([object]$File) {
    $computed = [string](Get-PropertyValue $File 'computed_md5')
    if (-not [string]::IsNullOrWhiteSpace($computed)) { return $computed.ToLowerInvariant() }
    return ([string](Get-PropertyValue $File 'supplied_md5')).ToLowerInvariant()
}

function Assert-PublicArticleIdentity([object]$Article) {
    if ([string](Get-PropertyValue $Article 'title') -cne $expectedTitle) {
        throw 'Anonymous Figshare title readback mismatch.'
    }
    $license = Get-PropertyValue $Article 'license'
    if ([int](Get-PropertyValue $license 'value') -ne $expectedLicenseId -or
        [string](Get-PropertyValue $license 'name') -cne $expectedLicenseName -or
        [string](Get-PropertyValue $license 'url') -cne $expectedLicenseUrl) {
        throw 'Anonymous Figshare license readback is not exact CC BY 4.0.'
    }
    if (-not (Test-SameWork $Article $script:zenodoUrl)) {
        throw 'Anonymous Figshare record does not retain the exact work identity.'
    }
    $publicUrl = [string](Get-PropertyValue $Article 'url_public_html')
    $publicUri = $null
    if ([string]::IsNullOrWhiteSpace($publicUrl) -or
        -not [uri]::TryCreate($publicUrl, [UriKind]::Absolute, [ref]$publicUri) -or
        $publicUri.Scheme -cne 'https' -or
        ($publicUri.Host -cne 'figshare.com' -and -not $publicUri.Host.EndsWith('.figshare.com', [StringComparison]::OrdinalIgnoreCase))) {
        throw 'Anonymous Figshare public URL is missing or is not an HTTPS URL under figshare.com.'
    }
    $description = [string](Get-PropertyValue $Article 'description')
    if (-not $description.Contains('belum lengkap', [StringComparison]::OrdinalIgnoreCase) -or
        -not $description.Contains('tidak disponsori', [StringComparison]::OrdinalIgnoreCase) -or
        -not $description.Contains($script:zenodoUrl, [StringComparison]::Ordinal)) {
        throw 'Anonymous Figshare scope, non-endorsement, or Zenodo-link readback failed.'
    }
}

function Assert-ExactArticleMetadata([object]$Article, [string]$ExpectedDescription, [array]$ExpectedTags, [string]$Context, [bool]$RequirePublic = $false) {
    if ($RequirePublic) {
        Assert-PublicArticleIdentity $Article
    } else {
        if ([string](Get-PropertyValue $Article 'title') -cne $expectedTitle -or
            -not (Test-SameWork $Article $script:zenodoUrl)) {
            throw "$Context does not retain the exact private work identity."
        }
        $license = Get-PropertyValue $Article 'license'
        if ([int](Get-PropertyValue $license 'value') -ne $expectedLicenseId -or
            [string](Get-PropertyValue $license 'name') -cne $expectedLicenseName -or
            [string](Get-PropertyValue $license 'url') -cne $expectedLicenseUrl) {
            throw "$Context license readback is not exact CC BY 4.0."
        }
    }
    $actualTags = @((Get-PropertyValue $Article 'tags') | ForEach-Object { [string]$_ } | Sort-Object)
    $expectedTagsSorted = @($ExpectedTags | ForEach-Object { [string]$_ } | Sort-Object)
    $actualReferences = @((Get-PropertyValue $Article 'references') | ForEach-Object { [string]$_ })
    $expectedReferences = @($sourceUrl, $script:zenodoUrl)
    $actualAuthors = @(Get-ArticleAuthorNames $Article)
    $actualCategoryIds = @((Get-PropertyValue $Article 'categories') | ForEach-Object { [int](Get-PropertyValue $_ 'id') })
    if ([string](Get-PropertyValue $Article 'description') -cne $ExpectedDescription -or
        (($actualTags -join "`n") -cne ($expectedTagsSorted -join "`n")) -or
        (($actualReferences -join "`n") -cne ($expectedReferences -join "`n")) -or
        $actualAuthors.Count -ne 1 -or $actualAuthors[0] -cne 'David Michael Roberts' -or
        $actualCategoryIds.Count -ne 1 -or $actualCategoryIds[0] -ne 26095 -or
        [string](Get-PropertyValue $Article 'defined_type_name') -cne 'book') {
        throw "$Context metadata drifted from the exact submitted title/description/tags/references/author/category/type body."
    }
}

function Assert-ExactRemoteFiles([array]$RemoteFiles, [array]$ExpectedFiles, [string]$Label, [bool]$RequireOrder = $false) {
    $remoteOriginal = @($RemoteFiles)
    if ($RequireOrder -and
        (($remoteOriginal | ForEach-Object { Get-RemoteFileName $_ }) -join "`n") -cne (($ExpectedFiles | ForEach-Object filename) -join "`n")) {
        throw "$Label does not preserve the required reader-first file order."
    }
    $remote = @($RemoteFiles | Sort-Object { Get-RemoteFileName $_ })
    $expectedSorted = @($ExpectedFiles | Sort-Object filename)
    $remoteNames = (($remote | ForEach-Object { Get-RemoteFileName $_ }) -join "`n")
    $expectedNames = (($expectedSorted | ForEach-Object filename) -join "`n")
    if ($remoteNames -cne $expectedNames) {
        throw "$Label file inventory is not the exact reader-first Figshare allowlist."
    }
    for ($index = 0; $index -lt $expectedSorted.Count; $index++) {
        $expected = $expectedSorted[$index]
        $file = $remote[$index]
        if ((Get-RemoteFileBytes $file) -ne [int64]$expected.bytes -or
            (Get-RemoteFileMd5 $file) -cne [string]$expected.md5) {
            throw "$Label byte/MD5 mismatch for $($expected.filename)."
        }
    }
}

function Send-FileToFigshare([int64]$ArticleId, [object]$ExpectedFile) {
    $localPath = Join-Path $artifactsDir $ExpectedFile.filename
    $body = [ordered]@{
        md5 = [string]$ExpectedFile.md5
        name = [string]$ExpectedFile.filename
        size = [int64]$ExpectedFile.bytes
    } | ConvertTo-Json -Compress
    $created = Invoke-FigshareRequest -Method POST -Uri "$apiRoot/account/articles/$ArticleId/files" -Label "initiate upload $($ExpectedFile.filename)" -JsonBody $body -AllowedStatus @(201)
    $fileId = Get-ResponseEntityId $created
    $details = (Invoke-FigshareRequest -Method GET -Uri "$apiRoot/account/articles/$ArticleId/files/$fileId" -Label "retrieve upload descriptor $($ExpectedFile.filename)").Json
    $uploadUrl = [string](Get-PropertyValue $details 'upload_url')
    if ([string]::IsNullOrWhiteSpace($uploadUrl)) { throw "Upload descriptor lacks upload_url for $($ExpectedFile.filename)." }
    $upload = (Invoke-UploadServiceRequest -Method GET -Uri $uploadUrl -Label "retrieve upload parts $($ExpectedFile.filename)").Json
    $parts = @((Get-PropertyValue $upload 'parts') | Sort-Object { [int](Get-PropertyValue $_ 'partNo') })
    if ($parts.Count -eq 0) { throw "Upload service returned no parts for $($ExpectedFile.filename)." }

    $stream = [IO.File]::Open($localPath, [IO.FileMode]::Open, [IO.FileAccess]::Read, [IO.FileShare]::Read)
    try {
        foreach ($part in $parts) {
            $partNo = [int](Get-PropertyValue $part 'partNo')
            $start = [int64](Get-PropertyValue $part 'startOffset')
            $end = [int64](Get-PropertyValue $part 'endOffset')
            $length = $end - $start + 1
            if ($partNo -lt 1 -or $start -lt 0 -or $end -lt $start -or $length -gt 67108864) {
                throw "Unsafe upload part descriptor for $($ExpectedFile.filename)."
            }
            $buffer = [byte[]]::new([int]$length)
            $null = $stream.Seek($start, [IO.SeekOrigin]::Begin)
            $offset = 0
            while ($offset -lt $buffer.Length) {
                $read = $stream.Read($buffer, $offset, $buffer.Length - $offset)
                if ($read -le 0) { throw "Unexpected EOF while reading $($ExpectedFile.filename)." }
                $offset += $read
            }
            Invoke-UploadServiceRequest -Method PUT -Uri "$($uploadUrl.TrimEnd('/'))/$partNo" -Label "upload part $partNo of $($ExpectedFile.filename)" -Bytes $buffer | Out-Null
        }
    } finally {
        $stream.Dispose()
    }

    Invoke-FigshareRequest -Method POST -Uri "$apiRoot/account/articles/$ArticleId/files/$fileId" -Label "finalize upload $($ExpectedFile.filename)" -AllowedStatus @(200,201,202) | Out-Null
    $deadline = [DateTimeOffset]::UtcNow.AddSeconds(40)
    do {
        $file = (Invoke-FigshareRequest -Method GET -Uri "$apiRoot/account/articles/$ArticleId/files/$fileId" -Label "poll finalized upload $($ExpectedFile.filename)").Json
        $status = [string](Get-PropertyValue $file 'status')
        if ((Get-RemoteFileBytes $file) -eq [int64]$ExpectedFile.bytes -and
            (Get-RemoteFileMd5 $file) -ceq [string]$ExpectedFile.md5 -and
            $status -in @('created','available','completed')) {
            return
        }
    } while ([DateTimeOffset]::UtcNow -lt $deadline)
    throw "Finalized file did not reach a verified state: $($ExpectedFile.filename)."
}

function Get-TransactionStateRank([string]$State) {
    $rank = [Array]::IndexOf([string[]]$transactionStates, $State)
    if ($rank -lt 0) { throw 'Figshare transaction contains a state outside the exact allowlist.' }
    return $rank
}

function Assert-TransactionBinding(
    [object]$Transaction,
    [array]$ExpectedFiles,
    [object]$QaExclusion,
    [string]$MetadataHash,
    [string]$ManifestHash,
    [string]$ZenodoReceiptHash,
    [string]$ZenodoDoi,
    [int64]$PayloadBytes,
    [string]$ArticleBodyHash
) {
    $state = [string](Get-PropertyValue $Transaction 'state')
    $mode = [string](Get-PropertyValue $Transaction 'mode')
    if ([string](Get-PropertyValue $Transaction 'schema_version') -cne $transactionSchemaVersion -or
        $mode -cne $transactionMode -or
        $transactionStates -cnotcontains $state) {
        throw 'Figshare transaction schema, mode, or state is outside the exact allowlist.'
    }
    if ([string](Get-PropertyValue $Transaction 'release_id') -cne $releaseId -or
        [string](Get-PropertyValue $Transaction 'title') -cne $expectedTitle -or
        [string](Get-PropertyValue $Transaction 'version') -cne $expectedVersion -or
        [int](Get-PropertyValue $Transaction 'project_id') -ne $projectId -or
        [int](Get-PropertyValue $Transaction 'collection_id') -ne $collectionId -or
        [string](Get-PropertyValue $Transaction 'zenodo_doi') -cne $ZenodoDoi -or
        [string](Get-PropertyValue $Transaction 'metadata_sha256') -cne $MetadataHash -or
        [string](Get-PropertyValue $Transaction 'zenodo_receipt_sha256') -cne $ZenodoReceiptHash -or
        [string](Get-PropertyValue $Transaction 'release_manifest_sha256') -cne $ManifestHash -or
        [string](Get-PropertyValue $Transaction 'article_body_sha256') -cne $ArticleBodyHash -or
        [int64](Get-PropertyValue $Transaction 'figshare_payload_bytes') -ne $PayloadBytes) {
        throw 'Existing Figshare transaction does not match the exact release and publication route.'
    }

    $actualFiles = @((Get-PropertyValue $Transaction 'payload_files'))
    if ($actualFiles.Count -ne $ExpectedFiles.Count) {
        throw 'Figshare transaction payload binding has the wrong file count.'
    }
    for ($index = 0; $index -lt $ExpectedFiles.Count; $index++) {
        $actual = $actualFiles[$index]
        $expected = $ExpectedFiles[$index]
        if ([string](Get-PropertyValue $actual 'filename') -cne [string]$expected.filename -or
            [int64](Get-PropertyValue $actual 'bytes') -ne [int64]$expected.bytes -or
            [string](Get-PropertyValue $actual 'sha256') -cne [string]$expected.sha256 -or
            [string](Get-PropertyValue $actual 'md5') -cne [string]$expected.md5) {
            throw "Figshare transaction payload binding mismatch at ordered position $index."
        }
    }
    $actualExclusion = Get-PropertyValue $Transaction 'qa_exclusion'
    if ([string](Get-PropertyValue $actualExclusion 'filename') -cne [string]$QaExclusion.filename -or
        [int64](Get-PropertyValue $actualExclusion 'bytes') -ne [int64]$QaExclusion.bytes -or
        [string](Get-PropertyValue $actualExclusion 'sha256') -cne [string]$QaExclusion.sha256 -or
        [string](Get-PropertyValue $actualExclusion 'reason') -cne [string]$QaExclusion.reason) {
        throw 'Figshare transaction does not retain the exact deliberate QA/provenance exclusion.'
    }
    $createRequest = Get-PropertyValue $Transaction 'create_request'
    if ([string](Get-PropertyValue $createRequest 'method') -cne 'POST' -or
        [string](Get-PropertyValue $createRequest 'endpoint') -cne "$apiRoot/account/projects/$projectId/articles" -or
        [string](Get-PropertyValue $createRequest 'article_body_sha256') -cne $ArticleBodyHash -or
        [string](Get-PropertyValue $createRequest 'request_id') -notmatch '^[0-9a-f]{32}$') {
        throw 'Figshare transaction lacks an exact bound create-request intent.'
    }
    $articleIdValue = [int64](Get-PropertyValue $Transaction 'article_id')
    if (($state -ceq 'create_request_intent' -and $articleIdValue -ne 0) -or
        ($state -cne 'create_request_intent' -and $articleIdValue -le 0)) {
        throw 'Figshare transaction state and bound article ID are inconsistent.'
    }
}

function New-CreateIntentTransaction(
    [array]$ExpectedFiles,
    [object]$QaExclusion,
    [string]$MetadataHash,
    [string]$ManifestHash,
    [string]$ZenodoReceiptHash,
    [string]$ZenodoDoi,
    [int64]$PayloadBytes,
    [string]$ArticleBodyHash
) {
    $now = [DateTimeOffset]::UtcNow.ToString('o')
    return [ordered]@{
        schema_version = $transactionSchemaVersion
        mode = $transactionMode
        state = 'create_request_intent'
        release_id = $releaseId
        title = $expectedTitle
        version = $expectedVersion
        project_id = $projectId
        collection_id = $collectionId
        article_id = [int64]0
        zenodo_doi = $ZenodoDoi
        metadata_sha256 = $MetadataHash
        zenodo_receipt_sha256 = $ZenodoReceiptHash
        release_manifest_sha256 = $ManifestHash
        article_body_sha256 = $ArticleBodyHash
        figshare_payload_bytes = $PayloadBytes
        payload_files = @($ExpectedFiles | ForEach-Object {
            [ordered]@{
                filename = [string]$_.filename
                bytes = [int64]$_.bytes
                sha256 = [string]$_.sha256
                md5 = [string]$_.md5
            }
        })
        qa_exclusion = [ordered]@{
            filename = [string]$QaExclusion.filename
            bytes = [int64]$QaExclusion.bytes
            sha256 = [string]$QaExclusion.sha256
            reason = [string]$QaExclusion.reason
        }
        create_request = [ordered]@{
            method = 'POST'
            endpoint = "$apiRoot/account/projects/$projectId/articles"
            request_id = [guid]::NewGuid().ToString('N')
            article_body_sha256 = $ArticleBodyHash
        }
        created_at_utc = $now
        updated_at_utc = $now
    }
}

function Update-TransactionState([object]$Transaction, [string]$State) {
    $current = [string](Get-PropertyValue $Transaction 'state')
    $null = Get-TransactionStateRank $current
    $null = Get-TransactionStateRank $State
    $allowed = @{
        create_request_intent = @('created_in_project')
        created_in_project = @('metadata_verified')
        metadata_verified = @('files_verified')
        files_verified = @('article_publish_intent')
        article_publish_intent = @('article_published')
        article_published = @('collection_append_intent')
        collection_append_intent = @('collection_membership_appended')
        collection_membership_appended = @('collection_publish_intent','collection_published')
        collection_publish_intent = @('collection_published')
        collection_published = @('published_collected_and_anonymously_verified')
        published_collected_and_anonymously_verified = @('published_collected_and_anonymously_verified')
    }
    if ($State -cne $current -and $allowed[$current] -cnotcontains $State) {
        throw "Refusing invalid Figshare transaction state transition from $current to $State."
    }
    Set-PropertyValue $Transaction 'state' $State
    Set-PropertyValue $Transaction 'updated_at_utc' ([DateTimeOffset]::UtcNow.ToString('o'))
    Write-JsonAtomic $transactionPath $Transaction
}

$prelockInputSnapshot = Get-ImmutableInputSnapshot
$prelockInputSnapshotText = Convert-SnapshotToCanonicalText $prelockInputSnapshot
$lockStream = $null
$token = $null
try {
    try {
        $lockStream = [IO.FileStream]::new(
            $sharedLockPath,
            [IO.FileMode]::CreateNew,
            [IO.FileAccess]::ReadWrite,
            [IO.FileShare]::None,
            4096,
            [IO.FileOptions]::DeleteOnClose
        )
    } catch {
        throw "Another Zenodo/Figshare release operation is active or a stale lock needs inspection: $sharedLockPath"
    }
    if (-not (Test-Path -LiteralPath $figshareReleaseRoot -PathType Container)) {
        New-Item -ItemType Directory -Path $figshareReleaseRoot | Out-Null
    }

    # Repeat the complete immutable input snapshot under the owned cross-service lock.
    $lockedInputSnapshot = Get-ImmutableInputSnapshot
    $lockedInputSnapshotText = Convert-SnapshotToCanonicalText $lockedInputSnapshot
    if ($lockedInputSnapshotText -cne $prelockInputSnapshotText) {
        throw 'Release inputs drifted between the pre-lock snapshot and acquisition of the shared release lock.'
    }
    & (Get-Command pwsh -ErrorAction Stop).Source -NoProfile -File $verifyScript -ReleaseDirectory $artifactsDir | Out-Host
    if ($LASTEXITCODE -ne 0) { throw 'Locked local eight-file release verification failed.' }

    $zenodoExpectedFiles = @($lockedInputSnapshot.artifacts)
    $expectedFiles = @($releaseNames | ForEach-Object {
        $name = $_
        $match = @($zenodoExpectedFiles | Where-Object { [string]$_.filename -ceq $name })
        if ($match.Count -ne 1) { throw "Unable to bind exact Figshare payload file: $name" }
        $match[0]
    })
    $payloadBytes = [int64](($expectedFiles | Measure-Object -Property bytes -Sum).Sum)
    if ($payloadBytes -le 0 -or $payloadBytes -gt $maximumFigsharePayloadBytes) {
        throw 'Reader-first Figshare payload is empty or exceeds the strict 500 MB ceiling.'
    }
    $qaName = 'TOPOLOGI_ALJABAR_ID_UNIT_001_013_QA_PROVENANCE.zip'
    if ($releaseNames -contains $qaName) { throw 'Figshare payload must exclude the QA/provenance archive.' }
    $qaMatch = @($zenodoExpectedFiles | Where-Object { [string]$_.filename -ceq $qaName })
    if ($qaMatch.Count -ne 1) { throw 'Unable to bind the deliberately excluded QA/provenance archive.' }
    $qaExclusion = [ordered]@{
        filename = $qaName
        bytes = [int64]$qaMatch[0].bytes
        sha256 = [string]$qaMatch[0].sha256
        reason = 'Large QA/provenance archive is intentionally retained only in the verified Zenodo release and is not duplicated in the reader-first Figshare payload.'
    }

    $metadataText = [IO.File]::ReadAllText($metadataPath)
    $metadataDocument = $metadataText | ConvertFrom-Json
    if ([string]$metadataDocument.metadata.title -cne $expectedTitle -or
        [string]$metadataDocument.metadata.version -cne $expectedVersion -or
        [string]$metadataDocument.metadata.license -cne 'cc-by-4.0') {
        throw 'Local Zenodo metadata identity/version/license mismatch.'
    }
    $zenodoReceiptText = [IO.File]::ReadAllText($zenodoReceiptPath)
    $zenodoReceipt = $zenodoReceiptText | ConvertFrom-Json
    Assert-ZenodoReceipt $zenodoReceipt $zenodoExpectedFiles
    $metadataHash = [string]$lockedInputSnapshot.metadata.sha256
    $zenodoReceiptHash = [string]$lockedInputSnapshot.zenodo_receipt.sha256
    $manifestHash = [string](@($zenodoExpectedFiles | Where-Object { [string]$_.filename -ceq 'release-manifest.json' })[0].sha256)
    $script:zenodoUrl = 'https://doi.org/' + [string]$zenodoReceipt.doi

    $description = [string]$metadataDocument.metadata.description +
        ('<p><strong>Salinan Figshare dari batas preservasi Zenodo yang sama:</strong> <a href="{0}">{0}</a>. Muatan Figshare berurutan dan berorientasi pembaca: PDF, pembaca HTML, arsip ringkas sumber/backend, dokumen hak, manifest, checksum, lalu README. Ketujuh berkas itu identik byte dengan rilis Zenodo. Arsip QA/provenance yang lebih besar tetap tersedia hanya di Zenodo dan sengaja tidak diduplikasi di sini.</p>' -f $script:zenodoUrl)
    $tags = @(
        @($metadataDocument.metadata.keywords | ForEach-Object { [string]$_ }) +
        @($workTag, $releaseId, 'O012', 'D60', 'id-ID', 'Unit 1–13', 'partial checkpoint', "version-$expectedVersion")
    ) | Sort-Object -Unique
    $articleBodyObject = [ordered]@{
        title = $expectedTitle
        description = $description
        tags = $tags
        references = @($sourceUrl, $script:zenodoUrl)
        categories = @(26095)
        authors = @([ordered]@{ name = 'David Michael Roberts' })
        defined_type = 'book'
        license = $expectedLicenseId
    }
    $articleBody = $articleBodyObject | ConvertTo-Json -Depth 10 -Compress
    $articleBodyHash = Get-TextSha256 $articleBody
    if ($articleBody -match '(?i)\bTTP\b|Translation and Transcription Project|C:\\Users\\|C:/Users/' -or
        -not $description.Contains('belum lengkap', [StringComparison]::OrdinalIgnoreCase) -or
        -not $description.Contains('tidak disponsori', [StringComparison]::OrdinalIgnoreCase)) {
        throw 'Figshare metadata contains forbidden text/path material or lacks exact scope/non-endorsement language.'
    }

    $transaction = $null
    $transactionText = $null
    if (Test-Path -LiteralPath $transactionPath -PathType Leaf) {
        $transactionText = [IO.File]::ReadAllText($transactionPath)
        $transaction = $transactionText | ConvertFrom-Json
        Assert-TransactionBinding $transaction $expectedFiles $qaExclusion $metadataHash $manifestHash $zenodoReceiptHash ([string]$zenodoReceipt.doi) $payloadBytes $articleBodyHash
    }

    if (-not (Test-Path -LiteralPath $secretPath -PathType Leaf)) {
        throw "Missing required release input: $secretPath"
    }
    $token = Get-SecretToken $secretPath
    Set-ActiveTokenScanner $token
    Assert-AllLocalTextAndPayloadTokenFree $metadataText $zenodoReceiptText $transactionText $articleBody
    $script:headers = @{ Authorization = "token $token" }

    if ($null -ne $transaction -and [string](Get-PropertyValue $transaction 'state') -ceq 'create_request_intent') {
        throw 'A bound create request has an ambiguous/lost response; refusing to repeat it or adopt an unbound article.'
    }

    $publicLicenses = @((Invoke-FigshareRequest -Method GET -Uri "$apiRoot/licenses" -Label 'verify public license catalog' -Authenticated $false).Json)
    $accountLicenses = @((Invoke-FigshareRequest -Method GET -Uri "$apiRoot/account/licenses" -Label 'verify account license catalog').Json)
    foreach ($catalog in @($publicLicenses, $accountLicenses)) {
        $matches = @($catalog | Where-Object {
            [int](Get-PropertyValue $_ 'value') -eq $expectedLicenseId -and
            [string](Get-PropertyValue $_ 'name') -ceq $expectedLicenseName -and
            [string](Get-PropertyValue $_ 'url') -ceq $expectedLicenseUrl
        })
        if ($matches.Count -ne 1) { throw 'Figshare does not expose one exact CC BY 4.0 license entry with ID 1.' }
    }

    $project = (Invoke-FigshareRequest -Method GET -Uri "$apiRoot/account/projects/$projectId" -Label 'verify target project').Json
    if ([int](Get-PropertyValue $project 'id') -ne $projectId -or [string](Get-PropertyValue $project 'title') -cne $expectedProjectTitle) {
        throw 'Authenticated Figshare project identity mismatch.'
    }
    $collection = (Invoke-FigshareRequest -Method GET -Uri "$apiRoot/account/collections/$collectionId" -Label 'verify target collection').Json
    if ([int](Get-PropertyValue $collection 'id') -ne $collectionId -or [string](Get-PropertyValue $collection 'title') -cne $expectedCollectionTitle) {
        throw 'Authenticated Figshare collection identity mismatch.'
    }

    $projectArticles = @(Get-AllProjectArticles $true)
    $ownCandidatesById = @{}
    foreach ($term in @($expectedTitle, 'Topologi Aljabar', $releaseId)) {
        foreach ($candidate in @(Search-OwnArticles $term)) {
            $id = Get-ObjectId $candidate
            if ($id -gt 0) { $ownCandidatesById[[string]$id] = $candidate }
        }
    }
    foreach ($candidate in $projectArticles) {
        $id = Get-ObjectId $candidate
        if ($id -gt 0 -and (Test-SuspiciousCandidate $candidate)) { $ownCandidatesById[[string]$id] = $candidate }
    }

    $fullCandidates = @()
    foreach ($id in @($ownCandidatesById.Keys | Sort-Object)) {
        $full = (Invoke-FigshareRequest -Method GET -Uri "$apiRoot/account/articles/$id" -Label 'resolve exact own/project search candidate').Json
        if (Test-SuspiciousCandidate $full) { $fullCandidates += $full }
    }
    $sameWork = @($fullCandidates | Where-Object { Test-SameWork $_ $script:zenodoUrl })
    $ambiguous = @($fullCandidates | Where-Object { (Test-SuspiciousCandidate $_) -and -not (Test-SameWork $_ $script:zenodoUrl) })
    if ($ambiguous.Count -gt 0) { throw 'A suspicious Topologi Aljabar/O012 item failed exact identity checks; refusing mutation or duplication.' }
    if ($sameWork.Count -gt 1) { throw 'Multiple own Figshare items match this exact work; refusing ambiguity.' }

    $projectIds = @($projectArticles | ForEach-Object { Get-ObjectId $_ })
    $articleId = [int64]0
    if ($null -ne $transaction) {
        $articleId = [int64]$transaction.article_id
        $known = (Invoke-FigshareRequest -Method GET -Uri "$apiRoot/account/articles/$articleId" -Label 'resume known Figshare article').Json
        if (-not (Test-SameWork $known $script:zenodoUrl) -or $projectIds -notcontains $articleId) {
            throw 'Known Figshare transaction no longer points to this exact work inside project 280296.'
        }
        if ($sameWork.Count -eq 1 -and (Get-ObjectId $sameWork[0]) -ne $articleId) {
            throw 'Exact searches disagree with the persisted Figshare article ID.'
        }
    } elseif ($sameWork.Count -eq 1) {
        throw 'An exact same-work item exists without this lane transaction; refusing to mutate it or create a duplicate.'
    } else {
        # Count every file of every authenticated project article, including
        # unpublished/private items, before the first mutation.
        $projectCapacityPreflight = Assert-AuthenticatedProjectCapacity 0 $payloadBytes
        $transaction = New-CreateIntentTransaction $expectedFiles $qaExclusion $metadataHash $manifestHash $zenodoReceiptHash ([string]$zenodoReceipt.doi) $payloadBytes $articleBodyHash
        Write-JsonAtomic $transactionPath $transaction
        $transactionText = [IO.File]::ReadAllText($transactionPath)
        Assert-AllLocalTextAndPayloadTokenFree $metadataText $zenodoReceiptText $transactionText $articleBody
        $created = Invoke-FigshareRequest -Method POST -Uri "$apiRoot/account/projects/$projectId/articles" -Label 'create O012 article directly in project' -JsonBody $articleBody -AllowedStatus @(201)
        $articleId = Get-ResponseEntityId $created
        Set-PropertyValue $transaction 'article_id' $articleId
        Update-TransactionState $transaction 'created_in_project'
    }

    $refreshedPrivateProject = @(Get-AllProjectArticles $true)
    if (@($refreshedPrivateProject | Where-Object { (Get-ObjectId $_) -eq $articleId }).Count -ne 1) {
        throw 'Known article is not associated exactly once with authenticated project 280296.'
    }

    $publicResponse = Get-PublicArticle $articleId
    $alreadyPublic = $publicResponse.StatusCode -eq 200
    if ($alreadyPublic) {
        $publicArticle = $publicResponse.Json
        Assert-ExactArticleMetadata $publicArticle $description $tags 'Existing public Figshare article' $true
        Assert-ExactRemoteFiles @($publicArticle.files) $expectedFiles 'Existing public Figshare article' $true
    } else {
        $currentState = [string](Get-PropertyValue $transaction 'state')
        if ($currentState -eq 'article_publish_intent') {
            $deadline = [DateTimeOffset]::UtcNow.AddSeconds(40)
            do {
                $publicResponse = Get-PublicArticle $articleId
                if ($publicResponse.StatusCode -eq 200) { $alreadyPublic = $true; break }
            } while ([DateTimeOffset]::UtcNow -lt $deadline)
            if (-not $alreadyPublic) {
                throw 'A prior article-publish request is persisted but not publicly visible; refusing a second publish request without inspection.'
            }
        }
    }
    if ($alreadyPublic) {
        $publicArticle = $publicResponse.Json
        Assert-ExactArticleMetadata $publicArticle $description $tags 'Recovered public Figshare article' $true
        Assert-ExactRemoteFiles @($publicArticle.files) $expectedFiles 'Recovered public Figshare article' $true
    }

    $projectCapacityPreflight = Assert-AuthenticatedProjectCapacity $articleId $payloadBytes
    if (-not $alreadyPublic) {
        Invoke-FigshareRequest -Method PUT -Uri "$apiRoot/account/articles/$articleId" -Label 'set exact O012 metadata' -JsonBody $articleBody -AllowedStatus @(205) | Out-Null
        $privateArticle = (Invoke-FigshareRequest -Method GET -Uri "$apiRoot/account/articles/$articleId" -Label 'verify private O012 metadata').Json
        Assert-ExactArticleMetadata $privateArticle $description $tags 'Private Figshare article'
        $stateAfterMetadata = [string](Get-PropertyValue $transaction 'state')
        if ($stateAfterMetadata -ceq 'created_in_project') {
            Update-TransactionState $transaction 'metadata_verified'
        } elseif ((Get-TransactionStateRank $stateAfterMetadata) -lt (Get-TransactionStateRank 'metadata_verified')) {
            throw 'Figshare transaction state is inconsistent with verified private metadata.'
        }

        $privateFiles = @((Invoke-FigshareRequest -Method GET -Uri "$apiRoot/account/articles/$articleId/files?page=1&page_size=100" -Label 'list private article files').Json)
        foreach ($remote in $privateFiles) {
            $name = Get-RemoteFileName $remote
            if ($releaseNames -cnotcontains $name) { throw "Unexpected private Figshare file; refusing deletion or publication: $name" }
            $expected = @($expectedFiles | Where-Object { $_.filename -ceq $name })
            if ($expected.Count -ne 1) { throw "Unable to bind private Figshare file to local allowlist: $name" }
            $status = [string](Get-PropertyValue $remote 'status')
            $matches = (Get-RemoteFileBytes $remote) -eq [int64]$expected[0].bytes -and
                (Get-RemoteFileMd5 $remote) -ceq [string]$expected[0].md5 -and
                $status -in @('created','available','completed')
            if (-not $matches) {
                $fileId = Get-ObjectId $remote
                if ($fileId -le 0) { throw "Mismatched draft file lacks an ID: $name" }
                Invoke-FigshareRequest -Method DELETE -Uri "$apiRoot/account/articles/$articleId/files/$fileId" -Label "delete only this lane's incomplete upload $name" -AllowedStatus @(204) | Out-Null
            }
        }

        $privateFiles = @((Invoke-FigshareRequest -Method GET -Uri "$apiRoot/account/articles/$articleId/files?page=1&page_size=100" -Label 'refresh private article files').Json)
        $presentNames = @($privateFiles | ForEach-Object { Get-RemoteFileName $_ })
        foreach ($expected in $expectedFiles) {
            if ($presentNames -cnotcontains [string]$expected.filename) {
                Send-FileToFigshare $articleId $expected
            }
        }

        $privateFiles = @((Invoke-FigshareRequest -Method GET -Uri "$apiRoot/account/articles/$articleId/files?page=1&page_size=100" -Label 'verify final private file inventory').Json)
        Assert-ExactRemoteFiles $privateFiles $expectedFiles 'Private Figshare draft' $true
        $stateAfterFiles = [string](Get-PropertyValue $transaction 'state')
        if ($stateAfterFiles -ceq 'metadata_verified') {
            Update-TransactionState $transaction 'files_verified'
        } elseif ((Get-TransactionStateRank $stateAfterFiles) -lt (Get-TransactionStateRank 'files_verified')) {
            throw 'Figshare transaction state is inconsistent with the verified private file inventory.'
        }

        # Repeat all local/Zenodo gates immediately before the irreversible publish request.
        $immediateSnapshot = Get-ImmutableInputSnapshot
        if ((Convert-SnapshotToCanonicalText $immediateSnapshot) -cne $lockedInputSnapshotText) {
            throw 'Complete release input snapshot drifted after lock acquisition; refusing publication.'
        }
        & (Get-Command pwsh -ErrorAction Stop).Source -NoProfile -File $verifyScript -ReleaseDirectory $artifactsDir | Out-Host
        if ($LASTEXITCODE -ne 0) { throw 'Immediate pre-publish local release verification failed.' }
        if ((Get-Sha256 $zenodoReceiptPath) -cne $zenodoReceiptHash) { throw 'Zenodo receipt changed during the Figshare transaction.' }
        Assert-ZenodoReceipt ([IO.File]::ReadAllText($zenodoReceiptPath) | ConvertFrom-Json) $zenodoExpectedFiles
        $lockedTransactionText = [IO.File]::ReadAllText($transactionPath)
        Assert-AllLocalTextAndPayloadTokenFree ([IO.File]::ReadAllText($metadataPath)) ([IO.File]::ReadAllText($zenodoReceiptPath)) $lockedTransactionText $articleBody
        $projectCapacityPreflight = Assert-AuthenticatedProjectCapacity $articleId $payloadBytes

        Update-TransactionState $transaction 'article_publish_intent'
        Invoke-FigshareRequest -Method POST -Uri "$apiRoot/account/articles/$articleId/publish" -Label 'publish exact O012 Figshare article' -AllowedStatus @(201) | Out-Null
        $deadline = [DateTimeOffset]::UtcNow.AddSeconds(60)
        $publicArticle = $null
        do {
            $publicResponse = Get-PublicArticle $articleId
            if ($publicResponse.StatusCode -eq 200) { $publicArticle = $publicResponse.Json; break }
        } while ([DateTimeOffset]::UtcNow -lt $deadline)
        if ($null -eq $publicArticle) { throw 'Published Figshare article did not become anonymously readable within 60 seconds; transaction is persisted for safe inspection.' }
        Assert-ExactArticleMetadata $publicArticle $description $tags 'Published Figshare article' $true
        Assert-ExactRemoteFiles @($publicArticle.files) $expectedFiles 'Published Figshare article' $true
        Update-TransactionState $transaction 'article_published'
    } else {
        $publicArticle = $publicResponse.Json
        $stateAtPublicRecovery = [string](Get-PropertyValue $transaction 'state')
        if ($stateAtPublicRecovery -ceq 'article_publish_intent') {
            Update-TransactionState $transaction 'article_published'
        } elseif ((Get-TransactionStateRank $stateAtPublicRecovery) -lt (Get-TransactionStateRank 'article_published')) {
            throw 'A public Figshare article appeared without the required publish-intent journal state.'
        }
    }

    $publicProjectArticles = @(Get-AllProjectArticles $false)
    if (@($publicProjectArticles | Where-Object { (Get-ObjectId $_) -eq $articleId }).Count -ne 1) {
        throw 'Published article is not exposed exactly once by public project 280296.'
    }

    $privateCollectionArticles = @(Get-AllCollectionArticles $true)
    $privateMembership = @($privateCollectionArticles | Where-Object { (Get-ObjectId $_) -eq $articleId })
    if ($privateMembership.Count -gt 1) { throw 'Article appears more than once in the private collection membership.' }
    if ($privateMembership.Count -eq 0) {
        if ([string](Get-PropertyValue $transaction 'state') -ceq 'collection_append_intent') {
            throw 'A prior collection-append request has an unresolved response; refusing to repeat it.'
        }
        $addBody = @{ articles = @($articleId) } | ConvertTo-Json -Compress
        Update-TransactionState $transaction 'collection_append_intent'
        Invoke-FigshareRequest -Method POST -Uri "$apiRoot/account/collections/$collectionId/articles" -Label 'append O012 article to Indonesian collection' -JsonBody $addBody -AllowedStatus @(201) | Out-Null
        Update-TransactionState $transaction 'collection_membership_appended'
    } else {
        $stateAtAppendRecovery = [string](Get-PropertyValue $transaction 'state')
        if ($stateAtAppendRecovery -ceq 'collection_append_intent') {
            Update-TransactionState $transaction 'collection_membership_appended'
        } elseif ((Get-TransactionStateRank $stateAtAppendRecovery) -lt (Get-TransactionStateRank 'collection_membership_appended')) {
            throw 'Collection membership appeared without the required append-intent journal state.'
        }
    }
    $privateCollectionArticles = @(Get-AllCollectionArticles $true)
    if (@($privateCollectionArticles | Where-Object { (Get-ObjectId $_) -eq $articleId }).Count -ne 1) {
        throw 'Authenticated collection readback did not retain exactly one appended O012 article.'
    }

    $publicCollectionBefore = (Invoke-FigshareRequest -Method GET -Uri "$apiRoot/collections/$collectionId" -Label 'read current public collection' -Authenticated $false).Json
    $publicCollectionArticles = @(Get-AllCollectionArticles $false)
    $publicMembership = @($publicCollectionArticles | Where-Object { (Get-ObjectId $_) -eq $articleId })
    if ($publicMembership.Count -gt 1) { throw 'Article appears more than once in the public collection membership.' }
    if ($publicMembership.Count -eq 0) {
        $privateCollectionIds = @($privateCollectionArticles | ForEach-Object { Get-ObjectId $_ } | Sort-Object -Unique)
        $publicCollectionIds = @($publicCollectionArticles | ForEach-Object { Get-ObjectId $_ } | Sort-Object -Unique)
        $expectedPrivateCollectionIds = @($publicCollectionIds + $articleId | Sort-Object -Unique)
        if (($privateCollectionIds -join "`n") -cne ($expectedPrivateCollectionIds -join "`n")) {
            throw 'Authenticated collection draft contains unrelated pending membership changes; refusing to publish another task''s changes.'
        }
        if ([string](Get-PropertyValue $transaction 'state') -eq 'collection_publish_intent') {
            $deadline = [DateTimeOffset]::UtcNow.AddSeconds(40)
            do {
                $publicCollectionArticles = @(Get-AllCollectionArticles $false)
                $publicMembership = @($publicCollectionArticles | Where-Object { (Get-ObjectId $_) -eq $articleId })
                if ($publicMembership.Count -eq 1) { break }
            } while ([DateTimeOffset]::UtcNow -lt $deadline)
            if ($publicMembership.Count -ne 1) {
                throw 'A prior collection-publish request is persisted but not publicly visible; refusing a second collection version without inspection.'
            }
            Update-TransactionState $transaction 'collection_published'
        } else {
            Set-PropertyValue $transaction 'public_collection_version_before' ([int](Get-PropertyValue $publicCollectionBefore 'version'))
            Update-TransactionState $transaction 'collection_publish_intent'
            Invoke-FigshareRequest -Method POST -Uri "$apiRoot/account/collections/$collectionId/publish" -Label 'publish appended Indonesian collection version' -AllowedStatus @(201) | Out-Null
            $deadline = [DateTimeOffset]::UtcNow.AddSeconds(60)
            do {
                $publicCollectionArticles = @(Get-AllCollectionArticles $false)
                $publicMembership = @($publicCollectionArticles | Where-Object { (Get-ObjectId $_) -eq $articleId })
                if ($publicMembership.Count -eq 1) { break }
            } while ([DateTimeOffset]::UtcNow -lt $deadline)
            if ($publicMembership.Count -ne 1) { throw 'Updated Indonesian collection did not expose the article within 60 seconds.' }
            Update-TransactionState $transaction 'collection_published'
        }
    } else {
        $stateAtCollectionRecovery = [string](Get-PropertyValue $transaction 'state')
        if ($stateAtCollectionRecovery -ceq 'collection_publish_intent') {
            Update-TransactionState $transaction 'collection_published'
        } elseif ((Get-TransactionStateRank $stateAtCollectionRecovery) -lt (Get-TransactionStateRank 'collection_published')) {
            throw 'Public collection membership appeared without the required collection-publish intent state.'
        }
    }

    $publicCollection = (Invoke-FigshareRequest -Method GET -Uri "$apiRoot/collections/$collectionId" -Label 'verify updated public collection' -Authenticated $false).Json
    if ([int](Get-PropertyValue $publicCollection 'id') -ne $collectionId -or
        [string](Get-PropertyValue $publicCollection 'title') -cne $expectedCollectionTitle) {
        throw 'Public collection identity readback mismatch.'
    }
    $collectionVersionBefore = Get-PropertyValue $transaction 'public_collection_version_before'
    if ($null -ne $collectionVersionBefore -and
        [int](Get-PropertyValue $publicCollection 'version') -le [int]$collectionVersionBefore) {
        throw 'Collection membership changed without a strictly newer public collection version.'
    }

    $publicArticle = (Get-PublicArticle $articleId @(200)).Json
    Assert-ExactArticleMetadata $publicArticle $description $tags 'Final anonymous Figshare article' $true
    $publicFiles = @($publicArticle.files)
    Assert-ExactRemoteFiles $publicFiles $expectedFiles 'Final anonymous Figshare article' $true

    $readbackDir = Join-Path $figshareReleaseRoot ('.anonymous-readback-' + [guid]::NewGuid().ToString('N'))
    Assert-FigshareReleaseChild $readbackDir
    if (-not (Test-Path -LiteralPath $figshareReleaseRoot -PathType Container)) {
        New-Item -ItemType Directory -Path $figshareReleaseRoot | Out-Null
    }
    New-Item -ItemType Directory -Path $readbackDir | Out-Null
    try {
        $fileReceipts = @()
        foreach ($remote in @($publicFiles | Sort-Object { Get-RemoteFileName $_ })) {
            $name = Get-RemoteFileName $remote
            $expected = @($expectedFiles | Where-Object { $_.filename -ceq $name })[0]
            $downloadUrl = [string](Get-PropertyValue $remote 'download_url')
            $readbackPath = Join-Path $readbackDir $name
            Invoke-AnonymousDownload $downloadUrl $readbackPath $name
            if ((Get-Item -LiteralPath $readbackPath).Length -ne [int64]$expected.bytes -or
                (Get-Sha256 $readbackPath) -cne [string]$expected.sha256) {
                throw "Anonymous Figshare byte/SHA-256 readback mismatch for $name."
            }
            $fileReceipts += [ordered]@{
                filename = $name
                file_id = Get-ObjectId $remote
                bytes = [int64]$expected.bytes
                md5 = [string]$expected.md5
                sha256 = [string]$expected.sha256
                anonymous_url = $downloadUrl
                verified = $true
            }
        }
    } finally {
        if (Test-Path -LiteralPath $readbackDir) { Remove-Item -LiteralPath $readbackDir -Recurse -Force }
    }

    $publicProjectArticles = @(Get-AllProjectArticles $false)
    $publicCollectionArticles = @(Get-AllCollectionArticles $false)
    if (@($publicProjectArticles | Where-Object { (Get-ObjectId $_) -eq $articleId }).Count -ne 1 -or
        @($publicCollectionArticles | Where-Object { (Get-ObjectId $_) -eq $articleId }).Count -ne 1) {
        throw 'Final anonymous project/collection membership readback failed.'
    }
    $finalProjectInventory = Get-AuthenticatedProjectByteInventory
    if ([int64]$finalProjectInventory.Bytes -ge $maximumProjectBytes) {
        throw 'Final public project inventory reaches or exceeds the strict 20 GB ceiling.'
    }

    $articleDoi = [string](Get-PropertyValue $publicArticle 'doi')
    $articleUrl = [string](Get-PropertyValue $publicArticle 'url_public_html')
    $collectionDoi = [string](Get-PropertyValue $publicCollection 'doi')
    if ($articleDoi -notmatch '^10\.6084/m9\.figshare\.[0-9]+\.v[0-9]+$' -or
        $collectionDoi -notmatch '^10\.6084/m9\.figshare\.c\.8668413\.v[0-9]+$') {
        throw 'Final Figshare article or collection DOI is missing/malformed.'
    }

    $receipt = [ordered]@{
        schema_version = '1.0'
        release_id = $releaseId
        published_at_utc = [DateTimeOffset]::UtcNow.ToString('o')
        article_id = $articleId
        title = $expectedTitle
        version_label = $expectedVersion
        doi = $articleDoi
        public_record_url = $articleUrl
        anonymous_api_url = "$apiRoot/articles/$articleId"
        project_id = $projectId
        project_url = "https://figshare.com/projects/Open_and_Share-Alike_Educational_Materials_Translations/$projectId"
        collection_id = $collectionId
        collection_version = [int](Get-PropertyValue $publicCollection 'version')
        collection_doi = $collectionDoi
        collection_url = "https://doi.org/$collectionDoi"
        zenodo_doi = [string]$zenodoReceipt.doi
        zenodo_url = $script:zenodoUrl
        zenodo_receipt_sha256 = $zenodoReceiptHash
        release_manifest_sha256 = $manifestHash
        license = $expectedLicenseName
        incomplete_checkpoint = $true
        figshare_payload_bytes = $payloadBytes
        figshare_payload_order = $releaseNames
        deliberately_excluded = @('TOPOLOGI_ALJABAR_ID_UNIT_001_013_QA_PROVENANCE.zip')
        project_total_authenticated_bytes = [int64]$finalProjectInventory.Bytes
        project_byte_ceiling = $maximumProjectBytes
        public_file_count = $fileReceipts.Count
        files = $fileReceipts
        verification = [ordered]@{
            exact_authenticated_own_search = $true
            exact_authenticated_project_search = $true
            created_directly_in_project_or_resumed_known_transaction = $true
            exact_public_inventory = $true
            anonymous_project_membership = $true
            anonymous_collection_membership = $true
            anonymous_byte_readback = $true
            all_sha256_match_local = $true
            zenodo_release_binding_verified = $true
            credential_material_persisted = $false
        }
    }
    Write-JsonAtomic $receiptPath $receipt
    Set-PropertyValue $transaction 'figshare_doi' $articleDoi
    Set-PropertyValue $transaction 'collection_doi' $collectionDoi
    Set-PropertyValue $transaction 'receipt_sha256' (Get-Sha256 $receiptPath)
    Update-TransactionState $transaction 'published_collected_and_anonymously_verified'

    [pscustomobject]@{
        Status = 'PUBLISHED_COLLECTED_AND_VERIFIED'
        ArticleId = $articleId
        DOI = $articleDoi
        PublicURL = $articleUrl
        ProjectId = $projectId
        CollectionDOI = $collectionDoi
        FileCount = $fileReceipts.Count
        ReceiptPath = $receiptPath
        ReceiptSHA256 = Get-Sha256 $receiptPath
    }
} finally {
    $script:headers = $null
    $token = $null
    if ($null -ne $lockStream) {
        try { $lockStream.Dispose() } catch { Write-Warning 'Could not dispose the shared release lock handle cleanly.' }
    }
}
