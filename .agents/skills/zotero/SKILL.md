---
name: zotero
description: >-
  Gerencia a biblioteca acadêmica do Zotero Desktop (local SQLite e API local de escrita), sincroniza papers, preprints e livros com o Lake (resources/_lake/) usando PyMuPDF4LLM em Markdown estruturado (tabelas e fórmulas nativas), adiciona itens por DOI/URL/ISBN, pesquisa acervo bibliográfico, consulta métricas de integridade no scite.ai e sincroniza citações com master.bib. Use sempre que o usuário invocar os comandos /zotero, /zot ou solicitar busca, adição ou sincronização de fontes acadêmicas.
---

# 📚 Zotero Lake Synchronization & Research Skill (`/zotero`)

Esta skill integra a biblioteca acadêmica local do Zotero (banco SQLite nativo `~/Zotero/zotero.sqlite`, processos locais e armazenamento de anexos em `~/Zotero/storage/`) diretamente ao ecossistema do **Academic PKM (`acc_pkm`)**.

O doc parsing é executado com **PyMuPDF4LLM**, convertendo artigos científicos e livros complexos em Markdown limpo com tabelas GFM nativas, equações matemáticas e desdobramento correto de colunas acadêmicas, sincronizando automaticamente com o catálogo web `resources/_lake_catalog.html` e o arquivo `references/master.bib`.

---

## ⚡ Comandos Rápidos (`/zotero` ou `acc zotero`)

### 1. Sincronização Completa Zotero ➔ Lake (`/zotero sync`)
Converte e transfere todos os papers da biblioteca para `resources/_lake/` com parsing de alta fidelidade:
```bash
uv run python scripts/zotero_lake_sync.py
```
- **Forçar reprocessamento de todos os itens:**
  ```bash
  uv run python scripts/zotero_lake_sync.py --force
  ```
- **Sincronizar coleção específica:**
  ```bash
  uv run python scripts/zotero_lake_sync.py --collection <COLLECTION_KEY>
  ```

### 2. Busca Rápida na Biblioteca (`/zotero search <termo>`)
Pesquisa por título, autor, ano ou tag em milissegundos via SQLite local:
```bash
zotero-cli --json search "<termo>"
```
Ou busca por tag booleana:
```bash
zotero-cli --json search --mode tag "metodologia AND quali"
```

### 3. Adição Instantânea de Fontes (`/zotero add <doi|url|isbn>`)
Adiciona o artigo à biblioteca do Zotero, baixa o PDF open-access e sincroniza automaticamente com o Lake:
```bash
uv run python scripts/acc.py zotero add "<doi_ou_url>"
```
*Exemplo:*
```bash
uv run python scripts/acc.py zotero add "10.48550/ARXIV.2412.12505"
```

### 4. Inspeção de Anexos no Disco (`/zotero path <key>`)
Retorna o caminho exato do PDF ou anexo no disco rígido:
```bash
zotero-cli --json path <ITEM_KEY>
```

### 5. Sumário Hierárquico do PDF (`outline`)
Extrai o sumário / capítulos do PDF:
```bash
zotero-cli --json outline <ITEM_KEY>
```

### 6. Leitura Paginada Inteligente (`read`)
Lê uma faixa específica de páginas em Markdown sem estourar o contexto:
```bash
zotero-cli --json read <ITEM_KEY> --pages 1-5
```

### 7. Integridade Científica & Retrações (`scite`)
Verifica se um artigo sofreu retração, errata ou se possui citações de suporte/contraste:
```bash
zotero-cli --json related <ITEM_KEY>
```

---

## 🔄 Fluxo de Ingestão e Padronização no Lake

1. **Fonte Única:** Os arquivos gerados são salvos em `resources/_lake/` com a convenção:
   `Autor_et_al-Ano-Titulo_Slug.md`
2. **YAML Frontmatter Padronizado:**
   ```yaml
   ---
   title: "Título do Artigo"
   citekey: "AutorAno"
   authors: ["Autor 1", "Autor 2"]
   year: 2025
   item_type: "preprint"
   doi: "10.xxxx/..."
   url: "https://..."
   zotero_key: "KEY8CHARS"
   source: "zotero"
   tipo: "academic_paper"
   parsed_with: "pymupdf4llm"
   original_file: "artigo.pdf"
   ---
   ```
3. **Sincronização com `references/master.bib`:**
   Toda sincronização atualiza automaticamente o arquivo de referências BibTeX do monólito, permitindo citações imediatas em LaTeX via `\cite{...}`.
4. **Atualização Automática do Catálogo:**
   Reconstrói `resources/_lake_catalog.html` e `resources/_catalog/documents.jsonl`.
