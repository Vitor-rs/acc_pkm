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

---

## 5. Comandos de Barra de LaTeX & Overleaf (`/latex` e `/overleaf`)

Sempre que o usuário enviar comandos iniciando com `/latex`, `/overleaf` ou `/tex`:

1. **Criação de Novo Projeto (`/latex new <nome> [--template sbc|tcc]`):**
   Instancia projeto acadêmico modular pronto para redação:

   ```bash
   uv run python scripts/acc.py new-project <nome> [--template sbc|tcc]
   ```

2. **Compilação de Manuscrito (`/latex build [caminho]` ou `/latex`):**
   Compila via `latexmk` com SyncTeX, resolução automática de pacotes MiKTeX e diagnóstico de erros:

   ```bash
   uv run python scripts/acc.py build [caminho_do_projeto]
   ```

3. **Empacotamento Limpo para o Overleaf (`/overleaf pack <projeto>`):**
   Gera `.zip` autocontido com apenas as referências citadas extraídas de `references/master.bib`, sem artefatos de compilação:

   ```bash
   uv run python scripts/acc.py overleaf pack <caminho_do_projeto>
   ```

4. **Descompactação e Mesclagem de Export do Overleaf (`/overleaf unpack <arquivo.zip> [nome]`):**
   Extrai o pacote em `projects/` e mescla automaticamente referências inéditas adicionadas por coautores de volta ao `references/master.bib`:

   ```bash
   uv run python scripts/acc.py overleaf unpack "<caminho_zip>" [<nome_projeto>]
   ```

5. **Sincronização de Referências e Git Bridge (`/latex sync-bib` e `/overleaf git-info`):**

   ```bash
   uv run python scripts/acc.py overleaf sync-bib <caminho_do_projeto>
   uv run python scripts/acc.py overleaf git-info
   ```

---

## 6. Comando de Barra do Consensus (`/consensus`)

Sempre que o usuário enviar comandos iniciando com `/consensus`:

1. **Pesquisa Acadêmica & Consenso Científico (`/consensus <pergunta>`):**
   Consulta a base de mais de 200M+ de artigos revisados por pares do Consensus.app:

   ```bash
   uv run python scripts/acc.py consensus "<pergunta_ou_hipotese>" [--save] [--open-access]
   ```
   - Com a flag `--save`: gera fichamento em `resources/_lake/`, atualiza `master.bib` e sincroniza `_lake_catalog.html`.

2. **Autorização OAuth do MCP (`/consensus auth`):**
   Abre o navegador para autenticação segura com o servidor oficial Consensus MCP:

   ```bash
   uv run python scripts/consensus.py auth
   ```

---

## 7. Comando de Barra da Frota Acadêmica Multibases (`/fleet` e `/frota`)

Sempre que o usuário enviar comandos iniciando com `/fleet` ou `/frota`:

1. **Pesquisa Concorrente Multibases (`/fleet "<termo>"`):**
   Consulta em paralelo todos os provedores acadêmicos (arXiv, OpenAlex, CrossRef, Semantic Scholar, Consensus):

   ```bash
   uv run python scripts/acc.py fleet "<termo_ou_pergunta>" [--save] [-p <provedores>] [-n <limite>]
   ```
   - Com a flag `--save`:
     - Grava fichamentos individuais por base com tags padronizadas em `resources/_lake/[provider]_[slug].md`.
     - Grava a síntese executiva consolidada em `resources/_lake/[fleet]_[slug].md`.
     - Sincroniza referências únicas no `references/master.bib`.
     - Atualiza o catálogo `resources/_lake_catalog.html` e `documents.jsonl`.

2. **Listagem de Provedores Conectados (`/fleet providers` ou `acc providers`):**

   ```bash
   uv run python scripts/acc.py providers
   ```

3. **Pós-processamento:**
   - Retorne sempre os links clicáveis (`file:///...`) dos arquivos gerados no Data Lake e do catálogo HTML.

---

## 8. Comando de Barra de Conversão com Pandoc (`/convert` ou `acc convert`)

Sempre que o usuário solicitar conversão de documentos para `.docx`, `.pdf` ou `.tex`:

