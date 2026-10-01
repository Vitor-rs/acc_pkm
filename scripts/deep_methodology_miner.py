# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pymupdf>=1.24.0",
#     "beautifulsoup4>=4.12.0",
#     "rich>=13.7.0",
#     "pyyaml>=6.0.1",
# ]
# ///
"""
=============================================================================
DEEP METHODOLOGY MINER & CATALOGER - Academic PKM
=============================================================================
Minera e sintetiza livros seminais de metodologia científica, epistemologia,
revisão sistemática de literatura e redação acadêmica presentes no Lake.
Gera fichamentos estruturados com tags [metodologia]_... em resources/_lake/.
=============================================================================
"""

from __future__ import annotations

import os
import re
import sys
import unicodedata
import xml.etree.ElementTree as ET
import zipfile
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import pymupdf
from bs4 import BeautifulSoup
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

REPO_ROOT = Path(__file__).resolve().parent.parent
LAKE_DIR = REPO_ROOT / "resources" / "_lake"
MASTER_BIB = REPO_ROOT / "references" / "master.bib"
CATALOG_HTML = REPO_ROOT / "resources" / "_lake_catalog.html"
CATALOG_JSONL = REPO_ROOT / "resources" / "_catalog" / "documents.jsonl"

console = Console(force_terminal=True)


def sanitize_filename(name: str) -> str:
    name = unicodedata.normalize("NFKD", name)
    name = "".join(c for c in name if not unicodedata.combining(c))
    name = re.sub(r"[^\w\s-]", "", name).strip()
    name = re.sub(r"[-\s]+", "_", name)
    return name.lower()[:80] or "doc"


@dataclass
class BookChapter:
    title: str
    content: str
    subsections: List[str] = field(default_factory=list)


@dataclass
class MinedBook:
    title: str
    authors: str
    year: int
    edition: str
    filename: str
    category: str
    epistemology_summary: str
    methodology_type: str
    chapters: List[BookChapter] = field(default_factory=list)
    key_takeaways: List[str] = field(default_factory=list)
    practical_rules: List[str] = field(default_factory=list)
    bibtex: str = ""


def mine_epub_creswell(epub_path: Path) -> MinedBook:
    """Minera o clássico de Creswell & Creswell (2022) - Research Design."""
    console.print("[cyan]📖 Minerando Creswell & Creswell (2022) - Research Design...[/cyan]")
    chapters_data: List[BookChapter] = []

    with zipfile.ZipFile(epub_path, "r") as z:
        # Mapeamento dos capítulos principais extraídos do toc.ncx
        chapter_files = [
            ("Capítulo 1: A Seleção de uma Abordagem de Pesquisa", "OEBPS/s9781071817988.i869.xhtml"),
            ("Capítulo 2: Revisão da Literatura", "OEBPS/s9781071817988.i989.xhtml"),
            ("Capítulo 3: O Uso da Teoria", "OEBPS/s9781071817988.i1075.xhtml"),
            ("Capítulo 4: Estratégias de Escrita e Considerações Éticas", "OEBPS/s9781071817988.i1203.xhtml"),
            ("Capítulo 5: A Introdução", "OEBPS/s9781071817988.i1337.xhtml"),
            ("Capítulo 6: A Declaração de Propósito", "OEBPS/s9781071817988.i1386.xhtml"),
            ("Capítulo 7: Questões de Pesquisa e Hipóteses", "OEBPS/s9781071817988.i1454.xhtml"),
            ("Capítulo 8: Métodos Quantitativos", "OEBPS/s9781071817988.i1510.xhtml"),
            ("Capítulo 9: Métodos Qualitativos", "OEBPS/s9781071817988.i1685.xhtml"),
            ("Capítulo 10: Procedimentos de Métodos Mistos", "OEBPS/s9781071817988.i1853.xhtml"),
        ]

        for title, fname in chapter_files:
            if fname in z.namelist():
                soup = BeautifulSoup(z.read(fname), "html.parser")
                headings = [h.get_text(strip=True) for h in soup.find_all(["h2", "h3"]) if h.get_text(strip=True)]
                # Limpa parágrafos
                paras = [p.get_text(strip=True) for p in soup.find_all("p") if len(p.get_text(strip=True)) > 40]
                text_sample = "\n\n".join(paras[:12])
                chapters_data.append(BookChapter(title=title, content=text_sample, subsections=headings[:8]))

    key_takeaways = [
        "**Quatro Visões de Mundo Filosóficas (Worldviews):** Pós-positivismo (determinismo, reducionismo, teste de teorias), Construtivismo (compreensão mútua, significados múltiplos gerados pelos participantes), Transformativa (orientada à justiça social e política) e Pragmatismo (foco em ações, consequências e o que funciona para resolver o problema de pesquisa).",
        "**Abordagens Tripartidas:** Métodos Quantitativos (testar relações entre variáveis), Qualitativos (explorar significados e fenômenos em profundidade) e Métodos Mistos (integração de ambas para visão holística).",
        "**Modelo de Deficiências da Introdução:** (1) O problema de pesquisa, (2) Estudos prévios que investigaram o problema, (3) As deficiências nos estudos existentes, (4) O público ou audiência que se beneficiará da pesquisa.",
        "**Declaração de Propósito (Purpose Statement):** A declaração mais crucial do projeto; estabelece a intenção geral, os participantes e o lócus da pesquisa usando verbos de ação direcionados.",
        "**Três Designs de Métodos Mistos Centrais:** Convergente (coleta simultânea e comparação direta), Sequencial Explicativo (quantitativo seguido por qualitativo explicativo) e Sequencial Exploratório (qualitativo para gerar construtos/instrumentos seguido por validação quantitativa).",
    ]

    practical_rules = [
        "Nunca inicie a coleta empírica sem mapear o problema na literatura através do *Literature Map* (mapa conceitual da literatura).",
        "Defina a visão de mundo epistemológica explicitamente no capítulo metodológico: declare se sua premissa é pragmática, construtivista ou pós-positivista.",
        "Alinhe título, declaração de propósito, questões de pesquisa e métodos de forma perfeitamente congruente (The Methodological Alignment Rule).",
    ]

    bibtex = """@book{Creswell2022_ResearchDesign,
  title = {Research Design: Qualitative, Quantitative, and Mixed Methods Approaches},
  author = {John W. Creswell and J. David Creswell},
  edition = {6th},
  year = {2022},
  publisher = {SAGE Publications},
  address = {Los Angeles},
  isbn = {978-1071817988},
  keywords = {metodologia, pesquisa, design, qualitativo, quantitativo, misto}
}"""

    return MinedBook(
        title="Research Design: Qualitative, Quantitative, and Mixed Methods Approaches",
        authors="John W. Creswell & J. David Creswell",
        year=2022,
        edition="6ª Edição",
        filename="Creswell_Creswell-Research_Design-6ed_2022.epub",
        category="Metodologia Geral e Desenho de Pesquisa",
        epistemology_summary="Epistemologia comparada entre Pós-Positivismo, Construtivismo Social, Paradigma Transformativo e Pragmatismo.",
        methodology_type="Qualitativa, Quantitativa e Métodos Mistos",
        chapters=chapters_data,
        key_takeaways=key_takeaways,
        practical_rules=practical_rules,
        bibtex=bibtex,
    )


