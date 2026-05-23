# 12 — Formulario

> Fórmulas clave del módulo **IAA** (Clases 1 y 2 + TP1). Cada fórmula incluye: **expresión en LaTeX**, **variables explicadas**, **cuándo usarla** y **trampa común**. Organizado en bloques temáticos siguiendo el orden del curso.
>
> **Convención de notación de la cátedra:** `N` = tamaño del dataset, `M` = grado del polinomio, `t_i` (PDF) o `y_i` (notebooks) = target, `w` = pesos, `w_0` = bias, `r` = tasa de aprendizaje, `λ` = parámetro Ridge, `θ` = pesos en notación logística (estilo Andrew Ng), `m` = tamaño del training set (notación logística), `|V|` = vocabulario, `α` = parámetro de suavizado de Lidstone.

---

## Bloque 1 — Regresión y mínimos cuadrados

### F1.1 — Modelo lineal univariado

$$
y = w_0 + w_1 x
$$

- **Variables:** `w_0` bias / intercepto, `w_1` pendiente, `x` feature, `y` predicción.
- **Cuándo usarla:** punto de partida didáctico (PDF p. 16), línea de referencia para todo lo demás.
- **Trampa común:** olvidar `w_0` y forzar la recta a pasar por el origen. En código, eso requiere **agregar una columna de 1's** al input (notebook 01 celda 36) o `fit_intercept=True` en sklearn.

### F1.2 — Modelo polinomial de grado M

$$
y(x, \mathbf{w}) = w_0 + w_1 x + w_2 x^2 + \dots + w_M x^M = \sum_{j=0}^{M} w_j x^j
$$

- **Variables:** `M` grado del polinomio (hiperparámetro), `w = (w_0, ..., w_M)` vector de coeficientes.
- **Cuándo usarla:** cuando la relación `x → y` es **no lineal pero suave** (curvas). Cátedra PDF p. 19.
- **Trampa común:** elegir `M` "alto por las dudas" → **overfitting** garantizado. La cátedra muestra `M=9, N=20` con val RMSE **5.856** (catastrófico).

### F1.3 — MSE / Error cuadrático medio (con factor 1/2 de la cátedra)

$$
E(\mathbf{w}) = \frac{1}{2}\sum_{n=1}^{N}\bigl(y(x_n, \mathbf{w}) - t_n\bigr)^2
$$

- **Variables:** `t_n` target real, `y(x_n, w)` predicción del modelo, `N` cantidad de datos.
- **Cuándo usarla:** función de costo estándar para regresión. El factor `1/2` simplifica la derivada (se cancela con el `2` que baja al derivar).
- **Trampa común:** sklearn `mean_squared_error` usa `1/N` (no `1/(2N)`). Si compará a mano con sklearn, vas a obtener **el doble** del MSE de la cátedra. Ambas notaciones son válidas; lo importante es la **monotonía** (qué `w` minimiza), no el valor absoluto.

### F1.4 — RMSE

$$
E_{\text{RMS}} = \sqrt{\frac{2 E(\mathbf{w}^*)}{N}}
$$

- **Variables:** `E(w*)` MSE evaluado en el `w` óptimo.
- **Cuándo usarla:** para reportar el error en **las mismas unidades del target** (más interpretable que MSE en sí).
- **Trampa común:** RMSE de val ≠ RMSE de train. La separación entre ambos es el síntoma clave de overfitting (PDF p. 21).

### F1.5 — Vector de features expandido (regresión polinomial como lineal)

$$
\mathbf{z}_i = (1, x_i, x_i^2, \dots, x_i^M)^T \in \mathbb{R}^{M+1}
$$

- **Variables:** una fila de la matriz de diseño `Z` por cada punto `x_i`.
- **Cuándo usarla:** para **reducir polinomial a lineal** en `w`. Permite usar la misma maquinaria (`np.linalg.pinv`).
- **Trampa común:** olvidar el `1` inicial → no se ajusta `w_0` correctamente.

### F1.6 — Función de costo en forma matricial

$$
E(\mathbf{w}) = \frac{1}{2}\|\mathbf{Z}\mathbf{w} - \mathbf{y}\|^2
$$

- **Variables:** `Z ∈ ℝ^(N × (M+1))` matriz de diseño, `y ∈ ℝ^N` vector de targets.
- **Cuándo usarla:** versión vectorizada — es la que se implementa en NumPy.
- **Trampa común:** la cátedra alterna `Z` y `Φ` para la matriz de diseño en la misma slide (PDF p. 27). Adoptá una sola en tus apuntes y aclarálo.

