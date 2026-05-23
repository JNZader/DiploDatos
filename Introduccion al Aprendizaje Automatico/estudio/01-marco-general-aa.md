# 01 — Marco general del Aprendizaje Automático

> **Mapa del capítulo.** Este es el *manifiesto conceptual* sobre el que se monta todo lo que sigue. Antes de poder hablar de regresión, clasificación, gradientes o regularización, hace falta entender DOS cosas: (1) qué tipo de problema es el ML (y por qué es distinto a "programar"), y (2) qué familias de aprendizaje existen y qué supuestos hace cada una. Lo que sigue es la cátedra DiploDatos UNC 2026 (Clase 1, PDF p. 1–14) cruzada con las fuentes canónicas (Bishop, Murphy, Karpathy).

## 1. Concepto

**Aprendizaje automático (Machine Learning)** es la disciplina que estudia algoritmos capaces de **mejorar su desempeño en una tarea T a partir de la experiencia E**, medida por una métrica de desempeño P (Mitchell, 1997 — definición clásica).

Versión cátedra (PDF Clase 1, p. 6): *"Aprender es encontrar la 'función óptima' dentro de un espacio de hipótesis infinito mediante estrategias de optimización."*

Versión Bishop (PRML, §1, 2006): *"the field [...] of automatically discovering regularities in data through the use of computer algorithms and with the use of these regularities to take actions such as classifying the data into different categories."*

Versión Murphy (PML, §1.1, 2022): el ML es un caso particular de **modelado probabilístico** — todo modelo es una hipótesis sobre la distribución que generó los datos, y aprender es seleccionar parámetros que maximizan la verosimilitud (o minimizan una función de costo).

> **Tres definiciones, una idea común:** elegir, dentro de un conjunto enorme de funciones candidatas, aquella que mejor reproduce la relación observada entre entradas y salidas — con la esperanza de que generalice a entradas nuevas.

## 2. Intuición

La cátedra arranca con la pregunta rectora (PDF p. 3):

> **"¿Cuál es la diferencia entre programar una computadora y entrenarla?"**

Karpathy (2017) responde con la metáfora más memorable del campo: **Software 2.0**.

- **Software 1.0** — el programador escribe REGLAS explícitas. El compilador las traduce a binario. Cuando algo nuevo aparece, hay que escribir más reglas.
- **Software 2.0** — el programador escribe un **dataset** + una **arquitectura** (red neuronal, árbol, polinomio, etc). El optimizador **compila** ese dataset en un binario (los pesos $\mathbf{w}$). Cuando algo nuevo aparece, agregás ejemplos.

Karpathy lo dice así: *"In Software 2.0 most often the source code comprises 1) the dataset that defines the desirable behavior and 2) the neural net architecture that gives the rough skeleton of the code, but with many details (the weights) to be filled in. The process of training the neural network compiles the dataset into the binary — the final neural network."* (Karpathy, *Software 2.0*, Medium 2017).

**Analogía didáctica complementaria (Bishop, §1):** un chico aprende a reconocer perros. Nadie le da una regla formal del tipo "patas + cola + ladrido → perro" — le señalan ejemplos: "esto es un perro, esto también, esto es un gato". Después de N ejemplos, el chico generaliza. ESO es ML.

> **Frase clave cátedra (PDF p. 4):** *"El programador es el experto. Codifica la lógica explícitamente y el sistema solo la ejecuta"* (Software 1.0) vs *"El sistema aprende los patrones. Entregamos ejemplos y el algoritmo infiere la función"* (Software 2.0).

## 3. Cuerpo técnico

### 3.1 — Software 1.0 vs Software 2.0 (formalización)

| Eje | Software 1.0 | Software 2.0 |
|-----|-------------|--------------|
| **Input al desarrollador** | Especificación + datos | Dataset etiquetado |
| **Output del desarrollador** | Código (reglas) | Modelo (pesos) |
| **Quién escribe la lógica** | Humano | Optimizador |
| **Cómo se "compila"** | Compilador / intérprete | Algoritmo de entrenamiento (SGD, etc.) |
| **Cómo se itera** | Editar código | Agregar/limpiar datos, ajustar arquitectura |
| **Debugging** | Stack trace, logs | Curva de pérdida, matriz de confusión, inspección de pesos |
| **Generaliza a casos no vistos** | Sólo si las reglas lo contemplan | Sí, si los datos son representativos |

### 3.2 — El espacio de hipótesis

