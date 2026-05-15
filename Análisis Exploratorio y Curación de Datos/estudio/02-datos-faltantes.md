# 02 — Datos faltantes

## Concepto

Un **dato faltante** es información que **debería estar y no está**. Suena trivial, pero arrastra dos preguntas que la cátedra exige separar:

1. **¿Cómo está codificado?** ¿Como `NaN`, como `0`, como `-1`, como `"NA"`, como string vacío? Reconocer la codificación correcta es el primer paso. Si pandas no sabe que un `0` es faltante, lo va a usar como dato válido y todos tus promedios van a estar contaminados.
2. **¿Por qué falta?** ¿Es azar puro? ¿Es porque la persona con sueldo alto se incomoda y no responde? ¿Es porque el sensor falla cuando hace mucho frío? La respuesta a esto define qué técnica de imputación es legítima.

La cátedra trata datos faltantes en **toda la Clase 1** porque es **el primer eslabón crítico del pipeline de curación**. Si los faltantes no se tratan bien, todo lo que viene después (encoding, PCA, modelado) está sobre arena.

## Intuición

Pensá los faltantes como **lluvia sobre un mapa**:

- **MCAR** (Missing Completely At Random): llueve **al azar** sobre toda la ciudad. No importa si la casa es alta, baja, rica, pobre, vieja o nueva: la gota tiene la misma chance de caer en cualquier techo. Si tirás los techos mojados, los que quedan son una muestra **insesgada** de toda la ciudad. Podés "secar" el dataset eliminando filas y no se distorsiona nada.

- **MAR** (Missing At Random): llueve **donde hay terreno alto**. La lluvia sigue siendo "aleatoria", pero **condicionada** a otra variable observable (la altura). Si conocés la altura del terreno, podés predecir dónde llovió y reconstruir con bastante exactitud qué techos hubieran tenido lluvia. La imputación con modelos (KNN, MICE) funciona bien acá.

- **MNAR** (Missing Not At Random): llueve **solo donde había paraguas**. La gota cae únicamente donde el techo, por su propia naturaleza, tenía algo que la atrae. La presencia o ausencia de la lluvia depende **del valor que está oculto**. No hay forma de imputarlo sin sesgar: necesitás salir a la calle y recolectar de nuevo.

Esta analogía es importante: la diferencia entre MCAR/MAR/MNAR **no es sobre los datos que tenés, sino sobre el mecanismo que los generó**. Y vos no observás el mecanismo: solo podés razonar sobre él con conocimiento de dominio y diagnóstico visual.

---

## Distinciones previas que muchos confunden

### NaN vs None

| Concepto | Qué es | Cómo se comporta |
|----------|--------|------------------|
| `NaN` | Float estándar IEEE-754 (*Not a Number*) | Se propaga en aritmética: `NaN + 1 = NaN`. Pandas y NumPy lo usan para marcar faltantes |
| `None` | Singleton de Python, tipo `NoneType` | Rompe operaciones vectorizadas. `None + 1` tira `TypeError` |

Por eso pandas/NumPy usan NaN: **se puede meter en operaciones masivas** sin romper todo. Cuando una columna tiene `None`, pandas la suele dejar como `object`, lo cual te deshabilita las operaciones numéricas vectorizadas. La conversión correcta:

```python
df["col"] = df["col"].replace({None: np.nan})
df["col"] = pd.to_numeric(df["col"], errors="coerce")  # los no parseables → NaN
```

### Perdido vs inexistente

Cita de la cátedra:

> *"Perdido = sabemos que existe pero no se conoce. Inexistente = no puede ser recolectado (ej. tamaño del 3er dormitorio en una casa de 2 ambientes). Python no distingue."*

Los dos terminan como `NaN`, pero conceptualmente son cosas distintas:

- **Perdido**: existe el dato real, no se registró. Imputar puede tener sentido.
- **Inexistente**: el dato **no aplica**. Imputarlo es inventar realidad que no existe.

Pandas no los distingue, **vos sí tenés que distinguirlos** con conocimiento de dominio. Si imputás el "tamaño del tercer dormitorio" en una casa de dos ambientes, estás generando información ficticia.

### Predecir vs imputar

Lo vimos en el archivo 01, lo refrescamos:

| Verbo | Sobre qué actúa |
|-------|-----------------|
| **Predecir** | Valor que no fue muestreado (no está en la tabla) |
| **Imputar** | Valor no informado (debería estar y no está) |

Cita textual: *"Imputar es predecir esos datos."* Operativamente la cuenta es la misma, pero la intención cambia y, por lo tanto, también la validación de la calidad: una imputación buena reproduce la distribución observada; una predicción buena reproduce la distribución futura.

### Imputación determinística vs estocástica

- **Determinística**: rellenar siempre con el mismo valor (la media, la mediana, una constante). Fácil, rápido, **sin incertidumbre**. Subestima la varianza original.
- **Estocástica**: rellenar usando información de otras variables **+ ruido aleatorio**. La cátedra lo define así: *"usa otras variables + incertidumbre asociada en lugar de un valor fijo"*. Más cara, pero respeta la varianza. Es lo que hace MICE bien configurado.

---

## Taxonomía de Rubin: MCAR, MAR, MNAR

Esta taxonomía la propuso Donald Rubin en los años 70 y sigue siendo **el marco oficial** para razonar sobre faltantes. La cátedra la usa textual:

### MCAR — Missing Completely At Random

> *"Los faltantes no dependen de variables observadas ni del valor."*

- **Analogía**: lluvia que cae al azar sobre toda la ciudad.
- **Mecanismo**: una falla técnica aleatoria del sensor; un dedazo del encuestador en cualquier fila; una página que se perdió al digitalizar la encuesta.
- **Implicancia**: la muestra **sin** los faltantes es **insesgada** de la muestra completa. Podés hacer `dropna()` sin distorsionar (perdiendo solo potencia estadística).
- **Cuándo se acepta**: cuando el porcentaje de faltantes es bajo (< 5–10% como regla de pulgar) y no hay un patrón identificable.

### MAR — Missing At Random

> *"La pérdida se explica completamente como función de OTRAS variables observadas."*

- **Analogía**: lluvia que cae solo donde el terreno está alto. El terreno (la altura) está en tu dataset.
- **Mecanismo**: hombres mayores responden menos sus ingresos, pero **conocés su edad y género**. La probabilidad de faltante en `ingresos` se modela a partir de `edad` y `género`.
- **Implicancia**: si imputás usando esas variables observadas, podés reconstruir el valor faltante sin introducir sesgo (en promedio). KNN, MICE, regresión condicional, todas funcionan acá.
- **Trampa**: vos podés *creer* que estás en MAR cuando en realidad la variable que explicaría el faltante **no la observaste**. Eso te lleva a MNAR sin que te des cuenta.

### MNAR — Missing Not At Random

> *"La pérdida depende del propio valor no observado."*

- **Analogía**: lluvia que cae solo donde había paraguas. El paraguas es el valor del techo y vos no lo ves.
- **Mecanismo**: las personas con sueldo muy alto omiten responder cuánto ganan (el faltante depende del propio ingreso, que no observás).
- **Implicancia**: la cátedra es contundente: *"Lo mejor es recolectar nuevos datos. Cualquier imputación introduce sesgo."*
- **Por qué duele**: no hay test estadístico que distinga MAR de MNAR sin tener los valores reales (que justamente son los que faltan). Solo podés razonar con conocimiento de dominio.

### Tabla resumen

| Mecanismo | El faltante depende de... | Imputable | Técnica recomendada |
|-----------|---------------------------|-----------|---------------------|
| **MCAR** | Nada (azar puro) | Sí, trivialmente | `dropna()` o cualquier otra |
| **MAR** | Otras variables **observadas** | Sí, con modelo condicional | KNN, MICE, regresión |
| **MNAR** | El propio valor no observado | **No** (sin sesgar) | Recolectar más datos |

Cita operativa de la cátedra: *"MAR/MCAR → técnicas anteriores OK; MNAR → recolectar más datos. Probar distintas técnicas para que el post-procesamiento no dependa del pre-procesamiento."* Es decir: no te enamores de una sola técnica, comparala con otra para verificar que tu conclusión no es un artefacto de la imputación elegida.

---

## Estrategias de tratamiento: árbol de decisiones

La cátedra ordena las estrategias en este árbol:

```
Faltante detectado
│
├── Eliminar
│   ├── Puntual (un solo valor)
│   ├── Columna entera (si > 80% faltante)
│   └── Fila entera (si MCAR y % bajo)
│
├── Imputar — matriz estática
│   ├── Constante (categóricas: nueva categoría)
│   ├── Media (numéricas simétricas)
│   ├── Mediana (numéricas asimétricas)
│   └── Moda (most_frequent, categóricas)
│
├── Imputar — series temporales
│   ├── ffill (forward fill: tomar el último valor conocido)
│   ├── bfill (backward fill: tomar el próximo valor conocido)
│   └── Interpolación lineal
│
└── Imputar — avanzado (multivariado)
    ├── KNN (k vecinos más cercanos)
    └── MICE / IterativeImputer (rotativo, con incertidumbre)
```

### Pros y contras (tabla canónica de la Clase 1)

| Estrategia | Ventaja | Desventaja / Riesgo | Cuándo usarla |
|------------|---------|----------------------|---------------|
| **dropna por fila** | Simple, no inventa nada | Pierde información. Sesga si pérdida no es MCAR | MCAR + bajo % |
| **dropna por columna** | Saca una variable problemática | Rompe en test si test tiene valores donde train no tenía | Columna con >80% faltante |
| **`SimpleImputer(strategy="constant")`** | Categóricas: agrega "categoría nueva" para marcar | No considera correlaciones. **Introduce sesgo** | Categóricas donde el faltante es informativo |
| **`strategy="most_frequent"` (moda)** | Categóricas sin necesidad de encoding | Sobrerrepresenta la moda | Categóricas con clase dominante |
| **`strategy="mean"`** | Numéricas, rápida | Distorsiona si hay asimetría. Subestima varianza | Numéricas **simétricas** |
| **`strategy="median"`** | Robusta a outliers | Subestima varianza | Numéricas **asimétricas** o con outliers |
| **`KNNImputer`** | Considera correlaciones con vecinos | Requiere numéricas **estandarizadas**. Costoso en memoria | MAR, datos numéricos, dataset chico/medio |
| **`IterativeImputer` (MICE)** | Modela cada feature en función de las otras. Estocástico | No soporta tipos mixtos sin encoding previo | MAR con relaciones multivariadas |
| **miceforest / MissForest** | Manejan tipos mixtos (numéricas + categóricas) | Más lentos, librerías externas | MAR con dataset mixto grande |

Pista clave: *"Probar distintas técnicas para que el post-procesamiento no dependa del pre-procesamiento."* Si tu conclusión cambia drásticamente según imputaste con media o con KNN, **tu conclusión es frágil** y eso es información valiosa.

---

## NUNCA accionar sobre el original

Esto es **cita textual de la cátedra**, y va en mayúsculas porque es la regla que más gente rompe:

> **NUNCA ACCIONAR SOBRE EL DATASET ORIGINAL.**

Patrón obligatorio antes de cualquier tratamiento de faltantes:

```python
melb_data = pd.read_csv(url)   # crudo, intocable
melb_df = melb_data.copy()     # copia de trabajo
# ... toda la curación va sobre melb_df ...
```

Si no hacés `.copy()`, dos cosas malas pasan:

1. **Perdés el "antes"**: no podés verificar cuánto cambió tu imputación porque pisaste el original.
2. **Concatenás errores**: si en la celda 7 ejecutás algo mal y en la celda 12 te das cuenta, restaurar requiere recargar el CSV desde cero. En notebooks con celdas en cualquier orden, esto se vuelve una pesadilla.

Y por eso el código de la Clase 1 abre así, sin excepción:

```python
melb_df = melb_data.copy()
melb_df.loc[melb_df.Bathroom < 1, "Bathroom"] = pd.NA
```

---

## Análisis visual con `missingno`

Antes de imputar nada, **mirá** los faltantes. `missingno` (alias `msno`) te da tres gráficos que la cátedra usa en la Clase 1:

```python
import missingno as msno
```

### `msno.bar(df, sort="ascending")`

Barras de **completitud** por columna. Una barra al 100% significa que la columna no tiene faltantes; una al 50% significa que falta la mitad. Lo primero que mirás: ¿qué columnas tienen problema y en qué orden de magnitud?

