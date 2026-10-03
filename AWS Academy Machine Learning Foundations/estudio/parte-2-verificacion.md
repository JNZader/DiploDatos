# Segunda parte: "AWS Academy Machine Learning Foundations", con material externo

**Esta es la continuación de** `apunte-de-estudio.md` y `guia-de-implementacion.md` (las ocho grabaciones del curso AWS Academy Machine Learning Foundations publicadas en el canal de FAMAF UNC, dictadas por Fabián "Hanu" Hanuseski, CTO de Craftech, entre el 28/08/2026 y el 05/09/2026). Esos dos archivos resumen lo que dice el curso. Esta segunda parte suma material externo para verificar las cifras y afirmaciones que el docente da de memoria, resolver los nombres que la transcripción automática deformó, sumar mejoras concretas para implementar y para estudiar, y marcar dónde el enfoque tiene límites. Revisé todo entre el 01/10/2026 y el 02/10/2026. Solo cito páginas que abrí; cuando una página no cargó y la leí por otra vía (por ejemplo, el JSON de precios que usa la propia página), lo digo.

> Cómo leer esto: cuando digo "el curso" o "el docente" me refiero a lo que dijo Hanuseski en las clases. Las marcas de tiempo usan la etiqueta de cada grabación (C1P1 es la clase 1, parte 1, y así hasta C4P2) y llevan al minuto exacto en la grabación. Cuando digo "sugerencia" es una idea mía que combina fuentes, no algo que diga una fuente puntual. Los ejemplos de código y los cálculos que no tienen fuente son míos. Casi todas las fuentes son del propio AWS, que tiene interés en que uses sus servicios; lo marco cuando importa.

---

## Checklist actualizado (curso + mejoras)

1. Antes de repetir una cifra de la clase, revisala en la página oficial, porque varias estaban desactualizadas o mal recordadas: la capa gratuita de Rekognition es de 1.000 imágenes por mes en cada grupo de APIs (no 5.000) y la retención de Kinesis Video Streams vale 0 por defecto y se configura desde 1 hora.
2. No uses SageMaker Model Monitor en un proyecto nuevo: AWS lo cerró a clientes nuevos y propone reemplazarlo con MLflow, Evidently AI, QuickSight y CloudWatch, todo dentro de tu cuenta.
3. No planifiques nada sobre Amazon Forecast ni sobre Timestream for LiveAnalytics: el primero ya no acepta clientes nuevos y el segundo tiene aviso de fin de soporte (AWS recomienda Timestream for InfluxDB).
4. Si tu cuenta es nueva, contá con la capa gratuita actual (hasta USD 200 en créditos desde el 15/07/2025, con un plan Free de 6 meses) y no con los límites viejos de "5 GB y 100.000 requests" de S3.
5. Configurá Budgets con alertas y Cost Anomaly Detection el primer día, sabiendo que la detección de anomalías puede tardar hasta 24 horas y necesita unos 10 días de historia de un servicio nuevo.
6. Usá la API Converse de Bedrock como punto de entrada por defecto, porque te deja cambiar de modelo sin reescribir código, y dejá InvokeModel para cuando necesites un parámetro propio de un modelo.
7. Activá el prompt caching en los prompts largos que se repiten, porque en Bedrock las lecturas de caché se cobran con descuento (no "como si no hubiera caché"), y recordá que no funciona con inferencia por lotes.
8. Elegí la modalidad de cobro según la urgencia: lotes con 50% de descuento en modelos seleccionados, el tier Flex con 50% de descuento, el estándar, o Priority con 75% de recargo.
9. Si tus datos no pueden salir de una geografía (el caso del Banco Central que menciona el docente), no uses el perfil de inferencia Global y restringí regiones con una SCP o una política IAM, porque la inferencia entre regiones procesa el pedido en otra región.
10. Leé la política de datos de cada servicio por separado: Bedrock no usa tus prompts para entrenar ni se los muestra al proveedor del modelo, pero Comprehend puede guardar tu contenido para mejorar sus modelos y AgentCore puede guardarlo para mejorar tu propio servicio.
11. Configurá Guardrails por caso de uso, con los cuatro niveles (NONE, LOW, MEDIUM, HIGH) separados para entrada y salida, y probalos con frases reales en rioplatense antes de confiar en ellos, porque el GCBA terminó usando un clasificador propio en Boti.
12. Si usás Guardrails con agentes, acordate de que no evalúan los resultados de las tools ni sus argumentos, y que en streaming asincrónico no enmascaran PII.
13. Antes de lanzar un RAG, armá un set de preguntas reales y corré un job de evaluación de Bedrock (solo recuperación, y recuperación más generación) comparando al menos dos modelos de embeddings, porque en el caso de Boti Cohere Multilingual le ganó a Titan V2 en español.
14. Elegí el vector store por patrón de uso: S3 Vectors para consultas poco frecuentes y baratas, OpenSearch cuando necesitás baja latencia o vectores binarios, y Aurora con pgvector si ya tenés Postgres.
15. Para identidad con documentos argentinos, no cuentes con una función "de DNI": Textract AnalyzeID está pensado para documentos de EE. UU., así que combiná Face Liveness con CompareFaces y un OCR general, y validalo con tus propios documentos.
16. Revisá tu arquitectura con la Machine Learning Lens y la Generative AI Lens de Well-Architected (las dos son de noviembre de 2025) antes de pasar a producción.
17. Escribí el código de tus agentes con un framework portable (Strands Agents, LangGraph) y desplegalo en AgentCore si te conviene, para que el día que quieras salir de AWS no tengas que reescribir todo.
18. Si vas a rendir una certificación, el AI Practitioner (AIF-C01) se puede rendir en español latinoamericano; para Machine Learning Engineer Associate, la versión en inglés de MLA-C01 se pudo rendir hasta el 28/09/2026 y desde el 29/09/2026 está en beta MLA-C02, que suma Bedrock, RAG y agentes.
19. Aprovechá que AWS Academy les da a los estudiantes 12 meses de Skill Builder sin costo, y usalo para los exámenes de práctica.
20. Mirá con ojo crítico las cifras de rendimiento y ahorro: "hasta 90%", "hasta 99%" y "hasta 30%" son afirmaciones de AWS, y el "75% menos que Redshift" es de ClickHouse.

---

## Versión completa

### 1. Los datos del curso, verificados

El docente da muchas cifras de memoria y aclara varias veces que hay que revisarlas. Las revisé y las ordené de la corrección más importante a la menos importante. "Sí" quiere decir que la fuente lo confirma, "En parte" que es correcto con matices importantes, "No" que la fuente lo contradice, y "No verificable" que no encontré una fuente primaria que lo confirme o lo niegue.

