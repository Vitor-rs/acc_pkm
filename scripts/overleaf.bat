@echo off
chcp 65001 > nul
set PYTHONIOENCODING=utf-8
echo ===================================================
echo [Academic PKM] Ponte Overleaf (Pack, Unpack, Sync)
echo ===================================================
uv run python "%~dp0overleaf_bridge.py" %*
pause
