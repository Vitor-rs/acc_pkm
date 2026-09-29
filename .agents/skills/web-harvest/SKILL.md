---
name: web-harvest
description: >-
  Raspa artigos científicos, documentações técnicas e páginas da web usando uma cascata híbrida e inteligente de Scrapling (anti-bot stealth local com bypass de Cloudflare Turnstile, 0 créditos) e Firecrawl (cloud deep research, paper search e crawling recursivo). Armazena o conteúdo limpo em Markdown no Data Lake (resources/_lake/) com metadados YAML e atualiza automaticamente o catálogo web interativo (resources/_lake_catalog.html). Use sempre que o usuário invocar os comandos /scrape, /crawl, /paper-search ou fornecer URLs da web para extração ou solicitar pesquisa de papers acadêmicos.
---

# 🌐 Heavy Web Harvester & Research Engine (`/scrape`, `/crawl`, `/paper-search`)

Esta skill fornece uma suíte completa e autocontida de **Web Scraping Pesado** e **Pesquisa de Literatura Acadêmica** para o ecossistema `acc_pkm`, combinando o melhor de dois mundos:
1. **Scrapling**: Raspagem local ultrarrápida, gratuita (0 créditos), com emulação de TLS Fingerprint do Chrome e navegador furtivo (*Patchright*) com resolução automática de desafios Cloudflare Turnstile.
2. **Firecrawl**: Raspagem e crawling recursivo em nuvem com proxies residenciais, além de índice semântico especializado em papers científicos e literatura acadêmica (arXiv, PubMed, etc.).

---

## ⚡ Comandos de Barra Disponíveis

### 1. Raspar Página Web ou Artigo (`/scrape` ou `/web`)
Raspa uma ou mais páginas da web com conversão limpa para Markdown, ignorando scripts e propagandas:

```text
/scrape https://arxiv.org/abs/2301.00000
/scrape https://site-com-cloudflare.com --tags "metodologia,ti"
/scrape URL1 URL2 URL3
```

**Comando Terminal Executado:**
```bash
uv run python scripts/web_harvester.py scrape "<url>" [--tags "tag1,tag2"]
# Ou via CLI central:
uv run python scripts/acc.py scrape "<url>"
# Ou via batch no Windows:
scripts\raspar.bat "<url>"
```

### 2. Buscar Artigos Científicos e Literatura (`/paper-search` ou `/paper`)
Realiza busca semântica no índice global de papers e preprints via Firecrawl:

```text
/paper-search "systematic literature review software engineering" -k 5 --save
/paper "qualitative data analysis methods" --save
```

**Comando Terminal Executado:**
```bash
uv run python scripts/web_harvester.py search-papers "<termo>" -k 5 --save
# Ou via CLI central:
uv run python scripts/acc.py search-papers "<termo>" --save
# Ou via batch no Windows:
scripts\buscar_papers.bat "<termo>" --save
```
> O parâmetro `--save` cria automaticamente fichamentos acadêmicos individuais em Markdown com metadados estruturados dentro de `resources/_lake/` e os cataloga imediatamente.

### 3. Rastreamento Recursivo de Documentação / Sitemaps (`/crawl`)
Extrai recursivamente múltiplas páginas de uma documentação ou seção técnica:

```text
/crawl https://docs.exemplo.org/guia --max-pages 10
```

**Comando Terminal Executado:**
```bash
uv run python scripts/web_harvester.py crawl "<url>" --max-pages 10
```

---

## 🔄 Cascata Híbrida e Inteligente de Execução

Ao receber uma URL para raspagem no modo padrão (`--engine auto`), o motor executa uma cascata de 3 níveis de resiliência:

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Scrapling HTTP (Chrome TLS Impersonate)                  │
│    ⚡ Sub-segundo | 0 tokens | 0 créditos de nuvem          │
└──────────────────────────────┬──────────────────────────────┘
                               │ Falha / Cloudflare / 403
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Scrapling Stealth Browser (Patchright Headless)          │
│    🛡️ Bypassa Cloudflare Turnstile localmente | 0 créditos  │
└──────────────────────────────┬──────────────────────────────┘
                               │ Bloqueio de IP extremo / JS complexo
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Firecrawl Cloud Scrape API (Proxy Residencial Global)    │
│    🔥 Renderização em nuvem via FIRECRAWL_API_KEY           │
└─────────────────────────────────────────────────────────────┘
```

---

## 💾 Ingestão no Lake & Catálogo Web

1. **Gravação no Data Lake:**
   Cada conteúdo extraído é salvo em `resources/_lake/<slug_normalizado>.md` com YAML frontmatter completo:
   ```yaml
   ---
   tipo: web_article # ou academic_paper, documentation
   title: "Título do Artigo"
   url: "https://..."
   site_name: "dominio.com"
   author: "Nome do Autor ou Domínio"
   scraped_at: "2026-09-29T16:55:00"
   engine: "scrapling_stealth"
   tags: ["metodologia", "web"]
   word_count: 1450
   summary: "Resumo executivo do conteúdo..."
   ---
   ```

2. **Reindexação Automática:**
   O catálogo interativo [`resources/_lake_catalog.html`](file:///resources/_lake_catalog.html) e o índice estruturado [`resources/_catalog/documents.jsonl`](file:///resources/_catalog/documents.jsonl) são atualizados em milissegundos sem intervenção manual.

3. **Resposta com Links Clicáveis:**
   O agente deve sempre retornar ao usuário o link clicável (`file:///...`) do arquivo `.md` salvo no Lake e do catálogo web.
