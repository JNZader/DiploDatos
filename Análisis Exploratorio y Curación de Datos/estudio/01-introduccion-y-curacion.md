# 01 — Introducción y curación de datos

## Concepto

La cátedra define **curación de datos** como *"la selección y transformación de los datos para su experimentación, incluyendo limpieza de ruido, faltantes y errores"*. En criollo: agarrar el dataset tal como te lo dieron y dejarlo en condiciones de que un modelo (o vos) pueda aprender algo útil sin tomarlo del lado equivocado.

Pero ojo: curar **no es** limpiar a fuerza bruta. Es decidir, con criterio, qué información conservás, cuál descartás y cuál reconstruís — sabiendo que cada decisión define **qué pregunta podés responder con qué muestra**. Cambiar el criterio de curación cambia la conclusión, igual que en AVD pasaba con el criterio de limpieza.

Curación es el primer eslabón después del EDA. En AVD usaste el EDA para describir; en EyCD usás el EDA para **diagnosticar qué hay que curar**, y después usás la curación para producir un dataset que pueda alimentar un modelo o un dashboard sin sorpresas.

## Intuición

La curación de datos es como **preparar los ingredientes antes de cocinar**.

- El cocinero pro abre la heladera y antes de prender el fuego revisa: zanahorias podridas afuera, papas con brotes a la basura, lechuga lavada, ajo pelado, especias medidas en cuencos. Recién entonces enciende la hornalla.
- El cocinero apurado tira todo a la olla "porque hay que comer" y después se sorprende de que el guiso tenga gusto raro.

Tu dataset es la heladera. Las verduras podridas son los valores absurdos. Los brotes son los outliers. La lechuga sin lavar son los duplicados. El ajo entero son las categóricas sin codificar. Si no preparás los ingredientes, el modelo se come la basura junto con la señal y vas a echarle la culpa al algoritmo, cuando el problema lo metiste vos en la olla.

La diferencia con AVD: ahí preparábamos solo para describir un plato; acá preparamos para que **otro** (el modelo, el dashboard, el sistema en producción) cocine. La preparación tiene que ser **reproducible**: cualquiera que reciba tu receta tiene que poder repetirla y obtener el mismo plato.

---

## Pipeline completo: de la fuente cruda a producción

La materia entera se mueve dentro de este pipeline, y cada clase ataca un eslabón distinto. Tenerlo mapeado desde el principio te ahorra perderte:

```
recolección  →  exploración  →  curación  →  modelado  →  producción  →  monitoreo
```

| Etapa | Qué se hace | Qué clase la cubre |
|-------|-------------|--------------------|
| **Recolección** | Conseguir los datos: encuestas, APIs, scraping, sensores. Se decide qué muestrear, cómo y de dónde | Clase 2.1 (sesgos de recolección) |
| **Exploración (EDA)** | Mirar el dataset, entender qué hay, detectar problemas, formular hipótesis | Clases 3 y 4 |
| **Curación** | Resolver los problemas detectados: faltantes, ruido, outliers, mal codificados, redundantes | Clases 1, 2.2, 2.3 |
| **Modelado** | Entrenar un modelo o producir el análisis final. Fuera del alcance de EyCD, pero el dataset curado es su input | Materias posteriores |
| **Producción** | El modelo o pipeline corre solo, sobre datos nuevos | Clase 4 (ETL, DAGs, Airflow) |
| **Monitoreo** | Detectar que algo cambió: drift de datos, drift de concepto, sesgos emergentes | Clase 2.1 (data drift) |

Mensaje fuerte de la cátedra (Clase 4): *"Almacenar es barato y flexible. Guardar primero el dato crudo y transformar después según el caso."* Ese es el paradigma ELT moderno (Extract → Load → Transform), opuesto al ETL clásico donde transformabas antes de cargar. En EyCD usamos los dos según contexto.

---

## EDA vs curación: la diferencia que cuesta entender

Mucha gente los mete en la misma bolsa. No son lo mismo.

| Dimensión | EDA | Curación |
|-----------|-----|----------|
| **Verbo** | *Observar*, *describir* | *Modificar*, *transformar* |
| **Producto** | Diagnóstico (lista de problemas detectados) | Dataset nuevo, listo para modelar |
| **Reversible** | Sí: si mirás un boxplot, el dato no se mueve | No por defecto: si imputás un NaN, el valor cambia |
| **Cuándo se hace** | Antes y después de curar (para chequear que la curación funcionó) | Después del EDA inicial, antes de modelar |
| **Riesgo si lo hacés mal** | Conclusiones equivocadas en la exploración | Conclusiones equivocadas **en el modelo** que cargas a producción |

