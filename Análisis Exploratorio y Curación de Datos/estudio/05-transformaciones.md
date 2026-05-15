# 05 — Transformaciones

## Concepto

Una vez que tus variables son todas numéricas (porque imputaste faltantes y codificaste las categóricas), todavía hay decisiones por tomar. Las variables numéricas pueden estar en escalas muy distintas (`Price` en cientos de miles, `Rooms` entre 1 y 10) o tener formas de distribución muy raras (colas largas, sesgo, picos). Eso afecta a casi cualquier modelo que dependa de **distancias** (KNN, K-means, SVM), **gradientes** (regresiones, redes neuronales) o **varianzas** (PCA).

La cátedra distingue tres operaciones que en el lenguaje cotidiano se mezclan, pero que conceptualmente son distintas:

| Operación | Qué cambia | Sobre qué |
|-----------|------------|-----------|
| **Escalar** (en inglés *scale*) | El RANGO de los valores | Variables numéricas |
| **Normalizar** (en inglés *normalize*) | La FORMA de la distribución | Variables numéricas |
| **Encoding** | El TIPO (texto a número) | Variables categóricas |

**Orden correcto**: primero encoding (texto → número), después transformación (escala o forma).

## Intuición

Pensá un mapa de Buenos Aires. **Escalar** es cambiar la escala del mapa de 1:10.000 a 1:50.000: las distancias se achican proporcionalmente, pero la forma de la ciudad sigue siendo la misma. Si Palermo era más grande que Boedo en el mapa original, sigue siendo más grande en el mapa nuevo, solo que más chiquito todo.

**Normalizar** es cambiar la **proyección** cartográfica: pasar de proyección Mercator a Robinson. Ahí cambia la forma misma de los continentes: Groenlandia se hace más chica, África más grande, los meridianos dejan de ser paralelos. Es una operación más profunda que el escalado.

**Encoding** es otra cosa entera: es traducir "Avenida Corrientes" a coordenadas GPS. No estás cambiando la escala ni la proyección: estás convirtiendo texto en números.

Esa distinción importa porque las herramientas tienen nombres confusos. `StandardScaler` se llama "Scaler" pero conceptualmente está más cerca de una normalización (cambia la forma a una con media 0 y varianza 1, no solo el rango). El nombre engaña; la operación es lo que importa.

---

## Escaladores (cambian rango, mantienen forma)

### MinMaxScaler

Lleva los valores al rango fijo `[0, 1]` (o `[-1, 1]` si lo configurás):

$$
x' = \frac{x - x_{\min}}{x_{\max} - x_{\min}}
$$

- **Cuándo**: cuando necesitás un rango acotado conocido. Útil para redes neuronales con activaciones sigmoideas, o para visualizar variables en un mismo plano.
- **Trampa**: es **extremadamente sensible a outliers**. Un solo valor altísimo "aplasta" a todo el resto en el extremo inferior del rango. Si tenés outliers, casi siempre conviene RobustScaler.

```python
from sklearn.preprocessing import MinMaxScaler
X_scaled = MinMaxScaler().fit_transform(X)
```

### MaxAbsScaler

Divide cada valor por el **máximo del valor absoluto** de la columna. Resultado: rango `[-1, 1]`, pero **preserva el cero** (los ceros siguen siendo ceros).

- **Cuándo**: datos **ralos** (en inglés *sparse*, con muchos ceros). Es el escalador correcto para matrices que salen de OHE o TF-IDF, donde la mayoría de los valores son cero y no querés "centrarlos" (centrar los rompe).
- **Razón técnica**: centrar una matriz esparsa la convierte en densa (cada cero se vuelve un `-media`). Si tu matriz tenía 95% de ceros y la centrás, ahora tiene 0% de ceros y la memoria explota.

```python
from sklearn.preprocessing import MaxAbsScaler
X_sparse_scaled = MaxAbsScaler().fit_transform(X_sparse)  # preserva esparsidad
```

### RobustScaler

Usa la **mediana** y el **rango intercuartílico** (en inglés *IQR*, `Q3 - Q1`) en lugar de la media y el desvío:

$$
x' = \frac{x - \text{mediana}(x)}{Q3(x) - Q1(x)}
$$

