# Apunte de estudio: Aprendizaje Supervisado (Diplodatos, FAMAF UNC, Karim Nemer Pelliza y Diego González Dondo)

**Curso:** Aprendizaje Supervisado, materia obligatoria de la Diplomatura en Ciencia de Datos, Aprendizaje Automático y sus Aplicaciones de FAMAF (UNC), cohorte 2026. Va después de Introducción al Aprendizaje Automático y antes de Aprendizaje No Supervisado · Docentes: Karim Nemer Pelliza (la teoría con filminas) y Diego González Dondo (las notebooks), los dos docentes investigadores de un centro de investigación de la UTN (robótica y visión) · Coordinación: Carolina ("Caro") · Formato: cuatro clases sincrónicas grabadas en 8 videos no listados del canal FAMAF UNC: viernes 26 de junio a la tarde, sábado 27 de junio a la mañana, viernes 3 de julio (adelantada a las 15 por el partido de Argentina contra Cabo Verde del Mundial) y sábado 4 de julio a la mañana de 2026. En las grabaciones se dicen "Karim" y "Diego González"; los nombres completos salen de la página del equipo docente de la diplomatura, que lista a Karim Alejandra Nemer Pelliza y a Diego González Dondo.
**De qué va:** la materia arranca por los cuatro enfoques de la inteligencia artificial y las etapas de un proyecto de aprendizaje automático, y después recorre los modelos supervisados "fuertes" que no se vieron en Introducción: máquinas de vectores de soporte para clasificación y regresión, con kernels; perceptrón y redes neuronales multicapa, con descenso por gradiente, backpropagation, regularización y dropout; redes convolucionales y transfer learning; redes recurrentes, LSTM y Transformers, con un fine tuning de DistilBERT; ensambles (bagging, random forest, boosting, XGBoost y voting) y sistemas de recomendación. Las notebooks usan scikit-learn, Keras, PyTorch con Hugging Face, XGBoost y Surprise. Se aprueba con un único trabajo: una competencia de Kaggle en grupos que cierra el 27 de julio.

> Nota: este apunte sale de los subtítulos automáticos en español de los videos. Siete tienen transcripción completa de la grabación. La de C4P2 no se pudo bajar (la grabación pidió "confirmar que no sos un bot" y después devolvió "demasiadas solicitudes" en todos los reintentos espaciados) y se rehízo con faster-whisper a partir del audio (ver "Lo que falta"). Muchos nombres vienen deformados (ver el glosario al final). Todo lo que figura acá es lo que se dice en clase. Cuando lo que se dijo está mal o es impreciso, lo marco como **Corrección**. Las cifras, fechas y afirmaciones que no chequeé están marcadas como **para verificar**. Algunas cosas sí las chequeé corriendo código en el box: scikit-learn 1.9.1, Keras 3.15.1 con backend PyTorch, XGBoost 3.4.1, Surprise 1.1.5 y Transformers 5.18 (con un fine tuning chico de DistilBERT). Eso está dicho en cada caso. Lo que no se entiende bien en la transcripción va como **dudoso**. Las ideas mías van marcadas como **Sugerencia**.

**Cómo leer los links:** cada link dice el video y el minuto. "C2P1 1:23:45" es la clase 2, parte 1, en la hora 1, minuto 23, segundo 45.

## Los 8 videos

| # | Id | Video | Contenido | Duración | Link |
|---|---|---|---|---|---|
| 1 | — | C1P1: Clase 1, parte 1 (26/06/2026 17:40) | Presentación, enfoques de la IA, definición y etapas del aprendizaje automático, SVM lineal, margen, hinge loss, C, desbalance, kernels, GridSearchCV, anuncio de la competencia de Kaggle | 2:17:11 |  |
| 2 | — | C1P2: Clase 1, parte 2 ("Recording 2") | SVR, épsilon y C, kernels en regresión, GridSearchCV, California housing, perceptrón | 1:17:19 |  |
| 3 | — | C2P1: Clase 2, parte 1 (27/06/2026 09:50) | Arquitecturas de redes, tipos de aprendizaje, activaciones, TensorFlow Playground, descenso por gradiente, backpropagation, MLPClassifier y Keras con gato o no gato | 1:57:09 |  |
| 4 | — | C2P2: Clase 2, parte 2 ("Recording 2") | Entrenar y evaluar en Keras, MNIST, dropout, sesgo y varianza, regularización, redes convolucionales, Fashion MNIST, data augmentation, transfer learning | 1:45:56 |  |
| 5 | — | C3P1: Clase 3, parte 1 (03/07/2026 14:54) | Redes recurrentes, tokens, SimpleRNN y LSTM con IMDB, Transformers: atención, Q, K y V, multi head, positional encoding | 1:53:45 |  |
| 6 | — | C3P2: Clase 3, parte 2 ("Recording 2") | Fine tuning de DistilBERT con Hugging Face, ensambles, bagging, árboles, random forest, boosting (AdaBoost, gradient boosting, XGBoost), voting | 1:37:57 |  |
| 7 | — | C4P1: Clase 4, parte 1 (04/07/2026 09:54) | Demo de XGBoost, sistemas de recomendación, filtros colaborativos, Pearson y coseno ajustado, librería Surprise | 1:27:46 |  |
| 8 | — | C4P2: Clase 4, parte 2 ("Recording 2") | Buenas prácticas (Machine Learning Yearning): particiones, métricas, clasificadores bobos, sesgo y varianza, análisis de errores, registro de experimentos, tests; notebook de Titanic; explicación de la competencia de Kaggle con barbijos (transcripción con faster-whisper, ver "Lo que falta") | 2:08:16 |  |

Duración total: 14:25:19 (unas 14 horas y 25 minutos).

**Cómo se determinó el orden.** Los títulos traen la clase y la fecha y hora de grabación, y la segunda parte de cada clase se llama "Recording 2". El contenido encadena sin huecos: C1P1 corta en el recreo después de anunciar la competencia de Kaggle C1P1 2:16:49 y C1P2 arranca con SVM para regresión C1P2 0:10; C1P2 cierra con "la clase de mañana es intensa", redes neuronales, y "mañana a las 10" C1P2 58:50, C1P2 1:16:56, y C2P1 arranca con "ayer habíamos visto hasta las partes de una neurona" C2P1 0:36; C2P1 corta a las 12:10 en medio de la notebook de Keras C2P1 1:56:09 y C2P2 sigue con "ahora lo que hay que hacer es entrenarla" C2P2 0:20; C2P2 termina con "nos vemos el viernes" y las recurrentes "la semana que viene" C2P2 1:45:45, y C3P1 es "la tercera clase", con recurrentes y Transformers C3P1 0:25, C3P1 2:03; C3P1 corta en la pausa de las 17 C3P1 1:52:52 y C3P2 retoma con la notebook de Transformers en PyTorch C3P2 1:34; C3P2 termina con "nos vemos mañana a las 10" C3P2 1:37:11 y C4P1 abre con "la demo de anoche de XGBoost" C4P1 0:34; C4P1 corta en el recreo de las 12:20 anunciando buenas prácticas y el práctico C4P1 18:03, C4P1 1:25:55, que es el contenido de C4P2.

## Mapa de módulos y videos

| Módulo | Dónde se ve |
|---|---|
| 0. La materia: quiénes la dan, plan, horarios, materiales y evaluación | C1P1 (inicio y final), C1P2 (final), C3P1 (inicio), C4P1, C4P2 |
| 1. Inteligencia artificial, aprendizaje automático y las etapas de un proyecto | C1P1 |
| 2. SVM para clasificación: margen, hinge loss, C y desbalance | C1P1 |
| 3. Kernels: cuando los datos no son linealmente separables | C1P1, C1P2 |
| 4. SVR: SVM para regresión | C1P2 |
| 5. Perceptrón y redes neuronales: neurona, activaciones, gradiente y backpropagation | C1P2 (final), C2P1 |
| 6. Redes en la práctica: scikit-learn, Keras, sobreajuste, regularización y dropout | C2P1, C2P2 |
| 7. Redes convolucionales y transfer learning | C2P2, C3P2 |
| 8. Redes recurrentes y LSTM | C3P1 |
| 9. Transformers y fine tuning | C3P1, C3P2 |
| 10. Ensambles, árboles, bagging y random forest | C3P2 |
| 11. Boosting, XGBoost y voting | C3P2, C4P1 |
| 12. Sistemas de recomendación | C4P1 |
| 13. Buenas prácticas: del problema al modelo en producción | C4P2 |
| 14. El trabajo práctico: la competencia de Kaggle | C1P1, C4P2 |

---

## 0. La materia: quiénes la dan, plan, horarios, materiales y evaluación
**Dónde:** C1P1 0:06, C1P1 2:54, C1P1 14:05, C1P1 42:54, C1P1 44:40, C1P1 2:12:28, C1P1 2:14:53, C1P2 1:00:11, C2P1 1:25:31, C2P2 1:45:24, C3P1 0:25, C3P1 2:03, C3P2 30:51, C4P1 18:03

### Conceptos clave
- **Karim.** Da la teoría con filminas. Hizo la tesis doctoral entrenando redes con un millón de imágenes de 200 por 200 en cuatro computadoras durante cuatro meses C2P2 39:42 y trabaja con imágenes satelitales SAR de coberturas de la provincia de Córdoba C2P1 1:37:25. Fue alumna del curso de redes neuronales de "Pancho" Tamarit en FAMAF, que según ella le enseñó sus primeras redes C2P2 1:45:24 (el nombre completo, Francisco Tamarit, es **para verificar**). En C1P1 dice que ya se había presentado "en la materia anterior" C1P1 1:19:00; cuál es, **para verificar** (Introducción al Aprendizaje Automático la dieron otros docentes).
- **Diego González.** Se presenta como ingeniero electrónico, doctor en electrónica y docente investigador en la UTN con Karim, en un centro de investigación de robótica y visión C1P1 42:54. Su dominio son las imágenes: aclara que no es especialista en recurrentes ni en Transformers para texto C3P1 39:17, C3P2 23:02. Corre las notebooks en Jupyter local, sin subir los datos a Colab, y recurre a Colab cuando su máquina tarda demasiado C2P1 1:06:32, C3P2 0:29.
- **Qué cambió este año.** Karim dice que modificaron la materia y la hicieron "muy ambiciosa" C1P1 2:54; Diego, que sacaron lo redundante con Introducción C1P1 42:54. Recurrentes y Transformers son "temas nuevos que el año pasado no vimos" C3P1 2:03.
- **Otras personas que aparecen.** Carolina, la coordinadora, que responde por Slack y por mail C3P1 0:25; Georgina, que da la electiva de series temporales con LSTM C1P1 14:05; Jorge Sánchez, a quien Diego presenta como pionero en SVM y kernels con un paper muy citado C1P1 1:31:30 (cuál, **para verificar**: puede ser el trabajo de Fisher vectors de Sánchez, Perronnin y otros de 2013); un profesor "Bustos" de FAMAF, ya fallecido, que llamaba "datos sorprendentes" a los atípicos C1P1 58:36 (nombre completo **para verificar**). Entre los alumnos que preguntan: Juan, Carla, Agustín, Franco, Florencio, Eric, Daniela, Nicolás, Federico, Manuel (que hace de "asistencia técnica" con los parámetros de Keras C3P1 46:20), Antonio, Gonzalo, María, Sebastián, Guillermo, Jonathan y Lu.
- **Horarios.** Viernes de 18 a 22 y sábado de 10 a 14 C1P2 1:00:11. La clase 3 se adelantó: el viernes 3 de julio Argentina jugaba a las 19, Karim hizo una encuesta y la clase arrancó cerca de las 15 C1P2 1:00:11; en C3P1 ella misma nombra el partido contra Cabo Verde C3P1 1:38:42, y Diego cierra C3P2 con "Chao, Argentina, vamos" C3P2 1:37:11. En C1P2 la transcripción dice "contra Ciudad del Cabo", que es un error de transcripción o un lapsus.
- **Materiales.** Filminas y notebooks en el aula virtual; la librería propia `mlutils` está en el repositorio y hay que subirla a Colab si no corrés local C1P1 44:40, C2P1 1:06:32. Las dudas van por Slack o por mail C1P2 1:16:56, y por Slack se hizo la encuesta del horario del viernes C2P2 1:45:45.
- **Electivas que recomiendan.** Deep Learning (aprendizaje profundo) C2P1 1:25:31, Procesamiento de imágenes y Visión por computadora C2P2 1:20:44, Series temporales C3P1 40:33. Diego cuenta que Ética ahora es obligatoria y la recomienda C3P2 30:51.
- **Evaluación.** Un único trabajo: una competencia de Kaggle en grupos, con muchas entregas y tabla pública, que se explica en la última clase y cierra el 27 de julio C1P1 2:12:28, C1P1 2:14:53. El detalle está en el módulo 14.

### Correcciones y matices
- **para verificar:** quiénes dan Ética. Diego dice que son doctoras y que "una es lingüista" C3P2 30:51; en las clases de Aprendizaje No Supervisado de esta misma cohorte se dice que Ética la dan Laura Alonso Alemany, que es lingüista, y Luciana, lo que coincide.

### Preguntas de repaso
1. ¿Qué temas son nuevos este año y por qué la materia se siente apurada?
2. ¿Qué tenés que subir a Colab además de la notebook para que corran los ejemplos?
3. ¿Cómo se aprueba la materia y hasta cuándo hay tiempo?

---

## 1. Inteligencia artificial, aprendizaje automático y las etapas de un proyecto
**Dónde:** C1P1 0:40, C1P1 4:34, C1P1 6:46, C1P1 8:27, C1P1 12:20, C1P1 15:05, C1P1 16:30, C1P1 17:51, C1P1 20:38, C1P1 24:43

