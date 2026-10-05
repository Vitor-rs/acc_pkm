
"""
=============================================================================
ACADEMIC FLEET ORCHESTRATOR - Academic PKM
=============================================================================
Mini-frota de agentes de pesquisa acadêmica que consulta concorrentemente
múltiplos provedores científicos abertos (arXiv, OpenAlex, CrossRef,
Semantic Scholar, Consensus, Web Harvester), desduplica por DOI e título,
enriquece metadados e armazena os resultados no Data Lake (resources/_lake/)
com tags padronizadas [provider]_... e sincroniza com master.bib e catálogo web.
=============================================================================
"""

from __future__ import annotations

import argparse
import concurrent.futures
import datetime
import json
import os
import re
import sys
import unicodedata
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from dotenv import load_dotenv
from rich import box
from rich.console import Console
from rich.markup import escape
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
LAKE_DIR = REPO_ROOT / "resources" / "_lake"
MASTER_BIB = REPO_ROOT / "references" / "master.bib"
CATALOG_HTML = REPO_ROOT / "resources" / "_lake_catalog.html"
CATALOG_JSONL = REPO_ROOT / "resources" / "_catalog" / "documents.jsonl"
ENV_PATH = REPO_ROOT / ".env"

if ENV_PATH.exists():
    load_dotenv(ENV_PATH)
else:
    load_dotenv()

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from providers import (
    DEFAULT_FLEET_PROVIDERS,
    AcademicPaper,
    BaseAcademicProvider,
    get_provider,
    list_providers,
    sanitize_filename,
)

console = Console(force_terminal=True)


@dataclass
class ConsolidatedPaper:
    """Artigo consolidado e enriquecido após fusão de múltiplos provedores."""
    title: str
    canonical_doi: str = ""
    authors: List[str] = field(default_factory=list)
    year: Optional[int] = None
    venue: str = ""
    url: str = ""
    pdf_url: str = ""
    abstract: str = ""
    citation_count: Optional[int] = None
    influential_citation_count: Optional[int] = None
    study_type: str = ""
    consensus_takeaway: str = ""
    discovered_by: List[str] = field(default_factory=list)
    provider_records: Dict[str, AcademicPaper] = field(default_factory=dict)

    @property
    def author_summary(self) -> str:
        if not self.authors:
            return "Autor Desconhecido"
        if len(self.authors) == 1:
            return self.authors[0]
        if len(self.authors) == 2:
            return f"{self.authors[0]} & {self.authors[1]}"
        return f"{self.authors[0]} et al."

    @property
    def citekey(self) -> str:
        first_author = "Autor"
        if self.authors:
            parts = re.sub(r"[^a-zA-Z\s]", "", self.authors[0]).strip().split()
            first_author = parts[-1].capitalize() if parts else "Autor"

        year_str = str(self.year) if self.year else "s_d"
        title_words = re.sub(r"[^a-zA-Z0-9\s]", "", self.title).strip().split()
        title_slug = "".join(w.capitalize() for w in title_words[:2]) or "Doc"
        return f"{first_author}{year_str}_{title_slug}"

    def to_bibtex(self) -> str:
        authors_bib = " and ".join(self.authors) if self.authors else "Desconhecido"
        year_bib = str(self.year) if self.year else ""
        venue_bib = self.venue or "Artigo Científico"

        lines = [f"@article{{{self.citekey},"]
        lines.append(f"  title = {{{self.title}}},")
        lines.append(f"  author = {{{authors_bib}}},")
        if year_bib:
            lines.append(f"  year = {{{year_bib}}},")
        if venue_bib:
            lines.append(f"  journal = {{{venue_bib}}},")
        if self.canonical_doi:
            lines.append(f"  doi = {{{self.canonical_doi}}},")
        if self.url:
            lines.append(f"  url = {{{self.url}}},")
        if self.abstract:
            clean_abs = self.abstract.replace("\n", " ").replace("{", "").replace("}", "")[:500]
            lines.append(f"  abstract = {{{clean_abs}}},")
        lines.append(f"  note = {{Discovered by Academic PKM Fleet: {', '.join(self.discovered_by)}}},")
        lines.append("}")
        return "\n".join(lines)


