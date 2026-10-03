# Apunte de estudio: Introducción al Aprendizaje Automático (Diplodatos, FAMAF UNC, Vanessa Mainardi y Edgardo)

**Curso:** Introducción al Aprendizaje Automático, materia de la diplomatura en ciencia de datos de FAMAF (UNC), edición 2026 · Docentes: Vanessa Mainardi (la teoría) y Edgardo (los prácticos en Colab; su apellido no se dice en ninguna de las grabaciones, dudoso) · Coordinación: Caro, la misma coordinadora que aparece en otras materias · Formato: cuatro clases sincrónicas grabadas en 10 videos no listados del canal FAMAF UNC. Por los títulos y lo que se dice en clase, las clases fueron el viernes 22 de mayo a la tarde, el sábado 23 de mayo a la mañana, el viernes 5 de junio a la tarde y el sábado 6 de junio a la mañana de 2026 (las dos primeras fechas son inferidas, para verificar).
**De qué va:** la materia presenta el aprendizaje automático como un problema de optimización: elegís una familia de modelos (el espacio de hipótesis), definís una función de costo y buscás los parámetros que la minimizan, cuidando que el modelo generalice y no memorice. Recorre los tipos de aprendizaje, la regresión lineal y polinomial con sobreajuste y regularización, los clasificadores lineales y el perceptrón, la regresión logística, Naive Bayes con bolsa de palabras, KNN, la clasificación multiclase, los árboles de decisión y los ensambles, el descenso por gradiente y sus variantes, la validación cruzada con búsqueda de hiperparámetros y las métricas de clasificación y de regresión, incluido el problema de las clases desbalanceadas. Hay dos trabajos prácticos: una regresión sobre California Housing y un esquema completo de clasificación sobre datos de préstamos bancarios.

> Nota: este apunte sale de los subtítulos automáticos en español de los 10 videos; los 10 tienen transcripción completa (la de C1P2 llegó tarde, después de varios reintentos espaciados). Muchos nombres vienen deformados (ver el glosario al final). Todo lo que figura acá es lo que se dice en clase. Cuando lo que se dijo está mal o es impreciso, lo marco como **Corrección**. Las cifras, fechas y afirmaciones que no chequeé están marcadas como **para verificar**. Algunas cuentas y valores por defecto de scikit-learn sí los chequeé corriendo scikit-learn 1.9.1 en el box, y eso está dicho en cada caso. Lo que no se entiende bien en la transcripción va como **dudoso**. Las ideas mías van marcadas como **Sugerencia**.

**Cómo leer los links:** cada link dice el video y el minuto. "C2P1 1:23:45" es la clase 2, parte 1, en la hora 1, minuto 23, segundo 45.

## Los 10 videos

| # | Id | Video | Contenido | Duración | Link |
|---|---|---|---|---|---|
| 1 | — | C1P1: Clase 1, parte 1 ("Recording") | Presentación, qué es aprender, tipos de aprendizaje, regresión, ciclo de trabajo, polinomios, sobreajuste y regularización | 1:29:52 |  |
| 2 | — | C1P2: Clase 1, parte 2 ("Recording 2") | Solución cerrada, práctico de regresión (dimensión cero y polinomios), clasificación lineal y perceptrón | 2:10:29 |  |
| 3 | — | C2P1: Clase 2, parte 1 ("Recording") | Práctico del perceptrón, regresión logística (teoría y práctico con dígitos) | 1:34:40 |  |
| 4 | — | C2P2: Clase 2, parte 2 ("Recording 2") | Naive Bayes, bolsa de palabras y práctico de spam y China/Japón | 1:07:37 |  |
| 5 | — | C2P3: Clase 2, parte 3 ("Recording 3") | KNN, multiclase y multietiqueta, OvA y AvA, presentación del práctico 1 | 55:35 |  |
| 6 | — | C3P1: Clase 3, parte 1 (05/06/2026 17:51) | Árboles de decisión: Gini, entropía, ganancia de información, algoritmos, ensambles | 1:28:24 |  |
| 7 | — | C3P2: Clase 3, parte 2 ("Recording 2") | Práctico de árboles; funciones de costo, descenso por gradiente y tasa de aprendizaje | 2:05:45 |  |
| 8 | — | C4P1: Clase 4, parte 1 (06/06/2026 09:53) | Validación y remuestreo, práctico de árboles y random forest, validación cruzada y búsqueda de hiperparámetros | 1:16:41 |  |
| 9 | — | C4P2: Clase 4, parte 2 ("Recording 2") | Mentorías; métricas binarias, umbral, curvas ROC y PR | 55:55 |  |
| 10 | — | C4P3: Clase 4, parte 3 ("Recording 3") | Métricas multiclase, desbalance, práctico de métricas, presentación del práctico 2 | 1:17:23 |  |

Duración total: 14:22:21 (unas 14 horas y 20 minutos).

**Cómo se determinó el orden.** Los títulos dicen la clase y la parte ("Recording", "Recording 2", "Recording 3"), y los de las clases 3 y 4 traen la fecha y la hora de grabación. Las fechas de subida no sirven para ordenar: C1P2 se subió el 27/05 y C1P1 el 29/05. Dentro de cada clase, el contenido encadena: C1P1 termina con la regularización y la escala logarítmica de lambda C1P1 1:28:01 y C1P2 arranca con la solución cerrada de la regresión y con una pregunta sobre ese lambda C1P2 0:02, C1P2 5:37. C1P2 termina con "mañana sigo" con el perceptrón C1P2 2:09:09 y C2P1 arranca justamente con ese práctico C2P1 6:38. C2P2 sigue después de una pausa con Naive Bayes C2P2 0:07, y C2P3 con KNN después de la pausa "para preparar el mate" C2P2 1:07:04, C2P3 0:05. C3P1 termina con un corte "hasta las 8" y la promesa del práctico de árboles C3P1 1:28:03, que es como arranca C3P2 C3P2 2:16. C4P1 termina con el corte en el que "tiene que venir Luis a contar de las mentorías" C4P1 1:16:10 y C4P2 arranca con Luis C4P2 0:07. C4P2 se corta cuando a Vanessa se le cae el micrófono C4P2 54:38 y C4P3 sigue con las métricas multiclase C4P3 0:02.

## Mapa de módulos y videos

| Módulo | Dónde se ve |
|---|---|
| 0. La materia: quiénes la dan, cronograma, materiales y mentorías | C1P1 (inicio), C2P3 (final), C3P2 (inicio), C4P2 (inicio), C4P3 (final) |
| 1. Qué es aprender de datos y tipos de aprendizaje | C1P1 |
| 2. El ciclo de trabajo: conjuntos, parámetros e hiperparámetros | C1P1, C1P2, C2P1 (inicio), C4P1 |
| 3. Regresión lineal y polinomial, sobreajuste y regularización | C1P1, C1P2 |
| 4. Clasificadores lineales y perceptrón | C1P2, C2P1 |
| 5. Regresión logística | C2P1 |
| 6. Naive Bayes y bolsa de palabras | C2P2 |
| 7. KNN y modelos no paramétricos | C2P3 |
| 8. Multiclase y multietiqueta | C2P3, C2P1 (softmax) |
| 9. Árboles de decisión | C3P1, C3P2 |
| 10. Ensambles y el práctico de árboles y random forest | C3P1, C4P1 |
| 11. Funciones de costo y optimización | C3P2, C1P2 |
| 12. Validación y selección de modelos | C4P1 |
| 13. Métricas de clasificación y de regresión | C4P2, C4P3 |
| 14. Clases desbalanceadas | C4P3, C2P1 |
| 15. Los trabajos prácticos | C2P3, C4P3 |

---

## 0. La materia: quiénes la dan, cronograma, materiales y mentorías
**Dónde:** C1P1 0:04, C1P1 0:58, C1P1 2:18, C1P1 2:56, C1P1 3:29, C2P3 36:54, C2P3 55:04, C3P2 0:04, C3P2 0:35, C4P2 0:07, C4P2 0:42, C4P2 4:47, C4P2 6:45, C4P3 1:16:04

### Conceptos clave
- **Vanessa Mainardi.** Se presenta como matemática, recibida en FAMAF, con doctorado en matemática y maestría en estadística. Es investigadora del CONICET (la transcripción dice "CONISET") desde hace más de 12 años y docente de la Universidad Nacional de Villa María. Investiga aprendizaje automático con señales biomédicas, electroencefalogramas y electrocardiogramas, con deep learning para predecir patologías neuronales o cardíacas C1P1 0:04.
- **Edgardo.** Es doctor en física y fue profesor titular de FAMAF. Trabaja con redes neuronales y aprendizaje automático en física (espectros, estado sólido, materiales) y, "para divertirnos", con tests de psiquiatría C1P1 0:58. Más adelante cuenta que entrenó redes para reconstruir espectros de radiación de aceleradores lineales C2P1 3:26. Su apellido no se dice; Vanessa lo llama "Edo" al cierre C4P3 1:16:04.
- **El temario de la clase 1.** Fundamentos, espacio de hipótesis, tipos de problemas, regresión lineal y polinomial, regularización, sobreajuste, clasificación, clasificadores lineales y perceptrón, con prácticas en notebooks "como las otras materias" C1P1 2:56. En esta materia los modelos se ven "por encima"; en las dos materias siguientes, en profundidad C1P1 3:29.
- **Materiales.** Las clases están en PDF en el aula virtual C1P1 2:18. Las notebooks corren en Colab (o en Jupyter local, porque no son pesadas), montan Google Drive y usan una librería `utils` armada en la diplomatura para graficar C3P2 0:35. Las consultas van por Slack C2P3 36:54.
- **Asistencia.** Edgardo comenta que en la clase 3 llegaron a 103 conectados como máximo C3P2 0:04.
- **Cronograma.** La clase 2 terminó con "nos vemos de nuevo el cinco" y "en 15 días" C2P3 55:04. El práctico 1 vence el 8 de junio y el práctico 2 el 22 de junio (ver el módulo 15).
- **Mentorías.** Luis (apellido deformado en la transcripción, dudoso) coordina las mentorías con Yanina (apellido dudoso). Habrá una reunión "dentro de dos viernes", en horario de clase, con micrositios de cada mentoría y un formulario para elegir 4 o 5 prioridades; son unas 140 personas en 18 grupos y la asignación se hace con un algoritmo C4P2 0:07, C4P2 0:42. Son tres prácticos de alrededor de un mes cada uno, en grupos de unas cuatro personas, con un mentor o mentora cada dos grupos; este año ya no hace falta el video intermedio C4P2 4:47. Caro les pide que no pasen de largo los mails de Luis y de Yanina ni el canal de Slack, porque si no eligen los ponen donde haya lugar; los dos viernes siguientes no hay clase C4P2 6:45.

<details>
<summary>Preguntas de repaso del módulo 0 (con respuestas)</summary>

1. **¿Quién da la teoría y quién la práctica?** Vanessa Mainardi da la teoría y Edgardo los prácticos en Colab C1P1 0:04, C1P1 0:58.
2. **¿Qué profundidad tienen los modelos en esta materia?** Se ven "por encima"; las dos materias siguientes los profundizan C1P1 3:29.
3. **¿Dónde están las slides y por dónde se consulta?** Las slides en PDF están en el aula virtual y las consultas van por Slack C1P1 2:18, C2P3 36:54.
4. **¿Qué pasa si no elegís mentoría a tiempo?** Te asignan donde haya lugar C4P2 6:45.

</details>

---

## 1. Qué es aprender de datos y tipos de aprendizaje
**Dónde:** C1P1 4:03, C1P1 9:06, C1P1 10:14, C1P1 11:19, C1P1 13:04, C1P1 14:37, C1P1 15:09, C1P1 16:54, C1P1 18:04, C1P1 19:10, C1P1 21:24, C1P1 22:32, C1P1 24:26, C1P1 27:30, C1P1 29:10, C1P1 34:10, C1P1 37:33, C1P1 40:52, C1P1 43:31, C1P1 44:37, C1P1 45:45, C1P1 48:27, C1P1 49:30

Vanessa arranca preguntando qué diferencia hay entre programar y entrenar C1P1 4:03.

