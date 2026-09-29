# Regras Operacionais do Academic PKM (`acc_pkm`)

## 1. Princípios de Isolamento e Organização do Projeto

- **Escopo Exclusivo:** Este projeto é estritamente **Academic PKM** (Personal Knowledge Management focado em pesquisa científica, metodologia, escrita de teses/dissertações e análise acadêmica). **NÃO tem qualquer relação com o projeto Startuzeiro** (que foca em marketing digital, vendas B2B e infoprodutos). Não misturar dados, temas ou arquivos entre os dois projetos.
- **Raiz Limpa:** Nenhum arquivo solto (scripts Python, arquivos `.bat`, dados temporários ou duplicatas) deve ser colocado na raiz. Utilitários e scripts devem ficar sempre em `scripts/`.
- **Localização Única do Catálogo:** O catálogo web interativo fica **exclusivamente** em `resources/_lake_catalog.html`. Não duplicar na raiz.
- **Data Lake Centralizado:** Todo o acervo (livros, artigos e transcrições de vídeos) fica em `resources/_lake/`.

---

## 2. Comando de Barra `/transcript` (e `/yt`)

Sempre que o usuário enviar uma mensagem iniciando com `/transcript` ou `/yt`:

1. **Interpretar os Parâmetros:**
   - Se o comando for `/transcript reindex` ou `/transcript --reindex`:
     Execute a reindexação autônoma do Lake:
     ```bash
     uv run scripts/yt_transcribe_and_catalog.py reindex
     ```
   - Se forem fornecidas uma ou mais URLs de vídeos:
     Execute a ingestão direta (com suporte a `--tags` e `--translate-to` se especificados):
     ```bash
     uv run scripts/yt_transcribe_and_catalog.py <links_ou_parametros>
     ```
   - Se for fornecida uma URL de playlist do YouTube:
     Execute a extração e ingestão automática de todos os vídeos da playlist:
     ```bash
     uv run scripts/yt_transcribe_and_catalog.py <url_da_playlist>
     ```

2. **Pós-processamento Automático:**
   - O script atualiza o catálogo `resources/_lake_catalog.html` de forma 100% automática ao final de cada execução.
   - Retorne sempre ao usuário os links clicáveis (`file:///...`) dos novos arquivos `.md` gravados em `resources/_lake/` e do catálogo web em `resources/_lake_catalog.html`.
