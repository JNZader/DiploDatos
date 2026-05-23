# 10 — Multiclase: estrategias y softmax

> Clase 2 — DiploDatos UNC 2026
> Material fuente: PDF clase 2, p. 35–43 (bloque multiclase) + Notebook 03 (softmax con digits).
> Pre-requisitos: cap. 06 (regresión logística binaria), cap. 07 (multiclase con logística + softmax), cap. 08 (Naive Bayes), cap. 09 (KNN).

---

## 1. Concepto

Hasta acá vimos modelos pensados originalmente para **clasificación binaria** (perceptrón, regresión logística) y otros que ya manejaban múltiples clases naturalmente (Naive Bayes, KNN). Cuando tenés un problema con $K > 2$ clases, hay tres maneras canónicas de resolverlo:

| Estrategia | Cómo opera | Cantidad de modelos | Tipo |
|---|---|---|---|
| **OVA / One-vs-All / One-vs-Rest** | Para cada clase, entrena un clasificador binario clase-vs-resto | $K$ | Wrapper (envuelve binarios) |
| **AVA / OVO / One-vs-One** | Para cada par de clases, entrena un clasificador binario clase-vs-clase | $K(K-1)/2$ | Wrapper |
| **Softmax / Multinomial Logistic** | Un único modelo con $K$ salidas que suman 1 | 1 | Nativo multiclase |

Y antes que nada, una distinción que se confunde feo:

| Problema | Descripción | Ejemplo |
|---|---|---|
| **Binaria** | $y \in \{0, 1\}$ | Spam / No spam |
| **Multiclase** (single-label) | $y \in \{1, \dots, K\}$, **exactamente una clase por instancia** | Dígito 0–9; flor iris setosa/versicolor/virginica |
| **Multietiqueta** (multi-label) | $\mathbf{y} \in \{0, 1\}^K$, **cero o más clases por instancia** | Tags en una foto (gato Y pájaro Y árbol); géneros de una película |

> Confusión típica: la cátedra (PDF p. 36) llama "Perro / Caballo / Pez / Pájaro" a un ejemplo multiclase. Si la imagen tiene **un solo animal**, es multiclase. Si puede haber un gato Y un pájaro en la misma foto, ya es multietiqueta — y se trata distinto.

Este capítulo se enfoca en **multiclase mutuamente excluyente**. Multietiqueta se tipifica como "$K$ problemas binarios independientes" (binary relevance) y se aborda por separado.

---

## 2. Intuición

### 2.1. Por qué hay tres estrategias y no una sola

Algunos modelos están naturalmente diseñados para una decisión binaria (un score, un umbral, un sí/no). Para usarlos en multiclase necesitás **un wrapper** que combine múltiples binarios — OVA o AVA.

Otros modelos generalizan de manera nativa: Naive Bayes calcula $P(y=c\mid \mathbf{x})$ para cualquier número de clases sin esfuerzo extra; KNN cuenta votos entre vecinos sin importarle cuántas clases hay. La regresión logística también tiene una generalización **principled**: softmax.

### 2.2. La metáfora de los torneos

- **OVA** es como un **torneo de "yo contra todos"**. Cada candidato se postula y los demás son sus rivales colectivos. Gana quien obtiene el mayor puntaje individual. **Riesgo**: dos candidatos pueden creer ambos que ganaron — y no hay tie-break formal.

- **AVA** es como un **torneo todos-contra-todos** (round-robin de fútbol). Cada par juega un partido. Gana quien acumula más victorias. **Costo**: con 32 equipos hay $32 \cdot 31 / 2 = 496$ partidos.

- **Softmax** es como una **votación con porcentajes coherentes**: el sistema garantiza que las probabilidades sumen 100 % y se reparten entre todas las opciones de manera lógica.

### 2.3. Por qué softmax es "más elegante"

> "A diferencia de OVA, Softmax garantiza que las probabilidades sean coherentes y mutuamente excluyentes." (cátedra, PDF p. 43)

OVA y AVA combinan modelos entrenados por separado. Cada modelo "no sabe" de la existencia de los otros. Eso lleva a regiones del espacio donde dos clasificadores dicen "yo soy positivo" simultáneamente — y a probabilidades que no suman 1 sin hacks de normalización ad-hoc.

Softmax resuelve esto desde el diseño: un único modelo con $K$ salidas vinculadas por la función exponencial-normalizada. Las decisiones son intrínsecamente excluyentes.

### 2.4. La conexión con la sigmoide

> "La sigmoide es, en cierto sentido, el caso especial binario de softmax." (notebook 03 celda 58)

