# 08 — Naive Bayes

> Clase 2 — Modelos Probabilísticos | DiploDatos UNC 2026
> Material fuente: PDF clase 2 (p. 14–25) + Notebook 04 (Naive Bayes)
> Pre-requisitos: cap. 06 (regresión logística) y cap. 07 (multiclase con softmax — visto luego en este apunte como contraste).

---

## 1. Concepto

**Naive Bayes (NB)** es un clasificador **probabilístico generativo** que combina dos ingredientes:

1. **Regla de Bayes** para invertir el condicional: en lugar de modelar directamente $P(y\mid\mathbf{x})$, modela $P(\mathbf{x}\mid y)$ y $P(y)$.
2. **Supuesto naïve** (ingenuo): las features son **condicionalmente independientes dado y**.

La regla de decisión es:

$$
\hat{y} \;=\; \arg\max_{y}\; P(y)\prod_{j=1}^{n} P(x_j \mid y)
$$

A diferencia de regresión logística (que es **discriminativa** y modela $P(y\mid\mathbf{x})$ directamente), Naive Bayes asume cómo se **generan** los datos: primero se sortea la clase con $P(y)$, después se sortea cada feature independientemente con $P(x_j\mid y)$.

> Frase de la cátedra: "dos caminos distintos para llegar a probabilidades" (notebook 04).

**Ubicación en la taxonomía:**
- Paramétrico (estima un número fijo de probabilidades por clase, no crece con el training set).
- Generativo (modela la distribución conjunta $P(\mathbf{x}, y) = P(\mathbf{x}\mid y)P(y)$).
- Lineal en log-espacio (la frontera de decisión es lineal cuando las features son discretas con likelihoods multinomiales o Bernoulli — ver Bishop §4.2.3).

---

## 2. Intuición

### 2.1. La pregunta motivadora

> "Dado lo que observamos, ¿qué clase es más probable?" (notebook 04)

Tenés un email con palabras `["dinero", "oferta"]`. Querés decidir si es spam o no spam. La regla de Bayes te dice:

$$
P(\text{spam}\mid \text{dinero},\text{oferta}) \;\propto\; P(\text{spam})\cdot P(\text{dinero}\mid \text{spam})\cdot P(\text{oferta}\mid \text{spam})
$$

El supuesto "naïve" es asumir que `dinero` y `oferta` aparecen independientemente entre sí **dentro de la clase spam**. Es falso (las palabras se correlacionan), pero la cuenta funciona igual.

### 2.2. La metáfora del voto

> "Naive Bayes actúa como si cada variable aportara información independiente sobre la clase. Por ejemplo: una palabra en un texto, un píxel en una imagen. Cada una 'vota' por una clase. El modelo combina esos votos multiplicando probabilidades." (notebook 04)

Cada feature emite un voto cuantitativo (su likelihood), y NB **multiplica los votos** (equivale a sumar log-votos). Ganar = ser la clase con producto más alto.

### 2.3. Por qué se llama "naïve" (ingenuo)

Porque asume **independencia condicional** entre features dado y, algo que en la realidad casi nunca se cumple:
- Píxeles vecinos en una imagen están correlacionados.
- Palabras en un texto tienen co-ocurrencia (sintaxis, semántica).
- Altura y peso de una persona están fuertemente correlacionados.

**Reflexión de la cátedra:** "Naive Bayes sabe que no es del todo cierto: las variables son quasi-independientes entre sí, dado y" (notebook 04).

### 2.4. El gran misterio: ¿por qué funciona?

Aquí entra el paper clave **Domingos & Pazzani (1997)** — *On the Optimality of the Simple Bayesian Classifier under Zero-One Loss*. Demostraron que NB puede ser **óptimo bajo zero-one loss** (error de clasificación) incluso cuando el supuesto de independencia se viola drásticamente. La intuición:

- NB **no necesita estimar bien las probabilidades** (eso requeriría que el supuesto fuera cierto).
- Solo necesita que el **ordenamiento** de las clases por puntaje sea correcto. Es decir, basta con que la clase verdadera tenga el producto más alto, aunque los valores absolutos estén sesgados.