1. **Conversão de Documentos com CSL & BibTeX:**
   ```bash
   uv run python scripts/acc.py convert "<arquivo_origem>" [-o "<arquivo_destino>"] [--csl abnt|apa|ieee] [--toc]
   ```
   - **Padrão:** Converte notas do Lake ou manuscritos para `.docx` formatado com citações e bibliografia em ABNT (`resources/csl/abnt.csl`) resolvidas de `references/master.bib`.
   - **Formatos:** Suporta Markdown, DOCX, LaTeX, PDF e HTML5.

2. **Pós-processamento:**
   - Retorne o link clicável (`file:///...`) do arquivo final convertido.

---

## 9. Padrão de Diagramação Visual com Mermaid.js

- **Formato Obrigatório:** Diagramas visuais metodológicos, fluxogramas de triagem, cronogramas e pipelines devem ser expressos em blocos de código com linguagem `mermaid`.
- **Compatibilidade Nativa:** O Mermaid roda sem extensões extras no Obsidian Vault, no preview de Markdown do VS Code, no GitHub e no painel web `resources/_lake_catalog.html`.
- **Templates Padrão:**
  - Fluxo PRISMA 2020 para Revisões Sistemáticas: [`resources/templates/mermaid/prisma_flowchart.mermaid`](file:///c:/Users/user/Documents/Vitor/acc_pkm/resources/templates/mermaid/prisma_flowchart.mermaid)
  - Cronograma de Pesquisa (Gantt): [`resources/templates/mermaid/research_gantt.mermaid`](file:///c:/Users/user/Documents/Vitor/acc_pkm/resources/templates/mermaid/research_gantt.mermaid)
  - Pipeline Metodológico: [`resources/templates/mermaid/methodology_workflow.mermaid`](file:///c:/Users/user/Documents/Vitor/acc_pkm/resources/templates/mermaid/methodology_workflow.mermaid)

---

## 10. Comandos de Revisão Sistemática & Protocolo (`/protocol` e `/matrix`)

Sempre que o usuário for estruturar uma revisão de literatura ou triar evidências:

1. **Geração de Protocolo Formal (PRISMA-P & SALSA):**
   ```bash
   uv run python scripts/acc.py protocol "<titulo_da_revisao>" [--framework pico|spider] [--author "<nome>"]
   ```
   - Gera documento auditável em `resources/protocols/protocolo_<slug>.md` congelado pré-coleta para controle de viés.

2. **Geração de Matriz Estruturada de Extração e Triagem:**
   ```bash
   uv run python scripts/acc.py matrix "<caminho_arquivo_lake_fleet.md>"
   ```
   - Extrai artigos de um dossiê do Lake e gera tabela de triagem e formulário padronizado em Markdown e CSV em `resources/protocols/`.

---

## 11. Comandos de Diagramação Visual com Diagrams.net / Draw.io (`/drawio` e `/diagram`)

Sempre que o usuário solicitar criação, edição ou exportação de diagramas visuais (PRISMA, frameworks conceituais, modelos teóricos, arquiteturas):

1. **Diagnóstico do Ambiente (`/drawio status`):**
   ```bash
   uv run python scripts/acc.py diagram status
   ```

2. **Exportação Vetorial com XML Embutido (`/drawio export`):**
   ```bash
   uv run python scripts/acc.py diagram export <arquivo.drawio> -f svg|pdf|png [--scale 2.0]
   ```
   - Gera `.drawio.svg` ou `.drawio.pdf` com a flag `-e` ativada, sendo 100% editável e diretamente incluível em manuscritos LaTeX (`\includegraphics`) ou Markdown.

3. **Edição In-Editor e Links Web Zero-Install (`/drawio url`):**
   ```bash
   uv run python scripts/acc.py diagram url <arquivo.drawio> [--open]
   ```
   - Gera URL oficial `https://app.diagrams.net/#create=...` via algoritmo RFC 1951 `zlib.deflateRaw` + base64 e abre via atalho seguro `.url`.
   - Edição local no VS Code via extensão instalada `hediet.vscode-drawio`.

4. **Instanciação de Templates Acadêmicos:**
   - Templates disponíveis em `resources/templates/drawio/` (`prisma_2020.drawio`, `conceptual_framework.drawio`).
   ```bash
   uv run python scripts/acc.py diagram template prisma_2020 -o resources/diagrams/meu_prisma.drawio
   ```
