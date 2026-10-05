"""
=============================================================================
CORE PACKAGE - Academic PKM
=============================================================================
Exporta constantes centrais de diretórios, utilitários do sistema,
serviço de catalogação do Lake e serviço de gerenciamento do BibTeX.
=============================================================================
"""

from .bibtex_service import (
    add_entries_to_bib,
    audit_master_bib,
    extract_citekeys,
    extract_dois,
    get_master_bib_path,
    normalize_doi,
    normalize_title,
    parse_bibtex_entries,
    read_bib_file,
)
from .catalog_service import (
    generate_catalog_html,
    generate_catalog_jsonl,
    reindex_catalog,
    scan_lake_items,
)
from .config import (
    CATALOG_HTML,
    CATALOG_JSONL,
    CSL_DIR,
    DIAGRAMS_DIR,
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
    # Diretórios e Config
    "REPO_ROOT",
    "SCRIPTS_DIR",
    "LAKE_DIR",
    "CATALOG_HTML",
    "CATALOG_JSONL",
    "MASTER_BIB",
    "CSL_DIR",
    "TEMPLATES_DIR",
    "PROTOCOLS_DIR",
    "DIAGRAMS_DIR",
    "ENV_PATH",
    "find_executable",
    # Catálogo
    "scan_lake_items",
    "generate_catalog_html",
    "generate_catalog_jsonl",
    "reindex_catalog",
    # BibTeX
    "get_master_bib_path",
    "read_bib_file",
    "extract_citekeys",
    "extract_dois",
    "parse_bibtex_entries",
    "add_entries_to_bib",
    "audit_master_bib",
    "normalize_doi",
    "normalize_title",
]