Por eso NB sigue compitiendo con modelos más sofisticados en tareas de texto, spam y diagnóstico — y por eso fue durante décadas el baseline obligatorio en NLP.

---

## 3. Cuerpo técnico

### 3.1. Teorema de Bayes — el motor

Para clases $y \in \{1, \dots, K\}$ y features $\mathbf{x} = (x_1, \dots, x_n)$:

$$
P(y\mid \mathbf{x}) \;=\; \frac{P(\mathbf{x}\mid y)\,P(y)}{P(\mathbf{x})}
$$

Donde:
- $P(y)$ = **prior**, qué tan frecuente es la clase y a priori.
- $P(\mathbf{x}\mid y)$ = **likelihood**, qué tan probable es observar $\mathbf{x}$ si la clase es y.
- $P(\mathbf{x})$ = **evidencia**, probabilidad marginal de $\mathbf{x}$ (independiente de y).
- $P(y\mid \mathbf{x})$ = **posterior**, lo que queremos.

**Truco clave:** como $P(\mathbf{x})$ no depende de y, podemos ignorarlo para el `argmax`:

$$
\hat{y} \;=\; \arg\max_y\, P(y\mid \mathbf{x}) \;=\; \arg\max_y\, P(\mathbf{x}\mid y)P(y)
$$

### 3.2. El supuesto naïve

Sin supuestos, $P(\mathbf{x}\mid y) = P(x_1, x_2, \dots, x_n \mid y)$ tiene una **complejidad combinatoria**: para n features binarias necesitarías $2^n$ parámetros por clase.

El supuesto naïve descompone:

$$
P(x_1, \dots, x_n \mid y) \;=\; \prod_{j=1}^{n} P(x_j \mid y)
$$

Ahora solo necesitás **n parámetros por clase** (uno por feature). Para MNIST 28×28 binarizado: $784 \times 10 = 7{,}840$ parámetros — una bicoca.

Combinando ambas piezas:

$$
\boxed{\;\hat{y} \;=\; \arg\max_y\, P(y) \prod_{j=1}^{n} P(x_j \mid y)\;}
$$

### 3.3. Estimación por Máxima Verosimilitud (MLE)

NB se entrena contando frecuencias en el training set.

**Prior:**

$$
\hat{P}(y) \;=\; \frac{\text{Count}(Y = y)}{\sum_{y'}\text{Count}(Y = y')} \;=\; \frac{N_y}{N}
$$

Si tenés 3 emails spam de 10 totales: $\hat{P}(\text{spam}) = 0.3$.

**Likelihood (caso discreto):**

$$
\hat{P}(X_j = x \mid Y = y) \;=\; \frac{\text{Count}(X_j = x, Y = y)}{\sum_{x'}\text{Count}(X_j = x', Y = y)}
$$

> "Estimar los parámetros de Naïve Bayes por MV equivale a calcular frecuencias relativas directamente desde los datos de entrenamiento." (PDF p. 17)

### 3.4. El problema del cero

**Escenario catastrófico:** entrenás un clasificador de reviews de cine. La palabra `"fantastic"` aparece varias veces en reviews positivas pero **nunca** en reviews negativas del training set. Entonces:

$$
\hat{P}(\text{"fantastic"} \mid \text{negativa}) \;=\; \frac{0}{n_{\text{negativa}}} \;=\; 0
$$

Ahora llega una review nueva: `"the movie was terrible but the soundtrack was fantastic"`. Tu producto:

$$
\hat{P}(\text{negativa}) \cdot \dots \cdot \underbrace{P(\text{fantastic}\mid \text{negativa})}_{=\,0} \cdot \dots \;=\; 0
$$

**Un único cero anula todo el producto.** La review se clasifica como positiva no porque sea positiva, sino porque NB no admite la posibilidad de que `"fantastic"` aparezca en una review negativa.

> Frase de la cátedra: "Un único cero anula todo el producto de likelihoods, sin importar cuántas otras palabras apoyen la clasificación." (PDF p. 23)

### 3.5. Suavizado de Laplace y Lidstone

**Lidstone (general):** sumar un pseudo-conteo $\alpha \geq 0$ a cada feature:

$$
\hat{P}(X_j = x \mid Y = y) \;=\; \frac{\text{count}(x_j, y) + \alpha}{\text{count}(y) + \alpha\cdot|V|}
$$

