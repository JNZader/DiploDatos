# 14 — Bibliografía y recursos externos

> **Guía de USO** (no listado pasivo). Para cada referencia detallo: **qué cubre**, **para qué capítulo del estudio sirve**, **nivel** (intro / intermedio / avanzado), y si está **disponible online gratis**. Las URLs fueron verificadas en mayo de 2026.
>
> **Cómo leer esta guía:** los libros están ordenados de **más accesible** a **más exigente**. Las referencias marcadas con `[⭐]` son las que **más se alinean con el estilo y notación de la cátedra DiploDatos**.

---

## A — Libros de texto (referencia principal)

### A.1 — Bishop, *Pattern Recognition and Machine Learning* (PRML), Springer 2006 `[⭐]`

**Autor:** Christopher M. Bishop (Microsoft Research). **Año:** 2006. **Editorial:** Springer (Information Science and Statistics series).

**Qué cubre:** referencia clásica de ML probabilístico. Cubre regresión lineal, regresión bayesiana, regresión logística, redes neuronales, gráficos probabilísticos, modelos de mezcla, métodos no paramétricos, kernels, SVM y aprendizaje no supervisado. Notación rigurosa, derivaciones completas.

**Para qué capítulos del estudio:**
- Cap. 02-03 (Regresión polinomial y regularización): **Capítulo 1 — Introduction**, ejemplo del polinomio sinusoidal — **es literalmente el mismo ejemplo que usa la cátedra**, incluyendo el efecto de `M`, la tabla de coeficientes que crecen con `M`, y la regularización Ridge. Casi todo el material del PDF Clase 1 está calcado de Bishop §1.1.
- Cap. 05 (Perceptrón): **Capítulo 4 — Linear Models for Classification**, §4.1.7 — derivación clásica.
- Cap. 06-07 (Logística): **Capítulo 4 §4.3** — Logistic Regression, IRLS.
- Cap. 08 (Naive Bayes): **Capítulo 4 §4.2** — Probabilistic Generative Models.
- Cap. 09 (KNN): **Capítulo 2 §2.5.2** — Nearest-Neighbour Methods.

**Nivel:** intermedio-avanzado. Asume álgebra lineal sólida y cálculo multivariable. Las primeras 90 páginas (Capítulo 1) son accesibles y **muy recomendadas para arrancar**.

**Disponibilidad:** PDF oficial publicado por Microsoft Research en su sitio (Bishop es Distinguished Scientist allí). Sample chapter gratis en `microsoft.com/en-us/research/`. El libro completo está disponible en formato PDF en archivos institucionales y en Internet Archive.

**Cuándo abrirlo:** cuando una explicación de la cátedra te quede corta y necesites el desarrollo matemático completo. Es el **libro de referencia principal** del curso, aunque la cátedra no lo cite explícitamente.

### A.2 — Murphy, *Probabilistic Machine Learning: An Introduction* (PML book 1), MIT Press 2022 `[⭐]`

**Autor:** Kevin P. Murphy (Google DeepMind). **Año:** 2022. **Editorial:** MIT Press.

**Qué cubre:** sucesor moderno de Bishop. Cubre todo lo de Bishop + deep learning, atención, generative models, fairness, causalidad. Notación uniforme, código Python en colab para cada capítulo.

**Para qué capítulos del estudio:**
- Cap. 00-01 (Marco): **Capítulo 1 — Introduction** — taxonomía moderna de ML.
- Cap. 02-03 (Regresión): **Capítulo 4 — Statistics**, **Capítulo 11 — Linear Regression**.
- Cap. 06-07 (Logística + softmax): **Capítulo 10 — Logistic Regression**.
- Cap. 08 (NB): **Capítulo 9 — Linear Discriminant Analysis**, §9.3 Naive Bayes.
- Cap. 09 (KNN): **Capítulo 16 — Exemplar-based methods**.

**Nivel:** intermedio. Más actualizado que Bishop (vocabulario moderno: cross-entropy, softmax, etc.).

