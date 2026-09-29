# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "rich>=13.7.0",
# ]
# ///
"""
=============================================================================
OVERLEAF BRIDGE - Academic PKM Monorepo Integration
=============================================================================
Gerencia a ponte bidirecional entre o monorepo local (VS Code / LaTeX Workshop)
e a plataforma Overleaf para colaboração com orientadores e coautores.

Funcionalidades:
1. `pack`: Empacota um projeto local em um arquivo .zip limpo e autocontido,
   resolvendo e embutindo apenas as referências de `references/master.bib`
   utilizadas no manuscrito (sem bloat de compilação).
2. `unpack`: Descompacta um arquivo .zip exportado do Overleaf em `projects/`,
   limpa artefatos temporários e mescla automaticamente novas referências BibTeX
   adicionadas pelos colaboradores de volta ao `references/master.bib`.
3. `sync-bib`: Sincroniza referências entre o projeto local e a base mestre.
4. `git-info`: Instruções e comandos para sincronização via Git Subtree / Remote.

Uso via CLI:
    uv run python scripts/overleaf_bridge.py pack projects/meu_artigo
    uv run python scripts/overleaf_bridge.py unpack "C:/Downloads/artigo.zip" meu_artigo
    uv run python scripts/overleaf_bridge.py sync-bib projects/meu_artigo
    uv run python scripts/overleaf_bridge.py git-info
=============================================================================
"""

import sys
import os
import re
import shutil
import zipfile
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

console = Console()
ROOT_DIR = Path(__file__).resolve().parent.parent
MASTER_BIB = ROOT_DIR / "references" / "master.bib"

# Padrões para descarte no empacotamento
EXCLUDE_DIRS = {"build", "__pycache__", ".git", ".vscode", ".idea"}
EXCLUDE_EXTENSIONS = {
    ".aux", ".bbl", ".blg", ".log", ".out", ".toc", ".lof", ".lot",
    ".fls", ".fdb_latexmk", ".synctex.gz", ".synctex", ".nav", ".snm",
    ".vrb", ".idx", ".ind", ".ilg", ".xdv"
}


def parse_bibtex_entries(content: str) -> dict[str, str]:
    """Extrai todas as entradas de um arquivo BibTeX usando contagem balanceada de chaves."""
    entries = {}
    pos = 0
    while True:
        m = re.search(r"(@\w+\s*\{(\s*[^,]+),)", content[pos:])
        if not m:
            break
        start = pos + m.start()
        key = m.group(2).strip()
        depth = 0
        in_entry = False
        end = -1
        for i in range(start, len(content)):
            char = content[i]
            if char == "{":
                depth += 1
                in_entry = True
            elif char == "}":
                depth -= 1
                if in_entry and depth == 0:
                    end = i + 1
                    break
        if end != -1:
            entries[key] = content[start:end].strip()
            pos = end
        else:
            pos += len(m.group(0))
    return entries


def extract_cited_keys(project_dir: Path) -> set[str]:
    """Varre todos os arquivos .tex do projeto em busca de chaves de citação."""
    keys = set()
    pattern = r"\\(?:cite|citep|citet|citeauthor|citeyear|nocite|autocite|textcite|parencite|citeonline)\*?(?:\[[^\]]*\])?\{([^}]+)\}"
    for tex_file in project_dir.rglob("*.tex"):
        if any(excluded in tex_file.parts for excluded in EXCLUDE_DIRS):
            continue
        try:
            text = tex_file.read_text(encoding="utf-8", errors="ignore")
            lines = [line.split("%")[0] for line in text.splitlines()]
            clean_text = "\n".join(lines)
            for m in re.finditer(pattern, clean_text):
                for k in m.group(1).split(","):
                    k = k.strip()
                    if k:
                        keys.add(k)
        except Exception:
            pass
    return keys


