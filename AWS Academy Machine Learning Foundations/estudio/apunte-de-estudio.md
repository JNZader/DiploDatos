# Apunte de estudio: AWS Academy Machine Learning Foundations (FAMAF UNC, Fabián Hanuseski)

**Curso:** AWS Academy Machine Learning Foundations, dictado dentro de la diplomatura de FAMAF (UNC) · Docente: Fabián "Hanu" Hanuseski, CTO de Craftech (partner de AWS en Córdoba) · Formato: 4 clases de unas 4 horas, grabadas en 8 videos no listados del canal de FAMAF.
**De qué va:** el curso recorre los fundamentos de machine learning en AWS siguiendo los módulos de la plataforma de AWS Academy: introducción al ML, implementación con SageMaker (con la mayoría de los labs), Forecast (que el docente saltea), visión por computadora con Rekognition y procesamiento de lenguaje natural con Lex, Polly, Transcribe, Translate y Comprehend. Las últimas dos clases suman material extra que no está en la plataforma: IA generativa, Bedrock, guardrails, RAG con knowledge bases y agentes.

> Nota: este apunte sale de los subtítulos automáticos en español de los 8 videos, que no tienen capítulos ni descripción. Muchos nombres de servicios y modelos vienen deformados (ver el glosario al final). Todo lo que figura acá es lo que se dice en clase; las cifras, fechas y afirmaciones que pueden haber cambiado están marcadas como **para verificar** y todavía no las chequeé contra la documentación de AWS.

**Cómo leer los links:** cada link dice la clase, la parte y el minuto. Por ejemplo, "C2P1 1:23:45" es la clase 2, parte 1, en la hora 1, minuto 23, segundo 45.

## Los 8 videos en orden

| # | Id | Clase | Parte | Duración | Link |
|---|---|---|---|---|---|
| 1 | — | Clase 1 (28/08/2026, tarde) | Parte 1 | 1:56:16 |  |
| 2 | — | Clase 1 | Parte 2 | 1:51:07 |  |
| 3 | — | Clase 2 (29/08/2026, mañana) | Parte 1 (el título dice solo "Clase 2") | 1:58:08 |  |
| 4 | — | Clase 2 | Parte 2 | 1:43:12 |  |
| 5 | — | Clase 3 (04/09/2026, tarde) | Parte 1 | 2:13:51 |  |
| 6 | — | Clase 3 | Parte 2 (se habla hasta el 47:09, el resto es silencio) | 1:10:31 |  |
| 7 | — | Clase 4 (05/09/2026, mañana) | Parte 1 | 1:56:14 |  |
| 8 | — | Clase 4 | Parte 2 | 1:47:25 |  |

## Mapa de módulos y clases

| Módulo o bloque | Dónde se ve | Lab |
|---|---|---|
| 0. Cómo funciona el curso (plataforma, evaluación, labs) | C1P1 y C1P2 | No |
| Módulo 1. Introducción a la plataforma | El docente lo saltea | No |
| Módulo 2. Introducción al machine learning | C1P1 | Recorrido por la consola de SageMaker |
| Módulo 3. Implementación de ML con SageMaker | C1P1 (final), C1P2, C2P1, C2P2 (inicio) | Labs 3.1 a 3.7 |
| Costos de ML en AWS (dentro del módulo 3) | C2P2 | No |
| Módulo 4. Forecast | C2P2, salteado por deprecado | No |
| Módulo 5. Visión por computadora | C2P2, C3P1 (repaso) | Colección de caras con Rekognition |
| Módulo 6. Procesamiento de lenguaje natural | C3P1 | Chatbot con Lex, Lambda, S3 y Cognito |
| Extra A. IA generativa, Amazon Q y Kiro | C3P2 | Demo de Kiro |
| Extra B. Bedrock en profundidad | C4P1 | Demo con boto3 |
| Extra C. Bases vectoriales, RAG, datos y agentes | C4P1 (final), C4P2 | Demo de agente con knowledge base |
| Cierre. Preguntas sobre el mercado laboral | C4P2 | No |

---

## 0. Cómo funciona el curso

**Dónde:** C1P1 0:02, C1P1 2:16, C1P1 2:49, C1P1 3:56, C1P1 5:35, C1P1 1:15:31, C1P1 1:17:08, C1P1 1:19:53, C1P1 1:31:20, C1P2 0:34, C1P2 2:16, C1P2 1:27:15, C3P1 0:02

**Conceptos clave.**
- El curso es de AWS Academy y se accede con una invitación por mail que crea un usuario en Canvas. El docente saltea el módulo de introducción a la plataforma y pasa rápido por el módulo 2.
- Son 4 clases de 4 horas (16 horas en total). En cada clase hay unas 2 horas de módulos, un break y los módulos siguientes.
- Casi todos los módulos tienen un lab guiado. La guía dice 30 a 45 minutos (algunos 1 hora), pero el entorno del lab queda vivo unas 3 horas. Los labs son asincrónicos y se pueden repetir todas las veces que quieras.
- Cada módulo tiene en la plataforma una presentación y un video en inglés con subtítulos. El docente comparte además un Drive con los labs resueltos, traducidos y comentados línea por línea, y un Slack del curso.

**Cómo se evalúa (pistas para el examen).**
- La única evaluación son los cuestionarios de opción múltiple al final de cada módulo. No hay penalidad por adivinar y se pueden repetir todas las veces que quieras (C1P1 1:15:31, C1P2 1:28:46).
- Los labs no son parte de la evaluación (C1P1 1:18:15, C1P2 1:03:32), pero el docente insiste en hacerlos porque es donde se juega con la consola.
- Para el certificado hay que hacer sí o sí el cuestionario. Según el docente cada uno lleva unos 20 minutos y con una hora deberías liquidar todos; recomienda hacerlos a medida que avanzás para no olvidarte (C1P2 1:27:15).
- El módulo 3 tiene su examen (C1P2 1:04:05). El módulo 4 (Forecast) no se ve en clase, pero el cuestionario igual hay que hacerlo para el certificado (C2P2 24:46).
- El certificado se puede publicar en LinkedIn desde la plataforma (C1P1 1:17:41).

**Advertencias.**
- La plataforma queda abierta "hasta el 31 de noviembre" según dice en la clase 1, fecha que no existe (**para verificar** la fecha real) (C1P1 1:17:08). También dice que Amazon no deja extender más de 4 meses (C1P1 1:19:53). En la clase 3 aclara que la coordinación pide tener los exámenes alrededor del 28 de septiembre y que se puede extender unas semanas (C3P1 0:02).
- El botón Start Lab puede tardar 10 a 20 minutos en preparar la cuenta, y los labs 6 o 7 tardan más porque crean infraestructura. Recomienda darle Start Lab antes de empezar a leer el módulo (C1P2 0:34, C1P2 1:08, C1P2 1:43).
- End Lab no cambia la nota; solo apaga la cuenta del lab, que igual se apaga sola (C1P2 2:16).
- Usá Chrome o, si no, Firefox. Safari o un Edge viejo se pueden colgar (C1P2 4:07).

<details>
<summary>Preguntas de repaso del bloque 0 (con respuestas)</summary>

1. **¿Qué parte del curso cuenta para la evaluación?** Solo los cuestionarios de opción múltiple de cada módulo; los labs no se califican.
2. **¿Conviene dejar en blanco una pregunta que no sabés?** No, porque no hay penalidad por adivinar y el cuestionario se puede repetir.
3. **¿Qué hace el botón End Lab?** Apaga la cuenta del lab; no cambia la nota.
4. **¿Por qué conviene apretar Start Lab antes de leer el módulo?** Porque preparar el entorno puede tardar 10 a 20 minutos, y más en los labs que crean infraestructura.
5. **¿Hay que hacer el cuestionario del módulo 4 aunque no se vea en clase?** Sí, es necesario para el certificado.

</details>

---

## Módulo 2. Introducción al machine learning

**Dónde:** C1P1 14:45, C1P1 15:49, C1P1 16:56, C1P1 19:38, C1P1 30:31, C1P1 39:14, C1P1 41:24, C1P1 47:25, C1P1 50:47, C1P1 58:47, C1P1 1:02:35, C1P1 1:03:40, C1P1 1:10:59

### Conceptos clave
- **Jerarquía de términos.** La inteligencia artificial contiene al machine learning, que contiene al deep learning, que contiene a la IA generativa. El boom masivo de la generativa lo ubica con GPT 3.5 en 2022 ("si no me equivoco, 2023", **para verificar** la fecha que quiso decir) (C1P1 15:49).
- **El dato es la materia prima.** Con datos de mala calidad vas a tener malas predicciones. Cuenta que muchos clientes quieren ML sin tener datos (C1P1 16:56).
- **On premise contra nube.** En la nube alquilás cómputo y escalás. SageMaker permite entrenar con volúmenes enormes y levantar mil servidores "siempre que lo puedas pagar" (C1P1 19:38, C1P1 20:38).
- **Cuánto cuesta.** Depende; hay que hacer una simulación con la calculadora. Para empresas como Netflix la velocidad de decisión importa más que el costo; en fraude con tarjetas el modelo tiene que responder en microsegundos y aguantar picos como diciembre (C1P1 21:47, C1P1 23:59).
- **No uses una bazuca para matar una hormiga.** Para un modelo de 50 MB no hace falta SageMaker: corrélo local en un Jupyter (C1P1 25:03). Los modelos chicos están en todos lados (lavarropas, heladeras, motores de fraude que tienen que responder rápido) (C1P1 27:47, C1P1 29:25).
- **Tipos de aprendizaje** (C1P1 30:31):
  - Supervisado: ejemplos de patentes y radiografías de covid (C1P1 31:03, C1P1 32:38).
  - No supervisado: clustering, por ejemplo churn en Shell para dar descuentos solo a quien no consume seguido (C1P1 33:46).
  - Por refuerzo: prueba y error con recompensa, como Amazon DeepRacer y los vehículos autónomos (C1P1 41:24).
- **Lenguaje natural y modelos fundacionales.** Los modelos preentrenados son probabilísticos: a la misma pregunta dan una respuesta parecida, no igual (C1P1 37:02). Los fundacionales son generalistas ("el que mucho abarca poco aprieta"), lentos, costosos y grandes. Por eso siguen existiendo modelos chicos y específicos, que suelen ser más precisos para su tarea (C1P1 39:14, C1P1 40:21).

### El proceso de ML según la clase
1. **Formular el problema** a partir de una necesidad real, no por FOMO (C1P1 47:25).
2. **Limpiar los datos**, por ejemplo nombre y apellido mezclados con "señora", sexo inconsistente o fechas con día y mes invertidos (C1P1 47:57).
3. **Separar roles:** el data engineer entrega datos sanitizados y el data scientist trabaja el modelo (C1P1 50:47).
4. **Codificar** variables categóricas (por ejemplo a 0 y 1) (C1P1 51:51).
5. **Dividir** en entrenamiento y prueba (C1P1 52:26).
6. **Evitar sobreajuste e infraajuste** buscando el equilibrio; "todo esto va a estar en Amazon" (C1P1 52:58).
7. **Desplegar:** disponibilizar el modelo para que, por ejemplo, marketing lo use, en lugar de pasarle la notebook (C1P1 53:30).

### Herramientas y servicios de AWS que nombra
| Servicio | Para qué sirve según la clase |
|---|---|
| Jupyter (dentro de SageMaker) | Notebooks como Colab; pandas y librerías open source (C1P1 56:29) |
| Instancias | Servidores; el tipo C es de cómputo; hay CPU y GPU (C1P1 58:47, C1P1 59:19) |
| Amazon Q | Asistente para preguntar, por ejemplo, cuál es el mejor cómputo (C1P1 59:50) |
| AWS Marketplace para SageMaker | Modelos preentrenados gratis o pagos (OCR, rostros, mascotas) que podés extender o ajustar; también podés publicar y cobrar tu modelo (C1P1 1:02:35, C1P1 1:14:44) |
| — | Reconocimiento de imágenes y caras, por ejemplo ingreso a edificios (C1P1 1:03:40, C1P1 1:05:25) |
| Textract | OCR que distingue, por ejemplo, una factura de la foto de un perro (C1P1 1:06:28) |
| Polly | Texto a voz (C1P1 1:07:34) |
| Transcribe | Voz a texto; en call centers sirve para detectar patrones, palabras ofensivas o una conversación caliente (C1P1 1:07:34, C1P1 1:08:06) |
| Comprehend | Comprensión de texto (no multimodal), barato a escala (C1P1 1:08:38) |
| Translate | Traducción (C1P1 1:09:12) |
| Lex | Chatbots (C1P1 1:09:12) |
| Forecast | Pronósticos (C1P1 1:09:44) |

