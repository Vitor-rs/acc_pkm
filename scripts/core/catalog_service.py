"""
=============================================================================
CATALOG SERVICE - Academic PKM
=============================================================================
Serviço centralizado de varredura do Data Lake (resources/_lake/) e
geração do catálogo interativo web (HTML) e índice estruturado (JSONL).
Totalmente desacoplado de bibliotecas de transcrição e vídeo.
=============================================================================
"""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

from .config import CATALOG_HTML, CATALOG_JSONL, LAKE_DIR


def scan_lake_items(lake_dir: Path) -> List[Dict[str, Any]]:
    """
    Escaneia o diretório _lake e extrai metadados de todas as transcrições (.md)
    e de obras acadêmicas pré-existentes (.pdf, .epub).
    """
    items = []
    if not lake_dir.exists():
        return items

    for f in sorted(lake_dir.iterdir()):
        if f.is_file():
            # 1. Transcrições em Markdown
            if f.suffix.lower() == ".md":
                try:
                    content = f.read_text(encoding="utf-8")
                    meta = {}
                    # Extrair YAML frontmatter se houver
                    if content.startswith("---"):
                        parts = content.split("---", 2)
                        if len(parts) >= 3:
                            meta = yaml.safe_load(parts[1]) or {}
                            body = parts[2]
                        else:
                            body = content
                    else:
                        body = content

                    # Extrair resumo do body se não estiver no frontmatter
                    summary = meta.get("summary") or meta.get("resumo") or ""
                    if not summary:
                        sum_match = re.search(r"## 📌 Assunto Resumido\s*\n+([^\n#]+)", body)
                        if sum_match:
                            summary = sum_match.group(1).strip()
                        else:
                            clean_b = re.sub(r"[#*`>\[\]]", "", body).strip()
                            first_p = clean_b.split("\n\n")[0] if clean_b else ""
                            summary = (first_p[:220] + "...") if len(first_p) > 220 else first_p

                    # Transcrição preview ou Artigo preview
                    trans_match = re.search(r"## 🎙️ Transcrição Completa\s*\n+(.+)", body, re.DOTALL)
                    transcript_preview = ""
                    if trans_match:
                        raw_preview = trans_match.group(1).strip()
                        transcript_preview = raw_preview[:800] + ("..." if len(raw_preview) > 800 else "")
                    else:
                        clean_b = re.sub(r"[#*`>\[\]]", "", body).strip()
                        transcript_preview = clean_b[:800] + ("..." if len(clean_b) > 800 else "")

                    video_id = meta.get("video_id") or ""
                    thumbnail_url = meta.get("thumbnail_url") or (f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg" if video_id else "")
                    is_yt = bool(video_id) or "youtube" in (meta.get("url") or "")

                    tipo = meta.get("tipo") or meta.get("type") or meta.get("source_type") or ("youtube_transcript" if is_yt else "web_article")
                    canal = meta.get("channel") or meta.get("canal") or meta.get("site_name") or meta.get("author") or ("YouTube" if is_yt else "Web")

                    items.append({
                        "id": video_id or f.stem,
                        "tipo": tipo,
                        "titulo": meta.get("title") or meta.get("titulo_original") or f.stem.replace("_", " ").title(),
                        "canal": canal,
                        "canal_url": meta.get("channel_url") or meta.get("url") or "",
                        "data_publicacao": meta.get("publish_date") or meta.get("data_publicacao") or meta.get("scraped_at", "")[:10] if meta.get("scraped_at") else "",
                        "data_transcricao": meta.get("transcription_date") or meta.get("data_transcricao") or meta.get("scraped_at", "")[:10] if meta.get("scraped_at") else "",
                        "duracao": meta.get("duration_formatted") or "",
                        "duracao_segundos": meta.get("duration_seconds") or 0,
                        "views": meta.get("views") or meta.get("visualizacoes") or "",
                        "url_original": meta.get("url") or meta.get("url_original") or "",
                        "idioma": meta.get("language") or "pt",
                        "palavras": meta.get("word_count") or len(body.split()),
                        "resumo": summary,
                        "preview": transcript_preview,
                        "arquivo_rel": f"_lake/{f.name}",
                        "nome_arquivo": f.name,
                        "tags": meta.get("tags") or (["youtube", "transcricao"] if is_yt else ["web", "pesquisa"]),
                        "thumbnail_url": thumbnail_url,
                        "tamanho_bytes": f.stat().st_size,
                    })
                except Exception as e:
                    print(f"⚠️ Erro ao indexar {f.name}: {e}")

            # 2. Documentos do Lake (PDF / EPUB)
            elif f.suffix.lower() in [".pdf", ".epub"]:
                size_mb = round(f.stat().st_size / (1024 * 1024), 2)
                # Tentar extrair autor e título a partir do padrão Nome_Autor-Titulo_do_Livro-Ano.ext
                stem = f.stem
                parts = stem.split("-")
                autor = parts[0].replace("_", " ") if len(parts) > 1 else "Autor Não Identificado"
                titulo = parts[1].replace("_", " ") if len(parts) > 1 else stem.replace("_", " ")
                ano = ""
                for p in parts[2:]:
                    year_match = re.search(r"\b(19\d\d|20\d\d)\b", p)
                    if year_match:
                        ano = year_match.group(1)
                        break

                items.append({
                    "id": f.stem,
                    "tipo": "livro_documento",
                    "extensao": f.suffix.lower().lstrip("."),
                    "titulo": titulo.title(),
                    "canal": autor.title(),
                    "data_publicacao": ano or "N/D",
                    "tamanho_mb": f"{size_mb} MB",
                    "arquivo_rel": f"_lake/{f.name}",
                    "nome_arquivo": f.name,
                    "tags": ["academico", "livro", f.suffix.lower().lstrip(".")],
                    "resumo": f"Obra acadêmica armazenada no Lake ({f.suffix.upper()}, {size_mb} MB).",
                    "preview": f"Arquivo original disponível no acervo local: {f.name}",
                    "tamanho_bytes": f.stat().st_size,
                })

    return items


def generate_catalog_html(lake_items: List[Dict[str, Any]], catalog_file: Path):
    """
    Gera uma interface web de catálogo moderna, interativa, responsiva e 100% autossuficiente
    para visualização, filtragem, busca e leitura de todos os ativos do Lake.
    """
    # Ordenar por data mais recente / nome
    yt_count = sum(1 for i in lake_items if i.get("tipo") == "youtube_transcript")
    doc_count = sum(1 for i in lake_items if i.get("tipo") == "livro_documento")
    web_count = sum(1 for i in lake_items if i.get("tipo") in ["web_article", "academic_paper", "documentation"])
    total_words = sum(i.get("palavras", 0) for i in lake_items if i.get("tipo") in ["youtube_transcript", "web_article", "academic_paper", "documentation"])
    total_sec = sum(i.get("duracao_segundos", 0) for i in lake_items if i.get("tipo") == "youtube_transcript")

    total_hours = round(total_sec / 3600, 1)

    json_payload = json.dumps(lake_items, ensure_ascii=False, indent=2)

    html_template = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>🌊 Academic PKM — Lake Catalog</title>
  <style>
    :root {{
      --bg: #0f172a;
      --surface: #1e293b;
      --surface-hover: #334155;
      --border: #334155;
      --text: #f8fafc;
      --text-muted: #94a3b8;
      --primary: #38bdf8;
      --primary-hover: #0284c7;
      --accent: #818cf8;
      --success: #34d399;
      --warning: #fbbf24;
      --badge-yt: #ef4444;
      --badge-pdf: #f97316;
      --badge-epub: #10b981;
      --radius: 12px;
      --transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    }}

    [data-theme="light"] {{
      --bg: #f8fafc;
      --surface: #ffffff;
      --surface-hover: #f1f5f9;
      --border: #e2e8f0;
      --text: #0f172a;
      --text-muted: #64748b;
      --primary: #0284c7;
      --primary-hover: #0369a1;
      --accent: #6366f1;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      background-color: var(--bg);
      color: var(--text);
      line-height: 1.5;
      padding: 24px;
      min-height: 100vh;
      transition: background-color 0.3s ease;
    }}

    .container {{
      max-width: 1400px;
      margin: 0 auto;
    }}

    /* Header */
    header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 24px;
      padding-bottom: 20px;
      border-bottom: 1px solid var(--border);
      flex-wrap: wrap;
      gap: 16px;
    }}

    .brand {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}

    .brand-icon {{
      font-size: 2.2rem;
      background: linear-gradient(135deg, #38bdf8, #818cf8);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}

    .brand h1 {{
      font-size: 1.75rem;
      font-weight: 800;
      letter-spacing: -0.025em;
    }}

    .brand p {{
      color: var(--text-muted);
      font-size: 0.875rem;
    }}

    .header-actions {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}

    .btn {{
      padding: 8px 16px;
      border-radius: var(--radius);
      border: 1px solid var(--border);
      background: var(--surface);
      color: var(--text);
      cursor: pointer;
      font-size: 0.875rem;
      font-weight: 600;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      transition: var(--transition);
      text-decoration: none;
    }}

    .btn:hover {{
      background: var(--surface-hover);
      border-color: var(--primary);
    }}

    .btn-primary {{
      background: var(--primary);
      color: #0f172a;
      border: none;
    }}

    .btn-primary:hover {{
      background: var(--primary-hover);
      color: #ffffff;
    }}

    /* KPIs */
    .kpi-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 16px;
      margin-bottom: 28px;
    }}

    .kpi-card {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 16px 20px;
      display: flex;
      align-items: center;
      gap: 16px;
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }}

    .kpi-icon {{
      font-size: 2rem;
      background: var(--surface-hover);
      width: 52px;
      height: 52px;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 10px;
    }}

    .kpi-info .kpi-value {{
      font-size: 1.5rem;
      font-weight: 700;
      color: var(--text);
    }}

    .kpi-info .kpi-label {{
      font-size: 0.8rem;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }}

    /* Controls Bar */
    .controls {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 16px 20px;
      margin-bottom: 24px;
      display: flex;
      flex-wrap: wrap;
      gap: 16px;
      align-items: center;
      justify-content: space-between;
    }}

    .search-wrapper {{
      position: relative;
      flex: 1;
      min-width: 280px;
    }}

    .search-input {{
      width: 100%;
      padding: 10px 16px 10px 40px;
      border-radius: 8px;
      border: 1px solid var(--border);
      background: var(--bg);
      color: var(--text);
      font-size: 0.95rem;
      outline: none;
      transition: var(--transition);
    }}

    .search-input:focus {{
      border-color: var(--primary);
      box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.2);
    }}

    .search-icon {{
      position: absolute;
      left: 14px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--text-muted);
      font-size: 1rem;
    }}

    .filter-group {{
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
    }}

    .filter-select {{
      padding: 9px 14px;
      border-radius: 8px;
      border: 1px solid var(--border);
      background: var(--bg);
      color: var(--text);
      font-size: 0.875rem;
      outline: none;
      cursor: pointer;
    }}

    .filter-pills {{
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }}

    .pill {{
      padding: 6px 14px;
      border-radius: 20px;
      font-size: 0.825rem;
      font-weight: 600;
      border: 1px solid var(--border);
      background: var(--surface-hover);
      color: var(--text-muted);
      cursor: pointer;
      transition: var(--transition);
    }}

    .pill.active {{
      background: var(--primary);
      color: #0f172a;
      border-color: var(--primary);
    }}

    /* View Switcher */
    .view-switcher {{
      display: flex;
      border: 1px solid var(--border);
      border-radius: 8px;
      overflow: hidden;
    }}

    .view-btn {{
      padding: 8px 12px;
      background: var(--surface);
      border: none;
      color: var(--text-muted);
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 4px;
    }}

    .view-btn.active {{
      background: var(--primary);
      color: #0f172a;
    }}

    /* Cards Grid */
    .catalog-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
      gap: 20px;
    }}

    .card {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      overflow: hidden;
      display: flex;
      flex-direction: column;
      transition: var(--transition);
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }}

    .card:hover {{
      transform: translateY(-3px);
      box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2);
      border-color: var(--primary);
    }}

    .card-media {{
      position: relative;
      width: 100%;
      height: 190px;
      background: #000;
      overflow: hidden;
      display: flex;
      align-items: center;
      justify-content: center;
    }}

    .card-media img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      transition: transform 0.3s ease;
    }}

    .card:hover .card-media img {{
      transform: scale(1.04);
    }}

    .card-media-doc {{
      background: linear-gradient(135deg, #1e293b, #0f172a);
      font-size: 3.5rem;
      color: var(--accent);
    }}

    .card-badge {{
      position: absolute;
      top: 12px;
      left: 12px;
      padding: 4px 10px;
      border-radius: 6px;
      font-size: 0.75rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }}

    .badge-yt {{
      background: var(--badge-yt);
      color: #fff;
    }}

    .badge-doc {{
      background: var(--accent);
      color: #fff;
    }}

    .badge-web {{
      background: #0284c7;
      color: #fff;
    }}

    .card-duration {{
      position: absolute;
      bottom: 12px;
      right: 12px;
      background: rgba(0, 0, 0, 0.8);
      color: #fff;
      padding: 3px 8px;
      border-radius: 4px;
      font-size: 0.75rem;
      font-weight: 700;
    }}

    .card-body {{
      padding: 18px;
      display: flex;
      flex-direction: column;
      flex: 1;
    }}

    .card-title {{
      font-size: 1.05rem;
      font-weight: 700;
      line-height: 1.4;
      margin-bottom: 8px;
      color: var(--text);
    }}

    .card-meta {{
      display: flex;
      align-items: center;
      gap: 12px;
      font-size: 0.825rem;
      color: var(--text-muted);
      margin-bottom: 12px;
      flex-wrap: wrap;
    }}

    .card-summary {{
      font-size: 0.875rem;
      color: var(--text-muted);
      margin-bottom: 16px;
      flex: 1;
      display: -webkit-box;
      -webkit-line-clamp: 3;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }}

    .card-tags {{
      display: flex;
      gap: 6px;
      flex-wrap: wrap;
      margin-bottom: 16px;
    }}

    .tag {{
      background: var(--surface-hover);
      color: var(--primary);
      font-size: 0.75rem;
      padding: 2px 8px;
      border-radius: 4px;
      font-weight: 600;
    }}

    .card-footer {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-top: 12px;
      border-top: 1px solid var(--border);
      gap: 8px;
    }}

    /* Table View */
    .catalog-table-wrap {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      overflow-x: auto;
      display: none;
    }}

    table {{
      width: 100%;
      border-collapse: collapse;
      text-align: left;
      font-size: 0.875rem;
    }}

    th {{
      background: var(--surface-hover);
      color: var(--text-muted);
      padding: 12px 16px;
      font-weight: 600;
      text-transform: uppercase;
      font-size: 0.75rem;
      letter-spacing: 0.05em;
    }}

    td {{
      padding: 14px 16px;
      border-bottom: 1px solid var(--border);
      vertical-align: middle;
    }}

    tr:hover td {{
      background: var(--surface-hover);
    }}

    /* Modal / Drawer Preview */
    .modal-overlay {{
      display: none;
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.7);
      backdrop-filter: blur(4px);
      z-index: 999;
      align-items: center;
      justify-content: center;
      padding: 20px;
    }}

    .modal-overlay.active {{
      display: flex;
    }}

    .modal-content {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      width: 100%;
      max-width: 860px;
      max-height: 85vh;
      display: flex;
      flex-direction: column;
      overflow: hidden;
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.4);
    }}

    .modal-header {{
      padding: 18px 24px;
      border-bottom: 1px solid var(--border);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    .modal-header h3 {{
      font-size: 1.25rem;
      font-weight: 700;
    }}

    .modal-close {{
      background: transparent;
      border: none;
      color: var(--text-muted);
      font-size: 1.5rem;
      cursor: pointer;
      padding: 4px 8px;
    }}

    .modal-body {{
      padding: 24px;
      overflow-y: auto;
      font-size: 0.95rem;
      line-height: 1.7;
    }}

    .transcript-box {{
      background: var(--bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 16px;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-size: 0.85rem;
      white-space: pre-wrap;
      max-height: 420px;
      overflow-y: auto;
      margin-top: 12px;
    }}

    .empty-state {{
      text-align: center;
      padding: 60px 20px;
      color: var(--text-muted);
      grid-column: 1 / -1;
    }}

    .empty-state-icon {{
      font-size: 3rem;
      margin-bottom: 12px;
    }}
  </style>
  <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
  <script>
    document.addEventListener("DOMContentLoaded", () => {{
      if (window.mermaid) {{
        mermaid.initialize({{ startOnLoad: true, theme: 'dark' }});
      }}
    }});
  </script>
</head>
<body>

<div class="container">
  <!-- Header -->
  <header>
    <div class="brand">
      <div class="brand-icon">🌊</div>
      <div>
        <h1>Academic PKM — Lake Catalog</h1>
        <p>Repositório Central de Transcrições do YouTube, Livros Técnicos e Metodologia Científica</p>
      </div>
    </div>
    <div class="header-actions">
      <button class="btn" onclick="toggleTheme()" id="themeBtn">🌓 Tema</button>
      <button class="btn btn-primary" onclick="copyCatalogInfo()">📋 Copiar Sumário</button>
    </div>
  </header>

  <!-- KPI Metrics -->
  <div class="kpi-grid">
    <div class="kpi-card">
      <div class="kpi-icon">🎬</div>
      <div class="kpi-info">
        <div class="kpi-value">{yt_count}</div>
        <div class="kpi-label">Transcrições do YouTube</div>
      </div>
    </div>
    <div class="kpi-card">
      <div class="kpi-icon">⏱️</div>
      <div class="kpi-info">
        <div class="kpi-value">{total_hours}h</div>
        <div class="kpi-label">Tempo Total de Conteúdo</div>
      </div>
    </div>
    <div class="kpi-card">
      <div class="kpi-icon">📝</div>
      <div class="kpi-info">
        <div class="kpi-value">{total_words:,}</div>
        <div class="kpi-label">Palavras Transcritas</div>
      </div>
    </div>
    <div class="kpi-card">
      <div class="kpi-icon">📚</div>
      <div class="kpi-info">
        <div class="kpi-value">{doc_count}</div>
        <div class="kpi-label">Livros & Artigos (.pdf/.epub)</div>
      </div>
    </div>
    <div class="kpi-card">
      <div class="kpi-icon">🌐</div>
      <div class="kpi-info">
        <div class="kpi-value">{web_count}</div>
        <div class="kpi-label">Artigos Web & Papers (.md)</div>
      </div>
    </div>
  </div>

  <!-- Controls Bar -->
  <div class="controls">
    <div class="search-wrapper">
      <span class="search-icon">🔍</span>
      <input type="text" id="searchInput" class="search-input" placeholder="Buscar por título, canal, palavra-chave ou autor..." oninput="renderItems()">
    </div>

    <div class="filter-group">
      <div class="filter-pills">
        <button class="pill active" onclick="setTypeFilter('all', this)">Todos</button>
        <button class="pill" onclick="setTypeFilter('youtube_transcript', this)">🎬 YouTube</button>
        <button class="pill" onclick="setTypeFilter('livro_documento', this)">📚 Livros/PDFs</button>
        <button class="pill" onclick="setTypeFilter('web_article', this)">🌐 Web / Artigos</button>
      </div>

      <select id="sortSelect" class="filter-select" onchange="renderItems()">
        <option value="recent">Adicionados Recentemente</option>
        <option value="title_asc">Título (A-Z)</option>
        <option value="duration_desc">Maior Duração</option>
        <option value="words_desc">Mais Palavras</option>
      </select>

      <div class="view-switcher">
        <button class="view-btn active" id="btnCards" onclick="setView('cards')">⊞ Cards</button>
        <button class="view-btn" id="btnTable" onclick="setView('table')">☰ Tabela</button>
      </div>
    </div>
  </div>

  <!-- Content Container -->
  <div id="catalogGrid" class="catalog-grid"></div>

  <div id="catalogTableWrap" class="catalog-table-wrap">
    <table>
      <thead>
        <tr>
          <th>Tipo</th>
          <th>Título</th>
          <th>Canal / Autor</th>
          <th>Data</th>
          <th>Duração / Tam.</th>
          <th>Tags</th>
          <th>Ações</th>
        </tr>
      </thead>
      <tbody id="catalogTableBody"></tbody>
    </table>
  </div>
</div>

<!-- Modal Preview -->
<div class="modal-overlay" id="previewModal" onclick="closeModal(event)">
  <div class="modal-content" onclick="event.stopPropagation()">
    <div class="modal-header">
      <h3 id="modalTitle">Prévia</h3>
      <button class="modal-close" onclick="closeModal()">&times;</button>
    </div>
    <div class="modal-body">
      <div id="modalMeta" style="margin-bottom: 12px; color: var(--text-muted); font-size: 0.9rem;"></div>
      <h4>📌 Resumo</h4>
      <p id="modalSummary" style="margin-bottom: 18px;"></p>
      <div id="modalTranscriptSection">
        <h4>🎙️ Amostra da Transcrição</h4>
        <div id="modalTranscript" class="transcript-box"></div>
      </div>
      <div style="margin-top: 20px; display: flex; gap: 12px;">
        <a id="modalFileLink" href="#" class="btn btn-primary">Abrir Arquivo Local (.md)</a>
        <a id="modalYtLink" href="#" target="_blank" class="btn">Assistir no YouTube ↗</a>
      </div>
    </div>
  </div>
</div>

<!-- JSON Data Island -->
<script id="lakeData" type="application/json">
{json_payload}
</script>

<script>
  let items = [];
  try {{
    items = JSON.parse(document.getElementById('lakeData').textContent);
  }} catch(e) {{
    console.error("Falha ao carregar lakeData", e);
  }}

  let currentTypeFilter = 'all';
  let currentView = 'cards';

  function setTypeFilter(type, btn) {{
    currentTypeFilter = type;
    document.querySelectorAll('.filter-pills .pill').forEach(p => p.classList.remove('active'));
    btn.classList.add('active');
    renderItems();
  }}

  function setView(view) {{
    currentView = view;
    document.getElementById('btnCards').classList.toggle('active', view === 'cards');
    document.getElementById('btnTable').classList.toggle('active', view === 'table');
    document.getElementById('catalogGrid').style.display = view === 'cards' ? 'grid' : 'none';
    document.getElementById('catalogTableWrap').style.display = view === 'table' ? 'block' : 'none';
    renderItems();
  }}

  function renderItems() {{
    const query = (document.getElementById('searchInput').value || '').toLowerCase().trim();
    const sort = document.getElementById('sortSelect').value;

    let filtered = items.filter(item => {{
      if (currentTypeFilter !== 'all') {{
        if (currentTypeFilter === 'web_article') {{
          if (!['web_article', 'academic_paper', 'documentation'].includes(item.tipo)) return false;
        }} else if (item.tipo !== currentTypeFilter) {{
          return false;
        }}
      }}
      if (!query) return true;
      const haystack = [
        item.titulo,
        item.canal,
        item.resumo,
        (item.tags || []).join(" ")
      ].join(" ").toLowerCase();
      return haystack.includes(query);
    }});

    // Sorting
    filtered.sort((a, b) => {{
      if (sort === 'title_asc') {{
        return a.titulo.localeCompare(b.titulo);
      }} else if (sort === 'duration_desc') {{
        return (b.duracao_segundos || 0) - (a.duracao_segundos || 0);
      }} else if (sort === 'words_desc') {{
        return (b.palavras || 0) - (a.palavras || 0);
      }}
      return 0; // default order
    }});

    if (currentView === 'cards') {{
      renderCards(filtered);
    }} else {{
      renderTable(filtered);
    }}
  }}

  function renderCards(list) {{
    const grid = document.getElementById('catalogGrid');
    if (list.length === 0) {{
      grid.innerHTML = `
        <div class="empty-state">
          <div class="empty-state-icon">🔎</div>
          <h3>Nenhum conteúdo encontrado</h3>
          <p>Tente ajustar sua busca ou limpar os filtros selecionados.</p>
        </div>
      `;
      return;
    }}

    grid.innerHTML = list.map(item => {{
      const isYT = item.tipo === 'youtube_transcript';
      const isDoc = item.tipo === 'livro_documento';
      const isWeb = ['web_article', 'academic_paper', 'documentation'].includes(item.tipo);

      let badge = '<span class="card-badge badge-doc">Doc</span>';
      if (isYT) badge = '<span class="card-badge badge-yt">YouTube</span>';
      else if (isWeb) badge = '<span class="card-badge badge-web">🌐 Web</span>';
      else if (isDoc) badge = `<span class="card-badge badge-doc">${{item.extensao || 'Livro'}}</span>`;

      const duration = isYT ? `<span class="card-duration">${{item.duracao || '00:00'}}</span>` : (isDoc ? `<span class="card-duration">${{item.tamanho_mb || ''}}</span>` : `<span class="card-duration">${{item.palavras ? item.palavras + ' pal.' : ''}}</span>`);

      const mediaHtml = isYT && item.thumbnail_url
        ? `<img src="${{item.thumbnail_url}}" alt="${{item.titulo}}" loading="lazy" onerror="this.src='data:image/svg+xml;utf8,<svg xmlns=\\'http://www.w3.org/2000/svg\\' width=\\'360\\' height=\\'200\\' fill=\\'%231e293b\\'><rect width=\\'100%\\' height=\\'100%\\'/></svg>'">`
        : `<div class="card-media-doc">${{isYT ? '🎬' : (isWeb ? '🌐' : '📚')}}</div>`;

      const tagsHtml = (item.tags || []).map(t => `<span class="tag">#${{t}}</span>`).join('');
      const linkBtn = item.url_original ? `<a href="${{item.url_original}}" target="_blank" class="btn" style="padding: 6px 12px; font-size: 0.8rem;">${{isYT ? 'Assistir ↗' : 'Fonte ↗'}}</a>` : '';

      return `
        <div class="card">
          <div class="card-media">
            ${{badge}}
            ${{mediaHtml}}
            ${{duration}}
          </div>
          <div class="card-body">
            <h3 class="card-title">${{item.titulo}}</h3>
            <div class="card-meta">
              <span>👤 ${{item.canal}}</span>
              ${{item.data_publicacao ? `<span>📅 ${{item.data_publicacao}}</span>` : ''}}
              ${{item.palavras ? `<span>📝 ${{item.palavras}} palavras</span>` : ''}}
            </div>
            <p class="card-summary">${{item.resumo || 'Sem resumo disponível.'}}</p>
            <div class="card-tags">${{tagsHtml}}</div>
            <div class="card-footer">
              <a href="${{item.arquivo_rel}}" class="btn btn-primary" style="padding: 6px 12px; font-size: 0.8rem;">Abrir Arquivo</a>
              <div style="display: flex; gap: 6px;">
                <button class="btn" style="padding: 6px 12px; font-size: 0.8rem;" onclick="openPreview('${{item.id}}')">Ver Prévia</button>
                ${{linkBtn}}
              </div>
            </div>
          </div>
        </div>
      `;
    }}).join('');
  }}

  function renderTable(list) {{
    const tbody = document.getElementById('catalogTableBody');
    if (list.length === 0) {{
      tbody.innerHTML = `<tr><td colspan="7" style="text-align: center; padding: 40px;">Nenhum conteúdo encontrado.</td></tr>`;
      return;
    }}

    tbody.innerHTML = list.map(item => {{
      const isYT = item.tipo === 'youtube_transcript';
      const isWeb = ['web_article', 'academic_paper', 'documentation'].includes(item.tipo);
      const typeLabel = isYT ? '🎬 Transcrição' : (isWeb ? '🌐 Artigo Web' : `📚 ${{item.extensao ? item.extensao.toUpperCase() : 'Doc'}}`);
      const dur = isYT ? item.duracao : (item.tamanho_mb || (item.palavras ? item.palavras + ' pal.' : '-'));
      const tags = (item.tags || []).map(t => `<span class="tag">#${{t}}</span>`).join(' ');

      return `
        <tr>
          <td><strong>${{typeLabel}}</strong></td>
          <td><a href="${{item.arquivo_rel}}" style="color: var(--primary); text-decoration: none; font-weight: 600;">${{item.titulo}}</a></td>
          <td>${{item.canal}}</td>
          <td>${{item.data_publicacao || '-'}}</td>
          <td>${{dur || '-'}}</td>
          <td>${{tags}}</td>
          <td>
            <div style="display: flex; gap: 6px;">
              <button class="btn" style="padding: 4px 8px; font-size: 0.75rem;" onclick="openPreview('${{item.id}}')">Prévia</button>
              ${{item.url_original ? `<a href="${{item.url_original}}" target="_blank" class="btn" style="padding: 4px 8px; font-size: 0.75rem;">${{isYT ? 'Vídeo ↗' : 'Fonte ↗'}}</a>` : ''}}
            </div>
          </td>
        </tr>
      `;
    }}).join('');
  }}

  function openPreview(id) {{
    const item = items.find(i => i.id === id);
    if (!item) return;

    document.getElementById('modalTitle').textContent = item.titulo;
    document.getElementById('modalMeta').innerHTML = `
      Canal/Autor: <strong>${{item.canal}}</strong> |
      Publicação: <strong>${{item.data_publicacao || 'N/D'}}</strong>
      ${{item.duracao ? ` | Duração: <strong>${{item.duracao}}</strong>` : ''}}
      ${{item.palavras ? ` | Palavras: <strong>${{item.palavras}}</strong>` : ''}}
    `;
    document.getElementById('modalSummary').textContent = item.resumo || 'Sem resumo disponível.';

    const modalTranscriptSec = document.getElementById('modalTranscriptSection');
    const modalTranscript = document.getElementById('modalTranscript');
    if (item.preview) {{
      modalTranscriptSec.style.display = 'block';
      modalTranscript.textContent = item.preview;
    }} else {{
      modalTranscriptSec.style.display = 'none';
    }}

    const fileLink = document.getElementById('modalFileLink');
    fileLink.href = item.arquivo_rel;
    fileLink.textContent = item.tipo === 'youtube_transcript' ? 'Abrir Transcrição (.md)' : 'Abrir Obra Original';

    const ytLink = document.getElementById('modalYtLink');
    if (item.url_original) {{
      ytLink.href = item.url_original;
      ytLink.style.display = 'inline-flex';
    }} else {{
      ytLink.style.display = 'none';
    }}

    document.getElementById('previewModal').classList.add('active');
  }}

  function closeModal(e) {{
    document.getElementById('previewModal').classList.remove('active');
  }}

  function toggleTheme() {{
    const cur = document.documentElement.getAttribute('data-theme');
    const next = cur === 'light' ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('lake_theme', next);
  }}

  function copyCatalogInfo() {{
    const text = `🌊 Academic PKM Lake Catalog\\nTotal de Itens: ${{items.length}}\\nTotal Transcrições: ${{items.filter(i => i.tipo === 'youtube_transcript').length}}\\nTotal Livros/PDFs: ${{items.filter(i => i.tipo === 'livro_documento').length}}`;
    navigator.clipboard.writeText(text).then(() => {{
      alert('Resumo do catálogo copiado para a área de transferência!');
    }});
  }}

  // Inicialização
  const savedTheme = localStorage.getItem('lake_theme') || 'dark';
  document.documentElement.setAttribute('data-theme', savedTheme);
  renderItems();
</script>

</body>
</html>
"""

    # Gravar catálogo HTML exclusivamente no local configurado (resources/_lake_catalog.html)
    catalog_file.write_text(html_template, encoding="utf-8")
    print(f"📖 Catálogo HTML atualizado com sucesso em: {catalog_file}")



def generate_catalog_jsonl(lake_dir: Optional[Path] = None, jsonl_file: Optional[Path] = None) -> Path:
    """Gera o índice estruturado documents.jsonl para auditoria fina e controle no Git."""
    target_lake = lake_dir or LAKE_DIR
    target_jsonl = jsonl_file or CATALOG_JSONL
    target_jsonl.parent.mkdir(parents=True, exist_ok=True)

    documents = []
    if target_lake.exists():
        for file in sorted(target_lake.iterdir()):
            if file.is_file() and not file.name.startswith("."):
                h = hashlib.sha256()
                with open(file, "rb") as f:
                    while chunk := f.read(65536):
                        h.update(chunk)

                digest = h.hexdigest()
                doc_record = {
                    "id": f"sha256:{digest[:16]}",
                    "filename": file.name,
                    "media_type": file.suffix.lower().lstrip("."),
                    "size_bytes": file.stat().st_size,
                    "sha256": digest,
                    "updated_at": datetime.fromtimestamp(file.stat().st_mtime).isoformat(),
                }
                documents.append(doc_record)

    with open(target_jsonl, "w", encoding="utf-8") as f:
        for doc in documents:
            f.write(json.dumps(doc, ensure_ascii=False) + "\n")

    return target_jsonl


class ReindexResult(dict):
    """Resultado de reindexação do catálogo compatível tanto como dict de metadados quanto como lista de itens."""
    def __len__(self) -> int:
        return self.get("total_items", 0)

    @property
    def items(self) -> List[Dict[str, Any]]:
        return self.get("items", [])

    def __iter__(self):
        return iter(self.get("items", []))

    def __getitem__(self, key: Any) -> Any:
        if isinstance(key, int):
            return self.get("items", [])[key]
        return super().__getitem__(key)


def reindex_catalog(
    lake_dir: Optional[Path] = None,
    catalog_file: Optional[Path] = None,
    jsonl_file: Optional[Path] = None,
) -> ReindexResult:
    """
    Operação atômica e unificada de reindexação do Lake.
    Atualiza tanto o catálogo HTML interativo quanto o índice estruturado JSONL.
    """
    target_lake = lake_dir or LAKE_DIR
    target_html = catalog_file or CATALOG_HTML
    target_jsonl = jsonl_file or CATALOG_JSONL

    items = scan_lake_items(target_lake)
    generate_catalog_html(items, target_html)
    generate_catalog_jsonl(target_lake, target_jsonl)

    return ReindexResult({
        "total_items": len(items),
        "html_path": target_html,
        "jsonl_path": target_jsonl,
        "items": items,
    })
