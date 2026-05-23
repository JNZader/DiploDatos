# 00 — Python y NumPy para Machine Learning

> **Nota de propósito.** Este capítulo no enseña Python desde cero. Es un refresher táctico para no tropezar con las trampas técnicas del TP1 y de los notebooks de la cátedra (DiploDatos UNC 2026, IAA — Meinardi & Bonzi). Si ya manejaste NumPy y sklearn antes, igualmente conviene leer la sección 6 (errores comunes) porque ahí están enterrados los gotchas más caros.

## 1. Concepto

**NumPy** es la biblioteca de cómputo numérico de Python: provee el objeto `ndarray` (arreglo multidimensional homogéneo y tipado) y las operaciones vectorizadas que lo manipulan en C bajo el capó. Es el lenguaje franco del ML clásico en Python.

**scikit-learn** es la biblioteca de ML clásico que se monta sobre NumPy: ofrece **un API uniforme** (`fit` / `predict` / `transform` / `score`) para que TODOS los algoritmos se usen de la misma manera (sklearn docs, *Developing scikit-learn estimators*).

> Cita cátedra: en el notebook 01 (celda 31) la cátedra usa explícitamente `np.linalg.pinv(X.T @ X) @ X.T @ y` "para mayor estabilidad" — el punto es exactamente el que NumPy documenta: la pseudoinversa via SVD aguanta multicolinealidad y matrices casi-singulares que `inv` no puede invertir.

## 2. Intuición

Pensá NumPy como una **planilla de Excel tipada y vectorizada**:

- En Excel, una columna de 1000 números se procesa celda a celda con una fórmula que se "arrastra".
- En NumPy, esa misma operación es UNA línea (`x * 2 + 1`) y se ejecuta en un loop compilado en C que es 50–100× más rápido que un `for` puro en Python.

Y pensá sklearn como un **enchufe universal**: enchufes una `LinearRegression`, un `Perceptron`, un `LogisticRegression`, un `MultinomialNB`, todos en el mismo socket — `.fit(X, y)` y `.predict(X)`. Es el patrón de diseño "Strategy" hecho biblioteca (sklearn docs, API design).

## 3. Cuerpo técnico

### 3.1 — `ndarray`: forma, tipo y orden

```python
import numpy as np

x = np.array([1, 2, 3, 4, 5])
print(x.shape)   # (5,)        ← 1-D, vector
print(x.dtype)   # int64
print(x.ndim)    # 1
print(x.size)    # 5

A = np.array([[1, 2, 3], [4, 5, 6]])
print(A.shape)   # (2, 3)      ← 2-D, matriz
```

Tres atributos que vas a mirar 200 veces: `shape`, `dtype`, `ndim`. Cuando algo "no compila" en sklearn, el 80% de las veces es un `shape` que no esperabas.

**Diferencia crítica:** `(5,)` (vector 1-D) NO es lo mismo que `(5, 1)` (matriz columna). Muchos estimadores de sklearn esperan `(n, k)` y rompen con `(n,)`. Reshape de rescate:

```python
x = np.array([1, 2, 3, 4, 5])        # shape (5,)
x_col = x.reshape(-1, 1)              # shape (5, 1)
```

El `-1` significa "calculá vos cuántas filas hacen falta" (la cátedra lo aclara en el notebook 01, celda 48).

### 3.2 — Slicing y fancy indexing

```python
A = np.arange(12).reshape(3, 4)
# array([[ 0,  1,  2,  3],
#        [ 4,  5,  6,  7],
#        [ 8,  9, 10, 11]])

A[0]          # fila 0:        [0, 1, 2, 3]
A[:, 0]       # columna 0:     [0, 4, 8]
A[1:, 1:3]    # submatriz:     [[5, 6], [9, 10]]
A[:, [0, 2]]  # fancy:         columnas 0 y 2
A[A > 5]      # boolean mask:  [6, 7, 8, 9, 10, 11]
```