Cuenta que cada llamada a OpenAI sale "unos 5 centavos de dólar" frente a un modelo chico propio (**para verificar**) (C1P1 1:04:49). También menciona servicios de recomendaciones sin que el nombre se entienda en la transcripción (C1P1 1:10:18).

### Desafíos del ML
Datos no representativos o insuficientes, sobreajuste, operacionalizar el modelo, hacerle las preguntas correctas al cliente, el clásico "es muy caro, lo dejo para otro momento", privacidad, elegir la herramienta y disponibilizar el modelo (C1P1 1:10:59 a C1P1 1:14:14).

<details>
<summary>Preguntas de repaso del módulo 2 (con respuestas)</summary>

1. **Ordená de más general a más específico: deep learning, IA, IA generativa, machine learning.** IA, machine learning, deep learning, IA generativa.
2. **¿Por qué no conviene usar SageMaker para un modelo de 50 MB?** Porque es matar una hormiga con una bazuca; ese modelo se puede correr local.
3. **¿Qué tipo de aprendizaje usa DeepRacer?** Aprendizaje por refuerzo, con prueba, error y recompensa.
4. **Un modelo que agrupa clientes según su consumo para detectar churn, ¿qué tipo de aprendizaje es?** No supervisado (clustering).
5. **¿Por qué siguen existiendo modelos chicos si hay modelos fundacionales?** Porque los fundacionales son generalistas, lentos, grandes y caros, y un modelo chico suele ser más preciso y barato para una tarea concreta.
6. **¿Qué servicio usarías para pasar texto a voz y cuál para voz a texto?** Polly para texto a voz y Transcribe para voz a texto.
7. **¿Qué significa desplegar un modelo según la clase?** Disponibilizarlo para que otra área lo use, no entregarle la notebook.

</details>

---

## Módulo 3. Implementación de ML con SageMaker

Es el módulo más grande y el que tiene más labs. Los labs son "evolutivos": el mismo modelo va creciendo de un lab al siguiente (C1P1 1:20:26, C1P1 14:45). Los labs 3.1 a 3.4 los hace con la clase; desde el 3.5 los alumnos siguen solos, "que se tropiecen" (C1P2 0:02, C2P1 0:04).

### 3.1 Formular el problema
**Dónde:** C1P1 1:20:58, C1P1 1:22:02, C1P1 1:24:47, C1P1 1:26:24, C1P1 1:27:28, C1P1 1:28:00

- El ejemplo es un cliente que recibe certificados médicos y tiene que validar la matrícula. El éxito se mide, por ejemplo, con 9 de cada 10 bien resueltos, y el valor es el tiempo humano que se ahorra (C1P1 1:20:58, C1P1 1:22:02, C1P1 1:22:37).
- Hace falta un experto de dominio (C1P1 1:24:15, C1P1 1:38:01).
- Preguntas a hacerse: si es un problema de ML o no, si es supervisado, cuál es el rendimiento mínimo y si hace falta tiempo real o alcanza con un proceso nocturno (C1P1 1:24:47, C1P1 1:25:19, C1P1 1:25:51).
- Regla práctica: el problema tiene que poder resolverse manualmente primero (C1P1 1:26:24).
- Definí un objetivo de negocio medible, como bajar 10% los reclamos (C1P1 1:27:28). Un modelo de fraude demasiado agresivo genera mala experiencia, como bloquearle la tarjeta a alguien que viaja a Europa (C1P1 1:28:00).

### 3.2 Recolectar, guardar y preparar datos
**Dónde:** C1P1 1:29:06, C1P1 1:33:41, C1P1 1:34:13, C1P1 1:35:15, C1P1 1:39:06, C1P1 1:43:21, C1P1 1:46:06

- Hay repositorios públicos de datasets (vinos, salud, autos) que se importan desde Python; la clase no dice el nombre del repositorio (C1P1 1:29:06). También hay fuentes públicas como el SMN, el censo o sismos (C1P1 1:35:48).
- Preguntas de recolección: qué datos, cuántos, dónde están y cómo llegan (C1P1 1:33:41). S3 centraliza los datos (C1P1 1:34:13).
- "Un buen data scientist nunca debería recibir datos crudos": los datos llegan ofuscados (el ejemplo es Shell) y preparados por el data engineer (C1P1 1:34:44, C1P1 1:35:15).
- Para muestrear en producción no hay que afectar la operación (C1P1 1:38:34).

**Servicios de almacenamiento y datos que repasa** (C1P1 1:39:06 a C1P1 1:47:13):

| Servicio | Para qué sirve según la clase |
|---|---|
| S3 (Simple Storage Service) | Almacenamiento de objetos, "como un Drive"; el servicio que más vas a usar |
| FSx | Disco de red para Windows o Linux |
| EFS | Sistema de archivos compartido |
| RDS | Bases relacionales |
| Redshift | Data warehouse (lo usa Naranja X) |
| "Regi" (nombre dudoso) | Un servicio para millones de operaciones en milisegundos; no se entiende cuál es |
| "Timestam" (probablemente Timestream, dudoso) | Streaming en tiempo real para IoT o aerolíneas |
| Glue | Lee las fuentes, arma un catálogo y un pipeline; la notebook le pega a Glue sin conectores |
| IAM | Define quién accede a qué; SageMaker tiene que poder leer el bucket (C1P1 1:50:36, C1P1 1:51:39) |
| CloudTrail | Auditor de logs de la cuenta (C1P1 1:54:56) |

- El ETL lo hace el data engineer, combinando por ejemplo transacciones y CRM (C1P1 1:43:21, C1P1 1:43:55).
- En S3 hay clases de almacenamiento: backup barato con pocas lecturas contra acceso frecuente más caro, y automatizaciones de borrado (C1P1 1:53:15, C1P1 1:53:49).
- S3 viene cifrado por defecto y "ya no podés elegir no encriptar"; RDS también se cifra (**para verificar**) (C1P1 1:54:22).
- En la demo del final de C1P1 muestra cómo se suben los archivos del ZIP extraído a S3 con la librería Python de AWS, con un for por archivo. Aclara que ahora el ZIP viene precargado (C1P1 1:48:21, C1P1 1:49:30).

### 3.3 Lab 3.1: crear la notebook de SageMaker
**Dónde:** C1P2 0:34, C1P2 2:51, C1P2 5:44, C1P2 6:48, C1P2 8:26, C1P2 12:16, C1P2 12:49, C1P2 15:35, C1P2 16:07, C1P2 19:27, C1P2 22:12, C1P2 37:47, C1P2 39:59

Pasos tal como los muestra en clase:
1. Apretá **Start Lab** y esperá a que esté listo (C1P2 0:34).
2. Apretá el botón **AWS** para abrir la consola (C1P2 2:51).
3. Fijate la región. El link del lab te lleva a us-east-1 (C1P2 10:05).
4. Opcional: poné la consola en inglés. Él lo recomienda porque la traducción es literal (notebook queda "libreta", pipeline "canalización", bucket "cubo") (C1P2 6:48).
5. Buscá **Amazon SageMaker AI**. Vas a ver la diferencia entre SageMaker Unified Studio y la consola tradicional, y las capturas del lab pueden tener otros colores (C1P2 8:26, C1P2 8:59, C1P2 9:32).
6. Creá la notebook instance con el **nombre exacto que da el lab**, copiado y pegado, porque los permisos de IAM están asociados a ese nombre y distinguen mayúsculas (C1P2 12:16).
7. Tipo de instancia **ml.m5.xlarge** (C1P2 12:49).
8. Plataforma **notebook-al2023-v1** (C1P2 15:35).
9. Lifecycle configuration **ml-pipeline**, un script que configura Jupyter al arrancar y que en una empresa arma DevOps o MLOps (C1P2 16:07, C1P2 18:22).
10. Creá la notebook y esperá de 2 a 5 minutos hasta que aparezca **Open JupyterLab** (C1P2 19:27, C1P2 22:12).
11. En Jupyter, usá el kernel de Python 3, importá `sagemaker` y obtené el rol de IAM (C1P2 37:47, C1P2 38:20).
12. El ejemplo usa el algoritmo **Linear Learner**: convierte los datos a float32, los sube a S3, entrena con la URL del bucket y al final hostea el modelo (C1P2 39:59, C1P2 41:12, C1P2 41:46).

Advertencias del lab:
- A él le falló un permiso para crear un bucket y dice que "puede pasar"; este lab solo te pasea por la consola, así que si tira error no pasa nada (C1P2 38:50, C1P2 42:57).
- La notebook puede no ser igual a la guía porque la actualizan (C1P2 22:44).
- CloudShell no se usa en estos labs (C1P2 23:19).

**Tipos de instancia.** La línea M5 es "buena en todo, excelente en nada" y tiene buen precio; la línea P tiene GPU y es carísima. Si la CPU anda al 90%, el dataset o la notebook son muy grandes y conviene una instancia mayor (C1P2 13:22, C1P2 15:03, C1P2 21:40).

**Colab contra SageMaker.** Colab es un playground integrado con Google; SageMaker da más control sobre servidores, región y sistema operativo (C1P2 10:38). En C2P1 agrega que la abstracción de Colab tiene un costo y que SageMaker, al ser ajustable, sale más económico a la larga (C2P1 43:28, C2P1 44:02).

### 3.4 Lab 3.2: exploración de datos
**Dónde:** C1P2 46:14, C1P2 48:23, C1P2 50:15, C1P2 54:13, C1P2 57:19

1. Cerrá sesión en la consola anterior y volvé a abrir AWS desde el lab nuevo. No toques la instancia del lab anterior: se cierra sola y es otra cuenta (C1P2 48:23, C1P2 49:35).
2. La ruedita que gira es CloudFormation creando la cuenta del lab y su bucket. En este lab la instancia la crea el lab; en la práctica la crea alguien de infraestructura (C1P2 50:15, C1P2 51:24, C1P2 52:33).
3. El dataset es de ortopedia: anomalías en pacientes, como hernia de disco y espondilolistesis (C1P2 54:13).
4. Si una librería falta o está vieja, agregá una celda con `!pip install scipy` (o lo que pida) y volvé a correr (C1P2 57:19, C1P2 59:32).
5. Explorá con pandas: separador del CSV, estadísticas con `describe` y matriz de correlación (C1P2 44:03, C1P2 45:42, C1P2 46:14).

Advertencia: "las librerías quedan viejas muy rápido" y los labs quedan desactualizados (C1P2 55:51, C1P2 58:58). Lo importante no es la notebook sino jugar con Amazon y la consola (C1P2 1:02:25).

### 3.5 Lab 3.3: ingeniería de características
**Dónde:** C1P2 1:04:36, C1P2 1:05:10, C1P2 1:06:20, C1P2 1:07:25, C1P2 1:07:57, C1P2 1:15:34

- Seleccioná características y filtrá datos incorrectos (C1P2 1:04:36).
- Pasá valores ordinales (bajo, medio, alto, muy alto) a números del 1 al 4 (C1P2 1:05:10).
- Ante datos faltantes, decidí por qué faltan antes de borrarlos (C1P2 1:05:43, C1P2 1:06:20). Revisá outliers (C1P2 1:07:25).
- Pasos del lab: importar el CSV, definir los nombres de columna porque no trae encabezado, mirar `shape` y `head`, y transformar los ordinales (C1P2 1:15:34, C1P2 1:16:38).
- Si la sesión queda en caché, cerrá sesión y volvé a entrar (C1P2 1:10:00).

### 3.6 Lab 3.4: entrenamiento
**Dónde:** C1P2 1:17:48, C1P2 1:19:23, C1P2 1:21:36, C1P2 1:22:07, C1P2 1:22:42, C1P2 1:29:51, C1P2 1:35:06

