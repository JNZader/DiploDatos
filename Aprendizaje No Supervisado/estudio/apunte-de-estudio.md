# Apunte de estudio: Aprendizaje No Supervisado (Diplodatos, FAMAF UNC, Laura Alonso Alemany y Georgina Flesia)

**Curso:** Aprendizaje No Supervisado, la quinta y última materia obligatoria de la Diplomatura en Ciencia de Datos, Aprendizaje Automático y sus Aplicaciones de FAMAF (UNC), cohorte 2026 · Docentes: Laura Alonso Alemany (la parte general, embeddings, semisupervisado, reglas de asociación, grafos y recomendación) y Georgina Flesia (clustering y las notebooks) · Coordinación: Carolina Chavero ("Caro") · Formato: cuatro clases sincrónicas grabadas en 8 videos no listados del canal FAMAF UNC: viernes 24 de julio a la tarde, sábado 25 de julio a la mañana, viernes 7 de agosto a la tarde y sábado 8 de agosto a la mañana de 2026. En las grabaciones solo se dicen los nombres de pila; los apellidos salen del sitio de la diplomatura, que lista a ambas en el equipo docente, y el calendario publicado coincide con las cuatro fechas.
**De qué va:** la materia arranca con qué es aprender sin etiquetas y por qué es tan difícil evaluar lo que sale. La primera mitad es clustering: distancias, escalado, K-means, mezclas de gaussianas, mean shift, DBSCAN y jerárquicos, con métricas internas (inercia, silueta, BIC) y externas contra "testigos", todo sobre el dataset de jugadores del videojuego FIFA. La segunda mitad recorre embeddings (selección y agrupamiento de características, PCA, t-SNE, UMAP, LSA, LDA y embeddings neuronales), por qué los modelos de lenguaje se consideran no supervisados, aprendizaje semisupervisado, reglas de asociación, análisis de redes sociales y sistemas de recomendación. Hay un único trabajo especial: clustering sobre FIFA 24 de Kaggle, aprobado con 70%.

> Nota: este apunte sale de los subtítulos automáticos en español de los 8 videos. Siete tienen transcripción completa de la grabación. La de C3P2 no se pudo bajar (la grabación devolvió "demasiadas solicitudes" en todos los reintentos espaciados) y se rehízo con faster-whisper a partir del audio (ver la sección "Lo que falta"). Muchos nombres vienen deformados (ver el glosario al final). Todo lo que figura acá es lo que se dice en clase. Cuando lo que se dijo está mal o es impreciso, lo marco como **Corrección**. Las cifras, fechas y afirmaciones que no chequeé están marcadas como **para verificar**. Algunas cosas sí las chequeé: los valores por defecto y el comportamiento de scikit-learn corriendo la versión 1.9.1 en el box (y la 1.6.1, parecida a la de Colab, cuando cambia algo), mlxtend 0.25, networkx 3.7, umap-learn 0.5 y Yellowbrick 1.5, y algunos hechos con una búsqueda web. Eso está dicho en cada caso. Lo que no se entiende bien en la transcripción va como **dudoso**. Las ideas mías van marcadas como **Sugerencia**.

**Cómo leer los links:** cada link dice el video y el minuto. "C2P1 1:23:45" es la clase 2, parte 1, en la hora 1, minuto 23, segundo 45.

## Los 8 videos

| # | Id | Video | Contenido | Duración | Link |
|---|---|---|---|---|---|
| 1 | — | C1P1: Clase 1, parte 1 (24/07/2026 17:47) | Presentación, qué es el aprendizaje no supervisado, causas latentes, evaluación, hoja de ruta de la materia | 1:15:59 |  |
| 2 | — | C1P2: Clase 1, parte 2 ("Recording 2") | Clustering: planteo, el dataset FIFA, escalado, distancias y similitudes, familias de algoritmos, K-means, GMM, mean shift | 2:10:10 |  |
| 3 | — | C2P1: Clase 2, parte 1 (25/07/2026 09:50) | Relación con ANOVA, DBSCAN, comparación en datos de juguete, jerárquicos, notebook de K-means en FIFA, inercia, silueta, testigos, mean shift | 1:44:34 |  |
| 4 | — | C2P2: Clase 2, parte 2 ("Recording 2") | GMM y BIC, linkages, PCA, Yellowbrick, métricas externas, consigna del trabajo especial, uso de LLM | 1:43:31 |  |
| 5 | — | C3P1: Clase 3, parte 1 (07/08/2026 17:55, "Recording01") | Puesta en común del práctico, cómputo y nube, protección de datos, Cloudflare, embeddings: selección de características, PCA, t-SNE, UMAP, LSA, LDA | 1:54:56 |  |
| 6 | — | C3P2: Clase 3, parte 2 ("Recording 02") | Notebook de embeddings (PCA, t-SNE, UMAP sobre FIFA), embeddings neuronales y tareas de pretexto (transcripción con faster-whisper, ver "Lo que falta") | 1:23:06 |  |
| 7 | — | C4P1: Clase 4, parte 1 (08/08/2026 09:50, "Recording01") | Modelos de lenguaje como no supervisado, pesos abiertos, barreras de seguridad, aprendizaje semisupervisado | 1:56:27 |  |
| 8 | — | C4P2: Clase 4, parte 2 ("Recording 2") | Reglas de asociación, análisis de redes sociales, sistemas de recomendación, cierre y consejos para el trabajo | 1:36:21 |  |

Duración total: 13:45:04 (unas 13 horas y 45 minutos).

**Cómo se determinó el orden.** Los títulos traen la clase y la fecha y hora de grabación, y la segunda parte de cada clase es "Recording 2" o "Recording 02". Los ocho se subieron en dos tandas (27/07 y 10/08), así que la fecha de subida no ordena dentro de cada clase. El contenido encadena: C1P1 cierra con "frenamos y tomamos mate 15 minutos" C1P1 1:15:01 y C1P2 arranca con la parte de clustering de Georgina C1P2 0:03; C1P2 termina con "mañana: conectividad y jerárquicos" C1P2 2:08:25, que es lo que se ve en C2P1 C2P1 14:20, C2P1 30:01; C2P1 corta en el recreo anunciando métricas y el trabajo especial C2P1 1:43:02 y C2P2 sigue con eso C2P2 1:48, C2P2 1:16:14. C3P1 termina con la pausa y la promesa de ver la notebook de t-SNE y PCA y después los embeddings neuronales C3P1 1:53:56, que es el contenido de C3P2: arranca con "empezamos de vuelta" y la notebook de embeddings C3P2 0:00 y cierra con "arrancamos mañana retomando esto", sobre los modelos de lenguaje C3P2 1:21:47. C4P1 arranca retomando "por donde veníamos ayer" con los modelos de lenguaje C4P1 2:22 y corta a las 12 con la pausa C4P1 1:56:23; C4P2 sigue con reglas de asociación, redes y recomendación, que eran los temas que quedaban.

## Mapa de módulos y videos

| Módulo | Dónde se ve |
|---|---|
| 0. La materia: quiénes la dan, plan, materiales y contexto | C1P1 (inicio y final), C2P1 (inicio), C3P1 (inicio), C4P2 (final) |
| 1. Qué es el aprendizaje no supervisado y por qué cuesta evaluarlo | C1P1 |
| 2. Clustering: el planteo, los datos, el escalado y las distancias | C1P2, C2P1 (inicio) |
| 3. Algoritmos de clustering | C1P2, C2P1, C2P2 |
| 4. Elegir K y evaluar un clustering | C2P1, C2P2, C3P1 (inicio) |
| 5. El caso FIFA en las notebooks | C1P2, C2P1, C2P2, C3P1 (inicio) |
| 6. Cómputo, nube y datos personales | C3P1 (inicio), C4P1 (inicio) |
| 7. Embeddings y reducción de dimensión | C1P1, C2P2 (final), C3P1, C3P2 |
| 8. Embeddings neuronales y modelos de lenguaje | C1P1, C3P2, C4P1 |
| 9. Aprendizaje semisupervisado y otras formas de supervisión débil | C1P1, C4P1 |
| 10. Reglas de asociación | C1P1, C4P2 |
| 11. Análisis de redes sociales y grafos | C1P1, C4P2 |
| 12. Sistemas de recomendación | C4P2 |
| 13. El trabajo especial | C1P2, C2P2, C3P1, C4P2 |

---

## 0. La materia: quiénes la dan, plan, materiales y contexto
**Dónde:** C1P1 0:04, C1P1 2:55, C1P1 4:00, C1P1 6:12, C1P1 1:05:58, C1P1 1:08:15, C1P1 1:13:54, C2P1 0:31, C3P1 22:15, C4P2 1:34:17

### Conceptos clave
- **Laura.** Se presenta como lingüista, con más de 20 años en tratamiento automático del lenguaje, desde el lado empírico, y dice que hizo mucho clustering C1P1 2:55. Georgina cuenta que Laura fue la primera directora de la diplomatura, hace unos 8 años, y que después la dirigió ella C1P1 1:05:58. Laura se define como española en C3P1 ("a la hora de terminar se me cae la lapicera") C3P1 1:53:56.
- **Georgina.** Es la "experta en clustering" C1P1 2:55, trabaja hace 30 años en procesamiento de señales C1P1 1:11:38 y con imágenes de microscopio C2P1 44:34. Su formación estadística aparece todo el tiempo: el problema no identificable, ANOVA, EM.
- **Otras personas que aparecen.** Carolina, la coordinadora, astrónoma C1P1 2:55; Luis Biedma (la transcripción dice "Vietma"), coordinador de mentorías C1P1 1:08:15; Jorge Sánchez, que según Laura armó con ella la idea de los temas y "trajo" t-SNE C1P1 1:08:15, C3P1 1:02:21; Diego, que da la optativa de modelos de lenguaje C4P1 27:28; Luciana, que da Ética con Laura C4P2 1:34:17; Damián, que da la optativa de cálculo distribuido (su apellido no se dice, **dudoso**) C3P1 6:52.
- **El plan.** El primer fin de semana es clustering con Georgina y la consigna del práctico C1P1 4:00. El segundo, comentarios del práctico, embeddings, semisupervisado, reglas de asociación, redes y grafos y sistemas de recomendación C1P1 6:12, C3P1 22:15. Georgina anuncia "tres notebooks para estas 8 horas": cuándo un método no anda, cuándo anda y cuándo le puedo dar información para que ande mejor C1P1 1:13:54.
- **Materiales.** Filminas en el aula virtual "actualizadas al estilo 2026" y notebooks de Colab cuyas preguntas son las del entregable C2P1 0:31. La clase 4 no estaba activada en el aula virtual al empezar y Laura la activa en vivo C4P1 1:49.
- **Postura sobre los asistentes de IA.** Laura avisa que si hacen todo con Claude ("clot") el práctico sale "un Shein, un Temu": lo promedio, lo obvio C1P1 1:49. En el cierre, Georgina pide hacer el trabajo primero y recién después comparar con lo que dice el modelo C4P2 1:30:56.
- **Cierre de las obligatorias.** Carolina se conecta al final: con esta materia terminan las obligatorias, Ética empieza en 15 días con Laura y Luciana, y las optativas siguen (series temporales y finanzas hacia octubre) C4P2 1:34:17.

### Preguntas de repaso
1. ¿Qué dos fines de semana tiene la materia y qué se ve en cada uno?
2. ¿Qué "tres notebooks" promete Georgina y qué pregunta responde cada una?

---

## 1. Qué es el aprendizaje no supervisado y por qué cuesta evaluarlo
**Dónde:** C1P1 6:44, C1P1 8:59, C1P1 10:03, C1P1 11:12, C1P1 14:02, C1P1 16:17, C1P1 17:58, C1P1 22:54, C1P1 26:13, C1P1 28:25, C1P1 30:36, C1P1 33:28, C1P1 37:55, C1P1 40:10, C1P1 1:03:45

