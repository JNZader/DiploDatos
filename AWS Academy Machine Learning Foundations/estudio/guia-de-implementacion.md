# Guía de implementación: AWS Academy Machine Learning Foundations (FAMAF UNC, Fabián Hanuseski)

**Videos:** 8 clases grabadas del curso AWS Academy Machine Learning Foundations en el canal de FAMAF UNC: C1P1 · C1P2 · C2P1 · C2P2 · C3P1 · C3P2 · C4P1 · C4P2 · Duración total: unas 14 horas y media.
**De qué va:** Fabián "Hanu" Hanuseski, CTO de Craftech, recorre el flujo completo de ML en AWS: datos en S3, entrenamiento, despliegue, evaluación y ajuste en SageMaker, control de costos, visión por computadora con Rekognition y chatbots con Lex. En las últimas clases suma IA generativa con Bedrock: elección de modelos, costo en tokens, guardrails, RAG con knowledge bases y agentes con permisos mínimos. Esta guía junta las ideas que se pueden aplicar; el detalle por módulo está en el apunte de estudio (`aws-ml-foundations-apunte-de-estudio.md`).

> Nota: esta guía sale de los subtítulos automáticos en español de los 8 videos. Muchos nombres vienen deformados (ver el glosario al final). Lo que el docente afirmó y puede estar desactualizado va marcado como **para verificar**; todavía no está chequeado. Las ideas mías van marcadas como **Sugerencia**. Los links dicen clase, parte y minuto: "C2P1 1:23:45" es la clase 2, parte 1, en 1:23:45.

---

## Checklist para arrancar ya

1. Antes de abrir SageMaker, escribí el problema de negocio con una métrica medible (por ejemplo, bajar 10% los reclamos en 6 meses) y confirmá que se puede resolver manualmente.
2. Hacé que el data engineer te deje los datos limpios y ofuscados en un bucket de S3, en CSV, JSON o RecordIO, y nunca conectes la notebook a la base de producción.
3. Entrená en SageMaker leyendo train, test y validación desde S3 y guardando el modelo en S3, así podés destruir la instancia sin perder nada.
4. Elegí un endpoint de SageMaker cuando otra aplicación necesite consultar el modelo en línea, y una transformación por lotes cuando tengas que procesar un volumen grande sin respuesta inmediata.
5. Para el endpoint, preferí varias instancias chicas con autoescalado en lugar de una grande, y ponele un tope a la cantidad de instancias.
6. Sacá el umbral de clasificación del código y guardalo en una variable de entorno o una base de parametría, para cambiarlo sin redesplegar.
7. Probá varios umbrales (por ejemplo 0,25, 0,3 y 0,75) mirando la matriz de confusión y la curva ROC, y elegí el que tenga sentido para el costo de equivocarse en tu negocio.
8. Automatizá la búsqueda de hiperparámetros con rangos, un máximo de jobs en paralelo y un máximo de jobs totales, porque cada job es cómputo que pagás.
9. Estimá el costo con AWS Pricing Calculator antes de levantar nada, configurá Budgets con alertas y apagá o borrá notebooks y endpoints que nadie usa.
10. Etiquetá cada recurso con un tag por cliente o proyecto y revisá Cost Explorer filtrando por ese tag, o separá cuentas por cliente si querés facturas limpias.
11. Si tenés que analizar imágenes a escala, armá un flujo en el que cada archivo que entra a S3 dispare una Lambda que llama a Rekognition y guarda las etiquetas en una base de datos.
12. Antes de pagar Rekognition por cada imagen, probá si una librería local de OCR o detección alcanza, y mandá a Rekognition solo los casos difíciles.
13. Para un chatbot transaccional de alto volumen (turnos, reservas), empezá con Lex más Lambda, que es rápido y barato, y reservá la IA generativa para cuando necesites conversación libre.
14. En Bedrock, compará la misma consulta contra varios modelos midiendo tokens de entrada y salida, latencia y calidad, en lugar de actualizar siempre al modelo más nuevo.
15. Fijá un presupuesto de tokens por caso de uso con max tokens y poné una alerta cuando el consumo se acerque al límite.
16. Bajá el costo en tokens con caché de respuestas cuando los datos cambian poco, inferencia por lotes cuando no hay apuro y modelos chicos para tareas simples.
17. Poné un guardrail delante del modelo para bloquear prompt injection, temas fuera del negocio y datos sensibles antes de gastar tokens en el modelo grande.
18. Usá un RAG con una knowledge base de Bedrock solo cuando la información no entre en el prompt, y medí cuántos tokens agrega cada respuesta.
19. Dale a la IA datos de la capa gold (sumarizados y sin datos sensibles) y, si genera SQL, entregale la query armada para que solo complete el filtro.
20. Tratá a cada agente como un usuario más: un rol de IAM con permisos mínimos, solo las tools que necesita y un guardrail en cada salto.
21. Activá CloudTrail, el registro de invocaciones y métricas de CloudWatch para saber quién llama al modelo, con qué prompt y cuántos tokens consume.

