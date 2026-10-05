
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
    """Verifica se um executável está disponível no PATH do sistema ou locais conhecidos."""
    path = shutil.which(cmd)
    if not path:
        local_app = os.environ.get("LOCALAPPDATA", "")
        prog_files = os.environ.get("ProgramFiles", "")
        prog_files_x86 = os.environ.get("ProgramFiles(x86)", "")
        candidates = [
            Path(local_app) / "Pandoc" / f"{cmd}.exe",
            Path(prog_files) / "Pandoc" / f"{cmd}.exe",
            Path(prog_files_x86) / "Pandoc" / f"{cmd}.exe",
            Path(local_app) / "Programs" / "Pandoc" / f"{cmd}.exe",
        ]
        for c in candidates:
            if c.exists():
                p_dir = str(c.parent)
                if p_dir not in os.environ.get("PATH", ""):
                    os.environ["PATH"] = f"{p_dir};{os.environ.get('PATH', '')}"
                return True, str(c)
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

    has_pandoc, pandoc_info = check_command("pandoc")
    table.add_row("Pandoc (Doc Converter)", "[green]✔ OK[/green]" if has_pandoc else "[yellow]⚠ Opcional[/yellow]", pandoc_info)

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

    # 5. Consensus Research MCP & API
    consensus_key = os.getenv("CONSENSUS_API_KEY")
    mcp_auth_dir = Path.home() / ".mcp-auth"
    has_oauth = any(mcp_auth_dir.glob("mcp-remote*")) if mcp_auth_dir.exists() else False

    table.add_row(
        "Consensus Research (MCP / API)",
        "[green]✔ Configurado[/green]" if (consensus_key or has_oauth) else "[yellow]⚠ Requer Auth/Key[/yellow]",
        "Chave CONSENSUS_API_KEY ativa" if consensus_key else ("OAuth configurado em ~/.mcp-auth" if has_oauth else "Executar: uv run python scripts/consensus.py auth")
    )

    # 6. Diagramação Visual Científica (Diagrams.net / Draw.io)
    try:
        from drawio_manager import check_drawio_environment
        drawio_env = check_drawio_environment()
        has_drawio_cli = bool(drawio_env.get("cli_path"))
        drawio_ver = drawio_env.get("cli_version") or "Ativo"
        has_drawio_ext = bool(drawio_env.get("vscode_extension"))
        has_drawio_mcp = bool(drawio_env.get("mcp_registered"))

        table.add_row(
            "Draw.io Desktop CLI",
            f"[green]✔ OK ({drawio_ver})[/green]" if has_drawio_cli else "[yellow]⚠ Ausente[/yellow]",
            f"Exportador SVG/PDF com XML embutido ({drawio_env['cli_path']})" if has_drawio_cli else "Instalar via winget install JGraph.Draw"
        )
        table.add_row(
            "Diagrams.net MCP (@drawio/mcp)",
            "[green]✔ Configurado[/green]" if has_drawio_mcp else "[yellow]⚠ Requer Config[/yellow]",
            "Servidor MCP ativo em ~/.gemini/config/mcp_config.json" if has_drawio_mcp else "Adicionar @drawio/mcp ao mcp_config.json"
        )
        table.add_row(
            "VS Code Draw.io Integration",
            "[green]✔ Instalada[/green]" if has_drawio_ext else "[yellow]⚠ Não Detectada[/yellow]",
            "Extensão hediet.vscode-drawio para edição in-editor" if has_drawio_ext else "Instalar: code --install-extension hediet.vscode-drawio"
        )
    except Exception as e:
        table.add_row("Diagrams.net / Draw.io", "[yellow]⚠ Verificação Falhou[/yellow]", str(e))

    console.print(table)


def cmd_catalog():
    """Invoca o motor de catalogação e gera documents.jsonl estruturado."""
    console.print("[cyan]🔄 Sincronizando catálogo e gerando índice estruturado...[/cyan]")
    try:
        from core.catalog_service import reindex_catalog
        res = reindex_catalog()
        console.print(f"[green]✔ Catálogo HTML e índice estruturado atualizados ({res['total_items']} itens).[/green]")
        console.print(f"  [dim]HTML:[/dim] {res['html_path'].relative_to(ROOT_DIR)}")
        console.print(f"  [dim]JSONL:[/dim] {res['jsonl_path'].relative_to(ROOT_DIR)}")
    except Exception as e:
        console.print(f"[red]Erro ao atualizar catálogo:[/red] {e}")