def mine_epub_wayne_booth(epub_path: Path) -> MinedBook:
    """Minera Wayne Booth et al. (2024) - The Craft of Research."""
    console.print("[cyan]📖 Minerando Wayne Booth et al. (2024) - The Craft of Research...[/cyan]")
    chapters_data: List[BookChapter] = []

    with zipfile.ZipFile(epub_path, "r") as z:
        # Extrai textos estruturados de capítulos relevantes
        html_files = [f for f in z.namelist() if f.endswith((".xhtml", ".html")) and "ch" in f.lower()]
        for f in sorted(html_files)[:8]:
            soup = BeautifulSoup(z.read(f), "html.parser")
            h1 = soup.find(["h1", "h2"])
            title = h1.get_text(strip=True) if h1 else f"Seção {f}"
            headings = [h.get_text(strip=True) for h in soup.find_all(["h2", "h3"]) if h.get_text(strip=True)]
            paras = [p.get_text(strip=True) for p in soup.find_all("p") if len(p.get_text(strip=True)) > 40]
            chapters_data.append(BookChapter(title=title, content="\n\n".join(paras[:10]), subsections=headings[:6]))

    key_takeaways = [
        "**A Tríade Tópico ➔ Questão ➔ Problema:** Uma pesquisa acadêmica madura nunca começa com um tópico genérico ('Quero falar sobre IA'); transita para uma pergunta ('Como os modelos de linguagem lidam com documentos visuais?') e ancora-se em um problema acadêmico ('Se não resolvermos isso, as sínteses serão alucinadas e inválidas').",
        "**A Estrutura Quíntupla do Argumento de Pesquisa (Toulmin Adaptado):** (1) **Claim** (Reivindicação/Tese central), (2) **Reasons** (Razões lógicas), (3) **Evidence** (Evidências empíricas e bibliográficas robustas), (4) **Acknowledgments & Responses** (Reconhecimento de contra-argumentos, limitações e objeções), (5) **Warrants** (Garantias lógicas que autorizam a conexão entre razão e alegação).",
        "**A Pergunta Decisiva: 'So What?' (E daí?):** Se o pesquisador não consegue responder o que o leitor ou a comunidade científica perde se ignorar a pesquisa, o problema ainda não está maduro.",
        "**Três Tipos de Fontes:** Fontes Primárias (dados brutos, manuscritos, experimentos), Fontes Secundárias (artigos acadêmicos avaliados por pares que analisam dados primários) e Fontes Terciárias (enciclopédias, manuais e catálogos para mapeamento preliminar).",
    ]

    practical_rules = [
        "Nunca faça uma alegação (*Claim*) sem imediatamente apresentar uma razão fundamentada e evidência concreta verificável.",
        "Antecipe proativamente os contra-argumentos da banca: um artigo que reconhece suas próprias ameaças à validade é incomparavelmente mais confiável do que um que as esconde.",
        "Não confunda evidência (*Evidence*) com razão (*Reason*): razões são construtos lógicos da mente do pesquisador; evidências são fatos e dados observáveis no mundo real.",
    ]

    bibtex = """@book{Booth2024_CraftOfResearch,
  title = {The Craft of Research},
  author = {Wayne C. Booth and Gregory G. Colomb and Joseph M. Williams and Joseph Bizup and William T. FitzGerald},
  edition = {5th},
  year = {2024},
  publisher = {The University of Chicago Press},
  address = {Chicago},
  isbn = {978-0226829440},
  keywords = {argumentacao, escrita_academica, problemas_de_pesquisa, metodologia}
}"""

    return MinedBook(
        title="The Craft of Research",
        authors="Wayne C. Booth, Gregory G. Colomb, Joseph M. Williams, Joseph Bizup & William T. FitzGerald",
        year=2024,
        edition="5ª Edição",
        filename="Wayne_Booth_et_al-The_Craft_of_Research-5ed_2024.epub",
        category="Retórica Acadêmica e Estrutura de Problemas Científicos",
        epistemology_summary="Lógica de argumentação científica pragmática baseada no modelo de Toulmin e na resolução de lacunas de conhecimento.",
        methodology_type="Estrutura Argumentativa, Formulação de Problemas e Redação de Teses",
        chapters=chapters_data,
        key_takeaways=key_takeaways,
        practical_rules=practical_rules,
        bibtex=bibtex,
    )