La cátedra es explícita: *"El EDA no es un fin en sí mismo: sirve para decidir qué columnas conservamos, cuáles descartamos y qué transformaciones necesitamos antes de modelar."* Es decir, **el EDA existe para informar la curación**, no para reemplazarla.

Patrón típico en EyCD: EDA → detectar problema → curar → EDA otra vez (verificar que el problema se resolvió y que no apareció uno nuevo).

---

## Las 7 dimensiones de calidad de datos

La cátedra (Clase 3) lista siete dimensiones que tenés que evaluar contra tu dataset. Cada una responde a una pregunta distinta y necesita su propio chequeo. Si no las separás, después no sabés qué arreglar.

| # | Dimensión | Pregunta que responde | Chequeo típico |
|---|-----------|------------------------|----------------|
| 1 | **Completitud** | ¿Están todos los datos que esperaba? | `df.isnull().sum() / len(df)` |
| 2 | **Validez** | ¿Cada valor cumple las reglas del dominio (rango, formato)? | `df.Price.between(0, 1e8).all()` |
| 3 | **Precisión** | ¿El valor refleja la realidad o tiene error de medición? | Comparar contra fuente externa |
| 4 | **Integridad** | ¿Las relaciones entre tablas son consistentes? | Validar claves foráneas, post-merge |
| 5 | **Consistencia** | ¿La misma entidad aparece igual en distintos lugares? | "CABA" vs "caba" vs "Capital Federal" |
| 6 | **Temporalidad** | ¿El dato sigue vigente / no es viejo? | `df.Date.max()` vs hoy |
| 7 | **Representatividad** | ¿La muestra refleja la población de interés? | Comparar distribuciones contra censo |

Detalle clave: estas dimensiones **se chequean en orden**. Si tu dataset falla en completitud (faltantes masivos), no tiene sentido evaluar precisión hasta que no decidas qué hacés con los huecos.

---

## Tipos de problemas a curar (taxonomía de la Clase 1)

La cátedra clasifica los problemas de calidad en estos seis tipos. Saberlos identificar es la mitad de la curación:

| Tipo de problema | Definición de la cátedra | Ejemplo en Melbourne |
|------------------|--------------------------|----------------------|
| **Ruido** | Error que ensucia/contamina la señal. *"Cuando entra basura, sale basura."* | Precios mal cargados por bug del scraper |
| **Dato faltante** | Dato no registrado. Puede estar como NaN, 0, -1 | `BuildingArea` con ~6450 NaN |
| **Dato erróneo** | Dato recolectado con error que lo separa de la generalidad | `Bathroom = 0` (toda casa tiene al menos uno) |
| **Outlier (atípico)** | Valor real con baja probabilidad. Mucho efecto palanca | Precio de $9M en un suburbio promedio |
| **Dato mal codificado** | Aparece al mezclar bases con distinta codificación de faltantes | Una fuente usa NaN, otra usa 0, otra usa -1 |
| **Dato redundante** | Información duplicada en dos columnas distintas | `Rooms` ≈ `Bedroom2` (correlación alta) |

Diferencia conceptual importante:

- **Dato erróneo**: existe el dato real, pero se cargó mal. Hay que corregir o descartar.
- **Outlier**: existe el dato real y se cargó bien, simplemente es raro. Hay que **decidir** si lo mantenés (puede ser informativo) o lo eliminás (puede sesgar).

No son lo mismo, y la cátedra es enfática al separarlos: *"dato atípico es un valor real con baja probabilidad"*, *"dato erróneo es un dato recolectado con error"*.

---

## Predecir vs imputar: un concepto que muchos confunden

Otra distinción que cae en TP:

| Operación | Sobre qué actúa | Ejemplo |
|-----------|-----------------|---------|
| **Predecir** | Un valor que **no fue muestreado**, no existe en la tabla | Estimar el precio de una casa que recién se publicó |
| **Imputar** | Sustituir un valor **no informado** que sí debería estar en la tabla | Rellenar el `BuildingArea` faltante de una casa del dataset |

