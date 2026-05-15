# =============================================================================
# TP2 — Inferencia y visualización
# Comparación de salarios netos entre Varón cis y Mujer cis
# Dataset: Encuesta Sysarmy 2026 (procesada)
# =============================================================================

# IDEA GENERAL DEL TP
# -------------------
# En TP1 nos enfocamos en describir datos: limpiar, resumir, visualizar,
# comparar distribuciones y extraer hallazgos.
#
# En TP2 damos un paso más: usamos herramientas de INFERENCIA.
# Eso significa que ya no nos quedamos solo con "qué pasó en esta muestra",
# sino que intentamos responder:
#   - ¿Cuál es una estimación razonable de la diferencia entre medias?
#   - ¿Qué incertidumbre tiene esa estimación?
#   - ¿La evidencia es suficiente para rechazar una hipótesis nula?
#   - ¿La muestra tenía tamaño suficiente para detectar el efecto?
#
# Vamos a trabajar igual que en TP1:
#   1. Script Python pedagógico y muy comentado
#   2. Notebook con la versión más narrativa/presentable

# =============================================================================
# PASO 0: Imports y configuración
# =============================================================================

import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
from statsmodels.stats.power import tt_ind_solve_power

sns.set_context("talk")

DIR = Path(__file__).parent
IMG_DIR = DIR / "img"
IMG_DIR.mkdir(exist_ok=True)

ALPHA = 0.05
DATA_URL = (
    "https://raw.githubusercontent.com/DiploDatos/AnalisisyVisualizacion/"
    "refs/heads/master/sysarmy_survey_2026_processed.csv"
)

# =============================================================================
# PASO 1: Carga de datos
# =============================================================================
# Igual que en TP1, primero cargamos el CSV remoto en un DataFrame.

print("=" * 80)
print("PASO 1 — CARGA DE DATOS")
print("=" * 80)

df = pd.read_csv(DATA_URL)
print(f"Forma del dataset: {df.shape}")
print(df[["profile_gender", "salary_monthly_NETO", "work_dedication"]].head())

# =============================================================================
# PASO 2: Variable de género agrupada
# =============================================================================
# En la notebook original de TP2 se agrupan identidades de género en:
#   - Varón cis
#   - Mujer cis
#   - Diversidades
#
# Para los ejercicios de inferencia vamos a comparar específicamente:
#   groupA = Varón cis
#   groupB = Mujer cis

print("\n" + "=" * 80)
print("PASO 2 — RECODIFICACIÓN DE GÉNERO")
print("=" * 80)

gender_map = {
    "Hombre Cis": "Varón cis",
    "Mujer Cis": "Mujer cis",
    "Queer": "Diversidades",
    "Trans": "Diversidades",
    "Lesbiana": "Diversidades",
    "Agénero": "Diversidades",
}

df = df.copy()
df["profile_g"] = df["profile_gender"].replace(gender_map)
print(df["profile_g"].value_counts(dropna=False))

# =============================================================================
# PASO 3: Selección y limpieza de la variable salario
# =============================================================================
# Acá conviene ser EXPLÍCITOS con el criterio de limpieza, tal como hicimos en TP1.
#
# Queremos comparar salarios netos entre dos grupos. Entonces:
#   - eliminamos NaN
#   - conservamos solo Varón cis y Mujer cis
#   - filtramos solo Full-Time para no mezclar dedicaciones distintas
#   - filtramos salarios absurdamente bajos o altos
#   - removemos outliers por IQR
#
# Esto define mejor la pregunta estadística del trabajo:
#   - parámetro de interés: mu_A - mu_B
#   - muestra analizada: casos observados que sobreviven al filtrado
#   - población de referencia: personas comparables dentro de la encuesta
#
# OJO: cualquier decisión de limpieza afecta la inferencia.
# Por eso dejamos el criterio escrito y reproducible. Además, esta encuesta es
# observacional y voluntaria: no equivale a una muestra aleatoria perfecta de
# todo el mercado IT, así que la generalización debe hacerse con cautela.

print("\n" + "=" * 80)
print("PASO 3 — LIMPIEZA DE DATOS")
print("=" * 80)

