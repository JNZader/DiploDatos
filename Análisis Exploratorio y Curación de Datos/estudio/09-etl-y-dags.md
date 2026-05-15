# 09 — ETL, DAGs y el ecosistema de datos

## Concepto

Un **pipeline de datos** es la cadena de pasos que mueve un dato desde donde nace (un CSV, una API, una base operacional, una planilla) hasta donde se consume (un dashboard, un modelo, un reporte). La cátedra organiza ese viaje en tres etapas y le pone nombre histórico: **ETL** — *Extract, Transform, Load*.

Las definiciones de cátedra son literales:

- **Extracción**: *"Extraer datos heterogéneos de las distintas fuentes provistas."*
- **Transformación**: *"Normalizar, elegir solo las partes relevantes, interrelacionar los datos."*
- **Load**: *"Agregar todos estos datos al Data Warehouse."*

Sobre ese armazón básico, la materia construye dos ideas más modernas que conviene tener claras desde el arranque:

1. **ELT** (el orden cambió): primero se carga el dato crudo y después se transforma. *"Almacenar es barato y flexible. Guardar primero el dato crudo y transformar después según el caso."*
2. **DAG** (la coordinación se separa del procesamiento): orquestadores como Airflow no procesan los datos; solo coordinan qué tarea va antes que cuál. *"Airflow no procesa datos, solo coordina."*

## Intuición

Pensá una cadena de montaje en una fábrica de autos. Cada estación hace una cosa puntual: una pone el chasis, otra los asientos, otra la pintura. Si la pintura llega antes que el chasis, tenés un quilombo. **El DAG es el plano de la fábrica**: dice qué estación va antes que cuál, qué estaciones pueden trabajar en paralelo y qué pasa si una falla.

El ETL es la cadena de montaje en sí. La extracción es el camión que descarga las piezas (los datos crudos). La transformación es el ensamblado (limpiar, juntar, normalizar). El load es estacionar el auto terminado en el playón (el Data Warehouse).

Y acá viene la gracia: **Airflow no es la cadena de montaje, es el capataz con el plano**. No suelda ni pinta nada. Solo grita "ahora la 1, ahora la 2, si la 2 falla reintentá 3 veces, después llamame".

---

## ETL vs ELT (el shift moderno)

### ETL clásico
1. **E**xtract → leés de la fuente.
2. **T**ransform → en una máquina intermedia (servidor ETL) hacés limpieza, joins, agregaciones.
3. **L**oad → cargás el resultado limpio al Data Warehouse.

Problema histórico: el almacenamiento era caro. Había que llegar al DW con el dato lo más prolijo posible. Eso obligaba a transformar antes de cargar.

### ELT moderno
1. **E**xtract → leés de la fuente.
2. **L**oad → tirás el dato crudo, sin transformar, en un Data Lake o un DW columnar (Snowflake, BigQuery, Databricks).
3. **T**ransform → recién después, dentro del propio almacén, ejecutás SQL/dbt para producir vistas limpias.

Por qué cambió: *"Almacenar es barato y flexible."* Guardar el crudo permite:
- Reprocesar si descubrís un error de limpieza meses después.
- Atender necesidades nuevas que no preveías cuando diseñaste el pipeline original.
- Separar **ingesta** (rápida, automática) de **modelado** (decisiones del negocio).

**Cuándo ETL todavía tiene sentido**: cuando el destino no soporta transformaciones complejas, o cuando hay restricciones legales (no podés guardar PII en crudo).

---

## Batch vs Real-time

Dos formas de mover datos, con stacks diferentes:

| Eje | Batch | Real-time (streaming) |
|---|---|---|
| Cuándo procesa | Cada cierto tiempo (cada hora, cada día) | A medida que llega el dato |
| Latencia típica | Minutos a horas | Milisegundos a segundos |
| Herramientas cátedra | **Airflow**, **Spark** | **Kafka**, **Flink** |
| Caso típico | Reporte diario de ventas, ETL nocturno | Detección de fraude, feed de noticias, IoT |
| Costo | Más barato (recursos on/off) | Más caro (siempre prendido) |

