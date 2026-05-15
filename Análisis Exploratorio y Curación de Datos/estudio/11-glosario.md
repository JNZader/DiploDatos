# 11 — Glosario

Este glosario no es un diccionario seco. Cada término viene con una explicación de por qué importa, en qué clase aparece y qué error suele acompañarlo. Si un término no está acá es porque la cátedra no lo trabajó: no inflé el listado.

---

## Curación, EDA y calidad de datos

**Curación de datos**
Proceso de seleccionar y transformar datos para volverlos aptos para experimentación. Incluye limpieza de ruido, faltantes y errores. No es "ordenar el dataset": es decidir, con criterio, qué entra al modelo y qué se descarta. En esta materia es el paraguas que cubre clases 1, 2 y 4.

**EDA** (Exploratory Data Analysis / Análisis Exploratorio de Datos)
Primera etapa de cualquier análisis: inspeccionar estructura, calidad y potencial analítico antes de modelar. No es "perder tiempo": las decisiones metodológicas más caras se toman acá. En la materia se trabaja con un protocolo de 7 etapas: vistazo, numéricas, faltantes, distribuciones, categóricas, correlaciones, lectura de la matriz.

**Ruido**
Error que ensucia o contamina la señal. La frase de cabecera de la clase 1 es *"cuando entra basura, sale basura"*: si no se trata el ruido en la curación, ningún modelo lo arregla después.

**Dato erróneo**
Dato recolectado con un error que lo aparta de la generalidad. Distinto del outlier: el outlier es real pero raro; el erróneo es directamente inválido (ej.: edad = -3).

**Dato atípico (outlier)**
Valor real con baja probabilidad de ocurrencia que ejerce mucho efecto palanca sobre estimadores no robustos (media, varianza, regresión lineal). La decisión de eliminar o conservar depende del objetivo del análisis, no de una regla automática.

**Dato mal codificado**
Aparece al combinar bases con codificaciones distintas de faltante (una usa `NaN`, otra `0`, otra `-1`). Reconocer la codificación es parte de la curación, no un detalle técnico.

**Calidad de datos**
Conjunto de dimensiones que la cátedra explicita: completitud, validez, precisión, integridad, consistencia, temporalidad y representatividad. Un dataset puede ser técnicamente "limpio" y a la vez no representativo.

---

## Datos faltantes, NaN y mecanismos de pérdida

**Dato faltante**
Dato no registrado. En pandas se materializa como `NaN`, pero puede venir enmascarado como `0`, `-1` o un string vacío. La curación arranca detectando estas máscaras (típico en clase 1: `Landsize == 0`, `Bathroom == 0`).

**Perdido vs inexistente**
Perdido: sabemos que el valor existe pero no lo conocemos. Inexistente: no puede ser recolectado (ej.: superficie del 3er dormitorio en una casa de 2 ambientes). Python no distingue ambos casos: hay que documentarlo a mano.

**NaN** (Not a Number)
Float especial definido por IEEE-754. Se propaga en aritmética (`NaN + 1 = NaN`) sin romper el cálculo vectorizado de Numpy/Pandas. Por eso pandas usa NaN y no `None` para representar faltantes en columnas numéricas.

**None**
Objeto Python de tipo `NoneType`. Rompe operaciones aritméticas vectorizadas. Si una columna tiene `None`, pandas suele rebajarla a dtype `object` y se pierde performance.

**Predecir vs imputar**
Predecir es estimar un valor que nunca se muestreó (fila nueva). Imputar es sustituir un valor no informado de una fila ya existente. La cátedra remarca: *"imputar es predecir esos datos"*; las herramientas son similares pero la intención es distinta.

**Imputación estocástica**
Usa otras variables más una componente de incertidumbre (no un valor fijo). MICE es el ejemplo paradigmático.

**MCAR** (Missing Completely At Random)
Los faltantes no dependen ni de las variables observadas ni del valor faltante mismo. Insesgado. Si el porcentaje es bajo se puede dropear sin culpa. Es el caso más cómodo y el más raro.

