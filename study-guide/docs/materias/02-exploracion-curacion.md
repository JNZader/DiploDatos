# Materia 2 — Análisis Exploratorio y Curación de Datos

> **Idea rectora:** explorar permite descubrir qué puede estar mal; curar exige decidir qué hacer, registrar por qué y demostrar qué cambió. Una transformación que “deja lindo” el dataset pero no conserva su significado, no puede auditarse o usa información del futuro no es una buena curación.

Esta materia comienza exactamente donde terminó AVD. En la Materia 1 aprendimos a formular preguntas, reconocer unidades de análisis, describir distribuciones, detectar faltantes, observar outliers, comparar grupos y limitar una conclusión. Ahora agregamos un compromiso más fuerte: **modificar datos sin borrar la historia de lo que eran**.

Curar no es aplicar una receta universal. Es construir una versión de los datos apta para un propósito declarado. El mismo registro puede ser útil para describir la historia del corpus, inconveniente para entrenar un clasificador y esencial para auditar un error. La decisión depende del objetivo, pero nunca debe depender del capricho.

---

## 0. Cómo estudiar esta materia

### 0.1 Qué deberías poder hacer al terminar

Al completar este capítulo deberías poder:

1. explicar la diferencia entre detectar un problema y decidir una transformación;
2. definir la unidad de análisis y el esquema esperado antes de limpiar;
3. evaluar completitud, validez, consistencia, unicidad, temporalidad y trazabilidad;
4. distinguir faltantes estructurales de faltantes accidentales;
5. elegir entre conservar, eliminar, imputar o agregar un indicador sin fingir certeza;
6. definir duplicados exactos, por clave, cercanos y semánticos;
7. normalizar categorías mediante tablas de mapeo auditables;
8. construir una propuesta de target `fuero` desde `materia` y separar casos claros, transversales y ambiguos;
9. preparar texto legal preservando el original y justificando cada normalización;
10. distinguir un error de un caso raro válido, también en longitudes textuales;
11. clasificar features como seguras, dudosas o prohibidas según disponibilidad y riesgo de fuga;
12. reconocer sesgos temporales, geográficos, institucionales y de tipo documental;
13. evitar fugas por target, duplicados, tiempo y preprocesamiento;
14. explicar la frontera conceptual entre train, validación y test;
15. entender qué conservan y qué pierden BoW, TF-IDF y embeddings;
16. diseñar una curación reproducible con versiones, semillas, diccionario y diario de transformaciones;
17. usar ETL, linaje y contratos livianos sin convertir el proyecto en una plataforma industrial;
18. preparar un roadmap de TP2 donde cada acción tenga evidencia, riesgo y verificación.

### 0.2 Ruta recomendada: teoría → control → transferencia

Esta materia se estudia mejor en cinco pasadas:

1. **Teoría:** entendé el problema antes de mirar una herramienta.
2. **Checkpoint:** explicalo con tus palabras y buscá el supuesto oculto.
3. **Ejercicio conceptual:** resolvé una decisión pequeña sin código.
4. **Aplicación SAIJ:** trasladá el criterio a sumarios, fallos, `materia`, fechas y texto.
5. **Conexión TP2:** convertí el criterio en una fila de la matriz de decisiones.

El recorrido no es lineal una sola vez. La curación forma un ciclo:

```text
diagnóstico → decisión → transformación → verificación → nuevo diagnóstico
```

Si la verificación falla, no se “arregla” el gráfico. Se revisa la decisión.

### 0.3 Convenciones de evidencia dentro de Materia 2

Usaremos los mismos cuatro rótulos del libro:

- **Teoría:** principio general, independiente del corpus.
- **Ejemplo ilustrativo:** caso inventado para razonar.
- **Hallazgo del notebook del grupo — a reproducir:** dato o patrón informado por el equipo que Javier todavía no verificó por sí mismo.
- **Decisión de Javier — pendiente:** elección metodológica que no debe heredarse por copiar un notebook.

> **Checkpoint 0**
>
> Completá: “AVD produce un ________. Curación produce una nueva ________ del dataset y debe conservar una ________ de cómo llegó a ella”.

---

## 1. Del diagnóstico de AVD a una decisión de curación

### 1.1 Dos verbos diferentes

En AVD podíamos observar: “la columna `materia` contiene variantes de escritura”. Esa frase es un **diagnóstico**. Todavía no modificó nada.

En curación debemos responder preguntas adicionales:

- ¿Cuáles son variantes equivalentes y cuáles representan conceptos distintos?
- ¿Quién define el vocabulario canónico?
- ¿Qué pasa con una categoría que no encaja?
- ¿La transformación afecta análisis históricos?
- ¿Podemos volver del valor normalizado al original?
- ¿Cómo verificamos que no fusionamos etiquetas legítimas?

La curación empieza cuando la observación se convierte en una regla explícita.

```text
diagnóstico: "hay variantes"
decisión: "estas variantes representan el mismo concepto"
transformación: aplicar un mapeo versionado
verificación: revisar cobertura, colisiones y casos no mapeados
```

### 1.2 Una decisión siempre tiene costo

Toda transformación gana algo y pierde algo. Pasar todo a mayúsculas reduce variantes de capitalización, pero borra una diferencia que podría ser significativa en otro dominio. Eliminar tildes facilita ciertos emparejamientos, pero puede complicar la reconstrucción del texto original. Agrupar clases raras mejora estabilidad estadística, pero deja de distinguir situaciones minoritarias.

Por eso una buena decisión declara:

1. **qué problema resuelve**;
2. **qué información modifica o descarta**;
3. **qué supuesto necesita**;
4. **qué riesgo introduce**;
5. **qué evidencia permitirá verificarla**.

### 1.3 Criterio de aptitud para el propósito

No existe “el dataset limpio” en abstracto. Existe un dataset **apto para una tarea**.

**Ejemplo ilustrativo.** Imaginemos un documento excepcionalmente largo.

- Para describir la diversidad histórica del corpus, conservarlo puede ser imprescindible.
- Para estimar el tiempo típico de lectura, puede convenir reportarlo aparte para que no domine la media.
- Para entrenar un modelo con un límite técnico de tokens, habrá que definir truncamiento, segmentación o exclusión.
- Para auditar la cobertura, nunca debería desaparecer sin registro.

El documento no cambió. Cambió la pregunta. La curación responsable hace visible esa dependencia.

### 1.4 Puente operativo

Usá una tabla de dos columnas antes de transformar:

| Diagnóstico de AVD | Pregunta de curación |
|---|---|
| Hay muchos nulos | ¿Son estructurales, accidentales o una mezcla? |
| Hay muchas categorías parecidas | ¿Qué equivalencias pueden justificarse? |
| La clase minoritaria tiene pocos casos | ¿Es una clase válida, un error o un alcance que no podremos evaluar? |
| Existen fechas extremas | ¿Son imposibles, errores de formato o documentos históricos legítimos? |
| Dos textos son casi iguales | ¿Son duplicados, versiones, citas o documentos relacionados? |
| Una feature anticipa mucho el target | ¿Es señal legítima o información que no estará disponible al predecir? |

> **Error frecuente:** saltar de “me incomoda este valor” a “lo borro”. La incomodidad visual no es evidencia de invalidez.

> **Checkpoint 1**
>
> ¿Podrías explicar por qué un mismo outlier puede conservarse para una pregunta y excluirse para otra sin que una decisión sea deshonesta? La respuesta debe mencionar propósito, población resultante y documentación.

---

## 2. Qué es curar y por qué no significa “borrar filas extrañas”

### 2.1 Definición desde primeros principios

Curar datos es **seleccionar, organizar, corregir, transformar y documentar** observaciones para que una tarea pueda realizarse con significado y repetirse. El verbo central no es “limpiar”; es **decidir con trazabilidad**.

Una curación puede incluir:

- corregir un formato inequívocamente inválido;
- separar poblaciones que obedecen a esquemas distintos;
- conservar un valor raro con una bandera de revisión;
- reconstruir una categoría mediante una regla;
- excluir una fila que no pertenece a la población objetivo;
- imputar un valor faltante bajo supuestos explícitos;
- preservar dos versiones: original y transformada;
- impedir que una variable prohibida llegue al modelo;
- definir pruebas que fallen si aparece un dato inesperado.

### 2.2 Limpio no equivale a homogéneo

Un dataset puede ser heterogéneo y estar correctamente curado. Si contiene sumarios y fallos, la solución no es forzar a ambos a tener los mismos campos. Puede ser mejor modelar dos subesquemas o definir con claridad cuál población alimenta cada tarea.

Del mismo modo, un dataset puede verse prolijo y estar mal curado. Una tabla sin nulos puede haber sido completada con valores inventados. Una variable categórica sin variantes puede haber fusionado conceptos distintos. Una muestra sin outliers puede haber perdido todos los casos difíciles.

### 2.3 Cuatro acciones antes de eliminar

Cuando aparece una observación extraña, considerá en orden:

1. **Validar:** ¿viola una regla del dominio o solo es poco frecuente?
2. **Comparar:** ¿aparece en la fuente original y en variables relacionadas?
3. **Marcar:** ¿podemos conservarla con un indicador de revisión?
4. **Separar:** ¿pertenece a otra población o régimen que merece análisis propio?

Eliminar es una quinta opción, no la primera.

### 2.4 El conjunto de exclusiones también es un producto

Si excluís filas, guardá al menos:

- identificador estable;
- regla que disparó la exclusión;
- fecha o versión de la regla;
- cantidad afectada;
- resumen por grupo relevante;
- destino: cuarentena, población fuera de alcance o error confirmado.

Así podés responder “¿qué quedó afuera?” sin reconstruir el notebook meses después.

> **Material complementario integrado 6 — Transformaciones reversibles y auditabilidad (nivel DiploDatos)**
>
> “Reversible” no siempre significa recuperar matemáticamente cada carácter desde la tabla final. Significa poder reconstruir el proceso y volver a la fuente: conservar datos crudos inmutables, registrar reglas, mantener identificadores y guardar tablas de correspondencia. Borrar acentos en una columna derivada es aceptable si el texto crudo permanece intacto. Sobrescribir el único texto disponible no lo es. En esta materia alcanza con una disciplina liviana: `raw` no se toca, `clean` se regenera y cada paso tiene una justificación y una métrica antes/después.

> **Checkpoint 2**
>
> Señalá la diferencia entre “excluir de la matriz de entrenamiento” y “borrar del proyecto”. La primera limita una tarea; la segunda destruye trazabilidad.

---

## 3. Unidad de análisis y esquema: decidir qué representa una fila

### 3.1 La unidad antecede al esquema

La unidad de análisis es la entidad sobre la que interpretamos una observación. Puede ser:

- un documento completo;
- un sumario;
- un fallo;
- un párrafo;
- una relación documento–descriptor;
- una decisión judicial;
- una combinación documento–fuero si el problema es multietiqueta.

No son intercambiables. Si un documento tiene cinco descriptores y lo “explosionamos” a cinco filas, la unidad deja de ser el documento y pasa a ser el par documento–descriptor. Contar filas después de esa operación ya no cuenta documentos.

### 3.2 Qué es un esquema

Un esquema es el contrato estructural de los datos:

- nombres de campos;
- tipos esperados;
- obligatoriedad;
- dominios permitidos;
- claves;
- relaciones;
- reglas condicionales;
- significado temporal.

Un esquema no es solo `string`, `integer` o `date`. También expresa condiciones como:

> Si `tipo_registro = sumario`, entonces `texto` debería seguir la semántica definida para sumarios; si `tipo_registro = fallo`, la ausencia de ese campo puede ser estructural y no un error.