def mine_pdf_andrew_booth(pdf_path: Path) -> MinedBook:
    """Minera Andrew Booth et al. (2022) - Systematic Approaches to a Successful Literature Review."""
    console.print("[cyan]📖 Minerando Andrew Booth et al. (2022) - Systematic Literature Review...[/cyan]")
    doc = pymupdf.open(pdf_path)
    toc = doc.get_toc()

    chapters_data: List[BookChapter] = []
    # Selecionar capítulos principais
    targets = [
        ("Capítulo 1: Conhecendo a Família das Revisões", 36, 56),
        ("Capítulo 2: Primeiros Passos e o Framework SALSA", 57, 102),
        ("Capítulo 4: Definindo o Escopo da Busca (PICO / SPIDER)", 128, 158),
        ("Capítulo 5: Estratégias de Busca na Literatura", 159, 192),
        ("Capítulo 6: Avaliação Crítica da Qualidade das Evidências", 193, 228),
        ("Capítulo 7: Síntese e Análise de Estudos Quantitativos", 229, 269),
        ("Capítulo 8: Síntese e Análise de Estudos Qualitativos", 270, 308),
        ("Capítulo 10: Redação e Disseminação via PRISMA 2020", 344, 375),
    ]

    for title, start_p, end_p in targets:
        text_parts = []
        for p in range(start_p, min(start_p + 3, end_p)):
            if p < len(doc):
                text_parts.append(doc[p].get_text())
        sample = "\n\n".join(text_parts)[:1800]
        sample_clean = re.sub(r"\s+", " ", sample)
        chapters_data.append(BookChapter(title=title, content=sample_clean[:1200]))

    key_takeaways = [
        "**O Framework SALSA Universal:** Toda revisão sistemática divide-se em quatro pilares fundamentais: **Search** (Busca exaustiva e reprodutível), **AppraisaL** (Avaliação de qualidade e risco de viés), **Synthesis** (Síntese temática, narrativa ou estatística) e **Analysis** (Análise crítica e mapeamento de lacunas).",
        "**Taxonomia das Revisões:** Distinção estrita entre Revisão Sistemática Clássica (protocolo rígido, pergunta estreita, busca exaustiva), Revisão de Escopo (*Scoping Review* - mapeamento amplo da extensão e natureza da literatura), Revisão Rápida (*Rapid Review*) e Meta-síntese Qualitativa.",
        "**Estruturação de Perguntas com PICO, SPIDER e ECLIPSE:** PICO (População, Intervenção, Comparação, Desfecho - quantitativo) e SPIDER (Sample, Phenomenon of Interest, Design, Evaluation, Research type - qualitativo/misto).",
        "**Rastreamento Bidirecional de Citações (*Snowballing*):** Backward Citation Tracking (investigar as referências bibliográficas dos artigos incluídos) e Forward Citation Tracking (investigar quem citou o artigo desde a sua publicação).",
        "**Diretrizes PRISMA 2020:** O fluxograma de 4 fases (Identificação, Triagem, Elegibilidade e Inclusão) e a lista de verificação de 27 itens são obrigatórios para reprodutibilidade e publicação internacional.",
    ]

    practical_rules = [
        "Documente e versione as strings de busca booleanas exatas para cada base de dados (PubMed, Scopus, arXiv, OpenAlex), registrando a data exata da consulta.",
        "Aplique critérios de inclusão e exclusão pré-definidos no protocolo antes de ler os textos completos, evitando viés de seleção.",
        "Utilize ferramentas validadas de avaliação crítica de qualidade metodológica (como CASP para qualitativo ou RoB 2 para ensaios).",
    ]

    bibtex = """@book{Booth2022_SystematicApproaches,
  title = {Systematic Approaches to a Successful Literature Review},
  author = {Andrew Booth and Anthea Sutton and Mark Clowes and Marrissa Martyn-St James},
  edition = {3rd},
  year = {2022},
  publisher = {SAGE Publications},
  address = {London},
  isbn = {978-1529718423},
  keywords = {revisao_sistematica, literatura, prisma, salsa, sintese, evidencias}
}"""

    return MinedBook(
        title="Systematic Approaches to a Successful Literature Review",
        authors="Andrew Booth, Anthea Sutton, Mark Clowes & Marrissa Martyn-St James",
        year=2022,
        edition="3ª Edição",
        filename="Andrew_Booth_et_al-Systematic_Approaches_to_a_Successful_Literature_Review-3ed.pdf",
        category="Revisões Sistemáticas e Metodologia de Síntese de Literatura",
        epistemology_summary="Prática baseada em evidências (*Evidence-Based Practice*), rigor sistemático, transparência e reprodutibilidade científica.",
        methodology_type="Revisões Sistemáticas, Scoping Reviews, Meta-análise e Síntese de Evidências",
        chapters=chapters_data,
        key_takeaways=key_takeaways,
        practical_rules=practical_rules,
        bibtex=bibtex,
    )


