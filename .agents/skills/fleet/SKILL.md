---
name: fleet
description: >-
  Orquestra a mini-frota concorrente de busca acadêmica e literatura científica do Academic PKM. Consulta em paralelo múltiplos provedores científicos abertos (arXiv, OpenAlex, Semantic Scholar, CrossRef, Consensus, Web Harvester/Scrapling), desduplica por DOI e título, enriquece metadados, grava no Data Lake com tags padronizadas ([provider]_... e [fleet]_...), sincroniza referências com master.bib e atualiza o catálogo interativo. Use sempre que o usuário invocar os comandos /fleet, /frota ou solicitar busca de literatura multibases.
---

# 🛸 Academic PKM Fleet Skill (`/fleet`)

Esta skill comanda a **Mini-Frota de Provedores Acadêmicos Multibases** do `acc_pkm`. Ela resolve o dilema de *Tool Over-Engineering Hell*, substituindo ferramentas pagas e interfaces fragmentadas por uma arquitetura agêntica concorrente, gratuita e padronizada.

---

## 🏛️ Filosofia Lakehouse em 2 Camadas

```
[arXiv] [OpenAlex] [CrossRef] [S2] [Consensus] [Web Harvester]
         \         |          |          |         /
          \--------+----------+----------+--------/
                              │
                    🛸 Academic Fleet Engine
                    (ThreadPoolExecutor Concorrente)
                    (Desduplicação por DOI & Título)
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
           [Data Lake Bronze/Silver]  [references/master.bib]
           resources/_lake/           (Citações determinísticas)
           [provider]_[id]_[slug].md            │
           [fleet]_[query_slug].md              ▼
                    │                 [Curadoria do Pesquisador]
                    ▼                           │
           [Catálogo Interativo]                ▼
           resources/_lake_catalog.html    [Zotero Desktop] (Gold)
                    │                 (/zotero add <doi> + PyMuPDF4LLM)
                    ▼                           │
           [Obsidian Vault] <───────────────────┘
           (Lente visual sem duplicar arquivos)
```

1. **Data Lake (`resources/_lake/`):** Camada de exploração ágil (Bronze/Silver). As pesquisas da frota aterrisam diretamente aqui, marcadas com tags de provedor (`[arxiv]`, `[openalex]`, `[s2]`, `[crossref]`, `[consensus]`, `[fleet]`).
2. **Zotero Desktop:** Data Warehouse curado (Gold). Apenas os artigos selecionados pelo pesquisador para redação são promovidos (`/zotero add <doi>`), extraindo texto completo com PyMuPDF4LLM.
3. **Obsidian:** Lente visual zero-copy sobre `resources/`, sem gerar cópias de arquivos.

---

## ⚡ Comandos Rápidos & Uso

### 1. Pesquisa Multibases Concorrente (`/fleet "<termo>"`)
Consulta todas as bases padrão da frota (arXiv, OpenAlex, CrossRef, Semantic Scholar, Consensus) em paralelo:
```bash
uv run python scripts/acc.py fleet "vision language models document understanding"
```

### 2. Pesquisa e Ingestão Automática no Lake & BibTeX (`--save`)
```bash
uv run python scripts/acc.py fleet "vision language models document understanding" --save
```
Com a flag `--save`:
1. Gera os fichamentos específicos de cada base com tags padronizadas:
   - `resources/_lake/[arxiv]_vision_language_models.md`
   - `resources/_lake/[openalex]_vision_language_models.md`
   - `resources/_lake/[crossref]_vision_language_models.md`
2. Gera o **Dossiê Executivo de Síntese Comparativa**:
   - `resources/_lake/[fleet]_vision_language_models.md`
3. Atualiza automaticamente `references/master.bib` com chaves canônicas (ex: `\cite{LeCun1998_GradientbasedLearning}`).
4. Reindexa o painel web interativo `resources/_lake_catalog.html` e `resources/_catalog/documents.jsonl`.

### 3. Seleção de Provedores Específicos (`-p` / `--providers`)
Para restringir a busca a bases pontuais:
```bash
# Apenas preprints do arXiv e grafo aberto do OpenAlex
uv run python scripts/acc.py fleet "reinforcement learning reasoning" -p "arxiv,openalex" -n 3 --save

# Apenas evidências com medidor de consenso
uv run python scripts/acc.py fleet "creatine cognitive performance" -p "consensus" --save
```

### 4. Listagem de Provedores Disponíveis (`acc providers`)
```bash
uv run python scripts/acc.py providers
```

---

## 🏷️ Convenção de Nomes no Data Lake

Todos os artefatos gerados seguem a convenção rígida:
- **Por Provedor:** `[provider]_[identifier]_[title_slug].ext`
- **Síntese da Frota:** `[fleet]_[query_slug].md`
- **Exemplos:**
  - `[arxiv]_2312.10997_rag_survey.md`
  - `[openalex]_w31250_benchmarking_llms.md`
  - `[fleet]_retrieval_augmented_generation.md`
