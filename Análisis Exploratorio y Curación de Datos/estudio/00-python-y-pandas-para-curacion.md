# 00 — Python y pandas para curación

## Concepto

Curar datos no es escribir código bonito: es **modificar la realidad** que va a ver tu modelo. Cada `.fillna()`, cada `replace`, cada `merge`, cada `drop_duplicates` es una decisión que sobrevive hasta producción. Por eso, en EyCD pandas deja de ser "una herramienta para hacer tablas" y pasa a ser el bisturí con el que vas a operar tu dataset. Si no manejás el bisturí, no operás: arruinás al paciente.

Este archivo es un refresher. Asume que ya tocaste pandas en AVD. Lo que cambia acá es la **intención**: en AVD pandas era para describir; en EyCD pandas es para transformar de forma reproducible, trazable y reversible.

## Intuición

Pensá un DataFrame como una **planilla de Excel con superpoderes y memoria**. La planilla normal te deja escribir, copiar y pegar; el DataFrame además te deja rebobinar (siempre que hayas hecho una copia), aplicar la misma operación a millones de filas sin tocar el mouse, y dejar registro de qué cambiaste.

La trampa: esos superpoderes incluyen **pisar el original sin avisar**. En AVD eso era molesto; en EyCD es catastrófico, porque la curación es un pipeline y si pisás el original perdés el "estado antes de" contra el cual auditar. La regla mental: **el DataFrame crudo es sagrado, todo lo demás se trabaja sobre copias**.

---

## Lo mínimo indispensable (revisitado para curación)

### Importar librerías

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
```

Las cuatro de siempre. En EyCD se suman dos invitadas frecuentes que vamos a ver en otros archivos:

```python
import missingno as msno              # visualización de faltantes
from sklearn.impute import SimpleImputer, KNNImputer  # imputación
```

### Leer el dataset (con la URL canónica de la materia)

```python
url = "https://cs.famaf.unc.edu.ar/~mteruel/datasets/diplodatos/melb_data.csv"
melb_data = pd.read_csv(url)
melb_data.shape  # (13580, 21)
```

`melb_data` (Melbourne Housing Snapshot) es **el dataset que vas a usar en TODA la materia**. Acostumbrate a su forma: 13.580 filas, 21 columnas, faltantes conocidos en `Car`, `BuildingArea`, `YearBuilt` y `CouncilArea`.

---

## DataFrames, Series y por qué importa la diferencia

| Estructura | Qué es | Ejemplo |
|------------|--------|---------|
| `DataFrame` | Tabla 2D (filas × columnas) | `melb_data` completo |
| `Series` | Una sola columna (vector con nombre e índice) | `melb_data["Price"]` |

Si seleccionás **una columna con corchetes simples** obtenés una Series:

```python
precios = melb_data["Price"]            # Series
type(precios)                           # pandas.core.series.Series
```

Si la seleccionás **con corchetes dobles** obtenés un DataFrame de una columna:

```python
precios_df = melb_data[["Price"]]       # DataFrame de 1 columna
type(precios_df)                        # pandas.core.frame.DataFrame
```

¿Por qué nos importa en curación? Porque `sklearn` espera estructuras 2D (DataFrames o matrices). Si le pasás una Series, te tira un `ValueError` o un warning incómodo. Acostumbrate a usar dobles corchetes cuando vas a pasar la columna a un imputador o scaler.

---

## Dtypes: la diferencia entre `object`, `int64`, `float64` y `datetime64`

Esto es **el primer chequeo de toda curación**:

```python
melb_data.dtypes
```

| Dtype | Qué guarda | Trampa común en curación |
|-------|-----------|--------------------------|
| `int64` | Enteros | Una columna con NaN deja de ser `int64` y pasa a `float64`. Pandas no tiene int con NaN salvo el tipo `Int64` (con I mayúscula, nullable) |
| `float64` | Decimales | Aparece "sin querer" cuando una columna entera tiene faltantes |
| `object` | Texto o tipos mixtos | El cajón de sastre. Si una columna numérica aparece como `object`, **hay basura adentro** (comas, símbolos, espacios) |
| `bool` | Verdadero/falso | Útil para máscaras de filtrado |
| `datetime64[ns]` | Fechas con resolución de nanosegundo | Solo aparece si llamaste a `pd.to_datetime`. Por defecto las fechas vienen como `object` |

Ejemplo de la trampa más típica:

```python
# Antes de tocar nada
melb_data["Date"].dtype           # dtype('O') → object, NO es fecha todavía
melb_data["Date"].head()          # '3/12/2016', '4/02/2016', ...