Donde $|V|$ es el tamaño del vocabulario (cantidad de valores posibles que puede tomar $X_j$).

**Laplace (add-one):** caso particular $\alpha = 1$.

$$
\hat{P}(X_j = x \mid Y = y) \;=\; \frac{\text{count}(x_j, y) + 1}{\text{count}(y) + |V|}
$$

**Interpretación bayesiana:** $\alpha$ es el parámetro de un prior Dirichlet conjugado sobre la multinomial. Equivale a haber "imaginado" $\alpha$ ocurrencias previas de cada palabra en cada clase antes de ver los datos.

**Casos límite:**
- $\alpha = 0$: MLE puro (sin suavizado, riesgo de ceros).
- $\alpha = 1$: Laplace (estándar didáctico).
- $\alpha < 1$ (típicamente 0.01 a 0.1): suavizado leve, menos sesgo en vocabularios grandes.
- $\alpha \to \infty$: distribución uniforme — pierde info de los datos.

**En sklearn:** el hiperparámetro es `alpha`, default 1.0.

### 3.6. Log-probabilidades (estabilidad numérica)

Multiplicar 1000 probabilidades chicas produce **underflow** (números menores al menor representable en float). Solución: trabajar en log-espacio.

$$
\log P(y\mid \mathbf{x}) \;\propto\; \log P(y) \;+\; \sum_{j=1}^{n} \log P(x_j\mid y)
$$

El `argmax` se preserva porque $\log$ es monótono creciente. Sklearn lo hace internamente: ver `feature_log_prob_` y `class_log_prior_`.

> "Multiplicar probabilidades se transforma en sumar logaritmos — más estable numéricamente." (notebook 04)

### 3.7. Las tres variantes en sklearn

| Variante | Likelihood asumida | Cuándo usar | Doc sklearn |
|---|---|---|---|
| `MultinomialNB` | Multinomial — conteos enteros (o tf-idf) | Texto con bag-of-words (frecuencias) | ver §8 |
| `GaussianNB` | Gaussiana por feature dentro de cada clase | Features continuas (mediciones físicas, embeddings densos) | ver §8 |
| `BernoulliNB` | Bernoulli — features binarias | Texto con presencia/ausencia, píxeles binarizados | ver §8 |

**Multinomial vs Bernoulli para texto** — McCallum & Nigam (1998) lo zanjaron empíricamente:
- **Bernoulli** funciona mejor con vocabularios chicos (modela ausencias explícitamente — la palabra que **no** apareció también vota).
- **Multinomial** funciona mejor con vocabularios grandes (reducción promedio del error del 27 % respecto a Bernoulli).

**Gaussian NB** asume $P(x_j\mid y) = \mathcal{N}(\mu_{j,y}, \sigma_{j,y}^2)$ y estima media y varianza por feature y clase. No usa suavizado tipo Laplace; en su lugar tiene `var_smoothing` (suma una pequeña constante a las varianzas para evitar singularidades).

### 3.8. Bag of Words (BoW) — la representación para texto

Antes de aplicar `MultinomialNB` a texto, necesitás vectorizar. El esquema canónico es **Bag of Words**:

- Cada palabra del vocabulario = una feature (una dimensión).
- El valor es **cuántas veces aparece la palabra** en el documento.
- Se pierde el orden (un texto = una bolsa de palabras, no una secuencia).
- Vectores **muy dispersos**: la mayoría de las palabras del vocabulario global no aparecen en cada documento.
- Vocabularios típicos: 10k–100k palabras, con sparsity > 99.9 %.

**Ejemplo (PDF p. 22):**

| Palabra | "el mejor guión" | "no es buena" | "de lo mejor" |
|---|---|---|---|
| de | 0 | 0 | 1 |
| es | 0 | 1 | 0 |
| no | 0 | 1 | 0 |
| buena | 0 | 1 | 0 |
| mejor | 1 | 0 | 1 |
| guión | 1 | 0 | 0 |

En sklearn esto lo hace `CountVectorizer`. Variante con normalización por documento + IDF: `TfidfVectorizer`. Manning, Raghavan & Schütze (2008) capítulo 13 es la referencia canónica.