### Conceptos clave
- **Cuatro enfoques de la IA.** Actuar como humanos (el test de Turing, de 1950), pensar como humanos (modelos cognitivos), pensar racionalmente (las leyes del pensamiento, la lógica) y actuar racionalmente (agentes) C1P1 0:40, C1P1 2:54. Es la clasificación clásica de Russell y Norvig, aunque en clase no se los nombra.
- **Ejemplos.** El robot Sophia parece humano pero no genera conocimiento: responde por probabilidades C1P1 4:34. Para el enfoque lógico, el chiste de "nada es mejor que la felicidad eterna; un sándwich es mejor que nada; entonces un sándwich es mejor que la felicidad eterna" muestra lo frágil de razonar con palabras ambiguas C1P1 6:46. Los agentes racionales usan lo que tienen para decidir lo mejor posible, con racionalidad limitada; ejemplos de lógica difusa en trenes y ascensores C1P1 8:27.
- **Dónde está la materia.** En Introducción vieron lógica, Naive Bayes, vecinos y perceptrón; acá se ven los modelos de la "capa" siguiente, y algo de aprendizaje por refuerzo C1P1 12:20.
- **Definición de aprendizaje automático.** Darle a la computadora la capacidad de aprender sin ser programada explícitamente; y la versión formal: un programa aprende de la experiencia E respecto de una tarea T y una medida de desempeño P si su desempeño en T, medido por P, mejora con E C1P1 15:05.
- **Usos.** Clasificación (fraude, retención de clientes, imágenes, diagnóstico) y regresión (publicidad, clima, economía, esperanza de vida) C1P1 16:30.
- **Etapas de un proyecto.** Definir el problema, analizar los datos, fijar métricas de éxito y fracaso, dividir los datos, probar primero un modelo chico para ver si converge, ajustar, entrenar con todo, testear e iterar. La división "suele ser 80 20" C1P1 17:51.
- **Los datos y las tres particiones.** Instancias con n atributos y una etiqueta; el modelo aproxima una función, en general no lineal, y lo que importa es que generalice. Con el ejemplo de edad y tamaño de tumor: entrenamiento para ajustar, validación para elegir hiperparámetros y evaluación (test) para medir la generalización C1P1 20:38, C1P1 24:43.

### Correcciones y matices
- **Corrección:** Karim atribuye a Arthur Samuel las dos definiciones C1P1 15:05. La de "aprender sin ser programada explícitamente" se le atribuye a Samuel (1959), pero la de experiencia, tarea y medida (E, T, P) es de Tom Mitchell, en su libro *Machine Learning* de 1997.
- **Corrección:** para hablar de la programación tradicional dice "programación lineal" C1P1 15:05. La programación lineal es un método de optimización; lo que quiso decir es programación explícita, con reglas escritas a mano.
- **para verificar:** el ejemplo de lógica difusa en el frenado de trenes rápidos de Japón C1P1 8:27. El caso conocido es el metro de Sendai, que empezó a operar con control difuso en 1987.
- **dudoso:** "Aprendizaje supervisado es otra materia" C1P1 12:20; por el contexto quiso decir no supervisado.

### Preguntas de repaso
1. ¿Cuáles son los cuatro enfoques de la IA y en cuál cae el test de Turing?
2. Escribí la definición de Mitchell con un ejemplo tuyo de E, T y P.
3. ¿Para qué sirve cada una de las tres particiones y por qué no alcanza con entrenamiento y test?
4. ¿Por qué conviene probar primero un modelo chico antes de entrenar con todo?

---
## 2. SVM para clasificación: margen, hinge loss, C y desbalance
**Dónde:** C1P1 28:03, C1P1 34:45, C1P1 36:05, C1P1 38:24, C1P1 45:50, C1P1 48:48, C1P1 50:43, C1P1 58:36, C1P1 1:02:13, C1P1 1:04:18, C1P1 1:07:19, C1P1 1:13:24

### Conceptos clave
- **La idea.** Entre las infinitas fronteras que separan dos clases, la máquina de vectores de soporte elige la de **máximo margen**: la que deja más espacio hasta los puntos más cercanos de cada clase. Esos puntos son los **vectores de soporte** y los encuentra el algoritmo, no uno C1P1 28:03, C1P1 34:45. Karim lo muestra con una demo de navegador donde movés puntos y ves cambiar la frontera (cuál, **para verificar**).
- **Función de costo.** La **hinge loss** (pérdida bisagra; la transcripción dice "King Los"), con etiquetas −1 y 1 C1P1 36:05.
- **C.** Regula cuánto tolerás puntos mal clasificados o dentro del margen: margen duro (hard margin) contra margen blando (soft margin). C alto castiga mucho los errores y deja un margen angosto; C chico castiga poco y deja un margen ancho. En scikit-learn C es la inversa de la fuerza de regularización C1P1 38:24, C1P1 1:04:18.
- **Frente a perceptrón y regresión logística.** El perceptrón simple no converge si los datos no son separables C1P1 1:02:13; la SVM sí encuentra una solución con margen blando. Es liviana y fue el estado del arte en visión hasta que las redes convolucionales la superaron C1P1 45:50.
- **Notebook de SVM lineal (Diego).** Dataset sintético de 100 muestras con 38 y 62 por clase, `LinearSVC` con `penalty`, `loss`, `tol`, `C` y `random_state`, y después `coef_` e `intercept_` para dibujar la recta C1P1 48:48, C1P1 50:43. Con 3%, 10% y 20% de ruido la recta casi no se mueve: es robusta porque solo los vectores de soporte la definen C1P1 58:36.
- **Barrido de C** de 0,001 a 1000: el mejor es C = 100, con 0,88 en entrenamiento y 0,81 en test; la brecha entre los dos es la señal de sobreajuste C1P1 1:07:19.
- **Desbalance.** Con 400 contra 100 ejemplos, `class_weight="balanced"` sube el acierto de la clase chica de 81% a 94% aunque el accuracy total baje de 0,93 a 0,918 C1P1 1:13:24. Moraleja: con clases desbalanceadas, el accuracy solo engaña.

### Correcciones y matices
- **Corrección:** Karim dice que el costo es "cero si tiene el mismo signo y está dentro del margen, y si no será uno" C1P1 36:05. La hinge loss es max(0, 1 − y·f(x)): vale 0 solo si el punto está bien clasificado y fuera del margen (y·f(x) ≥ 1), y crece linealmente cuanto más se mete en el margen o del lado equivocado. No es una pérdida 0 o 1. Verificado en el box: para y·f(x) = 2, 1, 0,5, 0 y −1 da 0, 0, 0,5, 1 y 2.
- **Corrección:** "SVM no da probabilidad o confianza" C1P1 45:50. `SVC` tiene `decision_function` (la distancia firmada a la frontera) y puede dar probabilidades con escalado de Platt. Ojo: en scikit-learn 1.9 `SVC(probability=True)` ya tira un aviso de obsoleto (se quita en la 1.11); la forma recomendada es `CalibratedClassifierCV(SVC(), ensemble=False)` (verificado en el box).
- **Corrección:** "las redes convolucionales de fines de la década del 2000 les pasaron el trapo" C1P1 45:50. El quiebre fue AlexNet en ImageNet, en 2012.
- **Corrección:** según Diego, `class_weight="balanced"` "multiplica los pesos por la probabilidad de que la clase aparezca" C1P1 1:13:24. Es al revés: el peso de cada clase es inversamente proporcional a su frecuencia, n_muestras / (n_clases · n_clase). Con 400 y 100 da 0,625 y 2,5 (verificado en el box).
- **dudoso:** en el mismo bloque habla de "la media geométrica entre los dos valores" C1P1 1:13:24 y no queda claro qué métrica está mostrando.
- **Matiz:** "omegas grandes son numéricamente intratables" C1P1 1:04:18. El motivo de penalizar pesos grandes es sobre todo evitar el sobreajuste (y en SVM, maximizar el margen, que es 2/‖w‖), no un problema numérico.

### Preguntas de repaso
1. ¿Qué son los vectores de soporte y por qué la frontera no cambia si movés un punto lejano?
2. Calculá la hinge loss para un punto con y = 1 y f(x) = 0,3. ¿Está bien clasificado? ¿Tiene costo?
3. ¿Qué pasa con el margen y con el sobreajuste si subís C?
4. ¿Qué pesos asigna `class_weight="balanced"` a dos clases de 900 y 100 ejemplos?

---

## 3. Kernels: cuando los datos no son linealmente separables
**Dónde:** C1P1 1:19:00, C1P1 1:23:08, C1P1 1:25:11, C1P1 1:26:20, C1P1 1:31:30, C1P1 1:36:46, C1P1 1:38:55, C1P1 1:41:48, C1P1 1:46:08, C1P1 1:54:34, C1P1 1:56:37, C1P1 2:01:47, C1P1 1:59:01, C1P1 2:03:03, C1P1 2:05:25, C1P1 2:09:04

### Conceptos clave
- **Proyectar a más dimensiones.** Si los datos no se separan con una recta, se los lleva a un espacio de características de mayor dimensión donde sí se separan. Ejemplo de Karim: con x₃ = √2·x₁·x₂ (el mapa polinomial de grado 2) C1P1 1:19:00.
- **El truco del kernel.** Un kernel es una función que calcula directamente el producto interno en ese espacio proyectado, sin construir la proyección C1P1 1:23:08, C1P1 1:31:30. Los comunes: lineal, polinomial, RBF (gaussiano) y sigmoide (tangente hiperbólica); se puede definir uno propio C1P1 1:25:11, C1P1 1:36:46.
- **Intuición de Diego con círculos concéntricos.** Si pasás a coordenadas polares, el radio solo separa las dos clases C1P1 1:38:55. "La naturaleza es altamente no lineal; los ingenieros linealizamos" C1P1 1:41:15.
- **Resultados en círculos.** Sigmoide 65% ("apenas por encima de tirar la moneda") C1P1 1:41:48; RBF 99% C1P1 1:46:08; polinomial de grado 6, 95%, y barriendo grados de 2 a 7, 99% C1P1 1:56:37, C1P1 2:00:44.
- **gamma.** En RBF, gamma chico da una frontera suave y gamma grande una frontera que rodea cada punto: sobreajuste, con más vectores de soporte (86 contra 156) C1P1 1:46:08.
- **Búsqueda de hiperparámetros.** Primero valores por defecto, después barrer, y mirar qué usa la literatura C1P1 1:54:34. `train_test_split` 80/20 y `GridSearchCV` sobre un `Pipeline` con `StandardScaler` y `SVC`, con validación cruzada de 5 partes: RBF con C = 1 y gamma = 10 da 0,98 y 0,97; polinomial, 0,99 y 1,00 C1P1 2:01:47.
- **Otros datasets sintéticos.** `make_circles`, `make_moons` y `make_blobs` con ruido C1P1 2:03:03. Un kernel lineal con 0,9 en lunas puede ser aceptable si tenés recursos acotados (microcontroladores, tiempo real) C1P1 2:05:25.
- **Resumen de buenas prácticas** C1P1 2:09:04: elegir el kernel según la literatura, escalar siempre, empezar por el lineal, usar validación cruzada y vigilar el sobreajuste. Parsimonia: si un modelo simple alcanza, ahorrás cómputo, agua y carbono C1P1 1:56:37.

### Correcciones y matices
- **Corrección:** Karim describe el kernel como "un proceso iterativo que va agregando dimensiones, lo proyecta n veces hasta que separa" C1P1 1:23:08, y lo repite en regresión C1P2 13:20. El kernel se elige de antemano y es fijo; no se van agregando dimensiones. Con RBF el espacio implícito es de dimensión infinita, y con el kernel lineal no hay proyección.
- **Corrección:** al explicar la matriz de confusión dice que "la precisión analiza esta fila y el recall esta columna" C1P1 1:59:01. En scikit-learn las filas son la clase verdadera y las columnas la predicha: el recall se lee por fila y la precisión por columna.
- **Corrección:** "F1, la media geométrica" C1P1 1:59:01. F1 es la media **armónica** de precisión y recall: 2PR/(P+R). El error se repite en C2P2 11:29 y C3P2 25:17. Con P = 1 y R = 0,5, la armónica da 0,667 y la geométrica 0,707 (verificado en el box).
- **dudoso:** "los grados pares dan forma ovalada y los impares oscilaciones" C1P1 1:56:37. Es una intuición de la demo, no una regla.
- **Sugerencia:** en el box, con círculos concéntricos, el lineal da entre 0,43 y 0,55 según la partición, el sigmoide 0,58 o 0,59, y RBF y polinomial de 0,99 a 1,0; un barrido de gamma muestra el sobreajuste (con gamma = 1000 el test cae a 0,6). Los números exactos cambian con la semilla y el ruido, pero el patrón es el mismo de la clase.

### Preguntas de repaso
1. ¿Qué calcula un kernel y por qué no hace falta construir la proyección?
2. ¿Por qué el kernel sigmoide anda mal en círculos concéntricos y el RBF bien?
3. ¿Qué indica que un SVC con RBF tenga muchísimos vectores de soporte?
4. En una matriz de confusión de scikit-learn, ¿dónde leés el recall de la clase 1?

---

## 4. SVR: SVM para regresión
**Dónde:** C1P2 0:10, C1P2 1:17, C1P2 3:32, C1P2 9:01, C1P2 10:43, C1P2 11:26, C1P2 16:57, C1P2 17:31, C1P2 20:37, C1P2 32:27, C1P2 34:17, C1P2 40:40, C1P2 42:08, C1P2 43:48, C1P2 48:48, C1P2 49:47, C1P2 50:55, C1P2 54:15, C1P2 55:53, C1P2 56:57

### Conceptos clave
- **El tubo épsilon.** En SVR se arma un tubo de ancho ε alrededor de la función: los errores dentro del tubo no cuestan nada (error aceptable) y los de afuera cuestan linealmente (pérdida ε insensible). C pesa esos errores contra la complejidad del modelo C1P2 0:10, C1P2 1:17, C1P2 10:43. Un ε demasiado chico sobreajusta C1P2 9:01.
- **Regresión como ajuste de curvas.** Diego: la regresión lineal por mínimos cuadrados tiene solución cerrada y única; por eso `fit` se llama así, por ajustar C1P2 11:26, C1P2 20:15.
- **LinearSVR** con `epsilon`, `C`, `loss` y `max_iter`, sobre `make_regression` de 100 datos y una característica C1P2 13:13, C1P2 16:57. Partición 70/30, "como el fernet" C1P2 18:37.
- **Kernels en regresión.** Con 200 datos no lineales, el MSE da 28,11 con lineal, 0,19 con polinomial de grado 3 y 0,072 con RBF C1P2 32:27, C1P2 40:40. Barrido: mejor C = 10 y ε = 0,1; gamma alto sobreajusta C1P2 43:48. `GridSearchCV` prueba 64 candidatos, 320 ajustes, y elige C = 10 y ε = 0,1 con R² 0,91 C1P2 48:48.
- **Frente a la regresión polinomial.** En mínimos cuadrados los puntos de los extremos tienen más "torque" (palanca), y un atípico tira la curva; en SVR la pérdida es lineal fuera del tubo y cero adentro, así que los puntos lejanos pesan menos C1P2 34:17, C1P2 54:15.
- **California housing** (el práctico 1 de la materia anterior): 8 variables, `Pipeline` con `StandardScaler` y SVR RBF con C = 1 y ε = 0,1, error 0,33 en entrenamiento y 0,35 en test C1P2 49:47, C1P2 50:55. Tarda mucho: SVR escala mal con la cantidad de muestras y scikit-learn no usa GPU C1P2 56:57.
- **Checklist de SVR:** escalar, elegir el kernel, barrer C, ε y gamma C1P2 54:15.

