# 12 — Formulario

Este formulario no es un cheat sheet seco. Cada bloque viene con: (a) qué hace cada argumento, (b) cuándo conviene usarlo, (c) la trampa típica. Si copiás sin entender, vas a romper el pipeline en el primer dataset distinto al de la clase.

---

## Pandas básico (inspección y copias)

### `df.info()` — radiografía estructural

```python
df.info()
```

- Muestra dtype, cantidad de no-nulos y memoria por columna.
- **Usalo primero**, antes de cualquier transformación: te dice si una columna numérica entró como `object` (señal de comas, espacios o NaN no parseados).

### `df.describe()` — resumen numérico

```python
df.describe()                       # solo numéricas
df.describe(include='object')       # solo categóricas
df.describe(include='all')          # todo
```

- Numéricas: count, mean, std, min, 25%, 50%, 75%, max.
- Comparar **mean vs 50% (mediana)**: si difieren mucho, hay asimetría.
- `min == 0` en variables que no pueden ser 0 (Landsize, BuildingArea) = faltantes enmascarados.

### `df.isnull().sum()` — conteo de faltantes

```python
missing = df.isnull().sum()
missing[missing > 0].sort_values(ascending=False)
(df.isnull().sum() / len(df) * 100).round(2)   # en %
```

- Si el % es bajo y los datos son MCAR, podés `dropna`.
- Si el % supera 80% en una columna, evaluá descartarla entera.

### `df.copy()` — operar sin tocar el original

```python
melb_df = melb_data.copy()
```

- **Regla de oro de la clase 1**: jamás operar sobre el DataFrame original.
- Una asignación normal (`df2 = df1`) crea una referencia, no una copia. Modificar `df2` muta `df1`.

### `dropna` / `fillna`

```python
df.dropna()                         # filas con CUALQUIER NaN
df.dropna(subset=['Price'])         # sólo si NaN en Price
df.dropna(axis=1, thresh=0.2*len(df))# columnas con <20% no-nulos

df['Car'] = df['Car'].fillna(0)
df['Council'] = df['Council'].fillna(df['Council'].mode()[0])
df.fillna({'Car': 0, 'Bathroom': df.Bathroom.median()})
```

- `dropna` directo es una decisión: documentala. Si la pérdida no es MCAR, sesgás.
- `fillna(0)` es válido para variables donde 0 tiene significado real (cocheras = sin auto); roto para Landsize o BuildingArea.

### Detección de ceros enmascarados

```python
zero_counts = melb_data[melb_data == 0].count(axis=0)
zero_counts[zero_counts > 0]

melb_df.loc[melb_df.Bathroom < 1, 'Bathroom'] = pd.NA
```

- `pd.NA` es el faltante "tipo-agnóstico" de pandas moderno; en columnas float también podés usar `np.nan`.

---

## Faltantes con sklearn

### `SimpleImputer`

```python
from sklearn.impute import SimpleImputer

imp = SimpleImputer(strategy='mean')            # numéricas
imp = SimpleImputer(strategy='median')          # numéricas con outliers
imp = SimpleImputer(strategy='most_frequent')   # categóricas
imp = SimpleImputer(strategy='constant',
                    fill_value=999)             # marcador explícito

X_imp = imp.fit_transform(X)
```

- `strategy`: define la regla. `mean` y `median` exigen numéricas.
- `fill_value`: sólo si `strategy='constant'`. Útil para categóricas (agrega una categoría nueva tipo `"Desconocido"`).
- Trampa: opera **a nivel columna**, ignora correlaciones → sesga si la pérdida no es MCAR.
- `fit_transform` devuelve un `numpy.ndarray`, **no un DataFrame**. Si querés conservar columnas, envolvelo en `pd.DataFrame(..., columns=X.columns)`.

### `KNNImputer`

```python
from sklearn.impute import KNNImputer

knn = KNNImputer(n_neighbors=3, weights='uniform')
X_imp = knn.fit_transform(X_num_scaled)
```

- `n_neighbors`: cuántos vecinos promediar. Pocos = más varianza; muchos = más sesgo.
- `weights`: `'uniform'` promedia, `'distance'` pondera por distancia inversa.
- **Requisito**: variables numéricas y **estandarizadas** (la distancia euclídea es sensible a la escala). Sin escalar, la columna de mayor magnitud domina.

