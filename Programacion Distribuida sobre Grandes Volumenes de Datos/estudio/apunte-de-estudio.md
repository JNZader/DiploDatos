# Apunte de estudio: Programación Distribuida sobre Grandes Volúmenes de Datos (Diplodatos, FAMAF UNC, Damián Barsotti)

**Curso:** Programación Distribuida sobre Grandes Volúmenes de Datos, materia optativa de la Diplomatura en Ciencia de Datos, Aprendizaje Automático y sus Aplicaciones de FAMAF (UNC), cohorte 2026 · Docente: Damián Barsotti (es el único docente que figura en la página oficial de la materia y el que da las cuatro clases) · Formato: cuatro clases sincrónicas por Meet, grabadas en 11 videos del canal FAMAF UNC (dos no listados): viernes 25 de septiembre a la tarde, sábado 26 de septiembre a la mañana, viernes 2 de octubre a la tarde y sábado 3 de octubre a la mañana de 2026. Según la página oficial son 16 horas sincrónicas más 8 de apoyo, y se evalúa con trabajos prácticos en notebooks de Zeppelin.

**De qué va:** es la materia de "qué hago cuando los datos no entran en una computadora". Arranca con el problema (volumen, velocidad y variedad; mover datos es más caro que procesarlos), la programación de flujo de datos y MapReduce, y sigue con Apache Spark en cuatro capas: la API de bajo nivel (RDD, transformaciones, acciones, evaluación perezosa, cache, particiones, etapas y shuffle), Spark SQL y DataFrames (lectura de CSV y JSON, consultas SQL y declarativas, UDF, joins, broadcast, Parquet, ORC y tablas permanentes), aprendizaje automático con MLlib (estimadores y transformadores, VectorAssembler, StringIndexer, árboles, bosques, regresión logística, SVM lineal, expansión polinomial, pipelines, hashing de texto, KMeans) y grafos con GraphFrames (grados, PageRank, influencia colectiva con pasaje de mensajes, motif finding y visualización con Gephi). Los datasets son los del repositorio de la materia: vuelos de 2008 (`flights.csv`), usuarios de Last.fm (`userid-profile.tsv`), personas con peso, altura y sexo, y una red de retuits de 2017 sobre un conflicto docente. Se aprueba entregando los notebooks con los ejercicios resueltos.

> Nota: este apunte sale de los subtítulos automáticos en español de los 11 videos (los 11 tenían subtítulos de la grabación, no hizo falta transcribir con whisper). La página oficial de la materia en el sitio de la diplomatura confirma el nombre, el docente (Damián Barsotti), los módulos, la bibliografía, la carga horaria y la evaluación con notebooks de Zeppelin; la página general de equipo docente no lo lista. En la organización DiploDatos de GitHub no hay repositorio de esta materia. El repositorio 2026 está en Bitbucket y no es público, así que usé el repositorio público anterior del docente en el GitLab de FAMAF (`git.cs.famaf.unc.edu.ar/dbarsotti/diplodatos_bigdata`), que es la **versión 2019**: notebooks en Scala, siete clases (en 2019 el 07 era grafos; en 2026 grafos es el 08) y la misma carpeta `ds/` con los datasets. Corrí en el box, con PySpark 3.5.9, el código de las clases contra esos datasets. Muchos nombres vienen deformados en la transcripción (ver el glosario al final). Cuando lo que se dijo está mal o es impreciso, lo marco como **Corrección** o **Matiz**. Las cifras, fechas y afirmaciones que no pude chequear van como **dudoso** o **para verificar**. Lo que dice "verificado en el box" lo comprobé corriendo código (los scripts y salidas están en la guía de implementación).

**Cómo leer los links:** cada link dice el video y el minuto. "C2P1 1:23:45" es la clase 2, parte 1, en la hora 1, minuto 23, segundo 45.

## Los 11 videos

| # | Id | Video | Contenido | Duración | Link |
|---|---|---|---|---|---|
| 1 | — | C1P1: "Clase 1 Programación distribuida..." (viernes 25/09/2026, 17:45; no listado) | Presentación, big data, unidades, clústeres, MPI, flujo de datos, MapReduce, sistemas de archivos distribuidos, Spark, contenedores, entorno | 2:31:46 |  |
| 2 | — | C1P2: "Clase 1..." (25/09, después del recreo) | Docker y Zeppelin locales, arquitectura de Spark, word count en PySpark, Spark UI, spark-submit, ejercicios 1 | 1:06:54 |  |
| 3 | — | C2P1: "Clase 2..." (sábado 26/09, 09:48) | Notebook 02 Spark Core: driver y ejecutores, masters, RDD, union e intersection, particiones y etapas, evaluación perezosa, cache, ejercicios de logs y vuelos | 1:57:07 |  |
| 4 | — | C2P2: "Clase 2..." (26/09) | Notebook 03 Spark SQL: SparkSession, formatos, userid-profile, SQL vs DataFrame, JDBC, Parquet, people.json, word count con DataFrames | 1:13:47 |  |
| 5 | — | C2P3: "Clase 2..." (26/09) | Repaso, notebook 04: flights.csv, columnas, filtro con cache, anticipo de UDF | 18:53 |  |
| 6 | — | C3P1: "Clase 3..." (viernes 02/10, 17:46; no listado) | UDF, agregaciones, SQL y UDF registradas, CASE, ORC, volúmenes de Docker, tablas permanentes, joins y broadcast | 1:41:25 |  |
| 7 | — | C3P2: "Clase 3..." (02/10) | Notebook 05 ML: estimadores y transformadores, dataset de personas, particiones, VectorAssembler, StringIndexer, árbol de decisión, grilla | 1:19:25 |  |
| 8 | — | C3P3: "Clase 3..." (02/10, última parte) | Random forest, regresión logística, LinearSVC, PolynomialExpansion | 31:00 |  |
| 9 | — | C4P1: "Clase 4..." (sábado 03/10, 09:56) | Notebook 06: texto a vectores, Tokenizer, HashingTF, Pipeline, PipelineModel, guardar y cargar | 58:50 |  |
| 10 | — | C4P2: "Clase 4 2..." (03/10) | Vuelta al notebook 05: KMeans sobre cinco nubes 3D, BisectingKMeans | 24:50 |  |
| 11 | — | C4P3: "Clase 4..." (03/10, última parte) | Notebook 08 grafos: GraphFrames, Gephi, PageRank, red de retuits, influencia colectiva, motif finding, ejercicios y entregas | 2:15:32 |  |

Duración total: 14:19:29.

**Cómo se determinó el orden.** Los títulos traen número de clase y la fecha y hora de inicio de la reunión (25/09 17:45, 26/09 09:48, 02/10 17:46 y 03/10 09:56), pero no el número de parte. Las clases 1 y 2 se subieron el 28 y 29/09/2026 y las 3 y 4 el 06/10/2026. Dentro de cada clase ordené por continuidad del contenido. C1P1 termina en el recreo C1P1 2:31:16 y C1P2 arranca con Docker local, que es lo que se había anunciado C1P2 0:07. C2P1 cierra anunciando Spark SQL C2P1 1:56:13, C2P2 abre con el notebook 03 de Spark SQL C2P2 0:05 y cierra con el ejercicio de registraciones y los grupos C2P2 1:10:09, y C2P3 empieza repasando SQL vs DataFrame C2P3 0:07. C3P1 cierra "fin de datos tabulares, empieza ML" C3P1 1:41:02 y C3P2 abre con el notebook 05 de ML C3P2 0:09. **C3P3 se subió antes que C3P2, pero va después**: C3P2 termina con "recreo; después random forest" C3P2 1:18:36 y C3P3 empieza con el sobreajuste del árbol y sigue con random forest C3P3 0:05. C4P1 termina con "pausa de 10 minutos y volvemos al notebook 05 para clustering" C4P1 56:22, C4P2 hace justamente eso C4P2 0:06 y cierra con "sigue grafos" C4P2 22:24, y C4P3 abre con el notebook 08 de grafos C4P3 0:07.

## Mapa de módulos y videos

| Módulo | Dónde se ve |
|---|---|
| 0. La materia: docente, cursada, entregas | C1P1 (inicio), C2P1 (inicio), C2P2 (final), C3P1, C4P3 (final) |
| 1. Big data: las tres V, ejemplos y unidades | C1P1 |
| 2. Por qué clústeres: MPI, leyes de crecimiento y flujo de datos | C1P1 |
| 3. MapReduce y sistemas de archivos distribuidos | C1P1 |
| 4. Spark: qué agrega, arquitectura y lenguajes | C1P1 (final), C1P2, C2P1 |
| 5. El entorno: Docker, Zeppelin, CCAD y Git | C1P1 (final), C1P2, C2P1, C3P1 |
| 6. RDD: transformaciones, acciones y el word count | C1P2, C2P1 |
| 7. Ejecución distribuida: driver, ejecutores, particiones, etapas y shuffle | C2P1 |
| 8. Evaluación perezosa y cache | C2P1 |
| 9. Spark SQL y DataFrames | C2P2, C2P3 |
| 10. UDF, agregaciones y consultas sobre vuelos | C2P3, C3P1 |
| 11. Formatos, tablas permanentes y joins | C2P2, C3P1 |
| 12. ML en Spark: estimadores, transformadores y preparación de features | C3P2 |
| 13. Clasificadores: árbol, random forest, logística, SVM lineal y expansión polinomial | C3P2, C3P3 |
| 14. Pipelines y texto | C4P1 |
| 15. Clustering | C4P2 |
| 16. Grafos con GraphFrames | C4P3 |

---

