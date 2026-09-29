# Contexto do Projeto: Academic PKM (`acc_pkm`)

Repositório de Gestão de Conhecimento Pessoal (Personal Knowledge Management - PKM) exclusivamente acadêmico e científico (metodologia, pesquisa quanti/quali, revisões sistemáticas, redação de dissertações/teses). **Totalmente isolado do projeto Startuzeiro.**

## Estrutura do Projeto
- `resources/_lake/`: Data Lake onde ficam as transcrições Markdown (`.md`) e os livros/artigos em `.pdf` e `.epub`.
- `resources/_lake_catalog.html`: Painel web interativo para busca, filtros e leitura do acervo (localização única, sem duplicatas na raiz).
- `scripts/`: Scripts utilitários, automações e arquivos `.bat` (evitar arquivos soltos na raiz).
- `.agents/skills/transcript/SKILL.md`: Definição da skill e do comando `/transcript`.
- `.agents/skills/web-harvest/SKILL.md`: Definição da skill e comandos `/scrape`, `/crawl` e `/paper-search`.
- `.agents/skills/zotero/SKILL.md`: Definição da skill e comando `/zotero`.

## Comandos Rápidos
- `/zotero sync`: Sincroniza todo o acervo do Zotero Desktop para `resources/_lake/` com parsing PyMuPDF4LLM e atualiza `master.bib` e o catálogo.
- `/zotero search "<termo>"`: Busca instantânea na biblioteca local via SQLite.
- `/zotero add "<doi>"`: Adiciona artigo por DOI no Zotero, obtém o PDF e puxa para o Lake.
- `/transcript <url>`: Transcreve um vídeo, salva no Lake e atualiza o catálogo em `resources/`.
- `/transcript <url1> <url2>`: Transcreve múltiplos vídeos em lote.
- `/transcript <playlist_url>`: Transcreve automaticamente todos os vídeos de uma playlist.
- `/transcript reindex`: Re-escaneia o `_lake` e reconstrói o catálogo HTML em `resources/_lake_catalog.html`.
- `/scrape <url>`: Raspa página web com Scrapling stealth e fallback Firecrawl, salva no Lake e cataloga.
- `/paper-search "<termo>"`: Busca literatura científica e preprints via Firecrawl Research Index.
- `/crawl <url>`: Rastreamento recursivo de documentação para o Lake.
