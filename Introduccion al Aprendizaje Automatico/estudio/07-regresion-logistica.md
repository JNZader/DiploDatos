# 07 — Regresión Logística

> "El perceptrón decide de forma brusca; la regresión logística decide de forma suave y probabilística." — Cátedra, notebook 03 celda 2
>
> "Esta función es convexa bajo la sigmoide, garantizando que el gradiente descendente converge al mínimo global." — PDF Clase 2 p. 7

---

## 1. Concepto

**Regresión logística** es un modelo de **clasificación supervisada** (no es regresión, a pesar del nombre histórico) que estima la **probabilidad** $P(y=1\mid\mathbf{x})$. Toma un score lineal $\mathbf{w}^T\mathbf{x} + b$ y lo "comprime" a $(0, 1)$ usando la **función sigmoide**:

$$
P(y=1\mid\mathbf{x};\mathbf{w}, b) = \sigma(\mathbf{w}^T\mathbf{x} + b), \qquad \sigma(z) = \frac{1}{1 + e^{-z}}
$$

**Por qué importa.** Resuelve los tres defectos del perceptrón (cap. 06) de una vez:
1. **Da probabilidades** → permite hablar de incertidumbre.
2. **Loss convexa** (log-loss / cross-entropy) → siempre converge al mínimo global con GD.
3. **Diferenciable** → encaja en redes neuronales (una red binaria con una capa **es** una regresión logística).

Histórico: viene del lado de la estadística, no del ML. David Cox la formalizó en 1958 (*The Regression Analysis of Binary Sequences*) para bioensayos. Hoy es herramienta de cabecera en epidemiología, scoring crediticio y baseline ineludible en clasificación. Bishop §4.3, Murphy cap. 10, Hastie §4.4.

> **Convención de etiquetas:** volvemos a $y \in \{0, 1\}$ (no $\pm 1$). La interpretación probabilística requiere que $y$ sea Bernoulli, definida sobre $\{0, 1\}$.

---

## 2. Intuición

### 2.1. De la decisión dura al gradiente suave

El perceptrón usa $\text{sign}(\mathbf{w}^T\mathbf{x})$: salto brusco en cero, derivada cero casi en todas partes, **sin gradiente útil**.

La sigmoide $\sigma(z) = 1/(1+e^{-z})$ es la versión suave:
- En $z=0$ vale $0.5$ → umbral natural.
- $\sigma(z) \to 1$ cuando $z \to +\infty$; $\sigma(z) \to 0$ cuando $z \to -\infty$.
- **Diferenciable en todas partes**, con derivada $\sigma'(z) = \sigma(z)(1-\sigma(z))$.

Si $\text{sign}$ es un termostato bang-bang, la sigmoide es un dimmer: **qué tan encendido**, que es exactamente la probabilidad.

### 2.2. La moneda sesgada (Bernoulli) — PDF Clase 2 p. 6

Cada observación $y$ es como tirar **una moneda sesgada**, donde la probabilidad de "cara" (clase 1) **depende de $\mathbf{x}$**:
- $\mathbf{x}$ claramente positivo → $\sigma(\mathbf{w}^T\mathbf{x}) \approx 0.95$.
- $\mathbf{x}$ ambiguo → $\approx 0.5$.
- $\mathbf{x}$ claramente negativo → $\approx 0.05$.

Regresión logística = **aprender cómo el input controla la probabilidad de una moneda**.

### 2.3. Por qué NO usamos MSE (anticipo)

Es tentador usar $J_{\text{MSE}} = \frac{1}{N}\sum (\sigma(\mathbf{w}^T\mathbf{x}_i) - y_i)^2$. **No lo hagas.** Es **no convexo** combinado con la sigmoide y **el gradiente se satura**. La log-loss arregla ambas cosas (§3.4).

---

## 3. Cuerpo técnico

### 3.1. La sigmoide en detalle

$$
\sigma(z) = \frac{1}{1 + e^{-z}}
$$

