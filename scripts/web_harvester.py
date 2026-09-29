"""
🌊 Academic PKM — Heavy Web Harvester & Research Engine
Integrates Scrapling (Anti-bot Stealth Local Fetcher) + Firecrawl (Cloud Deep Research & Paper Search).

Self-contained, automated, and strictly scoped for Academic PKM research.
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Console para saídas estilizadas
console = Console(force_terminal=True)

# Caminhos do repositório
REPO_ROOT = Path(__file__).resolve().parent.parent
LAKE_DIR = REPO_ROOT / "resources" / "_lake"
CATALOG_HTML = REPO_ROOT / "resources" / "_lake_catalog.html"
CATALOG_JSONL = REPO_ROOT / "resources" / "_catalog" / "documents.jsonl"
ENV_PATH = REPO_ROOT / ".env"

# Carregar variáveis de ambiente (.env)
if ENV_PATH.exists():
    load_dotenv(ENV_PATH)
else:
    load_dotenv()


def sanitize_filename(name: str) -> str:
    """Normaliza e sanitiza nome para arquivo Markdown no Lake."""
    name = unicodedata.normalize("NFKD", name)
    name = "".join(c for c in name if not unicodedata.combining(c))
    name = re.sub(r"[^\w\s-]", "", name).strip()
    name = re.sub(r"[-\s]+", "_", name)
    return name.lower()[:90] or "web_resource"


def extract_domain(url: str) -> str:
    """Extrai domínio limpo da URL."""
    try:
        parsed = urlparse(url)
        netloc = parsed.netloc.lower()
        if netloc.startswith("www."):
            netloc = netloc[4:]
        return netloc or "web"
    except Exception:
        return "web"


def trigger_catalog_reindex():
    """Aciona reindexação autônoma do catálogo Lake."""
    try:
        scripts_dir = REPO_ROOT / "scripts"
        if str(scripts_dir) not in sys.path:
            sys.path.insert(0, str(scripts_dir))
        if str(REPO_ROOT) not in sys.path:
            sys.path.insert(0, str(REPO_ROOT))
        import yt_transcribe_and_catalog as ytc
        items = ytc.scan_lake_items(LAKE_DIR)
        ytc.generate_catalog_html(items, CATALOG_HTML)
        # Atualiza JSONL
        CATALOG_JSONL.parent.mkdir(parents=True, exist_ok=True)
        with open(CATALOG_JSONL, "w", encoding="utf-8") as f:
            for it in items:
                f.write(json.dumps(it, ensure_ascii=False) + "\n")
        console.print("[dim green]✔ Catálogo Lake reindexado com sucesso.[/dim green]")
    except Exception as e:
        console.print(f"[yellow]⚠️ Aviso ao reindexar catálogo: {e}[/yellow]")


def scrape_with_scrapling_http(url: str) -> Dict[str, Any]:
    """
    Tier 1: Scrapling HTTP rápido (Chrome TLS Fingerprint impersonate).
    Custo: 0 créditos, sem abrir navegador, sub-segundo.
    """
    from scrapling import Fetcher

    console.print(f"[cyan]⚡ [Scrapling HTTP][/cyan] Requisitando {url}...")
    res = Fetcher.get(url, stealthy_headers=True, timeout=20)
    
    if res.status not in [200, 201]:
        raise ValueError(f"HTTP status {res.status}")

    # Tenta extrair título
    title = ""
    title_elem = res.css("title::text").get() or res.css("h1::text").get()
    if title_elem:
        title = title_elem.strip()

    # Extrai Markdown limpo
    markdown = res.markdown(main_content_only=True)
    if not markdown or len(markdown.strip()) < 80:
        # Se veio vazio ou muito curto, pode ser SPA em JS ou bloqueio
        raise ValueError("Conteúdo Markdown vazio ou protegido por JavaScript.")

    # Detecta mensagens típicas de Cloudflare
    low = markdown.lower()
    if "just a moment..." in low or "cloudflare" in low and "turnstile" in low:
        raise ValueError("Desafio Cloudflare/Turnstile detectado.")

    return {
        "success": True,
        "title": title or extract_domain(url),
        "markdown": markdown.strip(),
        "engine": "scrapling_http",
        "status": res.status,
    }


def scrape_with_scrapling_stealth(url: str) -> Dict[str, Any]:
    """
    Tier 2: Scrapling Stealth Browser (Patchright + Cloudflare bypass).
    Executa navegador headless indetectável, resolve Turnstile localmente sem custo de nuvem.
    """
    from scrapling.fetchers import StealthyFetcher

    console.print(f"[magenta]🛡️ [Scrapling Stealth][/magenta] Iniciando navegador indetectável para {url}...")
    res = StealthyFetcher.fetch(url, headless=True, solve_cloudflare=True, timeout=35000)

    if res.status not in [200, 201]:
        raise ValueError(f"Stealth HTTP status {res.status}")

    title = ""
    title_elem = res.css("title::text").get() or res.css("h1::text").get()
    if title_elem:
        title = title_elem.strip()

    markdown = res.markdown(main_content_only=True)
    if not markdown or len(markdown.strip()) < 80:
        raise ValueError("Conteúdo retornado pelo Stealth Browser insuficiente.")

    return {
        "success": True,
        "title": title or extract_domain(url),
        "markdown": markdown.strip(),
        "engine": "scrapling_stealth",
        "status": res.status,
    }


def scrape_with_firecrawl(url: str) -> Dict[str, Any]:
    """
    Tier 3: Firecrawl Cloud Scrape.
    Utiliza a API do Firecrawl para raspagem pesada em nuvem, garantindo contorno de barreiras extremas.
    """
    api_key = os.getenv("FIRECRAWL_API_KEY")
    if not api_key:
        raise ValueError("FIRECRAWL_API_KEY não configurada no arquivo .env!")

    from firecrawl import FirecrawlApp

    console.print(f"[orange3]🔥 [Firecrawl Cloud][/orange3] Raspando via API oficial para {url}...")
    app = FirecrawlApp(api_key=api_key)
    doc = app.scrape(url, formats=["markdown"])

    title = ""
    if hasattr(doc, "metadata") and doc.metadata:
        title = getattr(doc.metadata, "title", "") or ""
    
    markdown = getattr(doc, "markdown", "") or ""
    if not markdown:
        raise ValueError("Firecrawl não retornou conteúdo markdown.")

    return {
        "success": True,
        "title": title or extract_domain(url),
        "markdown": markdown.strip(),
        "engine": "firecrawl_cloud",
        "status": 200,
    }


def harvest_url(
    url: str,
    engine: str = "auto",
    tags: Optional[List[str]] = None,
    category: str = "web_article",
    author: str = "",
    save: bool = True,
) -> Dict[str, Any]:
    """
    Executa raspagem com cascata híbrida e inteligente:
    1. Scrapling HTTP (0 créditos, ultra rápido)
    2. Scrapling Stealth (Patchright + Cloudflare Turnstile bypass local)
    3. Firecrawl Cloud (Fallback garantido via proxy residencial em nuvem)
    """
    tags = tags or ["pesquisa", "web"]
    domain = extract_domain(url)
    result = None
    errors = []

    if engine == "scrapling-http":
        result = scrape_with_scrapling_http(url)
    elif engine == "scrapling-stealth":
        result = scrape_with_scrapling_stealth(url)
    elif engine == "firecrawl":
        result = scrape_with_firecrawl(url)
    else:  # auto
        # Tentativa 1: Scrapling HTTP
        try:
            result = scrape_with_scrapling_http(url)
            console.print("[green]✔ Sucesso via Scrapling HTTP![/green]")
        except Exception as e1:
            errors.append(f"Scrapling HTTP: {e1}")
            console.print(f"[yellow]⚠️ Scrapling HTTP encontrou barreira: {e1}[/yellow]")
            # Tentativa 2: Scrapling Stealth
            try:
                result = scrape_with_scrapling_stealth(url)
                console.print("[green]✔ Sucesso via Scrapling Stealth Browser![/green]")
            except Exception as e2:
                errors.append(f"Scrapling Stealth: {e2}")
                console.print(f"[yellow]⚠️ Scrapling Stealth falhou: {e2}[/yellow]")
                # Tentativa 3: Firecrawl Cloud
                if os.getenv("FIRECRAWL_API_KEY"):
                    try:
                        result = scrape_with_firecrawl(url)
                        console.print("[green]✔ Sucesso via Firecrawl Cloud![/green]")
                    except Exception as e3:
                        errors.append(f"Firecrawl Cloud: {e3}")
                        console.print(f"[red]❌ Firecrawl também falhou: {e3}[/red]")
                else:
                    console.print("[dim]FIRECRAWL_API_KEY ausente para fallback.[/dim]")

    if not result:
        raise RuntimeError(f"Falha ao raspar {url}. Erros acumulados: {' | '.join(errors)}")

    title = result.get("title") or domain
    markdown_content = result.get("markdown") or ""
    used_engine = result.get("engine") or "unknown"
    words = len(markdown_content.split())

    # Resumo automático (primeiros 200 caracteres ou primeiro parágrafo)
    paragraphs = [p.strip() for p in markdown_content.split("\n\n") if p.strip() and not p.startswith("#")]
    summary = paragraphs[0][:250] + "..." if paragraphs else f"Artigo raspado da web: {title}"

    slug = sanitize_filename(f"{domain}_{title}")
    now_iso = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    # Frontmatter YAML estruturado
    frontmatter = f"""---
