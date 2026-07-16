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
        check = "mock-api-runs"
        domain = "11-prototype"
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
    Write-Result "error" @("Cannot access repo-root: $RepoRoot") @{ server_started = $false; endpoints_tested = 0; endpoints_passed = 0 }
}

$mockConfigs = @(
    "mock-server.js",
    "mockapi.config.js",
    "mock-server.ts",
    "mock-server.py",
    "mock_routes.json",
    "msw handlers.js"
)

$configFile = $null
foreach ($cfg in $mockConfigs) {
    $path = Join-Path $RepoRoot $cfg
    if (Test-Path $path) { $configFile = $cfg; break }
}

if ($null -eq $configFile) {
    $found = Get-ChildItem -Path $RepoRoot -Recurse -File -ErrorAction SilentlyContinue |
        Where-Object { $_.Name -match "mock.*(server|api|route)" -and $_.FullName -notmatch "(node_modules|\.git|__pycache__)" } |
        Select-Object -First 1
    if ($null -ne $found) {
        $configFile = $found.Name
    }
}

if ($null -eq $configFile) {
    Write-Result "not_applicable" @("No mock server config found (checked: $($mockConfigs -join ', '))") @{ server_started = $false; endpoints_tested = 0; endpoints_passed = 0 }
}

$serverStarted = $false
$endpointsTested = 0
$endpointsPassed = 0
$testPort = 3099
$evidence = @()

try {
    $process = Start-Process -FilePath "cmd.exe" -ArgumentList "/c", "cd /d `"$RepoRoot`" && node $configFile" -NoNewWindow -PassThru -RedirectStandardOutput "$env:TEMP\mock_stdout.txt" -RedirectStandardError "$env:TEMP\mock_stderr.txt" -ErrorAction Stop
    Start-Sleep -Seconds 3

    $processHasExited = $process.HasExited
    if ($processHasExited) {
        $evidence += "Mock server exited immediately (exit code: $($process.ExitCode))"
        $stderr = if (Test-Path "$env:TEMP\mock_stderr.txt") { Get-Content "$env:TEMP\mock_stderr.txt" -Raw } else { "" }
        if ($stderr.Length -gt 0) {
            $lines = $stderr -split "`n" | Select-Object -Last 5
            foreach ($line in $lines) {
                if ($line.Trim().Length -gt 0) { $evidence += "stderr: $($line.Trim())" }
            }
        }
        Write-Result "fail" $evidence @{ server_started = $false; endpoints_tested = 0; endpoints_passed = 0 }
    }

    $serverStarted = $true
    $evidence += "Mock server started on port $testPort using $configFile"

    try {
        $request = [System.Net.WebRequest]::Create("http://localhost:$testPort/")
        $request.Method = "GET"
        $request.Timeout = 5000
        $response = $request.GetResponse()
        $endpointsTested++
        $endpointsPassed++
        $response.Close()
    } catch {
        $endpointsTested++
        $evidence += "Root endpoint unreachable: $($_.Exception.Message)"
    }
} catch {
    $evidence += "Failed to start mock server: $_"
} finally {
    if ($null -ne $process -and -not $process.HasExited) {
        try { $process.Kill() } catch { }
    }
}

$metrics = @{
    server_started = $serverStarted
    endpoints_tested = $endpointsTested
    endpoints_passed = $endpointsPassed
}

if ($serverStarted -and $endpointsPassed -gt 0) {
    Write-Result "pass" $evidence $metrics
} elseif ($serverStarted) {
    Write-Result "fail" $evidence $metrics
} else {
    Write-Result "fail" $evidence $metrics
}