```python
msno.bar(melb_data, sort="ascending")
```

### `msno.matrix(df)`

Mapa de calor de presencia/ausencia, fila por fila. **Las rayas blancas** marcan faltantes. Si las rayas se alinean entre columnas (faltan juntas), hay correlación de faltantes: cuando falta una variable, suele faltar otra. Eso es señal de **MAR estructural**.

```python
msno.matrix(melb_data.sample(200))   # 200 filas al azar para no saturar
```

### `msno.heatmap(df)`

Matriz de **correlación de faltantes**. Valor cercano a 1 entre dos variables = cuando falta una, falta la otra. Valor cercano a -1 = cuando falta una, la otra está siempre presente. Es el chequeo más fuerte para distinguir MCAR de MAR.

```python
msno.heatmap(melb_data)
```

Heurística práctica: si el heatmap muestra correlaciones fuertes (> 0.5) entre faltantes, **no es MCAR**. Probablemente sea MAR (las dos variables vienen del mismo formulario que el encuestado dejó incompleto). La imputación con métodos multivariados (KNN, MICE) tiene sentido.

---

## Código de imputación, técnica por técnica

### Eliminación (`dropna`)

```python
# Eliminar filas con cualquier NaN (drástico)
melb_df.dropna()

# Eliminar filas solo si NaN está en columnas críticas
melb_df.dropna(subset=["Price", "Rooms"])

# Eliminar columnas que tengan más del 80% de NaN
threshold = 0.8 * len(melb_df)
melb_df.dropna(axis=1, thresh=threshold)
```

Lectura: `subset` te deja **acotar** qué columnas miran al decidir si tirar una fila. Es lo más conservador.

### `SimpleImputer` (constante, media, mediana, moda)

`SimpleImputer` es la API de `sklearn` para imputación a nivel columna, sin cruzar con otras variables.

```python
from sklearn.impute import SimpleImputer

# Constante (típico para categóricas: marca "faltante" como categoría)
imp_const = SimpleImputer(strategy="constant", fill_value="MISSING")

# Moda — most_frequent (categóricas sin encoding)
imp_mode = SimpleImputer(strategy="most_frequent")

# Media (numéricas simétricas)
imp_mean = SimpleImputer(strategy="mean")

# Mediana (numéricas asimétricas, robusta a outliers)
imp_median = SimpleImputer(strategy="median")

# Aplicación: fit + transform
out = imp_median.fit_transform(melb_df[["Car"]])
melb_df["Car"] = out
```

Por qué `fit_transform` y no `df.fillna(df.median())` directo: porque `SimpleImputer` **guarda el valor aprendido** (`imp_median.statistics_`). Eso te permite aplicar **la misma media/mediana del train** al test sin recalcular (evita leak). En notebooks educativos pasa desapercibido; en producción es la diferencia entre un pipeline correcto y uno que pierde dinero.

### `KNNImputer`

```python
from sklearn.impute import KNNImputer

# Importante: KNN exige NUMÉRICAS y ESTANDARIZADAS
# Por eso esto es típicamente paso 2 después de escalar
knn = KNNImputer(n_neighbors=3, weights="uniform")
melb_imputado = knn.fit_transform(melb_df_numeric_scaled)
```

Lectura del bloque:

- `n_neighbors=3`: para cada fila con NaN, busca las 3 filas más parecidas (sin NaN en esa columna) y promedia.
- `weights="uniform"`: las 3 contribuyen igual. `weights="distance"` les da más peso a las más cercanas.
- **Requisito clave**: las distancias se calculan en el espacio de todas las variables. Si una variable está en miles (precio) y otra en unidades (cantidad de baños), el precio domina la distancia. Por eso **hay que estandarizar antes** (típicamente con `MinMaxScaler` o `StandardScaler`).

Cita de la cátedra: *"KNN exige numéricas ESTANDARIZADAS."*

### `IterativeImputer` (MICE)

MICE = *Multiple Imputation by Chained Equations*. Es la artillería pesada de la imputación univariada-condicional.