def cmd_new_project(project_name: str, template: str = "sbc"):
    """Cria um novo projeto acadêmico a partir dos templates (sbc, tcc/abnt, simple)."""
    clean_name = re.sub(r"[^a-zA-Z0-9_-]", "_", project_name.lower().strip())
    target_dir = ROOT_DIR / "projects" / clean_name

    if target_dir.exists():
        console.print(f"[yellow]⚠ O projeto '{clean_name}' já existe em: {target_dir}[/yellow]")
        return

    tmpl = template.lower().strip()
    if tmpl in ("tcc", "abnt", "tese", "monografia"):
        source_dir = ROOT_DIR / "templates" / "tcc_abnt"
        tmpl_desc = "TCC / Monografia ABNT (IFMA modular)"
    elif tmpl in ("sbc", "artigo", "paper"):
        source_dir = ROOT_DIR / "templates" / "artigo_sbc"
        tmpl_desc = "Artigo Científico SBC (Sociedade Brasileira de Computação)"
    elif tmpl in ("simple", "basico"):
        source_dir = ROOT_DIR / "projects" / "_template"
        tmpl_desc = "Manuscrito Básico Simples"
    else:
        cand = ROOT_DIR / "templates" / tmpl
        if cand.exists():
            source_dir = cand
            tmpl_desc = f"Template Personalizado ({tmpl})"
        else:
            console.print(f"[yellow]Template '{tmpl}' não reconhecido. Usando SBC por padrão.[/yellow]")
            source_dir = ROOT_DIR / "templates" / "artigo_sbc"
            tmpl_desc = "Artigo Científico SBC"

    if not source_dir.exists():
        console.print(f"[red]❌ Diretório template não encontrado em: {source_dir}[/red]")
        return

    shutil.copytree(source_dir, target_dir)
    # Limpar qualquer pasta build ou artefatos temporários
    build_dir = target_dir / "build"
    if build_dir.exists():
        shutil.rmtree(build_dir, ignore_errors=True)
    for aux in target_dir.rglob("*-converted-to.pdf"):
        try:
            aux.unlink()
        except Exception:
            pass

    console.print(Panel(
        f"[green]✅ Novo projeto acadêmico criado com sucesso![/green]\n\n"
        f"📋 [bold]Template Utilizado:[/bold] {tmpl_desc}\n"
        f"📁 [bold]Local:[/bold] projects/{clean_name}\n"
        f"📄 [bold]Manuscrito principal:[/bold] projects/{clean_name}/main.tex\n\n"
        f"Para compilar:\n"
        f"  [cyan]uv run python scripts/acc.py build projects/{clean_name}[/cyan]\n"
        f"Para empacotar para o Overleaf:\n"
        f"  [cyan]uv run python scripts/acc.py overleaf pack projects/{clean_name}[/cyan]\n"
        f"Ou abra no VS Code com a extensão [italic]LaTeX Workshop[/italic] ([bold]Ctrl+Alt+B[/bold]).",
        title=f"Projeto: {clean_name}",
        border_style="green"
    ))