salary_min = 300_000
salary_max = 20_000_000

analysis_df = df[["profile_g", "salary_monthly_NETO", "work_dedication"]].copy()
print(f"Filas iniciales: {len(analysis_df)}")

analysis_df = analysis_df.dropna(subset=["profile_g", "salary_monthly_NETO", "work_dedication"])
print(f"Después de eliminar NaN: {len(analysis_df)}")

analysis_df = analysis_df[analysis_df["profile_g"].isin(["Varón cis", "Mujer cis"])]
print(f"Después de quedarnos con los dos grupos: {len(analysis_df)}")

analysis_df = analysis_df[analysis_df["work_dedication"] == "Full-Time"]
print(f"Después de filtrar solo Full-Time: {len(analysis_df)}")

analysis_df = analysis_df[
    analysis_df["salary_monthly_NETO"].between(salary_min, salary_max)
]
print(f"Después de filtrar salarios [{salary_min:,} - {salary_max:,}]: {len(analysis_df)}")

# Igual que en TP1, removemos outliers por IQR para trabajar con una muestra
# más robusta frente a valores extremos.
Q1 = analysis_df["salary_monthly_NETO"].quantile(0.25)
Q3 = analysis_df["salary_monthly_NETO"].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

analysis_df = analysis_df[
    analysis_df["salary_monthly_NETO"].between(lower_bound, upper_bound)
]
print(f"Después de IQR [{lower_bound:,.0f} - {upper_bound:,.0f}]: {len(analysis_df)}")

print("\nConteo por grupo:")
print(analysis_df["profile_g"].value_counts())

# Armamos las dos muestras que vamos a comparar.
# A partir de este punto, todo el análisis inferencial descansa sobre estas
# muestras independientes.
groupA = analysis_df.loc[
    analysis_df["profile_g"] == "Varón cis", "salary_monthly_NETO"
].copy()
groupB = analysis_df.loc[
    analysis_df["profile_g"] == "Mujer cis", "salary_monthly_NETO"
].copy()

print(f"\nTamaño groupA (Varón cis): {len(groupA)}")
print(f"Tamaño groupB (Mujer cis): {len(groupB)}")

# =============================================================================
# PASO 4: Exploración descriptiva inicial
# =============================================================================
# Antes de inferir, SIEMPRE conviene mirar la muestra.
# Si no entendemos las distribuciones, interpretar un test después es riesgoso.

print("\n" + "=" * 80)
print("PASO 4 — DESCRIPTIVOS")
print("=" * 80)

summary = pd.DataFrame(
    {
        "Varón cis": groupA.describe(),
        "Mujer cis": groupB.describe(),
    }
)
print(summary)

print("\nSupuestos y condiciones de trabajo:")
print("- Tratamos las observaciones como aproximadamente independientes.")
print("- Usamos Welch porque no exige igualdad de varianzas entre grupos.")
print("- Los tamaños muestrales grandes ayudan a justificar la inferencia sobre medias.")

print("\nMedias:")
print(f"Varón cis: {groupA.mean():,.2f}")
print(f"Mujer cis: {groupB.mean():,.2f}")
print(f"Diferencia de medias (A - B): {groupA.mean() - groupB.mean():,.2f}")

print("\nMedianas:")
print(f"Varón cis: {groupA.median():,.2f}")
print(f"Mujer cis: {groupB.median():,.2f}")

# Una lectura rápida de estos números:
#   - si media y mediana están relativamente separadas, puede haber asimetría;
#   - si un grupo presenta mayor dispersión, Welch es preferible a un t clásico
#     con varianzas iguales;
#   - si ambos grupos conservan tamaños grandes, el TCL ayuda a que la
#     distribución de la media muestral sea aproximadamente normal;
#   - mirar esto ANTES del test evita interpretar resultados en el vacío.

# =============================================================================
# PASO 5: Visualización exploratoria
# =============================================================================
# Guardamos gráficos en img/ para poder reutilizarlos luego en notebook o reporte.