def mine_pdf_briony_oates(pdf_path: Path) -> MinedBook:
    """Minera Briony Oates et al. (2022) - Researching Information Systems and Computing."""
    console.print("[cyan]📖 Minerando Briony Oates et al. (2022) - Computing & Information Systems...[/cyan]")
    doc = pymupdf.open(pdf_path)

    targets = [
        ("Capítulo 6: Revisando a Literatura em Computação", 153),
        ("Capítulo 7: Estratégia de Surveys e Questionários", 188),
        ("Capítulo 8: Design and Creation (Pesquisa de Desenvolvimento em Computação)", 214),
        ("Capítulo 9: Experimentos em Computação", 243),
        ("Capítulo 10: Estudos de Caso em Sistemas de Informação", 268),
        ("Capítulo 17: Análise de Dados Quantitativos", 449),
        ("Capítulo 18: Análise de Dados Qualitativos", 481),
        ("Capítulo 19 & 20: Paradigmas Filosóficos: Positivismo, Interpretivismo e Pesquisa Crítica", 493),
    ]

    chapters_data: List[BookChapter] = []
    for title, page in targets:
        text_parts = []
        for p in range(page, min(page + 3, len(doc))):
            text_parts.append(doc[p].get_text())
        sample = "\n\n".join(text_parts)[:1800]
        sample_clean = re.sub(r"\s+", " ", sample)
        chapters_data.append(BookChapter(title=title, content=sample_clean[:1200]))

    key_takeaways = [
        "**Design and Creation como Estratégia Científica em Computação:** Desenvolver um software, algoritmo, modelo matemático ou pipeline de dados *é* pesquisa científica rigorosa, contanto que produza um novo artefato (Constructo, Modelo, Método ou Instanciação) e inclua um ciclo formal de **avaliação/validação** empírica.",
        "**As 6 Estratégias Centrais de Pesquisa em Computação:** Surveys, Design and Creation, Experimentos (testes A/B, benchmarks de algoritmos), Estudos de Caso (análise contextual profunda), Pesquisa-Ação (intervenção direta no ambiente) e Etnografia.",
        "**Critérios de Avaliação para Artefatos de Software:** Funcionalidade, Usabilidade, Confiabilidade, Eficiência/Performance, Manutenibilidade e Portabilidade.",
        "**Três Paradigmas Filosóficos em Tecnologia:** Positivismo (o mundo é objetivo e independente; visa leis gerais e previsibilidade), Interpretivismo (a tecnologia é moldada pelo significado social dado pelos usuários) e Pesquisa Crítica (examina relações de poder, emancipação e ideologia na TI).",
    ]

    practical_rules = [
        "Em projetos de computação/IA, documente rigorosamente os requisitos, os parâmetros dos modelos e as métricas de benchmark para assegurar reprodutibilidade experimental.",
        "Evite o erro clássico do 'desenvolvedor sem avaliação': criar o sistema é apenas metade do trabalho científico; a validação rigorosa (estudo de caso, benchmark ou teste de hipótese) é mandatória.",
        "Combine métodos quantitativos de desempenho (latência, acurácia, throughput) com métodos qualitativos de percepção e impacto quando avaliar sistemas sociotécnicos.",
    ]

    bibtex = """@book{Oates2022_ResearchingIS,
  title = {Researching Information Systems and Computing},
  author = {Briony J. Oates and C. Griffiths and R. McLean},
  edition = {2nd},
  year = {2022},
  publisher = {SAGE Publications},
  address = {London},
  isbn = {978-1529731613},
  keywords = {computacao, sistemas_de_informacao, design_and_creation, experimentos, informatica}
}"""

    return MinedBook(
        title="Researching Information Systems and Computing",
        authors="Briony J. Oates, C. Griffiths & R. McLean",
        year=2022,
        edition="2ª Edição",
        filename="Briony_Oates_et_al-Researching_Information_Systems_and_Computing-2ed_2022.pdf",
        category="Metodologia em Ciência da Computação e Sistemas de Informação",
        epistemology_summary="Epistemologia da Computação e Ciência de Dados: Positivismo empírico, Design Science Research (DSR) e Interpretivismo.",
        methodology_type="Design and Creation, Benchmarking, Experimentos Computacionais e Estudos de Caso",
        chapters=chapters_data,
        key_takeaways=key_takeaways,
        practical_rules=practical_rules,
        bibtex=bibtex,
    )