### 3.3 Poblaciones documentales mezcladas

Una tabla ancha suele esconder varios formularios pegados. Cada tipo documental completa un subconjunto diferente de columnas. Si calculamos faltantes globales sin distinguir tipos, confundimos “no aplica” con “se perdió”.

**Ejemplo ilustrativo.**

| id | tipo | texto_resumen | tribunal | número_fallo |
|---|---|---|---|---|
| A | sumario | presente | vacío | vacío |
| B | fallo | vacío | presente | presente |

Globalmente, cada campo tiene 50% de nulos. Sin embargo, no hay necesariamente ningún dato perdido. Hay dos esquemas.

La respuesta adecuada puede ser:

- mantener una tabla común con reglas condicionales;
- separar tablas por tipo y conservar una clave de relación;
- definir una vista específica para la tarea;
- excluir un tipo si está fuera del objetivo, registrando la decisión.

### 3.4 Aplicación SAIJ con evidencia rotulada

> **Hallazgo del notebook del grupo — a reproducir:** el equipo informa que la fuente mezcla poblaciones documentales y que varios patrones de nulos se explican por campos propios de un tipo de documento. También informa la presencia de registros que no pertenecerían a la población de jurisprudencia elegida.
>
> **Decisión de Javier — pendiente:** reproducir la clasificación de tipos, verificar las reglas de pertenencia y definir qué unidad alimentará TP2. No alcanza con copiar filtros o cantidades del notebook.

### 3.5 Esquema mínimo propuesto para razonar

Antes de limpiar, redactá una ficha:

| Campo conceptual | Pregunta |
|---|---|
| Unidad primaria | ¿Qué representa exactamente una fila? |
| Identidad | ¿Qué campo o combinación identifica la unidad? |
| Tipo documental | ¿Cuáles existen y cómo se reconocen? |
| Texto candidato | ¿Cuál contiene el contenido útil y para qué tipos aplica? |
| Target candidato | ¿Viene observado o se construye? |
| Fechas | ¿Representan decisión, publicación, carga o actualización? |
| Metadata | ¿Se conoce antes de la predicción o después? |
| Relaciones | ¿Una fila puede tener varias materias o descriptores? |

> **Error frecuente:** definir la unidad mirando solamente el índice del DataFrame. El índice técnico no garantiza identidad semántica.

> **Checkpoint 3**
>
> Si expandís una lista de tres materias a tres filas, ¿qué denominador usarías para contar documentos y cuál para contar asignaciones de materia? Explicá por qué ambos conteos son válidos pero responden preguntas diferentes.

---

## 4. Seis dimensiones de calidad de datos

La calidad no es una nota única. Un dataset puede ser completo pero inválido, consistente pero desactualizado, único pero imposible de rastrear. Separar dimensiones permite diagnosticar y verificar con precisión.

> **Material complementario integrado 1 — Seis dimensiones de calidad (nivel DiploDatos)**
>
> Para esta guía usamos seis dimensiones operativas: **completitud, validez, consistencia, unicidad, temporalidad y trazabilidad**. No son una certificación universal ni agotan todas las taxonomías. Funcionan como un mapa práctico para que cada problema tenga una pregunta, una evidencia y una comprobación.

### 4.1 Completitud

Pregunta: **¿está presente la información que debería existir para esta unidad y este uso?**

No se evalúa solo con porcentaje global de nulos. Debe condicionarse por:

- tipo documental;
- período;
- jurisdicción;
- fuente;
- clase objetivo;
- obligatoriedad del campo.

Una columna con 90% de ausencia puede estar completa para el 10% de filas a las que aplica. En cambio, 2% de ausencia en el target puede ser crítico si esos casos se concentran en una provincia o época.

**Verificación útil:** tasa de presencia por grupo y comparación antes/después.

### 4.2 Validez

Pregunta: **¿el valor cumple las reglas del dominio y del formato?**

Ejemplos:

- fecha parseable y dentro de un rango posible;
- código dentro de un vocabulario permitido;
- texto no vacío después de remover únicamente markup;
- identificador con estructura esperada;
- combinación de campos compatible con el tipo documental.

Validez no es frecuencia. Un fallo del siglo XIX puede ser raro y válido. Una fecha futura imposible según la fecha de extracción puede ser inválida, salvo que el campo tenga otra semántica.

### 4.3 Consistencia

Pregunta: **¿la misma entidad o concepto se representa de manera compatible en lugares distintos?**

Incluye:

- `laboral`, `LABORAL` y `Laboral`;
- fechas con día/mes invertidos;
- el mismo código asociado a descripciones incompatibles;
- una materia que contradice una regla documental;
- dos tablas con distintas definiciones de “fecha”.

Consistencia no exige igualdad textual. Exige que las diferencias tengan una explicación y una traducción controlada.

### 4.4 Unicidad

Pregunta: **¿cada unidad aparece la cantidad de veces esperada?**

La respuesta depende de la clave y de la unidad:

- un `id` puede ser único a nivel documento;
- un documento puede tener múltiples materias;
- una versión corregida puede compartir identidad documental pero diferir en versión;
- un merge puede multiplicar filas sin que haya nuevos documentos.

La métrica no es “cantidad de filas duplicadas” a secas. Es violaciones de cardinalidad respecto de una clave declarada.

### 4.5 Temporalidad

Pregunta: **¿el dato representa el período correcto y sigue siendo adecuado para el uso?**

En SAIJ puede haber más de un reloj:

- fecha de la decisión;
- fecha de publicación;
- fecha de alta administrativa;
- fecha de actualización.

No deben intercambiarse. La temporalidad también pregunta si entrenar con años lejanos sigue siendo representativo del presente y si una regla de normalización cambió a través del tiempo.

### 4.6 Trazabilidad

Pregunta: **¿podemos saber de dónde vino un valor y qué transformaciones lo produjeron?**

Requiere:

- identificación de fuente;
- versión o fecha de extracción;
- clave estable;
- reglas de transformación;
- mapeos versionados;
- métricas antes/después;
- autor o responsable de decisiones relevantes.

Sin trazabilidad, una corrección correcta hoy se vuelve una incógnita mañana.

### 4.7 Perfil de calidad por decisión

En vez de un informe genérico, conectá cada dimensión con una acción:

| Dimensión | Evidencia | Posible acción | Verificación |
|---|---|---|---|
| Completitud | Ausencia por tipo | Separar no-aplica de perdido | Tasas por subpoblación |
| Validez | Valores fuera de dominio | Corregir, marcar o cuarentenar | Cero violaciones no explicadas |
| Consistencia | Variantes o contradicciones | Mapeo controlado | Colisiones revisadas |
| Unicidad | Claves repetidas | Deduplicar o versionar | Cardinalidad esperada |
| Temporalidad | Relojes mezclados | Renombrar y restringir uso | Rangos y orden temporal |
| Trazabilidad | Origen o regla ausente | Diario y linaje | Reproducción desde raw |

> **Checkpoint 4**
>
> Una columna sin nulos puede fallar en cinco dimensiones. Inventá un ejemplo breve para validez, consistencia, unicidad, temporalidad y trazabilidad.

---

## 5. Valores faltantes: ausencia no significa una sola cosa

### 5.1 Primero: no aplica, perdido o no observado

Antes de elegir una técnica, distinguí:

- **Estructural / no aplica:** el atributo no corresponde a esa unidad.
- **Accidental / perdido:** debería existir, pero no fue registrado o se perdió.
- **No observado por diseño:** decidimos no recolectarlo para ciertas filas.
- **Codificado como valor:** una fuente usa cadena vacía, `0`, `-1`, “s/d” o una plantilla en lugar de nulo.
- **Ausente después de transformación:** el dato existía, pero un parseo o merge falló.

Los cinco pueden verse como `NaN` al final. Su origen cambia la decisión.

### 5.2 Diagnóstico por grupos

El porcentaje global oculta patrones. Para cada campo relevante preguntá:

1. ¿Cómo varía la ausencia por tipo documental?
2. ¿Por año o período?
3. ¿Por provincia o tribunal?
4. ¿Por clase de `fuero`?
5. ¿Por fuente o lote de carga?
6. ¿Coincide con ausencia en otros campos?
7. ¿Apareció después de un merge o una conversión?

**Ejemplo ilustrativo.** Si `tribunal` falta en todos los sumarios pero aparece en casi todos los fallos, probablemente es estructural. Si dentro de fallos falta solo en un lote de un año, puede ser un problema de carga. El mismo nulo cambia de significado al condicionar.

### 5.3 Cuatro familias de estrategia

#### Conservar el nulo

Es correcto cuando la ausencia expresa una realidad que no debe inventarse o cuando el algoritmo posterior puede manejarla y su semántica está documentada.

#### Eliminar filas o columnas

Puede ser razonable si:

- la unidad queda fuera del propósito;
- el campo crítico no puede recuperarse;
- la pérdida es pequeña y no selectiva respecto de grupos relevantes;
- una columna no aporta información suficiente para justificar su costo.

El riesgo es cambiar la población sin notarlo.

#### Imputar

Imputar significa reemplazar una ausencia por una estimación o categoría. No “recupera la verdad”. Puede preservar cantidad de filas, pero añade incertidumbre y puede deformar distribución, relaciones y varianza.

Opciones conceptuales:

- constante explícita, como `NO_APLICA` o `DESCONOCIDO`, sin mezclarlas;
- moda o mediana, con riesgo de concentrar artificialmente;
- valor por grupo, si el grupo tiene fundamento y no usa información futura;
- modelo de imputación, que aprende patrones pero también errores;
- imputación múltiple, que representa incertidumbre con varias versiones, fuera del mínimo operativo de este proyecto.

#### Agregar un indicador

Una bandera como `tribunal_faltante = sí/no` conserva la información de que el dato faltaba, aun si además se imputa. Es útil cuando la ausencia puede contener señal. También puede ser riesgosa si esa señal proviene de un proceso que cambiará en producción.

### 5.4 Estrategia por tipo de ausencia

| Situación | Acción inicial razonable | Riesgo principal |
|---|---|---|
| No aplica por tipo documental | Categoría separada o esquema separado | Confundir con desconocido |
| Perdido en campo no crítico | Conservar o imputar con bandera | Inventar estructura |
| Perdido en target | Excluir del entrenamiento; conservar para análisis | Sesgo de selección |
| Falta tras un merge | Diagnosticar claves antes de imputar | Tapar un join fallido |
| Plantilla textual vacía | Detectar semánticamente y marcar | Contarla como texto real |
| Campo casi vacío | Evaluar utilidad por población | Borrar una señal minoritaria |

### 5.5 Comparar antes y después

Una imputación no se valida porque eliminó nulos. Compará:

- cantidad y tasa imputada;
- distribución de valores;
- centro y dispersión;
- relación con variables relevantes;
- resultados por grupo;
- sensibilidad de conclusiones a otra estrategia.

Si la columna quedó completa pero su varianza colapsó, la completitud mejoró y la fidelidad estadística pudo empeorar.

> **Material complementario integrado 2 — MCAR, MAR y MNAR como contexto opcional (nivel DiploDatos)**
>
> **MCAR** describe una ausencia que no depende ni de variables observadas ni del valor faltante. **MAR** permite que dependa de otras variables observadas. **MNAR** contempla que dependa del propio valor no observado o de información ausente. Sirven para explicitar supuestos, no para etiquetar mecánicamente cada columna. Con los datos observados casi nunca podemos demostrar por completo que un mecanismo es MAR y no MNAR: justamente no vemos el valor faltante. En este proyecto alcanza con formular hipótesis de mecanismo, usar conocimiento del dominio, comparar grupos, hacer análisis de sensibilidad y reconocer incertidumbre. No presentes MCAR/MAR/MNAR como diagnóstico seguro obtenido por una gráfica.