### `IterativeImputer` (MICE)

```python
from sklearn.experimental import enable_iterative_imputer   # noqa
from sklearn.impute import IterativeImputer
from sklearn.linear_model import BayesianRidge
from sklearn.neighbors import KNeighborsRegressor

mice = IterativeImputer(estimator=BayesianRidge(),
                        max_iter=10, random_state=10)
mice_knn = IterativeImputer(estimator=KNeighborsRegressor(n_neighbors=5),
                            random_state=10)

X_imp = mice.fit_transform(X)
```

- `estimator`: regresor que predice cada feature en función de las otras. Si no se setea, usa `BayesianRidge`.
- `max_iter`: cuántas rondas de imputación rotatoria antes de cortar.
- **Requiere todas las features numéricas**: encoding obligatorio antes.
- Es la opción del TP1 con `KNeighborsRegressor` como estimador.

---

## Encodings de variables categóricas

### `OrdinalEncoder`

```python
from sklearn.preprocessing import OrdinalEncoder

niveles = [[' Preschool', ' 1st-4th', ' 5th-6th', ' 7th-8th',
            ' 9th', ' 10th', ' 11th', ' 12th', ' HS-grad',
            ' Some-college', ' Assoc-voc', ' Assoc-acdm',
            ' Bachelors', ' Masters', ' Prof-school', ' Doctorate']]
enc = OrdinalEncoder(categories=niveles)
df['education_enc'] = enc.fit_transform(df[['education']])
```

- `categories`: lista de listas (una lista de orden por columna). Hace explícito el orden.
- **SÓLO para ordinales**. Usado sobre nominales (color, provincia) inventa un orden que el modelo va a tratar como real.

### `OneHotEncoder`

```python
from sklearn.preprocessing import OneHotEncoder

ohe = OneHotEncoder(drop='first', sparse_output=False,
                    handle_unknown='ignore')
X_ohe = ohe.fit_transform(df[['Type', 'Method', 'Regionname']])
df_ohe = pd.DataFrame(X_ohe,
                      columns=ohe.get_feature_names_out())
```

- `drop='first'`: elimina una columna por categoría (evita colinealidad perfecta).
- `sparse_output=False`: devuelve denso. Con alta cardinalidad, dejá `True` para ahorrar memoria.
- `handle_unknown='ignore'`: si en test aparece una categoría no vista, mete 0s en lugar de fallar.
- `get_feature_names_out()`: recupera los nombres de columna (clave para reconstruir el DataFrame en el TP1).

### `pd.get_dummies`

```python
dummies = pd.get_dummies(df['race'], drop_first=True, prefix='race')
df = pd.concat([df, dummies], axis=1).drop(columns=['race'])
```

- Atajo "pandas-native". Equivalente operativo a `OneHotEncoder` pero sin estado: no se reaplica al test.
- En pipelines de sklearn, preferí `OneHotEncoder` (es reusable).

### `DictVectorizer`

```python
from sklearn.feature_extraction import DictVectorizer

vec = DictVectorizer(sparse=True)
X = vec.fit_transform(df.to_dict(orient='records'))   # (13580, 332) esparsa
```

- Acepta lista de dicts y combina OHE de strings con paso directo de numéricas.
- Devuelve esparsa por defecto: chequear MB **antes** de convertir a densa.

---

## Escalado y transformaciones numéricas

Todos los scalers comparten la misma API: `.fit()`, `.transform()`, `.fit_transform()`. `.fit()` aprende los parámetros (mean, std, min, max, IQR, etc.) del **train**, y `.transform()` los aplica. **Nunca** hacer `fit` sobre test.

### `MinMaxScaler`

```python
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range=(0, 1))
X_mm = scaler.fit_transform(X)
```

- Lleva a un rango fijo `[a, b]` aplicando `(x − min) / (max − min)`.
- No cambia la forma. **Sensible a outliers**: un outlier estira la escala y comprime al resto.

### `MaxAbsScaler`

```python
from sklearn.preprocessing import MaxAbsScaler
X_ma = MaxAbsScaler().fit_transform(X)
```