### Conceptos clave
- **Muchos nombres para lo mismo.** Análisis exploratorio de datos (como lo llaman los ingenieros), detección de anomalías, data mining (hace 20 o 30 años), business intelligence y KDD, knowledge discovery in databases, que propone un alumno C1P1 6:44, C1P1 8:59.
- **La diferencia con supervisado.** No hay clases. Lo que se busca son patrones que caractericen **causas latentes** de los fenómenos que observamos C1P1 10:03. El ejemplo: segmentar clientes de un supermercado con datos de tarjetas de fidelización; los grupos (los que compran el fin de semana, a diario, después del cierre de la tarjeta, con promociones) responden a causas que no se ven directamente C1P1 11:12. Cuando Agustín pregunta si causa latente es lo mismo que correlación, Laura responde que la correlación es el método, no la causa C1P1 12:55.
- **Cuándo usarlo.** Cuando no sabemos bien qué queremos, cuando sospechamos de los datos (fraude, grupos raros, epidemias) o cuando queremos terminar de definir las clases. "El paciente siempre miente", como en Dr. House, y los datos también C1P1 14:02. Si el objetivo estuviera claro, etiquetaríamos y haríamos supervisado; la intención (una campaña, ubicar productos en góndolas) es lo que da criterio C1P1 15:10.
- **Los datos nunca son crudos.** La intuición falsa es "meto la base y salen las clases". Hay decisiones antes: qué variables, cómo segmentar la edad, aplicar logaritmo a distribuciones muy sesgadas, sacar características irrelevantes C1P1 17:58, C1P1 19:34. Un ejemplo clásico: la primera segmentación sale por género porque es binario e informativo; si eso no sirve para la pregunta, conviene sacar el atributo C1P1 16:17.
- **Dónde está el costo.** En supervisado se paga etiquetar; en no supervisado se paga analizar los resultados, y hace falta alguien que sepa del dominio C1P1 22:54. Por eso el práctico es sobre fútbol: todos pueden opinar con criterio C1P1 24:35, C1P1 25:41.
- **Temas relacionados.** ANOVA y test de hipótesis, proyecciones y embeddings, reglas de asociación, vecinos más cercanos, recomendación, detección de anomalías ("la inversa del clustering"), grafos y modelos de lenguaje C1P1 26:13.
- **El problema central: no hay evaluación intrínseca.** No hay definición de error ni gold standard C1P1 28:25. La mejor evaluación es el impacto en el uso real, un test A/B ("la posta no es accuracy"), pero es carísimo y no se puede hacer con 50 modelos C1P1 30:36. Las métricas geométricas (compacidad) no garantizan utilidad C1P1 32:19. Queda la **evaluación anecdótica**: elegir casos, al azar o dirigidos, y mirar en qué grupo caen C1P1 33:28.
- **Pensamiento crítico ante el resultado.** Cualquier agrupamiento se puede "leer" como un test de Rorschach. Los asistentes de IA dicen lo más probable y suena bien. Hay que preguntar cuántos casos tienen la característica y cuántos la tienen en los otros grupos C1P1 37:55.
- **Aplicaciones.** Carrito de compras, segmentación de mercado, tipologías de pacientes o estudiantes, comportamiento de usuarios, fallas en producción, fraude, temas en documentos, objetos en imágenes y comunidades en redes C1P1 40:10, C1P1 41:52.
- **Evaluación, otra vez.** Al final de la clase un alumno se queja de lo difícil que es evaluar. Las respuestas: expertos de dominio, impacto en producción y reproducibilidad, es decir estabilidad del resultado ante perturbaciones C1P1 1:03:45.

### Correcciones y matices
- **Para verificar.** Laura cuenta la anécdota de los pañales y la cerveza como "años 80, creo" y aclara que en la realidad no pasaba C1P1 26:13, C1P1 40:10. La versión más citada viene de un análisis de Osco Drug con Teradata de 1992 y nunca se usó para mover góndolas; no lo pude confirmar con una fuente primaria.
- **Corrección.** Laura menciona por primera vez el caso Enron como "una petrolera" que quebró a fines del siglo XX y dice que "el juez pidió los mails" C1P1 42:26. Enron era una empresa de energía y comercialización de gas y electricidad, quebró en diciembre de 2001, y el corpus de correos lo hizo público la FERC (el regulador federal de energía de EE.UU.) durante su investigación. El caso vuelve en C4P2 (sección 11).

### Preguntas de repaso
1. ¿Por qué no hay una evaluación intrínseca en clustering y qué tres formas de evaluar quedan?
2. ¿Qué es una causa latente y por qué la correlación no es lo mismo?
3. Dá un ejemplo de una decisión previa sobre los datos que cambia lo que sale del clustering.

---

## 2. Clustering: el planteo, los datos, el escalado y las distancias
**Dónde:** C1P2 0:03, C1P2 1:08, C1P2 11:43, C1P2 14:35, C1P2 17:23, C1P2 19:35, C1P2 21:48, C1P2 32:06, C1P2 37:05, C1P2 39:57, C1P2 48:28, C1P2 1:34:07, C1P2 1:37:00, C1P2 1:41:35, C1P2 1:44:57, C1P2 1:47:14, C2P1 3:18, C2P1 3:53

### Conceptos clave
- **Un problema no identificable.** Georgina arranca desde la estadística: en un problema clásico el parámetro existe aunque no lo conozcas; en clustering no sabés si la partición que buscás existe C1P2 1:08. Si suponés que los datos vienen de una mezcla de gaussianas y la estimás, ahí sí tenés un problema estadístico bien planteado C1P2 2:47. Por eso no hay una única respuesta y distintos algoritmos dan respuestas distintas C1P2 19:35.
- **Entrada y salida.** La entrada es una matriz de n objetos por m variables (en el ejemplo, los skills de los jugadores de FIFA, de 0 a 100) C1P2 11:43. La salida es una partición con cohesión alta dentro de cada grupo y separación alta entre grupos, que son objetivos opuestos y necesitan una distancia C1P2 14:35, C1P2 1:34:07.
- **Las categóricas parten solas.** Una variable categórica divide los datos como un GROUP BY de SQL. Conviene sacarla, ver si aparece otra división y usarla después para interpretar C1P2 17:23.
- **Más variables no es mejor.** De 80 variables quizás te quedás con 40, y tal vez 3 o 4 son las que separan C1P2 32:06, C1P2 34:16. Georgina logró su mejor división con dos variables de cincuenta C1P2 50:43.
- **Pedir contexto.** El peor caso es una tabla sin contexto: hay que saber qué se midió, cómo y cuándo C1P2 37:05.
- **Escalar es obligatorio.** Precio en millones, edad entre 20 y 38 y skills de 0 a 100 no se pueden mezclar en una distancia euclídea sin escalar C1P2 48:28. Las herramientas son StandardScaler, MinMaxScaler y Normalizer, y para categóricas OneHotEncoder u OrdinalEncoder C1P2 1:34:07, C1P2 1:36:28. Georgina insiste en el cierre de la materia: "no escalar son dos puntos menos en cualquier examen de ciencia de datos" C2P2 1:11:15.
- **Distancias de magnitud.** Euclídea y Manhattan son casos de Minkowski (p = 2 y p = 1); con p infinito es Chebyshev, la de los movimientos del rey en el ajedrez C1P2 1:41:35, C1P2 1:43:19. Mahalanobis pesa por la matriz de covarianza, no depende de la escala y sirve con gaussianas no esféricas (elipses en vez de círculos) C1P2 1:38:43.
- **Distancias para secuencias.** Levenshtein cuenta las operaciones para pasar de una cadena a otra C1P2 1:44:57.
- **Similitudes de ángulo.** Coseno, Tanimoto, correlación y producto escalar ignoran la magnitud (el brillo de una imagen) y sirven para datos de alta dimensión y dispersos. Se maximiza la similitud y se minimiza la distancia C1P2 1:45:32, C1P2 1:47:49. En alta dimensión las distancias pierden contraste C1P2 1:47:14.
- **Imágenes.** Un dígito corrido tres píxeles cambia mucho la distancia euclídea C1P2 39:57.

### Correcciones y matices
- **Corrección.** Georgina presenta Normalizer como "normalizar, vector con norma uno" junto a los escaladores de variables C1P2 1:34:07. En scikit-learn Normalizer lleva **cada fila** (cada jugador) a norma 1, no cada variable. Lo chequeé en el box: [1, 2] pasa a [0,447; 0,894]. Para escalar columnas se usan StandardScaler o MinMaxScaler.
- **Matiz.** Dice que si los datos fueran binarios Levenshtein "se llamaría Hamming" C1P2 1:44:57. Hamming solo cuenta sustituciones entre cadenas de igual longitud; Levenshtein también admite inserciones y borrados.
- **Matiz.** Laura dice que coseno y correlación están muy relacionados C2P1 3:18. Exacto: la correlación de Pearson es el coseno entre los vectores centrados (a cada uno le restás su media).
- **Para verificar.** Georgina dice que hay "una notebook" donde la euclídea no funciona y el coseno sí con K-means C1P2 43:21. KMeans de scikit-learn no tiene parámetro de métrica (en 1.9.1 sus parámetros son n_clusters, init, n_init, max_iter, tol, verbose, random_state, copy_x y algorithm); el truco habitual es normalizar las filas con Normalizer y después correr K-means, lo que equivale a trabajar con coseno.

### Preguntas de repaso
1. ¿Qué quiere decir que clustering es un problema no identificable?
2. ¿Qué hace Normalizer y por qué no es lo mismo que StandardScaler?
3. ¿Cuándo preferirías una similitud coseno a una distancia euclídea?

---

## 3. Algoritmos de clustering
**Dónde:** C1P2 1:50:07, C1P2 1:50:44, C1P2 1:51:17, C1P2 1:51:53, C1P2 1:53:40, C1P2 1:55:25, C1P2 1:57:04, C1P2 1:59:16, C1P2 2:03:17, C1P2 2:05:30, C2P1 9:55, C2P1 12:36, C2P1 14:20, C2P1 19:58, C2P1 30:01, C2P1 35:02, C2P1 41:48, C2P2 2:22, C2P2 4:03, C2P2 11:26, C2P2 13:39, C2P2 17:03, C2P2 21:02, C2P2 23:17, C2P2 25:00

### Conceptos clave
- **Cuatro familias.** Particionales (K-means y sus primos), basados en densidad de probabilidad (GMM, mean shift), basados en densidad de puntos y conectividad (DBSCAN, OPTICS, DENCLUE) y jerárquicos C1P2 1:50:07, C1P2 1:58:10.
- **K-means.** Elegís K centroides, asignás cada punto al más cercano, recalculás cada centroide como el promedio y repetís hasta que nada cambia C1P2 1:59:16, C2P1 9:55. Es rápido porque con distancia euclídea al cuadrado el centro óptimo es el promedio C1P2 1:51:53. Es el más usado y Laura recomienda empezar siempre por él como exploración barata, antes de "los cañones grandes" C2P1 17:43, C2P1 42:53.
- **PAM, CLARA y CLARANS.** El centro es un elemento real (un medoide). Es más lento porque calcula todas las distancias, pero los centros tienen sentido C1P2 1:51:17, C1P2 1:51:53.
- **Mezcla de gaussianas (GMM) y EM.** Modela los datos como una suma de gaussianas; EM alterna entre asignar probabilidades y reestimar medias, covarianzas y pesos C1P2 2:03:17, C2P2 5:13, C2P2 7:29. Da una distribución de probabilidad, no solo centros C1P2 2:03:50. Cada covarianza completa tiene n(n+1)/2 parámetros, así que necesita muchos datos; con diagonal, esférica o compartida ("tied") hay menos parámetros, y un modelo más simple bien estimado puede ser mejor que uno completo mal estimado C2P2 2:22, C2P2 3:28, C2P2 11:26. Se suele inicializar con la partición de K-means C2P2 4:03.
- **Mean shift.** Una ventana de ancho fijo (bandwidth) se mueve hacia la media de su entorno hasta llegar a una moda; cada moda es un cluster. Es un estimador de densidad por kernel y el bandwidth es difícil de elegir C1P2 2:05:30, C2P1 11:33.
- **DBSCAN.** Dos parámetros: el radio eps y el mínimo de vecinos min_samples. Encadena puntos densos y deja como ruido (etiqueta -1) los sueltos. Encuentra formas que ninguna distribución conocida genera (cintas, espirales, letras de una patente) pero junta grupos que están muy cerca C1P2 1:55:25, C2P1 12:36, C2P1 14:20, C2P1 16:02.
- **Jerárquicos aglomerativos.** Unen de abajo hacia arriba y un punto nunca sale del grupo en que se unió (a diferencia de K-means, que reacomoda todo) C2P1 30:01. La historia de uniones es el dendrograma, que se corta para obtener K grupos C2P2 17:03. El linkage define la distancia entre grupos: single (la mínima), complete (la máxima), average, centroide y Ward (la unión que menos aumenta la varianza) C2P2 21:02, C2P2 23:17. Un truco: correr el jerárquico hasta 7 grupos para ver qué se une con qué y después pedirle 7 a K-means o a GMM C2P2 19:52.
- **Qué anda en los datos de juguete.** Con la figura de comparación de scikit-learn: en círculos concéntricos y lunas, K-means y mean shift cortan con una línea y DBSCAN acierta C2P1 19:58, C2P1 21:06; en gaussianas alargadas solo GMM acierta C2P1 23:52; en ruido uniforme K-means igual da 3 grupos "porque se lo pedí" C2P1 25:31. Entre los jerárquicos, single linkage es el único que resuelve círculos y lunas pero une de más, y Ward es el único que separa las tres gaussianas C2P2 25:00, C2P2 26:40.
- **Una señal útil.** Si los métodos de densidad dicen "todo ruido" o "un solo grupo", probablemente hay una mezcla: probá GMM, o K-means si es caro C2P1 41:48.
- **La etiqueta del cluster es arbitraria.** El "cluster 2" de una corrida no tiene por qué ser el "cluster 2" de otra; para comparar hay que emparejarlos C2P1 24:59.
- **Relación con ANOVA.** ANOVA testea si las medias de grupos conocidos son iguales; GMM es como el problema inverso: no sabés cuántos grupos hay C2P1 3:53, C2P1 4:30.