- Formatos de entrenamiento: CSV, JSON y protobuf RecordIO (C1P2 1:17:48).
- El data engineer deja cada noche un CSV en un bucket. No te conectes a producción desde la notebook: dejar credenciales ahí es inseguro y corrés el riesgo de hacer un update o un delete sobre datos productivos (C1P2 1:18:19, C1P2 1:19:23, C1P2 1:20:28).
- Dividí los datos y usá un set reducido para la primera evaluación (C1P2 1:21:36).
- SageMaker tiene algoritmos integrados como k-means y XGBoost. Dice que la lista que muestra "es de 204" y que hay algoritmos nuevos (**para verificar**; probablemente quiso decir 2024) (C1P2 1:22:07). Son algoritmos propios de SageMaker, no de scikit-learn, aunque podés importar tu librería (C1P2 1:29:51, C1P2 1:30:58).
- El resultado del entrenamiento queda en el bucket de S3. "El pan de cada día" es SageMaker con S3, con train, test y validación en S3 (C1P2 1:35:06, C1P2 1:35:42).
- Es el último lab guiado (C1P2 1:22:42).

**Apagá lo que no usás.** Borrá la instancia cuando nadie la use: la notebook va a GitHub y los resultados quedan en S3, así que podés destruirla sin problema (C1P2 1:36:49, C1P2 1:37:56, C1P2 1:39:31).

**Arquitectura de referencia** (C1P2 1:40:03 a C1P2 1:49:27): las bases de la empresa (facturación, finanzas, compras) van a S3, Glue arma el catálogo, SageMaker entrena, el modelo queda en un bucket y un servidor de producción lo carga. En una transacción con tarjeta, el servidor consulta el modelo para decidir si es fraude. Producción pregunta todos los días cuál es la última versión del modelo, que se guarda con un prefijo de fecha como 20260809. Dice que los bancos de Córdoba usan esta arquitectura porque separa roles y cada servicio escala por separado.

### 3.7 Lab 3.5: desplegar el modelo (endpoint o batch transform)
**Dónde:** C2P1 0:35, C2P1 12:11, C2P1 14:27, C2P1 14:58, C2P1 16:02, C2P1 18:14, C2P1 19:19, C2P1 21:13, C2P1 21:45, C2P1 22:48, C2P1 47:19, C2P1 48:25, C2P1 1:12:03

**Conceptos.**
- Hay dos opciones: el **alojamiento de SageMaker** (hosting administrado, un endpoint) o la **transformación por lotes** (batch transform). El modelo se expone como una API (C2P1 0:35).
- Explica qué es una API con ejemplos de clima, dólar y noticias que devuelven JSON (C2P1 1:06). Los agentes de IA también usan APIs si les declarás qué hacen (C2P1 9:25).
- La forma clásica es un servidor con el modelo y FastAPI; a gran escala se usa SageMaker (C2P1 12:11).
- El deploy se hace con un comando que recibe el tipo de instancia. Normalmente lo implementa un ML developer o DevOps (C2P1 14:27, C2P1 14:58).
- Si responde lento, subí de tamaño (medium, large, xlarge) o de familia (T, M, G, P). Se pueden testear varias en paralelo antes de producción (C2P1 15:29).
- `initial_instance_count` controla el escalamiento. Muchas instancias chicas cuestan lo mismo que una grande, pero escalan horizontalmente y se prenden y apagan según la demanda (pocos usuarios a las 2 de la mañana, 20 servidores a las 5 de la tarde) (C2P1 16:02, C2P1 17:08).
- SageMaker monitorea logs y CPU, manda alertas por mail y puede autoescalar al 80%. Ponele un tope porque "la billetera no es infinita" (C2P1 18:14, C2P1 18:47).

**Pasos del lab.**
1. Abrí el lab siguiente con tiempo, porque cada uno tarda en arrancar (C2P1 27:18).
2. Si usás la notebook resuelta del Drive, cambiá el nombre del bucket, porque es dinámico y cambia en cada cuenta (C2P1 21:13).
3. Instalá scipy y scikit-learn si lo pide (C2P1 34:20).
4. Creá el endpoint. Tarda, sobre todo al alojar el modelo; Jupyter muestra un asterisco mientras corre (C2P1 31:06, C2P1 36:19).
5. Invocá el predictor por HTTPS con la región y el nombre del endpoint. Él agregó código para obtener el endpoint y armar la URL con boto3 (C2P1 37:27, C2P1 47:19).
6. Probá la transformación por lotes con el modelo entrenado (C2P1 22:48).
7. Borrá el endpoint al final (C2P1 21:45, C2P1 1:02:08).

**Advertencias.**
- Como mínimo deberías llegar a levantar el endpoint (C2P1 24:04). El endpoint no queda accesible desde afuera sin más arquitectura (C2P1 24:37).
- En una empresa lo común es no borrar el endpoint y escalarlo. Si lo borrás deja de estar hosteado, pero el archivo del modelo sigue en S3 (C2P1 48:25, C2P1 48:59, C2P1 49:31).
- Lotes contra API: los lotes sirven para no correr todo de una tirada, y una transformación en lote enorme tarda (C2P1 1:12:03).
- La notebook del lab mezcla limpieza y ETL con el modelo; en la práctica deberías consumir un CSV ya preparado (C2P1 45:38).
- Dice que SageMaker tiene unos 8 años y fue el primer servicio de ML en la nube (**para verificar**) (C2P1 42:42).

**Costos de S3 que menciona** (C2P1 50:03, C2P1 50:38, C2P1 52:16): se paga por almacenamiento y por request. Dice que la capa gratuita es de "5 GB y 100.000 requests", que al principio hay "200 de crédito" y que el TB sale unos 23,55 USD (**todo para verificar**). En la clase 4 da otras cifras ("20 centavos por giga" en C4P1 1:46:28 y "2 pesos con 50" en C4P2 1:00:18), así que conviene chequear el precio real. También cuenta que S3 se puede usar como tabla con consultas SQL (S3 Tables) y disparar un evento cuando llega un archivo, por ejemplo para reentrenar (C2P1 53:23, C2P1 53:56).

### 3.8 Lab 3.6: evaluación y umbral
**Dónde:** C2P1 59:05, C2P1 1:00:11, C2P1 1:20:53, C2P1 1:22:58, C2P1 1:23:31, C2P1 1:32:58, C2P1 1:34:32, C2P1 1:38:25, C2P1 1:41:41

- La métrica de éxito del ejemplo es reducir 10% los reclamos de fraude en 6 meses. Si el proyecto no resuelve un problema real, muere (C2P1 59:05, C2P1 59:38).
- Matriz de confusión (gato o no gato), sensibilidad y curva ROC (C2P1 1:00:11, C2P1 1:00:42).
- **Umbral (threshold):** es el valor que convierte la probabilidad en 0 o 1. El lab usa 0,3 para clasificar normal o anormal (C2P1 1:22:58, C2P1 1:38:25).
- **Ejercicio que propone:** probá 0,25 y 0,75 y mirá cómo cambian las métricas (C2P1 1:34:32). La línea roja punteada de la ROC es el threshold (C2P1 1:32:58). Con valores extremos del umbral puede aparecer un error en las curvas ROC (C2P1 1:29:46).
- En producción tenés que definir un umbral: podés arrancar en 0,25 y después subir a 0,7 u 0,8, cuidando que "no se te dispare". En fraude, el nivel de confianza depende del negocio (C2P1 1:38:25, C2P1 1:40:37, C2P1 1:41:41).
- En la práctica el umbral va en una variable de entorno o en una base de parametría consultada por URL, para cambiarlo en tiempo real sin redesplegar. Lo mismo vale para hiperparámetros y tipo o cantidad de instancias (C2P1 1:23:31, C2P1 1:24:04, C2P1 1:25:08, C2P1 1:25:41).
- La notebook tiene un año y algunas librerías están deprecadas (C2P1 1:07:18).

### 3.9 Lab 3.7: ajuste de hiperparámetros
**Dónde:** C2P1 1:44:01, C2P1 1:44:33, C2P1 1:47:08, C2P1 1:49:21, C2P1 1:50:28, C2P1 1:54:55, C2P2 0:02, C2P2 1:47, C2P2 3:26, C2P2 5:38

- En clase lo llama "configurar el autopilot", pero lo que muestra es ajuste automático de hiperparámetros (C2P1 1:44:01). Correr hiperparámetros uno por uno es engorroso y en una sola instancia puede tardar días (C2P1 1:44:33, C2P1 1:45:45).
- Es el lab que más tarda (hasta unos 40 minutos) porque levanta muchas instancias, y él lo considera el más importante (C2P1 1:47:08, C2P1 1:56:35).
- Pasos: configurá rangos de hiperparámetros con mínimo, máximo y valor esperado (los que antes estaban fijos en el código), la cantidad de jobs en paralelo y en total, la imagen de entrenamiento, el tipo de instancia, el tiempo máximo y el volumen (C2P1 1:48:16, C2P1 1:49:21, C2P2 0:02, C2P2 6:12).
- Después analizá todos los training jobs para ver cuál se acerca al objetivo (por ejemplo con eta y alpha) (C2P2 1:47).
- Lo que en el 3.6 hiciste a mano acá es automático; se puede correr todos los días (C2P2 5:38, C2P2 6:12).
- Escalamiento horizontal es cantidad de servidores; vertical es tamaño (RAM, CPU); el autoescalado se ajusta a la demanda (C2P1 1:50:28, C2P1 1:51:36, C2P1 1:52:42).
- Muestra una ROC de alrededor de 0,78 sin ajuste contra 0,89 con ajuste (lectura dudosa del audio) (C2P1 1:54:55).
- Él puso 10 instancias y "aprovechen que paga Amazon"; con 10 jobs de 10 instancias son 100 instancias (C2P2 2:20, C2P2 7:18).
- `instance_count` del estimador no es lo mismo que la cantidad de jobs del tuning. Podés cortar cuando llega al valor esperado (C2P2 15:07, C2P2 16:14, C2P2 17:54).

### 3.10 Costos y control de gasto
**Dónde:** C1P2 24:32, C1P2 25:36, C2P2 7:50, C2P2 9:31, C2P2 11:12, C2P2 11:44, C2P2 12:49, C2P2 20:16, C2P2 21:58

- **AWS Pricing Calculator:** Craftech la usa para estimar. Ejemplo: ml.m5.xlarge 8 horas por día durante 22 días (C1P2 24:32). En C2P2 calcula una notebook ml.m5.xlarge 1 hora por día durante 30 días y le da "muy poquito" (C2P2 7:50).
- **Anécdota de Winclap:** un data scientist bloqueaba su máquina 8 horas una vez al mes; migraron a SageMaker por "40 por mes" (no dice la moneda) y solo pagan cuando está prendida. Además no conviene tener datos de clientes en la máquina personal por compliance y robo (C1P2 25:36, C1P2 27:45).
- La ejecución del lab costó muy poco (1 minuto 34 segundos de una M5). Dice "estamos por la M6 ya" (**para verificar**) (C2P2 7:50).
- 30 jobs con 10 instancias cada uno dan 100 horas por día, que es muchísimo; con la línea P (GPU) 10 jobs de una hora "se va a 250" (C2P2 9:31, C2P2 10:05, C2P2 10:40).
- Menciona una instancia de 1152 GB de RAM por "250 USD por mes" (cifra dudosa, **para verificar**) (C2P2 14:28).
- **No podés limitar el gasto en duro:** lo que tenés son alertas y billing. Con **Budgets** definís cuánto podés gastar por mes (C2P2 11:12, C2P2 11:44).
- **FinOps:** una empresa mediana gasta 20.000 o 30.000 por mes en AWS y alguien de FinOps o DevOps mira métricas, por ejemplo "nunca llegaste al 50% de CPU", para bajar a una instancia más barata (C2P2 12:17, C2P2 12:49).
- **Tags y Cost Explorer:** etiquetá recursos por cliente (el ejemplo es Epec) y filtrá en Cost Explorer por tag para cobrarle a cada uno (C2P2 20:16, C2P2 21:24).
- **Multi-account:** una cuenta por cliente o proyecto deja la factura limpia; aclara que no es parte de la materia (C2P2 21:58).

<details>
<summary>Preguntas de repaso del módulo 3 (con respuestas)</summary>

