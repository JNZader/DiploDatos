# Apunte de estudio: Análisis Exploratorio y Curación de Datos (Diplodatos, FAMAF UNC, José Robledo y Ariel Wolfmann)

**Curso:** Análisis Exploratorio y Curación de Datos (en la página vieja de la materia figura como "Exploración y Curación de datos"), la segunda de las cinco materias obligatorias de la Diplomatura en Ciencia de Datos, Aprendizaje Automático y sus Aplicaciones de FAMAF (UNC), cohorte 2026. Viene después de Análisis y Visualización de Datos · Docentes: José Ignacio Robledo (clases 1 y 2: datos faltantes, imputación, sesgos, encodings, PCA y transformaciones) y Ariel Mauricio Wolfmann (clases 3 y 4: el panorama de los roles y los proyectos de datos, recolección, calidad, formatos, SQL, combinación de datasets, ETL y arquitectura). En las clases 3 y 4 los dos están juntos y José interviene seguido · Coordinación: Carolina Chavero · Formato: cuatro clases sincrónicas por Meet, grabadas en 9 videos no listados del canal FAMAF UNC: viernes 24 de abril a la tarde, sábado 25 de abril a la mañana, viernes 8 de mayo a la tarde y sábado 9 de mayo a la mañana de 2026.
**De qué va:** es la materia de "los datos antes del modelo". La primera mitad trata de qué hacer cuando los datos vienen sucios: datos erróneos y faltantes, los mecanismos MCAR, MAR y MNAR, cómo explorarlos con pandas y missingno, cuándo tirar y cuándo imputar (constante, regresión, KNN, MICE, imputación múltiple), los sesgos, cómo pasar categorías a números (one hot, ordinal), cómo reducir dimensiones con PCA y cómo escalar o transformar variables. La segunda mitad es ingeniería de datos: qué hace cada rol (analytics, data science, ML, data engineering), cómo es el ciclo de un proyecto, de dónde salen los datos, calidad, privacidad y gobernanza, formatos (CSV, JSON, Parquet, Avro, Iceberg), bases relacionales, NoSQL y vectoriales, SQL desde Python, cómo combinar datasets sin explotar la cardinalidad y cómo se arma un ETL con su arquitectura (data warehouse, data lake, medallion, Airflow). El dataset que atraviesa todo es Melbourne Housing Snapshot (13.580 propiedades), y en la última clase se cruza con los avisos de Airbnb de Melbourne. Se aprueba con dos entregables grupales en notebooks.

> Nota: este apunte sale de los subtítulos automáticos en español de los 9 videos (los 9 tenían subtítulos de la grabación, no hizo falta transcribir con whisper). También usé el repositorio público de la materia, `DiploDatos/AnalisisYCuracion`, pero **ojo: es la versión 2022** (último commit del 11/05/2022; el README dice "Exploración Y Curación de Datos 2022"). Las notebooks 2026 están en el aula virtual, que no es pública. Las notebooks de Ariel (exploración, SQL, combinación, ETL) son casi las mismas que las de 2022; las de José (faltantes, encodings, PCA, transformaciones) se parecen a las de Clase3 y Clase4 de 2022 pero no son idénticas. Bajé los CSV que usa el repo desde el servidor de FAMAF (`cs.famaf.unc.edu.ar/~mteruel/datasets/diplodatos/`) y corrí el código contra esos datos. Muchos nombres vienen deformados en la transcripción (ver el glosario al final). Cuando lo que se dijo está mal o es impreciso, lo marco como **Corrección**. Las cifras, fechas y afirmaciones que no pude chequear van como **dudoso** o **para verificar**. Lo que dice "verificado en el box" lo comprobé corriendo código (los scripts están en la guía de implementación).

**Cómo leer los links:** cada link dice el video y el minuto. "C2P2 1:23:45" es la clase 2, parte 2, en la hora 1, minuto 23, segundo 45.

## Los 9 videos

| # | Id | Video | Contenido | Duración | Link |
|---|---|---|---|---|---|
| 1 | — | C1P1: "Clase 1 AEyCD PARTE1" (viernes 24/04/2026, tarde) | Presentación, cursada, datos ruidosos, erróneos y faltantes, MCAR, MAR y MNAR | 50:59 |  |
| 2 | — | C1P2: "CLASE 1 AEyCD parte 2" (24/04) | Colab, Series con NaN, None y pd.NA, Melbourne: info, describe, ceros, Bedroom2, crosstab, missingno | 1:31:58 |  |
| 3 | — | C1P3: "Clase 1 AEyCD PARTE3" (24/04, desde las 21) | Eliminar o imputar, constante, regresión, KNN, imputación múltiple, MICE | 54:01 |  |
| 4 | — | C2P1: "Clase 2 AEyCD PARTE 1" (sábado 25/04, 10 h) | Notebook de faltantes parte 2: dropna, isna, filtro por cuantiles, SimpleImputer, KNNImputer | 1:04:32 |  |
| 5 | — | C2P2: "Clase 2 AEyCD PARTE 2" (25/04, 11:30 a 14) | Sesgos, encodings (Adult), PCA (Iris), escalado y transformaciones, entregable 1 | 2:32:40 |  |
| 6 | — | C3P1: "Clase 3 AEyCD" (viernes 08/05, tarde) | Cierre de dudas con José; Ariel: roles, data products, ciclo de un proyecto, ética; mentorías | 2:04:52 |  |
| 7 | — | C3P2: "Clase 3 AEyCD segunda parte" (08/05, desde las 20:30) | Evaluación, despliegue, monitoreo, recolección, tipos de datos, privacidad, calidad, formatos, bases de datos, RAG | 1:07:29 |  |
| 8 | — | C4P1: "Clase 4 AEyCD" (sábado 09/05, 10 h) | Notebook de exploración de Melbourne, SQL (SQLite, SQLAlchemy), groupby, join y merge | 1:36:05 |  |
| 9 | — | C4P2: "Clase 4 AEyCD segunda parte" (09/05, 12 h) | Combinación Melbourne y Airbnb, ETL y ELT, data warehouse y data lake, Airflow, medallion, entregable 2 | 1:38:45 |  |

Duración total: 13:21:21.

**Cómo se determinó el orden.** Los títulos traen el número de clase y de parte, pero no la fecha. Las clases 1 y 2 se subieron el 28/04/2026 y las 3 y 4 el 12/05/2026, y el calendario público de la diplomatura pone esta materia el 24 y 25 de abril y el 8 y 9 de mayo. El contenido encadena sin huecos. En C1P1 José dice "hoy hasta las 22, mañana de 10 a 14, y las siguientes clases el 8 y 9 de mayo" C1P1 8:24 y corta al recreo C1P1 50:00; C1P2 retoma con la notebook de faltantes y corta "pausa hasta las 21" C1P2 1:31:22; C1P3 sigue con el tratamiento de faltantes y cierra con "mañana a las 10" C1P3 53:31. C2P1 abre con el aviso de que las grabaciones van a una carpeta de Drive y el link arreglado de la notebook C2P1 0:04 y corta "pausa hasta las 11:30; sigue sesgos" C2P1 1:03:49; C2P2 arranca con sesgos C2P2 1:18 y cierra la parte de José anunciando que "desde mayo" sigue Ariel C2P2 2:31:20. C3P1 empieza con José respondiendo dudas del entregable 1 y moviendo la entrega al 14 de mayo C3P1 11:05, sigue Ariel y corta "hasta las 20:30" C3P1 2:04:08; C3P2 es la segunda parte de esa noche y cierra con "mañana a las 10, notebooks" C3P2 1:07:03. En C4P1 Ariel recapitula "lo del viernes" C4P1 0:02 y corta al recreo "hasta las 12" C4P1 1:35:12; C4P2 sigue con la combinación de datasets y cierra la materia C4P2 1:37:13.

## Mapa de módulos y videos

| Módulo | Dónde se ve |
|---|---|
| 0. La materia: equipo, cursada, herramientas | C1P1 (inicio), C1P2 (inicio), C2P1 (inicio), C3P1 (inicio y final) |
| 1. Datos ruidosos, erróneos y faltantes; MCAR, MAR y MNAR | C1P1 |
| 2. Faltantes en pandas: NaN, None, pd.NA, isna e isnull | C1P2, C2P1, C4P1 |
| 3. Explorar un dataset: Melbourne con pandas y missingno | C1P2, C4P1 |
| 4. Tirar o imputar: técnicas de imputación | C1P3, C3P1 (inicio) |
| 5. Imputación con scikit-learn (notebook de faltantes, parte 2) | C2P1 |
| 6. Sesgos | C2P2 |
| 7. Codificación de variables categóricas | C2P1 (final), C2P2 |
| 8. Reducción de dimensionalidad con PCA | C2P2 |
| 9. Escalar, normalizar, estandarizar y transformar | C2P2 |
| 10. Roles, productos de datos y ciclo de un proyecto | C3P1, C3P2 |
| 11. Recolección, tipos de datos, privacidad, gobernanza y calidad | C3P2 |
| 12. Ingesta, formatos y bases de datos (relacionales, NoSQL, vectoriales, RAG) | C3P2, C4P1 (inicio) |
| 13. SQL desde Python | C4P1, C4P2 (inicio) |
| 14. Combinar datasets: groupby, join, merge y cardinalidad | C4P1 (final), C4P2 |
| 15. ETL, orquestación y arquitectura de datos | C4P2 |
| 16. Los entregables | C1P1, C2P2, C3P1, C4P2 |

---

## 0. La materia: equipo, cursada, herramientas
**Dónde:** C1P1 0:02, C1P1 1:10, C1P1 6:43, C1P1 8:24, C1P2 1:40, C2P1 0:04, C3P1 12:10, C3P1 1:53:14