---

## Versión completa

### 1. Formular el problema antes de tocar la consola
**Dónde:** C1P1 47:25, C1P1 1:20:58, C1P1 1:22:02, C1P1 1:24:47, C1P1 1:26:24, C1P1 1:27:28, C1P1 1:28:00, C2P1 59:05

**Contexto.** El docente insiste en arrancar por la necesidad y no por FOMO. Su ejemplo es un cliente que valida certificados médicos: el éxito se mide como 9 de cada 10 bien resueltos, y el valor es el tiempo humano que se ahorra. Las preguntas que propone son si es un problema de ML, si es supervisado, cuál es el rendimiento mínimo y si hace falta tiempo real o alcanza con un proceso nocturno. Agrega que el problema tiene que poder resolverse manualmente primero y que conviene un objetivo de negocio medible, como bajar 10% los reclamos.

**Por qué importa.** En el lab 3.6 lo dice sin vueltas: si el proyecto no resuelve un problema real, muere. También muestra el costo de equivocarse en la otra dirección: un modelo de fraude demasiado agresivo le bloquea la tarjeta a alguien que viaja a Europa.

**Cómo implementarlo.**
- Escribí en una línea qué decisión va a tomar el modelo y quién la usa.
- Definí la métrica de negocio y el plazo (por ejemplo, 10% menos reclamos en 6 meses) y el rendimiento mínimo aceptable.
- Decidí si necesitás respuesta en línea o por lotes, porque eso define el despliegue (sección 4).
- Sumá un experto de dominio desde el principio.
- **Sugerencia:** anotá también cuánto cuesta un falso positivo y un falso negativo, porque esa cuenta es la que después te ayuda a elegir el umbral de la sección 5.

### 2. Datos en S3, preparados por otro y sin tocar producción
**Dónde:** C1P1 1:34:13, C1P1 1:35:15, C1P1 1:46:06, C1P1 1:50:36, C1P2 1:18:19, C1P2 1:19:23, C1P2 1:20:28, C1P2 1:40:03

**Contexto.** S3 centraliza los datos. "Un buen data scientist nunca debería recibir datos crudos": el data engineer los ofusca, hace el ETL y deja cada noche un CSV en un bucket. Glue arma el catálogo de las fuentes. Desde la notebook no hay que conectarse a producción porque las credenciales quedan expuestas y podés hacer un update o un delete sin querer. IAM tiene que dejar que SageMaker lea el bucket.

**Por qué importa.** Separar roles protege los datos productivos y deja que cada servicio escale por su lado. Además, si todo vive en S3, la instancia de cómputo es descartable.

**Cómo implementarlo.**
- Pedí un bucket de entrada con los datos ya limpios, en CSV, JSON o protobuf RecordIO.
- Dale al rol de la notebook permiso de lectura sobre ese bucket y no le pases credenciales de bases de datos.
- Si tenés varias fuentes (facturación, finanzas, compras), juntalas en S3 y catalogalas con Glue.
- Revisá la clase de almacenamiento de S3: backup barato para lo que casi no se lee y acceso frecuente para lo que usás todos los días, con reglas de borrado.
- **Sugerencia:** separá en prefijos distintos los datos de entrada, los de entrenamiento y los modelos, para que los permisos y los borrados automáticos sean más fáciles de definir.

### 3. Del CSV en S3 a un modelo entrenado en SageMaker
**Dónde:** C1P2 12:16, C1P2 12:49, C1P2 16:07, C1P2 39:59, C1P2 41:12, C1P2 1:22:07, C1P2 1:35:06, C1P2 1:36:49, C1P2 1:48:21

**Contexto.** El flujo de los labs 3.1 a 3.4 es: crear una notebook instance (ml.m5.xlarge en el lab), explorar los datos con pandas, hacer ingeniería de características (ordinales a números, faltantes, outliers), dividir los datos, subirlos a S3 y entrenar con un algoritmo integrado de SageMaker (Linear Learner en el 3.1; también menciona k-means y XGBoost). El resultado queda en S3. Después, borrá la instancia: la notebook va a GitHub y los resultados ya están en S3. En producción, el servidor pregunta todos los días cuál es la última versión del modelo, guardada con un prefijo de fecha.

**Por qué importa.** La notebook es solo cómputo. Si la dejás prendida pagás aunque nadie la use, y si guardás todo en S3 podés destruirla sin miedo.

