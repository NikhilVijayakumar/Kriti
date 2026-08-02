[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)] [string] $RepoRoot,
    [Parameter(Mandatory=$true)] [string] $RepoFingerprint,
    [Parameter(Mandatory=$true)] [string] $Out,
    [Parameter(Mandatory=$false)] [double] $Threshold = 80
)

# coverage-threshold: measures line coverage with cargo-tarpaulin and reports
# pass/fail against the crate's configured threshold. qa.md leaves the concrete
# number and measurement tool project-specific; the tool is named here only as
# this check's implementation detail, not as generation policy (see
# test/profile-default/unit.yaml, which keeps the tool a per-crate [Tool] slot).
# Same fixed contract as tier5's lint-pass.ps1: result envelope written to $Out.

$executedAt = [DateTime]::UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ")

function Write-Result($status, $evidence, $metrics) {
    $result = [ordered]@{
        repo_fingerprint = $RepoFingerprint
        check = "coverage-threshold"
        domain = "codegen.test"
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

$errorMetrics = @{ line_coverage_pct = $null; threshold_pct = $Threshold; files_measured = 0 }

if (-not (Test-Path -LiteralPath $RepoRoot)) {
    Write-Result "error" @("Cannot access repo-root: $RepoRoot") $errorMetrics
}

if (-not (Get-Command cargo-tarpaulin -ErrorAction SilentlyContinue)) {
    Write-Result "error" @("cargo-tarpaulin not installed (cargo install cargo-tarpaulin)") $errorMetrics
}

Push-Location $RepoRoot
try {
    $raw = (cargo tarpaulin --out Json 2>$null) -join "`n"
    $tarpaulinExit = $LASTEXITCODE
} finally {
    Pop-Location
}

if (-not $raw -or $raw.Trim().Length -eq 0) {
    foreach ($candidate in @("tarpaulin-report.json", "coverage.json")) {
        if (Test-Path -LiteralPath (Join-Path $RepoRoot $candidate)) {
            $raw = Get-Content -Path (Join-Path $RepoRoot $candidate) -Raw -ErrorAction SilentlyContinue
            if ($raw) { break }
        }
    }
}

if ($tarpaulinExit -ne 0 -and -not $raw) {
    Write-Result "error" @("cargo tarpaulin exited with code $tarpaulinExit") $errorMetrics
}

if (-not $raw) {
    Write-Result "error" @("cargo tarpaulin produced no JSON output") $errorMetrics
}

$json = $null
$brace = $raw.IndexOf("{")
if ($brace -ge 0) {
    try { $json = $raw.Substring($brace) | ConvertFrom-Json } catch { $json = $null }
}

if ($null -eq $json) {
    Write-Result "error" @("cargo tarpaulin produced no parseable JSON output") $errorMetrics
}

$coveragePct = $null
$filesMeasured = 0

if ($null -ne $json.coverage -and ($json.coverage.ToString()) -match '^\d+(\.\d+)?$') {
    $coveragePct = [double]$json.coverage.ToString()
    $filesMeasured = @($json.files).Count
} elseif ($json.files) {
    $totalCovered = 0.0
    $totalLines = 0
    foreach ($f in @($json.files)) {
        if ($null -eq $f.coverage) { continue }
        foreach ($v in @($f.coverage)) {
            if ($null -eq $v) { continue }
            $totalLines++
            if ($v -gt 0) { $totalCovered++ }
        }
        $filesMeasured++
    }
    if ($totalLines -gt 0) {
        $coveragePct = [math]::Round(($totalCovered / $totalLines) * 100, 2)
    }
}

if ($null -eq $coveragePct) {
    Write-Result "error" @("tarpaulin returned no line coverage data") $errorMetrics
}

$metrics = @{
    line_coverage_pct = $coveragePct
    threshold_pct = $Threshold
    files_measured = $filesMeasured
}

if ($coveragePct -ge $Threshold) {
    Write-Result "pass" @("Line coverage $coveragePct% meets threshold $Threshold%") $metrics
} else {
    Write-Result "fail" @("Line coverage $coveragePct% is below threshold $Threshold%") $metrics
}