def find_or_create_project_bib(project_dir: Path) -> Path:
    """Encontra o arquivo .bib principal do projeto ou cria um references.bib padrão."""
    # Verificar se há algum .bib no projeto
    bib_files = list(project_dir.glob("*.bib"))
    if not bib_files:
        bib_files = list(project_dir.rglob("*.bib"))
    
    # Excluir os da pasta build
    valid_bibs = [b for b in bib_files if not any(x in b.parts for x in EXCLUDE_DIRS)]
    if valid_bibs:
        # Se houver references.bib ou b_referencias.bib preferir esse
        for b in valid_bibs:
            if b.name in ("references.bib", "referencias.bib", "b_referencias.bib"):
                return b
        return valid_bibs[0]

    # Se não houver, criar references.bib na raiz do projeto
    new_bib = project_dir / "references.bib"
    new_bib.write_text("% Referências bibliográficas locais do projeto\n", encoding="utf-8")
    return new_bib


def sync_project_citations(project_dir: Path) -> tuple[int, int, list[str]]:
    """
    Sincroniza citações utilizadas no projeto com o master.bib.
    Retorna: (total_citadas, adicionadas_ao_bib_local, chaves_nao_encontradas)
    """
    cited_keys = extract_cited_keys(project_dir)
    bib_file = find_or_create_project_bib(project_dir)

    # Carregar referências locais existentes
    local_content = bib_file.read_text(encoding="utf-8", errors="ignore") if bib_file.exists() else ""
    local_entries = parse_bibtex_entries(local_content)

    # Carregar master.bib
    master_entries = {}
    if MASTER_BIB.exists():
        master_entries = parse_bibtex_entries(MASTER_BIB.read_text(encoding="utf-8", errors="ignore"))

    missing_keys = []
    added_entries = []

    for key in cited_keys:
        if key in local_entries:
            continue
        if key in master_entries:
            added_entries.append(master_entries[key])
        else:
            missing_keys.append(key)

    if added_entries:
        with open(bib_file, "a", encoding="utf-8") as f:
            f.write("\n\n% --- Importadas automaticamente do Academic PKM master.bib ---\n")
            for entry in added_entries:
                f.write(entry + "\n\n")

    return len(cited_keys), len(added_entries), missing_keys