### Correcciones y matices
- **Corrección.** Georgina dice que K-means "teóricamente con cualquier partición inicial encuentra la óptima, lo cual no ocurre en la vida" C1P2 1:59:16. K-means converge siempre, pero a un óptimo **local** que depende del inicio. En scikit-learn eso se ataca con init="k-means++" (el valor por defecto) y varias corridas con n_init, quedándose con la de menor inercia.
- **Para verificar, y en scikit-learn es falso.** "K-means está adaptado a muchísimas distancias" C1P2 2:02:09 y "se adapta a distintas similaridades" C2P1 17:43. KMeans de scikit-learn solo usa euclídea (lo chequeé en 1.9.1: no tiene parámetro metric). Para otras distancias hay que ir a K-medoids (paquete aparte, scikit-learn-extra) o transformar los datos.
- **Corrección.** Georgina presenta MiniBatchKMeans como una variante "para evitar mínimo local" C2P1 19:58. MiniBatchKMeans existe para ir más rápido con muchos datos, usando minilotes; los mínimos locales se atacan con k-means++ y n_init.
- **Matiz.** Dice que K-means es "el estimador no paramétrico" de una mezcla de gaussianas C1P2 1:50:44. Lo correcto es que K-means es un caso límite de GMM con covarianzas esféricas iguales y asignación dura. En C4P1 Laura lo dice bien: K-means es "una instancia particular de EM" C4P1 1:19:09.
- **Matiz.** Dice que GMM usa "pseudo máxima verosimilitud" C1P2 2:03:17. EM maximiza la verosimilitud; lo que se garantiza es un máximo local.
- **Corrección.** Explica average linkage como "el promedio de la distancia más baja" C2P2 23:17. Average es el promedio de **todas** las distancias entre pares de puntos de A y de B.
- **Matiz.** Dice que la covarianza diagonal supone variables independientes C2P2 3:28. Supone independencia **dentro de cada componente**; en la mezcla completa las variables pueden estar correlacionadas.
- **Chequeado.** En scikit-learn 1.9.1 GaussianMixture tiene covariance_type="full" e init_params="kmeans" por defecto, y trae los métodos bic y aic C2P2 4:03.
- **Para verificar.** En la comparación de jerárquicos dice que average linkage y DBSCAN son los únicos que encadenan C2P1 35:02; en la figura de scikit-learn el que encadena es single linkage, que es lo que ella misma dice después C2P2 25:00.
- **Para verificar.** La anécdota de un KNN con 50 vecinos sobre 18.000 puntos que tardó 45 minutos contra 2 segundos de un random forest C2P1 26:43 es rara para ese tamaño en scikit-learn; puede depender de la máquina o de la implementación.

### Preguntas de repaso
1. ¿Por qué K-means es rápido y qué precio pagás por eso?
2. ¿Qué parámetros tiene DBSCAN y qué significa la etiqueta -1?
3. ¿Qué diferencia hay entre single, complete, average y Ward?
4. Si DBSCAN te devuelve todo como ruido, ¿qué te está diciendo y qué probás después?

---

## 4. Elegir K y evaluar un clustering
**Dónde:** C2P1 52:25, C2P1 58:05, C2P1 1:01:42, C2P1 1:02:16, C2P1 1:06:09, C2P1 1:16:54, C2P1 1:18:37, C2P1 1:21:27, C2P2 1:48, C2P2 11:26, C2P2 12:00, C2P2 41:01, C2P2 42:40, C2P2 44:22, C2P2 47:10, C2P2 48:49, C2P2 49:58, C2P2 52:11, C2P2 1:04:02, C2P2 1:12:23, C2P2 1:42:59, C3P1 0:38

### Conceptos clave
- **Inercia y codo.** La inercia es la suma de los cuadrados de las distancias de cada punto a su centroide C2P1 52:25. Siempre baja al subir K, hasta llegar a cero con un grupo por punto, así que se mira el "codo" de la curva C2P1 1:02:16, C2P2 42:40.
- **Silueta.** Para cada punto compara la distancia promedio a su propio grupo con la distancia al grupo vecino; el promedio resume el agrupamiento y no supone ninguna distribución C2P1 58:05. Los valores negativos ("chorreadas" en el gráfico) son puntos que estarían mejor en otro grupo C2P1 1:01:42. En la puesta en común, Laura dice que entre codo y silueta "a mí me gusta más la silueta" C3P1 0:38.
- **BIC y AIC para GMM.** Como GMM tiene verosimilitud, se pueden comparar número de componentes y tipo de covarianza con BIC o AIC; gana el más bajo. En el ejemplo, "full" con 2 componentes C2P2 11:26, C2P2 12:00, C2P1 6:38.
- **Testigos.** Casos que conocés bien (Messi, el Dibu, los arqueros) y que te dan una "verdad de campo" parcial. Son filas, no columnas, y permiten restricciones del tipo "Messi no puede quedar con el Dibu"; si quedan juntos, buscá la variable que hace ruido C2P1 1:21:27. El experto de dominio da unos 10 testigos por grupo, nunca una etiqueta por objeto C2P2 1:04:02. Si los testigos quedan mezclados, el algoritmo dividió solo porque se lo pediste C2P1 1:18:37.
- **Clustering no es clasificación.** Las posiciones de los jugadores son validación externa, no clases, y la relación no es uno a uno: "Messi no es un 10, es un todo" C2P1 1:06:09. En no supervisado el concepto es "soft"; en clasificación, "hard" C2P1 1:18:37.
- **Métricas externas.** Contra los testigos se miden homogeneidad (cada grupo tiene una sola clase), completitud (cada clase cae en un solo grupo), V-measure (su promedio pesado), el índice de Rand ajustado (ARI) e información mutua C2P2 47:10, C2P2 48:49, C2P2 49:58. Georgina arma una tabla con una fila por agrupamiento y una columna por métrica C2P2 52:11.
- **Yellowbrick.** KElbowVisualizer dibuja el codo y marca un K sugerido; también hay un visualizador de silueta C2P2 41:01, C2P2 44:22.
- **Opción de rechazo.** En lugar de forzar a cada caso a un grupo, dejar una franja intermedia, como cuando el médico pide otro estudio C2P2 1:12:23.
- **Advertencia.** "Puedo hacer que cualquier métrica me diga lo que yo quiera" eligiendo la muestra C2P2 1:42:59.

### Correcciones y matices
- **Corrección.** Georgina dice que "el que tiene la inercia más chica me permite decidir que este K es mejor que otro K" C2P1 52:25. Como la inercia siempre baja al subir K, elegir el mínimo te lleva al K más grande. Sirve para comparar corridas con el **mismo** K (por eso KMeans se queda con la de menor inercia entre las n_init) y para buscar el codo. Ella misma lo aclara más tarde C2P1 1:02:16.
- **Para verificar.** "Cuando el valor medio baja de 0,4 no es un buen cluster" C2P1 1:01:42. No hay un umbral universal; una regla citada a menudo (Kaufman y Rousseeuw) habla de 0,5 a 0,7 como estructura razonable y más de 0,7 como fuerte, pero depende de los datos.
- **Corrección.** "Las métricas van entre 0 y 1" C2P2 52:11. Homogeneidad, completitud y V-measure sí, pero el ARI puede ser negativo cuando el acuerdo es peor que el azar. Lo chequeé en el box: adjusted_rand_score([0,0,1,1], [0,1,0,1]) da -0,5.
- **Corrección, chequeada.** Georgina llama "fit" o "estimador de fit" a la segunda curva de KElbowVisualizer C2P2 41:01. Esa curva es el **tiempo** de ajuste de cada K: en Yellowbrick 1.5 el parámetro timings vale True por defecto y la métrica por defecto es "distortion" (la inercia). No mide calidad.
- **Sugerencia, chequeada.** Yellowbrick 1.5 anda con scikit-learn 1.6.1, pero con la 1.9.1 falla al crear el visualizador ("The supplied model is not a clustering estimator"), porque pregunta por el atributo `_estimator_type`, que scikit-learn ya no define; en Python 3.12 o más nuevo, además, hay que instalar setuptools para que importe. Si te pasa, dibujá inercia y silueta a mano (está en la guía de implementación).
- **Matiz.** "Dos siempre te da un cluster muy grande y uno muy chico" C2P2 42:40. Pasa en FIFA porque los arqueros se separan del resto, pero no es una regla general.
- **Matiz.** Dice que con varios inicios de K-means "hay métodos que promedian, votan las etiquetas" C2P1 1:41:19. KMeans de scikit-learn no vota: corre n_init veces y se queda con la de menor inercia. Votar entre corridas es otra técnica (clustering por consenso).

### Preguntas de repaso
1. ¿Por qué no podés elegir K tomando la inercia mínima?
2. ¿Qué es un testigo y en qué se diferencia de una etiqueta de clase?
3. ¿Qué mide la homogeneidad y qué la completitud? ¿Cuál de las métricas externas puede ser negativa?

---

## 5. El caso FIFA en las notebooks
**Dónde:** C1P2 53:42, C1P2 55:25, C1P2 56:34, C1P2 1:00:03, C1P2 1:04:58, C1P2 1:17:34, C1P2 1:20:21, C1P2 1:23:15, C1P2 1:27:54, C2P1 49:36, C2P1 51:16, C2P1 54:11, C2P1 57:31, C2P1 1:04:30, C2P1 1:13:26, C2P1 1:28:51, C2P1 1:33:28, C2P1 1:36:54, C2P2 28:28, C2P2 30:15, C2P2 35:57, C2P2 39:21, C2P2 53:49, C2P2 56:39, C2P2 1:01:46, C3P1 3:34, C3P1 4:39

