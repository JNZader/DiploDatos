# 11 — Glosario

> Glosario temático del módulo **Introducción al Aprendizaje Automático** (DiploDatos UNC FAMAF 2026, Clases 1 y 2). Los términos están **agrupados por categoría** — no es una lista plana — siguiendo el orden conceptual del curso: del marco general a los algoritmos puntuales. Cada entrada incluye la **definición** tal como aparece en el material (PDF + notebooks) y el **capítulo del estudio** donde se desarrolla.
>
> **Convención de notación de la cátedra** (respetar siempre): `N` = tamaño del dataset, `M` = grado del polinomio, `K` = dimensión del input, `t_i` (PDF) o `y_i` (notebooks) = target, `w` = vector de pesos, `w_0` = bias, `r` = tasa de aprendizaje, `λ` = parámetro de regularización Ridge, `y ∈ {+1, -1}` para perceptrón.

---

## Grupo 1 — Marco general del Aprendizaje Automático

**Aprendizaje Automático (AA / ML).** Paradigma donde el sistema **infiere la lógica directamente de los datos**, sin reglas programadas explícitamente. La cátedra lo contrapone a "Software 1.0" (datos + reglas → código → respuesta) frente a "Software 2.0" (datos + salidas → modelo). El programador deja de codificar la lógica y pasa a **dirigir el entrenamiento**. → Cap. 00, 01.

**Espacio de hipótesis.** Conjunto (típicamente infinito) de funciones que el algoritmo puede elegir como candidatas para representar la relación entre entrada y salida. **Aprender = encontrar la función óptima dentro de ese espacio mediante optimización.** Esta idea es **universal**: cambia la escala (XGBoost vs. GPT-4) pero no el principio. → Cap. 01.

**Aprendizaje supervisado.** "Datos con salida esperada. El modelo aprende a mapear entradas a salidas conocidas." Pares `(x_i, y_i)` con `y_i` provisto por el dataset. Dos subtipos: **regresión** (target continuo) y **clasificación** (target discreto). → Cap. 01.

**Aprendizaje no supervisado.** "Datos sin salida esperada. El modelo descubre estructura interna." Ejemplo paradigmático: **clustering** (segmentación de clientes). → Cap. 01.

**Aprendizaje semi-supervisado.** Combina pocas etiquetas con muchos datos sin etiquetar. "Lo mejor de ambos mundos" en escenarios donde el etiquetado es caro. → Cap. 01.

**Aprendizaje auto-supervisado.** Supervisión **generada automáticamente** mediante "tareas de pretexto" (autorregresión como en GPT, enmascaramiento como en BERT). Base de los LLMs modernos. → Cap. 01.

**Pre-entrenamiento + fine-tuning.** Dos fases del paradigma moderno: (1) base de **cultura general del dominio** sobre datos masivos sin etiquetas; (2) **especialización crítica** sobre pocos ejemplos etiquetados. → Cap. 01.

**Aprendizaje por refuerzo.** "Un agente aprende a tomar decisiones óptimas mediante prueba, error y recompensa." Componentes: **agente, ambiente, acción, recompensa**. Ejemplo cátedra: Ta-Te-Ti. → Cap. 01.

**Generalización.** Capacidad del modelo de **rendir bien sobre datos no vistos** durante el entrenamiento. La frase rectora del notebook 01: *"No buscamos el modelo que mejor ajusta los datos de entrenamiento. Buscamos el modelo que mejor generaliza a datos nuevos."* → Cap. 02, 04.

**Función de costo / pérdida `E(w)` o `J(θ)`.** Función escalar que mide qué tan mal predice el modelo. Entrenar = **minimizar** esta función moviendo los parámetros. En el PDF se denota `E(w)` para regresión y `J(θ)` para logística. → Caps. 02, 06.

---

## Grupo 2 — Datos, splits y exploración

**Dataset.** Conjunto de pares `{(x_i, y_i)}_{i=1}^N`. La cátedra usa **N** mayúscula (no `n`) para el total. → Cap. 02.

**Sample / observación / instancia.** Una fila del dataset, un par `(x_i, y_i)`. → Cap. 02.

**Feature / atributo / variable de entrada.** Una columna del dataset. La dimensión del input se denota `K` (notebook 01 celda 36). → Cap. 02.