Una **hipótesis** es una función candidata $h: \mathcal{X} \to \mathcal{Y}$ del input al output. El **espacio de hipótesis $\mathcal{H}$** es el conjunto de TODAS las funciones que el algoritmo puede aprender.

Ejemplos:
- Regresión lineal univariada: $\mathcal{H} = \{y = w_0 + w_1 x : w_0, w_1 \in \mathbb{R}\}$ — espacio 2-dimensional (los dos pesos).
- Regresión polinomial de grado M: $\mathcal{H} = \{y = \sum_{j=0}^{M} w_j x^j\}$ — espacio (M+1)-dimensional.
- Perceptrón en $\mathbb{R}^n$: $\mathcal{H} = \{h(\mathbf{x}) = \text{sign}(\mathbf{w}^T\mathbf{x} + b)\}$ — espacio (n+1)-dimensional.
- Red neuronal con D parámetros: $\mathcal{H}$ es un espacio D-dimensional (D = billones para GPT-4).

> **Frase cátedra (PDF p. 6):** *"Este fundamento de búsqueda y optimización es universal: desde modelos clásicos como XGBoost hasta LLMs modernos como GPT-4. Solo cambia la escala del espacio de hipótesis explorado."*

**Aprender = optimizar en $\mathcal{H}$.** Toda la maquinaria que sigue (mínimos cuadrados, gradiente descendente, MLE, MAP) son distintos algoritmos para BUSCAR la mejor hipótesis dentro de $\mathcal{H}$.

**Sesgo inductivo** (concepto NO explícito en la cátedra pero relevante — Bishop §1, Murphy §1.4): la elección de $\mathcal{H}$ es UNA hipótesis previa sobre cómo es el mundo. Elegir $\mathcal{H} = $ rectas implica creer que la relación es lineal. Elegir $\mathcal{H} = $ polinomios de grado 9 implica creer que puede ser muy compleja. NO HAY MODELO sin sesgo inductivo — el "no free lunch theorem" (Wolpert, 1996) dice que ningún algoritmo es uniformemente mejor en todos los problemas.

### 3.3 — Los 5 tipos de aprendizaje (PDF Clase 1, p. 7)

Cada paradigma se adapta a una **disponibilidad diferente de datos etiquetados** y a un objetivo distinto.

#### 3.3.1 — Supervisado

**Datos:** pares $(x_i, y_i)_{i=1}^N$ con etiqueta conocida. **Objetivo:** aprender $f: \mathcal{X} \to \mathcal{Y}$.

Sub-tipos:
- **Regresión:** $y$ continuo (ej.: precio de vivienda).
- **Clasificación:** $y$ categórico (ej.: spam / no spam).

(Bishop §1.1, Murphy §1.2 — la mitad del libro va de acá.)

#### 3.3.2 — No supervisado

**Datos:** sólo $x_i$, SIN etiqueta. **Objetivo:** descubrir estructura.

Sub-tipos:
- **Clustering** (k-means, DBSCAN) — agrupar similares.
- **Reducción de dimensionalidad** (PCA, t-SNE, UMAP) — comprimir preservando estructura.
- **Estimación de densidad** (KDE, GMM) — modelar la distribución de los datos.

> **Frase cátedra (PDF p. 9):** *"Identificar y explotar la estructura interna de los datos sin ninguna 'salida esperada' predefinida."*

Murphy (§1.3) advierte: evaluar no-supervisado es ESTRUCTURALMENTE más difícil — no hay "ground truth" contra qué comparar. Métricas típicas: silueta, índice de Davies-Bouldin, log-likelihood en held-out.

#### 3.3.3 — Semi-supervisado

**Datos:** muchos $x_i$ sin etiqueta + pocos $(x_j, y_j)$ con etiqueta. **Objetivo:** aprovechar los no etiquetados para mejorar el supervisado.

Caso de uso típico: etiquetar datos es CARO (ej.: imágenes médicas que necesitan un radiólogo). Tenés 1M imágenes pero sólo 5000 etiquetadas — el semi-supervisado usa las 1M para aprender representaciones útiles y las 5000 para la tarea final.

#### 3.3.4 — Auto-supervisado

**Datos:** sólo $x_i$, PERO se construyen etiquetas automáticamente a partir del propio input (tareas de pretexto).

> **Frase cátedra (PDF p. 11):** *"El modelo aprende a predecir lo que falta. Sin etiquetas. Sin supervisión humana."*

