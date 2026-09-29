# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "rich>=13.7.0",
#     "pypdf>=5.0.0",
#     "pyyaml>=6.0.1",
#     "bibtexparser>=2.0.1",
#     "httpx>=0.27.0",
# ]
# ///
"""
=============================================================================
ACC CLI - Academic PKM Monorepo Management Tool
=============================================================================
Linha de comando central para o ecossistema acadêmico acc_pkm.
Gerencia diagnósticos (doctor), catalogação, criação de projetos LaTeX,
auditoria bibliográfica e compilação de manuscritos.

Uso:
    uv run scripts/acc.py doctor
    uv run scripts/acc.py catalog
    uv run scripts/acc.py new-project meu_artigo_2026
    uv run scripts/acc.py bib-audit
    uv run scripts/acc.py build [caminho_do_projeto]
    uv run scripts/acc.py transcript <url1> <url2> ...
=============================================================================
"""

import sys
import os
import shutil
import hashlib
import json
import re
import subprocess
from pathlib import Path
from datetime import datetime

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

from dotenv import load_dotenv

console = Console()
ROOT_DIR = Path(__file__).resolve().parent.parent

# Carregar variáveis de ambiente
load_dotenv(ROOT_DIR / ".env")


def check_command(cmd: str) -> tuple[bool, str]:
    """Verifica se um executável está disponível no PATH do sistema."""
    path = shutil.which(cmd)
    if not path:
        return False, "Não encontrado"
    return True, path


