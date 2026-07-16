[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)] [string] $RepoRoot,
    [Parameter(Mandatory=$true)] [string] $RepoFingerprint,
    [Parameter(Mandatory=$true)] [string] $Out
)

$executedAt = [DateTime]::UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ")

function Write-Result($status, $evidence, $metrics) {
    $result = [ordered]@{
        check = "cargo-audit"
        domain = "03-security"
        category = "A"
        status = $status
        metrics = $metrics
        evidence = $evidence
        executed_at = $executedAt
        repo_fingerprint = $RepoFingerprint
    } | ConvertTo-Json -Compress
    Set-Content -Path $Out -Value $result -Encoding UTF8
    if ($status -eq "error") { exit 1 }
    exit 0
}

if (-not (Test-Path -LiteralPath $RepoRoot -PathType Container)) {
    Write-Result "error" @("Cannot access repo-root: $RepoRoot") @{ vulnerability_count = 0; critical_count = 0 }
}

$cargoLock = Join-Path $RepoRoot "Cargo.lock"
if (-not (Test-Path $cargoLock)) {
    Write-Result "not_applicable" @("No Cargo.lock found — cargo-audit requires a lockfile") @{ vulnerability_count = 0; critical_count = 0 }
}

$hasCargoAudit = $null -ne (Get-Command "cargo-audit" -ErrorAction SilentlyContinue)
$hasCargo = $null -ne (Get-Command "cargo" -ErrorAction SilentlyContinue)

if (-not $hasCargoAudit -and -not $hasCargo) {
    Write-Result "error" @("cargo-audit not installed. Install with: cargo install cargo-audit") @{ vulnerability_count = 0; critical_count = 0 }
}

$tmpFile = [System.IO.Path]::GetTempFileName()
try {
    if ($hasCargoAudit) {
        & cargo-audit audit --json -q 2>$null | Set-Content -Path $tmpFile -Encoding UTF8
    } elseif ($hasCargo) {
        & cargo audit --json -q 2>$null | Set-Content -Path $tmpFile -Encoding UTF8
    }

    $content = Get-Content $tmpFile -Raw
    if ([string]::IsNullOrWhiteSpace($content)) {
        Write-Result "pass" @("cargo-audit executed, no vulnerabilities found") @{ vulnerability_count = 0; critical_count = 0 }
    }

    $data = $content | ConvertFrom-Json
    $vulns = @()
    if ($data.vulnerabilities.list) { $vulns = @($data.vulnerabilities.list) }
    $vulnCount = $vulns.Count
    $criticalCount = ($vulns | Where-Object { $_.advisory.cvss.score -ge 9.0 }).Count

    if ($vulnCount -gt 0) {
        $names = ($vulns | Select-Object -First 5 | ForEach-Object { $_.advisory.id }) -join ", "
        Write-Result "fail" @("Found $vulnCount vulnerabilities: $names") @{ vulnerability_count = $vulnCount; critical_count = $criticalCount }
    } else {
        Write-Result "pass" @("cargo-audit passed — no known vulnerabilities in Cargo.lock") @{ vulnerability_count = 0; critical_count = 0 }
    }
} catch {
    Write-Result "error" @("cargo-audit execution failed: $_") @{ vulnerability_count = 0; critical_count = 0 }
} finally {
    Remove-Item -Path $tmpFile -Force -ErrorAction SilentlyContinue
}
