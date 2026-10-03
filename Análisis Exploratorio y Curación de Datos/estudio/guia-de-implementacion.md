# Guía de implementación: Análisis Exploratorio y Curación de Datos (Diplodatos, FAMAF UNC, José Robledo y Ariel Wolfmann)

**Videos:** C1P1, C1P2, C1P3, C2P1, C2P2, C3P1, C3P2, C4P1, C4P2. El apunte de estudio que acompaña esta guía es `analisis-exploratorio-y-curacion-apunte-de-estudio.md`.
**De qué va:** la parte práctica de la materia, ordenada por tema y no por clase: cómo se ven los faltantes en pandas, cómo explorar Melbourne Housing, cómo imputar (constante, regresión, KNN, MICE e imputación múltiple con las reglas de Rubin), cómo codificar categóricas con el dataset Adult, PCA con Iris, escaladores y transformaciones, chi cuadrado, SQL con SQLAlchemy, la combinación de Melbourne con Airbnb sin explotar la cardinalidad y un ETL chico con capas bronce, plata y oro. El código sigue las notebooks del repositorio público `DiploDatos/AnalisisYCuracion`, que es **la versión 2022** (las notebooks 2026 están en el aula virtual y no son públicas), corregido donde la clase o la notebook se equivocan.

> Nota: los links llevan al minuto de la clase donde se ve cada cosa ("C2P2 1:23:45" es la clase 2, parte 2, en la hora 1, minuto 23, segundo 45). Todo el código de esta guía se corrió en el box con Python 3.13, pandas 3.0.6, numpy 2.2.4, scikit-learn 1.9.1, scipy 1.18.1, matplotlib 3.11.2, missingno 0.5.2, SQLAlchemy 2.1.3 y pyarrow 25.0.1. Los datos son los mismos CSV que usa el repo, bajados del servidor de FAMAF (`https://cs.famaf.unc.edu.ar/~mteruel/datasets/diplodatos/`: `melb_data.csv`, `cleansed_listings_dec18.csv` y `sysarmy_survey_2020_processed.csv`) y `adult.data` de UCI; Iris viene con scikit-learn. Los scripts leen copias locales en `data/`; en Colab cambiá la ruta por la URL (está anotada en cada script). Lo que aparece como "lo que da en el box" es la salida real.

## Checklist para arrancar ya
1. Leé Melbourne desde la copia de FAMAF y mirá `shape` (13.580 × 21), `info()`, `describe()` e `isna().sum()` antes de tocar nada. Si el servidor no responde, el archivo de Kaggle que bajaron en clase tenía 18.396 filas y los números no van a coincidir C2P1 4:44 (sección 2).
2. Trabajá siempre sobre una copia (`df.copy()`) y guardá el original intacto C1P2 1:16:10.
3. Buscá faltantes con `isna()` (`isnull()` es lo mismo) y convertí a NaN los centinelas (0 baños en una casa, 9999, "?") antes de contar C1P2 1:21:14 (secciones 1 y 2).
4. Antes de decidir cómo imputar, mirá el patrón con `msno.matrix` y `msno.heatmap`: BuildingArea y YearBuilt faltan juntas C1P2 1:24:05 (sección 2).
5. Si filtrás outliers por cuantil, agregá `| col.isna()` para no tirar los faltantes en silencio C2P1 32:01 (sección 4).
6. Estandarizá antes de `KNNImputer` y volvé a la escala original después; usá `set_output(transform="pandas")` para no perder los nombres de columnas (sección 4).
7. Para el entregable 1 elegí un encoding y justificalo: ordinal solo si hay orden real, one hot para nominales con pocas categorías (Suburb tiene 314) C2P2 2:28:29, C4P1 48:28 (sección 5).
8. Estandarizá antes de PCA si las variables tienen escalas distintas y reportá la varianza explicada acumulada; distinguí loadings (`components_`) de scores (`transform`) (sección 6).
9. Para variables asimétricas como Price probá `PowerTransformer` o log; sabé que reducen la asimetría pero no eliminan outliers (sección 7).
10. En SQLAlchemy 2 envolvé las consultas con `text(...)`; el `conn.execute("SELECT ...")` de la notebook 2022 ya no anda (sección 9).
11. Antes de un merge, contá cuántas veces se repite la clave en cada lado; agregá primero y usá `validate="many_to_one"` C4P2 20:37 (sección 10).
12. Para el entregable 2: cargá ventas y la tabla de Airbnb por código postal en SQLite y hacé el JOIN en SQL C4P2 1:22:51 (secciones 10 y 11).
13. Entregá el 1 a más tardar el 14 de mayo C3P1 11:05; la fecha del 2 revisala en el aula virtual (sección 12).

## Versión completa

### 1. Faltantes en pandas: NaN, None, pd.NA, isna e isnull
**En clase:** C1P2 14:23, C1P2 17:42, C1P2 18:50, C1P2 19:59, C1P2 21:38, C1P2 23:52, C2P1 15:16, C2P1 20:13, C4P1 32:40, C4P1 35:36

José arranca la notebook de faltantes con Series chicas: un NaN pasa la columna a float, `astype("Int64")` la devuelve a entera con `<NA>`, y las comparaciones con NaN no funcionan C1P2 17:42, C1P2 21:38. En la clase 2 dice que `isnull` e `isna` son distintos C2P1 21:21, y en la clase 4 termina mostrando la documentación que dice que son lo mismo C4P1 35:36.

Qué tenés que hacer:
- Usá `"Int64"` (con mayúscula) si necesitás enteros con faltantes; `"int64"` falla.
- No compares con `== np.nan`: usá `isna()`. `np.nan` es un único objeto; no es igual a sí mismo por la norma IEEE 754, no por "instancias distintas".
- `isnull` e `isna` son lo mismo; elegí uno y usalo siempre.
- En pandas 3 las columnas de texto usan el dtype `str` y `None` se guarda como NaN; en pandas 2 (dtype `object`) quedaba `None`. Si tu Colab tiene pandas 2 vas a ver lo que muestra José.
- Convertí los centinelas (9999, -1) a NaN antes de contar.

```python
# g01_nan_tipos.py
import numpy as np
import pandas as pd

s = pd.Series([5, 2, 3])
print("dtype inicial:", s.dtype)
s.loc[2] = np.nan                       # aparece un faltante
print("con NaN:", s.dtype, s.tolist())
s_int = s.astype("Int64")               # entero que admite nulos (I mayúscula)
print("Int64:", s_int.dtype, s_int.tolist())
try:
    s.astype("int64")                   # minúscula: no admite nulos
except Exception as e:
    print("astype('int64') falla:", type(e).__name__)

txt_obj = pd.Series(["a", None, np.nan], dtype=object)   # como en pandas 2 / Colab
print("object:", txt_obj.tolist(), "| isna:", txt_obj.isna().tolist())
txt = pd.Series(["a", None, np.nan])                      # pandas 3: dtype str por defecto
print("pandas 3:", txt.dtype, txt.tolist(), "| isna:", txt.isna().tolist())

print("None == None:", None == None)
print("np.nan == np.nan:", np.nan == np.nan)
print("np.nan is np.nan:", np.nan is np.nan)   # es el mismo objeto
print("float('nan') == float('nan'):", float("nan") == float("nan"))
print("pd.NA == pd.NA:", pd.NA == pd.NA)
print("pd.NA | True:", pd.NA | True, "| pd.NA & False:", pd.NA & False)

print(pd.DataFrame.isnull.__doc__.strip().splitlines()[0])   # la doc lo declara alias
df = pd.DataFrame({"f": [1.0, np.nan, 3.0], "o": pd.Series(["x", None, np.nan], dtype=object),
                   "t": [pd.NaT, pd.Timestamp("2026-04-24"), None],
                   "i": pd.array([1, pd.NA, 3], dtype="Int64")})
print("isna == isnull en NaN, None, NaT y pd.NA:", df.isna().equals(df.isnull()))
print(df.isna().sum().to_dict())

x = pd.Series([1.0, np.nan, 3.0])
print("mean saltea NaN:", x.mean(), "| skipna=False:", x.mean(skipna=False))

codes = pd.Series([3, 9999, 5, -1])
print("isna no ve centinelas:", codes.isna().sum(),
      "| tras replace:", codes.replace([9999, -1], np.nan).isna().sum())
print("pandas", pd.__version__)
```