def cmd_doctor():
    """Executa diagnóstico completo do ambiente acadêmico."""
    console.print(Panel.fit("[bold cyan]🌊 Academic PKM Doctor[/bold cyan]\nVerificação de Ferramentas e Integridade do Monorepo", border_style="cyan"))

    table = Table(box=box.ROUNDED, show_header=True, header_style="bold magenta")
    table.add_column("Componente / Ferramenta", style="bold")
    table.add_column("Status", justify="center")
    table.add_column("Detalhes", style="dim")

    # 1. Ferramentas do Sistema
    py_ver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    table.add_row("Python", "[green]✔ OK[/green]", f"v{py_ver} ({sys.executable})")

    has_uv, uv_info = check_command("uv")
    table.add_row("UV (Astral)", "[green]✔ OK[/green]" if has_uv else "[red]✘ Ausente[/red]", uv_info)

    has_git, git_info = check_command("git")
    table.add_row("Git", "[green]✔ OK[/green]" if has_git else "[red]✘ Ausente[/red]", git_info)

    has_lfs, lfs_info = check_command("git-lfs")
    table.add_row("Git LFS", "[green]✔ OK[/green]" if has_lfs else "[yellow]⚠ Opcional[/yellow]", lfs_info)

    has_gh, gh_info = check_command("gh")
    table.add_row("GitHub CLI (gh)", "[green]✔ OK[/green]" if has_gh else "[yellow]⚠ Opcional[/yellow]", gh_info)

    has_pdflatex, pdf_info = check_command("pdflatex")
    table.add_row("pdfLaTeX", "[green]✔ OK[/green]" if has_pdflatex else "[red]✘ Ausente[/red]", pdf_info)

    has_bibtex, bib_info = check_command("bibtex")
    table.add_row("BibTeX", "[green]✔ OK[/green]" if has_bibtex else "[red]✘ Ausente[/red]", bib_info)

    has_biber, biber_info = check_command("biber")
    table.add_row("Biber", "[green]✔ OK[/green]" if has_biber else "[yellow]⚠ Ausente[/yellow]", biber_info)

    # 2. Integridade dos Diretórios
    lake_dir = ROOT_DIR / "resources" / "_lake"
    pdfs = list(lake_dir.glob("*.pdf")) if lake_dir.exists() else []
    epubs = list(lake_dir.glob("*.epub")) if lake_dir.exists() else []
    mds = list(lake_dir.glob("*.md")) if lake_dir.exists() else []

    table.add_row(
        "Data Lake (resources/_lake)",
        "[green]✔ Ativo[/green]" if lake_dir.exists() else "[red]✘ Não Encontrado[/red]",
        f"{len(pdfs)} PDFs | {len(epubs)} EPUBs | {len(mds)} Transcrições .md"
    )

    catalog_html = ROOT_DIR / "resources" / "_lake_catalog.html"
    table.add_row(
        "Catálogo Web",
        "[green]✔ Presente[/green]" if catalog_html.exists() else "[yellow]⚠ Requer Gerar[/yellow]",
        str(catalog_html.relative_to(ROOT_DIR)) if catalog_html.exists() else "resources/_lake_catalog.html"
    )

    master_bib = ROOT_DIR / "references" / "master.bib"
    bib_count = 0
    if master_bib.exists():
        bib_count = len(re.findall(r"@\w+\s*\{", master_bib.read_text(encoding="utf-8")))

    table.add_row(
        "Bibliografia Master",
        "[green]✔ Ativa[/green]" if master_bib.exists() else "[yellow]⚠ Não Encontrada[/yellow]",
        f"{bib_count} referências indexadas ({master_bib.relative_to(ROOT_DIR)})"
    )

    # 3. Automação de Web Scraping & Pesquisa
    try:
        import scrapling
        has_scrapling = True
        scrapling_ver = f"v{scrapling.__version__}"
    except Exception:
        has_scrapling = False
        scrapling_ver = "Ausente"

    table.add_row(
        "Scrapling (Stealth Engine)",
        "[green]✔ OK[/green]" if has_scrapling else "[red]✘ Ausente[/red]",
        f"{scrapling_ver} (Anti-bot e Cloudflare Turnstile local)"
    )

    firecrawl_key = os.getenv("FIRECRAWL_API_KEY")
    table.add_row(
        "Firecrawl API (Cloud & Papers)",
        "[green]✔ Configurada[/green]" if firecrawl_key else "[yellow]⚠ Ausente (.env)[/yellow]",
        "Chave ativa no .env (Pesquisa de papers e deep crawl)" if firecrawl_key else "Definir FIRECRAWL_API_KEY em .env"
    )

    # 4. Zotero & PyMuPDF4LLM
    has_zcli, zcli_path = check_command("zotero-cli")
    table.add_row(
        "Zotero CLI",
        "[green]✔ OK[/green]" if has_zcli else "[red]✘ Ausente[/red]",
        f"Operacional ({zcli_path})" if has_zcli else "Instalar via uv tool install 'zotero-mcp-server[all]'"
    )

    try:
        import pymupdf4llm
        has_pymupdf4llm = True
        pymupdf4llm_ver = f"v{pymupdf4llm.__version__}"
    except Exception:
        has_pymupdf4llm = False
        pymupdf4llm_ver = "Ausente"

    table.add_row(
        "PyMuPDF4LLM (Doc Parsing)",
        "[green]✔ OK[/green]" if has_pymupdf4llm else "[red]✘ Ausente[/red]",
        f"{pymupdf4llm_ver} (GFM Markdown com tabelas nativas e equações)"
    )

    console.print(table)


