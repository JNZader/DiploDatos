# Materia 3 — Introducción al Aprendizaje Automático

> **Idea rectora:** aprender automáticamente no es adivinar ni descubrir una verdad jurídica. Es ajustar una regla con ejemplos pasados y comprobar, mediante una evaluación honesta, si esa regla puede ayudar en casos nuevos dentro de un uso definido.

Esta materia empieza donde terminó la curación. Ya no preguntamos solamente si las filas están bien formadas, si el texto conserva sentido o si el target tiene linaje. Preguntamos si existe una regularidad aprovechable entre unas entradas y una salida, cómo estimarla sin contaminar la evaluación y qué clase de error produciría en operación.

El caso SAIJ funciona como hilo conductor: usar texto u otras variables autorizadas para proponer un fuero. Ese caso es un **candidato** a clasificación supervisada multiclase, no una tarea ya resuelta. La etiqueta puede ser construida, ambigua o compuesta; la población puede cambiar con el tiempo; ciertos campos pueden revelar directamente el resultado. Por eso el primer trabajo de aprendizaje automático no es elegir un algoritmo. Es formular el problema.

El capítulo mantiene una secuencia deliberada:

```text
intuición
  → vocabulario preciso
  → ejemplo inventado resuelto a mano
  → fórmula explicada símbolo por símbolo
  → interpretación
  → error frecuente
  → checkpoint
  → transferencia a SAIJ
  → ejercicio conceptual
```

No hay código en la ruta principal. Primero vas a aprender qué decisión representa cada operación. La implementación llegará después, en los trabajos y en la Materia 4.

---

## 0. Contrato de lectura y evidencia

### 0.1 Qué deberías poder hacer al terminar

Al completar la materia deberías poder:

1. explicar qué significa que un sistema “aprenda de datos” y qué afirmaciones no se desprenden de ello;
2. formular una tarea indicando unidad, entradas, target, salida, uso y criterio de éxito;
3. distinguir aprendizaje supervisado, no supervisado y por refuerzo;
4. separar clasificación de regresión y reconocer problemas binarios, multiclase y multietiqueta;
5. explicar dataset, hipótesis, modelo, parámetros, hiperparámetros, entrenamiento, inferencia y generalización;
6. asignar roles correctos a train, validación y test;
7. elegir entre particiones aleatorias, estratificadas, grupales y temporales según el futuro que se quiere estimar;
8. construir e interpretar una baseline como control científico;
9. diagnosticar sobreajuste, subajuste y desbalance sin reducirlos a una sola cifra;
10. calcular a mano accuracy, precision, recall y F1;
11. interpretar promedios macro, micro y weighted en multiclase;
12. explicar validación cruzada y reconocer lo que no puede corregir;
13. detectar fuga de información en transformaciones y representaciones de texto;
14. explicar Bag of Words, conteos binarios, n-gramas, TF-IDF y matrices dispersas;
15. reconstruir la intuición de Naive Bayes, su supuesto “ingenuo” y el suavizado;
16. diseñar un experimento reproducible con análisis de errores;
17. conectar las salidas de TP2 con un entrenamiento futuro sin fingir que TP2 exige el modelo final;
18. justificar revisión humana o abstención cuando una predicción automática no es suficiente.

### 0.2 Cuatro rótulos que no se mezclan

En esta materia siguen vigentes los rótulos del libro:

- **Teoría:** concepto general enseñado por la materia.
- **Ejemplo ilustrativo inventado:** números o textos creados solo para aprender. Nunca describen SAIJ.
- **Hallazgo del notebook del equipo — pendiente de reproducción:** observación que orienta preguntas, pero Javier todavía no la obtuvo con una ejecución propia y documentada.
- **Decisión de Javier — pendiente:** elección que debe justificarse con el propósito, la evidencia reproducida y el costo del error.

Esta separación es especialmente importante en aprendizaje automático. Un ejemplo inventado puede demostrar una fórmula, pero no demostrar desempeño. Un resultado del equipo puede sugerir una partición temporal, pero no convertirse en resultado propio. Una etiqueta construida puede permitir entrenar, pero no volverse verdad jurídica por haber sido usada como `y`.

> **Checkpoint 0**
>
> Completá sin mirar: “Un modelo puede aprender a reproducir ________ sin haber aprendido ________”. Una respuesta posible es: “una regla de etiquetado histórica” sin haber aprendido “la naturaleza jurídica verdadera del caso”.

---

## 1. Qué significa “aprender de datos”

### 1.1 Intuición: de reglas escritas a reglas ajustadas

En programación tradicional, una persona escribe reglas explícitas y la computadora las aplica. Si se quisiera clasificar documentos con reglas manuales, podríamos decir: “si aparece cierta expresión, asignar cierta categoría”. El comportamiento depende de esas reglas escritas de antemano.

En aprendizaje automático, damos **ejemplos** de entradas y salidas. Un procedimiento de entrenamiento busca, dentro de una familia posible de reglas, una que cometa poco error en esos ejemplos y conserve buen desempeño en datos no vistos.

La diferencia no es magia. Cambia dónde se concentra el trabajo:

```text
programación por reglas:
criterio humano explícito + entrada → salida

aprendizaje supervisado:
ejemplos de entrada y salida + algoritmo de entrenamiento → regla ajustada
regla ajustada + entrada nueva → salida propuesta
```

El modelo no deja de estar diseñado. Alguien elige la población, las variables, la representación, la familia de hipótesis, la pérdida, la métrica y el modo de evaluación. Los datos tampoco “hablan solos”: contienen decisiones de registro, selección y etiquetado.

### 1.2 Una definición operativa

Diremos que un sistema aprende de datos cuando su desempeño en una tarea mejora al ajustar su comportamiento con experiencia observada. Conviene identificar tres componentes:

- **Tarea:** qué debe producir. Por ejemplo, proponer una categoría.
- **Experiencia:** con qué ejemplos se ajusta. Por ejemplo, documentos etiquetados.
- **Desempeño:** con qué criterio se juzga. Por ejemplo, F1 macro sobre documentos futuros.

Si alguno falta, la frase “hacer machine learning” es demasiado vaga. Un modelo que reduce su pérdida de entrenamiento aprendió a optimizar sobre train; todavía no sabemos si generaliza.

### 1.3 Qué no significa aprender

Aprender de datos **no garantiza**:

- comprender el derecho o razonar como una persona experta;
- descubrir relaciones causales;
- producir una salida verdadera cuando la etiqueta de entrenamiento es discutible;
- funcionar en épocas, organismos o formatos no representados;
- ser neutral frente a sesgos del corpus;
- explicar por sí solo por qué una predicción es correcta;
- reemplazar una decisión humana de alto impacto;
- mejorar solamente por usar un algoritmo más complejo.

Un clasificador puede aprovechar atajos: una marca de formato, el nombre de un organismo o una fórmula repetida que correlaciona con el target. Puede obtener buena métrica y aprender una señal que no queremos usar. Por eso la evaluación técnica y la evaluación del propósito son inseparables.

### 1.4 Ejemplo inventado: aprender o memorizar

Supongamos seis documentos de práctica. Tres de clase A incluyen accidentalmente el prefijo `AAA-` y tres de clase B incluyen `BBB-`. Un modelo puede lograr seis aciertos mirando solo el prefijo. Si en producción los prefijos desaparecen, falla.

¿Qué aprendió? Una correlación perfecta del dataset de entrenamiento. ¿Qué no aprendió? El contenido que define las clases. El desempeño en train no distingue ambas historias. Una partición honesta o una prueba específica sin prefijos sí puede hacerlo.

> **Error frecuente:** creer que “encontró un patrón” equivale a “encontró el patrón correcto”. La primera afirmación es estadística; la segunda requiere conocimiento del uso y pruebas adicionales.

### 1.5 Transferencia a SAIJ

Para SAIJ, “aprender fuero” podría significar varias cosas distintas:

- reproducir el valor normalizado derivado de `materia`;
- proponer una única categoría operativa para ruteo;
- detectar todas las ramas aplicables a un documento;
- asistir una revisión humana con un ranking de opciones.

Esas tareas no son equivalentes. Cambian el target, la salida, las métricas y el costo de error. Antes de entrenar, Javier debe decidir cuál representa el propósito real.

---

## 2. Formular el problema antes de elegir un modelo

### 2.1 Las siete preguntas mínimas

Una formulación útil responde:

1. **Unidad:** ¿qué representa una observación?
2. **Entrada (X):** ¿qué información estará disponible al predecir?
3. **Features:** ¿cómo se expresa esa información para el modelo?
4. **Target (y):** ¿qué salida se usa como respuesta durante entrenamiento?
5. **Salida operacional:** ¿qué recibe la persona o sistema usuario?
6. **Escenario de uso:** ¿quién usa la salida, cuándo y para qué?
7. **Criterio de éxito:** ¿qué métricas y condiciones indican utilidad?

No alcanza con decir “predecir fuero con texto”. Puede esconder decisiones incompatibles.

### 2.2 Unidad

La **unidad de análisis** define qué es un caso. Podría ser un documento, un sumario, una decisión, una versión de una decisión o un par documento–fuero. Si dos filas son versiones del mismo texto y se dividen entre train y test, la evaluación puede premiar memoria. Si una fila contiene varios fueros, forzar una sola clase cambia la pregunta.

**Pregunta manual:** tomá tres filas hipotéticas que comparten identificador y texto casi idéntico. ¿Son tres experiencias independientes? No necesariamente. Tal vez sean un grupo que debe permanecer unido.

### 2.3 Entradas, matriz (X) y features

Usamos (X) para representar todas las entradas del dataset. Cada fila (x_i) corresponde al caso (i). Sus columnas son **features**, es decir, variables que el modelo puede usar.

Una notación común es:

[
X =
\begin{bmatrix}
x_{11} & x_{12} & \cdots & x_{1p} \\
x_{21} & x_{22} & \cdots & x_{2p} \\
\vdots & \vdots & \ddots & \vdots \\
x_{n1} & x_{n2} & \cdots & x_{np}
\end{bmatrix}
]

Símbolo por símbolo:

- (X) es el conjunto de entradas representado como matriz;
- (n) es la cantidad de observaciones;
- (p) es la cantidad de features;
- (x_{ij}) es el valor de la feature (j) para la observación (i);
- (x_i) es la fila completa del caso (i).

En texto, (p) puede ser el tamaño del vocabulario y (x_{ij}) indicar cuántas veces aparece el término (j) en el documento (i). Aunque no veamos una tabla densa, la idea matricial sigue vigente.

### 2.4 Target (y)

El vector de targets puede escribirse:

[
y = [y_1, y_2, \ldots, y_n]
]

- (y) reúne las respuestas usadas para aprender;
- (y_i) es la respuesta asociada al caso (i);
- en regresión, (y_i) suele ser numérico continuo;
- en clasificación, (y_i) representa una categoría;
- en multietiqueta, cada caso puede tener un vector de varios indicadores.

