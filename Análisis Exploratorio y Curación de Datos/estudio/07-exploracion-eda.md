# 07 — Análisis Exploratorio de Datos (EDA)

## Concepto

El **Análisis Exploratorio de Datos (EDA)** es la primera mirada sistemática sobre un dataset. No es modelado, no es inferencia: es entender qué tenés en las manos antes de tomar cualquier decisión de curación o de feature engineering. La cátedra lo define así:

> *"Análisis exploratorio inicial. Identificar patrones y relaciones significativas. Estadística descriptiva."*

Y aclara por qué importa:

> *"El EDA no es un fin en sí mismo: sirve para decidir qué columnas conservamos, cuáles descartamos y qué transformaciones necesitamos antes de modelar."*

Las tres preguntas guía que estructuran cualquier EDA son:

1. **¿Qué variables hay?** (tipos, escalas, codificación, faltantes).
2. **¿Qué distribución tienen?** (forma, centro, dispersión, colas, asimetría).
3. **¿Cómo se relacionan entre sí?** (correlaciones, cruces categórica-numérica, target vs predictoras).

## Intuición

Pensá en EDA como abrir una caja de fotos antiguas que heredaste y nunca miraste. Antes de armar un álbum (modelo), te sentás en el piso y vas viendo foto por foto: cuántas hay, de qué años son, cuáles están rotas, cuáles repetidas, qué personas aparecen más, qué historias se conectan. Recién después de esa primera mirada sabés qué incluir, qué descartar y cómo ordenar el álbum.

Si saltás esta etapa, vas a terminar imputando ceros que en realidad eran faltantes enmascarados, eliminando outliers que eran datos legítimos, o construyendo un modelo que predice usando una variable que en producción no vas a tener.

Otra analogía útil de la cátedra:

> *"Elegir features para un modelo es una decisión muy parecida a diseñar el contexto de un LLM: demasiada información irrelevante agrega ruido."*

---

## Las 7 etapas del EDA (en orden)

La cátedra propone un recorrido estandarizado. El orden importa porque cada paso depende del anterior.

| # | Etapa                              | Qué hacés                                                        | Herramientas                            |
|---|------------------------------------|------------------------------------------------------------------|-----------------------------------------|
| 1 | Primer vistazo                     | Forma del dataset, tipos, nulos rápidos                          | `info()`, `shape`, `dtypes`             |
| 2 | Resumen de numéricas               | Estadísticos: media, mediana, mín, máx, percentiles              | `describe()`                            |
| 3 | Faltantes                          | Cuántos, en qué columnas, qué patrón siguen                      | `isnull().sum()`, missingno             |
| 4 | Distribución                       | Forma de cada variable: simétrica, sesgada, multimodal           | histplot, boxplot                       |
| 5 | Categóricas y precio (target)      | Frecuencias y relación con la variable objetivo                  | `value_counts()`, boxplot por categoría |
| 6 | Relaciones entre variables         | Correlaciones cruzadas                                           | heatmap                                 |
| 7 | Qué dice la matriz                 | Interpretar: feature selection, redundancias, sospechas          | ranking de correlaciones                |

**Bonus**: fechas (parsear y graficar estacionalidad) + outliers (tres técnicas combinadas).

### Lo que la cátedra NO usa en esta materia

Importante para no confundirse con AVD:

- **No** se usan tests de normalidad (Shapiro-Wilk, KS).
- **No** se usan tablas de contingencia con chi-cuadrado.
- **No** se usa pairplot (caro y poco informativo en datasets grandes).
- **No** se usa z-score para outliers; se prefiere IQR.

El EDA acá es **visual + descriptivo**, no inferencial.

---

## Etapa 1 — Primer vistazo

```python
import pandas as pd
melb_df = pd.read_csv('https://cs.famaf.unc.edu.ar/~mteruel/datasets/diplodatos/melb_data.csv')

melb_df.info()      # filas, columnas, dtypes, nulos por columna
melb_df.shape       # (13580, 21)
melb_df.dtypes      # tipos pandas (object, int64, float64)
melb_df.head()
```

Acá lo importante NO es el código sino lo que mirás:

- ¿Cuántas filas y columnas? ¿Tiene sentido el tamaño?
- ¿Hay columnas `object` que deberían ser numéricas? (Indica problemas de parseo.)
- ¿Hay columnas con muchísimos nulos? (Candidatas a eliminar o imputar agresivamente.)
- ¿Las fechas vienen como `object`? (Casi siempre sí; hay que parsearlas.)

