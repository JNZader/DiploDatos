# Segunda parte: "Programación Distribuida sobre Grandes Volúmenes de Datos", con material externo

**Esta es la continuación de** `programacion-distribuida-grandes-volumenes-apunte-de-estudio.md` y `programacion-distribuida-grandes-volumenes-guia-de-implementacion.md` (las clases de Programación Distribuida sobre Grandes Volúmenes de Datos, materia optativa de la Diplomatura en Ciencia de Datos de FAMAF UNC, cohorte 2026, dictadas por Damián Barsotti en cuatro encuentros: 25 y 26 de septiembre y 2 y 3 de octubre de 2026). Esos archivos resumen lo que dice la materia. Esta segunda parte suma material externo para verificar lo que en el apunte quedó "para verificar" o "dudoso", respaldar con fuentes las correcciones que ya marqué, corregir errores míos de la primera parte (incluida la revisión línea por línea de las marcas de tiempo del apunte, que no había hecho), sumar bibliografía y discutir el enfoque de la materia (Spark como herramienta por defecto para datos que "no entran en una computadora") contra la alternativa más fuerte, con un benchmark real sobre los datasets del curso. Revisé todo el 07/10/2026 y solo cito páginas que abrí (las que solo vi en un buscador las marco así). Conflictos de interés: los marco donde aparecen; los más importantes son **Databricks** (la empresa de los creadores de Spark: vende Spark administrado, regala *Learning Spark*, es la autora de Delta Lake y de GraphFrames y publica los casos de clientes que cito), **MotherDuck** (vende DuckDB en la nube y es la autora de "Big Data is Dead"), **Google** (autor del caso del Event Horizon Telescope y del blog de Mercado Libre, que cuentan cómo usan sus productos), **Seagate** (patrocina el estudio de IDC sobre el volumen de datos del mundo y vende discos) y **Sandvine** (vende gestión de tráfico y publica el informe de Netflix). Los autores de DuckDB, Polars, Dask y Ray, cuya documentación cito, también tienen empresas que venden servicios sobre esas herramientas.

> Cómo leer esto: cuando digo "la materia" o "el docente" me refiero a lo que dice Damián en las clases. Las marcas de tiempo usan la etiqueta de cada grabación del apunte (C1P1 es la clase 1, parte 1, y así hasta C4P3) y llevan al minuto exacto en la grabación. Cuando digo "sugerencia" es una idea mía que combina fuentes, no algo que diga una fuente puntual. Como pidió el docente, acá **no hay soluciones** de los ejercicios de los notebooks que se entregan: el benchmark usa las consultas de los ejemplos resueltos en clase (vuelos y red de retuits), no las de los ejercicios. Corrí el benchmark en el box el 07/10/2026 con dos entornos aparte: Spark en el de la guía (`pd_venv`: Python 3.13, PySpark 3.5.9, Java 17 Temurin; no pude confirmar qué versión trae el contenedor del curso, ver sección 11) y los motores de una sola máquina en uno nuevo (`bench_pd_venv`: DuckDB 1.5.6, Polars 2.0.0, pandas 3.0.6, pyarrow). El box tiene 8 núcleos y 15 GB de RAM (unos 7 GB libres al empezar). Spark corrió en `local[*]` con 4 GB para el driver y la configuración por defecto (AQE prendido, 200 particiones de shuffle). Los datos son `flights.csv` (100.000 filas) y `twitter-out` de la carpeta `ds/` del repositorio público 2019 de la materia, más copias agrandadas 10 y 100 veces. Los tiempos son de una sola corrida de cada configuración repetida dos veces (me quedo con la mejor), con el box compartido con otros trabajos, así que tomalos como órdenes de magnitud.

---

## Checklist actualizado (curso + mejoras)

1. Antes de levantar un clúster, medí tus datos **en Parquet y en memoria**, no en CSV. Los vuelos ×100 (10 millones de filas) son 926 MB en CSV y 147 MB en Parquet; en una sola máquina, DuckDB los carga en 1 s y responde cada consulta de la clase en menos de 0,1 s (sección 5).
2. Usá Spark cuando los datos o el cómputo **de verdad** no entran en una máquina, o cuando ya tenés el clúster, el lakehouse o el equipo armado. En `local[*]` y con estos tamaños, Spark fue entre 8 y 90 veces más lento que DuckDB por consulta y tardó de 12 a 50 s por proceso contra 0,4 a 5 s; con datos chicos usó de 3 a 6 veces más memoria (secciones 5 a 7). La propia materia lo dice al revés: "si entra en una computadora, scikit-learn" C1P1 42:16.
3. Si vas a usar Spark para trabajos iterativos (PageRank, entrenamiento, un DataFrame que consultás muchas veces), hacé `cache()` o `persist()` **vos**: Spark no lo decide solo. La documentación dice que cada RDD transformado "puede recalcularse cada vez que corrés una acción sobre él" (sección 3.1).
4. Ese costo de recalcular y escribir a disco es exactamente el que motivó Spark: Zaharia y otros midieron que en Hadoop la replicación, la E/S de disco y la serialización se llevaban "más del 90% del tiempo de ejecución" de algoritmos de aprendizaje automático iterativos (sección 1).
5. En los joins con una tabla chica, Spark ya hace broadcast solo cuando la tabla mide menos de 10 MB (`spark.sql.autoBroadcastJoinThreshold`); el `broadcast()` explícito de la clase sirve cuando Spark no puede estimar el tamaño. AQE viene prendido desde Spark 3.2 y reajusta el plan en mitad de la ejecución.
6. Con `HashingTF`, usá una potencia de dos como `numFeatures` (la documentación lo recomienda) y no bajes de las 2^18 posiciones por defecto sin medir colisiones: con 1000 posiciones, en el ejemplo de clase colisionaban 458 de 1126 palabras.
7. `PolynomialExpansion` es un **Transformer** (no tiene `fit`) y `StringIndexer` es un **Estimator** (necesita `fit`). Con dos variables, grado 4 da 14 columnas, no 12.
8. Si usás Python 3.12 o más nuevo con PySpark 3.5, instalá `setuptools` en el entorno: Python sacó `distutils` en la 3.12 y Spark recién dejó de usarlo en la 4.0 (SPARK-45390).
9. Si arrancás un proyecto nuevo hoy, mirá Spark 4.x (la última es la 4.2.0, de julio de 2026): ANSI SQL por defecto, Java 17 por defecto, Python 3.8 afuera y Spark Connect, que permite un cliente liviano de Python separado del clúster. Lo que aprendés en la materia con Spark 3 sigue valiendo casi todo.
10. Para grafos, GraphFrames sigue siendo un paquete aparte de Spark (ahora mantenido por la comunidad en `io.graphframes`, con soporte para Spark 4 y Spark Connect desde la 0.9.2). GraphX no recibe trabajo nuevo y su futuro se discutió en la comunidad de Spark en 2024.
11. Para tablas que se actualizan (insertar, borrar, versiones), guardá en Delta Lake o Iceberg sobre Parquet en lugar de Parquet suelto: suman transacciones ACID y metadatos escalables.
12. Para datos que entran en memoria en una máquina, DuckDB (SQL) o Polars (DataFrames) son la opción por defecto razonable; pandas sirve hasta unos pocos GB pero con CSV grandes se come la RAM (7,9 GB de pico para un CSV de 926 MB en el benchmark).
13. Si vas a medir "Spark contra otra cosa", aplicá la métrica COST de McSherry: compará contra una buena implementación en **un solo hilo**, no solo contra Spark con menos máquinas.
14. Cuando cites cifras del tamaño del mundo digital (ZB de IDC, PB del CERN, GB por vuelo), aclará de qué etapa hablás: generado, filtrado, guardado o transmitido. Las cifras de la clase son correctas o casi, pero mezclan etapas (sección 1).
15. Revisá en el aula virtual las fechas de entrega de los notebooks: no figuran en ninguna página pública.

## Versión completa

### 1. Los datos de la clase, verificados