**Boolean mask:** clave para el Ej. 2 del TP1 — la cátedra propone seleccionar features con un selector booleano:

```python
selector = np.array(feature_names) == 'MedInc'   # array([True, False, ...])
X_sel = X[:, selector]
```

### 3.3 — Broadcasting

Regla canónica (numpy docs, *Broadcasting*):

1. Si los arrays difieren en dimensiones, se rellena con 1s a la **izquierda** del shape menor.
2. Dos dimensiones son compatibles si son iguales o si una de ellas es 1.
3. El resultado tiene el `max` de cada dimensión.

```python
A = np.ones((3, 4))      # (3, 4)
b = np.array([1, 2, 3, 4])   # (4,)  → broadcast a (1, 4) → (3, 4)
A + b                     # ✓ shape (3, 4)

c = np.array([1, 2, 3])  # (3,)
A + c                     # ✗ ValueError: shapes (3,4) (3,) incompatibles
A + c.reshape(-1, 1)      # ✓ (3,1) broadcastea a (3,4)
```

Ejemplo canónico de la doc de NumPy: una imagen `(256, 256, 3)` por un vector `(3,)` escala cada canal independientemente.

### 3.4 — Álgebra lineal: el operador `@` y solvers

| Operación | Sintaxis | Cuándo |
|-----------|----------|--------|
| Producto matricial | `A @ B` (Python ≥3.5) o `np.dot(A, B)` | Ecuación normal, predicción lineal |
| Transposición | `A.T` | $X^T X$, etc. |
| Inversa | `np.linalg.inv(A)` | Sólo si A es cuadrada e invertible. **Evitalá** en ML — preferí solve/pinv |
| Pseudoinversa (Moore-Penrose) | `np.linalg.pinv(A)` | Funciona siempre (vía SVD). Tolerante a singularidad |
| Resolver $Ax=b$ | `np.linalg.solve(A, b)` | Más estable que `inv(A) @ b` |
| Mínimos cuadrados | `np.linalg.lstsq(X, y, rcond=None)` | **Recomendado** por NumPy para regresión |
| Norma euclídea | `np.linalg.norm(v)` | $\Vert \mathbf{w}\Vert $ en regularización |

**Ecuación normal (cátedra, PDF p.27 / notebook 01 celda 30):**

$$
\mathbf{w}^* = (\mathbf{X}^T \mathbf{X})^{-1} \mathbf{X}^T \mathbf{y}
$$

Implementación que usa la cátedra (notebook 01, celda 30):

```python
def linear_least_squares(X, y):
    X_b = np.stack((np.ones(X.shape[0]), X), axis=1)   # agrega columna de 1s (bias)
    return np.linalg.pinv(X_b.T @ X_b) @ (X_b.T @ y)
```

**Por qué `pinv` y no `inv`:** si $X^TX$ es singular o casi singular (multicolinealidad — pasa con `PolynomialFeatures` de grado alto), `inv` explota con `LinAlgError`. La pseudoinversa via SVD aguanta y devuelve la solución de mínima norma (numpy docs, `np.linalg.pinv`).

> **Tip pro:** en producción, ni `pinv` ni `inv` — usá `np.linalg.lstsq(X, y, rcond=None)` que es el recomendado por NumPy para mínimos cuadrados (más eficiente, más estable).

### 3.5 — DataFrame de pandas vs `ndarray`: LA TRAMPA DEL TP1

Desde sklearn ≥ 0.24, varios `load_*` y `fetch_*` devuelven el `data` como **DataFrame** (no como `ndarray`) por defecto. Esto rompe el código de ejemplo de la cátedra en el TP1:

```python
from sklearn.datasets import fetch_california_housing
california = fetch_california_housing()
X = california['data']        # ← puede ser DataFrame o ndarray según versión

selector = np.array(california['feature_names']) == 'MedInc'

# Esto FUNCIONA si X es ndarray, FALLA si X es DataFrame:
X_sel = X[:, selector]
# DataFrame.__getitem__ con (slice, bool_array) → InvalidIndexError
```