tipo: {category}
title: "{title.replace('"', "'")}"
url: "{url}"
site_name: "{domain}"
author: "{author or domain}"
scraped_at: "{now_iso}"
engine: "{used_engine}"
tags: {json.dumps(tags, ensure_ascii=False)}
word_count: {words}
summary: "{summary.replace('"', "'").replace('\n', ' ')}"
---

# {title}

**Fonte Original:** [{url}]({url})  
**Extraído em:** {now_iso}  
**Mecanismo:** `{used_engine}` | **Extensão:** {words:,} palavras  

---

{markdown_content}
"""

    saved_file = None
    if save:
        LAKE_DIR.mkdir(parents=True, exist_ok=True)
        target_path = LAKE_DIR / f"{slug}.md"
        # Se arquivo já existir, adiciona timestamp curto
        if target_path.exists():
            ts_suffix = datetime.datetime.now().strftime("%H%M%S")
            target_path = LAKE_DIR / f"{slug}_{ts_suffix}.md"

        target_path.write_text(frontmatter, encoding="utf-8")
        saved_file = target_path
        console.print(f"[bold green]💾 Salvo no Lake:[/bold green] {target_path.name}")
        trigger_catalog_reindex()

    return {
        "title": title,
        "url": url,
        "engine": used_engine,
        "words": words,
        "file": str(saved_file) if saved_file else None,
        "summary": summary,
    }


def search_academic_papers(query: str, k: int = 5, save: bool = False) -> List[Dict[str, Any]]:
    """
    Pesquisa literatura científica e papers via Firecrawl Research Index.
    """
    api_key = os.getenv("FIRECRAWL_API_KEY")
    if not api_key:
        raise ValueError("FIRECRAWL_API_KEY não configurada no arquivo .env!")

    from firecrawl import FirecrawlApp
    app = FirecrawlApp(api_key=api_key)

    console.print(f"[cyan]🔍 Buscando literatura acadêmica para:[/cyan] [bold]'{query}'[/bold] (k={k})...")
    res = app.search_papers(query, k=k)

    results = []
    if isinstance(res, dict) and res.get("results"):
        results = res["results"]

    if not results:
        console.print("[yellow]Nenhum artigo acadêmico encontrado.[/yellow]")
        return []

    table = Table(title=f"Artigos Acadêmicos Encontrados ({len(results)})", border_style="cyan")
    table.add_column("#", style="dim", width=4)
    table.add_column("Título do Artigo", style="bold white", max_width=45)
    table.add_column("ID / Fonte", style="green", width=18)
    table.add_column("Abstract / Resumo", style="dim", max_width=50)

    saved_items = []
    for i, p in enumerate(results, 1):
        pid = p.get("primaryId") or p.get("paperId") or f"paper_{i}"
        title = p.get("title") or "Sem título"
        abstract = p.get("abstract") or "Sem resumo disponível."
        short_abstract = abstract[:160] + "..." if len(abstract) > 160 else abstract

        table.add_row(str(i), title, pid, short_abstract)

        if save:
            slug = sanitize_filename(f"paper_{pid}_{title}")
            now_iso = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            frontmatter = f"""---
