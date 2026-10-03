# Optativa 2 — AWS Academy Machine Learning Foundations

> **Idea rectora:** en la nube el orden es **problema de negocio → datos fuera de producción → entrenar o invocar → apagar lo que no se usa**. SageMaker y Bedrock son un catálogo. La nota de esta optativa son los **quizzes** de la plataforma, no los labs.

Esta optativa no sustituye el tronco, ni Ética, ni Perez (LLMs), ni Spark. El Consorcio y SAIJ no se aprueban en Canvas. Los apuntes de subtítulos son fuente; las cifras de clase **no se recitan** sin chequeo.

**Contexto de materiales del curso.** Fabián Hanuseski (Craftech). 4 clases, 8 videos FAMAF (28/08–05/09/2026). Labs asincrónicos, repetibles, **sin puntaje**. Forecast se saltea en clase; el cuestionario **igual** cuenta para el certificado.

Cifras **chequeadas** contrastadas con documentación AWS el 02/10/2026.

---

## 0. Cómo estudiar esta optativa

### 0.1 Recorrido didáctico

```text
intuición
  → vocabulario preciso
  → ejemplo inventado trabajado a mano
  → fórmula o regla de decisión
  → interpretación
  → error frecuente
  → checkpoint
  → transferencia hipotética a SAIJ
  → ejercicio conceptual
```

### 0.2 Qué evidencia se distingue

| Rótulo | Significado |
|---|---|
| **Teoría general** | Train/test, umbral, costo de error. |
| **Ejemplo inventado** | Caso chico para razonar; no es un cliente real. |
| **Contexto Academy** | SageMaker, S3, Rekognition, Lex, Bedrock, lo dicho en clase. |
| **Cifra chequeada** | Docs AWS, octubre 2026. |
| **Desactualizado** | Lo dijo el docente y AWS ya lo cambió. |
| **Hipótesis SAIJ / CC** | Analogía; no es lab de Academy. |
| **Decisión pendiente** | La tenés que justificar vos. |

### 0.3 Qué deberías poder hacer al terminar

1. Decir qué entra en la nota (quizzes) y qué no (labs).
2. Formular un problema de ML con métrica de negocio, plazo y online vs batch.
3. Explicar por qué la notebook no se clava a producción.
4. Elegir endpoint vs transformación por lotes.
5. Sacar el umbral del código y relacionarlo con FP/FN.
6. Estimar que cada job de hiperparámetros se paga.
7. Encender Budgets el día uno y apagar endpoints.
8. No planificar sobre Forecast ni Model Monitor si tu cuenta es nueva.
9. Distinguir la política de datos de Bedrock de la de Comprehend.
10. Decir qué es un perfil de inferencia Global (residencia, no “lo más barato”).
11. Tratar un agente como un usuario IAM más.
12. Separar esta entrega de los notebooks de la optativa 3.

### Checkpoint 0

¿Qué parte del curso cuenta para la evaluación? Si contestás “los labs”, paramos acá.

> **Respuesta razonada:** los **quizzes** de la plataforma. Los labs son asincrónicos, repetibles y **sin puntaje**; la idea rectora de la optativa lo dice: la nota son los quizzes, no los labs.

---

## 1. El problema antes de la consola

### Intuición

Si no se puede hacer a mano, no es un proyecto de ML: es un deseo.

### Vocabulario

Métrica de negocio (no solo accuracy). Online vs batch. Experto de dominio. Costo de FP vs FN.

### Ejemplo inventado

Validar certificados médicos. Éxito: 9 de cada 10 bien resueltos. Valor: horas humanas. Un modelo de fraude que bloquea la tarjeta de quien viaja a Europa: FP **caro en reputación**. Un fraude que pasa: FN **caro en plata**.

**Interpretación.** El umbral 0,5 no sabe eso. Lo tenés que escribir vos.

### Regla de decisión

Una línea: qué decide el modelo, quién la usa, métrica, plazo, ¿respuesta ahora o de noche?

