# 05 — Regularización Ridge (L2)

> **Tema:** penalización L2 sobre los coeficientes, solución cerrada Ridge, efecto del hiperparámetro $\lambda$, y diferencia con Lasso (L1).
> **Material base:** Clase 1 — Bloque B (PDF p.24–27), Ejercicio 7 (opcional) del TP1.
> **Bibliografía:** Bishop (2006) §3.1.4, ESL (Hastie et al., 2009) §3.4, Hoerl & Kennard (1970), Tibshirani (1996).

---

## 1. Concepto

La **regularización Ridge** (también llamada regularización L2, *weight decay* o *Tikhonov regularization*) modifica la función de costo de la regresión lineal añadiendo un término que **penaliza la norma cuadrática** de los pesos (Clase 1, PDF p.24):

$$
\tilde{E}(\mathbf{w}) = E(\mathbf{w}) + \frac{\lambda}{2}\|\mathbf{w}\|^2 = \frac{1}{2}\sum_{n=1}^{N}\bigl(y(\mathbf{x}_n, \mathbf{w}) - y_n\bigr)^2 + \frac{\lambda}{2}\sum_{j=0}^{M} w_j^2
$$

donde $\lambda \geq 0$ es el **hiperparámetro de regularización** (Bishop, 2006, §3.1.4, ec. 3.27). Esta formulación se conoce desde 1970 — Hoerl y Kennard la introdujeron para resolver problemas de **multicolinealidad** en regresión múltiple (Hoerl & Kennard, 1970, *Technometrics*).

> **Resultado fundamental (PDF p.27, literal):** "La regularización Ridge solo añade $\lambda \mathbf{I}$ a la matriz a invertir."

Es decir, la solución cerrada cambia mínimamente respecto del cap. 03:

$$
\boxed{\;\mathbf{w}^*_{\text{ridge}} = (\mathbf{Z}^T \mathbf{Z} + \lambda \mathbf{I})^{-1} \mathbf{Z}^T \mathbf{y}\;}
$$

Tres consecuencias inmediatas:
1. **Sigue siendo analítica.** No hay iteración.
2. **$\lambda > 0$ vuelve invertible $\mathbf{Z}^T\mathbf{Z} + \lambda \mathbf{I}$**, incluso si $\mathbf{Z}^T\mathbf{Z}$ era singular. Ridge es un **estabilizador numérico**, no sólo un regularizador estadístico.
3. **Cuando $\lambda \to 0$** recuperamos la regresión lineal estándar; cuando $\lambda \to \infty$, todos los $w_j \to 0$ (el modelo colapsa al cero).

---

## 2. Intuición

Imaginate que cada coeficiente $w_j$ es una **palanca** que el modelo puede mover. Sin regularización, las palancas son **gratis**: el optimizador las tira hasta donde haga falta para minimizar el error de train, incluso si eso implica $w_j = 10^4$ (PDF p.23 — los coeficientes a $M=9$ llegan a 9276.55).

Ridge le pone un **resorte** a cada palanca. El optimizador todavía puede moverlas, pero ahora paga **un costo cuadrático**: tirar una palanca a $|w_j|=10$ cuesta 100 unidades de costo extra. Si querés moverla a 100, pagás 10.000. Como el costo crece **cuadráticamente**, el optimizador prefiere distribuir el "ajuste" entre muchas palancas en lugar de tirar de una sola.

**Resultado:** los coeficientes **se achican** uniformemente — quedan **pequeños y estables** en lugar de explotar. La regularización funciona porque, en presencia de ruido, **modelos con coeficientes chicos generalizan mejor** que modelos con coeficientes gigantes que pasan exactamente por los puntos de train (ESL §3.4.1).

> "Con regularización fuerte ($\ln \lambda = 0$), los coeficientes son pequeños y estables: el modelo captura la tendencia real sin memorizar el ruido." (PDF p.25, literal)

