# Vol1 三稿对比审读 UI — 本地 HTTP 启动器
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
$port = 8765
$url = "http://localhost:$port/"

Write-Host ""
Write-Host " Vol1 三稿对比审读 UI — 本地服务器" -ForegroundColor Cyan
Write-Host " 目录: $PWD"
Write-Host " 地址: $url"
Write-Host ""
Write-Host " 按 Ctrl+C 停止服务" -ForegroundColor DarkGray
Write-Host ""

Start-Process $url
python -m http.server $port