### F1.7 — Ecuación normal (solución analítica cerrada)

$$
\boxed{\mathbf{w}^* = (\mathbf{Z}^T \mathbf{Z})^{-1} \mathbf{Z}^T \mathbf{y}}
$$

- **Variables:** `w*` solución óptima sin regularización.
- **Cuándo usarla:** dataset chico/mediano, `Z^T Z` bien condicionada. **No requiere iteración** — un solo cálculo.
- **Trampa común:** `(Z^T Z)` puede ser **singular** o **muy mal condicionada** (sobre todo con muchas features muy correlacionadas). Solución cátedra: usar `np.linalg.pinv` en lugar de `inv` (notebook 01 celda 31).

### F1.8 — Ecuación normal regularizada (Ridge)

$$
\boxed{\mathbf{w}^* = (\mathbf{Z}^T \mathbf{Z} + \lambda \mathbf{I})^{-1} \mathbf{Z}^T \mathbf{y}}
$$

- **Variables:** `λ > 0` parámetro Ridge, `I` matriz identidad de tamaño `(M+1) × (M+1)`.
- **Cuándo usarla:** cuando hay **overfitting** o `Z^T Z` no es invertible. `λ > 0` **garantiza que la matriz sea invertible**.
- **Trampa común:** **no penalizar el bias `w_0`**: en la versión "limpia" la identidad tiene un `0` en `I_{00}`. Muchas implementaciones ignoran este detalle por simplicidad.

### F1.9 — Función de costo regularizada (Ridge)

$$
\tilde{E}(\mathbf{w}) = E(\mathbf{w}) + \frac{\lambda}{2}\|\mathbf{w}\|^2 = \frac{1}{2}\|\mathbf{Z}\mathbf{w} - \mathbf{y}\|^2 + \frac{\lambda}{2}\|\mathbf{w}\|^2
$$

- **Variables:** mismo que F1.6 + término L2 `(λ/2)‖w‖²`.
- **Cuándo usarla:** cuando se sospecha overfitting. Mover `λ` en escala **logarítmica** (`np.logspace`) — la cátedra evalúa `ln λ ∈ {-∞, -18, 0}`.
- **Trampa común:** `λ` muy grande sub-ajusta (modelo "demasiado suave", train RMSE 0.450 vs 0.165 de la cátedra); `λ` muy chico no regulariza nada.

### F1.10 — Solución de mínimos cuadrados con bias explícito (notebook 01)

```python
def linear_least_squares(X, y):
    X_b = np.stack((np.ones(X.shape[0]), X), axis=1)  # columna de 1's
    return np.linalg.pinv(X_b.T @ X_b) @ (X_b.T @ y)
```

- **Cuándo usarla:** implementación didáctica de la ecuación normal (notebook 01 celda 30).
- **Trampa común:** usar `np.linalg.inv` en lugar de `pinv` → se rompe si los datos generan rango deficiente.

---

## Bloque 2 — Regresión logística y log-loss

### F2.1 — Función sigmoide / logística

$$
\sigma(z) = \frac{1}{1 + e^{-z}}
$$

- **Variables:** `z = θ^T x` score lineal.
- **Propiedades:** `σ(0)=0.5`, `σ(+∞)=1`, `σ(-∞)=0`, monótona creciente, derivable.
- **Cuándo usarla:** para mapear cualquier número real a una probabilidad en `(0, 1)`.
- **Trampa común:** **saturación** en los extremos: si `z` es muy grande/negativo, `σ'(z) ≈ 0` y el gradiente se anula → el modelo deja de aprender (PDF p. 5).

### F2.2 — Hipótesis del modelo logístico (notación cátedra)

$$
h_\theta(x) = g(\theta^T x) = \sigma(\theta^T x) = \frac{1}{1 + e^{-\theta^T x}}
$$

- **Variables:** `θ` parámetros, `x` features.
- **Cuándo usarla:** clasificación binaria probabilística.
- **Trampa común:** confundir score (`θ^T x`) con probabilidad (`σ(θ^T x)`). El score lineal NO suma 1 sobre las clases (PDF p. 4).

### F2.3 — Interpretación probabilística

$$
P(y=1 \mid x; \theta) = h_\theta(x), \qquad P(y=0 \mid x; \theta) = 1 - h_\theta(x)
$$