En esta materia el foco es **batch con Airflow**. Streaming aparece como conocimiento de ecosistema, no como tema operativo.

---

## DW vs Lake vs Lakehouse

Tres formas de almacenar el dato analítico. La diferencia es **cuán estructurado y cuán flexible** es el almacén.

### Data Warehouse (DW)
- Esquema fijo, definido por adelantado (*schema-on-write*).
- Pensado para consultas SQL rápidas.
- Datos limpios y modelados (estrella, copo de nieve).
- Ejemplos: **Snowflake**, **Redshift**, **BigQuery**.
- Trade-off: rápido y prolijo, pero rígido. Cambiar el esquema duele.

### Data Lake
- Almacena cualquier formato (CSV, JSON, Parquet, imágenes, audio).
- Esquema se interpreta al leer (*schema-on-read*).
- Barato (suele estar sobre S3 / GCS / Azure Blob).
- Ejemplos: **S3**, **GCS**, **Databricks** (sobre lakes).
- Trade-off: flexible, pero sin gobernanza se vuelve un *data swamp* (pantano).

### Lakehouse
- Lo mejor de los dos mundos: storage barato como un lake, performance y transacciones como un DW.
- Capas de metadatos por encima del lake (Delta Lake, Iceberg, Hudi).
- Ejemplos: **Databricks** (Delta Lake), **Snowflake** (Iceberg), **Apache Iceberg**.
- Trade-off: arquitectura más nueva, herramientas todavía evolucionando.

---

## Modelo Bronze / Silver / Gold (Delta Lake)

Patrón de organización dentro de un Lakehouse. Tres capas progresivamente más limpias:

| Capa | Estado | Quién la usa | Ejemplo en Sysarmy / Melbourne |
|---|---|---|---|
| **Bronze** | Crudo, sin transformar. Ingesta rápida, append-only. | Ingenieros de datos, auditoría. | `melb_data.csv` tal cual lo bajaste de la URL. |
| **Silver** | Depurado: tipos correctos, NaN tratados, joins básicos. | Analistas, científicos de datos. | `melb_data` + `airbnb_by_zip` mergeado, con outliers marcados pero no eliminados. |
| **Gold** | Productos finales: métricas, KPIs, vistas para dashboards. | Negocio, BI, modelos productivos. | `precio_promedio_por_suburbio_mensual` listo para PowerBI. |

La regla mental: **Bronze = lo que entró**, **Silver = lo que es confiable**, **Gold = lo que sirve para decidir**.

Esta separación es la versión "industria" del pipeline que ya venís haciendo en los TPs: el CSV original es bronze, el dataframe después de `dropna` + IQR + recodificación es silver, y el dataframe que mandás al modelo o a la visualización final es gold.

---

## DAG: el plano de la fábrica

**DAG** = *Directed Acyclic Graph* = grafo dirigido acíclico.

- **Grafo**: nodos (tareas) conectados por flechas (dependencias).
- **Dirigido**: las flechas tienen sentido (A va antes que B).
- **Acíclico**: no podés volver al punto de partida (no hay ciclos). Si pudieras, el pipeline no terminaría nunca.

Cita textual de la cátedra: *"Tareas como código (DAGs = Directed Acyclic Graphs). Controla dependencia y secuencia."* Y la clave que define qué hace Airflow: *"Airflow no procesa datos, solo coordina."*

Eso quiere decir: el cálculo, el pandas, el SQL, el spark — todo eso lo ejecutan los **operadores** que vos definís. Airflow solo se encarga de:

1. Disparar las tareas en el orden correcto.
2. Reintentar si fallan.
3. Avisarte por mail / Slack si algo se rompe.
4. Mostrar el estado en una UI web.
5. Programar la próxima corrida.

---

## El stack del ecosistema (mapa)

La cátedra menciona el ecosistema entero. Conviene saber qué hace cada categoría aunque no uses todas las herramientas.

