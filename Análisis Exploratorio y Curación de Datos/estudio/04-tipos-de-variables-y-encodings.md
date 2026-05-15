# 04 — Tipos de variables y encodings

## Concepto

Los algoritmos de Machine Learning (excepto unos pocos basados en árboles puros) **requieren exclusivamente datos numéricos**. Si tu dataset tiene una columna con valores `"Casa"`, `"Departamento"`, `"Townhouse"`, ningún modelo de scikit-learn va a multiplicar matrices con strings. Tenés que **codificar** (en inglés *encoding*): convertir categorías en números, eligiendo una técnica que no le mienta al modelo.

La elección del encoding no es un trámite técnico. Si te equivocás, le estás contando una historia falsa a tu modelo: "estas tres ciudades están ordenadas, y la distancia entre la primera y la segunda es la misma que entre la segunda y la tercera" cuando en realidad son tres ciudades nominales sin orden.

## Intuición

Encoding es traducir de un idioma a otro. Estás pasando del idioma "texto" al idioma "números". El problema es que algunas traducciones pierden información y otras inventan información que no estaba.

- Traducir "lunes < martes < miércoles" a `1 < 2 < 3` mantiene el orden. Funciona.
- Traducir "Casa, Departamento, Townhouse" a `1, 2, 3` **inventa un orden que no existe**. El modelo va a creer que "Townhouse" es el doble de "Casa" y eso es absurdo.
- Traducir "Casa, Departamento, Townhouse" a tres columnas binarias (una por categoría) **conserva la diferencia sin inventar orden**, pero infla la dimensionalidad.

La regla mental es: ¿la columna original tenía orden? Sí → ordinal. No → one-hot u otra técnica para nominales.

---

## Taxonomía de variables

Repaso rápido (lo vimos en `01-eda-y-tipos-de-datos.md`), porque sin esto no podés elegir encoding:

### Categóricas

- **Ordinales**: hay un orden jerárquico natural. Ejemplos: nivel educativo (`Preschool < 1st-4th < ... < Doctorate`), seniority (`Junior < Semi-Senior < Senior`), satisfacción (`Malo < Regular < Bueno < Excelente`).
- **Nominales**: no hay orden. Ejemplos: sexo, color, país, tipo de propiedad (`Casa`, `Departamento`, `Townhouse`), suburbio.

### Numéricas

- **Discretas**: enteros. Edad en años, cantidad de cuartos, año de construcción.
- **Continuas**: reales. Precio, área en m², distancia al CBD (en inglés *Central Business District*, el centro comercial de la ciudad).

La trampa de siempre: **el tipo computacional (`object`, `int64`, `float64` en pandas) no te dice el tipo estadístico**. Una columna `object` puede ser nominal u ordinal; una columna `int64` puede ser ordinal codificada o numérica de verdad. Mirá los valores únicos y pensá si tienen orden.

---

## Por qué hay que codificar

Repetimos la frase de la cátedra porque es la justificación de todo el capítulo:

> *"Los algoritmos de aprendizaje automático requieren exclusivamente datos numéricos."*

Detrás de scikit-learn hay álgebra lineal: multiplicaciones de matrices, distancias euclídeas, gradientes. Nada de eso se puede hacer con strings. Incluso modelos que "aceptan categóricas" (como CatBoost o LightGBM) hacen el encoding internamente — lo hacen ellos, pero lo hacen.

Tu trabajo es **elegir el encoding correcto según el tipo de variable y el modelo que viene después**. KNN, K-means y SVM dependen de distancias, así que les importa muchísimo el encoding. Árboles de decisión son menos sensibles, pero igual conviene hacerlo bien.

---

## Técnicas de encoding

### 1. OrdinalEncoder — **SOLO para ordinales**

Asigna un entero por categoría **respetando el orden que vos definís**. Para `education`, podés decirle: "Preschool=0, 1st-4th=1, ..., Doctorate=15".

```python
from sklearn.preprocessing import OrdinalEncoder

categorias_ordenadas = [" Preschool", " 1st-4th", " 5th-6th", " 7th-8th",
                        " 9th", " 10th", " 11th", " 12th",
                        " HS-grad", " Some-college", " Assoc-voc", " Assoc-acdm",
                        " Bachelors", " Masters", " Prof-school", " Doctorate"]

encoder = OrdinalEncoder(categories=[categorias_ordenadas])
df["education-encoded"] = encoder.fit_transform(df[["education"]])
```

