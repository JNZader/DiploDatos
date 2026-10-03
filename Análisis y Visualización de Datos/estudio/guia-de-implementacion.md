# Guía de implementación: Análisis y Visualización de Datos (Diplodatos, FAMAF UNC, Georgina Flesia y Karim Nemer)

**Videos:** C1P1, C1P2, C2P1, C2P2, C3P1, C3P2, C4P1, C4P2 y los videos de apoyo de Milagro Teruel V01, V02, V03, V04, V05. El apunte de estudio que acompaña esta guía es `analisis-y-visualizacion-apunte-de-estudio.md`.
**De qué va:** la parte práctica de la materia, ordenada por tema y no por clase: cómo leer y limpiar la encuesta de sueldos de Sysarmy 2026, graficar una variable, calcular probabilidades con los datos, describir y tratar outliers, trabajar con distribuciones, relacionar varias variables, simular el teorema central del límite, armar intervalos de confianza, hacer tests de hipótesis con scipy y comunicar con gráficos honestos. Todo con el código de las notebooks 00 a 05 del repositorio público `DiploDatos/AnalisisyVisualizacion`, corregido donde la clase o la notebook se equivocan.

> Nota: los links llevan al minuto de la clase donde se ve cada cosa ("C3P1 1:02:15" es la clase 3, parte 1, en la hora 1, minuto 2, segundo 15; "V04 2:12" es el video de apoyo 04). Todo el código de esta guía se corrió en el box con Python 3, pandas 3.0.6, seaborn 0.13.2, matplotlib 3.11.2, scipy 1.18.1 y statsmodels 0.15.0 y scikit-learn 1.9.1 (Python 3.13), contra `sysarmy_survey_2026_processed.csv` y los CSV de la notebook 05 del repositorio (rama `master`). Los números que aparecen como "lo que da en el box" son las salidas reales. En Colab, borrá la línea `matplotlib.use("Agg")` y cambiá las rutas `/workspace/yt/...` por las tuyas o por la URL del repositorio.

## Checklist para arrancar ya
1. Abrí cada notebook desde el repositorio 2026 y guardá una copia en tu Drive; si un link de la filmina da 404, cambiá 2025 por 2026 en la URL C1P1 1:15:52, C1P1 1:54:41.
2. Leé el CSV procesado directo de GitHub con `pd.read_csv(URL)` y mirá `shape`, `dtypes`, `isna().mean()` y `describe()` antes de graficar nada (sección 1).
3. Recodificá género con `map` desde las categorías reales de 2026 (`"Hombre Cis"`, `"Mujer Cis"`), no con el diccionario de la notebook 03, que deja vacío el grupo de varones (sección 1).
4. Decidí y documentá los cortes: edad menor a 70, neto entre un mínimo razonable y 15 o 40 millones, filas con neto mayor que bruto; justificá cada uno como experto del dominio C3P1 1:24:49.
5. En los histogramas usá `stat="count"`, `"probability"` o `"density"` sabiendo qué suma 1; `"frequency"` no es la frecuencia relativa (sección 2).
6. Guardá las figuras con `fig.savefig(...)` en la misma celda que las dibuja, nunca en una celda aparte C2P1 30:30.
7. Para categóricas usá barras ordenadas (`order=value_counts().index`); nunca histogramas de booleanos ni líneas entre provincias C2P1 34:31.
8. Reportá media y mediana juntas; con sueldos, preferí la mediana y el IQR (sección 4).
9. Marcá outliers con la regla de Tukey (1,5 IQR) y compará contra otros criterios antes de tirar filas; informá cuántas filas sacás y por qué (sección 4).
10. Estandarizá con z score o con min max bien hecho, `(x − min)/(max − min)` (sección 5).
11. Para relacionar bruto y neto, mirá Pearson y Spearman juntos: si difieren mucho, hay outliers (sección 6).
12. Para comparar grupos, armá intervalos de confianza con Welch (`ttest_ind(..., equal_var=False).confidence_interval()`); si las dos medidas son de la misma persona, usá el test apareado (sección 7).
13. En los tests, compará el p valor de scipy con α = 0,05, no con 0,025, y fijá `alternative` según H1 (sección 8).
14. Si un ANOVA rechaza, hacé un post hoc (Tukey HSD) para saber qué grupos difieren (sección 8).
15. Para la brecha de género, además del test general, condicioná por seniority C4P1 44:21 (sección 8).
16. En la visualización final: ejes desde 0 en barras, distribuciones en vez de dynamite plots, paleta apta para daltonismo y un solo mensaje claro (sección 9).
17. Verificá que la notebook del grupo corra entera de principio a fin antes de entregar C2P1 13:50 (sección 10).

## Versión completa

### 1. Entorno, lectura y limpieza mínima del dataset
**En clase:** C1P1 1:14:12, C1P1 1:15:52, C1P1 1:21:27, C1P1 1:25:29, C1P1 1:33:03, C1P1 1:36:24, C1P1 1:41:04, C1P1 1:45:31, C1P1 1:54:41, V03 0:01, V03 3:18, V03 4:57, C1P2 48:46, C1P2 1:16:00, C2P1 32:11, C3P1 1:03:18, C3P1 1:15:19

Karim trabaja en Colab: "Archivo, guardar una copia en Drive", entorno con CPU gratis, celdas con Ctrl+Enter C1P1 1:15:52. La notebook 00 lee el CSV crudo de Sysarmy, que trae filas basura arriba, y renombra las preguntas largas a nombres cortos con un prefijo por categoría (`work_`, `salary_`, `profile_`) C1P1 1:36:24, C1P1 1:41:04. Las notebooks siguientes ya leen el CSV procesado del repositorio.

Qué tenés que hacer:
- Si leés un CSV crudo, configurá `skiprows` y `header` mirando el archivo; no adivines.
- Al renombrar, avisá si alguna columna esperada no está (las encuestas cambian las preguntas entre ediciones).
- Mirá tipos, faltantes y rangos antes de graficar. En pandas 3 las columnas de texto salen con dtype `str` en lugar de `object`.
- Recodificá género con `map` desde las categorías que realmente tiene el CSV y verificá los conteos.
- Definí las ordinales (nivel de estudios) como `Categorical` ordenado, y recordá que el nivel no dice si está terminado: para eso está `profile_studies_level_state`.

```python
# g00_lectura_cruda.py
# Leer un CSV "crudo" con filas de encabezado basura y renombrar columnas con prefijos
# (reproduce la lógica del nb00 con un archivo de juguete, porque el CSV crudo de
#  Sysarmy no está en el repo de la materia)
import io
import pandas as pd

crudo = "\n".join(
    ["Para analizar los resultados podés bajar el .csv,,"] + [",,"] * 7 +      # 8 filas basura
    ["(fila en blanco del formulario),,",
     "donde_estas_trabajando,ultimo_salario_mensual_o_retiro_bruto_en_pesos_argentinos,genero",
     "Mendoza,3000000,Mujer Cis",
     "Santa Fe,5000000,Hombre Cis"])

# Sin configurar: la "tabla" sale mal
print(pd.read_csv(io.StringIO(crudo)).shape)

# skiprows=range(8) saltea las 8 primeras filas; header=1 toma como nombres la
# SEGUNDA de las filas que quedan (la primera es la fila en blanco)
df = pd.read_csv(io.StringIO(crudo), skiprows=range(8), header=1)
print(df)

# Renombrar: diccionario por categoría -> prefijo_nombre (función del nb00)
new_columns = {
    "work": {"donde_estas_trabajando": "province"},
    "salary": {"ultimo_salario_mensual_o_retiro_bruto_en_pesos_argentinos": "monthly_BRUTO"},
    "profile": {"genero": "gender"},
}
def replace_columns(df, new_columns):
    nombres = {orig: f"{cat}_{nuevo}"
               for cat, cols in new_columns.items() for orig, nuevo in cols.items()}
    faltan = set(nombres) - set(df.columns)
    if faltan:                                   # avisa si una pregunta cambió de nombre
        print("ojo, columnas que no están:", faltan)
    return df.rename(columns=nombres)

df = replace_columns(df, new_columns)
print(df.columns.tolist())
print(df.salary_monthly_BRUTO.mean())           # con nombres cortos se accede como atributo
```

Lo que da en el box: sin configurar, `read_csv` arma una tabla de 11 × 3 llena de basura; con `skiprows=range(8), header=1` quedan las dos filas de datos con los nombres correctos. La duda de Karim sobre cuántas filas saltear C1P1 1:33:03 se resuelve así: `range(8)` saltea las ocho primeras y `header=1` toma la segunda de las que quedan, porque hay una fila en blanco en el medio.