Hay otra lectura igualmente útil — la **interpretación bayesiana**: si ponés un prior gaussiano $\mathbf{w} \sim \mathcal{N}(0, \tau^2 \mathbf{I})$ sobre los pesos y hacés MAP (Maximum A Posteriori) bajo verosimilitud gaussiana, **te sale exactamente Ridge con $\lambda = \sigma^2/\tau^2$** (Bishop, 2006, §3.3; Murphy, 2022, §11.6). Es decir: regularizar = creer a priori que los pesos deberían ser chicos.

---

## 3. Cuerpo técnico

### 3.1 Derivación de la solución cerrada

Partimos del costo regularizado en forma matricial:

$$
\tilde{E}(\mathbf{w}) = \frac{1}{2}(\mathbf{Z}\mathbf{w} - \mathbf{y})^T(\mathbf{Z}\mathbf{w} - \mathbf{y}) + \frac{\lambda}{2}\mathbf{w}^T\mathbf{w}
$$

Gradiente respecto de $\mathbf{w}$:

$$
\nabla_{\mathbf{w}} \tilde{E} = \mathbf{Z}^T \mathbf{Z} \mathbf{w} - \mathbf{Z}^T \mathbf{y} + \lambda \mathbf{w} = (\mathbf{Z}^T \mathbf{Z} + \lambda \mathbf{I})\mathbf{w} - \mathbf{Z}^T \mathbf{y}
$$

Igualando a cero:

$$
\mathbf{w}^*_{\text{ridge}} = (\mathbf{Z}^T \mathbf{Z} + \lambda \mathbf{I})^{-1} \mathbf{Z}^T \mathbf{y}
$$

(Bishop, 2006, ec. 3.28; ESL §3.4.1, ec. 3.44.)

### 3.2 Por qué $\lambda \mathbf{I}$ resuelve el mal condicionamiento

Si $\mathbf{Z}^T \mathbf{Z}$ tiene valores propios $\{s_i^2\}$ (cuadrados de los valores singulares de $\mathbf{Z}$), entonces $\mathbf{Z}^T \mathbf{Z} + \lambda \mathbf{I}$ tiene valores propios $\{s_i^2 + \lambda\}$. **El menor de ellos pasa de $s_{\min}^2$ a $s_{\min}^2 + \lambda$**, lo que reduce el número de condición de la matriz:

$$
\kappa(\mathbf{Z}^T\mathbf{Z} + \lambda \mathbf{I}) = \frac{s_{\max}^2 + \lambda}{s_{\min}^2 + \lambda} \;\leq\; \kappa(\mathbf{Z}^T\mathbf{Z})
$$

Por eso Ridge **siempre tiene solución** incluso con $N < M+1$ (más features que muestras), y es la forma estándar de regularización en problemas mal-pose (Tikhonov, en su origen matemático).

### 3.3 Efecto de $\lambda$ — TABLA CANÓNICA

La cátedra muestra el efecto sobre los coeficientes con $M=9$ y datos sinusoidales (PDF p.25). Esta tabla es **literal del material**:

| Coef. | $\ln \lambda = -\infty$ (sin reg.) | $\ln \lambda = -18$ | $\ln \lambda = 0$ |
|:------|----------------------------------:|--------------------:|------------------:|
| $w_0^*$ | 0.00 | 0.00 | 0.00 |
| $w_1^*$ | -24.82 | 6.50 | -0.64 |
| $w_2^*$ | -704.18 | 6.19 | -0.63 |
| $w_3^*$ | -6347.68 | -131.53 | -0.45 |
| $w_4^*$ | 29667.37 | 292.01 | -0.28 |
| $w_9^*$ | -18408.52 | -207.10 | 0.04 |

**Lectura:**
- **Sin regularización**: los coeficientes alcanzan ~$10^4$ — el modelo está interpolando ruido (ver cap. 04).
- **$\lambda = e^{-18} \approx 1.5 \times 10^{-8}$**: una micro-regularización ya los frena a ~$10^2$.
- **$\lambda = e^0 = 1$**: los coeficientes son todos menores que 1 en valor absoluto. El modelo es "suave" (PDF p.24).

Y los errores (PDF p.24, $M=9$ fijo):