---

## Etapa 2 — Análisis univariado de numéricas

```python
melb_df.describe()
```

`describe()` te da media, desvío, mín, Q1, mediana, Q3, máx. Lo que tenés que detectar:

1. **Rangos desproporcionados**: si la media de `Landsize` es 558 pero el máximo es 433.014, hay outliers gravísimos.
2. **Asimetría**: si `media > mediana`, la distribución está sesgada a la derecha (cola larga de valores altos). Si `media < mediana`, sesgada a la izquierda. En precios inmobiliarios la asimetría a la derecha es la regla.
3. **Mínimos imposibles**: `BuildingArea == 0` no es una superficie de cero metros cuadrados; es un faltante enmascarado.

### Visualización: histplot + boxplot

```python
import seaborn as sns
import matplotlib.pyplot as plt

sns.histplot(melb_df.Price.dropna())
plt.ticklabel_format(style='plain', axis='x')   # evita notación científica
plt.show()

sns.boxplot(x=melb_df.Price)
plt.show()
```

El histograma te muestra la **forma**; el boxplot te muestra **mediana, IQR y outliers** de un golpe. Usalos juntos: el histograma sin boxplot no te marca outliers; el boxplot sin histograma no te muestra si la distribución es bimodal.

---

## Etapa 3 — Análisis univariado de categóricas

```python
cats = melb_df.select_dtypes(include='object').columns

resumen_cat = pd.DataFrame({
    'columna': cats,
    'cantidad_categorias': [melb_df[c].nunique(dropna=True) for c in cats],
    'nulos': [melb_df[c].isnull().sum() for c in cats],
}).sort_values('cantidad_categorias', ascending=False)
```

Lo que descubrís en Melbourne:

- `Suburb`: cientos de categorías → no se puede aplicar OHE directo, explota la dimensionalidad.
- `SellerG`: muchas categorías con frecuencia 1 → ruido.
- `Type`: pocas (h, u, t) → ideal para OHE.
- `Method`: pocas → ideal para OHE.

Regla práctica: si `nunique > 20-30`, considerá agrupar las menos frecuentes en una categoría "Otros" o usar **codificación de frecuencia** en lugar de OHE.

---

## Etapa 4 — Faltantes

```python
missing = melb_df.isnull().sum()
missing[missing > 0]
```

En `melb_data`:

- `Car`: 62 (poco, dropear o imputar con mediana).
- `BuildingArea`: ~6450 (¡casi la mitad!, decisión compleja).
- `YearBuilt`: ~5375 (idem).
- `CouncilArea`: 1369 (categórica, agregar "Desconocido").

Lo importante no es el conteo, es **entender el patrón** (MCAR, MAR, MNAR — ver Clase 1). Para eso `missingno` ayuda con visualizaciones de la matriz de presencia/ausencia.

---

## Etapa 5 — Análisis bivariado

### Categórica × numérica: boxplot

```python
sns.boxplot(data=melb_df, x='Type', y='Price')
```

Te muestra cómo varía la mediana y la dispersión del precio entre tipos de propiedad (`h` = house, `u` = unit, `t` = townhouse). En Melbourne `h` mediana más alta, `u` más baja.

### Numérica × numérica: scatter

```python
sns.scatterplot(data=melb_df, x='BuildingArea', y='Price')
```

Detectás:

- Tendencia general (suben juntas → correlación positiva).
- Heteroscedasticidad (más dispersión a medida que `BuildingArea` crece).
- Outliers que rompen la tendencia.

Truco útil: agregar `hue='is_price_outlier'` para colorear los puntos sospechosos y ver si forman patrón.

---

## Etapa 6 — Correlaciones (multivariado)

```python
numeric_df = melb_df.select_dtypes(include=['number'])
corr = numeric_df.corr().abs()
sns.heatmap(corr, cmap='coolwarm', annot=False)
```

El heatmap te da una vista panorámica. Para extraer información concreta, ranqueá contra el target:

```python
ranking = numeric_df.corr()['Price'].abs().sort_values(ascending=False).head(10)
```

### Top correlaciones con Price (cátedra)

| Variable    | Correlación con Price |
|-------------|-----------------------|
| Rooms       | 0.497                 |
| Bedroom2    | 0.476                 |
| Bathroom    | 0.467                 |
| YearBuilt   | 0.324                 |

Lo que sospechás inmediatamente:

- `Rooms` y `Bedroom2` tienen correlación de 0.497 y 0.476 con Price, **pero entre sí están altísimamente correlacionadas** (son casi la misma información). Hay **redundancia**, candidato a eliminar una de las dos.
- Ninguna correlación supera 0.5: el precio no se explica linealmente con una sola variable. Esperá modelos no lineales o feature engineering.

---

## Etapa 7 — Qué dice la matriz

Interpretar el heatmap es donde se pasa de "describir" a "decidir". Las preguntas:

1. ¿Qué variables tienen correlación alta con el target? → Candidatas a entrar al modelo.
2. ¿Qué pares de variables están altamente correlacionadas entre sí? → Una sobra (colinealidad).
3. ¿Hay variables con correlación cercana a 0 con TODO? → Posiblemente no aportan, o aportan en forma no lineal.

Esto alimenta directamente el siguiente paso: **selección de features** para PCA o para el modelo final.

---

## Outliers: tres técnicas combinadas

La cátedra usa específicamente **tres técnicas y las combina**, no una sola:

### 1. Boxplot

Visualización rápida, te marca los puntos por encima de `Q3 + 1.5·IQR` o por debajo de `Q1 - 1.5·IQR`.

### 2. IQR cuantitativo

```python
q1, q3 = melb_df['Price'].quantile([0.25, 0.75])
iqr = q3 - q1
lower, upper = q1 - 1.5*iqr, q3 + 1.5*iqr
price_outliers = melb_df[(melb_df['Price'] < lower) | (melb_df['Price'] > upper)]
```

### 3. Scatter coloreado

```python
sns.scatterplot(data=melb_df, x='BuildingArea', y='Price', hue='is_price_outlier')
```

Te permite ver si los outliers forman un patrón (por ejemplo, todos están en un barrio concreto) o si son ruido disperso.

### Importante

La cátedra **no usa z-score** para outliers porque z-score asume normalidad, y `Price` está claramente sesgada a la derecha. IQR es robusto: no depende de la forma de la distribución.

---

## Ejemplo numérico: IQR sobre Price (Melbourne)

Aplicando el método sobre la columna `Price` de `melb_data`:

```
Q1 = $650.000
Q3 = $1.330.000
IQR = Q3 - Q1 = $680.000

Límite inferior = Q1 - 1.5 × IQR = 650.000 - 1.020.000 = -$370.000
Límite superior = Q3 + 1.5 × IQR = 1.330.000 + 1.020.000 = $2.350.000
```

Como precios negativos no existen, el límite inferior se ignora. Todo lo que esté **por encima de $2.350.000** se marca como outlier.

Resultado: **612 outliers en `Price`**.

¿Qué hacer con ellos? Depende del objetivo:

- **Modelo de precios "típicos"**: eliminarlos (TP2 pide esto).
- **Estudio del mercado premium**: conservarlos, son la información que te interesa.
- **Detección de fraude**: son justamente lo que estás buscando.

La consigna del TP2 te pide eliminarlos visualmente, así que el flujo es: detectar con IQR + boxplot, eliminar las filas correspondientes, volver a graficar para verificar el resultado.

---

## Fechas

`melb_data` tiene una columna `Date` en formato día/mes/año como string. Antes de cualquier análisis temporal hay que parsearla:

```python
melb_df['date'] = pd.to_datetime(melb_df.Date, format="%d/%m/%Y")
melb_df['date_month'] = pd.to_datetime(melb_df.date.dt.strftime('%Y-%m'))

monthly = melb_df.groupby('date_month')['Price'].mean()
sns.lineplot(x=monthly.index, y=monthly.values)
```

El `lineplot` por mes te muestra **estacionalidad** (¿hay meses con más operaciones?) y **tendencias** (¿los precios suben con el tiempo?). En Melbourne se ven ciclos asociados al calendario fiscal australiano.

---

## ydata_profiling: complemento, no reemplazo

`ydata_profiling` (antes `pandas-profiling`) genera un reporte HTML automático con histogramas, correlaciones, faltantes y alertas:

```python
from ydata_profiling import ProfileReport
profile = ProfileReport(melb_df, title="EDA Melbourne")
profile.to_file("eda_melb.html")
```

Útil para un primer barrido rápido, pero **no reemplaza el análisis manual**. El reporte te da todo junto y no te obliga a pensar: si lo usás sin reflexión, te perdés la intuición que da hacer cada gráfico a mano.