tipo: academic_paper
title: "{title.replace('"', "'")}"
paper_id: "{pid}"
query: "{query.replace('"', "'")}"
scraped_at: "{now_iso}"
engine: "firecrawl_research"
tags: ["paper", "academic", "pesquisa"]
summary: "{short_abstract.replace('"', "'").replace('\n', ' ')}"
---

# {title}

**Identificador:** `{pid}`  
**Termo de Busca:** `{query}`  
**Data da Consulta:** {now_iso}  

## Resumo (Abstract)

{abstract}

## Citações e Metadados Brutos

```json
{json.dumps(p, ensure_ascii=False, indent=2)}
```
"""
            target = LAKE_DIR / f"{slug}.md"
            target.write_text(frontmatter, encoding="utf-8")
            saved_items.append(str(target))

    console.print(table)

    if save and saved_items:
        console.print(f"[bold green]✔ {len(saved_items)} fichamentos de papers salvos em resources/_lake/![/bold green]")
        trigger_catalog_reindex()

    return results


def crawl_site(url: str, max_pages: int = 10, tags: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """
    Rastreia recursivamente páginas de um site/documentação usando Firecrawl crawl.
    """
    api_key = os.getenv("FIRECRAWL_API_KEY")
    if not api_key:
        raise ValueError("FIRECRAWL_API_KEY necessária para crawling recursivo em nuvem.")

    from firecrawl import FirecrawlApp
    app = FirecrawlApp(api_key=api_key)

    console.print(f"[cyan]🕷️ Iniciando crawl recursivo em {url} (limite: {max_pages} páginas)...[/cyan]")
    crawl_res = app.crawl(url, limit=max_pages, formats=["markdown"])
    
    docs = getattr(crawl_res, "data", []) or []
    if not docs and isinstance(crawl_res, dict):
        docs = crawl_res.get("data", [])

    console.print(f"[green]✔ Crawl finalizado: {len(docs)} páginas obtidas.[/green]")
    saved_count = 0
    for doc in docs:
        d_url = getattr(doc, "url", None) or (doc.get("url") if isinstance(doc, dict) else url)
        d_md = getattr(doc, "markdown", None) or (doc.get("markdown") if isinstance(doc, dict) else "")
        d_meta = getattr(doc, "metadata", None) or (doc.get("metadata") if isinstance(doc, dict) else {})
        d_title = (getattr(d_meta, "title", None) if hasattr(d_meta, "title") else d_meta.get("title")) or extract_domain(d_url)

        if d_md and len(d_md.strip()) > 50:
            slug = sanitize_filename(f"doc_{d_title}")
            now_iso = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            frontmatter = f"""---
