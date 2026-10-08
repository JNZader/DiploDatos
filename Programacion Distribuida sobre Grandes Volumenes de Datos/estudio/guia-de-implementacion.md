# Guía de implementación: Programación Distribuida sobre Grandes Volúmenes de Datos (Diplodatos, FAMAF UNC, Damián Barsotti)

**Videos:** C1P1, C1P2, C2P1, C2P2, C2P3, C3P1, C3P2, C3P3, C4P1, C4P2, C4P3. El apunte de estudio que acompaña esta guía es `programacion-distribuida-grandes-volumenes-apunte-de-estudio.md`.
**De qué va:** la parte práctica de la materia, ordenada por tema y no por clase: el word count y la API de RDD, la evaluación perezosa y el cache medidos con un contador, Spark SQL y DataFrames con los usuarios de Last.fm y los vuelos de 2008, UDF, planes de ejecución, Parquet, ORC, tablas y joins con broadcast, MLlib con el dataset de personas (árbol, bosque, logística, SVM lineal, expansión polinomial), pipelines y hashing de texto, KMeans y grafos con GraphFrames sobre la red de retuits (grados, PageRank, influencia colectiva y motif finding).

> Nota: los links llevan al minuto de la clase donde se ve cada cosa ("C2P1 1:23:45" es la clase 2, parte 1, en la hora 1, minuto 23, segundo 45). En clase los notebooks son de Zeppelin y corren en el contenedor Docker del curso; acá todo está escrito como scripts de PySpark que corrí en el box con Python 3.13, PySpark 3.5.9, Java 17 (Temurin JRE), pandas 3.0.6, pyarrow y GraphFrames 0.8.4 para Spark 3.5, en modo `local[*]` con 8 núcleos. Los datos son los de la carpeta `ds/` del repositorio público 2019 del docente (`git.cs.famaf.unc.edu.ar/dbarsotti/diplodatos_bigdata`); el repo 2026 (Bitbucket) no es público, así que pueden aparecer diferencias con los notebooks de este año, y las marco. En Zeppelin `sc`, `spark` y `z` ya existen: borrá la creación de la SparkSession y el `spark.stop()` del final. Lo que aparece como "lo que da en el box" es la salida real.

> **Sobre los ejercicios.** Los ejercicios de los notebooks son la evaluación de la materia y el docente pidió hacerlos solos, sin inteligencia artificial C3P1 38:17, C4P3 2:00:14. Por eso esta guía trae el código de lo que se muestra en clase, pero **no** las soluciones de los ejercicios: en la sección 12 está qué pide cada uno, qué parte de la clase lo prepara y, cuando el docente dio un número de control, si ese número cierra.

## Checklist para arrancar ya
1. Cloná el repo de la materia y hacé `git pull` antes de cada clase; el docente corrige notebooks entre clases C1P1 2:21:08, C3P1 2:23 (sección 0).
2. Levantá el contenedor con los volúmenes `-v` del script `zeppelin.sh` o `zeppelin.cmd`: lo que no esté en una carpeta montada se pierde al apagar C1P2 7:26, C3P1 1:19:26 (sección 0).
3. Mirá `sc.master` y `sc.defaultParallelism` al empezar: 8 en una máquina de 8 núcleos, 2 en el CCAD C2P1 31:09 (sección 1).
4. Acordate de que nada corre hasta una acción; si algo "anduvo" demasiado rápido, probablemente no se ejecutó C2P1 1:14:19 (secciones 2 y 3).
5. Si vas a usar un RDD o DataFrame en dos acciones, cachealo; si no, se recalcula entero C2P1 1:33:17 (sección 3).
6. Leé `flights.csv` con `.option("nullValue", "NA")`: sin eso DepDelay, ArrDelay y AirTime quedan como texto y una UDF que compara números revienta (sección 6).
7. Declará el tipo de retorno de cada UDF (`IntegerType()`, etc.) y preferí funciones nativas (`when`, `avg`...) cuando existan: la UDF de Python agrega un paso `BatchEvalPython` C3P1 14:25 (sección 6).
8. Importá lo que usás de `pyspark.sql.functions` (`avg`, `count`, `desc`, `col`); en clase falla por un `avg` sin importar C3P1 1:01:31 (secciones 5 y 6).
9. En joins contra una tabla chica, usá `broadcast()` y confirmá `BroadcastHashJoin` en el plan C3P1 1:35:23 (sección 7).
10. Después de leer el JSON de personas, hacé `repartition(sc.defaultParallelism)`: llega en una sola partición C3P2 22:01 (sección 8).
11. StringIndexer es un Estimator: primero `fit`, después `transform`; dentro de un Pipeline se ajusta solo C3P2 37:21, C4P1 46:00 (secciones 8 y 9).
12. PolynomialExpansion es un Transformer: aplicala igual al train, al test y a la grilla C3P3 24:19 (sección 8).
13. Con HashingTF, usá un `numFeatures` grande y potencia de 2; con 1000 las colisiones son frecuentes (sección 9).
14. Para GraphFrames en Python: `id` en vértices, `src` y `dst` en aristas; no hay `GraphFrame.fromEdges` en Python 0.8.4, armá los vértices con `union` y `distinct` C4P3 17:25, C4P3 51:12 (sección 11).
15. Exportá a Gephi con `coalesce(1)` solo resultados chicos C4P3 28:13 (sección 11).
16. Entregas: notebooks 1 a 4 la penúltima semana de octubre, 5, 6 y 8 la última, cada uno con su formulario; el 8 con las imágenes de Gephi C4P3 2:01:19 (sección 12).

## Versión completa

### 0. El entorno
**En clase:** C1P1 2:14:19, C1P1 2:18:15, C1P2 0:07, C1P2 4:03, C1P2 10:11, C2P1 2:57, C3P1 1:18:40, C3P1 1:22:15

Hay dos caminos. El recomendado es Docker local: con Git y Docker instalados y al menos 8 GB de RAM, desde la carpeta `docker` del repo corrés `zeppelin.sh` (Linux) o `zeppelin.cmd` (Windows) C1P2 1:15; la primera vez construye la imagen y puede tardar, porque baja unos 9 GB C1P2 5:18. Después abrís `localhost:8080` (Zeppelin), importás el JSON del notebook con "Import note" y mirás la Spark UI en `localhost:4040` C1P2 10:11, C1P2 46:06. El otro camino es el JupyterHub del CCAD con cuenta UNC (entorno "diplodatos", botón de Zeppelin), con 2 núcleos y solo el home persistente C1P1 2:18:15, C2P1 4:07, C3P1 1:21:05.

Qué tenés que hacer:
- No borres los `-v` del comando: montan conf, logs, notebooks y el repo; sin ellos, todo lo que escribas muere con el contenedor. El `--rm` borra el contenedor al apagarlo, así que lo único que sobrevive es lo montado C3P1 1:19:26, C3P1 1:23:26.
- Para saber dónde escribe Spark, corré `%sh pwd` en Zeppelin: `/opt/zeppelin` en Docker, el home de jovyan en el CCAD C3P1 1:18:40.

**Cómo lo armé en el box, sin Docker** (sirve si querés correr los scripts de esta guía fuera de Zeppelin): bajé el JRE Temurin 17 como tarball, creé un venv aparte con `pip install pyspark==3.5.9 pandas pyarrow matplotlib setuptools numpy`, y antes de correr cargo estas variables:

```bash
export JAVA_HOME=/workspace/yt/jdk/jdk-17.0.20.1+1-jre
export PATH=$JAVA_HOME/bin:/workspace/yt/pd_venv/bin:$PATH
export PYSPARK_PYTHON=/workspace/yt/pd_venv/bin/python
export SPARK_LOCAL_IP=127.0.0.1
```

Dos tropiezos: con Python 3.13, `import pyspark.ml` falla con `ModuleNotFoundError: No module named 'distutils'` (PySpark 3.5 todavía lo importa); se arregla instalando `setuptools` en el venv. Y GraphFrames no viene con Spark: bajé el jar `graphframes-0.8.4-spark3.5-s_2.12.jar` de `repos.spark-packages.org`, que trae adentro el paquete Python (ver sección 11).

### 1. La sesión: driver, master y paralelismo
**En clase:** C2P1 24:18, C2P1 28:06, C2P1 31:09, C2P1 36:09, C2P2 7:19, C2P2 10:21

En Zeppelin la SparkSession y el SparkContext ya están creados; en un programa autónomo hay que crearlos C2P1 28:06. `local[*]` usa todos los núcleos como si fueran nodos; en un clúster cambiás solo el master (`spark://`, `yarn`, `k8s://`) C2P1 36:09.

```python
# g01_sesion.py
from pyspark.sql import SparkSession

spark = (SparkSession.builder.master("local[*]").appName("g01")
         .config("spark.ui.showConsoleProgress", "false").getOrCreate())
sc = spark.sparkContext
sc.setLogLevel("ERROR")
print("version:", spark.version)
print("master:", sc.master)
print("defaultParallelism:", sc.defaultParallelism)
print("mismo sc:", spark.sparkContext is sc)
spark.stop()
```

Lo que da en el box:
```text
version: 3.5.9
master: local[*]
defaultParallelism: 8
mismo sc: True
```

### 2. RDD: el word count, union e intersection
**En clase:** C1P2 27:08, C1P2 30:29, C1P2 33:15, C1P2 35:24, C1P2 42:15, C2P1 43:27, C2P1 48:33

El word count de la clase, aplicado a la presentación HTML del repo (el README que usa el docente es más chico). Después, dos filtros sobre el mismo archivo y su `union` y `intersection`, como el ejemplo de "error" y "config" de los logs de Zeppelin C2P1 43:27.

Qué tenés que hacer:
- Encadená transformaciones y terminá con una sola acción (`take`, `collect`, `count`).
- Preferí `take(n)` a `collect()` para mirar: `collect()` trae todo al driver C1P2 43:25, C2P1 50:14.
- Ojo que `union` no saca repetidos: una línea que tenga "spark" y "scala" aparece dos veces (acá la intersección es vacía, así que la unión da 9 + 4 = 13).

```python
# g02_rdd.py
from pyspark.sql import SparkSession

spark = (SparkSession.builder.master("local[*]").appName("g02")
         .config("spark.ui.showConsoleProgress", "false").getOrCreate())
sc = spark.sparkContext
sc.setLogLevel("ERROR")
TXT = "/workspace/yt/repo_pd/clases/00_introduccion/presentation.html"

# word count (C1P2): transformaciones y una sola accion al final
lines = sc.textFile(TXT)
counts = (lines.flatMap(lambda line: line.split(" "))
               .filter(lambda w: w)              # la cadena vacia es falsa
               .map(lambda w: (w, 1))
               .reduceByKey(lambda a, b: a + b))
print("particiones:", lines.getNumPartitions())
print("top 5:", counts.sortBy(lambda p: p[1], ascending=False).take(5))

# union e intersection (C2P1)
con_spark = lines.filter(lambda l: "spark" in l.lower())
con_scala = lines.filter(lambda l: "scala" in l.lower())
print("spark:", con_spark.count(), "scala:", con_scala.count(),
      "union:", con_spark.union(con_scala).count(),
      "intersection:", con_spark.intersection(con_scala).count())
spark.stop()
```

Lo que da en el box:
```text
particiones: 2
top 5: [('<div', 123), ('</div>', 121), ('de', 90), ('|', 59), ('</aside>', 58)]
spark: 9 scala: 4 union: 13 intersection: 0
```

### 3. Evaluación perezosa y cache, medidas
**En clase:** C2P1 1:14:19, C2P1 1:17:30, C2P1 1:33:17, C2P1 1:39:02, C2P1 1:40:05

El ejemplo de los cuadrados de la clase, con un acumulador que cuenta cuántas veces se ejecuta la función. Sin cache, `mean()` y `collect()` recalculan todo (60 evaluaciones para 30 números); con `.cache()`, la segunda acción lee lo guardado (30). También muestra que un `map` solo no lanza ningún job y que hay excepciones a la pereza: `reduceByKey` mira las particiones del RDD padre al definirse, así que un archivo inexistente falla en esa línea.

Qué tenés que hacer:
- Cacheá lo que vas a reutilizar, y ponele nombre con `setName` para encontrarlo en la pestaña Storage C2P1 1:40:05.
- Cuando algo falla "en la línea equivocada", acordate de la pereza: el error suele aparecer en la acción, no donde está el bug.

```python
# g03_lazy_cache.py
from pyspark.sql import SparkSession

spark = (SparkSession.builder.master("local[*]").appName("g03")
         .config("spark.ui.showConsoleProgress", "false").getOrCreate())
sc = spark.sparkContext
sc.setLogLevel("ERROR")
jobs = lambda: len(sc.statusTracker().getJobIdsForGroup())

# 1. una transformacion sola no lanza ningun job
antes = jobs()
sq = sc.parallelize(range(30)).map(lambda x: x * x)
print("jobs antes/despues del map:", antes, jobs())
sq.count()
print("jobs despues de count():", jobs())

# 2. dos acciones sin cache: la funcion corre dos veces por elemento
evals = sc.accumulator(0)
def cuad(x):
    evals.add(1)
    return x * x
sq = sc.parallelize(range(30)).map(cuad)
print("media:", sq.mean(), "| n:", len(sq.collect()), "| evaluaciones sin cache:", evals.value)

# 3. con cache: la segunda accion lee lo guardado
evals2 = sc.accumulator(0)
def cuad2(x):
    evals2.add(1)
    return x * x
sqc = sc.parallelize(range(30)).map(cuad2).cache().setName("cuadrados")
print("media:", sqc.mean(), "| n:", len(sqc.collect()), "| evaluaciones con cache:", evals2.value)
print("guardado en Storage:", [r.name() for r in sc._jsc.getPersistentRDDs().values()])

# 4. no todo es perezoso: reduceByKey mira las particiones del padre al definirse
try:
    sc.textFile("/no/existe.txt").map(lambda l: (l, 1)).reduceByKey(lambda a, b: a + b)
    print("reduceByKey se definio sin error")
except Exception as e:
    print("reduceByKey fallo al definirse:", type(e).__name__)
spark.stop()
```

Lo que da en el box:
```text
jobs antes/despues del map: 0 0
jobs despues de count(): 1
media: 285.1666666666667 | n: 30 | evaluaciones sin cache: 60
media: 285.1666666666667 | n: 30 | evaluaciones con cache: 30
guardado en Storage: ['cuadrados']
reduceByKey fallo al definirse: Py4JJavaError
```

### 4. flights.csv con la API de RDD
**En clase:** C2P1 1:45:17, C2P1 1:48:24, C2P1 1:50:09

La preparación que necesitás para los ejercicios de vuelos del notebook 02: sacar el encabezado, partir por comas, pasar de la numeración de columnas de la clase (desde 1) a índices de Python (desde 0) y detectar los "NA". El script no calcula los porcentajes ni el máximo, que son el ejercicio.