```python
# g01_lectura.py
# Leer la encuesta Sysarmy 2026 procesada y dejarla lista para trabajar
from pathlib import Path
import pandas as pd

URL = ("https://raw.githubusercontent.com/DiploDatos/AnalisisyVisualizacion/"
       "refs/heads/master/sysarmy_survey_2026_processed.csv")
LOCAL = Path("/workspace/yt/ayvd_repo/sysarmy_survey_2026_processed.csv")

# En Colab usá directamente pd.read_csv(URL); acá leo la copia local del repo
df = pd.read_csv(LOCAL if LOCAL.exists() else URL)
print("filas, columnas:", df.shape)

# 1. Tipos: el tipo de dato de pandas no es el tipo de variable aleatoria
print(df[["work_province", "salary_monthly_BRUTO", "salary_monthly_NETO",
          "profile_age", "salary_satisfaction"]].dtypes)

# 2. Faltantes por columna (proporción), las 5 peores entre las que usamos
cols = ["salary_monthly_BRUTO", "salary_monthly_NETO", "profile_age",
        "profile_gender", "profile_studies_level", "profile_years_experience"]
print(df[cols].isna().mean().sort_values(ascending=False).round(3))

# 3. Rangos sospechosos: edad 999, neto de 1,6 pesos o 653 millones
print(df[["salary_monthly_BRUTO", "salary_monthly_NETO", "profile_age"]]
      .describe().loc[["count", "min", "50%", "max"]])
print("neto > bruto:", (df.salary_monthly_NETO > df.salary_monthly_BRUTO).sum())

# 4. Recodificar género SIN el bug del notebook 03 (que mapea 'Varón Cis',
#    categoría que no existe en 2026, y deja vacío el grupo de varones)
print(df.profile_gender.value_counts(dropna=False))
mapa = {"Hombre Cis": "Varón cis", "Mujer Cis": "Mujer cis",
        "No binarie": "Diversidades", "Queer": "Diversidades",
        "Trans": "Diversidades", "Agénero": "Diversidades"}
df["profile_g"] = df.profile_gender.map(mapa)   # lo que no está en el mapa queda NaN
print(df.profile_g.value_counts(dropna=False))

# Chequeo del bug: con el diccionario del notebook 03 no queda ningún varón
bug = df.profile_gender.replace({"Varón Cis": "Varón cis", "Mujer Cis": "Mujer cis"})
print("varones con el mapa del nb03:", (bug == "Varón cis").sum())

# 5. Variable ordinal: nivel de estudios con orden explícito
orden = ["Secundario", "Terciario", "Universitario", "Posgrado/Especialización",
         "Maestría", "Doctorado", "Posdoctorado"]
df["studies"] = pd.Categorical(df.profile_studies_level, categories=orden, ordered=True)
print(df.studies.value_counts(sort=False, dropna=False))
# El nivel NO es solo "terminado": hay una columna de estado aparte
print(pd.crosstab(df.studies, df.profile_studies_level_state))

# 6. Guardar una versión limpia mínima para los scripts siguientes
df.to_pickle("/workspace/yt/guia_code_ayvd/sysarmy2026.pkl")
```

Lo que da en el box:
- 4939 filas y 60 columnas. `work_province` sale como `str`; los salarios, `float64`; edad y satisfacción, `int64`.
- Faltantes: el 64,3% no respondió el nivel de estudios y el 4,5% no dio el neto.
- Rangos imposibles: neto mínimo 1,6 pesos y máximo 653.388.190; edad máxima 999; 161 filas con neto mayor que bruto.
- Género: `Hombre Cis` 3861, `Mujer Cis` 983, `Prefiero no decir` 52, `No binarie` 22, `Queer` 11, `Trans` 8, `Agénero` 1. Recodificado: varones cis 3861, mujeres cis 983, diversidades 42 y 53 sin dato.
- **Bug de la notebook 03:** su `replace` mapea `'Varón Cis'`, que en 2026 no existe; con ese diccionario quedan 0 varones y el gráfico de varones contra mujeres solo dibuja mujeres. La notebook 04 sí usa `'Hombre Cis'`.
- Estudios: de los 1175 universitarios, 590 completos, 317 en curso y 268 incompletos. En clase se dijo que "son terminados" C3P1 1:15:19: no es así.

### 2. Gráficos de una variable (notebook 01, parte A)
**En clase:** C1P2 48:46, C1P2 52:17, C1P2 57:48, C1P2 1:00:40, C1P2 1:01:13, C1P2 1:05:19, C1P2 1:07:01, C1P2 1:10:23, C1P2 1:23:53, C2P1 30:30, C2P1 34:31, V05 3:22, V05 8:22

La notebook 01 toma el neto, corta en 40 millones y recorre histogramas, conteos de provincias, edades, género y nivel de estudios, y cierra con dos gráficos mal elegidos a propósito para discutir.

Qué tenés que hacer:
- Elegí el `stat` del histograma sabiendo qué representa: `count` (conteos), `probability` (las alturas suman 1), `density` (el área suma 1, para superponer una densidad). `frequency` es conteo dividido por ancho de bin.
- Guardá la figura en la misma celda, o mejor con el objeto `fig`.
- Ordená las barras de las categóricas y ponelas horizontales si las etiquetas son largas.
- Para variables enteras como la edad, usá `discrete=True` o menos bins que valores distintos.
- Booleanos y categóricas van en barras; el gráfico de líneas solo para una x numérica con continuidad.

```python
# g02_graficos_univariados.py
# Gráficos de una variable: histogramas, stat de seaborn, conteos ordenados y savefig
import matplotlib
matplotlib.use("Agg")            # en Colab no hace falta
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from PIL import Image

df = pd.read_pickle("/workspace/yt/guia_code_ayvd/sysarmy2026.pkl")
FIG = "/workspace/yt/guia_code_ayvd/fig/"
neto = df.loc[df.salary_monthly_NETO < 40e6, "salary_monthly_NETO"]   # corte del nb01

# 1. Qué devuelve cada stat de histplot (lo que en clase se confundió)
for stat in ["count", "frequency", "probability", "density"]:
    ax = sns.histplot(neto, bins=200, stat=stat)
    alturas = np.array([p.get_height() for p in ax.patches])
    ancho = ax.patches[0].get_width()
    print(f"{stat:12s} suma alturas={alturas.sum():.6g}  suma alturas*ancho={(alturas*ancho).sum():.6g}")
    plt.close()

# 2. savefig: en la MISMA celda que el gráfico, o con el objeto figura
fig, ax = plt.subplots(figsize=(8, 3))
sns.histplot(neto, bins=60, ax=ax, color="gray")
ax.axvline(neto.mean(), color="orangered", ls="--", label="media")
ax.axvline(neto.median(), color="indigo", ls="-.", label="mediana")
ax.ticklabel_format(style="plain", axis="x")
ax.legend()
fig.savefig(FIG + "neto_hist.png", dpi=80, bbox_inches="tight")
plt.close(fig)
# Simulación de "savefig en otra celda": en Colab la figura ya se mostró y se cerró
plt.figure(); plt.close("all")
plt.savefig(FIG + "vacia.png", dpi=80)                # figura nueva, vacía
for f in ["neto_hist.png", "vacia.png"]:
    a = np.asarray(Image.open(FIG + f).convert("L"))
    print(f, "píxeles distintos de blanco:", int((a < 250).sum()))

# 3. Conteo de una categórica, ordenado por frecuencia y horizontal
fig, ax = plt.subplots(figsize=(6, 6))
orden = df.work_province.value_counts().index
sns.countplot(y=df.work_province, order=orden, color="steelblue", ax=ax)
fig.savefig(FIG + "provincias.png", dpi=80, bbox_inches="tight"); plt.close(fig)
print(df.work_province.value_counts().head(3))

# 4. Edad: filtrar el 999 y elegir bins (más bins que valores enteros = "peine")
edad = df.profile_age[df.profile_age < 70]
print("edades distintas:", edad.nunique(), " rango:", edad.min(), edad.max())
fig, axs = plt.subplots(1, 3, figsize=(12, 3))
for ax, b in zip(axs, [200, edad.max() - edad.min() + 1, 10]):
    sns.histplot(edad, bins=b, ax=ax); ax.set_title(f"bins={b}")
fig.savefig(FIG + "edad_bins.png", dpi=80, bbox_inches="tight"); plt.close(fig)
# Para enteros, discrete=True centra una barra por valor
fig, ax = plt.subplots(figsize=(8, 3))
sns.histplot(edad, discrete=True, ax=ax)
fig.savefig(FIG + "edad_discrete.png", dpi=80, bbox_inches="tight"); plt.close(fig)

# 5. Los dos gráficos "incorrectos" del nb01, bien hechos
df["usd"] = df.salary_in_usd.notna()       # True si cobra algo en dólares (o dolarizado)
print(df.salary_in_usd.value_counts(dropna=False))
fig, axs = plt.subplots(1, 2, figsize=(11, 3))
sns.countplot(x=df.usd, ax=axs[0])          # booleano: barras, no histograma
cnt = df.work_province.value_counts().head(8)
sns.barplot(x=cnt.values, y=cnt.index, ax=axs[1], color="steelblue")  # no lineplot
fig.savefig(FIG + "correctos.png", dpi=80, bbox_inches="tight"); plt.close(fig)
print("ok figuras")
```

Lo que da en el box (neto menor a 40 millones, 4709 valores, 200 bins):
- `count`: las alturas suman 4709. `frequency`: suman 0,026, y alturas por ancho dan 4709. `probability`: suman 1. `density`: alturas por ancho dan 1. Karim dijo que `frequency` era "la proporción" y que "la suma me da uno" C1P2 57:48, C1P2 1:00:40: eso es `probability`.
- La figura guardada con `fig.savefig` tiene 13.594 píxeles no blancos; la que imita "savefig en otra celda", 0: está en blanco, como le pasó a la clase C2P1 30:30.
- Provincias: CABA 2476, Buenos Aires 1064, Córdoba 447.
- Edad filtrada: de 16 a 69 años, 53 valores distintos; con 200 bins aparece el "peine" que en clase llamaron estegosaurio C1P2 1:07:01.
- `salary_in_usd` tiene 3356 vacíos (cobran en pesos), 737 que cobran todo en dólares, 493 una parte y 353 dolarizados: el booleano "cobra algo en dólares" va en un `countplot`.

### 3. Probabilidad con los datos (notebook 01, parte B)
**En clase:** C2P1 53:44, C2P1 56:30, C2P1 1:07:50, C2P1 1:12:12, C2P1 1:19:40, C2P1 1:21:52, C2P1 1:28:33, C2P2 17:31, C2P2 21:48

Con Laplace, Ω son las filas y la probabilidad de un evento es la proporción de filas que lo cumplen. La notebook define A = "el neto es mayor o igual al promedio" y B = "más de 5 años de experiencia" y compara P(A | B) con P(A).

