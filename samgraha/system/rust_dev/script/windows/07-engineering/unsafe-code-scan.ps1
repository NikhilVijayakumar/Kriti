[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)] [string] $RepoRoot,
    [Parameter(Mandatory=$true)] [string] $RepoFingerprint,
    [Parameter(Mandatory=$true)] [string] $Out
)

$executedAt = [DateTime]::UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ")

function Write-Result($status, $evidence, $metrics) {
    $result = [ordered]@{
        check = "unsafe-code-scan"
        domain = "07-engineering"
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
    Write-Result "error" @("Cannot access repo-root: $RepoRoot") @{ unsafe_blocks_found = 0; crates_without_forbid = 0 }
}

$srcDir = Join-Path $RepoRoot "src"
if (-not (Test-Path -LiteralPath $srcDir -PathType Container)) {
    Write-Result "not_applicable" @("No src/ directory found") @{ unsafe_blocks_found = 0; crates_without_forbid = 0 }
}

# Count unsafe blocks
$unsafeCount = 0
$unsafeFiles = @()
$codeFiles = Get-ChildItem -Path $srcDir -Include "*.rs" -File -Recurse -ErrorAction SilentlyContinue
foreach ($f in $codeFiles) {
    $content = Get-Content $f.FullName -Raw -ErrorAction SilentlyContinue
    if ($content -match 'unsafe\s*\{') {
        $matches = [regex]::Matches($content, 'unsafe\s*\{')
        $unsafeCount += $matches.Count
        $unsafeFiles += $f.FullName.Replace($RepoRoot + [IO.Path]::DirectorySeparatorChar, "")
    }
}

# Check crate roots for #![forbid(unsafe_code)]
$cratesWithoutForbid = 0
$crateRootList = @()
$crateRoots = Get-ChildItem -Path $RepoRoot -Include "lib.rs","main.rs" -File -Recurse -ErrorAction SilentlyContinue
foreach ($cr in $crateRoots) {
    $content = Get-Content $cr.FullName -Raw -ErrorAction SilentlyContinue
    if ($content -notmatch '#!\[forbid\(unsafe_code\)\]|#!\[deny\(unsafe_code\)\]') {
        $cratesWithoutForbid++
        $crateRootList += $cr.FullName.Replace($RepoRoot + [IO.Path]::DirectorySeparatorChar, "")
    }
}

$crateRootStr = $crateRootList -join ", "

if ($unsafeCount -gt 0 -and $cratesWithoutForbid -gt 0) {
    Write-Result "fail" @("Found $unsafeCount unsafe blocks; $cratesWithoutForbid crate(s) missing forbid(unsafe_code): $crateRootStr") @{ unsafe_blocks_found = $unsafeCount; crates_without_forbid = $cratesWithoutForbid }
} elseif ($unsafeCount -gt 0) {
    Write-Result "pass" @("Found $unsafeCount unsafe blocks but all crate roots have forbid(unsafe_code)") @{ unsafe_blocks_found = $unsafeCount; crates_without_forbid = 0 }
} else {
    Write-Result "pass" @("No unsafe blocks found in source code") @{ unsafe_blocks_found = 0; crates_without_forbid = 0 }
}
