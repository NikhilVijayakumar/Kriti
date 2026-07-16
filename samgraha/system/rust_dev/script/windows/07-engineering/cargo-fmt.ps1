[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)] [string] $RepoRoot,
    [Parameter(Mandatory=$true)] [string] $RepoFingerprint,
    [Parameter(Mandatory=$true)] [string] $Out
)

$executedAt = [DateTime]::UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ")

function Write-Result($status, $evidence, $metrics) {
    $result = [ordered]@{
        check = "cargo-fmt"
        domain = "07-engineering"
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
    Write-Result "error" @("Cannot access repo-root: $RepoRoot") @{ unformatted_files = 0; total_violations = 0 }
}

$cargoToml = Join-Path $RepoRoot "Cargo.toml"
if (-not (Test-Path $cargoToml)) {
    Write-Result "not_applicable" @("No Cargo.toml found — not a Rust project") @{ unformatted_files = 0; total_violations = 0 }
}

if (-not (Get-Command "cargo" -ErrorAction SilentlyContinue)) {
    Write-Result "error" @("cargo not installed — cannot run cargo fmt") @{ unformatted_files = 0; total_violations = 0 }
}

$tmpFile = [System.IO.Path]::GetTempFileName()
try {
    & cargo fmt --all -- --check 2>$tmpFile
    $exitCode = $LASTEXITCODE

    if ($exitCode -eq 0) {
        Write-Result "pass" @("All Rust source files are properly formatted (cargo fmt)") @{ unformatted_files = 0; total_violations = 0 }
    }

    $output = Get-Content $tmpFile -Raw
    $diffCount = ([regex]::Matches($output, "^Diff")).Count
    $unformattedFiles = ([regex]::Matches($output, "^Diff in (.+)") | ForEach-Object { $_.Groups[1].Value } | Select-Object -First 10) -join ", "

    Write-Result "fail" @("$diffCount file(s) need formatting. Run: cargo fmt --all. Files: $unformattedFiles") @{ unformatted_files = $diffCount; total_violations = $output.Split("`n").Count }
} catch {
    Write-Result "error" @("cargo fmt failed: $_") @{ unformatted_files = 0; total_violations = 0 }
} finally {
    Remove-Item -Path $tmpFile -Force -ErrorAction SilentlyContinue
}