| Régimen | $\ln \lambda$ | train RMSE | val RMSE | Diagnóstico |
|---------|-------------:|----------:|---------:|-------------|
| Bajo $\lambda$ | $-18$ | 0.165 | 0.219 | Overfitting moderado |
| Alto $\lambda$ | $0$ | 0.450 | 0.468 | Modelo "suave" |

**La forma del trade-off:** train RMSE sube con $\lambda$ (más regularización = peor ajuste); val RMSE tiene **forma de U** con un mínimo en algún $\lambda^*$ que no es ni 0 ni $\infty$. **Ese $\lambda^*$ se busca con validación cruzada** (`RidgeCV` en sklearn, ver §3.5).

### 3.4 Convención $\lambda$ vs `alpha` — TRAMPA SKLEARN

`sklearn.linear_model.Ridge` parametriza con `alpha`, **no $\lambda$**. La correspondencia, según la documentación oficial, es:

$$
\text{sklearn: } \min_{\mathbf{w}} \|\mathbf{Z}\mathbf{w} - \mathbf{y}\|^2 + \alpha\|\mathbf{w}\|^2
$$

Comparando con la cátedra (Bishop):

$$
\text{cátedra: } \min_{\mathbf{w}} \tfrac{1}{2}\|\mathbf{Z}\mathbf{w} - \mathbf{y}\|^2 + \tfrac{\lambda}{2}\|\mathbf{w}\|^2
$$

**Las dos son equivalentes salvo factores:** sklearn no lleva el $\tfrac{1}{2}$, así que numéricamente $\alpha_{\text{sklearn}} = \lambda_{\text{Bishop}}$ (al cancelarse los $1/2$). Pero ojo: **otras librerías y autores varían** (algunos usan $\lambda/N$, otros $\lambda \cdot 2$). **Antes de mover el hiperparámetro a ciegas, leé la fórmula exacta de la librería que estés usando.** (sklearn docs, *Ridge*; ESL §3.4.1.)

> **Mnemotécnica:** en sklearn, **`alpha` grande = regularización fuerte**. `alpha=0` equivale a `LinearRegression`. `alpha=∞` colapsa todo a cero.

### 3.5 Implementación con sklearn

```python
from sklearn.linear_model import Ridge, RidgeCV
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.metrics import mean_squared_error
import numpy as np

# Pipeline polinomial + Ridge
model = make_pipeline(
    StandardScaler(),                       # MUY recomendado con polinomios
    PolynomialFeatures(9, include_bias=True),
    Ridge(alpha=1.0, fit_intercept=False)   # fit_intercept=False porque ya viene en PolyFeatures
)
model.fit(X_tr, y_tr)
mse = mean_squared_error(y_te, model.predict(X_te))
```

**Búsqueda de $\alpha$ por CV:**

```python
alphas = np.logspace(-6, 3, 50)
ridge_cv = make_pipeline(
    StandardScaler(),
    PolynomialFeatures(9, include_bias=True),
    RidgeCV(alphas=alphas, fit_intercept=False, cv=5)
)
ridge_cv.fit(X_tr, y_tr)
print('alpha óptimo:', ridge_cv.named_steps['ridgecv'].alpha_)
```

`RidgeCV` por dentro hace **leave-one-out CV de forma analítica** (gracias a que Ridge tiene solución cerrada — un truco que no es posible con Lasso). Es **muy rápido**, mucho más que `GridSearchCV(Ridge, ...)`.

### 3.6 Ridge vs Lasso — la diferencia geométrica

Aunque la cátedra **sólo cubre Ridge**, vale la pena tener el contraste con Lasso (L1) en la cabeza, porque aparece en TODA la bibliografía moderna (ESL §3.4):

| Aspecto | Ridge (L2) | Lasso (L1) |
|---------|-----------|-----------|
| Penalización | $\lambda \sum w_j^2$ | $\lambda \sum |w_j|$ |
| Solución | Cerrada, $(\mathbf{Z}^T\mathbf{Z} + \lambda \mathbf{I})^{-1}\mathbf{Z}^T\mathbf{y}$ | Iterativa (coordinate descent, LARS) |
| Efecto sobre coeficientes | **Encoge** (shrink) — nunca a exactamente 0 | **Selecciona** — pone $w_j = 0$ |
| Cuándo usar | Muchas features, todas posiblemente relevantes | Pocas features relevantes, muchas irrelevantes |
| Origen histórico | Hoerl & Kennard, 1970 | Tibshirani, 1996 |

