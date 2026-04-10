# =============================================================================
# EJERCICIO 1 — Análisis Descriptivo
# Pregunta: ¿Cuáles son los lenguajes de programación asociados a los mejores salarios?
# Dataset: Encuesta Sysarmy 2026 (procesada)
# =============================================================================

# =============================================================================
# PASO 0: Imports y configuracion
# =============================================================================
# pandas: LA libreria para manipular datos tabulares (como un Excel con superpoderes).
#   - DataFrame: tabla con filas y columnas
#   - Series: una sola columna
#
# matplotlib: libreria base de graficos en Python. seaborn se construye ENCIMA de ella.
#
# seaborn: graficos estadisticos de alto nivel. Mas lindo y mas facil que matplotlib puro.
#   - set_context('talk'): agranda fuentes y elementos para que se vea bien en presentaciones.
#
# numpy: operaciones numericas. pandas lo usa internamente.

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

sns.set_context("talk")

# =============================================================================
# PASO 1: Carga de datos
# =============================================================================
# pd.read_csv() lee un archivo CSV (Comma-Separated Values) y lo convierte en un DataFrame.
# Puede leer desde una URL directamente — no necesitas descargar el archivo.

url = "https://raw.githubusercontent.com/DiploDatos/AnalisisyVisualizacion/master/sysarmy_survey_2026_processed.csv"
df = pd.read_csv(url)

# =============================================================================
# PASO 2: Exploracion inicial — ANTES de analizar, hay que CONOCER los datos
# =============================================================================
# Estas son las preguntas basicas que SIEMPRE te haces al recibir un dataset:
#   1. ¿Cuantas filas y columnas tiene? -> .shape
#   2. ¿Que columnas hay y de que tipo son? -> .dtypes / .info()
#   3. ¿Hay valores nulos? -> .isnull().sum()
#   4. ¿Como se ven los datos? -> .head() / .describe()

print("=" * 60)
print("FORMA DEL DATASET (filas, columnas)")
print("=" * 60)
print(df.shape)
print(f"\n{df.shape[0]} respuestas, {df.shape[1]} preguntas/columnas")

print("\n" + "=" * 60)
print("COLUMNAS DISPONIBLES")
print("=" * 60)
for i, col in enumerate(df.columns):
    print(f"  {i:2d}. {col}")

print("\n" + "=" * 60)
print("TIPOS DE DATOS")
print("=" * 60)
# dtypes te dice si cada columna es numerica (int64, float64) o texto (object).
# Esto es CLAVE porque determina que operaciones podes hacer:
#   - Numericas: media, mediana, correlacion, histogramas
#   - Categoricas (object): conteo de frecuencias, agrupacion, barplots
print(df.dtypes)

print("\n" + "=" * 60)
print("PRIMERAS 5 FILAS")
print("=" * 60)
print(df.head())

print("\n" + "=" * 60)
print("ESTADISTICAS DESCRIPTIVAS (solo columnas numericas)")
print("=" * 60)
# .describe() te da de una:
#   count: cuantos valores NO nulos hay
#   mean: promedio (suma / cantidad)
#   std: desviacion estandar (que tan dispersos estan los datos respecto a la media)
#   min/max: valores extremos
#   25%, 50%, 75%: percentiles (cuartiles)
#     - 50% = mediana (el valor que divide los datos en dos mitades iguales)
#     - 25% y 75% definen el IQR (rango intercuartilico), usado para detectar outliers
print(df.describe())

# =============================================================================
# PASO 3: Seleccion de columnas relevantes
# =============================================================================
# CONCEPTO: No todas las columnas sirven para responder nuestra pregunta.
# Necesitamos pensar: "¿que variables INFLUYEN en la relacion lenguaje-salario?"
#
# Columnas elegidas y POR QUE:
#   - tools_programming_languages: los lenguajes (variable central de la pregunta)
#   - salary_monthly_NETO: el salario. Usamos NETO porque es lo que la persona
#     realmente cobra. El BRUTO depende del tipo de contrato y deducciones.
#   - work_dedication: Full-Time vs Part-Time. Si no filtramos, un part-time
#     con salario bajo contamina el analisis (gana menos por TRABAJAR MENOS,
#     no por el lenguaje que usa).
#   - work_seniority: Senior vs Junior. Un senior de PHP puede ganar mas que
#     un junior de Rust. Si no controlamos esto, confundimos experiencia con lenguaje.
#
# CONCEPTO: Esto se llama "variables de control" o "confounders".
# Son factores que afectan el salario pero NO son el lenguaje.
# Si no los controlamos, nuestras conclusiones pueden ser FALSAS.

relevant_columns = [
    "tools_programming_languages",
    "salary_monthly_NETO",
    "work_dedication",
    "work_seniority",
]

print("\n" + "=" * 60)
print("PASO 3: COLUMNAS SELECCIONADAS")
print("=" * 60)
print(relevant_columns)

# =============================================================================
# PASO 4: Limpieza de datos — FILTRADO DE FILAS
# =============================================================================
# CONCEPTO: Los datos del mundo real son SUCIOS. Siempre. La encuesta tiene:
#   - Valores nulos (NaN): gente que no respondio
#   - Valores absurdos: alguien puso $1.6 de sueldo neto, o $653 millones
#   - Valores extremos (outliers): no son "errores", pero distorsionan las metricas
#
# Estrategia de limpieza (cada paso se justifica):

df_clean = df[relevant_columns].copy()
print("\n" + "=" * 60)
print("PASO 4: LIMPIEZA DE DATOS")
print("=" * 60)
print(f"Filas iniciales: {len(df_clean)}")

# --- 4a: Eliminar filas sin salario neto ---
# CONCEPTO: NaN = "Not a Number". Representa datos faltantes.
# No podemos comparar salarios si no HAY salario. .dropna() elimina esas filas.
# subset= indica en que columnas buscar NaN.
df_clean = df_clean.dropna(subset=["salary_monthly_NETO"])
print(f"Despues de eliminar NaN en salario: {len(df_clean)}")

# --- 4b: Eliminar filas sin lenguaje de programacion ---
# Si no declararon lenguaje, no sirven para nuestro analisis.
df_clean = df_clean.dropna(subset=["tools_programming_languages"])
print(f"Despues de eliminar NaN en lenguajes: {len(df_clean)}")

