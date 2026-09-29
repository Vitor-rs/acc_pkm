@echo off
chcp 65001 > nul
setlocal

cd /d "%~dp0\.."

echo =======================================================
echo  🌊 Academic PKM - YouTube Lake Transcriber
echo =======================================================

if "%~1"=="" (
    echo [USO] Arraste um link ou execute:
    echo   scripts\transcrever.bat "https://www.youtube.com/watch?v=..."
    echo   scripts\transcrever.bat --playlist "https://www.youtube.com/playlist?list=..."
    echo.
    set /p URL_INPUT="Ou cole a URL do YouTube agora: "
    if not "!URL_INPUT!"=="" (
        uv run scripts/yt_transcribe_and_catalog.py "!URL_INPUT!"
    )
    goto end
)

uv run scripts/yt_transcribe_and_catalog.py %*

:end
pause