**Regla crítica**: si aplicás `OrdinalEncoder` sobre una variable nominal (`color`, `país`, `suburbio`), le estás inventando un orden al modelo. El modelo va a aprender que "rojo (1) está más cerca de azul (2) que de verde (3)" cuando en realidad los tres son equidistantes en significado. Esto degrada cualquier modelo basado en distancias.

### 2. OneHotEncoder y `pd.get_dummies` — para nominales

Crea **una columna binaria por categoría**. Si tenés `Type ∈ {h, t, u}`, se transforma en:

| Type | Type_h | Type_t | Type_u |
|------|--------|--------|--------|
| h | 1 | 0 | 0 |
| t | 0 | 1 | 0 |
| u | 0 | 0 | 1 |

Cada categoría queda representada por un vector ortogonal. No hay orden inventado: las tres categorías son equidistantes.

```python
# Con pandas
dummies = pd.get_dummies(df['Type'], drop_first=True)
df = pd.concat([df, dummies], axis=1).drop(columns=['Type'])

# Con sklearn
from sklearn.preprocessing import OneHotEncoder
ohe = OneHotEncoder(sparse_output=True, drop='first')
matriz = ohe.fit_transform(df[['Type']])
```

#### `drop_first=True` y colinealidad

Si tenés 3 categorías y creás 3 columnas binarias, esas 3 columnas son **linealmente dependientes** (suman siempre 1). Esa redundancia se llama **multicolinealidad** y rompe modelos lineales (regresión, regresión logística) porque la matriz X'X no se puede invertir.

`drop_first=True` elimina la primera columna. Con 3 categorías quedan 2 columnas: la categoría eliminada se identifica cuando las otras dos son 0. No perdés información, eliminás redundancia.

Para modelos basados en árboles (Random Forest, XGBoost) la colinealidad no rompe nada y `drop_first=False` es aceptable. Para regresión lineal/logística, **siempre** `drop_first=True`.

### 3. DictVectorizer — combinar categóricas + numéricas

Útil cuando tu input ya viene como lista de diccionarios (común en NLP o features extraídos). Aplica OHE a las strings y deja las numéricas como están, todo en una sola matriz esparsa.

```python
from sklearn.feature_extraction import DictVectorizer

feature_dict = df.to_dict(orient='records')
vec = DictVectorizer()
feature_matrix = vec.fit_transform(feature_dict)
# Resultado en Melbourne: sparse (13580, 332)
```

### 4. Codificación de frecuencia

Reemplaza cada categoría por **su frecuencia (o conteo) en el dataset**. Suburbio "Reservoir" aparece 359 veces → se codifica como 359. Suburbio "Albert Park" aparece 47 veces → 47.

Ventajas: una sola columna, no infla dimensionalidad, captura la "popularidad" de cada categoría.

Desventaja: dos categorías con la misma frecuencia se vuelven indistinguibles para el modelo. Es útil para **alta cardinalidad** (muchas categorías distintas) donde OHE crearía cientos de columnas.

```python
freq_map = df['Suburb'].value_counts().to_dict()
df['Suburb_freq'] = df['Suburb'].map(freq_map)
```

---

## Curse of dimensionality del OHE

OHE es la técnica más "honesta" para nominales, pero tiene un costo brutal cuando la cardinalidad es alta. La **maldición de la dimensionalidad** (en inglés *curse of dimensionality*) se manifiesta así:

1. **Vectores de alta dimensionalidad**: si tu columna `Suburb` tiene 314 categorías, OHE crea 314 columnas. Si tu dataset tenía 20 columnas, ahora tiene 333.
2. **Memoria**: en formato denso, una matriz de 13.580 × 332 con dtype int64 son ~36 MB solo para esa parte. Si pasás a float64 (necesario para muchas operaciones), 72 MB.
3. **Vectores ortogonales equidistantes**: cada par de filas codificadas tiene la misma distancia euclídea entre sí (sqrt(2) si difieren en una sola categoría). El espacio se vuelve "plano": KNN no puede distinguir vecinos cercanos de lejanos. Los productos punto pierden significado.

Mitigaciones:
- **Reducir cardinalidad antes del OHE**: agrupar categorías raras en "Otros" (umbral típico: menos de 1% de las observaciones).
- **Codificación de frecuencia** o **target encoding** (no cubierto en esta materia) para variables de muy alta cardinalidad.
- **Matrices esparsas** (sección siguiente).