- **Cuándo usarla:** para reportar **incertidumbre**, no solo decisión binaria.
- **Trampa común:** un score de 0.51 NO es lo mismo que uno de 0.99 — la regla `≥ 0.5 → clase 1` esconde esa diferencia. Usar siempre `predict_proba` cuando el costo de los errores no es simétrico.

### F2.4 — Logit / log-odds (función inversa de la sigmoide)

$$
\text{logit}(p) = \log\frac{p}{1-p} = \theta^T x
$$

- **Cuándo usarla:** para interpretar coeficientes: un cambio de 1 unidad en `x_i` cambia el log-odds en `θ_i`.
- **Trampa común:** confundir `log-odds` (linealidad en `x`) con `odds` (multiplicativa en `x`).

### F2.5 — Forma unificada de Bernoulli

$$
P(y \mid x; \theta) = h_\theta(x)^y \cdot (1 - h_\theta(x))^{1-y}
$$

- **Cuándo usarla:** **paso intermedio obligatorio** para derivar la log-loss. Verificá: `y=1` → `h(x)`; `y=0` → `1-h(x)`.
- **Trampa común:** confundir esta forma "trucos algebraicos" con una distribución condicional real — sí lo es, pero solo porque las dos probabilidades suman 1.

### F2.6 — Verosimilitud conjunta (muestras i.i.d.)

$$
L(\theta) = \prod_{i=1}^{m} \sigma(\theta^T x^{(i)})^{y^{(i)}} \cdot (1 - \sigma(\theta^T x^{(i)}))^{1-y^{(i)}}
$$

- **Cuándo usarla:** punto de partida del MLE en logística.
- **Trampa común:** **multiplicar probabilidades chicas produce underflow** numérico. Trabajar siempre con logaritmos.

### F2.7 — Log-loss / Cross-entropy / Función de costo `J(θ)`

$$
\boxed{J(\theta) = -\frac{1}{m}\sum_{i=1}^{m}\Bigl[y^{(i)} \log h_\theta(x^{(i)}) + (1-y^{(i)})\log(1 - h_\theta(x^{(i)}))\Bigr]}
$$

- **Variables:** `m` tamaño del train set, `h_θ(x^(i))` predicción del modelo, `y^(i) ∈ {0,1}`.
- **Cuándo usarla:** función de costo estándar para clasificación binaria probabilística.
- **Propiedades clave:** **convexa** bajo la sigmoide → gradiente descendente converge al **mínimo global**.
- **Trampa común:** usar MSE en lugar de log-loss → la superficie se vuelve **no convexa** + gradiente saturado (PDF p. 5).

### F2.8 — Log-loss por casos (función llave)

$$
\text{cost}(h_\theta(x), y) = \begin{cases} -\log(h_\theta(x)) & \text{si } y=1 \\ -\log(1 - h_\theta(x)) & \text{si } y=0 \end{cases}
$$

- **Cuándo usarla:** para entender intuitivamente la penalización.
- **Trampa común:** olvidar que **un error muy seguro de un lado equivocado tiene costo infinito**: si `y=1` pero `h(x) → 0`, entonces `-log(h(x)) → ∞` (PDF p. 8).

### F2.9 — Regla de decisión

$$
\hat{y} = \begin{cases} 1 & \text{si } h_\theta(x) \geq 0.5 \\ 0 & \text{si } h_\theta(x) < 0.5 \end{cases}
$$

- **Cuándo usarla:** decisión binaria post-modelo.
- **Trampa común:** el threshold `0.5` es **convencional, no obligatorio**. En problemas desbalanceados o con costos asimétricos, hay que moverlo (no tratado en clases 1-2).

### F2.10 — Función softmax (multiclase)

$$
\boxed{P(Y = k \mid x; \Theta) = \frac{e^{\theta_k^T x}}{\sum_{j=1}^{K} e^{\theta_j^T x}}}
$$

- **Variables:** `K` número de clases, `θ_k` vector de pesos de la clase `k`, `Θ = (θ_1, ..., θ_K)`.
- **Propiedad clave:** `Σ_k P(Y=k|x) = 1`. **Es una distribución de probabilidad coherente**.
- **Cuándo usarla:** clasificación multiclase mutuamente excluyente (dígitos 0-9).
- **Trampa común:** softmax **es invariante a shift**: `softmax(z) = softmax(z + c)`. Usar este truco (`z = z - max(z)`) para evitar overflow numérico al exponenciar.

### F2.11 — Predicción multiclase

