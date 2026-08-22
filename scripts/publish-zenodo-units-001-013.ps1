#requires -Version 7.0
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$SecretPath
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$lane = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$releaseRoot = Join-Path $lane 'release\zenodo-units-001-013'
$artifactsDir = Join-Path $releaseRoot 'artifacts'
$metadataPath = Join-Path $releaseRoot 'metadata.json'
$transactionPath = Join-Path $releaseRoot 'transaction.json'
$lockPath = Join-Path $releaseRoot '.release-operation.lock'
$verifyScript = Join-Path $PSScriptRoot 'verify-zenodo-units-001-013.ps1'
$secretPath = [IO.Path]::GetFullPath($SecretPath)
$receiptPath = Join-Path $lane '00_control\ZENODO_PUBLICATION_RECEIPT_UNITS_001_013.json'
$apiRoot = 'https://zenodo.org/api'

$releaseId = 'o012-roberts-id-units-001-013-v0.13.0'
$expectedTitle = 'Topologi Aljabar: Edisi Bahasa Indonesia — Unit 1–13'
$expectedVersion = '0.13.0'
$sourceUrl = 'https://github.com/DavidMichaelRoberts/AlgebraicTopology2019/tree/b947ad2e9f9e301bfe24590a9db653bc54fa1a53'
$releaseNames = @(
    '00_TOPOLOGI_ALJABAR_ID_UNIT_001_013_READER.pdf',
    'TOPOLOGI_ALJABAR_ID_UNIT_001_013_READER.html',
    'TOPOLOGI_ALJABAR_ID_UNIT_001_013_EDITABLE_SOURCE_BACKEND.zip',
    'TOPOLOGI_ALJABAR_ID_UNIT_001_013_QA_PROVENANCE.zip',
    'README_RELEASE.md',
    'RELEASE_RIGHTS.md',
    'release-manifest.json',
    'SHA256SUMS'
)

function Get-Sha256([string]$Path) {
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}

function Get-Md5([string]$Path) {
    return (Get-FileHash -LiteralPath $Path -Algorithm MD5).Hash.ToLowerInvariant()
}

