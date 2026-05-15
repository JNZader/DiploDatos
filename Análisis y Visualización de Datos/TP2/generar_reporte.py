"""
Genera un reporte HTML para el Ejercicio 3 del TP2.

Uso:
    python generar_reporte.py

Salida:
    reporte_tp2.html

El reporte recalcula los indicadores principales con el mismo criterio del TP2 y
embebe los gráficos ya generados en img/.
"""

import base64
import math
from pathlib import Path

import pandas as pd
from scipy import stats
from statsmodels.stats.power import tt_ind_solve_power

OUTPUT = "reporte_tp2.html"
DIR = Path(__file__).parent
IMG_DIR = DIR / "img"
ALPHA = 0.05
DATA_URL = (
    "https://raw.githubusercontent.com/DiploDatos/AnalisisyVisualizacion/"
    "refs/heads/master/sysarmy_survey_2026_processed.csv"
)


def img_to_base64(filename: str) -> str:
    path = IMG_DIR / filename
    if not path.exists():
        return f'<p class="warning">Imagen no encontrada: {filename}</p>'
    data = path.read_bytes()
    b64 = base64.b64encode(data).decode()
    return (
        f'<img src="data:image/png;base64,{b64}" '
        'style="max-width:100%; border-radius:12px; margin:1rem 0;">'
    )


def build_analysis() -> dict:
    df = pd.read_csv(DATA_URL)

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

    analysis_df = df[["profile_g", "salary_monthly_NETO", "work_dedication"]].copy()
    initial_n = len(analysis_df)
    analysis_df = analysis_df.dropna(subset=["profile_g", "salary_monthly_NETO", "work_dedication"])
    after_na = len(analysis_df)
    analysis_df = analysis_df[analysis_df["profile_g"].isin(["Varón cis", "Mujer cis"])]
    after_groups = len(analysis_df)
    analysis_df = analysis_df[analysis_df["work_dedication"] == "Full-Time"]
    after_full_time = len(analysis_df)
    analysis_df = analysis_df[analysis_df["salary_monthly_NETO"].between(300_000, 20_000_000)]
    after_domain = len(analysis_df)

    q1 = analysis_df["salary_monthly_NETO"].quantile(0.25)
    q3 = analysis_df["salary_monthly_NETO"].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    analysis_df = analysis_df[analysis_df["salary_monthly_NETO"].between(lower, upper)]
    final_n = len(analysis_df)

    group_a = analysis_df.loc[analysis_df["profile_g"] == "Varón cis", "salary_monthly_NETO"]
    group_b = analysis_df.loc[analysis_df["profile_g"] == "Mujer cis", "salary_monthly_NETO"]

    mean_diff = group_a.mean() - group_b.mean()
    var_a = group_a.var(ddof=1)
    var_b = group_b.var(ddof=1)
    n_a = len(group_a)
    n_b = len(group_b)
    se_diff = math.sqrt(var_a / n_a + var_b / n_b)
    welch_df = (var_a / n_a + var_b / n_b) ** 2 / (
        ((var_a / n_a) ** 2 / (n_a - 1)) + ((var_b / n_b) ** 2 / (n_b - 1))
    )
    t_crit = stats.t.ppf(1 - ALPHA / 2, df=welch_df)
    ci_low = mean_diff - t_crit * se_diff
    ci_high = mean_diff + t_crit * se_diff

    ttest = stats.ttest_ind(group_a, group_b, equal_var=False, alternative="two-sided")
    pooled_std = math.sqrt(((n_a - 1) * var_a + (n_b - 1) * var_b) / (n_a + n_b - 2))
    cohen_d = mean_diff / pooled_std
    hedges_g = cohen_d * (1 - 3 / (4 * (n_a + n_b) - 9))
    ratio = n_b / n_a
    required_n_group_a = tt_ind_solve_power(
        effect_size=cohen_d,
        alpha=ALPHA,
        power=0.80,
        ratio=ratio,
        alternative="two-sided",
    )

    median_diff = group_a.median() - group_b.median()
    mannwhitney = stats.mannwhitneyu(group_a, group_b, alternative="two-sided")

    return {
        "initial_n": initial_n,
        "after_na": after_na,
        "after_groups": after_groups,
        "after_full_time": after_full_time,
        "after_domain": after_domain,
        "final_n": final_n,
        "n_a": n_a,
        "n_b": n_b,
        "mean_diff": mean_diff,
        "ci_low": ci_low,
        "ci_high": ci_high,
        "t_stat": ttest.statistic,
        "pvalue": ttest.pvalue,
        "pooled_std": pooled_std,
        "cohen_d": cohen_d,
        "hedges_g": hedges_g,
        "required_n_group_a": required_n_group_a,
        "median_diff": median_diff,
        "mw_pvalue": mannwhitney.pvalue,
        "relative_gap": mean_diff / group_b.mean(),
        "lower_iqr": lower,
        "upper_iqr": upper,
    }