### 5.6 Aplicación SAIJ

> **Hallazgo del notebook del grupo — a reproducir:** el equipo interpreta buena parte de la ausencia como estructural por coexistencia de tipos documentales, y señala algunas excepciones que podrían ser faltantes reales.
>
> **Decisión de Javier — pendiente:** verificar tasas por tipo, definir reglas `NO_APLICA` versus `DESCONOCIDO` y decidir qué población entra a TP2. No imputar texto, tribunal o materia solo para lograr una tabla sin nulos.

> **Error frecuente:** imputar inmediatamente después de calcular `isna()`. La tasa detecta ausencia; no explica su causa.

> **Checkpoint 5**
>
> ¿Por qué un nulo aparecido después de un merge debe investigarse como problema de claves antes de tratarse como dato faltante?

---

## 6. Duplicados: identidad, versiones y similitud

### 6.1 Duplicado exacto

Dos filas coinciden en todas las columnas consideradas. Puede surgir por concatenar dos veces un archivo, repetir una carga o guardar copias idénticas.

Es el caso más fácil, pero aun así hay que revisar si columnas técnicas —fecha de ingesta, índice— impiden detectar una igualdad semántica.

### 6.2 Duplicado por clave

Dos filas comparten la clave que debería ser única, aunque otros campos difieran.

Posibles explicaciones:

- error de carga;
- corrección posterior;
- versiones legítimas;
- clave insuficiente;
- relación uno-a-muchos mal modelada.

No se resuelve con “quedarse con la primera”. Primero se define una regla de precedencia o versionado.

### 6.3 Duplicado cercano

Dos registros difieren poco:

- espacios, mayúsculas o puntuación;
- OCR;
- fecha en distinto formato;
- título abreviado;
- texto con una corrección menor;
- identificador ausente en uno.

Se detecta con reglas de similitud, pero la similitud no prueba identidad.

### 6.4 Duplicado semántico

Dos textos expresan esencialmente el mismo contenido aunque no compartan forma superficial. Puede tratarse de:

- sumario y fallo del mismo caso;
- reproducción editorial;
- cita extensa;
- versión redactada;
- documentos distintos con fórmula jurídica estándar.

Esta categoría requiere conocimiento del dominio y, muchas veces, revisión humana. Un modelo de embeddings puede proponer candidatos; no debería decidir por sí solo qué documento borrar.

### 6.5 Consecuencias analíticas

Los duplicados afectan:

- conteos y proporciones;
- frecuencia de términos;
- distribución de clases;
- importancia aparente de instituciones;
- estimaciones temporales;
- evaluación de modelos.

Si una misma pieza textual cae en train y test, el modelo puede “recordarla”. La métrica parecerá alta sin demostrar generalización.

### 6.6 Duplicados y particiones

La regla conceptual es agrupar entidades relacionadas **antes** de dividir. Si distintas versiones o fragmentos del mismo caso comparten una identidad de grupo, todas deben ir a la misma partición.

```text
documentos → grupos de identidad/duplicación → split por grupo
```

No al revés.

### 6.7 Registro de deduplicación

Una tabla de decisiones debería contener:

| id_conservado | id_relacionado | tipo_relación | evidencia | acción | regla |
|---|---|---|---|---|---|
| A | B | exacto | igualdad normalizada | excluir B de matriz | lote duplicado |
| C | D | versión | misma clave, fecha distinta | conservar última y archivar ambas | versión oficial |
| E | F | cercano dudoso | alta similitud textual | revisión | sin decisión automática |

> **Checkpoint 6**
>
> ¿Por qué dos filas con el mismo `id` y distinto texto podrían revelar un problema de versionado, mientras dos filas con distinto `id` y texto idéntico podrían revelar una carga duplicada? La clave sola no alcanza en ninguno de los casos.

---

## 7. Normalización categórica y tablas de mapeo auditables

### 7.1 Qué problema resuelve normalizar

Las categorías pueden variar por:

- mayúsculas y minúsculas;
- tildes;
- espacios;
- puntuación;
- abreviaturas;
- errores de tipeo;
- cambios históricos;
- sinónimos;
- conceptos realmente distintos.

Las primeras diferencias suelen ser de forma. Las últimas pueden ser semánticas. Una función automática no conoce la frontera.

### 7.2 Separar forma, equivalencia y decisión de negocio

Aplicá tres niveles:

1. **Normalización de forma:** recortar espacios, unificar Unicode, estandarizar separadores.
2. **Corrección conocida:** mapear un error confirmado a una forma canónica.
3. **Agrupación conceptual:** decidir que dos etiquetas pertenecen a una categoría de análisis.

El tercer nivel es el más delicado. Requiere definición de dominio, no solo similitud de caracteres.

### 7.3 Tabla de mapeo

No escondas equivalencias en una cadena larga de reemplazos. Usá una tabla conceptual:

| valor_original | valor_normalizado | categoría_canónica | motivo | confianza | versión | revisión |
|---|---|---|---|---|---|---|
| variante A | VARIANTE A | CANÓNICA | capitalización | alta | v1 | automática |
| error B | ERROR B | CANÓNICA | typo confirmado | alta | v1 | manual |
| etiqueta C | ETIQUETA C | PENDIENTE | ambigua | baja | v1 | humana |

Ventajas:

- se puede auditar;
- conserva el original;
- permite medir cobertura;
- muestra casos no resueltos;
- evita que un cambio silencioso altere todo el corpus;
- facilita comparar versiones.

### 7.4 Métricas de una normalización

Reportá:

- categorías antes y después;
- porcentaje mapeado;
- porcentaje sin cambios;
- porcentaje corregido;
- cantidad de colisiones;
- casos ambiguos;
- frecuencia afectada por cada regla;
- diferencias por período o fuente.

Una caída drástica en cardinalidad no es automáticamente un éxito. Puede indicar sobreagrupación.

### 7.5 Límites del fuzzy matching

El fuzzy matching compara forma textual. Es útil para sugerir candidatos cuando hay typos, pero tiene límites:

- palabras cercanas pueden significar cosas distintas;
- una palabra corta produce coincidencias engañosas;
- el umbral elegido cambia cobertura y falsos positivos;
- los vocabularios evolucionan;
- no comprende jerarquías jurídicas;
- un acierto en ejemplos conocidos no prueba seguridad en todos los casos.

Uso responsable:

1. producir candidatos;
2. guardar puntaje y alternativas;
3. aceptar automáticamente solo reglas de alta confianza ya validadas;
4. enviar casos dudosos a revisión;
5. conservar valor original;
6. medir falsos positivos en una muestra.

> **Hallazgo del notebook del grupo — a reproducir:** el equipo informa haber comparado un diccionario manual con una estrategia fuzzy para variantes de `materia` y haber preferido una base manual por transparencia, usando similitud como apoyo.
>
> **Decisión de Javier — pendiente:** reconstruir el vocabulario, validar cada mapeo y elegir umbral o política de revisión. El resultado del equipo es una hipótesis de trabajo, no una regla heredada.

> **Error frecuente:** creer que “más categorías corregidas” significa mejor normalización. Si se fusionan etiquetas legítimas, aumentó el daño.

> **Checkpoint 7**
>
> Explicá por qué una tabla de mapeo con diez casos pendientes puede ser metodológicamente mejor que una función que fuerza el 100% a una categoría.

---

## 8. Construir y validar el target `fuero` desde `materia`

### 8.1 El target construido no es una verdad dada

Si el dataset no incluye `fuero` como etiqueta directa y estable, derivarlo desde `materia` crea una **variable construida**. Esa variable depende de reglas humanas. El modelo futuro aprenderá esas reglas y sus errores.

Antes de escribir el mapeo, definí qué significa `fuero` para el proyecto:

- ¿una sola clase por documento?
- ¿varias ramas por documento?
- ¿rama sustantiva principal?
- ¿incluye dimensiones procesales?
- ¿qué se hace con materias compuestas?
- ¿quién resuelve ambigüedades?

### 8.2 Materias sustantivas, transversales y fuera de alcance

Una taxonomía de trabajo puede separar:

- **Etiquetas sustantivas candidatas a fuero:** ramas que el proyecto desea predecir.
- **Etiquetas transversales:** dimensiones que pueden aparecer en muchas ramas, como aspectos procesales o constitucionales según la definición adoptada.
- **Etiquetas compuestas:** combinaciones de dos o más ramas.
- **Ambiguas:** no permiten asignación confiable sin contexto.
- **Fuera de alcance:** categorías administrativas, temáticas o documentales que no responden al target.

Esta clasificación no debe presentarse como doctrina jurídica universal. Es una definición operacional del proyecto, a validar con mentores o especialistas.

### 8.3 ¿Clase única o multietiqueta?

**Clase única:** cada documento recibe un fuero principal.

- Ventaja: simplifica modelado y evaluación.
- Riesgo: borra coexistencias reales y obliga a decidir prioridad.

**Multietiqueta:** cada documento puede tener varios fueros.

- Ventaja: conserva combinaciones.
- Riesgo: aumenta complejidad, exige métricas específicas y suficientes ejemplos por combinación.

**Estrategia intermedia:** entrenar una primera versión con casos claros de una sola etiqueta y reservar combinaciones para análisis o etapa posterior. Esto acota alcance sin fingir que los casos complejos no existen.

### 8.4 Pipeline conceptual del target

```text
materia_raw
  → normalización de forma
  → tokenización que protege expresiones compuestas
  → mapeo a vocabulario canónico
  → clasificación sustantiva/transversal/ambigua
  → aplicación de política de clase única o multietiqueta
  → target_fuero + estado_target + versión_regla
```

Campos derivados recomendados:

- `materia_raw`;
- `materia_normalizada`;
- `fuero_candidato`;
- `estado_target` = claro / compuesto / transversal / ambiguo / fuera_de_alcance;
- `regla_target_version`;
- `requiere_revision`.

### 8.5 Validación del target

No basta con contar clases. Validá:

1. **Cobertura:** qué proporción recibe target.
2. **Ambigüedad:** cuántos casos requieren decisión.
3. **Estabilidad:** si la regla da resultados similares por período y fuente.
4. **Consistencia externa interna al corpus:** si otras metadata compatibles contradicen sistemáticamente el target.
5. **Muestra manual:** revisión estratificada por clase y por tipo de regla.
6. **Colisiones:** materias distintas fusionadas.
7. **Reproducibilidad:** misma entrada y versión producen la misma salida.

Si se usa información de tribunal para validar, no se sigue automáticamente que tribunal sea una feature segura. Una variable puede servir para **control de calidad** y estar prohibida para **predicción**.

### 8.6 Casos ambiguos

Nunca fuerces un caso ambiguo solo para completar la etiqueta. Alternativas:

- dejarlo sin target para entrenamiento;
- asignarlo a revisión humana;
- mantener varias etiquetas;
- crear una clase “otro” solo si tiene significado y suficiente coherencia;
- excluirlo de la primera versión, conservándolo en raw y en un conjunto de pendientes.

> **Checkpoint 8**
>
> Si `tribunal` coincide mucho con el `fuero` construido, ¿por qué eso puede aumentar confianza en la etiqueta y al mismo tiempo convertir `tribunal` en una feature dudosa o prohibida?

---

## 9. Curación de texto legal: conservar significado, no solo caracteres

### 9.1 Siempre preservar el texto crudo