### Conceptos clave
- **Los datos.** FIFA 18 y 19 del videojuego de EA Sports, porque los docentes conocen a los jugadores; ustedes trabajan con FIFA 24 de Kaggle C1P1 24:35, C1P2 53:42. En las versiones viejas no está Lamine Yamal C2P1 1:21:27. El 19 se baja de una URL del GitHub de la diplomatura y el 18 solo está en el aula virtual ("estos datos ya no existen más en Kaggle"): guarden copia C2P2 30:15, C2P2 37:09.
- **La pregunta.** ¿Se pueden separar las posiciones de juego a partir de los skills? Las posiciones se usan solo para evaluar, nunca para agrupar C1P2 55:25, C1P2 1:17:34. Es como en teledetección: unos píxeles de referencia curados (pasto, agua, cultivos) sobre los que se mide la coincidencia C1P2 1:18:41.
- **Columnas difíciles.** Valores y salarios con símbolos, puntajes por posición tipo "85+3" que vienen como texto, NaN en las columnas de posición para los arqueros C1P2 58:20, C1P2 1:00:03, C1P2 1:07:14.
- **Factores.** Los skills vienen agrupados (attacking, skill, movement, defending, goalkeeping). Para visualizar no pongas dos variables del mismo factor, porque están muy correlacionadas C1P2 1:04:58, C1P2 1:23:15. Finishing contra sliding tackle separa bien; interceptions contra sliding tackle pega arqueros con delanteros C1P2 1:20:21.
- **Filtrar.** Con overall mayor a 70 quedan unos 5.000 jugadores; Georgina trabajó con todo el 24 C1P2 1:15:51, C2P1 49:36.
- **K-means con K = 4.** Sobre los 34 skills, mirando dos variables: los primeros de cada grupo son los testigos (Suárez, Hazard, Neymar, Ronaldo y Messi en uno; los arqueros en otro; Modric; Godín) C2P1 53:35, C2P1 57:31. La tabla cruzada grupo por posición muestra arqueros perfectos y medio campo mezclado con defensa y ataque: "¿qué es medio campo?" C2P1 1:04:30, C2P1 1:10:37. Sin arqueros aparece la misma media luna C2P1 1:13:26.
- **Mean shift y DBSCAN no andan en FIFA.** Mean shift con bandwidth 1 encontró 4.747 grupos y con 1,5 uno solo C2P1 1:28:51; DBSCAN con eps 0,1 marcó a todos como ruido C2P1 1:33:28. Los datos son "flat", sin montañas de densidad, y DBSCAN encadena C2P1 1:31:13, C2P1 1:35:11.
- **Ward en dos variables.** Georgina admite que "hizo trampa": corrió el jerárquico en dos variables y le dio parecido a K-means con 34, señal de que sobran variables C2P1 1:36:54.
- **PCA, escalado y métricas.** Sin escalar, PC1 explicaba el 94% de la varianza y K-means cortaba vertical; al escalar, las métricas suben, y en dos variables bien elegidas suben más; complete linkage le dio el mejor resultado C2P2 35:57, C2P2 53:49, C2P2 56:39, C2P2 1:01:46.
- **La puesta en común (clase 3).** Eric hizo selección de características y vio tres grupos (arqueros puros y dos mixtos) más que cuatro, y usó un dendrograma; Laura: si las características no separan, ningún método sofisticado separa C3P1 3:34, C3P1 4:39.

### Correcciones y matices
- **Para verificar.** El 94% de varianza en la PC1 C2P2 35:57 es típico de datos sin escalar: una o dos variables de rango grande dominan. Georgina lo reconoce después ("no la escalé") C2P2 53:49.
- **Corrección.** "Usualmente el bandwidth es 0,5 o 0,7" C2P1 1:28:51. El bandwidth depende de la escala de los datos. scikit-learn trae estimate_bandwidth; en los dígitos 8x8 sin escalar da unos 42,8 (chequeado en el box).
- **Para verificar.** Al probar bandwidth 6, el error que lee Georgina dice que no encontró ningún punto y sugiere otra estrategia C2P1 1:28:51; no reproduje ese caso exacto.
- **Matiz, inconsistencia de la clase.** Georgina aconseja usar PCA para visualizar y no para armar los grupos, pero en la notebook corre K-means sobre 15 componentes y muestra 2 C2P2 39:21. Las dos cosas son válidas si se dice qué se hizo; para el trabajo conviene reportar ambas variantes.
- **Para verificar.** Que la mayoría de los jugadores de overall bajo sean defensores C2P1 49:36 es algo que Georgina "leyó"; se puede chequear con el propio dataset.

### Preguntas de repaso
1. ¿Por qué las posiciones no se usan para agrupar y para qué sí se usan?
2. ¿Por qué mean shift y DBSCAN fallan con los skills de FIFA?
3. ¿Qué te dice que Ward en dos variables dé parecido a K-means en 34?

---

## 6. Cómputo, nube y datos personales
**Dónde:** C3P1 5:13, C3P1 6:52, C3P1 8:00, C3P1 11:16, C3P1 12:25, C3P1 14:01, C3P1 16:14, C3P1 18:25, C3P1 20:38, C3P1 21:43, C4P1 13:28

### Conceptos clave
- **No corras todo en tu compu.** Eric tardó 15 minutos en su computadora; Laura recomienda servidores o la nube C3P1 5:13. Opciones: el CCAD de la UNC (la transcripción dice "SECAT"), gratis para investigadores y contratable; la optativa de cálculo distribuido con Damián; la optativa de AWS C3P1 6:52, C3P1 7:27.
- **Usar bien el cluster.** Georgina advierte que mucha gente manda trabajos al cluster y usa un solo hilo: hay que entender memoria contra procesamiento y elegir herramientas multihilo o GPU C3P1 8:00.
- **Cuentas y créditos.** Las cuentas del CCAD se piden por Damián o por afiliación a la UNC; según Laura la UNC tiene un convenio con AWS para docencia con 100 dólares de crédito por alumno C3P1 11:16.
- **Datos personales.** Laura dice que, por la Ley de Protección de Datos, los datos personales "no deberían salir de jurisdicción argentina", que las empresas usan sandboxes de IBM y que los datos anonimizados (desconectados de identificadores) dejan de estar protegidos C3P1 12:25, C3P1 16:14. Georgina cuenta que el Banco Galicia trabaja con IBM y detecta accesos raros a cuentas con grafos C3P1 14:01. En C4P1 vuelve el tema: el Ministerio Público Fiscal compró una máquina para correr modelos propios y no mandar datos de víctimas afuera C4P1 13:28.
- **El caso Cloudflare.** Laura lo usa como ejemplo de un archivo de features generado automáticamente que creció al doble y tiró abajo media internet (ChatGPT, Twitter); Georgina agrega que hay que poner un tope a la cantidad de features C3P1 18:25, C3P1 20:38.

### Correcciones y matices
- **Para verificar.** El convenio UNC con AWS y los 100 dólares por alumno C3P1 11:16; el CCAD gratuito para investigadores C3P1 6:52.
- **Matiz.** La Ley 25.326 no prohíbe en forma absoluta que los datos salgan del país: prohíbe transferirlos a países u organismos que no den un nivel de protección adecuado, con excepciones (por ejemplo, consentimiento) C3P1 12:25. **Para verificar** el detalle vigente.
- **Matiz.** Que los datos anonimizados queden fuera de la ley C3P1 16:14 es así solo si la anonimización es real, es decir si no se puede volver a identificar a la persona.
- **Para verificar.** Lo del Banco Galicia con IBM C3P1 14:01 y el Ministerio Público Fiscal C4P1 13:28 son relatos de clase.
- **Corrección, chequeada en la web.** El incidente de Cloudflare fue el 18 de noviembre de 2025 C3P1 18:25. Según el informe de Cloudflare, la causa fue un cambio de permisos en una base de datos ClickHouse que hizo que una consulta devolviera filas duplicadas: el archivo de features del sistema de gestión de bots duplicó su tamaño, superó el límite de 200 features que el software tenía preasignado y el proxy falló. No fue que "el módulo de machine learning estuviera haciendo demasiado bien". El impacto principal duró unas tres horas (de 11:20 a 14:30 UTC, es decir de 8:20 a 11:30 hora argentina) y todo quedó normal a las 17:06 UTC; el tope que propone Georgina existía y fue justamente lo que saltó C3P1 20:38.
- **Corrección.** "Es una empresa alemana, si no recuerdo mal" C3P1 21:43. Cloudflare es estadounidense, con sede en San Francisco.

### Preguntas de repaso
1. ¿Qué tenés que saber antes de mandar un trabajo a un cluster para no desperdiciarlo?
2. ¿Qué restringe la Ley 25.326 sobre transferencias internacionales de datos?
3. ¿Qué falló realmente en el incidente de Cloudflare de noviembre de 2025?

---

## 7. Embeddings y reducción de dimensión
**Dónde:** C1P1 56:28, C1P1 58:13, C2P2 31:55, C2P2 1:21:51, C2P2 1:23:34, C3P1 25:32, C3P1 27:48, C3P1 28:54, C3P1 31:08, C3P1 35:03, C3P1 36:11, C3P1 44:00, C3P1 46:50, C3P1 48:28, C3P1 51:12, C3P1 52:19, C3P1 56:11, C3P1 57:53, C3P1 1:03:27, C3P1 1:06:15, C3P1 1:08:56, C3P1 1:11:07, C3P1 1:20:29, C3P1 1:22:42, C3P1 1:26:02, C3P1 1:28:18, C3P1 1:32:49, C3P1 1:35:07, C3P1 1:36:12, C3P1 1:38:50, C3P1 1:42:13, C3P1 1:46:10, C3P1 1:50:00, C3P2 0:49, C3P2 2:50, C3P2 5:30, C3P2 8:57, C3P2 11:01, C3P2 12:57, C3P2 17:10, C3P2 17:59, C3P2 21:49, C3P2 23:04, C3P2 25:35, C3P2 29:34, C3P2 30:17, C3P2 32:19, C3P2 34:38, C3P2 35:55, C3P2 38:22, C3P2 39:49

### Conceptos clave
- **Para qué sirve una proyección.** Llevar los datos a otro espacio para visualizar, sacar ruido, reducir dimensión y representar mejor los datos para la tarea C3P1 25:32, C3P1 26:39. También para reducir el sobreajuste cuando hay ruido o muestras poco representativas, que fue el comienzo de la revolución del deep learning en lenguaje y visión C3P1 44:00, C3P1 45:07.
- **Proyectar o incrustar.** Georgina distingue proyectar (a un subespacio de menor dimensión) de incrustar, "embedding" (meter los datos en un espacio más grande) C3P1 31:08. El kernel trick de las SVM es una incrustación a más dimensiones donde una frontera lineal alcanza C3P1 28:54, C3P1 30:01, C1P1 58:13.
- **Qué se pierde.** Información (si no hay ruido, no conviene reducir) e interpretabilidad: las dimensiones nuevas no se llaman "latitud" ni "finishing" C3P1 46:50. Pero los puntos siguen siendo Messi, el Dibu o Lamine: lo que perdió sentido son los ejes C3P1 1:29:57.
- **Si no aparecen grupos.** O falta información o está diluida, repartida entre variables C3P1 36:11.
- **Selección de características sin clase.** Descartar variables casi constantes (umbral de varianza, con conocimiento de dominio) y quedarse con una de cada grupo de variables muy correlacionadas, idealmente la más barata de obtener C3P1 48:28, C3P1 51:12. La selección de características también es un embedding C3P1 35:03.
- **Agrupar características.** Viento, temperatura y humedad se reemplazan por sensación térmica: hay menos información pero estás más cerca de la causa latente C3P1 52:19. Lematizar ("corríamos" pasa a "correr") o usar la categoría gramatical son abstracciones del mismo tipo C3P1 56:11. Las redes neuronales hacen esto solas, por eso se dice que "aprenden representaciones" C3P1 55:05.
- **PCA.** Busca la dirección de mayor variación, después la siguiente ortogonal, y así; con todas las componentes es una rotación y la reconstrucción es perfecta; con pocas, minimiza el error cuadrático de reconstrucción C3P1 57:53, C3P1 1:17:47, C2P2 31:55. Sirve para visualizar, comprimir y sacar ruido C3P1 1:01:48. Si los grupos están separados en alta dimensión, probablemente se vean en las primeras componentes; si están "uno dentro del otro", no C3P1 1:20:29.
- **t-SNE.** Mantiene la distribución de probabilidad de que dos puntos sean vecinos, no las distancias. Arranca con puntos al azar en el plano y los mueve para que las dos distribuciones se parezcan según la divergencia de Kullback-Leibler; en el plano usa una distribución t de Student, de colas pesadas, para que no se amontonen C3P1 1:03:27, C3P1 1:06:15, C3P1 1:22:42. Es estocástico (con semilla fija repite) y tiende a dibujar "gusanitos" C3P1 1:06:47. Te dice qué está cerca de qué, no cuánto C3P1 1:08:56.
- **UMAP.** Arma un grafo de vecinos y lo "aplasta" en dos dimensiones buscando la estructura topológica más parecida; puede usar otras distancias C3P1 1:26:02, C3P1 1:31:39, C3P1 1:32:49.
- **Cuál usar.** Laura: plotear PCA y t-SNE y, si no se entiende, UMAP; "hacer las dos no cuesta tanto" C3P1 1:08:56, C3P1 1:28:18. La consigna incluye probar clustering en el espacio proyectado y ver si los grupos tienen más sentido C3P1 1:28:18.
- **Visualizar o trabajar.** Georgina: los métodos de visualización (t-SNE, UMAP) son para inspeccionar y ubicar testigos, no para armar los grupos; para agrupar se usan los datos originales escalados o variables elegidas por factor C3P1 1:35:07, C3P1 1:47:47. Laura: en lenguaje natural sí se agrupa sobre el espacio proyectado, porque es una representación "mejor que la real" C3P1 1:36:12, C3P1 1:46:10.
- **LSA.** La descomposición en valores singulares (SVD) de una matriz documentos por términos. El primer eje del ejemplo va de computación a medicina: explica la mayor variación aunque no sea un concepto "humano". Al reconstruir con pocas dimensiones los conteos se suavizan y los ceros pasan a valores chicos, que representan mejor "no lo vimos" que "es imposible" C3P1 1:36:44, C3P1 1:38:50, C3P1 1:42:13.
- **LDA (latent Dirichlet allocation).** Modela cada documento como una mezcla de temas y cada tema como una distribución de palabras. Le das la colección y el número de temas y te devuelve, por ejemplo, que una nota de fichajes es 30% deportes y 70% finanzas C3P1 1:50:00, C3P1 1:52:51.
- **La notebook de embeddings (C3P2).** Georgina corre PCA, t-SNE y UMAP sobre FIFA 2018 sin arqueros y con overall mayor a 70 C3P2 30:45. Los arqueros salen separados en cualquier proyección, y el resto forma una media luna con la defensa en un extremo, el ataque en el otro y el medio campo "desarmado por todos lados" C3P2 17:59. PCA la dibuja estirada, t-SNE más chata y UMAP "gordita" C3P2 34:38, C3P2 37:37.
- **Perplexity de t-SNE.** Es el parámetro principal, y Georgina se queja del nombre C3P2 9:50. Con perplexity baja se miran relaciones locales y un grupo puede aparecer partido en subgrupos; con alta se miran relaciones más globales y se unen C3P2 11:01, C3P2 12:57. Laura lo asocia con la sorpresa y la entropía C3P2 15:50; eso es correcto: la perplexity es 2 elevado a la entropía de la distribución de vecinos de cada punto, algo así como el número efectivo de vecinos. Georgina usó 30, que es el valor por defecto de scikit-learn (chequeado).
- **Costo.** Georgina corrió t-SNE con solo 1.000 jugadores "porque es pesadísimo" (necesita las distancias entre todos los pares), y lo demás con los 18.000; UMAP le sorprende por lo rápido C3P2 17:10, C3P2 14:02, C3P2 37:16. En Colab hoy corre todo con los 18.000 C3P2 43:24.
- **Cuántas componentes.** Con PCA no se reduce "de 40 a 2" para trabajar: se mira cuánta varianza explica cada componente y se decide C3P2 25:35. En su ejemplo la PC1 explica 41%, las dos primeras casi 60% y las tres primeras 67%; ella tomaría 4 C3P2 29:34, C3P2 32:19. Reducir de 40 a 10 es razonable cuando las últimas componentes son casi cero C3P2 24:48.
- **Biplot.** Muestra cuánto aporta cada variable a las primeras componentes; variables que quedan juntas y con peso parecido podrían reemplazarse por una, y se ven los factores del juego C3P2 30:17, C3P2 33:20.
- **Clustering sobre la proyección.** Georgina recuerda que t-SNE es solo para visualizar, mientras que UMAP admite agrupar sobre su salida; aun así ella no lo hace, porque pasar de 40 variables a 2 le parece demasiado si PCA dice que hacen falta 4 o 5. K-means sobre UMAP en 2D le partió la media luna en 3 C3P2 38:22, C3P2 38:47.
- **Comparar métodos entre sí.** Sin etiquetas, pedile el mismo número de grupos a varios métodos (jerárquico, K-means, K-means sobre PCA, K-means sobre UMAP), mirá cuánto coinciden y después nombrá los grupos con testigos. Los grupos que se mantienen de método en método son los confiables; el medio campo "se esparce para los costados" C3P2 39:49.
- **Etiquetas construidas.** Las etiquetas de posición las armó ella y pueden estar mal construidas; además, en FIFA un jugador tiene varias posiciones y el primer campo no siempre es la preferida C3P2 19:17, C3P2 20:59. Diseñar con las etiquetas de 2018 y aplicar a 2024, que tiene otros jugadores, es usar "información privilegiada" con el mismo espíritu C3P2 21:49.

