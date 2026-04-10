"""
Genera un reporte HTML COMPLETO con:
  - Los resultados y graficos del TP (igual que reporte.html)
  - TODAS las explicaciones conceptuales de los comentarios de ejercicio1.py

Ejecutar DESPUES de ejercicio1.py (necesita los PNGs generados).

Uso:
    python reporte_completo.py

Genera: reporte_completo.html (archivo unico, graficos embebidos en base64)
"""

import base64
from pathlib import Path

OUTPUT = "reporte_completo.html"
DIR = Path(__file__).parent


def img_to_base64(filename: str) -> str:
    """Convierte un PNG a base64 para embeber en HTML."""
    path = DIR / filename
    if not path.exists():
        return f'<p style="color:red;">Imagen no encontrada: {filename}</p>'
    data = path.read_bytes()
    b64 = base64.b64encode(data).decode()
    return f'<img src="data:image/png;base64,{b64}" style="max-width:100%; border-radius:8px; margin:1rem 0;">'


html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>TP Entregable Completo - Análisis y Visualización de Datos</title>
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
  .concept {{
    background: #fff8e1;
    border-left: 4px solid #ff8f00;
    padding: 1rem 1.5rem;
    border-radius: 0 8px 8px 0;
    margin: 1rem 0;
    font-size: 0.95rem;
  }}
  .concept strong {{ color: #e65100; }}
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

<h1>Diplomatura en Ciencia de Datos — Entregable Parte 1 (Reporte Completo)</h1>
<p><strong>Edicion 2026</strong> | Analisis y Visualizacion de Datos</p>
<p>Dataset: Encuesta Sysarmy 2026 (procesada) — 4939 respuestas, 60 variables</p>
<p><em>Este reporte incluye tanto los resultados del analisis como las explicaciones conceptuales de cada paso.</em></p>

<!-- ============================================================ -->
<h2>Ejercicio 1 — Analisis Descriptivo</h2>
<p><strong>Pregunta:</strong> ¿Cuales son los lenguajes de programacion asociados a los mejores salarios?</p>
<!-- ============================================================ -->

<!-- PASO 0: IMPORTS -->
<div class="card">
<h3>Paso 0 — Imports y configuracion</h3>

<div class="concept">
<strong>pandas:</strong> LA libreria para manipular datos tabulares (como un Excel con superpoderes).
Un <em>DataFrame</em> es una tabla con filas y columnas; una <em>Series</em> es una sola columna.<br><br>

<strong>matplotlib:</strong> Libreria base de graficos en Python. seaborn se construye ENCIMA de ella.<br><br>

<strong>seaborn:</strong> Graficos estadisticos de alto nivel. Mas lindo y mas facil que matplotlib puro.
<code>set_context('talk')</code> agranda fuentes y elementos para que se vea bien en presentaciones.<br><br>

<strong>numpy:</strong> Operaciones numericas. pandas lo usa internamente.
</div>
</div>

<!-- PASO 1: CARGA -->
<div class="card">
<h3>Paso 1 — Carga de datos</h3>

<div class="concept">
<strong>pd.read_csv()</strong> lee un archivo CSV (Comma-Separated Values) y lo convierte en un DataFrame.
Puede leer desde una URL directamente — no necesitas descargar el archivo.
</div>
</div>

<!-- PASO 2: EXPLORACION -->
<div class="card">
<h3>Paso 2 — Exploracion inicial</h3>

<div class="concept">
<strong>Las 4 preguntas basicas</strong> que SIEMPRE te haces al recibir un dataset:
<ol>
<li><strong>¿Cuantas filas y columnas tiene?</strong> → <code>.shape</code></li>
<li><strong>¿Que columnas hay y de que tipo son?</strong> → <code>.dtypes</code> / <code>.info()</code></li>
<li><strong>¿Hay valores nulos?</strong> → <code>.isnull().sum()</code></li>
<li><strong>¿Como se ven los datos?</strong> → <code>.head()</code> / <code>.describe()</code></li>
</ol>
</div>

<div class="concept">
<strong>dtypes (tipos de datos):</strong> Te dice si cada columna es numerica (<code>int64</code>, <code>float64</code>) o texto (<code>object</code>).
Esto es CLAVE porque determina que operaciones podes hacer:
<ul>
<li><strong>Numericas:</strong> media, mediana, correlacion, histogramas</li>
<li><strong>Categoricas (object):</strong> conteo de frecuencias, agrupacion, barplots</li>
</ul>
</div>

<div class="concept">
<strong>.describe()</strong> te da de una:
<ul>
<li><strong>count:</strong> cuantos valores NO nulos hay</li>
<li><strong>mean:</strong> promedio (suma / cantidad)</li>
<li><strong>std:</strong> desviacion estandar (que tan dispersos estan los datos respecto a la media)</li>
<li><strong>min/max:</strong> valores extremos</li>
<li><strong>25%, 50%, 75%:</strong> percentiles (cuartiles)</li>
</ul>
El <strong>50%</strong> es la <em>mediana</em> (el valor que divide los datos en dos mitades iguales).
El <strong>25%</strong> y <strong>75%</strong> definen el <strong>IQR</strong> (rango intercuartilico), usado para detectar outliers.
</div>
</div>

<!-- PASO 3: COLUMNAS -->
<div class="card">
<h3>Paso 3 — Seleccion de columnas relevantes</h3>

<div class="concept">
<strong>Variables de control (confounders):</strong> No todas las columnas sirven para responder nuestra pregunta.
Necesitamos pensar: "¿que variables INFLUYEN en la relacion lenguaje-salario?"<br><br>

Columnas elegidas y POR QUE:
<ul>
<li><strong>tools_programming_languages:</strong> los lenguajes (variable central de la pregunta)</li>
<li><strong>salary_monthly_NETO:</strong> el salario. Usamos NETO porque es lo que la persona realmente cobra. El BRUTO depende del tipo de contrato y deducciones.</li>
<li><strong>work_dedication:</strong> Full-Time vs Part-Time. Si no filtramos, un part-time con salario bajo contamina el analisis (gana menos por TRABAJAR MENOS, no por el lenguaje que usa).</li>
<li><strong>work_seniority:</strong> Senior vs Junior. Un senior de PHP puede ganar mas que un junior de Rust. Si no controlamos esto, confundimos experiencia con lenguaje.</li>
</ul>

Estos son factores que afectan el salario pero NO son el lenguaje.
Si no los controlamos, nuestras conclusiones pueden ser <strong>FALSAS</strong>.
</div>

<p><strong>Columnas seleccionadas:</strong> salary_monthly_NETO, tools_programming_languages, work_dedication, work_seniority</p>

<div class="highlight">
<strong>Pregunta reformulada:</strong> ¿Cuales son los lenguajes asociados a mejores salarios entre <em>trabajadores full-time</em> de IT en Argentina?
</div>
</div>

<!-- PASO 4: LIMPIEZA -->
<div class="card">
<h3>Paso 4 — Limpieza de datos</h3>

<div class="concept">
<strong>NaN (Not a Number):</strong> Representa datos faltantes. No podemos comparar salarios si no HAY salario.
<code>.dropna()</code> elimina esas filas. <code>subset=</code> indica en que columnas buscar NaN.<br><br>

<strong>Datos "raros" — dos tipos:</strong>
<ul>
<li><strong>ERRORES:</strong> alguien puso $1.6 o $653M. Imposible. Se eliminan.</li>
<li><strong>OUTLIERS:</strong> valores extremos pero posibles. No son "errores", pero distorsionan las metricas.</li>
</ul>
</div>

<div class="concept">
<strong>Criterio por dominio (conocimiento del mundo real):</strong>
<ul>
<li>Salario minimo en Argentina 2026: ~300K. Menos que eso es error.</li>
<li>Mas de $20M netos para IT en Argentina: muy improbable, posible error.</li>
</ul>

<strong>Metodo IQR (Interquartile Range):</strong> Alternativa mas "estadistica".
<ul>
<li><strong>Q1 (percentil 25):</strong> el 25% de los datos esta por debajo</li>
<li><strong>Q3 (percentil 75):</strong> el 75% de los datos esta por debajo</li>
<li><strong>IQR = Q3 - Q1:</strong> el "ancho" del 50% central</li>
<li><strong>Limites:</strong> [Q1 - 1.5*IQR, Q3 + 1.5*IQR]</li>
</ul>
El IQR es robusto contra outliers (a diferencia de la media y std).
Es el criterio que usan los boxplots para los "bigotes".<br><br>
Aca usamos AMBOS: primero eliminamos errores obvios por dominio, luego aplicamos IQR.
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

<!-- PASO 5: EXPLODE -->
<div class="card">
<h3>Paso 5 — Separar lenguajes (el "explode")</h3>

<div class="concept">
<strong>Operacion one-to-many (explode):</strong> La columna <code>tools_programming_languages</code> tiene MULTIPLES lenguajes
en un solo string, separados por coma: ".NET, C#, CSS, Go, HTML, Java".<br><br>

Para analizar cada lenguaje por separado necesitamos "explotar" esa columna.
Si una persona sabe 3 lenguajes, esa fila se convierte en 3 filas, una por lenguaje.
La persona "aparece" en cada lenguaje que sabe.<br><br>

En pandas se hace con:
<ol>
<li>Convertir el string a lista (<code>.str.split(",")</code>)</li>
<li><code>.explode()</code> para que cada elemento de la lista sea su propia fila</li>
</ol>

<strong>CUIDADO:</strong> Despues del explode, la persona con 3 lenguajes esta 3 veces.
Esto NO es un error — es necesario para contar por lenguaje.
Pero significa que <strong>NO podes sumar salarios</strong> del DataFrame explotado
(contarias el salario de esa persona 3 veces).
</div>
</div>

<!-- PASO 6: FRECUENCIAS -->
<div class="card">
<h3>Paso 6 — Frecuencia de lenguajes</h3>

<div class="concept">
<strong>value_counts():</strong> Cuenta cuantas veces aparece cada valor unico.
Es la base de un analisis de frecuencias (estadistica descriptiva basica).
Nos sirve para:
<ol>
<li>Ver cuales son los lenguajes mas usados</li>
<li>Decidir cuales incluir en el analisis (los que tienen pocos datos no son confiables)</li>
</ol>

<strong>Ley de los Grandes Numeros:</strong> Cuantas mas muestras tenes, mas confiable es la estimacion.
Un lenguaje con 10 respuestas puede tener una mediana de salario altisima por pura casualidad.
Uno con 500 no.
</div>
</div>

<!-- PASO 7: SELECCION -->
<div class="card">
<h3>Paso 7 — Seleccion de lenguajes para el analisis</h3>

<div class="concept">
<strong>Umbral de 100 respuestas:</strong> Elegimos lenguajes con al menos 100 respuestas.
¿Por que 100? Es un umbral razonable para que las estadisticas sean estables.
Con menos de 100, un par de valores extremos cambian mucho la mediana.<br><br>

<strong>El balance:</strong>
<ul>
<li>Incluir muchos lenguajes → mas completo, pero algunos con pocos datos y estadisticas poco confiables</li>
<li>Incluir pocos → mas confiable, pero menos comparacion</li>
</ul>
No hay un numero magico. 100 es una convencion practica.
</div>
</div>

<!-- PASO 8: ESTADISTICA DESCRIPTIVA -->
<div class="card">
<h3>Paso 8 — Estadistica descriptiva por lenguaje</h3>

<div class="concept">
<strong>groupby():</strong> Agrupa los datos por una columna y aplica funciones.
Es como una tabla dinamica de Excel: "para cada lenguaje, calcular X".<br><br>

<strong>Metricas que calculamos:</strong>
<ul>
<li><strong>count:</strong> cuantos datos hay (tamanio de muestra)</li>
<li><strong>mean:</strong> promedio. CUIDADO: sensible a outliers.</li>
<li><strong>median:</strong> valor central. ROBUSTO contra outliers. Mejor para salarios.</li>
<li><strong>std:</strong> desviacion estandar. Mide que tan "dispersos" estan los datos.</li>
<li><strong>Q1/Q3:</strong> cuartiles. El 50% central de los datos esta entre Q1 y Q3.</li>
</ul>

<strong>¿Por que la MEDIANA es mejor que la MEDIA para salarios?</strong><br>
Porque la distribucion de salarios es ASIMETRICA (skewed right):
hay muchos salarios "normales" y pocos muy altos que inflan el promedio.<br>
Ejemplo: si 9 personas ganan $2M y una gana $20M:
<ul>
<li><strong>Media = $3.8M</strong> (inflada por el outlier)</li>
<li><strong>Mediana = $2M</strong> (refleja lo que gana la MAYORIA)</li>
</ul>
</div>
</div>

<!-- OPCION A -->
<div class="card">
<h3>Opcion A — Comparacion de distribuciones</h3>

<div class="concept">
<strong>¿Que es una distribucion?</strong> Te dice COMO se reparten los datos.
No alcanza con saber el promedio — necesitas ver la "forma":
<ul>
<li>¿Es simetrica o esta sesgada (skewed)?</li>
<li>¿Hay un pico o varios (unimodal vs multimodal)?</li>
<li>¿Los datos estan concentrados o dispersos?</li>
</ul>
</div>

<div class="concept">
<strong>1. BOXPLOT (diagrama de caja):</strong>
<ul>
<li>La <strong>CAJA</strong> va de Q1 a Q3 (el 50% central, el IQR)</li>
<li>La <strong>LINEA</strong> dentro de la caja es la mediana</li>
<li>Los <strong>BIGOTES</strong> van hasta 1.5*IQR desde la caja</li>
<li>Los <strong>PUNTOS</strong> fuera de los bigotes son outliers</li>
</ul>
Bueno para: comparar medianas y dispersiones de varios grupos rapidamente.<br>
Malo para: no muestra la FORMA de la distribucion (puede ocultar bimodalidad).
</div>

<p><strong>Boxplot:</strong> La caja muestra Q1-Q3 (50% central), la linea es la mediana, bigotes hasta 1.5*IQR.</p>
{img_to_base64("opcion_a1_boxplot.png")}

<div class="concept">
<strong>2. VIOLINPLOT:</strong>
<ul>
<li>Combina boxplot + KDE (estimacion de densidad por kernel)</li>
<li>La "forma del violin" te muestra DONDE se concentran los datos</li>
<li>Mas ancho = mas datos en ese rango de salario</li>
</ul>
Bueno para: ver la forma completa de la distribucion.<br>
Malo para: puede ser confuso si hay muchos grupos.
</div>

<p><strong>Violinplot:</strong> Combina boxplot + KDE. La forma muestra donde se concentran los datos.</p>
{img_to_base64("opcion_a2_violinplot.png")}

<div class="concept">
<strong>3. KDE (Kernel Density Estimation):</strong>
<ul>
<li>Una curva suavizada que estima la funcion de densidad de probabilidad</li>
<li>Es como un histograma "suave" y continuo</li>
<li>El area total bajo la curva siempre suma 1</li>
</ul>
Bueno para: superponer varias distribuciones y compararlas.<br>
Malo para: con muchos grupos se vuelve un quilombo visual.
Por eso elegimos los top 6 por mediana para una comparacion clara.
</div>

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

<div class="concept">
<strong>Metricas avanzadas:</strong>
<ul>
<li><strong>Percentil 90 (P90):</strong> el salario que supera el 90% de los datos.
Util para ver "el techo" de cada lenguaje.</li>
<li><strong>Coeficiente de variacion (CV):</strong> std / mean. Mide la dispersion RELATIVA.
Un CV de 0.5 significa que la std es la mitad de la media.
Permite comparar dispersiones entre lenguajes con medianas distintas.</li>
<li><strong>Skewness (asimetria):</strong> mide si la distribucion esta "cargada" a un lado.
<ul>
<li>> 0: cola a la derecha (hay salarios altos que "tiran" la media arriba)</li>
<li>= 0: simetrica</li>
<li>&lt; 0: cola a la izquierda</li>
</ul></li>
</ul>
</div>

<div class="concept">
<strong>Hallazgo creativo — "¿Quienes dominan el top 10% de salarios?"</strong><br>
Miramos el P90 global y vemos que % de cada lenguaje supera ese umbral.
Esto responde: "si agarro el 10% que MAS gana, ¿que lenguajes saben?"
</div>

<div class="concept">
<strong>Intervalo de confianza (IC) por bootstrap:</strong>
El barplot de seaborn con <code>estimator=np.median</code> y <code>errorbar=("ci", 95)</code> calcula el IC:
<ul>
<li>Toma muchas muestras aleatorias CON reemplazo</li>
<li>Calcula la mediana de cada muestra</li>
<li>El IC es el rango donde cae el 95% de esas medianas</li>
<li>Cuanto mas angosto el IC, mas "segura" es la estimacion</li>
</ul>
</div>

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

<div class="concept">
<strong>Probabilidad condicional:</strong>
P(salario > X | sabe lenguaje L) = "de los que saben L, que % gana mas que X?"<br>
Permite hacer afirmaciones como: "Si sabes Go, tenes un 45% de probabilidad de ganar mas de $3M".<br><br>

<strong>Probabilidad vs Frecuencia relativa:</strong>
En estadistica, la probabilidad se ESTIMA con la frecuencia relativa:
<code>P(evento) ≈ (veces que ocurrio) / (total de intentos)</code>.
Esto es valido por la <strong>Ley de los Grandes Numeros</strong> (con suficientes datos).<br><br>

<strong>Lift (incremento relativo):</strong>
<code>Lift = P(>X | lenguaje A) / P(>X | todos) - 1</code><br>
Un lift de +30% significa "30% mas chances que el promedio general".
</div>

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

<!-- SETUP EJ2 -->
<div class="card">
<h3>Variables seleccionadas</h3>

<div class="concept">
<strong>Variables numericas (cuantitativas):</strong> Toman valores en un rango continuo.
Se pueden sumar, promediar, correlacionar. Ejemplos: salario, edad, anios de experiencia.<br><br>

<strong>Variables categoricas (cualitativas):</strong> Toman valores discretos/etiquetas.
Se pueden contar, agrupar, comparar frecuencias. Ejemplos: genero, seniority, provincia.<br><br>

Para explorar patrones necesitamos variables de DISTINTO tipo.
</div>

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

<div class="concept">
<strong>Densidad conjunta f(x,y):</strong> Describe la distribucion de DOS o MAS variables simultaneamente.
En vez de preguntar "¿como se distribuye X?", preguntamos "¿como se distribuyen X e Y JUNTAS?"<br><br>

<strong>Independencia:</strong> Si X e Y son independientes: <code>f(x,y) = f(x) * f(y)</code>
(la densidad conjunta es el producto de las marginales).
Si NO son independientes: la densidad conjunta "deforma" respecto al producto, y eso nos dice que hay una ASOCIACION.
</div>

<div class="concept">
<strong>Herramientas visuales para densidad conjunta:</strong><br><br>

<strong>1. PAIRPLOT (matriz de dispersion):</strong>
Cruza TODAS las variables numericas entre si. La diagonal muestra la distribucion individual (histograma o KDE).
Fuera de la diagonal: scatterplots de cada par. Con <code>hue=</code> agrega una variable categorica como color.
Bueno para: vision general de relaciones entre multiples variables.
Malo para: con muchas variables se vuelve enorme e ilegible.<br><br>

<strong>2. JOINTPLOT (densidad conjunta de 2 variables):</strong>
Scatterplot central + histogramas/KDE marginales en los bordes.
Puede mostrar la densidad como "nube de calor" (<code>kind="kde"</code>): curvas de nivel donde las zonas mas cerradas = mayor concentracion.
Bueno para: explorar en detalle la relacion entre 2 variables.<br><br>

<strong>3. HEATMAP de correlacion:</strong>
Muestra la correlacion de Pearson entre cada par de variables numericas.
Rango: -1 (relacion inversa perfecta) a +1 (relacion directa perfecta). 0 = sin correlacion lineal.
Bueno para: detectar rapidamente que variables estan relacionadas.
</div>

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

<div class="concept">
<strong>Correlacion de Pearson (r):</strong>
Mide la FUERZA y DIRECCION de la relacion LINEAL entre dos variables.<br>
<code>r = cov(X,Y) / (std(X) * std(Y))</code><br>
<ul>
<li><strong>r = +1:</strong> relacion lineal perfecta positiva (si X sube, Y sube proporcionalmente)</li>
<li><strong>r = -1:</strong> relacion lineal perfecta negativa</li>
<li><strong>r = 0:</strong> sin relacion lineal (CUIDADO: puede haber relacion NO lineal)</li>
</ul>

<strong>Interpretacion practica:</strong>
<ul>
<li>|r| > 0.9: correlacion muy fuerte</li>
<li>|r| > 0.7: correlacion fuerte</li>
<li>|r| > 0.4: correlacion moderada</li>
<li>|r| &lt; 0.4: correlacion debil</li>
</ul>
</div>

<div class="concept">
<strong>R² (coeficiente de determinacion):</strong>
R² = r². Indica que % de la variabilidad de Y es explicada por X.
Si r = 0.95 → R² = 0.90 → el bruto explica el 90% de la variacion del neto.<br><br>

<strong>Correlacion de Spearman (rho):</strong>
Mide relacion MONOTONA (no necesariamente lineal). Usa rangos en vez de valores. Mas robusta contra outliers.<br><br>

<strong>p-valor:</strong>
Responde: "si NO hubiera correlacion (H0: r=0), ¿cual es la probabilidad de observar un r tan extremo por puro azar?"
Si p &lt; 0.05: rechazamos H0 → la correlacion es estadisticamente significativa.
Con 4000+ datos y r=0.95, el p-valor es esencialmente 0.<br><br>

<strong>Correlacion NO implica causalidad.</strong>
Pero aca es obvio: el neto SE CALCULA a partir del bruto (menos deducciones).
Hay una relacion CAUSAL directa. La correlacion solo cuantifica que tan "limpia" es.
</div>

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
La relacion es practicamente lineal (como se ve en el scatter).
La diferencia entre bruto y neto depende del tipo de contrato y deducciones,
pero en la MAYORIA de los casos es un porcentaje relativamente estable.
</div>
</div>

<!-- 2c -->
<div class="card">
<h3>2c) Densidad condicional — Salario segun nivel de estudio</h3>

<div class="concept">
<strong>Densidad condicional f(X | Y=y):</strong>
Es la distribucion de X dado que Y toma un valor especifico.
Ejemplo: "¿como se distribuye el salario DADO QUE la persona tiene titulo universitario?" vs "¿como se distribuye DADO QUE tiene terciario?"<br><br>

<strong>Independencia estadistica:</strong>
X e Y son independientes si: <code>f(X|Y) = f(X)</code> para todo valor de Y.
Es decir: saber el nivel de estudio no cambia la distribucion de salario.
Si son dependientes: <code>f(X|Y=universitario) != f(X|Y=secundario)</code>.
</div>

<div class="concept">
<strong>Medidas de centralidad</strong> — ¿donde esta el "centro" de los datos?
<ul>
<li><strong>Media:</strong> promedio aritmetico. Sensible a outliers.</li>
<li><strong>Mediana:</strong> valor central (50% arriba, 50% abajo). Robusta.</li>
<li><strong>Moda:</strong> valor mas frecuente. Util para categoricas, menos para continuas.</li>
</ul>

<strong>Medidas de dispersion</strong> — ¿que tan "dispersos" estan?
<ul>
<li><strong>Desviacion estandar (std):</strong> distancia promedio a la media.</li>
<li><strong>Varianza:</strong> std². Menos intuitiva pero matematicamente conveniente.</li>
<li><strong>IQR:</strong> rango intercuartilico. Robusto contra outliers.</li>
<li><strong>Rango:</strong> max - min. Muy sensible a outliers.</li>
</ul>
</div>

<div class="concept">
<strong>stat="density":</strong> Normaliza el histograma para que el area total sea 1.
Esto permite comparar distribuciones con diferente cantidad de datos.
Sin normalizar, el grupo mas grande siempre "tapa" al otro.
</div>

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

<div class="concept">
<strong>Test de Mann-Whitney U:</strong>
Compara si dos muestras vienen de la misma distribucion. Es la version NO PARAMETRICA del t-test.
No asume normalidad (y los salarios NO son normales).
<ul>
<li><strong>H0:</strong> las dos distribuciones son iguales (independencia)</li>
<li><strong>H1:</strong> son diferentes (dependencia)</li>
</ul>
</div>

<div class="highlight">
<strong>Test Mann-Whitney U:</strong> p = 2.78e-11<br>
Rechazamos H0: las distribuciones son <strong>diferentes</strong>. El salario y el nivel de estudio <strong>NO son independientes</strong>.
Los universitarios ganan una mediana 36% mas alta que los terciarios.
</div>
</div>

<!-- 2d -->
<div class="card">
<h3>2d) Densidad conjunta condicional</h3>

