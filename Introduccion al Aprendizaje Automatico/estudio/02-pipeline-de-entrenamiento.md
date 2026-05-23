# 02 — El pipeline de entrenamiento

> **Mapa del capítulo.** En el capítulo 01 vimos QUÉ es ML. Acá vemos CÓMO se entrena un modelo, paso por paso. Es el diagrama de flujo de la slide 14 del PDF Clase 1 desplegado con detalle: cómo se particionan los datos, cómo se define una función de costo, cómo se itera, qué se monitorea, cómo se evalúa. Es la "infraestructura conceptual" sobre la que se montan TODOS los modelos que siguen (regresión, perceptrón, logística, NB, KNN).

## 1. Concepto

Un **pipeline de entrenamiento supervisado** es el procedimiento que transforma un dataset etiquetado $\mathcal{D} = \{(x_i, y_i)\}_{i=1}^N$ en un **modelo entrenado** $f_{\mathbf{w}^*}: \mathcal{X} \to \mathcal{Y}$ con parámetros $\mathbf{w}^*$ que minimizan una **función de costo** sobre el conjunto de entrenamiento, sujeto a buena generalización en datos no vistos.

Versión cátedra (PDF Clase 1, p. 14): el pipeline tiene 5 componentes acoplados:

```
DATASET ─┬─> TRAIN ──┐
         ├─> VAL ────┼─> CICLO DE OPTIMIZACIÓN ──> w* (PARÁMETROS)
         └─> TEST ───┘   ↑                            │
                         │ (HIPERPARÁMETROS)          │
                         └────────────────────────────┘
                                       │
                                       ├─> FUNCIÓN DE COSTO ──> PREDICCIONES
                                       └─> MONITOREO + CURVA DE PÉRDIDA
```

Goodfellow et al. (§5.3, 2016) lo formaliza así: *"What separates machine learning from optimization is that we want the generalization (test) error to be low, not just the training error."*

> **Idea de fondo.** Optimización clásica minimiza una función en SU dominio. ML minimiza una función EN TRAIN con la esperanza de que el mínimo se traslade a TEST. Esa esperanza requiere supuestos (i.i.d., representatividad, regularización, etc.) — todo lo que sigue es maquinaria para hacer válida esa esperanza.

## 2. Intuición

Pensá el entrenamiento como **preparar a alguien para un examen**:

- **Train set** = los ejercicios que practicás en casa con la solución delante.
- **Validation set** = los simulacros que hacés sin mirar la solución para ver cómo vas (y para decidir si necesitás otra estrategia de estudio: más tiempo, otro libro, etc.).
- **Test set** = EL examen real. Lo abrís UNA VEZ, al final.

Si usás el simulacro para decidir qué estudiar, entonces el simulacro deja de ser válido como predictor de tu desempeño — porque te "ajustaste" a él. Y si usás el examen real para decidir qué estudiar, ya rompiste todo: tu nota no significa nada respecto a tu capacidad general.

La cátedra usa una analogía equivalente del libro de Bishop (§1.1): el modelo NO debe **memorizar**, debe **aprender la regularidad subyacente**. Memorizar = test error >> train error. Aprender = ambos errores bajos y cercanos.

## 3. Cuerpo técnico

### 3.1 — La partición de datos: train / val / test

**Razón estadística (Murphy §1.4, Goodfellow §5.3).** Si midiéramos el error en los mismos datos con los que entrenamos, obtendríamos una estimación **optimista sesgada** (subestima el error real). Para estimar el error de generalización (lo que importa), necesitamos datos NUEVOS.

**Tres conjuntos, tres funciones:**

| Conjunto | Para qué se usa | Cuántas veces se mira |
|----------|-----------------|----------------------|
| **Train** | Aprender parámetros $\mathbf{w}$ vía optimización | Una vez por iteración (epoch) |
| **Validation (val)** | Elegir hiperparámetros (grado M, $\lambda$, k, learning rate, etc.) | Una vez por config |
| **Test** | Estimación final, honesta, del error de generalización | UNA VEZ al final |

**Proporciones típicas (Goodfellow §5.3):** 60/20/20 o 80/10/10 o 70/15/15. NO HAY regla universal — depende del tamaño total. Con $N=10^9$ podés vivir con 99/0.5/0.5.

> **Nota cátedra:** la slide 14 del PDF muestra el triple split. Pero los notebooks 01 y 02 sólo usan train/val (sin test) — es una simplificación didáctica. En problemas reales (y en el TP1) usás train/test.

