# 09 — KNN y modelos no paramétricos

> Clase 2 — DiploDatos UNC 2026
> Material fuente: PDF clase 2, p. 26–34 (bloque K-NN) + complemento bibliográfico.
> Pre-requisitos: cap. 04 (escalado de features), cap. 05/06 (qué es un clasificador), cap. 08 (concepto de modelo paramétrico).

---

## 1. Concepto

**K-Nearest Neighbors (KNN)** es un clasificador **no paramétrico** que asigna a cada nuevo punto la clase mayoritaria entre sus $k$ vecinos más cercanos en el espacio de features.

La regla de decisión es:

$$
\hat{y}(\mathbf{x}) \;=\; \arg\max_{c \in \mathcal{C}}\; \sum_{i \in N_k(\mathbf{x})} \mathbb{1}\{y_i = c\}
$$

donde $N_k(\mathbf{x})$ es el conjunto de los $k$ índices del training set más cercanos a $\mathbf{x}$ según una métrica de distancia $d(\cdot, \cdot)$.

**Lo que define a KNN como categoría diferente:**

- **No paramétrico** — no hay un vector fijo de parámetros que resuma los datos.
- **Memory-based** / **instance-based learning** — el modelo almacena todo el training set y posterga el cómputo hasta la predicción ("lazy learning").
- **No tiene fase de entrenamiento** real: `fit` se limita a guardar los datos (y construir índices espaciales).
- Genera **fronteras de decisión arbitrariamente complejas** sin asumir ninguna forma funcional.
- Extiende a multiclase de forma **trivial**: el argmax sobre votos funciona igual para K = 2 que para K = 1000.

> Subtítulo del PDF (p. 26): "Vecinos más cercanos — clasificación por similitud local."

---

## 2. Intuición

### 2.1. Paramétrico vs no paramétrico — la definición precisa

Esta distinción no aparece formalizada en el material de cátedra; se infiere por contraste. La definición rigurosa (Bishop §2.5):

> **Paramétrico:** la distribución (o el clasificador) queda completamente especificada por un **vector finito y fijo** de parámetros $\boldsymbol{\theta}$. El tamaño de $\boldsymbol{\theta}$ es **independiente del tamaño del training set**.

Ejemplos: regresión logística (un peso por feature), Naive Bayes (priors + likelihoods por clase), redes neuronales (pesos por capa).

> **No paramétrico:** la complejidad efectiva del modelo **crece con la cantidad de datos**. El modelo no resume los datos en un vector fijo — los usa directamente o construye estructuras que escalan con $m$.

Ejemplos: KNN ($O(m)$ ejemplos almacenados), kernel density estimation (una bandwidth por punto), árboles de decisión sin pruning, procesos Gaussianos.

> Cuidado con la palabra: "no paramétrico" **no** significa "sin parámetros". Significa **"sin un número fijo de parámetros"**. KNN tiene hiperparámetros ($k$, métrica), pero su "vector de información" es todo el training set, que crece con $m$.

### 2.2. La metáfora del barrio

Si te mudaste a una ciudad nueva y querés saber cuánto cuesta una pizza típica, **no construís un modelo regional**: preguntás en tu cuadra. Si todos los vecinos pagan \$5000, asumís \$5000. Eso es KNN con $k$ = vecinos en la cuadra.

- $k = 1$: copiás el precio del **único** vecino más cercano. Si vivís al lado del único restaurante caro de la zona, vas a errar feo.
- $k = 21$: promediás (votación mayoritaria) entre 21 vecinos. Más estable, menos ruidoso.
- $k = m$ (todos): predecís siempre la clase global mayoritaria. Te perdiste toda la estructura local.

### 2.3. Diagramas de Voronoi (k = 1)

Para $k = 1$, el clasificador particiona el espacio en **celdas de Voronoi**: cada celda contiene exactamente un punto del training y todo el espacio dentro de la celda se clasifica como ese punto.

```
. . . . . . . . . . .
.   A      |       .
.    +-----+       .
.    |  B  |       .
.    |  +  |       .
.    |     +---+   .
.    |   C  | D|   .
.    +------+--+   .
. . . . . . . . . .
```

