# Contexto do Projeto: Academic PKM (`acc_pkm`)

Repositório de Gestão de Conhecimento Pessoal (Personal Knowledge Management - PKM) exclusivamente acadêmico e científico (metodologia, pesquisa quanti/quali, revisões sistemáticas, redação de dissertações/teses). **Totalmente isolado do projeto Startuzeiro.**

## Estrutura do Projeto

- `resources/_lake/`: Data Lake onde ficam as transcrições Markdown (`.md`) e os livros/artigos em `.pdf` e `.epub`.
- `resources/_lake_catalog.html`: Painel web interativo para busca, filtros e leitura do acervo (localização única, sem duplicatas na raiz).
- `scripts/`: Scripts utilitários, automações e arquivos `.bat` (evitar arquivos soltos na raiz).
- `.agents/skills/transcript/SKILL.md`: Definição da skill e do comando `/transcript`.
- `.agents/skills/web-harvest/SKILL.md`: Definição da skill e comandos `/scrape`, `/crawl` e `/paper-search`.
- `.agents/skills/zotero/SKILL.md`: Definição da skill e comando `/zotero`.
- `.agents/skills/latex/SKILL.md`: Definição da skill e comandos `/latex` e `/overleaf`.
- `.agents/skills/consensus/SKILL.md`: Definição da skill e comando `/consensus`.
- `.agents/skills/fleet/SKILL.md`: Definição da skill e comando `/fleet` (Mini-Frota Acadêmica Concorrente).

- `/convert <input> [-o output.docx] [--csl abnt|apa|ieee]`: Converte documentos acadêmicos via Pandoc com resolução CSL e BibTeX.
- `/fleet "<termo>"`: Consulta concorrente em múltiplos provedores (arXiv, OpenAlex, S2, CrossRef, Consensus) com desduplicação e síntese no Lake com `--save`.
- `/consensus "<pergunta>"`: Busca evidências científicas e consenso no Consensus.app e salva no Lake com `--save`.
- `/consensus auth`: Inicia fluxo de autorização OAuth no navegador para o Consensus MCP.
- `/latex new <nome> [--template sbc|tcc]`: Cria projeto acadêmico a partir dos templates SBC ou ABNT.
- `/latex build [projeto]`: Compila manuscrito via latexmk com SyncTeX e diagnósticos no VS Code.
- `/overleaf pack <projeto>`: Empacota projeto limpo em `.zip` com citações resolvidas de `master.bib` para o Overleaf.
- `/overleaf unpack <zip>`: Descompacta pacote do Overleaf e mescla novas referências ao `references/master.bib`.
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
- **Templates Mermaid:** em `resources/templates/mermaid/` (PRISMA, Gantt, Pipeline).