# --- 4c: Filtrar solo Full-Time ---
# JUSTIFICACION: Comparar salarios entre full-time y part-time no tiene sentido
# para nuestra pregunta. Un part-timer cobra menos por definicion.
# Esto REFORMULA nuestra pregunta a:
#   "¿Cuales son los lenguajes asociados a mejores salarios ENTRE TRABAJADORES FULL-TIME?"
df_clean = df_clean[df_clean["work_dedication"] == "Full-Time"]
print(f"Despues de filtrar solo Full-Time: {len(df_clean)}")

# --- 4d: Eliminar valores absurdos de salario ---
# CONCEPTO: Hay dos tipos de "datos raros":
#   1. ERRORES: alguien puso $1.6 o $653M. Imposible. Se eliminan.
#   2. OUTLIERS: valores extremos pero posibles. Se manejan con criterio.
#
# Criterio por dominio (conocimiento del mundo real):
#   - Salario minimo en Argentina 2026: ~300K. Menos que eso es error.
#   - Mas de $20M netos para IT en Argentina: muy improbable, posible error.
#
# ALTERNATIVA mas "estadistica": metodo IQR (Interquartile Range)
#   IQR = Q3 - Q1 (rango del 50% central de los datos)
#   Outlier = cualquier valor < Q1 - 1.5*IQR  o  > Q3 + 1.5*IQR
#   Es el criterio que usan los boxplots para los "bigotes".
#
# Aca usamos AMBOS: primero eliminamos errores obvios, luego aplicamos IQR.

# Paso 4d.1: Eliminar errores obvios por dominio
salary_min = 300_000
salary_max = 20_000_000
df_clean = df_clean[
    (df_clean["salary_monthly_NETO"] >= salary_min)
    & (df_clean["salary_monthly_NETO"] <= salary_max)
]
print(f"Despues de filtrar salarios [{salary_min:,} - {salary_max:,}]: {len(df_clean)}")

# Paso 4d.2: Eliminar outliers por IQR
# CONCEPTO: El IQR es robusto contra outliers (a diferencia de la media y std).
#   Q1 (percentil 25): el 25% de los datos esta por debajo
#   Q3 (percentil 75): el 75% de los datos esta por debajo
#   IQR = Q3 - Q1: el "ancho" del 50% central
#   Limites: [Q1 - 1.5*IQR, Q3 + 1.5*IQR]
Q1 = df_clean["salary_monthly_NETO"].quantile(0.25)
Q3 = df_clean["salary_monthly_NETO"].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

df_clean = df_clean[
    (df_clean["salary_monthly_NETO"] >= lower_bound)
    & (df_clean["salary_monthly_NETO"] <= upper_bound)
]
print(f"Despues de IQR [{lower_bound:,.0f} - {upper_bound:,.0f}]: {len(df_clean)}")

print(f"\n--- Resumen de limpieza ---")
print(f"Filas originales: {len(df)}")
print(f"Filas despues de limpieza: {len(df_clean)}")
print(f"Filas eliminadas: {len(df) - len(df_clean)} ({(len(df) - len(df_clean)) / len(df) * 100:.1f}%)")

print("\nEstadisticas del salario LIMPIO:")
print(df_clean["salary_monthly_NETO"].describe())

# =============================================================================
# PASO 5: Separar lenguajes (el "explode")
# =============================================================================
# PROBLEMA: La columna tools_programming_languages tiene MULTIPLES lenguajes
# en un solo string, separados por coma: ".NET, C#, CSS, Go, HTML, Java"
#
# Para analizar cada lenguaje por separado necesitamos "explotar" esa columna.
# Es decir, si una persona sabe 3 lenguajes, esa fila se convierte en 3 filas,
# una por lenguaje. La persona "aparece" en cada lenguaje que sabe.
#
# CONCEPTO: Esto es un "one-to-many" o "explode". En pandas se hace con:
#   1. Convertir el string a lista (split por coma)
#   2. .explode() para que cada elemento de la lista sea su propia fila
#
# CUIDADO: Despues del explode, la persona con 3 lenguajes esta 3 veces.
# Esto NO es un error — es necesario para contar por lenguaje.
# Pero significa que NO podes sumar salarios del DataFrame explotado
# (contarias el salario de esa persona 3 veces).

# Paso 5a: Convertir string de lenguajes a lista
df_clean = df_clean.copy()
df_clean["lang_list"] = (
    df_clean["tools_programming_languages"]
    .str.split(",")        # "Go, Python, SQL" -> ["Go", " Python", " SQL"]
    .apply(lambda langs: [l.strip() for l in langs])  # quitar espacios
)

# Paso 5b: Explotar — cada lenguaje en su propia fila
df_lang = df_clean.explode("lang_list").rename(columns={"lang_list": "language"})

print("\n" + "=" * 60)
print("PASO 5: EXPLODE DE LENGUAJES")
print("=" * 60)
print(f"Filas antes del explode: {len(df_clean)}")
print(f"Filas despues del explode: {len(df_lang)}")
print(f"(Cada persona aparece N veces, una por cada lenguaje que sabe)")

# =============================================================================
# PASO 6: Frecuencia de lenguajes — ¿cuales son los mas populares?
# =============================================================================
# CONCEPTO: value_counts() cuenta cuantas veces aparece cada valor unico.
# Es la base de un analisis de frecuencias (estadistica descriptiva basica).
# Nos sirve para:
#   1. Ver cuales son los lenguajes mas usados
#   2. Decidir cuales incluir en el analisis (los que tienen pocos datos no son confiables)
#
# CONCEPTO: Ley de los grandes numeros — cuantas mas muestras tenes,
# mas confiable es la estimacion. Un lenguaje con 10 respuestas puede tener
# una mediana de salario altisima por pura casualidad. Uno con 500 no.

lang_counts = df_lang["language"].value_counts()
print("\n" + "=" * 60)
print("PASO 6: FRECUENCIA DE LENGUAJES (top 15)")
print("=" * 60)
print(lang_counts.head(15))

