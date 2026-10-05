
"""
=============================================================================
CONSENSUS RESEARCH CLIENT & HARVESTER - Academic PKM
=============================================================================
Integração com o Consensus.app (busca acadêmica em mais de 200M+ de artigos
científicos revisados por pares, medidor de consenso e study snapshots).

Funcionalidades:
1. `auth`: Inicia autenticação OAuth no navegador para o MCP Consensus
2. `search`: Consulta a literatura científica, extrai evidências e sínteses
3. `--save`: Ficha as evidências no Data Lake (resources/_lake/), gera citações
   em BibTeX e atualiza o catálogo web interativo (_lake_catalog.html)

Uso via CLI:
    uv run python scripts/consensus.py auth
    uv run python scripts/consensus.py search "does exercise improve cognition in elderly" --save
=============================================================================
"""

import sys
import os
import re
import json
import subprocess
from pathlib import Path
from datetime import datetime

import httpx
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

console = Console()
ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")

CONSENSUS_API_URL = "https://api.consensus.app/v1/search"
CONSENSUS_MCP_URL = "https://mcp.consensus.app/mcp"
LAKE_DIR = ROOT_DIR / "resources" / "_lake"
MASTER_BIB = ROOT_DIR / "references" / "master.bib"


def cmd_auth():
    """Inicia o fluxo de autorização OAuth local com o Consensus via mcp-remote."""
    console.print(Panel.fit(
        "[bold cyan]🔑 Autenticação Consensus MCP (OAuth)[/bold cyan]\n"
        "O Consensus MCP utiliza autenticação OAuth 2.0 segura.\n"
        "Seu navegador será aberto para autorizar a conexão com sua conta Consensus.",
        border_style="cyan"
    ))
    try:
        cmd = ["npx", "-y", "mcp-remote", CONSENSUS_MCP_URL]
        console.print("[dim]Iniciando mcp-remote proxy e abrindo navegador...[/dim]")
        subprocess.run(cmd)
    except Exception as e:
        console.print(f"[red]Erro ao executar mcp-remote:[/red] {e}")


def search_api(query: str, api_key: str, open_access: bool = False, include_full_text: bool = True) -> dict:
    """Consulta a API REST oficial do Consensus usando x-api-key."""
    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }
    params = {
        "query": query,
        "include_full_text_chunks": str(include_full_text).lower()
    }
    if open_access:
        params["open_access"] = "true"

    with httpx.Client(timeout=30) as client:
        resp = client.get(CONSENSUS_API_URL, headers=headers, params=params)
        resp.raise_for_status()
        return resp.json()


