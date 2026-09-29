# 🌊 Academic PKM (`acc_pkm`) — Monorepo de Pesquisa Acadêmica & PKM

Repositório central de gerenciamento de conhecimento pessoal e acadêmico (**Personal Knowledge Management - PKM**), focado em pesquisa científica, metodologia quantitativa/qualitativa, revisões sistemáticas, escrita de artigos/dissertações em LaTeX e automações via Python (`uv`).

> [!IMPORTANT]
> **Isolamento de Escopo:** Este repositório é estritamente voltado para pesquisa acadêmica e estudos científicos. Não possui qualquer relação ou vínculo com projetos de marketing ou vendas. Todas as automações e utilitários residem organizados em `scripts/`, mantendo a raiz limpa.

---

## 🏗️ Arquitetura do Monorepo

```text
acc_pkm/
├── pyproject.toml              # Dependências e metadados do projeto Python (uv)
├── uv.lock                     # Lockfile reprodutível de dependências
├── README.md                   # Documentação geral
├── AGENTS.md                   # Regras de orquestração e contexto para agentes IA
├── GEMINI.md                   # Diretrizes operacionais
├── .github/workflows/          # CI/CD (GitHub Actions para compilação automática de LaTeX)
│   └── latex.yml
├── .vscode/                    # Configurações do VS Code (LaTeX Workshop, LTeX pt-BR, UV)
│   ├── settings.json
│   └── extensions.json
├── .agents/skills/             # Habilidades integradas do agente
│   └── transcript/SKILL.md     # Definição do comando /transcript e /yt
├── docs/                       # Documentação técnica e sínteses conceituais
├── references/                 # Base bibliográfica centralizada
│   └── master.bib              # Arquivo BibTeX mestre com acervo catalogado
├── notes/                      # PKM de notas atômicas em Markdown
│   ├── literature/             # Fichamentos de leitura e sínteses de livros/artigos
│   └── concepts/               # Notas conceituais e definições metodológicas
├── projects/                   # Artigos, relatórios e manuscritos acadêmicos
│   └── _template/              # Template LaTeX modular pronto para compilar
│       ├── main.tex
│       ├── build.bat           # Script de compilação rápida local
│       ├── references.bib
│       └── sections/           # Seções modulares (introdução, metodologia, etc.)
├── resources/                  # Data Lake e Catálogo Web
│   ├── _lake_catalog.html      # Catálogo Web Interativo e pesquisável
│   ├── _catalog/               # Metadados e índices do acervo
│   └── _lake/                  # Data Lake local (PDFs, EPUBs e transcrições .md)
└── scripts/                    # Utilitários e CLI central
    ├── acc.py                  # CLI unificada (doctor, catalog, build, new-project)
    ├── web_harvester.py        # Motor híbrido Scrapling + Firecrawl (PEP 723)
    ├── yt_transcribe_and_catalog.py  # Automação de extração do YouTube
    ├── raspar.bat              # Atalho Windows para raspagem web
    ├── buscar_papers.bat       # Atalho Windows para busca de papers
    ├── transcrever.bat         # Atalho Windows para transcrições
    └── atualizar_catalogo.bat  # Atalho Windows para reindexação do Lake
```

---

## ⚡ CLI Unificada (`scripts/acc.py`)

O repositório inclui a CLI `acc.py`, gerenciada com `uv` sem necessidade de ativação manual de ambiente virtual:

```bash
# 1. Diagnóstico completo do ambiente (Python, MiKTeX/LaTeX, Git, Lake, BibTeX, Scrapling, Firecrawl)
uv run scripts/acc.py doctor

# 2. Raspar página web com bypass anti-bot e salvar limpo no Lake
uv run scripts/acc.py scrape "https://exemplo.org/artigo" --tags "metodologia,qualitativa"

# 3. Pesquisar papers acadêmicos e preprints científicos
uv run scripts/acc.py search-papers "systematic literature review" --save

# 4. Criar um novo projeto de manuscrito a partir do template
uv run scripts/acc.py new-project "meu_artigo_2026"

# 5. Compilar um projeto LaTeX para PDF (com BibTeX e saída limpa em build/)
uv run scripts/acc.py build projects/_template

# 6. Auditar integridade da base bibliográfica BibTeX
uv run scripts/acc.py bib-audit

# 7. Reindexar o acervo de livros, transcrições e artigos no Lake
uv run scripts/acc.py catalog
```

---

## 📝 Escrita Acadêmica com LaTeX

### 1. No VS Code

