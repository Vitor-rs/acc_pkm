# 🌊 Academic PKM (`acc_pkm`) — Knowledge Lake & YouTube Transcriber

Repositório central de gerenciamento de conhecimento pessoal e acadêmico (**Personal Knowledge Management - PKM**), focado exclusivamente em pesquisa científica, metodologia quantitativa/qualitativa, revisões sistemáticas e redação acadêmica.

> [!IMPORTANT]
> **Isolamento de Escopo:** Este repositório é estritamente voltado para pesquisa acadêmica e estudos científicos. Ele não possui qualquer relação ou vínculo temático com o projeto Startuzeiro (focado em mercado digital e negócios). Apenas os conceitos de automação foram adaptados de forma genérica para o ecossistema acadêmico.

---

## ⚡ Comando de Barra `/transcript` (Chat Antigravity / Skill)

No chat com o agente no Antigravity, você pode usar diretamente o comando de barra `/transcript`:

```text
/transcript https://www.youtube.com/watch?v=VIDEO_ID
/transcript URL1 URL2 URL3 --tags "metodologia,qualitativa"
/transcript https://www.youtube.com/playlist?list=PLrAX...
/transcript reindex
```

O comando aciona a skill [`transcript`](file:///.agents/skills/transcript/SKILL.md), extrai as legendas com timestamps agrupados em parágrafos coerentes, salva no Data Lake (`resources/_lake/`) e reindexa o catálogo web [`resources/_lake_catalog.html`](file:///resources/_lake_catalog.html) automaticamente.

---

## 🚀 Como Usar no Terminal / Scripts

### 1. Transcrever um ou mais Vídeos

```bash
# Transcrever um único vídeo
uv run scripts/yt_transcribe_and_catalog.py "https://www.youtube.com/watch?v=VIDEO_ID"

# Transcrever múltiplos vídeos em lote com tags
uv run scripts/yt_transcribe_and_catalog.py URL1 URL2 URL3 --tags "metodologia,pesquisa"

# No Windows via script auxiliar na pasta scripts:
scripts\transcrever.bat "https://www.youtube.com/watch?v=VIDEO_ID"
```

### 2. Transcrever uma Playlist Completa

Basta passar o link da playlist (o script detecta e desmembra todos os vídeos automaticamente):

```bash
uv run scripts/yt_transcribe_and_catalog.py "https://www.youtube.com/playlist?list=ID_DA_PLAYLIST"
```

### 3. Traduzir Transcrição Automaticamente

```bash
uv run scripts/yt_transcribe_and_catalog.py "https://www.youtube.com/watch?v=..." --translate-to pt
```

### 4. Reindexar o Lake e Atualizar o Catálogo HTML

Se você adicionar arquivos manuais ao `_lake/` (artigos, livros em PDF/EPUB ou notas), execute:

```bash
uv run scripts/yt_transcribe_and_catalog.py reindex
# Ou pelo arquivo batch na pasta scripts:
scripts\atualizar_catalogo.bat
```

---

## 📁 Estrutura Organizada de Pastas

Para manter a raiz limpa e sem arquivos dispersos:

```text
acc_pkm/
├── pyproject.toml              # Configuração e dependências do ambiente Python (uv)
├── README.md                   # Documentação do projeto
├── AGENTS.md                   # Regras operacionais do workspace e do comando /transcript
├── GEMINI.md                   # Contexto e diretrizes do agente
├── .agents/
│   └── skills/
│       └── transcript/
│           └── SKILL.md        # Definição formal da skill do agente
├── scripts/
│   ├── yt_transcribe_and_catalog.py  # Automação principal (PEP 723)
│   ├── transcrever.bat               # Atalho de execução para Windows
│   └── atualizar_catalogo.bat        # Atalho de reindexação do catálogo
└── resources/
    ├── _lake_catalog.html      # Catálogo Web Interativo (localização única)
    └── _lake/                  # Data Lake acadêmico (obras e transcrições)
        ├── *.md                # Transcrições estruturadas do YouTube
        ├── *.pdf               # Livros e manuais de metodologia/ciência de dados
        └── *.epub              # Obras acadêmicas e guias de pesquisa
```

---

## 📊 Recursos do Catálogo Web (`resources/_lake_catalog.html`)

- **Localização Única:** Mantido exclusivamente dentro de `resources/_lake_catalog.html`.
- **Busca Instantânea em Tempo Real:** Pesquise por títulos, canais, autores, resumos e tags.
- **Filtros por Categoria:** Alternância instantânea entre *Todos*, *Transcrições do YouTube* e *Livros/Artigos*.
- **Visualização em Cards & Tabela:** Escolha entre grade com miniaturas visuais ou tabela densa compacta.
- **Modal de Prévia:** Leitura imediata do resumo e amostra da transcrição sem sair da página.
- **Dark / Light Mode:** Alternância de tema com preferência persistida no navegador.
- **100% Autônomo:** Não requer internet para abrir; CSS e lógica incorporados internamente.