1. **¿Por qué el nombre de la notebook instance tiene que ser exactamente el del lab?** Porque los permisos de IAM están asociados a ese nombre, que distingue mayúsculas y minúsculas.
2. **¿Qué tipo de instancia y qué lifecycle configuration usa el lab 3.1?** ml.m5.xlarge y la lifecycle configuration ml-pipeline, que configura Jupyter al arrancar.
3. **¿Qué algoritmo usa el lab 3.1?** Linear Learner, uno de los algoritmos integrados de SageMaker.
4. **¿Qué dataset se usa desde el lab 3.2?** Uno de ortopedia con anomalías en pacientes (hernia de disco, espondilolistesis).
5. **¿Qué hacés con una variable ordinal como bajo, medio, alto, muy alto?** La pasás a números del 1 al 4.
6. **¿Qué formatos de entrenamiento menciona la clase?** CSV, JSON y protobuf RecordIO.
7. **¿Por qué no conviene conectarse a la base de producción desde la notebook?** Porque las credenciales quedan expuestas y podés modificar o borrar datos productivos; lo correcto es consumir un CSV que deja el data engineer.
8. **¿Cuáles son las dos formas de desplegar del lab 3.5?** Alojamiento de SageMaker (endpoint) y transformación por lotes (batch transform).
9. **¿Qué pasa con el modelo si borrás el endpoint?** Deja de estar hosteado, pero el archivo del modelo sigue en S3.
10. **¿Qué controla initial_instance_count?** La cantidad inicial de instancias que sirven el endpoint, es decir el escalamiento horizontal.
11. **¿Qué umbral usa el lab 3.6 y qué valores propone probar?** Usa 0,3 y propone probar 0,25 y 0,75.
12. **¿Dónde debería vivir el umbral en producción según el docente?** En una variable de entorno o una base de parametría, para cambiarlo sin redesplegar.
13. **¿Qué automatiza el lab 3.7?** La búsqueda de hiperparámetros, corriendo muchos training jobs con rangos definidos.
14. **¿Cuál es la diferencia entre escalar horizontal y verticalmente?** Horizontal es sumar servidores; vertical es hacer más grande el servidor.
15. **¿Se puede poner un tope duro al gasto de AWS según la clase?** No; se usan alertas, billing y Budgets.
16. **¿Cómo separás los costos de cada cliente?** Con tags filtrados en Cost Explorer, o con una cuenta por cliente.

</details>

---

## Módulo 4. Forecast (salteado)
**Dónde:** C1P2 1:24:30, C2P2 24:11, C2P2 24:46, C2P2 25:18

- Es el único módulo que no hacen en clase. Según el docente, Forecast "no se usa más" y "ahora todo eso lo corren dentro de SageMaker" (**para verificar** el estado actual del servicio) (C1P2 1:24:30, C2P2 24:46).
- No hace falta estudiarlo de memoria, pero el cuestionario hay que hacerlo para el certificado. En la transcripción dice "reclamar el budget", que en contexto es la insignia (badge) (C2P2 25:18).

<details>
<summary>Preguntas de repaso del módulo 4 (con respuestas)</summary>

1. **¿Por qué no se ve Forecast en clase?** Porque el docente dice que está deprecado y que los pronósticos ahora se resuelven dentro de SageMaker.
2. **¿Igual hay que hacer el cuestionario del módulo 4?** Sí, para obtener el certificado.

</details>

---

## Módulo 5. Visión por computadora
**Dónde:** C2P2 25:18, C2P2 26:26, C2P2 35:11, C2P2 36:15, C2P2 41:23, C2P2 45:57, C2P2 48:17, C2P2 52:12, C2P2 57:38, C2P2 59:19, C2P2 1:01:16, C3P1 2:12

Dice que es el módulo más sencillo (C2P2 25:54).

### Conceptos clave
- **Visión artificial** es extraer automáticamente información de imágenes. Estos modelos son más chicos que los fundacionales (C2P2 26:26, C2P2 26:59).
- **Casos que da:** accesos con rostro (México, countries, colegios), onboarding bancario con DNI, cara y gestos, redes sociales que etiquetan contenido, Google Photos buscando "bosque", autos con corrección de carril y lectura de carteles, imágenes médicas como sugerencia probabilística, comercios sin cajeros en Chile, la cámara del Mundial que sigue a Messi, Amazon Prime X-Ray con actores en tiempo real y flujo de personas en aeropuertos (C2P2 27:32 a C2P2 40:53).
- **Rekognition** es un modelo preentrenado y totalmente administrado: no pensás en cómputo. Identifica algunas cosas, no todo; si no reconoce cubiertos o servilletas, tenés que entrenarlo con tus propias imágenes. En clase lo llama "fine tuneo"; no nombra la función específica de Rekognition para eso (C2P2 35:11, C2P2 35:42, C2P2 41:23).
- **Confianza:** Rekognition devuelve etiqueta, porcentaje de confianza y bounding box (coordenadas). Él toma desde 70% para decir que es el objeto (C2P2 36:15, C2P2 36:49, C2P2 57:38).
- **Cuándo Rekognition y cuándo un modelo propio.** Rekognition ahorra tiempo y cómputo pero se paga por imagen analizada. Conviene cuando necesitás escalar mucho y no necesitás correr local, como un shopping, Instagram o Netflix. Para una cámara hogareña conviene un modelo chiquito local (C2P2 42:31, C2P2 43:06).
- Tiene SDKs para Java, Python y PHP, y la gracia es el ecosistema de AWS (C2P2 44:49, C2P2 45:22).

### Arquitecturas con Rekognition
- **S3 + Lambda + Rekognition:** cada imagen que entra a S3 dispara un servidor (Lambda) que llama a Rekognition y guarda las etiquetas en una base de datos, para después buscar, por ejemplo, "monumentos". El servidor se prende y se apaga, y pagás por imagen procesada y por segundo de servidor (C2P2 45:57, C2P2 46:31, C2P2 47:04, C2P2 47:36).
- **Moderación con certificados médicos:** el archivo llega a S3, se despierta la Lambda, Rekognition analiza y, si no es un certificado médico, se le devuelve al usuario. Esto es lo que lo diferencia de un Google Drive, que no tiene esos triggers (C2P2 48:17).
- **Búsqueda por etiquetas:** una tabla con la URL de la imagen en S3 y sus etiquetas. Guardar los tags en S3 "no es lo ideal"; para búsqueda existen Elasticsearch u OpenSearch (ejemplo de Mercado Libre con zapatillas) (C2P2 49:56, C2P2 50:31, C2P2 51:07, C2P2 51:41).
- **Video en tiempo real:** cámara, streaming, servidor, S3 y data warehouse. La persistencia del streaming es corta, de 1 a 2 horas, "creo que hasta 24 horas" (**para verificar**). Es near real time: hasta el tablero pueden pasar 5 minutos. Una Lambda filtra solo autos o patentes y devuelve JSON; S3 es almacenamiento frío y Redshift hace la analítica pesada (C2P2 52:12, C2P2 53:51, C2P2 56:03, C2P2 56:36, C2P2 57:07).

### Colección de caras
- Una **colección** es como un álbum interno o catálogo de caras. Le das una imagen y te dice con un porcentaje si está esa persona; cada cara tiene un Face ID (C2P2 59:19, C2P2 1:00:24, C2P2 1:33:36).
- El hiperparámetro principal es la confianza (C2P2 1:04:33).
- En el repaso de C3P1: la carpeta models tiene fotos de la persona con sombrero, con anteojos y sin nada. Amazon siempre devuelve un porcentaje de coincidencia (98, 50, 20) y elegís el mayor; con un umbral de 70% "es más probable que sea Pepe que José" (C3P1 2:12, C3P1 4:24, C3P1 5:31).
- Es "una especie de entrenamiento" porque vos etiquetás el nombre. Sumar más caras de la persona (frontal, de costado, con gorra) mejora el resultado (C3P1 8:15, C3P1 8:51, C3P1 9:58).

### El lab del módulo 5
**Dónde:** C2P2 1:01:16, C2P2 1:02:22, C2P2 1:05:09, C2P2 1:11:23, C2P2 1:15:02, C2P2 1:23:25, C2P2 1:25:54, C3P1 6:36

1. Primero hay una demo de Rekognition por consola y después "los bifes" en la notebook (C2P2 1:05:09).
2. Creá la colección y registrá las imágenes con un for por cada imagen de la carpeta (C2P2 1:02:22, C2P2 1:02:54).
3. Tomá una imagen target, reescalala, agregá la cara a la colección y obtené su Face ID (C2P2 1:11:23).
4. Tirale imágenes nuevas y mirá cuáles reconoce ("este es, este no") (C2P2 1:03:59).
5. Dibujá el recuadro (bounding box) del color que quieras, con un offset de 15% para recortar (C3P1 6:36, C3P1 7:10).
6. Cambiá el target por una foto tuya; está incluido en los créditos del lab (C2P2 1:17:17).

Problemas que aparecieron en clase:
- El bucket apuntaba a otro: hay que cambiarlo (C2P2 1:15:02).
- Si la colección ya existe da error: reiniciá el kernel o eliminá la colección. A veces el lab no deja borrarla porque los permisos de las cuentas del lab son muy limitados y cambiaron en un año (C2P2 1:16:08, C2P2 1:16:44, C2P2 1:23:25).
- Si detecta una sola cara es porque MaxFaces está en 1; subilo. Con MaxFaces en 5 puede devolver algo parecido a una persona, así que definí un umbral, por ejemplo 90% (C2P2 1:25:54, C2P2 1:26:58, C2P2 1:27:31).
- Imprimí la respuesta entera para ver todo lo que devuelve (C2P2 1:30:13).
- Podés cambiar caras por patentes para otro caso (C2P2 1:41:40).

### Tips del docente
- Hay librerías Python gratuitas que corrés local (por ejemplo para patentes) y las de OCR andan muy bien (C2P2 1:05:41, C2P2 1:08:25).
- Él combina: primero OCR local y, si no alcanza, Rekognition (1 de cada 10 casos). Dice que Rekognition "tiene un feature solamente para DNI" (**para verificar**) (C2P2 1:08:39, C2P2 1:09:12).
- La capa gratuita de Rekognition sería de "5000 imágenes al mes durante los primeros 12 meses" (**para verificar**) (C2P2 1:17:55).
- Para documentación, mirá el SDK de Python (boto3), los límites y los tipos de archivo (C2P2 1:18:27).
- Recomienda los cursos gratuitos de AWS Skill Builder, como el de machine learning engineer en español, y certificarse; en Craftech todos tienen que certificarse en los primeros 3 meses (C2P2 1:20:09, C2P2 1:20:43).

<details>
<summary>Preguntas de repaso del módulo 5 (con respuestas)</summary>

1. **¿Qué devuelve Rekognition por cada objeto detectado?** Una etiqueta, un porcentaje de confianza y un bounding box.
2. **¿Cuándo conviene Rekognition y cuándo un modelo local?** Rekognition cuando tenés que escalar mucho sin correr local; un modelo chico local para casos como una cámara hogareña.
3. **¿Cómo se cobra Rekognition según la clase?** Por imagen analizada.
4. **Describí la arquitectura de etiquetado automático que muestra la clase.** Una imagen entra a S3, dispara una Lambda que llama a Rekognition y las etiquetas se guardan en una base de datos para buscarlas después.
5. **¿Qué es una colección de caras?** Un catálogo interno de caras registradas, cada una con su Face ID, contra el que se comparan imágenes nuevas.
6. **¿Por qué el lab detectaba una sola cara?** Porque MaxFaces estaba en 1.
7. **¿Qué hacés si la colección ya existe?** Reiniciás el kernel o eliminás la colección.
8. **¿Cómo mejorás el reconocimiento de una persona?** Agregando más caras de esa persona desde distintos ángulos y con distintos accesorios.

</details>

---

## Módulo 6. Procesamiento de lenguaje natural
**Dónde:** C3P1 17:44, C3P1 18:17, C3P1 20:29, C3P1 29:58, C3P1 36:36, C3P1 43:46, C3P1 45:53, C3P1 49:42, C3P1 55:47, C3P1 58:05, C3P1 1:02:34, C3P1 1:07:32, C3P1 1:08:38, C3P1 1:12:23