### Conceptos clave
- **Quiénes.** Abre Carolina Chavero ("Caro"), la coordinadora, que presenta a los dos docentes C1P1 0:02. José Ignacio Robledo se presenta como licenciado y doctor en física por FAMAF, con posdoctorados en Bariloche y Alemania, investigador de CONICET en el Centro Atómico Bariloche, docente del Instituto Balseiro y, hasta noviembre de 2025, consultor de IA en el Jülich Supercomputing Centre C1P1 6:43; más adelante cuenta que también tiene una maestría en estadística C1P1 39:59. Ariel Mauricio Wolfmann se presenta en la clase 3: computador de FAMAF, con años en la industria de datos y ML y en startups, y hoy "director de ingeniería, plataforma, toda la parte de data" en Yalo, una empresa de comercio conversacional C3P1 12:10.
- **Cursada.** Cuatro horas por clase con pausas. Todo el material (diapositivas, notebooks, ejercicios extra no obligatorios) está en el aula virtual, con link fijo de Meet C1P1 1:10. Hay un canal de Slack de la materia C1P1 5:04. Las grabaciones se comparten en una carpeta de Drive C2P1 0:04.
- **Estructura.** Tres componentes: curación, análisis exploratorio y ETL (extracción, transformación y carga) C1P1 10:01. José da EDA y curación (clases 1 y 2) y Ariel ETL e ingeniería de datos (clases 3 y 4) C1P1 8:24. Ariel aclara que este año el orden quedó al revés de lo ideal (lo conceptual al final) por logística C4P1 0:02.
- **Colab.** Se trabaja en Google Colab: "Conectar" da una máquina con unos 12 GB de RAM y 107 GB de disco; se puede pedir GPU o TPU con límites; con `!` se corren comandos de shell, por ejemplo `!pip install` C1P2 1:40. En cada sesión nueva hay que reinstalar los paquetes que no vienen C4P1 57:56.
- **Leer la documentación.** Los dos insisten en leer la documentación de pandas y scikit-learn en vez de pedirle todo a un chatbot C1P2 11:02, C3P1 23:43. Ariel: "usemos la IA para aprender y no para evitar aprender" C3P1 24:15.
- **Mentorías.** Al final de la clase 3 Carolina presenta las mentorías (coordinan Yanina Iberra y Luis Biedma): 18 proyectos con 18 mentores, dos grupos de 4 por mentor, se eligen 3 opciones, unos cuatro meses desde junio, video final de 10 a 15 minutos y presentación la primera semana de diciembre C3P1 1:53:14.

### Correcciones y matices
- **para verificar:** José dice que JUPITER, la supercomputadora de Jülich, es "la cuarta más grande del mundo" C1P1 7:18. Era cierto cuando la inauguraron (cuarta en las listas TOP500 de junio y noviembre de 2025), pero en la lista de junio de 2026 bajó al quinto puesto. Sigue siendo la primera exaescala de Europa.
- **para verificar:** el cargo de Ariel. En clase dice "director de ingeniería, plataforma, data" en Yalo C3P1 13:16; la página oficial del equipo docente lo lista como "VP de tecnología y datos, Lic. en Cs. de la Computación".
- **Matiz:** el canal de Slack se nombra con una sigla que la transcripción deforma ("EICD"); seguramente es el de AEyCD C1P1 5:04.

### Preguntas de repaso
1. ¿Qué tres componentes tiene la materia y quién da cada parte?
2. ¿Por qué conviene leer la documentación aunque tengas un chatbot a mano?

## 1. Datos ruidosos, erróneos y faltantes; MCAR, MAR y MNAR
**Dónde:** C1P1 11:09, C1P1 16:42, C1P1 18:19, C1P1 21:42, C1P1 25:00, C1P1 29:21, C1P1 32:08, C1P1 33:19, C1P1 37:10, C1P1 45:34

### Conceptos clave
- **Ruido.** Todo lo que contamina el mensaje. Los alumnos aportan qué provoca: resultados engañosos, patrones ocultos, sesgos, errores. José remarca que lo que se cura hoy entrena los modelos de mañana C1P1 16:42.
- **Taxonomía.** Un dato **erróneo** puede ser *atípico* (un 99 donde debería ir un 9; ojo, no todo atípico es un error, puede ser solo poco probable) o *mal codificado* (una fecha guardada como texto) C1P1 18:19. Un dato **faltante** puede ser *perdido* (se sobrescribió, se borró una columna) o *inexistente* (nunca se midió, como las etiquetas de clase que nadie cargó) C1P1 20:34.
- **Qué hacer con los erróneos.** Corregir la codificación, tirarlos (caro, porque muchos modelos dependen de la cantidad de datos) o modelarlos C1P1 21:42. Se puede probar varias estrategias y combinarlas, que es la idea de la imputación múltiple C1P1 24:26. Las decisiones posibles: retirar atípicos, retirar mal codificados o registrarlos y no tocarlos C1P1 28:46.
- **Documentación y metadata.** Un diccionario de datos cuesta horas y plata, pero sin él no se puede curar bien. José menciona los principios FAIR C1P1 25:00.
- **Faltantes en la práctica.** Se pueden imputar, no usar o dejar como NaN ("not a number") en pandas. Lo peligroso es la codificación con un valor atípico, como 9999, si no está documentada C1P1 29:21.
- **Predecir vs imputar.** Predecir es estimar un valor que no se muestreó; imputar es sustituir un valor que falta. A veces es la misma operación C1P1 31:35.
- **Mecanismos (Rubin).** **MCAR** (missing completely at random): la falta no se relaciona con ninguna característica, observada o no; es el caso ideal C1P1 33:54. **MAR** (missing at random): la falta depende solo de variables observadas C1P1 35:34. **MNAR** o NMAR (missing not at random): la falta depende de algo no observado, incluido el propio valor que falta; cualquier cosa que hagas introduce sesgo C1P1 35:34.
- **El ejemplo de la tabla.** Con una variable V1 (categorías A, B, C) y una V2 ordenada de menor a mayor: si faltan valores sueltos al azar es MCAR C1P1 37:45; si faltan todos los de la categoría B es MAR, como cuando "Pedro no cargó sus datos" en un ensayo agronómico C1P1 40:34, C1P1 43:18; si faltan siempre los dos valores más chicos de cada grupo es MNAR C1P1 44:26. Imputar con una constante rompe la correlación entre variables C1P1 44:59.
- **Para qué sirve la clasificación.** No se puede probar del todo qué mecanismo hay, pero ordena el razonamiento: casi todos los métodos de imputación suponen MCAR o MAR C1P1 47:49. Con MNAR José sugiere eliminar la variable o al menos documentarlo C1P1 46:41.

### Correcciones y matices
- **Corrección:** José dice "FAIR: F, accessible, reproduce y no me acuerdo" C1P1 27:09. FAIR significa **Findable, Accessible, Interoperable, Reusable** (localizable, accesible, interoperable, reutilizable), de Wilkinson y otros, *Scientific Data*, 2016.
- **para verificar:** "el paper de Rubin de 1978" C1P1 32:08. La definición de MCAR y MAR es de Rubin, "Inference and missing data", *Biometrika*, 1976. Las "reglas de Rubin" para combinar imputaciones son del libro *Multiple Imputation for Nonresponse in Surveys* (1987). De 1978 hay un trabajo de Rubin sobre imputación múltiple en encuestas, así que puede que se refiera a ese.
- **para verificar:** el libro abierto sobre faltantes "en R" que José promete subir al Slack C1P1 12:16 es probablemente *Flexible Imputation of Missing Data*, de Stef van Buuren, que está libre en línea.
- **Matiz:** MAR no quiere decir "sin patrón". Es sistemático, pero respecto de una variable que sí observaste, y por eso se puede corregir condicionando en ella C1P1 45:34.

### Preguntas de repaso
1. Das una encuesta y las personas con sueldos altos no contestan el sueldo. ¿Qué mecanismo es?
2. ¿Por qué imputar con una constante rompe la correlación entre dos variables?
3. ¿Qué significa cada letra de FAIR?

## 2. Faltantes en pandas: NaN, None, pd.NA, isna e isnull
**Dónde:** C1P2 14:23, C1P2 17:42, C1P2 19:59, C1P2 21:38, C1P2 23:52, C2P1 14:42, C2P1 20:13, C4P1 32:40, C4P1 35:36

### Conceptos clave
- **Series y tipos.** `pd.Series([5, 2, 3])` es entera; si metés un `3.0` pasa toda a float C1P2 14:23, C1P2 16:02. Si asignás `np.nan` a un elemento, la columna pasa a `float64` y muestra `NaN` C1P2 17:42. Con `astype("Int64")` (con I mayúscula: el entero que admite nulos) vuelve a entera y el faltante se muestra como `<NA>` C1P2 18:50.
- **Strings.** En una Series de texto (dtype object) `None` queda como `None` y `np.nan` como `NaN` C1P2 19:59.
- **Comparaciones.** `None == None` da `True`, `np.nan == np.nan` da `False` y `pd.NA == pd.NA` da `<NA>` C1P2 21:38. Por eso nunca se buscan faltantes con `==`: se usa `isna()`. Si buscás solo `None` te salteás los `NaN` C1P2 26:08.
- **Qué usar.** José recomienda lo que propone cada paquete: `pd.NA` en pandas y `np.nan` en numpy C1P2 24:26.
- **mean() saltea los NaN.** Divide por la cantidad de valores no faltantes C2P1 15:16.
- **isna e isnull.** `df.isnull().sum()` cuenta faltantes por columna C2P1 22:34.

### Correcciones y matices
- **Corrección:** José explica que `np.nan` no es igual a sí mismo "porque son instancias distintas en memoria" C1P2 22:45. No es así: `np.nan` es un único objeto (`np.nan is np.nan` da `True`). NaN es distinto de todo, incluso de sí mismo, porque lo define así el estándar de punto flotante IEEE 754. `pd.NA` usa lógica de tres valores (Kleene): comparar con un desconocido da desconocido. Verificado en el box.
- **Corrección:** en la clase 2 José dice que `isnull` mira NaN, None y NaT y que `isna` mira `pd.NA`, "isnull es un poco más amplio" C2P1 21:21. En la clase 4 Ariel dice que "son ligeramente distintos, por algo son dos métodos" C4P1 32:40, y José muestra la documentación: "es exactamente lo mismo, lo han unificado, esto es nuevo" C4P1 35:36. Lo correcto: **`isnull` es un alias de `isna`**, hacen exactamente lo mismo (igual que `notnull` y `notna`). Tampoco es nuevo: `isna` se agregó en pandas 0.21 (2017) como nombre alternativo de `isnull`, que existía desde antes. Verificado en el box con pandas 3.0.6: la documentación de `DataFrame.isnull` arranca con "DataFrame.isnull is an alias for DataFrame.isna", el código de `isnull` es literalmente `return self.isna()`, y sobre una tabla con NaN, None, NaT y `pd.NA` los dos dan exactamente lo mismo.
- **Matiz:** lo de que en una Series de texto `None` queda como `None` C1P2 19:59 vale para el dtype `object`, que es lo que da pandas 2 (la versión de Colab en abril de 2026, **para verificar**). En pandas 3 el texto usa por defecto el dtype `str` y tanto `None` como `np.nan` se guardan como `NaN`. Verificado en el box.
- **Matiz:** `info()` y `isna()` detectan `None`, `NaN`, `NaT` y `pd.NA`, pero no los códigos centinela como -1 o 9999; esos hay que convertirlos a mano C1P2 36:05.

