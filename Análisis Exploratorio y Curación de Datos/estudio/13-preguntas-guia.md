# 13 — Preguntas guía para estudiar

Estas preguntas no son un examen: son un espejo. Si las podés responder en voz alta con un ejemplo concreto del notebook o del TP, entendés. Si balbuceás, hay un hueco. Cada bloque sigue al archivo de estudio correspondiente.

---

## Bloque 01 — Python y pandas para curación

1. ¿Qué hace `df.copy()` que no hace `df2 = df1`? ¿Por qué la cátedra insiste con la frase *"nunca accionar sobre el dataset original"*?
2. Una columna numérica entra como `object` en `df.info()`. Listá tres causas posibles y cómo las descartarías.
3. ¿Qué muestra `df[df == 0].count(axis=0)` y por qué es la primera línea que se corre en la clase 1?
4. ¿Cuándo `Bathroom == 0` es un faltante enmascarado y cuándo `Car == 0` es un valor válido? ¿Cómo decidís sin preguntarle al cliente?
5. ¿Qué diferencia hay entre `df.dropna()`, `df.dropna(subset=['Price'])` y `df.dropna(axis=1, thresh=...)`?
6. `pandas` saltea `NaN` automáticamente al calcular `mean()`. ¿En qué escenario esto es una trampa, no una conveniencia?

## Bloque 02 — Datos faltantes y mecanismos de pérdida (Rubin)

7. Definí MCAR, MAR y MNAR con tus palabras y mostrá un ejemplo de `melb_data` para cada uno.
8. ¿Por qué el dataset `melb_data` tiene `BuildingArea` con ~6450 faltantes y eso no es necesariamente MCAR?
9. Si un atributo es MNAR, ¿qué dice la cátedra que hay que hacer? ¿Por qué cualquier imputación introduce sesgo?
10. ¿Qué requisito tiene `KNNImputer` sobre los datos de entrada que `SimpleImputer` no exige?
11. Tenés una columna categórica con 15% de faltantes. ¿Usás `SimpleImputer` con `strategy='most_frequent'` o `strategy='constant'`? Defendé las dos opciones con un caso donde cada una sea mejor.
12. Explicá la regla de Rubin (`var_total = var_dentro + var_entre`) y por qué es el fundamento de MICE.
13. ¿Qué riesgo aparece al imputar la columna de testing usando estadísticos calculados con todo el dataset (train + test)?

## Bloque 03 — Sesgo y dilema sesgo-varianza

14. Escribí la fórmula `Bias(T) = E(T) − θ` y traducila a una situación de la encuesta Sysarmy.
15. Diferenciá sesgo de autoselección y sesgo de supervivencia con ejemplos distintos a los de clase.
16. ¿Por qué Abraham Wald recomendó reforzar las zonas SIN impactos del avión? ¿Qué error de razonamiento estaba evitando?
17. ¿Cómo se manifestó el caso de Países Bajos 2013 (fraude fiscal con IA) como combinación de sesgo de selección y sesgo de procesamiento?
18. Diana de tiro: dame un ejemplo de un modelo con bajo sesgo y alta varianza, y otro con alto sesgo y baja varianza.
19. ¿Qué sesgo introducís vos como analista cuando hacés *cherry picking* de filtros para que el resultado "se vea bonito"?
20. ¿Qué sesgos persisten incluso después de una limpieza impecable del CSV y por qué no son problema de curación?

## Bloque 04 — Encodings y maldición de la dimensionalidad

21. ¿Por qué `OrdinalEncoder` sobre una variable nominal como `Suburb` es un error conceptual? ¿Qué le pasa a un modelo lineal entrenado sobre eso?
22. ¿Qué problema concreto resuelve `drop_first=True` en `get_dummies` o `OneHotEncoder`?
23. Una columna tiene 200 categorías únicas. ¿Hacés OHE, codificación de frecuencia o reducís cardinalidad primero? Justificá.
24. ¿Qué quiere decir que los vectores OHE son "ortogonales equidistantes con norma 1" y por qué eso rompe distancias en KNN?
25. ¿Por qué `DictVectorizer` devuelve una matriz esparsa y qué pasa si llamás `.todense()` sin pensar?
26. La curse of dimensionality afecta a KNN, K-means y SVM, pero no a árboles de decisión. ¿Por qué?

## Bloque 05 — PCA