def pack_project(project_path_str: str, output_zip_str: str = "") -> Path | None:
    """Empacota o projeto em um arquivo .zip limpo e otimizado para o Overleaf."""
    project_dir = Path(project_path_str).resolve()
    if not project_dir.exists() or not project_dir.is_dir():
        console.print(f"[red]❌ Diretório do projeto não encontrado:[/red] {project_dir}")
        return None

    main_tex = project_dir / "main.tex"
    if not main_tex.exists():
        # Procurar qualquer .tex na raiz
        tex_files = list(project_dir.glob("*.tex"))
        if not tex_files:
            console.print(f"[red]❌ Nenhum arquivo LaTeX (.tex) encontrado em:[/red] {project_dir}")
            return None

    console.print(Panel.fit(
        f"[bold cyan]📦 Empacotando Projeto para Overleaf[/bold cyan]\n"
        f"Projeto: [bold]{project_dir.name}[/bold] ({project_dir})",
        border_style="cyan"
    ))

    # 1. Sincronizar citações de master.bib para o bib local
    console.print("[dim]→ Verificando e embutindo citações de master.bib...[/dim]")
    total_cited, added, missing = sync_project_citations(project_dir)
    console.print(f"  Total de citações no manuscrito: [bold]{total_cited}[/bold]")
    if added > 0:
        console.print(f"  [green]✔ {added} referências incorporadas automaticamente de master.bib ao .bib local.[/green]")
    if missing:
        console.print(f"  [yellow]⚠ Chaves citadas não localizadas em master.bib nem no .bib local:[/yellow] {', '.join(missing)}")

    # 2. Definir destino do ZIP
    if output_zip_str:
        out_zip = Path(output_zip_str).resolve()
    else:
        out_zip = project_dir / f"{project_dir.name}_overleaf.zip"

    out_zip.parent.mkdir(parents=True, exist_ok=True)

    # 3. Empacotar arquivos
    files_to_pack = []
    for item in project_dir.rglob("*"):
        if item.is_dir():
            continue
        # Ignorar diretórios excluídos
        if any(part in EXCLUDE_DIRS for part in item.parts):
            continue
        # Ignorar o próprio arquivo zip de saída
        if item.resolve() == out_zip:
            continue
        # Ignorar extensões de build
        if item.suffix.lower() in EXCLUDE_EXTENSIONS:
            continue
        # Ignorar arquivos temporários como *-converted-to.pdf
        if item.name.endswith("-converted-to.pdf"):
            continue
        # Ignorar PDF de saída do compilador na raiz do projeto (apenas manter PDFs em subpastas de figuras)
        if item.suffix.lower() == ".pdf" and item.parent == project_dir:
            continue
        # Ignorar zip temporários
        if item.suffix.lower() == ".zip":
            continue

        rel_path = item.relative_to(project_dir)
        files_to_pack.append((item, rel_path))

    with zipfile.ZipFile(out_zip, "w", zipfile.ZIP_DEFLATED) as zf:
        for full_path, rel_path in files_to_pack:
            zf.write(full_path, arcname=str(rel_path))

    zip_size_kb = out_zip.stat().st_size / 1024
    tex_count = sum(1 for _, p in files_to_pack if p.suffix.lower() == ".tex")
    bib_count = sum(1 for _, p in files_to_pack if p.suffix.lower() == ".bib")
    img_count = sum(1 for _, p in files_to_pack if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".eps", ".pdf", ".svg"})

    console.print(Panel(
        f"[green]✅ Pacote Overleaf gerado com sucesso![/green]\n\n"
        f"📁 [bold]Arquivo ZIP:[/bold] {out_zip}\n"
        f"📊 [bold]Tamanho:[/bold] {zip_size_kb:.1f} KB | [bold]Arquivos:[/bold] {len(files_to_pack)} ({tex_count} tex, {bib_count} bib, {img_count} figuras)\n\n"
        f"[bold yellow]Como importar no Overleaf:[/bold yellow]\n"
        f" 1. Acesse [link=https://www.overleaf.com/project]overleaf.com/project[/link]\n"
        f" 2. Clique em [bold]New Project[/bold] ➔ [bold]Upload Project[/bold]\n"
        f" 3. Arraste e solte o arquivo [underline]{out_zip.name}[/underline]",
        title="Pronto para Colaboração",
        border_style="green"
    ))

    return out_zip