Dos variantes canónicas (cátedra y bibliografía):
- **Autorregresión** — predecir el siguiente token dado el contexto. Base de **GPT** (Radford et al., 2018).
- **Enmascaramiento** — ocultar parte del input y reconstruirla. Base de **BERT** (Devlin et al., 2019).

Ejemplo gráfico de la cátedra: "Diplomatura en [Ciencia] de [Datos] y [Machine Learning]" — el modelo aprende a llenar los huecos.

#### 3.3.5 — Por refuerzo

**Datos:** trayectorias $(s_t, a_t, r_t, s_{t+1})$ — un agente interactúa con un ambiente, recibe recompensas $r$, ajusta su política.

Ejemplo cátedra (PDF p. 13) — **Ta-Te-Ti**:

| Componente | Definición |
|------------|-----------|
| **Agente** | El algoritmo que decide dónde marcar |
| **Ambiente** | El tablero |
| **Acción** | Colocar X u O en celda libre |
| **Recompensa** | +1 ganar, -1 perder, 0 empate |

Algoritmos clásicos: Q-learning (Watkins, 1989), DQN (Mnih et al., 2015), PPO (Schulman et al., 2017).

### 3.4 — Pre-entrenamiento + Fine-tuning (PDF Clase 1, p. 12)

La cátedra dedica una slide entera al paradigma que dominó ML en los últimos 6 años:

**FASE 1 — Pre-entrenamiento ("La Base"):**
- Datos: volúmenes masivos SIN etiquetas (Common Crawl, libros, código).
- Tarea: auto-supervisada (autorregresión / enmascaramiento).
- Resultado: un modelo que aprendió la estructura general del dominio.
- Escala: billones de parámetros, semanas/meses de cómputo en miles de GPUs.

**FASE 2 — Fine-tuning ("La Especialización"):**
- Datos: pocos miles de ejemplos etiquetados de la tarea objetivo.
- Tarea: supervisada (diagnóstico médico, clasificación legal, asistente conversacional).
- Resultado: un modelo experto en una tarea concreta.
- Escala: horas de cómputo en una sola GPU.

**Ejemplos canónicos:**
- **BERT** (Devlin et al., 2019) — pre-entrenado con masked language modeling sobre Wikipedia + BookCorpus. Fine-tuned para clasificación de sentimiento, NER, QA, etc.
- **GPT-3/4** (Brown et al., 2020; OpenAI 2023) — pre-entrenado con autorregresión sobre la web. Fine-tuned para instrucciones (RLHF) → ChatGPT.
- **CLIP** (Radford et al., 2021) — pre-entrenado contrastivamente con pares imagen-texto. Fine-tuned para clasificación zero-shot.

Karpathy lo enmarca como la culminación de Software 2.0: el "compilador" (entrenamiento) genera modelos cuyo conocimiento se transfiere a tareas nuevas con muy poca señal.

### 3.5 — Proceso de entrenamiento (PDF Clase 1, p. 14) — preview

La cátedra cierra el bloque conceptual con el diagrama de flujo del ciclo de entrenamiento. Acá sólo lo introducimos — el desarrollo completo va en el capítulo 02:

```
DATASET ─┬─> TRAIN ──┐
         ├─> VAL ────┼─> CICLO DE OPTIMIZACIÓN ──> w*
         └─> TEST ───┘   (hiperparámetros)
                              │
                              ├─> FUNCIÓN DE COSTO ──> PREDICCIONES
                              └─> MONITOREO + CURVA DE PÉRDIDA
```

Tres ideas que vamos a desplegar en [02-pipeline-de-entrenamiento.md](02-pipeline-de-entrenamiento.md):
1. **Particionar los datos** (train / val / test) — la razón es estadística (Goodfellow §5.3).
2. **Iterar minimizando la función de costo** — el "ciclo" central.
3. **Monitorear con la curva de pérdida** — ver overfitting/underfitting EN TIEMPO REAL.

## 4. Ejemplo numérico

Veamos cómo el MISMO problema cambia según el paradigma elegido.

**Dataset toy:** 5 pacientes con edad y nivel de glucosa.

| id | edad | glucosa | diabetes |
|----|------|---------|----------|
| 1  | 25   | 90      | 0        |
| 2  | 60   | 180     | 1        |
| 3  | 45   | 140     | 1        |
| 4  | 30   | 95      | 0        |
| 5  | 55   | 150     | 1        |