## 0. La materia: docente, cursada, entregas
**Dónde:** C1P1 0:09, C1P1 1:21, C1P1 4:21, C1P1 7:16, C2P1 14:21, C2P1 15:25, C2P2 1:10:09, C3P1 36:00, C3P1 39:24, C4P3 2:00:14

### Conceptos clave
- **Quién.** Damián Barsotti se presenta como docente investigador de FAMAF, licenciado y doctor en computación, con trabajo de vinculación tecnológica (consultoría para empresas y el Estado). Cuenta proyectos propios: una visualización de redes de músicos de un festival de jazz hecha con Zeppelin, simulaciones de redes neuronales naturales, ML con físicos para ondas gravitacionales, predicción de retuits con grafos y un sistema RAG on premise para una empresa de dispositivos educativos C1P1 1:21, C1P1 3:09.
- **Estructura.** Dos bloques de 8 horas: el primero (clases 1 y 2) es Spark para datos estructurados y semiestructurados; el segundo (clases 3 y 4) es ML y grafos C1P1 7:16. **Matiz:** la página oficial lista cinco módulos (introducción, RDD, conceptos de computación distribuida, interfaz SQL y ML) y no menciona grafos, aunque en 2026 la última clase es entera de grafos (y en el repo 2019 también había un notebook de grafos).
- **Material.** Todo está en un repositorio git que hay que clonar y actualizar con `git pull` antes de cada clase, porque el docente corrige y agrega cosas C1P1 4:21, C2P1 5:27, C3P1 2:23. Las indicaciones de instalación están en el README del repo y en el aula virtual C2P1 0:10.
- **Bibliografía.** La presentación trae varios libros; *Learning Spark* es el clásico, y el docente avisa que están "viejitos" C2P1 15:25. Cuenta que esta materia en FAMAF es de grado y posgrado y dura 120 horas, contra las 16 de la diplomatura C2P1 15:25. La página oficial lista *Learning Spark* (2015), *High Performance Spark* (2017), *Machine Learning with Spark* (2017) y *Advanced Analytics with Spark* (2015).
- **Consultas.** Por Slack (canal de Big Data) y en clases de consulta técnica entre semana C1P2 58:14, C2P1 14:21, C4P3 2:13:08.
- **Cómo se aprueba.** Los ejercicios de los notebooks son el examen: se corre el notebook completo, se llenan las celdas de ejercicio y se sube al aula virtual C2P2 1:11:21, C3P1 40:32. Se trabaja en grupos de 3 o 4 que se arman con un formulario C2P2 1:12:32. Las fechas que da al final: notebooks 1 a 4 la penúltima semana de octubre y 5, 6 y 8 la última (el 7, de búsqueda de hiperparámetros, no se entrega); un formulario por notebook, y el 8 va con las dos imágenes exportadas de Gephi C4P3 2:01:19, C4P3 2:03:01. Para entregar se exporta el notebook desde Zeppelin C4P3 2:12:00.
- **Sobre la IA.** Pide hacer los ejercicios sin IA: no hace falta ser experto en SQL, pero sí entender lo que genera un LLM porque "alucinan" C3P1 37:07, C3P1 38:17, C4P3 2:00:14.

---

## 1. Big data: las tres V, ejemplos y unidades
**Dónde:** C1P1 13:26, C1P1 16:11, C1P1 17:16, C1P1 22:18, C1P1 26:19, C1P1 35:13, C1P1 39:19

### Conceptos clave
- **Una palabra ambigua.** "Big data" se usa para muchas cosas; las fuentes típicas son redes sociales, la IA y los LLM ("una cantidad insana de datos") y los sensores (IoT) C1P1 13:26, C1P1 15:05.
- **Las tres V.** Volumen, velocidad y variedad. La materia se centra en el volumen C1P1 16:11, C1P1 17:16.
- **Ejemplos que da** (casi todos van como **para verificar**, ver "Correcciones y matices"): un Boeing 787 genera unos 500 GB por vuelo; el CERN "un petabyte por segundo" C1P1 17:16, C1P1 18:28; Netflix como 15% del tráfico de internet en 2022 C1P1 21:07; PepsiCo armando un lakehouse con Databricks, la empresa de los creadores de Spark C1P1 21:07, C1P1 22:18; los satélites SAOCOM 1A y 1B (2018 y 2020) con unos 100 TB por año de imágenes para humedad de suelo en la región pampeana, cruzados con el catastro rural de Córdoba (IDECOR) C1P1 22:18, C1P1 24:01. La idea que repite es que "el dato es valor" C1P1 23:25.
- **El Event Horizon Telescope.** Ocho radiotelescopios generaron tanto que los discos se llevaron en avión (media tonelada); "no hay internet que le gane a 5 PB en un avión" C1P1 26:19, C1P1 33:00. La lección: el problema no es guardar los datos sino moverlos.
- **Unidades.** PB = 1000 TB, EB = 1000 PB, después ZB e YB C1P1 35:13, C1P1 36:21. Cuenta que en 2022 se agregaron el ronnabyte y el quettabyte, y que el "brontobyte" no es oficial C1P1 38:07. Según IDC (Global DataSphere) el mundo pasó de 33 ZB en 2018 a 149 ZB en 2024 y 181 ZB en 2025, con 394 ZB proyectados para 2028 C1P1 39:19, C1P1 40:29.

---

## 2. Por qué clústeres: MPI, leyes de crecimiento y flujo de datos
**Dónde:** C1P1 42:16, C1P1 46:10, C1P1 49:29, C1P1 55:33, C1P1 58:26, C1P1 1:06:11

### Conceptos clave
- **Regla práctica.** Si los datos entran en una computadora, usá scikit-learn; si no, hace falta un clúster: nodos conectados por una red rápida, con hardware que escala horizontalmente (sumando máquinas) C1P1 42:16, C1P1 43:22. Spark también sirve en una sola máquina con muchos núcleos C1P1 45:04.
- **Almacenamiento compartido.** Servidores de disco en red (filers, NAS); compara S3 con un filer C1P1 46:10, C1P1 47:19 (**Matiz:** S3 es almacenamiento de objetos, no un sistema de archivos en red).
- **Programación paralela clásica.** MPI y pasaje de mensajes C1P1 49:29, C1P1 50:03. Problemas: es difícil de programar, no tolera fallas (si cae un nodo, se cae todo) C1P1 51:08, el filer central es un cuello de botella C1P1 52:13 y casi no se usa en empresas ni en la nube C1P1 53:21.
- **Las curvas que se separan.** Ley de Moore (capacidad de cómputo), ley de Kryder (almacenamiento) y ley de Nielsen (ancho de banda de usuario, 50% por año): el almacenamiento y el cómputo crecen más rápido que la red, así que mover datos es cada vez más caro en relación C1P1 55:33, C1P1 57:20, C1P1 58:26.
- **Programación de flujo de datos (data flow).** En vez de traer los datos al programa, se lleva el programa a donde están los datos C1P1 58:26, C1P1 59:31. El sistema paraleliza solo, divide en tareas C1P1 1:01:10 y tolera fallas C1P1 1:07:18; a cambio, hay que escribir el programa con un conjunto restringido de patrones o "esqueletos" C1P1 1:06:11.

---

## 3. MapReduce y sistemas de archivos distribuidos
**Dónde:** C1P1 1:08:25, C1P1 1:15:30, C1P1 1:22:32, C1P1 1:30:26, C1P1 1:38:10, C1P1 1:40:25, C1P1 1:50:18

### Conceptos clave
- **El patrón.** Los datos se parten en splits; una función **map** produce pares (clave, valor); el sistema agrupa por clave moviendo datos por la red (**shuffle**); una función **reduce** combina los valores de cada clave C1P1 1:08:25, C1P1 1:15:30, C1P1 1:18:24. El programador escribe solo map y reduce C1P1 1:19:30. El shuffle es lo más caro C1P1 1:20:03.
- **Word count, el "Hola mundo".** Map: cada palabra pasa a (palabra, 1); shuffle; reduce: suma C1P1 1:22:32, C1P1 1:25:26. Los splits no tienen por qué ser iguales; elegirlos bien reduce el shuffle C1P1 1:29:20.
- **Qué se resuelve con MapReduce.** PageRank (el problema que originó MapReduce en Google), grep y sort distribuidos, recorrido del grafo de links, índice invertido, varios algoritmos de ML (regresión logística, random forest, k-means) y hasta motores SQL como Apache Hive C1P1 1:30:26, C1P1 1:33:12, C1P1 1:35:27, C1P1 1:36:31.
- **Lenguajes declarativos.** Decís qué querés y el sistema decide cómo; con gestores de clúster y tolerancia a fallas C1P1 1:38:10, C1P1 1:39:17.
- **Sistemas de archivos distribuidos.** Los datos se parten entre nodos y se leen en paralelo; el sistema sabe dónde está cada parte C1P1 1:40:25, C1P1 1:42:05. La **replicación** (copias en varios nodos) da localidad y tolerancia a fallas a cambio de espacio C1P1 1:45:25; S3 es más barato pero más lento C1P1 1:48:07. Google File System fue el original y HDFS es la versión libre C1P1 1:49:15.
- **El límite de MapReduce.** Es malo para algoritmos iterativos porque escribe a disco (con réplicas) en cada iteración; PageRank necesita unas 10 C1P1 1:50:18, C1P1 1:53:01. Spark nace para resolver eso C1P1 1:55:15.

---

## 4. Spark: qué agrega, arquitectura y lenguajes
**Dónde:** C1P1 1:55:15, C1P1 2:00:14, C1P2 15:12, C1P2 18:06, C1P2 22:00, C1P2 23:08, C2P1 20:23, C2P1 22:04

