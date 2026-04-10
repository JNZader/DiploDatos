#!/usr/bin/env python3
"""
py2report — Convierte un archivo .py comentado en un reporte HTML.

Uso:
    python py2report.py archivo.py [--output reporte.html] [--title "Mi Reporte"]

Como funciona:
    1. Lee el .py linea por linea
    2. Clasifica cada linea en uno de 3 tipos:
       - HEADER: lineas que empiezan con # === o # --- o # ### (se vuelven titulos)
       - COMMENT: lineas que empiezan con # (se vuelven texto explicativo)
       - CODE: todo lo demas (se muestra como bloque de codigo)
    3. Agrupa lineas consecutivas del mismo tipo en "bloques"
    4. Detecta plt.savefig("algo.png") en el codigo y embebe la imagen
    5. Genera un HTML standalone con CSS y syntax highlighting via Prism.js (CDN)

Convenciones para que tu .py se vea bien:
    # =============================================================
    # TITULO DE SECCION
    # =============================================================
    → Se convierte en <h2>

    # --- Subtitulo ---
    → Se convierte en <h3>

    # Texto normal de explicacion
    # que puede ocupar varias lineas
    → Se convierte en <p> dentro de una card

    # CONCEPTO: Algo importante
    → Se convierte en una caja amarilla destacada

    codigo_python = "normal"
    → Se muestra en bloque de codigo con syntax highlighting

    plt.savefig("grafico.png")
    → Embebe la imagen en el reporte (base64)
"""

import argparse
import base64
import re
import sys
from enum import Enum
from pathlib import Path


class BlockType(Enum):
    HEADER = "header"
    SUBHEADER = "subheader"
    COMMENT = "comment"
    CONCEPT = "concept"
    CODE = "code"
    IMAGE = "image"
    BLANK = "blank"


def classify_line(line: str) -> BlockType:
    """Clasifica una linea del .py en su tipo de bloque."""
    stripped = line.strip()

    if not stripped:
        return BlockType.BLANK

    # Lineas de separacion tipo # ============ o # ############
    if re.match(r"^#\s*[=]{10,}$", stripped) or re.match(r"^#\s*[#]{10,}$", stripped):
        return BlockType.BLANK  # las ignoramos, son decoracion

    # Subtitulos: # --- algo ---
    if re.match(r"^#\s*-{3,}\s*.+", stripped):
        return BlockType.SUBHEADER

    # Detectar savefig
    if "savefig(" in stripped and not stripped.startswith("#"):
        return BlockType.IMAGE

    # Comentarios
    if stripped.startswith("#"):
        text = stripped.lstrip("#").strip()

        # Headers: lineas en MAYUSCULAS que parecen titulos
        # (linea corta, mayoritariamente mayusculas o con formato de titulo)
        if re.match(r"^(PASO|OPCION|EJERCICIO|SECCION)\s+\d", text, re.IGNORECASE):
            return BlockType.HEADER
        if text.isupper() and len(text) > 5 and len(text) < 80:
            return BlockType.HEADER

        # Conceptos destacados
        if text.startswith("CONCEPTO:") or text.startswith("CUIDADO:"):
            return BlockType.CONCEPT

        return BlockType.COMMENT

    return BlockType.CODE


def parse_blocks(lines: list[str]) -> list[dict]:
    """Agrupa lineas consecutivas del mismo tipo en bloques."""
    blocks = []
    current_type = None
    current_lines = []

    for line in lines:
        line_type = classify_line(line)

        # Las imagenes siempre son bloque propio
        if line_type == BlockType.IMAGE:
            if current_lines and current_type != BlockType.BLANK:
                blocks.append({"type": current_type, "lines": current_lines})
            blocks.append({"type": BlockType.IMAGE, "lines": [line]})
            current_type = None
            current_lines = []
            continue

        # Los headers siempre son bloque propio
        if line_type in (BlockType.HEADER, BlockType.SUBHEADER):
            if current_lines and current_type != BlockType.BLANK:
                blocks.append({"type": current_type, "lines": current_lines})
            blocks.append({"type": line_type, "lines": [line]})
            current_type = None
            current_lines = []
            continue

        # Blanks: si tenemos algo acumulado, cerramos el bloque
        if line_type == BlockType.BLANK:
            if current_lines and current_type != BlockType.BLANK:
                blocks.append({"type": current_type, "lines": current_lines})
                current_type = None
                current_lines = []
            continue

        # CONCEPT siempre empieza bloque nuevo (aunque venga de COMMENT)
        if line_type == BlockType.CONCEPT and current_type != BlockType.CONCEPT:
            if current_lines:
                blocks.append({"type": current_type, "lines": current_lines})
            current_type = BlockType.CONCEPT
            current_lines = [line]
            continue

        # Si cambia de comment a code (o viceversa), nuevo bloque
        # Pero concept seguido de comment se agrupa como concept
        if current_type == BlockType.CONCEPT and line_type == BlockType.COMMENT:
            current_lines.append(line)
            continue

        if line_type != current_type:
            if current_lines:
                blocks.append({"type": current_type, "lines": current_lines})
            current_type = line_type
            current_lines = [line]
        else:
            current_lines.append(line)

    if current_lines and current_type != BlockType.BLANK:
        blocks.append({"type": current_type, "lines": current_lines})

    return blocks


