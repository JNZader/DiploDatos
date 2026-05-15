# 07 — Limpieza y calidad de datos

## Concepto

Los datos del mundo real están sucios. Siempre. La limpieza no es una tarea técnica menor: es una **decisión metodológica** que define sobre qué muestra vas a inferir. Cambiar un criterio de limpieza puede cambiar tu conclusión.

## Intuición

Imaginá que vas a cocinar para 20 personas. Antes de empezar, revisás los ingredientes: algunas verduras están podridas, el aceite venció, y hay un par de especias que no sabés qué son. La limpieza es decidir qué tirás, qué lavás, y qué dejás afuera de la receta. Si cocinás con todo tal como viene, el plato puede ser veneno.

---

## Tipos de problemas de calidad

### 1. Valores faltantes (NaN, null, en blanco)

- **Causas**: el encuestado no respondió, el dato se perdió en la carga, la pregunta no aplicaba.
- **Impacto**: si eliminás todas las filas con algún NaN, podés perder mucha información. Si imputás (rellenás con la media), podés inventar estructura falsa.
- **Estrategia en esta materia**: la más conservadora es `dropna(subset=[columnas_clave])` — eliminar solo las filas que no tienen la información indispensable para tu pregunta.

### 2. Valores absurdos (errores de dominio)

Son valores que violan reglas del mundo real:
- Salario neto = $1.60 (error de tipeo).
- Salario neto = $653.000.000 (imposible en Argentina).
- Edad = 150 años.

**Estrategia**: definir rangos plausibles por conocimiento de dominio.

**Ejemplo numérico (TP1 y TP2)**:
```python
salary_min = 300_000    # Salario mínimo razonable en Argentina 2026
salary_max = 20_000_000 # Más que esto es muy improbable
```

### 3. Valores extremos (outliers)

Son valores que estadísticamente quedan lejos del resto. Pueden ser:
- **Errores**: un tipeo de $5.000.000 en lugar de $500.000.
- **Observaciones reales pero extremas**: un CTO que gana $8.000.000 neto.

**La decisión de eliminarlos depende del objetivo**:
- Si querés describir la "típica" experiencia, eliminar outliers puede ayudar.
- Si querés detectar fraude, los outliers son lo más importante.

**Métodos de detección**:

#### Percentiles
Quedarse con el 99% central (eliminar el 1% más extremo).

#### IQR (Rango Intercuartílico)
El criterio clásico de los boxplots:

$$
\text{Límite inferior} = Q1 - 1.5 \times IQR \\
\text{Límite superior} = Q3 + 1.5 \times IQR
$$

**Ejemplo numérico**:
Salarios ordenados (en miles): 400, 500, 600, 700, 800, 900, 1000, 2000, 5000.

- Q1 (percentil 25) = 600.
- Q3 (percentil 75) = 1000.
- IQR = 1000 − 600 = 400.
- Límite inferior = 600 − 1.5×400 = 0.
- Límite superior = 1000 + 1.5×400 = 1600.

**Outliers**: el valor 5000 queda por encima de 1600, así que se detecta como outlier.

**En TP1 y TP2 aplicaste exactamente esto**:
```python
Q1 = df["salary_monthly_NETO"].quantile(0.25)
Q3 = df["salary_monthly_NETO"].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
```

#### Desvío estándar
Quedarse con datos dentro de k desvíos de la media (típicamente k = 2.5 o 3).

**Cuidado**: este método **no es robusto** porque la media y el desvío se ven afectados por los propios outliers.

### Por qué IQR con datos contaminados arrastra outliers legítimos

Acá hay una trampa que **te muerde sí o sí en TP1 y TP2 si no entendés la mecánica**. El IQR parece "objetivo" porque usa cuartiles, pero el orden en que aplicás las limpiezas cambia qué considera outlier.

#### Concepto base: el IQR no es magia, es un cálculo sobre los datos QUE LE PASES