Qué tenés que hacer:
- Filtrá el encabezado comparando con `first()` y cacheá las filas partidas, porque vas a hacer varias cuentas.
- Antes de convertir a número, sacá los "NA" (en AirTime hay 1302).
- El total de vuelos es la cantidad de líneas menos el encabezado: son 100.000, no 10.000.

```python
# g04_flights_rdd.py
from pyspark.sql import SparkSession

spark = (SparkSession.builder.master("local[*]").appName("g04")
         .config("spark.ui.showConsoleProgress", "false").getOrCreate())
sc = spark.sparkContext
sc.setLogLevel("ERROR")

fl = sc.textFile("/workspace/yt/repo_pd/ds/flights.csv")
header = fl.first()
cols = header.split(",")
rows = fl.filter(lambda l: l != header).map(lambda l: l.split(",")).cache()
print("filas sin encabezado:", rows.count())
for n in (14, 22, 24):                      # numeracion desde 1, como en la clase
    print(f"columna {n} -> indice {n-1}: {cols[n-1]}")
print("valores 'NA' en AirTime:", rows.filter(lambda r: r[13] == "NA").count())
print("valores distintos de Cancelled:", sorted(rows.map(lambda r: r[21]).distinct().collect()))
spark.stop()
```

Lo que da en el box:
```text
filas sin encabezado: 100000
columna 14 -> indice 13: AirTime
columna 22 -> indice 21: Cancelled
columna 24 -> indice 23: Diverted
valores 'NA' en AirTime: 1302
valores distintos de Cancelled: ['0', '1']
```

### 5. Spark SQL y DataFrames: usuarios de Last.fm y people.json
**En clase:** C2P2 7:19, C2P2 13:07, C2P2 16:07, C2P2 24:10, C2P2 31:21, C2P2 32:27, C2P2 58:03, C2P2 1:02:00

La misma consulta, cantidad de usuarios por país, en SQL sobre una vista temporal y con la API de DataFrames; las dos dan lo mismo porque terminan en el mismo plan. Después, el JSON de personas de la documentación y el word count reescrito con `split` y `explode`.

Qué tenés que hacer:
- Usá `inferSchema` si querés tipos: sin esa opción, `age` es string.
- `createOrReplaceTempView` no copia datos: solo le pone nombre al DataFrame para usarlo desde SQL C2P2 24:10.
- Importá `pyspark.sql.functions` como `F` y escribí `F.count`, `F.desc`: te ahorrás el error de la función sin importar.
- En Zeppelin, `z.show(df)` te da tabla y gráficos; acá uso `show()` y `take()`.
- Ojo con los nulos: en el ranking por país, el tercer "país" es `None`, con 85 usuarios que no lo cargaron.

```python
# g05_sql.py
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = (SparkSession.builder.master("local[*]").appName("g05")
         .config("spark.ui.showConsoleProgress", "false").getOrCreate())
spark.sparkContext.setLogLevel("ERROR")
DS = "/workspace/yt/repo_pd/ds"

profiles = (spark.read.format("csv").option("delimiter", "\t").option("header", "true")
            .option("inferSchema", "true").load(f"{DS}/userid-profile.tsv"))
profiles.printSchema()
sin_infer = spark.read.option("delimiter", "\t").option("header", "true").csv(f"{DS}/userid-profile.tsv")
print("age sin inferSchema:", dict(sin_infer.dtypes)["age"], "| filas:", profiles.count())

# SQL
profiles.createOrReplaceTempView("users")
q = spark.sql("SELECT country, count(*) AS cantidad FROM users GROUP BY country ORDER BY cantidad DESC")
print("SQL:", [tuple(r) for r in q.take(4)])
# DataFrame
d = profiles.groupBy("country").agg(F.count("*").alias("cantidad")).orderBy(F.desc("cantidad"))
print("DF: ", [tuple(r) for r in d.take(4)])

# people.json (JSON Lines)
people = spark.read.json(f"{DS}/people.json")
people.selectExpr("name", "age + 1").show()
people.filter(people["age"] > 21).show()

# word count con DataFrames
txt = spark.read.text("/workspace/yt/repo_pd/clases/00_introduccion/presentation.html")
wc = (txt.select(F.explode(F.split("value", " ")).alias("palabra"))
         .filter(F.col("palabra") != "").groupBy("palabra").count().orderBy(F.desc("count")))
print("word count DF:", [tuple(r) for r in wc.take(3)])
spark.stop()
```

Lo que da en el box:
```text
root
 |-- id: string (nullable = true)
 |-- gender: string (nullable = true)
 |-- age: integer (nullable = true)
 |-- country: string (nullable = true)
 |-- registered: string (nullable = true)

age sin inferSchema: string | filas: 992
SQL: [('United States', 228), ('United Kingdom', 126), (None, 85), ('Poland', 50)]
DF:  [('United States', 228), ('United Kingdom', 126), (None, 85), ('Poland', 50)]
+-------+---------+
|   name|(age + 1)|
+-------+---------+
|Michael|     NULL|
|   Andy|       31|
| Justin|       20|
+-------+---------+

+---+----+
|age|name|
+---+----+
| 30|Andy|
+---+----+

word count DF: [('<div', 123), ('</div>', 121), ('de', 90)]
```

### 6. Vuelos con DataFrames: "NA", UDF, SQL y planes
**En clase:** C2P3 5:29, C3P1 9:20, C3P1 14:25, C3P1 17:18, C3P1 24:11, C3P1 29:16, C3P1 45:03, C3P1 49:03, C3P1 56:24, C3P1 1:07:10, C3P1 1:11:22, C2P3 3:11

Lo central del notebook 04, en orden: el problema de los "NA" al inferir tipos, la UDF `is_delayed` con su tipo de retorno, el porcentaje de demorados, la UDF registrada para SQL con las cuentas por empresa, el `CASE WHEN` por hora programada y la agregación por origen y destino. Al final, dos comprobaciones que en clase se cuentan pero no se miden: que la UDF de Python agrega un paso `BatchEvalPython` que la versión con `F.when` no tiene, y que dos `filter` seguidos quedan como un solo `Filter` en el plan optimizado (Catalyst los fusiona, la optimización de base de datos que nombra el docente C2P3 3:11).

Qué tenés que hacer:
- Leé con `.option("nullValue", "NA")`. Sin eso, `DepDelay` es string; el filtro `DepDelay > 15` igual da 19.587 porque Spark castea al comparar, pero la UDF recibe texto y falla con `TypeError: '>' not supported between instances of 'str' and 'int'`.
- En la UDF, contemplá el `None` (los vuelos cancelados no tienen demora).
- La UDF registrada con `spark.udf.register` vive en la sesión: si reiniciás el intérprete, volvé a registrarla o vas a ver "unresolved routine" C3P1 51:14.
- Para pasar de hhmm a hora, `CAST(CRSDepTime / 100 AS INT)` C3P1 1:07:10.
- Para ver un plan, `df.explain()` (o `df.explain("formatted")`); el script lo lee del objeto Java solo para contar nodos.