### Conceptos clave
- **Programar contra aprender.** En la programación clásica le das a la computadora datos y reglas y te devuelve respuestas; en el aprendizaje automático le das datos y resultados y lo que sale es el modelo C1P1 9:06. Son dos mundos: instrucciones explícitas (los `if`) contra inferencia a partir de datos, con entrenamiento, optimización, parámetros y ajuste C1P1 10:14. Una alumna lo resume así: el experto define el por qué y el para qué, y el modelo el cómo C1P1 4:03.
- **Espacio de hipótesis.** Primero elegís un modelo, por ejemplo una regresión lineal. El espacio de hipótesis es el conjunto de funciones que obtenés variando sus parámetros, y aprender es buscar la mejor minimizando una función de costo. Vale "desde regresión lineal y random forest hasta GPT" C1P1 11:19. Qué modelo elegir depende del tipo de problema y del análisis exploratorio: "si uno va ciego..." C1P1 13:04.
- **Supervisado.** Los datos traen la respuesta, como el precio en el dataset de casas de Melbourne de las materias anteriores; entrenar es "ajustar las perillas", los pesos C1P1 15:09.
- **No supervisado.** No hay etiquetas y se busca la estructura interna, como un nene con un balde de Lego C1P1 16:54. Ejemplos: segmentación de clientes con clustering, donde la etiqueta del clúster la ponés vos C1P1 21:24; las listas de Spotify o la grabación y los perfiles de clientes de un banco C1P1 40:52. Sirve para explorar antes de un modelo supervisado: sacás la etiqueta y mirás si los clústeres coinciden con sanos y enfermos C1P1 27:30.
- **Autosupervisado.** Es "el motor de la IA actual": se oculta una parte del dato (una palabra) y el modelo la adivina, como tarea de pretexto C1P1 18:04, C1P1 43:31. Hay dos variantes: la autorregresión (predecir el siguiente token, como GPT) y el enmascaramiento (como BERT) C1P1 44:37.
- **Por refuerzo.** Un agente aprende por recompensas en un entorno interactivo, por ensayo y error, como en un videojuego o el ta te ti, balanceando explorar y explotar C1P1 19:10, C1P1 48:27. Vanessa lo presenta como el "toque final" de los modelos de lenguaje, con humanos que dan la recompensa C1P1 49:30.
- **Preentrenamiento y ajuste fino.** El aprendizaje moderno va de lo general a lo específico: un preentrenamiento con muchísimos datos y semanas de cómputo da "cultura general", y un ajuste fino de horas con unos pocos miles de ejemplos lo especializa en leyes o medicina; eso es transfer learning C1P1 45:45.
- **Regresión y clasificación.** La regresión predice una variable continua: tenés pares (x, y) con x un vector, suponés y = f(x) + ruido y buscás la curva que minimiza el error, no la que pasa por todos los puntos C1P1 29:10, C1P1 31:58. La clasificación predice una categoría y dibuja una frontera de decisión, por ejemplo spam según signos de exclamación y enlaces externos C1P1 34:10. Lo que define el tipo de problema es la variable respuesta: con los datos de Melbourne, predecir el precio es regresión y predecir el tipo de propiedad (h, u, t) es clasificación C1P1 37:33.
- **KNN es supervisado.** Ante la duda de si el imputador KNN de las materias anteriores es supervisado, Vanessa aclara que KNN es un clasificador supervisado que vota por mayoría C1P1 24:26.

### Correcciones y matices
- **Corrección:** al hablar de compresión de imágenes agrupando píxeles, Vanessa dice "supervisado", pero el ejemplo es de aprendizaje no supervisado (clustering de colores) C1P1 40:52.
- **Dudoso:** Manuel pregunta si hay autosupervisión con imágenes; Vanessa responde que lo que conoce es pasarle etiquetas con redes convolucionales C1P1 44:37. **Sugerencia:** existen métodos autosupervisados para imágenes, como los masked autoencoders (para verificar el estado del arte).
- **Matiz:** el pulgar arriba o abajo de un chat no reentrena el modelo en el momento; el aprendizaje por refuerzo con feedback humano (RLHF) se hace en una etapa de entrenamiento aparte (para verificar los detalles de cada proveedor) C1P1 49:30.
- **Pregunta abierta:** un alumno pregunta si se pueden estimar precios con aprendizaje no supervisado; Vanessa dice que no, porque sin respuesta no podés validar, y que lo va a pensar C1P1 25:11.

<details>
<summary>Preguntas de repaso del módulo 1 (con respuestas)</summary>

1. **¿Qué invierte el aprendizaje automático respecto de la programación clásica?** En lugar de reglas que producen respuestas, le das datos y respuestas y sale el modelo C1P1 9:06.
2. **¿Qué es el espacio de hipótesis?** El conjunto de funciones que obtenés variando los parámetros del modelo elegido C1P1 11:19.
3. **¿Qué hace un modelo autosupervisado?** Oculta parte del dato y aprende a adivinarla, como la palabra siguiente o una palabra enmascarada C1P1 18:04, C1P1 44:37.
4. **Con los datos de Melbourne, ¿cuándo es regresión y cuándo clasificación?** Regresión si predecís el precio; clasificación si predecís el tipo de propiedad C1P1 37:33.
5. **¿Para qué sirve el aprendizaje no supervisado antes de uno supervisado?** Para explorar: ver si los grupos que aparecen solos coinciden con las clases que te interesan C1P1 27:30.

</details>

---

## 2. El ciclo de trabajo: conjuntos, parámetros e hiperparámetros
**Dónde:** C1P1 50:37, C1P1 52:14, C1P1 53:19, C1P1 1:03:52, C1P2 42:00, C1P2 44:10, C1P2 49:22, C1P2 53:14, C2P1 0:03, C2P1 1:41, C2P1 3:26, C2P1 5:01, C3P2 16:51, C4P1 0:07, C4P1 1:46, C4P1 3:27

### Conceptos clave
- **Tres conjuntos.** El dataset se divide en entrenamiento, validación (para las decisiones intermedias, como los hiperparámetros) y prueba, que queda "bajo llave" hasta el final y "no sale de la cancha" C1P1 50:37. En la clase 4 Vanessa lo repite: separás train y test antes de cualquier ajuste, el test se usa una sola vez con el modelo definitivo y si lo usás más de una vez queda contaminado C4P1 0:07, C4P1 1:46. Su resumen: "divido, testeo me olvido" C4P1 3:27.
- **Hasta cuatro conjuntos.** Edgardo cuenta que a veces divide en cuatro: hiperparámetros, entrenamiento, testeo y un conjunto final de contraste; en su trabajo con espectros de aceleradores guarda datos medidos por otros usuarios para la validación final C2P1 0:03, C2P1 3:26. El ejemplo senoidal con 20 datos "no es muy aconsejable", es para mostrar "que el auto funciona, no la tapicería" C2P1 1:41.
- **Parámetros e hiperparámetros.** Los parámetros (pesos) dan forma al modelo y los encuentra el entrenamiento; los hiperparámetros los decidís vos antes, como el grado del polinomio C1P1 52:14. En redes neuronales son hiperparámetros la cantidad de capas ocultas y de neuronas por capa; la entrada y la salida las fija el problema C2P1 5:01.
- **No es magia.** "La máquina no es mágica, no es una caja negra": ajusta perillas hasta minimizar el costo. Mirás la curva de pérdida y, si se estanca o sube, volvés a los hiperparámetros C1P1 53:19. Y siempre empezás por el modelo más simple C1P1 1:03:52.
- **`train_test_split` por dentro.** Edgardo muestra la firma con `inspect.signature`: recibe los arreglos, `test_size` o `train_size` (conviene pasar uno solo), `random_state` (None por defecto), `shuffle=True` y `stratify=None` C1P2 44:10, C1P2 53:14. El conjunto de evaluación es "un conjuntito guardado en una caja fuerte que no se entere scikit-learn" C1P2 42:00.
- **La semilla.** Las computadoras generan números pseudoaleatorios a partir de una semilla; `random_state` fija dónde empieza la serie, así que con la misma semilla obtenés la misma partición. Conviene fijarla mientras probás y depurás C1P2 49:22, C3P2 16:51.

### Tips
- Edgardo sugiere sacar el `random_state` "cuando anda bien" C3P2 16:51, C1P2 49:22. **Sugerencia:** para un práctico o un informe es mejor dejarlo fijo y, si querés medir la variabilidad, repetir con varias semillas y reportarlas.
- Ante cualquier función que no conocés, `help()` o `inspect.signature()` te dicen qué espera C1P2 44:10.

<details>
<summary>Preguntas de repaso del módulo 2 (con respuestas)</summary>

1. **¿Para qué sirve el conjunto de validación y para qué el de prueba?** Validación para elegir modelos e hiperparámetros; prueba para medir una sola vez el modelo final C1P1 50:37, C4P1 1:46.
2. **¿Qué diferencia hay entre un parámetro y un hiperparámetro?** El parámetro lo aprende el entrenamiento; el hiperparámetro lo fijás vos antes, como el grado del polinomio C1P1 52:14.
3. **¿Qué controla `random_state`?** El punto de partida de la serie pseudoaleatoria, y con eso la reproducibilidad de la partición C1P2 49:22.
4. **¿Qué pasa si usás el test varias veces para decidir?** Queda contaminado y tu estimación deja de ser insesgada C4P1 0:07.

</details>

---

## 3. Regresión lineal y polinomial, sobreajuste y regularización
**Dónde:** C1P1 54:55, C1P1 56:04, C1P1 57:43, C1P1 1:04:25, C1P1 1:07:11, C1P1 1:09:56, C1P1 1:16:07, C1P1 1:18:56, C1P1 1:19:31, C1P1 1:20:45, C1P1 1:22:20, C1P1 1:23:28, C1P1 1:26:21, C1P1 1:28:01, C1P1 1:29:08, C1P2 0:02, C1P2 5:37, C1P2 7:07, C1P2 15:29, C1P2 22:07, C1P2 28:54, C1P2 31:14, C1P2 54:54, C1P2 57:16, C1P2 1:02:24, C1P2 1:04:40, C1P2 1:07:41, C1P2 1:16:39, C1P2 1:20:01, C1P2 1:21:08, C1P2 1:22:08

### Conceptos clave
- **Regresión lineal.** Una recta, un plano o un hiperplano: superinterpretable, pero asume una relación lineal, y "en la gran mayoría de los casos no hay relación lineal" C1P1 54:55. Vanessa discute con la clase si el precio de una vivienda es lineal (la antigüedad tiene una relación inversa) y les deja la respuesta para el práctico; la intuición se valida con gráficos de pares y estadística descriptiva C1P1 57:43.
- **Regresión polinomial.** y(x, w) = w0 + w1 x + ... + wM x^M, minimizando el error cuadrático con un 1/2 adelante para que la derivada quede prolija C1P1 1:04:25. Captura curvas, pero con más riesgo de sobreajuste: el modelo memoriza en lugar de aprender, como quien estudia de memoria para un examen C1P1 56:04. Las variables categóricas entran como variables dummy 0/1 C1P1 1:07:11.
- **El grado como hiperparámetro.** Con el ejemplo del seno, el grado 0 y el 1 se quedan cortos, el 3 anda bien y el 9 interpola los puntos de entrenamiento pero en validación el error se dispara C1P1 1:09:56. El error de entrenamiento baja siempre; el de validación baja y después sube; el equilibrio está entre la brecha y la magnitud del error C1P1 1:16:07. Cuando la cantidad de parámetros se acerca a la de observaciones, el modelo copia el ruido: "el juez es la validación" y, entre dos modelos parecidos, gana el más simple (navaja de Occam) C1P1 1:18:56.
- **Más datos.** Con M = 9 y 20 puntos el error de validación es 5.856; con 100 puntos baja a 0.189 C1P1 1:19:31.
- **Solución cerrada.** La regresión polinomial es una regresión lineal con el cambio de variable z = (1, x, x², ..., x^M). Escribiendo el error en forma matricial y derivando, w* = (ZᵀZ)⁻¹Zᵀy; con regularización la fórmula cambia y por eso cambian los pesos. "Algo que no nos va a pasar con el resto de los modelos", que necesitan descenso por gradiente C1P1 1:20:45, C1P2 0:02.
- **Regularización.** Se suma al costo un término lambda/2 ||w||² que penaliza coeficientes grandes; lambda es un hiperparámetro que se prueba en escala logarítmica C1P1 1:23:28, C1P1 1:28:01. Si los pesos son grandes, el costo sube y el modelo reajusta C1P1 1:24:13. Un lambda grande da coeficientes chicos y estables, menos sensibles al ruido C1P1 1:29:08. Pero la penalización máxima no es el mejor modelo: probás varios lambdas y te quedás con el que mejor generaliza C1P2 5:37.
- **Una cosa por vez.** Ante la pregunta de si combinar varios remedios contra el sobreajuste, Vanessa dice que se puede, pero que no vas a saber cuál funcionó; ella prefiere probar por partes C1P2 7:07.
- **El práctico, desde dimensión cero.** Edgardo arranca con un modelo constante: con siete notas de un alumno, minimizar Σ(yᵢ - a)² derivando da que el mejor representante es el promedio C1P2 15:29. Lo programa con una lista de Python y un barrido con `np.linspace(4, 10, 300)` que muestra el mínimo C1P2 22:07.
- **Datos con ruido.** Genera sin(2πx) y le suma ruido gaussiano con un "spread" que es el sigma de la gaussiana C1P2 28:54, C1P2 31:14, C1P2 33:27. Toma 20 puntos, 5 para entrenar y 15 para validar, ajusta una recta por mínimos cuadrados con la fórmula de Vanessa y obtiene un MSE de 0.015 en entrenamiento contra 0.78 en validación C1P2 54:54, C1P2 57:16.
- **Polinomios con scikit-learn.** `make_pipeline(PolynomialFeatures(degree=d), LinearRegression(fit_intercept=False))`, con `X.reshape(-1, 1)` porque `fit` espera una matriz columna C1P2 1:02:24, C1P2 1:07:41. `fit_intercept=False` obliga a pasar por el origen; acá se usa porque `PolynomialFeatures` ya agrega la columna de unos C1P2 1:04:40. Con grados 1, 3, 5 y 10, la validación baja hasta el grado 3 y después se dispara: grados 1 y 2 son underfitting, de 5 en adelante overfitting C1P2 1:20:01, C1P2 1:21:08.
- **Grados de libertad.** Datos menos parámetros: con 20 datos y una recta quedan 18. Con tantos parámetros como datos, la curva pasa por todos los puntos, y eso es memorizar C1P2 1:16:39.