Con $K = 2$, softmax colapsa exactamente a la sigmoide. Por eso decimos que **softmax es la extensión coherente de la regresión logística binaria**. No es una herramienta nueva — es la misma idea generalizada (ver cap. 07 para la derivación detallada).

---

## 3. Cuerpo técnico

### 3.1. One-vs-All (OVA, también One-vs-Rest)

**Setup:**
- Para cada clase $k \in \{1, \dots, K\}$, entrenar un clasificador binario $f_k$ donde:
  - **Positivos:** los ejemplos con $y = k$.
  - **Negativos:** todos los demás (ejemplos con $y \neq k$).
- Cada $f_k$ devuelve un score (o probabilidad) $f_k(\mathbf{x}) \in \mathbb{R}$ (o en $[0, 1]$).

**Regla de decisión — Winner Takes All:**

$$
\hat{y}(\mathbf{x}) \;=\; \arg\max_{k \in \{1,\dots,K\}} f_k(\mathbf{x})
$$

> Ejemplo cátedra (PDF p. 38) — clasificar imagen:
>
> | Clasificador | Score | Interpretación |
> |---|---|---|
> | Avión vs Resto | 0.80 | **GANADOR** |
> | Camión vs Resto | 0.65 | Posible |
> | Barco vs Resto | 0.20 | Poco probable |
> | Auto vs Resto | 0.31 | Posible |
>
> Predicción: Avión (mayor score).

**Costo computacional:** $O(K)$ modelos entrenados.

**Problemas conocidos:**
- **Imbalance inducido**: cada clasificador binario ve una clase "positiva" minoritaria (1 de $K$ partes) y "negativa" mayoritaria ($(K-1)/K$ partes). Sin pesado o `class_weight='balanced'`, esto puede degradar la calidad.
- **Regiones ambiguas**: en algunos puntos, **varios clasificadores predicen positivo**. La regla `argmax` rompe empates por score, pero si los scores no son comparables entre clasificadores, la decisión final puede ser incoherente.
- **Probabilidades inconsistentes**: $\sum_k f_k(\mathbf{x}) \neq 1$ en general. Hay que normalizar a mano si querés interpretar probabilidades.

**Cuándo usar:**
- El clasificador base es naturalmente binario (perceptrón, SVM binaria sin extensión nativa).
- $K$ es moderado (< 50) y querés rapidez de entrenamiento.
- Tenés un baseline rápido y simple antes de pasar a algo más sofisticado.

**Sklearn:** `OneVsRestClassifier(base_estimator)` envuelve cualquier clasificador binario y entrena $K$ copias. Doc: https://scikit-learn.org/stable/modules/generated/sklearn.multiclass.OneVsRestClassifier.html

```python
from sklearn.svm import LinearSVC
from sklearn.multiclass import OneVsRestClassifier
ovr = OneVsRestClassifier(LinearSVC(random_state=0))
ovr.fit(X_train, y_train)
ovr.predict(X_test)
```

> Nota: `OneVsRestClassifier` también sirve para **multietiqueta** si pasás `y` como matriz binaria 2D — la cátedra no profundiza ahí.

### 3.2. One-vs-One (AVA / OVO)

**Setup:**
- Para cada par no ordenado $(i, j)$ con $i < j$, entrenar un clasificador binario $f_{ij}$ que distingue clase $i$ de clase $j$.
- **Cada $f_{ij}$ solo ve los ejemplos de las clases $i$ y $j$** (descarta el resto del training set).
- Total: $\binom{K}{2} = K(K-1)/2$ clasificadores.

**Regla de decisión — Votación:**

$$
\hat{y}(\mathbf{x}) \;=\; \arg\max_{k \in \{1,\dots,K\}} \text{votos}(k)
$$

donde $\text{votos}(k) = \sum_{j \neq k} \mathbb{1}\{f_{kj}(\mathbf{x}) = k\}$ (el número de partidos que ganó la clase $k$).

> Ejemplo cátedra (PDF p. 41) — clasificar entre Avión / Auto / Bus:
>
> | Clasificador | Voto | Confianza |
> |---|---|---|
> | Avión vs Auto | Avión | 0.82 |
> | Avión vs Bus | Avión | 0.76 |
> | Auto vs Bus | Auto | 0.61 |
>
> Votos: Avión=2, Auto=1, Bus=0 → predice **Avión** (2 de 3 partidos).

