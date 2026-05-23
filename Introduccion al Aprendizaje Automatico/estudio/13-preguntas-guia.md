# 13 — Preguntas-guía de auto-examen

> Preguntas pensadas para **auto-examen** sobre los Caps. 00-10 del estudio y el TP1. **NO incluyen respuestas** — la idea es que respondas vos y compares con el material (notebooks + apuntes + glosario).
>
> Hay **~95 preguntas** organizadas por capítulo. Cada capítulo cubre: definiciones precisas, diferenciaciones conceptuales, aplicación práctica, conceptos sutiles, trampas comunes. Las preguntas marcadas con `[⚠️]` son las que tienen mayor probabilidad de aparecer en un parcial.
>
> **Cómo usarlo:** leé el capítulo correspondiente, esperá unas horas, intentá responder de memoria, y solo después volvé al material a verificar. Si tu respuesta tiene la misma **estructura** que la cátedra (no necesariamente las mismas palabras), vas por buen camino.

---

## Cap. 00 — Marco general y motivación

1. ¿Cuál es la diferencia entre **programar** una computadora y **entrenarla**? Explicalo con el contraste Software 1.0 vs Software 2.0.
2. [⚠️] ¿Qué se entiende por **espacio de hipótesis** y por qué la cátedra dice que "aprender = encontrar la función óptima dentro de un espacio de hipótesis infinito"?
3. ¿Por qué la cátedra dice que la idea de "espacio de hipótesis + optimización" es **universal**, desde XGBoost hasta GPT-4?
4. Listá los **cinco tipos de aprendizaje** que diferencia el material (Cap. 00 / PDF p. 7) y dá un ejemplo de cada uno.
5. ¿Qué diferencia hay entre aprendizaje **semi-supervisado** y **auto-supervisado**? ¿Cuál es la base de GPT y cuál la de BERT?
6. Explicá el ciclo de **pre-entrenamiento + fine-tuning** con un ejemplo concreto y la escala de cómputo asociada a cada fase.
7. ¿Qué componentes definen un problema de aprendizaje por **refuerzo**? Usá el ejemplo del Ta-Te-Ti de la cátedra.
8. [⚠️] ¿Qué tres etapas separa la cátedra en el "proceso de entrenamiento de un modelo" (PDF p. 14)? ¿Para qué sirve cada subconjunto (train/val/test)?
9. ¿Por qué el hiperparámetro `M` (grado del polinomio) **NO** se aprende junto con los `w`? ¿Quién lo elige?
10. ¿Qué significa "el sistema aprende los patrones" en contraposición a "el programador codifica la lógica"?

---

## Cap. 01 — Tipos de aprendizaje y formalización supervisada

11. Dado un dataset `{(x_i, y_i)}_{i=1}^N`, ¿cómo determinás si el problema es de **regresión** o de **clasificación**?
12. ¿Qué notación usa el PDF de la cátedra para el target (`t_i` o `y_i`)? ¿Y los notebooks? ¿Por qué importa la convención?
13. ¿Por qué la cátedra escribe `y = f(x) + ε` en lugar de `y = f(x)`? ¿Qué representa `ε`?
14. [⚠️] Explicá con tus palabras la diferencia entre **datos con salida esperada** vs **datos sin salida esperada**. Dá un ejemplo de cada uno tomado del material.
15. Si te dan un dataset de transacciones bancarias **sin etiquetas** y te piden "detectar grupos de comportamiento similar", ¿qué tipo de aprendizaje es?
16. La cátedra menciona "salidas mediante tareas de pretexto" para auto-supervisado. ¿Qué es una tarea de pretexto y por qué se llama así?
17. ¿Por qué la cátedra dice que el fine-tuning permite "ser experto en un tema concreto con muy pocos datos"? ¿Qué hace posible eso?
18. Diferenciá **agente, ambiente, acción, recompensa** en un sistema de aprendizaje por refuerzo. ¿Quién emite cada uno?
19. ¿Por qué el aprendizaje por refuerzo en Ta-Te-Ti usa recompensa `+1 / -1 / 0` y no `1 / 0`?
20. En el diagrama del PDF p. 14, ¿qué retroalimentación reciben los pesos `w` desde la curva de pérdida?