def strip_comment(line: str) -> str:
    """Saca el # inicial y espacios de un comentario."""
    stripped = line.strip()
    if stripped.startswith("#"):
        return stripped.lstrip("#").strip()
    return stripped


def extract_savefig_path(line: str) -> str | None:
    """Extrae el path del plt.savefig("algo.png")."""
    match = re.search(r'savefig\(["\']([^"\']+)["\']', line)
    return match.group(1) if match else None


def img_to_base64(filepath: Path) -> str:
    """Convierte imagen a tag <img> con base64."""
    if not filepath.exists():
        return f'<p class="missing-img">Imagen no encontrada: {filepath.name}</p>'
    data = filepath.read_bytes()
    b64 = base64.b64encode(data).decode()
    return f'<img src="data:image/png;base64,{b64}">'


def block_to_html(block: dict, base_dir: Path) -> str:
    """Convierte un bloque parseado a HTML."""
    btype = block["type"]
    lines = block["lines"]

    if btype == BlockType.HEADER:
        text = strip_comment(lines[0])
        # Limpiar formato tipo "PASO 8: ALGO" -> "Paso 8: Algo"
        return f'<h2>{text}</h2>'

    if btype == BlockType.SUBHEADER:
        text = strip_comment(lines[0]).strip("-").strip()
        return f'<h3>{text}</h3>'

    if btype == BlockType.CONCEPT:
        paragraphs = []
        current = []
        for line in lines:
            text = strip_comment(line)
            if not text:
                if current:
                    paragraphs.append(" ".join(current))
                    current = []
            else:
                # Limpiar el "CONCEPTO:" o "CUIDADO:" del inicio
                if text.startswith("CONCEPTO:"):
                    text = text[len("CONCEPTO:"):].strip()
                if text.startswith("CUIDADO:"):
                    text = "<strong>CUIDADO:</strong> " + text[len("CUIDADO:"):].strip()
                current.append(text)
        if current:
            paragraphs.append(" ".join(current))

        inner = "".join(f"<p>{p}</p>" for p in paragraphs)
        return f'<div class="concept">{inner}</div>'

    if btype == BlockType.COMMENT:
        paragraphs = []
        current = []
        in_list = False
        list_items = []

        for line in lines:
            text = strip_comment(line)

            # Detectar items de lista (empiezan con -, *, numero.)
            is_list_item = bool(re.match(r"^[-*]\s+", text) or re.match(r"^\d+\.\s+", text))

            if is_list_item:
                if current and not in_list:
                    paragraphs.append(("p", " ".join(current)))
                    current = []
                in_list = True
                # Limpiar el marcador
                item_text = re.sub(r"^[-*]\s+", "", text)
                item_text = re.sub(r"^\d+\.\s+", "", item_text)
                list_items.append(item_text)
            else:
                if in_list:
                    paragraphs.append(("ul", list_items[:]))
                    list_items = []
                    in_list = False
                if not text:
                    if current:
                        paragraphs.append(("p", " ".join(current)))
                        current = []
                else:
                    current.append(text)

        if in_list:
            paragraphs.append(("ul", list_items))
        if current:
            paragraphs.append(("p", " ".join(current)))

        parts = []
        for tag, content in paragraphs:
            if tag == "ul":
                items = "".join(f"<li>{item}</li>" for item in content)
                parts.append(f"<ul>{items}</ul>")
            else:
                parts.append(f"<p>{content}</p>")

        return f'<div class="explanation">{"".join(parts)}</div>'

    if btype == BlockType.CODE:
        code_text = "\n".join(lines)
        # Escapar HTML
        code_text = (
            code_text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )
        return f'<pre><code class="language-python">{code_text}</code></pre>'

    if btype == BlockType.IMAGE:
        img_path = extract_savefig_path(lines[0])
        if img_path:
            full_path = base_dir / img_path
            return f'<div class="chart">{img_to_base64(full_path)}</div>'
        return ""

    return ""