El IQR se calcula como Q3 - Q1. Si tu dataset incluye absurdos extremos (un salario de $653.000.000 por error de carga, o salarios de $1 por error en la unidad), estos valores **NO** afectan directamente el Q1 ni el Q3 (porque los cuartiles son robustos, viste el `breakdown point` antes). Pero sí afectan **la dispersión que mide el IQR**.

Esto suena raro. Vamos con cuentas.

#### El experimento numérico: dataset contaminado

Imaginate los salarios mensuales de 10 trabajadores IT. La gran mayoría es razonable, hay un valor anómalo extremo (error de carga, alguien puso bruto anual en la celda de neto mensual):

```
350.000, 600.000, 800.000, 950.000, 1.100.000, 1.300.000, 1.500.000, 1.800.000, 2.500.000, 200.000.000
```

Aplicamos IQR directo:

- Q1 (percentil 25) ≈ 837.500
- Q3 (percentil 75) ≈ 1.725.000
- IQR = 1.725.000 - 837.500 = **887.500**
- Límite superior = Q3 + 1.5 × IQR = 1.725.000 + 1.331.250 = **3.056.250**

¿Qué pasa? El valor de 200.000.000 obviamente se marca como outlier (bien). Pero el valor de **2.500.000** (que es un salario PERFECTAMENTE PLAUSIBLE para un senior en una multinacional) **también** queda fuera porque supera el límite de 3.056.250... esperá, no lo supera. Veamos otro ejemplo donde sí pasa.

#### El caso de contaminación bilateral

Ahora supongamos que tenés ruido en ambos extremos: errores de tipeo que metieron $1 y $5, y errores de carga que metieron $200M:

```
1, 5, 350.000, 600.000, 800.000, 950.000, 1.100.000, 1.300.000, 1.500.000, 1.800.000, 2.500.000, 200.000.000
```

- Q1 (percentil 25) ≈ 537.500 (más bajo por los $1 y $5 que empujan la cola izquierda)
- Q3 (percentil 75) ≈ 1.575.000 (más alto porque el 200M empuja el rango)
- IQR = 1.575.000 - 537.500 = **1.037.500**
- Límite superior = 1.575.000 + 1.5 × 1.037.500 = **3.131.250**
- Límite inferior = 537.500 - 1.5 × 1.037.500 = **-1.018.750** (se vuelve negativo)

El IQR se "infló" porque los datos contaminados estiraron Q1 hacia abajo y Q3 hacia arriba. Resultado: el límite superior es generoso (deja pasar 2.5M y 3M), pero también deja pasar **muchos** valores que vos considerarías sospechosos. Y peor: el límite inferior tan extendido NO te limpia los $1 y $5.

#### El problema del breakdown bilateral

El IQR tiene un breakdown point de **25%** (puede aguantar hasta 25% de contaminación en cada cola antes de "romperse"). Pero si los datos están **muy** contaminados en una sola cola, el cuartil de esa cola se desplaza, infla el IQR, y entonces el criterio "1.5 × IQR" se vuelve laxo. Outliers legítimos pasan el filtro, y por el otro lado, valores razonables en la cola opuesta pueden quedar marcados como outliers.

#### La solución: limpiar A OJO ANTES de aplicar IQR

Acá viene la decisión metodológica clave de los TPs. El pipeline correcto es:

1. **Primero, filtrar por dominio**: definir rangos plausibles con conocimiento del problema.
   ```python
   salary_min = 300_000     # Por debajo es imposible o error de carga
   salary_max = 20_000_000  # Por arriba es estadísticamente posible pero muy raro
   df = df[(df["salary"] >= salary_min) & (df["salary"] <= salary_max)]
   ```

2. **Después, aplicar IQR sobre los datos YA limpios** para detectar outliers estadísticos en una distribución que ahora es razonable.

