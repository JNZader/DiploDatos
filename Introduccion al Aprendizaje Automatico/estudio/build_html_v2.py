from pathlib import Path
import html
import os
import re

# ---------------------------------------------------------------------------
# Configuración de paths
# ---------------------------------------------------------------------------
ROOT = Path(__file__).parent          # estudio/v2/
BUILD = ROOT / 'build'
BUILD.mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# Detectar páginas automáticamente: README.md primero, luego orden natural
# ---------------------------------------------------------------------------
md_files = sorted(ROOT.glob('*.md'), key=lambda p: p.name.lower())
# Mover README.md al principio si existe
readme = ROOT / 'README.md'
PAGES = []
if readme.exists():
    PAGES.append('README.md')
for f in md_files:
    if f.name != 'README.md':
        PAGES.append(f.name)

# ---------------------------------------------------------------------------
# Extraer metadatos de cada markdown
# ---------------------------------------------------------------------------

def extract_title(md_path: Path) -> str:
    text = md_path.read_text(encoding='utf-8')
    m = re.search(r'^# (.+)$', text, re.MULTILINE)
    if m:
        return m.group(1).strip()
    return md_path.stem.replace('-', ' ').replace('_', ' ').title()


def extract_intro(md_path: Path) -> str:
    text = md_path.read_text(encoding='utf-8')
    # Primer párrafo después del título que no sea vacío ni heading
    lines = text.splitlines()
    after_title = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('# '):
            after_title = True
            continue
        if after_title and stripped and not stripped.startswith('#') and not stripped.startswith('|'):
            # Limpiar markdown inline básico
            clean = re.sub(r'\*\*(.+?)\*\*', r'\1', stripped)
            clean = re.sub(r'`([^`]+)`', r'\1', clean)
            clean = re.sub(r'\[(.*?)\]\((.*?)\)', r'\1', clean)
            return clean[:220] + ('…' if len(clean) > 220 else '')
    return ''


def guess_meta(md_path: Path) -> list[str]:
    text = md_path.read_text(encoding='utf-8').lower()
    tags = []
    name = md_path.stem.lower()
    if 'python' in name or 'numpy' in name:
        tags.append('Python')
    if 'marco' in name:
        tags.append('Marco AA')
    if 'pipeline' in name or 'entrenamiento' in name:
        tags.append('Pipeline')
    if 'regresion-lineal' in name or name == '03-regresion-lineal':
        tags.append('Regresión')
    if 'polinomial' in name:
        tags.append('Polinomial')
    if 'ridge' in name or 'regularizacion' in name:
        tags.append('Regularización')
    if 'clasificacion' in name or 'perceptron' in name:
        tags.append('Clasificación')
    if 'logistica' in name:
        tags.append('Logística')
    if 'naive' in name or 'bayes' in name:
        tags.append('Probabilístico')
    if 'knn' in name or 'no-parametricos' in name:
        tags.append('No paramétrico')
    if 'multiclase' in name:
        tags.append('Multiclase')
    if 'formulario' in name:
        tags.append('Referencia')
    if 'glosario' in name:
        tags.append('Referencia')
    if 'preguntas' in name:
        tags.append('Repaso')
    if 'bibliografia' in name:
        tags.append('Bibliografía')
    if 'guia-de-tp' in name:
        tags.append('Guía TP')
    # tags por contenido
    if 'error común' in text or 'errores comunes' in text:
        tags.append('Errores')
    if 'ejemplo' in text:
        tags.append('Ejemplos')
    if 'tp' in text or 'trabajo práctico' in text:
        tags.append('TP')
    return tags[:3]  # max 3 tags


TITLE_MAP = {page: extract_title(ROOT / page) for page in PAGES}
INTRO_MAP = {page: extract_intro(ROOT / page) for page in PAGES}
META_MAP = {page: guess_meta(ROOT / page) for page in PAGES}