El texto original es la evidencia. Toda representación limpia debe ser derivada:

- `texto_raw`: sin sobrescritura;
- `texto_limpio_v1`: transformaciones mínimas;
- `texto_modelo_v1`: preparación específica para una representación;
- métricas y versión de reglas.

Esto permite cambiar de criterio sin volver a descargar la fuente y revisar qué eliminó cada paso.

### 9.2 Unicode y encoding

Caracteres visualmente iguales pueden tener codificaciones distintas. También pueden aparecer:

- secuencias mal decodificadas;
- comillas tipográficas;
- guiones diferentes;
- espacios no separables;
- caracteres de control;
- letras compuestas de varias maneras Unicode.

Normalizar Unicode ayuda a comparar y tokenizar, pero debe hacerse en una columna derivada. Un reemplazo incorrecto puede borrar símbolos jurídicos o números de expediente.

### 9.3 Whitespace

Es razonable:

- unificar saltos de línea cuando no aportan estructura;
- colapsar espacios repetidos;
- quitar espacios al inicio y al final;
- convertir tabs de formato.

No siempre conviene eliminar todos los saltos. Párrafos, encabezados y listas pueden contener información estructural. La decisión depende de la representación posterior.

### 9.4 Mayúsculas, minúsculas y tildes

Pasar a minúsculas reduce vocabulario superficial. Quitar tildes puede facilitar coincidencias. Pero hay costos:

- siglas pueden perder señal de forma;
- nombres propios e instituciones se vuelven menos distinguibles;
- la legibilidad baja;
- dos cadenas distintas pueden colisionar.

Para BoW o TF-IDF, minúsculas puede ser razonable. Para un modelo contextual, quizá no haga falta. Para auditoría humana, siempre se conserva el original.

### 9.5 Puntuación

Eliminar toda puntuación sin pensar puede destruir:

- números de ley;
- artículos;
- incisos;
- abreviaturas;
- identificadores;
- separaciones de referencias;
- negación asociada a una expresión.

Podemos normalizar puntuación decorativa y preservar patrones significativos. La regla debe responder a la tarea, no a una receta genérica de internet.

### 9.6 Stopwords

Las stopwords son palabras muy frecuentes que a veces aportan poca discriminación. Sin embargo, en texto legal algunas cumplen funciones decisivas.

- “no”, “sin” y “nunca” expresan negación;
- preposiciones pueden formar expresiones jurídicas;
- auxiliares pueden cambiar modalidad;
- términos institucionales frecuentes pueden ser ruido para distinguir fuero, pero útiles para detectar fuente o estilo.

No existe una lista universal. Compará representaciones con y sin ciertas stopwords y documentá qué se preserva.

### 9.7 Negación

La diferencia entre “se hace lugar” y “no se hace lugar” puede depender de una palabra. Eliminar `no` por pertenecer a una lista general de stopwords invierte el significado.

Opciones acotadas:

- conservar términos de negación;
- formar bigramas como `no_corresponde`;
- preservar una ventana alrededor de negaciones;
- inspeccionar errores en ejemplos reales.

No hace falta resolver NLP avanzado aquí. Sí reconocer que una limpieza agresiva puede destruir la señal.

### 9.8 Lematización

Lematizar intenta llevar variantes flexivas a una forma base. Puede reducir dispersión, pero:

- depende del analizador;
- puede equivocarse en lenguaje jurídico;
- pierde matices gramaticales;
- cuesta más que una normalización superficial;
- no siempre mejora una representación contextual.

La decisión se valida comparando objetivos. No se prescribe por costumbre.

### 9.9 Términos de dominio e identificadores significativos

En documentos legales pueden ser importantes:

- números de ley y artículo;
- siglas de tribunales;
- números de expediente;
- tipos de recurso;
- denominaciones institucionales;
- fechas;
- montos;
- nombres propios.

Algunos son señal jurídica legítima; otros generan memorización, privacidad o fuga. Por eso conviene distinguir:

- **contenido semántico generalizable**;
- **identificador de caso**;
- **marca de fuente o jurisdicción**;
- **dato sensible**;
- **información posterior al evento objetivo**.

> **Material complementario integrado 5 — Normalización de texto legal (nivel DiploDatos)**
>
> La regla práctica es conservadora: preservar `raw`, normalizar Unicode y whitespace de forma reversible, no eliminar negación, y tratar números de ley, artículos, expedientes, siglas y nombres como decisiones de dominio. “Sacar todo lo que no sea letra” es una mala regla por defecto para jurisprudencia. Puede destruir la diferencia entre normas, casos y resultados. En esta etapa alcanza con crear dos o tres variantes comparables y justificar cuál se usa para qué.

### 9.10 Markup y plantillas

Los marcadores técnicos pueden contaminar longitud y vocabulario. Antes de removerlos:

1. identificá patrones;
2. comprobá que son formato y no contenido;
3. medí cuántos textos afectan;
4. guardá el original;
5. verificá ejemplos antes/después;
6. detectá textos que quedan vacíos.

Una cadena plantilla repetida puede parecer texto válido si solo se mide longitud. La curación semántica necesita reconocerla.

> **Hallazgo del notebook del grupo — a reproducir:** el equipo informa que el campo textual candidato contiene marcas de formato y que probó su remoción antes del análisis léxico. También diferencia texto narrativo de metadata breve.
>
> **Decisión de Javier — pendiente:** reproducir muestras, definir reglas mínimas y comparar variantes. No asumir que la pipeline del grupo es universal ni final.

> **Checkpoint 9**
>
> Proponé una razón para conservar un número de ley y otra para enmascarar un número de expediente. Ambas decisiones deben referirse a generalización, privacidad o fuga.

---

## 10. Longitudes textuales inusuales y outliers

### 10.1 Longitud como variable derivada

Podemos medir:

- caracteres;
- palabras;
- tokens;
- oraciones;
- párrafos;
- proporción de caracteres no alfabéticos.

Cada medida responde algo distinto. La cantidad de tokens depende del tokenizador; no es una propiedad absoluta del documento.

### 10.2 Textos muy cortos

Pueden ser:

- título o metadata en el campo equivocado;
- plantilla;
- documento truncado;
- texto legítimamente breve;
- error de parseo;
- referencia a otro documento.

No se eliminan por umbral sin inspección. Un texto de cinco palabras puede ser inválido para entrenar, pero válido para documentar la fuente.

### 10.3 Textos muy largos

Pueden ser:

- fallo completo en un campo pensado para sumario;
- concatenación accidental;
- markup no removido;
- documento histórico extenso;
- repetición;
- caso válido de alta complejidad.

La cola larga es común en lenguaje natural. La regla IQR puede marcar muchos casos legítimos porque la distribución es asimétrica.

### 10.4 Diagnóstico de outliers textuales

Para cada extremo:

1. verificar tipo documental;
2. abrir una muestra;
3. buscar repetición o concatenación;
4. comparar longitud antes/después de markup;
5. revisar período y fuente;
6. comprobar si existe texto duplicado;
7. decidir tratamiento específico.

### 10.5 Acciones posibles

- conservar;
- marcar con `longitud_extrema`;
- separar por tipo;
- truncar solo en la entrada de un modelo, no en raw;
- segmentar en fragmentos con identidad del documento;
- excluir de una tarea concreta y registrar;
- reparar si hay error determinístico.

### 10.6 Verificación

No alcanza con ver un histograma más compacto. Medí:

- filas afectadas;
- distribución por clase;
- pérdida de tokens;
- proporción de documentos truncados;
- cambio en representación de grupos;
- sensibilidad de conclusiones.

> **Error frecuente:** llamar “ruido” a todo lo que queda fuera de los bigotes del boxplot. El boxplot señala rareza estadística, no invalidez jurídica.

> **Checkpoint 10**
>
> Un documento histórico muy largo es válido pero excede el límite del modelo. Diseñá una solución que preserve el documento, permita modelar y deje rastrear qué fragmentos provienen de él.

---

## 11. Features, variables derivadas y metadata

### 11.1 Feature no es sinónimo de columna disponible

Una feature es una entrada autorizada para una tarea. Para decidir si una columna sirve preguntá:

- ¿estará disponible al momento real de predecir?
- ¿su significado es estable?
- ¿deriva directa o indirectamente del target?
- ¿identifica el caso?
- ¿representa contenido o un atajo de fuente?
- ¿introduce una dimensión ética o legal?
- ¿puede reproducirse sobre datos nuevos?

### 11.2 Variables derivadas

Ejemplos:

- longitud de texto;
- año de decisión;
- cantidad de descriptores;
- indicador de ausencia;
- cantidad de materias;
- tipo documental;
- densidad de puntuación;
- representación numérica de texto.

Cada derivación necesita:

- definición;
- campos de origen;
- momento de cálculo;
- versión;
- disponibilidad;
- riesgo.

### 11.3 Clasificación segura, dudosa y prohibida

La clasificación depende del objetivo. Para predecir `fuero` desde contenido textual, una matriz preliminar podría ser:

| Grupo | Ejemplos | Razón |
|---|---|---|
| **Seguras en principio** | texto disponible antes de etiquetar, longitud, rasgos de formato estables | Pueden representar contenido accesible al momento de predicción. Igual requieren validación. |
| **Dudosas** | provincia, tribunal, año, descriptores humanos, tipo de fuente | Pueden ser señal legítima, pero también atajos, sesgo o información de cobertura. |
| **Prohibidas para el modelo** | `materia` usada para construir `fuero`, `fuero` textual explícito, columnas derivadas del target, identificador que permite memorizar | Revelan la respuesta o impiden generalización. |
| **Solo auditoría** | regla que creó el target, estado de revisión, versión de mapeo | Necesarias para trazabilidad, no para aprender. |

No tomes esta tabla como decisión final. Es una plantilla para que Javier justifique su versión.

### 11.4 Metadata humana

Los descriptores pueden contener conocimiento experto. Eso no los vuelve automáticamente seguros.

Preguntas:

- ¿se asignan antes o después del target?
- ¿usan la misma taxonomía?
- ¿estarán disponibles en el caso nuevo?
- ¿contienen términos que codifican la respuesta?
- ¿su cobertura es uniforme por período y tribunal?
- ¿dependen de una práctica editorial que puede cambiar?

Una feature poderosa puede ser un atajo frágil.

### 11.5 Ablación conceptual

Para features dudosas, planificá comparar:

1. texto solo;
2. texto + feature;
3. feature sola.

Si la feature sola resuelve casi el problema, investigá si representa información legítima o fuga. Este es solo un diseño de comprobación; la ejecución pertenece a IAA.

> **Checkpoint 11**
>
> ¿Por qué `provincia` podría mejorar una métrica y empeorar la validez del modelo? Mencioná asociación geográfica, cobertura y cambio de dominio.

---

## 12. Sesgo y representatividad después de curar

### 12.1 El dataset curado define una nueva población

Cada filtro cambia quién queda representado. Después de curar, repetí perfiles por:

- período;
- provincia;
- tribunal;
- tipo documental;
- clase objetivo;
- longitud;
- disponibilidad de texto.

Compará `raw` y `clean`. Si una regla elimina mucho más de una provincia o clase, el impacto debe justificarse.

### 12.2 Sesgo temporal

Puede surgir por:

- cobertura desigual entre épocas;
- cambios de vocabulario;
- reformas legales;
- digitalización;
- criterios editoriales;
- fechas administrativas confundidas con judiciales;
- reglas de curación que funcionan peor en documentos antiguos.

Una muestra aleatoria puede mezclar pasado y futuro de forma poco realista.

### 12.3 Sesgo geográfico