### Conceptos clave
- **Por qué siguen vigentes estos servicios.** Parecen viejos, pero están pensados para escalamiento. A escala masiva los modelos fundacionales son costosos por los tokens, así que conviene usar servicios específicos para tareas específicas (C3P1 17:44, C3P1 18:17, C3P1 19:23).
- **Cómo funciona Alexa.** El dispositivo (muestra un Echo Dot) más herramientas para desarrollar productos. Su demo de 2019 o 2020 iba de la skill a una Lambda, de ahí a reglas de negocio y a bases de datos. La inferencia es un porcentaje de probabilidad de lo que quisiste decir (C3P1 20:29, C3P1 21:44, C3P1 24:25).
- **PLN clásico.** Es un modelo de ML chico y probabilístico: la frase se parte en palabras, se calcula la probabilidad de cada instrucción y una variable (leche, jugo, agua) cambia la query. Los intents y las variaciones de frases se cargan a mano (C3P1 28:19, C3P1 29:58).
- **Desafíos.** Con muchas variaciones todo se vuelve probable (pedís stock de leche y te da ventas), la gente habla con interrupciones y pausas, y hay variantes regionales (popote, pururú) que obligan a entrenar constantemente (C3P1 32:47, C3P1 36:36, C3P1 37:41).
- **Pasos del procesamiento:** normalización (pururú y pochoclo, carro y auto, corrió y corriendo), bolsa de palabras (contar coincidencias), tokenización y clasificación de texto, contexto ("Mercedes negro" puede ser un auto o Mercedes Sosa) y extracción de entidades (Titanic como barco, Atlántico Norte como ubicación) (C3P1 45:53, C3P1 49:42, C3P1 52:29, C3P1 54:40, C3P1 55:47).
- **Costo del call center generativo.** Cuenta que "ya fueron miles" los intentos con IA generativa (ChatGPT, Amazon Nova, ElevenLabs) y que el problema es el costo: lo describe como "más caro que un ser humano contestando", con "cientos de dólares" por hora (opinión, **para verificar**). Los chatbots de PLN clásico, en cambio, funcionan muy bien (C3P1 43:46, C3P1 44:19).

### Servicios
| Servicio | Para qué sirve según la clase |
|---|---|
| Transcribe | Transcripción, subtítulos y etiquetado de contenido, también en streaming por WebSocket. En un call center transcribe en tiempo real, tokeniza y da un scoring de la llamada. A gran escala (500.000 personas) el 5 o 10% de sobreprecio de Amazon importa frente a levantar tu propio modelo en SageMaker (C3P1 58:05, C3P1 59:11, C3P1 1:00:17, C3P1 1:01:26, C3P1 1:02:01) |
| Polly | Texto a voz; muy barato, "casi ni te conviene hostear el tuyo". Sirve para noticias, radios o un GPS que lee calles (C3P1 1:02:34, C3P1 1:04:48, C3P1 1:05:21) |
| Nova | Lo presenta como una "versión mejorada de Polly", más generativa y con tonadas (**para verificar**) (C3P1 1:04:48) |
| Translate | Traducción clásica (C3P1 1:07:32) |
| Comprehend | Entidades clave y sentimiento positivo o negativo. Dice que ahora usa modelos fundacionales además de PLN (**para verificar**). Ejemplos: buscador de libros con "Córdoba", nombres ambiguos como Ángeles y auditoría de mantenimiento de maquinaria agrícola (C3P1 1:08:38, C3P1 1:09:42, C3P1 1:10:47, C3P1 1:11:18) |
| Lex | Combina voz y texto para armar chatbots: inventario, ventas, consultas a base de datos, servicio al cliente, el clásico "marque la opción uno" (C3P1 1:12:23, C3P1 1:13:27) |

También aclara que la voz de ChatGPT son dos modelos, uno de texto y otro de síntesis (C3P1 1:03:08).

### El lab del módulo 6: chatbot con Lex
**Dónde:** C3P1 1:14:00, C3P1 1:15:04, C3P1 1:17:12, C3P1 1:20:00, C3P1 1:21:05, C3P1 1:34:18, C3P1 1:48:08, C3P1 1:51:53, C3P1 1:55:47, C3P1 1:58:58, C3P1 2:03:21, C3P1 2:11:04

Lo hacen los alumnos. La guía dice 60 minutos y él estima 40 a 45. No hay notebook: es copiar y pegar, con código HTML (C3P1 1:14:00, C3P1 1:15:04, C3P1 1:18:52).

1. Usá el starter code del lab (C3P1 1:16:11).
2. Al crear el bot, a todos les falló la creación del rol: usá un rol existente (C3P1 1:21:05).
3. Amazon ya sugiere probar el builder nuevo con IA generativa en Lex; el lab usa el bot clásico (C3P1 1:20:00).
4. Si da error de permisos la Lambda, usá el rol de ejecución "Lex role"; los nombres de rol están mapeados a los nombres de las funciones (C3P1 1:34:18, C3P1 1:35:59).
5. Asociá la Lambda dentro del intent y configurá el alias (C3P1 1:48:08).
6. Creá el bucket "Lab 6", desbloqueá el acceso público y reconocé la advertencia. Tener un bucket público es mala práctica, pero en el lab no pasa nada (C3P1 1:51:53, C3P1 1:52:56, C3P1 1:53:29).
7. En la bucket policy reemplazá el ARN por el de tu bucket; si no, aparece "Policy has invalid resource". Si el nombre del bucket ya existe es porque los nombres son únicos a nivel global (C3P1 1:58:58, C3P1 2:01:02).
8. Activá static website hosting con index.html y error.html (C3P1 2:03:21).
9. En el HTML cambiá el bot ID, el bot alias ID, la región (us-east-1, la ves en la URL) y el identity pool de Cognito (C3P1 1:17:12, C3P1 1:53:59, C3P1 1:54:32, C3P1 2:11:04).
10. Editá el index local y subilo (C3P1 2:12:12).

Conceptos del lab:
- **Bot y alias:** cada alias es un despliegue distinto (idiomas, comportamientos, canales) y puede usar una Lambda distinta (C3P1 1:55:47, C3P1 1:56:52).
- **Qué conecta los servicios:** los roles de IAM. Un servicio asume un rol y todo se comunica por API con credenciales (C3P1 1:42:44, C3P1 1:44:56, C3P1 1:46:03).
- **El bot es primitivo:** para mejorarlo agregás flujos; los horarios están fijos en la Lambda y deberían salir de una base o una API de disponibilidad. Si querés algo conversacional necesitás un modelo agéntico con RAG; el clásico es muy económico (C3P1 1:38:02, C3P1 1:38:35, C3P1 1:39:09).
- **Por qué el bot clásico sigue sirviendo:** responde muy rápido, con cientos de miles de requests gana sí o sí porque usa poco cómputo, y conversar con un generativo gasta tokens cuando solo querés un booking (C3P1 2:05:36, C3P1 2:06:40, C3P1 2:08:16).

Advertencias: la interfaz cambia mucho (C3P1 1:23:23, C3P1 1:50:08) y en noviembre, con re:Invent, suelen cambiar toda la UI (**para verificar**). Dice que hostear la web estática en S3 sale "sin costo" (**para verificar** fuera del lab) (C3P1 2:04:27) y que el repo de su bot generativo se puede desplegar en una cuenta personal "sin costo" (**para verificar**) (C3P1 1:41:16).

<details>
<summary>Preguntas de repaso del módulo 6 (con respuestas)</summary>

1. **¿Por qué usar servicios específicos de PLN en lugar de un modelo fundacional?** Porque a escala masiva los fundacionales son caros por los tokens y los servicios específicos son más baratos y rápidos.
2. **¿Qué es la normalización?** Llevar variantes a una forma común, como pururú y pochoclo o corrió y corriendo.
3. **¿Qué ejemplo usa para explicar la importancia del contexto?** "Mercedes negro", que puede ser un auto o Mercedes Sosa.
4. **¿Qué servicio usarías para el scoring de llamadas en tiempo real?** Transcribe en streaming, tokenizando la conversación.
5. **¿Qué hace Comprehend?** Extrae entidades clave y analiza sentimiento.
6. **En el lab de Lex, ¿qué valores hay que cambiar en el HTML?** El bot ID, el bot alias ID, la región y el identity pool de Cognito.
7. **¿Qué error aparece si no reemplazás el ARN en la bucket policy?** "Policy has invalid resource".
8. **¿Para qué sirven los alias de un bot de Lex?** Para tener despliegues distintos (idioma, comportamiento, canal), cada uno con su propia Lambda si hace falta.
9. **¿Qué conecta a Lex, Lambda y S3 entre sí?** Los roles de IAM que cada servicio asume.

</details>

---

## Extra A. IA generativa, Amazon Q y Kiro
**Dónde:** C3P2 0:03, C3P2 2:15, C3P2 3:20, C3P2 10:27, C3P2 12:05, C3P2 14:14, C3P2 18:04, C3P2 19:11, C3P2 20:16, C3P2 22:58, C3P2 28:23, C3P2 28:57, C3P2 35:06, C3P2 37:01

Desde la clase 1 avisa que va a mostrar servicios nuevos que no están en la plataforma (C1P2 1:25:24). La clase no dice si este bloque entra en algún cuestionario.

### Conceptos clave
- **Generativa contra bot clásico.** El bot de Lex fragmenta el flujo (turno, después hora); la generativa puede investigar una base interna y recomendar, por ejemplo, una habitación para 4 personas (C3P2 0:03, C3P2 1:09).
- **Casos de uso:** experiencia del cliente, productividad de empleados, automatización, creatividad y contenido (C3P2 2:15, C3P2 2:47).
- **Modelo fundacional:** alguien lo entrenó con muchísima información. Los modelos tradicionales usan datos etiquetados; los fundacionales, datos sin etiquetar (C3P2 3:20, C3P2 4:25, C3P2 10:27).
- **Generación de imagen y video:** menciona Sora y el antes y después de Will Smith comiendo, la consistencia del personaje entre frames y una opinión sobre series en tiempo real a futuro (C3P2 4:58, C3P2 6:02, C3P2 8:18, C3P2 9:22).
- **Costo:** un chatbot de turnos con generativa "es carísimo", y un modelo generalista para atención al cliente también; por eso Lex sigue vigente (C3P2 10:27, C3P2 11:32).
- **Hacia dónde va la carrera:** entrenar modelos específicos, porque la gracia no es un modelo gigante que sepa de todo (C3P2 12:05, C3P2 12:36).
- **Bases vectoriales:** resurgieron con los fundacionales para buscar por patrones (vuelve el ejemplo de Mercedes) (C3P2 14:14).
- **Entrada y salida:** al fundacional lo adaptás con una petición (input) y obtenés una salida (output) (C3P2 16:23, C3P2 16:54).

### Servicios y hardware
| Servicio o recurso | Para qué sirve según la clase |
|---|---|
| Bedrock | "El servicio para todo lo que tiene que ver con modelos de IA": modelos fundacionales como servicio (C3P2 19:11). En C3P1 dice que "excepto Gemini están casi todos los modelos" (**para verificar**) (C3P1 15:25) |
| SageMaker JumpStart | Modelos preentrenados para usar o ajustar (C3P2 20:16) |
| Trainium | Chips de AWS para entrenamiento; también menciona chips para inferencia sin que el nombre se entienda (C3P2 20:48) |
| Instancias de la línea P | GPU de Nvidia (C3P2 21:21) |
| Amazon Q y Kiro | Asistente de código. Dice que Amazon Q "quedó medio viejo" y que hubo un rebranding a Kiro "hace un par de meses", y que Kiro tiene menos de un año (**para verificar**) (C3P2 18:39, C3P2 28:57) |
| "Transobre" (probablemente AWS Transform, dudoso) | Plataforma para migrar código COBOL de bancos a AWS con varios modelos ajustados por etapa (C3P2 32:52, C3P2 33:25) |

### Cuándo entrenar tu propio modelo
- Cuando gastás cientos de miles de dólares en tokens. Cuenta de un cliente que gasta 200.000 USD en Bedrock con Opus, donde cualquier 5% de ahorro es mucho (C3P2 22:58, C3P2 23:30).
- Tener ese cómputo en casa es inviable por refrigeración y ruido, conseguir el hardware tarda días y queda viejo en un año; en la nube son dos clics (C3P2 21:54, C3P2 25:40, C3P2 26:40).

### Integraciones nativas
Lex se integra con Lambda y con Bedrock, y Bedrock con Lambda. Así el fundacional responde de forma más inteligente sin que tengas que armar todas las preguntas y respuestas (C3P2 28:23).

### Kiro en empresas y demo
- La ventaja en empresas (el ejemplo es Bancor) es el acceso a los servicios de AWS con permisos y gobernanza: qué notebooks, qué instancias, reglas como "solo código de la empresa" o "no compartir información sensible" (C3P2 29:31, C3P2 30:37).
- En C3P1 suma que Kiro usa el catálogo de modelos de Bedrock y elige el modelo solo para reducir tokens (C3P1 13:47).
- Demo: habilitá Kiro en la cuenta e invitá personas por correo, bajá el IDE (parecido a VS Code), abrí la carpeta del lab 6 y pedile que deje el index.html "más bonito" (C3P2 37:01, C3P2 38:48, C3P2 41:19, C3P2 41:52).
- Kiro tiene costo de suscripción y "creo que tiene una capa gratuita" (**para verificar**) (C3P2 37:01).
- Los modelos detrás son los mismos de siempre; la gracia está en la interfaz, la planificación y la integración con tus credenciales de AWS para desplegar instancias o el bot de Lex (C3P2 43:04, C3P2 43:36, C3P2 45:53).