# ---------------------------------------------------------------------------
# CSS idéntico al original (build_html.py)
# ---------------------------------------------------------------------------
CSS = """
:root {
  --bg: #eef3fb;
  --panel: #0b1220;
  --panel-2: #162033;
  --text: #172033;
  --muted: #475569;
  --card: #ffffff;
  --border: #c7d2e3;
  --accent: #1d4ed8;
  --accent-hover: #1e40af;
  --accent-soft: #dbeafe;
  --ok: #166534;
  --ok-soft: #dcfce7;
  --warn: #9a3412;
  --warn-soft: #ffedd5;
  --note: #1e40af;
  --note-soft: #dbeafe;
  --shadow: rgba(15, 23, 42, 0.12);
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  font-family: Inter, Segoe UI, Arial, sans-serif;
  margin: 0;
  background: linear-gradient(180deg, #f8fbff 0%, var(--bg) 100%);
  color: var(--text);
}
a {
  color: var(--accent);
  text-decoration-thickness: 0.1em;
  text-underline-offset: 0.16em;
}
a:hover { color: var(--accent-hover); }
a:focus-visible {
  outline: 3px solid #f59e0b;
  outline-offset: 3px;
  border-radius: 8px;
}
.skip-link {
  position: absolute;
  left: 12px;
  top: -42px;
  background: #111827;
  color: white;
  padding: 10px 14px;
  border-radius: 10px;
  text-decoration: none;
  z-index: 1000;
}
.skip-link:focus { top: 12px; }
.layout {
  display: grid;
  grid-template-columns: 320px minmax(0, 1fr);
  min-height: 100vh;
}
.sidebar {
  background: linear-gradient(180deg, var(--panel) 0%, var(--panel-2) 100%);
  color: #f8fafc;
  padding: 24px 18px;
  position: sticky;
  top: 0;
  height: 100vh;
  overflow: auto;
}
.brand {
  padding: 8px 10px 18px;
  border-bottom: 1px solid rgba(255,255,255,0.12);
  margin-bottom: 14px;
}
.brand h1 {
  font-size: 1.15rem;
  margin: 0 0 10px;
  color: #f8fafc;
}
.brand p { color: #dbe6f4; font-size: 0.92rem; margin: 0; line-height: 1.6; }
.nav-section {
  color: #c7d2e3;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-size: 0.72rem;
  margin: 16px 10px 8px;
}
.nav-link {
  display: block;
  color: #f8fafc;
  text-decoration: none;
  padding: 10px 12px;
  border-radius: 12px;
  margin-bottom: 6px;
  transition: background 0.15s ease, transform 0.15s ease;
  border: 1px solid rgba(255,255,255,0.06);
  background: rgba(255,255,255,0.02);
}
.nav-link:hover, .nav-link.active {
  background: rgba(255,255,255,0.14);
  transform: translateX(2px);
  border-color: rgba(255,255,255,0.18);
}
.nav-title { display: block; font-weight: 600; }
.nav-link.active .nav-title { color: #ffffff; }
.nav-meta { display: flex; gap: 6px; flex-wrap: wrap; margin-top: 6px; }
.nav-pill {
  display: inline-block;
  font-size: 0.72rem;
  color: #f8fafc;
  background: rgba(191, 219, 254, 0.18);
  border: 1px solid rgba(191, 219, 254, 0.36);
  padding: 2px 7px;
  border-radius: 999px;
}
.content { padding: 36px 40px 60px; max-width: 1120px; }
.hero { margin-bottom: 20px; }
.eyebrow {
  color: var(--accent);
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  font-size: 0.78rem;
}
.hero h1 { font-size: 2.35rem; margin: 8px 0 10px; color: #0f172a; }
.hero p { color: var(--muted); max-width: 840px; line-height: 1.75; font-size: 1.02rem; }
.top-actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin-top: 16px;
}
.top-actions a {
  text-decoration: none;
  background: #ffffff;
  border: 1px solid var(--border);
  padding: 10px 14px;
  border-radius: 12px;
  color: var(--text);
  font-weight: 600;
  box-shadow: 0 2px 8px rgba(15, 23, 42, 0.05);
}
.top-actions a:hover { background: #eff6ff; border-color: #93c5fd; }
.card {
  background: var(--card);
  border: 1px solid rgba(15,23,42,0.08);
  border-radius: 22px;
  padding: 34px 38px;
  box-shadow: 0 12px 30px var(--shadow);
}
h1, h2, h3, h4 { color: #0f172a; }
h1 { font-size: 2rem; margin-top: 0; }
h2 { margin-top: 2.3rem; padding-bottom: 0.45rem; border-bottom: 1px solid var(--border); }
h3 { margin-top: 1.6rem; }
p, li { line-height: 1.8; }
li + li { margin-top: 0.25rem; }
code {
  background: var(--accent-soft);
  padding: 0.12rem 0.4rem;
  border-radius: 6px;
  color: #1e3a8a;
  font-family: ui-monospace, SFMono-Regular, monospace;
}
pre {
  background: #0b1220;
  color: #f8fafc;
  padding: 16px;
  border-radius: 14px;
  overflow-x: auto;
  border: 1px solid rgba(255,255,255,0.12);
}
blockquote {
  border-left: 4px solid var(--accent);
  margin: 1rem 0;
  padding: 0.9rem 1rem;
  background: #eff6ff;
  border-radius: 0 12px 12px 0;
}
.section-box {
  margin: 1.25rem 0;
  padding: 1rem 1.1rem;
  border-radius: 16px;
  border: 1px solid var(--border);
  background: #f8fafc;
  box-shadow: 0 4px 12px rgba(15, 23, 42, 0.04);
}
.section-box.note { background: var(--note-soft); border-color: #60a5fa; }
.section-box.ok { background: var(--ok-soft); border-color: #4ade80; }
.section-box.warn { background: var(--warn-soft); border-color: #fb923c; }
.box-label {
  display: inline-block;
  margin-bottom: 0.65rem;
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}
.section-box.note .box-label { color: var(--note); }
.section-box.ok .box-label { color: var(--ok); }
.section-box.warn .box-label { color: var(--warn); }
.quick-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 14px;
  margin: 1rem 0 1.5rem;
}
.quick-card {
  display: block;
  text-decoration: none;
  background: #f8fafc;
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 14px;
  color: var(--text);
  box-shadow: 0 3px 10px rgba(15, 23, 42, 0.04);
}
.quick-card:hover { background: #ffffff; border-color: #93c5fd; }
.quick-card strong { display: block; margin-bottom: 8px; }
figure { margin: 1.2rem 0; }
figure img {
  width: 100%;
  border-radius: 16px;
  border: 1px solid var(--border);
  box-shadow: 0 10px 24px rgba(15,23,42,0.10);
  background: white;
}
figcaption { color: var(--muted); font-size: 0.95rem; margin-top: 0.55rem; }
.pager {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  margin-top: 28px;
  padding-top: 20px;
  border-top: 1px solid var(--border);
}
.pager a {
  flex: 1;
  text-decoration: none;
  background: #f8fafc;
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 14px 16px;
  color: var(--text);
  font-weight: 600;
}
.pager a:hover { background: #ffffff; border-color: #93c5fd; }
.pager .next { text-align: right; }
table {
  width: 100%;
  border-collapse: collapse;
  margin: 1rem 0;
  font-size: 0.95rem;
}
th, td {
  border: 1px solid var(--border);
  padding: 10px 12px;
  text-align: left;
}
th {
  background: #f1f5f9;
  font-weight: 600;
}
tr:nth-child(even) { background: #f8fafc; }
@media (max-width: 900px) {
  .layout { grid-template-columns: 1fr; }
  .sidebar { position: relative; height: auto; }
  .content { padding: 20px; }
  .card { padding: 22px; }
  .hero h1 { font-size: 1.9rem; }
  .pager { flex-direction: column; }
}
"""