Llamarlo target no lo convierte en verdad absoluta. Puede provenir de anotación humana, una regla de negocio, una categoría administrativa o un mapeo construido. Su calidad limita lo que el modelo puede aprender.

### 2.5 Salida y escenario de uso

Una misma predicción puede entregarse como:

- una clase única;
- varias clases posibles;
- un ranking;
- un score por clase;
- una recomendación con opción de abstención;
- una alerta para revisión.

La salida debe corresponder al uso. Si una persona revisará sugerencias, un ranking puede ser más útil que imponer una sola clase. Si el sistema deriva automáticamente expedientes, un error puede tener mayor costo y exigir umbrales, auditoría y reversibilidad.

### 2.6 Criterio de éxito

Un criterio defendible combina:

- **métrica primaria:** la que gobierna la comparación;
- **métricas de diagnóstico:** por clase, período y subgrupo;
- **baseline:** control mínimo que se debe superar;
- **restricciones operativas:** latencia, cobertura, revisión disponible;
- **condiciones de seguridad:** ausencia de fuga, estabilidad y capacidad de abstenerse;
- **criterio humano:** utilidad real para la tarea.

“Maximizar accuracy” no es una formulación completa. No dice cuánto importa cada clase ni qué futuro representa el test.

### 2.7 Ejemplo inventado resuelto

Supongamos ocho notas breves sobre trámites, cada una con una categoría A, B o C. Queremos sugerir una categoría a una persona revisora.

- Unidad: una nota, no cada oración.
- (X): texto disponible antes de clasificar.
- Features: conteos de términos construidos solo con train.
- (y): categoría administrativa revisada A/B/C.
- Salida: ranking de tres categorías con posibilidad de “revisar”.
- Uso: asistencia, no asignación automática.
- Éxito: mejorar una baseline mayoritaria en F1 macro, mantener resultados razonables por clase y enviar a revisión casos de baja confianza.

Fijate que todavía no elegimos modelo. Ya resolvimos decisiones más importantes.

### 2.8 SAIJ como candidato multiclase, con límites

Si cada documento recibe **exactamente un fuero**, la tarea candidata es clasificación multiclase. Pero esa frase depende de evidencia y reglas:

- puede haber categorías compuestas o transversales;
- una normalización puede transformar textos originales en etiquetas construidas;
- una misma decisión puede admitir más de una rama;
- documentos duplicados o versionados pueden romper independencia;
- campos institucionales pueden revelar el target por un atajo;
- la definición de fuero útil para ruteo puede diferir de la categoría histórica.

Por eso, antes de fijar (y), Javier debe responder:

1. ¿Se excluyen categorías combinadas, se mapean, se conservan o se formula multietiqueta?
2. ¿Qué ocurre con etiquetas raras o dudosas?
3. ¿Qué tabla de mapeo y versión produjo el target?
4. ¿Quién puede revisar casos ambiguos?
5. ¿Qué población futura se espera clasificar?

> **Decisión de Javier — pendiente:** no se afirma aquí cuál es la taxonomía final ni cuántas clases tiene. Esa decisión exige reproducir la curación y documentar el propósito.

---

## 3. Familias de aprendizaje y tipos de salida

### 3.1 Aprendizaje supervisado

En aprendizaje supervisado observamos pares ((x_i, y_i)). El modelo intenta aprender una función:

[
f: \mathcal{X} \rightarrow \mathcal{Y}
]

- (f) es la regla aprendida;
- (mathcal{X}) es el espacio de entradas posibles;
- (mathcal{Y}) es el espacio de salidas;
- (x_i \in \mathcal{X}) es un ejemplo;
- (y_i \in \mathcal{Y}) es su respuesta.

La materia se concentra en esta familia porque el candidato SAIJ usaría textos con etiquetas de fuero.

### 3.2 Aprendizaje no supervisado

En aprendizaje no supervisado observamos (X) sin un target externo (y). Buscamos estructura: grupos, dimensiones latentes, patrones de similitud o casos atípicos. Un agrupamiento de textos no “descubre fueros verdaderos” automáticamente. Produce grupos según una representación y un criterio de similitud; la interpretación llega después.

### 3.3 Aprendizaje por refuerzo

En aprendizaje por refuerzo un agente actúa en un entorno, recibe recompensas y aprende una política para elegir acciones a lo largo del tiempo. El resultado de una acción puede afectar situaciones futuras. No es el marco natural para la primera clasificación de fueros, porque allí tenemos ejemplos etiquetados y no una secuencia de decisiones con recompensas.

### 3.4 Clasificación y regresión

- **Regresión:** la salida es numérica continua. Ejemplo inventado: estimar minutos de revisión.
- **Clasificación:** la salida es una categoría. Ejemplo inventado: A, B o C.

No se decide por el tipo visual de la columna solamente. Un número que codifica categorías no vuelve regresión al problema.

### 3.5 Binaria, multiclase y multietiqueta

- **Binaria:** dos clases mutuamente excluyentes, como “requiere revisión / no requiere”.
- **Multiclase:** una clase entre (K>2), como A/B/C.
- **Multietiqueta:** un subconjunto de etiquetas, como A y C simultáneamente.

Un documento SAIJ con varias ramas posibles no debería forzarse a multiclase solo porque un algoritmo espera un vector unidimensional. Primero se decide qué salida representa el uso.

> **Checkpoint 1**
>
> Si un documento puede pertenecer simultáneamente a CIVIL y COMERCIAL, ¿es multiclase? No bajo esa definición: es multietiqueta. Sería multiclase solo si una regla de negocio obliga a elegir una categoría única y esa transformación se documenta.

---

## 4. Dataset, hipótesis, parámetros y generalización

### 4.1 Dataset de ejemplos

Un dataset supervisado se representa como:

[
\mathcal{D} = \{(x_i, y_i)\}_{i=1}^{n}
]

- (mathcal{D}) es el conjunto de datos;
- las llaves indican una colección de pares;
- (i) identifica una observación;
- (n) es la cantidad de observaciones;
- (x_i) es la entrada del caso (i);
- (y_i) es su target.

La fórmula no dice que los casos sean independientes, representativos ni correctos. Esas son condiciones que debemos investigar.

### 4.2 Modelo e hipótesis

Una **hipótesis** es una regla candidata. El **espacio de hipótesis** (mathcal{H}) es el conjunto de reglas que el procedimiento puede considerar. El entrenamiento selecciona una:

[
f^* = \arg\min_{f \in \mathcal{H}} L_{train}(f)
]

Símbolo por símbolo:

- (f) es una hipótesis candidata;
- (mathcal{H}) es la familia permitida;
- (L_{train}(f)) es la pérdida de esa hipótesis en train;
- (arg\min) significa “la opción que produce el valor mínimo”;
- (f^*) es la hipótesis seleccionada.

La fórmula resume la optimización, no garantiza generalización. Dos modelos pueden tener pérdida parecida en train y comportamiento distinto en test.

### 4.3 Parámetros e hiperparámetros

- **Parámetros:** valores ajustados por el entrenamiento. En un modelo lineal, los pesos de las features.
- **Hiperparámetros:** decisiones configuradas fuera de ese ajuste. Por ejemplo, complejidad permitida, fuerza de regularización, tamaño de vocabulario o rango de n-gramas.

Los parámetros se aprenden con train. Los hiperparámetros se eligen con validación o validación cruzada dentro de train. Test no debe convertirse en asesor de decisiones.

### 4.4 Entrenamiento e inferencia

- **Entrenamiento:** proceso que usa ejemplos etiquetados para ajustar parámetros.
- **Inferencia:** uso del modelo ya entrenado para producir una salida sobre un caso.

No confundir inferencia de un modelo predictivo con inferencia causal o estadística en un sentido más amplio. Aquí significa aplicar la función aprendida.

### 4.5 Generalización

Generalizar es mantener desempeño útil sobre datos nuevos provenientes del futuro relevante para el uso. No significa “funcionar en cualquier lugar”. Siempre está condicionado por población, época, proceso de captura y definición de target.

Un modelo puede generalizar bien a una partición aleatoria del mismo archivo y mal a documentos de años posteriores. Ambas mediciones pueden ser correctas porque responden preguntas diferentes.

### 4.6 Material complementario integrado 2 — Sesgo inductivo y ausencia de un modelo universalmente mejor

Todo modelo favorece ciertos patrones. Esa preferencia es su **sesgo inductivo**. Un modelo lineal favorece fronteras simples; un modelo con más capacidad puede representar interacciones complejas; Naive Bayes favorece una estructura probabilística con independencia condicional aproximada.

No hay un modelo universalmente mejor para todos los datasets y propósitos. Elegir depende de:

- cantidad y calidad de ejemplos;
- representación;
- relación señal–ruido;
- desbalance;
- costo computacional;
- necesidad de explicación;
- estabilidad temporal;
- costo de errores.

La consecuencia práctica es importante: comparar modelos sin fijar split, métrica y representación no produce una competencia justa. También evita el error de elegir un algoritmo por prestigio.

---

## 5. Train, validación y test: tres roles, una sola honestidad

### 5.1 Train

Train se usa para ajustar todo lo aprendido de los datos:

- parámetros del modelo;
- vocabulario;
- frecuencias de términos;
- pesos IDF;
- escalas o normalizaciones aprendidas;
- reglas estadísticas de imputación;
- selección de features basada en datos.

Train puede mirarse muchas veces durante desarrollo, pero su métrica no es una estimación neutral del futuro.

### 5.2 Validación

Validación se usa para elegir:

- familia o configuración de modelo;
- hiperparámetros;
- representación;
- threshold, si corresponde;
- momento de detener entrenamiento;
- decisiones comparativas del experimento.

Cada vez que decidimos mirando validación, nos adaptamos a ella. Por eso también puede sobreajustarse si probamos demasiadas variantes.

### 5.3 Test

Test se reserva para una estimación final del procedimiento elegido. No se usa para escoger vocabulario, modelo, métrica o threshold. Si una mirada a test cambia la decisión, test pasó a ser validación y hace falta otro conjunto final.

### 5.4 Ejemplo de examen

- Train son los ejercicios con solución usados para aprender.
- Validación son simulacros usados para elegir estrategia.
- Test es el examen final que estima cómo funcionó la estrategia elegida.

Resolver el examen, revisar respuestas y volver a estudiar con ellas ya no permite usar esa misma nota como evaluación independiente.

### 5.5 Una partición estima un futuro

La pregunta no es “¿cuál split es correcto?”. Es “¿qué escenario futuro intenta imitar?”.

#### Partición aleatoria

Mezcla casos y separa al azar. Estima desempeño en nuevos casos intercambiables con la misma población y período, siempre que no haya grupos vinculados. Es útil cuando la independencia aproximada es plausible.

#### Partición estratificada

Además de separar, conserva aproximadamente proporciones de clases. Estima el mismo tipo de futuro que el split aleatorio, pero reduce el riesgo de particiones con composición de clases accidentalmente distinta. No corrige duplicados, drift ni sesgo.