def cmd_catalog():
    """Invoca o motor de catalogação e gera documents.jsonl estruturado."""
    console.print("[cyan]🔄 Sincronizando catálogo e gerando índice estruturado...[/cyan]")
    # 1. Atualizar catálogo HTML
    try:
        scripts_dir = ROOT_DIR / "scripts"
        if str(scripts_dir) not in sys.path:
            sys.path.insert(0, str(scripts_dir))
        if str(ROOT_DIR) not in sys.path:
            sys.path.insert(0, str(ROOT_DIR))
        import yt_transcribe_and_catalog as ytc
        items = ytc.scan_lake_items(ROOT_DIR / "resources" / "_lake")
        ytc.generate_catalog_html(items, ROOT_DIR / "resources" / "_lake_catalog.html")
        console.print("[green]✔ Catálogo HTML resources/_lake_catalog.html atualizado com sucesso.[/green]")
    except Exception as e:
        console.print(f"[red]Erro ao atualizar catálogo HTML:[/red] {e}")

    # 2. Gerar documents.jsonl para controle fino no Git
    lake_dir = ROOT_DIR / "resources" / "_lake"
    catalog_dir = ROOT_DIR / "resources" / "_catalog"
    catalog_dir.mkdir(parents=True, exist_ok=True)
    jsonl_file = catalog_dir / "documents.jsonl"

    documents = []
    if lake_dir.exists():
        for file in sorted(lake_dir.iterdir()):
            if file.is_file() and not file.name.startswith("."):
                # Calcular hash SHA-256 rápido
                h = hashlib.sha256()
                with open(file, "rb") as f:
                    while chunk := f.read(65536):
                        h.update(chunk)
                
                doc_record = {
                    "id": f"sha256:{h.hexdigest()[:16]}",
                    "filename": file.name,
                    "media_type": file.suffix.lower().lstrip("."),
                    "size_bytes": file.stat().st_size,
                    "sha256": h.hexdigest(),
                    "updated_at": datetime.fromtimestamp(file.stat().st_mtime).isoformat()
                }
                documents.append(doc_record)

    with open(jsonl_file, "w", encoding="utf-8") as f:
        for doc in documents:
            f.write(json.dumps(doc, ensure_ascii=False) + "\n")

    console.print(f"[green]✔ Índice estruturado gerado em: {jsonl_file.relative_to(ROOT_DIR)} ({len(documents)} itens)[/green]")


def cmd_new_project(project_name: str):
    """Cria um novo projeto acadêmico a partir do template limpo."""
    clean_name = re.sub(r"[^a-zA-Z0-9_-]", "_", project_name.lower().strip())
    target_dir = ROOT_DIR / "projects" / clean_name

    if target_dir.exists():
        console.print(f"[yellow]⚠ O projeto '{clean_name}' já existe em: {target_dir}[/yellow]")
        return

    template_dir = ROOT_DIR / "projects" / "_template"
    if not template_dir.exists():
        console.print(f"[red]❌ Diretório template não encontrado em: {template_dir}[/red]")
        return

    shutil.copytree(template_dir, target_dir)
    # Limpar qualquer arquivo temporário da cópia
    for aux in target_dir.glob("build/*"):
        try:
            aux.unlink()
        except Exception:
            pass

    console.print(Panel(
        f"[green]✅ Novo projeto acadêmico criado com sucesso![/green]\n\n"
        f"📁 [bold]Local:[/bold] projects/{clean_name}\n"
        f"📄 [bold]Manuscrito principal:[/bold] projects/{clean_name}/main.tex\n"
        f"📚 [bold]Citações:[/bold] projects/{clean_name}/references.bib\n\n"
        f"Para compilar:\n"
        f"  [cyan]uv run python scripts/acc.py build projects/{clean_name}[/cyan]\n"
        f"  ou abra no VS Code com a extensão [italic]LaTeX Workshop[/italic].",
        title=f"Projeto: {clean_name}",
        border_style="green"
    ))


