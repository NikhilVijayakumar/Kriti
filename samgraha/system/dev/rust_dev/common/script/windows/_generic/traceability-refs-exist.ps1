[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)] [string] $DocsRoot,
    [Parameter(Mandatory=$true)] [string] $RepoFingerprint,
    [Parameter(Mandatory=$true)] [string] $Out
)

# traceability-refs-exist — Category C generic script
# Checks that every downstream document referenced in a domain's Traceability
# section actually exists in --docs-root.

if (-not (Test-Path -LiteralPath $DocsRoot -PathType Container)) {
    $result = @{
        check = "traceability-refs-exist"
        domain = "_generic"
        category = "C"
        status = "error"
        metrics = @{ domains_checked = 0; refs_found = 0; refs_valid = 0; refs_missing = 0 }
        evidence = @("docs-root not found: $DocsRoot")
        executed_at = [DateTime]::UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ")
        repo_fingerprint = $RepoFingerprint
    }
    $result | ConvertTo-Json -Depth 10 | Set-Content -Path $Out -Encoding UTF8
    exit 1
}

$executedAt = [DateTime]::UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ")
$domainsChecked = 0
$refsFound = 0
$refsValid = 0
$refsMissing = 0
$evidence = @()

# Domain number → name mapping
$domainNums = @{
    "01"="vision"; "02"="philosophy"; "03"="security"; "04"="feature"
    "05"="architecture"; "06"="design"; "07"="engineering"
    "08"="external-context"; "09"="feature-design"; "10"="feature-technical"
    "11"="prototype"; "12"="qa"; "13"="implementation"; "14"="build"
    "15"="readme"; "16"="product-guide"
}

$mdFiles = Get-ChildItem -Path $DocsRoot -Filter "*.md" -File -Recurse

foreach ($docfile in $mdFiles) {
    $content = Get-Content -Path $docfile.FullName -Raw -ErrorAction SilentlyContinue
    if (-not $content) { continue }

    # Check if file has a Traceability section
    if ($content -notmatch '(?m)^## Traceability') { continue }

    $domainsChecked++
    $docname = $docfile.BaseName

    # Extract content between "## Traceability" and the next "##" heading
    $inTraceability = $false
    $traceabilityLines = @()
    foreach ($line in ($content -split "`n")) {
        if ($line -match '(?m)^## ' -and $inTraceability) { break }
        if ($line -match '(?m)^## Traceability') { $inTraceability = $true; continue }
        if ($inTraceability) { $traceabilityLines += $line }
    }
    $traceabilityContent = $traceabilityLines -join "`n"

    # Find the Consuming Standards table
    $inTable = $false
    foreach ($line in ($traceabilityContent -split "`n")) {
        if ($line -match '^\|[\s]*Standard[\s]*\|') { $inTable = $true; continue }
        if ($inTable) {
            if ($line -match '^\|[\s]*-+') { continue }
            if ($line -notmatch '^\|') { break }

            $columns = $line -split '\|'
            $standard = if ($columns.Length -gt 2) { $columns[1].Trim() } else { "" }
            if (-not $standard) { continue }

            $refsFound++

            # Extract domain number
            $numMatch = [regex]::Match($standard, '\((\d{2})\)')
            if (-not $numMatch.Success) {
                $evidence += "${docname}: Cannot resolve domain number from standard '${standard}'"
                $refsMissing++
                continue
            }

            $domainNum = $numMatch.Groups[1].Value
            $domainName = if ($domainNums.ContainsKey($domainNum)) { $domainNums[$domainNum] } else { "unknown" }

            # Check if any file starts with this domain number
            $matches = Get-ChildItem -Path $DocsRoot -Filter "$domainNum-$domainName*" -File -ErrorAction SilentlyContinue
            if ($matches -and $matches.Count -gt 0) {
                $refsValid++
            } else {
                $refsMissing++
                $evidence += "${docname}: Referenced standard '${standard}' (domain ${domainNum}-${domainName}) has no matching document in docs-root"
            }
        }
    }
}

# Determine status
if ($domainsChecked -eq 0) {
    $status = "not_applicable"
    $evidence = @("No domains with Traceability sections found in docs-root")
} elseif ($refsMissing -gt 0) {
    $status = "fail"
} else {
    $status = "pass"
}

$result = @{
    check = "traceability-refs-exist"
    domain = "_generic"
    category = "C"
    status = $status
    metrics = @{
        domains_checked = $domainsChecked
        refs_found = $refsFound
        refs_valid = $refsValid
        refs_missing = $refsMissing
    }
    evidence = $evidence
    executed_at = $executedAt
    repo_fingerprint = $RepoFingerprint
}

$result | ConvertTo-Json -Depth 10 | Set-Content -Path $Out -Encoding UTF8