**Como problema supervisado de clasificación binaria:**
- Input: $\mathbf{x} = (\text{edad}, \text{glucosa})$.
- Output: $y \in \{0, 1\}$ (diabetes sí/no).
- Hipótesis: $h(\mathbf{x}) = \text{sign}(w_1 \cdot \text{edad} + w_2 \cdot \text{glucosa} + b)$.
- Espacio: $\mathcal{H} = \mathbb{R}^3$ (dos pesos + bias).
- Algoritmo: perceptrón, logistic regression, SVM.

**Como problema supervisado de regresión:**
- Si en vez de etiqueta binaria tuviéramos un puntaje continuo de riesgo (0–100), el MISMO dataset se modela con regresión.

**Como problema no supervisado:**
- Si BORRARAMOS la columna "diabetes", podríamos hacer clustering (k-means con k=2) y ver si emergen dos grupos. Probablemente sí — los puntos 1,4 (jóvenes, glucosa normal) vs 2,3,5 (mayores, glucosa alta).

**Como problema auto-supervisado:**
- Ocultaríamos la columna glucosa y entrenaríamos un modelo a predecir glucosa desde el resto. Después usaríamos las representaciones aprendidas para la tarea final con pocos ejemplos.

**Como problema de refuerzo:**
- Cuesta forzar la analogía con un dataset estático — RL típicamente requiere un AMBIENTE interactivo. Pero podríamos pensar un agente médico que decide "pedir más estudios / dar de alta" y recibe recompensa diferida según outcome del paciente.

> **Moraleja:** el mismo dato puede entrar en distintos paradigmas según qué información asumas disponible y qué objetivo persigas. La elección NO es trivial — define todo lo que sigue.

## 5. Conexión con el TP

**TP1 — Laboratorio 1: Regresión en California.** El TP1 es íntegramente **aprendizaje supervisado de regresión**. Concretamente:

- **Ej. 1 (cell-12):** la primera pregunta del TP es *"¿De qué se trata el conjunto de datos?"*. Esa pregunta es exactamente el ejercicio de mapear el problema al paradigma correcto. Respuesta esperada: regresión supervisada, target continuo (mediana de precio de vivienda en bloques censales de California).
- **Ej. 1, pregunta 5:** *"¿Qué problemas / sesgos / dilemas éticos observa?"*. Acá entra la discusión que Karpathy menciona explícitamente en *Software 2.0*: el dataset ES el código. Si el dataset codifica sesgos históricos (redlining en California — ver Pace & Barry, 1997), el modelo los reproduce. La pregunta NO es académica: el California Housing dataset tiene historia documentada de sesgos por raza/ingreso heredados del censo de 1990.

**Lo que el TP1 NO toca (por ahora):** no usa aprendizaje no supervisado ni clustering, no toca perceptrón/logística (eso es TP2/Clase 2), no usa pre-entrenamiento ni fine-tuning. Es un TP de bases sólidas.

> Por eso este capítulo 01 NO te enseña a hacer el TP — te enseña a **describir QUÉ ESTÁS HACIENDO** cuando lo hacés. El Ej. 1 evalúa precisamente eso.

## 6. Errores comunes

1. **Confundir "ML" con "DL" (deep learning)** — DL es UN sub-caso de ML (modelos con representaciones aprendidas jerárquicamente). Toda la cátedra de IAA es ML clásico, no DL.
2. **Confundir aprendizaje no supervisado con "no tener targets de entrenamiento"** — en auto-supervisado tampoco hay targets EXTERNOS, pero NO es no-supervisado. La diferencia: el auto-supervisado FABRICA su propio target a partir del input.
3. **Pensar que "más datos = mejor"** sin matiz — más datos ayudan SIEMPRE que sean representativos de la distribución que vas a predecir. Si tu dataset tiene sesgo, más datos del mismo lado lo amplifican.
4. **Asumir IID donde no lo hay** — la teoría supone train y test muestreados i.i.d. de la misma distribución. En datos temporales (series financieras, sensores), eso se rompe → necesitás validación temporal, no aleatoria.
5. **Confundir entrenar con compilar** — Karpathy es explícito: el "compilador" del Software 2.0 es el optimizador. Si lo confundís, te perdés todo el sentido de la analogía.
6. **Creer que el espacio de hipótesis es libre** — es la primera DECISIÓN de modelado y carga TODO el sesgo inductivo. Cambiar de $\mathcal{H} =$ rectas a $\mathcal{H} =$ polinomios de grado 9 NO es un detalle.
7. **Confundir multietiqueta con multiclase** — multiclase: una etiqueta entre K. Multietiqueta: subconjunto de K etiquetas. Distinto problema, distinta función de pérdida, distinta métrica (Clase 2 lo desarrolla).
8. **Usar el test set como validación** — si lo hacés, perdés la única señal honesta que tenés sobre generalización. Esto se desarrolla en el cap 02.
9. **Olvidar que "aprender los pesos" ≠ "aprender la estructura"** — un perceptrón aprende UN hiperplano. Si el problema no es linealmente separable, NO HAY pesos que resuelvan el problema. La elección de $\mathcal{H}$ pesa más que el algoritmo de optimización.