Qué tenés que hacer:
- Calculá probabilidades como medias de columnas booleanas (`(A & B).mean()`).
- No decidas independencia mirando si dos números "se parecen": con datos nunca da exacto. Usá un test chi cuadrado de independencia sobre la tabla de contingencia.
- La probabilidad total lleva pesos: Σ P(A | Bᵢ) P(Bᵢ).
- Simulá experimentos chicos (tres monedas) con numpy y compará con la distribución exacta.

```python
# g03_probabilidad.py
# Probabilidad empírica, condicional, independencia, Bayes y probabilidad total
import numpy as np
import pandas as pd
from scipy import stats

df = pd.read_pickle("/workspace/yt/guia_code_ayvd/sysarmy2026.pkl")
df1 = df[df.salary_monthly_NETO < 40e6]          # como el nb01 (descarta NaN y extremos)
print("n =", len(df1))

# Laplace sobre "los que contestaron": P(A) = |A| / |Omega|
media = df1.salary_monthly_NETO.mean()
A = df1.salary_monthly_NETO >= media             # cobra al menos el promedio
B = df1.profile_years_experience > 5             # más de 5 años de experiencia
pA, pB, pAB = A.mean(), B.mean(), (A & B).mean()
print(f"media={media:,.0f}  mediana={df1.salary_monthly_NETO.median():,.0f}")
print(f"P(A)={pA:.4f}  P(B)={pB:.4f}  P(A∩B)={pAB:.4f}")
print(f"P(A|B)={pAB/pB:.4f}  P(A|no B)={(A & ~B).mean()/(1-pB):.4f}")
print(f"P(A)P(B)={pA*pB:.4f}  (independencia exigiría P(A∩B) = P(A)P(B))")

# P(A) ≈ 0,375 y no 0,5 porque la media queda a la derecha de la mediana
print("P(neto >= mediana) =", round((df1.salary_monthly_NETO >= df1.salary_monthly_NETO.median()).mean(), 4))

# ¿Es "casi igual" o distinto? Test chi cuadrado de independencia en la tabla 2x2
tabla = pd.crosstab(A, B)
chi2, p, dof, esperadas = stats.chi2_contingency(tabla)
print(tabla); print(f"chi2={chi2:.1f}  p={p:.2e}  gl={dof}")

# Bayes: P(B|A) = P(A|B) P(B) / P(A)
print(f"P(B|A) por Bayes={(pAB/pB)*pB/pA:.4f}  directo={(A & B).sum()/A.sum():.4f}")

# Probabilidad total con pesos: P(A) = sum_i P(A|Bi) P(Bi)
niveles = pd.cut(df1.profile_years_experience, [-1, 2, 5, 10, 100],
                 labels=["0-2", "3-5", "6-10", "+10"])
pBi = niveles.value_counts(normalize=True).sort_index()
pA_Bi = A.groupby(niveles, observed=True).mean()
print(pd.DataFrame({"P(Bi)": pBi.round(3), "P(A|Bi)": pA_Bi.round(3)}))
print("suma P(A|Bi)P(Bi) =", round((pBi * pA_Bi).sum(), 4), " P(A) =", round(pA, 4))
print("suma SIN pesos (error dicho en clase) =", round(pA_Bi.sum(), 4))

# Moneda: X = caras en 3 tiradas, exacta vs simulada (1000 y 10000 repeticiones)
rng = np.random.default_rng(0)
exacta = stats.binom.pmf(range(4), 3, 0.5)
for m in [1000, 10000]:
    sim = np.bincount(rng.binomial(3, 0.5, size=m), minlength=4) / m
    print(m, "simulada", sim.round(3), " exacta", exacta.round(3))
```

Lo que da en el box:
- n = 4709, media del neto 3.270.653, mediana 2.748.626. Como la media queda a la derecha de la mediana, P(A) = 0,3755, no 0,5. En clase se leyó P(A | B) como "cobrar más que el 50%" y se ubicó la media a la izquierda de la mediana C2P1 1:19:40, C2P1 1:21:52: las dos cosas están mal.
- P(B) = 0,5817, P(A ∩ B) = 0,3054, P(A | B) = 0,5250 y P(A | no B) = 0,1675. Si fueran independientes, P(A ∩ B) sería P(A) P(B) = 0,2184. Chi cuadrado 623, p = 1,7 × 10⁻¹³⁷: no son independientes.
- Bayes: P(B | A) = 0,8133, igual al cálculo directo.
- Probabilidad total con cuatro tramos de experiencia: la suma ponderada da 0,3755, exactamente P(A). La suma sin pesos, como se enunció en clase C2P1 1:28:33, da 1,2893, que ni siquiera es una probabilidad.
- Tres monedas: con 1000 simulaciones las frecuencias son 0,110, 0,363, 0,402 y 0,125; con 10.000, 0,128, 0,376, 0,376 y 0,120; la exacta es 1/8, 3/8, 3/8 y 1/8.

### 4. Estadística descriptiva, percentiles y outliers (notebook 02)
**En clase:** C2P2 1:45, C2P2 4:04, C2P2 7:28, C2P2 9:12, C2P2 10:20, C2P2 14:13, C2P2 1:01:49, C2P2 1:05:15, C2P2 1:09:30, C2P2 1:11:12, C2P2 1:13:35, C2P2 1:24:10, C2P2 1:28:46, C3P1 1:02:12, C3P1 1:07:25, C3P1 1:29:21, V04 0:34, V04 2:12, V04 3:52, V04 4:59

La notebook 02 pasa al bruto (sin faltantes, de 200.000 a 20 millones) y recorre media, mediana, desvío, percentiles, boxplots por nivel de estudios y dos funciones para sacar outliers: `clean_outliers_q3` (se queda con lo menor o igual a 2,5 × Q3) y `clean_outliers_sd` (a menos de 2,5 desvíos de la media).

Qué tenés que hacer:
- Reportá media y mediana juntas y mirá cómo cambian con cada corte: truncar a la izquierda de la cola invierte el orden.
- Fijate qué `ddof` usa cada librería: pandas divide por n − 1 y numpy por n.
- Usá la regla de Tukey (fuera de Q1 − 1,5 IQR o Q3 + 1,5 IQR es atípico; fuera de 3 IQR, extremo) y compará con otras reglas antes de decidir.
- Los boxplots por grupo, con el orden ordinal y mirando el n de cada grupo (6 posdoctorados no se comparan con 1175 universitarios).
- Informá siempre cuántas filas sacás y con qué criterio.

```python
# g04_descriptiva.py
# Estadística descriptiva: centro, dispersión, percentiles, outliers y estandarización
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats

df = pd.read_pickle("/workspace/yt/guia_code_ayvd/sysarmy2026.pkl")
FIG = "/workspace/yt/guia_code_ayvd/fig/"
bruto = df.salary_monthly_BRUTO
neto = df.salary_monthly_NETO.dropna()

# 1. Media vs mediana según dónde cortes (truncar a la izquierda invierte el orden)
for corte in [20e6 + 1, 10e6, 5e6, 3e6, 2e6]:
    x = bruto[bruto < corte]
    print(f"corte {corte/1e6:>5.1f}M  n={len(x):4d}  media={x.mean():>12,.0f}  mediana={x.median():>12,.0f}")

# 2. Dispersión: desvío con ddof, coeficiente de variación
print("pandas std (ddof=1):", round(bruto.std(), 1), " numpy std (ddof=0):", round(np.std(bruto), 1))
print("CV bruto:", round(stats.variation(bruto), 3), " CV neto:", round(stats.variation(neto), 3))
neto_ok = neto[(neto > 100_000) & (neto < 40e6)]
print("CV neto sin extremos:", round(stats.variation(neto_ok), 3))

# 3. Robustez: un solo dato absurdo mueve la media y el desvío, no la mediana ni el IQR
x = bruto.copy()
x.iloc[0] = 653_388_190
for nombre, f in [("media", np.mean), ("mediana", np.median), ("std", np.std),
                  ("IQR", lambda s: np.subtract(*np.percentile(s, [75, 25])))]:
    print(f"{nombre:8s} original={f(bruto):>14,.0f}  con 1 outlier={f(x):>14,.0f}")

# 4. Percentiles
print(bruto.quantile([.25, .5, .75, .9, .95, .98, .99]).apply(lambda v: f"{v:,.0f}"))

# 5. Tres reglas de outliers: Tukey (1,5 IQR), la del nb02 (2,5*Q3) y 2,5 desvíos
q1, q3 = bruto.quantile([.25, .75]); iqr = q3 - q1
reglas = {
    "Tukey 1,5 IQR": (bruto < q1 - 1.5 * iqr) | (bruto > q3 + 1.5 * iqr),
    "Tukey 3 IQR (extremos)": (bruto < q1 - 3 * iqr) | (bruto > q3 + 3 * iqr),
    "nb02: > 2,5*Q3": bruto > 2.5 * q3,
    "nb02: |x-media| > 2,5 sd": (bruto - bruto.mean()).abs() > 2.5 * bruto.std(),
}
print(f"Q1={q1:,.0f} Q3={q3:,.0f} IQR={iqr:,.0f} bigote sup={q3+1.5*iqr:,.0f}")
for k, m in reglas.items():
    print(f"{k:26s} marca {m.sum():4d} filas ({m.mean():.1%})")

# 6. Boxplot y boxenplot por nivel de estudios (orden ordinal y n por grupo)
orden = list(df.studies.cat.categories)
fig, axs = plt.subplots(1, 2, figsize=(13, 4), sharey=True)
sns.boxplot(data=df, x="salary_monthly_BRUTO", y="studies", order=orden, ax=axs[0], color="orangered")
sns.boxenplot(data=df, x="salary_monthly_BRUTO", y="studies", order=orden, ax=axs[1], color="orangered")
for ax in axs: ax.ticklabel_format(style="plain", axis="x")
fig.savefig(FIG + "box_estudios.png", dpi=80, bbox_inches="tight"); plt.close(fig)
print(df.groupby("studies", observed=True).salary_monthly_BRUTO.agg(["count", "median"]).round(0))

# 7. Estandarizar: z-score y min-max (se divide por max - min, no por max)
v = bruto.to_numpy()
z = (v - v.mean()) / v.std(ddof=1)
mm = (v - v.min()) / (v.max() - v.min())
mal = (v - v.min()) / v.max()
print(f"z: media={z.mean():.2e} sd={z.std(ddof=1):.3f} min={z.min():.2f} max={z.max():.2f}")
print(f"min-max: [{mm.min():.3f}, {mm.max():.3f}]   dividido por max (mal): [{mal.min():.3f}, {mal.max():.3f}]")
# Con scikit-learn (lo que van a usar en las materias siguientes)
from sklearn.preprocessing import MinMaxScaler, StandardScaler
print(StandardScaler().fit_transform(v.reshape(-1, 1)).std().round(3),
      MinMaxScaler().fit_transform(v.reshape(-1, 1)).max())
```

