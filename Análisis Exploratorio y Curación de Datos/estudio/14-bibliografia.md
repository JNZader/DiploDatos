# 14 — Bibliografía y profundización

La bibliografía no es decoración. Cada recurso responde un tipo de pregunta distinta. Saber cuál abrir para qué duda te ahorra horas de lectura inútil. Esta versión es la ampliación pedagógica de `BIBLIOGRAFIA.md` (raíz de la materia): no la reemplaza, la usa como base y le suma "cuándo abrir, qué buscar".

---

## VanderPlas — Python Data Science Handbook (2016, O'Reilly)

**Acceso**: gratuito en https://jakevdp.github.io/PythonDataScienceHandbook/
**Ediciones**: 1ª edición libre online; 2ª edición (2023) sólo en O'Reilly Learning.

### Qué aporta

- Base sólida de Numpy y Pandas con ejemplos minimalistas.
- Capítulo dedicado a *missing data* en Pandas (la convención `NaN`, propagación, métodos `isnull`/`fillna`/`dropna`).
- Tratamiento claro de `groupby`, `merge`, `join` y reshape (`pivot`, `melt`, `stack`).
- Capítulo de PCA con la intuición geométrica y la fórmula de varianza explicada.

### Cuándo ir ahí

- Cuando arrancás con la materia y necesitás "el manual" de pandas.
- Cuando dudás del comportamiento de un método (`groupby` con múltiples columnas, `merge` con `left_on`/`right_on`).
- Cuando querés entender PCA por dentro y no sólo llamar a `sklearn`.

### Secciones más relevantes para la materia

- **Capítulo 3 — Pandas**:
  - "Handling Missing Data" → complemento directo del archivo `01-datos-faltantes.md`.
  - "Combining Datasets: Concat and Append" + "Combining Datasets: Merge and Join" → base para `06-combinacion-datasets.md`.
  - "Aggregation and Grouping" → base de los `GROUP BY` que después se traducen a SQL en `08-sql-y-sqlalchemy.md`.
  - "Pivot Tables" → técnica que la cátedra no usa pero ayuda a pensar agregaciones.
- **Capítulo 4 — Matplotlib**: fundamentos de gráficos. Útil si tu `seaborn` "no se ve bien" y querés bajar al nivel de figura/eje.
- **Capítulo 5 — Machine Learning**:
  - "In Depth: Principal Component Analysis" → complemento de `05-pca.md`. Tiene el desarrollo geométrico que la clase no profundiza.

---

## Géron — Hands-On ML with Scikit-Learn, Keras & TF (2ª ed., 2019)

### Qué aporta

- Pipeline completo de ML aplicado, con código real y dataset transversal (California housing).
- El **Capítulo 2** es prácticamente un TP guiado: descarga, EDA, manejo de faltantes, encoding, transformers, pipelines, train/test split, evaluación.
- Mejor referencia para entender los `Pipeline` y `ColumnTransformer` de sklearn que aparecen tarde en la materia.

### Cuándo ir ahí

- Cuando querés ver un pipeline end-to-end antes de armar el tuyo en el TP1.
- Cuando dudás cómo encadenar `SimpleImputer` + `OneHotEncoder` + `StandardScaler` en un solo objeto reutilizable.
- Cuando llegás al tramo de transformers personalizados (no es obligatorio en la materia, pero te salva en producción).

### Secciones más relevantes

- **Capítulo 2 completo** — *End-to-End Machine Learning Project*:
  - "Get the Data" → patrón de carga reproducible (paralelo al `pd.read_csv(URL)` de clase 1).
  - "Discover and Visualize the Data" → EDA orientado a modelo. Complemento de `04-eda-practico.md`.
  - "Prepare the Data for ML Algorithms" → faltantes, encoding y feature scaling en orden. Complemento de los archivos `01`, `02` y `03`.
  - "Transformation Pipelines" → `Pipeline` y `ColumnTransformer`. No es contenido obligatorio de la materia, pero es el cierre natural del TP1.

---

## Molinaro & de Graaf — SQL Cookbook (2ª ed., O'Reilly)

### Qué aporta

- Recetario por problema, no por sintaxis: "cómo encontrar duplicados", "cómo paginar resultados", "cómo agrupar por intervalos de fechas".
- Cubre múltiples motores (Oracle, PostgreSQL, MySQL, SQL Server, DB2) con las diferencias marcadas: útil cuando saltás de SQLite a otro motor.
- Sección extensa de JOINs y self-joins con casos contraintuitivos.

### Cuándo ir ahí