#### Partición consciente de grupos

Mantiene juntas observaciones relacionadas: versiones, documentos de una misma causa, una misma fuente o un mismo expediente. Estima desempeño sobre **grupos no vistos**, no sobre nuevas filas de grupos ya conocidos.

#### Partición temporal

Entrena con pasado y evalúa en futuro. Estima capacidad de transferir a períodos posteriores. Respeta el orden y permite ver drift, cambios de taxonomía o de estilo.

### 5.6 Material complementario integrado 4 — Group-aware y temporal responden preguntas de despliegue distintas

No son dos “variantes más estrictas” del split aleatorio. Responden preguntas distintas:

| Split | Pregunta de despliegue aproximada |
|---|---|
| Aleatorio | ¿Cómo funciona con otra muestra de la misma mezcla? |
| Estratificado | ¿Cómo funciona con otra muestra de la misma mezcla preservando clases? |
| Grupal | ¿Cómo funciona con entidades o familias documentales nunca vistas? |
| Temporal | ¿Cómo funciona con documentos que llegan después? |

Si el uso real recibe expedientes nuevos en años futuros, una evaluación aleatoria puede ser demasiado cómoda. Si recibe nuevas versiones de expedientes ya conocidos, la pregunta cambia. Puede ser útil reportar más de un escenario, siempre que cada resultado se nombre correctamente.

### 5.7 Transferencia SAIJ

**Hallazgo del notebook del equipo — pendiente de reproducción:** el trabajo del grupo señala posibles efectos temporales, cargas administrativas y categorías relacionadas, y por eso sugiere mirar particiones temporales y confusiones entre fueros. Esa observación sirve como roadmap, no como hecho propio.

**Decisión de Javier — pendiente:** identificar el reloj operativo correcto, los grupos de documentos relacionados y el escenario real de llegada. Solo entonces elegir split principal y pruebas secundarias.

> **Error frecuente:** estratificar y creer que ya se evitó toda fuga. La estratificación cuida proporciones de (y); no impide que duplicados crucen particiones.

---

## 6. Baselines: el control científico del experimento

### 6.1 Intuición

Una baseline es una regla simple que fija el nivel mínimo de comparación. En clasificación puede ser:

- predecir siempre la clase mayoritaria;
- predecir según frecuencias observadas;
- usar una regla simple acordada;
- usar una representación y modelo deliberadamente sencillos.

### 6.2 Material complementario integrado 1 — La baseline como control científico, no como juguete descartable

La baseline cumple el papel de **control científico**. Permite preguntar si la complejidad agregó evidencia real o solo una impresión de sofisticación.

Una buena baseline:

1. se define antes de mirar resultados finales;
2. usa el mismo split y las mismas métricas que los modelos;
3. queda registrada en el ledger;
4. se conserva en informes posteriores;
5. obliga a explicar qué mejora y a qué costo.

Si un modelo complejo no supera una baseline en la métrica primaria o empeora clases críticas, la conclusión no es “necesitamos todavía más complejidad”. Primero se revisan target, representación, split y señal disponible.

### 6.3 Baseline y desbalance

La regla mayoritaria puede tener accuracy alta cuando una clase domina. Ese es precisamente su valor como control: muestra que accuracy sola no alcanza. Si un modelo iguala la accuracy mayoritaria pero mejora recall de clases minoritarias, las métricas por clase revelan un progreso que el total oculta.

### 6.4 Ejemplo inventado

En 100 ejemplos inventados, 80 pertenecen a A, 15 a B y 5 a C. La baseline mayoritaria predice siempre A:

- acierta 80;
- accuracy = (80/100 = 0{,}80);
- recall de A = 1;
- recall de B = 0;
- recall de C = 0.

Decir “80%” sin el perfil por clase sería engañoso. La baseline funciona como detector de esa ilusión.

---

## 7. Capacidad, subajuste, sobreajuste y sesgo–varianza

### 7.1 Capacidad

La **capacidad** describe cuán complejas son las relaciones que un modelo puede representar. No depende solo del nombre del algoritmo: también de hiperparámetros, regularización y representación.

- Capacidad muy baja: no captura señal suficiente.
- Capacidad adecuada: captura patrones transferibles.
- Capacidad muy alta para los datos disponibles: puede capturar ruido y particularidades.

### 7.2 Subajuste

Hay subajuste cuando el modelo es demasiado limitado o las features son insuficientes. Suele mostrar desempeño pobre tanto en train como en validación.

Ejemplo inventado: clasificar textos usando únicamente su cantidad total de caracteres. Si las clases dependen de vocabulario jurídico, esa feature puede no contener señal suficiente.

### 7.3 Sobreajuste

Hay sobreajuste cuando el modelo ajusta particularidades de train que no se transfieren. Suele verse como train muy bueno y validación claramente peor. También puede existir sin una brecha espectacular si la validación tiene fuga o es demasiado parecida a train.

Ejemplo inventado: memorizar identificadores únicos o frases de plantillas repetidas.

### 7.4 Intuición de sesgo y varianza

- **Sesgo alto:** el modelo impone una simplificación fuerte y falla sistemáticamente. Se vincula con subajuste.
- **Varianza alta:** pequeños cambios en train producen modelos muy distintos. Se vincula con sensibilidad y sobreajuste.

La intuición del equilibrio no dice que debamos calcular una descomposición exacta. Sirve para diagnosticar:

| Señal | Hipótesis de diagnóstico |
|---|---|
| Train malo y validación mala | capacidad o representación insuficiente, target ruidoso |
| Train excelente y validación mala | sobreajuste, fuga en selección, grupos mal separados |
| Ambos razonables y cercanos | posible generalización dentro de ese split |
| Resultados muy variables entre folds | sensibilidad a la muestra, clases escasas o grupos heterogéneos |

### 7.5 Error frecuente

“Más complejo” no significa “más inteligente”. Un modelo de alta capacidad puede ser peor si hay pocos datos, etiquetas ruidosas o drift. Tampoco una brecha pequeña garantiza utilidad: train y validación pueden ser igualmente pobres.

> **Checkpoint 2**
>
> Un modelo tiene 99% en train y 61% en validación; otro 73% y 70%. Sin conocer la métrica ni el uso, no se puede declarar ganador. El primero muestra una brecha preocupante; el segundo parece más estable, pero todavía debe compararse con baseline y por clase.

---

## 8. Pérdida y métrica de evaluación

### 8.1 Dos funciones distintas

La **pérdida** guía el ajuste de parámetros. La **métrica** comunica desempeño según el problema.

- La pérdida debe ser adecuada para optimizar el modelo.
- La métrica debe ser adecuada para decidir si el sistema sirve.
- Pueden coincidir, pero no tienen obligación de hacerlo.

En clasificación probabilística puede minimizarse log-loss y reportarse F1 macro. La primera premia probabilidades asignadas a la clase correcta; la segunda resume un equilibrio entre precision y recall después de producir clases.

### 8.2 Pérdida promedio

Una forma general es:

[
L(f) = \frac{1}{n}\sum_{i=1}^{n}\ell(y_i, f(x_i))
]

- (L(f)) es la pérdida promedio del modelo (f);
- (n) es la cantidad de ejemplos;
- (sum) suma el aporte de todos;
- (y_i) es el target real;
- (f(x_i)) es la predicción;
- (ell) mide el error de un ejemplo.

La fórmula no decide qué errores importan más. Esa decisión puede incorporarse con pesos, otra pérdida o criterios operativos.

### 8.3 Error frecuente

Elegir una métrica porque la biblioteca la muestra por defecto. La métrica debe acordarse con el escenario y, de ser posible, antes de comparar modelos.

---

## 9. Matriz de confusión y métricas binarias

### 9.1 La matriz como mapa de errores

Para una clase positiva y otra negativa:

| Real \ Predicho | Positivo | Negativo |
|---|---:|---:|
| Positivo | TP | FN |
| Negativo | FP | TN |

- **TP, verdadero positivo:** era positivo y se predijo positivo.
- **TN, verdadero negativo:** era negativo y se predijo negativo.
- **FP, falso positivo:** era negativo, pero se predijo positivo.
- **FN, falso negativo:** era positivo, pero se predijo negativo.

“Positivo” no significa bueno. Es la clase de interés elegida para el análisis.

### 9.2 Ejemplo inventado calculado a mano

Supongamos 20 casos:

- TP = 6;
- TN = 9;
- FP = 3;
- FN = 2.

Comprobación: (6+9+3+2=20).

#### Accuracy

[
\text{Accuracy} = \frac{TP+TN}{TP+TN+FP+FN}
]

Símbolo por símbolo:

- (TP+TN) cuenta aciertos;
- (TP+TN+FP+FN) cuenta todos los casos;
- el cociente es la proporción total correcta.

Cálculo:

[
\frac{6+9}{6+9+3+2}=\frac{15}{20}=0{,}75
]

Interpretación: se acertó el 75% de estos ejemplos. No informa por sí sola qué clase sufrió los errores.

#### Precision

[
\text{Precision} = \frac{TP}{TP+FP}
]

- (TP) son positivos predichos correctamente;
- (TP+FP) son todos los casos que el modelo llamó positivos;
- precision responde: “cuando predijo positivo, ¿con qué frecuencia acertó?”.

Cálculo:

[
\frac{6}{6+3}=\frac{6}{9}\approx 0{,}667
]

Interpretación: aproximadamente dos de cada tres predicciones positivas fueron correctas.

#### Recall

[
\text{Recall} = \frac{TP}{TP+FN}
]

- (TP+FN) son todos los positivos reales;
- recall responde: “de los positivos que existían, ¿qué proporción detectó?”.

Cálculo:

[
\frac{6}{6+2}=\frac{6}{8}=0{,}75
]

Interpretación: detectó tres de cada cuatro positivos reales.

#### F1

[
F_1 = 2\cdot\frac{\text{Precision}\cdot\text{Recall}}
{\text{Precision}+\text{Recall}}
]

- (F_1) es la media armónica de precision y recall;
- el producto reúne ambas;
- la suma normaliza;
- el factor 2 deja el resultado en la misma escala;
- la media armónica cae si una de las dos es baja.

Usando (2/3) y (3/4):

[
F_1 = 2\cdot\frac{(2/3)(3/4)}{2/3+3/4}
=2\cdot\frac{1/2}{17/12}
=\frac{12}{17}\approx0{,}706
]

Interpretación: el equilibrio entre calidad de predicciones positivas y cobertura es cercano a 0,706. No significa “70,6% de casos correctos”; esa descripción corresponde a accuracy.

### 9.3 Otro ejemplo: accuracy alta, utilidad nula para la minoría

En 100 casos inventados hay 95 negativos y 5 positivos. Un modelo predice siempre negativo:

- TN = 95;
- FN = 5;
- TP = 0;
- FP = 0;
- accuracy = (95/100=0{,}95);
- recall positivo = (0/(0+5)=0).

La accuracy parece excelente, pero el sistema no detecta ningún positivo. El ejemplo muestra por qué se necesitan baseline y métricas por clase.