Cada borde entre dos celdas es **equidistante** a los dos puntos vecinos: es la **mediatriz** del segmento que los une. La frontera de decisión es la unión de los bordes donde las clases difieren.

> PDF p. 30: "El espacio se divide en regiones disjuntas. Las fronteras son equidistantes a los puntos de entrenamiento vecinos. k-NN genera fronteras arbitrariamente complejas. La extensión a multiclases es trivial."

### 2.4. KNN como aproximador local de la densidad

Bishop §2.5.2 da el marco probabilístico: KNN es equivalente a **estimar $P(y\mid\mathbf{x})$** mediante una ventana que se adapta a la densidad local. La ventana tiene radio igual a la distancia al $k$-ésimo vecino, así que:

- En zonas con muchos datos, la ventana es chiquita → resolución fina.
- En zonas con pocos datos, la ventana se agranda → menos resolución pero más estabilidad.

Esta adaptación local es la razón por la cual KNN funciona bien en datasets con densidad heterogénea — algo que kernel methods de ancho fijo (KDE clásico) no logran.

---

## 3. Cuerpo técnico

### 3.1. Algoritmo paso a paso

**Entrada:**
- Training set $\{(\mathbf{x}^{(i)}, y^{(i)})\}_{i=1}^{m}$.
- Punto a clasificar $\mathbf{x}^*$.
- Hiperparámetros: $k$, métrica $d$, pesado $w$ (uniforme o por distancia).

**Algoritmo:**
1. Calcular $d(\mathbf{x}^*, \mathbf{x}^{(i)})$ para todo $i \in \{1, \dots, m\}$.
2. Seleccionar los índices de los $k$ vecinos con menor distancia: $N_k(\mathbf{x}^*) = \{i_1, \dots, i_k\}$.
3. Aplicar la regla de votación:

$$
\hat{y}(\mathbf{x}^*) \;=\; \arg\max_{c \in \mathcal{C}}\; \sum_{i \in N_k(\mathbf{x}^*)} w_i \cdot \mathbb{1}\{y^{(i)} = c\}
$$

Si $w_i = 1$ ∀i: votación uniforme. Si $w_i = 1/d(\mathbf{x}^*, \mathbf{x}^{(i)})$: votación pesada por proximidad inversa (vecinos más cercanos pesan más).

**Para predicción probabilística:**

$$
\hat{P}(y = c \mid \mathbf{x}^*) \;=\; \frac{1}{k} \sum_{i \in N_k(\mathbf{x}^*)} \mathbb{1}\{y^{(i)} = c\}
$$

— el porcentaje de vecinos de la clase $c$.

### 3.2. Métricas de distancia

La métrica define qué quiere decir "cerca". Cambia la métrica, cambia el clasificador.

| Métrica | Fórmula | Cuándo usar |
|---|---|---|
| **Euclidiana** (L2) | $d(\mathbf{a}, \mathbf{b}) = \sqrt{\sum_j (a_j - b_j)^2}$ | Default razonable; features continuas comparables |
| **Manhattan** (L1) | $d(\mathbf{a}, \mathbf{b}) = \sum_j \lvert a_j - b_j\rvert$ | Features con outliers; alta dimensión |
| **Minkowski** | $d(\mathbf{a}, \mathbf{b}) = \left(\sum_j \lvert a_j - b_j\rvert^p\right)^{1/p}$ | Familia paramétrica (L2 = Minkowski p=2; L1 = p=1) |
| **Mahalanobis** | $d(\mathbf{a}, \mathbf{b}) = \sqrt{(\mathbf{a}-\mathbf{b})^T \Sigma^{-1}(\mathbf{a}-\mathbf{b})}$ | Cuando las features están correlacionadas y tienen escalas diferentes |
| **Coseno** | $d(\mathbf{a}, \mathbf{b}) = 1 - \frac{\mathbf{a} \cdot \mathbf{b}}{\Vert \mathbf{a}\Vert \,\Vert \mathbf{b}\Vert }$ | Vectores de texto (tf-idf), embeddings — interesa la dirección, no la magnitud |
| **Hamming** | $d(\mathbf{a}, \mathbf{b}) = \sum_j \mathbb{1}\{a_j \neq b_j\}$ | Features categóricas / binarias |