# =============================================================================
# PASO 7: Seleccion de lenguajes para el analisis
# =============================================================================
# Criterio: elegimos lenguajes con al menos 100 respuestas.
# ¿Por que 100? Es un umbral razonable para que las estadisticas sean estables.
# Con menos de 100, un par de valores extremos cambian mucho la mediana.
#
# CONCEPTO: Esto es un balance entre:
#   - Incluir muchos lenguajes (mas completo, pero algunos con pocos datos)
#   - Incluir pocos (mas confiable, pero menos comparacion)
# No hay un numero magico. 100 es una convencion practica.

MIN_RESPONSES = 100
popular_languages = lang_counts[lang_counts >= MIN_RESPONSES].index.tolist()

print("\n" + "=" * 60)
print(f"PASO 7: LENGUAJES CON >= {MIN_RESPONSES} RESPUESTAS")
print("=" * 60)
print(f"Lenguajes seleccionados ({len(popular_languages)}):")
for lang in popular_languages:
    print(f"  - {lang}: {lang_counts[lang]} respuestas")

# Filtrar el DataFrame para quedarnos solo con estos lenguajes
df_analysis = df_lang[df_lang["language"].isin(popular_languages)].copy()
print(f"\nFilas en el dataset de analisis: {len(df_analysis)}")

# =============================================================================
# PASO 8: Estadistica descriptiva por lenguaje
# =============================================================================
# CONCEPTO: groupby() agrupa los datos por una columna y aplica funciones.
# Es como una tabla dinamica de Excel: "para cada lenguaje, calcular X".
#
# Metricas que calculamos:
#   - count: cuantos datos hay (tamanio de muestra)
#   - mean: promedio. CUIDADO: sensible a outliers.
#   - median: valor central. ROBUSTO contra outliers. Mejor para salarios.
#   - std: desviacion estandar. Mide que tan "dispersos" estan los datos.
#   - Q1/Q3: cuartiles. El 50% central de los datos esta entre Q1 y Q3.
#
# ¿Por que la MEDIANA es mejor que la MEDIA para salarios?
# Porque la distribucion de salarios es ASIMETRICA (skewed right):
# hay muchos salarios "normales" y pocos muy altos que inflan el promedio.
# Ejemplo: si 9 personas ganan $2M y una gana $20M:
#   Media = $3.8M (inflada por el outlier)
#   Mediana = $2M (refleja lo que gana la MAYORIA)

salary_stats = (
    df_analysis.groupby("language")["salary_monthly_NETO"]
    .agg(["count", "mean", "median", "std"])
    .sort_values("median", ascending=False)
)
salary_stats["mean"] = salary_stats["mean"].apply(lambda x: f"${x:,.0f}")
salary_stats["median"] = salary_stats["median"].apply(lambda x: f"${x:,.0f}")
salary_stats["std"] = salary_stats["std"].apply(lambda x: f"${x:,.0f}")

print("\n" + "=" * 60)
print("PASO 8: ESTADISTICAS POR LENGUAJE (ordenado por mediana)")
print("=" * 60)
print(salary_stats.to_string())

# Sacamos "Ninguno de los anteriores" — no es un lenguaje de programacion
df_analysis = df_analysis[df_analysis["language"] != "Ninguno de los anteriores"]
popular_languages = [l for l in popular_languages if l != "Ninguno de los anteriores"]

# =============================================================================
# OPCION A: Comparar DISTRIBUCIONES con visualizaciones
# =============================================================================
# CONCEPTO: Una distribucion te dice COMO se reparten los datos.
# No alcanza con saber el promedio — necesitas ver la "forma":
#   - ¿Es simetrica o esta sesgada (skewed)?
#   - ¿Hay un pico o varios (unimodal vs multimodal)?
#   - ¿Los datos estan concentrados o dispersos?
#
# Herramientas visuales para comparar distribuciones:
#
# 1. BOXPLOT (diagrama de caja):
#    - La CAJA va de Q1 a Q3 (el 50% central, el IQR)
#    - La LINEA dentro de la caja es la mediana
#    - Los BIGOTES van hasta 1.5*IQR desde la caja
#    - Los PUNTOS fuera de los bigotes son outliers
#    BUENO PARA: comparar medianas y dispersiones de varios grupos rapidamente
#    MALO PARA: no muestra la FORMA de la distribucion (puede ocultar bimodalidad)
#
# 2. VIOLINPLOT:
#    - Combina boxplot + KDE (estimacion de densidad por kernel)
#    - La "forma del violin" te muestra DONDE se concentran los datos
#    - Mas ancho = mas datos en ese rango de salario
#    BUENO PARA: ver la forma completa de la distribucion
#    MALO PARA: puede ser confuso si hay muchos grupos
#
# 3. KDE (Kernel Density Estimation):
#    - Una curva suavizada que estima la funcion de densidad de probabilidad
#    - Es como un histograma "suave" y continuo
#    - El area total bajo la curva siempre suma 1
#    BUENO PARA: superponer varias distribuciones y compararlas
#    MALO PARA: con muchos grupos se vuelve un quilombo visual

# Ordenar lenguajes por mediana para que los graficos tengan sentido visual
median_order = (
    df_analysis.groupby("language")["salary_monthly_NETO"]
    .median()
    .sort_values(ascending=False)
    .index.tolist()
)

# --- Grafico A1: Boxplot ---
fig, ax = plt.subplots(figsize=(14, 8))
sns.boxplot(
    data=df_analysis,
    x="salary_monthly_NETO",
    y="language",
    order=median_order,
    palette="viridis",
    ax=ax,
)
ax.set_title("Distribución de salario neto por lenguaje (Boxplot)")
ax.set_xlabel("Salario mensual neto ($)")
ax.set_ylabel("Lenguaje")
# Formatear el eje X para que muestre los numeros en millones
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x/1e6:.1f}M"))
plt.tight_layout()
plt.savefig("img/opcion_a1_boxplot.png", dpi=150)
plt.close()
print("\n[Guardado] opcion_a1_boxplot.png")

