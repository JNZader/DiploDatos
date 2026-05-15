# Guía de Trabajos Prácticos — EyCD 2026

## Cómo usar esta guía

Esta no es una "solución" de los TPs. Es la guía que te hubiera gustado tener cuando abriste el notebook por primera vez y leíste "Decidir si elimina algunas filas o columnas en base al análisis de datos faltantes" sin saber qué tenían en la cabeza los profes.

Acá vas a encontrar, para cada subejercicio:

1. **Qué pide la consigna** (con cita textual cuando importa).
2. **Qué archivos de estudio tenés que tener abiertos al lado**.
3. **El razonamiento previo al código** — la decisión, no la línea de Python.
4. **El código sugerido**, con explicación.
5. **Errores que la cátedra detecta seguro**.
6. **Qué conviene escribir en la celda de justificación** (porque sí, **la justificación pesa más que el código**).

> **Regla de oro de la materia**: *"No se espera una única solución correcta, pero sí que las decisiones estén justificadas y sean consistentes con los datos."*
>
> Si tu código corre pero no explicás por qué tomaste cada decisión, tu nota va a ser baja. Si tu código es razonable y justificás cada paso con criterio, aunque la decisión no sea la "ideal", la nota va a ser alta. La cátedra evalúa criterio, no perfección.

---

## Mapa general de los TPs

| TP | Ejercicio | Conceptos centrales | Archivos de estudio principales |
|----|-----------|---------------------|---------------------------------|
| **TP1** | Ej1 — Encoding | EDA, faltantes, dtype, OHE, cardinalidad, tratamiento de Date | `00`, `02`, `04`, `07` |
| **TP1** | Ej2 — Imputación KNN | IterativeImputer + KNeighborsRegressor, escalado | `02`, `05` |
| **TP1** | Ej3 — PCA | Reducción de dimensionalidad, escalado obligatorio | `06` |
| **TP1** | Ej4 — Composición | get_feature_names, reconstrucción de DataFrame | `04`, `00` |
| **TP1** | Ej5 — Documentación | Reproducibilidad técnica | — |
| **TP2** | Ej1 — SQL | SQLite + SQLAlchemy, queries, JOIN, validaciones | `10`, `08` |
| **TP2** | Ej2 — Pandas | Subset, outliers IQR, enriquecimiento, agregación por zipcode | `07`, `08` |
| **TP2** | Ej3 — Persistencia | Guardar dataset final | — |
| **TP2** | Ej4 — Opcionales | ETL, DAG, embeddings, LLM | `09` |

Los archivos numerados son los apuntes de estudio en este mismo directorio. Si nombro `02-datos-faltantes.md`, está al lado de este archivo.

---

# TP1 — Entregable parte 1

## El dataset: `melb_data`

El TP1 trabaja sobre `melb_data.csv` (Melbourne Housing Snapshot), descargado de:

```
https://cs.famaf.unc.edu.ar/~mteruel/datasets/diplodatos/melb_data.csv
```

**Tamaño**: 13.580 filas × 21 columnas.

**Faltantes según `melb_df.info()`** (recordá esto, lo vas a usar todo el TP):

| Columna | No-nulos | Faltantes |
|---------|----------|-----------|
| `Car` | 13.518 | 62 |
| `BuildingArea` | 7.130 | **6.450** |
| `YearBuilt` | 8.205 | **5.375** |
| `CouncilArea` | 12.211 | 1.369 |
| (resto) | 13.580 | 0 |

**Numéricas** (12 float + 1 int): Rooms, Price, Distance, Postcode, Bedroom2, Bathroom, Car, Landsize, BuildingArea, YearBuilt, Lattitude, Longtitude, Propertycount.

**Categóricas** (8 object): Suburb, Address, Type, Method, SellerG, Date, CouncilArea, Regionname.

> **Observación importante para todo el TP1**: `Postcode` y `Propertycount` están como `float64` aunque conceptualmente son enteros (Postcode es un identificador, Propertycount es un conteo). El profe en la consigna pregunta "¿Todas tienen el tipo `Dtype` correcto asignado?" — esto es justamente lo que te está marcando. Más adelante volvemos sobre esto.

---

## Ejercicio 1 — Encoding

### Qué pide la consigna (cita textual)

> "1. Seleccionar todas las filas y columnas del conjunto de datos, **excepto** `BuildingArea` y `YearBuilt`.
> 2. Decidir si elimina algunas filas o columnas en base al análisis de datos faltantes.
> 3. Hacer un análisis descriptivo de las variables numéricas del conjunto de datos. Todas tienen el tipo `Dtype` correcto asignado? Armar una matriz (array) sólo con las variables numéricas.
> 4. Estudiar las variables categóricas del DataFrame. Aplicar una codificación One-hot encoding a las columnas categóricas que crea pertinente. Si lo consideran necesario, pueden reducir el número de categorías únicas de algunas variables. ¿Cómo trataría la variable `Date`? Armar la matriz de variables categóricas codificada.
> 5. Concatenar la matriz de variables numéricas a la matriz que codifica las variables categóricas resultante del punto anterior."

### Archivos de estudio que tenés que tener abiertos

- `00-python-y-pandas-para-curacion.md` — cómo manipular DataFrames sin pisar el original.
- `02-datos-faltantes.md` — criterios de eliminación e imputación.
- `04-tipos-de-variables-y-encodings.md` — OrdinalEncoder vs OneHotEncoder, cardinalidad.
- `07-exploracion-eda.md` — describe, value_counts, primer vistazo.

---

### 1.1 Seleccionar filas/columnas excepto BuildingArea y YearBuilt

**Decisión**: trabajás sobre una **copia** y dejás afuera las dos columnas con más faltantes. Las vas a re-agregar en el Ejercicio 2 para imputarlas.

```python
import pandas

melb_df = pandas.read_csv(
    'https://cs.famaf.unc.edu.ar/~mteruel/datasets/diplodatos/melb_data.csv')

# IMPORTANTE: .copy() para no pisar el original. Es la primera regla de la materia.
work_df = melb_df.drop(columns=['BuildingArea', 'YearBuilt']).copy()
print(work_df.shape)  # (13580, 19)
```

**Errores a evitar**:

- **No hacer `.copy()`** y después modificar `work_df` afecta `melb_df` por SettingWithCopyWarning. Caso típico que la cátedra marca en Clase 1: *"NUNCA accionar sobre el dataset original"*.
- Confundir `drop(columns=...)` con `drop(...)` que sin axis por defecto borra filas. Sé explícito.

**Qué escribir en la celda de justificación**:
> "Excluimos `BuildingArea` (~47% faltantes) y `YearBuilt` (~40% faltantes) del flujo inicial de encoding por dos razones: (a) imputarlas requiere usar el resto de las variables como predictores, por lo que primero hay que tenerlas codificadas; (b) reincorporarlas tras encoding permite aplicar `IterativeImputer` con KNN sobre la matriz numérica completa, que es el método sugerido en Ejercicio 2."

---

### 1.2 Decidir eliminar filas/columnas según faltantes

Ahora que sacaste BuildingArea y YearBuilt, **¿qué queda con faltantes?**

```python
missing = work_df.isnull().sum()
missing[missing > 0].sort_values(ascending=False)
# CouncilArea    1369
# Car              62
```

**Análisis y decisión**:

| Columna | % faltante | Decisión sugerida | Razón |
|---------|-----------|-------------------|-------|
| `CouncilArea` | ~10% | **Imputar como categoría "Unknown"** o dropear filas | Es categórica. La media/mediana no aplica. Si la mantenés, agregás categoría "Unknown" en SimpleImputer(strategy='constant'); si la dropeás, perdés 10% de los datos, lo cual es mucho para suponer MCAR. |
| `Car` | ~0.46% | **Dropear filas o imputar con mediana** | Es numérica. 62 filas es despreciable. Si dropeás, asumís MCAR (razonable). Si imputás, mediana (es entera, count). |

**Código**:

```python
# Opción A: dropear filas con cualquier faltante (perdés ~10%)
clean_df = work_df.dropna().copy()
print(clean_df.shape)  # (~12150, 19) — perdés 1430 filas

# Opción B (más conservadora): dropear solo Car (62 filas) e imputar CouncilArea
clean_df = work_df.dropna(subset=['Car']).copy()
clean_df['CouncilArea'] = clean_df['CouncilArea'].fillna('Unknown')
print(clean_df.shape)  # (13518, 19)
```

**Errores a evitar**:

- Dropear filas con `dropna()` sin `subset` te elimina todo lo que tenga al menos un faltante, incluso si esa columna no la vas a usar. Sé específico.
- **No documentar el shape antes y después**. La cátedra quiere ver cuánto data perdiste.

**Qué escribir en la celda de justificación**:
> "Elegimos la opción B (dropear `Car` faltantes, imputar `CouncilArea` con 'Unknown') porque: (a) perder 10% de los datos por `CouncilArea` antes de modelar es agresivo dado que el mecanismo de faltantes podría ser MAR (depende de Suburb); (b) `Car` con 0.46% de faltantes es despreciable y descartarlos no introduce sesgo apreciable; (c) 'Unknown' como categoría explícita conserva la información de que el dato falta, lo cual el modelo puede aprovechar."

---

### 1.3 Análisis descriptivo numéricas, Dtype, matriz numérica

**Lo que pide explícitamente la consigna**: "Todas tienen el tipo `Dtype` correcto asignado?"

Esto no es retórico. Te está marcando que **hay variables mal tipadas**.

```python
numeric_cols = clean_df.select_dtypes(include=['number']).columns.tolist()
clean_df[numeric_cols].describe()
clean_df[numeric_cols].dtypes
```

**Lo que vas a encontrar**:

- `Rooms`: int64 (correcto).
- `Price`: float64 (correcto — dólares australianos con decimales).
- `Distance`: float64 (correcto — kilómetros).
- `Postcode`: float64 (**INCORRECTO** — debería ser categórica/string, es un identificador postal, NO tiene sentido sumar postcodes).
- `Bedroom2`, `Bathroom`, `Car`: float64 (técnicamente count → int, pero como Car tenía NaN, pandas las convirtió a float).
- `Landsize`: float64 (correcto — m²).
- `Lattitude`, `Longtitude`: float64 (correcto, pero **conceptualmente son coordenadas, no se promedian linealmente**).
- `Propertycount`: float64 (es un conteo entero, ahí no hay justificación).