27. ¿Qué garantiza que las componentes principales sean ortogonales entre sí? ¿Qué significa eso geométricamente?
28. ¿Por qué la cátedra dice que escalar antes de PCA es "fundamental" y no "recomendable"? Apoyate en el ejemplo Iris (MinMax vs Standard).
29. ¿Qué decisión cambia si usás `n_components=20` versus `n_components=0.90`?
30. ¿Cómo elegirías el corte mirando la curva de varianza explicada acumulada? ¿Qué hacés si no hay codo claro?
31. Después de PCA, ¿qué significa una "componente"? ¿Podés interpretarla como una feature original?
32. En el TP1, la consigna pide `n_components = min(20, X.shape[0])`. Con 13.580 filas eso da 20. ¿Por qué es razonable sospechar que la cátedra quiso escribir `X.shape[1]`?

## Bloque 06 — Transformaciones (escalar vs normalizar)

33. ¿Cuál es la diferencia exacta entre escalar y normalizar en el sentido de esta materia?
34. ¿Por qué `StandardScaler` con outliers degrada y `RobustScaler` no? Apoyate en cómo se calcula cada uno.
35. ¿Cuándo elegirías `MaxAbsScaler` por encima de `StandardScaler`?
36. Explicá la diferencia entre Box-Cox y Yeo-Johnson. Si no sabés si tu variable es positiva, ¿cuál usás por default?
37. `QuantileTransformer(output_distribution='normal')` produce una distribución gaussiana, pero la cátedra advierte algo. ¿Qué?
38. ¿Por qué `Normalizer(norm='l2')` opera sobre filas y no sobre columnas? ¿En qué caso eso es lo que querés?

## Bloque 07 — EDA práctico (clase 3)

39. Listá las 7 etapas del protocolo de EDA y explicá por qué el orden importa.
40. ¿Qué información extra te da el `boxplot` de `Price` por `Type` que no te da el `describe()` por `Type`?
41. ¿Cuál es la diferencia entre análisis univariado y bivariado? Dame un ejemplo de cada uno aplicado a `melb_data`.
42. ¿Para qué sirve `df.corr().abs()` en lugar de `df.corr()` cuando hacés el heatmap?
43. Las top correlaciones con `Price` en `melb_data` son `Rooms` (0.497), `Bedroom2` (0.476), `Bathroom` (0.467), `YearBuilt` (0.324). ¿Por qué `Rooms` y `Bedroom2` casi se duplican y qué decisión de feature selection sugiere?
44. ¿Por qué `ydata_profiling` es complemento y no reemplazo del EDA manual?
45. La cátedra **no usa** Q-Q plots, KDE independientes, pairplots ni tests formales de normalidad (Shapiro, KS). ¿Por qué? ¿Qué decisión metodológica representa esa elección?

## Bloque 08 — Outliers (IQR y compañía)

46. Mostrá el cálculo paso a paso de outliers por IQR usando `Price` (Q1≈650K, Q3≈1.33M). ¿Cuántos detectaste?
47. ¿Por qué la cátedra **no** usa z-score para detectar outliers? Pensalo desde el lado de la media y la varianza.
48. ¿Qué información extra agrega un `scatterplot` coloreado por "es outlier" que un boxplot no muestra?
49. Tu modelo predice precio de casas. ¿En qué casos eliminarías el outlier y en qué casos lo conservarías?
50. ¿Por qué la regla `1.5 × IQR` es operativa pero no sagrada? ¿Qué cambia con `3 × IQR`?

## Bloque 09 — Combinación de datasets (merge / join)

51. Diferencia entre `df.join` y `df.merge`. ¿Por qué `merge` es la herramienta cotidiana?
52. ¿Cuál es la diferencia entre `inner`, `left`, `right` y `outer` en `merge`? Dame un caso del TP2 para cada uno.
53. En el notebook 04_1, el merge ingenuo de `melb_data` con AirBnB produce 2 millones de filas. ¿Por qué pasó eso y cuál fue la solución?
54. Listá las tres validaciones obligatorias post-merge que la cátedra hace con `assert`.
55. La cátedra dice que la "clave" puede ser un identificador, una fecha, una coordenada GPS, una entidad nombrada o un embedding. Dame un caso de uso donde la clave NO sea una columna alfanumérica.
56. `Postcode` en `melb_data` está como `float` (por los NaN). ¿Qué pasa si lo mergeás directamente contra `zipcode` que está como `int`?

## Bloque 10 — ETL, DAGs, SQL