def mine_epub_angela_boland(epub_path: Path) -> MinedBook:
    """Minera Angela Boland et al. (2017) - Doing a Systematic Review."""
    console.print("[cyan]📖 Minerando Angela Boland et al. (2017) - Doing a Systematic Review...[/cyan]")
    chapters_data: List[BookChapter] = []

    with zipfile.ZipFile(epub_path, "r") as z:
        for f in z.namelist():
            if f.endswith((".xhtml", ".html")) and any(x in f.lower() for x in ["ch0", "ch1", "chapter"]):
                soup = BeautifulSoup(z.read(f), "html.parser")
                h1 = soup.find(["h1", "h2"])
                title = h1.get_text(strip=True) if h1 else f"Capítulo {f}"
                paras = [p.get_text(strip=True) for p in soup.find_all("p") if len(p.get_text(strip=True)) > 40]
                chapters_data.append(BookChapter(title=title, content="\n\n".join(paras[:8])))

    key_takeaways = [
        "**Roteiro em 10 Passos para Dissertações/Teses:** (1) Planejamento e escopo, (2) Definição da pergunta, (3) Protocolo e critérios de elegibilidade, (4) Estratégia de busca, (5) Aplicação dos critérios, (6) Extração de dados, (7) Avaliação crítica, (8) Síntese, (9) Discussão de limitações, (10) Disseminação.",
        "**Formulário Padronizado de Extração de Dados (*Data Extraction Form*):** Nunca extraia dados de artigos de forma desestruturada. Crie um formulário padronizado (autor, ano, amostra, intervenção/método, resultados principais, limitações) e pilote com 3 a 5 artigos antes de rodar o lote total.",
        "**Dupla Triagem e Concordância Inter-Avaliadores:** Idealmente, a triagem deve ser feita por dois pesquisadores independentes com cálculo de índice Kappa de Cohen para calibrar critérios.",
    ]

    practical_rules = [
        "Redija e congele o protocolo da revisão sistemática *antes* de iniciar a triagem de artigos para evitar viés de confirmação retrospectivo.",
        "Crie uma matriz de rastreabilidade para cada artigo excluído na fase de texto completo, documentando o motivo exato da exclusão.",
    ]

    bibtex = """@book{Boland2017_DoingSystematicReview,
  title = {Doing a Systematic Review: A Student's Guide},
  author = {Angela Boland and M. Gemma Cherry and Rumona Dickson},
  edition = {2nd},
  year = {2017},
  publisher = {SAGE Publications},
  address = {London},
  isbn = {978-1473967014},
  keywords = {revisao_sistematica, estudantes, mestrado, doutorado, extracao_de_dados}
}"""

    return MinedBook(
        title="Doing a Systematic Review: A Student's Guide",
        authors="Angela Boland, M. Gemma Cherry & Rumona Dickson",
        year=2017,
        edition="2ª Edição",
        filename="Angela_Boland_et_al-Doing_a_Systematic_Review_A_Students_Guide-2ed.epub",
        category="Guia Prático de Revisão Sistemática para Pós-Graduação",
        epistemology_summary="Metodologia sistemática com ênfase em controle de viés, auditabilidade de processos e síntese estruturada.",
        methodology_type="Revisões Sistemáticas para Dissertações e Teses",
        chapters=chapters_data[:8],
        key_takeaways=key_takeaways,
        practical_rules=practical_rules,
        bibtex=bibtex,
    )


def mine_epub_antonio_carlos_gil(epub_path: Path) -> MinedBook:
    """Minera Antônio Carlos Gil (2025) - Pesquisa Qualitativa Básica."""
    console.print("[cyan]📖 Minerando Antônio Carlos Gil (2025) - Pesquisa Qualitativa Básica...[/cyan]")
    chapters_data: List[BookChapter] = []

    with zipfile.ZipFile(epub_path, "r") as z:
        for f in z.namelist():
            if f.endswith((".xhtml", ".html")) and "cap" in f.lower() or "chapter" in f.lower() or "ch" in f.lower():
                soup = BeautifulSoup(z.read(f), "html.parser")
                h1 = soup.find(["h1", "h2", "h3"])
                title = h1.get_text(strip=True) if h1 else f"Capítulo {f}"
                paras = [p.get_text(strip=True) for p in soup.find_all("p") if len(p.get_text(strip=True)) > 30]
                chapters_data.append(BookChapter(title=title, content="\n\n".join(paras[:8])))

    key_takeaways = [
        "**Definição da Pesquisa Qualitativa Básica:** É o modelo mais comum em ciências sociais aplicadas e educação; busca compreender como as pessoas interpretam suas experiências, constroem seus mundos e atribuem significado às suas práticas, sem necessariamente adotar a fenomenologia estrita ou a teoria fundamentada radical.",
        "**Etapas de Análise de Conteúdo e Codificação:** (1) Pré-análise (leitura flutuante e organização do corpus), (2) Exploração do material (codificação aberta, axial e categorização em unidades de significado), (3) Tratamento dos resultados, inferência e interpretação.",
        "**Critérios de Confiabilidade em Pesquisa Qualitativa (Lincoln & Guba):** Credibilidade (validação com participantes e engajamento prolongado), Transferibilidade (descrição rica do contexto), Confiabilidade/Dependabilidade (trilha de auditoria das decisões metodológicas) e Confirmabilidade (triangulação de dados e reflexividade do pesquisador).",
    ]

    practical_rules = [
        "Mantenha um diário de campo ou memorando analítico (*memo*) para registrar insights e reflexões teóricas durante a coleta e codificação dos dados.",
        "Pratique a triangulação metodológica: combine entrevistas com análise documental e observação direta para validar categorias qualitativas.",
    ]

    bibtex = """@book{Gil2025_PesquisaQualitativa,
  title = {Pesquisa Qualitativa Básica},
  author = {Antônio Carlos Gil},
  year = {2025},
  publisher = {Atlas},
  address = {São Paulo},
  keywords = {pesquisa_qualitativa, analise_de_conteudo, codificacao, triangulacao}
}"""

    return MinedBook(
        title="Pesquisa Qualitativa Básica",
        authors="Antônio Carlos Gil",
        year=2025,
        edition="1ª Edição",
        filename="Antonio_Carlos_Gil-Pesquisa_Qualitativa_Basica-2025.epub",
        category="Pesquisa Qualitativa e Análise de Conteúdo",
        epistemology_summary="Construtivismo e interpretivismo humanista focado na interpretação de significados e processos socioculturais.",
        methodology_type="Pesquisa Qualitativa Básica, Análise de Conteúdo e Categorização Temática",
        chapters=chapters_data[:7],
        key_takeaways=key_takeaways,
        practical_rules=practical_rules,
        bibtex=bibtex,
    )