### 9.4 Multiclase: una matriz más grande

Con clases A, B y C, las filas representan clases reales y las columnas predicciones. La diagonal contiene aciertos; las celdas fuera de la diagonal muestran confusiones específicas.

Ejemplo inventado:

| Real \ Predicho | A | B | C |
|---|---:|---:|---:|
| A | 8 | 1 | 1 |
| B | 2 | 5 | 1 |
| C | 0 | 2 | 4 |

Total: (10+8+6=24). Aciertos: (8+5+4=17). Accuracy: (17/24\approx0{,}708).

Pero la matriz agrega información: B se confunde dos veces con A; C se confunde dos veces con B. Esas parejas guían análisis textual y revisión del target.

### 9.5 SAIJ transfer

En fuero multiclase, cada clase puede tratarse temporalmente como “esa clase versus el resto” para calcular precision y recall. Las confusiones entre pares pueden revelar:

- lenguaje realmente cercano;
- etiquetas compuestas forzadas;
- reglas de normalización discutibles;
- campos faltantes por tipo de documento;
- drift temporal;
- atajos o metadata filtrada.

La matriz no explica la causa. Indica dónde mirar.

---

## 10. Promedios macro, micro, weighted y balanced accuracy

### 10.1 Por qué hace falta promediar

En multiclase obtenemos una métrica por clase. Para resumir debemos decidir cuánto pesa cada una.

### 10.2 Macro

[
M_{macro}=\frac{1}{K}\sum_{k=1}^{K} M_k
]

- (M_k) es la métrica de la clase (k);
- (K) es la cantidad de clases;
- cada clase pesa lo mismo;
- (sum) suma métricas por clase.

Si recalls de A, B y C son 0,90; 0,60; 0,30:

[
Recall_{macro}=\frac{0{,}90+0{,}60+0{,}30}{3}=0{,}60
]

### 10.3 Weighted

[
M_{weighted}=\sum_{k=1}^{K}\frac{n_k}{n}M_k
]

- (n_k) es el soporte real de la clase (k);
- (n) es el total;
- (n_k/n) es el peso de esa clase.

Si soportes son 80, 15 y 5, con los recalls anteriores:

[
0{,}80(0{,}90)+0{,}15(0{,}60)+0{,}05(0{,}30)
=0{,}72+0{,}09+0{,}015=0{,}825
]

El promedio weighted es alto porque A domina. No está mal calculado; responde una pregunta global dominada por la composición observada.

### 10.4 Micro

Micro suma primero TP, FP y FN de todas las clases y luego calcula la métrica. Cada decisión individual pesa igual. En clasificación multiclase de etiqueta única, micro precision, micro recall y micro F1 suelen coincidir con accuracy porque cada error produce una predicción incorrecta y una clase real perdida.

### 10.5 Material complementario integrado 3 — Por qué macro importa bajo desbalance

Macro obliga a mirar cada clase como una responsabilidad equivalente. Una clase rara no desaparece por tener poco soporte. Es valiosa cuando el objetivo exige calidad transversal o cuando no queremos que las clases grandes decidan solas el promedio.

No siempre macro debe ser la única métrica. Conviene acompañarla con:

- soporte por clase;
- métricas por clase;
- matriz de confusión;
- promedio weighted o micro;
- intervalos o variación entre folds;
- relevancia operacional de cada error.

### 10.6 Balanced accuracy como contexto opcional

**Contexto opcional dentro del nivel DiploDatos.** En multiclase, balanced accuracy puede entenderse como el promedio del recall por clase:

[
\text{Balanced Accuracy}=\frac{1}{K}\sum_{k=1}^{K} Recall_k
]

Es, en este uso, equivalente al recall macro. Sirve para que cada clase tenga el mismo peso, pero no reemplaza precision ni revela qué clases se confunden.

> **Error frecuente:** decir que weighted “corrige” el desbalance. Weighted refleja el soporte; por eso puede ocultar una clase rara. Macro cambia el peso de la pregunta.

---

## 11. Desbalance de clases: problema de aprendizaje y de evaluación

### 11.1 Por qué importa

Cuando unas clases tienen muchos más ejemplos:

- la pérdida promedio puede estar dominada por ellas;
- una baseline mayoritaria puede tener accuracy alta;
- clases raras pueden faltar en algunos folds;
- precision o recall pueden ser inestables;
- las probabilidades pueden reflejar prevalencias históricas;
- el modelo puede casi nunca predecir una clase minoritaria.

### 11.2 Respuestas conceptuales

1. **Métricas adecuadas:** por clase, macro, matriz de confusión y, según el problema, curvas basadas en precision–recall.
2. **Pesos de clase:** asignar mayor costo a errores de clases menos representadas o más importantes.
3. **Submuestreo:** reducir ejemplos de clases grandes. Puede perder información.
4. **Sobremuestreo:** reutilizar o generar más ejemplos minoritarios. Puede aumentar sobreajuste si se replica sin cuidado.
5. **Recolección o revisión:** conseguir mejores etiquetas o más casos reales, si es posible.
6. **Reformular taxonomía:** unir clases solo si tiene sentido jurídico y operativo, no para mejorar una métrica.

Todo remuestreo debe hacerse **dentro de train**, y dentro de cada fold durante validación cruzada. Si se remuestrea antes del split, copias relacionadas pueden cruzar hacia validación.

### 11.3 No confundir rareza con irrelevancia

Una clase escasa puede ser operativamente crítica. Tampoco todo desbalance es un defecto: puede representar la prevalencia real. La decisión es qué desempeño se necesita en cada clase y cómo estimarlo con suficiente incertidumbre.

---

## 12. Validación cruzada: múltiples ensayos, no una cura universal

### 12.1 K-fold ordinaria

Se divide train en (K) partes. En cada iteración, una parte valida y las restantes entrenan. Se obtienen (K) resultados:

[
\bar M = \frac{1}{K}\sum_{k=1}^{K}M_k
]

- (M_k) es la métrica en el fold (k);
- (K) es la cantidad de folds;
- \(\bar M\) resume el desempeño promedio.

También se mira dispersión: resultados muy variables indican sensibilidad a la partición.

### 12.2 Estratificada

Mantiene aproximadamente proporciones de clases en cada fold. Es apropiada como opción inicial de clasificación cuando los casos son intercambiables y no hay grupos ni orden temporal dominante. La cantidad de folds está limitada por la clase menos frecuente: cada fold necesita ejemplos evaluables.

### 12.3 Grupal

Asigna grupos completos a folds. Evita que versiones o entidades relacionadas aparezcan a ambos lados. Estima generalización a grupos no vistos.

### 12.4 Temporal

Usa ventanas que respetan pasado → futuro. Puede entrenar con períodos iniciales y validar en períodos posteriores, avanzando el corte. Estima estabilidad ante evolución.

### 12.5 Qué CV no puede arreglar

La validación cruzada no corrige:

- target mal definido;
- duplicados no identificados;
- fuga previa a la división;
- población no representativa;
- features no disponibles en inferencia;
- drift que no está representado;
- pocos ejemplos reales de una clase;
- métrica mal elegida;
- sobreajuste a la propia CV por probar muchas variantes;
- diferencias entre el experimento y el uso.

CV reduce dependencia de una única partición dentro del esquema elegido. No convierte un esquema equivocado en uno válido.

### 12.6 Ejemplo inventado

Cinco folds producen F1 macro: 0,71; 0,69; 0,42; 0,70; 0,68. El promedio es 0,64, pero el fold de 0,42 exige investigación. Tal vez contiene un grupo, período o clase distinta. Reportar solo 0,64 borra la evidencia más útil.

---

## 13. Pipelines de preprocesamiento y fuga de información

### 13.1 Regla de oro

Toda transformación que **aprende algo de los datos** debe ajustarse solo con train y luego aplicarse sin reajuste a validación o test.

Esto incluye:

- vocabulario;
- IDF;
- imputación por media, mediana o moda;
- escalado;
- selección estadística de features;
- reducción dimensional;
- remuestreo;
- calibración;
- elección de threshold;
- reglas inducidas por frecuencias.

### 13.2 Pipeline conceptual

```text
fuente congelada
  → split según futuro
  → en train: ajustar transformación
  → transformar train
  → entrenar modelo
  → aplicar transformación ya ajustada a validación
  → elegir configuración
  → evaluación final en test
```

En validación cruzada, cada fold debe repetir el ajuste usando solo su porción de entrenamiento. No se construye un vocabulario global antes de rotar folds.

### 13.3 Tipos de leakage

- **Target leakage:** una feature contiene directa o indirectamente la respuesta.
- **Preprocessing leakage:** una transformación usa estadísticas de validación o test.
- **Duplicate leakage:** casos casi idénticos cruzan particiones.
- **Temporal leakage:** se usa información futura para predecir pasado.
- **Selection leakage:** se elige el modelo mirando repetidamente test.

### 13.4 Transferencia SAIJ

Un campo que codifica organismo, materia o una ruta de carga podría revelar fuero sin usar contenido. No debe eliminarse automáticamente: primero se documenta su disponibilidad y si representa una señal legítima para el uso. Si se prohíbe por ser atajo, queda registrado.

**Decisión de Javier — pendiente:** definir lista de features autorizadas y dudosas, con motivo y momento de disponibilidad.

---

## 14. Representar texto sin perder la intuición

### 14.1 Del documento al vocabulario

Un modelo clásico no recibe prosa directamente. Se define un **vocabulario** de términos y cada documento se convierte en un vector.

Ejemplo inventado de train:

1. “recurso laboral aceptado”
2. “contrato laboral”
3. “recurso penal”

Vocabulario ordenado:

```text
[aceptado, contrato, laboral, penal, recurso]
```

### 14.2 Bag of Words

Bag of Words ignora el orden global y cuenta apariciones.

- Documento 1 → ([1,0,1,0,1])
- Documento 2 → ([0,1,1,0,0])
- Documento 3 → ([0,0,0,1,1])

Cada posición corresponde al mismo término en todos los documentos. Se conserva presencia o frecuencia, pero no la sintaxis completa.

### 14.3 Conteos binarios

En una representación binaria, cada posición indica si el término aparece:

[
x_{ij}=\begin{cases}
1 & \text{si el término } j \text{ aparece en el documento } i\\
0 & \text{si no aparece}
\end{cases}
]

Esto reduce la influencia de repeticiones. Puede ser útil cuando “apareció o no” importa más que cuántas veces.

### 14.4 N-gramas

- Unigrama: una palabra, como “seguridad”.
- Bigrama: dos consecutivas, como “seguridad social”.
- Trigrama: tres consecutivas.

Los n-gramas recuperan contexto local y expresiones compuestas, pero amplían mucho el vocabulario. También hacen más rara cada feature.

En texto jurídico, expresiones de varias palabras pueden ser relevantes. Pero incluir todos los n-gramas sin límite aumenta memoria, ruido y riesgo de memorizar fórmulas específicas.

### 14.5 TF-IDF