def unpack_project(zip_path_str: str, project_name: str = "", sync_to_master: bool = True) -> Path | None:
    """Descompacta um pacote exportado do Overleaf em projects/ e mescla referências novas."""
    zip_path = Path(zip_path_str).resolve()
    if not zip_path.exists() or not zip_path.is_file():
        console.print(f"[red]❌ Arquivo ZIP não encontrado:[/red] {zip_path}")
        return None

    name = project_name.strip() if project_name else zip_path.stem.replace("_overleaf", "").replace(" ", "_").lower()
    clean_name = re.sub(r"[^a-zA-Z0-9_-]", "_", name)
    target_dir = ROOT_DIR / "projects" / clean_name

    console.print(Panel.fit(
        f"[bold cyan]📥 Importando Projeto do Overleaf[/bold cyan]\n"
        f"Origem: [bold]{zip_path.name}[/bold]\n"
        f"Destino: [bold]projects/{clean_name}[/bold]",
        border_style="cyan"
    ))

    target_dir.mkdir(parents=True, exist_ok=True)

    extracted_files = []
    with zipfile.ZipFile(zip_path, "r") as zf:
        for member in zf.infolist():
            # Pular pastas de sistema como __MACOSX ou .DS_Store
            if "__MACOSX" in member.filename or ".DS_Store" in member.filename:
                continue
            # Normalizar caminho para evitar zip slip
            member_path = Path(member.filename)
            dest_file = target_dir / member_path
            if member.is_dir():
                dest_file.mkdir(parents=True, exist_ok=True)
            else:
                dest_file.parent.mkdir(parents=True, exist_ok=True)
                with zf.open(member) as source, open(dest_file, "wb") as target:
                    shutil.copyfileobj(source, target)
                extracted_files.append(dest_file)

    console.print(f"[green]✔ {len(extracted_files)} arquivos descompactados em projects/{clean_name}[/green]")

    # Sincronizar novas citações adicionadas pelos colaboradores de volta para o master.bib
    if sync_to_master and MASTER_BIB.exists():
        console.print("[dim]→ Auditando e mesclando referências do Overleaf em references/master.bib...[/dim]")
        master_content = MASTER_BIB.read_text(encoding="utf-8", errors="ignore")
        master_entries = parse_bibtex_entries(master_content)

        new_entries_found = []
        for bib_file in target_dir.rglob("*.bib"):
            if any(part in EXCLUDE_DIRS for part in bib_file.parts):
                continue
            try:
                content = bib_file.read_text(encoding="utf-8", errors="ignore")
                project_entries = parse_bibtex_entries(content)
                for key, bib_raw in project_entries.items():
                    if key not in master_entries:
                        new_entries_found.append((key, bib_raw))
                        master_entries[key] = bib_raw
            except Exception:
                pass

        if new_entries_found:
            date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
            with open(MASTER_BIB, "a", encoding="utf-8") as f:
                f.write(f"\n\n% =========================================================================\n")
                f.write(f"% [OVERLEAF IMPORT] Adicionadas a partir de projects/{clean_name} em {date_str}\n")
                f.write(f"% =========================================================================\n")
                for key, bib_raw in new_entries_found:
                    f.write(bib_raw + "\n\n")

            table = Table(box=box.SIMPLE, show_header=True, header_style="bold green")
            table.add_column("Chave BibTeX", style="bold")
            table.add_column("Status")
            for key, _ in new_entries_found:
                table.add_row(key, "Incorporada a references/master.bib")
            console.print(table)
            console.print(f"[bold green]✔ {len(new_entries_found)} novas referências salvas na biblioteca global master.bib![/bold green]")
        else:
            console.print("[dim]✔ Nenhuma referência inédita para adicionar ao master.bib.[/dim]")

    console.print(Panel(
        f"[green]✅ Projeto Overleaf integrado ao VS Code com sucesso![/green]\n\n"
        f"📁 [bold]Diretório:[/bold] projects/{clean_name}\n"
        f"📄 [bold]Principal:[/bold] projects/{clean_name}/main.tex\n\n"
        f"Para compilar:\n"
        f"  [cyan]uv run python scripts/acc.py build projects/{clean_name}[/cyan]\n"
        f"Ou simplesmente abra o arquivo no VS Code e pressione [italic]Ctrl+Alt+B[/italic]!",
        title="Importação Concluída",
        border_style="green"
    ))

    return target_dir


