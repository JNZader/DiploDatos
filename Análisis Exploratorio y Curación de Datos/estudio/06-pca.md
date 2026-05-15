# 06 — PCA (Análisis de Componentes Principales)

## Concepto

PCA (*Principal Component Analysis*) es una técnica de **reducción de dimensionalidad**: toma una matriz `X ∈ ℝ^(n×m)` con muchas variables y la lleva a una matriz `Z ∈ ℝ^(n×d)` con `d ≪ m`, perdiendo la menor cantidad posible de **varianza** (información).

No selecciona columnas: construye **direcciones nuevas** (combinaciones lineales de las originales) que cumplen dos propiedades:

1. Son **ortogonales entre sí** (no están correlacionadas).
2. Están **ordenadas por varianza capturada**: PC1 captura la mayor varianza, PC2 la mayor varianza restante perpendicular a PC1, y así sucesivamente.

En la práctica te sirve para tres cosas: comprimir datos antes de un modelo, romper colinealidad entre features, y visualizar datasets de alta dimensión en 2D o 3D sin perder la estructura principal.

## Intuición

Imaginate que tenés un objeto 3D, por ejemplo un libro abierto, y querés sacarle una foto. Si lo fotografiás de canto, la foto se ve como una línea: perdiste casi toda la información. Si lo fotografiás desde el ángulo que **mejor "abre" el objeto**, la foto muestra el contenido entero. PCA es exactamente eso: busca el ángulo desde el que tus datos se ven con más detalle, donde están **más esparcidos**.

Otra forma de pensarlo: si tenés una nube de puntos alargada en alguna dirección, PC1 es la línea que pasa por el medio de esa nube siguiendo el eje largo. PC2 es perpendicular a PC1 y captura la dispersión que queda. Si proyectás los puntos sobre PC1, conservás la "forma larga"; si proyectás sobre PC2, conservás el "ancho".

La idea de fondo: **mayor varianza = más información**. Una variable que es casi constante no te dice nada; una variable muy dispersa diferencia bien a los individuos.

---

## Definición algebraica

Dada una matriz `X` centrada (con media cero por columna), PCA busca un conjunto de vectores `v_1, v_2, …, v_m` (los **componentes principales**) tales que:

1. Cada `v_k` es un vector unitario (`‖v_k‖ = 1`).
2. `v_1` maximiza la varianza de la proyección `X · v_1`.
3. `v_2` maximiza la varianza de `X · v_2` sujeto a que `v_2 ⟂ v_1`.
4. En general, `v_k` maximiza la varianza sujeto a ser ortogonal a todos los anteriores.

Los vectores `v_k` resultan ser los **autovectores de la matriz de covarianza** (o correlación si los datos están estandarizados), y los autovalores asociados son las **varianzas capturadas** por cada componente.

La proyección al nuevo espacio es:

$$
Z = X \cdot V_d
$$

donde `V_d` es la matriz `m × d` que junta los primeros `d` autovectores.

---

## Proceso en 5 pasos

1. **Normalización**. Centrar restando la media y, salvo casos especiales, **escalar dividiendo por el desvío** (StandardScaler). Si no escalás, una variable con rango grande en valor absoluto domina la varianza total y "se roba" PC1.
2. **Matriz de covarianza (o de correlación)**. Calcular la covarianza entre cada par de variables, lo que da una matriz cuadrada `m × m`.
3. **Cálculo de componentes principales**. Obtener los autovectores y autovalores de esa matriz. Los autovectores son las direcciones; los autovalores, la varianza capturada en cada una.
4. **Selección de `d`**. Elegir cuántas componentes conservar mirando la **varianza explicada acumulada** (típicamente apuntando al 90% o 95%).
5. **Proyección**. Multiplicar los datos originales por la matriz de autovectores seleccionados. El resultado es la nueva matriz `Z` con `d` columnas.

En sklearn esto es:

```python
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

X_std = StandardScaler().fit_transform(X)
pca = PCA(n_components=d)
Z = pca.fit_transform(X_std)
pca.explained_variance_ratio_   # varianza capturada por cada PC
```