**MAR** (Missing At Random)
La probabilidad de faltar se explica completamente por OTRAS variables observadas. Se puede imputar con KNN, MICE, regresión, etc. Es el escenario donde la imputación tiene sentido.

**MNAR** (Missing Not At Random)
La probabilidad de faltar depende del propio valor no observado (ej.: gente con salario alto que decide no informarlo). Cualquier imputación introduce sesgo. La recomendación de la cátedra es directa: *"recolectar nuevos datos"*.

**Regla de Rubin**
En imputación múltiple, la varianza total combina la varianza dentro de cada imputación con la varianza entre imputaciones: `var_total = var_dentro + var_entre`. Es el fundamento de MICE.

**SimpleImputer**
Clase de sklearn para imputación a nivel columna con valor constante, media, mediana o moda. Rápida, pero no contempla correlaciones entre variables → introduce sesgo si la pérdida no es MCAR.

**KNNImputer**
Imputa cada faltante usando los k vecinos más cercanos en el espacio de features. Exige variables **numéricas y estandarizadas** (la distancia euclídea es sensible a la escala).

**IterativeImputer (MICE — Multiple Imputation by Chained Equations)**
Modela cada feature con faltantes como función de las demás, rotando hasta converger. Permite usar distintos estimadores: `BayesianRidge` (default), `DecisionTreeRegressor`, `ExtraTreesRegressor`, `KNeighborsRegressor`. No soporta tipos mixtos sin encoding previo.

**ffill / bfill / interpolación**
Estrategias específicas para series temporales: rellenar con el último valor observado, con el próximo o interpolar entre ambos. No tienen sentido en datasets transversales.

**missingno**
Librería de visualización de faltantes. Tres gráficos útiles: `bar` (cuántos faltantes por columna), `matrix` (patrón visual por fila/columna), `heatmap` (correlación de presencia/ausencia entre columnas).

---

## Sesgo y dilema sesgo-varianza

**Sesgo de un estimador**
`Bias(T) = E(T) − θ`. Diferencia sistemática entre la esperanza del estimador y el parámetro real. Si es 0, el estimador es insesgado. En ML se traduce como *"diferencia consistente entre las predicciones del modelo y los valores reales"*.

**Dilema sesgo-varianza**
Descomposición del error esperado: `E[(Y − Ŷ)²] = Bias² + Variance`. Modelos simples → alto sesgo, baja varianza. Modelos complejos → bajo sesgo, alta varianza. La diana de tiro con cuatro cuadrantes (low/high bias × low/high variance) es la imagen canónica.

**Sesgo de selección/recolección**
La muestra no se obtuvo de forma aleatoria. Engloba muchos sub-tipos (autoselección, exclusión, supervivencia, pre-selección, etc.).

**Autoselección**
Sesgo donde participa quien decide hacerlo. Encuestas voluntarias (Sysarmy, formularios online) lo sufren por construcción.

**Sesgo de exclusión**
Grupos que quedan fuera del marco de muestreo (por idioma, acceso a la plataforma, edad, etc.).

**Sesgo de supervivencia**
Sólo se observan los individuos que "pasaron el proceso". El ejemplo clásico es Abraham Wald y los aviones de la WWII: reforzar las zonas SIN impactos, porque los aviones impactados ahí no volvieron.

**Sesgo de información**
Errores en el registro o datos incompletos. No es un problema de muestreo, es un problema de medición.

**Sesgo de respuesta**
Respuestas inexactas por deseabilidad social, memoria deficiente o presión externa.

**Sesgo de medición**
Instrumentos con errores sistemáticos (una balanza descalibrada, un sensor con drift).

**Sesgo de publicación (file drawer)**
Sólo se publican los estudios con resultados significativos. Quien hace metaanálisis termina viendo una literatura inflada artificialmente.

**Sesgo de omisión**
Faltan variables relevantes en el dataset. El modelo "ve" un mundo incompleto.