- Divide por `|max|`. Resultado en `[-1, 1]` sin centrar.
- **Preserva la esparsidad**: por eso es el default para matrices ralas (OHE, TF-IDF). `StandardScaler` con `with_mean=True` rompería esparsas.

### `RobustScaler`

```python
from sklearn.preprocessing import RobustScaler
X_rs = RobustScaler().fit_transform(X)
```

- Aplica `(x − mediana) / IQR`.
- **Robusto a outliers**: ni el centro ni la escala se construyen con extremos.

### `StandardScaler` (z-score)

```python
from sklearn.preprocessing import StandardScaler
X_z = StandardScaler().fit_transform(X)
# [10,20,30,40,50] → [-1.41, -0.71, 0, 0.71, 1.41]
```

- Aplica `(x − mean) / std`. Media 0, varianza 1.
- Asume distribución aproximadamente simétrica. Con outliers fuertes, conviene `RobustScaler`.

### `Normalizer` (l1, l2, max)

```python
from sklearn.preprocessing import Normalizer
X_norm = Normalizer(norm='l2').fit_transform(X)
```

- **Normaliza filas** (cada muestra con norma 1). No columnas.
- Sirve para similitud coseno, kernels, NLP. Confundirlo con `StandardScaler` es uno de los errores más comunes.

### `QuantileTransformer`

```python
from sklearn.preprocessing import QuantileTransformer
qt = QuantileTransformer(output_distribution='normal',
                         random_state=0)
X_qt = qt.fit_transform(X)
```

- `output_distribution`: `'uniform'` (rango [0,1]) o `'normal'`.
- Mapea cada valor a su cuantil empírico y proyecta a la distribución elegida.
- **Distorsiona correlaciones y distancias**: usar sólo cuando importa la forma marginal, no las relaciones.

### `PowerTransformer` (Box-Cox / Yeo-Johnson)

```python
from sklearn.preprocessing import PowerTransformer
bc = PowerTransformer(method='box-cox')        # requiere x > 0
yj = PowerTransformer(method='yeo-johnson')    # acepta negativos y ceros
X_yj = yj.fit_transform(X)
```

- Estima `λ` por máxima verosimilitud para aproximar a gaussiana.
- `λ = 0` ⇒ logaritmo. Por eso `log(x)` es un caso particular.
- Usar cuando el modelo asume normalidad o cuando el target tiene cola larga (precios, ingresos).

---

## PCA

### Ajuste y proyección

```python
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

X_std = StandardScaler().fit_transform(X)

pca = PCA(n_components=20)        # cantidad fija
pca = PCA(n_components=0.90)      # cantidad mínima para 90% de varianza
Z = pca.fit_transform(X_std)
```

- `n_components` entero: cantidad fija de componentes.
- `n_components` float ∈ (0,1): selecciona componentes hasta acumular esa proporción de varianza.
- `Z` queda con shape `(n_samples, n_components)`.

### Varianza explicada acumulada

$$
\text{VarExpAcum}(k) = \sum_{i=1}^{k} \frac{\lambda_i}{\sum_{j=1}^{m} \lambda_j}
$$

- **λᵢ** = autovalor asociado al i-ésimo componente principal.
- **m** = dimensión original.
- **k** = cantidad de componentes retenidos.
- Sirve para decidir el corte (típico: 90% o 95%).

```python
ev = pca.explained_variance_ratio_       # ej: [0.73, 0.23, 0.04, 0.005]
cumv = ev.cumsum()                       # [0.73, 0.96, 1.00, 1.00]
import matplotlib.pyplot as plt
plt.plot(range(1, len(cumv)+1), cumv, 'o-')
plt.axhline(0.9, ls='--')
```

- En el ejemplo Iris (4 features), PC1 + PC2 = 95.8%.
- **Sin escalar, todo cambia**: en el mismo Iris, con MinMax la PC1 explicaba ≈17% y con Standard ≈2.2%. Por eso PCA sin escalar previo NO sirve.

---

## EDA con seaborn

### Numéricas

```python
import seaborn as sns
import matplotlib.pyplot as plt

sns.histplot(df['Price'].dropna(), bins=50, kde=False)
plt.ticklabel_format(style='plain', axis='x')   # evitar notación científica

sns.boxplot(data=df, x='Price')
```