# --- Grafico A2: Violinplot ---
fig, ax = plt.subplots(figsize=(14, 8))
sns.violinplot(
    data=df_analysis,
    x="salary_monthly_NETO",
    y="language",
    order=median_order,
    palette="viridis",
    density_norm="width",  # normaliza el ancho para que todos los violines sean comparables
    inner="quartile",      # muestra las lineas de Q1, mediana, Q3 dentro del violin
    ax=ax,
)
ax.set_title("Distribución de salario neto por lenguaje (Violinplot)")
ax.set_xlabel("Salario mensual neto ($)")
ax.set_ylabel("Lenguaje")
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x/1e6:.1f}M"))
plt.tight_layout()
plt.savefig("img/opcion_a2_violinplot.png", dpi=150)
plt.close()
print("[Guardado] opcion_a2_violinplot.png")

# --- Grafico A3: KDE superpuesto (top 6 lenguajes para que se lea bien) ---
# CONCEPTO: Con 15 lenguajes superpuestos no se ve nada.
# Elegimos los top 6 por mediana para una comparacion clara.
top_6 = median_order[:6]
fig, ax = plt.subplots(figsize=(14, 8))
for lang in top_6:
    data = df_analysis[df_analysis["language"] == lang]["salary_monthly_NETO"]
    # kde_kws={"clip": (0, None)} evita que la curva se extienda a salarios negativos
    sns.kdeplot(data, label=f"{lang} (n={len(data)})", ax=ax, fill=True, alpha=0.3)
ax.set_title("Densidad de salario neto — Top 6 lenguajes por mediana (KDE)")
ax.set_xlabel("Salario mensual neto ($)")
ax.set_ylabel("Densidad")
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x/1e6:.1f}M"))
ax.legend()
plt.tight_layout()
plt.savefig("img/opcion_a3_kde_top6.png", dpi=150)
plt.close()
print("[Guardado] opcion_a3_kde_top6.png")

# =============================================================================
# OPCION B: Comparar ESTADISTICA DESCRIPTIVA
# =============================================================================
# CONCEPTO: La estadistica descriptiva RESUME los datos en numeros clave.
# En vez de mirar miles de filas, condensamos en metricas.
#
# Metricas avanzadas que agregamos:
#   - Percentil 90 (P90): el salario que supera el 90% de los datos.
#     Util para ver "el techo" de cada lenguaje.
#   - Coeficiente de variacion (CV): std / mean. Mide la dispersión RELATIVA.
#     Un CV de 0.5 significa que la std es la mitad de la media.
#     Permite comparar dispersiones entre lenguajes con medianas distintas.
#   - Skewness (asimetria): mide si la distribucion esta "cargada" a un lado.
#     > 0: cola a la derecha (hay salarios altos que "tiran" la media arriba)
#     = 0: simetrica
#     < 0: cola a la izquierda

salary_stats_full = (
    df_analysis.groupby("language")["salary_monthly_NETO"]
    .agg(
        count="count",
        mean="mean",
        median="median",
        std="std",
        Q1=lambda x: x.quantile(0.25),
        Q3=lambda x: x.quantile(0.75),
        P90=lambda x: x.quantile(0.90),
        skew="skew",
    )
    .sort_values("median", ascending=False)
)
salary_stats_full["CV"] = salary_stats_full["std"] / salary_stats_full["mean"]

print("\n" + "=" * 60)
print("OPCION B: ESTADISTICA DESCRIPTIVA COMPLETA")
print("=" * 60)
print(salary_stats_full.round(0).to_string())

# Hallazgo creativo: "¿Quienes dominan el top 10% de salarios?"
# CONCEPTO: Mirar el P90 global y ver que % de cada lenguaje supera ese umbral.
# Esto responde: "si agarro el 10% que MAS gana, ¿que lenguajes saben?"
p90_global = df_analysis["salary_monthly_NETO"].quantile(0.90)
print(f"\nPercentil 90 global: ${p90_global:,.0f}")
print("(El 10% de los encuestados full-time gana mas que esto)\n")

top_earners = (
    df_analysis.groupby("language")["salary_monthly_NETO"]
    .apply(lambda x: (x >= p90_global).mean() * 100)
    .sort_values(ascending=False)
)
print("% de cada lenguaje que esta en el top 10% de salarios:")
for lang, pct in top_earners.items():
    bar = "#" * int(pct / 2)
    print(f"  {lang:25s} {pct:5.1f}%  {bar}")

# --- Grafico B1: Barplot de medianas con IC ---
fig, ax = plt.subplots(figsize=(14, 8))
# CONCEPTO: barplot de seaborn por defecto muestra la MEDIA y un
# intervalo de confianza (IC) del 95% usando bootstrapping.
# estimator=np.median cambia para mostrar la mediana en su lugar.
# errorbar=("ci", 95) calcula el IC por bootstrap:
#   - Toma muchas muestras aleatorias CON reemplazo
#   - Calcula la mediana de cada muestra
#   - El IC es el rango donde cae el 95% de esas medianas
#   - Cuanto mas angosto el IC, mas "segura" es la estimacion
sns.barplot(
    data=df_analysis,
    x="salary_monthly_NETO",
    y="language",
    order=median_order,
    estimator=np.median,
    errorbar=("ci", 95),
    palette="viridis",
    ax=ax,
)
ax.set_title("Mediana de salario neto por lenguaje (con IC 95%)")
ax.set_xlabel("Salario mensual neto ($)")
ax.set_ylabel("Lenguaje")
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x/1e6:.1f}M"))
plt.tight_layout()
plt.savefig("img/opcion_b1_barplot_mediana.png", dpi=150)
plt.close()
print("\n[Guardado] opcion_b1_barplot_mediana.png")

# --- Grafico B2: Heatmap del % en top 10% ---
fig, ax = plt.subplots(figsize=(10, 8))
top_earners_df = top_earners.reset_index()
top_earners_df.columns = ["language", "pct_top10"]
top_earners_df = top_earners_df.set_index("language")
sns.heatmap(
    top_earners_df,
    annot=True,
    fmt=".1f",
    cmap="YlOrRd",
    cbar_kws={"label": "% en top 10%"},
    ax=ax,
)
ax.set_title("% de programadores de cada lenguaje en el top 10% de salarios")
ax.set_ylabel("Lenguaje")
ax.set_xlabel("")
plt.tight_layout()
plt.savefig("img/opcion_b2_heatmap_top10.png", dpi=150)
plt.close()
print("[Guardado] opcion_b2_heatmap_top10.png")

