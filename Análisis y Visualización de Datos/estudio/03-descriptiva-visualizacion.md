# 03 — Estadística descriptiva y visualización exploratoria

## Concepto

La estadística descriptiva resume y organiza datos observados. No prueba nada ni extrapola a una población: simplemente te dice "así se ven tus datos". Pero "simplemente" es una palabra engañosa: un buen resumen descriptivo puede revelar patrones que luego justifican toda una línea de inferencia.

## Intuición

Imaginá que tenés una bolsa con 10.000 caramelos de distintos sabores. No podés mirar cada caramelo. Entonces contás cuántos hay de cada sabor (frecuencias), buscás el sabor más común (moda), calculás el peso promedio (media), y te fijás si hay algún caramelo gigante o enano (dispersión). Eso es descriptiva.

---

## Medidas de tendencia central

Son "resúmenes de una sola cifra" que intentan representar el "centro" de los datos.

### Media (promedio aritmético)

$$
\bar{x} = \frac{1}{N} \sum_{i=1}^{N} x_i
$$

**Intuición**: la media es el **centro de masa** del histograma. Si el histograma fuera una figura de madera, la media es el punto donde podrías apoyarlo y no se cae.

**Ejemplo numérico**:
Salarios de 5 personas: $800.000, $900.000, $950.000, $1.000.000, $2.000.000.

Media = (800 + 900 + 950 + 1000 + 2000) / 5 = 5.650 / 5 = **$1.130.000**.

**Trampa**: ese $2.000.000 "tira" la media hacia arriba. La mayoría gana menos de $1.130.000.

### Mediana

Ordenás los datos y tomás el valor central (o el promedio de los dos centrales si N es par).

**Ejemplo numérico** (mismos datos ordenados):
$800.000, $900.000, **$950.000**, $1.000.000, $2.000.000.

Mediana = **$950.000**.

**Por qué importa**: la mediana es **robusta** a valores extremos. Si el dueño de la empresa se suma a la encuesta y gana $50.000.000, la media se dispara a $8.275.000, pero la mediana sigue siendo $950.000.

### Moda

El valor más frecuente. Útil para variables categóricas.

**Ejemplo**: en la encuesta Sysarmy, la moda de `profile_gender` suele ser "Varón cis" porque es la categoría más frecuente.

### Cuándo usar cada una

| Medida | Usala cuando... | Evitala cuando... |
|--------|----------------|-------------------|
| Media | La distribución es simétrica y no hay outliers | Hay colas largas o valores extremos |
| Mediana | Hay asimetría o outliers | Necesitás una medida que reaccione a cambios en todos los valores |
| Moda | Variables categóricas o discretas con pocos valores | Variables continuas (cada valor aparece una vez) |

### Por qué la media es vulnerable a outliers y la mediana no

Acá hay un concepto que **mucha gente repite de memoria sin entender la mecánica**. Vamos a verlo con cuentas.

#### Concepto base: cómo se construye cada una

La **media** se calcula sumando todos los valores y dividiendo por N. Esto significa que **cada valor contribuye a la suma con su magnitud completa**. Un valor 100 veces más grande que el resto, "pesa" 100 veces más en la suma. Esa es exactamente la vulnerabilidad.

La **mediana** se calcula **ordenando** los datos y agarrando el del medio. La magnitud del valor extremo **no importa**: solo importa su **posición** en el orden. Que el último valor sea 5 millones o 500 millones es lo mismo para la mediana: sigue siendo el último.

#### El experimento del millonario en la sala

Tenés una sala con 9 trabajadores IT cobrando salarios típicos:

```
800, 850, 900, 950, 1000, 1050, 1100, 1150, 1200  (en miles de pesos)
```

- **Media** = (800 + 850 + ... + 1200) / 9 = 9000 / 9 = **$1.000.000**.
- **Mediana** = el valor del medio (posición 5) = **$1.000.000**.

Las dos coinciden. La distribución es simétrica, no hay sorpresa.

Ahora entra Mark Zuckerberg a la sala. Su salario mensual es, digamos, $1.000.000.000 (mil millones). Recalculemos:

```
800, 850, 900, 950, 1000, 1050, 1100, 1150, 1200, 1.000.000.000
```

- **Nueva media** = (9.000 + 1.000.000.000) / 10 = 1.000.009.000 / 10 ≈ **$100.000.900**.
- **Nueva mediana** = promedio de las posiciones 5 y 6 = (1000 + 1050) / 2 = **$1.025.000**.

¿Ves lo que pasó? La media **se multiplicó por 100**. La mediana se movió un 2.5%. La media te diría "el salario típico de esta sala es 100 millones", lo cual es una mentira descarada: 9 de las 10 personas ganan menos de 1.5 millones.

#### El concepto técnico: punto de ruptura

En estadística esto se llama **breakdown point** (punto de ruptura). Mide qué proporción de valores extremos puede aguantar un estimador antes de "romperse" (dar resultados arbitrariamente malos).