| Afirmación | Resultado | Matiz | Fuente |
|---|---|---|---|
| Los datos que mandás a un modelo por API pueden terminar en el servidor del proveedor y los modelos propietarios reentrenan con tu información (C4P1 17:37, C4P1 21:24) | No, para Bedrock | Bedrock dice que los proveedores de modelos no tienen acceso a tus prompts ni a las respuestas, que no se usan para entrenar ningún modelo y que Converse no guarda el contenido. Lo que sí es cierto: con inferencia entre regiones el pedido se procesa en otra región (importa para residencia de datos), y otros servicios de IA de AWS tienen otra política. Comprehend "may store your content to continuously improve" sus modelos preentrenados, y AgentCore puede guardar tu contenido para mejorar tu propia experiencia (no la de otros clientes). La advertencia del docente aplica a las apps de consumo y a algunos servicios, no a Bedrock. | [Bedrock, protección de datos](https://docs.aws.amazon.com/bedrock/latest/userguide/data-protection.html); [FAQ de Bedrock](https://aws.amazon.com/bedrock/faqs/); [Comprehend, qué es](https://docs.aws.amazon.com/comprehend/latest/dg/what-is.html); [AgentCore, qué es](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html) |
| Los modelos privados cachean el prompt pero te cobran como si no; con un modelo local ahorrás hasta 90% (C4P1 32:23) | No | En Bedrock las lecturas de caché se cobran a una tarifa reducida (en GPT-5.6, 90% menos que la entrada normal) y la escritura cuesta 1,25 veces la entrada. El TTL es de 5 minutos o 1 hora en Claude y de 30 minutos en GPT-5.6. Hay caché implícito y explícito, los tokens leídos de caché no cuentan para el límite de tasa, y no funciona con inferencia por lotes. El "90%" existe, pero es el descuento de la API, no el de un modelo local. | [Bedrock, prompt caching](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html) |
| SageMaker sirve para monitorear modelos en producción (implícito en todo el bloque de MLOps del curso) | Desactualizado | SageMaker Model Monitor "is no longer open to new customers": los clientes existentes siguen y no va a tener funciones nuevas. AWS publica siete soluciones open source en `aws-samples` (SageMaker AI MLflow Apps con Evidently AI, más QuickSight y CloudWatch) como reemplazo, incluida una para monitorear LLMs. | [Cambio de disponibilidad de Model Monitor](https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor-availability-change.html) |
| La capa gratuita de Rekognition es de unas 5.000 imágenes (C2P2 1:17:55) | No | Durante los 12 meses de capa gratuita podés analizar 1.000 imágenes por mes en las APIs del Grupo 1 y otras 1.000 en las del Grupo 2, y guardar 1.000 vectores de caras. Video: 60 minutos por mes. Fuera de la capa gratuita, imagen desde USD 0,001 por imagen, Custom Labels a USD 1 por hora de entrenamiento y USD 4 por hora de inferencia, Face Liveness a USD 0,015 por chequeo. Las cuentas creadas desde el 15/07/2025 tienen el modelo de créditos. | [Precios de Rekognition](https://aws.amazon.com/rekognition/pricing/) (volví a abrirla el 02/10/2026 para confirmar) |
| Rekognition tiene una función "solo para DNI" (C2P2 1:08:39) | No, tal como está dicho | Lo que existe es Face Liveness (un puntaje de 0 a 100 de que hay una persona real frente a la cámara, más una imagen de referencia) que se combina con CompareFaces o SearchFacesByImage para comparar contra la foto del documento. La extracción de datos de documentos de identidad es de otro servicio, Textract AnalyzeID, y su documentación habla de pasaportes y licencias emitidos por el gobierno de EE. UU. Para un DNI argentino no encontré una función específica. | [Rekognition, Face Liveness](https://docs.aws.amazon.com/rekognition/latest/dg/face-liveness.html); [Textract, documentos de identidad](https://docs.aws.amazon.com/textract/latest/dg/how-it-works-identity.html) |
| Los modelos se habilitan de a poco por cuenta y región, y si no los usás uno o dos meses se deshabilitan (C4P1 47:09, C4P1 47:43) | Desactualizado; lo de deshabilitarse no lo encontré | Hoy el acceso a los modelos serverless está habilitado por defecto si tenés los permisos de AWS Marketplace: la primera invocación dispara la suscripción, que puede tardar hasta 15 minutos. Anthropic pide un formulario de primer uso. Para bloquear modelos se usan SCP o políticas IAM. La página no dice nada de que un modelo se deshabilite por falta de uso. Las cuotas por región sí existen, y por eso tiene sentido lo de que en empresa "no está en todas las regiones". | [Bedrock, acceso a modelos](https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html) |
| El inference profile manda el pedido a la región más barata en ese momento, y va a durar poco (C4P1 36:53, C4P1 37:25) | No | La inferencia entre regiones existe para tener más capacidad (throughput), no para buscar precio: los perfiles geográficos (US, EU, APAC) cobran el precio de la región de origen y no hay costo de ruteo. El perfil Global da "aproximadamente 10%" de ahorro. El tráfico va por la red de AWS y CloudTrail registra en qué región se procesó (`inferenceRegion`). Lo de "va a durar poco" es una opinión del docente y no se puede verificar. | [Bedrock, inferencia entre regiones](https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html) |
| Kinesis Video Streams guarda el video una o dos horas, "creo que hasta 24" (C2P2 52:12) | No | `DataRetentionInHours` vale 0 por defecto, que significa que el stream no persiste datos (solo queda un buffer de 5 minutos o 200 MB). Si querés retención, el mínimo es 1 hora y la API no fija un máximo en esa página. En la documentación del modelo de datos, 24 horas aparece como valor típico de ejemplo. | [KVS, CreateStream](https://docs.aws.amazon.com/kinesisvideostreams/latest/dg/API_CreateStream.html) (revisada otra vez el 02/10/2026); [KVS, modelo de datos](https://docs.aws.amazon.com/kinesisvideostreams/latest/dg/how-data.html) |
| SageMaker tiene unos 8 años y fue el primer servicio cloud de ML (C2P1 42:42) | En parte: la edad sí, lo de "primero" no | SageMaker se lanzó el 29/11/2017 en re:Invent, así que al momento de la clase tenía 8 años y 9 meses. Pero Azure Machine Learning ya tenía disponibilidad general el 18/02/2015. | [Blog de AWS, lanzamiento de SageMaker](https://aws.amazon.com/blogs/aws/sagemaker/); [Blog de Microsoft, 18/02/2015](https://blogs.microsoft.com/blog/2015/02/18/new-azure-services-help-people-realize-possibilities-big-data/) |
| Amazon Q cambió a Kiro hace un par de meses, y Kiro tiene menos de un año (C3P2 18:39, C3P2 28:57) | En parte | Kiro se presentó el 14/07/2025, así que a la fecha de la clase (04/09/2026) tenía casi 14 meses. No fue un simple cambio de nombre: el 30/04/2026 AWS anunció que los plugins de IDE y las suscripciones pagas de Amazon Q Developer llegan a fin de soporte el 30/04/2027, que desde el 15/05/2026 no hay altas nuevas, que Opus 4.7 y los modelos posteriores solo están en Kiro, y que la transformación de código pasa a AWS Transform. Q en la consola de AWS y Q para Slack y Teams siguen igual. | [Blog de AWS, fin de soporte de Q Developer](https://aws.amazon.com/blogs/devops/amazon-q-developer-end-of-support-announcement/); [Kiro, presentación](https://kiro.dev/blog/introducing-kiro/) |
| Para el examen de Machine Learning Engineer hay cursos en español en Skill Builder (C2P2 1:20:09) | En parte, y cambió el examen | La versión en inglés de MLA-C01 se pudo rendir hasta el 28/09/2026. Desde el 29/09/2026 está en beta MLA-C02: solo en inglés, 85 preguntas, 170 minutos, USD 75 durante la beta, y suma Bedrock, RAG, IA agéntica y modelos fundacionales. La fecha de disponibilidad general todavía no está definida. El AI Practitioner (AIF-C01) sí está en español latinoamericano. La página de Skill Builder no cargó (llegó vacía), así que no pude verificar qué cursos hay en español. | [MLA, página de la certificación](https://aws.amazon.com/certification/certified-machine-learning-engineer-associate/); [AIF-C01, página de la certificación](https://aws.amazon.com/certification/certified-ai-practitioner/) |
| Forecast está deprecado, ahora todo eso se corre dentro de SageMaker (C1P2 1:24:30, C2P2 24:46) | En parte | La documentación dice que Forecast "is no longer available to new customers" y que los clientes existentes pueden seguir usándolo. La página de producto, en cambio, no muestra ningún aviso. En SageMaker existe el algoritmo DeepAR para series de tiempo; no abrí la documentación de SageMaker Canvas, así que no confirmo cuál es el reemplazo oficial. | [Forecast, documentación](https://docs.aws.amazon.com/forecast/latest/dg/what-is-forecast.html); [Forecast, página de producto](https://aws.amazon.com/forecast/); [SageMaker, algoritmos integrados](https://docs.aws.amazon.com/sagemaker/latest/dg/algos.html) |
| Nova es una versión mejorada de Polly, más generativa y con tonadas (C3P1 1:04:48) | No | Son productos distintos. Polly es texto a voz y tiene un motor generativo (un transformer de mil millones de parámetros) con 43 voces, entre ellas español de México (Andrés, Mía), de España y de EE. UU.; no hay voz de Argentina. Nova Sonic es un modelo de voz a voz en Bedrock, pensado para conversar en tiempo real con streaming bidireccional y tools; según su ficha soporta inglés, español, alemán, francés e italiano, no admite fine tuning y no deja cambiar tono ni velocidad. | [Polly, voces generativas](https://docs.aws.amazon.com/polly/latest/dg/generative-voices.html); [Nova Sonic, ficha de servicio](https://docs.aws.amazon.com/ai/responsible-ai/nova-sonic/overview.html) |
| Comprehend ahora usa modelos fundacionales además de NLP clásico (C3P1 1:08:38) | No se confirma | La documentación describe modelos preentrenados, modelos personalizados de clasificación y entidades, y AutoML. No menciona modelos fundacionales. Sí aclara que Comprehend puede guardar tu contenido para mejorar sus modelos. | [Comprehend, qué es](https://docs.aws.amazon.com/comprehend/latest/dg/what-is.html) |
| Guardrails consume "el 4% de los tokens" (C4P1 45:32) | No verificable, y la unidad es otra | Guardrails no se cobra por tokens sino por unidades de texto (1 unidad equivale a 1.000 caracteres): los filtros de contenido de texto y los temas denegados cuestan USD 0,15 cada 1.000 unidades, la detección de PII USD 0,10, el contextual grounding USD 0,10, y los filtros de palabras y de regex son gratis. El costo relativo depende del modelo: con uno barato puede costar más el guardrail que la inferencia (ver sección 5). | [Precios de Bedrock](https://aws.amazon.com/bedrock/pricing/) (la bajé con curl porque la tabla se arma con JavaScript) |
| Guardrails tiene niveles low, medium y high, y uno sin validación (C4P1 43:56) | Sí | Los niveles son NONE, LOW, MEDIUM y HIGH, por categoría y por separado para entrada y salida, con acción de bloquear o solo detectar. Hay dos tiers (Classic y Standard; Standard requiere inferencia entre regiones). No evalúan resultados ni argumentos de tools. | [Guardrails, filtros de contenido](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-content-filters.html) |
| En Bedrock están casi todos los modelos, excepto Gemini (C3P1 15:25) | Sí | Google aparece solo con los modelos abiertos Gemma 3 y Gemma 4. Hay modelos de Anthropic, OpenAI (incluidos GPT-6 y gpt-oss), Amazon, Meta, Mistral, DeepSeek, Qwen, Kimi, MiniMax, NVIDIA, xAI, GLM, Cohere, Writer, TwelveLabs, Stability y AI21. La FAQ de Bedrock está más vieja que la lista de modelos; conviene mirar las model cards. | [Bedrock, model cards](https://docs.aws.amazon.com/bedrock/latest/userguide/model-cards.html) |
| InvokeModel "ya medio no se usa"; ahora es Converse, y el parámetro system cambió "desde Opus 4" (C4P1 48:17, C4P1 50:27) | En parte | Converse es la API recomendada para conversar porque es la misma para todos los modelos que soportan mensajes, y tiene campos para system, configuración de inferencia, guardrails, tools, puntos de caché y tier de servicio. InvokeModel sigue documentado y vigente. Además existen APIs compatibles con OpenAI (Chat Completions y Responses) en el endpoint `bedrock-mantle`. Lo de "desde Opus 4" no lo pude verificar. | [Bedrock, Converse](https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference.html) |
| La inferencia por lotes es más barata si mandás todo junto (C4P1 32:55) | Sí | Batch cuesta 50% menos para modelos seleccionados. Además hay tiers: Flex con 50% de descuento y Priority con 75% de recargo. | [Precios de Bedrock](https://aws.amazon.com/bedrock/pricing/) |
| Hay herramientas de Amazon que eligen el modelo y dan la misma respuesta con 30% menos (C4P1 6:04) | Sí, como afirmación de AWS | Intelligent Prompt Routing cuesta USD 1 cada 1.000 pedidos y AWS dice que ahorra "hasta 30%". Es una cifra del proveedor, no una medición independiente. | [Precios de Bedrock](https://aws.amazon.com/bedrock/pricing/) |
| S3 cuesta unos 23,55 USD por TB (C2P1 52:16) | Sí | S3 Standard en us-east-1 cuesta USD 0,023 por GB-mes en los primeros 50 TB, después 0,022 y desde 500 TB 0,021. 1.024 GB por 0,023 dan 23,55. La tabla de la página no cargó por WebFetch; saqué los precios del JSON que usa la propia página. | [Precios de S3](https://aws.amazon.com/s3/pricing/) |
| S3 serverless sale "20 centavos por giga" (C4P1 1:46:28) | En parte, es otra cosa | En S3 Vectors la carga (PUT) cuesta USD 0,20 por GB, el almacenamiento USD 0,06 por GB-mes y las consultas USD 2,50 por millón. No contradice el 23,55 por TB de S3 Standard: es otro producto y otro concepto de cobro. AWS dice que S3 Vectors baja "hasta 90%" el costo de un vector store; es cifra del proveedor. | [Precios de S3](https://aws.amazon.com/s3/pricing/) |
| La capa gratuita de S3 es de 5 GB y 100.000 requests (C2P1 50:03) | Desactualizado | Desde el 15/07/2025 las cuentas nuevas reciben hasta USD 200 en créditos (100 al registrarte y 100 más por actividades), con un plan Free de 6 meses o hasta agotar los créditos. Los límites por servicio que menciona el docente eran de la capa gratuita anterior y no los vi en la página actual. | [Capa gratuita de AWS](https://aws.amazon.com/free/) |
| Hay 200 de crédito al principio (C2P1 50:38) | Sí | Hasta USD 200 para cuentas nuevas desde el 15/07/2025; los créditos vencen a los 12 meses. | [Capa gratuita de AWS](https://aws.amazon.com/free/) |
| S3 cifra por defecto y ya no se puede elegir no cifrar (C1P1 1:54:22) | Sí | Desde el 05/01/2023 todo objeto nuevo se cifra con SSE-S3 (AES-256) sin costo, y no se puede desactivar. Los objetos que ya existían antes no se cifraron solos. | [S3, FAQ de cifrado por defecto](https://docs.aws.amazon.com/AmazonS3/latest/userguide/default-encryption-faq.html) |
| Virginia y Ohio son las regiones más baratas y donde salen primero los modelos (C1P2 5:44, C1P2 6:16) | En parte | En S3 Standard, Virginia cuesta lo mismo que Oregon, Irlanda, España y Estocolmo, y Malasia, Taipei y Tailandia son un poco más baratas (USD 0,0225). São Paulo es 76% más cara (USD 0,0405). No verifiqué la disponibilidad de cada modelo de Bedrock por región, así que esa parte queda sin confirmar. | [Precios de S3](https://aws.amazon.com/s3/pricing/) |
| El hosting de sitio estático en S3 no tiene costo extra (C3P1 2:04:27) | En parte | No vi un cargo específico por la función, pero pagás almacenamiento, requests y transferencia (los primeros 100 GB por mes de salida a internet son gratis). La documentación hoy recomienda Amplify Hosting o CloudFront, y para HTTPS o buckets con SSE-KMS hace falta CloudFront. Lo de "sin costo extra" es inferencia mía a partir de las dos páginas. | [S3, sitio estático](https://docs.aws.amazon.com/AmazonS3/latest/userguide/WebsiteHosting.html); [Precios de S3](https://aws.amazon.com/s3/pricing/) |
| En noviembre es re:Invent y suelen cambiar la interfaz (C3P1 1:50:08) | En parte | re:Invent 2026 es del 30/11 al 04/12 en Las Vegas. Lo de la interfaz es una anécdota y no se puede verificar. | [re:Invent](https://aws.amazon.com/events/reinvent/) |
| Hay unos "204" algoritmos integrados (C1P2 1:22:07) | No verificable | La lista oficial tiene unos 22 algoritmos integrados (XGBoost, Linear Learner, k-NN, K-Means, PCA, DeepAR, BlazingText, Object Detection, entre otros) y JumpStart agrega modelos preentrenados para 15 tipos de problema. Puede que haya dicho "de 2024"; no se escucha claro. | [SageMaker, algoritmos integrados](https://docs.aws.amazon.com/sagemaker/latest/dg/algos.html) |
| ClickHouse sale 40% menos que cualquier warehouse (C4P2 59:13) | No verificable, y hay conflicto de interés | La página de ClickHouse que compara con Redshift habla de "75% de reducción de costo" y de un cliente (Rokt) que paga tres veces menos. Es material de marketing del propio proveedor, con sus propios benchmarks. El 40% no aparece. | [ClickHouse contra Redshift](https://clickhouse.com/comparison/redshift) |
| OpenSearch es lo más rápido y lo usan Mercado Libre y Netflix (C4P1 1:44:18) | No verificado | No abrí casos de Mercado Libre o Netflix con OpenSearch. Lo que sí dice la documentación de Knowledge Bases: OpenSearch (Serverless o Managed) es el único vector store con vectores binarios, y S3 Vectors está pensado para consultas poco frecuentes con latencia por debajo del segundo. Eso coincide con la idea del docente de que S3 Vectors es más barato y más lento. | [Bedrock, vector stores para Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-setup.html) |
| Redshift es "carísimo" (C4P2 1:01:24) | Opinión | No comparé precios de Redshift. Depende de la carga y del modo (provisionado o serverless). | Ninguna |
| Una instancia con 1.152 GB de RAM por unos USD 250 por mes, y "estamos por la M6" (C2P2 14:28, C2P2 7:50) | No verificable, muy dudoso | El JSON de precios de SageMaker no cargó y no pude confirmar ninguna de las dos cosas. Por el orden de magnitud de los precios de otras instancias, 1.152 GB por USD 250 al mes es muy improbable; revisalo en la calculadora antes de usarlo. | Ninguna (la fuente no cargó) |
| Cada llamada a OpenAI cuesta unos 5 centavos de dólar, y OpenAI tiene cuotas de 100 pedidos por minuto y ventanas de 5 horas (C1P1 1:04:49, C4P1 38:25) | No verificado | No abrí las páginas de precios ni de límites de OpenAI. El costo por llamada depende del modelo y de los tokens, así que "5 centavos" no es una cifra fija. | Ninguna |
| La plataforma queda abierta hasta el "31 de noviembre", se puede extender hasta 4 meses, y los exámenes conviene tenerlos para el 28 de septiembre (C1P1 1:17:08, C1P1 1:19:53, C3P1 0:02) | No verificable | Son fechas internas del curso. El 31 de noviembre no existe, así que probablemente quiso decir 30 de noviembre. La página de AWS Academy confirma que ML Foundations tiene unas 20 horas de contenido y que los estudiantes reciben 12 meses de Skill Builder, pero no habla de plazos. | [AWS Academy](https://aws.amazon.com/training/awsacademy/) |

**Lo más importante para corregir en el apunte.** Las correcciones que cambian decisiones son cinco: la política de datos de Bedrock (es más protectora de lo que dijo el docente, pero no vale igual para todos los servicios), el prompt caching (sí ahorra), Model Monitor y Forecast (ya no aceptan clientes nuevos), la capa gratuita (créditos en lugar de límites por servicio y 1.000 imágenes de Rekognition), y el examen MLA (si estudiás en inglés, ahora es MLA-C02).

### 2. Nombres y dudas de la transcripción, resueltos

| En la transcripción | Resultado | Cómo lo resolví |
|---|---|---|
| "Fable", "Fabel" (C1P1 40:21) | Claude Fable 5 y Claude Fable 5.1, de Anthropic | Aparecen en las model cards de Bedrock, junto con Mythos 5 y 5.1. |
| "Opus 5", "OP 48" (C4P1 6:04) | Claude Opus 5 y Claude Opus 4.8 | Están los dos en las model cards de Bedrock y en la página de precios de Kiro. |
| "Luna", "Sol" | GPT-5.6 Sol, Terra y Luna, y GPT-6 Sol y Luna, de OpenAI | Están en las model cards de Bedrock; Kiro también ofrece GPT-5.6 Sol, Terra y Luna. |
| "Nova Pro o el Premiere" (C4P1 36:14) | Amazon Nova Pro y Amazon Nova Premier | Están en las model cards; Nova Premier figura además como modelo evaluador en la evaluación de RAG. |
| "Timestam" (C1P1 1:42:18) | Amazon Timestream, base de datos de series de tiempo | La [página de producto](https://aws.amazon.com/timestream/) existe. Ojo: Timestream for LiveAnalytics tiene aviso de fin de soporte y AWS recomienda Timestream for InfluxDB. Además, es una base de series de tiempo, no un servicio de streaming (eso es Kinesis). |
| "Transobre" (C3P2 33:25) | AWS Transform | Lo nombran la página de la capa gratuita y el anuncio del fin de Q Developer, que dice que la transformación de código pasa a AWS Transform. El ejemplo del docente (migrar COBOL de bancos) coincide con ese servicio. |
| "glazers" (C4P2 56:50) | Amazon S3 Glacier, probablemente | En el contexto (S3 Tables, Iceberg, almacenamiento) encaja con [Glacier](https://aws.amazon.com/s3/storage-classes/glacier/), que tiene tres clases: Instant Retrieval (milisegundos), Flexible Retrieval (de minutos a 12 horas) y Deep Archive (USD 0,00099 por GB-mes, de 12 a 48 horas). |
| "un DB" (C4P2 3:19) | MongoDB Atlas | El docente enumeró los vector stores en el mismo orden que la documentación de Knowledge Bases, y el último de esa lista es MongoDB Atlas. |
| "trans" (C4P2 49:48) | Strands Agents, probablemente | Es el SDK open source de AWS para agentes (Python y TypeScript) y AgentCore lo lista entre los frameworks soportados. Lo nombró junto a LangChain, como "otro framework para agéntico". |
| "advance prontation" (C4P1 1:26:58) | Advanced Prompt Optimization de Bedrock | La página de precios describe un modo que usa LLMs para reescribir y evaluar prompts en bucle (API `CreateAdvancedPromptOptimizationJob`), igual a lo que describe el docente ("genera muchas respuestas"). El modo simple cuesta USD 0,03 cada 1.000 tokens. |
| "Asian Core", "Cord" (C1P2 1:25:24, C4P1 2:14) | Amazon Bedrock AgentCore | [Documentación de AgentCore](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html). |
| "BR Data Automas" (C4P2 6:02) | Bedrock Data Automation | Aparece en la [FAQ de Bedrock](https://aws.amazon.com/bedrock/faqs/). |
| "Kir", "Kiro" | Kiro | La [presentación de Kiro](https://kiro.dev/blog/introducing-kiro/) y su [página de precios](https://kiro.dev/pricing/). |
| "Regi" (C1P1 1:42:18) | Sin resolver | Lo describe como "un monstruo, millones de operaciones en milisegundos" que usa una empresa de Buenos Aires. Los candidatos razonables son DynamoDB o ElastiCache (Redis), pero el audio no alcanza para decidir y no encontré nada que lo confirme. |
| "Fratching" (C4P1 1:22:33) | Sin resolver | Describe un caché que reutiliza respuestas cuando el input se parece (caché semántico). No es el prompt caching de Bedrock, que funciona por prefijo exacto. No encontré un servicio con ese nombre. |
| "Sora 2.5", "salió en agosto" (C3P2 6:02) | Sin resolver | No abrí ninguna página de OpenAI sobre Sora, así que no confirmo ni la versión ni la fecha. Sora no está en Bedrock. |
| "Google base tridimensional" (C4P1 1:35:35) | Sin resolver | Por el contexto (búsqueda vectorial, CPU contra GPU) podría ser una explicación de espacios de embeddings, pero no identifiqué el producto. |
| "face show" (C2P2 1:01:16), "Droptech" (C3P1 21:44), "Steam Editor" | Sin resolver | Son nombres de un lab propio del docente y de un cliente o proyecto suyo; no hay fuente pública para confirmarlos. |

### 3. Revisar la arquitectura con Well-Architected: la lente de ML y la de IA generativa

**Qué dice el curso.** El docente insiste en arrancar por el problema de negocio, en medir costo, calidad y seguridad, y en no usar "una bazuca para matar una hormiga". Lo hace con ejemplos de clientes, pero sin una lista de control que se pueda repetir.

**Qué suma el material externo.** AWS publica dos lentes del Well-Architected Framework que convierten esas ideas en preguntas concretas. La [Machine Learning Lens](https://docs.aws.amazon.com/wellarchitected/latest/machine-learning-lens/machine-learning-lens.html) (actualizada el 19/11/2025) recorre el ciclo de vida del ML clásico (formular el problema, datos, desarrollo, despliegue, monitoreo) con los seis pilares, y aclara que su guía es "cloud- and technology-agnostic", o sea que la podés usar aunque no estés en AWS. La [Generative AI Lens](https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/generative-ai-lens.html) (misma fecha) hace lo mismo para IA generativa: incluye riesgos como la agencia excesiva de los agentes, el costo de los vector stores y de los agentes, y la ingeniería de prompts como palanca de costo, y cubre Bedrock, SageMaker y Q. Las dos se pueden cargar como lentes en la Well-Architected Tool de la consola.

**Cómo implementarlo.**
1. Antes de pasar a producción, abrí la Well-Architected Tool, creá un workload y sumale la lente que corresponda (ML Lens para el modelo de SageMaker del curso, GenAI Lens para el chatbot con Bedrock).
2. Contestá las preguntas con el equipo y anotá los riesgos altos como tareas.
3. **Sugerencia:** usá las preguntas de la GenAI Lens como checklist de las secciones 11 a 17 de la guía de implementación (elegir modelo, tokens, guardrails, RAG, agentes, observabilidad), porque cubren lo mismo con otro orden.
4. **Sugerencia:** repetí la revisión cada vez que cambies de modelo o de vector store, no solo una vez.

### 4. MLOps en SageMaker sin Model Monitor: Pipelines, MLflow y Evidently

**Qué dice el curso.** El flujo del lab es: datos en S3, entrenamiento con XGBoost, ajuste de hiperparámetros, endpoint o transformación por lotes. El docente menciona que hay que monitorear y reentrenar, pero el lab no llega a automatizarlo.

**Qué suma el material externo.**
- [SageMaker Pipelines](https://docs.aws.amazon.com/sagemaker/latest/dg/pipelines.html) es el orquestador serverless de SageMaker: armás los pasos con un editor visual o con el SDK de Python, pagás solo por los jobs que corre, y guarda el linaje de cada modelo.
- El cambio más importante: [SageMaker Model Monitor ya no acepta clientes nuevos](https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor-availability-change.html). AWS lo reemplaza con siete soluciones open source en `aws-samples`, basadas en SageMaker AI MLflow Apps y Evidently AI, más QuickSight para tableros y CloudWatch para métricas de sistema. Para lotes recomienda empezar por "Predictive ML Batch Monitoring Pipeline" y para endpoints por "Predictive ML Endpoint Monitoring". Las dos traen de ejemplo un XGBoost sobre el dataset UCI Bank Marketing, que es muy parecido al lab del curso. Hay también una solución para monitorear la calidad de las respuestas de un LLM.
- Los umbrales por defecto que trae el ejemplo son concretos: alerta cuando deriva más del 30% de las variables, o cuando F1 baja de 0,70, accuracy de 0,80 o ROC AUC de 0,75.

**Cómo implementarlo.**
1. Pasá el notebook del lab a un SageMaker Pipeline con tres pasos: procesamiento, entrenamiento y evaluación, más un paso condicional que solo registra el modelo si supera tu métrica mínima.
2. Registrá cada corrida en un MLflow App de SageMaker (parámetros, métricas, artefactos).
3. Para monitorear, cloná la solución de lotes o de endpoint de `aws-samples` y ajustá los umbrales a tu problema (el docente usaba 0,7 de confianza para Rekognition; para tu modelo definí el tuyo).
4. **Sugerencia:** si estás en la cuenta de AWS Academy y no podés usar algunos servicios, corré Evidently en el mismo notebook contra un CSV de "producción" simulado; lo importante es entender la idea de línea base contra datos nuevos.
5. **Sugerencia:** como Evidently y MLflow son open source, lo que aprendas acá te sirve fuera de AWS. Es la parte más portable del stack.

### 5. Costos: alertas, modalidades de cobro y el costo escondido de los guardrails

**Qué dice el curso.** No se puede poner un tope duro de gasto; hay alertas, billing y Budgets (C2P2 11:12). Para pagar menos en IA generativa el docente propone caché, lotes, Spot, elegir región o momento, modelos chicos y ruteo por tarea (C4P1 31:51).

**Qué suma el material externo.**
- [Cost Anomaly Detection](https://docs.aws.amazon.com/cost-management/latest/userguide/manage-ad.html) usa ML para detectar gastos raros. Corre unas tres veces por día, puede tardar hasta 24 horas en avisar y necesita unos 10 días de historia para un servicio nuevo. Monitorea los modelos de terceros de Bedrock que se cobran por Marketplace, pero no el resto de Marketplace (para eso, Budgets).
- En [la página de precios de Bedrock](https://aws.amazon.com/bedrock/pricing/) hay cuatro palancas que el curso no detalla: batch (50% menos en modelos seleccionados), los tiers Flex (50% de descuento a cambio de menor prioridad) y Priority (75% de recargo), Intelligent Prompt Routing (USD 1 cada 1.000 pedidos, "hasta 30%" de ahorro según AWS) y Prompt Optimization.
- El [prompt caching](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html) tiene mínimos de tokens por punto de caché que cambian por modelo: 512 en Opus 5, 1.024 en Sonnet 5 y 4.096 en Haiku 4.5. Si tu prompt fijo es más corto, no se cachea.

**Un cálculo que conviene hacer (sugerencia, con números aproximados).** Los guardrails se cobran por unidad de texto de 1.000 caracteres: USD 0,15 cada 1.000 unidades por filtro de contenido y otro tanto por temas denegados, o sea USD 0,0003 por cada 1.000 caracteres con esas dos políticas. Un prompt de 1.000 caracteres son unos 250 tokens (esto es una aproximación mía). En un modelo barato como gpt-oss-120b, que en el tier Priority cuesta USD 0,1545 por millón de tokens de entrada, esos 250 tokens cuestan unos USD 0,00004. El guardrail cuesta entonces unas siete veces más que la entrada al modelo. En un modelo frontier pasa lo contrario. Por eso el "4%" del docente no se puede generalizar: depende de qué modelo protejas.

**Cómo implementarlo.**
1. El primer día, creá un Budget mensual con alertas al 50%, 80% y 100%, y un monitor de Cost Anomaly Detection por servicio.
2. Marcá cada recurso con tags de proyecto y de cliente, como propone el docente, para que Cost Explorer te muestre quién gasta.
3. Para cada caso de uso de Bedrock, escribí en una línea qué latencia necesita y elegí la modalidad: lotes o Flex para lo que puede esperar, estándar para lo interactivo, Priority solo si la latencia vale la plata.
4. Prendé prompt caching en el system prompt largo y en los documentos que mandás siempre, y verificá en la respuesta de Converse cuántos tokens se leyeron de caché.
5. **Sugerencia:** activá los filtros de palabras y de regex primero (son gratis) y sumá los filtros pagos solo donde los necesitás.

### 6. RAG medido antes de producción: evaluación de Bedrock y elección del vector store

**Qué dice el curso.** Knowledge Bases con fuentes en S3, Confluence o SharePoint, embeddings de Titan o Nova, y una lista de vector stores. El docente recomienda evaluar con un dataset de prueba, versiones de prompt y un juez (C4P1 1:25:17).

**Qué suma el material externo.**
- Bedrock tiene [jobs de evaluación de RAG](https://docs.aws.amazon.com/bedrock/latest/userguide/evaluation-kb.html) de dos tipos: solo recuperación (mide si trajo los fragmentos correctos) y recuperación más generación (mide la respuesta final). Sirven para una Knowledge Base de Bedrock y también para un RAG propio, si le pasás las respuestas. Los evaluadores son LLMs (Nova, Claude o GPT-5.x) y podés definir métricas propias.
- La [lista de vector stores](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-setup.html) trae criterios de elección: OpenSearch (Serverless o Managed) es el único con vectores binarios, S3 Vectors es para consultas poco frecuentes con latencia por debajo del segundo, Aurora usa pgvector, Neptune Analytics habilita GraphRAG, y también están Pinecone, Redis Enterprise Cloud y MongoDB Atlas.
- El caso de [Boti del GCBA](https://aws.amazon.com/blogs/machine-learning/meet-boti-the-ai-assistant-transforming-how-the-citizens-of-buenos-aires-access-government-information-with-amazon-bedrock/) (28/08/2025) muestra cómo se hizo en un proyecto real en Argentina: con 1.908 preguntas sintéticas compararon embeddings y Cohere Multilingual superó a Titan V2, y un retriever con razonamiento llegó a 98,9% de acierto en la primera posición, entre 12,5 y 17,5 puntos más que un RAG estándar. Ojo: el artículo lo escribieron el GCBA y el equipo de IA generativa de AWS, así que es un caso contado por el proveedor.

**Cómo implementarlo.**
1. Juntá entre 50 y 200 preguntas reales de tus usuarios, en el español que hablan (con voseo y modismos), con la respuesta esperada y el documento fuente.
2. Corré un job de solo recuperación con dos modelos de embeddings distintos y elegí por números, no por costumbre.
3. Después corré uno de recuperación más generación con dos modelos generadores, uno chico y uno grande.
4. Elegí el vector store por patrón: si son pocas consultas por día, probá S3 Vectors; si es un chat con mucho tráfico, OpenSearch.
5. **Sugerencia:** guardá ese set de preguntas en el repo y corré la evaluación cada vez que cambies de modelo, de chunking o de prompt. Es la mejora más barata y la que más errores te ahorra.

### 7. Guardrails configurados y probados en rioplatense

**Qué dice el curso.** Un guardrail por caso de uso, con severidad low, medium o high, delante del modelo para no gastar tokens en lo que se va a bloquear (C4P1 45:01).

**Qué suma el material externo.**
- Los [filtros de contenido](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-content-filters.html) tienen cuatro niveles (NONE, LOW, MEDIUM, HIGH), separados para entrada y salida, con acción de bloquear o solo detectar, y dos tiers (Classic y Standard; Standard requiere inferencia entre regiones). Además hay temas denegados, filtros de palabras, PII, regex, contextual grounding y Automated Reasoning, del que AWS dice que llega a "hasta 99%" de precisión (cifra del proveedor).
- Un límite que importa para agentes: los guardrails no evalúan los resultados de las tools ni sus argumentos.
- En [streaming](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-streaming.html) podés elegir modo sincrónico (más latencia, más preciso) o asincrónico (sin latencia, pero pueden pasar fragmentos que debían bloquearse y no enmascara PII).
- `ApplyGuardrail` te deja usar el mismo guardrail con modelos que no están en Bedrock.
- En Boti, el GCBA usó un clasificador propio basado en LLM en lugar de Bedrock Guardrails, para tener flexibilidad con el habla local. Bloqueó el 100% de las consultas dañinas de su set, con algunos falsos positivos.

**Cómo implementarlo.**
1. Armá un set de 50 frases "malas" y 50 "buenas que parecen malas" en rioplatense (insultos de cancha, ironía, jerga bancaria).
2. Probá el guardrail en MEDIUM y en HIGH y medí los dos errores: lo que deja pasar y lo que bloquea de más.
3. Si usás agentes, validá los resultados de las tools con una llamada aparte a `ApplyGuardrail`.
4. Si hay PII, usá streaming sincrónico.
5. **Sugerencia:** si el guardrail no rinde con tu jerga, hacé lo que hizo el GCBA y compará contra un clasificador propio con un modelo chico; decidí con tu set de prueba.

### 8. Agentes con AgentCore, pero con código portable

**Qué dice el curso.** AgentCore es "el servicio estrella" para desplegar agentes, con MCPs, memoria y evaluación (C4P1 2:14, C4P1 41:47). El ejemplo es una Lambda con boto3 y tools declaradas a mano.

**Qué suma el material externo.**
- La [documentación de AgentCore](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html) lista más piezas de las que se ven en clase: Runtime, Memory, Gateway (convierte APIs en tools MCP), Identity, Code Interpreter, Browser, Observability (con OpenTelemetry), Evaluations, Optimization (pruebas A/B), Policy (reglas con Cedar), Registry y Payments.
- Funciona con cualquier framework (Strands, LangGraph, CrewAI, LlamaIndex, Google ADK, OpenAI Agents SDK) y con cualquier modelo, incluso fuera de Bedrock.
- La misma página aclara que "AgentCore may use and store your content to improve your service experience or performance", con mejoras solo para tu uso y no para otros clientes. Es distinto de la política de Bedrock y conviene leerlo antes de mandar datos sensibles.
- [Strands Agents](https://strandsagents.com/) es el SDK open source de AWS para agentes, en Python y TypeScript, y funciona con distintos proveedores de modelos.

**Cómo implementarlo.**
1. Escribí el agente con Strands o LangGraph, no con llamadas sueltas a boto3, para poder cambiar de modelo y de plataforma.
2. Desplegalo en AgentCore Runtime y usá Gateway para exponer tus APIs como tools.
3. Definí con Policy qué tools puede usar cada agente, siguiendo la idea de permisos mínimos de la guía de implementación.
4. Activá Observability y corré Evaluations sobre las trazas antes de cada cambio grande.
5. **Sugerencia:** guardá las trazas en formato OpenTelemetry, así no quedás atado a una sola herramienta de observabilidad.

### 9. Residencia de datos y regiones: el caso del Banco Central

**Qué dice el curso.** Hay organizaciones, como el BCRA, donde los datos no pueden salir del core (C4P1 18:41), y el docente desconfía de mandar datos por API.

**Qué suma el material externo.** La [protección de datos de Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/data-protection.html) cubre lo contractual (sin entrenamiento, sin acceso del proveedor del modelo), pero la [inferencia entre regiones](https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html) puede procesar el pedido en otra región de la misma geografía, y el perfil Global en cualquier región. CloudTrail deja registrado dónde se procesó. El [acceso a modelos](https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html) se puede restringir con SCP o IAM. La región más cercana a Argentina es São Paulo, que en S3 cuesta 76% más que Virginia.

**Cómo implementarlo.**
1. Escribí qué datos pueden salir del país y cuáles no, con el área legal o de cumplimiento.
2. Para los que no pueden salir de una geografía, usá modelos invocados en la región sin perfil Global, y bloqueá el perfil Global con una SCP.
3. Revisá en CloudTrail el campo `inferenceRegion` durante las pruebas.
4. **Sugerencia:** si la regulación exige que el dato no salga de tu infraestructura, Bedrock no alcanza; ese es justo el escenario donde gana la alternativa del "Análisis adversario".

### 10. Casos reales para mirar (y cómo leerlos)

- **Boti, GCBA** ([blog de AWS, 28/08/2025](https://aws.amazon.com/blogs/machine-learning/meet-boti-the-ai-assistant-transforming-how-the-citizens-of-buenos-aires-access-government-information-with-amazon-bedrock/)). LangGraph con Bedrock y la API Converse, DynamoDB, un clasificador propio de seguridad y un retriever con razonamiento. Es el caso más cercano a lo que enseña el curso y está hecho en Argentina. Lo escribieron junto con AWS.
- **Mercado Libre, GenAds** ([caso de estudio de AWS](https://aws.amazon.com/solutions/case-studies/mercado-libre-mutt-data/)). Con Mutt Data generaron anuncios con Stable Diffusion y Claude 3 Sonnet en Bedrock, S3 y DynamoDB, en 7 países, y reportan 45% más de impresiones y 25% más de clics. Es una página de marketing del proveedor y las métricas no están auditadas.
- **Sugerencia:** de cada caso, quedate con la arquitectura y con cómo evaluaron, no con los porcentajes. Los dos casos usan servicios gestionados con un framework portable arriba (LangGraph en Boti), lo que encaja con el híbrido del final.

### 11. Estudiar para la certificación

**Qué dice el curso.** El examen del módulo es múltiple choice, se puede repetir y sirve para el badge; las certificaciones suman y en Craftech están todos certificados (C2P2 1:20:43).

**Qué suma el material externo.**
- **AWS Certified AI Practitioner (AIF-C01)** ([página](https://aws.amazon.com/certification/certified-ai-practitioner/), [guía del examen](https://docs.aws.amazon.com/aws-certification/latest/ai-practitioner-01/ai-practitioner-01.html)): 90 minutos, 65 preguntas (50 puntúan y 15 no), USD 100, aprobación con 700 sobre 1.000, válida 3 años, disponible en español latinoamericano. Los dominios pesan así: fundamentos de IA y ML 20%, fundamentos de IA generativa 24%, aplicaciones de modelos fundacionales 28%, IA responsable 14%, y seguridad, cumplimiento y gobernanza 14%.
- **AWS Certified Machine Learning Engineer Associate** ([página](https://aws.amazon.com/certification/certified-machine-learning-engineer-associate/)): MLA-C01 cuesta USD 150 y su versión en inglés se pudo rendir hasta el 28/09/2026. Desde el 29/09/2026 está en beta MLA-C02, solo en inglés, con 85 preguntas, 170 minutos y USD 75, y suma Bedrock, RAG, IA agéntica y modelos fundacionales.
- [AWS Academy](https://aws.amazon.com/training/awsacademy/) les da a los estudiantes 12 meses de AWS Skill Builder sin costo, y a los docentes vouchers de examen. La página de Skill Builder no cargó cuando la abrí, así que no pude ver qué cursos y exámenes de práctica hay.

**Cómo implementarlo.**
1. **Sugerencia:** si querés certificarte en español y el curso es tu primer contacto con ML, apuntá a AIF-C01. Las clases 1 y 2 cubren buena parte del dominio 1, y las clases 3 y 4 los dominios 2, 3 y 4.
2. **Sugerencia:** si vas por MLA, estudiá para MLA-C02 y en inglés. El curso te da la base de SageMaker, pero te falta MLOps (sección 4), monitoreo y despliegue con más profundidad.
3. Descargá la guía del examen y marcá cada tema con "lo vi en clase", "lo vi por arriba" o "no lo vi".
4. Activá el Skill Builder de AWS Academy y hacé el examen de práctica oficial antes de pagar el real.
5. **Sugerencia:** las secciones 1 y 2 de este archivo sirven de repaso: varias preguntas típicas del examen (cifrado por defecto, Guardrails, inferencia entre regiones, Converse) están ahí, con el dato correcto.

---

## Críticas y límites

1. **Es capacitación del proveedor, dictada por un partner.** AWS Academy es el currículo oficial de AWS para universidades, pensado para preparar certificaciones de AWS. Craftech, la empresa del docente, es partner AWS de nivel Advanced, se presenta como "Rising Star Partner of the Year 2026" y vende soluciones de IA generativa con Bedrock y un producto propio en AWS Marketplace ([craftech.io](https://craftech.io/)). Eso no invalida el contenido, pero explica por qué casi no se discuten alternativas fuera de AWS.
2. **La plataforma envejece más rápido que el curso.** En el entorno del curso hay cuatro servicios en retirada: Forecast y Model Monitor no aceptan clientes nuevos, Timestream for LiveAnalytics tiene aviso de fin de soporte y Amazon Q Developer termina su soporte el 30/04/2027. El examen MLA también cambió de versión menos de un mes después de la última clase. Si construís sobre servicios gestionados, el calendario de cambios lo pone el proveedor.
3. **Muchas cifras son de memoria y algunas están mal.** Rekognition, Kinesis Video Streams, la capa gratuita, el prompt caching y la edad de Kiro son ejemplos. El docente lo avisa varias veces, y está bien, pero el apunte necesita la tabla de la sección 1 al lado.
4. **El mensaje sobre datos queda mal calibrado.** Es más alarmista de lo que corresponde para Bedrock y no menciona que Comprehend y AgentCore sí pueden guardar contenido para mejorar el servicio. La regla útil no es "las APIs son peligrosas" sino "leé la política de cada servicio".
5. **Lock-in.** Knowledge Bases, Guardrails, AgentCore, Converse y SageMaker Pipelines no tienen equivalente directo en otra nube. El costo de salida no aparece en ninguna clase.
6. **La práctica tiene un hueco.** Según el docente, la cuenta de AWS Academy no da acceso a Bedrock, así que la parte de IA generativa se ve en demos y no en labs propios, y para practicar necesitás una cuenta propia que se paga.
7. **Las cifras de ahorro y precisión son del proveedor.** "Hasta 90%" (S3 Vectors), "hasta 99%" (Automated Reasoning), "hasta 30%" (ruteo de prompts) y "75% menos que Redshift" (ClickHouse) son números de quien vende. Los casos de Boti y Mercado Libre están publicados por AWS.
8. **Límites de esta revisión.** No verifiqué la disponibilidad de cada modelo por región, la página de precios de SageMaker y la de Skill Builder no cargaron, varias tablas de precios las leí del JSON que usa la página y no de la página renderizada, y la documentación de vLLM no cargó con WebFetch (la leí con curl).

---

## Análisis adversario

> Cómo leer esta sección: pongo el enfoque del curso contra la alternativa más fuerte que encontré, presentada en su mejor versión. La idea no es desarmar el curso, sino ver en qué contextos conviene y en cuáles no. Solo cito fuentes que abrí entre el 01/10/2026 y el 02/10/2026.

**La tesis, en dos oraciones.** El curso sostiene que conviene construir ML e IA generativa sobre los servicios gestionados de AWS (S3, SageMaker, Bedrock, Knowledge Bases, Guardrails, AgentCore), porque te ahorran operar infraestructura, te dan seguridad y gobernanza integradas y te dejan elegir entre muchos modelos. El trabajo del equipo pasa a ser elegir el servicio y el modelo correctos para cada problema y controlar el costo.

### La alternativa más fuerte: un stack portable y open source

**Qué propone.** Construir sobre piezas abiertas que corren en cualquier nube o en servidores propios: modelos de pesos abiertos servidos con vLLM o KServe sobre Kubernetes, MLflow para experimentos y registro de modelos, Evidently para monitoreo, y un framework de agentes abierto (LangGraph o Strands). La versión seria no dice "salí de la nube ya", sino "diseñá para poder irte" y movés a infraestructura propia las cargas grandes y estables.

**Por qué elegí esta.** Es la única que discute la premisa de fondo del curso (que conviene apoyarse en los servicios gestionados de un solo proveedor), tiene un ecosistema maduro, y hay evidencia pública de costos a favor y en contra. Otras alternativas que consideré:
- **Usar directamente las APIs de los proveedores de modelos** (OpenAI, Anthropic, Google) sin una nube en el medio. Es simple y rápida, pero cambia el lock-in de la nube por el lock-in de un proveedor de modelos, y Bedrock ya ofrece casi los mismos modelos (salvo Gemini) bajo las reglas de datos de AWS. La uso como contrapeso, no como alternativa principal.
- **"No entrenes, usá APIs"**: reemplazar los modelos propios de SageMaker por modelos fundacionales para todo. El propio curso responde a esto con lo de "la hormiga y la bazuca" (un modelo chico entrenado es más preciso y barato para tareas acotadas), y la Generative AI Lens también trata el costo como un pilar, así que no la elegí como la contraria más fuerte.

### La alternativa en su mejor versión

**Quién la defiende y qué dice.**
- **Sarah Wang y Martin Casado (a16z)**, en [*The Cost of Cloud, a Trillion Dollar Paradox*](https://a16z.com/the-cost-of-cloud-a-trillion-dollar-paradox/) (27/05/2021), estiman que repatriar cargas puede costar entre un tercio y la mitad de lo que se paga en la nube, citan que Dropbox ahorró unos USD 75 millones en dos años, y resumen la idea en "You're crazy if you don't start in the cloud; you're crazy if you stay on it". Recomiendan diseñar para la portabilidad (por ejemplo, con Kubernetes) y repatriar de a poco. Conflicto de interés: a16z es un fondo que invierte en empresas de infraestructura.
- **37signals (Basecamp, HEY)**, en [cloud-exit](https://basecamp.com/cloud-exit), cuenta que salió de AWS en 2023 y que ahorra unos USD 10 millones en cinco años (entre la mitad y dos tercios del costo), sin sumar personal. Conflicto de interés: es su propio caso y la empresa hace campaña pública con él.
- **Proyectos open source maduros.** [MLflow](https://mlflow.org/docs/latest/) cubre ML clásico y también LLMs y agentes (tracing y evaluación). [KServe](https://kserve.github.io/website/) sirve modelos predictivos y generativos en Kubernetes con vLLM, API compatible con OpenAI, escalado a cero, despliegues canary y detección de drift. vLLM ofrece serving compatible con OpenAI, prefix caching y charts de Helm (su documentación no cargó con WebFetch y la leí con curl). El dato curioso: el propio AWS usa MLflow y Evidently para reemplazar Model Monitor.

**Qué evidencia la respalda.**
- Un [paper de investigadores de Carnegie Mellon (arXiv 2509.18101)](https://arxiv.org/abs/2509.18101) calcula cuándo se recupera la inversión en hardware propio frente a APIs comerciales: unos 3 meses para modelos chicos, de 6 a 24 meses para medianos y 5 años o más para los grandes. Concluye que conviene a partir de unos 50 millones de tokens por mes o cuando hay requisitos de residencia de datos. Su límite: deja afuera el costo del personal y del mantenimiento.
- En la práctica, el lock-in ya le costó a quien usaba Forecast o Model Monitor: tienen que migrar cuando el proveedor decide. Con piezas abiertas, el calendario es tuyo.

**La evidencia en contra que más pesa.** Un [estudio de caso en Pegatron (arXiv 2607.13080)](https://arxiv.org/abs/2607.13080), con un solo desarrollador durante dos períodos de 28 días, comparó una API frontier contra un modelo abierto en servidores propios. Con 99,3% de aciertos de caché, Claude Opus por API salió USD 0,57 por millón de tokens efectivo, contra USD 2,83 del modelo abierto en infraestructura compartida. El modelo abierto tuvo 74,9% de commits de corrección contra 45,9% de la API. El costo total con infraestructura compartida fue 40,1% menor, pero con un servidor dedicado fue 43,8% mayor, y ninguna política híbrida le ganó a usar solo la API. Es un solo caso, en una empresa que fabrica hardware, pero muestra que el prompt caching cambió la cuenta que hacía el paper de CMU.

### Comparación directa

| Criterio | A: servicios gestionados de AWS (el curso) | B: stack portable y open source |
|---|---|---|
| Costo | Pagás por uso, sin inversión inicial. Barato con volumen bajo o variable; caro con volumen alto y estable. Con prompt caching y lotes, las APIs frontier pueden quedar más baratas por token que un modelo propio (caso Pegatron). | Inversión inicial en GPUs o clusters y en personal. Puede ahorrar entre un tercio y dos tercios con cargas grandes y estables (a16z, 37signals), y se recupera en meses para modelos chicos y en años para los grandes (CMU). |
| — | Baja para empezar: consola, SDK y servicios integrados. Crece con la cantidad de servicios y permisos. | Alta: Kubernetes, serving, drivers de GPU, seguridad, actualizaciones y monitoreo corren por tu cuenta. |
| Tiempo hasta obtener valor | Días: un RAG con Knowledge Bases o un modelo XGBoost con SageMaker sale en la primera semana. | Semanas o meses hasta tener una plataforma estable, salvo que ya tengas el equipo y el cluster. |
| Riesgo | Lock-in, cambios de servicio que decide el proveedor (Forecast, Model Monitor, Q), sorpresas de factura y residencia de datos fuera de tu control. | Calidad menor de los modelos abiertos en tareas difíciles (más correcciones en Pegatron), falta de GPUs, dependencia de pocas personas que saben operar todo. |
| Madurez | Servicios con años en el mercado, pero las piezas de IA generativa cambian cada pocos meses. | MLflow, Kubernetes y KServe son maduros; vLLM y los modelos abiertos cambian casi tan rápido como los servicios gestionados. |
| Evidencia disponible | Casos publicados por AWS (Boti, Mercado Libre), con coautoría o marketing del proveedor. Ningún estudio independiente de costo total. | Casos de empresas que salieron (37signals, Dropbox vía a16z), un análisis académico sin costo de personal (CMU) y un caso que favorece a la API (Pegatron). Todos con algún interés o con muestras chicas. |
| Tipo de equipo/contexto | Estudiantes, pymes, startups, equipos sin especialistas en infraestructura, volumen incierto, necesidad de modelos frontier. | Volumen alto y estable, regulación que exige datos en infraestructura propia, equipo de plataforma con experiencia, horizonte largo. |

### Dónde gana la alternativa

- **Residencia de datos estricta.** Si el dato no puede salir de tu infraestructura (el ejemplo del BCRA), Bedrock no alcanza aunque no entrene con tus datos.
- **Volumen alto y sostenido.** Con decenas de millones de tokens por mes de un modelo mediano o chico, el paper de CMU y los casos de salida de la nube muestran ahorros grandes.
- **Control del calendario.** No te enterás por un aviso de que tu servicio de monitoreo o de pronóstico ya no acepta clientes nuevos.
- **Portabilidad del conocimiento.** MLflow, Evidently, Kubernetes y vLLM te sirven en cualquier empresa, también en las que no usan AWS.

### Dónde pierde

- **Tiempo hasta obtener valor.** Para aprender, validar una idea o un proyecto de pyme, operar GPUs y Kubernetes es una distracción.
- **Calidad en tareas difíciles.** Los modelos frontier (Claude, GPT) no se pueden alojar en tu infraestructura, y en el caso Pegatron el modelo abierto generó bastante más trabajo de corrección.
- **El caché cambió la cuenta.** Con aciertos de caché altos, el precio efectivo por token de una API frontier puede quedar por debajo del de un modelo propio.
- **Personal.** Los análisis a favor de salir de la nube suelen dejar afuera o minimizar el costo de las personas que operan la plataforma.
- **El lock-in de AWS es menor de lo que parece.** Bedrock aloja modelos de pesos abiertos, AgentCore acepta cualquier framework y cualquier modelo, y AWS mismo usa MLflow y Evidently para monitorear. Podés llegar bastante portable sin salir de AWS.

### Cómo decidir

**Elegí A (servicios gestionados de AWS) si** estás aprendiendo o validando una idea, tu volumen es bajo o incierto, necesitás modelos frontier, tu equipo no tiene especialistas en infraestructura, o la regulación acepta que el dato se procese en una región de AWS con los controles contractuales de Bedrock.

**Elegí B (stack portable y open source) si** tenés un volumen alto y estable con un modelo que un modelo abierto resuelve bien, la regulación exige que el dato no salga de tu infraestructura, ya tenés un equipo de plataforma que opera Kubernetes, o el riesgo de que el proveedor cambie o retire un servicio es inaceptable para tu negocio.

**Un híbrido posible (sugerencia).** Empezá en AWS, pero con piezas que se puedan mover:
1. Escribí los agentes con Strands o LangGraph y llamá a los modelos con Converse o con la API compatible con OpenAI de Bedrock, para que cambiar de proveedor sea cambiar una configuración.
2. Registrá experimentos y modelos en MLflow (el que gestiona SageMaker) y monitoreá con Evidently, como recomienda AWS después de Model Monitor.
3. Guardá los datos en S3 en formatos abiertos (Parquet, Iceberg) y las trazas en OpenTelemetry.
4. Usá un modelo de pesos abiertos en Bedrock para las tareas simples, así sabés si te alcanza antes de pensar en alojarlo vos.
5. Medí tokens por mes y costo por caso de uso desde el día 1, y revisá la decisión cuando pases los 50 millones de tokens por mes de un mismo modelo o cuando aparezca un requisito de residencia que Bedrock no cubra.
6. Mantené tu set de evaluación (sección 6) independiente de la plataforma, porque es lo que te va a decir si el cambio de modelo o de infraestructura empeora la calidad.

**Veredicto.** Para estudiar, para una pyme o para validar un producto, el enfoque del curso gana con claridad: el tiempo hasta obtener valor es mucho menor y, con caché y lotes, las APIs frontier pueden ser incluso más baratas por token. La alternativa portable gana cuando hay volumen alto y estable, residencia de datos estricta o un equipo de plataforma que ya existe. La evidencia más reciente (el caso Pegatron) le resta fuerza al argumento de costo de la alternativa, pero los retiros de Forecast, Model Monitor y Q le dan fuerza al argumento de control. La opción más sensata para la mayoría es el híbrido: AWS como plataforma, con código, datos y evaluación portables.

---

## Material para seguir

**Arquitectura y buenas prácticas**
- [Well-Architected Machine Learning Lens](https://docs.aws.amazon.com/wellarchitected/latest/machine-learning-lens/machine-learning-lens.html): la lista de control más completa para ML clásico, y sirve también fuera de AWS.
- [Well-Architected Generative AI Lens](https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/generative-ai-lens.html): las mismas preguntas para RAG y agentes, con costo y agencia excesiva incluidos.

**SageMaker y MLOps**
- [SageMaker Pipelines](https://docs.aws.amazon.com/sagemaker/latest/dg/pipelines.html): para pasar el notebook del lab a un flujo que se repite solo.
- [Cambio de disponibilidad de Model Monitor](https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor-availability-change.html): explica el reemplazo con MLflow y Evidently y trae umbrales de ejemplo.
- [Algoritmos integrados de SageMaker](https://docs.aws.amazon.com/sagemaker/latest/dg/algos.html): la lista oficial, útil para el examen y para elegir algoritmo.
- [Documentación de MLflow](https://mlflow.org/docs/latest/): la pieza más portable del stack, para ML clásico y para LLMs.

**Bedrock**
- [Converse](https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference.html): la API que conviene usar por defecto, con todos sus campos.
- [Prompt caching](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html): mínimos de tokens, TTL y precios por modelo.
- [Inferencia entre regiones](https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html): qué hace cada perfil y qué implica para la residencia de datos.
- [Protección de datos en Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/data-protection.html): la respuesta oficial a "¿entrenan con mis datos?".
- [Filtros de contenido de Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-content-filters.html): niveles, tiers y límites con agentes.
- [Evaluación de RAG](https://docs.aws.amazon.com/bedrock/latest/userguide/evaluation-kb.html): cómo medir un RAG antes de ponerlo en producción.
- [Vector stores para Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-setup.html): la comparación de opciones que el docente enumeró.
- [Model cards de Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/model-cards.html): la lista de modelos al día, más confiable que la FAQ.
- [Precios de Bedrock](https://aws.amazon.com/bedrock/pricing/): tiers, lotes, guardrails y optimización de prompts.

**Agentes**
- [Qué es AgentCore](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html): todas las piezas y la nota sobre uso de contenido.
- [Strands Agents](https://strandsagents.com/): el SDK abierto de AWS, para que tu agente no dependa de una sola plataforma.

**Costos**
- [Cost Anomaly Detection](https://docs.aws.amazon.com/cost-management/latest/userguide/manage-ad.html): qué detecta, con qué demora y qué deja afuera.
- [Capa gratuita de AWS](https://aws.amazon.com/free/): cómo funcionan los créditos para cuentas nuevas.

**Casos reales**
- [Boti, GCBA, con Bedrock](https://aws.amazon.com/blogs/machine-learning/meet-boti-the-ai-assistant-transforming-how-the-citizens-of-buenos-aires-access-government-information-with-amazon-bedrock/): el mejor ejemplo local de RAG y seguridad medidos (escrito con AWS).
- [Mercado Libre GenAds](https://aws.amazon.com/solutions/case-studies/mercado-libre-mutt-data/): IA generativa para anuncios en 7 países (marketing de AWS).

**Certificación y estudio**
- [Guía del examen AIF-C01](https://docs.aws.amazon.com/aws-certification/latest/ai-practitioner-01/ai-practitioner-01.html): los dominios y su peso, para planificar el estudio.
- [AWS Certified AI Practitioner](https://aws.amazon.com/certification/certified-ai-practitioner/): precio, idiomas y duración, incluido el español.
- [AWS Certified Machine Learning Engineer Associate](https://aws.amazon.com/certification/certified-machine-learning-engineer-associate/): el cambio de MLA-C01 a MLA-C02 y lo que suma.
- [AWS Academy](https://aws.amazon.com/training/awsacademy/): qué incluye el programa, incluido el Skill Builder para estudiantes.

**La otra mirada**
- [a16z, *The Cost of Cloud*](https://a16z.com/the-cost-of-cloud-a-trillion-dollar-paradox/): el argumento más citado a favor de diseñar para poder salir de la nube.
- [37signals, cloud-exit](https://basecamp.com/cloud-exit): un caso real de salida de AWS con números.
- [CMU, break-even de LLMs propios (arXiv 2509.18101)](https://arxiv.org/abs/2509.18101): cuándo conviene alojar tu modelo, en meses y tokens.
- [Caso Pegatron (arXiv 2607.13080)](https://arxiv.org/abs/2607.13080): la mejor evidencia reciente de que una API con caché puede ganar en costo y en calidad.
- [KServe](https://kserve.github.io/website/): cómo se ve servir modelos en Kubernetes sin un proveedor de nube.