### Correcciones y matices
- **Corrección:** con ln λ = 0 (λ = 1) Vanessa dice que se está "penalizando lo máximo posible" C1P1 1:26:21. λ puede ser mayor que 1; λ = 1 es solo el extremo del rango que muestra la figura.
- **Corrección:** cuando el grado es alto los coeficientes se disparan, y Vanessa lo atribuye al "costo computacional" C1P1 1:22:20. El problema real es la inestabilidad numérica y la varianza del modelo (para verificar el matiz exacto de la slide).
- **Para verificar:** las figuras del seno con M = 0, 1, 3 y 9 y la regularización con ln λ = -18 parecen las del capítulo 1 de Pattern Recognition and Machine Learning de Bishop C1P1 1:09:56, C1P1 1:26:21.
- **Corrección:** Edgardo dice que x, x² y x³ "son ortogonales entre sí, independientes" C1P2 1:03:34. No lo son: en [0, 1] están muy correlacionadas. La linealización vale porque el modelo es lineal en los parámetros w, no porque las potencias sean independientes.
- **Corrección:** según Edgardo, el FWHM de una gaussiana es "como un 38% más grande que sigma" C1P2 33:27. En realidad FWHM = 2√(2 ln 2) σ ≈ 2,355 σ, y el ancho entre los puntos de inflexión es 2σ.
- **Matiz:** dice que scikit-learn arranca con pesos aleatorios y los corrige iterando "durante el entrenamiento de la red neuronal" C1P2 1:01:17. `LinearRegression` resuelve por mínimos cuadrados sin iterar; lo iterativo vale para el descenso por gradiente y las redes.
- **Para verificar:** Edgardo explica que "regresión" viene de que el modelo "regresa datos" C1P2 9:54. El término viene de Galton y la "regresión a la media".
- **Para verificar:** dice que "ChatGPT anda por los 5000 millones de parámetros" C1P2 21:34. OpenAI no publica la cifra de sus modelos actuales, y los modelos de ese tamaño son bastante más grandes.
- **Dudoso:** "si influyen más de 10 o 12 variables externas, el ruido es gaussiano" C1P2 31:14. La idea viene del teorema central del límite, pero no hay un número mágico.
- **Problema de escala.** Un alumno no ve bajar el error de entrenamiento: es la escala automática de matplotlib, aplastada por el error de validación C1P2 1:22:08.

<details>
<summary>Preguntas de repaso del módulo 3 (con respuestas)</summary>

1. **¿Por qué la regresión polinomial es "lineal"?** Porque con z = (1, x, ..., x^M) el modelo es lineal en los pesos w C1P2 0:02.
2. **¿Qué curva de error delata el sobreajuste?** La de validación, que baja y después sube mientras la de entrenamiento sigue bajando C1P1 1:16:07, C1P2 1:21:08.
3. **Nombrá dos remedios contra el sobreajuste que se ven en la clase 1.** Más datos y regularización C1P1 1:19:31, C1P1 1:23:28.
4. **¿Por qué no elegir siempre el lambda más grande?** Porque estabiliza los coeficientes pero no minimiza el error de generalización; se elige con validación C1P2 5:37.
5. **¿Cuál es el mejor modelo constante para un conjunto de notas según el error cuadrático?** El promedio C1P2 15:29.

</details>

---

## 4. Clasificadores lineales y perceptrón
**Dónde:** C1P2 1:26:11, C1P2 1:28:22, C1P2 1:28:53, C1P2 1:29:38, C1P2 1:30:18, C1P2 1:36:57, C1P2 1:39:13, C1P2 1:40:54, C1P2 1:43:11, C1P2 1:50:16, C1P2 1:51:22, C1P2 1:58:10, C1P2 2:02:10, C1P2 2:06:39, C2P1 6:06, C2P1 6:38, C2P1 7:47, C2P1 9:39, C2P1 13:18, C2P1 16:09, C2P1 18:57, C2P1 20:02, C2P1 22:19, C2P1 22:54

### Conceptos clave
- **Clasificación binaria.** Ejemplos: detectar fraude con monto, hora, ubicación e historial, o perro contra gato con los píxeles aplanados de una imagen de 28 × 28 C1P2 1:26:11. Se busca un hiperplano f y se decide por su signo: +1 si f(x) > 0 y -1 si no. Una observación está bien clasificada si yᵢ f(xᵢ) > 0 C1P2 1:28:22.
- **Arquitectura.** f(x) = wᵀx + b. El resultado es el score, una medida de confianza que dice qué tan lejos está el punto de la frontera, y una función de activación o de decisión lo convierte en etiqueta. La frontera son los puntos donde f = 0 C1P2 1:29:38.
- **Separabilidad lineal.** El perceptrón converge solo si existe un hiperplano que separe las clases, algo difícil de encontrar en datos reales. Si no, hay que mapear a dimensiones superiores con SVM (próxima materia) o usar redes profundas C1P2 1:28:53.
- **El algoritmo.** Lo propuso Frank Rosenblatt en 1958 como la primera neurona artificial. Es online, procesa una observación por vez, y es "el átomo de las redes neuronales profundas" C1P2 1:30:18. Arrancás con pesos en cero o aleatorios chicos, predecís con el signo de wᵀx y, si te equivocaste, actualizás w ← w + r yᵢ xᵢ, con r la tasa de aprendizaje C1P2 1:36:57, C1P2 1:39:13. Convergiste cuando pasás por todos los puntos y están todos bien C1P2 1:40:54.
- **Por qué funciona (geometría).** w es perpendicular al hiperplano y wᵀx = |w||x| cos θ. Un positivo mal clasificado forma un ángulo mayor a 90° con w; sumar r y x rota w, y con él el hiperplano, hasta que el ángulo baja de 90°. Para un negativo, la suma es en realidad una resta C1P2 1:43:11.
- **Etiquetas -1 y +1.** Con etiquetas 0 la actualización no hace nada (y = 0), por eso conviene -1/+1 C1P2 1:40:54, C2P1 7:47.
- **Límites.** Es un modelo muy básico que ya no se usa, "pero es la base de todo"; si los datos no son separables no converge y hay que pasar a SVM, a la regresión logística u otros C1P2 1:50:16. La versión con descenso por gradiente reemplaza la pérdida 0-1, que no es diferenciable y no dice cuánto te equivocaste (un score de 0.51 no es lo mismo que uno de 100), por una diferenciable C1P2 1:51:22.
- **Historia.** El perceptrón resolvía AND y OR, pero no XOR; un libro mostró que solo hacía separaciones lineales y vino "el primer invierno" de las redes neuronales, hasta que se juntaron varios perceptrones en una red C1P2 1:58:10, C2P1 6:38.
- **El práctico.** `make_classification` genera 100 puntos con 2 features informativas, 2 clases, un clúster por clase y `class_sep=0.5`; las etiquetas 0 se pasan a -1 y se separan 60/40 C1P2 2:02:10, C2P1 9:39, C2P1 12:23. Con W = (1, 1) sin entrenar la exactitud es del 10% C2P1 16:09. La regla se aplica solo a los mal clasificados, en un loop con contador de pasos y una bandera de fin; con r = 5 termina en 9 pasos C2P1 18:57, C2P1 20:02. Los pesos finales indican que la separación izquierda derecha es la que importa, y la frontera w1x1 + w2x2 = 0 tiene pendiente -w1/w2 C2P1 22:19, C2P1 22:54.
- **El bias.** Sin bias (b = 0) se ahorra cálculo, pero la frontera pasa por el origen; Edgardo lo deja para estudiar C2P1 6:06.

### Correcciones y matices
- **Corrección:** en la historia, la tabla de XOR sale mal en la transcripción (1 XOR 1 es 0, no 1) C1P2 1:58:10.
- **Para verificar:** el libro que Edgardo no recuerda es "Perceptrons" de Minsky y Papert (1969), y la salida del invierno vino del perceptrón multicapa entrenado con retropropagación (Rumelhart, Hinton y Williams, 1986) C1P2 1:58:10.
- **Matiz:** Edgardo dice que "lo importante es que W nunca sea cero" C1P2 2:06:39, C2P1 13:18, mientras que Vanessa dice que se puede arrancar en cero C1P2 1:36:57. En el perceptrón arrancar en cero funciona, porque la primera actualización ya mueve w.
- Un alumno pregunta cómo saber el `class_sep` con datos reales: "esta función no existe" con datos reales, "nuestro problema empieza acá" C2P1 14:25.

<details>
<summary>Preguntas de repaso del módulo 4 (con respuestas)</summary>

1. **¿Cuándo está bien clasificada una observación en un clasificador lineal?** Cuando yᵢ f(xᵢ) > 0, es decir, cuando la etiqueta y el score tienen el mismo signo C1P2 1:28:22.
2. **¿Cuál es la regla de actualización del perceptrón y cuándo se aplica?** w ← w + r y x, solo cuando la observación está mal clasificada C1P2 1:39:13.
3. **¿Por qué se usan etiquetas -1/+1?** Porque con y = 0 la actualización no cambia nada C1P2 1:40:54.
4. **¿Qué pasa si los datos no son linealmente separables?** El perceptrón no converge; hay que ir a otros modelos C1P2 1:50:16.

</details>

---

## 5. Regresión logística
**Dónde:** C2P1 24:32, C2P1 25:39, C2P1 30:04, C2P1 32:20, C2P1 33:26, C2P1 35:10, C2P1 35:44, C2P1 38:32, C2P1 41:16, C2P1 46:12, C2P1 46:47, C2P1 50:10, C2P1 53:11, C2P1 54:56, C2P1 56:05, C2P1 1:00:49, C2P1 1:03:27, C2P1 1:05:41, C2P1 1:07:30, C2P1 1:08:45, C2P1 1:11:29, C2P1 1:13:45, C2P1 1:16:34, C2P1 1:21:38, C2P1 1:23:51, C2P1 1:25:55, C2P1 1:29:00

### Conceptos clave
- **Probabilidad en vez de signo.** La regresión logística devuelve P(y | x), una confianza: no es lo mismo 0.51 que 0.99, sobre todo en un diagnóstico médico C2P1 24:32, C2P1 25:39. La sigmoide σ(z) = 1/(1 + e^-z) convierte un número real en una probabilidad, y con 0.5 como umbral decidís la clase C2P1 30:04, C2P1 56:05. "No inventa nada nuevo": es el mismo hiperplano, pero ahora sabés qué tan lejos está cada punto C2P1 32:20.
- **Por qué no el error cuadrático.** El ECM compuesto con la sigmoide da una superficie no convexa con mínimos locales donde el optimizador se puede trabar C2P1 33:26.
- **Máxima verosimilitud.** Cada etiqueta es una Bernoulli: P(y | x) = h^y (1 - h)^(1 - y), con h = σ(θᵀx) C2P1 35:44. Con datos independientes la verosimilitud es un producto; el logaritmo lo pasa a suma por estabilidad numérica, y el signo menos lo convierte en un costo a minimizar: la log loss o entropía cruzada binaria, que es convexa y garantiza que el descenso por gradiente llegue al mínimo global C2P1 35:10, C2P1 38:32. Por partes: -log h si y = 1 y -log(1 - h) si y = 0; "a peor predicción, mayor costo" C2P1 41:16.
- **Criterio de parada.** Salvo con solución cerrada, el costo no llega a cero: se para cuando el cambio es menor a un épsilon C2P1 46:12.
- **Regularización L2 y L1.** L2 (Ridge) achica los pesos sin eliminarlos; L1 (Lasso) lleva pesos exactamente a cero y elimina variables que no aportan. scikit-learn usa L2 por defecto; L1 conviene si sospechás que hay variables que sobran C2P1 46:47.
- **Contra outliers.** Para clasificar, la regresión lineal se mueve mucho con un outlier porque minimiza el ECM, mientras que la logística es más robusta C2P1 50:10. Sobre los outliers: hay que entenderlos, "no es limpiar por limpiar"; se limpian si son errores de carga C2P1 53:11.
- **Intuición de Edgardo.** El perceptrón decide "brusco" y la logística "suave"; es como decir que en el Mundial "los rayados" ganan con 55% C2P1 54:56.
- **Práctico con dígitos.** `load_digits`: 1797 imágenes de 8 × 8 aplanadas en 64 features, con valores de 0 a 16 y clases balanceadas (178 ceros, 182 unos...) C2P1 1:00:49, C2P1 1:03:27. Con `train_test_split(test_size=0.2, random_state=0)` quedan 1437 y 360 C2P1 1:05:41. En `LogisticRegression`, `C` es la inversa de lambda, `fit_intercept=True` y el solver por defecto es `lbfgs` (BFGS por Broyden, Fletcher, Goldfarb y Shanno) C2P1 1:07:30, C2P1 1:33:12.
- **Multiclase con softmax.** Con diez dígitos hay un score lineal por clase y softmax, una "sigmoide multidimensional", los convierte en probabilidades; gana la mayor C2P1 1:08:45. `coef_` es una matriz 10 × 64, una fila por clase y una columna por píxel: para el 1 pesan los píxeles centrales, para el 0 la periferia C2P1 1:11:29, C2P1 1:16:34.
- **Resultados.** 0.97 de exactitud en entrenamiento y 0.96 en validación C2P1 1:21:38. La matriz de confusión (`confusion_matrix` y `ConfusionMatrixDisplay`) tiene la etiqueta real en las filas y la predicha en las columnas: los 27 ceros salen bien y algún 8 se confunde con 1 C2P1 1:23:51. La escala de color sin normalizar engaña: 27 ceros perfectos se ven más claros que 43 seises C2P1 1:25:55. `predict_proba` devuelve probabilidades que suman 1 C2P1 1:29:00.