**Tres soluciones (documentar las tres):**

```python
# Opción 1 — cargar como ndarray desde el inicio
california = fetch_california_housing(as_frame=False)

# Opción 2 — convertir antes de indexar
X = np.asarray(california['data'])

# Opción 3 — usar .iloc del DataFrame
X_sel = X.iloc[:, selector]
```

Cuál preferir: para los notebooks de la cátedra, **opción 1** (la más parecida al código de ejemplo). Para código nuevo, opción 3 (mantiene los nombres de columnas, debugging más amable).

### 3.6 — sklearn API: el patrón `fit` / `predict` / `transform`

Todos los estimadores siguen el mismo contrato (sklearn docs, *Developing scikit-learn estimators*):

```python
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

# Predictor (regressor o classifier)
model = LinearRegression()
model.fit(X_train, y_train)                # aprende
y_pred = model.predict(X_test)             # predice
r2 = model.score(X_test, y_test)           # evalúa (default: R² para regresores, accuracy para clasificadores)

# Transformer (preprocesa datos)
scaler = StandardScaler()
scaler.fit(X_train)                        # aprende media/desvío
X_train_s = scaler.transform(X_train)      # aplica
X_test_s = scaler.transform(X_test)        # aplica MISMOS parámetros
```

**Regla de oro:** `fit` SOLO con train. Si llamás `fit` o `fit_transform` sobre test, contaminás la evaluación (data leakage).

### 3.7 — `train_test_split` y `random_state`

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    train_size=0.8,       # 80% train, 20% test
    random_state=0        # ← REPRODUCIBILIDAD
)
```

`random_state` es la semilla del RNG que decide cómo barajar (sklearn docs, `train_test_split`). Tres modos:
- `int` (ej. `0`, `42`): mismo split siempre → reproducible.
- `None`: split nuevo cada corrida → NO reproducible.
- `RandomState`: pasás un generador propio.

En el TP1 (celda 9) la cátedra fija `random_state=0` para que todos tengan el mismo split. Si lo cambiás "para probar", los números del enunciado dejan de coincidir.

> **Nota:** en el notebook 02 (perceptrón) la cátedra hace el split MANUALMENTE (`X[:60]`, `X[60:]`) en vez de usar `train_test_split`. Es legítimo si los datos ya vienen barajados (como `make_classification` con `random_state`).

### 3.8 — Pipelines

Patrón que aparece en el notebook 01 (celda 48):

```python
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

model = make_pipeline(
    PolynomialFeatures(degree=3),
    LinearRegression(fit_intercept=False)   # bias ya viene en PolynomialFeatures
)
model.fit(X_train, y_train)
```

El pipeline es UN estimador: `fit` ejecuta `fit_transform` de cada paso intermedio y `fit` del último. `predict` aplica `transform` y luego `predict`. Te evita data leakage gratis.

## 4. Ejemplo numérico

Recreemos el problema "0 dimensión" del notebook 01 (celda 12) — calcular el promedio como solución de mínimos cuadrados:

```python
import numpy as np

notas = np.array([6, 7, 8, 7, 9, 6, 8])

# Vía 1: promedio aritmético
print(notas.mean())               # 7.2857...

# Vía 2: minimizando E(a) = Σ(y_i - a)²  →  a* = mean(y)
N = notas.shape[0]
a_optimo = notas.sum() / N
print(a_optimo)                   # 7.2857...

# Verificación: E(a) es parábola con mínimo en a*
def E(a):
    return ((notas - a) ** 2).sum()

for a in [6.0, 7.0, 7.2857, 8.0]:
    print(f"E({a}) = {E(a):.4f}")