tipo: documentation
title: "{d_title.replace('"', "'")}"
url: "{d_url}"
scraped_at: "{now_iso}"
engine: "firecrawl_crawl"
tags: {json.dumps(tags or ["docs", "crawl"], ensure_ascii=False)}
word_count: {len(d_md.split())}
summary: "{d_md[:180].replace('"', "'").replace('\n', ' ')}..."
---

# {d_title}

**URL:** [{d_url}]({d_url})  

---

{d_md}
"""
            target = LAKE_DIR / f"{slug}.md"
            target.write_text(frontmatter, encoding="utf-8")
            saved_count += 1

    if saved_count > 0:
        trigger_catalog_reindex()
        console.print(f"[bold green]✔ {saved_count} páginas catalogadas no Lake![/bold green]")

    return docs


def main():
    parser = argparse.ArgumentParser(
        description="🌊 Academic PKM — Motor Unificado de Web Scraping & Pesquisa Acadêmica (Scrapling + Firecrawl)",
    )
    subparsers = parser.add_subparsers(dest="command", help="Comandos disponíveis")

    # 1. Scrape
    p_scrape = subparsers.add_parser("scrape", help="Raspar página web ou artigo")
    p_scrape.add_argument("urls", nargs="+", help="Uma ou mais URLs para raspar")
    p_scrape.add_argument("--engine", choices=["auto", "scrapling-http", "scrapling-stealth", "firecrawl"], default="auto", help="Mecanismo (padrão: auto)")
    p_scrape.add_argument("--tags", help="Tags separadas por vírgula")
    p_scrape.add_argument("--category", default="web_article", help="Categoria (padrão: web_article)")
    p_scrape.add_argument("--no-save", action="store_true", help="Apenas imprimir, não salvar no Lake")

    # 2. Search Papers
    p_papers = subparsers.add_parser("search-papers", help="Buscar papers acadêmicos e literatura científica")
    p_papers.add_argument("query", help="Termo de pesquisa (ex: 'literature review methodology')")
    p_papers.add_argument("-k", "--limit", type=int, default=5, help="Quantidade máxima de papers (padrão: 5)")
    p_papers.add_argument("--save", action="store_true", help="Salvar fichamentos dos papers no Lake")

    # 3. Crawl
    p_crawl = subparsers.add_parser("crawl", help="Rastrear documentação ou seção inteira de site")
    p_crawl.add_argument("url", help="URL inicial do site ou documentação")
    p_crawl.add_argument("--max-pages", type=int, default=10, help="Limite máximo de páginas (padrão: 10)")
    p_crawl.add_argument("--tags", help="Tags separadas por vírgula")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    if args.command == "scrape":
        tags = [t.strip() for t in args.tags.split(",")] if args.tags else ["pesquisa", "web"]
        for u in args.urls:
            console.rule(f"[bold]Raspando: {u}[/bold]")
            try:
                res = harvest_url(
                    url=u,
                    engine=args.engine,
                    tags=tags,
                    category=args.category,
                    save=not args.no_save,
                )
                console.print(Panel(
                    f"[bold]{res['title']}[/bold]\n"
                    f"Mecanismo: [green]{res['engine']}[/green] | Palavras: {res['words']:,}\n"
                    f"Arquivo: [cyan]{res['file']}[/cyan]",
                    title="Sucesso na Raspagem",
                    border_style="green",
                ))
            except Exception as e:
                console.print(f"[bold red]❌ Erro ao raspar {u}:[/bold red] {e}")

    elif args.command == "search-papers":
        try:
            search_academic_papers(args.query, k=args.limit, save=args.save)
        except Exception as e:
            console.print(f"[bold red]❌ Erro ao buscar papers:[/bold red] {e}")

    elif args.command == "crawl":
        tags = [t.strip() for t in args.tags.split(",")] if args.tags else ["docs", "crawl"]
        try:
            crawl_site(args.url, max_pages=args.max_pages, tags=tags)
        except Exception as e:
            console.print(f"[bold red]❌ Erro no crawl:[/bold red] {e}")


if __name__ == "__main__":
    main()