La diferencia geométrica clave: la **bola L2** ($\|\mathbf{w}\|_2 \leq t$) es una esfera, las restricciones tocan a las curvas de nivel del MSE **en cualquier dirección**; la **bola L1** ($\|\mathbf{w}\|_1 \leq t$) es un romboide, con **vértices sobre los ejes**, donde es muy probable que las curvas de nivel toquen — y en esos vértices algunos $w_j$ son exactamente 0. Por eso Lasso **hace feature selection automática**. (Ver figura 3.11 de ESL para la visualización clásica.)

Si querés lo mejor de ambos mundos, mirá **Elastic Net** (`sklearn.linear_model.ElasticNet`), que combina L1 + L2.

### 3.7 Por qué no se penaliza el bias $w_0$

Convención estándar (no siempre explícita): **el bias $w_0$ NO debería entrar en $\|\mathbf{w}\|^2$**. Penalizar el intercepto sesga el modelo hacia $\hat{y}=0$, lo cual sólo tiene sentido si tu target está centrado en cero (ESL §3.4.1).

`sklearn.linear_model.Ridge` con `fit_intercept=True` **internamente excluye** el intercepto de la penalización — primero centra los datos, entrena Ridge sobre las features centradas, y recupera el intercepto al final. Si usás `fit_intercept=False` (porque tu pipeline ya tiene la columna de unos vía `PolynomialFeatures`), **estás penalizando $w_0$** y los resultados van a ser ligeramente distintos. En la práctica, con `StandardScaler` antes, el sesgo es chico, pero conviene saberlo.

---

## 4. Ejemplo numérico

Reproducimos la dinámica de la PDF p.24-25:

```python
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error

def create_sinusoidal_data(spread=0.10, data_size=20):
    np.random.seed(0)
    x = np.linspace(0, 1, data_size)
    y = np.sin(2*np.pi*x) + np.random.normal(scale=spread, size=x.shape)
    return x.reshape(-1,1), y

X_tr, y_tr = create_sinusoidal_data(0.10, 20)
X_te, y_te = create_sinusoidal_data(0.10, 100)   # eval con más puntos

phi = PolynomialFeatures(9, include_bias=True)
Z_tr = phi.fit_transform(X_tr)
Z_te = phi.transform(X_te)

print(f'{"ln(λ)":>6s} {"train RMSE":>12s} {"val RMSE":>10s} {"|w|_∞":>10s}')
for ln_lam in [-np.inf, -18, -10, -5, 0, 3]:
    lam = 0.0 if ln_lam == -np.inf else np.exp(ln_lam)
    model = Ridge(alpha=lam, fit_intercept=False).fit(Z_tr, y_tr)
    pred_tr = model.predict(Z_tr)
    pred_te = model.predict(Z_te)
    rmse_tr = np.sqrt(mean_squared_error(y_tr, pred_tr))
    rmse_te = np.sqrt(mean_squared_error(y_te, pred_te))
    w_max = np.max(np.abs(model.coef_))
    print(f'{ln_lam:>6.1f} {rmse_tr:>12.4f} {rmse_te:>10.4f} {w_max:>10.2f}')
```

**Lo que vas a observar:**
- Con $\ln \lambda = -\infty$ (= sin regularización): RMSE train $\sim 0.13$, RMSE val mucho mayor, $\|\mathbf{w}\|_\infty$ del orden de $10^4$.
- Con $\ln \lambda = -5$ a $0$: RMSE val MÍNIMO, $\|\mathbf{w}\|_\infty < 10$. Sweet spot.
- Con $\ln \lambda = 3$: RMSE train sube, RMSE val también — sobre-regularizado (underfit por exceso de penalización).

