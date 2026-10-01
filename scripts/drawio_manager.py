"""
=============================================================================
ACADEMIC PKM - DIAGRAMS.NET / DRAW.IO MANAGER & AUTOMATION ENGINE
=============================================================================
Gerencia a integração de diagramação visual científica do Academic PKM:
- Automação via Draw.io Desktop CLI (exportação SVG/PDF com XML embutido)
- Servidor MCP (@drawio/mcp) e busca de formas em bibliotecas acadêmicas/técnicas
- Geração determinística de URLs web RFC 1951 (app.diagrams.net/#create=...)
- Gestão de templates acadêmicos (PRISMA 2020, Triangulação Metodológica, Frameworks)
- Ponte com extensão VS Code (hediet.vscode-drawio) e inclusão em LaTeX/Markdown
=============================================================================
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import shutil
import subprocess
import sys
import tempfile
import urllib.parse
import zlib
from pathlib import Path
from typing import Any, Dict, List, Optional

# Adiciona scripts ao sys.path para import de core
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from core.config import (
    DIAGRAMS_DIR,
    REPO_ROOT,
    TEMPLATES_DIR,
    find_executable,
)

DRAWIO_TEMPLATES_DIR = TEMPLATES_DIR / "drawio"


def get_drawio_cli() -> Optional[str]:
    """Localiza o binário do Draw.io Desktop (draw.io.exe)."""
    return find_executable("draw.io") or find_executable("drawio")


def check_drawio_environment() -> Dict[str, Any]:
    """Audita a prontidão do ecossistema Draw.io no ambiente."""
    cli_path = get_drawio_cli()
    cli_version = None
    if cli_path and Path(cli_path).exists():
        try:
            # Em Windows, tenta obter FileVersion via PowerShell se disponível
            cmd = f'(Get-Item "{cli_path}").VersionInfo.ProductVersion'
            res = subprocess.run(["powershell", "-NoProfile", "-Command", cmd], capture_output=True, text=True, timeout=5)
            if res.returncode == 0 and res.stdout.strip():
                cli_version = res.stdout.strip()
        except Exception:
            cli_version = "Detectado (versão não obtida)"

    npx_path = shutil.which("npx")

    # Verifica extensão VS Code
    vscode_ext_installed = False
    try:
        res = subprocess.run(
            ["code", "--list-extensions"],
            capture_output=True,
            text=True,
            timeout=6,
            shell=(sys.platform == "win32"),
        )
        if "hediet.vscode-drawio" in res.stdout:
            vscode_ext_installed = True
    except Exception:
        vscode_ext_installed = False

    # Verifica MCP config global
    mcp_config_path = Path(os.environ.get("USERPROFILE", "")) / ".gemini" / "config" / "mcp_config.json"
    mcp_registered = False
    if mcp_config_path.exists():
        try:
            data = json.loads(mcp_config_path.read_text(encoding="utf-8"))
            mcp_registered = "drawio" in data.get("mcpServers", {})
        except Exception:
            mcp_registered = False

    # Templates disponíveis
    templates = []
    if DRAWIO_TEMPLATES_DIR.exists():
        templates = [f.stem for f in DRAWIO_TEMPLATES_DIR.glob("*.drawio")]

    return {
        "cli_path": cli_path,
        "cli_version": cli_version,
        "npx_path": npx_path,
        "vscode_extension": vscode_ext_installed,
        "mcp_registered": mcp_registered,
        "templates": templates,
        "diagrams_dir": str(DIAGRAMS_DIR),
    }


def generate_browser_url(drawio_input: str | Path, lightbox: bool = False, dark: str = "auto") -> str:
    """
    Gera URL oficial do Diagrams.net com payload comprimido via RFC 1951 raw deflate.
    Permite abrir e editar o diagrama imediatamente em qualquer navegador sem instalação.
    """
    if isinstance(drawio_input, Path) or (isinstance(drawio_input, str) and os.path.isfile(drawio_input)):
        xml_content = Path(drawio_input).read_text(encoding="utf-8")
    else:
        xml_content = str(drawio_input)

    # Codifica para URI component
    encoded_xml = urllib.parse.quote(xml_content)

    # Comprime usando zlib deflateRaw (sem cabeçalhos zlib/gzip)
    compressor = zlib.compressobj(wbits=-15)
    compressed = compressor.compress(encoded_xml.encode("utf-8")) + compressor.flush()

    # Base64
    b64_data = base64.b64encode(compressed).decode("utf-8")

    payload_dict = {
        "type": "xml",
        "compressed": True,
        "data": b64_data,
    }
    payload_str = urllib.parse.quote(json.dumps(payload_dict))

    base_url = "https://app.diagrams.net/?grid=0&pv=0&border=10"
    if lightbox:
        base_url += "&lightbox=1"
    else:
        base_url += "&edit=_blank"

    if dark != "auto":
        base_url += f"&dark={1 if dark == 'true' else 0}"

    return f"{base_url}#create={payload_str}"


def open_in_browser(drawio_file: Path) -> str:
    """
    Abre o diagrama no navegador contornando a truncagem do fragmento #create no Windows.
    Gera um atalho temporário .url e invoca o navegador padrão.
    """
    url = generate_browser_url(drawio_file)

    if sys.platform == "win32":
        # No Windows, cmd.exe /c start trata & e # como delimitadores especiais.
        # Criar um arquivo .url temporário é a forma 100% robusta de abrir a URL completa.
        temp_dir = Path(tempfile.gettempdir())
        url_file = temp_dir / f"diagram_{drawio_file.stem}.url"
        url_file.write_text(f"[InternetShortcut]\r\nURL={url}\r\n", encoding="utf-8")
        try:
            os.startfile(str(url_file))
        except Exception:
            subprocess.run(["cmd.exe", "/c", "start", "", str(url_file)], shell=False)
    else:
        import webbrowser
        webbrowser.open(url)

    return url


def export_diagram(
    input_file: Path,
    output_file: Optional[Path] = None,
    fmt: str = "svg",
    border: int = 10,
    scale: float = 1.0,
    embed: bool = True,
    crop: bool = True,
    transparent: bool = True,
) -> Path:
    """
    Exporta um diagrama .drawio para SVG, PNG ou PDF via Draw.io Desktop CLI.
    Assegura que -e (--embed-diagram) esteja ativo, mantendo o arquivo exportado 100% editável.
    """
    cli_path = get_drawio_cli()
    if not cli_path:
        raise RuntimeError("Draw.io Desktop CLI (draw.io.exe) não foi encontrado no sistema.")

    input_file = input_file.resolve()
    if not input_file.exists():
        raise FileNotFoundError(f"Arquivo de diagrama não encontrado: {input_file}")

    if output_file is None:
        if fmt == "svg":
            output_file = input_file.parent / f"{input_file.stem}.drawio.svg"
        elif fmt == "png":
            output_file = input_file.parent / f"{input_file.stem}.drawio.png"
        elif fmt == "pdf":
            output_file = input_file.parent / f"{input_file.stem}.drawio.pdf"
        else:
            output_file = input_file.parent / f"{input_file.stem}.{fmt}"
    else:
        output_file = output_file.resolve()

    output_file.parent.mkdir(parents=True, exist_ok=True)

    args = [
        cli_path,
        "-x",
        "-f", fmt,
        "-b", str(border),
        "-s", str(scale),
        "-o", str(output_file),
    ]

    if embed and fmt in ("png", "svg", "pdf"):
        args.append("-e")

    if crop and fmt == "pdf":
        args.append("--crop")

    if transparent and fmt == "png":
        args.append("-t")

    args.append(str(input_file))

    res = subprocess.run(args, capture_output=True, text=True, timeout=30)
    if res.returncode != 0 or not output_file.exists():
        err = res.stderr.strip() or res.stdout.strip()
        raise RuntimeError(f"Falha na exportação via Draw.io CLI: {err}")

    return output_file


def search_shapes_mcp(query: str, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Consulta o servidor MCP local (@drawio/mcp) para buscar formas e estilos compatíveis.
    """
    npx = shutil.which("npx")
    if not npx:
        return []

    p = subprocess.Popen(
        [npx, "-y", "@drawio/mcp"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        shell=(sys.platform == "win32"),
    )

    try:
        def send(msg: dict):
            p.stdin.write(json.dumps(msg) + "\n")
            p.stdin.flush()

        send({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "acc_pkm_client", "version": "1.0"},
            },
        })
        p.stdout.readline()
        send({"jsonrpc": "2.0", "method": "notifications/initialized"})

        send({
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "search_shapes",
                "arguments": {"query": query},
            },
        })

        line = p.stdout.readline()
        resp = json.loads(line)
        content_items = resp.get("result", {}).get("content", [])
        if content_items and content_items[0].get("type") == "text":
            data = json.loads(content_items[0].get("text", "[]"))
            return data[:limit]
        return []
    except Exception:
        return []
    finally:
        p.kill()