**Decisiones razonables**:

```python
# Postcode tratarlo como categórica (es ID, no medible)
clean_df['Postcode'] = clean_df['Postcode'].astype(int).astype(str)

# Bedroom2, Bathroom, Car → int (después de imputar Car ya no hay NaN)
for col in ['Bedroom2', 'Bathroom', 'Car']:
    clean_df[col] = clean_df[col].astype(int)

# Propertycount → int
clean_df['Propertycount'] = clean_df['Propertycount'].astype(int)
```

**Lattitude/Longtitude**: las dejás como float, pero anotás que el promedio de latitudes carece de sentido geográfico (la cátedra lo menciona en Clase 4 cuando habla de geoespacial). Para PCA está bien tenerlas porque PCA trabaja con varianza, no con interpretabilidad espacial.

**La matriz numérica**:

```python
numeric_cols_final = ['Rooms', 'Price', 'Distance', 'Bedroom2', 'Bathroom',
                      'Car', 'Landsize', 'Lattitude', 'Longtitude',
                      'Propertycount']
X_num = clean_df[numeric_cols_final].values  # numpy array (n, 10)
print(X_num.shape, X_num.dtype)
```

**Errores a evitar**:

- No notar que **Postcode es ID, no número**. Es el típico error que demuestra que copiaste un EDA sin pensarlo.
- Mantener Postcode como float y meterlo a PCA: las componentes te van a salir dominadas por la varianza absoluta de Postcode (van de 3000 a 4000), que no significa nada.
- Promediar coordenadas geográficas en `describe()` sin aclarar que el número es decorativo.

**Qué escribir en la celda de justificación**:
> "Identificamos que `Postcode` y `Propertycount` están como `float64` pero conceptualmente son enteros. Convertimos `Postcode` a string porque es un identificador postal (no admite operaciones aritméticas significativas) y lo trataremos como categórica nominal en la siguiente etapa. `Propertycount`, `Bedroom2`, `Bathroom` y `Car` los convertimos a `int` por consistencia. Las coordenadas `Lattitude`/`Longtitude` quedan como `float` pero conceptualmente no son aritméticas (promediar latitudes carece de sentido geográfico); las incluimos en la matriz numérica porque PCA opera sobre varianza, no sobre semántica."

---

### 1.4 Categóricas + OHE + tratamiento de Date

Este punto es **el más cargado del TP1**. Tres decisiones se mezclan: cardinalidad, OHE y Date.

#### Inspección inicial

```python
cat_cols = clean_df.select_dtypes(include='object').columns.tolist()
cat_summary = pandas.DataFrame({
    'columna': cat_cols,
    'cant_unicos': [clean_df[c].nunique() for c in cat_cols],
    'nulos': [clean_df[c].isnull().sum() for c in cat_cols],
    'top1_freq': [clean_df[c].value_counts().iloc[0] for c in cat_cols],
}).sort_values('cant_unicos', ascending=False)
cat_summary
```

Lo que vas a ver:

| columna | cant_unicos | nulos | top1_freq |
|---------|-------------|-------|-----------|
| `Address` | ~13.000 | 0 | 1 |
| `SellerG` | ~270 | 0 | ~1900 |
| `Suburb` | ~310 | 0 | ~360 |
| `CouncilArea` | ~34 (con "Unknown") | 0 | ~1100 |
| `Date` | ~58 | 0 | ~470 |
| `Method` | 5 | 0 | ~9000 |
| `Type` | 3 | 0 | ~9000 |
| `Regionname` | 8 | 0 | ~4500 |
| `Postcode` (lo movimos acá) | ~200 | 0 | — |

#### Decisión por columna

| columna | Decisión | Razón |
|---------|----------|-------|
| `Address` | **Eliminar** | Cardinalidad ≈ N. OHE genera 13.000 columnas, todas con un único 1. Información nula. |
| `Suburb` | **Eliminar o reducir top-N** | 310 únicos. OHE explota. Alternativa: quedarse con top 30 + "Otros". Pero `Suburb` está muy correlacionado con `Postcode` y `Regionname`, así que se puede dropear. |
| `SellerG` | **Reducir top-N (10-20)** o eliminar | Similar a Suburb. La inmobiliaria que vendió no debería predecir el precio (sería data leakage si querés generalizar). |
| `Postcode` | **OHE top-N o frecuencia** | 200 únicos. Misma lógica que Suburb. |
| `CouncilArea` | **OHE completo** | 34 únicos es manejable. |
| `Type` | **OHE completo (drop_first=True)** | 3 únicos. |
| `Method` | **OHE completo (drop_first=True)** | 5 únicos. |
| `Regionname` | **OHE completo (drop_first=True)** | 8 únicos. |
| `Date` | **VER PUNTO ESPECIAL ABAJO** | — |

#### El nudo: Date

> "¿Cómo trataría la variable `Date`?"

La consigna **NO impone** una solución. Tenés tres alternativas razonables:

**Opción A — Descartar**:
- Asume que el precio no cambia con el tiempo dentro del período.
- En general MAL: el dataset cubre 2016-2017, hay variación estacional y de mercado.
- Justificable solo si demostrás que la correlación Date-Price es despreciable.

**Opción B — Convertir a numérica (ordinal: días desde mínimo)**:
```python
clean_df['Date'] = pandas.to_datetime(clean_df['Date'], format='%d/%m/%Y')
clean_df['days_since_start'] = (clean_df['Date'] - clean_df['Date'].min()).dt.days
clean_df = clean_df.drop(columns=['Date'])
```
- Convierte la fecha en una numérica continua.
- Captura tendencia temporal lineal.
- **Esta es la opción más limpia** y la que mejor justifica.

**Opción C — Descomponer en año-mes / cuatrimestre**:
```python
clean_df['Date'] = pandas.to_datetime(clean_df['Date'], format='%d/%m/%Y')
clean_df['year'] = clean_df['Date'].dt.year
clean_df['month'] = clean_df['Date'].dt.month
# o cuatrimestre
clean_df['quarter'] = clean_df['Date'].dt.quarter
```
- Captura estacionalidad.
- Costo: agregás 2-3 columnas, alguna de las cuales podés OHE'ar si la querés categórica.

**Recomendación práctica**: opción B (ordinal en días). La consigna dice "matriz de variables categóricas codificada", entonces Date va por el lado numérico, no categórico. Si querés ser elegante, agregás `month` como categórica adicional para estacionalidad.

> **La consigna no aclara qué hacer con Date, conviene asumir que la convertimos a numérica ordinal (días desde el inicio del período) porque captura tendencia temporal y evita explotar la dimensionalidad con un OHE de 58 fechas únicas. Justificarlo explícitamente.**

#### Código para OHE

```python
from sklearn.preprocessing import OneHotEncoder

# Columnas que sí se OHE'an (baja cardinalidad)
ohe_cols = ['Type', 'Method', 'Regionname', 'CouncilArea']

# Postcode: reducir a top 30 + Otros (alternativa: frecuencia)
top_postcodes = clean_df['Postcode'].value_counts().head(30).index.tolist()
clean_df['Postcode_reduced'] = clean_df['Postcode'].where(
    clean_df['Postcode'].isin(top_postcodes), 'Otros'
)
ohe_cols.append('Postcode_reduced')

# Eliminamos las de alta cardinalidad sin uso directo
clean_df = clean_df.drop(columns=['Address', 'Suburb', 'SellerG', 'Postcode'])

# OHE
encoder = OneHotEncoder(sparse_output=False, drop='first',
                        handle_unknown='ignore')
X_cat_encoded = encoder.fit_transform(clean_df[ohe_cols])

# Nombres de columnas resultantes (para el Ejercicio 4)
ohe_feature_names = encoder.get_feature_names_out(ohe_cols)
print(X_cat_encoded.shape)  # (~13518, ~70)
```

**Errores a evitar**:

- **OHE sobre `Suburb` o `Address` sin reducir cardinalidad**: te explota la matriz a 13.000+ columnas. La cátedra lo marca como ejemplo clásico del "curse of dimensionality" en `04-tipos-de-variables-y-encodings.md`.
- **OHE con `drop_first=False` por defecto** (en `pandas.get_dummies`): genera colinealidad perfecta entre las dummies. Usá `drop_first=True` o `drop='first'` (sklearn).
- **OHE sin `handle_unknown='ignore'`**: si después en producción aparece una categoría nueva, el encoder rompe. Es buena práctica aunque acá no tengamos "producción".
- **Olvidarse de guardar los `feature_names`**: en el Ejercicio 4 los vas a necesitar para reconstruir el DataFrame. Sin eso, tu matriz es un array anónimo.
- **OHE sobre NaN**: si Type tiene NaN (no lo tiene en este caso), OHE crea una columna `Type_nan`. Limpiá antes.

**Qué escribir en la celda de justificación**:
> "Decisiones de encoding:
> - **Eliminadas**: `Address` (cardinalidad = N, no aporta), `Suburb` (~310 únicos, correlacionado con Regionname/Postcode), `SellerG` (~270 únicos, podría introducir data leakage del proceso de venta).
> - **OHE completo**: `Type` (3), `Method` (5), `Regionname` (8), `CouncilArea` (34, incluyendo 'Unknown' como categoría explícita).
> - **OHE reducido**: `Postcode` (200 únicos), agrupando los menos frecuentes en 'Otros' (top 30). Alternativa válida: codificación de frecuencia.
> - **Date**: convertida a `days_since_start` (numérica ordinal) para capturar tendencia temporal sin explotar la dimensionalidad.
> Usamos `drop_first=True` para evitar colinealidad perfecta y `handle_unknown='ignore'` por robustez."

---

### 1.5 Concatenar numéricas + categóricas