### Correcciones y matices
- **Corrección.** Laura dice que LDA "es la tesis de Andrew Ng, el de Coursera, el del premio Turing" y que se desarrolló a la vez en lenguaje (Ng) y en biología C3P1 37:50, C3P1 41:16. El artículo de LDA es de Blei, Ng y Jordan (2003) y fue la tesis doctoral de David Blei, no de Ng. Andrew Ng no ganó el premio Turing. Lo de biología es correcto en espíritu: Pritchard, Stephens y Donnelly publicaron en 2000 un modelo equivalente para genética de poblaciones.
- **Corrección.** Georgina invita a buscar en scikit-learn "el uso de Dirichlet allocation" como prior sobre el número de grupos de K-means C3P1 39:00. En scikit-learn el proceso de Dirichlet como prior está en BayesianGaussianMixture (weight_concentration_prior_type="dirichlet_process", que es el valor por defecto, chequeado en 1.9.1), es decir para mezclas de gaussianas, no para K-means, y no tiene que ver con LatentDirichletAllocation.
- **Matiz.** "Embedding es inglés para proyección" C3P1 25:32. Embedding se traduce como incrustación; Georgina lo aclara enseguida C3P1 31:08.
- **Matiz.** "La información mutua es básicamente correlación" C3P1 51:46. También capta dependencias no lineales. Además, mutual_info_classif de scikit-learn mide cada variable contra el target (sus parámetros son X, y, ...), no variables entre sí; para selección sin clase lo que sí trae scikit-learn es VarianceThreshold C3P1 51:12.
- **Corrección, chequeada.** Laura dice que "PCA, si algo tiene, es que eficiente no es; UMAP y t-SNE son mucho más rápidos" C3P1 1:12:11. Es al revés. En el box, con los dígitos 8x8 (1.797 filas, 64 columnas): PCA a 2 dimensiones tardó 0,003 s, t-SNE 2,3 s y UMAP unos 13 s (incluida la compilación inicial).
- **Corrección.** "UMAP es la que salió antes que t-SNE" C3P1 1:11:07. t-SNE es de 2008 (van der Maaten y Hinton) y UMAP de 2018 (McInnes y otros).
- **Corrección, chequeada.** Georgina dice que con los dígitos 8x8 "me quedo con las 10 primeras y tengo prácticamente toda la variabilidad" C3P1 1:21:03. En el box, 10 componentes explican el 73,8%; hacen falta 21 para el 90% y 29 para el 95%.
- **Matiz.** "t-SNE trata de mantener la estructura de distancia original" C2P2 1:21:51. Preserva vecindarios locales, no distancias globales; Laura lo dice bien en C3P1 C3P1 1:08:56.
- **Matiz.** Laura describe la divergencia de Kullback-Leibler como "qué tan probable es que una distribución venga de otra" C3P1 1:06:47. Mide cuánta información perdés al aproximar una distribución P con otra Q; no es una probabilidad y no es simétrica (eso último sí lo dice).
- **Matiz.** En t-SNE la distribución t se usa solo en el espacio de llegada; en el original se usan gaussianas C3P1 1:22:42.
- **Chequeado.** PCA con todas las componentes preserva exactamente las distancias euclídeas (comparé las matrices de distancias en el box) C3P1 1:20:29.
- **Corrección, chequeada.** Georgina dice que la matriz de covarianza tiene que ser definida positiva, sin autovalores 0, y que si no lo es hay que pasar a SVD porque "no se podría calcular" C3P2 0:49, C3P2 23:55, C3P2 28:46. La matriz de covarianza siempre es semidefinida positiva y puede tener autovalores 0 cuando hay variables colineales; PCA anda igual (en el box, con una columna que es suma de otras dos, PCA dio una componente con varianza 0 sin ningún error). scikit-learn calcula PCA por SVD de los datos centrados, o con la opción covariance_eigh, por estabilidad numérica, no porque la descomposición espectral sea imposible.
- **Para verificar.** "El paper de t-SNE te dice que no lo uses para clustering" C3P2 38:22. Es una advertencia muy difundida (t-SNE no conserva densidades ni distancias entre grupos), pero no confirmé que esté escrita así en el artículo de 2008.
- **Matiz.** "UMAP sí te dice que podés hacer K-means sobre la proyección" C3P2 38:32. La documentación de UMAP admite usarlo antes de agrupar, pero recomienda más de 2 componentes, min_dist bajo y un método por densidad como HDBSCAN, más que K-means en 2D.

### Preguntas de repaso
1. ¿Qué diferencia hay entre proyectar e incrustar? Dá un ejemplo de cada una.
2. ¿Qué preserva PCA, qué preserva t-SNE y qué intenta preservar UMAP?
3. ¿Por qué Georgina no usaría t-SNE para armar los grupos y Laura sí agruparía sobre un embedding en lenguaje natural?
4. ¿Qué hace LSA con los ceros de una matriz documentos por términos y por qué eso es útil?

---

## 8. Embeddings neuronales y modelos de lenguaje
**Dónde:** C1P1 59:16, C1P1 1:02:01, C3P1 43:24, C3P2 41:05, C3P2 44:10, C3P2 47:31, C3P2 51:21, C3P2 53:51, C3P2 55:08, C3P2 56:23, C3P2 1:00:07, C3P2 1:01:40, C3P2 1:03:41, C3P2 1:05:14, C3P2 1:06:31, C3P2 1:07:40, C3P2 1:10:08, C3P2 1:11:34, C3P2 1:15:24, C3P2 1:16:40, C3P2 1:19:08, C3P2 1:20:34, C4P1 2:22, C4P1 3:28, C4P1 4:01, C4P1 5:39, C4P1 6:46, C4P1 10:07, C4P1 11:47, C4P1 14:37, C4P1 15:43, C4P1 16:19, C4P1 17:57, C4P1 20:15, C4P1 20:47, C4P1 23:01, C4P1 24:42, C4P1 30:53, C4P1 32:36, C4P1 34:18

