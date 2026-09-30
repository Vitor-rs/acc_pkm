"""
=============================================================================
SEMANTIC SCHOLAR ACADEMIC PROVIDER (S2) - Academic PKM
=============================================================================
Consulta o Semantic Scholar Open Research Corpus da Allen Institute for AI.
Suporta contagem de citações, citações influentes, metadados de periódicos,
preprints e links de PDFs de acesso aberto.
=============================================================================
"""

from __future__ import annotations

import os
import re
from typing import List, Optional

import httpx

from .base_provider import AcademicPaper, BaseAcademicProvider

S2_SEARCH_URL = "https://api.semanticscholar.org/graph/v1/paper/search"


class SemanticScholarProvider(BaseAcademicProvider):
    name = "s2"
    display_name = "Semantic Scholar (AI2 Knowledge Graph)"
    description = "Grafo acadêmico com 200M+ de artigos, contagem de citações e citações influentes."

    def search(self, query: str, limit: int = 5, **kwargs) -> List[AcademicPaper]:
        api_key = os.getenv("SEMANTIC_SCHOLAR_API_KEY", "").strip() or os.getenv("S2_API_KEY", "").strip()
        headers = {
            "User-Agent": "AcademicPKM/1.0 (academic-pkm@local.vault)"
        }
        if api_key:
            headers["x-api-key"] = api_key

        fields = (
            "title,authors,year,venue,externalIds,abstract,citationCount,"
            "influentialCitationCount,openAccessPdf,url"
        )
        params = {
            "query": query,
            "limit": min(limit, 25),
            "fields": fields,
        }

        papers: List[AcademicPaper] = []
        try:
            with httpx.Client(timeout=25, follow_redirects=True) as client:
                resp = client.get(S2_SEARCH_URL, params=params, headers=headers)
                if resp.status_code == 429:
                    # Rate limit atingido - tentar fallback silencioso
                    return []
                resp.raise_for_status()
                data = resp.json()

            for item in data.get("data", []):
                title = item.get("title", "").strip()
                if not title:
                    continue

                raw_authors = item.get("authors", []) or []
                authors = [a.get("name", "").strip() for a in raw_authors if a.get("name")]

                year = item.get("year")
                try:
                    year = int(year) if year is not None else None
                except (ValueError, TypeError):
                    year = None

                venue = item.get("venue", "").strip()
                external_ids = item.get("externalIds", {}) or {}
                doi = external_ids.get("DOI", "") or ""
                arxiv_id = external_ids.get("ArXiv", "")

                if not doi and arxiv_id:
                    doi = f"10.48550/ARXIV.{arxiv_id}"

                url = item.get("url", "") or (f"https://doi.org/{doi}" if doi else "")

                oa_pdf = item.get("openAccessPdf", {}) or {}
                pdf_url = oa_pdf.get("url", "") if isinstance(oa_pdf, dict) else ""

                abstract = item.get("abstract", "") or ""
                citation_count = item.get("citationCount")
                influential_citations = item.get("influentialCitationCount")

                paper = AcademicPaper(
                    title=title,
                    authors=authors,
                    year=year,
                    venue=venue or ("arXiv" if arxiv_id else "Periódico / Conferência"),
                    doi=doi,
                    url=url,
                    pdf_url=pdf_url,
                    abstract=abstract,
                    citation_count=citation_count,
                    influential_citation_count=influential_citations,
                    source_provider=self.name,
                    study_type="Artigo Científico",
                    raw_data=item,
                )
                papers.append(paper)

        except Exception:
            # Fallback seguro para não travar a frota
            pass

        return papers