### Correcciones y matices
- **Corrección:** "todos los puntos fuera del tubo forman el vector de soporte; queremos que llegue a ser nulo, no tener ningún vector de soporte" C1P2 3:32. Los vectores de soporte de SVR son los puntos sobre el borde del tubo o fuera de él, y la solución siempre tiene algunos. El objetivo combina la norma de los pesos con las desviaciones, ponderadas por C. En el box, con 140 puntos de entrenamiento, ε = 0, 0,1, 0,3 y 0,5 dejan 140, 48, 4 y 2 vectores de soporte: bajan, pero no llegan a cero.
- **Corrección:** "estamos tratando de maximizar las diferencias" C1P2 10:43: lapsus, se minimizan.
- **Matiz:** ante "¿épsilon arranca en cero?", Diego responde "sí, empieza en cero" C1P2 17:31. ε es un hiperparámetro fijo, no "arranca" ni cambia durante el ajuste. El valor por defecto es 0,0 en `LinearSVR` y 0,1 en `SVR` (verificado en el box).
- **Corrección:** C "le da peso uno al valor absoluto de los pesos" C1P2 20:37. `LinearSVR` regulariza con la norma L2 al cuadrado, como Ridge; el valor absoluto es L1, como Lasso.
- **Matiz:** Karim justifica regularizar porque "los pesos grandes llenan la memoria, un número de 64 bits no entra en 32" C1P2 20:37. La razón es el sobreajuste, no el desborde numérico.
- **para verificar:** ante un R² negativo Diego dice "quizás está mal calculado, un menos en mlutils" C1P2 42:08. El R² de test puede ser negativo legítimamente cuando el modelo predice peor que la media; en el box un modelo malo da R² = −3,0. Puede haber un error en `mlutils`, pero un R² negativo no lo prueba.
- **Corrección:** "el SVR proyecta los datos de vuelta, lo hace el sistema automáticamente" C1P2 34:17. Depende del kernel que elijas.
- **Corrección:** a la pregunta de qué es X en California, Karim responde "el barrio, las dimensiones, si tenés vecinos de color" C1P2 55:53. California housing no tiene ninguna variable racial; eso era la columna "B" del dataset de Boston, que scikit-learn quitó en la versión 1.2 por problemas éticos.
- **Matiz:** "20.000 muestras" son 20.640 C1P2 49:47.
- **dudoso:** varios números de los resultados se entienden mal en el audio: un MSE de entrenamiento con "épsilon 5" C1P2 25:45, un MSE de test de "215" (probablemente 2,15) C1P2 31:14 y un MSE de "0,71" del GridSearch que, por los barridos anteriores, debería ser 0,071 C1P2 48:48.

### Preguntas de repaso
1. ¿Qué puntos son vectores de soporte en SVR y qué pasa con ellos si agrandás ε?
2. ¿Por qué SVR es más robusta a atípicos que la regresión por mínimos cuadrados?
3. ¿Qué significa un R² negativo en test?
4. ¿Por qué SVR con RBF tarda tanto con 20.640 muestras y qué alternativa probarías?

---
## 5. Perceptrón y redes neuronales: neurona, activaciones, gradiente y backpropagation
**Dónde:** C1P2 1:04:59, C1P2 1:05:33, C1P2 1:10:07, C1P2 1:11:28, C1P2 1:13:28, C1P2 1:15:45, C2P1 0:36, C2P1 2:22, C2P1 5:14, C2P1 8:05, C2P1 9:31, C2P1 11:25, C2P1 13:33, C2P1 19:59, C2P1 22:50, C2P1 23:24, C2P1 26:37, C2P1 31:00, C2P1 38:17, C2P1 42:40, C2P1 43:15, C2P1 47:06, C2P1 50:51, C2P1 54:13, C2P1 58:48

### Conceptos clave
- **Perceptrón.** Frank Rosenblatt, 1958. Como la neurona biológica (dendritas, axón, neurotransmisores), hace una suma ponderada de las entradas más un sesgo y devuelve 0 o 1. Solo resuelve problemas linealmente separables. Aprende online, un ejemplo por vez, con una tasa de aprendizaje y una regla de actualización C1P2 1:05:33, C1P2 1:10:07.
- **Por qué la sigmoide.** La función signo no es derivable; la sigmoide es su versión continua y derivable, y permite actualizar con pasos chicos C1P2 1:11:28.
- **Por qué es aprendizaje automático.** Aprende de la experiencia; además tiene un factor estocástico: cambiar la semilla o el orden de los datos cambia el resultado C1P2 1:13:28, C2P1 11:25. Con muchas neuronas hay más incógnitas que ecuaciones y se usan métodos iterativos C1P2 1:15:45.
- **Partes de una red.** Capa de entrada (una "neurona" por dato, sin pesos), capas ocultas y capa de salida C2P1 2:22, C2P1 1:55:38.
- **Arquitecturas** C2P1 5:14: perceptrón simple; multicapa hacia adelante (sin conexiones hacia atrás); convolucionales, con una ventana que recorre la entrada; recurrentes, donde el estado anterior influye en el siguiente C2P1 8:05.
- **Tipos de aprendizaje** C2P1 11:25, C2P1 13:21, C2P1 13:33: supervisado (corrección de errores, retropropagación); no supervisado (hebbiano, competitivo, se ve en la materia siguiente); por refuerzo (el videojuego donde solo sabés que algo salió mal cuando el personaje muere).
- **Activaciones** C2P1 19:59, C2P1 22:50, C2P1 1:05:28: escalón, sigmoide (de 0 a 1), tangente hiperbólica (de −1 a 1, transición más abrupta) y ReLU = max(0, x), que Diego compara con un diodo rectificador.
- **TensorFlow Playground** C2P1 23:24, C2P1 26:37: una neurona separa datos lineales pero no aprende el XOR; con capas ocultas y ReLU sí. Si sacás una neurona que "no pesaba", a veces deja de funcionar. Se pueden agregar entradas como x₁², x₁·x₂ o seno. Diseñar redes "tiene mucho de prueba y error y de artístico" C2P1 31:00, C2P1 37:36.
- **Curvas de pérdida.** Si la pérdida de validación sube mientras la de entrenamiento baja, hay sobreajuste C2P1 35:21. Los sesgos también se aprenden C2P1 37:06.
- **Softmax** para multiclase: convierte las salidas en un vector de probabilidades C2P1 38:17.
- **Descenso por el gradiente.** La regresión logística no tiene solución cerrada; se minimiza la función de costo con métodos numéricos que bajan en la dirección del gradiente y pueden quedar en mínimos locales C2P1 42:40, C2P1 43:15. En una página de visualización de optimizadores (cuál, **para verificar**) se ve que con una tasa grande diverge y con una chica no avanza C2P1 47:06.
- **Backpropagation** (década de 1980): calcula las derivadas parciales de la pérdida respecto de cada peso con la regla de la cadena, de la salida hacia la entrada C2P1 54:13.
- **Por qué volvieron las redes.** Quedaron relegadas en los 90 y 2000; volvieron por las GPU baratas gracias a los videojuegos y por los datos de internet y los celulares C2P1 58:48.

### Correcciones y matices
- **Corrección:** "las recurrentes son predecesoras de los Transformers; ChatGPT, Gemini y Claude usan este tipo de redes recurrentes" C2P1 8:05. Los Transformers (Vaswani y otros, 2017) reemplazaron la recurrencia por atención; los LLM actuales no son recurrentes. Algo parecido dice Karim en C2P2 1:08:50 ("las convolucionales mezcladas con las recurrentes son la base de los Transformers").
- **Corrección:** las "redes de bases radiales" descriptas como "cada neurona conectada con todas las demás, no supervisadas, que evolucionan hasta estabilizarse" C2P1 9:31 son en realidad las redes de **Hopfield**. Las redes de funciones de base radial (RBF) son redes hacia adelante con una capa oculta de funciones radiales, entrenadas en forma supervisada.
- **Corrección:** "ReLU compara x con 0 y me da el máximo, o sea, es cero o es uno" C2P1 22:50. ReLU devuelve x si es positivo y 0 si no; no devuelve 1. Diego lo dice bien en C2P1 1:05:28.
- **Corrección:** la sigmoide "tiene el área bajo la curva igual a uno, se parece a una distribución de probabilidad" C2P1 23:42, C2P1 1:06:32, y la tangente hiperbólica "también tiene la integral 1" C2P1 1:08:42. La sigmoide va de 0 a 1 (es la función de distribución acumulada de la logística) y su integral sobre toda la recta es infinita; la tanh va de −1 a 1. La salida de la sigmoide se interpreta como probabilidad por cómo se entrena el modelo (entropía cruzada), no por un área.
- **Matiz:** "regresión softmax... valores entre −1 y 1... se calcula el jacobiano" C2P1 38:17. Softmax da valores entre 0 y 1 que suman 1; entre −1 y 1 es la tanh.
- **Matiz:** "el descenso de gradiente estocástico hace el paso en forma estocástica" C2P1 43:15. SGD estima el gradiente con un minilote al azar; la dirección sale de ese gradiente.
- **Corrección:** "la tasa se suele ir achicando; eso se llama simulated annealing" C2P1 50:51. Achicar la tasa es un *learning rate schedule* (decaimiento). El recocido simulado es otro algoritmo de optimización, que acepta pasos peores con cierta probabilidad.
- **Matiz:** "cada peso es un número real de 64 bits" C2P1 2:22. En redes se usa casi siempre float32, y float16 u 8 bits al desplegar.
- **Matiz:** las redes no desaparecieron del todo en los 90: las convolucionales de LeCun leían cheques C2P1 58:48.
- **dudoso:** "modelo tradicional de Schrbel" C1P2 1:12:20: nombre deformado; puede ser el diagrama de Rosenblatt o el de McCulloch y Pitts.
- **Matiz:** "son sistemas caóticos en sentido físico" C1P2 1:13:28. Lo que quiere decir es que el resultado es sensible a la semilla y a la inicialización.

### Preguntas de repaso
1. ¿Por qué un perceptrón no aprende el XOR y qué cambia al agregar una capa oculta?
2. ¿Qué valores devuelve ReLU para −2, 0 y 3? ¿Y la sigmoide para 0?
3. ¿Qué pasa si la tasa de aprendizaje es demasiado grande? ¿Y demasiado chica?
4. ¿Qué calcula backpropagation y qué regla matemática usa?
5. ¿Qué diferencia hay entre una red de Hopfield y una red RBF?

---

## 6. Redes en la práctica: scikit-learn, Keras, sobreajuste, regularización y dropout
**Dónde:** C2P1 1:02:06, C2P1 1:09:18, C2P1 1:11:28, C2P1 1:14:54, C2P1 1:16:37, C2P1 1:22:23, C2P1 1:27:39, C2P1 1:29:12, C2P1 1:31:15, C2P1 1:34:54, C2P1 1:39:22, C2P1 1:42:07, C2P1 1:48:18, C2P2 0:20, C2P2 3:05, C2P2 4:17, C2P2 6:30, C2P2 10:25, C2P2 11:29, C2P2 13:46, C2P2 15:55, C2P2 18:30, C2P2 21:00, C2P2 23:54, C2P2 26:10, C2P2 27:18, C2P2 28:24, C2P2 31:48, C2P2 33:33, C2P2 34:44, C2P2 36:27, C2P2 39:42, C2P2 41:05, C2P2 42:32, C2P2 44:43

### Conceptos clave
- **Frameworks** C2P1 1:02:06: scikit-learn para aprender (didáctico), Keras sobre TensorFlow (Google) y PyTorch (Meta).
- **Gato o no gato.** Una imagen es un arreglo de píxeles: 64 × 64 × 3 = 12.288 entradas, que se normalizan de 0 a 255 a 0 a 1 C2P1 1:09:18, C2P1 1:11:28, C2P1 1:12:28. Hay que curar los datos (el "gato" Dumas, el cocinero, no es un gato).
- **MLPClassifier** con `solver="sgd"`, `learning_rate_init=0.001`, `batch_size=20`, `max_iter=1000` y `hidden_layer_sizes=(5,)` C2P1 1:14:54. El tamaño de lote existe porque 2000 imágenes no entran juntas en memoria C2P1 1:16:37; una época es una pasada por todos los datos. `verbose` muestra la pérdida en cada iteración para monitorear C2P1 1:22:23.
- **Parámetros.** 61.451: cada una de las 5 neuronas recibe los 12.288 píxeles (12.288 × 5 + 5 = 61.445) y la salida suma 5 + 1 C2P1 1:27:39, C2P1 1:48:18, C2P1 1:55:38. Verificado en el box.
- **Parada temprana.** Se detuvo en la iteración 419 porque pasaron 10 épocas sin mejora (`n_iter_no_change=10`) C2P1 1:31:15. Entrenamiento 94%, test 68%: sobreajuste C2P1 1:32:34, C2P1 1:34:54.
- **Qué hace una red por dentro.** Las primeras capas llevan los datos a un espacio donde la última capa separa linealmente, "como un kernel que se modela con los datos" C2P1 1:42:07. Detección de anomalías: entrenar solo con los casos sanos C2P1 1:39:22.
- **Keras.** `Sequential` con `Dense(5, relu)` con regularización L2 y `Dense(1, sigmoid)`, `compile` con SGD, `binary_crossentropy` y `accuracy`, `summary` con los mismos 61.451 parámetros C2P1 1:48:18. `fit` con `batch_size`, épocas y `validation_data` C2P2 0:20. Desde la época 432 el entrenamiento llega a 1,0 y la validación se estanca C2P2 4:17. `history` para graficar y TensorBoard C2P2 5:58.
- **Checkpoints y callbacks.** Si se corta la luz a las 4 horas y media de un entrenamiento de 5, Keras puede haber guardado el estado y quedarse con la mejor época C2P2 3:05. Conviene guardar cada 100 o 1000 épocas, porque escribir a disco suma tiempo C2P2 41:05.
- **Evaluar.** `evaluate` en test, `predict` devuelve la salida de la sigmoide y vos elegís el umbral ("decime que es gato si estás 90% seguro") C2P2 6:30, C2P2 10:25. `classification_report` y matriz de confusión: accuracy de test 74% C2P2 11:29, C2P2 12:02.
- **MNIST.** Dígitos manuscritos, 28 × 28 = 784 píxeles, 60.000 de entrenamiento; one hot con `to_categorical` C2P2 13:46, C2P2 15:55, C2P2 17:43. Red `Dense(256)`, ReLU, `Dropout`, `Dense(256)`, ReLU, `Dropout`, `Dense(10, softmax)`, unos 270.000 parámetros, Adam y 10 épocas: 95% en entrenamiento y 96% en validación C2P2 21:00, C2P2 23:54, C2P2 26:10. La validación queda por encima porque el dropout solo actúa al entrenar (en el box, con 2 épocas: entrenamiento 0,959 y validación 0,974).
- **Chequeo de sanidad.** Antes de entrenar con todo, sobreajustá un subconjunto chico hasta pérdida casi cero: si no lo logra, hay un error C2P2 27:18.
- **Decidir.** Un 3 puede tener probabilidad no nula de 2 y de 8; quedarte con el máximo es una decisión con responsabilidad C2P2 29:33. Las redes densas exigen tamaño fijo de imagen C2P2 31:16.
- **Problemas de entrenamiento (Karim)** C2P2 31:48, C2P2 33:33: entrenamiento, validación y test con la misma estructura que la población (estratificar). Sesgo y varianza con la diana C2P2 34:44. Subajuste: agrandar la red, cambiar la tasa o las activaciones; sobreajuste: más datos, regularización o cambiar la arquitectura C2P2 36:27. Empezar con una parte homogénea del dataset C2P2 39:42.
- **Regularización L2.** Suma a la pérdida el cuadrado de los pesos: penaliza los grandes. Se usa el cuadrado porque es derivable, "más amable matemáticamente" C2P2 42:32.
- **Dropout.** Bien explicado por Juan: forzar a la red a aprender en condiciones más difíciles C2P2 18:55.

