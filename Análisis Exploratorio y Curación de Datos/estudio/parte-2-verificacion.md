# Segunda parte: "Análisis Exploratorio y Curación de Datos", con material externo

**Esta es la continuación de** `analisis-exploratorio-y-curacion-apunte-de-estudio.md` y `analisis-exploratorio-y-curacion-guia-de-implementacion.md` (las clases de Análisis Exploratorio y Curación de Datos, segunda materia obligatoria de la Diplomatura en Ciencia de Datos de FAMAF UNC, cohorte 2026, dictadas por José Ignacio Robledo y Ariel Mauricio Wolfmann en cuatro encuentros: 24 y 25 de abril y 8 y 9 de mayo de 2026). Esos archivos resumen lo que dice la materia. Esta segunda parte suma material externo para verificar lo que en el apunte quedó "para verificar" o "dudoso", respaldar con fuentes las correcciones que ya marqué, corregir errores míos de la primera parte, sumar bibliografía y discutir el enfoque de la materia (exploración y curación a mano con pandas en notebooks, imputación elegida a criterio, scripts de ETL) contra la alternativa más fuerte, con benchmarks reales sobre Melbourne y Adult. Revisé todo el 03/10/2026 y solo cito páginas que abrí (las que solo vi en un buscador las marco así). Conflictos de interés: los marco donde aparecen; los más importantes son Databricks (vende el lakehouse y es la autora de la arquitectura medallion), Great Expectations, Soda y dbt Labs (venden plataformas de calidad y transformación de datos), CrowdFlower (vendía etiquetado y es la autora de la cifra del 60%), CENIA y AWS (hablan de su propio LatamGPT) y Niantic (habla de su propio modelo).

> Cómo leer esto: cuando digo "la materia" o "los docentes" me refiero a lo que dicen José y Ariel en las clases. Las marcas de tiempo usan la etiqueta de cada grabación del apunte (C1P1 es la clase 1, parte 1, y así hasta C4P2) y llevan al minuto exacto en la grabación. Cuando digo "sugerencia" es una idea mía que combina fuentes, no algo que diga una fuente puntual. Los benchmarks los corrí en el box el 03/10/2026 en un entorno aparte (`bench_aeycd_venv`) con Python 3.13, pandas 2.3.3, scikit-learn 1.9.1, XGBoost 3.4.1, DuckDB 1.5.6, Polars 1.44.2, pandera 0.33.1 y ydata-profiling 4.18.4 (que obliga a pandas menor que 3; por eso no usé el entorno de la guía, que tiene pandas 3.0.6). Los datos son los mismos de la guía: `melb_data.csv` de FAMAF (13.580 filas), `cleansed_listings_dec18.csv` de Airbnb y `adult.data` de UCI. Los tiempos son de una CPU del box, sin GPU, y algunos corrieron en paralelo con otros trabajos, así que tomalos como órdenes de magnitud.

---

## Checklist actualizado (curso + mejoras)

1. Antes de contar faltantes, anotá **sobre qué archivo y después de qué filtro** los contás. Las cifras de la clase 2 (7.102 faltantes en BuildingArea, 2.587 en CouncilArea, 5.911 en YearBuilt) salen del CSV de 18.396 filas **después** de `dropna(subset=["Car"])`, que deja 14.820 filas. Con el CSV de FAMAF, el mismo filtro da 13.518 filas y 6.417, 1.307 y 5.344.
2. Usá `isna()` (o `isnull()`, que la documentación declara alias) y convertí antes los centinelas a NaN: en Melbourne hay 34 casas con 0 baños y 17 con BuildingArea 0.
3. Para saber si algo es NaN, nunca compares con `==`: el estándar IEEE 754 define que NaN es distinto de todo, incluso de sí mismo. `pd.NA` usa lógica de tres valores (Kleene).
4. Escribí el **contrato** de la tabla como código (rangos, categorías, nulos permitidos) con pandera o Great Expectations y corrélo cada vez que cargás datos. En Melbourne, ocho reglas encuentran en 0,3 s los 22 valores raros que en clase se buscaron a ojo (BuildingArea 0 y 44.515, YearBuilt 1196).
5. Si el objetivo es **predecir**, probá primero un modelo que acepta NaN (`HistGradientBoosting`, XGBoost) sin imputar. En Melbourne ganó o empató a todas las imputaciones y fue de los más rápidos (sección 4).
6. Si el modelo necesita una matriz completa (regresión lineal, KNN, PCA), imputá **dentro** del `Pipeline` (así no hay fuga entre train y test) y agregá `add_indicator=True`. Cuando la falta es informativa, el indicador recupera casi todo lo perdido (sección 5).
7. Si el objetivo es **estimar e inferir** (un coeficiente, una media con su intervalo), usá imputación múltiple de verdad: m copias imputadas con ruido (`IterativeImputer(sample_posterior=True)` con semillas distintas, o `mice` en R) y combiná con las reglas de Rubin. van Buuren dice que las opciones tradicionales eran 3, 5 o 10 y que el consejo actual es subir m, por ejemplo a 50.
8. Recordá que `IterativeImputer` es **experimental** en scikit-learn 1.9.1: hay que importarlo con `enable_iterative_imputer` y su API puede cambiar sin aviso. Fijá la versión en `requirements.txt`.
9. `KNNImputer` no exige vecinos con filas completas: usa `nan_euclidean`. Escalá antes (en el benchmark lo hice con `StandardScaler`) y medí el costo: con Ridge fue 35 a 50 veces más lento que la mediana y con árboles 6 veces, sin mejorarlos.
10. Con faltantes categóricos (Adult), una categoría propia "Falta" es tan buena como la moda o mejor, y deja el rastro de que faltaba. Kimball recomienda lo mismo en las dimensiones ("Unknown" o "Not Applicable" en vez de null).
11. Ante MNAR, no tires la variable por reflejo: agregá el indicador y hacé un análisis de sensibilidad (van Buuren, sección 3.8.5, y el ajuste δ del capítulo 9.2).
12. En la arquitectura medallion, el formateo y la limpieza van en **plata**; oro es lo agregado con lógica de negocio. Databricks lo dice explícitamente.
13. Para ETL sobre archivos medianos, pandas alcanza. Si el volumen crece 50 veces, Polars hizo el agrupar y combinar de la clase 4 unas 18 veces más rápido que pandas; DuckDB rinde cuando la consulta queda adentro de DuckDB y no cuando el resultado vuelve a pandas.
14. Leé el CSV crudo de Airbnb con el motor C de pandas o con DuckDB: tiene saltos de línea dentro de celdas, y el motor `pyarrow` de pandas y la inferencia por defecto de Polars fallan.
15. Usá un perfilado automático (ydata-profiling, hoy renombrado fg-data-profiling) como **primer pantallazo**, no como reemplazo: en Melbourne tardó 5 a 18 s y no marcó ninguno de los tres valores imposibles.
16. Fijá en tu entorno la versión de pandas que usás. En Colab, durante la materia, había pandas 2.2.2 (dtype `object` para texto); en el box, pandas 3.0.6 (dtype `str`). El mismo código cambia de comportamiento.
17. Revisá la fecha del entregable 2 en el aula virtual: no figura en ninguna página pública.

## Versión completa

### 1. Los datos del curso, verificados