**Codigo en sklearn (cátedra notebook 01, celda 28):**

```python
from sklearn.model_selection import train_test_split

# Para train / test
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=0)

# Para train / val / test: dos splits anidados
X_temp, X_test, y_temp, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
X_train, X_val, y_train, y_val = train_test_split(X_temp, y_temp, test_size=0.25, random_state=0)
# resultado: 60% / 20% / 20%
```

**Validación cruzada (k-fold).** No está en el material cátedra, pero es la práctica estándar cuando $N$ es chico (cientos a pocos miles): divide train en k folds, entrena k veces rotando el fold de validación, promedia el score. Ventaja: usás todos los datos para "validar" sin desperdiciar nada. Costo: k veces más cómputo. Ver Hastie, Tibshirani & Friedman (ESL §7.10).

### 3.2 — La función de costo

Una **función de costo** $E(\mathbf{w})$ (o $J(\mathbf{w})$, o $L(\mathbf{w})$ — la cátedra usa $E$) es una medida ESCALAR de qué tan mal predice el modelo con parámetros $\mathbf{w}$ sobre el conjunto de entrenamiento. Es la cantidad que el algoritmo de optimización minimiza.

**Propiedades deseables:**
1. **Diferenciable** (al menos casi en todas partes) — para usar gradiente descendente.
2. **Convexa** en $\mathbf{w}$ (si es posible) — garantiza mínimo global único.
3. **Penaliza fuerte los errores grandes** o **suaviza con probabilidades** (depende del problema).

#### 3.2.1 — MSE: Mean Squared Error (caso canónico de regresión)

La cátedra introduce MSE en la PDF Clase 1, p. 19, como **suma de cuadrados con factor 1/2**:

$$
E(\mathbf{w}) = \frac{1}{2} \sum_{n=1}^{N} (y(x_n, \mathbf{w}) - t_n)^2
$$

> **El factor 1/2** es una conveniencia matemática — al derivar, el 2 cancela y queda $\sum (\hat y - t) \cdot \nabla_w \hat y$. No cambia el argmin (es una constante). Bishop (§1.1) y casi toda la bibliografía usan esta forma.

**MSE (versión estándar de ML, con promedio):**

$$
\text{MSE}(\mathbf{w}) = \frac{1}{N} \sum_{n=1}^N (\hat y_n - y_n)^2
$$

**RMSE (Root Mean Squared Error):**

$$
\text{RMSE} = \sqrt{\text{MSE}} = \sqrt{\frac{1}{N}\sum (\hat y_n - y_n)^2}
$$

La cátedra usa $E_{RMS} = \sqrt{2E(\mathbf{w}^*)/N}$ (PDF p. 21) — equivalente a RMSE estándar gracias al factor 1/2.

**¿Por qué CUADRADO y no valor absoluto?**
- **Diferenciable** en todas partes (el valor absoluto no es diferenciable en 0).
- **Penaliza más los errores grandes** — un error de 10 cuenta 100, dos errores de 5 cuentan 25+25=50.
- **Relación con MLE bajo ruido gaussiano** — minimizar MSE equivale a maximum likelihood asumiendo $\epsilon \sim \mathcal{N}(0, \sigma^2)$ (Bishop §1.2.5).

**Alternativas (no en cátedra pero útiles saber):**
- **MAE** (Mean Absolute Error): $\frac{1}{N}\sum |\hat y - y|$ — más robusto a outliers, no diferenciable en 0.
- **Huber loss**: cuadrática cerca de 0, lineal lejos — combina lo mejor.
- **Quantile loss**: para regresión robusta a sesgos asimétricos.

#### 3.2.2 — Otras funciones de costo (preview de capítulos siguientes)

| Modelo | Función de costo | Capítulo donde aparece |
|--------|-----------------|------------------------|
| Regresión lineal | MSE | Cap 03 |
| Regresión polinomial | MSE | Cap 03 |
| Ridge regression | MSE + L2 | Cap 05 |
| Lasso | MSE + L1 | Cap 05 |
| Perceptrón | Pérdida 0/1 (no derivable) o MSE diferenciable | Cap 06 |
| Logistic regression | Cross-entropy (log-loss) | Cap 07 |
| Naive Bayes | Maximum likelihood (no hay "loss" iterativa) | Cap 08 |
| KNN | No tiene loss — es lazy | Cap 09 |

