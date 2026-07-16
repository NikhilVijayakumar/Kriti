[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)] [string] $DocsRoot,
    [Parameter(Mandatory=$true)] [string] $RepoFingerprint,
    [Parameter(Mandatory=$true)] [string] $Out
)

# feature-family-mapping — Category C generic script
# Checks that every Feature has a corresponding Feature-Design and Feature-Technical,
# no orphaned Feature-Technical without a parent Feature, and IDs/names line up.

if (-not (Test-Path -LiteralPath $DocsRoot -PathType Container)) {
    $result = @{
        check = "feature-family-mapping"
        domain = "_generic"
        category = "C"
        status = "error"
        metrics = @{ features_count = 0; feature_designs_count = 0; feature_technicals_count = 0; valid_mappings = 0; orphans = 0 }
        evidence = @("docs-root not found: $DocsRoot")
        executed_at = (Get-Date -AsUTC).ToString("yyyy-MM-ddTHH:mm:ssZ")
        repo_fingerprint = $RepoFingerprint
    }
    $result | ConvertTo-Json -Depth 10 | Set-Content -Path $Out -Encoding UTF8
    exit 1
}

$executedAt = [DateTime]::UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ")

# Collect feature families by extracting the name part after the domain prefix
$features = @{}
$featureDesigns = @{}
$featureTechnicals = @{}

# Find Feature documents (04-feature*)
Get-ChildItem -Path $DocsRoot -Filter "04-feature*" -File | ForEach-Object {
    $base = $_.BaseName
    $family = $base -replace '^04-feature-', ''
    if ($family -eq $base) { $family = "" }
    $features[$family] = $_.FullName
}

# Find Feature-Design documents (09-feature-design*)
Get-ChildItem -Path $DocsRoot -Filter "09-feature-design*" -File | ForEach-Object {
    $base = $_.BaseName
    $family = $base -replace '^09-feature-design-', ''
    if ($family -eq $base) { $family = "" }
    $featureDesigns[$family] = $_.FullName
}

# Find Feature-Technical documents (10-feature-technical*)
Get-ChildItem -Path $DocsRoot -Filter "10-feature-technical*" -File | ForEach-Object {
    $base = $_.BaseName
    $family = $base -replace '^10-feature-technical-', ''
    if ($family -eq $base) { $family = "" }
    $featureTechnicals[$family] = $_.FullName
}

$featuresCount = $features.Count
$featureDesignsCount = $featureDesigns.Count
$featureTechnicalsCount = $featureTechnicals.Count
$validMappings = 0
$orphans = 0
$evidence = @()

# Check: every Feature should have a Feature-Design and Feature-Technical
foreach ($family in $features.Keys) {
    $label = if ($family -eq "") { "<untitled>" } else { $family }
    $hasDesign = $featureDesigns.ContainsKey($family)
    $hasTechnical = $featureTechnicals.ContainsKey($family)

    if ($hasDesign -and $hasTechnical) {
        $validMappings++
    } else {
        $orphans++
        $missing = @()
        if (-not $hasDesign) { $missing += "Feature-Design" }
        if (-not $hasTechnical) { $missing += "Feature-Technical" }
        $evidence += "Feature '$label' is missing: $($missing -join ', ')"
    }
}

# Check: every Feature-Technical should have a parent Feature
foreach ($family in $featureTechnicals.Keys) {
    $label = if ($family -eq "") { "<untitled>" } else { $family }
    if (-not $features.ContainsKey($family)) {
        $orphans++
        $evidence += "Feature-Technical '$label' has no parent Feature"
    }
}

# Check: every Feature-Design should have a parent Feature
foreach ($family in $featureDesigns.Keys) {
    $label = if ($family -eq "") { "<untitled>" } else { $family }
    if (-not $features.ContainsKey($family)) {
        $orphans++
        $evidence += "Feature-Design '$label' has no parent Feature"
    }
}

# Determine status
$total = $featuresCount + $featureDesignsCount + $featureTechnicalsCount
if ($total -eq 0) {
    $status = "not_applicable"
    $evidence = @("No Feature/Feature-Design/Feature-Technical documents found in docs-root")
} elseif ($orphans -gt 0) {
    $status = "fail"
} else {
    $status = "pass"
}

$result = @{
    check = "feature-family-mapping"
    domain = "_generic"
    category = "C"
    status = $status
    metrics = @{
        features_count = $featuresCount
        feature_designs_count = $featureDesignsCount
        feature_technicals_count = $featureTechnicalsCount
        valid_mappings = $validMappings
        orphans = $orphans
    }
    evidence = $evidence
    executed_at = $executedAt
    repo_fingerprint = $RepoFingerprint
}

$result | ConvertTo-Json -Depth 10 | Set-Content -Path $Out -Encoding UTF8
