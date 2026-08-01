[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)] [string] $RepoRoot,
    [Parameter(Mandatory=$true)] [string] $RepoFingerprint,
    [Parameter(Mandatory=$true)] [string] $Out,
    [string] $DocsRoot = ""
)

$executedAt = [DateTime]::UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ")

function Write-Result($status, $evidence, $metrics) {
    $result = [ordered]@{
        repo_fingerprint = $RepoFingerprint
        check = "dependency-reachable"
        domain = "08-external-context"
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
    Write-Result "error" @("Cannot access repo-root: $RepoRoot") @{ dependencies_checked = 0; dependencies_reachable = 0 }
}

if ([string]::IsNullOrEmpty($DocsRoot)) {
    $DocsRoot = Join-Path $RepoRoot "docs"
    if (-not (Test-Path $DocsRoot)) {
        $DocsRoot = $RepoRoot
    }
}

$urlPattern = "https?://[^\s`"'\)>\]]+"
$urls = @()
$checked = 0
$reachable = 0
$evidence = @()

try {
    $docFiles = Get-ChildItem -Path $DocsRoot -Recurse -Include "*.md","*.txt","*.rst","*.html","*.yaml","*.yml","*.json","*.toml" -File -ErrorAction SilentlyContinue |
        Where-Object { $_.FullName -notmatch "(node_modules|\.git|__pycache__|\.venv)" }
    foreach ($file in $docFiles) {
        $content = Get-Content $file.FullName -Raw -ErrorAction SilentlyContinue
        if ([string]::IsNullOrEmpty($content)) { continue }
        $matches = [regex]::Matches($content, $urlPattern)
        foreach ($m in $matches) {
            $url = $m.Value.TrimEnd('.', ',', ';', ':', ')')
            if ($url -match "^https?://") {
                $urls += $url
            }
        }
    }
} catch {
    Write-Result "error" @("Error scanning docs: $_") @{ dependencies_checked = 0; dependencies_reachable = 0 }
}

$uniqueUrls = $urls | Sort-Object -Unique
$unreachable = @()

foreach ($url in $uniqueUrls) {
    $checked++
    try {
        $request = [System.Net.WebRequest]::Create($url)
        $request.Method = "HEAD"
        $request.Timeout = 10000
        $request.AllowAutoRedirect = $true
        $response = $request.GetResponse()
        $statusCode = [int]$response.StatusCode
        $response.Close()
        if ($statusCode -ge 200 -and $statusCode -lt 400) {
            $reachable++
        } else {
            $unreachable += "$url (HTTP $statusCode)"
        }
    } catch {
        $unreachable += "$url (unreachable: $($_.Exception.Message))"
    }
}

if ($checked -eq 0) {
    Write-Result "not_applicable" @("No URLs found in docs under $DocsRoot") @{ dependencies_checked = 0; dependencies_reachable = 0 }
}

$evidence += "Checked $checked unique URLs, $reachable reachable"
foreach ($u in ($unreachable | Select-Object -First 10)) {
    $evidence += "  Unreachable: $u"
}

$metrics = @{
    dependencies_checked = $checked
    dependencies_reachable = $reachable
}

if ($unreachable.Count -eq 0) {
    Write-Result "pass" $evidence $metrics
} else {
    Write-Result "fail" $evidence $metrics
}