**Target / salida / variable objetivo `t_i` o `y_i`.** Lo que queremos predecir. **Atención a la notación dual:** el PDF formal usa `t_i` (p. 18-19); los notebooks usan `y_i`. → Cap. 02.

**Train / Validation / Test split.** División del dataset en tres subconjuntos: **train** para ajustar parámetros, **validation** para elegir hiperparámetros (grado `M`, `α`, `λ`) y **test** para evaluación final no contaminada. El diagrama PDF p. 14 menciona los tres; los notebooks usan solo train/val con `train_test_split`. → Cap. 02.

**Train/test split (holdout).** Partición simple (típicamente 80/20). En el TP1 se fija con `train_size=0.8, random_state=0` produciendo `X_train (16512, 8)` y `X_test (4128, 8)`. → TP1, cap. 15.

**Validación cruzada (cross-validation, CV) — k-fold.** *NO aparece formalmente en el material de Clases 1-2.* Se menciona como herramienta para Ridge (`RidgeCV`) en TP1 Ej. 7, pero sin desarrollo teórico. → TP1.

**EDA (Exploratory Data Analysis).** Análisis exploratorio: scatter plots univariados feature-vs-target, ranking visual de informatividad. Eje del Ej. 2 del TP1. → TP1.

**Sesgo en los datos (data bias).** Riesgos éticos del dataset: California Housing tiene historia documentada de **redlining** (sesgos por raza/ingreso). El Ej. 1 del TP1 obliga a discutirlos. → TP1.

---

## Grupo 3 — Regresión lineal y polinomial

**Regresión.** Problema supervisado donde `y` es **continua**. Forma: `y = f(x) + ε`. Ejemplo recurrente: predecir precio de vivienda. → Cap. 02.

**Regresión lineal simple.** Modelo `y = w_0 + w_1 x`. Máxima interpretabilidad, asume relación lineal. → Cap. 02.

**Regresión polinomial.** Modelo `y(x, w) = w_0 + w_1 x + w_2 x² + ... + w_M x^M = Σ w_j x^j`. Captura curvaturas. **Riesgo: overfitting con `M` alto.** → Cap. 02.

**Hiperparámetro.** Parámetro que **no se aprende** sino que se elige antes (ej. `M`, `λ`, `k` en KNN, `α` en Laplace, `r` en perceptrón). Distinto de los parámetros `w` que sí se ajustan. → Cap. 02, 04.

**MSE (Mean Squared Error).** Función de costo cuadrática: `E(w) = (1/2) Σ (y(x_n, w) - t_n)²`. El factor `1/2` de la cátedra simplifica la derivada. → Caps. 02, 03.

**RMSE (Root Mean Squared Error).** `E_RMS = sqrt(2 E(w*) / N)`. Misma unidad que el target, más interpretable. → Cap. 02.

**Ecuación normal.** Solución analítica cerrada de mínimos cuadrados: `w* = (Z^T Z)^(-1) Z^T y`. **No requiere iteración.** → Cap. 03.

**Matriz de diseño `Z` o `Φ`.** Matriz `N × (M+1)` cuyas filas son los vectores expandidos `z_i = (1, x_i, x_i², ..., x_i^M)`. El PDF p. 27 alterna ambas notaciones. → Cap. 03.

**Pseudoinversa `np.linalg.pinv`.** Generalización de la inversa para matrices no cuadradas o mal condicionadas. La cátedra **recomienda usar `pinv` en lugar de `inv`** "para mayor estabilidad numérica" (notebook 01 celda 31). → Cap. 02.

**Bias / intercepto `w_0`.** Término constante del modelo. Para que la recta no esté obligada a pasar por el origen hay que **agregar una columna de 1's** al input (notebook 01 celda 36). En `LinearRegression(fit_intercept=False)` debe desactivarse cuando `PolynomialFeatures` ya lo incluye. → Cap. 02.

---

## Grupo 4 — Sobreajuste, capacidad y regularización

**Underfitting.** "Modelo demasiado simple": no captura la tendencia. Síntoma: error de entrenamiento alto. Caso `M=0` y `M=1` sobre la sinusoidal del PDF (RMSE train ≈ 0.76 y 0.53). → Cap. 04.