### Preguntas de repaso
1. ¿Por qué una columna entera pasa a float cuando le aparece un NaN, y cómo lo evitás?
2. ¿Qué devuelve `pd.NA == pd.NA` y por qué?
3. ¿Qué diferencia hay entre `isna` e `isnull`?

## 3. Explorar un dataset: Melbourne con pandas y missingno
**Dónde:** C1P2 26:40, C1P2 33:53, C1P2 42:03, C1P2 46:27, C1P2 54:42, C1P2 1:00:58, C1P2 1:11:02, C1P2 1:16:10, C1P2 1:19:35, C1P2 1:24:05, C4P1 24:41, C4P1 27:01, C4P1 36:46, C4P1 42:24, C4P1 44:34, C4P1 52:14, C4P1 59:01

### Conceptos clave
- **El dataset.** Melbourne Housing Snapshot, de Kaggle (la versión reducida de Dan Becker), con una copia en un servidor de FAMAF: 13.580 filas y 21 columnas C1P2 26:40, C1P2 28:52. Tiene propiedades vendidas con suburbio, dirección, ambientes (`Rooms`), tipo, precio, método de venta, vendedor, fecha, distancia al centro, código postal, dormitorios (`Bedroom2`), baños, cocheras (`Car`), superficie del terreno (`Landsize`) y construida (`BuildingArea`), año de construcción, municipio (`CouncilArea`), coordenadas y región.
- **Primeras miradas.** `.info()` da el índice, las columnas, la cuenta de no nulos y el dtype de cada una, y la memoria C1P2 33:53. `.describe()` da count, media, desvío, mínimo, cuartiles y máximo: `Rooms` va de 1 a 10 con mediana 3 y media 2,94; `Landsize` tiene mínimo 0, sospechoso C1P2 42:03, C1P2 44:13. La tabla interactiva con filtros que aparece es de Colab, no de pandas C1P2 40:23.
- **Ayuda y muestras.** `df.sample?` o `help(df.sample)` muestran la documentación C1P2 46:27. `sample(n=20, random_state=...)` saca una muestra reproducible; José compara el describe de la muestra con el del total C1P2 50:15, C1P2 53:04.
- **Condiciones lógicas.** `==`, `!=`, `>=`, `&`, `|`, siempre entre paréntesis. `df[df == 0].count()` cuenta ceros por columna: Distance 6, Bedroom2 16, Bathroom 34, Car 1026 C1P2 54:42, C1P2 57:29. Error común: no guardar el resultado de una operación C1P2 59:48.
- **El caso Bedroom2 = 20.** Hay una casa con 3 ambientes y 20 dormitorios C1P2 1:03:43. ¿Corregir a 2 o borrar? Corregir ya es modelar; José probaría con y sin, y en este caso la tiraría (es 1 en 13.580) C1P2 1:08:46.
- **crosstab.** `pd.crosstab(df.Rooms, df.Bedroom2)` sale casi diagonal: Bedroom2 parece la misma información que Rooms, sacada de otra fuente por scraping, y aporta multicolinealidad C1P2 1:11:02. La de Rooms contra Bathroom no es diagonal y por eso es más informativa C1P2 1:19:35. Una crosstab no sirve para variables continuas C1P2 1:14:29.
- **Nunca sobre el original.** Trabajar sobre `df.copy()` C1P2 1:16:10. Para marcar valores imposibles como faltantes: `df.loc[cond, "Bathroom"] = pd.NA` y comparar el describe antes y después C1P2 1:21:14.
- **missingno.** `msno.bar` cuenta no nulos por columna; `msno.matrix` pinta en blanco los faltantes (un patrón ordenado sugiere MAR, uno disperso MCAR); `msno.heatmap` muestra la correlación de nulidad: `BuildingArea` y `YearBuilt` faltan juntas C1P2 1:24:05, C1P2 1:30:15.
- **La versión de Ariel (clase 4).** Con la notebook de exploración del repo: `info()`, `describe()`, `isnull().sum()` (Car 62, BuildingArea 6.450) C4P1 29:45, C4P1 31:32; `nunique()`: Address 13.378 (texto casi único), Suburb 314, Regionname 8, Method 5, Type 3, Date 58 C4P1 38:29. Columnas con una sola categoría, o con 99,9% de una, no aportan C4P1 39:34. El objetivo es estimar el precio, que tiene cola larga C4P1 36:46.
- **Gráficos.** Boxplot de precio por región C4P1 42:24, heatmap de correlaciones (Bedroom2 y Rooms casi 1) C4P1 44:34, correlación con Price (Rooms, Bedroom2, Bathroom) C4P1 52:14. Postcode sirve para combinar con otros datasets; de la fecha se pueden sacar mes, año, trimestre C4P1 52:46. Hay perfiladores automáticos como ydata-profiling para contrastar C4P1 55:41.
- **Correlación entre categóricas.** José: tabla de contingencia y prueba chi cuadrado de independencia C4P1 59:01.

### Correcciones y matices
- **Matiz:** José dice que la línea a la derecha de `msno.matrix` "muestra la cantidad de datos faltantes que tiene cada caso" C1P2 1:27:54. Es el sparkline de completitud: muestra cuántos valores **no nulos** tiene cada fila, con el mínimo y el máximo anotados.
- **Corrección:** Ariel dice que la desviación estándar de Rooms "es de 0" C4P1 30:20. Es un desliz: da 0,956. Verificado en el box (media 2,937997, desvío 0,9557).
- **Corrección:** Ariel dice que "el CouncilArea tiene 1369" al leer `nunique` C4P1 38:29. CouncilArea tiene **33** categorías; 1.369 es la cantidad de **faltantes**, como el mismo Ariel dice bien un rato después ("council area tiene 1369 nulos") C4P1 51:11. Verificado en el box.
- **Corrección:** al describir el boxplot Ariel habla de "media y desviaciones estándar"; José lo corrige al toque C4P1 42:24. La caja va de Q1 a Q3 con la mediana adentro; los bigotes llegan al último dato dentro de 1,5 veces el rango intercuartil y los puntos de afuera se dibujan como outliers.
- **Corrección:** el Netflix Prize no se corrió en Kaggle, como duda Ariel C4P1 25:16: fue de 2006 a 2009 en un sitio propio de Netflix, y Kaggle se fundó en 2010 (Google la compró en 2017).
- **para verificar:** Ariel ubica Northern Metropolitan "en unos 2.500" C4P1 41:16; en el CSV del snapshot son 3.890 (Southern Metropolitan es la mayor, 4.695). Verificado en el box.

### Preguntas de repaso
1. ¿Qué te dice que la crosstab de Rooms contra Bedroom2 sea casi diagonal?
2. ¿Qué diferencia hay entre `msno.matrix` y `msno.heatmap`?
3. ¿Qué muestra exactamente un boxplot?

## 4. Tirar o imputar: técnicas de imputación
**Dónde:** C1P3 0:37, C1P3 3:25, C1P3 6:09, C1P3 8:20, C1P3 11:01, C1P3 13:45, C1P3 25:11, C1P3 36:19, C1P3 37:58, C1P3 41:18, C1P3 44:37, C1P3 49:30, C3P1 0:01

### Conceptos clave
- **Eliminar.** Si a una columna le faltan casi todos los datos (20 de 10.000), imputar 9.980 valores inventados no tiene sentido; como regla práctica José no usa una columna a la que le falte más del 50% C1P3 1:13, C1P3 2:20. Lo mismo para una fila a la que le faltan casi todas las variables. Eliminar no "sesga" por sí mismo si la decisión no se toma mirando el resultado del modelo C1P3 3:25.
- **Por qué imputar.** Muchos algoritmos no aceptan faltantes y descartan la fila entera: perdés 199 valores buenos por uno que falta C1P3 8:53. José cuenta que una red neuronal le dio NaN en la pérdida por 5 faltantes en 100.000 filas C3P1 2:16.
- **Imputación simple.** En tablas, una constante: media, mediana o moda, que coinciden en una normal y se separan en una asimétrica C1P3 11:34. En series de tiempo: forward fill, backward fill e interpolación lineal (con t = 3 y t = 5 imputás t = 4) o no lineal C1P3 3:57. Para enteros, moda o mediana C1P3 19:48.
- **El ejemplo animado.** Tres variables con relación lineal exacta. Imputar con la media da 29 (el real era 35), 7 (era 1) y 134 (era 80); una regresión ajustada con las filas completas recupera exactamente 35, 1 y 80 C1P3 13:45, C1P3 14:54, C1P3 23:00. Antes de imputar por regresión hay que mirar la correlación o el R² C1P3 16:32; más variables ayudan, pero cuidado con los grados de libertad (3 filas y 50 variables no sirve) C1P3 17:38. "Regresión lineal" es lineal en los parámetros: ax² + b también lo es C1P3 24:39.
- **KNN.** Para cada fila con faltantes busca los k vecinos más cercanos en el espacio de las variables (no en la tabla) y promedia C1P3 25:11, C1P3 27:56. Es costoso porque calcula distancias de todos contra todos C1P3 30:12. Se usan pocos vecinos, 3 a 5 C1P3 33:33. Para categóricas codificadas se vota por mayoría C1P3 35:12. El KNN común no reutiliza lo que ya imputó; los métodos iterativos sí C1P3 32:26.
- **MICE.** Iterativo: arranca imputando con la media y después regresa cada variable con faltantes contra las demás, una por vez y en ronda, hasta que converge C1P3 44:37. MissForest es la misma idea con random forest, y se puede usar cualquier modelo C1P3 47:22. Preserva mejor las correlaciones C1P3 48:26.
- **Imputación múltiple.** Se imputa varias veces, se analiza cada versión y se combinan los resultados con las reglas de Rubin, que suman la varianza dentro de cada imputación (within) y entre imputaciones (between) C1P3 41:18, C1P3 42:57.
- **¿Cuál usar?** No hay una receta. José propone repetir el análisis con varias técnicas y quedarse tranquilo si el resultado no depende de la imputación C1P3 8:20. Validar la imputación depende de qué análisis viene después C1P3 36:19. "Similar no significa que esté bien" C1P3 49:30.
- **¿Cuánto se puede imputar?** Mientras no cambie la distribución: imputar 1.000 de 2.000 con la media hace un pico enorme C1P3 37:58. Mucha gente no imputa más del 10 al 20%, aunque bien hecho se puede más en una variable C1P3 40:13, C3P1 0:34.
- **Datos que sabés que están mal.** En encuestas, pasarlos a NaN e imputarlos, documentando y sin perder el original; por ejemplo un 4,6 cargado como 46 C3P1 3:58, C3P1 5:37.