Lo que da en el box:
```text
dtype inicial: int64
con NaN: float64 [5.0, 2.0, nan]
Int64: Int64 [5, 2, <NA>]
astype('int64') falla: IntCastingNaNError
object: ['a', None, nan] | isna: [False, True, True]
pandas 3: str ['a', nan, nan] | isna: [False, True, True]
None == None: True
np.nan == np.nan: False
np.nan is np.nan: True
float('nan') == float('nan'): False
pd.NA == pd.NA: <NA>
pd.NA | True: True | pd.NA & False: False
DataFrame.isnull is an alias for DataFrame.isna.
isna == isnull en NaN, None, NaT y pd.NA: True
{'f': 1, 'o': 2, 't': 2, 'i': 1}
mean saltea NaN: 2.0 | skipna=False: nan
isna no ve centinelas: 0 | tras replace: 2
pandas 3.0.6
```

### 2. Explorar Melbourne con pandas y missingno
**En clase:** C1P2 26:40, C1P2 33:53, C1P2 42:03, C1P2 57:29, C1P2 1:03:43, C1P2 1:11:02, C1P2 1:21:14, C1P2 1:24:05, C4P1 27:01, C4P1 31:32, C4P1 38:29, C4P1 44:34

José explora con `info`, `describe`, conteos de ceros, el caso de Bedroom2 = 20, la crosstab de Rooms contra Bedroom2 y missingno C1P2 33:53, C1P2 1:11:02, C1P2 1:24:05. Ariel repite la exploración en la clase 4 con la notebook "01 Exploracion" del repo C4P1 27:01.

Qué tenés que hacer:
- Contá faltantes, ceros y valores únicos por columna y anotá qué es sospechoso (Landsize 0, Bathroom 0 en casas).
- Si dos columnas dicen casi lo mismo (Rooms y Bedroom2, 95% de la crosstab en la diagonal), quedate con una o justificá por qué no.
- Pasá a NaN los valores imposibles con `.loc[cond, col] = pd.NA` en una copia.
- Mirá la correlación de nulidad: si dos columnas faltan juntas, imputarlas por separado no tiene mucho sentido.

```python
# g02_explorar_melbourne.py
import matplotlib
matplotlib.use("Agg")
import missingno as msno
import pandas as pd

URL = "https://cs.famaf.unc.edu.ar/~mteruel/datasets/diplodatos/melb_data.csv"
try:
    df = pd.read_csv("data/melb_data.csv")      # copia local bajada de URL
except FileNotFoundError:
    df = pd.read_csv(URL)
print(df.shape)
print(df["Rooms"].describe().round(6).to_dict())
print("faltantes:", df.isna().sum()[lambda s: s > 0].to_dict())
print("ceros:", (df == 0).sum()[lambda s: s > 0].to_dict())
print("nunique:", df.nunique()[["Address", "Suburb", "CouncilArea", "Regionname",
                                "Method", "Type", "Date", "Postcode"]].to_dict())
print(df.loc[df.Bedroom2 == 20, ["Suburb", "Rooms", "Bedroom2", "Bathroom", "Type"]])

ct = pd.crosstab(df.Rooms, df.Bedroom2)
diag = sum(ct.loc[r, float(r)] for r in ct.index if float(r) in ct.columns)
print(f"crosstab Rooms vs Bedroom2: {diag / ct.values.sum():.1%} en la diagonal")
print("Rooms=1 y Bedroom2=1:", ct.loc[1, 1.0], "| 2 y 2:", ct.loc[2, 2.0], "| 2 y 1:", ct.loc[2, 1.0])

work = df.copy()                                 # nunca sobre el original
mask = (work.Bathroom == 0) & (work.Type == "h")
work.loc[mask, "Bathroom"] = pd.NA
print("casas con 0 baños pasadas a NA:", int(mask.sum()))

print(df.Regionname.value_counts().head(3).to_dict())
print("corr Rooms-Bedroom2:", round(df.Rooms.corr(df.Bedroom2), 3))

nul = df[["Car", "BuildingArea", "YearBuilt", "CouncilArea"]].isna().astype(int)
print("correlación de nulidad:\n", nul.corr().round(2))
ax = msno.matrix(df.sample(200, random_state=0))
ax.get_figure().savefig("out/msno_matrix.png", dpi=80)
ax = msno.heatmap(df)
ax.get_figure().savefig("out/msno_heatmap.png", dpi=80)
print("guardados out/msno_matrix.png y out/msno_heatmap.png")
```

Lo que da en el box:
```text
(13580, 21)
{'count': 13580.0, 'mean': 2.937997, 'std': 0.955748, 'min': 1.0, '25%': 2.0, '50%': 3.0, '75%': 3.0, 'max': 10.0}
faltantes: {'Car': 62, 'BuildingArea': 6450, 'YearBuilt': 5375, 'CouncilArea': 1369}
ceros: {'Distance': 6, 'Bedroom2': 16, 'Bathroom': 34, 'Car': 1026, 'Landsize': 1939, 'BuildingArea': 17}
nunique: {'Address': 13378, 'Suburb': 314, 'CouncilArea': 33, 'Regionname': 8, 'Method': 5, 'Type': 3, 'Date': 58, 'Postcode': 198}
              Suburb  Rooms  Bedroom2  Bathroom Type
7404  Caulfield East      3      20.0       1.0    h
crosstab Rooms vs Bedroom2: 95.0% en la diagonal
Rooms=1 y Bedroom2=1: 663 | 2 y 2: 3539 | 2 y 1: 21
casas con 0 baños pasadas a NA: 15
{'Southern Metropolitan': 4695, 'Northern Metropolitan': 3890, 'Western Metropolitan': 2948}
corr Rooms-Bedroom2: 0.944
correlación de nulidad:
                Car  BuildingArea  YearBuilt  CouncilArea
Car           1.00          0.01       0.01         0.20
BuildingArea  0.01          1.00       0.77         0.02
YearBuilt     0.01          0.77       1.00         0.04
CouncilArea   0.20          0.02       0.04         1.00
guardados out/msno_matrix.png y out/msno_heatmap.png
```

Con el CSV de FAMAF los números de la clase 4 cierran: Car 62 y BuildingArea 6.450 faltantes, CouncilArea 33 categorías y 1.369 faltantes (no "1369 categorías"), desvío de Rooms 0,956 (no 0). Las cifras de la clase 2 (14.820 filas tras `dropna`, 7.102 faltantes en BuildingArea, 2.587 en CouncilArea) son del archivo de Kaggle de 18.396 filas. La crosstab coincide con la de José: 663 con 1 y 1, 3.539 con 2 y 2, 21 con 2 y 1 C1P2 1:11:39.