| Propiedad | Valor |
|-----------|-------|
| Rango | $(0, 1)$ |
| $\sigma(0)$ | $0.5$ |
| Asíntotas | $\to 1$ en $+\infty$; $\to 0$ en $-\infty$ |
| Simetría | $\sigma(-z) = 1 - \sigma(z)$ |
| **Derivada** | $\sigma'(z) = \sigma(z)(1-\sigma(z))$ |

**La identidad de la derivada — la perla.** Si $p = \sigma(z)$, entonces $\sigma'(z) = p(1-p)$. Mucho más limpio que derivar con regla del cociente. Va a hacer que las cuentas del gradiente colapsen (§3.6).

### 3.2. Modelo

**Hipótesis** (notación cátedra):

$$
h_\theta(\mathbf{x}) = \sigma(\boldsymbol{\theta}^T\mathbf{x}) = P(y=1\mid\mathbf{x};\boldsymbol{\theta})
$$

con $\boldsymbol{\theta}$ absorbiendo el bias en $\theta_0$ (asumiendo $x_0 = 1$).

**Regla de decisión** (umbral 0.5):

$$
\hat{y} = \begin{cases} 1 & h_\theta(\mathbf{x}) \geq 0.5 \\ 0 & h_\theta(\mathbf{x}) < 0.5 \end{cases}
$$

Notar que $h_\theta \geq 0.5 \iff \boldsymbol{\theta}^T\mathbf{x} \geq 0$. **La frontera es lineal**, igual que el perceptrón. La diferencia está en lo que el modelo **dice** cerca de la frontera (los marca como inciertos en vez de empujarlos a un lado).

> **El umbral 0.5 NO es sagrado.** Para clases desbalanceadas o costos asimétricos (falso negativo en cáncer = catástrofe vs falso positivo = molestia), se ajusta el umbral. La logística da una probabilidad que permite esa decisión informada — el perceptrón **no puede**.

### 3.3. Log-odds (logit)

Despejá: $p = 1/(1+e^{-z}) \implies p/(1-p) = e^z$ ⇒

$$
\boxed{\log\frac{p}{1-p} = \boldsymbol{\theta}^T\mathbf{x}}
$$

Esta es la transformación **logit**. **Lo que modelamos linealmente NO es la probabilidad, sino el log-odds.**

**Interpretación de coeficientes.** Aumentar $x_j$ en una unidad multiplica la odds-ratio por $e^{\theta_j}$. Si $\theta_j = 0.7 \Rightarrow e^{0.7} \approx 2$ → cada unidad duplica la odds. Esto es lo que mantiene a la logística como modelo de cabecera en epidemiología, ciencias sociales y finanzas.

### 3.4. ¿Por qué NO MSE? (PDF Clase 2 p. 5)

Dos razones técnicas:

**(1) No convexidad.** $J_{\text{MSE}}$ compuesto con la sigmoide deforma la superficie de error de una parábola limpia ("cuenco verde") a una superficie "volcánica" con múltiples mínimos locales (PDF p. 5). Gradient descent puede quedar atrapado.

**(2) Saturación del gradiente.** El gradiente del MSE contiene el factor $\sigma'(z) = p(1-p)$, que vale 0 cuando $p \to 0$ o $p \to 1$. Es decir: **cuando el modelo está confiadamente equivocado, el gradiente se desvanece y el modelo deja de aprender exactamente cuando más necesita corregirse**. La saturación mata el entrenamiento.

**Solución:** usar cross-entropy. La derivamos a partir de la verosimilitud.

### 3.5. Derivación de la log-loss desde verosimilitud Bernoulli (PDF p. 6–7)

**Paso 1 — Modelo unificado.** $P(y=1\mid\mathbf{x}) = h_\theta(\mathbf{x})$, $P(y=0\mid\mathbf{x}) = 1 - h_\theta(\mathbf{x})$. Combinando:

$$
P(y\mid\mathbf{x};\boldsymbol{\theta}) = h_\theta(\mathbf{x})^y \cdot (1 - h_\theta(\mathbf{x}))^{1-y}
$$

Verificación: $y=1 \Rightarrow h^1(1-h)^0 = h$ ✓; $y=0 \Rightarrow h^0(1-h)^1 = 1-h$ ✓. Es **exactamente una Bernoulli** con parámetro $p = h_\theta(\mathbf{x})$.

**Paso 2 — Verosimilitud conjunta** (i.i.d.):

$$
L(\boldsymbol{\theta}) = \prod_{i=1}^N h_\theta(\mathbf{x}^{(i)})^{y^{(i)}} \cdot (1 - h_\theta(\mathbf{x}^{(i)}))^{1-y^{(i)}}
$$

**Paso 3 — Log-verosimilitud** (productos → sumas, evita underflow):

$$
\ell(\boldsymbol{\theta}) = \sum_{i=1}^N \left[y^{(i)}\log h_\theta(\mathbf{x}^{(i)}) + (1-y^{(i)})\log(1-h_\theta(\mathbf{x}^{(i)}))\right]
$$

**Paso 4 — Costo $J(\boldsymbol{\theta})$** (negativo de la log-verosimilitud, promediado):

$$
\boxed{J(\boldsymbol{\theta}) = -\frac{1}{N}\sum_{i=1}^N \left[y^{(i)}\log h_\theta(\mathbf{x}^{(i)}) + (1-y^{(i)})\log(1-h_\theta(\mathbf{x}^{(i)}))\right]}
$$

Es la **log-loss** (= **binary cross-entropy**). *"Convexa bajo la sigmoide, garantizando que el gradiente descendente converge al mínimo global"* (PDF p. 7).

**Por casos** (PDF p. 8–9):

$$
\text{cost}(h, y) = \begin{cases} -\log(h) & y = 1 \\ -\log(1-h) & y = 0 \end{cases}
$$

- $y=1$: si $h \to 1$ (correcto), $\to 0$. Si $h \to 0$ (incorrecto), $\to +\infty$.
- $y=0$: análogo. *"Mayores errores reciben mayores penalizaciones"* (literal cátedra).

### 3.6. Gradiente de la log-loss

Usando $\sigma'(z) = p(1-p)$, derivando $\log\sigma(\boldsymbol{\theta}^T\mathbf{x})$ y $\log(1-\sigma(\boldsymbol{\theta}^T\mathbf{x}))$, todo colapsa a:

$$
\boxed{\nabla_\theta J(\boldsymbol{\theta}) = \frac{1}{N}\sum_{i=1}^N \left(h_\theta(\mathbf{x}^{(i)}) - y^{(i)}\right)\mathbf{x}^{(i)}}
$$

**Compará con la regresión lineal:** $\nabla J_{\text{MSE}} = \frac{1}{N}\sum(\mathbf{w}^T\mathbf{x}^{(i)} - y^{(i)})\mathbf{x}^{(i)}$. **¡Es la misma forma!** Si entendiste el gradiente de MSE, ya entendiste el de log-loss.

**A diferencia del MSE compuesto con sigmoide, este gradiente NO se satura.** Si $y=1$ y $h \to 0$, el residuo $(h-y) \to -1$ y el gradiente sigue siendo grande → el modelo se sigue corrigiendo agresivamente. **Esa es la magia de la log-loss.**

**Update rule:** $\boldsymbol{\theta} \leftarrow \boldsymbol{\theta} - r \cdot \nabla J(\boldsymbol{\theta})$.

### 3.7. Regularización (PDF p. 10 + notebook 03 celda 36)

En sklearn `LogisticRegression`:

| Penalty | Fórmula | Efecto |
|---------|---------|--------|
| **L2 (default)** | $J + \frac{1}{2C}\Vert \boldsymbol{\theta}\Vert _2^2$ | Suaviza, achica coeficientes proporcionalmente. |
| **L1 (Lasso)** | $J + \frac{1}{C}\Vert \boldsymbol{\theta}\Vert _1$ | Lleva algunos $\theta_j$ a **cero exacto** → selección de features. |
| **elasticnet** | combinación L1+L2 (`l1_ratio`) | Balance. |
| **None** | sin reg. | Puede causar overfitting / inestabilidad numérica si los datos son separables. |

**Convención sklearn — atención.** El hiperparámetro $C$ es el **inverso** de la fuerza de regularización:

$$
C = \frac{1}{\lambda}
$$

- **$C$ grande** ($\to \infty$) → $\lambda \to 0$ → **poca penalización**.
- **$C$ chico** ($\to 0$) → $\lambda \to \infty$ → **mucha penalización**.

Es al revés de lo intuitivo, pero es la convención sklearn. **Memorizalo.** Grid search con `np.logspace(-4, 4, 9)` te cubre 8 órdenes.

*"La penalización actúa como una fuerza que evita que el modelo se vuelva demasiado extremo"* (notebook 03 celda 36).

**Detalle solver:** `'lbfgs'` (default), `'newton-cg'`, `'newton-cholesky'`, `'sag'` solo soportan **L2 o None**. Para L1 o elasticnet usar `'liblinear'` o `'saga'`.

### 3.8. Multiclase: Softmax (PDF p. 41–43)

Con $K$ clases generalizamos a softmax. Hay $K$ vectores $\boldsymbol{\theta}_1, \dots, \boldsymbol{\theta}_K$ y:

$$
P(Y=k\mid\mathbf{x};\boldsymbol{\Theta}) = \frac{e^{\boldsymbol{\theta}_k^T\mathbf{x}}}{\sum_{j=1}^K e^{\boldsymbol{\theta}_j^T\mathbf{x}}}
$$

**Propiedades:** $P \in (0,1)$, $\sum_k P = 1$, mutuamente excluyentes. **Decisión:** $\hat{y} = \arg\max_k P(Y=k\mid\mathbf{x})$.

*"La sigmoide es, en cierto sentido, el caso especial binario de softmax"* (notebook 03 celda 58). Para $K=2$:

$$
P(Y=1\mid\mathbf{x}) = \frac{e^{\boldsymbol{\theta}_1^T\mathbf{x}}}{e^{\boldsymbol{\theta}_0^T\mathbf{x}} + e^{\boldsymbol{\theta}_1^T\mathbf{x}}} = \sigma((\boldsymbol{\theta}_1 - \boldsymbol{\theta}_0)^T\mathbf{x})
$$

**Costo multiclase: cross-entropy categórica:**

$$
J(\boldsymbol{\Theta}) = -\frac{1}{N}\sum_{i=1}^N\sum_{k=1}^K \mathbb{1}\{y^{(i)} = k\}\log P(Y=k\mid\mathbf{x}^{(i)};\boldsymbol{\Theta})
$$

En la práctica, $y$ se codifica **one-hot** y se calcula producto interno.

> Los próximos capítulos cubren **estrategias alternativas multiclase** (OVA = One-vs-All, AVA = All-vs-All) cuando el modelo base es binario. Softmax tiene la ventaja de probabilidades coherentes que suman 1 — algo que OVA no garantiza.

### 3.9. sklearn: `linear_model.LogisticRegression`

```python
from sklearn.linear_model import LogisticRegression

model = LogisticRegression(
    penalty='l2', C=1.0,
    solver='lbfgs', max_iter=100,
    multi_class='auto', random_state=0,
)
model.fit(X_train, y_train)
model.predict(X_test); model.predict_proba(X_test); model.decision_function(X_test)
model.coef_, model.intercept_     # (K, n) y (K,)
```

**L-BFGS** = cuasi-Newton con memoria limitada (aproxima el Hessiano sin almacenarlo). Default desde sklearn 0.22.

---

## 4. Ejemplo numérico

### 4.1. Setup: dígitos manuscritos (notebook 03)

