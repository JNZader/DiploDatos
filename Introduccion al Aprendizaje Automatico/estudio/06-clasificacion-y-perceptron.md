# 06 — Clasificación y Perceptrón

> "De la regresión a la decisión: aprender fronteras en espacios de características para asignar clases a nuevas observaciones." — Cátedra, PDF Clase 1 p. 28
>
> "El perceptrón es el átomo de las redes neuronales profundas modernas." — PDF Clase 1 p. 34

---

## 1. Concepto

**Clasificación supervisada binaria.** Dado un conjunto etiquetado

$$
D = \{(\mathbf{x}_i, y_i)\}_{i=1}^N, \qquad \mathbf{x}_i \in \mathbb{R}^n, \quad y_i \in \{+1, -1\}
$$

queremos aprender $h: \mathbb{R}^n \to \{+1, -1\}$ que, dado un nuevo $\mathbf{x}$, le asigne la etiqueta correcta. A diferencia de la regresión (caps. 02–05), el target es **discreto**.

**El perceptrón** (Rosenblatt, 1958) es el clasificador lineal seminal: el primer algoritmo de aprendizaje supervisado con **garantía de convergencia** cuando los datos son linealmente separables. Es además el ancestro directo de las redes neuronales modernas: cada neurona artificial es, en esencia, un perceptrón con una función de activación más suave.

> **Convención de etiquetas:** en perceptrón usamos $y \in \{+1, -1\}$, **no** $\{0, 1\}$. La regla de actualización se simplifica enormemente con $\pm 1$ (§3.4). Para regresión logística (cap. 07) se vuelve a $\{0, 1\}$ por compatibilidad con la Bernoulli.

---

## 2. Intuición

### 2.1. Software 2.0 aplicado a categorías

En Software 1.0 escribirías "si el email contiene 'gratis' y >3 signos !, marcar spam". En Software 2.0 le mostrás miles de emails etiquetados y dejás que el modelo **infiera la frontera**.

La cátedra usa dos ejemplos canónicos (PDF Clase 1 p. 30): **detección de fraude** (input: monto/hora/ubicación; output: ¿fraude?) y **perro vs gato** (input: píxeles; output: clase). En ambos, el modelo aprende un **hiperplano** $\mathbf{w}^T \mathbf{x} + b = 0$ que parte el espacio de features en dos regiones.

### 2.2. Termómetro vs termostato

Pensá en un termómetro (output continuo: temperatura) vs un termostato (output binario: on/off). El termostato toma la lectura continua y la compara contra un umbral. El perceptrón hace exactamente eso:

- **Fase score** (termómetro): $f(\mathbf{x}) = \mathbf{w}^T \mathbf{x} + b$ → confianza continua.
- **Fase threshold** (termostato): $\hat{y} = \text{sign}(f(\mathbf{x}))$ → etiqueta discreta.

La función $\text{sign}$ es nuestra primera **función de activación**. Las redes modernas la reemplazan por sigmoide/ReLU/tanh para poder derivar y usar descenso de gradiente — pero la idea es la misma.

---

## 3. Cuerpo técnico

### 3.1. Formalización (PDF Clase 1 p. 31)

Queremos $f: \mathbb{R}^n \to \mathbb{R}$ tal que

$$
f(\mathbf{x}_i) \begin{cases} \geq 0 & \text{si } y_i = +1 \\ < 0 & \text{si } y_i = -1 \end{cases}
$$

**Condición compacta de clasificación correcta** (gracias a $\pm 1$):

$$
y_i \cdot f(\mathbf{x}_i) > 0
$$

Cuando $y_i = +1$ y $f > 0$, producto positivo. Cuando $y_i = -1$ y $f < 0$, también (negativo × negativo). Solo es negativo si hay error. Esa es la razón de usar $\{+1, -1\}$ en vez de $\{0, 1\}$.

### 3.2. Separabilidad lineal (PDF Clase 1 p. 32)

**Definición.** $D$ es **linealmente separable** si existen $\mathbf{w}^* \in \mathbb{R}^n$ y $b^* \in \mathbb{R}$ tales que $y_i \cdot (\mathbf{w}^{*T} \mathbf{x}_i + b^*) > 0$ para todo $i$. Equivalentemente, existe un hiperplano que deja todos los positivos de un lado y todos los negativos del otro.