**Cómo implementarlo.**
1. Creá la notebook instance con el tipo más chico que alcance; si la CPU vive al 90%, subí de tamaño.
2. Explorá y prepará los datos; si falta una librería, instalala en una celda con `!pip install`.
3. Convertí los datos al formato que pide el algoritmo (el lab usa float32) y subilos a S3.
4. Entrená con la URL del bucket y dejá el artefacto del modelo en S3.
5. Guardá el modelo con un prefijo de fecha para que producción sepa cuál es el último.
6. Subí la notebook a GitHub y borrá la instancia.
- Ojo: el docente aclara que para un modelo chico (50 MB) SageMaker es "matar una hormiga con una bazuca", y que lo podés correr local (C1P1 25:03).
- **Sugerencia:** limpieza y ETL en una notebook o proceso aparte, y en la de entrenamiento solo consumir el CSV listo, como él mismo recomienda al criticar la notebook del lab (C2P1 45:38).

### 4. Endpoint o transformación por lotes
**Dónde:** C2P1 0:35, C2P1 14:58, C2P1 15:29, C2P1 16:02, C2P1 17:08, C2P1 18:14, C2P1 18:47, C2P1 48:25, C2P1 49:31, C2P1 1:12:03

**Contexto.** En el lab 3.5 hay dos caminos: el alojamiento de SageMaker, que expone el modelo como un endpoint (una API), y la transformación por lotes. El deploy recibe el tipo y la cantidad inicial de instancias. Si responde lento, subís de tamaño o de familia. Muchas instancias chicas cuestan lo mismo que una grande, pero escalan horizontalmente y se apagan cuando hay poca demanda. SageMaker puede autoescalar al 80% de CPU y mandar alertas, y conviene ponerle un tope porque "la billetera no es infinita". Los lotes sirven para no correr todo de una tirada.

**Por qué importa.** Un endpoint prendido cuesta todo el tiempo. Si nadie consulta el modelo en línea, un proceso por lotes es más barato. Y si borrás un endpoint que alguien usa, deja de estar hosteado aunque el modelo siga en S3.

**Cómo implementarlo.**
- **Endpoint:** cuando una web, una app o un servidor necesitan respuesta en el momento (por ejemplo, fraude en una transacción con tarjeta). Arrancá con instancias chicas, configurá autoescalado con un máximo y alertas.
- **Batch transform:** cuando procesás un archivo grande cada tanto (scoring nocturno de clientes, por ejemplo). Tené en cuenta que una transformación enorme tarda.
- Si vas a exponer el endpoint afuera, hace falta más arquitectura; tal como sale del lab no es accesible desde fuera (C2P1 24:37).
- Después de cada lab o prueba, borrá los endpoints que levantaste (C2P1 1:02:08).
- **Sugerencia:** al terminar el día corré `aws sagemaker list-endpoints` (o mirá la consola) para confirmar que no quedó ninguno prendido sin querer.

### 5. El umbral como parámetro, no como constante
**Dónde:** C2P1 1:20:53, C2P1 1:22:58, C2P1 1:23:31, C2P1 1:24:04, C2P1 1:25:08, C2P1 1:25:41, C2P1 1:34:32, C2P1 1:38:25, C2P1 1:41:41

**Contexto.** El lab 3.6 usa un umbral de 0,3 para pasar la probabilidad a normal o anormal, y el docente propone probar 0,25 y 0,75. En producción dice que hay que definir un umbral: podés arrancar en 0,25 y después subir a 0,7 u 0,8, cuidando que no se dispare. En fraude, el nivel de confianza depende del negocio. Lo ideal es tenerlo en una variable de entorno o, más dinámico todavía, en una base de parametría consultada por URL, igual que hiperparámetros y cantidad de instancias.

**Por qué importa.** El umbral define cuántos falsos positivos y falsos negativos vas a tener, y el negocio lo va a querer mover. Si está hardcodeado, cada ajuste es un redespliegue.

**Cómo implementarlo.**
1. Calculá la matriz de confusión y la curva ROC con varios umbrales.
2. Elegí el que equilibre el costo de cada error para tu caso.
3. Leé el umbral desde una variable de entorno o una tabla de parámetros.
4. Revisalo periódicamente con datos nuevos.
- Lo mismo aplica a Rekognition (confianza mínima, sección 9) y a la extracción de campos con IA (sección 15).
- **Sugerencia:** registrá en cada predicción el umbral que estaba vigente, así podés explicar después por qué una decisión salió como salió.

### 6. Ajuste automático de hiperparámetros con límites
**Dónde:** C2P1 1:44:01, C2P1 1:44:33, C2P1 1:47:08, C2P1 1:49:21, C2P1 1:54:55, C2P2 1:47, C2P2 3:26, C2P2 5:38, C2P2 15:07, C2P2 16:14

