@echo off
chcp 65001 > nul
set PYTHONIOENCODING=utf-8
echo ===================================================
echo [Academic PKM] Sincronizador Zotero - Lake (PyMuPDF4LLM)
echo ===================================================
uv run python "%~dp0zotero_lake_sync.py" %*
pause