TF-IDF combina frecuencia en un documento con rareza en el corpus de entrenamiento. Una forma conceptual es:

[
TFIDF(t,d)=TF(t,d)\cdot IDF(t)
]

- (t) es un término;
- (d) es un documento;
- (TF(t,d)) mide cuánto aparece (t) en (d);
- (IDF(t)) baja el peso de términos presentes en muchos documentos;
- el producto da peso mayor a términos relativamente característicos.

Una forma suavizada de IDF es:

[
IDF(t)=\log\left(\frac{1+N}{1+df(t)}\right)+1
]

- (N) es la cantidad de documentos de train;
- (df(t)) es cuántos documentos de train contienen (t);
- (1+) evita divisiones problemáticas y suaviza;
- (log) comprime diferencias grandes;
- el (+1) final conserva pesos positivos según esta convención.

Ejemplo inventado: en 10 documentos, “recurso” aparece en 8 y “quiebra” en 1. “Quiebra” recibe IDF mayor. Eso no prueba que sea mejor feature: solo que es más rara.

### 14.6 Normalización

Los documentos tienen longitudes distintas. Sin normalización, un texto largo puede acumular mayores conteos o pesos solo por extensión. Normalizar un vector, por ejemplo a longitud euclídea 1, permite comparar patrones relativos.

Para un vector (x):

[
\|x\|_2=\sqrt{\sum_{j=1}^{p}x_j^2},
\qquad
x' = \frac{x}{\|x\|_2}
]

