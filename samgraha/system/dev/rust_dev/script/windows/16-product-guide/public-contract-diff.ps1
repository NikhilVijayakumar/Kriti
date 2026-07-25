[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)] [string] $RepoRoot,
    [Parameter(Mandatory=$true)] [string] $RepoFingerprint,
    [Parameter(Mandatory=$true)] [string] $Out,
    [string] $DocsRoot = ""
)

$executedAt = [DateTime]::UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ")

function Write-Result($status, $evidence, $metrics) {
    $result = [ordered]@{
        repo_fingerprint = $RepoFingerprint
        check = "public-contract-diff"
        domain = "16-product-guide"
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
    Write-Result "error" @("Cannot access repo-root: $RepoRoot") @{ declared_endpoints = 0; actual_endpoints = 0; mismatches = 0 }
}

if ([string]::IsNullOrEmpty($DocsRoot)) {
    $DocsRoot = Join-Path $RepoRoot "docs"
    if (-not (Test-Path $DocsRoot)) {
        $DocsRoot = $RepoRoot
    }
}

$declaredEndpoints = @()
$actualEndpoints = @()
$evidence = @()

$endpointPatterns = @(
    "(?:GET|POST|PUT|PATCH|DELETE|HEAD|OPTIONS)\s+(?:/[\w/{}\-\.]+)",
    "(?:get|post|put|patch|delete)\s*\(\s*['\""](/[\w/{}\-\.]+)",
    "(?:path|route|endpoint)\s*[:=]\s*['\""](/[\w/{}\-\.]+)"
)

try {
    $docFiles = Get-ChildItem -Path $DocsRoot -Recurse -Include "*.md","*.txt","*.rst","*.html","*.yaml","*.yml" -File -ErrorAction SilentlyContinue |
        Where-Object { $_.FullName -notmatch "(node_modules|\.git|__pycache__|\.venv)" }
    foreach ($file in $docFiles) {
        $content = Get-Content $file.FullName -Raw -ErrorAction SilentlyContinue
        if ([string]::IsNullOrEmpty($content)) { continue }
        foreach ($pattern in $endpointPatterns) {
            $matches = [regex]::Matches($content, $pattern)
            foreach ($m in $matches) {
                $ep = $m.Value.Trim()
                $declaredEndpoints += $ep
            }
        }
    }
} catch {
    $evidence += "Warning: Error scanning docs: $_"
}

$routePatterns = @(
    "(?:app|router|server)\.(?:get|post|put|patch|delete|use)\s*\(\s*['\""](/[\w/{}\-\.]+)",
    "(?:path|endpoint)\s*=\s*['\""](/[\w/{}\-\.]+)",
    "@(?:app|router)\.(?:get|post|put|patch|delete)\s*\(\s*['\""](/[\w/{}\-\.]+)",
    "(?:HandleFunc|Handle)\s*\(\s*['\""](/[\w/{}\-\.]+)",
    "#\[(?:get|post|put|patch|delete|head|options)\s*\(\s*['\""](/[\w/{}\-\.]+)['\""]\s*\)]",
    "\.route\s*\(\s*['\""](/[\w/{}\-\.]+)['\""]\s*,\s*(?:get|post|put|patch|delete)\s*\("
)

try {
    $codeFiles = Get-ChildItem -Path $RepoRoot -Recurse -Include "*.rs","*.ts","*.js","*.py","*.go","*.java","*.cs","*.rb" -File -ErrorAction SilentlyContinue |
        Where-Object { $_.FullName -notmatch "(node_modules|\.git|__pycache__|\.venv|dist|build|vendor|\.opencode)" }
    foreach ($file in $codeFiles) {
        $content = Get-Content $file.FullName -Raw -ErrorAction SilentlyContinue
        if ([string]::IsNullOrEmpty($content)) { continue }
        foreach ($pattern in $routePatterns) {
            $matches = [regex]::Matches($content, $pattern)
            foreach ($m in $matches) {
                $ep = $m.Value.Trim()
                $actualEndpoints += $ep
            }
        }
    }
} catch {
    $evidence += "Warning: Error scanning code: $_"
}

$uniqueDeclared = $declaredEndpoints | Sort-Object -Unique
$uniqueActual = $actualEndpoints | Sort-Object -Unique

$mismatches = 0
$mismatchDetails = @()
foreach ($dep in $uniqueDeclared) {
    $found = $false
    $depPath = if ($dep -match "(?:GET|POST|PUT|PATCH|DELETE|HEAD|OPTIONS)\s+(.+)") { $matches[1] } else { $dep }
    foreach ($act in $uniqueActual) {
        $actPath = if ($act -match "(?:get|post|put|patch|delete|use|Route|path)\s*\(?['\""]?(\/[\w\/{}\-\.]+)") { $matches[1] } else { $act }
        if ($depPath -eq $actPath -or $dep -eq $act) {
            $found = $true
            break
        }
    }
    if (-not $found) {
        $mismatches++
        $mismatchDetails += "Documented but not found in code: $dep"
    }
}

$evidence += "Declared endpoints: $($uniqueDeclared.Count), Actual endpoints: $($uniqueActual.Count), Mismatches: $mismatches"
foreach ($d in ($mismatchDetails | Select-Object -First 10)) {
    $evidence += "  $d"
}

$metrics = @{
    declared_endpoints = $uniqueDeclared.Count
    actual_endpoints = $uniqueActual.Count
    mismatches = $mismatches
}

if ($mismatches -eq 0) {
    Write-Result "pass" $evidence $metrics
} else {
    Write-Result "fail" $evidence $metrics
}