<details>
<summary>Preguntas de repaso del extra A (con respuestas)</summary>

1. **¿Qué diferencia de datos de entrenamiento hay entre un modelo tradicional y uno fundacional?** El tradicional usa datos etiquetados; el fundacional, grandes volúmenes sin etiquetar.
2. **¿Por qué Lex sigue vigente frente a la generativa?** Porque un chatbot generativo para tareas simples como turnos es carísimo a escala.
3. **¿Qué servicio de AWS es el catálogo de modelos fundacionales?** Bedrock.
4. **¿Cuándo tiene sentido entrenar un modelo propio según el docente?** Cuando el gasto en tokens llega a cientos de miles de dólares.
5. **¿Qué ventaja tiene Kiro en una empresa?** Se integra con los servicios de AWS con permisos y reglas de gobernanza.

</details>

---

## Extra B. Bedrock en profundidad
**Dónde:** C4P1 0:02, C4P1 1:40, C4P1 3:53, C4P1 5:30, C4P1 7:41, C4P1 11:31, C4P1 14:55, C4P1 17:05, C4P1 22:36, C4P1 31:51, C4P1 39:34, C4P1 41:47, C4P1 47:09, C4P1 48:17, C4P1 59:21, C4P1 1:02:07, C4P1 1:09:47

Plan de la clase 4: Bedrock, embeddings y búsqueda, datos, agentes, AgentCore ("el servicio estrella") y despliegue, con un repo de GitHub que podés desplegar en tu cuenta y que "les va a salir algunos centavos de dólar" (C4P1 0:02, C4P1 0:35, C4P1 1:08, C4P1 2:14).

### Tokens y modelos
- Los modelos generalistas se encauzan para que sean expertos en algo (resumir, responder un RAG). Funcionan prediciendo el siguiente token (C4P1 2:47, C4P1 3:20).
- **Fine tuning:** una capa extra con tus datos, porque te interesa el 20% del modelo que hace a tu especialidad. Usa el ejemplo de un recetario con milanesa y no milanesa. Ajustar un modelo como DeepSeek es una tarea titánica (C4P1 3:53, C4P1 4:25, C4P1 4:58, C4P1 7:41).
- **Token:** la mínima unidad de lo que entra y sale; la cantidad varía según el modelo (C4P1 5:30).
- **Elegir modelo** es tarea del AI engineer y AWS tiene herramientas para eso. Dice que un modelo nuevo puede gastar mucho más que el anterior y dar lo mismo para ciertas tareas (da nombres de versiones de Opus que **hay que verificar**), así que actualizar siempre no es la mejor estrategia (C4P1 6:04).
- Con **boto3** declarás el modelo, mandás el mensaje y la respuesta te dice los tokens de entrada y de salida. La demo corre la misma frase contra varios modelos y compara tokens (C4P1 6:38, C4P1 7:09).
- **Parámetros de inferencia:** top P, temperatura, top K, max tokens y cantidad de secuencias. Permiten ajustar sin redesplegar ni hacer fine tuning. La temperatura baja da la respuesta más probable y la alta, más creatividad; lo compara con el umbral de Rekognition (C4P1 7:41, C4P1 8:47, C4P1 9:53, C4P1 10:28).
- **Tipos de modelo:** texto, embeddings (vectores que dan contexto rápido sin gastar todo en tokens) e imagen. Pesos abiertos contra API; también podés crear los tuyos con SageMaker y GPU (C4P1 11:31, C4P1 12:05, C4P1 13:47, C4P1 14:21).
- **Catálogo de Bedrock:** Claude, GPT, Nova, Llama (pesos abiertos), DeepSeek, y modelos de imagen, video y voz. También está el Marketplace de SageMaker (C4P1 17:05).

### Datos sensibles y regulación
- En Bancor no podían implementar IA porque los datos personales tienen que quedar en fuentes privadas; hay que anonimizar (C4P1 14:55).
- Afirma que los proveedores se quedan con la información y la reusan para entrenar, y que hubo información sensible que apareció en modelos futuros (**para verificar**) (C4P1 16:31, C4P1 21:24).
- Un alumno pregunta si Bedrock no usa los datos para entrenar. Él responde que el dato viaja por API y puede ir a un servidor del proveedor, que el compliance cubre algunas cosas pero movés datos a una frontera que no conocés, y que el Banco Central pone límites a lo que sale del core (**para verificar** qué hace Bedrock con los datos) (C4P1 17:37, C4P1 18:41).
- Sigue un tramo de opinión sobre regulación de la IA (Brasil, China, bancos que publican algoritmos de crédito) (C4P1 25:20).

### Elegir modelo y pagar menos
- Criterios: calidad, latencia y costo. Ejemplo: un análisis de vulnerabilidades que corre de noche con un modelo pesado, donde no importa el tiempo pero el costo es muy alto. Los modelos de razonamiento profundo gastan más tokens y el video es más lento (C4P1 22:36, C4P1 23:09, C4P1 24:13).
- Pagar menos no es elegir el modelo más barato (C4P1 31:51). Opciones que da:
  - **Prompt caching.** Dice que los modelos privados cachean pero cobran como si no, y que con un modelo local ahorrás "hasta un 90%" (**para verificar**) (C4P1 32:23).
  - **Batch inference.** Mandar el volumen junto en un momento de poco uso (C4P1 32:55).
  - **Spot.** Precio volátil (C4P1 33:28).
  - **Región o momento más barato** (C4P1 34:00).
  - **No usar el modelo más caro para algo simple** ("usemos el modelo más caro para mandar mails" es el chiste) y enrutar por tarea, con versiones reducidas o Lite (C4P1 35:40, C4P1 36:14).
  - **Inference profiles y cross region.** Bedrock enruta el mismo modelo a una región más barata en el momento. Opina que eso tiene vida finita por la escasez de infraestructura y de RAM (**para verificar**) (C4P1 36:53, C4P1 37:25).
- Menciona cuotas de OpenAI de unos 100 requests por minuto y ventanas de uso de 5 horas (**para verificar**) (C4P1 38:25).
- Ejemplos de uso: normalizar facturas de terceros con IA y análisis sobre un data lake (C4P1 34:32, C4P1 35:06).

### Piezas de Bedrock
- Bedrock y SageMaker van de la mano (C4P1 41:13).
- Componentes: el runtime (donde corre el cómputo), la knowledge base (el RAG), AgentCore (orquesta los MCPs y la memoria) y la evaluación (saber si la respuesta es buena o hay que mejorar). Atrás está el modelo fundacional (C4P1 41:47).
- RAG sirve para darle información actualizada o propia del negocio sin esperar un modelo nuevo (C4P1 40:08).

### Guardrails
**Dónde:** C4P1 41:47, C4P1 42:20, C4P1 43:25, C4P1 43:56, C4P1 44:28, C4P1 45:01, C4P1 45:32, C4P2 23:35, C4P2 25:20, C4P2 29:13, C4P2 29:45, C4P2 30:49, C4P2 31:20

- Un guardrail es un modelo muy chiquito entrenado para filtrar input y output, "como un patovica de boliche". Recomienda tener los propios porque son fáciles de entrenar (C4P1 41:47, C4P1 42:20).
- En Bedrock es un servicio propio: le das un system prompt (por ejemplo, solo atención al cliente de Bancor o venta de productos) y una severidad. Recuerda "tres o cuatro niveles", algo como low, medium, high y uno que no valida nada (**para verificar**) (C4P1 43:25, C4P1 43:56).
- Bloquea el input y el usuario recibe un "no pasás". Evita prompt injection y que se filtre información sensible (C4P1 44:28).
- Si filtrás con el system prompt del modelo grande, ya "moviste un titán": gastaste cómputo y tokens para decidir que la pregunta no era válida. En benchmarks el guardrail consumiría "4%" de los tokens, por ejemplo 40 contra 1000 (**para verificar**) (C4P1 45:01, C4P1 45:32).
- También corta alucinaciones, como ofrecer un crédito hipotecario para naves espaciales, y puede mandar casos a evaluación (C4P1 46:04, C4P1 46:37).
- En C4P2 suma: filtra datos sensibles (email, teléfono, reglas de compliance, patrones PCI); se configura en Converse con su versión y un trace; las políticas incluyen contenido filtrado, temas denegados, palabras clave, información sensible y contexto; conviene un guardrail por caso (ventas, cliente); puede bloquear o filtrar y siempre documentar; el trace muestra los tópicos y la fuerza del filtro, y los logs sirven para reentrenar (C4P2 23:35, C4P2 29:13, C4P2 29:45, C4P2 30:49, C4P2 31:20, C4P2 31:54).
- **Prompt injection dentro de documentos:** una foto de DNI puede traer un prompt adentro. El OCR lo hace el modelo, no el guardrail, así que se usa una IA intermedia que abre el documento y lo pasa por un guardrail primero (C4P2 24:47, C4P2 25:20, C4P2 25:52).
- En la demo, cuando el guardrail bloquea, el consumo de tokens es cero porque no llegó al modelo (C4P2 56:17).

### Acceso a modelos y API
- En uso personal alcanza con los modelos disponibles, pero en una empresa con 100 o 1000 requests por segundo vas a ver que no están en todas las regiones y se habilitan de a poco por cuenta (C4P1 47:09).
- Afirma que si habilitás un modelo en una región y no lo usás uno o dos meses, se vuelve a deshabilitar, que a veces hay que habilitarlo desde el Marketplace, y que los modelos nuevos hay que habilitarlos mientras los clásicos no (**para verificar**) (C4P1 47:43).
- **Converse contra InvokeModel:** Invoke "ya medio no se usa" porque Converse evolucionó; Converse sirve para interactuar y tiene más parámetros, como max tokens (**para verificar**) (C4P1 48:17, C4P1 48:50, C4P1 49:22).
- La estructura de una llamada es modelo, system prompt, messages e inference config (temperatura) (C4P1 49:54).
- El parámetro system "cambió desde Opus 4, creo" (**para verificar**). Con él no repetís "sos un profesor" en cada mensaje, condicionás al modelo y armás un agente experto por tema (C4P1 50:27, C4P1 50:59, C4P1 52:41).
- **Streaming:** el guardrail revisa el stream a medida que llega; por eso, según él, muchos chats como los de Rappi o Mercado Pago responden sin streaming, porque cuanto menos streameás más fácil es validar (afirmación, **para verificar**) (C4P1 53:15, C4P1 54:55, C4P1 55:27).
- Podés mandar bytes a un modelo multimodal, que hace OCR interno de un PDF; no todos los modelos son multimodales (C4P1 57:04, C4P1 57:38).
- Con un esquema de respuesta obtenés siempre el mismo formato (C4P1 58:11).

### Seguridad y observabilidad
- La IA no es determinística como un script de Python, así que aplicá **mínimo privilegio** (least privilege): el agente que lee el RAG solo puede leer ese RAG, usando IAM. Cuidá también las API keys de Bedrock (C4P1 59:21, C4P1 59:54, C4P1 1:01:01).
- A gran volumen hay que vigilar consumo de tokens, accesos no controlados y tasa de errores (C4P1 1:01:34).
- **CloudTrail** muestra quién usó qué API key. En el mismo tramo habla del **invocation logging**, que registra el prompt que entró y salió y los tokens; **CloudWatch** da insights de logs y métricas como RAM, disco, CPU y latencia (C4P1 1:02:07).
- Se pierde de vista en qué se consumen los tokens. Las herramientas no están maduras, y una IA que vigila a otra también consume ("el perro que se muerde la cola"). Menciona Datadog (C4P1 1:03:12, C4P1 1:03:45).
- Para modelos propios, mide eficiencia en tokens por minuto (C4P1 1:06:32).
- **SageMaker JumpStart** permite tomar modelos abiertos, ajustarlos y publicarlos (C4P1 1:08:11).