Lo que da en el box:
- Media contra mediana según el corte del bruto: hasta 20 M (sin cortar), 3.876.029 contra 3.268.000; hasta 10 M, 3.590.552 contra 3.194.286; hasta 5 M, 2.752.302 contra 2.700.000; hasta 3 M (quedan 2132 filas, se va el 57%), 1.951.557 contra 2.000.000; hasta 2 M, 1.389.450 contra 1.469.000.
- Desvío del bruto: 2.492.699 con pandas y 2.492.447 con numpy. Coeficiente de variación: bruto 0,643, neto 3,289 (por los outliers) y neto sin extremos 0,722.
- Reemplazando un solo bruto por 653.388.190 (el neto absurdo del dataset): la media pasa de 3.876.029 a 4.007.713 y el desvío (numpy) de 2,49 M a 9,57 M; la mediana pasa de 3.268.000 a 3.270.000 y el IQR casi no cambia.
- Percentiles: Q1 2.166.336, mediana 3.268.000, Q3 4.944.960, p90 7.000.000, p95 8.700.000, p98 11.000.000, p99 12.978.340. IQR 2.778.624 y bigote superior 9.112.897. En clase se leyó "outliers por encima de unos 7,5 millones" C2P2 1:11:12: el bigote está en 9,1 M.
- Filas marcadas por cada regla: Tukey 1,5 IQR 202 (4,1%); Tukey 3 IQR 39 (0,8%); 2,5 × Q3 de la notebook 61 (1,2%); 2,5 desvíos 142 (2,9%). La regla de la notebook y de V04 V04 3:52 no es la de Tukey, y la clase mezcló "1,5", "2 o 3" y "3 veces el IQR" C2P2 9:12, C3P1 1:29:21.
- Medianas del bruto por nivel de estudios: secundario 2.450.000 (n = 65), terciario 2.500.000 (272), universitario 3.420.000 (1175), posgrado 4.000.000 (108), maestría 4.269.477 (108), doctorado 4.800.000 (27), posdoctorado 4.000.000 (6). El doctorado tiene la mediana más alta, no la maestría C2P2 1:13:35.
- En la notebook, `central_tendency_max` usa `range(1500000, max, 10**7)` y genera solo dos puntos; con un paso de 500.000 se ve la tendencia.

### 5. Distribuciones y estandarización
**En clase:** C2P2 17:31, C2P2 27:22, C2P2 30:18, C2P2 37:31, C2P2 38:10, C2P2 40:29, C2P2 43:49, C2P2 44:54, C2P2 47:38, C2P2 51:05, C4P2 40:26

Georgina presenta binomial, uniforme, normal, exponencial y chi cuadrado, la estandarización y la diferencia entre varianza poblacional y muestral. No hay notebook específica; el código de abajo hace con `scipy.stats` lo que se dibujó en las filminas.

Qué tenés que hacer:
- Usá `scipy.stats` (`norm`, `binom`, `uniform`, `expon`, `chi2`) con `cdf`, `ppf`, `rvs`, `mean` y `var` en lugar de tablas.
- Leé la parametrización: en scipy la exponencial va con `scale = 1/λ` y todas tienen `loc` y `scale` C4P2 40:26.
- Antes de aproximar una binomial con la normal, mirá n·p y n·(1 − p), no solo n.
- Estandarizá con z score o min max correcto; en las materias siguientes, con `StandardScaler` y `MinMaxScaler` de scikit-learn ajustados solo con los datos de entrenamiento.

```python
# g05_distribuciones.py
# Distribuciones: normal (68-95-99,7), binomial y su aproximación normal,
# uniforme, exponencial (ojo con la parametrización de scipy) y chi cuadrado
import numpy as np
from scipy import stats

# 1. Regla empírica de la normal
for k in [1, 2, 3]:
    print(f"P(|Z| < {k}) = {stats.norm.cdf(k) - stats.norm.cdf(-k):.4f}")
print("z para 95% bilateral:", round(stats.norm.ppf(0.975), 4))

# 2. Binomial y aproximación normal (De Moivre Laplace): depende de n*p, no solo de n
for n, p in [(100, 0.5), (100, 0.05), (1000, 0.05)]:
    k = int(n * p + 2 * np.sqrt(n * p * (1 - p)))       # un valor en la cola derecha
    exacta = stats.binom.cdf(k, n, p)
    aprox = stats.norm.cdf(k + 0.5, n * p, np.sqrt(n * p * (1 - p)))   # corrección por continuidad
    print(f"n={n:4d} p={p:.2f} np={n*p:5.1f}  P(X<={k}) exacta={exacta:.4f}  normal={aprox:.4f}")

# 3. Uniforme continua en [a, b]: P(c < X < d) = (d - c)/(b - a)
print("Uniforme[0,10], P(2<X<5) =", stats.uniform(loc=0, scale=10).cdf(5) - stats.uniform(loc=0, scale=10).cdf(2))

# 4. Exponencial: scipy usa scale = 1/lambda (media), no lambda
lam = 3.0
e1 = stats.expon(scale=1 / lam)       # correcto: media 1/3
e2 = stats.expon(scale=lam)           # error típico: media 3
print("media con scale=1/λ:", round(e1.mean(), 4), " media con scale=λ:", e2.mean())
print("expon(loc=5, scale=2): media", stats.expon(loc=5, scale=2).mean(), " var", stats.expon(loc=5, scale=2).var())

# 5. Chi cuadrado: suma de k normales estándar al cuadrado
rng = np.random.default_rng(1)
k = 4
s = (rng.standard_normal((100_000, k)) ** 2).sum(axis=1)
print(f"chi2({k}) simulada: media={s.mean():.3f} var={s.var():.3f}  teórica: {k}, {2*k}")

# 6. (n-1)S^2/sigma^2 ~ chi2(n-1) para muestras normales
n, sigma = 10, 2.0
S2 = rng.normal(0, sigma, (50_000, n)).var(axis=1, ddof=1)
q = (n - 1) * S2 / sigma**2
print("percentil 95 simulado:", round(np.percentile(q, 95), 3), " teórico:", round(stats.chi2.ppf(0.95, n - 1), 3))

# 7. Asimetría y curtosis (exceso) del salario bruto vs una normal
import pandas as pd
b = pd.read_pickle("/workspace/yt/guia_code_ayvd/sysarmy2026.pkl").salary_monthly_BRUTO
print("asimetría bruto:", round(stats.skew(b), 2), " curtosis (exceso):", round(stats.kurtosis(b), 2))
print("log(bruto): asimetría", round(stats.skew(np.log(b)), 2))
```

Lo que da en el box:
- Normal: P(|Z| < 1) = 0,6827, P(|Z| < 2) = 0,9545, P(|Z| < 3) = 0,9973; z para 95% bilateral = 1,96. En clase se dijo "63... 68" y "99,5" para tres desvíos C2P2 40:29, C2P2 56:03.
- Binomial contra normal: con n = 100 y p = 0,5 (n·p = 50), 0,9824 exacta contra 0,9821 aproximada; con n = 100 y p = 0,05 (n·p = 5), 0,9718 contra 0,9805: con 100 personas no siempre "ya es normal" C2P2 37:31. Con n = 1000 y p = 0,05, 0,9716 contra 0,9749.
- Uniforme en [0, 10]: P(2 < X < 5) = 0,3.
- Exponencial con λ = 3: con `scale=1/3` la media es 0,333; con `scale=3`, 3. `expon(loc=5, scale=2)` (la de la notebook 04) tiene media 7 y varianza 4.
- Chi cuadrado con 4 grados de libertad simulada como suma de cuadrados de normales: media 3,985 y varianza 8,018 (teóricas 4 y 8); percentil 95 simulado 16,94 contra 16,92.
- Asimetría del bruto 1,71 y curtosis en exceso 4,26; el logaritmo del bruto tiene asimetría −0,37.
- Estandarizado del bruto (en el script de la sección 4): z con media 0 y desvío 1, de −1,47 a 6,47; min max en [0, 1]; dividiendo por el máximo, como se explicó en clase C2P2 47:38, queda en [0; 0,990].

### 6. Varias variables (notebook 03)
**En clase:** C2P2 1:36:37, C2P2 1:39:20, C3P1 28:16, C3P1 29:24, C3P1 38:31, C3P1 50:22, C3P1 52:06, C3P1 58:51, C3P1 1:03:18, C3P1 1:11:46, C3P1 1:17:37, C3P1 1:22:08, C3P1 1:32:08, C3P1 1:34:22, C3P1 1:35:26, C3P1 1:39:25

Karim filtra bruto y edad, cruza provincia con estudios en una tabla de contingencia y un heatmap, dibuja `pairplot`, `jointplot` hexagonal y KDE con `hue`, y deja como práctico la relación entre bruto y neto con una columna de descuentos.