---

## Matrices esparsas (`scipy.sparse`)

Una matriz **esparsa** (en inglés *sparse*) es una matriz mayoritariamente compuesta por ceros. OHE produce matrices esparsas naturalmente: en una fila con 332 columnas y tres categóricas one-hot codificadas, hay 3 unos y 329 ceros.

`scipy.sparse` guarda solo los valores no nulos y sus posiciones. La memoria crece con los no-nulos (lineal en el número de unos), no con el tamaño total (cuadrático en filas × columnas).

```python
# OneHotEncoder devuelve sparse por defecto
from sklearn.preprocessing import OneHotEncoder
ohe = OneHotEncoder(sparse_output=True)
X_sparse = ohe.fit_transform(df[['Suburb', 'Type', 'CouncilArea']])

print(type(X_sparse))   # scipy.sparse.csr_matrix
print(X_sparse.shape)   # (13580, 332) por ejemplo
print(X_sparse.nnz)     # cantidad de no-nulos (mucho menos que filas*cols)
```

### ¿Cuándo `.todense()` (o `.toarray()`) y cuándo NO?

- **NO densificar** si la matriz ocupa más memoria de la que tenés disponible cuando se expande. Antes de llamar `.todense()`, **calculá el tamaño en MB**: `filas × columnas × bytes_por_celda / 1024 / 1024`. Para una matriz de 13.580 × 332 con `float64` (8 bytes): `13580 × 332 × 8 / 1024² ≈ 34 MB`. Eso entra en RAM. Para 1.000.000 × 10.000 ya estás en 75 GB y se te explota la máquina.
- **SÍ densificar** cuando necesitás operaciones que solo existen en denso (algunas visualizaciones, ciertos imputadores, modelos viejos que no aceptan sparse).
- **Mejor opción**: usar modelos compatibles con sparse (LogisticRegression, SVM linear con `liblinear`, RandomForest, etc.) y mantener la matriz comprimida hasta el final.

---

## Ejemplo numérico

Supongamos una columna `Type` con tres categorías y 6 propiedades:

| ID | Type |
|----|------|
| 1 | h (Casa) |
| 2 | t (Townhouse) |
| 3 | u (Departamento) |
| 4 | h |
| 5 | h |
| 6 | t |

### Aplicación correcta: OneHotEncoder

`pd.get_dummies(df['Type'])` produce:

| ID | Type_h | Type_t | Type_u |
|----|--------|--------|--------|
| 1 | 1 | 0 | 0 |
| 2 | 0 | 1 | 0 |
| 3 | 0 | 0 | 1 |
| 4 | 1 | 0 | 0 |
| 5 | 1 | 0 | 0 |
| 6 | 0 | 1 | 0 |

Con `drop_first=True` queda:

| ID | Type_t | Type_u |
|----|--------|--------|
| 1 | 0 | 0 | (la categoría "h" es la baseline)
| 2 | 1 | 0 |
| 3 | 0 | 1 |
| 4 | 0 | 0 |
| 5 | 0 | 0 |
| 6 | 1 | 0 |

Distancias euclídeas entre filas:
- ID 1 (Casa) vs ID 2 (Townhouse): `sqrt((0-1)² + (0-0)²) = 1`.
- ID 1 (Casa) vs ID 3 (Departamento): `sqrt((0-0)² + (0-1)²) = 1`.
- ID 2 (Townhouse) vs ID 3 (Departamento): `sqrt((1-0)² + (0-1)²) = sqrt(2) ≈ 1.41`.

Las tres categorías están en posiciones distintas; no hay orden inventado.

### Aplicación INCORRECTA: OrdinalEncoder sobre nominales

Si en su lugar aplicás `OrdinalEncoder` mal (sobre una variable que no tiene orden):

```python
encoder = OrdinalEncoder()  # sin pasar `categories=` -> orden alfabético
df['Type_ord'] = encoder.fit_transform(df[['Type']])
```

Esto produce:

| ID | Type | Type_ord |
|----|------|----------|
| 1 | h | 0 |
| 2 | t | 1 |
| 3 | u | 2 |
| 4 | h | 0 |
| 5 | h | 0 |
| 6 | t | 1 |