Cita textual: *"Imputar es predecir esos datos"*. Operativamente son lo mismo (estimar un valor desconocido), pero la **intención** y el **contexto** cambian. Cuando imputás, ya tenés casi toda la fila y querés tapar el agujero. Cuando predecís, la fila es nueva. Esto va a importar cuando veamos imputación estocástica (Clase 1) y se vuelve crucial en producción.

---

## Ejemplo numérico: detectar problemas en una mini-tabla

Tomá este subconjunto de 6 filas del estilo Melbourne:

| id | Suburb        | Rooms | Bathroom | BuildingArea | Price     | Date       |
|----|---------------|-------|----------|--------------|-----------|------------|
| 1  | Abbotsford    | 3     | 1.0      | 79.0         | 1480000   | 3/12/2016  |
| 2  | Abbotsford    | 2     | 0.0      | 0.0          | 1035000   | 4/02/2016  |
| 3  | abbotsford    | 4     | 2.0      | 142.0        | NaN       | 4/06/2016  |
| 4  | Carlton       | 3     | NaN      | 134.0        | 1876000   | 5/06/2016  |
| 5  | Carlton       | 2     | 1.0      | 91.0         | 850000    | 4/02/2017  |
| 6  | Brunswick     | 2     | 1.0      | 89.0         | 98000000  | 8/03/2017  |

Sin tocar código, identificá las dimensiones de calidad afectadas. Mínimo cuatro problemas:

**1. Completitud (faltante explícito) — fila 4**:
`Bathroom = NaN`. Sabemos que existe (toda casa tiene baños), pero no se registró.

**2. Completitud (faltante explícito) — fila 3**:
`Price = NaN`. Si Price es nuestra variable objetivo, esta fila tiene que descartarse o imputarse con muchísimo cuidado.

**3. Completitud (faltante enmascarado) — fila 2**:
`Bathroom = 0` y `BuildingArea = 0`. Una casa con cero baños o cero metros cuadrados no existe. Estos ceros son **dato faltante codificado como cero**. Hay que pasarlos a `NaN` antes de cualquier imputación:
```python
melb_df.loc[melb_df.Bathroom < 1, "Bathroom"] = pd.NA
melb_df.loc[melb_df.BuildingArea < 1, "BuildingArea"] = pd.NA
```

**4. Consistencia — filas 1 y 3**:
`"Abbotsford"` vs `"abbotsford"`. Mismo suburbio, distinta capitalización. Si agrupás por suburbio, vas a tener dos grupos cuando debería haber uno:
```python
melb_df["Suburb"] = melb_df["Suburb"].str.strip().str.title()
```

**5. Validez (outlier o error) — fila 6**:
`Price = 98000000` (98 millones) en Brunswick para 2 habitaciones es **imposible**. Comparado con la mediana de Melbourne (~$900K), está dos órdenes de magnitud arriba. Puede ser:
- Error de tipeo (extra cero).
- Dato real pero atípico extremo (mansión histórica).

La decisión depende del análisis. Para describir el mercado típico, **fuera**. Para detectar transacciones sospechosas, **es el dato más interesante**.

**6. Validez (formato) — toda la columna Date**:
Tipo `object`, no `datetime`. No podés filtrar por año ni agrupar por mes sin convertirla primero:
```python
melb_df["Date"] = pd.to_datetime(melb_df["Date"], format="%d/%m/%Y")
```

Total: con 6 filas detectamos al menos 6 problemas distintos en 4 de las 7 dimensiones (completitud, validez, consistencia, integridad si lo merge-aramos contra otra tabla). Eso te da idea del nivel de detalle que pide la curación seria.

---

## El árbol de decisión básico de la curación

Cuando aparece un problema, no improvises. Aplicá este árbol:

```
Hay problema detectado en el EDA
│
├── ¿Es un faltante?
│   ├── Sí → ir al árbol de faltantes (archivo 02)
│   └── No → seguir
│
├── ¿Es un valor inválido (fuera de dominio)?
│   ├── Sí → ¿puedo corregirlo con regla? (capitalización, parsing)
│   │        ├── Sí → corregir
│   │        └── No → marcar como NaN y tratar como faltante
│   └── No → seguir
│
├── ¿Es un outlier?
│   ├── Sí → ¿es objeto de estudio? (fraude, valores extremos)
│   │        ├── Sí → conservar
│   │        └── No → eliminar por IQR o percentil
│   └── No → seguir
│
├── ¿Es redundancia?
│   ├── Sí → eliminar la columna con menos varianza o más faltantes
│   └── No → seguir
│
└── ¿Es codificación inconsistente?
    └── Sí → normalizar a un vocabulario único antes de cualquier merge
```