# Conversión a fecha verdadera
melb_data["Date"] = pd.to_datetime(melb_data["Date"], format="%d/%m/%Y")
melb_data["Date"].dtype           # dtype('<M8[ns]') → ahora sí es datetime
```

Mientras `Date` siga siendo `object`, no podés ordenar cronológicamente, ni hacer `.dt.year`, ni agrupar por mes. Lo confunde con strings.

---

## `.copy()`: el reflejo que te puede salvar la materia

En EyCD vas a leer esta frase en cada clase y en cada TP:

> **NUNCA accionar sobre el dataset original.**

La razón no es ideológica, es técnica. Pandas, cuando te devuelve un subconjunto, a veces te da una **vista** (referencia al original) y a veces una **copia**. La diferencia es invisible hasta que modificás y se rompe todo, o aparece el famoso `SettingWithCopyWarning`. Para no pelearte con cuándo te devuelve qué, el patrón seguro es **forzar copia explícita**:

```python
# MAL: trabajar directo sobre el original
melb_data.loc[melb_data.Bathroom < 1, "Bathroom"] = pd.NA   # rompe el crudo

# BIEN: copia explícita y trabajo sobre la copia
melb_df = melb_data.copy()
melb_df.loc[melb_df.Bathroom < 1, "Bathroom"] = pd.NA       # original intacto
```

¿Por qué importa tanto en curación y no tanto en AVD?

- En AVD describías. Si pisabas el original, recargabas el CSV y listo.
- En EyCD curás. Encadenás 5 transformaciones. Si pisás el original en la transformación 3, no tenés contra qué comparar el "antes" para la transformación 5, y perdés la trazabilidad.

**Regla operativa**: en cada notebook, la primera línea después de `read_csv` es `melb_df = melb_data.copy()`. Después trabajás sobre `melb_df`. El `melb_data` queda como **piedra Rosetta** para auditar.

---

## `loc` vs `iloc`: el malentendido más caro

| Selector | Indexa por | Ejemplo |
|----------|-----------|---------|
| `.loc[]` | **Etiquetas** (nombres de fila y columna) | `df.loc[5, "Price"]` |
| `.iloc[]` | **Posiciones enteras** (0, 1, 2, ...) | `df.iloc[0, 4]` |

El error más caro es asumir que `df.loc[5]` te devuelve la fila número 6 (índice 5). Solo es cierto si el índice del DataFrame son enteros 0..N. Si filtraste antes y el índice quedó "salteado", `.loc[5]` puede no existir o devolver otra fila.

Patrón limpio para filtrar Y modificar al mismo tiempo:

```python
# Marcar como faltante todas las filas con Bathroom == 0
melb_df.loc[melb_df.Bathroom < 1, "Bathroom"] = pd.NA
```

Esto se lee: "en las filas donde `Bathroom < 1`, en la columna `Bathroom`, escribí `pd.NA`". `.loc` es la forma **segura** de asignar; `df[df.x < 1]["x"] = pd.NA` te tira `SettingWithCopyWarning` y a veces ni siquiera modifica.

---

## Detectar faltantes: `isnull`, `notnull` y los "ceros enmascarados"

```python
melb_df.isnull().sum()        # cantidad de NaN por columna
melb_df.notnull().sum()       # cantidad de NO NaN por columna
melb_df.isnull().sum() / len(melb_df)  # proporción de faltantes
```

La **trampa de EyCD**: en muchos datasets, los faltantes vienen disfrazados de `0`, `-1`, `999` o `"NA"` (como string). Pandas los toma como valores válidos hasta que vos no le digás "che, esto en realidad es un faltante".

El patrón canónico de la cátedra para detectar ceros sospechosos:

```python
# Contar ceros por columna
cols_con_ceros = melb_df[melb_df == 0].count(axis=0)
cols_con_ceros[cols_con_ceros > 0]
# Salida típica: Landsize, BuildingArea, Bedroom2, Bathroom...
```

Después, **con criterio**, decidís cuáles ceros son enmascaramiento y cuáles son válidos. `Car == 0` significa "sin cochera" (válido). `Landsize == 0` significa "no se registró" (faltante disfrazado).

---

## `select_dtypes`: separar numéricas de categóricas en una línea

En curación, casi todas las técnicas se aplican **por tipo de variable**. Imputar la media solo tiene sentido en numéricas. OneHotEncoder solo en categóricas. Necesitás un cuchillo limpio para separar ambos mundos:

```python
# Solo numéricas
numericas = melb_df.select_dtypes(include=["number"])