Distancias:
- ID 1 (h=0) vs ID 2 (t=1): `|0-1| = 1`.
- ID 1 (h=0) vs ID 3 (u=2): `|0-2| = 2`.
- ID 2 (t=1) vs ID 3 (u=2): `|1-2| = 1`.

**El modelo ahora cree que una Casa está al doble de distancia de un Departamento que de una Townhouse**. Inventaste un orden alfabético arbitrario y se lo vendiste al modelo como si fuera estructura real. Si después usás KNN, regresión lineal o cualquier modelo basado en magnitud numérica, va a tomar decisiones equivocadas con confianza.

### Frecuencia (alternativa para alta cardinalidad)

Conteos: `h` aparece 3 veces, `t` 2 veces, `u` 1 vez.

| ID | Type_freq |
|----|-----------|
| 1 | 3 |
| 2 | 2 |
| 3 | 1 |
| 4 | 3 |
| 5 | 3 |
| 6 | 2 |

Inventa una "distancia por popularidad" pero no infla columnas. Útil para `Suburb` con 314 categorías.

---

## Conexión con el TP

**TP1, Ejercicio 1.4 (encoding de categóricas)**: este apunte es prácticamente el manual de instrucciones de ese ejercicio. Decisiones que tenés que justificar:

- **`Suburb` (314 categorías)**: OHE produce 313 columnas adicionales (con `drop_first=True`). Conviene reducir cardinalidad antes: agrupar suburbios con menos de N observaciones en "Otros". Justificá el umbral (por ejemplo, 30 propiedades) con un argumento estadístico: por debajo de eso, la estimación por suburbio es muy ruidosa. Alternativa: codificación de frecuencia. Decidí y dejalo escrito.

- **`SellerG`**: similar problema, alta cardinalidad. Misma estrategia.

- **`CouncilArea` (33 categorías)**: cardinalidad moderada. OHE directo es aceptable, pero 32 columnas adicionales no son gratis. Evaluá si la variable aporta más que `Regionname` (8 categorías), que está fuertemente correlacionada.

- **`Type` (3 categorías)**: OHE sin pensarlo. Es nominal pura, baja cardinalidad, perfecta para one-hot.

- **`Method` (5 categorías)**: igual que `Type`.

- **`Regionname` (8 categorías)**: nominal, OHE con `drop_first=True`.

- **`Date`**: la consigna NO impone tratamiento. Tres opciones razonables:
  1. **Descartar**: si tu objetivo es predecir precio "atemporal", la fecha es ruido. Justificá.
  2. **Año + mes como ordinal**: tratar `Date` como ordinal (fecha más antigua = 0, más nueva = N). Captura tendencia temporal.
  3. **OHE por mes/año**: si sospechás estacionalidad fuerte. Infla dimensionalidad. Mencionar en la entrega.

Cualquiera de las tres es válida si está justificada. La que NO sirve es ignorarla y dejar la columna `object` en el dataset final — el modelo va a romper.

**TP1, encoding sobre NaN**: **NUNCA ENCODEES SOBRE COLUMNAS CON NaN SIN HABERLOS TRATADO ANTES**. `OneHotEncoder` puede crear una columna `Type_nan` que captura el patrón de faltantes; eso puede ser deseable o terrible según el caso. La regla de la cátedra (en mayúsculas porque la dijeron en mayúsculas):

> **"ANTES DE LLEGAR ACÁ TENGO QUE HABER TRABAJADO CON MIS DATOS FALTANTES"**

Si imputás después de encodear, terminás imputando una columna binaria, lo cual no tiene mucho sentido (la media de una binaria es la proporción de 1s, no una categoría). El orden correcto es: imputación → encoding → escalado.

---

## Errores comunes

1. **OrdinalEncoder sobre nominales**: el más frecuente y el más caro. Le inventás un orden al modelo. Si la variable no tiene orden natural escrito por vos, NO uses OrdinalEncoder.
2. **OHE sin pensar dimensionalidad**: hacés `pd.get_dummies(df)` sin filtrar y de repente tu dataset pasó de 20 columnas a 350. La memoria se va, los modelos se ralentizan y las distancias se rompen.
3. **`drop_first=False` por defecto en modelos lineales**: introduce multicolinealidad. Para regresión lineal/logística, siempre `drop_first=True`.
4. **Encodear antes de imputar**: violás el orden correcto. Imputar después es imputar binarias, lo cual deforma todo.
5. **Convertir esparsa a densa sin calcular MB**: `.todense()` sobre una matriz de un millón × diez mil te tira la sesión de Jupyter. Calculá antes.
6. **Mezclar tipos en el encoder**: si pasás un `OrdinalEncoder` un DataFrame con columnas numéricas y categóricas mezcladas sin `ColumnTransformer`, vas a obtener resultados raros o errores silenciosos. Separá numéricas y categóricas explícitamente.
7. **Olvidar codificar `Date`**: queda como `object` y el modelo se cae. O codificarla mal (como string ordinal alfabético, lo cual produce un orden cronológicamente incorrecto: "01/02/2017" es "menor" que "31/01/2017" en orden lexicográfico).