Qué tenés que hacer:
- `pd.crosstab` con `normalize=True` da proporciones conjuntas; con `normalize="index"`, condicionales por fila (lo que sirve para comparar provincias de distinto tamaño).
- Calculá Pearson, Spearman y Kendall juntos: si Pearson y Spearman difieren mucho, mirá los outliers.
- Recordá que correlación cero no implica independencia, y que tener marginales normales no hace normal al vector.
- Para una ordinal contra un sueldo, boxplots o medianas por nivel, no `pairplot`.
- Filtrá con `.copy()` antes de crear columnas nuevas, para evitar el `SettingWithCopyWarning`.

```python
# g06_varias_variables.py
# Varias variables: tablas de contingencia, heatmap, covarianza y correlación,
# correlación sin dependencia lineal, y gráficos de dos o tres variables
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats

df = pd.read_pickle("/workspace/yt/guia_code_ayvd/sysarmy2026.pkl")
FIG = "/workspace/yt/guia_code_ayvd/fig/"
df = df[(df.salary_monthly_BRUTO <= 100e6) & (df.profile_age <= 100)].copy()  # filtros del nb03
orden = list(df.studies.cat.categories)

# 1. Tabla de contingencia: conteos, proporciones conjuntas y condicionales por fila
top = df.work_province.value_counts().index[:5]
sub = df[df.work_province.isin(top)]
ct = pd.crosstab(sub.work_province, sub.studies)
print(ct)
print(pd.crosstab(sub.work_province, sub.studies, normalize=True).round(3).iloc[:, :3])   # suma 1 toda la tabla
print(pd.crosstab(sub.work_province, sub.studies, normalize="index").round(3).iloc[:, :3])  # cada fila suma 1
fig, ax = plt.subplots(figsize=(8, 3))
sns.heatmap(ct, annot=True, fmt="g", cmap="viridis", ax=ax)
fig.savefig(FIG + "heatmap_prov_estudios.png", dpi=80, bbox_inches="tight"); plt.close(fig)

# 2. Covarianza y correlación bruto vs neto: el resultado depende de los outliers
d = df.dropna(subset=["salary_monthly_NETO"])
filtros = {
    "sin filtro": d,
    "neto < 15M": d[d.salary_monthly_NETO < 15e6],
    "ambos < 2,5M (práctico nb03)": d[(d.salary_monthly_BRUTO < 2.5e6) & (d.salary_monthly_NETO < 2.5e6)],
}
for k, x in filtros.items():
    b, n_ = x.salary_monthly_BRUTO, x.salary_monthly_NETO
    print(f"{k:30s} n={len(x):4d} pearson={stats.pearsonr(b, n_)[0]:.3f} "
          f"spearman={stats.spearmanr(b, n_)[0]:.3f} kendall={stats.kendalltau(b, n_)[0]:.3f}")
lim = filtros["ambos < 2,5M (práctico nb03)"].copy()
lim["descuentos"] = lim.salary_monthly_BRUTO - lim.salary_monthly_NETO    # con .copy() no hay warning
print("descuentos: media", round(lim.descuentos.mean()), " mín", lim.descuentos.min(),
      " negativos", (lim.descuentos < 0).sum())
print(np.cov(lim.salary_monthly_BRUTO, lim.salary_monthly_NETO).round(-6))

# 3. Var(X + Y) = Var X + Var Y + 2 Cov(X, Y)  (no "menos")
X, Y = lim.salary_monthly_BRUTO, lim.salary_monthly_NETO
print("Var(X+Y)", f"{(X + Y).var():.4e}", " VarX+VarY+2Cov", f"{X.var() + Y.var() + 2 * X.cov(Y):.4e}")
print("Var(X-Y)", f"{(X - Y).var():.4e}", " VarX+VarY-2Cov", f"{X.var() + Y.var() - 2 * X.cov(Y):.4e}")

# 4. Correlación cero con dependencia total (círculo) e independencia de verdad
rng = np.random.default_rng(0)
t = rng.uniform(0, 2 * np.pi, 2000)
cx, cy = np.cos(t), np.sin(t)
print("círculo: r =", round(np.corrcoef(cx, cy)[0, 1], 3), " pero x² + y² = 1 siempre")
u = rng.normal(size=2000); w = u**2
print("y = x²: r =", round(np.corrcoef(u, w)[0, 1], 3))

# 5. Normal bivariada: misma marginal, distinta correlación
for rho in [0, 0.8, -0.8]:
    cov = [[1, rho], [rho, 1]]
    s = rng.multivariate_normal([0, 0], cov, 5000)
    print(f"rho={rho:+.1f} r muestral={np.corrcoef(s.T)[0,1]:+.3f}")
# Marginales normales NO alcanzan: Y = S*X con S = ±1 tiene marginal normal pero (X, Y) no es normal bivariada
x = rng.normal(size=100_000); sgn = rng.choice([-1, 1], size=x.size); y = sgn * x
print("X+Y tiene un átomo en 0:", round(np.mean(x + y == 0), 3), "(una normal bivariada daría 0)")

# 6. Satisfacción vs salario: ¿ganan menos los más satisfechos? (no)
print(df[df.profile_age < 70].groupby("salary_satisfaction").salary_monthly_NETO.median())

# 7. Gráficos de dos y tres variables
s = d[(d.salary_monthly_NETO < 15e6) & (d.profile_age < 70)]
g = sns.jointplot(data=s, x="salary_monthly_NETO", y="profile_age", kind="hex", height=5)
g.savefig(FIG + "joint_hex.png", dpi=70); plt.close("all")
fig, ax = plt.subplots(figsize=(7, 4))
sns.boxplot(data=s, x="salary_satisfaction", y="salary_monthly_NETO", ax=ax)
fig.savefig(FIG + "satisfaccion.png", dpi=80, bbox_inches="tight"); plt.close(fig)
g = sns.displot(data=s[s.studies.isin(["Terciario", "Universitario", "Maestría"])],
                x="profile_age", y="salary_monthly_NETO", col="studies", kind="kde", height=3)
g.savefig(FIG + "kde_por_estudio.png", dpi=70); plt.close("all")
print("ok figuras")
```

Lo que da en el box:
- Proporciones condicionales por provincia: el universitario es el 67% en Buenos Aires y en CABA, 64% en Córdoba, 58% en Mendoza y 66% en Santa Fe (sobre quienes respondieron el nivel).
- Correlación bruto y neto: sin filtrar (4715 pares), Pearson 0,201, Spearman 0,950 y Kendall 0,865; con neto menor a 15 M, Pearson 0,947; con los dos menores a 2,5 M como el práctico (1496 pares), Pearson 0,870. Karim dijo "0,61" C3P1 1:40:31: no lo reproduje con ningún filtro razonable.
- Descuentos (bruto menos neto) con ese filtro: media 228.568, mínimo −1.806.217 y 52 filas negativas, que son netos mayores que brutos.
- Var(X + Y) = 8,8661 × 10¹¹ = Var X + Var Y + 2 Cov, y Var(X − Y) = 6,3796 × 10¹⁰ = Var X + Var Y − 2 Cov: el "menos la covarianza" de la clase C3P1 28:49 corresponde a la resta.
- Puntos sobre un círculo: r = −0,009 con x² + y² = 1 siempre; con x normal estándar e y = x²: r = 0,078.
- Normal bivariada con ρ = 0, 0,8 y −0,8: r muestral 0,019, 0,801 y −0,793. El contraejemplo Y = S·X tiene marginales normales, pero X + Y vale 0 en el 50,1% de los casos, algo imposible en una normal bivariada C3P1 38:31.
- Mediana del neto por satisfacción: 1.650.000 (nivel 1), 2.400.000, 3.200.000 y 4.500.000 (nivel 4). Los más satisfechos ganan más, al revés de lo que se leyó en el `pairplot` C3P1 1:34:22.

### 7. Teorema central del límite e intervalos de confianza (notebook 04)
**En clase:** C3P1 1:50:00, C3P1 1:56:49, C3P2 1:11, C3P2 4:27, C3P2 5:36, C3P2 6:44, C3P2 47:47, C3P2 58:41, C3P2 1:01:28, C3P2 1:08:43, C3P2 1:12:39, C3P2 1:16:03, C3P2 1:20:30, C3P2 1:25:40, C3P2 1:28:35

La notebook 04 arma una matriz de m muestras de tamaño n, toma la media de cada fila y dibuja el histograma de las medias; después calcula intervalos z para una normal simulada, mide la cobertura con 1000 repeticiones y aplica todo al sueldo bruto y a la diferencia entre varones y mujeres.

Qué tenés que hacer:
- Recordá qué es cada cosa en la simulación: n es el tamaño de cada muestra (lo que importa para el TCL) y m es cuántas medias dibujás (solo afina el histograma).
- Con σ desconocida y n chico, usá la t (`stats.t.interval` o el `confidence_interval()` de `ttest_1samp`); con n grande, z y t casi coinciden.
- Para dos grupos independientes, Welch (`ttest_ind(a, b, equal_var=False).confidence_interval()`).
- Si las dos medidas son de la misma persona (bruto y neto), trabajá con la diferencia: `ttest_rel` o `ttest_1samp` de la diferencia.
- Interpretá bien: el 95% es la tasa de acierto del método, no la probabilidad de que μ esté en tu intervalo.