**Sesgo de deriva (data drift)**
El sistema generador de datos cambia con el tiempo y el modelo entrenado en datos viejos pierde validez.

**Sesgo de contenido social**
Datos de internet (tweets, Wikipedia, comentarios) reflejan estereotipos sociales y los modelos los aprenden.

**Sesgo de retroalimentación**
Las predicciones del modelo influencian los datos que recolectará después (recomendadores, sistemas predictivos en justicia o crédito).

**Sesgo de procesamiento (curado)**
Sesgo introducido por nosotros: faltantes mal tratados, cohortes mal unidas, escalado mal aplicado, cherry picking de subconjuntos cómodos.

**Cherry picking**
Elegir el subconjunto de datos o análisis que respalda la conclusión que ya teníamos en mente. Una de las trampas más comunes y menos visibles del procesamiento.

---

## Variables y encodings

**Variable categórica**
Toma valores de un conjunto finito de categorías. Puede ser **ordinal** (con orden jerárquico: nivel educativo, talle de remera) o **nominal** (sin orden: provincia, color).

**Variable numérica**
Toma valores numéricos. Puede ser discreta (años de experiencia) o continua (precio, superficie).

**OrdinalEncoder**
Asigna un entero a cada categoría respetando un orden explícito. SÓLO para variables ordinales. Usado sobre nominales genera un orden artificial que el modelo va a interpretar como real.

**OneHotEncoder / get_dummies**
Genera una columna binaria por categoría. Para nominales. `drop_first=True` elimina una columna por categoría para evitar colinealidad perfecta (la última categoría queda codificada como "todas las demás en 0").

**drop_first**
Parámetro de `pd.get_dummies` (y `OneHotEncoder` vía `drop='first'`). Evita que K columnas binarias sean linealmente dependientes (la suma da 1). Si no se setea, se introduce redundancia que confunde a modelos lineales.

**DictVectorizer**
Combina codificación one-hot de categóricas con paso directo de numéricas, partiendo de una lista de diccionarios. Devuelve matriz **esparsa** por defecto.

**Codificación de frecuencia (frequency encoding)**
Reemplaza cada categoría por la frecuencia con que aparece. Útil cuando la cardinalidad es alta y OHE explota.

**Curse of dimensionality (maldición de la dimensionalidad)**
Al subir dimensiones con OHE, los vectores se vuelven esparsos y casi ortogonales entre sí. Las distancias dejan de discriminar (todo está "igual de lejos"), los productos punto se anulan y los algoritmos basados en distancia (KNN, K-means, SVM) degradan.

**Matriz esparsa (sparse matrix)**
Representación que almacena sólo los valores no nulos (`scipy.sparse`). En OHE de alta cardinalidad es la única forma viable de mantener todo en memoria. La memoria de la versión densa crece cuadráticamente con las dimensiones; la esparsa, linealmente con los no-nulos. **Antes de hacer `.todense()` hay que estimar los MB resultantes.**

---

## PCA y reducción de dimensionalidad

**PCA** (Principal Component Analysis)
Método algebraico que proyecta una matriz `X ∈ ℝ^(n×m)` en un subespacio `Z ∈ ℝ^(n×d)` con `d ≪ m`, conservando la mayor varianza posible. Los componentes principales son las direcciones ortogonales del espacio original ordenadas por varianza capturada.

**Componente principal**
Combinación lineal de las features originales. PC1 captura la mayor varianza, PC2 la siguiente bajo la restricción de ser ortogonal a PC1, y así. Geométricamente: ejes rotados del espacio original.

**Varianza explicada**
Proporción de la varianza total del dataset que captura cada componente. `pca.explained_variance_ratio_` la devuelve. Sumar de a uno hasta cubrir un umbral (típico 90-95%) es el criterio operativo para elegir `n_components`.

**Varianza explicada acumulada**
Suma acumulativa de `explained_variance_ratio_`. Es la curva que se grafica para decidir el corte (codo o umbral).

