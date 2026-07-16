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
        check = "mitigation-present-at-boundary"
        domain = "03-security"
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
    Write-Result "error" @("Cannot access docs-root: $DocsRoot") @{ mitigations_declared = 0; mitigations_found = 0; mitigations_missing = 0 }
}

if (-not (Test-Path -LiteralPath $RepoRoot -PathType Container)) {
    Write-Result "error" @("Cannot access repo-root: $RepoRoot") @{ mitigations_declared = 0; mitigations_found = 0; mitigations_missing = 0 }
}

$securityFiles = Get-ChildItem -Path $DocsRoot -Filter "*.md" -File -Recurse -ErrorAction SilentlyContinue |
    Where-Object { $_.Name -match "^(03-)?security" }

if (-not $securityFiles -or $securityFiles.Count -eq 0) {
    Write-Result "not_applicable" @("No security documents found in docs-root") @{ mitigations_declared = 0; mitigations_found = 0; mitigations_missing = 0 }
}

$allContent = ""
foreach ($sf in $securityFiles) {
    $allContent += (Get-Content -Path $sf.FullName -Raw -ErrorAction SilentlyContinue) + "`n"
}

$mitigationPatterns = @(
    @{ Pattern = '(?i)sanitiz'; Name = 'input sanitization' },
    @{ Pattern = '(?i)escap'; Name = 'output escaping' },
    @{ Pattern = '(?i)validat'; Name = 'input validation' },
    @{ Pattern = '(?i)authenticat'; Name = 'authentication' },
    @{ Pattern = '(?i)authoriz'; Name = 'authorization' },
    @{ Pattern = '(?i)encrypt'; Name = 'encryption' },
    @{ Pattern = '(?i)\bhash'; Name = 'hashing' },
    @{ Pattern = '(?i)rate.?limit'; Name = 'rate limiting' },
    @{ Pattern = '(?i)\bCSRF'; Name = 'CSRF protection' },
    @{ Pattern = '(?i)\bXSS'; Name = 'XSS protection' }
)

$declaredMitigations = @()

foreach ($mp in $mitigationPatterns) {
    $matches = [regex]::Matches($allContent, $mp.Pattern)
    if ($matches.Count -gt 0) {
        $declaredMitigations += $mp.Name
    }
}

$declaredMitigations = $declaredMitigations | Sort-Object -Unique

if ($declaredMitigations.Count -eq 0) {
    Write-Result "not_applicable" @("No security mitigations found in security documents") @{ mitigations_declared = 0; mitigations_found = 0; mitigations_missing = 0 }
}

$srcDir = Join-Path $RepoRoot "src"
$srcContent = ""
if (Test-Path -LiteralPath $srcDir -PathType Container) {
    $codeFiles = Get-ChildItem -Path $srcDir -Include "*.rs", "*.ts", "*.tsx", "*.js", "*.jsx", "*.py", "*.go", "*.java", "*.cs" -File -Recurse -ErrorAction SilentlyContinue
    foreach ($cf in $codeFiles) {
        $srcContent += (Get-Content -Path $cf.FullName -Raw -ErrorAction SilentlyContinue) + "`n"
    }
}

$foundCount = 0
$missingCount = 0
$missingList = @()

foreach ($mitigation in $declaredMitigations) {
    $codePatterns = switch ($mitigation) {
        'input sanitization'    { @('(?i)sanitiz') }
        'output escaping'       { @('(?i)escap') }
        'input validation'      { @('(?i)validat') }
        'authentication'        { @('(?i)authenticat') }
        'authorization'         { @('(?i)authoriz') }
        'encryption'            { @('(?i)encrypt') }
        'hashing'               { @('(?i)\bhash') }
        'rate limiting'         { @('(?i)rate.?limit') }
        'CSRF protection'       { @('(?i)csrf', '(?i)xsrf', '(?i)cross.site.request') }
        'XSS protection'        { @('(?i)\bxss', '(?i)cross.site.script') }
    }

    $found = $false
    foreach ($cp in $codePatterns) {
        if ($srcContent -match $cp) {
            $found = $true
            break
        }
    }

    if ($found) {
        $foundCount++
    } else {
        $missingCount++
        $missingList += $mitigation
    }
}

$evidence = @()
$evidence += "Scanned $($securityFiles.Count) security document(s), found $($declaredMitigations.Count) declared mitigation type(s)"
$evidence += "Checked code in src/, found $foundCount of $($declaredMitigations.Count) mitigations"

foreach ($m in $missingList) {
    $evidence += "Missing mitigation: $m"
}

$metrics = @{
    mitigations_declared = $declaredMitigations.Count
    mitigations_found = $foundCount
    mitigations_missing = $missingCount
}

if ($missingCount -eq 0) {
    Write-Result "pass" $evidence $metrics
} else {
    Write-Result "fail" $evidence $metrics
}