| Afirmación | Resultado | Matiz | Fuente |
|---|---|---|---|
| Un Boeing 787 "genera 500 GB por vuelo" C1P1 17:16 | Dudoso o exagerado | La cifra circula desde 2013 en notas de prensa sin fuente primaria. Boeing, en una presentación propia para IATA de 2017, dice que "1 año de mediciones de sensores del 787 de un avión es ~1 TB". La diferencia depende de qué se cuente (sensores registrados contra todos los datos del avión), pero la cifra oficial de Boeing es unas 100 veces menor por vuelo | [Boeing para IATA, 2017 (PDF)](https://www.iata.org/contentassets/af577ffae2714e859202927be50afbea/1000-1030-tackling-data-analytics-dilemma-boeing.pdf); [Ubergizmo, 2013](https://www.ubergizmo.com/2013/03/boeing-787-conjures-more-than-500gb-of-data-per-flight/) |
| El CERN "genera alrededor de un petabyte por segundo" C1P1 18:28, y después "lo que el CERN tiene archivado" es "alrededor de un exabyte" C1P1 36:21 | Sí, las dos, en etapas distintas | Los detectores del LHC producen del orden de 1 PB/s de datos de colisiones **antes** de los filtros (triggers); después del filtrado, el centro de datos procesó del orden de 1 PB por día en la Run 2. El CERN anunció el 29/09/2023 que su capacidad de disco pasó 1 EB (un millón de TB, en 111.000 dispositivos); es capacidad lista para datos, no exactamente "lo archivado", pero el orden de magnitud es el de la clase. En el apunte dije que se contradecía: no, habla de cosas distintas (corrijo en la sección 11). Las diapositivas de 2019 decían "40 TB/seg en 2012" | [CERN, Storage](https://home.cern/science/computing/storage); [CERN, "An exabyte of disk storage at CERN"](https://home.cern/news/news/computing/exabyte-disk-storage-cern) |
| Netflix es el 15% del tráfico de internet en 2022 C1P1 20:07 | Sí | El informe de Sandvine de enero de 2023 da 14,93% del tráfico de bajada y 13,74% del volumen total en 2022 (conflicto de interés: Sandvine vende gestión de tráfico) | [Sandvine, Global Internet Phenomena Report 2023 (PDF)](https://www.sandvine.com/hubfs/Sandvine_Redesign_2019/Downloads/2023/reports/Sandvine%20GIPR%202023.pdf) |
| SAOCOM 1A y 1B, radar, unos 100 TB por año C1P1 22:18 | En parte | CONAE confirma radar de apertura sintética en banda L (1,275 GHz), revisita de 16 días por satélite y 8 con los dos. La cifra de 100 TB por año no la encontré en ninguna fuente oficial: queda sin verificar | [CONAE, SAOCOM, características técnicas](https://www.argentina.gob.ar/ciencia/conae/misiones-espaciales/saocom) |
| El Event Horizon Telescope: 350 TB por día por telescopio, discos en avión C1P1 31:19, 5 PB C1P1 33:00, "media tonelada" de discos C1P1 32:27 | Sí | El caso de Google dice 350 TB por día por telescopio, media tonelada de discos con helio y 5 PB (conflicto de interés: es un caso de Google). La FAQ del EHT da unos 3,5 PB crudos en abril de 2017 y 5,5 PB en 2018, y explica que los discos viajan en avión porque por internet tardaría demasiado. El comunicado de prensa original no cargó (403), y al volver a abrir la FAQ para revisar el enlace también dio 403 | [EHT, FAQ](https://eventhorizontelescope.org/faq/how-much-data-recorded-during-observation-and-how-it-transferred-central-processing); [Google for Education, caso del EHT](https://edu.google.com/intl/ALL_us/resources/customer-stories/eht-gcp/) |
| IDC: 33 ZB en 2018, 149 ZB en 2024, 181 ZB en 2025 y 394 ZB en 2028 C1P1 40:29, y "el mundo genera 181 ZB en el 2025" C1P1 36:21 | En parte | El estudio IDC y Seagate "Data Age 2025" (2018, patrocinado por Seagate) pronosticaba de 33 ZB en 2018 a 175 ZB en 2025. Los 149 y 181 ZB son de Statista, que vi citados en Rivery (fuente secundaria). Los 394 ZB para 2028 solo los vi en el buscador. Dos matices: la "DataSphere" cuenta datos creados, capturados, replicados **y consumidos**, no guardados; y los 181 ZB de 2025 también son una estimación, así que comparar "pronóstico contra real" es comparar dos pronósticos | [IDC y Seagate, Data Age 2025 (PDF)](https://www.seagate.com/files/www-content/our-story/trends/files/idc-seagate-dataage-whitepaper.pdf); [Rivery, citando a Statista](https://rivery.io/blog/big-data-statistics-how-much-data-is-there-in-the-world/) |
| Bajar 1 YB a "1 GB por segundo" tarda 253 millones de años C1P1 37:33 | Sí, a 1 gigabit por segundo | 10^24 bytes × 8 bits / 10^9 bits por segundo = 8 × 10^15 s, unos 253,5 millones de años. A 1 gigabyte por segundo serían 31,7 millones. La cuenta de la clase está bien si "GB" quiere decir gigabit; en el apunte la marqué mal como errónea (corrijo en la sección 11). Las diapositivas de 2019 dicen otra cosa: "11.000.000.000.000 años", citando una charla de Esteban Feuerstein de 2014 | Cuenta propia; diapositivas 2019 del repositorio de la materia |
| En MapReduce, PageRank pasa "el 90% del tiempo" haciendo E/S de disco C1P1 1:55:15 | Sí, con matices | Zaharia y otros (en *;login:*, la revista de USENIX) escriben que la replicación de datos, la E/S de disco y la serialización "podían llevarse más del 90% del tiempo de ejecución de algoritmos comunes de aprendizaje automático implementados en Hadoop". Es para trabajos iterativos y de varias pasadas, no para MapReduce en general | [Zaharia y otros, "Fast and Interactive Analytics over Hadoop Data with Spark", ;login: (PDF)](https://www.usenix.org/system/files/login/articles/zaharia.pdf) |
| Google "inventa MapReduce para hacer" PageRank C1P1 1:55:15 | Dudoso | El paper de MapReduce (Dean y Ghemawat, OSDI 2004) no menciona PageRank: cuenta que lo usaron para reescribir "nuestro sistema de indexación de producción", el que produce las estructuras de datos de la búsqueda web. PageRank es anterior (1998) y es parte de esa búsqueda, así que la relación existe, pero "lo inventaron para PageRank" no está en la fuente | [Dean y Ghemawat 2004 (PDF)](https://static.googleusercontent.com/media/research.google.com/es//archive/mapreduce-osdi04.pdf) |
| "El paper de Spark es del 2009" C1P1 2:00:14 | Ya corregido | El primer paper es "Spark: Cluster Computing with Working Sets" (Zaharia, Chowdhury, Franklin, Shenker y Stoica, HotCloud 2010): Spark "puede superar a Hadoop por 10x en trabajos iterativos de aprendizaje automático" y consultar 39 GB de forma interactiva. El de los RDD es de NSDI 2012 ("Resilient Distributed Datasets"): "hasta 20× más rápido que Hadoop para aplicaciones iterativas" | [HotCloud 2010 (PDF)](https://www.usenix.org/legacy/event/hotcloud10/tech/full_papers/Zaharia.pdf); [NSDI 2012 (PDF)](https://www.usenix.org/system/files/conference/nsdi12/nsdi12-final138.pdf) |
| Clientes de Databricks: Heineken, Mercedes, Santander, Toyota, Pepsi y otros dos que el subtítulo da como "Mitely" y "Simel" C4P3 8:07 | Sí, los cinco que se entienden | Abrí las páginas de clientes de Databricks de Santander (más de 4000 usuarios, ingesta de 71 días a horas), Heineken y Mercedes-Benz Tech Innovation (consultas de 192 horas a 90 minutos), y el blog de PepsiCo (6 PB, Unity Catalog, Azure). Toyota figura en un comunicado de enero de 2026 que solo vi en el buscador. Conflicto de interés: todo esto lo publica Databricks. "Mitely" y "Simel" no los pude resolver | [Databricks, Santander](https://www.databricks.com/customers/santander); [Heineken](https://www.databricks.com/customers/heineken-international); [Mercedes-Benz](https://www.databricks.com/customers/mercedes-benz); [PepsiCo](https://www.databricks.com/blog/how-pepsico-established-enterprise-grade-data-intelligence-platform-powered-databricks-unity) |
| Es "computacionalmente imposible" que Spark sepa si dos acciones van a reusar el mismo RDD, "está demostrado" C2P1 1:39:02 | Correcto en espíritu (no es CAP ni FLP) | El resultado que encaja es el **teorema de Rice**: toda propiedad semántica no trivial de los programas es indecidible, y "este programa del driver va a volver a usar este RDD" es una. Además, en uso interactivo el código futuro todavía no existe. Pero Spark tampoco intenta los casos fáciles: la documentación lo plantea como diseño ("cada RDD transformado puede recalcularse cada vez que corrés una acción sobre él") y deja el `cache()` al usuario. CAP (consistencia y disponibilidad ante particiones de red) y FLP (consenso con fallas) hablan de otra cosa | [Spark, RDD Programming Guide](https://spark.apache.org/docs/latest/rdd-programming-guide.html); [Wikipedia, teorema de Rice](https://en.wikipedia.org/wiki/Rice%27s_theorem) |
| GraphFrames "en algún momento muy seguramente va a ser parte de Spark" C4P3 7:33 | Sigue dudoso, con movimiento | La propuesta de grafos con Cypher dentro de Spark (SPIP SPARK-25994) se revirtió antes de Spark 3.0 ("no parece que se vaya a agregar contenido", PR #26928, diciembre de 2019). En septiembre de 2024 Holden Karau abrió una votación para deprecar GraphX en Spark 4; el informe de Spark al directorio de Apache del 20/11/2024 dice que la comunidad discute "deprecar GraphX o traer el proyecto externo GraphFrames a Apache Spark". El blog de GraphFrames de agosto de 2025 dice que la inclusión "se debate activamente" y que GraphX ya está deprecado en Spark (la guía de GraphX de Spark 4.0 y 4.2 no muestra ningún aviso). Hoy GraphFrames es un paquete aparte | [PR #26928](https://github.com/apache/spark/pull/26928); [votación en la lista dev](https://www.mail-archive.com/dev@spark.apache.org/msg32370.html); [actas del directorio de Apache, Spark](https://whimsy.apache.org/board/minutes/Spark.html); [GraphFrames, "GraphFrames is back!"](https://graphframes.io/05-blog/1000-graphframes-is-back.html) |
| Un protocolo de red "no supera los 50 GB por segundo desde hace ya muchos años" C1P1 54:26 | Falso como cifra, cierto como tendencia | Ethernet de 400 Gb/s existe desde 2017 y la IEEE 802.3df empezó en 2022 a estandarizar 800 Gb/s y 1,6 Tb/s (el 1,6 T pasó a 802.3dj, con cierre previsto en julio de 2026). Lo que sí se sostiene es la idea de fondo: Nielsen estima que el ancho de banda de un usuario de punta crece un 50% por año, menos que el cómputo | [Wikipedia, Terabit Ethernet](https://en.wikipedia.org/wiki/Terabit_Ethernet); [Nielsen, "Law of Internet Bandwidth"](https://www.nngroup.com/articles/law-of-bandwidth/) |
| La ley de Moore: "crece un 60% cada año" C1P1 55:33 | En parte | Moore (1965) habló de duplicar componentes por año y en 1975 corrigió a cada dos años (41% anual). Los 18 meses vienen de David House, de Intel, que habló de rendimiento | [Wikipedia, Moore's law](https://en.wikipedia.org/wiki/Moore%27s_law) |
| Python 3.13 y `distutils` (tropiezo de mi guía) | Sí, y explicado | SPARK-45390 ("Remove distutils usage"): PEP 632 deprecó `distutils` en Python 3.10 y lo sacó en la 3.12; Spark lo arregló en la 4.0.0. Las notas de Spark 4.0 suman soporte de Python 3.13 en Spark Connect. Con PySpark 3.5 y Python 3.12 o 3.13 hay que instalar `setuptools` | [SPARK-45390](https://issues.apache.org/jira/browse/SPARK-45390); [notas de Spark 4.0.0](https://spark.apache.org/releases/spark-release-4-0-0.html) |

### 2. Nombres y dudas que quedaron

- **"Mitely" y "Simel"** C4P3 8:07: son dos clientes de Databricks que el subtítulo automático no entendió. No los resolví; cualquier nombre que ponga sería adivinar.
- **"el Vido"** C4P3 8:07: tampoco lo pude resolver.
- **SAOCOM**: el subtítulo dice "banda ancha"; es **banda L**, según CONAE (ya estaba corregido en el apunte).
- **"Learning Spark"**: el docente avisa que los libros de la presentación están "viejitos" C2P1 15:25. La segunda edición (Damji, Wenig, Das y Lee, O'Reilly, 2020, cubre Spark 3.0) la regaló Databricks; el repositorio oficial con el código es `databricks/LearningSparkV2`. La página de descarga de Databricks solo la vi en el buscador (la que probé dio 404).
- **Dask** C4P3 2:04:09: el docente lo describe como "parche" sobre pandas. La documentación de Dask lo presenta como biblioteca de Python para cómputo paralelo y distribuido, con DataFrames que paralelizan pandas, ejecución más grande que la memoria en una máquina y cómputo distribuido "para datasets de terabytes". Es una opinión del docente, no un error, pero conviene saber que Dask apunta también a clústeres.

### 3. Las correcciones de la clase, con fuentes

#### 3.1. Evaluación perezosa y cache: Spark no adivina

**Qué dice la fuente.** El docente muestra que `sq.mean()` y `sq.collect()` calculan los cuadrados dos veces C2P1 1:33:17 y que la solución es `cache()`, porque Spark no puede saber solo que vas a reusar el RDD C2P1 1:39:02.

**Qué suma el material externo.** La guía de programación de RDD lo dice con todas las letras: "Por defecto, cada RDD transformado puede recalcularse cada vez que corrés una acción sobre él. Pero también podés persistir un RDD en memoria con `persist` (o `cache`)". El paper de NSDI 2012 lo presenta como diseño desde el origen: el usuario indica qué RDD va a reusar y con qué estrategia de almacenamiento. Sobre "está demostrado": como expliqué en la tabla de la sección 1, el resultado que encaja es el teorema de Rice, no CAP ni FLP.

**Cómo implementarlo.** En un notebook, poné `cache()` al DataFrame o RDD que vas a consultar más de una vez, contalo una vez (`count()`) para materializarlo, y `unpersist()` cuando terminás. En el benchmark (sección 4) Spark solo es competitivo en la segunda y tercera consulta gracias a eso: el tiempo de "carga" de Spark incluye `cache()` y `count()`.

#### 3.2. PolynomialExpansion es un Transformer y grado 4 da 14 columnas

**Qué dice la fuente.** "No es un transformer" C3P3 22:05 y "12" columnas con grado 4 C3P3 25:28.

**Qué suma el material externo.** La referencia de PySpark define `class pyspark.ml.feature.PolynomialExpansion(*, degree=2, inputCol=None, outputCol=None)`, sin `fit`, y da el ejemplo: con `(x, y)` y grado 2 sale `(x, x*x, y, x*y, y*y)`, cinco columnas. La cuenta general es C(n + d, d) − 1 (todos los monomios de grado 1 a d con n variables, sin la constante): con n = 2 y d = 4 da 15 − 1 = 14. Ya lo había verificado en el box.

**Cómo implementarlo.** Usalo directo con `transform`; si lo ponés en un `Pipeline` no necesita `fit` propio. Mirá el tamaño antes de subir el grado: con 10 variables y grado 4 son 1000 columnas.

#### 3.3. StringIndexer es un Estimator

**Qué suma el material externo.** La referencia de PySpark lo describe como "un indexador de etiquetas que mapea una columna de texto a índices"; el orden por defecto es `frequencyDesc` (la categoría más frecuente recibe el 0) y el ejemplo oficial hace `fit` y después `transform` con `stringOrderType="alphabetDesc"`, igual que en clase C3P2 37:21.

**Cómo implementarlo.** Si querés que el 1 sea una clase concreta (por ejemplo "masculino"), fijá `stringOrderType` explícitamente: con `frequencyDesc` el índice cambia si cambian las proporciones de los datos.

#### 3.4. Colisiones de HashingTF

**Qué dice la fuente.** Las colisiones son "muy raras" C4P1 18:27.

**Qué suma el material externo.** La guía de features de Spark recomienda usar "una potencia de dos como dimensión, si no las features no se reparten parejo" y fija por defecto 2^18 = 262.144 posiciones. Con eso, en el ejemplo de clase, colisionaban 8 de 1126 palabras; con las 1000 posiciones del notebook, 458 (lo medí en la primera parte).

**Cómo implementarlo.** Dejá el valor por defecto o una potencia de dos grande; si necesitás saber qué palabra es cada columna, usá `CountVectorizer`, que guarda el vocabulario.

#### 3.5. El grafo de juguete de GraphFrames

**Qué suma el material externo.** La guía de usuario de GraphFrames arma el mismo grafo de Alice a Gabby con 8 aristas, de las cuales 4 son `friend`. En clase dio 5 C4P3 20:15 porque el notebook del curso agrega una arista (ya lo había verificado en el box). La guía de motif finding trae el patrón `(a)-[e1]->(b); (b)-[e2]->(a)` para pares mutuos, que es el que se ve en clase C4P3 1:17:23.

#### 3.6. Influencia colectiva: el paper existe

**Qué suma el material externo.** Morone y Makse, "Influence maximization in complex networks through optimal percolation", *Nature* 524, 65 a 68, publicado el 01/07/2015 C4P3 57:22. El resumen dice que el conjunto óptimo de influenciadores es "mucho más chico" que el que predicen las centralidades heurísticas y que aparecen muchos nodos de grado bajo rodeados de hubs. El texto completo es pago, así que no pude comparar la fórmula del notebook con la del paper.

#### 3.7. Hive y Redshift: menos error del que marqué

**Qué dice la fuente.** "Hive es el equivalente a Amazon Redshift pero libre" C1P1 1:37:05.

**Qué suma el material externo.** La página de Hive lo define como "un sistema de data warehouse distribuido y tolerante a fallas" que maneja "petabytes de datos en almacenamiento distribuido usando SQL". AWS define Redshift como "un data warehouse administrado, de escala de petabytes, en la nube". Como **función** (SQL sobre muchos datos para análisis), la comparación del docente es razonable. La diferencia es de arquitectura: Redshift guarda los datos en su propio formato columnar; Hive consulta archivos en almacenamiento distribuido, igual que Athena, que AWS define como un servicio de consultas interactivas con SQL "directamente sobre Amazon S3". En el apunte lo marqué como "Corrección"; es un "Matiz" (lo corrijo en la sección 11).

#### 3.8. Hadoop sí acepta Python

**Qué suma el material externo.** La documentación de Hadoop Streaming dice que permite "crear y correr trabajos de Map/Reduce con cualquier ejecutable o script como mapper o reducer" y trae un ejemplo con `myPythonScript.py`. Lo que es cierto es que la API nativa de Hadoop es Java C1P2 24:18.

#### 3.9. `spark.table` en lugar de `sqlContext.table`

**Qué suma el material externo.** La referencia de PySpark 4.2 documenta `SparkSession.table(tableName)`: "devuelve la tabla indicada como DataFrame", nueva en la versión 2.0.0 y compatible con Spark Connect desde la 3.4. En Zeppelin `sqlContext` sigue existiendo por compatibilidad C3P1 1:27:01, pero en código nuevo usá `spark.table`.

#### 3.10. Broadcast y AQE

**Qué dice la fuente.** En clase se usa `broadcast()` a mano para el join con la tabla de aerolíneas C3P1 1:34:15.

**Qué suma el material externo.** La guía de rendimiento de Spark SQL dice que `spark.sql.autoBroadcastJoinThreshold` vale 10 MB por defecto: cualquier tabla que Spark estime por debajo de eso se manda a todos los nodos sin pedirlo. AQE (Adaptive Query Execution) "reoptimiza el plan en mitad de la ejecución con estadísticas reales" y viene prendido desde Spark 3.2.0; entre otras cosas convierte joins a broadcast y junta particiones chicas después de un shuffle. La guía de tuning suma que Kryo es "a menudo hasta 10x" más rápido y compacto que la serialización de Java.

**Cómo implementarlo.** Dejá AQE prendido; usá `broadcast()` explícito cuando Spark no tiene estadísticas (por ejemplo, después de una UDF) y mirá el plan con `explain()` para confirmar `BroadcastHashJoin`.

#### 3.11. MLlib: la API de RDD está en mantenimiento

**Qué suma el material externo.** La guía de MLlib dice que "la API de MLlib basada en RDD está en modo mantenimiento" desde Spark 2.0; la principal es la de DataFrames (`pyspark.ml`), que es la que usa la materia. Si encontrás ejemplos viejos con `pyspark.mllib`, no los copies.

### 4. El benchmark: qué medí y cómo

La pregunta: con los datos de la materia, y con versiones 10 y 100 veces más grandes, ¿cuánto tarda y cuánta memoria usa Spark en `local[*]` contra DuckDB, Polars y pandas en una sola máquina, haciendo las mismas consultas de los ejemplos resueltos en clase?

- **Datos.** `flights.csv` del repositorio 2019 (100.000 filas, 29 columnas, 9 MB) y copias de 1 y 10 millones de filas hechas repitiendo el cuerpo (92 y 926 MB en CSV; 14 y 147 MB en Parquet). Repetir filas hace que el Parquet comprima mejor que con datos reales, así que el ×100 en Parquet es optimista. Para grafos, la red de retuits `twitter-out` en Parquet (172.040 retuits) y una versión ×10 con diez copias disjuntas (sufijo `_1`, `_2`... en los usuarios), que da exactamente 10 veces las aristas y los vértices.
- **Consultas de vuelos** (las cinco de las clases 2 y 3): q1, cantidad y porcentaje de vuelos con DepDelay > 15 C3P1 9:20, C3P1 27:02; q2, demorados en llegada por aerolínea C3P1 48:30; q3, TaxiOut medio por origen y destino, los 10 mayores C3P1 30:27; q4, demorados y en horario por hora de salida C3P1 1:07:10; q5, join con `carriers.csv` y conteo por nombre de aerolínea (en Spark, con `broadcast`) C3P1 1:34:15.
- **Consulta de grafos.** La influencia colectiva del ejemplo resuelto de la clase 4 C4P3 1:01:22, C4P3 1:03:11: armar las aristas (del que retuitea al retuiteado, sin repetir), calcular el grado y la suma de (grado del vecino − 1), y quedarse con los 10 de mayor CI. En los cuatro motores la escribí con joins y agregaciones comunes (en Spark, con DataFrames y sin GraphFrames), así el motor es lo único que cambia. No es ninguno de los ejercicios que se entregan.
- **Control.** Los cuatro motores dan los mismos números que la clase en el ×1 (19.587 demorados, 19,587%; WN 17.753 y XE 1041; LCH a IAH 84,0; a las 13 h, 1346 demorados y 5225 en horario; Southwest 94.055 y Expressjet 5945; 152.613 aristas, 57.138 vértices y Winston_Dunhill primero con CI 71.551.312) y exactamente 10 y 100 veces esos conteos en las copias.
- **Cómo medí.** Cada configuración corre en un proceso aparte y un script mide cada 50 ms la memoria residente (RSS) de todo el árbol de procesos (en Spark incluye la JVM). Separo arranque, "carga" (dejar los datos listos en memoria: en Spark, `cache()` más `count()`; en DuckDB, `CREATE TABLE`; en Polars y pandas, leer el archivo) y cada consulta, que corre tres veces (me quedo con la mejor). Repetí todo dos veces y reporto la corrida de menor tiempo total. Polars lee el CSV con `infer_schema_length=None` (mira todas las filas para inferir tipos, como el `inferSchema` de Spark) y pandas con `low_memory=False`.

### 5. Resultados: vuelos

Tiempos en segundos; "consultas" es la suma de la mejor corrida de q1 a q5; "total" es todo el proceso, con arranque e importaciones; "pico" es la memoria máxima del proceso.

| Datos | Motor | Arranque | Carga | Consultas (q1 a q5) | Total | Pico de memoria |
|---|---|---|---|---|---|---|
| ×1 CSV (9 MB) | pandas | 0,3 | 0,25 | 0,038 | 0,9 | 169 MB |
| | Polars | 0,1 | 0,58 | 0,012 | 0,9 | 168 MB |
| | DuckDB | 0,1 | 0,26 | 0,024 | 0,5 | 149 MB |
| | Spark | 2,5 | 5,05 | 0,67 | 11,9 | 806 MB |
| ×1 Parquet (1 MB) | pandas | 0,3 | 0,06 | 0,043 | 0,6 | 261 MB |
| | Polars | 0,1 | 0,03 | 0,012 | 0,3 | 156 MB |
| | DuckDB | 0,1 | 0,14 | 0,023 | 0,4 | 131 MB |
| | Spark | 2,4 | 5,22 | 0,79 | 11,8 | 715 MB |
| ×10 CSV (92 MB) | pandas | 0,3 | 2,82 | 0,31 | 4,3 | 873 MB |
| | Polars | 0,1 | 5,68 | 0,076 | 6,2 | 802 MB |
| | DuckDB | 0,1 | 0,84 | 0,033 | 1,2 | 679 MB |
| | Spark | 2,6 | 6,99 | 0,77 | 14,5 | 1,6 GB |
| ×10 Parquet (14 MB) | pandas | 0,3 | 0,19 | 0,35 | 1,8 | 800 MB |
| | Polars | 0,1 | 0,05 | 0,10 | 0,6 | 848 MB |
| | DuckDB | 0,1 | 0,11 | 0,031 | 0,4 | 449 MB |
| | Spark | 2,5 | 7,15 | 0,84 | 14,4 | 1,3 GB |
| ×100 CSV (926 MB) | pandas | 0,4 | 29,7 (52,2 en la otra corrida) | 3,74 | 42,9 | **7,9 GB** |
| | Polars | 0,1 | 58,6 | 0,71 | 62,5 | 5,8 GB |
| | DuckDB | 0,1 | 3,60 | 0,23 | 4,7 | 3,9 GB |
| | Spark | 3,0 | 17,2 | 1,87 | 28,6 | 3,2 GB |
| ×100 Parquet (147 MB) | pandas | 0,4 | 1,56 | 3,95 | 15,0 | 5,6 GB |
| | Polars | 0,1 | 0,70 | 1,12 | 5,2 | 6,3 GB |
| | DuckDB | 0,1 | 1,00 | 0,23 | 2,0 | 3,6 GB |
| | Spark | 2,8 | 12,8 | 1,81 | 23,8 | 3,0 GB |

**Variante sin cargar antes** (una consulta suelta de punta a punta, leyendo el archivo cada vez: DuckDB con `read_parquet` o `read_csv` dentro del SQL, Polars con `scan_parquet` o `scan_csv` en modo perezoso y con la inferencia por defecto, Spark sin `cache()`), mejor de tres corridas de q2 y q5:

| Datos | Motor | q2 | q5 | Primera corrida de q2 | Total del proceso | Pico |
|---|---|---|---|---|---|---|
| ×100 Parquet | DuckDB | 0,019 | 0,075 | 0,030 | 0,4 | 85 MB |
| | Polars (perezoso) | 0,018 | 0,074 | 0,053 | 0,5 | 260 MB |
| | Spark (sin cache) | 0,32 | 1,01 | 4,37 | 13,1 | 1,2 GB |
| ×100 CSV | DuckDB | 0,87 | 0,94 | 1,34 | 6,2 | 599 MB |
| | Polars (perezoso) | 0,55 | 0,51 | 0,68 | 3,8 | 1,2 GB |
| | Spark (sin cache) | 5,90 | 6,33 | 10,65 | 46,3 | 1,9 GB |

### 6. Resultados: grafo de retuits (influencia colectiva)

| Datos | Motor | Carga | CI (mejor de 3) | Total | Pico de memoria |
|---|---|---|---|---|---|
| ×1 (152.613 aristas) | pandas | 0,07 | 0,19 | 1,2 | 300 MB |
| | Polars | 0,03 | 0,056 | 0,4 | 192 MB |
| | DuckDB | 0,05 | 0,078 | 0,5 | 171 MB |
| | Spark (200 particiones, por defecto) | 3,99 | 7,32 | 33,5 | 3,4 GB |
| | Spark (8 particiones de shuffle) | 3,77 | 1,07 | 12,9 | 1,7 GB |
| ×10 (1.526.130 aristas) | pandas | 0,18 | 2,41 | 8,0 | 1,1 GB |
| | Polars | 0,06 | 0,75 | 2,6 | 827 MB |
| | DuckDB | 0,11 | 0,36 | 1,4 | 971 MB |
| | Spark (200 particiones, por defecto) | 4,92 | 12,03 | 50,1 | 3,0 GB |
| | Spark (8 particiones de shuffle) | 4,91 | 2,69 | 23,6 | 2,4 GB |

Con 8 particiones de shuffle, Spark también mejoró apenas en vuelos ×100 Parquet (total 22,8 s contra 23,8 s; pico 2,0 a 2,3 GB): ahí el costo está en la carga y el arranque, no en el shuffle.

### 7. Qué muestra el benchmark

- **Con los datos de la materia, Spark en una máquina pierde siempre en tiempo.** Por consulta, DuckDB fue de 8 a 35 veces más rápido que Spark en vuelos (0,023 contra 0,79 s en ×1 Parquet; 0,23 contra 1,81 s en ×100 Parquet) y de 30 a 90 veces en el grafo con la configuración por defecto. Solo el arranque de Spark (2,5 a 3 s, levantar la JVM) ya es más que todo el trabajo de DuckDB en casi todas las configuraciones.
- **La afirmación de clase "Spark le gana a scikit-learn en una máquina porque usa todos los núcleos" C2P1 34:25 no se sostiene contra motores modernos**: DuckDB y Polars también usan todos los núcleos, sin JVM ni serialización entre Python y Java.
- **La configuración por defecto de Spark castiga a los datos chicos.** Con 200 particiones de shuffle (el valor por defecto) el CI tardó 7,3 s; con 8 (una por núcleo), 1,1 s. AQE junta particiones chicas, pero no alcanza a compensar. Es una lección práctica para la materia: en `local[*]`, bajá `spark.sql.shuffle.partitions`.
- **Parquet cambia todo.** Leer el CSV de 926 MB fue la parte más cara para todos menos DuckDB; en Parquet, DuckDB y Polars responden una consulta suelta sobre 10 millones de filas en 0,02 a 0,08 s sin cargar nada antes y con menos de 300 MB de memoria, porque leen solo las columnas que usa la consulta.
- **La memoria es donde Spark no sale mal.** En ×100, Spark (limitado a 4 GB de driver, con el cache comprimido en columnas) usó 3,0 a 3,2 GB, menos que pandas (5,6 a 7,9 GB) y Polars en modo ansioso (5,8 a 6,3 GB), y parecido a DuckDB con la tabla cargada (3,6 a 3,9 GB). pandas con el CSV de 926 MB llegó a 7,9 GB: con un CSV de 2 GB no habría entrado en este box. En modo perezoso o directo, DuckDB y Polars bajan a decenas o cientos de MB.
- **Polars con inferencia completa es lento leyendo CSV** (58,6 s en ×100, el peor). Con la inferencia por defecto y `scan_csv` en modo perezoso, la misma consulta sobre el mismo CSV tardó 0,55 s. La comparación de carga en CSV es injusta para Polars por cómo la configuré, y lo dejo dicho.
- **Lo que este benchmark no mide:** datos que no entran en una máquina, tolerancia a fallas, muchos usuarios a la vez y trabajos de horas. Es justamente donde Spark tiene sentido (ver "Críticas y límites" y el análisis adversario).

### 8. Para estudiar Spark hoy

**Qué dice la fuente.** El docente recomienda *Learning Spark* y avisa que la bibliografía está "viejita" C2P1 15:25; en mi apunte escribí que el contenedor trae Spark 3.5.9, pero la marca que cité no lo respalda (sección 11).

**Qué suma el material externo.**

- ***Learning Spark*, 2.ª edición** (O'Reilly): según lo que vi en el buscador, cubre Spark 3.0 y Databricks la regala como ebook (conflicto de interés: es su libro y su producto). Abrí solo el repositorio oficial del código, `databricks/LearningSparkV2`; la página de descarga que probé dio 404. Es la versión que conviene leer en lugar de la de 2015 que lista la página de la materia.
- **La documentación oficial está al día y es buena.** La guía de programación de RDD explica transformaciones, acciones, evaluación perezosa y persistencia con los mismos ejemplos que la clase. La guía de rendimiento de Spark SQL explica cache de tablas, broadcast automático y AQE. La guía de tuning explica serialización (Kryo), memoria y paralelismo.
- **Spark 4.** Las notas de Spark 4.0.0 traen: ANSI SQL por defecto (las conversiones inválidas tiran error en vez de devolver null), Java 17 por defecto, Python 3.8 afuera, Python 3.13 en Spark Connect, un cliente `pyspark-client` de 1,5 MB y SparkR deprecado. La última versión es la 4.2.0 (14/07/2026), con tipos geoespaciales, captura de cambios (CDC) y UDF de Python optimizadas con Arrow por defecto.
- **Spark Connect.** Desde Spark 3.4 hay "una arquitectura cliente servidor desacoplada que permite conectarse a clústeres remotos con la API de DataFrames", mandando planes lógicos sin resolver. En la práctica: tu notebook de Python no necesita Java ni el clúster en la misma máquina.

**Cómo implementarlo.** Para la materia, seguí con la versión que trae el contenedor del curso (es con la que se corrige). Para un proyecto propio nuevo, arrancá en 4.x y leé la guía de migración, sobre todo por ANSI: código que en 3.5 devolvía null puede tirar error en 4.0.

### 9. Las alternativas: una sola máquina y Python distribuido

**Qué dice la fuente.** "Si entra en una computadora, scikit-learn" C1P1 42:16, pero también que Spark a veces le gana a scikit-learn en una sola máquina porque usa todos los núcleos C2P1 34:25. Dask es "un parche" sobre pandas C4P3 2:04:09.

**Qué suma el material externo.**

- **COST (McSherry, Isard y Murray, HotOS 2015).** Definen COST como "la configuración de hardware necesaria antes de que la plataforma supere a una implementación competente en un solo hilo". Con el grafo `twitter_rv`, 20 iteraciones de PageRank tardaron 857 s en Spark con 128 núcleos, 419 s en GraphX con 128 núcleos y 300 s en **un solo hilo** de una laptop de 2014 (275 s leyendo de RAM). Componentes conexas: 1784 s Spark, 251 s GraphX, 153 s un hilo. Concluyen que "muchos sistemas publicados tienen COST ilimitado": ninguna configuración le gana al hilo único. Son resultados de 2015 y de grafos, pero la pregunta sigue sirviendo.
- **"Big Data is Dead" (Jordan Tigani, MotherDuck, 2023).** Tigani fue ingeniero fundador de BigQuery y hoy dirige MotherDuck, que vende DuckDB en la nube (conflicto de interés fuerte). Dice que la gran mayoría de los clientes de BigQuery tenían menos de 1 TB en total, que entre los que más lo usaban la mediana de almacenamiento era "mucho menos de 100 GB" y que el 90% de las consultas procesaba menos de 100 MB. Él mismo avisa que sus gráficos están "dibujados a mano, de memoria", sin poder mostrar los números.
- **DuckDB.** Base de datos analítica, columnar, que corre **dentro del proceso** (como SQLite, sin servidor que instalar) y puede consultar datos de pandas, Arrow o Parquet sin copiarlos.
- **Polars.** Biblioteca de DataFrames escrita en Rust, con optimizador de consultas, paralela por defecto y con una API de streaming para procesar datos más grandes que la memoria.
- **Dask.** "Biblioteca de Python para cómputo paralelo y distribuido": sus DataFrames paralelizan pandas, permiten trabajar con más datos que la RAM en una máquina y escalan a clústeres para "datasets de terabytes". Es más que un parche, aunque es cierto que hereda las limitaciones de pandas.
- **Ray.** "Framework unificado para escalar aplicaciones de IA y Python", con Ray Data para ingesta y preprocesamiento y Ray Train y Tune para entrenamiento. Apunta más a aprendizaje automático distribuido que a SQL.

**Cómo implementarlo (sugerencia).** Antes de abrir Spark, hacé la pregunta de Tigani y de McSherry con tus datos: ¿cuánto pesan en Parquet? ¿qué parte toca cada consulta? ¿cuánto tarda DuckDB o Polars en una máquina? El benchmark de las secciones 4 a 7 es esa prueba con los datos de la materia.

### 10. Formatos de tabla, grafos y casos de la región

**Delta Lake e Iceberg.** La materia guarda en Parquet y ORC y usa tablas permanentes de Spark C2P2 51:09. Delta Lake (creado por Databricks, conflicto de interés) suma sobre Parquet "transacciones ACID, metadatos escalables" y une streaming y batch sobre S3, ADLS, GCS o HDFS. Apache Iceberg es "un formato de alto rendimiento para tablas analíticas enormes" que permite que Spark, Trino, Flink, Presto, Hive e Impala trabajen "con las mismas tablas, al mismo tiempo", con `MERGE`, `UPDATE` y `DELETE`. **Cómo implementarlo:** si tus tablas se actualizan o las leen varios motores, escribí en Delta o Iceberg; si son resultados de un notebook que no cambian, Parquet alcanza. Y DuckDB y Polars también leen Parquet, así que el mismo archivo sirve para los dos mundos.

**GraphFrames contra GraphX.** La materia usa GraphFrames porque trabaja con DataFrames y desde Python C4P3 5:11. GraphX es la biblioteca oficial sobre RDD y no tiene API de Python. En 2025 GraphFrames volvió a tener mantenimiento activo (versión 0.9.2 con Spark 4 y Spark Connect, nuevo `groupId` `io.graphframes` y paquete `graphframes-py` en PyPI) y anunció que GraphX quedará deprecado en GraphFrames 1.0 y se sacará en la 2.0 (sección 1). **Cómo implementarlo:** con Spark 3.5, el jar `graphframes-0.8.4-spark3.5` de la guía funciona; con Spark 4, usá los paquetes nuevos.

**Casos de Argentina y la región.** La materia ya trae uno argentino: SAOCOM con el catastro rural de Córdoba (IDECOR) C1P1 22:18. Encontré uno documentado más, que **no** usa Spark: Mercado Libre contó en el blog de Google Cloud (01/08/2022, conflicto de interés: es el blog del proveedor) que su equipo de operaciones de envíos pasó de Kibana más Teradata a BigQuery más Looker, con datos casi en tiempo real y más de 150 consultas concurrentes por tablero, y que entregó el 79% de los envíos en menos de 48 horas en el primer trimestre de 2022. Es un ejemplo de la alternativa C de la sección de análisis adversario (warehouse administrado). Otros casos que vi solo en el buscador (perfiles de LinkedIn de ingenieros de Mercado Libre que mencionan Spark, Hive y Presto) no los cito porque no son fuentes verificables.

### 11. Correcciones a mis archivos de la primera parte

**Revisión de marcas de tiempo.** Revisé las 615 marcas del apunte con un script que compara cada afirmación con el minuto de transcripción que cita (puntaje por palabras en común) y miré a mano las 99 dudosas: las 28 de coincidencia baja, las 50 de coincidencia media y las 21 que solo aparecen en las listas "Dónde". Casi todas caen al comienzo del tramo correcto (los tramos de transcripción duran cerca de un minuto). Estas son las que están mal (el número de línea es el del apunte entregado):

1. **Línea 76 y línea 348, Event Horizon Telescope.** Dice C1P1 26:19; los 350 TB por día por telescopio están en C1P1 31:19, la "media tonelada" en C1P1 32:27 y los "5 PB en un avión" en C1P1 33:00.
2. **Línea 127, el CCAD.** "`sc.defaultParallelism` da 2 en vez de 8" cita C2P1 31:09; el 2 aparece en C2P1 33:21 (en 31:09 da 8, en su máquina, que es lo que dice bien la línea 159).
3. **Línea 271, regresión logística.** `LogisticRegression(maxIter=10, regParam=0.001)` cita C4P1 29:04; está en C4P1 30:12.
4. **Línea 307, motif finding.** La primera marca, C4P3 1:14:07, es sobre filtrar el grafo; los pares mutuos están en C4P3 1:17:23 y C4P3 1:18:27.
5. **Línea 56, lista "Dónde" del módulo 0.** C3P1 36:00 es el `z.show`; el comentario sobre la IA que esa lista quería citar está en C3P1 37:07.

Al escribir esta parte encontré tres más, mirando los minutos que cito acá:

6. **Líneas 75 y 346, Netflix.** El 15% del tráfico de 2022 cita C1P1 21:07; está en el tramo que empieza en C1P1 20:07 (en 21:07 ya habla de PepsiCo).
7. **Línea 206, TaxiOut por origen y destino.** Cita C3P1 29:16, que es sobre traer la primera fila al driver; el TaxiOut empieza en C3P1 30:27.
8. **Línea 353, Spark 3.5.9.** Dice "versión del contenedor C1P2 57:00", pero en ese minuto, y en ningún otro de los subtítulos, se nombra la versión de Spark. Puede que se vea en pantalla; no lo puedo confirmar. Debería decir "versión que usé en el box; la del contenedor, para verificar".

Antes de entregar ya había corregido otras tres (el promedio en C3P1 1:01:31, C4P3 1:58:20 y C3P1 1:18:40), que están bien en el archivo entregado.

**Errores de contenido.**

9. **La cuenta de los 253 millones de años (línea 349).** Escribí que "la cuenta da otra cosa" (31,7 millones). Está mal: la cuenta del docente es correcta si "1 GB por segundo" es un **gigabit** por segundo (10^24 × 8 / 10^9 s = 253,5 millones de años). Lo que da 31,7 millones es un gigabyte por segundo. Debería decir "correcto a 1 Gbit/s".
10. **El CERN (línea 345).** Puse que el docente dice "un PB por día" en C1P1 36:21 y que "se contradice". No dice eso: en ese minuto dice que el CERN "tiene archivado" alrededor de un **exabyte**. No hay contradicción; 1 PB/s (antes de filtrar, C1P1 18:28) y 1 EB de disco son cosas distintas, y las dos son correctas en orden de magnitud (sección 1).
11. **Hive y Redshift (línea 326).** Lo marqué como "Corrección". Es un "Matiz": la página de Hive lo define como data warehouse para petabytes con SQL, igual que AWS define a Redshift; la diferencia es de arquitectura (sección 3.7).
12. **MapReduce y PageRank (línea 99).** Escribí como hecho que PageRank fue "el problema que originó MapReduce en Google". El paper de MapReduce no menciona PageRank; habla del sistema de indexación. Debería decir "según el docente" y marcarlo dudoso (sección 1).
13. **"Computacionalmente imposible" (líneas 175 y 330).** Escribí que no encontré "ningún resultado de imposibilidad". Sí hay uno que encaja: el teorema de Rice. El veredicto pasa de "dudoso" a "correcto en espíritu, aunque Spark tampoco intenta los casos decidibles" (sección 1).
14. **Red de 50 GB/s (línea 343).** Puse "no queda claro qué quiso decir". La transcripción dice "un protocolo de red no supera los 50 GB por segundo desde hace ya muchos años": la cifra es falsa (hay Ethernet de 400 y 800 Gb/s), la tendencia de fondo (la red crece más lento que el cómputo) es defendible.
15. **Las filas "No lo chequeé" (líneas 344 a 352).** Ya quedan resueltas en la sección 1: Boeing dudoso, CERN, Netflix, EHT y 90% confirmados, SAOCOM en parte, IDC en parte, clientes de Databricks confirmados con conflicto de interés.
16. **Guía, sección 13, `distutils`.** Dejé "para verificar" si pasa en el contenedor del curso. Ahora está explicado (SPARK-45390): pasa con cualquier Python 3.12 o más nuevo y PySpark 3.5; si el contenedor trae Python 3.11 o anterior, no pasa. Sigo sin saber qué Python trae el contenedor 2026.

## Críticas y límites

- **El benchmark es chico a propósito, y eso favorece a la alternativa.** El dato más grande son 10 millones de filas (926 MB en CSV), muy por debajo de donde Spark tiene sentido. `local[*]` no es un clúster: no hay red, ni nodos que fallan, ni datos repartidos en discos distintos. Lo que el benchmark prueba es la afirmación de la materia sobre Spark en una máquina C2P1 34:25, no Spark en su terreno.
- **Las copias agrandadas son artificiales.** Repetir filas hace los datos más regulares y el Parquet más compresible que con datos reales; el ×10 de tweets son diez grafos disjuntos, no una red más densa.
- **Spark corrió casi sin tunear** (salvo la variante de 8 particiones), en 3.5.9 y no en 4.x, con 4 GB de driver. Con más memoria, Kryo o Spark 4 podría mejorar algo; no cambiaría el orden de magnitud del arranque de la JVM.
- **El box es compartido**: dos corridas de pandas con el mismo CSV dieron 29,7 y 52,2 s de carga. Tomá los tiempos como órdenes de magnitud.
- **La medición de memoria es el RSS del proceso**, que incluye memoria que la JVM reserva y no usa, y no incluye la caché de archivos del sistema operativo.
- **Las fuentes de la alternativa tienen intereses.** MotherDuck vende DuckDB; Tigani admite que sus gráficos son de memoria. Databricks publica los casos de clientes de Spark y es autora de Delta y GraphFrames. Google publica el caso del EHT y el de Mercado Libre. Seagate patrocina la cifra de IDC. El paper de COST es académico y revisado por pares, pero es de 2015 y sobre grafos.
- **La revisión de marcas de tiempo es semiautomática.** Un primer script compara palabras entre la afirmación y una ventana de unos dos minutos alrededor de la marca; revisé a mano 99 de las 615 marcas (las de puntaje bajo o medio y las de listas "Dónde"). Un segundo script busca los números de cada afirmación en el tramo citado y en los vecinos: marcó 25 casos, que revisé; son cifras dichas en el minuto anterior o siguiente (lo tomo como tolerancia) o cifras que salen de mi verificación en el box y no de la clase. Las tres marcas que encontré al escribir esta parte (Netflix, TaxiOut y la versión de Spark) muestran que la ventana del primer script era generosa: puede quedar alguna marca que cae un minuto después de lo que cita.
- **Quedaron sin resolver**: los 100 TB por año de SAOCOM, los dos clientes de Databricks que el subtítulo da como "Mitely" y "Simel", y qué versión de Python trae el contenedor del curso.
- **Páginas que leí con curl** (texto extraído en el box): guía de RDD, guía de rendimiento de Spark SQL, guía de tuning, Spark Connect, guía de features de MLlib, guía de Parquet, referencia de `PolynomialExpansion`, `StringIndexer` y `SparkSession.table`, notas de Spark 4.0.0 y 4.2.0, guía de GraphX 4.0 y 4.2, guía de MLlib; Hadoop Streaming; Apache Hive; actas del directorio de Apache sobre Spark; Wikipedia (teorema de Rice, ley de Moore, Terabit Ethernet); Nielsen; DuckDB "Why DuckDB"; documentación de Polars, Dask, Ray, Delta Lake e Iceberg; Morone y Makse en *Nature* (resumen); guía de usuario y de motif finding de GraphFrames; sitio de DDIA; página de contenedores de Microsoft. PDF bajados y convertidos: Dean y Ghemawat 2004, Zaharia y otros 2010 y 2012, McSherry y otros 2015, Zaharia y otros en *;login:*, Boeing para IATA 2017, Sandvine 2023 e IDC y Seagate 2018; Rivery.
- **Abiertas con el lector web**: "Big Data is Dead" de MotherDuck; Amazon Redshift y Amazon Athena; CERN (almacenamiento y el exabyte de disco); CONAE SAOCOM; caso del EHT de Google; Ubergizmo 2013; páginas de clientes de Databricks (Santander, Heineken, Mercedes-Benz) y blog de PepsiCo; blog "GraphFrames is back!"; PR #26928 de Spark; votación para deprecar GraphX; SPARK-45390; página de DDIA 2.ª edición de Kleppmann; blog de Google Cloud sobre Mercado Libre; repositorio `databricks/LearningSparkV2`; FAQ del EHT (al volver a abrirla dio 403).
- **Vistas solo en el buscador**: comunicado de Toyota y Databricks (enero de 2026); los 394 ZB de IDC para 2028; la página de descarga de *Learning Spark* de Databricks; la ficha de O'Reilly de DDIA 2.ª edición; SPARK-44120 (soporte de Python 3.12); la versión 0.12.3 de GraphFrames; perfiles de LinkedIn de Mercado Libre.
- **No cargaron**: comunicado de prensa del EHT (403); página de IDC en marketresearch (sin contenido útil); resultado de la votación de GraphX en lists.apache.org; página de *Learning Spark* en databricks.com (404); referencia de `SQLContext` (404); notas de Spark 4.1.0 en la dirección que probé (404); documentación de S3 y EMR con curl (sin respuesta).

## Análisis adversario

> Cómo leer esto: tomo la tesis de la materia, busco la alternativa más fuerte, la presento en su mejor versión (con quién la defiende y qué evidencia tiene, a favor y en contra), las comparo de frente y termino con criterios para elegir. Lo que marco "sugerencia" es mío.

**La tesis.** Cuando los datos no entran en una computadora, hay que llevar el cómputo a los datos y repartirlo en un clúster; Spark es la herramienta estándar, madura y "muy profesional" para eso C4P3 8:07, mejor que MapReduce porque guarda en memoria C1P1 1:55:15 y mejor que MPI porque tolera fallas C4P3 2:04:09. Además conviene usarla incluso en una sola máquina, porque aprovecha todos los núcleos C2P1 34:25.

### La alternativa más fuerte: motores de una sola máquina (DuckDB y Polars) sobre Parquet

Evalué cuatro candidatas:

1. **DuckDB o Polars en una máquina grande**, con los datos en Parquet. Ataca la premisa ("tus datos no son tan grandes") y se puede probar con los datos de la materia.
2. **Un warehouse administrado** (BigQuery, Snowflake, Redshift, Athena): SQL sin administrar clústeres, se paga por uso. Es fuerte en organizaciones (el caso de Mercado Libre), pero no se puede probar gratis en el box y compite más con Databricks que con lo que enseña la materia.
3. **Dask o Ray**: distribuido pero en Python nativo. Resuelve el mismo problema que Spark con otra API; la evidencia pública a favor es más débil y el docente ya lo discute.
4. **MPI y HPC**: la materia ya explica por qué no, para datos (sin tolerancia a fallas, depende del filer).

Elijo la 1 porque es la única que discute **cuándo** hace falta distribuir (no solo cómo), tiene evidencia independiente y revisada por pares (COST) además de la de los vendedores, y se puede medir acá. La 2 queda como tercera opción en la comparación.

### La alternativa en su mejor versión

**Quién la defiende.** Frank McSherry, Michael Isard y Derek Murray (COST, HotOS 2015),, investigadores de sistemas distribuidos. Jordan Tigani, ingeniero fundador de BigQuery y hoy al frente de MotherDuck (conflicto de interés). Los equipos de DuckDB y Polars, que tienen empresas detrás.

**Qué evidencia la respalda.**

- COST: un hilo de una laptop le ganó a Spark con 128 núcleos en PageRank (300 s contra 857 s) y en componentes conexas (153 s contra 1784 s), y también a GraphX.
- Tigani: la mayoría de los clientes de BigQuery tenían menos de 1 TB; el 90% de las consultas leía menos de 100 MB; una sola máquina de la nube llegaba en 2023 a 24 TB de RAM y 445 núcleos.
- Mi benchmark: con los datos de la materia y hasta 10 millones de filas, DuckDB fue de 8 a 35 veces más rápido por consulta en vuelos y de 30 a 90 veces en el grafo (con Spark por defecto), con un total de proceso de 0,4 a 4,7 s contra 12 a 50 s.
- Costo: es una biblioteca de Python que se instala con `pip`, sin Java, sin clúster y sin Docker.

**Qué evidencia la contradice.**

- **Hay datos que de verdad no entran en una máquina.** El CERN tiene 1 EB de disco, el EHT juntó varios PB, PepsiCo dice tener 6 PB en su lakehouse (según Databricks). Ahí no hay discusión.
- **Tolerancia a fallas.** Un trabajo de horas en una máquina se pierde entero si la máquina se cae; Spark reintenta tareas y reconstruye particiones a partir del linaje (el paper de NSDI 2012).
- **Memoria.** En ×100, pandas y Polars en modo ansioso usaron más memoria que Spark, que estuvo acotado a 4 GB. Los motores de una máquina tienen modo perezoso y de streaming, pero el techo es el de la máquina.
- **Las cifras de Tigani no se pueden verificar** (gráficos de memoria) y vienen de alguien que vende la alternativa. COST es de 2015 y sobre grafos; GraphX y Spark mejoraron desde entonces.
- **Contexto organizacional**: si la empresa ya tiene un lakehouse en Databricks, gobernanza centralizada y miles de usuarios, sumar una herramienta de una máquina es otra pieza más que mantener.

### Comparación directa

| Criterio | A: Spark (la materia) | B: DuckDB o Polars en una máquina | C: warehouse administrado (BigQuery, Snowflake, Redshift) |
|---|---|---|---|
| Costo | Gratis local; un clúster o Databricks se paga por hora de máquina | Gratis; una máquina grande en la nube se paga por hora | Se paga por consulta o por tiempo de cómputo; nada que administrar |
| — | Alta: JVM, Docker, configuración de memoria, particiones, shuffle | Baja: `pip install`, SQL o DataFrames | Baja para el usuario; alta dependencia del proveedor |
| Tiempo hasta el valor | Minutos para arrancar; 12 s de proceso mínimo en el benchmark | Segundos; 0,3 a 5 s de proceso en el benchmark | Minutos para cargar los datos; consultas en segundos |
| Riesgo | Configuración por defecto lenta en datos chicos (200 particiones); fácil equivocarse con cache | Techo de una máquina; sin tolerancia a fallas | Costo que crece con el uso; datos en un proveedor |
| Madurez | Muy alta (desde 2010, Apache, miles de empresas) | Alta y reciente (DuckDB 1.x, Polars 2.x) | Muy alta |
| Evidencia | Papers de Zaharia y casos de clientes (de Databricks) | COST (revisado por pares), mi benchmark, Tigani (con conflicto) | Casos de proveedores (Mercado Libre en el blog de Google) |
| Dónde rinde | Datos de TB a PB, trabajos largos, aprendizaje automático y grafos distribuidos | Datos de MB a cientos de GB en Parquet, análisis interactivo, un usuario | SQL de toda una organización, muchos usuarios y tableros |

### Dónde gana la alternativa

- Todo lo que entra en una máquina, que según Tigani es la mayoría de los casos reales y según el benchmark incluye todos los datasets de la materia multiplicados por 100.
- Exploración interactiva en notebooks: respuesta en centésimas de segundo, sin esperar a la JVM.
- Enseñanza y prototipos: menos piezas que pueden romperse (Docker, Java, `distutils`, memoria del driver).

### Dónde pierde

- Cuando los datos o el cómputo no entran en la máquina más grande que podés pagar, o cuando la consulta tiene que leer gran parte de varios TB.
- Trabajos largos donde perder una máquina es perder horas.
- Organizaciones que ya tienen Spark o Databricks, con datos compartidos y gobernados.
- Streaming y pipelines de aprendizaje automático distribuidos, donde Spark tiene un ecosistema que los motores de una máquina no tienen.

### Cómo decidir

**Elegí A (Spark) si** tus datos en Parquet superan lo que entra cómodo en el disco y la memoria de una máquina (varios TB o más), si tenés trabajos de horas que no pueden empezar de cero ante una falla, si ya trabajás sobre un lakehouse con Spark o Databricks, o si necesitás streaming, aprendizaje automático o grafos sobre datos distribuidos. Y, por supuesto, para la materia: los entregables se hacen en Spark.

**Elegí B (DuckDB o Polars) si** tus datos en Parquet entran en el disco de una máquina (de MB a cientos de GB), si trabajás solo o en un equipo chico, si querés respuestas interactivas en un notebook o si estás prototipando antes de saber si hace falta escalar.

**Y C (warehouse administrado) si** la necesidad es SQL para toda una organización, con muchos usuarios y tableros a la vez, y preferís pagar por uso a mantener infraestructura, como hizo Mercado Libre con sus operaciones de envíos.

**Un híbrido posible (sugerencia).** Guardá todo en Parquet (o Delta o Iceberg si se actualiza), que leen los tres. Explorá y prototipá con DuckDB o Polars sobre una muestra o una partición (por ejemplo, un mes). Cuando el mismo trabajo pase un umbral concreto, por ejemplo más de la mitad de la RAM de la máquina o más de unos minutos por corrida, pasalo a Spark: el SQL de DuckDB y el de Spark SQL se parecen mucho, así que la lógica se traslada casi entera. Usá Spark para producir tablas agregadas y DuckDB para consultarlas. Y antes de comprar clúster, aplicá COST: medí contra una buena versión en un hilo o en una máquina.

**Veredicto.** La materia tiene razón en lo importante: cuando los datos no entran en una máquina, hay que distribuir, y Spark es la herramienta madura para eso; aprenderla vale la pena. Donde se queda corta es en la afirmación de que Spark conviene incluso en una sola máquina: con los datos del curso y hasta 100 veces más grandes, DuckDB y Polars fueron entre 8 y 90 veces más rápidos por consulta, con menos piezas y, en modo perezoso, con mucha menos memoria. La regla práctica del propio docente ("si entra en una computadora, usá herramientas de una computadora") es la correcta; solo hay que actualizar la lista de herramientas.

## Material para seguir

**Papers fundacionales**

- [Dean y Ghemawat, "MapReduce: Simplified Data Processing on Large Clusters", OSDI 2004](https://static.googleusercontent.com/media/research.google.com/es//archive/mapreduce-osdi04.pdf): el origen de todo lo que la materia explica en la clase 1; corto y claro.
- [Zaharia y otros, "Spark: Cluster Computing with Working Sets", HotCloud 2010](https://www.usenix.org/legacy/event/hotcloud10/tech/full_papers/Zaharia.pdf): el primer paper de Spark, seis páginas, con el argumento de los trabajos iterativos.
- [Zaharia y otros, "Resilient Distributed Datasets", NSDI 2012](https://www.usenix.org/system/files/conference/nsdi12/nsdi12-final138.pdf): explica RDD, linaje, persistencia y tolerancia a fallas; es la teoría detrás de las clases 1 y 2.
- [McSherry, Isard y Murray, "Scalability! But at what COST?", HotOS 2015](https://www.usenix.org/system/files/conference/hotos15/hotos15-paper-mcsherry.pdf): la pregunta que hay que hacerse antes de distribuir.

**Libros**

- [*Learning Spark*, 2.ª edición, código oficial](https://github.com/databricks/LearningSparkV2): la versión actualizada del libro que recomienda el docente (Databricks la regala; conflicto de interés).
- [*Designing Data-Intensive Applications*, 2.ª edición (Kleppmann y Riccomini, 2026)](https://martin.kleppmann.com/2026/03/24/designing-data-intensive-applications-2e.html): el mejor libro para entender por qué los sistemas distribuidos son como son; salió en marzo de 2026.

**Documentación de Spark**

- [Guía de programación de RDD](https://spark.apache.org/docs/latest/rdd-programming-guide.html): transformaciones, acciones y persistencia con ejemplos.
- [Rendimiento de Spark SQL (cache, broadcast, AQE)](https://spark.apache.org/docs/latest/sql-performance-tuning.html): lo que conviene leer antes de tunear nada.
- [Guía de tuning](https://spark.apache.org/docs/latest/tuning.html): serialización, memoria y paralelismo.
- [Spark Connect](https://spark.apache.org/docs/latest/spark-connect-overview.html): cómo usar Spark desde un cliente liviano.
- [Notas de Spark 4.0.0](https://spark.apache.org/releases/spark-release-4-0-0.html) y [de Spark 4.2.0](https://spark.apache.org/releases/spark-release-4-2-0.html): qué cambia respecto de la 3.5 de la materia.
- [Guía de features de MLlib](https://spark.apache.org/docs/latest/ml-features.html): HashingTF, StringIndexer, PolynomialExpansion y el resto, con ejemplos.

**Alternativas de una sola máquina y de Python distribuido**

- ["Big Data is Dead", Jordan Tigani (MotherDuck, conflicto de interés)](https://motherduck.com/blog/big-data-is-dead/): el argumento en contra, contado por alguien que vendía big data.
- [Why DuckDB](https://duckdb.org/why_duckdb): qué es una base analítica dentro del proceso y por qué es rápida.
- [Documentación de Polars](https://docs.pola.rs/): DataFrames con optimizador y modo perezoso.
- [Documentación de Dask](https://docs.dask.org/en/stable/) y [de Ray](https://docs.ray.io/en/latest/ray-overview/index.html): para comparar con Spark desde Python.

**Formatos y grafos**

- [Delta Lake](https://docs.delta.io/latest/index.html) y [Apache Iceberg](https://iceberg.apache.org/): tablas con transacciones sobre Parquet.
- [Guía de usuario de GraphFrames](https://graphframes.io/04-user-guide/01-creating-graphframes.html), [motif finding](https://graphframes.io/04-user-guide/04-motif-finding.html) y ["GraphFrames is back!"](https://graphframes.io/05-blog/1000-graphframes-is-back.html): la documentación al día de la biblioteca de la clase 4.
- [Morone y Makse, *Nature* 2015](https://www.nature.com/articles/nature14604): el paper de la influencia colectiva (texto completo pago).

**Datos para dimensionar**

- [CERN, almacenamiento](https://home.cern/science/computing/storage) y [el exabyte de disco](https://home.cern/news/news/computing/exabyte-disk-storage-cern): cifras oficiales para el ejemplo de la clase.
- [Zaharia y otros en *;login:*](https://www.usenix.org/system/files/login/articles/zaharia.pdf): de dónde sale el "90% del tiempo en E/S".