Regla práctica: usalo como **chequeo cruzado** al final del EDA, no como atajo al principio.

---

## Conexión con AVD

La cátedra explicita esta continuidad:

> *"Aplicar las herramientas que hemos estudiado durante la materia anterior, Análisis y Visualización de Datos. No entraremos en detalles en esta notebook, sino que será parte de la ejercitación práctica."*

Lo que cambia respecto a AVD:

1. **Foco en curación**, no solo visualización. En AVD describías; acá decidís qué hacer con lo que ves.
2. **EDA orientado a modelo**: cada decisión apunta a feature selection.
3. **Pipeline completo**: el EDA es la primera etapa de un proceso que termina en un dataset productivo.
4. **Calidad de datos**: completitud, validez, precisión, integridad, consistencia, temporalidad, representatividad.
5. **Conexión con GenAI**: features para LLMs, RAG, embeddings.

Si venís de AVD, esto es **AVD + decisión + producción**.

---

## Conexión con el TP

- **TP1 Ejercicio 1**: la consigna pide "análisis descriptivo de las variables numéricas, verificar Dtype". Esto es exactamente las etapas 1 y 2: `info()`, `describe()`, identificar tipos mal codificados (`Date` como `object`, valores numéricos como strings).
- **TP1 Ejercicio 1**: también pide "estudiar las variables categóricas" → etapa 3 con `nunique()` + `value_counts()`. La decisión de **reducir cardinalidad** antes del OHE depende directamente de esta exploración.
- **TP2 Ejercicio 2**: pide explícitamente **eliminar outliers** después de elegir el subset de columnas. El flujo: subset → faltantes → distribución → outliers (IQR + boxplot + scatter) → eliminación visual → verificación.
- **TP2 Ejercicio 2**: pide **graficar la distribución** antes y después de las transformaciones (eliminación de outliers, escalado). Esto es etapa 4 aplicada como control de calidad.

---

## Errores comunes

1. **Saltarse el EDA y empezar a modelar**. Sin EDA terminás imputando ceros que eran faltantes, eliminando outliers legítimos, o entrenando modelos con leakage.
2. **Mirar solo `describe()` y declararse satisfecho**. `describe()` te da estadísticos, pero no la **forma** de la distribución. Una distribución bimodal y una unimodal pueden tener la misma media y mediana.
3. **Confundir `0` con faltante**. En `melb_data`, `BuildingArea == 0` o `Bathroom == 0` no son ceros legítimos: son faltantes enmascarados. Detectalos con `melb_data[melb_data == 0].count(axis=0)`.
4. **Usar pairplot con datasets grandes**. Es lentísimo y poco informativo cuando tenés muchas variables. Preferí heatmap de correlaciones + scatter específicos.
5. **Aplicar z-score para outliers sobre datos sesgados**. `Price` no es normal, así que `|z| > 3` te marca como outliers a propiedades que son tranquilamente "caras pero normales". Usá IQR.
6. **Eliminar outliers automáticamente sin mirar el contexto**. En TP2 sí se pide eliminarlos, pero la decisión debe ser explícita y documentada. Outlier no es sinónimo de error.
7. **Usar correlación de Pearson con relaciones no lineales**. Si la relación es curva (logarítmica, exponencial), Pearson puede dar ≈ 0 aunque haya una asociación clara. Considerá Spearman o transformar la variable (log) antes.
8. **Tomar `ydata_profiling` como verdad revelada**. Es una herramienta de chequeo, no un sustituto del criterio del analista.
9. **No graficar antes y después de cada transformación**. Si imputás con la mediana y no comparás histogramas, no sabés si arruinaste la distribución.

---

## Checklist de comprensión

- [ ] ¿Por qué la cátedra prefiere IQR sobre z-score para outliers en `Price`?
- [ ] En el cálculo de outliers de `Price`, ¿de dónde sale el 612? ¿Podrías reproducir Q1, Q3, IQR y el límite superior?
- [ ] Si `Rooms` y `Bedroom2` tienen correlación 0.497 y 0.476 con `Price` pero entre ellas están altamente correlacionadas, ¿qué hacés?
- [ ] ¿Cuál es la diferencia conceptual entre el EDA que hacías en AVD y el que hacés en EyCD?
- [ ] Si `ydata_profiling` te genera todos los gráficos automáticamente, ¿por qué no es buena idea reemplazar el análisis manual con eso?

---

**Próximo paso**: `08-combinacion-de-datasets.md`
