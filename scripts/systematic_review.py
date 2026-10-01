# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "rich>=13.7.0",
#     "pyyaml>=6.0.1",
# ]
# ///
"""
=============================================================================
SYSTEMATIC REVIEW & EXTRACTION MATRIX ENGINE - Academic PKM
=============================================================================
Implementa as diretrizes seminais de Revisão Sistemática (PRISMA 2020, SALSA,
Booth 2022, Boland 2017) no monorepo:
1. Geração de Protocolos Formais de Revisão (PRISMA-P / PICO / SPIDER).
2. Construção de Matrizes de Extração e Triagem (Markdown & CSV).
=============================================================================
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
import unicodedata
from datetime import datetime
from pathlib import Path
from typing import List, Optional

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from core import LAKE_DIR, PROTOCOLS_DIR

console = Console(force_terminal=True)


def sanitize_slug(name: str) -> str:
    name = unicodedata.normalize("NFKD", name)
    name = "".join(c for c in name if not unicodedata.combining(c))
    name = re.sub(r"[^\w\s-]", "", name).strip()
    name = re.sub(r"[-\s]+", "_", name)
    return name.lower()[:60] or "protocol"


def generate_protocol(
    title: str,
    framework: str = "pico",
    author: str = "Pesquisador",
) -> Path:
    """Gera um protocolo formal de revisão sistemática aderente ao PRISMA-P."""
    PROTOCOLS_DIR.mkdir(parents=True, exist_ok=True)
    slug = sanitize_slug(title)
    target_path = PROTOCOLS_DIR / f"protocolo_{slug}.md"

    now_iso = datetime.now().isoformat()
    date_str = datetime.now().strftime("%d/%m/%Y")

    is_pico = framework.lower() == "pico"
    scope_section = (
        "| Elemento PICO | Descrição Operacional |\n"
        "|---|---|\n"
        "| **P (População/Problema)** | Definir a população-alvo, corpus ou contexto tecnológico |\n"
        "| **I (Intervenção)** | Modelo, método, técnica ou intervenção avaliada |\n"
        "| **C (Comparação)** | Linha de base (baseline), abordagem tradicional ou controle |\n"
        "| **O (Desfecho/Outcome)** | Métricas primárias (ex: acurácia, latência, fidedignidade, custo) |\n"
    ) if is_pico else (
        "| Elemento SPIDER | Descrição Operacional |\n"
        "|---|---|\n"
        "| **S (Sample)** | Amostra ou contexto de análise |\n"
        "| **PI (Phenomenon of Interest)** | Fenômeno comportamental, técnico ou cognitivo sob escrutínio |\n"
        "| **D (Design)** | Abordagens de pesquisa aceitas (estudo de caso, survey, experimento) |\n"
        "| **E (Evaluation)** | Resultados qualitativos ou métricas de percepção |\n"
        "| **R (Research type)** | Qualitativo, quantitativo ou métodos mistos |\n"
    )

    content = f"""---
title: "Protocolo de Revisão Sistemática: {title}"
type: systematic_review_protocol
framework: "{framework.upper()}"
author: "{author}"
date: '{now_iso}'
status: "congelado_pre_busca"
tags: [revisao_sistematica, protocolo, prisma_p, salsa, metodologia]
---

# 📋 Protocolo de Revisão Sistemática: {title}

**Autor Principal:** {author}  
**Data de Registro do Protocolo:** {date_str}  
**Framework de Escopo:** `{framework.upper()}` (Diretrizes PRISMA-P & SALSA)  
**Status:** `Em Execução (Congelado pré-coleta para controle de viés)`  

---

## 1. Justificativa & Contextualização Teórica
*Descreva brevemente a lacuna científica fundamentada no modelo de deficiências da literatura (Creswell, 2022; Wayne Booth, 2024).*

---

## 2. Pergunta Central de Pesquisa ({framework.upper()})
> **Pergunta:** Como [Intervenção/Fenômeno] afeta [População/Contexto] em comparação a [Controle] quanto a [Desfecho]?

{scope_section}

---

## 3. Critérios Formais de Elegibilidade