$$
\hat{y} = \arg\max_{k} P(Y=k \mid x; \Theta) = \arg\max_{k} \theta_k^T x
$$

- **Cuándo usarla:** la segunda igualdad funciona porque la exponencial es **monótona** y el denominador no depende de `k`.
- **Trampa común:** confundir `predict` (devuelve `argmax`) con `decision_function` (devuelve scores lineales) con `predict_proba` (devuelve softmax).

### F2.12 — Score lineal por clase

$$
z_k = \theta_k^T x = w_k \cdot x + b_k
$$

- **Cuándo usarla:** este es el "input" del softmax. En sklearn, `model.decision_function(x)` lo devuelve, equivalente a `model.coef_ @ x + model.intercept_` (notebook 03 celda 89-90).
- **Trampa común:** los `z_k` **no son probabilidades** hasta aplicar softmax.

---

## Bloque 3 — Perceptrón

### F3.1 — Función de scoring del perceptrón

$$
f(x) = \mathbf{w}^T \mathbf{x} + b
$$

- **Variables:** `w` pesos, `b` bias, `x` features.
- **Cuándo usarla:** medida de **confianza** del modelo antes del threshold. PDF p. 33.

### F3.2 — Función de decisión (signo)

$$
g(f(x)) = \text{sign}(f(x)) = \begin{cases} +1 & \text{si } f(x) \geq 0 \\ -1 & \text{si } f(x) < 0 \end{cases}
$$

- **Cuándo usarla:** convierte el score continuo en decisión binaria.
- **Trampa común:** la cátedra usa etiquetas `y ∈ {+1, -1}` (NO `{0, 1}`). Si cargás un dataset con `{0, 1}`, hay que **mapear** con `y_true[y_true == 0] = -1` (notebook 02).

### F3.3 — Condición de clasificación correcta

$$
y_i \cdot f(x_i) > 0
$$

- **Cuándo usarla:** un único test para saber si el ejemplo `i` está bien clasificado, sea cual sea la clase.
- **Trampa común:** olvidar que esto **solo funciona con `y ∈ {+1, -1}`**.

### F3.4 — Regla de actualización del perceptrón (Rosenblatt)

$$
\boxed{\mathbf{w}^{(t+1)} = \mathbf{w}^{(t)} + r \cdot y_i \cdot \mathbf{x}_i \quad \text{si } \hat{y}_i \neq y_i}
$$

- **Variables:** `r` tasa de aprendizaje (escalar pequeño `< 1`), `y_i ∈ {+1, -1}` etiqueta real, `x_i` ejemplo mal clasificado.
- **Cuándo usarla:** algoritmo **online** — un ejemplo a la vez, **actualiza solo si hay error**.
- **Trampa común:** si `r` es muy chico, la corrección puede no alcanzar para cambiar el `sign` (notebook 02 celda 49). Si es muy grande, oscila.

### F3.5 — Algoritmo estándar: MSE diferenciable

$$
J(\mathbf{w}) = \frac{1}{2}\sum_{i}(\mathbf{w}^T \mathbf{x}_i - y_i)^2
$$

- **Variables:** mismas que F1.3.
- **Cuándo usarla:** alternativa al perceptrón clásico, **diferenciable** → permite descenso de gradiente real (PDF p. 39).
- **Trampa común:** "el error 0/1 no es diferenciable" — por eso no se puede gradient-descend directamente sobre la pérdida discreta del perceptrón.

### F3.6 — Gradiente del MSE (perceptrón estándar)

$$
\nabla J(\mathbf{w}) = \sum_i (\mathbf{w}^T \mathbf{x}_i - y_i)\, \mathbf{x}_i
$$

- **Cuándo usarla:** para implementar gradient descent batch.
- **Trampa común:** este es el gradiente **batch** (suma sobre TODOS los `i`). Para SGD es por ejemplo.

### F3.7 — Actualización con descenso de gradiente

$$
\mathbf{w} \leftarrow \mathbf{w} - r \cdot \nabla J(\mathbf{w})
$$

- **Cuándo usarla:** algoritmo "estándar" PDF p. 39. **Actualiza siempre**, no solo ante errores.
- **Trampa común:** "Si `r` es muy grande, los pesos oscilan y el algoritmo no converge." Probar en escala logarítmica.

### F3.8 — Hiperplano perpendicular a `w`

$$
\mathbf{w}^T \mathbf{x} + b = 0 \quad \Rightarrow \quad x_2 = -\frac{w_1}{w_2} x_1 - \frac{b}{w_2}
$$