### Prompt engineering desde el backend
- Partes de un prompt: contexto, datos de entrada y formato de salida (C4P1 1:09:47).
- **Presupuesto de tokens por caso de uso:** un bot de turnos con 500 tokens. Si se pasa, monitoreá y poné una alerta al 90%. Con max tokens en 5000 el modelo se explaya; con 500 contesta en dos renglones (C4P1 1:11:28, C4P1 1:11:59, C4P1 1:13:06).
- Roles en el system prompt; MoE (mixture of experts), que elige dos nodos expertos (C4P1 1:13:45, C4P1 1:14:16).
- Zero shot, few shot y adaptive thinking (esfuerzo). Resolver 3 o 4 veces y elegir la mejor "te mata los tokens" (C4P1 1:16:26, C4P1 1:16:59, C4P1 1:18:05).
- Un agente puede ajustar hiperparámetros en SageMaker solo (C4P1 1:18:39).
- Estructurá con etiquetas XML y JSON. En procesos desatendidos, estructurá el input (por ejemplo con regex) y mandá la salida a un destino (C4P1 1:19:13, C4P1 1:19:44, C4P1 1:20:52).
- **Catálogo de prompts versionado** en algún storage, para complementar el system prompt (C4P1 1:21:26, C4P1 1:21:58).
- **Caching:** si el output es el mismo aunque cambie el input, sacalo del caché; Converse tiene caché y se puede consultar. No cachees cuando los datos cambian todo el tiempo (por ejemplo, vienen de una API), sí cuando la base cambia poco (C4P1 1:22:33, C4P1 1:23:07, C4P1 1:23:41).
- Evitá instrucciones ambiguas ("resumilo, pero con toda la información") (C4P1 1:24:44).
- **Evaluar prompts:** un dataset de prueba, varias versiones del prompt, el pulgar arriba o abajo de los usuarios y un juez que evalúa. Según el resultado ajustás el RAG, cambiás de modelo o dividís un agente en dos (C4P1 1:25:17, C4P1 1:26:24, C4P1 1:26:58).

<details>
<summary>Preguntas de repaso del extra B (con respuestas)</summary>

1. **¿Qué permiten los parámetros de inferencia que no permite el fine tuning?** Ajustar el comportamiento del modelo en cada llamada sin redesplegar ni reentrenar.
2. **¿Qué efecto tiene bajar la temperatura?** El modelo da respuestas más probables y precisas, menos creativas.
3. **¿Cuáles son los tres criterios para elegir un modelo?** Calidad, latencia y costo.
4. **Nombrá tres formas de pagar menos en Bedrock que da la clase.** Prompt caching, batch inference, enrutar por tarea a modelos más chicos (también Spot, región más barata e inference profiles).
5. **¿Cuáles son las piezas de Bedrock que enumera?** Runtime, knowledge base, AgentCore y evaluación, con el modelo fundacional atrás.
6. **¿Por qué conviene un guardrail en lugar de filtrar con el system prompt del modelo grande?** Porque el guardrail es chico y barato, y bloquea antes de gastar cómputo y tokens en el modelo grande.
7. **¿Qué API recomienda para hablar con un modelo?** Converse, en lugar de InvokeModel.
8. **¿Qué partes tiene una llamada a Converse?** Modelo, system prompt, messages e inference config.
9. **¿Qué registra el invocation logging según la clase?** El prompt que entró y el que salió y los tokens consumidos; lo presenta junto con CloudTrail, que muestra quién usó qué API key.
10. **¿Qué presupuesto de tokens usa como ejemplo para un bot de turnos?** 500 tokens, con alerta al 90%.
11. **¿Cuándo no conviene cachear respuestas?** Cuando los datos de origen cambian todo el tiempo, por ejemplo si vienen de una API.

</details>

---

## Extra C. Bases vectoriales, RAG, datos y agentes
**Dónde:** C4P1 1:28:19, C4P1 1:29:26, C4P1 1:29:59, C4P1 1:32:43, C4P1 1:43:46, C4P1 1:49:09, C4P1 1:51:21, C4P1 1:53:36, C4P2 0:01, C4P2 2:14, C4P2 2:46, C4P2 8:13, C4P2 9:47, C4P2 12:06, C4P2 14:16, C4P2 17:36, C4P2 19:47, C4P2 34:15, C4P2 43:35

### Embeddings y bases vectoriales
- El modelo fundacional sabe hasta la fecha en que se entrenó. Para darle contexto del negocio inyectás información en el prompt (C4P1 1:28:19, C4P1 1:28:51).
- **Embeddings:** vectores que se guardan en una base para buscar de forma vectorial. En Bedrock el principal es Titan, también está Nova, y hay opciones propietarias. Titan es para texto y hay otro para imágenes, audio y video (multimodal) (C4P1 1:29:26, C4P1 1:39:55).
- **Búsqueda determinística contra vectorial:** una query SQL busca la coincidencia exacta y se terminó; la vectorial devuelve resultados con una probabilidad. Si buscás "Córdoba" con K igual te trae Córdoba, porque busca patrones y se aleja del coseno a medida que baja la similitud (C4P1 1:32:43, C4P1 1:33:50).
- Podés pedir registros con 20%, 80% o 100% de coincidencia; cuanto más alto, más estricto. El ejemplo es un hospital con procedimientos para sacar, borrar o anular turnos (C4P1 1:29:59, C4P1 1:31:08).
- Como la IA es probabilística, la base vectorial le da contexto con una probabilidad, por ejemplo 80% (C4P1 1:37:10).
- **Quién las usa:** buscadores, reconocimiento facial (la colección de Rekognition, Google Photos) (C4P1 1:38:49).
- Lo común es arrancar dejando que Titan arme los embeddings y después mejorar. Para evaluar, usá preguntas de prueba con respuesta conocida y medí a medida que agregás embeddings (C4P1 1:41:35, C4P1 1:42:07).
- Comenta que Google sacó una base "tridimensional" hace un año (dudoso) y que en más dimensiones hace falta GPU (C4P1 1:35:35).

### Dónde guardar los vectores
| Opción | Qué dice la clase |
|---|---|
| S3 Vectors | S3 como base vectorial. Muy barato para laboratorio, cobra por consultas, más lento que OpenSearch (C4P1 1:43:46) |
| OpenSearch | Usa RAM y cómputo especializado; "lo más rápido que hay" y según él lo usan Mercado Libre y Netflix (**para verificar**) (C4P1 1:43:46, C4P1 1:44:18) |
| Postgres con pgvector (RDS) | Tu propia base vectorial; también hay librerías chicas para correr local (C4P1 1:44:18) |
| Neptune | Grafos, sirve para GraphRAG (C4P1 1:44:50) |
| En knowledge bases | Menciona S3, OpenSearch, Aurora, Neptune, Pinecone (que nunca usó), Redis y "un DB" que no se entiende (C4P2 3:19) |

- **Chunks:** el documento no se embebe entero sino en fragmentos. Un chunk grande cuesta más embeber; uno muy fragmentado se dispersa. También ajustás cuántos resultados devuelve (C4P1 1:45:56, C4P1 1:53:36).
- **Búsqueda híbrida y reranking:** combinar algoritmos para la misma respuesta. El vector es bueno para probabilidades pero caro de procesar y de cargar; una base relacional tiene el dato disponible al instante (C4P1 1:49:09, C4P1 1:49:42, C4P1 1:50:15).
- **Costo serverless de S3:** dice "20 centavos por giga" (contradice la cifra de la clase 2, **para verificar**). Si no lo usás, no tenés consumo (C4P1 1:46:28).
- Opinión: Google AI Studio es muy bueno pero "caja negra"; Amazon te da las herramientas y no el producto terminado (C4P1 1:47:34).

### RAG paso a paso
1. Una app recibe la pregunta, busca palabras clave, consulta el vector y trae el contexto (retriever) (C4P1 1:51:21).
2. Arma los pasajes recuperados; es como una query en tiempo real (C4P1 1:52:27). El ejemplo es buscar facturas de jeringas en el hospital (C4P1 1:53:03).
3. El modelo responde con el contexto del vector, el system prompt y la pregunta (C4P1 1:54:41).
4. En el system prompt decidís qué hacer si la información no está: por ejemplo, para turnos responder solo con lo que hay, o directamente decir que no tiene la información (C4P2 0:01, C4P2 0:33).
5. Algunas knowledge bases, como la de AWS, devuelven también la ubicación del documento fuente (la URL del PDF) como cita (C4P2 0:33, C4P2 4:59).

### Knowledge bases de Bedrock
- Puede ser administrada o local. En la local generás vos los embeddings con Titan; en la administrada Titan arma embeddings y chunks, vos das los porcentajes, usás retrieve "y acá no hay código" (C4P2 1:06, C4P2 1:41, C4P2 2:14).
- **Data sources:** S3 (PDFs), Confluence, SharePoint, Salesforce, un crawler web o una API (C4P2 2:46).
- A gran volumen "se paga solo" frente a construirlo vos (C4P2 3:52).
- Es común una **IA intermedia**: un modelo más chico reformula la pregunta del usuario para buscar en la knowledge base (C4P2 4:27).
- Para datos estructurados, la knowledge base usa queries sobre Redshift o RDS, y puede apoyarse en el catálogo de Glue (C4P2 4:59, C4P2 5:31).
- **Bedrock Data Automation** transforma datos no estructurados (por ejemplo facturas PDF en S3 con formatos distintos) en la estructura que le pedís, sin integrar nada (C4P2 6:02).
- Hay evaluación con scoring de recuperación y de generación (C4P2 7:40).

**Fallas típicas de un RAG** (C4P2 8:13, C4P2 9:16): información mezclada, chunks cortados por un corte muy fino de tokens, contexto irrelevante, información no vigente (el ejemplo es un bot que aprende de tickets) y citas inventadas, con URLs que no existían.

**Cuándo no usar RAG** (C4P2 9:47, C4P2 10:21, C4P2 11:27): cuando no querés sobrecargar el contexto, cuando la información entra en el prompt (como el horario de turnos) o cuando no tenés grandes volúmenes (no son 40 PDFs ni 2 GB). Otra opción es hacer fine tuning con la información de la empresa. Un RAG siempre consume más tokens porque arma contexto en cada pregunta; preguntarle al modelo fundacional o a uno ajustado es mucho menos costoso en tokens.

### Datos para la IA
- Un agente tiene system prompt, tools, historial (Amazon llama "turnos" a las conversaciones) y tablas como contexto. Se mide en calidad, costo y seguridad (C4P2 12:06, C4P2 12:38).
- Advierte contra "meter IA en todos lados" sin pensar qué información usa (C4P2 13:10).
- **Lakehouse:** data lake (datos no estructurados, de distintos orígenes, sin sanitizar) más data warehouse (datos estructurados, más potente) (C4P2 14:16, C4P2 14:48, C4P2 15:22).
- **Athena:** pagás por consulta, usa S3 por detrás y lee CSV, JSON o Parquet con SQL. Es muy común junto a SageMaker y sirve para data science que no necesita tiempo real (C4P2 15:55, C4P2 16:27).
- **Arquitectura medallón:** bronce (crudo), silver (limpio, ordenado, segmentado) y gold (reducido y sumarizado, por ejemplo el forecast de venta del día). La IA debería trabajar sobre gold porque está sumarizado, no es sensible y puede cumplir compliance (C4P2 17:36, C4P2 19:15).
- **Riesgos de text to SQL:** prompt injection para que te dé el esquema, SQL libre, columnas expuestas o demasiadas filas. La mitigación es darle la query armada y que solo complete el WHERE, o limitarla a una tabla; es menos flexible pero más seguro (C4P2 19:47, C4P2 20:53, C4P2 22:30, C4P2 23:02).
- **Clasificadores y jueces:** XGBoost, Comprehend o SageMaker para analizar contenido, y un LLM como juez (por ejemplo Sonnet). Se arma una cadena donde un modelo genera, otro valida, otro revisa seguridad y otro el contexto (C4P2 26:24, C4P2 26:58).
- **Extracción estructurada con umbral por campo:** para una factura, el CUIT necesita un umbral muy alto (0,98) y la fecha también; los ítems pueden ir más bajos (C4P2 28:04, C4P2 28:38).