---

## Cap. 02 — Regresión lineal y polinomial

21. [⚠️] Derivá paso a paso por qué **el promedio** es la solución óptima del problema "minimizar `Σ (y_i - a)²` con `a` constante". (Notebook 01 celda 11.)
22. ¿Cuál es la función de costo `E(w)` para regresión y por qué aparece el factor `1/2`?
23. ¿Qué es el **error cuadrático medio (MSE)** y cuál es la diferencia con el **RMSE**?
24. Dada la regresión polinomial `y(x, w) = Σ w_j x^j`, ¿cómo se interpreta el grado `M`? ¿Es un parámetro o un hiperparámetro?
25. La cátedra muestra que con `N=20` y `M=9` el val RMSE es **5.856**. ¿Por qué este número es catastrófico y qué dice sobre el modelo?
26. ¿Por qué la regresión polinomial se puede reducir a una **regresión lineal en `w`**? Mostrá la transformación `x → z`.
27. ¿Qué es la **matriz de diseño** `Z` (o `Φ`)? ¿Cuál es su shape en términos de `N` y `M`?
28. [⚠️] Escribí la **ecuación normal**. ¿Por qué se dice que es una "solución analítica cerrada"? ¿Qué significa eso operacionalmente?
29. ¿Por qué la cátedra recomienda **`np.linalg.pinv`** en lugar de **`np.linalg.inv`** en el notebook 01? ¿Cuándo importa esta distinción?
30. Si entrenás `LinearRegression` con `fit_intercept=False` sobre features creadas con `PolynomialFeatures`, ¿por qué NO necesitás el intercept? (Notebook 01 celda 43.)
31. Una recta SIN bias forzosamente pasa por **el origen**. ¿Qué problema causa eso en regresión, y cuál es la solución de la cátedra (notebook 01 celda 36)?
32. Para un dataset 1D, ¿qué shape tiene `X` para `sklearn.LinearRegression`? ¿Y por qué se usa `X.reshape(-1, 1)`?

---

## Cap. 03 — Sobreajuste, capacidad y regularización

33. Definí **underfitting** y **overfitting** con tus palabras. Dá una señal de cada uno en términos de error de train y error de validación.
34. [⚠️] La cátedra dice "El error de entrenamiento tiende a cero, pero el de validación crece con `M`". ¿Por qué? ¿Qué está pasando en el modelo?
35. Mirando la tabla de coeficientes del PDF p. 23: para `M=9` los `w` alcanzan **miles**. ¿Qué dice eso sobre el modelo?
36. ¿Cómo se relacionan `M` (capacidad) y `N` (cantidad de datos)? ¿Por qué aumentar `N` "rescata" un modelo de alto `M`?
37. Si tenés un modelo con val RMSE muy alto, **dos posibles diagnósticos** (sin regularización por ahora): ¿cuáles son y cómo los distinguís?
38. ¿Qué es el **bias-variance tradeoff**? Aunque la cátedra no usa estas palabras textualmente, ¿qué dos errores está balanceando la curva en U del val RMSE?
39. [⚠️] Escribí la función de costo **Ridge** (regularizada). ¿Qué término se añade y qué efecto tiene sobre los `w`?
40. Si subís `λ` mucho, ¿qué le pasa al modelo? ¿Y si lo bajás demasiado? Citá los números concretos del PDF p. 24 (`ln λ = -18` vs `ln λ = 0`).
41. ¿Por qué la cátedra siempre mueve `λ` en **escala logarítmica** (`ln λ`)?
42. ¿En qué se diferencia Ridge (L2) de Lasso (L1)? ¿Cuál de los dos hace **selección automática de features** y por qué?
43. En `sklearn.linear_model.LogisticRegression`, ¿qué relación hay entre el parámetro `C` y el `λ` matemático?
44. ¿Por qué el material **NO** desarrolla validación cruzada k-fold? ¿Con qué la sustituye?

---

## Cap. 04 — Clasificación y perceptrón

