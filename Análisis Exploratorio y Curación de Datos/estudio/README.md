# Apuntes de estudio v2 — Análisis Exploratorio y Curación de Datos

## Qué son estos apuntes

Esta es una reconstrucción pedagógica de la materia **Análisis Exploratorio y Curación de Datos** (DiploDatos 2026, docentes: José Robledo y Ariel Wolfman). No es un copy-paste de las clases: es una reorganización pensada para que entiendas el **porqué** antes del **cómo**, y para que cada concepto se conecte directamente con los dos trabajos prácticos que tenés que entregar.

El dataset que recorre toda la materia es **Melbourne Housing Snapshot** (`melb_data.csv`, 13.580 filas × 21 columnas). Aparece desde Clase 1 hasta Clase 4 y es el corazón de los dos TPs. Si lo entendés bien, entendés la materia.

## Estructura y progresión lógica

Los archivos están ordenados para que no te encuentres con PCA antes de entender qué es escalar, ni con un merge antes de saber qué es una clave. La regla es: **cada archivo depende de los anteriores**.

| Orden | Archivo | Qué cubre | Depende de |
|-------|---------|-----------|------------|
| 0 | [`00-python-y-pandas-para-curacion.md`](00-python-y-pandas-para-curacion.md) | Refresher pandas con foco curación: DataFrame, dtypes, `.copy()`, loc/iloc, select_dtypes, groupby + agg | Nada |
| 1 | [`01-introduccion-y-curacion.md`](01-introduccion-y-curacion.md) | Qué es curación, pipeline completo, 7 dimensiones de calidad, EDA vs curación | 00 |
| 2 | [`02-datos-faltantes.md`](02-datos-faltantes.md) | NaN vs None, taxonomía Rubin (MCAR/MAR/MNAR), estrategias (eliminar, SimpleImputer, KNN, MICE), análisis con missingno | 00, 01 |
| 3 | [`03-sesgo.md`](03-sesgo.md) | Sesgo formal, dilema sesgo-varianza, tipos (selección, información, supervivencia, retroalimentación, procesamiento), casos famosos | 01 |
| 4 | [`04-tipos-de-variables-y-encodings.md`](04-tipos-de-variables-y-encodings.md) | Categóricas (ordinales/nominales) vs numéricas, OrdinalEncoder, OneHotEncoder, DictVectorizer, codificación de frecuencia, curse of dimensionality | 02, 03 |
| 5 | [`05-transformaciones.md`](05-transformaciones.md) | Escalar vs normalizar vs encoding, MinMax/Robust/Standard/MaxAbs, PowerTransformer (Box-Cox / Yeo-Johnson), Quantile | 04 |
| 6 | [`06-pca.md`](06-pca.md) | Intuición geométrica, los 5 pasos, por qué escalar siempre, explained_variance_ratio_, ejemplo Iris | 04, 05 |
| 7 | [`07-exploracion-eda.md`](07-exploracion-eda.md) | Definición operativa, 7 etapas, univariado/bivariado/multivariado, outliers IQR, fechas, ydata_profiling | 02, 03, 04, 05 |
| 8 | [`08-combinacion-de-datasets.md`](08-combinacion-de-datasets.md) | join vs merge, 4 tipos, groupby + agg previo, validación post-merge con assertions | 00, 07 |
| 9 | [`09-etl-y-dags.md`](09-etl-y-dags.md) | ETL/ELT, Bronze/Silver/Gold, DAG en Airflow, stack del ecosistema, buenas prácticas | 08 |
| 10 | [`10-sql-basico.md`](10-sql-basico.md) | SQLite, sintaxis general, agregaciones, HAVING vs WHERE, 6 tipos de JOIN, SQLAlchemy, equivalencias Pandas/SQL | 08, 09 |
| 11 | [`11-glosario.md`](11-glosario.md) | Definiciones conceptuales agrupadas por tema | Todo |
| 12 | [`12-formulario.md`](12-formulario.md) | Sintaxis comentada de cada técnica con explicación de cuándo usarla | 02-10 |
| 13 | [`13-preguntas-guia.md`](13-preguntas-guia.md) | 83 preguntas de auto-examen por tema + bloque TPs + trampas cruzadas | Todo |
| 14 | [`14-bibliografia.md`](14-bibliografia.md) | Guía de uso de la bibliografía complementaria + docs oficiales | Todo |
| 15 | [`15-guia-de-tps.md`](15-guia-de-tps.md) | Guía paso a paso de TP1 y TP2, ejercicio por ejercicio, con criterios de evaluación | Todo |

## Cómo se lee cada archivo (00 a 10)

Cada archivo temático sigue esta estructura fija:

1. **Concepto**: qué es y por qué importa.
2. **Intuición**: la explicación "para un amigo" antes de la fórmula.
3. **Cuerpo técnico**: lo formal — fórmulas, taxonomías, técnicas — con explicación de cada elemento.
4. **Ejemplo numérico**: con datos concretos, no solo variables abstractas.
5. **Conexión con el TP**: "Esto lo vas a usar cuando..." con cita al ejercicio puntual.
6. **Errores comunes**: lo que la cátedra detecta seguido.
7. **Checklist de comprensión**: 2-3 preguntas para autoevaluarte.

Los archivos 11-14 son utility (glosario, formulario, preguntas, bibliografía) y siguen el formato de su tipo. El 15 es la guía completa de TPs.

## Analogías que vas a encontrar

- **El DataFrame como planilla de Excel con superpoderes y memoria** (00)
- **La curación como preparar ingredientes antes de cocinar** (01)
- **La lluvia para Rubin**: MCAR (azar puro), MAR (terreno alto), MNAR (paraguas) (02)
- **El sesgo como un dedo en la balanza**: qué tan visible es, quién lo puso (03)
- **El encoding como traducir de un idioma a otro**, con o sin preservar orden (04)
- **Escalar como cambiar la escala del mapa** (no cambia la forma); **normalizar como cambiar la proyección** (cambia la forma) (05)
- **PCA como sacar una foto desde el ángulo que mejor abre el objeto** (06)
- **El EDA como abrir una caja de fotos antiguas** antes de contar (07)
- **El merge como cruzar dos planillas por el DNI** (08)
- **El ETL como cadena de montaje en una fábrica**, con un capataz (el DAG) que coordina (09)
- **SQL como pedir comida en un restaurante** (SELECT qué quiero, FROM dónde, WHERE con qué condición) (10)

## Regla de oro de esta materia

> **Un pipeline correcto en código pero flojo en criterio es un pipeline incorrecto.**

No alcanza con que `knn.fit_transform()` corra. Tenés que poder justificar por qué imputaste con KNN y no con la media, por qué dropeaste esas 612 filas con `Price > 2.35M`, por qué reduciste Suburb a top-20, y por qué decidiste tratar `Date` como ordinal en lugar de descartarlo. La cátedra explicita en el TP2: *"No se espera una única solución correcta"* — pero sí esperan que justifiques cada decisión.

---

## Mapa rápido: de los TPs a los archivos

| TP | Ejercicio | Conceptos centrales | Archivos de estudio |
|----|-----------|---------------------|---------------------|
| **TP1** | Ej1 (Encoding) | Selección de filas/cols, faltantes preliminares, dtypes, OHE, reducción de cardinalidad, tratamiento de Date | 00, 01, 02, 04, 07 |
| **TP1** | Ej2 (Imputación KNN) | IterativeImputer + KNeighborsRegressor, decisión de estandarizar, visualización antes/después | 02, 05 |
| **TP1** | Ej3 (PCA) | n_components (con el typo), por qué escalar, explained_variance_ratio_, features nuevas | 05, 06 |
| **TP1** | Ej4 (Composición) | Reconvertir matriz a DataFrame con nombres originales | 04 |
| **TP1** | Ej5 (Documentación) | Justificar cada decisión de curación | 01, 11, 15 |
| **TP2** | Ej1 (SQL) | SQLite + SQLAlchemy, ingesta con validación de tipos, 5 queries, JOIN equivalente a merge, assertions post-JOIN | 08, 09, 10 |
| **TP2** | Ej2 (Pandas) | Subset + outliers IQR + enriquecimiento con AirBnB (mediana vs media, agregar antes de merger) | 07, 08 |
| **TP2** | Ej3 (Persistencia) | Guardar dataset final (CSV o Parquet) | 09 |
| **TP2** | Ej4 (Opcionales) | ETL .py + DAG Airflow + embeddings con sentence-transformers + curación asistida por LLM | 09 |

---

## Caminos sugeridos según tiempo disponible

- **Tenés 2 horas antes del TP1**: leé `15-guia-de-tps.md` (sección TP1) + `02-datos-faltantes.md` + `04-tipos-de-variables-y-encodings.md` + `06-pca.md`. Mirá `12-formulario.md` para la sintaxis exacta.

- **Tenés 2 horas antes del TP2**: leé `15-guia-de-tps.md` (sección TP2) + `08-combinacion-de-datasets.md` + `10-sql-basico.md`. Tené abierto `12-formulario.md` para SQL y SQLAlchemy.

- **Tenés un día completo para estudiar**: hacé el recorrido completo en orden (00 → 15). El glosario y el formulario son referencia, no se leen lineal.

- **Estás repasando para un parcial / coloquio**: leé el `11-glosario.md` y respondé el `13-preguntas-guia.md` en papel. Si dudás, volvé al archivo temático correspondiente.

---

**Carpeta `_v1_backup/`**: contiene la primera versión de estos apuntes (más cruda, sin la estructura pedagógica fija). Se guarda como referencia, no se mantiene.