```python
import numpy

# Reconstruir matriz numérica (con Date convertida + Bedroom2/etc. como int)
numeric_cols_final = ['Rooms', 'Price', 'Distance', 'Bedroom2', 'Bathroom',
                      'Car', 'Landsize', 'Lattitude', 'Longtitude',
                      'Propertycount', 'days_since_start']
X_num = clean_df[numeric_cols_final].values  # (~13518, 11)

# Concatenar
X = numpy.hstack([X_num, X_cat_encoded])
print(X.shape)  # (~13518, ~81)

# Guardar nombres totales para Ejercicio 4
all_feature_names = numeric_cols_final + list(ohe_feature_names)
assert X.shape[1] == len(all_feature_names)
```

**Errores a evitar**:

- `numpy.hstack` te exige que las matrices tengan el mismo número de **filas**. Si dropeaste filas en una y no en la otra, esto explota. Trabajá siempre sobre `clean_df` para que todo tenga la misma N.
- No guardar `all_feature_names` ordenado. En el Ej 4 la consigna explícita dice *"Ninguno de los métodos aplicados intercambia de lugar las columnas o las filas de la matriz"* — eso significa que el orden importa y te lo van a verificar.

**Qué escribir**:
> "La matriz final `X` tiene forma (~13518, ~81). Las primeras 11 columnas son numéricas (en el orden de `numeric_cols_final`), las restantes son las OHE categóricas (en el orden de `ohe_feature_names`). Mantener el orden es crítico para el Ejercicio 4 (reconstrucción)."

---

## Ejercicio 2 — Imputación KNN

### Qué pide la consigna (cita textual)

> "1. Agregue a la matriz obtenida en el punto anterior las columnas `YearBuilt` y `BuildingArea`.
> 2. Aplique una instancia de `IterativeImputer` con un estimador `KNeighborsRegressor` para imputar los valores de las variables. ¿Es necesario estandarizar o escalar los datos previamente?
> 3. Realice un gráfico mostrando la distribución de cada variable antes de ser imputada, y con ambos métodos de imputación."

### Archivos de estudio relevantes

- `02-datos-faltantes.md` — IterativeImputer, MICE, mecanismos MAR/MCAR/MNAR.
- `05-transformaciones.md` — StandardScaler vs MinMaxScaler.

### 2.1 Agregar YearBuilt y BuildingArea

```python
# Volvemos a buscarlas en el original (recordá que en 1.1 las habíamos sacado)
X_with_missing = numpy.hstack([
    X,  # las ~81 columnas ya procesadas
    melb_df.loc[clean_df.index, ['YearBuilt', 'BuildingArea']].values
])
print(X_with_missing.shape)  # (~13518, ~83)

# Sumar a los feature names
all_feature_names_v2 = all_feature_names + ['YearBuilt', 'BuildingArea']
```

**Trampa**: `clean_df.index` te garantiza que matcheás las mismas filas. Si reseteaste el índice en algún momento, esto te trae filas equivocadas.

---

### 2.2 IterativeImputer + KNeighborsRegressor — ¿estandarizar?

**La pregunta explícita de la consigna**: "¿Es necesario estandarizar o escalar los datos previamente?"

**Respuesta corta**: **SÍ, obligatorio**.

**Por qué**:

- `IterativeImputer` rota sobre cada feature usando un estimador (`KNeighborsRegressor` en este caso).
- KNN calcula **distancias euclídeas** entre filas.
- Si tus features tienen escalas dispares (Price en cientos de miles, Rooms entre 1 y 10, Lattitude entre −38 y −37), la distancia está dominada por Price. KNN va a "encontrar vecinos" basándose casi exclusivamente en Price, ignorando las demás.
- El apunte `02-datos-faltantes.md` lo dice textual: *"KNN exige numéricas ESTANDARIZADAS"*.
- El apunte `05-transformaciones.md` lo refuerza: *"Crítico antes de distancias (SVM, KNN, K-means)"*.

**Código**:

```python
from sklearn.preprocessing import StandardScaler
from sklearn.impute import IterativeImputer
from sklearn.neighbors import KNeighborsRegressor
from sklearn.experimental import enable_iterative_imputer  # noqa

# 1. Escalar (StandardScaler funciona también con OHE: la varianza queda chica
#    pero no rompe nada; alternativa: escalar solo las numéricas)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_with_missing)

# 2. IterativeImputer con KNN
imputer_knn = IterativeImputer(
    estimator=KNeighborsRegressor(n_neighbors=5),
    random_state=42,
    max_iter=10
)
X_imputed_scaled = imputer_knn.fit_transform(X_scaled)

# 3. Des-escalar para volver a la unidad original
X_imputed = scaler.inverse_transform(X_imputed_scaled)
```

**Comparación con baseline (imputación simple por mediana)** — útil para el gráfico del 2.3:

```python
from sklearn.impute import SimpleImputer

imputer_median = SimpleImputer(strategy='median')
X_imputed_median = imputer_median.fit_transform(X_with_missing)
```

**Errores a evitar**:

- **No escalar antes de KNN**: el resultado va a estar dominado por Price (escala más grande). Es el error más común y la cátedra lo detecta seguro.
- **Olvidar `from sklearn.experimental import enable_iterative_imputer`**: en versiones nuevas de sklearn ya no hace falta, pero por compatibilidad conviene ponerlo.
- **`max_iter` muy bajo (default = 10)**: si ves el `ConvergenceWarning: Early stopping criterion not reached`, podés subirlo o aceptarlo y documentarlo (la cátedra muestra ese warning en el notebook, no es bloqueante).
- **Confundir `IterativeImputer` con `KNNImputer`**: son distintos. `KNNImputer` imputa directamente con vecinos. `IterativeImputer` ajusta un modelo (acá KNN) iterativamente sobre cada feature usando las demás como predictores. La consigna pide explícitamente `IterativeImputer(estimator=KNeighborsRegressor)`.
- **No invertir el escalado**: si guardás `X_imputed_scaled`, las visualizaciones del 2.3 van a estar en unidades estandarizadas, no en dólares.

**Qué escribir en la celda de justificación**:
> "Sí, es necesario escalar antes de aplicar `IterativeImputer(KNeighborsRegressor)`. La razón es que KNN calcula distancias euclídeas entre filas, y nuestras features tienen escalas muy dispares (Price ~10⁶, Rooms ~1, Lattitude ~−37, días-desde-inicio ~10²). Sin escalar, la distancia entre filas está dominada por Price y los demás predictores son ignorados de hecho. Usamos `StandardScaler` (media 0, varianza 1) por ser estándar; `MinMaxScaler` también es válido. Tras imputar, invertimos el escalado para que las distribuciones queden en unidades originales (dólares, años, m²)."

---

### 2.3 Graficar antes/después

Conviene graficar las DOS variables que se imputaron: `YearBuilt` y `BuildingArea`.

```python
import matplotlib.pyplot as plt
import seaborn

fig, axes = plt.subplots(2, 2, figsize=(14, 8))

# Índices de YearBuilt y BuildingArea en la matriz
idx_yb = all_feature_names_v2.index('YearBuilt')
idx_ba = all_feature_names_v2.index('BuildingArea')

# YearBuilt
seaborn.histplot(melb_df['YearBuilt'].dropna(), ax=axes[0,0], color='steelblue')
axes[0,0].set_title('YearBuilt — Original (con NaN dropeados)')

seaborn.histplot(X_imputed_median[:, idx_yb], ax=axes[0,1], color='orange')
axes[0,1].set_title('YearBuilt — Imputado con Mediana')

# BuildingArea
seaborn.histplot(melb_df['BuildingArea'].dropna(), ax=axes[1,0], color='steelblue')
axes[1,0].set_title('BuildingArea — Original')
axes[1,0].set_xlim(0, 1000)  # cortar outliers para visualizar

seaborn.histplot(X_imputed[:, idx_ba], ax=axes[1,1], color='green')
axes[1,1].set_title('BuildingArea — Imputado con KNN')
axes[1,1].set_xlim(0, 1000)

plt.tight_layout()
```

**Qué tenés que observar**:

- **Mediana**: deja un pico artificial enorme en el valor de la mediana (alrededor de 1970 para YearBuilt y ~130 m² para BuildingArea). Es el caso de libro de "imputación que destruye la distribución".
- **KNN**: las distribuciones imputadas se parecen mucho más a las originales. Conserva colas, varianza, asimetría.

**Qué escribir**:
> "Comparando las distribuciones, observamos que: (a) la imputación por mediana introduce un pico artificial en el valor central, distorsionando la varianza y la forma de la distribución; (b) la imputación con `IterativeImputer(KNN)` produce distribuciones casi indistinguibles de las originales, conservando colas, asimetría y dispersión. Esto es consistente con la teoría: la imputación basada en modelos multivariados (MICE) preserva relaciones entre features, mientras que la imputación univariada (mediana) solo reproduce un estadístico central."

---

## Ejercicio 3 — PCA

### Qué pide la consigna (cita textual)

> "1. Aplique `PCA` para obtener $n$ componentes principales de la matriz, donde `n = min(20, X.shape[0])`. ¿Es necesario estandarizar o escalar los datos? Puede decidir si hacer PCA sobre todas las variables o bien seleccionar un subconjunto que crea pertinente.
> 2. Seleccione las proyecciones de los datos sobre las dos primeras componentes principales (las primeras dos columnas del resultado) para agregar como nuevas características al conjunto de datos."

### Archivo de estudio relevante

- `06-pca.md` — PCA, varianza explicada, escalado obligatorio.

### 3.1 PCA — el aviso del typo

**Atención**: `n = min(20, X.shape[0])`.

Si tomamos esto al pie de la letra:

- `X.shape[0]` es el **número de filas** = ~13.518.
- `min(20, 13518) = 20`.

Entonces n = 20. Eso es perfectamente válido.

**PERO**: leyendo la consigna en contexto (`X` tiene ~83 columnas), lo que tiene más sentido pedagógicamente es **`min(20, X.shape[1])` = `min(20, 83) = 20`**, que en este caso da el mismo número. Para una matriz con menos columnas (digamos 15), `min(20, X.shape[1]) = 15` evita el error de pedir más componentes que features.

**Recomendación**: mencionalo explícitamente.