### Correcciones y matices
- **Corrección:** Edgardo dice que la `tol` por defecto de `LogisticRegression` es 0,001 C2P1 1:07:30. Es 1e-4: lo chequeé en scikit-learn 1.9.1, donde además `max_iter=100`, `C=1.0` y `solver="lbfgs"`. En esa versión el parámetro `penalty` figura como deprecado y la regularización se controla con `l1_ratio` (0.0 por defecto, que equivale a L2) y `C`. La clase se dio con otra versión (para verificar cuál usa Colab).
- **Corrección:** dice que los datos de `load_digits` ya están normalizados C2P1 1:13:45. Vienen de 0 a 16 (chequeado en el box); si querés llevarlos a [0, 1], dividí por 16 o usá un escalador.
- **Corrección:** al hablar de outliers, Vanessa dice "logística" cuando se refiere a la regresión lineal C2P1 32:53, C2P1 50:10.
- **Matiz:** para clases desbalanceadas Vanessa propone ponderar el costo con un peso igual a la proporción de cada clase C2P1 52:35. Ver la corrección del módulo 14: el peso tiene que ser inverso a la frecuencia.
- **Sugerencia:** para la matriz de confusión usá `normalize="true"` y vas a ver tasas por clase en lugar de conteos C2P1 1:25:55.

<details>
<summary>Preguntas de repaso del módulo 5 (con respuestas)</summary>

1. **¿Qué agrega la sigmoide sobre el clasificador lineal?** Una probabilidad: el mismo hiperplano, pero sabiendo qué tan lejos está cada punto C2P1 32:20.
2. **¿Por qué la logística no usa ECM?** Porque con la sigmoide da una superficie no convexa; la log loss es convexa C2P1 33:26, C2P1 38:32.
3. **¿Qué diferencia práctica hay entre L1 y L2?** L1 lleva pesos a cero y elimina variables; L2 los achica sin eliminarlos C2P1 46:47.
4. **¿Qué es `C` en `LogisticRegression`?** La inversa de la fuerza de regularización C2P1 1:07:30.
5. **¿Cómo se lee una fila de `coef_` en el problema de dígitos?** Como el peso de cada píxel para esa clase C2P1 1:11:29.

</details>

---

## 6. Naive Bayes y bolsa de palabras
**Dónde:** C2P2 0:07, C2P2 0:40, C2P2 2:22, C2P2 3:29, C2P2 6:17, C2P2 8:00, C2P2 9:05, C2P2 12:26, C2P2 13:04, C2P2 14:00, C2P2 15:05, C2P2 16:44, C2P2 20:33, C2P2 21:38, C2P2 23:21, C2P2 28:27, C2P2 29:35, C2P2 35:22, C2P2 37:39, C2P2 39:18, C2P2 39:53, C2P2 42:36, C2P2 45:31, C2P2 51:20, C2P2 54:14, C2P2 55:01, C2P2 56:42, C2P2 57:50, C2P2 1:01:49, C2P2 1:02:25, C2P2 1:04:09

### Conceptos clave
- **Bayes da vuelta la probabilidad.** P(x, y) = P(x | y)P(y) = P(y | x)P(x); en spam es más fácil estimar P("gratis" | spam) que lo contrario C2P2 0:40. Es la base de los clasificadores generativos, de los filtros de spam y de diagnósticos médicos C2P2 1:48.
- **El supuesto ingenuo.** Las features son independientes dada la clase, aunque no lo sean ("oferta" y "gratis" van juntas), y aun así funciona bien C2P2 2:22, C2P2 28:27. Se predice con argmax_y P(y) ∏ P(xᵢ | y); el denominador no depende de y C2P2 3:29.
- **Entrenar es contar.** El prior es la proporción de cada clase y la condicional, la frecuencia relativa dentro de la clase. No hay iteraciones, ni tasa de aprendizaje, ni convergencia: es rápido y sirve como baseline C2P2 6:17, C2P2 8:00. Con dígitos de 28 × 28 binarios y 10 clases son 7840 parámetros, muchos menos que un modelo generativo completo C2P2 9:05.
- **Aplicaciones.** Clasificación de texto, análisis de sentimiento, atribución de autoría, plagio y toxicidad C2P2 12:26.
- **Bolsa de palabras.** Antes de los word embeddings, cada palabra es una feature que cuenta apariciones. El vocabulario grande da matrices dispersas con muchos ceros y se pierde el orden de las palabras C2P2 13:04, C2P2 14:00, C2P2 15:05.
- **Suavizado.** Una palabra que no apareció en una clase anula todo el producto; el suavizado aditivo (Laplace con alfa = 1) simula haberla visto una vez y divide por N + alfa|V| C2P2 16:44.
- **Baseline y textos cortos.** Para NLP, Vanessa usaría otro baseline, como FastText con embeddings: un baseline muy pobre "te estás mintiendo vos mismo" C2P2 21:38. Edgardo: NB sirve para textos cortos (un mail, un tweet), no para un libro con sentimientos contradictorios C2P2 23:21.
- **El práctico de spam.** Con priors 50/50 y probabilidades inventadas, "dinero oferta" da 0.28 contra 0.0025, así que es spam C2P2 29:35. Con `CountVectorizer` y `MultinomialNB`, las palabras desconocidas se ignoran C2P2 35:22, C2P2 38:12. NB no dibuja una frontera geométrica ni entiende distancias; aprende probabilidades condicionales C2P2 37:39. A diferencia de la logística, asume independencia C2P2 39:18.
- **China contra Japón.** Tres documentos chinos y uno japonés dan priors 0.75 y 0.25 C2P2 39:53, C2P2 51:20. P(Chinese | china) = 6/14 = 0.43 con suavizado C2P2 54:14. Para "Chinese Chinese Chinese Tokyo Japan" los puntajes son 0.0003 contra 0.0001 y, normalizando, 69% china contra 31% Japón C2P2 55:01, C2P2 56:42. Los puntajes de las dos clases no suman 1 porque no están normalizados C2P2 42:36.
- **Por dentro de scikit-learn.** `vocabulary_` ordena alfabéticamente (Beijing 0, Chinese 1, Japan 2, Macao 3, Shanghai 4, Tokyo 5) y el documento nuevo queda [0, 3, 1, 0, 0, 1] C2P2 57:50. `class_log_prior_` y `feature_log_prob_` guardan logaritmos, porque multiplicar muchas probabilidades chicas da underflow C2P2 1:04:09. "El modelo automático no hace magia, hace lo mismo que el ejemplo manual" C2P2 1:05:50.

### Correcciones y matices
- **Corrección:** Edgardo lee el `predict_proba` como "0,25 japonés y 75 chino" C2P2 1:02:25. Lo corrí en el box con scikit-learn 1.9.1 y da 0.690 para china y 0.310 para Japón, igual que la cuenta a mano. El 0.75/0.25 es el prior.
- **Pregunta respondida después:** Rodrigo pregunta si NB saca las stopwords; Vanessa no lo sabe en el momento C2P2 20:33 y más tarde responde que `CountVectorizer` acepta `stop_words` C2P2 45:31.
- **Para verificar:** el ejemplo China/Japón es el clásico del libro Introduction to Information Retrieval de Manning, Raghavan y Schütze C2P2 39:53.

<details>
<summary>Preguntas de repaso del módulo 6 (con respuestas)</summary>

1. **¿Por qué "ingenuo"?** Porque supone que las features son independientes dada la clase C2P2 2:22.
2. **¿Qué hay que hacer para entrenar Naive Bayes?** Contar: proporciones de clase y frecuencias de cada feature dentro de cada clase C2P2 6:17.
3. **¿Para qué sirve el suavizado de Laplace?** Para que una palabra no vista en una clase no anule todo el producto C2P2 16:44.
4. **¿Qué se pierde con la bolsa de palabras?** El orden de las palabras C2P2 15:05.
5. **¿Por qué scikit-learn guarda logaritmos?** Para evitar el underflow al multiplicar muchas probabilidades chicas C2P2 1:04:09.

</details>

---

## 7. KNN y modelos no paramétricos
**Dónde:** C2P3 0:05, C2P3 0:37, C2P3 1:44, C2P3 2:18, C2P3 2:51, C2P3 3:57, C2P3 5:21, C2P3 5:57, C2P3 6:29, C2P3 7:05, C2P3 17:17, C2P3 19:45, C2P3 20:57, C2P3 21:29, C2P3 22:04, C2P3 24:19, C2P3 27:38, C2P3 32:04

### Conceptos clave
- **Paramétricos contra no paramétricos.** Los paramétricos asumen una geometría fija (recta, curva), calculan pesos y después podés tirar los datos C2P3 0:05. KNN no asume forma: "entrenar" es memorizar todos los datos, que hay que conservar, y la frontera puede ser irregular C2P3 0:37. Ya lo vieron con el imputador de valores faltantes de la materia anterior C2P3 1:44.
- **Cómo predice.** Busca los K vecinos más cercanos según una métrica de distancia y vota por mayoría; K es un hiperparámetro C2P3 2:18. Con K = 1 cada punto de entrenamiento tiene su celda (diagrama de Voronoi) C2P3 5:21. Puede dibujar fronteras arbitrariamente complejas y el caso multiclase es trivial C2P3 5:57.
- **Supuesto i.i.d.** Entrenamiento y prueba vienen de la misma distribución; vale para todos los modelos, y por eso no hay que cambiar la distribución al limpiar C2P3 2:51.
- **Elegir K.** Con K = 1 el error de test sube: sobreajuste C2P3 7:05. Con K = 3 el error es 0.17 en entrenamiento y 0.386 en test; con K = 7, 0.27 y 0.36; con K = 21, 0.269 y 0.314, con una frontera más suave y sin "islitas" C2P3 17:17. Se grafica el error contra K, igual que contra el grado del polinomio C2P3 19:45.
- **Ventajas.** No tiene fase de entrenamiento explícita, es fácil de implementar e interpretar, da fronteras no lineales, es multiclase directo y mejora con más datos C2P3 21:29.
- **Desventajas.** Cada predicción cuesta O(m·n) (m puntos, n dimensiones), depende de la métrica (hay que escalar o normalizar; existe la distancia de Mahalanobis) y ocupa memoria C2P3 20:57, C2P3 22:04. Se mitiga con KD-tree y Ball tree, con vecinos aproximados y con poda de puntos redundantes C2P3 24:19.
- **En la práctica.** Es bueno para entender conceptos, pero casi no se usa en producción, salvo en exploración, sistemas de recomendación o búsqueda con estructuras eficientes C2P3 32:04.

### Correcciones y matices
- **Corrección:** Vanessa dice que con dos clases "conviene elegir un K par" para evitar empates C2P3 6:29. Es al revés: con dos clases conviene un K impar.
- **Corrección (dudoso lo que quiso decir):** dice que el error de clasificación "se usa solamente para entrenar, no para evaluar" C2P3 3:57. Es al revés: como no es diferenciable, no se usa para entrenar, pero sí para evaluar. En la clase 3 ella misma lo dice bien C3P1 1:11:07.

<details>
<summary>Preguntas de repaso del módulo 7 (con respuestas)</summary>

1. **¿Qué guarda KNN después de "entrenar"?** Todos los datos de entrenamiento C2P3 0:37.
2. **¿Qué pasa con K = 1?** La frontera sigue cada punto y el modelo sobreajusta C2P3 7:05.
3. **¿Por qué hay que escalar las variables antes de KNN?** Porque la distancia se dispara con las variables de mayor escala C2P3 22:04.
4. **Con dos clases, ¿K par o impar?** Impar, para evitar empates (corrección de lo dicho en clase) C2P3 6:29.