| Categoría | Qué hace | Herramientas cátedra |
|---|---|---|
| **Orquestación** | Coordinar tareas (el "capataz"). | Airflow, Prefect, Dagster |
| **Ingesta** | Mover datos de A a B con conectores predefinidos. | Airbyte, Fivetran, Stitch |
| **Almacenamiento** | DW, Lake, Lakehouse. | BigQuery, Redshift, Snowflake, S3, GCS, Databricks, Iceberg, Delta |
| **Transformación** | Modelar dentro del almacén (SQL versionado). | dbt, dataform |
| **Visualización** | Dashboards. | PowerBI, Tableau, Looker, Metabase |
| **Reverse ETL** | Empujar datos del DW de vuelta a herramientas operacionales (CRM, mail). | Hightouch, Census, Segment |
| **Data Quality** | Validar contratos sobre los datos. | Great Expectations |
| **Streaming** | Procesar en tiempo real. | Kafka, Flink, Spark Streaming |

**Tip mental**: cuando alguien diga "modernizar la plataforma de datos", probablemente esté hablando de elegir herramientas en cada una de estas siete cajas.

---

## Pipeline RAG: ETL para LLMs

Una extensión moderna del ETL que la cátedra menciona explícitamente. Cuando armás un sistema de **Retrieval Augmented Generation** (un chatbot que responde sobre tus documentos), la lógica es la misma cadena de montaje, con nuevas estaciones:

```
ingest  →  chunk  →  enriquecer  →  embed  →  index  →  retrieve  →  generar
```

| Paso | Qué hace | Equivalente ETL |
|---|---|---|
| **Ingest** | Leer PDFs, HTMLs, Confluence, Notion. | Extract |
| **Chunk** | Partir en fragmentos manejables (200-500 tokens). | Transform |
| **Enriquecer** | Agregar metadatos (fecha, autor, categoría). | Transform |
| **Embed** | Convertir cada chunk en un vector. | Transform |
| **Index** | Guardar los vectores en una BD vectorial (Pinecone, Weaviate, pgvector). | Load |
| **Retrieve** | Buscar los chunks más parecidos a la pregunta. | Query |
| **Generar** | El LLM responde usando esos chunks como contexto. | Consumo |

Es ETL, pero con vectores en lugar de filas.

---

## DAGs de datos vs DAGs agénticos

Hay dos familias de DAGs y se confunden seguido.

| Eje | DAG de datos (Airflow clásico) | DAG agéntico (LLM/agentes) |
|---|---|---|
| Determinismo | Determinístico: misma entrada, mismo grafo. | Dinámico: el grafo se reescribe en runtime según las decisiones del LLM. |
| Reintentos | Automáticos, sin intervención humana. | A veces requieren *human-in-the-loop* (aprobación). |
| Predictibilidad | Alta — sabés qué corre y cuándo. | Baja — el LLM puede decidir saltar pasos o crear nuevos. |
| Caso típico | ETL nocturno, reportes, ingesta. | Agente que investiga, decide herramientas, encadena llamadas. |
| Herramientas | Airflow, Prefect, Dagster. | LangGraph, CrewAI, AutoGen. |

La regla: **si el grafo lo dibujás vos a mano y no cambia, es un DAG de datos. Si el LLM decide la próxima tarea en tiempo de ejecución, es agéntico.**

---

## Ejemplo: DAG mínimo en Airflow

El esqueleto más simple posible. Dos tareas, una depende de la otra.

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def extraer():
    # acá leés del CSV / API / DB
    pass

def transformar():
    # acá limpiás, hacés joins, calculás
    pass

with DAG(
    "mi_etl",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
) as dag:
    t1 = PythonOperator(task_id="extraer", python_callable=extraer)
    t2 = PythonOperator(task_id="transformar", python_callable=transformar)

    t1 >> t2  # t1 corre antes que t2
```

El operador `>>` define la dependencia. Si tuvieras una tercera tarea de carga: `t1 >> t2 >> t3`. Si dos tareas pueden ir en paralelo después de t1: `t1 >> [t2, t3]`.

Lo importante: las funciones `extraer` y `transformar` son **Python normal**. Airflow no las "magicea": solo decide cuándo ejecutarlas y qué hacer si fallan.

---

## Ejemplo: ETL completo con SQLAlchemy (notebook 04_2)

El patrón canónico de la materia para un ETL de verdad: leer un CSV, transformar, escribir a una base, ejecutar un script SQL de carga.

```python
from sqlalchemy import create_engine, text
import pandas as pd
import datetime as dt
from decouple import config

