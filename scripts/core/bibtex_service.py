"""
=============================================================================
BIBTEX SERVICE - Academic PKM
=============================================================================
Serviço centralizado, atômico e idempotente para gerenciamento do arquivo
global de referências bibliográficas (references/master.bib) e arquivos
locais de projetos LaTeX. Elimina duplicações por DOI, título e citekey.
=============================================================================
"""

from __future__ import annotations

import datetime
import re
import unicodedata
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Union

from .config import MASTER_BIB


def normalize_doi(doi: str) -> str:
    """Normaliza identificador DOI para comparação estrita."""
    if not doi:
        return ""
    d = doi.lower().strip()
    d = d.replace("https://doi.org/", "").replace("http://doi.org/", "").replace("doi:", "")
    return d.strip()


def normalize_title(title: str) -> str:
    """Normaliza título para comparação fonética/lexical."""
    if not title:
        return ""
    t = unicodedata.normalize("NFKD", title.lower())
    t = "".join(c for c in t if not unicodedata.combining(c))
    t = re.sub(r"[^a-z0-9\s]", "", t)
    return re.sub(r"\s+", " ", t).strip()


def get_master_bib_path() -> Path:
    """Retorna o caminho canônico do master.bib, garantindo que o diretório exista."""
    MASTER_BIB.parent.mkdir(parents=True, exist_ok=True)
    if not MASTER_BIB.exists():
        MASTER_BIB.write_text(
            "% =========================================================================\n"
            "% Academic PKM - Master Bibliography Database (references/master.bib)\n"
            "% Base canônica global de referências bibliográficas para projetos LaTeX e PKM\n"
            "% =========================================================================\n\n",
            encoding="utf-8",
        )
    return MASTER_BIB


def read_bib_file(path: Optional[Path] = None) -> str:
    """Lê o conteúdo de um arquivo BibTeX com tratamento de codificação."""
    target = path or get_master_bib_path()
    if not target.exists():
        return ""
    return target.read_text(encoding="utf-8", errors="replace")


def extract_citekeys(content: Optional[str] = None, bib_path: Optional[Path] = None) -> List[str]:
    """Extrai todas as chaves de citação (citekeys) presentes no texto BibTeX."""
    text = content if content is not None else read_bib_file(bib_path)
    matches = re.findall(r"@(\w+)\s*\{\s*([^,]+),", text)
    return [m[1].strip() for m in matches]


def extract_dois(content: Optional[str] = None, bib_path: Optional[Path] = None) -> Set[str]:
    """Extrai todos os DOIs normalizados presentes no arquivo BibTeX."""
    text = content if content is not None else read_bib_file(bib_path)
    dois = set()
    for m in re.finditer(r'doi\s*=\s*[\{"\']([^"\'\}]+)[\}"\']', text, re.IGNORECASE):
        norm = normalize_doi(m.group(1))
        if norm:
            dois.add(norm)
    return dois


def parse_bibtex_entries(content: str) -> Dict[str, str]:
    """
    Segmenta um texto BibTeX em entradas individuais mapeadas por citekey.
    Suporta aninhamento de chaves ({...}).
    """
    entries = {}
    pattern = r"@\w+\s*\{"
    starts = [m.start() for m in re.finditer(pattern, content)]

    for i, start in enumerate(starts):
        end = starts[i + 1] if i + 1 < len(starts) else len(content)
        entry_text = content[start:end].strip()

        # Extrair citekey
        key_match = re.search(r"@\w+\s*\{\s*([^,]+),", entry_text)
        if key_match:
            key = key_match.group(1).strip()
            # Encontrar fechamento real da chave externa
            depth = 0
            close_idx = -1
            for idx, ch in enumerate(entry_text):
                if ch == "{":
                    depth += 1
                elif ch == "}":
                    depth -= 1
                    if depth == 0:
                        close_idx = idx + 1
                        break
            if close_idx > 0:
                entries[key] = entry_text[:close_idx]
            else:
                entries[key] = entry_text

    return entries