57. Diferenciá ETL de ELT con la justificación que da la cátedra (*"almacenar es barato y flexible..."*).
58. ¿Qué hace exactamente Airflow y qué NO hace? Citalo con la frase de clase.
59. Definí Bronze / Silver / Gold y dame un ejemplo concreto de qué tabla iría en cada capa.
60. ¿Qué diferencia hay entre un Data Warehouse, un Data Lake y un Lakehouse?
61. En SQL, ¿cuál es la diferencia entre `WHERE` y `HAVING`? Si querés filtrar por una variable cruda y por un agregado en la misma consulta, ¿en qué cláusula va cada uno?
62. ¿Por qué `COUNT(*)`, `COUNT(1)` y `COUNT(col)` pueden dar resultados distintos? ¿En qué caso difieren?
63. ¿Qué ventaja operativa tiene `pd.read_sql` sobre el patrón `engine.connect() + text() + DataFrame(rs.fetchall())`?
64. En `to_sql`, ¿qué hace cada opción de `if_exists`? ¿Cuándo elegís `'append'` sobre `'replace'`?
65. ¿Por qué la cátedra recomienda Parquet como destino sobre CSV?

## Bloque TP1 — Encoding + KNN + PCA + composición

66. ¿Por qué la consigna pide hacer encoding ANTES de agregar `BuildingArea` y `YearBuilt` para la imputación con `IterativeImputer`?
67. Para tratar la columna `Date` en TP1, ¿la descartás, la convertís a ordinal o la separás en año/mes? Defendé tu elección.
68. `Suburb` tiene cientos de categorías. ¿Cómo reducís cardinalidad sin perder señal antes del OHE?
69. La consigna pregunta explícitamente si hace falta estandarizar antes de `IterativeImputer(estimator=KNeighborsRegressor)`. ¿Sí o no, y por qué?
70. Después de PCA, ¿agregás las componentes principales como nuevas features o reemplazás las originales? Defendé.
71. `OneHotEncoder.get_feature_names_out()` ¿qué te devuelve y por qué lo necesitás al final del pipeline?

## Bloque TP2 — SQL + Pandas + AirBnB

72. En el TP2 hay que ingestar `melb_data` y `airbnb_price_by_zipcode` en SQLite con SQLAlchemy. ¿Qué validaciones de tipo hacés sobre `Date` y `Price` antes de cargar?
73. Diseñá la consulta SQL que devuelve el AVG de `Price` por `Type` y `Regionname`. ¿Qué cláusulas usás y en qué orden lógico ejecuta el motor?
74. ¿Cómo justificás mediana versus media al agregar precios de AirBnB por zipcode? ¿Qué cambia para el merge final?
75. ¿Qué pasa con propiedades en `melb_data` cuyo `Postcode` no tiene match en `airbnb_price_by_zipcode`? ¿Cómo manejás esos nulos y cómo lo reportás?
76. Listá las tres preguntas que le harías a un experto inmobiliario antes de elegir variables alternativas para el join (latitud/longitud, suburbio, distancia al centro, etc.).
77. El bonus de embeddings sobre `CouncilArea` propone calcular similitud coseno. ¿Cuándo te sirve sustituir un categórico por un embedding y cuándo no?
78. ¿Qué validaciones post-JOIN explícitas (con `assert`) corresponden al TP2?

## Bloque "Trampas cruzando temas"

Estas requieren conectar más de un tema. Si no podés responderlas, releé los archivos involucrados.

79. Tenés un dataset con `Price` (numérica con outliers fuertes), `Suburb` (200 categorías nominales) y faltantes en ambos. Diseñá el orden completo del pipeline: imputación, encoding, transformación, PCA. Justificá cada paso y explicá por qué el orden inverso rompería el resultado.
80. Un compañero corrió PCA directo sobre `melb_data` sin escalar ni imputar. Obtiene que la PC1 explica el 99% de la varianza. ¿Por qué eso es sospechoso y qué columna está dominando casi seguro?
81. Hiciste `merge` por `Postcode` y obtuviste 10× más filas que antes. Explicá los dos motivos posibles (cardinalidad de la clave en cada lado) y cómo los diagnosticarías con código.
82. La conclusión "la zona X tiene precios más altos" cambia totalmente cuando agregás `Type` al `GROUP BY` (de departamentos a casas). ¿Cómo se llama este fenómeno y qué tiene que ver con sesgo de omisión?
83. Después de aplicar `QuantileTransformer(output_distribution='normal')` a todas las features, el modelo lineal explica mejor la varianza pero las correlaciones entre features cambiaron. ¿Por qué pasó eso y en qué contexto sería aceptable y en cuál no?

---

## Cómo usar estas preguntas

- Respondé en voz alta o por escrito.
- Si te tropezás, abrí el archivo correspondiente y volvé a leer la sección.
- Las preguntas del bloque "trampas" requieren conectar varios temas: si no las podés responder con seguridad, todavía no integraste el material.

**Próximo paso**: `14-bibliografia.md`