**Margen** (estándar — no está en el PDF pero aparece en Novikoff):

$$
\gamma = \min_i \frac{y_i \cdot (\mathbf{w}^{*T} \mathbf{x}_i + b^*)}{\|\mathbf{w}^*\|}
$$

Es la distancia del punto **más cercano** al hiperplano separador óptimo. $\gamma > 0$ por construcción.

| Caso | Algoritmo |
|------|-----------|
| **Linealmente separable** | Perceptrón **converge** en pasos finitos. |
| **NO separable** | Perceptrón **no converge nunca**. Alternativas: SVM con kernel, regresión logística, MLP. |

### 3.3. Arquitectura: dos fases (PDF Clase 1 p. 33)

**Fase A — Scoring (combinación lineal):**

$$
f(\mathbf{x}) = \mathbf{w}^T \mathbf{x} + b
$$

- $\mathbf{w}$ son los **pesos** (cuánto pesa cada feature).
- $b$ es el **bias / intercepto** (desplaza el hiperplano respecto al origen).
- $f(\mathbf{x})$ es el **score**: cuanto más grande $|f(\mathbf{x})|$, más lejos del límite.

**Truco habitual:** absorber $b$ en $\mathbf{w}$ agregando $x_0 = 1$ ⇒ $f(\mathbf{x}) = \tilde{\mathbf{w}}^T \tilde{\mathbf{x}}$. Mismo truco que en regresión lineal (cap. 03). El notebook 02 de la cátedra **no** incluye bias y eso trae consecuencias geométricas (§4.3).

**Fase B — Thresholding (activación):**

$$
\hat{y} = \text{sign}(f(\mathbf{x})) = \begin{cases} +1 & f(\mathbf{x}) \geq 0 \\ -1 & f(\mathbf{x}) < 0 \end{cases}
$$

### 3.4. Algoritmo del perceptrón (PDF Clase 1 p. 34–35)

**Hiperparámetros:** $r \in (0, 1]$ (tasa, la cátedra usa $r$, no $\eta$) y $T_{\max}$.

**Pseudocódigo:**

```
Entrada: D = {(x_i, y_i)} con y_i ∈ {+1,-1}, tasa r
1. Inicializar w^(0) := 0
2. Mientras haya errores y step < T_max:
     Para cada (x_i, y_i):
         ŷ_i := sign(w^T · x_i)
         Si ŷ_i ≠ y_i:                          # mal clasificado
             w := w + r · y_i · x_i             # ¡actualizar!
             step += 1
3. Devolver w
```

**La regla clave:**

$$
\boxed{\mathbf{w}^{(i+1)} = \mathbf{w}^{(i)} + r \cdot y_i \cdot \mathbf{x}_i \qquad \text{(solo si } \hat{y}_i \neq y_i\text{)}}
$$

**¿Por qué funciona?** Si mal clasificamos un punto con $y_i = +1$ (debía ser positivo y dio negativo), $\mathbf{w}^T\mathbf{x}_i < 0$. Tras actualizar, el nuevo score sobre el mismo punto:

$$
(\mathbf{w} + r\mathbf{x}_i)^T \mathbf{x}_i = \mathbf{w}^T\mathbf{x}_i + r\|\mathbf{x}_i\|^2
$$

aumenta en $r\|\mathbf{x}_i\|^2 > 0$. **Empujamos el hiperplano hacia el punto que clasificamos mal**. Si lo hacemos suficientes veces, el punto queda del lado correcto. Lo mismo simétricamente para $y_i = -1$. La notación $\pm 1$ unifica ambos casos.

> **Algoritmo online.** El perceptrón procesa una muestra a la vez y actualiza solo ante errores. No necesita el batch en memoria.

### 3.5. Geometría: $\mathbf{w}$ es perpendicular a la frontera

La frontera es $\{\mathbf{x} : \mathbf{w}^T\mathbf{x} + b = 0\}$. Si $\mathbf{x}_a, \mathbf{x}_b$ están sobre ella, $\mathbf{w}^T(\mathbf{x}_a - \mathbf{x}_b) = 0$ ⇒ **$\mathbf{w}$ es perpendicular a cualquier vector sobre la frontera**. Apunta del lado negativo hacia el positivo.