def instantiate_template(template_name: str, target_path: Optional[Path] = None) -> Path:
    """Copia um template oficial de diagrama acadêmico para o destino."""
    tmpl_file = DRAWIO_TEMPLATES_DIR / f"{template_name}.drawio"
    if not tmpl_file.exists():
        # Tenta sem extensão
        matches = list(DRAWIO_TEMPLATES_DIR.glob(f"{template_name}*.drawio"))
        if matches:
            tmpl_file = matches[0]
        else:
            available = [f.stem for f in DRAWIO_TEMPLATES_DIR.glob("*.drawio")]
            raise FileNotFoundError(f"Template '{template_name}' não encontrado. Disponíveis: {available}")

    if target_path is None:
        DIAGRAMS_DIR.mkdir(parents=True, exist_ok=True)
        target_path = DIAGRAMS_DIR / f"{tmpl_file.name}"

    target_path = target_path.resolve()
    target_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(tmpl_file, target_path)
    return target_path


def main():
    parser = argparse.ArgumentParser(
        prog="drawio_manager",
        description="Academic PKM - Diagrams.net / Draw.io Manager",
    )
    subparsers = parser.add_subparsers(dest="subcommand", help="Subcomando a executar")

    # status
    subparsers.add_parser("status", help="Audita ecossistema do Draw.io, MCP e extensões")

    # export
    p_export = subparsers.add_parser("export", help="Exporta diagrama .drawio para SVG, PNG ou PDF")
    p_export.add_argument("input", help="Caminho do arquivo .drawio")
    p_export.add_argument("-o", "--output", help="Caminho de saída (opcional)")
    p_export.add_argument("-f", "--format", choices=["svg", "png", "pdf"], default="svg", help="Formato de exportação")
    p_export.add_argument("--scale", type=float, default=1.0, help="Fator de escala")
    p_export.add_argument("--no-embed", action="store_true", help="Não embutir XML de edição")

    # url
    p_url = subparsers.add_parser("url", help="Gera link web app.diagrams.net para visualização/edição")
    p_url.add_argument("input", help="Caminho do arquivo .drawio")
    p_url.add_argument("--open", action="store_true", help="Abrir automaticamente no navegador")

    # template
    p_tmpl = subparsers.add_parser("template", help="Instancia um template acadêmico")
    p_tmpl.add_argument("name", help="Nome do template (ex: prisma_2020, framework)")
    p_tmpl.add_argument("-o", "--output", help="Arquivo destino")

    # search
    p_srch = subparsers.add_parser("search", help="Busca formas via servidor MCP @drawio/mcp")
    p_srch.add_argument("query", help="Termo de busca (ex: database, cloud, arrow)")
    p_srch.add_argument("-n", "--limit", type=int, default=8, help="Limite de resultados")

    args = parser.parse_args()

    if args.subcommand == "status":
        env = check_drawio_environment()
        print("\n=== DIAGRAMS.NET / DRAW.IO ENVIRONMENT AUDIT ===")
        print(f"CLI Executable:   {env['cli_path'] or 'NÃO ENCONTRADO'}")
        if env["cli_version"]:
            print(f"Versão CLI:       {env['cli_version']}")
        print(f"Node / NPX:       {env['npx_path'] or 'NÃO ENCONTRADO'}")
        print(f"VS Code Extensão: {'INSTALADA (hediet.vscode-drawio)' if env['vscode_extension'] else 'NÃO DETECTADA'}")
        print(f"MCP Config:       {'CONFIGURADO (@drawio/mcp)' if env['mcp_registered'] else 'NÃO REGISTRADO'}")
        print(f"Templates:        {', '.join(env['templates']) if env['templates'] else 'Nenhum'}")
        print(f"Diretório Base:   {env['diagrams_dir']}")
        print("================================================\n")

    elif args.subcommand == "export":
        in_path = Path(args.input)
        out_path = Path(args.output) if args.output else None
        res = export_diagram(in_path, out_path, fmt=args.format, scale=args.scale, embed=not args.no_embed)
        print(f"Diagrama exportado com sucesso: {res}")

    elif args.subcommand == "url":
        in_path = Path(args.input)
        if args.open:
            url = open_in_browser(in_path)
            print(f"Aberto no navegador: {url}")
        else:
            url = generate_browser_url(in_path)
            print(f"URL de edição web:\n{url}")

    elif args.subcommand == "template":
        out_path = Path(args.output) if args.output else None
        res = instantiate_template(args.name, out_path)
        print(f"Template '{args.name}' instanciado em: {res}")

    elif args.subcommand == "search":
        shapes = search_shapes_mcp(args.query, limit=args.limit)
        print(f"\nFormas encontradas para '{args.query}': {len(shapes)}")
        for idx, s in enumerate(shapes, 1):
            title = s.get("title") or s.get("name", "Forma")
            style = s.get("style", "")
            w = s.get("w", 80)
            h = s.get("h", 80)
            print(f"[{idx}] {title} ({w}x{h}): {style[:60]}...")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
