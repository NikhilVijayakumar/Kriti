[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)] [string] $RepoRoot,
    [Parameter(Mandatory=$true)] [string] $RepoFingerprint,
    [Parameter(Mandatory=$true)] [string] $Out
)

# unsafe-usage-scan: fails when an `unsafe` block or `unsafe fn`/`unsafe impl`/
# `unsafe trait`/`unsafe extern` item lacks a preceding `// SAFETY:` comment, or
# when `unwrap()`/`expect()` appears outside `#[cfg(test)]`/`#[test]` code —
# per engineering.md's Rust Engineering Practices (Unsafe Code + Error Handling).
# Same fixed contract as tier5's lint-pass.ps1: result envelope written to $Out.

$executedAt = [DateTime]::UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ")

function Write-Result($status, $evidence, $metrics) {
    $result = [ordered]@{
        repo_fingerprint = $RepoFingerprint
        check = "unsafe-usage-scan"
        domain = "codegen.code"
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

$emptyMetrics = @{ files_scanned = 0; unsafe_blocks = 0; unsafe_items = 0; unwrap_uses = 0; violations = 0 }

if (-not (Test-Path -LiteralPath $RepoRoot)) {
    Write-Result "error" @("Cannot access repo-root: $RepoRoot") $emptyMetrics
}

$files = @(Get-ChildItem -Path $RepoRoot -Recurse -File -Filter *.rs -ErrorAction SilentlyContinue |
           Where-Object { $_.FullName -notmatch '\\target\\|\\.git\\' })

if ($files.Count -eq 0) {
    Write-Result "not_applicable" @("No .rs source files found under $RepoRoot") $emptyMetrics
}

$violations = @()
$unsafeBlocks = 0
$unsafeItems = 0
$unwrapUses = 0

foreach ($file in $files) {
    $lines = @(Get-Content -Path $file.FullName -ErrorAction SilentlyContinue)
    if ($lines.Count -eq 0) { continue }

    $prevSafety = $false
    $pendingUnsafe = 0
    $pendingUnsafeNeedsSafety = $false
    $pendingTestAttr = $false
    $inTestScope = $false
    $testDepth = 0

    for ($i = 0; $i -lt $lines.Count; $i++) {
        $lineNo = $i + 1
        $line = $lines[$i]
        $trimmed = $line.Trim()
        $blank = ($trimmed.Length -eq 0)

        $opens = ([regex]::Matches($line, '\{')).Count
        $closes = ([regex]::Matches($line, '\}')).Count

        if ($inTestScope) {
            $testDepth += ($opens - $closes)
            if ($testDepth -le 0) { $inTestScope = $false; $testDepth = 0 }
        }

        if ($trimmed -match '^#\[(cfg\(test\)|test)\]') {
            $pendingTestAttr = $true
        } elseif ($pendingTestAttr -and -not $blank) {
            if ($trimmed -match '^(mod|fn)\b') {
                $inTestScope = $true
                $testDepth = $opens
                $pendingTestAttr = $false
            } else {
                $pendingTestAttr = $false
            }
        }

        if (-not $blank) {
            $safetyIdx = $line.IndexOf("SAFETY:")
            $unsafeIdx = $line.IndexOf("unsafe")
            $safetyBeforeUnsafe = ($safetyIdx -ge 0 -and $unsafeIdx -gt $safetyIdx)
            $commentIdx = $line.IndexOf("//")
            $startsComment = ($trimmed -match '^(//|/\*)')

            if ($pendingUnsafe -gt 0) {
                if ($trimmed -match '^\{') {
                    $unsafeBlocks++
                    if ($pendingUnsafeNeedsSafety) {
                        $violations += ("{0}:{1}: unsafe block missing a preceding // SAFETY: comment" -f $file.FullName, $pendingUnsafe)
                    }
                }
                $pendingUnsafe = 0
            }

            if (-not $inTestScope -and -not $startsComment) {
                $unwIdx = $line.IndexOf(".unwrap()")
                $expIdx = $line.IndexOf(".expect(")
                $hit = -1
                if ($unwIdx -ge 0) { $hit = $unwIdx }
                if ($expIdx -ge 0 -and ($hit -lt 0 -or $expIdx -lt $hit)) { $hit = $expIdx }
                if ($hit -ge 0 -and ($commentIdx -lt 0 -or $hit -lt $commentIdx)) {
                    $unwrapUses++
                    $violations += ("{0}:{1}: unwrap()/expect() used outside test code" -f $file.FullName, $lineNo)
                }
            }

            if (-not $startsComment -and $line -match 'unsafe[ \t]*\{') {
                $unsafeBlocks++
                if (-not $prevSafety -and -not $safetyBeforeUnsafe) {
                    $violations += ("{0}:{1}: unsafe block missing a preceding // SAFETY: comment" -f $file.FullName, $lineNo)
                }
            }

            if (-not $startsComment -and
                ($line -match '(^|[ \t])unsafe[ \t]+(fn|impl|trait|extern)[ \t(]' -or
                 $line -match '(^|[ \t])unsafe[ \t]+(fn|impl|trait|extern)[ \t]*$')) {
                $unsafeItems++
                if (-not $prevSafety -and -not $safetyBeforeUnsafe) {
                    $violations += ("{0}:{1}: unsafe item missing a preceding // SAFETY: comment" -f $file.FullName, $lineNo)
                }
            }

            if ($trimmed -match '^unsafe$') {
                $pendingUnsafe = $lineNo
                $pendingUnsafeNeedsSafety = (-not $prevSafety -and -not $safetyBeforeUnsafe)
            }

            if ($trimmed -match '^unsafe') {
                $prevSafety = $false
            } elseif ($safetyIdx -ge 0) {
                $prevSafety = $true
            }
        }
    }
}

$metrics = @{
    files_scanned = $files.Count
    unsafe_blocks = $unsafeBlocks
    unsafe_items = $unsafeItems
    unwrap_uses = $unwrapUses
    violations = $violations.Count
}

if ($violations.Count -eq 0) {
    Write-Result "pass" @("No unsafe usage without a preceding // SAFETY: comment; no unwrap()/expect() outside test code") $metrics
} else {
    Write-Result "fail" $violations $metrics
}