### Correcciones y matices
- **Corrección importante:** José describe la imputación múltiple como "agarrar subconjuntos del conjunto de datos e imputar en los subconjuntos; el método es el mismo, cambiamos solamente el subconjunto" C1P3 41:50, y lo repite al responder una pregunta C1P3 52:59. No es así. La imputación múltiple genera **m copias completas** del dataset, cada una imputada con valores **aleatorios** distintos sacados de la distribución predictiva de los faltantes (no la predicción puntual, sino predicción más ruido). Se corre el mismo análisis en cada copia y se combina con las reglas de Rubin: la estimación final es el promedio de las m estimaciones y la varianza total es T = W + (1 + 1/m) B, donde W es el promedio de las varianzas dentro de cada copia y B la varianza entre las estimaciones. Lo que José describe se parece más a bootstrap. Verificado en el box con `IterativeImputer(sample_posterior=True)`.
- **Matiz:** José traduce MICE como "imputación múltiple con ecuaciones encadenadas" C1P3 5:36. La sigla es **Multivariate Imputation by Chained Equations**. Usada con una sola imputación (como hace `IterativeImputer` por defecto) no es imputación múltiple; lo es cuando se repite m veces con muestreo aleatorio.
- **Matiz:** la diapositiva dice que con MNAR "no imputen, es mejor tirar esa variable" C1P3 7:15. Tirar también sesga cuando la falta depende del valor. Lo recomendado en la bibliografía es hacer análisis de sensibilidad (probar supuestos distintos sobre los faltantes), modelar el mecanismo o, como mínimo, agregar una columna indicadora de faltante.
- **Matiz:** a la pregunta de si KNN busca vecinos con filas completas José responde "sí" C1P3 28:29. El `KNNImputer` de scikit-learn usa la distancia `nan_euclidean`, que ignora las coordenadas faltantes y reescala; al vecino solo le exige tener la variable que se está imputando. Verificado en el box.

### Preguntas de repaso
1. En el ejemplo animado, ¿por qué la regresión recupera los valores exactos y la media no?
2. ¿Qué hace distinta a la imputación múltiple de imputar una vez con MICE?
3. Escribí las reglas de Rubin y explicá qué es B.

## 5. Imputación con scikit-learn (notebook de faltantes, parte 2)
**Dónde:** C2P1 4:44, C2P1 14:42, C2P1 15:50, C2P1 24:48, C2P1 27:33, C2P1 40:33, C2P1 42:13, C2P1 51:35, C2P1 57:37

### Conceptos clave
- **El servidor caído.** El servidor de FAMAF no respondía, así que bajaron el CSV de Kaggle (con el paquete `kagglehub`) y lo subieron a Colab arrastrándolo C2P1 4:44, C2P1 7:37. Ese archivo tiene 18.396 filas en vez de 13.580 C2P1 10:35, C2P1 50:31, así que todas las cifras de esta clase son de otro archivo.
- **dropna.** `dropna(subset=["Car"])` tira filas; con ese archivo quedan 14.820. José: "yo no haría eso" C2P1 15:50.
- **CouncilArea.** 2.587 faltantes y 33 valores; imputar un municipio es difícil y José la tira C2P1 24:48.
- **Filtro por cuantiles.** `df.hist()` muestra distribuciones muy asimétricas con outliers extremos C2P1 27:33. Se recorta con cuantiles en vez de con un valor fijo: el 99% de BuildingArea (465) y el 1% de YearBuilt (1880). El truco es conservar los faltantes: `(col < q99) | col.isnull()`; si no, el filtro los tira sin avisar C2P1 28:38, C2P1 32:01. José se confunde de signo con Landsize y lo corrige un alumno C2P1 36:29.
- **El patrón de scikit-learn.** Importar, instanciar, `fit_transform` C2P1 40:33. `SimpleImputer(strategy="constant", fill_value=0)` mete un pico en 0 que deforma los histogramas C2P1 42:13, C2P1 44:27. Con 999 se ve un outlier en YearBuilt, pero en Landsize no se nota porque 999 cae dentro de su rango C2P1 46:34. `fit_transform` devuelve un array de numpy, no un DataFrame C2P1 48:18.
- **KNNImputer.** Solo sobre columnas numéricas (`select_dtypes`), con `n_neighbors` y `weights="uniform"` o `"distance"` C2P1 51:35, C2P1 53:13. Los histogramas después de imputar se parecen a los de antes C2P1 57:07. Un loop con k de 1 a 4 da distribuciones casi iguales C2P1 57:37. Probar los métodos en una submuestra representativa ahorra tiempo C2P1 1:00:33.

### Correcciones y matices
- **para verificar:** cuál es el archivo de Kaggle de 18.396 filas. Probablemente es una versión anterior del mismo snapshot de Dan Becker; con el CSV del servidor de FAMAF (13.580 filas) las cifras cambian: Car tiene 62 faltantes, BuildingArea 6.450, CouncilArea 1.369 y el cuantil 99 de BuildingArea da 466,42 en vez de 465. El cuantil 1 de YearBuilt sí da 1880. Verificado en el box con el CSV de 13.580 filas.
- **Matiz:** José dice que un subconjunto con condición "ya es otro objeto, no hace falta copy" C2P1 39:25. En pandas viejo eso podía dar `SettingWithCopyWarning`; con copy on write (por defecto desde pandas 3) es seguro, pero un `.copy()` explícito no cuesta nada y deja clara la intención.
- **Matiz:** el KNN se corre sobre las columnas sin escalar. La distancia la dominan las variables de mayor escala (Landsize, Price) y los vecinos salen casi solo por esas. Conviene estandarizar antes de imputar y volver a la escala original después. Verificado en el box: cambian los valores imputados.
- **Matiz:** para no perder los nombres de columnas podés usar `set_output(transform="pandas")` en el imputador, en vez de reconstruir el DataFrame a mano por índice de columna (José se confunde de orden justamente así C2P1 53:47).

### Preguntas de repaso
1. ¿Por qué el filtro por cuantil lleva `| col.isnull()`?
2. ¿Qué problema tiene imputar con KNN sin escalar?

## 6. Sesgos
**Dónde:** C2P2 1:18, C2P2 3:32, C2P2 8:05, C2P2 12:29, C2P2 16:51, C2P2 20:06, C2P2 21:42, C2P2 23:55

### Conceptos clave
- **Sesgo estadístico.** Sesgo(θ̂) = E[θ̂] − θ: cuánto se equivoca en promedio un estimador C2P2 1:18.
- **Sesgo en ML.** Error sistemático del modelo. El error cuadrático medio se descompone en sesgo² más varianza; dilema sesgo varianza y el dibujo de las dianas C2P2 3:32, C2P2 5:16.
- **Tipos.** De selección, de información, de respuesta (una encuesta de café y salud cardiovascular), de medición (tres cintas métricas distintas, un supervisor con preferencias) y de publicación (el efecto cajón: lo que no da significativo no se publica) C2P2 8:05, C2P2 9:44, C2P2 10:50, C2P2 11:55.
- **Datasets generados automáticamente.** Omisión de variables, deriva del sistema (un cambio de horario), contenido social con estereotipos, sesgo de respuesta u opinión en redes y tiendas, y retroalimentación (modelos generativos que se entrenan con lo que ellos mismos produjeron) C2P2 12:29.
- **Muestreo.** Autoselección, área específica, exclusión ("a la gente le gusta responder encuestas: 99,8%") C2P2 16:51. Supervivencia: los aviones de la Segunda Guerra que volvían con agujeros; hay que blindar donde no hay agujeros, porque los que recibieron ahí no volvieron C2P2 18:27. Selección previa: preguntar por escrito "¿sabés leer?" C2P2 19:34.
- **Casos.** Un sistema del gobierno de Países Bajos para detectar fraude que usaba como factores de riesgo tener nacionalidad extranjera y bajos ingresos C2P2 20:06; estadísticas de criminalidad de EE. UU. de 1900 a 1940 con documentación sesgada C2P2 21:10; un chatbot de 2016 para jóvenes de 18 a 24 que un ataque coordinado llenó de odio y hubo que cancelar C2P2 21:42.
- **Prevención.** Planificar el protocolo, tener un objetivo claro, capacitar, calibrar instrumentos, definir población y marco de muestreo, usar pesos, evitar el muestreo de conveniencia y seguir a los que no responden C2P2 23:55. En el procesamiento: faltantes mal tratados, mezclar cortes temporales, escalar mal y seleccionar datos a dedo también sesgan C2P2 27:13.

### Correcciones y matices
- **Matiz:** José dice que el promedio como estimador de μ tiene sesgo que "se hace cero a medida que aumentamos n" C2P2 2:24. El promedio es **insesgado para cualquier n**: E[X̄] = μ siempre. Lo que mejora al crecer n es la varianza (consistencia). Un ejemplo de sesgo que se va con n es la varianza muestral que divide por n en vez de n − 1.
- **Matiz:** la descomposición del ECM que muestra es sesgo² + varianza C2P2 4:05. Para el error de predicción falta el **ruido irreducible** σ²: ECM = sesgo² + varianza + σ².
- **para verificar:** el caso de Países Bajos C2P2 20:06 es el escándalo de los subsidios por cuidado infantil (toeslagenaffaire): el fisco usó un modelo de riesgo que incluía la nacionalidad, miles de familias fueron acusadas falsamente de fraude y el gobierno renunció en enero de 2021. José lo fecha en 2013, que es cuando empezó a usarse el sistema.
- **Matiz:** el chatbot de 2016 que no nombra es Tay, de Microsoft, que duró menos de un día.
- **Corrección:** José dice que la IA "viene de los 80, inclusive Turing" C2P2 22:14. El artículo de Turing sobre máquinas pensantes es de 1950 y el término "inteligencia artificial" es de 1956 (la conferencia de Dartmouth). En los 80 hubo el auge de los sistemas expertos.
- **Matiz:** el ejemplo de los aviones es de Abraham Wald, aunque José no lo nombra C2P2 18:27.

### Preguntas de repaso
1. ¿Por qué el promedio es insesgado pero igual mejora con n?
2. Dá un ejemplo de sesgo de supervivencia en datos de una empresa.

## 7. Codificación de variables categóricas
**Dónde:** C2P1 1:01:39, C2P2 28:53, C2P2 31:36, C2P2 32:44, C2P2 35:32, C2P2 38:50, C2P2 40:03, C2P2 44:37, C2P2 52:22