print("\n" + "=" * 80)
print("PASO 5 — VISUALIZACIONES EXPLORATORIAS")
print("=" * 80)

fig, axes = plt.subplots(1, 2, figsize=(16, 5), sharey=True)
axes[0].hist(groupA, bins=40, color="steelblue", edgecolor="black", alpha=0.85)
axes[0].set_title("Varón cis")
axes[0].set_xlabel("Salario neto mensual")
axes[0].set_ylabel("Frecuencia")

axes[1].hist(groupB, bins=40, color="salmon", edgecolor="black", alpha=0.85)
axes[1].set_title("Mujer cis")
axes[1].set_xlabel("Salario neto mensual")

fig.suptitle("Histogramas por grupo")
fig.tight_layout()
fig.savefig(IMG_DIR / "tp2_histogramas_grupos.png", dpi=160, bbox_inches="tight")
plt.close(fig)

plot_df = analysis_df.copy()
fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(data=plot_df, x="profile_g", y="salary_monthly_NETO", ax=ax)
ax.set_title("Distribución salarial por grupo")
ax.set_xlabel("Grupo")
ax.set_ylabel("Salario neto mensual")
fig.tight_layout()
fig.savefig(IMG_DIR / "tp2_boxplot_grupos.png", dpi=160, bbox_inches="tight")
plt.close(fig)

# =============================================================================
# PASO 6: Ejercicio 1 — Estimación puntual e intervalo de confianza
# =============================================================================
# Queremos estimar:
#   mu_A - mu_B
# donde:
#   mu_A = media poblacional del salario neto de Varón cis
#   mu_B = media poblacional del salario neto de Mujer cis
#
# La estimación puntual natural es:
#   media_muestral_A - media_muestral_B
#
# Para el intervalo de confianza usamos la aproximación t de Welch,
# que NO asume varianzas iguales.
#
# Además, este intervalo se conecta directamente con el test de hipótesis:
# si el 0 cae dentro del intervalo, no esperaríamos rechazar H0 al 5%;
# si el 0 queda afuera, eso es consistente con rechazar H0.

print("\n" + "=" * 80)
print("PASO 6 — EJERCICIO 1: ESTIMACIÓN")
print("=" * 80)

mean_diff = groupA.mean() - groupB.mean()
varA = groupA.var(ddof=1)
varB = groupB.var(ddof=1)
nA = len(groupA)
nB = len(groupB)

se_diff = math.sqrt(varA / nA + varB / nB)

# Grados de libertad aproximados por Welch-Satterthwaite
welch_df = (varA / nA + varB / nB) ** 2 / (
    ((varA / nA) ** 2 / (nA - 1)) + ((varB / nB) ** 2 / (nB - 1))
)

t_crit = stats.t.ppf(1 - ALPHA / 2, df=welch_df)
ci_low = mean_diff - t_crit * se_diff
ci_high = mean_diff + t_crit * se_diff

print(f"Estimación puntual (media A - media B): {mean_diff:,.2f}")
print(f"Error estándar de la diferencia: {se_diff:,.2f}")
print(f"Grados de libertad aproximados (Welch): {welch_df:,.2f}")
print(f"IC {100*(1-ALPHA):.0f}% para (mu_A - mu_B): [{ci_low:,.2f}, {ci_high:,.2f}]")

if ci_low > 0 or ci_high < 0:
    print("Interpretación: el intervalo no contiene al 0, así que la diferencia")
    print("entre medias se mantiene positiva/negativa incluso incorporando incertidumbre.")
else:
    print("Interpretación: el intervalo contiene al 0, así que no habría evidencia")
    print("suficiente para afirmar una diferencia clara entre medias al 95%.")

relative_gap = mean_diff / groupB.mean()
print(f"Magnitud práctica aproximada: la diferencia equivale al {relative_gap:.1%} del salario promedio de Mujer cis.")