def generate_report(py_path: str, output: str = None, title: str = None) -> str:
    """Pipeline completo: .py → HTML."""
    py_file = Path(py_path)
    if not py_file.exists():
        print(f"Error: {py_path} no existe", file=sys.stderr)
        sys.exit(1)

    base_dir = py_file.parent
    if not output:
        output = str(base_dir / f"{py_file.stem}_reporte.html")
    if not title:
        # Intentar extraer titulo del primer comentario
        title = py_file.stem.replace("_", " ").title()

    lines = py_file.read_text(encoding="utf-8").splitlines()

    # Intentar extraer titulo mejor del primer bloque de comentarios
    for line in lines[:10]:
        stripped = line.strip()
        if stripped.startswith("#") and not re.match(r"^#\s*[=#-]+$", stripped):
            candidate = strip_comment(line)
            if len(candidate) > 5 and not candidate.startswith("!"):
                title = candidate
                break

    blocks = parse_blocks(lines)
    body_html = "\n".join(block_to_html(b, base_dir) for b in blocks)

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}

  body {{
    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
    line-height: 1.7;
    color: #1a1a2e;
    background: #f0f2f5;
    padding: 2rem;
  }}

  .container {{
    max-width: 900px;
    margin: 0 auto;
  }}

  /* --- Titulos --- */
  h1 {{
    font-size: 1.8rem;
    color: #16213e;
    border-bottom: 3px solid #0f3460;
    padding-bottom: 0.5rem;
    margin-bottom: 1.5rem;
  }}
  h2 {{
    font-size: 1.4rem;
    color: #0f3460;
    margin-top: 2.5rem;
    margin-bottom: 0.8rem;
    padding: 0.5rem 1rem;
    background: #16213e;
    color: white;
    border-radius: 6px;
  }}
  h3 {{
    font-size: 1.15rem;
    color: #533483;
    margin-top: 1.5rem;
    margin-bottom: 0.5rem;
    padding-left: 0.5rem;
    border-left: 3px solid #533483;
  }}

  /* --- Texto explicativo (comentarios normales) --- */
  .explanation {{
    background: white;
    border-radius: 8px;
    padding: 1rem 1.5rem;
    margin: 0.8rem 0;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
  }}
  .explanation p {{ margin-bottom: 0.4rem; }}
  .explanation ul {{
    padding-left: 1.5rem;
    margin: 0.4rem 0;
  }}
  .explanation li {{ margin-bottom: 0.2rem; }}

  /* --- Conceptos destacados --- */
  .concept {{
    background: #fff8e1;
    border-left: 4px solid #ff8f00;
    padding: 1rem 1.5rem;
    border-radius: 0 8px 8px 0;
    margin: 0.8rem 0;
  }}
  .concept strong {{ color: #e65100; }}
  .concept p {{ margin-bottom: 0.4rem; }}

  /* --- Bloques de codigo --- */
  pre {{
    margin: 0.8rem 0;
    border-radius: 8px;
    overflow-x: auto;
  }}
  pre code {{
    font-size: 0.85rem;
    line-height: 1.5;
  }}

  /* --- Graficos --- */
  .chart {{
    text-align: center;
    margin: 1rem 0;
  }}
  .chart img {{
    max-width: 100%;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.12);
  }}

  .missing-img {{
    color: #c62828;
    background: #ffebee;
    padding: 0.5rem 1rem;
    border-radius: 6px;
  }}

  /* --- Footer --- */
  footer {{
    margin-top: 3rem;
    padding-top: 1rem;
    border-top: 1px solid #dee2e6;
    color: #666;
    font-size: 0.85rem;
  }}

  /* --- Responsive --- */
  @media (max-width: 768px) {{
    body {{ padding: 1rem; }}
    h2 {{ font-size: 1.2rem; }}
  }}

  /* --- Print --- */
  @media print {{
    body {{ background: white; padding: 0; }}
    .container {{ max-width: 100%; }}
    pre {{ page-break-inside: avoid; }}
    .chart {{ page-break-inside: avoid; }}
    h2 {{ page-break-after: avoid; }}
  }}
</style>
</head>
<body>
<div class="container">
<h1>{title}</h1>
<p style="color:#666; margin-bottom:2rem;">
  Generado desde <code>{py_file.name}</code> con py2report
</p>

{body_html}

<footer>
  Generado con <strong>py2report.py</strong> — convierte archivos .py comentados en reportes HTML.
</footer>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-core.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-python.min.js"></script>
</body>
</html>"""

    out_path = Path(output)
    out_path.write_text(html, encoding="utf-8")
    size_kb = out_path.stat().st_size / 1024
    print(f"Reporte generado: {output}")
    print(f"Tamanio: {size_kb:.0f} KB")
    print(f"Bloques parseados: {len(blocks)}")
    print(f"Abrir con: xdg-open {output}")
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convierte un archivo .py comentado en un reporte HTML."
    )
    parser.add_argument("pyfile", help="Archivo .py a convertir")
    parser.add_argument("--output", "-o", help="Archivo HTML de salida")
    parser.add_argument("--title", "-t", help="Titulo del reporte")
    args = parser.parse_args()

    generate_report(args.pyfile, args.output, args.title)