### 3.9. Frontera de decisión: ¿lineal?

Para `MultinomialNB` y `BernoulliNB`, tomando logaritmo:

$$
\log P(y\mid \mathbf{x}) \;=\; \underbrace{\log P(y)}_{\text{constante por clase}} \;+\; \sum_j x_j \log P(\text{palabra } j\mid y) \;+\; \text{const}
$$

Lo cual es **lineal en $\mathbf{x}$**. Por eso NB y regresión logística producen fronteras **del mismo tipo geométrico** (hiperplanos), aunque los parámetros se estiman de forma muy diferente (Bishop §4.2.3 lo discute en detalle).

`GaussianNB` con varianzas distintas por clase produce fronteras **cuadráticas** (forma de QDA — Quadratic Discriminant Analysis con independencia entre features).

### 3.10. Sklearn — uso canónico

```python
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

vect = CountVectorizer()
X_train_vec = vect.fit_transform(X_train_text)  # matriz dispersa
X_test_vec = vect.transform(X_test_text)         # transform, NO fit_transform

mnb = MultinomialNB(alpha=1.0)
mnb.fit(X_train_vec, y_train)

mnb.predict(X_test_vec)
mnb.predict_proba(X_test_vec)
```

**Atributos importantes:**
- `mnb.classes_` — array con los nombres de las clases.
- `mnb.class_count_` — vector con cuántos ejemplos hay por clase en el training set.
- `mnb.feature_count_` — matriz `(n_clases, n_features)` con conteos crudos.
- `mnb.class_log_prior_` — log del prior por clase. `np.exp(...)` recupera el prior.
- `mnb.feature_log_prob_` — log de la likelihood ya suavizada. `np.exp(...)` recupera $P(x_j\mid y)$.

---

## 4. Ejemplo numérico

### 4.1. Corpus toy Chinese / Japan (notebook 04)

**Training set:**

```python
training = [
    ('chinese beijing chinese',   'zh'),
    ('chinese chinese shangai',   'zh'),
    ('chinese macao',             'zh'),
    ('tokyo japan chinese',       'ja'),
]
```

**Vocabulario:** $V = \{\text{chinese, beijing, shangai, macao, tokyo, japan}\}$, $|V| = 6$.

**Prior:**
$$P(zh) = 3/4 = 0.75,\quad P(ja) = 1/4 = 0.25$$

**Conteos crudos:**

| palabra | en zh | en ja |
|---|---|---|
| chinese | 5 | 1 |
| beijing | 1 | 0 |
| shangai | 1 | 0 |
| macao | 1 | 0 |
| tokyo | 0 | 1 |
| japan | 0 | 1 |
| **total tokens** | **8** | **3** |

**Likelihoods con Laplace (α=1, |V|=6):**

$$\hat{P}(\text{chinese}\mid zh) = \frac{5+1}{8+6} = \frac{6}{14} \approx 0.4286$$

$$\hat{P}(\text{tokyo}\mid zh) = \frac{0+1}{8+6} = \frac{1}{14} \approx 0.0714$$

$$\hat{P}(\text{chinese}\mid ja) = \frac{1+1}{3+6} = \frac{2}{9} \approx 0.2222$$

$$\hat{P}(\text{tokyo}\mid ja) = \frac{1+1}{3+6} = \frac{2}{9} \approx 0.2222$$

(Sin Laplace, $P(\text{tokyo}\mid zh) = 0$ y todo el producto se anularía.)

### 4.2. Predicción para `"chinese chinese chinese tokyo japan"`

**Score zh:**

$$
\text{score}(zh) = P(zh)\cdot P(\text{chinese}\mid zh)^3 \cdot P(\text{tokyo}\mid zh) \cdot P(\text{japan}\mid zh)
$$

$$
= 0.75 \cdot (6/14)^3 \cdot (1/14) \cdot (1/14) \;\approx\; 0.75 \cdot 0.0787 \cdot 0.0714 \cdot 0.0714 \;\approx\; 3.01\times 10^{-4}
$$

**Score ja:**

$$
\text{score}(ja) = 0.25 \cdot (2/9)^3 \cdot (2/9) \cdot (2/9) \;\approx\; 0.25 \cdot 0.01097 \cdot 0.2222 \cdot 0.2222 \;\approx\; 1.35\times 10^{-4}
$$