def cmd_build(target_path: str = ""):
    """Compila um projeto LaTeX usando latexmk (com detecção de Perl e SyncTeX) salvando binários em build/."""
    if not target_path:
        projects_dir = ROOT_DIR / "projects"
        subdirs = [p for p in projects_dir.iterdir() if p.is_dir() and not p.name.startswith("_") and (p / "main.tex").exists()]
        if subdirs:
            project_dir = subdirs[0]
        else:
            project_dir = ROOT_DIR / "templates" / "artigo_sbc"
    else:
        project_dir = Path(target_path).resolve()
        if not project_dir.is_dir():
            project_dir = project_dir.parent

    main_tex = project_dir / "main.tex"
    if not main_tex.exists():
        tex_files = list(project_dir.glob("*.tex"))
        if tex_files:
            main_tex = tex_files[0]
        else:
            console.print(f"[red]❌ Nenhum arquivo .tex encontrado em: {project_dir}[/red]")
            return

    build_dir = project_dir / "build"
    build_dir.mkdir(parents=True, exist_ok=True)

    rel_tex = main_tex.relative_to(ROOT_DIR) if main_tex.is_relative_to(ROOT_DIR) else main_tex
    console.print(f"[cyan]🚀 Compilando manuscrito: [bold]{rel_tex}[/bold]...[/cyan]")

    # Configurar ambiente com Git Perl para latexmk no Windows
    env = os.environ.copy()
    git_usr_bin = r"C:\Program Files\Git\usr\bin"
    if os.path.exists(git_usr_bin) and git_usr_bin not in env.get("PATH", ""):
        env["PATH"] = git_usr_bin + os.pathsep + env.get("PATH", "")

    has_latexmk, _ = check_command("latexmk")

    if has_latexmk:
        cmd = [
            "latexmk",
            "-pdf",
            "-interaction=nonstopmode",
            "-file-line-error",
            "-synctex=1",
            f"-output-directory={build_dir.name}",
            f"-pdflatex=pdflatex -interaction=nonstopmode --enable-installer -synctex=1 %O %S",
            main_tex.name
        ]
        console.print(f"  [dim]Executando: latexmk (resolução automática de passadas e pacotes MiKTeX)[/dim]")
        res = subprocess.run(cmd, cwd=str(project_dir), env=env, capture_output=True, text=True, errors="ignore")

        pdf_name = main_tex.stem + ".pdf"
        out_pdf = build_dir / pdf_name
        dest_pdf = project_dir / pdf_name

        if res.returncode == 0 and out_pdf.exists():
            shutil.copy2(out_pdf, dest_pdf)
            rel_pdf = dest_pdf.relative_to(ROOT_DIR) if dest_pdf.is_relative_to(ROOT_DIR) else dest_pdf
            file_url = dest_pdf.as_uri()
            console.print(f"[bold green]✔ PDF gerado com sucesso:[/bold green] [link={file_url}]{rel_pdf}[/link]")
            return
        else:
            log_file = build_dir / (main_tex.stem + ".log")
            if log_file.exists():
                console.print(f"[yellow]Diagnosticando log de compilação ({log_file.name}):[/yellow]")
                errors = []
                for line in log_file.read_text(encoding="utf-8", errors="ignore").splitlines():
                    if line.startswith("!") or "Error:" in line or "Fatal error" in line:
                        errors.append(line)
                for err in errors[:6]:
                    console.print(f"  [red]{err}[/red]")
            console.print(f"[red]❌ Falha na compilação latexmk. Código de saída: {res.returncode}[/red]")
            return

    # Fallback se latexmk não estiver disponível: pdflatex + bibtex tradicional
    console.print("  [dim]latexmk não disponível, usando fallback pdflatex + bibtex...[/dim]")
    try:
        subprocess.run(["pdflatex", "-interaction=nonstopmode", "--enable-installer", f"-output-directory={build_dir}", str(main_tex)], check=True, stdout=subprocess.DEVNULL)
        aux_file = build_dir / f"{main_tex.stem}.aux"
        if aux_file.exists():
            subprocess.run(["bibtex", main_tex.stem], cwd=str(build_dir), stdout=subprocess.DEVNULL)
        subprocess.run(["pdflatex", "-interaction=nonstopmode", "--enable-installer", f"-output-directory={build_dir}", str(main_tex)], check=True, stdout=subprocess.DEVNULL)
        subprocess.run(["pdflatex", "-interaction=nonstopmode", "--enable-installer", f"-output-directory={build_dir}", str(main_tex)], check=True, stdout=subprocess.DEVNULL)

        pdf_name = main_tex.stem + ".pdf"
        out_pdf = build_dir / pdf_name
        dest_pdf = project_dir / pdf_name
        if out_pdf.exists():
            shutil.copy2(out_pdf, dest_pdf)
            console.print(f"[bold green]✔ PDF gerado com sucesso:[/bold green] {dest_pdf}")
    except Exception as e:
        console.print(f"[red]❌ Erro ao compilar LaTeX via fallback:[/red] {e}")