**Costo computacional:**
- Cantidad de modelos: $O(K^2)$ — escala mal en $K$ grande.
- **Pero** cada modelo se entrena con menos datos (solo dos clases), así que cada `fit` individual es más rápido. Para algoritmos con costo super-lineal en $m$ (kernel SVM en particular), AVA puede ser **más rápido en total** que OVA.

**Ventajas:**
- Cada problema binario es **balanceado por construcción** (asumiendo clases relativamente balanceadas en el dataset original).
- Los modelos individuales son más simples (frontera entre solo dos clases) → mejor capacidad de discriminación local.

**Desventajas:**
- $O(K^2)$ no escala a clases enormes (ej: ImageNet con 1000 clases ⇒ casi 500.000 clasificadores).
- Empates en votos posibles — sklearn los rompe agregando los scores brutos como tie-breaker.

**Cuándo usar:**
- Tu clasificador base escala mal con $m$ (kernel SVM).
- $K$ es moderado-bajo (3–20 clases).
- Tenés clases con cantidades muy distintas y querés evitar el imbalance que induce OVA.

**Sklearn:** `OneVsOneClassifier(base_estimator)`. Doc: https://scikit-learn.org/stable/modules/generated/sklearn.multiclass.OneVsOneClassifier.html

```python
from sklearn.svm import SVC
from sklearn.multiclass import OneVsOneClassifier
ovo = OneVsOneClassifier(SVC(kernel='rbf'))
ovo.fit(X_train, y_train)
```

### 3.3. Softmax / Multinomial Logistic Regression — el camino directo

La generalización **natural** de la regresión logística binaria a $K$ clases. No es un wrapper; es un único modelo con $K$ salidas.

**Función softmax:**

$$
P(Y = k \mid \mathbf{x}; \boldsymbol{\Theta}) \;=\; \frac{\exp(\boldsymbol{\theta}_k^{T} \mathbf{x})}{\sum_{j=1}^{K} \exp(\boldsymbol{\theta}_j^{T} \mathbf{x})}
$$

donde $\boldsymbol{\Theta} = (\boldsymbol{\theta}_1, \dots, \boldsymbol{\theta}_K)$ es una matriz de pesos: una fila por clase, una columna por feature.

**Propiedades clave:**
- $P(Y = k \mid \mathbf{x}) \in (0, 1)$ — cada probabilidad es positiva y menor que 1.
- $\sum_{k=1}^{K} P(Y = k \mid \mathbf{x}) = 1$ — distribución de probabilidad válida.
- La función es **invariante a traslaciones** del vector de scores: $\text{softmax}(\mathbf{z} + c\mathbf{1}) = \text{softmax}(\mathbf{z})$ para cualquier escalar $c$. Por eso una de las filas $\boldsymbol{\theta}_k$ puede fijarse a cero sin perder generalidad (lo que reduce la cantidad de parámetros libres a $(K-1) \times n$, aunque sklearn por simplicidad mantiene $K$ filas).

**Regla de decisión:**

$$
\hat{y}(\mathbf{x}) \;=\; \arg\max_{k} P(Y = k \mid \mathbf{x}) \;=\; \arg\max_{k} \boldsymbol{\theta}_k^T \mathbf{x}
$$

(El argmax se preserva sobre los scores lineales sin necesidad de aplicar el exponencial — solo necesitás softmax si querés interpretar probabilidades.)

**Flujo conceptual (notebook 03 celda 58):**
1. Para cada muestra $\mathbf{x}$, calcular un **score lineal por clase**: $z_k = \mathbf{w}_k \cdot \mathbf{x} + b_k$.
2. Los $z_k$ **no son probabilidades** todavía.
3. Exponenciar y normalizar: $p_k = e^{z_k} / \sum_j e^{z_j}$.
4. Predicción: $\hat{y} = \arg\max_k p_k$.

**Estabilidad numérica — log-sum-exp trick:** $\exp(z_k)$ explota numéricamente para $z_k$ grandes. La implementación canónica resta primero $\max_k z_k$:

$$
\text{softmax}(\mathbf{z})_k \;=\; \frac{\exp(z_k - \max_j z_j)}{\sum_i \exp(z_i - \max_j z_j)}
$$

Resultado matemáticamente idéntico, numéricamente estable. Sklearn lo hace internamente.

### 3.4. Cross-entropy multiclase — la función de costo

Generalización de la log-loss binaria a $K$ clases:

$$
J(\boldsymbol{\Theta}) \;=\; -\frac{1}{m} \sum_{i=1}^{m} \sum_{k=1}^{K} \mathbb{1}\{y^{(i)} = k\} \cdot \log P(Y = k \mid \mathbf{x}^{(i)})
$$