**Overfitting / Sobreajuste.** "El modelo memoriza en lugar de aprender." Ocurre cuando "ajusta demasiado bien a los datos de entrenamiento y no generaliza bien en los nuevos". Síntomas: (1) **train error → 0** mientras **val error explota**, (2) **coeficientes enormes** (con `M=9` la cátedra mide `w_3 ≈ -6349, w_9 ≈ 9276`). → Cap. 04.

**Capacidad del modelo.** Riqueza del espacio de hipótesis. En polinomial, el grado `M` la controla. Demasiada capacidad + pocos datos = sobreajuste. → Cap. 04.

**Bias-variance tradeoff.** Compromiso entre **sesgo** (error sistemático por modelo demasiado simple) y **varianza** (sensibilidad excesiva a la muestra). Curva en U del error de validación. Aparece implícito en la curva train↓ vs val∪ del PDF p. 21. → Cap. 04.

**Relación N vs M.** Aumentar `N` puede **rescatar** un modelo de alto `M`. Tabla cátedra: con `M=9, N=20` el RMSE val explota a **5.856**; con `M=9, N=100` cae a **0.189**. → Cap. 04.

**Regularización.** Técnica que **penaliza los pesos grandes** añadiendo un término a la función de costo. Actúa como "fuerza que evita que el modelo se vuelva demasiado extremo" (notebook 03 celda 36). → Cap. 04.

**Ridge (L2).** Regularización con norma cuadrática: `Ẽ(w) = E(w) + (λ/2) ‖w‖²`. Reduce coeficientes grandes sin volverlos exactamente cero. Solución cerrada: `w* = (Z^T Z + λI)^(-1) Z^T y`. → Caps. 04, 07.

**Lasso (L1).** Regularización con norma absoluta: `J(θ) + (λ/n) Σ |θ_j|`. **Algunos coeficientes se vuelven exactamente cero** → selección automática de variables. Mencionada en sklearn (`penalty='l1'`), no desarrollada teóricamente. → Cap. 07.

**ElasticNet.** Combinación L1 + L2. Disponible como `penalty='elasticnet'` en `LogisticRegression`. → Cap. 07.

**Parámetro `λ` (Ridge) / `α` (Lasso) / `C` (sklearn).** Controlan la intensidad de la regularización. En sklearn `LogisticRegression`, **`C ∝ 1/λ`**: `C` grande = poca penalización; `C` chico = mucha. → Caps. 04, 07.

---

## Grupo 5 — Clasificación lineal y perceptrón

**Clasificación.** Problema supervisado donde `y` es **discreta** (categórica). Binaria: `y ∈ {0, 1}` o `y ∈ {+1, -1}`. La cátedra usa `{+1, -1}` para perceptrón y `{0, 1}` para logística — **respetar la convención según el algoritmo**. → Cap. 05.

**Hiperplano de decisión.** Conjunto `{x : w^T x + b = 0}`. En 2D es una recta; en 3D, un plano. **El vector `w` es perpendicular al hiperplano** (notebook 02 celda 59). → Cap. 05.

**Frontera de decisión.** Región del espacio donde la predicción `h(x)` cambia de clase. Puede ser lineal (perceptrón, logística) o no lineal (KNN, redes profundas). → Caps. 05, 09.

**Separabilidad lineal.** Existe un hiperplano que separa **perfectamente** las clases. **Condición necesaria para que el perceptrón converja.** Si los datos no son linealmente separables, el perceptrón **no converge nunca**. → Cap. 05.

**Score / función discriminante `f(x) = w^T x + b`.** Combinación lineal de features. Antes del threshold es la **medida de confianza** del modelo: "qué tan lejos está el punto del límite de decisión" (PDF p. 33). → Cap. 05.

**Threshold / función de decisión / activación.** Convierte el score continuo en una etiqueta discreta. En perceptrón: `g(f(x)) = sign(f(x))`. → Cap. 05.

**Perceptrón (Rosenblatt 1958).** "El átomo de las redes neuronales profundas modernas." Algoritmo **online**: procesa un ejemplo a la vez y **actualiza solo ante errores**. Regla: `w ← w + r · y_i · x_i`. → Cap. 05.

**Teorema de convergencia del perceptrón.** "Si los datos son linealmente separables, el perceptrón garantiza encontrar el hiperplano de separación en un **número finito de iteraciones**." → Cap. 05.