### Conceptos clave
- **Qué es.** MapReduce con los datos intermedios en memoria, con una visión global del programa (lo compila entero) y muchas más operaciones que map y reduce (filter, join...) C1P1 1:55:15, C1P1 1:56:20, C1P2 16:19. Lee de HDFS, Cassandra, cualquier base relacional por JDBC, S3 C1P2 16:19.
- **"100 veces más rápido".** La diapositiva dice que Spark es 100 veces más rápido que Hadoop MapReduce en memoria y 10 veces en disco, con regresión logística C1P2 15:12. Es la cifra que publicaba el propio proyecto (**Matiz:** benchmark del autor, sobre un algoritmo iterativo, el caso más favorable).
- **Historia.** Proyecto académico de 2009 en Berkeley, Apache desde 2013, y la empresa Databricks de sus creadores C2P1 20:23. En C1P1 dice "el paper de Spark es del 2009" C1P1 2:00:14 (**Corrección:** el proyecto arranca en 2009, pero el primer paper, "Spark: Cluster Computing with Working Sets", es de HotCloud 2010).
- **Capas.** Gestor de clúster abajo (standalone, YARN, Mesos; también Kubernetes) C1P2 18:06; Spark Core con los RDD; arriba Spark SQL (lo más usado), Streaming, MLlib y GraphX, que se pueden combinar en un mismo programa C1P2 19:12, C1P2 21:26, C2P1 22:04. Streaming no se ve en el curso C1P1 1:59:09.
- **Lenguajes.** Python, R, Java y Scala; Spark está escrito en Scala y corre en la JVM C1P2 22:00. PySpark habla con la JVM a través de Py4J C2P1 1:43:03.
- **Hadoop vs Spark en código.** El word count de Hadoop en Java ocupa una clase con map y reduce; en Spark son 12 líneas C1P2 23:08, C1P2 26:00. Dice que en Hadoop "no se puede en Python" C1P2 24:18 (**Matiz:** existe Hadoop Streaming, que acepta mappers y reducers en cualquier lenguaje, incluido Python).

---

## 5. El entorno: Docker, Zeppelin, CCAD y Git
**Dónde:** C1P1 9:31, C1P1 2:04:16, C1P1 2:14:19, C1P1 2:21:08, C1P2 0:07, C1P2 4:03, C1P2 10:11, C2P1 2:57, C2P1 8:15, C3P1 1:18:40, C3P1 1:22:15

### Conceptos clave
- **Zeppelin.** Notebooks parecidos a Jupyter, de Apache, que además grafican resultados de SQL C1P1 9:31, C1P1 2:00:14. Cada celda arranca con el intérprete: `%pyspark`, `%sql`, `%sh`, `%html`, `%md` C2P1 1:00:00, C2P2 13:07, C3P1 28:07. En Zeppelin `sc` (SparkContext), `spark` (SparkSession) y `z` (el contexto de Zeppelin, con `z.show`) ya vienen creados C1P2 27:08, C2P2 21:21. El intérprete Spark se reinicia desde el menú Interpreter y vuelve a arrancar de forma perezosa en la próxima celda C2P1 56:22, C2P1 58:02.
- **Contenedores.** Explica máquinas virtuales vs contenedores: un contenedor aísla procesos, memoria, disco y red en el mismo kernel Linux y es mucho más liviano C1P1 2:04:16, C1P1 2:10:24. En Windows, Docker usa WSL2, que levanta una VM Linux, y es más pesado C1P1 2:13:13 (**Matiz:** existen contenedores Windows nativos, pero las imágenes Linux como la del curso necesitan WSL2 o Hyper-V). Spark también corre sobre YARN y Kubernetes con escalado dinámico C1P1 2:07:01.
- **Imagen vs contenedor.** La imagen es el molde (la define el Dockerfile); el contenedor es una copia en ejecución C2P1 8:48, C3P1 3:28. Sirve para que todo el equipo tenga el mismo entorno C2P1 8:15.
- **Opción recomendada: Docker local.** Mínimo 8 GB de RAM, Git y Docker C1P1 2:15:27. En el repo hay una carpeta `docker` con `zeppelin.sh` (Linux) y `zeppelin.cmd` (Windows) C1P2 1:15. La primera construcción baja unos 9 GB C1P2 5:18. El comando de arranque monta carpetas de la máquina real con `-v` (conf, logs, notebooks y el repo); sin eso, todo lo que hagas se pierde al apagar C1P2 7:26, C3P1 1:19:26. `--rm` borra el contenedor al apagarlo C3P1 1:22:15. Los notebooks quedan en `/home/jovyan/notebooks` C1P2 8:32. Zeppelin se abre en `localhost:8080` y la interfaz de Spark en el puerto 4040 C1P2 10:11, C1P2 46:06.
- **Alternativa: JupyterHub del CCAD.** Con cuenta UNC, entorno "diplodatos", 6 GB de RAM y 2 núcleos; tiene un botón de Zeppelin C1P1 2:18:15, C2P1 4:07. Ahí solo persiste el home C3P1 1:21:05 y `sc.defaultParallelism` da 2 en vez de 8 C2P1 31:09.
- **Importar notebooks.** Desde el navegador de la máquina real, con "Import note" y el JSON del repo C1P1 2:23:33, C1P2 11:19. Las imágenes de los notebooks pueden no verse porque están alojadas en Bitbucket C1P2 13:31.
- **Git.** `git clone` del repositorio `diplodatos_bigdata` y `git pull` antes de cada clase; recomienda la terminal antes que GitHub Desktop C1P1 10:05, C1P1 2:21:08. Avisa que `rm -rf` hay que usarlo con cuidado C1P1 2:21:08.
- **Dónde quedan los archivos que escribe Spark.** `%sh pwd` da `/opt/zeppelin` en Docker local o el home de jovyan en el CCAD; lo que escribas fuera de los volúmenes montados se pierde C3P1 1:18:40.

---

## 6. RDD: transformaciones, acciones y el word count
**Dónde:** C1P2 27:08, C1P2 35:24, C1P2 38:18, C1P2 42:15, C1P2 48:15, C1P2 52:27, C1P2 1:00:27, C2P1 39:31, C2P1 42:19, C2P1 50:14

### Conceptos clave
- **RDD (resilient distributed dataset).** Una colección distribuida e inmutable, a prueba de fallas: si se cae un ejecutor, Spark recalcula la parte perdida C1P2 35:24, C2P1 41:10.
- **El word count en PySpark, línea por línea** C1P2 27:08:
  - `sc.textFile("README.md")` crea un RDD de líneas C1P2 28:15;
  - `flatMap(lambda line: line.split(" "))` aplana a un RDD de palabras C1P2 30:29;
  - `filter(lambda w: w)` saca las cadenas vacías, porque la cadena vacía es falsa en Python C1P2 33:15;
  - `map(lambda w: (w, 1))` y `reduceByKey(lambda a, b: a + b)` son el map y el reduce de MapReduce C1P2 35:24;
  - `sortBy(lambda p: p[1], ascending=False)` ordena y `collect()` trae el resultado como lista Python al driver C1P2 42:15, C1P2 43:25.
- **Local = clúster chiquito.** En modo local cada núcleo hace de nodo; el mismo programa corre en 20.000 máquinas cambiando solo cómo se crea `sc` C1P2 39:24. Nada se ejecuta hasta que pedís un resultado C1P2 41:05.
- **Directorios.** `sc.textFile` con un directorio lee todos los archivos (ejercicio 0 con las licencias) C1P2 48:15.
- **Fuera de notebooks.** `pyspark` o `spark-shell` interactivos, o un programa autónomo con `spark-submit wordcount.py`; si el 4040 está ocupado, la UI pasa al 4041 (que el contenedor no exporta) C1P2 52:27, C1P2 54:11, C1P2 56:27. En un programa autónomo hay que crear el SparkContext o la SparkSession a mano C2P1 28:06.
- **Transformaciones binarias.** `union` es el "o" y `intersection` el "y"; el ejemplo filtra líneas de logs con "error" y con "config" y las une C2P1 42:19, C2P1 48:33.
- **¿Por qué no un for de Python?** Porque `collect()` trae todo a una sola máquina, que puede quedarse sin memoria y no aprovecha el clúster; hay que expresarse con los esqueletos (map, filter, reduce, union...) C2P1 50:14, C2P1 54:10.
- **Ejercicios del notebook 01** C1P2 1:00:27: contar letras en vez de palabras cambiando solo la línea del `flatMap`, y, con `links_raw.txt` (cada línea es una URL seguida de las URLs a las que apunta), contar cuántos links apuntan a cada página, que es la base de PageRank C1P2 1:02:14, C1P2 1:05:01. Verificado en el box que `links_raw.txt` tiene 5027 líneas.

---

## 7. Ejecución distribuida: driver, ejecutores, particiones, etapas y shuffle
**Dónde:** C2P1 24:18, C2P1 31:09, C2P1 36:09, C2P1 1:00:00, C2P1 1:06:14, C2P1 1:09:05, C2P1 1:27:18

