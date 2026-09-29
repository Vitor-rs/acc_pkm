# Regras Operacionais do Academic PKM (`acc_pkm`)

## 1. Princípios de Isolamento e Organização do Projeto

- **Escopo Exclusivo:** Este projeto é estritamente **Academic PKM** (Personal Knowledge Management focado em pesquisa científica, metodologia, escrita de teses/dissertações e análise acadêmica). **NÃO tem qualquer relação com o projeto Startuzeiro** (que foca em marketing digital, vendas B2B e infoprodutos). Não misturar dados, temas ou arquivos entre os dois projetos.
- **Raiz Limpa:** Nenhum arquivo solto (scripts Python, arquivos `.bat`, dados temporários ou duplicatas) deve ser colocado na raiz. Utilitários e scripts devem ficar sempre em `scripts/`.
- **Localização Única do Catálogo:** O catálogo web interativo fica **exclusivamente** em `resources/_lake_catalog.html`. Não duplicar na raiz.
- **Data Lake Centralizado:** Todo o acervo (livros, artigos e transcrições de vídeos) fica em `resources/_lake/`.

---

## 2. Comando de Barra `/transcript` (e `/yt`)

Sempre que o usuário enviar uma mensagem iniciando com `/transcript` ou `/yt`:

1. **Interpretar os Parâmetros:**
   - Se o comando for `/transcript reindex` ou `/transcript --reindex`:
     Execute a reindexação autônoma do Lake:
     ```bash
     uv run scripts/yt_transcribe_and_catalog.py reindex
     ```
   - Se forem fornecidas uma ou mais URLs de vídeos:
     Execute a ingestão direta (com suporte a `--tags` e `--translate-to` se especificados):
     ```bash
     uv run scripts/yt_transcribe_and_catalog.py <links_ou_parametros>
     ```
   - Se for fornecida uma URL de playlist do YouTube:
     Execute a extração e ingestão automática de todos os vídeos da playlist:
     ```bash
     uv run scripts/yt_transcribe_and_catalog.py <url_da_playlist>
     ```

2. **Pós-processamento Automático:**
   - O script atualiza o catálogo `resources/_lake_catalog.html` de forma 100% automática ao final de cada execução.
   - Retorne sempre ao usuário os links clicáveis (`file:///...`) dos novos arquivos `.md` gravados em `resources/_lake/` e do catálogo web em `resources/_lake_catalog.html`.

---

## 3. Comandos de Barra de Web Scraping & Literatura (`/scrape`, `/crawl`, `/paper-search`)

Sempre que o usuário enviar comandos iniciando com `/scrape`, `/crawl`, `/paper-search` (ou `/paper`, `/web`):

1. **Raspagem de Páginas Web e Artigos (`/scrape <url>` ou `/web <url>`):**
   Execute o motor de colheita com a cascata híbrida (Scrapling HTTP -> Scrapling Stealth Browser -> Firecrawl Cloud):
   ```bash
   uv run python scripts/web_harvester.py scrape "<url>" [--tags "<tags>"]
   ```

2. **Pesquisa Semântica de Papers Acadêmicos (`/paper-search <termo>` ou `/paper <termo>`):**
   Execute a busca de literatura científica no índice Firecrawl Research:
   ```bash
   uv run python scripts/web_harvester.py search-papers "<termo>" -k 5 --save
   ```
   Com a flag `--save`, os resumos e metadados estruturados dos artigos são gravados no Data Lake (`resources/_lake/`) e catalogados imediatamente no painel HTML.

3. **Rastreamento Recursivo de Documentação (`/crawl <url>`):**
   Rastreia seções inteiras de documentações e bibliotecas para o Lake:
   ```bash
   uv run scripts/web_harvester.py crawl "<url>" --max-pages 10
   ```

4. **Pós-processamento:**
   - O catálogo `resources/_lake_catalog.html` e `resources/_catalog/documents.jsonl` são sincronizados automaticamente.
   - Apresente sempre links clicáveis (`file:///...`) para o conteúdo salvo e para o catálogo.

---

## 4. Comando de Barra do Zotero (`/zotero` e `/zot`)

Sempre que o usuário enviar comandos iniciando com `/zotero` ou `/zot`:

1. **Sincronização Completa Zotero ➔ Lake (`/zotero sync` ou `/zot sync`):**
   Executa a extração em lote com PyMuPDF4LLM e atualiza catálogo e `master.bib`:
   ```bash
   uv run python scripts/zotero_lake_sync.py [--force]
   ```

2. **Busca na Biblioteca Local (`/zotero search "<termo>"`):**
   ```bash
   zotero-cli --json search "<termo>"
   ```

3. **Adição por DOI / URL (`/zotero add "<doi_ou_url>"`):**
   Adiciona ao Zotero Desktop e puxa diretamente para o Lake:
   ```bash
   uv run python scripts/acc.py zotero add "<doi_ou_url>"
   ```

4. **Auditoria e BibTeX (`/zotero bib`):**
   ```bash
   uv run python scripts/acc.py bib-audit
   ```