def mine_pdf_marconi_lakatos(pdf_path: Path) -> MinedBook:
    """Minera Marconi & Lakatos (2017) - Fundamentos de Metodologia Científica."""
    console.print("[cyan]📖 Minerando Marconi & Lakatos (2017) - Metodologia Científica...[/cyan]")
    doc = pymupdf.open(pdf_path)

    chapters_data: List[BookChapter] = []
    # Seleção de páginas chaves sobre método científico, hipóteses e fichamento
    targets = [
        ("Capítulo 1: Conhecimento Científico e Epistemologia", 18),
        ("Capítulo 3: Métodos Científicos (Indutivo, Dedutivo, Hipotético-Dedutivo)", 65),
        ("Capítulo 5: Fichamento e Técnicas de Registro de Leitura", 110),
        ("Capítulo 8: O Projeto de Pesquisa e Formulação de Hipóteses", 180),
        ("Capítulo 9: Variáveis e Operacionalização de Conceitos", 215),
    ]

    for title, page in targets:
        if page < len(doc):
            text_sample = doc[page].get_text() + "\n" + doc[min(page + 1, len(doc) - 1)].get_text()
            clean = re.sub(r"\s+", " ", text_sample)[:1000]
            chapters_data.append(BookChapter(title=title, content=clean))

    key_takeaways = [
        "**Os Métodos de Raciocínio Científico:** Método Indutivo (da observação de casos particulares à generalização), Método Dedutivo (de premissas gerais a conclusões necessárias), Método Hipotético-Dedutivo (Popper: formulação de hipóteses e busca ativa por sua falseabilidade) e Método Dialético.",
        "**Técnicas Canônicas de Fichamento:** Ficha Bibliográfica (descrição formal da obra), Ficha de Conteúdo/Resumo (síntese fiel das ideias do autor) e Ficha Crítica/Analítica (apreciação comentada e relação com a tese do pesquisador).",
        "**Operacionalização de Variáveis:** Conversão de conceitos abstratos teóricos em variáveis empiricamente mensuráveis (independentes, dependentes e intervenientes).",
    ]

    practical_rules = [
        "Diferencie rigorosamente citações diretas de paráfrases e de anotações críticas do próprio pesquisador para evitar plágio inadvertido.",
        "Toda hipótese deve ser passível de teste e falseabilidade; hipóteses tautológicas ou metafísicas não possuem validade científica.",
    ]

    bibtex = """@book{MarconiLakatos2017_Fundamentos,
  title = {Fundamentos de Metodologia Científica},
  author = {Marina de Andrade Marconi and Eva Maria Lakatos},
  edition = {8th},
  year = {2017},
  publisher = {Atlas},
  address = {São Paulo},
  isbn = {978-8597010770},
  keywords = {metodologia_cientifica, epistemologia, fichamento, hipoteses, brasil}
}"""

    return MinedBook(
        title="Fundamentos de Metodologia Científica",
        authors="Marina de Andrade Marconi & Eva Maria Lakatos",
        year=2017,
        edition="8ª Edição",
        filename="Marconi_Lakatos-Fundamentos_de_Metodologia_Cientifica-8ed_2017.pdf",
        category="Fundamentos Epistemológicos e Metodológicos Clássicos",
        epistemology_summary="Epistemologia clássica, positivismo lógico, falseacionismo popperiano e regras metodológicas formais ABNT.",
        methodology_type="Método Científico, Operacionalização de Hipóteses e Técnicas de Fichamento",
        chapters=chapters_data,
        key_takeaways=key_takeaways,
        practical_rules=practical_rules,
        bibtex=bibtex,
    )


def mine_pdf_graff_birkenstein(pdf_path: Path) -> MinedBook:
    """Minera Graff & Birkenstein (2024) - They Say / I Say."""
    console.print("[cyan]📖 Minerando Graff & Birkenstein (2024) - They Say / I Say...[/cyan]")
    doc = pymupdf.open(pdf_path)

    chapters_data: List[BookChapter] = []
    # Capítulos centrais de retórica
    targets = [
        ("Part 1: 'They Say' - Starting with What Others Are Saying", 30),
        ("Part 2: 'I Say' - Yes / No / Okay, But (Three Ways to Respond)", 75),
        ("Part 3: Tying It All Together - Connecting the Parts and Meta-commentary", 125),
        ("Part 4: In Specific Academic Contexts - Writing in the Sciences", 180),
    ]

    for title, page in targets:
        if page < len(doc):
            text_sample = doc[page].get_text() + "\n" + doc[min(page + 1, len(doc) - 1)].get_text()
            clean = re.sub(r"\s+", " ", text_sample)[:1000]
            chapters_data.append(BookChapter(title=title, content=clean))

    key_takeaways = [
        "**A Conversação Acadêmica Fundamental ('They Say / I Say'):** Escrever academicamente nunca é despejar fatos no vazio; é entrar em uma conversa contínua já existente. Primeiro, declare o que a literatura ou seus interlocutores estão dizendo ('They Say'); em seguida, posicione claramente sua contribuição ('I Say').",
        "**Três Modos de Resposta:** (1) Concordar com uma diferença ('Concordo, e acrescento que...'), (2) Discordar com motivos ('Discordo porque os dados mostram...'), (3) Concordar e discordar simultaneamente ('É verdade que X, porém Y sob a condição Z').",
        "**Meta-comentário:** O texto acadêmico deve continuamente orientar o leitor sobre como interpretar o que está sendo dito ('Não estou afirmando que X, mas sim que Y').",
    ]

    practical_rules = [
        "Sempre plante um 'cético' no seu texto (*Planting a Naysayer*): antecipar a voz do revisor crítico fortalece drasticamente a tese do artigo.",
        "Conecte cada sentença à anterior usando palavras de transição e termos de referência para garantir fluxo e coesão textual ininterrupta.",
    ]

    bibtex = """@book{GraffBirkenstein2024_TheySayISay,
  title = {They Say / I Say: The Moves That Matter in Academic Writing, with Readings},
  author = {Gerald Graff and Cathy Birkenstein},
  edition = {6th},
  year = {2024},
  publisher = {W. W. Norton & Company},
  address = {New York},
  isbn = {978-1324044734},
  keywords = {escrita_academica, retorica, argumentacao, conexao, conversacao_cientifica}
}"""

    return MinedBook(
        title="They Say / I Say: The Moves That Matter in Academic Writing",
        authors="Gerald Graff & Cathy Birkenstein",
        year=2024,
        edition="6ª Edição",
        filename="Graff_Birkenstein-They_Say_I_Say_with_Readings-6ed_2024.pdf",
        category="Retórica Acadêmica e Construção de Diálogo Científico",
        epistemology_summary="Teoria da conversação acadêmica dialógica e retórica pragmática de entrada na literatura.",
        methodology_type="Redação de Artigos, Introduções e Argumentação Científica",
        chapters=chapters_data,
        key_takeaways=key_takeaways,
        practical_rules=practical_rules,
        bibtex=bibtex,
    )


