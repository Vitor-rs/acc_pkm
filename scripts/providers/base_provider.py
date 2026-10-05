# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "httpx>=0.27.0",
#     "rich>=13.7.0",
#     "pyyaml>=6.0.1",
#     "python-dotenv>=1.0.0",
# ]
# ///
"""
=============================================================================
BASE ACADEMIC PROVIDER - Academic PKM
=============================================================================
Define a interface abstrata e modelo de dados padrão para todos os adaptadores
de fontes acadêmicas e bibliográficas (Consensus, S2, arXiv, OpenAlex, etc.).
=============================================================================
"""

from __future__ import annotations

import re
import unicodedata
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class AcademicPaper:
    """Modelo canônico unificado para artigos científicos e fontes acadêmicas."""
    title: str
    authors: List[str] = field(default_factory=list)
    year: Optional[int] = None
    venue: str = ""
    doi: str = ""
    url: str = ""
    pdf_url: str = ""
    abstract: str = ""
    citation_count: Optional[int] = None
    influential_citation_count: Optional[int] = None
    source_provider: str = "generic"
    study_type: str = ""
    consensus_takeaway: str = ""
    raw_data: Dict[str, Any] = field(default_factory=dict)

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
        """Gera chave de citação BibTeX consistente e determinística."""
        first_author = "Autor"
        if self.authors:
            # Pegar o último sobrenome do primeiro autor
            parts = re.sub(r"[^a-zA-Z\s]", "", self.authors[0]).strip().split()
            first_author = parts[-1].capitalize() if parts else "Autor"

        year_str = str(self.year) if self.year else "s_d"
        # Primeiras 2 palavras do título
        title_words = re.sub(r"[^a-zA-Z0-9\s]", "", self.title).strip().split()
        title_slug = "".join(w.capitalize() for w in title_words[:2]) or "Doc"

        return f"{first_author}{year_str}_{title_slug}"

    def to_bibtex(self) -> str:
        """Exporta o artigo no formato BibTeX padrão."""
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
        if self.doi:
            lines.append(f"  doi = {{{self.doi}}},")
        if self.url:
            lines.append(f"  url = {{{self.url}}},")
        if self.abstract:
            clean_abs = self.abstract.replace("\n", " ").replace("{", "").replace("}", "")[:500]
            lines.append(f"  abstract = {{{clean_abs}}},")
        lines.append("}")
        return "\n".join(lines)


def sanitize_filename(name: str) -> str:
    """Higieniza string para nomes de arquivo seguros em qualquer SO."""
    name = unicodedata.normalize("NFKD", name)
    name = "".join(c for c in name if not unicodedata.combining(c))
    name = re.sub(r"[^\w\s-]", "", name).strip()
    name = re.sub(r"[-\s]+", "_", name)
    return name.lower()[:80] or "paper"


class BaseAcademicProvider(ABC):
    """Classe base para todos os provedores acadêmicos."""

    name: str = "base"
    display_name: str = "Base Provider"
    description: str = ""

    @abstractmethod
    def search(self, query: str, limit: int = 5, **kwargs) -> List[AcademicPaper]:
        """Executa busca e retorna lista de AcademicPaper unificados."""
        pass

    def format_lake_markdown(self, papers: List[AcademicPaper], query: str) -> str:
        """Gera conteúdo Markdown estruturado para o Data Lake."""
        now_iso = datetime.now().isoformat()
        date_str = datetime.now().strftime("%d/%m/%Y %H:%M")

        frontmatter = (
            f"---\n"
            f"title: \"[{self.name.upper()}] {query}\"\n"
            f"type: research_literature\n"
            f"provider: \"{self.name}\"\n"
            f"date: '{now_iso}'\n"
            f"query: \"{query}\"\n"
            f"total_papers: {len(papers)}\n"
            f"tags: [{self.name}, pesquisa_cientifica, literatura, acervo]\n"
            f"---\n\n"
            f"# 📚 [{self.display_name}] Literatura Científica: {query}\n\n"
            f"*Colhido via Academic PKM Fleet Provider `{self.name}` em {date_str}.*\n\n"
            f"## Artigos Selecionados ({len(papers)} resultados)\n\n"
        )

        entries = []
        for idx, p in enumerate(papers, 1):
            cites = f" | **Citações:** {p.citation_count}" if p.citation_count is not None else ""
            study = f" | **Tipo:** `{p.study_type}`" if p.study_type else ""
            doi_link = f"[{p.doi}](https://doi.org/{p.doi})" if p.doi else ("N/D" if not p.url else f"[Link]({p.url})")
            pdf_link = f" | [📄 PDF Aberto]({p.pdf_url})" if p.pdf_url else ""

            body = (
                f"### {idx}. {p.title}\n\n"
                f"- **Autores:** {p.author_summary}\n"
                f"- **Ano / Periódico:** {p.year or 'N/D'} | *{p.venue or 'Sem periódico informado'}*{cites}{study}\n"
                f"- **DOI / Link:** {doi_link}{pdf_link}\n"
            )

            if p.consensus_takeaway:
                body += f"- **Síntese de Evidência:**\n> {p.consensus_takeaway}\n\n"
            elif p.abstract:
                body += f"- **Resumo (Abstract):**\n> {p.abstract[:600]}...\n\n"
            else:
                body += "\n"

            entries.append(body)

        return frontmatter + "\n".join(entries)

    def save_to_lake(self, papers: List[AcademicPaper], query: str, lake_dir: Path, master_bib: Optional[Path] = None) -> Optional[Path]:
        """Salva a busca no Data Lake com o prefixo padronizado [provider]_... e atualiza master.bib."""
        if not papers:
            return None

        lake_dir.mkdir(parents=True, exist_ok=True)
        slug = sanitize_filename(query)[:40]
        filename = f"[{self.name}]_{slug}.md"
        target_path = lake_dir / filename

        md_content = self.format_lake_markdown(papers, query)
        target_path.write_text(md_content, encoding="utf-8")

        # Atualizar master.bib se fornecido
        if master_bib:
            try:
                from core.bibtex_service import add_entries_to_bib
                entries = [p.to_bibtex() for p in papers]
                add_entries_to_bib(entries, source_label=f"Academic Fleet [{self.name}]: {query}", target_bib=master_bib)
            except Exception as e:
                print(f"⚠️ Aviso ao atualizar master.bib: {e}")

        return target_path
