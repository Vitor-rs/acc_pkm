"""
=============================================================================
CORE CONFIGURATION & COMMON UTILITIES - Academic PKM
=============================================================================
Centraliza constantes de caminhos, resolução de executáveis e configurações
globais do monorepo, assegurando o princípio Don't Repeat Yourself (DRY).
=============================================================================
"""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path
from typing import Optional

# Reconfigura streams padrão para UTF-8 no Windows para prevenir erros de codificação
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from dotenv import load_dotenv

# Diretórios Centrais do Monorepo
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
LAKE_DIR = REPO_ROOT / "resources" / "_lake"
CATALOG_HTML = REPO_ROOT / "resources" / "_lake_catalog.html"
CATALOG_JSONL = REPO_ROOT / "resources" / "_catalog" / "documents.jsonl"
MASTER_BIB = REPO_ROOT / "references" / "master.bib"
CSL_DIR = REPO_ROOT / "resources" / "csl"
TEMPLATES_DIR = REPO_ROOT / "resources" / "templates"
PROTOCOLS_DIR = REPO_ROOT / "resources" / "protocols"
DIAGRAMS_DIR = REPO_ROOT / "resources" / "diagrams"
ENV_PATH = REPO_ROOT / ".env"

if ENV_PATH.exists():
    load_dotenv(ENV_PATH)
else:
    load_dotenv()


def find_executable(cmd: str) -> Optional[str]:
    """Localiza executáveis no PATH ou em diretórios conhecidos de instalação no Windows."""
    path = shutil.which(cmd)
    if path:
        return path

    local_app = os.environ.get("LOCALAPPDATA", "")
    prog_files = os.environ.get("ProgramFiles", "")
    prog_files_x86 = os.environ.get("ProgramFiles(x86)", "")

    candidates = [
        Path(prog_files) / "draw.io" / f"{cmd}.exe",
        Path(local_app) / "Programs" / "draw.io" / f"{cmd}.exe",
        Path(prog_files) / "draw.io" / "draw.io.exe",
        Path(local_app) / "Programs" / "draw.io" / "draw.io.exe",
        Path(local_app) / "Pandoc" / f"{cmd}.exe",
        Path(prog_files) / "Pandoc" / f"{cmd}.exe",
        Path(prog_files_x86) / "Pandoc" / f"{cmd}.exe",
        Path(local_app) / "Programs" / "Pandoc" / f"{cmd}.exe",
        Path(local_app) / "Programs" / "MiKTeX" / "miktex" / "bin" / "x64" / f"{cmd}.exe",
        Path(prog_files) / "MiKTeX" / "miktex" / "bin" / "x64" / f"{cmd}.exe",
        Path(local_app) / "bin" / f"{cmd}.exe",
        Path(os.environ.get("USERPROFILE", "")) / ".local" / "bin" / f"{cmd}.exe",
    ]

    for c in candidates:
        if c.exists():
            p_dir = str(c.parent)
            if p_dir not in os.environ.get("PATH", ""):
                os.environ["PATH"] = f"{p_dir};{os.environ.get('PATH', '')}"
            return str(c)

    return None