```python
from sklearn.experimental import enable_iterative_imputer   # opt-in obligatorio
from sklearn.impute import IterativeImputer
from sklearn.linear_model import BayesianRidge
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import ExtraTreesRegressor

# Versión por defecto: BayesianRidge como estimador interno
mice = IterativeImputer(random_state=10, estimator=BayesianRidge())
melb_mice = mice.fit_transform(melb_df_numeric)

# Versión con KNN como estimador (lo que pide el TP1)
mice_knn = IterativeImputer(estimator=KNeighborsRegressor(n_neighbors=5), random_state=10)
melb_mice_knn = mice_knn.fit_transform(melb_df_numeric)
```

Cómo funciona, en una línea: **modela cada feature como una función de las otras**, en forma rotatoria. Para imputar `BuildingArea`, lo predice usando `Rooms`, `YearBuilt`, `Price`, etc. Para imputar `Rooms`, lo predice usando `BuildingArea`, `YearBuilt`, etc. Iterativamente, hasta que las imputaciones convergen.

**Regla de Rubin** (citada en clase): `var_total = var_dentro + var_entre`. Significa que la varianza de las imputaciones múltiples (cuando corrés MICE varias veces) tiene dos componentes: la incertidumbre dentro de una corrida y la diferencia entre corridas. Esto es lo que distingue una imputación honesta (estocástica) de una que finge precisión.

**Limitación**: el `IterativeImputer` de `sklearn` **no soporta tipos mixtos**. Necesita todo numérico. Para mixtos, hay alternativas: `miceforest`, `MissForest`, `Datawig`.

### Imputación de series temporales

```python
df["temp"].fillna(method="ffill")        # forward fill: arrastra el último
df["temp"].fillna(method="bfill")        # backward fill: trae el próximo
df["temp"].interpolate(method="linear")  # interpolación entre vecinos
```

Solo tiene sentido si la columna tiene **orden temporal**. Aplicar `ffill` en un dataset sin orden te da basura.

---

## Ejemplo numérico: 3 estrategias sobre la misma mini-tabla

Tenés esta tabla con un faltante en `Price`:

| id | Suburb     | Rooms | Bathroom | BuildingArea | Price     |
|----|------------|-------|----------|--------------|-----------|
| 1  | Abbotsford | 3     | 1.0      | 79.0         | 1480000   |
| 2  | Abbotsford | 2     | 1.0      | 65.0         | 1035000   |
| 3  | Carlton    | 4     | 2.0      | 142.0        | 1876000   |
| 4  | Carlton    | 3     | 1.0      | 134.0        | NaN       |
| 5  | Carlton    | 2     | 1.0      | 91.0         | 850000    |
| 6  | Brunswick  | 2     | 1.0      | 89.0         | 920000    |

Vamos a imputar el NaN de la fila 4 (`Price`) con tres estrategias distintas y discutir cuál tiene más sentido.

### Estrategia 1: media global

Media de los 5 precios conocidos:

```
(1.480.000 + 1.035.000 + 1.876.000 + 850.000 + 920.000) / 5 = 1.232.200
```

`Price` imputado: **$1.232.200**.

Pro: trivial.
Contra: ignora que la fila 4 es de Carlton, donde la mediana es más alta. Subestima el verdadero valor probable.

### Estrategia 2: mediana por grupo (`Suburb`)

Mediana de Price para `Suburb == "Carlton"`:

```
Carlton: [1876000, 850000]  → mediana = (850000 + 1876000) / 2 = 1.363.000
```

`Price` imputado: **$1.363.000**.

Pro: aprovecha la información del suburbio. Mejor que la media global.
Contra: ignora `BuildingArea` (134 m², que es grande dentro de Carlton). Sigue siendo univariado por grupo.

### Estrategia 3: KNN con k=3 sobre todas las numéricas

Si calculamos la distancia euclidiana de la fila 4 (Rooms=3, Bathroom=1, BuildingArea=134) contra las otras 5 filas, **después de estandarizar**, los 3 vecinos más cercanos son típicamente:

- Fila 1 (Abbotsford, 3 amb, 1 baño, 79 m², $1.480.000) — cerca por rooms y bathroom
- Fila 3 (Carlton, 4 amb, 2 baños, 142 m², $1.876.000) — cerca por BuildingArea
- Fila 5 (Carlton, 2 amb, 1 baño, 91 m², $850.000) — cerca por bathroom