Este árbol no es de la cátedra al pie de la letra, pero condensa la lógica de las Clases 1 a 4. Te conviene tenerlo a mano en los TP.

---

## Regla de oro de la materia

> **Un pipeline correcto en código pero flojo en criterio es un pipeline incorrecto.**

Esto es la traducción a EyCD de la regla de AVD ("un análisis correcto en código pero flojo en criterio..."). En curación es más exigente todavía, porque las decisiones modifican el dataset que después usa otro. No alcanza con que el código no tire error. Tenés que poder responder, ante cada paso:

- ¿Qué problema estoy resolviendo? (referenciar la dimensión de calidad)
- ¿Por qué elijo esta técnica y no otra? (tradeoff explícito)
- ¿Cómo verifico que mejoró? (chequeo de antes/después)
- ¿Qué supuestos estoy aceptando? (por ejemplo, asumir MAR para imputar con KNN)

Si no podés contestar las cuatro, la decisión no está madura, aunque corra.

---

## Conexión con el TP

- **Ambos TPs son ejercicios de curación de punta a punta**: ese es **el** mensaje de la materia. No es "hacer un modelo": es "dejar el dataset listo para que un modelo pueda hacer su trabajo".
- **TP1**: encodear categóricas, imputar numéricas con KNN, aplicar PCA y entregar un dataset transformado. Cada paso ataca una dimensión: encoding ataca *validez* (los algoritmos necesitan números); imputación ataca *completitud*; PCA ataca *representatividad* compacta y elimina redundancia.
- **TP1, criterio de evaluación**: la entrega pide un PDF/MD con *"criterios, interpretación y transformaciones"*. Eso es exactamente la regla de oro materializada: no se evalúa solo el código, se evalúa el **porqué**.
- **TP2**: combinar Melbourne con AirBnB. Ataca *integridad* (claves), *consistencia* (`Postcode` vs `zipcode`), *completitud* (faltantes post-merge), *validez* (rangos plausibles de precios AirBnB) y *representatividad* (zipcodes que aparecen en uno y no en el otro).
- **TP2 ejercicio 3 (persistencia)**: el dataset final tiene que poder volcarse a SQLite. Si tu curación dejó tipos basura o NaN donde no corresponden, falla la carga. Es el chequeo "¿está realmente listo para producción?".

---

## Errores comunes

1. **Confundir EDA con curación**: hacer 30 gráficos en lugar de modificar el dataset. El EDA informa; la curación actúa. Ambos son necesarios, pero no son lo mismo.
2. **Curar sin EDA previo**: imputar la media de Price sin haber mirado la distribución (que está sesgada a la derecha). La mediana es mejor en ese caso, pero solo lo sabés si miraste antes.
3. **Curar sin documentar**: hacer 10 transformaciones en un notebook sin escribir el porqué de cada una. En un mes ni vos vas a poder reproducirlo.
4. **Confundir outlier con error**: eliminar todos los precios "raros" sin investigar. Si tu pregunta es "¿qué hace que una casa valga 5x el promedio?", los outliers son tu dataset, no la basura.
5. **Curar igual para todas las preguntas**: la curación es **dependiente de la pregunta**. El mismo dataset, para "predecir precio típico" y para "detectar fraude inmobiliario", debe curarse distinto.
6. **No volver a hacer EDA después de curar**: si imputaste con la media, la nueva media coincide artificialmente con la vieja, pero la varianza bajó. Hay que verlo.
7. **Ignorar dimensiones más allá de completitud**: lo más vistoso es contar NaN, pero validez (rangos), consistencia (typos), integridad (claves duplicadas) y representatividad (sesgo muestral) son igual de importantes y se ignoran más.

---

## Checklist de comprensión

- [ ] ¿Podés enunciar las 7 dimensiones de calidad de datos sin mirar la tabla y dar un ejemplo de cada una sobre `melb_data`?
- [ ] Frente a un `Bathroom = 0` en Melbourne, ¿lo dejás, lo eliminás o lo convertís a NaN, y por qué?
- [ ] ¿Cuál es la diferencia operativa entre EDA y curación y por qué en EyCD vas a tener que alternarlos varias veces sobre el mismo dataset?

---

**Próximo paso**: `02-datos-faltantes.md`
