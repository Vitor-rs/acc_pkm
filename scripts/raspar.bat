@echo off
chcp 65001 >nul
if "%~1"=="" (
    echo Uso: scripts\raspar.bat "https://url-do-artigo" [--tags "tags"]
    exit /b 1
)
uv run python "%~dp0web_harvester.py" scrape %*
