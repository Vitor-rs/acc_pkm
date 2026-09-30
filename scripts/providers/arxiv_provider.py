"""
=============================================================================
ARXIV ACADEMIC PROVIDER - Academic PKM
=============================================================================
Consulta a API pública e aberta do arXiv (preprints em Ciência da Computação,
Inteligência Artificial, Matemática, Física e Engenharia).
Zero chaves necessárias, 100% gratuito e direto.
=============================================================================
"""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from typing import List, Optional

import httpx

from .base_provider import AcademicPaper, BaseAcademicProvider

ARXIV_API_URL = "https://export.arxiv.org/api/query"
ATOM_NS = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}


class ArxivProvider(BaseAcademicProvider):
    name = "arxiv"
    display_name = "arXiv Preprints (Open Access)"
    description = "Repositório global de preprints científicos de IA, Ciência da Computação e Exatas."

    def search(self, query: str, limit: int = 5, **kwargs) -> List[AcademicPaper]:
        clean_q = re.sub(r"[^\w\s-]", " ", query).strip()
        STOP_WORDS = {"for", "the", "and", "in", "of", "a", "an", "with", "to", "on", "by", "as", "at", "from", "is", "that"}
        clean_words = [w for w in clean_q.split() if len(w) > 2 and w.lower() not in STOP_WORDS]
        if not clean_words:
            clean_words = [w for w in clean_q.split() if len(w) > 1]
        formatted_q = f"all:{'+'.join(clean_words)}" if clean_words else f"all:{clean_q}"

        params = {
            "search_query": formatted_q,
            "start": 0,
            "max_results": limit,
            "sortBy": "relevance",
            "sortOrder": "descending",
        }
        headers = {"User-Agent": "AcademicPKM/1.0 (scientific monorepo harvester)"}

        papers: List[AcademicPaper] = []
        try:
            with httpx.Client(timeout=20, follow_redirects=True) as client:
                resp = client.get(ARXIV_API_URL, params=params, headers=headers)
                resp.raise_for_status()

            root = ET.fromstring(resp.text)
            for entry in root.findall("atom:entry", ATOM_NS):
                title_elem = entry.find("atom:title", ATOM_NS)
                title = title_elem.text.strip().replace("\n", " ") if title_elem is not None and title_elem.text else "Sem Título"
                title = re.sub(r"\s+", " ", title)

                summary_elem = entry.find("atom:summary", ATOM_NS)
                abstract = summary_elem.text.strip().replace("\n", " ") if summary_elem is not None and summary_elem.text else ""
                abstract = re.sub(r"\s+", " ", abstract)

                authors = []
                for author_elem in entry.findall("atom:author", ATOM_NS):
                    name_elem = author_elem.find("atom:name", ATOM_NS)
                    if name_elem is not None and name_elem.text:
                        authors.append(name_elem.text.strip())

                published_elem = entry.find("atom:published", ATOM_NS)
                year = None
                if published_elem is not None and published_elem.text:
                    try:
                        year = int(published_elem.text[:4])
                    except ValueError:
                        pass

                id_elem = entry.find("atom:id", ATOM_NS)
                id_url = id_elem.text.strip() if id_elem is not None and id_elem.text else ""
                arxiv_id = id_url.split("/abs/")[-1] if "/abs/" in id_url else id_url

                # Buscar DOI e links de PDF
                doi_elem = entry.find("arxiv:doi", ATOM_NS)
                doi = doi_elem.text.strip() if doi_elem is not None and doi_elem.text else (f"10.48550/ARXIV.{arxiv_id}" if arxiv_id else "")

                pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf" if arxiv_id else ""
                venue = "arXiv preprint"

                paper = AcademicPaper(
                    title=title,
                    authors=authors,
                    year=year,
                    venue=venue,
                    doi=doi,
                    url=id_url,
                    pdf_url=pdf_url,
                    abstract=abstract,
                    source_provider=self.name,
                    study_type="Preprint",
                )
                papers.append(paper)

        except Exception as e:
            # Fallback seguro para logs sem derrubar outros provedores
            pass

        return papers