Frase literal de la cátedra (notebook 02, celda 59): *"El vector $\mathbf{w}$ es perpendicular a la recta o al hiperplano."*

### 3.6. Teorema de convergencia de Novikoff (1962)

La cátedra lo enuncia sin demostrar (PDF p. 38). Vale la pena precisarlo.

**Teorema (Novikoff, 1962).** Sea $D$ linealmente separable, con $\|\mathbf{x}_i\| \leq R$ para todo $i$, y supongamos que existe $\mathbf{w}^*$ con $\|\mathbf{w}^*\| = 1$ y margen $\gamma > 0$ tal que $y_i \cdot \mathbf{w}^{*T}\mathbf{x}_i \geq \gamma$ para todo $i$. Entonces el perceptrón (inicializado en $\mathbf{0}$, sin bias) realiza **a lo sumo**

$$
M \leq \left(\frac{R}{\gamma}\right)^2
$$

actualizaciones antes de converger.

**Interpretación.**
- Margen $\gamma$ chico → algoritmo tarda mucho.
- Datos mal escalados ($R$ grande) → cota crece cuadráticamente.
- Si NO separables, $\gamma$ no existe → puede oscilar para siempre.

**Práctico:** **normalizá features** antes de entrenar (`StandardScaler`).

### 3.7. La limitación de XOR (Minsky & Papert, 1969)

La cátedra menciona el límite (*"no converge nunca"*) sin invocar el caso histórico. Lo agrego porque **es** el caso que paralizó la IA durante 15 años.

**XOR:**

| $x_1$ | $x_2$ | XOR |
|-------|-------|-----|
| 0 | 0 | $-1$ |
| 0 | 1 | $+1$ |
| 1 | 0 | $+1$ |
| 1 | 1 | $-1$ |

Graficá los 4 puntos: los positivos forman una diagonal, los negativos la otra. **No existe recta que separe las clases.** Es la falla estructural del perceptrón monocapa.

**El golpe histórico.** En 1969 Minsky y Papert publicaron *Perceptrons*, demostrando que el perceptrón monocapa **no puede aprender XOR** ni cualquier función no separable. El libro produjo el **primer invierno de la IA** (~1969–1986).

**La salida.** Backpropagation (Rumelhart, Hinton, Williams, 1986) permitió entrenar redes con **capas ocultas**. Una red con 1 capa oculta de 2 neuronas resuelve XOR: la primera capa "rota" el espacio, la segunda hace separación lineal en el espacio transformado.

> **Por eso el perceptrón es "el átomo" de las redes profundas.** Cada neurona de una red profunda **es** un perceptrón con activación diferenciable y backprop. La idea sobrevive; la limitación se supera apilando capas.

### 3.8. Perceptrón clásico vs descenso de gradiente (PDF p. 39)

| Perceptrón clásico | Algoritmo estándar (GD con MSE) |
|--------------------|---------------------------------|
| Solo actualiza ante error | Siempre actualiza |
| Loss 0/1 (no diferenciable) | Loss diferenciable |
| Converge en finito si separable | Converge al óptimo de $J$ |
| Online | Suele ser batch/mini-batch |

**¿Por qué no 0/1 loss?** Su derivada es cero casi en todas partes. Sin gradiente, no hay descenso de gradiente. **La regla clásica del perceptrón es un truco para evitar la no-diferenciabilidad** (solo actualiza ante error).

**Solución diferenciable (PDF p. 39):** $J(\mathbf{w}) = \frac{1}{2}\sum_i (\mathbf{w}^T\mathbf{x}_i - y_i)^2$. Funciona pero es subóptimo. **El camino correcto** es regresión logística (cap. 07): reemplazá $\text{sign}$ por sigmoide → cross-entropy convexa → descenso de gradiente limpio.

**Advertencia cátedra:** "Si $r$ es muy grande, los pesos oscilan y el algoritmo no converge."

### 3.9. sklearn: `linear_model.Perceptron`

```python
from sklearn.linear_model import Perceptron
clf = Perceptron(
    penalty=None, alpha=0.0001,
    fit_intercept=True,         # incluye bias por default
    max_iter=1000, tol=1e-3,
    eta0=1.0,                   # learning rate (cátedra: r)
    random_state=0,
)
clf.fit(X_train, y_train)
clf.coef_, clf.intercept_       # pesos aprendidos
```