### Error frecuente

Empezar por “hagamos SageMaker” porque hay crédito de Academy.

### Checkpoint 1

“Bajar 10% los reclamos en 6 meses.” ¿Online o batch? ¿Qué es un FP caro?

> **Respuesta razonada:** depende de cuándo se necesita la decisión: si el reclamo se clasifica en el momento de la llamada, *online*; si la medición es periódica sobre un lote, *batch*. El plazo “6 meses” es la meta de negocio, no la cadencia. Un FP caro es marcar como problema algo que no lo es cuando esa marca dispara una acción costosa o dañina (en el capítulo: bloquearle la tarjeta a quien viaja a Europa cuesta reputación).

### Hipótesis SAIJ

“Clasificar fuero” no es métrica de negocio. ¿Quién usa la etiqueta y qué pasa si es CIVIL-COMERCIAL cuando era penal?

### Ejercicio

Escribí la línea de problema para un bot de FAQ **sin** nombrar un servicio AWS.

> **Respuesta razonada:** una línea con decisión, usuario, métrica, plazo y modo. Ejemplo: “un bot responde consultas frecuentes en línea; éxito = resolver sin intervención humana ≥ 80 % con TTFT &lt; 2 s, medido en 3 meses”. No hace falta ningún nombre de servicio.

---

## 2. Datos, entrenamiento y apagado

### Intuición

La notebook es un taller. S3 es el depósito. Si el taller se incendia (terminás la instancia), el depósito tiene que seguir.

### Vocabulario

Train / val / test en S3. Endpoint (consulta en línea). Batch transform (volumen sin apuro). Autoscaling con **tope**. Tag de costo.

### Ejemplo inventado

Un CSV de 2 GB en el disco de la notebook. Cerrás el lab: se borró. Si train.parquet está en `s3://proyecto/train/`, reabrís otra instancia y seguís.

### Regla

Endpoint 24/7 para un job que corre a las 2 de la mañana es un error de **producto**. Varias instancias chicas + tope, no una gigante “por las dudas”.

Cada job de búsqueda de hiperparámetros es cómputo que **pagás**. Máximo de jobs en paralelo y totales.

**Desactualizado.** SageMaker **Model Monitor** no acepta clientes nuevos. AWS propone MLflow / Evidently / CloudWatch en *tu* cuenta.

**Cifra chequeada.** Forecast: no para cuentas nuevas. No diseñes el TP sobre Forecast. Capa gratuita de cuentas nuevas ≠ el folleto viejo de “5 GB y 100 000 requests” de S3.

### Error frecuente

Dejar el endpoint de un lab prendido el fin de semana. Umbral *hardcodeado* en el `.py`.

### Checkpoint 2

¿Por qué el umbral va en una variable de entorno y no en el artefacto del modelo?

> **Respuesta razonada:** el umbral es una **decisión de política** (costo de FP vs FN) que cambia sin reentrenar. Si queda hardcodeado en el artefacto, se congela con el modelo; en una variable de entorno se ajusta por despliegue o por negocio sin reempaquetar nada.

### Hipótesis CC

Un índice RAG que no se apaga no es “alta disponibilidad”: es una factura. El pin de snapshot es el equivalente a “esta versión está en S3”.

### Ejercicio

Listá tres recursos que apagarías el viernes a la noche en un lab (nombres de tipo: notebook, endpoint, bucket de logs). No hace falta IDs reales.

> **Respuesta razonada:** la instancia/notebook del lab (terminar), el endpoint de inferencia (dejar de servir) y el bucket o job de logs/transformación por lotes que no corre el fin de semana. El bucket con los datos de train **no** se apaga: el depósito sigue aunque el taller se incendie.

---

## 3. Umbral, matriz y dinero

### Intuición

El modelo tira un puntaje. Vos tirás un corte. El corte es política.

### Ejemplo inventado (2×2)