```python
# g06_flights_df.py
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import IntegerType

spark = (SparkSession.builder.master("local[*]").appName("g06")
         .config("spark.ui.showConsoleProgress", "false").getOrCreate())
spark.sparkContext.setLogLevel("ERROR")
CSV = "/workspace/yt/repo_pd/ds/flights.csv"
TIPOS = ("DepDelay", "ArrDelay", "AirTime")

# 1. el problema de "NA": sin nullValue esas columnas quedan como string
raw = spark.read.option("header", "true").option("inferSchema", "true").csv(CSV)
print("sin nullValue:", [(c, t) for c, t in raw.dtypes if c in TIPOS])
flights = (spark.read.option("header", "true").option("inferSchema", "true")
           .option("nullValue", "NA").csv(CSV))
print("con nullValue:", [(c, t) for c, t in flights.dtypes if c in TIPOS])
print("filas:", flights.count())

demorados = flights.filter(F.col("DepDelay") > 15).cache()
print("DepDelay > 15:", demorados.count())

# 2. UDF (C3P1)
def is_delayed(t):
    return 1 if t is not None and t > 15 else 0
is_delayed_udf = F.udf(is_delayed, IntegerType())
con_udf = flights.select("UniqueCarrier", is_delayed_udf(F.col("DepDelay")).alias("IsDepDelayed"))
pct = con_udf.agg((F.sum("IsDepDelayed") * 100 / F.count("*")).alias("pct")).first().asDict()["pct"]
print("porcentaje de demorados:", pct)

# 3. la UDF obliga a pasar por Python; la version nativa no
nativa = flights.select(F.when(F.col("DepDelay") > 15, 1).otherwise(0).alias("IsDepDelayed"))
plan = lambda df: df._jdf.queryExecution().executedPlan().toString()
print("plan con UDF tiene BatchEvalPython:", "BatchEvalPython" in plan(con_udf))
print("plan nativo tiene BatchEvalPython:", "BatchEvalPython" in plan(nativa))

# 4. SQL con UDF registrada
flights.createOrReplaceTempView("flightsTbl")
spark.udf.register("isDelayedTabUDF", is_delayed, IntegerType())
print("demorados en llegada por empresa:", [tuple(r) for r in spark.sql(
    "SELECT UniqueCarrier, SUM(isDelayedTabUDF(ArrDelay)) AS n FROM flightsTbl "
    "GROUP BY UniqueCarrier ORDER BY n DESC").collect()])
print("ArrDelay medio de los demorados:", [(r[0], round(r[1], 2)) for r in spark.sql(
    "SELECT UniqueCarrier, avg(ArrDelay) FROM flightsTbl WHERE isDelayedTabUDF(ArrDelay) = 1 "
    "GROUP BY UniqueCarrier ORDER BY UniqueCarrier").collect()])

# 5. CASE y hora programada (hhmm / 100)
print("hora 13:", [tuple(r) for r in spark.sql(
    "SELECT CAST(CRSDepTime / 100 AS INT) AS hora, "
    "CASE WHEN DepDelay > 15 THEN 'delayed' ELSE 'ok' END AS estado, count(*) AS n "
    "FROM flightsTbl GROUP BY hora, estado HAVING hora = 13 ORDER BY estado").collect()])

# 6. agregacion por dos claves
print("TaxiOut medio, top 2:", [tuple(r) for r in flights.groupBy("Origin", "Dest")
      .agg(F.avg("TaxiOut").alias("taxi")).orderBy(F.desc("taxi")).take(2)])

# 7. dos filter seguidos: Catalyst los junta en uno
demorados.unpersist()      # si no, el plan reutiliza el DataFrame cacheado
dos = flights.filter(F.col("DepDelay") > 15).filter(F.col("Origin") == "IAD")
qe = dos._jdf.queryExecution()
nodos = lambda p: sum(l.lstrip("+- :").startswith("Filter") for l in p.toString().splitlines())
print("nodos Filter: analizado", nodos(qe.analyzed()), "| optimizado", nodos(qe.optimizedPlan()))
spark.stop()
```

Lo que da en el box:
```text
sin nullValue: [('AirTime', 'string'), ('ArrDelay', 'string'), ('DepDelay', 'string')]
con nullValue: [('AirTime', 'int'), ('ArrDelay', 'int'), ('DepDelay', 'int')]
filas: 100000
DepDelay > 15: 19587
porcentaje de demorados: 19.587
plan con UDF tiene BatchEvalPython: True
plan nativo tiene BatchEvalPython: False
demorados en llegada por empresa: [('WN', 17753), ('XE', 1041)]
ArrDelay medio de los demorados: [('WN', 50.37), ('XE', 60.72)]
hora 13: [(13, 'delayed', 1346), (13, 'ok', 5225)]
TaxiOut medio, top 2: [('LCH', 'IAH', 84.0), ('EWR', 'BHM', 63.0)]
nodos Filter: analizado 2 | optimizado 1
```

Los números coinciden con los de clase: 19.587 demorados y 19,587% C3P1 24:11, WN con "17.000 y pico" demorados en llegada y XE con 1041 C3P1 49:03, unos 50 y 60 minutos de demora media C3P1 56:24 y, a las 13 h, 1346 demorados contra 5225 a tiempo C3P1 1:11:22.

### 7. Parquet, ORC, tablas permanentes y joins con broadcast
**En clase:** C2P2 44:04, C2P2 48:11, C2P2 51:09, C2P2 52:17, C3P1 1:12:36, C3P1 1:14:12, C3P1 1:24:14, C3P1 1:28:09, C3P1 1:30:25, C3P1 1:35:23

Qué se escribe cuando escribís: un directorio con un archivo `part` por partición (y no por núcleo, como se puede entender en clase). Después ORC con relectura, una tabla permanente en `spark-warehouse` frente a la vista temporal, `spark.table` para volver a DataFrame y el join de vuelos con el nombre de la empresa, con `broadcast` sobre la tabla chica.

Qué tenés que hacer:
- Elegí el modo de escritura: `error` es el defecto; para rehacer una celda usá `overwrite` C3P1 1:14:12.
- Si necesitás un solo archivo, `coalesce(1)`; si querés paralelismo al leer después, más particiones.
- Las tablas permanentes quedan en `spark-warehouse` dentro del directorio de trabajo: en Docker, montado o perdido según dónde esté (sección 0).
- En Spark 3, `spark.table("nombre")`; el `sqlContext.table` de clase anda por compatibilidad C3P1 1:27:01.
- Con `broadcast` la tabla chica viaja entera a cada nodo; usala solo si de verdad es chica.

```python
# g07_formatos_joins.py
import os, shutil
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

W = "/tmp/g07"
shutil.rmtree(W, ignore_errors=True); os.makedirs(W)
spark = (SparkSession.builder.master("local[*]").appName("g07")
         .config("spark.sql.warehouse.dir", f"{W}/spark-warehouse")
         .config("spark.ui.showConsoleProgress", "false").getOrCreate())
spark.sparkContext.setLogLevel("ERROR")
DS = "/workspace/yt/repo_pd/ds"

# Parquet: se escribe un directorio con un archivo por particion
profiles = spark.read.option("delimiter", "\t").option("header", "true").csv(f"{DS}/userid-profile.tsv")
profiles.write.mode("overwrite").save(f"{W}/profiles.parquet")
print("particiones:", profiles.rdd.getNumPartitions(),
      "| archivos part:", len([f for f in os.listdir(f"{W}/profiles.parquet") if f.startswith("part-")]))
profiles.repartition(4).write.mode("overwrite").save(f"{W}/profiles4.parquet")
print("con repartition(4), archivos part:",
      len([f for f in os.listdir(f"{W}/profiles4.parquet") if f.startswith("part-")]))

# ORC y relectura
flights = (spark.read.option("header", "true").option("inferSchema", "true")
           .option("nullValue", "NA").csv(f"{DS}/flights.csv"))
flights.write.format("orc").mode("overwrite").save(f"{W}/flights.orc")
print("ORC releido:", spark.read.format("orc").load(f"{W}/flights.orc").count())

# tabla permanente vs vista temporal
flights.write.saveAsTable("flightsPermTbl", format="orc", mode="overwrite")
profiles.createOrReplaceTempView("users")
print("tablas:", [(r.tableName, r.isTemporary) for r in spark.sql("SHOW TABLES").collect()])
print("spark.table:", spark.table("flightsPermTbl").count())

# join con broadcast de la tabla chica
carriers = spark.read.option("header", "true").csv(f"{DS}/carriers.csv")
j = (flights.join(F.broadcast(carriers), flights.UniqueCarrier == carriers.Code)
            .withColumnRenamed("Description", "CarrierName"))
print("join:", [tuple(r) for r in j.groupBy("CarrierName").count().orderBy(F.desc("count")).collect()])
print("BroadcastHashJoin en el plan:", "BroadcastHashJoin" in j._jdf.queryExecution().executedPlan().toString())
spark.stop()
```

