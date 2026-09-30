"""
=============================================================================
CONSENSUS ACADEMIC PROVIDER - Academic PKM
=============================================================================
Consulta a base científica do Consensus.app (200M+ de artigos revisados por
pares, sintetizando medidor de consenso e study snapshots).
=============================================================================
"""

from __future__ import annotations

import os
from typing import List

import httpx

from .base_provider import AcademicPaper, BaseAcademicProvider

CONSENSUS_API_URL = "https://api.consensus.app/v1/search"


class ConsensusProvider(BaseAcademicProvider):
    name = "consensus"
    display_name = "Consensus AI (Peer-Reviewed Evidence)"
    description = "Medidor de consenso científico e sínteses diretas de mais de 200M+ de papers."

    def search(self, query: str, limit: int = 5, **kwargs) -> List[AcademicPaper]:
        api_key = os.getenv("CONSENSUS_API_KEY", "").strip()
        if not api_key:
            return []

        headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json"
        }
        params = {
            "query": query,
            "include_full_text_chunks": "true"
        }
        if kwargs.get("open_access"):
            params["open_access"] = "true"

        papers: List[AcademicPaper] = []
        try:
            with httpx.Client(timeout=25) as client:
                resp = client.get(CONSENSUS_API_URL, headers=headers, params=params)
                if resp.status_code == 200:
                    data = resp.json()
                    raw_papers = data.get("papers", []) or data.get("results", []) or []
                    for p in raw_papers[:limit]:
                        authors = p.get("authors", [])
                        if isinstance(authors, str):
                            authors = [authors]
                        year = None
                        try:
                            year = int(p.get("year")) if p.get("year") else None
                        except (ValueError, TypeError):
                            pass

                        doi = p.get("doi", "")
                        url = p.get("url") or (f"https://doi.org/{doi}" if doi else "")
                        takeaway = p.get("takeaway") or p.get("summary") or ""

                        paper = AcademicPaper(
                            title=p.get("title", "Sem título").strip(),
                            authors=authors,
                            year=year,
                            venue=p.get("journal", "") or p.get("venue", "Periódico Revisado"),
                            doi=doi,
                            url=url,
                            abstract=p.get("abstract", ""),
                            source_provider=self.name,
                            study_type=p.get("study_type", "Artigo Científico"),
                            consensus_takeaway=takeaway,
                            raw_data=p
                        )
                        papers.append(paper)
        except Exception:
            pass

        return papers