### 3. Imputación: del ejemplo de juguete a la imputación múltiple
**En clase:** C1P3 11:01, C1P3 13:45, C1P3 14:54, C1P3 25:11, C1P3 28:29, C1P3 41:18, C1P3 44:37

José muestra con una animación que imputar por la media se equivoca feo cuando las variables se relacionan, y que la regresión recupera los valores C1P3 13:45; después presenta KNN, MICE e imputación múltiple C1P3 25:11, C1P3 41:18, C1P3 44:37. El script de abajo arma un ejemplo propio con la misma idea (no tengo los números exactos de su animación) y suma KNN e `IterativeImputer`, que es el MICE de scikit-learn.

Qué tenés que hacer:
- Antes de imputar por regresión, mirá la correlación: si es alta, la regresión le gana por mucho a la media.
- Recordá que la media achica la correlación (de 1 a 0,95 en el ejemplo).
- `KNNImputer` no exige vecinos completos: el vecino solo tiene que tener la columna que imputás.
- `IterativeImputer` necesita `from sklearn.experimental import enable_iterative_imputer` antes de importarlo.

```python
# g03_imputacion_juguete.py
import numpy as np
import pandas as pd
from sklearn.experimental import enable_iterative_imputer  # noqa: F401
from sklearn.impute import IterativeImputer, KNNImputer, SimpleImputer
from sklearn.linear_model import LinearRegression

# tres variables con relación lineal exacta: y = 2x + 5, z = 3x - 10
x = np.arange(1, 21, dtype=float)
full = pd.DataFrame({"x": x, "y": 2 * x + 5, "z": 3 * x - 10})
df = full.copy()
holes = {"y": [2, 9], "z": [15]}                  # filas con faltantes
for col, rows in holes.items():
    df.loc[rows, col] = np.nan

def show(name, imputed):
    vals = [round(float(imputed.loc[r, c]), 2) for c, rows in holes.items() for r in rows]
    print(f"{name:<12}", vals)

show("real", full)
show("media", pd.DataFrame(SimpleImputer(strategy="mean").fit_transform(df), columns=df.columns))

reg = df.copy()
for col in holes:
    ok = df[col].notna()
    m = LinearRegression().fit(df.loc[ok, ["x"]], df.loc[ok, col])
    reg.loc[~ok, col] = m.predict(df.loc[~ok, ["x"]])
show("regresión", reg)

show("KNN k=3", pd.DataFrame(KNNImputer(n_neighbors=3).fit_transform(df), columns=df.columns))
show("Iterative", pd.DataFrame(IterativeImputer(random_state=0).fit_transform(df), columns=df.columns))

med = pd.DataFrame(SimpleImputer().fit_transform(df), columns=df.columns)
print("corr x-y real:", round(full.x.corr(full.y), 4), "| tras imputar con la media:", round(med.x.corr(med.y), 4))

# KNNImputer no exige vecinos completos: usa nan_euclidean
X = np.array([[1, 2, np.nan], [1, np.nan, 30], [1.1, 2.1, 31], [9, 9, 90]])
print("KNN con vecinos incompletos:\n", KNNImputer(n_neighbors=1).fit_transform(X))
```

Lo que da en el box:
```text
real         [11.0, 25.0, 38.0]
media        [26.89, 26.89, 20.63]
regresión    [11.0, 25.0, 38.0]
KNN k=3      [9.67, 26.33, 36.0]
Iterative    [11.0, 25.0, 38.0]
corr x-y real: 1.0 | tras imputar con la media: 0.9538
KNN con vecinos incompletos:
 [[ 1.   2.  30. ]
 [ 1.   2.  30. ]
 [ 1.1  2.1 31. ]
 [ 9.   9.  90. ]]
```

La imputación múltiple bien hecha es distinta de lo que se describe en clase C1P3 41:50: no se imputan subconjuntos, se generan m copias completas con sorteos distintos (`sample_posterior=True`) y se combinan con las reglas de Rubin. El ejemplo usa faltantes MAR (y falta más cuando x es alto), así que el promedio de casos completos sale sesgado.

```python
# g04_imputacion_multiple.py
import numpy as np
import pandas as pd
from sklearn.experimental import enable_iterative_imputer  # noqa: F401
from sklearn.impute import IterativeImputer

rng = np.random.default_rng(0)
n = 500
x = rng.normal(50, 10, n)
y = 0.8 * x + rng.normal(0, 6, n)
true_mean = y.mean()
df = pd.DataFrame({"x": x, "y": y})
# MAR: y falta más cuando x es alto (depende de una variable observada)
p_miss = 1 / (1 + np.exp(-(x - 55) / 4))
df.loc[rng.random(n) < p_miss, "y"] = np.nan
print(f"faltan {df.y.isna().mean():.0%} de y | media real {true_mean:.2f}")
print(f"casos completos (sesgado por MAR): {df.y.mean():.2f}")

# imputación múltiple: m copias COMPLETAS, cada una con sorteos distintos
m = 20
estimates, variances = [], []
for i in range(m):
    imp = IterativeImputer(sample_posterior=True, random_state=i)
    full = pd.DataFrame(imp.fit_transform(df), columns=df.columns)
    estimates.append(full.y.mean())
    variances.append(full.y.var(ddof=1) / n)          # varianza de la media en esa copia

q_bar = np.mean(estimates)                 # estimación combinada
W = np.mean(variances)                     # varianza dentro (within)
B = np.var(estimates, ddof=1)              # varianza entre (between)
T = W + (1 + 1 / m) * B                    # reglas de Rubin
print(f"MI (m={m}): media {q_bar:.2f} | W={W:.4f} B={B:.4f} T={T:.4f} | EE={np.sqrt(T):.3f}")

single = IterativeImputer(random_state=0).fit_transform(df)[:, 1]
print(f"una sola imputación determinística: media {single.mean():.2f} | EE ingenuo {single.std(ddof=1)/np.sqrt(n):.3f}")
print("las m estimaciones varían:", np.round(estimates[:5], 2))
```

Lo que da en el box:
```text
faltan 34% de y | media real 39.37
casos completos (sesgado por MAR): 35.83
MI (m=20): media 39.68 | W=0.2079 B=0.0230 T=0.2321 | EE=0.482
una sola imputación determinística: media 39.69 | EE ingenuo 0.434
las m estimaciones varían: [39.89 39.78 39.76 39.52 39.58]
```

Fijate tres cosas. Los casos completos subestiman la media (35,83 contra 39,37) porque faltan justo los valores altos. Las dos imputaciones corrigen casi todo el sesgo porque el mecanismo es MAR y x está observada. Y el error estándar de la imputación múltiple (0,482) es más grande que el de una sola imputación tratada como si fueran datos reales (0,434): esa diferencia es la incertidumbre por los faltantes, que la imputación única esconde.

### 4. Imputación en Melbourne con scikit-learn
**En clase:** C2P1 15:50, C2P1 24:48, C2P1 27:33, C2P1 32:01, C2P1 36:29, C2P1 42:13, C2P1 46:34, C2P1 51:35, C2P1 57:37

La parte 2 de la notebook de faltantes filtra outliers por cuantiles conservando los NaN, imputa con constantes y con KNN y compara k de 1 a 4 C2P1 32:01, C2P1 42:13, C2P1 51:35, C2P1 57:37.

Qué tenés que hacer:
- Usá cuantiles y no valores fijos para recortar, y siempre `| col.isna()`: sin eso, el filtro de BuildingArea tira casi la mitad de la tabla (de 13.580 a 7.058 filas).
- No imputes con una constante fuera de rango (0, 999) salvo que el modelo lo necesite: deforma la distribución.
- Estandarizá antes de KNN. Sin escalar, Price (millones) domina la distancia y los vecinos salen casi solo por precio.
- Probá en una submuestra antes de correr sobre todo.