- `dropna()` antes del plot: histplot no falla con NaN, pero `kde` sí.
- `ticklabel_format(style='plain')`: clave en precios grandes; sin esto Matplotlib muestra `1e6` y nadie entiende.

### Categóricas

```python
df['Type'].value_counts()
df['Type'].value_counts().plot(kind='bar')

cats = df.select_dtypes(include='object').columns
pd.DataFrame({
    'columna': cats,
    'cant_categorias': [df[c].nunique(dropna=True) for c in cats],
    'nulos': [df[c].isnull().sum() for c in cats],
}).sort_values('cant_categorias', ascending=False)
```

- `nunique(dropna=True)`: cardinalidad real, sin contar el NaN como una categoría más.

### Bivariadas

```python
# Cat × num
sns.boxplot(data=df, x='Type', y='Price')

# Num × num
sns.scatterplot(data=df, x='BuildingArea', y='Price',
                hue='is_price_outlier', alpha=0.5)
```

### Matriz de correlaciones

```python
num_df = df.select_dtypes(include=['number'])
corr = num_df.corr().abs()
sns.heatmap(corr, cmap='coolwarm', annot=False)

# Ranking de correlación con el target
corr['Price'].sort_values(ascending=False).head(10)
```

- `.abs()` para ver fuerza, sin que se compensen positivos con negativos.
- En `melb_data`: Rooms (0.497), Bedroom2 (0.476), Bathroom (0.467), YearBuilt (0.324).

### Series temporales

```python
df['date'] = pd.to_datetime(df.Date, format='%d/%m/%Y')
df['date_month'] = pd.to_datetime(df.date.dt.strftime('%Y-%m'))
sns.lineplot(data=df, x='date_month', y='Price', estimator='mean')
```

- `format=`: explícito siempre. Sin formato, pandas adivina y a veces invierte día/mes.

### ydata_profiling

```python
from ydata_profiling import ProfileReport
ProfileReport(df, title='Melb EDA').to_file('report.html')
```

- **Complemento**, no reemplazo: ayuda a barrer, no piensa por vos.

---

## Outliers por IQR (cálculo paso a paso)

```python
q1, q3 = df['Price'].quantile([0.25, 0.75])
iqr = q3 - q1
lower = q1 - 1.5 * iqr
upper = q3 + 1.5 * iqr

is_outlier = (df['Price'] < lower) | (df['Price'] > upper)
df_clean = df.loc[~is_outlier].copy()
df_outliers = df.loc[is_outlier].copy()
print(f"Outliers detectados: {is_outlier.sum()}")
```

- `1.5 × IQR` es la regla operativa estándar; `3 × IQR` se reserva para "outliers extremos".
- Para boxplot: esos valores ya son los puntos individuales que se grafican fuera de los bigotes.
- Para `melb_data.Price`: Q1≈650K, Q3≈1.33M, IQR≈680K, límite superior≈2.35M, 612 outliers detectados.

---

## Combinación de DataFrames

### Merge básico y por columnas distintas

```python
# Misma columna en ambos
m1 = df1.merge(df2, on='Postcode', how='left')

# Columnas con nombres distintos
m2 = melb_df.merge(airbnb_by_zip,
                   left_on='Postcode', right_on='zipcode',
                   how='left')
```

- `how`: `'inner'` (default), `'left'`, `'right'`, `'outer'`.
- `on`: cuando la columna se llama igual en ambos.
- `left_on` / `right_on`: cuando los nombres difieren. Ojo: deja ambas columnas en el resultado.

### Agregación previa al merge (anti-explosión)

```python
relevant = ['price', 'weekly_price', 'monthly_price', 'zipcode']
airbnb_by_zip = (airbnb_df[relevant]
    .groupby('zipcode')
    .agg({'price': ['mean', 'count'],
          'weekly_price': 'mean',
          'monthly_price': 'mean'})
    .reset_index())
# Aplanar MultiIndex de columnas
airbnb_by_zip.columns = [' '.join(c).strip()
                          for c in airbnb_by_zip.columns.values]
```

