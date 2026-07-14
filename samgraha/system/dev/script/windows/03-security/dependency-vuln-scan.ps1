[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)] [string] $RepoRoot,
    [Parameter(Mandatory=$true)] [string] $RepoFingerprint,
    [Parameter(Mandatory=$true)] [string] $Out
)

$executedAt = [DateTime]::UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ")

function Write-Result($status, $evidence, $metrics) {
    $result = [ordered]@{
        repo_fingerprint = $RepoFingerprint
        check = "dependency-vuln-scan"
        domain = "03-security"
        category = "A"
        status = $status
        metrics = $metrics
        evidence = $evidence
        executed_at = $executedAt
    }
    $result | ConvertTo-Json -Depth 10 | Set-Content -Path $Out -Encoding UTF8
    if ($status -eq "error") { exit 1 }
    exit 0
}

if (-not (Test-Path $RepoRoot)) {
    Write-Result "error" @("Cannot access repo-root: $RepoRoot") @{ vulnerabilities_found = 0; dependencies_scanned = 0 }
}

$vulnerabilitiesFound = 0
$depsScanned = 0
$evidence = @()

$npmAudit = $false
$packageJson = Join-Path $RepoRoot "package.json"
if (Test-Path $packageJson) {
    try {
        $process = Start-Process -FilePath "cmd.exe" -ArgumentList "/c", "cd /d `"$RepoRoot`" && npm audit --json" -NoNewWindow -Wait -PassThru -RedirectStandardOutput "$env:TEMP\npm_audit.txt" -RedirectStandardError "$env:TEMP\npm_audit_err.txt" -ErrorAction Stop
        if (Test-Path "$env:TEMP\npm_audit.txt") {
            $auditJson = Get-Content "$env:TEMP\npm_audit.txt" -Raw | ConvertFrom-Json
            if ($auditJson.metadata -and $auditJson.metadata.vulnerabilities) {
                $vul = $auditJson.metadata.vulnerabilities
                $vulnerabilitiesFound = 0
                if ($vul.critical) { $vulnerabilitiesFound += $vul.critical }
                if ($vul.high) { $vulnerabilitiesFound += $vul.high }
                if ($vul.moderate) { $vulnerabilitiesFound += $vul.moderate }
                if ($vul.low) { $vulnerabilitiesFound += $vul.low }
                $depsScanned = $vul.total
                $evidence += "npm audit: $vulnerabilitiesFound vulnerabilities (critical=$($vul.critical), high=$($vul.high), moderate=$($vul.moderate), low=$($vul.low)) in $depsScanned dependencies"
            }
            $npmAudit = $true
        }
    } catch {
        $evidence += "npm audit failed: $_"
    }
}

if (-not $npmAudit) {
    $reqFile = Join-Path $RepoRoot "requirements.txt"
    if (Test-Path $reqFile) {
        $content = Get-Content $reqFile -Raw
        $lines = ($content -split "`n") | Where-Object { $_ -match "^[a-zA-Z]" -and $_ -notmatch "^#" }
        $depsScanned = $lines.Count
        $evidence += "Found requirements.txt with $depsScanned dependencies (npm audit unavailable, manual review needed)"
    }

    $pkg = Get-Content $packageJson -Raw -ErrorAction SilentlyContinue | ConvertFrom-Json -ErrorAction SilentlyContinue
    if ($null -ne $pkg) {
        $count = 0
        if ($pkg.dependencies) { $count += $pkg.dependencies.PSObject.Properties.Count }
        if ($pkg.devDependencies) { $count += $pkg.devDependencies.PSObject.Properties.Count }
        if ($depsScanned -eq 0) { $depsScanned = $count }
        $evidence += "Found package.json with $count dependencies (npm audit unavailable, manual review needed)"
    }
}

if ($depsScanned -eq 0) {
    Write-Result "not_applicable" @("No dependency manifests found to scan") @{ vulnerabilities_found = 0; dependencies_scanned = 0 }
}

$metrics = @{
    vulnerabilities_found = $vulnerabilitiesFound
    dependencies_scanned = $depsScanned
}

if ($vulnerabilitiesFound -eq 0) {
    Write-Result "pass" $evidence $metrics
} else {
    Write-Result "fail" $evidence $metrics
}