def normalize_title(title: str) -> str:
    """Normaliza título para comparação fonética/lexical simples."""
    t = unicodedata.normalize("NFKD", title.lower())
    t = "".join(c for c in t if not unicodedata.combining(c))
    t = re.sub(r"[^a-z0-9\s]", "", t)
    return re.sub(r"\s+", " ", t).strip()


def normalize_doi(doi: str) -> str:
    """Normaliza identificador DOI."""
    if not doi:
        return ""
    d = doi.lower().strip()
    d = d.replace("https://doi.org/", "").replace("http://doi.org/", "").replace("doi:", "")
    return d.strip()


def consolidate_papers(raw_results: Dict[str, List[AcademicPaper]]) -> List[ConsolidatedPaper]:
    """
    Desduplica e mescla artigos vindos de múltiplos provedores.
    Associa por DOI exato ou título normalizado idêntico.
    """
    merged: List[ConsolidatedPaper] = []
    doi_index: Dict[str, ConsolidatedPaper] = {}
    title_index: Dict[str, ConsolidatedPaper] = {}

    for provider_name, papers in raw_results.items():
        for p in papers:
            norm_doi = normalize_doi(p.doi)
            norm_title = normalize_title(p.title)

            # Procurar se já existe por DOI ou Título
            target: Optional[ConsolidatedPaper] = None
            if norm_doi and norm_doi in doi_index:
                target = doi_index[norm_doi]
            elif norm_title and norm_title in title_index:
                target = title_index[norm_title]

            if target is None:
                # Criar novo registro consolidado
                target = ConsolidatedPaper(
                    title=p.title,
                    canonical_doi=norm_doi,
                    authors=list(p.authors),
                    year=p.year,
                    venue=p.venue,
                    url=p.url,
                    pdf_url=p.pdf_url,
                    abstract=p.abstract,
                    citation_count=p.citation_count,
                    influential_citation_count=p.influential_citation_count,
                    study_type=p.study_type,
                    consensus_takeaway=p.consensus_takeaway,
                    discovered_by=[provider_name],
                    provider_records={provider_name: p},
                )
                merged.append(target)
                if norm_doi:
                    doi_index[norm_doi] = target
                if norm_title:
                    title_index[norm_title] = target
            else:
                # Enriquecer registro existente com novos dados do outro provedor
                if provider_name not in target.discovered_by:
                    target.discovered_by.append(provider_name)
                target.provider_records[provider_name] = p

                if not target.canonical_doi and norm_doi:
                    target.canonical_doi = norm_doi
                    doi_index[norm_doi] = target

                if not target.authors and p.authors:
                    target.authors = list(p.authors)
                elif len(p.authors) > len(target.authors):
                    target.authors = list(p.authors)

                if not target.year and p.year:
                    target.year = p.year

                if (not target.venue or target.venue == "Periódico Aberto") and p.venue:
                    target.venue = p.venue

                if not target.pdf_url and p.pdf_url:
                    target.pdf_url = p.pdf_url

                if not target.url and p.url:
                    target.url = p.url

                # Reter maior contagem de citações
                if p.citation_count is not None:
                    if target.citation_count is None or p.citation_count > target.citation_count:
                        target.citation_count = p.citation_count

                if p.influential_citation_count is not None:
                    if target.influential_citation_count is None or p.influential_citation_count > target.influential_citation_count:
                        target.influential_citation_count = p.influential_citation_count

                if p.consensus_takeaway and not target.consensus_takeaway:
                    target.consensus_takeaway = p.consensus_takeaway

                if (not target.abstract or len(p.abstract) > len(target.abstract)) and p.abstract:
                    target.abstract = p.abstract

    return merged


