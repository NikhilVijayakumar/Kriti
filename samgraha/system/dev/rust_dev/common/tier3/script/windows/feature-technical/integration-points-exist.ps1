[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)] [string] $RepoRoot,
    [Parameter(Mandatory=$true)] [string] $RepoFingerprint,
    [Parameter(Mandatory=$true)] [string] $Out,
    [Parameter(Mandatory=$true)] [string] $DocsRoot
)

$executedAt = [DateTime]::UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ")

function Write-Result($status, $evidence, $metrics) {
    $result = [ordered]@{
        repo_fingerprint = $RepoFingerprint
        check = "integration-points-exist"
        domain = "10-feature-technical"
        category = "B"
        status = $status
        metrics = $metrics
        evidence = $evidence
        executed_at = $executedAt
    }
    $result | ConvertTo-Json -Depth 10 | Set-Content -Path $Out -Encoding UTF8
    if ($status -eq "error") { exit 1 }
    exit 0
}

if (-not (Test-Path -LiteralPath $DocsRoot -PathType Container)) {
    Write-Result "error" @("Cannot access docs-root: $DocsRoot") @{ points_declared = 0; points_found = 0; points_missing = 0 }
}

if (-not (Test-Path -LiteralPath $RepoRoot -PathType Container)) {
    Write-Result "error" @("Cannot access repo-root: $RepoRoot") @{ points_declared = 0; points_found = 0; points_missing = 0 }
}

$featureFiles = Get-ChildItem -Path $DocsRoot -Filter "*.md" -File -Recurse -ErrorAction SilentlyContinue |
    Where-Object { $_.Name -match "^(10-)?feature-technical" }

if (-not $featureFiles -or $featureFiles.Count -eq 0) {
    Write-Result "not_applicable" @("No feature-technical documents found in docs-root") @{ points_declared = 0; points_found = 0; points_missing = 0 }
}

$allContent = ""
foreach ($ff in $featureFiles) {
    $allContent += (Get-Content -Path $ff.FullName -Raw -ErrorAction SilentlyContinue) + "`n"
}

$importPatterns = @(
    '(?i)import\s+(?:\{[^}]+\}|\w+)\s+from\s+["\x27]([^"\x27]+)["\x27]',
    '(?i)require\s*\(\s*["\x27]([^"\x27]+)["\x27]',
    '(?i)from\s+([a-zA-Z][\w./-]+)',
    '(?i)(?:connects?\s+to|api\s+endpoint|database\s+connection)\s*[:=]\s*["\x27]?([a-zA-Z][\w./-]+)',
    '(?i)(?:function|class|module)\s+([A-Z]\w+)'
)

$declaredPoints = @()

# Extract identifiers from code blocks in the markdown
$codeBlocks = [regex]::Matches($allContent, '```[\s\S]*?```')
foreach ($block in $codeBlocks) {
    $codeText = $block.Value
    # Extract import sources
    $imports = [regex]::Matches($codeText, '(?i)import\s+(?:\{[^}]+\}|\w+)\s+from\s+["\x27]([^"\x27]+)["\x27]')
    foreach ($imp in $imports) {
        $declaredPoints += $imp.Groups[1].Value
    }
    # Extract require sources
    $requires = [regex]::Matches($codeText, '(?i)require\s*\(\s*["\x27]([^"\x27]+)["\x27]')
    foreach ($req in $requires) {
        $declaredPoints += $req.Groups[1].Value
    }
    # Extract function/class names
    $funcNames = [regex]::Matches($codeText, '(?i)(?:function|class)\s+([A-Z]\w+)')
    foreach ($fn in $funcNames) {
        $declaredPoints += $fn.Groups[1].Value
    }
}

# Also look for integration keywords in prose
$keywordMatches = [regex]::Matches($allContent, '(?i)(?:imports?|api|database|connects?\s+to)\s+[`\x27"]([a-zA-Z][\w./-]+)[`\x27"]')
foreach ($km in $keywordMatches) {
    $declaredPoints += $km.Groups[1].Value
}

$declaredPoints = $declaredPoints | Where-Object { $_ -and $_.Length -gt 1 -and $_ -notmatch '^\d' } | Sort-Object -Unique

if ($declaredPoints.Count -eq 0) {
    Write-Result "not_applicable" @("No integration points found in feature-technical documents") @{ points_declared = 0; points_found = 0; points_missing = 0 }
}

$srcDir = Join-Path $RepoRoot "src"
$srcContent = ""
if (Test-Path -LiteralPath $srcDir -PathType Container) {
    $codeFiles = Get-ChildItem -Path $srcDir -Include "*.rs", "*.ts", "*.tsx", "*.js", "*.jsx", "*.py", "*.go", "*.java", "*.cs" -File -Recurse -ErrorAction SilentlyContinue
    foreach ($cf in $codeFiles) {
        $srcContent += (Get-Content -Path $cf.FullName -Raw -ErrorAction SilentlyContinue) + "`n"
    }
}

$pointsFound = 0
$pointsMissing = 0
$missingList = @()

foreach ($point in $declaredPoints) {
    # Try matching as import/require source or as an identifier
    $escapedPoint = [regex]::Escape($point)
    $shortName = Split-Path $point -Leaf
    $escapedShort = [regex]::Escape($shortName)

    if ($srcContent -match $escapedPoint -or $srcContent -match $escapedShort) {
        $pointsFound++
    } else {
        $pointsMissing++
        $missingList += $point
    }
}

$evidence = @()
$evidence += "Scanned $($featureFiles.Count) feature-technical document(s), found $($declaredPoints.Count) declared integration point(s)"
$evidence += "Checked code in src/, found $pointsFound of $($declaredPoints.Count) points"

foreach ($m in ($missingList | Select-Object -First 10)) {
    $evidence += "Missing integration point: $m"
}
if ($pointsMissing -gt 10) {
    $evidence += "... and $($pointsMissing - 10) more missing integration points"
}

$metrics = @{
    points_declared = $declaredPoints.Count
    points_found = $pointsFound
    points_missing = $pointsMissing
}

if ($pointsMissing -eq 0) {
    Write-Result "pass" $evidence $metrics
} else {
    Write-Result "fail" $evidence $metrics
}