**Predicción:** `zh` (3.01 × 10⁻⁴ > 1.35 × 10⁻⁴).

**Normalizando** (dividiendo cada score por la suma):

$$
P(zh\mid \mathbf{x}) \approx \frac{3.01}{3.01+1.35} \approx 0.69
$$
$$
P(ja\mid \mathbf{x}) \approx \frac{1.35}{3.01+1.35} \approx 0.31
$$

### 4.3. Spam toy (notebook 04)

| Email | Clase |
|---|---|
| "gana dinero rápido" | spam |
| "oferta exclusiva" | spam |
| "reunión mañana" | no_spam |
| "informe proyecto" | no_spam |

Estimaciones simplificadas (cátedra usa frecuencias inventadas, no MLE estricto):
- $P(\text{spam}) = 0.5$, $P(\text{no\_spam}) = 0.5$
- $P(\text{dinero}\mid \text{spam}) = 0.8$, $P(\text{oferta}\mid \text{spam}) = 0.7$
- $P(\text{dinero}\mid \text{no\_spam}) = 0.10$, $P(\text{oferta}\mid \text{no\_spam}) = 0.05$

**Clasificar `"dinero oferta"`:**
- $\text{score}(\text{spam}) = 0.5 \cdot 0.8 \cdot 0.7 = 0.28$
- $\text{score}(\text{no\_spam}) = 0.5 \cdot 0.10 \cdot 0.05 = 0.0025$
- $\Rightarrow \text{spam}$ (gana por dos órdenes de magnitud).

### 4.4. En código (sklearn)

```python
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import numpy as np

X_train = ['chinese beijing chinese',
           'chinese chinese shangai',
           'chinese macao',
           'tokyo japan chinese']
y_train = ['zh', 'zh', 'zh', 'ja']

vect = CountVectorizer()
X2 = vect.fit_transform(X_train)
# vect.get_feature_names_out() => ['beijing','chinese','japan','macao','shangai','tokyo']

mnb = MultinomialNB(alpha=1.0)
mnb.fit(X2, y_train)

X_test = vect.transform(['chinese chinese chinese tokyo japan'])
mnb.predict(X_test)         # array(['zh'], dtype='<U2')
mnb.predict_proba(X_test)   # [[0.31..., 0.69...]] aprox

np.exp(mnb.class_log_prior_)    # [0.25, 0.75]   (orden: classes_)
np.exp(mnb.feature_log_prob_)   # matriz con las P(x_j|y) suavizadas
```

---

## 5. Conexión con el TP

> **TP1** (regresión lineal y polinomial) **no toca Naive Bayes**. NB aparecerá en el **TP2** junto con regresión logística, KNN y comparativas de clasificadores.

Cuando llegue ese TP, vas a tener que:

1. **Vectorizar texto** con `CountVectorizer` o `TfidfVectorizer`.
2. **Probar las tres variantes** (`MultinomialNB`, `BernoulliNB`, `GaussianNB`) y justificar cuál corresponde a cada tipo de feature.
3. **Tunear `alpha`** vía validación cruzada (rango típico: $\{0.001, 0.01, 0.1, 0.5, 1, 2, 5\}$).
4. **Reportar accuracy + matriz de confusión + precision/recall por clase** (no solo accuracy: en spam-like tasks la clase positiva suele ser minoritaria).
5. **Comparar con regresión logística** sobre el mismo dataset — ver quién gana, por cuánto, y conjeturar por qué.

**Patrón mental para el TP:**
- Features de **conteos** (frecuencias) → `MultinomialNB`.
- Features **binarias** (presencia/ausencia, dummies) → `BernoulliNB`.
- Features **continuas** (mediciones, longitudes) → `GaussianNB` o estandarizar y usar logística.

---

## 6. Errores comunes

### 6.1. Olvidar el suavizado y comerse un cero

**Síntoma:** todas las predicciones convergen a una clase, o `predict_proba` devuelve `nan`.

**Causa:** una palabra del test no estaba en una clase del train → $P=0$ → producto cero → log = $-\infty$.