**Tasa de aprendizaje `r`.** Hiperparámetro escalar pequeño (`r < 1`) que controla el tamaño del paso de actualización. "Si `r` es muy grande, los pesos oscilan y el algoritmo no converge" (PDF p. 39). La cátedra usa `r` (NO `η` ni `α`). → Cap. 05.

**Algoritmo estándar con descenso de gradiente.** Variante del perceptrón que minimiza una función **diferenciable** (MSE) en lugar del error 0/1. Actualiza **siempre**, no solo ante errores. → Cap. 05.

**Pocket algorithm.** Variante para datos NO linealmente separables: guarda los mejores pesos encontrados. Mencionado como ejercicio (notebook 02). → Cap. 05.

---

## Grupo 6 — Marco probabilístico y MLE

**Variable aleatoria.** Función que asigna un número a cada resultado posible de un experimento. En clasificación binaria, `Y ∈ {0,1}` es una **Bernoulli**. → Cap. 06.

**Distribución de Bernoulli.** Modelo de **dos resultados posibles**: 1 con probabilidad `p`, 0 con probabilidad `1-p`. "Como tirar una moneda, pero donde la probabilidad depende de `x`" (PDF p. 6). → Cap. 06.

**Verosimilitud (likelihood) `P(X | Y)`.** Probabilidad de observar los datos dado el modelo. En NB: `P(palabra | clase)`. → Caps. 06, 08.

**Prior `P(Y)`.** Probabilidad **a priori** de cada clase, antes de ver `x`. En NB: frecuencia relativa de la clase en el train set. → Cap. 08.

**Posterior `P(Y | X)`.** Probabilidad **a posteriori** de la clase dado los datos. Es lo que queremos calcular para clasificar. → Cap. 08.

**Evidencia `P(X)`.** Probabilidad marginal de los datos. **No depende de `y`**, así que se **ignora en el `argmax`** de NB. → Cap. 08.

**Regla de Bayes.** `P(Y|X) = P(X|Y) · P(Y) / P(X)`. "Permite invertir el condicional: cuando `P(Y|X)` es difícil, se calcula a través de `P(X|Y)`" (PDF p. 14). → Caps. 06, 08.

**Máxima verosimilitud (MLE).** Estima parámetros maximizando `L(θ)`. Para Bernoulli i.i.d.: `θ̂ = (1/N) Σ y_i`. En NB equivale a **frecuencias relativas** del train set. → Caps. 06, 08.

**Log-verosimilitud.** `log L(θ) = Σ log P(x_i | θ)`. Convertir productos en sumas evita **underflow numérico** y simplifica derivadas. → Caps. 06, 08.

**Cross-entropy / entropía cruzada / log-loss.** Función de costo de clasificación probabilística: `J(θ) = -(1/m) Σ [y log p + (1-y) log(1-p)]`. **Convexa** bajo la sigmoide → gradiente descendente converge al mínimo global. → Cap. 06.

**i.i.d. (independent and identically distributed).** Supuesto de que las muestras de train y test provienen **independientemente de la misma distribución**. Base teórica del análisis de generalización (PDF p. 32). → Cap. 06.

**Modelo discriminativo vs generativo.** Discriminativo (regresión logística): modela `P(y|x)` directamente. Generativo (Naive Bayes): modela `P(x|y)` y aplica Bayes. "Dos caminos distintos para llegar a probabilidades" (notebook 04). → Caps. 07, 08.

---

## Grupo 7 — Regresión logística y softmax

**Regresión logística.** Clasificador probabilístico lineal. Modelo: `h_θ(x) = σ(θ^T x)`. Estima `P(y=1 | x)`. → Cap. 07.

**Función sigmoide / logística.** `σ(z) = 1 / (1 + e^(-z))`. Mapea ℝ → (0, 1). `σ(0) = 0.5`, `σ(+∞) = 1`, `σ(-∞) = 0`. → Cap. 07.

**Logit / log-odds.** Inverso de la sigmoide: `logit(p) = log(p / (1-p)) = θ^T x`. La regresión logística asume que el **log-odds es lineal en `x`**. → Cap. 07.

**Decisión brusca vs decisión suave.** "El perceptrón decide de forma brusca; la regresión logística decide de forma suave y probabilística" (notebook 03 celda 1). → Cap. 07.