Lo que da en el box:
```text
particiones: 1 | archivos part: 1
con repartition(4), archivos part: 4
ORC releido: 100000
tablas: [('flightspermtbl', False), ('users', True)]
spark.table: 100000
join: [('Southwest Airlines Co.', 94055), ('Expressjet Airlines Inc.', 5945)]
BroadcastHashJoin en el plan: True
```

### 8. MLlib con el dataset de personas
**En clase:** C3P2 17:06, C3P2 22:01, C3P2 25:23, C3P2 30:04, C3P2 37:21, C3P2 58:11, C3P2 1:00:25, C3P3 5:03, C3P3 8:30, C3P3 10:07, C3P3 15:21, C3P3 18:10, C3P3 25:28

El recorrido de las clases 3 y 4 sobre `people_sex_height_age_weight.json`: leer y reparticionar, separar train y test, armar `features` con VectorAssembler, codificar el sexo con StringIndexer y entrenar árbol, random forest, regresión logística y LinearSVC. En clase la evaluación es visual, con la grilla y los gráficos; acá agrego exactitud y AUC en test para tener un número. Cierra con la expansión polinomial: cuántas features genera por grado y un LinearSVC con grado 4.

Qué tenés que hacer:
- `repartition(sc.defaultParallelism)` después de leer: el JSON llega en 1 partición C3P2 22:01.
- Fijá la semilla del `randomSplit`. Igual, el split exacto depende también del particionado: a mí me dio 9492 y 508 y en clase 9532 y 468 C3P2 25:23.
- StringIndexer: `fit` y después `transform`. Con `stringOrderType="alphabetDesc"` queda M = 0 y F = 1, así que la probabilidad de la clase 1 es la de ser mujer.
- Para las probabilidades, la columna `probability` es un vector: extraé el elemento 1 con `pyspark.ml.functions.vector_to_array` C3P3 11:11.
- PolynomialExpansion no tiene `fit`: es un Transformer. Aplicala igual al train, al test y a cualquier grilla que quieras graficar C3P3 24:19.
- Con dos variables, grado 2 da 5 features, grado 3 da 9 y grado 4 da 14 (no 12 como se dice en clase C3P3 25:28).
- Si querés los gráficos de clase fuera de Zeppelin, convertí a pandas una muestra (`sample` o `limit`) antes de `toPandas()` C3P2 49:16.

```python
# g08_ml.py
from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler, StringIndexer, PolynomialExpansion
from pyspark.ml.classification import (DecisionTreeClassifier, RandomForestClassifier,
                                       LogisticRegression, LinearSVC)
from pyspark.ml.evaluation import MulticlassClassificationEvaluator, BinaryClassificationEvaluator
from pyspark.ml.functions import vector_to_array

spark = (SparkSession.builder.master("local[*]").appName("g08")
         .config("spark.ui.showConsoleProgress", "false").getOrCreate())
sc = spark.sparkContext
sc.setLogLevel("ERROR")

raw = spark.read.json("/workspace/yt/repo_pd/ds/people_sex_height_age_weight.json").select("kgs", "mts", "sex")
print("particiones al leer:", raw.rdd.getNumPartitions())
people = raw.repartition(sc.defaultParallelism).cache()
print("filas:", people.count(), "| particiones:", people.rdd.getNumPartitions())
train, test = people.randomSplit([0.95, 0.05], seed=12345)
print("train/test:", train.count(), test.count())

assembler = VectorAssembler(inputCols=["kgs", "mts"], outputCol="features")   # Transformer
indexer = StringIndexer(inputCol="sex", outputCol="label", stringOrderType="alphabetDesc")  # Estimator
sex_indexer = indexer.fit(train)
print(type(indexer).__name__, "->", type(sex_indexer).__name__, "| labels:", sex_indexer.labels)
tr = sex_indexer.transform(assembler.transform(train))
te = sex_indexer.transform(assembler.transform(test))

acc = MulticlassClassificationEvaluator(metricName="accuracy")
auc = BinaryClassificationEvaluator(metricName="areaUnderROC")
def evalua(nombre, est, a=tr, b=te):
    m = est.fit(a)
    p = m.transform(b)
    print(f"{nombre:16s} acc test {acc.evaluate(p):.3f}  AUC test {auc.evaluate(p):.3f}")
    return m

print("maxDepth por defecto:", DecisionTreeClassifier().getOrDefault("maxDepth"))
evalua("arbol", DecisionTreeClassifier(featuresCol="features", labelCol="label"))
evalua("random forest", RandomForestClassifier(numTrees=20))
lr = evalua("logistica", LogisticRegression())
evalua("LinearSVC", LinearSVC())

# probabilidad de "F" (label 1) para dos personas
nuevos = assembler.transform(spark.createDataFrame([(95.0, 1.70), (60.0, 1.50)], ["kgs", "mts"]))
print("P(mujer):", [round(r.p, 3) for r in
      lr.transform(nuevos).select(vector_to_array("probability")[1].alias("p")).collect()])

# expansion polinomial: es un Transformer, no tiene fit
for g in (2, 3, 4):
    pe = PolynomialExpansion(degree=g, inputCol="features", outputCol="poly")
    n = len(pe.transform(tr).first()["poly"])
    print(f"grado {g}: {n} features | tiene fit: {hasattr(pe, 'fit')}")
pe = PolynomialExpansion(degree=4, inputCol="features", outputCol="poly")
evalua("SVC poly grado 4", LinearSVC(featuresCol="poly"), pe.transform(tr), pe.transform(te))
spark.stop()
```

Lo que da en el box:
```text
particiones al leer: 1
filas: 10000 | particiones: 8
train/test: 9492 508
StringIndexer -> StringIndexerModel | labels: ['M', 'F']
maxDepth por defecto: 5
arbol            acc test 0.750  AUC test 0.562
random forest    acc test 0.752  AUC test 0.825
logistica        acc test 0.726  AUC test 0.807
LinearSVC        acc test 0.730  AUC test 0.809
P(mujer): [0.462, 0.978]
grado 2: 5 features | tiene fit: False
grado 3: 9 features | tiene fit: False
grado 4: 14 features | tiene fit: False
SVC poly grado 4 acc test 0.754  AUC test 0.817
```

Cómo leerlo: todos los modelos rondan 0,73 a 0,75 de exactitud, el techo que anticipa el docente cuando muestra que peso y altura no separan bien los sexos C3P2 54:14. El AUC bajo del árbol (0,56) no quiere decir que clasifique mal: sus probabilidades salen de pocas hojas y casi no ordenan; la exactitud es la misma que la del bosque. La logística da 46% de ser mujer para 95 kg y 1,70 m (en clase, 44% C3P3 10:07) y 98% para 60 kg y 1,50 m, que el árbol de clase también da como femenino C3P2 1:02:02.