Equivalente compacto con **one-hot encoding** $\mathbf{y}^{(i)}$ (vector de ceros con un 1 en la clase verdadera):

$$
J(\boldsymbol{\Theta}) \;=\; -\frac{1}{m} \sum_{i=1}^{m} \sum_{k=1}^{K} y_k^{(i)} \log \hat{p}_k^{(i)}
$$

**Por qué cross-entropy y no MSE:** mismas razones que en logística binaria (cap. 06):
1. **Convexa** en los parámetros bajo la función softmax — gradient descent converge al mínimo global.
2. **Gradientes saludables** en toda la curva — no hay saturación cerca de los extremos.

**Gradiente** (útil para entender SGD y backprop):

$$
\frac{\partial J}{\partial \boldsymbol{\theta}_k} \;=\; \frac{1}{m} \sum_{i=1}^{m} (\hat{p}_k^{(i)} - y_k^{(i)})\, \mathbf{x}^{(i)}
$$

Es decir: "predicción menos verdad, multiplicado por la entrada". Misma forma que la regresión lineal y la logística binaria — y de hecho es la forma canónica de la familia de modelos lineales generalizados (GLM).

### 3.5. Comparativa OVA vs AVA vs Softmax

| Aspecto | OVA | AVA | Softmax |
|---|---|---|---|
| Cantidad de modelos | $K$ | $K(K-1)/2$ | 1 |
| Datos por modelo | todo | dos clases | todo |
| Balance por modelo | desbalanceado (1 vs $K-1$) | balanceado (1 vs 1) | balanceado global |
| Probabilidades coherentes | no (suman libre) | no (votación) | **sí** (suman 1) |
| Regiones ambiguas | sí | menos | no |
| Escala a $K$ grande | razonable | malo (cuadrático) | excelente |
| Aplicable con base no probabilística | sí | sí | no (requiere extensión nativa) |
| Cuándo usar | base binaria genérica, $K$ medio | base con costo super-lineal en $m$, $K$ chico | si el base lo soporta, casi siempre |

### 3.6. ¿Cuándo NO podés usar softmax?

Necesitás que el clasificador base soporte la formulación multinomial. SVM clásico NO lo soporta (es un clasificador binario por diseño, basado en márgenes); por eso sklearn usa OVA/AVA por default en `SVC` multiclase. Lo mismo con perceptrón y algunos métodos basados en kernels.

Los modelos que sí soportan softmax nativo:
- **Regresión logística multinomial** (`LogisticRegression(multi_class='multinomial')` — default desde sklearn 0.22).
- **Redes neuronales** (capa final softmax).
- **Naive Bayes** (calcula $P(y=k\mid\mathbf{x})$ para todo $k$ por diseño — ¡no necesita wrapper!).
- **KNN** (calcula votación entre todas las clases — tampoco necesita wrapper).
- **Árboles de decisión / Random Forest / Gradient Boosting** — manejan multiclase nativamente (no via softmax, sino via splits que pueden separar múltiples clases).

### 3.7. Conexión con capítulos anteriores

**Cap. 07 — Regresión logística multiclase:** la regresión logística binaria con sigmoide es exactamente softmax para $K = 2$. La fórmula

$$
\sigma(z) = \frac{1}{1 + e^{-z}} = \frac{e^z}{e^z + 1}
$$

es softmax con $z_1 = z$ y $z_2 = 0$. Por eso "la sigmoide es el caso especial binario de softmax".

**Cap. 08 — Naive Bayes:** ya es **naturalmente multiclase**. Calculás $P(y=k)\prod_j P(x_j\mid y=k)$ para cada $k$ y hacés argmax. No necesitás OVA / OVO / softmax.

**Cap. 09 — KNN:** también **naturalmente multiclase**. Contás votos entre los $k$ vecinos. Si hay 100 clases y los 5 vecinos votan {3, 7, 7, 12, 7}, predecís 7. Sin wrapper.

### 3.8. En sklearn — el caso de `LogisticRegression`

`LogisticRegression` desde sklearn 0.22 elige el solver y el modo multiclase de forma automática:

- **`multi_class='auto'`** (default): elige `'multinomial'` si el solver lo soporta y hay más de 2 clases, sino `'ovr'`.
- **`multi_class='multinomial'`**: softmax cross-entropy.
- **`multi_class='ovr'`**: One-vs-Rest manual.

