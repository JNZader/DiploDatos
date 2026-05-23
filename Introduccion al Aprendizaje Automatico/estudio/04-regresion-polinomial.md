# 04 — Regresión Polinomial

> **Tema:** extensión polinomial del modelo lineal, capacidad del modelo, overfitting y la dinámica del error en función del grado $M$.
> **Material base:** Clase 1 — Bloque B (PDF p.19–23), Notebook 01 (Bloque B.14.3, celdas 41–55).
> **Bibliografía:** Bishop (2006) §3.1.1, Murphy (2022) §11.5, ESL §3.2.

---

## 1. Concepto

La **regresión polinomial** ajusta a los datos un polinomio de grado $M$:

$$
y(x, \mathbf{w}) = w_0 + w_1 x + w_2 x^2 + \dots + w_M x^M = \sum_{j=0}^{M} w_j \, x^j
$$

(Clase 1, PDF p.19). Operacionalmente, **no es un modelo nuevo**: es la regresión lineal del capítulo anterior, pero con **funciones base monomiales** $\phi_j(x) = x^j$ (Bishop, 2006, §3.1.1).

Esa equivalencia es **el truco más importante del bloque** y la cátedra lo destaca con un slide entero (PDF p.26):

> "La regresión polinomial puede ser vista como una regresión lineal con múltiples variables regresoras."

Sustituyendo $z_j = x^j$:

$$
y(x, \mathbf{w}) = w_0 + w_1 z_1 + \dots + w_M z_M = \mathbf{w}^T \mathbf{z}
$$

Resultado: todo lo del cap. 03 — ecuación normal, pseudoinversa, función de costo — sigue valiendo. Sólo **cambia la matriz de diseño** $\mathbf{Z}$, que ahora apila potencias.

---

## 2. Intuición

Pensá el grado $M$ como **el número de "codos"** que tu curva puede dibujar. Con $M=1$ tenés una recta (sin codos); con $M=3$ podés hacer una S; con $M=9$ podés hacer una serpiente que pasa exactamente por 10 puntos cualesquiera.

> **Analogía de la cátedra (PDF p.21):** *"el modelo memoriza en lugar de aprender"*.

Esa frase es la clave entera del capítulo. Con $M$ grande el polinomio puede pasar **exactamente** por todos los puntos de entrenamiento — pero a costa de inventar oscilaciones brutales entre ellos (fenómeno de Runge en interpolación clásica, mismo origen matemático). El modelo no aprendió la **regla**; aprendió de memoria.

El problema es generalizable: cualquier familia de modelos con **capacidad** (model capacity) demasiado alta para los datos disponibles va a memorizar el ruido. Es **el motivo de existir** de toda la teoría posterior de regularización, validación cruzada, dropout, weight decay, early stopping (Murphy, 2022, §11.5; ESL §7).

---

## 3. Cuerpo técnico

### 3.1 Matriz de diseño polinomial

Para 1-D y grado $M$, la matriz de diseño es **Vandermonde**:

$$
\mathbf{Z} = \begin{pmatrix}
1 & x_1 & x_1^2 & \cdots & x_1^M \\
1 & x_2 & x_2^2 & \cdots & x_2^M \\
\vdots & \vdots & \vdots & \ddots & \vdots \\
1 & x_N & x_N^2 & \cdots & x_N^M
\end{pmatrix} \in \mathbb{R}^{N \times (M+1)}
$$

(Clase 1, PDF p.27.) Y la solución es exactamente la misma ecuación normal:

$$
\mathbf{w}^* = (\mathbf{Z}^T \mathbf{Z})^{-1} \mathbf{Z}^T \mathbf{y}
$$

**Detalle crítico para sklearn.** `PolynomialFeatures(degree=M, include_bias=True)` te genera exactamente esa matriz $\mathbf{Z}$ con la primera columna `1`. Si pegás un `LinearRegression(fit_intercept=True)` después, **duplicás el bias**. Por eso la cátedra usa explícitamente (Notebook 01, celda 43):

```python
model = make_pipeline(
    PolynomialFeatures(d),
    LinearRegression(fit_intercept=False)   # ← el bias ya viene como columna
)
```

### 3.2 Capacidad del modelo y bias-variance

A medida que crece $M$, la **capacidad** del modelo (su habilidad para representar funciones complejas) crece. Eso reduce el **bias** (error sistemático por sub-ajuste) pero aumenta la **varianza** (sensibilidad a cambios en la muestra de entrenamiento). Es el **bias-variance tradeoff** (ESL §2.9, Bishop, 2006, §3.2).