Promedio de los 3 precios:

```
(1.480.000 + 1.876.000 + 850.000) / 3 = 1.402.000
```

`Price` imputado: **$1.402.000**.

Pro: usa **todas** las variables observadas (Rooms, Bathroom, BuildingArea) para encontrar parecidos. Es lo más cercano a "buscaste casas parecidas y promediaste".
Contra: depende de la métrica de distancia. Si no estandarizás, `BuildingArea` (entre 65 y 142) domina sobre `Bathroom` (entre 1 y 2), y los vecinos cambian.

### ¿Cuál es mejor?

Depende del mecanismo:

| Si el mecanismo es... | Mejor estrategia |
|-----------------------|------------------|
| MCAR (faltó al azar) | Cualquiera funciona. Hasta tirar la fila es válido |
| MAR (faltó porque la casa era cara y la inmobiliaria no publicó precio) | KNN o MICE, porque "ser cara" se infiere de Rooms/BuildingArea |
| MNAR (faltó porque era una venta privada que se negó a publicar) | Ninguna imputación es válida sin sesgo |

Lo correcto en TP es **probar 2 o 3 estrategias y discutir cómo cambian las conclusiones**. La cátedra lo pide explícito: *"probar distintas técnicas para que el post-procesamiento no dependa del pre-procesamiento"*.

---

## Heurística de cierre (cita textual)

> *"MAR/MCAR → técnicas anteriores OK; MNAR → recolectar más datos."*

Es la regla operativa. Si después del análisis visual concluís que estás en MNAR, no hay imputación que te salve. Hay que **volver a la etapa de recolección**, no a la de pre-procesamiento.

---

## Conexión con el TP

- **TP1 ejercicio 2 (imputación KNN)**: la consigna pide agregar `YearBuilt` y `BuildingArea` (que tenían ~5375 y ~6450 faltantes respectivamente) y aplicar `IterativeImputer(estimator=KNeighborsRegressor)`. La pregunta del enunciado "¿hace falta estandarizar?" tiene una sola respuesta correcta: **sí**, porque KNN usa distancia euclidiana y `BuildingArea` (en metros) tiene una escala muy distinta a `Rooms` (en unidades). Sin estandarizar, `BuildingArea` domina la distancia y los vecinos elegidos son malos. La consigna también pide **graficar la distribución antes y después** de la imputación — esa es la verificación visual de que la imputación no destrozó la forma original.

- **TP1, decisión sobre `BuildingArea` y `YearBuilt`**: ambos tienen >40% de faltantes. La pregunta es: ¿se imputan o se descartan? La cátedra los **imputa** (el ejercicio lo pide), pero un argumento alternativo válido sería: con tanto faltante, la imputación inventa demasiado. Esa discusión es exactamente lo que pide la entrega documental del TP.

- **TP2 ejercicio 2 (Postcode como float)**: cuando una columna numérica tiene NaN, pandas la pasa a `float64`. Eso significa que `Postcode` en `melb_data` es `5234.0` en lugar de `5234`. Si la mergeás contra AirBnB y `zipcode` es `int64`, **el merge falla por tipos incompatibles** o, peor, devuelve filas vacías. Antes del merge:
  ```python
  melb_df["Postcode"] = melb_df["Postcode"].fillna(-1).astype(int)
  # o, mejor todavía, eliminar las filas con Postcode faltante si son pocas
  ```
  Este es **un faltante con consecuencias en cascada**: no es solo "falta un valor", es "rompe la integridad del merge". Lo vas a sentir cuando un assert de filas post-merge te dé un número distinto al esperado.

- **TP2, validaciones post-imputación**: la consigna pide assertions explícitas sobre rangos y nulos después de cualquier operación crítica. La imputación de faltantes es una operación crítica. Después de imputar `BuildingArea`, asertá que `melb_df.BuildingArea.between(0, 2000).all()`. Si la imputación generó valores absurdos (por ejemplo, negativos), el assert lo detecta.

---

## Errores comunes