| Estimador | Breakdown point | Qué significa |
|-----------|----------------|---------------|
| Media | 0% | Con UN solo valor lo suficientemente grande, la media se va a cualquier lado |
| Mediana | 50% | Hasta que el 50% de los datos sea contaminado, la mediana se mantiene cerca del centro real |
| Media recortada al 10% | 10% | Aguanta hasta 10% de contaminación |

La mediana tiene el **breakdown point más alto posible** para un estimador de centro. Eso es lo que se llama un estimador **robusto**.

#### Por qué importa en datos reales

Tu dataset Sysarmy tiene salarios que van de $100.000 a $50.000.000 (rangos absurdos por errores de carga incluidos). La distribución de salarios tiene **cola derecha pesada**: pocos cargos directivos cobran muchísimo más que la mediana. Si reportás "el salario promedio en IT es X" usando la media sin filtrar, ese X va a estar inflado por los outliers.

En cambio: "la mediana salarial en IT es Y" describe al **trabajador típico** (el que está en el medio del orden). Esa es la cifra que usan los medios serios cuando hablan de ingresos.

#### Cuándo SÍ querés la media

- Cuando la distribución es simétrica (alturas, errores de medición física).
- Cuando los outliers son **objeto de interés** (estás analizando fraude, eventos raros).
- Cuando necesitás que el estimador reaccione a **todos** los valores (por ejemplo, calcular un total esperado).

#### La trampa típica en el TP

En TP1 Ejercicio 1 (Opción B) reportaste media, mediana, Q1, Q3 por lenguaje. Si miraste solo la media, lenguajes con un par de salarios atípicos (un director que sabe COBOL, por ejemplo) te aparecían "altos". Por eso ordenaste los lenguajes **por mediana**, no por media. La mediana te daba el ranking del "programador típico" de cada stack. La media te daba el ranking distorsionado por los cargos de dirección.

#### Resumen

- Media usa magnitudes; un valor enorme la arrastra arbitrariamente.
- Mediana usa posiciones; un valor enorme sigue siendo "el último" y aporta lo mismo que cualquier otro.
- Breakdown point: media = 0%, mediana = 50%.
- En distribuciones asimétricas (como salarios), reportá mediana o reportá las dos.

¿Se entiende? Cuando alguien te diga "el salario promedio es X", preguntá siempre: ¿media o mediana? Si dudan, ya sabés la respuesta.

---

## Medidas de dispersión

Dos grupos pueden tener la misma media y ser completamente distintos. La dispersión te dice "qué tan esparcidos están los datos".

### Varianza muestral

$$
s^2 = \frac{1}{N-1} \sum_{i=1}^{N} (x_i - \bar{x})^2
$$

**Intuición**: promedio de las distancias al cuadrado entre cada dato y la media. Usamos $N-1$ (no $N$) porque es un estimador insesgado de la varianza poblacional.

**Ejemplo numérico**:
Datos: 2, 4, 6, 8, 10. Media = 6.

- $(2-6)^2 = 16$
- $(4-6)^2 = 4$
- $(6-6)^2 = 0$
- $(8-6)^2 = 4$
- $(10-6)^2 = 16$

Suma = 40. Varianza = 40 / 4 = **10**.

### Desvío estándar

$$
s = \sqrt{s^2}
$$

Es la raíz cuadrada de la varianza. Tiene las mismas unidades que los datos originales, así que es más interpretable.

En el ejemplo: $s = \sqrt{10} \approx$ **3.16**.

### Coeficiente de variación (CV)

$$
CV = \frac{s}{\bar{x}}
$$

**Intuición**: dispersión relativa. Te permite comparar la "variabilidad" de dos variables que tienen escalas distintas.

**Ejemplo numérico**:
- Salario bruto: media = $1.500.000, desvío = $300.000 → CV = 0.20 (20%).
- Edad: media = 32 años, desvío = 6 años → CV = 0.19 (19%).

Aunque el desvío del salario sea mucho mayor en pesos, la variabilidad *relativa* es similar a la de la edad.

### Percentiles, cuartiles e IQR

- **Percentil k**: el valor debajo del cual cae el k% de los datos.
- **Q1 (percentil 25)**: el 25% de los datos está por debajo.
- **Q2 (percentil 50)**: la mediana.
- **Q3 (percentil 75)**: el 75% de los datos está por debajo.
- **IQR** = Q3 - Q1: el "ancho" del 50% central de los datos.

**Ejemplo numérico**:
Salarios ordenados de 8 personas (en miles): 400, 500, 600, 750, 900, 1000, 1200, 5000.

- Q1 (percentil 25) = 550 (promedio de 500 y 600).
- Q2 (mediana) = 825 (promedio de 750 y 900).
- Q3 (percentil 75) = 1100 (promedio de 1000 y 1200).
- IQR = 1100 - 550 = **550**.

El IQR es robusto: si cambiamos el $5.000.000 por $10.000.000, el IQR no se mueve.

---

## Gráficos exploratorios

### Histograma

Muestra la forma general de la distribución: ¿dónde se concentran los datos? ¿Hay colas? ¿Es simétrica?

**Trampa**: la forma depende de la cantidad de "bins" (intervalos). Con pocos bins todo parece uniforme; con muchos, todo parece ruido.