# ---------------------------------------------------------------------------
# Conversión Markdown -> HTML (parser custom idéntico al original)
# ---------------------------------------------------------------------------

def page_target(page: str) -> str:
    if page == 'README.md':
        return 'index.html'
    # Don't rewrite external URLs or anchors
    if re.match(r'^[a-z]+://', page) or page.startswith('#'):
        return page
    p = Path(page)
    if p.suffix == '.md':
        return str(p.with_suffix('.html'))
    return page


def inline_format(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    text = re.sub(
        r'\[(.*?)\]\((.*?)\)',
        lambda m: f'<a href="{page_target(m.group(2))}">{m.group(1)}</a>',
        text,
    )
    return text


def image_to_html(stripped: str, source_dir: Path) -> str | None:
    m = re.match(r'^!\[(.*?)\]\((.*?)\)$', stripped)
    if not m:
        return None
    alt, src = m.groups()
    if re.match(r'^[a-z]+://', src):
        out_src = src
    else:
        # Si la imagen está en img_viz/ (carpeta compartida de v2),
        # usar ruta directa relativa a build/ (donde ya copiamos las imágenes)
        if src.startswith('img_viz/'):
            out_src = src
        else:
            target = (source_dir / src).resolve()
            out_src = os.path.relpath(target, BUILD).replace('\\', '/')
    return f'<figure><img src="{html.escape(out_src)}" alt="{html.escape(alt)}"><figcaption>{html.escape(alt)}</figcaption></figure>'


def box_kind(title: str) -> str | None:
    lower = title.lower()
    if 'mini ejercicio resuelto' in lower:
        return 'ok'
    if 'error común' in lower or 'error comun' in lower:
        return 'warn'
    if 'ejemplo' in lower:
        return 'note'
    return None


def md_to_html(md: str, source_dir: Path) -> str:
    lines = md.splitlines()
    out = []
    in_code = False
    in_ul = False
    in_ol = False
    in_blockquote = False
    in_display_math = False
    display_math_buffer: list[str] = []
    current_box = None

    def close_lists():
        nonlocal in_ul, in_ol
        if in_ul:
            out.append('</ul>')
            in_ul = False
        if in_ol:
            out.append('</ol>')
            in_ol = False

    def close_box():
        nonlocal current_box
        if current_box is not None:
            close_lists()
            out.append('</section>')
            current_box = None

    for raw in lines:
        line = raw.rstrip('\n')
        stripped = line.strip()

        if stripped.startswith('```'):
            close_lists()
            close_box()
            if in_blockquote:
                out.append('</blockquote>')
                in_blockquote = False
            if not in_code:
                out.append('<pre><code>')
                in_code = True
            else:
                out.append('</code></pre>')
                in_code = False
            continue

        if in_code:
            out.append(html.escape(line))
            continue

        # Detectar bloques display math $$ ... $$
        if stripped == '$$':
            if not in_display_math:
                # Iniciar bloque display math
                close_lists()
                close_box()
                if in_blockquote:
                    out.append('</blockquote>')
                    in_blockquote = False
                in_display_math = True
                display_math_buffer = ['$$']
            else:
                # Cerrar bloque display math
                display_math_buffer.append('$$')
                math_content = '\n'.join(display_math_buffer)
                out.append(f'<div class="math">{math_content}</div>')
                in_display_math = False
                display_math_buffer = []
            continue

        if in_display_math:
            display_math_buffer.append(line)
            continue

        if not stripped:
            close_lists()
            if in_blockquote:
                out.append('</blockquote>')
                in_blockquote = False
            continue

        image_html = image_to_html(stripped, source_dir)
        if image_html is not None:
            close_lists()
            if in_blockquote:
                out.append('</blockquote>')
                in_blockquote = False
            out.append(image_html)
            continue

        if stripped.startswith('> '):
            close_lists()
            if not in_blockquote:
                out.append('<blockquote>')
                in_blockquote = True
            out.append(f'<p>{inline_format(stripped[2:])}</p>')
            continue
        elif in_blockquote:
            out.append('</blockquote>')
            in_blockquote = False

        if stripped.startswith('# '):
            close_box()
            out.append(f'<h1>{inline_format(stripped[2:])}</h1>')
        elif stripped.startswith('## '):
            close_box()
            title = stripped[3:]
            kind = box_kind(title)
            if kind:
                label = 'Ejercicio' if kind == 'ok' else 'Atención' if kind == 'warn' else 'Ejemplo'
                out.append(f'<section class="section-box {kind}"><div class="box-label">{label}</div><h2>{inline_format(title)}</h2>')
                current_box = kind
            else:
                out.append(f'<h2>{inline_format(title)}</h2>')
        elif stripped.startswith('### '):
            out.append(f'<h3>{inline_format(stripped[4:])}</h3>')
        elif stripped.startswith('#### '):
            out.append(f'<h4>{inline_format(stripped[5:])}</h4>')
        elif re.match(r'^\d+\. ', stripped):
            if not in_ol:
                close_lists()
                out.append('<ol>')
                in_ol = True
            item = re.sub(r'^\d+\.\s+', '', stripped)
            out.append(f'<li>{inline_format(item)}</li>')
        elif stripped.startswith('- '):
            if not in_ul:
                close_lists()
                out.append('<ul>')
                in_ul = True
            out.append(f'<li>{inline_format(stripped[2:])}</li>')
        elif stripped.startswith('|') and stripped.endswith('|'):
            # Tablas markdown básicas: renderizar como filas de tabla HTML
            # Acumulamos en buffer y procesamos al final del bloque de tabla
            # Por simplicidad en este parser custom, las manejamos línea por línea
            # Saltamos la línea de separación de tabla (|---|)
            if re.match(r'^\|[\s\-:|]+\|$', stripped):
                continue
            cells = [c.strip() for c in stripped[1:-1].split('|')]
            if not hasattr(md_to_html, '_in_table'):
                md_to_html._in_table = False
                md_to_html._table_header = []
                md_to_html._table_rows = []
            if not md_to_html._in_table:
                md_to_html._in_table = True
                md_to_html._table_header = cells
                md_to_html._table_rows = []
            else:
                md_to_html._table_rows.append(cells)
            # No cerramos lists aquí; el siguiente non-table line cerrará
            continue
        else:
            close_lists()
            # Si veníamos de tabla, cerrarla
            if getattr(md_to_html, '_in_table', False):
                thead = ''.join(f'<th>{inline_format(c)}</th>' for c in md_to_html._table_header)
                tbody = ''
                for row in md_to_html._table_rows:
                    tbody += '<tr>' + ''.join(f'<td>{inline_format(c)}</td>' for c in row) + '</tr>'
                out.append(f'<table><thead><tr>{thead}</tr></thead><tbody>{tbody}</tbody></table>')
                md_to_html._in_table = False
                md_to_html._table_header = []
                md_to_html._table_rows = []
            out.append(f'<p>{inline_format(stripped)}</p>')

    close_lists()
    if in_blockquote:
        out.append('</blockquote>')
    if in_code:
        out.append('</code></pre>')
    if current_box is not None:
        out.append('</section>')
    # Cerrar tabla si quedó abierta
    if getattr(md_to_html, '_in_table', False):
        thead = ''.join(f'<th>{inline_format(c)}</th>' for c in md_to_html._table_header)
        tbody = ''
        for row in md_to_html._table_rows:
            tbody += '<tr>' + ''.join(f'<td>{inline_format(c)}</td>' for c in row) + '</tr>'
        out.append(f'<table><thead><tr>{thead}</tr></thead><tbody>{tbody}</tbody></table>')
        md_to_html._in_table = False
        md_to_html._table_header = []
        md_to_html._table_rows = []
    return '\n'.join(out)


# ---------------------------------------------------------------------------
# Componentes de UI (navbar, pager, home cards)
# ---------------------------------------------------------------------------

def nav(current: str) -> str:
    links = []
    for page in PAGES:
        target = page_target(page)
        cls = 'active' if page == current else ''
        meta = ''.join(f'<span class="nav-pill">{html.escape(tag)}</span>' for tag in META_MAP.get(page, []))
        links.append(
            f'<a class="nav-link {cls}" href="{target}">'
            f'<span class="nav-title">{html.escape(TITLE_MAP[page])}</span>'
            f'<span class="nav-meta">{meta}</span>'
            f'</a>'
        )
    return '\n'.join(links)


def pager(page: str) -> str:
    idx = PAGES.index(page)
    prev_html = '<span></span>'
    next_html = ''
    if idx > 0:
        prev_page = PAGES[idx - 1]
        prev_html = f'<a class="prev" href="{page_target(prev_page)}">← {html.escape(TITLE_MAP[prev_page])}</a>'
    if idx < len(PAGES) - 1:
        next_page = PAGES[idx + 1]
        next_html = f'<a class="next" href="{page_target(next_page)}">{html.escape(TITLE_MAP[next_page])} →</a>'
    return f'<nav class="pager" aria-label="Navegación entre páginas">{prev_html}{next_html}</nav>'


def home_cards() -> str:
    cards = []
    for page in PAGES[1:]:
        cards.append(
            f'<a class="quick-card" href="{page_target(page)}">'
            f'<strong>{html.escape(TITLE_MAP[page])}</strong>'
            f'<span>{html.escape(INTRO_MAP[page])}</span>'
            f'</a>'
        )
    return '<div class="quick-grid">' + ''.join(cards) + '</div>'


# ---------------------------------------------------------------------------
# Generación
# ---------------------------------------------------------------------------

errors = []
generated = []

for page in PAGES:
    md_path = ROOT / page
    try:
        content = md_to_html(md_path.read_text(encoding='utf-8'), md_path.parent)
    except Exception as e:
        errors.append(f'{page}: {e}')
        continue
    if page == 'README.md':
        content += home_cards()
    out_name = page_target(page)
    out_path = BUILD / out_name
    page_html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(TITLE_MAP[page])} — Apuntes IAA</title>