> "La consigna usa `min(20, X.shape[0])`. Interpretamos que se trata de un typo y la intención era `min(20, X.shape[1])` (limitar n al número de features, no al número de filas, dado que PCA no puede generar más componentes que min(n_samples, n_features) menos el rango). En nuestro caso, con 13.518 filas y ~83 features, ambas expresiones dan el mismo valor `n=20`, así que la diferencia es semántica, no numérica. Si el dataset hubiera tenido <20 columnas, `X.shape[1]` sería el límite correcto."

### ¿Es necesario escalar?

**Respuesta**: **SÍ, obligatorio**. Y más obligatorio que en KNN.

Razones técnicas:

- PCA descompone la matriz de **covarianza** (o correlación si está escalada).
- Si una feature tiene escala 10⁶ (Price) y otra escala 1 (Rooms), la varianza de Price domina absolutamente.
- La primera componente principal va a ser, esencialmente, Price. No estás capturando estructura: estás capturando que Price tiene varianza grande.

El apunte `06-pca.md` lo dice: *"sklearn centra los datos restándoles la media. Sin embargo, es recomendable también estandarizar o al menos escalar la matriz original para asegurar que todas las variables estén en las mismas unidades y ninguna tenga un peso demasiado grande."*

El apunte `05-transformaciones.md`: *"PCA sin escalar → la columna con mayor varianza absoluta domina."*

**Si ya escalaste en el Ejercicio 2 con StandardScaler**: no hace falta escalar de nuevo, **siempre que mantengas el escalado**. Si invertiste el escalado para graficar, tenés que re-escalar.

```python
from sklearn.decomposition import PCA

# Re-escalar si invertiste el escalado en el Ej 2
scaler_pca = StandardScaler()
X_imputed_scaled = scaler_pca.fit_transform(X_imputed)

n_components = min(20, X_imputed_scaled.shape[1])  # 20
pca = PCA(n_components=n_components, random_state=42)
X_pca = pca.fit_transform(X_imputed_scaled)

# Inspeccionar varianza explicada
print("Varianza explicada por componente:", pca.explained_variance_ratio_)
print("Acumulada:", numpy.cumsum(pca.explained_variance_ratio_))
print(f"PC1+PC2 explican: {sum(pca.explained_variance_ratio_[:2])*100:.1f}%")
```

**Qué esperar**: con datos heterogéneos como melb_data (muchas OHE + numéricas), PC1+PC2 típicamente explican entre 15% y 30% de la varianza total. No es como Iris (que da 95%+) porque acá hay mucha más dimensionalidad efectiva.

**¿Hacer PCA sobre todo o sobre un subconjunto?**

La consigna te lo permite. Tres alternativas:

| Alternativa | Pro | Contra |
|-------------|-----|--------|
| **Todo (numéricas + OHE)** | Capta toda la estructura | OHE binarias tienen varianza Bernoulli (p·(1−p)), distorsiona PCs |
| **Solo numéricas** | PCs interpretables | Perdés señal categórica |
| **Numéricas + OHE de baja cardinalidad** | Compromiso | Decisión arbitraria |

Recomendación: **hacer PCA sobre todo**, documentando que las OHE pueden "contaminar" las componentes. Es lo más fiel a la consigna y permite que las dos primeras PCs sirvan como features sintéticos.

**Errores a evitar**:

- **PCA sin escalar**. El error clásico que `06-pca.md` y la cátedra repiten.
- **Reportar varianza explicada sin acumulada**. Decir "PC1 explica 12%" sin agregar "PC1+PC2 = 22%, PC1..PC10 = 60%" es contar la mitad de la historia.
- **Olvidar `random_state`**. PCA es determinístico en sklearn (no usa randomness salvo en `svd_solver='randomized'`), pero ponerlo es buena práctica.

**Qué escribir**:
> "Aplicamos PCA con `n_components=min(20, X.shape[1])=20` sobre la matriz imputada y estandarizada. Escalar antes es obligatorio porque PCA descompone covarianza y, sin escalado, la PC1 sería dominada por la feature con mayor varianza absoluta (en este dataset, Price). Decidimos hacer PCA sobre toda la matriz (numéricas + OHE), documentando que las OHE binarias tienen varianza acotada por p·(1−p) y pueden distorsionar las primeras componentes. Las primeras 2 componentes explican aproximadamente X% de la varianza; las primeras 20 acumulan aproximadamente Y%."

---

### 3.2 Agregar 2 primeras componentes como features

```python
# Primeras 2 columnas de X_pca son PC1 y PC2
X_final = numpy.hstack([X_imputed, X_pca[:, :2]])
all_feature_names_v3 = all_feature_names_v2 + ['PC1', 'PC2']
print(X_final.shape)  # (~13518, ~85)
```

**Atención conceptual**: estás agregando **features derivadas** del propio dataset. Esto puede generar colinealidad si después modelás con un algoritmo sensible (regresión lineal). Para árboles/ensembles no es problema. La cátedra no lo problematiza explícitamente, pero es un punto que vale comentar si querés sumar.

---

## Ejercicio 4 — Composición del resultado

### Qué pide la consigna (cita textual)

> "Transformar nuevamente el conjunto de datos procesado en un `pandas.DataFrame` y guardarlo en un archivo.
> Para eso, será necesario recordar el nombre original de cada columna de la matriz, en el orden correcto. Tener en cuenta:
> 1. El método `OneHotEncoder.get_feature_names` o el atributo `OneHotEncoder.categories_` permiten obtener una lista con los valores de la categoría que le corresponde a cada índice de la matriz.
> 2. Ninguno de los métodos aplicados intercambia de lugar las columnas o las filas de la matriz."

### Código

```python
# Reconstruimos el DataFrame con los nombres preservados
melb_final = pandas.DataFrame(
    X_final,
    columns=all_feature_names_v3,
    index=clean_df.index
)

# Validación: shapes consistentes
assert melb_final.shape == (clean_df.shape[0], len(all_feature_names_v3))
assert melb_final.isna().sum().sum() == 0  # No deben quedar NaN

# Guardar
melb_final.to_csv('melb_data_curated.csv', index=False)
print(f"Guardado: {melb_final.shape}, columnas: {melb_final.columns.tolist()[:10]}...")
```

**Errores a evitar**:

- **Nombres pisados**: en versiones nuevas de sklearn, `get_feature_names()` está deprecada. Usá `get_feature_names_out()`.
- **Orden de columnas alterado**: si concatenaste con un orden distinto al de los `feature_names`, las etiquetas no matchean los datos. Cuidá esto cada vez que hagas `numpy.hstack`.
- **No verificar que no quedan NaN**: si KNN no convergió y dejó algún valor sin imputar, te entregás con NaN sin saberlo.

**Qué escribir**:
> "Reconstruimos el DataFrame final preservando el orden exacto de las columnas a lo largo de todo el pipeline: numéricas en posiciones 0–10, OHE en 11–80 (en el orden de `get_feature_names_out`), YearBuilt/BuildingArea en 81–82, PC1/PC2 en 83–84. Validamos shape y ausencia de NaN antes de persistir."

---

## Ejercicio 5 — Documentación

### Qué pide la consigna

> "En un documento `.pdf` o `.md` realizar un reporte de las operaciones que realizaron para obtener el conjunto de datos final. Se debe incluir:
> 1. Criterios de exclusión (o inclusión) de filas o columnas
> 2. Interpretación de las columnas presentes
> 3. Todas las transformaciones realizadas."

### Estructura sugerida del PDF/MD

```markdown
# Reporte técnico — Curación de melb_data
Autor: ...
Fecha: ...
Fuente original: https://cs.famaf.unc.edu.ar/~mteruel/datasets/diplodatos/melb_data.csv
Shape original: 13.580 × 21
Shape final: 13.518 × 85

## 1. Criterios de exclusión de filas
1. Se eliminaron 62 filas con `Car` faltante (~0.46% del dataset). Asumimos MCAR.

## 2. Criterios de exclusión de columnas
1. `Address` — cardinalidad ≈ N, sin valor predictivo.
2. `Suburb` — alta cardinalidad (~310 únicos), correlacionada con Regionname/Postcode.
3. `SellerG` — alta cardinalidad (~270), posible data leakage del proceso de venta.

## 3. Tratamiento de faltantes
1. `Car` (0.46% faltantes): dropeo de filas (MCAR).
2. `CouncilArea` (~10% faltantes): categoría "Unknown" agregada.
3. `BuildingArea` (~47%) y `YearBuilt` (~40%): imputados con `IterativeImputer(KNeighborsRegressor)` sobre la matriz completa (numéricas + OHE) previamente estandarizada.

## 4. Características categóricas
1. `Type` (3 valores, h/u/t): OHE con drop_first=True.
2. `Method` (5 valores): OHE con drop_first=True.
3. `Regionname` (8 valores): OHE con drop_first=True.
4. `CouncilArea` (~34 incluyendo "Unknown"): OHE con drop_first=True.
5. `Postcode` (~200 valores): reducido a top 30 + "Otros", luego OHE.

## 5. Características numéricas
1. `Rooms`, `Price`, `Distance`, `Bedroom2`, `Bathroom`, `Car`, `Landsize`, `Lattitude`, `Longtitude`, `Propertycount`: estandarizadas con StandardScaler.
2. `Date` → `days_since_start` (numérica ordinal: días desde la fecha mínima).

## 6. Cambios de tipo
1. `Postcode`: de float64 a string (es identificador, no aritmético).
2. `Bedroom2`, `Bathroom`, `Car`, `Propertycount`: de float64 a int (son conteos).

## 7. Datos aumentados
1. PC1 y PC2 — primeras dos componentes principales del PCA aplicado sobre la matriz imputada+estandarizada. Acumulan aproximadamente X% de la varianza.

## 8. Reproducibilidad
- random_state = 42 en IterativeImputer y PCA.
- `StandardScaler` fit sobre train (no hay split por ser ejercicio único; en producción se ajusta solo en train).
```

**Errores a evitar**:

- Reporte que solo cuenta el "qué" y no el "por qué". La cátedra evalúa criterio.
- Reporte sin shapes (cuántas filas/columnas antes/después de cada paso).
- Reporte sin random_state. Sin eso no es reproducible.

---

## Decisiones clave del TP1 — resumen