### 9. Pipelines y texto: Tokenizer, HashingTF y regresión logística
**En clase:** C4P1 10:28, C4P1 16:15, C4P1 20:09, C4P1 25:06, C4P1 29:04, C4P1 31:17, C4P1 35:10, C4P1 42:32, C4P1 47:12, C4P1 51:16

El ejemplo de juguete del notebook 06 (documentos que hablan o no de Spark) en su versión de Pipeline: `Tokenizer`, `HashingTF(numFeatures=1000)` y `LogisticRegression(maxIter=10, regParam=0.001)` en una lista de etapas, un solo `fit` con el texto crudo y un `transform` con el test crudo. Después guarda el `PipelineModel`, lo recarga y compara predicciones. Al final mide cuántas colisiones produce el hashing con el vocabulario de la presentación del curso.

Qué tenés que hacer:
- Armá el Pipeline con instancias nuevas o reutilizadas, pero en orden: cada etapa lee la columna de salida de la anterior (`tokenizer.getOutputCol()`) C4P1 45:23.
- `pipeline.fit(train)` devuelve un `PipelineModel` y ese modelo es el que transforma; el Pipeline sin entrenar no predice.
- Guardá con `model.write().overwrite().save(ruta)` y cargá con `PipelineModel.load(ruta)` C4P1 51:16.
- Subí `numFeatures` (el defecto es 2^18): con 1000, 458 de 1126 palabras comparten posición con otra.
- No esperes las mismas predicciones de clase: con los datos del repo 2019 solo la última frase da 1 (ver abajo).

```python
# g09_pipeline_texto.py
import shutil
from pyspark.sql import SparkSession
from pyspark.ml import Pipeline, PipelineModel
from pyspark.ml.feature import Tokenizer, HashingTF
from pyspark.ml.classification import LogisticRegression

spark = (SparkSession.builder.master("local[*]").appName("g09")
         .config("spark.ui.showConsoleProgress", "false").getOrCreate())
spark.sparkContext.setLogLevel("ERROR")

# datos de juguete del notebook del curso (version 2019)
training = spark.createDataFrame([
    (0, "a b c d e spark a", 1.0), (1, "b d", 0.0),
    (2, "spark f g h", 1.0), (3, "hadoop a mapreduce", 0.0)], ["id", "text", "label"])
test = spark.createDataFrame([
    (4, "spark i j k"), (5, "l m n"), (6, "mapreduce spark"),
    (7, "apache hadoop"), (8, "spark f j k")], ["id", "text"])

tokenizer = Tokenizer(inputCol="text", outputCol="words")
hashingTF = HashingTF(numFeatures=1000, inputCol=tokenizer.getOutputCol(), outputCol="features")
lr = LogisticRegression(maxIter=10, regParam=0.001)

print("indice de 'a':", hashingTF.indexOf("a"))
print("vector de la fila 0:", hashingTF.transform(tokenizer.transform(training)).first()["features"])

pipeline = Pipeline(stages=[tokenizer, hashingTF, lr])      # Estimator
model = pipeline.fit(training)                               # PipelineModel (Transformer)
print("etapas:", [type(s).__name__ for s in model.stages])
pred = model.transform(test)                                 # test crudo, sin featurizar a mano
for r in pred.select("text", "probability", "prediction").collect():
    print(f"{r.text:18s} P(1)={r.probability[1]:.3f} pred={r.prediction}")

shutil.rmtree("/tmp/spark-model", ignore_errors=True)
model.write().overwrite().save("/tmp/spark-model")
again = PipelineModel.load("/tmp/spark-model")
print("recargado, mismas predicciones:",
      again.transform(test).select("prediction").collect() == pred.select("prediction").collect())

# colisiones del hashing trick segun numFeatures
palabras = {w for w in open("/workspace/yt/repo_pd/clases/00_introduccion/presentation.html").read().split()}
for nf in (1000, 2 ** 18):
    h = HashingTF(numFeatures=nf)
    pos = {h.indexOf(w) for w in palabras}
    print(f"numFeatures={nf}: {len(palabras)} palabras en {len(pos)} posiciones, "
          f"{len(palabras) - len(pos)} colisionan")
spark.stop()
```

Lo que da en el box:
```text
indice de 'a': 467
vector de la fila 0: (1000,[165,286,467,550,768,890],[1.0,1.0,2.0,1.0,1.0,1.0])
etapas: ['Tokenizer', 'HashingTF', 'LogisticRegressionModel']
spark i j k        P(1)=0.324 pred=0.0
l m n              P(1)=0.011 pred=0.0
mapreduce spark    P(1)=0.095 pred=0.0
apache hadoop      P(1)=0.002 pred=0.0
spark f j k        P(1)=0.823 pred=1.0
recargado, mismas predicciones: True
numFeatures=1000: 1126 palabras en 668 posiciones, 458 colisionan
numFeatures=262144: 1126 palabras en 1118 posiciones, 8 colisionan
```

En clase dice que dan 1 la primera y la última frase, las que tienen "spark" C4P1 31:17, C4P1 34:05. Acá "spark i j k" da 0,32 y solo "spark f j k" pasa el umbral (0,82); es **para verificar** con el notebook 2026, que el docente modificó. Fijate que "mapreduce spark" también tiene "spark" y da 0,095: el modelo aprendió más de "f" y de las palabras de los documentos negativos que de "spark" sola, algo esperable con 6 documentos de entrenamiento.

### 10. Clustering con KMeans
**En clase:** C4P2 2:21, C4P2 4:08, C4P2 5:20, C4P2 11:29, C4P2 14:21

Las cinco nubes de 50 puntos en 3D de la clase, centradas en (0,0,0), (5,0,0), (0,5,0), (0,0,5) y (5,5,5), con desvío 1 y semilla fija; VectorAssembler, `KMeans(k=5)` y los centroides.

Qué tenés que hacer:
- Armá un DataFrame por nube y juntalos con `union` C4P2 5:20.
- `model.clusterCenters()` da los centroides en el orden de los números de cluster; para saber cuál es cuál, transformá también los centros o contá por `prediction`.
- Los números de cluster son arbitrarios: compará centroides con centros, no etiquetas con nubes.
- El gráfico 3D de clase usa plotly sobre `toPandas()`; con 250 puntos no hay problema, con millones muestreá C4P2 8:05.

```python
# g10_kmeans.py
import random
from pyspark.sql import SparkSession, Row
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.clustering import KMeans

spark = (SparkSession.builder.master("local[*]").appName("g10")
         .config("spark.ui.showConsoleProgress", "false").getOrCreate())
spark.sparkContext.setLogLevel("ERROR")

random.seed(1)
centros = [(0, 0, 0), (5, 0, 0), (0, 5, 0), (0, 0, 5), (5, 5, 5)]
nubes = [spark.createDataFrame([Row(x=cx + random.gauss(0, 1), y=cy + random.gauss(0, 1),
                                    z=cz + random.gauss(0, 1)) for _ in range(50)])
         for cx, cy, cz in centros]
df = nubes[0]
for n in nubes[1:]:
    df = df.union(n)
data = VectorAssembler(inputCols=["x", "y", "z"], outputCol="features").transform(df)
print("puntos:", data.count())

model = KMeans(k=5, featuresCol="features", predictionCol="prediction", seed=1).fit(data)
for i, c in enumerate(model.clusterCenters()):
    print("centroide", i, [round(float(v), 2) for v in c])
print("tamanios:", sorted(r["count"] for r in model.transform(data).groupBy("prediction").count().collect()))
spark.stop()
```