def cmd_overleaf(args: list[str]):
    """Gerencia comandos de ponte e colaboração com o Overleaf."""
    script_path = ROOT_DIR / "scripts" / "overleaf_bridge.py"
    subprocess.run([sys.executable, str(script_path)] + args)



def cmd_bib_audit():
    """Audita referências nos arquivos BibTeX verificando duplicidades e campos essenciais."""
    console.print("[cyan]🔍 Auditando acervo de referências bibliográficas...[/cyan]")
    try:
        from core.bibtex_service import audit_master_bib
        audit = audit_master_bib()
        console.print(f"Total de referências encontradas em master.bib: [bold]{audit['total_entries']}[/bold] (Únicas: {audit['unique_keys']})")

        if audit["duplicate_keys"]:
            console.print(f"[red]⚠️ Chaves duplicadas encontradas:[/red] {', '.join(audit['duplicate_keys'])}")
        else:
            console.print("[green]✔ Nenhuma chave duplicada encontrada no master.bib.[/green]")

        if audit["missing_author"]:
            console.print(f"[yellow]ℹ️ Referências sem campo 'author':[/yellow] {len(audit['missing_author'])}")
    except Exception as e:
        console.print(f"[red]Erro ao auditar master.bib:[/red] {e}")


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


def cmd_consensus(args: list[str]):
    """Encaminha consultas científicas para o motor Consensus."""
    script_path = ROOT_DIR / "scripts" / "consensus.py"
    subprocess.run([sys.executable, str(script_path)] + args)


def cmd_fleet(args: list[str]):
    """Encaminha consultas científicas para a mini-frota de pesquisa acadêmica."""
    script_path = ROOT_DIR / "scripts" / "academic_fleet.py"
    subprocess.run([sys.executable, str(script_path)] + args)


def cmd_convert(args: list[str]):
    """Encaminha comandos de conversão para o conversor Pandoc (DOCX, PDF, LaTeX)."""
    script_path = ROOT_DIR / "scripts" / "pandoc_converter.py"
    subprocess.run([sys.executable, str(script_path)] + args)


def cmd_protocol(args: list[str]):
    """Encaminha comandos de protocolo de revisão sistemática."""
    script_path = ROOT_DIR / "scripts" / "systematic_review.py"
    subprocess.run([sys.executable, str(script_path), "protocol"] + args)


def cmd_matrix(args: list[str]):
    """Encaminha comandos de matriz de extração e triagem."""
    script_path = ROOT_DIR / "scripts" / "systematic_review.py"
    subprocess.run([sys.executable, str(script_path), "matrix"] + args)


def cmd_drawio(args: list[str]):
    """Encaminha comandos de diagramas visuais para o Draw.io Manager."""
    script_path = ROOT_DIR / "scripts" / "drawio_manager.py"
    subprocess.run([sys.executable, str(script_path)] + args)


