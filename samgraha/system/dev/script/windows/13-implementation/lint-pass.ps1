[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)] [string] $RepoRoot,
    [Parameter(Mandatory=$true)] [string] $RepoFingerprint,
    [Parameter(Mandatory=$true)] [string] $Out,
    [string] $LintCommand = "npm run lint"
)

$executedAt = [DateTime]::UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ")

function Write-Result($status, $evidence, $metrics) {
    $result = [ordered]@{
        repo_fingerprint = $RepoFingerprint
        check = "lint-pass"
        domain = "13-implementation"
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
    Write-Result "error" @("Cannot access repo-root: $RepoRoot") @{ lint_exit_code = -1; lint_errors = 0 }
}

try {
    $process = Start-Process -FilePath "cmd.exe" -ArgumentList "/c", "cd /d `"$RepoRoot`" && $LintCommand" -NoNewWindow -Wait -PassThru -RedirectStandardOutput "$env:TEMP\lint_stdout.txt" -RedirectStandardError "$env:TEMP\lint_stderr.txt" -ErrorAction Stop
    $exitCode = $process.ExitCode
} catch {
    Write-Result "error" @("Lint command failed to execute: $_") @{ lint_exit_code = -1; lint_errors = 0 }
}

$stdout = if (Test-Path "$env:TEMP\lint_stdout.txt") { Get-Content "$env:TEMP\lint_stdout.txt" -Raw } else { "" }
$stderr = if (Test-Path "$env:TEMP\lint_stderr.txt") { Get-Content "$env:TEMP\lint_stderr.txt" -Raw } else { "" }

$evidence = @()
if ($exitCode -ne 0) {
    $evidence += "Lint command exited with code $exitCode"
    $evidence += "Command: $LintCommand"
    if ($stderr.Length -gt 0) {
        $lines = $stderr -split "`n" | Select-Object -Last 15
        foreach ($line in $lines) {
            if ($line.Trim().Length -gt 0) { $evidence += "lint: $($line.Trim())" }
        }
    }
} else {
    $evidence += "Lint passed"
}

$metrics = @{
    lint_exit_code = $exitCode
    lint_errors = 0
}

if ($exitCode -eq 0) {
    Write-Result "pass" $evidence $metrics
} else {
    Write-Result "fail" $evidence $metrics
}