- Si una clave aparece N veces en cada lado, el merge devuelve N×M filas (en TP2 ingenuo: 2 millones).
- Solución: agregar primero a un nivel donde la clave sea única.

### Validación post-merge

```python
assert len(merged) == len(melb_df), 'El merge cambió filas'
assert merged['Price'].isna().sum() == 0
assert merged['airbnb_price_mean'].dropna().between(0, 10000).all()

# Claves comunes
import numpy as np
intersection = np.intersect1d(airbnb_df.zipcode.values,
                              melb_df.Postcode.values)
```

- Tres preguntas obligadas: ¿cambiaron las filas?, ¿aparecieron nulos donde no debía?, ¿los rangos siguen siendo plausibles?

---

## SQL (SQLite)

### Sintaxis completa con cada cláusula

```sql
SELECT DISTINCT col1, col2, AGG(col3) AS alias
FROM tabla
JOIN otra ON tabla.id = otra.tabla_id
WHERE col1 > 10
GROUP BY col1, col2
HAVING AGG(col3) > 100
ORDER BY alias DESC
LIMIT 50 OFFSET 0;
```

Orden lógico de ejecución (no de escritura): **FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT**.

### Filtro y conteo

```sql
SELECT * FROM survey WHERE salary_monthly_NETO > 100000 LIMIT 10;

SELECT COUNT(1) FROM survey WHERE salary_monthly_NETO > 100000;
```

- `COUNT(1)` y `COUNT(*)` son equivalentes en SQLite. `COUNT(col)` cuenta no-nulos.

### Agregaciones con filtro

```sql
SELECT AVG(salary_monthly_NETO)
FROM survey
WHERE profile_gender = 'Mujer';
```

### GROUP BY simple

```sql
SELECT profile_gender, AVG(salary_monthly_NETO) AS avg_salary
FROM survey
GROUP BY profile_gender;
```

### GROUP BY múltiple + HAVING + ORDER BY

```sql
SELECT profile_gender,
       work_province,
       AVG(salary_monthly_NETO) AS avg_salary,
       COUNT(1) AS n
FROM survey
WHERE profile_years_experience > 5
GROUP BY profile_gender, work_province
HAVING COUNT(*) > 10
ORDER BY avg_salary DESC;
```

- `WHERE` filtra **filas** antes de agrupar; `HAVING` filtra **grupos** después de agregar. Confundirlos rompe el query.

### Top con HAVING

```sql
SELECT composer, COUNT(trackid) AS cant
FROM tracks
WHERE composer <> ''
GROUP BY composer
HAVING cant > 30
ORDER BY cant DESC
LIMIT 10;
```

### JOIN básico

```sql
SELECT title, name
FROM albums
INNER JOIN artists ON artists.artistId = albums.artistId;
```

- `INNER`: sólo filas con match en ambos lados.
- `LEFT`: todos los del izquierdo + NaN para los del derecho sin match.
- Sin `ON`, JOIN es un producto cartesiano: explosión.

---

## SQLAlchemy + pandas

### Conexión y carga

```python
from sqlalchemy import create_engine, text
import pandas as pd

# SQLite local
engine = create_engine('sqlite:///sysarmy.sqlite3', echo=False)

# PostgreSQL (ETL clase 4)
engine = create_engine(
    f'postgresql://{user}:{pwd}@{host}:{port}/{db}',
    echo=False, client_encoding='utf8')

# Volcar DataFrame a tabla
df.to_sql('survey', con=engine, if_exists='replace', index=False)
```

- `if_exists`: `'fail'` (default), `'replace'`, `'append'`.
- `echo=True` imprime cada query: útil para debug, ruidoso en producción.
- `index=False`: evitá escribir el índice de pandas como columna si no lo necesitás.

### Lectura — dos patrones

```python
# Patrón A: pandas.read_sql (devuelve DataFrame)
query = "SELECT * FROM survey WHERE salary_monthly_NETO > 100000"
df_result = pd.read_sql(query, con=engine)

# Patrón B: engine.connect() + text() (control granular)
with engine.connect() as conn:
    rs = conn.execute(text(query))
    df_result = pd.DataFrame(rs.fetchall(), columns=rs.keys())
```

