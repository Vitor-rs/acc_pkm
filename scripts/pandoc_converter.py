
"""
=============================================================================
PANDOC CONVERTER - Academic PKM
=============================================================================
Utilitário de conversão universal de documentos acadêmicos (Markdown ⇄ DOCX ⇄ LaTeX ⇄ PDF)
com suporte nativo a estilos CSL (ABNT, APA, IEEE) e resolução de referências
diretamente do references/master.bib.
=============================================================================
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List, Optional, Tuple

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from rich import box
from rich.console import Console
from rich.panel import Panel

REPO_ROOT = Path(__file__).resolve().parent.parent
CSL_DIR = REPO_ROOT / "resources" / "csl"
MASTER_BIB = REPO_ROOT / "references" / "master.bib"

console = Console(force_terminal=True)


def find_pandoc() -> Optional[str]:
    """Localiza o executável do Pandoc no PATH ou em diretórios conhecidos do Windows."""
    # 1. Checa PATH existente
    which_path = shutil.which("pandoc")
    if which_path:
        return which_path

    # 2. Checa caminhos padrão de instalação do Windows (winget/msi)
    local_app = os.environ.get("LOCALAPPDATA", "")
    prog_files = os.environ.get("ProgramFiles", "")
    prog_files_x86 = os.environ.get("ProgramFiles(x86)", "")

    candidates = [
        Path(local_app) / "Pandoc" / "pandoc.exe",
        Path(prog_files) / "Pandoc" / "pandoc.exe",
        Path(prog_files_x86) / "Pandoc" / "pandoc.exe",
        Path(local_app) / "Programs" / "Pandoc" / "pandoc.exe",
    ]

    for c in candidates:
        if c.exists():
            # Injeta o diretório no PATH do processo corrente
            p_dir = str(c.parent)
            if p_dir not in os.environ.get("PATH", ""):
                os.environ["PATH"] = f"{p_dir};{os.environ.get('PATH', '')}"
            return str(c)

    return None


def resolve_csl_path(csl_name: str) -> Optional[Path]:
    """Resolve o arquivo CSL pelo nome amigável (abnt, apa, ieee) ou caminho direto."""
    csl_map = {
        "abnt": CSL_DIR / "abnt.csl",
        "apa": CSL_DIR / "apa.csl",
        "ieee": CSL_DIR / "ieee.csl",
    }
    low = csl_name.lower().strip()
    if low in csl_map:
        target = csl_map[low]
        if target.exists():
            return target

    custom = Path(csl_name)
    if custom.exists():
        return custom

    # Tenta procurar em resources/csl/
    cand = CSL_DIR / f"{low}.csl"
    if cand.exists():
        return cand

    return None


def convert_document(
    input_file: Path | str,
    output_file: Optional[Path | str] = None,
    output_format: Optional[str] = None,
    csl: str = "abnt",
    bib_file: Optional[Path | str] = None,
    toc: bool = False,
    standalone: bool = True,
    extra_args: Optional[List[str]] = None,
) -> Tuple[bool, Path, str]:
    """
    Executa a conversão do documento usando o Pandoc com citeproc e referências.
    Retorna: (sucesso, caminho_arquivo_saida, mensagem)
    """
    pandoc_exe = find_pandoc()
    if not pandoc_exe:
        return False, Path(""), "Pandoc não encontrado no sistema. Instale com: winget install JohnMacFarlane.Pandoc"

    in_path = Path(input_file).resolve()
    if not in_path.exists():
        return False, Path(""), f"Arquivo de entrada não encontrado: {in_path}"

    # Determinar caminho e formato de saída
    if output_file:
        out_path = Path(output_file).resolve()
    else:
        # Se saída não informada, deriva para .docx no mesmo diretório
        target_ext = f".{output_format}" if output_format else ".docx"
        out_path = in_path.with_suffix(target_ext)

    out_path.parent.mkdir(parents=True, exist_ok=True)

    cmd = [pandoc_exe, str(in_path), "-o", str(out_path)]

    if standalone:
        cmd.append("--standalone")

    if toc:
        cmd.append("--toc")

    # Resolução de Bibliografia e Citações
    bib_target = Path(bib_file).resolve() if bib_file else MASTER_BIB
    if bib_target.exists():
        cmd.extend(["--citeproc", f"--bibliography={bib_target}"])

        # Estilo CSL
        csl_path = resolve_csl_path(csl)
        if csl_path:
            cmd.append(f"--csl={csl_path}")

    # Tratamento para geração de PDF via LaTeX engine se solicitado
    if out_path.suffix.lower() == ".pdf":
        pdflatex_path = shutil.which("pdflatex")
        if pdflatex_path:
            cmd.append(f"--pdf-engine={pdflatex_path}")
        else:
            xelatex_path = shutil.which("xelatex")
            if xelatex_path:
                cmd.append(f"--pdf-engine={xelatex_path}")

    if extra_args:
        cmd.extend(extra_args)

    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if res.returncode == 0:
            return True, out_path, "Conversão concluída com sucesso."
        else:
            err = res.stderr.strip() or res.stdout.strip() or f"Código de saída {res.returncode}"
            return False, out_path, f"Erro na conversão do Pandoc: {err}"
    except Exception as e:
        return False, out_path, f"Falha na execução do processo: {e}"


def main():
    parser = argparse.ArgumentParser(
        prog="acc convert",
        description="🌊 Academic PKM — Conversor Universal de Documentos (Pandoc)",
    )
    parser.add_argument("input_file", help="Caminho do documento de entrada (.md, .tex, .docx, etc.)")
    parser.add_argument("-o", "--output", help="Arquivo de destino com extensão (ex: relatorio.docx, artigo.tex, doc.pdf)")
    parser.add_argument("-f", "--to", dest="output_format", help="Formato de saída (docx, latex, pdf, html5, markdown)")
    parser.add_argument("--csl", default="abnt", help="Estilo de citação CSL (abnt, apa, ieee). Padrão: abnt")
    parser.add_argument("--bib", help="Arquivo BibTeX customizado (padrão: references/master.bib)")
    parser.add_argument("--toc", action="store_true", help="Gera sumário (Table of Contents)")
    parser.add_argument("--open", action="store_true", help="Abre o arquivo gerado no aplicativo padrão do Windows")

    args, unknown = parser.parse_known_args()

    console.print(Panel.fit(
        f"[bold cyan]📄 Academic PKM Pandoc Bridge[/bold cyan]\n"
        f"[bold]Entrada:[/bold] {args.input_file}\n"
        f"[bold]Estilo CSL:[/bold] [magenta]{args.csl.upper()}[/magenta]\n"
        f"[bold]Destino:[/bold] {args.output or 'Automático (.docx)'}",
        border_style="cyan"
    ))

    success, out_path, msg = convert_document(
        input_file=args.input_file,
        output_file=args.output,
        output_format=args.output_format,
        csl=args.csl,
        bib_file=args.bib,
        toc=args.toc,
        extra_args=unknown,
    )

    if success:
        console.print(Panel.fit(
            f"[bold green]✔ Conversão Concluída com Sucesso![/bold green]\n"
            f"[bold]Arquivo Gerado:[/bold] file:///{out_path.as_posix()}",
            border_style="green"
        ))
        if args.open and out_path.exists():
            os.startfile(str(out_path))
    else:
        console.print(Panel.fit(
            f"[bold red]✘ Falha na Conversão[/bold red]\n{msg}",
            border_style="red"
        ))
        sys.exit(1)


if __name__ == "__main__":
    main()