### Conceptos clave
- **Driver y ejecutores.** Tu programa corre en el **driver**, que tiene el SparkContext; los **ejecutores** viven en los nodos y reciben **tareas** C2P1 24:18.
- **Masters.** `sc.master` da `local[*]` (todos los núcleos) y `sc.defaultParallelism` da 8 en su máquina C2P1 31:09. Otras opciones: `local` (un hilo), `local[K]`, `spark://` (standalone), Mesos, YARN y `k8s://` C2P1 36:09. En la nube, con Kubernetes y máquinas que se prenden y apagan, la tolerancia a fallas permite usar instancias baratas interrumpibles (spot) C2P1 37:16.
- **Spark en una sola máquina.** A veces le gana a scikit-learn porque usa todos los núcleos C2P1 34:25 (**Matiz:** depende del problema; para datos chicos el costo de arrancar la JVM y de serializar entre Python y la JVM suele dominar).
- **Particiones.** Un RDD (o DataFrame) se divide en particiones; cada tarea procesa una partición C2P1 1:06:14. En una etapa puede haber muchas más tareas que núcleos (por ejemplo 55 tareas de a 8) C2P1 1:27:18. Un alumno ve 12 tareas en vez de 8 por hyperthreading o núcleos heterogéneos C2P1 1:01:08.
- **Etapas y shuffle.** El grafo de operaciones (DAG) se corta en **etapas** donde hay shuffle, es decir, intercambio de datos por red C2P1 1:02:16, C2P1 1:09:05. En la Spark UI se ven jobs, etapas, tareas y el DAG C1P2 46:06, C2P1 1:00:00.
- **Linaje.** Si se caen nodos, Spark recalcula solo lo que falta siguiendo el linaje; funciona también con S3 sin replicación C2P1 1:51:21, C2P1 1:52:25.

---

## 8. Evaluación perezosa y cache
**Dónde:** C2P1 1:11:20, C2P1 1:14:19, C2P1 1:17:30, C2P1 1:21:44, C2P1 1:25:00, C2P1 1:33:17, C2P1 1:40:05, C2P1 1:45:17

### Conceptos clave
- **Transformaciones y acciones.** Las transformaciones (map, filter, union...) solo arman el grafo; las acciones (collect, take, count...) disparan la ejecución C2P1 1:17:30. Si copiás el word count sin la acción final, Spark no ejecuta nada C2P1 1:14:19. Verificado en el box: la cantidad de jobs es la misma antes y después de definir un `map`.
- **Por qué conviene.** Con todo el grafo a la vista, Spark optimiza: con `take(1)` sobre las licencias usa 56 tareas en vez de 110 C2P1 1:21:44, y el filtro de logs con `take(2)` corre 1 tarea en vez de 8 C2P1 1:24:27. También facilita recuperar fallas C2P1 1:23:23.
- **¿Dos filter o uno?** Un alumno pregunta si conviene un solo `filter`; responde que Spark "quizás" los fusiona C2P1 1:25:00 (**Matiz:** en RDD, las transformaciones angostas consecutivas se encadenan dentro de la misma etapa, pipelining, así que no hay doble pasada; con DataFrames el optimizador Catalyst además las combina en un solo predicado. Verificado en el box: el plan optimizado de dos `filter` encadenados sobre `flights` muestra un único `Filter` con los dos predicados).
- **Matiz verificado en el box:** no todo es perezoso. `reduceByKey` sin número de particiones consulta las particiones del RDD padre al definirse, así que si el archivo de entrada no existe el error salta en esa línea y no en la acción.
- **El problema de la evaluación perezosa.** `sc.parallelize(range(30)).map(lambda x: x*x)` seguido de `mean()` y `collect()`: son dos acciones y los cuadrados se calculan dos veces C2P1 1:33:17. Dice que "es computacionalmente imposible darse cuenta, está demostrado" C2P1 1:39:02 (**dudoso:** la documentación de Spark lo plantea como decisión de diseño, "cada RDD transformado puede recalcularse cada vez que corrés una acción sobre él" salvo que lo persistas; no encontré ningún resultado de imposibilidad citado).
- **cache.** `.cache()` (y `.setName("cuadrados")` para verlo con nombre) guarda el resultado la primera vez que se calcula; en el DAG aparece un punto verde y en la pestaña Storage el RDD guardado C2P1 1:40:05. Verificado en el box con un acumulador: sin cache la función se evaluó 60 veces para 30 elementos; con cache, 30.
- **Ejercicios del notebook 02** C2P1 1:27:18, C2P1 1:43:03, C2P1 1:48:24: contar la letra "c" en los logs; contar líneas que empiezan con INFO, WARN y ERROR usando cache donde convenga; y con `flights.csv` y la API de RDD, el porcentaje de vuelos cancelados (columna 22) y desviados (columna 24), usando `split(",")`, índices desde 0 y restando el encabezado, más el máximo de la columna 14 (AirTime) cuidando los "NA" C2P1 1:50:09. Verificado en el box que el encabezado coincide (Cancelled es la 22, Diverted la 24 y AirTime la 14, contando desde 1) y que hay valores "NA" en AirTime.

---

## 9. Spark SQL y DataFrames
**Dónde:** C2P2 0:05, C2P2 5:34, C2P2 7:19, C2P2 10:21, C2P2 16:07, C2P2 24:10, C2P2 31:21, C2P2 58:03, C2P2 1:02:00, C2P2 1:07:21, C2P3 3:11

### Conceptos clave
- **Para qué.** Datos tabulares y semiestructurados (JSON); como tienen estructura regular, Spark los optimiza mejor C2P2 0:05, C2P2 2:05. Dos sabores: SQL y DataFrames (parecido a pandas); también existe una API de pandas sobre Spark C2P2 2:05, C2P2 3:19. Los Datasets tipados existen solo en Scala y Java C2P2 5:34.
- **SparkSession.** El punto de entrada es `spark`; `spark.sparkContext` devuelve el `sc` de siempre C2P2 7:19, C2P2 10:21.
- **Formatos y fuentes.** JSON, CSV, Parquet, ORC y texto; archivos locales o distribuidos, JDBC (por ejemplo PostgreSQL), Hive, Redshift, S3, Azure, Cassandra, MongoDB, Neo4j C2P2 10:21, C2P2 11:28.
- **Leer un CSV.** Con `userid-profile.tsv` (usuarios de Last.fm: id, gender, age, country, registered): `spark.read.format("csv").option("delimiter", "\t").option("header", "true").option("inferSchema", "true").load(...)` C2P2 13:07, C2P2 16:07. `printSchema()` muestra age como entero; sin `inferSchema` todo es string C2P2 19:30. `show()` muestra 20 filas y en Zeppelin `z.show(df.limit(20))` da una tabla con gráficos C2P2 21:21. Verificado en el box: age se infiere como integer y el archivo tiene 992 filas.
- **SQL.** `profiles.createOrReplaceTempView("users")` registra una vista sin copiar datos y `spark.sql("SELECT country, count(*) AS cantidad FROM users GROUP BY country ORDER BY cantidad DESC")` devuelve un DataFrame C2P2 24:10, C2P2 28:01, C2P2 55:12. Resultado: United States primero, después United Kingdom, y 85 nulos C2P2 31:21. Verificado en el box: United States 228, United Kingdom 126, nulos 85, Poland 50.
- **Lo mismo con DataFrames.** `profiles.groupBy("country").agg(count("*").alias("cantidad")).orderBy(desc("cantidad"))`, importando `count` de `pyspark.sql.functions`; la agregación colapsa filas C2P2 32:27, C2P2 34:29. Un solo query genera muchos jobs en la Spark UI C2P2 38:29, C2P3 1:12. En Zeppelin también se puede escribir la celda con `%sql` C2P2 40:11.
- **people.json.** JSON Lines: `spark.read.json(...)`, `selectExpr("name", "age + 1")` o `df.select(df["name"], df["age"] + 1)`, `filter(df["age"] > 21)`, `groupBy("age").count()` C2P2 58:03. Verificado en el box: el archivo tiene tres personas (Michael sin edad, Andy de 30 y Justin de 19), así que `age > 21` deja solo a Andy.
- **Word count con DataFrames.** `spark.read.text`, `split` y `explode`, filtrar vacías y `groupBy("palabra").count()` C2P2 1:02:00. Los DataFrames gastan menos memoria y corren más rápido que los RDD gracias a Catalyst (optimizador) y Tungsten (ejecución) C2P2 1:06:16. Las optimizaciones clásicas de bases de datos, como filtrar antes de agrupar, son las que aplica C2P3 3:11.
- **Errores.** SQL detecta los errores de sintaxis recién al ejecutar; los DataFrames detectan la sintaxis antes, y los Datasets también los errores de análisis (tipos) C2P2 1:07:21, C2P2 1:08:28.
- **Ejercicios del notebook 03** C2P2 41:18, C2P2 56:20, C2P2 1:10:09: usuarios por país y género en SQL y DataFrame; edad promedio por género guardada como tabla SQL y como Parquet; y registraciones por día de la semana parseando las fechas. Verificado en el box que las fechas de `registered` tienen formato tipo "Aug 13, 2006" y se parsean todas con el patrón `MMM d, yyyy` (8 filas tienen la fecha vacía).

---

## 10. UDF, agregaciones y consultas sobre vuelos
**Dónde:** C2P3 4:17, C2P3 7:16, C2P3 12:19, C3P1 8:13, C3P1 9:20, C3P1 12:09, C3P1 17:18, C3P1 29:16, C3P1 42:14, C3P1 45:03, C3P1 51:14, C3P1 56:24, C3P1 1:02:04

