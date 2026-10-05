
"""
=============================================================================
ZOTERO LAKE SYNCHRONIZER (Academic PKM)
=============================================================================
Sincroniza fontes da biblioteca do Zotero Desktop (PDFs, preprints, artigos,
livros e páginas web) diretamente para o Data Lake (resources/_lake/) em
formato Markdown de altíssima fidelidade gerado pelo PyMuPDF4LLM.

Principais Recursos:
1. Resolução automática de anexos locais (~/Zotero/storage/).
2. Parsing de PDF para GFM Markdown estruturado com PyMuPDF4LLM:
   - Tabelas nativas em Markdown (| ... | ... |).
   - Equações matemáticas e cabeçalhos (#, ##, ###).
   - Desdobramento limpo de colunas acadêmicas múltiplas.
3. Padronização de Metadados em YAML Frontmatter unificado.
4. Nomenclatura acadêmica padronizada: Autor_et_al-Ano-Titulo_Slug.md.
5. Sincronização incremental com cache (resources/_catalog/zotero_sync_state.json).
6. Atualização automática do master.bib com citekeys do BetterBibTeX.
7. Atualização automática do Catálogo Web (resources/_lake_catalog.html).

Uso:
    uv run scripts/zotero_lake_sync.py
    uv run scripts/zotero_lake_sync.py --force
    uv run scripts/zotero_lake_sync.py --limit 20
    uv run scripts/zotero_lake_sync.py --collection <KEY>
=============================================================================
"""

import sys
import os
import json
import re
import unicodedata
import subprocess
import argparse
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, List

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import pymupdf4llm
import yaml
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.panel import Panel

console = Console()
ROOT_DIR = Path(__file__).resolve().parent.parent
LAKE_DIR = ROOT_DIR / "resources" / "_lake"
CATALOG_DIR = ROOT_DIR / "resources" / "_catalog"
SYNC_STATE_FILE = CATALOG_DIR / "zotero_sync_state.json"
MASTER_BIB_FILE = ROOT_DIR / "references" / "master.bib"


def run_zotero_cli(args: List[str]) -> Optional[Dict[str, Any]]:
    """Executa zotero-cli com saída JSON estruturada."""
    cmd = ["zotero-cli", "--json"] + args
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", env=env)
        if res.returncode == 0 and res.stdout.strip():
            return json.loads(res.stdout)
    except Exception as e:
        console.print(f"[yellow]Aviso ao executar zotero-cli {' '.join(args)}:[/yellow] {e}")
    return None


def sanitize_filename(title: str, max_chars: int = 80) -> str:
    """Sanitiza strings para nomes de arquivo seguros no Windows e Linux."""
    nfkd = unicodedata.normalize("NFKD", title)
    ascii_str = nfkd.encode("ASCII", "ignore").decode("ASCII")
    clean = re.sub(r"[^\w\s-]", "", ascii_str)
    clean = re.sub(r"[-\s]+", "_", clean).strip("_")
    return clean[:max_chars] if clean else "paper"


def generate_item_slug(item: Dict[str, Any]) -> str:
    """Gera slug no formato: PrimeiroAutor_et_al-Ano-Titulo_Slug.md"""
    creators = item.get("creators", [])
    author_part = "Anonimo"
    if creators:
        first = creators[0]
        last_name = first.get("last") or first.get("lastName") or first.get("name") or ""
        if last_name:
            last_clean = sanitize_filename(last_name, 25)
            author_part = f"{last_clean}_et_al" if len(creators) > 1 else last_clean

    raw_date = str(item.get("date") or "")
    year_match = re.search(r"\b(19\d\d|20\d\d)\b", raw_date)
    year = year_match.group(1) if year_match else "s_d"

    title = item.get("title") or "sem_titulo"
    title_slug = sanitize_filename(title, 65)

    return f"{author_part}-{year}-{title_slug}.md"


def get_attachment_info(key: str) -> Optional[Path]:
    """Obtém o caminho do anexo local no disco via zotero-cli path."""
    data = run_zotero_cli(["path", key])
    if not data or not data.get("ok"):
        return None

    text = data.get("data", {}).get("text", "")
    # Procura linha Local path: `...`
    match = re.search(r"Local path:\s*`([^`]+)`", text)
    if match:
        local_path = Path(match.group(1))
        if local_path.exists():
            return local_path
    return None


def get_bibtex_entry(key: str) -> str:
    """Busca o BibTeX formatado do item."""
    data = run_zotero_cli(["get", "bibtex", key])
    if data and data.get("ok"):
        return data.get("data", {}).get("bibtex", "").strip()
    return ""