**Contexto.** En el lab 3.7 (que en clase llama "autopilot") SageMaker corre muchos training jobs con rangos de hiperparámetros (mínimo, máximo, valor esperado), una cantidad de jobs en paralelo y un total. Lo que en el 3.6 hacías a mano pasa a ser automático y se puede correr todos los días. Muestra que la ROC mejora con el ajuste (alrededor de 0,78 contra 0,89, lectura dudosa). Advierte que con 10 jobs de 10 instancias tenés 100 instancias y que "te lo cobra".

**Por qué importa.** Probar combinaciones a mano en una sola instancia puede tardar días; en paralelo es rápido, pero cada job suma costo.

**Cómo implementarlo.**
- Definí rangos razonables solo para los hiperparámetros que importan.
- Fijá un máximo de jobs en paralelo y un máximo total.
- Usá corte temprano cuando se alcanza el valor esperado.
- Analizá todos los jobs para ver cuál se acerca al objetivo.
- **Sugerencia:** antes de lanzar el tuning, estimá en Pricing Calculator el peor caso (jobs totales por instancias por tiempo máximo) y compará contra tu Budget.

### 7. Control de costos: calculadora, Budgets, tags y FinOps
**Dónde:** C1P2 24:32, C1P2 25:36, C2P2 7:50, C2P2 9:31, C2P2 11:12, C2P2 11:44, C2P2 12:17, C2P2 12:49, C2P2 20:16, C2P2 21:24, C2P2 21:58

**Contexto.** Craftech estima con AWS Pricing Calculator (el ejemplo es una ml.m5.xlarge 8 horas por día durante 22 días). La ejecución del lab salió muy poco, pero 30 jobs de 10 instancias son 100 horas por día, y con GPU se dispara. El docente aclara que no podés limitar el gasto en duro: tenés alertas, billing y Budgets. Una empresa mediana gasta 20.000 o 30.000 por mes en AWS y alguien de FinOps mira métricas como "nunca llegaste al 50% de CPU" para bajar de instancia. Para cobrarle a cada cliente usás tags (el ejemplo es Epec) filtrados en Cost Explorer, o una cuenta por cliente. La anécdota de Winclap muestra el otro lado: migrar a SageMaker y pagar solo cuando está prendido salió más barato que bloquear una máquina personal.

**Por qué importa.** En la nube el gasto crece en silencio, sobre todo con tuning y GPU, y como no hay un corte automático tenés que enterarte a tiempo.

**Cómo implementarlo.**
1. Estimá cada carga en Pricing Calculator antes de levantarla.
2. Creá un Budget mensual con alertas.
3. Etiquetá todos los recursos con cliente y proyecto, y revisá Cost Explorer por tag.
4. Una vez por mes, revisá el uso de CPU de instancias y endpoints y bajá las que están sobredimensionadas.
5. Si trabajás para varios clientes, evaluá una cuenta por cliente.
- **Para verificar:** las cifras que dio en clase (una instancia de 1152 GB de RAM por 250 USD por mes, "estamos por la M6", la capa gratuita de S3) (C2P2 7:50, C2P2 14:28, C2P1 50:03).
- **Sugerencia:** poné alertas del Budget en varios escalones (por ejemplo 50%, 80% y 100%) para tener tiempo de reaccionar antes de pasarte.

### 8. Servicios administrados contra modelos propios
**Dónde:** C1P1 25:03, C2P2 42:31, C2P2 43:06, C2P2 1:09:12, C3P1 18:17, C3P1 1:01:26, C3P1 1:04:48, C3P2 22:58, C3P2 23:30

**Contexto.** Un argumento que vuelve en todo el curso: los servicios específicos (Rekognition, Polly, Transcribe, Comprehend, Lex) están pensados para escalar y suelen ser más baratos que un modelo fundacional para una tarea puntual. Pero a muy gran escala el sobreprecio de Amazon (5 o 10%) importa, y ahí puede convenir levantar tu propio modelo en SageMaker. Polly es tan barato que "casi ni te conviene hostear el tuyo". Para modelos generativos, entrenar el propio tiene sentido cuando gastás cientos de miles de dólares en tokens.

**Por qué importa.** Elegir mal es pagar de más o mantener infraestructura que no necesitabas.

**Cómo implementarlo.**
- Tarea simple y volumen bajo o medio: servicio administrado.
- Modelo chico o que tiene que correr en el dispositivo: local.
- Volumen enorme con gasto alto y estable: evaluá un modelo propio en SageMaker.
- Combiná: primero lo barato y local, y lo difícil al servicio administrado (él lo hace con OCR local y Rekognition para 1 de cada 10 casos).
- **Sugerencia:** antes de decidir, calculá el costo por unidad (por imagen, por minuto de audio, por consulta) a tu volumen real, no al de una prueba.