---

## Detrás de escena: por qué `pd.get_dummies` NO es lo mismo que `OneHotEncoder`

Acá hay un tema que **MUCHA gente subestima** hasta que pasa a producción y el modelo predice cualquier cosa porque llegó una categoría nueva que el entrenamiento nunca vio. Las dos herramientas — `pd.get_dummies` y `OneHotEncoder` — producen un resultado **visualmente idéntico** sobre el mismo DataFrame, pero se comportan de forma muy distinta cuando aparece una categoría nueva en test. Vamos por partes.

### El problema concreto

Imaginate que entrenaste tu modelo con `Type ∈ {h, t, u}`. Tres categorías, tres columnas dummies (o dos con `drop_first=True`). Todo perfecto.

Llega test (o producción) y aparece una propiedad con `Type == 'commercial'`. ¿Qué pasa?

```python
# Train: Type ∈ {h, t, u}
train = pd.DataFrame({'Type': ['h', 't', 'u', 'h']})
dummies_train = pd.get_dummies(train['Type'])
# Columnas: ['h', 't', 'u']

# Test: aparece una categoría nueva
test = pd.DataFrame({'Type': ['h', 'commercial']})
dummies_test = pd.get_dummies(test['Type'])
# Columnas: ['commercial', 'h']    ← ¡DESASTRE!
```

`pd.get_dummies` genera las columnas **a partir de los valores que ve en el DataFrame que le pasás**. No tiene memoria de lo que vio en train. Resultado:

- Las columnas de train y test son distintas (`['h', 't', 'u']` vs `['commercial', 'h']`).
- El modelo entrenado espera 3 features en posiciones específicas y va a recibir 2 features en posiciones distintas.
- Si las "alineás" a mano, vas a tener `commercial` que el modelo nunca aprendió a interpretar, o vas a perder la columna `t` y `u` que el modelo sí necesita.

### Por qué OneHotEncoder lo hace bien

`OneHotEncoder` de sklearn implementa el patrón **fit / transform**. En el `fit` aprende qué categorías existen; en el `transform` aplica ese conocimiento a cualquier dataset nuevo.

```python
from sklearn.preprocessing import OneHotEncoder

ohe = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
ohe.fit(train[['Type']])
# Aprende: categorías = ['h', 't', 'u']

X_train = ohe.transform(train[['Type']])    # shape (4, 3)
X_test = ohe.transform(test[['Type']])      # shape (2, 3) — MISMO número de columnas

# La fila 'commercial' queda como [0, 0, 0] (todas las dummies en 0)
# porque handle_unknown='ignore'
```

Tres ventajas:
1. **Mismo número de columnas** en train y test, en el mismo orden. El modelo recibe lo que espera.
2. **`handle_unknown='ignore'`** te deja decidir qué hacer con categorías nuevas: ignorarlas (vector de ceros), tirar error, o (en versiones nuevas de sklearn) mapearlas a una categoría "infrequent".
3. Es **compatible con `Pipeline` y `ColumnTransformer`** de sklearn. El estado entrenado se guarda y se versiona junto con el modelo.

### Tabla comparativa

| Aspecto | `pd.get_dummies` | `OneHotEncoder` |
|---------|------------------|------------------|
| Tipo de salida | DataFrame (lindo de leer) | Matriz numpy o sparse |
| Mantiene estado entre train/test | **No** | Sí (vía `fit`) |
| Manejo de categorías nuevas en test | Crea/pierde columnas | Configurable con `handle_unknown` |
| Integración con Pipeline de sklearn | No (hay que hacer un wrapper) | Sí, nativa |
| Velocidad en datasets chicos | Más rápido | Levemente más lento |
| Trazabilidad para producción | Frágil | Robusta |
| Útil para EDA y exploración | Sí, ideal | Demasiado verboso |

