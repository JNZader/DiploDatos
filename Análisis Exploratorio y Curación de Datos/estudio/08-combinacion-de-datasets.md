# 08 — Combinación de datasets (join, merge, groupby)

## Concepto

Pocas veces el dataset que necesitás viene en un solo archivo. Lo habitual es tener **fuentes heterogéneas**: ventas en un CSV, clientes en una tabla SQL, precios de referencia en una API externa. **Combinar** esos datasets significa unirlos sobre una **clave común** para enriquecer la información.

En pandas hay dos operaciones centrales para esto:

| Operación      | Une por           | Equivalente conceptual         |
|----------------|-------------------|--------------------------------|
| `df.join()`    | índice            | Pegado lateral por índice      |
| `df.merge()`   | columnas          | JOIN de SQL                    |

Y un tercer paso, **groupby + agg**, que muchas veces tenés que aplicar **antes** del merge cuando las claves no son únicas en alguna de las tablas.

## Intuición

Pensá en dos planillas de papel. Una tiene datos de clientes (nombre, DNI, teléfono) y la otra tiene operaciones de venta (DNI, fecha, monto). Querés saber el nombre de cada cliente al lado de cada venta.

La **clave** es el DNI: la columna que aparece en ambas planillas y permite saber qué fila de una corresponde a qué fila de la otra. El **merge** es el acto de tomar cada fila de la planilla de ventas y pegarle a su lado el nombre del cliente cuyo DNI coincide.

Lo que cambia entre los tipos de join es **qué hacés con las filas que no encuentran pareja**:

- **inner**: descartás todo lo que no matchea de los dos lados.
- **left**: conservás todas las filas de la planilla izquierda; las que no matchean quedan con NaN en las columnas de la derecha.
- **right**: simétrico al anterior.
- **outer**: conservás todo de ambos lados, llenando NaN donde no hay match.

Y un tema crítico: si en la planilla de clientes hay **dos filas con el mismo DNI** (por error o porque registraste a la misma persona dos veces), cada venta de ese DNI va a duplicarse al pegar. Esto se llama **explosión cartesiana** y es la fuente número uno de bugs silenciosos en pipelines de datos.

---

## df.join vs df.merge

### df.join

Une por el **índice**. Útil cuando dos DataFrames comparten el mismo identificador como índice.

```python
df1.join(df2, how='outer')
```

Es más rápido y menos explícito. Lo usás cuando ya configuraste los índices a propósito (típicamente después de un `set_index`).

### df.merge

Une por **columnas** específicas. Es la operación equivalente al `JOIN` de SQL.

```python
df1.merge(df2, on='Postcode', how='left')
df1.merge(df2, left_on='Postcode', right_on='zipcode', how='left')
```

Lo usás cuando las claves están como columnas regulares (no como índice). Es más flexible: podés cruzar por **una o varias columnas**, con nombres distintos en cada tabla (`left_on` / `right_on`).

**Regla práctica**: para análisis exploratorio en pandas, usá `merge`. Es más explícito sobre qué columna estás usando, y eso evita el peor error de todos.

### Lo que pandas hace por default si no especificás `on`

```python
df1.merge(df2)   # SIN on=
```

Pandas usa la **intersección de columnas con el mismo nombre** entre ambos DataFrames. Esto es peligroso porque:

- Si las columnas comparten nombre pero significan cosas distintas (ej. `id` en una tabla es id de cliente y en la otra id de operación), pandas las cruza igual.
- Si no compartís ninguna columna, error críptico.
- Es completamente implícito: no podés mirar el código y saber qué está pasando.

**Regla**: pasá siempre `on=` o `left_on=/right_on=` explícito. Nunca confíes en el default.

---

## Tipos de join (visual)

Supongamos dos tablas:

**Tabla A** (clientes):

| dni | nombre  |
|-----|---------|
| 1   | Ana     |
| 2   | Beto    |
| 3   | Carla   |

**Tabla B** (ventas):

| dni | monto |
|-----|-------|
| 1   | 100   |
| 2   | 200   |
| 4   | 400   |

### Inner join

