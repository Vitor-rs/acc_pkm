# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "youtube-transcript-api>=0.6.2",
#     "httpx>=0.27.0",
#     "yt-dlp>=2024.0.0",
#     "pyyaml>=6.0.1",
# ]
# ///
"""
=============================================================================
Academic PKM - Generic YouTube Lake Transcriber & Cataloger
=============================================================================
Automação avançada e genérica para extração de transcrições do YouTube,
armazenamento estruturado no Data Lake (_lake) e catalogação interativa
em _lake_catalog.html.

Suporta:
- Vídeos individuais, múltiplos links, playlists completas ou arquivos de URLs
- Fallbacks inteligentes de idioma (pt, pt-BR, en, es) e tradução opcional
- Formatação inteligente com timestamps agrupados em parágrafos legíveis
- Frontmatter YAML completo (metadados, tags, estatísticas de leitura)
- Catálogo HTML moderno, interativo, responsivo e 100% offline (zero CDN obrigatório)
- Suporte unificado no catálogo para transcrições e documentos existentes (PDF/EPUB)

Exemplos de Uso:
    uv run scripts/yt_transcribe_and_catalog.py "https://www.youtube.com/watch?v=CzDTaLqozlQ"
    uv run scripts/yt_transcribe_and_catalog.py -f urls.txt --tags "pkm,metodologia"
    uv run scripts/yt_transcribe_and_catalog.py --playlist "https://www.youtube.com/playlist?list=..."
    uv run scripts/yt_transcribe_and_catalog.py --reindex
=============================================================================
"""

import sys
import os
import re
import json
import html
import unicodedata
import argparse
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

import httpx
import yaml
from youtube_transcript_api import YouTubeTranscriptApi
import yt_dlp

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


def resolve_paths(custom_lake: Optional[str] = None, custom_catalog: Optional[str] = None) -> tuple[Path, Path, Path]:
    """
    Resolve dinamicamente os diretórios do projeto (Root, Lake e Catálogo HTML).
    Compatível com chamadas a partir de qualquer pasta.
    """
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent

    # Detectar pasta _lake
    if custom_lake:
        lake_dir = Path(custom_lake).resolve()
    else:
        # Priorizar resources/_lake se existir
        res_lake = project_root / "resources" / "_lake"
        root_lake = project_root / "_lake"
        if res_lake.exists():
            lake_dir = res_lake
        elif root_lake.exists():
            lake_dir = root_lake
        else:
            # Padrão do projeto acc_pkm
            lake_dir = res_lake

    lake_dir.mkdir(parents=True, exist_ok=True)

    # Detectar arquivo de catálogo
    if custom_catalog:
        catalog_path = Path(custom_catalog).resolve()
    else:
        if (project_root / "resources").exists():
            catalog_path = project_root / "resources" / "_lake_catalog.html"
        else:
            catalog_path = project_root / "_lake_catalog.html"

    return project_root, lake_dir, catalog_path