### Conceptos clave
- **Por qué.** Los algoritmos clásicos piden números. Al codificar hay que cuidar qué distancia inducís: −1, 0 y 1 para "menor, igual, mayor" tiene sentido; numerar barrios no C2P1 1:01:39, C2P2 31:36. Los embeddings son otra forma de codificar C2P2 32:10.
- **One hot.** Una columna binaria por categoría; con k − 1 columnas alcanza porque la última se deduce. Ejemplo con barrios de Córdoba (San Vicente, Cerro de las Rosas, Maipú) y la matriz esparsa resultante C2P2 32:44, C2P2 34:24. Es reversible C2P2 56:44. Con muchas categorías aparece la maldición de la dimensionalidad C2P2 38:18.
- **Codificar 1, 2, 3.** Introduce un orden y distancias falsas: "Maipú está a 2 de San Vicente" no significa nada C2P2 35:32.
- **Ordinal.** Cuando las categorías sí tienen orden, como el nivel educativo C2P2 38:50.
- **El dataset Adult.** Datos del censo de EE. UU. (UCI), 48.842 instancias en total; el archivo que carga la notebook es el de entrenamiento, con 32.561 filas C2P2 40:03, C2P2 42:19. Los faltantes vienen como "?" y pandas no los ve como nulos C2P2 41:43, C2P2 42:53. `education` tiene 16 categorías C2P2 43:29.
- **OrdinalEncoder.** `OrdinalEncoder(categories=[orden])` con el orden explícito de los niveles educativos; devuelve float64, que conviene pasar a entero C2P2 44:37, C2P2 46:53. Si imputás con KNN te puede dar 12,5 y hay que redondear C2P2 47:58. Los saltos entre niveles no son parejos (años de estudio) C2P2 48:31.
- **get_dummies.** `pd.get_dummies(df.race, drop_first=True)` y `pd.concat(axis=1)` para pegarlo; trabajar sobre copias y elegir entre `drop(..., inplace=True)` o reasignar C2P2 52:22, C2P2 55:09, C2P2 58:28.

### Correcciones y matices
- **Corrección:** José dice que Adult fue "extraído por Barry Becker de la base del Sens Soccer, una empresa de 1994" C2P2 40:03. Es la base del **Censo de EE. UU. de 1994** (US Census Bureau): la transcripción deformó "Census". La extracción fue de Barry Becker y la donaron Ronny Kohavi y Barry Becker a UCI en 1996.
- **Matiz:** en `adult.data` los valores vienen separados por coma y espacio, así que el faltante es `" ?"` con un espacio adelante. Si leés con `na_values="?"` solo, no los detecta; hay que usar `skipinitialspace=True` o `na_values=" ?"`. Verificado en el box: con `skipinitialspace=True` aparecen 1.836 faltantes en workclass, 1.843 en occupation y 583 en native-country.
- **Matiz:** scikit-learn tiene `OneHotEncoder(drop="first", handle_unknown=...)`, que a diferencia de `get_dummies` recuerda las categorías vistas en el entrenamiento y sirve dentro de un pipeline.

### Preguntas de repaso
1. ¿Por qué no codificar barrios como 1, 2, 3?
2. ¿Cuándo usarías `drop_first=True`?
3. ¿Por qué `na_values="?"` no alcanza con `adult.data`?

## 8. Reducción de dimensionalidad con PCA
**Dónde:** C2P2 1:00:40, C2P2 1:03:29, C2P2 1:05:10, C2P2 1:10:41, C2P2 1:15:03, C2P2 1:17:51, C2P2 1:22:12, C2P2 1:27:12, C2P2 1:38:16, C2P2 1:45:27

### Conceptos clave
- **Para qué.** Pasar de una matriz n × m a una n × d con d mucho menor que m C2P2 1:00:40. Se buscan los ejes de máxima varianza C2P2 1:03:29.
- **Pasos.** Centrar (y opcionalmente dividir por el desvío), calcular la matriz de covarianza (o de correlación si estandarizaste), sacar autovalores y autovectores y proyectar los datos sobre los autovectores C2P2 1:03:29. Hay m componentes ordenadas por varianza; la reducción ocurre al quedarte con las primeras, por ejemplo las que explican el 90%, o con el criterio del codo C2P2 1:05:10, C2P2 1:10:08, C2P2 1:25:33.
- **Geometría.** En 2D, PC1 es la dirección de máxima varianza y PC2 la ortogonal C2P2 1:10:41. Lo esencial es centrar; dividir por el desvío es una decisión aparte, necesaria si las variables están en escalas distintas C2P2 1:21:39. Se pierde interpretabilidad física, pero es reversible C2P2 1:22:12.
- **Iris.** 150 flores, 4 medidas, 3 especies C2P2 1:27:47. `sns.pairplot(hue="label")` muestra que las medidas de pétalo separan muy bien las especies C2P2 1:32:15. Con dos variables estandarizadas la varianza explicada da 55,87% y 44,12% C2P2 1:39:55. Con las cuatro estandarizadas: 72,96%, 22,85%, 3,67% y 0,52% C2P2 1:46:34. `x_reduced[:, :2]` se queda con las dos primeras, y un gráfico 3D de plotly muestra la proyección C2P2 1:48:12.
- **Atributos de sklearn.** `components_` (las direcciones), `explained_variance_` (los autovalores) y `explained_variance_ratio_` (la proporción) C2P2 1:39:55.

### Correcciones y matices
- **Corrección:** una alumna propone que "PC1 es la regresión lineal que mejor ajusta" y José asiente antes de matizar C2P2 1:14:30. No coinciden: PC1 minimiza la suma de distancias **perpendiculares** a la recta (y trata a las dos variables por igual), mientras que la regresión por mínimos cuadrados minimiza las distancias **verticales** de y. Verificado en el box: las pendientes difieren.
- **Corrección:** José dice que estandarizar "lleva a un rango entre −1 y 1 o algo así" C2P2 1:17:51. Estandarizar deja media 0 y desvío 1, y suele haber valores fuera de [−1, 1] (con una normal, un tercio de los datos). Él mismo lo aclara más tarde C2P2 2:15:47. Lo que lleva a un rango fijo es MinMaxScaler.
- **Corrección:** José dice que los coeficientes de cada variable en las componentes "se llaman scores en inglés" C2P2 1:23:56. Esos coeficientes son los **loadings** o direcciones (`pca.components_`, a veces escalados por la raíz del autovalor). Los **scores** son las coordenadas de cada dato en las nuevas componentes, lo que da `pca.transform(X)`.
- **Corrección (verificado en el box):** José dice que el PCA de dos variables es con "petal length y petal width" y da 55,87% y 44,12% C2P2 1:38:16. Con las de pétalo estandarizadas da 98,14% y 1,86% (están muy correlacionadas, r ≈ 0,96). El 55,88% y 44,12% sale con **sépalo** largo y ancho estandarizados (r ≈ −0,12). O la notebook usaba las de sépalo o la transcripción mezcló los nombres.
- **Corrección:** con las cuatro variables José dice primero "me quedo con un 99%" y después "no es 99, 94, 95%" C2P2 1:47:08, C2P2 2:03:04. PC1 + PC2 = 72,96 + 22,85 = **95,81%**. Verificado en el box.
- **Matiz:** José dice que sklearn "calcula la SVD de la matriz de covarianza" C2P2 1:38:48. `sklearn.decomposition.PCA` centra los datos y hace la SVD de la **matriz de datos centrada**; da lo mismo que diagonalizar la covarianza, pero es numéricamente más estable.
- **Matiz:** "la distancia entre los datos se preserva" C2P2 1:51:31 vale para la rotación completa (todas las componentes). Si descartás componentes las distancias se achican, y si estandarizaste antes ya cambiaron.
- **para verificar:** la bibliografía para la demostración ("el Fisher" y "Johnson... William and Johnson") C2P2 1:06:17 es casi seguro Johnson y Wichern, *Applied Multivariate Statistical Analysis*.

### Preguntas de repaso
1. ¿Qué diferencia hay entre loadings y scores?
2. ¿Por qué PC1 no es la recta de regresión?
3. ¿Cuándo hace falta estandarizar antes de PCA?

## 9. Escalar, normalizar, estandarizar y transformar
**Dónde:** C2P2 2:07:33, C2P2 2:13:42, C2P2 2:16:20, C2P2 2:17:28, C2P2 2:20:42, C2P2 2:21:47, C2P2 2:26:11, C2P2 2:27:19

### Conceptos clave
- **Tres cosas distintas.** Escalar es cambiar el rango; normalizar, en el sentido de José, es cambiar la forma de la distribución para acercarla a una normal; estandarizar es dejar media 0 y desvío 1 C2P2 2:07:33.
- **Escaladores de sklearn.** `MinMaxScaler` lleva a [0, 1]; `MaxAbsScaler` divide por el máximo absoluto y deja [−1, 1]; `StandardScaler` estandariza; `RobustScaler` es resistente a atípicos C2P2 2:13:42, C2P2 2:16:20.
- **Transformaciones de distribución.** Algunos modelos suponen normalidad. `PowerTransformer` (Yeo-Johnson, que acepta ceros y negativos, o Box-Cox, que exige positivos) y `QuantileTransformer` (lleva a uniforme o normal por rangos) C2P2 2:17:28. Todas tienen inversa, así que podés volver a la escala original C2P2 2:19:04.
- **El gráfico de sklearn.** Con distribuciones gaussiana, uniforme, bimodal, lognormal, chi cuadrado y Weibull: el cuantil normaliza mejor la uniforme y la bimodal; Box-Cox y Yeo-Johnson andan bien con las asimétricas C2P2 2:21:47.
- **Normalizer.** El `Normalizer` de sklearn hace otra cosa: lleva cada **fila** a norma 1 C2P2 2:26:11.
- **Notebook.** Hay una notebook de transformaciones con Melbourne C2P2 2:27:19.

### Correcciones y matices
- **Corrección:** José dice que MinMaxScaler "le resta el mínimo y divide por el máximo" C2P2 2:14:43. Divide por **max − min**: x' = (x − min) / (max − min).
- **Matiz:** dice que MinMax preserva los ceros C2P2 2:15:47. Solo si el mínimo es 0. El que preserva ceros siempre (y la esparsidad) es MaxAbsScaler.
- **Matiz:** dice que RobustScaler "no usa los atípicos para estimar promedio y varianza" C2P2 2:16:20. Más preciso: no usa ni promedio ni varianza; centra en la **mediana** y divide por el **rango intercuartil**.
- **Matiz:** "la normal es la gaussiana con media 0 y desvío 1" C2P2 2:10:54. Esa es la normal **estándar**; una normal puede tener cualquier media y desvío.
- **Matiz:** un alumno aplica log a los salarios "para eliminar outliers" C2P2 2:20:42. El log reduce la asimetría y comprime la cola, pero no elimina outliers: los acerca.
- **Matiz:** José justifica la normalidad de muchas variables "por la ley de los grandes números y el TCL" C2P2 2:21:47. La que explica la forma normal es el teorema central del límite; la ley de los grandes números habla de convergencia del promedio, no de forma.