Lo que da en el box:
```text
puntos: 250
centroide 0 [-0.19, 5.14, -0.01]
centroide 1 [5.34, 0.2, 0.24]
centroide 2 [-0.45, 0.1, 4.96]
centroide 3 [-0.12, 0.19, -0.04]
centroide 4 [4.77, 4.97, 5.08]
tamanios: [49, 50, 50, 50, 51]
```

Los cinco centroides caen a menos de 0,5 de los centros reales y los grupos tienen entre 49 y 51 puntos: KMeans recupera las nubes casi sin errores.

### 11. Grafos con GraphFrames: grafo de juguete, Gephi y la red de retuits
**En clase:** C4P3 9:36, C4P3 14:01, C4P3 17:25, C4P3 19:06, C4P3 20:15, C4P3 24:17, C4P3 28:13, C4P3 38:08, C4P3 44:00, C4P3 46:09, C4P3 51:12, C4P3 52:21, C4P3 54:03, C4P3 1:01:22, C4P3 1:03:11, C4P3 1:14:07, C4P3 1:25:00, C4P3 1:29:23

Todo lo que se muestra del notebook 08: el grafo de Alice, Bob y compañía (con la arista a→h que agrega el notebook del curso), grados de entrada, filtro de aristas, PageRank, motif finding de pares mutuos y la exportación de aristas a un solo CSV para Gephi. Después la red de retuits: aristas `rt_by → user` con la cantidad de retuits, vértices como unión de src y dst, el top de grado, la influencia colectiva (CI) con `aggregateMessages` y el subgrafo de los nodos con CI de al menos 29 millones o grado de al menos 600.

Qué tenés que hacer:
- Fuera del contenedor del curso, GraphFrames no viene con Spark C4P3 9:36. Pasale el jar con `spark.jars` (o `--packages graphframes:graphframes:0.8.4-spark3.5-s_2.12` con acceso a internet) y poné el mismo jar en `sys.path`: adentro trae el paquete Python `graphframes`.
- Vértices con columna `id`, aristas con `src` y `dst`; los nombres son obligatorios.
- En GraphFrames 0.8.4 para Python no hay `GraphFrame.fromEdges`: armá los vértices como la unión de `src` y `dst` renombradas a `id`, con `distinct` C4P3 51:12.
- En el archivo del repo 2019 las columnas de `tweets.pqt` son `timestamp`, `user`, `RT_by`, `RT_times` y `text`; en 2026 el docente nombra `rt_by` y avisa que cambió el archivo C4P3 1:58:20. Mirá `printSchema()` antes de copiar código.
- La CI de cada nodo es (grado menos 1) por la suma, sobre sus vecinos, de (grado del vecino menos 1) C4P3 1:01:22. Con `aggregateMessages`, cada arista manda a cada punta el grado de la otra menos 1 y se suma con `F.sum(AM.msg)` C4P3 1:03:11.
- `coalesce(1)` solo para exportar resultados chicos a Gephi C4P3 28:13.
- En Zeppelin, para que Gephi vea el CSV, escribilo en una carpeta montada (sección 0).

```python
# g11_grafos.py
import sys, os, shutil
JAR = "/workspace/yt/jars/graphframes-0.8.4-spark3.5-s_2.12.jar"
sys.path.insert(0, JAR)                 # el jar trae tambien el paquete Python graphframes
from pyspark.sql import SparkSession, functions as F

spark = (SparkSession.builder.master("local[*]").appName("g11")
         .config("spark.jars", JAR).config("spark.sql.shuffle.partitions", "8")
         .config("spark.ui.showConsoleProgress", "false").getOrCreate())
spark.sparkContext.setLogLevel("ERROR")
from graphframes import GraphFrame
from graphframes.lib import AggregateMessages as AM

# 1. grafo chico del notebook (incluye la arista a->h a un vertice inexistente)
v = spark.createDataFrame([("a", "Alice", 34), ("b", "Bob", 36), ("c", "Charlie", 30), ("d", "David", 29),
                           ("e", "Esther", 32), ("f", "Fanny", 36), ("g", "Gabby", 60)], ["id", "name", "age"])
e = spark.createDataFrame([("a", "b", "friend"), ("b", "c", "follow"), ("c", "b", "follow"),
                           ("f", "c", "follow"), ("e", "f", "follow"), ("e", "d", "friend"),
                           ("d", "a", "friend"), ("a", "e", "friend"), ("a", "h", "friend")],
                          ["src", "dst", "relationship"])
g = GraphFrame(v, e)
print("inDegrees:", sorted((r.id, r.inDegree) for r in g.inDegrees.collect()))
print("aristas friend:", g.edges.filter("relationship = 'friend'").count())
pr = g.pageRank(resetProbability=0.15, maxIter=10)
print("pageRank:", [(r.id, round(r.pagerank, 2)) for r in pr.vertices.orderBy(F.desc("pagerank")).collect()])
m = g.find("(a)-[e]->(b); (b)-[e2]->(a)")
print("mutuos:", [(r.a.id, r.b.id) for r in m.collect()],
      "| con b.age > 30:", [(r.a.id, r.b.id) for r in m.filter("b.age > 30").collect()])

# 2. CSV para Gephi: coalesce(1) deja un solo archivo
out = "/tmp/g11_gephi"
shutil.rmtree(out, ignore_errors=True)
g.vertices.select("*", F.col("id").alias("Label")).coalesce(1).write.option("header", True).csv(f"{out}/v")
g.edges.select(F.col("src").alias("Source"), F.col("dst").alias("Target"), "relationship") \
       .coalesce(1).write.option("header", True).csv(f"{out}/e")
print("archivos de aristas:", [f for f in os.listdir(f"{out}/e") if f.endswith(".csv")].__len__())

# 3. red de retuits
tweets = spark.read.parquet("/workspace/yt/repo_pd/ds/tweets.pqt")
print("retuits:", tweets.count(), "| columnas:", tweets.columns)
edges = (tweets.groupBy("user", "RT_by").count()
               .select(F.col("RT_by").alias("src"), F.col("user").alias("dst"), "count").cache())
verts = edges.select(F.col("src").alias("id")).union(edges.select(F.col("dst").alias("id"))).distinct()
graph = GraphFrame(verts, edges)
print("vertices:", graph.vertices.count(), "| aristas:", graph.edges.count())
deg = graph.degrees.cache()
print("top 3 grado:", [(r.id, r.degree) for r in deg.orderBy(F.desc("degree")).take(3)])

# 4. influencia colectiva: CI(i) = (k_i - 1) * suma sobre vecinos de (k_j - 1)
dg = GraphFrame(deg, graph.edges)
suma = dg.aggregateMessages(F.sum(AM.msg).alias("sum_nd"),
                            sendToSrc=AM.dst["degree"] - 1,   # el src recibe el grado del dst
                            sendToDst=AM.src["degree"] - 1)   # y el dst el del src: no dirigido
ci = (suma.join(deg, "id")
          .select("id", "degree", ((F.col("degree") - 1) * F.col("sum_nd")).alias("ci"))
          .orderBy(F.desc("ci")).cache())
for i, r in enumerate(ci.take(10), 1):
    print(f"{i:2d} {r.id:16s} grado {r.degree:5d}  CI {r.ci:,}")

# 5. subgrafo de los mas influyentes para Gephi
tops = ci.filter((F.col("ci") >= 29000000) | (F.col("degree") >= 600))
e_tops = GraphFrame(tops, graph.edges).find("(a)-[e]->(b)").select("e.*")
print("subgrafo: vertices", tops.count(), "| aristas", e_tops.count())
spark.stop()
```

