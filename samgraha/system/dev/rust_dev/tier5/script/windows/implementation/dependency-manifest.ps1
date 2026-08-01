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
        check = "dependency-manifest"
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
    Write-Result "error" @("Cannot access repo-root: $RepoRoot") @{ manifest_exists = $false; dependency_count = 0 }
}

$manifestFiles = @(
    @{ Name = "package.json"; Type = "npm" },
    @{ Name = "requirements.txt"; Type = "pip" },
    @{ Name = "Pipfile"; Type = "pipenv" },
    @{ Name = "pyproject.toml"; Type = "python" },
    @{ Name = "go.mod"; Type = "go" },
    @{ Name = "Cargo.toml"; Type = "cargo" },
    @{ Name = "pom.xml"; Type = "maven" },
    @{ Name = "build.gradle"; Type = "gradle" },
    @{ Name = "Gemfile"; Type = "bundler" },
    @{ Name = "composer.json"; Type = "composer" }
)

$found = $null
foreach ($mf in $manifestFiles) {
    $path = Join-Path $RepoRoot $mf.Name
    if (Test-Path $path) {
        $found = $mf
        break
    }
}

if ($null -eq $found) {
    Write-Result "not_applicable" @("No dependency manifest found (checked: $($manifestFiles.Name -join ', '))") @{ manifest_exists = $false; dependency_count = 0 }
}

$manifestPath = Join-Path $RepoRoot $found.Name
$depCount = 0
$evidence = @()

try {
    switch ($found.Type) {
        "npm" {
            $pkg = Get-Content $manifestPath -Raw | ConvertFrom-Json
            $depCount = 0
            if ($pkg.dependencies) { $depCount += $pkg.dependencies.PSObject.Properties.Count }
            if ($pkg.devDependencies) { $depCount += $pkg.devDependencies.PSObject.Properties.Count }
            $evidence += "Found package.json with $depCount dependencies"
        }
        "pip" {
            $content = Get-Content $manifestPath -Raw
            $lines = ($content -split "`n") | Where-Object { $_ -match "^[a-zA-Z]" -and $_ -notmatch "^#" }
            $depCount = $lines.Count
            $evidence += "Found requirements.txt with $depCount dependencies"
        }
        "go" {
            $content = Get-Content $manifestPath -Raw
            $lines = ($content -split "`n") | Where-Object { $_ -match "^\t" -and $_ -notmatch "require" }
            $depCount = $lines.Count
            $evidence += "Found go.mod with $depCount dependencies"
        }
        "cargo" {
            $content = Get-Content $manifestPath -Raw
            $lines = $content -split "`n"
            $inDeps = $false
            $depCount = 0
            foreach ($line in $lines) {
                if ($line -match "^\[([a-zA-Z_-]+)\]") {
                    $section = $Matches[1]
                    $inDeps = ($section -eq "dependencies" -or $section -eq "dev-dependencies" -or $section -eq "build-dependencies")
                } elseif ($inDeps -and $line -match "^[^#\[\s].*") {
                    $depCount++
                }
            }
            $evidence += "Found Cargo.toml with $depCount dependencies"
        }
        default {
            $evidence += "Found $($found.Name) (type: $($found.Type)) - dependency count not parsed"
        }
    }
} catch {
    $evidence += "Error parsing $($found.Name): $_"
}

$metrics = @{
    manifest_exists = $true
    dependency_count = $depCount
}

Write-Result "pass" $evidence $metrics