```python
# g05_melbourne_imputadores.py
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer, SimpleImputer
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("data/melb_data.csv")
print("filas:", len(df), "| dropna(subset=['Car']):", len(df.dropna(subset=["Car"])))
print("CouncilArea faltantes:", df.CouncilArea.isna().sum(), "categorías:", df.CouncilArea.nunique())

q99_ba = df.BuildingArea.quantile(0.99)
q01_yb = df.YearBuilt.quantile(0.01)
q99_ls = df.Landsize.quantile(0.99)
print(f"q99 BuildingArea {q99_ba:.2f} | q01 YearBuilt {q01_yb:.0f} | q99 Landsize {q99_ls:.2f}")
mal = df[df.BuildingArea < q99_ba]                       # tira los NaN sin avisar
bien = df[(df.BuildingArea < q99_ba) | df.BuildingArea.isna()]
print("sin '| isnull':", len(mal), "| con '| isnull':", len(bien))
work = bien[((bien.YearBuilt > q01_yb) | bien.YearBuilt.isna())
            & ((bien.Landsize < q99_ls) | bien.Landsize.isna())].copy()
print("tras los tres filtros:", len(work))

cols = ["BuildingArea", "YearBuilt", "Landsize", "Rooms", "Distance", "Price"]
X = work[cols]
for fill in (0, 999):
    imp = SimpleImputer(strategy="constant", fill_value=fill).set_output(transform="pandas")
    out = imp.fit_transform(X)
    print(f"constante {fill}: mediana YearBuilt {out.YearBuilt.median():.0f} | "
          f"proporción BuildingArea == {fill}: {(out.BuildingArea == fill).mean():.1%}")

knn = KNNImputer(n_neighbors=3).set_output(transform="pandas")
raw = knn.fit_transform(X)                               # sin escalar
sc = StandardScaler().set_output(transform="pandas")
Z = sc.fit_transform(X)                                  # StandardScaler ignora los NaN al ajustar
scaled = pd.DataFrame(sc.inverse_transform(knn.fit_transform(Z)), columns=cols, index=X.index)
miss = X.BuildingArea.isna()
print("BuildingArea: real media", round(X.BuildingArea.mean(), 1),
      "| KNN sin escalar", round(raw.loc[miss, "BuildingArea"].mean(), 1),
      "| KNN escalado", round(scaled.loc[miss, "BuildingArea"].mean(), 1))
print("diferencia media absoluta entre las dos imputaciones:",
      round((raw.loc[miss, "BuildingArea"] - scaled.loc[miss, "BuildingArea"]).abs().mean(), 1))

sub = X.sample(3000, random_state=0)                     # probar en una submuestra
for k in (1, 2, 3, 4):
    o = KNNImputer(n_neighbors=k).set_output(transform="pandas").fit_transform(sub)
    print(f"k={k}: BuildingArea media {o.BuildingArea.mean():.1f} desvío {o.BuildingArea.std():.1f}")
```

Lo que da en el box:
```text
filas: 13580 | dropna(subset=['Car']): 13518
CouncilArea faltantes: 1369 categorías: 33
q99 BuildingArea 466.42 | q01 YearBuilt 1880 | q99 Landsize 2959.83
sin '| isnull': 7058 | con '| isnull': 13508
tras los tres filtros: 13279
constante 0: mediana YearBuilt 1925 | proporción BuildingArea == 0: 48.0%
constante 999: mediana YearBuilt 1925 | proporción BuildingArea == 999: 47.8%
BuildingArea: real media 139.4 | KNN sin escalar 141.8 | KNN escalado 135.4
diferencia media absoluta entre las dos imputaciones: 36.0
k=1: BuildingArea media 140.9 desvío 72.9
k=2: BuildingArea media 139.6 desvío 65.6
k=3: BuildingArea media 139.4 desvío 63.6
k=4: BuildingArea media 139.4 desvío 62.6
```

Los valores imputados de BuildingArea cambian en promedio 36 m² según escales o no. La media global casi no se mueve, pero los valores fila por fila sí, y eso es lo que importa si después usás la columna para predecir. Con k más grande el desvío baja (72,9 con k = 1, 62,6 con k = 4): promediar más vecinos aplana la distribución imputada. El q99 de BuildingArea es 466,42 con este CSV; el 465 de la clase es del archivo de Kaggle.

### 5. Codificación de categóricas con Adult
**En clase:** C2P2 32:44, C2P2 35:32, C2P2 40:03, C2P2 41:43, C2P2 44:37, C2P2 46:53, C2P2 52:22, C2P2 55:09

José usa el dataset Adult de UCI: marca los "?" como faltantes, codifica `education` con `OrdinalEncoder` y un orden explícito, y `race` con `get_dummies` C2P2 40:03, C2P2 44:37, C2P2 52:22.

Qué tenés que hacer:
- Leé `adult.data` con `skipinitialspace=True`: los campos vienen separados por coma y espacio y el faltante es `" ?"`. Con `na_values="?"` solo, no detecta ninguno.
- Pasá el orden de las categorías a `OrdinalEncoder`; si no, las ordena alfabéticamente. Chequeá contra `education-num`, que ya es ese mismo orden.
- `drop_first=True` saca una columna redundante; útil con modelos lineales, no hace falta con árboles.
- Para producción, preferí `OneHotEncoder(handle_unknown="ignore")`: recuerda las categorías del entrenamiento y devuelve una matriz esparsa.

```python
# g06_adult_encoding.py
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder

cols = ["age", "workclass", "fnlwgt", "education", "education-num", "marital-status",
        "occupation", "relationship", "race", "sex", "capital-gain", "capital-loss",
        "hours-per-week", "native-country", "income"]
URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data"
src = "data/adult.data"                       # copia local de URL
naive = pd.read_csv(src, names=cols, na_values="?")
print("filas:", len(naive), "| faltantes con na_values='?':", int(naive.isna().sum().sum()))
df = pd.read_csv(src, names=cols, na_values="?", skipinitialspace=True)
print("con skipinitialspace=True:", df.isna().sum()[lambda s: s > 0].to_dict())

print("niveles de education:", df.education.nunique())
order = ["Preschool", "1st-4th", "5th-6th", "7th-8th", "9th", "10th", "11th", "12th",
         "HS-grad", "Some-college", "Assoc-voc", "Assoc-acdm", "Bachelors", "Masters",
         "Prof-school", "Doctorate"]
enc = OrdinalEncoder(categories=[order])
df["education_encoded"] = enc.fit_transform(df[["education"]]).astype("int8")
check = df.groupby("education_encoded")["education-num"].unique().apply(list)
print("coincide con education-num - 1:",
      all(v == [k + 1] for k, v in check.items()))

print(df.race.value_counts().to_dict())
d1 = pd.get_dummies(df.race, prefix="race", drop_first=True, dtype=int)
d0 = pd.get_dummies(df.race, prefix="race", dtype=int)
print("get_dummies:", d0.shape[1], "columnas | drop_first:", d1.shape[1], list(d1.columns)[:2])
df2 = pd.concat([df.copy(), d1], axis=1).drop(columns="race")
print("df2:", df2.shape)

ohe = OneHotEncoder(drop="first", handle_unknown="ignore", sparse_output=True)
M = ohe.fit_transform(df[["native-country"]].fillna("Unknown"))
print("one hot esparso:", M.shape, f"densidad {M.nnz / (M.shape[0] * M.shape[1]):.3f}")
```