100 casos, 10 fraudes reales. Umbral alto: 4 fraudes cazados, 1 cliente bloqueado de más. Umbral bajo: 9 fraudes, 20 clientes bloqueados. **Interpretación:** no hay umbral “más ML”. Hay costo de FN vs FP.

### Fórmula (definición)

\[
\mathrm{Precision} = \frac{TP}{TP+FP},\quad \mathrm{Recall} = \frac{TP}{TP+FN}
\]

Elegís el corte mirando **esas** cuentas en la matriz, no el accuracy.

### Error frecuente

Maximizar accuracy con 1% de positivos. El modelo que dice “nunca fraude” acierta 99%.

### Checkpoint 3

En el 2×2 de arriba, ¿qué umbral elegís si un FN vale 10 veces un FP? No hace falta número exacto: el *sentido*.

> **Respuesta razonada:** el sentido es **bajar el umbral**: cazar más fraudes aunque suban los FP, porque cada FN cuesta 10× un FP. Con los números del capítulo: umbral alto = 6 FN + 1 FP (≈61 unidades); umbral bajo = 1 FN + 20 FP (≈30 unidades).

### Hipótesis SAIJ

FN: no recuperás el fallo que el abogado necesitaba. FP: le mostrás un sumario como si fuera la sentencia. El umbral de un ranker es la misma familia de decisión.

### Ejercicio

Dibujá una matriz 2×2 con números redondos y marcá el umbral que preferís para un filtro de spam vs un filtro de cáncer (inventado). ¿Por qué no es el mismo?

> **Respuesta razonada:** en spam, un FP (mail legítimo a la papelera) es molesto pero barato → umbral más alto; un FN (spam que pasa) es tolerable. En cáncer, un FN es carísimo (no detectar la enfermedad) → umbral más bajo, aceptando más FP. El capítulo: el corte es política según costo de FN vs FP, no “más ML”.

---

## 4. APIs de visión y de diálogo

### Intuición

Rekognition y Lex son modelos **ajenos** con precio por llamado. Primero preguntate si una librería local alcanza.

### Vocabulario

Lambda disparada por S3. Lex + Lambda para turnos/reservas. Face Liveness vs “función DNI”.

### Ejemplo inventado

Mil fotos de DNI por mes. **Cifra chequeada:** free tier de Rekognition ≈ **1.000** imágenes/mes **por grupo** de APIs, no 5.000. AnalyzeID está pensado para documentos de EE. UU. Un DNI argentino no tiene un botón mágico.

**Cifra chequeada.** Kinesis Video Streams: retención por defecto **0** (casi no persiste). “Una o dos horas” de clase **no**.

### Error frecuente

Mandar cada frame a Rekognition “porque es ML”. Chatbot transaccional de alto volumen arrancando por un LLM de 70B.

### Checkpoint 4

Lex primero o Bedrock primero para “reservar un turno a las 15”. Una frase.

> **Respuesta razonada:** **Lex primero**: es el servicio de diálogo transaccional (turnos/reservas, con Lambda); un LLM de 70B para un flujo cerrado es caro y frágil. El capítulo: chatbot transaccional de alto volumen no arranca por un LLM de 70B.

### Hipótesis SAIJ

OCR de un PDF de fallo no es “el fuero”. Es un paso de ingesta, como Rekognition es un paso de etiquetas.

### Ejercicio

Escribí un flujo de tres cajas: objeto entra a S3 → ¿qué se dispara? → ¿dónde se guarda la etiqueta? Sin nombres de cuenta.

> **Respuesta razonada:** objeto en S3 → evento dispara **Lambda** → Lambda llama a la API de visión (p. ej. Rekognition) → la etiqueta se guarda como metadata del objeto o en una base. El capítulo: Lambda disparada por S3; el OCR es un paso de ingesta, no “el fuero”.

---

## 5. Bedrock: el mismo token, otra factura

### Intuición