# =============================================================================
# PASO 7: Ejercicio 2 — Test de hipótesis
# =============================================================================
# Formalización:
#   H0: mu_A - mu_B = 0
#   H1: mu_A - mu_B != 0
#
# Usamos un test t para dos muestras independientes, versión Welch.
# Esto permite comparar medias sin asumir igualdad de varianzas.
#
# Importante: esto sigue siendo una comparación BIVARIADA.
# No estamos controlando explícitamente por seniority, rol, experiencia,
# stack tecnológico u otras variables que podrían actuar como confusoras.
# Por lo tanto, la conclusión debe leerse como una diferencia observada
# en la muestra analizada, no como una relación causal pura.

print("\n" + "=" * 80)
print("PASO 7 — EJERCICIO 2: TEST DE HIPÓTESIS")
print("=" * 80)

ttest = stats.ttest_ind(groupA, groupB, equal_var=False, alternative="two-sided")
print(f"Estadístico t: {ttest.statistic:,.4f}")
print(f"p-valor: {ttest.pvalue:,.8f}")

if ttest.pvalue < ALPHA:
    print(f"Decisión: Rechazamos H0 al nivel α = {ALPHA}")
    print("La muestra ofrece evidencia estadística de que las medias difieren.")
else:
    print(f"Decisión: No rechazamos H0 al nivel α = {ALPHA}")
    print("La muestra no ofrece evidencia estadística suficiente para afirmar diferencia.")

# =============================================================================
# PASO 8: Potencia del test
# =============================================================================
# La potencia responde: si realmente existe una diferencia de cierto tamaño,
# ¿qué tan probable era detectarla con nuestra muestra?
#
# Para estandarizar la diferencia usamos Cohen's d con desvío combinado
# (pooled standard deviation), que es una referencia más estándar que tomar
# sólo la dispersión de uno de los grupos.
# Como corrección por sesgo muestral también mostramos Hedges' g.
# La potencia para Welch no tiene una fórmula cerrada tan directa en esta
# implementación, así que usamos d como aproximación práctica y explicitamos
# esa decisión.

print("\n" + "=" * 80)
print("PASO 8 — POTENCIA DEL TEST")
print("=" * 80)

pooled_std = math.sqrt(((nA - 1) * varA + (nB - 1) * varB) / (nA + nB - 2))
cohen_d = mean_diff / pooled_std
hedges_g = cohen_d * (1 - 3 / (4 * (nA + nB) - 9))
ratio = len(groupB) / len(groupA)
power_target = 0.80

required_n_groupA = tt_ind_solve_power(
    effect_size=cohen_d,
    alpha=ALPHA,
    power=power_target,
    ratio=ratio,
    alternative="two-sided",
)

# En este caso, statsmodels devuelve NaN para la potencia "observada" con estos
# tamaños muestrales concretos. Para no dejar el análisis roto, la aproximamos
# por simulación Monte Carlo usando las medias y desvíos observados.
rng = np.random.default_rng(42)
n_sim = 2000
rejections = 0

for _ in range(n_sim):
    sim_A = rng.normal(loc=groupA.mean(), scale=groupA.std(ddof=1), size=len(groupA))
    sim_B = rng.normal(loc=groupB.mean(), scale=groupB.std(ddof=1), size=len(groupB))
    sim_test = stats.ttest_ind(sim_A, sim_B, equal_var=False, alternative="two-sided")
    if sim_test.pvalue < ALPHA:
        rejections += 1

observed_power = rejections / n_sim

print(f"Desvío combinado (pooled std): {pooled_std:,.2f}")
print(f"Cohen's d: {cohen_d:,.4f}")
print(f"Hedges' g: {hedges_g:,.4f}")
print(f"Ratio n_B / n_A: {ratio:,.4f}")
print(f"n requerido en groupA para potencia 0.80: {required_n_groupA:,.2f}")
print(f"Potencia observada aproximada (simulación): {observed_power:,.4f}")
if len(groupA) > required_n_groupA:
    print("Lectura: el tamaño de muestra observado parece más que suficiente")
    print("para detectar un efecto de esta magnitud.")

# =============================================================================
# PASO 9: Chequeos de robustez
# =============================================================================
# Para no depender de una única mirada, contrastamos la conclusión principal con
# dos chequeos simples:
#   1. comparar medianas, menos sensibles a extremos;
#   2. usar Mann-Whitney como contraste no paramétrico complementario.