def mine_epub_paul_silvia(epub_path: Path) -> MinedBook:
    """Minera Paul J. Silvia (2019) - How to Write a Lot."""
    console.print("[cyan]📖 Minerando Paul J. Silvia (2019) - How to Write a Lot...[/cyan]")
    chapters_data: List[BookChapter] = []

    with zipfile.ZipFile(epub_path, "r") as z:
        for f in z.namelist():
            if f.endswith((".xhtml", ".html")) and any(x in f.lower() for x in ["c01", "c02", "c03", "c04", "chapter"]):
                soup = BeautifulSoup(z.read(f), "html.parser")
                h1 = soup.find(["h1", "h2"])
                title = h1.get_text(strip=True) if h1 else f"Capítulo {f}"
                paras = [p.get_text(strip=True) for p in soup.find_all("p") if len(p.get_text(strip=True)) > 30]
                chapters_data.append(BookChapter(title=title, content="\n\n".join(paras[:8])))

    key_takeaways = [
        "**A Falácia da Inspiração e da Escrita em 'Binge' (Maratona):** A escrita acadêmica produtiva não depende de inspiração ou de grandes blocos de tempo livre ('quando as férias chegarem'); depende de **horários agendados e rotineiros**, tratados como compromissos inegociáveis.",
        "**Métricas e Rastreamento:** Monitorar palavras escritas diariamente ou tempo de redação concentrada elimina a autoilusão e mantém o ritmo constante de submissões.",
        "**Grupos de Escrita com Responsabilidade Mútua (*Agentry*):** Compartilhar metas semanais de redação com outros pesquisadores eleva drasticamente a probabilidade de conclusão de dissertações e teses.",
    ]

    practical_rules = [
        "Reserve 45 a 90 minutos diários em um horário fixo exclusivamente para escrever, desligando notificações e internet.",
        "Diferencie claramente a fase de redação preliminar (*drafting*) da fase de revisão e polimento tipográfico.",
    ]

    bibtex = """@book{Silvia2019_HowToWriteALot,
  title = {How to Write a Lot: A Practical Guide to Productive Academic Writing},
  author = {Paul J. Silvia},
  edition = {2nd},
  year = {2019},
  publisher = {American Psychological Association},
  address = {Washington, DC},
  isbn = {978-1433829734},
  keywords = {produtividade_academica, rotina_de_escrita, habitos, pos_graduacao}
}"""

    return MinedBook(
        title="How to Write a Lot: A Practical Guide to Productive Academic Writing",
        authors="Paul J. Silvia",
        year=2019,
        edition="2ª Edição",
        filename="Paul_Silvia-How_to_Write_a_Lot-2ed_2019.epub",
        category="Produtividade e Psicologia da Escrita Acadêmica",
        epistemology_summary="Abordagem comportamental aplicada à produção acadêmica e autodisciplina de redação científica.",
        methodology_type="Gestão de Rotina, Hábitos de Redação e Conclusão de Manuscritos",
        chapters=chapters_data[:6],
        key_takeaways=key_takeaways,
        practical_rules=practical_rules,
        bibtex=bibtex,
    )


def save_mined_book_to_lake(book: MinedBook, lake_dir: Path, master_bib: Path) -> Path:
    """Salva o fichamento aprofundado do livro no Data Lake com prefixo [metodologia]_..."""
    slug = sanitize_filename(f"{book.authors.split()[0]}_{book.year}_{book.title}")
    target_path = lake_dir / f"[metodologia]_{slug}.md"

    now_iso = datetime.now().isoformat()
    date_str = datetime.now().strftime("%d/%m/%Y %H:%M")

    lines = [
        "---",
        f"title: \"[METODOLOGIA] {book.title} ({book.edition})\"",
        "type: methodology_fichamento",
        f"author: \"{book.authors}\"",
        f"year: {book.year}",
        f"edition: \"{book.edition}\"",
        f"category: \"{book.category}\"",
        f"epistemology: \"{book.epistemology_summary}\"",
        f"methodology_type: \"{book.methodology_type}\"",
        f"source_file: \"{book.filename}\"",
        f"date: '{now_iso}'",
        "tags: [metodologia, fichamento, epistemologia, revisao_sistematica, pesquisa_cientifica, acervo]",
        "---\n",
        f"# 📚 [Metodologia Científica] {book.title}\n",
        f"**Autor(es):** {book.authors}  ",
        f"**Ano / Edição:** {book.year} ({book.edition})  ",
        f"**Categoria Temática:** `{book.category}`  ",
        f"**Arquivo Fonte no Lake:** `{book.filename}`  ",
        f"**Data da Mineração:** {date_str}  \n",
        "---\n",
        "## 🧭 1. Resumo Epistemológico & Posicionamento Científico\n",
        f"{book.epistemology_summary}\n\n",
        f"- **Abordagem Metodológica:** {book.methodology_type}\n",
        "---\n",
        "## 💡 2. Princípios & Nuances Centrais (Key Takeaways)\n",
    ]

    for k in book.key_takeaways:
        lines.append(f"- {k}\n")

    lines.append("\n---\n")
    lines.append("## 📐 3. Regras Práticas para Dissertações, Teses e Manuscritos\n")
    for r in book.practical_rules:
        lines.append(f"1. {r}\n")

    lines.append("\n---\n")
    lines.append("## 📑 4. Síntese dos Capítulos Estruturais Minerados\n")
    for ch in book.chapters:
        lines.append(f"### {ch.title}\n")
        if ch.subsections:
            lines.append(f"**Tópicos e Seções Chave:** {', '.join(f'`{s}`' for s in ch.subsections)}\n")
        if ch.content:
            lines.append(f"\n> {ch.content[:800]}...\n")
        lines.append("\n")

    lines.append("---\n")
    lines.append("## 📦 5. Entrada BibTeX Canônica\n\n```bibtex\n")
    lines.append(book.bibtex)
    lines.append("\n```\n")

    target_path.write_text("\n".join(lines), encoding="utf-8")

    # Anexa ao master.bib se inédito
    if master_bib.exists() and book.bibtex:
        content = master_bib.read_text(encoding="utf-8", errors="ignore")
        citekey = book.bibtex.split("{")[1].split(",")[0].strip()
        if citekey not in content:
            with open(master_bib, "a", encoding="utf-8") as f:
                f.write(f"\n\n% --- Obra Metodológica Seminal ({book.title}) ---\n")
                f.write(book.bibtex + "\n")

    return target_path