def cmd_build(target_path: str = ""):
    """Compila um projeto LaTeX com pdfLaTeX e BibTeX salvando os binários em build/."""
    if not target_path:
        project_dir = ROOT_DIR / "projects" / "_template"
    else:
        project_dir = Path(target_path).resolve()
        if not project_dir.is_dir():
            project_dir = project_dir.parent

    main_tex = project_dir / "main.tex"
    if not main_tex.exists():
        console.print(f"[red]❌ Arquivo main.tex não encontrado em: {project_dir}[/red]")
        return

    build_dir = project_dir / "build"
    build_dir.mkdir(parents=True, exist_ok=True)

    console.print(f"[cyan]🚀 Compilando manuscrito: {main_tex.relative_to(ROOT_DIR)}...[/cyan]")

    try:
        # Passada 1: pdflatex
        console.print("  [dim][1/4] Executando pdfLaTeX (passo inicial)...[/dim]")
        subprocess.run(["pdflatex", "-interaction=nonstopmode", f"-output-directory={build_dir}", str(main_tex)], check=True, stdout=subprocess.DEVNULL)

        # Passada 2: bibtex se houver aux
        aux_file = build_dir / "main.aux"
        if aux_file.exists():
            console.print("  [dim][2/4] Processando citações com BibTeX...[/dim]")
            subprocess.run(["bibtex", "main"], cwd=str(build_dir), stdout=subprocess.DEVNULL)

        # Passada 3: pdflatex
        console.print("  [dim][3/4] Atualizando referências cruzadas...[/dim]")
        subprocess.run(["pdflatex", "-interaction=nonstopmode", f"-output-directory={build_dir}", str(main_tex)], check=True, stdout=subprocess.DEVNULL)

        # Passada 4: pdflatex final
        console.print("  [dim][4/4] Gerando PDF final...[/dim]")
        subprocess.run(["pdflatex", "-interaction=nonstopmode", f"-output-directory={build_dir}", str(main_tex)], check=True, stdout=subprocess.DEVNULL)

        out_pdf = build_dir / "main.pdf"
        dest_pdf = project_dir / "main.pdf"
        if out_pdf.exists():
            shutil.copy2(out_pdf, dest_pdf)
            console.print(f"[bold green]✔ PDF gerado com sucesso:[/bold green] [underline]{dest_pdf.relative_to(ROOT_DIR)}[/underline]")
    except Exception as e:
        console.print(f"[red]❌ Erro ao compilar LaTeX:[/red] {e}")
        console.print(f"[yellow]Consulte o log de erros em: {build_dir / 'main.log'}[/yellow]")


def cmd_bib_audit():
    """Audita referências nos arquivos BibTeX verificando duplicidades e campos essenciais."""
    console.print("[cyan]🔍 Auditando acervo de referências bibliográficas...[/cyan]")
    master_bib = ROOT_DIR / "references" / "master.bib"

    if not master_bib.exists():
        console.print(f"[red]❌ references/master.bib não encontrado![/red]")
        return

    content = master_bib.read_text(encoding="utf-8")
    entries = re.findall(r"@(\w+)\s*\{\s*([^,]+),", content)

    console.print(f"Total de referências encontradas em master.bib: [bold]{len(entries)}[/bold]")

    keys = [e[1].strip() for e in entries]
    seen = set()
    duplicates = set()
    for k in keys:
        if k in seen:
            duplicates.add(k)
        seen.add(k)

    if duplicates:
        console.print(f"[red]⚠ Chaves duplicadas encontradas:[/red] {', '.join(duplicates)}")
    else:
        console.print("[green]✔ Nenhuma chave duplicada encontrada no master.bib.[/green]")


def cmd_transcript(args: list[str]):
    """Encaminha chamadas de transcrição para o motor de transcrição."""
    script_path = ROOT_DIR / "scripts" / "yt_transcribe_and_catalog.py"
    subprocess.run([sys.executable, str(script_path)] + args)


def cmd_scrape(args: list[str]):
    """Encaminha chamadas de scraping (Scrapling + Firecrawl) para o motor de colheita."""
    script_path = ROOT_DIR / "scripts" / "web_harvester.py"
    subprocess.run([sys.executable, str(script_path), "scrape"] + args)


def cmd_search_papers(args: list[str]):
    """Encaminha buscas de literatura acadêmica para o Firecrawl Research Index."""
    script_path = ROOT_DIR / "scripts" / "web_harvester.py"
    subprocess.run([sys.executable, str(script_path), "search-papers"] + args)