| Decisión | Opciones | Qué justificar |
|----------|----------|----------------|
| Tratamiento de Date | descartar / ordinal-días / año+mes | Por qué elegiste esa; idealmente medir correlación Date-Price |
| Cardinalidad Suburb/SellerG | dropear / top-N+Otros / frecuencia | Trade-off entre dimensionalidad y pérdida de información |
| Estandarización antes de KNN | sí (obligatorio) | Distancias euclídeas dominadas por escala |
| Estandarización antes de PCA | sí (obligatorio) | PCA descompone covarianza, varianza absoluta domina |
| n_components en PCA | 20 (consigna) | Mencionar el posible typo X.shape[0] vs X.shape[1] |
| PCA sobre OHE o solo numéricas | todo / solo num / mix | Las OHE tienen varianza acotada, pueden distorsionar |

---

# TP2 — Entregable parte 2

## Los datasets

### Principal: `melb_data.csv`
Mismo del TP1. Acá la cátedra recomienda usar **el dataset original** (no el curado del TP1) porque el TP2 enfoca otros aspectos (SQL, outliers visuales, enriquecimiento) y conviene partir limpio.

### Secundario: `airbnb_price_by_zipcode.csv`

**Importante**: este archivo NO está disponible para descarga directa. **Lo generás vos** corriendo el notebook `02.1 Combinación de datasets.ipynb` (clase 4 del campus). Si no lo tenés, este es el código mínimo para reproducirlo:

```python
# Reproducción del archivo airbnb_price_by_zipcode.csv
# Requiere descargar cleansed_listings_dec18.csv de:
# https://www.kaggle.com/tylerx/melbourne-airbnb-open-data
import pandas

airbnb_df = pandas.read_csv('cleansed_listings_dec18.csv')

# Limpiar precios (vienen como string '$120.00' en algunos casos)
for col in ['price', 'weekly_price', 'monthly_price']:
    if airbnb_df[col].dtype == object:
        airbnb_df[col] = (airbnb_df[col]
                          .astype(str)
                          .str.replace('$', '', regex=False)
                          .str.replace(',', '', regex=False))
        airbnb_df[col] = pandas.to_numeric(airbnb_df[col], errors='coerce')

airbnb_df['zipcode'] = pandas.to_numeric(airbnb_df.zipcode, errors='coerce')

relevant = ['price', 'weekly_price', 'monthly_price', 'zipcode']
airbnb_by_zip = (airbnb_df[relevant]
    .dropna(subset=['zipcode'])
    .groupby('zipcode')
    .agg({'price': ['mean', 'median', 'count'],
          'weekly_price': 'mean',
          'monthly_price': 'mean'})
    .reset_index())
airbnb_by_zip.columns = ['_'.join(c).strip('_') for c in airbnb_by_zip.columns]

airbnb_by_zip.to_csv('airbnb_price_by_zipcode.csv', index=False)
```

---

## Ejercicio 1 — SQL

### Qué pide la consigna (cita textual, resumida por sub-puntos)

> "1. Crear una base de datos en SQLite utilizando la libreria SQLalchemy.
> 2. Ingestar los datos provistos en 'https://cs.famaf.unc.edu.ar/...melb_data.csv' en una tabla y el dataset generado en clase con datos de airbnb y sus precios por código postal en otra.
> 3. Validar tipos de columnas antes de guardar. Usá `df.dtypes` para ver los tipos actuales. Prestá especial atención a columnas como `Date` y `Price`...
> 4. Implementar consultas en SQL que respondan con la siguiente información:
>    - cantidad de registros totales por `Regionname`.
>    - cantidad de registros totales por `Suburb` y `Regionname`.
>    - ¿Cuántas propiedades hay por `Regionname` con más de 2 habitaciones?
>    - ¿Cuál es el precio promedio de propiedades según tipo (`Type`) y `Regionname`?
>    - Mostrá el top 5 barrios con propiedades más caras en promedio.
> 5. Combinar los datasets de ambas tablas ingestadas utilizando el comando JOIN de SQL...
> 6. Agregar una celda de validación posterior al JOIN con assertions o validación de esquema..."

### Archivos de estudio relevantes

- `10-sql-basico.md` — sintaxis SQL, SQLAlchemy.
- `08-combinacion-de-datasets.md` — merge vs JOIN, validaciones.

---

### 1.1 Crear DB SQLite con SQLAlchemy

```python
from sqlalchemy import create_engine, text
import pandas

# Engine en archivo (persistente). Alternativa ':memory:' para volátil.
engine = create_engine('sqlite:///melbourne.sqlite3', echo=False)
```

**Errores a evitar**:

- `echo=True` te llena la consola de logs SQL. Útil para debug, molesto en entrega.
- Usar `:memory:` y después no poder reabrir la base en otra sesión.

---

### 1.2 Ingestar tablas

```python
melb_df = pandas.read_csv(
    'https://cs.famaf.unc.edu.ar/~mteruel/datasets/diplodatos/melb_data.csv')
airbnb_zip = pandas.read_csv('airbnb_price_by_zipcode.csv')

melb_df.to_sql('properties', con=engine, if_exists='replace', index=False)
airbnb_zip.to_sql('airbnb_zip', con=engine, if_exists='replace', index=False)

# Verificación
with engine.connect() as con:
    n = con.execute(text("SELECT COUNT(*) FROM properties")).scalar()
    print(f"properties: {n} filas")
    n = con.execute(text("SELECT COUNT(*) FROM airbnb_zip")).scalar()
    print(f"airbnb_zip: {n} filas")
```

**Errores a evitar**:

- `if_exists='fail'` (default) rompe si la tabla ya existe. Para iteración usá `'replace'`.
- `index=True` te crea una columna "index" en SQL que no necesitás y rompe queries.

---

### 1.3 Validación de tipos

La consigna pide **explícitamente** chequear `Date` y `Price`.

```python
print("dtypes melb_df:")
print(melb_df.dtypes)

# Vas a ver:
# Date: object → SQLite la guarda como TEXT
# Price: float64 → REAL (correcto)
# Postcode: float64 (debería ser INTEGER para el JOIN)
```

**Correcciones**:

```python
# Convertir Date a datetime
melb_df['Date'] = pandas.to_datetime(melb_df['Date'], format='%d/%m/%Y')

# Postcode: convertir a int (asegurándose de no tener NaN)
print("Postcodes con NaN:", melb_df['Postcode'].isna().sum())  # debería ser 0
melb_df['Postcode'] = melb_df['Postcode'].astype(int)

# Lo mismo en el airbnb
airbnb_zip['zipcode'] = airbnb_zip['zipcode'].astype(int)

# Re-ingestar
melb_df.to_sql('properties', con=engine, if_exists='replace', index=False)
airbnb_zip.to_sql('airbnb_zip', con=engine, if_exists='replace', index=False)
```

**Qué escribir**:
> "SQLite infiere tipos automáticamente al hacer `to_sql`, pero los problemáticos eran: (a) `Date` que estaba como string (`object`) y guardamos como TEXT con formato ISO tras convertir a datetime; (b) `Postcode` como float (por arrastre de NaN en el CSV original) — convertimos a int para que el JOIN con `zipcode` (también int) funcione sin conversiones implícitas. Validamos con `df.dtypes` antes y después de ingestar."

---

### 1.4 Consultas SQL

#### Conteo por Regionname

```python
q1 = """
SELECT Regionname, COUNT(*) AS cantidad
FROM properties
GROUP BY Regionname
ORDER BY cantidad DESC;
"""
result_q1 = pandas.read_sql(q1, con=engine)
result_q1
```

#### Conteo por Suburb y Regionname

```python
q2 = """
SELECT Suburb, Regionname, COUNT(*) AS cantidad
FROM properties
GROUP BY Suburb, Regionname
ORDER BY cantidad DESC
LIMIT 20;
"""
result_q2 = pandas.read_sql(q2, con=engine)
```

#### Propiedades por Regionname con más de 2 habitaciones

```python
q3 = """
SELECT Regionname, COUNT(*) AS cantidad
FROM properties
WHERE Rooms > 2
GROUP BY Regionname
ORDER BY cantidad DESC;
"""
result_q3 = pandas.read_sql(q3, con=engine)
```

#### Precio promedio por Type y Regionname

```python
q4 = """
SELECT Type, Regionname,
       AVG(Price) AS precio_promedio,
       COUNT(*) AS cantidad
FROM properties
GROUP BY Type, Regionname
ORDER BY precio_promedio DESC;
"""
result_q4 = pandas.read_sql(q4, con=engine)
```

#### Top 5 barrios más caros en promedio

```python
q5 = """
SELECT Suburb,
       AVG(Price) AS precio_promedio,
       COUNT(*) AS cantidad
FROM properties
GROUP BY Suburb
HAVING COUNT(*) >= 5
ORDER BY precio_promedio DESC
LIMIT 5;
"""
result_q5 = pandas.read_sql(q5, con=engine)
```

**Nota importante**: agregar el `HAVING COUNT(*) >= 5` evita que el top esté contaminado por suburbios con 1 sola propiedad de precio extremo. La consigna no lo pide explícitamente, pero **es lo correcto estadísticamente** y vale comentarlo. La cátedra premia ese tipo de criterio.

**Errores a evitar**:

- Top 5 sin filtro de cantidad mínima: te aparecen suburbios con 1-2 propiedades millonarias, no información útil.
- Olvidar `ORDER BY` en queries de ranking. Sin orden, "top 5" no tiene sentido.
- Mezclar `HAVING` con `WHERE`: `WHERE` filtra antes del groupby, `HAVING` filtra agregaciones después.

---

### 1.5 JOIN equivalente al merge

```python
q_join = """
SELECT p.*,
       a.price_mean   AS airbnb_price_mean,
       a.price_median AS airbnb_price_median,
       a.price_count  AS airbnb_count
FROM properties p
LEFT JOIN airbnb_zip a
    ON p.Postcode = a.zipcode;
"""
merged_sql = pandas.read_sql(q_join, con=engine)
print(merged_sql.shape)
```

**Equivalente Pandas (para comparar)**:

```python
merged_pd = melb_df.merge(airbnb_zip, how='left',
                          left_on='Postcode', right_on='zipcode')
```