### Correcciones y matices
- **Corrección:** "usar cinco neuronas, cinco capas ocultas" C2P1 1:14:54. `hidden_layer_sizes=(5,)` es **una** capa oculta de 5 neuronas (en el box: `n_layers_` = 3, contando entrada y salida). El valor por defecto es `(100,)` con ReLU y Adam.
- **Corrección:** "la capa de salida tiene dos neuronas, una para gato y otra para no gato" C2P1 1:29:12. En binario, `MLPClassifier` usa una sola neurona logística (`n_outputs_` = 1, `out_activation_` = "logistic"); `predict_proba` arma las dos columnas como p y 1 − p (verificado en el box).
- **Matiz:** "el método más común es Newton Raphson" C2P1 1:19:22. Los solvers de `MLPClassifier` son "lbfgs", "sgd" y "adam" (por defecto); Newton Raphson casi no se usa en redes.
- **Corrección:** "Facebook logró detección de rostros con 99,99 contra 99,98 del ojo humano" C2P1 1:33:15. DeepFace (2014) llegó a 97,35% en el benchmark LFW contra 97,53% humano: casi igual, no mejor. Y era verificación de rostros, no detección.
- **Corrección:** "un estudio de Stanford: 98% en hombres blancos y 3% en mujeres negras; decía que eran animales" C2P1 1:36:02. Mezcla dos casos: Gender Shades (Buolamwini y Gebru, MIT Media Lab, 2018), con error de hasta 34,7% en mujeres de piel oscura, y Google Photos, que en 2015 etiquetó a personas negras como gorilas.
- **Corrección:** "el vector de soporte, o sea, la cantidad de imágenes" C2P2 11:29. El *support* del `classification_report` es la cantidad de ejemplos reales de cada clase; no tiene nada que ver con los vectores de soporte.
- **Corrección:** "una sola imagen me demora 27 minutos" C2P2 11:09: son milisegundos.
- **Corrección:** Diego: "dropout es apagar neuronas que no aportan nada, la saco, y consigo modelos más chicos", y "cuando uno hace dropout tiene que volver a entrenar" C2P2 18:30, C2P2 18:55. Eso es poda (pruning). El dropout apaga **al azar** una fracción p de neuronas en cada paso de entrenamiento, distinta en cada minilote, dentro del mismo entrenamiento, y en inferencia usa todas: el modelo no se achica.
- **Corrección:** Karim: dropout "cada cierto número de épocas elimina una proporción de neuronas y se sigue entrenando; se va sacando de las que quedan un 10% o 5%" C2P2 44:43. No es acumulativo ni se eliminan neuronas: en cada paso se apagan al azar y en el siguiente vuelven. En el box: la capa `Dropout(0.5)` en entrenamiento pone ceros y multiplica el resto por 2; en inferencia devuelve la entrada sin cambios.
- **Matiz:** "la regularización les pone tope a los pesos" C2P2 44:43. L2 los penaliza; un tope duro es otra técnica (max norm).
- **Corrección:** "el máximo está en la posición siete, entonces el número sería un seis porque arrancamos del índice cero" C2P2 28:24. En MNIST el índice 0 es el dígito 0, así que argmax 7 es el dígito 7 (verificado en el box).
- **Matiz:** "65.000 y pico" pesos con `get_weights` C2P2 6:30; el summary decía 61.451.
- **dudoso:** "se puede sobreentrenar solamente por pasar los datos una vez" C2P2 31:48. Con una sola pasada es raro sobreajustar; no queda claro qué quiso decir.
- **Matiz:** en la diana de sesgo y varianza, Karim prefiere "el que clasifica mal pero con poca variabilidad, porque podría desplazarlo" C2P2 34:44. Es una opinión: un sesgo constante se puede corregir, pero en general se busca un equilibrio.

### Preguntas de repaso
1. ¿Cuántos parámetros tiene una capa `Dense(5)` que recibe 12.288 entradas? ¿Por qué?
2. ¿Por qué la accuracy de validación puede quedar arriba de la de entrenamiento cuando usás dropout?
3. ¿Qué diferencia hay entre dropout y poda?
4. ¿Para qué sirve sobreajustar a propósito un subconjunto chico al principio?
5. Nombrá dos remedios para el subajuste y dos para el sobreajuste.

---
## 7. Redes convolucionales y transfer learning
**Dónde:** C2P2 49:15, C2P2 49:54, C2P2 50:30, C2P2 52:08, C2P2 53:53, C2P2 54:27, C2P2 56:08, C2P2 1:00:00, C2P2 1:01:36, C2P2 1:04:14, C2P2 1:06:34, C2P2 1:07:09, C2P2 1:09:24, C2P2 1:11:00, C2P2 1:12:05, C2P2 1:13:49, C2P2 1:16:57, C2P2 1:19:41, C2P2 1:24:43, C2P2 1:26:19, C2P2 1:29:29, C2P2 1:31:04, C2P2 1:31:44, C2P2 1:34:29, C2P2 1:36:05, C2P2 1:37:15, C2P2 1:38:21, C2P2 1:41:05, C3P2 13:38

### Conceptos clave
- **Por qué no alcanzan las densas.** Una imagen de 224 × 224 × 3 tiene 150.528 valores; con 1000 neuronas en la primera capa serían 150 millones de pesos C2P2 52:08. Además las densas ignoran la estructura espacial y no aprovechan patrones que se repiten C2P2 53:53.
- **Convolución.** Un filtro (máscara o kernel) de, por ejemplo, 3 × 3 recorre la imagen y detecta bordes, degradés o texturas; sus pesos se comparten en todas las posiciones C2P2 54:27, C2P2 1:01:36. Sirve para datos con correlación espacial o temporal: imágenes, audio, video, series C2P2 56:08.
- **Estructura típica** C2P2 1:00:00: convolución, pooling, otra convolución, otro pooling, aplanado (`Flatten`) y capas densas para clasificar. Las primeras capas aprenden bordes y texturas; las siguientes, partes (manchas, narices, caras) C2P2 50:30, C2P2 1:04:14.
- **Ventajas y desventajas** C2P2 1:07:09: pesos compartidos, detectan el patrón en cualquier lugar y extraen características solas; pero necesitan muchos datos, son sensibles a perturbaciones adversariales y son poco interpretables.
- **Redes famosas** C2P2 1:09:24: LeNet (1998), AlexNet (GPU), VGG (muchas capas simples) y ResNet (conexiones residuales). Aplicaciones: tumores, autos autónomos, industria, seguridad C2P2 1:11:00.
- **Kernels clásicos de procesamiento de imágenes** con scikit-image (Diego): identidad, desenfoque, bordes, enfoque, relieve, Sobel, Laplace, esquinas C2P2 1:13:49. El detector de esquinas sirve para emparejar imágenes y seguir objetos C2P2 1:19:41.
- **Fashion MNIST** C2P2 1:26:19, C2P2 1:28:28, C2P2 1:29:29: 28 × 28, 10 clases, 60.000 y 10.000 imágenes; normalizar y agregar el canal; `Conv2D` con ReLU, `MaxPooling2D` 2 × 2, otra `Conv2D` y otro pooling, `Flatten`, `Dense(128)`, `Dense(10)`. `EarlyStopping`, lotes de 64 y 90% en test C2P2 1:31:44. La remera se confunde con la camisa C2P2 1:34:29.
- **Parámetros no entrenables:** son las capas congeladas, que es lo que se hace en transfer learning C2P2 1:31:04.
- **Data augmentation.** Con pocos datos, rotar, hacer zoom, desplazar, invertir, agregar ruido o desenfocar; las imágenes aumentadas tienen que ser posibles en la realidad C2P2 1:36:05. `Dropout(0.25)` en la CNN; con una red chica un 25% puede ser mucho C2P2 1:37:15.
- **Transfer learning.** Tomar una red entrenada con millones de imágenes (AlexNet, ResNet, MobileNet, que tiene unos 2.250.000 parámetros y pesa 8 MB) y adaptarla a tu problema C2P2 1:38:21. Si el propósito es el mismo, no hace falta reentrenar C2P2 1:43:05. La analogía de Diego: si sabés manejar un Corolla, manejar un Etios es fácil; una moto, no tanto C3P2 13:38.

### Correcciones y matices
- **Corrección:** "las convolucionales son bastante modernas, son del 2017" C2P2 49:54. El Neocognitron es de 1980, LeNet de 1989 y 1998, AlexNet de 2012; 2017 es el año del Transformer. La propia Karim dice después "LeNet, 98" C2P2 1:09:24.
- **Matiz:** "todas las conexiones desde la matriz tienen el mismo peso" C2P2 54:27. El filtro se comparte en todas las posiciones, pero dentro del filtro cada peso es distinto.
- **Matiz:** "pooling, que detecta los patrones que se repiten" C2P2 1:00:00. El pooling reduce la resolución (máximo o promedio) y da algo de invariancia a pequeños desplazamientos.
- **Corrección:** "flattening elimina los valores muy altos o muy bajos, homogeneiza" C2P2 1:06:34. `Flatten` solo aplana el tensor a un vector. Diego lo explica bien al armar la red C2P2 1:29:29.
- **Corrección:** ResNet "tiene unos 5 o 6 años", con conexiones residuales "para ver qué pasa con lo que se elimina" C2P2 1:09:24. ResNet es de 2015 (unos 11 años). Las conexiones residuales suman la entrada del bloque a su salida, y así el gradiente fluye y se pueden entrenar redes muy profundas.
- **Matiz:** las CNN "exigen tamaño fijo" C2P2 1:12:05. Con pooling global al final pueden aceptar tamaños variables; igual en la práctica se estandariza.
- **Matiz:** la convolución matemática invierte el filtro C2P2 1:16:57; las CNN calculan en realidad la correlación cruzada, sin invertir. Da lo mismo porque el filtro se aprende.
- **Corrección:** "hasta 2010 o 2012 se ponían capas de convolución y a la salida SVM; AlexNet propuso aprender también los pesos de los kernels" C2P2 1:24:43. LeNet ya aprendía los filtros con backpropagation en 1989 y 1998. Lo que se combinaba con SVM eran descriptores hechos a mano (SIFT, HOG) o Fisher vectors. AlexNet escaló el aprendizaje de filtros con GPU y ganó ImageNet 2012.
- **para verificar:** el summary de la CNN de Fashion MNIST da "total 250.000" C2P2 1:29:29. En el box, con 32 y 64 filtros de 3 × 3 sin relleno, da 225.034 (320 + 18.496 + 204.928 + 1.290); con relleno "same" da 421.642. La cantidad de filtros de la notebook no se lee en el video.
- **para verificar:** la data augmentation usa `ImageDataGenerator` C2P2 1:36:05. En Keras 3.15.1 ya no existe (ni en `keras.preprocessing.image` ni en `legacy`); hay que usar capas como `RandomFlip` y `RandomRotation`. Puede seguir andando en el `tf.keras` de Colab según la versión instalada.
- **dudoso:** "CNN básica 90%, con regularización 0,8" C2P2 1:37:15: puede ser 0,88.
- **Corrección:** "en transfer learning se mantienen fijos los pesos internos y se reentrenan la capa de entrada y la de salida" C2P2 1:41:05, y Diego: "solo tengo que entrenar la primera capa y la última" C3P2 13:38. Se congela la base entera (las capas convolucionales, incluidas las primeras, que detectan bordes genéricos) y se entrena una cabeza nueva al final. En el fine tuning se descongelan además las últimas capas de la base con una tasa baja. La capa de entrada no se reentrena.

### Preguntas de repaso
1. ¿Cuántos parámetros tiene una `Conv2D(32, 3×3)` sobre una imagen de un canal? ¿Y si la imagen fuera de 256 × 256?
2. ¿Qué hace el pooling y qué hace `Flatten`?
3. ¿Qué capas congelás en transfer learning y por qué esas?
4. Dá un ejemplo de data augmentation que no tenga sentido para Fashion MNIST.

---

## 8. Redes recurrentes y LSTM
**Dónde:** C3P1 2:37, C3P1 4:52, C3P1 8:11, C3P1 12:11, C3P1 13:49, C3P1 14:55, C3P1 19:21, C3P1 27:13, C3P1 29:33, C3P1 30:34, C3P1 32:51, C3P1 39:17, C3P1 42:00, C3P1 43:07, C3P1 44:12, C3P1 46:20, C3P1 47:29, C3P1 48:39, C3P1 52:37, C3P1 54:21, C3P1 1:00:12, C3P1 1:01:32, C3P1 1:04:14, C3P1 1:05:27, C3P1 1:11:32, C3P1 1:14:18, C3P1 1:18:16, C3P1 1:19:01, C3P1 1:22:10