def load_sync_state() -> Dict[str, Any]:
    """Carrega o estado da sincronização incremental."""
    if SYNC_STATE_FILE.exists():
        try:
            with open(SYNC_STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def save_sync_state(state: Dict[str, Any]):
    """Salva o estado da sincronização."""
    CATALOG_DIR.mkdir(parents=True, exist_ok=True)
    with open(SYNC_STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def append_bibtex_entries(bib_entries: List[str]):
    """Adiciona novas entradas ao master.bib evitando duplicatas de chaves."""
    if not bib_entries:
        return
    try:
        from core.bibtex_service import add_entries_to_bib
        added = add_entries_to_bib(
            bib_entries,
            MASTER_BIB_FILE,
            header_comment="% Synchronized from Zotero Desktop",
        )
        if added > 0:
            console.print(f"[green]✔ Adicionadas {added} novas entradas ao master.bib[/green]")
    except Exception as e:
        console.print(f"[yellow]Aviso ao atualizar master.bib:[/yellow] {e}")


def sync_zotero_to_lake(force: bool = False, limit: int = 500, collection_key: Optional[str] = None):
    """Executa a sincronização completa de itens do Zotero para o Lake."""
    console.print(Panel.fit(
        "[bold cyan]🌊 Sincronizador Zotero ➔ Lake (Academic PKM)[/bold cyan]\n"
        f"Extração avançada via PyMuPDF4LLM | Destino: [italic]resources/_lake/[/italic]",
        border_style="cyan"
    ))

    # 1. Carregar itens do Zotero
    console.print("[cyan]🔍 Consultando acervo do Zotero...[/cyan]")
    args = ["get", "recent", "--limit", str(limit)]
    if collection_key:
        args = ["get", "collection-items", collection_key]

    resp = run_zotero_cli(args)
    if not resp or not resp.get("ok"):
        console.print("[red]✘ Não foi possível obter itens do Zotero. Verifique se o Zotero Desktop está em execução.[/red]")
        return

    items = resp.get("data", {}).get("items", [])
    console.print(f"[bold green]✔ {len(items)} itens bibliográficos identificados no Zotero.[/bold green]")

    LAKE_DIR.mkdir(parents=True, exist_ok=True)
    sync_state = load_sync_state()

    synced_count = 0
    skipped_count = 0
    error_count = 0
    new_bib_entries = []

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console
    ) as progress:
        task = progress.add_task("Processando papers...", total=len(items))

        for it in items:
            key = it.get("key")
            title = it.get("title") or "Sem título"
            date_modified = str(it.get("dateModified") or "")
            progress.update(task, description=f"Processando: [dim]{title[:40]}...[/dim]")

            # Verificar se já foi sincronizado
            prev_info = sync_state.get(key)
            target_slug = generate_item_slug(it)
            target_file = LAKE_DIR / target_slug

            if not force and prev_info and target_file.exists():
                if prev_info.get("dateModified") == date_modified:
                    skipped_count += 1
                    progress.advance(task)
                    continue

            try:
                # 2. Localizar anexo
                att_path = get_attachment_info(key)
                parsed_with = "metadata_only"
                markdown_body = ""
                original_filename = ""

                if att_path and att_path.exists():
                    original_filename = att_path.name
                    if att_path.suffix.lower() == ".pdf":
                        # Parsing com PyMuPDF4LLM
                        parsed_with = "pymupdf4llm"
                        markdown_body = pymupdf4llm.to_markdown(str(att_path))
                    elif att_path.suffix.lower() in [".html", ".htm"]:
                        parsed_with = "html_cleaner"
                        raw_html = att_path.read_text(encoding="utf-8", errors="replace")
                        # Limpeza simples de HTML para Markdown
                        clean_text = re.sub(r"<style.*?</style>", "", raw_html, flags=re.DOTALL)
                        clean_text = re.sub(r"<script.*?</script>", "", clean_text, flags=re.DOTALL)
                        clean_text = re.sub(r"<[^>]+>", " ", clean_text)
                        clean_text = re.sub(r"\s+", " ", clean_text).strip()
                        markdown_body = clean_text
                    elif att_path.suffix.lower() == ".epub":
                        parsed_with = "epub"
                        markdown_body = f"E-book EPUB disponível localmente em: `{att_path.name}`"

                # 3. Metadados para YAML Frontmatter
                creators = []
                for c in it.get("creators", []):
                    c_name = f"{c.get('first', '')} {c.get('last', '')}".strip() or c.get("name") or ""
                    if c_name:
                        creators.append(c_name)

                citekey = it.get("citationKey") or (sanitize_filename(creators[0].split()[-1] if creators else "Anonimo", 15) + (it.get("date", "")[:4] or ""))

                raw_date = str(it.get("date") or "")
                year_match = re.search(r"\b(19\d\d|20\d\d)\b", raw_date)
                year = int(year_match.group(1)) if year_match else None

                abstract = it.get("abstractNote") or it.get("abstract") or ""

                frontmatter = {
                    "title": title,
                    "citekey": citekey,
                    "authors": creators,
                    "year": year,
                    "date": raw_date,
                    "item_type": it.get("itemType") or "article",
                    "doi": it.get("doi") or it.get("DOI") or "",
                    "url": it.get("url") or "",
                    "zotero_key": key,
                    "collections": it.get("collections") or [],
                    "tags": it.get("tags") or [],
                    "abstract": abstract[:500] + "..." if len(abstract) > 500 else abstract,
                    "source": "zotero",
                    "tipo": "academic_paper",
                    "parsed_with": parsed_with,
                    "original_file": original_filename,
                    "synced_at": datetime.now().isoformat()
                }

                # 4. Montar Documento Final
                frontmatter_str = yaml.dump(frontmatter, allow_unicode=True, sort_keys=False).strip()
                
                content_parts = [
                    f"---\n{frontmatter_str}\n---",
                    f"\n# {title}\n",
                ]

                if creators:
                    content_parts.append(f"**Autores:** {', '.join(creators)}")
                if it.get("doi"):
                    content_parts.append(f"**DOI:** [{it.get('doi')}](https://doi.org/{it.get('doi')})")
                if it.get("url"):
                    content_parts.append(f"**URL:** {it.get('url')}")
                if abstract:
                    content_parts.append(f"\n## 📌 Resumo / Abstract\n\n{abstract}\n")

                if markdown_body:
                    content_parts.append(f"\n## 📄 Conteúdo Completo do Documento\n\n{markdown_body}\n")
                else:
                    content_parts.append("\n> [!NOTE]\n> Este item foi catalogado via metadados do Zotero sem arquivo PDF local indexado.\n")

                full_markdown = "\n".join(content_parts)

                # Gravar no _lake
                with open(target_file, "w", encoding="utf-8") as f:
                    f.write(full_markdown)

                # Coletar BibTeX
                bibtex_text = get_bibtex_entry(key)
                if bibtex_text:
                    new_bib_entries.append(bibtex_text)

                # Atualizar sync state
                sync_state[key] = {
                    "title": title,
                    "target_file": target_slug,
                    "dateModified": date_modified,
                    "parsed_with": parsed_with,
                    "synced_at": datetime.now().isoformat()
                }

                synced_count += 1

            except Exception as e:
                console.print(f"[red]Erro ao sincronizar '{title}':[/red] {e}")
                error_count += 1

            progress.advance(task)

    # 5. Salvar sync state
    save_sync_state(sync_state)

    # 6. Atualizar master.bib
    if new_bib_entries:
        append_bibtex_entries(new_bib_entries)

    # 7. Atualizar Catálogo Web
    console.print("\n[cyan]🔄 Atualizando Catálogo Web (resources/_lake_catalog.html)...[/cyan]")
    try:
        from core.catalog_service import reindex_catalog
        catalog_path = ROOT_DIR / "resources" / "_lake_catalog.html"
        jsonl_path = CATALOG_DIR / "documents.jsonl"
        lake_items = reindex_catalog(LAKE_DIR, catalog_path, jsonl_path)
        console.print(f"[green]✔ Catálogo Web atualizado com sucesso ({len(lake_items)} ativos catalogados).[/green]")
    except Exception as e:
        console.print(f"[yellow]Aviso ao atualizar catálogo web:[/yellow] {e}")

    # Relatório Final
    table = Table(box=None)
    table.add_column("Métrica", style="bold")
    table.add_column("Valor", style="cyan")
    table.add_row("Novos / Atualizados no Lake", f"[bold green]{synced_count}[/bold green]")
    table.add_row("Inalterados (Cache)", f"[dim]{skipped_count}[/dim]")
    table.add_row("Erros", f"[red]{error_count}[/red]" if error_count else "0")
    table.add_row("Total de Itens no Zotero", str(len(items)))
    table.add_row("Localização do Lake", str(LAKE_DIR.relative_to(ROOT_DIR)))
    table.add_row("Catálogo Web", "resources/_lake_catalog.html")

    console.print(Panel(table, title="[bold green]Sincronização Concluída[/bold green]", border_style="green"))


def main():
    parser = argparse.ArgumentParser(description="Zotero Lake Synchronizer")
    parser.add_argument("--force", action="store_true", help="Força re-extração de todos os itens")
    parser.add_argument("--limit", type=int, default=500, help="Limite de itens a sincronizar")
    parser.add_argument("--collection", type=str, default=None, help="Chave de coleção específica")

    args = parser.parse_args()
    sync_zotero_to_lake(force=args.force, limit=args.limit, collection_key=args.collection)


if __name__ == "__main__":
    main()
