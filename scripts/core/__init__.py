"""Pacote de componentes e utilitários centrais do Academic PKM."""

from .config import (
    CATALOG_HTML,
    CATALOG_JSONL,
    CSL_DIR,
    ENV_PATH,
    LAKE_DIR,
    MASTER_BIB,
    PROTOCOLS_DIR,
    REPO_ROOT,
    SCRIPTS_DIR,
    TEMPLATES_DIR,
    find_executable,
)

__all__ = [
    "REPO_ROOT",
    "SCRIPTS_DIR",
    "LAKE_DIR",
    "CATALOG_HTML",
    "CATALOG_JSONL",
    "MASTER_BIB",
    "CSL_DIR",
    "TEMPLATES_DIR",
    "PROTOCOLS_DIR",
    "ENV_PATH",
    "find_executable",
]