¿Por qué este orden? Porque al aplicar el filtro por dominio primero, eliminás los absurdos que distorsionan el cálculo del IQR. Los cuartiles que calculás después son **representativos de la distribución real**, no de un dataset contaminado.

#### Tabla comparativa: orden de operaciones

| Orden | Resultado |
|-------|-----------|
| IQR primero, dominio después | El IQR se calcula con datos contaminados; outliers legítimos pasan el filtro; el dominio limpia lo absurdo pero ya perdiste filas razonables |
| Dominio primero, IQR después | Los cuartiles representan la distribución real; el IQR captura outliers estadísticos genuinos; tu muestra final es coherente |

La segunda opción es lo que hiciste en TP1 y TP2. **Y por eso funcionó**.

#### La trampa típica: confiar ciegamente en IQR

Hay gente que aplica IQR a TODO sin mirar los datos. "Es un método objetivo", dicen. **No lo es**. El IQR es un cálculo determinístico, sí, pero el resultado depende totalmente de qué entrada le des. Si le metés datos sucios, sale resultado sucio. Garbage in, garbage out.

Por eso en TP1 y TP2 vos primero **mirabas un histograma o un boxplot inicial**, identificabas valores absurdos, los filtrabas por dominio, y RECIÉN AHÍ aplicabas IQR. Ese paso de "mirar a ojo primero" no es opcional. Es lo que separa al análisis honesto del análisis automatizado y ciego.

#### Cuándo aplicar IQR directo (sin pre-limpieza)

- Cuando confiás en que los datos vienen limpios (datos sintéticos, de un proceso bien controlado).
- Cuando el objetivo es detectar precisamente esos absurdos como anomalías (auditoría, detección de fraude).
- Cuando tenés un dataset homogéneo donde no esperás errores de carga.

En cualquier otro caso, **filtrá por dominio primero**.

#### Resumen

- El IQR tiene breakdown point del 25%, pero datos muy contaminados igual lo distorsionan.
- Si Q1 y Q3 se "estiran" por outliers extremos, el límite 1.5×IQR se vuelve laxo y deja pasar lo que no debería.
- Pipeline correcto: filtro por dominio (conocimiento del problema) → IQR (criterio estadístico).
- "Limpiar a ojo" NO es trampa: es una decisión metodológica informada que mejora el resultado posterior.

¿Se entiende? Cuando un método estadístico parece "objetivo", revisá siempre QUÉ datos le estás dando. La objetividad del método no compensa la contaminación de la entrada.

### 4. Categorías inconsistentes

**Ejemplo**: en la columna de género, la encuesta de 2023 tuvo troleo con respuestas como "Helicóptero Apache". En la de 2026, hay categorías como "Varón Cis", "Varón cis", "Mujer", "Mujer Cis", "Femenino".

**Estrategia**: recodificar en categorías limpias antes de analizar.

```python
gender_map = {
    "Varón Cis": "Varón cis",
    "Mujer Cis": "Mujer cis",
    "Mujer": "Mujer cis",
    "Femenino": "Mujer cis",
    # etc.
}
df["profile_g"] = df["profile_gender"].replace(gender_map)
```

### 5. Duplicados y redundancias

En TP1 descubriste que `salary_monthly_BRUTO` y `salary_monthly_NETO` tienen correlación r ≈ 0.95. Eso significa que una variable es prácticamente redundante. No es un "problema de calidad" en sí, pero es una decisión analítica: ¿necesitás ambas?

---

## Pipeline de limpieza de TP1 y TP2

Ambos trabajos siguieron el mismo pipeline, que es un buen patrón para reutilizar:

1. **Seleccionar columnas relevantes**: no cargues todo el dataset en memoria si solo necesitás 4 columnas.
2. **Eliminar NaN en variables clave**: si tu pregunta depende de salario y género, descartá filas que no tengan eso.
3. **Filtrar por dominio**: salarios dentro de un rango plausible, edades razonables.
4. **Filtrar por categoría de interés**: en TP2, quedarse solo con "Varón cis" y "Mujer cis".
5. **Controlar confusores básicos**: en ambos TPs, filtrar por `work_dedication == "Full-Time"` para no mezclar cargas horarias.
6. **Remover outliers por IQR**: para trabajar con una muestra más robusta frente a valores extremos.