La optativa 3 te enseña qué es un token. Esta te enseña **quién lo cobra y si se entrena con tu texto**.

### Vocabulario

Converse vs InvokeModel. Guardrail. Perfil de inferencia (región / Global). Knowledge base. Agente = principal IAM.

### Ejemplo inventado y reglas chequeadas

Un banco que no puede salir del país. **Cifra chequeada:** el perfil **Global** no es “la región más barata”. La inferencia entre regiones es **capacidad**; el pedido puede **procesarse en otra región**. Global ≈ un 10% de ahorro según AWS. Para residencia: **no** Global; SCP/IAM.

**Cifra chequeada.** Bedrock **no** usa tus prompts para entrenar ni se los muestra al proveedor del modelo. **Comprehend** *puede* guardar contenido para mejorar *sus* modelos. La advertencia del docente aplica a **algunos** servicios y a apps de consumo, no a “AWS entero”.

Prompt caching en Bedrock: la **lectura** de caché se cobra con **descuento**, no “como si no cachearas”.

Guardrails: niveles NONE–HIGH, entrada y salida por separado. **No** evalúan argumentos ni resultados de tools. En streaming a veces **no** enmascaran PII. Probar frases en rioplatense.

API **Converse**: cambiar de modelo sin reescribir el cliente.

RAG en Bedrock: set de preguntas reales y job de evaluación **antes** de casarte con un embedding. Vector store: S3 Vectors (barato, poco frecuente), OpenSearch (latencia), Aurora pgvector (si ya hay Postgres).

### Error frecuente

“Los datos nunca salen de AWS, entonces puedo pegar el padrón.” Política **por servicio**. Agente con `*` en IAM.

### Checkpoint 5

Un banco argentino, dato no puede salir. ¿Converse + perfil US Cross-Region? Sí/no y por qué.

> **Respuesta razonada:** **no**: el perfil Global/Cross-Region no es residencia de datos; el pedido puede procesarse en otra región (es capacidad, no “la región más barata”). Para que el dato no salga se usan regiones concretas + SCP/IAM, no el perfil Global.

### Hipótesis SAIJ / CC

Tier **gratis** de Gemini (optativa 3) usa contenido para mejorar productos. Bedrock no, en la política citada. Elegir API es elegir **contrato de datos**, no solo precio. El fallo con nombres y el padrón del consorcio no van a un tier que reentrena.

### Ejercicio

Tabla de tres filas: Bedrock, Comprehend, un chatbot de consumo. Columna: “¿pueden usar mi texto para entrenar?”. Completala con sí/no/depende **sin** inventar un cuarto servicio.

> **Respuesta razonada:** Bedrock → **no** (política citada: no usa tus prompts para entrenar ni se los muestra al proveedor). Comprehend → **sí/puede** (puede guardar contenido para mejorar sus modelos). Chatbot de consumo → **depende** (muchos tiers gratis usan el contenido para mejorar productos; es el contraste de la Hipótesis SAIJ/CC).

---

## 6. Relación con las otras optativas

| | Esta (2) | Perez (3) | Spark (4) |
|---|---|---|---|
| Entrega | Quizzes | Notebooks Colab | Ejercicios en Zeppelin |
| Unidad | Servicio y factura | Token, prompt, RAG, juez | Partición y shuffle |
| Error típico | Recurso prendido / política mal leída | Alucinación / nota vs norma | Mover datos de más |

No mezcles entregas. Guardrail de Bedrock ≠ contrato de fundamentación de Vertex; los dos cortan disparates en **capas distintas**.

### Checkpoint 6

¿Dónde se aprueba *esta* materia? Una palabra.

> **Respuesta razonada:** **Canvas** (los quizzes de la plataforma). Ni los labs, ni el Consorcio, ni SAIJ.

### Transferencia (decisión pendiente)

Aplicar SageMaker al JSONL de SAIJ o Bedrock al canal es **otro** proyecto, después de los quizzes. No es el certificado de Academy.
