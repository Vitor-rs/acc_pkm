"""
=============================================================================
CROSSREF ACADEMIC PROVIDER - Academic PKM
=============================================================================
Consulta o catálogo oficial da CrossRef (Agência Oficial de Registro de DOIs).
Cobre editoras internacionais e nacionais (Springer, Elsevier, IEEE, ACM,
MDPI, SciELO, Wiley, etc.).
100% aberto e gratuito.
=============================================================================
"""

from __future__ import annotations

import re
from typing import List, Optional

import httpx

from .base_provider import AcademicPaper, BaseAcademicProvider

CROSSREF_WORKS_URL = "https://api.crossref.org/works"


def clean_jats_xml(text: str) -> str:
    """Remove tags JATS XML comuns no abstract retornado pela CrossRef."""
    if not text:
        return ""
    clean = re.sub(r"<[^>]+>", " ", text)
    clean = re.sub(r"\s+", " ", clean).strip()
    return clean


class CrossRefProvider(BaseAcademicProvider):
    name = "crossref"
    display_name = "CrossRef (Official DOI Authority)"
    description = "Registro oficial global de DOIs acadêmicos e metadados de editoras científicas."

    def search(self, query: str, limit: int = 5, **kwargs) -> List[AcademicPaper]:
        params = {
            "query": query,
            "rows": min(limit, 25),
            "sort": "relevance",
        }
        headers = {
            "User-Agent": "AcademicPKM/1.0 (mailto:scientific-pkm@local.vault)"
        }

        papers: List[AcademicPaper] = []
        try:
            with httpx.Client(timeout=25, follow_redirects=True) as client:
                resp = client.get(CROSSREF_WORKS_URL, params=params, headers=headers)
                resp.raise_for_status()
                data = resp.json()

            items = data.get("message", {}).get("items", []) or []
            for item in items:
                title_list = item.get("title", [])
                title = title_list[0].strip() if title_list else ""
                if not title:
                    continue

                authors = []
                for a in item.get("author", []):
                    given = a.get("given", "").strip()
                    family = a.get("family", "").strip()
                    name = f"{given} {family}".strip() if given or family else a.get("name", "").strip()
                    if name:
                        authors.append(name)

                year = None
                issued = item.get("issued") or item.get("published-print") or item.get("published-online") or {}
                date_parts = issued.get("date-parts", [])
                if date_parts and date_parts[0] and date_parts[0][0]:
                    try:
                        year = int(date_parts[0][0])
                    except (ValueError, TypeError):
                        year = None

                venues = item.get("container-title", [])
                venue = venues[0].strip() if venues else item.get("publisher", "Editora Científica")

                doi = item.get("DOI", "").strip()
                url = f"https://doi.org/{doi}" if doi else item.get("URL", "")

                pdf_url = ""
                for link in item.get("link", []):
                    content_type = link.get("content-type", "").lower()
                    if "pdf" in content_type:
                        pdf_url = link.get("URL", "")
                        break

                raw_abstract = item.get("abstract", "")
                abstract = clean_jats_xml(raw_abstract)

                citation_count = item.get("is-referenced-by-count")
                work_type = item.get("type", "journal-article").replace("-", " ")

                paper = AcademicPaper(
                    title=title,
                    authors=authors,
                    year=year,
                    venue=venue,
                    doi=doi,
                    url=url,
                    pdf_url=pdf_url,
                    abstract=abstract,
                    citation_count=citation_count,
                    source_provider=self.name,
                    study_type=work_type.capitalize(),
                    raw_data=item,
                )
                papers.append(paper)

        except Exception:
            pass

        return papers