- Cuando una consulta del TP2 te tira un resultado raro y no sabés si es bug de SQL o de tus datos.
- Cuando tenés que escribir una consulta no trivial (filtros condicionales, agregados con ventanas) y no querés reinventar la rueda.
- Cuando vas a usar PostgreSQL en lugar de SQLite y querés ver las diferencias sintácticas.

### Secciones más relevantes para la materia

- "Retrieving Records" → complementa `SELECT` / `WHERE` / `LIMIT`.
- "Working with Multiple Tables" → todos los tipos de JOIN, incluido `LEFT JOIN` con `IS NULL` para encontrar registros sin pareja.
- "Inserting, Updating, Deleting" → no se cubre en la cursada pero aparece en `to_sql(..., if_exists='append')`.
- "Working with Numbers" + "Working with Strings" → casts, conversiones, manipulación.

> **Nota**: la materia **no** cubre window functions, CTEs (`WITH`) ni subqueries anidados. El cookbook los trata: si te interesa profundizar, son los capítulos siguientes a "Reporting and Reshaping". Útil para entrevistas, no para el TP.

---

## Kaggle — Feature Engineering (notebook práctico)

**URL**: https://www.kaggle.com/code/ponybiam/feature-engineering-1-simple-features/notebook

### Qué aporta

- Ejemplos prácticos cortos de feature engineering aplicados a competencias.
- Patrones reutilizables: extracción de features desde fechas, binning, interacciones simples.
- Bueno para ver el "estilo Kaggle" de iterar features rápido y medir impacto.

### Cuándo ir ahí

- Cuando llegás al tramo de "qué hago con `Date`" en el TP1 y no sabés si descartar, codificar como ordinal o separar en año/mes/día.
- Cuando querés ver más allá del encoding básico: features derivadas (diferencias entre columnas, ratios, agregados por grupo).
- Cuando preparás casos para entrevistas técnicas.

### Limitación

Es una notebook, no un libro: la profundidad teórica es nula. Sirve como inventario de patrones, no como fundamento.

---

## SQLite Tutorial

**URL**: https://www.sqlitetutorial.net/
**Sandbox interactivo**: https://www.sqlitetutorial.net/tryit/
**Base de ejemplo**: Chinook (tracks, albums, artists, customers, invoices, employees, playlists).

### Qué aporta

- Referencia rápida de SQLite con ejemplos ejecutables sin instalar nada.
- Cubre el subset exacto que usa la cátedra: SELECT, WHERE, GROUP BY, HAVING, JOINs.
- El sandbox `tryit` permite ejecutar consultas contra Chinook online: ideal para practicar sin abrir SQLite local.

### Cuándo ir ahí

- Cuando querés correr un query y ver el resultado sin armar el entorno.
- Cuando tenés dudas de sintaxis específica de SQLite (que difiere de PostgreSQL en algunas cosas, como el tratamiento de fechas o el `||` para concatenar).
- Cuando preparás los queries del TP2 antes de armar el SQLAlchemy.

### Limitación

Es tutorial-style: no explica las decisiones de diseño detrás del modelo relacional. Para eso conviene un libro de fundamentos (Date, "An Introduction to Database Systems") que está fuera del alcance de la materia.

---

## Recursos extras para profundizar

Estos son links **reales y verificables** a documentación oficial. No reemplazan los libros: son la referencia última cuando hay duda sobre el comportamiento exacto de una función o método.

### Manipulación de datos

- **pandas** — documentación oficial: https://pandas.pydata.org/docs/
  - User Guide → Missing data: https://pandas.pydata.org/docs/user_guide/missing_data.html
  - User Guide → Merge, join, concatenate: https://pandas.pydata.org/docs/user_guide/merging.html
  - Ir acá cuando la cátedra mostró un método y necesitás ver todos sus argumentos.

- **NumPy** — documentación oficial: https://numpy.org/doc/stable/
  - Referencia obligada para entender cómo `NaN` se propaga en aritmética vectorizada.

### Limpieza y faltantes

- **missingno** — repositorio oficial: https://github.com/ResidentMario/missingno
  - El README tiene los cuatro tipos de gráfico (`bar`, `matrix`, `heatmap`, `dendrogram`) con ejemplos visuales. Más completo que la presentación en clase.

- **ydata-profiling** — documentación oficial: https://docs.profiling.ydata.ai/
  - Antes era `pandas-profiling`. Misma librería, marca nueva.
  - Tiene una sección sobre interpretación de correlaciones espurias que vale la pena leer.

### Machine learning y preprocesamiento

- **scikit-learn** — documentación oficial: https://scikit-learn.org/stable/
  - User Guide → Preprocessing data: https://scikit-learn.org/stable/modules/preprocessing.html (cubre todos los scalers + power + quantile).
  - User Guide → Imputation: https://scikit-learn.org/stable/modules/impute.html (`SimpleImputer`, `KNNImputer`, `IterativeImputer`).
  - User Guide → Decomposing signals in components: https://scikit-learn.org/stable/modules/decomposition.html (PCA y variantes).