```python
from sklearn.linear_model import LogisticRegression
clf = LogisticRegression(multi_class='multinomial', solver='lbfgs', max_iter=200)
clf.fit(X_train, y_train)

clf.coef_.shape         # (K, n_features) — una fila por clase
clf.intercept_.shape    # (K,)
clf.predict_proba(X)    # matriz (n_samples, K) — filas que suman 1
clf.classes_            # array con el orden de las clases
```

**Equivalencia con cálculo manual:**

```python
scores = X @ clf.coef_.T + clf.intercept_   # (n_samples, K) — los z_k
probs = np.exp(scores) / np.exp(scores).sum(axis=1, keepdims=True)
# probs == clf.predict_proba(X)   (módulo precisión flotante)
```

### 3.9. Estrategias para multietiqueta — fuera del scope pero importante

Si el problema es multietiqueta (cada instancia puede tener 0+ etiquetas):

- **Binary Relevance**: entrenar $K$ clasificadores binarios independientes (uno por etiqueta). Es exactamente OVA, pero **sin** la regla de winner-takes-all — cada clasificador predice independientemente.
- **Classifier Chains**: orden secuencial donde cada clasificador usa las predicciones de los anteriores como features.
- **Label Powerset**: tratar cada combinación de etiquetas como una clase nueva — explota combinatoriamente.

En sklearn: `MultiOutputClassifier`, `ClassifierChain`. No se cubre en esta clase; mencionarlo para no confundir con multiclase puro.

---

## 4. Ejemplo numérico

### 4.1. Softmax sobre dígito '3' (PDF p. 43)

Un clasificador softmax con 10 clases entrenado sobre `load_digits` produce, para una imagen del dígito `3`:

| Dígito | Score lineal $z_k$ | $e^{z_k}$ | $p_k = e^{z_k} / \sum$ |
|---|---|---|---|
| 0 | -2.5 | 0.082 | 0.01 |
| 1 | -1.8 | 0.165 | 0.02 |
| 2 | -1.1 | 0.332 | 0.04 |
| **3** | **+1.9** | **6.685** | **0.87** |
| 4 | -1.8 | 0.165 | 0.02 |
| 5 | -2.5 | 0.082 | 0.01 |
| 6 | -2.5 | 0.082 | 0.01 |
| 7 | -2.5 | 0.082 | 0.01 |
| 8 | -∞ | ~0 | 0.00 |
| 9 | -2.5 | 0.082 | 0.01 |
| **Σ** | | **7.757** | **1.00** |

(Los scores son ilustrativos; reproducen las probabilidades del PDF.)

Predicción: $\arg\max_k p_k = 3$.

### 4.2. Ejemplo OVA — tres clases en 2D

Dataset toy: tres puntos por clase, 2D.

| Clase A | Clase B | Clase C |
|---|---|---|
| (1, 1) | (5, 1) | (3, 5) |
| (1, 2) | (5, 2) | (3, 6) |
| (2, 1) | (6, 1) | (4, 5) |

Entrenando regresión logística OVA, obtenemos 3 clasificadores binarios:
- $f_A$: A vs {B, C}.
- $f_B$: B vs {A, C}.
- $f_C$: C vs {A, B}.

Para el punto $\mathbf{x}^* = (3, 3)$ (en el medio del triángulo):
- $f_A(\mathbf{x}^*) = 0.35$ (poco probable que sea A).
- $f_B(\mathbf{x}^*) = 0.38$ (poco probable que sea B).
- $f_C(\mathbf{x}^*) = 0.42$ (un poco más probable que sea C).

OVA predice **C** porque tiene el mayor score, pero las probabilidades suman 1.15 (¡más que 1!). Si querés "probabilidades" coherentes, hay que normalizar a posteriori — y aún así no son tan principled como las de softmax.

### 4.3. Mismo ejemplo con AVA

Tres clasificadores binarios:
- $f_{AB}$: A vs B → mediatriz horizontal alrededor de $x_1 = 3.5$.
- $f_{AC}$: A vs C → mediatriz alrededor de $x_2 = 3.5$.
- $f_{BC}$: B vs C → diagonal alrededor de $x_1 + x_2 = 8$.

Para $\mathbf{x}^* = (3, 3)$:
- $f_{AB}(3, 3) = A$ ($x_1 < 3.5$).
- $f_{AC}(3, 3) = A$ ($x_2 < 3.5$).
- $f_{BC}(3, 3) = ?$ — el plano (3,3) está al sur-oeste de la diagonal $x_1 + x_2 = 8$, donde no hay puntos B ni C entrenando — la predicción es indefinida en esa zona, depende del clasificador.