| Critérios de Inclusão (IC) | Critérios de Exclusão (EC) |
|---|---|
| **IC1:** Artigos publicados em periódicos ou anais de conferências revisados por pares. | **EC1:** Artigos sem texto completo disponível ou resumo inacessível. |
| **IC2:** Estudos que apresentem dados empíricos ou validação formal de artefato. | **EC2:** Artigos de opinião, cartas ao editor ou tutoriais sem metodologia. |
| **IC3:** Publicações no intervalo temporal de [2020 - 2026]. | **EC3:** Estudos fora do escopo ou que não utilizem as métricas definidas no PICO. |
| **IC4:** Idiomas: Inglês e Português. | **EC4:** Estudos duplicados ou versões anteriores de mesmo preprint. |

---

## 4. Fontes de Informação & Estratégia de Busca
A coleta deve ser executada de forma concorrente através da mini-frota `acc fleet`:

- **Bases Científicas Primárias:** arXiv, OpenAlex, CrossRef, Semantic Scholar, Consensus.app.
- **String Booleana Padronizada:**
  ```text
  ("termo_principal" OR "sinonimo_1") AND ("metodo_ou_modelo") AND ("desfecho_alvo")
  ```

---

## 5. Fluxo de Seleção e Triagem (PRISMA 2020)

```mermaid
flowchart TD
    subgraph Fase1["1. Identificação"]
        A["Registros Identificados via acc fleet (n = ...)"]
        B["Registros Únicos após Desduplicação por DOI (n = ...)"]
        A --> B
    end

    subgraph Fase2["2. Triagem"]
        C["Triagem de Título e Resumo (n = ...)"]
        D["Registros Excluídos (n = ...)"]
        B --> C
        C -->|Não elegíveis| D
    end

    subgraph Fase3["3. Elegibilidade"]
        E["Avaliação de Texto Completo (n = ...)"]
        F["Estudos Excluídos com Motivo Declarado (n = ...)"]
        C -->|Elegíveis| E
        E -->|Critérios EC| F
    end

    subgraph Fase4["4. Inclusão"]
        G["Estudos Incluídos na Matriz de Síntese (n = ...)"]
        E -->|Aprovados| G
    end

    classDef step fill:#1e293b,stroke:#38bdf8,stroke-width:2px,color:#f8fafc;
    classDef final fill:#0284c7,stroke:#38bdf8,stroke-width:2px,color:#ffffff;
    class A,B,C,D,E,F step;
    class G final;
```

---

## 6. Procedimento de Extração de Dados e Avaliação de Qualidade
Os artigos aprovados na Fase 3 devem ser transferidos para a matriz de dados:
- Ferramenta de Extração: `acc matrix <arquivo_fleet_ou_termo>`
- Instrumento de Avaliação Crítica: CASP Checklist / RoB 2 / MMAT.