### 9. Rekognition con S3 y Lambda
**Dónde:** C2P2 36:15, C2P2 45:57, C2P2 46:31, C2P2 47:36, C2P2 48:17, C2P2 49:56, C2P2 51:41, C2P2 59:19, C2P2 1:25:54, C2P2 1:27:31

**Contexto.** El patrón es: una imagen entra a S3, dispara una Lambda que llama a Rekognition y las etiquetas se guardan en una base de datos para buscar después. La Lambda se prende y se apaga, y pagás por imagen procesada y por segundo de servidor. Para moderación, el ejemplo es un certificado médico: si Rekognition dice que no lo es, se le devuelve al usuario. Guardar los tags en S3 "no es lo ideal"; para búsqueda están Elasticsearch u OpenSearch. Rekognition devuelve etiqueta, confianza y bounding box; él toma desde 70% para aceptar un objeto. En colecciones de caras, ajustá MaxFaces y definí un umbral (por ejemplo 90%) para no aceptar caras parecidas.

**Por qué importa.** Te da análisis de imágenes a escala sin manejar cómputo ni entrenar un modelo desde cero.

**Cómo implementarlo.**
1. Creá un bucket de entrada.
2. Configurá un evento de S3 que invoque una Lambda por cada objeto nuevo.
3. En la Lambda, llamá a Rekognition con boto3 y filtrá por confianza mínima.
4. Guardá la URL de la imagen y sus etiquetas en una base de datos, o indexalas en OpenSearch si vas a buscar.
5. Si es moderación, devolvé el archivo o avisale al usuario cuando no cumple.
6. Para caras, creá una colección, indexá varias fotos por persona (frontal, de costado, con accesorios) y usá un umbral alto.
- **Para verificar:** la capa gratuita de "5000 imágenes al mes durante 12 meses" y la función específica para DNI que mencionó (C2P2 1:17:55, C2P2 1:08:39).
- **Sugerencia:** guardá también la respuesta completa de Rekognition, no solo la etiqueta ganadora, para poder recalibrar el umbral sin volver a pagar el análisis.

### 10. Chatbot transaccional con Lex
**Dónde:** C3P1 1:12:23, C3P1 1:21:05, C3P1 1:34:18, C3P1 1:39:09, C3P1 1:42:44, C3P1 1:55:47, C3P1 1:58:58, C3P1 2:03:21, C3P1 2:05:36, C3P1 2:06:40, C3P1 2:11:04

**Contexto.** El lab del módulo 6 arma un bot de turnos con Lex y una Lambda, y una web estática en S3 que habla con el bot usando un identity pool de Cognito. Los servicios se conectan con roles de IAM. Cada alias del bot es un despliegue distinto y puede usar otra Lambda. El docente defiende el bot clásico porque responde muy rápido, con cientos de miles de requests gana por poco cómputo, y conversar con un generativo gasta tokens cuando solo querés un booking. El bot del lab es primitivo: los horarios están fijos en la Lambda.

**Por qué importa.** Para flujos cerrados (reservar, consultar un estado, "marque uno") un bot clásico es barato y predecible.

**Cómo implementarlo.**
1. Diseñá los intents y las frases de ejemplo.
2. Creá el bot y, si falla la creación del rol, usá uno existente.
3. Escribí la Lambda de fulfillment con su rol de ejecución.
4. Reemplazá los horarios fijos por una consulta a una base o API de disponibilidad.
5. Creá un alias por entorno o canal.
6. Para la web, configurá el bucket con hosting estático (index.html y error.html), la bucket policy con el ARN correcto y, en el HTML, el bot ID, el alias ID, la región y el identity pool.
- El bucket público está bien para el lab pero es mala práctica en general (C3P1 1:53:29).
- Si necesitás conversación libre, el paso siguiente es un modelo agéntico con RAG (secciones 13 a 16), que Lex puede invocar (C3P1 1:38:35, C3P2 28:23).
- **Sugerencia:** registrá qué frases no matchean ningún intent; esa lista te dice qué flujos agregar y si hace falta pasar a algo generativo.

### 11. Elegir modelo en Bedrock midiendo, no por moda
**Dónde:** C4P1 5:30, C4P1 6:04, C4P1 6:38, C4P1 7:09, C4P1 7:41, C4P1 10:28, C4P1 22:36, C4P1 23:09, C4P1 35:40, C4P1 36:14, C4P1 48:17, C4P1 49:54

**Contexto.** El AI engineer elige el modelo. Con boto3 mandás un mensaje y la respuesta te dice los tokens de entrada y salida; la demo compara la misma frase en varios modelos. Los criterios son calidad, latencia y costo: un análisis de vulnerabilidades nocturno puede usar un modelo pesado porque no importa el tiempo, pero no tiene sentido usar el modelo más caro para mandar mails. Un modelo nuevo puede gastar más y dar lo mismo, así que actualizar siempre no es la mejor estrategia. Los parámetros de inferencia (temperatura, top P, top K, max tokens) ajustan el comportamiento sin redesplegar. Recomienda Converse en lugar de InvokeModel.