### Conceptos clave
- **flights.csv.** Vuelos de 2008: `count()` da 100.000 filas C2P3 5:29, C3P1 8:13 (en C2P1 había dicho "unos 10000" C2P1 1:46:06; **verificado en el box: son 100.000**). Columnas: Year, Month, DayofMonth, DayOfWeek, DepTime (hhmm, 1829 son las 18:29), CRSDepTime (programado), ArrTime, UniqueCarrier, FlightNum, ArrDelay, DepDelay, Origin, Dest, Distance, TaxiIn, TaxiOut, Cancelled... C2P3 8:23. Vuelos con DepDelay > 15: 19.587 C3P1 9:20 (**verificado en el box**).
- **cache y niveles.** Cachea el DataFrame filtrado y muestra niveles de almacenamiento (memoria, disco) y la pestaña Storage C2P3 13:27, C2P3 14:01.
- **Matiz verificado en el box sobre "NA".** Con `inferSchema` y sin más opciones, las columnas con "NA" (DepDelay, ArrDelay, AirTime) se infieren como **string**. El filtro `DepDelay > 15` igual da 19.587 porque Spark castea al comparar, pero una UDF de Python que compara con un número falla con `TypeError` ('>' entre str e int). La solución es leer con `.option("nullValue", "NA")`: así esas columnas salen como enteros y los "NA" como nulos. Es el mismo problema de "NA" que el docente avisa para la versión con RDD C2P1 1:50:09.
- **UDF (user defined function).** Una función propia para salir del patrón declarativo, a cambio de perder optimización C3P1 9:20, C3P1 12:09. `is_delayed(t)` devuelve 1 si t > 15 y 0 si no; `udf(is_delayed, IntegerType())` la convierte en UDF, y hay que declarar el tipo de retorno porque Python no tiene tipos estáticos y las tablas sí C3P1 14:25, C3P1 16:09. Se usa como columna: `isDelayedUDF(col("DepDelay")).alias("IsDepDelayed")` C3P1 17:18. El porcentaje de demorados (suma por 100 sobre el total) da 19,587% C3P1 24:11, C3P1 27:02 (**verificado en el box**). Para traer un valor al driver usa `first().asDict()[...]` C3P1 26:29. **Matiz verificado en el box:** el plan físico con la UDF de Python tiene un nodo `BatchEvalPython` (los datos viajan de la JVM a un proceso Python y vuelven) que no aparece si escribís lo mismo con funciones nativas (`when`), por eso conviene usar UDF solo cuando no hay función nativa.
- **Agregaciones.** Promedio de TaxiOut por Origin y Dest con `groupBy("Origin", "Dest").agg(avg("TaxiOut").alias(...))` y `orderBy(desc(...))` C3P1 29:16. Verificado en el box: el primero es LCH a IAH con 84 minutos.
- **SQL con UDF.** `createOrReplaceTempView("flightsTbl")` y `spark.udf.register("isDelayedTabUDF", f, IntegerType())` para usarla dentro de SQL C3P1 42:14, C3P1 45:03. Por empresa, demorados en llegada: WN "17.000 y pico" y la otra 1041; dice que hay solo dos empresas C3P1 48:30, C3P1 49:03. Verificado en el box: solo hay dos (WN con 94.055 vuelos y XE con 5945) y los demorados en llegada son WN 17.753 y XE 1041.
- **La UDF registrada no persiste.** Al reiniciar Spark aparece el error "unresolved routine": la UDF vive en la sesión C3P1 51:14, C3P1 52:20.
- **Filtrar con la UDF.** Promedio de ArrDelay por empresa con `WHERE isDelayedTabUDF(ArrDelay) = 1`: WN unos 50 minutos y la otra unos 60 C3P1 56:24 (**verificado en el box:** 50,37 y 60,72). En la versión DataFrame le da error por no haber importado `avg` C3P1 1:01:31.
- **CASE y horas.** `CASE WHEN ... THEN 'delayed' ELSE 'ok' END` por día de la semana con el gráfico de barras de Zeppelin C3P1 1:03:09; por hora con `CAST(CRSDepTime / 100 AS INT)` porque el formato es hhmm C3P1 1:07:10. A las 13 h: 1346 demorados y 5225 no C3P1 1:11:22 (**verificado en el box**).
- **Ejercicios del notebook 04** C3P1 39:24, C3P1 1:02:04, C3P1 1:27:01, C3P1 1:37:03: promedio de TaxiIn por origen y destino; distancia promedio por empresa; vuelos por aeropuerto de origen en una tabla permanente; y el join con `airports.csv` (ver módulo 11).

---

## 11. Formatos, tablas permanentes y joins
**Dónde:** C2P2 42:24, C2P2 44:04, C2P2 48:11, C2P2 52:17, C3P1 1:12:36, C3P1 1:24:14, C3P1 1:28:09, C3P1 1:30:25, C3P1 1:33:09

### Conceptos clave
- **JDBC y Hive.** Conexión a PostgreSQL con url, dbtable, user y password; Hive con una SparkSession configurada para eso C2P2 42:24.
- **Tablas.** `DROP TABLE IF EXISTS mytable` y `CREATE TABLE mytable AS SELECT * FROM users`; sin un data warehouse externo, Spark usa la carpeta local `spark-warehouse` C2P2 44:04, C2P2 46:19. `SHOW TABLES` distingue las vistas temporales (users) de las tablas C2P2 52:17.
- **Parquet.** `profiles.write.mode("overwrite").save("profiles.parquet")` usa Parquet por defecto: columnar y legible en paralelo C2P2 48:11, C2P2 49:23. Lo que se escribe es un **directorio** con varios archivos part, uno por tarea C2P2 51:09. **Matiz verificado en el box:** con `userid-profile.tsv` (992 filas, una sola partición) sale un único archivo part; la cantidad de archivos depende de las particiones del DataFrame, no de los núcleos.
- **ORC y modos de escritura.** `write.format("orc").mode("overwrite").save("flights.orc")`; Parquet y ORC son columnares C3P1 1:12:36. Modos: error (por defecto), append, overwrite e ignore C3P1 1:14:12. Al releer compara conteos y dice "10.000" C3P1 1:14:12 (son 100.000; verificado en el box que el ORC releído tiene 100.000 filas).
- **Tablas permanentes.** `saveAsTable("flightsPermTbl", format="orc")` crea una tabla que sobrevive al reinicio de Spark C3P1 1:24:14. Para volver a DataFrame usa `sqlContext.table(...)` C3P1 1:27:01 (**Matiz:** en Spark 3 lo directo es `spark.table(...)`; `sqlContext` queda por compatibilidad).
- **Joins.** `flights.join(carrierDF, flights.UniqueCarrier == carrierDF.Code)` y renombrar a CarrierName C3P1 1:28:09. Son caros porque mueven datos (shuffle) C3P1 1:30:25. Tipos: inner, left, right, cross C3P1 1:31:30. Co-ubicar las claves es la optimización avanzada C3P1 1:33:09.
- **broadcast.** `broadcast(carrierDF)` replica la tabla chica en todos los nodos y evita el shuffle de la grande C3P1 1:33:09. Verificado en el box: el plan físico muestra `BroadcastHashJoin` y el join da Southwest Airlines Co. 94.055 y Expressjet Airlines Inc. 5945.
- **Ejercicio con `airports.csv`** (iata, airport, city, state, country, lat, long): dos joins, uno para el origen y otro para el destino C3P1 1:37:03.

---

## 12. ML en Spark: estimadores, transformadores y preparación de features
**Dónde:** C3P2 0:09, C3P2 2:28, C3P2 7:33, C3P2 12:02, C3P2 15:27, C3P2 22:01, C3P2 24:15, C3P2 30:04, C3P2 37:21, C3P2 48:06, C3P2 49:16, C4P1 0:06

### Conceptos clave
- **Solo algoritmos paralelizables.** Spark implementa la subclase de algoritmos de ML que se reparte bien entre máquinas C3P2 1:20, C3P2 11:30.
- **Dos APIs.** MLlib empezó sobre RDD (esa API está congelada, en mantenimiento) y hoy se usa la de DataFrames, `pyspark.ml`, que se mezcla con SQL para preparar los datos C3P2 2:28, C3P2 6:24.
- **Estimator y Transformer.** Un **Transformer** tiene `transform` y convierte un DataFrame en otro (agrega columnas, no saca); un **Estimator** tiene `fit` y devuelve un Transformer (el modelo) C3P2 12:02, C3P2 35:06. No confundir con los transformers de redes neuronales C3P2 12:02. En la clase 4 explica el porqué: es pensar en "tipos", que permiten detectar errores antes de correr, algo valioso cuando depurar en un clúster es difícil C4P1 0:06.
- **El dataset.** `people_sex_height_age_weight.json` (JSON Lines, datos reales con ruido agregado) C3P2 15:27, C3P2 20:24. Se lee con `spark.read.json(...).select(...).repartition(sc.defaultParallelism).cache()`: 10.000 filas en 8 particiones C3P2 17:06, C3P2 18:13. Sin `repartition` queda en una sola partición y se pierde el paralelismo C3P2 22:01. Verificado en el box: 10.000 filas, 1 partición sin `repartition` y 8 con. El objetivo didáctico es predecir el sexo a partir de peso y altura C3P2 24:15.
- **train y test.** `randomSplit([0.95, 0.05], seed)` le da 9532 y 468 filas C3P2 25:23; el test es chico a propósito para poder graficarlo C3P2 26:29. (En el box, con otra semilla, salieron 9492 y 508; los números exactos dependen de la semilla y del particionado.)
- **VectorAssembler.** `VectorAssembler(inputCols=["kgs", "mts"], outputCol="features")` junta las columnas en un vector; es un Transformer C3P2 30:04, C3P2 32:18.
- **StringIndexer.** `StringIndexer(inputCol="sex", outputCol="label", stringOrderType="alphabetDesc")` es un **Estimator**: hay que hacer `fit` para obtener un `StringIndexerModel`, que es el que transforma y agrega `label` C3P2 37:21. No se le puede hacer `show`, porque es un programa y no un DataFrame C3P2 44:07. Verificado en el box: los valores son "M" y "F", y con `alphabetDesc` queda M = 0 y F = 1.
- **Más featurizadores.** La documentación lista Word2Vec, Tokenizer, StopWordsRemover, OneHotEncoder, SQLTransformer y muchos más C3P2 48:06.
- **Visualizar.** En big data es difícil: la función de gráficos usa `toPandas()`, que trae todo al driver, así que con datos grandes hay que muestrear C3P2 49:16, C3P2 50:23. En el gráfico de peso contra altura no hay una frontera clara entre sexos: cualquier clasificador va a errar y un analista pediría más features C3P2 54:14.