**Detalle de implementación:** internamente es un wrapper sobre `SGDClassifier` con `loss="perceptron"` y `learning_rate="constant"`. Para `penalty=None` el comportamiento coincide con Rosenblatt clásico.

---

## 4. Ejemplo numérico

### 4.1. Setup (notebook 02)

```python
from sklearn.datasets import make_classification
import numpy as np

X, y_true = make_classification(
    n_samples=100, n_features=2, n_classes=2,
    n_redundant=0, n_informative=2,
    n_clusters_per_class=1, class_sep=0.5,
    random_state=1,
)
y_true[y_true == 0] = -1     # convertir {0,1} → {-1,+1}

train_size = 60
X_train, X_val = X[:train_size], X[train_size:]
y_train, y_val = y_true[:train_size], y_true[train_size:]
```

`class_sep=0.5` = "clases moderadamente cercanas". Split manual 60/40.

### 4.2. Implementación didáctica (replicando el notebook)

```python
def predict(X, w):
    return np.sign(np.dot(X, w))

def accuracy(y_true, y_pred):
    return (y_true == y_pred).sum() / y_true.shape[0]

w = np.ones(2)                # inicialización "mala" intencional
r = 0.5
step = 0
finished = False
while not finished:
    y_pred = predict(X_train, w)
    if (y_train == y_pred).all():
        finished = True
    else:
        i = np.where(y_train != y_pred)[0][0]    # primer mal clasificado
        xi, yi = X_train[i], y_train[i]
        w = w + r * xi * yi                       # ¡la regla!
        step += 1
```

### 4.3. Resultado y geometría

Tras convergencia el notebook reporta (celda 59): $\mathbf{w}^* \approx (-0.6743,\ 0.0243)$, con $|w_1| \approx 27.7\,|w_2|$.

1. **Frontera dada por $\mathbf{w}^T\mathbf{x} = 0$** (sin bias) → $x_2 = -(w_1/w_2) x_1 \approx 27.7 x_1$.
2. **Sin bias, la frontera pasa obligatoriamente por el origen** → restricción fuerte. Si las clases tuvieran centro de masa lejos del origen, no se podrían separar.
3. **$|w_1| \gg |w_2|$** → la decisión depende casi solo de $x_1$.
4. **$\mathbf{w}$ apunta perpendicular a la frontera, hacia los positivos.**

### 4.4. Experimento con la tasa de aprendizaje

El notebook explora $r \in \{0.001, 0.01, 0.1, 0.5, 1.0\}$:
- $r$ muy chico → la actualización ni cambia el signo de $\mathbf{w}^T\mathbf{x}$.
- $r$ grande → oscilaciones.
- $r = 0.5$ o $1.0$ funciona bien.

**Detalle teórico:** en el perceptrón clásico **$r$ no afecta la convergencia** (solo escala $\mathbf{w}$). El número de actualizaciones según Novikoff es independiente de $r$. El learning rate solo importa para el **algoritmo estándar con MSE**.

### 4.5. Ejemplo "a mano": XOR (caso testigo)

Con $\mathbf{w} = (0, 0)$, $r = 1$, etiquetas $\pm 1$:
- $\mathbf{x}_1 = (0,0)$: $\hat{y} = +1 \neq -1$ → mal. Update: $\mathbf{w} + 1\cdot(-1)\cdot(0,0) = (0,0)$ (no cambia, $\mathbf{x}_1 = \mathbf{0}$).
- $\mathbf{x}_2 = (0,1)$: $\hat{y} = +1 = +1$ ✓.
- $\mathbf{x}_3 = (1,0)$: $\hat{y} = +1 = +1$ ✓.
- $\mathbf{x}_4 = (1,1)$: $\hat{y} = +1 \neq -1$ → mal. Update: $\mathbf{w} = (-1, -1)$.
- Reiniciamos pasada: $\mathbf{x}_1 = (0,0)$ → mal otra vez...

**Nunca converge.** No importa cuántas épocas le des. Consecuencia de Novikoff al revés: $\gamma$ no existe ⇒ cota infinita.

---

## 5. Conexión con el TP

**Estado:** el TP1 (*Laboratorio 1: Regresión en California*) **no toca clasificación** — es íntegramente regresión continua. Clasificación + perceptrón + logística entran en **TP2** (clases 3–4).