### Conceptos clave
- **Qué es una RNN.** Un modelo para información secuencial con memoria interna: el estado oculto h_t comprime la historia de lo que leyó ("La película no estuvo buena") C3P1 2:37, C3P1 4:52. La ecuación: h_t = f(W_x·x_t + W_h·h_{t−1} + b) C3P1 8:11. Lo viejo se va desvaneciendo.
- **Entrenamiento.** Backpropagation en el tiempo: se desenrolla la red a lo largo de la secuencia; pide mucha memoria y conviene GPU C3P1 12:11, C3P1 20:31.
- **Tokens.** La unidad puede ser palabra, subpalabra ("hiper" y "flujo"; "cónclave" como "con" y "clave") o letra C3P1 13:49, C3P1 19:21. Tokenizar es pasar texto a IDs numéricos ("la" = 45, "película" = 81) y después a vectores C3P1 27:13. La salida puede ser el próximo token (generación) o una clase C3P1 29:33.
- **Tipos** C3P1 14:55: uno a uno; uno a muchos (describir una imagen); muchos a uno (sentimiento, diagnóstico, fraude); muchos a muchos (traducción, subtitulado).
- **Limitación.** Les cuesta la memoria a largo plazo C3P1 42:00. La LSTM la mejora con compuertas C3P1 43:07. Diego aclara que no es especialista en recurrentes y que sirven para entender por qué funcionan los Transformers C3P1 39:17.
- **Notebook en Keras.** `Embedding` + `SimpleRNN(32)` con vocabulario de 10.000 palabras C3P1 44:12, C3P1 45:16. Parámetros que calcula Manuel: Embedding 320.000 (10.000 × 32), SimpleRNN 2.080 (32 × 32 + 32 × 32 + 32), y apilando cuatro capas recurrentes 328.320 C3P1 46:20, C3P1 47:29. Verificado en el box. `return_sequences=True` hace falta para apilar.
- **IMDB.** 25.000 críticas de entrenamiento y 25.000 de prueba, vocabulario de 10.000, largo máximo 500 C3P1 48:39. Modelo muchos a uno: `Embedding` + `SimpleRNN` + `Dense(1, sigmoid)`, `binary_crossentropy`, 10 épocas, `validation_split=0.2` C3P1 52:37, C3P1 54:21. Si falta memoria, dividí el batch por dos C3P1 50:57.
- **Resultados.** SimpleRNN: 99% en entrenamiento y 85% en validación, sobreajuste C3P1 1:00:12. LSTM(32): 8.320 parámetros y 89% en validación, menos sobreajuste C3P1 1:01:32, C3P1 1:04:14.
- **Predecir una crítica nueva.** Pasar las palabras a índices con el diccionario del dataset, rellenar a 500, `predict` y elegir el umbral (50% es una decisión tuya) C3P1 1:05:27. Una crítica negativa salió positiva y una mixta 95% positiva C3P1 1:14:18: hay doble subjetividad, en la crítica y en la etiqueta C3P1 1:18:16.
- **Versiones.** A Manuel no le encuentra `word_index`; Diego usa Keras 3.14.1 y otro alumno 3.13. Moraleja: entornos virtuales o Docker C3P1 1:11:32.
- **Embeddings.** Textos parecidos quedan cerca; también existen GRU y capas bidireccionales C3P1 1:22:10.

### Correcciones y matices
- **Corrección:** "a medida que pasan las palabras se van modificando los pesos internos de esta red" C3P1 4:52, y la respuesta a María C3P1 9:17. En inferencia los pesos están fijos; lo que cambia con cada palabra es el estado oculto (las activaciones). Los pesos solo cambian al entrenar.
- **Matiz:** "tenemos una red por cada instancia de tiempo" C3P1 12:11 y "cinco tokens, cinco redes a entrenar" C3P1 26:07. Es la misma red con los mismos pesos aplicada en cada paso; lo que se guarda por paso son las activaciones. Manuel lo dice bien: "las RNN comparten pesos" C3P1 47:29.
- **Corrección:** ante la pregunta de Gonzalo, Karim dice que "ChatGPT va generando un reentrenamiento en vivo, cambia sus pesos para darnos más de lo que queremos" C3P1 30:34. ChatGPT no cambia sus pesos en una conversación: usa el contexto de la charla y, si está activada, una memoria guardada como texto que se agrega al prompt. La intuición de Gonzalo (los pesos se ajustan solo al entrenar) era la correcta.
- **Corrección:** "el año pasado los LLM con redes recurrentes se perdían a mitad de oración" C3P1 16:05 y "los LLM cuando surgieron se olvidaban de los primeros párrafos" C3P1 32:51. Los LLM y los generadores de video de los últimos años son Transformers (o modelos de difusión); esos errores vienen de la ventana de contexto y de la coherencia, no de la recurrencia.
- **Matiz:** el ejemplo de una memoria de 16 posiciones que no puede responder por la posición 24 C3P1 32:51. Una RNN simple no tiene una ventana dura: olvida por el desvanecimiento. La ventana fija de N tokens es propia de los Transformers. Lo mismo con "este sistema tiene un millón de tokens" C3P1 19:21: eso es la ventana de contexto.
- **Matiz:** "la LSTM tiene una estructura muy sencilla, entra en microcontroladores" C3P1 43:07. Es más compleja que la RNN simple: 4 compuertas y 4 veces más parámetros.
- **Corrección:** "fíjense cómo bajó la cantidad de parámetros" C3P1 1:01:32. Subió: la LSTM tiene 8.320 contra 2.080 de la SimpleRNN.
- **Matiz:** "no escala lineal porque las RNN comparten pesos" C3P1 47:29. Con capas iguales escala lineal (2.080 por capa); lo que se comparte entre pasos de tiempo hace que no dependa del largo de la secuencia.
- **Matiz:** el `Embedding` "lleva los textos al espacio tokenizado" C3P1 44:12. Convierte IDs de tokens en vectores densos; la tokenización es un paso previo.
- **Matiz:** "lo ideal sería entrenar con todo de una" C3P1 55:55. Los minilotes además agregan ruido que ayuda a generalizar.
- **para verificar:** la función para el diccionario es `keras.datasets.imdb.get_word_index()`, que existe en Keras 3.15.1 (verificado en el box) C3P1 1:11:32.
- **para verificar:** Federico pregunta cómo ver qué palabras pesaron más y la respuesta es "hay herramientas" C3P1 1:19:01, sin nombrarlas (por ejemplo Integrated Gradients, SHAP o LIME). También la notebook sale "de un repositorio con libro" que no se nombra C3P1 1:24:00.
- **Sugerencia:** en el box, con 5000 críticas, largo 200 y solo 3 épocas, la SimpleRNN llega a 0,61 en test y la LSTM a 0,80. Con tan pocas épocas no se ve el sobreajuste de la clase, pero sí que la LSTM aprende mucho mejor las dependencias largas (a cambio de tardar unas 10 veces más en CPU).

### Preguntas de repaso
1. ¿Qué cambia de un paso al otro en una RNN durante la inferencia: los pesos o el estado?
2. Calculá los parámetros de `SimpleRNN(64)` sobre embeddings de 32. ¿Y de `LSTM(64)`?
3. ¿Por qué hace falta `return_sequences=True` para apilar dos capas recurrentes?
4. ¿Por qué ChatGPT "recuerda" lo que le dijiste antes en la misma conversación?

---

## 9. Transformers y fine tuning
**Dónde:** C3P1 1:24:43, C3P1 1:25:50, C3P1 1:27:31, C3P1 1:28:41, C3P1 1:30:52, C3P1 1:32:32, C3P1 1:34:44, C3P1 1:36:31, C3P1 1:37:37, C3P1 1:38:10, C3P1 1:40:59, C3P1 1:43:23, C3P1 1:44:29, C3P1 1:45:38, C3P1 1:46:11, C3P1 1:46:44, C3P1 1:47:18, C3P1 1:48:58, C3P1 1:49:32, C3P2 1:34, C3P2 3:16, C3P2 4:23, C3P2 7:07, C3P2 8:48, C3P2 10:19, C3P2 11:34, C3P2 13:10, C3P2 18:09, C3P2 19:48, C3P2 20:51, C3P2 23:02, C3P2 25:17, C3P2 26:27, C3P2 28:35, C3P2 30:19

### Conceptos clave
- **Origen.** "Attention Is All You Need", Ashish Vaswani y su equipo de Google, 2017 C3P1 1:24:43. Resuelve tres problemas de las RNN: dependencias largas, procesamiento no paralelizable y memoria C3P1 1:25:50.
- **Autoatención.** Cada palabra mira a todas las demás para decidir a qué se refiere: en "el gato cruzó el patio porque estaba cansado / inundado", "estaba" apunta al gato o al patio C3P1 1:27:31.
- **Q, K y V** (María, que acaba de entregar su tesis): la consulta (qué busco), la clave (qué ofrezco) y el valor (el contenido), con la analogía de la biblioteca C3P1 1:28:41. La fórmula es softmax(Q·Kᵀ / √d_k)·V: similitud, escalado para que no explote y softmax C3P1 1:30:52.
- **Multi head.** Varias atenciones en paralelo, cada una puede capturar relaciones distintas C3P1 1:32:32.
- **Arquitectura** C3P1 1:34:44, C3P1 1:38:10, C3P1 1:40:59, C3P1 1:43:23: embeddings más positional encoding ("vivir en la calle del medio" no es "vivir en el medio de la calle"), encoder con multi head attention, feed forward, conexiones residuales ("la salida es la entrada más la transformación; permite entrenar redes muy profundas") y normalización; decoder que genera paso a paso ("I love science").
- **Ventajas y desventajas** C3P1 1:44:29, C3P1 1:46:11, C3P1 1:48:58: contexto global y escalado con datos y parámetros; pero piden GPU, energía y muchos datos, y son poco interpretables (en salud piden "¿dónde ves el tumor?"). Aplicaciones: texto, imágenes, audio, video, proteínas, código C3P1 1:45:38.
- **RNN contra Transformer** C3P1 1:49:32: la RNN es secuencial, tiene estado oculto y olvida; el Transformer es paralelo, con atención global, y domina el lenguaje natural.
- **Notebook de fine tuning (Diego, PyTorch y Hugging Face).** TensorFlow nació para desplegar en la nube y Torch para lo académico; hoy los dos están en la industria C3P2 1:34. Colab con GPU C3P2 3:50. IMDB con la librería `datasets`: 25.000 + 25.000 y 50.000 sin etiqueta C3P2 4:23; la mayoría de las críticas tiene entre 100 y 150 palabras C3P2 7:07. Tokenizador de DistilBERT, "versión destilada de BERT": `input_ids`, `attention_mask`, `decode`, `convert_ids_to_tokens` C3P2 8:48, C3P2 10:19. Subconjunto al azar de 3000 críticas de entrenamiento y 1000 de test C3P2 13:10.
- **Modelo y entrenamiento.** `AutoModelForSequenceClassification` con 2 etiquetas: embeddings de palabra y de posición, LayerNorm, dropout 0,1, capas Transformer y un clasificador lineal C3P2 18:09. `compute_metrics` con argmax C3P2 19:48. `TrainingArguments` (carpeta, evaluación y guardado por época, tasa, batch, épocas) y `Trainer.train()` en vez de `fit` C3P2 20:51. Con 2 épocas: pérdida 0,39 y accuracy 0,87 C3P2 25:17; matriz de confusión 429, 83, 44 y 444 C3P2 26:27.
- **Discusión final** C3P2 28:35, C3P2 30:19: energía, sesgos lingüísticos, alucinaciones y datos masivos con basura.

### Correcciones y matices
- **Matiz:** "atención autorregresiva" C3P1 1:24:43. El mecanismo es autoatención (self attention); autorregresivo es la forma de generar del decoder, token a token.
- **Corrección:** "con las RNN había que procesar todo en el orden inverso" C3P1 1:25:50. Se procesan en el orden de entrada (existen variantes bidireccionales).
- **dudoso:** "para relacionar una con dos palabras necesitaríamos más dimensiones" C3P1 1:30:52. La matriz de atención ya relaciona todos los tokens con todos; con varias capas se componen relaciones más complejas.
- **Matiz:** "la primera cabeza se fija las relaciones gramaticales, la segunda las referencias" C3P1 1:32:32. Es una ilustración: nadie programa qué mira cada cabeza; emerge del entrenamiento y solo a veces se puede interpretar así.
- **Corrección:** palabras similares quedan cerca "con una distancia de Hamming" C3P1 1:36:31. Para embeddings se usa similitud coseno o distancia euclídea; Hamming es para cadenas binarias.
- **Corrección:** la dimensión de los embeddings "depende del tamaño del diccionario; 256, 1024, siempre potencias de dos" C3P1 1:37:37. No depende del vocabulario. El Transformer original usa 512, BERT base y DistilBERT 768 (verificado en la configuración de DistilBERT en el box) y GPT 3 12.288; las dos últimas no son potencias de dos.
- **Corrección:** la conexión residual "para conceptos muy importantes puede saltear varias capas dándole mayor peso" C3P1 1:40:59. Se suma siempre, para todos los tokens; no elige conceptos.
- **Corrección:** "Gemini o ChatGPT nos pueden ir mostrando las capas intermedias" C3P1 1:43:23. Lo que muestran es texto de razonamiento o la respuesta a medida que se genera, no las capas.
- **Matiz:** "no le pregunten a ChatGPT fórmulas matemáticas, para eso no funciona" C3P1 1:45:38. Opinión desactualizada: los modelos actuales resuelven bastante matemática, aunque hay que verificar.
- **Corrección:** "cuando le decimos a Gemini actuá como experto, la ventana de contexto aísla los datos de entrenamiento que sirven" C3P1 1:46:44. La ventana de contexto es la cantidad máxima de tokens que el modelo mira a la vez; un prompt de rol condiciona la generación, no aísla datos.
- **dudoso:** alucinaciones "porque se autoalimenta con las salidas", sistemas que "están soñando" C3P1 1:47:18. Mezcla la generación autorregresiva con el colapso de modelos al entrenar con datos sintéticos (Shumailov y otros, 2024).
- **Corrección:** "la velocidad de entrenamiento de la recurrente es menor porque no es un procesamiento secuencial" C3P1 1:50:39: lapsus, es menor porque sí es secuencial.
- **Corrección (verificado):** "si instalan transformers también se instala torch por defecto" C3P2 3:16. `pip install transformers` no instala torch (los requisitos de la 5.18 no lo incluyen); hay que instalarlo aparte o con `pip install "transformers[torch]"`. En Colab ya viene instalado, por eso no se nota.
- **Matiz:** "Google usó Bard, su ChatGPT, fracasó rotundamente" C3P2 8:48. Bard (2023) era un chatbot sobre LaMDA y PaLM, sin relación con BERT; se renombró Gemini en 2024. Lo de "fracasó" es opinión.
- **Corrección:** "una fuente de alucinación es que el modelo genera números que al detokenizar no tienen sentido" C3P2 11:34. Todo ID que genera el modelo corresponde a un token del vocabulario (en el box, los 30.522 IDs de DistilBERT se decodifican). La alucinación es contenido plausible pero falso.
- **Corrección:** los Vision Transformers "procesan de a pedacitos y relacionan cada uno con los vecinos que tiene al lado" C3P2 23:02. Se llaman parches (por ejemplo de 16 × 16) y la atención relaciona cada parche con **todos** los demás.
- **Matiz:** "si fueron entrenados con texto de X, puro odio" C3P2 30:19: opinión del docente.

