"""
=============================================================================
OPENALEX ACADEMIC PROVIDER - Academic PKM
=============================================================================
Consulta o catálogo do OpenAlex (250M+ obras científicas, autores e instituições).
100% aberto, sem necessidade de chaves de API, com acesso a PDFs abertos
e reconstrução de resumos a partir do abstract inverted index.
=============================================================================
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

import httpx

from .base_provider import AcademicPaper, BaseAcademicProvider

OPENALEX_WORKS_URL = "https://api.openalex.org/works"


def reconstruct_abstract(inverted_index: Optional[Dict[str, List[int]]]) -> str:
    """Reconstrói o abstract a partir do abstract_inverted_index do OpenAlex."""
    if not inverted_index or not isinstance(inverted_index, dict):
        return ""
    try:
        word_positions: List[tuple[int, str]] = []
        for word, positions in inverted_index.items():
            if isinstance(positions, list):
                for pos in positions:
                    word_positions.append((pos, word))
        word_positions.sort(key=lambda x: x[0])
        return " ".join(word for _, word in word_positions)
    except Exception:
        return ""


class OpenAlexProvider(BaseAcademicProvider):
    name = "openalex"
    display_name = "OpenAlex (Global Scholarly Graph)"
    description = "Catálogo universal aberto de 250M+ de publicações científicas e métricas globais."

    def search(self, query: str, limit: int = 5, **kwargs) -> List[AcademicPaper]:
        params = {
            "search": query,
            "per_page": min(limit, 25),
            "sort": "relevance_score:desc",
        }
        headers = {
            "User-Agent": "AcademicPKM/1.0 (mailto:scientific-pkm@local.vault)"
        }

        papers: List[AcademicPaper] = []
        try:
            with httpx.Client(timeout=25, follow_redirects=True) as client:
                resp = client.get(OPENALEX_WORKS_URL, params=params, headers=headers)
                resp.raise_for_status()
                data = resp.json()

            results = data.get("results", []) or []
            for work in results:
                title = (work.get("display_name") or work.get("title") or "").strip()
                if not title:
                    continue

                authors = []
                for auth in work.get("authorships", []):
                    auth_name = auth.get("author", {}).get("display_name", "").strip()
                    if auth_name:
                        authors.append(auth_name)

                year = work.get("publication_year")
                try:
                    year = int(year) if year is not None else None
                except (ValueError, TypeError):
                    year = None

                primary_loc = work.get("primary_location") or {}
                source = primary_loc.get("source") or {}
                venue = source.get("display_name", "") or "Periódico Aberto"

                raw_doi = work.get("doi") or ""
                doi = raw_doi.replace("https://doi.org/", "").strip() if raw_doi else ""

                oa_data = work.get("open_access") or {}
                pdf_url = oa_data.get("oa_url") or primary_loc.get("pdf_url") or ""

                url = raw_doi or work.get("id") or (f"https://doi.org/{doi}" if doi else "")
                abstract = reconstruct_abstract(work.get("abstract_inverted_index"))
                citation_count = work.get("cited_by_count")

                paper_type = work.get("type_crossref") or work.get("type") or "Artigo Científico"

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
                    study_type=paper_type.capitalize(),
                    raw_data=work,
                )
                papers.append(paper)

        except Exception:
            pass

        return papers