El corpus puede reflejar disponibilidad de digitalización y no incidencia real de litigios. Si una jurisdicción domina, un modelo puede aprender nombres, fórmulas o instituciones locales.

No corresponde convertir cobertura documental en afirmación causal sobre actividad social o judicial sin evidencia externa.

### 12.4 Sesgo de tribunal

Tribunales pueden tener estilos, plantillas y vocabulario propios. Si ciertos tribunales se asocian con fueros, el modelo puede aprender estilo institucional en vez de contenido jurídico.

Verificación conceptual:

- evaluar por tribunal;
- separar grupos de tribunal entre particiones;
- revisar términos distintivos;
- comparar desempeño en instituciones poco vistas.

### 12.5 Sesgo de tipo documental

Sumarios y fallos difieren en longitud, estructura y disponibilidad de campos. Entrenar en uno y evaluar mezclado con otro puede medir reconocimiento del tipo, no del fuero.

Primero debe definirse la población objetivo. Después se decide si existe un modelo por tipo o una representación común.

### 12.6 Sesgo de procesamiento

Lo introducimos al:

- eliminar outliers;
- imputar con una regla global;
- normalizar de forma desigual;
- descartar clases pequeñas;
- seleccionar solo textos completos;
- resolver ambigüedades siempre hacia la clase mayoritaria.

Documentar no elimina el sesgo, pero permite medirlo y discutirlo.

> **Hallazgo del notebook del grupo — a reproducir:** el equipo reporta concentraciones geográficas, variación temporal, desbalance de clases y posibles asociaciones entre metadata y fuero. También distingue fecha judicial de fecha administrativa.
>
> **Decisión de Javier — pendiente:** reproducir con denominadores claros, evitar explicaciones causales no verificadas y decidir una estrategia de partición compatible con el uso esperado.

> **Checkpoint 12**
>
> Si una regla de “texto suficiente” elimina el doble de documentos antiguos que recientes, ¿qué población termina aprendiendo el modelo y qué comparación antes/después deberías reportar?

---

## 13. Fugas de información y fronteras train/validación/test

### 13.1 Qué es leakage

Hay fuga cuando el proceso usa información que no estaría legítimamente disponible en el momento de predicción o cuando la evaluación deja entrar conocimiento del conjunto reservado. El resultado suele parecer mejor de lo que generaliza.

### 13.2 Target leakage

Ejemplos:

- usar `materia` si de allí se derivó `fuero`;
- conservar una frase o etiqueta que declara explícitamente el fuero;
- usar una metadata creada después de la clasificación;
- imputar una feature con el target sin encapsular correctamente el procedimiento.

La regla es examinar linaje: ¿de qué campos y momento proviene cada feature?

### 13.3 Duplicate leakage

Ocurre cuando el mismo documento, una versión cercana o un fragmento relacionado aparece en particiones distintas. El modelo reconoce contenido visto.

Prevención:

- definir grupos de identidad;
- detectar duplicados antes del split;
- dividir por grupo, no por fila;
- auditar similitud cruzada entre particiones.

### 13.4 Temporal leakage

Ocurre al usar futuro para predecir pasado:

- datos posteriores en train;
- metadata de carga futura;
- estadísticas calculadas con todo el período;
- normalizaciones aprendidas con categorías futuras;
- split aleatorio cuando el escenario real es predecir documentos venideros.

La solución puede ser split temporal, pero debe respetar la pregunta real.

### 13.5 Preprocessing leakage

Aparece cuando una transformación aprende parámetros usando validación o test:

- media de imputación;
- vocabulario;
- IDF;
- escalado;
- selección de features;
- umbral aprendido;
- categorías del encoder;
- reducción dimensional.

Aunque no use el target, incorpora información de la distribución reservada.

> **Material complementario integrado 4 — Fit-on-train y fuga de preprocesamiento (nivel DiploDatos)**
>
> **Fit** significa aprender algo de los datos: una media, un vocabulario, pesos IDF, categorías o un umbral. Ese aprendizaje se hace solo con train. Luego la transformación aprendida se aplica, sin recalcular, a validación y test. La secuencia conceptual es: primero separar; después ajustar el preprocesamiento en train; finalmente transformar los tres conjuntos con el mismo objeto. Explorar el dataset completo antes del modelado puede ser útil para comprenderlo, pero cualquier evaluación final exige reconstruir la pipeline respetando esta frontera.

### 13.6 Train, validación y test

- **Train:** permite aprender parámetros del preprocesamiento y del modelo.
- **Validación:** permite comparar alternativas y ajustar decisiones.
- **Test:** se reserva para una estimación final; no guía iteraciones.

Si se mira repetidamente test para decidir, test se convierte de hecho en validación. Haría falta otro conjunto realmente reservado.

### 13.7 Estrategias de split conceptuales

#### Aleatorio estratificado

Conserva aproximadamente proporciones de clase. Útil si los casos futuros se parecen a una mezcla aleatoria del mismo universo. No protege por sí solo de duplicados, tiempo o tribunales.

#### Por grupos

Mantiene todos los documentos relacionados en una partición. Útil para versiones, expedientes, tribunales o fuentes según el riesgo.

#### Temporal

Entrena con pasado y evalúa en futuro. Se acerca a despliegues prospectivos y revela deriva. Puede producir clases ausentes si la taxonomía cambia.

#### Híbrido

Combina tiempo, grupos y estratificación dentro de lo posible. No existe una división perfecta; se documenta qué riesgo prioriza.

### 13.8 Sin convertir esto en IAA

Aquí no elegimos algoritmo ni métrica final. Solo establecemos que la curación y el split no son pasos independientes. Una base “limpia” puede seguir produciendo una evaluación inválida si su pipeline aprendió de test.

> **Checkpoint 13**
>
> ¿Por qué calcular TF-IDF sobre todo el corpus antes de separar es fuga, aunque no hayas usado `fuero`? Explicá qué aprendió el IDF del conjunto reservado.

---

## 14. Representaciones numéricas de texto: anticipo para decidir la curación

Los modelos trabajan con números. Representar texto es decidir qué aspectos conservar. Este bloque es un anticipo de preparación, no una clase avanzada de NLP.

### 14.1 Bag of Words

BoW crea una dimensión por término y cuenta apariciones.

Conserva:

- presencia;
- frecuencia;
- vocabulario superficial.

Pierde:

- orden;
- contexto;
- gran parte de la semántica;
- relación entre sinónimos.

Decisiones de curación relacionadas:

- tokenización;
- minúsculas;
- puntuación;
- stopwords;
- n-gramas;
- vocabulario mínimo;
- tratamiento de identificadores.

Es interpretable: podemos ver qué términos pesan. Pero puede producir matrices enormes y esparsas.

### 14.2 TF-IDF

TF-IDF aumenta el peso de términos frecuentes en un documento pero menos comunes en el corpus. Ayuda a destacar vocabulario distintivo.

No significa “importancia jurídica”. Significa rareza relativa bajo una colección y una configuración.

El IDF se aprende. Por eso debe ajustarse solo con train. Si el vocabulario o la frecuencia cambian por época, también cambia la representación.

### 14.3 Embeddings

Los embeddings convierten textos o términos en vectores densos donde cercanía intenta capturar similitud contextual o semántica.

Ventajas:

- pueden acercar expresiones relacionadas;
- reducen dimensionalidad respecto de vocabularios enormes;
- aprovechan representaciones preentrenadas.

Riesgos:

- menor interpretabilidad;
- sesgos heredados;
- truncamiento;
- dependencia de versión;
- similitud no equivale a identidad jurídica;
- posible costo computacional;
- cambios entre modelos.

En esta materia basta con registrar modelo, versión, texto de entrada, estrategia de segmentación y momento de cálculo.

### 14.4 Comparación de decisión

| Representación | Qué necesita de curación | Riesgo típico | Uso pedagógico |
|---|---|---|---|
| BoW | vocabulario y tokenización explícitos | dimensionalidad, pérdida de contexto | entender conteos |
| TF-IDF | lo anterior + corpus de ajuste | leakage en IDF, confundir peso con relevancia | términos distintivos |
| Embeddings | texto preservado, segmentación y versión | opacidad, sesgo, truncamiento | similitud semántica preliminar |

### 14.5 No hay pipeline universal

Una limpieza agresiva quizá ayude a BoW y perjudique embeddings. Lematizar puede reducir variantes, pero eliminar información útil. Mantener puntuación puede favorecer modelos contextuales. La decisión se compara, no se proclama.

> **Checkpoint 14**
>
> ¿Por qué la misma frase puede quedar muy lejos en BoW por usar sinónimos y relativamente cerca en embeddings? ¿Qué riesgo introduce confiar ciegamente en esa cercanía?

---

## 15. Reproducibilidad: raw, clean, versiones y diario

### 15.1 Separación raw/clean

- **Raw:** copia inmutable de lo recibido, con identificación de origen.
- **Clean/curated:** resultado regenerable de reglas versionadas.
- **Analytic/model:** vista específica para una pregunta o partición.

Nunca sobrescribas raw con clean. Si el proceso cambia, generá una nueva versión.

### 15.2 Versionado

Versionar significa poder identificar:

- versión o huella de la fuente;
- versión del código o notebook;
- versión del mapeo;
- versión del target;
- parámetros;
- fecha de ejecución;
- dependencias relevantes.

No hace falta una infraestructura compleja. Un manifiesto y nombres coherentes pueden bastar para un TP.

### 15.3 Semillas aleatorias

Una semilla controla operaciones aleatorias reproducibles:

- muestreo para revisión;
- división de datos;
- ciertos imputadores;
- inicialización de algoritmos.

La semilla no garantiza reproducibilidad total si cambian datos, bibliotecas o hardware. Es una pieza del registro.

### 15.4 Diccionario de datos

Para cada campo:

| Elemento | Contenido |
|---|---|
| Nombre | nombre técnico |
| Significado | definición en lenguaje claro |
| Unidad | documento, asignación, fecha, etc. |
| Tipo | lógico y técnico |
| Dominio | valores o reglas |
| Ausencia | no aplica, desconocido, no permitido |
| Origen | fuente o derivación |
| Disponibilidad | antes o después del target |
| Riesgo | sesgo, fuga, privacidad |
| Versión | regla vigente |

### 15.5 Diario de transformaciones

Cada paso debería registrar:

1. identificador;
2. problema observado;
3. evidencia;
4. acción;
5. filas/columnas afectadas;
6. riesgo;
7. verificación;
8. responsable;
9. versión.

Ejemplo de estructura:

| paso | evidencia | acción | antes | después | verificación |
|---|---|---|---|---|---|
| C-07 | variantes de forma | aplicar mapeo v1 | N categorías | M categorías | revisar colisiones |
| C-08 | textos con markup | crear texto_limpio | tasa con marca | cero marcas esperadas | muestra pareada |
| C-09 | duplicados por grupo | asignar grupo | pares candidatos | grupos resueltos/pendientes | no cruzan splits |

### 15.6 Métricas antes/después

Como mínimo:

- filas;
- unidades únicas;
- columnas;
- distribución por tipo;
- distribución de target;
- faltantes por grupo;
- duplicados por definición;
- cardinalidad de categorías;
- longitud textual;
- rango temporal;
- cobertura geográfica;
- cantidad en cuarentena.

Una transformación se evalúa por el problema que pretendía resolver y por daños colaterales.

### 15.7 Prueba de reconstrucción

La pregunta final es:

> Si mañana desaparece el DataFrame curado pero conservamos raw, reglas, mapeos y parámetros, ¿podemos regenerarlo?

Si la respuesta depende de recordar una celda ejecutada manualmente, falta reproducibilidad.