### Preguntas de repaso
1. Explicá con tus palabras qué son Q, K y V y para qué se divide por √d_k.
2. ¿Por qué un Transformer necesita positional encoding y una RNN no?
3. ¿Qué hace la `attention_mask` del tokenizador?
4. ¿Qué capas se entrenan al hacer fine tuning de DistilBERT con `AutoModelForSequenceClassification`?
5. ¿Qué tenés que instalar además de `transformers` para correr el fine tuning en tu máquina?

---
## 10. Ensambles, árboles, bagging y random forest
**Dónde:** C3P2 32:05, C3P2 34:11, C3P2 35:52, C3P2 36:56, C3P2 38:45, C3P2 41:02, C3P2 44:51, C3P2 47:10, C3P2 49:57, C3P2 51:04, C3P2 52:43, C3P2 53:17, C3P2 55:03, C3P2 58:27, C3P2 1:00:42, C3P2 1:01:50, C3P2 1:03:25, C3P2 1:05:46, C3P2 1:09:56, C3P2 1:11:05, C3P2 1:13:48, C3P2 1:17:33

### Conceptos clave
- **Ensamble.** Varios modelos (árbol, Bayes, vecinos, SVM) votan y gana la mayoría C3P2 32:05. Conviene que se equivoquen en ejemplos distintos C3P2 35:52.
- **La cuenta.** Con 5 modelos independientes de 0,8 de acierto, la mayoría acierta con probabilidad 0,942 (exactamente 3, 4 o 5 aciertos: 0,2048 + 0,4096 + 0,32768 = 0,94208) C3P2 36:56. Verificado en el box.
- **Bagging.** El mismo modelo base entrenado con distintas muestras de los datos, y votación por mayoría, preferentemente con un número impar de modelos C3P2 38:45. Hay que apartar un test que ningún modelo vio C3P2 41:02.
- **Árboles de decisión.** Los nodos son reglas y las hojas clases; profundidad y mínimo de muestras por hoja controlan el sobreajuste; son caja blanca C3P2 47:10. El corte se elige comparando la entropía del nodo con la de los hijos C3P2 49:57, y se para por profundidad o cuando ya no se puede dividir C3P2 50:29.
- **Random forest.** Bagging de árboles en el que además se sortea un subconjunto de atributos, típicamente la raíz cuadrada del total (100 → 10) C3P2 51:04. Los árboles no se podan C3P2 52:43. Es fácil, tiene pocos hiperparámetros y es menos interpretable que un árbol solo C3P2 53:17.
- **Notebook (Diego).** `RandomForestClassifier` sobre el dataset de cáncer de mama (569 muestras, 30 atributos, maligno o benigno) C3P2 55:03. Un árbol solo da 100% en entrenamiento: sobreajuste C3P2 58:27. En oncología importa más no tener falsos negativos: elegí la métrica C3P2 1:00:42. "Cuando no sepan qué hacer, usen árboles": random forest es un buen modelo a vencer C3P2 1:01:50.
- **Hiperparámetros** C3P2 1:03:25: `n_estimators`, `criterion` ("gini" o "entropy"), `min_samples_leaf`, `max_features` ("sqrt" o "log2"), `max_depth` y `class_weight`. Es un metaestimador que promedia las probabilidades de los árboles.
- **Interpretación.** Graficar árboles del bosque: la raíz es "worst radius ≤ 16,8", con Gini y 228 muestras; el color más intenso es el nodo más puro C3P2 1:11:05. `feature_importances_`: worst radius, radio, concavidad y área C3P2 1:13:48.

### Correcciones y matices
- **Matiz:** "dos médicos con 5% de error: juntos 0,05 × 0,05" C3P2 34:11. Vale solo si los errores son independientes; en la práctica están correlacionados, que es justamente por qué después pide modelos que se equivoquen en ejemplos distintos.
- **Corrección:** en la cuenta de 0,942 dice que "se suman porque son probabilidades independientes" C3P2 36:56. Se suman porque son eventos mutuamente excluyentes (exactamente 3, 4 o 5 aciertos); la independencia es entre los modelos y sirve para calcular cada término.
- **Corrección:** bagging "entrena cada modelo con el 70% o el 80% al azar" C3P2 38:45 y "cada uno tendrá un 20% que no vio" C3P2 41:02. El bagging clásico (Breiman, 1996) toma muestras bootstrap del mismo tamaño n **con reemplazo**: cada muestra tiene alrededor de 63,2% de ejemplos únicos (en el box, 0,633) y deja afuera alrededor de 36,8% (out of bag), que sirve como validación. Sacar un porcentaje sin reemplazo se llama pasting.
- **Corrección:** "los árboles de decisión son muy inestables dependiendo del orden en el que van ingresando los datos" C3P2 44:51. Un árbol CART no depende del orden; es inestable porque cambia mucho ante pequeños cambios en los datos (alta varianza), y eso es lo que el bagging promedia.
- **Matiz:** "la idea es que todos los sistemas sean iguales o cada uno distinto" C3P2 45:57. En bagging el modelo base es el mismo; mezclar modelos distintos es voting o stacking.
- **Matiz:** "los árboles para regresión son bastante ineficientes" C3P2 47:10. Los árboles de regresión funcionan bien y son la base del gradient boosting.
- **Corrección:** "sistema de máxima entropía" para elegir el corte C3P2 49:57. Se llama **ganancia de información**: se elige el corte que más reduce la entropía (o el índice de Gini). "Máxima entropía" es otro concepto.
- **Corrección:** "para cada árbol elegimos 10, 15 o 20 atributos y armamos el árbol con esos" C3P2 51:04. En el random forest de Breiman y en scikit-learn el subconjunto de atributos se sortea **en cada división**, no una vez por árbol (al principio Karim lo dice bien).
- **Matiz:** no se poda "porque cada árbol tiene pocos datos" C3P2 52:43. No se poda porque árboles profundos tienen poco sesgo y el promedio baja la varianza.
- **Corrección:** random forest "fue publicado en 2008" C3P2 53:17. Breiman lo publicó en 2001.
- **Matiz:** con 15 y 20 árboles "bastante malo, más árboles no garantiza que sea más robusto, con un solo árbol había dado joya" C3P2 1:05:46. El 100% del árbol solo era en entrenamiento. En el box, promediando 5 semillas: 1 árbol 0,923, 5 árboles 0,936, 10 a 20 árboles 0,94 y 100 árboles 0,943. Con más árboles el resultado se estabiliza; las diferencias entre 10, 15 y 20 en un test chico son ruido del azar.
- **Corrección:** las importancias suman 1 "como la entropía, las probabilidades suman uno" C3P2 1:17:33. Cada importancia es la reducción media de impureza que aporta un atributo, sumada en todos los árboles y normalizada para que el total dé 1.

### Preguntas de repaso
1. ¿Por qué el ensamble de 5 modelos de 0,8 da 0,942 y qué supuesto hace falta?
2. ¿Qué diferencia hay entre bagging y pasting? ¿Qué es el error out of bag?
3. ¿En qué momento sortea atributos un random forest?
4. ¿Por qué no hace falta podar los árboles de un random forest?

---

## 11. Boosting, XGBoost y voting
**Dónde:** C3P2 1:18:42, C3P2 1:19:47, C3P2 1:20:51, C3P2 1:21:28, C3P2 1:22:37, C3P2 1:23:45, C3P2 1:27:06, C3P2 1:28:15, C3P2 1:28:50, C3P2 1:30:00, C3P2 1:30:34, C3P2 1:32:12, C3P2 1:33:58, C3P2 1:35:52, C4P1 0:34, C4P1 1:08, C4P1 2:15, C4P1 3:22, C4P1 4:28, C4P1 5:31, C4P1 6:45, C4P1 7:50, C4P1 9:31, C4P1 11:13, C4P1 12:14, C4P1 13:53, C4P1 15:38, C4P1 17:14

### Conceptos clave
- **Boosting.** Combinar clasificadores débiles en uno fuerte, entrenándolos en secuencia: cada uno corrige lo que el anterior hizo mal, con una jerarquía según el error (los cuatro médicos con distinta experiencia) C3P2 1:18:42, C3P2 1:20:51.
- **AdaBoost.** Los pesos de los ejemplos empiezan uniformes; cada clasificador tiene un peso α_t = ½·ln((1 − ε_t)/ε_t), y la predicción final es el signo de la suma ponderada C3P2 1:22:37. El ejemplo: ε = 0,30 da α = 0,42; ε = 0,21 da α = 0,65; el tercero α = 0,92 C3P2 1:23:45 (es el ejemplo clásico de Schapire; en el box: 0,424, 0,662 y un ε₃ de 0,137 para α = 0,92). La analogía del profesor que tiene razón contra la mayoría C3P2 1:26:00.
- **Tres sabores** C3P2 1:27:06, C3P2 1:28:15, C3P2 1:28:50: adaptativo (AdaBoost), por gradiente (gradient boosting, más lento, para clasificación y regresión) y por gradiente extremo (XGBoost).
- **Comparación** C3P2 1:30:00, C3P2 1:30:34: un gráfico donde boosting arranca peor que bagging y random forest y termina mejor (la fuente, **para verificar**). Ventajas: fácil, poco sesgo, eficiente. Desventajas: atípicos grandes, no es para tiempo real, muchos árboles.
- **Voting** C3P2 1:32:12, C3P2 1:33:58: hard (gana la mayoría) y soft. El ejemplo combina vecinos, SVM con C = 10 y RBF, una red con 3 o 4 capas ocultas y un árbol, y se puede pesar más a los que menos se equivocan con `weights`. Hay una demo web interactiva cuyo link no anda en el PDF y se pasa por el chat C3P2 1:35:52 (**para verificar** cuál es).
- **XGBoost (demo de Diego en C4P1).** Corre en Colab porque graficar el árbol le explota la memoria C4P1 0:34. Librería libre para Python, C++, R y Julia, con interfaz como scikit-learn; `XGBRegressor` y `XGBClassifier` C4P1 2:15, C4P1 7:50.
- **Diabetes** (442 pacientes, 10 atributos: edad, sexo, IMC, presión y seis medidas de sangre s1 a s6) y **California housing** (20.640 muestras, 8 atributos) con `max_depth=10` y `n_estimators=10` C4P1 4:28, C4P1 6:45, C4P1 7:50. Las predicciones siguen la tendencia C4P1 9:31. El primer árbol de diabetes arranca por s5 C4P1 11:13.
- **Vinos** (wine), multiclase, contra random forest con validación cruzada de 4 partes C4P1 12:14, C4P1 13:53. Entrena rápido C4P1 17:14.

### Correcciones y matices
- **Matiz:** boosting "planteado en el 89" C3P2 1:18:42. La pregunta de Kearns y Valiant es de 1988 y 1989, el primer boosting de Schapire de 1990 y AdaBoost (Freund y Schapire) de 1995 y 1997.
- **Corrección:** en AdaBoost "los datos se siguen eligiendo de forma aleatoria" C3P2 1:19:47. AdaBoost no sortea: repondera los ejemplos y sube el peso de los mal clasificados.
- **Corrección:** "se inicializan los pesos de cada árbol uniformes y en la primera iteración se entrenan todos los árboles" C3P2 1:21:28. Lo que se inicializa uniforme (1/N) son los pesos de los **ejemplos**; se entrena un clasificador débil por ronda, en secuencia, con los pesos que dejó el anterior.
- **Corrección:** "Z es normal, corresponde a la distribución normal" C3P2 1:22:37. Z_t es solo el factor de normalización para que los pesos sumen 1.
- **dudoso:** "AdaBoost se parece al backpropagation" C3P2 1:27:06: no hay relación directa.
- **Corrección:** AdaBoost "es menos sensible a valores extremos porque mira los datos en conjunto" C3P2 1:27:06 y tiene "poca variabilidad ante atípicos" C3P2 1:30:34. AdaBoost es conocido por lo contrario: su pérdida exponencial lo hace sensible al ruido y a los atípicos (en la misma filmina figura como desventaja).
- **dudoso:** "no funciona bien cuando hay correlación entre las características" C3P2 1:27:06: no es una limitación conocida de AdaBoost.
- **Corrección:** AdaBoost "es para clasificación" C3P2 1:27:06. Existe AdaBoost.R2 para regresión (`AdaBoostRegressor` en scikit-learn, verificado en el box).
- **Corrección:** gradient boosting "no asigna ponderación a los mal clasificados, solo a los correctos" C3P2 1:28:15. Cada árbol nuevo se ajusta al gradiente negativo de la pérdida; con pérdida cuadrática, a los residuos. No hay ponderación de correctos.
- **Corrección:** XGBoost hace "procesamiento fuera del núcleo, o sea en la GPU" C3P2 1:28:50. Out of core es entrenar con datos que no entran en RAM leyéndolos de disco. XGBoost (Chen y Guestrin, 2016) suma regularización, gradiente de segundo orden, búsqueda de cortes en paralelo y uso de caché; la GPU es una opción aparte.
- **Corrección:** "core i5 o i7 significa la cantidad de núcleos" C3P2 1:28:50. Son gamas comerciales de Intel.
- **Matiz:** "como se toman características al azar se pueden perder importantes" C3P2 1:30:34. Eso es del random forest; en boosting pasa solo si activás el submuestreo de columnas.
- **Corrección:** el voto blando "me dice qué porcentaje votó a esa clase" C3P2 1:32:12. El voto blando promedia las probabilidades predichas por cada modelo y elige la clase de mayor promedio (verificado en el box).
- **Corrección:** XGBoost "ganó varias competencias por el 2009, 2010" C4P1 1:08. Salió en 2014 (lo dice el propio Diego después C4P1 15:38) y se hizo famoso con la competencia Higgs de Kaggle de ese año.
- **Corrección:** el dataset de diabetes "para decir si una persona tiene diabetes o no" C4P1 3:22. En `load_diabetes` los 442 pacientes son diabéticos y el objetivo es una medida de la progresión de la enfermedad un año después: es **regresión** (en el box, el objetivo va de 25 a 346).
- **Matiz:** Federico dice que los datos vienen normalizados (bien: cada columna tiene suma de cuadrados 1, verificado en el box) y Karim agrega que "siempre es necesario estandarizar para que todos tengan el mismo peso" C4P1 5:31. Para árboles, random forest y XGBoost escalar no hace falta; sí para SVM, vecinos, redes y regresión regularizada.
- **Matiz:** el árbol arranca por s5 C4P1 11:13, que es el logaritmo de los triglicéridos séricos, no la glucemia.
- **Matiz:** "usamos la sigmoide como salida" para vinos C4P1 12:14. En multiclase XGBoost usa `multi:softprob`, que es softmax (verificado en el box).
- **dudoso:** "error 0,63 y 0,74... 58 y 54" C4P1 10:39 y "el primero 94, el segundo 40 y el último random forest 97" C4P1 13:53: no queda claro qué métrica ni qué modelo es cada uno. En el box, con validación cruzada de 4 partes en vinos, XGBoost da 0,927 y random forest 0,978.
- **para verificar:** "la última versión estable va por el 2023" C4P1 15:38. En 2025 salieron las versiones 3.0 y 3.1; en el box está la 3.4.1.