### Boxplot (diagrama de caja)

Resume en un dibujo:
- Línea central = mediana.
- Caja = Q1 a Q3 (IQR).
- Bigotes = típicamente Q1 - 1.5×IQR y Q3 + 1.5×IQR.
- Puntos fuera = valores atípicos (outliers).

**Ventaja**: comparar muchos grupos rápidamente.
**Desventaja**: oculta la forma de la distribución (no sabés si es bimodal, es decir, si tiene dos picos o modas).

### Violinplot

Combina boxplot + estimación de densidad (KDE, del inglés *Kernel Density Estimation*, una forma de suavizar un histograma para ver la forma de la distribución). El "ancho" del violín indica dónde hay más datos.

**Ventaja**: veo la forma completa.
**Desventaja**: con muchos grupos se vuelve denso.

### Scatterplot (gráfico de dispersión)

Cada punto es una observación. El eje X es una variable, el eje Y es otra.

**Uso**: detectar asociaciones entre variables numéricas. Si los puntos suben de izquierda a derecha, hay correlación positiva.

### Heatmap de correlación

Matriz cuadrada donde cada celda muestra la correlación entre dos variables numéricas.

---

## Relaciones entre variables

### Correlación no implica causalidad

Que dos variables se muevan juntas no significa que una cause a la otra.

- **Confusor**: una tercera variable afecta a ambas. Ejemplo: el tama del helado vendido y la cantidad de ahogados están correlacionados porque ambos dependen de la temperatura.
- **Causalidad inversa**: A "cause" B, pero en realidad B causa A.
- **Relación espuria**: pura casualidad.

### Marginal vs condicional

Una relación puede desaparecer o invertirse cuando condicionás por otra variable.

**Ejemplo numérico**:
Sin condicionar: los que saben Java cobran más que los que saben Python en promedio.
Condicionado a Seniority: entre seniors, Python paga más. Entre juniors, Java paga más. La relación marginal mezclaba niveles de experiencia distintos.

Esto es la **paradoja de Simpson** y aparece constantemente en datos reales.

---

## Conexión con el TP

- **TP1 Ejercicio 1**: comparaste distribuciones salariales por lenguaje usando **boxplot** (para ver medianas y dispersión), **violinplot** (para ver la forma), y **KDE** (para superponer curvas de densidad). Ordenaste los lenguajes por mediana para que la lectura visual fuera inmediata.
- **TP1 Ejercicio 1, Opción B**: calculaste media, mediana, desvío, Q1, Q3, P90 (percentil 90), skewness (asimetría de la distribución) y CV por lenguaje. Descubriste que la mediana ordenaba distinto que la media en algunos casos, lo cual revelaba asimetrías.
- **TP1 Ejercicio 2a**: usaste **pairplot** (matriz de scatterplots de seaborn) para cruzar todas las variables numéricas y **heatmap** para ver correlaciones de Pearson. Descubriste que bruto y neto tienen r ≈ 0.95.
- **TP1 Ejercicio 2c**: comparaste histogramas condicionales (salario según nivel de estudio) y calculaste medidas descriptivas por subpoblación.
- **TP1 Ejercicio 2d**: usaste **scatterplot con hue** (parámetro de seaborn que colorea los puntos según una variable categórica) para ver la relación edad-salario condicionada por seniority.
- **TP2**: antes de inferir, hiciste descriptivos básicos de los grupos A y B para verificar que ambos tenían tamaños muestrales grandes y para interpretar luego el intervalo de confianza en contexto.

---

## Errores comunes

1. **Mirar solo la media**: un promedio sin dispersión dice poco. Dos grupos pueden tener la misma media y distribuciones completamente distintas.
2. **Confundir desvío estándar con error estándar**: el desvío mide la dispersión de los **datos individuales**; el error estándar mide la variabilidad del **promedio muestral** (lo vemos en `04-estimacion`).
3. **Eliminar outliers automáticamente**: un outlier puede ser un error de carga o una observación real pero extrema. La decisión de eliminarlo debe depender del objetivo del análisis y de la variable.
4. **Usar correlación de Pearson con datos no lineales**: Pearson mide relación **lineal**. Si la relación es curva (por ejemplo, edad vs salario: sube y después se estabiliza), Pearson puede dar ≈ 0 aunque haya una asociación clara. Para eso existe Spearman (correlación de rangos de Spearman, que detecta relaciones monotónicas).
5. **Interpretar un boxplot sin mirar el tamaño de grupo**: una mediana alta en un grupo de 10 personas es mucho menos confiable que en un grupo de 1000.

---

## Checklist de comprensión

- [ ] ¿Por qué en TP1 ordenaste los lenguajes por mediana y no por media?
- [ ] Si dos grupos tienen la misma media pero distinto IQR, ¿qué podés decir sobre sus distribuciones?
- [ ] ¿Por qué el pairplot de TP1 mostró que bruto y neto están correlacionados, pero eso no significa que uno "cause" al otro en sentido de intervención?

---

**Próximo paso**: `04-estimacion-e-inferencia.md`