### Conceptos clave
- **Embeddings neuronales.** Representar cada objeto con los valores de una capa de una red entrenada; "no se entiende nada" de lo que hay adentro, pero las representaciones son mejores para objetos, traducción, preguntas y conducción autónoma C1P1 59:16. Se obtienen con **tareas de pretexto** generadas automáticamente a partir de datos sin etiquetar, y la representación depende de la tarea C1P1 1:02:01.
- **La receta (C3P2).** Laura: entrenás una red, le sacás la capa de predicción y te quedás con la anterior; cada neurona es una dimensión del espacio nuevo, y el camino hasta esa capa es la proyección C3P2 47:31, C3P2 53:51. Un texto de 10.000 dimensiones (una por palabra) pasa a, por ejemplo, 300 C3P2 48:47. Las dimensiones no se entienden, pero un clasificador de perros y gatos o de spam acierta "muchísimo más" sobre ese espacio que sobre los píxeles o las palabras C3P2 51:21, C3P2 52:36. Es el núcleo del área llamada aprendizaje de representaciones, cuya conferencia principal es ICLR C3P2 44:10, C3P2 46:05.
- **Por qué es no supervisado.** La red se entrena de forma supervisada, pero los ejemplos etiquetados se fabrican solos con una tarea de pretexto: borrar una palabra y pedir que la adivine; de "el gato come pescado" salen cuatro ejemplos C3P2 55:08, C3P2 1:03:58. Así hay datos de sobra y la red no sobreajusta C3P2 56:23, C3P2 57:39. No es data augmentation: no se inventan combinaciones nuevas C3P2 1:04:33.
- **Tareas de pretexto en imágenes.** Sacarle el color a una imagen y pedir que la coloree, o desordenarla como un rompecabezas y pedir que la ordene C3P2 1:01:40, C3P2 1:03:13. Cada tarea enseña otra cosa: colores y contrastes, siluetas y formas, relaciones entre palabras y contexto C3P2 1:04:44, C3P2 1:05:14.
- **El embedding se diseña.** PCA es "neutro", basado en la variabilidad; un embedding neuronal depende de la tarea de pretexto: centrada en sustantivos, en inglés o en traducción, representa mejor eso C3P2 1:06:31, C3P2 1:07:40. Para FIFA podrías entrenar una red que prediga la posición y usar la capa anterior, pero "nadie espera que lo hagan" C3P2 1:07:40, C3P2 1:09:00.
- **Embeddings de palabras.** En 2013 apareció la primera librería para entrenarlos (word2vec) y poco después una de Meta más eficiente (fastText); se usan 300 dimensiones "porque funcionaba" C3P2 1:10:08, C3P2 1:10:48. Laura muestra un mapa t-SNE de palabras de la Biblia y las dimensiones de "reina", "rey", "mujer", "hombre", "chica", "chico" y "agua" del blog de Jay Alammar: algunas parecen captar concreto o abstracto, género o edad, aunque no se puede asegurar C3P2 1:11:07, C3P2 1:11:34, C3P2 1:15:24.
- **Hipótesis distribucional.** Palabras que aparecen en contextos parecidos quedan cerca. Con tres oraciones sobre el durian deducís que es una fruta tropical sin haberlo visto nunca; pero relacionar palabras no es entender C3P2 1:16:40, C3P2 1:17:57.
- **Puente a los LLM.** El núcleo de ChatGPT o Claude es esto, entrenado con tareas de pretexto sobre texto e imágenes; por eso alucinan: modelan combinaciones probables de palabras sin un chequeo con la realidad, salvo que se agreguen módulos que verifiquen C3P2 1:19:08, C3P2 1:21:47. Encima van la orientación a instrucciones, las barreras de seguridad y módulos de cuentas o de documentos (RAG) C3P2 1:19:50, C3P2 1:20:34. La clase siguiente retoma desde acá C4P1 2:22.
- **Por qué los modelos de lenguaje son no supervisados.** Son redes enormes (con Transformers adentro) que aprenden por retropropagación, como cualquier red supervisada, pero sus ejemplos etiquetados salen de tareas de pretexto que convierten texto sin etiquetar en pares entrada y salida. Por eso pueden usar cantidades enormes de datos sin sobreajustar C4P1 4:01. La salida de ese núcleo es un embedding C4P1 17:57.
- **El Transformer.** Su gran aporte fue paralelizar el aprendizaje de secuencias, que antes era secuencial: meses en vez de "un tiempo infinito" C4P1 5:39. Se usa también para proteínas y ADN C4P1 3:28. Lectura recomendada: "The Illustrated Transformer" de Jay Alammar C4P1 2:55.
- **Por qué GPUs.** El chip está diseñado para operaciones con matrices, que es lo que hacen las redes C4P1 6:46.
- **Modelos propios y pesos abiertos.** Mandar datos a un servicio es dárselos a esa empresa; por eso hay quienes entrenan o corren modelos propios C4P1 10:07. Los modelos "abiertos" son en rigor de **pesos abiertos**: tenés los parámetros, no el código ni los datos de entrenamiento C4P1 11:47. Corren en máquinas con GPU grande o en centros de cálculo como el CCAD C4P1 13:28.
- **Capas encima del núcleo.** Orientación a instrucciones (supervisada, con personas mal pagas que escribieron y rankearon respuestas, de Nigeria y Kenia para el inglés y de Latinoamérica para el castellano); módulos aritméticos, lógicos y de búsqueda (métodos híbridos o neurosimbólicos), porque los primeros ChatGPT decían siempre 7 cuando les pedías un número al azar; y barreras de seguridad C4P1 16:19, C4P1 20:47, C4P1 23:01. Ese aprendizaje supervisado funciona porque parte de un núcleo que ya aprendió la estructura del lenguaje: concordancia sujeto y verbo, correferencia C4P1 17:57, C4P1 20:15.
- **Barreras de seguridad y jailbreaks.** Son más rígidas y por eso más fáciles de romper: exfiltración de datos, lenguaje tóxico, juicios por inducción al suicidio, el subreddit DAN ("do anything now") y el truco de la abuelita y el cóctel molotov que cuenta Tomás Balmaceda (Capitán Intriga) C4P1 24:42, C4P1 30:53.
- **Historia reciente.** Meta empujó los pesos abiertos (Yann LeCun) con Llama hasta la "revolución de DeepSeek" C4P1 32:36. Cuando se filtró un Llama, la comunidad de software libre hizo en una semana que corriera en computadoras comunes bajando los bits de los pesos: cuantización C4P1 34:18.

### Correcciones y matices
- **Corrección.** "Cuando salieron en 2018, el primer modelo de lenguaje con todas las letras: le escribías y seguía escribiendo. BERT se llamaba" C4P1 14:37. BERT (2018) es un codificador entrenado a adivinar palabras enmascaradas y no genera continuaciones; el que seguía escribiendo era GPT (2018) y sobre todo GPT-2 (2019). Además, los modelos de lenguaje existen desde mucho antes (los de n-gramas).
- **Corrección probable.** "A los 15 días de salir ChatGPT, Bloomberg comentó que tenía su propio modelo" C4P1 10:07. BloombergGPT se presentó a fines de marzo de 2023, unos cuatro meses después de ChatGPT (30/11/2022). **Para verificar** si hubo un anuncio anterior.
- **Chequeado en la web.** "Andrej Karpathy ahora está en Anthropic desde hace unos meses" C4P1 15:43: es correcto, se sumó el 19 de mayo de 2026 al equipo de preentrenamiento. Lo de que "estuvo en el equipo que armó ChatGPT" es impreciso: fue cofundador de OpenAI, dirigió IA en Tesla de 2017 a 2022 y volvió a OpenAI en 2023 y 2024.
- **Matiz.** Sobre las GPUs, Laura dice que "no es tanto por paralelizar" C4P1 6:46. Las operaciones con matrices son rápidas en una GPU justamente porque tiene miles de núcleos que trabajan en paralelo y mucho ancho de banda de memoria; la respuesta de Juan no estaba mal.
- **Corrección, chequeada en la web.** "La valoración en bolsa de Nvidia bajó 20%, la mayor caída de la bolsa de la historia en términos absolutos" C4P1 32:36. El 27 de enero de 2025 Nvidia cayó cerca del 17% y perdió unos 590 mil millones de dólares: la mayor pérdida de valor de una sola empresa en un día en la bolsa de EE.UU., no "de la bolsa".
- **Matiz.** La cuantización no se inventó en esa semana C4P1 34:18: había métodos para modelos grandes desde 2022 (LLM.int8, GPTQ). Lo que apareció en días tras la filtración de LLaMA en marzo de 2023 fue llama.cpp, que corría el modelo en 4 bits en una CPU común. LLaMA, además, se distribuyó en 16 bits, no en 32.
- **Chequeado a medias.** La "novela" de los modelos de Anthropic que "se ponen y se sacan" C4P1 24:42: en abril de 2026 Anthropic no liberó Claude Mythos Preview por su capacidad para encontrar y explotar vulnerabilidades y lo dio solo a defensores (Project Glasswing). La transcripción dice "Fable"; una fuente web menciona un "Claude Fable 5" lanzado en junio de 2026 con salvaguardas, **para verificar**.
- **Para verificar.** Las cifras de parámetros que se mencionan al pasar ("8 billones", "Kimi 1,2 teras", "tres veces más grande que Kimi K3") son **dudosas** en la transcripción C4P1 12:21.
- **Corrección.** "Desde los años 50 sabíamos que una red neuronal podía modelar prácticamente todos los problemas; el problema era entrenarla" C3P2 1:00:07. El perceptrón de fines de los 50 no podía ni siquiera con el XOR (Minsky y Papert, 1969). Que una red con una capa oculta aproxima cualquier función continua es el teorema de aproximación universal, de 1989 (Cybenko) y 1991 (Hornik).
- **Chequeado en la web.** "Este año ICLR fue en Río" C3P2 46:05: correcto, ICLR 2026 fue en Río de Janeiro del 23 al 27 de abril (la transcripción automática dice "2016").
- **Matiz.** "Meta tiene los mensajes de Instagram y Facebook, que nunca tuvo encriptación punto a punto" C3P2 1:03:41. Messenger tiene cifrado de extremo a extremo por defecto desde diciembre de 2023; el estado de los mensajes de Instagram es **para verificar**.
- **Matiz.** La capa de instrucciones "entrenada con métodos semisupervisados de reinforcement learning" C3P2 1:19:50. Lo habitual es un ajuste fino supervisado seguido de aprendizaje por refuerzo con retroalimentación humana (RLHF); no se lo suele llamar semisupervisado.
- **Matiz.** Georgina dice que los embeddings de redes "no se basan en distancias sino en producto punto" C3P2 41:05. El producto punto y la distancia euclídea están directamente relacionados (para vectores de norma 1, uno se obtiene del otro); lo cierto es que las redes no optimizan una distancia entre ejemplos como lo hacen t-SNE o UMAP.

### Preguntas de repaso
1. ¿Qué es una tarea de pretexto y por qué permite decir que un modelo de lenguaje es no supervisado?
2. ¿Qué capas hay encima del núcleo preentrenado y cuál de ellas es supervisada?
3. ¿Qué diferencia hay entre un modelo de código abierto y uno de pesos abiertos?
4. ¿Qué es cuantizar un modelo y para qué sirve?

---

## 9. Aprendizaje semisupervisado y otras formas de supervisión débil
**Dónde:** C1P1 54:46, C4P1 0:03, C4P1 36:35, C4P1 37:40, C4P1 39:18, C4P1 41:32, C4P1 42:06, C4P1 43:50, C4P1 45:25, C4P1 46:35, C4P1 52:45, C4P1 55:44, C4P1 59:07, C4P1 1:01:56, C4P1 1:07:30, C4P1 1:08:37, C4P1 1:10:51, C4P1 1:14:04, C4P1 1:16:23, C4P1 1:20:14, C4P1 1:23:33, C4P1 1:28:02, C4P1 1:30:17, C4P1 1:34:12, C4P1 1:40:22, C4P1 1:42:02, C4P1 1:44:49, C4P1 1:46:33, C4P1 1:47:41, C4P1 1:51:32, C4P1 1:52:04, C4P1 1:54:12

### Conceptos clave
- **El contexto.** Pocos datos etiquetados, caros; muchos sin etiquetar, casi gratis (texto, imágenes). La excepción es la neuroimagen, donde obtener el dato cuesta más que etiquetarlo C4P1 37:40. El objetivo es un modelo más complejo que no sobreajuste, usando la información "poblacional" de los no etiquetados C4P1 45:25.
- **El continuo de supervisión.** Aprendizaje activo: es supervisado puro, pero un modelo elige qué ejemplos conviene que etiquete el "oráculo" (una persona o un servicio) C4P1 39:18. Semisupervisado: asunciones estructurales para propagar etiquetas C4P1 41:32. Supervisión débil: etiquetas poco confiables (captchas, heurísticas como "si dice príncipe nigeriano es spam") con triangulación entre anotadores C4P1 42:06. Transfer learning: lo aprendido en un dominio se usa en otro; los embeddings neuronales son exactamente eso C4P1 43:50.
- **La idea, con un dibujo.** Con una cruz y un círculo etiquetados, la frontera queda a mitad de camino. Si mirás dónde está la población sin etiquetar y suponés gaussianas, la corrés a la zona poco poblada sin violar la separación de los dos etiquetados C4P1 46:35. "Ante la duda, una gaussiana" C4P1 50:01.
- **Disjunto o conjunto.** Aprender con los etiquetados y aplicar a los otros, o ajustar los parámetros con ambos a la vez, que es más adecuado y más complejo C4P1 52:45.
- **Autoaprendizaje (self-training).** Antes se llamaba bootstrapping. Entrenás con lo poco que tenés, etiquetás los no etiquetados, incorporás los de mayor confianza (por ejemplo, 95%, o los n mejores) y repetís C4P1 55:44. Necesita un clasificador con un puntaje de confianza; se puede combinar con aprendizaje activo para que una persona revise los casos dudosos C4P1 59:07, C4P1 1:01:21. Es fácil, sirve con cualquier modelo, pero amplifica errores, sobre todo los iniciales, y no llega a regiones sin conexión; los outliers hacen "puentes" y la clase mayoritaria atrae a todos (deriva) C4P1 1:07:30, C4P1 1:08:37.
- **Yarowsky (1995).** Desambiguación de "plant" (planta biológica o industrial) con una lista de decisión que se va ampliando, más dos heurísticas: un sentido por colocación y un sentido por discurso, que corrige errores y completa huecos C4P1 1:01:56.
- **Coaprendizaje (co-training).** Lo mismo con dos modelos sobre dos vistas complementarias (el texto y las imágenes de una página); muchos problemas no se dividen bien en dos vistas C4P1 1:10:51, C4P1 1:12:59.
- **Modelos generativos.** Una gaussiana por clase ajustada con EM usando también los no etiquetados C4P1 1:14:04. Georgina agrega la versión práctica: inicializar K-means o GMM con los centroides, medias y varianzas de los pocos etiquetados; converge más rápido y evita mínimos locales absurdos, y el centroide igual se mueve hacia donde están los datos C4P1 1:16:23, C4P1 1:18:34, C4P1 1:20:14. El peligro: dos clases no son necesariamente dos gaussianas (el ejemplo tiene cuatro) C4P1 1:23:33.
- **Las categóricas ocultan estructura.** En clustering se tiende a descartar las categóricas, pero pueden ser la causa latente (consumo eléctrico comercial o domiciliario); conviene mirar el agrupamiento dentro de cada categoría C4P1 1:26:15, C4P1 1:28:02.
- **Basados en grafos.** Las etiquetas se propagan por los arcos de un grafo con pesos ("los amigos de mis amigos"), por ejemplo documentos que comparten palabras C4P1 1:30:17, C4P1 1:34:12. Lo difícil es modelar el problema como grafo C4P1 1:35:55.
- **Otros.** SVM semisupervisadas (costosas, búsqueda no convexa), ladder networks (una red supervisada más un autoencoder), aprendizaje positivo y no etiquetado (PU, típico de búsquedas y recomendaciones donde solo sabés lo que se clickeó) y aprendizaje por refuerzo (decisiones encadenadas con recompensa al final, como las damas) C4P1 1:40:22, C4P1 1:42:02, C4P1 1:44:49, C4P1 1:47:41.
- **Evaluar es una pesadilla.** Hay pocos etiquetados y si separás algunos para test la evaluación queda ridícula. Hay que dedicar parte de lo que ahorrás en etiquetado a monitorear, por ejemplo graficando cómo crece cada clase alrededor de las semillas C4P1 1:52:04.
- **La conclusión de Laura.** Es ingeniería: "una solución más que una tesis doctoral". Lo valioso es poner en juego lo que sabés de los datos y optimizar el tiempo del experto C4P1 1:54:12.

