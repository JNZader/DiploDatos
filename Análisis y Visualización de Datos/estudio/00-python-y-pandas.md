# 00 — Python y pandas para análisis de datos

## Concepto

Python no es el protagonista de esta materia: es la herramienta. Pero si no sabés manejar la herramienta, no podés construir. Acá no te vamos a enseñar a programar desde cero, pero sí a entender las operaciones que vas a usar en **cada** análisis de esta diplomatura.

## Intuición

Imaginá que un DataFrame de pandas es una planilla de Excel con superpoderes. Podés filtrar, ordenar, calcular promedios, hacer gráficos y manipular millones de filas sin que se cuelgue. Pero, como en Excel, si no entendés qué hace cada fórmula, vas a terminar con conclusiones basura.

---

## Lo mínimo indispensable

### Importar librerías

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
```

Cada una tiene un rol:
- **pandas**: tablas (DataFrames) y manipulación de datos.
- **numpy**: números, vectores, operaciones matemáticas.
- **matplotlib**: gráficos de bajo nivel (la base).
- **seaborn**: gráficos estadísticos de alto nivel (más lindo y más fácil).

### Leer un dataset

```python
url = "https://raw.githubusercontent.com/DiploDatos/.../sysarmy_survey_2026_processed.csv"
df = pd.read_csv(url)
```

`pd.read_csv` lee un archivo de texto separado por comas y lo convierte en un DataFrame. Puede leer desde una URL directamente.

Otros formatos comunes:

```python
# Excel — útil cuando tus datos vienen de una planilla con varias hojas
df = pd.read_excel("archivo.xlsx", sheet_name="Hoja1")

# JSON — común en APIs y datos semi-estructurados de la web
df = pd.read_json("archivo.json")

# Parquet — formato columnar eficiente para grandes volúmenes de datos
df = pd.read_parquet("archivo.parquet")

# SQL — directo desde una base de datos relacional
# Paso 1: crear la conexión (sqlite3 viene en la stdlib, la biblioteca estándar de Python)
import sqlite3
conexion = sqlite3.connect("mi_base_de_datos.db")

# Paso 2: consultar directamente en un DataFrame
df = pd.read_sql("SELECT * FROM tabla WHERE edad > 18", conexion)

# Paso 3 (importante): cerrar la conexión cuando terminás
conexion.close()

# Nota: para bases de datos reales (PostgreSQL, MySQL, etc.) se usa
# sqlalchemy.create_engine() en vez de sqlite3.connect()
```

### Inspección inicial (las 4 preguntas básicas)

```python
df.shape          # ¿Cuántas filas y columnas? → (filas, columnas)
df.head()         # ¿Cómo se ven las primeras filas?
df.sample(5)      # Muestra 5 filas al azar (útil para ver variedad sin sesgo de orden)
df.info()         # ¿Qué tipo de dato es cada columna? ¿Hay nulos?
df.describe()     # Resumen numérico: media, mediana, min, max, etc.
```

### Tipos de datos computacionales vs estadísticos

Esto es **clave** y muchos lo pasan por alto.

| Tipo computacional (Python/pandas) | Qué representa | Ejemplo en la encuesta |
|-----------------------------------|----------------|------------------------|
| `int64` / `float64` | Números enteros o decimales | `profile_age`, `salary_monthly_NETO` |
| `object` | Texto (cualquier cosa no numérica) | `profile_gender`, `work_province` |
| `bool` | Verdadero/Falso | Una columna que creemos de sí/no |

**Trampa común**: una columna puede tener números pero estar codificada como `object` (por ejemplo, porque tiene comas o símbolos de moneda). Si no la convertís a numérica, no podés calcular la media.

```python
# Ver tipos
df.dtypes

# Forzar conversión a numérico (los errores se convierten en NaN)
df["salary"] = pd.to_numeric(df["salary"], errors="coerce")
```

### Filtrar filas

```python
# Un solo filtro
full_time = df[df["work_dedication"] == "Full-Time"]

# Varios filtros a la vez
filtrado = df[
    (df["work_dedication"] == "Full-Time") &
    (df["salary_monthly_NETO"] > 300_000) &
    (df["profile_age"] >= 18)
]
```

El `&` es "y lógico". Cada condición va entre paréntesis. Esto es equivalente a poner filtros en Excel.

### Seleccionar columnas

```python
# Una sola columna (es una Series, la estructura unidimensional de pandas)
df["salary_monthly_NETO"]