Si $f_{BC}(3, 3) = B$: votos = {A: 2, B: 1, C: 0} → predice **A**.
Si $f_{BC}(3, 3) = C$: votos = {A: 2, B: 0, C: 1} → predice **A**.

AVA predice A — coherente porque (3,3) está más cerca del cluster A que del centro de B o C.

### 4.4. Mismo ejemplo con softmax

`LogisticRegression(multi_class='multinomial')` entrena un único modelo con matriz $\boldsymbol{\Theta} \in \mathbb{R}^{3 \times 2}$. Para $\mathbf{x}^* = (3, 3)$ produce algo como:
- $z_A = 0.5$, $z_B = -0.2$, $z_C = -0.3$.
- $p_A = 0.49$, $p_B = 0.26$, $p_C = 0.25$. (Σ = 1.00)

Predicción: **A** con 49 % de probabilidad. Las probabilidades suman exactamente 1 y reflejan la incertidumbre real del modelo en una zona ambigua.

### 4.5. En código

```python
import numpy as np
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

X, y = load_digits(return_X_y=True)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, train_size=0.8, random_state=0)

# Softmax (multinomial)
clf_sm = LogisticRegression(multi_class='multinomial', solver='lbfgs',
                             max_iter=200).fit(X_tr, y_tr)

# OVA (one-vs-rest)
clf_ovr = LogisticRegression(multi_class='ovr', solver='lbfgs',
                              max_iter=200).fit(X_tr, y_tr)

print(f"Softmax accuracy: {clf_sm.score(X_te, y_te):.3f}")
print(f"OVR accuracy:     {clf_ovr.score(X_te, y_te):.3f}")

# Verificar coherencia de probabilidades
np.allclose(clf_sm.predict_proba(X_te).sum(axis=1), 1.0)   # True
np.allclose(clf_ovr.predict_proba(X_te).sum(axis=1), 1.0)  # True (sklearn lo normaliza ad-hoc)

# Inspeccionar la matriz de pesos
clf_sm.coef_.shape       # (10, 64)
clf_sm.classes_          # array([0, 1, 2, ..., 9])
```

**Visualización de los pesos por clase como imagen** (notebook 03 celda 61):
```python
import matplotlib.pyplot as plt
fig, axes = plt.subplots(2, 5, figsize=(10, 4))
for k, ax in enumerate(axes.flat):
    ax.imshow(clf_sm.coef_[k].reshape(8, 8), cmap='seismic')
    ax.set_title(f'clase {k}')
    ax.axis('off')
```

Vas a ver que cada fila de `coef_` "se parece" al dígito que representa — píxeles positivos (rojos) son los que esa clase espera ver activos; píxeles negativos (azules) son los que la clase espera ver apagados.

---

## 5. Conexión con el TP

> **TP1 (regresión polinomial / lineal) no usa estrategias multiclase.** Las estrategias OVA / AVA / softmax aparecen explícitamente en el **TP2** (clasificación), cuando comparemos regresión logística, Naive Bayes y KNN sobre datasets multiclase.

En el TP2 esperá:

1. Cargar un dataset multiclase (`load_digits`, `load_iris`, `load_wine`, o uno propio).
2. **Verificar cuántas clases** tiene y si está balanceado (`Counter(y)`).
3. Entrenar al menos **dos modelos diferentes** sobre el mismo dataset:
   - Logística con `multi_class='multinomial'` (softmax) y comparar con `multi_class='ovr'`.
   - NB sobre el mismo dataset.
   - KNN sobre el mismo dataset (estandarizado).
4. **Reportar accuracy, matriz de confusión** (que se interpreta de forma específica en multiclase), y opcionalmente macro-F1 / micro-F1.
5. **Discutir cuándo conviene OVA vs softmax** en función del modelo base y del costo computacional.

**Lectura de matriz de confusión multiclase:** la diagonal es la cantidad de aciertos por clase. Los off-diagonal son las confusiones específicas — ej: "el modelo confunde 7's con 1's" se ve como un valor alto en la celda (7, 1).

**Trampas que el TP probablemente quiera detectar:**
- Si reportás solo accuracy en un dataset desbalanceado, podés engañarte: 95 % de accuracy puede ser "predice la clase mayoritaria siempre".
- Si las clases no están balanceadas, usá `class_weight='balanced'` y reportá métricas por clase.

---

## 6. Errores comunes

### 6.1. Confundir multiclase con multietiqueta

**Síntoma:** intentás usar `MultinomialNB` o `LogisticRegression(multi_class='multinomial')` con $y$ como matriz binaria 2D y explota.