### Preguntas de repaso
1. ¿Qué escalador usarías con datos esparsos?
2. ¿Por qué Box-Cox no sirve con ceros y Yeo-Johnson sí?
3. ¿Qué hace `Normalizer` y en qué se diferencia de `StandardScaler`?

## 10. Roles, productos de datos y ciclo de un proyecto
**Dónde:** C3P1 21:27, C3P1 27:35, C3P1 37:30, C3P1 44:47, C3P1 47:36, C3P1 53:00, C3P1 1:03:09, C3P1 1:08:09, C3P1 1:24:22, C3P1 1:27:04, C3P1 1:39:05, C3P1 1:42:20, C3P2 0:03, C3P2 1:46, C3P2 4:36, C3P2 8:55, C3P2 13:22, C3P2 16:13

### Conceptos clave
- **Qué aprender hoy.** Programar, buscar y preguntar bien (de memorizar a Stack Overflow y de ahí a escribir buenos prompts); los LLM no resuelven el 100%, hay que leer los errores y la documentación; formar criterio C3P1 21:27, C3P1 23:09, C3P1 25:22. Ejemplo de por qué: un `groupby` que te devuelve 2 millones de filas es una explosión de cardinalidad que tenés que saber reconocer C3P1 27:02.
- **El mapa.** IA contiene a ML, que contiene a deep learning. Alrededor: data science, data mining, big data, ML engineering, data engineering C3P1 33:41. La estadística es el fundamento; ML es estadística aplicada a escala; analytics y BI son tableros y KPIs; big data y data engineering son infraestructura; data science es aplicar el método científico a los datos C3P1 34:13.
- **Subcampos.** IA (simular inteligencia humana en casos puntuales), GenAI (predecir la próxima palabra), ML, deep learning (redes neuronales que no requieren definir features a mano), NLP, visión por computadora y aprendizaje por refuerzo (ajedrez, Go, ajuste fino de LLM) C3P1 37:30, C3P1 38:38, C3P1 39:14. José explica el fine tuning con un clasificador de perros y gatos que se reentrena para abejas y moscas C3P1 41:28.
- **Features.** Una columna no es una feature hasta que la pensás: el DNI como proxy de la edad, el prefijo 351 como indicador de Córdoba C3P1 44:47, C3P1 8:54.
- **E-commerce como ejemplo.** Analytics mide ventas; data science predice demanda; ML predice abandono (churn); GenAI hace el chatbot C3P1 47:36. Data engineering se ocupa de recolección, almacenamiento, procesamiento eficiente, ETL o ELT, calidad, escalabilidad, seguridad y privacidad C3P1 50:49.
- **Producto de datos.** "Los datos son el nuevo petróleo" contra "son como el agua" (hay que democratizarlos y cuidar la calidad) C3P1 53:34. Un producto de datos suma la incertidumbre del mercado y la de los datos: las predicciones nunca son 100% C3P1 54:09. Analogía del pan dulce: el modelo de ML es la pasa de uva y el resto es ingeniería C3P1 56:25. ML tradicional (tus datos entrenan el modelo) contra GenAI (tus datos son el contexto) C3P1 59:08.
- **Agentes.** El modelo es el motor; alrededor van herramientas, memoria, contexto y orquestación C3P1 1:03:44. Ariel cuenta que en una conferencia solo un 10% había logrado poner agentes en producción C3P1 1:05:22.
- **Netflix como caso.** Portadas personalizadas por perfil, metadata, A/B testing, gente paga para etiquetar contenido C3P1 1:08:40, C3P1 1:11:37, C3P1 1:12:42. "Mientras más cosas determinísticas, mejor" C3P1 1:13:52. El Netflix Prize de un millón de dólares: el modelo ganador nunca se puso entero en producción por el costo de ingeniería C3P1 1:17:15.
- **Equipos.** Data scientist, data engineer, analytics engineer, data analyst, ML engineer y product manager; el "unicornio" que hace todo no existe; roles nuevos: AI engineer, prompt engineer, AI PM C3P1 1:24:56, C3P1 1:26:32.
- **Ciclo de un proyecto.** Definir el problema y el caso de uso (por ejemplo, abandono de carrito), recolectar respetando la privacidad, explorar, curar, modelar, evaluar, desplegar, comunicar y monitorear C3P1 1:27:36, C3P1 1:29:45, C3P1 1:31:56. Un modelo simple con datos limpios le gana a uno potente con datos sucios C3P1 1:35:15. La curación incluye faltantes, outliers, redundancias, transformaciones y definiciones de negocio (¿usuario activo a 30, 60 o 90 días?) C3P1 1:36:20. Ejemplos: en la encuesta de sueldos hay edades menores de 18 y mayores de 99 y un sueldo de un millón C3P1 1:37:28.
- **ML clásico o LLM.** Error común: usar un LLM para todo. El ML clásico gana en determinismo, testeabilidad, auditabilidad, costo y latencia C3P1 1:39:36, C3P1 1:40:39, C3P2 0:03.
- **Garbage in, garbage out.** Superficies negativas, 1000 habitaciones, precios mezclados en pesos, dólares y Bitcoin C3P2 0:37. Detrás de los modelos hay humanos etiquetando (Amazon Mechanical Turk, anotadores que puntúan respuestas de ChatGPT, Claude o Gemini); el cuello de botella es el experto de dominio C3P2 1:46, C3P2 3:26.
- **Evaluación.** Métricas, generalización, sobreajuste; siempre un baseline ("mejor que tirar una moneda"); train y test; validación cruzada en 5 partes, 80/20 rotando C3P2 4:36, C3P2 5:10, C3P2 6:12. Evaluar GenAI es más difícil por el no determinismo C3P2 7:17.
- **Despliegue, comunicación y monitoreo.** Integración con APIs, observabilidad C3P2 8:55; storytelling y tableros (Apache Superset, libre) C3P2 10:00, C3P2 12:47; drift: el mundo cambia y hay que reentrenar con datos frescos C3P2 13:22, C3P2 15:38. En GenAI: alucinaciones (errores convincentes) y context rot C3P2 16:13.
- **Ética.** Clasificadores de imágenes que etiquetaron mal a personas negras, modelos de reincidencia, un modelo de selección de personal de Amazon que discriminaba mujeres C3P1 1:42:53, C3P1 1:47:14. La ética depende de quién entrena y cambia con el tiempo (José) C3P1 1:45:36. Laura Alonso Alemany dicta una optativa de ética C3P1 1:48:52. Leyes: LGPD en Brasil; la ley argentina 25.326 quedó vieja C3P1 1:49:25.

### Correcciones y matices
- **Matiz:** Ariel dice que con Gemini o NotebookLM "no estás haciendo un ajuste de hiperparámetros" C3P1 42:35, y en la clase 4 que el fine tuning es "para que el modelo ajuste esos hiperparámetros" C4P1 2:53. El fine tuning ajusta **parámetros** (los pesos); los hiperparámetros son lo que elegís vos antes de entrenar (tasa de aprendizaje, épocas, tamaño del lote).
- **Matiz:** el meme de "el trabajo más sexy del siglo XXI" C3P1 51:55 viene del artículo de Davenport y Patil en *Harvard Business Review*, 2012.
- **para verificar:** "hay papers" sobre que el modelo es una parte chica del sistema C3P1 56:25: el clásico es Sculley y otros, "Hidden Technical Debt in Machine Learning Systems", NeurIPS 2015, con el dibujo de la cajita de ML en medio de toda la infraestructura.
- **para verificar:** los modelos "como funciones SQL" de una conferencia de Google C3P1 1:00:51: suena a BigQuery ML y a las funciones de IA de BigQuery.
- **para verificar:** "60% del tiempo en limpieza, 20% en recolección" C3P1 1:34:08 es la cifra que popularizó una encuesta de CrowdFlower de 2016; circula mucho pero viene de una encuesta de una empresa, no de un estudio.
- **para verificar:** el caso de Google etiquetando personas negras como "monos" C3P1 1:42:53 es el de Google Photos en 2015 (las etiquetó como "gorilas"). El de reincidencia es probablemente COMPAS (ProPublica, 2016). **dudoso:** "juicios por varios millones" por COMPAS C3P1 1:43:28; el caso conocido (Loomis, Wisconsin) no fue una indemnización millonaria.
- **dudoso:** que las fotos de Pokémon Go se usaran "para una empresa de delivery tipo DHL" C3P1 1:44:00. Lo documentado es que Niantic anunció en 2024 un "Large Geospatial Model" entrenado con escaneos de jugadores; no encontré un cliente de delivery.
- **para verificar:** "LatamGPT salió este año" C3P1 1:50:29. El modelo regional coordinado desde Chile se presentó públicamente hace poco, pero la fecha exacta de lanzamiento no la confirmé.
- **para verificar:** "Claude tendía a abstenerse cuando no sabía y GPT tendía a inventar" C3P2 17:21; el mismo Ariel aclara que puede estar desactualizado.
- **Matiz:** el Y2K, bases con años de dos dígitos donde "algunos explotaron por los aires" C3P2 13:56. El impacto real fue acotado justamente porque se invirtió mucho en corregir antes.

### Preguntas de repaso
1. ¿Qué diferencia hay entre parámetros e hiperparámetros, y cuál ajusta el fine tuning?
2. ¿Por qué un modelo simple con datos limpios puede ganarle a uno potente con datos sucios?
3. Nombrá tres ventajas del ML clásico frente a un LLM.

## 11. Recolección, tipos de datos, privacidad, gobernanza y calidad
**Dónde:** C3P2 19:07, C3P2 22:33, C3P2 25:56, C3P2 31:34, C3P2 34:55, C3P2 38:46, C3P2 40:58