**Disponibilidad:** **PDF gratis** en `probml.github.io/pml-book/book1.html` (autorizado por MIT Press, draft completo accesible). Código en `github.com/probml/pyprobml`. Repositorio de figuras en `figures.probml.ai/x.y` para cada figura del libro.

**Cuándo abrirlo:** cuando querés vocabulario moderno + código directo en Python. Útil como **complemento** a Bishop: Bishop te explica el **porqué matemático**, Murphy te muestra el **código y la conexión con tecnología actual**.

### A.3 — Hastie, Tibshirani & Friedman, *The Elements of Statistical Learning* (ESL), Springer 2009 `[⭐]`

**Autores:** Trevor Hastie, Robert Tibshirani, Jerome Friedman (Stanford). **Año:** 2009 (2da ed.), 12va imprenta 2017.

**Qué cubre:** la referencia clásica de **statistical learning**. Cubre regresión (lineal, ridge, lasso), clasificación (LDA, logística, NB, KNN), métodos de árbol, boosting, redes neuronales, SVM, métodos no supervisados.

**Para qué capítulos del estudio:**
- Cap. 02-03 (Regresión + regularización): **Capítulo 3 — Linear Methods for Regression** — donde se introducen Ridge y Lasso con todos los detalles geométricos. **Lectura obligada** si querés entender Lasso en profundidad.
- Cap. 04 (Perceptrón): **Capítulo 4 — Linear Methods for Classification**, §4.5 Separating Hyperplanes — perceptrón con análisis de convergencia.
- Cap. 06 (Logística): **Capítulo 4 §4.4**.
- Cap. 08 (NB): **Capítulo 6 §6.6.3**.
- Cap. 09 (KNN): **Capítulo 13 — Prototype Methods and Nearest-Neighbors**.

**Nivel:** avanzado. Notación más densa que Bishop, pero **muy rigurosa**. Asume cómodo manejo de estadística + álgebra lineal.

**Disponibilidad:** **PDF gratis y autorizado por los autores** en `hastie.su.domains/ElemStatLearn/` (Springer permitió publicarlo abierto). 12va imprenta de 2017 incluye correcciones.

**Cuándo abrirlo:** para profundizar en regularización (Ridge vs Lasso vs ElasticNet, §3.4) o en bias-variance decomposition (§7.3). Es el libro de referencia para **estadística aplicada**.

### A.4 — Goodfellow, Bengio & Courville, *Deep Learning*, MIT Press 2016

**Autores:** Ian Goodfellow, Yoshua Bengio, Aaron Courville. **Año:** 2016.

**Qué cubre:** referencia oficial de deep learning. El **Capítulo 5 — Machine Learning Basics** es un excelente resumen autocontenido de los fundamentos: estimación, MLE, sesgo, varianza, regularización, hiperparámetros.

**Para qué capítulos del estudio:**
- Cap. 00-03 + 06: **Capítulo 5** sirve como **resumen general del módulo**. Lo recomiendo como repaso después de terminar las clases 1-2.
- Cap. 04 (Perceptrón): **Capítulo 6 — Deep Feedforward Networks** — donde el perceptrón aparece como **caso degenerado** (1 capa).

**Nivel:** intermedio-avanzado. El Cap. 5 es muy bueno como nivel intermedio.

**Disponibilidad:** **gratis online** en `deeplearningbook.org` (autorizado por los autores).

**Cuándo abrirlo:** cuando querés conectar el perceptrón con redes profundas (la cátedra dice "el átomo de las redes neuronales modernas" — Goodfellow desarrolla esa idea en detalle).

---

## B — Referencias prácticas (código y herramientas)

### B.1 — scikit-learn User Guide `[⭐]`

**Autores:** scikit-learn developers. **Versión actual:** 1.8 (2026).

**Qué cubre:** documentación oficial de la biblioteca usada en todos los notebooks del curso. Cada algoritmo del módulo tiene su sección con teoría breve + ejemplos.