- **Cuándo**: datos con **outliers** (valores atípicos extremos). La mediana y el IQR son robustos a outliers, así que la transformación no se distorsiona por uno o dos valores extremos.
- **Resultado**: NO queda en un rango fijo `[0, 1]`. La mediana queda en 0 y el IQR en 1, pero los outliers pueden seguir muy lejos. Eso es deseable: querés conservarlos para que el modelo los vea, no querés borrarlos.

```python
from sklearn.preprocessing import RobustScaler
X_robust = RobustScaler().fit_transform(X)
```

### StandardScaler (z-score)

Centra en media 0 y varianza 1:

$$
z = \frac{x - \mu}{\sigma}
$$

donde `μ` (mu) es la media muestral y `σ` (sigma) el desvío estándar.

- **Cuándo**: cuando esperás una distribución **aproximadamente gaussiana** (en forma de campana) y querés ponerlas todas en la misma escala estandarizada. Es el default de muchos métodos: PCA, regresión penalizada (Ridge, Lasso), métodos basados en descenso por gradiente.
- **Trampa**: la media y el desvío son sensibles a outliers. Si tenés un valor de $50.000.000 y el resto está en torno a $500.000, el desvío se infla y todos los valores razonables quedan apretados cerca de 0. Diagnóstico: si después de StandardScaler tu boxplot se ve casi plano con un par de puntos lejísimos, tenés outliers que arruinaron la escala. Cambiá a RobustScaler.

```python
from sklearn.preprocessing import StandardScaler
X_std = StandardScaler().fit_transform(X)
```

**Nota técnica**: aunque la cátedra lo llama "normalización z-score" en algunas slides, en scikit-learn está bajo "escaladores". Es el caso donde el nombre conceptual y el nombre de librería difieren.

---

## Normalizar por fila: `normalize(l1/l2/max)`

A diferencia de los escaladores (que operan **por columna**, una variable a la vez), `normalize` opera **por fila**: lleva cada muestra a tener **norma 1**.

Tres opciones:
- `norm='l1'`: la suma de los valores absolutos de la fila es 1.
- `norm='l2'`: la raíz cuadrada de la suma de los cuadrados es 1 (norma euclídea).
- `norm='max'`: el máximo absoluto de la fila es 1.

- **Cuándo**: cuando lo que importa es la **dirección del vector**, no la magnitud. Casos típicos: texto (TF-IDF antes de coseno), histogramas de color, productos punto en kernels SVM.
- **Trampa**: rompe la información de magnitud. Una fila con todos los valores duplicados queda idéntica a la original. Si tu modelo necesita saber "esta propiedad es grande", no normalices por fila.

```python
from sklearn.preprocessing import normalize
X_norm = normalize(X, norm='l2', axis=1)  # por fila
```

---

## Transformaciones de forma (cambian distribución)

### QuantileTransformer

Mapea los valores a una distribución de destino, ya sea **uniforme** `[0, 1]` o **normal**. Usa la transformación `G⁻¹(F(X))`, donde `F` es la CDF (en inglés *Cumulative Distribution Function*, función de distribución acumulada) empírica y `G⁻¹` la inversa de la CDF de destino.

- **Cuándo**: cuando tu variable tiene una forma rara (multimodal, con colas pesadas) y necesitás "domesticarla" para un modelo que asume normalidad o uniformidad.
- **Ventajas**: muy **robusta a outliers** (los aplasta automáticamente al final de la cola), no requiere supuestos sobre la distribución original.
- **Desventajas**: **distorsiona correlaciones y distancias** entre variables. Después de aplicar QuantileTransformer a varias variables, las relaciones entre ellas pueden cambiar (porque cada una se transforma independientemente). Cuidado con interpretarlas como lineales después.

```python
from sklearn.preprocessing import QuantileTransformer

qt = QuantileTransformer(output_distribution='normal', random_state=0)
X_qt = qt.fit_transform(X)
```

### PowerTransformer (Box-Cox, Yeo-Johnson)

Aplica una transformación paramétrica que **acerca la distribución a gaussiana**. Ajusta un parámetro `λ` (lambda) por columna para maximizar la normalidad (medida por verosimilitud).