### Conceptos clave
- **Qué datos generás.** Al salir a correr con música: zona, géneros, hora, recorrido, GPS, permisos, reloj inteligente C3P2 19:45. Cruzar fuentes multiplica lo que se sabe de vos C3P2 21:26.
- **Fuentes.** Internas o externas, comerciales o públicas; transaccionales, conversacionales, sensores, registros de actividad C3P2 22:33. Publicidad cruzada entre plataformas C3P2 23:39.
- **Tipos.** **Estructurados**: tablas, CSV, Parquet, bases relacionales; los mejores para ML clásico C3P2 26:29. **Semiestructurados**: JSON con campos distintos y anidados, bases de documentos, grafos C3P2 27:37, C3P2 29:18. **No estructurados**: texto, imágenes, audio, de los que se extrae metadata C3P2 29:52.
- **Combinar fuentes.** Unidades distintas, nombres distintos, zonas horarias desincronizadas; fuentes que cambian (una API pública que pasa a privada) C3P2 31:34, C3P2 33:49.
- **Privacidad.** Anonimización, consentimiento, letra chica, retención; el GDPR europeo con el derecho de supresión; la ley argentina 25.326 desactualizada C3P2 34:55. Datos sensibles: nombre, DNI, nacimiento, dirección, biométricos, historia clínica, ubicación C3P2 37:08. Si usás datos de un trabajo para tu portfolio, anonimizá C3P2 36:03.
- **Gobernanza.** Quién es responsable, dónde se guarda, cómo se protege; banca, sector público y salud tienen reglas propias; con tarjetas podés guardar el número pero no el código de seguridad, y necesitás certificación C3P2 38:46, C3P2 39:52.
- **Calidad.** Completitud; validez (una superficie negativa); precisión (el GPS); integridad (una venta sin cliente); consistencia y duplicados (mismo DNI o teléfono); temporalidad (datos de bolsa de hace una semana); representatividad C3P2 40:58. En GenAI, la fecha de corte del entrenamiento; la calidad de un agente depende de su capa de datos C3P2 43:51, C3P2 44:24.

### Correcciones y matices
- **Matiz:** "HIPA HPA" en la transcripción es **HIPAA**, la ley de EE. UU. sobre datos de salud C3P2 39:18. La regla de no guardar el código de seguridad de la tarjeta es del estándar **PCI DSS**, que Ariel no nombra C3P2 39:52.
- **para verificar:** Ariel menciona "el Opus 4.7" como modelo actual C3P2 44:24; no lo chequeé.

### Preguntas de repaso
1. Clasificá como estructurado, semiestructurado o no estructurado: un CSV de ventas, un JSON de pedidos, un audio de un call center.
2. Dá un ejemplo de problema de integridad y uno de temporalidad.

## 12. Ingesta, formatos y bases de datos
**Dónde:** C3P2 46:59, C3P2 49:39, C3P2 53:03, C3P2 55:21, C3P2 58:07, C3P2 1:00:14, C3P2 1:04:51, C4P1 1:13, C4P1 20:13

### Conceptos clave
- **Formatos.** Tabulares (CSV, Excel), jerárquicos (JSON, XML), crudos (TXT) C3P2 47:31. CSV: texto, primera línea con nombres, universal pero sin tipos. JSON: anidado (por ejemplo `owner.address`). Parquet: columnar, comprimido, lectura rápida para analizar a escala. Avro: por filas, con esquema que puede evolucionar, para mover datos entre sistemas y streaming. Iceberg: no es un formato de archivo sino un formato de tabla para data lakes. Markdown: el formato cómodo para darle texto a un LLM o a un RAG C3P2 49:39, C3P2 51:54, C3P2 53:38.
- **La ingesta es parte de la recolección**: volcar los datos a un data lake o data warehouse C4P1 1:13.
- **Bases relacionales.** Tablas de tuplas con claves y relaciones, consultadas con SQL. Ejemplo: tabla de equipos con clave primaria `id_equipo` y tabla de jugadores que la referencia (Real Madrid con Cristiano Ronaldo y Bale; Barcelona con Messi y Suárez) C3P2 55:21, C3P2 56:27.
- **NoSQL.** Clave valor, documentos, grafos y vectores C3P2 58:07. Las bases vectoriales guardan embeddings de texto, audio o video y buscan por similitud C3P2 58:38.
- **SQL contra similitud.** SQL busca coincidencia exacta ("zapatillas"); la búsqueda vectorial encuentra "calzado deportivo" C3P2 1:00:14. Postgres tiene extensión vectorial C3P2 1:00:48.
- **RAG.** Recuperar los fragmentos más parecidos a la pregunta y concatenarlos al prompt para que el modelo responda con ese contexto C3P2 1:00:48, C3P2 1:03:08. Ariel recapitula embeddings con "rey + mujer ≈ reina" y recomienda Chroma y los cursos de DeepLearning.AI C4P1 20:46, C4P1 23:02.

### Correcciones y matices
- **Matiz:** RAG es **Retrieval-Augmented Generation** (Lewis y otros, 2020). No modifica el modelo: le agrega contexto recuperado en cada consulta. Por eso no es "un LLM especializado", como propone un alumno en la clase 4 C4P2 51:38.
- **Matiz:** el ejemplo clásico de word2vec es **rey − hombre + mujer ≈ reina** C4P1 20:46; "rey + mujer" a secas no da reina.
- **dudoso:** ante una pregunta sobre tablas hash, Ariel dice que con "destilación, un vector de 1000 lo metés en un hashing y lo achicás a 10, donde la probabilidad de colisión es menor" C3P2 1:05:24. Achicar la dimensión no baja las colisiones (al contrario), y "destilación" es otra cosa: entrenar un modelo chico para imitar a uno grande. Las bases vectoriales usan índices aproximados (HNSW, IVF, LSH, que sí es hashing sensible a la localidad) y cuantización para comprimir vectores.
- **para verificar:** que Postgres haga búsqueda vectorial se refiere a la extensión pgvector C3P2 1:00:48.

### Preguntas de repaso
1. ¿Cuándo elegirías Parquet y cuándo Avro?
2. ¿Qué hace un RAG que no hace un fine tuning, y al revés?

## 13. SQL desde Python
**Dónde:** C4P1 1:00:41, C4P1 1:02:22, C4P1 1:05:15, C4P1 1:09:13, C4P1 1:11:54, C4P1 1:14:45, C4P1 1:18:45, C4P1 1:20:21, C4P2 0:01, C4P2 3:17

### Conceptos clave
- **Por qué SQL.** Es el estándar y escala a volúmenes grandes; los LLM ayudan a escribirlo pero no validan el resultado C4P1 1:00:41.
- **SQLite y el tutorial.** Se practica con el tutorial de SQLite y su base de ejemplo Chinook (albums, artists, tracks) C4P1 1:02:22. Cláusulas: `SELECT`, `DISTINCT`, `FROM`, `JOIN`, `WHERE`, `ORDER BY`, `LIMIT`, `GROUP BY`, `HAVING` C4P1 1:03:29. Ejemplos: `ORDER BY Composer ASC, Name DESC` (falla por una coma de más) C4P1 1:05:15, `LIKE '%Smith%'` C4P1 1:07:32, `LIMIT 10 OFFSET 30`, `GROUP BY` con `COUNT` y `HAVING COUNT(*) >= 30` C4P1 1:08:05, `INNER JOIN` de albums con artists C4P1 1:09:13. Diagrama de joins (left, inner, outer) y diagrama entidad relación C4P1 1:10:16, C4P1 1:11:22.
- **¿SQL o pandas?** SQL para extraer y filtrar, pandas para analizar C4P1 1:11:54. Depende del volumen: una laptop con 8 o 16 GB no carga una base de 100 GB, así que se extrae con SQL solo lo necesario C4P2 0:33. Si son CSV, `read_csv` directo, con `chunksize` o Polars si son grandes C4P2 3:17, C4P1 1:20:21.
- **SQLAlchemy.** La notebook carga la encuesta de sueldos 2020, crea un motor SQLite con `create_engine("sqlite:///...")`, la vuelca con `df.to_sql("survey", engine)` y la consulta con SQL; `pd.read_sql` devuelve un DataFrame C4P1 1:14:45, C4P1 1:18:45. Ejemplos: sueldo neto mayor a 100.000, una sola columna, un `COUNT`. Una columna de texto libre (beneficios extra) muestra por qué hace falta curar C4P1 1:19:49.

### Correcciones y matices
- **para verificar:** Ariel la llama "encuesta salarial 2020"; el archivo del repo es `sysarmy_survey_2020_processed.csv`, de la encuesta de sueldos de Sysarmy (verificado en el box: 6.095 filas). Para la versión 2026 de la notebook no lo pude ver.
- **Matiz:** en SQLAlchemy 2.x las consultas de texto van envueltas en `text(...)` y se ejecutan dentro de `with engine.connect() as conn:`. `pd.read_sql` acepta el string directo.

### Preguntas de repaso
1. Escribí la consulta SQL equivalente a `df[df.price > 100].groupby("zone").size()`.
2. ¿Cuándo conviene filtrar en SQL antes de traer los datos a pandas?

## 14. Combinar datasets: groupby, join, merge y cardinalidad
**Dónde:** C4P1 1:24:43, C4P1 1:26:25, C4P1 1:31:53, C4P1 1:34:08, C4P2 4:29, C4P2 7:51, C4P2 10:41, C4P2 13:31, C4P2 20:37, C4P2 26:09, C4P2 30:56, C4P2 37:34

### Conceptos clave
- **groupby.** Agregaciones `sum`, `mean`, `count`, `min` sobre Iris C4P1 1:24:43.
- **join y merge.** `join` une por índice; con `how="outer"` aparecen NaN donde falta un lado C4P1 1:26:25. `merge` une por columnas clave C4P1 1:31:53. Para imputar una categórica codificada como entero no conviene promediar (te da 1,5): mejor la más frecuente C4P1 1:28:37, C4P1 1:30:48.
- **Errores comunes.** Claves duplicadas o inconsistentes, tipos incompatibles (int contra object), mismos nombres con distinto significado, huecos, merge sin `on` C4P1 1:34:08.
- **El caso Airbnb.** Avisos de Airbnb de Melbourne de diciembre de 2018 (Kaggle, copia en FAMAF), leídos con `usecols` para no llenar la memoria C4P2 5:39. Imputar el precio semanal como 7 veces el diario es una estrategia válida, aunque algunos tienen descuento C4P2 7:19. Son 22.895 avisos; `zipcode` viene con tipos mezclados y se arregla con `pd.to_numeric`; el código 3000 aparece como 2.491 + 876 = 3.367 avisos C4P2 7:51; con `fillna(0).astype(int)` quedan 146 en cero C4P2 9:35.
- **Cobertura.** `np.intersect1d`: 248 códigos en Airbnb, 198 en Melbourne, 191 en común; el 99,85% de las ventas de Melbourne y cerca del 93% de los avisos caen en la intersección C4P2 10:41, C4P2 12:55.
- **Mapas.** `plotly` con `scatter_geo` o `scatter_mapbox` sobre OpenStreetMap C4P2 13:31, C4P2 18:50. La columna `state` tiene "VIC", "Vic" y "Victoria" sin normalizar C4P2 16:37.
- **Explosión de cardinalidad.** El merge directo de `Postcode` con `zipcode` da unos 2 millones de filas: cada venta se repite tantas veces como avisos haya en su código; "85 Turner St" (postcode 3067) aparece 258 veces C4P2 20:37, C4P2 21:43.
- **La solución.** Agregar Airbnb por código postal (precio medio, cantidad, semanal y mensual medios) y recién ahí unir: el 3000 queda con precio medio 150 por noche sobre 3.367 avisos, 918 semanal y 3.407 mensual C4P2 26:09. La hipótesis es que el alquiler de la zona informa el precio de venta C4P2 27:52. El merge `how="left"` conserva las 13.580 ventas y 20 quedan sin información de Airbnb C4P2 30:56.