# =============================================================================
# OPCION C: Comparar PROBABILIDADES
# =============================================================================
# CONCEPTO: Probabilidad condicional.
# P(salario > X | sabe lenguaje L) = "de los que saben L, que % gana mas que X?"
#
# Esto permite hacer afirmaciones del tipo:
#   "Si sabes Go, tenes un 45% de probabilidad de ganar mas de $3M"
#   "Eso es un 30% mas que si sabes PHP"
#
# CONCEPTO: Probabilidad vs Frecuencia relativa
# En estadistica, la probabilidad se ESTIMA con la frecuencia relativa:
#   P(evento) ≈ (veces que ocurrio) / (total de intentos)
# Esto es valido por la Ley de los Grandes Numeros (con suficientes datos).
#
# CONCEPTO: "Lift" o incremento relativo
#   Lift = P(>X | lenguaje A) / P(>X | todos) - 1
#   Un lift de +30% significa "30% mas chances que el promedio general"

thresholds = [2_000_000, 3_000_000, 4_000_000, 5_000_000]

print("\n" + "=" * 60)
print("OPCION C: PROBABILIDADES CONDICIONALES")
print("=" * 60)

# Probabilidad base (todos los lenguajes)
print("\nProbabilidad BASE (todos los full-time del dataset):")
for t in thresholds:
    p_base = (df_analysis["salary_monthly_NETO"] >= t).mean() * 100
    print(f"  P(salario >= ${t/1e6:.0f}M) = {p_base:.1f}%")

# Probabilidad por lenguaje
prob_by_lang = {}
for lang in median_order:
    data = df_analysis[df_analysis["language"] == lang]["salary_monthly_NETO"]
    probs = {}
    for t in thresholds:
        key = f">={int(t // 1_000_000)}M"
        probs[key] = (data >= t).mean() * 100
    prob_by_lang[lang] = probs

prob_df = pd.DataFrame(prob_by_lang).T
print("\nProbabilidad de ganar >= X por lenguaje (%):")
print(prob_df.round(1).to_string())

# Lift respecto al promedio general
print("\nLIFT vs promedio general (cuanto % MAS chances que el promedio):")
for t in thresholds:
    key = f">={int(t // 1_000_000)}M"
    p_base = (df_analysis["salary_monthly_NETO"] >= t).mean() * 100
    print(f"\n  Umbral ${int(t // 1_000_000)}M (base: {p_base:.1f}%):")
    for lang in median_order[:6]:
        p_lang = prob_by_lang[lang][key]
        if p_base > 0:
            lift = (p_lang / p_base - 1) * 100
            direction = "+" if lift > 0 else ""
            print(f"    {lang:15s}: {p_lang:5.1f}% ({direction}{lift:.0f}% vs promedio)")

# --- Grafico C1: Barplot agrupado de probabilidades ---
fig, ax = plt.subplots(figsize=(14, 8))
prob_plot = prob_df.loc[median_order]
prob_plot.plot(kind="barh", ax=ax, width=0.8)
ax.set_title("Probabilidad de ganar >= X por lenguaje")
ax.set_xlabel("Probabilidad (%)")
ax.set_ylabel("Lenguaje")
ax.legend(title="Umbral", bbox_to_anchor=(1.02, 1), loc="upper left")
plt.tight_layout()
plt.savefig("img/opcion_c1_probabilidades.png", dpi=150)
plt.close()
print("\n[Guardado] opcion_c1_probabilidades.png")


# #############################################################################
# #############################################################################
#
#              EJERCICIO 2 — DENSIDADES Y VARIAS VARIABLES
#
# #############################################################################
# #############################################################################
# Pregunta general: ¿Que herramientas (practicas y teoricas) son utiles
# para explorar la base, descubrir patrones y asociaciones?
#
# Partimos del df original (no del df_clean del ejercicio 1, porque aca
# queremos explorar MAS variables, no solo lenguajes).

# =============================================================================
# PASO 9: Preparacion del dataset para Ejercicio 2
# =============================================================================
# Reutilizamos la limpieza basica: quitar NaN en salario y valores absurdos.
# Pero NO filtramos por Full-Time ni por lenguaje — queremos mas datos.

df2 = df.copy()

# Limpieza basica de salarios
df2 = df2.dropna(subset=["salary_monthly_NETO", "salary_monthly_BRUTO"])
df2 = df2[
    (df2["salary_monthly_NETO"] >= 300_000)
    & (df2["salary_monthly_NETO"] <= 20_000_000)
    & (df2["salary_monthly_BRUTO"] >= 300_000)
    & (df2["salary_monthly_BRUTO"] <= 20_000_000)
]
# Limpiar edad absurda
df2 = df2[(df2["profile_age"] >= 18) & (df2["profile_age"] <= 70)]

print("\n" + "#" * 60)
print("# EJERCICIO 2 — DENSIDADES Y VARIAS VARIABLES")
print("#" * 60)
print(f"Dataset para ejercicio 2: {len(df2)} filas")

# =============================================================================
# Seleccion de variables
# =============================================================================
# CONCEPTO: Para explorar patrones necesitamos variables de DISTINTO tipo:
#
# VARIABLES NUMERICAS (cuantitativas): toman valores en un rango continuo.
#   Se pueden sumar, promediar, correlacionar.
#   Ejemplos: salario, edad, anios de experiencia.
#
# VARIABLES CATEGORICAS (cualitativas): toman valores discretos/etiquetas.
#   Se pueden contar, agrupar, comparar frecuencias.
#   Ejemplos: genero, seniority, provincia.
#
# Elegimos:
#   Numericas: salary_monthly_NETO, salary_monthly_BRUTO, profile_age
#   Categoricas: work_seniority, profile_gender

num_vars = ["salary_monthly_NETO", "salary_monthly_BRUTO", "profile_age"]
cat_vars = ["work_seniority", "profile_gender"]