1. **Confundir cero con faltante**: en Melbourne, `Bathroom == 0` y `BuildingArea == 0` son faltantes enmascarados, pero `Car == 0` es "sin cochera" (válido). Distinguirlos pide conocimiento de dominio, no código.
2. **Asumir MCAR sin evidencia**: hacer `dropna()` directo "porque son pocos" sin haber mirado el heatmap. Si el heatmap muestra correlación de faltantes entre dos columnas, no es MCAR.
3. **Confundir NaN con None**: `None + 1` rompe; `NaN + 1 = NaN`. Asegurate de que tu columna tenga NaN (float) y no None (object).
4. **Imputar con media sobre distribución asimétrica**: la media de `Price` en Melbourne está dominada por outliers. La mediana es mucho mejor estimador del "valor típico".
5. **KNN sin estandarizar**: cita textual: *"KNN exige numéricas ESTANDARIZADAS."* Si no estandarizás, la columna con mayor escala absoluta (Price, BuildingArea) domina la distancia y arruina los vecinos.
6. **MICE con tipos mixtos**: `IterativeImputer` de sklearn solo acepta numérico. Si tu dataset tiene categóricas, las tenés que **encodear primero**, después MICE, después decodear. Alternativa: `miceforest` o `MissForest`.
7. **Imputar y olvidar verificar**: imputar 6.450 valores de `BuildingArea` cambia drásticamente la distribución. Si no comparás histograma antes/después, te perdés el destrozo.
8. **Tratar todos los faltantes con la misma técnica**: `Car` (62 NaN, ~0.5%) y `BuildingArea` (6450 NaN, ~47%) **no** se tratan igual. Para `Car`, casi cualquier técnica anda. Para `BuildingArea`, hay que pensar si vale la pena imputar tanto.
9. **Pisar el original sin copia**: lo más caro de revertir. La regla NUNCA ACCIONAR SOBRE EL ORIGINAL no es decorativa.
10. **Imputar en MNAR**: si concluiste que el mecanismo es MNAR, ninguna técnica es válida. Imputar igual te da una falsa sensación de completitud y un análisis sesgado que parece limpio. **Lo correcto es documentar la limitación y, si se puede, recolectar más datos.**

---

## Detrás de escena: pd.NA vs np.nan vs None

Acá hay un tema que **te va a confundir el primer día** y te va a perseguir todo el cuatrimestre si no lo entendés bien. La cátedra usa `pd.NA` en el código de la Clase 1 (`melb_df.loc[..., "Bathroom"] = pd.NA`), pero en los datasets que leés con `read_csv` los faltantes vienen como `np.nan`. Y a veces aparece `None` cuando lo metiste vos sin querer. **Son tres cosas distintas**, con tres comportamientos distintos.

### Cada uno vive en un universo

| Símbolo | Origen | Tipo Python | Filosofía |
|---------|--------|-------------|-----------|
| `np.nan` | NumPy | `float` (¡sí, es un float!) | "Operación matemática inválida" (IEEE 754) |
| `None` | Python puro | `NoneType` (singleton) | "Ausencia total de valor" |
| `pd.NA` | Pandas (≥ 1.0) | `NAType` (singleton propio) | "Valor faltante, tipo-agnóstico" |

```python
import numpy as np
import pandas as pd

type(np.nan)    # <class 'float'>
type(None)      # <class 'NoneType'>
type(pd.NA)     # <class 'pandas._libs.missing.NAType'>
```

Que `np.nan` sea un `float` parece raro, pero es por la norma IEEE 754: NaN es un patrón de bits reservado dentro del universo de los floats. No hay un "NaN entero" en NumPy. Ese detalle es lo que hace que una columna `int64` con un solo NaN se promueva a `float64` automáticamente (ver archivo 00).

### Cómo se comportan en operaciones

Acá está la trampa real:

```python
# np.nan se PROPAGA en aritmética
np.nan + 1       # nan
np.nan * 0       # nan
np.nan == np.nan # False (!!)  — NaN no es igual a sí mismo

# None ROMPE en aritmética
None + 1         # TypeError: unsupported operand type(s)
None == None     # True
None is None     # True (lo correcto siempre con None)

# pd.NA es "tipo-agnóstico" y propaga lógica de tres valores
pd.NA + 1        # <NA>
pd.NA == pd.NA   # <NA>   ← ni True ni False: "no se sabe"
pd.NA | True     # True   ← lógica de tres valores (Kleene)
pd.NA & False    # False
```