Lo que da en el box:
```text
inDegrees: [('a', 1), ('b', 2), ('c', 2), ('d', 1), ('e', 1), ('f', 1), ('h', 1)]
aristas friend: 5
pageRank: [('b', 2.7), ('c', 2.67), ('a', 0.45), ('e', 0.36), ('d', 0.33), ('f', 0.33), ('g', 0.17)]
mutuos: [('b', 'c'), ('c', 'b')] | con b.age > 30: [('c', 'b')]
archivos de aristas: 1
retuits: 172040 | columnas: ['timestamp', 'user', 'RT_by', 'RT_times', 'text']
vertices: 57138 | aristas: 152613
top 3 grado: [('Winston_Dunhill', 2325), ('fernandocarnota', 1745), ('santosjorgeh', 1657)]
 1 Winston_Dunhill  grado  2325  CI 71,551,312
 2 santosjorgeh     grado  1657  CI 57,822,552
 3 fernandocarnota  grado  1745  CI 55,026,688
 4 JorgeFavaloro    grado  1483  CI 45,848,634
 5 lanatoparatodos  grado  1529  CI 42,052,088
 6 elcoya1977       grado  1471  CI 37,856,910
 7 betovaldez       grado  1407  CI 33,925,374
 8 LaBelgrana       grado   606  CI 31,175,045
 9 fargosi          grado  1271  CI 30,129,480
10 RobiBaradel      grado  1483  CI 29,494,764
subgrafo: vertices 33 | aristas 35
```

Coincide con lo de clase: 5 aristas friend C4P3 20:15 (en la documentación de GraphFrames son 4, la quinta es la a→h), Bob y Charlie como los de mayor PageRank C4P3 38:08, unos 170.000 retuits C4P3 44:00, 152.613 aristas C4P3 52:21, un máximo de grado cercano a 2300 C4P3 54:03, LaBelgrana con grado 606 entre los de mayor CI C4P3 1:13:00 y el subgrafo de 33 nodos y 35 aristas C4P3 1:29:23.

### 12. Los ejercicios: qué piden y cómo controlarlos
**En clase:** C2P2 1:11:21, C3P1 40:32, C4P3 2:01:19, C4P3 2:03:01, C4P3 2:12:00

Los ejercicios son el examen: se corre el notebook completo, se completan las celdas de ejercicio, se exporta desde Zeppelin y se sube con el formulario de cada notebook, en grupos de 3 o 4. Por eso acá no hay soluciones: está qué pide cada uno, qué sección de esta guía lo prepara y, cuando hay, un número de control.

| Notebook | Qué pide | Lo prepara | Control |
|---|---|---|---|
| 01 | Contar letras en vez de palabras cambiando solo el `flatMap`; con `links_raw.txt`, cuántos links apuntan a cada página C1P2 1:00:27, C1P2 1:02:14 | Sección 2 | `links_raw.txt` tiene 5027 líneas |
| 02 | Contar la letra "c" en los logs; líneas con INFO, WARN y ERROR con cache donde convenga; con `flights.csv` y RDD, porcentaje de cancelados (columna 22) y desviados (24) y máximo de AirTime (14) sin "NA" C2P1 1:27:18, C2P1 1:43:03, C2P1 1:48:24 | Secciones 2, 3 y 4 | 100.000 vuelos; 1302 "NA" en AirTime; Cancelled solo vale 0 o 1 |
| 03 | Usuarios por país y género en SQL y en DataFrame; edad promedio por género como tabla y como Parquet; registraciones por día de la semana C2P2 41:18, C2P2 56:20, C2P2 1:10:09 | Secciones 5 y 7 | Las fechas de `registered` tienen la forma "Aug 13, 2006" (patrón `MMM d, yyyy`); 8 filas vienen vacías |
| 04 | TaxiIn medio por origen y destino; distancia media por empresa; vuelos por aeropuerto de origen en una tabla permanente; join con `airports.csv` para origen y destino C3P1 39:24, C3P1 1:02:04, C3P1 1:27:01, C3P1 1:37:03 | Secciones 6 y 7 | Los totales por empresa tienen que sumar 100.000 (WN 94.055 y XE 5945) |
| 05 | Árbol con `maxDepth=10` y su gráfico; expansión de grado 3 con regresión logística (el título dice SVM pero el código usa LogisticRegression) C3P2 1:17:18, C3P3 28:19 | Sección 8 | Grado 3 con dos variables da 9 features; la exactitud no debería salir del rango 0,73 a 0,77 |
| 06 | Rehacer el ejemplo de personas como Pipeline con VectorAssembler, StringIndexer y un clasificador; se predice el sexo, no la edad como se dice en clase C4P1 54:08, C4P1 55:15 | Secciones 8 y 9 | El `PipelineModel` tiene que contener un `StringIndexerModel` ajustado |
| 05, parte final | Lo mismo que KMeans con `BisectingKMeans`; el clustering es la última parte del notebook 05 C4P2 0:06, C4P2 18:16 (el notebook 07, de búsqueda de hiperparámetros, no se entrega C4P2 22:24) | Sección 10 | Tiene que recuperar las cinco nubes |
| 08, ejercicio 1 | Grafo de todas las conexiones desde los 8 de mayor CI y su imagen desde la pestaña Preview de Gephi C4P3 1:49:24, C4P3 1:55:18 | Sección 11 | 120 vértices y 122 aristas, con la dirección `rt_by → user`; si te dan 9 aristas, armaste el grafo solo con los top como vértices |
| 08, ejercicio 2 | Triángulos dirigidos A→B→C→A con tres usuarios distintos, graficados en Gephi C4P3 1:56:22, C4P3 1:59:03 | Sección 11 (motif finding) | 415 vértices y 1006 aristas (en clase se oye "100"; un grafo hecho de triángulos no puede tener menos aristas que vértices) |

Los controles de los ejercicios del notebook 08 los verifiqué en el box con un script aparte que no incluyo, por la razón de arriba.

### 13. Problemas que me encontré y cómo los resolví
- **`TypeError: '>' not supported between instances of 'str' and 'int'`** en la UDF de demoras: `inferSchema` deja como string las columnas con "NA". Solución: `.option("nullValue", "NA")` (sección 6).
- **`ModuleNotFoundError: No module named 'distutils'`** al importar `pyspark.ml` con Python 3.13: instalé `setuptools` en el venv. En el contenedor del curso depende de la versión de Python que traiga (**para verificar**).
- **`AttributeError` con `GraphFrame.fromEdges`**: no existe en el paquete Python 0.8.4; vértices con `union` y `distinct` (sección 11).
- **Contar nodos de un plan**: si el DataFrame base está cacheado, el plan optimizado reutiliza el `InMemoryRelation` y aparecen nodos del plan cacheado; para mirar qué hace Catalyst con una consulta, `unpersist()` antes o usá `explain()` sobre un DataFrame sin cache (sección 6).
- **El split de train y test no da lo mismo que en clase** aunque uses la misma semilla: depende del particionado. No es un error (sección 8).

**Cómo corrí todo:** cada script es autónomo y se corre con `source pd_env.sh && python gNN_....py`; `run_all.sh` corre los once y guarda la salida en `out/`. Todos terminan con código 0 en el box, el 7 de octubre de 2026.