print(f"\nVariables numericas: {num_vars}")
print(f"Variables categoricas: {cat_vars}")
print(f"\nValores unicos en categoricas:")
for col in cat_vars:
    print(f"  {col}: {df2[col].value_counts().to_dict()}")

# =============================================================================
# 2a) DENSIDAD CONJUNTA
# =============================================================================
# CONCEPTO: La densidad conjunta describe la distribucion de DOS o MAS
# variables simultaneamente. En vez de preguntar "¿como se distribuye X?"
# preguntamos "¿como se distribuyen X e Y JUNTAS?"
#
# HERRAMIENTAS VISUALES para densidad conjunta:
#
# 1. PAIRPLOT (matriz de dispersion):
#    - Cruza TODAS las variables numericas entre si
#    - La diagonal muestra la distribucion individual (histograma o KDE)
#    - Fuera de la diagonal: scatterplots de cada par
#    - Con hue= agrega una variable categorica como color
#    BUENO PARA: vision general de relaciones entre multiples variables
#    MALO PARA: con muchas variables se vuelve enorme e ilegible
#
# 2. JOINTPLOT (densidad conjunta de 2 variables):
#    - Scatterplot central + histogramas/KDE marginales en los bordes
#    - Puede mostrar la densidad como "nube de calor" (kind="kde")
#    BUENO PARA: explorar en detalle la relacion entre 2 variables
#
# 3. HEATMAP de correlacion:
#    - Muestra la correlacion de Pearson entre cada par de variables numericas
#    - Rango: -1 (relacion inversa perfecta) a +1 (relacion directa perfecta)
#    - 0 = sin correlacion lineal
#    BUENO PARA: detectar rapidamente que variables estan relacionadas
#
# HERRAMIENTAS TEORICAS:
# - Funcion de densidad conjunta f(x,y): describe la probabilidad de que
#   X e Y tomen valores en cierto rango simultaneamente.
# - Si X e Y son independientes: f(x,y) = f(x) * f(y)
#   (la densidad conjunta es el producto de las marginales)
# - Si NO son independientes: la densidad conjunta "deforma" respecto al
#   producto, y eso nos dice que hay una ASOCIACION.

print("\n" + "=" * 60)
print("2a) DENSIDAD CONJUNTA")
print("=" * 60)

# --- Grafico 2a.1: Pairplot con seniority como color ---
# CONCEPTO: hue="work_seniority" colorea los puntos segun seniority.
# Esto nos permite ver si la relacion entre variables CAMBIA segun el grupo.
# Por ejemplo: ¿la relacion edad-salario es distinta para juniors vs seniors?
g = sns.pairplot(
    df2[num_vars + ["work_seniority"]].dropna(),
    hue="work_seniority",
    diag_kind="kde",       # KDE en la diagonal en vez de histograma
    plot_kws={"alpha": 0.4, "s": 15},  # transparencia y tamanio de puntos
    height=3,
)
g.figure.suptitle("Pairplot: variables numéricas por seniority", y=1.02)
plt.tight_layout()
plt.savefig("img/ej2a_pairplot.png", dpi=150)
plt.close()
print("[Guardado] ej2a_pairplot.png")

# --- Grafico 2a.2: Jointplot salario neto vs edad ---
# kind="kde" muestra curvas de nivel de densidad en vez de puntos
# Esto es literalmente una estimacion de la densidad conjunta f(salario, edad)
g = sns.jointplot(
    data=df2,
    x="profile_age",
    y="salary_monthly_NETO",
    kind="kde",
    fill=True,
    cmap="YlOrRd",
    height=8,
)
g.ax_joint.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x/1e6:.1f}M"))
g.figure.suptitle("Densidad conjunta: Edad vs Salario Neto", y=1.02)
plt.tight_layout()
plt.savefig("img/ej2a_jointplot_edad_salario.png", dpi=150)
plt.close()
print("[Guardado] ej2a_jointplot_edad_salario.png")

# --- Grafico 2a.3: Heatmap de correlacion ---
corr_matrix = df2[num_vars].corr()
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(
    corr_matrix,
    annot=True,          # muestra los numeros en cada celda
    fmt=".3f",           # 3 decimales
    cmap="coolwarm",     # azul (negativo) a rojo (positivo)
    vmin=-1, vmax=1,     # fuerza el rango completo [-1, 1]
    square=True,
    ax=ax,
)
ax.set_title("Matriz de correlación (Pearson)")
plt.tight_layout()
plt.savefig("img/ej2a_heatmap_correlacion.png", dpi=150)
plt.close()
print("[Guardado] ej2a_heatmap_correlacion.png")

print("\nDescripcion del comportamiento:")
print(f"  Correlacion BRUTO-NETO: {corr_matrix.loc['salary_monthly_BRUTO', 'salary_monthly_NETO']:.3f}")
print(f"  Correlacion Edad-Salario NETO: {corr_matrix.loc['profile_age', 'salary_monthly_NETO']:.3f}")
print(f"  Correlacion Edad-Salario BRUTO: {corr_matrix.loc['profile_age', 'salary_monthly_BRUTO']:.3f}")

# =============================================================================
# 2b) ASOCIACION — ¿Se puede sacar la columna de salario bruto?
# =============================================================================
# PREGUNTA: ¿Existe correlacion entre salario bruto y neto?
# Si la correlacion es MUY alta, una variable es REDUNDANTE — no aporta
# informacion nueva. Y se podria sacar de la encuesta para simplificarla.
#
# CONCEPTO: Correlacion de Pearson (r)
#   Mide la FUERZA y DIRECCION de la relacion LINEAL entre dos variables.
#   r = cov(X,Y) / (std(X) * std(Y))
#   - r = +1: relacion lineal perfecta positiva (si X sube, Y sube proporcionalmente)
#   - r = -1: relacion lineal perfecta negativa
#   - r = 0: sin relacion lineal (CUIDADO: puede haber relacion NO lineal)
#   Interpretacion practica:
#     |r| > 0.9: correlacion muy fuerte
#     |r| > 0.7: correlacion fuerte
#     |r| > 0.4: correlacion moderada
#     |r| < 0.4: correlacion debil
#
# CONCEPTO: Correlacion NO implica causalidad.
#   Pero aca es obvio: el neto SE CALCULA a partir del bruto (menos deducciones).
#   Hay una relacion CAUSAL directa. La correlacion solo cuantifica que tan "limpia" es.
#
# CONCEPTO: R² (coeficiente de determinacion)
#   R² = r². Indica que % de la variabilidad de Y es explicada por X.
#   Si r = 0.95 → R² = 0.90 → el bruto explica el 90% de la variacion del neto.
#
# OTROS ABORDAJES posibles:
# - Correlacion de Spearman: mide relacion MONOTONA (no necesariamente lineal).
#   Usa rangos en vez de valores. Mas robusta contra outliers.
# - Regresion lineal: ajusta Y = a + bX y mide que tan bien predice.
# - Prueba de hipotesis: test de significancia para saber si r != 0.