45. ¿Cuál es la diferencia entre regresión y clasificación en términos del rango de `y`? Y dentro de clasificación, ¿qué diferencia hay entre binaria y multiclase?
46. La cátedra usa `y ∈ {+1, -1}` para perceptrón pero `y ∈ {0, 1}` para logística. ¿Por qué la diferencia importa para la regla de actualización?
47. ¿Qué es **separabilidad lineal**? ¿Cómo se ve en 2D? Dá un caso clásico de datos **NO** linealmente separables.
48. [⚠️] Explicá las dos fases de un clasificador lineal: **scoring** (`f(x) = w^T x + b`) y **thresholding** (`sign(f(x))`). ¿Cuál es continua y cuál discreta?
49. ¿Qué es la "**medida de confianza**" del modelo según la cátedra? ¿Por qué se llama así (PDF p. 33)?
50. Escribí el **pseudocódigo del perceptrón clásico** en 5 pasos.
51. [⚠️] ¿Por qué la regla de actualización `w ← w + r · y_i · x_i` "rota la frontera hacia el ejemplo mal clasificado"? Explicalo geométricamente.
52. Enunciá el **teorema de convergencia del perceptrón**. ¿Cuándo aplica y cuándo NO?
53. Si los datos NO son linealmente separables, ¿qué le pasa al perceptrón? ¿Qué alternativas menciona la cátedra?
54. La cátedra dice: **"El vector `w` es perpendicular a la recta de decisión"** (notebook 02 celda 59). ¿Por qué? Mostralo a partir de la ecuación `w^T x = 0`.
55. En el experimento del notebook 02, `|w_1| ≈ 27.7 · |w_2|`. ¿Qué implica eso visualmente sobre la frontera?
56. ¿Qué pasa con un perceptrón **sin bias**? ¿Por qué la frontera está "tan restringida"?
57. Diferenciá el **perceptrón clásico** (actualización solo ante errores) del **algoritmo estándar con descenso de gradiente** (PDF p. 39).
58. ¿Por qué la cátedra dice que "la función de pérdida 0/1 no es diferenciable, así que necesitamos MSE"?
59. ¿Qué le pasa al algoritmo si la tasa de aprendizaje `r` es muy grande? ¿Y si es muy chica?

---

## Cap. 05 — Probabilidad y MLE

60. Enunciá la **regla de Bayes** y nombrá los cuatro términos: `P(Y|X)`, `P(X|Y)`, `P(Y)`, `P(X)`.
61. [⚠️] ¿Por qué la cátedra dice que clasificar = estimar `P(y|x)` para cada `x`?
62. ¿Qué es la **distribución de Bernoulli**? ¿Por qué la cátedra dice que "cada observación `y` es una Bernoulli con `p` que depende de `x`"?
63. Para muestras i.i.d., ¿qué significa la **independencia** y la **identidad de distribución**? ¿Por qué importa para el análisis de generalización (PDF p. 32)?
64. Definí **prior, likelihood, posterior, evidencia** en una clasificación de spam.
65. ¿Qué es la **máxima verosimilitud (MLE)**? ¿Por qué para una Bernoulli i.i.d. el estimador es la frecuencia relativa?
66. ¿Por qué se usa **log-verosimilitud** en lugar de verosimilitud directa? Mencioná las dos razones principales (matemática + numérica).
67. ¿Qué es la **cross-entropy** (entropía cruzada) y cómo se relaciona con la log-verosimilitud?
68. Diferenciá **modelos discriminativos** (regresión logística) de **modelos generativos** (Naive Bayes). ¿Qué modela cada uno?

---

## Cap. 06 — Regresión logística