- (|x|_2) es la longitud del vector;
- se elevan componentes al cuadrado, se suman y se toma raíz;
- (x') es el vector reescalado;
- la dirección se conserva, la magnitud se controla.

### 14.7 Vocabulario desconocido

El vocabulario se aprende con train. Si aparece una palabra nueva en validación, test o producción y no está en ese vocabulario, la representación clásica la ignora. No se agrega reajustando el vectorizador, porque eso cambiaría el espacio de features y usaría información externa a train.

Esta limitación importa con neologismos, cambios normativos, errores ortográficos y nombres nuevos. Los n-gramas de caracteres pueden aliviar parte del problema, pero son una decisión de representación a validar, no una solución automática.

### 14.8 Material complementario integrado 7 — Intuición de vectores dispersos e implicancias computacionales

Un vocabulario puede tener miles de términos, pero cada documento contiene solo una pequeña parte. El vector tiene muchos ceros: es **disperso**.

Ejemplo: vocabulario de 10.000 términos, documento con 80 términos distintos. Como máximo 80 posiciones son no nulas; más de 9.900 son cero. Guardar todos los ceros desperdicia memoria. Las estructuras dispersas registran principalmente posiciones y valores no nulos.

Implicancias:

- permiten trabajar con espacios de alta dimensión;
- algunos modelos y operaciones están optimizados para matrices dispersas;
- convertir sin necesidad a formato denso puede agotar memoria;
- aumentar n-gramas eleva dimensiones y costo;
- selección de vocabulario no es solo estadística: también es computacional;
- centrar ciertos datos puede destruir dispersidad.

La alta dimensión no significa que cada documento sea “complejo” en todas las features. Significa que el corpus ofrece muchas features posibles y cada caso activa pocas.

### 14.9 Hallazgos del equipo como roadmap

**Pendiente de reproducción:** el notebook del equipo compara campos textuales, limpia marcas, examina longitudes, vocabulario, stopwords, n-gramas y TF-IDF por categorías. Estas observaciones orientan las preguntas de representación, pero sus cantidades, umbrales y conclusiones no se presentan aquí como resultados de Javier.

---

## 15. Naive Bayes para texto, desde Bayes

### 15.1 Pregunta probabilística

Queremos comparar:

[
P(y=c\mid x)
]

Se lee: probabilidad de que la clase sea (c) dado el documento representado por (x).

El teorema de Bayes permite escribir:

[
P(y=c\mid x)=\frac{P(x\mid y=c)P(y=c)}{P(x)}
]

Símbolo por símbolo:

- (P(y=c\mid x)): probabilidad posterior de la clase después de observar el texto;
- (P(x\mid y=c)): verosimilitud de observar esas features si la clase fuera (c);
- (P(y=c)): probabilidad previa o prior de la clase;
- (P(x)): probabilidad del documento bajo todas las clases;
- la barra vertical significa “condicionado a”.

Para elegir la clase con mayor posterior, (P(x)) es igual para todas las clases candidatas. Por eso comparamos:

[
\hat y=\arg\max_c P(y=c)P(x\mid y=c)
]

- (hat y) es la clase predicha;
- (arg\max_c) elige la clase con mayor valor;
- el producto combina prior y compatibilidad del texto.

### 15.2 La suposición ingenua

Si (x) contiene features (x_1,\ldots,x_p), Naive Bayes asume independencia condicional dada la clase:

[
P(x\mid y=c)\approx\prod_{j=1}^{p}P(x_j\mid y=c)
]

- (prod) multiplica aportes de todas las features;
- (P(x_j\mid y=c)) mide compatibilidad de la feature (j) con la clase;
- “condicional” significa que se supone independencia una vez conocida la clase.

En lenguaje, las palabras no son realmente independientes: “seguridad” y “social” aparecen relacionadas. La suposición es simplificadora, no una descripción literal. Aun así, el modelo puede ser una baseline fuerte y eficiente porque necesita estimaciones simples y trabaja bien con conteos dispersos.

### 15.3 Ejemplo inventado a mano

Tenemos dos clases, A y B, y un vocabulario de tres términos: `laboral`, `pena`, `contrato`.

Conteos de train inventados después de suavizar:

| Término | (P(t\mid A)) | (P(t\mid B)) |
|---|---:|---:|
| laboral | 0,50 | 0,10 |
| pena | 0,10 | 0,60 |
| contrato | 0,40 | 0,30 |

Priors: (P(A)=0{,}6), (P(B)=0{,}4).

Documento nuevo: “laboral contrato”. Usando presencia simplificada:

[
Score(A)=0{,}6\times0{,}50\times0{,}40=0{,}12
]

[
Score(B)=0{,}4\times0{,}10\times0{,}30=0{,}012
]

Como (0{,}12>0{,}012), se predice A. Estos scores no están normalizados como probabilidades finales; para comparar alcanza el orden.

### 15.4 El problema del cero y suavizado

Si un término nunca apareció en train para una clase, su probabilidad estimada sería cero. Al multiplicar, todo el score se vuelve cero. El suavizado aditivo evita que una ausencia observada implique imposibilidad absoluta.

Para Naive Bayes multinomial:

[
P(t\mid c)=\frac{N_{t,c}+\alpha}{N_c+\alpha V}
]

- (N_{t,c}) es el conteo del término (t) en documentos de clase (c);
- (N_c) es el total de conteos de términos en la clase (c);
- (V) es el tamaño del vocabulario;
- (alpha) es la intensidad de suavizado, positiva;
- el numerador agrega (alpha) al término;
- el denominador agrega (alpha) para cada uno de los (V) términos.

Ejemplo: si (N_{t,c}=0), (N_c=20), (V=5), (alpha=1):

[
P(t\mid c)=\frac{0+1}{20+1\cdot5}=\frac{1}{25}=0{,}04
]

Ya no es cero. No inventa evidencia fuerte; reserva una probabilidad pequeña.

### 15.5 Fortalezas

- rápido de entrenar e inferir;
- natural para conteos y matrices dispersas;
- maneja multiclase de forma nativa;
- ofrece baseline probabilística interpretable a nivel de términos;
- funciona con muchos features y relativamente pocos ejemplos;
- permite inspeccionar qué términos favorecen cada clase.

### 15.6 Límites

- independencia condicional irrealista;
- sensibilidad a representación, vocabulario y suavizado;
- correlaciones entre términos pueden contar señal repetida;
- negación y orden se representan pobremente con unigramas;
- priors pueden perjudicar clases raras;
- probabilidades pueden no estar bien calibradas;
- no corrige labels ruidosos ni target ambiguo;
- términos espurios pueden dominar.

### 15.7 Transferencia SAIJ

Naive Bayes puede servir como baseline de texto, no como veredicto final. Si predice bien usando términos asociados al nombre del fuero incluido en el propio texto, hay que decidir si esa señal es legítima o una fuga semántica respecto del uso. El análisis de errores y de features debe acompañar la métrica.

> **Error frecuente:** interpretar “Naive” como modelo inútil. El nombre describe el supuesto de independencia, no su valor experimental. Su simplicidad lo vuelve un control muy informativo.

---

## 16. Manejo multiclase: nativo, uno contra el resto y uno contra uno

### 16.1 Nativo multiclase

Algunos modelos comparan todas las clases dentro de una sola formulación. Naive Bayes calcula un score por clase naturalmente. Otros modelos pueden producir una distribución conjunta sobre (K) clases.

### 16.2 One-vs-Rest, OvR

Se entrenan (K) clasificadores binarios. Cada uno distingue una clase del resto. Luego se elige el score mayor.

Ventajas: simple y permite reutilizar clasificadores binarios. Límites: cada problema induce desbalance; scores separados pueden no ser comparables; en multietiqueta la decisión ya no debe ser “un único ganador”.

### 16.3 One-vs-One, OvO

Se entrena un clasificador por cada par de clases:

[
\frac{K(K-1)}{2}
]

Con (K=4): (4\cdot3/2=6) clasificadores. Cada uno ve solo dos clases y luego se combinan votos. El costo crece cuadráticamente con (K).

### 16.4 No profundizar antes de formular

La elección entre nativo, OvR u OvO llega después de definir si SAIJ es multiclase o multietiqueta, qué modelos se comparan y qué costo tiene cada estrategia. No resuelve la ambigüedad del target.

---

## 17. Diseñar un experimento como una cadena auditable

### 17.1 Secuencia mínima

```text
baseline
  → representación
  → modelo
  → métrica
  → split
  → resultado
  → análisis de errores
```

En realidad, métrica y split deben fijarse antes de mirar resultados. El diagrama indica qué piezas debe declarar cada fila experimental.

### 17.2 Comparar una cosa por vez

Para atribuir una diferencia:

- mismo split;
- misma población;
- mismo target;
- misma métrica;
- misma semilla cuando corresponda;
- cambiar una decisión principal por comparación.

Si se cambia representación, modelo y split a la vez, una mejora no tiene causa identificable.

### 17.3 Resultado completo

Un resultado no es una sola cifra. Debe incluir:

- baseline;
- métrica primaria y secundarias;
- resultados por clase;
- matriz de confusión;
- variación entre folds o particiones;
- costo y cobertura;
- errores cualitativos;
- limitaciones;
- decisión siguiente.

### 17.4 Hipótesis experimental

Ejemplo inventado:

> “Los bigramas podrían mejorar la separación entre clases con expresiones compuestas, pero aumentarán dimensionalidad y riesgo de capturar plantillas. Se compararán contra unigramas, manteniendo modelo, split y métrica.”

Esta redacción obliga a anticipar beneficio y costo.

---

## 18. Reproducibilidad, ledger y taxonomía de errores

### 18.1 Material complementario integrado 6 — Ledger de experimentos y taxonomía de errores

Un **ledger** es una tabla cronológica y auditable. Cada ejecución relevante registra:

| Campo | Contenido |
|---|---|
| ID | identificador único |
| Fecha | momento de ejecución |
| Dataset | versión, hash o snapshot |
| Población | inclusiones y exclusiones |
| Target | regla y versión |
| Features | campos autorizados |
| Split | tipo, semilla, reloj o grupo |
| Representación | vocabulario, n-gramas, ponderación |
| Modelo | familia |
| Hiperparámetros | configuración |
| Métrica primaria | definida antes del resultado |
| Resultados | promedio, dispersión y por clase |
| Artefactos | matriz, reporte y errores |
| Decisión | conservar, descartar o revisar |
| Motivo | interpretación razonada |

Guardar solo “modelo X dio 0,82” impide reproducir y comparar. El número no identifica qué dataset, clase, split o versión lo produjo.

### 18.2 Taxonomía de errores

Además del ledger, cada revisión puede clasificar errores:

- target dudoso;
- texto insuficiente;
- categoría compuesta;
- confusión semántica entre pares;
- documento extremadamente corto o largo;
- marca o plantilla;
- drift temporal;
- geografía u organismo no visto;
- duplicado o versión;
- predicción de baja confianza;
- error de representación;
- caso fuera de población.

La taxonomía convierte una lista de fallos en decisiones. Si muchos errores son labels ambiguos, aumentar capacidad puede no ayudar.

---

## 19. Análisis de errores: dónde mirar después de la métrica

### 19.1 Por clase

Comparar precision, recall, F1 y soporte. Identificar clases nunca predichas o con alta confusión. Evitar interpretar diferencias diminutas cuando hay pocos casos.

### 19.2 Por longitud de texto

Agrupar textos cortos, medios y largos con umbrales definidos en train o por criterios previos. Los cortos pueden carecer de señal; los largos pueden diluir términos o consumir más recursos.

### 19.3 Por tiempo

Evaluar por período y observar degradación. Distinguir fecha judicial de fecha de carga si ambas existen. Un cambio abrupto puede reflejar migración o taxonomía, no conducta del modelo aislada.

### 19.4 Por geografía

Comparar regiones o jurisdicciones solo si la variable es válida y el tamaño permite. Un modelo puede aprender vocabulario local y fallar en geografías no representadas.

### 19.5 Por tipo de documento

Sumarios, fallos u otras poblaciones pueden tener esquemas y longitudes distintas. Una métrica agregada puede mezclar tareas heterogéneas.

### 19.6 Por pares de confusión

Ordenar celdas fuera de la diagonal por cantidad y por tasa relativa. Leer ejemplos de cada par y preguntar:

- ¿la distinción existe en el texto disponible?
- ¿el target es coherente?
- ¿son categorías compuestas?
- ¿hay términos compartidos?
- ¿hay una regla de mapeo discutible?

### 19.7 Error analysis no es buscar anécdotas favorables

La muestra debe seguir un protocolo: por ejemplo, revisar una cantidad fija de errores de cada clase y algunos aciertos. Solo mirar errores llamativos puede producir explicaciones sesgadas.

---

## 20. Límites éticos y operativos

### 20.1 Representación

El corpus puede sobrerrepresentar épocas, organismos, tipos documentales o clases. El modelo aprende la distribución disponible, no una población ideal. Reportar rendimiento global sin cobertura oculta ese límite.

### 20.2 Drift

El lenguaje, las normas, los procedimientos y la carga cambian. Hay drift cuando la relación entre entradas, etiquetas o prevalencias evoluciona. Se necesita monitoreo por tiempo y un criterio de reentrenamiento o retiro.

### 20.3 Shortcuts

Un shortcut es una señal fácil que correlaciona con el target pero no representa el criterio deseado. Nombres institucionales, formatos o marcas pueden dar alto desempeño. La solución no es siempre borrarlos: es decidir si estarán disponibles, si son legítimos y si vuelven frágil al sistema.

### 20.4 Revisión humana

La revisión humana debe diseñarse, no agregarse como frase de cierre. Hay que definir:

- qué casos revisa;
- qué información ve;
- cuánto tiempo tiene;
- cómo corrige;
- cómo se registran desacuerdos;
- quién tiene responsabilidad final;
- qué ocurre si modelo y persona discrepan.

### 20.5 Material complementario integrado 8 — Abstención y revisión humana como elección operacional

Un clasificador no tiene por qué decidir siempre. Puede abstenerse cuando:

- el score máximo es bajo;
- dos clases tienen scores cercanos;
- el texto está vacío o fuera de rango;
- aparece vocabulario desconocido en exceso;
- el caso pertenece a una población no cubierta;
- hay señales de drift;
- una regla de seguridad lo exige.

La abstención cambia la evaluación. Se deben reportar al menos:

- **cobertura:** proporción de casos decididos automáticamente;
- desempeño en los casos cubiertos;
- desempeño y carga de revisión en los abstenciones;
- distribución de abstenciones por clase y subgrupo.

Un sistema con menor cobertura puede ser más útil si decide con mayor seguridad y deriva el resto. Pero no hay que esconder errores excluyendo sistemáticamente clases difíciles.

### 20.6 Material complementario integrado 5 — Calibración de probabilidades y umbrales, contexto opcional

**Contexto opcional.** Una probabilidad está bien calibrada si, entre casos a los que el modelo asigna aproximadamente 0,7, cerca del 70% pertenece a la clase en condiciones comparables. Clasificar bien y calibrar bien son propiedades distintas.

Un **threshold** transforma score o probabilidad en decisión. Bajarlo suele aumentar cobertura o recall y también falsos positivos; subirlo suele hacer lo contrario. En multiclase pueden usarse reglas sobre probabilidad máxima o margen entre las dos primeras clases.

La calibración se aprende con datos separados de los usados para ajustar el modelo, y el threshold se elige con validación según costos operativos. Test conserva su rol final. Este tema queda opcional: primero hay que dominar matriz de confusión, métricas y particiones.

---

## 21. Del TP2 curado al entrenamiento futuro

### 21.1 Qué entrega TP2 conceptualmente

TP2, tal como se preparó en la Materia 2, puede entregar:

- fuente congelada y trazable;
- definición de unidad;
- población incluida y cuarentenas;
- target construido con tabla de mapeo;
- texto curado sin borrar originales;
- grupos de duplicados o versiones;
- features autorizadas, dudosas y prohibidas;
- propuesta de split;
- métricas de calidad y sesgo;
- diccionario, linaje y decisiones.

Eso es infraestructura de aprendizaje. No es “solo limpieza”.

### 21.2 Qué TP2 no tiene que fingir

TP2 no necesita demostrar un modelo final si la consigna no lo exige. Tampoco debe inventar:

- cantidad definitiva de clases;
- performance esperada;
- mejor algoritmo;
- threshold óptimo;
- capacidad de despliegue;
- validez jurídica de predicciones.

Puede cerrar con decisiones y contratos listos para una etapa posterior.

### 21.3 Contrato de handoff

Antes de entrenar, el equipo futuro debería poder responder:

1. ¿Qué snapshot exacto usamos?
2. ¿Qué representa cada fila?
3. ¿Cómo se creó cada (y_i)?
4. ¿Qué casos se excluyeron y por qué?
5. ¿Qué grupos no pueden separarse?
6. ¿Qué fecha ordena un split temporal?
7. ¿Qué texto existe al momento de inferencia?
8. ¿Qué campos están prohibidos por fuga o propósito?
9. ¿Qué clases son ambiguas o compuestas?
10. ¿Qué uso y persona usuaria se asumen?

Si no hay respuesta, el primer experimento debe corregir el contrato, no compensarlo con un modelo.

### 21.4 Secuencia futura detallada

#### Paso A — Congelar la tarea

Escribir una oración completa: “Para [persona o sistema], usando [información disponible], proponer [salida] sobre [población], para [uso], evaluado con [métrica] y [split]”.

#### Paso B — Auditar el target

Medir soporte, revisar mapeos, muestrear etiquetas, identificar compuestas y registrar desacuerdos. Decidir multiclase o multietiqueta por propósito.

#### Paso C — Reservar test

Aplicar split grupal o temporal si corresponde. No aprender vocabulario antes. Guardar test sin inspección orientada a selección.

#### Paso D — Construir baseline

Crear mayoría y una baseline de texto simple. Evaluarlas con las mismas métricas y particiones.

#### Paso E — Comparar representaciones

Por ejemplo: binaria, conteos, unigramas, bigramas o TF-IDF. Cambiar una dimensión por vez y registrar costo disperso.

#### Paso F — Comparar modelos

Empezar con modelos apropiados para texto disperso, incluyendo Naive Bayes como control. Seleccionar hiperparámetros dentro de train.

#### Paso G — Analizar errores

Por clase, longitud, período, geografía, tipo documental y pares de confusión. Leer casos con protocolo.

#### Paso H — Diseñar operación

Definir salida, revisión, abstención, cobertura, monitoreo y retiro. No desplegar solo porque una métrica supera baseline.

### 21.5 Hallazgos del equipo que solo funcionan como roadmap

**Pendientes de reproducción:** el notebook del grupo informa decisiones y observaciones sobre poblaciones documentales, normalización de materia, etiquetas combinadas, longitud y limpieza de texto, términos compartidos, TF-IDF y posibles artefactos temporales. En esta materia se usan para formular controles:

- verificar población antes de entrenar;
- revisar si el target representa una o varias etiquetas;
- proteger grupos relacionados;
- comparar futuros aleatorio, grupal y temporal;
- inspeccionar vocabulario por clase;
- analizar pares de confusión cercanos;
- evitar marcas de formato.

No se copian sus cantidades ni se afirma que Javier reprodujo sus resultados.

### 21.6 Matriz de decisiones para Javier

| Decisión | Opciones conceptuales | Evidencia necesaria | Estado |
|---|---|---|---|
| Unidad | documento, decisión, versión | identificadores y proceso de carga | Pendiente |
| Target | multiclase, multietiqueta, ranking | taxonomía y revisión jurídica | Pendiente |
| Población | una o varias clases documentales | cobertura y uso | Pendiente |
| Texto | cuerpo, sumario, combinación | disponibilidad y calidad | Pendiente |
| Features | solo texto o metadata autorizada | riesgo de shortcut | Pendiente |
| Split principal | aleatorio, grupal, temporal | futuro operacional | Pendiente |
| Métrica primaria | macro-F1 u otra justificada | costo de errores | Pendiente |
| Baseline | mayoría y texto simple | mismo protocolo | Pendiente |
| Abstención | sí/no y regla | capacidad de revisión | Pendiente |

La tabla no prescribe respuestas. Hace visibles las decisiones que un notebook podría esconder.

---

## 22. Caso integrado inventado, sin código

### 22.1 Formulación

Tenemos 60 documentos inventados en tres clases A, B y C. Hay 30 grupos de dos versiones. Los primeros 40 documentos pertenecen a períodos anteriores y 20 a un período posterior. El uso real recibe grupos nuevos en el futuro.

### 22.2 Diseño

- Unidad: documento, con `group_id` para versiones.
- Target: una clase única revisada.
- Entrada: texto sin metadata de clase.
- Split: últimos períodos como test; dentro del pasado, validación grupal estratificada cuando sea viable.
- Baseline: clase mayoritaria.
- Representación: unigramas TF-IDF ajustados en cada train.
- Modelo inicial: Naive Bayes.
- Métrica primaria: F1 macro.
- Diagnósticos: matriz, por clase, período, longitud y grupo.

### 22.3 Qué sería fuga

- calcular IDF con los 60 antes del split;
- poner una versión en train y otra en test;
- elegir suavizado mirando test;
- incluir un código que revela la clase;
- eliminar errores de test y volver a reportar sin declarar exclusión.

### 22.4 Qué puede concluirse

Si el modelo supera baseline en validación pero cae en test temporal, podemos concluir que la transferencia al período posterior es peor bajo ese experimento. No podemos afirmar causalmente por qué sin análisis. Podrían existir drift, cambios de etiquetas, grupos o texto.

---

## 23. Errores frecuentes en la primera materia de AA

1. **Empezar por el algoritmo.** Sin tarea y split, el resultado no tiene interpretación.
2. **Llamar feature a cualquier columna.** Debe estar disponible y autorizada al inferir.
3. **Tratar el target construido como verdad.** Su linaje y ambigüedad siguen vigentes.
4. **Evaluar en train.** Mide ajuste, no generalización.
5. **Usar test para decidir.** Lo convierte en validación.
6. **Estratificar duplicados.** Conserva clases pero permite fuga grupal.
7. **Ajustar TF-IDF con todo el corpus.** Usa información de validación y test.
8. **Reportar solo accuracy.** Puede ocultar clases raras.
9. **Promediar sin nombrar el promedio.** Macro y weighted responden preguntas distintas.
10. **Ver CV como garantía.** Repite el esquema; no corrige un esquema inválido.
11. **Confundir score con probabilidad calibrada.** El orden puede ser útil sin interpretar el número literalmente.
12. **Reentrenar hasta mejorar test.** Produce selección sobre test.
13. **Eliminar clases raras por comodidad.** Requiere razón de dominio, no solo estadística.
14. **Tomar correlaciones textuales como explicación jurídica.** El modelo detecta asociación predictiva.
15. **Dejar revisión humana sin diseño.** “Lo revisa una persona” no define operación.

---

## 24. Ejercicios conceptuales progresivos — antes del código

Los datos de estos ejercicios son inventados salvo que se indique una decisión SAIJ pendiente. Respondé primero sin mirar la clave.

### Ejercicio 1 — Aprender no es comprender

Un modelo acierta usando una marca de plantilla asociada a cada clase. Explicá qué aprendió y qué prueba falta.

### Ejercicio 2 — Formulación completa

Transformá “predecir fuero” en una formulación que incluya unidad, (X), (y), salida, usuario, uso y criterio de éxito.

### Ejercicio 3 — Regresión o clasificación

Decidí el tipo de problema para: a) estimar minutos de revisión; b) asignar A/B/C; c) predecir un código numérico que en realidad representa categorías.