Solo las filas que matchean **en ambos** lados.

```python
A.merge(B, on='dni', how='inner')
```

| dni | nombre | monto |
|-----|--------|-------|
| 1   | Ana    | 100   |
| 2   | Beto   | 200   |

### Left join

Todas las filas de A; las que no matchean en B quedan con NaN.

```python
A.merge(B, on='dni', how='left')
```

| dni | nombre | monto |
|-----|--------|-------|
| 1   | Ana    | 100   |
| 2   | Beto   | 200   |
| 3   | Carla  | NaN   |

### Right join

Todas las filas de B; las que no matchean en A quedan con NaN.

```python
A.merge(B, on='dni', how='right')
```

| dni | nombre | monto |
|-----|--------|-------|
| 1   | Ana    | 100   |
| 2   | Beto   | 200   |
| 4   | NaN    | 400   |

### Outer join

Todas las filas de ambos lados; los huecos se rellenan con NaN.

```python
A.merge(B, on='dni', how='outer')
```

| dni | nombre | monto |
|-----|--------|-------|
| 1   | Ana    | 100   |
| 2   | Beto   | 200   |
| 3   | Carla  | NaN   |
| 4   | NaN    | 400   |

**Cuándo cada uno**:

- `inner`: cuando solo te interesan filas con información completa de ambos lados.
- `left`: el más común en enriquecimiento. Conservás todo el dataset principal y le agregás información extra cuando hay.
- `right`: raro. Casi siempre es un `left` con los DataFrames intercambiados.
- `outer`: cuando querés diagnosticar qué filas están en una tabla pero no en la otra (auditoría).

---

## groupby + agg como paso previo obligatorio

Si las claves en la tabla "secundaria" son **N:N** (un mismo `zipcode` aparece en muchísimas filas), un `merge` directo te genera **explosión cartesiana**. Cada fila del dataset principal se duplica tantas veces como matches haya en el secundario.

La solución es agregar **antes** del merge:

```python
secundaria_agregada = (secundaria
    .groupby('clave')
    .agg({'columna_numerica': ['mean', 'count'],
          'otra_columna': 'mean'})
    .reset_index())
```

Esto colapsa las múltiples filas por clave en una sola fila con estadísticos agregados (media, conteo, mediana, lo que sea). Después podés mergear con confianza:

```python
merged = principal.merge(secundaria_agregada, on='clave', how='left')
```

Resultado: una fila por cada fila del principal, enriquecida con los estadísticos del secundario.

---

## Caso melb_data + AirBnB

Este es el caso central de la Clase 4. El objetivo, según la cátedra:

> *"Estimar con mayor precisión el valor del vecindario."*

Tenemos dos datasets:

- `melb_data.csv`: 13.580 propiedades en venta en Melbourne, con `Postcode`.
- `cleansed_listings_dec18.csv`: ~22.000 publicaciones de AirBnB en Melbourne, con `zipcode` y precios por noche, semana, mes.

La idea: para cada propiedad en venta, traer el **precio promedio de AirBnB en ese código postal** como feature de enriquecimiento.

### Por qué un merge ingenuo explota

Si hacés directamente:

```python
merged = melb_df.merge(airbnb_df, left_on='Postcode', right_on='zipcode', how='left')
```

Cada propiedad de Melbourne va a matchear con **todas** las publicaciones de AirBnB de su código postal. Si en un postcode hay 200 publicaciones, una propiedad en venta se duplica 200 veces.

Resultado: el merged pasa de 13.580 filas a más de **2 millones de filas**. Inviable para análisis posterior y conceptualmente incorrecto (cada propiedad es una sola, no 200).

### Solución: agregar AirBnB por zipcode antes

```python
airbnb_df['zipcode'] = pd.to_numeric(airbnb_df.zipcode, errors='coerce')

relevant = ['price', 'weekly_price', 'monthly_price', 'zipcode']
airbnb_by_zip = (airbnb_df[relevant]
    .groupby('zipcode')
    .agg({'price': ['mean', 'count'],
          'weekly_price': 'mean',
          'monthly_price': 'mean'})
    .reset_index())

# Aplastar el MultiIndex de columnas
airbnb_by_zip.columns = [' '.join(c).strip() for c in airbnb_by_zip.columns.values]

merged = melb_df.merge(airbnb_by_zip, how='left',
                       left_on='Postcode', right_on='zipcode')
```

