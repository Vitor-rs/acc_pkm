---
name: latex
description: >-
  Gerencia o ciclo de vida completo de escrita, compilação e colaboração LaTeX no VS Code e na ponte Overleaf. Cria projetos a partir de templates acadêmicos (artigo SBC, dissertação/tese ABNT), compila via latexmk com SyncTeX e resolução automática de pacotes MiKTeX, autocompleta citações diretamente de references/master.bib, empacota pacotes limpos para colaboração no Overleaf (resolvendo apenas citações necessárias) e descompacta exports do Overleaf mesclando novas referências de volta à base global. Use sempre que o usuário invocar os comandos /latex, /overleaf, /tex ou solicitar criação, compilação ou sincronização de manuscritos LaTeX.
---

# 📝 LaTeX Authoring & Overleaf Bridge Skill (`/latex`)

Esta skill fornece automação e integração de alta performance para escrita acadêmica em **LaTeX no VS Code** (ambiente principal de trabalho pesado) combinada com a **ponte bidirecional com o Overleaf** (utilizado exclusivamente para colaboração com orientadores e coautores).

---

## 🏗 Arquitetura do Fluxo de Escrita

```
   ┌────────────────────────────────────────────────────────┐
   │             Monorepo Local (VS Code)                   │
   │                                                        │
   │  references/master.bib ──(IntelliSense Autocomplete)──┐│
   │                                                       ▼│
   │  templates/ ──(acc new-project)──► projects/<nome>/    │
   │                                      ├── main.tex      │
   │                                      ├── build/        │
   │                                      └── references.bib│
   │                                            ▲           │
   └────────────────────────────────────────────┼───────────┘
                                                │
                          acc overleaf pack     │ acc overleaf unpack
                                  │             │
                                  ▼             │
                      ┌──────────────────────┐  │
                      │  <projeto>_overleaf  │  │
                      │        (.zip)        │  │
                      └──────────┬───────────┘  │
                                 │              │
                                 ▼              │
                      ┌─────────────────────────┴───────────┐
                      │              Overleaf               │
                      │    (Colaboração Nuvem / Orientador) │
                      └─────────────────────────────────────┘
```

---

## ⚡ Comandos de Barra & CLI (`/latex` e `/overleaf`)

### 1. Criar Novo Projeto Acadêmico (`/latex new <nome> [--template sbc|tcc]`)
Cria um projeto modular pronto para escrita:
- **Artigo SBC (Conferências de Computação):**
  ```bash
  uv run python scripts/acc.py new-project meu_artigo --template sbc
  ```
- **TCC / Dissertação / Tese ABNT (IFMA modular):**
  ```bash
  uv run python scripts/acc.py new-project minha_dissertacao --template tcc
  ```
- **Manuscrito Básico Simples:**
  ```bash
  uv run python scripts/acc.py new-project relatorio --template simple
  ```

### 2. Compilar Manuscrito no Terminal (`/latex build [caminho]`)
Executa `latexmk` configurado com Git Perl, SyncTeX, resolução automática de passadas e auto-instalação de pacotes CTAN MiKTeX:
```bash
uv run python scripts/acc.py build projects/meu_artigo
```
*Se omitido o caminho, compila automaticamente o projeto mais recente.*
*Também disponível via script Windows:* `scripts\compilar.bat [projeto]`

### 3. Empacotar para Colaboração no Overleaf (`/overleaf pack <projeto>`)
Gera um arquivo `.zip` ultraleve, autocontido e sem arquivos temporários de build:
```bash
uv run python scripts/acc.py overleaf pack projects/meu_artigo
```
- Varre todas as citações (`\cite{...}`, `\citeonline{...}`, etc.) usadas no documento.
- Extrai apenas essas referências de `references/master.bib` e embuti-as no `.bib` local.
- Ignora pastas `build/`, `.aux`, `.log`, `.synctex.gz` e PDFs compilados na raiz.
- Instruções de upload prontas para colar no navegador:
  *Acesse overleaf.com/project ➔ New Project ➔ Upload Project ➔ Arraste o zip.*

### 4. Descompactar e Mesclar Export do Overleaf (`/overleaf unpack <arquivo.zip>`)
Quando o orientador ou coautor terminar a revisão e você baixar o zip do Overleaf:
```bash
uv run python scripts/acc.py overleaf unpack "C:/Downloads/meu_artigo.zip" [nome_projeto]
```
- Descompacta em `projects/<nome_projeto>`.
- Remove lixo do macOS (`__MACOSX`, `.DS_Store`).
- **Mesclagem Inteligente de Citações:** Audita os arquivos `.bib` trazidos do Overleaf e, caso o colaborador tenha adicionado referências novas, as adiciona automaticamente em `references/master.bib` com data e proveniência!

### 5. Sincronizar Citações Manualmente (`/latex sync-bib <projeto>`)
Sincroniza citações entre o texto e o acervo master:
```bash
uv run python scripts/acc.py overleaf sync-bib projects/meu_artigo
```

### 6. Integração Git Direta com Overleaf (`/overleaf git-info`)
Exibe o guia para quem possui conta Overleaf Premium / Institucional sincronizar diretamente via Git Subtree sem precisar baixar zips:
```bash
uv run python scripts/acc.py overleaf git-info
```

---

## 💻 Produtividade no VS Code (LaTeX Workshop)

O repositório já está configurado em `.vscode/settings.json`:
1. **Compilação Automática:** Ao salvar (`Ctrl+S`), o documento compila em segundo plano para a pasta `build/`.
2. **Atalho de Compilação:** Pressione `Ctrl+Alt+B` para compilar sob demanda.
3. **Visualizador de PDF Integrado:** Abra o PDF clicando no ícone do visualizador no topo ou `Ctrl+Alt+V`.
4. **SyncTeX Bidirecional:**
   - **Do código para o PDF:** `Ctrl+Click` no código `.tex` salta para a linha correspondente no PDF.
   - **Do PDF para o código:** `Ctrl+Click` no visualizador de PDF salta para a linha correspondente no editor `.tex`.
5. **Autocompletar Global de Citações:**
   - Ao digitar `\cite{...}`, o IntelliSense lista instantaneamente todas as 90+ referências de `references/master.bib`.
6. **Verificação Ortográfica & Gramatical em Português:**
   - Extensão LTeX ativada com suporte a `pt-BR` e termos técnicos da computação.