### Correcciones y matices
- **Corrección, chequeada.** Laura y Georgina dicen que estos algoritmos "no están para nada" en scikit-learn y hay que programarlos C4P1 1:20:14, C4P1 1:51:32. scikit-learn tiene el módulo semi_supervised con SelfTrainingClassifier, LabelPropagation y LabelSpreading (chequeado en 1.9.1 y 1.6.1), y KMeans y GaussianMixture aceptan una inicialización explícita (init como array y means_init). Lo que no trae es EM semisupervisado con restricciones ni clustering con restricciones.
- **Corrección.** "XGBoost es un método de ensamble que no está basado en boosting" C4P1 1:11:54. XGBoost es eXtreme Gradient Boosting: sí es boosting.
- **Matiz.** "En coaprendizaje la asunción es que los ejemplos cercanos van a tener la misma etiqueta" C4P1 1:14:04. Co-training supone dos vistas, cada una suficiente para clasificar y condicionalmente independientes dada la clase; la de cercanía es la asunción de cluster o de suavidad.
- **Corrección.** Laura dice que las ladder networks son "muy viejitas" y que las vio en el libro de 2006 de Bing Liu sobre web mining C4P1 1:42:02. Las ladder networks son de 2015 (Rasmus, Valpola y otros). El libro de Bing Liu, Web Data Mining (2007), trata sobre todo el aprendizaje PU.
- **Matiz.** "No se puede hacer aprendizaje automático si no tenés ejemplos negativos, es un resultado teórico" C4P1 1:44:49. El aprendizaje PU aprende con positivos y no etiquetados bajo supuestos como que los positivos etiquetados se eligieron al azar (Elkan y Noto, 2008). Hace falta un supuesto, no necesariamente negativos.
- **Matiz.** El ejemplo de los oxímetros que funcionan peor en piel oscura C4P1 44:54 es un sesgo real, pero de calibración del sensor, no un caso típico de transfer learning.
- **Matiz.** Georgina dice que con distribuciones esféricas "hay cuatro parámetros para la matriz de covarianza" C4P1 1:17:28. Una covarianza esférica tiene un solo parámetro por componente; una completa de 2x2 tiene tres libres. **Dudoso** qué quiso decir.
- **Dudoso.** "La búsqueda en el espacio de todos los grafos es usualmente NP completa" C4P1 1:37:00 es una formulación vaga; depende del problema concreto.

### Preguntas de repaso
1. ¿En qué se diferencian aprendizaje activo, semisupervisado y supervisión débil?
2. ¿Cuáles son los dos problemas del autoaprendizaje y cómo los mitigó Yarowsky?
3. ¿Cómo usarías 10 jugadores etiquetados para ayudar a K-means?
4. ¿Por qué evaluar un sistema semisupervisado es tan difícil?

---

## 10. Reglas de asociación
**Dónde:** C1P1 53:38, C4P2 0:02, C4P2 1:13, C4P2 2:53, C4P2 4:07, C4P2 5:20, C4P2 5:54, C4P2 6:29, C4P2 7:03, C4P2 8:11, C4P2 10:55, C4P2 12:33, C4P2 14:45, C4P2 16:20, C4P2 19:06, C4P2 21:19, C4P2 23:32, C4P2 24:45, C4P2 25:18, C4P2 27:02, C4P2 27:35, C4P2 35:58, C4P2 37:07, C4P2 39:19, C4P2 40:22, C4P2 42:04, C4P2 43:46, C4P2 45:28, C4P2 47:44

### Conceptos clave
- **Qué son.** Probabilidad condicional convertida en regla: "si compra fernet, la probabilidad de que compre Coca es tanto" C4P2 0:02. El formato es cercano a las reglas de negocio y le sirve a gente que no maneja estadística C4P2 1:13. En la segunda cohorte, Andrés Vázquez aplicó la notebook a los tickets de unos kioscos durante la clase y le salió fernet con Coca C4P2 2:53.
- **Transacciones.** Una transacción es un conjunto de ítems sin orden (un ticket); la base de datos es el conjunto de tickets C4P2 6:29, C4P2 7:03. Todo tiene que ser categórico: las variables continuas se discretizan (rangos de edad) C4P2 5:54.
- **Modelar es lo difícil.** Hay mil tipos de pan: hay que decidir qué es un ítem (pan embolsado o no) con conocimiento de dominio, no con métodos empíricos de reducción de dimensión C4P2 8:11. Un documento puede ser una transacción y sus palabras los ítems; aparece, por ejemplo, que "sordera" se asocia con "superar obstáculos" más que con "profesionalidad" C4P2 10:55, C4P2 12:33. En historias clínicas, la transacción puede ser una consulta o un período (ibuprofeno, gastritis, protector gástrico) C4P2 16:20. También fallas de discos, navegación web o cursos en línea, convirtiendo el tiempo en ventanas C4P2 21:19.
- **Las reglas.** X entonces Y, con X e Y conjuntos de ítems disjuntos C4P2 23:32. **Soporte**: qué tan seguido aparece el conjunto completo; sirve para descartar "caviar implica Ferrero Rocher" que pasó una sola vez C4P2 25:18. **Confianza**: la probabilidad condicional; fernet a Coca 83%, Coca a fernet 35%, no es simétrica C4P2 27:02. Hay más métricas (lift, convicción) y se pueden armar propias C4P2 24:45, C4P2 35:58.
- **El algoritmo Apriori.** Primero busca los conjuntos frecuentes y después genera reglas con su confianza C4P2 39:19. La poda: si un ítem no llega al soporte mínimo, ningún conjunto que lo contenga llega C4P2 40:22. Ejemplo: {2, 3, 4} con soporte 50% da {2, 3} a 4 con 100% y {3, 4} a 2 con 67% C4P2 42:04.
- **En la práctica.** Salen miles de reglas: conviene un soporte mínimo bajo y después filtrar y ordenar según la pregunta de negocio C4P2 5:20, C4P2 43:46. Con películas, un soporte alto devuelve lo obvio (El Padrino 1 con El Padrino 2) y uno bajo devuelve cosas raras (El Padrino con un programa de cocina) C4P2 45:28.
- **Takeaway.** Junto con el clustering, es el no supervisado "puro", y es más fácil de mostrar a un experto que un clustering C4P2 47:44.

### Correcciones y matices
- **Corrección.** Apriori aparece como "del 93" y después "del 83" C4P2 5:54, C4P2 39:19. El algoritmo Apriori es de Agrawal y Srikant (1994). En 1993 Agrawal, Imielinski y Swami habían planteado la minería de reglas de asociación con otro algoritmo.
- **Corrección, chequeada.** Laura define el lift como "la probabilidad de que esa regla haya sido por casualidad" C4P2 35:58. El lift es P(X e Y) / (P(X) P(Y)), igual a confianza / soporte(Y): un cociente contra la independencia (1 es independencia), no una probabilidad. Lo de "básicamente información mutua" va bien encaminado: su logaritmo es la información mutua puntual (PMI). Con mlxtend en el box, fernet a Coca con confianza 1 y soporte(Coca) 0,667 da lift 1,5.
- **Corrección, chequeada.** "La convicción es la inversa del soporte por la confianza" C4P2 35:58. La convicción es (1 - soporte(Y)) / (1 - confianza(X a Y)); vale infinito cuando la confianza es 1 (así sale en mlxtend 0.25).
- **Corrección.** "Esa es la única optimización que se puede hacer" C4P2 41:31. Hay algoritmos que evitan generar candidatos, como FP-Growth (Han y otros, 2000) o Eclat. En mlxtend, apriori y fpgrowth devolvieron los mismos conjuntos frecuentes en mi prueba.
- **Matiz.** "Soporte es la cantidad de veces" C4P2 25:18. Se suele expresar como proporción de transacciones; mlxtend usa proporción.
- **Para verificar.** El modelo de negocio de Todo Moda como "100% machine learning" y con la ganancia de una ferretería C4P2 31:29 es una opinión de Georgina.

### Preguntas de repaso
1. ¿Qué diferencia hay entre soporte y confianza? ¿Por qué necesitás los dos?
2. ¿Qué mide el lift y qué valor indica independencia?
3. ¿Cómo modelarías historias clínicas como transacciones si te interesan efectos de largo plazo?

---

## 11. Análisis de redes sociales y grafos
**Dónde:** C1P1 42:26, C1P1 43:34, C4P2 48:18, C4P2 49:58, C4P2 51:05, C4P2 53:52, C4P2 55:00, C4P2 57:18, C4P2 58:24, C4P2 59:30, C4P2 1:00:39, C4P2 1:01:48, C4P2 1:04:03, C4P2 1:05:07, C4P2 1:06:47, C4P2 1:07:20, C4P2 1:08:29, C4P2 1:09:41

### Conceptos clave
- **El caso Enron.** Tras la quiebra, los correos de la empresa quedaron disponibles. Entre los empleados de base había evidencia del agujero financiero y entre los directivos no. Según Laura, especialistas en grafos mostraron que dos grupos que lo sabían a la vez solo se comunicaban a través de sus jefes, así que los jefes tenían que saberlo C4P2 49:58, C4P2 51:05. El dataset Enron se sigue usando mucho C4P2 53:17.
- **Mundo pequeño.** Las redes sociales tienen pocos grados de separación, hubs y cliques C4P2 53:52.
- **Datos.** Las grandes redes no publican sus datos; Bluesky tiene un "firehose" abierto y Reddit cerró el acceso por el uso que hacían empresas de IA C4P2 55:00. Otros grafos posibles: interconsultas médicas, transporte, llamadas C4P2 56:10.
- **Contenido o estructura.** Temas y sentimiento son contenido, no grafo (para sentimiento menciona la librería pysentimiento y para temas, LDA) C4P2 57:18. Lo estructural es detectar grupos, flujos de información e influencia C4P2 58:24.
- **Medidas sobre nodos.** Alcance (vistas, likes, republicaciones, seguidores, engagement), buzz (amplificación indirecta, difícil de medir), influencia (el alcance como probabilidad) y tipo de reacción (positiva, negativa, rage bait) C4P2 59:30, C4P2 1:00:39, C4P2 1:01:48, C4P2 1:02:54.
- **Medidas sobre el grafo.** Centralidad (sin dirección): de grado, de cercanía (distancia promedio a todos) y de intermediación o betweenness, que encuentra los "estrechos de Gibraltar" de la red, como en Enron C4P2 1:05:07, C4P2 1:06:47, C4P2 1:07:20. Prestigio (con dirección): no es lo mismo seguir a muchos que ser seguido por muchos; hubs y authorities C4P2 1:08:29. Comunidades: algoritmos de partición que cortan los arcos más débiles, como Louvain ("Lobaina") C4P2 1:09:41.