Ahora `airbnb_by_zip` tiene **una fila por código postal** con estadísticos agregados, y el merge produce un DataFrame de la misma longitud que `melb_df` (13.580 filas).

### Validación post-merge (siempre)

```python
import numpy

assert len(merged) == len(melb_df), "El merge cambió la cantidad de filas"
assert merged["Price"].isna().sum() == 0, "Aparecieron NaN donde no debería haber"
assert merged["airbnb_price_mean"].dropna().between(0, 10000).all(), "Precios fuera de rango"

intersection = numpy.intersect1d(airbnb_df.zipcode.values, melb_df.Postcode.values)
print(f"Postcodes en común: {len(intersection)}")
```

Estas tres líneas son la diferencia entre un pipeline robusto y uno que rompe en producción tres meses después. Las assertions tienen que estar **siempre** después de operaciones críticas.

---

## Ejemplo numérico: los cuatro tipos de join

Vamos a comparar el resultado con dos mini-tablas concretas.

**Productos**:

| sku | producto    |
|-----|-------------|
| A   | manzana     |
| B   | banana      |
| C   | cereza      |

**Ventas**:

| sku | cantidad |
|-----|----------|
| A   | 10       |
| B   | 5        |
| D   | 7        |

### inner

```python
productos.merge(ventas, on='sku', how='inner')
```

| sku | producto | cantidad |
|-----|----------|----------|
| A   | manzana  | 10       |
| B   | banana   | 5        |

**2 filas**. C (que no se vendió) y D (venta sin producto en catálogo) desaparecen.

### left

```python
productos.merge(ventas, on='sku', how='left')
```

| sku | producto | cantidad |
|-----|----------|----------|
| A   | manzana  | 10       |
| B   | banana   | 5        |
| C   | cereza   | NaN      |

**3 filas**. Conservamos todo el catálogo, incluso productos sin ventas.

### right

```python
productos.merge(ventas, on='sku', how='right')
```

| sku | producto | cantidad |
|-----|----------|----------|
| A   | manzana  | 10       |
| B   | banana   | 5        |
| D   | NaN      | 7        |

**3 filas**. Conservamos todas las ventas, incluso las que no tienen producto en catálogo (¿dato sucio? ¿producto descatalogado?).

### outer

```python
productos.merge(ventas, on='sku', how='outer')
```

| sku | producto | cantidad |
|-----|----------|----------|
| A   | manzana  | 10       |
| B   | banana   | 5        |
| C   | cereza   | NaN      |
| D   | NaN      | 7        |

**4 filas**. Vemos todo: productos sin ventas y ventas sin producto. Útil para auditar.

---

## La clave puede ser cualquier cosa

La cátedra cierra con esta idea:

> *"La clave puede ser un identificador, una fecha, una coordenada GPS, una entidad nombrada o incluso un embedding."*

Lo importante es que tengas en ambas tablas algo que represente la **misma entidad**. Algunos ejemplos:

- **Identificador clásico**: DNI, código postal, SKU, ID de transacción.
- **Fecha**: cuando unís series temporales (precio de acción + temperatura del día).
- **Coordenada GPS**: requiere joins espaciales (geopandas, sjoin). No es exacto; usás buffers o "punto más cercano".
- **Entidad nombrada**: NER (Named Entity Recognition) extrae personas/lugares/organizaciones de texto y eso es la clave.
- **Embedding**: vector denso de un texto/imagen. Unís por **similitud coseno**, no por igualdad. Es la base de RAG.

Esto último es lo más moderno: cuando no tenés clave exacta, la "clave" es una representación vectorial y el join se vuelve un problema de **vecinos más cercanos**.

---

## Conexión con el TP