**Fix:** `MultinomialNB(alpha=1.0)` (default) o cualquier $\alpha > 0$. **Nunca** uses $\alpha=0$ en producción.

### 6.2. Usar `MultinomialNB` con features negativas

**Síntoma:** `ValueError: Negative values in data passed to MultinomialNB (input X)`.

**Causa:** la multinomial asume conteos no-negativos. Si estandarizaste features (`StandardScaler`) o tenés datos con signo, no podés usar `MultinomialNB`.

**Fix:** usar `GaussianNB` (acepta cualquier real) o re-escalar con `MinMaxScaler` a [0, 1].

### 6.3. Usar `GaussianNB` cuando las features no son ni remotamente gaussianas

**Síntoma:** accuracy mucho peor que regresión logística sobre el mismo dataset.

**Causa:** features muy sesgadas, multimodales o categóricas codificadas como enteros.

**Fix:** transformaciones (log, Box-Cox) o usar otro modelo.

### 6.4. Vectorizar test con `fit_transform` (data leakage clásico)

**Síntoma:** accuracy en test sospechosamente alta; el modelo "ve" palabras del test en el vocabulario.

**Fix:** `vect.fit_transform(X_train)` y después `vect.transform(X_test)`. El vocabulario se ajusta **solo** con train.

### 6.5. Confundir las tres variantes

**Síntoma:** usar `BernoulliNB` con conteos, o `MultinomialNB` con features continuas.

**Fix:** mapeo mental:
- ¿Features cuentan ocurrencias? → Multinomial.
- ¿Features son 0/1? → Bernoulli.
- ¿Features son reales con distribución unimodal? → Gaussian.

### 6.6. Asumir que `predict_proba` es una probabilidad calibrada

**Síntoma:** usás las probabilidades para tomar decisiones de negocio (umbrales económicos) y los números mienten.

**Causa:** NB es famoso por dar probabilidades mal calibradas (suelen ser muy extremas, cerca de 0 o 1) — precisamente porque el supuesto de independencia infla la confianza al multiplicar muchas probabilidades correlacionadas.

**Fix:** usar `CalibratedClassifierCV` con `method='isotonic'` o `'sigmoid'` (Platt scaling).

### 6.7. Multiplicar probabilidades en lugar de sumar logs

**Síntoma:** con vocabularios grandes (> 1000 palabras), `predict_proba` devuelve ceros o `nan`.

**Causa:** underflow numérico.

**Fix:** sklearn ya trabaja en log-espacio internamente. Si implementás NB a mano, **siempre** usá log.

---

## 7. Checklist

- [ ] Sé escribir la regla de Bayes desde cero y explicar cada término (prior, likelihood, posterior, evidencia).
- [ ] Sé enunciar el supuesto naïve y dar dos ejemplos donde **no** se cumple.
- [ ] Puedo calcular a mano $\hat{P}(y)$ y $\hat{P}(x_j\mid y)$ a partir de conteos del training set.
- [ ] Entiendo por qué un cero anula todo el producto.
- [ ] Sé escribir la fórmula de Laplace y Lidstone, y qué hace $\alpha$.
- [ ] Sé cuándo usar `MultinomialNB`, `GaussianNB` y `BernoulliNB`.
- [ ] Sé qué hace `CountVectorizer` y por qué nunca llamarlo con `fit_transform` sobre el test.
- [ ] Puedo explicar el resultado de Domingos & Pazzani (1997) en una oración.
- [ ] Sé inspeccionar `class_log_prior_` y `feature_log_prob_` y reconstruir las probabilidades.
- [ ] Sé por qué se trabaja en log-espacio (underflow).
- [ ] Entiendo que las probabilidades de NB suelen estar **mal calibradas** aunque las decisiones sean correctas.

---

## 8. Para profundizar

### 8.1. Lecturas obligadas