**Escalado obligatorio en PCA**
Sin escalar, la columna con mayor varianza absoluta domina todos los componentes. La cátedra es explícita: *"sklearn centra los datos restándoles la media; sin embargo, es recomendable también estandarizar o al menos escalar la matriz original para asegurar que todas las variables estén en las mismas unidades y ninguna tenga un peso demasiado grande"*. En el ejemplo Iris, MinMax vs Standard cambia PC1 de ≈17% a ≈2.2%.

---

## Transformaciones numéricas

**Escalado vs normalización**
**Escalar** cambia el RANGO de una variable numérica (su forma sigue igual). **Normalizar** cambia la FORMA de la distribución. Confundirlas es un error frecuente en la materia.

**MinMaxScaler**
Lleva los datos a un rango fijo (típicamente [0, 1] o [−1, 1]). No cambia la forma. Sensible a outliers (el máximo y el mínimo dominan).

**MaxAbsScaler**
Divide por el máximo absoluto. Especial para datos centrados en 0 o ralos (sparse): preserva la esparsidad porque no centra.

**RobustScaler**
Resta la mediana y divide por el IQR. Es la opción cuando hay muchos outliers, porque ni el centro ni la escala se construyen con valores extremos.

**StandardScaler** (z-score)
Resta la media y divide por el desvío estándar. Resultado: media 0, varianza 1. Asume distribución aproximadamente gaussiana; con outliers fuertes degrada y conviene `RobustScaler`.

**normalize (l1/l2/max)**
Normaliza cada **muestra** (fila) para que tenga norma 1. Sirve cuando se trabaja con productos punto, similitud coseno o kernels. Ojo: opera sobre filas, no columnas.

**QuantileTransformer**
Mapea cada valor a su cuantil y opcionalmente lo reproyecta a una distribución uniforme o normal mediante `G⁻¹(F(X))`. Suaviza outliers y produce distribuciones muy regulares, pero **distorsiona correlaciones y distancias**.

**PowerTransformer**
Aplica una transformación de potencia para acercar la distribución a una gaussiana. Dos métodos disponibles: **Box-Cox** (requiere `x > 0` estrictamente) y **Yeo-Johnson** (acepta valores negativos y ceros).

**Box-Cox**
Familia paramétrica de transformaciones potencia. Caso particular: `λ = 0` ⇒ logaritmo. Sólo para datos positivos.

**Yeo-Johnson**
Generalización de Box-Cox que admite valores negativos. Es el default razonable cuando no sabés si tu variable es siempre positiva.

**Log transform**
Caso particular de Box-Cox con `λ = 0`. Útil para variables con cola derecha larga (precios, ingresos, conteos).

---

## EDA práctico, outliers y herramientas

**Análisis univariado**
Mirar una variable a la vez. Numéricas: `describe()`, histograma, boxplot. Categóricas: `nunique()`, `value_counts()`, tabla resumen.

**Análisis bivariado/multivariado**
Cruzar dos o más variables. Cat × num: boxplot. Num × num: scatterplot. Multivariado: heatmap de correlaciones, ranking del target contra todo el resto.

**Asimetría (skewness)**
Discrepancia entre media y mediana. Si la media supera bastante a la mediana, la distribución tiene cola derecha (asimetría positiva). En esta materia no se calcula con un test formal: se compara visualmente con `describe()` y un histograma.

**IQR (Rango Intercuartílico)**
`Q3 − Q1`. Ancho del 50% central. Robusto a outliers porque ignora los extremos.

**Outliers por IQR**
Regla operativa: cualquier valor por debajo de `Q1 − 1.5 × IQR` o por encima de `Q3 + 1.5 × IQR` es candidato a outlier. En `melb_data.Price`: Q1≈650K, Q3≈1.33M, IQR≈680K, límite superior≈2.35M, 612 outliers detectados.

