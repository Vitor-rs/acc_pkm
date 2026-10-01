---
title: "Protocolo de Revisão Sistemática: Impacto de LLMs em Processamento de Linguagem Natural"
type: systematic_review_protocol
framework: "SPIDER"
author: "Pesquisador"
date: '2026-09-30T22:38:34.815648'
status: "congelado_pre_busca"
tags: [revisao_sistematica, protocolo, prisma_p, salsa, metodologia]
---

# 📋 Protocolo de Revisão Sistemática: Impacto de LLMs em Processamento de Linguagem Natural

**Autor Principal:** Pesquisador  
**Data de Registro do Protocolo:** 30/09/2026  
**Framework de Escopo:** `SPIDER` (Diretrizes PRISMA-P & SALSA)  
**Status:** `Em Execução (Congelado pré-coleta para controle de viés)`  

---

## 1. Justificativa & Contextualização Teórica
*Descreva brevemente a lacuna científica fundamentada no modelo de deficiências da literatura (Creswell, 2022; Wayne Booth, 2024).*

---

## 2. Pergunta Central de Pesquisa (SPIDER)
> **Pergunta:** Como [Intervenção/Fenômeno] afeta [População/Contexto] em comparação a [Controle] quanto a [Desfecho]?

| Elemento SPIDER | Descrição Operacional |
|---|---|
| **S (Sample)** | Amostra ou contexto de análise |
| **PI (Phenomenon of Interest)** | Fenômeno comportamental, técnico ou cognitivo sob escrutínio |
| **D (Design)** | Abordagens de pesquisa aceitas (estudo de caso, survey, experimento) |
| **E (Evaluation)** | Resultados qualitativos ou métricas de percepção |
| **R (Research type)** | Qualitativo, quantitativo ou métodos mistos |


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

