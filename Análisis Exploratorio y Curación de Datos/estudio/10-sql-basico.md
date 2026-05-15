# 10 — SQL básico (lo que cubre la cátedra)

## Concepto

**SQL** (*Structured Query Language*) es el idioma con el que se le piden datos a una base de datos relacional. Lo aprendés una vez y te sirve para Postgres, MySQL, SQLite, Oracle, SQL Server, BigQuery, Snowflake, Redshift y casi cualquier otro motor — la sintaxis básica es la misma, los dialectos varían en los bordes.

La cátedra usa **SQLite** porque es *"la DB más desplegada (celulares, Skype, iTunes, TVs, autos)"* y porque no requiere instalar ningún servidor: la base es un solo archivo `.sqlite3`. Es ideal para aprender sin pelearte con la infraestructura.

> **Aviso temprano (importante)**: esta materia cubre SQL básico. **NO se ven** *window functions* (`OVER`, `PARTITION BY`, `LAG`, `LEAD`, `RANK`), **NO se ven** *CTEs* (`WITH`), **NO se ven** subconsultas anidadas (subqueries dentro de `SELECT` o `FROM`). Son temas centrales en SQL real y están fuera del alcance — vas a tener que estudiarlos por afuera (referencias al final).

## Intuición

Pedir datos en SQL es como **pedir comida en un restaurante**. La carta tiene la sintaxis pre-impresa y vos completás los huecos:

- `SELECT` → "Quiero (lomito completo, papas)"
- `FROM` → "del menú (del kiosko de la esquina)"
- `WHERE` → "con (pan sin tomate, papas con cheddar)"
- `GROUP BY` → "agrupame por (tipo de plato)"
- `HAVING` → "y mostrame solo los grupos donde (haya pedido más de 5)"
- `ORDER BY` → "ordenamelo por (precio descendente)"
- `LIMIT` → "y traeme los primeros (10)"

El mozo (el motor SQL) toma el pedido, va a la cocina (la base) y vuelve con lo que pediste. Si pediste algo imposible (campo que no existe, comparación entre número y string), te corrige.

---

## Por qué SQLite

- **Embebido**: la base es un archivo. No hay servidor, no hay puerto, no hay usuarios.
- **Ubicuo**: está en tu celular (WhatsApp, Telegram), en tu navegador (cookies, localStorage), en aplicaciones de escritorio, en autos.
- **Compatible**: la mayor parte de la sintaxis SQL estándar funciona.
- **Ideal para aprender**: el costo de equivocarte es cero. Borrás el archivo y empezás de nuevo.
- **Recurso oficial**: la cátedra recomienda `sqlitetutorial.net/tryit/` para practicar online, y la base **Chinook** (tracks, albums, artists, customers, invoices, employees, playlists) para tener algo real con joins entre 7 tablas.

---

## Sintaxis general (el orden de las cláusulas)

El esqueleto completo es éste. **El orden importa**: si invertís cláusulas, el motor tira error.

```sql
SELECT DISTINCT column_list
FROM table_list
JOIN table ON join_condition
WHERE row_filter
GROUP BY column
HAVING group_filter
ORDER BY column
LIMIT count OFFSET offset;
```

Una regla pedagógica importante: **el orden de escritura no es el orden de ejecución**. SQL escribe `SELECT` primero, pero el motor lo evalúa casi último. El orden lógico de ejecución es aproximadamente:

`FROM → JOIN → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT`.

Saber esto explica por qué un alias de `SELECT` no se puede usar en `WHERE` pero sí en `ORDER BY`.

---

## Cláusulas, una por una (con ejemplos del notebook sysarmy)

La base de ejemplos es la encuesta **sysarmy 2020** (~6.000 respondedores, ~48 columnas) cargada en una tabla `survey`.

### SELECT y FROM
Eligen qué columnas devolver y de qué tabla.

```sql
SELECT * FROM survey;
SELECT profile_gender, salary_monthly_NETO FROM survey;
```

`*` devuelve todas las columnas. En queries productivas, **evitá `*`**: nombrar las columnas explícitamente hace tu código resiliente a cambios de esquema y le dice al motor qué optimizar.

### DISTINCT
Quita duplicados del resultado.