69. ¿Cuál es la **función sigmoide** y cuáles son sus tres valores especiales (`σ(0)`, `σ(+∞)`, `σ(-∞)`)?
70. ¿Qué hace la sigmoide al score `z = θ^T x`? ¿Por qué decimos que da una **probabilidad**?
71. [⚠️] Explicá las **dos razones** por las que NO se usa MSE en regresión logística (PDF p. 5).
72. ¿Por qué la **log-loss** es convexa pero MSE+sigmoide NO lo es? ¿Qué garantiza la convexidad en términos de entrenamiento?
73. Derivá paso a paso de qué viene `J(θ) = -(1/m) Σ [y log h + (1-y) log(1-h)]` partiendo de la verosimilitud conjunta Bernoulli.
74. Si `y=1` y el modelo predice `h(x) → 0`, ¿qué le pasa a la log-loss para ese ejemplo? ¿Y si `y=1` y `h(x) → 1`?
75. ¿Qué es el **logit** o **log-odds**? ¿Por qué la regresión logística "asume linealidad en el log-odds"?
76. La cátedra dice **"el perceptrón decide de forma brusca; la regresión logística decide de forma suave"**. Traducí esa frase a una diferencia matemática concreta.
77. ¿Qué optimizador usa sklearn por defecto en `LogisticRegression`? ¿Por qué la cátedra elige no programarlo a mano (notebook 03 celda 96)?
78. En `LogisticRegression(max_iter=180)`, ¿qué significan las "iteraciones"?
79. ¿Cómo interpretarías visualmente `model.coef_[k].reshape(8,8)` para el caso del dígito `k` en el notebook 03 (celda 61)?
80. [⚠️] Escribí la **función softmax** y demostrá que `Σ_k P(Y=k|x) = 1`.
81. ¿Por qué la cátedra dice que "la sigmoide es el caso especial binario de softmax"? Verificalo con `K=2`.
82. Diferenciá `predict`, `decision_function`, `predict_proba` en sklearn. ¿Qué devuelve cada uno y en qué orden se aplican?

---

## Cap. 07 — Regularización en clasificación

83. Repasá los **tres tipos de regularización** disponibles en sklearn `LogisticRegression`: L1, L2, elasticnet. ¿Qué hace cada uno?
84. ¿Cuál es la relación entre `C` (sklearn) y `λ` (teórico)? Si querés **más regularización**, ¿subís o bajás `C`?
85. ¿Por qué Lasso (L1) hace **selección automática de variables** y Ridge (L2) NO?
86. ¿En qué situación elegirías `penalty='elasticnet'` por sobre L1 o L2 puros?
87. ¿Qué relación tiene la regularización con el **bias-variance tradeoff**?

---

## Cap. 08 — Naive Bayes

88. ¿Qué es el **supuesto naïve** y por qué la cátedra dice que "rara vez es cierto"?
89. [⚠️] Escribí la función de decisión Naive Bayes: `ŷ = argmax_y P(y) · Π P(x_i | y)`. ¿Por qué se ignora el denominador `P(x_1, ..., x_n)`?
90. Para el ejemplo "dinero oferta" del notebook 04, calculá a mano `P(spam | mensaje)` y verificá la predicción.
91. ¿Por qué Naive Bayes funciona bien en texto a pesar de violar la independencia? Mencioná el resultado de **Domingos & Pazzani 1997**.
92. ¿Qué es el **problema del cero** en MLE? Dá un ejemplo concreto donde una sola palabra rompe todo el clasificador.
93. [⚠️] Escribí el **suavizado de Laplace** (add-one). ¿Qué cambia respecto al MLE y por qué elimina el problema del cero?
94. Generalizá Laplace al suavizado de **Lidstone** con parámetro `α`. ¿Qué valores especiales tienen `α=0` y `α=1`?
95. ¿Por qué en Naive Bayes se trabaja con **log-probabilidades** y no con probabilidades directas?
96. Explicá la representación **Bag-of-Words (BoW)**. ¿Qué se pierde y qué se gana respecto a un texto en bruto?
97. Diferenciá las tres variantes de `MultinomialNB`, `GaussianNB`, `BernoulliNB` en sklearn. ¿Cuándo usás cada una?
98. Para el ejemplo Chinese/Japan del notebook 04, ¿por qué `P(zh) = 0.75` y no `P(zh) = 0.5`?
99. ¿Qué hace `CountVectorizer().fit_transform(corpus)`? ¿Qué tipo de matriz devuelve (densa o dispersa) y por qué?
100. Si una palabra aparece en `X_test` pero NO en `X_train`, ¿qué hace `CountVectorizer`?

---

## Cap. 09 — KNN