- **Box-Cox**: requiere **`x > 0`** estrictamente. Fórmula:
  $$
  y(\lambda) = \begin{cases} \frac{x^\lambda - 1}{\lambda} & \lambda \ne 0 \\ \ln(x) & \lambda = 0 \end{cases}
  $$
  El caso `λ = 0` es el **logaritmo natural**: por eso log es un caso particular de Box-Cox.

- **Yeo-Johnson**: extensión de Box-Cox que **acepta valores negativos y ceros**. Mismo objetivo, dominio más amplio.

- **Cuándo**: cuando tu variable tiene cola derecha pesada (típico en precios, ingresos, áreas) y querés simetrizarla para un modelo que asume normalidad (regresión lineal, ANOVA, ciertos tests).
- **Diferencia con Quantile**: Power produce una transformación **paramétrica suave** (monotónica, derivable) que conserva mejor las relaciones lineales. Quantile es no paramétrica, más agresiva, mejor con outliers extremos.

```python
from sklearn.preprocessing import PowerTransformer

bc = PowerTransformer(method='box-cox')        # x > 0
yj = PowerTransformer(method='yeo-johnson')    # acepta negativos
X_yj = yj.fit_transform(X)
```

---

## Tabla mental: cuándo cada una

| Situación | Transformación recomendada |
|-----------|---------------------------|
| Datos con **outliers** | **RobustScaler** |
| Datos **ralos** (esparsos, muchos ceros) | **MaxAbsScaler** |
| Necesito **rango fijo `[0, 1]`** (red neuronal, viz) | **MinMaxScaler** |
| Datos aproximadamente **gaussianos** | **StandardScaler** |
| Necesito **forma gaussiana exacta** | **PowerTransformer** o **QuantileTransformer** (normal) |
| Solo me importa **dirección del vector** | **normalize(l2)** |
| Modelo basado en **distancias** (KNN, K-means, SVM, PCA) | Escalar SÍ o SÍ (cualquiera de los escaladores) |
| Modelos basados en **árboles** (Random Forest, XGBoost) | No es necesario escalar |

---

## Ejemplo numérico

Vector `x = [10, 20, 30, 40, 50]`.

### StandardScaler

- Media: `μ = (10+20+30+40+50)/5 = 30`.
- Desvío estándar (poblacional, como hace sklearn por defecto):

$$
\sigma = \sqrt{\frac{(10-30)^2 + (20-30)^2 + (30-30)^2 + (40-30)^2 + (50-30)^2}{5}} = \sqrt{\frac{400+100+0+100+400}{5}} = \sqrt{200} \approx 14{,}14
$$

- Valores transformados:

| `x` | `(x - μ) / σ` | Resultado |
|-----|---------------|-----------|
| 10 | (10-30)/14.14 | **-1.41** |
| 20 | (20-30)/14.14 | **-0.71** |
| 30 | (30-30)/14.14 | **0.00** |
| 40 | (40-30)/14.14 | **+0.71** |
| 50 | (50-30)/14.14 | **+1.41** |

Media del resultado: 0. Desvío: 1. La forma de la distribución (simétrica, equiespaciada) se conservó.

### MinMaxScaler

- `min = 10`, `max = 50`, rango = 40.
- Valores transformados:

| `x` | `(x - min) / (max - min)` | Resultado |
|-----|---------------------------|-----------|
| 10 | (10-10)/40 | **0.00** |
| 20 | (20-10)/40 | **0.25** |
| 30 | (30-10)/40 | **0.50** |
| 40 | (40-10)/40 | **0.75** |
| 50 | (50-10)/40 | **1.00** |

Mínimo del resultado: 0. Máximo: 1. Equiespaciado, como esperábamos.

### Comparación

Ambos produjeron resultados equiespaciados porque la distribución original ya era simétrica y sin outliers. La diferencia es de **escala numérica**: Standard te da valores entre `-1.41` y `+1.41` (con media 0), MinMax entre `0` y `1`. Para algoritmos sensibles a la magnitud de los inputs, esa diferencia puede importar (por ejemplo, en redes neuronales con activaciones acotadas).

### ¿Qué pasa si agregás un outlier?