El detalle de "NaN no es igual a NaN" rompe el sentido común pero está en la norma IEEE 754. Por eso `df[df.col == np.nan]` siempre devuelve un DataFrame vacío. La forma correcta es `df[df.col.isna()]`. Es la misma razón por la que SQL usa `IS NULL` y no `= NULL` (lo vas a ver en el archivo 10).

### Cuándo aparece cada uno

- **`np.nan`** aparece naturalmente cuando `pd.read_csv` encuentra una celda vacía o un valor no parseable en una columna numérica. Es el faltante "histórico" de pandas, el que vas a ver el 95% del tiempo.
- **`None`** aparece cuando vos lo metés a mano (`df.loc[5, "col"] = None`) o cuando lees datos desde una fuente Python (JSON, lista de dicts) que tiene `null`. Pandas lo suele guardar en columnas `object`, lo cual **te deshabilita las operaciones numéricas vectorizadas**.
- **`pd.NA`** aparece cuando usás los nuevos dtypes "nullable" de pandas (`Int64`, `boolean`, `Float64` con mayúscula, `string`). Es el faltante moderno, diseñado para funcionar con cualquier tipo (entero, booleano, string).

### Qué usar y cuándo

| Situación | Usá |
|-----------|-----|
| Marcar un faltante en una columna `float64` clásica | `np.nan` o `pd.NA` (pandas convierte) |
| Marcar un faltante en una columna `Int64` (nullable) | `pd.NA` (obligado: NaN se promovería a float) |
| Marcar un faltante en una columna `object`/string | Cualquiera, pero conviene `pd.NA` para consistencia |
| Detectar faltantes (cualquiera de los tres) | `df.isna()` o `df.isnull()` (son alias, hacen lo mismo) |
| Comparar para filtrar | **NUNCA** `== np.nan`. Siempre `.isna()` |

```python
# MAL — siempre devuelve vacío
df[df["Price"] == np.nan]

# BIEN — funciona con NaN, None y pd.NA por igual
df[df["Price"].isna()]
```

### La trampa típica en EyCD

La cátedra usa `pd.NA` en la línea canónica:

```python
melb_df.loc[melb_df.Bathroom < 1, "Bathroom"] = pd.NA
```

¿Por qué `pd.NA` y no `np.nan`? Porque es el faltante "moderno" y funciona con cualquier dtype. Pero **OJO**: si después hacés `melb_df.isnull().sum()`, te cuenta los `pd.NA` igual que los `np.nan`. La función `isnull()` es tolerante.

El bug que vas a sufrir es otro: si filtrás con `melb_df[melb_df.Bathroom == pd.NA]`, no vas a obtener nada (devuelve `<NA>` que se interpreta como `False` en filtros). Otra vez: **siempre `.isna()`**.

### Resumen

- `np.nan` es float. Se propaga en aritmética. NaN ≠ NaN (¡cuidado!).
- `None` es Python puro. Rompe operaciones. Convive en columnas `object`.
- `pd.NA` es lo nuevo. Tipo-agnóstico. Compatible con `Int64`, `boolean`, `string`.
- Para detectar cualquiera de los tres, usá `.isna()` o `.isnull()`. Nunca `== nan`.
- En el código del TP usá `pd.NA` cuando marqués faltantes nuevos; vas a ser consistente con la cátedra.

¿Se entiende? Tres símbolos para "está vacío", pero con comportamientos distintos. Si te confundís cuál usar, `.isna()` los pesca a los tres.

---

## Checklist de comprensión

- [ ] ¿Podés explicar con la analogía de la lluvia la diferencia entre MCAR, MAR y MNAR sin mirar la tabla?
- [ ] ¿Por qué `KNNImputer` requiere estandarización y `SimpleImputer(strategy="mean")` no?
- [ ] Si imputás `BuildingArea` con la mediana y después graficás la nueva distribución, ¿qué cambio esperás ver respecto de la original y cómo lo justificás?
- [ ] ¿Por qué `df[df.col == np.nan]` siempre devuelve vacío? ¿Cuál es la forma correcta?
- [ ] ¿En qué se diferencia `pd.NA` de `np.nan` y cuándo conviene cada uno?

---

**Próximo paso**: `03-sesgo.md`