# Varias columnas (es un DataFrame más chico)
df[["salary_monthly_NETO", "profile_age", "work_seniority"]]
```

### Valores faltantes (NaN)

```python
# Contar faltantes por columna
df.isna().sum()

# Eliminar filas que tienen NaN en ciertas columnas
df_limpio = df.dropna(subset=["salary_monthly_NETO", "profile_gender"])
```

`NaN` significa "Not a Number" y representa un dato faltante. No podés calcular la media de una columna que tiene NaN sin decidir primero qué hacer con ellos.

---

## Detrás de escena: por qué un int con NaN se vuelve float

Acá hay un tema que **MUCHA gente no entiende** y te muerde feo cuando pasás a producción. Vamos por partes.

### Concepto base: NaN es un float, no un entero

NaN (Not a Number) es un valor especial definido por la norma **IEEE 754** de números de **punto flotante**. Es decir: vive en el universo de los floats. **No existe un "NaN entero"** en numpy estándar. Es así de fácil.

¿Por qué? Porque los enteros (`int64`, `int32`, etc.) representan **valores discretos exactos**. Cada bit cuenta y todos los patrones de bits están "tomados" para representar un número entero específico. No hay un patrón de bits reservado para decir "esto está vacío". En cambio, los floats tienen patrones de bits reservados para `+Infinity`, `-Infinity` y `NaN` porque la norma IEEE 754 lo dispuso así (concretamente, NaN es cualquier float con todos los bits del exponente en 1 y la mantisa distinta de 0).

### Qué hace pandas cuando ve un NaN en una columna int

Pandas no puede meter un NaN en una columna de `int64`. Entonces hace lo único que puede: **promueve toda la columna a `float64`**. Mirá esto:

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({"edad": [25, 30, np.nan, 42]})
print(df.dtypes)
# edad    float64   <-- ¡no es int64!

print(df["edad"].tolist())
# [25.0, 30.0, nan, 42.0]   <-- los 25 y 30 se volvieron 25.0 y 30.0
```

Los enteros se vuelven floats sin que vos hagas nada. Esto es silencioso, no hay warning. Y después te preguntás por qué tu `df["edad"] == 25` no matchea.

### La solución: Int64 nullable (con I mayúscula)

Pandas introdujo un tipo entero "anulable" que **sí** acepta NaN sin promover a float. La trampita: se escribe con **I mayúscula** (`Int64`), no con i minúscula (que es el tipo de numpy y NO acepta NaN).

```python
df["edad"] = df["edad"].astype("Int64")
print(df.dtypes)
# edad    Int64

print(df["edad"].tolist())
# [25, 30, <NA>, 42]   <-- enteros de verdad y <NA> en lugar de NaN
```

| Tipo | Acepta NaN | Promueve a float | Cuándo usarlo |
|------|------------|------------------|---------------|
| `int64` (numpy, i minúscula) | ❌ No | Sí, te lo cambia silencioso | Solo cuando GARANTIZÁS que no hay nulos |
| `float64` | ✅ Sí | N/A | Datos continuos (salario, peso) |
| `Int64` (pandas, I mayúscula) | ✅ Sí (como `<NA>`) | No, mantiene entero | Datos discretos que pueden tener nulos (edad, conteos) |

### Cuándo usar cada uno

- **`int64` (i minúscula)**: solo si limpiaste todos los nulos antes y querés el tipo más eficiente en memoria. Operaciones vectorizadas más rápidas.
- **`float64`**: para todo lo que sea continuo (salarios, alturas, tiempos). El NaN encaja natural.
- **`Int64` (I mayúscula)**: para enteros que **pueden** tener nulos. Edades, cantidad de hijos, años de experiencia, IDs opcionales. Acepta `<NA>` sin romper el tipo.

### La trampa típica

En TP1 cuando hacés `pd.to_numeric(df["salary"], errors="coerce")`, los errores se convierten en NaN. Si la columna tenía valores enteros con algún string mal cargado, pandas:

1. Convierte los strings a NaN.
2. **Promueve toda la columna a float64**.
3. Tu `df["salary"].dtypes` ahora dice `float64`, no `int64`.

Resultado: cuando hacés `df["salary"] == 1500000` puede fallar por comparación de float vs int, o cuando exportás a un sistema que espera enteros (una base de datos, una API), te tira error de tipo. Si querés mantener semántica entera con nulos posibles, hacé:

```python
df["salary"] = pd.to_numeric(df["salary"], errors="coerce").astype("Int64")
```

### Resumen

- NaN vive en el mundo de los floats por la norma IEEE 754.
- Un `int64` de numpy NO puede tener NaN, así que pandas promueve a `float64` sin avisar.
- Si querés enteros con posibilidad de nulos, usá `Int64` (I mayúscula) — el tipo nullable de pandas.
- En TP1/TP2 esto no te tocó directamente porque trabajaste con salarios (floats naturales), pero te va a aparecer apenas trabajes con edades, conteos o IDs.

¿Se entiende? Es un detalle chico pero te salva de bugs raros cuando los datos viajan entre pandas, numpy, bases de datos y APIs.

---

### Operaciones por grupo

```python
# Media salarial por género
df.groupby("profile_gender")["salary_monthly_NETO"].mean()

# Varias métricas a la vez
df.groupby("profile_gender")["salary_monthly_NETO"].agg(["mean", "median", "std", "count"])
```

`groupby` es una de las operaciones más poderosas. Es como una tabla dinámica de Excel: "para cada categoría, calculá X".

### Crear nuevas columnas

```python
df["descuentos"] = df["salary_monthly_BRUTO"] - df["salary_monthly_NETO"]
```

---

## Ejemplo numérico

Tenés este dataset miniatura de 5 personas:

| Nombre | Edad | Salario neto | Dedicación |
|--------|------|--------------|------------|
| Ana | 28 | 850000 | Full-Time |
| Bruno | 35 | NaN | Full-Time |
| Carla | 42 | 1200000 | Part-Time |
| Diego | 31 | 950000 | Full-Time |
| Elena | 29 | 1100000 | Full-Time |

**Pregunta**: ¿Cuál es el salario promedio de las personas Full-Time que tienen salario declarado?

```python
# Paso 1: filtrar Full-Time
ft = df[df["Dedicación"] == "Full-Time"]

# Paso 2: eliminar NaN en salario
ft_con_salario = ft.dropna(subset=["Salario neto"])

# Paso 3: calcular la media
media = ft_con_salario["Salario neto"].mean()
# Resultado: (850000 + 950000 + 1100000) / 3 = 966666.67
```

**Respuesta**: $966.667 aproximadamente.

---

## Conexión con el TP

- **TP1 Ejercicio 1**: usaste `pd.read_csv`, `dropna`, filtros por `work_dedication == "Full-Time"`, y `groupby` para calcular estadísticas por lenguaje. También usaste `.str.split(",")` (para dividir el string por comas) y `.explode()` (para convertir cada elemento de la lista resultante en una fila separada) para separar los lenguajes de programación que venían en un solo string.
- **TP2**: usaste exactamente las mismas operaciones de filtrado y limpieza antes de calcular estimaciones e intervalos de confianza. Sin estas operaciones básicas, la inferencia se construye sobre datos basura.

---

## Errores comunes

1. **No mirar `df.info()` antes de analizar**: si una columna numérica está como `object`, todas las operaciones matemáticas van a fallar o dar resultados absurdos.
2. **Filtrar en el orden equivocado**: si primero hacés `dropna` y después filtrás por grupo, podés estar eliminando filas que sí te servían para otro análisis. Siempre hacé copias (`df.copy()`).
3. **Confundir `int` con `float`**: si dividís dos enteros en Python 2, podés perder decimales. En Python 3 no pasa, pero con numpy a veces los tipos importan.
4. **Modificar el DataFrame original sin querer**: muchas operaciones de pandas devuelven una **vista**, no una copia. Si querés estar seguro, hacé `df_nuevo = df[condicion].copy()`.
5. **No entender que `object` no es lo mismo que categórica ordinal**: `object` es un tipo computacional. Que una variable sea `object` no te dice si sus categorías tienen orden o no.

---

## Checklist de comprensión

- [ ] ¿Podés explicar la diferencia entre `object` y `float64` en pandas?
- [ ] ¿Qué pasa si intentás calcular la media de una columna que tiene NaN y no usás `dropna`?
- [ ] ¿Por qué en TP1 tuviste que usar `.explode()` con la columna de lenguajes de programación?

---

**Próximo paso**: `01-eda-y-tipos-de-datos.md`