---

## 13. Clasificadores: árbol, random forest, logística, SVM lineal y expansión polinomial
**Dónde:** C3P2 58:11, C3P2 1:02:02, C3P2 1:05:24, C3P2 1:17:18, C3P3 0:05, C3P3 2:15, C3P3 5:03, C3P3 8:30, C3P3 15:21, C3P3 18:10, C3P3 28:19

### Conceptos clave
- **Árbol de decisión.** `DecisionTreeClassifier(featuresCol="features", labelCol="label")` y `fit` dan el modelo C3P2 58:11; `explainParams()` lista impurity, maxBins, maxDepth y el resto C3P2 1:00:25. Con un formulario de Zeppelin predice para 60 kg y 1,50 m: femenino C3P2 1:02:02.
- **La grilla.** Arma una grilla sintética de pesos y alturas entre el mínimo y el máximo con `crossJoin`, la predice y grafica: la frontera del árbol es escalonada (cortes verticales y horizontales) C3P2 1:05:24, C3P2 1:09:01. Las columnas que agrega el modelo son rawPrediction, probability y prediction C3P2 1:07:13. Es una evaluación cualitativa C3P2 1:16:11.
- **Sobreajuste y bosques.** El árbol es simple y propenso al sobreajuste; los bosques (random forest y boosting como XGBoost) lo corrigen C3P3 0:05, C3P3 1:10. Dice que el boosting suele ganarle a las redes neuronales en datos tabulares C3P3 2:15 (**Matiz:** es lo que muestran varios benchmarks sobre datos tabulares medianos, no una ley).
- **Qué se paraleliza.** Predecir es fácil (filas a distintas máquinas, árboles en paralelo); entrenar es lo difícil C3P3 2:15.
- **RandomForestClassifier.** Con `numTrees`; la frontera sigue siendo escalonada C3P3 5:03. Los modelos simples a veces alcanzan y son más baratos C3P3 6:16.
- **Regresión logística.** Se entrena por descenso por gradiente, iterativo: el ejemplo clásico donde Spark le gana a MapReduce C3P3 8:30. Da probabilidades: para 95 kg y 1,70 m, 44% de ser mujer C3P3 10:07. La columna `probability` trae un vector de dos valores y para graficar se extrae uno C3P3 11:11. La frontera es lineal: con clases en círculos fallaría C3P3 13:44. Verificado en el box: con mi partición, la probabilidad de mujer para 95 kg y 1,70 m da 46%, y para 60 kg y 1,50 m da 98%.
- **LinearSVC.** Frontera recta C3P3 15:21. Los métodos lineales se paralelizan más fácil; el SVM con kernel radial no está en Spark, el árbol (no lineal) sí C3P3 16:32, C3P3 17:05.
- **PolynomialExpansion.** El truco para tener fronteras curvas con un método lineal: agregar como features los productos de las variables hasta cierto grado C3P3 18:10, C3P3 27:12. Hay que aplicar la misma expansión a la grilla C3P3 24:19. Más features es más costo, que se compensa con más máquinas C3P3 27:12. Dice "no es un transformer, es como el VectorAssembler" C3P3 22:05 (**Corrección:** PolynomialExpansion es un Transformer, igual que VectorAssembler; no tiene `fit`). Para grado 4 cuenta "12" features C3P3 25:28 (**Corrección verificada en el box:** con dos variables, grado 2 da 5 features, grado 3 da 9 y grado 4 da 14; el término constante no se incluye).
- **Una métrica numérica que en clase no se calcula** (verificado en el box, con el split 95/5): exactitud en test de 0,75 para el árbol de profundidad 5, 0,77 para el de profundidad 10, 0,76 para random forest, 0,73 para regresión logística y LinearSVC, y 0,75 a 0,76 para LinearSVC con expansión de grado 2 a 4. Las AUC de los modelos con probabilidad o margen continuo (bosque, logística, SVM) andan en 0,81 a 0,83. Todos rondan el mismo techo, lo que confirma lo que dice el docente: con dos features no se puede separar mucho mejor.
- **Ejercicios del notebook 05** C3P2 1:17:18, C3P3 28:19: árbol con `maxDepth=10` y su gráfico; expansión de grado 3 con regresión logística (el título dice SVM pero el código usa LogisticRegression).

---

## 14. Pipelines y texto
**Dónde:** C4P1 7:31, C4P1 10:28, C4P1 12:08, C4P1 16:15, C4P1 20:09, C4P1 25:06, C4P1 29:04, C4P1 35:10, C4P1 42:32, C4P1 46:00, C4P1 51:16, C4P1 54:08

### Conceptos clave
- **El flujo clásico.** Featurizar, entrenar, predecir; al predecir hay que repetir la featurización, y el código repetido es "caldo de cultivo de errores" C4P1 9:17, C4P1 35:10.
- **Ejemplo de juguete** (de la documentación de Spark, modificado en el repo): documentos con id, text y label, y la idea de clasificar si hablan de Spark C4P1 10:28.
- **Texto a números.** Embeddings (el estado del arte) o bolsa de palabras (sin semántica ni orden, vectores enormes) C4P1 13:18, C4P1 15:43. El **hashing trick** da vectores de tamaño fijo y admite palabras nuevas, a cambio de posibles colisiones C4P1 16:15. Dice que con MurmurHash3 las colisiones son "muy raras" C4P1 18:27, C4P1 26:11 (**Matiz verificado en el box:** depende del tamaño. Con `numFeatures=1000`, las 1126 palabras distintas de la presentación del curso caen en solo 668 posiciones: 458 palabras comparten posición con otra. Con el valor por defecto, 2^18 = 262.144, solo 8 colisionan. La documentación de Spark recomienda subir la dimensión para reducir colisiones y usar una potencia de 2).
- **Tokenizer y HashingTF.** `Tokenizer(inputCol="text", outputCol="words")` parte en palabras, de forma distribuida C4P1 20:09, C4P1 22:14. `HashingTF(numFeatures=1000, inputCol=tokenizer.getOutputCol(), outputCol="features")` da un vector disperso (tamaño, posiciones, valores): "a" aparece 2 veces en la posición 467 C4P1 25:06, C4P1 27:16. **Verificado en el box:** `indexOf("a")` da 467 y el vector de "a b c d e spark a" tiene un 2.0 en la 467.
- **Entrenar y predecir.** `LogisticRegression(maxIter=10, regParam=0.001)` y `fit` C4P1 29:04; para el test hay que tokenizar y hashear otra vez a mano. Dice que dieron 1 la primera y la última cadena, las que tienen "spark" C4P1 31:17, C4P1 34:05 (**para verificar:** con los datos del repo 2019 y esos parámetros, en el box solo dio 1 la última, "spark f j k", con probabilidad 0,82; la primera, "spark i j k", dio 0,32. La diferencia probablemente viene de cambios en el notebook 2026. Además, lo que empuja a la última no es solo "spark": "f" aparece en un documento positivo del entrenamiento).
- **Pipeline.** `Pipeline(stages=[tokenizer, hashingTF, lr])` es un Estimator; `fit` con los datos crudos devuelve un `PipelineModel`, que es un Transformer con el tokenizer, el hashing y el modelo adentro C4P1 35:10, C4P1 42:32. El orden de las etapas lo define el programador C4P1 45:23. Puede tener estimadores intermedios, como StringIndexer, y Spark los ajusta C4P1 46:00. Se pueden anidar pipelines C4P1 51:16. `model.transform(test)` con el test crudo da las mismas predicciones C4P1 47:12.
- **Guardar y cargar.** `model.write().overwrite().save("/tmp/spark-model")` y `PipelineModel.load(...)`; también se puede guardar el Pipeline sin entrenar. Se guarda como un directorio con metadata y etapas C4P1 51:16. Verificado en el box: el modelo recargado da exactamente las mismas predicciones.
- **Ejercicio del notebook 06** C4P1 54:08: rehacer el ejemplo de personas con un Pipeline (VectorAssembler, StringIndexer y un clasificador a elección). Dice "predecir la edad" (**Corrección:** es el sexo, a partir de peso y altura). Avisa que StringIndexer es un estimador dentro del pipeline C4P1 55:15. Verificado en el box que un pipeline con StringIndexer como etapa intermedia funciona en Spark 3.5: el `PipelineModel` resultante contiene un `StringIndexerModel` ya ajustado.

---

## 15. Clustering
**Dónde:** C4P2 0:06, C4P2 2:21, C4P2 7:31, C4P2 11:29, C4P2 14:21, C4P2 18:16, C4P2 22:24

### Conceptos clave
- **Qué hay en Spark.** KMeans, LDA (tópicos en textos, que el docente usó en producción), BisectingKMeans, GaussianMixture y Power Iteration Clustering C4P2 0:06.
- **Datos sintéticos.** Cinco nubes de 50 puntos en 3D con distribución normal centradas en (0,0,0), (5,0,0), (0,5,0), (0,0,5) y (5,5,5); cada lista pasa a DataFrame, se unen con `union` y un VectorAssembler arma `features` C4P2 2:21, C4P2 4:08, C4P2 5:20. Gráfico 3D con plotly vía `toPandas` (con datos grandes, muestrear) C4P2 8:05.
- **KMeans.** `KMeans(k=5, featuresCol="features", predictionCol="prediction")`; `fit` es distribuido y `transform` agrega `prediction` de 0 a 4 C4P2 11:29. `model.clusterCenters()` da los centroides; para saber qué número tiene cada uno, los transforma también C4P2 14:21. Verificado en el box (con desvío 1): los cinco centroides caen a menos de 0,5 de los centros reales y los grupos tienen 48 a 52 puntos.
- **Ejercicio:** lo mismo con `BisectingKMeans` (jerárquico divisivo) C4P2 18:16. Verificado en el box que con esos datos también recupera las cinco nubes.
- **Documentación.** Distingue la guía de ML (conceptos y ejemplos) de la documentación de la API (todos los parámetros) C4P2 19:25.
- **Notebook 07.** Búsqueda de hiperparámetros (paralelizable): queda para el final si hay tiempo y no tiene ejercicio C4P2 22:24.