---

## Por qué SIEMPRE hay que escalar antes

Esta es la trampa más común y la cátedra la marca explícitamente:

> *"sklearn centra los datos restándoles la media. Sin embargo, es recomendable también estandarizar o al menos escalar la matriz original para asegurar que todas las variables estén en las mismas unidades y ninguna tenga un peso demasiado grande."*

PCA busca maximizar varianza. Si una variable está en pesos (millones) y otra en cantidad de habitaciones (1-10), la varianza absoluta de la primera es enorme comparada con la segunda **por una cuestión de unidad**, no porque tenga más información. PC1 va a estar prácticamente alineada con la variable cara, y las demás quedan invisibles.

### Comparación numérica (Melbourne Housing)

La cátedra muestra esta comparación al aplicar PCA sobre `melb_data`:

| Escalado            | Rango aprox. tras transformar | Varianza explicada por PC1 |
|---------------------|-------------------------------|----------------------------|
| MinMaxScaler(-1, 1) | [-1, 1] (acotado fijo)        | **≈ 17%**                  |
| StandardScaler      | min ≈ -2.89, max ≈ 88         | **≈ 2.2%**                 |

Parece contraintuitivo: con StandardScaler la varianza de PC1 es **menor**, no mayor. Lo que pasa es que StandardScaler deja que las colas largas (outliers) se manifiesten (máximo cerca de 88 desvíos), entonces la varianza queda repartida entre más componentes y ninguna domina abrumadoramente. Con MinMaxScaler todas las columnas se comprimen al mismo rango fijo y eso vuelve a dar peso desproporcionado a las que tienen distribución más uniforme.

Conclusión práctica: **escalá siempre** y elegí StandardScaler como default. Usá RobustScaler si hay muchos outliers y MinMaxScaler solo si entendés bien qué efecto tiene en tus datos.

---

## explained_variance_ratio_ y varianza acumulada

`pca.explained_variance_ratio_` devuelve un array con la **proporción de varianza** capturada por cada componente. Suma 1 cuando `n_components = m` (todas las componentes).

```python
import numpy as np

ratios = pca.explained_variance_ratio_
cum = np.cumsum(ratios)
# graficar cum vs número de componentes — el famoso "codo"
```

La curva acumulada se llama **scree plot** (o gráfico de codo). El criterio típico es elegir el `d` más chico tal que `cum[d-1] ≥ 0.95` (o 0.90 según cuán agresivo quieras ser).

### Iris (ejemplo clásico)

`Iris` tiene 4 features numéricas (largo y ancho de pétalo y sépalo). Con `n_components=4`:

```
explained_variance_ratio_ ≈ [0.7296, 0.2285, 0.0367, 0.0052]
```

Interpretación: PC1 captura el 72.96% de la varianza. PC1 + PC2 = **95.81%**. Es decir, con solo 2 dimensiones reconstruimos casi toda la estructura del dataset de 4 dimensiones. Esto explica por qué `Iris` se visualiza tan bien en 2D.

---

## Ejemplo numérico: PCA sin escalar vs PCA escalado

Veamos qué pasa con una matriz `5 × 3` donde una columna tiene una escala muy distinta a las otras dos.

| Fila | Salario (pesos) | Edad (años) | Antigüedad (años) |
|------|-----------------|-------------|-------------------|
| 1    | 800.000         | 25          | 1                 |
| 2    | 1.200.000       | 30          | 3                 |
| 3    | 1.500.000       | 35          | 5                 |
| 4    | 1.900.000       | 40          | 8                 |
| 5    | 2.400.000       | 45          | 10                |

**Varianzas (sin escalar)**:

- Salario: varianza ≈ 4 × 10¹¹ (cientos de miles de millones).
- Edad: varianza = 62.5.
- Antigüedad: varianza = 13.7.

La varianza del salario es **trillones de veces** mayor que la de las otras dos.

**PCA sin escalar**:

```
explained_variance_ratio_ ≈ [0.99999..., 1e-8, 1e-9]
```