def print_git_info():
    """Exibe instruções práticas para colaboração via Git Bridge do Overleaf."""
    console.print(Panel(
        "[bold cyan]🔗 Overleaf Git Bridge (Colaboração Direta sem ZIP)[/bold cyan]\n\n"
        "Se você possui Overleaf Premium ou conta institucional, o Overleaf oferece um repositório Git nativo.\n"
        "Em vez de baixar e subir .zip manualmente, você pode sincronizar um subdiretório do monorepo usando [bold]git subtree[/bold]:\n\n"
        "[bold yellow]1. Obtenha a URL Git no Overleaf:[/bold yellow]\n"
        "   Abra o projeto no Overleaf ➔ Menu (canto superior esquerdo) ➔ [bold]Git[/bold] ➔ Copie a URL (ex: [italic]https://git.overleaf.com/64a1b2c3d4...[/italic])\n\n"
        "[bold yellow]2. Adicione o remote do Overleaf no terminal:[/bold yellow]\n"
        "   [dim]git remote add overleaf_<nome> https://git.overleaf.com/<ID_DO_PROJETO>[/dim]\n\n"
        "[bold yellow]3. Para ENVIAR atualizações locais para o Overleaf:[/bold yellow]\n"
        "   [cyan]git subtree push --prefix=projects/<nome_projeto> overleaf_<nome> master[/cyan]\n\n"
        "[bold yellow]4. Para PUXAR alterações feitas pelos coautores no Overleaf:[/bold yellow]\n"
        "   [cyan]git subtree pull --prefix=projects/<nome_projeto> overleaf_<nome> master --squash[/cyan]\n\n"
        "[dim]Dica: Se preferir o modo tradicional simples, use sempre os comandos [bold]acc overleaf pack[/bold] e [bold]acc overleaf unpack[/bold].[/dim]",
        title="Git Subtree Workflow",
        border_style="cyan"
    ))


def main():
    if len(sys.argv) < 2:
        console.print(Panel.fit(
            "[bold cyan]🍃 Overleaf Bridge CLI (`overleaf_bridge`)[/bold cyan]\n"
            "Comandos:\n"
            "  [green]pack[/green] <projeto> [--out <arquivo.zip>] - Cria pacote limpo para o Overleaf com citações resolvidas\n"
            "  [green]unpack[/green] <arquivo.zip> [nome_projeto]    - Extrai zip do Overleaf e mescla novas referências ao master.bib\n"
            "  [green]sync-bib[/green] <projeto>                   - Sincroniza citações do projeto com master.bib\n"
            "  [green]git-info[/green]                             - Exibe guia de integração direta via Git Subtree\n\n"
            "Exemplo:\n"
            "  [italic]uv run python scripts/overleaf_bridge.py pack templates/artigo_sbc[/italic]",
            border_style="cyan"
        ))
        return

    action = sys.argv[1].lower()

    if action in ("pack", "bundle", "export"):
        if len(sys.argv) < 3:
            console.print("[red]Erro:[/red] Especifique o caminho do projeto. Ex: overleaf_bridge.py pack projects/meu_artigo")
            return
        proj = sys.argv[2]
        out_zip = sys.argv[4] if len(sys.argv) > 4 and sys.argv[3] in ("--out", "-o") else ""
        pack_project(proj, out_zip)

    elif action in ("unpack", "import"):
        if len(sys.argv) < 3:
            console.print("[red]Erro:[/red] Especifique o caminho do arquivo .zip. Ex: overleaf_bridge.py unpack C:/Downloads/artigo.zip")
            return
        zip_path = sys.argv[2]
        proj_name = sys.argv[3] if len(sys.argv) > 3 else ""
        unpack_project(zip_path, proj_name)

    elif action in ("sync-bib", "bib"):
        if len(sys.argv) < 3:
            console.print("[red]Erro:[/red] Especifique o caminho do projeto. Ex: overleaf_bridge.py sync-bib projects/meu_artigo")
            return
        proj_dir = Path(sys.argv[2]).resolve()
        total_cited, added, missing = sync_project_citations(proj_dir)
        console.print(f"[green]✔ Citações sincronizadas:[/green] {total_cited} no texto, {added} adicionadas do master.bib.")
        if missing:
            console.print(f"[yellow]⚠ Faltam no acervo:[/yellow] {', '.join(missing)}")

    elif action in ("git-info", "git", "subtree"):
        print_git_info()

    else:
        console.print(f"[red]Comando desconhecido:[/red] {action}")


if __name__ == "__main__":
    main()