> En sklearn: parámetro `metric` (default `'minkowski'` con `p=2` = euclidiana). La métrica de Mahalanobis requiere pasar la matriz $\Sigma^{-1}$ vía `metric_params`.

### 3.3. Escalado obligatorio antes de KNN

**Esta es la regla número uno**, no negociable: KNN depende de distancias en el espacio crudo de features. Si una feature tiene escala mucho mayor que las demás, **domina la distancia y aplasta al resto**.

**Ejemplo del horror:** dataset de personas con dos features:
- Altura en cm: rango ~150–200 (50 unidades de variación).
- Sueldo en pesos: rango ~200000–2000000 (1.800.000 unidades de variación).

La distancia euclidiana entre dos personas:

$$
d = \sqrt{(\Delta\text{altura})^2 + (\Delta\text{sueldo})^2} \approx \sqrt{(\Delta\text{sueldo})^2} = |\Delta\text{sueldo}|
$$

La altura es invisible para KNN. **El sueldo manda solo**.

**Fix:** estandarizar (o normalizar) antes de aplicar KNN.

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier

pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('knn', KNeighborsClassifier(n_neighbors=5)),
])
pipe.fit(X_train, y_train)
```

> Usar `Pipeline` no es estético — es **correcto**: garantiza que `StandardScaler` se ajusta solo con train y se aplica también al test, evitando data leakage.

### 3.4. Elección de k — el dial del bias-variance

| $k$ pequeño | $k$ grande |
|---|---|
| Frontera ruidosa, sigue cada ejemplo | Frontera suave, ignora detalles |
| Sesgo bajo, varianza alta | Sesgo alto, varianza baja |
| Overfitting → train error ≈ 0, test error alto | Underfitting → ambos errores altos |
| Sensible a outliers en el training | Robusto a outliers |

**Tabla del PDF (p. 31–32):**

| k | Training error | Testing error |
|---|---|---|
| 1 | 0.000 | 0.421 |
| 3 | 0.177 | 0.386 |
| 7 | 0.273 | 0.364 |
| 21 | 0.269 | 0.314 |

- **k=1** es el caso patológico clásico: error de entrenamiento **exactamente cero** (cada punto es su propio vecino más cercano), error de test mucho peor. Overfitting absoluto.
- **k=21** alcanza el mejor test error con un training error ligeramente peor — el modelo generaliza mejor a costa de no memorizar.

> Mensaje de cátedra: "k pequeño → overfitting / fronteras ruidosas. k grande → suaviza la frontera y mejora test (con tradeoff de sesgo)."

**Reglas prácticas para elegir k:**
- Empezar con $k = \sqrt{m}$ como heurística inicial ($m$ = tamaño de training).
- **Usar $k$ impar** para clasificación binaria → evita empates.
- Tunear con cross-validation. Rango típico: $\{1, 3, 5, 7, 11, 15, 21, 31\}$.
- Si tenés problema multiclase con $K$ clases, $k$ impar no garantiza romper empates — usar votación pesada por distancia (`weights='distance'`).

### 3.5. Curse of dimensionality (la trampa de la alta dimensión)

En espacios de alta dimensión, **todos los puntos están aproximadamente equidistantes entre sí**. Esto rompe la premisa de KNN.

**El argumento intuitivo (Bishop §1.4):**
- En una hiperesfera de radio $r$ en $d$ dimensiones, la mayor parte del volumen está concentrada en una cáscara externa cerca de la superficie cuando $d$ es grande.
- La distancia mínima y máxima entre cualquier par de puntos uniformemente distribuidos **converge al mismo valor** cuando $d \to \infty$.
- Resultado: el "vecino más cercano" deja de ser significativamente más cercano que un punto aleatorio cualquiera.

**Síntomas prácticos:**
- KNN funciona genial con 5–20 features.
- Degrada notablemente entre 50–200 features.
- Es casi inútil con > 500 features sin pre-procesamiento (PCA, embeddings).

**Mitigaciones:**
- **Reducción de dimensionalidad** (PCA, t-SNE para visualización, UMAP, autoencoders).
- **Selección de features** (filter / wrapper methods).
- **Métricas aprendidas** (Mahalanobis con $\Sigma$ aprendida de los datos — ver Large Margin Nearest Neighbor de Weinberger & Saul).
- **Embeddings densos** (Word2Vec, CLIP) — bajan la dimensión efectiva de datos esparzos.

### 3.6. Costo computacional y estructuras de datos

**Predicción naïve (brute force):** $O(m \cdot n)$ por consulta — calcular distancia a todos los $m$ puntos en $n$ dimensiones. Insostenible para $m > 10^5$ o consultas frecuentes.

**Estructuras espaciales:**

| Estructura | Construcción | Consulta promedio | Cuándo |
|---|---|---|---|
| **Brute force** | $O(1)$ | $O(mn)$ | $m$ chico (< 10k) o $n$ muy alto (> 30) |
| **KD-tree** | $O(mn \log m)$ | $O(\log m)$ esperado | $n$ bajo (≲ 20), datos densos |
| **Ball tree** | $O(mn \log m)$ | $O(\log m)$ esperado | $n$ medio (20–100), métricas no-euclidianas |
| **Approximate Nearest Neighbors (ANN)** | $O(m \log m)$ | $O(\log m)$ aprox. | $n$ alto, $m$ enorme; aceptás error |

**KD-tree** parte el espacio recursivamente con cortes ortogonales a los ejes. Funciona bien en baja dimensión pero degenera a brute force en alta (por curse of dimensionality).

**Ball tree** parte el espacio en hiperesferas anidadas. Más estable en dimensiones medias y soporta métricas no-euclidianas.

**ANN (Approximate Nearest Neighbors):** sacrifica exactitud por velocidad. Bibliotecas: FAISS (Facebook), Annoy (Spotify), HNSW. Imprescindible para sistemas de recomendación o búsqueda semántica con millones de vectores.

**Sklearn:** parámetro `algorithm` en `KNeighborsClassifier` — `'auto'` (default), `'ball_tree'`, `'kd_tree'`, `'brute'`. Con `'auto'`, sklearn decide en base al tamaño y dimensión del dataset.

### 3.7. Almacenamiento — el otro costo invisible

KNN guarda **todo el training set**. Para producción:
- $m = 10^4$ y $n = 100$ → ~ 8 MB en float64. Manejable.
- $m = 10^6$ y $n = 1000$ → ~ 8 GB. Empieza a doler.
- $m = 10^8$ → impráctico sin ANN + cuantización.

**Mitigaciones:**
- **Prototype methods** (Hastie ESL §13): condensar el training a un subconjunto representativo (Learning Vector Quantization, K-means + KNN sobre centroides).
- **Cuantización** (Product Quantization, Scalar Quantization): comprimir vectores a 1–8 bytes con pérdida controlada.
- **Pruning** de ejemplos dominados (CNN — Condensed Nearest Neighbor de Hart 1968; ENN — Edited Nearest Neighbor de Wilson 1972).

### 3.8. KNN para regresión

KNN no es solo clasificador; también hace regresión:

$$
\hat{y}(\mathbf{x}^*) \;=\; \frac{1}{k}\sum_{i \in N_k(\mathbf{x}^*)} y^{(i)}
$$

(promedio simple). O ponderado por distancia inversa. En sklearn: `KNeighborsRegressor`. Útil como baseline no paramétrico antes de saltar a árboles o redes.

### 3.9. La cota de Cover & Hart (1967)

El paper fundacional **Cover & Hart, "Nearest Neighbor Pattern Classification", IEEE TIT 13(1), 21-27 (1967)** demostró un resultado teórico clave:

> En el límite $m \to \infty$, el error asintótico de **1-NN** está acotado superiormente por el doble del error de Bayes:
> $$ R^* \leq R_{1\text{NN}} \leq 2R^*(1 - R^*) \leq 2R^* $$
> donde $R^*$ es el error de Bayes (el mínimo teórico alcanzable por **cualquier** clasificador conociendo la distribución verdadera).

Y para $k$-NN con $k$ creciente apropiadamente: $R_{k\text{NN}} \to R^*$ (converge al óptimo). Es decir, **KNN es asintóticamente óptimo**. El problema, claro, es que "asintótico" implica datos infinitos — en la práctica el curse of dimensionality te come antes.

### 3.10. Uso en sklearn

```python
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('knn', KNeighborsClassifier(
        n_neighbors=5,
        weights='uniform',        # o 'distance'
        algorithm='auto',          # o 'ball_tree' / 'kd_tree' / 'brute'
        metric='minkowski', p=2,   # euclidiana
        n_jobs=-1,                 # paraleliza la búsqueda
    )),
])
pipe.fit(X_train, y_train)
pipe.predict(X_test)
pipe.predict_proba(X_test)
```

**Atributos relevantes:**
- `pipe.named_steps['knn'].n_samples_fit_` — cantidad de ejemplos guardados.
- `pipe.named_steps['knn'].classes_` — clases vistas en train.
- Después de fit, **no hay coeficientes que inspeccionar**: los datos son el modelo.

---

## 4. Ejemplo numérico

### 4.1. Setup mínimo

Training set en 2D con dos clases:

| i | $x_1$ | $x_2$ | $y$ |
|---|---|---|---|
| 1 | 1 | 1 | A |
| 2 | 2 | 1 | A |
| 3 | 1 | 2 | A |
| 4 | 5 | 5 | B |
| 5 | 6 | 5 | B |
| 6 | 5 | 6 | B |
| 7 | 6 | 6 | B |

Punto a clasificar: $\mathbf{x}^* = (3, 3)$.

### 4.2. Distancias euclidianas a cada training point

$d_i = \sqrt{(x_{i,1} - 3)^2 + (x_{i,2} - 3)^2}$

| i | $\mathbf{x}^{(i)}$ | clase | $d_i$ |
|---|---|---|---|
| 1 | (1, 1) | A | $\sqrt{4 + 4} = 2.83$ |
| 2 | (2, 1) | A | $\sqrt{1 + 4} = 2.24$ |
| 3 | (1, 2) | A | $\sqrt{4 + 1} = 2.24$ |
| 4 | (5, 5) | B | $\sqrt{4 + 4} = 2.83$ |
| 5 | (6, 5) | B | $\sqrt{9 + 4} = 3.61$ |
| 6 | (5, 6) | B | $\sqrt{4 + 9} = 3.61$ |
| 7 | (6, 6) | B | $\sqrt{9 + 9} = 4.24$ |

### 4.3. Predicción con distintos k

- **k=1:** el más cercano es (2,1) o (1,2), ambos clase A → **A**.
- **k=3:** los tres más cercanos son (2,1, A), (1,2, A), (1,1, A) o (5,5, B) — empatan tres en 2.83. Tomando los tres más cercanos sin empate raro: (2,1, A), (1,2, A) y luego (1,1, A) o (5,5, B) según tie-breaking. Si entran los tres A's → **A** (3 a 0). Si el tie-break elige (5,5,B) → **A** igual (2 a 1).
- **k=5:** ordenadas por distancia: A, A, {A, B} empate, B, B → 3 A's vs 2 B's → **A**.
- **k=7:** todos los puntos → 3 A's vs 4 B's → **B**. 🤔

Mensaje del ejemplo: con $k$ demasiado grande respecto al tamaño del training, KNN tiende a predecir la clase mayoritaria global y pierde sensibilidad local.

### 4.4. Efecto del escalado — el caso del horror

Misma data, pero ahora $x_2$ está en escala 1000×:

| i | $x_1$ | $x_2$ | $y$ |
|---|---|---|---|
| 1 | 1 | 1000 | A |
| 2 | 2 | 1000 | A |
| 3 | 1 | 2000 | A |
| 4 | 5 | 5000 | B |
| 5 | 6 | 5000 | B |
| 6 | 5 | 6000 | B |
| 7 | 6 | 6000 | B |

Punto $\mathbf{x}^* = (3, 3000)$. Distancia al punto 1 (1, 1000):

$$
d = \sqrt{(1-3)^2 + (1000-3000)^2} = \sqrt{4 + 4{,}000{,}000} \approx 2000
$$

La diferencia en $x_1$ aporta $\sqrt{4} = 2$ unidades de distancia, contra ~2000 de $x_2$. **$x_1$ es ruido para KNN**. Estandarizando ambas a media 0 y desvío 1, las dos features pesan lo mismo y el ranking de vecinos refleja la geometría real.

### 4.5. Replicar la tabla del PDF (k vs error)

```python
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