def extract_video_ids(raw_inputs: List[str]) -> List[str]:
    """
    Extrai IDs válidos de 11 caracteres a partir de URLs, IDs avulsos ou playlists.
    """
    video_ids = []
    seen = set()

    for item in raw_inputs:
        item = item.strip()
        if not item or item.startswith("#"):
            continue

        # Playlist detection
        if "playlist?list=" in item or "&list=" in item:
            print(f"📋 Detectada playlist: {item}. Extraindo lista de vídeos...")
            try:
                ydl_opts = {
                    "extract_flat": True,
                    "quiet": True,
                    "no_warnings": True,
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    res = ydl.extract_info(item, download=False)
                    if res and "entries" in res:
                        for entry in res["entries"]:
                            if entry and "id" in entry:
                                vid = entry["id"]
                                if vid not in seen:
                                    seen.add(vid)
                                    video_ids.append(vid)
                        print(f"   -> {len(res.get('entries', []))} vídeos encontrados na playlist.")
                        continue
            except Exception as e:
                print(f"⚠️ Erro ao extrair playlist {item}: {e}. Tentando como vídeo único...")

        # ID direto
        if re.match(r"^[a-zA-Z0-9_-]{11}$", item):
            if item not in seen:
                seen.add(item)
                video_ids.append(item)
            continue

        # Regex para diversos formatos do YouTube
        patterns = [
            r"(?:v=|\/v\/|embed\/|shorts\/|live\/)([a-zA-Z0-9_-]{11})",
            r"youtu\.be\/([a-zA-Z0-9_-]{11})",
            r"(?:watch\?v=)([a-zA-Z0-9_-]{11})",
        ]
        matched = False
        for p in patterns:
            m = re.search(p, item)
            if m:
                vid = m.group(1)
                if vid not in seen:
                    seen.add(vid)
                    video_ids.append(vid)
                matched = True
                break

        if not matched:
            clean = re.sub(r"[?&].*$", "", item)
            parts = clean.split("/")
            if parts and len(parts[-1]) == 11:
                vid = parts[-1]
                if vid not in seen:
                    seen.add(vid)
                    video_ids.append(vid)

    return video_ids


def normalize_filename(title: str, video_id: str) -> str:
    """Normaliza o título para nome de arquivo seguro e limpo."""
    nfkd = unicodedata.normalize("NFKD", title)
    ascii_str = nfkd.encode("ASCII", "ignore").decode("ASCII")
    clean = ascii_str.lower()
    clean = re.sub(r"[^a-z0-9]+", "_", clean)
    clean = clean.strip("_")
    slug = clean[:90] if clean else "youtube_video"
    return f"{slug}_{video_id}.md"


def format_timestamp(seconds: float) -> str:
    """Formata segundos em [MM:SS] ou [HH:MM:SS]."""
    s = int(seconds)
    hours = s // 3600
    minutes = (s % 3600) // 60
    secs = s % 60
    if hours > 0:
        return f"[{hours:02d}:{minutes:02d}:{secs:02d}]"
    return f"[{minutes:02d}:{secs:02d}]"


def fetch_oembed_metadata(video_id: str) -> dict:
    """Coleta metadados essenciais rápidos via oEmbed do Google (sem quota/chaves)."""
    url = f"https://www.youtube.com/watch?v={video_id}"
    try:
        r = httpx.get("https://www.youtube.com/oembed", params={"url": url, "format": "json"}, timeout=10.0)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return {}


def fetch_ytdlp_metadata(video_id: str) -> dict:
    """Enriquece metadados (duração, upload_date, views, descrição) via yt-dlp."""
    url = f"https://www.youtube.com/watch?v={video_id}"
    try:
        ydl_opts = {
            "skip_download": True,
            "quiet": True,
            "no_warnings": True,
            "extract_flat": "in_playlist",
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if info:
                upload_raw = info.get("upload_date") or ""
                if len(upload_raw) == 8:
                    upload_date = f"{upload_raw[:4]}-{upload_raw[4:6]}-{upload_raw[6:]}"
                else:
                    upload_date = upload_raw or ""

                duration_sec = info.get("duration") or 0
                return {
                    "title": info.get("title"),
                    "channel": info.get("uploader") or info.get("channel"),
                    "channel_url": info.get("uploader_url") or info.get("channel_url") or "",
                    "publish_date": upload_date,
                    "views": info.get("view_count") or 0,
                    "duration_seconds": duration_sec,
                    "duration_formatted": format_timestamp(duration_sec).strip("[]"),
                    "description": info.get("description") or "",
                    "tags": info.get("tags") or [],
                }
    except Exception as e:
        # Fallback silencioso se falhar
        pass
    return {}


def fetch_transcript_smart(video_id: str, preferred_langs: List[str], translate_to: Optional[str] = None) -> tuple[Optional[List[dict]], str, bool]:
    """
    Busca transcrição com cascata inteligente de idiomas e tradução automática se solicitada.
    Retorna: (snippets_list, language_code, is_generated)
    """
    ytt = YouTubeTranscriptApi()

    # 1. Se tradução for explicitamente exigida
    if translate_to:
        try:
            transcript_list = ytt.list(video_id)
            for t in transcript_list:
                if t.is_translatable:
                    translated = t.translate(translate_to).fetch()
                    snippets = [{"start": s.start, "duration": s.duration, "text": s.text} for s in translated.snippets]
                    return snippets, translate_to, t.is_generated
        except Exception:
            pass

    # 2. Tentar busca direta nos idiomas preferenciais
    try:
        t = ytt.fetch(video_id, languages=preferred_langs)
        if t and t.snippets:
            snippets = [{"start": s.start, "duration": s.duration, "text": s.text} for s in t.snippets]
            # Determinar se era gerado ou o código exato
            lang_code = preferred_langs[0]
            return snippets, lang_code, False
    except Exception:
        pass

    # 3. Listar legendas disponíveis e selecionar a mais adequada
    try:
        t_list = ytt.list(video_id)
        # Priorizar legendas manuais em qualquer idioma da lista
        for item in t_list:
            if not item.is_generated and item.language_code in preferred_langs:
                fetched = item.fetch()
                snippets = [{"start": s.start, "duration": s.duration, "text": s.text} for s in fetched.snippets]
                return snippets, item.language_code, False

        # Segundo: qualquer legenda manual
        for item in t_list:
            if not item.is_generated:
                fetched = item.fetch()
                snippets = [{"start": s.start, "duration": s.duration, "text": s.text} for s in fetched.snippets]
                return snippets, item.language_code, False

        # Terceiro: gerada nos idiomas preferenciais
        for item in t_list:
            if item.language_code in preferred_langs:
                fetched = item.fetch()
                snippets = [{"start": s.start, "duration": s.duration, "text": s.text} for s in fetched.snippets]
                return snippets, item.language_code, True

        # Quarto: qualquer gerada disponível
        for item in t_list:
            fetched = item.fetch()
            snippets = [{"start": s.start, "duration": s.duration, "text": s.text} for s in fetched.snippets]
            return snippets, item.language_code, True
    except Exception:
        pass

    # 4. Fallback com yt-dlp para extrair legendas automáticas se youtube-transcript-api falhar
    try:
        url = f"https://www.youtube.com/watch?v={video_id}"
        ydl_opts = {
            "skip_download": True,
            "quiet": True,
            "writesubtitles": True,
            "writeautomaticsub": True,
            "subtitleslangs": preferred_langs + ["en"],
            "no_warnings": True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            subs = info.get("subtitles") or info.get("automatic_captions") or {}
            for l in preferred_langs + list(subs.keys()):
                if l in subs and subs[l]:
                    # Obter a url do formato json3 ou vtt
                    formats = subs[l]
                    json3 = next((f["url"] for f in formats if f.get("ext") == "json3"), None)
                    if json3:
                        resp = httpx.get(json3, timeout=10.0)
                        if resp.status_code == 200:
                            data = resp.json()
                            events = data.get("events", [])
                            snippets = []
                            for ev in events:
                                segs = ev.get("segs", [])
                                txt = "".join(s.get("utf8", "") for s in segs).strip()
                                if txt and "\n" not in txt:
                                    start = ev.get("tStartMs", 0) / 1000.0
                                    snippets.append({"start": start, "duration": ev.get("dDurationMs", 0)/1000.0, "text": txt})
                            if snippets:
                                return snippets, l, True
    except Exception:
        pass

    return None, "desconhecido", False


def format_transcript_paragraphs(snippets: List[dict], max_interval: float = 35.0, min_interval: float = 20.0, with_timestamps: bool = True) -> str:
    """
    Agrupa snippets em parágrafos coesos e bem formatados com pontuação e timestamps.
    """
    if not snippets:
        return ""

    paragraphs = []
    current_texts = []
    block_start = snippets[0]["start"]

    for s in snippets:
        txt = s["text"].strip()
        if not txt:
            continue

        current_texts.append(txt)
        elapsed = s["start"] - block_start

        # Condição de quebra: tempo corrido ou término em pontuação forte
        if elapsed >= max_interval or (elapsed >= min_interval and txt.endswith((".", "!", "?"))):
            joined = " ".join(current_texts)
            if with_timestamps:
                ts = format_timestamp(block_start)
                paragraphs.append(f"{ts} {joined}")
            else:
                paragraphs.append(joined)
            current_texts = []
            block_start = s["start"] + s.get("duration", 2)

    if current_texts:
        joined = " ".join(current_texts)
        if with_timestamps:
            ts = format_timestamp(block_start)
            paragraphs.append(f"{ts} {joined}")
        else:
            paragraphs.append(joined)

    return "\n\n".join(paragraphs)


def generate_summary(title: str, description: str, formatted_transcript: str) -> str:
    """Gera resumo executivo a partir da descrição ou parágrafos iniciais."""
    if description and len(description.strip()) > 40:
        lines = [l.strip() for l in description.strip().split("\n") if l.strip() and not l.startswith("http")]
        if lines:
            first_block = " ".join(lines[:2])
            if len(first_block) > 220:
                first_block = first_block[:217] + "..."
            return first_block

    # Fallback para o primeiro minuto da transcrição
    lines = [re.sub(r"^\[\d+:\d+(?::\d+)?\]\s*", "", l) for l in formatted_transcript.split("\n\n") if l.strip()]
    if lines:
        sample = " ".join(lines[:2])
        if len(sample) > 200:
            sample = sample[:197] + "..."
        return sample

    return f"Transcrição completa e análise do vídeo '{title}'."


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


def process_single_video(
    video_id: str,
    lake_dir: Path,
    preferred_langs: List[str],
    translate_to: Optional[str] = None,
    with_timestamps: bool = True,
    custom_tags: Optional[List[str]] = None,
) -> bool:
    """Processa a extração, formatação e salvamento de um único vídeo no Lake."""
    full_url = f"https://www.youtube.com/watch?v={video_id}"
    print(f"\n=======================================================")
    print(f"🔍 Processando vídeo ID: {video_id} ({full_url})")

    # 1. Metadados
    print("📥 Coletando metadados (oEmbed & yt-dlp)...")
    oembed = fetch_oembed_metadata(video_id)
    ytdlp = fetch_ytdlp_metadata(video_id)

    title = ytdlp.get("title") or oembed.get("title") or f"YouTube Video {video_id}"
    channel = ytdlp.get("channel") or oembed.get("author_name") or "Canal Desconhecido"
    channel_url = ytdlp.get("channel_url") or oembed.get("author_url") or ""
    publish_date = ytdlp.get("publish_date") or ""
    views = ytdlp.get("views") or ""
    desc = ytdlp.get("description") or ""
    duration_sec = ytdlp.get("duration_seconds") or 0
    duration_fmt = ytdlp.get("duration_formatted") or ""

    # 2. Transcrição
    print(f"🎙️ Extraindo transcrição (idiomas preferenciais: {preferred_langs})...")
    snippets, lang_code, is_generated = fetch_transcript_smart(video_id, preferred_langs, translate_to)

    if not snippets:
        print(f"❌ [ERRO] Não foi possível extrair legendas para o vídeo {video_id}.")
        print("   Verifique se o vídeo possui legendas ativas ou se há restrições de idade/região.")
        return False

    # Duração calculada a partir dos snippets caso yt-dlp não tenha fornecido
    if duration_sec == 0 and snippets:
        last_s = snippets[-1]
        duration_sec = int(last_s["start"] + last_s.get("duration", 2))
        duration_fmt = format_timestamp(duration_sec).strip("[]")

    formatted_transcript = format_transcript_paragraphs(snippets, with_timestamps=with_timestamps)
    summary = generate_summary(title, desc, formatted_transcript)
    word_count = len(formatted_transcript.split())
    reading_time_min = max(1, round(word_count / 180))

    # Tags
    tags = ["youtube", "transcricao", "pkm"]
    if custom_tags:
        for t in custom_tags:
            if t not in tags:
                tags.append(t)
    if ytdlp.get("tags"):
        for t in ytdlp["tags"][:5]:
            t_clean = re.sub(r"[^a-zA-Z0-9_-]", "", t.lower())
            if t_clean and t_clean not in tags:
                tags.append(t_clean)

    # 3. Preparar arquivo Markdown com Frontmatter
    filename = normalize_filename(title, video_id)
    file_path = lake_dir / filename
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    frontmatter = {
        "id": video_id,
        "type": "youtube_transcript",
        "title": title,
        "channel": channel,
        "channel_url": channel_url,
        "publish_date": publish_date,
        "views": views,
        "duration_seconds": duration_sec,
        "duration_formatted": duration_fmt,
        "url": full_url,
        "thumbnail_url": f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg",
        "transcription_date": now_str,
        "language": lang_code,
        "is_generated": is_generated,
        "word_count": word_count,
        "reading_time_minutes": reading_time_min,
        "summary": summary,
        "tags": tags,
    }

    yaml_header = yaml.dump(frontmatter, allow_unicode=True, sort_keys=False)

    md_content = f"""---
{yaml_header.strip()}
---

# {title}

> **📺 Canal:** [{channel}]({channel_url})  
> **📅 Publicado em:** {publish_date or 'Não informado'} | **⏱️ Duração:** {duration_fmt} | **👁️ Visualizações:** {views}  
> **🔗 Link Original:** [{full_url}]({full_url})  
> **🌐 Idioma:** {lang_code} {'(Gerado Automaticamente)' if is_generated else '(Manual)'} | **📝 Volume:** {word_count:,} palavras (~{reading_time_min} min de leitura)

---

## 📌 Assunto Resumido
{summary}

---

## 🎙️ Transcrição Completa
{formatted_transcript}
"""

    file_path.write_text(md_content, encoding="utf-8")
    print(f"✅ Transcrição salva com sucesso em: {file_path}")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Pipeline Genérico de Transcrição do YouTube e Catalogação no Data Lake (_lake)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  uv run scripts/yt_transcribe_and_catalog.py "https://www.youtube.com/watch?v=CzDTaLqozlQ"
  uv run scripts/yt_transcribe_and_catalog.py URL1 URL2 URL3 --tags "pesquisa,qualitativa"
  uv run scripts/yt_transcribe_and_catalog.py -f links.txt
  uv run scripts/yt_transcribe_and_catalog.py --playlist "https://www.youtube.com/playlist?list=..."
  uv run scripts/yt_transcribe_and_catalog.py --reindex
        """
    )

    parser.add_argument("urls", nargs="*", help="Um ou mais links ou IDs de vídeos do YouTube")
    parser.add_argument("-f", "--file", help="Arquivo contendo lista de URLs (um por linha)")
    parser.add_argument("-p", "--playlist", help="Link de Playlist do YouTube para transcrever todos os vídeos")
    parser.add_argument("--langs", default="pt,pt-BR,en,es", help="Idiomas preferenciais separados por vírgula (default: pt,pt-BR,en,es)")
    parser.add_argument("--translate-to", help="Traduzir transcrição para o código especificado (ex: pt)")
    parser.add_argument("--tags", help="Tags adicionais separadas por vírgula para catalogação")
    parser.add_argument("--no-timestamps", action="store_true", help="Omitir timestamps na transcrição")
    parser.add_argument("--lake-dir", help="Caminho personalizado para o diretório _lake")
    parser.add_argument("--catalog-file", help="Caminho personalizado para o arquivo _lake_catalog.html")
    parser.add_argument("--reindex", action="store_true", help="Apenas re-escanear o Lake e atualizar o _lake_catalog.html sem baixar novas transcrições")

    args = parser.parse_args()

    project_root, lake_dir, catalog_path = resolve_paths(args.lake_dir, args.catalog_file)
    print(f"📂 Diretório do Lake: {lake_dir}")
    print(f"📑 Arquivo de Catálogo: {catalog_path}")

    # Detectar modo somente re-indexação
    is_reindex = args.reindex or any(u.lower() in ("reindex", "--reindex", "re-index") for u in args.urls)
    if is_reindex and not any(u.lower() not in ("reindex", "--reindex", "re-index") for u in args.urls) and not args.file and not args.playlist:
        print("\n🔄 Re-escaneando diretório _lake e atualizando catálogo...", flush=True)
        items = scan_lake_items(lake_dir)
        generate_catalog_html(items, catalog_path)
        print(f"✨ Concluído! {len(items)} itens catalogados.", flush=True)
        return

    # Coletar entradas (filtrando palavra-chave reindex se houver)
    raw_inputs = [u for u in args.urls if u.lower() not in ("reindex", "--reindex", "re-index")]

    if args.playlist:
        raw_inputs.append(args.playlist)

    if args.file:
        file_path = Path(args.file)
        if file_path.exists():
            print(f"📄 Carregando links do arquivo: {file_path}", flush=True)
            lines = file_path.read_text(encoding="utf-8").splitlines()
            raw_inputs.extend(lines)
        else:
            print(f"❌ Arquivo não encontrado: {file_path}", flush=True)

    if not raw_inputs:
        # Se nenhuma URL foi fornecida, reindexar catálogo
        print("⚠️ Nenhuma URL fornecida. Reindexando catálogo existente...", flush=True)
        items = scan_lake_items(lake_dir)
        generate_catalog_html(items, catalog_path)
        print(f"✨ Concluído! {len(items)} itens catalogados.", flush=True)
        return

    # Extrair IDs
    video_ids = extract_video_ids(raw_inputs)
    if not video_ids:
        print("❌ Nenhum ID de vídeo válido encontrado nas entradas fornecidas.", flush=True)
        sys.exit(1)

    print(f"🎯 Total de vídeos para processar: {len(video_ids)}", flush=True)

    preferred_langs = [l.strip() for l in args.langs.split(",") if l.strip()]
    custom_tags = [t.strip() for t in args.tags.split(",") if t.strip()] if args.tags else []

    success_files = []
    for idx, vid in enumerate(video_ids, start=1):
        print(f"\n[{idx}/{len(video_ids)}] Iniciando processamento de {vid}...", flush=True)
        ok = process_single_video(
            video_id=vid,
            lake_dir=lake_dir,
            preferred_langs=preferred_langs,
            translate_to=args.translate_to,
            with_timestamps=not args.no_timestamps,
            custom_tags=custom_tags,
        )
        if ok:
            success_files.append(vid)

    # Atualizar automaticamente o Catálogo HTML
    print("\n📊 Atualizando o catálogo central _lake_catalog.html...", flush=True)
    lake_items = scan_lake_items(lake_dir)
    generate_catalog_html(lake_items, catalog_path)

    print(f"\n🎉 Processamento concluído com sucesso!", flush=True)
    print(f"   -> {len(success_files)}/{len(video_ids)} vídeos transcritos e salvos em: {lake_dir}", flush=True)
    print(f"   -> Catálogo interativo disponível em: {catalog_path}", flush=True)


if __name__ == "__main__":
    main()