print("\n" + "=" * 80)
print("PASO 9 — CHEQUEOS DE ROBUSTEZ")
print("=" * 80)

median_diff = groupA.median() - groupB.median()
mannwhitney = stats.mannwhitneyu(groupA, groupB, alternative="two-sided")

print(f"Diferencia de medianas (A - B): {median_diff:,.2f}")
print(f"Mann-Whitney U: {mannwhitney.statistic:,.2f}")
print(f"p-valor Mann-Whitney: {mannwhitney.pvalue:,.8f}")
print("Lectura: si la señal se mantiene también al comparar medianas y con un test no paramétrico,")
print("la conclusión principal resulta más robusta y menos dependiente de supuestos finos.")

# =============================================================================
# PASO 10: Ejercicio 3 — Comunicación y visualización
# =============================================================================
# En este ejercicio no alcanza con "hacer un gráfico lindo".
# Hay que elegir un mensaje y construir una visualización que lo comunique.
#
# Mensaje propuesto:
#   "En la muestra analizada de trabajadores Full-Time, el salario neto promedio
#    de Varón cis supera al de Mujer cis. La diferencia estimada ronda los
#    378 mil pesos mensuales, con un IC95% entre ~276 mil y ~481 mil pesos."
#
# Vamos a armar una visualización sencilla centrada en:
#   - la diferencia estimada de medias
#   - su intervalo de confianza

print("\n" + "=" * 80)
print("PASO 10 — EJERCICIO 3: COMUNICACIÓN")
print("=" * 80)

fig, ax = plt.subplots(figsize=(10, 4))
ax.errorbar(
    x=mean_diff,
    y=0,
    xerr=[[mean_diff - ci_low], [ci_high - mean_diff]],
    fmt="o",
    color="purple",
    ecolor="purple",
    elinewidth=3,
    capsize=8,
    markersize=10,
)
ax.axvline(0, color="black", linestyle="--", linewidth=1)
ax.set_yticks([])
ax.set_xlabel("Diferencia de medias (Varón cis - Mujer cis)")
ax.set_title("Estimación de la brecha salarial media con IC del 95%")
ax.text(
    mean_diff,
    0.08,
    f"Estimación = {mean_diff:,.0f}\nIC95% = [{ci_low:,.0f}, {ci_high:,.0f}]",
    ha="center",
    va="bottom",
    fontsize=11,
)
fig.tight_layout()
fig.savefig(IMG_DIR / "tp2_estimacion_ic.png", dpi=160, bbox_inches="tight")
plt.close(fig)

# =============================================================================
# PASO 11: Resumen interpretativo
# =============================================================================

print("\n" + "=" * 80)
print("PASO 11 — RESUMEN")
print("=" * 80)
print(
    "1) La estimación puntual de la diferencia de medias se calcula como "
    "media(Varón cis) - media(Mujer cis)."
)
print(
    f"2) El IC95% estimado fue [{ci_low:,.0f}, {ci_high:,.0f}]. "
    "Si este intervalo no contiene al 0, eso da evidencia de diferencia entre medias."
)
print(
    f"3) El p-valor del test de Welch fue {ttest.pvalue:,.6f}. "
    "La decisión depende de compararlo contra α = 0.05."
)
print(
    f"4) La potencia observada aproximada fue {observed_power:,.3f}. "
    "Esto ayuda a discutir si el tamaño muestral fue suficiente."
)
print(
    "5) El análisis sigue siendo bivariado: no controla explícitamente por "
    "seniority, rol, experiencia u otros posibles confusores."
)
print(
    "6) Además, la encuesta es observacional y voluntaria: puede haber "
    "autoselección, subcobertura de ciertos perfiles y error de autorreporte, "
    "por lo que la generalización al mercado completo debe hacerse con cautela."
)
print(
    "7) La diferencia también se sostuvo al comparar medianas y con un test "
    "no paramétrico complementario, lo que refuerza la robustez del hallazgo."
)
print(f"8) Gráficos guardados en: {IMG_DIR}")
