[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)] [string] $RepoRoot,
    [Parameter(Mandatory=$true)] [string] $RepoFingerprint,
    [Parameter(Mandatory=$true)] [string] $Out,
    [string] $ArtifactPath = "target/release"
)

$executedAt = [DateTime]::UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ")

function Write-Result($status, $evidence, $metrics) {
    $result = [ordered]@{
        repo_fingerprint = $RepoFingerprint
        check = "artifact-exists"
        domain = "14-build"
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
    Write-Result "error" @("Cannot access repo-root: $RepoRoot") @{ artifact_path = $ArtifactPath; artifact_exists = $false }
}

$fullPath = Join-Path $RepoRoot $ArtifactPath
$exists = Test-Path $fullPath

$evidence = @()
$metrics = @{
    artifact_path = $ArtifactPath
    artifact_exists = $exists
}

if ($exists) {
    $evidence += "Artifact found at $ArtifactPath"
    $item = Get-Item $fullPath
    if ($item.PSIsContainer) {
        $files = (Get-ChildItem $fullPath -Recurse -File).Count
        $evidence += "Directory contains $files files"
    } else {
        $size = [math]::Round($item.Length / 1KB, 1)
        $evidence += "File size: ${size}KB"
    }
    Write-Result "pass" $evidence $metrics
} else {
    $evidence += "Artifact not found at $ArtifactPath"
    Write-Result "fail" $evidence $metrics
}