# Solo objetos (categóricas)
categoricas = melb_df.select_dtypes(include=["object"])

# Excluir un tipo en lugar de incluir
sin_fechas = melb_df.select_dtypes(exclude=["datetime"])
```

Esto es lo que vas a usar en TP1 cuando separes el dataset en "matriz numérica" y "matriz categórica" antes de hacer encoding y concatenarlas.

---

## `value_counts`, `unique`, `nunique`: la santísima trinidad de las categóricas

| Método | Devuelve | Cuándo usarlo |
|--------|----------|---------------|
| `df["col"].unique()` | Array con los valores distintos | Ver si hay typos ("CABA", "caba", "Capital") |
| `df["col"].nunique()` | Cuántos valores distintos hay | Detectar alta cardinalidad antes de OHE |
| `df["col"].value_counts()` | Frecuencia de cada valor, ordenada desc | Ver desbalance / dominancia |

Ejemplo concreto sobre Melbourne:

```python
melb_df["Type"].value_counts()
# h    9449   (casa)
# u    3017   (unit/depto)
# t    1114   (townhouse)

melb_df["Suburb"].nunique()    # 314 suburbios distintos
```

Ese `314` es la **alarma** que dice "no le hagas OneHotEncoder a Suburb sin reducir cardinalidad primero, porque vas a generar 314 columnas nuevas".

---

## `groupby` + `agg`: agregar antes de pegar

`groupby` es la operación más subestimada en EyCD. No la usás solo para resumir: la usás para **preparar una tabla** antes de unirla con otra. El TP2 lo ejemplifica: si pegás 13.580 propiedades contra ~22.000 publicaciones de AirBnB sin agregar primero, terminás con **2 millones de filas**. Si agregás AirBnB por código postal primero, terminás con las 13.580 filas originales y un par de columnas nuevas.

```python
# Agregar AirBnB por código postal antes del merge
airbnb_by_zip = (
    airbnb_df[["price", "weekly_price", "monthly_price", "zipcode"]]
        .groupby("zipcode")
        .agg({
            "price":         ["mean", "count"],
            "weekly_price":  "mean",
            "monthly_price": "mean",
        })
        .reset_index()
)
```

Lectura del bloque:

- `.groupby("zipcode")` agrupa por código postal.
- `.agg({...})` aplica funciones distintas a cada columna. `price` recibe dos (`mean` y `count`); el resto, una.
- El resultado tiene un **MultiIndex** en columnas (`price.mean`, `price.count`, ...) que conviene aplanar con:

```python
airbnb_by_zip.columns = [" ".join(c).strip() for c in airbnb_by_zip.columns.values]
```

- `.reset_index()` pasa el `zipcode` de índice a columna normal, así podés mergear contra él.

---

## `merge` / `join`: preview rápido (lo detallado va en otro archivo)

`merge` es el `JOIN` de SQL traído a pandas:

```python
merged = melb_df.merge(
    airbnb_by_zip,
    how="left",
    left_on="Postcode",
    right_on="zipcode"
)
```

Lo que tenés que saber acá:

- `how`: `"left"`, `"right"`, `"inner"`, `"outer"`. **`"left"` es lo más seguro en curación**: garantiza que no perdés filas del dataset principal.
- `left_on` / `right_on`: las claves del lado izquierdo y derecho. Pueden tener nombres distintos (como `Postcode` y `zipcode`).
- Si los nombres coinciden, podés usar `on="zipcode"` directamente.

Y la **regla de oro post-merge** (que vas a aplicar en TP2):

```python
assert len(merged) == len(melb_df), "El merge cambió la cantidad de filas"
assert merged["Price"].isna().sum() == 0, "El merge introdujo NaN en Price"
```

Si una de estas dos falla, **algo en la curación se rompió** y tenés que volver atrás. Las assertions son tu sistema de alarma.

---

## Ejemplo numérico

Tenés esta mini-tabla de 5 propiedades:

| id | Suburb  | Rooms | Price    | Date       | Car |
|----|---------|-------|----------|------------|-----|
| 1  | Abbots  | 3     | 1480000  | 3/12/2016  | 1.0 |
| 2  | Abbots  | 2     | 1035000  | 4/02/2016  | 0.0 |
| 3  | Carlton | 4     | NaN      | 4/06/2016  | 2.0 |
| 4  | Carlton | 3     | 1876000  | 5/06/2016  | NaN |
| 5  | Carlton | 2     | 850000   | 4/02/2017  | 0.0 |

Pasos típicos de un primer minuto de curación:

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    "Suburb": ["Abbots", "Abbots", "Carlton", "Carlton", "Carlton"],
    "Rooms":  [3, 2, 4, 3, 2],
    "Price":  [1_480_000, 1_035_000, np.nan, 1_876_000, 850_000],
    "Date":   ["3/12/2016", "4/02/2016", "4/06/2016", "5/06/2016", "4/02/2017"],
    "Car":    [1.0, 0.0, 2.0, np.nan, 0.0],
})
```