> **Checkpoint 15**
>
> ¿Qué información mínima guardarías para reproducir una muestra manual estratificada de cien documentos y saber exactamente qué versión de texto revisaste?

---

## 16. ETL, linaje y contratos livianos

### 16.1 ETL como forma de ordenar

ETL significa:

1. **Extract:** obtener datos de la fuente;
2. **Transform:** aplicar reglas;
3. **Load:** guardar el resultado en un destino.

ELT cambia el orden: carga primero raw y transforma después. Para este proyecto importa la idea, no montar una plataforma.

Un flujo acotado puede ser:

```text
fuente SAIJ
  → snapshot raw
  → validación de esquema
  → separación de poblaciones
  → normalización y target
  → curación textual
  → deduplicación y split
  → dataset analítico versionado
```

### 16.2 Linaje

El linaje responde:

- ¿de qué fuente vino esta columna?
- ¿qué regla la transformó?
- ¿qué versión produjo este archivo?
- ¿qué campos alimentaron el target?
- ¿qué filas fueron excluidas y dónde quedaron?

Se puede representar con una tabla o diagrama simple. No hace falta una herramienta corporativa.

### 16.3 Contrato de datos

Un contrato liviano declara expectativas que deberían hacer fallar la pipeline si se violan:

- campos requeridos;
- tipos;
- claves;
- dominios;
- cardinalidad;
- reglas condicionales;
- rangos temporales;
- tolerancias de faltantes;
- semántica de cada fecha;
- versión del esquema.

Ejemplo conceptual:

| Regla | Expectativa | Respuesta al fallo |
|---|---|---|
| Identidad | `id_documento` presente y formato válido | cuarentena |
| Tipo | valor dentro del vocabulario conocido | detener o revisar |
| Target | no usar `materia` como feature | prueba de columnas prohibidas |
| Split | un grupo documental no cruza particiones | detener |
| Texto | raw preservado; limpio derivado | detener |
| Tiempo | fecha de decisión no se reemplaza por fecha de carga | detener |

### 16.4 Contrato no significa rigidez ciega

Los datos reales cambian. El contrato debe distinguir:

- error que exige detener;
- cambio esperado que exige nueva versión;
- advertencia;
- caso enviable a cuarentena.

Si aparece un nuevo tipo documental, forzarlo al tipo más parecido para “cumplir” el contrato sería peor que fallar.

> **Material complementario integrado 3 — Contratos livianos y linaje (nivel DiploDatos)**
>
> Para TP2 alcanza con dos artefactos: una tabla de expectativas y un mapa de columnas derivadas. El contrato dice qué debería llegar y qué hacer si no ocurre; el linaje dice de dónde salió cada resultado. No hace falta Airflow, un data lake ni una herramienta de catálogo. La meta es que un error de esquema sea visible y que una feature pueda rastrearse hasta raw.

### 16.5 Cargas y uniones

Si TP2 incorpora otra fuente:

- declarar clave y cardinalidad esperada;
- normalizar tipos de clave;
- medir cobertura de match;
- verificar que las filas no se multipliquen;
- distinguir ausencia original de ausencia post-join;
- registrar procedencia de columnas nuevas.

Una unión exitosa en código puede ser conceptualmente incorrecta.

> **Checkpoint 16**
>
> ¿Qué debería hacer un contrato si aparece una categoría de tipo documental desconocida: convertirla automáticamente a “otro”, detener, advertir o cuarentenar? Proponé una política y justificá el riesgo.

---

## 17. Roadmap detallado SAIJ para TP2

### 17.1 Alcance y honestidad

Esta sección propone cómo transformar el diagnóstico en un trabajo de curación. **No afirma conocer una consigna oficial de TP2 distinta de las fuentes permitidas.** Debe contrastarse con la consigna que Javier reciba. El notebook del equipo funciona como roadmap contextual, no como autoridad ni como evidencia reproducida.

El objetivo de una primera versión acotada puede formularse así:

> Construir un dataset versionado de documentos SAIJ aptos para una futura clasificación de fuero, con población, target, texto, particiones y exclusiones explícitas, evitando fuga y conservando trazabilidad.

### 17.2 Fase A — Congelar fuente y propósito

**Preguntas:**

- ¿Qué snapshot se usa?
- ¿Cuál es la unidad?
- ¿Qué tipos documentales entran?
- ¿Qué significa predecir `fuero`?
- ¿En qué momento estaría disponible cada feature?

**Entregables conceptuales:**

- ficha de fuente;
- definición de población;
- diccionario inicial;
- lista de columnas prohibidas.

**Criterio de salida:** otra persona puede explicar qué representa una fila y qué queda fuera.

### 17.3 Fase B — Reproducir el diagnóstico estructural

Acciones:

1. inventariar columnas y tipos;
2. identificar tipos documentales con reglas verificables;
3. perfilar faltantes por tipo;
4. revisar campos plantilla o vacíos;
5. confirmar claves y cardinalidades;
6. comparar con los hallazgos del grupo sin asumirlos.

**Criterio de salida:** cada patrón de ausencia relevante se clasifica como estructural, accidental, post-transformación o pendiente.

### 17.4 Fase C — Definir población y cuarentena

Separar:

- población de entrenamiento candidata;
- documentos válidos fuera de alcance;
- errores confirmados;
- casos ambiguos;
- duplicados o versiones pendientes.

No borrar. Asignar motivos.

**Criterio de salida:** el conteo se reconcilia:

```text
raw = incluidos + fuera_de_alcance + cuarentena + excluidos_justificados
```

### 17.5 Fase D — Construir el target

1. preservar `materia_raw`;
2. normalizar forma;
3. aplicar tabla de mapeo versionada;
4. proteger expresiones compuestas;
5. clasificar etiquetas transversales;
6. marcar ambigüedad;
7. decidir clase única o multietiqueta;
8. revisar muestra estratificada;
9. medir cobertura y cambios por grupo.

**Criterio de salida:** cada target puede rastrearse a materia y regla; ninguna feature del modelo deriva del target.

### 17.6 Fase E — Curar texto

Crear variantes, no sobrescribir:

- raw;
- mínima: Unicode, whitespace y markup validado;
- experimental para BoW/TF-IDF;
- opcional para embeddings.

Verificar:

- textos vacíos;
- longitudes;
- negación;
- identificadores;
- cambios de tokens;
- ejemplos pareados.

**Criterio de salida:** se puede explicar qué pierde cada variante.

### 17.7 Fase F — Resolver duplicados y grupos

1. exactos;
2. claves repetidas;
3. candidatos cercanos;
4. relaciones sumario–fallo o versión;
5. grupos de split.

**Criterio de salida:** ningún grupo de identidad cruza particiones; los casos dudosos siguen visibles.

### 17.8 Fase G — Seleccionar features

Construir registro:

| feature | origen | momento disponible | riesgo | uso |
|---|---|---|---|---|
| texto limpio | texto raw | antes | bajo/medio | candidata |
| longitud | texto | antes | bajo | candidata |
| provincia | metadata | antes | sesgo/atajo | experimento controlado |
| tribunal | metadata | depende | atajo | dudosa |
| descriptores | indexación humana | verificar | fuga/cobertura | dudosa |
| materia | fuente del target | revela respuesta | fuga | prohibida |

**Criterio de salida:** el conjunto seguro funciona sin columnas prohibidas.

### 17.9 Fase H — Diseñar particiones

Elegir entre:

- split temporal;
- por grupo documental;
- combinación;
- estratificación donde no rompa el criterio principal.

Aplicar split antes de ajustar:

- imputadores;
- vocabulario;
- TF-IDF;
- categorías;
- umbrales aprendidos;
- selección de features.

**Criterio de salida:** tabla de particiones, rangos temporales y distribución de clases; test no guio decisiones.

### 17.10 Fase I — Verificar sesgo y estabilidad

Comparar raw, incluidos y cada partición por:

- tiempo;
- provincia;
- tribunal;
- tipo;
- fuero;
- longitud;
- cobertura de texto;
- reglas de exclusión.

**Criterio de salida:** las diferencias importantes están explicadas o disparan revisión.

### 17.11 Fase J — Empaquetar y documentar

Entregables:

- dataset raw identificado;
- dataset curado;
- diccionario;
- tabla de mapeo;
- diario;
- contrato;
- manifiesto de versiones;
- reporte de métricas antes/después;
- lista de pendientes.

**Criterio de salida:** una persona puede regenerar y auditar el resultado.

### 17.12 Matriz de decisiones de TP2

La matriz obliga a no saltar de problema a acción. En `decisión elegida`, Javier debe escribir su propia conclusión después de reproducir evidencia.

| Problema observado | Evidencia necesaria | Acciones posibles | Riesgo de actuar | Decisión elegida | Verificación |
|---|---|---|---|---|---|
| Poblaciones mezcladas | Cobertura de campos por tipo y muestra de filas | separar vistas; excluir un tipo; esquema condicional | eliminar documentos válidos o mezclar unidades | **Pendiente de Javier** | conteos reconciliados y reglas por tipo |
| Nulos en `tribunal` | tasa por tipo, período y fuente | no-aplica; desconocido; revisar carga; excluir de una tarea | imputar institución inexistente | **Pendiente de Javier** | matriz de ausencia antes/después |
| Registros sin identidad útil | inspección de contenido y claves | cuarentena; exclusión; reconstrucción | borrar casos recuperables | **Pendiente de Javier** | lista de ids/motivos y suma de población |
| Variantes de `materia` | frecuencias, vecinos, revisión jurídica | mapeo manual; fuzzy asistido; pendiente | fusionar materias distintas | **Pendiente de Javier** | colisiones, cobertura y muestra |
| Etiquetas transversales | definición operacional y ejemplos | remover del target; mantener multietiqueta; clase aparte | simplificar doctrina de forma incorrecta | **Pendiente de Javier** | revisión estratificada |
| Materias compuestas | frecuencia y casos | multietiqueta; prioridad; primera versión con casos puros | perder complejidad o crear clases escasas | **Pendiente de Javier** | cobertura y distribución |
| Markup textual | patrones y textos pareados | remover con regla; conservar estructura; marcar | borrar contenido | **Pendiente de Javier** | muestras y tasa de texto vacío |
| Textos muy cortos/largos | distribución por tipo y muestra | conservar; marcar; segmentar; excluir de modelo | sesgo temporal o documental | **Pendiente de Javier** | impacto por grupo |
| Duplicados | claves, hashes, similitud y versiones | deduplicar; agrupar; versionar; revisar | perder documentos relacionados | **Pendiente de Javier** | unidades únicas y cero cruce de grupos |
| Desbalance de fueros | conteos y proporciones por split | conservar; agrupar; umbral de alcance; ponderar luego | borrar minorías o evaluación inestable | **Pendiente de Javier** | cobertura y clases en cada split |
| Metadata geográfica | asociación, disponibilidad y escenario | excluir; usar en ablación; evaluar por grupo | atajo y mala transferencia | **Pendiente de Javier** | comparación con/sin metadata |
| Descriptores humanos | momento de creación, cobertura, asociación | excluir; variante experimental; solo auditoría | target leakage o cobertura desigual | **Pendiente de Javier** | ablación y análisis de disponibilidad |
| Dos relojes temporales | definición y rangos | renombrar; usar fecha judicial; reservar carga para auditoría | interpretar administración como actividad | **Pendiente de Javier** | pruebas semánticas y rangos |
| TF-IDF | definición del split y pipeline | fit en train; limitar vocabulario; n-gramas | fuga y vocabulario inestable | **Pendiente de Javier** | vocabulario aprendido solo en train |
| Nuevas categorías futuras | contrato y ejemplos | ignorar; mapear a desconocida; nueva versión | error silencioso o pérdida | **Pendiente de Javier** | prueba con categoría no vista |
| Transformación no reversible | ausencia de raw o linaje | detener; recuperar fuente; documentar excepción | imposibilidad de auditoría | **Pendiente de Javier** | reconstrucción completa |