<div class="concept">
<strong>Densidad conjunta condicional f(X, Y | Z=z):</strong>
Es la distribucion conjunta de dos variables numericas, CONDICIONADA a una variable categorica.<br><br>

Visualmente: un scatterplot de X vs Y donde el COLOR indica Z.
Si los colores forman "nubes" separadas, hay dependencia entre (X,Y) y Z.
Si los colores se mezclan uniformemente, Z no afecta la relacion X-Y.<br><br>

<strong>hue en seaborn:</strong>
El parametro <code>hue=</code> mapea una variable categorica al color de los puntos.
Es una de las formas mas poderosas de agregar una TERCERA dimension
a un grafico 2D sin recurrir a 3D (que suele ser confuso).
</div>

<div class="concept">
<strong>lmplot = scatterplot + regresion lineal, separado por hue.</strong>
Cada grupo tiene su propia recta de ajuste, lo que permite ver
si la PENDIENTE de la relacion edad-salario es distinta por seniority.
</div>

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
<br>Reporte completo: incluye resultados + explicaciones conceptuales.
</p>

</div>
</body>
</html>"""

Path(OUTPUT).write_text(html, encoding="utf-8")
print(f"Reporte generado: {OUTPUT}")
print(f"Tamanio: {Path(OUTPUT).stat().st_size / 1024:.0f} KB")
print(f"Abrir con: xdg-open {OUTPUT}")
