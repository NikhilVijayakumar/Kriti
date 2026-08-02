[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)] [string] $RepoRoot,
    [Parameter(Mandatory=$true)] [string] $RepoFingerprint,
    [Parameter(Mandatory=$true)] [string] $Out
)

# rustfmt-check: first gate in build.md's CI/CD Validation sequence
# (fmt -> clippy -> tests -> ...). `cargo fmt --check` must exit 0.
# Same fixed contract as tier5's lint-pass.ps1: result envelope written to $Out.

$executedAt = [DateTime]::UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ")

function Write-Result($status, $evidence, $metrics) {
    $result = [ordered]@{
        repo_fingerprint = $RepoFingerprint
        check = "rustfmt-check"
        domain = "codegen.build"
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

$emptyMetrics = @{ fmt_exit_code = $null; diff_excerpt_bytes = 0 }

if (-not (Test-Path -LiteralPath $RepoRoot)) {
    Write-Result "error" @("Cannot access repo-root: $RepoRoot") @{ fmt_exit_code = -1; diff_excerpt_bytes = 0 }
}

if (-not (Get-Command cargo -ErrorAction SilentlyContinue)) {
    Write-Result "error" @("cargo not installed") @{ fmt_exit_code = -1; diff_excerpt_bytes = 0 }
}

if (-not (Test-Path -LiteralPath (Join-Path $RepoRoot "Cargo.toml"))) {
    Write-Result "not_applicable" @("No Cargo.toml found at $RepoRoot") $emptyMetrics
}

Push-Location $RepoRoot
try {
    $output = cargo fmt --check 2>&1
    $exitCode = $LASTEXITCODE
} finally {
    Pop-Location
}

$joined = if ($output) { $output -join "`n" } else { "" }
$excerpt = if ($joined.Length -gt 2000) { $joined.Substring(0, 2000) } else { $joined }

$metrics = @{ fmt_exit_code = $exitCode; diff_excerpt_bytes = $joined.Length }

if ($exitCode -eq 0) {
    Write-Result "pass" @("cargo fmt --check passed") $metrics
} else {
    $evidence = @("cargo fmt --check failed with exit code $exitCode")
    if ($excerpt) { $evidence += $excerpt }
    Write-Result "fail" $evidence $metrics
}