**ydata_profiling**
Librería que genera un reporte HTML automático con descripciones, correlaciones, faltantes y duplicados. Es **complemento, no reemplazo** del EDA manual: ayuda a barrer rápido pero no piensa por vos.

**Heatmap de correlaciones**
`df.corr().abs()` + `seaborn.heatmap`. Sirve para feature selection: las variables más correlacionadas con el target son candidatas naturales para el modelo, y pares con correlación muy alta entre features son señal de redundancia.

---

## Combinación de datasets

**join**
Combinación por **índice** (`df1.join(df2, how='outer')`). Útil cuando ambos DataFrames comparten ya el mismo índice.

**merge**
Combinación por **columnas** (`df1.merge(df2, on='key')`). El método de uso cotidiano.

**inner**
Conserva sólo las filas con clave presente en ambos DataFrames. Útil cuando se quiere garantizar matching completo.

**left**
Conserva todas las filas del izquierdo y agrega NaN donde el derecho no aporta. Es la elección por defecto en enriquecimiento (TP2 sobre Postcode con AirBnB).

**right**
Espejo del left. En la práctica se evita porque genera lecturas confusas (es más claro invertir los DataFrames y usar left).

**outer**
Conserva todas las filas de ambos lados, rellenando con NaN. Hace evidente qué claves quedaron sin pareja en cada lado.

**Validación post-merge**
Tras todo merge no trivial: chequear que la cantidad de filas no se infló (claves duplicadas), que los nulos esperados no aparecieron donde no deberían, y que los rangos siguen siendo plausibles. En la cátedra se materializa con `assert` después del merge.

**Clave de unión**
En sentido amplio: un identificador, una fecha, una coordenada GPS, una entidad nombrada o incluso un embedding. El concepto sale de la clase 4: no siempre es una columna alfanumérica trivial.

---

## ETL, ELT, orquestación

**ETL** (Extract, Transform, Load)
Patrón tradicional: extraer datos heterogéneos, transformarlos y cargarlos al destino final (típicamente un Data Warehouse).

**ELT** (Extract, Load, Transform)
Variante moderna: cargar primero el dato crudo y transformar después en el destino. La cátedra lo justifica: *"almacenar es barato y flexible. Guardar primero el dato crudo y transformar después según el caso."*

**Batch vs Real-time**
Procesamiento por lotes (Airflow, Spark) vs procesamiento de eventos en tiempo real (Kafka, Flink, Spark Streaming).

**Data Warehouse (DW)**
Almacén estructurado, modelado en tablas, optimizado para análisis. Ejemplo: BigQuery, Redshift, Snowflake.

**Data Lake**
Almacén de datos crudos en cualquier formato (S3, GCS). Barato y flexible, pero requiere disciplina para no convertirse en un "data swamp".

**Lakehouse**
Híbrido: estructura tipo DW sobre almacenamiento tipo Lake (Databricks, Iceberg, Delta).

**Arquitectura Bronze / Silver / Gold (Delta Lake)**
Tres capas progresivas: **Bronze** = crudo, ingesta rápida sin transformar. **Silver** = depurado e integrado. **Gold** = productos finales, métricas y KPIs listos para consumir.

**DAG** (Directed Acyclic Graph / Grafo dirigido acíclico)
Estructura que modela tareas como nodos con dependencias dirigidas y sin ciclos. Es el formato que usan los orquestadores de pipelines. *"Tareas como código. Controla dependencia y secuencia."*

**Airflow**
Orquestador open-source basado en DAGs. **No procesa datos, sólo coordina**: dispara tareas, controla orden, reintenta fallos, gestiona schedules. Operadores clave: `PythonOperator`, `BashOperator`. El operador `>>` define dependencias.

**DAGs de datos vs agénticos**
**De datos**: determinísticos, dependencias fijas, reintento automático. **Agénticos**: dinámicos, con human-in-the-loop, donde los pasos pueden cambiar según el contexto.