La curva de **val RMSE en función de $\ln \lambda$** tiene forma de **U**, exactamente igual que la curva de val RMSE en función de $M$ del cap. 04. **Misma matemática, distinto hiperparámetro** — siempre que aumentás capacidad efectiva (más $M$, menos $\lambda$), pasás de underfit a overfit por un punto óptimo.

---

## 5. Conexión con el TP

**Ejercicio 7 (opcional)** del TP1 (cell-36) pide exactamente esto: probar Ridge con varios `alpha` sobre California Housing.

```python
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_squared_error
import numpy as np

alphas = np.logspace(-3, 3, 13)
errores = []

for alpha in alphas:
    model = make_pipeline(
        StandardScaler(),
        PolynomialFeatures(degree=3, include_bias=True),
        Ridge(alpha=alpha, fit_intercept=False)
    )
    model.fit(X_train, y_train)
    e_tr = mean_squared_error(y_train, model.predict(X_train))
    e_te = mean_squared_error(y_test,  model.predict(X_test))
    errores.append((alpha, e_tr, e_te))
    print(f'alpha={alpha:>8.4f}  MSE_tr={e_tr:.4f}  MSE_te={e_te:.4f}')
```

**Observaciones que esperás encontrar:**
- El MSE de train sube monotónicamente con `alpha`.
- El MSE de test tiene un mínimo en algún `alpha` intermedio.
- Si el mejor `alpha` te sale muy chico ($\sim 10^{-3}$), tu modelo no estaba sobreajustado; si te sale grande ($\sim 10^2$), había overfit serio.

El enunciado **no pide CV**, pero usar `RidgeCV` te ahorra escribir el loop:

```python
ridge_cv = RidgeCV(alphas=np.logspace(-3, 3, 50), cv=5)
ridge_cv.fit(X_train_scaled, y_train)
print('alpha óptimo:', ridge_cv.alpha_)
```

**Trampa:** el TP1 enuncia "regresiones con regularización ridge" sin especificar grado polinomial. Probá combinaciones: `(degree, alpha)` con `degree in [1,2,3]` y `alpha in logspace(-3,3,7)`. Es un mini **grid search** manual.

---

## 6. Errores comunes

1. **No escalar las features antes de Ridge.** Ridge penaliza $\|\mathbf{w}\|^2$ uniformemente, pero $w_j$ tiene unidades de "target / feature$_j$". Si las features tienen escalas muy distintas (ej: `MedInc` $\sim 1$ vs `Population` $\sim 1000$), Ridge va a penalizar más al de escala chica. **Siempre usá `StandardScaler` antes de Ridge.** (ESL §3.4.1, recomendación estándar.)
2. **Confundir `alpha` sklearn con $\lambda$ de Bishop.** Numéricamente coinciden en magnitud porque sklearn no lleva el $\tfrac{1}{2}$ y Bishop sí, pero en general **siempre confirmá la fórmula de la librería** antes de comparar valores entre fuentes. Ver §3.4.
3. **Penalizar el intercepto sin querer.** Si usás `Ridge(fit_intercept=False)` con `PolynomialFeatures(include_bias=True)`, estás penalizando $w_0$. Para datos centrados puede no importar; para datos crudos sí importa.
4. **Usar Ridge para feature selection.** Ridge **encoge** los coeficientes pero **no los hace exactamente 0**. Si querés selección automática, usá Lasso o ElasticNet.
5. **Asumir que más regularización siempre es mejor.** Aumentar $\lambda$ baja la varianza pero **sube el bias**. Hay un sweet spot — y se encuentra con CV, no a ojo (ESL §7.10).
6. **No graficar la curva de validación.** Sin la curva train/val vs $\lambda$, no podés diagnosticar si estás del lado underfit o overfit. **Graficala siempre.**
7. **Pensar que Ridge "elimina" features.** Sólo las achica. Para eliminar (set a 0), Lasso.

---

## 7. Checklist de comprensión