def search_consensus(query: str, save_to_lake: bool = False, open_access: bool = False):
    """Executa a pesquisa no Consensus e exibe resultados estruturados."""
    api_key = os.getenv("CONSENSUS_API_KEY", "").strip()

    console.print(Panel.fit(
        f"[bold cyan]🔬 Consensus Academic Search[/bold cyan]\n"
        f"Pergunta / Hipótese: [bold]{query}[/bold]",
        border_style="cyan"
    ))

    if not api_key:
        console.print(Panel(
            "[yellow]⚠ Chave CONSENSUS_API_KEY não encontrada no .env[/yellow]\n\n"
            "O Consensus oferece duas formas de conexão:\n"
            " 1. [bold]Consensus MCP Server:[/bold] Conectado via OAuth em seu cliente AI (Claude, Antigravity).\n"
            "    Para autorizar via navegador, execute: [cyan]uv run python scripts/consensus.py auth[/cyan]\n\n"
            " 2. [bold]Chave de API REST Direta:[/bold]\n"
            "    Acesse [link=https://consensus.app]consensus.app[/link] ➔ Clique no seu perfil (canto inferior esquerdo)\n"
            "    ➔ [bold]API & MCP Dashboard[/bold] ➔ [bold]Keys and Clients[/bold]\n"
            "    Adicione no seu arquivo [italic].env[/italic]:\n"
            "    [cyan]CONSENSUS_API_KEY=sua_chave_aqui[/cyan]",
            title="Configuração de Acesso Consensus",
            border_style="yellow"
        ))
        return

    console.print("[dim]→ Consultando base de mais de 200M+ de artigos científicos...[/dim]")
    try:
        data = search_api(query, api_key, open_access=open_access)
    except httpx.HTTPStatusError as e:
        console.print(f"[red]Erro na API Consensus ({e.response.status_code}):[/red] {e.response.text}")
        return
    except Exception as e:
        console.print(f"[red]Falha ao conectar à API Consensus:[/red] {e}")
        return

    # Processar e exibir resultados
    papers = data.get("papers", []) or data.get("results", []) or []
    if not papers:
        console.print("[yellow]Nenhum estudo relevante encontrado para esta consulta.[/yellow]")
        return

    table = Table(box=box.ROUNDED, show_header=True, header_style="bold magenta", expand=True)
    table.add_column("Artigo / Autores", style="bold", ratio=4)
    table.add_column("Ano / Periódico", style="dim", ratio=2)
    table.add_column("Achados & Síntese Científica", ratio=6)

    md_entries = []
    bib_entries = []

    for idx, p in enumerate(papers, 1):
        title = p.get("title", "Sem título").strip()
        authors = p.get("authors", [])
        if isinstance(authors, list):
            auth_str = ", ".join(authors[:3]) + (" et al." if len(authors) > 3 else "")
        else:
            auth_str = str(authors)
        year = p.get("year", "N/D")
        journal = p.get("journal", "") or p.get("venue", "Periódico não especificado")
        doi = p.get("doi", "")
        url = p.get("url") or (f"https://doi.org/{doi}" if doi else "")
        takeaway = p.get("takeaway") or p.get("abstract", "") or p.get("summary", "")

        table.add_row(
            f"{idx}. {title}\n[dim]{auth_str}[/dim]",
            f"{year}\n[italic]{journal}[/italic]",
            takeaway[:250] + ("..." if len(takeaway) > 250 else "")
        )

        # Preparar registro Markdown para o Data Lake
        md_entry = (
            f"### {idx}. {title}\n\n"
            f"- **Autores:** {auth_str}\n"
            f"- **Ano:** {year} | **Periódico:** {journal}\n"
            f"- **DOI:** [{doi}]({url})\n"
            f"- **Síntese de Evidência (Study Snapshot):**\n"
            f"> {takeaway}\n\n"
        )
        md_entries.append(md_entry)

        # Preparar BibTeX
        if doi or title:
            clean_author = re.sub(r"[^a-zA-Z]", "", authors[0] if isinstance(authors, list) and authors else "Autor")
            cite_key = f"{clean_author.lower()}{year}_{idx}"
            bib_entry = (
                f"@article{{{cite_key},\n"
                f"  title = {{{title}}},\n"
                f"  author = {{{auth_str}}},\n"
                f"  year = {{{year}}},\n"
                f"  journal = {{{journal}}},\n"
                f"  doi = {{{doi}}},\n"
                f"  url = {{{url}}}\n"
                f"}}"
            )
            bib_entries.append((cite_key, bib_entry))

    console.print(table)

    # Salvar no Data Lake e atualizar catálogo se solicitado
    if save_to_lake:
        slug = re.sub(r"[^a-zA-Z0-9_-]", "_", query.lower().strip())[:45]
        lake_file = LAKE_DIR / f"consensus_{slug}.md"
        now_iso = datetime.now().isoformat()

        frontmatter = (
            f"---\n"
            f"title: \"Consensus: {query}\"\n"
            f"type: research_consensus\n"
            f"date: '{now_iso}'\n"
            f"source: Consensus.app AI Academic Engine\n"
            f"query: \"{query}\"\n"
            f"total_papers: {len(papers)}\n"
            f"tags: [consensus, pesquisa_cientifica, revisao_literatura, evidencias]\n"
            f"---\n\n"
            f"# 🔬 Evidências Científicas & Consenso: {query}\n\n"
            f"*Extraído do Consensus.app via Academic PKM Harvester em {datetime.now().strftime('%d/%m/%Y %H:%M')}.*\n\n"
            f"## Resumo dos Estudos Localizados ({len(papers)} artigos)\n\n"
        )

        content = frontmatter + "\n".join(md_entries)
        lake_file.write_text(content, encoding="utf-8")
        console.print(f"[bold green]✔ Fichamento gravado no Lake:[/bold green] {lake_file}")

        # Mesclar no master.bib
        if bib_entries:
            try:
                from core.bibtex_service import add_entries_to_bib
                added = add_entries_to_bib(
                    [b for _, b in bib_entries],
                    MASTER_BIB,
                    header_comment=f"% Artigos importados do Consensus: {query}",
                )
                if added > 0:
                    console.print(f"[green]✔ {added} novas referências adicionadas a references/master.bib.[/green]")
            except Exception as e:
                console.print(f"[yellow]Aviso ao sincronizar BibTeX:[/yellow] {e}")

        # Atualizar catálogo web interativo
        try:
            from core.catalog_service import reindex_catalog
            reindex_catalog(
                LAKE_DIR,
                ROOT_DIR / "resources" / "_lake_catalog.html",
                ROOT_DIR / "resources" / "_catalog" / "documents.jsonl",
            )
            console.print("[green]✔ Catálogo HTML e índice documental sincronizados.[/green]")
        except Exception as e:
            console.print(f"[yellow]Aviso ao atualizar catálogo:[/yellow] {e}")


def main():
    if len(sys.argv) < 2:
        console.print(Panel.fit(
            "[bold cyan]🔬 Consensus Academic Research CLI (`consensus`)[/bold cyan]\n"
            "Comandos:\n"
            "  [green]auth[/green]                     - Inicia autorização OAuth no navegador para o MCP\n"
            "  [green]search[/green] <pergunta> [--save] - Consulta evidências científicas e faturamentos\n\n"
            "Exemplo:\n"
            "  [italic]uv run python scripts/consensus.py search \"does caffeine enhance athletic endurance\" --save[/italic]",
            border_style="cyan"
        ))
        return

    action = sys.argv[1].lower()

    if action in ("auth", "authorize", "login"):
        cmd_auth()
    elif action in ("search", "s", "query", "ask"):
        if len(sys.argv) < 3:
            console.print("[red]Erro:[/red] Especifique a pergunta científica. Ex: consensus.py search \"does sleep help memory\"")
            return
        query = sys.argv[2]
        save = "--save" in sys.argv
        oa = "--open-access" in sys.argv or "--oa" in sys.argv
        search_consensus(query, save_to_lake=save, open_access=oa)
    else:
        # Se passado direto a pergunta: consensus.py "pergunta"
        save = "--save" in sys.argv
        oa = "--open-access" in sys.argv or "--oa" in sys.argv
        search_consensus(sys.argv[1], save_to_lake=save, open_access=oa)


if __name__ == "__main__":
    main()
