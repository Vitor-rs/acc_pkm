@echo off
chcp 65001 > nul
set PYTHONIOENCODING=utf-8
echo ===================================================
echo [Academic PKM] Compilador LaTeX (latexmk + SyncTeX)
echo ===================================================
uv run python "%~dp0acc.py" build %*
pause
