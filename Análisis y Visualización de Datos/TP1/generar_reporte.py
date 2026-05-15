"""
Genera un reporte HTML con los resultados del TP de Análisis y Visualización.
Ejecutar DESPUES de ejercicio1.py (necesita los PNGs generados).

Uso:
    python generar_reporte.py

Genera: reporte.html (archivo unico, graficos embebidos en base64)
"""

import base64
from pathlib import Path

OUTPUT = "reporte.html"
DIR = Path(__file__).parent


def img_to_base64(filename: str) -> str:
    """Convierte un PNG a base64 para embeber en HTML."""
    path = DIR / "img" / filename
    if not path.exists():
        return f'<p style="color:red;">Imagen no encontrada: img/{filename}</p>'
    data = path.read_bytes()
    b64 = base64.b64encode(data).decode()
    return f'<img src="data:image/png;base64,{b64}" style="max-width:100%; border-radius:8px; margin:1rem 0;">'


html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>TP Entregable - Análisis y Visualización de Datos</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
    line-height: 1.7;
    color: #1a1a2e;
    background: #f8f9fa;
    padding: 2rem;
  }}
  .container {{ max-width: 960px; margin: 0 auto; }}
  h1 {{
    font-size: 2rem;
    color: #16213e;
    border-bottom: 3px solid #0f3460;
    padding-bottom: 0.5rem;
    margin-bottom: 1.5rem;
  }}
  h2 {{
    font-size: 1.5rem;
    color: #0f3460;
    margin-top: 2.5rem;
    margin-bottom: 0.8rem;
  }}
  h3 {{
    font-size: 1.2rem;
    color: #533483;
    margin-top: 1.5rem;
    margin-bottom: 0.5rem;
  }}
  p, li {{ margin-bottom: 0.5rem; }}
  ul {{ padding-left: 1.5rem; }}
  .card {{
    background: white;
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1.5rem 0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  }}
  .highlight {{
    background: #e8f4f8;
    border-left: 4px solid #0f3460;
    padding: 1rem 1.5rem;
    border-radius: 0 8px 8px 0;
    margin: 1rem 0;
  }}
  .conclusion {{
    background: #f0e6ff;
    border-left: 4px solid #533483;
    padding: 1rem 1.5rem;
    border-radius: 0 8px 8px 0;
    margin: 1rem 0;
  }}
  table {{
    border-collapse: collapse;
    width: 100%;
    margin: 1rem 0;
    font-size: 0.9rem;
  }}
  th, td {{
    padding: 0.6rem 1rem;
    text-align: right;
    border-bottom: 1px solid #dee2e6;
  }}
  th {{ background: #0f3460; color: white; text-align: center; }}
  td:first-child, th:first-child {{ text-align: left; }}
  tr:hover {{ background: #f1f3f5; }}
  .tag {{
    display: inline-block;
    padding: 0.2rem 0.6rem;
    border-radius: 4px;
    font-size: 0.8rem;
    font-weight: 600;
    margin: 0.2rem;
  }}
  .tag-high {{ background: #d4edda; color: #155724; }}
  .tag-mid {{ background: #fff3cd; color: #856404; }}
  .tag-low {{ background: #f8d7da; color: #721c24; }}
  .grid-2 {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
  }}
  @media (max-width: 768px) {{
    .grid-2 {{ grid-template-columns: 1fr; }}
    body {{ padding: 1rem; }}
  }}
</style>
</head>
<body>
<div class="container">

<h1>Diplomatura en Ciencia de Datos — Entregable Parte 1</h1>
<p><strong>Edicion 2026</strong> | Analisis y Visualizacion de Datos</p>
<p>Dataset: Encuesta Sysarmy 2026 (procesada) — 4939 respuestas, 60 variables</p>

<!-- ============================================================ -->
<h2>Ejercicio 1 — Analisis Descriptivo</h2>
<p><strong>Pregunta:</strong> ¿Cuales son los lenguajes de programacion asociados a los mejores salarios?</p>
<!-- ============================================================ -->

<div class="card">
<h3>Preparacion de datos</h3>
<p><strong>Columnas seleccionadas:</strong> salary_monthly_NETO, tools_programming_languages, work_dedication, work_seniority</p>

<div class="highlight">
<strong>Pregunta reformulada:</strong> ¿Cuales son los lenguajes asociados a mejores salarios entre <em>trabajadores full-time</em> de IT en Argentina?
</div>

<p><strong>Pipeline de limpieza:</strong></p>
<table>
<tr><th>Paso</th><th>Criterio</th><th>Filas restantes</th></tr>
<tr><td>Dataset original</td><td>—</td><td>4,939</td></tr>
<tr><td>Eliminar NaN en salario</td><td>dropna</td><td>4,717</td></tr>
<tr><td>Eliminar NaN en lenguajes</td><td>dropna</td><td>4,716</td></tr>
<tr><td>Solo Full-Time</td><td>work_dedication == "Full-Time"</td><td>4,515</td></tr>
<tr><td>Salarios validos</td><td>$300K — $20M (dominio)</td><td>4,467</td></tr>
<tr><td>Outliers IQR</td><td>Q1 - 1.5*IQR a Q3 + 1.5*IQR</td><td>4,243</td></tr>
</table>
<p>Se descartaron 696 filas (14.1%). Lenguajes con >= 100 respuestas: 15 lenguajes seleccionados.</p>
</div>

<!-- OPCION A -->
<div class="card">
<h3>Opcion A — Comparacion de distribuciones</h3>

<p><strong>Boxplot:</strong> La caja muestra Q1-Q3 (50% central), la linea es la mediana, bigotes hasta 1.5*IQR.</p>
{img_to_base64("opcion_a1_boxplot.png")}

<p><strong>Violinplot:</strong> Combina boxplot + KDE. La forma muestra donde se concentran los datos.</p>
{img_to_base64("opcion_a2_violinplot.png")}

<p><strong>KDE (top 6):</strong> Curvas de densidad superpuestas. Go y Kotlin estan desplazados a la derecha.</p>
{img_to_base64("opcion_a3_kde_top6.png")}

<div class="conclusion">
<strong>Observacion:</strong> Go y Kotlin tienen distribuciones claramente desplazadas hacia salarios mas altos.
La separacion es mas visible a partir de $3M.
</div>
</div>

<!-- OPCION B -->
<div class="card">
<h3>Opcion B — Estadistica descriptiva</h3>

<p><strong>Mediana con intervalo de confianza 95% (bootstrap):</strong></p>
{img_to_base64("opcion_b1_barplot_mediana.png")}

<p><strong>Porcentaje de cada lenguaje en el top 10% de salarios (>= $5.2M):</strong></p>
{img_to_base64("opcion_b2_heatmap_top10.png")}

<div class="highlight">
<strong>Hallazgo:</strong> El 22.1% de los programadores de Go estan en el top 10% de salarios,
mas del doble que el promedio (~10%). Kotlin le sigue con 16.8%.
</div>

<p><strong>Ranking por mediana:</strong></p>
<table>
<tr><th>Lenguaje</th><th>N</th><th>Mediana</th><th>P90</th><th>Top 10%</th></tr>
<tr><td><span class="tag tag-high">Go</span></td><td>217</td><td>$3,672,182</td><td>$6,000,000</td><td>22.1%</td></tr>
<tr><td><span class="tag tag-high">Kotlin</span></td><td>113</td><td>$3,600,000</td><td>$5,892,200</td><td>16.8%</td></tr>
<tr><td><span class="tag tag-mid">C++</span></td><td>105</td><td>$3,200,000</td><td>$5,840,000</td><td>14.3%</td></tr>
<tr><td><span class="tag tag-mid">Java</span></td><td>690</td><td>$3,109,000</td><td>$5,600,000</td><td>13.6%</td></tr>
<tr><td>Bash/Shell</td><td>750</td><td>$2,980,000</td><td>$5,500,000</td><td>11.5%</td></tr>
<tr><td>Python</td><td>1496</td><td>$2,900,000</td><td>$5,300,000</td><td>11.0%</td></tr>
<tr><td>TypeScript</td><td>942</td><td>$2,900,000</td><td>$5,200,000</td><td>10.2%</td></tr>
<tr><td>Javascript</td><td>1578</td><td>$2,750,000</td><td>$5,100,000</td><td>9.5%</td></tr>
<tr><td>C#</td><td>383</td><td>$2,719,000</td><td>$5,092,364</td><td>9.9%</td></tr>
<tr><td>.NET</td><td>475</td><td>$2,700,000</td><td>$5,084,728</td><td>9.3%</td></tr>
<tr><td>SQL</td><td>1917</td><td>$2,697,129</td><td>$5,000,000</td><td>8.4%</td></tr>
<tr><td>VBA</td><td>116</td><td>$2,671,548</td><td>$4,111,000</td><td>5.2%</td></tr>
<tr><td>HTML</td><td>1183</td><td>$2,600,000</td><td>$4,999,200</td><td>8.2%</td></tr>
<tr><td>CSS</td><td>748</td><td>$2,600,000</td><td>$4,806,366</td><td>7.6%</td></tr>
<tr><td><span class="tag tag-low">PHP</span></td><td>479</td><td>$2,546,671</td><td>$5,120,000</td><td>10.0%</td></tr>
</table>
</div>

<!-- OPCION C -->
<div class="card">
<h3>Opcion C — Probabilidades condicionales</h3>

<p>P(salario >= X | sabe lenguaje L) — probabilidad de ganar mas de X dado que sabe L.</p>
{img_to_base64("opcion_c1_probabilidades.png")}

<table>
<tr><th>Lenguaje</th><th>>= $2M</th><th>>= $3M</th><th>>= $4M</th><th>>= $5M</th></tr>
<tr><td><strong>Go</strong></td><td>91.7%</td><td>71.4%</td><td>41.9%</td><td>26.3%</td></tr>
<tr><td><strong>Kotlin</strong></td><td>87.6%</td><td>68.1%</td><td>43.4%</td><td>22.1%</td></tr>
<tr><td>C++</td><td>69.5%</td><td>55.2%</td><td>33.3%</td><td>21.0%</td></tr>
<tr><td>Java</td><td>79.9%</td><td>55.7%</td><td>32.2%</td><td>18.1%</td></tr>
<tr><td>Python</td><td>76.9%</td><td>48.3%</td><td>26.9%</td><td>14.2%</td></tr>
<tr><td colspan="5" style="text-align:center; color:#666;">Base: 73.8% | 45.8% | 25.3% | 12.8%</td></tr>
</table>

<div class="conclusion">
<strong>Lift:</strong> Si sabes Go, tenes un <strong>106% mas de chances</strong> de ganar >= $5M que el promedio.
Kotlin: +74%. C++: +64%. Java: +42%.
</div>
</div>

<!-- CONCLUSION EJ1 -->
<div class="card">
<h3>Conclusion — Ejercicio 1</h3>
<div class="conclusion">
<p>Los tres enfoques (distribuciones, estadistica descriptiva y probabilidades) convergen en la misma conclusion:</p>
<ul>
<li><span class="tag tag-high">Go</span> y <span class="tag tag-high">Kotlin</span> son los lenguajes asociados a los mejores salarios</li>
<li><span class="tag tag-mid">C++</span> y <span class="tag tag-mid">Java</span> ocupan el segundo escalon</li>
<li><span class="tag tag-low">PHP</span>, CSS y HTML estan en la parte baja del ranking</li>
</ul>
<p><strong>Caveat:</strong> Correlacion no implica causalidad. Go y Kotlin pueden pagar mas porque se usan en empresas grandes o porque los perfiles que los saben tienden a ser mas senior.</p>
</div>
</div>

<!-- ============================================================ -->
<h2>Ejercicio 2 — Densidades y varias variables</h2>
<p><strong>Pregunta:</strong> ¿Que herramientas son utiles para explorar la base, descubrir patrones y asociaciones?</p>
<!-- ============================================================ -->

<div class="card">
<h3>Variables seleccionadas</h3>
<div class="grid-2">
<div>
<p><strong>Numericas:</strong></p>
<ul>
<li>salary_monthly_NETO</li>
<li>salary_monthly_BRUTO</li>
<li>profile_age</li>
</ul>
</div>
<div>
<p><strong>Categoricas:</strong></p>
<ul>
<li>work_seniority (Senior / Semi-Senior / Junior)</li>
<li>profile_gender</li>
</ul>
</div>
</div>
<p>Dataset: 4,653 filas despues de limpieza basica (edad 18-70, salarios $300K-$20M).</p>
</div>

<!-- 2a -->
<div class="card">
<h3>2a) Densidad conjunta</h3>

<p><strong>Pairplot</strong> — cruza todas las numericas, coloreado por seniority:</p>
{img_to_base64("ej2a_pairplot.png")}

<p><strong>Jointplot KDE</strong> — densidad conjunta edad vs salario (curvas de nivel = zonas de mayor concentracion):</p>
{img_to_base64("ej2a_jointplot_edad_salario.png")}

<p><strong>Matriz de correlacion de Pearson:</strong></p>
{img_to_base64("ej2a_heatmap_correlacion.png")}

<div class="highlight">
<strong>Observaciones:</strong>
<ul>
<li>Bruto-Neto: r = 0.950 — casi perfectamente lineal</li>
<li>Edad-Salario: r = 0.17 — relacion positiva pero debil</li>
<li>La zona de mayor densidad esta entre 25-45 anios y $1M-$5M</li>
<li>Los Seniors tienen distribuciones desplazadas hacia salarios mas altos</li>
</ul>
</div>
</div>

<!-- 2b -->
<div class="card">
<h3>2b) Asociacion — ¿Se puede sacar la columna de salario bruto?</h3>

{img_to_base64("ej2b_scatter_bruto_neto.png")}

<table>
<tr><th>Metrica</th><th>Valor</th><th>Interpretacion</th></tr>
<tr><td>Pearson r</td><td>0.9504</td><td>Correlacion muy fuerte positiva</td></tr>
<tr><td>R²</td><td>0.9033</td><td>El bruto explica el 90.3% de la varianza del neto</td></tr>
<tr><td>Spearman rho</td><td>0.9578</td><td>Relacion monotona aun mas fuerte</td></tr>
<tr><td>p-valor</td><td>~0</td><td>Estadisticamente significativo</td></tr>
</table>

<div class="conclusion">
<strong>Conclusion:</strong> Con r = 0.95 y R² = 0.90, la columna de salario bruto es <strong>redundante</strong>.
Se puede sacar de la encuesta sin perder informacion significativa.
</div>
</div>

<!-- 2c -->
<div class="card">
<h3>2c) Densidad condicional — Salario segun nivel de estudio</h3>

{img_to_base64("ej2c_histogramas_estudio.png")}

<table>
<tr><th>Metrica</th><th>Universitario (n=1,116)</th><th>Terciario (n=257)</th></tr>
<tr><td>Media</td><td>$3,340,980</td><td>$2,533,467</td></tr>
<tr><td>Mediana</td><td>$2,945,086</td><td>$2,158,000</td></tr>
<tr><td>Std</td><td>$2,092,015</td><td>$1,641,000</td></tr>
<tr><td>Q1</td><td>$1,900,000</td><td>$1,500,000</td></tr>
<tr><td>Q3</td><td>$4,200,000</td><td>$3,000,000</td></tr>
<tr><td>IQR</td><td>$2,300,000</td><td>$1,500,000</td></tr>
</table>

<div class="highlight">
<strong>Test Mann-Whitney U:</strong> p = 2.78e-11<br>
Rechazamos H0: las distribuciones son <strong>diferentes</strong>. El salario y el nivel de estudio <strong>NO son independientes</strong>.
Los universitarios ganan una mediana 36% mas alta que los terciarios.
</div>
</div>

<!-- 2d -->
<div class="card">
<h3>2d) Densidad conjunta condicional</h3>

<p><strong>Scatterplot</strong> edad vs salario, coloreado por seniority:</p>
{img_to_base64("ej2d_scatter_hue_seniority.png")}

<p><strong>Regresion lineal</strong> por grupo — cada seniority tiene su propia pendiente:</p>
{img_to_base64("ej2d_lmplot_seniority.png")}

<div class="conclusion">
<strong>Observaciones:</strong>
<ul>
<li>Los Seniors dominan la zona alta de salarios en TODAS las edades</li>
<li>Los Juniors estan concentrados en edades bajas (20-30) y salarios bajos</li>
<li>La pendiente de Senior es ligeramente positiva — mas experiencia, mas sueldo</li>
<li>La pendiente de Junior es casi plana — la edad no mueve el salario sin seniority</li>
</ul>
</div>
</div>

<hr style="margin: 2rem 0; border-color: #dee2e6;">
<p style="color: #666; font-size: 0.85rem;">
Generado automaticamente desde el analisis de la Encuesta Sysarmy 2026.
Diplomatura en Ciencia de Datos — Universidad Nacional de Cordoba.
</p>

</div>
</body>
</html>"""

Path(OUTPUT).write_text(html, encoding="utf-8")
print(f"Reporte generado: {OUTPUT}")
print(f"Tamanio: {Path(OUTPUT).stat().st_size / 1024:.0f} KB")
print(f"Abrir con: xdg-open {OUTPUT}")
