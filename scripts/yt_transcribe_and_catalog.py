
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


# =============================================================================
# CATALOG REINDEXING & LAKE SCANNER (DELEGADO AO CORE.CATALOG_SERVICE)
# =============================================================================
from core.catalog_service import scan_lake_items, generate_catalog_html, reindex_catalog


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