Lo que da en el box:
```text
filas: 32561 | faltantes con na_values='?': 0
con skipinitialspace=True: {'workclass': 1836, 'occupation': 1843, 'native-country': 583}
niveles de education: 16
coincide con education-num - 1: True
{'White': 27816, 'Black': 3124, 'Asian-Pac-Islander': 1039, 'Amer-Indian-Eskimo': 311, 'Other': 271}
get_dummies: 5 columnas | drop_first: 4 ['race_Asian-Pac-Islander', 'race_Black']
df2: (32561, 19)
one hot esparso: (32561, 41) densidad 0.024
```

El archivo `adult.data` es el de entrenamiento (32.561 filas); las 48.842 instancias que cita José C2P2 40:03 suman también `adult.test`.

### 6. PCA con Iris
**En clase:** C2P2 1:03:29, C2P2 1:05:10, C2P2 1:14:30, C2P2 1:17:51, C2P2 1:23:56, C2P2 1:27:12, C2P2 1:38:16, C2P2 1:45:27, C2P2 1:51:31

José muestra PCA primero con dos variables y después con las cuatro de Iris, estandarizadas C2P2 1:38:16, C2P2 1:45:27. El script verifica sus números y las cuatro correcciones del apunte: qué par de variables da 55,87% / 44,12%, cuánto suman PC1 y PC2, loadings contra scores, y que PC1 no es la recta de regresión.

Qué tenés que hacer:
- Estandarizá si las variables tienen escalas distintas; si no, la de mayor varianza se lleva la PC1 (con Iris sin estandarizar la PC1 explica 92,46%).
- Reportá `explained_variance_ratio_` acumulada y elegí cuántas componentes con un criterio (90 o 95%, o el codo).
- Los loadings (`components_`) dicen cuánto pesa cada variable en cada componente; los scores (`transform`) son las coordenadas de cada dato.
- Si querés interpretar, mirá los loadings: PC1 de Iris es casi "tamaño de pétalo y largo de sépalo", PC2 es casi "ancho de sépalo".

```python
# g07_pca_iris.py
import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.decomposition import PCA
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

iris = load_iris(as_frame=True)
X = iris.data
print(X.shape, "| especies:", iris.target_names.tolist())

for pair in (["sepal length (cm)", "sepal width (cm)"], ["petal length (cm)", "petal width (cm)"]):
    Z = StandardScaler().fit_transform(X[pair])
    p = PCA().fit(Z)
    r = X[pair].corr().iloc[0, 1]
    print(f"{pair[0][:5]} r={r:+.3f} -> varianza explicada {np.round(p.explained_variance_ratio_ * 100, 2)}")

Z = StandardScaler().fit_transform(X)
pca = PCA().fit(Z)
ratio = pca.explained_variance_ratio_
print("4 variables estandarizadas:", np.round(ratio * 100, 2), "| PC1+PC2 =", round(ratio[:2].sum() * 100, 2))
print("autovalores (explained_variance_):", np.round(pca.explained_variance_, 3))
loadings = pd.DataFrame(pca.components_[:2].T, index=X.columns, columns=["PC1", "PC2"])
print("loadings (components_):\n", loadings.round(3))
scores = pca.transform(Z)[:, :2]
print("scores de las 2 primeras flores:\n", scores[:2].round(3))

C = np.cov(Z, rowvar=False)                         # mismo resultado diagonalizando la covarianza
vals = np.sort(np.linalg.eigvalsh(C))[::-1]
print("autovalores de la covarianza:", np.round(vals, 3))

full = PCA().fit(Z).transform(Z)
d_orig = np.linalg.norm(Z[0] - Z[1]); d_rot = np.linalg.norm(full[0] - full[1])
d_2 = np.linalg.norm(scores[0] - scores[1])
print(f"distancia flor0-flor1: original {d_orig:.4f} | rotada {d_rot:.4f} | solo 2 PCs {d_2:.4f}")

xy = X[["sepal length (cm)", "sepal width (cm)"]].values
pc1 = PCA(1).fit(xy).components_[0]
ols = LinearRegression().fit(xy[:, [0]], xy[:, 1]).coef_[0]
print(f"pendiente PC1 {pc1[1] / pc1[0]:.4f} vs pendiente MCO {ols:.4f}")
std = StandardScaler().fit_transform(X)
print("estandarizado: fuera de [-1, 1]:", f"{(np.abs(std) > 1).mean():.1%}")
```

Lo que da en el box:
```text
(150, 4) | especies: ['setosa', 'versicolor', 'virginica']
sepal r=-0.118 -> varianza explicada [55.88 44.12]
petal r=+0.963 -> varianza explicada [98.14  1.86]
4 variables estandarizadas: [72.96 22.85  3.67  0.52] | PC1+PC2 = 95.81
autovalores (explained_variance_): [2.938 0.92  0.148 0.021]
loadings (components_):
                      PC1    PC2
sepal length (cm)  0.521  0.377
sepal width (cm)  -0.269  0.923
petal length (cm)  0.580  0.024
petal width (cm)   0.565  0.067
scores de las 2 primeras flores:
 [[-2.265  0.48 ]
 [-2.081 -0.674]]
autovalores de la covarianza: [2.938 0.92  0.148 0.021]
distancia flor0-flor1: original 1.1762 | rotada 1.1762 | solo 2 PCs 1.1687
pendiente PC1 -0.0850 vs pendiente MCO -0.0619
estandarizado: fuera de [-1, 1]: 43.5%
```

El 55,88% y 44,12% sale con las variables de **sépalo** (r = −0,118), no con las de pétalo, que dan 98,14% y 1,86% porque están casi perfectamente correlacionadas. PC1 + PC2 con las cuatro = 95,81%. La distancia entre dos flores se conserva con todas las componentes (1,1762) y se achica con dos (1,1687). La pendiente de PC1 y la de la regresión difieren (−0,085 contra −0,062). Y el 43,5% de los valores estandarizados cae fuera de [−1, 1].

### 7. Escaladores y transformaciones
**En clase:** C2P2 2:07:33, C2P2 2:13:42, C2P2 2:15:47, C2P2 2:16:20, C2P2 2:17:28, C2P2 2:20:42, C2P2 2:21:47, C2P2 2:26:11

José recorre los escaladores de scikit-learn y las transformaciones de potencia y de cuantiles con los gráficos de la documentación C2P2 2:13:42, C2P2 2:21:47.

Qué tenés que hacer:
- MinMax es `(x − min)/(max − min)`; no preserva el 0 si hay negativos. MaxAbs sí.
- RobustScaler centra en la mediana y divide por el IQR.
- Para Price (asimetría 2,24) probá log, Yeo-Johnson o Box-Cox; Box-Cox falla con ceros (Landsize).
- Guardá el transformador ajustado para poder volver con `inverse_transform`.
- Ajustá el escalador solo con los datos de entrenamiento y aplicalo al test.

