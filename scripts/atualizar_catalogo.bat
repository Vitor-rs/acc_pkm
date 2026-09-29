@echo off
chcp 65001 > nul
setlocal

cd /d "%~dp0\.."

echo =======================================================
echo  🔄 Academic PKM - Reindexar e Atualizar Catálogo HTML
echo =======================================================

uv run scripts/yt_transcribe_and_catalog.py --reindex

echo.
echo Abrindo catalogo no navegador...
start "" "resources\_lake_catalog.html"

pause