**Ejemplo numérico del impacto de la limpieza** (valores aproximados de TP2):
- Filas iniciales: ~6.500.
- Después de eliminar NaN: ~5.800.
- Después de filtrar Full-Time: ~4.200.
- Después de filtrar salarios absurdos: ~4.000.
- Después de IQR: ~3.400.

**Mensaje**: perdiste casi la mitad de las filas, pero ganaste comparabilidad y robustez.

---

## Sesgos de la encuesta

La encuesta Sysarmy es **observacional** (no manipulamos variables, solo observamos lo que ya existe) **y voluntaria**. Eso introduce al menos tres sesgos que no se eliminan con limpieza:

1. **Autoselección**: responde quien decide participar. Puede sobrerrepresentar ciertos perfiles (por ejemplo, personas más comprometidas con la comunidad).
2. **Subcobertura**: algunos segmentos del mercado IT pueden estar subrepresentados (por ejemplo, trabajadores de empresas que no difunden la encuesta).
3. **Autorreporte**: salario, rol y dedicación dependen de lo que cada persona declara. Puede haber error de memoria, redondeo o incluso exageración.

**Consecuencia**: incluso cuando aplicás inferencia clásica, la generalización al "mercado IT completo" debe hacerse con cautela. La muestra no es una muestra aleatoria perfecta.

---

## Conexión con el TP

- **TP1 Ejercicio 1**: definiste `salary_min = 300_000` y `salary_max = 20_000_000` por conocimiento de dominio. Luego aplicaste IQR. Cada paso lo justificaste en el texto: "eliminamos errores obvios, luego outliers estadísticos".
- **TP1 Ejercicio 1 (explode)**: la columna de lenguajes venía como string separado por comas. Tuviste que hacer `.str.split(",")` y `.explode()` para analizar cada lenguaje por separado. Eso es limpieza de formato.
- **TP2**: repetiste exactamente el mismo pipeline de limpieza, pero agregaste el filtro de género y explicitaste que la validez de la inferencia depende de "sobre qué muestra" se razona.
- **TP2 Ejercicio 3 (alcance poblacional)**: incluiste una sección sobre autoselección, subcobertura y autorreporte como limitaciones metodológicas.

---

## Errores comunes

1. **Limpiar sin justificar**: cada decisión de limpieza debe tener una razón escrita. "Eliminé outliers" no alcanza: ¿con qué criterio? ¿por qué?
2. **Aplicar IQR antes de filtrar por dominio**: si hay valores de $1 y $653M, el IQR se distorsiona. Primero filtrá lo absurdo, después aplicá IQR.
3. **Eliminar outliers automáticamente en todos los análisis**: si tu pregunta es "¿quiénes son los mejores pagos?", los outliers son tu objeto de estudio, no basura.
4. **Ignorar el sesgo de selección**: la limpieza mejora la calidad interna de la muestra, pero no elimina el hecho de que sea una encuesta voluntaria.
5. **No documentar el pipeline**: si no dejás escrito el criterio, nadie (ni vos en un mes) puede reproducir tu análisis.

---

## Checklist de comprensión

- [ ] ¿Por qué en TP1 y TP2 filtraste por `work_dedication == "Full-Time"` antes de cualquier otro análisis?
- [ ] Si un valor de salario es de $50.000.000 pero la persona dice ser "Senior Manager en una multinacional", ¿lo eliminás automáticamente o lo investigás?
- [ ] ¿Qué sesgos de la encuesta Sysarmy persisten incluso después de una limpieza perfecta?

---

**Próximo paso**: `08-formulario.md`
