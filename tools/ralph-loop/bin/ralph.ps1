# Ralph Loop · Windows PowerShell · 见 docs/learning/ralph-loop/00_全指南_V1.0.md
param(
    [int]$MaxIterations = 10,
    [string]$Workspace = "",
    [string]$AgentCmd = "claude --continue"
)

$ErrorActionPreference = "Stop"
$RootDir = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
if (-not $Workspace) { $Workspace = Join-Path $RootDir "workspace" }
$PromptFile = Join-Path $Workspace "prompt.md"
$ProgressFile = Join-Path $Workspace "progress.txt"
$CompleteTag = "<promise>COMPLETE</promise>"

if (-not (Test-Path $PromptFile)) {
    Write-Error "Missing prompt: $PromptFile`nCopy templates\prompt.md.template to workspace\prompt.md"
}

New-Item -ItemType Directory -Force -Path $Workspace | Out-Null
Write-Host "Ralph Loop start · max=$MaxIterations · workspace=$Workspace"

for ($i = 1; $i -le $MaxIterations; $i++) {
    Write-Host "═══ Iteration $i / $MaxIterations ═══"
    Add-Content -Path $ProgressFile -Value "`n--- iteration $i $(Get-Date -Format o) ---"

    $prompt = Get-Content -Raw -Path $PromptFile
    $output = $prompt | Invoke-Expression $AgentCmd 2>&1 | Tee-Object -Variable captured
    $text = ($captured | Out-String)

    if ($text -match [regex]::Escape($CompleteTag)) {
        Write-Host "Done at iteration $i"
        exit 0
    }

    Start-Sleep -Seconds 2
}

Write-Host "Max iterations reached without COMPLETE"
exit 1