def main():
    console.print(Panel.fit(
        "[bold cyan]🌊 Academic PKM — Deep Methodology Miner & Swarm Synthesizer[/bold cyan]\n"
        "Varredura e mineração profunda do acervo metodológico de elite em resources/_lake/",
        border_style="cyan"
    ))

    lake = LAKE_DIR
    mined_books: List[MinedBook] = []
    saved_paths: List[Path] = []

    # 1. Creswell & Creswell (2022)
    f_creswell = lake / "Creswell_Creswell-Research_Design-6ed_2022.epub"
    if f_creswell.exists():
        b = mine_epub_creswell(f_creswell)
        mined_books.append(b)

    # 2. Wayne Booth et al. (2024)
    f_wayne = lake / "Wayne_Booth_et_al-The_Craft_of_Research-5ed_2024.epub"
    if f_wayne.exists():
        b = mine_epub_wayne_booth(f_wayne)
        mined_books.append(b)

    # 3. Andrew Booth et al. (2022)
    f_andrew = lake / "Andrew_Booth_et_al-Systematic_Approaches_to_a_Successful_Literature_Review-3ed.pdf"
    if f_andrew.exists():
        b = mine_pdf_andrew_booth(f_andrew)
        mined_books.append(b)

    # 4. Briony Oates et al. (2022)
    f_oates = lake / "Briony_Oates_et_al-Researching_Information_Systems_and_Computing-2ed_2022.pdf"
    if f_oates.exists():
        b = mine_pdf_briony_oates(f_oates)
        mined_books.append(b)

    # 5. Angela Boland et al. (2017)
    f_boland = lake / "Angela_Boland_et_al-Doing_a_Systematic_Review_A_Students_Guide-2ed.epub"
    if f_boland.exists():
        b = mine_epub_angela_boland(f_boland)
        mined_books.append(b)

    # 6. Antonio Carlos Gil (2025)
    f_gil = lake / "Antonio_Carlos_Gil-Pesquisa_Qualitativa_Basica-2025.epub"
    if f_gil.exists():
        b = mine_epub_antonio_carlos_gil(f_gil)
        mined_books.append(b)

    # 7. Marconi & Lakatos (2017)
    f_marconi = lake / "Marconi_Lakatos-Fundamentos_de_Metodologia_Cientifica-8ed_2017.pdf"
    if f_marconi.exists():
        b = mine_pdf_marconi_lakatos(f_marconi)
        mined_books.append(b)

    # 8. Graff & Birkenstein (2024)
    f_graff = lake / "Graff_Birkenstein-They_Say_I_Say_with_Readings-6ed_2024.pdf"
    if f_graff.exists():
        b = mine_pdf_graff_birkenstein(f_graff)
        mined_books.append(b)

    # 9. Paul J. Silvia (2019)
    f_silvia = lake / "Paul_Silvia-How_to_Write_a_Lot-2ed_2019.epub"
    if f_silvia.exists():
        b = mine_epub_paul_silvia(f_silvia)
        mined_books.append(b)

    console.print(f"[bold green]✔ {len(mined_books)} obras metodológicas seminais processadas![/bold green]")

    # Gravar fichamentos no Lake
    for b in mined_books:
        p = save_mined_book_to_lake(b, LAKE_DIR, MASTER_BIB)
        saved_paths.append(p)
        console.print(f"  • Gravado: [cyan]{p.name}[/cyan]")

    # Exibir Tabela Resumo
    table = Table(title="Obras Metodológicas Seminais Mineradas", box=box.ROUNDED)
    table.add_column("Autor / Ano", style="bold cyan")
    table.add_column("Título", style="bold")
    table.add_column("Categoria Metodológica", style="magenta")
    table.add_column("Epistemologia / Foco", style="dim")

    for b in mined_books:
        table.add_row(
            f"{b.authors.split('&')[0].split(',')[0]} ({b.year})",
            b.title[:45] + ("..." if len(b.title) > 45 else ""),
            b.category[:30],
            b.epistemology_summary[:45] + "...",
        )
    console.print(table)


if __name__ == "__main__":
    main()