# E(6.0)    = 14.0000
# E(7.0)    = 5.0000
# E(7.2857) = 4.8571   ← mínimo
# E(8.0)    = 7.0000
```

> **Frase rectora de la cátedra (notebook 01, celda 15):** "El promedio no aparece como una receta: aparece como la solución del problema de minimizar el error cuadrático."

Mismo ejemplo con broadcasting (todo el barrido en una línea):

```python
a_grid = np.linspace(5, 10, 100)              # shape (100,)
errores = ((notas[:, None] - a_grid) ** 2).sum(axis=0)  # broadcasting (7,1) - (100,) → (7,100) → sum → (100,)
a_min = a_grid[errores.argmin()]
print(a_min)                                  # ~7.27 (resolución del grid)
```

Acá `notas[:, None]` agrega un eje para que broadcasting alinee `(7, 1)` con `(100,)` → resultado `(7, 100)`.

## 5. Conexión con el TP

**Ejercicio 2 (TP1, cell-14):** "Para cada atributo, hacer una gráfica que muestre su relación con el target."

El código de ejemplo de la cátedra usa el patrón:

```python
selector = np.array(california['feature_names']) == feature
plt.scatter(X[:, selector], y)
```

**TRAMPA #1 (DataFrame vs ndarray):** si `X` es DataFrame, `X[:, selector]` rompe (ver §3.5). Usá una de las tres salidas.

**TRAMPA #2 (shape):** `X[:, selector]` con un mask booleano de 1 valor `True` devuelve shape `(N, 1)` — eso es lo que sklearn quiere. Si en cambio hicieras `X[:, 0]` (indexación entera 1D), obtenés `(N,)` y `LinearRegression.fit` se queja.

**Ejercicio 3 (TP1, cell-19):** "Instanciar regresión lineal de sklearn y entrenarla con un atributo."

```python
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

selector = np.array(california['feature_names']) == 'MedInc'
X_train_sel = X_train[:, selector]   # (n, 1)

model = LinearRegression()
model.fit(X_train_sel, y_train)
y_pred_train = model.predict(X_train_sel)
y_pred_test  = model.predict(X_test[:, selector])

mse_train = mean_squared_error(y_train, y_pred_train)
mse_test  = mean_squared_error(y_test,  y_pred_test)
```

**Atención escala:** el target está en unidades de $100\,000$ USD. Un MSE de "50" no significa "promedio de error 50 USD" — es $50 \times (100\,000)^2$ USD². El enunciado del TP es ambiguo en esto (lo dice "< 50" sin aclarar).

**Ejercicio 4 (TP1, cell-26):** "Para varios grados de polinomio…" — acá entran `PolynomialFeatures` + `LinearRegression` en pipeline (ver §3.8).

## 6. Errores comunes

1. **`shape (n,)` vs `shape (n, 1)`** — sklearn pide 2-D para `X`. Fix: `X.reshape(-1, 1)` o `X[:, None]`.
2. **DataFrame vs ndarray en indexación booleana** — `X[:, mask]` falla en DataFrame. Fix: `X.values[:, mask]`, `X.iloc[:, mask]`, o `as_frame=False` (TP1, todos los ejercicios).
3. **`np.linalg.inv` con matriz singular** — explota en grado polinomial alto. Fix: `pinv` (la cátedra ya lo aplica en el notebook 01 celda 31) o `lstsq`.
4. **`fit` sobre test set** — leakage. `fit` SOLO con train. `transform` con todo.
5. **`fit_intercept=True` con `PolynomialFeatures`** — duplicás el bias (el grado 0 ya es la columna de 1s). La cátedra lo aclara en notebook 01 celda 43: `fit_intercept=False`.
6. **`random_state=None`** — corridas no reproducibles. Fijá `random_state=0` (o el que use la cátedra) para coincidir con los números del enunciado.
7. **Broadcasting "silencioso"** — `(N,)` y `(N, 1)` se broadcastean a `(N, N)` sin avisar. Si una operación devuelve un shape extraño, chequeá los shapes de entrada PRIMERO.
8. **`copy` vs `view`** — `A[1:3]` devuelve VISTA, no copia. Modificar la vista modifica `A`. Si querés independencia: `A[1:3].copy()`.
9. **`int` vs `float` en arrays** — `np.array([1, 2, 3]) / 2` devuelve `[0.5, 1.0, 1.5]` (Python 3, división verdadera). Pero `np.array([1, 2, 3], dtype=int) // 2` devuelve `[0, 1, 1]`. Conocé tu dtype.
10. **`@` vs `*`** — `A @ B` es producto matricial; `A * B` es producto elemento a elemento (Hadamard). NO son lo mismo. Confusión clásica.
11. **`mean_squared_error(..., squared=False)` deprecado** — desde sklearn 1.4 usá `root_mean_squared_error`. Si tu versión es vieja, `squared=False` aún anda.