```python
# g08_escaladores.py
import numpy as np
import pandas as pd
from scipy.stats import skew
from sklearn.preprocessing import (MaxAbsScaler, MinMaxScaler, Normalizer, PowerTransformer,
                                   QuantileTransformer, RobustScaler, StandardScaler)

x = np.array([[2.0], [4.0], [6.0], [10.0], [100.0]])
mm = MinMaxScaler().fit_transform(x).ravel()
print("MinMax:", mm.round(4), "| a mano:", ((x.ravel() - 2) / (100 - 2)).round(4))
print("dividir solo por el máximo daría:", ((x.ravel() - 2) / 100).round(4))
y = np.array([[-50.0], [0.0], [10.0], [200.0]])
print("MinMax con negativos, el 0 va a:", MinMaxScaler().fit_transform(y).ravel()[1].round(4),
      "| MaxAbs deja el 0 en:", MaxAbsScaler().fit_transform(y).ravel()[1])
rs = RobustScaler().fit(x)
print("RobustScaler center_ (mediana):", rs.center_, "scale_ (IQR):", rs.scale_)
print("Standard:", StandardScaler().fit_transform(x).ravel().round(3))

df = pd.read_csv("data/melb_data.csv")
price = df[["Price"]]
print(f"asimetría Price {skew(price.Price):.2f} | log {skew(np.log(price.Price)):.2f}")
yj = PowerTransformer(method="yeo-johnson").fit_transform(price).ravel()
bc = PowerTransformer(method="box-cox").fit_transform(price).ravel()
qt = QuantileTransformer(output_distribution="normal", n_quantiles=1000, random_state=0).fit_transform(price).ravel()
print(f"asimetría Yeo-Johnson {skew(yj):.3f} | Box-Cox {skew(bc):.3f} | Quantile normal {skew(qt):.3f}")
try:
    PowerTransformer(method="box-cox").fit(df[["Landsize"]])
except ValueError as e:
    print("Box-Cox con ceros falla:", str(e)[:60])
pt = PowerTransformer().fit(price)
back = pt.inverse_transform(pt.transform(price)).ravel()
print("inversa recupera el precio:", np.allclose(back, price.Price))
def n_outliers(v):
    q1, q3 = np.percentile(v, [25, 75])
    iqr = q3 - q1
    return int(((v < q1 - 1.5 * iqr) | (v > q3 + 1.5 * iqr)).sum())
print("outliers 1,5 IQR: crudo", n_outliers(price.Price.values), "| en log", n_outliers(np.log(price.Price.values)))
rows = np.array([[3.0, 4.0], [1.0, 1.0]])
print("Normalizer (cada fila a norma 1):", Normalizer().fit_transform(rows).round(4).tolist())
```

Lo que da en el box:
```text
MinMax: [0.     0.0204 0.0408 0.0816 1.    ] | a mano: [0.     0.0204 0.0408 0.0816 1.    ]
dividir solo por el máximo daría: [0.   0.02 0.04 0.08 0.98]
MinMax con negativos, el 0 va a: 0.2 | MaxAbs deja el 0 en: 0.0
RobustScaler center_ (mediana): [6.] scale_ (IQR): [6.]
Standard: [-0.591 -0.538 -0.486 -0.38   1.995]
asimetría Price 2.24 | log 0.18
asimetría Yeo-Johnson 0.001 | Box-Cox 0.001 | Quantile normal 0.008
Box-Cox con ceros falla: The Box-Cox transformation can only be applied to strictly p
inversa recupera el precio: True
outliers 1,5 IQR: crudo 612 | en log 92
Normalizer (cada fila a norma 1): [[0.6, 0.8], [0.7071, 0.7071]]
```

El log baja la asimetría de 2,24 a 0,18 y los outliers por la regla de 1,5 IQR de 612 a 92: los acerca, no los elimina. `Normalizer` trabaja por fila: (3, 4) pasa a (0,6; 0,8).

### 8. Chi cuadrado para dos categóricas
**En clase:** C4P1 59:01

José menciona la tabla de contingencia y la prueba chi cuadrado de independencia para medir relación entre categóricas, que la correlación de Pearson no cubre C4P1 59:01.

Qué tenés que hacer:
- Armá la tabla con `pd.crosstab` y pasala a `scipy.stats.chi2_contingency`.
- Chequeá que las frecuencias esperadas sean al menos 5.
- Con miles de filas casi todo da significativo: reportá también la V de Cramér.

```python
# g09_chi2.py
import pandas as pd
from scipy.stats import chi2_contingency

df = pd.read_csv("data/melb_data.csv")
tabla = pd.crosstab(df.Type, df.Method)
print(tabla)
chi2, p, dof, esperado = chi2_contingency(tabla)
print(f"chi2={chi2:.1f} gl={dof} p={p:.2e}")
print("esperados mínimos:", esperado.min().round(1), "(regla: todos >= 5)")
n = tabla.values.sum()
v = (chi2 / (n * (min(tabla.shape) - 1))) ** 0.5
print(f"V de Cramér={v:.3f} (la fuerza de la asociación; p chico con n grande no es lo mismo que efecto grande)")
```

Lo que da en el box:
```text
Method    PI     S  SA    SP   VB
Type                             
h       1069  6507  66  1079  728
t        134   723   7   143  107
u        361  1792  19   481  364
chi2=120.1 gl=8 p=3.18e-22
esperados mínimos: 7.5 (regla: todos >= 5)
V de Cramér=0.066 (la fuerza de la asociación; p chico con n grande no es lo mismo que efecto grande)
```

Tipo de propiedad y método de venta no son independientes (p ≈ 3 × 10⁻²²), pero la asociación es muy débil (V = 0,066).

### 9. SQL desde Python con SQLAlchemy
**En clase:** C4P1 1:02:22, C4P1 1:03:29, C4P1 1:08:05, C4P1 1:14:45, C4P1 1:18:45, C4P1 1:20:21, C4P2 0:33

Ariel usa la notebook "02 SQL": carga la encuesta de sueldos 2020 en SQLite con `to_sql` y la consulta con SQL C4P1 1:14:45.

Qué tenés que hacer:
- Creá el motor con `create_engine("sqlite:///archivo.sqlite3")` y volcá con `df.to_sql(..., if_exists="replace", index=False)`.
- En SQLAlchemy 2 las consultas van con `text(...)` dentro de `with engine.connect() as conn:`; el string crudo de la notebook 2022 tira `ObjectNotExecutableError`.
- `pd.read_sql(consulta, engine)` te devuelve un DataFrame directo.
- Escribí la misma consulta en pandas para comprobar que da igual (es lo que pide el entregable 2).
- Si el archivo es grande, leé en chunks o filtrá en SQL antes de traer los datos.

```python
# g10_sql_sqlalchemy.py
import pandas as pd
from sqlalchemy import create_engine, text

URL = "https://cs.famaf.unc.edu.ar/~mteruel/datasets/diplodatos/sysarmy_survey_2020_processed.csv"
df = pd.read_csv("data/sysarmy_survey_2020_processed.csv")   # copia local de URL
print("encuesta:", df.shape)

engine = create_engine("sqlite:///out/sysarmy.sqlite3")
df.to_sql("survey", con=engine, if_exists="replace", index=False)

q_count = "SELECT COUNT(1) FROM survey WHERE salary_monthly_NETO > 100000"
q_group = """
SELECT profile_gender, ROUND(AVG(salary_monthly_NETO)) AS avg_salary, COUNT(*) AS n
FROM survey
WHERE profile_years_experience > 5
GROUP BY profile_gender
HAVING COUNT(*) > 100
ORDER BY avg_salary DESC
"""
with engine.connect() as conn:
    try:
        conn.execute(q_count)                 # así está en la notebook 2022
    except Exception as e:
        print("string crudo en SQLAlchemy 2:", type(e).__name__)
    print("netos > 100000:", conn.execute(text(q_count)).scalar())
print(pd.read_sql(q_group, engine))

pandas_version = (df[df.profile_years_experience > 5]
                  .groupby("profile_gender")
                  .agg(avg_salary=("salary_monthly_NETO", "mean"), n=("salary_monthly_NETO", "size"))
                  .query("n > 100").sort_values("avg_salary", ascending=False).round())
print(pandas_version)

total = 0
for chunk in pd.read_csv("data/sysarmy_survey_2020_processed.csv", chunksize=2000):
    total += (chunk.salary_monthly_NETO > 100000).sum()
print("mismo conteo leyendo en chunks:", total)
```