- Abra o repositório no VS Code. O arquivo [`.vscode/settings.json`](file:///.vscode/settings.json) já está configurado com:
  - **LaTeX Workshop:** Compilação isolada para a pasta `build/` (evita poluir as pastas dos projetos).
  - **LTeX:** Corretor ortográfico e gramatical configurado em Português (`pt-BR`) e Inglês (`en-US`).
  - **Interpretador Python:** Aponta automaticamente para `.venv` gerado pelo `uv`.

### 2. No GitHub Actions (CI/CD)

- Qualquer push em `projects/**` aciona automaticamente o workflow [`.github/workflows/latex.yml`](file:///.github/workflows/latex.yml), que compila o PDF em ambiente Ubuntu + TeXLive e disponibiliza o PDF compilado como artefato para download.

### 3. No Overleaf

- Cada pasta dentro de `projects/` (como `projects/_template/`) é autocontida e pode ser zipada ou sincronizada diretamente com o Overleaf.

---

## 📺 Ingestão de Transcrições do YouTube & Data Lake

### Comando de Barra no Chat Antigravity

No chat com o agente no Antigravity, utilize o comando `/transcript`:

```text
/transcript https://www.youtube.com/watch?v=VIDEO_ID
/transcript URL1 URL2 URL3 --tags "metodologia,qualitativa"
/transcript https://www.youtube.com/playlist?list=PLrAX...
/transcript reindex
```

### Via Terminal

```bash
# Transcrever vídeo individual
uv run scripts/yt_transcribe_and_catalog.py "https://www.youtube.com/watch?v=VIDEO_ID"

# Transcrever playlist completa
uv run scripts/yt_transcribe_and_catalog.py "https://www.youtube.com/playlist?list=ID"

# Traduzir automaticamente para português
uv run scripts/yt_transcribe_and_catalog.py "https://www.youtube.com/watch?v=..." --translate-to pt
```

---

## 🌐 Motor de Web Scraping & Pesquisa de Literatura (Scrapling + Firecrawl)

O ecossistema integra uma arquitetura de raspagem em cascata híbrida, combinando execução local sem custos com inteligência em nuvem:

### Cascata Híbrida

1. **Tier 1 — Scrapling HTTP (0 créditos, ultra rápido):** Requisita a página com impersonação de TLS fingerprint do Chrome, extraindo Markdown higienizado.
2. **Tier 2 — Scrapling Stealth Browser (0 créditos, anti-bot):** Se detectar Cloudflare Turnstile, CAPTCHAs ou bloqueios, aciona o navegador furtivo Patchright para resolver os desafios localmente.
3. **Tier 3 — Firecrawl Cloud API (Resiliência global):** Para sites com proteções extremas ou que exigem proxies residenciais, delega a raspagem para a API em nuvem do Firecrawl.

### Comandos de Barra no Chat

- `/scrape <url>` (ou `/web <url>`): Raspa uma página web ou artigo e salva em `resources/_lake/` com frontmatter YAML e catálogo atualizado.
- `/paper-search "<termo>"` (ou `/paper "<termo>"`): Pesquisa papers acadêmicos e preprints científicos (arXiv, PubMed, etc.) e salva os fichamentos com `--save`.
- `/crawl <url>`: Rastreia documentações e sitemaps recursivamente.

### Via Terminal & Scripts

```bash
# Raspar artigo com tags
uv run scripts/web_harvester.py scrape "https://arxiv.org/abs/2301.00000" --tags "ia,metodologia"
# Ou via atalho Windows:
scripts\raspar.bat "https://exemplo.org/artigo"

# Buscar literatura científica e salvar fichamentos no Lake
uv run scripts/web_harvester.py search-papers "machine learning healthcare" -k 5 --save
# Ou via atalho Windows:
scripts\buscar_papers.bat "machine learning healthcare" --save
```

---

## 📊 Catálogo Web Interativo (`resources/_lake_catalog.html`)

O catálogo web [`resources/_lake_catalog.html`](file:///resources/_lake_catalog.html) permite explorar visualmente o acervo:

- **Busca em tempo real:** Pesquisa por título, autor, canal ou tags.
- **Modos de visualização:** Grid com cards visuais ou tabela detalhada.
- **Prévia e leitura rápida:** Visualização do resumo e trecho da obra sem abrir leitor externo.
- **Dark / Light Mode:** Alternância de tema com persistência local.
- **100% Offline:** Não depende de servidores externos ou conexão com a internet.

---

## 🛠️ Tecnologias Utilizadas

- **Gerenciador de Pacotes e Runtime:** [uv](https://github.com/astral-sh/uv) (Astral)
- **Tipografia & Diagramação:** LaTeX / pdfLaTeX / BibTeX / LaTeX Workshop
- **Extração de Mídia:** yt-dlp & youtube-transcript-api
- **Interface CLI:** Rich
- **Controle de Versão:** Git + GitHub CLI (`gh`) + GitHub Actions CI/CD