### Cuándo usar cada uno

**Usá `pd.get_dummies`** cuando:
- Estás explorando, haciendo análisis descriptivo, generando una visualización rápida.
- El dataset es uno solo y NO vas a aplicar el encoding a otro dataset distinto.
- Querés un resultado en formato DataFrame con nombres de columnas legibles para inspeccionar.

**Usá `OneHotEncoder`** cuando:
- Vas a entrenar un modelo y aplicarlo después sobre test (siempre).
- Vas a meterlo en un `Pipeline` o `ColumnTransformer`.
- Querés controlar qué pasa con categorías nuevas (`handle_unknown='ignore'`).
- Vas a versionar el preprocesador junto con el modelo (joblib, pickle).

### La trampa típica en TP1

En el TP1 vas a ver tutoriales que hacen `pd.get_dummies(df)` sobre el dataset completo, lo cual es válido **dentro del notebook** porque train y test son el mismo dataset (no estás haciendo split). Pero si después querés aplicar tu pipeline a `melb_data` "nuevo" (otra extracción de la misma fuente, otra ciudad, otra base), `pd.get_dummies` no te garantiza que las columnas sean las mismas.

El patrón correcto para que tu TP1 sea **productivo** (no solo "corre en el notebook"):

```python
from sklearn.preprocessing import OneHotEncoder

# 1. Separar columnas categóricas
cat_cols = ['Type', 'Method', 'Regionname']

# 2. Fit en train (o en el dataset completo del TP)
ohe = OneHotEncoder(handle_unknown='ignore', sparse_output=True, drop='first')
ohe.fit(melb_df[cat_cols])

# 3. Transform — sirve para el mismo dataset Y para cualquier otro futuro
X_cat = ohe.transform(melb_df[cat_cols])

# 4. Acceder a los nombres de las columnas generadas
ohe.get_feature_names_out(cat_cols)
# array(['Type_t', 'Type_u', 'Method_S', ...])
```

Esto te deja el encoder **entrenado y guardable**. Si mañana tu prof te pasa otro CSV de Melbourne, lo aplicás directo: `ohe.transform(otro_df[cat_cols])` y obtenés las mismas columnas en el mismo orden.

### Detalle de `drop_first` vs `drop='first'`

Para mayor confusión: el argumento se llama distinto en cada herramienta.
- `pd.get_dummies(..., drop_first=True)`
- `OneHotEncoder(drop='first')`

Hacen lo mismo: tiran la primera categoría para evitar multicolinealidad. La razón técnica está explicada arriba en este mismo archivo.

### Resumen

- `pd.get_dummies` y `OneHotEncoder` producen lo mismo sobre un dataset, pero solo `OneHotEncoder` mantiene memoria entre train y test.
- Si entrenás con `pd.get_dummies` y aplicás test con `pd.get_dummies` por separado, las columnas casi seguro no coinciden — y tu modelo va a fallar silenciosamente.
- `OneHotEncoder` con `handle_unknown='ignore'` es la opción profesional: maneja categorías nuevas sin romper.
- Para el TP1 podés usar cualquiera, pero acostumbrate a `OneHotEncoder`: es el patrón que vas a usar el resto de tu carrera.

¿Se entiende? Misma matriz de salida en el papel, dos comportamientos distintos cuando aparece algo nuevo.

---

## Checklist de comprensión

- [ ] Te dan una columna `nivel_satisfaccion ∈ {'Malo', 'Regular', 'Bueno', 'Excelente'}`. ¿Qué encoding aplicás y por qué?
- [ ] Te dan una columna `pais ∈ {'Argentina', 'Brasil', 'Uruguay'}`. Si aplicás `OrdinalEncoder` con orden alfabético, ¿qué le estás "diciendo" al modelo y por qué está mal?
- [ ] En TP1, ¿por qué hacer OHE directamente sobre `Suburb` es problemático y qué dos alternativas tenés?
- [ ] ¿Por qué `drop_first=True` es necesario en modelos lineales pero opcional en árboles?
- [ ] Antes de llamar `.todense()` sobre una matriz esparsa, ¿qué cálculo de servilleta hacés primero?
- [ ] Si entrenás con `pd.get_dummies` y en test aparece una categoría nueva, ¿qué pasa concretamente con las columnas? ¿Cómo lo resuelve `OneHotEncoder`?

---

**Próximo paso**: `05-transformaciones.md`
