[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)] [string] $RepoRoot,
    [Parameter(Mandatory=$true)] [string] $RepoFingerprint,
    [Parameter(Mandatory=$true)] [string] $Out,
    [string] $ScanInclude = "*.rs;*.ts;*.js;*.py;*.go;*.java;*.cs;*.env;*.yml;*.yaml;*.json;*.toml;*.xml;*.config;*.cfg;*.ini;*.properties"
)

$executedAt = [DateTime]::UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ")

function Write-Result($status, $evidence, $metrics) {
    $result = [ordered]@{
        repo_fingerprint = $RepoFingerprint
        check = "secret-scan"
        domain = "03-security"
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
    Write-Result "error" @("Cannot access repo-root: $RepoRoot") @{ secrets_found = 0; files_scanned = 0 }
}

$patterns = @(
    @{ Name = "AWS Key"; Regex = "AKIA[0-9A-Z]{16}" },
    @{ Name = "Private Key"; Regex = "-----BEGIN.*PRIVATE KEY-----" },
    @{ Name = "Password Assignment"; Regex = "(?i)password\s*[:=]\s*[`"'][^`"']+[`"']" },
    @{ Name = "API Key Assignment"; Regex = "(?i)api[_-]?key\s*[:=]\s*[`"'][^`"']+[`"']" },
    @{ Name = "Token Assignment"; Regex = "(?i)token\s*[:=]\s*[`"'][^`"']+[`"']" },
    @{ Name = "Secret Assignment"; Regex = "(?i)secret\s*[:=]\s*[`"'][^`"']+[`"']" }
)

$includePatterns = $ScanInclude -split ";" | ForEach-Object { $_.Trim() }
$excludeDirs = @("node_modules", ".git", "__pycache__", ".venv", "dist", "build", ".opencode", "vendor")

$filesScanned = 0
$secretsFound = 0
$findings = @()

try {
    foreach ($pattern in $includePatterns) {
        $files = Get-ChildItem -Path $RepoRoot -Recurse -Filter $pattern -File -ErrorAction SilentlyContinue |
            Where-Object {
                $excluded = $false
                foreach ($dir in $excludeDirs) {
                    if ($_.FullName -match [regex]::Escape("\$dir\")) { $excluded = $true; break }
                }
                -not $excluded
            }
        foreach ($file in $files) {
            $filesScanned++
            $content = Get-Content $file.FullName -Raw -ErrorAction SilentlyContinue
            if ([string]::IsNullOrEmpty($content)) { continue }
            foreach ($pat in $patterns) {
                $matches = [regex]::Matches($content, $pat.Regex)
                if ($matches.Count -gt 0) {
                    $relPath = $file.FullName.Substring($RepoRoot.Length).TrimStart('\', '/')
                    $findings += "$($pat.Name) in $relPath"
                    $secretsFound += $matches.Count
                }
            }
        }
    }
} catch {
    Write-Result "error" @("Error scanning files: $_") @{ secrets_found = 0; files_scanned = $filesScanned }
}

$evidence = @()
if ($secretsFound -eq 0) {
    $evidence += "No secrets found in $filesScanned files"
} else {
    $evidence += "Found $secretsFound potential secrets in $filesScanned files"
    foreach ($f in ($findings | Select-Object -First 20)) {
        $evidence += "  $f"
    }
}

$metrics = @{
    secrets_found = $secretsFound
    files_scanned = $filesScanned
}

if ($secretsFound -eq 0) {
    Write-Result "pass" $evidence $metrics
} else {
    Write-Result "fail" $evidence $metrics
}