101. ¿Por qué KNN es un **modelo no paramétrico**? ¿Tiene fase de "entrenamiento" en el sentido tradicional?
102. [⚠️] Escribí el algoritmo KNN en 2 pasos (encontrar vecinos + votar).
103. ¿Cuál es el efecto de `k` en KNN según la cátedra? Citá los números del PDF p. 32 (`k = 1, 3, 7, 21`).
104. ¿Por qué `k=1` produce **overfitting** según la tabla `(training error: 0.000, testing error: 0.421)`?
105. ¿Por qué `k` grande "suaviza la frontera"? ¿Cuál es el tradeoff?
106. ¿Qué es un **diagrama de Voronoi** y qué representa visualmente para KNN?
107. ¿Por qué necesitás **estandarizar features** antes de usar KNN con distancia euclidiana?
108. ¿Cuál es el costo computacional de la **predicción** en KNN para `n` features y `m` ejemplos? ¿Y el costo de **memoria**?
109. ¿Qué estructuras de datos mitigan ese costo en dimensiones bajas?
110. ¿Qué pasa con la noción de "vecino cercano" cuando la dimensión `p` es muy alta? (Curse of dimensionality.)

---

## Cap. 10 — Multiclase y evaluación

111. Diferenciá clasificación **multiclase** (mutuamente excluyente) de **multietiqueta**. Dá un ejemplo concreto de cada una.
112. [⚠️] Explicá la estrategia **One-vs-All (OVA)**: cuántos modelos entrena y cómo decide.
113. ¿Cuál es el **riesgo principal** de OVA según el PDF p. 39?
114. ¿Cuántos modelos entrena la estrategia **All-vs-All (AVA / OvO)** para `K=10` clases?
115. ¿Por qué AVA es **"más robusto pero más costoso"** que OVA?
116. ¿En qué se diferencia **Softmax** de OVA y AVA? ¿Cuál garantiza probabilidades coherentes?
117. Para el ejemplo PDF p. 41 (Avión vs Auto vs Bus con AVA), verificá la votación y la decisión final.
118. ¿Qué métrica básica usa la cátedra para evaluar clasificadores en los notebooks (03 y 04)?
119. ¿Cuándo la **accuracy es engañosa**? Dá un ejemplo extremo.
120. ¿Qué te dice una **matriz de confusión** que no te dice la accuracy?
121. En la matriz de confusión del notebook 03 (dígitos manuscritos), ¿qué celdas mirarías para detectar errores sistemáticos?

---

## Cap. 11-14 — TP1 California Housing

122. ¿Qué tipo de problema es el TP1 (regresión / clasificación / clustering)? ¿Cuál es la variable objetivo y en qué unidades está expresada?
123. [⚠️] Si abrís el dataset y `X = california['data']` te devuelve un DataFrame (sklearn ≥ 1.2) en lugar de un ndarray, **¿qué le pasa al código `X[:, selector]`** del notebook? Listá las 3 soluciones documentadas.
124. ¿Por qué el TP1 obliga a discutir **sesgos éticos** en el Ej. 1? ¿Qué historia tiene California Housing al respecto?
125. En el Ej. 2 te piden visualizar cada feature contra el target. ¿Qué criterios visuales usás para rankear features por **informatividad**?
126. ¿Por qué la cátedra pide que **selecciones a mano** las features y no usa un método automático (Lasso, mutual information, etc.)?
127. En el Ej. 3, ¿qué shape debe tener `X_train` para `LinearRegression.fit`? Si tu selector booleano devuelve `(n,)`, ¿cómo lo arreglás?
128. El enunciado dice **"Con algunos atributos se puede obtener un error en test menor a 50"**. ¿En qué unidades está ese 50? (Discutí la trampa).
129. En el Ej. 4 (regresión polinomial), ¿qué rango de grados conviene probar? ¿Por qué el enunciado **no lo especifica**?
130. Cuando subís el grado del polinomio sin **normalizar** las features, ¿qué pasa numéricamente con los coeficientes y por qué se puede confundir con "overfitting real"?
131. ¿Cómo identificás el **codo** en la curva train-vs-test del Ej. 4? ¿Dónde está el mejor `M`?
132. En el Ej. 5 (multivariado), si usás `PolynomialFeatures(degree=3)` con 3 features, ¿cuántas features genera? (Combinaciones + interacciones.)
133. ¿Por qué el Ej. 5 dice "no hace falta graficar el modelo final"?
134. En el Ej. 7 (opcional), `Ridge(alpha=...)`, ¿cómo elegirías el mejor `alpha`? ¿Qué función de sklearn automatiza eso?
135. Si tu objetivo es maximizar **interpretabilidad** del modelo de California Housing, ¿elegís `LinearRegression`, `Ridge` o `Lasso`? Justificá.