</details>

---

## 8. Multiclase y multietiqueta
**Dónde:** C2P3 18:30, C2P3 19:15, C2P3 21:58, C2P3 22:31, C2P3 24:44, C2P3 26:47, C2P3 27:35, C2P3 31:17, C2P3 34:43, C2P1 1:08:45

### Conceptos clave
- **Multiclase contra multietiqueta.** En multiclase cada observación tiene una sola clase, excluyente (perro, caballo, pez o pájaro). En multietiqueta puede tener varias a la vez (gato y pájaro en la misma foto) C2P3 18:30. Ejemplos de la clase: enfermedades, temas de un mensaje, géneros de una película, tipo y estado de un cultivo C2P3 19:15.
- **Descomponer en binarios.** Hay dos estrategias: uno contra todos (OvA, también llamado OvR) y todos contra todos (AvA u OvO) C2P3 21:58.
- **OvA.** K clasificadores, cada uno con una clase positiva contra las otras K - 1. Con scores 0.80, 0.65, 0.20 y 0.31 para avión, camión, barco y auto, gana avión. Sirve con cualquier clasificador binario C2P3 22:31. Problemas: cada clasificador está desbalanceado (1 contra 3), los scores no son comparables en teoría aunque en la práctica anda, y aparecen regiones ambiguas C2P3 24:44. La tabla de scores es para una observación, no un puntaje general del modelo C2P3 27:35.
- **AvA.** K(K - 1)/2 clasificadores, cada uno con solo dos clases; es más estable porque no hay desbalance, pero cuesta más, y se decide por votación "como partidos" C2P3 31:17.
- **Softmax.** La regresión logística multiclase da K probabilidades que suman 1, por ejemplo 0.87 para el dígito 3 C2P3 34:43, C2P1 1:08:45.

<details>
<summary>Preguntas de repaso del módulo 8 (con respuestas)</summary>

1. **¿Cuántos clasificadores necesitás con OvA y con AvA para K clases?** K con OvA y K(K - 1)/2 con AvA C2P3 22:31, C2P3 31:17.
2. **¿Cuál es el problema típico de OvA?** Cada clasificador queda desbalanceado C2P3 24:44.
3. **¿Clasificar los géneros de una película es multiclase o multietiqueta?** Multietiqueta, porque puede tener varios a la vez C2P3 19:15.

</details>

---

## 9. Árboles de decisión
**Dónde:** C3P1 0:05, C3P1 0:37, C3P1 1:49, C3P1 5:13, C3P1 6:29, C3P1 7:22, C3P1 9:38, C3P1 10:12, C3P1 12:25, C3P1 13:00, C3P1 14:28, C3P1 22:18, C3P1 23:52, C3P1 28:00, C3P1 29:40, C3P1 31:22, C3P1 32:00, C3P1 34:45, C3P1 36:25, C3P1 38:37, C3P1 42:37, C3P1 44:50, C3P1 49:20, C3P1 53:16, C3P1 54:29, C3P1 59:53, C3P1 1:08:51, C3P1 1:11:07, C3P1 1:12:03, C3P1 1:12:52, C3P1 1:13:16, C3P1 1:15:43, C3P1 1:16:19, C3P1 1:20:46, C3P1 1:23:11, C3P1 1:24:41, C3P1 1:25:55, C3P2 3:16, C3P2 7:53, C3P2 9:37, C3P2 12:15, C3P2 14:28, C3P2 16:51, C3P2 19:18, C3P2 20:53, C3P2 21:52, C3P2 22:55, C3P2 27:56, C3P2 30:03, C3P2 32:17, C3P2 35:55, C3P2 38:07, C3P2 39:34, C3P2 40:21, C3P2 45:31, C3P2 48:25, C3P2 50:37, C3P2 53:35, C3P2 55:42, C3P2 57:54, C3P2 1:00:43, C3P2 1:01:49, C3P2 1:06:10

### Conceptos clave
- **Qué es.** Un árbol aprende reglas `if`/`else` encadenadas, sin pesos, y parte el espacio de features en regiones. Sirve para clasificación y regresión, es multiclase por naturaleza y su gran ventaja es la interpretabilidad: seguís el camino nodo por nodo C3P1 0:37. Es una secuencia de decisiones en lugar de una fórmula global C3P2 3:16.
- **Partes.** Raíz, nodos internos y hojas, con la predicción en la hoja; nunca se retrocede y hay un único camino C3P1 1:49, C3P1 4:41. En regresión la hoja devuelve el promedio de los casos de entrenamiento que cayeron ahí (por ejemplo 340.000 contra 210.000 según superficie y garaje) C3P1 5:13.
- **Usos.** Predicción sin suponer linealidad (crédito, vivienda, reventa de autos), selección de variables, detección de interacciones y recodificación de categóricas C3P1 6:29, C3P1 9:38, C3P1 10:12, C3P1 11:19. Para segmentar necesitás una respuesta: o una proxy ("compró o no") o un clustering previo cuyos grupos el árbol describe C3P1 7:22.
- **Hilo conductor: churn.** 20 clientes de telefonía, con preguntas como "llamadas al soporte > 2", "meses de contrato > 12" y "tiene descuento" C3P1 13:00. Las preguntas son las variables recolectadas y el modelo elige solo preguntas, umbrales y orden C3P1 18:31, C3P1 22:18, C3P1 26:47.
- **Tres propiedades.** Preguntas simples y binarias, de una variable por nodo (la complejidad sale del encadenamiento); grupos mutuamente excluyentes; un camino único y determinístico C3P1 26:07, C3P1 29:40.
- **Voraz.** Encontrar el árbol óptimo es NP-hard, así que en cada nodo se elige el corte que más gana, sin garantía de óptimo global; si la primera pregunta fue mala, lo de abajo hereda el error C3P1 31:22, C3P1 32:00. En cada nodo se prueban todas las variables y puntos de corte, y se mide la impureza con entropía o Gini; "no elige la variable más correlacionada" C3P1 34:45.
- **Impureza.** Gini = 1 - Σ pᵢ²: 0 si el nodo es puro; con 6 y 9 de 15, 0.48 C3P1 14:28, C3P2 45:31. Se interpreta como la probabilidad de equivocarte si etiquetás al azar según las proporciones del nodo C3P2 48:25. Entropía H = -Σ pᵢ log₂ pᵢ, en bits, con máximo 1 en el 50/50 de dos clases C3P1 38:37. En general va de 0 a log₂ n: [0.25, 0.5, 0.25] da 1.5 y tres clases iguales, 1.58 C3P2 1:01:49. Una moneda 99/1 da 0.08 C3P2 1:00:43. La hoja con mezcla asigna la clase mayoritaria C3P1 28:00.
- **Ganancia de información.** IG = H(padre) - Σ (n_hijo/n) H(hijo), siempre ≥ 0 y dependiente del nodo C3P1 44:50. En el ejemplo: el padre tiene 11 de 20 que abandonan, H = 0.993; por "llamadas" quedan 9 puros y 11 con 10 contra 1 (H = 0.439), IG = 0.75; "tiene descuento" da IG 0.02, así que la raíz es "llamadas" C3P1 42:37, C3P1 49:20, C3P1 53:16. Un nodo puro no se divide más y una binaria ya usada no vuelve a aparecer C3P1 59:53.
- **Criterios de impureza.** Error de clasificación, entropía y Gini dan árboles casi idénticos. Gini es más rápido (no tiene logaritmo) y es el default de scikit-learn; la entropía es más sensible cerca del 50/50. El error de clasificación es poco sensible y no se usa para entrenar, sí para evaluar. No vale la pena invertir tiempo en cambiar el criterio C3P1 1:08:51, C3P1 1:11:07, C3P1 1:12:03.
- **Algoritmos.** ID3 (1986): entropía, solo categóricas, sin poda. C4.5 (1993): continuas, poda y gain ratio para no favorecer variables con muchas categorías. CART (1984): Gini, regresión y clasificación, poda; es el que usa scikit-learn C3P1 1:12:52, C3P2 57:54.
- **Variables continuas.** Se evalúan umbrales donde cambia la clase entre observaciones ordenadas, y una continua puede volver a usarse más abajo con otro umbral C3P1 1:20:46, C3P1 1:24:41.
- **Sobreajuste.** Sin criterio de parada cada dato termina en su hoja: "los árboles de decisión, por definición, tienen sobreajuste" C3P1 36:25. Se controla con `max_depth` elegido con la curva de error contra profundidad, `min_samples_split`, `min_samples_leaf`, un umbral mínimo de ganancia y poda C3P1 1:15:43, C3P1 1:16:19, C3P1 1:13:16. Fortalezas: muy usados, fáciles de visualizar, eficientes. Limitaciones: sobreajuste y alta varianza C3P1 1:25:55.
- **El práctico de árboles.** 15 estudiantes ficticios con horas de estudio y asistencia C3P2 9:37. `DecisionTreeClassifier()` sin parámetros y luego con `max_depth=2`, `min_samples_leaf=2`, `random_state=42` C3P2 12:15, C3P2 16:51. `max_depth` controla la complejidad global y `min_samples_leaf` suaviza C3P2 19:18, C3P2 20:53, C3P2 21:52. `plot_tree(..., filled=True)` muestra la raíz "horas_estudio <= 4.5, gini 0.48, samples 15, value [6, 9]" C3P2 22:55, C3P2 27:56. El árbol usó solo las horas; con `min_samples_leaf=1` aparece la asistencia C3P2 24:36, C3P2 35:55. Los defaults son `criterion="gini"`, `splitter="best"`, `max_depth=None`, `min_samples_split=2` y `min_samples_leaf=1` C3P2 39:34, y `criterion` acepta `"gini"`, `"entropy"` y `"log_loss"` C3P2 40:21. Con datos sintéticos tipo OR, el árbol separa de forma no lineal C3P2 1:06:10.

### Correcciones y matices
- **Corrección:** Vanessa dice que los tres criterios "varían entre 0 y 1" C3P1 1:08:51. Con dos clases, Gini y el error de clasificación llegan como máximo a 0.5; la entropía, a 1.
- **Para verificar:** "con 3 categorías hay 6 combinaciones" C3P1 23:52. Las particiones binarias distintas de 3 categorías son 3 (2^(k-1) - 1).
- **Chequeado en el box:** Guillermo pregunta si el umbral para meses de contrato es ≤ 8 o ≤ 12 y Vanessa no sabe cómo lo elige el modelo C3P1 1:23:11. scikit-learn usa el punto medio entre valores consecutivos: con 8 y 12 el umbral es 10.
- **Chequeado en el box:** ante un empate en una hoja, el árbol elige "la primera clase" C3P2 32:17, C3P2 35:04. scikit-learn ordena las clases (orden alfabético para strings) y se queda con la de menor índice.
- **Las cuentas de entropía.** Las recalculé: 0.993, 0.439, IG 0.751 y 0.08 para la moneda 99/1 coinciden con la clase.
- **Corrección:** Edgardo define la exactitud al revés (total sobre aciertos) y un alumno lo corrige C3P2 50:37. Es aciertos sobre total.
- **Corrección:** mezcla el coeficiente de Gini de desigualdad económica con la impureza de Gini ("el Estado quiere que sea lo más parecido a 0.5") C3P2 41:49. Son dos cosas distintas: el coeficiente económico va de 0 (igualdad) a 1 (desigualdad máxima) y se calcula con la curva de Lorenz.
- **Dudoso:** "uno se puede fabricar su propio criterio" C3P2 40:21. `DecisionTreeClassifier` solo acepta los criterios que trae; un criterio propio requiere modificar el código interno.
- **Para verificar:** Edgardo cuenta que Shannon trabajaba en Bell Labs y murió en 2001 C3P2 55:42.
- **El error de la slide del préstamo.** Un alumno nota que "buen historial" está invertido; Vanessa aclara que es un ejemplo ficticio que quedó al revés C3P1 1:49.

<details>
<summary>Preguntas de repaso del módulo 9 (con respuestas)</summary>

1. **¿Qué devuelve la hoja de un árbol de regresión?** El promedio de los casos de entrenamiento que cayeron en ella C3P1 5:13.
2. **¿Por qué se dice que el árbol es voraz?** Porque elige en cada nodo el mejor corte local, sin garantía de óptimo global C3P1 32:00.
3. **Calculá el Gini de un nodo con 6 y 9 casos.** 1 - (0.4² + 0.6²) = 0.48 C3P2 45:31.
4. **¿Qué mide la ganancia de información?** Cuánto baja la impureza al dividir, ponderando cada hijo por su tamaño C3P1 44:50.
5. **¿Qué algoritmo usa scikit-learn?** CART C3P1 1:12:52.
6. **¿Qué hiperparámetros frenan el sobreajuste?** `max_depth`, `min_samples_split`, `min_samples_leaf` y la poda C3P1 1:16:19, C3P2 21:52.