- **Cuándo usarla:** para graficar la frontera en 2D y entender la geometría (notebook 02 celda 59).
- **Trampa común:** **el vector `w` es perpendicular al hiperplano**. Si `|w_1| ≫ |w_2|`, la frontera depende casi solo de `x_1`. Sin bias (`b=0`), la recta pasa obligatoriamente por el origen — restringe brutalmente las soluciones.

---

## Bloque 4 — Naive Bayes

### F4.1 — Regla de Bayes

$$
\boxed{P(Y \mid X) = \frac{P(X \mid Y)\, P(Y)}{P(X)}}
$$

- **Variables:** `P(Y|X)` posterior, `P(X|Y)` likelihood, `P(Y)` prior, `P(X)` evidencia.
- **Cuándo usarla:** cuando `P(Y|X)` es difícil pero `P(X|Y)` se puede estimar por conteo.

### F4.2 — Supuesto naïve de independencia condicional

$$
P(x_1, x_2, \dots, x_n \mid y) = \prod_{i=1}^{n} P(x_i \mid y)
$$

- **Cuándo usarla:** el corazón de Naive Bayes. Reduce un problema **exponencial** (joint distribution) a uno **lineal** en `n` (productos de marginales).
- **Trampa común:** "las variables son independientes entre sí dado `y`" rara vez es cierto, pero **el clasificador funciona igual**. Es el "misterio" de Naive Bayes (PDF p. 18, Domingos & Pazzani 1997).

### F4.3 — Función de decisión NB

$$
\boxed{\hat{y} = \arg\max_{y}\, P(y) \prod_{i=1}^{n} P(x_i \mid y)}
$$

- **Cuándo usarla:** clasificación. El denominador `P(x_1, ..., x_n)` se **ignora** porque no depende de `y`.
- **Trampa común:** olvidar el **prior** `P(y)` y solo usar el producto de likelihoods. Si las clases están desbalanceadas, el prior cambia mucho la respuesta.

### F4.4 — Versión en log-probabilidades (estable numéricamente)

$$
\log\hat{P}(y \mid x) \propto \log P(y) + \sum_{i=1}^{n} \log P(x_i \mid y)
$$

- **Cuándo usarla:** **siempre que se manejen muchos features** (texto con vocabularios grandes). Evita underflow.
- **Trampa común:** `np.log(0) = -inf` → previo a sumar logs hay que **suavizar** (Laplace) para evitar ceros.

### F4.5 — Estimador MLE del prior

$$
P(Y = y) = \frac{\text{Count}(Y = y)}{\sum_{y'} \text{Count}(Y = y')}
$$

- **Cuándo usarla:** frecuencia relativa de la clase en el train set.
- **Trampa común:** si el dataset es muy desbalanceado, considerar un prior uniforme o muestrear.

### F4.6 — Estimador MLE del likelihood (sin suavizar)

$$
P(X_i = x_i \mid Y = y) = \frac{\text{Count}(X_i = x_i, Y = y)}{\sum_{x'}\text{Count}(X_i = x', Y = y)}
$$

- **Cuándo usarla:** solo si **tenés certeza** de que cada feature aparece al menos una vez en cada clase del train (poco realista).
- **Trampa común:** **el problema del cero**. Una palabra ausente en el train de una clase anula todo el producto (PDF p. 23).

### F4.7 — Suavizado de Laplace (add-one)

$$
\boxed{\hat{P}(x_i \mid y) = \frac{\text{count}(x_i, y) + 1}{\text{count}(y) + |V|}}
$$

- **Variables:** `|V|` tamaño del vocabulario, `count(y)` total de tokens en docs de la clase `y`.
- **Cuándo usarla:** **siempre** en NB con texto. Elimina ceros del producto.
- **Trampa común:** olvidar incluir `|V|` en el denominador → las probabilidades no suman 1.

### F4.8 — Suavizado de Lidstone (generalización)

$$
\hat{P}(x_i \mid y) = \frac{\text{count}(x_i, y) + \alpha}{\text{count}(y) + \alpha \cdot |V|}
$$

- **Variables:** `α ≥ 0` hiperparámetro. `α=0` → MLE; `α=1` → Laplace.
- **Cuándo usarla:** cuando querés controlar finamente la "fuerza" del suavizado por validación cruzada.
- **Trampa común:** `α` muy grande **uniforma** demasiado las probabilidades, perdiendo señal.

---

## Bloque 5 — KNN

