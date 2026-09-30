"""
=============================================================================
ACADEMIC PROVIDERS REGISTRY - Academic PKM
=============================================================================
Centraliza os provedores acadêmicos da mini-frota de agentes.
Cada base possui seu adapter especializado, unificando os dados em AcademicPaper.
=============================================================================
"""

from __future__ import annotations

from typing import Dict, List, Type

from .arxiv_provider import ArxivProvider
from .base_provider import AcademicPaper, BaseAcademicProvider, sanitize_filename
from .consensus_provider import ConsensusProvider
from .crossref_provider import CrossRefProvider
from .openalex_provider import OpenAlexProvider
from .semanticscholar_provider import SemanticScholarProvider
from .web_provider import WebHarvesterProvider

PROVIDER_CLASSES: Dict[str, Type[BaseAcademicProvider]] = {
    "arxiv": ArxivProvider,
    "consensus": ConsensusProvider,
    "s2": SemanticScholarProvider,
    "semanticscholar": SemanticScholarProvider,
    "openalex": OpenAlexProvider,
    "crossref": CrossRefProvider,
    "web": WebHarvesterProvider,
    "scrapling": WebHarvesterProvider,
    "firecrawl": WebHarvesterProvider,
}

# Provedores padrão da frota quando nenhum for especificado (gratuitos e sem restrição pesada)
DEFAULT_FLEET_PROVIDERS = ["arxiv", "openalex", "crossref", "s2", "consensus"]


def get_provider(name: str) -> BaseAcademicProvider:
    """Instancia um provedor pelo nome identificador."""
    key = name.lower().strip()
    if key not in PROVIDER_CLASSES:
        raise ValueError(
            f"Provedor '{name}' desconhecido. Disponíveis: {', '.join(sorted(set(PROVIDER_CLASSES.keys())))}"
        )
    return PROVIDER_CLASSES[key]()


def list_providers() -> List[Dict[str, str]]:
    """Retorna metadados de todos os provedores registrados."""
    unique_classes = {cls.name: cls for cls in PROVIDER_CLASSES.values()}
    return [
        {
            "name": p.name,
            "display_name": p.display_name,
            "description": p.description,
        }
        for p in unique_classes.values()
    ]


__all__ = [
    "AcademicPaper",
    "BaseAcademicProvider",
    "sanitize_filename",
    "ArxivProvider",
    "ConsensusProvider",
    "SemanticScholarProvider",
    "OpenAlexProvider",
    "CrossRefProvider",
    "WebHarvesterProvider",
    "PROVIDER_CLASSES",
    "DEFAULT_FLEET_PROVIDERS",
    "get_provider",
    "list_providers",
]