"""
    target_path.write_text(content, encoding="utf-8")
    return target_path


def generate_extraction_matrix(source_path: Path) -> Tuple[Path, Path]:
    """
    Gera uma matriz de extração estruturada em Markdown e CSV
    a partir de um dossiê de busca do Lake ([fleet]_...md).
    """
    PROTOCOLS_DIR.mkdir(parents=True, exist_ok=True)
    slug = sanitize_slug(source_path.stem)
    out_md = PROTOCOLS_DIR / f"matriz_extracao_{slug}.md"
    out_csv = PROTOCOLS_DIR / f"matriz_extracao_{slug}.csv"

    content = source_path.read_text(encoding="utf-8", errors="ignore")

    # Extrai entradas de artigos da síntese
    entries = []
    # Expressão regular para capturar blocos ### N. Titulo
    pattern = r"###\s+(\d+)\.\s+([^\n]+)(.*?)(?=(?:###\s+\d+\.)|\Z)"
    matches = re.findall(pattern, content, re.DOTALL)

    for num, title, block in matches:
        citekey_m = re.search(r"\\cite\{([^}]+)\}", block)
        citekey = citekey_m.group(1) if citekey_m else f"Doc_{num}"

        authors_m = re.search(r"- \*\*Autores:\*\*\s+([^\n]+)", block)
        authors = authors_m.group(1).strip() if authors_m else "N/D"

        venue_m = re.search(r"- \*\*Periódico / Veículo:\*\*\s+([^\n]+)", block)
        venue = venue_m.group(1).strip() if venue_m else "N/D"

        doi_m = re.search(r"https://doi\.org/([^\s\)]+)", block)
        doi = doi_m.group(1).strip() if doi_m else ""

        entries.append({
            "num": num,
            "citekey": citekey,
            "title": title.strip(),
            "authors": authors,
            "venue": venue,
            "doi": doi,
        })

    # 1. Gerar Markdown Matrix
    md_lines = [
        f"# 📊 Matriz Estruturada de Extração e Triagem: {source_path.stem}\n",
        f"*Gerada a partir do dossiê do Lake `{source_path.name}` em {datetime.now().strftime('%d/%m/%Y %H:%M')}.*\n",
        "| # | Chave | Título | Autores / Veículo | Elegibilidade | Objetivo Declarado | Método / Intervenção | Principais Achados | Limitações | Risco de Viés |\n",
        "|---|---|---|---|---|---|---|---|---|---|\n",
    ]

    for e in entries:
        title_esc = e['title'].replace("|", "-")[:45]
        auth_esc = e['authors'].replace("|", "-")[:25]
        md_lines.append(
            f"| {e['num']} | `\\cite{{{e['citekey']}}}` | {title_esc} | {auth_esc} | `[ ] Incluir / [ ] Excluir` | | | | | `Baixo / Médio / Alto` |\n"
        )

    out_md.write_text("".join(md_lines), encoding="utf-8")

    # 2. Gerar CSV Matrix para planilhas / R / Python
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "ID", "Citekey", "Title", "Authors", "Venue", "DOI",
            "Eligibility_Status", "Exclusion_Reason", "Objective",
            "Methodology", "Key_Findings", "Limitations", "Risk_of_Bias"
        ])
        for e in entries:
            writer.writerow([
                e["num"], e["citekey"], e["title"], e["authors"], e["venue"], e["doi"],
                "Pending", "", "", "", "", "", "Unassessed"
            ])

    return out_md, out_csv


def main():
    parser = argparse.ArgumentParser(
        prog="acc protocol / acc matrix",
        description="🌊 Academic PKM — Motor de Protocolos & Matrizes de Revisão Sistemática (PRISMA/SALSA)",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcomando: protocol
    p_proto = subparsers.add_parser("protocol", help="Cria um novo protocolo de revisão sistemática formal")
    p_proto.add_argument("title", help="Título da revisão sistemática ou pergunta de pesquisa")
    p_proto.add_argument("--framework", default="pico", choices=["pico", "spider"], help="Framework de escopo (PICO ou SPIDER)")
    p_proto.add_argument("--author", default="Pesquisador", help="Nome do autor responsável")

    # Subcomando: matrix
    p_mat = subparsers.add_parser("matrix", help="Gera matriz de extração e triagem a partir de um dossiê do Lake")
    p_mat.add_argument("source_file", help="Caminho do dossiê no Lake (ex: resources/_lake/[fleet]_...md)")

    args = parser.parse_args()

    if args.command == "protocol":
        path = generate_protocol(args.title, args.framework, args.author)
        console.print(Panel.fit(
            f"[bold green]✔ Protocolo de Revisão Sistemática Registrado com Sucesso![/bold green]\n"
            f"[bold]Arquivo Gerado:[/bold] file:///{path.as_posix()}\n"
            f"[bold]Framework Utilizado:[/bold] {args.framework.upper()} (PRISMA-P & SALSA)",
            border_style="green"
        ))

    elif args.command == "matrix":
        src = Path(args.source_file)
        if not src.exists():
            # Tenta procurar no Lake
            src = LAKE_DIR / args.source_file
        if not src.exists():
            console.print(f"[red]Erro:[/red] Arquivo fonte não encontrado: {args.source_file}")
            sys.exit(1)

        out_md, out_csv = generate_extraction_matrix(src)
        console.print(Panel.fit(
            f"[bold green]✔ Matriz de Extração e Triagem Criada com Sucesso![/bold green]\n"
            f"- [bold]Matriz Markdown:[/bold] file:///{out_md.as_posix()}\n"
            f"- [bold]Matriz Tabular CSV:[/bold] file:///{out_csv.as_posix()}",
            border_style="green"
        ))


if __name__ == "__main__":
    main()