Vector con outlier: `x = [10, 20, 30, 40, 50, 1000]`.

- Con **StandardScaler**: media = 191.7, σ ≈ 363. Los valores razonables quedan apretados cerca de `-0.5`, el outlier en `+2.2`. La escala "útil" del 99% de los datos se aplastó porque el 1% mandó.
- Con **MinMaxScaler**: min=10, max=1000. Los valores razonables quedan apretados entre `0.00` y `0.04`. Casi indistinguibles. Peor todavía.
- Con **RobustScaler**: mediana = 35, IQR ≈ 25. Los valores razonables quedan entre `-1.0` y `+0.6`, el outlier en `+38.6`. La escala "útil" se preservó y el outlier sigue siendo visiblemente atípico para el modelo. Esto es lo que querés.

---

## Conexión con el TP

### TP1 — Estandarizar antes de KNN

**Sí, obligatorio**. KNNImputer y KNeighborsRegressor calculan **distancias euclídeas** entre observaciones. Si una variable está en miles (`Price`) y otra entre 1 y 10 (`Rooms`), `Price` domina la distancia: la diferencia entre dos propiedades es básicamente la diferencia de precio, `Rooms` no influye.

La consigna del TP1 pregunta explícitamente *"¿hace falta estandarizar?"* para que vos justifiques **por qué sí**. Respuesta: porque KNN se basa en distancias y las distancias son sensibles a escala.

Opción recomendada: **MinMaxScaler** (la cátedra la sugiere para KNN) o StandardScaler. Si hay outliers fuertes en `Landsize` o `BuildingArea`, considerar RobustScaler antes y luego MinMax sobre el resultado robustizado.

### TP1 — Escalar antes de PCA

**Sí, obligatorio también**. PCA descompone la matriz de covarianza. Si una variable tiene varianza mucho mayor que las otras (porque está en otra escala), va a dominar el primer componente principal aunque no sea la más informativa.

La cátedra muestra el experimento sobre Melbourne:
- Con **MinMaxScaler(-1, 1)**: PC1 explica ~17% de varianza, distribución equilibrada.
- Con **StandardScaler**: PC1 explica solo ~2.2% — porque el `max` después de estandarizar es 88 (un outlier muy fuerte) y el `min` es -2.89. Ese outlier infla la varianza de esa columna y desbalancea la descomposición.

Lección de la cátedra: *"sklearn centra los datos restándoles la media. Sin embargo, es recomendable también estandarizar o al menos escalar la matriz original para asegurar que todas las variables estén en las mismas unidades y ninguna tenga un peso demasiado grande."*

Si tu Melbourne tiene outliers fuertes (los tiene en `Price`, `Landsize`, `BuildingArea`), conviene RobustScaler antes de PCA, o eliminar outliers por IQR primero y después aplicar StandardScaler.

### Orden recomendado para el pipeline del TP1

1. Trabajar faltantes (Clase 1).
2. Encoding categóricas (Clase 2.2).
3. Escalado/transformación numéricas (Clase 2.3, este apunte).
4. Imputación KNN (necesita el paso 3 hecho).
5. PCA (necesita los pasos 3 y 4 hechos).

Si invertís el orden, te tropezás. Imputar con KNN sin escalar = imputación dominada por una variable. PCA sin escalar = PC1 capturando varianza espuria.

---

## Errores comunes

1. **StandardScaler con outliers fuertes**: la media y el desvío se inflan, los valores "normales" quedan apretados. Síntoma: después del escalado el boxplot parece plano. Solución: RobustScaler, o eliminar outliers primero.

2. **Centrar datos ralos**: si tu matriz tiene 95% de ceros y le aplicás StandardScaler (que centra restando la media), cada cero se convierte en `-media` y la matriz pierde su esparsidad. La memoria explota. Solución: MaxAbsScaler, que preserva el cero.

3. **Confundir escalar (rango) con normalizar (forma)**: son operaciones distintas. Escalar mantiene la forma (un boxplot con cola larga sigue teniendo cola larga después de MinMaxScaler), normalizar la cambia. Saber qué hace cada una.