### 17.13 Informe breve recomendado

Cada bloque del TP2 puede cerrar con:

1. problema;
2. evidencia;
3. decisión;
4. supuesto;
5. impacto cuantitativo;
6. verificación;
7. limitación;
8. próximo paso.

Eso convierte un notebook de celdas en un argumento.

> **Checkpoint 17**
>
> Elegí una fila de la matriz y explicá qué evidencia te haría cambiar de una acción a otra. Si ninguna evidencia podría cambiar tu decisión, probablemente no es una decisión basada en datos.

---

## 18. Cómo usar los hallazgos del equipo sin apropiárselos

### 18.1 Qué puede usarse como roadmap

El notebook del equipo sugiere investigar:

- mezcla de tipos documentales;
- ausencia estructural;
- normalización de `materia`;
- target construido;
- desbalance;
- cobertura temporal y geográfica;
- dos relojes;
- preparación de texto;
- longitudes;
- términos distintivos;
- descriptores como metadata;
- posible fuga.

Estas son buenas **preguntas de reproducción**.

### 18.2 Qué no debe copiarse como hecho propio

No presentes como resultado de Javier:

- cantidades;
- porcentajes;
- umbrales;
- categorías finales;
- explicaciones causales;
- conclusión de que un outlier es válido;
- afirmación de que fuzzy no produce errores;
- política de clases;
- recomendación de split.

Todo eso necesita ejecución propia, revisión y contexto.

### 18.3 Formato de atribución

Usá frases como:

> “El notebook del grupo informa X. En esta reproducción se verificó/no se verificó mediante Y.”

Si todavía no se reprodujo:

> “X es un hallazgo informado por el equipo y funciona como hipótesis de trabajo; no se usa todavía como evidencia propia.”

### 18.4 Hipótesis causales

Una asociación temporal no demuestra una causa. Digitalización, reformas, cobertura y prácticas de carga pueden generar patrones. Si se menciona una explicación histórica, rotulala como hipótesis y buscá evidencia independiente antes de afirmarla. Esta guía no agrega esa evidencia.

> **Checkpoint 18**
>
> Reescribí “la pandemia causó la caída de documentos” de dos maneras: una como hipótesis pendiente y otra como conclusión que exigiría evidencia adicional. Explicá por qué la primera es honesta.

---

## 19. Errores frecuentes de curación

1. **Trabajar sobre el único original.** Impide volver atrás.
2. **Medir nulos globalmente.** Mezcla no-aplica con perdido.
3. **Eliminar filas raras por estética.** Confunde frecuencia con validez.
4. **Usar una clave sin declarar unidad.** Deduplica entidades distintas.
5. **Forzar todas las categorías.** Esconde ambigüedad.
6. **Confiar en fuzzy como juez semántico.** Similitud textual no es equivalencia jurídica.
7. **Sobrescribir texto.** Destruye evidencia.
8. **Borrar negación.** Puede invertir significado.
9. **Eliminar números indiscriminadamente.** Borra leyes e identificadores significativos.
10. **Usar metadata porque “mejora mucho”.** Puede ser atajo o fuga.
11. **Separar después de vectorizar.** Filtra vocabulario e IDF.
12. **Deduplicar después del split.** Permite documentos relacionados en train y test.
13. **Ajustar umbrales mirando test.** Convierte test en validación.
14. **Reportar solo filas finales.** Oculta quién quedó afuera.
15. **Tratar un contrato como coerción.** Fuerza datos nuevos a categorías viejas.
16. **Documentar solo código.** El criterio queda implícito.
17. **Confundir reproducible con correcto.** Un error puede reproducirse perfectamente.
18. **Copiar decisiones del equipo.** Sustituye evidencia propia por autoridad.

---

## 20. Ejercicios conceptuales progresivos — sin código

Resolvelos primero con palabras, tablas o diagramas. No abras pandas hasta poder justificar la decisión.

### Ejercicio 1 — Del hallazgo a la decisión

AVD muestra cinco variantes de una categoría. Escribí las cinco partes que debería contener una decisión de normalización antes de implementarla.

### Ejercicio 2 — Unidad después de explotar listas

Un documento tiene tres descriptores y se transforma en tres filas. Definí la unidad antes y después. Explicá cómo evitar contar tres documentos.

### Ejercicio 3 — Esquema mixto

En sumarios falta `tribunal`; en fallos falta `texto_resumen`. Diseñá dos interpretaciones posibles y la evidencia que permitiría elegir entre “faltante estructural” y “problema de carga”.

### Ejercicio 4 — Seis dimensiones

Un archivo tiene todos los campos completos, pero repite ids, mezcla formatos de fecha, usa categorías antiguas y no registra origen. Identificá qué dimensiones fallan y cuáles no podés evaluar todavía.

### Ejercicio 5 — Faltante post-merge

Después de unir una tabla de tribunales, 30% de las filas queda sin nombre de tribunal. Proponé un orden de diagnóstico antes de imputar.

### Ejercicio 6 — MCAR/MAR/MNAR con humildad

La ausencia de una metadata se concentra en documentos antiguos. Formulá una hipótesis MAR y una MNAR. Explicá por qué los datos observados quizá no permitan decidir entre ambas.

### Ejercicio 7 — Duplicados de versión

Dos filas comparten id, pero una tiene texto más largo y fecha de actualización posterior. Proponé tres acciones posibles y qué evidencia necesitaría cada una.

### Ejercicio 8 — Duplicate leakage

Un fallo completo y su sumario comparten párrafos. ¿Cómo diseñarías grupos de partición para evitar una evaluación inflada sin declarar automáticamente que son el mismo documento?

### Ejercicio 9 — Mapeo auditable

Diseñá las columnas mínimas de una tabla que normaliza `LAABORAL`, `Laboral` y una etiqueta dudosa hacia un vocabulario canónico. No decidas el caso dudoso por obligación.

### Ejercicio 10 — Fuzzy matching

Un sistema sugiere mapear una categoría rara a `CIVIL` con similitud alta. Enumerá cuatro motivos por los cuales debería seguir siendo candidata y no corrección automática.

### Ejercicio 11 — Target y etiquetas transversales

Un registro contiene una materia sustantiva y una etiqueta procesal. Compará política de clase única, multietiqueta y primera versión con casos claros. Indicá qué información pierde cada una.

### Ejercicio 12 — Negación legal

Una lista estándar de stopwords elimina “no” y “sin”. Construí dos frases jurídicas cuyo sentido cambie y proponé una regla conservadora.

### Ejercicio 13 — Longitud extrema

Un documento de miles de palabras es válido, pero el modelo futuro admite menos tokens. Diseñá una curación que preserve raw, modele y permita recomponer resultados a nivel documento.

### Ejercicio 14 — Features seguras y dudosas

Clasificá `texto`, `materia`, `provincia`, `tribunal`, `descriptores`, `id` y `longitud` como segura, dudosa, prohibida o solo auditoría para predecir fuero. Justificá dependencias del contexto.

### Ejercicio 15 — Preprocessing leakage

Explicá por qué estas acciones son problemáticas antes del split: aprender vocabulario, calcular IDF, elegir top categorías y estimar mediana de imputación. Proponé el orden correcto.

### Ejercicio 16 — Split temporal versus aleatorio

El vocabulario y la composición de fueros cambian con los años. Compará qué pregunta responde un split aleatorio y cuál un split temporal. Elegí uno para predecir documentos futuros y explicá el costo.

### Ejercicio 17 — Contrato liviano

Redactá cinco reglas de contrato para el dataset curado SAIJ: una de esquema, una de identidad, una de target, una de texto y una de partición. Indicá si cada falla detiene, advierte o envía a cuarentena.

### Ejercicio 18 — Matriz de decisión TP2

Elegí un problema real del roadmap y completá: problema → evidencia → acción posible → riesgo → decisión pendiente → verificación. Después escribí qué resultado te haría cambiar la decisión.

---

## 21. Clave de respuestas razonadas

Las respuestas son modelos de razonamiento, no una única solución. Una alternativa es válida si explicita propósito, evidencia, riesgo y verificación.

### Respuesta 1

La decisión debería declarar: problema observado; equivalencias propuestas; supuesto semántico; riesgo de fusionar categorías; y verificación mediante colisiones, cobertura y revisión de muestra. También conviene conservar original y versión del mapeo. “Aplicar mayúsculas” describe una operación, no toda la decisión.

### Respuesta 2

Antes, la unidad es documento. Después, cada fila representa un par documento–descriptor. Para contar documentos se usa el identificador único del documento; para contar asignaciones se cuentan filas. Ambos denominadores son correctos si se rotulan. El error sería interpretar filas expandidas como documentos independientes.

### Respuesta 3

Interpretación estructural: cada tipo usa un subesquema distinto y los campos no aplican al otro. Interpretación de carga: ambos campos deberían existir, pero fallaron en lotes. Para decidir hay que revisar documentación, cobertura por tipo, ejemplos, coausencia, período y fuente. No se imputa hasta entender la semántica.

### Respuesta 4

Falla unicidad por ids repetidos; consistencia por formatos incompatibles; temporalidad por categorías antiguas si ya no son aptas para el uso; trazabilidad por origen ausente. Completitud parece cumplir en presencia, pero no sabemos si los campos esperados son los correctos. Validez tampoco se garantiza: estar presente no implica cumplir dominio.

### Respuesta 5

Primero comprobar cardinalidad y tipos de clave; luego formatos, espacios y ceros a la izquierda; después medir intersección de dominios; revisar filas sin match por grupo; confirmar que la tabla derecha tenga cobertura esperada; y solo entonces decidir si el nulo expresa ausencia real. Imputar de entrada taparía un join fallido.

### Respuesta 6

Hipótesis MAR: la ausencia depende del año observado porque los sistemas antiguos registraban menos metadata; condicionar por período podría explicar el patrón. Hipótesis MNAR: faltan justamente ciertos valores de la metadata por una práctica no observada relacionada con su contenido. Como no vemos los valores ausentes ni todos los procesos históricos, no podemos probar la frontera solo con el dataset.

### Respuesta 7

Acciones: conservar ambas como versiones si la fecha y procedencia lo respaldan; seleccionar una vista vigente y archivar ambas si existe regla oficial de precedencia; enviar a revisión si no se sabe cuál es válida. Hace falta metadata de versión, fuente, timestamp, diferencias textuales y definición de identidad. “Quedarse con la última” sin semántica temporal puede ser erróneo.

### Respuesta 8

Crear un identificador de grupo de caso o relación documental que vincule fallo y sumario sin fusionar necesariamente sus unidades. El split asigna el grupo completo a una partición. La relación puede basarse en claves, referencias y revisión. Así se evita compartir contenido sin afirmar que fallo y sumario son idénticos.

### Respuesta 9

Columnas: original, forma normalizada, categoría canónica propuesta, motivo, confianza, estado de revisión, versión y responsable. `LAABORAL` puede tener una corrección confirmada; `Laboral` una normalización de forma; la dudosa queda `PENDIENTE`. El valor no resuelto es información, no fracaso.

### Respuesta 10