```sql
SELECT DISTINCT work_province FROM survey;
```

Te devuelve las provincias únicas, sin repetir.

### WHERE (filtro a nivel fila, antes de agrupar)
Filtra filas que cumplen una condición.

```sql
SELECT * FROM survey
WHERE salary_monthly_NETO > 100000
LIMIT 10;
```

**Operadores típicos**:

| Operador | Significa | Ejemplo |
|---|---|---|
| `=` | Igual | `gender = 'Mujer'` |
| `<>` (o `!=`) | Distinto | `gender <> 'Mujer'` |
| `<`, `>`, `<=`, `>=` | Comparaciones numéricas y de fecha | `salary > 100000` |
| `IN (...)` | Pertenece a una lista | `province IN ('CABA', 'Buenos Aires')` |
| `BETWEEN a AND b` | Está en el rango (inclusivo) | `salary BETWEEN 100000 AND 500000` |
| `LIKE`  | Coincide con un patrón (`%` cualquier cosa, `_` un caracter) | `name LIKE 'Mar%'` |
| `IS NULL` / `IS NOT NULL` | Vacío o no | `salary IS NOT NULL` |
| `AND`, `OR`, `NOT` | Combinaciones lógicas | `gender = 'M' AND salary > 100000` |

**Trampa con strings**: los valores de texto van entre comillas simples: `'Mujer'`. Las comillas dobles muchas veces se usan para nombres de columna, no para valores.

### ORDER BY
Ordena el resultado. Por defecto ascendente (`ASC`), pero podés forzar descendente con `DESC`.

```sql
SELECT * FROM survey
ORDER BY salary_monthly_NETO DESC
LIMIT 5;
```

Top 5 mejor pagos. Podés ordenar por múltiples columnas: `ORDER BY province ASC, salary DESC`.

### LIMIT y OFFSET
`LIMIT n` trae solo las primeras n filas. `OFFSET k` saltea las primeras k.

```sql
SELECT * FROM survey LIMIT 10 OFFSET 20;
```

Trae filas 21 a 30. Útil para paginar resultados.

### GROUP BY (agrupar para agregar)
Junta filas que comparten un valor en una o más columnas, y deja que las funciones de agregación operen sobre cada grupo.

```sql
SELECT profile_gender, AVG(salary_monthly_NETO)
FROM survey
GROUP BY profile_gender;
```

Te da el sueldo promedio por género. Una fila por cada valor único de `profile_gender`.

**Regla de oro**: si en el `SELECT` aparece una columna que no está dentro de una función de agregación, esa columna **tiene que** estar en el `GROUP BY`. Si no, error o resultados sin sentido (varía según el motor).

### HAVING (filtro DESPUÉS de agrupar)
Filtra grupos enteros según el resultado de una agregación.

```sql
SELECT profile_gender, AVG(salary_monthly_NETO) AS avg_salary, COUNT(1) AS n
FROM survey
GROUP BY profile_gender
HAVING COUNT(*) > 100;
```

Solo muestra géneros que aparecen más de 100 veces. **`HAVING` se aplica sobre el resultado de la agregación**; `WHERE` se aplica antes de agrupar, sobre cada fila individual. Esa diferencia es la que más confunde a quien arranca.

---

## WHERE vs HAVING (la diferencia clave)

Es la confusión más típica. La regla:

- **`WHERE`** filtra **filas individuales** antes de agrupar.
- **`HAVING`** filtra **grupos enteros** después de agrupar.

Ejemplo combinado:

```sql
SELECT profile_gender, work_province,
       AVG(salary_monthly_NETO) AS avg_salary,
       COUNT(1) AS n
FROM survey
WHERE profile_years_experience > 5    -- filtra filas: solo gente con >5 años
GROUP BY profile_gender, work_province
HAVING COUNT(*) > 10                  -- filtra grupos: solo combinaciones con >10 personas
ORDER BY AVG(salary_monthly_NETO) DESC;
```

Lectura mental: *"Primero quedate con la gente que tiene más de 5 años de experiencia. Después agrupá por género y provincia. De esos grupos, mostrame solo los que tienen más de 10 personas, ordenados por sueldo promedio descendente."*