def money(value: float) -> str:
    return f"${value:,.0f}".replace(",", ".")


def pct(value: float) -> str:
    return f"{100 * value:.1f}%"


result = build_analysis()

html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>TP2 — Comunicación de resultados</title>
<style>
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    font-family: 'Segoe UI', system-ui, sans-serif;
    background: #f7f9fc;
    color: #1d2433;
    line-height: 1.65;
  }}
  .container {{ max-width: 980px; margin: 0 auto; padding: 2rem 1rem 4rem; }}
  .hero {{
    background: linear-gradient(135deg, #1d3557, #457b9d);
    color: white;
    border-radius: 20px;
    padding: 2rem;
    box-shadow: 0 10px 30px rgba(29, 53, 87, 0.18);
  }}
  h1, h2, h3 {{ margin: 0 0 0.75rem; }}
  h1 {{ font-size: 2rem; }}
  h2 {{ color: #1d3557; margin-top: 2rem; }}
  .subtitle {{ opacity: 0.92; margin-top: 0.5rem; }}
  .grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-top: 1.5rem; }}
  .card {{
    background: white;
    border-radius: 16px;
    padding: 1.25rem;
    box-shadow: 0 4px 18px rgba(20, 27, 45, 0.08);
    margin-top: 1rem;
  }}
  .metric {{ font-size: 1.7rem; font-weight: 700; color: #6a1b9a; margin: 0.4rem 0; }}
  .label {{ font-size: 0.92rem; color: #5b6579; text-transform: uppercase; letter-spacing: 0.03em; }}
  .callout {{
    background: #eef5ff;
    border-left: 5px solid #457b9d;
    padding: 1rem 1.25rem;
    border-radius: 0 12px 12px 0;
    margin-top: 1rem;
  }}
  .note {{
    background: #fff7e6;
    border-left: 5px solid #ff9800;
    padding: 1rem 1.25rem;
    border-radius: 0 12px 12px 0;
    margin-top: 1rem;
  }}
  table {{ width: 100%; border-collapse: collapse; margin-top: 1rem; }}
  th, td {{ padding: 0.8rem; border-bottom: 1px solid #e5e9f2; text-align: left; }}
  th {{ background: #1d3557; color: white; }}
  .small {{ color: #667085; font-size: 0.95rem; }}
  .warning {{ color: #b42318; font-weight: 600; }}
  ul {{ padding-left: 1.25rem; }}
  @media (max-width: 820px) {{ .grid {{ grid-template-columns: 1fr; }} }}
</style>
</head>
<body>
<div class="container">
  <section class="hero">
    <h1>TP2 — Ejercicio 3: comunicación de un resultado relevante</h1>
    <p><strong>Diplomatura en Ciencia de Datos — Análisis y Visualización de Datos</strong></p>
    <p class="subtitle">Mensaje elegido: en la muestra filtrada de personas Full-Time, el salario neto promedio de Varón cis supera al de Mujer cis.</p>
  </section>

  <section class="grid">
    <div class="card">
      <div class="label">Diferencia estimada</div>
      <div class="metric">{money(result['mean_diff'])}</div>
      <p class="small">Brecha media mensual estimada entre ambos grupos.</p>
    </div>
    <div class="card">
      <div class="label">IC 95%</div>
      <div class="metric">[{money(result['ci_low'])}, {money(result['ci_high'])}]</div>
      <p class="small">Toda la banda queda del lado positivo.</p>
    </div>
    <div class="card">
      <div class="label">Magnitud práctica</div>
      <div class="metric">{pct(result['relative_gap'])}</div>
      <p class="small">Proporción de la diferencia respecto del salario promedio de Mujer cis.</p>
    </div>
  </section>

  <section class="card">
    <h2>1. Cómo se construyó la muestra</h2>
    <p>Siguiendo el mismo criterio metodológico usado en TP1, la inferencia se realiza sobre una muestra más comparable:</p>
    <ul>
      <li>se conservaron solo los grupos <strong>Varón cis</strong> y <strong>Mujer cis</strong>;</li>
      <li>se filtró la modalidad <strong>Full-Time</strong> para evitar mezclar distintas cargas horarias;</li>
      <li>se excluyeron salarios fuera del rango plausible <strong>$300.000 – $20.000.000</strong>;</li>
      <li>se eliminaron outliers con el criterio <strong>1.5 IQR</strong>.</li>
    </ul>
    <table>
      <tr><th>Paso</th><th>Filas restantes</th></tr>
      <tr><td>Base inicial</td><td>{result['initial_n']}</td></tr>
      <tr><td>Eliminar NaN relevantes</td><td>{result['after_na']}</td></tr>
      <tr><td>Conservar solo grupos comparados</td><td>{result['after_groups']}</td></tr>
      <tr><td>Filtrar Full-Time</td><td>{result['after_full_time']}</td></tr>
      <tr><td>Aplicar rango de salario plausible</td><td>{result['after_domain']}</td></tr>
      <tr><td>Aplicar IQR [{money(result['lower_iqr'])}; {money(result['upper_iqr'])}]</td><td>{result['final_n']}</td></tr>
    </table>
    <p class="small">Tamaños finales: Varón cis = {result['n_a']} | Mujer cis = {result['n_b']}.</p>
  </section>

  <section class="card">
    <h2>2. Resultado principal</h2>
    <div class="callout">
      <strong>Interpretación central:</strong> la diferencia estimada ronda los <strong>{money(result['mean_diff'])}</strong> mensuales y el intervalo de confianza del 95% va de <strong>{money(result['ci_low'])}</strong> a <strong>{money(result['ci_high'])}</strong>. Como el intervalo no contiene al 0, el resultado es consistente con rechazar la hipótesis nula de igualdad de medias al nivel del 5%.
    </div>
    {img_to_base64('tp2_estimacion_ic.png')}
    <p>El gráfico está construido para comunicar una sola idea: la brecha salarial media estimada es positiva y se mantiene positiva incluso al incorporar incertidumbre muestral.</p>
  </section>

  <section class="card">
    <h2>3. Evidencia estadística y robustez</h2>
    <p>Además del intervalo de confianza, se aplicó un test t de Welch para dos muestras independientes:</p>
    <ul>
      <li><strong>Estadístico t:</strong> {result['t_stat']:.4f}</li>
      <li><strong>p-valor:</strong> {result['pvalue']:.8f}</li>
      <li><strong>Desvío combinado:</strong> {result['pooled_std']:.0f}</li>
      <li><strong>Cohen's d:</strong> {result['cohen_d']:.4f}</li>
      <li><strong>Hedges' g:</strong> {result['hedges_g']:.4f}</li>
      <li><strong>n requerido para potencia 0.80:</strong> {result['required_n_group_a']:.1f} casos en groupA</li>
    </ul>
    <p>Como chequeo complementario, también se compararon medianas y se aplicó un contraste no paramétrico:</p>
    <ul>
      <li><strong>Diferencia de medianas:</strong> {money(result['median_diff'])}</li>
      <li><strong>p-valor Mann-Whitney:</strong> {result['mw_pvalue']:.8f}</li>
    </ul>
    <p>La señal principal se sostiene incluso con estas variantes, lo que refuerza la robustez del hallazgo.</p>
  </section>

  <section class="card">
    <h2>4. Visualizaciones de apoyo</h2>
    <p>Antes de inferir, se inspeccionó descriptivamente la muestra para revisar forma, dispersión y posibles asimetrías.</p>
    {img_to_base64('tp2_histogramas_grupos.png')}
    {img_to_base64('tp2_boxplot_grupos.png')}
  </section>

  <section class="card">
    <h2>5. Lectura final y limitaciones</h2>
    <div class="callout">
      <strong>Síntesis:</strong> en la muestra filtrada de personas Full-Time, aparece evidencia consistente de una brecha salarial media a favor del grupo <strong>Varón cis</strong>. Esa diferencia es estadísticamente detectable, tiene magnitud práctica relevante y se sostiene bajo chequeos de robustez sencillos.
    </div>
    <div class="note">
      <strong>Cautelas de interpretación:</strong> el análisis es bivariado y no controla explícitamente seniority, experiencia, rol, stack u otras variables potencialmente relevantes. Además, la encuesta es observacional y voluntaria: puede haber autoselección, subcobertura de ciertos perfiles y error de autorreporte, por lo que la representatividad poblacional no está garantizada en sentido estricto.
    </div>
  </section>
</div>
</body>
</html>
"""

(DIR / OUTPUT).write_text(html, encoding="utf-8")
print(f"Reporte generado en: {DIR / OUTPUT}")