Murphy (2022) lo formaliza: para un punto de evaluación $x_0$, el error cuadrático esperado descompone como:

$$
\mathbb{E}[(y_0 - \hat{f}(x_0))^2] = \underbrace{\sigma^2}_{\text{irreducible}} + \underbrace{\text{Bias}^2[\hat{f}(x_0)]}_{\text{underfit}} + \underbrace{\text{Var}[\hat{f}(x_0)]}_{\text{overfit}}
$$

El primer término es el **ruido inherente** del problema; los otros dos los controlamos eligiendo $M$ (y, en el cap. 05, $\lambda$).

### 3.3 El fenómeno del overfitting — TABLA CANÓNICA

La cátedra muestra explícitamente cómo cambian los errores con $M$ sobre datos sinusoidales con $N=20$, ruido $\sigma=0.10$ (PDF p.20). Esta tabla es **literal** del material:

| $M$ | Caso | train RMSE | val RMSE |
|----:|------|----------:|---------:|
| 0 | Underfitting total | 0.762 | 0.568 |
| 1 | Underfitting | 0.533 | 0.433 |
| 3 | **Buen ajuste** | **0.216** | **0.263** |
| 9 | Overfitting | 0.131 | 0.282 |

> Definición de RMSE de la cátedra (PDF p.21): $E_{\text{RMS}} = \sqrt{2 E(\mathbf{w}^*) / N}$. El factor 2 aparece porque el costo $E$ ya lleva el $\tfrac{1}{2}$.

**Lectura:**
- $M=0$ (modelo constante = promedio) y $M=1$ (recta) tienen errores grandes EN AMBOS — no captan la curva. Esto es **underfitting**.
- $M=3$ tiene el mejor compromiso: error de train razonable + error de val mínimo. Es el **óptimo**.
- $M=9$ logra el menor error de **train** (0.131, casi nulo) pero el de **val** sube de nuevo (0.282 > 0.263). Es **overfitting**: el polinomio está pasando por el ruido.

Gráficamente, lo que dibuja la cátedra (PDF p.21) es una **curva de validación** clásica: train baja monotónicamente con $M$, val tiene forma de U con mínimo en $M=3$. Ese **codo en U** es el patrón que vas a ver en CADA experimento de capacidad de modelo, no sólo en polinomial.

### 3.4 Datos VS complejidad: el segundo ojo del overfit

La cátedra refuerza con una segunda tabla (PDF p.22) que muestra el rol de $N$:

| $M$ | $N$ | Caso | train RMSE | val RMSE |
|----:|----:|------|----------:|---------:|
| 3 | 20 | Buen ajuste | 0.234 | 0.229 |
| 9 | 20 | **Overfitting extremo** | 0.141 | **5.856** |
| 3 | 100 | Ajuste robusto | 0.223 | 0.191 |
| 9 | 100 | **Generalización lograda** | 0.209 | 0.189 |

**Lo MISMO** modelo ($M=9$) que con $N=20$ es una catástrofe (val RMSE 5.856!), con $N=100$ generaliza casi tan bien como $M=3$. El **dato salva**.

Esto es importantísimo conceptualmente: el overfitting no es **una propiedad del modelo** sola, sino **del modelo dado un dataset**. La pregunta correcta no es "¿cuál es el grado óptimo?" sino "¿cuál es el grado óptimo PARA MI N?".

Conexión con la práctica moderna: por eso los Transformers gigantes (billones de parámetros) **no overfittean** cuando los entrenás con corpus de internet entero — el $N$ es astronómico. Misma idea, distinta escala.

### 3.5 Coeficientes que explotan

Otra evidencia de overfit que la cátedra muestra explícitamente (PDF p.23): los coeficientes mismos crecen exponencialmente con $M$.

| Coef. | $M=0$ | $M=1$ | $M=3$ | $M=9$ |
|:------|------:|------:|------:|------:|
| $w_0^*$ | 0.05 | 0.17 | 0.01 | 0.00 |
| $w_1^*$ | — | 1.18 | 10.65 | **-24.82** |
| $w_2^*$ | — | — | -32.78 | **704.4** |
| $w_3^*$ | — | — | 22.38 | **-6349.81** |
| $w_9^*$ | — | — | — | **9276.55** |

> "Con M=9, los coeficientes alcanzan valores de miles, lo que indica que el modelo está interpolando el ruido en lugar de capturar la tendencia real. La regularización es la solución." (PDF p.23, literal)

Esta observación es exactamente la motivación de Ridge (cap. 05): **penalizar la norma de $\mathbf{w}$** para frenar la explosión.