4. **Confundir escalar (por columna) con `normalize` (por fila)**: `normalize(X)` opera por fila y le da norma 1 a cada muestra. No es lo mismo que `StandardScaler`. Si pusiste `normalize` y querías estandarizar, todas tus variables ahora tienen rangos distintos según las otras variables de la misma fila.

5. **Escalar antes de splittear train/test**: si calculás `μ` y `σ` sobre el dataset completo y después separás train/test, hay **filtración de datos** (en inglés *data leakage*) del test al entrenamiento. Lo correcto: `scaler.fit(X_train)`, después `scaler.transform(X_test)`.

6. **Aplicar transformaciones a la variable objetivo sin invertir**: si transformás `y` con log o Box-Cox para entrenar, después tenés que invertir la transformación al predecir. Si no, tus predicciones están en escala transformada.

7. **PCA sin escalar**: la columna con mayor varianza absoluta domina los primeros componentes aunque no sea informativa. PCA siempre va precedida por escalado.

8. **Box-Cox sobre valores no positivos**: Box-Cox requiere `x > 0` estricto. Si tu variable tiene ceros o negativos, usá Yeo-Johnson.

---

## Detrás de escena: por qué `fit_transform` en test es data leakage

Acá hay un tema que **te van a tomar en cualquier entrevista de Data Science** y que la mayoría de la gente entiende mal porque "el código corre". El detalle es chiquito: `fit_transform(train)` y después `transform(test)`. Si hacés `fit_transform` también en test, tenés **data leakage** (en inglés *filtración de datos*) y tu evaluación es una mentira. Vamos a desarmarlo.

### Qué hace `fit_transform` por dentro

Cuando aplicás `StandardScaler().fit_transform(X)`, sklearn hace **dos pasos** en uno:

1. **`fit(X)`**: calcula la media `μ` y el desvío `σ` de cada columna y los guarda dentro del objeto.
2. **`transform(X)`**: aplica la fórmula `(X - μ) / σ` usando esos parámetros guardados.

Visualmente:

```python
scaler = StandardScaler()

# Equivalente:
scaler.fit(X_train)              # calcula μ y σ sobre X_train
X_train_std = scaler.transform(X_train)   # aplica la fórmula

# A esto:
X_train_std = scaler.fit_transform(X_train)
```

Después podés ver los parámetros aprendidos: `scaler.mean_` y `scaler.scale_`. Son los que el scaler va a usar para transformar **cualquier** dato futuro.

### Qué pasa si hacés `fit_transform(test)`

Si en test escribís `X_test_std = scaler.fit_transform(X_test)`, **estás recalculando `μ` y `σ` con los valores del test**. Eso significa que:

1. Tu test ahora está estandarizado contra **su propia distribución**, no contra la del train.
2. **Información del test "filtró" al modelo**: el modelo entrenado conocía un cierto rango de valores, y ahora le pasás un test escalado a otro rango. El modelo predice mal sin saber por qué.
3. La evaluación de tu modelo es **optimista falsa**: en producción, donde solo tendrás train para fittear el scaler, las métricas reales van a ser peores.

### Ejemplo concreto

Imaginate train con `Price ∈ [500.000, 2.000.000]` y test (más nuevo, post-inflación) con `Price ∈ [2.000.000, 5.000.000]`.

**Forma correcta** (`fit` solo en train):
```python
scaler.fit(X_train)         # μ_train ≈ 1.000.000, σ_train ≈ 400.000
X_train_std = scaler.transform(X_train)   # valores cerca de 0, σ=1
X_test_std = scaler.transform(X_test)     # valores entre +2.5 y +10 (fuera del rango entrenado, ¡correcto!)
```

El test queda **lejos del centro entrenado**. Eso es real: tu modelo no vio precios tan altos, y la métrica de error va a reflejarlo honestamente.

**Forma incorrecta** (`fit_transform` en test):
```python
scaler.fit_transform(X_train)        # ok
scaler.fit_transform(X_test)         # ¡recalcula μ, σ con test!
# μ_test ≈ 3.500.000, σ_test ≈ 800.000
# X_test_std queda cerca de 0, σ=1 — IGUAL que train aunque sean datos distintos
```

Ahora train y test parecen "iguales" en el espacio escalado. El modelo predice "bien" pero está mintiendo: en producción real, los datos nuevos no vendrán con `fit` mágico.

