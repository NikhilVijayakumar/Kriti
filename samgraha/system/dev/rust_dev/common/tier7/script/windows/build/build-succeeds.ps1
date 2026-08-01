[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)] [string] $RepoRoot,
    [Parameter(Mandatory=$true)] [string] $RepoFingerprint,
    [Parameter(Mandatory=$true)] [string] $Out,
    [string] $BuildCommand = "cargo build --release",
    [int] $TimeoutSeconds = 600
)

$executedAt = [DateTime]::UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ")

function Write-Result($status, $evidence, $metrics) {
    $result = [ordered]@{
        repo_fingerprint = $RepoFingerprint
        check = "build-succeeds"
        domain = "14-build"
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
    Write-Result "error" @("Cannot access repo-root: $RepoRoot") @{ build_exit_code = -1; build_duration_seconds = 0 }
}

$stopwatch = [System.Diagnostics.Stopwatch]::StartNew()
try {
    $process = Start-Process -FilePath "cmd.exe" -ArgumentList "/c", "cd /d `"$RepoRoot`" && $BuildCommand" -NoNewWindow -Wait -PassThru -RedirectStandardOutput "$env:TEMP\build_stdout.txt" -RedirectStandardError "$env:TEMP\build_stderr.txt" -ErrorAction Stop
    $exitCode = $process.ExitCode
} catch {
    $stopwatch.Stop()
    Write-Result "error" @("Build command failed to execute: $_") @{ build_exit_code = -1; build_duration_seconds = [math]::Round($stopwatch.Elapsed.TotalSeconds, 1) }
}
$stopwatch.Stop()
$duration = [math]::Round($stopwatch.Elapsed.TotalSeconds, 1)

$stdout = if (Test-Path "$env:TEMP\build_stdout.txt") { Get-Content "$env:TEMP\build_stdout.txt" -Raw } else { "" }
$stderr = if (Test-Path "$env:TEMP\build_stderr.txt") { Get-Content "$env:TEMP\build_stderr.txt" -Raw } else { "" }

$evidence = @()
if ($exitCode -ne 0) {
    $evidence += "Build command exited with code $exitCode"
    $evidence += "Command: $BuildCommand"
    if ($stderr.Length -gt 0) {
        $lines = $stderr -split "`n" | Select-Object -Last 10
        foreach ($line in $lines) {
            if ($line.Trim().Length -gt 0) { $evidence += "stderr: $($line.Trim())" }
        }
    }
} else {
    $evidence += "Build succeeded in ${duration}s"
}

$metrics = @{
    build_exit_code = $exitCode
    build_duration_seconds = $duration
}

if ($exitCode -eq 0) {
    Write-Result "pass" $evidence $metrics
} else {
    Write-Result "fail" $evidence $metrics
}
