@echo off
chcp 65001 > nul
set PYTHONIOENCODING=utf-8
echo ===================================================
echo [Academic PKM] Autorizacao Consensus MCP (OAuth)
echo ===================================================
echo Abrindo navegador para autorizar conexao com Consensus...
uv run python "%~dp0consensus.py" auth
pause