**Errores a evitar**:

- `INNER JOIN` en lugar de `LEFT JOIN`: te pierde filas de `properties` cuyo Postcode no aparece en `airbnb_zip`. Usás LEFT porque querés conservar todas las propiedades aunque no tengan match.
- **`merge` ingenuo sin agregar AirBnB primero**: como advierte la Clase 4, hacer `merge` con un airbnb sin agregar por zipcode te genera 2 millones de filas (producto cartesiano por zipcode). Nosotros usamos `airbnb_by_zipcode` que ya está agregado, así que estamos a salvo.

---

### 1.6 Validaciones post-JOIN (assertions)

La consigna pide explícitamente:
> "verificá que el número de filas no cambió, que no aparecieron nulos inesperados y que los rangos de variables agregadas sean razonables."

Estas son las **assertions exactas** que conviene escribir:

```python
# 1. La cantidad de filas no cambió (LEFT JOIN sobre tabla izquierda)
assert len(merged_sql) == len(melb_df), \
    f"El JOIN cambió filas: {len(merged_sql)} vs {len(melb_df)}"

# 2. Las columnas originales de melb_df no perdieron datos
assert merged_sql['Price'].isna().sum() == melb_df['Price'].isna().sum(), \
    "Price perdió valores no-nulos en el JOIN"

# 3. Las columnas agregadas tienen tasa de match razonable
match_rate = merged_sql['airbnb_price_mean'].notna().mean()
print(f"Tasa de match con AirBnB: {match_rate:.2%}")
assert match_rate > 0.5, \
    f"Tasa de match baja: {match_rate:.2%} — revisar tipos de Postcode/zipcode"

# 4. Los precios de AirBnB están en rango razonable (USD/AUD por noche)
prices = merged_sql['airbnb_price_mean'].dropna()
assert prices.between(10, 5000).all(), \
    f"Precios AirBnB fuera de rango razonable: min={prices.min()}, max={prices.max()}"

# 5. No se duplicaron filas (la PK lógica sigue siendo Address+Date)
duplicates = merged_sql.duplicated(subset=['Address', 'Date']).sum()
assert duplicates == 0, f"Aparecieron {duplicates} duplicados tras JOIN"
```

**Por qué cada assertion**:

1. **Filas no cambiaron**: si el JOIN explotó por una clave duplicada en la tabla derecha, el shape crece. Como `airbnb_zip` está agregado por zipcode (clave única), no debería pasar. Pero verificarlo es básico.
2. **Nulos no aparecieron donde no había**: protege contra que el JOIN haya roto valores no nulos por algún cast.
3. **Tasa de match**: si tu Postcode era float y zipcode era int (o viceversa), el JOIN matchea 0%. Una tasa muy baja es señal de incompatibilidad de tipos.
4. **Rangos razonables**: precio de AirBnB en \$10–\$5000 por noche es razonable. Si encontrás \$0 o \$1.000.000 es un dato corrupto.
5. **No duplicación**: defensiva.

**Qué escribir**:
> "Implementamos cinco assertions post-JOIN que verifican: (a) preservación del shape (no explotó por claves duplicadas), (b) preservación de no-nulos en columnas originales, (c) tasa de match con AirBnB (>50% indica compatibilidad de tipos), (d) rango razonable de precios AirBnB (10–5000 USD/noche), (e) ausencia de duplicación. Esto implementa las dimensiones básicas de calidad de datos: integridad (claves), completitud (nulos), validez (rangos)."

---

## Ejercicio 2 — Pandas

### Qué pide la consigna (cita textual resumida)

> "1. Seleccionar un subconjunto de columnas que les parezcan relevantes... Justificar explícitamente las columnas seleccionadas y las que no.
>    1. ¿Qué porcentaje de filas tienen al menos un valor faltante?
>    2. Mostrar la dispersión o distribución de las columnas seleccionadas.
>    3. Eliminar los valores extremos que no sean relevantes...
>    4. Mostrar visualmente los valores extremos que eliminás.
> 2. Agregar información adicional respectiva al entorno de una propiedad a partir del conjunto de datos de AirBnB..."

### Archivos de estudio relevantes

- `07-exploracion-eda.md` — outliers, IQR, distribuciones.
- `08-combinacion-de-datasets.md` — merge, validaciones, agregación previa.

---

### 2.1 Subset de columnas + faltantes + outliers + visualización

#### Selección y justificación

```python
# Columnas que conservamos y por qué
relevant_cols = ['Rooms', 'Price', 'Type', 'Method', 'Distance',
                 'Postcode', 'Bedroom2', 'Bathroom', 'Car',
                 'Landsize', 'BuildingArea', 'YearBuilt',
                 'CouncilArea', 'Lattitude', 'Longtitude',
                 'Regionname', 'Propertycount', 'Date']
melb = melb_df[relevant_cols].copy()

# Columnas que descartamos:
# - Address: cardinalidad ~ N, sin valor predictivo
# - SellerG: alta cardinalidad, posible leakage
# - Suburb: muy correlacionado con Postcode + Regionname (redundante)
```

#### Porcentaje de filas con al menos un faltante

```python
pct_rows_with_na = (melb.isna().any(axis=1).sum() / len(melb)) * 100
print(f"% de filas con al menos un NaN: {pct_rows_with_na:.1f}%")
# Esperado: ~50% (por BuildingArea y YearBuilt)

# Por columna
melb.isna().sum().sort_values(ascending=False).head(10)
```

#### Distribución

```python
fig, axes = plt.subplots(3, 3, figsize=(15, 12))
numericas = ['Price', 'Rooms', 'Distance', 'Landsize', 'BuildingArea',
             'YearBuilt', 'Bathroom', 'Car', 'Propertycount']
for ax, col in zip(axes.flat, numericas):
    seaborn.histplot(melb[col].dropna(), ax=ax, kde=True)
    ax.set_title(col)
plt.tight_layout()
```

Y para categóricas:

```python
for col in ['Type', 'Method', 'Regionname']:
    print(melb[col].value_counts())
    print()
```

#### Outliers con IQR

> **CRÍTICO**: la consigna pide *"eliminar los valores extremos"* y *"mostrar visualmente los valores extremos que eliminás"*. Usá **IQR**, **no a ojo**. El apunte `07-exploracion-eda.md` lo deja claro.

```python
def iqr_bounds(s, k=1.5):
    """Devuelve los límites IQR de una serie."""
    q1, q3 = s.quantile([0.25, 0.75])
    iqr = q3 - q1
    return q1 - k*iqr, q3 + k*iqr

# Aplicar a las columnas con outliers claros
target_outliers = ['Price', 'Landsize', 'BuildingArea']
masks = {}
for col in target_outliers:
    low, high = iqr_bounds(melb[col].dropna())
    masks[col] = (melb[col] < low) | (melb[col] > high)
    n_out = masks[col].sum()
    print(f"{col}: {n_out} outliers ({n_out/len(melb)*100:.2f}%) — fuera de [{low:.0f}, {high:.0f}]")

# Eliminar outliers (combinación: cualquier columna fuera del IQR)
mask_outliers = pandas.concat(masks.values(), axis=1).any(axis=1)
melb_clean = melb[~mask_outliers].copy()
print(f"Antes: {len(melb)}, Después: {len(melb_clean)}, Eliminados: {mask_outliers.sum()}")
```

#### Visualizar los outliers eliminados

```python
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
for ax, col in zip(axes, target_outliers):
    seaborn.scatterplot(data=melb, x=melb.index, y=col, ax=ax, alpha=0.3, label='Conservados')
    seaborn.scatterplot(data=melb[masks[col]], x=melb[masks[col]].index, y=col,
                        ax=ax, color='red', alpha=0.7, label='Outliers')
    ax.set_title(f'{col}: outliers IQR (k=1.5)')
plt.tight_layout()
```

Alternativa más sintética: boxplot.

```python
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
for ax, col in zip(axes, target_outliers):
    seaborn.boxplot(y=melb[col], ax=ax)
    ax.set_title(col)
```

**Errores a evitar**:

- **Eliminar outliers "a ojo"** sin método. La cátedra detecta seguro la falta de criterio cuantitativo.
- **Usar z-score** en distribuciones no-normales (Price, Landsize tienen colas pesadas). El apunte `07-exploracion-eda.md` lo dice: usar IQR, no z-score.
- **Eliminar TODOS los outliers de TODAS las columnas**: si combinás todas con OR, podés perder >20% del dataset. Sé selectivo: enfocate en las columnas que más influyen en el precio.
- **No documentar cuántos eliminás**: el shape antes/después es información obligatoria.

**Qué escribir**:
> "Detectamos y eliminamos outliers usando IQR (k=1.5) sobre Price, Landsize y BuildingArea. Total eliminado: X filas (~Y%). Visualizamos los outliers con un scatter coloreado para verificar que el método no descarta observaciones genuinas (un terreno de 5000 m² no necesariamente es error, pero es outlier matemático). Decidimos eliminar los outliers conjuntos (OR) porque para predecir precio queremos conservar el rango típico del mercado."

---

### 2.2 Enriquecimiento con AirBnB

#### Qué variables y por qué mediana vs media

```python
# Cargar AirBnB agregado
airbnb_zip = pandas.read_csv('airbnb_price_by_zipcode.csv')
print(airbnb_zip.head())
```

Las columnas relevantes son `price_mean`, `price_median`, `price_count`.

**¿Por qué la consigna pregunta "¿por qué no la media?"?**

Porque la **media** es sensible a outliers de AirBnB (publicaciones con precios extremos: mansiones, errores de carga con precios de 10.000 USD/noche). La **mediana** es robusta: si en un zipcode hay 50 publicaciones a 100 USD/noche y una a 10.000 USD/noche, la mediana sigue siendo ~100 USD/noche, la media es ~300 USD/noche.

Para enriquecer un dataset de precios de propiedades, la mediana representa mejor "el precio típico del entorno", que es lo que captura "valor del vecindario".

> "Usamos la mediana en lugar de la media porque AirBnB tiene una cola derecha pesada (mansiones de lujo, errores de carga) que distorsionan la media. La mediana es robusta a esos outliers y representa mejor el valor típico del entorno, que es lo que queremos capturar como feature de zona."