- **Bishop, *PRML* §4.2** — "Probabilistic Generative Models". Deriva la frontera de decisión de NB, muestra por qué es lineal con likelihoods exponenciales y compara con regresión logística (§4.3).
- **Bishop, *PRML* §2.5** — "Nonparametric Methods". Si bien es de KNN, contiene el marco general de estimación de densidad que NB extiende a clasificación.
- **Murphy, *Probabilistic Machine Learning* §9** — "Generative models for classification". Tratamiento más reciente que Bishop, incluye Naive Bayes Gaussian y su relación con QDA/LDA.
- **Manning, Raghavan & Schütze (2008), *Introduction to Information Retrieval*, capítulo 13** — *Text Classification and Naive Bayes*. La referencia canónica para NB en NLP. Disponible online gratis: https://nlp.stanford.edu/IR-book/html/htmledition/text-classification-and-naive-bayes-1.html

### 8.2. Papers fundamentales

- **Domingos, P. & Pazzani, M. (1997)** — "On the Optimality of the Simple Bayesian Classifier under Zero-One Loss", *Machine Learning* 29(2-3), 103-130. DOI: [10.1023/A:1007413511361](https://doi.org/10.1023/A:1007413511361). **MUST READ**: explica matemáticamente por qué NB funciona aunque el supuesto sea falso.
- **McCallum, A. & Nigam, K. (1998)** — "A Comparison of Event Models for Naive Bayes Text Classification", *AAAI-98 Workshop on Learning for Text Categorization*. PDF: https://aaai.org/papers/041-ws98-05-007/. Comparativa empírica Multinomial vs Bernoulli — el Multinomial gana ~27 % de reducción de error en vocabularios grandes.

### 8.3. Documentación de sklearn

- Naive Bayes overview: https://scikit-learn.org/stable/modules/naive_bayes.html
- `MultinomialNB`: https://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.MultinomialNB.html
- `GaussianNB`: https://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.GaussianNB.html
- `BernoulliNB`: https://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.BernoulliNB.html
- `CountVectorizer`: https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html

### 8.4. Extensiones que vale la pena conocer

- **Complement Naive Bayes** (`ComplementNB`): variante que funciona mejor con clases muy desbalanceadas (ver Rennie et al. 2003, "Tackling the Poor Assumptions of Naive Bayes Text Classifiers").
- **Calibración de probabilidades**: NB devuelve scores correctos en argmax pero probabilidades sesgadas. Usar `CalibratedClassifierCV` para producción.
- **Naive Bayes semi-supervisado** con EM (Nigam et al. 2000) — usa documentos sin etiquetar para mejorar el modelo.

---

## Próximo paso

→ [09-knn-y-no-parametricos.md](09-knn-y-no-parametricos.md) — KNN y la familia de modelos no paramétricos. Acá empezamos con clasificadores **paramétricos generativos** (NB) y los **paramétricos discriminativos** (logística, ver cap. 06). En el próximo apunte cruzamos al lado **no paramétrico**, donde el modelo no resume los datos en una fórmula fija sino que los **conserva enteros**.

---

## Referencias

### Material de cátedra
- PDF Clase 2 (DiploDatos UNC 2026), p. 14–25 — Bloque Naive Bayes.
- Notebook 04 — "Naive Bayes — corpus Chinese/Japan y ejemplo Spam".

### Bibliografía canónica
- Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*, Springer. Cap. 4.2 (modelos generativos).
- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*, MIT Press. Cap. 9 (modelos generativos para clasificación).
- Manning, C. D., Raghavan, P., & Schütze, H. (2008). *Introduction to Information Retrieval*, Cambridge University Press. Cap. 13 (Text Classification and Naive Bayes). Online: https://nlp.stanford.edu/IR-book/

### Papers
- Domingos, P., & Pazzani, M. (1997). "On the Optimality of the Simple Bayesian Classifier under Zero-One Loss". *Machine Learning*, 29(2-3), 103-130. DOI: [10.1023/A:1007413511361](https://doi.org/10.1023/A:1007413511361).
- McCallum, A., & Nigam, K. (1998). "A Comparison of Event Models for Naive Bayes Text Classification". *AAAI-98 Workshop on Learning for Text Categorization*, 41-48. PDF: https://aaai.org/papers/041-ws98-05-007/

### Documentación sklearn
- Naive Bayes (overview): https://scikit-learn.org/stable/modules/naive_bayes.html
- `MultinomialNB`: https://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.MultinomialNB.html
- `GaussianNB`: https://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.GaussianNB.html
- `BernoulliNB`: https://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.BernoulliNB.html
- `CountVectorizer`: https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html