# Credenciales fuera del código (python-decouple lee .env)
DB_USER = config("DB_USER")
DB_PASSWORD = config("DB_PASSWORD")
DB_HOST = config("DB_HOST")
DB_PORT = config("DB_PORT", default=5432, cast=int)
SQL_SCRIPT = config("SQL_SCRIPT", default="load.sql")

def connection_db():
    return create_engine(
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/survey",
        echo=False,
        client_encoding="utf8",
    )

def extract(url):
    return pd.read_csv(url)

def transformation(df, engine, tablename):
    df["fecha"] = dt.date.today()
    df.columns = df.columns.str.lower()
    df.to_sql(tablename, con=engine, if_exists="replace")

def load(engine):
    with engine.connect() as conn:
        conn.execute(text(open(SQL_SCRIPT).read()))
```

Cada función es una **etapa explícita** del ETL. Cada una se puede llamar desde un `PythonOperator` del DAG y reintentar de manera independiente.

Notá tres detalles importantes:
- **Credenciales con `python-decouple`**: las lee de un archivo `.env` que no se sube a git. Nunca quedan hardcodeadas.
- **Query SQL en archivo separado** (`SQL_SCRIPT`): el SQL no vive como string dentro del .py, vive en su propio archivo `.sql`. Eso permite que un DBA lo revise, que `git diff` muestre cambios SQL limpios, y que un linter SQL lo procese.
- **`if_exists="replace"`**: idempotencia. Si corro el ETL dos veces, no duplico filas.

---

## Buenas prácticas (las que la cátedra explicita)

### 1. Credenciales fuera del código (`python-decouple` + `.env`)
Nunca pongas `password = "mi_pass_secreto"` en un archivo `.py`. Usá un `.env`:

```
DB_USER=javier
DB_PASSWORD=cambiame
DB_HOST=localhost
```

Y leelo con `from decouple import config; DB_USER = config("DB_USER")`. El `.env` va a `.gitignore` y nunca termina en GitHub.

### 2. Queries en archivos `.sql` separados
Si tu query tiene más de 3 líneas, sacala del Python. Beneficios:
- Tu IDE le pone resaltado de sintaxis SQL.
- Un DBA puede revisarla sin entender Python.
- `git diff` muestra cambios SQL limpios.
- Podés versionarla aparte (migraciones, dbt, etc.).

### 3. `logging` con niveles, no `print`
`print` es para debuggear en una notebook. En un pipeline productivo, usá `logging`:

```python
import logging
log = logging.getLogger(__name__)

log.info("Extracción iniciada: %s", url)
log.warning("Encontramos %d filas con NaN en Price", n_nans)
log.error("Falló el merge: %s", e)
```

Los niveles (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`) te dejan filtrar después: en producción solo querés ver `WARNING` para arriba.

### 4. Parquet como destino, no CSV
Cuando guardás un dataset intermedio o final, **preferí Parquet**:
- **Columnar**: leer una columna no obliga a leer todo el archivo.
- **Comprimido**: típicamente 3-10× más chico que el CSV equivalente.
- **Tipado**: guarda tipos (int, float, datetime) — no perdés información en la serialización.
- **Lectura selectiva**: `pd.read_parquet("file.parquet", columns=["Price", "Suburb"])` solo levanta esas dos columnas.

```python
df.to_parquet("melb_silver.parquet")
df2 = pd.read_parquet("melb_silver.parquet", columns=["Price", "Suburb"])
```

CSV solo para intercambio humano o cuando la otra punta no soporta Parquet.

### 5. Validar siempre la carga
Después de cada operación crítica, un `assert`:

```python
assert len(merged) == len(melb_df), "El merge cambió la cantidad de filas"
assert merged["Price"].isna().sum() == 0, "Aparecieron NaN en Price post-merge"
assert merged["airbnb_price_mean"].dropna().between(0, 10000).all()
```