- Patrón A es más corto y suele alcanzar.
- Patrón B sirve cuando ejecutás DDL (CREATE, ALTER), múltiples sentencias o necesitás controlar transacciones.

---

## Airflow (DAG mínimo)

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def extraer():
    # leer fuente
    pass

def transformar():
    # limpiar, agregar columnas, validar
    pass

def cargar():
    # persistir en DW
    pass

with DAG('mi_etl',
         start_date=datetime(2024, 1, 1),
         schedule_interval='@daily',
         catchup=False) as dag:

    t1 = PythonOperator(task_id='extraer',     python_callable=extraer)
    t2 = PythonOperator(task_id='transformar', python_callable=transformar)
    t3 = PythonOperator(task_id='cargar',      python_callable=cargar)

    t1 >> t2 >> t3
```

- `start_date`: cuándo arranca lógicamente la primera ejecución.
- `schedule_interval`: `'@daily'`, `'@hourly'`, expresión cron `'0 6 * * *'`, o `None` (manual).
- `catchup=False`: si ponés `True` y la `start_date` es del pasado, Airflow ejecuta TODAS las corridas atrasadas.
- `t1 >> t2 >> t3`: el operador `>>` define dependencias dirigidas. Sin ciclos: por eso es un **DAG**.
- Airflow **no procesa datos**: dispara tareas. La lógica real va en los `python_callable`.

### ETL completo (patrón clase 4)

```python
from sqlalchemy import create_engine, text
import pandas as pd, datetime as dt

def connection_db():
    return create_engine(
        f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/survey',
        echo=False, client_encoding='utf8')

def extract(url):
    return pd.read_csv(url)

def transformation(df, engine, tablename):
    df['fecha'] = dt.date.today()
    df.columns = df.columns.str.lower()
    df.to_sql(tablename, con=engine, if_exists='replace')

def load(engine):
    with engine.connect() as conn:
        conn.execute(text(open(SQL_SCRIPT).read()))
```

- Credenciales: `python-decouple` + `.env`, **nunca hardcodeadas**.
- Queries largas: archivo `.sql` separado, no string embebido.
- Logs: `logging`, no `print`.

---

## Recordatorios conceptuales

- **PCA sin escalar no sirve**: la columna con mayor varianza absoluta domina los componentes. Standard o MinMax obligatorio antes.
- **Encoding sobre NaN rompe el pipeline**: `OneHotEncoder` con faltantes tira error y `OrdinalEncoder` los pasa como categoría artificial. Siempre faltantes primero, encoding después.
- **MNAR no se imputa, se recolecta**. Cualquier imputación bajo MNAR mete sesgo silencioso.
- **KNN sin estandarizar es ruido**: la distancia euclídea infla la columna con mayor escala. Vale para KNNImputer y para el clasificador KNN.
- **`describe()` no detecta faltantes enmascarados**: si Landsize tiene 50% en cero, el `min` será 0 y la media bajará, pero nada gritará "faltante". Por eso se hace el check explícito de ceros.
- **Outlier no es lo mismo que dato erróneo**: el outlier es real pero raro, el erróneo es inválido. La decisión de qué hacer depende del objetivo, no de una regla.
- **`copy()` siempre**: en pandas, asignar es referenciar. Sin `copy()` mutás el original sin querer.
- **Validar post-merge con `assert`**: cantidad de filas, nulos esperados, rangos plausibles. El merge silencioso es el bug que más cuesta encontrar.
- **`HAVING` no es `WHERE`**: `WHERE` filtra filas antes de agrupar, `HAVING` filtra grupos después. Si querés filtrar por un agregado, va `HAVING`.
- **Airflow orquesta, no procesa**: la lógica va en las funciones que ejecuta cada `PythonOperator`. Si tu DAG corre lento, no es problema de Airflow.
- **`pd.read_sql` te ahorra horas**: cualquier query que devuelva una tabla, va a DataFrame en una línea. El patrón con `engine.connect()` se reserva para DDL o múltiples sentencias.
- **`drop_first=True` no es opcional en modelos lineales**: sin él, las columnas binarias son linealmente dependientes y los coeficientes se rompen.

---

**Próximo paso**: `13-preguntas-guia.md`
