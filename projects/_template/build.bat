@echo off
chcp 65001 > nul
setlocal

cd /d "%~dp0"
echo ===================================================
echo  Compilando Artigo Academico (LaTeX + BibTeX)
echo ===================================================

if not exist build mkdir build

echo [1/4] Primeira passada pdflatex...
pdflatex -interaction=nonstopmode -output-directory=build main.tex > nul

echo [2/4] Processando citacoes BibTeX...
cd build
bibtex main > nul
cd ..

echo [3/4] Segunda passada pdflatex...
pdflatex -interaction=nonstopmode -output-directory=build main.tex > nul

echo [4/4] Finalizando referencias cruzadas...
pdflatex -interaction=nonstopmode -output-directory=build main.tex > nul

if exist build\main.pdf (
    copy /y build\main.pdf main.pdf > nul
    echo.
    echo ✅ Sucesso! Artigo gerado em: main.pdf
) else (
    echo.
    echo ❌ Falha na compilacao. Inspecione build\main.log para detalhes.
)

pause