- [ ] Puedo escribir el costo regularizado $\tilde{E}(\mathbf{w}) = E(\mathbf{w}) + \tfrac{\lambda}{2}\|\mathbf{w}\|^2$ y derivar la solución $\mathbf{w}^* = (\mathbf{Z}^T\mathbf{Z} + \lambda\mathbf{I})^{-1}\mathbf{Z}^T\mathbf{y}$.
- [ ] Entiendo por qué $\lambda \mathbf{I}$ vuelve invertible a $\mathbf{Z}^T\mathbf{Z}$ incluso si era singular.
- [ ] Sé que `alpha` en sklearn juega el rol de $\lambda$, y entiendo la convención de factores.
- [ ] Identifico la forma en U de la curva val-RMSE vs $\lambda$.
- [ ] Distingo Ridge (L2, encoge) de Lasso (L1, selecciona), aunque sólo cubrimos Ridge.
- [ ] Sé por qué hay que escalar features antes de Ridge.
- [ ] Sé que el intercepto típicamente no se penaliza, y entiendo cómo lo maneja sklearn por dentro.
- [ ] Puedo resolver el Ej. 7 del TP1 con `Ridge` o `RidgeCV`.
- [ ] Entiendo la conexión bayesiana: Ridge = MAP con prior gaussiano sobre $\mathbf{w}$.

---

## 8. Para profundizar

- **Hoerl & Kennard (1970)** — paper original de Ridge, *Technometrics* 12(1), 55-67. La motivación NO era ML moderno sino **multicolinealidad en regresión múltiple** (cuando dos columnas de $\mathbf{Z}$ son casi colineales y $\mathbf{Z}^T\mathbf{Z}$ se vuelve mal condicionada). El "ridge trace" — el gráfico de $w_j(\lambda)$ vs $\lambda$ — viene de este paper. Disponible en <https://homepages.math.uic.edu/~lreyzin/papers/ridge.pdf>
- **Tibshirani (1996)** — paper original de Lasso, JRSS-B 58(1), 267-288. Para entender por qué L1 selecciona y L2 no.
- **Bishop, 2006, §3.1.4** — tratamiento formal de regularización, conexión con MAP. §3.3 cubre Bayesian linear regression (sin parámetro fijo $\lambda$ — se aprende también).
- **ESL §3.4** (Hastie et al., 2009) — comparación profunda Ridge vs Lasso vs Best-Subset; sección 3.4.1 deriva la conexión con SVD y el "effective degrees of freedom" $\text{df}(\lambda) = \sum_i \frac{s_i^2}{s_i^2 + \lambda}$. ESL §3.4.4 cubre Elastic Net.
- **Murphy (2022), §11.6** — versión bayesiana moderna, conexión con weight decay en deep learning.
- **sklearn docs — `Ridge` y `RidgeCV`** — implementación, solvers (`auto`, `svd`, `cholesky`, `lsqr`, `sparse_cg`, `sag`, `saga`), y cuándo usar cada uno. <https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Ridge.html>

---

## Próximo paso

→ [06-clasificacion-y-perceptron.md](06-clasificacion-y-perceptron.md)

---

## Referencias

- Hoerl, A. E. & Kennard, R. W. (1970). Ridge regression: biased estimation for nonorthogonal problems. *Technometrics*, 12(1), 55-67. <https://www.tandfonline.com/doi/abs/10.1080/00401706.1970.10488634>
- Tibshirani, R. (1996). Regression shrinkage and selection via the Lasso. *Journal of the Royal Statistical Society Series B*, 58(1), 267-288. <https://rss.onlinelibrary.wiley.com/doi/10.1111/j.2517-6161.1996.tb02080.x>
- Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*. Springer. §3.1.4, §3.3.
- Hastie, T., Tibshirani, R. & Friedman, J. (2009). *The Elements of Statistical Learning* (2nd ed.). Springer. §3.4, §7.10.
- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press. §11.6.
- Meinardi, V. & Bonzi, E. (2026). *Introducción al Aprendizaje Automático — Clase 1*. DiploDatos UNC FAMAF. PDF slides 24–27.
- scikit-learn developers (2026). *`sklearn.linear_model.Ridge`* — <https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Ridge.html>
- scikit-learn user guide §1.1.2 — *Ridge regression and classification* — <https://scikit-learn.org/stable/modules/linear_model.html#ridge-regression>