</details>

---

## 10. Ensambles y el práctico de árboles y random forest
**Dónde:** C3P1 32:00, C3P1 1:18:29, C4P1 22:18, C4P1 26:20, C4P1 28:15, C4P1 30:01, C4P1 33:16, C4P1 34:24, C4P1 35:25, C4P1 37:03

### Conceptos clave
- **Random forest.** Cada árbol se entrena con una muestra distinta del dataset y en cada nodo mira un subconjunto aleatorio de variables; como los errores son distintos, se cancelan al promediar (por ejemplo, 100 árboles). Los árboles solos son muy inestables, de alta varianza C3P1 1:18:29, C3P1 32:00.
- **Boosting.** Los árboles se entrenan en secuencia, cada uno sobre los errores del anterior C3P1 1:18:29.
- **El práctico.** `make_moons` con 500 muestras y ruido, separado 70/30 (350 y 150) C4P1 22:18. Un `DecisionTreeClassifier` sin restricciones da exactitud 1.0 en entrenamiento; Edgardo muestra la frontera y `feature_importances_` C4P1 26:20. Con profundidades de 1 a 20, después de 7 u 8 memoriza; compara visualmente 1, 2, 4, 8 y None C4P1 28:15.
- **Configuraciones como diccionarios.** Una lista de dicts pasada con `DecisionTreeClassifier(**cfg, random_state=...)`; una llega a 0.96 en test C4P1 30:01. Compara `gini`, `entropy` y `log_loss` en un for C4P1 33:16.
- **Árbol contra bosque.** Con la matriz de confusión, el random forest llega a 0.96 con una frontera más detallada; después varía `n_estimators` (1, 5, 10...) y mira la importancia de variables del bosque C4P1 34:24, C4P1 35:25.
- **¿Qué `min_samples_leaf` uso?** Mariano pregunta si depende del tamaño del dataset; la respuesta es graficar train y test contra el hiperparámetro, y la experiencia ayuda C4P1 37:03.

<details>
<summary>Preguntas de repaso del módulo 10 (con respuestas)</summary>

1. **¿De dónde sale la diversidad de un random forest?** De muestras distintas por árbol y de subconjuntos aleatorios de variables en cada nodo C3P1 1:18:29.
2. **¿Qué diferencia hay entre bagging (random forest) y boosting?** El bosque entrena árboles independientes y promedia; el boosting los entrena en secuencia corrigiendo errores C3P1 1:18:29.
3. **¿Qué indica una exactitud de 1.0 en entrenamiento con un árbol sin límites?** Que memorizó C4P1 26:20.

</details>

---

## 11. Funciones de costo y optimización
**Dónde:** C3P2 1:07:50, C3P2 1:08:57, C3P2 1:10:24, C3P2 1:11:43, C3P2 1:12:51, C3P2 1:13:53, C3P2 1:16:47, C3P2 1:19:00, C3P2 1:20:45, C3P2 1:21:56, C3P2 1:23:42, C3P2 1:24:15, C3P2 1:25:51, C3P2 1:30:17, C3P2 1:32:32, C3P2 1:35:18, C3P2 1:38:35, C3P2 1:40:57, C3P2 1:42:05, C3P2 1:43:53, C3P2 1:50:39, C3P2 1:52:03, C3P2 1:55:29, C3P2 1:56:30, C3P2 1:58:09, C3P2 2:01:40, C1P2 1:51:22

### Conceptos clave
- **Aprender es optimizar.** L(w) = error de predicción + λ · complejidad; aprender es minimizar L y, además, generalizar, lo que se evalúa en otro conjunto C3P2 1:10:24. "El aprendizaje supervisado es un problema de optimización", y lo que cambia entre modelos es la función de costo C3P2 1:11:43.
- **Solución cerrada contra iterativa.** La regresión con ECM tiene solución cerrada, pero "es una excepción"; la logística con entropía cruzada no la tiene y necesita descenso por gradiente C3P2 1:07:50, C3P2 1:08:57.
- **Repaso de análisis.** En una dimensión, la derivada cero da un punto crítico y la segunda derivada dice si es máximo, mínimo o inflexión. En n dimensiones aparecen el gradiente (las derivadas parciales respecto de cada peso) y la hessiana, que es cara de calcular C3P2 1:12:51, C3P2 1:13:53. El gradiente apunta hacia donde la función más crece, así que se camina en la dirección opuesta; si su módulo es grande, estás lejos del mínimo C3P2 1:16:47.
- **Bajar la montaña.** El perceptrón actualizaba con cada observación mal clasificada; el descenso por gradiente actualiza en la dirección que baja el costo C3P2 1:19:00, C1P2 1:51:22. No hay garantía de llegar al mínimo global C3P2 1:20:45.
- **Tres métodos.** La forma general es w_{t+1} = w_t + α d_t. El descenso por gradiente es de primer orden y zigzaguea; Newton-Raphson usa la curvatura (hessiana), converge más rápido y es caro; el gradiente conjugado incorpora la dirección del paso anterior sin hessiana. En aprendizaje automático, con millones de parámetros, se usa descenso por gradiente o sus variantes C3P2 1:21:56, C3P2 1:23:42. El punto de inicio importa C3P2 1:24:15.
- **Batch, estocástico y mini-batch.** Batch usa todos los datos: es exacto y estable, pero lento y pesado en memoria. El estocástico usa un dato: rápido y ruidoso, puede no converger. El mini-batch usa K datos (32, 64, 128): buena aproximación, aprovecha la GPU y es el más usado. El tamaño del lote es un hiperparámetro C3P2 1:25:51.
- **El algoritmo.** Entradas: dataset, tasa de aprendizaje η y umbral ε. Iniciar w al azar ("cero no"), repetir w ← w - η ∇L hasta que ||∇L|| < ε y devolver w* C3P2 1:32:32.
- **Criterios de parada.** Convergencia natural (gradiente casi cero), máximo de iteraciones como límite de seguridad y early stopping sobre validación; conviene monitorear las curvas de pérdida de train y validación C3P2 1:35:18. Convergencia no es mínimo global: probá varias semillas; si con una converge y con otra no, sospechá de una superficie ruidosa C3P2 1:38:35.
- **Convexidad.** Una función es convexa si el segmento entre dos puntos queda por encima de la curva, y entonces tiene un solo mínimo. Son convexas la regresión lineal con ECM, la logística con log loss y SVM con hinge loss más el término cuadrático; la suma de convexas es convexa; las redes neuronales no lo son C3P2 1:40:57, C3P2 1:42:05.
- **Tasa de aprendizaje.** Muy chica: lenta. Grande: rebota alrededor del mínimo. Muy grande: diverge. El rango común es de 10⁻⁴ a 10⁻¹; se empieza grande y se achica, por ejemplo cada 20 iteraciones sin mejora en validación (un scheduler) C3P2 1:43:53.
- **El ciclo completo.** Datos, parametrización (lineal, polinomial, red), función de costo (ECM, log loss, hinge), optimización con hiperparámetros (λ, η, T), evaluación, y otra vuelta C3P2 1:50:39. Ridge es hiperplano + regularización + ECM; la logística es el mismo hiperplano compuesto con la sigmoide + log loss C3P2 1:58:09.
- **Costo a medida.** En un trabajo sobre fondos financieros Vanessa necesitaba respetar el ranking y no el precio, así que penalizaba los pares invertidos. La función tiene que ser diferenciable y, dentro de lo posible, convexa C3P2 1:52:03, C3P2 1:59:25.
- **Hiperparámetros combinados.** Grid search prueba todas las combinaciones de listas; la búsqueda aleatoria (`RandomizedSearchCV`) muestrea de distribuciones C3P2 2:01:40.

### Correcciones y matices
- **Dudoso:** las figuras de la superficie de costo salieron dibujadas al revés (un máximo en lugar de un mínimo) y Vanessa comenta que "la inteligencia artificial se equivoca y si uno no mira con detalle pasan estas cosas en vivo" C3P2 1:11:43, C3P2 1:16:15. No queda claro si las figuras las generó una IA.
- **Para verificar:** sobre por qué los lotes son potencias de dos, Vanessa no sabe y Edgardo lo atribuye a una optimización de hardware C3P2 1:30:17. Es más que nada una convención; la ganancia real es discutida.
- **Matiz:** "esto corre por debajo de `.fit`" C3P2 1:32:32. No siempre: scikit-learn usa distintos solvers (mínimos cuadrados, lbfgs, coordinate descent) según el modelo.
- **Matiz:** de la hinge loss se dice que "los gradientes desaparecen" C3P2 1:56:30. Lo preciso es que no es diferenciable en el codo y se usa un subgradiente; fuera del margen el gradiente es cero.

<details>
<summary>Preguntas de repaso del módulo 11 (con respuestas)</summary>

1. **¿Por qué la logística necesita descenso por gradiente y la regresión lineal no?** Porque la lineal con ECM tiene solución cerrada y la logística con log loss no C3P2 1:07:50, C3P2 1:08:57.
2. **¿Por qué se resta el gradiente?** Porque apunta hacia donde la función crece más C3P2 1:16:47.
3. **¿Qué ventaja tiene el mini-batch?** Aproxima bien el gradiente, es rápido y aprovecha la GPU C3P2 1:25:51.
4. **¿Qué síntoma tiene una tasa de aprendizaje demasiado grande?** La pérdida rebota o diverge C3P2 1:43:53.
5. **¿Qué es el early stopping?** Cortar cuando la pérdida de validación deja de mejorar C3P2 1:35:18.

</details>

---

## 12. Validación y selección de modelos
**Dónde:** C4P1 0:07, C4P1 4:00, C4P1 5:08, C4P1 7:20, C4P1 7:51, C4P1 9:27, C4P1 9:59, C4P1 11:50, C4P1 13:47, C4P1 17:45, C4P1 18:33, C4P1 19:57, C4P1 20:40, C4P1 39:18, C4P1 40:38, C4P1 43:13, C4P1 44:38, C4P1 49:18, C4P1 51:11, C4P1 54:14, C4P1 59:54, C4P1 1:03:27, C4P1 1:01:56, C4P1 1:05:56, C4P1 1:09:23, C4P1 1:12:15

### Conceptos clave
- **Límites de un solo split.** Con pocos datos los conjuntos chicos tienen alta varianza, el modelo aprende de menos datos y una sola partición puede ser poco afortunada e ignora la estabilidad C4P1 4:00.
- **Remuestreo.** Partir n veces al azar, siempre dentro del entrenamiento, con el test afuera; con reemplazo (bootstrap) o sin reemplazo C4P1 5:08, C4P1 7:20. El remuestreo es para evaluar estabilidad: el modelo final no es un promedio de coeficientes, sino el modelo elegido reentrenado con todos los datos C4P1 7:51. En cada partición se calcula una métrica y se promedia o se toma la mediana C4P1 9:27.
- **Estratificado.** Con clases desbalanceadas un fold se puede quedar sin la clase minoritaria: se separa por clase y se muestrea dentro de cada una. Con 1000 datos al 60/30/10, un test del 20% conserva esas proporciones. "Si tengo clases desbalanceadas, sí o sí muestreo estratificado" C4P1 13:47.
- **Validación cruzada K-fold.** K partes iguales, una para validar y K - 1 para entrenar, rotando: cada observación pasa una vez por validación C4P1 17:45. Vanessa cuenta que en sus datos de salud hay pacientes ruidosos, y que si nunca caen en validación no sabés cómo los predice el modelo C4P1 18:33. Con 800 de entrenamiento y 5 folds de 160 obtenés 5 modelos y promediás C4P1 19:57. Ventajas: mejor estimación y uso de todos los datos; desventaja: más cómputo C4P1 43:13.
- **Para hiperparámetros.** La métrica por defecto es la exactitud; con desbalance, F1 C4P1 9:59. En grid search cada combinación se evalúa en todas las particiones y se promedia (por ejemplo, 80% contra 85%) C4P1 11:50. La búsqueda usa validación cruzada interna y los rangos que le das acotan el espacio de hipótesis C4P1 20:40.
- **scikit-learn.** `cross_val_score(modelo, X, y, cv=5)` C4P1 44:38. `KFold(n_splits=4, shuffle=True, random_state=0)` no garantiza proporciones; `StratifiedKFold` sí (60/40 en cada fold) C4P1 49:18, C4P1 51:11. El número de folds no puede superar la cantidad de casos de la clase menos frecuente: con 3 A y 7 B, como máximo 3 folds; Edgardo lo calcula como el mínimo del conteo por clase C4P1 49:18, C4P1 54:14. Con 10 folds obtiene media 0.75 y desvío 0.33 C4P1 59:54. `cross_validate` acepta varias métricas a la vez (`accuracy`, `precision_macro`, `recall_macro`, `f1_macro`) C4P1 1:03:27.
- **Grillas.** `ParameterGrid` arma todas las combinaciones de `criterion` y `max_depth` C4P1 1:01:56. `GridSearchCV(modelo, param_grid, scoring="accuracy", cv=3)` y `cv_results_` con `mean_test_score`, `std_test_score` y `rank_test_score`; el rank 1 es el mejor (entropy con `max_depth=1`, 0.75 contra 0.60 y 0.70) C4P1 1:05:56.
- **Fuera de programa.** `SGDClassifier` con alfa en escala logarítmica entre 1e-4 y 100 y distintas pérdidas (hinge, modified_huber, squared_hinge, perceptron), con `RandomizedSearchCV`: gana hinge con alfa 0.019 y score 0.84. Es para el resto de la diplomatura; SVM se ve en otra materia C4P1 1:09:23, C4P1 1:12:15, C4P1 1:14:28.