**Por qué importa.** El costo de un modelo generativo depende de los tokens y del modelo, y la diferencia entre elegir bien y mal se multiplica por cada consulta.

**Cómo implementarlo.**
1. Armá un set chico de consultas reales de tu caso.
2. Corrélas con Converse contra dos o tres modelos, incluyendo versiones chicas o Lite.
3. Anotá tokens de entrada y salida, latencia y una nota de calidad.
4. Elegí por caso de uso, y enrutá tareas distintas a modelos distintos.
5. Ajustá temperatura y max tokens antes de pensar en fine tuning.
- **Para verificar:** que InvokeModel "ya medio no se usa", el cambio del parámetro system "desde Opus 4" y las comparaciones entre versiones de Opus que nombró (C4P1 48:17, C4P1 50:27, C4P1 6:04).
- **Sugerencia:** guardá ese set de consultas como prueba fija y volvé a correrlo cada vez que salga un modelo nuevo, para decidir con números si vale la pena cambiar.

### 12. Presupuesto de tokens, caché y lotes
**Dónde:** C4P1 31:51, C4P1 32:23, C4P1 32:55, C4P1 33:28, C4P1 36:53, C4P1 1:11:28, C4P1 1:11:59, C4P1 1:13:06, C4P1 1:22:33, C4P1 1:23:07, C4P1 1:23:41

**Contexto.** Pagar menos no es elegir el modelo más barato. El docente propone: presupuesto de tokens por caso (un bot de turnos con 500, y alerta al 90% si se pasa), max tokens bajo para respuestas cortas (500 da dos renglones, 5000 lo deja explayarse), caché de respuestas cuando el output se repite aunque cambie el input (Converse tiene caché), inferencia por lotes en horarios de poco uso, Spot, regiones más baratas e inference profiles con enrutamiento entre regiones. No cachees cuando los datos vienen de una API que cambia todo el tiempo.

**Por qué importa.** El gasto en tokens escala con el uso y, si no lo medís por caso de uso, no sabés dónde se va.

**Cómo implementarlo.**
1. Definí max tokens por caso de uso según el largo de respuesta que necesitás.
2. Medí el consumo real por caso y poné una alerta cerca del límite.
3. Identificá preguntas repetidas y servilas desde un caché, salvo que los datos cambien seguido.
4. Mandá por lotes lo que no necesita respuesta inmediata.
5. Evaluá inference profiles o regiones más baratas si tu caso lo permite.
- **Para verificar:** que los proveedores privados "cachean pero cobran como si no", el ahorro de "hasta 90%" con modelos locales y la duración de los inference profiles (C4P1 32:23, C4P1 36:53).
- **Sugerencia:** guardá en cada respuesta si vino del caché o del modelo, así podés medir cuánto te ahorra el caché de verdad.

### 13. Guardrails delante del modelo
**Dónde:** C4P1 41:47, C4P1 42:20, C4P1 43:25, C4P1 44:28, C4P1 45:01, C4P1 45:32, C4P2 23:35, C4P2 25:20, C4P2 25:52, C4P2 29:45, C4P2 30:49, C4P2 31:20, C4P2 56:17

**Contexto.** Un guardrail es un modelo muy chico que filtra input y output, "como un patovica de boliche". En Bedrock es un servicio propio: le das el contexto del negocio, una severidad y políticas (contenido filtrado, temas denegados, palabras clave, información sensible, contexto). Bloquea prompt injection, temas fuera del negocio y datos como email, teléfono o patrones PCI. Si filtrás con el system prompt del modelo grande, ya "moviste un titán" y gastaste tokens; el guardrail consume mucho menos (habla de 4% en benchmarks). En la demo, cuando bloquea, el consumo de tokens es cero. Un ataque puede venir dentro de un documento, como una foto de DNI con un prompt: el OCR lo hace el modelo, así que conviene una IA intermedia que abra el documento y lo pase por un guardrail. Recomienda un guardrail por caso (ventas, cliente) y usar el trace y los logs para ajustarlo.

**Por qué importa.** Protege la información del negocio y ahorra tokens en las preguntas que no deberían llegar al modelo.

**Cómo implementarlo.**
1. Definí el alcance del asistente en una frase (por ejemplo, solo atención al cliente de tu empresa).
2. Creá un guardrail con temas denegados, filtros de contenido y patrones de datos sensibles.
3. Asocialo en la llamada a Converse y activá el trace.
4. Si procesás documentos o imágenes, extraé el texto en un paso intermedio y pasalo por el guardrail antes del modelo principal.
5. Revisá los logs de bloqueos y ajustá la severidad.
- **Para verificar:** los niveles de severidad que recordó (low, medium, high y uno sin validación) y el 4% de consumo (C4P1 43:56, C4P1 45:32).
- **Sugerencia:** armá una lista de prompts de ataque y de preguntas legítimas, y corrélas cada vez que cambiás el guardrail para ver que no bloquea de más ni de menos.