### Ejercicio 4 — Multiclase o multietiqueta

Un documento puede pertenecer a CIVIL y COMERCIAL a la vez. ¿Qué formulación corresponde? ¿Qué tendría que ocurrir para justificar multiclase?

### Ejercicio 5 — Parámetro o hiperparámetro

Clasificá: peso aprendido de la palabra “contrato”, tamaño máximo del vocabulario, intensidad de suavizado y prior estimado desde train.

### Ejercicio 6 — Roles de particiones

Indicá dónde se ajustan pesos, dónde se elige el rango de n-gramas y dónde se estima el resultado final.

### Ejercicio 7 — Cuatro futuros

Relacioná aleatorio, estratificado, grupal y temporal con cuatro usos: nueva fila de la misma mezcla; misma mezcla conservando clases; expediente nuevo; año posterior.

### Ejercicio 8 — Baseline mayoritaria

Hay 70 A, 20 B y 10 C. ¿Qué accuracy obtiene la baseline mayoritaria? ¿Qué recalls por clase obtiene?

### Ejercicio 9 — Sobreajuste

Modelo M1: train 0,98 y validación 0,55. Modelo M2: train 0,72 y validación 0,69. ¿Qué diagnósticos iniciales proponés sin declarar ganador definitivo?

### Ejercicio 10 — Matriz binaria

Con TP=12, TN=20, FP=4 y FN=4, calculá accuracy, precision, recall y F1.

### Ejercicio 11 — Métrica y costo

Si lo más costoso es asignar automáticamente una clase equivocada, ¿qué aspecto mirarías? Si lo más costoso es no detectar casos de una clase crítica, ¿qué cambia?

### Ejercicio 12 — Macro versus weighted

Dos clases tienen recall 0,90 y 0,20; sus soportes son 90 y 10. Calculá recall macro y weighted. Interpretá la diferencia.

### Ejercicio 13 — CV con clase rara

La clase C tiene tres ejemplos. ¿Qué problema aparece al intentar cinco folds estratificados? ¿Qué alternativas conceptuales hay?

### Ejercicio 14 — Leakage de vocabulario

Se aprende el vocabulario y el IDF con todo el dataset y después se hace cross-validation. ¿Por qué es fuga aunque no se hayan usado explícitamente las etiquetas de validación?

### Ejercicio 15 — Sparse

Un vocabulario tiene 20.000 términos y un documento activa 100. ¿Por qué conviene una estructura dispersa y qué operación podría volverla costosa?

### Ejercicio 16 — TF-IDF

Dos palabras aparecen tres veces en un documento. Una aparece en casi todo train y la otra solo en pocos documentos. ¿Cuál tendrá mayor IDF y qué no permite concluir eso?

### Ejercicio 17 — Naive Bayes y cero

¿Por qué un término nunca visto en una clase puede anular el score sin suavizado? Explicá cómo cambia con (alpha>0).

### Ejercicio 18 — N-gramas

¿Qué aporta el bigrama “seguridad social” frente a unigramas? ¿Qué costo introduce?

### Ejercicio 19 — Error analysis

Una caída se concentra en textos cortos de una clase y período. Proponé tres hipótesis y una comprobación para cada una.

### Ejercicio 20 — Abstención

Un sistema decide solo cuando el score máximo supera un umbral. ¿Qué dos familias de resultados debe reportar además de la métrica de los casos decididos?

### Ejercicio 21 — TP2 a entrenamiento

Enumerá cinco artefactos de TP2 que deben entregarse antes de ajustar un modelo.

### Ejercicio 22 — Hallazgo ajeno

El notebook del equipo informa una aparente señal temporal. Redactá cómo usarla sin presentarla como resultado de Javier.

---

## 25. Clave de respuestas razonadas

### Respuesta 1

Aprendió una correlación entre marca y clase dentro de los datos observados. No hay evidencia de que haya aprendido contenido. Hace falta una evaluación donde la marca no determine la clase, además de verificar si esa señal existirá y será legítima en uso. La prueba puede incluir remover la marca, separar plantillas por grupos y evaluar en otro período.

### Respuesta 2

Una respuesta posible: “Para asistir a una persona revisora, usar el texto disponible de cada documento individual para proponer un ranking de fueros basado en un target versionado; evaluar con F1 macro y métricas por clase sobre grupos o períodos no vistos, comparando con una baseline y permitiendo abstención”. Cada elemento puede cambiar, pero no debe omitirse. En SAIJ real queda pendiente definir unidad y taxonomía.

### Respuesta 3

a) Regresión, porque minutos es continuo. b) Clasificación multiclase, si hay una clase única. c) Clasificación: el significado es categórico aunque el almacenamiento use números. Elegir por tipo semántico evita aplicar distancias o promedios sin sentido.

### Respuesta 4

Corresponde multietiqueta si ambas ramas son simultáneamente válidas. Multiclase podría justificarse si el uso exige una categoría principal única y existe una regla revisada, auditable y consistente para construirla. La comodidad del algoritmo no es justificación.

### Respuesta 5

El peso de “contrato” y el prior estimado son parámetros aprendidos con train. Tamaño de vocabulario y suavizado son hiperparámetros elegidos mediante validación. Una implementación puede tratar algún prior como configuración; lo importante es declarar si se aprende o se fija.

### Respuesta 6

Los pesos y todas las estadísticas aprendidas se ajustan en train. El rango de n-gramas se elige con validación o CV interna. Test se usa una vez para estimar el procedimiento final. Si test decide n-gramas, deja de ser test independiente.

### Respuesta 7

Aleatorio: nueva fila intercambiable de la misma mezcla. Estratificado: misma pregunta preservando proporciones de clase. Grupal: expediente o entidad nunca visto, manteniendo sus filas juntas. Temporal: año o período posterior. Si el uso combina futuros, pueden reportarse pruebas separadas con nombres explícitos.

### Respuesta 8

Predice siempre A y acierta 70 de 100: accuracy 0,70. Recall A = 1 porque detecta los 70 A. Recall B = 0 y recall C = 0. El buen total convive con fracaso completo en dos clases; por eso la baseline es control y no resultado suficiente.

### Respuesta 9

M1 sugiere alta brecha y posible sobreajuste, fuga de selección o diferencia fuerte entre conjuntos. M2 sugiere menor brecha y quizá mejor estabilidad, pero su nivel debe compararse con baseline y métricas por clase. Sin saber métrica, split, dispersión y costo no se declara ganador.

### Respuesta 10

Total (=12+20+4+4=40). Accuracy (=(12+20)/40=32/40=0{,}80). Precision (=12/(12+4)=12/16=0{,}75). Recall (=12/(12+4)=0{,}75). Como precision y recall son iguales, F1 también es 0,75. Cada cifra responde una pregunta distinta.

### Respuesta 11

Para evitar asignaciones positivas equivocadas, precision de la clase de interés y los falsos positivos son centrales, junto con cobertura y abstención. Para no perder casos críticos, recall y falsos negativos ganan prioridad. En multiclase hay que definir cada clase de interés y revisar la matriz completa; no existe un “positivo” universal.

### Respuesta 12

Macro (=(0{,}90+0{,}20)/2=0{,}55). Weighted (=0{,}90(90/100)+0{,}20(10/100)=0{,}81+0{,}02=0{,}83). Macro muestra que una clase funciona muy mal dándoles igual peso. Weighted refleja que la clase grande domina la población.

### Respuesta 13

No se pueden distribuir tres casos de C entre cinco folds garantizando presencia en cada validación. Puede reducirse (K), recolectar más ejemplos, usar una partición diseñada con cautela o reportar incertidumbre y métricas por clase. Duplicar casos antes de dividir no crea evidencia independiente y puede causar fuga.