**Por qué NO MSE en logística.** Dos razones cátedra (PDF p. 5): (1) **no convexidad** → mínimos locales; (2) **saturación del gradiente** en los extremos de la sigmoide → el modelo deja de aprender. → Cap. 07.

**L-BFGS.** Optimizador cuasi-Newton de memoria limitada usado por defecto en `LogisticRegression` de sklearn. → Cap. 07.

**Softmax.** Generalización multiclase de la sigmoide: `P(Y=k|x) = e^(θ_k^T x) / Σ_j e^(θ_j^T x)`. Garantiza `Σ_k P(Y=k|x) = 1`. **"La sigmoide es el caso especial binario de softmax"** (notebook 03 celda 58). → Cap. 07.

**Decision function (sklearn).** `model.decision_function(x) = w_k · x + b_k`. Score lineal **antes** del softmax. → Cap. 07.

**`predict_proba` (sklearn).** Devuelve las probabilidades softmax: vector de longitud `K` que suma 1. → Cap. 07.

---

## Grupo 8 — Naive Bayes

**Naive Bayes (NB).** Clasificador generativo basado en Bayes + supuesto naïve de **independencia condicional**: `P(x_1, ..., x_n | y) = Π P(x_i | y)`. → Cap. 08.

**Supuesto naïve.** "Las variables son independientes entre sí, dado `y`." Rara vez es cierto (altura y peso correlacionan, píxeles vecinos también), pero **el clasificador funciona sorprendentemente bien igual** (Domingos & Pazzani 1997). → Cap. 08.

**Función de decisión NB.** `ŷ = argmax_y P(y) · Π_i P(x_i | y)`. El denominador `P(x)` se ignora porque no depende de `y`. → Cap. 08.

**Estimación por conteo (MLE).** `P(Y=y) = Count(Y=y) / N`. `P(X_i=x | Y=y) = Count(X_i=x, Y=y) / Count(Y=y)`. → Cap. 08.

**Suavizado de Laplace (add-one).** Reemplaza la fórmula MLE por: `P̂(x_i | y) = (Count + 1) / (Count(y) + |V|)`. **Elimina los ceros** que arruinarían el producto. → Cap. 08.

**Suavizado de Lidstone.** Generalización: `(Count + α) / (Count(y) + α · |V|)`. `α=0` recupera MLE; `α=1` recupera Laplace. → Cap. 08.

**El "problema del cero".** Si una palabra nunca aparece en una clase durante el train, `P(palabra | clase) = 0` y **un único cero anula todo el producto**, sin importar las demás evidencias. → Cap. 08.

**Vocabulario `V`.** Conjunto de todas las palabras (features) del corpus. `|V|` = tamaño del vocabulario, aparece en el denominador del suavizado. → Cap. 08.

**Bag of Words (BoW).** Representación de texto donde cada documento es un vector con la **frecuencia de cada palabra del vocabulario**. **Se pierde el orden** de las palabras. Vectores típicamente dispersos. → Cap. 08.

**CountVectorizer (sklearn).** Convierte un corpus de strings en una matriz BoW dispersa. `.fit()` aprende el vocabulario; `.transform()` produce la matriz. Palabras fuera de vocabulario quedan como ceros. → Cap. 08.

**MultinomialNB.** Variante de NB para features de **conteo discreto** (texto típicamente). Asume `P(x|y)` multinomial. → Cap. 08.

**GaussianNB.** Variante para features **continuos**: `P(x_i|y)` modelado como gaussiana. → Cap. 08.

**BernoulliNB.** Variante para features **binarios** (`{0,1}`). Modelo natural para dígitos manuscritos binarizados (PDF p. 18). → Cap. 08.

**Log-probabilidades.** En NB se suelen usar `log P` en lugar de `P` para evitar **underflow**: multiplicar probabilidades chicas se vuelve sumar logaritmos. → Cap. 08.

---

## Grupo 9 — KNN y modelos no paramétricos

**Modelo paramétrico.** Tiene un **número fijo de parámetros** independiente del tamaño del dataset (regresión, logística, NB con parámetros tabulados). → Cap. 09.

**Modelo no paramétrico.** El "tamaño del modelo" crece con `N`: **KNN almacena todos los ejemplos del train**. No hay "entrenamiento" en el sentido clásico. → Cap. 09.

