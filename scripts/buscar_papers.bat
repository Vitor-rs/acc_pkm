@echo off
chcp 65001 >nul
if "%~1"=="" (
    echo Uso: scripts\buscar_papers.bat "termo de busca" [--save]
    exit /b 1
)
uv run python "%~dp0web_harvester.py" search-papers %*