### Agentes
- **Permisos:** un API Gateway con límite de llamadas, IAM y una IA responsable que orquesta (C4P2 33:00).
- **Patrón multiagente:** "cotizame el mejor vuelo para mañana". Un orquestador lidera; un investigador consulta la API de vuelos; un cotizador consulta RDS (impuestos y condiciones); un comercial, un diseñador y un QA iteran hasta tener una respuesta válida. Cada agente puede usar un modelo distinto con un gasto distinto (C4P2 34:15, C4P2 37:34).
- **MCP:** la forma de declararle a un agente las fuentes o tools a las que accede, con un manifiesto del esquema o un método como get_vuelos (C4P2 38:08, C4P2 39:12).
- **Tratá a los agentes como usuarios.** Si uno accede a todo, un atacante le pregunta "qué tools tenés" y le ordena al cotizador cambiar precios. Si todos están en la misma red virtual puede haber movimiento lateral. Poné guardrails en cada salto, porque "si dejaste una puerta abierta, van a llegar" (C4P2 38:40, C4P2 41:21, C4P2 42:27, C4P2 43:00).

### La demo de la clase 4
**Dónde:** C4P2 43:35, C4P2 44:16, C4P2 45:31, C4P2 47:41, C4P2 48:45, C4P2 49:48, C4P2 50:50, C4P2 53:30, C4P2 55:12

1. Arquitectura: Lambda, Bedrock, DynamoDB y S3 Vectors, con una UI donde un agente accede a la capa gold o a la tabla de detalle (C4P2 43:35).
2. Pregunta "¿Cuántos días tengo para devolver un producto?": va a la knowledge base, busca en la política de devoluciones y consume 3000 tokens en total (C4P2 44:16).
3. Código: una Lambda con el agente, el handler, el system prompt, las fuentes y boto3; las tools están declaradas (por ejemplo consultar pedidos), o el agente arma la query solo (C4P2 45:31, C4P2 46:35, C4P2 47:06).
4. La knowledge base devuelve solo el párrafo relevante del documento, no el documento entero (C4P2 47:41).
5. Configuración: data source, vector en S3, índice, dimensión, float32 y metadata; ARN del modelo de embeddings Titan (C4P2 48:45, C4P2 49:16).
6. Menciona LangChain como base de estas herramientas y otro framework para lo agéntico cuyo nombre no se entiende; la tool config termina siendo una librería de LangChain (C4P2 49:48, C4P2 50:19).
7. "Cuáles son mis pedidos" contra la capa gold y contra la de detalle (bronce): la de detalle tardó 10% más y gastó muchos más tokens, aun con un dataset de muy pocos registros (C4P2 50:50, C4P2 51:53).
8. El repo trae notebooks para probar guardrails, que no se pueden probar en los labs de la Academy porque ahí no hay acceso a Bedrock (**para verificar**), pero sí en tu cuenta. Se despliega con CDK (infraestructura como código) y el README tiene la arquitectura (C4P2 53:30, C4P2 54:02).
9. Una segunda demo, pública, es la que usa con clientes de Craftech: login con token por teléfono; cuando el guardrail bloquea, el consumo de tokens es cero (C4P2 55:12, C4P2 56:17).

<details>
<summary>Preguntas de repaso del extra C (con respuestas)</summary>

1. **¿Qué diferencia hay entre una query SQL y una búsqueda vectorial?** La SQL busca una coincidencia exacta; la vectorial devuelve resultados por similitud, con una probabilidad.
2. **¿Qué modelo de embeddings nombra como principal en Bedrock?** Titan.
3. **¿Qué ventaja y qué desventaja tiene S3 Vectors frente a OpenSearch?** Es mucho más barato, pero más lento.
4. **¿Qué pasa si los chunks son muy chicos o muy grandes?** Muy chicos se dispersan o cortan la información; muy grandes cuestan más de embeber.
5. **Nombrá tres fallas típicas de un RAG.** Chunks cortados, contexto irrelevante o información no vigente, y citas inventadas.
6. **¿Cuándo no conviene un RAG?** Cuando la información entra en el prompt, cuando no hay grandes volúmenes o cuando no querés sobrecargar el contexto.
7. **¿Por qué un RAG gasta más tokens que preguntarle a un modelo ajustado?** Porque en cada pregunta agrega contexto recuperado al prompt.
8. **¿Sobre qué capa de la arquitectura medallón debería trabajar la IA?** Sobre la capa gold, sumarizada y sin datos sensibles.
9. **¿Cómo reducís el riesgo de text to SQL?** Dándole una query armada para que solo complete el WHERE o limitándola a una tabla.
10. **¿Por qué hay que tratar a los agentes como usuarios?** Porque pueden ser manipulados; cada uno debe tener solo los permisos que necesita y guardrails en cada paso.
11. **¿Qué mostró la demo al comparar la capa gold con la de detalle?** Que la de detalle tardó 10% más y consumió muchos más tokens.

</details>

---

## Cierre. Preguntas sobre herramientas y mercado laboral
**Dónde:** C4P2 58:07, C4P2 59:13, C4P2 1:00:18, C4P2 1:01:24, C4P2 1:02:32, C4P2 1:30:00

- **ClickHouse:** dice que tiene "40% menos de costo" que cualquier data warehouse y que se puede instalar en Amazon (**para verificar**) (C4P2 59:13, C4P2 1:01:24).
- **S3 para entrenar:** para guardar datasets y entrenar, S3 es el mejor según él; BigQuery con Colab también sirve (C4P2 1:00:18).
- **Combo recomendado:** SageMaker, S3 y Athena. Redshift es de los servicios más caros y lo vio pocas veces (Bancor, Naranja X); una empresa mediana lo resuelve con una base relacional grande o con Athena, aunque saber Redshift paga bien en la industria (C4P2 1:01:24).
- **Carrera:** importa más el criterio y la resolución de problemas que el lenguaje; los juniors la tienen complicada y un senior con IA rinde mucho más; el data scientist que entrene modelos específicos para el cliente y entienda el negocio va a ser valioso; las habilidades blandas y la plasticidad hacen la diferencia; "que no cunda el pánico" (C4P2 1:02:32 a C4P2 1:25:00).
- El repo de la demo es público y se compartió por Slack. Craftech da también otra diplomatura de AWS en la UNC (C4P2 1:30:00).

---

## Glosario

### Términos de AWS y ML
| Término | Qué es según la clase |
|---|---|
| S3 | Almacenamiento de objetos; centraliza datos, modelos y resultados |
| Bucket | Contenedor de S3; el nombre es único a nivel global |
| IAM | Permisos de quién accede a qué; los roles conectan servicios |
| ARN | Identificador de un recurso de AWS (aparece en bucket policies y embeddings) |
| CloudFormation | Lo que crea la cuenta y los recursos del lab |
| CDK | Infraestructura como código; se usa para desplegar el repo de la demo |
| CloudTrail | Auditoría de lo que pasa en la cuenta |
| CloudWatch | Logs, insights y métricas |
| Glue | Catálogo de datos y pipelines |
| Athena | Consultas SQL sobre archivos en S3, pagando por consulta |
| Redshift | Data warehouse |
| SageMaker AI | Servicio administrado para entrenar, desplegar y ajustar modelos |
| Notebook instance | Instancia con Jupyter en SageMaker |
| Lifecycle configuration | Script que configura la notebook al arrancar |
| Endpoint | Modelo hosteado como API en SageMaker |
| Batch transform | Inferencia por lotes sobre un conjunto de datos |
| Hyperparameter tuning | Búsqueda automática de hiperparámetros con muchos training jobs |
| Threshold (umbral) | Valor que convierte una probabilidad en una clase |
| Matriz de confusión, ROC | Herramientas para evaluar un clasificador |
| Pricing Calculator | Estimador de costos |
| Budgets | Alertas de presupuesto mensual |
| Cost Explorer | Análisis de costos, filtrable por tags |
| FinOps | Práctica de controlar y optimizar el gasto en la nube |
| — | Análisis de imágenes y caras preentrenado |
| Colección (collection) | Catálogo de caras en Rekognition |
| Bounding box | Recuadro con las coordenadas del objeto detectado |
| Lex | Chatbots de voz y texto |
| Intent | Intención que el bot reconoce |
| Alias | Despliegue de un bot de Lex |
| Cognito identity pool | Identidad que usa la web del lab para hablar con Lex |
| Polly, Transcribe, Translate, Comprehend | Texto a voz, voz a texto, traducción y análisis de texto |
| Bedrock | Catálogo y runtime de modelos fundacionales |
| Converse, InvokeModel | APIs para hablar con un modelo en Bedrock |
| Guardrails | Filtro de entrada y salida para modelos |
| Knowledge base | RAG administrado de Bedrock |
| Bedrock Data Automation | Pasa datos no estructurados a una estructura definida |
| AgentCore | Orquestación de agentes, MCPs y memoria |
| Embeddings | Representación vectorial de texto, imagen o audio |
| RAG | Generación aumentada con recuperación de contexto |
| Chunk | Fragmento de documento que se embebe |
| MCP | Forma de declararle a un agente las tools a las que accede |
| Token | Unidad mínima de entrada y salida de un modelo |
| Fine tuning | Ajuste de un modelo con datos propios |
| MoE | Mixture of experts |
| Lakehouse, medallón | Combinación de data lake y warehouse; capas bronce, silver y gold |
| Least privilege | Dar solo los permisos mínimos necesarios |

### Nombres que la transcripción deforma
| En la transcripción | Probablemente es |
|---|---|
| Deep Race | AWS DeepRacer |
| Textra | Amazon Textract |
| FCX | Amazon FSx |
| Resft, Rift, Res, RIP | Amazon Redshift |
| Regi | Dudoso; un servicio para millones de operaciones en milisegundos que no se puede identificar |
| Timestam | Amazon Timestream (dudoso) |
| Yam, esam | IAM |
| Sagem Maker, S Maker | SageMaker |
| UniFi Studio | SageMaker Unified Studio |
| Starlab | Start Lab |
| Steam Editor | Dudoso; algo que corre al final del entrenamiento del lab 3.1 (C1P2 1:35:06) |
| Comprehead, Comprehet head, comprejet | Amazon Comprehend |
| Poli | Amazon Polly |
| Transcrive, trust | Amazon Transcribe |
| Recognillo | Amazon Rekognition |
| reclamar el budget | Reclamar el badge (insignia) |
| face show | Dudoso; el nombre de su notebook del lab del módulo 5 (C2P2 1:01:16) |
| Ecodoc | Echo Dot (el dispositivo de Alexa más chico) |
| Droptech, Deloptec | Dudoso; empresa donde trabajaba cuando hizo la demo de Alexa (C3P1 21:44) |
| Wingler, Winclub, Wing Club | Winclap |
| Asian Core, Cord, agent Core | Amazon Bedrock AgentCore (en C4P1 41:47 dice "agent Core" con claridad) |
| Jumpstar, JStar | SageMaker JumpStart |
| Trade Newum | AWS Trainium |
| Transobre | AWS Transform (dudoso) |
| Kir…, Kira | Kiro |
| Brock, Bedro, Bedw, BRCK | Bedrock |
| Bedings, embeding | Embeddings |
| W race, W rail, Wrail, War Rails, Warray, Wrate | Guardrails |
| RAE, RAL, RAC, rack | RAG |
| Norge Base, no base | Knowledge base |
| BR Data Automas | Bedrock Data Automation |
| Atina | Amazon Athena |
| Neptun | Amazon Neptune |
| Pine Con | Pinecone |
| Lin, L chain | LangChain |
| trans | Dudoso; un framework para la parte agéntica (C4P2 49:48) |
| un DB | Dudoso; una de las bases vectoriales de knowledge base (C4P2 3:19) |
| glazers | Dudoso; posiblemente S3 Glacier (C4P2 56:50) |
| Last privilege | Least privilege |
| Fratching | Dudoso; dice que sirve para reducir costos justo antes de hablar de caché (C4P1 1:22:33) |
| advance prontation | Dudoso; un servicio o técnica de optimización de prompts que genera muchas respuestas (C4P1 1:26:58) |
| quid | CUIT (por el contexto de facturas) |
| Fable, Fabel, Fabel 51 | Dudoso; nombre de un modelo que presenta como el más caro y nuevo |
| Opus 5, Opus 4.8, OP 48 | Dudoso; versiones de Claude Opus que habría que confirmar |
| Luna, Sol | Dudoso; nombres de modelos que atribuye a OpenAI |
| Nova Pro, Premiere | Probablemente Amazon Nova Pro y Nova Premier (dudoso) |
| Sora 2.5 | Dudoso; versión de Sora de OpenAI |
| Click House | ClickHouse |
| BQU | BigQuery |
| Google base tridimensional | Dudoso; no se entiende a qué producto se refiere (C4P1 1:35:35) |