### Respuesta 14

El vocabulario e IDF incorporaron qué términos existen y cuán frecuentes son en los folds que luego simulan ser no vistos. Aunque no usen (y), la transformación aprendió de (X) de validación. Debe ajustarse dentro de cada train fold y aplicarse sin reajuste.

### Respuesta 15

Solo 100 de 20.000 posiciones tienen valor; guardar 19.900 ceros desperdicia memoria y cómputo. Una estructura dispersa guarda posiciones no nulas. Convertir a denso o aplicar transformaciones que llenen ceros puede volver costoso el proceso. Agregar muchos n-gramas también amplía dimensiones.

### Respuesta 16

La palabra presente en pocos documentos tendrá mayor IDF. Eso indica rareza documental, no relevancia causal, calidad jurídica ni poder predictivo. Puede ser un error, nombre propio o artefacto. Su utilidad se prueba en validación y análisis de features.

### Respuesta 17

Naive Bayes multiplica probabilidades por feature. Un factor cero vuelve cero todo el producto para esa clase. Con (alpha>0), el conteo cero recibe una masa pequeña y el denominador se ajusta para todas las palabras. Así “no observado” deja de significar “imposible”.

### Respuesta 18

El bigrama conserva una expresión compuesta que los unigramas separan. Puede distinguir “seguridad social” de usos independientes. El costo es un vocabulario mayor, más dispersidad, mayor memoria y posibilidad de capturar frases demasiado específicas.

### Respuesta 19

Hipótesis 1: textos cortos no contienen señal; comprobar cobertura de términos y ejemplos. Hipótesis 2: cambió el formato en ese período; comparar esquema, marcas y longitudes. Hipótesis 3: target de esa clase cambió o es ambiguo; revisar mapeos y una muestra etiquetada. También habría que descartar grupos o duplicados mal separados.

### Respuesta 20

Debe reportar cobertura: qué proporción decidió. También resultados de los abstenciones: carga de revisión, distribución por clase y subgrupo, y si efectivamente concentran casos difíciles. La métrica sobre cubiertos puede mejorar artificialmente si el sistema rechaza siempre clases minoritarias.

### Respuesta 21

Cinco ejemplos: snapshot de fuente, definición de unidad, target versionado, grupos de duplicados, lista de features autorizadas. También son esenciales población y exclusiones, texto curado, reloj temporal, diccionario y propuesta de split. El objetivo es reconstruir cada decisión.

### Respuesta 22

Redacción adecuada: “El notebook del equipo informa una asociación temporal y propone revisar una partición por período. Javier debe reproducir el análisis, verificar qué fecha representa el uso y documentar si el efecto persiste antes de adoptar el split”. La frase conserva autoría, incertidumbre y acción siguiente.

---

## 26. Autoevaluación final

Marcá cada afirmación como **sí**, **todavía no** o **puedo explicarla con un ejemplo SAIJ**.

### Fundamentos

- [ ] Puedo explicar aprendizaje sin usar la palabra “magia”.
- [ ] Distingo patrón predictivo de causalidad y comprensión.
- [ ] Sé formular tarea, experiencia y desempeño.
- [ ] Distingo supervisado, no supervisado y refuerzo.
- [ ] Distingo regresión, binaria, multiclase y multietiqueta.

### Formulación

- [ ] Defino unidad, (X), features y (y).
- [ ] Separo target de salida operacional.
- [ ] Puedo justificar usuario, uso y criterio de éxito.
- [ ] Reconozco límites de un target construido.

### Evaluación

- [ ] Explico train, validación y test sin confundirlos.
- [ ] Elijo split según el futuro.
- [ ] Distingo aleatorio, estratificado, grupal y temporal.
- [ ] Trato baseline como control científico.
- [ ] Diagnostico subajuste y sobreajuste con más de una señal.
- [ ] Distingo pérdida y métrica.

### Métricas

- [ ] Reconstruyo TP, TN, FP y FN.
- [ ] Calculo accuracy, precision, recall y F1 a mano.
- [ ] Interpreto matriz multiclase.
- [ ] Explico macro, micro y weighted.
- [ ] Entiendo por qué macro importa bajo desbalance.
- [ ] Puedo explicar balanced accuracy como contexto opcional.

### Representación y modelos

- [ ] Explico vocabulario, BoW, binario, n-gramas y TF-IDF.
- [ ] Entiendo matrices dispersas y vocabulario desconocido.
- [ ] Aplico fit-on-train a toda transformación aprendida.
- [ ] Explico Bayes y la suposición de Naive Bayes.
- [ ] Explico el cero y el suavizado.
- [ ] Distingo multiclase nativa, OvR y OvO.

### Práctica responsable

- [ ] Diseño un ledger reproducible.
- [ ] Hago análisis por clase, longitud, tiempo, geografía y tipo.
- [ ] Busco shortcuts, drift y fuga.
- [ ] Diseño revisión humana y abstención.
- [ ] Puedo conectar TP2 con entrenamiento sin inventar resultados.

### Criterio de dominio

Considerá dominada la materia cuando puedas tomar un experimento ajeno y preguntar, en este orden:

1. ¿qué problema resolvía?;
2. ¿qué representaba una fila?;
3. ¿cómo se construyó (y)?;
4. ¿qué futuro estimó el split?;
5. ¿qué aprendió el preprocesamiento y dónde?;
6. ¿cuál fue la baseline?;
7. ¿qué métrica y promedio se usaron?;
8. ¿qué clases y subgrupos fallaron?;
9. ¿qué decisión operacional se desprende?;
10. ¿qué todavía no sabemos?

---

## 27. Glosario de Materia 3

| Término | Definición operativa |
|---|---|
| **Abstención** | Decisión de no clasificar automáticamente un caso y derivarlo a revisión. |
| **Accuracy** | Proporción total de predicciones correctas. |
| **Aprendizaje supervisado** | Ajuste de una regla a partir de pares entrada–target. |
| **Bag of Words** | Representación de texto mediante presencia o conteo de términos, sin orden global. |
| **Balanced accuracy** | Promedio del recall por clase; contexto útil bajo desbalance. |
| **Baseline** | Control simple contra el que se evalúa el valor agregado de un modelo. |
| **Calibración** | Correspondencia entre probabilidades predichas y frecuencias observadas. |
| **Capacidad** | Complejidad de patrones que una familia de modelos puede representar. |
| **Clasificación** | Predicción de categorías. |
| **Cross-validation** | Evaluación repetida rotando particiones de entrenamiento y validación. |
| **Dataset supervisado** | Colección de pares ((x_i,y_i)). |
| **Desbalance** | Diferencia marcada entre soportes de clases. |
| **Drift** | Cambio en datos, prevalencias o relación entrada–target a través del tiempo. |
| **Feature** | Variable de entrada disponible y autorizada para predecir. |
| **F1** | Media armónica de precision y recall. |
| **FN** | Positivo real predicho como negativo. |
| **FP** | Negativo real predicho como positivo. |
| **Generalización** | Desempeño transferible a datos nuevos del escenario relevante. |
| **Group-aware split** | Partición que mantiene entidades relacionadas juntas. |
| **Hiperparámetro** | Configuración elegida fuera del ajuste de parámetros. |
| **IDF** | Peso que reduce influencia de términos presentes en muchos documentos de train. |
| **Inferencia** | Aplicación del modelo entrenado a una entrada. |
| **Leakage** | Uso de información no disponible legítimamente durante aprendizaje o selección. |
| **Ledger** | Registro versionado de datos, decisiones, configuración, resultados y conclusión. |
| **Loss** | Función que guía el ajuste del modelo. |
| **Macro** | Promedio que da el mismo peso a cada clase. |
| **Matriz de confusión** | Tabla de clases reales versus predichas. |
| **Métrica** | Medida usada para evaluar según el propósito. |
| **Micro** | Agregación global de decisiones antes de calcular la métrica. |
| **Modelo** | Regla parametrizada o familia usada para producir predicciones. |
| **Multiclase** | Una clase única entre más de dos opciones. |
| **Multietiqueta** | Varias etiquetas simultáneas por caso. |
| **Naive Bayes** | Clasificador probabilístico basado en Bayes e independencia condicional aproximada. |
| **N-grama** | Secuencia contigua de (n) elementos de texto. |
| **OvO** | Estrategia con un clasificador por par de clases. |
| **OvR** | Estrategia con un clasificador por clase contra el resto. |
| **Parámetro** | Valor aprendido durante entrenamiento. |
| **Precision** | Fracción correcta entre predicciones positivas. |
| **Recall** | Fracción detectada entre positivos reales. |
| **Regresión** | Predicción de un valor numérico continuo. |
| **Representación dispersa** | Vector de alta dimensión con mayoría de ceros almacenado eficientemente. |
| **Sesgo inductivo** | Preferencia de una familia por ciertos patrones. |
| **Shortcut** | Señal fácil y potencialmente espuria usada para predecir. |
| **Suavizado** | Ajuste que evita probabilidades cero ante eventos no observados. |
| **Target** | Salida usada como referencia durante entrenamiento. |
| **Temporal split** | Partición que entrena con pasado y evalúa en futuro. |
| **Test** | Conjunto reservado para estimación final. |
| **TF-IDF** | Ponderación por frecuencia local y rareza documental en train. |
| **Threshold** | Umbral que convierte un score o probabilidad en decisión. |
| **Train** | Conjunto usado para ajustar parámetros y transformaciones. |
| **Underfitting** | Incapacidad de capturar señal suficiente. |
| **Validación** | Datos usados para elegir configuración sin tocar test. |
| **Weighted** | Promedio ponderado por soporte de clase. |

---

## 28. Puente hacia Materia 4: del experimento a las familias de modelos

La Materia 3 no termina cuando elegimos una métrica. Su cierre lógico es un **contrato experimental**: sabemos qué representa una fila, cuál es el target, qué información puede usarse, cómo se separan train, validación y test, qué baseline corresponde y qué errores importan. Ese contrato es la pista sobre la que ahora pueden competir distintas familias. Sin él, cambiar de algoritmo sería cambiar de respuesta sin haber fijado la pregunta.

El puente completo queda así:

```text
Curación construye evidencia confiable
  → Introducción a AA diseña el experimento
  → Aprendizaje Supervisado compara reglas de aprendizaje concretas
  → la evidencia, no la moda, decide qué familia merece avanzar
```

La nueva pregunta no es “¿cuál es el mejor modelo en abstracto?”, sino:

> ¿Qué regularidad supone cada familia, qué representación puede aprovechar, cuánto cuesta entrenarla y explicarla, y qué errores produce bajo el mismo protocolo?

Este puente conserva el cierre de la Materia 3: el target, el split, la fuga, el drift y la revisión humana siguen vigentes. Materia 4 agrega vocabulario y criterios para entender **cómo** aprende cada familia y **por qué** dos modelos pueden reaccionar de manera distinta ante los mismos ejemplos.

---

