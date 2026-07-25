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
        check = "module-boundary-diff"
        domain = "05-architecture"
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
    Write-Result "error" @("Cannot access repo-root: $RepoRoot") @{ declared_modules = 0; actual_modules = 0; boundary_violations = 0 }
}

$declaredModules = @()
$source = ""

$structureFile = Join-Path $RepoRoot "structure.yaml"
if (Test-Path $structureFile) {
    $source = "structure.yaml"
    $content = Get-Content $structureFile -Raw
    $lines = $content -split "`n"
    foreach ($line in $lines) {
        $trimmed = $line.Trim()
        if ($trimmed -match "^-?\s*(.+)/?$" -and $trimmed -notmatch "^#") {
            $mod = $matches[1].Trim()
            if ($mod.Length -gt 0) { $declaredModules += $mod }
        }
    }
} else {
    $pkgJson = Join-Path $RepoRoot "package.json"
    if (Test-Path $pkgJson) {
        $source = "package.json workspaces"
        try {
            $pkg = Get-Content $pkgJson -Raw | ConvertFrom-Json
            if ($pkg.workspaces) {
                foreach ($ws in $pkg.workspaces) {
                    $declaredModules += $ws
                }
            }
        } catch {
            Write-Result "error" @("Error parsing package.json: $_") @{ declared_modules = 0; actual_modules = 0; boundary_violations = 0 }
        }
    }
}

if ($declaredModules.Count -eq 0) {
    Write-Result "not_applicable" @("No module declarations found (no structure.yaml or package.json workspaces)") @{ declared_modules = 0; actual_modules = 0; boundary_violations = 0 }
}

$actualModules = @()
$excludeDirs = @("node_modules", ".git", "__pycache__", ".venv", "dist", "build", ".opencode", "vendor")
try {
    Get-ChildItem -Path $RepoRoot -Directory -ErrorAction Stop | ForEach-Object {
        $excluded = $false
        foreach ($dir in $excludeDirs) {
            if ($_.Name -eq $dir) { $excluded = $true; break }
        }
        if (-not $excluded) { $actualModules += $_.Name }
    }
} catch {
    Write-Result "error" @("Error scanning directories: $_") @{ declared_modules = $declaredModules.Count; actual_modules = 0; boundary_violations = 0 }
}

$violations = 0
$violationDetails = @()

$excludeDirs = @("node_modules", ".git", "__pycache__", ".venv", "dist", "build", ".opencode", "vendor")
foreach ($mod in $declaredModules) {
    $modDir = Join-Path $RepoRoot $mod
    if (-not (Test-Path $modDir)) { continue }
    try {
        $importFiles = Get-ChildItem -Path $modDir -Recurse -Include "*.ts","*.js","*.py","*.go","*.java","*.cs" -File -ErrorAction SilentlyContinue |
            Where-Object {
                $excluded = $false
                foreach ($dir in $excludeDirs) {
                    if ($_.FullName -match [regex]::Escape("\$dir\")) { $excluded = $true; break }
                }
                -not $excluded
            }
        foreach ($file in $importFiles) {
            $content = Get-Content $file.FullName -Raw -ErrorAction SilentlyContinue
            if ([string]::IsNullOrEmpty($content)) { continue }
            foreach ($otherMod in $declaredModules) {
                if ($otherMod -eq $mod) { continue }
                if ($content -match "(?:require|import|from)\s*.*['\""]$otherMod") {
                    $relPath = $file.FullName.Substring($RepoRoot.Length).TrimStart('\', '/')
                    $violationDetails += "$relPath imports from $otherMod (boundary violation)"
                    $violations++
                }
            }
        }
    } catch { }
}

$evidence = @()
$evidence += "Declared modules: $($declaredModules.Count) (source: $source), Actual top-level dirs: $($actualModules.Count)"
if ($violations -gt 0) {
    $evidence += "Found $violations boundary violation(s)"
    foreach ($v in ($violationDetails | Select-Object -First 10)) {
        $evidence += "  $v"
    }
} else {
    $evidence += "No boundary violations detected"
}

$metrics = @{
    declared_modules = $declaredModules.Count
    actual_modules = $actualModules.Count
    boundary_violations = $violations
}

if ($violations -eq 0) {
    Write-Result "pass" $evidence $metrics
} else {
    Write-Result "fail" $evidence $metrics
}