### 14. RAG con knowledge bases, solo cuando hace falta
**Dónde:** C4P1 1:28:19, C4P1 1:29:26, C4P1 1:43:46, C4P1 1:53:36, C4P1 1:54:41, C4P2 0:01, C4P2 0:33, C4P2 2:14, C4P2 2:46, C4P2 4:27, C4P2 8:13, C4P2 9:47, C4P2 11:27, C4P2 44:16, C4P2 48:45

**Contexto.** El RAG le da al modelo información actualizada o propia del negocio. En Bedrock, la knowledge base administrada arma los embeddings con Titan y los chunks, usa como data source S3 u otras fuentes (Confluence, SharePoint, Salesforce, un crawler, una API) y guarda los vectores en S3 Vectors, OpenSearch, Aurora, Neptune, Pinecone o Redis. Puede devolver la URL del documento como cita. Es común usar una IA intermedia que reformula la pregunta para la búsqueda. S3 Vectors es barato y más lento; OpenSearch es el más rápido. Las fallas típicas son chunks cortados, contexto irrelevante, información vieja y citas inventadas. No conviene RAG si la información entra en el prompt o no hay grandes volúmenes, porque un RAG siempre agrega tokens. En la demo, una pregunta sobre devoluciones consumió 3000 tokens.

**Por qué importa.** Bien usado evita reentrenar; mal usado agrega costo y respuestas con contexto equivocado.

**Cómo implementarlo.**
1. Preguntate primero si la información entra en el system prompt; si entra, no armes RAG.
2. Subí los documentos a S3 y creá la knowledge base con Titan como modelo de embeddings.
3. Para laboratorio usá S3 Vectors; si necesitás velocidad a escala, OpenSearch.
4. Ajustá el tamaño de los chunks y cuántos resultados devuelve.
5. En el system prompt, indicá que responda solo con el contexto y que diga que no sabe si no lo encuentra.
6. Pedí las citas y mostralas.
7. Evaluá con preguntas cuya respuesta ya conocés, y medí tokens por respuesta.
- **Para verificar:** que OpenSearch es "lo más rápido que hay" y el costo de S3 que dio ("20 centavos por giga", que contradice la cifra de la clase 2) (C4P1 1:44:18, C4P1 1:46:28).
- **Sugerencia:** guardá junto con cada respuesta los IDs de los chunks recuperados, así cuando una respuesta sale mal sabés si falló la búsqueda o la generación.

### 15. Datos para la IA: capa gold, SQL acotado y umbral por campo
**Dónde:** C4P2 6:02, C4P2 15:55, C4P2 17:36, C4P2 19:15, C4P2 19:47, C4P2 22:30, C4P2 26:58, C4P2 28:38, C4P2 50:50

**Contexto.** La arquitectura medallón separa bronce (crudo), silver (limpio) y gold (sumarizado). La IA debería trabajar sobre gold porque no tiene datos sensibles y cuesta menos: en la demo, la misma pregunta contra la capa de detalle tardó 10% más y consumió muchos más tokens, aun con pocos registros. Si la IA genera SQL, el riesgo es prompt injection para obtener el esquema, columnas expuestas o demasiadas filas; la mitigación es darle la query armada para que solo complete el WHERE. Athena permite consultar archivos de S3 con SQL pagando por consulta. Para facturas con formatos distintos está Bedrock Data Automation. En la extracción, cada campo tiene su umbral: el CUIT pide 0,98 y los ítems pueden ir más bajos. Un LLM juez (por ejemplo Sonnet) puede validar las respuestas.

**Por qué importa.** Lo que le das a la IA define el costo, la latencia y el riesgo de fuga.

**Cómo implementarlo.**
- Armá vistas o tablas gold específicas para cada caso de IA, sin datos personales.
- Si necesitás SQL, usá queries parametrizadas con columnas fijas.
- Para documentos no estructurados en S3, probá Bedrock Data Automation antes de programar un parser.
- Definí un umbral de confianza por campo crítico.
- Sumá un paso de validación con otro modelo o con reglas.
- **Sugerencia:** registrá cuántas filas y columnas devuelve cada consulta de la IA y alertá si se sale del rango esperado.

### 16. Agentes con permisos mínimos
**Dónde:** C4P1 59:21, C4P1 59:54, C4P2 33:00, C4P2 34:15, C4P2 37:34, C4P2 38:08, C4P2 39:12, C4P2 41:21, C4P2 42:27, C4P2 43:00, C4P2 45:31

