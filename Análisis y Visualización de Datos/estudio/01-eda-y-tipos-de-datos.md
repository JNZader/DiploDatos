# 01 — EDA y tipos de datos

## Concepto

El **EDA** (*Exploratory Data Analysis* o Análisis Exploratorio de Datos) no es una "etapa previa" al análisis real: **es** el análisis real. Es el momento en el que entendés qué mediste, cómo lo mediste, qué problemas tiene tu base y si tus datos alcanzan para responder la pregunta que te hiciste.

## Intuición

Imaginá que te dan una caja de fotos viejas de tu familia. Antes de contar cuántas fotos hay de cada vacación, primero abrís la caja, mirás si están rotas, si hay fechas escritas, si algunas son de otra familia. Eso es el EDA. No es perder tiempo: es evitar que cuentes fotos de los vecinos como si fueran tuyas.

---

## Preguntas iniciales frente a un dataset

Antes de tocar código, respondé estas preguntas en voz alta (o en papel):

1. **¿Cuál es la unidad de análisis?** ¿Cada fila es una persona, una empresa, una respuesta, un mes?
2. **¿Qué representa cada columna?** No asumas: leé el diccionario de datos o las primeras filas.
3. **¿Qué tipo de variable es cada una?** Numérica continua, numérica discreta, categórica nominal, categórica ordinal.
4. **¿Hay valores faltantes o categorías raras?** Un 30% de faltantes en una variable clave puede arruinar tu análisis.
5. **¿Qué transformación mínima necesito?** ¿Hay que separar strings? ¿Convertir tipos? ¿Unificar categorías mal escritas?
6. **¿Qué pregunta quiero responder y con qué variables?** Si tu pregunta necesita "años de experiencia" y no existe, no hay análisis que valga.

## Tipos de variables

### Cualitativas (categóricas)

- **Nominales**: categorías sin orden natural.
  - *Ejemplos de la encuesta*: provincia de trabajo, género, lenguaje de programación.
  - *Operaciones válidas*: contar frecuencias, moda, tablas de contingencia.
  - *Operaciones INVÁLIDAS*: calcular promedio (no tiene sentido "promediar" CABA + Mendoza).

- **Ordinales**: categorías con orden, pero sin distancias numéricas claras.
  - *Ejemplos de la encuesta*: nivel de estudios (Secundario < Terciario < Universitario < ...), seniority (Junior < Semi-Senior < Senior).
  - *Operaciones válidas*: contar, moda, mediana (a veces), comparar rangos.
  - *Cuidado*: la "distancia" entre Secundario y Terciario no es la misma que entre Universitario y Maestría.

### Cuantitativas (numéricas)

- **Discretas**: toman valores contables (generalmente enteros).
  - *Ejemplos*: edad en años, cantidad de personas a cargo, años de experiencia.

- **Continuas**: pueden tomar infinitos valores dentro de un rango.
  - *Ejemplos*: salario mensual neto, altura, peso.
  - *Trampa*: en la computadora todo se discretiza. El salario está en pesos, así que técnicamente es discreto, pero se modela como continuo porque hay muchos valores posibles.

### Tabla de resumen

| Tipo | ¿Tiene orden? | ¿Tiene distancia? | Ejemplo en Sysarmy |
|------|---------------|-------------------|--------------------|
| Nominal | No | No | `work_province` |
| Ordinal | Sí | No | `profile_studies_level` |
| Discreta | Sí | Sí (entre enteros) | `profile_age` |
| Continua | Sí | Sí | `salary_monthly_NETO` |

## Qué mirar en una exploración inicial

### Estructura
- Cantidad de filas y columnas: `df.shape`
- Nombres de variables: `df.columns`
- Tipos de dato: `df.dtypes` y `df.info()`

### Calidad de datos
- **Faltantes**: `df.isna().sum()`
- **Categorías inconsistentes**: `df['columna'].unique()` (¿hay "CABA", "caba" y "Capital Federal"?)
- **Valores extremos improbables**: alguien puso 1.6 pesos de salario, o 653 millones.
- **Columnas redundantes o poco útiles**: en TP1 descubriste que `salary_monthly_BRUTO` y `salary_monthly_NETO` están casi perfectamente correlacionadas (correlación de Pearson r ≈ 0.95, donde r mide la asociación lineal entre dos variables numéricas). Una es redundante.

### Potencial analítico
- ¿Existe la variable relevante para tu pregunta?
- ¿Hay suficiente cantidad de casos?
- ¿La codificación permite analizarla sin transformar demasiado?

## Ejemplo numérico

Dataset de 5 encuestados:

| ID | Edad | Salario neto | Estudios | Género |
|----|------|--------------|----------|--------|
| 1 | 28 | 850000 | Universitario | Mujer cis |
| 2 | 35 | NaN | Terciario | Varón cis |
| 3 | 42 | 1200000 | Universitario | Varón cis |
| 4 | 31 | 950000 | Secundario | Diversidades |
| 5 | 29 | 1600000 | Universitario | Mujer cis |

**Análisis EDA rápido**:
- **Unidad de análisis**: cada fila es una persona encuestada.
- **Variables**:
  - Edad: numérica discreta.
  - Salario neto: numérica continua (pero con un NaN en la fila 2).
  - Estudios: categórica ordinal.
  - Género: categórica nominal.
- **Problemas de calidad**: un salario faltante. Si queremos analizar salarios, perdemos la fila 2.
- **Potencial analítico**: con solo 5 filas no podemos inferir nada. Pero para describir, podemos calcular la media de salario de las 4 filas completas: (850000 + 1200000 + 950000 + 1600000) / 4 = 1.150.000.

---

## Conexión con el TP

- **TP1 Ejercicio 1**: antes de comparar lenguajes y salarios, hiciste exactamente esto. Miraste `shape`, `info()`, eliminaste NaN en salario y lenguaje, filtraste por `work_dedication == "Full-Time"` para no mezclar dedicaciones, y descartaste valores absurdos (< $300.000 o > $20M). Sin ese EDA, tu comparación de lenguajes habría estado contaminada por part-timers y errores de carga.
- **TP2**: repetiste el mismo EDA antes de inferir. La diferencia es que en TP2 el EDA no solo limpia: te permite verificar que ambos grupos (Varón cis y Mujer cis) tienen tamaños muestrales grandes después del filtrado, lo cual justifica el uso del TCL (Teorema Central del Límite, que veremos en detalle más adelante) y del test t (de Student, que también veremos más adelante).

---

## Errores comunes

1. **Saltar al modelo sin explorar**: querer correr un test t antes de ver si hay NaN, outliers (valores atípicos extremos) o categorías raras.
2. **Confundir tipo computacional con tipo estadístico**: que una columna sea `object` en pandas no te dice si es nominal u ordinal. Tenés que mirar los valores únicos.
3. **Ignorar el contexto de la pregunta**: si tu pregunta es "¿qué lenguaje paga más?" pero no filtrás por dedicación, estás comparando peras con manzanas.
4. **Creer que más datos siempre son mejores**: a veces un filtro razonable (como quedarse con Full-Time) mejora la calidad más que aumentar la cantidad de filas.

---

## Checklist de comprensión

- [ ] ¿Por qué en TP1 fue crucial filtrar solo `Full-Time` antes de comparar salarios por lenguaje?
- [ ] ¿Qué tipo de variable es `profile_studies_level` y por qué no podés calcularle un promedio?
- [ ] Si una columna tiene 40% de valores faltantes y es clave para tu pregunta, ¿qué decisión metodológica tenés que tomar antes de seguir?

---

**Próximo paso**: `02-probabilidad-basica.md`