**1. Diagnóstico inicial**:

```python
df.shape          # (5, 5)
df.dtypes
# Suburb     object
# Rooms       int64
# Price     float64
# Date       object   ← todavía no es fecha
# Car       float64   ← int "contaminado" por NaN
```

**2. Detección de faltantes**:

```python
df.isnull().sum()
# Suburb    0
# Rooms     0
# Price     1
# Date      0
# Car       1
```

**3. Copia antes de tocar nada**:

```python
clean = df.copy()
```

**4. Tipado correcto de fechas**:

```python
clean["Date"] = pd.to_datetime(clean["Date"], format="%d/%m/%Y")
clean["Date"].dtype     # datetime64[ns]
```

**5. `value_counts` de la categórica**:

```python
clean["Suburb"].value_counts()
# Carlton    3
# Abbots     2
```

**6. `groupby` + `agg` para resumen rápido**:

```python
clean.groupby("Suburb").agg(
    precio_medio=("Price", "mean"),
    precio_mediana=("Price", "median"),
    casas=("Price", "count"),
)
#          precio_medio  precio_mediana  casas
# Suburb
# Abbots     1257500.0       1257500.0      2
# Carlton    1363000.0       1363000.0      2
```

Fijate que `count` cuenta **no nulos**: Carlton tiene 3 filas pero solo 2 precios informados.

**7. Trazabilidad**:

```python
df.equals(clean)   # False — modificamos Date
# Pero el original df sigue como vino del CSV.
```

Eso es **la curación bien hecha**: cambiaste lo que tenías que cambiar, sin perder el crudo.

---

## Regla de oro de la materia

> **Un pipeline correcto en código pero flojo en criterio es un pipeline incorrecto.**

No alcanza con que `df.isnull().sum()` te dé cero al final. Tenés que poder justificar **por qué** imputaste con la mediana y no con la media, **por qué** descartaste filas y no columnas, **por qué** elegiste KNN sobre constante. Cada decisión de curación tiene que estar escrita, con su motivo y su impacto. Si no podés defender la decisión, la decisión está mal aunque el código corra.

---

## Conexión con el TP