function Get-PropertyValue([object]$Object, [string]$Name) {
    if ($null -eq $Object) { return $null }
    if ($Object -is [Collections.IDictionary]) {
        if ($Object.Contains($Name)) { return $Object[$Name] }
        return $null
    }
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

function Get-NormalizedMetadataProjection([object]$Metadata) {
    $licenseValue = Get-PropertyValue $Metadata 'license'
    $licenseId = if ($licenseValue -is [string]) { [string]$licenseValue } else { [string](Get-PropertyValue $licenseValue 'id') }
    $resourceType = Get-PropertyValue $Metadata 'resource_type'
    $normalizedType = if ($null -ne $resourceType) {
        [ordered]@{
            type = [string](Get-PropertyValue $resourceType 'type')
            subtype = [string](Get-PropertyValue $resourceType 'subtype')
        }
    } else {
        [ordered]@{
            type = [string](Get-PropertyValue $Metadata 'upload_type')
            subtype = [string](Get-PropertyValue $Metadata 'publication_type')
        }
    }
    $normalizePeople = {
        param([array]$People, [bool]$Contributor)
        return @($People | ForEach-Object {
            $person = [ordered]@{ name = [string](Get-PropertyValue $_ 'name') }
            if ($Contributor) { $person['type'] = [string](Get-PropertyValue $_ 'type') }
            foreach ($field in @('affiliation','orcid','gnd')) {
                $value = [string](Get-PropertyValue $_ $field)
                if (-not [string]::IsNullOrWhiteSpace($value)) { $person[$field] = $value }
            }
            $person
        })
    }
    $related = @((Get-PropertyValue $Metadata 'related_identifiers') | ForEach-Object {
        [ordered]@{
            identifier = [string](Get-PropertyValue $_ 'identifier')
            relation = [string](Get-PropertyValue $_ 'relation')
            scheme = [string](Get-PropertyValue $_ 'scheme')
        }
    })
    return [ordered]@{
        title = [string](Get-PropertyValue $Metadata 'title')
        resource_type = $normalizedType
        description = [string](Get-PropertyValue $Metadata 'description')
        creators = @(& $normalizePeople @(Get-PropertyValue $Metadata 'creators') $false)
        contributors = @(& $normalizePeople @(Get-PropertyValue $Metadata 'contributors') $true)
        access_right = [string](Get-PropertyValue $Metadata 'access_right')
        license = $licenseId
        language = [string](Get-PropertyValue $Metadata 'language')
        version = [string](Get-PropertyValue $Metadata 'version')
        publication_date = [string](Get-PropertyValue $Metadata 'publication_date')
        keywords = @((Get-PropertyValue $Metadata 'keywords') | ForEach-Object { [string]$_ })
        related_identifiers = $related
        notes = [string](Get-PropertyValue $Metadata 'notes')
        references = @((Get-PropertyValue $Metadata 'references') | ForEach-Object { [string]$_ })
        alternate_identifiers = @((Get-PropertyValue $Metadata 'alternate_identifiers'))
        dates = @((Get-PropertyValue $Metadata 'dates'))
        locations = @((Get-PropertyValue $Metadata 'locations'))
        grants = @((Get-PropertyValue $Metadata 'grants'))
        communities = @((Get-PropertyValue $Metadata 'communities'))
        subjects = @((Get-PropertyValue $Metadata 'subjects'))
        method = [string](Get-PropertyValue $Metadata 'method')
    }
}

function Assert-CriticalMetadata([object]$Metadata, [string]$Context, [object]$ReferenceMetadata = $null) {
    if ($null -eq $Metadata) { throw "Missing metadata in $Context." }
    $licenseValue = Get-PropertyValue $Metadata 'license'
    $licenseId = if ($licenseValue -is [string]) { [string]$licenseValue } else { [string](Get-PropertyValue $licenseValue 'id') }
    $creators = @(Get-PropertyValue $Metadata 'creators' | ForEach-Object { [string]$_.name })
    $contributors = @(Get-PropertyValue $Metadata 'contributors')
    $hasEditor = @($contributors | Where-Object { [string]$_.name -ceq 'Floris' -and [string]$_.type -ceq 'Editor' }).Count -eq 1
    $relatedObjects = @(Get-PropertyValue $Metadata 'related_identifiers')
    $related = @($relatedObjects | ForEach-Object { [string]$_.identifier })
    $hasExactSourceRelation = @($relatedObjects | Where-Object {
        [string]$_.identifier -ceq $sourceUrl -and
        [string]$_.relation -ceq 'isDerivedFrom' -and
        [string]$_.scheme -ceq 'url'
    }).Count -eq 1
    $resourceType = Get-PropertyValue $Metadata 'resource_type'
    $typeOk = (
        ([string](Get-PropertyValue $Metadata 'upload_type') -ceq 'publication' -and
         [string](Get-PropertyValue $Metadata 'publication_type') -ceq 'book') -or
        ([string](Get-PropertyValue $resourceType 'type') -ceq 'publication' -and
         [string](Get-PropertyValue $resourceType 'subtype') -ceq 'book')
    )
    if ([string](Get-PropertyValue $Metadata 'title') -cne $expectedTitle -or
        [string](Get-PropertyValue $Metadata 'version') -cne $expectedVersion -or
        $licenseId -cne 'cc-by-4.0' -or
        [string](Get-PropertyValue $Metadata 'language') -cne 'ind' -or
        [string](Get-PropertyValue $Metadata 'access_right') -cne 'open' -or
        -not $typeOk -or
        $creators.Count -ne 1 -or $creators[0] -cne 'Roberts, David Michael' -or
        $contributors.Count -ne 1 -or -not $hasEditor -or $related.Count -ne 1 -or -not $hasExactSourceRelation -or
        -not ([string](Get-PropertyValue $Metadata 'notes')).Contains($releaseId, [StringComparison]::Ordinal)) {
        throw "Critical metadata identity/rights mismatch in $Context."
    }
    $description = [string](Get-PropertyValue $Metadata 'description')
    $notes = [string](Get-PropertyValue $Metadata 'notes')
    foreach ($requiredDisclosure in @(
        'Status: edisi bertahap, belum lengkap.',
        'Codex (OpenAI) digunakan sebagai alat bantu',
        'tidak disponsori, didukung, disahkan, atau diberi status resmi'
    )) {
        if (-not $description.Contains($requiredDisclosure, [StringComparison]::Ordinal)) {
            throw "Required incomplete/tool/non-endorsement disclosure is missing in $Context."
        }
    }
    if (-not $notes.Contains('bukan klaim penyelesaian edisi penuh', [StringComparison]::Ordinal)) {
        throw "Required incomplete-checkpoint note is missing in $Context."
    }
    if ($null -ne $ReferenceMetadata) {
        $actualProjection = (Get-NormalizedMetadataProjection $Metadata) | ConvertTo-Json -Depth 12 -Compress
        $referenceProjection = (Get-NormalizedMetadataProjection $ReferenceMetadata) | ConvertTo-Json -Depth 12 -Compress
        if ($actualProjection -cne $referenceProjection) {
            throw "Client-controlled metadata drifted from the exact packaged reference in $Context."
        }
    }
}

function Test-ExactReleaseVersion([object]$Object) {
    $metadata = Get-PropertyValue $Object 'metadata'
    return (
        $null -ne $metadata -and
        [string](Get-PropertyValue $metadata 'title') -ceq $expectedTitle -and
        [string](Get-PropertyValue $metadata 'version') -ceq $expectedVersion
    )
}

function Assert-TransactionIdentity([object]$Transaction, [string]$MetadataHash, [string]$ManifestHash) {
    $allowedModes = @('new_concept','new_version_existing_concept','existing_published_exact')
    $allowedStates = @('create_requested','newversion_requested','created_or_resumed','draft_verified_publish_requested','published_and_anonymously_verified')
    $mode = [string](Get-PropertyValue $Transaction 'creation_mode')
    $state = [string](Get-PropertyValue $Transaction 'state')
    $depositionId = [string](Get-PropertyValue $Transaction 'deposition_id')
    if ([string](Get-PropertyValue $Transaction 'schema_version') -cne '1.0' -or
        [string](Get-PropertyValue $Transaction 'release_id') -cne $releaseId -or
        [string](Get-PropertyValue $Transaction 'title') -cne $expectedTitle -or
        [string](Get-PropertyValue $Transaction 'version') -cne $expectedVersion -or
        [string](Get-PropertyValue $Transaction 'metadata_sha256') -cne $MetadataHash -or
        [string](Get-PropertyValue $Transaction 'manifest_sha256') -cne $ManifestHash -or
        $allowedModes -cnotcontains $mode -or $allowedStates -cnotcontains $state) {
        throw 'Existing Zenodo transaction identity or state is invalid for this exact release.'
    }
    if ($state -notin @('create_requested','newversion_requested') -and [string]::IsNullOrWhiteSpace($depositionId)) {
        throw 'Zenodo transaction lacks its required deposition identity.'
    }
    if ($state -ceq 'newversion_requested' -and
        ([string]::IsNullOrWhiteSpace([string](Get-PropertyValue $Transaction 'parent_deposition_id')) -or
         [string]::IsNullOrWhiteSpace([string](Get-PropertyValue $Transaction 'concept_key')))) {
        throw 'New-version transaction intent lacks its parent/concept identity.'
    }
    $validStatesByMode = @{
        new_concept = @('create_requested','created_or_resumed','draft_verified_publish_requested','published_and_anonymously_verified')
        new_version_existing_concept = @('newversion_requested','created_or_resumed','draft_verified_publish_requested','published_and_anonymously_verified')
        existing_published_exact = @('created_or_resumed','published_and_anonymously_verified')
    }
    if ($validStatesByMode[$mode] -cnotcontains $state) {
        throw 'Zenodo transaction creation mode and state combination is invalid.'
    }
}

function Assert-ReleaseChild([string]$Path) {
    $full = [IO.Path]::GetFullPath($Path)
    $prefix = [IO.Path]::GetFullPath($releaseRoot).TrimEnd('\') + '\'
    if (-not $full.StartsWith($prefix, [StringComparison]::OrdinalIgnoreCase)) {
        throw "Refusing path outside the release root: $full"
    }
}

function Write-JsonAtomic([string]$Path, [object]$Value) {
    $temporary = "$Path.$([guid]::NewGuid().ToString('N')).tmp"
    try {
        [IO.File]::WriteAllText(
            $temporary,
            ($Value | ConvertTo-Json -Depth 14) + "`n",
            [Text.UTF8Encoding]::new($false)
        )
        Move-Item -LiteralPath $temporary -Destination $Path -Force
    } finally {
        if (Test-Path -LiteralPath $temporary) { Remove-Item -LiteralPath $temporary -Force }
    }
}

function Get-SecretToken([string]$Path) {
    $text = [IO.File]::ReadAllText($Path)
    $candidates = [Collections.Generic.List[string]]::new()
    foreach ($line in ($text -split "\r?\n")) {
        $trimmed = $line.Trim().Trim('`')
        if ($trimmed -match '^(?i)(?:[-*]\s*)?(?:zenodo\s+)?(?:access\s+)?token\s*[:=]\s*([A-Za-z0-9._~-]{30,})\s*$') {
            $candidates.Add($Matches[1])
        } elseif ($trimmed -match '^[A-Za-z0-9][A-Za-z0-9._~-]{29,}$') {
            $candidates.Add($trimmed)
        }
    }
    $unique = @($candidates | Sort-Object -Unique)
    if ($unique.Count -ne 1) {
        throw 'Zenodo credential file must contain exactly one unambiguous token value.'
    }
    return $unique[0]
}

function Assert-TokenAbsentFromArtifacts([string]$Token) {
    Add-Type -AssemblyName System.IO.Compression
    $assertBytes = {
        param([byte[]]$Bytes, [string]$Label)
        $asLatin1 = [Text.Encoding]::Latin1.GetString($Bytes)
        if ($asLatin1.Contains($Token, [StringComparison]::Ordinal)) {
            throw "Credential material is present in release content: $Label"
        }
    }
    foreach ($name in $releaseNames) {
        $path = Join-Path $artifactsDir $name
        & $assertBytes ([IO.File]::ReadAllBytes($path)) $name
        if ($name.EndsWith('.zip', [StringComparison]::OrdinalIgnoreCase)) {
            $stream = [IO.File]::OpenRead($path)
            try {
                $archive = [IO.Compression.ZipArchive]::new($stream, [IO.Compression.ZipArchiveMode]::Read, $false)
                try {
                    foreach ($entry in $archive.Entries) {
                        $entryStream = $entry.Open()
                        try {
                            $memory = [IO.MemoryStream]::new()
                            try {
                                $entryStream.CopyTo($memory)
                                & $assertBytes ($memory.ToArray()) "$name::$($entry.FullName)"
                            } finally { $memory.Dispose() }
                        } finally { $entryStream.Dispose() }
                    }
                } finally { $archive.Dispose() }
            } finally { $stream.Dispose() }
        }
    }
    & $assertBytes ([IO.File]::ReadAllBytes($metadataPath)) 'metadata.json'
}

function Convert-ResponseJson([object]$Response, [string]$Label) {
    if ([string]::IsNullOrWhiteSpace([string]$Response.Content)) { return $null }
    try { return ([string]$Response.Content | ConvertFrom-Json) }
    catch { throw "Zenodo returned non-JSON content for $Label (HTTP $([int]$Response.StatusCode))." }
}

$headers = $null
function Invoke-ZenodoRequest {
    param(
        [Parameter(Mandatory = $true)][ValidateSet('GET','POST','PUT','DELETE')][string]$Method,
        [Parameter(Mandatory = $true)][string]$Uri,
        [Parameter(Mandatory = $true)][string]$Label,
        [bool]$Authenticated = $true,
        [string]$JsonBody,
        [string]$InFile,
        [int[]]$AllowedStatus = @(200)
    )
    $parsedUri = [uri]$Uri
    if ($Authenticated -and ($parsedUri.Scheme -cne 'https' -or $parsedUri.Host -cne 'zenodo.org')) {
        throw "Refusing to send a Zenodo credential outside https://zenodo.org for $Label."
    }
    $arguments = @{
        Method = $Method
        Uri = $Uri
        SkipHttpErrorCheck = $true
        MaximumRedirection = if ($Authenticated) { 0 } else { 5 }
    }
    if ($Authenticated) { $arguments.Headers = $headers }
    if ($PSBoundParameters.ContainsKey('JsonBody')) {
        $arguments.ContentType = 'application/json'
        $arguments.Body = $JsonBody
    }
    if ($PSBoundParameters.ContainsKey('InFile')) {
        $arguments.InFile = $InFile
        $arguments.ContentType = 'application/octet-stream'
    }
    $response = Invoke-WebRequest @arguments
    if ($AllowedStatus -notcontains [int]$response.StatusCode) {
        throw "Zenodo request failed for $Label (HTTP $([int]$response.StatusCode))."
    }
    return [pscustomobject]@{
        StatusCode = [int]$response.StatusCode
        Json = Convert-ResponseJson $response $Label
    }
}

function Get-SearchItems([object]$Document) {
    if ($null -eq $Document) { return @() }
    if ($Document -is [array]) { return @($Document) }
    $hits = Get-PropertyValue $Document 'hits'
    $hitItems = Get-PropertyValue $hits 'hits'
    if ($null -ne $hitItems) { return @($hitItems) }
    $items = Get-PropertyValue $Document 'items'
    if ($null -ne $items) { return @($items) }
    return @($Document)
}

function Get-AllDepositions([string]$Query) {
    $items = [Collections.Generic.List[object]]::new()
    for ($page = 1; $page -le 100; $page++) {
        $uri = "$apiRoot/deposit/depositions?size=100&page=$page&all_versions=1&q=$([uri]::EscapeDataString($Query))"
        $response = Invoke-ZenodoRequest -Method GET -Uri $uri -Label 'authenticated deposition search' -AllowedStatus @(200)
        $batch = @(Get-SearchItems $response.Json)
        foreach ($item in $batch) { $items.Add($item) }
        if ($batch.Count -lt 100) { break }
        if ($page -eq 100) { throw 'Authenticated deposition search exceeded its bounded pagination limit.' }
    }
    return @($items)
}

function Get-AllPublicRecords([string]$Query) {
    $items = [Collections.Generic.List[object]]::new()
    for ($page = 1; $page -le 100; $page++) {
        $uri = "$apiRoot/records?size=25&page=$page&all_versions=1&q=$([uri]::EscapeDataString($Query))"
        $response = Invoke-ZenodoRequest -Method GET -Uri $uri -Label 'anonymous public-record search' -Authenticated $false -AllowedStatus @(200)
        $batch = @(Get-SearchItems $response.Json)
        foreach ($item in $batch) { $items.Add($item) }
        if ($batch.Count -lt 25) { break }
        if ($page -eq 100) { throw 'Anonymous record search exceeded its bounded pagination limit.' }
    }
    return @($items)
}

function Get-ObjectId([object]$Object) {
    $id = Get-PropertyValue $Object 'id'
    if (-not [string]::IsNullOrWhiteSpace([string]$id)) { return [string]$id }
    $recordId = Get-PropertyValue $Object 'record_id'
    if (-not [string]::IsNullOrWhiteSpace([string]$recordId)) { return [string]$recordId }
    return ''
}

function Test-SameWork([object]$Object) {
    $metadata = Get-PropertyValue $Object 'metadata'
    if ($null -eq $metadata) { return $false }
    $title = [string]$metadata.title
    $creatorNames = @($metadata.creators | ForEach-Object { [string]$_.name })
    $related = @(Get-PropertyValue $metadata 'related_identifiers' | ForEach-Object { [string]$_.identifier })
    $notes = [string](Get-PropertyValue $metadata 'notes')
    return (
        $title.StartsWith('Topologi Aljabar:', [StringComparison]::Ordinal) -and
        $creatorNames -ccontains 'Roberts, David Michael' -and
        (($related -ccontains $sourceUrl) -or $notes.Contains('o012-roberts-id-', [StringComparison]::Ordinal))
    )
}

function Get-ConceptKey([object]$Object) {
    foreach ($property in @('conceptrecid','concept_id')) {
        $value = [string](Get-PropertyValue $Object $property)
        if (-not [string]::IsNullOrWhiteSpace($value)) { return $value }
    }
    $conceptDoi = [string](Get-PropertyValue $Object 'conceptdoi')
    if (-not [string]::IsNullOrWhiteSpace($conceptDoi)) { return $conceptDoi }
    return Get-ObjectId $Object
}

function Resolve-TransactionIntent {
    param(
        [Parameter(Mandatory = $true)][object]$Transaction,
        [Parameter(Mandatory = $true)][AllowEmptyCollection()][object[]]$SameWorkDepositions,
        [bool]$AllowRequest = $false
    )
    $state = [string](Get-PropertyValue $Transaction 'state')
    $mode = [string](Get-PropertyValue $Transaction 'creation_mode')
    if ($state -ceq 'create_requested') {
        $allDrafts = @($SameWorkDepositions | Where-Object { -not [bool]$_.submitted })
        $candidates = @($allDrafts | Where-Object {
            [string]$_.metadata.title -ceq $expectedTitle -and [string]$_.metadata.version -ceq $expectedVersion
        })
        if ($allDrafts.Count -ne $candidates.Count -or $candidates.Count -gt 1) {
            throw 'Create-intent recovery found an ambiguous or different same-work draft.'
        }
        if ($candidates.Count -gt 0) {
            throw 'Persisted create intent found an unbound matching draft; refusing to adopt or mutate it.'
        }
        if (-not $AllowRequest) {
            throw 'Persisted create intent has no bound deposition; refusing an automatic repeat POST.'
        }
        $created = Invoke-ZenodoRequest -Method POST -Uri "$apiRoot/deposit/depositions" -Label 'create first deposition from persisted intent' -JsonBody $metadataText -AllowedStatus @(201)
        $deposit = $created.Json
    } elseif ($state -ceq 'newversion_requested') {
        $parentId = [string](Get-PropertyValue $Transaction 'parent_deposition_id')
        $expectedConcept = [string](Get-PropertyValue $Transaction 'concept_key')
        $parentResponse = Invoke-ZenodoRequest -Method GET -Uri "$apiRoot/deposit/depositions/$parentId" -Label 'recover parent for persisted new-version intent' -AllowedStatus @(200)
        $parent = $parentResponse.Json
        if (-not (Test-SameWork $parent) -or (Get-ConceptKey $parent) -cne $expectedConcept) {
            throw 'Persisted new-version intent is not bound to the retrieved parent concept.'
        }
        $draftUrl = [string](Get-PropertyValue (Get-PropertyValue $parent 'links') 'latest_draft')
        $deposit = $null
        if (-not [string]::IsNullOrWhiteSpace($draftUrl)) {
            $draftResponse = Invoke-ZenodoRequest -Method GET -Uri $draftUrl -Label 'inspect latest draft for persisted new-version intent' -AllowedStatus @(200)
            if (-not [bool]$draftResponse.Json.submitted) {
                throw 'Persisted new-version intent found an unbound latest draft; refusing to adopt or mutate it.'
            }
        }
        if (-not $AllowRequest) {
            throw 'Persisted new-version intent has no bound deposition; refusing an automatic repeat POST.'
        }
        $newVersion = Invoke-ZenodoRequest -Method POST -Uri "$apiRoot/deposit/depositions/$parentId/actions/newversion" -Label 'create new version from persisted intent' -AllowedStatus @(201)
        $candidate = $newVersion.Json
        $candidateDraftUrl = [string](Get-PropertyValue (Get-PropertyValue $candidate 'links') 'latest_draft')
        if (-not [string]::IsNullOrWhiteSpace($candidateDraftUrl)) {
            $draftResponse = Invoke-ZenodoRequest -Method GET -Uri $candidateDraftUrl -Label 'retrieve newly created version draft' -AllowedStatus @(200)
            $deposit = $draftResponse.Json
        } elseif (-not [bool]$candidate.submitted) {
            $deposit = $candidate
        } else {
            throw 'Zenodo new-version response did not expose a draft identity.'
        }
    } else {
        throw "Transaction state is not a recoverable request intent: $state"
    }
    if ($null -eq $deposit -or [string]::IsNullOrWhiteSpace((Get-ObjectId $deposit)) -or -not (Test-SameWork $deposit)) {
        throw 'Zenodo request intent did not resolve to one exact same-work deposition.'
    }
    $resolvedConcept = Get-ConceptKey $deposit
    $storedConcept = [string](Get-PropertyValue $Transaction 'concept_key')
    if ($mode -ceq 'new_version_existing_concept' -and $resolvedConcept -cne $storedConcept) {
        throw 'Resolved new-version draft left the persisted concept lineage.'
    }
    Set-PropertyValue $Transaction 'deposition_id' (Get-ObjectId $deposit)
    Set-PropertyValue $Transaction 'concept_key' $resolvedConcept
    Set-PropertyValue $Transaction 'state' 'created_or_resumed'
    Set-PropertyValue $Transaction 'updated_at_utc' ([DateTimeOffset]::UtcNow.ToString('o'))
    Write-JsonAtomic $transactionPath $Transaction
    return $deposit
}

function Get-RemoteFileName([object]$File) {
    $filename = [string](Get-PropertyValue $File 'filename')
    if (-not [string]::IsNullOrWhiteSpace($filename)) { return $filename }
    return [string](Get-PropertyValue $File 'key')
}

function Get-RemoteFileBytes([object]$File) {
    $filesize = Get-PropertyValue $File 'filesize'
    if ($null -ne $filesize -and -not [string]::IsNullOrWhiteSpace([string]$filesize)) { return [int64]$filesize }
    return [int64](Get-PropertyValue $File 'size')
}

function Get-RemoteFileMd5([object]$File) {
    $value = [string](Get-PropertyValue $File 'checksum')
    if ([string]::IsNullOrWhiteSpace($value)) { $value = [string](Get-PropertyValue $File 'computed_md5') }
    return ($value -replace '^(?i)md5:', '').ToLowerInvariant()
}

function Get-PublicFiles([object]$Record) {
    $files = Get-PropertyValue $Record 'files'
    if ($files -is [array]) { return @($files) }
    $entries = Get-PropertyValue $files 'entries'
    if ($null -ne $entries) {
        return @($entries.psobject.Properties | ForEach-Object {
            $value = $_.Value
            if ([string]::IsNullOrWhiteSpace([string]$value.key)) { $value | Add-Member -NotePropertyName key -NotePropertyValue $_.Name -Force }
            $value
        })
    }
    return @($files)
}

function Get-PublicDownloadUrl([object]$File) {
    foreach ($property in @('content','download','self')) {
        $value = [string](Get-PropertyValue (Get-PropertyValue $File 'links') $property)
        if (-not [string]::IsNullOrWhiteSpace($value)) { return $value }
    }
    throw "Public file lacks an anonymous download URL: $(Get-RemoteFileName $File)"
}

function Assert-ExactLocalInventory {
    $actual = @(Get-ChildItem -LiteralPath $artifactsDir -File | ForEach-Object Name | Sort-Object)
    if (($actual -join "`n") -cne (($releaseNames | Sort-Object) -join "`n")) {
        throw 'Local Zenodo release inventory is not the exact eight-file allowlist.'
    }
}

function Assert-VerifiedLocalRelease([string]$Label) {
    $result = @(& $verifyScript -ReleaseDirectory $artifactsDir)
    if ($result.Count -ne 1 -or [string](Get-PropertyValue $result[0] 'Status') -cne 'PASS') {
        throw "$Label release verification did not return one PASS result."
    }
}

foreach ($path in @($metadataPath, $verifyScript, $secretPath)) {
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { throw "Missing required release input: $path" }
}
if (-not (Test-Path -LiteralPath $artifactsDir -PathType Container)) { throw "Missing packaged release directory: $artifactsDir" }
Assert-ExactLocalInventory

# First independent gate happens before credential access or network mutation.
Assert-VerifiedLocalRelease 'Preflight'

$metadataText = [IO.File]::ReadAllText($metadataPath)
$metadataDocument = $metadataText | ConvertFrom-Json
Assert-CriticalMetadata $metadataDocument.metadata 'external metadata.json'
if ($metadataText -match '(?i)\bTTP\b|Translation and Transcription Project|C:\\Users\\|C:/Users/') {
    throw 'Forbidden umbrella name or private path found in Zenodo metadata.'
}

$manifestPath = Join-Path $artifactsDir 'release-manifest.json'
$metadataHash = Get-Sha256 $metadataPath
$manifestHash = Get-Sha256 $manifestPath
$manifestDocument = [IO.File]::ReadAllText($manifestPath) | ConvertFrom-Json
if ([string]$manifestDocument.metadata_sha256 -cne $metadataHash) {
    throw 'External Zenodo metadata is not the exact metadata embedded and bound by the release manifest.'
}
$transaction = $null
if (Test-Path -LiteralPath $transactionPath -PathType Leaf) {
    $transaction = [IO.File]::ReadAllText($transactionPath) | ConvertFrom-Json
    Assert-TransactionIdentity $transaction $metadataHash $manifestHash
}

$lockStream = $null
$lockOwned = $false
$token = $null
try {
    try {
        $lockStream = [IO.File]::Open($lockPath, [IO.FileMode]::CreateNew, [IO.FileAccess]::ReadWrite, [IO.FileShare]::None)
        $lockOwned = $true
    } catch {
        throw "Another release operation is active or a stale lock needs inspection: $lockPath"
    }

    # Re-read every mutable identity under the shared lock. A package swap
    # between the preliminary gate and lock acquisition fails closed.
    Assert-ExactLocalInventory
    Assert-VerifiedLocalRelease 'Locked preflight'
    $lockedMetadataText = [IO.File]::ReadAllText($metadataPath)
    $lockedMetadataHash = Get-Sha256 $metadataPath
    $lockedManifestHash = Get-Sha256 $manifestPath
    $lockedManifestDocument = [IO.File]::ReadAllText($manifestPath) | ConvertFrom-Json
    if ($lockedMetadataText -cne $metadataText -or $lockedMetadataHash -cne $metadataHash -or
        $lockedManifestHash -cne $manifestHash -or
        [string]$lockedManifestDocument.metadata_sha256 -cne $lockedMetadataHash) {
        throw 'Release bytes changed before the shared lock was acquired; rerun from a stable package.'
    }
    if (Test-Path -LiteralPath $transactionPath -PathType Leaf) {
        $lockedTransaction = [IO.File]::ReadAllText($transactionPath) | ConvertFrom-Json
        Assert-TransactionIdentity $lockedTransaction $lockedMetadataHash $lockedManifestHash
        $transaction = $lockedTransaction
    } elseif ($null -ne $transaction) {
        throw 'Zenodo transaction disappeared before the shared lock was acquired.'
    } else {
        $transaction = $null
    }

    $token = Get-SecretToken $secretPath
    Assert-TokenAbsentFromArtifacts $token
    $headers = @{ Authorization = "Bearer $token" }

    $depositionsById = @{}
    foreach ($query in @('metadata.title:"Topologi Aljabar"', "metadata.title:`"$expectedTitle`"")) {
        foreach ($item in @(Get-AllDepositions $query)) { $depositionsById[(Get-ObjectId $item)] = $item }
    }
    $sameWorkDepositions = @($depositionsById.Values | Where-Object { Test-SameWork $_ })
    $exactDepositions = @($depositionsById.Values | Where-Object { Test-ExactReleaseVersion $_ })
    $foreignExactDepositions = @($exactDepositions | Where-Object { -not (Test-SameWork $_) })
    if ($foreignExactDepositions.Count -gt 0) {
        throw 'An exact-title/version deposition exists without the required work identity; refusing to duplicate or adopt it.'
    }
    $conceptKeys = @($sameWorkDepositions | ForEach-Object { Get-ConceptKey $_ } | Sort-Object -Unique)
    if ($conceptKeys.Count -gt 1) { throw 'Multiple Zenodo concepts match this exact work; refusing ambiguous publication.' }

    $publicById = @{}
    foreach ($query in @('metadata.title:"Topologi Aljabar"', "metadata.title:`"$expectedTitle`"")) {
        foreach ($item in @(Get-AllPublicRecords $query)) { $publicById[(Get-ObjectId $item)] = $item }
    }
    $sameWorkPublic = @($publicById.Values | Where-Object { Test-SameWork $_ })
    $exactPublicRecords = @($publicById.Values | Where-Object { Test-ExactReleaseVersion $_ })
    $foreignExactPublicRecords = @($exactPublicRecords | Where-Object { -not (Test-SameWork $_) })
    if ($foreignExactPublicRecords.Count -gt 0) {
        throw 'An exact-title/version public record exists without the required work identity; refusing to duplicate or adopt it.'
    }
    $publicConceptKeys = @($sameWorkPublic | ForEach-Object { Get-ConceptKey $_ } | Sort-Object -Unique)
    if ($publicConceptKeys.Count -gt 1) { throw 'Multiple public Zenodo concepts match this exact work; refusing ambiguity.' }
    if ($conceptKeys.Count -eq 1 -and $publicConceptKeys.Count -eq 1 -and $conceptKeys[0] -cne $publicConceptKeys[0]) {
        throw 'Authenticated and anonymous Zenodo searches disagree on the concept identity.'
    }
    if ($sameWorkPublic.Count -gt 0 -and $sameWorkDepositions.Count -eq 0 -and $null -eq $transaction) {
        throw 'A public lineage exists but no authenticated owned deposition exposes it; refusing a competing concept.'
    }

    $currentPublic = @($exactPublicRecords)
    if ($currentPublic.Count -gt 1) { throw 'More than one public Zenodo record matches the exact release version.' }
    $currentSubmitted = @($exactDepositions | Where-Object { [bool]$_.submitted })
    if ($currentSubmitted.Count -gt 1) { throw 'More than one authenticated deposition matches the exact release version.' }
    if ($currentPublic.Count -eq 1 -and $currentSubmitted.Count -eq 0) {
        throw 'The exact public record is not present among authenticated owned depositions; refusing to claim or duplicate it.'
    }

    $deposit = $null
    $record = $null
    $createdMode = 'existing_public'
    if ($currentPublic.Count -eq 1 -and $null -eq $transaction) {
        $record = $currentPublic[0]
    } else {
        if ($null -ne $transaction) {
            $resumeState = [string](Get-PropertyValue $transaction 'state')
            if ($currentSubmitted.Count -eq 1) {
                $deposit = $currentSubmitted[0]
                $publishedConcept = Get-ConceptKey $deposit
                $storedConcept = [string](Get-PropertyValue $transaction 'concept_key')
                if (-not [string]::IsNullOrWhiteSpace($storedConcept) -and $storedConcept -cne $publishedConcept) {
                    throw 'Persisted transaction concept disagrees with the already-published exact version.'
                }
                Set-PropertyValue $transaction 'deposition_id' (Get-ObjectId $deposit)
                Set-PropertyValue $transaction 'concept_key' $publishedConcept
                Set-PropertyValue $transaction 'state' 'created_or_resumed'
                Set-PropertyValue $transaction 'updated_at_utc' ([DateTimeOffset]::UtcNow.ToString('o'))
                Write-JsonAtomic $transactionPath $transaction
            } else {
                $depositId = [string](Get-PropertyValue $transaction 'deposition_id')
                if ([string]::IsNullOrWhiteSpace($depositId)) {
                    $deposit = Resolve-TransactionIntent -Transaction $transaction -SameWorkDepositions $sameWorkDepositions
                    $depositId = Get-ObjectId $deposit
                } else {
                    $response = Invoke-ZenodoRequest -Method GET -Uri "$apiRoot/deposit/depositions/$depositId" -Label 'resume known deposition' -AllowedStatus @(200)
                    $deposit = $response.Json
                }
            }
            $storedConcept = [string](Get-PropertyValue $transaction 'concept_key')
            $remoteConcept = Get-ConceptKey $deposit
            if (-not (Test-SameWork $deposit) -or [string]::IsNullOrWhiteSpace($storedConcept) -or $remoteConcept -cne $storedConcept) {
                throw 'Known Zenodo transaction is not bound to the retrieved work/concept.'
            }
            if ($conceptKeys.Count -eq 1 -and $remoteConcept -cne $conceptKeys[0]) {
                throw 'Known Zenodo transaction disagrees with the authenticated same-work concept.'
            }
            if ($publicConceptKeys.Count -eq 1 -and $remoteConcept -cne $publicConceptKeys[0]) {
                throw 'Known Zenodo transaction disagrees with the public same-work concept.'
            }
            if ($resumeState -ceq 'draft_verified_publish_requested' -and -not [bool]$deposit.submitted) {
                $publishDeadline = [DateTimeOffset]::UtcNow.AddSeconds(50)
                do {
                    $publishPoll = Invoke-ZenodoRequest -Method GET -Uri "$apiRoot/deposit/depositions/$(Get-ObjectId $deposit)" -Label 'read-only poll of previously requested publication' -AllowedStatus @(200)
                    $deposit = $publishPoll.Json
                    if ([bool]$deposit.submitted) { break }
                    Start-Sleep -Seconds 2
                } while ([DateTimeOffset]::UtcNow -lt $publishDeadline)
                if (-not [bool]$deposit.submitted) {
                    throw 'A prior publish request remains unresolved; refusing to rewrite the draft or repeat the irreversible request.'
                }
            }
            $createdMode = [string](Get-PropertyValue $transaction 'creation_mode')
        } else {
            if ($currentSubmitted.Count -eq 1) {
                $deposit = $currentSubmitted[0]
                $createdMode = 'existing_published_exact'
            } else {
                $drafts = @($sameWorkDepositions | Where-Object { -not [bool]$_.submitted })
                if ($drafts.Count -gt 0) {
                    throw 'An unknown draft already exists for this work; refusing to mutate or duplicate it.'
                }
                $published = @($sameWorkDepositions | Where-Object { [bool]$_.submitted } | Sort-Object modified -Descending)
                if ($published.Count -gt 0) {
                    $latest = $published[0]
                    $latestId = Get-ObjectId $latest
                    $createdMode = 'new_version_existing_concept'
                    $transaction = [ordered]@{
                        schema_version = '1.0'; release_id = $releaseId; title = $expectedTitle; version = $expectedVersion
                        metadata_sha256 = $metadataHash; manifest_sha256 = $manifestHash
                        deposition_id = ''; parent_deposition_id = $latestId; concept_key = Get-ConceptKey $latest
                        creation_mode = $createdMode; state = 'newversion_requested'
                        updated_at_utc = [DateTimeOffset]::UtcNow.ToString('o')
                    }
                } else {
                    $createdMode = 'new_concept'
                    $transaction = [ordered]@{
                        schema_version = '1.0'; release_id = $releaseId; title = $expectedTitle; version = $expectedVersion
                        metadata_sha256 = $metadataHash; manifest_sha256 = $manifestHash
                        deposition_id = ''; concept_key = ''
                        creation_mode = $createdMode; state = 'create_requested'
                        updated_at_utc = [DateTimeOffset]::UtcNow.ToString('o')
                    }
                }
                Write-JsonAtomic $transactionPath $transaction
                $deposit = Resolve-TransactionIntent -Transaction $transaction -SameWorkDepositions $sameWorkDepositions -AllowRequest $true
            }
            if ($null -eq $deposit -or [string]::IsNullOrWhiteSpace((Get-ObjectId $deposit))) {
                throw 'Zenodo did not return the newly created deposition identity.'
            }
            if ($null -eq $transaction) {
                $transaction = [ordered]@{
                    schema_version = '1.0'; release_id = $releaseId; title = $expectedTitle; version = $expectedVersion
                    metadata_sha256 = $metadataHash; manifest_sha256 = $manifestHash
                    deposition_id = Get-ObjectId $deposit; concept_key = Get-ConceptKey $deposit
                    creation_mode = $createdMode; state = 'created_or_resumed'
                    updated_at_utc = [DateTimeOffset]::UtcNow.ToString('o')
                }
                Write-JsonAtomic $transactionPath $transaction
            }
        }

        if ([bool]$deposit.submitted) {
            Assert-CriticalMetadata $deposit.metadata 'known submitted deposition' $metadataDocument.metadata
        } else {
            $depositId = Get-ObjectId $deposit
            $updated = Invoke-ZenodoRequest -Method PUT -Uri "$apiRoot/deposit/depositions/$depositId" -Label 'update exact release metadata' -JsonBody $metadataText -AllowedStatus @(200)
            $deposit = $updated.Json

            $present = @{}
            foreach ($file in @($deposit.files)) { $present[(Get-RemoteFileName $file)] = $file }
            foreach ($name in @($present.Keys)) {
                $localPath = Join-Path $artifactsDir $name
                $file = $present[$name]
                $matches = (
                    ($releaseNames -ccontains $name) -and
                    (Test-Path -LiteralPath $localPath -PathType Leaf) -and
                    (Get-RemoteFileBytes $file) -eq (Get-Item -LiteralPath $localPath).Length -and
                    (Get-RemoteFileMd5 $file) -ceq (Get-Md5 $localPath)
                )
                if (-not $matches) {
                    $deleteUrl = [string](Get-PropertyValue (Get-PropertyValue $file 'links') 'self')
                    if ([string]::IsNullOrWhiteSpace($deleteUrl)) {
                        $fileId = [string]$file.id
                        $deleteUrl = "$apiRoot/deposit/depositions/$depositId/files/$fileId"
                    }
                    Invoke-ZenodoRequest -Method DELETE -Uri $deleteUrl -Label "delete mismatched draft file $name" -AllowedStatus @(204) | Out-Null
                    $present.Remove($name)
                }
            }

            $bucket = [string]$deposit.links.bucket
            if ([string]::IsNullOrWhiteSpace($bucket)) { throw 'Zenodo draft lacks a bucket upload URL.' }
            foreach ($name in $releaseNames) {
                if (-not $present.ContainsKey($name)) {
                    $uploadUri = "$bucket/$([uri]::EscapeDataString($name))"
                    Invoke-ZenodoRequest -Method PUT -Uri $uploadUri -Label "upload $name" -InFile (Join-Path $artifactsDir $name) -AllowedStatus @(200,201) | Out-Null
                }
            }

            $draftResponse = Invoke-ZenodoRequest -Method GET -Uri "$apiRoot/deposit/depositions/$depositId" -Label 'verify complete draft' -AllowedStatus @(200)
            $deposit = $draftResponse.Json
            $draftFiles = @($deposit.files)
            $draftNames = @($draftFiles | ForEach-Object { Get-RemoteFileName $_ } | Sort-Object)
            if (($draftNames -join "`n") -cne (($releaseNames | Sort-Object) -join "`n")) {
                throw 'Zenodo draft file inventory is not the exact release allowlist.'
            }
            foreach ($file in $draftFiles) {
                $name = Get-RemoteFileName $file
                $localPath = Join-Path $artifactsDir $name
                if ((Get-RemoteFileBytes $file) -ne (Get-Item -LiteralPath $localPath).Length -or
                    (Get-RemoteFileMd5 $file) -cne (Get-Md5 $localPath)) {
                    throw "Zenodo draft byte/MD5 mismatch for $name."
                }
            }
            Assert-CriticalMetadata $deposit.metadata 'verified Zenodo draft' $metadataDocument.metadata

            Assert-ExactLocalInventory
            Assert-VerifiedLocalRelease 'Immediate pre-publish'
            Assert-TokenAbsentFromArtifacts $token

            # Repeat duplicate suppression immediately before the irreversible
            # request. The known draft must be the sole authenticated exact
            # title/version object and no public exact version may exist.
            $prePublishDeadline = [DateTimeOffset]::UtcNow.AddSeconds(50)
            do {
                $prePublishDepositions = @(Get-AllDepositions "metadata.title:`"$expectedTitle`"" | Where-Object { Test-ExactReleaseVersion $_ })
                if ($prePublishDepositions.Count -eq 1 -and
                    (Get-ObjectId $prePublishDepositions[0]) -ceq $depositId -and
                    -not [bool]$prePublishDepositions[0].submitted) {
                    break
                }
                if ($prePublishDepositions.Count -gt 0) {
                    throw 'Pre-publish authenticated search found a different or additional exact release object.'
                }
                Start-Sleep -Seconds 2
            } while ([DateTimeOffset]::UtcNow -lt $prePublishDeadline)
            if ($prePublishDepositions.Count -ne 1 -or (Get-ObjectId $prePublishDepositions[0]) -cne $depositId) {
                throw 'Known draft did not become the sole authenticated exact release object before publication.'
            }
            $prePublishPublic = @(Get-AllPublicRecords "metadata.title:`"$expectedTitle`"" | Where-Object { Test-ExactReleaseVersion $_ })
            if ($prePublishPublic.Count -ne 0) {
                throw 'An exact public release appeared before publication; refusing a duplicate publish request.'
            }

            # The duplicate searches can take tens of seconds. Re-read the
            # actual draft and revalidate all client metadata and every file
            # immediately before journaling and issuing the publish request.
            $finalDraftResponse = Invoke-ZenodoRequest -Method GET -Uri "$apiRoot/deposit/depositions/$depositId" -Label 'final immutable draft readback before publication' -AllowedStatus @(200)
            $deposit = $finalDraftResponse.Json
            if ([bool]$deposit.submitted) { throw 'Zenodo draft became submitted before the controlled publish request.' }
            Assert-CriticalMetadata $deposit.metadata 'final pre-publish Zenodo draft' $metadataDocument.metadata
            $finalDraftFiles = @($deposit.files)
            $finalDraftNames = @($finalDraftFiles | ForEach-Object { Get-RemoteFileName $_ } | Sort-Object)
            if (($finalDraftNames -join "`n") -cne (($releaseNames | Sort-Object) -join "`n")) {
                throw 'Final pre-publish Zenodo draft inventory drifted from the exact allowlist.'
            }
            foreach ($file in $finalDraftFiles) {
                $name = Get-RemoteFileName $file
                $localPath = Join-Path $artifactsDir $name
                if ((Get-RemoteFileBytes $file) -ne (Get-Item -LiteralPath $localPath).Length -or
                    (Get-RemoteFileMd5 $file) -cne (Get-Md5 $localPath)) {
                    throw "Final pre-publish byte/MD5 drift for $name."
                }
            }

            Set-PropertyValue $transaction 'state' 'draft_verified_publish_requested'
            Set-PropertyValue $transaction 'updated_at_utc' ([DateTimeOffset]::UtcNow.ToString('o'))
            Write-JsonAtomic $transactionPath $transaction
            Invoke-ZenodoRequest -Method POST -Uri "$apiRoot/deposit/depositions/$depositId/actions/publish" -Label 'publish verified deposition' -AllowedStatus @(200,201,202) | Out-Null

            $deadline = [DateTimeOffset]::UtcNow.AddSeconds(50)
            do {
                $poll = Invoke-ZenodoRequest -Method GET -Uri "$apiRoot/deposit/depositions/$depositId" -Label 'poll publication completion' -AllowedStatus @(200)
                $deposit = $poll.Json
                if ([bool]$deposit.submitted -and -not [string]::IsNullOrWhiteSpace([string](Get-PropertyValue $deposit 'record_id'))) { break }
                Start-Sleep -Seconds 2
            } while ([DateTimeOffset]::UtcNow -lt $deadline)
            if (-not [bool]$deposit.submitted -or [string]::IsNullOrWhiteSpace([string](Get-PropertyValue $deposit 'record_id'))) {
                throw 'Zenodo publication did not become readable within the bounded poll; transaction is persisted for a safe rerun.'
            }
        }

        $publishedRecordId = [string](Get-PropertyValue $deposit 'record_id')
        $recordId = if (-not [string]::IsNullOrWhiteSpace($publishedRecordId)) { $publishedRecordId } else { Get-ObjectId $deposit }
        $deadline = [DateTimeOffset]::UtcNow.AddSeconds(50)
        do {
            $publicResponse = Invoke-ZenodoRequest -Method GET -Uri "$apiRoot/records/$recordId" -Label 'anonymous public record readback' -Authenticated $false -AllowedStatus @(200,404)
            if ($publicResponse.StatusCode -eq 200) { $record = $publicResponse.Json; break }
            Start-Sleep -Seconds 2
        } while ([DateTimeOffset]::UtcNow -lt $deadline)
        if ($null -eq $record) { throw 'Published Zenodo record did not become anonymously readable within 50 seconds.' }
    }

    Assert-CriticalMetadata $record.metadata 'anonymous public Zenodo record' $metadataDocument.metadata
    $recordId = Get-ObjectId $record
    $indexed = $false
    $deadline = [DateTimeOffset]::UtcNow.AddSeconds(50)
    do {
        $exactSearch = @(Get-AllPublicRecords "metadata.title:`"$expectedTitle`"" | Where-Object { Test-ExactReleaseVersion $_ })
        if ($exactSearch.Count -gt 1 -or ($exactSearch.Count -eq 1 -and (Get-ObjectId $exactSearch[0]) -cne $recordId)) {
            throw 'Anonymous exact-title/version search exposed a duplicate or different release record.'
        }
        if ($exactSearch.Count -eq 1) { $indexed = $true; break }
        Start-Sleep -Seconds 2
    } while ([DateTimeOffset]::UtcNow -lt $deadline)
    if (-not $indexed) { throw 'Anonymous exact-title search did not expose the published record within 50 seconds.' }

    $publicFiles = @(Get-PublicFiles $record)
    $publicNames = @($publicFiles | ForEach-Object { Get-RemoteFileName $_ } | Sort-Object)
    if (($publicNames -join "`n") -cne (($releaseNames | Sort-Object) -join "`n")) {
        throw 'Anonymous public file inventory is not the exact release allowlist.'
    }

    $readbackDir = Join-Path $releaseRoot ('.anonymous-readback-' + [guid]::NewGuid().ToString('N'))
    Assert-ReleaseChild $readbackDir
    New-Item -ItemType Directory -Path $readbackDir | Out-Null
    try {
        $fileReceipts = @()
        foreach ($publicFile in @($publicFiles | Sort-Object { Get-RemoteFileName $_ })) {
            $name = Get-RemoteFileName $publicFile
            $localPath = Join-Path $artifactsDir $name
            $readbackPath = Join-Path $readbackDir $name
            $download = Invoke-WebRequest -Method GET -Uri (Get-PublicDownloadUrl $publicFile) -OutFile $readbackPath -PassThru -SkipHttpErrorCheck -MaximumRedirection 5
            if ([int]$download.StatusCode -notin @(200,206)) { throw "Anonymous byte download failed for $name (HTTP $([int]$download.StatusCode))." }
            $local = Get-Item -LiteralPath $localPath
            $readback = Get-Item -LiteralPath $readbackPath
            $localSha = Get-Sha256 $localPath
            if ($local.Length -ne $readback.Length -or $localSha -cne (Get-Sha256 $readbackPath)) {
                throw "Anonymous byte/SHA-256 readback mismatch for $name."
            }
            $fileReceipts += [ordered]@{
                filename = $name
                bytes = [int64]$local.Length
                sha256 = $localSha
                zenodo_checksum = [string](Get-PropertyValue $publicFile 'checksum')
                anonymous_url = Get-PublicDownloadUrl $publicFile
                verified = $true
            }
        }
    } finally {
        if (Test-Path -LiteralPath $readbackDir) { Remove-Item -LiteralPath $readbackDir -Recurse -Force }
    }

    $recordDoi = [string](Get-PropertyValue $record 'doi')
    $recordPids = Get-PropertyValue $record 'pids'
    $recordDoiPid = Get-PropertyValue $recordPids 'doi'
    $doi = if (-not [string]::IsNullOrWhiteSpace($recordDoi)) { $recordDoi } else { [string](Get-PropertyValue $recordDoiPid 'identifier') }
    $recordConceptDoi = [string](Get-PropertyValue $record 'conceptdoi')
    $recordParent = Get-PropertyValue $record 'parent'
    $parentPids = Get-PropertyValue $recordParent 'pids'
    $parentDoiPid = Get-PropertyValue $parentPids 'doi'
    $conceptDoi = if (-not [string]::IsNullOrWhiteSpace($recordConceptDoi)) { $recordConceptDoi } else { [string](Get-PropertyValue $parentDoiPid 'identifier') }
    $publicUrl = [string](Get-PropertyValue (Get-PropertyValue $record 'links') 'self_html')
    if ([string]::IsNullOrWhiteSpace($publicUrl)) { $publicUrl = "https://zenodo.org/records/$recordId" }
    if ([string]::IsNullOrWhiteSpace($doi) -or [string]::IsNullOrWhiteSpace($conceptDoi)) {
        throw 'Anonymous public record lacks its required DOI or concept DOI; refusing a verified-publication receipt.'
    }

    $receipt = [ordered]@{
        schema_version = '1.0'
        release_id = $releaseId
        published_at_utc = [DateTimeOffset]::UtcNow.ToString('o')
        creation_mode = $createdMode
        deposition_id = if ($null -ne $deposit) { Get-ObjectId $deposit } else { $null }
        record_id = $recordId
        title = [string]$record.metadata.title
        version = [string]$record.metadata.version
        doi = $doi
        concept_doi = $conceptDoi
        public_record_url = $publicUrl
        anonymous_api_url = "$apiRoot/records/$recordId"
        metadata_sha256 = $metadataHash
        release_manifest_sha256 = $manifestHash
        source_commit = 'b947ad2e9f9e301bfe24590a9db653bc54fa1a53'
        source_span = 'Notes.tex:134-3046'
        license = 'CC BY 4.0'
        incomplete_checkpoint = $true
        github_state = 'account_reinstated; existing repository active; no Git mutation performed by this Zenodo transaction'
        public_file_count = $fileReceipts.Count
        files = $fileReceipts
        verification = [ordered]@{
            exact_authenticated_search = $true
            exact_anonymous_search = $true
            exact_public_inventory = $true
            anonymous_byte_readback = $true
            all_sha256_match_local = $true
            credential_material_persisted = $false
        }
    }
    Write-JsonAtomic $receiptPath $receipt

    if ($null -ne $transaction) {
        Set-PropertyValue $transaction 'state' 'published_and_anonymously_verified'
        Set-PropertyValue $transaction 'record_id' $recordId
        Set-PropertyValue $transaction 'doi' $doi
        Set-PropertyValue $transaction 'concept_doi' $conceptDoi
        Set-PropertyValue $transaction 'receipt_sha256' (Get-Sha256 $receiptPath)
        Set-PropertyValue $transaction 'updated_at_utc' ([DateTimeOffset]::UtcNow.ToString('o'))
        Write-JsonAtomic $transactionPath $transaction
    }

    [pscustomobject]@{
        Status = 'PUBLISHED_AND_VERIFIED'
        RecordId = $recordId
        DOI = $doi
        ConceptDOI = $conceptDoi
        PublicURL = $publicUrl
        FileCount = $fileReceipts.Count
        ReceiptPath = $receiptPath
        ReceiptSHA256 = Get-Sha256 $receiptPath
    }
} finally {
    $headers = $null
    $token = $null
    if ($null -ne $lockStream) {
        try { $lockStream.Dispose() } catch { Write-Warning 'Could not dispose the release lock handle cleanly.' }
    }
    if ($lockOwned -and (Test-Path -LiteralPath $lockPath)) {
        try { Remove-Item -LiteralPath $lockPath -Force } catch { Write-Warning "Could not remove owned release lock: $lockPath" }
    }
}