> **Idea clave:** elegir función de costo == decidir qué error te duele más. Esa elección codifica supuestos.

### 3.3 — El ciclo de optimización

**Hay dos grandes familias de algoritmos para minimizar $E(\mathbf{w})$:**

#### Familia 1 — Solución analítica cerrada (mínimos cuadrados)

Si $E$ es **cuadrática** en $\mathbf{w}$ (caso MSE + modelo lineal), $\nabla E = 0$ se resuelve algebraicamente. La cátedra deriva la **ecuación normal** en el PDF p. 27:

$$
\mathbf{w}^* = (\mathbf{Z}^T \mathbf{Z})^{-1} \mathbf{Z}^T \mathbf{y}
$$

donde $\mathbf{Z}$ es la matriz de diseño. **No requiere iteración.**

> **Frase cátedra (PDF p. 27):** *"Resultado clave: ambas soluciones son analíticas y cerradas. No requieren iteración. La regularización Ridge solo añade $\lambda \mathbf{I}$ a la matriz a invertir."*

**Costo:** $O(D^3)$ por la inversa, donde $D$ = número de features. Bien hasta $D \sim 10^4$. Para $D$ más grande, va lento.

#### Familia 2 — Métodos iterativos (gradient descent)

Cuando no hay solución cerrada (la mayoría de los modelos: logística, redes neuronales, etc.), iteramos:

$$
\mathbf{w}^{(t+1)} = \mathbf{w}^{(t)} - r \cdot \nabla E(\mathbf{w}^{(t)})
$$

donde $r$ es la **tasa de aprendizaje** (learning rate). La cátedra usa $r$, NO $\eta$ ni $\alpha$ — mantené la notación.

**Variantes:**
- **GD (batch)** — gradiente con TODOS los datos por step.
- **SGD (stochastic)** — gradiente con UN ejemplo por step.
- **Mini-batch SGD** — gradiente con un sub-lote (16, 32, 64…). El default en deep learning.

**Advertencia cátedra (PDF p. 39):** *"Si $r$ es muy grande, los pesos oscilan y el algoritmo no converge."* Demasiado chico, converge lento. Buscar el sweet spot es UNA decisión de hiperparámetro.

Optimizadores avanzados (no en cátedra pero canónicos): Adam (Kingma & Ba, 2015), L-BFGS (usado por sklearn `LogisticRegression` por default — notebook 03 celda 35), Newton-Raphson, RMSProp.

### 3.4 — Hiperparámetros: lo que NO se aprende con gradiente

**Parámetros** = lo que el optimizador ajusta (los $\mathbf{w}$).
**Hiperparámetros** = lo que VOS elegís ANTES de optimizar.

Ejemplos:
- Grado del polinomio $M$ (PDF p. 20).
- Coeficiente de regularización $\lambda$ (PDF p. 24).
- Learning rate $r$ (PDF p. 39).
- k en KNN.
- Número de capas / unidades en una red.

**¿Cómo se eligen?** Con el **validation set** (no con train, no con test):

```
Para cada combinación de hiperparámetros:
    Entrenar con train → obtener w*
    Evaluar con val → guardar val_error
Elegir la combinación con mínimo val_error
Evaluar UNA VEZ en test
```

Esto se llama **model selection**. Si el espacio de hiperparámetros es chico, hacés grid search. Si es grande, random search (Bergstra & Bengio, 2012) o Bayesian optimization.

### 3.5 — La curva de pérdida: el monitor universal

**Definición:** graficar el error en train y el error en val (en el eje y) contra una variable de complejidad o tiempo (en el eje x). Eje x posibles:
- Número de iteraciones (epochs).
- Cantidad de datos de train (learning curve).
- Complejidad del modelo (grado $M$, profundidad, número de capas).

**Diagnóstico canónico (PDF Clase 1, p. 21):**

```
Error
  ▲
  │       _____ validation
  │     ╱     ╲___
  │    ╱          ╲___
  │   ╱
  │  ╱   training (siempre baja)
  │ ╱   _____________
  │╱  ╱
  └────────────────────────► Complejidad (M)
       │     │
   underfit  ÓPTIMO   overfit
```

**Tres regiones:**
- **Underfitting (zona izquierda):** ambos errores ALTOS. Modelo demasiado simple para capturar la estructura. Solución: aumentar capacidad (más M, más features, modelo más rico).
- **Óptimo (zona media):** train bajo, val bajo y cercano. Sweet spot.
- **Overfitting (zona derecha):** train MUY bajo (casi 0), val ALTO y subiendo. Modelo memorizó ruido. Solución: regularización, más datos, modelo más simple.