- **TP1, todo el ejercicio**: arranca con `melb_data = pd.read_csv(url)` y la línea siguiente **tiene que ser** `melb_df = melb_data.copy()`. Después, vas a usar `select_dtypes` para separar numéricas y categóricas, `OneHotEncoder` sobre las categóricas, `IterativeImputer` sobre las numéricas, y al final concatenar las dos matrices. Cada paso vive sobre `melb_df`, el `melb_data` queda intocable como referencia.
- **TP1 ejercicio 1 (encoding)**: usa `select_dtypes(include="object")` para detectar candidatas a encoding y `nunique()` para decidir cuáles reducir cardinalidad antes de OHE (sobre todo `Suburb`, `SellerG`, `CouncilArea`).
- **TP1 ejercicio 2 (imputación KNN)**: agrega `YearBuilt` y `BuildingArea` y aplica `IterativeImputer`. La pregunta clave del enunciado ("¿hace falta estandarizar?") se contesta sabiendo que KNN usa distancias y por lo tanto **sí, siempre**.
- **TP2 ejercicio 1 (SQL)**: vas a usar `df.to_sql(...)` para volcar `melb_data` a SQLite. Eso requiere que los dtypes estén bien (`Date` como datetime, `Price` numérico).
- **TP2 ejercicio 2 (enriquecimiento con AirBnB)**: el patrón `groupby("zipcode").agg(...).reset_index()` + `merge(..., how="left", left_on="Postcode", right_on="zipcode")` es **literalmente** lo que vas a escribir. Y al final vas a poner las assertions post-merge.

---

## Errores comunes

1. **Saltarse el `.copy()`** y trabajar directo sobre `melb_data`. El día que tengas que volver atrás, no podés.
2. **Asumir que una columna numérica es `int64`** cuando en realidad es `float64` porque tiene NaN. `Car`, `Bedroom2`, `Bathroom` y `Postcode` en `melb_data` son `float64` por esta razón. Esto rompe muchos merges.
3. **No convertir `Date` a `datetime`** antes de filtrar o agrupar por tiempo. `melb_df["Date"] > "2017-01-01"` con `Date` como string da resultados arbitrarios (compara orden lexicográfico).
4. **Encadenar `df[df.x][["y"]] = z`**: la asignación encadenada no garantiza modificar el original. Usá siempre `df.loc[condicion, "columna"] = valor`.
5. **OneHotEncodear `Suburb` sin reducir cardinalidad**: 314 nuevas columnas, varianza absurdamente baja en cada una, y PCA dominado por ruido.
6. **Olvidar `.reset_index()` después de `groupby`**: el resultado queda con `zipcode` como índice y el `merge` por columna no encuentra la clave.
7. **No validar post-merge**: si el merge duplicó filas (porque la clave estaba duplicada en el lado derecho) y no lo asertaste, el resto del análisis está sobre un dataset inflado.

---

## Detrás de escena: por qué un int con NaN se vuelve float

Acá hay un tema que **MUCHA gente no entiende** y te muerde feo cuando pasás a producción o cuando hacés un merge en TP2 y los tipos no coinciden. Vamos por partes, porque es el origen del 80% de los bugs de "el merge me devolvió todo NaN aunque las claves matchean".

### Concepto base: NaN es un float, no un entero

NaN (en inglés *Not a Number*) es un valor especial definido por la norma **IEEE 754** de números de **punto flotante**. Es decir: vive en el universo de los floats. **No existe un "NaN entero"** en el NumPy clásico que usa pandas por debajo. Es así de fácil.

¿Por qué? Porque los enteros (`int64`, `int32`, etc.) representan **valores discretos exactos**. Cada bit cuenta. No hay un "patrón de bits" reservado para decir "esto está vacío" — los 64 bits ya están ocupados representando un número real. En cambio, los floats tienen patrones de bits reservados específicamente para `+Infinity`, `-Infinity` y `NaN`, porque la norma IEEE 754 lo dispuso así (un exponente con todos unos y mantisa distinta de cero = NaN). Por eso podés hacer `np.nan + 1` y obtener `NaN` en lugar de un error.

### Qué hace pandas cuando ve un NaN en una columna int

Pandas, cuando lee un CSV y encuentra una columna donde "casi todos" son enteros pero hay UN solo `NaN`, **promueve toda la columna a `float64`**. No te avisa. Lo hace y sigue.

```python
import pandas as pd
import numpy as np

# Sin NaN: int64
s1 = pd.Series([1, 2, 3, 4, 5])
s1.dtype                    # dtype('int64')

# Con un solo NaN: float64
s2 = pd.Series([1, 2, 3, 4, np.nan])
s2.dtype                    # dtype('float64')
s2                          # [1.0, 2.0, 3.0, 4.0, NaN]
```

Fijate la consecuencia: el `1` se convirtió en `1.0`. Si esa columna era un código postal (`Postcode = 3000`), ahora es `3000.0`. Y si la otra tabla del merge tiene `zipcode` como `int64` con valor `3000`, el merge **no matchea** porque `3000 ≠ 3000.0` cuando los dtypes son distintos.

