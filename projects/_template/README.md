# 📄 Template de Artigo Acadêmico

Este diretório serve como modelo base para a criação de novos artigos e relatórios de pesquisa no repositório `acc_pkm`.

## 📁 Estrutura

- `main.tex`: Documento mestre do artigo (preâmbulo, título, resumo e inclusão de seções).
- `sections/`: Seções modulares numeradas para redação colaborativa e ágil.
- `references.bib`: Arquivo local de referências (você pode copiar citações de `../../references/master.bib`).
- `build.bat`: Script local para compilação rápida no Windows sem sujar a pasta raiz (arquivos temporários vão para `build/`).

## ⚙️ Como Compilar

### No VS Code
Abra qualquer arquivo `.tex` e pressione `Ctrl + Alt + B` (ou use a barra lateral do **LaTeX Workshop**). O PDF gerado abrirá automaticamente em uma aba ao lado.

### Via Linha de Comando (CLI)
```bash
# Compilar usando a CLI central acc:
uv run python scripts/acc.py build projects/_template

# Ou pelo atalho local:
.\build.bat
```