PC1 captura prácticamente el 100% de la varianza pero **lo único que está midiendo es la variación del salario**. Edad y antigüedad son invisibles. Si usás `Z[:, 0]` como feature, estás usando una versión escalada del salario y nada más.

**PCA escalado (StandardScaler primero)**:

Después de estandarizar, las tres columnas tienen varianza = 1. La varianza total es 3.

```
explained_variance_ratio_ ≈ [0.99, 0.007, 0.003]
```

PC1 sigue capturando casi toda la varianza, pero ahora **porque las tres variables están altamente correlacionadas** (sueldo, edad y antigüedad se mueven juntas en este dataset chiquito). Eso sí es información real, no un artefacto de unidades.

Moraleja: sin escalar, PCA detecta **escalas**. Con escalado, PCA detecta **correlaciones**.

---

## Conexión con el TP

- **TP1 Ejercicio 3 (PCA)**: aplicaste PCA sobre la matriz final (numéricas + categóricas codificadas + imputadas con KNN). La consigna pide `n_components = min(20, X.shape[0])`. **Atención al posible typo**: con `melb_data` tenés 13.580 filas, así que `X.shape[0] = 13580` y el `min` da 20. Pero PCA no puede tener más componentes que `min(n_samples, n_features)`, y el límite que importa cuando reducís dimensionalidad es el de features. Probablemente la consigna quería decir `X.shape[1]`. **Mencionalo en la documentación** del entregable como observación crítica.
- **TP1 Ejercicio 3 (escalado)**: la consigna explicita "responder si hace falta escalar". La respuesta es **sí, siempre**. Después del OHE y la imputación KNN tenés columnas en escalas muy distintas (precio en millones, latitudes en decenas, dummies en 0/1). Sin escalar, las columnas de precio dominan.
- **TP1 Ejercicio 3 (composición)**: la consigna pide **agregar las dos primeras componentes como features nuevas** al DataFrame final. Es decir, no usás PCA solo para reducir, sino también para **enriquecer**: PC1 y PC2 se suman como columnas extra (`PC1`, `PC2`) que luego un modelo posterior puede aprovechar.
- **TP1 Ejercicio 3 (sub-selección opcional)**: si elegís reducir, mirá `explained_variance_ratio_` acumulado y cortá donde llegues al 90-95%. Justificalo en el documento.

---

## Errores comunes

1. **No escalar antes de PCA**. Es el error número uno. La columna con escala grande se come PC1 y el resultado es inútil. Si te aparece una PC1 que captura el 99% de la varianza con una columna numérica enorme en el dataset, sospechá antes de festejar.
2. **Elegir `n_components` "a ojo"**. Tres componentes porque "queda lindo en 3D" no es un criterio. Mirá el scree plot y elegí por varianza acumulada, no por estética.
3. **Aplicar PCA sobre One-Hot Encoding sin pensarlo**. Las columnas OHE son binarias con muchísimos ceros (esparsas). PCA sobre esa matriz mezcla la varianza de las dummies con la de las numéricas, y como las dummies tienen varianza chica (de un Bernoulli con `p` pequeño), suelen quedar enterradas. Si tu dataset es mayoritariamente OHE de alta cardinalidad, considerá `TruncatedSVD` (la versión de PCA pensada para matrices ralas) o reducí cardinalidad antes.
4. **Interpretar las componentes como si fueran variables originales**. PC1 NO es "salario": es una combinación lineal de todas las variables. Para entender qué significa, hay que mirar los **loadings** (los coeficientes en `pca.components_`) y ver qué variables pesan más. Si PC1 tiene loadings altos para `Rooms`, `Bathroom` y `Price`, podés interpretar PC1 como "tamaño/lujo de la propiedad".
5. **Hacer PCA sobre datos con NaN**. PCA no maneja faltantes: imputalos primero (KNN, MICE, media según el caso) y recién después aplicá PCA.
6. **Fit del PCA en el dataset completo y luego "train/test split"**. Si vas a modelar, el PCA tiene que ajustarse SOLO en train y transformarse sobre test, igual que cualquier preprocesador. Si no, hay leakage de información del test al entrenamiento.