```python
# g07_tcl_ic.py
# TCL (qué hace n y qué hace m), intervalos de confianza z, t, Welch,
# apareado y para la varianza, y cobertura por simulación
import numpy as np
import pandas as pd
from scipy import stats

rng = np.random.default_rng(42)

# 1. TCL: n = tamaño de cada muestra, m = cuántas muestras (cuántas medias dibujás)
#    La forma de la distribución de x̄ depende de n; m solo afina el histograma.
print("Exponencial(media 1): asimetría de x̄ (0 = simétrica, normal)")
for n, m in [(2, 20000), (10, 20000), (100, 20000), (20000, 10), (20000, 1000)]:
    medias = rng.exponential(1.0, size=(m, n)).mean(axis=1)
    print(f"  n={n:6d} m={m:6d}  var(x̄)={medias.var():.5f} (teórica 1/n={1/n:.5f})  "
          f"asimetría={stats.skew(medias):+.3f} (teórica 2/√n={2/np.sqrt(n):.3f})")

# 2. IC z con sigma conocida y cobertura en 1000 repeticiones (nb04, semilla 42)
np.random.seed(42)
mu, sigma, n, m, alpha = 100, 15, 700, 1000, 0.05
z = stats.norm.ppf(1 - alpha / 2)
x = np.random.normal(mu, sigma, n)
print(f"\nx̄={x.mean():.2f}  IC=({x.mean()-z*sigma/np.sqrt(n):.2f}, {x.mean()+z*sigma/np.sqrt(n):.2f})  long={2*z*sigma/np.sqrt(n):.2f}")
cubre = sum(abs(np.random.normal(mu, sigma, n).mean() - mu) <= z * sigma / np.sqrt(n) for _ in range(m))
print("cobertura:", cubre / m, " long con n=4000:", round(2 * z * sigma / np.sqrt(4000), 2))

# 3. IC t con sigma desconocida y n chico: más ancho que z
x10 = rng.normal(5, 1, 10)
se = x10.std(ddof=1) / np.sqrt(10)
print(f"n=10: z crítico={z:.3f}  t crítico(9 gl)={stats.t.ppf(0.975, 9):.3f}")
print("IC t (scipy):", tuple(round(float(v), 3) for v in stats.t.interval(0.95, 9, loc=x10.mean(), scale=se)))
# Cobertura de z vs t con n=10 y sigma estimada
cz = ct = 0
for _ in range(10000):
    s = rng.normal(0, 1, 10); e = s.std(ddof=1) / np.sqrt(10)
    cz += abs(s.mean()) <= z * e; ct += abs(s.mean()) <= stats.t.ppf(0.975, 9) * e
print("cobertura real con n=10:  z+S =", cz / 10000, "  t =", ct / 10000)

# 4. IC para sigma^2 con chi cuadrado (botellas: n = 20)
b = rng.normal(500, 0.4, 20); S2 = b.var(ddof=1)
lo = 19 * S2 / stats.chi2.ppf(0.975, 19); hi = 19 * S2 / stats.chi2.ppf(0.025, 19)
print(f"\nS²={S2:.4f}  IC σ² = ({lo:.4f}, {hi:.4f})  ¿0,15 adentro? {lo <= 0.15 <= hi}")

# 5. Encuesta: IC para la media del salario bruto
df = pd.read_pickle("/workspace/yt/guia_code_ayvd/sysarmy2026.pkl")
br = df.salary_monthly_BRUTO
se = br.std(ddof=1) / np.sqrt(len(br))
print(f"\nbruto: n={len(br)} media={br.mean():,.0f} IC95=({br.mean()-z*se:,.0f}, {br.mean()+z*se:,.0f}) long={2*z*se:,.0f}")

# 6. Diferencia de medias varón cis - mujer cis (Welch), como el nb04 ejercicio 4
h = df.loc[(df.profile_g == "Varón cis") & (df.salary_monthly_BRUTO > 100000), "salary_monthly_BRUTO"]
mu_ = df.loc[(df.profile_g == "Mujer cis") & (df.salary_monthly_BRUTO > 100000), "salary_monthly_BRUTO"]
r = stats.ttest_ind(h, mu_, equal_var=False)
ci = r.confidence_interval(0.95)
print(f"n_h={len(h)} n_m={len(mu_)}  diferencia={h.mean()-mu_.mean():,.0f}  IC95=({ci.low:,.0f}, {ci.high:,.0f})  gl Welch={r.df:.1f}")
print("¿El IC contiene al 0?", ci.low <= 0 <= ci.high)

# 7. Bruto y neto de la MISMA persona: apareado (sobre la diferencia), no Welch
d = df[(df.salary_monthly_NETO > 100000) & (df.salary_monthly_NETO < 15e6)
       & (df.salary_monthly_NETO <= df.salary_monthly_BRUTO)]
dif = d.salary_monthly_BRUTO - d.salary_monthly_NETO
rp = stats.ttest_rel(d.salary_monthly_BRUTO, d.salary_monthly_NETO)
rw = stats.ttest_ind(d.salary_monthly_BRUTO, d.salary_monthly_NETO, equal_var=False)
cp, cw = rp.confidence_interval(), rw.confidence_interval()
print(f"\nn={len(d)}  media de la diferencia={dif.mean():,.0f}")
print(f"apareado: IC=({cp.low:,.0f}, {cp.high:,.0f})  long={cp.high-cp.low:,.0f}")
print(f"Welch (mal planteado): IC=({cw.low:,.0f}, {cw.high:,.0f})  long={cw.high-cw.low:,.0f}")
```

Lo que da en el box:
- Exponencial de media 1, asimetría de x̄ (0 = normal): n = 2 da 1,42; n = 10, 0,60; n = 100, 0,20 (con m = 20.000 en los tres); la varianza de x̄ es 1/n en todos. Con n = 20.000 y m = 10 la asimetría estimada es −0,56 solo por ruido (diez medias no alcanzan para dibujar nada), y con m = 1000 baja a −0,03. Es lo contrario de lo que se dijo en clase, que el TCL depende de las repeticiones C3P2 6:44.
- Réplica de la notebook (normal μ = 100, σ = 15, n = 700, semilla 42): x̄ = 99,88, IC (98,77; 100,99), longitud 2,22; 949 de 1000 intervalos cubren a μ; con n = 4000 la longitud baja a 0,93.
- Con n = 10 y σ estimada: z crítico 1,960 contra t crítico 2,262 con 9 grados de libertad; el intervalo con z cubre el 92,2% y el de t el 95,2%.
- IC para σ² con chi cuadrado (20 botellas simuladas): S² = 0,1668, IC (0,0965; 0,3558).
- Sueldo bruto (4939 filas): media 3.876.029, IC 95% (3.806.511; 3.945.547), longitud 139.036.
- Varones cis menos mujeres cis (3861 y 983): 798.107, IC 95% Welch (650.632; 945.583), 1943,5 grados de libertad. No contiene al 0, aunque en clase quedó sin corregir un "no hay mucha diferencia" C3P2 1:28:35.
- Bruto menos neto de la misma persona (4539 filas con 100.000 < neto < 15 M y neto ≤ bruto): diferencia media 655.515; IC apareado (633.410; 677.620), longitud 44.210; el de Welch, mal planteado, (564.365; 746.664), longitud 182.299. En clase el bruto y el neto aparecieron primero como apareados y después como ejemplo de Welch C3P2 1:01:28, C3P2 1:07:05: lo correcto es apareado.

### 8. Tests de hipótesis con scipy (notebook 05)
**En clase:** C4P1 35:25, C4P1 1:02:27, C4P1 1:27:55, C4P1 1:46:05, C4P1 1:52:48, C4P2 3:51, C4P2 6:04, C4P2 8:22, C4P2 19:39, C4P2 22:02, C4P2 26:21, C4P2 27:57, C4P2 31:56, C4P2 34:06, C4P2 34:40, C4P2 37:00, C4P2 39:52, C4P2 45:37

La notebook 05 tiene cinco ejemplos: t de una muestra (alturas de plantas), t de dos muestras (`Cutlets.csv`), ANOVA (`LabTAT.csv`), chi cuadrado de homogeneidad (`BuyerRatio.csv`) y chi cuadrado de formularios defectuosos (`Customer+OrderForm.csv`). El script de abajo los rehace corregidos y agrega la pregunta del entregable, no paramétricos y potencia.

Qué tenés que hacer:
- Escribí H0 y H1 antes de mirar los datos y elegí `alternative` según H1 (`"two-sided"`, `"less"`, `"greater"`).
- Compará el p valor de scipy con α (0,05); el bilateral ya incluye las dos colas. α/2 solo aparece si buscás a mano el valor crítico con `ppf`.
- Revisá supuestos: normalidad (`shapiro`) y varianzas (`levene`); ante la duda, Welch (`equal_var=False`); sin normalidad y con n chico, no paramétricos.
- Si el ANOVA rechaza, hacé Tukey HSD (`stats.tukey_hsd` o statsmodels) para saber qué pares difieren.
- No paramétricos: Wilcoxon (`stats.wilcoxon`) para una muestra o apareadas; Mann Whitney (`stats.mannwhitneyu`) para dos independientes; Kruskal Wallis para tres o más; Friedman para medidas repetidas.
- Para la brecha: test de una cola y, después, condicioná por seniority.
- Decí "no rechazo H0", nunca "acepto H0" ni "se probó H0".