**Causa:** softmax y NB están diseñados para asignar **exactamente una** clase. Si querés múltiples etiquetas por instancia, necesitás binary relevance, classifier chains, o `MultiOutputClassifier`.

**Fix:** identificar correctamente el tipo de problema **antes** de elegir el modelo. Si $y$ es 1D con valores categóricos → multiclase. Si $y$ es 2D binaria → multietiqueta.

### 6.2. Usar OVA cuando podés usar softmax nativo

**Síntoma:** entrenás `OneVsRestClassifier(LogisticRegression())` cuando `LogisticRegression(multi_class='multinomial')` haría el mismo trabajo más coherente.

**Causa:** confusión histórica — en sklearn < 0.22 el default era OVA.

**Fix:** verificar la versión de sklearn y usar softmax si el modelo lo soporta. OVA solo si el base es genuinamente binario sin extensión nativa.

### 6.3. Normalizar las probabilidades de OVA y llamarlas "probabilidades"

**Síntoma:** reportás "probabilidades calibradas" usando $p_k / \sum p_j$ tras OVA.

**Causa:** intuición. Pero esos números no provienen de un modelo probabilístico coherente — son normalización ad-hoc.

**Fix:** si necesitás probabilidades reales, usá softmax o `CalibratedClassifierCV`.

### 6.4. Asumir que softmax + cross-entropy soluciona el desbalance de clases

**Síntoma:** softmax acertás 95 % en accuracy en un dataset con 95 % de la clase mayoritaria, pero los recall de las clases minoritarias son malos.

**Causa:** softmax minimiza el error de clasificación promedio, no balanceado por clase.

**Fix:** `class_weight='balanced'`, o métricas por clase (macro-F1, balanced accuracy).

### 6.5. Olvidar que sklearn requiere `y` con valores enteros o strings consistentes

**Síntoma:** error `Unknown label type: 'continuous-multioutput'` o similar.

**Causa:** $y$ tiene floats (ej: `[0.0, 1.0, 2.0]`) o un tipo inesperado.

**Fix:** `y.astype(int)` o `LabelEncoder().fit_transform(y)` antes de fit.

### 6.6. Mezclar OVA y AVA con clasificadores que ya son multiclase nativos

**Síntoma:** envolvés un `RandomForestClassifier` o `KNeighborsClassifier` con `OneVsRestClassifier` "por seguridad".

**Causa:** sobre-ingeniería.

**Fix:** los modelos basados en árboles, KNN y NB ya son multiclase nativos. No los envuelvas en wrappers innecesarios. Eso solo agrega costo y puede empeorar las métricas.

### 6.7. Comparar OVA contra softmax usando el "score" en lugar de las probabilidades

**Síntoma:** "OVA da scores más altos que softmax, entonces es más confiado".

**Causa:** los scores de OVA no están en $[0, 1]$ y no son comparables con las probabilidades de softmax.

**Fix:** comparar siempre mismo tipo de salida (`predict_proba` de ambos, o `decision_function` de ambos).

### 6.8. Aplicar AVA cuando $K$ es grande

**Síntoma:** ImageNet (1000 clases) tarda horas en `OneVsOneClassifier`.

**Causa:** $K(K-1)/2 \approx 500{,}000$ clasificadores.

**Fix:** softmax (con redes neuronales o logística multinomial). AVA escala mal y rara vez justifica el costo más allá de $K \approx 20$.

---

## 7. Checklist

- [ ] Sé distinguir binaria, multiclase y multietiqueta con un ejemplo de cada una.
- [ ] Puedo describir las tres estrategias OVA, AVA y softmax con sus pros y contras.
- [ ] Sé escribir la fórmula de softmax y demostrar que las salidas suman 1.
- [ ] Entiendo por qué la sigmoide es el caso especial $K=2$ de softmax.
- [ ] Puedo escribir la cross-entropy multiclase y explicar por qué se usa en vez de MSE.
- [ ] Sé que softmax requiere un modelo que soporte la formulación multinomial (logística sí, perceptrón clásico no).
- [ ] Sé que NB y KNN son **naturalmente multiclase** y no necesitan wrapper.
- [ ] Conozco `OneVsRestClassifier`, `OneVsOneClassifier` y `LogisticRegression(multi_class='multinomial')` en sklearn.
- [ ] Sé qué hace `clf.coef_` con shape `(K, n)` en logística multinomial.
- [ ] Reconozco cuándo OVA produce regiones ambiguas y cuándo softmax las elimina.
- [ ] Entiendo por qué AVA escala mal con $K$ grande ($O(K^2)$ modelos).
- [ ] Puedo calcular a mano una predicción softmax dados $K$ scores lineales.