**Contexto.** La IA no es determinística como un script, así que hay que aplicar mínimo privilegio: el agente que lee el RAG solo puede leer ese RAG. En el ejemplo multiagente de cotizar un vuelo hay un orquestador, un investigador que consulta la API de vuelos, un cotizador que va a RDS y otros que iteran (comercial, diseñador, QA), cada uno con el modelo que le conviene. MCP es la forma de declararle las tools a cada agente. El riesgo es que un atacante le pregunte al agente qué tools tiene y le ordene, por ejemplo, cambiar precios, o que use la red compartida para moverse lateralmente. Por eso hay que tratar a los agentes como usuarios, limitar llamadas con API Gateway y poner guardrails en cada salto. La demo usa Lambda, Bedrock, DynamoDB, S3 Vectors y tools declaradas en código con boto3, y se despliega con CDK.

**Por qué importa.** "Si dejaste una puerta abierta, van a llegar." Un agente con permisos amplios es una puerta abierta.

**Cómo implementarlo.**
1. Dibujá los agentes y qué necesita cada uno.
2. Creá un rol de IAM por agente con solo esas acciones (lectura donde alcanza lectura).
3. Declarale solo sus tools.
4. Poné un límite de llamadas en la entrada y un guardrail entre agentes.
5. Separá redes si los agentes acceden a servicios internos.
6. Elegí el modelo de cada agente según su tarea y costo.
- **Sugerencia:** probá cada agente pidiéndole explícitamente que liste sus tools y que haga algo fuera de su rol; si lo logra, el permiso está de más.

### 17. Observabilidad y evaluación continua
**Dónde:** C4P1 1:01:34, C4P1 1:02:07, C4P1 1:03:12, C4P1 1:03:45, C4P1 1:06:32, C4P1 1:25:17, C4P1 1:26:24, C4P2 7:40, C4P2 31:54

**Contexto.** A gran volumen hay que mirar consumo de tokens, accesos no controlados y tasa de errores. CloudTrail muestra quién usó qué API key; el registro de invocaciones guarda el prompt de entrada y salida con sus tokens; CloudWatch da logs y métricas como latencia. El docente admite que estas herramientas no están maduras y que es fácil perder de vista dónde se van los tokens. Para evaluar prompts propone un dataset de prueba, versiones del prompt, el pulgar arriba o abajo de los usuarios y un juez. Las knowledge bases tienen scoring de recuperación y generación, y los logs de guardrails sirven para reentrenar.

**Por qué importa.** Sin medir no podés justificar el costo ni detectar cuando un cambio empeora las respuestas.

**Cómo implementarlo.**
- Activá CloudTrail y el registro de invocaciones del modelo.
- Armá un tablero en CloudWatch con tokens por caso de uso, latencia y errores.
- Guardá un catálogo versionado de prompts y un set de prueba (C4P1 1:21:26).
- Corré el set de prueba con un juez cada vez que cambiás prompt, modelo o knowledge base.
- Según el resultado, ajustá el RAG, cambiá el modelo o dividí un agente en dos.
- **Sugerencia:** guardá el feedback de los usuarios junto con el ID del prompt y del modelo usados, para saber qué versión produjo cada respuesta mala.

---

## Glosario de nombres (la transcripción automática los deforma)

| En la transcripción | Probablemente es |
|---|---|
| Sagem Maker, S Maker | SageMaker |
| UniFi Studio | SageMaker Unified Studio |
| Yam, esam | IAM |
| Resft, Rift, RIP, Res | Redshift |
| FCX | FSx |
| Atina | Athena |
| Recognillo | — |
| Textra | Textract |
| Comprehead, comprejet | Comprehend |
| Poli | Polly |
| Transcrive | Transcribe |
| Brock, Bedro, BRCK | Bedrock |
| W race, W rail, Wrail, War Rails, Warray | Guardrails |
| Bedings | Embeddings |
| RAE, RAL, RAC | RAG |
| Norge Base | Knowledge base |
| BR Data Automas | Bedrock Data Automation |
| Asian Core, Cord, agent Core | Bedrock AgentCore |
| Jumpstar, JStar | SageMaker JumpStart |
| Trade Newum | Trainium |
| Transobre | AWS Transform (dudoso) |
| Kira, Kir… | Kiro |
| Neptun | Neptune |
| Lin, L chain | LangChain |
| Last privilege | Least privilege |
| quid | CUIT |
| Wingler, Winclub | Winclap |
| Regi | Dudoso, sin identificar |
| Timestam | Timestream (dudoso) |
| Fable, Fabel, Luna, Sol, Opus 5, Opus 4.8 | Dudoso; nombres de modelos que hay que confirmar |
| Fratching | Dudoso; una técnica para reducir costos mencionada junto al caché |
| trans | Dudoso; un framework agéntico |