def main():
    if len(sys.argv) < 2:
        console.print(Panel.fit(
            "[bold cyan]🌊 Academic PKM CLI (`acc`)[/bold cyan]\n"
            "Comandos disponíveis:\n"
            "  [green]doctor[/green]         - Verifica saúde do ecossistema e dependências\n"
            "  [green]catalog[/green]        - Reindexa o _lake e gera _lake_catalog.html e documents.jsonl\n"
            "  [green]convert[/green]        - Converte documentos acadêmicos via Pandoc (Markdown ⇄ DOCX ⇄ LaTeX)\n"
            "  [green]fleet[/green]          - Consulta mini-frota concorrente (arXiv, OpenAlex, S2, CrossRef, etc.)\n"
            "  [green]protocol[/green]       - Cria protocolo formal de revisão sistemática (PRISMA-P / PICO / SPIDER)\n"
            "  [green]matrix[/green]         - Gera matriz de extração e triagem (Markdown & CSV) de buscas do Lake\n"
            "  [green]diagram[/green]        - Automação Diagrams.net / Draw.io (status, export, url, template, search)\n"
            "  [green]consensus[/green]      - Pesquisa no Consensus.app (medidor de consenso e 200M+ papers)\n"
            "  [green]zotero[/green]         - Sincroniza acervo Zotero com Lake via PyMuPDF4LLM e master.bib\n"
            "  [green]scrape[/green]         - Raspa artigos e páginas web com bypass anti-bot e salva no Lake\n"
            "  [green]search-papers[/green]  - Pesquisa papers acadêmicos e indexa resumos no Lake\n"
            "  [green]new-project[/green]    - Cria um novo projeto LaTeX modular (--template sbc|tcc)\n"
            "  [green]build[/green]          - Compila o manuscrito LaTeX de um projeto com latexmk\n"
            "  [green]overleaf[/green]       - Ponte Overleaf: pack, unpack, sync-bib e git-info\n"
            "  [green]bib-audit[/green]      - Valida a consistência do arquivo master.bib\n"
            "  [green]transcript[/green]     - Transcreve vídeos e playlists do YouTube para o Lake\n\n"
            "Exemplo: [italic]uv run python scripts/acc.py diagram export resources/templates/drawio/prisma_2020.drawio -f svg[/italic]",
            border_style="cyan"
        ))
        return

    action = sys.argv[1].lower()

    if action in ("doctor", "--doctor"):
        cmd_doctor()
    elif action in ("catalog", "reindex", "--reindex"):
        cmd_catalog()
    elif action in ("convert", "conv", "pandoc"):
        cmd_convert(sys.argv[2:])
    elif action in ("fleet", "fl", "frota"):
        cmd_fleet(sys.argv[2:])
    elif action in ("protocol", "proto", "prisma"):
        cmd_protocol(sys.argv[2:])
    elif action in ("matrix", "mat", "triagem"):
        cmd_matrix(sys.argv[2:])
    elif action in ("diagram", "diag", "drawio", "draw"):
        cmd_drawio(sys.argv[2:])
    elif action in ("providers", "provider", "provedores"):
        cmd_fleet(["--list-providers"] + sys.argv[2:])
    elif action in ("consensus", "cons", "c"):
        cmd_consensus(sys.argv[2:])
    elif action in ("zotero", "zot", "z"):
        cmd_zotero(sys.argv[2:])
    elif action in ("scrape", "web", "harvest"):
        cmd_scrape(sys.argv[2:])
    elif action in ("search-papers", "papers", "paper-search"):
        cmd_search_papers(sys.argv[2:])
    elif action in ("new-project", "project", "novo"):
        name = sys.argv[2] if len(sys.argv) > 2 else "novo_artigo"
        template = "sbc"
        if len(sys.argv) > 4 and sys.argv[3] in ("--template", "-t"):
            template = sys.argv[4]
        elif len(sys.argv) > 3 and not sys.argv[2].startswith("-"):
            template = sys.argv[3]
        cmd_new_project(name, template)
    elif action in ("build", "compile"):
        target = sys.argv[2] if len(sys.argv) > 2 else ""
        cmd_build(target)
    elif action in ("overleaf", "ov"):
        cmd_overleaf(sys.argv[2:])
    elif action in ("latex", "tex"):
        sub = sys.argv[2].lower() if len(sys.argv) > 2 else "build"
        if sub in ("build", "b", "compile"):
            cmd_build(sys.argv[3] if len(sys.argv) > 3 else "")
        elif sub in ("new", "novo"):
            name = sys.argv[3] if len(sys.argv) > 3 else "novo_artigo"
            tmpl = sys.argv[4] if len(sys.argv) > 4 else "sbc"
            cmd_new_project(name, tmpl)
        elif sub in ("pack", "unpack", "sync-bib", "git-info"):
            cmd_overleaf(sys.argv[2:])
        else:
            cmd_build(sys.argv[2])
    elif action in ("bib-audit", "audit-bib"):
        cmd_bib_audit()
    elif action in ("transcript", "yt"):
        cmd_transcript(sys.argv[2:])
    else:
        console.print(f"[red]Comando desconhecido:[/red] {action}. Execute sem argumentos para ver o menu.")


if __name__ == "__main__":
    main()

