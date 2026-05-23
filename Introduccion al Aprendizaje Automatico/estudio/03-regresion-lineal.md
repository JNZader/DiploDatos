# 03 — Regresión Lineal

> **Tema:** modelo lineal de regresión, mínimos cuadrados, ecuación normal y solución analítica cerrada.
> **Material base:** Clase 1 — Bloque B (PDF p.15–27), Notebook 01 (`01 Regresion_2026.ipynb`).
> **Bibliografía:** Bishop (2006) §3.1, ESL (Hastie et al., 2009) §3.2, Murphy (2022) §11.

---

## 1. Concepto

La **regresión** es el subtipo de aprendizaje supervisado donde el target $t$ (o $y$, según el texto) es una variable **numérica continua**. Disponemos de $N$ pares de entrenamiento $(x_i, t_i)_{i=1}^{N}$ y queremos estimar una función $f(x)$ tal que $t \approx f(x)$ (Clase 1, PDF p.18).

La **regresión lineal** es la versión más simple de esa familia: asume que $f$ es una combinación lineal de los parámetros $\mathbf{w}$ (no necesariamente de $x$):

$$
y(\mathbf{x}, \mathbf{w}) = \sum_{j=0}^{M} w_j \, \phi_j(\mathbf{x}) = \mathbf{w}^T \boldsymbol{\phi}(\mathbf{x})
$$

donde $\phi_j$ son **funciones base** (basis functions) y $\phi_0(\mathbf{x}) \equiv 1$ absorbe el **bias** $w_0$ (Bishop, 2006, §3.1). Es "lineal en $\mathbf{w}$" — no en $\mathbf{x}$, y de ahí nace la polinomial del próximo capítulo.

> **Notación cátedra vs Bishop.** El PDF p.18 usa $t_i$ para el target; los notebooks usan $y_i$. Bishop también usa $t_n$ (Bishop, 2006, §3.1.1). En este apunte nos vamos a quedar con $y$ por consistencia con el código y porque el TP1 usa `y`.

---

## 2. Intuición

La cátedra arranca con un ejemplo que vale ORO didácticamente (Notebook 01, celda 12):

> Tenés las notas de un estudiante: `[6, 7, 8, 7, 9, 6, 8]`. ¿Qué número resume mejor su rendimiento?

Tu cabeza dice "el promedio" — pero **el promedio no es una receta, es la solución de un problema de optimización**. Específicamente: es el valor $a$ que minimiza $\sum (y_i - a)^2$.

Eso es **toda la regresión lineal en miniatura**: tenés una familia de modelos (acá, constantes $\hat{y}_i = a$), una función de costo (error cuadrático), y derivás para encontrar el mínimo. Cuando subís a $y = w_0 + w_1 x$, cambia la familia y la dimensión, pero la receta es la misma: **derivar, igualar a cero, despejar**.

Analogía construcción (mantengámonos en el tono cátedra): el bias $w_0$ es la **cota base** del terreno; los $w_j$ son las **pendientes** del techo en cada dirección. Si te falta el bias, tu casa está obligada a tener piso en el origen — exactamente el problema que aparece en el perceptrón sin término constante (Notebook 02, celda 59).

---

## 3. Cuerpo técnico

### 3.1 Modelo y función de costo

Para datos 1-D con $\phi_0(x)=1$, $\phi_1(x)=x$:

$$
y(x, \mathbf{w}) = w_0 + w_1 x
$$

Para el caso general con $M$ features (incluyendo bias):

$$
y(\mathbf{x}, \mathbf{w}) = \mathbf{w}^T \boldsymbol{\phi}(\mathbf{x}) \in \mathbb{R}
$$

La función de costo cuadrática (sum of squared errors, SSE) que usa la cátedra (PDF p.19) es:

$$
E(\mathbf{w}) = \frac{1}{2} \sum_{n=1}^{N} \bigl(y(\mathbf{x}_n, \mathbf{w}) - t_n\bigr)^2
$$

El factor $\frac{1}{2}$ no cambia el mínimo, sólo cancela el 2 de la derivada. Bishop la justifica como negative log-likelihood bajo ruido gaussiano (Bishop, 2006, §3.1.1, ecuación 3.10).

### 3.2 Caso cero-dimensión: por qué el promedio

Con $\hat{y}_i = a$ (modelo constante), $E(a) = \sum (y_i - a)^2$. Derivamos respecto de $a$ (Notebook 01, celda 11):

$$
\frac{dE}{da} = -2 \sum_{i=1}^{N} (y_i - a) = 0 \implies a^* = \frac{1}{N}\sum_{i=1}^{N} y_i
$$