### La solución: Int64 nullable (con I mayúscula)

Desde pandas 1.0 existe un tipo **`Int64`** (con `I` mayúscula) que SÍ admite faltantes sin promover a float. Es un "Extension dtype" de pandas, distinto del `int64` de NumPy.

```python
s3 = pd.Series([1, 2, 3, 4, np.nan], dtype="Int64")
s3.dtype                    # Int64
s3                          # [1, 2, 3, 4, <NA>]    ← enteros, con pd.NA
```

Notá dos diferencias visibles:
1. Los valores se imprimen como `1` (no `1.0`).
2. El faltante se imprime como `<NA>`, no como `NaN`. Es `pd.NA`, no `np.nan`.

| Aspecto | `int64` (minúscula, NumPy) | `Int64` (mayúscula, Pandas Extension) |
|---------|----------------------------|----------------------------------------|
| Acepta faltantes | No (se promueve a `float64`) | Sí, con `pd.NA` |
| Velocidad | Más rápido (NumPy nativo) | Un poco más lento (overhead de Pandas) |
| Compatibilidad con sklearn | Total | Parcial — algunos modelos no lo aceptan directo |
| Símbolo del faltante | `NaN` (float) | `pd.NA` (sentinel propio) |
| Operaciones aritméticas | Funcionan normal | Funcionan, propagan `pd.NA` |

### Cuándo usar cada uno

**Usá `int64` (minúscula)** cuando:
- La columna no tiene ni va a tener faltantes (claves primarias bien formadas, contadores, IDs autogenerados).
- Vas a pasarla a sklearn o numpy directo y necesitás máxima velocidad.
- Ya imputaste o eliminaste filas antes de este punto.

**Usá `Int64` (mayúscula)** cuando:
- La columna debería ser entera **conceptualmente** pero tiene faltantes (códigos postales, año de construcción, cantidad de baños).
- Vas a hacer un merge con otra tabla y la clave tiene NaN de un lado.
- Querés que `df.dtypes` te diga la verdad sobre la columna: "esto es entero, con huecos".

### La trampa típica en TP2

`melb_data["Postcode"]` viene como `float64` porque hay algunos NaN. Si querés mergearlo contra `airbnb_df["zipcode"]` que viene como `int64`, tenés dos opciones honestas:

```python
# Opción A: castear ambas a Int64 nullable (recomendado)
melb_df["Postcode"] = melb_df["Postcode"].astype("Int64")
airbnb_df["zipcode"] = airbnb_df["zipcode"].astype("Int64")

# Opción B: rellenar los NaN con un valor sentinela y castear a int64 clásico
melb_df["Postcode"] = melb_df["Postcode"].fillna(-1).astype("int64")
```

La opción A es preferible porque no inventa un valor falso (-1 no es un código postal real). La B la usás solo si vas a tirar después las filas con `-1`.

### Resumen

- `NaN` es float por definición IEEE 754. No existe un NaN entero en NumPy.
- Una sola fila con NaN promueve toda una columna `int64` a `float64`. Pandas no te avisa.
- Si te importa mantener el entero "real" (códigos, IDs, años), usá `Int64` (mayúscula).
- En merges, **siempre verificá que las claves de ambos lados tengan el MISMO dtype** antes de juntarlas. Si una es `float64` y la otra `int64`, el merge te devuelve NaN silenciosamente.

¿Se entiende? Es un detalle chico pero te salva de bugs que parecen brujería.

---

## Checklist de comprensión

- [ ] ¿Por qué la primera línea después de `pd.read_csv` debería ser `df_trabajo = df_crudo.copy()`?
- [ ] Si una columna entera tiene un solo NaN, ¿qué dtype va a tener en pandas y qué implicancia trae al hacer un merge?
- [ ] ¿Por qué tenés que hacer `groupby` + `agg` sobre AirBnB **antes** de mergearlo contra Melbourne y no al revés?
- [ ] ¿Qué diferencia hay entre `int64` y `Int64` en pandas? ¿En qué situación de TP2 conviene `Int64`?

---

**Próximo paso**: `01-introduccion-y-curacion.md`