**Lo que te llevás del TP1 para TP2:**
1. **Notación $\pm 1$ vs $\{0,1\}$.** Cuando aparezca clasificación binaria, fijate si pide perceptrón ($\pm 1$) o logística ($\{0,1\}$).
2. **Pipeline limpio.** `make_pipeline(StandardScaler, Perceptron)` — análogo a `make_pipeline(PolynomialFeatures, LinearRegression)` del TP1.
3. **Train/val/split + métricas.** Misma disciplina, distinta métrica (accuracy en vez de MSE).
4. **Identificar overfitting.** Síntoma: train accuracy ~1.0, val baja.
5. **Feature scaling.** Novikoff te lo dice: $R = \max_i\|\mathbf{x}_i\|$ aparece al cuadrado en la cota. **Escalá features.**

**Adaptación mental** (si extendieras TP1 a clasificación binaria):

```python
y_binary = (y_continuous > 2.0).astype(int)    # 2.0 = 200k USD
y_binary[y_binary == 0] = -1                    # convertir a ±1
clf = make_pipeline(StandardScaler(), Perceptron(max_iter=1000, random_state=0))
clf.fit(X_train, y_train_binary)
```

Pero ojo: California Housing probablemente **no sea linealmente separable** así → accuracy mediocre → necesitarás logística (cap. 07) o SVM.

---

## 6. Errores comunes