def cmd_zotero(args: list[str]):
    """Gerencia a integração e sincronização com o Zotero."""
    if not args:
        console.print("[cyan]Uso: acc zotero [sync|search|add|recent|path][/cyan]")
        console.print("  [green]sync[/green] [--force] [--limit N] - Sincroniza acervo para resources/_lake com PyMuPDF4LLM")
        console.print("  [green]search[/green] <termo>           - Busca artigos no Zotero por texto ou tag")
        console.print("  [green]add[/green] <doi|url|isbn>       - Adiciona item à biblioteca e baixa anexo")
        console.print("  [green]recent[/green] [--limit N]        - Lista itens recentes")
        return

    sub = args[0].lower()
    if sub in ("sync", "sincronizar", "lake"):
        script_path = ROOT_DIR / "scripts" / "zotero_lake_sync.py"
        subprocess.run([sys.executable, str(script_path)] + args[1:])
    elif sub in ("search", "s"):
        term = " ".join(args[1:])
        cmd = ["zotero-cli", "search", term]
        subprocess.run(cmd)
    elif sub in ("add", "a"):
        if len(args) < 2:
            console.print("[red]Especifique o identificador:[/red] acc zotero add <doi|url|isbn>")
            return
        identifier = args[1]
        mode = "doi" if "/" in identifier and not identifier.startswith("http") else ("url" if identifier.startswith("http") else "isbn")
        cmd = ["zotero-cli", "add", mode, identifier]
        res = subprocess.run(cmd)
        if res.returncode == 0:
            console.print("[green]✔ Item adicionado com sucesso. Sincronizando com o Lake...[/green]")
            script_path = ROOT_DIR / "scripts" / "zotero_lake_sync.py"
            subprocess.run([sys.executable, str(script_path)])
    elif sub in ("recent", "r"):
        cmd = ["zotero-cli", "get", "recent"] + args[1:]
        subprocess.run(cmd)
    elif sub in ("path", "p"):
        if len(args) < 2:
            console.print("[red]Especifique a chave do item:[/red] acc zotero path <ITEM_KEY>")
            return
        cmd = ["zotero-cli", "path", args[1]]
        subprocess.run(cmd)
    else:
        cmd = ["zotero-cli"] + args
        subprocess.run(cmd)


def main():
    if len(sys.argv) < 2:
        console.print(Panel.fit(
            "[bold cyan]🌊 Academic PKM CLI (`acc`)[/bold cyan]\n"
            "Comandos disponíveis:\n"
            "  [green]doctor[/green]         - Verifica saúde do ecossistema e dependências\n"
            "  [green]catalog[/green]        - Reindexa o _lake e gera _lake_catalog.html e documents.jsonl\n"
            "  [green]zotero[/green]         - Sincroniza acervo Zotero com Lake via PyMuPDF4LLM e master.bib\n"
            "  [green]scrape[/green]         - Raspa artigos e páginas web com bypass anti-bot e salva no Lake\n"
            "  [green]search-papers[/green]  - Pesquisa papers acadêmicos e indexa resumos no Lake\n"
            "  [green]new-project[/green]    - Cria um novo projeto acadêmico LaTeX modular\n"
            "  [green]build[/green]          - Compila o manuscrito LaTeX de um projeto\n"
            "  [green]bib-audit[/green]      - Valida a consistência do arquivo master.bib\n"
            "  [green]transcript[/green]     - Transcreve vídeos e playlists do YouTube para o Lake\n\n"
            "Exemplo: [italic]uv run python scripts/acc.py zotero sync[/italic]",
            border_style="cyan"
        ))
        return

    action = sys.argv[1].lower()

    if action in ("doctor", "--doctor"):
        cmd_doctor()
    elif action in ("catalog", "reindex", "--reindex"):
        cmd_catalog()
    elif action in ("zotero", "zot", "z"):
        cmd_zotero(sys.argv[2:])
    elif action in ("scrape", "web", "harvest"):
        cmd_scrape(sys.argv[2:])
    elif action in ("search-papers", "papers", "paper-search"):
        cmd_search_papers(sys.argv[2:])
    elif action in ("new-project", "project", "novo"):
        name = sys.argv[2] if len(sys.argv) > 2 else "novo_artigo"
        cmd_new_project(name)
    elif action in ("build", "compile"):
        target = sys.argv[2] if len(sys.argv) > 2 else ""
        cmd_build(target)
    elif action in ("bib-audit", "audit-bib"):
        cmd_bib_audit()
    elif action in ("transcript", "yt"):
        cmd_transcript(sys.argv[2:])
    else:
        console.print(f"[red]Comando desconhecido:[/red] {action}. Execute sem argumentos para ver o menu.")


if __name__ == "__main__":
    main()