```python
# g08_tests.py
# Tests de hipótesis: los 5 ejemplos del nb05 corregidos, la pregunta de la
# brecha salarial, no paramétricos y potencia (error tipo II)
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats

REPO = Path("/workspace/yt/ayvd_repo")   # en Colab: la URL raw del repo
ALPHA = 0.05                             # se compara SIEMPRE con el p valor, sea de una o dos colas

def decidir(p, alpha=ALPHA):
    return "rechazo H0" if p < alpha else "no rechazo H0 (no prueba que H0 sea cierta)"

# Ejemplo 1: t de una muestra (H0: mu = 38, H1: mu != 38)
data = [35.56, 35.56, 40.64, 33.02, 30.48, 43.18, 38.1, 35.56, 38.1, 33.02, 38.1, 35.56]
r = stats.ttest_1samp(data, 38, alternative="two-sided")
print(f"Ej1 media={np.mean(data):.3f} t={r.statistic:.4f} p={r.pvalue:.4f} gl={r.df} -> {decidir(r.pvalue)}")
print("    Shapiro (normalidad):", round(stats.shapiro(data).pvalue, 3))
# Lo mismo a mano: estadístico y p valor bilateral
t = (np.mean(data) - 38) / (np.std(data, ddof=1) / np.sqrt(len(data)))
print(f"    a mano: t={t:.4f} p={2*stats.t.sf(abs(t), len(data)-1):.4f}")

# Ejemplo 2: costeletas, dos muestras independientes, revisando supuestos
cut = pd.read_csv(REPO / "Cutlets.csv").dropna()
a, b = cut["Unit A"], cut["Unit B"]
print(f"\nEj2 n={len(a)},{len(b)}  Shapiro A p={stats.shapiro(a).pvalue:.3f} B p={stats.shapiro(b).pvalue:.3f}"
      f"  Levene p={stats.levene(a, b).pvalue:.3f}")
rs = stats.ttest_ind(a, b)                    # Student (equal_var=True por defecto), lo del nb05
rw = stats.ttest_ind(a, b, equal_var=False)   # Welch
print(f"    Student p={rs.pvalue:.4f}  Welch p={rw.pvalue:.4f} -> {decidir(rw.pvalue)} (comparando con 0,05, no 0,025)")

# Ejemplo 3: LabTAT, ANOVA de una vía + comparaciones de a pares (Tukey HSD)
lab = pd.read_csv(REPO / "LabTAT.csv")
grupos = [lab[c] for c in lab.columns]
f = stats.f_oneway(*grupos)
print(f"\nEj3 medias={lab.mean().round(1).to_dict()}")
print(f"    ANOVA F={f.statistic:.2f} p={f.pvalue:.3e} -> {decidir(f.pvalue)}")
print(f"    Levene p={stats.levene(*grupos).pvalue:.3f}  Kruskal Wallis p={stats.kruskal(*grupos).pvalue:.3e}")
tk = stats.tukey_hsd(*grupos)
pares = [(lab.columns[i], lab.columns[j], round(float(tk.pvalue[i, j]), 4))
         for i in range(4) for j in range(i + 1, 4)]
for p in pares: print("    Tukey", p)

# Ejemplo 4: BuyerRatio, chi cuadrado de homogeneidad
br = pd.read_csv(REPO / "BuyerRatio.csv", index_col=0)
print("\nEj4 datos del CSV (no coinciden con el enunciado del notebook):"); print(br)
c = stats.chi2_contingency(br)
print(f"    chi2={c.statistic:.3f} p={c.pvalue:.4f} gl={c.dof} -> {decidir(c.pvalue)}")
enun = pd.DataFrame({"East": [50, 550], "West": [142, 351], "North": [131, 480], "South": [70, 350]},
                    index=["Males", "Females"])
c2 = stats.chi2_contingency(enun)
print(f"    con los números del enunciado: chi2={c2.statistic:.2f} p={c2.pvalue:.2e} -> {decidir(c2.pvalue)}")

# Ejemplo 5: formularios defectuosos, de formato ancho a largo sin bucles
of = pd.read_csv(REPO / "Customer+OrderForm.csv")
largo = of.melt(var_name="centro", value_name="estado").dropna()
tab = pd.crosstab(largo.estado, largo.centro)
print("\nEj5"); print(tab)
c = stats.chi2_contingency(tab)
print(f"    chi2={c.statistic:.3f} p={c.pvalue:.4f} gl={c.dof} -> {decidir(c.pvalue)}")

# Brecha salarial: H0 mu_h - mu_m <= 0 vs H1 > 0 (una cola), Welch y Mann Whitney
df = pd.read_pickle("/workspace/yt/guia_code_ayvd/sysarmy2026.pkl")
h = df.loc[df.profile_g == "Varón cis", "salary_monthly_BRUTO"]
m = df.loc[df.profile_g == "Mujer cis", "salary_monthly_BRUTO"]
rw = stats.ttest_ind(h, m, equal_var=False, alternative="greater")
mw = stats.mannwhitneyu(h, m, alternative="greater")
print(f"\nBrecha: medias {h.mean():,.0f} vs {m.mean():,.0f}  medianas {h.median():,.0f} vs {m.median():,.0f}")
print(f"    Welch una cola t={rw.statistic:.2f} p={rw.pvalue:.2e}   Mann Whitney p={mw.pvalue:.2e}")
# Condicionando por seniority (posible confusión)
for s, g in df[df.profile_g.isin(["Varón cis", "Mujer cis"])].groupby("work_seniority"):
    hh, mm = g.loc[g.profile_g == "Varón cis", "salary_monthly_BRUTO"], g.loc[g.profile_g == "Mujer cis", "salary_monthly_BRUTO"]
    print(f"    {s:11s} n_h={len(hh):4d} n_m={len(mm):3d} dif medianas={hh.median()-mm.median():>10,.0f} "
          f"MW p={stats.mannwhitneyu(hh, mm, alternative='greater').pvalue:.3g}")

# No paramétricos: Wilcoxon = una muestra o APAREADAS; Mann Whitney = dos independientes
rng = np.random.default_rng(3)
antes = rng.exponential(10, 15); despues = antes * 0.8 + rng.normal(0, 1, 15)
print(f"\nWilcoxon apareado p={stats.wilcoxon(antes, despues).pvalue:.4f}"
      f"  Mann Whitney (ignora el apareo) p={stats.mannwhitneyu(antes, despues).pvalue:.4f}")
# Friedman: 3 modelos evaluados en los mismos 8 datasets (medidas repetidas)
acc = np.array([[.81, .83, .80], [.75, .78, .74], [.90, .91, .89], [.66, .70, .65],
                [.88, .87, .86], [.72, .76, .71], [.95, .96, .94], [.60, .64, .61]])
print("Friedman p =", round(stats.friedmanchisquare(*acc.T).pvalue, 4),
      " rangos promedio:", stats.rankdata(-acc, axis=1).mean(axis=0))

# Potencia y error tipo II con una alternativa concreta (lámparas: 5000 h vs 5200 h)
mu0, mu1, sigma, n = 5000, 5200, 600, 30
se = sigma / np.sqrt(n); corte = mu0 + stats.norm.ppf(1 - ALPHA) * se
beta = stats.norm.cdf(corte, mu1, se)
print(f"\nLámparas n={n}: rechazo si x̄ > {corte:.0f}  beta={beta:.3f}  potencia={1-beta:.3f}")
for n in [30, 60, 100, 200]:
    se = sigma / np.sqrt(n); corte = mu0 + stats.norm.ppf(1 - ALPHA) * se
    print(f"    n={n:3d} potencia={1 - stats.norm.cdf(corte, mu1, se):.3f}")

# p valor bajo H0 verdadera: ~5% de rechazos (eso es alfa)
p = [stats.ttest_1samp(rng.normal(0, 1, 30), 0).pvalue for _ in range(5000)]
print("\nproporción de p < 0,05 cuando H0 es cierta:", np.mean(np.array(p) < 0.05))
```

Lo que da en el box:
- Ejemplo 1: media 36,407, t = −1,5853, p = 0,1412, 11 grados de libertad (igual a mano); Shapiro p = 0,79. No se rechaza.
- Ejemplo 2: 35 y 35 costeletas; Shapiro 0,320 y 0,523; Levene 0,418; Student p = 0,4722 y Welch p = 0,4723. No se rechaza, comparando con 0,05 (en el repositorio la notebook todavía compara con 0,025, el error que se corrigió en clase C4P2 26:21).
- Ejemplo 3: medias 178,4, 178,9, 199,9 y 163,7; F = 118,70, p = 2,1 × 10⁻⁵⁷; Levene p = 0,052; Kruskal Wallis p = 1,2 × 10⁻⁴³. Tukey HSD: todos los pares difieren (p < 0,001) salvo laboratorio 1 contra 2 (p = 0,99). El ANOVA solo no dice "todos contra todos" C4P2 34:06.
- Ejemplo 4: con el CSV (mujeres 435, 1523, 1356 y 750 en Este, Oeste, Norte y Sur; varones 50, 142, 131 y 70), chi cuadrado 1,596, p = 0,66; con los números del enunciado (mujeres 550, 351, 480 y 350), chi cuadrado 80,27, p = 2,7 × 10⁻¹⁷. Revisá siempre que los datos sean los que creés C4P2 34:40.
- Ejemplo 5: defectuosos India 20, Indonesia 33, Malta 31 y Filipinas 29 de 300 cada uno; chi cuadrado 3,859, p = 0,277. No se rechaza.
- Brecha (bruto, varones cis contra mujeres cis): medias 4.039.036 y 3.240.928, medianas 3.450.941 y 2.800.000; Welch de una cola t = 10,61, p = 6,4 × 10⁻²⁶; Mann Whitney p = 1,4 × 10⁻²⁰. Por seniority, diferencia de medianas: Junior 0 (368 y 155 personas, p = 0,18), Semi Senior 300.000 (1123 y 360, p = 7 × 10⁻⁶), Senior 545.908 (2370 y 468, p = 3,3 × 10⁻⁶).
- 15 pares simulados antes y después: Wilcoxon apareado p = 0,0043; Mann Whitney, que ignora el apareo, p = 0,68. Por eso importa no intercambiarlos, como pasó en la tabla de la clase C4P1 1:52:48.
- Friedman con 3 modelos en 8 datasets: p = 0,0022, rangos promedio 2, 1,125 y 2,875 (rango 1 = mejor).
- Lámparas, H0: μ = 5000 h contra el proveedor que promete 5200 (σ = 600 h supuesto por mí, α = 0,05, una cola): con n = 30 se rechaza si x̄ > 5180, β = 0,428 y potencia 0,572; con 60, 0,826; con 100, 0,954; con 200, 0,999.
- Con H0 cierta, 5000 tests t dan p < 0,05 el 4,76% de las veces: eso es α.