### Correcciones y matices
- **Matiz:** ante la pregunta de por qué no usar `one_to_one`, Ariel dice que "la operación es válida, no rompió, pero no agrega información" C4P2 37:34. Con `validate="one_to_one"` pandas **sí rompe**: tira `MergeError` porque los códigos postales se repiten en Melbourne (y en Airbnb antes de agregar). Después de agregar, el chequeo correcto es `validate="many_to_one"`: muchas ventas por código, un solo registro de Airbnb por código. Verificado en el box.
- **Matiz:** `DataFrame.join` tiene `how="left"` por defecto y `merge` tiene `how="inner"` por defecto: un merge sin `how` te puede tirar filas en silencio.
- **Matiz:** los 248 códigos únicos de Airbnb incluyen el NaN de los 146 avisos sin código (`unique()` lo cuenta como un valor más): códigos reales hay 247. Verificado en el box.
- **Verificado en el box:** con el CSV del repo los números de Ariel coinciden (22.895 avisos, 146 sin código, 248 / 198 / 191 códigos, 13.580 filas tras el merge izquierdo y 20 sin dato). Las cifras exactas están en la guía.

### Preguntas de repaso
1. ¿Por qué el merge directo da 2 millones de filas y cómo lo detectás antes de que pase?
2. ¿Qué validación pondrías en el merge final y por qué?

## 15. ETL, orquestación y arquitectura de datos
**Dónde:** C4P2 40:24, C4P2 40:56, C4P2 43:47, C4P2 45:27, C4P2 47:13, C4P2 52:09, C4P2 54:23, C4P2 57:06, C4P2 1:02:50, C4P2 1:04:32, C4P2 1:08:22, C4P2 1:10:01, C4P2 1:13:20, C4P2 1:15:34, C4P2 1:16:40, C4P2 1:17:49, C4P2 1:28:52

### Conceptos clave
- **ETL.** Extraer de las fuentes (sistemas operacionales, ERP, CRM, archivos), transformar y cargar en un data warehouse que alimenta reportes, ML y minería C4P2 40:24. En la notebook de Airbnb, `usecols` y `to_numeric` ya eran transformaciones C4P2 44:20.
- **Data warehouse contra data lake.** El DW guarda datos estructurados y validados para BI (BigQuery, Redshift, Snowflake); el lake guarda cualquier tipo de dato con esquema flexible y más barato (S3, Google Cloud Storage, Azure Blob) C4P2 40:56, C4P2 42:03. Postgres es una base de datos, no un DW C4P2 42:38.
- **ELT.** Hoy es común cargar primero al lake y transformar después, con herramientas como dbt o Dataform C4P2 45:27.
- **Pipeline de RAG.** Ingesta (PDF, scraping), partir en chunks, enriquecer con metadata, calcular embeddings, indexar en una base vectorial, recuperar y generar. Error común: creer que es "subir un documento" C4P2 47:13, C4P2 49:24. Un embedding es una forma de encoding C4P2 51:38.
- **Batch contra streaming.** Batch con Airflow, Spark, SQL; streaming con Kafka, Flink, Spark Streaming, Dataflow; ejemplo de detección de fraude en menos de 10 segundos C4P2 52:09, C4P2 53:16.
- **Airflow.** Orquesta, no procesa. Un DAG (grafo acíclico dirigido) de tareas, por ejemplo `extract >> transform >> load` C4P2 54:23. Un ETL automático no es ML: automatizar no es aprender (José) C4P2 56:01. La notebook ilustrativa (no corre en Colab) usa logging, SQLAlchemy contra Postgres, la encuesta de sueldos, `requests` a una API pública, Parquet y una columna de fecha de carga C4P2 57:06.
- **Airflow contra agentes.** Airflow es determinístico; un agente decide dinámicamente qué herramienta llamar C4P2 1:02:50.
- **Medallion.** Bronce: crudo, tal como llega. Plata: limpio y con formatos unificados (fechas como "9 del 5 del 26" pasadas a un formato estándar). Oro: lógica de negocio y KPIs, por ejemplo la agregación de Airbnb por código postal C4P2 1:04:32. Además: indexación, particionamiento, clustering C4P2 1:08:22.
- **Modern data stack.** Ingesta (Fivetran, Stitch, Airbyte), orquestación (Airflow, Prefect), almacenamiento (BigQuery, Redshift, Snowflake), transformación (dbt), consumo (Power BI, Looker, Tableau); Databricks de punta a punta C4P2 1:10:34. Lakehouse: SQL sobre archivos en S3 con Iceberg o Delta Lake C4P2 1:13:20. Reverse ETL: devolver resultados del DW a los sistemas operativos, por ejemplo un puntaje de fraude C4P2 1:15:34. Data mesh: datos descentralizados por dominio, para organizaciones maduras C4P2 1:16:40.
- **Stack de GenAI.** La capa oro alimenta una base vectorial, el RAG, memoria, contexto, salida estructurada y restricciones (guardrails); un agente de soporte que terminó respondiendo código Python se hizo viral C4P2 1:17:49, C4P2 1:22:19.
- **Buenas prácticas.** Los warnings no son errores, pero hay que entender qué avisan C4P2 1:28:52. No subir claves a GitHub ni pegarlas en un chat; respetar las licencias de los datos C4P2 1:31:06.

### Correcciones y matices
- **Corrección:** Ariel dice que el formateo de fechas "va en la capa gold" C4P2 1:06:45 y después pone la agregación por código postal como gold. En la arquitectura medallion (Databricks) el formateo, la limpieza y la unificación de tipos van en **plata**; oro es lo agregado y con lógica de negocio. Lo segundo que dice es lo correcto.
- **Matiz:** un alumno dice que "un RAG sería como un LLM especializado" C4P2 51:38; ver el módulo 12.

### Preguntas de repaso
1. ¿Qué diferencia hay entre ETL y ELT y por qué hoy se usa más ELT?
2. Ubicá en bronce, plata u oro: el CSV crudo de Airbnb, el zipcode convertido a entero, el precio medio por código postal.
3. ¿Por qué Airflow no es un agente?

## 16. Los entregables
**Dónde:** C1P1 8:24, C2P2 2:04:42, C2P2 2:28:29, C3P1 6:44, C3P1 11:05, C4P2 1:22:51

### Conceptos clave
- **Formato.** Dos entregables grupales en notebooks de Jupyter, que se suben al aula virtual; los grupos los coordinan los profes de práctico C1P1 8:24, C2P2 2:30:45.
- **Entregable 1.** Con Melbourne: analizar las variables, elegir y justificar un encoding, imputar con KNN, aplicar PCA y escribir un informe "como para una empresa". Se pueden usar chatbots pero hay que explicar lo que se hace C2P2 2:28:29. Las columnas se eligen según un objetivo; un ID correlativo no sirve y las columnas sin varianza no aportan C3P1 6:44, C3P1 9:58.
- **Fecha del entregable 1.** En la clase 1 José dijo 10 de mayo C1P1 9:30, en la clase 2 "creo que el 10 de mayo" C2P2 2:04:42 y en la clase 3 lo movió: "les había pedido el 11, pero pueden entregarlo el 14 de mayo" C3P1 11:05. La fecha válida es la última, el **14 de mayo de 2026**.
- **Entregable 2.** Con Melbourne: crear una base SQLite, mapear a SQL las consultas que antes hacían en pandas, hacer el JOIN con los datos de Airbnb en SQL en vez de con `merge`, y revisar faltantes, dispersión y distribuciones. Hay bonus opcionales que no se evalúan: scripts de ETL y embeddings con la API de Anthropic C4P2 1:22:51. El repo de 2022 pedía algo parecido: ingestar en SQLite las ventas y la tabla de Airbnb por código postal, y como extra un script ETL y un DAG de Airflow.

### Correcciones y matices
- **para verificar:** la fecha del entregable 2. Ariel dice "15 días después" del entregable 1 C4P2 1:25:36 y en el aula virtual figuraba la edición 2025 hasta que la actualizaron C4P2 1:26:10. Revisá la fecha en el aula.

### Preguntas de repaso
1. ¿Qué técnicas obligatorias tiene el entregable 1?
2. ¿Qué cambia en el entregable 2 respecto de hacerlo todo en pandas?

## Glosario de la transcripción

| En la transcripción | Es |
|---|---|
| introducción y curación de datos | Análisis Exploratorio y Curación de Datos |
| EICD | el canal de Slack de AEyCD |
| Yuli | Jülich (Jülich Supercomputing Centre) |
| Ariel W | Ariel Wolfmann |
| Missing, la librería Missing | missingno |
| mel_data | melb_data (Melbourne) |
| inesgado | insesgado |
| NMAR | MNAR (missing not at random) |
| imputación múltiple con ecuaciones encadenadas | MICE: Multivariate Imputation by Chained Equations |
| Sens Soccer | Census (el censo de EE. UU.) |
| el Fisher, William and Johnson | probablemente Johnson y Wichern |
| scores (para los coeficientes) | loadings, `components_` |
| HIPA HPA | HIPAA |
| Yalo | Yalo (comercio conversacional) |
| Chinook | la base de ejemplo del tutorial de SQLite |
| survey | la tabla con la encuesta de sueldos de Sysarmy 2020 |
| cuatrimestre (de la fecha) | trimestre |
| medallion, bronce, plata, oro | la arquitectura medallion de Databricks |
| retrieval augmented | RAG: Retrieval-Augmented Generation |