---

## 16. Grafos con GraphFrames
**Dónde:** C4P3 1:11, C4P3 5:11, C4P3 10:08, C4P3 11:14, C4P3 14:01, C4P3 20:15, C4P3 34:10, C4P3 41:32, C4P3 46:09, C4P3 54:03, C4P3 57:22, C4P3 1:03:11, C4P3 1:14:07, C4P3 1:24:26, C4P3 1:49:24, C4P3 1:56:22, C4P3 2:04:09

### Conceptos clave
- **Por qué grafos.** Redes sociales, difusión de enfermedades, redes semánticas ("Aristóteles nació en Grecia") C4P3 1:11. A diferencia de tablas, imágenes y texto, no tienen estructura fija y son difíciles de paralelizar C4P3 3:29.
- **GraphX vs GraphFrames.** GraphX es el oficial, sobre RDD; GraphFrames trabaja sobre DataFrames y lo hizo Databricks C4P3 5:11. No viene en la distribución estándar (en el contenedor del curso ya está cargado) C4P3 9:36. Dice que "en algún momento muy seguramente va a ser parte de Spark" C4P3 7:33 (**dudoso:** es una predicción; hoy sigue siendo un paquete aparte).
- **Qué trae.** BFS, componentes conexas y fuertemente conexas, label propagation para comunidades, PageRank, caminos más cortos y conteo de triángulos; además el patrón de pasaje y agregación de mensajes (`aggregateMessages`) y **motif finding** para consultas C4P3 10:08, C4P3 11:14.
- **Particionado.** Edge cut vs vertex cut: dice que se guarda por aristas (vertex cut) C4P3 11:14. El notebook 2019 dice lo mismo ("se almacenan con redundancia (vertex cut)").
- **Crear un grafo.** Un DataFrame de vértices con columna `id` y uno de aristas con `src` y `dst`, y `GraphFrame(v, e)`; los grafos son dirigidos C4P3 14:01, C4P3 17:25. El ejemplo chico tiene a Alice, Bob, Charlie, David, Esther, Fanny y Gabby (a..g) con relaciones friend y follow. `inDegrees`: b tiene 2 C4P3 19:06; las aristas friend son 5 C4P3 20:15. Verificado en el box: friend da 5 porque el notebook del curso agrega una arista a→h hacia un vértice que no existe (en la documentación de GraphFrames son 4); b y c tienen grado de entrada 2.
- **Gephi.** Herramienta externa de visualización (también hay versión web) C4P3 20:15. Se exportan CSV renombrando columnas (Label, Source, Target) C4P3 24:17. Spark escribe un directorio con un archivo por partición; `coalesce(1)` deja un solo archivo, peligroso con datos grandes C4P3 26:30, C4P3 28:13. En Gephi se importan vértices y después aristas con "append to existing workspace", y se acomoda con layouts como ForceAtlas, Noverlap y Expansion C4P3 29:18, C4P3 32:16.
- **PageRank.** El navegante aleatorio, iterativo, converge en unas 10 iteraciones; con MapReduce escribe a disco en cada una, con Spark queda en memoria C4P3 34:10, C4P3 37:01. `g.pageRank(resetProbability=0.15, maxIter=10)`: Bob y Charlie son los más importantes C4P3 38:08 (**verificado en el box:** b 2,70 y c 2,67, muy por encima del resto).
- **La red de retuits.** Retuits de 2017 sobre un conflicto docente en la provincia de Buenos Aires, de un trabajo con un grupo que menciona C4P3 41:32. `tweets.pqt` (Parquet) con unos 170.000 retuits C4P3 44:00. Verificado en el box: 172.040 filas, del 24 al 28 de febrero de 2017; en el archivo del repo 2019 las columnas son timestamp, user, RT_by, RT_times y text (en 2026 nombra id, timestamp, user, rt_by y text; el docente avisa que "lo cambió un poquito" C4P3 1:58:20).
- **Armar el grafo.** Aristas: `groupBy("user", "rt_by").count()`, renombrando rt_by a src y user a dst, con la flecha del que retuitea al retuiteado C4P3 46:09, C4P3 50:01. Vértices: la unión de src y dst como id, con `distinct` C4P3 51:12. Da 57.000 usuarios y 152.613 aristas C4P3 52:21 (**verificado en el box:** 57.138 vértices y 152.613 aristas). Graficar todo da una "bola de pelos" C4P3 53:30.
- **Grado.** `degrees` (entrada más salida, tomado como no dirigido); el top 10 lo encabeza un usuario con unos 2300 C4P3 54:03. Verificado en el box: el máximo es 2325.
- **Influencia colectiva (CI).** Del paper de Morone y Makse (2015, "Influence maximization in complex networks through optimal percolation") para encontrar los nodos que más viralizan C4P3 57:22. La fórmula del notebook: CI(i) = (grado(i) − 1) × Σ sobre vecinos j de (grado(j) − 1), suponiendo grafo no dirigido C4P3 1:01:22. Al dictarla dice "su propio grado multiplicado" (**Matiz:** es el grado menos uno, tanto en el notebook como en el paper, donde además es el caso de radio 1 de una familia más general, y el algoritmo completo saca iterativamente el nodo de mayor CI y recalcula).
- **Implementación con aggregateMessages.** Cada arista manda a su src el grado del dst menos 1 y a su dst el grado del src menos 1; se suman con `AM.msg`, se hace join con los grados y se multiplica C4P3 1:03:11. CI es del orden del grado al cuadrado C4P3 1:12:25. Aparece "la Belgrana" con grado 600 pero CI alta C4P3 1:13:00 (**verificado en el box:** LaBelgrana tiene grado 606 y queda octava en CI, por delante de usuarios con más del doble de grado; es el efecto de "nodo débil" del paper, un nodo de grado moderado rodeado de hubs).
- **Motif finding.** `g.find("(a)-[e]->(b); (b)-[e2]->(a)")` busca pares que se siguen mutuamente; el resultado tiene columnas struct (`b.age`) y se filtra como cualquier DataFrame, por ejemplo `b.age > 30` C4P3 1:14:07, C4P3 1:17:23, C4P3 1:21:08. Verificado en el box: en el grafo chico, b y c son el único par mutuo.
- **Subgrafo para Gephi.** Vértices con CI ≥ 29 millones o grado ≥ 600; aristas solo entre ellos con `find("(a)-[e]->(b)")` y `select("e.*")` C4P3 1:25:00, C4P3 1:27:12. Da 33 nodos y 35 aristas C4P3 1:29:23, C4P3 1:37:08 (**verificado en el box**). En Gephi, cuidado con dirigido y no dirigido ("mutual edge removed") C4P3 1:38:23; color por grado y tamaño por CI C4P3 1:42:22.
- **Ejercicio 1** C4P3 1:49:24, C4P3 1:55:18: el grafo de todas las conexiones **desde** los 8 mayores influenciadores (en 2019 eran 5), que tiene que dar 120 vértices y 122 aristas, y la imagen exportada desde la pestaña Preview de Gephi. **Verificado en el box:** las aristas que salen de los 8 de mayor CI son 122 y tocan 120 vértices, así que el número cierra con la dirección src → dst que usa en 2026 (del que retuitea al retuiteado). Ojo: el esqueleto 2019 arma el grafo con solo los top como vértices, y así `find` devolvería apenas las aristas entre ellos (9 para el top 8), no 122.
- **Ejercicio 2** C4P3 1:56:22, C4P3 1:59:03: triángulos dirigidos A→B→C→A con tres usuarios distintos (hay que descartar los "triángulos colapsados" con usuarios repetidos), graficados en Gephi. Dice que tiene que dar "415 vértices y 100 aristas" (**Corrección probable, verificada en el box:** los triángulos con tres usuarios distintos tocan 415 vértices y 1006 aristas distintas; un grafo hecho de triángulos no puede tener menos aristas que vértices, así que el "100" es casi seguro "1006" cortado por la transcripción o el dictado).
- **Dask vs Spark** (opinión del docente): Dask es menos maduro, un "parche" sobre pandas, bueno para problemas chicos o académicos; MPI sirve para HPC pero sin tolerancia a fallas; hay que elegir la herramienta según el contexto C4P3 2:04:09.

---

## Correcciones y matices

