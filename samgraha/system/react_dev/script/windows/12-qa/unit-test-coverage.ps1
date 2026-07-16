[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)] [string] $RepoRoot,
    [Parameter(Mandatory=$true)] [string] $RepoFingerprint,
    [Parameter(Mandatory=$true)] [string] $Out,
    [string] $SourceInclude = "*.ts;*.js;*.py;*.go;*.rs;*.java;*.cs",
    [string] $SourceExclude = "node_modules;vendor;__pycache__;dist;build;coverage;.next;.nuxt",
    [string] $TestInclude = "*.test.*;*.spec.*;*_test.*;test_*.py;tests_*.py",
    [int] $Threshold = 80
)

$executedAt = [DateTime]::UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ")

function Write-Result($status, $evidence, $metrics) {
    $result = [ordered]@{
        repo_fingerprint = $RepoFingerprint
        check = "unit-test-coverage"
        domain = "12-qa"
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

try {
    $repoDir = Get-Item -Path $RepoRoot -ErrorAction Stop
} catch {
    Write-Result "error" @("Cannot access repo-root: $RepoRoot") @{ source_files = 0; tested_files = 0; coverage_percent = 0 }
}

$sourcePatterns = $SourceInclude -split ";" | ForEach-Object { $_.Trim() }
$excludeDirs = $SourceExclude -split ";" | ForEach-Object { $_.Trim() }
$testPatterns = $TestInclude -split ";" | ForEach-Object { $_.Trim() }

function Test-ExcludedDir($path) {
    foreach ($dir in $excludeDirs) {
        if ($path -match [regex]::Escape("\$dir\") -or $path -match [regex]::Escape("/$dir/")) {
            return $true
        }
    }
    return $false
}

$allFiles = @()
try {
    $allFiles = Get-ChildItem -Path $RepoRoot -Recurse -File -ErrorAction Stop |
        Where-Object { -not (Test-ExcludedDir $_.FullName) }
} catch {
    Write-Result "error" @("Error scanning files: $_") @{ source_files = 0; tested_files = 0; coverage_percent = 0 }
}

$sourceFiles = @()
$testFiles = @()

foreach ($file in $allFiles) {
    $isSource = $false
    foreach ($pattern in $sourcePatterns) {
        if ($file.Name -like $pattern) { $isSource = $true; break }
    }

    $isTest = $false
    foreach ($pattern in $testPatterns) {
        if ($file.Name -like $pattern) { $isTest = $true; break }
    }

    if ($isTest) { $testFiles += $file }
    elseif ($isSource) { $sourceFiles += $file }
}

$sourceCount = $sourceFiles.Count
$testedCount = 0
$untestedFiles = @()

foreach ($src in $sourceFiles) {
    $srcBase = [System.IO.Path]::GetFileNameWithoutExtension($src.Name)
    $srcDir = $src.DirectoryName
    $hasTest = $false
    foreach ($test in $testFiles) {
        $testBase = $test.Name
        if ($test.DirectoryName -eq $srcDir -and $testBase -match [regex]::Escape($srcBase)) {
            $hasTest = $true
            break
        }
    }
    if ($hasTest) { $testedCount++ }
    else {
        $relPath = $src.FullName.Substring($RepoRoot.Length).TrimStart('\', '/')
        $untestedFiles += $relPath
    }
}

if ($sourceCount -eq 0) {
    Write-Result "not_applicable" @("No source files found matching patterns: $SourceInclude") @{ source_files = 0; tested_files = 0; coverage_percent = 0 }
}

$pct = [math]::Round(($testedCount / $sourceCount) * 100, 1)

$evidence = @()
if ($pct -lt $Threshold) {
    $evidence += "Coverage ${pct}% is below threshold ${Threshold}%"
    foreach ($f in ($untestedFiles | Select-Object -First 20)) {
        $evidence += "  No test: $f"
    }
    if ($untestedFiles.Count -gt 20) {
        $evidence += "  ... and $($untestedFiles.Count - 20) more untested files"
    }
}

$metrics = @{
    source_files = $sourceCount
    tested_files = $testedCount
    coverage_percent = $pct
}

if ($pct -ge $Threshold) {
    Write-Result "pass" $evidence $metrics
} else {
    Write-Result "fail" $evidence $metrics
}
