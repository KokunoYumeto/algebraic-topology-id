[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$Lane = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
$Authority = Join-Path $Lane 'authority\upstream\math-notes-563194fae879178b9a6871b249513bfc27968975'
$FrozenTree = Join-Path $Authority 'tree'
$Overlay = Join-Path $Authority 'build-overlay'
$Baseline = Join-Path $Authority 'build-baseline'
$Scratch = Join-Path $Lane 'tmp\fomberg-build-gate'

$Source = Join-Path $FrozenTree 'algebraic_topology.tex'
$Header = Join-Path $FrozenTree 'header.tex'
$License = Join-Path $FrozenTree 'LICENSE'
$Shim = Join-Path $Overlay 'commath.sty'

function Convert-ToPortableEvidenceText {
    param([Parameter(Mandatory = $true)][string]$Text)

    $UserRoot = [Environment]::GetFolderPath('UserProfile')
    $Replacements = [ordered]@{
        $Lane = '<TASK_ROOT>'
        $Lane.Replace('\', '/') = '<TASK_ROOT>'
        $UserRoot = '<LOCAL_ACCOUNT_ROOT>'
        $UserRoot.Replace('\', '/') = '<LOCAL_ACCOUNT_ROOT>'
    }
    foreach ($Pair in $Replacements.GetEnumerator()) {
        # TeX can wrap an absolute path between any two characters.  Match the
        # exact known literal with optional wrapped-line whitespace between
        # characters, keeping the replacement path-scoped rather than
        # redacting coincidental prose.
        $WrappedLiteralPattern = (([string]$Pair.Key).ToCharArray() | ForEach-Object {
            [regex]::Escape([string]$_)
        }) -join '(?:\r?\n[ \t]*)?'
        $Text = [regex]::Replace(
            $Text,
            $WrappedLiteralPattern,
            [string]$Pair.Value,
            [Text.RegularExpressions.RegexOptions]::IgnoreCase
        )
    }
    return $Text
}

function Convert-FileToPortableEvidence {
    param([Parameter(Mandatory = $true)][string]$Path)

    $Text = Get-Content -LiteralPath $Path -Raw
    $Portable = Convert-ToPortableEvidenceText -Text $Text
    Set-Content -LiteralPath $Path -Value $Portable -Encoding utf8NoBOM -NoNewline
}

function Assert-PortableEvidenceFile {
    param([Parameter(Mandatory = $true)][string]$Path)

    $UserRoot = [Environment]::GetFolderPath('UserProfile')
    $Text = Get-Content -LiteralPath $Path -Raw
    # Rejoin only physical wrapping whitespace for the privacy assertion; the
    # evidence file itself keeps its diagnostic line structure.
    $Flat = [regex]::Replace($Text, '\r?\n[ \t]*', '')
    foreach ($Forbidden in @(
        $Lane,
        $Lane.Replace('\', '/'),
        $UserRoot,
        $UserRoot.Replace('\', '/')
    )) {
        if ($Flat.IndexOf($Forbidden, [StringComparison]::OrdinalIgnoreCase) -ge 0) {
            throw "Non-portable absolute path survived evidence sanitization: $Path"
        }
    }
    if ($Flat -match '(?i)[A-Z]:[\\/]Users[\\/]') {
        throw "Unredacted local-account path survived evidence sanitization: $Path"
    }
}

$Expected = [ordered]@{
    $Source = 'd27095de0f38f0c14b2d7716cb52d51d064f0594dd9f82f9d1b3e6af5b35a483'
    $Header = '7c4c5cbe901c1b6c7ae8d6053d42cd28110ece34dd90bc60c5bcb7423e45e28e'
    $License = '0b7fc2608b6d990314e908569407a6058b4a29175167c6d91ca0070c946661be'
}

foreach ($Pair in $Expected.GetEnumerator()) {
    if (-not (Test-Path -LiteralPath $Pair.Key -PathType Leaf)) {
        throw "Missing frozen input: $($Pair.Key)"
    }
    $Actual = (Get-FileHash -Algorithm SHA256 -LiteralPath $Pair.Key).Hash.ToLowerInvariant()
    if ($Actual -ne $Pair.Value) {
        throw "Frozen input hash mismatch: $($Pair.Key): $Actual"
    }
}
if (-not (Test-Path -LiteralPath $Shim -PathType Leaf)) {
    throw "Missing task-local commath compatibility overlay: $Shim"
}

foreach ($ExactPath in @($Scratch, $Baseline)) {
    $ResolvedParent = (Resolve-Path -LiteralPath (Split-Path -Parent $ExactPath)).Path
    if (-not $ResolvedParent.StartsWith($Lane, [StringComparison]::OrdinalIgnoreCase)) {
        throw "Refusing to touch path outside lane: $ExactPath"
    }
    if (Test-Path -LiteralPath $ExactPath) {
        Remove-Item -LiteralPath $ExactPath -Recurse -Force
    }
    New-Item -ItemType Directory -Path $ExactPath | Out-Null
}

$PdfLaTeX = (Get-Command pdflatex -ErrorAction Stop).Source
$PdfInfo = (Get-Command pdfinfo -ErrorAction Stop).Source
$FixedEpoch = '1735689600' # 2025-01-01T00:00:00Z; a declared build normalization value.
$PriorSourceDateEpoch = $env:SOURCE_DATE_EPOCH
$PriorForceSourceDate = $env:FORCE_SOURCE_DATE
$PriorTz = $env:TZ
$PriorTexInputs = $env:TEXINPUTS
$PriorMiKTeXInstaller = $env:MIKTEX_ENABLE_INSTALLER

try {
    $env:SOURCE_DATE_EPOCH = $FixedEpoch
    $env:FORCE_SOURCE_DATE = '1'
    $env:TZ = 'UTC'
    $env:MIKTEX_ENABLE_INSTALLER = '0'
    # The trailing separator preserves the engine's normal system search path.
    $env:TEXINPUTS = "$Overlay$([IO.Path]::PathSeparator)"

    foreach ($RunNumber in 1, 2) {
        $RunDir = Join-Path $Scratch "run-$RunNumber"
        New-Item -ItemType Directory -Path $RunDir | Out-Null
        Copy-Item -LiteralPath $Source -Destination (Join-Path $RunDir 'algebraic_topology.tex')
        Copy-Item -LiteralPath $Header -Destination (Join-Path $RunDir 'header.tex')
        Copy-Item -LiteralPath $License -Destination (Join-Path $RunDir 'LICENSE')

        # Four absent/overbroad packages export no commands or styles used by
        # algebraic_topology.tex. Remove exactly those semantically inert loads
        # from the disposable build copy; the frozen header remains untouched.
        $RunHeader = Join-Path $RunDir 'header.tex'
        $RunHeaderText = Get-Content -LiteralPath $RunHeader -Raw
        $UnusedPackageLines = [ordered]@{
            '\usepackage{esvect} % \vv makes vectors' = '% build overlay: unused esvect dependency omitted'
            '\usepackage{esdiff}' = '% build overlay: unused esdiff dependency omitted'
            '\usepackage{witharrows}' = '% build overlay: unused witharrows dependency omitted'
            '\usepackage{quiver}' = '% build overlay: unused quiver dependency omitted'
        }
        foreach ($UnusedPackageLine in $UnusedPackageLines.GetEnumerator()) {
            if (($RunHeaderText.Split($UnusedPackageLine.Key).Count - 1) -ne 1) {
                throw "Expected exactly one disposable-header match for: $($UnusedPackageLine.Key)"
            }
            $RunHeaderText = $RunHeaderText.Replace($UnusedPackageLine.Key, $UnusedPackageLine.Value)
        }
        Set-Content -LiteralPath $RunHeader -Value $RunHeaderText -Encoding utf8NoBOM -NoNewline

        Push-Location $RunDir
        try {
            foreach ($Pass in 1, 2, 3) {
                & $PdfLaTeX --disable-installer -interaction=nonstopmode -halt-on-error -file-line-error -recorder algebraic_topology.tex *> "pdflatex-pass-$Pass.log"
                if ($LASTEXITCODE -ne 0) {
                    throw "pdflatex failed in clean run $RunNumber pass $Pass"
                }
            }
        }
        finally {
            Pop-Location
        }
    }
}
finally {
    $env:SOURCE_DATE_EPOCH = $PriorSourceDateEpoch
    $env:FORCE_SOURCE_DATE = $PriorForceSourceDate
    $env:TZ = $PriorTz
    $env:TEXINPUTS = $PriorTexInputs
    $env:MIKTEX_ENABLE_INSTALLER = $PriorMiKTeXInstaller
}

$Pdf1 = Join-Path $Scratch 'run-1\algebraic_topology.pdf'
$Pdf2 = Join-Path $Scratch 'run-2\algebraic_topology.pdf'
foreach ($Pdf in @($Pdf1, $Pdf2)) {
    if (-not (Test-Path -LiteralPath $Pdf -PathType Leaf)) {
        throw "Expected PDF was not produced: $Pdf"
    }
}

$Hash1 = (Get-FileHash -Algorithm SHA256 -LiteralPath $Pdf1).Hash.ToLowerInvariant()
$Hash2 = (Get-FileHash -Algorithm SHA256 -LiteralPath $Pdf2).Hash.ToLowerInvariant()
$Bytes1 = (Get-Item -LiteralPath $Pdf1).Length
$Bytes2 = (Get-Item -LiteralPath $Pdf2).Length
if ($Bytes1 -ne $Bytes2 -or $Hash1 -ne $Hash2) {
    throw "Clean-build PDFs differ: run1=$Bytes1/$Hash1 run2=$Bytes2/$Hash2"
}

$FinalPdf = Join-Path $Baseline 'algebraic_topology-baseline.pdf'
Copy-Item -LiteralPath $Pdf1 -Destination $FinalPdf
Copy-Item -LiteralPath (Join-Path $Scratch 'run-1\algebraic_topology.log') -Destination (Join-Path $Baseline 'algebraic_topology.log')
Copy-Item -LiteralPath (Join-Path $Scratch 'run-1\algebraic_topology.fls') -Destination (Join-Path $Baseline 'algebraic_topology.fls')
foreach ($Pass in 1, 2, 3) {
    Copy-Item -LiteralPath (Join-Path $Scratch "run-1\pdflatex-pass-$Pass.log") -Destination (Join-Path $Baseline "pdflatex-pass-$Pass.log")
}

$PdfInfoText = (& $PdfInfo $FinalPdf 2>&1) -join "`n"
$PdfInfoText | Set-Content -LiteralPath (Join-Path $Baseline 'pdfinfo.txt') -Encoding utf8NoBOM

$PackageRows = @()
$Fls = Get-Content -LiteralPath (Join-Path $Baseline 'algebraic_topology.fls')
$InputPaths = $Fls |
    Where-Object { $_.StartsWith('INPUT ') } |
    ForEach-Object { $_.Substring(6).Trim() } |
    Where-Object { $_ -match '\.(sty|cls|def|cfg|fd|map)$' } |
    Sort-Object -Unique
foreach ($InputPath in $InputPaths) {
    if (Test-Path -LiteralPath $InputPath -PathType Leaf) {
        $Item = Get-Item -LiteralPath $InputPath
        $PackageRows += [pscustomobject]@{
            path = Convert-ToPortableEvidenceText -Text $Item.FullName
            bytes = $Item.Length
            sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $Item.FullName).Hash.ToLowerInvariant()
        }
    }
}
$PackageRows | Export-Csv -LiteralPath (Join-Path $Baseline 'tex-input-manifest.csv') -NoTypeInformation -Encoding utf8NoBOM

$Result = [ordered]@{
    schema_version = '1.0.0'
    status = 'PASS'
    authority_commit = '563194fae879178b9a6871b249513bfc27968975'
    authority_tree = 'fb678966d1533d529bdd72f49d8496a3bdc14a9b'
    source_date_epoch = [int64]$FixedEpoch
    engine_path = Convert-ToPortableEvidenceText -Text $PdfLaTeX
    engine_version = ((& $PdfLaTeX --version | Select-Object -First 1) -join '')
    clean_build_count = 2
    passes_per_build = 3
    byte_identical = $true
    pdf_bytes = $Bytes1
    pdf_sha256 = $Hash1
    package_input_count = $PackageRows.Count
    output_pdf = Convert-ToPortableEvidenceText -Text $FinalPdf
    pdfinfo = $PdfInfoText
    path_sanitization = [ordered]@{
        applied = $true
        task_root_placeholder = '<TASK_ROOT>'
        local_account_root_placeholder = '<LOCAL_ACCOUNT_ROOT>'
        wrapped_literal_path_matching = $true
        mathematical_and_build_diagnostic_text_changed = $false
    }
}
$ResultJson = $Result | ConvertTo-Json -Depth 6
$ResultJson | Set-Content -LiteralPath (Join-Path $Baseline 'BUILD_RESULT.json') -Encoding utf8NoBOM

foreach ($EvidenceName in @(
    'algebraic_topology.fls',
    'algebraic_topology.log',
    'pdflatex-pass-1.log',
    'pdflatex-pass-2.log',
    'pdflatex-pass-3.log'
)) {
    $EvidencePath = Join-Path $Baseline $EvidenceName
    Convert-FileToPortableEvidence -Path $EvidencePath
    Assert-PortableEvidenceFile -Path $EvidencePath
}

# The baseline directory now contains every durable proof artifact. Remove the
# two clean build trees at their exact task-local path.
if (Test-Path -LiteralPath $Scratch) {
    Remove-Item -LiteralPath $Scratch -Recurse -Force
}
$ResultJson