---

## 8. Para profundizar

### 8.1. Lecturas obligadas

- **Bishop, *PRML* §4.3.4** — "Multiclass logistic regression". Derivación completa de softmax desde el principio de máxima verosimilitud, gradiente, y conexión con discriminant analysis.
- **Murphy, *Probabilistic Machine Learning: An Introduction* §10.3** — "Multiclass logistic regression". Tratamiento moderno con conexiones a redes neuronales.
- **Hastie, Tibshirani & Friedman, *ESL* §4.3** y §4.4 — Discriminant analysis y regresión logística multinomial. Cubre cuándo el supuesto gaussiano de LDA gana o pierde contra logística.

### 8.2. Documentación sklearn

- Multiclass and Multioutput Algorithms (overview): https://scikit-learn.org/stable/modules/multiclass.html
- `OneVsRestClassifier`: https://scikit-learn.org/stable/modules/generated/sklearn.multiclass.OneVsRestClassifier.html
- `OneVsOneClassifier`: https://scikit-learn.org/stable/modules/generated/sklearn.multiclass.OneVsOneClassifier.html
- `LogisticRegression` (con `multi_class`): https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html

### 8.3. Variantes y extensiones

- **Error-Correcting Output Codes (ECOC)** — Dietterich & Bakiri (1995). Generaliza OVA y AVA: cada clase se codifica como un vector binario, y se entrenan tantos clasificadores binarios como bits del código. Más robusto a errores individuales. En sklearn: `OutputCodeClassifier`.
- **Hierarchical softmax** — usado en NLP (word2vec) cuando $K$ es enorme (vocabulario de 100k+). Estructura las clases en un árbol binario y reduce el costo de $O(K)$ a $O(\log K)$.
- **Negative sampling** — alternativa a softmax cuando $K$ es enorme. Aproxima el gradiente muestreando un subconjunto pequeño de clases negativas en cada paso.

### 8.4. Calibración de probabilidades

- **Platt scaling** (logística sobre los scores) — útil para SVM.
- **Isotonic regression** — más flexible, no asume forma paramétrica.
- En sklearn: `CalibratedClassifierCV` con `method='sigmoid'` o `'isotonic'`.

### 8.5. Tema avanzado — Maximum Entropy

La regresión logística multinomial es exactamente el modelo de **maximum entropy** (MaxEnt) con feature functions lineales. Es decir, softmax es la distribución de probabilidad de **máxima entropía** que cumple ciertas restricciones (matching de momentos empíricos). Esta perspectiva conecta logística con information theory y aparece mucho en NLP clásico. Ver Berger, Della Pietra & Della Pietra (1996), "A Maximum Entropy Approach to Natural Language Processing".

---

## Próximo paso

→ [11-glosario.md](11-glosario.md)

---

## Referencias

### Material de cátedra
- PDF Clase 2 (DiploDatos UNC 2026), p. 35–43 — Bloque multiclase, OVA, AVA, softmax.
- Notebook 03 — Regresión logística multiclase sobre `load_digits`, celdas 58–95.

### Bibliografía canónica
- Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*, Springer. §4.3.4 (Multiclass logistic regression).
- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*, MIT Press. §10.3 (Multiclass logistic regression).
- Hastie, T., Tibshirani, R., & Friedman, J. (2009). *The Elements of Statistical Learning* (2nd ed.), Springer. §4.3 y §4.4. Online: https://hastie.su.domains/ElemStatLearn/

### Papers relacionados (extensiones)
- Dietterich, T. G., & Bakiri, G. (1995). "Solving Multiclass Learning Problems via Error-Correcting Output Codes". *Journal of Artificial Intelligence Research*, 2, 263-286.
- Berger, A. L., Della Pietra, S. A., & Della Pietra, V. J. (1996). "A Maximum Entropy Approach to Natural Language Processing". *Computational Linguistics*, 22(1), 39-71.

### Documentación sklearn
- Multiclass overview: https://scikit-learn.org/stable/modules/multiclass.html
- `OneVsRestClassifier`: https://scikit-learn.org/stable/modules/generated/sklearn.multiclass.OneVsRestClassifier.html
- `OneVsOneClassifier`: https://scikit-learn.org/stable/modules/generated/sklearn.multiclass.OneVsOneClassifier.html
- `LogisticRegression`: https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html