Si pusieras `COUNT(*) > 10` en el `WHERE`, el motor tira error: en el momento del `WHERE` los grupos todavía no existen.

---

## Funciones de agregación

Operan sobre un conjunto de filas (típicamente un grupo creado por `GROUP BY`) y devuelven un solo valor.

| Función | Qué hace |
|---|---|
| `COUNT(*)` | Cuenta filas (incluye NULL). |
| `COUNT(col)` | Cuenta filas donde `col` NO es NULL. |
| `COUNT(DISTINCT col)` | Cuenta valores únicos no nulos. |
| `SUM(col)` | Suma. |
| `AVG(col)` | Promedio (saltea NULL). |
| `MIN(col)` | Mínimo. |
| `MAX(col)` | Máximo. |

**Cuidado con `AVG` y NULL**: `AVG` ignora los NULL. Si la mitad de tu columna está vacía y no lo sabés, el promedio se calcula solo sobre la otra mitad. Validá siempre con un `COUNT(col)` paralelo.

---

## JOIN: combinar tablas (6 tipos)

Cuando los datos están en varias tablas, los traés juntos con un `JOIN` indicando la condición de unión con `ON`.

### Ejemplo de la cátedra (Chinook)
```sql
SELECT title, name
FROM albums
INNER JOIN artists ON artists.artistId = albums.artistId;
```

Te trae el título del álbum y el nombre del artista, uniendo las tablas `albums` y `artists` por su clave `artistId`.

### Los 6 tipos

| Tipo | Qué devuelve | Cuándo usarlo |
|---|---|---|
| **INNER JOIN** (default) | Solo filas que matchean en AMBAS tablas. | El caso más común — querés intersección. |
| **LEFT JOIN** | Todas las filas de la izquierda + las que matchean de la derecha (NULL si no hay match). | Querés conservar todo lo de A aunque no tenga par en B. |
| **RIGHT JOIN** | Todas las filas de la derecha + las que matchean de la izquierda. | Espejo del LEFT. Rara vez se usa: invertís las tablas y usás LEFT. SQLite hasta hace poco no lo soportaba. |
| **FULL OUTER JOIN** | Todas las filas de ambas, NULL donde no hay match. | Querés ver todo lo que existe en cualquiera de las dos. SQLite reciente lo soporta. |
| **CROSS JOIN** | Producto cartesiano (cada fila de A con cada fila de B). | Generar todas las combinaciones — peligroso, explota rápido. |
| **SELF JOIN** | Tabla unida consigo misma. | Jerarquías: empleado → jefe en la misma tabla. |

**Regla**: si no especificás el tipo, `JOIN` en SQLite y Postgres equivale a `INNER JOIN`. Pero **siempre escribilo explícito** — la próxima persona que lea tu código (incluyéndote a vos en 3 meses) lo agradece.

**Trampa habitual**: si te olvidás el `ON`, en algunos motores te tira error y en otros te hace un producto cartesiano que tarda media hora y devuelve millones de filas que no tienen sentido. Si no especificás `on=` en `merge` de pandas, usa intersección de columnas con el mismo nombre y eso también es confuso.

---

## Lo que NO cubre la cátedra (gap a estudiar fuera)

Para ser claros: esto no es tema de parcial, pero **lo vas a necesitar en cualquier laburo de datos real**. Estudialo por afuera.

### 1. Window functions (`OVER`, `PARTITION BY`)
Permiten calcular cosas tipo "ranking dentro de cada grupo" sin perder las filas originales. Ejemplo: top 3 sueldos por provincia conservando todas las columnas.

```sql
-- Esto NO se cubre. Lo vas a ver en SQL Cookbook.
SELECT *,
       RANK() OVER (PARTITION BY province ORDER BY salary DESC) AS rk
FROM survey;
```

### 2. CTEs (Common Table Expressions, `WITH`)
Te permiten "darle nombre" a una subquery para reutilizarla y hacer queries legibles.

```sql
-- Esto NO se cubre.
WITH alto_salario AS (
  SELECT * FROM survey WHERE salary_monthly_NETO > 200000
)
SELECT province, COUNT(*) FROM alto_salario GROUP BY province;
```

### 3. Subqueries anidadas
Un `SELECT` dentro de otro `SELECT`, en `FROM`, `WHERE`, o `SELECT`.