- **TP2 Ejercicio 2.2 (Enriquecimiento AirBnB)**: la consigna pide unir `melb_data` con `airbnb_price_by_zipcode.csv` por código postal. **Importante**: este segundo CSV se genera en la notebook 04_1 con el groupby agregado, así que tenés que correr esa notebook primero o replicar el cálculo.
- **TP2 Ejercicio 2.2 (transformaciones)**: la consigna pide justificar si usás mediana o media al agregar AirBnB. Mediana si hay outliers (caro/barato extremo); media si la distribución por zipcode es simétrica. **Justificalo siempre** en el documento.
- **TP2 Ejercicio 2.2 (mínimo de registros)**: la consigna pide elegir un mínimo de registros AirBnB por zipcode para que la agregación sea confiable. Si un zipcode tiene una sola publicación de AirBnB, el "promedio" no es informativo. Filtrá con `count >= 10` o el umbral que justifiques.
- **TP2 Ejercicio 2.2 (variables alternativas de join)**: la consigna pide proponer 2 variables alternativas de cruce y enumerar 3 preguntas que le harías a un experto inmobiliario. Pista: coordenadas geoespaciales (Latitude/Longitude) permiten cruces más finos que zipcode.
- **TP2 Ejercicio 1 (SQL JOIN)**: el mismo merge se replica en SQL usando JOIN. Validá que ambas implementaciones produzcan resultados equivalentes (mismas filas, mismos valores) como ejercicio de coherencia.
- **TP2 Validación post-merge**: la consigna pide **explícitamente** asserts de filas, % de nulos y rangos después de cualquier operación crítica. No son opcionales.

---

## Errores comunes

1. **Claves duplicadas no detectadas**. Si la "clave" se repite en una de las tablas, el merge explota cartesianamente. Verificalo antes:
   ```python
   assert df['clave'].is_unique, "Hay claves duplicadas — agregar antes"
   ```
2. **Tipos incompatibles**. `Postcode` viene como `float` en `melb_data` (porque hay NaN) y como `int` o `str` en AirBnB. El merge no rompe pero **no matchea**: te devuelve todos los joins como NaN y vos no te das cuenta. Castealos al mismo tipo antes:
   ```python
   df1['key'] = df1['key'].astype('Int64')   # nullable integer
   df2['key'] = df2['key'].astype('Int64')
   ```
3. **Mismo nombre, distinto significado**. Si ambas tablas tienen una columna llamada `price` pero significan precios distintos, el merge crea `price_x` y `price_y`. Renombralas antes para que el resultado sea legible:
   ```python
   airbnb_df = airbnb_df.rename(columns={'price': 'airbnb_price'})
   ```
4. **No validar nulos post-merge**. Si esperabas un `left join` con cobertura del 100% y aparecen NaN, hay un problema: claves desalineadas, tipos distintos, encoding diferente. Detectalo con `merged.isnull().sum()`.
5. **Hacer merge sin `on=`**. Pandas usa la intersección de columnas con el mismo nombre, lo que produce resultados impredecibles. **Siempre** especificá la clave.
6. **No agregar antes cuando hay relación N:N**. Es el error que produce la explosión a 2 millones de filas en el caso AirBnB. Si el secundario tiene múltiples filas por clave, agregá primero con `groupby`.
7. **Confundir join con concat**. `pd.concat` apila DataFrames (uno arriba del otro o uno al lado del otro), no une por clave. Si querés "agregarle columnas a una tabla", usá merge o join, no concat.
8. **Olvidarse del `how=` y obtener un inner por default**. El default de `merge` es `inner`, que **descarta filas sin match**. Si tu dataset adelgaza inesperadamente después de un merge, revisá el `how`.
9. **Aplastar MultiIndex de columnas manualmente y mal**. Cuando hacés `.agg({'col': ['mean', 'count']})`, pandas devuelve un MultiIndex en las columnas. Si no lo aplastás, el merge posterior se complica. Usá:
   ```python
   df.columns = [' '.join(c).strip() for c in df.columns.values]
   ```

---

## Detrás de escena: por qué `merge` puede DUPLICAR filas sin avisarte