## 7. Checklist de comprensión

- [ ] Puedo explicar la diferencia entre Software 1.0 y 2.0 SIN usar la palabra "neural".
- [ ] Sé citar la definición de Mitchell (T, P, E) y mapearla a un ejemplo concreto.
- [ ] Puedo distinguir supervisado, no supervisado, semi-supervisado, auto-supervisado y por refuerzo, dando un ejemplo concreto de cada uno.
- [ ] Sé qué es el espacio de hipótesis y por qué su elección es la primera fuente de sesgo inductivo.
- [ ] Puedo explicar pre-entrenamiento + fine-tuning con un ejemplo (BERT o GPT).
- [ ] Sé identificar qué tipo de problema es el TP1 y citar el dataset.
- [ ] Puedo argumentar por qué evaluar no-supervisado es estructuralmente más difícil.
- [ ] Conozco el ejemplo del Ta-Te-Ti de la cátedra para refuerzo y sé identificar los 4 componentes.
- [ ] Puedo dar dos ejemplos modernos de auto-supervisado (BERT/enmascaramiento y GPT/autorregresión).
- [ ] Sé que "no free lunch" implica que ningún algoritmo es universalmente mejor.

## 8. Para profundizar

- **Karpathy, A. (2017). *Software 2.0*.** Lectura obligatoria — 15 minutos, te cambia la cabeza. <https://karpathy.medium.com/software-2-0-a64152b37c35>
- **Bishop §1.** Introducción con el ejemplo de regresión polinomial como hilo conductor. Muy didáctico, NO requiere fondo matemático fuerte para esta primera parte.
- **Murphy §1 (PML 2022).** Visión más probabilística — empieza con MNIST como ejemplo y formaliza supervisado/no-supervisado en términos de distribuciones.
- **Goodfellow, Bengio, Courville §5 (Deep Learning, 2016).** Cap 5 "Machine Learning Basics" — aunque el libro es de DL, este capítulo es el mejor compendio gratis del ML clásico que es la base de DL. <https://www.deeplearningbook.org/contents/ml.html>
- **Mitchell, T. (1997). *Machine Learning*, McGraw-Hill.** El libro clásico. Definición canónica de T/P/E.
- **Wolpert, D. (1996). "The Lack of A Priori Distinctions Between Learning Algorithms".** El paper del "no free lunch theorem". Lectura técnica, pero el TL;DR vale: sin supuestos sobre la distribución, todos los algoritmos son equivalentes en promedio.
- **Devlin et al. (2019). *BERT: Pre-training of Deep Bidirectional Transformers*.** Para entender enmascaramiento.
- **Radford et al. (2018, 2019, 2020). serie GPT.** Para entender autorregresión a escala.

## Próximo paso

→ [02-pipeline-de-entrenamiento.md](02-pipeline-de-entrenamiento.md)

## Referencias

- Karpathy, A. (2017). *Software 2.0*. Medium. <https://karpathy.medium.com/software-2-0-a64152b37c35>
- Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*. Springer. §1.
- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press. §1.
- Goodfellow, I., Bengio, Y., & Courville, A. (2016). *Deep Learning*. MIT Press. Cap 5. <https://www.deeplearningbook.org/contents/ml.html>
- Mitchell, T. M. (1997). *Machine Learning*. McGraw-Hill.
- Wolpert, D. H. (1996). The Lack of A Priori Distinctions Between Learning Algorithms. *Neural Computation* 8(7).
- Devlin, J. et al. (2019). *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding*. NAACL.
- Brown, T. et al. (2020). *Language Models are Few-Shot Learners* (GPT-3). NeurIPS.
- Pace, R. K. & Barry, R. (1997). Sparse spatial autoregressions. *Statistics & Probability Letters*, 33(3), 291–297. (Paper original del California Housing.)
- Material de cátedra: Clase 1 PDF, DiploDatos UNC 2026 — Introducción al Aprendizaje Automático (Meinardi & Bonzi).