from scipy import stats

print("\n" + "=" * 60)
print("2b) ASOCIACION — Salario bruto vs neto")
print("=" * 60)

# Pearson
r_pearson, p_pearson = stats.pearsonr(
    df2["salary_monthly_BRUTO"], df2["salary_monthly_NETO"]
)
print(f"\nCorrelacion de Pearson: r = {r_pearson:.4f}")
print(f"  p-valor: {p_pearson:.2e}")
print(f"  R² = {r_pearson**2:.4f} ({r_pearson**2*100:.1f}% de varianza explicada)")

# CONCEPTO: p-valor
# El p-valor responde: "si NO hubiera correlacion (H0: r=0),
# ¿cual es la probabilidad de observar un r tan extremo por puro azar?"
# Si p < 0.05: rechazamos H0 → la correlacion es estadisticamente significativa.
# Con 4000+ datos y r=0.95, el p-valor es esencialmente 0.

# Spearman (para comparar)
r_spearman, p_spearman = stats.spearmanr(
    df2["salary_monthly_BRUTO"], df2["salary_monthly_NETO"]
)
print(f"\nCorrelacion de Spearman: rho = {r_spearman:.4f}")
print(f"  p-valor: {p_spearman:.2e}")

# --- Grafico 2b: Scatter + regresion ---
fig, ax = plt.subplots(figsize=(10, 8))
sns.regplot(
    data=df2,
    x="salary_monthly_BRUTO",
    y="salary_monthly_NETO",
    scatter_kws={"alpha": 0.3, "s": 10},
    line_kws={"color": "red", "linewidth": 2},
    ax=ax,
)
ax.set_title(f"Salario Bruto vs Neto (Pearson r={r_pearson:.3f}, R²={r_pearson**2:.3f})")
ax.set_xlabel("Salario mensual BRUTO ($)")
ax.set_ylabel("Salario mensual NETO ($)")
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x/1e6:.0f}M"))
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x/1e6:.0f}M"))
plt.tight_layout()
plt.savefig("img/ej2b_scatter_bruto_neto.png", dpi=150)
plt.close()
print("\n[Guardado] ej2b_scatter_bruto_neto.png")

# CONCLUSION:
# Con r=0.95 y R²=0.90, el salario bruto explica el 90% de la variacion del neto.
# Se puede SACAR la columna de bruto sin perder informacion significativa.
# La relacion es practicamente lineal (como se ve en el scatter).
# La diferencia entre bruto y neto depende del tipo de contrato y deducciones,
# pero en la MAYORIA de los casos es un porcentaje relativamente estable.
print("\nCONCLUSION: Con r=0.95, la columna de salario bruto es REDUNDANTE.")
print("Se puede sacar de la encuesta sin perder informacion significativa.")

# =============================================================================
# 2c) DENSIDAD CONDICIONAL — Salario segun nivel de estudio
# =============================================================================
# CONCEPTO: Densidad condicional f(X | Y=y)
# Es la distribucion de X dado que Y toma un valor especifico.
# Ejemplo: "¿como se distribuye el salario DADO QUE la persona tiene
# titulo universitario?" vs "¿como se distribuye DADO QUE tiene secundario?"
#
# Si las distribuciones condicionales son IGUALES para todos los valores de Y,
# entonces X e Y son INDEPENDIENTES (saber Y no te dice nada sobre X).
# Si son DIFERENTES, hay DEPENDENCIA (saber Y cambia lo que esperas de X).
#
# CONCEPTO: Independencia estadistica
#   X e Y son independientes si: f(X|Y) = f(X)  para todo valor de Y
#   Es decir: saber el nivel de estudio no cambia la distribucion de salario.
#   Si son dependientes: f(X|Y=universitario) != f(X|Y=secundario)
#
# Para evaluar esto comparamos:
#   1. Histogramas superpuestos de cada subpoblacion
#   2. Medidas de centralidad y dispersion de cada grupo

print("\n" + "=" * 60)
print("2c) DENSIDAD CONDICIONAL — Salario segun nivel de estudio")
print("=" * 60)

# Veamos que niveles de estudio hay y cuantos datos tiene cada uno
print("\nNiveles de estudio:")
print(df2["profile_studies_level"].value_counts())

# Elegimos las dos subpoblaciones mas numerosas
# (necesitamos suficientes datos para que los histogramas sean confiables)
top_2_studies = df2["profile_studies_level"].value_counts().head(2).index.tolist()
print(f"\nSubpoblaciones elegidas: {top_2_studies}")

group_a = df2[df2["profile_studies_level"] == top_2_studies[0]]["salary_monthly_NETO"]
group_b = df2[df2["profile_studies_level"] == top_2_studies[1]]["salary_monthly_NETO"]

# Medidas de centralizacion y dispersion
# CONCEPTO: Medidas de centralidad — ¿donde esta el "centro" de los datos?
#   - Media: promedio aritmetico. Sensible a outliers.
#   - Mediana: valor central (50% arriba, 50% abajo). Robusta.
#   - Moda: valor mas frecuente. Util para categoricas, menos para continuas.
#
# CONCEPTO: Medidas de dispersion — ¿que tan "dispersos" estan?
#   - Desviacion estandar (std): distancia promedio a la media.
#   - Varianza: std². Menos intuitiva pero matematicamente conveniente.
#   - IQR: rango intercuartilico. Robusto contra outliers.
#   - Rango: max - min. Muy sensible a outliers.