### Correcciones y matices
- **Corrección.** "Enron era una petrolera, sector secundario" C4P2 49:58. Era una empresa de energía y comercialización de gas y electricidad con sede en Houston; quebró en diciembre de 2001. Arthur Andersen, su auditora, era una de las "Big Five" y dejó de operar tras ser condenada en 2002 (la condena se anuló en 2005, ya sin empresa).
- **Corrección.** "Hubo un juicio de acreedores y el juez pidió los correos" C4P2 51:05. El corpus lo publicó la FERC durante su investigación.
- **Para verificar.** Que el análisis de grafos de los correos haya servido para "condenar a un montón de gente" C4P2 53:17. No encontré registro de que fuera prueba en los juicios; los análisis de redes sobre el corpus son posteriores y académicos.
- **Corrección.** Laura dice que la distinción entre hubs y authorities "es la base del algoritmo PageRank" C4P2 1:09:03. Hubs y authorities es el algoritmo HITS de Kleinberg (1999); PageRank (Brin y Page, 1998) da un solo puntaje de importancia por página. En networkx están las dos: nx.hits y nx.pagerank.
- **Matiz.** Gephi ("Geppi") es un programa de escritorio para visualizar grafos, no una librería C4P2 1:11:20; en Python, lo habitual es networkx.
- **Dudoso.** "La misma empresa no puede tener infraestructura de comunicaciones e internet, hay una legislación bastante internacional" C4P2 56:45.
- **Para verificar.** Que en Chile los datos de interconsultas médicas sean públicos C4P2 56:10 y que pysentimiento sea de un estudiante de Laura C4P2 57:52.

### Preguntas de repaso
1. ¿Qué mide la betweenness y por qué fue clave en el relato de Enron?
2. ¿Qué diferencia hay entre centralidad y prestigio?
3. ¿Qué es un hub y qué una authority?

---

## 12. Sistemas de recomendación
**Dónde:** C4P2 1:11:54, C4P2 1:12:28, C4P2 1:14:08, C4P2 1:16:23, C4P2 1:17:30, C4P2 1:19:43, C4P2 1:20:47, C4P2 1:22:28, C4P2 1:24:08, C4P2 1:24:44, C4P2 1:25:16, C4P2 1:26:59, C4P2 1:29:44

### Conceptos clave
- **Por qué es no supervisado.** Nadie etiquetó nada: hay datos de comportamiento (si viste la serie entera, si la dejaste prendida tres horas porque te dormiste) C4P2 1:12:28. Lo que se quiere predecir es si a Alice le va a gustar el ítem 5; al usar lo que sabemos de Alice como características y lo que dijeron otros del ítem 5 como objetivo, el problema se vuelve supervisado C4P2 1:14:08.
- **Filtrado colaborativo con KNN.** Buscás los usuarios más parecidos a Alice en los ítems que ambos calificaron y hacés un voto pesado de lo que dijeron sobre el ítem 5 C4P2 1:16:23, C4P2 1:17:30. KNN no entrena pero predice caro, así que se calcula offline C4P2 1:16:57.
- **Netflix.** Infiere los gustos (si "bingeaste" una serie, normalizado por tu hábito) y mezcla filtrado colaborativo con perfil y reglas de negocio para promocionar contenidos C4P2 1:19:43, C4P2 1:21:21. El Premio Netflix daba un millón de dólares a quien mejorara su algoritmo C4P2 1:20:47.
- **Cola larga y arranque en frío.** Los ítems poco populares y los usuarios o ítems nuevos tienen pocos datos. Se atacan con características del producto (género, actores, país), con embeddings, que en este campo se llaman factorización de matrices, y con clustering de usuarios o de ítems C4P2 1:22:28, C4P2 1:24:08, C4P2 1:24:44.
- **Más allá de películas.** Salud preventiva (pacientes parecidos a vos tuvieron tal problema: venite a hacer un chequeo), medicina personalizada, trayectorias de aprendizaje (Duolingo) y personalización de chatbots C4P2 1:25:16, C4P2 1:26:59. Francisco advierte en el chat que con todo tu historial el chatbot puede sugerir bien y también manipular bien C4P2 1:29:44.

### Correcciones y matices
- **Para verificar.** El Premio Netflix C4P2 1:20:47 se lanzó en 2006 y se entregó en 2009 por una mejora de 10% en el error (RMSE) respecto del algoritmo de Netflix.
- **Matiz.** La factorización de matrices "es PCA básicamente" C4P2 1:24:08: está emparentada con la SVD, pero se ajusta solo con las calificaciones observadas, porque la matriz tiene casi todo vacío.
- **Matiz.** "Todo eso está basado exactamente en los mismos algoritmos de filtrado colaborativo" C4P2 1:26:59 es una generalización amplia; en salud se combinan con reglas clínicas, como ella misma dice.

### Preguntas de repaso
1. ¿Cómo se convierte una recomendación en un problema supervisado?
2. ¿Qué son la cola larga y el arranque en frío y cómo se atacan?

---

## 13. El trabajo especial
**Dónde:** C1P2 1:10:05, C1P2 1:17:34, C2P2 38:16, C2P2 1:14:05, C2P2 1:16:14, C2P2 1:17:23, C2P2 1:20:14, C2P2 1:25:13, C2P2 1:29:13, C2P2 1:34:40, C2P2 1:41:16, C2P2 1:41:51, C3P1 1:28:18, C4P2 1:30:56

### Conceptos clave
- **Una sola tarea.** Es el único entregable de la materia, se evalúa con una rúbrica como aprobado o desaprobado, y aprueba con 70% o más C2P2 1:16:14, C2P2 1:17:23, C2P2 1:41:16.
- **Los datos.** FIFA 24 de Kaggle (el archivo trae también las versiones 21 a 23); hay que llamarlo df y revisar los nombres de columnas, que pueden venir con mayúsculas o con el prefijo del factor C1P2 1:10:05, C2P2 38:16.
- **La consigna, punto por punto** (según cómo la explica Georgina) C2P2 1:17:23:
  1. Análisis exploratorio (bastante de la notebook de exploración).
  2. Evaluación visual intuitiva con pares de variables (scatter de todos contra todos).
  3. Normalización o escalado.
  4. Clustering: se espera K-means y el jerárquico que mejor ande, con un mapa de métricas y explicando cómo eligieron los hiperparámetros (K, el linkage).
  5. Análisis cuantitativo e interpretación.
  6. Las proyecciones de la segunda semana: PCA, t-SNE y UMAP para visualizar, y probar clustering en el espacio proyectado C3P1 1:28:18, C4P2 1:30:56.
  7. El punto "a pedido de Carolina": pasarle el mismo prompt a dos o más LLM (Claude, ChatGPT, Gemini; Georgina usa Grok) para que interpreten cada grupo y comparar coincidencias, diferencias y alucinaciones con la interpretación del grupo C2P2 1:25:13.
- **Consejos.** Posiciones solo para evaluar, nunca para agrupar C1P2 1:17:34. Escalar siempre C2P2 1:11:15, C4P2 1:33:43. Probar clustering con 6 o 7 componentes y sumarlo a la tabla; armar un tablero de 3 por 3 gráficos para comunicar; tener la tabla a mano para cuando pregunten "¿y no hiciste otra cosa?" C2P2 1:14:05. Hacerlo ustedes primero y después comparar con el LLM; usar el material de clase, porque el asistente va a hacer otra cosa C4P2 1:30:56, C4P2 1:31:30.
- **Uso de LLM.** Laura: si los usan para el código, se quedan con el código; si los usan para el análisis, dependen del servicio C2P2 1:34:40.

### Correcciones y matices
- **Para verificar.** La numeración exacta de los puntos (el de los LLM se nombra como "punto 7") y qué proyecciones son obligatorias: la lista de arriba es una reconstrucción a partir de lo que se dice en clase; la consigna escrita está en el aula virtual C2P2 1:25:13.
- **Para verificar.** El dataset exacto de Kaggle (hay varios "FIFA 24" publicados) C1P2 1:10:05.
- **Dudoso.** En el cierre, Georgina habla de "dar una charla" para defender las decisiones C4P2 1:32:05; no queda claro si es parte de esta materia o un comentario general.

### Preguntas de repaso
1. ¿Qué tiene que tener la tabla de métricas del trabajo?
2. ¿Qué tenés que comparar en el punto de los LLM?

---

## Lo que falta o quedó en duda
- **C3P2 sin subtítulos de la grabación.** la grabación devolvió "demasiadas solicitudes" (HTTP 429) en nueve intentos espaciados y después pidió confirmar que no era un bot. El audio sí bajó, y la transcripción de esa parte la hice con faster-whisper (modelo small, en el box). Es menos prolija con los nombres propios y los tiempos se marcan por frase, no cada 30 segundos. Revisé la transcripción completa, pero los nombres propios de C3P2 (por ejemplo, el año de ICLR, que sale como 2016) los corregí a mano y alguno puede seguir mal.
- **Notebooks.** No tengo acceso al aula virtual ni a las notebooks de clase; todo lo que digo de ellas sale de lo que se ve y se dice en las grabaciones.
- **Consigna escrita del trabajo especial.** Está en el aula virtual; la lista de la sección 13 es una reconstrucción.
- **Apellidos.** Solo se dicen nombres de pila. Laura Alonso Alemany y Georgina Flesia salen del sitio de la diplomatura (que en la página propia de la materia lista a "Valeria Rulloni y Laura Alonso Alemany", probablemente de otra edición, **para verificar**). Damián (cálculo distribuido) y Luciana (Ética) quedan sin apellido.

## Glosario y nombres deformados en la transcripción

| Lo que dice la transcripción | Qué es |
|---|---|
| clot, cloud, Cloud, clotebook | Claude, el asistente de Anthropic (y Claude Code) |
| camas, camedias, que means | K-means, K medias |
| Clara, Clarence | CLARA y CLARANS (variantes de PAM) |
| minift | mean shift |
| den clue | DENCLUE |
| Word | Ward (linkage de mínima varianza) |
| tight | tied (covarianza compartida en GaussianMixture) |
| bas and information, akik | BIC (Bayesian information criterion) y AIC (Akaike) |
| Elena Nova | MANOVA (**dudoso**) |
| Lein | — |
| tanimoto | coeficiente de Tanimoto |
| Kle | Kaggle |
| TCN, Disney, Tesne, TSNE | t-SNE |
| Spectral Manifold | spectral embedding (embedding espectral) |
| un map, umap, lumap | UMAP |
| Coolback Libler, Culba Claver, Colback Laber | divergencia de Kullback-Leibler |
| tendricticlet, late and let allocation, Latendal location, la tendirictation | LDA, latent Dirichlet allocation |
| lat semantic análisis | LSA, latent semantic analysis |
| aigen vectors, Men vectors | eigenvectors, autovectores |
| SECAT, Secat, Seat | CCAD, Centro de Computación de Alto Desempeño de la UNC |
| Vietma | Luis Biedma (coordinador de mentorías) |
| Jorina, Yosina, Yorgina, Jorgena | Georgina (Flesia) |
| Andre un G | Andrew Ng |
| J Alamar | Jay Alammar ("The Illustrated Transformer") |
| Andrey Carpati | Andrej Karpathy |
| Jan Leun | Yann LeCun |
| Dipsic, Dipsik, Deep Six | DeepSeek |
| Quen | Qwen |
| Tomás Balma | Tomás Balmaceda (Capitán Intriga) |
| Fable | modelo de Anthropic; probablemente Claude Fable 5 o la familia Mythos (**para verificar**) |
| Jarovski | David Yarowsky |
| one sense collocation, OneSense per discorse | one sense per collocation, one sense per discourse |
| weekion, Wix Provision, weekvision | weak supervision |
| lader network | ladder networks |
| Bingu | Bing Liu |
| Exchi Boost | XGBoost |
| course of dimensionality | curse of dimensionality (maldición de la dimensionalidad) |
| Ferné | fernet |
| pisentimiento | pysentimiento (librería de análisis de sentimiento) |
| Lobaina | algoritmo de Louvain |
| Geppi | Gephi |
| Arthur y Andersen | Arthur Andersen |
| Big F, Big Ford | Big Five, Big Four |
| longil | long tail (cola larga) |
| vingear | bingear, ver una serie de corrido (binge-watching) |
| Rexis | RecSys, sistemas de recomendación |
| Ormús | estrecho de Ormuz |
| Lisa | un asistente o bot de grabación que entró a la llamada (**dudoso**) |