```sql
-- Esto NO se cubre.
SELECT * FROM survey
WHERE salary_monthly_NETO > (SELECT AVG(salary_monthly_NETO) FROM survey);
```

**Dónde estudiarlo**:
- **SQL Cookbook** (Molinaro & de Graaf, 2ed, O'Reilly) — bibliografía oficial de la materia. Los capítulos sobre windows y subqueries son obligados.
- **sqlitetutorial.net** — tiene secciones específicas de window functions y CTEs con ejemplos sobre Chinook.
- **Practicá con LeetCode SQL** o **HackerRank SQL** si querés ejercicios resueltos.

---

## Integración con Python (SQLAlchemy + SQLite)

En la práctica casi nunca abrís una shell de SQLite y tipeás queries a mano. Las disparás desde Python.

### Setup base
```python
from sqlalchemy import create_engine, text
import pandas as pd

# Crear/conectar a la base (es un archivo)
engine = create_engine("sqlite:///sysarmy.sqlite3", echo=False)

# Cargar un DataFrame como tabla
df = pd.read_csv("sysarmy_survey_2020_processed.csv")
df.to_sql("survey", con=engine, if_exists="replace")
```

### Patrón A — `pd.read_sql` (lo más simple)
Cuando querés que el resultado vuelva directo como DataFrame.

```python
query1 = "SELECT * FROM survey WHERE salary_monthly_NETO > 100000 LIMIT 10"
result = pd.read_sql(query1, con=engine)
```

`result` ya es un DataFrame listo para `.head()`, `.describe()`, lo que quieras.

### Patrón B — `engine.connect()` + `text()` (más control)
Cuando necesitás ejecutar varios statements, transacciones, o cuando el resultado no es tabular (un UPDATE, un DDL).

```python
with engine.connect() as con:
    rs = con.execute(text(query1))
    df_rs = pd.DataFrame(rs.fetchall())
```

El `with` cierra la conexión automáticamente al salir. `text()` envuelve el string SQL para que SQLAlchemy lo trate como query parametrizable (protección contra SQL injection si pasás parámetros).

---

## Pandas vs SQL — tabla de equivalencias

Para que cuando pienses una operación, sepas traducir entre los dos mundos.

| Operación | SQL | Pandas |
|---|---|---|
| Seleccionar columnas | `SELECT col1, col2 FROM t` | `df[['col1', 'col2']]` |
| Filtrar filas | `WHERE col > 10` | `df[df['col'] > 10]` |
| Agrupar y agregar | `GROUP BY col` + `AVG(...)` | `df.groupby('col').mean()` |
| Unir tablas | `JOIN ... ON ...` | `pd.merge(df1, df2, on='col')` |
| Ordenar | `ORDER BY col DESC` | `df.sort_values('col', ascending=False)` |
| Primeras N filas | `LIMIT n` | `df.head(n)` |
| Únicos | `SELECT DISTINCT col` | `df['col'].unique()` |
| Conteo total | `SELECT COUNT(*) FROM t` | `len(df)` |
| Conteo por grupo | `GROUP BY col, COUNT(*)` | `df.groupby('col').size()` |
| Filtro post-grupo | `HAVING ...` | `.groupby(...).filter(lambda g: ...)` |

**Cuándo elegir cada uno**:
- Los datos viven en una base → empezá con SQL, así reducís el volumen antes de traerlos a memoria.
- Necesitás operaciones de stats avanzadas, ML, plots → traé al DataFrame y usá pandas.
- Pipeline reproducible y versionado → SQL en archivos `.sql` + dbt > pandas notebook.

---

## Queries de ejemplo (encuesta sysarmy)

Las queries canónicas del notebook 04_3 que conviene tener internalizadas.

### 1. Filtro simple
```sql
SELECT *
FROM survey
WHERE salary_monthly_NETO > 100000
LIMIT 10;
```

### 2. Conteo con filtro
```sql
SELECT COUNT(1)
FROM survey
WHERE salary_monthly_NETO > 100000;
```

### 3. Promedio por subgrupo (con filtro de fila)
```sql
SELECT AVG(salary_monthly_NETO)
FROM survey
WHERE profile_gender = 'Mujer';
```

### 4. Promedio por grupo
```sql
SELECT profile_gender, AVG(salary_monthly_NETO)
FROM survey
GROUP BY profile_gender;
```

### 5. La query completa con todas las cláusulas
```sql
SELECT profile_gender, work_province,
       AVG(salary_monthly_NETO) AS avg_salary,
       COUNT(1) AS n
FROM survey
WHERE profile_years_experience > 5
GROUP BY profile_gender, work_province
HAVING COUNT(*) > 10
ORDER BY AVG(salary_monthly_NETO) DESC;
```

### 6. Top 10 con HAVING (Chinook)
```sql
SELECT composer, COUNT(trackid) AS cant
FROM tracks
WHERE composer <> ''
GROUP BY composer
HAVING cant > 30
ORDER BY cant DESC
LIMIT 10;
```

Top 10 compositores con más de 30 tracks, ordenados por cantidad.

---

## Ejemplo numérico (mini-tabla)

Imaginá una tabla `survey` chiquita, solo 5 filas:

| gender | salary | experience |
|---|---|---|
| Mujer | 800000 | 3 |
| Varón | 1200000 | 8 |
| Varón | 900000 | 2 |
| Mujer | 1500000 | 10 |
| Varón | 1100000 | 6 |

**Query 1 — Sueldo promedio por género**:
```sql
SELECT gender, AVG(salary) FROM survey GROUP BY gender;
```
Resultado:
- Mujer → (800000 + 1500000) / 2 = **1.150.000**
- Varón → (1200000 + 900000 + 1100000) / 3 = **1.066.667**

**Query 2 — Solo personas con más de 5 años de experiencia**:
```sql
SELECT * FROM survey WHERE experience > 5;
```
Resultado: 3 filas (Varón/1200000/8, Mujer/1500000/10, Varón/1100000/6).

**Query 3 — Sueldo promedio por género, solo experimentados, mostrando grupos con más de 1 persona**:
```sql
SELECT gender, AVG(salary), COUNT(*)
FROM survey
WHERE experience > 5
GROUP BY gender
HAVING COUNT(*) > 1;
```
Pasos mentales:
- Después de `WHERE`: quedan 3 filas (los experimentados).
- Después de `GROUP BY`: Mujer (1 persona), Varón (2 personas).
- Después de `HAVING COUNT(*) > 1`: solo queda Varón.

Resultado: una fila → Varón, 1.150.000, 2.

**Query 4 — Top sueldo**:
```sql
SELECT gender, salary FROM survey ORDER BY salary DESC LIMIT 1;
```
Resultado: Mujer, 1.500.000.

---

## Conexión con el TP

- **TP2 Ejercicio 1 (SQL con SQLAlchemy)**: el enunciado pide ingestar `melb_data` y `airbnb_price_by_zipcode` en una base SQLite, validar tipos (Date, Price), correr una serie de consultas (conteo por `Regionname`, conteo por `Suburb` + `Regionname`, propiedades con `Rooms > 2` por región, AVG de precio por `Type` y `Regionname`, top 5 suburbios), hacer un `JOIN` equivalente al `merge` de pandas, y **validar el resultado post-JOIN con assertions** (filas, %nulos, rangos).
- El patrón a usar: `engine = create_engine("sqlite:///melb.sqlite3")`, `df.to_sql("properties", engine, if_exists="replace")`, después `pd.read_sql(query, engine)` o `engine.connect() + text(query)`.
- Las assertions post-JOIN son críticas. Ejemplo:
  ```python
  result = pd.read_sql(join_query, engine)
  assert len(result) == len(melb_df), "El JOIN cambió la cantidad de filas"
  assert result["Price"].isna().sum() == 0, "Aparecieron NaN en Price post-JOIN"
  ```
- **TP2 — equivalencia mental Pandas/SQL**: como la consigna se puede resolver de los dos lados, conviene escribir la versión SQL primero, validarla, y después confirmar con pandas que da lo mismo. Es ejercicio mental de traducción.

---

## Errores comunes

1. **Olvidar `GROUP BY` cuando hay agregación**: escribís `SELECT province, AVG(salary) FROM survey` sin `GROUP BY province`. SQLite a veces te deja, otros motores tiran error. El resultado, cuando "anda", suele ser basura.
2. **Confundir `WHERE` con `HAVING`**: querer filtrar por `COUNT(*) > 10` adentro de `WHERE`. En `WHERE` todavía no existen los grupos. Va en `HAVING`.
3. **`JOIN` sin `ON`**: te puede explotar en producto cartesiano. Si la tabla A tiene 10.000 filas y B tiene 10.000, un join sin `ON` te da 100 millones de filas. Siempre `ON`.
4. **Asumir el motor de base de datos cuando se cambia**: lo que anda en SQLite no necesariamente anda en Postgres o MySQL. Funciones de fecha, conversión de tipos, sintaxis de `LIMIT`/`OFFSET`, soporte de `FULL OUTER JOIN`: todo varía. Si migrás de motor, retesteá todas las queries.
5. **`SELECT *` en queries productivas**: rompe cuando cambia el esquema, trae más datos de los necesarios, no expresa la intención. Listá las columnas.
6. **Comparar con NULL usando `=`**: `WHERE col = NULL` **nunca matchea nada**. NULL no es igual a NULL — es desconocido. Va `WHERE col IS NULL` o `WHERE col IS NOT NULL`.
7. **No validar tipos al ingestar**: `pd.to_sql` puede mapear un `Date` como texto si vos no parseás antes. Después tu `WHERE date > '2020-01-01'` ordena como string, no como fecha. Convertí con `pd.to_datetime` antes del `to_sql`.
8. **Asumir que `AVG` considera todas las filas**: `AVG(col)` saltea NULL. Si la mitad de tu columna es NULL y no lo sabés, el promedio que calculás es sobre la otra mitad solamente. Acompañalo siempre con un `COUNT(col)`.
9. **Pelearte con strings y mayúsculas**: SQLite por default es case-sensitive en `=` pero el `LIKE` es case-insensitive para ASCII. En Postgres es al revés. Si comparás texto, normalizá con `LOWER()` o usá `ILIKE` (Postgres).
10. **No usar `LIMIT` al explorar**: cuando estás aprendiendo una tabla nueva, `SELECT * FROM tabla` puede traerte 10 millones de filas y colgarte la notebook. Siempre arrancá con `LIMIT 100`.

---

## Detrás de escena: por qué NULL rompe la lógica que aprendiste en la escuela

Acá hay un tema que **te va a hacer dudar de tu cordura** la primera vez que te pase. NULL en SQL no se comporta como "vacío" o "cero" — se comporta como **desconocido**, y eso cambia toda la lógica booleana. Vamos a desarmarlo, porque te va a aparecer en TP2 sí o sí.

### El concepto: lógica de tres valores (3VL)

La lógica clásica (Boolean) tiene dos valores: TRUE y FALSE. SQL tiene **tres**: TRUE, FALSE y **UNKNOWN** (que aparece cuando hay NULL en la comparación).

Cuando vos comparás `5 = NULL` en SQL, no estás preguntando "¿son iguales?". Estás preguntando "¿son iguales 5 y un valor que no conozco?". Y la respuesta correcta es: **no sé**. Por eso devuelve UNKNOWN, no FALSE.

```sql
SELECT 5 = NULL;            -- NULL (UNKNOWN, no FALSE)
SELECT NULL = NULL;         -- NULL (no TRUE, porque "dos desconocidos" no son iguales)
SELECT NULL <> NULL;        -- NULL (otra vez, no se sabe)
SELECT NULL + 1;            -- NULL (cualquier operación con NULL es NULL)
```

### Por qué `WHERE col = NULL` siempre devuelve vacío

`WHERE` filtra las filas donde la condición es **TRUE**. UNKNOWN no es TRUE — es "no se sabe". Por lo tanto, ninguna fila pasa el filtro.

```sql
-- MAL: devuelve 0 filas siempre
SELECT * FROM melb WHERE Car = NULL;

-- BIEN: usá el operador especial IS NULL
SELECT * FROM melb WHERE Car IS NULL;

-- BIEN: para "no es NULL"
SELECT * FROM melb WHERE Car IS NOT NULL;
```

`IS NULL` y `IS NOT NULL` son los **únicos** operadores que devuelven TRUE/FALSE limpios sobre NULLs. Acordate de esos dos y te salvás del 90% de los bugs con nulos en SQL.

### Las dos versiones del COUNT (y por qué la cátedra las distingue)

Otro lugar donde NULL te muerde:

```sql
SELECT COUNT(*) FROM melb;          -- 13580 (todas las filas, incluso con NULL)
SELECT COUNT(Car) FROM melb;        -- 13518 (solo filas donde Car NO es NULL)
SELECT COUNT(BuildingArea) FROM melb;  -- 7130 (las que tienen el dato)
```

**Regla**:
- `COUNT(*)` cuenta filas. NULL no le importa.
- `COUNT(col)` cuenta valores NO NULOS de esa columna.
- `COUNT(DISTINCT col)` cuenta valores únicos NO NULOS.

La diferencia se vuelve crítica cuando calculás "completitud" de un dataset:

```sql
SELECT
    COUNT(*) AS total_filas,
    COUNT(BuildingArea) AS con_dato,
    COUNT(*) - COUNT(BuildingArea) AS sin_dato,
    100.0 * COUNT(BuildingArea) / COUNT(*) AS porcentaje_completo
FROM melb;
```

Esta query te dice exactamente cuántos faltantes tiene `BuildingArea`. Si confundís `COUNT(*)` con `COUNT(col)`, la métrica de completitud te miente.

### La trampa de AVG con NULLs

Las funciones de agregación (`AVG`, `SUM`, `MIN`, `MAX`) **ignoran los NULLs**. Eso suele ser lo que querés, pero hay que saberlo.

```sql
-- AVG ignora NULLs
SELECT AVG(BuildingArea) FROM melb;
-- Esto NO es la media sobre 13580 filas, es la media sobre 7130 filas.
```

Si la mitad de tu columna es NULL y no lo sabés, el promedio que reportás está calculado solo sobre la mitad informada. Eso puede sesgar tu análisis si los faltantes no son MCAR (ver archivo 02).

**Patrón defensivo**: cuando reportés un promedio, acompañalo con `COUNT(col)` para que el lector sepa sobre cuántas observaciones se calculó:

```sql
SELECT
    Suburb,
    AVG(BuildingArea) AS area_promedio,
    COUNT(BuildingArea) AS n_observaciones
FROM melb
GROUP BY Suburb
HAVING COUNT(BuildingArea) >= 10   -- ignoro suburbios con poca data
ORDER BY area_promedio DESC;
```

### NULL en JOINs

Cuando hacés un `LEFT JOIN` y una fila de la izquierda no tiene match, las columnas de la derecha quedan como **NULL** (no como 0, no como string vacío).

```sql
SELECT p.title, a.name
FROM albums p
LEFT JOIN artists a ON p.artistId = a.artistId;
-- Si un album no tiene artist registrado, a.name = NULL
```

La trampa habitual: querés filtrar "albums sin artista":

```sql
-- MAL: nunca matchea
WHERE a.name = NULL

-- BIEN
WHERE a.name IS NULL
```

Esto es exactamente lo que hace falta para auditar un `LEFT JOIN` en TP2: contar cuántas propiedades de Melbourne NO tienen match en AirBnB.

```sql
SELECT COUNT(*)
FROM melb LEFT JOIN airbnb_by_zip
    ON melb.Postcode = airbnb_by_zip.zipcode
WHERE airbnb_by_zip.zipcode IS NULL;
-- Cantidad de propiedades sin match en AirBnB
```

### `IN` y `NOT IN` con NULL: la trampa más sutil

Cuando usás `NOT IN` con una subquery o lista que contiene NULL, **la query se rompe silenciosamente**.

```sql
-- Si alguna fila de B tiene id = NULL, esta query devuelve VACÍO siempre
SELECT * FROM A WHERE id NOT IN (SELECT id FROM B);
```

¿Por qué? Porque `NOT IN` se traduce internamente a `id <> b1 AND id <> b2 AND id <> NULL AND ...`. Y `id <> NULL` es UNKNOWN, que NO es TRUE, así que NUNCA matchea.

**Solución**: usar `NOT EXISTS` o filtrar NULLs primero:

```sql
-- Opción 1: NOT EXISTS (recomendado)
SELECT * FROM A WHERE NOT EXISTS (
    SELECT 1 FROM B WHERE B.id = A.id
);

-- Opción 2: filtrar NULLs
SELECT * FROM A WHERE id NOT IN (
    SELECT id FROM B WHERE id IS NOT NULL
);
```

### Tabla resumen: operadores y NULL

| Expresión | Resultado | Por qué |
|-----------|-----------|---------|
| `5 = NULL` | NULL (UNKNOWN) | Igualdad con desconocido = desconocido |
| `5 <> NULL` | NULL | Lo mismo |
| `NULL = NULL` | NULL | Dos desconocidos no se confirman iguales |
| `NULL IS NULL` | TRUE | Operador especial, sí funciona |
| `NULL IS NOT NULL` | FALSE | Idem |
| `NULL AND TRUE` | NULL | Desconocido AND verdadero = desconocido |
| `NULL AND FALSE` | FALSE | Cualquier cosa AND falso = falso |
| `NULL OR TRUE` | TRUE | Cualquier cosa OR verdadero = verdadero |
| `NULL OR FALSE` | NULL | Desconocido OR falso = desconocido |
| `NULL + 1` | NULL | Aritmética con NULL = NULL |
| `COUNT(*)` | Cuenta filas | NULL no le afecta |
| `COUNT(col)` | Cuenta no-nulos | NULL no entra |
| `AVG(col)`, `SUM(col)` | Ignoran NULLs | Promedian/suman solo informados |
| `col IN (..., NULL, ...)` | Puede dar UNKNOWN | Cuidado con `NOT IN` |

### Resumen

- NULL en SQL es **desconocido**, no "vacío" ni "cero". Lógica de tres valores: TRUE, FALSE, UNKNOWN.
- `=` y `<>` con NULL devuelven NULL, no TRUE/FALSE. Por eso `WHERE col = NULL` nunca matchea.
- Usá `IS NULL` y `IS NOT NULL` como únicos operadores válidos.
- `COUNT(*)` cuenta filas; `COUNT(col)` cuenta no-nulos. La diferencia es la completitud de tu columna.
- `AVG`, `SUM` ignoran NULLs. Acompañá siempre con `COUNT(col)` para no engañar al lector.
- `NOT IN` con NULL en la lista se rompe silenciosamente. Usá `NOT EXISTS`.

¿Se entiende? La lógica que aprendiste en programación (booleana de dos valores) no es la que usa SQL. Saber esto te ahorra horas de "¿por qué mi query me devuelve vacío?".

---

## Checklist de comprensión

- [ ] Explicá la diferencia entre `WHERE` y `HAVING` con un ejemplo concreto donde uno no se pueda reemplazar por el otro.
- [ ] ¿Por qué `WHERE col = NULL` no funciona y qué se usa en cambio?
- [ ] ¿Cuál es el orden lógico de ejecución de una query con `SELECT`, `FROM`, `WHERE`, `GROUP BY`, `HAVING`, `ORDER BY`, `LIMIT`?
- [ ] Si tenés que combinar `melb_data` y `airbnb_by_zip` y querés conservar TODAS las propiedades aunque no tengan match en AirBnB, ¿qué tipo de JOIN usás?
- [ ] La cátedra cubre `JOIN`, `GROUP BY`, `HAVING`, agregaciones. ¿Qué tres temas SQL importantes te quedan para estudiar por afuera y dónde estudiarlos?
- [ ] Traducí esta query a pandas:  
   `SELECT gender, AVG(salary) FROM survey WHERE province = 'CABA' GROUP BY gender HAVING COUNT(*) > 50 ORDER BY AVG(salary) DESC;`
- [ ] ¿Por qué `SELECT *` es considerado mala práctica en queries productivas?
- [ ] ¿Cuál es la diferencia entre `COUNT(*)` y `COUNT(col)`? Construí una query que te diga el porcentaje de completitud de `BuildingArea`.
- [ ] ¿Qué pasa con `WHERE id NOT IN (SELECT id FROM B)` si en B hay algún NULL? ¿Cómo lo resolvés?

---

**Próximo paso**: `11-glosario.md`