#### Mínimo de registros por zipcode

```python
MIN_RECORDS = 5  # Justificable: con menos de 5 publicaciones, la mediana es ruidosa

airbnb_filtered = airbnb_zip[airbnb_zip['price_count'] >= MIN_RECORDS].copy()
print(f"Zipcodes con >= {MIN_RECORDS} publicaciones: {len(airbnb_filtered)} de {len(airbnb_zip)}")
```

**Por qué un mínimo**: si un zipcode tiene 1 sola publicación, su "mediana" es solo ese valor. No representa nada estadísticamente.

#### El merge

```python
melb_enriched = melb_clean.merge(
    airbnb_filtered,
    how='left',
    left_on='Postcode',
    right_on='zipcode'
)
print(f"Filas antes: {len(melb_clean)}, después: {len(melb_enriched)}")
# Tiene que ser igual: LEFT JOIN sobre tabla izquierda

# Match rate
match_rate = melb_enriched['price_median'].notna().mean()
print(f"Match rate: {match_rate:.2%}")
```

#### Gráfico zipcode vs airbnb_price_median

```python
fig, ax = plt.subplots(figsize=(14, 5))
airbnb_sorted = airbnb_filtered.sort_values('price_median')
ax.bar(airbnb_sorted['zipcode'].astype(str), airbnb_sorted['price_median'])
ax.set_xlabel('Zipcode')
ax.set_ylabel('Mediana de precio AirBnB (USD/noche)')
ax.set_title('Precio mediano de AirBnB por zipcode (Melbourne)')
plt.xticks(rotation=90, fontsize=7)
plt.tight_layout()
```

#### Alternativas de join + preguntas al experto

La consigna pide *"Investigar al menos otras 2 variables que puedan servir para combinar los datos"*.

Dos alternativas:

1. **CouncilArea (Melbourne) ↔ neighbourhood_cleansed (AirBnB)**: ambos describen un agrupamiento geográfico-administrativo. Problema: los nombres no están normalizados (Yarra ≠ City of Yarra; mayúsculas, espacios). Requiere un mapeo manual o asistido por LLM (Ejercicio 4 bonus).

2. **Coordenadas geográficas (Lattitude, Longtitude ↔ latitude, longitude)**: ambos datasets tienen lat/long. Permite hacer un *spatial join* o usar k-NN espacial para asignar a cada propiedad las N publicaciones AirBnB más cercanas. Es lo más preciso pero requiere librerías geo (geopandas, sklearn BallTree).

**Las 3 preguntas al experto inmobiliario** (la consigna explícita lo pide):

1. ¿Cómo definen los límites entre suburbios oficiales y barrios percibidos en Melbourne? Por ejemplo, ¿"South Yarra" en AirBnB corresponde 1:1 con "Yarra" en CouncilArea, o son áreas distintas?
2. Cuando hay solapamiento entre Postcode y CouncilArea (un Postcode puede caer en múltiples councils), ¿cuál es la convención para asignar una propiedad? ¿El Postcode mayoritario o el de la dirección física?
3. ¿Existen diferencias relevantes de valor de propiedad **dentro** de un mismo Postcode (por ejemplo, una calle premium vs el resto del código postal)? Si sí, ¿el mapeo zipcode-only es suficiente o necesitamos algo más granular?

#### Coordenadas geoespaciales — cómo usarlas

> "Si tuviéramos las coordenadas, podríamos: (a) hacer un *k-NN espacial* donde para cada propiedad encontramos las N publicaciones AirBnB más cercanas (típicamente 5–20) y agregamos sus precios (mediana). Esto reemplaza al merge por Postcode con una vecindad geográfica real, eliminando el problema de zipcodes muy grandes o muy chicos. (b) Construir features geográficas: distancia al CBD ya existe, pero también podríamos calcular densidad de publicaciones AirBnB en un radio de N km, distancia al transporte público, etc. (c) Visualizar con folium/plotly el dataset enriquecido en un mapa interactivo."

#### Qué no está en los datos que sería útil

La consigna pregunta esto explícitamente. Sumá una breve lista:

- Estado de la propiedad (a renovar, reformada, nueva).
- Calidad de las terminaciones.
- Orientación, vista, exposición al sol.
- Cercanía a transporte público, escuelas, hospitales.
- Antigüedad del último impuesto inmobiliario (proxy de gentrificación).
- Crimen / seguridad por zona.

---

## Ejercicio 3 — Persistencia

```python
melb_enriched.to_csv('melb_data_enriched.csv', index=False)
print(f"Guardado: {melb_enriched.shape}")

# Validación post-guardado
melb_test = pandas.read_csv('melb_data_enriched.csv')
assert melb_test.shape == melb_enriched.shape, "El archivo guardado difiere"
print("Persistencia OK")
```

**Errores a evitar**:

- `to_csv` sin `index=False`: te agrega una columna "Unnamed: 0" al releer.
- No verificar post-guardado: si el archivo se truncó, te lo entregás roto.

---

## Ejercicio 4 — Opcionales

Estos son los opcionales. Si tenés tiempo, **el #1 (ETL .py) suma mucho** porque demuestra que entendés el ciclo completo. El #2 (DAG Airflow) es bastante; el #3 (embeddings) es divertido pero ortogonal al resto del TP; el #4 (curación con LLM) es práctico pero requiere API key.

### 4.1 Script ETL en .py

Estructura mínima:

```python
# etl_melb.py
import logging
import pandas
from sqlalchemy import create_engine

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

URL_MELB = 'https://cs.famaf.unc.edu.ar/~mteruel/datasets/diplodatos/melb_data.csv'
URL_AIRBNB = 'airbnb_price_by_zipcode.csv'
DB_URL = 'sqlite:///melbourne.sqlite3'

def extract():
    logging.info("Extracción...")
    melb = pandas.read_csv(URL_MELB)
    airbnb = pandas.read_csv(URL_AIRBNB)
    return melb, airbnb

def transform(melb, airbnb):
    logging.info("Transformación...")
    melb['Date'] = pandas.to_datetime(melb['Date'], format='%d/%m/%Y')
    melb['Postcode'] = melb['Postcode'].astype(int)
    airbnb['zipcode'] = airbnb['zipcode'].astype(int)
    # IQR outlier removal sobre Price
    q1, q3 = melb['Price'].quantile([0.25, 0.75])
    iqr = q3 - q1
    melb = melb[(melb['Price'] >= q1 - 1.5*iqr) & (melb['Price'] <= q3 + 1.5*iqr)]
    merged = melb.merge(airbnb, how='left', left_on='Postcode', right_on='zipcode')
    assert len(merged) == len(melb), "El merge cambió filas"
    return merged

def load(df):
    logging.info("Carga...")
    engine = create_engine(DB_URL)
    df.to_sql('properties_enriched', con=engine, if_exists='replace', index=False)
    df.to_csv('melb_data_enriched.csv', index=False)

def main():
    melb, airbnb = extract()
    merged = transform(melb, airbnb)
    load(merged)
    logging.info(f"ETL completado: {merged.shape}")

if __name__ == "__main__":
    main()
```

**Errores a evitar**:

- Usar `print` en lugar de `logging`. La cátedra lo marca como buena práctica en Clase 4 (*"logging con niveles, NO print"*).
- Credenciales hardcoded. Si tu DB fuera Postgres con password, usás `python-decouple` + `.env`.
- Sin assertions en transform.

### 4.2 DAG Airflow

Estructura mínima (no hace falta correrlo, solo presentarlo):

```python
# dags/melb_dag.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from etl_melb import extract, transform, load

def task_extract(**ctx):
    melb, airbnb = extract()
    ctx['ti'].xcom_push(key='melb', value=melb.to_json())
    ctx['ti'].xcom_push(key='airbnb', value=airbnb.to_json())

def task_transform(**ctx): ...
def task_load(**ctx): ...

with DAG('melb_etl', start_date=datetime(2026, 1, 1),
         schedule_interval='@weekly', catchup=False) as dag:
    t1 = PythonOperator(task_id='extract', python_callable=task_extract)
    t2 = PythonOperator(task_id='transform', python_callable=task_transform)
    t3 = PythonOperator(task_id='load', python_callable=task_load)
    t1 >> t2 >> t3
```

### 4.3 Embeddings con sentence-transformers

La consigna pide:
> "Tomar un subconjunto chico de descripciones, calcular embeddings y encontrar el par más similar con similitud coseno."

```python
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy

# Asumiendo que tenés el airbnb_df completo con la columna 'description'
sample = airbnb_df.sample(50, random_state=42).reset_index(drop=True)
descriptions = sample['description'].fillna('').tolist()

model = SentenceTransformer('all-MiniLM-L6-v2')  # 384 dims
embeddings = model.encode(descriptions, show_progress_bar=True)

sim_matrix = cosine_similarity(embeddings)
numpy.fill_diagonal(sim_matrix, -1)  # ignorar la diagonal (similitud consigo mismo)

i, j = numpy.unravel_index(sim_matrix.argmax(), sim_matrix.shape)
print(f"Par más similar (sim={sim_matrix[i, j]:.3f}):")
print(f"A: {descriptions[i][:200]}...")
print(f"B: {descriptions[j][:200]}...")
```

**Reflexiones que pide la consigna**:

- ¿Por qué no se puede con `LIKE '%keyword%'`? Porque LIKE busca coincidencia textual exacta. "cozy apartment near beach" y "comfortable flat by the coast" tienen 0 palabras en común pero significan lo mismo. Los embeddings capturan semántica.
- ¿Qué representan los 384 números? Coordenadas en un espacio vectorial aprendido donde la distancia coseno aproxima similitud semántica. Cada dimensión no tiene interpretación humana; emerge del entrenamiento.

### 4.4 Curación con Claude sobre CouncilArea

La consigna trae un ejemplo de código (lo dejo abajo simplificado):