## 7. Checklist de comprensión

- [ ] Sé la diferencia entre `(N,)` y `(N, 1)` y cuándo cada uno.
- [ ] Puedo explicar por qué `pinv` es preferible a `inv` en regresión lineal.
- [ ] Sé reconocer cuándo `X` es DataFrame vs ndarray y aplicar las 3 soluciones del TP1.
- [ ] Entiendo qué hace `random_state` y por qué la cátedra lo fija.
- [ ] Sé instanciar un `LinearRegression`, llamar a `fit`, `predict`, `score`.
- [ ] Puedo construir un pipeline `PolynomialFeatures` → `LinearRegression`.
- [ ] Conozco las 3 reglas del broadcasting y sé cuándo agregar `None` para alinear ejes.
- [ ] Sé diferenciar `@` (producto matricial) de `*` (Hadamard).
- [ ] Puedo describir el patrón `fit`/`predict`/`transform` y por qué se diseña así.
- [ ] Sé que `fit_intercept=False` se usa cuando `PolynomialFeatures` ya genera el grado 0.

## 8. Para profundizar

- **NumPy** — la doc oficial es de las mejores del ecosistema Python. Empezá por el "Absolute beginner's guide" y después *Broadcasting* (numpy docs, [`numpy.org/doc/stable/user/basics.broadcasting.html`](https://numpy.org/doc/stable/user/basics.broadcasting.html)).
- **scikit-learn user guide** — el capítulo *Common pitfalls and recommended practices* es lectura obligatoria para evitar leakage y errores reproducibilidad.
- **VanderPlas, *Python Data Science Handbook*** — capítulo 2 (NumPy), §2.5 broadcasting. Disponible gratis online.
- **McKinney, *Python for Data Analysis* (3ed, 2022)** — capítulo 4 (NumPy basics) y 5 (pandas).
- **sklearn docs, *Developing scikit-learn estimators*** — explica el contrato del API. Útil incluso si nunca vas a crear un estimator propio: te hace entender por qué todos los `fit/predict` se comportan igual.

## Próximo paso

→ [01-marco-general-aa.md](01-marco-general-aa.md)

## Referencias

- NumPy User Guide — Broadcasting: <https://numpy.org/doc/stable/user/basics.broadcasting.html>
- NumPy Reference — `numpy.linalg.pinv`: <https://numpy.org/doc/stable/reference/generated/numpy.linalg.pinv.html>
- scikit-learn — `train_test_split`: <https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html>
- scikit-learn — Developing scikit-learn estimators (API design): <https://scikit-learn.org/stable/developers/develop.html>
- VanderPlas, J. (2016). *Python Data Science Handbook*, O'Reilly. Disponible en: <https://jakevdp.github.io/PythonDataScienceHandbook/>
- Material de cátedra: notebooks 01 y 02 (DiploDatos UNC, IAA 2026); TP1 *Trabajo_Practico_1.ipynb* (California Housing).