> "El promedio no aparece como una receta: aparece como la solución del problema de minimizar el error cuadrático." (Notebook 01, celda 15)

### 3.3 Caso general: la ecuación normal

Definimos la **matriz de diseño** $\mathbf{Z} \in \mathbb{R}^{N \times (M+1)}$ apilando los vectores de features de cada muestra:

$$
\mathbf{Z} = \begin{pmatrix}
1 & x_1 & x_1^2 & \cdots & x_1^M \\
1 & x_2 & x_2^2 & \cdots & x_2^M \\
\vdots & \vdots & \vdots & \ddots & \vdots \\
1 & x_N & x_N^2 & \cdots & x_N^M
\end{pmatrix}
$$

Y el vector de targets $\mathbf{y} = (y_1, \dots, y_N)^T \in \mathbb{R}^N$. La función de costo se reescribe en forma matricial (PDF p.27):

$$
E(\mathbf{w}) = \frac{1}{2}\|\mathbf{Z}\mathbf{w} - \mathbf{y}\|^2 = \frac{1}{2}(\mathbf{Z}\mathbf{w} - \mathbf{y})^T(\mathbf{Z}\mathbf{w} - \mathbf{y})
$$

Bishop nota la convención alterna $\boldsymbol{\Phi}$ para la matriz de diseño (Bishop, 2006, §3.1.1, ec. 3.16) — el PDF p.27 alterna $\mathbf{Z}$ y $\boldsymbol{\Phi}$ en la misma diapositiva.

**Derivación.** Expandimos:

$$
E(\mathbf{w}) = \tfrac{1}{2}\bigl(\mathbf{w}^T \mathbf{Z}^T \mathbf{Z} \mathbf{w} - 2 \mathbf{w}^T \mathbf{Z}^T \mathbf{y} + \mathbf{y}^T \mathbf{y}\bigr)
$$

Gradiente respecto de $\mathbf{w}$:

$$
\nabla_{\mathbf{w}} E = \mathbf{Z}^T \mathbf{Z} \mathbf{w} - \mathbf{Z}^T \mathbf{y}
$$

Igualando a cero obtenemos la **ecuación normal** (normal equation):

$$
\boxed{\;\mathbf{w}^* = (\mathbf{Z}^T \mathbf{Z})^{-1} \mathbf{Z}^T \mathbf{y}\;}
$$

Esto es la **pseudo-inversa de Moore-Penrose** aplicada a $\mathbf{Z}$ cuando tiene rango completo en columnas (Bishop, 2006, §3.1.1; ESL §3.2, ec. 3.6).

> **Resultado clave (PDF p.27, literal):** "Ambas soluciones son analíticas y cerradas. No requieren iteración."

### 3.4 Implementación: `pinv` vs `solve` vs `inv`

Tres formas de obtener $\mathbf{w}^*$ en NumPy, en orden de robustez creciente:

```python
# Opción 1 — inversa explícita (mala para mal-condicionados)
w = np.linalg.inv(Z.T @ Z) @ Z.T @ y

# Opción 2 — pseudoinversa (la que usa la cátedra)
w = np.linalg.pinv(Z.T @ Z) @ Z.T @ y          # PDF / Notebook 01 celda 30
# o, mejor todavía, directamente sobre Z (SVD-based):
w = np.linalg.pinv(Z) @ y

# Opción 3 — sistema lineal (la más estable y rápida)
w = np.linalg.solve(Z.T @ Z, Z.T @ y)

# Opción 4 — lstsq directo (lo que internamente hace sklearn)
w, *_ = np.linalg.lstsq(Z, y, rcond=None)
```

**¿Por qué la cátedra usa `pinv`?** El Notebook 01 (celda 31) lo justifica: "para mayor estabilidad". Cuando $\mathbf{Z}^T \mathbf{Z}$ es **mal condicionada** (columnas casi colineales, features con escalas muy distintas, $M$ alto), `inv` produce números basura. `pinv` resuelve con SVD y es robusta. `solve` también es buena y suele ser más rápida.

### 3.5 ¿Cuándo falla la ecuación normal?

Tres modos de falla que conviene tener en la cabeza (ESL §3.2):