**Para qué capítulos del estudio:**
- Cap. 02-03 (Regresión): `linear_model.LinearRegression`, `linear_model.Ridge`, `preprocessing.PolynomialFeatures`, `pipeline.make_pipeline`.
- Cap. 04 (Perceptrón): `linear_model.Perceptron`.
- Cap. 06-07 (Logística): `linear_model.LogisticRegression`.
- Cap. 08 (NB): `naive_bayes.MultinomialNB`, `naive_bayes.GaussianNB`, `naive_bayes.BernoulliNB`, `feature_extraction.text.CountVectorizer`.
- Cap. 09 (KNN): `neighbors.KNeighborsClassifier`, `neighbors.KNeighborsRegressor`.
- Cap. 10 (Multiclase): `multiclass.OneVsRestClassifier`, `multiclass.OneVsOneClassifier`, `metrics.confusion_matrix`, `metrics.accuracy_score`.

**Nivel:** intro-intermedio. Pragmático, con ejemplos minimales.

**Disponibilidad:** `scikit-learn.org/stable/user_guide.html`. Modules:
- Supervised learning: `scikit-learn.org/stable/supervised_learning.html`
- Naive Bayes: `scikit-learn.org/stable/modules/naive_bayes.html`
- Working with text data: `scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html`

**Cuándo abrirlo:** **siempre que abras un notebook**. Es la referencia de uso diario.

### B.2 — VanderPlas, *Python Data Science Handbook* (2da ed.) `[⭐]`

**Autor:** Jake VanderPlas. **Editorial:** O'Reilly. **Año:** 2da edición.

**Qué cubre:** introducción a numpy, pandas, matplotlib, scikit-learn. Cubre exactamente las bibliotecas que se usan en el curso.

**Para qué capítulos del estudio:**
- **Pre-requisito numpy/pandas:** si te cuesta `np.linalg.pinv`, `np.stack`, indexación booleana, o slicing de DataFrames vs ndarrays (la trampa del TP1), VanderPlas es el lugar para arrancar.
- Cap. 02-09 (sklearn): Capítulo 5 cubre todos los modelos del módulo con ejemplos.
- TP1: Capítulo 5 §5.6 — Linear Regression, §5.13 — KMeans, §5.14 — GMM, etc.

**Nivel:** intro. **Perfecto para arrancar** si venís sin background fuerte en Python científico.

**Disponibilidad:** **gratis online** en `jakevdp.github.io/PythonDataScienceHandbook/` (texto bajo CC-BY-NC-ND, código bajo MIT). Versión ejecutable en Google Colab y Binder.

**Cuándo abrirlo:** **antes** de tocar los notebooks de la cátedra, si te cuesta numpy/pandas. **Es el libro técnico más útil del listado para los TPs.**

---

## C — Cursos abiertos (videos y materiales)

### C.1 — Andrew Ng, *CS229: Machine Learning*, Stanford `[⭐]`

**Profesor:** Andrew Ng + Tengyu Ma (versiones recientes).

**Qué cubre:** curso clásico de ML en Stanford. Cubre regresión lineal y logística, generative models, SVM, redes neuronales, regularización, kernel methods, modelos no supervisados, refuerzo.

**Para qué capítulos del estudio:**
- Cap. 02 (Regresión lineal): Lecture 1-2 — derivación con ecuación normal.
- Cap. 06 (Logística): Lecture 3 — donde se introduce la notación `h_θ(x) = g(θ^T x)` que la cátedra DiploDatos también usa.
- Cap. 08 (NB): Lecture 5 — Naive Bayes en filtros de spam.
- Cap. 09 (KNN): mencionado brevemente.

**Nivel:** intermedio. Los **lecture notes** son **extremadamente claros** (200+ páginas, escritas por Ng y mantenidas por Ma).

**Disponibilidad:**
- Sitio oficial: `cs229.stanford.edu/`
- Lecture notes (Ng + Ma, junio 2023): `cs229.stanford.edu/main_notes.pdf`
- Videos: Stanford Online (la versión 2018 con Ng está en YouTube).

**Cuándo abrirlo:** cuando una clase de la cátedra te quede corta. La **notación `θ` y `h_θ(x)`** del PDF DiploDatos viene directamente de Ng — es **el curso espiritualmente más cercano** a las clases 1-2.

### C.2 — fast.ai, *Practical Deep Learning for Coders*

