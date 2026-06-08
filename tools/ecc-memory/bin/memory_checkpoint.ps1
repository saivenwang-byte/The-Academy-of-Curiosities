# ECC memory checkpoint · Windows PowerShell
# See docs/learning/ecc/00_ECC_长期记忆全指南_V1.0.md
param(
    [Parameter(Mandatory = $true)]
    [string]$Topic,
    [string]$Notes = "",
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"
$RootDir = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $PSScriptRoot))
$SessionsDir = Join-Path $RootDir ".cursor\memory\sessions"
$TemplateFile = Join-Path $RootDir "tools\ecc-memory\templates\checkpoint.md.template"

function Get-Slug([string]$Text) {
    $slug = $Text.ToLower()
    $slug = $slug -replace '[^\w\u4e00-\u9fff]+', '-'
    $slug = $slug.Trim('-')
    if ($slug.Length -gt 40) { $slug = $slug.Substring(0, 40).TrimEnd('-') }
    if (-not $slug) { $slug = "checkpoint" }
    return $slug
}

$date = Get-Date -Format "yyyy-MM-dd"
$slug = Get-Slug $Topic
$filename = "${date}_${slug}.md"
$outPath = Join-Path $SessionsDir $filename

if (Test-Path $outPath) {
    $base = [System.IO.Path]::GetFileNameWithoutExtension($filename)
    $n = 2
    while (Test-Path $outPath) {
        $filename = "${base}_$n.md"
        $outPath = Join-Path $SessionsDir $filename
        $n++
    }
}

$branch = "unknown"
try {
    Push-Location $RootDir
    $b = git branch --show-current 2>$null
    if ($b) { $branch = $b }
} finally {
    Pop-Location
}

$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss K"
$notesBlock = if ($Notes) { $Notes } else { "(none)" }

if (-not (Test-Path $TemplateFile)) {
    throw "Missing template: $TemplateFile"
}

$content = Get-Content -Raw -Path $TemplateFile -Encoding UTF8
$content = $content -replace '\{\{DATE\}\}', $date
$content = $content -replace '\{\{TOPIC\}\}', $Topic
$content = $content -replace '\{\{BRANCH\}\}', $branch
$content = $content -replace '\{\{TIMESTAMP\}\}', $timestamp
$content = $content -replace '\{\{NOTES\}\}', $notesBlock

if ($DryRun) {
    Write-Host "[DryRun] Would write: $outPath"
    Write-Host $content
    exit 0
}

New-Item -ItemType Directory -Force -Path $SessionsDir | Out-Null
Set-Content -Path $outPath -Value $content -Encoding UTF8

Write-Host "Checkpoint written: $outPath"
Write-Host "Next: update .cursor/memory/MEMORY.md checkpoint index table."