**K-Nearest Neighbors (KNN).** Algoritmo de clasificación por **similitud local**: dado un nuevo `x`, buscar los `k` vecinos más cercanos en train y votar por mayoría. → Cap. 09.

**`k` (hiperparámetro de KNN).** Número de vecinos a considerar. `k=1` overfitting (memoriza); `k` grande suaviza la frontera. **Distinto de la `K` mayúscula** que en el material denota el número de clases en multiclase. → Cap. 09.

**Métrica de distancia.** Función que mide qué tan "lejos" están dos puntos. Opciones: **euclidiana** (`||x - z||_2`), **Manhattan** (`||x - z||_1`), **coseno**. La elección impacta fuertemente el resultado. → Cap. 09.

**Diagrama de Voronoi.** Partición del espacio en regiones donde cada región corresponde al "más cercano" entre los puntos de train. Visualiza la frontera de KNN como un mosaico. → Cap. 09.

**Curse of dimensionality (maldición de la dimensionalidad).** Fenómeno por el cual en dimensiones altas **todos los puntos se vuelven equidistantes**, degradando la noción de "vecino cercano". Mencionado implícitamente al hablar de costo `O(m·n)` y de mitigaciones. → Cap. 09.

**KD-tree / Ball tree.** Estructuras de datos que aceleran la búsqueda de vecinos en `O(log m)` en dimensiones bajas. → Cap. 09.

**ANN (Approximate Nearest Neighbors).** Búsqueda aproximada para datasets muy grandes (FAISS, Annoy, HNSW). Mencionado como mitigación al costo `O(m·n)`. → Cap. 09.

---

## Grupo 10 — Clasificación multiclase y evaluación

**Clasificación binaria.** `y ∈ {0, 1}` o `{+1, -1}`. → Cap. 05, 07.

**Clasificación multiclase (mutuamente excluyente).** `y ∈ {0, 1, ..., K-1}` — cada instancia pertenece a **exactamente una** clase. Ejemplo: dígitos 0-9. → Cap. 10.

**Multietiqueta (multi-label).** Una instancia puede pertenecer a **múltiples** clases simultáneamente (ej.: gato Y pájaro en la misma imagen). Las clases NO son mutuamente excluyentes. → Cap. 10.

**One-vs-All (OVA / One-vs-Rest).** Entrenar `K` clasificadores binarios independientes (clase `i` vs todo lo demás). Predicción: `k* = argmax_k f_k(x)` (**Winner Takes All**). Costo: `O(K)` modelos. Riesgo: **regiones ambiguas** donde varios predicen positivo. → Cap. 10.

**All-vs-All (AVA / One-vs-One).** Entrenar `K(K-1)/2` clasificadores binarios, uno por cada par de clases. Predicción por **votación de mayoría**. Costo: `O(K²)` modelos. Más robusto pero más caro. → Cap. 10.

**Accuracy.** Métrica más simple: `predicciones correctas / total`. Aparece como `accuracy_score` en sklearn. → Cap. 10.

**Matriz de confusión.** Tabla `K × K` donde la entrada `(i, j)` es el número de ejemplos de clase real `i` que el modelo predijo como `j`. Diagonal = aciertos; fuera-diagonal = errores. Visualizada con `ConfusionMatrixDisplay`. → Cap. 10.

**Precisión, Recall, F1.** *NO desarrolladas en el material de Clases 1-2 — solo se menciona accuracy y matriz de confusión.* Definiciones canónicas se introducen en clases posteriores. → Cap. 10 (referencia externa).

---

## Notas finales — Cosas que NO están en el material y NO deben usarse como si lo estuvieran

La cátedra **NO** desarrolla en Clases 1-2:

- Validación cruzada k-fold (solo train/val/test holdout).
- Métricas F1, precision, recall, AUC, ROC.
- SVM, árboles, random forests, boosting.
- Redes neuronales profundas (solo se menciona perceptrón como "átomo").
- XOR y el "AI winter" de Minsky-Papert (se menciona la limitación de separabilidad sin invocar el ejemplo histórico).
- Cota matemática del teorema de convergencia del perceptrón (margen `γ`).
- Distinción formal "paramétrico vs no paramétrico" (se infiere por contraste).

Si una pregunta del estudio menciona estos términos, son **referencias externas** (Bishop, Murphy, Hastie) — ver `14-bibliografia.md`.

---

→ [12-formulario.md](12-formulario.md)