**Profesores:** Jeremy Howard, Rachel Thomas.

**Qué cubre:** deep learning **práctico** desde la primera lección (no fundamentos teóricos primero). Top-down: usás modelos antes de entender la matemática.

**Para qué capítulos del estudio:** complemento. Sirve si después del módulo querés ir directo a deep learning sin pasar por meses de matemática teórica.

**Nivel:** intro-intermedio (asume Python sólido).

**Disponibilidad:** gratis en `course.fast.ai`. Videos + notebooks + libro acompañante.

**Cuándo abrirlo:** **después** del módulo, si te gustó la parte de notebooks y querés algo más práctico-aplicado.

### C.3 — StatQuest (Josh Starmer), YouTube

**Qué cubre:** videos cortos (10-30 min) explicando intuitivamente cada algoritmo de ML/estadística. Estilo "dibujado a mano".

**Para qué capítulos del estudio:**
- Cap. 02: "Linear Regression" (~30 min), "Polynomial Regression Clearly Explained".
- Cap. 03: "Ridge (L2) Regression", "Lasso (L1) Regression".
- Cap. 04: "Perceptron in Neural Networks" (intuición).
- Cap. 06: "Logistic Regression Details Pt 1: Coefficients".
- Cap. 08: "Naive Bayes, Clearly Explained!".
- Cap. 09: "K-Nearest Neighbors", "Confusion Matrices".

**Nivel:** intro. **Ideal para una primera pasada** o repaso visual rápido.

**Disponibilidad:** gratis en YouTube, canal "StatQuest with Josh Starmer".

**Cuándo abrirlo:** antes o después de leer la teoría, para tener una **intuición visual**. Especialmente útil si la matemática del PDF te frena.

### C.4 — MIT 6.036, *Introduction to Machine Learning*

**Qué cubre:** versión MIT del curso introductorio. Cubre clasificación lineal, perceptrón, regresión, redes neuronales, optimización por gradiente, modelos generativos.

**Nivel:** intermedio.

**Disponibilidad:** MIT OpenCourseWare hosts materiales del curso. Notas y problemas accesibles.

**Cuándo abrirlo:** alternativa más matemática a fast.ai si querés practicar con problem sets.

---

## D — Papers seminales (lectura histórica)

### D.1 — Rosenblatt (1958), *The Perceptron*

**Cita:** Rosenblatt, F. (1958). The perceptron: A probabilistic model for information storage and organization in the brain. *Psychological Review*, 65(6), 386-408.

**Por qué leerlo:** la cátedra cita explícitamente "Rosenblatt 1958" (PDF p. 34). Es **el paper fundacional** del perceptrón. Curiosidad histórica más que utilidad técnica — el algoritmo moderno está bien explicado en cualquier libro de texto.

**Para qué capítulo:** Cap. 04 (Perceptrón).

**Disponibilidad:** búsqueda en Google Scholar como "Rosenblatt 1958 perceptron".

### D.2 — Gallant (1990), *Perceptron-based learning algorithms*

**Cita:** Gallant, S. I. (1990). Perceptron-based learning algorithms. *IEEE Transactions on Neural Networks*, 1(2), 179-191.

**Por qué leerlo:** referenciado explícitamente en el notebook 02 (celda 61). Cubre variantes del perceptrón incluyendo el **pocket algorithm** (útil para datos no linealmente separables — uno de los ejercicios del notebook 02).

**Para qué capítulo:** Cap. 04 (Perceptrón), específicamente la sección de extensiones.

**Disponibilidad:** PDF en `ftp.cs.nyu.edu/~roweis/csc2515-2006/readings/gallant.pdf` (NYU mirror).

### D.3 — Cover & Hart (1967), *Nearest neighbor pattern classification*

**Cita:** Cover, T. M. & Hart, P. E. (1967). Nearest neighbor pattern classification. *IEEE Transactions on Information Theory*, 13(1), 21-27.

**Por qué leerlo:** paper fundacional de KNN. Demuestra el resultado clásico: **el error asintótico de KNN (k=1) es a lo sumo el doble del error de Bayes**.

**Para qué capítulo:** Cap. 09 (KNN).