<style>{CSS}</style>
<script>
MathJax = {{
  tex: {{
    inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
    displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
    processEscapes: true
  }},
  svg: {{
    fontCache: 'global'
  }}
}};
</script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
</head>
<body>
  <a class="skip-link" href="#contenido">Saltar al contenido</a>
  <div class="layout">
    <nav class="sidebar" aria-label="Navegación principal">
      <div class="brand">
        <h1>Apuntes IAA</h1>
        <p>Reformulación pedagógica con ejemplos, analogías y conexión con los TPs.</p>
      </div>
      <div class="nav-section">Módulos</div>
      {nav(page)}
    </nav>
    <main id="contenido" class="content">
      <header class="hero">
        <div class="eyebrow">Diplomatura · estudio v2</div>
        <h1>{html.escape(TITLE_MAP[page])}</h1>
        <p>{html.escape(INTRO_MAP[page])}</p>
        <div class="top-actions">
          <a href="index.html">Volver al índice</a>
        </div>
      </header>
      <article class="card">
        {content}
        {pager(page)}
      </article>
    </main>
  </div>
</body>
</html>"""
    out_path.write_text(page_html, encoding='utf-8')
    generated.append(out_name)

print('─' * 50)
print(f'HTML generados en: {BUILD}')
print(f'Archivos procesados: {len(generated)}')
if errors:
    print(f'Errores: {len(errors)}')
    for e in errors:
        print(f'  ⚠ {e}')
else:
    print('Sin errores.')
print('─' * 50)
for g in generated:
    print(f'  ✓ {g}')