**Datos numéricos concretos cátedra (PDF p. 20, sinusoidal con N=20):**

| M | Caso | Train RMSE | Val RMSE |
|---|------|-----------|----------|
| 0 | Underfitting total | 0.762 | 0.568 |
| 1 | Underfitting | 0.533 | 0.433 |
| 3 | Buen ajuste | 0.216 | 0.263 |
| 9 | Overfitting | 0.131 | **0.282** |

Notá: train SIEMPRE baja con M. Val baja, llega a un mínimo, y sube. El mínimo del val define el M óptimo.

**Efecto del tamaño N (PDF p. 22):** con N=20 y M=9 → val_RMSE = 5.856 (catástrofe). Con N=100 y M=9 → val_RMSE = 0.189 (perfecto). **Más datos rescatan modelos complejos.** Es la lección de oro de la era deep learning.

### 3.6 — Métricas iniciales

Distinguir:
- **Función de costo (loss)** = lo que el OPTIMIZADOR minimiza.
- **Métrica** = lo que el HUMANO interpreta para evaluar.

A veces coinciden (MSE como loss y como métrica de regresión). A veces no (cross-entropy como loss, accuracy como métrica de clasificación — la accuracy no es diferenciable).

**Métricas de regresión:**

| Métrica | Fórmula | Cuándo usar |
|---------|---------|-------------|
| **MSE** | $\frac{1}{N}\sum (\hat y - y)^2$ | Default. Penaliza outliers. |
| **RMSE** | $\sqrt{\text{MSE}}$ | Mismas unidades que $y$, interpretable |
| **MAE** | $\frac{1}{N}\sum \Vert \hat y - y\Vert $ | Robusta a outliers |
| **R²** | $1 - \frac{\sum(y - \hat y)^2}{\sum(y - \bar y)^2}$ | Proporción de varianza explicada (0 = peor, 1 = perfecto) |
| **MAPE** | $\frac{1}{N}\sum \frac{\Vert \hat y - y\Vert }{\Vert y\Vert }$ | Error relativo en %, útil en negocio |

**Métricas de clasificación (preview Clase 2):**

| Métrica | Fórmula | Cuándo usar |
|---------|---------|-------------|
| **Accuracy** | $\frac{\text{correctos}}{\text{total}}$ | Default. **Engaña con clases desbalanceadas.** |
| **Precision** | $\frac{TP}{TP+FP}$ | Cuando los FP cuestan (spam que NO era spam) |
| **Recall** | $\frac{TP}{TP+FN}$ | Cuando los FN cuestan (cáncer no detectado) |
| **F1** | $2\frac{P \cdot R}{P+R}$ | Compromiso P/R |
| **AUC-ROC** | Área bajo curva TPR vs FPR | Comparar clasificadores agnóstico al umbral |
| **Matriz de confusión** | Conteos por celda | Diagnóstico completo |

> La cátedra (Clase 1 + Clase 2 hasta el material visto) usa **sólo accuracy + matriz de confusión** para clasificación, y MSE/RMSE para regresión. No introduce F1, AUC, etc.

## 4. Ejemplo numérico

Reproducimos la **tabla numérica de la cátedra (PDF p. 20)** sobre el dataset sinusoidal sintético, ejecutado fielmente al notebook 01:

```python
import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

def create_sinusoidal_data(spread=0.10, data_size=20, seed=0):
    np.random.seed(seed)
    x = np.linspace(0, 1, data_size)
    y = np.sin(2*np.pi*x) + np.random.normal(scale=spread, size=x.shape)
    return x.reshape(-1, 1), y

X_train, y_train = create_sinusoidal_data(0.10, data_size=20)
X_val,   y_val   = create_sinusoidal_data(0.10, data_size=20, seed=1)  # val "independiente"

for M in [0, 1, 3, 9]:
    if M == 0:
        # caso especial: modelo constante (el "promedio" del cap 00)
        a = y_train.mean()
        train_rmse = np.sqrt(((y_train - a)**2).mean())
        val_rmse   = np.sqrt(((y_val   - a)**2).mean())
    else:
        model = make_pipeline(
            PolynomialFeatures(M),
            LinearRegression(fit_intercept=False)
        )
        model.fit(X_train, y_train)
        train_rmse = np.sqrt(mean_squared_error(y_train, model.predict(X_train)))
        val_rmse   = np.sqrt(mean_squared_error(y_val,   model.predict(X_val)))
    print(f"M={M}  train_RMSE={train_rmse:.3f}  val_RMSE={val_rmse:.3f}")
```