La categoría puede ser corta; una palabra parecida puede tener significado distinto; el vocabulario canónico puede estar incompleto; el umbral se ajustó con ejemplos conocidos; puede haber cambio histórico; y la frecuencia baja dificulta evaluar falsos positivos. El puntaje ofrece evidencia de forma, no equivalencia jurídica.

### Respuesta 11

Clase única simplifica pero descarta transversalidad o exige prioridad. Multietiqueta conserva relaciones pero necesita más datos y evaluación compleja. Una primera versión con casos claros reduce ambigüedad y acota alcance, pero ya no representa documentos complejos. La elección debe reflejar el objetivo y declarar la población resultante.

### Respuesta 12

Ejemplos: “no corresponde hacer lugar al recurso” versus “corresponde hacer lugar”; “sin responsabilidad penal” versus “responsabilidad penal”. Regla: preservar negaciones, revisar listas de stopwords del dominio y, si se usan n-gramas, considerar asociaciones cercanas. Siempre comparar texto antes/después.

### Respuesta 13

Conservar `texto_raw`; crear una versión normalizada; segmentar con solapamiento y guardar `id_documento`, `id_fragmento`, posición y versión; enviar fragmentos al modelo; agregar resultados por documento con regla documentada. Truncar puede ser una variante, pero debe medirse cuánto contenido pierde.

### Respuesta 14

`materia` es prohibida si construye el target. `id` es solo auditoría o prohibido como feature. `texto` y `longitud` son seguras en principio si están disponibles. Provincia, tribunal y descriptores son dudosos por atajo, disponibilidad, sesgo o fuga. Ninguna clasificación es absoluta: depende de cuándo se crean los campos y del escenario real.

### Respuesta 15

Cada acción aprende de la distribución: términos, rareza, categorías frecuentes o mediana. Si incluye validación/test, el preprocesamiento conoce el conjunto reservado. Orden: definir grupos y split; ajustar decisiones aprendibles en train; transformar train, validación y test con parámetros congelados; usar validación para elegir; reservar test.

### Respuesta 16

El aleatorio estima desempeño dentro de una mezcla parecida al corpus observado. El temporal estima transferencia del pasado al futuro y expone deriva. Para documentos futuros, temporal suele ser más fiel. El costo es mayor dificultad, clases nuevas o cambio de distribución; justamente esa dificultad representa el uso real.

### Respuesta 17

Ejemplo: esquema exige campos básicos y detiene si faltan; identidad inválida envía a cuarentena; target no puede entrar como feature y detiene; texto limpio vacío advierte o cuarentena según tasa; un grupo que cruza splits detiene. La severidad depende de si el problema compromete integridad global o un caso aislado.

### Respuesta 18

Una fila válida podría ser: “variantes de materia → tabla de frecuencias y revisión → mapeo manual o fuzzy asistido → riesgo de colisión → decisión pendiente → medir cobertura y revisar muestra”. La decisión cambiaría si la revisión revela falsos positivos o una categoría jurídica distinta. Explicitar esa condición muestra que el criterio puede aprender de evidencia.

---

## 22. Autoevaluación final

Marcá cada afirmación solo si podés explicarla con un ejemplo propio.

### Fundamentos

- [ ] Distingo diagnóstico, decisión, transformación y verificación.
- [ ] Puedo explicar por qué no existe un dataset limpio independiente del propósito.
- [ ] Sé qué significa preservar raw y qué vuelve auditable una transformación.
- [ ] Puedo definir unidad de análisis antes y después de una expansión.

### Calidad y faltantes

- [ ] Puedo evaluar las seis dimensiones por separado.
- [ ] Distingo no-aplica, perdido, no observado y faltante post-transformación.
- [ ] Sé por qué una imputación no recupera la verdad.
- [ ] Puedo usar MCAR/MAR/MNAR como supuestos sin fingir diagnóstico seguro.
- [ ] Sé comparar una transformación antes/después y por grupos.

### Identidad y categorías

- [ ] Distingo duplicados exactos, por clave, cercanos y semánticos.
- [ ] Puedo explicar duplicate leakage.
- [ ] Sé diseñar una tabla de mapeo versionada.
- [ ] Reconozco los límites del fuzzy matching.
- [ ] Puedo dejar casos pendientes sin forzarlos.

### Target y texto

- [ ] Puedo explicar por qué `fuero` construido contiene decisiones humanas.
- [ ] Distingo etiquetas sustantivas, transversales, compuestas y ambiguas.
- [ ] Puedo comparar clase única y multietiqueta.
- [ ] Preservo texto raw y justifico Unicode, whitespace, case, tildes y puntuación.
- [ ] Sé por qué negación e identificadores legales requieren cuidado.
- [ ] Distingo longitud rara de texto inválido.

### Features, sesgo y fuga

- [ ] Clasifico features por disponibilidad y linaje, no por conveniencia.
- [ ] Reconozco sesgo temporal, geográfico, de tribunal y tipo documental.
- [ ] Distingo target, duplicate, temporal y preprocessing leakage.
- [ ] Puedo explicar fit-on-train.
- [ ] Distingo funciones de train, validación y test.
- [ ] Puedo justificar split aleatorio, grupal o temporal.

### Representaciones y reproducibilidad

- [ ] Explico qué conservan y pierden BoW, TF-IDF y embeddings.
- [ ] Sé que TF-IDF aprende IDF y debe ajustarse en train.
- [ ] Puedo diseñar diccionario, diario, manifiesto y métricas antes/después.
- [ ] Entiendo ETL, linaje y contrato liviano sin herramientas avanzadas.
- [ ] Puedo completar la matriz de decisiones del TP2 con evidencia y riesgo.

### Criterio de dominio

Si marcaste todo, hacé una prueba final oral:

> “Recibo un corpus legal con tipos mezclados, target construido, textos variables y dos fechas. ¿Qué hago desde raw hasta particiones y cómo demuestro que no borré, inventé ni filtré información?”

Si la explicación respeta unidad, poblaciones, target, texto, duplicados, tiempo, split, fit-on-train y auditoría, estás listo para implementar. Si salta directamente a `dropna`, vectorizar o entrenar, volvé a los bloques correspondientes.

---

## 23. Glosario de Materia 2

| Término | Definición operativa |
|---|---|
| **Auditabilidad** | Capacidad de inspeccionar una decisión, su evidencia, regla, impacto y responsable. |
| **BoW** | Representación que cuenta términos sin conservar el orden global. |
| **Cardinalidad** | Cantidad de valores distintos o relación esperada entre claves. |
| **Caso ambiguo** | Observación para la que la evidencia no alcanza para una asignación confiable. |
| **Completitud** | Presencia de datos que deberían existir para una unidad y uso. |
| **Consistencia** | Compatibilidad de representaciones de una entidad o concepto. |
| **Contrato de datos** | Conjunto de expectativas de esquema, dominio y respuesta ante fallos. |
| **Cuarentena** | Zona donde se conservan casos dudosos sin incorporarlos silenciosamente al producto. |
| **Curación** | Selección y transformación documentada de datos para un propósito. |
| **Data lineage / linaje** | Rastro desde un dato derivado hasta sus fuentes y transformaciones. |
| **Dataset curado** | Versión regenerable de datos preparada para una tarea explícita. |
| **Dato crudo / raw** | Copia inmutable de la fuente recibida. |
| **Dato faltante accidental** | Valor que debería existir pero no fue observado o se perdió. |
| **Dato faltante estructural** | Ausencia porque el atributo no aplica a esa unidad. |
| **Data leakage** | Uso indebido de información no disponible o reservada. |
| **Deduplicación** | Resolución de repeticiones según una definición de identidad. |
| **Diario de transformaciones** | Registro de problemas, acciones, impactos y verificaciones. |
| **Duplicate leakage** | Presencia de entidades iguales o relacionadas en particiones distintas. |
| **Embedding** | Vector denso que intenta representar similitud contextual o semántica. |
| **Esquema** | Estructura y reglas esperadas de los datos. |
| **ETL** | Extraer, transformar y cargar datos. |
| **Feature dudosa** | Variable cuyo valor predictivo puede depender de atajos, sesgo o disponibilidad. |
| **Feature prohibida** | Variable que revela el target, identifica casos o viola el escenario de uso. |
| **Fit** | Aprendizaje de parámetros desde datos. |
| **Fit-on-train** | Regla de ajustar preprocesamiento y modelo solo con entrenamiento. |
| **Fuzzy matching** | Comparación aproximada de cadenas; sugiere similitud de forma. |
| **Imputación** | Sustitución de un faltante por un valor estimado o categoría. |
| **Linaje de feature** | Origen, campos y reglas que producen una entrada del modelo. |
| **Mapeo auditable** | Tabla versionada que conserva valor original, destino y motivo. |
| **MAR** | Supuesto donde la ausencia depende de variables observadas. |
| **MCAR** | Supuesto donde la ausencia no depende de variables observadas ni faltantes. |
| **MNAR** | Supuesto donde la ausencia depende de información no observada o del propio valor. |
| **Preprocessing leakage** | Ajuste de transformaciones usando validación o test. |
| **Representatividad** | Adecuación de datos y proceso de selección respecto de la población objetivo. |
| **Reversible** | Proceso que permite volver a la fuente o reconstruir decisiones. |
| **Semilla aleatoria** | Valor que controla operaciones pseudoaleatorias reproducibles. |
| **Split grupal** | División que mantiene entidades relacionadas en la misma partición. |
| **Split temporal** | División que respeta el orden del tiempo. |
| **Target construido** | Etiqueta derivada mediante reglas, no observada directamente. |
| **Temporalidad** | Adecuación del reloj, período y vigencia al uso. |
| **TF-IDF** | Representación que pondera frecuencia local y rareza en el corpus. |
| **Traceabilidad** | Capacidad de seguir origen, versión y transformaciones. |
| **Unicidad** | Cumplimiento de la cantidad esperada de apariciones por unidad. |
| **Validez** | Cumplimiento de reglas de formato y dominio. |
| **Versión** | Identificador de un estado reproducible de datos o reglas. |

---

## 24. Puente desde la curación hacia Introducción al Aprendizaje Automático

La Materia 2 termina con un dataset y una evaluación diseñados, no con un modelo elegido. La próxima materia agregará preguntas nuevas:

- ¿qué significa aprender una función desde ejemplos?
- ¿qué diferencia hay entre entrenamiento y generalización?
- ¿cómo se construye una línea base?
- ¿qué métricas sirven con clases desbalanceadas?
- ¿cómo se comparan modelos sin tocar test?
- ¿qué significa error por clase?
- ¿cómo se interpretan falsos positivos y falsos negativos en un contexto jurídico?

El puente es:

```text
AVD descubre
  → Curación decide, transforma y audita
  → IAA aprende y evalúa sobre esa base
```

Para SAIJ, el futuro problema de clasificación podría usar texto para proponer un `fuero`. Pero antes de entrenar debe existir:

- una definición defendible del target;
- una población clara;
- texto preservado y curado;
- features autorizadas;
- grupos de duplicados;
- particiones honestas;
- preprocesamiento fit-on-train;
- métricas de calidad y sesgo;
- límites de uso.

Si falta alguno, el algoritmo no corrige la deuda. La vuelve menos visible.

Ese cierre no es una invitación a entrenar apurado. Es el contrato de entrada de la Materia 3: tomar las salidas documentadas de TP2, formular una tarea predictiva, elegir una evaluación que represente el uso futuro y recién después comparar hipótesis. La curación sigue siendo parte del sistema de aprendizaje; no desaparece cuando aparece un modelo.

La Materia 3 desarrolla ese puente sin exigir código. Su meta es que cada futura línea de entrenamiento pueda justificarse antes de ejecutarse.


---

