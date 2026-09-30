---
name: consensus
description: >-
  Pesquisa evidências científicas, medidor de consenso e sínteses acadêmicas baseadas em mais de 200M+ de artigos revisados por pares via Consensus.app (MCP Server e API REST). Permite responder perguntas científicas com estudos reais, extrair study snapshots, gerar fichamentos no Data Lake (resources/_lake/) e enriquecer o master.bib. Use sempre que o usuário invocar os comandos /consensus ou solicitar busca de consensos científicos, ensaios clínicos e sínteses de evidências.
---

# 🔬 Consensus Academic Research Skill (`/consensus`)

Esta skill integra a inteligência científica do **[Consensus.app](https://consensus.app)** diretamente ao ecossistema do **Academic PKM (`acc_pkm`)**.

O Consensus é um mecanismo de busca acadêmica com inteligência artificial que indexa mais de **200 a 400 milhões de artigos científicos revisados por pares** (PubMed, Semantic Scholar, arXiv), permitindo avaliar se a comunidade científica concorda, discorda ou se há neutralidade sobre determinada hipótese ou pergunta de pesquisa (*Consensus Meter*), além de extrair *Study Snapshots* (sínteses de 1 linha de metodologia e achados de cada estudo).

---

## ⚡ Formas de Uso & Comandos

### 1. Chamada via MCP Server do Consensus (`consensus_search`)
O servidor oficial MCP do Consensus está configurado em:
- **Endpoint:** `https://mcp.consensus.app/mcp`
- **Transporte:** `mcp-remote` com suporte a autenticação OAuth 2.0.
- **Ferramenta Principal:** `search` (ou `consensus_search`).

Qualquer agente pode chamar o MCP diretamente para buscar evidências científicas com alto rigor.

### 2. Autorização OAuth no Navegador (`/consensus auth`)
Para autorizar a conexão entre sua conta Consensus e o MCP:
```bash
uv run python scripts/consensus.py auth
```
*Ou dê duplo clique no script Windows:* [`scripts/autorizar_consensus.bat`](file:///c:/Users/user/Documents/Vitor/acc_pkm/scripts/autorizar_consensus.bat).
Isso abrirá seu navegador padrão com a tela oficial do Consensus (`https://consensus.app/oauth/authorize/...`). Ao clicar em **Authorize**, as credenciais seguras são salvas localmente em `~/.mcp-auth/`.

### 3. Busca de Literatura & Evidências no Terminal (`/consensus search`)
```bash
uv run python scripts/acc.py consensus "does exercise improve cognitive function in elderly"
```
- **Salvar fichamento estruturado no Data Lake e BibTeX:**
  ```bash
  uv run python scripts/acc.py consensus "does zinc reduce duration of common cold" --save
  ```
  Com a flag `--save`:
  1. Cria um arquivo Markdown em `resources/_lake/consensus_<slug>.md` com metadados YAML.
  2. Extrai e anexa as entradas BibTeX dos artigos ao `references/master.bib`.
  3. Atualiza automaticamente o painel web interativo `resources/_lake_catalog.html`.

### 4. Chave de API REST Direta (Opcional)
Se preferir usar sua chave de API pessoal do Consensus em vez de OAuth:
1. Acesse [consensus.app](https://consensus.app) ➔ Clique no seu perfil no canto inferior esquerdo.
2. Acesse **API & MCP Dashboard** ➔ **Keys and Clients**.
3. Crie uma chave e adicione ao seu arquivo `.env`:
   ```bash
   CONSENSUS_API_KEY=sua_chave_aqui
   ```