**Disponibilidad:** búsqueda en Google Scholar.

### D.4 — Hoerl & Kennard (1970), *Ridge regression*

**Cita:** Hoerl, A. E. & Kennard, R. W. (1970). Ridge regression: Biased estimation for nonorthogonal problems. *Technometrics*, 12(1), 55-67.

**Por qué leerlo:** paper original de Ridge. Aporta intuición estadística y geométrica que rara vez se ve en cursos.

**Para qué capítulo:** Cap. 03 (Regularización).

**Disponibilidad:** búsqueda en Google Scholar.

### D.5 — Domingos & Pazzani (1997), *On the optimality of the simple Bayesian classifier under zero-one loss* `[⭐]`

**Cita:** Domingos, P. & Pazzani, M. (1997). On the optimality of the simple Bayesian classifier under zero-one loss. *Machine Learning*, 29(2), 103-130.

**Por qué leerlo:** **resuelve el "misterio" de Naive Bayes** que la cátedra plantea (PDF p. 18): ¿por qué funciona bien cuando viola tan flagrantemente el supuesto de independencia? Domingos & Pazzani demuestran que **NB es óptimo bajo zero-one loss en condiciones más amplias que las que requieren independencia** — la independencia no es necesaria para la **clasificación correcta**, solo para tener probabilidades calibradas.

**Para qué capítulo:** Cap. 08 (Naive Bayes).

**Disponibilidad:** **gratis** en `gwern.net/doc/ai/1997-domingos.pdf` (mirror) y `link.springer.com/article/10.1023/A:1007413511361` (oficial Springer, posiblemente paywall según institución).

**Cuándo abrirlo:** después de entender NB básico, cuando te preguntes "¿por qué carajo funciona si la independencia es falsa?".

---

## E — Documentación de referencia citada en los notebooks

Material **explícitamente referenciado** dentro de los notebooks (recomendados por la cátedra):

- **Perceptron** (Wikipedia): `en.wikipedia.org/wiki/Perceptron`.
- **Naive Bayes classifier** (Wikipedia): `en.wikipedia.org/wiki/Naive_Bayes_classifier`.
- **CountVectorizer** (sklearn): `scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html`.
- **train_test_split** (sklearn): `scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html`.
- **make_classification** (sklearn): `scikit-learn.org/stable/modules/generated/sklearn.datasets.make_classification.html`.
- **PolynomialFeatures** (sklearn): `scikit-learn.org/stable/modules/generated/sklearn.preprocessing.PolynomialFeatures.html`.
- **Perceptron** (sklearn): `scikit-learn.org/stable/modules/generated/sklearn.linear_model.Perceptron.html`.

---

## F — Recursos en español

### F.1 — Material UNC FAMAF

**Qué cubre:** apuntes propios de la cátedra DiploDatos UNC FAMAF. Slides y notebooks de las profesoras Vanesa Meinardi y Edgardo Bonzi. **Son el material principal del curso.**

**Disponibilidad:** Plataforma de la Diplomatura (acceso restringido a inscriptos). Los PDFs `1-Introduccion-al-Aprendizaje-Automatico.pdf` y `2-Modelos-Probabilisticos-y-No-Parametricos.pdf` + notebooks 01-04 son el corazón del módulo.

### F.2 — MOOCs en español (referencias generales)

- **Coursera — "Aprendizaje Automático"** (Andrew Ng, traducciones automáticas con subtítulos): versión en español del CS229 popular. Calidad de traducción variable.
- **edX — Diplomado en Inteligencia Artificial** (TEC Monterrey y otras instituciones): cursos completos en castellano, suelen ser pagos.

**Nivel:** intro-intermedio. **Calidad variable** según la traducción.

**Recomendación honesta:** la mayoría de los recursos de calidad están en inglés. Si tu inglés técnico es básico, conviene mejorar comprensión lectora antes que conformarse con material en castellano de calidad menor. Excepción: los **videos de StatQuest** tienen subtítulos en español muy decentes.

---

## G — Cómo combinar las referencias (workflow sugerido)

### Si recién arrancás (cero background en ML)