```python
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from collections import Counter

digits = load_digits()
X, y = digits.data, digits.target
print(X.shape, y.shape)      # (1797, 64) (1797,)
print(Counter(y))            # ~180 por clase, balanceado

X_train, X_val, y_train, y_val = train_test_split(
    X, y, train_size=0.8, random_state=0,
)
```

1797 imágenes 8×8 aplanadas a 64 features, 10 clases.

### 4.2. Entrenamiento

```python
model = LogisticRegression(max_iter=180)
model.fit(X_train, y_train)
```

Internamente: 10 clases → softmax (`multi_class='multinomial'` por default en versiones modernas), optimización con **L-BFGS** + `penalty='l2'`, `C=1.0`. Se ajustan **10 vectores** $\boldsymbol{\theta}_k \in \mathbb{R}^{64}$ + 10 biases.

### 4.3. Inspección

```python
model.classes_      # [0, 1, 2, ..., 9]
model.coef_.shape   # (10, 64) — fila = clase, columna = píxel
model.intercept_.shape  # (10,)
model.n_iter_
```

**Interpretación de `coef_`** (notebook celda 43): cada fila es una clase, cada columna un píxel; el valor indica cuánto contribuye ese píxel al score de esa clase.

**Visualizar pesos como imagen** (celda 61):

```python
import matplotlib.pyplot as plt
plt.imshow(model.coef_[3].reshape(8, 8), cmap="seismic")
plt.colorbar(); plt.title("Pesos para clase '3'")
```

Rojo intenso = píxeles que favorecen al "3"; azul = penalizan. Verás un patrón vagamente con forma de 3.

### 4.4. Predicción y probabilidades

```python
x = X_val[0].reshape(1, -1)
print(model.predict(x))           # [3]
print(model.predict_proba(x))     # vector de 10 probabilidades
```

Salida típica (PDF p. 43, dígito '3'):

| Clase | $P$ |
|-------|-----|
| 0 | 0.01 |
| 1 | 0.02 |
| 2 | 0.04 |
| **3** | **0.87 (predicción)** |
| 4 | 0.02 |
| ... | ... |
| Σ | 1.00 |

**Equivalencia score lineal ↔ logits** (celdas 89–90):

```python
print(model.decision_function(x))          # API sklearn
print(model.coef_.dot(x.T) + model.intercept_.reshape(-1, 1))   # manual
```

Coinciden exactamente. Aplicando softmax a los logits obtenés las probabilidades.

### 4.5. Evaluación

```python
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay
y_pred = model.predict(X_val)
print(accuracy_score(y_val, y_pred))    # típicamente ~0.96-0.97
cm = confusion_matrix(y_val, y_pred)
ConfusionMatrixDisplay(confusion_matrix=cm).plot(cmap="Blues")
```

### 4.6. Softmax "a mano" (ejercicio 1 del notebook)

Si los logits son $\mathbf{z} = (2.1, -0.5, 3.4, 1.2, 0.8)$:

```python
import numpy as np
z = np.array([2.1, -0.5, 3.4, 1.2, 0.8])
exp_z = np.exp(z)                     # [8.166, 0.607, 29.964, 3.320, 2.226]
softmax = exp_z / np.sum(exp_z)       # [0.187, 0.014, 0.685, 0.076, 0.051]
print(np.argmax(softmax))             # 2
```

**Truco de estabilidad numérica:** restar el máximo antes de exponenciar (`z - z.max()`) evita overflow sin cambiar el resultado. Sklearn ya lo hace internamente.

---

## 5. Conexión con el TP

**Estado:** el TP1 (*Laboratorio 1: Regresión en California*) **no toca regresión logística** — es íntegramente regresión continua. Logística aparece en clases 3–4 y se evalúa en **TP2**.

