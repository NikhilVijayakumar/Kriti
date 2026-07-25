[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)] [string] $RepoRoot,
    [Parameter(Mandatory=$true)] [string] $RepoFingerprint,
    [Parameter(Mandatory=$true)] [string] $Out,
    [string] $ExpectedStructure = ""
)

$executedAt = [DateTime]::UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ")

function Write-Result($status, $evidence, $metrics) {
    $result = [ordered]@{
        repo_fingerprint = $RepoFingerprint
        check = "folder-structure"
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
    Write-Result "error" @("Cannot access repo-root: $RepoRoot") @{ expected_count = 0; actual_count = 0; mismatch_count = 0 }
}

if ([string]::IsNullOrEmpty($ExpectedStructure)) {
    $structureFile = Join-Path $RepoRoot "structure.yaml"
    if (Test-Path $structureFile) {
        $ExpectedStructure = Get-Content $structureFile -Raw
    } else {
        Write-Result "not_applicable" @("No expected structure provided (pass --expected-structure or create structure.yaml)") @{ expected_count = 0; actual_count = 0; mismatch_count = 0 }
    }
}

$expectedDirs = @()
$lines = $ExpectedStructure -split "`n"
foreach ($line in $lines) {
    $trimmed = $line.Trim()
    if ($trimmed -match "^-?\s*(.+)/?$" -and $trimmed -notmatch "^#") {
        $dir = $matches[1].Trim()
        if ($dir.Length -gt 0) { $expectedDirs += $dir }
    }
}

$actualDirs = @()
try {
    Get-ChildItem -Path $RepoRoot -Directory -Recurse -ErrorAction Stop | ForEach-Object {
        $rel = $_.FullName.Substring($RepoRoot.Length).TrimStart('\', '/')
        $actualDirs += $rel
    }
} catch {
    Write-Result "error" @("Error scanning directories: $_") @{ expected_count = $expectedDirs.Count; actual_count = 0; mismatch_count = 0 }
}

$mismatches = @()
$found = 0
foreach ($expected in $expectedDirs) {
    $normalized = $expected.Replace('/', '\')
    $found_match = $false
    foreach ($actual in $actualDirs) {
        if ($actual -eq $normalized -or $actual -like "*$normalized*") {
            $found_match = $true
            break
        }
    }
    if ($found_match) { $found++ }
    else { $mismatches += "Missing: $expected" }
}

$extra = @()
foreach ($actual in $actualDirs) {
    $isExpected = $false
    foreach ($expected in $expectedDirs) {
        $normalized = $expected.Replace('/', '\')
        if ($actual -eq $normalized -or $actual -like "*$normalized*") {
            $isExpected = $true
            break
        }
    }
    if (-not $isExpected -and $actual -notmatch "^(node_modules|\.git|__pycache__|\.venv|dist|build|\.opencode)") {
        $extra += "Unexpected: $actual"
    }
}

$evidence = @()
$evidence += "Expected: $($expectedDirs.Count) directories, Found: $($actualDirs.Count) directories, Matches: $found, Mismatches: $($mismatches.Count)"
foreach ($m in $mismatches | Select-Object -First 10) { $evidence += $m }
foreach ($e in $extra | Select-Object -First 5) { $evidence += $e }

$metrics = @{
    expected_count = $expectedDirs.Count
    actual_count = $actualDirs.Count
    mismatch_count = $mismatches.Count
}

if ($mismatches.Count -eq 0) {
    Write-Result "pass" $evidence $metrics
} else {
    Write-Result "fail" $evidence $metrics
}