Lo que da en el box:
```text
encuesta: (6095, 48)
string crudo en SQLAlchemy 2: ObjectNotExecutableError
netos > 100000: 1657
  profile_gender  avg_salary     n
0         Hombre    117716.0  3116
1          Mujer     89313.0   450
                avg_salary     n
profile_gender                  
Hombre            117716.0  3116
Mujer              89313.0   450
mismo conteo leyendo en chunks: 1657
```

El conteo de netos mayores a 100.000 (1.657) coincide con la salida guardada en la notebook 2022.

### 10. Combinar Melbourne con Airbnb
**En clase:** C4P1 1:26:25, C4P1 1:31:53, C4P1 1:34:08, C4P2 5:39, C4P2 7:51, C4P2 10:41, C4P2 20:37, C4P2 21:43, C4P2 26:09, C4P2 30:56, C4P2 37:34

La notebook "03 Combinación de datasets" cruza las ventas con los avisos de Airbnb por código postal. El merge directo explota a unos 2 millones de filas, y la solución es agregar Airbnb por código antes de unir C4P2 20:37, C4P2 26:09.

Qué tenés que hacer:
- Leé solo las columnas necesarias con `usecols`.
- Normalizá la clave con `pd.to_numeric(errors="coerce")` y mirá cuántos quedan sin código (146).
- Medí la cobertura con `np.intersect1d` o `isin` antes de unir.
- Agregá con `groupby().agg(nombre=(col, func))` para que las columnas salgan con nombres claros.
- Usá `validate="many_to_one"` en el merge final; con `one_to_one` pandas tira `MergeError`.
- Normalizá también `state` ("VIC", "Victoria", "Vic", "vic" y una veintena de variantes más) si lo vas a usar.
- Ojo: `unique()` cuenta el NaN como un valor; los 248 códigos de Airbnb son 247 reales más el NaN.

```python
# g11_merge_airbnb.py
import numpy as np
import pandas as pd

melb = pd.read_csv("data/melb_data.csv")
cols = ["description", "neighborhood_overview", "street", "neighborhood", "city", "suburb",
        "state", "zipcode", "price", "weekly_price", "monthly_price", "latitude", "longitude"]
air = pd.read_csv("data/cleansed_listings_dec18.csv", usecols=cols, low_memory=False)
print("airbnb:", air.shape, "| zipcode dtype:", air.zipcode.dtype)
print(air.zipcode.value_counts().head(3).to_dict())
air["zipcode"] = pd.to_numeric(air.zipcode, errors="coerce")
print("3000 tras to_numeric:", int((air.zipcode == 3000).sum()), "| no numéricos:", int(air.zipcode.isna().sum()))
print("variantes de state:", air.state.value_counts().head(4).to_dict())

inter = np.intersect1d(air.zipcode.dropna().values, melb.Postcode.values)
print("únicos airbnb", air.zipcode.nunique(dropna=False), "| melb", melb.Postcode.nunique(),
      "| en común", len(inter))
print(f"cobertura ventas {melb.Postcode.isin(inter).mean():.2%} | avisos {air.zipcode.isin(inter).mean():.2%}")

naive = melb.merge(air, how="left", left_on="Postcode", right_on="zipcode")
print("merge directo:", len(naive), "filas")
print("'85 Turner St' aparece", int((naive.Address == "85 Turner St").sum()), "veces")
try:
    melb.merge(air, left_on="Postcode", right_on="zipcode", validate="one_to_one")
except pd.errors.MergeError as e:
    print("validate='one_to_one':", type(e).__name__, "|", str(e)[:60])

agg = (air.groupby("zipcode")
          .agg(airbnb_record_count=("price", "count"), airbnb_price_mean=("price", "mean"),
               airbnb_weekly_price_mean=("weekly_price", "mean"),
               airbnb_monthly_price_mean=("monthly_price", "mean"))
          .reset_index())
print(agg[agg.zipcode.isin([2010, 3000])].round(1).to_string(index=False))

merged = melb.merge(agg, how="left", left_on="Postcode", right_on="zipcode", validate="many_to_one")
print("tras agregar:", len(merged), "filas | sin dato de airbnb:", int(merged.airbnb_price_mean.isna().sum()))
print("corr Price vs precio medio airbnb:", round(merged.Price.corr(merged.airbnb_price_mean), 3))
agg.to_csv("out/airbnb_price_by_zipcode.csv", index=False)

a = pd.DataFrame({"k": [1, 2]}).set_index("k"); b = pd.DataFrame({"v": [10, 30]}, index=[1, 3])
print("join por defecto (left):", a.join(b).v.tolist(), "| merge por defecto (inner):",
      len(a.reset_index().merge(b.rename_axis("k").reset_index(), on="k")))
```

Lo que da en el box:
```text
airbnb: (22895, 13) | zipcode dtype: str
{'3000': 3367, '3006': 1268, '3182': 1135}
3000 tras to_numeric: 3367 | no numéricos: 146
variantes de state: {'VIC': 21858, 'Victoria': 876, 'Vic': 38, 'vic': 10}
únicos airbnb 248 | melb 198 | en común 191
cobertura ventas 99.85% | avisos 93.03%
merge directo: 2139684 filas
'85 Turner St' aparece 258 veces
validate='one_to_one': MergeError | Merge keys are not unique in either left or right dataset; n
 zipcode  airbnb_record_count  airbnb_price_mean  airbnb_weekly_price_mean  airbnb_monthly_price_mean
  2010.0                    1               40.0                       NaN                        NaN
  3000.0                 3367              150.5                     918.7                     3407.2
tras agregar: 13580 filas | sin dato de airbnb: 20
corr Price vs precio medio airbnb: 0.199
join por defecto (left): [10.0, nan] | merge por defecto (inner): 1
```

Todos los números de Ariel se reproducen: 22.895 avisos, 3.367 en el 3000, 146 sin código, 248 / 198 / 191 códigos, 99,85% y 93,03% de cobertura, 2.139.684 filas en el merge directo con "85 Turner St" repetida 258 veces, y 13.580 filas con 20 sin dato tras agregar. Un detalle de versión: con pandas 3 y `low_memory=False` el zipcode se lee todo como texto, así que no ves la mezcla de "3000.0" (2.491) y "3000" (876) que aparece en la clase C4P2 8:26; con pandas 2 y la lectura por bloques sí aparece. La correlación entre el precio de venta y el precio medio de Airbnb del código postal es baja (0,199): suma algo de información de zona, pero no reemplaza a las variables de la propiedad.

### 11. Un ETL chico con capas bronce, plata y oro
**En clase:** C4P2 40:24, C4P2 43:47, C4P2 45:27, C4P2 54:23, C4P2 57:06, C4P2 1:04:32, C4P2 1:22:51

Ariel muestra una notebook ilustrativa de ETL con logging, SQLAlchemy contra Postgres y un DAG de Airflow `extract >> transform >> load`, que no corre en Colab C4P2 57:06, y explica la arquitectura medallion C4P2 1:04:32. El script de abajo arma lo mismo en chico y corriendo de verdad: bronce en Parquet con los datos crudos de Airbnb, plata con tipos y formatos normalizados (acá va el formateo, no en oro), oro con el agregado por código postal, y una carga final en SQLite con el JOIN hecho en SQL, que es lo que pide el entregable 2. En vez de Airflow uso `graphlib` de la biblioteca estándar para ordenar las tareas; la idea del DAG es la misma.