**Lo que te llevás del TP1:**
1. **Pipeline + train/test split.** `make_pipeline(StandardScaler(), LogisticRegression(max_iter=200))`.
2. **Identificar overfitting.** Train acc >> val acc → bajar $C$ (más regularización).
3. **Grid de hiperparámetros.** Como probaste `degree` en TP1, vas a probar $C$ en TP2 con `np.logspace(-4, 4, 9)`.
4. **Trampa DataFrame vs ndarray.** Misma cosa que en TP1: convertí con `.values` o usá `.iloc`.
5. **Escala de features.** **Más crítico** que en regresión lineal: la sigmoide se satura si $\boldsymbol{\theta}^T\mathbf{x}$ es muy grande. **Siempre `StandardScaler` antes.**

**Adaptación mental** (clasificación binaria sobre California Housing):

```python
y_binary = (y > 2.0).astype(int)   # 2.0 = 200k USD
pipe = make_pipeline(
    StandardScaler(),
    LogisticRegression(C=1.0, max_iter=500, random_state=0),
)
pipe.fit(X_train, y_train)
proba = pipe.predict_proba(X_val)[:, 1]
```

---

## 6. Errores comunes

1. **Usar MSE en logística.** Mantra cátedra: *"MSE sola es convexa y funciona bien. El problema aparece al combinarla con la sigmoide."* **Siempre log-loss.**
2. **Olvidar que $C_{\text{sklearn}} = 1/\lambda$.** $C$ chico → mucha regularización (contra-intuitivo).
3. **Esperar probabilidades calibradas sin más.** `predict_proba` da una estimación, no necesariamente bien calibrada. Para calibrar: `CalibratedClassifierCV`.
4. **No escalar features.** Si rangos disparejos, la sigmoide se satura, el gradiente colapsa. **`StandardScaler` siempre.**
5. **Confundir `predict` con `predict_proba`.** El primero devuelve labels (int), el segundo probabilidades en $(0,1)$. Para ROC AUC / log-loss querés el segundo.
6. **Asumir umbral 0.5 óptimo.** Para desbalanceo o costos asimétricos, ajustá con `roc_curve` o `precision_recall_curve`.
7. **Solver incompatible con penalty.** L1/elasticnet requieren `'liblinear'` o `'saga'`. L-BFGS solo L2 o None.
8. **`max_iter` muy bajo.** Sklearn te tira `ConvergenceWarning` — leelo. Subí `max_iter` o escalá features.
9. **Separabilidad perfecta sin regularización.** El optimizador empuja $\theta_j \to \infty$ (requiere $\sigma \to 1$ exacto). Catastrófico numéricamente. **L2 con $C$ moderado mantiene los pesos finitos.**
10. **Interpretar coeficientes como en regresión lineal.** En logística, $\theta_j$ es "cuánto cambia el **log-odds**", no $y$ ni $P(y=1)$.
11. **Tratarla como caja negra.** Es uno de los modelos **más interpretables** que existen — coeficientes con significado epidemiológico/causal directo.

---

## 7. Checklist

- [ ] Sé que la regresión logística **es un clasificador** (nombre histórico).
- [ ] Conozco $\sigma(z) = 1/(1+e^{-z})$, sus propiedades y $\sigma'(z) = p(1-p)$.
- [ ] Puedo derivar $\log[p/(1-p)] = \boldsymbol{\theta}^T\mathbf{x}$ e interpretar coeficientes (odds-ratio = $e^{\theta_j}$).
- [ ] Sé las **dos razones por las que NO usamos MSE** (no convexidad + saturación del gradiente).
- [ ] Puedo derivar la log-loss a partir de la verosimilitud Bernoulli.
- [ ] Conozco el gradiente $\nabla J = (1/N)\sum(h_\theta(\mathbf{x}^{(i)}) - y^{(i)})\mathbf{x}^{(i)}$ y reconozco la forma idéntica al MSE.
- [ ] Sé que sklearn usa $C = 1/\lambda$ (al revés) y elijo grilla logarítmica.
- [ ] Conozco las tres penalizaciones (L1, L2, elasticnet) y cuándo usarlas.
- [ ] Sé extender a multiclase con softmax y que **la sigmoide es softmax con K=2**.
- [ ] Sé usar `LogisticRegression` con `predict_proba`, `decision_function`, `coef_`.
- [ ] Reconozco 3+ errores comunes: no escalar, confundir $C$ con $\lambda$, asumir umbral 0.5.