---

## Preguntas integradoras (cross-capítulos)

136. [⚠️] Comparar **perceptrón, regresión logística y Naive Bayes** en una tabla: (a) frontera, (b) probabilidades, (c) supuestos, (d) regularización disponible, (e) cuándo usar cada uno.
137. ¿Cuáles de los modelos vistos en el módulo son **paramétricos**? ¿Cuál(es) **no paramétrico(s)**?
138. Dado un dataset chico (`N=200`) con 50 features altamente correlacionadas, ¿qué modelo del módulo elegirías y por qué? ¿Qué regularización?
139. Dado un dataset de 100k correos electrónicos para clasificar spam vs no spam, ¿elegís MultinomialNB o LogisticRegression? Pensá en velocidad de entrenamiento, interpretabilidad, y necesidad de probabilidades calibradas.
140. ¿Cómo se manifiesta el **overfitting** en regresión polinomial (Cap. 02), en perceptrón con tasa de aprendizaje mal calibrada (Cap. 04), y en KNN con `k=1` (Cap. 09)? Buscá el patrón común.
141. La cátedra dice "**No buscamos el modelo que mejor ajusta los datos de entrenamiento. Buscamos el modelo que mejor generaliza a datos nuevos.**" Aplicá esta idea a: regresión polinomial, regresión logística y KNN.
142. Explicá cómo se relaciona la **regla de Bayes** con: (a) Naive Bayes, (b) la log-loss derivada de la verosimilitud, (c) la distribución de Bernoulli en logística.
143. ¿Por qué la **función de costo convexa** es deseable? ¿En cuál de los modelos vistos la cátedra garantiza convexidad y en cuál no?
144. Para un mismo dataset binario, ¿en qué se parece y en qué se diferencia la **frontera de decisión** de: perceptrón, regresión logística (con `threshold=0.5`), Naive Bayes y KNN?
145. La cátedra menciona que el perceptrón es **"el átomo de las redes neuronales profundas"**. ¿Qué componentes del perceptrón aparecen idénticos en una neurona de red neuronal moderna?

---

## Preguntas-trampa (errores típicos)

146. Tu compañero dice: "Usé MSE como función de costo en regresión logística y funciona bien". ¿Qué le respondés?
147. Tu compañero dice: "Subí `M` a 15 y el train error es 0.001, ¡el modelo es perfecto!". ¿Qué le respondés?
148. Tu compañero dice: "Como las clases son `{0, 1}`, el perceptrón debería andar". ¿Qué le corregís?
149. Tu compañero dice: "Multiplicé todas las `P(palabra|clase)` y me dio cero". ¿Cuál es el problema y la solución?
150. Tu compañero dice: "Mi modelo de fraude tiene 99% de accuracy, está perfecto". ¿Qué le decís?
151. Tu compañero dice: "Usé Ridge con `λ = 10^6` y los coeficientes son chicos, ya está, no hay overfitting". ¿Qué le señalás?
152. Tu compañero dice: "Cargué el dataset y como `X` es DataFrame, hice `X[:, selector]` y no anda — sklearn está roto". ¿Está sklearn roto?
153. Tu compañero dice: "KNN con `k=1` da error 0 en train, es el mejor modelo". ¿Por qué está equivocado?
154. Tu compañero dice: "Como el perceptrón no converge, voy a aumentar las iteraciones a 1 millón". ¿Qué le proponés en vez?
155. Tu compañero dice: "Los `z_k` del modelo son las probabilidades por clase". ¿Cuál es la confusión y cómo se la corregís?

---

→ [14-bibliografia.md](14-bibliografia.md)