Acá hay un tema que **te muerde feo y silencioso**, sobre todo en TP2 cuando enriquecés con AirBnB. La explosión cartesiana de 13.580 → 2 millones de filas que ya vimos es la versión obvia. Pero hay una versión sutil, donde el merge **duplica solo algunas filas** y vos no te enterás hasta que tus métricas dan raras. Vamos a desarmarlo.

### El escenario que duele

Imaginate que mergeás `melb_df` (13.580 filas) contra `airbnb_by_zip`, que vos **creés** que tiene una sola fila por zipcode (porque hiciste `groupby('zipcode')`). El merge te devuelve **13.582 filas**.

Dos filas de diferencia. Nada explota, ningún assert obvio falla. Tus análisis siguen corriendo. Tres semanas después descubrís que dos propiedades se duplicaron y tu promedio de precio está sesgado por esa duplicación.

¿Qué pasó? Probablemente uno de estos tres:

1. **`zipcode` tenía un duplicado en `airbnb_by_zip`** porque hubo dos versiones del mismo postcode (uno como `3000` y otro como `3000.0`, o uno como string y otro como int).
2. **El `reset_index()` se olvidó** y el `zipcode` siguió como índice + columna, generando ambigüedad.
3. **El `groupby` no agrupó todo** porque había NaN en `zipcode` (groupby por defecto los descarta, pero pueden quedar duplicados en otra forma).

Pandas no te avisa de nada. El merge corrió, devolvió un DataFrame válido. La explosión fue silenciosa.

### Por qué pandas no te avisa

`merge` no sabe qué esperabas. Si las claves de un lado tienen duplicados, pandas asume que **vos sabés** y que querés el producto cartesiano para esas filas. Es lo mismo que un `JOIN` en SQL: si A tiene 1 fila con `id=5` y B tiene 3 filas con `id=5`, el `JOIN` te devuelve 3 filas. Es matemáticamente correcto. Conceptualmente, suele ser un bug.

### La solución: `validate=`

Pandas tiene un argumento poco conocido pero **crítico** para evitar esto: `validate=`. Le decís qué cardinalidad esperás en el merge, y si no se cumple, **pandas tira error en lugar de seguir**.

```python
merged = melb_df.merge(
    airbnb_by_zip,
    how='left',
    left_on='Postcode',
    right_on='zipcode',
    validate='many_to_one'   # ← LA LÍNEA CLAVE
)
```

Cuatro valores posibles para `validate`:

| Valor | Lo que pandas chequea | Cuándo usarlo |
|-------|------------------------|---------------|
| `'one_to_one'` | Claves únicas en AMBOS lados | Merge entre dos tablas dimensionales (raro) |
| `'one_to_many'` | Claves únicas en el lado IZQUIERDO | Lookup desde tabla dimensional hacia tabla de hechos |
| `'many_to_one'` | Claves únicas en el lado DERECHO | **El caso típico**: enriquecimiento con tabla agregada |
| `'many_to_many'` | No chequea nada (default) | Cuando explícitamente esperás explosión |

### Aplicado al caso TP2

Después de hacer `groupby('zipcode')` sobre AirBnB, esperás que **cada zipcode aparezca una sola vez** en `airbnb_by_zip`. Por lo tanto, el merge con `melb_df` (donde un mismo `Postcode` aparece varias veces porque hay muchas propiedades en el mismo barrio) es **many-to-one** (muchas propiedades, un solo registro agregado de AirBnB).

```python
merged = melb_df.merge(
    airbnb_by_zip,
    how='left',
    left_on='Postcode',
    right_on='zipcode',
    validate='many_to_one'
)
# Si airbnb_by_zip tiene un solo zipcode duplicado, esto tira:
# MergeError: Merge keys are not unique in right dataset; not a many-to-one merge
```

Si te tira ese error, **buena noticia**: lo cazaste antes de que infle el dataset. Vas a tu `groupby` y ves por qué no agrupó bien.

### Cómo verificar a mano (antes o además de `validate`)

`validate` es la herramienta canónica, pero también es buena costumbre validar manualmente:

```python
# Antes del merge: chequear unicidad en el lado derecho
assert airbnb_by_zip['zipcode'].is_unique, "zipcode duplicado en airbnb_by_zip"

# Después del merge: chequear cardinalidad
assert len(merged) == len(melb_df), f"Merge cambió filas: {len(melb_df)} → {len(merged)}"
```

Las dos son redundantes con `validate='many_to_one'`, pero más explícitas en el código. La cátedra pide las assertions post-merge en TP2 explícitamente.

### Causas más comunes de duplicados silenciosos

| Causa | Cómo detectarla | Solución |
|-------|-----------------|----------|
| NaN en la clave del lado derecho | `airbnb_by_zip['zipcode'].isna().sum() > 0` | `dropna(subset=['zipcode'])` antes |
| Tipos mixtos (`3000` int y `3000.0` float) | `airbnb_by_zip['zipcode'].apply(type).unique()` | `astype('Int64')` ambos lados |
| Whitespace en strings (`'CABA '` vs `'CABA'`) | `airbnb_by_zip['zipcode'].str.strip().nunique()` | `.str.strip()` antes del groupby |
| Mayúsculas/minúsculas (`'caba'` vs `'CABA'`) | `nunique()` con y sin `.str.lower()` | Normalizar a mismo case |
| Olvido del `reset_index()` post-groupby | `airbnb_by_zip.index.name` no es None | Agregar `.reset_index()` |

### Caso real: el bug del Postcode con NaN

En Melbourne, `Postcode` tiene algunos NaN (porque originalmente era numérica y se promovió a float). Si hacés un `groupby('Postcode')` en AirBnB y AirBnB también tiene NaN en `zipcode`, **ambos lados van a tener una "categoría NaN"**. Pandas trata cada NaN como **distinto** (recordá: NaN ≠ NaN por IEEE 754). Resultado: tu merge no junta los NaN entre sí, los deja como NaN sin match. Y si por algún motivo aparecen duplicados con la misma clave NaN en algún lado, el comportamiento se vuelve aún más impredecible.

**Solución**: explícitamente eliminá las filas con clave NaN antes de mergear:

```python
melb_df_clean = melb_df.dropna(subset=['Postcode'])
airbnb_by_zip_clean = airbnb_by_zip.dropna(subset=['zipcode'])

merged = melb_df_clean.merge(
    airbnb_by_zip_clean,
    how='left',
    left_on='Postcode',
    right_on='zipcode',
    validate='many_to_one'
)
```

### Resumen

- `merge` puede duplicar filas silenciosamente si las claves del lado derecho no son únicas.
- Pandas **no te avisa** por default. Para sí avisar, pasá `validate='many_to_one'` (o el modo que corresponda).
- Causas típicas: NaN en la clave, tipos mixtos, whitespace, olvido del `reset_index`.
- En TP2 el patrón canónico es: `groupby` + `reset_index` + `merge(validate='many_to_one')` + asserts post-merge.
- Si te tira `MergeError`, festejá: cazaste el bug antes de que lo cuente tu profesor.

¿Se entiende? Es un argumento de una palabra (`validate=`) que te ahorra debuggear pipelines tres meses después.

---

## Checklist de comprensión

- [ ] ¿Cuál es la diferencia entre `df.join` y `df.merge`? ¿Cuándo usás cada uno?
- [ ] En el caso AirBnB, ¿por qué el merge ingenuo produce 2 millones de filas y por qué eso es conceptualmente incorrecto?
- [ ] Dadas las dos mini-tablas de productos y ventas, ¿podés escribir de memoria los 4 resultados (inner, left, right, outer)?
- [ ] ¿Qué tres validaciones post-merge son obligatorias en TP2?
- [ ] Si el merge te devuelve todos los joins como NaN aunque las claves "deberían" matchear, ¿cuál es el primer sospechoso?
- [ ] La cátedra dice que la clave "puede ser un embedding". ¿Qué significa eso operativamente? (Pista: pensá en RAG.)
- [ ] ¿Qué hace `validate='many_to_one'` y en qué situación de TP2 lo activarías?

---

**Próximo paso**: `09-etl-y-dags.md`