**Parquet**
Formato columnar binario optimizado para lectura selectiva. Más chico que CSV y permite leer sólo las columnas que necesitás. Se usa como destino estándar en Data Lakes modernos.

**python-decouple + .env**
Patrón para mantener credenciales fuera del código (lo lee desde un archivo `.env` no versionado). Buena práctica obligatoria en ETLs.

**logging**
Reemplazo profesional de `print` en pipelines de producción. Niveles (`DEBUG`, `INFO`, `WARNING`, `ERROR`) y handlers (archivo, stdout, syslog) que permiten depurar sin tocar código.

---

## SQL y SQLAlchemy

**SQLite**
Motor SQL embebido, sin servidor, almacenado en un único archivo. La cátedra lo describe como *"la DB más desplegada"* (celulares, navegadores, autos). Es el motor elegido para aprender SQL en la materia.

**Chinook**
Base de ejemplo (música) que distribuye SQLite Tutorial: tracks, albums, artists, customers, invoices, employees, playlists. Se usa para practicar JOINs.

**SELECT**
Cláusula que define qué columnas devolver. `SELECT *` trae todas; `SELECT DISTINCT` elimina duplicados.

**FROM**
Define la tabla (o tablas) de origen. Puede combinarse con JOIN.

**WHERE**
Filtro a nivel **fila**. Operadores: `=`, `<>`, `<`, `>`, `IN`, `BETWEEN`, `LIKE`. No puede usar funciones de agregación.

**GROUP BY**
Agrupa filas por los valores de una o más columnas, para aplicar agregaciones (`SUM`, `COUNT`, `AVG`, `MIN`, `MAX`). Toda columna en el `SELECT` que no esté agregada debe estar en el `GROUP BY`.

**HAVING**
Filtro a nivel **grupo**, después de `GROUP BY`. Sirve para condiciones sobre agregados (`HAVING COUNT(*) > 30`). Confundirlo con `WHERE` es uno de los errores clásicos.

**JOIN**
Combina filas de dos tablas según una condición. Tipos: `INNER`, `LEFT`, `RIGHT`, `FULL OUTER`, `CROSS`, `SELF`. En la materia se cubrieron los seis tipos pero se usaron sobre todo INNER y LEFT.

**ORDER BY**
Define el orden del resultado (`ASC` o `DESC`). Se aplica al final del pipeline lógico.

**LIMIT / OFFSET**
Paginación: cantidad de filas a devolver y cuántas saltear. Útil para previsualizar o paginar resultados.

**SQLAlchemy**
ORM y toolkit SQL en Python. En la materia se usa el modo "core": `create_engine(...)`, `engine.connect()`, `text("...")`. Permite conectar con SQLite, PostgreSQL, MySQL y otros desde el mismo código.

**create_engine**
Función que devuelve un motor de conexión a una base. La URL define el driver: `sqlite:///archivo.db`, `postgresql://user:pass@host:port/db`.

**to_sql / read_sql**
Métodos de pandas para volcar un DataFrame a una tabla (`df.to_sql(...)`) o leer un query directamente como DataFrame (`pd.read_sql(query, con=engine)`).

---

## LLMs y conexión con el resto del stack

**Embedding**
Representación vectorial densa de un texto, una imagen o un dato categórico. Permite calcular similitud (coseno, euclídea) entre elementos no triviales. En el TP2 aparece como bonus con `sentence-transformers`.

**Similitud coseno**
Métrica de cercanía entre vectores: `cos(θ) = (a · b) / (||a|| · ||b||)`. Va de −1 a 1. Es la métrica natural para comparar embeddings.

**RAG** (Retrieval-Augmented Generation)
Pipeline donde un LLM responde apoyándose en documentos recuperados desde una base vectorial. Etapas estándar (clase 4): ingest → chunk → enriquecer → embed → index → retrieve → generar. En la materia se menciona como ejemplo de cómo el stack de datos se integra con GenAI, no como tema central.

---

**Próximo paso**: `12-formulario.md`