| Afirmación | Resultado | Matiz | Fuente |
|---|---|---|---|
| El CSV de Kaggle que bajaron en clase tiene 18.396 filas C2P1 10:35 | Sí (corrijo mi apunte) | Encontré una copia de 18.396 × 22 (con una columna `Unnamed: 0`) en un repositorio de GitHub. Con `dropna(subset=["Car"])` reproduce **exactamente** las cifras de José: 14.820 filas; 7.102, 2.587 y 5.911 faltantes; cuantil 99 de BuildingArea 465; cuantil 1 de YearBuilt 1880; CouncilArea con 33 categorías. La página de Kaggle solo la vi en el buscador (dice que es una foto fija de septiembre de 2017). No pude confirmar qué versión de Kaggle es | [CSV en GitHub](https://raw.githubusercontent.com/amankharwal/Website-data/master/melb_data.csv), verificado en el box |
| Las cifras de la clase 2 contra las de FAMAF | En parte (corrijo mi apunte) | En el apunte comparé las cifras de José (contadas tras el `dropna`) con las del CSV de FAMAF **sin** el `dropna`. Comparando igual con igual: FAMAF con el mismo filtro da 13.518 filas, BuildingArea 6.417, CouncilArea 1.307, YearBuilt 5.344 y cuantil 99 = 467. El archivo de 18.396 tiene muchos más faltantes en Car (3.576 contra 62) | Verificado en el box |
| JUPITER es "la cuarta más grande del mundo" C1P1 7:18 | Sí, cuando lo dijo | Cuarta en las listas TOP500 de junio y noviembre de 2025 (que era la vigente en abril de 2026); quinta en la de junio de 2026. Rmax de 1.000 PFlop/s | [TOP500, JUPITER Booster](https://www.top500.org/system/180357/) |
| "El paper de Rubin de 1978" C1P1 32:08 | Sí, existe | Rubin, "Multiple imputations in sample surveys: a phenomenological Bayesian approach to nonresponse", actas de la sección de métodos de encuestas de la ASA, 1978: "The plan is to impute several values for each missing datum". MCAR y MAR vienen de Rubin (1976), *Biometrika* 63(3):581 a 592 (este solo lo vi en el buscador); las reglas para combinar, del libro de 1987 | [Rubin 1978, PDF de la ASA](http://www.asasrms.org/Proceedings/papers/1978_004.pdf) |
| El libro abierto sobre faltantes "en R" C1P1 12:16 | Sí, casi seguro | *Flexible Imputation of Missing Data* (2.ª ed.) de Stef van Buuren, libre en línea, con todo el código en R (`mice`) | [FIMD](https://stefvanbuuren.name/fimd/) |
| El cargo de Ariel: "director de ingeniería, plataforma, data" en Yalo C3P1 13:16 | En parte | La página del equipo docente dice "VP de tecnología y datos". Perfiles de terceros que solo vi en el buscador (neuron.com, signalhire) dicen "Director of Platform Engineering, Data & AI at Yalo", que coincide con lo que él dice. LinkedIn pide sesión; no lo abrí | [Equipo docente de la Diplomatura](https://diplodatos.famaf.unc.edu.ar/equipo-docente/) |
| Toeslagenaffaire: el fisco neerlandés usó la nacionalidad y cayó el gobierno C2P2 20:06 | Sí | El gobierno de Rutte renunció el 15/01/2021 después de que "thousands of families were wrongly accused of child welfare fraud". El uso de la nacionalidad en el modelo de riesgo lo sancionó la autoridad de datos neerlandesa (ese informe solo lo vi en el buscador) | [BBC, 15/01/2021](https://www.bbc.com/news/world-europe-55674146) |
| La bibliografía de la demostración de PCA: "el Fisher, William and Johnson" C2P2 1:06:17 | Sí, casi seguro | Johnson y Wichern, *Applied Multivariate Statistical Analysis*: capítulo 8 "Principal Components" y en el 11 "Fisher's Discriminant Function". Bonus: el capítulo 4 tiene "Detecting Outliers and Data Cleaning" y el 5 "Inferences about Mean Vectors When Some Observations Are Missing" | [Pearson, 6.ª ed. clásica](https://www.pearson.com/en-us/subject-catalog/p/Johnson-Applied-Multivariate-Statistical-Analysis-Classic-Version-6th-Edition/P200000006217/9780137980963) |
| "Hay papers" de que el modelo es una parte chica del sistema C3P1 56:25 | Sí | Sculley y otros, "Hidden Technical Debt in Machine Learning Systems", NeurIPS 2015. El resumen lista erosión de fronteras, entrelazamiento, ciclos de realimentación ocultos, consumidores no declarados, dependencias de datos, problemas de configuración y cambios en el mundo externo | [NeurIPS 2015](https://papers.nips.cc/paper/2015/hash/86df7dcfd896fcaf2674f757a2463eba-Abstract.html) |
| Modelos "como funciones SQL" de una conferencia de Google C3P1 1:00:51 | Sí, existe | BigQuery ML: "lets you create and run machine learning (ML) models by using either GoogleSQL queries or the Google Cloud console", y también llama a modelos de Gemini desde SQL. No sé a qué charla se refiere | [BigQuery ML](https://cloud.google.com/bigquery/docs/bqml-introduction) |
| "60% del tiempo en limpieza" C3P1 1:34:08 | Sí, pero es una encuesta de una empresa | El informe de CrowdFlower de 2016 dice "Cleaning and organizing data: 60%" y que es "the least enjoyable part". Conflicto de interés: CrowdFlower vendía limpieza y etiquetado de datos | [CrowdFlower 2016, PDF](https://www2.cs.uh.edu/~ceick/UDM/CFDS16.pdf) |
| Google etiquetando personas negras C3P1 1:42:53 | Sí | Google Photos, junio de 2015: el programador Jacky Alciné encontró que la app etiquetaba fotos de él y su novia como "gorillas" (no "monos"); Google pidió disculpas | [The Verge, 01/07/2015](https://www.theverge.com/2015/7/1/8880363/google-apologizes-photos-app-tags-two-black-people-gorillas) |
| Algoritmo de reincidencia sesgado (COMPAS) | Sí | ProPublica (Angwin y otros, 23/05/2016): el algoritmo marcaba falsamente como futuros delincuentes a acusados negros "at almost twice the rate as white defendants" | [ProPublica, Machine Bias](https://www.propublica.org/article/machine-bias-risk-assessments-in-criminal-sentencing) |
| "Juicios por varios millones" por COMPAS C3P1 1:43:28 | No encontré respaldo | El caso conocido es Loomis contra Wisconsin: la Corte de Wisconsin avaló el uso de COMPAS (881 N.W.2d 749, 2016), Loomis quedó condenado a 6 años y la Corte Suprema de EE. UU. rechazó revisarlo el 26/06/2017. No hubo indemnización. No encontré juicios millonarios | [Wikipedia, Loomis v. Wisconsin](https://en.wikipedia.org/wiki/Loomis_v._Wisconsin) |
| Fotos de Pokémon Go usadas "para una empresa de delivery tipo DHL" C3P1 1:44:00 | En parte | Niantic sí anunció (12/11/2024) un "Large Geospatial Model" entrenado con escaneos que los jugadores hacen de forma voluntaria ("Merely walking around playing our games does not train an AI model"). Entre las aplicaciones futuras nombra "logistics", pero no hay ningún cliente de delivery. Conflicto de interés: Niantic escribe sobre sí misma | [Niantic Spatial, blog](https://nianticspatial.com/blog/largegeospatialmodel) |
| "LatamGPT salió este año" C3P1 1:50:29 | Sí | Lanzado el martes 10/02/2026 en Chile, coordinado por CENIA, sobre Llama 3.1 70B, con más de 60 instituciones de 15 países. Conflicto de interés: es la página de CENIA, que coordina el proyecto, y menciona a AWS como socio | [CENIA, 10/02/2026](https://cenia.cl/2026/02/10/latam-gpt-la-primera-ia-regional-abierta-creada-con-datos-latinoamericanos/) |
| "Claude tendía a abstenerse y GPT a inventar" C3P2 17:21 | No verificable | Ariel mismo aclara que puede estar desactualizado. No busqué evaluaciones comparativas de alucinación; cualquier cifra cambia con cada versión | |
| "El Opus 4.7" como modelo actual C3P2 44:24 | Sí, en mayo de 2026 | Anthropic anunció Claude Opus 4.7 el 16/04/2026 como "generally available"; la clase fue el 08/05 | [Anthropic, 16/04/2026](https://www.anthropic.com/news/claude-opus-4-7) |
| "GPT salió el 5.5" C4P1 3:26 | Sí, en mayo de 2026 | OpenAI publicó GPT 5.5 el 23/04/2026 y lo abrió en la API el 24/04. Hoy la misma página ya remite a un modelo posterior. Solo afirmo lo que dicen esas dos páginas | [OpenAI, 23/04/2026](https://openai.com/index/introducing-gpt-5-5/) |
| Postgres hace búsqueda vectorial C3P2 1:00:48 | Sí | Con la extensión pgvector: "Open-source vector similarity search for Postgres", búsqueda exacta y aproximada con índices HNSW e IVFFlat, y cuantización | [pgvector](https://github.com/pgvector/pgvector) |
| La encuesta salarial 2020 | Sí | `sysarmy_survey_2020_processed.csv`, 6.095 filas × 48 columnas | Verificado en el box |
| La versión de pandas en Colab durante la materia | Resuelto (corrijo mi apunte) | El archivo `pip-freeze.txt` del repositorio oficial de Colab, en los commits del 24/04/2026 y del 08/05/2026, lista pandas 2.2.2, numpy 2.0.2, scikit-learn 1.6.1, SQLAlchemy 2.0.49 y **missingno 0.5.2 ya instalado**. O sea: en clase el texto era dtype `object` (y `None` quedaba como `None`), y el `!pip install missingno` no hacía falta. En agosto de 2026 Colab pasó a pandas 2.2.3 y Python 3.13 | [googlecolab/backend-info](https://github.com/googlecolab/backend-info/blob/main/pip-freeze.txt) |
| Fecha del entregable 2 C4P2 1:25:36 | No verificable | El calendario público de la cohorte 2026 confirma las fechas de las clases (24 y 25 de abril, 8 y 9 de mayo) pero no las de los entregables | [Calendario de la Diplomatura](https://diplodatos.famaf.unc.edu.ar/calendar/) |
| Adult se extrajo del censo de 1994 C2P2 40:03 | Sí | "Extraction was done by Barry Becker from the 1994 Census database"; donado a UCI el 30/04/1996 por Barry Becker y Ronny Kohavi | [UCI, Adult](https://archive.ics.uci.edu/dataset/2/adult) |

### 2. Nombres y dudas de la transcripción, resueltos

| En la transcripción | Es | Fuente |
|---|---|---|
| Yuli | Jülich, donde está JUPITER | [TOP500](https://www.top500.org/system/180357/) |
| Sens Soccer | Census, el censo de EE. UU. de 1994 | [UCI, Adult](https://archive.ics.uci.edu/dataset/2/adult) |
| el Fisher, William and Johnson | Johnson y Wichern | [Pearson](https://www.pearson.com/en-us/subject-catalog/p/Johnson-Applied-Multivariate-Statistical-Analysis-Classic-Version-6th-Edition/P200000006217/9780137980963) |
| FAIR, "F, accessible, reproduce y no me acuerdo" | Findable, Accessible, Interoperable, Reusable; Wilkinson y otros, *Scientific Data*, publicado el 15/03/2016 | [Nature Scientific Data](https://www.nature.com/articles/sdata201618) |
| el paper de Rubin | Rubin 1976 (mecanismos), 1978 (imputación múltiple), 1987 (libro y reglas de combinación) | [Rubin 1978](http://www.asasrms.org/Proceedings/papers/1978_004.pdf), [FIMD 2.3.2](https://stefvanbuuren.name/fimd/sec-whyandwhen.html) |
| destilación (para achicar vectores) | La destilación es otra cosa: "compress the knowledge in an ensemble into a single model" (Hinton, Vinyals y Dean, 2015). Lo que achica vectores con colisiones a propósito es LSH | [arXiv 1503.02531](https://arxiv.org/abs/1503.02531) |
| hashing que achica el vector "y baja la colisión" | LSH: "hash collisions are maximized, not minimized" | [Wikipedia, LSH](https://en.wikipedia.org/wiki/Locality-sensitive_hashing) |
| bases vectoriales en Postgres | pgvector, con índices HNSW e IVFFlat | [pgvector](https://github.com/pgvector/pgvector) |
| medallion, bronce, plata, oro | La arquitectura medallion de Databricks | [Databricks](https://www.databricks.com/glossary/medallion-architecture) |
| las funciones SQL de Google | BigQuery ML | [BigQuery ML](https://cloud.google.com/bigquery/docs/bqml-introduction) |
| el modelo de Pokémon | El Large Geospatial Model de Niantic Spatial | [Niantic Spatial](https://nianticspatial.com/blog/largegeospatialmodel) |

### 3. Las correcciones de la clase, con fuentes

Estas correcciones ya estaban en el apunte; acá van con la documentación que las respalda.

#### 3.1 isna e isnull son lo mismo

**Qué dice la fuente.** En la clase 2 José dice que `isnull` es "un poco más amplio" que `isna` C2P1 21:21; en la clase 4 Ariel dice que "son ligeramente distintos, por algo son dos métodos" C4P1 32:40, y José abre la documentación y concluye "es exactamente lo mismo, lo han unificado, esto es nuevo" C4P1 35:36.

**Qué suma el material externo.** La documentación de pandas 3.0.6 dice textualmente "DataFrame.isnull is an alias for DataFrame.isna" (y lo mismo para Series). No es nuevo: las notas de pandas 0.21 (2017) explican que se agregaron `isna()` y `notna()` "that are aliases for isnull() and notnull()" para que los nombres fueran coherentes con `dropna()` y `fillna()`.

**Cómo implementarlo.** Elegí uno (te sugiero `isna`, por coherencia con `dropna` y `fillna`) y usalo siempre. La guía, sección 1, lo comprueba con NaN, None, NaT y `pd.NA`.

#### 3.2 Por qué NaN no es igual a NaN

**Qué dice la fuente.** José explica que `np.nan == np.nan` da `False` "porque son instancias distintas en memoria" C1P2 22:45.

**Qué suma el material externo.** Es una regla del estándar de punto flotante, no de la memoria. Wikipedia resume la tabla de comparaciones de IEEE 754: con NaN, los predicados ≥, ≤, >, < y = dan falso y ≠ da verdadero, así que "x ≠ x" es verdadero solo si x es NaN; la página también cuenta que el uso sistemático de NaN lo introdujo IEEE 754 en 1985. La documentación de numpy dice que "NumPy uses the IEEE Standard for Binary Floating-Point for Arithmetic (IEEE 754)". La guía de faltantes de pandas marca la diferencia con `pd.NA`: "This deviates from the behaviour of np.nan, where comparisons with np.nan always return False"; `pd.NA == pd.NA` da `<NA>`, y en operaciones lógicas sigue "the three-valued logic (or Kleene logic, similarly to R, SQL and Julia)".

**Cómo implementarlo.** `s.isna()` para filtrar, `math.isnan(x)` o `np.isnan(x)` para un número suelto, y nunca `x == np.nan`. Si querés enteros con faltantes, `astype("Int64")`, y ahí las comparaciones con faltante dan `<NA>`, no `False`.

#### 3.3 Imputación múltiple y reglas de Rubin

**Qué dice la fuente.** José presenta bien la idea de combinar varianza dentro y entre imputaciones C1P3 41:18, pero describe el método como "agarrar subconjuntos del conjunto de datos e imputar en los subconjuntos" C1P3 41:50, C1P3 52:59.

**Qué suma el material externo.** Rubin (1978) lo plantea desde el resumen: "impute several values for each missing datum, where the imputed values reflect variation within an imputation model and sensitivity to different imputation models". van Buuren, sección 2.3.2, da las fórmulas: la estimación combinada es el promedio de las m estimaciones, y la varianza total es T = Ū + (1 + 1/m)B, "referred to as Rubin's rules". Ū es la varianza promedio dentro de cada copia, B la varianza entre copias y B/m el costo extra de usar un m finito; si omitís B/m, los p valores salen demasiado chicos. Sobre cuántas copias: "Traditional choices for m are m=3, m=5 and m=10. The current advice is to set m higher, e.g., m=50". La guía de scikit-learn lo dice desde su lado: `IterativeImputer` "differs from [MICE] by returning a single imputation instead of multiple imputations", y para imputación múltiple hay que repetirlo con `sample_posterior=True` y semillas distintas.

**Cómo implementarlo.** La guía, sección 3, tiene el código con m = 5 copias y las reglas de Rubin a mano. Subí m a 20 o 50 si la fracción de faltantes es grande (en Melbourne, BuildingArea tiene 47,5%).

#### 3.4 IterativeImputer es experimental y no es MICE

**Qué dice la fuente.** José traduce MICE como "imputación múltiple con ecuaciones encadenadas" C1P3 5:36 y presenta `IterativeImputer` como la versión de scikit-learn.

**Qué suma el material externo.** La página de `IterativeImputer` en scikit-learn 1.9.1: "This estimator is still experimental for now: the predictions and the API might change without any deprecation cycle", y hay que importar antes `sklearn.experimental.enable_iterative_imputer`. La misma página advierte "Depending on the nature of missing values, simple imputers can be preferable in a prediction context", da un costo de O(knp³ min(n, p)) y remite al paquete `mice` de van Buuren. La sigla MICE es "Multivariate Imputation by Chained Equations", como figura en la guía de scikit-learn. Esa misma guía reconoce que "It is still an open problem as to how useful single vs. multiple imputation is in the context of prediction and classification".

**Cómo implementarlo.** Si lo usás en un entregable, fijá la versión de scikit-learn y dejá el import experimental explícito. Para predecir, compará siempre contra la mediana y contra un modelo con NaN nativo (sección 4): en Melbourne no le ganó a ninguno de los dos con árboles.

#### 3.5 KNNImputer no necesita filas completas

**Qué dice la fuente.** A la pregunta de si KNN busca vecinos con filas completas, José responde "sí" C1P3 28:29.

**Qué suma el material externo.** La guía de scikit-learn: "By default, a euclidean distance metric that supports missing values, nan_euclidean_distances, is used to find the nearest neighbors. Each missing feature is imputed using values from n_neighbors nearest neighbors that have a value for the feature." O sea, al vecino solo se le pide tener la variable que se imputa.

**Cómo implementarlo.** Escalá antes de imputar (si no, Landsize en metros cuadrados domina la distancia) y medí el tiempo: en el benchmark tardó 22 a 31 s contra menos de 1 s de la mediana con Ridge.

#### 3.6 MNAR: "no imputen, tiren la variable"

**Qué dice la fuente.** La diapositiva dice que con MNAR "no imputen, es mejor tirar esa variable" C1P3 7:15.

**Qué suma el material externo.** El índice de FIMD dedica la sección 3.8 a los faltantes no ignorables, con su análisis de sensibilidad (3.8.5), y discute el "indicator method" (1.3.7) como método ad hoc con limitaciones para estimar. Para **predecir**, la guía de scikit-learn dice que "preserving the information about which values had been missing can be informative" y por eso trae `MissingIndicator` y `add_indicator`. Mi sección 5 muestra el caso: si faltan justamente las casas grandes, la regresión lineal con media más indicador queda igual que sin faltantes.

**Cómo implementarlo.** Para predecir: indicador más imputación simple, o un modelo con NaN nativo. Para estimar: probá dos o tres supuestos sobre los faltantes (por ejemplo, sumar un δ a los valores imputados, el "δ adjustment" del capítulo 9.2 de van Buuren) y mostrá cuánto cambia la conclusión.

#### 3.7 Medallion: formatear es plata, no oro

**Qué dice la fuente.** Ariel dice que el formateo de fechas "va en la capa gold" C4P2 1:06:45 y después pone la agregación por código postal como oro C4P2 1:04:32.

**Qué suma el material externo.** El glosario de Databricks: bronce es el dato crudo "as-is" más metadatos; en plata los datos se "matched, merged, conformed and cleansed ('just-enough')" para dar una "Enterprise view"; oro es para "business level aggregates" y modelos tipo Kimball (estrella) o Inmon (data marts). El mismo texto aclara que en oro se aplica "the final layer of data transformations and data quality rules", así que puede haber reglas de calidad también ahí, pero el formateo de fechas es "conform", o sea plata. Conflicto de interés: Databricks vende el lakehouse en el que se apoya esta arquitectura.

**Cómo implementarlo.** En el entregable 2: bronce = los dos CSV tal cual, plata = fechas con `pd.to_datetime`, zipcode como entero, centinelas a NaN, duplicados fuera; oro = la tabla de Airbnb agregada por código postal y combinada con las ventas.

#### 3.8 Hashing, destilación y bases vectoriales

**Qué dice la fuente.** Ante una pregunta, Ariel dice que con "destilación, un vector de 1000 lo metés en un hashing y lo achicás a 10, donde la probabilidad de colisión es menor" C3P2 1:05:24.

**Qué suma el material externo.** Son tres cosas distintas. La destilación (Hinton y otros, 2015) entrena un modelo chico para imitar a uno grande: "compress the knowledge in an ensemble into a single model". El hashing sensible a la localidad (LSH) sí reduce la dimensión, pero busca lo contrario de lo que dijo: "hash collisions are maximized, not minimized", para que vectores parecidos caigan en el mismo balde. Y pgvector, la extensión de Postgres que nombró antes C3P2 1:00:48, usa índices aproximados HNSW e IVFFlat y cuantización para comprimir vectores.

**Cómo implementarlo.** Si necesitás búsqueda vectorial en el trabajo práctico, `CREATE EXTENSION vector` en Postgres con un índice HNSW alcanza para millones de vectores; no hace falta inventar un hash.

### 4. Benchmark 1: imputar o no imputar (Melbourne)

**La pregunta.** La materia elige a mano entre tirar filas, la media, la mediana, KNN e `IterativeImputer`, y lo evalúa mirando histogramas antes y después C2P1 51:35. Para predecir, lo que importa es otra cosa: el error del modelo. Acá comparo todas esas imputaciones con un modelo lineal y con árboles, contra no imputar (NaN nativo) y contra agregar un indicador de faltante.

```python
# bench_imputacion.py (resumen; entorno aparte con scikit-learn 1.9.1 y XGBoost 3.4.1)
df = pd.read_csv("data/melb_data.csv")                      # 13.580 filas de FAMAF
y = np.log(df["Price"])                                     # error en log = error relativo
NUM = ["Rooms", "Distance", "Bedroom2", "Bathroom", "Car", "Landsize", "BuildingArea",
       "YearBuilt", "Lattitude", "Longtitude", "Propertycount", "year", "month"]
CAT = ["Type", "Method", "Regionname", "CouncilArea"]        # NaN de CouncilArea como "Falta"
imputadores = {"media": SimpleImputer(), "mediana": SimpleImputer(strategy="median"),
               "KNN": make_pipeline(StandardScaler(), KNNImputer(n_neighbors=5)),
               "Iterative": IterativeImputer(random_state=0)}   # cada uno con y sin add_indicator
# Ridge (one hot) y HistGradientBoosting (categóricas nativas), con el imputador DENTRO del Pipeline
# más HGB y XGBoost sin imputar (NaN nativo); KFold(5, shuffle=True, random_state=0)
```

Faltantes numéricos en el CSV de FAMAF: BuildingArea 6.450 (47,5%), YearBuilt 5.375 (39,6%), Car 62.

**Resultados.** RMSE en log del precio (más bajo es mejor; 0,178 equivale más o menos a un error típico de 19% en el precio), con el desvío entre los 5 folds, R², error absoluto mediano en porcentaje y segundos totales de los 5 folds.

| Modelo | Faltantes | RMSE log (± sd) | R² | Error mediano | Segundos |
|---|---|---|---|---|---|
| Ridge | media | 0,2865 ± 0,027 | 0,701 | 17,9% | 0,8 |
| Ridge | media + indicador | 0,2862 ± 0,027 | 0,702 | 17,9% | 0,5 |
| Ridge | mediana | 0,2857 ± 0,025 | 0,703 | 17,9% | 0,7 |
| Ridge | mediana + indicador | 0,2862 ± 0,027 | 0,702 | 17,9% | 0,4 |
| Ridge | KNN | 0,2755 ± 0,024 | 0,724 | 17,3% | 23,1 |
| Ridge | KNN + indicador | 0,2754 ± 0,024 | 0,724 | 17,3% | 22,0 |
| Ridge | Iterative | 0,2790 ± 0,026 | 0,717 | 17,3% | 3,6 |
| Ridge | Iterative + indicador | 0,2789 ± 0,025 | 0,717 | 17,3% | 3,3 |
| HGB | media | 0,1784 ± 0,002 | 0,885 | 10,4% | 5,1 |
| HGB | mediana | 0,1783 ± 0,002 | 0,885 | 10,4% | 4,9 |
| HGB | mediana + indicador | 0,1783 ± 0,002 | 0,885 | 10,4% | 5,1 |
| HGB | KNN | 0,1814 ± 0,002 | 0,881 | 10,7% | 30,7 |
| HGB | KNN + indicador | 0,1805 ± 0,002 | 0,883 | 10,6% | 28,0 |
| HGB | Iterative | 0,1809 ± 0,002 | 0,882 | 10,7% | 6,8 |
| HGB | Iterative + indicador | 0,1795 ± 0,002 | 0,884 | 10,5% | 7,4 |
| HGB | **nativo (sin imputar)** | **0,1779 ± 0,002** | **0,886** | 10,5% | 4,7 |
| XGBoost | **nativo (sin imputar)** | **0,1726 ± 0,003** | **0,893** | 10,0% | 2,9 |
| XGBoost | mediana + indicador | 0,1725 ± 0,003 | 0,893 | 10,0% | 2,6 |

**Qué muestra.**

- **El modelo pesa diez veces más que la imputación.** Pasar de Ridge a árboles baja el RMSE de 0,28 a 0,18. Cambiar de imputación dentro de un mismo modelo lo mueve, como mucho, 0,011 (Ridge) o 0,0035 (HGB).
- **Con árboles, no imputar gana o empata.** HGB nativo (0,1779) queda dentro del ruido de la media y la mediana (desvío 0,002) y **por encima** de KNN e Iterative, que empeoran el error y tardan más. XGBoost nativo y XGBoost con mediana más indicador empatan.
- **Con un modelo lineal, la imputación sí importa.** KNN mejora a Ridge de 0,286 a 0,275, porque rellena BuildingArea con un valor plausible según los vecinos. Pero cuesta 30 veces más tiempo, y aun así el peor árbol es mucho mejor que el mejor Ridge.
- **El indicador casi no cambia nada acá**, porque en Melbourne la falta de BuildingArea y YearBuilt parece poco informativa sobre el precio. La sección siguiente muestra qué pasa cuando sí lo es.
- Límite: es un solo dataset, un solo esquema de validación cruzada (5 folds, una semilla) y sin ajustar hiperparámetros. Las diferencias de 0,0005 son ruido.

### 5. Benchmark 2: cuando la falta es informativa (faltantes inyectados)

**La pregunta.** ¿Qué pasa si los faltantes no son al azar? Tomé las 6.764 filas de Melbourne con BuildingArea entre 20 y 1000 m² y sin faltantes en Car ni YearBuilt, y le borré a BuildingArea un 40% de dos maneras: al azar (MCAR) y con más probabilidad cuanto más grande es la casa (MNAR, con una logística sobre el log del área). Así conozco la verdad y puedo comparar contra el modelo sin faltantes.

```python
# bench_mnar.py (resumen)
z = (np.log(df.BuildingArea) - np.log(df.BuildingArea).mean()) / np.log(df.BuildingArea).std()
masks = {"MCAR 40%": rng.random(len(df)) < 0.40,
         "MNAR 40%": rng.random(len(df)) < 1 / (1 + np.exp(-(2.5 * z - 0.45)))}   # faltan las grandes
# Ridge con media o Iterative, con y sin indicador; HGB con media, Iterative o NaN nativo; KFold(5)
```

**Resultados.** RMSE en log del precio (desvío entre folds de 0,009 a 0,012).

| Modelo | Faltantes | Sin faltantes | MCAR 40% | MNAR 43% (faltan las grandes) |
|---|---|---|---|---|
| Ridge | media | 0,2621 | 0,2699 | 0,2710 |
| Ridge | media + indicador | 0,2621 | 0,2699 | **0,2620** |
| Ridge | Iterative | 0,2621 | 0,2678 | 0,2685 |
| Ridge | Iterative + indicador | 0,2621 | 0,2679 | 0,2646 |
| HGB | media | 0,1760 | 0,1868 | 0,1814 |
| HGB | Iterative | 0,1760 | 0,1857 | 0,1831 |
| HGB | nativo | 0,1760 | 0,1860 | 0,1813 |

Tiempos: Ridge de 0,1 a 0,7 s y HGB de 3,4 a 4,8 s por configuración.

**Qué muestra.**

- **Con MCAR, el indicador no sirve de nada** (0,2699 con y sin) y la imputación iterativa recupera un poco (0,2678), porque usa las otras variables para adivinar el área.
- **Con MNAR, el indicador es lo que más ayuda.** Ridge con media más indicador (0,2620) queda igual que sin faltantes: el hecho de que falte ya dice "casa grande". La imputación iterativa sin indicador (0,2685) es peor que la media con indicador, porque imputa un valor "promedio condicional" que justamente subestima las casas grandes.
- **Los árboles con NaN nativo aprovechan la falta solos** (0,1813 en MNAR contra 0,1860 en MCAR): aprenden de qué lado de cada corte mandar los faltantes. `IterativeImputer` con árboles empeora en MNAR (0,1831) porque borra esa señal.
- Esto contradice la diapositiva de "con MNAR, tirá la variable": para predecir, la falta informativa es una variable más. Para estimar el efecto del área sobre el precio, en cambio, ninguna de estas opciones corrige el sesgo; ahí va el análisis de sensibilidad (sección 3.6).

### 6. Benchmark 3: faltantes categóricos (Adult)

**La pregunta.** En Adult los faltantes son "?" en tres columnas categóricas. ¿Conviene la moda, una categoría propia, el NaN nativo o borrar las filas?

Hay 2.399 filas con algún "?" (7,4%): workclass 1.836, occupation 1.843, native_country 583. La falta es informativa: gana más de 50 mil el 13,9% de las filas con faltante contra el 24,9% de las completas.

```python
# bench_adult.py (resumen): StratifiedKFold(5), AUC de la curva ROC
df = pd.read_csv("data/adult.data", names=cols, skipinitialspace=True, na_values="?")
# LogisticRegression con one hot; HGB con OrdinalEncoder y categóricas nativas
# opciones: moda, constante "Falta", moda + indicador, NaN nativo, borrar filas solo en train
```

| Modelo | Faltantes | AUC (± sd) | Exactitud | Segundos |
|---|---|---|---|---|
| Regresión logística | moda | 0,9057 ± 0,004 | 0,851 | 1,1 |
| Regresión logística | categoría "Falta" | 0,9068 ± 0,004 | 0,852 | 1,1 |
| Regresión logística | moda + indicador | 0,9068 ± 0,004 | 0,852 | 1,2 |
| HGB | moda | 0,9279 ± 0,003 | 0,875 | 2,2 |
| HGB | categoría "Falta" | 0,9283 ± 0,002 | 0,874 | 2,2 |
| HGB | NaN nativo | 0,9283 ± 0,002 | 0,874 | 2,3 |
| HGB | borrar filas en train (y evaluar en todas) | 0,9278 ± 0,003 | | |

**Qué muestra.** Las diferencias son chicas (Adult tiene pocos faltantes), pero van todas para el mismo lado: la categoría propia o el indicador le ganan a la moda, y HGB con NaN nativo da **idéntico** a la categoría "Falta" (para categóricas, el NaN nativo es justamente tratar la falta como una categoría más). Borrar filas no ganó nada y en producción igual vas a recibir filas con "?", así que tenés que imputar de todos modos. Es lo mismo que recomienda Kimball para las dimensiones: "substituting a descriptive string, such as Unknown or Not Applicable in place of the null value".

### 7. Benchmark 4: pandas, DuckDB y Polars en el ETL de la clase 4

**La pregunta.** La clase 4 agrupa Airbnb por código postal y lo combina con las ventas de Melbourne C4P2 1:04:32. ¿Cuánto cambia el motor? Repetí la operación con los datos tal cual y con los dos archivos replicados 50 veces.

```python
# bench_motores.py (resumen): mejor de 5 corridas
g = A.groupby("zipcode").agg(n=("price", "count"), price_mean=("price", "mean"),
                             weekly_mean=("weekly_price", "mean")).reset_index()
M.merge(g, how="left", left_on="Postcode", right_on="zipcode", validate="many_to_one")   # pandas
duckdb.sql("WITH g AS (SELECT zipcode, COUNT(price) n, AVG(price) price_mean, ... GROUP BY zipcode) "
           "SELECT M.*, g.* FROM M LEFT JOIN g ON M.Postcode = g.zipcode").df()             # DuckDB
M_pl.join(A_pl.group_by("zipcode").agg(...), left_on="Postcode", right_on="zipcode", how="left")  # Polars
```

| Datos | pandas | DuckDB (resultado a pandas) | Polars | Polars lazy |
|---|---|---|---|---|
| Tal cual: 22.895 publicaciones, 13.580 ventas | 8,0 ms | 29,6 ms | 1,2 ms | 1,0 ms |
| × 50: 1.144.750 publicaciones, 679.000 ventas | 320 ms | 685 ms | 17 ms | 17 ms |

Las cuatro versiones devuelven las mismas filas y las mismas 20 ventas (× 50 = 1.000) sin dato de Airbnb para su código postal.

**Leer el CSV crudo de Airbnb** (96 MB, 84 columnas, con saltos de línea dentro de algunas celdas):

| Motor | Resultado | Tiempo |
|---|---|---|
| pandas, motor C | 22.895 × 84 | 0,99 s |
| pandas, motor `pyarrow` | Falla: "CSV parser got out of sync… cell values spanning multiple lines" | |
| Polars, inferencia por defecto | Falla: no puede convertir "62 618 882 698" a entero en la columna `license` | |
| Polars, `infer_schema_length=None` | 22.895 × 84 | 0,32 s |
| DuckDB a pandas | 22.895 × 84 | 0,65 s |
| DuckDB, solo contar filas | 22.895 | 0,44 s |

**Qué muestra.**

- A la escala de la materia, el motor no importa: todo tarda milisegundos y el costo real es leer el CSV.
- A 50 veces el volumen, Polars hace la transformación unas 18 veces más rápido que pandas. DuckDB salió el más lento en esta prueba, pero es injusto con DuckDB: el tiempo incluye escanear DataFrames de pandas y convertir 679.000 filas × 25 columnas de vuelta a pandas. Mi tiempo de Polars, en cambio, no incluye la conversión inicial desde pandas.
- La robustez cuenta tanto como la velocidad: con datos sucios, el motor C de pandas y DuckDB leyeron el archivo a la primera, y los motores más estrictos fallaron. Que Polars falle por un tipo mal inferido es bueno (te avisa), pero hay que saberlo.

### 8. Calidad de datos como código: contratos, validación y perfilado automático

**Qué dice la fuente.** Ariel enumera las dimensiones de calidad: completitud, validez (una superficie negativa), precisión, integridad (una venta sin cliente), duplicados y temporalidad C3P2 40:58. En la práctica, la materia las revisa a ojo en la notebook: `describe()`, histogramas, cuantiles, `value_counts()`. En el modern data stack nombra dbt como herramienta de transformación, pero no muestra ningún test de datos.

**Qué suma el material externo.**

- **pandera** valida DataFrames en tiempo de ejecución: "The goal of Pandera is to make data processing pipelines more readable and robust with statistically typed dataframes", con chequeos por columna, pruebas de hipótesis y un esquema por clases al estilo pydantic. Es software libre y no vende nada en esa página.
- **Great Expectations (GX Core 1.23)**: "An Expectation is a verifiable assertion about data… Similar to assertions in traditional Python unit tests"; los Checkpoints corren las validaciones en producción y los Data Docs son la documentación legible que se genera sola. Conflicto de interés: la empresa vende GX Cloud.
- **Soda** se define como "a data quality platform" que permite "Define data contracts, making expectations explicit" y testear "as part of CI/CD workflows". Conflicto de interés: es una plataforma comercial y la página termina en "Contact us".
- **dbt**: "Data tests are assertions you make about your models", con `not_null`, `unique` y relaciones entre tablas listas para usar; un test pasa si la consulta que busca filas que lo violan devuelve cero filas. Los **model contracts** son "upfront guarantees" sobre nombres y tipos de columnas: si el modelo no los cumple, "it will fail to build". Ojo: los contratos no se aplican a modelos en Python. Conflicto de interés: dbt Labs vende dbt Cloud.
- **ydata-profiling** promete EDA "with a single line of code". Hoy el paquete se renombró: el repositorio dice "ydata-profiling is now fg-data-profiling… the old package will no longer receive updates", y el `import` de la versión 4.18.4 tira la misma advertencia.

**Cómo implementarlo.** Escribí el contrato de Melbourne con lo que la materia descubrió a mano y corrélo sobre el CSV de FAMAF:

```python
# contrato_pandera.py (pandera 0.33.1)
ventas = pa.DataFrameSchema({
    "Price": Column(float, Check.gt(0)),
    "Rooms": Column(int, Check.in_range(1, 12)),
    "Type": Column(str, Check.isin(["h", "u", "t"])),
    "Postcode": Column(float, Check.in_range(3000, 3999)),
    "Car": Column(float, Check.in_range(0, 12), nullable=True),
    "BuildingArea": Column(float, [Check.gt(0), Check.le(3000)], nullable=True),
    "YearBuilt": Column(float, Check.in_range(1800, 2018), nullable=True),
    "Date": Column(str, Check.str_matches(r"^\d{1,2}/\d{1,2}/\d{4}$")),
}, checks=[Check(lambda d: d["BuildingArea"].isna().mean() < 0.50, error="más de 50% faltante")])
ventas.validate(pd.read_csv("data/melb_data.csv"), lazy=True)   # lazy: junta todas las fallas
```

Resultado, en 0,26 s: 22 fallas. BuildingArea = 0 en 17 casas, BuildingArea mayor a 3000 en 4 (3.112, 3.558, 6.791 y 44.515 m²) y YearBuilt = 1196 en 1. La regla de "menos de 50% faltante" pasa por poco (47,5%), y si la próxima versión del archivo trae más faltantes, el contrato avisa.

Para comparar, **ydata-profiling** sobre el mismo archivo:

| Modo | Tiempo | Alertas | Qué marcó |
|---|---|---|---|
| `minimal=True` | 4,9 s | 7 | Faltantes de BuildingArea (47,5%), YearBuilt (39,6%) y CouncilArea (10,1%); asimetría de Landsize y BuildingArea; ceros en Car (1.026) y Landsize (1.939) |
| completo | 18,1 s | 18 | Lo mismo más 11 alertas de correlación alta (Rooms con Bedroom2 y Bathroom, CouncilArea con Regionname y Postcode, y así) |

Ninguno de los dos modos marcó los 34 baños en 0, las 17 superficies en 0, el 44.515 ni el año 1196: el perfilado ve distribuciones, no sabe qué es imposible en tu dominio. Sirve para el primer pantallazo y para el informe (el HTML queda lindo), pero el contrato es el que atrapa los errores.

**Sugerencia.** Para el entregable 2, sumá a la notebook una celda con el esquema de pandera de la tabla final (la combinada con Airbnb) y validala antes de guardarla en SQLite. Es el equivalente en pandas de los tests de dbt y te obliga a escribir lo que suponés de cada columna.

### 9. Arquitectura y teoría de la limpieza: Kimball, lakehouse, Rahm y Do, tidy data

**Qué dice la fuente.** Ariel presenta ETL contra ELT, data warehouse contra data lake, el modern data stack y la arquitectura medallion C4P2 1:04:32.

**Qué suma el material externo.**

- **Kimball.** La página de técnicas del Kimball Group resume el modelado dimensional de *The Data Warehouse Toolkit* (3.ª ed.): proceso de diseño en cuatro pasos, proceso de negocio, grano, hechos y dimensiones, esquema estrella, dimensiones conformadas. Tiene entradas específicas sobre "Nulls in fact tables" y "Null attributes in dimensions"; en la segunda recomienda reemplazar el null por "Unknown" o "Not Applicable". Conflicto de interés: el Kimball Group vende libros y cursos.
- **Lakehouse.** Databricks lo define como "a new, open data management architecture that combines the flexibility, cost-efficiency, and scale of data lakes with the data management and ACID transactions of data warehouses". Kimball y lakehouse no son rivales: el glosario de medallion de Databricks dice que la capa oro puede tener un esquema estrella al estilo Kimball. Conflicto de interés: Databricks vende el lakehouse.
- **Rahm y Do (2000)**, "Data Cleaning: Problems and Current Approaches", *IEEE Data Engineering Bulletin*. Clasifican los problemas en "single-source and multi-source problems and between schema- and instance-related problems" y dicen que en un data warehouse la limpieza "is a major part of the so-called ETL process". La combinación de Melbourne con Airbnb es un caso de manual de problema multifuente: el mismo código postal como texto en una tabla y como número en la otra, el estado escrito "VIC", "Vic" y "Victoria" C4P2 16:37.
- **Tidy data (Wickham, 2014)**, *Journal of Statistical Software* 59(10): "each variable is a column, each observation is a row, and each type of observational unit is a table". La última parte explica por qué Airbnb (publicaciones) y Melbourne (ventas) son dos tablas que se combinan por una clave y no una sola planilla desde el origen.
- **Reis y Housley, *Fundamentals of Data Engineering* (O'Reilly, 2022)** y **Strengholt, *Data Management at Scale* (2.ª ed., O'Reilly, 2023).** Las páginas de O'Reilly me devolvieron 403; solo vi en el buscador que el primero organiza todo en un "ciclo de vida" (generación, almacenamiento, ingesta, transformación y servicio, más corrientes transversales como DataOps y orquestación) y que el segundo trata arquitectura descentralizada, data mesh y data fabric. No los cito más allá de eso.

**Cómo implementarlo.** En el informe del entregable, nombrá cada problema con la taxonomía de Rahm y Do (por ejemplo, "multifuente, de instancia: códigos postales sin correspondencia") y ubicá cada paso en bronce, plata u oro. Para la tabla final, pensá el grano (una fila por venta) antes de combinar; con `validate="many_to_one"` en `merge`, pandas te avisa si el grano se rompe.

### 10. Libros y documentación: qué sacar de cada uno

| Recurso | Qué sacar | Para qué parte de la materia |
|---|---|---|
| van Buuren, *Flexible Imputation of Missing Data* (2.ª ed., libre) | 1.3.7 "Indicator method"; 2.3.2 reglas de Rubin; 2.6 "Imputation is not prediction"; 2.8 cuántas imputaciones; 3.8 faltantes no ignorables y sensibilidad; 5.1.2 por qué no promediar las copias | Clases 1 y 2 |
| Guía de imputación de scikit-learn | Imputación univariada, multivariada, KNN, `MissingIndicator`, "Multiple vs. Single Imputation" | Clase 2 |
| Ejemplo "Imputing missing values before building an estimator" de scikit-learn | Compara 0, media, KNN e iterativa, **siempre con indicador**, sobre diabetes y California con faltantes artificiales y un RandomForest. Ojo: son faltantes inventados y usa solo 300 filas de cada dataset | Clase 2 |
| Documentación de `HistGradientBoosting` | "built-in support for missing values (NaNs)": en cada corte aprende si los faltantes van a la izquierda o a la derecha | Benchmark de la sección 4 |
| Preguntas frecuentes de XGBoost | "XGBoost supports missing values by default… branch directions for missing values are learned"; ojo que el booster lineal los trata como ceros | Ídem |
| Rubin (1978) | La idea original de imputar varias veces | Clase 1 |
| Johnson y Wichern | Capítulo 4 (outliers y limpieza), 5 (medias con observaciones faltantes), 8 (PCA), 11 (Fisher) | Clase 2 |
| Rahm y Do (2000) | La taxonomía de problemas de calidad (una fuente o varias, esquema o instancia) | Clases 3 y 4 |
| Wickham (2014) | Las tres reglas de tidy data (una variable por columna, una observación por fila, una tabla por tipo de unidad) | Clase 4 |
| Sculley y otros (2015) | Deuda técnica de datos: dependencias de datos, cambios en el mundo externo | Clase 3 |
| Josse y otros (2019) y Perez-Lebel y otros (2022) | La teoría y la evidencia de que, para predecir, imputar con una constante es consistente si la falta no es informativa y que los árboles con NaN nativo predicen mejor y más rápido. Conflicto de interés: Varoquaux, coautor de los dos, es uno de los creadores de scikit-learn | Análisis adversario |

### 11. Correcciones a mis archivos de la primera parte

1. **Las cifras de la clase 2 y el archivo de 18.396 filas.** En el apunte (módulo 5) dejé "para verificar" qué archivo era y comparé las cifras de José con las del CSV de FAMAF **sin** filtrar (62, 6.450, 1.369). Comparé mal: José cuenta después de `dropna(subset=["Car"])`. El archivo está identificado (una copia de 18.396 × 22 que reproduce todas sus cifras) y, con el mismo filtro, FAMAF da 13.518 filas, BuildingArea 6.417, CouncilArea 1.307, YearBuilt 5.344 y cuantil 99 = 467 (no 466,42, que era sin filtrar). La guía (sección 2) ya decía "tras dropna" y está bien.
2. **La versión de pandas en Colab.** En el apunte (módulo 2) quedó "para verificar". Era pandas 2.2.2, así que la explicación de José (en texto, `None` queda como `None`) era correcta **para su entorno**; en mi box con pandas 3.0.6 cambia. Además, missingno 0.5.2 ya venía instalado en Colab y el SQLAlchemy de Colab era 2.0.49, así que el error de `execute` con texto plano que vimos en la guía también pasaba en Colab.
3. **"El paper de Rubin de 1978".** En el apunte puse que "puede que se refiera" a un trabajo de 1978. Existe y lo abrí: "Multiple imputations in sample surveys", actas de la ASA, 1978.
4. **Resueltos sin cambios de fondo:** JUPITER (cuarta cuando lo dijo, quinta desde junio de 2026), van Buuren, Johnson y Wichern, Sculley, BigQuery ML, CrowdFlower, Google Photos (el término fue "gorillas"), COMPAS (ProPublica, 2016), toeslagenaffaire, pgvector, Adult y el censo, FAIR, y la fecha en que pandas agregó `isna` (0.21).
5. **LatamGPT.** En el apunte puse que no confirmé la fecha. Fue el 10/02/2026, así que "salió este año" es correcto.
6. **Opus 4.7 y GPT 5.5.** En el apunte puse que no lo chequeé. Los dos existían cuando se nombraron en clase (16/04 y 23/04 de 2026).
7. **Pokémon Go.** Mantengo "dudoso" en la parte del cliente de delivery, pero lo precisé: el modelo geoespacial existe, se entrena con escaneos voluntarios y "logistics" aparece solo como aplicación futura.
8. **Matiz que agrego al apunte sobre MNAR (módulo 4).** Allí recomendé "como mínimo" una columna indicadora. Vale para **predecir**; para **estimar**, van Buuren discute el método del indicador como ad hoc y la vía correcta es el análisis de sensibilidad.

## Críticas y límites

- **Los benchmarks son chicos.** Tres datasets (Melbourne real, Melbourne con faltantes inyectados, Adult), validación cruzada de 5 folds con una sola semilla y sin ajustar hiperparámetros. Las diferencias menores a un desvío (0,002 en HGB, 0,003 en el AUC de Adult) son ruido. Un ajuste fino de cada configuración podría reordenar las de la mitad de la tabla, no los extremos.
- **El escenario MNAR es inventado por mí.** Elegí una logística sobre el log del área para que falten las casas grandes. Es un caso plausible (un tasador que no mide las casas grandes), pero no sé si así faltan los datos reales de Melbourne. Lo uso para mostrar el mecanismo, no como estimación.
- **Medí predicción, no inferencia.** Ninguno de los benchmarks dice nada sobre si un coeficiente o una media quedan sesgados; para eso hacen falta otras métricas (cobertura de intervalos, sesgo contra la verdad) y es justo donde la imputación múltiple tiene ventaja.
- **Los tiempos son aproximados.** Corrieron en una CPU compartida del box y algunos en paralelo con otros trabajos. HGB y XGBoost usan varios hilos. Tomá las proporciones (KNN 6 veces más lento que la mediana con árboles; Polars 18 veces más rápido que pandas a 50×), no los segundos exactos.
- **La comparación de motores tiene sesgos de diseño.** DuckDB carga con la conversión a pandas del resultado; Polars, en cambio, arranca con los datos ya convertidos. Una comparación justa haría todo dentro de cada motor, desde el CSV hasta el archivo final.
- **Usé pandas 2.3.3 en los benchmarks** (ydata-profiling no acepta pandas 3) y pandas 3.0.6 en la guía. Para lo que medí no debería cambiar nada, pero no lo comprobé con las dos versiones.
- **El archivo de 18.396 filas lo identifiqué por coincidencia de cifras**, con una copia en GitHub de un tercero. Que reproduzca todas las cifras de José es evidencia fuerte, pero no vi la versión de Kaggle.
- **Lo que no pude verificar:** la fecha del entregable 2 (no es pública), el cargo actual de Ariel en una fuente primaria (LinkedIn pide sesión), la frase sobre Claude y GPT y abstenerse, y la existencia de "juicios por varios millones" por COMPAS (no encontré ninguno).
- **Conflictos de interés:** Databricks (autora del glosario de medallion y de la definición de lakehouse, vende la plataforma), Great Expectations, Soda y dbt Labs (venden versiones comerciales de lo que documentan), el Kimball Group (vende libros y cursos), CrowdFlower (vendía limpieza de datos y es autora del 60%), CENIA y AWS (promueven LatamGPT), Niantic (escribe sobre su propio modelo), OpenAI y Anthropic (anuncian sus modelos), y Varoquaux, coautor de los dos papers de la alternativa y creador de scikit-learn.
- **Páginas que leí con curl:** guías de imputación, ensembles, `IterativeImputer`, `KNNImputer`, `HistGradientBoostingRegressor` y los ejemplos de imputación y de HGBT de scikit-learn 1.9.1; guía de faltantes y referencia de `isnull` de pandas 3.0.6; notas de pandas 0.21; constantes de numpy; Wikipedia sobre NaN, LSH y Loomis contra Wisconsin; tutorial de punto flotante de Python; FIMD (índice, 2.3.2 y 3.8); Rubin 1978 (PDF); Rahm y Do (PDF de Leipzig); CrowdFlower 2016 (PDF); Wickham 2014 (página de JSS); Sculley 2015 (resumen); Hinton 2015 (resumen); Josse 2019 y Perez-Lebel 2022 (resúmenes en arXiv); páginas de pandera, GX Core, Soda, ydata-profiling (y su repositorio renombrado), dbt (tests y contratos), DuckDB ("Why DuckDB"), Polars, preguntas frecuentes de XGBoost; Kimball (técnicas y nulls en dimensiones); Databricks (medallion y lakehouse); TOP500; CENIA; Niantic; ProPublica; BBC; The Verge; BigQuery ML; OpenAI; Anthropic; UCI Adult; FAIR en Nature; el `pip-freeze.txt` de Colab en GitHub; pgvector; calendario y equipo docente de la Diplomatura.
- **Abiertas con el lector web:** la página de Pearson de Johnson y Wichern (con curl daba 403).
- **Vistas solo en el buscador:** la página de Kaggle de Melbourne, Rubin 1976 en *Biometrika*, los perfiles de Ariel en neuron.com y signalhire, el informe de la autoridad de datos neerlandesa, la nota de AP sobre LatamGPT y las páginas de O'Reilly de Reis y Housley y de Strengholt.
- **No cargaron:** las páginas de O'Reilly (403) y el PDF de Rahm y Do en el sitio de la IEEE (404; usé la copia de la Universidad de Leipzig).

## Análisis adversario

> Cómo leer esto: acá discuto el enfoque de la materia contra la alternativa más fuerte que encontré, con la mejor versión posible de esa alternativa. No es una crítica a los docentes: una materia de cuatro encuentros tiene que elegir, y esto sirve para que sepas qué elegirías vos en un trabajo real.

**La tesis.** La materia enseña a explorar y curar a mano con pandas en notebooks: mirar `info()`, `describe()`, histogramas y missingno; decidir caso por caso si tirar filas, imputar con media, mediana, KNN o `IterativeImputer`, juzgando por cómo quedan las distribuciones; y llevar el resultado a una base con scripts de ETL. La imputación es una etapa previa al modelo, separada de él.

### La alternativa más fuerte: no imputar para predecir (NaN nativo más indicadores de faltante)

Evalué tres candidatas. **Los pipelines declarativos con contratos** (dbt, Great Expectations, pandera, SQL primero) son muy buenos, pero no compiten con la materia sino que la completan: alguien tiene que explorar para saber qué escribir en el contrato, y en la sección 8 lo uso como complemento. **El perfilado automático** es la más débil: en Melbourne no marcó ninguno de los valores imposibles que encontró la materia a mano, y el paquete más usado acaba de cambiar de nombre y de dueño. La más fuerte es **no imputar**: si el objetivo es predecir, dejar los NaN y usar un modelo que los maneja (HistGradientBoosting, XGBoost, LightGBM), o, si el modelo necesita una matriz completa, imputar lo más simple posible y sumar un indicador de faltante. Ataca justo el centro de la tesis, que la imputación es una decisión artesanal previa al modelo, y es la única de las tres que pude poner a prueba con números.

### La alternativa en su mejor versión

**Quién la defiende.** Josse, Chen, Prost, Scornet y Varoquaux (2019), con la teoría; Perez-Lebel, Varoquaux, Le Morvan, Josse y Poline (2022), con un benchmark en ocho bases de salud; la documentación de scikit-learn ("built-in support for missing values, which avoids the need for an imputer"; "simple imputers can be preferable in a prediction context") y la de XGBoost ("supports missing values by default"). Conflicto de interés: Varoquaux es uno de los creadores de scikit-learn, que implementa este enfoque.

**Qué evidencia la respalda.**

- Josse y otros demuestran que imputar con una constante, como la media, antes de aprender "is consistent when missing values are not informative", algo que contrasta con la inferencia, donde la media distorsiona la distribución. Y recomiendan para árboles el método "missing incorporated in attribute", que es lo que hacen HGB y XGBoost, porque "can handle both non-informative and informative missing values".
- Perez-Lebel y otros concluyen que "Native support for missing values in supervised machine learning predicts better than state-of-the-art imputation with much less computational cost" y que, si se imputa, "it is important to add indicator columns".
- Mi sección 4: en Melbourne, HGB nativo (0,1779) empata con la media y la mediana y le gana a KNN (0,1814) e Iterative (0,1809), que además tardan entre 1,4 y 6,6 veces más. XGBoost nativo es el mejor de la tabla (0,1726) en 2,9 s.
- Mi sección 5: cuando la falta es informativa, la media más indicador en un modelo lineal recupera todo lo perdido (0,2620 contra 0,2621 sin faltantes), y la imputación iterativa sin indicador queda peor (0,2685).
- Mi sección 6: en Adult, el NaN nativo y la categoría "Falta" le ganan a la moda.
- Operativamente, es la misma transformación en entrenamiento y en producción: no hay un imputador que ajustar, guardar y versionar, ni riesgo de fuga si alguien imputa antes de partir los datos.

**Qué evidencia la contradice.**

- **No sirve para inferir.** van Buuren titula una sección "Imputation is not prediction" (2.6) y advierte que el método del indicador es ad hoc para estimar. Si la pregunta es "¿cuánto sube el precio por metro cuadrado?", un HGB con NaN no te da un coeficiente con su intervalo, y la imputación múltiple con reglas de Rubin sí.
- **Con modelos lineales, imputar bien sí paga.** En Melbourne, KNN mejoró a Ridge de 0,286 a 0,275, más que cualquier indicador.
- **Aprender de la falta es frágil.** Si el modelo aprendió "falta el área, entonces es una casa grande" y mañana el formulario hace obligatorio el campo, la señal desaparece y el modelo se degrada sin aviso. Es uno de los riesgos que Sculley y otros llaman "changes in the external world". La imputación explícita, documentada, hace visible ese supuesto.
- **Esconde los datos.** Sin la etapa de exploración e imputación, nadie mira los 34 baños en 0 ni el área de 44.515 m², que no son faltantes sino errores, y el árbol los usa como valores válidos.
- **La evidencia empírica es acotada.** Perez-Lebel y otros miran bases de salud grandes; mi benchmark mira tres casos chicos. En Melbourne real, la ventaja de no imputar sobre la mediana es de 0,0004, dentro del ruido.

### Comparación directa

| Criterio | A: la materia (EDA y curación a mano, imputación elegida a criterio) | B: no imputar (NaN nativo más indicadores) | C: pipelines declarativos con contratos (dbt, GX, pandera, SQL) |
|---|---|---|---|
| Costo | Bajo en herramientas, alto en horas de analista por dataset | Bajo: un parámetro o ninguno | Medio: escribir y mantener contratos y tests; plataforma si es comercial |
| — | Baja para empezar; crece con cada decisión manual que hay que documentar | Baja | Media a alta (orquestación, CI, varias herramientas) |
| Tiempo hasta valor | Horas a días por dataset | Minutos: en Melbourne, 2,9 a 4,7 s por validación cruzada completa | Días para montar; después, cada carga se valida sola en segundos |
| Riesgo | Decisiones no reproducibles, fuga si se imputa antes de partir, imputaciones que "se ven bien" pero empeoran el modelo (KNN con árboles) | Modelos que dependen del patrón de faltantes; errores que no son NaN pasan de largo; no da inferencia | Falsa seguridad si el contrato está mal escrito; costo de mantenimiento |
| Madurez | Total (pandas, scikit-learn), pero `IterativeImputer` sigue experimental | Alta: HGB estable en scikit-learn, XGBoost con soporte por defecto | Alta en dbt y GX; pandera estable; ydata-profiling recién renombrado |
| Evidencia | La literatura de imputación múltiple (Rubin, van Buuren) para inferir | Josse 2019, Perez-Lebel 2022 y mis secciones 4 a 6 para predecir | Más práctica de la industria que estudios controlados; mi contrato encontró 22 fallas en 0,26 s |
| Contexto donde rinde | Informes, inferencia, modelos lineales, aprender qué hay en los datos | Predicción tabular con árboles, producción, muchos faltantes | Datos que llegan una y otra vez, equipos, producción |

### Dónde gana la alternativa

- Predicción tabular con árboles: igual o mejor error, con menos tiempo y menos código.
- Faltantes informativos (MNAR): el indicador o el NaN nativo convierten la falta en señal en vez de taparla.
- Producción: no hay imputador que mantener y la transformación es la misma en entrenamiento y en producción.
- Muchas columnas con faltantes: imputar con KNN o iterativo escala mal (costo O(knp³ min(n, p)) según scikit-learn) y no mejora a los árboles.

### Dónde pierde

- Inferencia y estimación: no reemplaza a la imputación múltiple.
- Modelos que necesitan matriz completa (lineales, KNN, PCA, redes): ahí hay que imputar sí o sí, y una buena imputación ayuda.
- Errores que no son NaN: centinelas, unidades mal cargadas, outliers imposibles. Eso solo lo atrapan la exploración de la materia o un contrato.
- Cambios en el mecanismo de falta: un modelo que aprendió de la falta se rompe cuando la falta cambia.
- Comunicación: un informe con distribuciones imputadas y un criterio explícito se explica mejor que "el árbol decide".

### Cómo decidir

**Elegí A (la materia: explorar e imputar a criterio) si…**

- La pregunta es de estimación o inferencia (un coeficiente, una media, una tasa con su intervalo); en ese caso, con imputación múltiple de verdad y reglas de Rubin.
- El modelo necesita una matriz completa y la imputación mejora el resultado (en Melbourne, KNN mejoró a Ridge).
- Es un análisis puntual o un entregable donde lo que se evalúa es el criterio y la exploración.
- Todavía no sabés qué hay en los datos: la exploración manual es la que encuentra centinelas y errores.

**Elegí B (no imputar: NaN nativo más indicadores) si…**

- El objetivo es predecir con datos tabulares y podés usar HistGradientBoosting, XGBoost o LightGBM.
- Sospechás que la falta es informativa (formularios opcionales, mediciones que solo se hacen a algunos).
- El modelo va a producción y querés la menor cantidad de piezas que mantener.
- Tenés poco tiempo: en Melbourne, el modelo nativo dio el mejor resultado en menos de 5 s.

**Y C (contratos declarativos) si** los datos se recargan periódicamente o los usa más de una persona: no reemplaza a A ni a B, los protege.

**Un híbrido posible (sugerencia).** (1) Explorá a mano como enseña la materia, pero una sola vez y con preguntas concretas: qué columnas tienen faltantes, cuáles son centinelas disfrazados, qué valores son imposibles. (2) Escribí lo que encontraste como contrato (pandera en la notebook, tests de dbt si trabajás en SQL) y validá cada carga en la capa plata. (3) Convertí los centinelas a NaN en plata y no imputes ahí: dejá los faltantes como faltantes y, en categóricas, usá una categoría "Falta" (o "Unknown", como Kimball). (4) Para predecir, empezá con HGB o XGBoost con NaN nativo; si necesitás un modelo lineal, usá un `Pipeline` con imputación simple más `add_indicator=True`, y probá KNN o iterativa solo si mejora la validación cruzada. (5) Para estimar, hacé imputación múltiple con m entre 20 y 50 y reglas de Rubin, y un análisis de sensibilidad si sospechás MNAR. (6) Monitoreá en producción la proporción de faltantes por columna; si cambia, reentrená. Los scripts `bench_imputacion.py`, `bench_mnar.py`, `bench_adult.py` y `contrato_pandera.py` hacen cada paso.

**Veredicto.** Para predecir, la alternativa gana: no imputar (o imputar simple con indicador) es el punto de partida correcto, y las imputaciones sofisticadas de la materia tienen que ganarse su lugar en la validación cruzada, cosa que en Melbourne no pasó con árboles. Para inferir, la materia tiene razón en tomarse la imputación en serio, pero tiene que ser imputación múltiple de verdad, no "imputar en subconjuntos". Y en los dos casos, la exploración manual sigue siendo indispensable para encontrar los errores que no son NaN; lo que conviene cambiar es dejarla escrita como contrato y no solo como celdas de una notebook.

## Material para seguir

**Faltantes e imputación**

- [van Buuren, *Flexible Imputation of Missing Data*, 2.ª ed. (libre)](https://stefvanbuuren.name/fimd/): el libro de referencia, con código en R.
- [FIMD 2.3: reglas de Rubin y cuántas imputaciones](https://stefvanbuuren.name/fimd/sec-whyandwhen.html): las fórmulas y el consejo de m = 50.
- [Rubin (1978), "Multiple imputations in sample surveys"](http://www.asasrms.org/Proceedings/papers/1978_004.pdf): el paper original, corto.
- [Guía de imputación de scikit-learn](https://scikit-learn.org/stable/modules/impute.html): univariada, iterativa, KNN e indicadores.
- [Ejemplo "Imputing missing values before building an estimator"](https://scikit-learn.org/stable/auto_examples/impute/plot_missing_values.html): comparación de imputadores con indicador.
- [`IterativeImputer` en scikit-learn 1.9.1](https://scikit-learn.org/stable/modules/generated/sklearn.impute.IterativeImputer.html): la advertencia de experimental y `sample_posterior`.
- [`KNNImputer`](https://scikit-learn.org/stable/modules/generated/sklearn.impute.KNNImputer.html): `nan_euclidean` y pesos.
- [Josse y otros (2019), "On the consistency of supervised learning with missing values"](https://arxiv.org/abs/1902.06931): por qué imputar con la media alcanza para predecir.
- [Perez-Lebel y otros (2022), benchmark de estrategias en bases de salud](https://arxiv.org/abs/2202.10580): NaN nativo contra imputación, con tiempos.

**Modelos con NaN nativo**

- [scikit-learn, soporte de faltantes en HistGradientBoosting](https://scikit-learn.org/stable/modules/ensemble.html): cómo decide el lado de cada corte.
- [Ejemplo de HGBT en scikit-learn](https://scikit-learn.org/stable/auto_examples/ensemble/plot_hgbt_regression.html): faltantes, categóricas y restricciones.
- [Preguntas frecuentes de XGBoost](https://xgboost.readthedocs.io/en/stable/faq.html): faltantes por defecto y el caso de las matrices dispersas.

**pandas, NaN y punto flotante**

- [Guía de datos faltantes de pandas](https://pandas.pydata.org/docs/user_guide/missing_data.html): NaN, NA, NaT y la lógica de Kleene.
- [`DataFrame.isnull` en pandas 3.0.6](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.isnull.html): "an alias for DataFrame.isna".
- [Notas de pandas 0.21](https://pandas.pydata.org/pandas-docs/stable/whatsnew/v0.21.0.html): cuándo y por qué se agregó `isna`.
- [Wikipedia, NaN](https://en.wikipedia.org/wiki/NaN): la tabla de comparaciones de IEEE 754.
- [Constantes de numpy](https://numpy.org/doc/stable/reference/constants.html): numpy usa IEEE 754.

**Calidad de datos y contratos**

- [pandera](https://pandera.readthedocs.io/en/stable/): esquemas y chequeos para DataFrames, libre.
- [GX Core, visión general](https://docs.greatexpectations.io/docs/core/introduction/gx_overview): Expectations, Checkpoints y Data Docs (empresa con versión comercial).
- [Soda](https://docs.soda.io/): contratos y monitoreo (plataforma comercial).
- [dbt, data tests](https://docs.getdbt.com/docs/build/data-tests): `not_null`, `unique`, relaciones.
- [dbt, model contracts](https://docs.getdbt.com/docs/mesh/govern/model-contracts): garantías de columnas y tipos.
- [fg-data-profiling (antes ydata-profiling)](https://github.com/ydataai/ydata-profiling): perfilado automático, con el aviso del cambio de nombre.

**Motores y arquitectura**

- [Why DuckDB](https://duckdb.org/why_duckdb): base analítica embebida y libre.
- [Guía de Polars](https://docs.pola.rs/): DataFrames en Rust, modo lazy.
- [Databricks, arquitectura medallion](https://www.databricks.com/glossary/medallion-architecture): bronce, plata y oro (vende la plataforma).
- [Databricks, qué es un lakehouse](https://www.databricks.com/glossary/data-lakehouse): la definición (ídem).
- [Kimball Group, técnicas de modelado dimensional](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/): grano, hechos, dimensiones.
- [Kimball, null en dimensiones](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/null-dimension-attribute/): "Unknown" en vez de null.
- Reis y Housley, *Fundamentals of Data Engineering* (O'Reilly, 2022): no pude abrir la página; vista en el buscador.
- Strengholt, *Data Management at Scale*, 2.ª ed. (O'Reilly, 2023): ídem.

**Papers clásicos**

- [Rahm y Do (2000), "Data Cleaning: Problems and Current Approaches"](https://dbs.uni-leipzig.de/files/research/publications/2000-1/pdf/TBDE2000.pdf): la taxonomía de problemas.
- [Wickham (2014), "Tidy Data"](https://www.jstatsoft.org/article/view/v059i10): las tres reglas.
- [Sculley y otros (2015), "Hidden Technical Debt in Machine Learning Systems"](https://papers.nips.cc/paper/2015/hash/86df7dcfd896fcaf2674f757a2463eba-Abstract.html): la deuda técnica de datos.
- [Wilkinson y otros (2016), principios FAIR](https://www.nature.com/articles/sdata201618): Findable, Accessible, Interoperable, Reusable.

**Ética y casos de la clase 3**

- [ProPublica (2016), "Machine Bias"](https://www.propublica.org/article/machine-bias-risk-assessments-in-criminal-sentencing): COMPAS.
- [Loomis contra Wisconsin](https://en.wikipedia.org/wiki/Loomis_v._Wisconsin): el caso judicial.
- [BBC (2021), renuncia del gobierno neerlandés](https://www.bbc.com/news/world-europe-55674146): toeslagenaffaire.
- [The Verge (2015), Google Photos](https://www.theverge.com/2015/7/1/8880363/google-apologizes-photos-app-tags-two-black-people-gorillas): el caso de las etiquetas.
- [CrowdFlower (2016), Data Science Report](https://www2.cs.uh.edu/~ceick/UDM/CFDS16.pdf): el origen del 60% (encuesta de una empresa).
