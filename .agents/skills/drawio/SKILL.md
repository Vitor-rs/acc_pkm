---
name: drawio
description: >-
  Cria, edita, exporta e gerencia diagramas visuais científicos e técnicos no formato Diagrams.net / Draw.io (.drawio, .drawio.svg, .drawio.pdf). Permite desenhar fluxogramas metodológicos (PRISMA 2020), modelos conceituais de hipóteses, arquiteturas de sistemas e pipelines de pesquisa. Integra o servidor oficial MCP (@drawio/mcp), exportação vetorial com XML embutido via Draw.io Desktop CLI, edição in-editor no VS Code (hediet.vscode-drawio) e geração de links web zero-install (app.diagrams.net/#create=...). Use sempre que o usuário invocar os comandos /drawio, /diagram, /diagrama ou solicitar criação e edição de diagramas visuais.
---

# 📐 Diagrams.net / Draw.io Academic Skill (`/drawio`, `/diagram`)

Esta skill comanda a infraestrutura de **diagramação visual científica e técnica** do `acc_pkm`. Ela conecta a modelagem conceitual e metodológica ao ecossistema do **Diagrams.net (JGraph/draw.io)** de forma 100% automatizada, reprodutível e integrada ao VS Code, LaTeX e Obsidian.

---

## 🏛️ Os 4 Pilares da Integração no `acc_pkm`

```
                               ┌────────────────────────────────────────┐
                               │           Agente Antigravity           │
                               │      (Geração de XML ou Mermaid)       │
                               └──────────────────┬─────────────────────┘
                                                  │
                 ┌────────────────────────────────┼────────────────────────────────┐
                 ▼                                ▼                                ▼
    ┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
    │     Draw.io MCP Local    │    │   Draw.io Desktop CLI    │    │    Zero-Install Web URL  │
    │      (@drawio/mcp)       │    │     (draw.io.exe)        │    │    (RFC 1951 Deflate)    │
    ├──────────────────────────┤    ├──────────────────────────┤    ├──────────────────────────┤
    │ • search_shapes (10k+)   │    │ • Exportação SVG/PDF     │    │ • app.diagrams.net URL   │
    │ • open_drawio_xml        │    │ • XML embutido (-e)      │    │ • Atalho Windows .url    │
    │ • open_drawio_mermaid    │    │ • Layouts automáticos    │    │ • Compartilhamento ágil  │
    │ • get/set_page           │    │ • Automação headless     │    │ • Sem dependência local  │
    └────────────┬─────────────┘    └─────────────┬────────────┘    └─────────────┬────────────┘
                 │                                │                               │
                 └────────────────────────────────┼───────────────────────────────┘
                                                  │
                                                  ▼
                         ┌──────────────────────────────────────────────────┐
                         │              Arquivos & Artefatos                │
                         ├──────────────────────────────────────────────────┤
                         │ • resources/diagrams/<nome>.drawio               │
                         │ • resources/diagrams/<nome>.drawio.svg (Vetor)   │
                         │ • projects/<manuscrito>/figures/<nome>.drawio.pdf│
                         │ • VS Code Tab (hediet.vscode-drawio)             │
                         └──────────────────────────────────────────────────┘
```

1. **Arquivos Vetoriais Híbridos (`.drawio.svg` / `.drawio.pdf`):** Ao exportar com a flag `-e` (`--embed-diagram`), o arquivo gerado é tanto uma imagem vetorial padrão pronta para compilação em LaTeX (`\includegraphics`) ou Markdown quanto um documento XML 100% editável no Draw.io.
2. **Edição In-Editor no VS Code:** A extensão oficial recomendada `hediet.vscode-drawio` permite abrir e editar qualquer arquivo `.drawio` ou `.drawio.svg` diretamente como uma aba gráfica dentro do VS Code.
3. **Servidor MCP Oficial (`@drawio/mcp`):** Registrado globalmente em `~/.gemini/config/mcp_config.json` e no workspace em `.vscode/mcp.json`. Provê busca semântica de formas (`search_shapes`) em mais de 10.000 bibliotecas (UML, BPMN, AWS, GCP, Azure, Redes, Entidade-Relacionamento).
4. **Links de Edição Web Imediata:** Algoritmo nativo Python RFC 1951 (`zlib.deflateRaw` + base64) para gerar URLs do tipo `https://app.diagrams.net/?grid=0&pv=0#create=...` que abrem instantaneamente no navegador padrão sem truncagem no Windows.

---

## ⚡ Comandos de Linha de Comando (`acc diagram` / `drawio_manager`)

### 1. Diagnóstico do Ambiente
```bash
uv run python scripts/acc.py diagram status
```
*Audita binário CLI, extensão VS Code, servidor MCP, diretórios e templates.*

### 2. Exportação Vetorial com XML Embutido
```bash
# Exportar para SVG com XML embutido (padrão)
uv run python scripts/acc.py diagram export resources/templates/drawio/prisma_2020.drawio -f svg

# Exportar para PDF recortado (--crop) para inclusão direta em LaTeX
uv run python scripts/acc.py diagram export resources/templates/drawio/prisma_2020.drawio -f pdf

# Exportar para PNG de alta resolução (2x scale)
uv run python scripts/acc.py diagram export resources/templates/drawio/prisma_2020.drawio -f png --scale 2.0
```

### 3. Geração de URL Web & Abertura no Navegador
```bash
# Exibe a URL com payload comprimido
uv run python scripts/acc.py diagram url resources/templates/drawio/conceptual_framework.drawio

# Abre diretamente no navegador padrão via atalho seguro .url
uv run python scripts/acc.py diagram url resources/templates/drawio/conceptual_framework.drawio --open
```

### 4. Instanciação de Templates Acadêmicos
```bash
# Copia o template PRISMA 2020 para um projeto de revisão sistemática
uv run python scripts/acc.py diagram template prisma_2020 -o resources/diagrams/minha_revisao_prisma.drawio

# Copia o template de Framework Conceitual
uv run python scripts/acc.py diagram template conceptual_framework -o resources/diagrams/meu_framework.drawio
```

### 5. Busca de Formas no Catálogo MCP
```bash
uv run python scripts/acc.py diagram search "database" -n 5
uv run python scripts/acc.py diagram search "cloud" -n 5
```

---

## 🎨 Templates Acadêmicos Disponíveis (`resources/templates/drawio/`)

1. **`prisma_2020.drawio`:**
   - Fluxograma estrito do padrão PRISMA 2020 para revisões sistemáticas de literatura.
   - Fases: Identificação em bases (arXiv, OpenAlex, S2, CrossRef, Consensus) ➔ Remoção de duplicatas ➔ Triagem de título/resumo ➔ Avaliação de texto completo com justificativas de exclusão ➔ Inclusão qualitativa e quantitativa.
2. **`conceptual_framework.drawio`:**
   - Diagrama conceitual de construtos e hipóteses científicas.
   - Variáveis independentes (X1, X2) ➔ Mecanismo mediador (M) ➔ Desfecho/impacto dependente (Y) + Moderação contextual (Z).

---

## 📐 Diretrizes para Geração de XML mxGraphModel

Ao gerar ou editar arquivos `.drawio` diretamente como XML:

### Estrutura Obrigatória
```xml
<mxGraphModel adaptiveColors="auto">
  <root>
    <mxCell id="0"/>
    <mxCell id="1" parent="0"/>
    <!-- Células do diagrama com parent="1" -->
  </root>
</mxGraphModel>
```

### Regras Críticas de Boa-Formação
1. **NUNCA emitir comentários XML (`<!-- -->`):** Comentários gastam tokens e podem corromper parsers estritos do Draw.io.
2. **Célula de Vértice (Nó):** Deve conter `vertex="1"`, `id` único e filho `<mxGeometry x="..." y="..." width="..." height="..." as="geometry"/>`.
3. **Célula de Aresta (Conector):** Deve conter `edge="1"`, `parent="1"`, `source="id_origem"`, `target="id_destino"` e filho `<mxGeometry relative="1" as="geometry"/>`.
4. **Paleta Científica Elegante:**
   - Azul Científico: `fillColor=#e0f2fe;strokeColor=#0284c7;fontColor=#0369a1;`
   - Verde Validação/Inclusão: `fillColor=#dcfce7;strokeColor=#16a34a;fontColor=#14532d;`
   - Âmbar Atenção/Mediação: `fillColor=#fef3c7;strokeColor=#d97706;fontColor=#92400e;`
   - Vermelho Exclusão/Viés: `fillColor=#fee2e2;strokeColor=#dc2626;fontColor=#991b1b;`
   - Neutro/Bordas: `fillColor=#f8fafc;strokeColor=#cbd5e1;fontColor=#0f172a;`