---

## Detrás de escena: los tres modos de `n_components`

Acá hay un tema que **mucha gente parametriza a ojo** y no sabe que `n_components` acepta tres formas distintas con tres comportamientos distintos. Esto es importante para justificar tu elección en TP1 Ej. 3 cuando tengas que defender por qué elegiste 10, 20 o "lo que cubra el 95%".

### Modo 1 — Entero: cantidad fija de componentes

```python
pca = PCA(n_components=10)
```

Le decís: "quedate con las 10 primeras componentes principales, no me importa cuánta varianza capturan". Es el modo más directo y el más usado en visualización (típicamente `n_components=2` para plottear en 2D).

**Cuándo conviene**:
- Querés un número fijo, predecible, para meter en un modelo posterior.
- Necesitás controlar el tamaño exacto de la matriz reducida (por ejemplo, para memoria o tiempo).
- Estás haciendo benchmarks contra otra técnica de reducción y querés el mismo `d`.

**Trampa**: si elegís 10 a ojo, podés estar quedándote con muy poca varianza (10% en datasets de alta dimensión) o demasiada (99.9% en datasets correlacionados, donde 3 hubieran alcanzado).

### Modo 2 — Float entre 0 y 1: ratio de varianza acumulada

```python
pca = PCA(n_components=0.95)
```

Le decís: "elegí la cantidad de componentes que necesites para capturar el 95% de la varianza". Sklearn calcula la varianza acumulada y se queda con el primer `d` tal que `cumsum[d] >= 0.95`.

**Cómo lo implementa internamente**:
1. Ajusta PCA con `n_components = min(n_samples, n_features)` (todas).
2. Calcula `np.cumsum(explained_variance_ratio_)`.
3. Devuelve el `d` mínimo que cubre el umbral.

```python
pca = PCA(n_components=0.95)
pca.fit(X_std)
pca.n_components_   # cantidad efectiva de componentes elegidas, p.ej. 7
```

**Cuándo conviene**:
- Querés un criterio **basado en información**, no en estética.
- No conocés el dataset y querés que la elección sea data-driven.
- Estás escribiendo un pipeline que va a procesar varios datasets distintos: el `0.95` se adapta solo, mientras que un `n_components=10` fijo puede ser excesivo o insuficiente según el caso.

**Umbrales típicos**:
- `0.99` → conservador, preserva casi todo. Reducción modesta.
- `0.95` → estándar. Buen balance entre reducción e información.
- `0.90` → agresivo. Reducción fuerte, asume que el 10% restante es ruido.
- `0.80` → solo para visualización o cuando sabés que el dataset tiene mucho ruido.

### Modo 3 — String `'mle'`: estimación automática por Máxima Verosimilitud

```python
pca = PCA(n_components='mle')
```

Le decís: "elegí vos cuántas componentes". Sklearn implementa el algoritmo de **Minka (2000)** que usa Máxima Verosimilitud (en inglés *Maximum Likelihood Estimation*) para estimar la "dimensión intrínseca" del dataset asumiendo un modelo probabilístico (PPCA — *Probabilistic PCA*).

**Idea intuitiva**: PPCA asume que tus datos viven en un subespacio de dimensión `d` más ruido gaussiano. MLE estima qué `d` es más compatible con la estructura observada de los autovalores.

**Cuándo conviene**:
- No querés elegir umbral ni cantidad y querés delegar al algoritmo.
- Sospechás que el dataset tiene una "dimensión real" baja oculta bajo ruido.
- Estás haciendo investigación o un análisis automático sin supervisión.

**Trampas**:
- Solo funciona si `n_samples > n_features` (no admite datasets "anchos").
- Es más lento que los otros dos modos.
- A veces devuelve resultados extraños en datasets pequeños o muy correlacionados.
- Asume gaussianidad de los datos en el subespacio — si no es gaussiano, la estimación es subóptima.

### Tabla comparativa