def trigger_catalog_reindex():
    """Aciona reindexação autônoma do catálogo Lake."""
    try:
        from core.catalog_service import reindex_catalog
        reindex_catalog(LAKE_DIR, CATALOG_HTML, CATALOG_JSONL)
        console.print("[dim green]✔ Catálogo Lake reindexado com sucesso.[/dim green]")
    except Exception as e:
        console.print(f"[yellow]⚠️ Aviso ao reindexar catálogo: {e}[/yellow]")


def sync_to_master_bib(papers: List[ConsolidatedPaper], query: str) -> int:
    """Sincroniza citações únicas com references/master.bib."""
    from core.bibtex_service import add_entries_to_bib
    header_comment = f"% Academic Fleet Harvest: {query} ({datetime.datetime.now().strftime('%d/%m/%Y %H:%M')})"
    bib_strings = [p.to_bibtex() for p in papers]
    return add_entries_to_bib(bib_strings, MASTER_BIB, header_comment=header_comment)


def save_fleet_synthesis(
    papers: List[ConsolidatedPaper],
    raw_results: Dict[str, List[AcademicPaper]],
    query: str,
    lake_dir: Path = LAKE_DIR
) -> Path:
    """Gera o documento analítico global de síntese [fleet]_[query].md no Lake."""
    lake_dir.mkdir(parents=True, exist_ok=True)
    slug = sanitize_filename(query)[:50]
    filename = f"[fleet]_{slug}.md"
    target_path = lake_dir / filename

    now_iso = datetime.datetime.now().isoformat()
    date_str = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    providers_used = list(raw_results.keys())

    frontmatter = (
        f"---\n"
        f"title: \"[FLEET] {query}\"\n"
        f"type: academic_fleet_synthesis\n"
        f"query: \"{query}\"\n"
        f"date: '{now_iso}'\n"
        f"providers: {json.dumps(providers_used, ensure_ascii=False)}\n"
        f"total_unique_papers: {len(papers)}\n"
        f"tags: [fleet, academic_pkm, literatura, sintese_multiprovedor, acervo]\n"
        f"---\n\n"
        f"# 🛸 [Academic Fleet] Síntese Multi-Provedor: {query}\n\n"
        f"*Colheita concorrente executada em {date_str} através dos provedores: "
        f"`{', '.join(providers_used)}`.*\n\n"
        f"## 📊 Painel Executivo de Literatura ({len(papers)} obras únicas descobertas)\n\n"
        f"| # | Título | Autores | Ano | Citações | Provedores | Links |\n"
        f"|---|---|---|---|---|---|---|\n"
    )

    rows = []
    for idx, p in enumerate(papers, 1):
        cites = str(p.citation_count) if p.citation_count is not None else "-"
        provs = " ".join(f"`{pr}`" for pr in p.discovered_by)
        links = []
        if p.canonical_doi:
            links.append(f"[DOI](https://doi.org/{p.canonical_doi})")
        elif p.url:
            links.append(f"[URL]({p.url})")
        if p.pdf_url:
            links.append(f"[📄 PDF]({p.pdf_url})")
        links_str = " \\| ".join(links) or "-"

        title_esc = p.title.replace("|", "-")
        authors_esc = p.author_summary.replace("|", "-")
        rows.append(f"| {idx} | **{title_esc}** | {authors_esc} | {p.year or '-'} | {cites} | {provs} | {links_str} |")

    table_md = "\n".join(rows) + "\n\n---\n\n## 📝 Fichamento Estruturado das Evidências\n\n"

    details = []
    for idx, p in enumerate(papers, 1):
        cites_info = f" | **Citações:** {p.citation_count}" if p.citation_count is not None else ""
        influential = f" ({p.influential_citation_count} influentes)" if p.influential_citation_count else ""
        study = f" | **Tipo de Obra:** `{p.study_type}`" if p.study_type else ""
        doi_str = f"[{p.canonical_doi}](https://doi.org/{p.canonical_doi})" if p.canonical_doi else (f"[Link]({p.url})" if p.url else "N/D")
        pdf_str = f" | [📄 PDF Aberto Encontrado]({p.pdf_url})" if p.pdf_url else ""

        entry = (
            f"### {idx}. {p.title}\n\n"
            f"- **Chave de Citação:** `\\cite{{{p.citekey}}}`\n"
            f"- **Autores:** {', '.join(p.authors) if p.authors else p.author_summary}\n"
            f"- **Periódico / Veículo:** *{p.venue or 'Sem veículo informado'}* ({p.year or 's.d.'}){cites_info}{influential}{study}\n"
            f"- **DOI / Acesso:** {doi_str}{pdf_str}\n"
            f"- **Bases que indexaram:** {', '.join(f'`{pr}`' for pr in p.discovered_by)}\n\n"
        )

        if p.consensus_takeaway:
            entry += f"#### 💡 Síntese de Evidência (Consensus AI):\n> {p.consensus_takeaway}\n\n"

        if p.abstract:
            entry += f"#### 📄 Resumo (Abstract):\n> {p.abstract}\n\n"

        entry += (
            f"<details><summary>📦 BibTeX Citação</summary>\n\n"
            f"```bibtex\n{p.to_bibtex()}\n```\n\n"
            f"</details>\n\n---\n"
        )
        details.append(entry)

    full_content = frontmatter + table_md + "\n".join(details)
    target_path.write_text(full_content, encoding="utf-8")
    return target_path


