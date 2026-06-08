@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"

echo.
echo  Vol1 三稿对比审读 UI — 本地服务器
echo  目录: %CD%
echo  地址: http://localhost:8765/
echo.
echo  按 Ctrl+C 停止服务
echo.

start "" "http://localhost:8765/"
python -m http.server 8765