---

## 4. Ejemplo numérico

Vamos a reproducir el Notebook 01 paso a paso (Bloque B.14.3):

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

def create_sinusoidal_data(spread=0.25, data_size=50):
    np.random.seed(0)
    x = np.linspace(0, 1, data_size)
    y = np.sin(2*np.pi*x) + np.random.normal(scale=spread, size=x.shape)
    return x, y

X, y = create_sinusoidal_data(0.10, 20)
X_tr, X_val, y_tr, y_val = train_test_split(X, y, train_size=5, random_state=1)

# Importante: reshape de 1-D a 2-D para sklearn
X_tr2  = X_tr.reshape(-1, 1)
X_val2 = X_val.reshape(-1, 1)

errores = []
for d in [1, 3, 5, 10]:
    model = make_pipeline(
        PolynomialFeatures(d),
        LinearRegression(fit_intercept=False)
    )
    model.fit(X_tr2, y_tr)
    e_tr  = mean_squared_error(y_tr,  model.predict(X_tr2))
    e_val = mean_squared_error(y_val, model.predict(X_val2))
    errores.append((d, e_tr, e_val))
    print(f'd={d:2d}  MSE_tr={e_tr:.4f}  MSE_val={e_val:.4f}')
```

**Output típico** (con la semilla del notebook): el error de train cae rápido hasta $d=3$ y luego se estanca cerca de cero; el de val tiene un mínimo (alrededor de $d=3$ con sólo 5 puntos de train, idealmente $d=3$–$5$ con $N=20$) y luego se dispara.

Concluyendo con la frase canónica del Notebook 01 (celda 55, **literal**):

> "**No buscamos el modelo que mejor ajusta los datos de entrenamiento. Buscamos el modelo que mejor generaliza a datos nuevos.**"

### Reshape: el detalle de las dimensiones

La cátedra explica explícitamente el `-1` en `reshape` (Notebook 01, celda 48):

```python
X_tr.reshape(-1, 1)
# 1  → una columna
# -1 → NumPy calcula automáticamente cuántas filas hacen falta
```

Sin el reshape sklearn explota con `Expected 2D array, got 1D array`.

---

## 5. Conexión con el TP

**Ejercicio 4 del TP1** (cell-26) es el experimento canónico de polinomial sobre California Housing — exactamente la misma receta del Notebook 01:

1. Elegí un atributo (típicamente `MedInc`).
2. Loop por `degree in range(1, 11)` (el enunciado no especifica el rango — sugerencia: 1..10).
3. Entrená pipeline `PolynomialFeatures + LinearRegression(fit_intercept=False)`.
4. Calculá MSE train y test.
5. Graficá la **curva del error vs grado**.
6. Identificá el codo (donde val/test empieza a subir) → ese es tu grado óptimo.
7. Graficá el mejor modelo sobre el scatter.

```python
errores = []
for d in range(1, 11):
    model = make_pipeline(
        PolynomialFeatures(d),
        LinearRegression(fit_intercept=False)
    )
    model.fit(X_tr, y_train)
    e_tr   = mean_squared_error(y_train, model.predict(X_tr))
    e_test = mean_squared_error(y_test,  model.predict(X_te))
    errores.append((d, e_tr, e_test))

