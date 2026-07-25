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
        check = "design-tokens-in-implementation"
        domain = "06-design"
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
    Write-Result "error" @("Cannot access docs-root: $DocsRoot") @{ tokens_declared = 0; tokens_found = 0; tokens_missing = 0 }
}

if (-not (Test-Path -LiteralPath $RepoRoot -PathType Container)) {
    Write-Result "error" @("Cannot access repo-root: $RepoRoot") @{ tokens_declared = 0; tokens_found = 0; tokens_missing = 0 }
}

$designFiles = Get-ChildItem -Path $DocsRoot -Filter "*.md" -File -Recurse -ErrorAction SilentlyContinue |
    Where-Object { $_.Name -match "^(06-)?design" }

if (-not $designFiles -or $designFiles.Count -eq 0) {
    Write-Result "not_applicable" @("No design documents found in docs-root") @{ tokens_declared = 0; tokens_found = 0; tokens_missing = 0 }
}

$allContent = ""
foreach ($df in $designFiles) {
    $allContent += (Get-Content -Path $df.FullName -Raw -ErrorAction SilentlyContinue) + "`n"
}

$hexColors = [regex]::Matches($allContent, '#[0-9a-fA-F]{3,8}\b') | ForEach-Object { $_.Value } | Sort-Object -Unique
$pixelValues = [regex]::Matches($allContent, '\b\d+(\.\d+)?px\b') | ForEach-Object { $_.Value } | Sort-Object -Unique
$remValues = [regex]::Matches($allContent, '\b\d+(\.\d+)?rem\b') | ForEach-Object { $_.Value } | Sort-Object -Unique
$fontFamilies = [regex]::Matches($allContent, 'font-family\s*:\s*([^;]+)') | ForEach-Object { $_.Groups[1].Value.Trim() } | Sort-Object -Unique

$declaredTokens = @()
$declaredTokens += $hexColors
$declaredTokens += $pixelValues
$declaredTokens += $remValues
$declaredTokens += $fontFamilies

$declaredTokens = $declaredTokens | Where-Object { $_ -and $_.Length -gt 0 } | Sort-Object -Unique

if ($declaredTokens.Count -eq 0) {
    Write-Result "not_applicable" @("No design tokens found in design documents") @{ tokens_declared = 0; tokens_found = 0; tokens_missing = 0 }
}

$srcDir = Join-Path $RepoRoot "src"
$styleExtensions = @("*.css", "*.scss", "*.less", "*.styled.*", "*.styles.*")

$allStyleContent = ""
if (Test-Path -LiteralPath $srcDir -PathType Container) {
    foreach ($ext in $styleExtensions) {
        $styleFiles = Get-ChildItem -Path $srcDir -Filter $ext -File -Recurse -ErrorAction SilentlyContinue
        foreach ($sf in $styleFiles) {
            $allStyleContent += (Get-Content -Path $sf.FullName -Raw -ErrorAction SilentlyContinue) + "`n"
        }
    }
    $jsTsFiles = Get-ChildItem -Path $srcDir -Include "*.ts", "*.tsx", "*.js", "*.jsx" -File -Recurse -ErrorAction SilentlyContinue
    foreach ($jf in $jsTsFiles) {
        $content = Get-Content -Path $jf.FullName -Raw -ErrorAction SilentlyContinue
        if ($content -match '(styled|css|style)') {
            $allStyleContent += $content + "`n"
        }
    }
}

$tokensFound = 0
$tokensMissing = 0
$missingList = @()

foreach ($token in $declaredTokens) {
    $escapedToken = [regex]::Escape($token)
    if ($allStyleContent -match $escapedToken) {
        $tokensFound++
    } else {
        $tokensMissing++
        $missingList += $token
    }
}

$evidence = @()
$evidence += "Scanned $($designFiles.Count) design document(s), found $($declaredTokens.Count) declared token(s)"
$evidence += "Checked style files in src/, found $tokensFound of $tokensDeclared tokens in code"

foreach ($m in ($missingList | Select-Object -First 10)) {
    $evidence += "Missing token: $m"
}
if ($tokensMissing -gt 10) {
    $evidence += "... and $($tokensMissing - 10) more missing tokens"
}

$metrics = @{
    tokens_declared = $declaredTokens.Count
    tokens_found = $tokensFound
    tokens_missing = $tokensMissing
}

if ($tokensMissing -eq 0) {
    Write-Result "pass" $evidence $metrics
} else {
    Write-Result "fail" $evidence $metrics
}