| Modo | Tipo de input | Qué hace | Cuándo elegirlo |
|------|---------------|----------|------------------|
| **Entero** (ej. `10`) | `int >= 1` | Te quedás con esa cantidad fija | Querés control exacto, visualización, benchmarks |
| **Float** (ej. `0.95`) | `0 < float < 1` | Devuelve el mínimo `d` tal que cumsum ≥ ratio | Criterio basado en información, pipelines flexibles |
| **`'mle'`** | string | Minka MLE estima `d` automáticamente | Análisis exploratorio sin criterio fijo |
| `None` (default) | — | `min(n_samples, n_features)` (todas) | Análisis inicial, scree plot |

### Ejemplo en Melbourne (TP1)

Supongamos que después de imputar y escalar, tu matriz tiene 25 columnas (originales + OHE). Probás los tres modos:

```python
from sklearn.decomposition import PCA

# Modo 1 — fijo
pca_fixed = PCA(n_components=10).fit(X)
pca_fixed.explained_variance_ratio_.sum()
# Por ejemplo: 0.78 (78% de varianza con 10 componentes)

# Modo 2 — por ratio
pca_ratio = PCA(n_components=0.95).fit(X)
pca_ratio.n_components_
# Por ejemplo: 17 componentes (necesarias para llegar al 95%)

# Modo 3 — MLE
pca_mle = PCA(n_components='mle').fit(X)
pca_mle.n_components_
# Por ejemplo: 12 (lo que el algoritmo estima como "dimensión real")
```

Cada modo te da una respuesta distinta a la misma pregunta. La que justifiques con argumento en el documento del TP es la "correcta" para tu caso.

### La trampa típica en TP1

La consigna del TP1 Ej. 3 dice `n_components = min(20, X.shape[0])`. Como vimos en el archivo, `X.shape[0]` son las **filas** (13.580), no las columnas. El `min(20, 13580)` siempre va a dar `20`. Por lo tanto, la consigna está pidiendo **modo entero fijo con `n_components=20`** (probablemente con un typo: debería ser `X.shape[1]`, las columnas).

Si querés ir más allá de la consigna y dar valor al documento, podés justificar:
1. Por qué `20` puede ser arbitrario (no responde a un criterio de varianza).
2. Qué te daría `n_components=0.95` (criterio basado en información).
3. Que `'mle'` es una opción de "elige solo" para análisis automatizado.

Esa discusión es lo que la entrega documental del TP recompensa.

### Resumen

- `n_components` acepta entero (cantidad fija), float entre 0 y 1 (umbral de varianza acumulada), o `'mle'` (estimación automática por MLE).
- Para visualización: usá entero (típicamente 2 o 3).
- Para pipelines productivos: usá float (típicamente 0.95).
- Para análisis exploratorio sin criterio: `'mle'`, pero con cuidado.
- En el TP1, la consigna fija un entero por simplicidad pedagógica, pero el modo float es más profesional y vale la pena mencionarlo en la entrega.

¿Se entiende? Tres formas de responder a la misma pregunta ("¿cuántas componentes me quedo?"), tres filosofías distintas.

---

## Checklist de comprensión

- [ ] ¿Por qué la cátedra muestra PC1 ≈ 17% con MinMaxScaler y ≈ 2.2% con StandardScaler? ¿Cuál preferís y por qué?
- [ ] Si en TP1 Ej. 3 ves que tu PC1 captura el 99% de la varianza, ¿qué tenés que verificar antes de seguir?
- [ ] En el ejemplo de salario/edad/antigüedad, ¿por qué sin escalar PC1 captura el 99.99% y eso es una mala señal?
- [ ] ¿Cuál es la diferencia entre usar PCA para **reducir** dimensionalidad y para **enriquecer** features? (TP1 pide lo segundo.)
- [ ] ¿Qué pasa si pasás `n_components=0.95` vs `n_components=10` vs `n_components='mle'`? ¿Cuándo elegirías cada uno?

---

**Próximo paso**: `07-exploracion-eda.md`
