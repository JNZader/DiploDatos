# 15 — Guía paso a paso del TP1

> **Material de estudio — DiploDatos UNC 2026 — Introducción al Aprendizaje Automático.**
> Este capítulo es una **guía**, no la solución. Cubre el `Trabajo_Practico_1.ipynb` (*Laboratorio 1: Regresión en California*) ejercicio por ejercicio: contexto teórico, pasos sugeridos, snippets clave, trampas técnicas, sanity checks y errores comunes.
> Está pensado para acompañar al notebook abierto: leés la consigna, leés esta guía, escribís código vos.

---

## Tabla de contenidos

1. [Introducción](#introducción)
2. [Dataset California Housing](#dataset-california-housing)
3. [Mapa de ejercicios → capítulos del estudio](#mapa-de-ejercicios--capítulos-del-estudio)
4. [Setup recomendado](#setup-recomendado)
5. [Reglas de oro](#reglas-de-oro)
6. [TRAMPA CRÍTICA: DataFrame vs ndarray](#trampa-crítica-dataframe-vs-ndarray)
7. [Ejercicio 1 — Descripción de los Datos y la Tarea](#ejercicio-1--descripción-de-los-datos-y-la-tarea)
8. [Ejercicio 2 — Visualización de los Datos](#ejercicio-2--visualización-de-los-datos)
9. [Ejercicio 3 — Regresión Lineal](#ejercicio-3--regresión-lineal)
10. [Ejercicio 4 — Regresión Polinomial](#ejercicio-4--regresión-polinomial)
11. [Ejercicio 5 — Regresión con más de un Atributo](#ejercicio-5--regresión-con-más-de-un-atributo)
12. [Ejercicio 6 (opcional) — A Todo Feature](#ejercicio-6-opcional--a-todo-feature)
13. [Ejercicio 7 (opcional) — Regularización Ridge](#ejercicio-7-opcional--regularización-ridge)
14. [Reflexión sobre uso de IA](#reflexión-sobre-uso-de-ia)
15. [Checklist final antes de entregar](#checklist-final-antes-de-entregar)
16. [Apéndice A — Snippets reutilizables](#apéndice-a--snippets-reutilizables)
17. [Apéndice B — Referencias bibliográficas para el TP1](#apéndice-b--referencias-bibliográficas-para-el-tp1)
18. [Apéndice C — Mini-FAQ del TP1](#apéndice-c--mini-faq-del-tp1)

---

## Introducción

### Objetivo del TP

El TP1 propone aplicar todo lo visto en la **Clase 1** (regresión lineal, MSE, train/test split) y la **Clase 2** (regresión polinomial, capacidad, overfitting/underfitting, regularización Ridge) sobre un dataset real de regresión: **California Housing**.

El enunciado (cell-1 del notebook) lo dice con claridad:

> "El objetivo de este trabajo es que puedas aplicar los conceptos de regresión sobre un dataset real, tomando decisiones propias en cada etapa: **qué atributos usar, qué modelo elegir y cómo interpretar los resultados**. No se trata solo de ejecutar el código: se espera que puedas **justificar tus elecciones**, **interpretar los errores obtenidos** y **explicar qué está pasando** en cada experimento. Al finalizar, deberías poder responder: ¿qué modelo elegirías para este problema y por qué? ¿Cómo reconocés underfitting y overfitting en tus resultados?"

Traducido a criterios de corrección esperables (no hay rúbrica explícita pero se deduce del tono):

- **No basta con código que corra**: cada decisión debe estar justificada por escrito.
- **Hay que interpretar los errores**: no se trata sólo de imprimirlos; explicar qué significan en relación a la complejidad del modelo y al dataset.
- **Hay que detectar overfitting/underfitting**: por curva train vs test, por magnitud de coeficientes, por brecha entre errores.

### Tipo de problema

**Regresión supervisada** (target continuo). Ver `03-regresion-lineal.md §1` para la definición formal del problema y la diferencia con clasificación.

### Entregable

El **mismo notebook completado**, con:

- Código en las celdas marcadas (`# 1. Resolver acá.`, etc.).
- Respuestas escritas en las celdas marcadas como `raw` o `markdown` (las que dicen `**Responder acá**` o `*Escribí tu respuesta acá*`).
- La reflexión final sobre uso de IA (cells 37-42), que es **obligatoria** aunque no haya rúbrica explícita.

> **Nota administrativa.** El notebook **no especifica** fecha de entrega, formato del archivo, ni si es individual o grupal. Si la cátedra no aclara por canales paralelos (foro/aula), preguntá antes de asumir. La convención DiploDatos previa suele ser entrega individual del `.ipynb` con el formato `Apellido_Nombre_TP1.ipynb`.

---

## Dataset California Housing

### Origen y características

- **Fuente sklearn:** `sklearn.datasets.fetch_california_housing` ([docs](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.fetch_california_housing.html)).
- **Origen real:** Pace, R. Kelley & Barry, Ronald (1997). *"Sparse Spatial Autoregressions"*, Statistics and Probability Letters, 33, 291–297. Datos del censo de EE.UU. de 1990 agregados por *block group* (la unidad geográfica más fina del censo, típicamente 600-3000 habitantes).
- **Shape:** `X` de `(20640, 8)`, `y` de `(20640,)`.
- **Tipo:** todos los atributos son **numéricos continuos**. No hay categóricos, no hay missing values, no hace falta encoding.

### Atributos (feature_names)

| # | Nombre | Significado |
|---|--------|------------|
| 0 | `MedInc` | Ingreso mediano del block group (en decenas de miles de USD de 1990). |
| 1 | `HouseAge` | Antigüedad mediana de las viviendas del block group (en años). |
| 2 | `AveRooms` | **Promedio** de habitaciones por hogar en el block group. |
| 3 | `AveBedrms` | **Promedio** de dormitorios por hogar. |
| 4 | `Population` | Población total del block group. |
| 5 | `AveOccup` | Ocupación promedio (personas por hogar). |
| 6 | `Latitude` | Latitud del centroide del block group. |
| 7 | `Longitude` | Longitud del centroide del block group. |

### Variable objetivo (target)

- Nombre interno: `target`.
- Significado: **valor mediano de la vivienda del block group**, expresado en *cientos de miles de dólares*. El ylabel del notebook (cell-15) lo dice: `'median house value [x 100 000 USD]'`.
- Rango: aproximadamente `[0.15, 5.0]` (es decir, entre 15.000 y 500.000 USD).
- **Hay un *cap* superior en 5.0**: las viviendas que en realidad valían más de 500k aparecen agrupadas en `y=5.0`. Esto es una particularidad histórica del dataset (censo, privacidad) y se ve a ojo como una "barra horizontal" en `y=5.0` en todos los scatters. **Mencionalo en la respuesta del Ejercicio 1 — es un sesgo importante.**

### ¿Por qué este dataset?

Reemplaza al viejo **Boston Housing** (que fue retirado de sklearn por razones éticas — incluía un atributo `B` con una transformación de la proporción de población afroamericana que reforzaba sesgos). California Housing es el reemplazo estándar para enseñar regresión: tamaño moderado, features interpretables, target continuo, no triviales pero tampoco imposibles de modelar.

> Más contexto en `01-introduccion-y-flujo-ml.md §3` (paradigmas de ML, datos como insumo).

---

## Mapa de ejercicios → capítulos del estudio

| Ejercicio | Tema | Capítulo del estudio | Clase de origen |
|-----------|------|---------------------|-----------------|
| Ej 1 | EDA, dominio, sesgos | `02-tipos-de-aprendizaje.md §2`, `01-introduccion-y-flujo-ml.md §4` | Clase 1 (intro) |
| Ej 2 | Visualización, intuición de features | `03-regresion-lineal.md §1-§2` | Clase 1 |
| Ej 3 | Regresión lineal univariada, MSE, train/test | `03-regresion-lineal.md §3-§5`, `05-funcion-de-costo-y-mse.md §1-§3` | Clase 1 |
| Ej 4 | Regresión polinomial, capacidad, overfitting | `04-regresion-polinomial.md §1-§4`, `06-overfitting-underfitting-capacidad.md §1-§3` | Clase 2 |
| Ej 5 | Regresión multivariada | `04-regresion-polinomial.md §5` (extensión multivariada) | Clase 2 |
| Ej 6 (opt) | Regresión múltiple completa | `04-regresion-polinomial.md §5`, `06-overfitting-underfitting-capacidad.md §4` | Clase 2 |
| Ej 7 (opt) | Ridge / regularización L2 | `07-regularizacion-ridge.md §1-§3` | Clase 2 |

> Si todavía no escribiste estos capítulos: los nombres son los que **se van a usar** en el estudio. Si ya tenés otra nomenclatura, ajustá las referencias internas.

---

## Setup recomendado

### Bibliotecas

```python
# Imports estándar del TP
import numpy as np
import matplotlib.pyplot as plt

from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_squared_error
```

### Versiones

- **scikit-learn ≥ 1.0** (el TP fue diseñado para >=1.0; idealmente 1.2 o superior).
- **numpy ≥ 1.20**.
- **matplotlib ≥ 3.4**.

Para chequear versiones:

```python
import sklearn, numpy, matplotlib
print("sklearn:", sklearn.__version__)
print("numpy:", numpy.__version__)
print("matplotlib:", matplotlib.__version__)
```

### Semilla random

El notebook **ya fija `random_state=0`** en el split (cell-9). **Respetá ese valor**: cambiarlo da splits distintos y resultados no comparables con los del enunciado ("error en test menor a 50").

```python
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=0)
# X_train: (16512, 8) — X_test: (4128, 8)
```

### Notebook starter

Las primeras celdas (0 a 11) ya vienen resueltas en el notebook. **No las toques**: cargan el dataset y arman el split. Tu trabajo arranca en el **Ejercicio 1** (celda 12-13) y termina en la **Reflexión** (celdas 37-42).

---

## Reglas de oro

1. **NO modifiques las celdas de setup** (cells 0–11). Si cambiás el `random_state=0` o el `train_size=0.8`, tus errores no van a coincidir con las observaciones del enunciado.
2. **Justificá TODO**. Cada decisión técnica (qué feature elegir, qué grado de polinomio, qué `alpha`) tiene que tener una oración explicándola. Tono semi-formal, voseo o "ud." — lo importante es que se entienda el porqué.
3. **Métrica única: MSE**. El TP **sólo pide MSE** ("error cuadrático medio"). Si querés agregar R² o RMSE, sumalos como complemento, **no como reemplazo**.
4. **Una sola semilla por experimento**. No varíes `random_state` para que "te dé mejor" — eso es *p-hacking*.
5. **Train vs test, no validation**. El TP1 usa sólo split train/test (sin validation set). Para Ej 4 (regresión polinomial), la curva "train vs test" hace de proxy de la curva train vs validation que aparece en la teoría (`06-overfitting-underfitting-capacidad.md §3`). **Conceptualmente esto es imperfecto** (estás usando el test set para elegir hiperparámetros, lo que produce *leakage* leve), pero es lo que pide el enunciado.
6. **El notebook tiene celdas raw**: las celdas que dicen "Responder acá" o "Escribí tu respuesta acá" son del tipo `raw`. Si querés que se rendericen lindo, **convertilas a markdown** (`Esc + M` en Jupyter / `Cell → Cell Type → Markdown`).
7. **Hacelo a mano antes de pedirle a la IA**. Si vas a usar IA, primero probá vos. La reflexión final se nota muchísimo cuando alguien sólo copió código sin entender.

---

## TRAMPA CRÍTICA: DataFrame vs ndarray

### El problema

El notebook arranca con esta celda **ya resuelta** (cell-4):

```python
from sklearn.datasets import fetch_california_housing
X_california, y_california = fetch_california_housing(return_X_y=True, as_frame=True)
california = fetch_california_housing()
```

Y luego usa:

```python
X, y = california['data'], california['target']
```

**Acá está la trampa**: `california = fetch_california_housing()` **sin** `as_frame=True` devuelve un Bunch donde `california['data']` es un **ndarray** de NumPy. Pero como en la primera línea pidió `as_frame=True`, la versión `X_california` sí es DataFrame. Coexisten ambas.

Después, el código de ayuda usa **indexado tipo ndarray** sobre `X`:

```python
plt.scatter(X[:, selector], y, ...)        # cell-15
X_train_f = X_train[:, selector]            # cell-20
X_train_fs = X_train[:, selector]           # cell-33
```

**Si `X` viene del Bunch sin `as_frame=True`** (que es lo que ocurre con la línea `california = fetch_california_housing()` por defecto), `X[:, selector]` funciona porque `X` es ndarray.

**Pero — y acá viene la trampa — muchos alumnos:**

1. Tocan la celda 4 y ponen `as_frame=True` en la segunda llamada también.
2. O reemplazan `X = california['data']` por `X = X_california`.
3. O cargan el dataset en otro entorno con sklearn más nuevo, donde el default cambia.

En cualquiera de esos casos, `X` queda como `DataFrame` y `X[:, selector]` explota con:

```
InvalidIndexError: (slice(None, None, None), array([False, True, False, ...]))
```

> **Para verificar la fuente**, ver [docs oficial de `fetch_california_housing`](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.fetch_california_housing.html). El default actual de `as_frame` es `False`, pero esto puede cambiar.

### Soluciones (las tres alternativas)

#### Opción A — Forzar ndarray al cargar

La más segura. Modificá la celda 4 para que `X` sea siempre ndarray:

```python
from sklearn.datasets import fetch_california_housing

california = fetch_california_housing(as_frame=False)   # ndarray garantizado
X, y = california['data'], california['target']
```

#### Opción B — Convertir a values después

Si no querés tocar la celda 4 y `X` ya es DataFrame:

```python
X = np.asarray(X)        # o bien X.values
y = np.asarray(y)
# A partir de acá X[:, selector] funciona.
```

#### Opción C — Usar `.iloc` con `selector`

Aprovechando que es DataFrame, usá su API:

```python
X_train_f = X_train.iloc[:, selector]   # selector booleano funciona con iloc
```

> **Cuidado con la opción C**: si después hacés `LinearRegression().fit(X_train_f, y_train)`, sklearn acepta DataFrame sin problema (lo convierte internamente), pero algunas líneas como `np.min(X_train_f)` siguen funcionando porque pandas hereda los métodos de numpy. **Sólo cuidado con concatenar con arrays plain si lo intentás manualmente.**

### Cómo detectarlo antes de que explote

Insertá esto justo después de la celda de carga:

```python
print("Tipo de X:", type(X).__name__)        # ndarray o DataFrame
print("Tipo de X_train:", type(X_train).__name__)
```

Si decís "ndarray" → tranquilo, podés usar `X[:, selector]`.
Si decís "DataFrame" → aplicá una de las 3 opciones de arriba.

### ¿Por qué la guía le dedica tanto espacio a esto?

Porque cada año ~30% de los alumnos se traban **en el Ejercicio 2** por este motivo. La guía equivalente del TP1 de **Estadística y Ciencia de Datos** marcaba un typo del PCA que rompía a media clase; en IAA, el equivalente es esta ambigüedad DataFrame/ndarray. **Si entendés esto antes de empezar, te ahorrás 2 horas de frustración.**

---

## Ejercicio 1 — Descripción de los Datos y la Tarea

### Consigna (cell-12, literal)

Responda las siguientes preguntas:

1. ¿De qué se trata el conjunto de datos?
2. ¿Cuál es la variable objetivo que hay que predecir? ¿Qué significado tiene?
3. ¿Qué información (atributos) hay disponibles para hacer la predicción?
4. ¿Qué atributos imagina ud. que serán los más determinantes para la predicción?
5. ¿Qué problemas observa a priori en el conjunto de datos? ¿Observa posibles sesgos, riesgos, dilemas éticos, etc? Piense que los datos pueden ser utilizados para hacer predicciones futuras.

> **No hace falta escribir código para responder estas preguntas.**

### Conceptos teóricos

- **EDA (análisis exploratorio):** entender el dominio antes de modelar. Ver `01-introduccion-y-flujo-ml.md §4` (proceso de entrenamiento).
- **Sesgos en datos:** los datos heredan los sesgos del proceso que los generó. Ver `02-tipos-de-aprendizaje.md §2.5` si hay sección de ética, o las notas del PDF de la clase 1 (slide sobre datos como insumo).

### Pasos sugeridos

1. **Aunque la consigna dice "no hace falta código", abrí los datos primero.** Ejecutá:

   ```python
   print(california['DESCR'])
   ```

   Eso imprime la descripción oficial del dataset (origen Pace & Barry 1997, unidades, rango del target). Citar de ahí en tu respuesta es **lo más limpio** que podés hacer.

2. **Pregunta 1** — ¿De qué se trata el dataset? Respondé:
   - Origen: censo de EE.UU. de 1990, datos agregados por block group californiano.
   - Tamaño: 20.640 observaciones, 8 atributos numéricos.
   - Tipo de problema: regresión (target continuo).

3. **Pregunta 2** — Variable objetivo:
   - Es el **valor mediano de la vivienda del block group**, en unidades de 100.000 USD.
   - Es **continua** → problema de regresión.
   - **Tiene un cap en 5.0** (las viviendas que valían más de 500k aparecen "topadas").

4. **Pregunta 3** — Atributos disponibles:
   - Mencioná los 8: `MedInc`, `HouseAge`, `AveRooms`, `AveBedrms`, `Population`, `AveOccup`, `Latitude`, `Longitude`.
   - Aclarar que son **agregados por block group**, no por vivienda individual.

5. **Pregunta 4** — Atributos más determinantes (a priori, antes de ver los datos):
   - **`MedInc`** es el candidato natural: en EE.UU., el precio de vivienda correlaciona fuertemente con el ingreso del barrio. *(En el Ej 2 lo vas a verificar visualmente.)*
   - **`Latitude` y `Longitude`** son fuertes pero no lineales (ubicaciones costeras como San Francisco / Los Ángeles valen más).
   - **`AveRooms`** podría tener efecto pero es ambiguo (más habitaciones puede significar más espacio O más densidad rural).
   - **`HouseAge`** suele tener efecto pequeño / contraintuitivo (zonas viejas pero céntricas valen más que zonas nuevas suburbanas).

6. **Pregunta 5** — Sesgos, riesgos, dilemas éticos:
   - **Sesgo temporal**: datos de 1990. Cualquier predicción se vuelve obsoleta — el mercado inmobiliario californiano cambió radicalmente en 35 años.
   - **Sesgo geográfico**: sólo California, no generaliza a otros estados / países.
   - **Cap del target en 500k**: cualquier modelo va a *subestimar* el precio de las viviendas más caras (el modelo "no sabe" que pueden valer más).
   - **Sesgos heredados del censo de 1990**: el redlining histórico (segregación residencial por raza/ingreso) influyó en qué zonas tenían qué valor inmobiliario. Predicciones basadas en estos datos pueden **perpetuar** esa segregación.
   - **Uso ético**: usar estos modelos para decisiones reales (préstamos hipotecarios, tasaciones, decisiones de inversión inmobiliaria) **sin auditoría** puede discriminar contra zonas históricamente subvaluadas.
   - **Ausencia de `B` y `MEDV` (Boston)**: California Housing reemplazó a Boston Housing precisamente porque éste último incluía una "feature" sobre proporción afroamericana. La cátedra eligió California porque es éticamente más limpio — pero **no por eso está libre de sesgos**.

### Output esperado

Texto en prosa en la celda 13. Apuntá a **150-250 palabras** en total (no es un ensayo, pero tampoco bullets sin contexto). Tono: semi-formal, en primera persona o "uno" en español.

### Trampas

- **No respondas sin haber leído `DESCR`.** Aunque la consigna diga "no hace falta código", evitate la vergüenza de inventar datos.
- **No copies y pegues `DESCR` entero**: extractá lo relevante. Citá si conviene ("según la descripción oficial del dataset…").
- **No subestimes la pregunta 5.** La cátedra ya advirtió que la diplomatura prioriza **uso transparente y ético de la IA y los datos**. Esta pregunta es donde se mide tu criterio.

### Cómo verificar que está bien

- ✅ Tu respuesta menciona origen, target (con unidades correctas), 8 features, problema de regresión, al menos 2 sesgos identificados.
- ✅ Justificás qué atributo te parece más relevante **con una razón conceptual** (no sólo "MedInc porque sí").
- ✅ La pregunta 5 tiene al menos 3 ítems diferenciados, no un único "datos viejos".

### Errores comunes

- ❌ "El target es el precio promedio de la vivienda". **No es promedio, es mediana.** Y no es del hogar, es del block group.
- ❌ "Las unidades son dólares". **Son cientos de miles de dólares.**
- ❌ Olvidarse del cap en 5.0.
- ❌ Listar features mal (`AveRooms` ≠ "habitaciones de cada casa"; es promedio del block group).
- ❌ Saltar la pregunta 5 con "no veo problemas". Siempre hay problemas — buscalos.

---

## Ejercicio 2 — Visualización de los Datos

### Consigna (cell-14, literal)

1. Para cada atributo de entrada, haga una gráfica que muestre su relación con la variable objetivo.
2. Estudie las gráficas, identificando **a ojo** los atributos que a su criterio sean los más informativos para la predicción.
3. Para ud., ¿cuáles son esos atributos? Lístelos en orden de importancia.

### Conceptos teóricos

- **EDA univariado** (un feature por vez vs target). Ver `03-regresion-lineal.md §1` para la motivación de visualizar antes de modelar.
- **Criterios visuales para evaluar "informatividad":**
  - **Linealidad visible** → el scatter forma una nube con dirección clara.
  - **Dispersión vertical chica** → al fijar X, los valores de Y están concentrados.
  - **Rango efectivo del feature** → si todos los valores están aplastados en una zona, ese feature no discrimina bien.
  - **Estructura no lineal evidente** → forma de U, J, etc. (los dos `Latitude`/`Longitude` muestran esto).

### Pasos sugeridos

1. **Resolvé la trampa DataFrame vs ndarray ANTES** (sección "TRAMPA CRÍTICA"). Si no, tu código del Ej 2 va a explotar en la primera iteración.
2. **Iterá sobre los 8 features con un `for`**. No copies y pegues 8 veces el mismo código.
3. **Usá `plt.subplots(2, 4, ...)`** para que las 8 gráficas queden en una grilla 2×4 (más compacto que 8 gráficos separados).
4. **Para cada gráfico:** scatter de feature vs y, label el eje X con el nombre del feature, label el eje Y con el target.
5. **Identificá visualmente:** cuál muestra correlación más nítida con `y`. **`MedInc` debería ganar a ojo** (forma de "nube alargada" hacia arriba a la derecha).
6. **Ranking en prosa:** justificá tu orden con criterio visual ("MedInc muestra una tendencia lineal clara; AveRooms muestra menos estructura porque…").

### Código guía (snippets, NO la solución completa)

#### Versión simple con `for` y un sólo gráfico por iteración

```python
feature_names = california['feature_names']  # lista de strings

for feature in feature_names:
    selector = (np.array(feature_names) == feature)
    plt.figure(figsize=(6, 4))
    plt.scatter(X[:, selector], y, facecolor="dodgerblue",
                edgecolor="k", alpha=0.3, s=10)
    plt.xlabel(feature)
    plt.ylabel('median house value [x 100 000 USD]')
    plt.title(f"{feature} vs target")
    plt.show()
```

> Notá el `alpha=0.3` y `s=10`: con 20.640 puntos, los scatter quedan saturados. Bajar alpha y tamaño revela densidad.

#### Versión limpia con grilla 2×4 (mejor)

```python
feature_names = california['feature_names']

fig, axes = plt.subplots(2, 4, figsize=(20, 8))
for ax, feature in zip(axes.flatten(), feature_names):
    selector = (np.array(feature_names) == feature)
    ax.scatter(X[:, selector], y, facecolor="dodgerblue",
               edgecolor="k", alpha=0.2, s=8)
    ax.set_xlabel(feature)
    ax.set_ylabel('y (x 100k USD)')
    ax.set_title(feature)
plt.tight_layout()
plt.show()
```

### Trampas técnicas

1. **DataFrame vs ndarray** → ver sección dedicada arriba. Si `X` es DataFrame, `X[:, selector]` truena.
2. **`feature_names` es una lista, no un ndarray.** Por eso el código de ayuda hace `np.array(california['feature_names']) == 'HouseAge'`. Si te olvidás del `np.array`, la comparación `'HouseAge' == lista_python` devuelve `False` (no un array booleano).
3. **El selector booleano devuelve shape `(n, 1)`, no `(n,)`.** Es decir, `X[:, selector]` da una columna 2D. Para `plt.scatter` no importa, pero **importará en Ejercicio 3** cuando se lo pases a `LinearRegression.fit()` (que de hecho **espera** shape `(n, 1)`, no `(n,)`).
4. **Outliers visuales:** el cap en `y=5.0` aparece como una raya horizontal en todos los scatters. NO es un bug, es el cap del dataset. Mencionalo cuando interpretes.
5. **`AveOccup` y `Population` tienen colas larguísimas.** Hay block groups con `AveOccup` ~ 1000 (probablemente militares, prisiones, hoteles). El scatter queda dominado por outliers. Considerá log-transform o filtrar visualización, pero **NO transformes los datos reales** — es sólo para visualizar.

### Cómo verificar que está bien

- ✅ Generaste **los 8 gráficos** (uno por feature).
- ✅ Identificaste a `MedInc` como el de mejor correlación visible (debería ser obvio: forma de nube con pendiente positiva clara).
- ✅ Notaste el cap en `y=5`.
- ✅ Tu ranking tiene criterio (no "MedInc, Latitude, Longitude" sin justificar).
- ✅ Las 8 figuras se ven en el notebook (no quedaron como referencias rotas).

### Errores comunes

- ❌ **Olvidarse de `np.array(...)` en la comparación con el selector** → da `True`/`False` plain, no funciona como índice booleano.
- ❌ **`alpha=1.0`** → los 20.640 puntos quedan apilados en una mancha azul opaca. No se ve nada.
- ❌ Hacer scatter de cada feature **vs el índice de la fila**, no vs el target. Ojo con el orden de argumentos en `plt.scatter(x, y)`.
- ❌ **Decir "todos los atributos parecen importantes"** sin justificar. Si todos te parecen iguales, mirá más atento — `MedInc` sobresale, `AveBedrms` es bastante plano, `Population` no muestra estructura.
- ❌ **Listar los 8 features en orden de importancia subjetivo sin haberlos visualizado**.

### Mi ranking sugerido (espero al final del ejercicio)

> *No es la "respuesta correcta" — vos justificás el tuyo. Pero esta es una respuesta razonable para contrastar.*

| Ranking | Feature | Por qué |
|---------|---------|---------|
| 1 | `MedInc` | Pendiente positiva clara, nube alargada. **El predictor estrella.** |
| 2 | `Latitude` | Estructura no lineal (precios altos en zonas costeras al sur y al centro). |
| 3 | `Longitude` | Idem, complementario con `Latitude`. |
| 4 | `HouseAge` | Tendencia leve, no muy fuerte. |
| 5 | `AveRooms` | Algo de correlación pero ensuciada por outliers. |
| 6 | `AveOccup` | Outliers dominan, señal débil. |
| 7 | `AveBedrms` | Casi plano. |
| 8 | `Population` | Sin estructura visible. |

---

## Ejercicio 3 — Regresión Lineal

### Consigna (cell-19, literal)

1. Seleccione **un solo atributo** que considere puede ser el más apropiado.
2. Instancie una regresión lineal de **scikit-learn**, y entrénela usando sólo el atributo seleccionado.
3. Evalúe, calculando error cuadrático medio para los conjuntos de entrenamiento y evaluación.
4. Grafique el modelo resultante, junto con los puntos de entrenamiento y evaluación.
5. Interprete el resultado, haciendo algún comentario sobre las cualidades del modelo obtenido.

> **Observación:** Con algunos atributos se puede obtener un error en test menor a 50.

### Conceptos teóricos

- **Regresión lineal univariada:** modelo $\hat{y} = w_0 + w_1 x$. Ver `03-regresion-lineal.md §3`.
- **MSE (error cuadrático medio):** $\frac{1}{N}\sum_{i=1}^{N}(\hat{y}_i - y_i)^2$. Ver `05-funcion-de-costo-y-mse.md §1-§2`.
- **Train/test split:** ya viene resuelto. Conceptualmente importa porque el MSE en train ↓ no garantiza buen MSE en test. Ver `06-overfitting-underfitting-capacidad.md §2`.
- **Underfitting:** una sola feature lineal es casi siempre **un modelo simple** → es probable que muestre underfitting (alto error en train Y test). Eso es **información**, no fracaso.

### Pasos sugeridos

1. **Decidí qué feature usar.** Basado en el Ej 2: `MedInc` es el candidato natural.
2. **Extraé la columna correspondiente** de `X_train` y `X_test`. La celda 20 te da el patrón (`selector` booleano).
3. **Verificá shape**: `X_train_f.shape` debe ser `(16512, 1)` (no `(16512,)`).
4. **Instanciá `LinearRegression()`** — sin parámetros, los defaults están bien.
5. **`.fit(X_train_f, y_train)`** sobre el conjunto de entrenamiento.
6. **`.predict(...)`** en train y test, **luego** `mean_squared_error(y_real, y_pred)` en cada uno.
7. **Imprimí ambos errores**, en train y test.
8. **Graficá** la línea predicha sobre la grilla `x` ya provista (cell-24), más los scatters de train (color sólido) y test (color hueco).
9. **Interpretá**: ¿qué dicen los números? ¿train y test son parecidos? ¿el modelo capturó la tendencia o se quedó corto?

### Código guía (snippets)

#### Selector y extracción

```python
feature = 'MedInc'  # tu elección — justificala
selector = (np.array(california['feature_names']) == feature)

X_train_f = X_train[:, selector]   # OJO: trampa DataFrame
X_test_f  = X_test[:, selector]
print(X_train_f.shape, X_test_f.shape)
# Esperado: (16512, 1) (4128, 1)
```

#### Entrenamiento

```python
from sklearn.linear_model import LinearRegression

model = LinearRegression()
model.fit(X_train_f, y_train)

# Coeficientes aprendidos
print("w_0 (intercept):", model.intercept_)
print("w_1 (slope):    ", model.coef_)
```

> Notá: para `MedInc`, esperás `w_1` positivo (más ingreso → más precio). Si te dio negativo, hay un bug.

#### Predicción y evaluación

```python
from sklearn.metrics import mean_squared_error

y_pred_train = model.predict(X_train_f)
y_pred_test  = model.predict(X_test_f)

mse_train = mean_squared_error(y_train, y_pred_train)
mse_test  = mean_squared_error(y_test,  y_pred_test)

print(f"MSE train: {mse_train:.4f}")
print(f"MSE test:  {mse_test:.4f}")
```

> **Atención** — el target está en unidades de 100k USD, así que `y` ronda 0–5. Un MSE en torno a **0.7** corresponde a ~RMSE 0.84 que en USD reales es ~84.000. NO confundir con "MSE 50" del enunciado (ver sección "Sobre el número 50" abajo).

#### Gráfico

```python
x_start = min(np.min(X_train_f), np.min(X_test_f))
x_end   = max(np.max(X_train_f), np.max(X_test_f))
x_grid  = np.linspace(x_start, x_end, 200).reshape(-1, 1)

plt.figure(figsize=(8, 6))
plt.plot(x_grid, model.predict(x_grid), color="tomato", lw=2, label="modelo")
plt.scatter(X_train_f, y_train, facecolor="dodgerblue", edgecolor="k", alpha=0.2, s=10, label="train")
plt.scatter(X_test_f,  y_test,  facecolor="white",      edgecolor="k", alpha=0.4, s=10, label="test")
plt.title(f"Regresión lineal — {feature}")
plt.xlabel(feature)
plt.ylabel('median house value [x 100 000 USD]')
plt.legend()
plt.show()
```

### Sobre el número 50 (¡ojo!)

El enunciado dice: *"Con algunos atributos se puede obtener un error en test menor a 50"*. **Esta cifra es ambigua y confunde a casi todos.**

Hay **dos interpretaciones posibles**:

- **Interpretación A (improbable):** MSE en las unidades del target tal cual están (100k USD)². Un MSE = 50 en esas unidades sería un RMSE ≈ 7.07, es decir 707.000 USD. **Eso es muchísimo, no es buen modelo.**
- **Interpretación B (la creemos correcta):** El enunciado piensa el target en **decenas de miles** (es decir, multiplicando `y` por 10), o usa una métrica histórica que viene del Boston Housing original. En esas escalas, MSE < 50 es razonable.

**¿Qué te conviene hacer?** Reportá el MSE en las unidades que sklearn te devuelve directamente (`mean_squared_error(y_test, y_pred_test)`) y **al lado** poné el equivalente en USD reales:

```python
print(f"MSE test = {mse_test:.4f} (en unidades de y, target en 100k USD)")
print(f"RMSE test = {np.sqrt(mse_test):.4f} → {np.sqrt(mse_test)*100_000:.0f} USD")
```

> **Tu MSE con `MedInc` debería estar en el rango ~0.7** (target en 100k USD). Si lo escalás a "miles de USD" mentalmente (multiplicando `y` por 100 y volviendo a calcular MSE), te queda ~7000. Si lo escalás a "decenas de miles" (`y * 10`), te queda MSE ~70. **Ninguno es exactamente 50** — pero todos están en el orden correcto. El enunciado pide *menor a 50* sólo como referencia laxa.

> **TL;DR sobre el número 50:** No te frustres si tu MSE no es "literalmente menor a 50". El enunciado es ambiguo en unidades. Lo importante es que tus errores **bajan al elegir mejor feature** y **bajan más con polinomio** (Ej 4) y **bajan aún más con multivariado** (Ej 5).

### Trampas técnicas

1. **`X[:, selector]` con `X` DataFrame** → ver "TRAMPA CRÍTICA".
2. **Shape `(n,)` vs `(n,1)`** → `LinearRegression.fit()` quiere `X` 2D. Si tu selector te dio 1D, usá `.reshape(-1, 1)`.
3. **`model.coef_` es un array, no un scalar** → si imprimís, te aparece `[0.4173]`, no `0.4173`. Para extraer el número: `model.coef_[0]`.
4. **No uses `random_state` distinto del 0** en el split — eso lo fija el enunciado.
5. **No pongas `model.fit(X_train, y_train)` con `X_train` completo** (las 8 features). El ejercicio pide **una sola feature**. Si pasás las 8, sklearn no se queja, pero el modelo deja de ser "regresión univariada".

### Cómo verificar que está bien

- ✅ `X_train_f.shape == (16512, 1)` y `X_test_f.shape == (4128, 1)`.
- ✅ `model.coef_` tiene signo coherente con el feature elegido (positivo para `MedInc`, etc.).
- ✅ MSE train y test son **similares en magnitud** — si son muy distintos, algo raro pasa (en lineal univariado no hay overfitting, tienen que parecerse).
- ✅ El gráfico muestra la línea roja **cortando la nube de puntos en diagonal**, no horizontal y no vertical.
- ✅ Tu respuesta del punto 5 menciona **underfitting** (es lo esperado para una recta sobre una nube ruidosa).

### Errores comunes

- ❌ **Elegir `HouseAge` (porque es el ejemplo)**. El ejemplo está en `HouseAge` sólo para ilustrar; **vos tenés que elegir el que justificaste en el Ej 2**, que casi seguro es `MedInc`.
- ❌ **Olvidarse de imprimir MSE en train Y test** (sólo imprimen uno).
- ❌ **Graficar la línea sobre los datos test pero no entrenar con train**. El modelo se entrena con train y se evalúa en ambos.
- ❌ **`plt.plot(X_train_f, model.predict(X_train_f))`** → si `X_train_f` no está ordenado, te dibuja una línea zigzagueante (matplotlib une los puntos en el orden del array). Usá `x_grid` ordenado (la celda 24 ya te lo da).
- ❌ **Interpretar el resultado en una sola línea**: "el MSE es bajo, el modelo anda". No. ¿Qué significa "bajo"? ¿Comparado con qué? Mencioná: rango del target, cap en 5.0, varianza del target (`y.var()` ≈ 1.33 — un modelo que predice siempre la media tendría MSE ≈ 1.33; **tu modelo debe ser claramente mejor que eso**).

### Cualidades del modelo (para tu respuesta del punto 5)

Sugerencia de párrafo:

> *"El MSE en train y test son similares (≈ 0.70 y ≈ 0.69 respectivamente con `MedInc`), lo que indica que el modelo generaliza, pero el error absoluto sigue siendo alto: RMSE ≈ 0.84 implica un error típico de unos 84.000 USD por vivienda. Esto es esperable: una recta no puede capturar el cap en `y = 5.0` ni la dispersión vertical creciente para valores altos de MedInc. Hay underfitting: el modelo es demasiado simple para la complejidad del fenómeno."*

---

## Ejercicio 4 — Regresión Polinomial

### Consigna (cell-26, literal)

> En este ejercicio deben entrenar regresiones polinomiales de diferente complejidad, siempre usando **scikit-learn**. Deben usar **el mismo atributo** seleccionado para el ejercicio anterior.

1. Para varios grados de polinomio, haga lo siguiente:
   1. Instancie y entrene una regresión polinomial.
   2. Prediga y calcule error en entrenamiento y evaluación. Imprima los valores.
   3. Guarde los errores en una lista.
2. Grafique las curvas de error en términos del grado del polinomio.
3. Interprete la curva, identificando el punto en que comienza a haber sobreajuste, si lo hay.
4. Seleccione el modelo que mejor funcione, y grafique el modelo conjuntamente con los puntos.
5. Interprete el resultado, haciendo algún comentario sobre las cualidades del modelo obtenido.

> **Observación:** Con algunos atributos se pueden obtener errores en test menores a 40 e incluso a 35.

### Conceptos teóricos

- **Regresión polinomial:** $\hat{y} = w_0 + w_1 x + w_2 x^2 + \dots + w_M x^M$. Ver `04-regresion-polinomial.md §1-§2`.
- **Capacidad del modelo:** controlada por el grado $M$. Ver `06-overfitting-underfitting-capacidad.md §1`.
- **Bias-variance tradeoff:** modelos simples → alto bias (underfitting); modelos complejos → alta varianza (overfitting). Ver `06-overfitting-underfitting-capacidad.md §3`.
- **Curva de error vs complejidad:** train baja monótonamente, test forma una "U" — el mínimo de test es donde está el modelo óptimo. Ver `06-overfitting-underfitting-capacidad.md §3`, tabla numérica de la clase 1 (Bishop §3).
- **`PolynomialFeatures` de sklearn:** expande $x$ en $[1, x, x^2, \dots, x^M]$ → la regresión polinomial **es regresión lineal en el espacio expandido**. Ver `03-regresion-lineal.md §6` o `04-regresion-polinomial.md §3`.

### Pasos sugeridos

1. **Decidí el rango de grados a probar.** **El enunciado NO lo especifica** (ambiguo). Recomendación: `1..15` o `1..20`. Empezás en 1 (que es la regresión lineal del Ej 3 — tiene que dar el mismo error) y subís hasta que **veas claramente** la curva de overfitting.

2. **Usá un Pipeline.** No hagas la expansión polinomial a mano. La sintaxis moderna:

   ```python
   from sklearn.preprocessing import PolynomialFeatures
   from sklearn.linear_model import LinearRegression
   from sklearn.pipeline import make_pipeline

   model = make_pipeline(
       PolynomialFeatures(degree=d, include_bias=False),
       LinearRegression()
   )
   ```

3. **`include_bias=False` + `LinearRegression()` (con `fit_intercept=True` por default)**, NO `include_bias=True` + `fit_intercept=False`. **Las dos formas son equivalentes matemáticamente, pero la primera es más limpia** (queda más claro qué es el bias). El notebook 01 de la clase 1 usa `include_bias=True` + `fit_intercept=False`; aceptable también, pero menos pythonico.

4. **Bucle sobre grados:**

   ```python
   degrees = list(range(1, 16))   # 1..15
   results = []   # va a guardar (grado, mse_train, mse_test)

   for d in degrees:
       model = make_pipeline(
           PolynomialFeatures(degree=d, include_bias=False),
           LinearRegression()
       )
       model.fit(X_train_f, y_train)

       mse_train = mean_squared_error(y_train, model.predict(X_train_f))
       mse_test  = mean_squared_error(y_test,  model.predict(X_test_f))

       print(f"d={d:2d}  MSE train={mse_train:.4f}  MSE test={mse_test:.4f}")
       results.append((d, mse_train, mse_test))
   ```

5. **Gráfico de curvas de error vs grado:**

   ```python
   results = np.array(results)
   plt.plot(results[:, 0], results[:, 1], 'o-', label='MSE train')
   plt.plot(results[:, 0], results[:, 2], 's-', label='MSE test')
   plt.xlabel('grado del polinomio M')
   plt.ylabel('MSE')
   plt.title(f'Error vs grado — feature: {feature}')
   plt.legend()
   plt.show()
   ```

   **Tip:** poné el eje Y en log si los errores explotan en grados altos (`plt.yscale('log')`).

6. **Identificá el "codo":** el grado donde **el error de test es mínimo**. Es tu mejor modelo. Para `MedInc` típicamente ronda **M=3 a M=5**, pero depende de la feature elegida.

7. **Re-entrená el mejor modelo y graficálo** sobre los datos (igual que en el Ej 3 pero con la curva polinomial).

8. **Interpretá:**
   - ¿Hay overfitting visible (test sube luego del codo)?
   - ¿Hasta qué grado mejora razonablemente?
   - ¿Lograste bajar el error respecto al Ej 3? (debería sí — el Ej 3 era $M=1$, y $M=3$ debería estar mejor).

### Código guía completo (estructura, no la solución)

```python
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Asumiendo feature = 'MedInc' y X_train_f/X_test_f del Ej 3
degrees = list(range(1, 16))
mse_train_list = []
mse_test_list = []

for d in degrees:
    model = make_pipeline(
        PolynomialFeatures(degree=d, include_bias=False),
        LinearRegression()
    )
    model.fit(X_train_f, y_train)

    mse_train_list.append(mean_squared_error(y_train, model.predict(X_train_f)))
    mse_test_list.append(mean_squared_error(y_test, model.predict(X_test_f)))

    print(f"d={d:2d}  train={mse_train_list[-1]:.4f}  test={mse_test_list[-1]:.4f}")

# Curva de errores
plt.plot(degrees, mse_train_list, 'o-', label='train')
plt.plot(degrees, mse_test_list, 's-', label='test')
plt.xlabel('grado M'); plt.ylabel('MSE')
plt.legend(); plt.title('Error vs complejidad')
plt.show()

# Mejor modelo (mínimo de test)
best_d = degrees[np.argmin(mse_test_list)]
print(f"Mejor grado: {best_d}")
```

### Sobre los números 40 y 35 del enunciado

Misma ambigüedad de unidades que en el Ej 3. La cátedra dice "errores en test menores a 40 e incluso a 35" — el patrón es **claramente decreciente**:
- Ej 3 → < 50
- Ej 4 (polinomial univariada) → < 40
- Ej 5 (polinomial multivariada) → < 35

Tu objetivo es **mostrar la misma tendencia** (cada ejercicio mejora respecto al anterior), aunque tu escala numérica no coincida exactamente. Si tus errores van de **0.72 → 0.51 → 0.34** (en unidades de target × 100k), estás siguiendo la dirección correcta.

### Trampas técnicas

1. **Sin escalar, grados altos explotan.** Si elegís `MedInc` (rango ~0.5 a 15) y subís a M=15, entonces $x^{15}$ ronda $15^{15} \approx 4 \times 10^{17}$. Los coeficientes resultantes pueden ser absurdamente grandes y numéricamente inestables. **El TP no pide escalar**, pero si querés grados altos limpios, sumá `StandardScaler` al pipeline:

   ```python
   from sklearn.preprocessing import StandardScaler
   model = make_pipeline(
       StandardScaler(),
       PolynomialFeatures(degree=d, include_bias=False),
       LinearRegression()
   )
   ```

   Esto te da estabilidad numérica sin cambiar la naturaleza del modelo. **Mencionalo en la interpretación si lo hiciste.**

2. **`PolynomialFeatures(degree=0)`** te tira un solo feature constante. La regresión queda como "predecir siempre la media" (intercept solo). Suele dar MSE = `y_train.var()`. NO empezar en 0 a menos que quieras ese baseline; empezá en 1.

3. **Curva del Ej 4 vs ejemplo de la clase.** El ejemplo canónico de la clase 1 (sinusoidal sintética, Bishop §3) tiene **datos limpios** y la curva de test forma una U perfecta. **California Housing es ruidoso**, así que tu curva puede ser menos prolija — la mejora con polinomial es real pero no tan dramática.

4. **Overfitting "ruidoso" vs "real".** Si la curva de test es errática en grados altos (sube, baja, sube), es por **inestabilidad numérica** (coeficientes grandes), no por overfitting "puro". Escalá las features y la curva queda más limpia.

5. **`np.argmin` te da el índice, no el grado.** Si `degrees = range(1, 16)`, el argmin es un índice `i` y el grado es `degrees[i]`. Cuidado con confundirlos.

### Cómo verificar que está bien

- ✅ Tu lista incluye al menos **5 grados distintos**, idealmente 10+.
- ✅ La curva muestra:
  - Train decreciente (al subir M, MSE train baja monótonamente o casi).
  - Test con forma de U (baja, mínimo, sube) — **eso es overfitting visible**.
  - Si la U no aparece, probaste pocos grados o tu feature es muy "lineal" (probá subir hasta M=20).
- ✅ Identificás el mejor grado y su MSE en test.
- ✅ El mejor modelo (gráfico final) **muestra una curva**, no una recta. Si te quedó casi recto, M es demasiado bajo.
- ✅ Tu interpretación menciona explícitamente: overfitting, capacidad, bias-variance.

### Errores comunes

- ❌ **Olvidar `include_bias=False` con `fit_intercept=True`** → te quedan dos términos constantes (la columna de 1 que mete `PolynomialFeatures` y el intercept de `LinearRegression`). El modelo igual converge porque `LinearRegression` resuelve por SVD/pinv, pero tenés un grado de libertad redundante.
- ❌ **No fijar `random_state`** en train_test_split → tus errores no son reproducibles (esto está fijo en cell-9, no lo toques).
- ❌ **Sacar `mean_squared_error` con `squared=False`** en sklearn nuevo → da error o warning. Si querés RMSE, usá `root_mean_squared_error` (sklearn ≥ 1.4) o `np.sqrt(mse)`.
- ❌ **Confundir M (grado) con N (cantidad de datos)**. La clase 1 muestra que aumentar N "rescata" un M alto del overfitting (tabla N=20 vs N=100 del PDF p.22). Acá N está fijo (16.512), así que sólo controlás M.
- ❌ **Interpretar "el menor MSE en train es el mejor modelo"**. NO. **El mejor es el de menor MSE en TEST** — ese es el criterio.
- ❌ **Pasar `X` 2D a `PolynomialFeatures` sin shape correcta** → si `X_train_f.shape == (16512,)` (1D), tirá `.reshape(-1, 1)` antes.

### Selección del mejor modelo y gráfico

```python
best_d = degrees[np.argmin(mse_test_list)]
print(f"Mejor grado: M = {best_d}, MSE test = {min(mse_test_list):.4f}")

best_model = make_pipeline(
    PolynomialFeatures(degree=best_d, include_bias=False),
    LinearRegression()
)
best_model.fit(X_train_f, y_train)

x_start = min(np.min(X_train_f), np.min(X_test_f))
x_end   = max(np.max(X_train_f), np.max(X_test_f))
x_grid  = np.linspace(x_start, x_end, 500).reshape(-1, 1)

plt.figure(figsize=(8, 6))
plt.plot(x_grid, best_model.predict(x_grid), color="tomato", lw=2, label=f"polinomial M={best_d}")
plt.scatter(X_train_f, y_train, facecolor="dodgerblue", edgecolor="k", alpha=0.2, s=10, label="train")
plt.scatter(X_test_f,  y_test,  facecolor="white",      edgecolor="k", alpha=0.4, s=10, label="test")
plt.title(f"Mejor modelo polinomial — {feature}")
plt.xlabel(feature); plt.ylabel('median house value [x 100 000 USD]')
plt.legend()
plt.show()
```

---

## Ejercicio 5 — Regresión con más de un Atributo

### Consigna (cell-32, literal)

> En este ejercicio deben entrenar regresiones que toman más de un atributo de entrada.

1. Seleccione **dos o tres atributos** entre los más relevantes encontrados en el ejercicio 2.
2. Repita el ejercicio anterior, pero usando los atributos seleccionados. No hace falta graficar el modelo final.
3. Interprete el resultado y compare con los ejercicios anteriores. ¿Se obtuvieron mejores modelos? ¿Porqué?

### Conceptos teóricos

- **Regresión polinomial multivariada:** `PolynomialFeatures(degree=d)` con $k$ features de entrada genera $\binom{k+d}{d}$ features (incluyendo el bias). Con $k=3$ y $d=4$: $\binom{7}{4} = 35$ features. Con $k=3$ y $d=10$: $\binom{13}{10} = 286$ features. **Crece rápido**, especialmente en grados altos.
- **Combinaciones e interacciones:** además de $x_1^d, x_2^d, x_3^d$, aparecen términos cruzados $x_1 x_2, x_1^2 x_2$, etc. Estos modelan **interacciones** entre features (un feature modula el efecto del otro).
- **Curse of dimensionality:** más features expandidas → más coeficientes a aprender → necesitás más datos para no sobreajustar. Con N=16.512 todavía estás cómodo en grados moderados.

### Pasos sugeridos

1. **Elegí 2 o 3 features.** Basado en tu ranking del Ej 2:
   - **Opción A** (la natural): `MedInc` + `Latitude` + `Longitude` (los tres top del ranking sugerido).
   - **Opción B** (más simple): `MedInc` + `AveRooms` (dos features).
   - Lo importante: **justificar** por qué esos y no otros.

2. **Selector booleano para múltiples features.** El notebook ya da el patrón (cell-33):

   ```python
   selector = (np.array(california['feature_names']) == 'MedInc') | \
              (np.array(california['feature_names']) == 'Latitude') | \
              (np.array(california['feature_names']) == 'Longitude')
   ```

   **Versión más limpia con `np.isin`:**

   ```python
   selector = np.isin(california['feature_names'], ['MedInc', 'Latitude', 'Longitude'])
   ```

   Ambas son equivalentes; usá la que te parezca más legible.

3. **Repetí el loop del Ej 4** con las features seleccionadas. Mismo código, sólo cambia `X_train_fs` (con `s` de "subset" o "varias features").

4. **Cuidado con el rango de grados.** Con 3 features:
   - $M=4$ → 35 features expandidas — manejable.
   - $M=6$ → 84 features.
   - $M=10$ → 286 features.
   - $M=15$ → 816 features — empieza a pesar.

   Sugerencia: probá `1..8` o `1..10` y mirá cuándo empieza a tardar.

5. **No graficás el modelo final** (lo dice el enunciado): graficar un modelo de 3 inputs requeriría un espacio 4D. Sólo graficás la curva train/test vs grado.

6. **Comparación con Ej 3 y Ej 4:** tu MSE test debería **bajar** respecto a los anteriores. Si subió, hay algo mal. Justificá:
   - **Más features = más información** → si están bien elegidas, mejora.
   - **Pero más features expandidas = más capacidad** → riesgo de overfitting más rápido (con menor M).

### Código guía (estructura)

```python
selector = np.isin(california['feature_names'], ['MedInc', 'Latitude', 'Longitude'])

X_train_fs = X_train[:, selector]    # OJO: trampa DataFrame
X_test_fs  = X_test[:, selector]
print(X_train_fs.shape, X_test_fs.shape)
# Esperado: (16512, 3) (4128, 3)

degrees = list(range(1, 9))   # rango más conservador por la explosión combinatoria
mse_train_multi = []
mse_test_multi = []

for d in degrees:
    model = make_pipeline(
        StandardScaler(),     # ⚡ MUY recomendado con multivariado
        PolynomialFeatures(degree=d, include_bias=False),
        LinearRegression()
    )
    model.fit(X_train_fs, y_train)
    mse_train_multi.append(mean_squared_error(y_train, model.predict(X_train_fs)))
    mse_test_multi.append(mean_squared_error(y_test, model.predict(X_test_fs)))
    print(f"d={d}  train={mse_train_multi[-1]:.4f}  test={mse_test_multi[-1]:.4f}")

# Curvas
plt.plot(degrees, mse_train_multi, 'o-', label='train')
plt.plot(degrees, mse_test_multi, 's-', label='test')
plt.xlabel('grado M'); plt.ylabel('MSE')
plt.legend(); plt.title('Multivariado — Error vs grado')
plt.show()
```

### Trampas técnicas

1. **Explosión combinatoria.** Con $k=3$ features y $d=15$ son **816 features expandidas**. El fit tarda. Empezá con grados bajos.
2. **DataFrame vs ndarray** (otra vez) → cell-33 usa el mismo patrón problemático.
3. **`StandardScaler` recomendado.** Con `MedInc` (rango ~0-15), `Latitude` (rango 32-42), `Longitude` (rango -125 a -114), las escalas son **muy distintas**. Sin escalar, `Longitude^4 ≈ 10^8` y `MedInc^4 ≈ 10^4` — el modelo se enloquece con los pesos. **Escalá.**
4. **`PolynomialFeatures` mezcla cuadrados e interacciones.** Si querés sólo interacciones (sin $x_i^2$ puros), usá `interaction_only=True`. **El TP no lo especifica**, así que dejá el default (`False`).
5. **Comparación de errores entre Ej 3, 4 y 5.** Necesitás los 3 MSE de test para compararlos. **Guardalos en variables claras** (`mse_test_ej3`, `mse_test_ej4_best`, `mse_test_ej5_best`).

### Cómo verificar que está bien

- ✅ `X_train_fs.shape == (16512, k)` donde k es el número de features elegidas (2 o 3).
- ✅ El MSE test en el mejor grado es **menor** que el mejor MSE del Ej 4.
- ✅ Tu curva muestra train decreciente y test con U (o al menos decreciente y luego estancada).
- ✅ Tu interpretación menciona:
  - Mejora vs Ej 3 (lineal univariado) y Ej 4 (polinomial univariado).
  - Por qué mejora (más información de features relevantes).
  - Por qué overfitting puede aparecer antes (más capacidad por feature expandida).

### Errores comunes

- ❌ **Elegir 2 features cualquiera** (ej. `Population` + `AveBedrms`, los peores del ranking) y después quejarse de que no mejora. **Si elegís mal, el resultado del Ej 5 puede ser peor que el Ej 4 con `MedInc` solo.**
- ❌ **No usar `StandardScaler` con features de escalas dispares** → coeficientes basura, MSE inestable.
- ❌ **Probar grados muy altos sin paciencia** → el kernel de Jupyter se cuelga. Empezá conservador.
- ❌ **No reportar tabla comparativa**. Hacé una mini-tabla en la respuesta del punto 3:

  ```
  Ej 3 (lineal, MedInc):              MSE test ≈ 0.71
  Ej 4 (poly M=4, MedInc):            MSE test ≈ 0.51
  Ej 5 (poly M=3, MedInc+Lat+Long):   MSE test ≈ 0.36
  ```

### ¿Mejoró? ¿Por qué? (sugerencia de respuesta)

> *"Sí, el MSE en test bajó significativamente respecto a los ejercicios anteriores. La mejora del Ej 3 al Ej 4 captura la no-linealidad de `MedInc` con el target (relación curva, no estrictamente lineal). La mejora del Ej 4 al Ej 5 viene de **agregar información geográfica** (`Latitude`/`Longitude`): hay un componente espacial fuerte en el precio que `MedInc` por sí solo no captura — barrios con ingresos similares pueden tener precios muy distintos según su ubicación costera o interior. Como contrapartida, el overfitting empieza a aparecer en grados más bajos (M ≈ 4-5 vs M ≈ 6-7 en el univariado) porque cada feature adicional multiplica la cantidad de coeficientes a estimar."*

---

## Ejercicio 6 (opcional) — A Todo Feature

### Consigna (cell-36, literal)

> Entrene y evalúe regresiones pero utilizando todos los atributos de entrada (va a andar mucho más lento). Estudie los resultados.

### Conceptos teóricos

- **Regresión múltiple completa** con todas las features → modelo "máxima información disponible".
- **Performance vs interpretabilidad:** más features ≠ siempre mejor. Algunas features (`Population`, `AveBedrms`) tenían bajo poder predictivo en el Ej 2.
- **Curse of dimensionality con polinomial:** con $k=8$ y $d=3$, hay $\binom{11}{3} = 165$ features expandidas. Con $d=5$, $\binom{13}{5} = 1287$. **Pesado pero hacible.**

### Pasos sugeridos

1. **Usá `X_train` y `X_test` completos** (sin selector). Acordate que pueden ser DataFrame — si lo son, conviene `X_train.values` para que el resto del pipeline sea predecible.
2. **Empezá con regresión lineal multivariada** (degree=1). Eso es el "baseline" — qué tan bien anda combinando linealmente las 8 features.
3. **Subí a polinomial**, pero con grados conservadores (`degree=2`, máximo `degree=3`). Más allá es lento y propenso a overfitting masivo.
4. **Escalá obligatoriamente.** Sin `StandardScaler`, las features no comparables (`Population` ~ 1000 vs `Longitude` ~ -120) producen polinomios numéricamente caóticos.

### Código guía

```python
# Lineal multivariada (degree=1, todas las features)
model_full = make_pipeline(
    StandardScaler(),
    LinearRegression()
)
model_full.fit(X_train, y_train)
mse_train_full = mean_squared_error(y_train, model_full.predict(X_train))
mse_test_full  = mean_squared_error(y_test,  model_full.predict(X_test))
print(f"Lineal 8-features: train={mse_train_full:.4f}  test={mse_test_full:.4f}")

# Polinomial multivariada (degree=2 a 3)
for d in [1, 2, 3]:
    model = make_pipeline(
        StandardScaler(),
        PolynomialFeatures(degree=d, include_bias=False),
        LinearRegression()
    )
    model.fit(X_train, y_train)
    mse_test = mean_squared_error(y_test, model.predict(X_test))
    print(f"d={d}  features={d*8 if d==1 else 'múltiples'}  MSE test={mse_test:.4f}")
```

### Trampas técnicas

1. **`degree=4` con 8 features = 495 features expandidas.** Lento, alto riesgo de overfitting. Si tu compu sufre, quedate en `degree=2` o `degree=3`.
2. **Tiempo de ejecución:** una regresión lineal sobre 16.512 × 495 features puede tardar varios segundos. **No es un bug** — es la realidad de la complejidad combinatoria.
3. **Si el RAM peta:** reducí degree o (mejor) usá `Ridge` (Ej 7), que es más estable.
4. **`X` como DataFrame entero**: a sklearn no le molesta, pero `model.predict(X.values)` puede ser más predecible si tenés problemas raros.

### Cómo verificar que está bien

- ✅ Tu MSE test con todas las features y `degree=1` (lineal multivariada) **es mejor que** el del Ej 3 (lineal univariada). Esperable: estás usando 8 features en vez de 1.
- ✅ `degree=2` o `3` puede mejorar respecto a `degree=1`, pero el efecto es menor (las features ya estaban casi explotadas en información).
- ✅ Si entrás a overfitting masivo (`MSE train ≈ 0.1`, `MSE test ≈ 0.5`), eso **es un hallazgo**, no un fracaso. Mostralo y discutilo.

### Errores comunes

- ❌ **No escalar** → resultados numéricamente caóticos, coeficientes absurdos.
- ❌ **Subir a `degree=10`** sin pensar → te quedás esperando 30 minutos y la memoria explota.
- ❌ **No comparar con Ej 5** → ¿realmente "todo feature" es mejor que "3 features bien elegidas"? **Depende:** con muchos datos sí, con pocos no. Esa discusión es lo que la consigna quiere ver.

---

## Ejercicio 7 (opcional) — Regularización Ridge

### Consigna (cell-36, literal)

> Entrene y evalúe regresiones con regularización "ridge". Deberá probar distintos valores de "alpha" (fuerza de la regularización). ¿Mejoran los resultados?

### Conceptos teóricos

- **Ridge regression (L2):** función de costo penalizada $\tilde{E}(\mathbf{w}) = E(\mathbf{w}) + \frac{\lambda}{2}\|\mathbf{w}\|^2$. Penaliza coeficientes grandes. Ver `07-regularizacion-ridge.md §1-§2`.
- **¿Por qué Ridge "rescata" overfitting?** El sobreajuste en regresión polinomial se manifiesta en **coeficientes enormes** (ver clase 1 PDF p.23, tabla $w^*$ con M=9: coeficientes en miles). Ridge los penaliza, los achica → coeficientes razonables → modelo no memoriza el ruido. Ver `07-regularizacion-ridge.md §3`.
- **Solución cerrada:** $\mathbf{w}^* = (\mathbf{Z}^T \mathbf{Z} + \lambda \mathbf{I})^{-1} \mathbf{Z}^T \mathbf{y}$. La matriz a invertir siempre es invertible para $\lambda > 0$ (más estable numéricamente).
- **Convención `alpha` (sklearn) vs `lambda` (teoría).** ⚠️ **Importante:** en la teoría usamos $\lambda$; sklearn usa `alpha`. **Son la misma cosa.** `alpha` no es el $\alpha$ de Lidstone/Laplace de naive bayes. Tampoco es el "tipo I error". En `Ridge`, `alpha = lambda` literal. Ver [docs Ridge](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Ridge.html).

### Pasos sugeridos

1. **Tomá la mejor configuración del Ej 5 o Ej 6** como base. El punto es ver si la regularización **mejora** sobre el mejor modelo no regularizado.
2. **Probá varios `alpha` en escala logarítmica.** El espacio típico:
   ```python
   alphas = np.logspace(-4, 4, 9)   # [1e-4, 1e-3, ..., 1e3, 1e4]
   ```
3. **Para cada `alpha`:** entrená Ridge + Polinomial, medí MSE train y test.
4. **Gráfico:** `alpha` (escala log) vs MSE train/test.
5. **Identificá el mejor `alpha`** y compará con el Ej 5/6 sin regularizar.

### Código guía

```python
from sklearn.linear_model import Ridge

# Asumo Ej 5: 3 features, mejor grado del Ej 5 fue (por ejemplo) M=4
best_d_ej5 = 4   # ajustá según tu Ej 5
alphas = np.logspace(-4, 4, 9)
ridge_mse_train = []
ridge_mse_test = []

for alpha in alphas:
    model = make_pipeline(
        StandardScaler(),
        PolynomialFeatures(degree=best_d_ej5, include_bias=False),
        Ridge(alpha=alpha)
    )
    model.fit(X_train_fs, y_train)
    ridge_mse_train.append(mean_squared_error(y_train, model.predict(X_train_fs)))
    ridge_mse_test.append(mean_squared_error(y_test, model.predict(X_test_fs)))
    print(f"alpha={alpha:.4f}  train={ridge_mse_train[-1]:.4f}  test={ridge_mse_test[-1]:.4f}")

# Gráfico
plt.semilogx(alphas, ridge_mse_train, 'o-', label='train')
plt.semilogx(alphas, ridge_mse_test,  's-', label='test')
plt.xlabel('alpha (log)'); plt.ylabel('MSE')
plt.legend(); plt.title(f'Ridge — Error vs alpha (M={best_d_ej5})')
plt.show()

best_alpha = alphas[np.argmin(ridge_mse_test)]
print(f"Mejor alpha: {best_alpha:.4f}")
print(f"MSE test con Ridge: {min(ridge_mse_test):.4f}")
```

### Trampas técnicas

1. **Escalar antes de Ridge es OBLIGATORIO.** Ridge penaliza coeficientes — pero si las features están en escalas distintas, los coeficientes "naturales" también lo están, y la penalización es injusta. **`StandardScaler` siempre antes de `Ridge`.**
2. **`alpha=0` equivale a regresión sin regularizar.** Sklearn lo permite pero advierte por inestabilidad numérica. No lo uses como caso "control" — usá `LinearRegression()` directamente para eso.
3. **Convención sklearn `alpha = lambda`.** No te confundas con otras herramientas (statsmodels usa `lambda`, scikit-learn usa `alpha`).
4. **Rango de `alpha`:** depende del scaling. Con `StandardScaler` + features polinomiales, el rango `[1e-4, 1e4]` suele cubrir todo el espectro útil. Si tu mínimo de test está en el extremo del rango, **ampliá** el rango.
5. **Ridge no hace selección de features** (eso es Lasso/L1). Todos los coeficientes quedan != 0 pero pequeños. El TP **pide sólo Ridge**, no Lasso ni ElasticNet — no te confundas.

### Cómo verificar que está bien

- ✅ La curva de MSE test vs alpha **muestra una U**: para alpha muy bajo (≈ sin regularización), MSE test puede ser igual o peor que sin Ridge; para alpha muy alto (regularización fuerte), MSE test sube (underfitting); en el medio hay un óptimo.
- ✅ El **mejor alpha** está **dentro del rango probado**, no en los extremos. Si está en el extremo, ampliá el rango.
- ✅ Con Ridge, el MSE test del mejor modelo es **igual o ligeramente mejor** que sin Ridge. Si Ridge no mejora, es señal de que tu modelo del Ej 5/6 **no estaba sobreajustando demasiado** — y eso es información útil para la respuesta.

### Errores comunes

- ❌ **No escalar antes de Ridge.** Resultados inestables, coeficientes basura.
- ❌ **Probar pocos `alpha`** (sólo 2-3) → no ves la U.
- ❌ **Probar `alpha` en escala lineal** (`[0.1, 0.2, 0.3, ...]`) en vez de log → exploras un rango ridículo.
- ❌ **Decir "Ridge no mejora" sin justificar.** A veces no mejora porque el modelo base ya no sobreajusta — eso es una conclusión válida, pero hay que argumentarla.
- ❌ **Confundir Ridge con Lasso.** Lasso (L1) hace selección de features (coeficientes exactamente cero); Ridge (L2) sólo los achica. El TP pide Ridge.

### ¿Mejoran los resultados? (sugerencia de respuesta)

> *"En este caso, Ridge mejora marginalmente el MSE test (de ≈0.36 a ≈0.34), lo que sugiere que el modelo polinomial multivariado del Ej 5 estaba sobreajustando levemente. El mejor `alpha` resultó ≈ 1.0, valor moderado: no estamos en un régimen de overfitting severo (donde alpha tendría que ser mucho más grande). La regularización Ridge funciona como una 'póliza de seguro' contra coeficientes inestables: aún cuando el modelo base ya generaliza razonable, Ridge da más robustez ante variaciones del conjunto de entrenamiento."*

---

## Reflexión sobre uso de IA

### Las 3 sub-preguntas (cells 37, 39, 41)

**a) ¿Usaste alguna herramienta de IA (ChatGPT, Claude, Copilot, etc.) durante este trabajo? ¿Para qué?**

**b) Si usaste IA: ¿qué tuviste que entender vos para validar lo que te produjo? ¿Hubo algo que te pareció incorrecto o que tuviste que corregir?**

**c) Si no usaste IA: ¿qué recursos o estrategias usaste cuando te trabaste?**

### Sugerencias sobre cómo encararla

#### Si usaste IA (respondés a y b)

**a) — Honestidad ante todo.** La diplomatura cambió la política a *uso transparente* en 2026 explícitamente. **Mentir o minimizar es peor que admitir uso amplio.** Ejemplos de buenas respuestas:

- *"Usé ChatGPT para entender la API de `PolynomialFeatures` cuando me confundía con `include_bias`."*
- *"Le pedí a Claude que me explicara la diferencia entre `mean_squared_error` deprecado y `root_mean_squared_error`."*
- *"Usé Copilot para auto-completar el bucle sobre los 8 features del Ej 2."*

Frases a **evitar**:
- *"Sólo lo usé para revisar el código"* (si lo usaste también para escribirlo, mentí).
- *"No, sólo busqué en Google"* (si googleaste y Google te llevó a respuestas generadas por IA, indirectamente la usaste).

**b) — Esto es CLAVE.** La cátedra quiere ver que pensaste sobre lo que te dio la IA. Cosas que vale la pena mencionar:

- **La trampa `DataFrame vs ndarray`**: si ChatGPT te dio código sin advertir esto y a vos te explotó, **contalo**. Es el ejemplo más concreto de "tuve que entender X para corregir Y".
- **El default cambiante de `mean_squared_error(..., squared=False)`**: si la IA te dio código que asumía sklearn vieja y a vos te tira deprecation warning, **mostralo**.
- **El número 50 ambiguo del enunciado**: si la IA te aseguró que tu MSE estaba "mal" porque no era literalmente menor a 50, y vos descubriste que la ambigüedad era de unidades, **mostralo**.
- **Un coeficiente de regresión con signo incorrecto**: si la IA te generó código que dio un `MedInc` con coeficiente negativo (señal de bug), y vos detectaste que el problema era el selector booleano, **mostralo**.

**Ejemplo de respuesta sólida a (b):**

> *"La IA me dio un primer skeleton del Ej 2 que usaba `X[:, selector]` directamente. Cuando ejecuté me dio `InvalidIndexError` porque mi `X` era DataFrame. Tuve que entender la diferencia entre `Bunch.data` (ndarray) y `as_frame=True` (DataFrame) y elegir convertir con `np.asarray(X)`. También me sugirió usar `mean_squared_error(..., squared=False)`, que en mi versión de sklearn (1.5) tira DeprecationWarning — lo cambié por `np.sqrt(mse)`. En general, validé los coeficientes mirando el signo (esperaba positivo para MedInc) y el orden de magnitud de MSE comparado contra la varianza del target."*

#### Si no usaste IA (respondés c)

**c) — Sé concreto.** Listá:

- **Documentación oficial**: ¿de qué librería? ¿qué página? Mencionar `https://scikit-learn.org/stable/...` directamente está bien.
- **Foros**: StackOverflow, foro de la diplomatura, etc.
- **Compañeros / grupos de estudio**: ojo con esto si la entrega es individual; mejor decir "discutí conceptos con un compañero, el código lo escribí solo".
- **Libros**: si leíste Bishop §3 o Hastie ESL §3 para entender la teoría, mencionalo.
- **Notebooks de clase**: los notebooks 01 y 02 de la clase 1 tienen ejemplos muy similares (sinusoidal vs polinomial).

**Ejemplo de respuesta sólida a (c):**

> *"No usé IA. Cuando me trabé con el shape de los selectors, leí la documentación de numpy sobre boolean indexing. Para entender por qué `PolynomialFeatures` necesita `include_bias=False`, comparé con el notebook 01 de la clase 1 que usa la opción contraria (`include_bias=True` + `fit_intercept=False`). La sección §3 del Bishop me ayudó a entender por qué los coeficientes explotan con M alto (página 7 sobre regularización Ridge). Para la trampa DataFrame, leí el changelog de sklearn 1.2 donde mencionan el cambio en `as_frame`."*

### Tono recomendado para esta sección

- **Honesto** (transparencia es lo que pide la consigna).
- **Específico** (no "usé IA para todo" sino "usé IA para X, Y, Z").
- **Reflexivo** (mostrar que pensaste *por qué* funcionó o no funcionó lo que te dio).
- **3-5 líneas por pregunta** (ni un párrafo corto sin sustancia ni un ensayo larguísimo).

---

## Checklist final antes de entregar

Antes de subir el `.ipynb`, andate por esta lista:

### Estructura

- [ ] Las celdas de setup (0-11) **no fueron modificadas** (`random_state=0`, `train_size=0.8`).
- [ ] Cada ejercicio tiene **código en las celdas marcadas como `# Resolver acá`** y **texto en las celdas marcadas como `Responder acá` / `*Escribí tu respuesta acá*`**.
- [ ] La reflexión final (cells 37-42) **tiene las 3 respuestas** (a, b, c — respondés según corresponda).

### Ejercicio 1

- [ ] Las 5 preguntas tienen respuesta.
- [ ] Mencionaste el origen del dataset (censo de 1990, Pace & Barry).
- [ ] Mencionaste el cap del target en 5.0.
- [ ] Identificaste al menos 2 sesgos / dilemas éticos.

### Ejercicio 2

- [ ] Generaste **8 gráficos** (uno por feature).
- [ ] Identificaste el feature más informativo (típicamente `MedInc`).
- [ ] Tu ranking tiene **justificación** por feature.

### Ejercicio 3

- [ ] Usaste **una sola** feature.
- [ ] Imprimiste MSE en **train Y test**.
- [ ] Graficaste **modelo + train + test** en un solo gráfico.
- [ ] Tu interpretación menciona **underfitting** o equivalentemente "modelo demasiado simple".

### Ejercicio 4

- [ ] Probaste **al menos 8 grados distintos** (idealmente 1..15).
- [ ] Graficaste la **curva de error vs grado** (train + test).
- [ ] Identificaste el **mejor grado** y por qué (mínimo de test).
- [ ] Graficaste el **mejor modelo** sobre los puntos.
- [ ] Tu interpretación menciona **overfitting** (test sube luego del codo).

### Ejercicio 5

- [ ] Elegiste **2 o 3 features** con justificación.
- [ ] Repetiste el barrido de grados.
- [ ] No graficaste el modelo final (la consigna dice que no hace falta).
- [ ] Comparaste con Ej 3 y Ej 4 — **tabla numérica explícita**.

### Ejercicios 6 y 7 (opcionales — sólo si los hacés)

- [ ] Ej 6: entrenaste con 8 features, comparaste con Ej 5.
- [ ] Ej 7: probaste **al menos 5 valores de alpha en escala log**, identificaste el mejor.

### Reflexión

- [ ] Respondiste **honestamente** sobre uso de IA.
- [ ] Cada respuesta tiene **3-5 líneas**, no más, no menos.
- [ ] Si usaste IA, mencionaste **algo concreto que tuviste que entender / corregir**.

### Sanity check técnico

- [ ] El notebook **corre de arriba a abajo sin errores** (Kernel → Restart & Run All).
- [ ] No hay warnings rojos en las salidas.
- [ ] Los gráficos se ven (no quedaron como referencias rotas).
- [ ] Las celdas raw o markdown de respuesta están **renderizadas** (no se ven los asteriscos crudos).

### Antes del upload

- [ ] Nombrá el archivo con tu apellido (ej: `Zader_Javier_TP1.ipynb`) — convención DiploDatos típica.
- [ ] Verificá tamaño razonable (un `.ipynb` con muchas figuras puede pesar 1-5 MB; si pesa 50 MB hay algo raro).
- [ ] Subí a donde corresponda (campus virtual / GitHub Classroom / mail según indique la cátedra).

---

## Apéndice A — Snippets reutilizables

Esta sección es **referencia rápida**. Cuando estés trabado en el TP, mirá acá primero.

### A.1 — Carga del dataset (con fix de DataFrame)

```python
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
import numpy as np

# Forzá ndarray para evitar problemas
california = fetch_california_housing(as_frame=False)
X, y = california['data'], california['target']

# Split fijo (NO toques el random_state)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, train_size=0.8, random_state=0
)
print("X_train:", X_train.shape, "X_test:", X_test.shape)
# Esperado: (16512, 8) (4128, 8)
```

### A.2 — Selector booleano (1 feature)

```python
feature = 'MedInc'
feature_names = california['feature_names']
selector = (np.array(feature_names) == feature)

X_train_f = X_train[:, selector]    # shape (16512, 1)
X_test_f  = X_test[:, selector]     # shape (4128, 1)
```

### A.3 — Selector booleano (varias features)

```python
# Versión 1 — explícita con OR (la del notebook)
selector = (np.array(feature_names) == 'MedInc') | \
           (np.array(feature_names) == 'Latitude') | \
           (np.array(feature_names) == 'Longitude')

# Versión 2 — más pythonica
selector = np.isin(feature_names, ['MedInc', 'Latitude', 'Longitude'])

# Ambas dan el mismo array booleano de shape (8,)
X_train_fs = X_train[:, selector]   # shape (16512, 3)
X_test_fs  = X_test[:, selector]
```

### A.4 — Regresión lineal univariada + MSE

```python
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

model = LinearRegression()
model.fit(X_train_f, y_train)

mse_train = mean_squared_error(y_train, model.predict(X_train_f))
mse_test  = mean_squared_error(y_test,  model.predict(X_test_f))
print(f"MSE train: {mse_train:.4f}")
print(f"MSE test:  {mse_test:.4f}")
print(f"w_0 (intercept): {model.intercept_:.4f}")
print(f"w_1 (slope):     {model.coef_[0]:.4f}")
```

### A.5 — Pipeline polinomial con sklearn moderno

```python
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.linear_model import LinearRegression

# Univariado, sin escalar (suficiente para grados bajos)
model = make_pipeline(
    PolynomialFeatures(degree=4, include_bias=False),
    LinearRegression()      # fit_intercept=True por default
)

# Multivariado, escalando (recomendado siempre que haya >1 feature)
model_safe = make_pipeline(
    StandardScaler(),
    PolynomialFeatures(degree=4, include_bias=False),
    LinearRegression()
)
```

### A.6 — Barrido de grados (Ej 4 y Ej 5)

```python
from sklearn.metrics import mean_squared_error

degrees = list(range(1, 16))
mse_train_list, mse_test_list = [], []

for d in degrees:
    model = make_pipeline(
        StandardScaler(),
        PolynomialFeatures(degree=d, include_bias=False),
        LinearRegression()
    )
    model.fit(X_train_f, y_train)
    mse_train_list.append(mean_squared_error(y_train, model.predict(X_train_f)))
    mse_test_list.append(mean_squared_error(y_test, model.predict(X_test_f)))

best_d = degrees[np.argmin(mse_test_list)]
print(f"Mejor grado: {best_d}  MSE test: {min(mse_test_list):.4f}")
```

### A.7 — Ridge con barrido de alphas

```python
from sklearn.linear_model import Ridge

alphas = np.logspace(-4, 4, 9)   # [1e-4, ..., 1e4]
ridge_mse_test = []

for alpha in alphas:
    model = make_pipeline(
        StandardScaler(),
        PolynomialFeatures(degree=4, include_bias=False),
        Ridge(alpha=alpha)
    )
    model.fit(X_train_fs, y_train)
    ridge_mse_test.append(mean_squared_error(y_test, model.predict(X_test_fs)))

best_alpha = alphas[np.argmin(ridge_mse_test)]
print(f"Mejor alpha: {best_alpha}  MSE test: {min(ridge_mse_test):.4f}")
```

### A.8 — Cross-validation (NO la pide el TP, pero es buena práctica)

```python
from sklearn.model_selection import cross_val_score

# K-fold con K=5
scores = cross_val_score(
    model, X_train_f, y_train,
    scoring='neg_mean_squared_error',
    cv=5
)
# OJO: sklearn devuelve "neg" MSE para que mayor sea mejor
mean_mse = -scores.mean()
std_mse  = scores.std()
print(f"CV MSE: {mean_mse:.4f} ± {std_mse:.4f}")
```

> **Por qué no es obligatorio en el TP1:** la consigna pide sólo train/test split. CV es más robusto pero no se pide. Si lo agregás, mencionalo como "extra de validación" en tu interpretación.

### A.9 — Gráfico modelo + train + test (Ej 3 y Ej 4)

```python
x_start = min(np.min(X_train_f), np.min(X_test_f))
x_end   = max(np.max(X_train_f), np.max(X_test_f))
x_grid  = np.linspace(x_start, x_end, 500).reshape(-1, 1)

plt.figure(figsize=(8, 6))
plt.plot(x_grid, model.predict(x_grid), color="tomato", lw=2, label="modelo")
plt.scatter(X_train_f, y_train, facecolor="dodgerblue", edgecolor="k", alpha=0.2, s=10, label="train")
plt.scatter(X_test_f,  y_test,  facecolor="white",      edgecolor="k", alpha=0.4, s=10, label="test")
plt.title(f"Modelo — {feature}")
plt.xlabel(feature); plt.ylabel('y (x 100k USD)')
plt.legend()
plt.show()
```

### A.10 — Curva train vs test vs grado

```python
plt.figure(figsize=(8, 5))
plt.plot(degrees, mse_train_list, 'o-', label='MSE train', color='steelblue')
plt.plot(degrees, mse_test_list,  's-', label='MSE test',  color='tomato')
plt.xlabel('grado del polinomio M')
plt.ylabel('MSE')
plt.title('Error vs complejidad — bias-variance tradeoff')
plt.axvline(best_d, color='gray', ls='--', alpha=0.5, label=f'mejor M={best_d}')
plt.legend()
plt.grid(alpha=0.3)
plt.show()
```

### A.11 — Sanity check: ¿mi MSE es bueno o malo?

```python
# Baseline: predecir siempre la media del target
y_mean_pred = np.full_like(y_test, y_train.mean())
mse_baseline = mean_squared_error(y_test, y_mean_pred)
print(f"MSE baseline (predecir la media): {mse_baseline:.4f}")
# Esperado: ≈ var(y) ≈ 1.33 para California Housing

# Si tu modelo da MSE > baseline, tenés un PROBLEMA — el modelo es peor que adivinar.
# Si tu modelo da MSE ≈ baseline, no aprendió nada útil.
# Si tu modelo da MSE << baseline, está aprendiendo.
```

### A.12 — Comparar varios modelos (tabla resumen)

```python
results = {
    "Lineal univariada (Ej 3)":         mse_test_ej3,
    "Polinomial univariada (Ej 4)":     mse_test_ej4_best,
    "Polinomial multivariada (Ej 5)":   mse_test_ej5_best,
    "Todo feature (Ej 6)":              mse_test_ej6_best,
    "Ridge mejor (Ej 7)":               mse_test_ej7_best,
    "Baseline (predecir media)":        mse_baseline,
}

for name, mse in results.items():
    print(f"{name:35s}  MSE = {mse:.4f}")
```

---

## Apéndice B — Referencias bibliográficas para el TP1

### Documentación oficial sklearn

| Función | URL |
|---------|-----|
| `fetch_california_housing` | https://scikit-learn.org/stable/modules/generated/sklearn.datasets.fetch_california_housing.html |
| `train_test_split` | https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html |
| `LinearRegression` | https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html |
| `PolynomialFeatures` | https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.PolynomialFeatures.html |
| `Ridge` | https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Ridge.html |
| `RidgeCV` (alternativa) | https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.RidgeCV.html |
| `StandardScaler` | https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html |
| `mean_squared_error` | https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_squared_error.html |
| `make_pipeline` | https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.make_pipeline.html |
| `cross_val_score` | https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.cross_val_score.html |

### Guías conceptuales sklearn

| Tema | URL |
|------|-----|
| Linear models user guide | https://scikit-learn.org/stable/modules/linear_model.html |
| Preprocessing (scaling) | https://scikit-learn.org/stable/modules/preprocessing.html |
| Polynomial regression tutorial | https://scikit-learn.org/stable/modules/linear_model.html#polynomial-regression-extending-linear-models-with-basis-functions |

### Bibliografía clásica (teoría)

| Libro | Capítulo relevante | Tema |
|-------|--------------------|------|
| Bishop, C. (2006). *Pattern Recognition and Machine Learning* | §1.1, §3.1-§3.3 | Regresión lineal, polinomial, regularización Ridge |
| Hastie, Tibshirani, Friedman. *The Elements of Statistical Learning* (2nd ed., 2009) | §3.1-§3.4 | Regresión lineal y métodos shrinkage (Ridge, Lasso) |
| Goodfellow, Bengio, Courville. *Deep Learning* (2016) | §5.2-§5.4 | Capacity, overfitting, regularization (intro general) |

### NumPy / álgebra lineal

| Función | URL |
|---------|-----|
| `np.linalg.solve` | https://numpy.org/doc/stable/reference/generated/numpy.linalg.solve.html |
| `np.linalg.pinv` (pseudoinversa) | https://numpy.org/doc/stable/reference/generated/numpy.linalg.pinv.html |
| `np.linalg.lstsq` (solución least squares) | https://numpy.org/doc/stable/reference/generated/numpy.linalg.lstsq.html |
| `np.linspace` | https://numpy.org/doc/stable/reference/generated/numpy.linspace.html |
| `np.isin` (alternativa al OR encadenado) | https://numpy.org/doc/stable/reference/generated/numpy.isin.html |

### Pandas (por si X queda como DataFrame)

| Función | URL |
|---------|-----|
| `DataFrame.iloc` | https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.iloc.html |
| `DataFrame.values` (conversión a ndarray) | https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.values.html |
| `np.asarray` aplicado a DataFrame | https://numpy.org/doc/stable/reference/generated/numpy.asarray.html |

### Dataset original

- Pace, R. Kelley & Barry, Ronald (1997). *Sparse Spatial Autoregressions*. Statistics and Probability Letters, 33, 291–297. (referencia académica del dataset)
- Página de descripción sklearn: ejecutá `print(california['DESCR'])` dentro del notebook.

---

## Apéndice C — Mini-FAQ del TP1

### ¿Tengo que escalar las features?

- **Ej 3 y 4** (1 sola feature): **no estrictamente** — con una sola feature, escalar no cambia el problema (cambia la escala del coeficiente pero no el MSE).
- **Ej 5, 6, 7** (varias features): **sí, recomendado** — features con escalas dispares (`Latitude` 32-42 vs `Population` 0-30000) hacen que la regresión polinomial sea numéricamente inestable. En Ridge es aún más importante (la penalización L2 es injusta si las escalas son distintas).

### ¿Tengo que normalizar `y`?

**No.** El TP no lo pide. Y normalizar `y` complica la interpretación de los MSE (tendrías que des-normalizar para reportar en unidades reales). Dejá `y` tal cual viene de sklearn.

### ¿Puedo usar `Pipeline` o tengo que hacerlo paso a paso?

**Usá `Pipeline`** (más concretamente `make_pipeline`). Es la práctica moderna recomendada por sklearn y el notebook 01 de la clase 1 lo hace así explícitamente. Hacerlo paso a paso (instanciar `PolynomialFeatures`, fit, transform, después `LinearRegression`) funciona pero es código más feo y propenso a errores.

### ¿Puedo usar `RidgeCV` en vez de barrer alphas a mano?

**Sí, pero…** El TP **pide** explícitamente *"probar distintos valores de alpha"*, lo que sugiere un barrido manual. `RidgeCV` automatiza el CV interno y elige el alpha. **Mi recomendación: hacé el barrido manual primero (para mostrar la curva U), después podés agregar `RidgeCV` como "verificación" si querés ser explícito.**

### Mi curva de error de test NO forma una U

Posibles causas:
1. **Probaste pocos grados** → ampliá el rango (1..20 o más).
2. **No escalaste y los coeficientes explotan numéricamente** → el "test" es errático, no una U limpia.
3. **El feature es muy lineal** y no se beneficia de polinomial → es válido, mencionalo.
4. **Los datos son demasiado ruidosos** y la mejora marginal de polinomial se confunde con el ruido del split → es un hallazgo, no un error.

### ¿Tengo que sacar el cap del target en 5.0?

**No.** El TP no lo pide. Sacarlo cambia el problema (estás resolviendo un subset distinto del dataset). Lo correcto es **mencionarlo en la respuesta del Ej 1** (sesgo conocido) y **mostrar que afecta el modelo** (el modelo sub-predice las casas más caras), pero NO eliminar esas observaciones.

### Mi MSE no baja de 50 ni con el mejor modelo. ¿Está mal?

**Probablemente no.** Como discutimos, el "50" del enunciado es ambiguo en unidades. Lo importante es:
1. Tu MSE en train y test son similares (no overfitting masivo).
2. Tu MSE baja del Ej 3 al Ej 4 al Ej 5 (mejora monotónica con la complejidad apropiada).
3. Tu MSE es **mucho menor** que el baseline de predecir la media (≈ 1.33 si tu target está en unidades de 100k USD).

Si esas 3 cosas se cumplen, estás bien — independientemente de si tu número absoluto coincide con "< 50".

### ¿Por qué `LinearRegression()` no tiene parámetro `alpha`?

Porque `LinearRegression` es regresión lineal **sin regularización**. Si querés regularización, usá `Ridge(alpha=...)` (L2) o `Lasso(alpha=...)` (L1). El TP1 sólo pide Ridge (Ej 7).

### ¿Qué pasa si elijo `Population` o `AveBedrms` (los features "malos")?

Tu MSE va a ser peor, **y eso es información útil para tu interpretación**. Si lo hacés intencionalmente como "experimento de contraste", mencionalo: *"Quise verificar que los features con menor poder predictivo dan peor MSE. Con `Population` obtuve MSE ≈ 1.3, prácticamente equivalente al baseline de predecir la media."*

### ¿El notebook se puede abrir con Google Colab?

**Sí.** Subí el `.ipynb` a Colab y corre tal cual. Sklearn y numpy ya vienen instalados. Si vas a usar Colab, **fijate la versión de sklearn** al principio (`!pip show scikit-learn`) — Colab puede tener una versión más vieja o nueva que la tuya local, y eso afecta la trampa DataFrame.

### ¿Tengo que reportar coeficientes (`model.coef_`)?

**No es obligatorio** pero suma para la interpretación. Mostrar que el coeficiente de `MedInc` es positivo (más ingreso → más precio) refuerza tu análisis. Para modelos polinomiales, mostrar **el orden de magnitud** de los coeficientes (`np.abs(model.coef_).max()`) ayuda a explicar el overfitting (coeficientes en miles = inestabilidad). Ver clase 1 PDF p.23 — la tabla de coeficientes con M=9.

### Si el kernel se cuelga / queda lento en el Ej 5

Reducí el rango de grados. Con 3 features y `degree=10` ya son 286 features polinomiales — manejable pero pesado. Si tu compu sufre:
1. Bajá a `degree=8` máximo.
2. Agregá `StandardScaler` (los solvers están más optimizados con datos escalados).
3. Si seguís sufriendo, considerá Ridge en vez de LinearRegression (Ridge es más estable numéricamente).

### ¿Cómo cito esta guía en mi notebook?

No hace falta citarla — es material interno tuyo. Si tu interpretación es claramente influida por esta guía, mencioná simplemente *"siguiendo recomendaciones del material de estudio del curso"*.

---

→ Volver al [README.md](README.md)