| Tema | Qué se dijo | Qué corresponde | Tipo |
|---|---|---|---|
| Tamaño de flights.csv | "unos 10000" C2P1 1:46:06, y "10.000" al releer el ORC C3P1 1:14:12 | 100.000 filas, como dice en C2P3 5:29 | Corrección, verificado en el box |
| PolynomialExpansion | "no es un transformer" C3P3 22:05 | Es un Transformer (no tiene `fit`), igual que VectorAssembler | Corrección, verificado en el box |
| Features de grado 4 | "12" C3P3 25:28 | Con 2 variables: grado 2 da 5, grado 3 da 9, grado 4 da 14 | Corrección, verificado en el box |
| Ejercicio del notebook 06 | "predecir la edad" C4P1 54:08 | Es el sexo a partir de peso y altura | Corrección |
| Triángulos del ejercicio 2 | "415 vértices y 100 aristas" C4P3 1:59:03 | 415 vértices y 1006 aristas | Corrección probable, verificado en el box |
| Paper de Spark | "es del 2009" C1P1 2:00:14 | El proyecto arranca en 2009; el primer paper es de HotCloud 2010 | Corrección |
| SAOCOM | radar de "banda ancha" C1P1 22:18 | SAR de banda L (1,275 GHz), según CONAE | Corrección |
| Hive y Redshift | "Hive es el equivalente a Amazon Redshift pero libre" C1P1 1:37:05 | Redshift es un data warehouse columnar MPP; lo más parecido a Hive en AWS es Hive sobre EMR o Athena | Corrección |
| Fórmula de CI | "su propio grado multiplicado" C4P3 1:01:22 | (grado − 1) × Σ (grado del vecino − 1) | Matiz |
| Hadoop y Python | "no se puede en Python" C1P2 24:18 | Hadoop Streaming acepta Python | Matiz |
| Dos filter | Spark "quizás" los fusiona C2P1 1:25:00 | En RDD se encadenan en la misma etapa; en DataFrames Catalyst los combina en un solo Filter | Matiz, verificado en el box |
| Recalcular sin cache | "computacionalmente imposible darse cuenta, está demostrado" C2P1 1:39:02 | La documentación lo presenta como decisión de diseño | dudoso |
| Colisiones de hashing | "muy raro" C4P1 18:27 | Con 1000 posiciones y 1126 palabras, 458 colisionan; con 2^18, 8 | Matiz, verificado en el box |
| Predicciones del ejemplo de texto | dieron 1 la primera y la última C4P1 34:05 | Con los datos 2019 solo la última da 1 (0,82); la primera da 0,32 | para verificar |
| inferSchema y "NA" | (no lo menciona para DataFrames) | Sin `nullValue="NA"`, DepDelay, ArrDelay y AirTime quedan como string y una UDF que compara números falla | Matiz, verificado en el box |
| Archivos de Parquet | uno por tarea C2P2 51:09 | Uno por partición del DataFrame; con 992 filas sale uno solo | Matiz, verificado en el box |
| `sqlContext.table` | C3P1 1:27:01 | En Spark 3, `spark.table` | Matiz |
| Spark en una máquina vs scikit-learn | a veces le gana C2P1 34:25 | Depende del tamaño: con datos chicos domina el costo de la JVM y la serialización | Matiz |
| S3 como filer | C1P1 47:19 | S3 es almacenamiento de objetos | Matiz |
| Docker en Windows | necesita WSL2 C1P1 2:13:13 | Hay contenedores Windows nativos; las imágenes Linux necesitan WSL2 o Hyper-V | Matiz |
| Ley de Moore | "60% por año", doble cada 18 meses C1P1 55:33 | Moore habló de transistores, duplicándose cada 2 años en su versión de 1975; los 18 meses son una reformulación posterior | Matiz |
| Boosting en datos tabulares | le gana a las redes C3P3 2:15 | Es lo que muestran varios benchmarks, no una ley | Matiz |
| GraphFrames dentro de Spark | "muy seguramente" va a ser parte C4P3 7:33 | Predicción; hoy es un paquete aparte | dudoso |
| Grafos en el programa | (se dan en la clase 4) | La página oficial no lista grafos entre los módulos | Matiz |
| Red de "50 GB/s" | "la red no supera 50 GB/s desde hace 10 años" C1P1 54:26 | Hay Ethernet de 400 y 800 Gb/s; no queda claro qué quiso decir | dudoso |
| Boeing 787 | 500 GB por vuelo C1P1 17:16 | No lo chequeé | para verificar |
| CERN | "un PB por segundo" C1P1 18:28 y después "un PB por día" C1P1 36:21 | Se contradice; el orden de PB por segundo es lo que generan los detectores antes del filtrado | para verificar |
| Netflix | 15% del tráfico de internet en 2022 C1P1 21:07 | No lo chequeé | para verificar |
| SAOCOM | 100 TB por año C1P1 22:18 | No lo chequeé | para verificar |
| Event Horizon Telescope | 350 TB por día por telescopio C1P1 26:19 | No lo chequeé | para verificar |
| Bajar 1 YB a 1 GB/s | 253 millones de años C1P1 37:33 | 10^24 / 10^9 = 10^15 s, unos 31,7 millones de años; ni con unidades binarias llega a 253 | para verificar (la cuenta da otra cosa) |
| IDC DataSphere | 33, 149, 181 y 394 ZB C1P1 40:29 | Pronósticos de IDC (estudios patrocinados por Seagate) | para verificar |
| MapReduce y disco | "90% del tiempo en E/S de disco" C1P1 1:55:15 | Sin fuente | para verificar |
| Clientes de Databricks | Heineken, Mercedes, Santander, Toyota, Pepsi C4P3 8:07 | No lo chequeé | para verificar |
| Spark 3.5.9 | versión del contenedor C1P2 57:00 | PySpark 3.5.9 existe en PyPI y es la que usé en el box | verificado en el box |

---

## Preguntas de repaso

1. ¿Por qué la materia insiste en que el problema es mover los datos y no guardarlos? Relacionalo con las leyes de Moore, Kryder y Nielsen.
2. ¿Qué tres desventajas tiene MPI para big data según el docente?
3. Describí las fases de MapReduce con el word count. ¿Cuál es la más cara y por qué?
4. ¿Por qué MapReduce es malo para PageRank y cómo lo resuelve Spark?
5. ¿Qué diferencia hay entre una imagen y un contenedor de Docker? ¿Qué pasa con tus archivos si no usás `-v`?
6. En el word count de PySpark, ¿qué hace el `filter(lambda w: w)` y por qué funciona?
7. ¿Qué diferencia hay entre una transformación y una acción? Dá tres ejemplos de cada una.
8. ¿Por qué `take(1)` usa menos tareas que `collect()`?
9. ¿Qué es una etapa y qué la corta?
10. Con `sq = sc.parallelize(range(30)).map(lambda x: x*x)`, ¿cuántas veces se calculan los cuadrados si hacés `sq.mean()` y `sq.collect()`? ¿Y con `sq.cache()`?
11. ¿Qué devuelve `printSchema()` para la columna age de `userid-profile.tsv` con y sin `inferSchema`?
12. Escribí el conteo de usuarios por país en SQL y con la API de DataFrames.
13. ¿Por qué hay que declarar el tipo de retorno de una UDF en PySpark? ¿Qué se pierde al usar una UDF?
14. Si leés `flights.csv` con `inferSchema` y sin `nullValue`, ¿de qué tipo queda DepDelay y qué problema trae?
15. ¿Qué diferencia hay entre `createOrReplaceTempView` y `saveAsTable`? ¿Cuál sobrevive a un reinicio de Spark?
16. ¿Qué hace `broadcast()` en un join y cuándo conviene?
17. ¿Qué es un Estimator y qué es un Transformer? Clasificá VectorAssembler, StringIndexer, StringIndexerModel, DecisionTreeClassifier y PolynomialExpansion.
18. ¿Por qué el notebook hace `repartition(sc.defaultParallelism)` al leer el JSON de personas?
19. ¿Por qué la frontera de un árbol de decisión es escalonada y la de la regresión logística es recta?
20. ¿Cuántas features da PolynomialExpansion de grado 3 sobre dos variables? ¿Por qué ayuda a un clasificador lineal?
21. ¿Qué ventaja tiene el hashing trick sobre la bolsa de palabras con vocabulario, y cuál es su costo?
22. ¿Qué devuelve `Pipeline.fit` y qué se puede meter dentro de un Pipeline?
23. ¿Qué columnas obligatorias necesita GraphFrames en vértices y aristas?
24. Escribí la fórmula de influencia colectiva y explicá cómo se calcula con `aggregateMessages`.
25. ¿Por qué un nodo como LaBelgrana puede tener CI alta con grado moderado?
26. ¿Qué expresión de motif finding usarías para encontrar triángulos dirigidos, y cómo descartás los colapsados?

---

## Glosario de nombres deformados

| En la transcripción | Es |
|---|---|
| CPELI, Cepelin, seppeling, Zpelin | Zeppelin |
| Bitbacker, Bitbacket | Bitbucket |
| Secad, SC, SK, Cad | CCAD (Centro de Computación de Alto Desempeño, UNC) |
| Júpiter Hub | JupyterHub |
| home hobian | /home/jovyan |
| RMIDMI, ritme, remi | README |
| Hitcron, Gitclon | git clone |
| escala | Scala |
| Persico | PepsiCo |
| Databicks, Databaks, Data Brix | Databricks |
| Lakheo | lakehouse |
| SACOM | SAOCOM |
| y decor | IDECOR |
| ley de Creer | ley de Kryder |
| Yamu | YARN |
| cubernet, SCM | Kubernetes |
| Sparcore | Spark Core |
| Sparque SQL | Spark SQL |
| spack submit | spark-submit |
| P for J | Py4J |
| Parket York | Parquet, ORC |
| deion 3 | decision tree |
| stream indexer | StringIndexer |
| Logite Ration, logity Regresión | logistic regression |
| Supervector, suport vector machine | support vector machine (SVM) |
| polinum en espacio | PolynomialExpansion |
| has intf, casing TF, cashing TF | HashingTF |
| has 3 | — |
| fichurizador, faturizar | featurizador, featurizar |
| Camins, comins | KMeans |
| bisecting comins | BisectingKMeans |
| graf X | GraphX |
| Gepi, GPI, GEPI | Gephi |
| P rank | PageRank |
| agre message | aggregateMessages |
| motive finding, multi finding, mtifinding | motif finding |
| Dusk, Task | Dask |
