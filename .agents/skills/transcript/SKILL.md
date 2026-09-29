---
name: transcript
description: >-
  Extrai transcrições do YouTube (vídeos individuais, múltiplos links ou playlists inteiras), formata em parágrafos inteligentes com timestamps, armazena no Data Lake (resources/_lake/) em Markdown com YAML frontmatter e atualiza automaticamente o catálogo web interativo (resources/_lake_catalog.html). Use sempre que o usuário invocar o comando de barra /transcript, /yt ou fornecer links/playlists do YouTube para extração ou solicitar reindexação do catálogo.
---

# 📺 YouTube Lake Transcript Skill & Slash Command (`/transcript`)

Esta skill automatiza a ingestão de vídeos e playlists do YouTube para o Data Lake do projeto **acc_pkm** (exclusivamente voltado para pesquisa científica e acadêmica), gerando transcrições estruturadas em Markdown e mantendo o catálogo web interativo sempre atualizado em `resources/_lake_catalog.html`.

---

## ⚡ Comportamento do Comando de Barra (`/transcript`)

Sempre que o usuário enviar uma mensagem iniciando com `/transcript` ou `/yt` (ou enviar URLs do YouTube para transcrever):

### 1. Ingestão de Vídeo Único
```bash
uv run scripts/yt_transcribe_and_catalog.py "<url_do_video>"
```

### 2. Ingestão de Múltiplos Vídeos em Lote
```bash
uv run scripts/yt_transcribe_and_catalog.py "<url1>" "<url2>" "<url3>" --tags "metodologia,pesquisa"
```

### 3. Ingestão de Playlists Completas
Basta passar a URL da playlist diretamente (a extração e expansão de todos os vídeos é 100% automática):
```bash
uv run scripts/yt_transcribe_and_catalog.py "<url_da_playlist>"
```

### 4. Tradução Automática Sob Demanda
```bash
uv run scripts/yt_transcribe_and_catalog.py "<url>" --translate-to pt
```

### 5. Reindexação Independente do Catálogo
Para atualizar o catálogo web sem baixar novos vídeos:
```bash
uv run scripts/yt_transcribe_and_catalog.py reindex
```

---

## 🔄 Fluxo de Execução Automática

Ao executar o comando:
1. **Extração de Metadados:** Obtém título, canal, visualizações, data de publicação, duração e resumo via Google oEmbed e `yt-dlp` (0 chaves de API, 100% gratuito).
2. **Extração de Legendas:** Busca transcrição com cascata inteligente de idiomas (`pt`, `pt-BR`, `en`, `es`) com fallback para ASR e `yt-dlp`.
3. **Formatação Inteligente:** Concatena os trechos em parágrafos coerentes a cada ~30-40 segundos com timestamps legíveis (`[00:00]`, `[01:23]`).
4. **Armazenamento no Lake:** Grava o arquivo Markdown no lake:
   `resources/_lake/<slug_normalizado>_<video_id>.md`
   com YAML frontmatter completo (tags, métricas de leitura, palavras, links).
5. **Atualização Automática do Catálogo:** Reconstrói imediatamente:
   - `resources/_lake_catalog.html` (localização única, sem duplicatas na raiz).
6. **Resposta ao Usuário:** Apresenta sempre os links clicáveis para os arquivos `.md` gerados e para o catálogo HTML.

---

## 🛠️ Execução Direta via Scripts

O script também pode ser executado diretamente pelo terminal ou pelos atalhos Windows dentro de `scripts/`:
- `scripts\transcrever.bat "<url>"`
- `scripts\atualizar_catalogo.bat`