### Preguntas de repaso
1. ¿Qué diferencia hay entre bagging y boosting en cómo se entrenan los modelos?
2. Calculá α para un clasificador con ε = 0,1. ¿Y con ε = 0,5? ¿Qué significa ese último?
3. ¿A qué se ajusta cada árbol nuevo en gradient boosting con pérdida cuadrática?
4. ¿Qué es "out of core" y por qué no es lo mismo que usar GPU?
5. ¿Cuándo preferirías voto blando y qué necesitan los modelos para usarlo?

---

## 12. Sistemas de recomendación
**Dónde:** C4P1 18:03, C4P1 19:19, C4P1 20:36, C4P1 21:43, C4P1 23:22, C4P1 25:37, C4P1 27:19, C4P1 28:25, C4P1 31:46, C4P1 32:51, C4P1 34:33, C4P1 36:16, C4P1 37:25, C4P1 39:43, C4P1 42:00, C4P1 44:15, C4P1 46:26, C4P1 48:11, C4P1 49:49, C4P1 52:08, C4P1 53:19, C4P1 53:51, C4P1 56:00, C4P1 57:17, C4P1 59:24, C4P1 1:01:07, C4P1 1:02:50, C4P1 1:04:33, C4P1 1:08:50, C4P1 1:11:16, C4P1 1:13:33, C4P1 1:16:04, C4P1 1:21:15, C4P1 1:24:51

### Conceptos clave
- **Dónde están.** Google, Mercado Libre, Amazon, streaming, Steam, Facebook, Instagram, TikTok C4P1 19:19. Guían decisiones sobre ítems; "lo que realmente venden es nuestro tiempo" C4P1 20:36.
- **Tipos** C4P1 21:43, C4P1 23:22: basados en contenido (ítems parecidos a los que te gustaron), filtros colaborativos (usuarios con gustos parecidos) y basados en conocimiento. Las cámaras de eco (lo aporta Lu) y los terraplanistas como ejemplo del riesgo.
- **La matriz usuarios por ítems** C4P1 27:19, C4P1 28:25: retroalimentación explícita (estrellas, me gusta) e implícita (cuánto tiempo te detuviste). Es rala y dinámica.
- **Filtro colaborativo basado en usuarios** C4P1 31:46, C4P1 32:51, C4P1 34:33, C4P1 36:16: Claudia puntuó 5, 3, 4 y 4 y hay que predecir el ítem 5. La similitud se calcula con la correlación de Pearson, restando la media de cada usuario para corregir a los generosos y a los exigentes. La predicción es la media de Claudia más la suma de los desvíos de los vecinos ponderada por la similitud.
- **Basado en ítems** C4P1 37:25: similitud coseno ajustada (resta la media del usuario), sumando sobre los usuarios que puntuaron los dos ítems.
- **Costo y problemas** C4P1 39:43, C4P1 42:00, C4P1 44:15: las matrices son enormes y no se actualizan en tiempo real; se usan vecindarios (contactos, seguidos, geografía) y un mínimo de puntuaciones en común. Arranque en frío: encuesta inicial, datos de parentesco o ubicación, y actualizar más seguido a los nuevos.
- **Por qué es supervisado** (Diego): se predice la puntuación C4P1 48:11.
- **Surprise** (`pip install scikit-surprise`), parecida a scikit-learn C4P1 49:49. Dataset de libros Book Crossing: usuarios (ID, edad, ubicación), libros (ISBN) y puntuaciones C4P1 52:08. El libro más puntuado es "Wild Animus" C4P1 56:00; hay un usuario con 13.000 libros puntuados C4P1 57:02. Se filtran libros y usuarios con al menos 50 puntuaciones C4P1 57:17. `Reader` con escala de 1 a 10 C4P1 59:24.
- **Algoritmos y benchmark** C4P1 1:01:07, C4P1 1:02:50, C4P1 1:04:33: SVD, KNNBasic, KNNWithMeans y BaselineOnly, con validación cruzada de 3 partes y RMSE. Gana BaselineOnly con RMSE 3,3 (que incluye los ceros), en 0,27 segundos; kNN es lentísimo. Con k = 1 hay sobreajuste (celdas de Voronoi) C4P1 1:03:57.
- **Análisis del error** C4P1 1:08:50, C4P1 1:11:16, C4P1 1:13:33: el error depende de cuánta información hay del usuario y del libro (Manuel); los bots distorsionan. Recomendaciones para el usuario 4017 con predicciones de 8,58 a 9,47 C4P1 1:21:15.
- **Ética** C4P1 1:24:51: perfilado y manipulación.

### Correcciones y matices
- **Corrección:** "filtros basados en el conocimiento: el usuario explícitamente interactúa, me gusta, no me gusta" C4P1 23:22. Los sistemas basados en conocimiento usan requisitos explícitos y reglas del dominio ("quiero un auto de menos de tanto"). Los me gusta son retroalimentación explícita que usan el colaborativo y el basado en contenido. Y "basadas en cuestiones demográficas" es otro tipo más, el filtrado demográfico.
- **para verificar:** las similitudes de Claudia dan 0,83, 0,6, 0 y negativa C4P1 34:33. Es el ejemplo clásico de Alice (Jannach y otros, *Recommender Systems: An Introduction*); en el box, con esos datos, Pearson da 0,85, 0,71, 0,00 y −0,79, y la predicción 4,87 (o 5,09 si las medias de los vecinos se calculan solo sobre los ítems en común). Si los números de la filmina difieren, puede ser por redondeo o por otra variante.
- **Matiz:** "cuando el usuario 4 tenga baja interacción se lo voy a proponer a Claudia" C4P1 34:33. La fórmula usual toma los k vecinos más parecidos, con similitud positiva.
- **dudoso:** memoria "n² por m²" C4P1 42:00. La similitud ítem a ítem cuesta del orden de n² pares por los usuarios en común, no n²·m².
- **Corrección:** "es otro de los motivos por los cuales con VPN dejan de funcionar algunas plataformas de streaming" C4P1 43:42. Con VPN fallan por las licencias por país (geobloqueo), no por las matrices de similitud.
- **Matiz:** a la pregunta por la descomposición SVD, Karim responde "me equivoqué" y no se explica C4P1 46:26; Diego la usa en la notebook igual. Ver la guía para una explicación corta.
- **Corrección:** "tenemos 1.149.000 usuarios" C4P1 53:19. Son 1.149.780 **puntuaciones**; el dataset tiene unos 278.858 usuarios y 271.379 libros.
- **Corrección:** "el 62% de los libros no tuvo valoración" C4P1 53:51. Es el 62% de las puntuaciones, las que valen 0.
- **Corrección:** Daniel pregunta si 0 es "no puntuar" y Karim responde "no, el cero es un número; es que no le gustó para nada" C4P1 1:16:04. En Book Crossing el 0 es una interacción implícita sin nota (la escala explícita es de 1 a 10). Por eso el RMSE de 3,3 es tan alto: habría que sacar los ceros o tratarlos aparte.
- **Corrección:** "BaselineOnly es justamente el que calcula los coeficientes de correlación" C4P1 1:01:07. BaselineOnly predice media global + sesgo del usuario + sesgo del ítem, sin similitudes; Karim lo completa después con la media global.

### Preguntas de repaso
1. ¿Por qué Pearson resta la media de cada usuario?
2. ¿Qué diferencia hay entre filtro colaborativo basado en usuarios y basado en ítems?
3. ¿Qué es el arranque en frío y cómo lo mitigás?
4. ¿Qué predice BaselineOnly y por qué puede ganarle a kNN?
5. ¿Por qué tratar los ceros de Book Crossing como notas infla el RMSE?

---
## 13. Buenas prácticas: del problema al modelo en producción
**Dónde:** C4P2 0:00, C4P2 1:33, C4P2 3:46, C4P2 6:03, C4P2 7:34, C4P2 8:18, C4P2 12:04, C4P2 13:31, C4P2 14:15, C4P2 16:32, C4P2 18:00, C4P2 19:30, C4P2 21:00, C4P2 24:01, C4P2 26:29, C4P2 29:26, C4P2 31:34, C4P2 33:52, C4P2 35:16, C4P2 38:16, C4P2 40:33, C4P2 42:03, C4P2 42:50, C4P2 45:00, C4P2 48:23, C4P2 51:46, C4P2 54:53, C4P2 1:00:04, C4P2 1:08:23, C4P2 1:09:42, C4P2 1:10:32, C4P2 1:14:17, C4P2 1:15:46, C4P2 1:18:48, C4P2 1:20:20, C4P2 1:26:21, C4P2 1:29:17, C4P2 1:31:33, C4P2 1:33:24

### Conceptos clave
- **El libro de referencia.** Karim recomienda *Machine Learning Yearning* de Andrew Ng (cofundador de Coursera y de DeepLearning.AI): coloquial e introductorio, está en la bibliografía C4P2 0:00, C4P2 1:33. Buena parte de la clase sigue su estructura.
- **No compararse con Google.** Los grandes tienen datos y GPU sin límite; un grupo de investigación tiene 2 a 4 personas y máquinas de 2018. Karim entrena en sus computadoras para no regalar sus datos C4P2 2:16, C4P2 3:46, C4P2 4:31.
- **Primero la estadística.** Antes de programar: medias, varianzas, correlaciones, regresiones simples, modelos lineales generalizados. Si eso alcanza, no hace falta aprendizaje automático C4P2 6:03, C4P2 6:46, C4P2 7:34.
- **Si el primer modelo anda mal:** más datos o más completos, preprocesamiento, ingeniería de características, reducción de dimensionalidad y normalización C4P2 8:18, C4P2 9:01. El proceso es un ciclo iterativo (idea, código, experimento) C4P2 12:04, y el modelo nunca es final: los datos cambian con el tiempo y hay que reentrenar C4P2 13:31.
- **Particiones** C4P2 14:15, C4P2 16:32, C4P2 17:17, C4P2 18:00, C4P2 18:46: entrenamiento, validación y prueba con la misma distribución que la población. En un dataset de 230.000 imágenes satelitales de barcos con una clase de 530, hace falta muestreo estratificado. Tamaños típicos 70/10/20; con muchos datos la prueba puede ser un porcentaje chico.
- **El test del cliente** (Diego): muchas veces el cliente se guarda una parte y te evalúa con eso; la competencia de Kaggle funciona igual C4P2 19:30, C4P2 22:30, C4P2 23:23.
- **Datos fuera de distribución.** Un detector de rostros entrenado solo con personas blancas falla con piel oscura C4P2 21:00. El cliente que sacó del bolsillo un vástago con una manchita mínima C4P2 24:01. El detector de barbijos de la pandemia, que falló con los barbijos rosados de Conicet y con los transparentes para personas hipoacústicas C4P2 26:29.
- **Métricas** C4P2 29:26, C4P2 30:55, C4P2 31:34, C4P2 33:52: con desbalance el accuracy no sirve; F1, accuracy balanceada, macro average, curvas ROC y precisión recall. Una **métrica de optimización** y varias **de satisfacción** (tiempo de entrenamiento, de entrega) con umbrales. Qué error es más grave lo decide el cliente, y los umbrales se fijan **antes** de entrenar.
- **Clasificadores bobos** C4P2 35:16, C4P2 36:02, C4P2 36:50: responder siempre la clase más frecuente, al azar uniforme o al azar respetando las proporciones dan el piso de las métricas.
- **Setup rápido** C4P2 38:16, C4P2 39:01, C4P2 42:50, C4P2 43:34: un modelo con los parámetros por defecto y una parte de los datos para ver la tendencia; no construir el programa perfecto; probar varios modelos y varias semillas.
- **Registro de experimentos** C4P2 40:33, C4P2 42:03: fecha, dataset, configuración y métricas de cada prueba, para no repetir. Recomienda MLflow.
- **Empezar por modelos interpretables** C4P2 45:00, C4P2 1:06:01: "nunca empezamos con redes neuronales": árboles, regresión logística o SVM muestran qué características pesan; después redes con esas características. No casarse con un modelo y mantenerse actualizado C4P2 45:45.
- **Búsqueda de hiperparámetros** C4P2 48:23, C4P2 49:34, C4P2 50:15, C4P2 51:46: leer la documentación, búsqueda manual, en grilla (exhaustiva) o aleatoria, con validación cruzada; empezar con el 5% o 10% de los datos; guardar varias configuraciones buenas, no una.
- **Sesgo y varianza** C4P2 54:00, C4P2 54:53, C4P2 55:30, C4P2 57:02: con sesgo alto (no aprende ni el entrenamiento) agrandá el modelo o regularizá menos; con varianza alta, más datos, regularización, early stopping o bagging. La imagen de Karim: amasar una masa blanda en el aire.
- **Análisis de errores** C4P2 1:00:04, C4P2 1:01:34, C4P2 1:02:16, C4P2 1:04:34: listar los mal clasificados y buscar qué tienen en común; suelen estar cerca de las fronteras. Ablation test: sacar características y medir C4P2 1:08:23.
- **Aumento de datos con criterio** C4P2 1:09:02, C4P2 1:09:42: en imágenes de radar (SAR), rotar o agrandar un barco cambia la física de la retrodispersión y agrega ruido en vez de datos.
- **Software con aprendizaje automático** C4P2 1:09:47, C4P2 1:10:32, C4P2 1:14:17, C4P2 1:15:46, C4P2 1:18:00: el modelo es lo que sale del entrenamiento; hay un repositorio de modelos y se reentrena cuando el rendimiento se degrada. Tests antes de entrenar (formas, rangos esperados, probabilidades que suman 1, que el costo baje, fuga de datos) y después (perturbaciones que no deberían cambiar la salida, expectativas direccionales, repetir el test en el tiempo).
- **Notebook de buenas prácticas con Titanic** (Diego, "para ver en casa") C4P2 1:20:20, C4P2 1:21:46, C4P2 1:23:20, C4P2 1:26:21, C4P2 1:27:00, C4P2 1:28:34, C4P2 1:29:17, C4P2 1:30:46, C4P2 1:31:33, C4P2 1:33:24: exploración (faltan 177 edades), imputación simple, codificación de categóricas, escalado, validación cruzada estratificada, varios modelos con parámetros por defecto en un DataFrame, elección por parsimonia (todos rondan 79%), grilla para el perceptrón multicapa, matriz de confusión y curva ROC (AUC 0,81).