### 9. Visualización para comunicar
**En clase:** V05 3:22, V05 5:04, V05 8:22, C4P2 49:34, C4P2 1:07:01, C4P2 1:15:27, C4P2 1:18:14, C4P2 1:19:53, C4P2 1:28:54, C4P2 1:33:23, C4P2 1:35:05, C4P2 1:43:27

Georgina cierra con lo que hace buena o tramposa a una visualización, y Milagro muestra en V05 barras, líneas y scatter con seaborn. El código aplica eso a la brecha de género, que es la figura que más probablemente termine en el entregable 2.

Qué tenés que hacer:
- Barras siempre desde 0; si querés mostrar un detalle, agregá un recuadro de zoom y decilo.
- En vez de dynamite plots (barra de media más barra de error), mostrá la distribución: violín, boxplot o puntos.
- Mismo orden de categorías y mismos colores en todos los paneles.
- `barplot(..., estimator="median", errorbar=None)`; `ci=None` está obsoleto desde seaborn 0.12.
- Agrupá una numérica ruidosa con `pd.cut` antes de graficarla contra otra.
- Paneles separados (small multiples) en vez de muchas curvas superpuestas.
- Paleta `colorblind` de seaborn o una apta para daltonismo.

```python
# g09_visualizacion.py
# Visualización para comunicar: eje truncado, dynamite plot vs distribución,
# paleta apta para daltonismo, errorbar=None, pd.cut y paneles separados
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

df = pd.read_pickle("/workspace/yt/guia_code_ayvd/sysarmy2026.pkl")
FIG = "/workspace/yt/guia_code_ayvd/fig/"
d = df[df.profile_g.isin(["Varón cis", "Mujer cis"]) & (df.salary_monthly_BRUTO < 15e6)]
med = d.groupby("profile_g").salary_monthly_BRUTO.median()
print(med)

# 1. Mismo dato, dos ejes: el truncado exagera la diferencia
fig, axs = plt.subplots(1, 2, figsize=(9, 3))
for ax, lo, tit in [(axs[0], 0, "eje desde 0"), (axs[1], 2.7e6, "eje truncado (engaña)")]:
    ax.bar(med.index, med.values, color=["#0072B2", "#E69F00"])
    ax.set_ylim(lo, med.max() * 1.05); ax.set_title(tit); ax.ticklabel_format(style="plain", axis="y")
fig.savefig(FIG + "eje_truncado.png", dpi=80, bbox_inches="tight"); plt.close(fig)
r = med.max() / med.min()
print(f"cociente real {r:.2f}; con eje desde 2,7M las barras miden {(med.max()-2.7e6)/(med.min()-2.7e6):.1f} veces")

ORD = ["Varón cis", "Mujer cis"]   # mismo orden en los tres paneles
# 2. Dynamite plot (media + barra de error) vs mostrar la distribución
fig, axs = plt.subplots(1, 3, figsize=(13, 3.5), sharey=True)
sns.barplot(data=d, x="profile_g", y="salary_monthly_BRUTO", ax=axs[0], errorbar=("ci", 95), order=ORD)
axs[0].set_title("barras + IC (dynamite)")
sns.violinplot(data=d, x="profile_g", y="salary_monthly_BRUTO", ax=axs[1], inner="quartile", cut=0, order=ORD)
axs[1].set_title("violín con cuartiles")
sns.stripplot(data=d.sample(800, random_state=0), x="profile_g", y="salary_monthly_BRUTO",
              ax=axs[2], alpha=.3, size=3, jitter=.25, order=ORD)
axs[2].set_title("puntos (muestra de 800)")
for ax in axs: ax.ticklabel_format(style="plain", axis="y")
fig.savefig(FIG + "dynamite_vs_dist.png", dpi=80, bbox_inches="tight"); plt.close(fig)

# 3. barplot sin barras de error (seaborn >= 0.12: errorbar=None; ci=None está obsoleto)
#    y edad agrupada con pd.cut para no graficar un lineplot ruidoso
d = d.assign(edad_g=pd.cut(d.profile_age, bins=range(15, 70, 5)))
fig, ax = plt.subplots(figsize=(9, 3.5))
pal = sns.color_palette("colorblind", 2)
sns.barplot(data=d, x="edad_g", y="salary_monthly_BRUTO", hue="profile_g",
            estimator="median", errorbar=None, palette=pal, ax=ax)
ax.tick_params(axis="x", rotation=45); ax.ticklabel_format(style="plain", axis="y")
ax.set_title("Mediana del salario bruto por edad y género (encuesta Sysarmy 2026.1, no representativa)")
fig.savefig(FIG + "edad_genero.png", dpi=80, bbox_inches="tight"); plt.close(fig)
print(d.groupby(["edad_g", "profile_g"], observed=True).size().unstack().head(4))

# 4. Paneles separados (small multiples) en vez de superponer muchas curvas
s = df[df.studies.isin(["Terciario", "Universitario", "Maestría"]) & (df.salary_monthly_BRUTO < 15e6)]
g = sns.displot(data=s, x="salary_monthly_BRUTO", col="studies", stat="density",
                common_norm=False, height=2.8, aspect=1.2)
g.savefig(FIG + "paneles_estudios.png", dpi=70); plt.close("all")
print("paleta colorblind:", [tuple(round(c, 2) for c in col) for col in pal])
print("ok figuras")
```

Lo que da en el box (bruto menor a 15 M):
- Medianas: mujeres cis 2.800.000 y varones cis 3.427.000, cociente 1,22. Con el eje y desde 2,7 M, la barra de varones mide 7,3 veces la de mujeres: el truco del eje truncado C4P2 1:18:14.
- El dynamite plot muestra dos barras con barras de error angostas y esconde que las dos distribuciones son asimétricas y se superponen mucho; el violín y el strip plot lo muestran.
- Tabla de edad agrupada por género: entre 30 y 35 años, 252 mujeres y 804 varones; entre 15 y 20, 3 y 16: los grupos extremos tienen muy pocos casos y sus barras no son confiables.
- La paleta `colorblind` empieza con azul (0; 0,45; 0,70) y naranja (0,87; 0,56; 0,02), distinguibles con daltonismo rojo verde.
- Las figuras quedan en `fig/` (`eje_truncado.png`, `dynamite_vs_dist.png`, `edad_genero.png`, `paneles_estudios.png`).

### 10. Los entregables
**En clase:** C1P1 17:17, C2P1 2:22, C2P1 7:15, C2P1 13:50, C3P1 1:24:49, C4P2 45:37, C4P2 47:18, C4P2 1:49:42

Qué tenés que hacer:
- **Parte 1 (notebook):** contestá "¿las mujeres cobran menos que los hombres?" C4P2 45:37 con lo de las secciones 1 a 8: limpieza justificada, descriptiva por género, intervalos de confianza de la diferencia, un test de una cola con sus supuestos revisados y el análisis condicionado por seniority. Probá cómo cambia la conclusión con α = 0,03 y 0,01, y averiguá qué hace el comando si no le pasás `alternative` C4P2 47:18.
- **Parte 2 (visualización):** una página como máximo, en formato libre (artículo, reporte, tweet, publicación de Instagram), con poca estadística y un mensaje C4P2 1:49:42; aplicá la sección 9.
- **En grupo:** todos con nombre en el encabezado; si uno sube, cuenta para todos; la notebook tiene que correr entera C2P1 7:15, C2P1 13:50.
- **Fechas:** para verificar en el aula virtual. En clase se habló de apertura el 10/04, entrega de la parte 2 desde el 17/04 y cierre a confirmar por Carolina Chavero C2P1 2:22, C4P2 1:49:42.

Un esqueleto para la parte 1, armado con las piezas probadas de esta guía:

```python
# esqueleto_entregable.py
import pandas as pd
from scipy import stats

URL = ("https://raw.githubusercontent.com/DiploDatos/AnalisisyVisualizacion/"
       "refs/heads/master/sysarmy_survey_2026_processed.csv")
df = pd.read_csv(URL)
df["profile_g"] = df.profile_gender.map({"Hombre Cis": "Varón cis", "Mujer Cis": "Mujer cis"})

# 1. Cortes justificados (anotá cuántas filas saca cada uno)
d = df[df.profile_g.notna() & (df.profile_age < 70)].copy()

# 2. Descriptiva por género
print(d.groupby("profile_g").salary_monthly_BRUTO.describe())

# 3. IC de la diferencia (Welch) y test de una cola
h = d.loc[d.profile_g == "Varón cis", "salary_monthly_BRUTO"]
m = d.loc[d.profile_g == "Mujer cis", "salary_monthly_BRUTO"]
print(stats.ttest_ind(h, m, equal_var=False).confidence_interval())
print(stats.ttest_ind(h, m, equal_var=False, alternative="greater"))
print(stats.mannwhitneyu(h, m, alternative="greater"))

# 4. Condicionado por seniority
for s, g in d.groupby("work_seniority"):
    gh = g.loc[g.profile_g == "Varón cis", "salary_monthly_BRUTO"]
    gm = g.loc[g.profile_g == "Mujer cis", "salary_monthly_BRUTO"]
    print(s, gh.median() - gm.median(), stats.mannwhitneyu(gh, gm, alternative="greater").pvalue)
```

Lo que da en el box (leyendo la copia local del CSV en lugar de la URL): con el corte de edad quedan 3856 varones cis y 982 mujeres cis (el filtro de edad saca 5 y 1); medianas 3.455.983 y 2.800.000; IC 95% Welch de la diferencia de medias (654.273; 949.442); Welch de una cola t = 10,66, p = 4,2 × 10⁻²⁶; Mann Whitney p = 8,6 × 10⁻²¹; por seniority, diferencias de medianas de 0 (Junior, p = 0,18), 300.000 (Semi Senior, p = 7 × 10⁻⁶) y 548.000 (Senior, p = 2,4 × 10⁻⁶). Es la misma historia que en la sección 8: la brecha no aparece en Junior y crece con la seniority.