### F5.1 — Distancia euclidiana

$$
d(x, z) = \sqrt{\sum_{j=1}^{p}(x_j - z_j)^2} = \|x - z\|_2
$$

- **Variables:** `x, z` dos puntos en `ℝ^p`.
- **Cuándo usarla:** métrica por defecto en KNN cuando las features están **en la misma escala**.
- **Trampa común:** si una feature está en miles y otra en decimales, **la grande domina la distancia**. → **estandarizar** antes de usar KNN.

### F5.2 — Distancia Manhattan (L1)

$$
d(x, z) = \sum_{j=1}^{p} |x_j - z_j| = \|x - z\|_1
$$

- **Cuándo usarla:** robusta a outliers, suele funcionar bien en dimensiones altas.

### F5.3 — Decisión KNN por votación de mayoría

$$
\hat{y} = \text{moda}\{ y_{(1)}, y_{(2)}, \dots, y_{(k)} \}
$$

donde `y_{(i)}` es la etiqueta del `i`-ésimo vecino más cercano a `x`.

- **Cuándo usarla:** clasificación con KNN. Para regresión sería `mean` en vez de `moda`.
- **Trampa común:** **empates con `k` par**. Solución: usar `k` impar (en binaria) o introducir ponderación por distancia.

### F5.4 — Error de clasificación

$$
\frac{1}{N}\sum_{i=1}^{N}\mathbb{1}[y_i \neq h(\mathbf{x}_i)]
$$

- **Variables:** `𝟙[·]` indicador (1 si el predicado es cierto, 0 si no).
- **Cuándo usarla:** medir la tasa de error sobre un conjunto. Es **1 − accuracy**.

---

## Bloque 6 — Métricas y evaluación

### F6.1 — Accuracy

$$
\text{accuracy} = \frac{\text{predicciones correctas}}{\text{total}} = \frac{1}{N}\sum_{i=1}^{N}\mathbb{1}[y_i = \hat{y}_i]
$$

- **Cuándo usarla:** dataset **balanceado** y errores de todas las clases con el mismo costo.
- **Trampa común:** en datasets muy desbalanceados (ej.: 99% no-fraude), accuracy=99% se logra prediciendo siempre la clase mayoritaria — métrica **engañosa**.

### F6.2 — Matriz de confusión (binaria)

$$
\text{CM} = \begin{pmatrix} TN & FP \\ FN & TP \end{pmatrix}
$$

- **Variables:** `TP` true positives, `TN` true negatives, `FP` falsos positivos, `FN` falsos negativos.
- **Cuándo usarla:** **inspección visual** del tipo de errores.
- **Trampa común:** sklearn por defecto pone `TN` arriba-izquierda; otras libs lo invierten. Mirar siempre los ejes etiquetados (Eje y = "Etiqueta correcta", eje x = "Etiqueta predicha", utils.py).

### F6.3 — Precision y Recall (referencia — NO desarrollado en clases 1-2)

$$
\text{Precision} = \frac{TP}{TP + FP}, \qquad \text{Recall} = \frac{TP}{TP + FN}
$$

- **Variables:** mismas que F6.2.
- **Cuándo usarla:** problemas desbalanceados o con costos asimétricos.
- **Nota cátedra:** estas métricas **no aparecen formalmente** en el material de Clases 1-2 — incluidas acá como referencia para TPs posteriores.

### F6.4 — F1-Score

$$
F_1 = 2 \cdot \frac{\text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}}
$$

- **Cuándo usarla:** un único número que balancea precision y recall (media armónica).

---

## Tabla resumen — Qué fórmula usar en qué contexto

| Problema | Fórmula clave | Bloque |
|---|---|---|
| Regresión lineal 1D | F1.1, F1.3, F1.7 | 1 |
| Regresión polinomial | F1.2, F1.5, F1.7 | 1 |
| Overfitting → regularizar | F1.8, F1.9 | 1 |
| Clasificación binaria probabilística | F2.1, F2.7, F2.9 | 2 |
| Multiclase con probabilidades coherentes | F2.10, F2.11 | 2 |
| Clasificación lineal sin probabilidades | F3.1, F3.2, F3.4 | 3 |
| Clasificación de texto / spam | F4.1, F4.3, F4.7 | 4 |
| Clasificación local sin entrenar | F5.1, F5.3 | 5 |
| Evaluar modelo | F6.1, F6.2 | 6 |

---

→ [13-preguntas-guia.md](13-preguntas-guia.md)
