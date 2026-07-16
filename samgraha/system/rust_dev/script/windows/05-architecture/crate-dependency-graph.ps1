[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)] [string] $RepoRoot,
    [Parameter(Mandatory=$true)] [string] $RepoFingerprint,
    [Parameter(Mandatory=$true)] [string] $Out
)

$executedAt = [DateTime]::UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ")

function Write-Result($status, $evidence, $metrics) {
    $result = [ordered]@{
        check = "crate-dependency-graph"
        domain = "05-architecture"
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
    Write-Result "error" @("Cannot access repo-root: $RepoRoot") @{ has_cycles = $false; violation_count = 0 }
}

$cargoToml = Join-Path $RepoRoot "Cargo.toml"
if (-not (Test-Path $cargoToml)) {
    Write-Result "not_applicable" @("No Cargo.toml found — not a Rust workspace") @{ has_cycles = $false; violation_count = 0 }
}

if (-not (Get-Command "cargo" -ErrorAction SilentlyContinue)) {
    Write-Result "error" @("cargo not installed") @{ has_cycles = $false; violation_count = 0 }
}

$tmpFile = [System.IO.Path]::GetTempFileName()
try {
    & cargo metadata --format-version 1 --no-deps 2>$null | Set-Content -Path $tmpFile -Encoding UTF8
    if ($LASTEXITCODE -ne 0) {
        Write-Result "error" @("cargo metadata failed — ensure Cargo.toml is valid") @{ has_cycles = $false; violation_count = 0 }
    }

    $data = Get-Content $tmpFile -Raw | ConvertFrom-Json
    $packages = @{}
    foreach ($p in $data.packages) { $packages[$p.name] = $p }
    $workspaceMembers = @($data.workspace_members)

    # Build adjacency list for workspace crates
    $graph = @{}
    foreach ($kv in $packages.GetEnumerator()) {
        $pkgName = $kv.Key
        $pkg = $kv.Value
        if ($workspaceMembers -notcontains $pkg.manifest_path) { continue }
        $deps = @()
        foreach ($dep in $pkg.dependencies) {
            if ($packages.ContainsKey($dep.name) -and $workspaceMembers -contains $packages[$dep.name].manifest_path) {
                $deps += $dep.name
            }
        }
        $graph[$pkgName] = $deps
    }

    # Simple cycle detection using DFS
    $hasCycles = $false
    $cycleDetails = @()
    $color = @{}
    foreach ($n in $graph.Keys) { $color[$n] = "WHITE" }

    function Invoke-DFS($node, [System.Collections.ArrayList]$path) {
        $color[$node] = "GRAY"
        [void]$path.Add($node)
        foreach ($neighbor in $graph[$node]) {
            if ($color.ContainsKey($neighbor)) {
                if ($color[$neighbor] -eq "GRAY") {
                    $script:hasCycles = $true
                    $idx = $path.IndexOf($neighbor)
                    $cycle = $path[$idx..($path.Count-1)] + $neighbor
                    $script:cycleDetails += ($cycle -join " -> ")
                } elseif ($color[$neighbor] -eq "WHITE") {
                    Invoke-DFS $neighbor $path
                }
            }
        }
        $path.RemoveAt($path.Count - 1)
        $color[$node] = "BLACK"
    }

    foreach ($node in $graph.Keys) {
        if ($color[$node] -eq "WHITE") {
            $path = [System.Collections.ArrayList]@()
            Invoke-DFS $node $path
        }
    }

    # Check direction violations
    $infraKeywords = @("infra", "util", "common", "shared", "internal")
    $infraCrates = @()
    foreach ($name in $graph.Keys) {
        if ($infraKeywords | Where-Object { $name.ToLower().Contains($_) }) {
            $infraCrates += $name
        }
    }

    $violations = @()
    foreach ($kv in $graph.GetEnumerator()) {
        $pkg = $kv.Key
        if ($infraCrates -contains $pkg) { continue }
        foreach ($dep in $kv.Value) {
            if ($infraCrates -contains $dep) {
                $violations += "$pkg -> $dep"
            }
        }
    }

    $violationStr = $violations -join ", "
    $cycleStr = $cycleDetails -join "; "

    if ($hasCycles) {
        Write-Result "fail" @("Circular dependency detected: $cycleStr. Total crates: $($graph.Count)") @{ has_cycles = $true; violation_count = $violations.Count }
    } elseif ($violations.Count -gt 0) {
        Write-Result "fail" @("Dependency direction violations: $violationStr") @{ has_cycles = $false; violation_count = $violations.Count }
    } else {
        Write-Result "pass" @("No circular dependencies. All crate dependencies flow correctly. Total crates: $($graph.Count)") @{ has_cycles = $false; violation_count = 0 }
    }
} catch {
    Write-Result "error" @("crate-dependency-graph analysis failed: $_") @{ has_cycles = $false; violation_count = 0 }
} finally {
    Remove-Item -Path $tmpFile -Force -ErrorAction SilentlyContinue
}