**Resultado esperado (cualitativamente, idéntico al patrón cátedra PDF p. 20):**

| M | train_RMSE | val_RMSE | Diagnóstico |
|---|-----------|----------|-------------|
| 0 | ~0.76 | ~0.57 | Underfitting total |
| 1 | ~0.53 | ~0.43 | Underfitting |
| 3 | ~0.22 | ~0.26 | Buen ajuste |
| 9 | ~0.13 | ~0.28 | Overfitting (val empezó a subir) |

> **Lección:** el train baja monotónicamente. El val muestra forma de U. El **mínimo del val** define el M óptimo (acá M=3).

## 5. Conexión con el TP

**TP1 — Ej. 3 (cell-19):** *"Evaluar con error cuadrático medio en train y test."*

Este es el ciclo COMPLETO del pipeline en acción:
1. Split → ya viene resuelto (cell-9, `random_state=0`).
2. Modelo → `LinearRegression()`.
3. Función de costo → MSE (la cátedra escribe explícitamente *mean squared error*).
4. Métricas → `mean_squared_error(y_train, y_pred)` y `mean_squared_error(y_test, y_pred)`.
5. Diagnóstico → comparar train vs test para detectar overfitting/underfitting.

**Pseudo-código del Ej. 3:**

```python
model = LinearRegression()
model.fit(X_train_sel, y_train)
mse_train = mean_squared_error(y_train, model.predict(X_train_sel))
mse_test  = mean_squared_error(y_test,  model.predict(X_test_sel))
print(f"MSE train = {mse_train:.3f}")
print(f"MSE test  = {mse_test:.3f}")
```

**TP1 — Ej. 4 (cell-26):** *"Para varios grados de polinomio... Graficar curvas de error vs grado del polinomio. Identificar dónde empieza el sobreajuste."*

Esto es LITERALMENTE replicar la slide 21 del PDF con un dataset real. La estructura:

```python
grados = range(1, 11)
mse_train_list, mse_test_list = [], []
for d in grados:
    model = make_pipeline(PolynomialFeatures(d), LinearRegression(fit_intercept=False))
    model.fit(X_train_sel, y_train)
    mse_train_list.append(mean_squared_error(y_train, model.predict(X_train_sel)))
    mse_test_list.append(mean_squared_error(y_test,   model.predict(X_test_sel)))

# Ahora graficar grados vs mse_*_list → debería ver el "codo" del overfitting
```

> **Tip Ej. 4:** el enunciado dice "errores menores a 40 e incluso a 35" pero NO aclara qué grados probar. Probar 1 a 10 es razonable; con más, los polinomios numéricamente explotan en datos sin escalar.

**TP1 — NO TOCA:** validación cruzada (k-fold), métricas distintas a MSE (no pide R², MAE), regularización con Ridge (eso es opcional, Ej. 7). El pipeline del TP1 es el básico que acabamos de describir.

## 6. Errores comunes

1. **"Optimizar bien train" como objetivo** — error conceptual de raíz. El train sirve para AJUSTAR, no para EVALUAR. Goodfellow §5.3 lo machaca: lo que importa es el error de generalización.
2. **Usar test como val** — si decidís hiperparámetros con test, perdés la honestidad de la evaluación. Sólo usar test UNA VEZ.
3. **Confundir loss con métrica** — la cross-entropy minimiza, la accuracy reporta. No siempre coinciden, no siempre tienen que coincidir.
4. **Train RMSE bajando ≠ "el modelo mejora"** — el train siempre baja con más capacidad. El indicador real es VAL.
5. **Curva de val plana** — síntoma frecuente de que el espacio de hipótesis es demasiado pobre (underfit) o demasiado regularizado. No hay sweet spot porque no hay sensibilidad.
6. **No estratificar split en clasificación desbalanceada** — `train_test_split(..., stratify=y)` mantiene la proporción de clases en cada partición. Crítico cuando una clase es rara.
7. **"Más M = mejor"** — error didáctico que la cátedra ataca explícitamente con la tabla de PDF p. 20.
8. **Olvidar `random_state`** — corridas no reproducibles. Tus números no van a coincidir con los del enunciado.
9. **Reportar SÓLO accuracy en clases desbalanceadas** — si 95% son negativos, un clasificador trivial "siempre 0" tiene 95% accuracy. Engaña. Cap 07 lo desarrolla.
10. **Aplicar `StandardScaler.fit_transform` sobre todo el dataset** — leakage. Fit con train, transform con todo. Pipelines lo hacen automático.
11. **Confundir "sin solución analítica" con "sin solución"** — gradiente descendente CONVERGE en problemas convexos (Bishop §3, Goodfellow §4.3). Que no haya forma cerrada no significa que no haya respuesta.
12. **Pensar el learning rate como detalle** — un $r$ mal elegido es la diferencia entre converger en 50 epochs y oscilar para siempre (PDF p. 39).