class AddEntriesResult(int):
    """Resultado de adição ao BibTeX compatível tanto com int quanto com Tuple[int, List[str]]."""
    keys: List[str]

    def __new__(cls, count: int, keys: List[str]):
        obj = super().__new__(cls, count)
        obj.keys = list(keys)
        return obj

    def __iter__(self):
        return iter((int(self), self.keys))


def add_entries_to_bib(
    entries: Union[List[str], str],
    target_bib: Optional[Union[Path, str]] = None,
    source_label: str = "Academic PKM",
    dedup_by_doi: bool = True,
    header_comment: Optional[str] = None,
    **kwargs: Any,
) -> AddEntriesResult:
    """
    Adiciona novas entradas BibTeX ao arquivo especificado (padrão: master.bib) de forma idempotente.
    Evita duplicações por citekey e opcionalmente por DOI.
    Retorna objeto AddEntriesResult compatível tanto como int (contagem) quanto como tuple (contagem, chaves).
    """
    # Flexibilidade de parâmetros posicionais
    if isinstance(target_bib, str) and not target_bib.endswith(".bib") and "/" not in target_bib and "\\" not in target_bib:
        source_label = target_bib
        target = kwargs.get("target_bib_path") or get_master_bib_path()
    elif target_bib is not None:
        target = Path(target_bib)
    else:
        target = get_master_bib_path()

    current_content = read_bib_file(target)

    existing_keys = set(extract_citekeys(current_content))
    existing_dois = extract_dois(current_content) if dedup_by_doi else set()

    # Normalizar entradas para dicionário
    if isinstance(entries, str):
        parsed = parse_bibtex_entries(entries)
    elif isinstance(entries, list):
        parsed = {}
        for item in entries:
            p = parse_bibtex_entries(item)
            parsed.update(p)
    else:
        parsed = {}

    to_add = []
    added_keys = []

    for key, bib_code in parsed.items():
        if key in existing_keys:
            continue

        # Verificar se possui DOI já existente
        if dedup_by_doi:
            doi_match = re.search(r'doi\s*=\s*[\{"\']([^"\'\}]+)[\}"\']', bib_code, re.IGNORECASE)
            if doi_match:
                norm_doi = normalize_doi(doi_match.group(1))
                if norm_doi and norm_doi in existing_dois:
                    continue
                if norm_doi:
                    existing_dois.add(norm_doi)

        to_add.append(bib_code.strip())
        added_keys.append(key)
        existing_keys.add(key)

    if to_add:
        if header_comment:
            header_str = f"\n\n{header_comment}\n\n"
        else:
            now_str = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
            header_str = f"\n\n% --- Adicionado por: {source_label} ({now_str}) ---\n\n"

        with open(target, "a", encoding="utf-8") as f:
            f.write(header_str)
            for b in to_add:
                f.write(b + "\n\n")

    return AddEntriesResult(len(to_add), added_keys)


def audit_master_bib(bib_path: Optional[Path] = None) -> Dict[str, Any]:
    """
    Audita a integridade da base BibTeX:
    - Total de referências
    - Chaves duplicadas
    - DOIs duplicados
    - Entradas sem autor ou título
    """
    target = bib_path or get_master_bib_path()
    content = read_bib_file(target)

    matches = re.findall(r"@(\w+)\s*\{\s*([^,]+),", content)
    keys = [m[1].strip() for m in matches]

    seen_keys = set()
    dup_keys = []
    for k in keys:
        if k in seen_keys:
            dup_keys.append(k)
        seen_keys.add(k)

    parsed = parse_bibtex_entries(content)

    entries_without_title = []
    entries_without_author = []
    for k, text in parsed.items():
        if not re.search(r'\btitle\s*=', text, re.IGNORECASE):
            entries_without_title.append(k)
        if not re.search(r'\bauthor\s*=', text, re.IGNORECASE):
            entries_without_author.append(k)

    return {
        "file": str(target),
        "total_entries": len(keys),
        "unique_keys": len(seen_keys),
        "duplicate_keys": dup_keys,
        "missing_title": entries_without_title,
        "missing_author": entries_without_author,
    }