### Correcciones y matices
- **Corrección:** "modelos lineales generalizados mixtos, LGM" C4P2 7:34: la sigla usual es GLMM.
- **Corrección:** "cuando tenemos overfitting significa que no tenemos la complejidad necesaria" C4P2 55:30: lapsus. Falta de complejidad es underfitting (sesgo alto); el overfitting es exceso de complejidad respecto de los datos.
- **dudoso:** en el ejemplo de cáncer de mama Karim dice que diagnosticar cáncer a una persona sana "es peor" que decirle sana a una enferma, y enseguida que el tratamiento que no empieza a tiempo "es lo peor que puede pasar" C4P2 33:02. La transcripción mezcla las dos ideas. Lo que sí queda claro es que esa decisión es del cliente; en tamizaje médico en general se prioriza no perder enfermos (recall).
- **dudoso:** "si tenemos un elemento, el 1% para prueba; si tenemos 500, el 2%" C4P2 18:46: confuso en el audio. La regla del libro de Ng es que con un millón de ejemplos un 1% de prueba (10.000) ya alcanza.
- **dudoso:** "los sistemas de Bevin" C4P2 15:45 y "los sistemas del baby" C4P2 57:46 probablemente son bagging.
- **Matiz:** lo que Karim llama grid search en C4P2 46:30 es primero una grilla de experimentos (conjuntos de datos por modelos); `GridSearchCV` barre los hiperparámetros de un modelo, que es lo que explica después C4P2 48:23.
- **Matiz:** Diego codifica título y puerto con `LabelEncoder` C4P2 1:27:00. Para variables nominales con modelos lineales, SVM o redes conviene one hot; `LabelEncoder` está pensado para la etiqueta y le impone un orden falso a las categorías. Para árboles da casi igual.
- **para verificar:** "en primera clase casi el 50 por ciento sobrevivió" C4P2 1:24:06. En el train de Kaggle del Titanic sobrevivió alrededor del 63% de primera, 47% de segunda y 24% de tercera.
- **para verificar:** el rover de Marte entrenado en lugares de la Tierra parecidos C4P2 21:00; la transcripción dice "en la tía ya", que puede ser Atacama.
- **para verificar:** en qué materia se ve MLflow C4P2 42:03 (dice Deep Learning u otra electiva).
- **Matiz:** Karim no usa Colab "para no regalar los datos" C4P2 4:31: es una opinión razonable para datos propios o sensibles, pero las condiciones de uso cambian según el servicio y el plan.
- **Nota de transcripción:** entre C4P2 28:31 y C4P2 29:26 faster-whisper entró en un bucle de repetición y se pierde casi un minuto (habla del cinturón de seguridad y empieza con las métricas).

### Preguntas de repaso
1. ¿Qué diferencia hay entre una métrica de optimización y una de satisfacción? Dá un ejemplo de cada una para un detector de barbijos.
2. ¿Por qué hay que fijar los umbrales de las métricas antes de entrenar?
3. ¿Qué tres clasificadores bobos usarías como piso y qué accuracy daría el primero con un 70% de una clase?
4. ¿Qué harías primero con sesgo alto? ¿Y con varianza alta?
5. Nombrá dos tests previos al entrenamiento y dos posteriores.
6. ¿Por qué no siempre conviene rotar imágenes para aumentar datos?

---

## 14. El trabajo práctico: la competencia de Kaggle
**Dónde:** C1P1 2:12:28, C1P1 2:14:53, C4P2 1:36:02, C4P2 1:36:45, C4P2 1:37:34, C4P2 1:39:04, C4P2 1:39:50, C4P2 1:40:34, C4P2 1:41:20, C4P2 1:42:00, C4P2 1:43:32, C4P2 1:44:18, C4P2 1:46:34, C4P2 1:47:23, C4P2 1:48:02, C4P2 1:50:16, C4P2 1:51:01, C4P2 1:52:32, C4P2 1:54:06, C4P2 1:54:51, C4P2 1:56:18, C4P2 1:57:05, C4P2 1:57:50, C4P2 1:58:31, C4P2 1:59:21, C4P2 2:00:13, C4P2 2:02:18, C4P2 2:03:01, C4P2 2:06:35

### Conceptos clave
- **Formato.** Competencia privada en Kaggle, en equipos (pueden ser los grupos de los otros prácticos). El link está en el aula virtual y no hay que divulgarlo C4P2 1:36:02, C4P2 1:42:00. Cierra el 27 de julio C1P1 2:12:28.
- **El problema.** Clasificar caras con barbijo o sin barbijo, con un dataset que armaron Karim y Diego para el detector de la pandemia C4P2 1:36:45. Las caras recortadas se pasaron por una ResNet 101 preentrenada en ImageNet y ustedes reciben solo el **vector de características** de cada imagen, no la imagen, para que no se pueda etiquetar a mano C4P2 1:37:34, C4P2 1:39:04. Es transfer learning usado como extractor de características (módulo 7).
- **Columnas** C4P2 1:39:50, C4P2 1:45:04: id de la imagen, clase, ancho y alto del recorte, promedio del histograma de los tres canales RGB y las columnas del vector de características. Hay un `train` con etiqueta y un `test` sin ella C4P2 1:44:18.
- **Requisitos** C4P2 1:40:34, C4P2 1:41:20, C4P2 1:43:32, C4P2 2:06:35: análisis exploratorio; usar modelos de esta materia o de la anterior; superar el **baseline** que subió Diego, obtenido con un árbol sin configurar; probar **al menos tres modelos distintos** del árbol de decisión con búsqueda de hiperparámetros; discutir si la métrica es adecuada y justificar el modelo elegido. Participar es obligatorio y además hay que entregar la notebook con todos los análisis, con dos o tres días extra después del cierre.
- **Métrica:** accuracy balanceada (el promedio del recall de cada clase), que calcula Kaggle al subir C4P2 1:43:32, C4P2 1:56:18, C4P2 2:05:15.
- **La notebook de ejemplo** C4P2 1:47:23, C4P2 1:48:02, C4P2 1:49:46, C4P2 1:50:16, C4P2 1:51:01: hay más caras con barbijo que sin barbijo (desbalance); la clase se recodifica para que "sin barbijo" sea el 1, porque es lo que se quiere detectar; `StandardScaler`; 80/20 del train para validar (1500 para entrenar), que no es el test de la competencia; un árbol sin configurar ya da 94% en entrenamiento.
- **Predicción y envío** C4P2 1:52:32, C4P2 1:54:51, C4P2 2:00:13: aplicar al test exactamente las mismas transformaciones que al train, `predict`, y armar un CSV con dos columnas (id y clase) y exactamente 524 filas. Hay un archivo de ejemplo para probar el formato.
- **Tabla pública y privada** C4P2 1:57:50, C4P2 2:03:01: la pública usa el 26% del test y la final el 74% restante, que se publica un día después del cierre. A Diego le dio 97% en la pública y 96% en la privada. En una competencia de un año anterior (diabetes), un grupo que estaba en el top 10 perdió 22 posiciones y quedó debajo del baseline: no ajustes mirando la tabla pública.
- **Límite de envíos** diario C4P2 1:58:31, C4P2 2:06:01 ("creo que cinco por persona").
- **Qué probar** C4P2 1:59:21: SVM, XGBoost, random forest, redes, ensambles con modelos distintos.

### Correcciones y matices
- **Corrección:** ResNet "salió hace un par de años" C4P2 1:37:34: es de 2015.
- **Corrección:** "ImageNet tiene 100 mil imágenes y mil categorías" C4P2 1:38:19. ImageNet 1k, con el que se preentrena ResNet, tiene unos 1,28 millones de imágenes de entrenamiento y 1000 clases; el ImageNet completo tiene unos 14 millones de imágenes y más de 20.000 categorías.
- **dudoso:** el tamaño del test: Diego dice "438 imágenes para testeo... 1800 para entrenamiento... para testeo 524" C4P2 1:46:34, y después que el CSV tiene que tener exactamente 524 filas C4P2 2:00:13. Lo más probable es 524 en test; el resto, **para verificar** en la página de la competencia.
- **dudoso:** el baseline sale de "un árbol de clasificación, random forest creo que era" C4P2 1:40:34 y después "un árbol sin configurar" C4P2 1:57:05.
- **para verificar:** las fechas. En Overview dice que "comienza en media hora y termina en 18 días" C4P2 1:54:06, que desde el 4 de julio sería el 22; en C1P1 se dijo el 27 de julio C1P1 2:12:28.
- **para verificar:** el límite exacto de envíos por día C4P2 1:58:31.
- **Sugerencia:** con accuracy balanceada, usá `class_weight="balanced"` o umbrales ajustados y medí con `balanced_accuracy_score` en validación cruzada estratificada; y como las características vienen de una red, probá también regresión logística y SVM lineal, que suelen andar muy bien sobre embeddings.

### Preguntas de repaso
1. ¿Por qué la cátedra da vectores de ResNet y no las imágenes?
2. ¿Qué mide la accuracy balanceada y por qué es mejor que el accuracy para este dataset?
3. ¿Qué tenés que entregar además de participar?
4. ¿Por qué no conviene elegir el modelo final mirando la tabla pública?

---

## Lo que falta o quedó en duda
- **C4P2 sin subtítulos de la grabación.** Se transcribió con faster-whisper (modelo small, CPU) desde el audio: las citas son menos fieles, los nombres salen peor y hay casi un minuto perdido por un bucle de repetición (C4P2 28:31).
- **Notebooks, filminas y `mlutils`.** No están en los videos ni tuve acceso al aula virtual ni al repositorio; el código de la guía está reescrito. No pude comprobar la cantidad de filtros de la CNN de Fashion MNIST, el dataset de gato o no gato (parece el del curso de Andrew Ng, 64 × 64 × 3, **para verificar**) ni la versión exacta de cada librería que usó Diego.
- **Detalles de la competencia** (fechas, tamaño del test, límite de envíos, link): solo se ven de pasada en C4P2 y están marcados **para verificar**.
- **SVD en recomendación.** Karim reconoce que se salteó la explicación C4P1 46:26; la guía tiene una explicación corta y una implementación mínima.
- **Demos sin nombre:** la demo de SVM en el navegador C1P1 28:03, la página de visualización de optimizadores C2P1 47:06, la demo de voting que se pasó por el chat C3P2 1:35:52, el repositorio con libro de donde sale la notebook de recurrentes C3P1 1:24:00 y el gráfico de bagging contra boosting C3P2 1:30:00.
- **Herramientas de interpretabilidad** para ver qué palabras pesaron en una crítica: se dice que existen y no se nombran C3P1 1:19:01.
- **Quién es quién:** el nombre completo de "Bustos" C1P1 58:36 y de "Pancho" Tamarit C2P2 1:45:24, qué paper de Jorge Sánchez se menciona C1P1 1:31:30 y en qué "materia anterior" se había presentado Karim C1P1 1:19:00.
- **Números que no se entienden en el audio:** varios MSE de C1P2, los resultados de XGBoost en C4P1 (C4P1 10:39, C4P1 13:53) y el "0,8" de la CNN regularizada C2P2 1:37:15.

## Glosario de nombres que la transcripción deforma

| Se oye o se lee | Es |
|---|---|
| super vector machine, supervector machine | support vector machine (SVM) |
| King Los | hinge loss |
| ML utils | `mlutils`, la librería de la materia |
| Schrbel | dudoso: quizás Rosenblatt o McCulloch y Pitts |
| softgar | softmax |
| squishy | `np.squeeze` |
| Gato Dumas | el cocinero Carlos "Gato" Dumas (chiste del dataset de gatos) |
| Ashish | Ashish Vaswani, primer autor de "Attention Is All You Need" |
| Ciudad del Cabo | Cabo Verde (rival de Argentina el 3 de julio) |
| Bard | el chatbot de Google de 2023, hoy Gemini |
| Book Crossing | dataset de libros Book-Crossing |
| Wild Animus | el libro más puntuado de Book-Crossing |
| Machine Learning Jaring | *Machine Learning Yearning*, de Andrew Ng |
| LGM | GLMM, modelos lineales generalizados mixtos |
| sistemas de Bevin, sistemas del baby | dudoso: bagging |
| Con Iset | Conicet (los barbijos rosados) |
| la vela en color | `LabelEncoder` |
| simple imputación | `SimpleImputer` |
| veritas, vericelum | virginica y versicolor (dataset Iris) |
| el balance aquí uve si, balance es corta | balanced accuracy |
| cagle, kail | Kaggle |
| resnet 101 | ResNet-101 |
| uve, el ové | aula virtual (Moodle) |
| pancho tamari | "Pancho" Tamarit (Francisco Tamarit, para verificar) |
| mlflow | MLflow |