ds, etrs, etes = zip(*errores)
plt.plot(ds, etrs,  'o-', label='train')
plt.plot(ds, etes, 's-', label='test')
plt.xlabel('grado del polinomio'); plt.ylabel('MSE'); plt.legend()
```

**Trampas del enunciado (documentadas en `iaa_tp1_extract.md`):**

- **No especifica el rango de grados** — usá 1..10 o 1..15.
- **Sin escalar las features**, los polinomios de grado alto explotan numéricamente. Conviene sumar `StandardScaler` al pipeline (no lo pide el TP, pero te ahorra falsos positivos de overfit).
- El MSE objetivo de la consigna ("< 40, incluso < 35") está en unidades de target².

**Ejercicio 5** (cell-32) extiende a 2-3 atributos. **Cuidado:** `PolynomialFeatures(degree=d)` con $K$ features genera $\binom{K+d}{d}$ columnas — con $K=3, d=10$ ya son 286 features. Combinatoria explosiva, riesgo de overfit mucho mayor.

---

## 6. Errores comunes

1. **Duplicar el bias.** `PolynomialFeatures` genera la columna de unos por default. Si después pegás `LinearRegression(fit_intercept=True)` (el default), el modelo tiene **dos columnas constantes** y `Z^T Z` se vuelve singular en esa dirección. Síntoma: `ConvergenceWarning` o resultados raros. Fix: `fit_intercept=False`. (PDF de la cátedra y Notebook 01 celda 43 lo aclaran explícitamente.)
2. **Olvidar el reshape.** `LinearRegression.fit(X, y)` necesita `X` 2-D. Para 1 sólo feature: `X.reshape(-1, 1)`.
3. **No escalar features.** $x^{10}$ con $x \approx 10$ es $10^{10}$. Sin `StandardScaler`, `Z^T Z` se vuelve **brutal**mente mal condicionada y los coeficientes explotan. La cátedra no lo pide pero es práctica estándar. La diferencia entre "overfit real" y "explosión numérica" se vuelve indistinguible — y la responsable suele ser la segunda.
4. **Interpretar errores en train como evidencia de "buen modelo".** Train MSE 0.001 con val MSE 5.0 = overfit catastrófico. **El de val es el que mide generalización.**
5. **Asumir que mayor grado = mejor.** El razonamiento "más capacidad = más mejor" es exactamente el que la cátedra desmonta con la tabla del PDF p.20.
6. **Confundir polinomial con no-lineal "real".** Polinomial **sigue siendo lineal en $\mathbf{w}$**; podés resolverlo con la ecuación normal. Modelos genuinamente no-lineales en $\mathbf{w}$ (redes neuronales, kernel ridge no-paramétrico) requieren gradient descent.

---

## 7. Checklist de comprensión

- [ ] Sé escribir el polinomio como $y(x, \mathbf{w}) = \sum_{j=0}^M w_j x^j$ y mostrar que es lineal en $\mathbf{w}$.
- [ ] Construyo la matriz de diseño Vandermonde a mano y la resuelvo con `pinv` o `lstsq`.
- [ ] Explico por qué `PolynomialFeatures + LinearRegression(fit_intercept=False)` es la combinación correcta.
- [ ] Puedo dibujar la curva train-vs-val del PDF p.21 sin mirarla.
- [ ] Identifico **underfitting** por error alto en AMBOS sets, y **overfitting** por gap grande entre train (bajo) y val (alto).
- [ ] Sé que aumentar $N$ "rescata" modelos de alto $M$ (PDF p.22).
- [ ] Reconozco la explosión de coeficientes como síntoma de overfit y motivación de la regularización del cap. 05.
- [ ] Puedo armar el Ej. 4 del TP1 e identificar el grado óptimo en California Housing.

---

## 8. Para profundizar

- **Bishop, 2006, §1.1** — la introducción del libro usa **exactamente este ejemplo** (sinusoidal + polinomial + tabla de coeficientes que explotan). Es la versión académica del bloque que estamos viendo. §3.1.1 da el tratamiento formal con basis functions.
- **Murphy, 2022, §11.5** — versión moderna con bias-variance + validación cruzada + curva de error como diagnóstico estándar.
- **ESL §3.2** (Hastie et al., 2009) — tratamiento de selección de subconjuntos y "best subset" como antecedente histórico de la regularización.
- **scikit-learn docs — `PolynomialFeatures`** — semántica exacta de `degree`, `interaction_only`, `include_bias`. Vale la pena leer la cantidad de columnas que genera con `K=3, degree=5` antes de hacerlo en producción.
- **Fenómeno de Runge** — desde la teoría de interpolación: por qué los polinomios de alto grado oscilan brutalmente entre nodos. Es la **misma matemática** del overfit que vemos en regresión polinomial.

---

## Próximo paso

→ [05-regularizacion-ridge.md](05-regularizacion-ridge.md) — la solución al overfit del cap. 04: penalizamos $\|\mathbf{w}\|^2$ y le agregamos $\lambda \mathbf{I}$ a la ecuación normal.

---

## Referencias

- Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*. Springer. §1.1, §3.1.1.
- Hastie, T., Tibshirani, R., & Friedman, J. (2009). *The Elements of Statistical Learning* (2nd ed.). Springer. §3.2, §7.
- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press. §11.5.
- Meinardi, V. & Bonzi, E. (2026). *Introducción al Aprendizaje Automático — Clase 1*. DiploDatos UNC FAMAF. PDF slides 19–23, Notebook `01 Regresion_2026.ipynb` (Bloque B.14.3).
- scikit-learn developers (2026). *`sklearn.preprocessing.PolynomialFeatures`* — <https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.PolynomialFeatures.html>
- scikit-learn user guide §1.1 — *Generalized Linear Models* — <https://scikit-learn.org/stable/modules/linear_model.html>