```python
import anthropic, json

client = anthropic.Anthropic()
council_values = melb_df['CouncilArea'].dropna().unique().tolist()

message = client.messages.create(
    model="claude-opus-4-7",  # ajustar al modelo disponible
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": f"""Estos son los valores únicos de la columna CouncilArea en un dataset de Melbourne:
{council_values}

Identificá: (1) duplicados con distinta capitalización o spelling,
(2) valores que parecen errores, (3) valores que podrían agruparse.
Respondé en JSON: {{"estandarizado": {{"valor_original": "valor_correcto"}}}}"""
    }]
)
mapping = json.loads(message.content[0].text)
melb_df['CouncilArea_clean'] = melb_df['CouncilArea'].map(
    mapping.get('estandarizado', {})
).fillna(melb_df['CouncilArea'])
```

**Reflexiones que pide la consigna**:

- **¿Cuándo confiarías sin revisar?** Nunca con datos críticos. La validación manual es obligatoria en datos que van a producción o a un modelo de decisión.
- **¿Qué pasa si el modelo inventa un mapeo incorrecto?** Hallucination. El LLM puede "estandarizar" Bayside a "City of Bayside" cuando en realidad son cosas distintas en la ontología municipal australiana. Por eso necesitás ground truth.
- **¿Cómo validás con miles de valores únicos?** Sampling estratificado (un % aleatorio para revisión manual), validación contra una fuente externa autorizada (ej. catálogo oficial de councils), o usar el LLM solo para *sugerir* y mantener al humano en el loop para *decidir*.

---

# Errores típicos transversales

Esta es la lista que la cátedra detecta en el 80% de las entregas mediocres. Si en tu TP no aparece NINGUNO de estos, ya estás arriba del promedio.

| Error | Dónde aparece | Qué pierde |
|-------|---------------|------------|
| **No usar `.copy()`** al filtrar/asignar | Cualquier sub-ejercicio | SettingWithCopyWarning, modificación accidental del original |
| **No validar tipos antes de `to_sql`** | TP2 Ej1 | JOIN que matchea 0% por Postcode float vs zipcode int |
| **OHE sobre columnas con NaN** | TP1 Ej1.4 | Columna `_nan` espuria, código que no generaliza |
| **OHE sobre Suburb/Address** sin reducir cardinalidad | TP1 Ej1.4 | Matriz de 13.000+ columnas, memoria explota |
| **PCA o KNN sin escalar** | TP1 Ej2.2, Ej3.1 | Resultados dominados por la variable de escala más grande |
| **Eliminar outliers a ojo** sin IQR/percentil | TP2 Ej2.1 | Decisión arbitraria, no defendible |
| **No validar post-merge** (assertions de filas, nulos, rangos) | TP2 Ej1.6, Ej2 | Datos corrompidos pasan sin alerta |
| **`merge` ingenuo de AirBnB sin agregar antes** | TP2 Ej2 | Producto cartesiano: 2M de filas |
| **Justificar decisiones "a ojo"** en vez de con métrica | Todo el TP | Pérdida directa de puntos por criterio |
| **Reportar varianza explicada de PCA solo de PC1** | TP1 Ej3.1 | Falta contexto: cuánto se captura con 2, 5, 10 componentes |
| **No guardar `feature_names` tras OHE** | TP1 Ej4 | DataFrame final con columnas anónimas |
| **Mediana vs media sin justificar** | TP2 Ej2.2 | La consigna pregunta explícitamente |
| **Top N sin filtro de cantidad mínima** | TP2 Ej1.4 | Top 5 contaminado por suburbios con 1 registro |
| **Olvidar `random_state`** en métodos estocásticos | TP1 Ej2, Ej3 | Resultados no reproducibles |
| **`print` en lugar de `logging`** | TP2 Ej4.1 | Buena práctica de ETL ausente |

---

# Cómo se evalúa (según el notebook del TP2)

Cita textual del notebook:

> "**Criterios de evaluación**
> Se evaluará principalmente:
> - claridad del código,
> - justificación de las decisiones de curación,
> - coherencia entre el análisis realizado y las conclusiones,
> - presencia de validaciones después de operaciones críticas como merges o cargas a base.
>
> No se espera una única solución correcta, pero sí que las decisiones estén justificadas y sean consistentes con los datos."

Lo que esto significa en la práctica:

| Criterio | Cómo se gana | Cómo se pierde |
|----------|--------------|----------------|
| **Claridad de código** | Funciones reutilizables, variables con nombre semántico, comentarios donde haga falta | Pegote lineal de celdas, copy-paste, variables `df`, `df2`, `df3` |
| **Justificación de curación** | Cada decisión tiene una celda markdown que explica el por qué con métrica concreta | Decisiones "a ojo" sin justificación; o justificación genérica tipo "porque me pareció" |
| **Coherencia análisis-conclusiones** | Las conclusiones se siguen de los números mostrados | Conclusiones que no se apoyan en lo mostrado o que contradicen los datos |
| **Validaciones post-operación** | Assertions explícitas después de merges, ingestas, imputaciones | Operaciones sin validación; si rompe, te enterás en el corregido |

> **La materia tiene un sesgo claro hacia el criterio sobre la habilidad técnica**. Un alumno que entrega código simple y bien justificado va a sacar más que uno que entrega código sofisticado mal justificado.

---

# Checklist final pre-entrega

Antes de subir, pasá por esta lista. Si hay un check sin marcar, todavía tenés laburo.

## Estructura general
- [ ] El notebook corre **de arriba a abajo sin errores** en una sesión limpia (Kernel → Restart & Run All).
- [ ] No quedan celdas con `print` debug, ni variables huérfanas, ni comentarios `# TODO`.
- [ ] Las versiones de paquetes están al menos listadas en una celda inicial (pandas, sklearn, sqlalchemy).
- [ ] El nombre del archivo entregado coincide con el formato pedido (`Entregable_parte_1_<grupo>.ipynb`).

## TP1 — Encoding
- [ ] Excluiste `BuildingArea` y `YearBuilt` en el subset inicial (1.1).
- [ ] Documentaste cuántas filas y columnas se eliminaron y por qué (1.2).
- [ ] Comentaste que `Postcode` (y similares) tenían dtype incorrecto y lo corregiste (1.3).
- [ ] Tu decisión sobre `Date` está **explícita** y justificada (1.4).
- [ ] No hiciste OHE sobre Address/Suburb/SellerG sin reducir cardinalidad (1.4).
- [ ] Guardaste `feature_names` ordenados para el Ej 4.

## TP1 — Imputación + PCA
- [ ] Respondiste **explícitamente** "sí, hay que escalar" antes de KNN, con razón técnica (2.2).
- [ ] El gráfico antes/después muestra al menos 2 métodos comparados (2.3).
- [ ] Mencionaste el posible typo `X.shape[0]` vs `X.shape[1]` en PCA (3.1).
- [ ] Respondiste "sí, hay que escalar" antes de PCA (3.1).
- [ ] Reportaste varianza explicada acumulada, no solo PC1 (3.1).

## TP1 — Composición + documentación
- [ ] El DataFrame final tiene **nombres de columna**, no anónimos (4).
- [ ] No quedan NaN después de la imputación (assert) (4).
- [ ] El reporte técnico (.pdf/.md) cubre: filas eliminadas, columnas eliminadas, transformaciones, imputación, PCA, random_states (5).

## TP2 — SQL
- [ ] Convertiste `Date` a datetime y `Postcode`/`zipcode` a int antes de `to_sql` (1.3).
- [ ] Las 5 queries del 1.4 corren y retornan resultados sensatos.
- [ ] El "top 5 suburbios" tiene un `HAVING COUNT(*) >= N` para evitar contaminación.
- [ ] El JOIN es **LEFT** (no INNER) sobre `properties` (1.5).
- [ ] Tenés **5 assertions explícitas** post-JOIN (filas, nulos, match rate, rangos, duplicados) (1.6).

## TP2 — Pandas
- [ ] El subset de columnas está justificado (2.1).
- [ ] Reportaste el % de filas con al menos un NaN (2.1.1).
- [ ] Usaste IQR (no z-score, no a ojo) para outliers (2.1.3).
- [ ] Visualizaste outliers eliminados con color/marcador (2.1.4).
- [ ] Justificaste mediana vs media en la agregación AirBnB (2.2.1).
- [ ] Fijaste un mínimo de registros por zipcode con razón (2.2.2).
- [ ] Mostraste el gráfico zipcode vs precio mediano (2.2.3).
- [ ] Escribiste las 3 preguntas para el experto inmobiliario (2.2.4).
- [ ] Describiste cómo usarías coordenadas si las tuvieras (2.2.5).

## TP2 — Persistencia + opcionales
- [ ] Guardaste el CSV final sin index extra (`index=False`) (3).
- [ ] Validaste el archivo guardado releyéndolo (3).
- [ ] Si hiciste opcionales: el ETL usa `logging`, no `print`; el DAG es legible (4).

## General — justificación
- [ ] Cada decisión "no trivial" tiene una celda markdown que la justifica con métrica.
- [ ] No hay decisiones del tipo "porque sí" o "me pareció lo más simple" sin más contexto.
- [ ] Las conclusiones del análisis se siguen de lo que mostraste.

---

# Cierre

Lo que pasa con esta materia es que **es muy difícil sacar 10 con código brillante mal justificado, pero es fácil sacar 9 con código simple bien justificado**. La cátedra te dice esto explícitamente cuando escribe en el notebook *"No se espera una única solución correcta, pero sí que las decisiones estén justificadas y sean consistentes con los datos"*.

Si en tu próxima entrega:

- Cada decisión importante tiene una métrica detrás (un porcentaje, un IQR, una varianza explicada).
- Cada operación crítica (merge, imputación, ingesta) tiene una assertion después.
- Cada elección "abierta" (Date, cardinalidad, mediana vs media) tiene una celda markdown con tu razonamiento.

Entonces tenés el TP entregable. El resto es ajustar.

Y un consejo final: **no copies un EDA "estándar" sin pensarlo**. La cátedra ya leyó 200 notebooks donde alguien aplica `df.describe()` + `df.isnull().sum()` + un histograma de cada columna como si fuera un ritual. Eso no demuestra criterio. Demostrá criterio mirando el dataset y diciendo "esto me llama la atención porque X, voy a investigar Y". Eso es lo que diferencia un análisis curado de un script.