### Bases de datos y orquestación

- **SQLAlchemy** — documentación oficial: https://docs.sqlalchemy.org/
  - Empezar por "Engine Configuration" y "Working with Engines and Connections".
  - El tutorial Core 2.0 es directo y aplicable a lo que se usa en la materia.

- **SQLite** — documentación oficial: https://www.sqlite.org/docs.html
  - Sección "SQL syntax" para detalles del dialecto.

- **Apache Airflow** — documentación oficial: https://airflow.apache.org/docs/
  - "Concepts → DAGs" y "Concepts → Operators" son la lectura mínima si vas a hacer el bonus de TP2.

- **Apache Parquet** — sitio oficial: https://parquet.apache.org/docs/
  - Páginas "File Format" y "Overview" explican por qué columnar es más eficiente para lectura selectiva.

### Visualización

- **seaborn** — documentación oficial: https://seaborn.pydata.org/
  - Galería de ejemplos en `seaborn.pydata.org/examples/`: útil para copiar el patrón visual que necesitás.

- **matplotlib** — documentación oficial: https://matplotlib.org/stable/
  - Cuando seaborn no alcanza y hay que bajar al nivel `fig, ax = plt.subplots()`.

### Embeddings y LLMs (bonus TP2)

- **sentence-transformers** — documentación oficial: https://www.sbert.net/
  - "Quickstart" muestra el patrón mínimo: cargar modelo, `encode()`, similitud coseno con `util.cos_sim`.
  - Para el bonus del TP2 sobre `CouncilArea` alcanza con un modelo multilingüe chico como `paraphrase-multilingual-MiniLM-L12-v2`.

---

## Estrategia sugerida de uso por fase

### Fase 1 — Familiarización con la materia (clases 1 y 2)

- **Base**: notebooks de la cátedra + apuntes `00` a `03`.
- **Complemento**: VanderPlas cap. 3 (Pandas missing data + groupby + merge).
- **Objetivo**: dominar el "primer vistazo" del dataset y los conceptos de Rubin (MCAR/MAR/MNAR).

### Fase 2 — Encoding, transformaciones, PCA (clase 2)

- **Base**: apuntes `02-encodings.md` y `03-transformaciones-y-pca.md`.
- **Complemento**: Géron cap. 2 (transformers, pipelines) + scikit-learn User Guide (preprocessing y decomposition).
- **Objetivo**: entender por qué cada transformer existe y cuándo se usa cada uno.

### Fase 3 — EDA, combinación, ETL, SQL (clases 3 y 4)

- **Base**: apuntes `04-eda-practico.md`, `06-combinacion-datasets.md`, `07-etl-dags-airflow.md`, `08-sql-y-sqlalchemy.md`.
- **Complemento**: SQL Cookbook + SQLite Tutorial + Airflow docs.
- **Objetivo**: poder pasar de pandas a SQL y viceversa sin perder semántica.

### Fase 4 — Trabajos prácticos

- **TP1** (encoding + KNN + PCA + composición): apuntes `01` a `05`, Géron cap. 2, scikit-learn User Guide.
- **TP2** (SQL + pandas + merge AirBnB): apuntes `04`, `06`, `07`, `08`. SQL Cookbook para queries no triviales. sentence-transformers para el bonus.

### Fase 5 — Preparación de exámenes

- **Repaso rápido**: formulario (`12`) + preguntas guía (`13`).
- **Profundización conceptual**: VanderPlas + Géron para volver al porqué.
- **Tropiezos puntuales**: docs oficiales del módulo donde te trabaste.

---

## Idea final

La bibliografía complementaria no reemplaza la práctica. Su valor principal es ayudarte a:

1. Entender el **por qué** detrás de los métodos que usás.
2. Distinguir **técnica** (`fit_transform` correcto) de **interpretación** (qué significa que la PC1 explique el 70%).
3. Evitar análisis correctos en código pero flojos en criterio.

Si leés todo pero no hacés los TPs con las manos, no aprendés. Si hacés los TPs pero nunca leés, te quedás en la receta. La clave es alternar: **hacer → dudar → leer → replantear → volver a hacer**.

---

**Fin de los apuntes EyCD.**

**Recordá**: estos apuntes son una guía, no un reemplazo de tu propio razonamiento. El objetivo es que llegues al punto donde podás discutir los supuestos, cuestionar las conclusiones, y justificar cada decisión de curación con la misma claridad con la que escribís código.