---

## 8. Para profundizar

**Papers clásicos:**
- **Cox, D. R. (1958).** "The Regression Analysis of Binary Sequences." *JRSS-B*, 20(2), 215–242. El origen estadístico. DOI: [10.1111/j.2517-6161.1958.tb00292.x](https://doi.org/10.1111/j.2517-6161.1958.tb00292.x).
- **Berkson, J. (1944).** "Application of the Logistic Function to Bio-Assay." *JASA*, 39(227), 357–365. Precursor de Cox; introduce el término "logit".

**Libros:**
- **Bishop (2006)** *PRML*, **§4.3** — derivación completa, IRLS, multiclase.
- **Murphy (2022)** *PML*, **§10**. Gratis: [probml.github.io/pml-book](https://probml.github.io/pml-book/book1.html).
- **Hastie, Tibshirani, Friedman (2009)** *ESL*, **§4.4** — odds-ratio, deviance, GLMs. Gratis: [hastie.su.domains/ElemStatLearn](https://hastie.su.domains/ElemStatLearn/).
- **McCullagh & Nelder (1989)** *Generalized Linear Models*. La logística como GLM con enlace logit + Bernoulli.
- **Goodfellow, Bengio, Courville (2016)** *Deep Learning*, **§6.2** — logística como neurona con activación sigmoide.

**scikit-learn:** [`LogisticRegression`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html), [User Guide §1.1.11](https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression), [`load_digits`](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_digits.html).

**Complementos:** **statsmodels.api.Logit** (p-values, IC, tests de hipótesis — sklearn no los da); **scipy.special.expit** (sigmoide vectorizada numéricamente estable).

---

## Próximo paso

La regresión logística asume que **podemos modelar $P(y\mid\mathbf{x})$ directamente** (enfoque **discriminativo**). Hay otra familia que da el rodeo: modela $P(\mathbf{x}\mid y)$ y $P(y)$, después aplica Bayes para obtener $P(y\mid\mathbf{x})$ (enfoque **generativo**). El representante canónico es **Naive Bayes**, que con un supuesto fuerte de independencia condicional logra un clasificador rápido, simple y sorprendentemente potente para texto y datos discretos.

→ [08-naive-bayes.md](08-naive-bayes.md)

---

## Referencias

**Material primario:** DiploDatos UNC FAMAF 2026 — IAA Clase 2 Bloque B (PDF p. 2–13, p. 41–43) + Notebook 03. Dataset: `sklearn.datasets.load_digits()` (1797 imágenes 8×8, 10 clases).

**Bibliografía citada:**
- Cox, D. R. (1958). *JRSS-B*, 20(2), 215–242. https://doi.org/10.1111/j.2517-6161.1958.tb00292.x
- Berkson, J. (1944). *JASA*, 39(227), 357–365.
- Bishop, C. M. (2006). *PRML*, §4.3. Springer.
- Murphy, K. P. (2022). *PML*, §10. MIT Press.
- Hastie, Tibshirani, Friedman (2009). *ESL*, §4.4. Springer.
- McCullagh, P. & Nelder, J. A. (1989). *Generalized Linear Models*. Chapman & Hall.
- Boyd, S. & Vandenberghe, L. (2004). *Convex Optimization*. Cambridge UP.

**Documentación:** [`LogisticRegression`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html), [`load_digits`](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_digits.html), [Linear Models — Logistic Regression](https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression), [Logistic regression (Wikipedia)](https://en.wikipedia.org/wiki/Logistic_regression), [Sigmoid function (Wikipedia)](https://en.wikipedia.org/wiki/Sigmoid_function).

→ [08-naive-bayes.md](08-naive-bayes.md)