### Correcciones y matices
- **Corrección:** en la notebook la fórmula del promedio aparece como "1/(K - 1) sumando todos menos el j" C4P1 40:38. Lo estándar es promediar las K métricas de validación, una por fold.
- **Corrección:** Edgardo primero dice que el rank más alto es el mejor y después se corrige: el rank 1 es el mejor C4P1 1:05:56.
- **Dudoso:** en el ejemplo de juguete, `predict_proba` da "75% clase A y 24% clase B" C4P1 48:15; probablemente es 0.75 y 0.25 redondeado.

<details>
<summary>Preguntas de repaso del módulo 12 (con respuestas)</summary>

1. **Después de una validación cruzada, ¿cuál es el modelo final?** El elegido, reentrenado con todos los datos de entrenamiento C4P1 7:51.
2. **¿Cuándo es obligatorio estratificar?** Cuando las clases están desbalanceadas C4P1 13:47.
3. **¿Cuántos folds como máximo con 3 casos de la clase minoritaria?** Tres C4P1 49:18.
4. **En `cv_results_`, ¿qué indica `rank_test_score = 1`?** La mejor combinación C4P1 1:05:56.

</details>

---

## 13. Métricas de clasificación y de regresión
**Dónde:** C4P2 7:54, C4P2 9:31, C4P2 12:13, C4P2 16:58, C4P2 18:00, C4P2 22:56, C4P2 27:30, C4P2 30:57, C4P2 38:38, C4P2 42:27, C4P2 44:40, C4P2 48:21, C4P2 28:04, C4P2 29:10, C4P2 31:57, C4P2 32:59, C4P2 34:58, C4P2 37:45, C4P2 41:46, C4P2 42:56, C4P2 44:02, C4P2 45:42, C4P2 48:31, C4P2 53:36, C4P3 0:02, C4P3 3:53, C4P3 6:07, C4P3 7:50, C4P3 30:39, C4P3 31:12, C4P3 33:13, C4P3 34:33, C4P3 36:26, C4P3 39:09, C4P3 40:18, C4P3 41:24, C4P3 42:50, C4P3 44:09, C4P3 48:40, C4P3 50:11, C4P3 51:30, C4P3 52:01, C4P3 54:53

### Conceptos clave
- **Costo contra métrica.** La función de costo es lo que se optimiza, una aproximación; la métrica captura el objetivo real, reconociendo que no todos los errores cuestan lo mismo. La exactitud y F1 no son diferenciables, por eso no se optimizan directamente C4P2 7:54. Las métricas sirven para comparar contra un modelo base, seguir la evolución y alinear al equipo técnico con el negocio C4P2 9:31. "La función de costo guía el aprendizaje, la métrica da la evaluación y la toma de decisiones" C4P3 32:39.
- **Dos familias de clasificadores.** Los de salida directa (KNN, árboles) y los basados en score (logística, SVM), que necesitan un umbral; en la logística es 0.5 por defecto, pero se puede cambiar C4P2 12:13.
- **Matriz de confusión.** Con 20 clientes de churn ordenados por score y umbral 0.5: TP 9, FP 2, FN 1 y TN 8 C4P2 16:58, C4P2 27:30. El total y las sumas por clase real son fijos; lo que depende del umbral es el reparto de las predicciones C4P2 27:30. Subir el umbral da menos positivos y más falsos negativos; bajarlo, más positivos y más falsos positivos C4P2 22:56.
- **Qué error es peor.** El de tipo I es el falso positivo y el de tipo II el falso negativo. En un diagnóstico médico pesa más el tipo II; en spam, el tipo I (un mail importante a la basura: "si se te pierde como les pasó con la Diplo, estamos en el horno"). Eric agrega el caso de las valijas con bombas en un aeropuerto C4P2 30:57.
- **Las cuatro métricas.** Exactitud = (9 + 8)/20 = 85%, engañosa con desbalance: con 1% de bombas, 99% sin detectar nada C4P2 38:38. Precisión = TP/(TP + FP) = 9/11 = 81%, importa cuando el falso positivo cuesta C4P2 42:27. Recall = TP/(TP + FN) = 9/10 = 90%, importa cuando el falso negativo cuesta; predecir todo positivo da recall 1 C4P2 44:40. F1 es la media armónica, que penaliza los extremos: 0.857 en el ejemplo, más cerca del valor menor C4P2 48:21, C4P2 28:04. F1 no usa los verdaderos negativos C4P2 28:04.
- **La métrica sigue al objetivo.** No dejes la exactitud por defecto al buscar hiperparámetros si no responde tu pregunta C4P2 29:10. "La métrica no se elige por comodidad técnica, se elige en función del problema real": recall en diagnóstico, precisión en alertas, F1 para equilibrio, ROC AUC o PR AUC para comparar clasificadores C4P3 36:26.
- **El umbral.** Se elige con el modelo ya entrenado, porque la función de costo usa probabilidades C4P2 31:57. Hay tantos umbrales efectivos como ejemplos más uno, los que quedan entre scores consecutivos C4P2 32:59. En la tabla de umbrales del ejemplo, el mejor F1 está en 0.50, el default de `predict` C4P2 34:58, C4P2 36:40.
- **Curva ROC.** TPR (recall) contra FPR (1 - especificidad), un punto por umbral; se busca el más cercano a la esquina superior izquierda, y la diagonal es el modelo aleatorio C4P2 37:45. El AUC mayor a 0.5 dice que el modelo aprende algo, sirve para comparar modelos independientemente del umbral y para elegir el umbral C4P2 41:46.
- **Curva PR.** Con muchos negativos el FPR queda bajo aunque haya muchos falsos positivos y la ROC engaña; la curva de precisión contra recall se mira en ese caso C4P2 42:56. Su baseline es la proporción de positivos: con 10 de 20 es 0.5 y el AUPRC del ejemplo es 0.81; con 100 de 1000 sería 0.10 C4P2 45:42.
- **ROC con validación cruzada.** O juntás todas las predicciones (si los scores son comparables entre folds) o trazás una curva por fold y mostrás la promedio con una banda de desvío, que habla de la estabilidad; lo mismo se hace con las curvas de pérdida C4P2 48:31, C4P2 52:39.
- **Multiclase.** La matriz es n × n y las métricas se calculan por clase con uno contra todos C4P3 0:02. El macro promedia por clase "democráticamente" (F1 0.67, 0.40 y 0.67); el micro suma TP, FP y FN de todas las clases (6, 4 y 4) y calcula una métrica global, donde pesan más las clases grandes C4P3 3:53, C4P3 6:07. `classification_report` devuelve los dos C4P3 7:50.
- **Train, validación, test y campo.** Una métrica se puede calcular en los tres conjuntos y, más adelante, contra lo que pasó en la realidad; comparar train y test muestra el sobreajuste C4P3 33:13.
- **Más métricas.** Especificidad y valor predictivo negativo (NPV = TN/(TN + FN)), que scikit-learn no trae y hay que definir C4P3 39:09. Manuel menciona el coeficiente de correlación de Matthews y ninguno de los docentes lo conoce C4P3 17:41.
- **Regresión.** MSE (positivo, penaliza errores grandes, unidades al cuadrado; con errores 2, 2 y 3 da 5.67), RMSE (mismas unidades que el target, como un desvío estándar), MAE (más robusto a los extremos) y R² = 1 - SS_res/SS_tot (1 perfecto, 0 igual que predecir la media, negativo peor que la media; "si da 1 hay que sospechar") C4P3 40:18, C4P3 41:24, C4P3 42:50. Edgardo grafica |e|, e² y e⁴: subir la potencia castiga más los errores grandes y menos los chicos C4P3 44:09.
- **En código.** `accuracy_score`, `precision_score`, `recall_score`, `f1_score`, `confusion_matrix(...).ravel()` para sacar tn, fp, fn y tp, `roc_curve`, `roc_auc_score` y `precision_recall_curve` C4P3 50:11, C4P3 52:01, C4P3 54:53. Ojo con la división por cero: si una clase nunca se predice aparece `UndefinedMetricWarning` C4P3 51:30.

### Correcciones y matices
- **Corrección:** Vanessa dice que F1 refleja qué tan bien se clasifican "ambas clases" y en un momento dice "media aritmética" donde quiere decir armónica C4P2 48:21. F1 solo mira la clase positiva; para evaluar las dos clases, usá F1 macro o balanced accuracy.
- **Corrección:** al describir la curva PR dice que "con umbral muy alto el modelo predice todos positivos" C4P2 44:02. Con umbral alto predice pocos positivos: precisión alta y recall bajo.
- **Dudoso:** en la tabla de umbrales, con umbral 1 la precisión figura como 1 C4P2 34:58. Es 0/0, indefinida; scikit-learn devuelve 0 con una advertencia, salvo que cambies `zero_division`.
- **Convención de la matriz.** En la slide de Vanessa las columnas son la etiqueta real C4P2 18:00; en scikit-learn las filas son la real y las columnas la predicha C4P3 52:01, C2P1 1:23:51. Fijate siempre cómo está armada antes de leerla.
- **Corrección:** Edgardo nombra "true negative rate" en un eje de la ROC C4P3 54:53. Los ejes son FPR (x) y TPR (y).
- **Para verificar:** en el ejemplo binario de la notebook, precisión 0.6 y recall 0.8 van con F1 0.72 C4P3 50:11. Con esos valores la F1 es 0.686 (lo calculé); puede ser otro cálculo o un redondeo.
- **Dudoso:** la definición de NPV en pantalla se lee como "true negative sobre la suma total" C4P3 39:44. La correcta es TN/(TN + FN).
- **Para verificar:** el coeficiente de Matthews existe en scikit-learn como `matthews_corrcoef` (lo importé sin problema en el box) y se recomienda con clases desbalanceadas C4P3 17:41.
- **Las cuentas.** Recalculé 85%, 9/11, 90%, F1 0.857, micro 0.6 y MSE 5.67 (RMSE 2.38): coinciden.
- Los alumnos notan que en la lista de la slide faltan dos puntos verdes: "qué detallistas que son" C4P2 22:03.

<details>
<summary>Preguntas de repaso del módulo 13 (con respuestas)</summary>

1. **¿Por qué no se optimiza la exactitud directamente?** Porque no es diferenciable C4P2 7:54.
2. **Con TP 9, FP 2, FN 1 y TN 8, calculá precisión y recall.** 9/11 ≈ 0.82 y 9/10 = 0.90 C4P2 42:27, C4P2 44:40.
3. **¿Cuándo preferís la curva PR a la ROC?** Con clases desbalanceadas C4P2 42:56, C4P2 45:42.
4. **¿Qué diferencia hay entre macro y micro average?** Macro pesa igual cada clase; micro suma los conteos y pesa más las clases grandes C4P3 3:53, C4P3 6:07.
5. **¿Qué significa un R² negativo?** Que el modelo es peor que predecir la media C4P3 42:50.
6. **¿Cuándo se elige el umbral?** Con el modelo ya entrenado C4P2 31:57.

</details>

---

## 14. Clases desbalanceadas
**Dónde:** C4P3 8:36, C4P3 9:05, C4P3 9:43, C4P3 11:41, C4P3 13:13, C4P3 13:26, C4P3 19:22, C4P3 26:35, C4P3 27:07, C2P1 52:35, C4P1 13:47

### Conceptos clave
- **El problema.** El modelo se sesga hacia la clase mayoritaria y la clasifica mejor que a la minoritaria C4P3 8:36.
- **Submuestreo.** Sacar ejemplos de la mayoritaria hasta equilibrar; es simple, pero podés perder información valiosa C4P3 9:05.
- **Sobremuestreo.** Inventar casos de la minoritaria con sentido. SMOTE crea ejemplos sintéticos interpolando entre instancias reales de la clase minoritaria; ADASYN hace algo parecido pero da más peso a los ejemplos difíciles, los que quedan cerca del umbral; en imágenes se rota o distorsiona C4P3 9:43. Los datos inventados tienen que parecerse a los reales para no meter sesgo C4P3 13:26.
- **Ponderar la función de costo.** No tocás los datos y multiplicás cada parte del costo por un peso de clase C4P3 11:41. Se prefiere porque no cambia la distribución original de los datos, que es la que vas a encontrar al predecir C4P3 13:13. Vanessa recomienda empezar por acá C4P3 26:35.
- **Duplicar sin más.** Copiar exactamente los ejemplos minoritarios equivale a un remuestreo con reemplazo. Edgardo advierte que depende del problema: si tenés un solo precio de un barrio, duplicarlo no enseña nada y, si el dato es malo, empeora; en física puede generar datos sintéticos con modelos, pero "no me puedo poner a inventar enfermedades" C4P3 19:22. Vanessa: los electrocardiogramas no se pueden inventar, solo alterar un poco C4P3 26:35.
- **Resumen de la clase.** Con desbalance, la exactitud no sirve: usá precisión, recall, F1, ROC AUC para la separabilidad general y la matriz de confusión por clase. En el postproceso, mové el umbral sin reentrenar, eligiéndolo con la curva PR. En el preproceso, pesos o remuestreo C4P3 27:07.