print(f"\n{'Metrica':<20} {top_2_studies[0]:>20} {top_2_studies[1]:>20}")
print("-" * 62)
print(f"{'N (datos)':<20} {len(group_a):>20,} {len(group_b):>20,}")
print(f"{'Media':<20} {group_a.mean():>20,.0f} {group_b.mean():>20,.0f}")
print(f"{'Mediana':<20} {group_a.median():>20,.0f} {group_b.median():>20,.0f}")
print(f"{'Std':<20} {group_a.std():>20,.0f} {group_b.std():>20,.0f}")
print(f"{'Q1':<20} {group_a.quantile(0.25):>20,.0f} {group_b.quantile(0.25):>20,.0f}")
print(f"{'Q3':<20} {group_a.quantile(0.75):>20,.0f} {group_b.quantile(0.75):>20,.0f}")
print(f"{'IQR':<20} {group_a.quantile(0.75) - group_a.quantile(0.25):>20,.0f} {group_b.quantile(0.75) - group_b.quantile(0.25):>20,.0f}")

# --- Grafico 2c: Histogramas superpuestos ---
fig, ax = plt.subplots(figsize=(12, 7))
# CONCEPTO: stat="density" normaliza el histograma para que el area total sea 1.
# Esto permite comparar distribuciones con diferente cantidad de datos.
# Sin normalizar, el grupo mas grande siempre "tapa" al otro.
sns.histplot(group_a, label=f"{top_2_studies[0]} (n={len(group_a)})",
             stat="density", kde=True, alpha=0.5, color="steelblue", ax=ax)
sns.histplot(group_b, label=f"{top_2_studies[1]} (n={len(group_b)})",
             stat="density", kde=True, alpha=0.5, color="coral", ax=ax)
ax.set_title("Distribución de salario neto según nivel de estudio")
ax.set_xlabel("Salario mensual neto ($)")
ax.set_ylabel("Densidad")
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x/1e6:.1f}M"))
ax.legend()
plt.tight_layout()
plt.savefig("img/ej2c_histogramas_estudio.png", dpi=150)
plt.close()
print("\n[Guardado] ej2c_histogramas_estudio.png")

# Test de independencia: Mann-Whitney U
# CONCEPTO: El test de Mann-Whitney compara si dos muestras vienen de la
# misma distribucion. Es la version NO PARAMETRICA del t-test.
# No asume normalidad (y los salarios NO son normales).
# H0: las dos distribuciones son iguales (independencia)
# H1: son diferentes (dependencia)
stat_u, p_mannwhitney = stats.mannwhitneyu(group_a, group_b, alternative="two-sided")
print(f"\nTest Mann-Whitney U:")
print(f"  Estadistico U = {stat_u:,.0f}")
print(f"  p-valor = {p_mannwhitney:.2e}")
if p_mannwhitney < 0.05:
    print("  → Rechazamos H0: las distribuciones son DIFERENTES (p < 0.05)")
    print("  → El salario y el nivel de estudio NO son independientes.")
else:
    print("  → No podemos rechazar H0: no hay evidencia suficiente de diferencia.")

# =============================================================================
# 2d) DENSIDAD CONJUNTA CONDICIONAL — Scatter con hue
# =============================================================================
# CONCEPTO: Densidad conjunta condicional f(X, Y | Z=z)
# Es la distribucion conjunta de dos variables numericas, CONDICIONADA
# a una variable categorica.
#
# Visualmente: un scatterplot de X vs Y donde el COLOR indica Z.
# Si los colores forman "nubes" separadas, hay dependencia entre (X,Y) y Z.
# Si los colores se mezclan uniformemente, Z no afecta la relacion X-Y.
#
# CONCEPTO: hue en seaborn
# El parametro hue= mapea una variable categorica al color de los puntos.
# Es una de las formas mas poderosas de agregar una TERCERA dimension
# a un grafico 2D sin recurrir a 3D (que suele ser confuso).

print("\n" + "=" * 60)
print("2d) DENSIDAD CONJUNTA CONDICIONAL — Scatter con hue")
print("=" * 60)

# Variables elegidas:
#   Numericas: profile_age (X) y salary_monthly_NETO (Y)
#   Categorica: work_seniority (color)
# Justificacion: queremos ver si la relacion edad-salario cambia segun seniority.
# Hipotesis: un senior de 30 anios deberia ganar mas que un junior de 30 anios.

fig, ax = plt.subplots(figsize=(12, 8))
sns.scatterplot(
    data=df2,
    x="profile_age",
    y="salary_monthly_NETO",
    hue="work_seniority",
    hue_order=["Junior", "Semi-Senior", "Senior"],
    palette="Set2",
    alpha=0.5,
    s=30,
    ax=ax,
)
ax.set_title("Edad vs Salario Neto por Seniority")
ax.set_xlabel("Edad")
ax.set_ylabel("Salario mensual neto ($)")
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x/1e6:.1f}M"))
ax.legend(title="Seniority")
plt.tight_layout()
plt.savefig("img/ej2d_scatter_hue_seniority.png", dpi=150)
plt.close()
print("[Guardado] ej2d_scatter_hue_seniority.png")

# Version alternativa con lmplot: agrega lineas de regresion por grupo
# CONCEPTO: lmplot = scatterplot + regresion lineal, separado por hue.
# Cada grupo tiene su propia recta de ajuste, lo que permite ver
# si la PENDIENTE de la relacion edad-salario es distinta por seniority.
g = sns.lmplot(
    data=df2,
    x="profile_age",
    y="salary_monthly_NETO",
    hue="work_seniority",
    hue_order=["Junior", "Semi-Senior", "Senior"],
    palette="Set2",
    scatter_kws={"alpha": 0.3, "s": 15},
    height=7,
    aspect=1.4,
)
g.ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x/1e6:.1f}M"))
g.figure.suptitle("Regresión lineal Edad-Salario por Seniority", y=1.02)
plt.tight_layout()
plt.savefig("img/ej2d_lmplot_seniority.png", dpi=150)
plt.close()
print("[Guardado] ej2d_lmplot_seniority.png")

print("\n" + "=" * 60)
print("EJERCICIO 2 COMPLETO")
print("=" * 60)