def run_fleet_query(
    query: str,
    provider_names: Optional[List[str]] = None,
    limit_per_provider: int = 5,
    save: bool = False,
    save_individual_providers: bool = True,
) -> Tuple[List[ConsolidatedPaper], Dict[str, List[AcademicPaper]], List[Path]]:
    """
    Executa a busca concorrente com todos os provedores selecionados.
    """
    if not provider_names:
        provider_names = list(DEFAULT_FLEET_PROVIDERS)

    raw_results: Dict[str, List[AcademicPaper]] = {}
    saved_files: List[Path] = []

    def fetch_provider(name: str) -> Tuple[str, List[AcademicPaper]]:
        try:
            prov = get_provider(name)
            res = prov.search(query, limit=limit_per_provider)
            return name, res
        except Exception as e:
            console.print(f"[dim yellow]⚠ Provedor {name} encontrou falha: {e}[/dim yellow]")
            return name, []

    console.print(Panel.fit(
        f"[bold cyan]🛸 Academic PKM Fleet[/bold cyan]\n"
        f"[bold]Consulta:[/bold] [italic]{query}[/italic]\n"
        f"[bold]Provedores Concorrentes:[/bold] {', '.join(f'[magenta]{p}[/magenta]' for p in provider_names)}\n"
        f"[bold]Limite por Base:[/bold] {limit_per_provider} artigos",
        border_style="cyan"
    ))

    with Progress(
        SpinnerColumn(spinner_name="dots"),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task(f"Consultando {len(provider_names)} bases científicas em paralelo...", total=None)

        with concurrent.futures.ThreadPoolExecutor(max_workers=min(len(provider_names), 8)) as executor:
            futures = [executor.submit(fetch_provider, name) for name in provider_names]
            for fut in concurrent.futures.as_completed(futures):
                p_name, papers = fut.result()
                if papers:
                    raw_results[p_name] = papers

        progress.update(task, description="Fusão e desduplicação de fontes...")

    # Desduplicar e fundir
    consolidated = consolidate_papers(raw_results)
    # Ordenar por contagem de citações (decrescente) e depois por ano
    consolidated.sort(key=lambda p: (p.citation_count or 0, p.year or 0), reverse=True)

    # Exibir Tabela de Resultados
    table = Table(
        title=f"Resultados Consolidados da Frota ({len(consolidated)} artigos únicos)",
        box=box.ROUNDED,
        header_style="bold cyan",
    )
    table.add_column("#", justify="right", style="dim")
    table.add_column("Título", style="bold", max_width=45)
    table.add_column("Autores / Ano", max_width=25)
    table.add_column("Citações", justify="center", style="green")
    table.add_column("Bases", style="magenta")
    table.add_column("DOI / PDF", style="blue")

    for i, p in enumerate(consolidated, 1):
        year_str = f"({p.year})" if p.year else ""
        auth_year = f"{escape(p.author_summary)}\n[dim]{year_str} {escape(p.venue[:20])}[/dim]"
        cites = str(p.citation_count) if p.citation_count is not None else "-"
        bases = ", ".join(p.discovered_by)

        doi_display = p.canonical_doi[:22] + "..." if len(p.canonical_doi) > 25 else p.canonical_doi
        pdf_badge = " [📄PDF]" if p.pdf_url else ""
        doi_col = f"{escape(doi_display)}{pdf_badge}" if doi_display else ("PDF Direto" if p.pdf_url else "-")

        table.add_row(str(i), escape(p.title), auth_year, cites, bases, doi_col)

    console.print(table)

    if save:
        # 1. Salvar os arquivos isolados por provedor [provider]_[query].md se solicitado
        if save_individual_providers:
            for p_name, p_list in raw_results.items():
                prov = get_provider(p_name)
                saved_path = prov.save_to_lake(p_list, query, LAKE_DIR, MASTER_BIB)
                if saved_path:
                    saved_files.append(saved_path)

        # 2. Salvar o documento executivo sintetizado [fleet]_[query].md
        fleet_synthesis = save_fleet_synthesis(consolidated, raw_results, query, LAKE_DIR)
        saved_files.append(fleet_synthesis)

        # 3. Sincronizar com master.bib
        added_bib = sync_to_master_bib(consolidated, query)

        # 4. Reindexar o catálogo web
        trigger_catalog_reindex()

        files_list = "\n".join(f"  • file:///{escape(f.as_posix())}" for f in saved_files)
        console.print(Panel.fit(
            f"[bold green]✔ Colheita Concluída com Sucesso![/bold green]\n"
            f"- [bold]Novas Citações no master.bib:[/bold] {added_bib}\n"
            f"- [bold]Catálogo Web Atualizado:[/bold] file:///{escape(CATALOG_HTML.as_posix())}\n"
            f"- [bold]Arquivos Salvos no Data Lake ({len(saved_files)}):[/bold]\n{files_list}",
            border_style="green"
        ))

    return consolidated, raw_results, saved_files


def main():
    parser = argparse.ArgumentParser(
        description="🛸 Academic PKM Fleet — Mini-Frota de Provedores Acadêmicos Multibases",
    )
    parser.add_argument("query", nargs="?", help="Termo de pesquisa científica ou pergunta de pesquisa.")
    parser.add_argument(
        "-p", "--providers",
        help=f"Lista de provedores separados por vírgula (ex: arxiv,openalex,s2,crossref,consensus,web). Padrão: todos.",
    )
    parser.add_argument(
        "-n", "--limit",
        type=int,
        default=5,
        help="Limite de resultados por provedor (padrão: 5).",
    )
    parser.add_argument(
        "--save",
        action="store_true",
        help="Salva as evidências no Lake (resources/_lake/) com tags [provider]_... e atualiza master.bib e catálogo.",
    )
    parser.add_argument(
        "--list-providers",
        action="store_true",
        help="Lista todos os provedores acadêmicos disponíveis e status.",
    )

    args = parser.parse_args()

    if args.list_providers:
        table = Table(title="Provedores Acadêmicos da Frota (Academic PKM)", box=box.ROUNDED)
        table.add_column("Tag / ID", style="bold cyan")
        table.add_column("Nome Oficial", style="bold")
        table.add_column("Descrição", style="dim")
        for p in list_providers():
            table.add_row(f"\\[{p['name']}]", p["display_name"], p["description"])
        console.print(table)
        return

    if not args.query:
        parser.print_help()
        sys.exit(1)

    prov_list = None
    if args.providers:
        prov_list = [p.strip().lower() for p in args.providers.split(",") if p.strip()]

    run_fleet_query(
        query=args.query,
        provider_names=prov_list,
        limit_per_provider=args.limit,
        save=args.save,
    )


if __name__ == "__main__":
    main()