1. **VanderPlas (B.2)** caps. 4-5: numpy/pandas/matplotlib + intro a sklearn.
2. **StatQuest (C.3)**: ver 1 video por algoritmo antes de leer la teoría formal.
3. **Material de la cátedra (F.1)**: PDF + notebooks.
4. **scikit-learn user guide (B.1)**: para cada modelo, revisar la sección correspondiente mientras hacés el notebook.

### Si tenés base de estadística y querés profundizar

1. **Material de la cátedra (F.1)**.
2. **Bishop Cap. 1 (A.1)**: derivaciones completas de regresión + regularización. Es **directamente el contenido de la Clase 1** con todas las cuentas.
3. **Hastie ESL Cap. 3 (A.3)**: regularización (Ridge, Lasso) con todo el detalle.
4. **Bishop Cap. 4 + Ng CS229 Lecture 3 (A.1 + C.1)**: regresión logística.
5. **Domingos & Pazzani (D.5)**: el paper que resuelve el "misterio" de NB.

### Si querés conectar con deep learning después

1. **Material de la cátedra (F.1)**.
2. **Goodfellow Cap. 5 (A.4)**: resumen de fundamentos.
3. **Goodfellow Cap. 6**: perceptrón → redes feedforward.
4. **fast.ai (C.2)** o **Murphy Cap. 13+ (A.2)**: deep learning.

### Para los TPs

1. **VanderPlas Cap. 5 (B.2)**: ejemplos prácticos de regresión + clasificación con sklearn.
2. **scikit-learn user guide (B.1)**: API exacta de cada función.
3. **StatQuest (C.3)**: para refrescar la intuición de overfitting / regularización antes del Ej. 4 y Ej. 7.

---

## H — Resumen tabular

| Referencia | Tipo | Nivel | Online gratis | Mejor para |
|---|---|---|---|---|
| Bishop PRML 2006 | Libro | Int-Avan | Sí (MS Research) | Caps. 02-08 (referencia matemática) |
| Murphy PML 2022 | Libro | Int | Sí (probml.github.io) | Caps. 02-09 (moderno) |
| Hastie ESL 2009 | Libro | Avan | Sí (hastie.su.domains) | Cap. 03 (regularización) |
| Goodfellow DL 2016 | Libro | Int-Avan | Sí (deeplearningbook.org) | Cap. 04 + transición a DL |
| VanderPlas PDSH | Libro | Intro | Sí (jakevdp.github.io) | TPs y pre-requisitos |
| Ng CS229 | Curso | Int | Sí (cs229.stanford.edu) | Caps. 02, 06, 08 |
| fast.ai | Curso | Int | Sí (course.fast.ai) | Práctica post-módulo |
| StatQuest | Videos | Intro | Sí (YouTube) | Intuición visual |
| sklearn user guide | Docs | Intro-Int | Sí (scikit-learn.org) | Implementación |
| Domingos & Pazzani 1997 | Paper | Avan | Sí (gwern.net mirror) | Cap. 08 (NB profundo) |
| Material UNC (F.1) | Apuntes | Intro-Int | Acceso curso | **Material principal** |

---

## I — Advertencias finales

- **No leas Bishop entero antes de empezar.** Es trampa de perfeccionista. El Capítulo 1 (~80 páginas) es suficiente para el módulo.
- **No saltees el material de la cátedra** asumiendo que un libro lo reemplaza. La cátedra elige una notación, una secuencia y un nivel de detalle específicos — los libros la complementan, no la sustituyen.
- **Si una explicación no te cierra**, buscá el mismo concepto en 2-3 fuentes distintas (cátedra + Bishop + StatQuest, por ejemplo). El cerebro consolida mejor cuando ve el mismo concepto desde ángulos diferentes.
- **La regla "30% lectura, 70% código"** vale acá: una hora de notebook bien hecho te enseña más que tres horas de lectura pasiva.
- **Para citar las referencias en informes:** usá formato APA o IEEE consistente. El TP1 no exige formato específico, pero es buena práctica.

---

→ [15-guia-de-tp1.md](15-guia-de-tp1.md)