## 7. Checklist de comprensión

- [ ] Sé explicar para qué sirve cada uno de los 3 conjuntos (train, val, test) y por qué son necesarios.
- [ ] Puedo escribir el MSE con y sin el factor 1/2 y sé por qué la cátedra lo usa.
- [ ] Distinguo entre parámetros e hiperparámetros y sé con qué conjunto se eligen.
- [ ] Sé reconocer una curva de overfitting y una de underfitting mirando train vs val.
- [ ] Conozco la diferencia entre solución cerrada (ecuación normal) e iterativa (gradient descent).
- [ ] Sé cuál es el riesgo de un learning rate $r$ demasiado alto o demasiado bajo.
- [ ] Conozco la diferencia entre loss y métrica.
- [ ] Sé que accuracy puede engañar con clases desbalanceadas.
- [ ] Puedo escribir RMSE y R² y saber cuándo elegir uno u otro.
- [ ] Sé describir el ciclo de optimización en 4 pasos.
- [ ] Sé que aumentar N puede rescatar a un modelo de alto M (PDF p. 22).
- [ ] Puedo reproducir el experimento de la slide 20 sobre el dataset sinusoidal.

## 8. Para profundizar

- **Goodfellow, Bengio & Courville §5 (2016).** El mejor capítulo único sobre fundamentos de ML. §5.2 (capacity, overfitting), §5.3 (validation), §5.4 (estimators, bias, variance), §5.5 (MLE). Lectura obligatoria. <https://www.deeplearningbook.org/contents/ml.html>
- **Hastie, Tibshirani & Friedman §7 (ESL, 2009).** Cap "Model Assessment and Selection" — el tratamiento estadístico riguroso del bias-variance tradeoff, k-fold CV, AIC/BIC. Más técnico que Goodfellow.
- **Bishop §1.1–1.4 (PRML, 2006).** El ejemplo de regresión polinomial como hilo conductor. La derivación clásica del bias-variance decomposition está en §3.2.
- **Murphy §4.5 (PML, 2022).** Empirical risk minimization. Más probabilístico.
- **Bergstra & Bengio (2012). "Random Search for Hyper-Parameter Optimization".** El paper que sustituyó grid search por random search en la práctica.
- **scikit-learn user guide — Cross-validation:** <https://scikit-learn.org/stable/modules/cross_validation.html> — implementación práctica de k-fold, leave-one-out, time series split.
- **scikit-learn — Common pitfalls:** <https://scikit-learn.org/stable/common_pitfalls.html> — exactamente los errores comunes de §6 acá, explicados con código.

## Próximo paso

→ [03-regresion-lineal.md](03-regresion-lineal.md)

## Referencias

- Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*. Springer. §1.1, §3.
- Goodfellow, I., Bengio, Y., & Courville, A. (2016). *Deep Learning*. MIT Press. Cap 5. <https://www.deeplearningbook.org/contents/ml.html>
- Hastie, T., Tibshirani, R., & Friedman, J. (2009). *The Elements of Statistical Learning* (2nd ed.). Springer. Cap 7. <https://hastie.su.domains/ElemStatLearn/>
- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press. §1, §4.
- Bergstra, J. & Bengio, Y. (2012). Random Search for Hyper-Parameter Optimization. *Journal of Machine Learning Research* 13.
- Kingma, D. P. & Ba, J. (2015). Adam: A Method for Stochastic Optimization. *ICLR*.
- scikit-learn — Cross-validation: <https://scikit-learn.org/stable/modules/cross_validation.html>
- scikit-learn — `train_test_split`: <https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html>
- Material de cátedra: Clase 1 PDF (p. 14, p. 19–22), notebook 01 (DiploDatos UNC 2026 — IAA).
