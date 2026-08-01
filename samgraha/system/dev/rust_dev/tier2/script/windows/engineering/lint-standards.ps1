[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)] [string] $RepoRoot,
    [Parameter(Mandatory=$true)] [string] $RepoFingerprint,
    [Parameter(Mandatory=$true)] [string] $Out,
    [string] $LintCommand = "cargo clippy --all-targets --all-features -- -D warnings"
)

$executedAt = [DateTime]::UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ")

function Write-Result($status, $evidence, $metrics) {
    $result = [ordered]@{
        repo_fingerprint = $RepoFingerprint
        check = "lint-standards"
        domain = "07-engineering"
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

$lintConfigs = @(".eslintrc", ".eslintrc.js", ".eslintrc.json", ".eslintrc.yml", ".pylintrc", ".flake8", "pyproject.toml", ".golangci.yml", ".rubocop.yml", ".stylelintrc", "clippy.toml", ".clippy.toml")
$configFound = @()
foreach ($cfg in $lintConfigs) {
    $path = Join-Path $RepoRoot $cfg
    if (Test-Path $path) { $configFound += $cfg }
}

if ($configFound.Count -eq 0) {
    $evidence = @()
    $evidence += "No lint config found (checked: $($lintConfigs -join ', '))"
    $evidence += "Attempting lint command: $LintCommand"
}

$lintExitCode = -1
$lintErrors = 0
$lintOutput = ""

try {
    $process = Start-Process -FilePath "cmd.exe" -ArgumentList "/c", "cd /d `"$RepoRoot`" && $LintCommand" -NoNewWindow -Wait -PassThru -RedirectStandardOutput "$env:TEMP\lint_stdout.txt" -RedirectStandardError "$env:TEMP\lint_stderr.txt" -ErrorAction Stop
    $lintExitCode = $process.ExitCode
} catch {
    Write-Result "error" @("Lint command failed to execute: $_") @{ lint_exit_code = -1; lint_errors = 0 }
}

$stdout = if (Test-Path "$env:TEMP\lint_stdout.txt") { Get-Content "$env:TEMP\lint_stdout.txt" -Raw } else { "" }
$stderr = if (Test-Path "$env:TEMP\lint_stderr.txt") { Get-Content "$env:TEMP\lint_stderr.txt" -Raw } else { "" }
$lintOutput = "$stdout $stderr"

$errorPatterns = @("error", "Error", "ERROR", "problems", "Problems")
foreach ($ep in $errorPatterns) {
    $errorMatches = [regex]::Matches($lintOutput, "(?m)^.*$ep.*$")
    $lintErrors += $errorMatches.Count
}

$evidence = @()
if ($configFound.Count -gt 0) {
    $evidence += "Lint configs found: $($configFound -join ', ')"
}
if ($lintExitCode -eq 0) {
    $evidence += "Lint passed"
} else {
    $evidence += "Lint exited with code $lintExitCode"
    if ($stderr.Length -gt 0) {
        $lines = $stderr -split "`n" | Select-Object -Last 10
        foreach ($line in $lines) {
            if ($line.Trim().Length -gt 0) { $evidence += "stderr: $($line.Trim())" }
        }
    }
}

$metrics = @{
    lint_exit_code = $lintExitCode
    lint_errors = $lintErrors
}

if ($lintExitCode -eq 0) {
    Write-Result "pass" $evidence $metrics
} else {
    Write-Result "fail" $evidence $metrics
}