1. **Confundir $\{0,1\}$ con $\{+1,-1\}$.** Con $\{0,1\}$ los puntos de clase 0 nunca actualizan los pesos (porque $y_i \mathbf{x}_i = 0$). La regla **requiere** $\pm 1$.
2. **Olvidar el bias.** Sin bias, la frontera está obligada a pasar por el origen. Para clases con centro de masa lejos del origen, te quedás sin solución. **Siempre incluí bias** salvo en ejercicios didácticos.
3. **Esperar convergencia con datos no separables.** El perceptrón **no converge nunca** en ese caso. **Siempre `max_iter` finito** o usá variante Pocket.
4. **No escalar features.** Novikoff: $M \leq (R/\gamma)^2$. $R$ grande = lentitud cuadrática. **`StandardScaler` siempre.**
5. **$r$ mal calibrada en gradient descent.** En perceptrón clásico no afecta convergencia. En la versión con gradiente, $r$ grande → oscilaciones (advertencia explícita de la cátedra).
6. **Online vs batch.** El perceptrón clásico es online; existen variantes batch. La cátedra enseña la versión online.
7. **Creer que encuentra el "mejor" hiperplano.** Falso. Encuentra **alguno** que separa (cuando separable). No es único, no es de máximo margen (eso es SVM). Depende de orden de procesamiento e inicialización.
8. **No usar Pocket para datos no separables.** Pocket guarda el mejor $\mathbf{w}$ visto (menor # errores) y lo devuelve al final. Es el ejercicio 3 del notebook 02.
9. **Confundir bias con regularization bias / bias estadístico.** Tres conceptos con el mismo nombre. Contexto manda.
10. **`Perceptron` de sklearn ≠ algoritmo clásico puro.** Es SGD con `loss="perceptron"`, learning rate constante. Para `penalty=None` coincide; con regularización ya no es Rosenblatt.

---

## 7. Checklist

- [ ] Sé formalizar clasificación binaria con $y_i \in \{+1,-1\}$ y la condición $y_i f(\mathbf{x}_i) > 0$.
- [ ] Puedo definir "linealmente separable" rigurosamente.
- [ ] Sé escribir la regla $\mathbf{w}^{(i+1)} = \mathbf{w}^{(i)} + r y_i \mathbf{x}_i$ y argumentar geométricamente por qué funciona.
- [ ] Conozco el enunciado del teorema de Novikoff ($M \leq R^2/\gamma^2$).
- [ ] Sé explicar XOR como caso testigo de no separabilidad + contexto histórico Minsky & Papert 1969.
- [ ] Entiendo que el perceptrón es **el átomo** de las redes profundas (con activación + capas + backprop).
- [ ] Sé implementar el algoritmo en NumPy en <15 líneas.
- [ ] Sé usar `sklearn.linear_model.Perceptron` con sus hiperparámetros.
- [ ] Reconozco 3+ limitaciones: no separable → no converge; no da probabilidades; sensible a escala.

---

## 8. Para profundizar

**Papers fundacionales:**
- **Rosenblatt, F. (1958).** "The Perceptron: A Probabilistic Model for Information Storage and Organization in the Brain." *Psychological Review*, 65(6), 386–408. DOI: [10.1037/h0042519](https://doi.org/10.1037/h0042519). El paper original.
- **Novikoff, A. B. J. (1962).** "On Convergence Proofs for Perceptrons." *Proc. Symp. Math. Theory of Automata*, 615–622. PDF: [cs.uwaterloo.ca/~y328yu/classics/novikoff.pdf](https://cs.uwaterloo.ca/~y328yu/classics/novikoff.pdf).
- **Minsky, M. & Papert, S. (1969).** *Perceptrons.* MIT Press. Demuestra los límites del perceptrón monocapa.
- **Rumelhart, Hinton & Williams (1986).** "Learning representations by back-propagating errors." *Nature* 323, 533–536. El paper que destrabó las redes neuronales después del invierno post-Minsky.

**Libros:**
- **Bishop (2006)** *PRML*, **§4.1.7** — perceptrón con notación moderna y prueba de convergencia.
- **Hastie, Tibshirani, Friedman (2009)** *ESL*, **§4.5** — clasificadores lineales separadores; **§12** generaliza con SVM. Gratis: [hastie.su.domains/ElemStatLearn](https://hastie.su.domains/ElemStatLearn/).
- **Murphy (2022)** *PML*, **§10** — clasificación lineal (perceptrón, logística, SVM).
- **Gallant, S. I. (1990).** "Perceptron-based learning algorithms." *IEEE TNN*, 1(2). PDF: [ftp.cs.nyu.edu/~roweis/csc2515-2006/readings/gallant.pdf](https://ftp.cs.nyu.edu/~roweis/csc2515-2006/readings/gallant.pdf). Variante Pocket. (Cita explícita del notebook 02.)
- **Goodfellow, Bengio, Courville (2016)** *Deep Learning*, **cap. 6** — perceptrón → MLP → backprop. Gratis: [deeplearningbook.org](https://www.deeplearningbook.org/).

**scikit-learn:**
- [`Perceptron`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Perceptron.html) — wrapper sobre SGDClassifier.
- [`make_classification`](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.make_classification.html) — generador del notebook 02.
- [User Guide §1.1.13](https://scikit-learn.org/stable/modules/linear_model.html#perceptron).

---

## Próximo paso

El perceptrón es discreto y duro: $\text{sign}$ aplasta el score a $\pm 1$. Tres problemas serios:
1. **No da probabilidades.**
2. **No converge si no es separable.**
3. **No es diferenciable** (no encaja en pipelines más grandes con gradientes).

La **regresión logística** resuelve los tres a la vez: reemplaza $\text{sign}$ por la sigmoide $\sigma$, lo que da probabilidades, una loss convexa, y entrenamiento estable con gradient descent.

→ [07-regresion-logistica.md](07-regresion-logistica.md)

---

## Referencias

**Material primario:** DiploDatos UNC FAMAF 2026 — IAA Clase 1 Bloque C (PDF p. 28–39) + Notebook 02.

**Bibliografía citada:**
- Rosenblatt, F. (1958). *Psychological Review*, 65(6), 386–408. https://doi.org/10.1037/h0042519
- Novikoff, A. B. J. (1962). *Proc. Symp. Math. Theory of Automata*, 615–622.
- Minsky, M. & Papert, S. (1969). *Perceptrons.* MIT Press.
- Bishop, C. M. (2006). *PRML*, §4.1.7. Springer.
- Hastie, Tibshirani, Friedman (2009). *ESL*, §4.5. Springer.
- Murphy, K. P. (2022). *PML*, §10. MIT Press.
- Gallant, S. I. (1990). *IEEE TNN*, 1(2), 179–191.
- Rumelhart, Hinton, Williams (1986). *Nature*, 323, 533–536.

**Documentación:** [`sklearn.linear_model.Perceptron`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Perceptron.html), [`make_classification`](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.make_classification.html), [Perceptron (Wikipedia)](https://en.wikipedia.org/wiki/Perceptron), [Perceptrons (libro)](https://en.wikipedia.org/wiki/Perceptrons_(book)).