1. **$\mathbf{Z}^T \mathbf{Z}$ singular.** Pasa si $N < M+1$ (más features que muestras) o si dos columnas son linealmente dependientes. La ecuación normal directamente no tiene solución única. **Solución:** `pinv` (devuelve la solución de mínima norma) o **regularización Ridge** (cap. 05).
2. **Mal condicionamiento numérico.** Aunque sea invertible, $\kappa(\mathbf{Z}^T \mathbf{Z}) = \kappa(\mathbf{Z})^2$ — invertir $\mathbf{Z}^T \mathbf{Z}$ **eleva al cuadrado** el número de condición. Por eso `pinv(Z)` (que actúa sobre $\mathbf{Z}$ directamente con SVD) es mejor que `pinv(Z.T @ Z)` cuando hay riesgo numérico.
3. **Datasets enormes.** La ecuación normal cuesta $O(NM^2 + M^3)$. Con $N$ de millones y $M$ alto, hay que ir a métodos iterativos (gradiente, SGD). Para California Housing ($N=16{,}512$, $M=8$) la ecuación normal anda barbaro.

---

## 4. Ejemplo numérico

### 4.1 Caso cero-dimensión (Notebook 01)

```python
notas = np.array([6, 7, 8, 7, 9, 6, 8])
a_optimo = notas.mean()      # 7.2857...
E_min   = ((notas - a_optimo)**2).sum()   # ≈ 7.43
```

Si graficás $E(a)$ moviendo $a$ entre 5 y 9, obtenés una **parábola** con vértice exactamente en 7.286.

### 4.2 Regresión 1-D sobre sinusoidal (Notebook 01, Bloque B.14.2)

```python
def create_sinusoidal_data(spread=0.25, data_size=50):
    np.random.seed(0)
    x = np.linspace(0, 1, data_size)
    y = np.sin(2*np.pi*x) + np.random.normal(scale=spread, size=x.shape)
    return x, y

X, y = create_sinusoidal_data(0.10, 20)
X_train, X_val, y_train, y_val = train_test_split(X, y, train_size=5, random_state=1)

def linear_least_squares(X, y):
    X_b = np.stack((np.ones(X.shape[0]), X), axis=1)
    return np.linalg.pinv(X_b.T @ X_b) @ (X_b.T @ y)

w = linear_least_squares(X_train, y_train)
# w[0] ≈ bias, w[1] ≈ pendiente
```

**Resultado esperado:** una recta plana que cae hacia la derecha (intenta seguir el primer cuarto de la sinusoide). RMSE de validación > RMSE de entrenamiento → "no generaliza bien". La conclusión cátedra (Notebook 01, celda 39, literal): **"Una recta no puede representar adecuadamente una sinusoide"**. Eso motiva polinomial (cap. 04).

### 4.3 El bias como columna de unos

Notación crítica que la cátedra explica en la celda 36 del Notebook 01:

> Con $K=1$ tendríamos $f_{w^*}(x) = x_1 w_1^*$. Para que sea una recta nos falta un $w_0$ ('bias'). Esto se puede resolver haciendo $K=2$ y agregando un valor constante 1 a cada dato.

En código: `X_b = np.stack((np.ones(N), X), axis=1)` — la primera columna de unos absorbe $w_0$. Lo mismo hace sklearn por defecto con `fit_intercept=True`; **lo desactiva** (`fit_intercept=False`) cuando usás `PolynomialFeatures`, porque esta última ya genera la columna `1` (Notebook 01, celda 43).

---

## 5. Conexión con el TP

**Ejercicio 3 del TP1** (cell-19 del notebook) es regresión lineal pura sobre California Housing:

1. Seleccionás **un solo atributo** del Ej. 2 (típicamente `MedInc`, que tiene la correlación visual más fuerte con el target).
2. Entrenás `LinearRegression()` de sklearn.
3. Evaluás MSE en train y test.
4. Graficás la recta sobre el scatter.

```python
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

selector = np.array(california['feature_names']) == 'MedInc'
X_tr = X_train.values[:, selector]   # cuidado: DataFrame → ndarray
X_te = X_test.values[:, selector]

model = LinearRegression().fit(X_tr, y_train)
print('MSE train:', mean_squared_error(y_train, model.predict(X_tr)))
print('MSE test :', mean_squared_error(y_test,  model.predict(X_te)))
```

El enunciado dice "se puede obtener un error en test menor a 50". Ese "50" está en unidades de (target)² — el target son centenas de miles de USD, así que es **MSE crudo**, no RMSE ni R².

Acordate también que `LinearRegression` de sklearn internamente usa **`np.linalg.lstsq`** (SVD), no la ecuación normal explícita. Por eso es robusto incluso con features mal condicionadas (sklearn docs, `LinearRegression`).

---

## 6. Errores comunes