### Por qué es "leakage"

Leakage = información que **no deberías tener al momento de predecir** se filtra al modelo. En el caso del scaler, lo que filtra es la **distribución del test**: la media y el desvío del conjunto que querías mantener "ciego".

El test simula producción. En producción, cuando llega una fila nueva, no podés calcular la media con todo el resto del test porque las filas llegan de a una. La única media que tenés disponible es la del train. Por eso `fit` va una vez, en train, y nada más.

### Regla general que aplica a TODO sklearn (no solo scaler)

| Operación | Train | Test |
|-----------|-------|------|
| `StandardScaler` / `MinMaxScaler` / `RobustScaler` | `fit_transform` | `transform` |
| `SimpleImputer` (media, mediana) | `fit_transform` | `transform` |
| `KNNImputer` | `fit_transform` | `transform` |
| `IterativeImputer` (MICE) | `fit_transform` | `transform` |
| `OneHotEncoder` | `fit_transform` | `transform` |
| `PCA` | `fit_transform` | `transform` |
| `PowerTransformer` (Box-Cox, Yeo-Johnson) | `fit_transform` | `transform` |
| Modelo (regresión, RF, etc.) | `fit` | `predict` |

**Patrón único**: en train aprendés los parámetros, en test los aplicás. Sin excepciones.

### Excepción aparente: cuando aún NO splitteaste

Si estás en una fase 100% exploratoria (EDA) y todavía no hiciste `train_test_split`, podés usar `fit_transform` sobre el dataset completo solo para **mirar**. Pero antes de modelar, vas a tener que reescribir el código con el patrón correcto.

### Cómo se ve el patrón en código real

```python
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

# 1. Split SIEMPRE primero
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 2. Fit en train, transform en train
imputer = SimpleImputer(strategy='median')
X_train_imp = imputer.fit_transform(X_train)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_imp)

# 3. Transform en test (NO fit)
X_test_imp = imputer.transform(X_test)
X_test_scaled = scaler.transform(X_test_imp)

# 4. Modelo (mismo patrón)
modelo.fit(X_train_scaled, y_train)
y_pred = modelo.predict(X_test_scaled)
```

Mejor todavía: meté todo en un `Pipeline` y se aplica el patrón solito.

```python
from sklearn.pipeline import Pipeline

pipe = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler()),
    ('modelo', LinearRegression()),
])

pipe.fit(X_train, y_train)        # fit aplica fit_transform internamente
pipe.predict(X_test)              # predict aplica transform internamente
```

### Resumen

- `fit_transform = fit + transform`. El `fit` aprende parámetros (media, desvío, categorías); el `transform` los aplica.
- En train: `fit_transform`. En test: solo `transform`.
- Si hacés `fit_transform` en test, estás filtrando la distribución del test al preprocesador. Eso es **data leakage**.
- La regla aplica a TODO sklearn (scaler, imputer, encoder, PCA, modelo). Sin excepciones.
- Usar `Pipeline` te evita el error: maneja `fit_transform` vs `transform` automáticamente.

¿Se entiende? Es un detalle de una palabra (`fit_transform` vs `transform`) pero la diferencia entre un pipeline honesto y uno que se miente a sí mismo.

---

## Checklist de comprensión

- [ ] ¿Cuál es la diferencia conceptual entre escalar (MinMaxScaler) y normalizar (PowerTransformer)? ¿Cuándo elegís cada uno?
- [ ] En TP1, justificá en una frase por qué hay que escalar antes de KNN y antes de PCA.
- [ ] Si tu variable `Price` tiene outliers fuertes (algunas mansiones de varios millones), ¿qué escalador NO usarías y por qué? ¿Cuál sí?
- [ ] ¿Por qué MaxAbsScaler es el escalador correcto para una matriz que sale de OneHotEncoder, y qué pasaría si en su lugar usaras StandardScaler?
- [ ] ¿En qué se diferencia `normalize(X, norm='l2', axis=1)` de `StandardScaler().fit_transform(X)`?
- [ ] ¿Por qué `scaler.fit_transform(X_test)` es data leakage y cuál es el patrón correcto?

---

**Próximo paso**: `06-pca.md`