Qué tenés que hacer:
- Una función por etapa y un `main` que las corra en orden, con logging en cada paso.
- Guardá cada capa por separado para poder rehacer la siguiente sin volver a extraer.
- Contá cuántas filas descartás en plata y por qué.
- No pongas credenciales en el código ni en GitHub; leelas de variables de entorno C4P2 1:31:06.

```python
# g12_etl_medallion.py
import logging
from graphlib import TopologicalSorter
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
log = logging.getLogger("etl")
LAKE = Path("out/lake")
SRC = "data/cleansed_listings_dec18.csv"
COLS = ["zipcode", "state", "price", "weekly_price", "monthly_price", "last_scraped"]

def extract():
    """bronce: los datos tal como llegan, solo se fija el tipo texto para no perder nada"""
    raw = pd.read_csv(SRC, usecols=COLS, dtype=str)
    (LAKE / "bronze").mkdir(parents=True, exist_ok=True)
    raw.to_parquet(LAKE / "bronze/airbnb.parquet", index=False)
    log.info("bronce: %d filas", len(raw))

def transform_silver():
    """plata: tipos, formatos y valores normalizados; acá va el formateo"""
    b = pd.read_parquet(LAKE / "bronze/airbnb.parquet")
    s = pd.DataFrame({
        "zipcode": pd.to_numeric(b.zipcode, errors="coerce").astype("Int64"),
        "state": b.state.str.strip().str.upper().replace({"VICTORIA": "VIC"}),
        "price": pd.to_numeric(b.price, errors="coerce"),
        "weekly_price": pd.to_numeric(b.weekly_price, errors="coerce"),
        "monthly_price": pd.to_numeric(b.monthly_price, errors="coerce"),
        "scraped_at": pd.to_datetime(b.last_scraped, errors="coerce"),
    })
    bad = s.zipcode.isna() | (s.price <= 0)
    log.info("plata: %d filas, %d descartadas por zipcode o precio inválido", (~bad).sum(), bad.sum())
    (LAKE / "silver").mkdir(exist_ok=True)
    s[~bad].to_parquet(LAKE / "silver/airbnb.parquet", index=False)

def transform_gold():
    """oro: lógica de negocio, agregado por código postal"""
    s = pd.read_parquet(LAKE / "silver/airbnb.parquet")
    g = (s.groupby("zipcode")
          .agg(n=("price", "size"), price_mean=("price", "mean"),
               weekly_mean=("weekly_price", "mean"), monthly_mean=("monthly_price", "mean"))
          .reset_index())
    (LAKE / "gold").mkdir(exist_ok=True)
    g.to_parquet(LAKE / "gold/airbnb_by_zipcode.parquet", index=False)
    log.info("oro: %d códigos postales", len(g))

def load():
    """carga: ventas y oro a SQLite, y el JOIN en SQL (como pide el entregable 2)"""
    engine = create_engine("sqlite:///out/melb.sqlite3")
    pd.read_csv("data/melb_data.csv").to_sql("sales", engine, if_exists="replace", index=False)
    pd.read_parquet(LAKE / "gold/airbnb_by_zipcode.parquet").to_sql(
        "airbnb_by_zipcode", engine, if_exists="replace", index=False)
    q = """
    SELECT COUNT(*) AS filas, SUM(a.price_mean IS NULL) AS sin_airbnb,
           ROUND(AVG(s.Price)) AS precio_venta_medio
    FROM sales s LEFT JOIN airbnb_by_zipcode a ON s.Postcode = a.zipcode
    """
    with engine.connect() as conn:
        log.info("JOIN en SQL: %s", dict(conn.execute(text(q)).mappings().one()))

# el DAG: extract >> silver >> gold >> load (en Airflow serían tareas con >>)
dag = {"silver": {"extract"}, "gold": {"silver"}, "load": {"gold"}}
tasks = {"extract": extract, "silver": transform_silver, "gold": transform_gold, "load": load}
order = list(TopologicalSorter(dag).static_order())
log.info("orden del DAG: %s", " >> ".join(order))
for name in order:
    tasks[name]()
```

Lo que da en el box:
```text
INFO orden del DAG: extract >> silver >> gold >> load
INFO bronce: 22895 filas
INFO plata: 22728 filas, 167 descartadas por zipcode o precio inválido
INFO oro: 247 códigos postales
INFO JOIN en SQL: {'filas': 13580, 'sin_airbnb': 20, 'precio_venta_medio': 1075684.0}
```

Plata descarta 167 filas (146 sin código postal y 21 con precio 0 o inválido), así que oro queda con 247 códigos. No se pierde ninguno real: los 248 "únicos" de la notebook cuentan el NaN como un código más (`unique()` incluye el NaN). Ojo también con `state`: además de "VIC", "Victoria", "Vic" y "vic" hay valores como "Melbourne", "VIC 3008", "NSW" o en chino; la normalización del script solo resuelve los casos comunes. El JOIN en SQL da las mismas 13.580 filas y 20 sin dato que el merge de pandas de la sección 10. Si querés llevarlo a Airflow, cada función pasa a ser una tarea y las dependencias se escriben `extract >> silver >> gold >> load`; ese DAG no lo probé en el box porque Airflow no está instalado.

### 12. Los entregables
**En clase:** C1P1 8:24, C2P2 2:28:29, C3P1 6:44, C3P1 11:05, C4P2 1:22:51, C4P2 1:25:36

**Entregable 1** (fecha: 14 de mayo de 2026 C3P1 11:05). Con Melbourne: análisis de variables, encoding justificado, imputación con KNN, PCA e informe para una empresa C2P2 2:28:29. Pasos sugeridos:
1. Definí un objetivo (por ejemplo, estimar el precio) y elegí las columnas en función de eso; descartá IDs, texto libre (Address) y columnas sin varianza C3P1 6:44 (sección 2).
2. Documentá cada decisión de limpieza: qué pasaste a NaN, qué filas sacaste por cuantil y cuántas (secciones 2 y 4).
3. Codificá Type, Method y Regionname con one hot; para Suburb pensá si vale la pena (314 columnas) o si alcanza Regionname o el código postal (sección 5).
4. Imputá BuildingArea y YearBuilt con `KNNImputer` sobre variables estandarizadas, compará histogramas antes y después y probá dos o tres valores de k (sección 4).
5. Corré PCA sobre las numéricas estandarizadas, reportá la varianza explicada y explicá los loadings de las dos primeras (sección 6).
6. Escribí el informe sin jerga: qué datos había, qué problemas encontraste, qué hiciste y qué queda abierto.

**Entregable 2** (fecha: para verificar en el aula; en clase se dijo "15 días después" del 1 C4P2 1:25:36). Con Melbourne en SQLite: consultas en SQL equivalentes a las de pandas, el JOIN con Airbnb en SQL, y revisión de faltantes, dispersión y distribuciones; bonus opcionales con un script ETL o embeddings C4P2 1:22:51. Pasos sugeridos:
1. Cargá `melb_data.csv` y la tabla agregada de Airbnb por código postal en SQLite (sección 11, función `load`).
2. Para cada consulta, escribila en SQL y en pandas y comprobá que den lo mismo (sección 9).
3. Hacé el `LEFT JOIN` por código postal y verificá que no cambie la cantidad de filas (sección 10).
4. Si hacés el bonus de ETL, separá extracción, transformación y carga en funciones con logging (sección 11).
