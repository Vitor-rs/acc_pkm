"""
=============================================================================
WEB & RESEARCH HARVESTER PROVIDER - Academic PKM
=============================================================================
Adaptador de pesquisa web e raspagem profunda baseado em Scrapling (anti-bot local)
e Firecrawl (Cloud Deep Research). Atua como provedor para fontes sem API estruturada
ou para raspagem direta de links acadêmicos.
=============================================================================
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import List

from .base_provider import AcademicPaper, BaseAcademicProvider

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))


class WebHarvesterProvider(BaseAcademicProvider):
    name = "web"
    display_name = "Web Harvester (Scrapling + Firecrawl)"
    description = "Varredura na web aberta e pesquisa profunda para páginas, teses e fontes sem API."

    def search(self, query: str, limit: int = 5, **kwargs) -> List[AcademicPaper]:
        papers: List[AcademicPaper] = []
        is_url = query.strip().startswith("http://") or query.strip().startswith("https://")

        if is_url:
            # Raspagem direta de URL via Scrapling / Firecrawl cascade
            try:
                import web_harvester as wh
                result = wh.harvest_url(query.strip(), save=False)
                if result.get("success"):
                    title = result.get("title") or "Página Web"
                    engine = result.get("engine", "scrapling")
                    markdown = result.get("markdown", "")
                    abstract = markdown[:800] if markdown else ""

                    paper = AcademicPaper(
                        title=title,
                        authors=["Web Resource"],
                        year=None,
                        venue=f"Web ({engine})",
                        url=query.strip(),
                        abstract=abstract,
                        source_provider=self.name,
                        study_type="Recurso Web",
                        raw_data=result,
                    )
                    papers.append(paper)
            except Exception:
                pass
            return papers

        # Busca por papers via Firecrawl Research se chave configurada
        firecrawl_key = os.getenv("FIRECRAWL_API_KEY", "").strip()
        if firecrawl_key:
            try:
                import web_harvester as wh
                raw_results = wh.search_papers(query, limit=limit, save=False)
                for p in raw_results:
                    title = p.get("title") or ""
                    if not title:
                        continue
                    authors = p.get("authors") or []
                    if isinstance(authors, str):
                        authors = [authors]
                    pid = p.get("id") or ""
                    doi = p.get("doi") or (f"10.48550/ARXIV.{pid}" if pid.startswith("arxiv") else "")
                    url = p.get("url") or (f"https://doi.org/{doi}" if doi else "")

                    paper = AcademicPaper(
                        title=title,
                        authors=authors,
                        year=p.get("year"),
                        venue=p.get("venue") or "Literatura Web / Preprint",
                        doi=doi,
                        url=url,
                        abstract=p.get("abstract", ""),
                        source_provider=self.name,
                        study_type="Artigo Web",
                        raw_data=p,
                    )
                    papers.append(paper)
            except Exception:
                pass

        return papers