Si algo se rompe, querés enterarte en el DAG, no en el dashboard.

---

## Conexión con el TP

- **TP2 — Opcionales (ETL .py + DAG Airflow)**: el enunciado pide armar el ETL del pipeline `melb_data` → SQLite → consultas con SQLAlchemy como script `.py` separado, y bonus armar un DAG mínimo en Airflow para correrlo automáticamente. La estructura del ETL completo que vimos arriba (`connection_db`, `extract`, `transformation`, `load`) es exactamente el molde a copiar.
- **TP2 — Persistencia del dataset final**: cuando guardes el dataset enriquecido (`melb_data` + AirBnB + outliers limpios + variables nuevas), elegí Parquet sobre CSV. Justificalo en el documento: menos espacio, lectura selectiva, tipos preservados.
- **TP2 — Bonus embeddings y LLM**: el pipeline de embeddings sobre `CouncilArea` o `Suburb` es la versión "para una sola variable" del pipeline RAG que vimos: ingest (texto) → embed (sentence-transformers) → similitud coseno. Es ETL, pero con vectores.
- **Bronze/Silver/Gold mental**: el `melb_data.csv` original es bronze; el dataframe tras `dropna`, IQR y merge con AirBnB es silver; el dataset final que guardás es el gold de este trabajo.

---

## Errores comunes

1. **Hacer ETL sin logging**: usás `print` en una notebook y cuando lo mudás a un script `.py` corriéndose de noche en un servidor, te enterás de los errores tres semanas después. Logging con niveles desde el día uno.
2. **Queries SQL como strings inline en el .py**: terminás con un string de 80 líneas dentro de una función Python, sin syntax highlighting, imposible de revisar. Las queries van en archivos `.sql` aparte.
3. **No validar la carga**: hacés un merge, asumís que está bien, y dos semanas después el dashboard muestra precios negativos. **Assertions post-merge obligatorias**: filas, nulos, rangos.
4. **Escribir CSV cuando Parquet sería mejor**: el CSV se siente "humano" pero te cuesta espacio, lectura completa siempre y pérdida de tipos. Reservá el CSV para intercambio puntual; para almacenamiento intermedio o final, Parquet.
5. **Credenciales hardcodeadas en el código**: meter `DB_PASSWORD = "..."` directo en el `.py` es un boleto al cementerio de incidentes de seguridad. `python-decouple` + `.env` + `.gitignore` desde el minuto cero.
6. **Confundir Airflow con un motor de procesamiento**: Airflow **coordina**, no procesa. Si tu pandas tarda 3 horas, ponerlo dentro de un DAG no lo va a acelerar — para eso necesitás Spark, Dask, o repensar la query.
7. **Mezclar DAG de datos con DAG agéntico**: querer hacer un agente con LLM dentro de un Airflow tradicional. Andan diferente: uno es determinístico, el otro decide en runtime. Cada uno con su herramienta.
8. **Saltar Bronze**: querer transformar el dato crudo "en el momento" y no guardar nunca el original. Cuando descubrís un bug de limpieza, no tenés a qué volver. Siempre dejá el crudo guardado en algún lado.

---

## Checklist de comprensión

- [ ] ¿Cuál es la diferencia entre ETL y ELT y por qué ELT se volvió la opción por defecto en la última década?
- [ ] Si te muestran un DAG con 6 tareas, ¿cómo sabés cuál corre primero y cuáles pueden correr en paralelo?
- [ ] ¿Por qué Airflow "no procesa datos" si el código de las tareas está escrito en Python adentro del DAG?
- [ ] Describí en una frase qué hay en Bronze, qué en Silver, y qué en Gold.
- [ ] Tenés una API key para conectar a una base de datos. ¿Dónde va? ¿Por qué no en el `.py`?
- [ ] Vas a guardar un dataset de 10 millones de filas para que otro pipeline lo consuma. ¿CSV o Parquet? ¿Por qué?

---

**Próximo paso**: `10-sql-basico.md`