### Correcciones y matices
- **Corrección importante:** Vanessa dice que el peso de cada clase "es la proporción de datos" (con 60/40, la parte positiva se multiplica por 0.60) C4P3 11:41, C2P1 52:35. Así se favorece todavía más a la mayoritaria. El peso tiene que ser inverso a la frecuencia; en scikit-learn, `class_weight="balanced"` usa n / (k · n_clase).
- **Corrección:** dice que SMOTE "duplica ejemplos existentes" C4P3 9:43. SMOTE no duplica: genera puntos nuevos sobre el segmento entre un ejemplo minoritario y uno de sus vecinos minoritarios.
- **Sugerencia:** el remuestreo se aplica solo al conjunto de entrenamiento, dentro de cada fold, nunca antes de separar el test.

<details>
<summary>Preguntas de repaso del módulo 14 (con respuestas)</summary>

1. **¿Por qué se prefiere ponderar el costo antes que remuestrear?** Porque no altera la distribución original de los datos C4P3 13:13.
2. **¿Qué peso le corresponde a la clase minoritaria?** Uno mayor, inverso a su frecuencia (corrección de lo dicho en clase) C4P3 11:41.
3. **¿En qué se diferencia SMOTE de duplicar?** SMOTE interpola entre vecinos y crea puntos nuevos C4P3 9:43.
4. **¿Qué podés hacer después de entrenar, sin reentrenar?** Mover el umbral, eligiéndolo con la curva PR C4P3 27:07.

</details>

---

## 15. Los trabajos prácticos
**Dónde:** C2P3 37:09, C2P3 37:48, C2P3 38:36, C2P3 40:34, C2P3 43:52, C2P3 44:26, C2P3 46:41, C2P3 47:48, C2P3 49:38, C2P3 50:34, C2P3 51:41, C2P3 52:14, C2P3 52:53, C1P2 46:45, C1P2 1:25:22, C4P3 59:37, C4P3 1:00:27, C4P3 1:01:21, C4P3 1:02:12, C4P3 1:03:13, C4P3 1:04:05, C4P3 1:05:11, C4P3 1:06:39, C4P3 1:08:45, C4P3 1:10:55, C4P3 1:12:02, C4P3 1:13:28

### Práctico 1: "Regresión en California"
- **Entrega:** 8 de junio de 2026 C2P3 37:09, C4P3 59:37. Edgardo lo había anunciado al cierre de la clase 1 como un ajuste multidimensional C1P2 1:25:22.
- **Datos:** California Housing (`fetch_california_housing` de scikit-learn), 20.640 instancias y 8 atributos numéricos de un censo: MedInc, HouseAge, AveRooms, AveBedrms, Population, AveOccup, Latitude y Longitude. El target está en cientos de miles de dólares C2P3 37:48, C2P3 40:34. Con 80/20 quedan 16.512 y 4.128 C2P3 43:52. Según Edgardo, "ya viene limpita", pero hay que hacer un análisis exploratorio básico C2P3 49:38.
- **Objetivo:** justificar las elecciones e interpretar los errores: qué modelo elegirías y por qué, y cómo reconocés el underfitting y el overfitting C2P3 38:36.
- **Partes:** 1) preguntas sin código sobre el dataset, el target, los atributos más y menos determinantes, sesgos, riesgos y dilemas éticos C2P3 44:26; 2) un gráfico de cada atributo contra el target C2P3 46:41; 3) regresión lineal con un solo atributo, ECM en train y test, gráfico e interpretación C2P3 47:48; 4) regresión polinomial con varios grados, curva de error contra grado y punto de sobreajuste C2P3 50:34; 5) dos o tres atributos C2P3 51:41. Opcionales: todos los atributos y Ridge con distintos alfa C2P3 52:14.
- **Reflexión sobre IA:** contar si usaron ChatGPT, Claude u otras, para qué y qué corrigieron; "cómo saben que la IA no les mintió"; "los responsables de los resultados son ustedes" C2P3 52:53. Edgardo ya lo había dicho con la analogía del médico que firma el informe aunque lo ayude una herramienta C1P2 46:45.
- **Para verificar:** Edgardo dice que con algunos atributos el error de test debería quedar "menor a 50", y con polinomios "menor a 40, incluso 35" C2P3 47:48, C2P3 50:34. No aclara las unidades; con el target en cientos de miles de dólares, un ECM de 50 no tiene sentido, así que puede referirse a otra escala (dudoso).
- **Corrección:** Edgardo lee el target 4.526 como "52.000 aproximadamente" C2P3 40:34. Son unos 452.600 dólares.

### Práctico 2: un esquema completo de aprendizaje automático
- **Entrega:** 22 de junio de 2026 ("ya confirmo", para verificar) C4P3 59:37.
- **Consigna:** armar un esquema de aprendizaje automático sobre datos de clasificación: selección de modelo, ajuste de hiperparámetros y evaluación C4P3 1:00:27. Los datos son de clientes de un banco y la pregunta es a quién prestarle; el archivo tiene líneas de comentario con "#" que se saltean al leerlo con pandas C4P3 1:00:27, C4P3 1:05:11. La descripción de las variables está en esos comentarios y en el GitHub de la diplomatura C4P3 1:13:28.
- **Flujo pedido:** entender el problema y el dataset, identificar el target, mirar el balance de clases, separar train y test (estratificado), entrenar, ajustar hiperparámetros con validación cruzada, evaluar con métricas apropiadas, comparar y justificar una recomendación. La pregunta central: "¿qué modelo recomendaríamos y con qué evidencia lo justificamos?" C4P3 1:01:21.
- **Métricas mínimas:** exactitud, precisión, recall, F1 y matriz de confusión, interpretadas: si el modelo clasifica igual de bien las dos clases, cuántos falsos positivos y negativos hay, qué métrica importa más C4P3 1:02:12.
- **Análisis exploratorio mínimo:** tamaño, nombres y tipos de variables, faltantes, distribuciones, target y desbalance C4P3 1:03:13.
- **Costo del error:** qué error es más costoso para el banco y cuál para el cliente, y qué métrica controla cada uno C4P3 1:04:05.
- **Preguntas orientadoras:** de qué se trata el dataset, qué significan las clases 0 y 1, qué variables pueden ser importantes o estar relacionadas, qué información adicional le pedirías al banco C4P3 1:06:39.
- **Parte 2:** `SGDClassifier` con hiperparámetros por defecto (solo la semilla fija), evaluado en train y test; después `GridSearchCV` o 5-fold, con `best_params_`, `best_score_`, media y varianza del score. Preguntarse qué pérdida usa, qué defaults tiene y por qué la tasa de aprendizaje y la regularización importan C4P3 1:08:45.
- **Parte 3:** lo mismo con `DecisionTreeClassifier`: primero por defecto y después ajustado (profundidad, sobreajuste, criterio, `max_depth`, `min_samples_leaf`) C4P3 1:10:55.
- **Conclusión:** mejor modelo e hiperparámetros, qué métrica y por qué, estabilidad entre folds, sobreajuste, qué error preocupa más, si lo usarías en un caso real y con qué advertencias, en una tabla comparativa; "no copiar números" C4P3 1:12:02.
- **Corrección:** al plantear el costo del error, Edgardo llama "falso negativo" tanto a aprobar un préstamo que no debía aprobarse como a rechazar uno que sí C4P3 1:04:05. Uno de los dos es un falso positivo; cuál depende de qué clase tomes como positiva.
- **Para verificar:** el dataset parece ser HMEQ (préstamos con garantía hipotecaria), que la diplomatura publica en su GitHub; en ese caso el target indica incumplimiento, no "si se le dio el préstamo", como se dice en clase C4P3 1:05:11. Revisá la descripción del archivo.
- **Chequeado en el box:** en scikit-learn 1.9.1, `SGDClassifier` usa por defecto `loss="hinge"`, `alpha=0.0001`, `penalty="l2"`, `max_iter=1000`, `tol=0.001` y `learning_rate="optimal"`.

<details>
<summary>Preguntas de repaso del módulo 15 (con respuestas)</summary>

1. **¿Qué tiene que mostrar la parte 4 del práctico 1?** La curva de error contra el grado del polinomio y dónde empieza el sobreajuste C2P3 50:34.
2. **¿Qué pregunta central guía el práctico 2?** Qué modelo recomendarías y con qué evidencia C4P3 1:01:21.
3. **¿Qué métricas mínimas pide el práctico 2?** Exactitud, precisión, recall, F1 y matriz de confusión, interpretadas C4P3 1:02:12.
4. **¿Quién es responsable si usaste IA?** Vos C2P3 52:53.

</details>

---

## Glosario y nombres deformados en la transcripción

| En la transcripción | Qué es |
|---|---|
| "CONISET" | CONICET |
| "Villamaría" | Universidad Nacional de Villa María |
| "nodu", "nobulos" | notebooks |
| "cycle learn", "cycit learn", "sakarn" | scikit-learn |
| "M classification" | `make_classification` |
| "vallas" | bias, el término independiente b |
| "Sord" | XOR |
| "Rosenbl" | Frank Rosenblatt |
| "Inspect", "ISPEC" | módulo `inspect` de Python |
| "Mardam" | Markdown |
| "resapha", "resape" | `reshape` |
| "Jamie Kight" | Gemini (dudoso) |
| "la" (como regularización) | Lasso |
| "softmap" | softmax |
| "Naí Valles", "valles" | Naive Bayes, Bayes |
| "waring bedings" | word embeddings |
| "comorized" | `CountVectorizer` |
| "FastEx" | FastText |
| "Borono" | diagrama de Voronoi |
| "el volt" | Ball tree |
| "pobreza" (en árboles) | pureza |
| "NPJAR" | NP-hard |
| "max dep" | `max_depth` |
| "byes" | bits |
| "Conrado" | Corrado Gini |
| "Claus Shanon" | Claude Shannon |
| "Genny", "Ginopy" | Gini, Gini y entropía |
| "miniqu error", "min square error" | mean squared error |
| "false", "fals", "fo" | folds |
| "Cafold", "CFOL", "Stratifier" | `KFold`, `StratifiedKFold` |
| "cross bar score" | `cross_val_score` |
| "parámeter grid" | `ParameterGrid` |
| "lif" | leaf (`min_samples_leaf`) |
| "acuracy", "acurais", "cura así", "acúes" | accuracy, exactitud |
| "récord", "recol", "rico" | recall |
| "curva rock", "R cube" | curva ROC, `roc_curve` |
| "trillol", "trillón", "trisol" | threshold, umbral |
| "SMOE" | SMOTE |
| "adasín" | ADASYN |
| "Matthw" | coeficiente de correlación de Matthews |
| "NPB" | NPV, valor predictivo negativo |
| "intancia" (tomografía) | tomografía por impedancia eléctrica |
| "supervector machine", "soporte vector" | support vector machine (SVM) |
| "Vietma", "Iberra" | apellidos de Luis y Yanina, coordinadores de mentorías (dudosos) |

| Término | Definición breve |
|---|---|
| Espacio de hipótesis | Conjunto de funciones que obtenés variando los parámetros de un modelo |
| Parámetro | Valor que aprende el entrenamiento (los pesos) |
| Hiperparámetro | Valor que fijás antes de entrenar (grado, K, profundidad, lambda, tasa de aprendizaje) |
| — | El modelo memoriza el entrenamiento y generaliza mal |
| Regularización | Penalizar la complejidad (pesos grandes) dentro del costo |
| Log loss | Entropía cruzada; el costo de la regresión logística |
| Softmax | Generalización de la sigmoide a K clases |
| Suavizado de Laplace | Sumar 1 a los conteos para no tener probabilidades cero |
| Impureza | Medida de mezcla de clases en un nodo (Gini, entropía, error) |
| Ganancia de información | Reducción de impureza al dividir un nodo |
| Validación cruzada | Rotar el conjunto de validación entre K partes y promediar |
| Estratificar | Mantener la proporción de clases en cada partición |
| Umbral | Valor del score a partir del cual se predice la clase positiva |
| AUC | Área bajo la curva ROC; 0.5 es azar |
| AUPRC | Área bajo la curva de precisión contra recall; su baseline es la proporción de positivos |