1. **Indexar DataFrame como ndarray.** `X_train[:, selector]` falla con `InvalidIndexError` cuando `fetch_california_housing` devuelve DataFrame (sklearn ≥ 1.2). Soluciones: `as_frame=False` al cargar, `.values[:, selector]`, o `.iloc[:, selector]`. (TP1 trampa documentada en `iaa_tp1_extract.md`.)
2. **Olvidar el bias.** Si entrenás `LinearRegression(fit_intercept=False)` sin agregar columna de unos, tu recta pasa por el origen — exactamente el bug del perceptrón en Notebook 02 (celda 59).
3. **Usar `inv` en lugar de `pinv` o `solve`.** Funciona en juguete; revienta con datos reales o $M$ alto. Tip: si tu MSE sale negativo o $|w| > 10^6$, sospechá del condicionamiento.
4. **Confundir "lineal en $\mathbf{w}$" con "lineal en $\mathbf{x}$".** $y = w_0 + w_1 x^2$ es **regresión lineal** (sobre $\phi_1(x) = x^2$). Lo único que pide la teoría es que el modelo sea afín en los parámetros (Bishop, 2006, §3.1).
5. **Reshape de 1-D a 2-D.** sklearn espera shape `(N, M)`. Con un solo feature hay que pasar `X.reshape(-1, 1)`. El selector booleano de NumPy ya lo devuelve en `(N, 1)`, pero `X[:, 0]` no.
6. **No mirar la escala del MSE.** El TP1 usa target en "x 100k USD"; un MSE de 0.5 es ~\$50k² de error medio cuadrático, no "50%". Conviene reportar también RMSE o $R^2$ para interpretabilidad.

---

## 7. Checklist de comprensión

- [ ] Sé escribir el modelo como $y(\mathbf{x}, \mathbf{w}) = \mathbf{w}^T \boldsymbol{\phi}(\mathbf{x})$ y explicar qué pone cada $\phi_j$.
- [ ] Puedo derivar la ecuación normal $\mathbf{w}^* = (\mathbf{Z}^T\mathbf{Z})^{-1}\mathbf{Z}^T\mathbf{y}$ desde $E(\mathbf{w}) = \tfrac{1}{2}\|\mathbf{Z}\mathbf{w} - \mathbf{y}\|^2$.
- [ ] Sé por qué el promedio es la solución óptima del caso constante.
- [ ] Distingo `inv`, `pinv`, `solve` y `lstsq` y sé cuál usar.
- [ ] Identifico los tres modos de falla de la ecuación normal.
- [ ] Sé que "lineal" se refiere a los parámetros, no al input.
- [ ] Puedo resolver el Ej. 3 del TP1 con `LinearRegression` y `mean_squared_error`.

---

## 8. Para profundizar

- **Bishop, 2006, §3.1** — formulación completa con basis functions, máxima verosimilitud bajo ruido gaussiano, geometría de mínimos cuadrados (proyección ortogonal de $\mathbf{y}$ sobre el span de las columnas de $\boldsymbol{\Phi}$). Sección 3.1.3 introduce la solución on-line / SGD que vamos a usar cuando $N$ es grande.
- **ESL §3.2** (Hastie et al., 2009) — interpretación estadística: distribución de $\hat{\mathbf{w}}$, intervalos de confianza, ANOVA. Sec. 3.2.2 cubre el test F y la inferencia clásica.
- **Murphy, 2022, §11.2** — versión moderna con vista probabilística completa, incluye MLE bajo Gaussiana y conexión con MAP (que es Ridge — cap. 05).
- **scikit-learn user guide §1.1** — implementación, opciones (`positive=True`, `fit_intercept`), benchmarks `LinearRegression` vs `Ridge` vs `Lasso`.

---

## Próximo paso

→ [04-regresion-polinomial.md](04-regresion-polinomial.md) — extendemos el modelo a $\phi_j(x) = x^j$ y vemos en vivo el fenómeno de **overfitting** cuando $M$ crece.

---

## Referencias

- Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*. Springer. §3.1, §3.1.1.
- Hastie, T., Tibshirani, R., & Friedman, J. (2009). *The Elements of Statistical Learning* (2nd ed.). Springer. §3.2.
- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press. §11.
- Meinardi, V. & Bonzi, E. (2026). *Introducción al Aprendizaje Automático — Clase 1*. DiploDatos UNC FAMAF. PDF slides 15–27, Notebook `01 Regresion_2026.ipynb`.
- scikit-learn developers (2026). *`sklearn.linear_model.LinearRegression`* — <https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html>
- Bishop, C. M. (2009). *PRML companion notes / chapter 3 slides* — <https://www.di.fc.ul.pt/~jpn/r/PRML/chapter3.html>