X, y = make_classification(n_samples=500, n_features=10, n_informative=5,
                           n_redundant=2, random_state=0)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=0)

scaler = StandardScaler().fit(X_tr)
X_tr_s = scaler.transform(X_tr)
X_te_s = scaler.transform(X_te)

for k in [1, 3, 7, 21]:
    clf = KNeighborsClassifier(n_neighbors=k).fit(X_tr_s, y_tr)
    train_err = 1 - accuracy_score(y_tr, clf.predict(X_tr_s))
    test_err  = 1 - accuracy_score(y_te, clf.predict(X_te_s))
    print(f"k={k}: train_err={train_err:.3f}  test_err={test_err:.3f}")
```

Vas a observar el mismo patrón cualitativo de la tabla del PDF: train error de 0 en k=1 y caída del test error hasta cierto $k$ óptimo, después subida.

---

## 5. Conexión con el TP

> **TP1 (regresión polinomial / lineal) no toca KNN.** KNN entra en el **TP2**, junto con NB y regresión logística, como parte de la comparativa de clasificadores.

Cuando llegue ese TP, vas a tener que:

1. **Estandarizar** las features antes de KNN (`StandardScaler` dentro de un `Pipeline`).
2. **Tunear `n_neighbors`** vía `GridSearchCV` con un rango como `{1, 3, 5, 7, 11, 15, 21, 31}`.
3. **Probar `weights='uniform'` vs `weights='distance'`** y reportar cuál mejora.
4. **Comparar con Naive Bayes y regresión logística** sobre el mismo dataset.
5. **Reportar tiempos de fit y predict** — KNN se entrena rapidísimo pero predice lento; los otros, al revés. Esto es parte del análisis.
6. **No usar KNN con features categóricas codificadas como one-hot sin pensar la métrica** — la euclidiana entre vectores one-hot no captura semántica. Pensar en Hamming o coseno.

**Mapa mental para el TP2:**

| Si... | Probá... |
|---|---|
| Features mixtas (numéricas + cats) | Tipo de pre-procesado adecuado + logística como baseline |
| Dataset chico (< 5000) y baja dimensión | KNN suele competir bien |
| Dataset grande con features de texto | NB Multinomial gana en tiempo |
| Necesitás interpretabilidad de coeficientes | Logística |
| Necesitás fronteras no lineales sin tunear redes | KNN con $k$ apropiado |

---

## 6. Errores comunes

### 6.1. Usar KNN sin escalar

**Síntoma:** accuracy mucho peor que logística en el mismo dataset. Features de escalas dispares.

**Causa:** las distancias están dominadas por la feature de mayor varianza absoluta.

**Fix:** `StandardScaler` o `MinMaxScaler` dentro de un `Pipeline`.

### 6.2. Aplicar `StandardScaler` al test con `fit_transform`

**Síntoma:** accuracy en test sospechosamente alta.

**Causa:** el scaler usó estadísticos del test (data leakage).

**Fix:** `fit` solo en train; `transform` en test. O mejor: `Pipeline`.

### 6.3. Elegir k par en clasificación binaria

**Síntoma:** comportamiento inconsistente cerca de la frontera.

**Causa:** empates en la votación. Sklearn rompe empates por el orden de los datos — frágil.

**Fix:** usar $k$ **impar** para binaria, o `weights='distance'` para que empates se decidan por proximidad.

### 6.4. Aplicar KNN en 500 dimensiones sin reducción previa

**Síntoma:** KNN ofrece poco mejor que predecir la clase mayoritaria. Test error alto y plano respecto a $k$.

**Causa:** curse of dimensionality. Todos los puntos están aprox. equidistantes.

**Fix:** reducir dimensionalidad (PCA, UMAP) o usar embeddings densos antes.

### 6.5. Olvidar que KNN es lento en predicción

**Síntoma:** entrenás rapidísimo, después en producción cada query tarda segundos.

**Causa:** brute force con $m$ grande. Sklearn intenta usar KD-tree por default pero con n > 30 vuelve a brute.

**Fix:** ANN (Faiss, Annoy, HNSW) o reducir $m$ con prototipos.

### 6.6. Comparar KNN con árboles sin estandarizar

**Síntoma:** "los árboles aplastan a KNN, descarto KNN".

**Causa:** árboles son **invariantes a escala** (parten por umbrales en features sueltas). KNN no. Comparación injusta sin escalar.

**Fix:** estandarizar antes de KNN. Después comparar.

### 6.7. Asumir que k=1 nunca es buena idea

**Contraejemplo:** en algunos datasets con clases muy separadas y poco ruido, k=1 es competitivo. Y k=1 sigue siendo asintóticamente acotado por el doble del error de Bayes (Cover & Hart). No es **siempre** el peor; es **frecuentemente** el peor cuando hay ruido.

### 6.8. Usar `KNeighborsClassifier` con datos imbalanceados sin cuidado

**Síntoma:** KNN predice casi siempre la clase mayoritaria.

**Causa:** entre los $k$ vecinos de cualquier punto, la clase mayoritaria del dataset domina.

**Fix:** `weights='distance'`, ajustar $k$, o resamplear (SMOTE, oversampling, undersampling).

---

## 7. Checklist

- [ ] Sé enunciar la definición precisa de paramétrico vs no paramétrico (tamaño de parámetros vs tamaño de datos).
- [ ] Puedo escribir el algoritmo de KNN paso a paso.
- [ ] Sé calcular a mano la predicción de KNN para un punto con $k$ chico.
- [ ] Entiendo por qué hay que escalar features antes de KNN — y puedo dar un ejemplo donde sin escalar la cuenta sale mal.
- [ ] Sé qué pasa con $k = 1$: train error 0, overfitting.
- [ ] Sé qué pasa con $k$ muy grande: predicción colapsa a la clase mayoritaria.
- [ ] Conozco al menos 4 métricas de distancia y cuándo usar cada una.
- [ ] Puedo explicar el curse of dimensionality en una oración y dar la intuición geométrica.
- [ ] Sé qué hacen KD-tree y ball tree, y cuándo conviene cada una.
- [ ] Conozco la cota asintótica de Cover & Hart (1967): $R_{1\text{NN}} \leq 2 R^*$.
- [ ] Sé construir un `Pipeline` con `StandardScaler` + `KNeighborsClassifier`.
- [ ] Reconozco que KNN tiene costo en **predicción**, no en entrenamiento (al revés de logística / NB).

---

## 8. Para profundizar

### 8.1. Lecturas obligadas

- **Hastie, Tibshirani & Friedman, *The Elements of Statistical Learning* (ESL), §13** — "Prototype Methods and Nearest-Neighbors". El tratamiento más detallado de KNN, sus variantes (Learning Vector Quantization, K-means classification, Adaptive Nearest Neighbors), y el análisis de bias-variance en función de $k$. Descarga gratuita en https://hastie.su.domains/ElemStatLearn/
- **Bishop, *PRML* §2.5** — "Nonparametric Methods" (estimación de densidad por histogramas, kernel density estimation, KNN density). §2.5.2 específicamente cubre KNN como estimador de densidad.
- **Murphy, *Probabilistic Machine Learning: An Introduction* §16** — "Exemplar-based methods". Tratamiento moderno con conexiones a métodos de kernel y embeddings.

### 8.2. Papers fundacionales

- **Cover, T., & Hart, P. (1967)** — "Nearest neighbor pattern classification". *IEEE Transactions on Information Theory*, 13(1), 21-27. DOI: [10.1109/TIT.1967.1053964](https://doi.org/10.1109/TIT.1967.1053964). PDF disponible en: https://isl.stanford.edu/~cover/papers/transIT/0021cove.pdf. **Imprescindible**: la cota $R_{1\text{NN}} \leq 2 R^*$ se demuestra acá.
- **Fix, E., & Hodges, J. L. (1951)** — "Discriminatory Analysis: Nonparametric Discrimination: Consistency Properties". El paper que **introdujo** el método de vecinos más cercanos, dieciséis años antes de Cover & Hart.
- **Weinberger, K. Q., & Saul, L. K. (2009)** — "Distance Metric Learning for Large Margin Nearest Neighbor Classification". JMLR. Aprender la métrica desde los datos.

### 8.3. Documentación de sklearn

- `KNeighborsClassifier`: https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html
- Módulo Nearest Neighbors (overview, KD-tree, Ball tree): https://scikit-learn.org/stable/modules/neighbors.html
- `BallTree`: https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.BallTree.html
- `KDTree`: https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KDTree.html

### 8.4. Bibliotecas de Approximate Nearest Neighbors (para producción)

- **FAISS** (Facebook AI Research) — la biblioteca de referencia para búsqueda ANN a escala. https://github.com/facebookresearch/faiss
- **HNSW** (Hierarchical Navigable Small World) — algoritmo grafo-basado, state of the art en muchos benchmarks.
- **Annoy** (Spotify) — más simple, basado en árboles aleatorios.
- **ScaNN** (Google Research) — competitivo con FAISS, soporta cuantización avanzada.

### 8.5. Conexión con otros métodos

- **Kernel methods** y **SVMs**: KNN puede verse como un kernel "indicador" sobre los $k$ vecinos. Murphy §17 cruza ambos mundos.
- **Procesos Gaussianos**: otra forma de regresión / clasificación no paramétrica, con incertidumbre cuantificada.
- **Sistemas de recomendación item-based**: KNN sobre embeddings de items.
- **Few-shot learning / Prototypical Networks**: KNN sobre representaciones aprendidas con redes neuronales.

---

## Próximo paso

→ [10-multiclase.md](10-multiclase.md) — Estrategias multiclase (OVA, OVO y softmax) y por qué algunas familias de modelos (KNN, NB) son **naturalmente multiclase** mientras otras (SVM, logística binaria) requieren wrappers explícitos.

---

## Referencias

### Material de cátedra
- PDF Clase 2 (DiploDatos UNC 2026), p. 26–34 — Bloque K-NN.
- (No hay notebook acompañante de KNN en la Clase 2; aparece como demostración conceptual.)

### Bibliografía canónica
- Hastie, T., Tibshirani, R., & Friedman, J. (2009). *The Elements of Statistical Learning* (2nd ed.), Springer. Cap. 13 (Prototype Methods and Nearest-Neighbors). Online: https://hastie.su.domains/ElemStatLearn/
- Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*, Springer. §2.5 (Nonparametric Methods) y §2.5.2 (Nearest-Neighbour Methods).
- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*, MIT Press. Cap. 16 (Exemplar-based methods).

### Papers
- Cover, T., & Hart, P. (1967). "Nearest neighbor pattern classification". *IEEE Transactions on Information Theory*, 13(1), 21-27. DOI: [10.1109/TIT.1967.1053964](https://doi.org/10.1109/TIT.1967.1053964). PDF: https://isl.stanford.edu/~cover/papers/transIT/0021cove.pdf
- Fix, E., & Hodges, J. L. (1951). "Discriminatory Analysis: Nonparametric Discrimination: Consistency Properties". USAF School of Aviation Medicine, Technical Report 4.

### Documentación sklearn
- `KNeighborsClassifier`: https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html
- Nearest Neighbors (overview): https://scikit-learn.org/stable/modules/neighbors.html
- `BallTree`: https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.BallTree.html
