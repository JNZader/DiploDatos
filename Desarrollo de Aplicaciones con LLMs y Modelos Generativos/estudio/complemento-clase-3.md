# Complemento de la clase 3: introducción a RAG (C3P1) y CRAG (C3P4)

**Esto completa** `apunte-de-estudio.md` y `guia-de-implementacion.md`, que tenían dos huecos en la clase 3 (18/09/2026): la primera hora y el cierre sobre CRAG. El 02/10/2026 pude bajar los subtítulos automáticos en español de C3P1 (1:00:58) y de C3P4 (14:22) sin iniciar sesión ni usar cookies, en reintentos espaciados. Este archivo resume esas dos partes con el mismo formato del apunte: lo que se dice en clase, con el minuto exacto, y al final preguntas de repaso. No modifica los archivos anteriores; donde algo de acá los corrige, lo aclaro.

> Nota: sale de subtítulos automáticos, así que muchos términos vienen deformados ("RAC" o "rack" por RAG, "F tuning" por fine-tuning, "fish shot" por few-shot, "chanking" por chunking, "threcho" por threshold). Los resolví en la tabla del final. Lo marcado como **para verificar** es una cifra o afirmación que el docente da de memoria; cuando ya la verifiqué en `parte-2-verificacion.md`, lo digo. La explicación de CRAG (C3P4) está en las secciones K y L.

---

## Dónde encaja

C3P1 es la teoría de RAG que C3P2 da por vista cuando arranca con la arquitectura de dos etapas. Llena el "hueco de transcripción" del **módulo 16 del apunte (RAG: arquitectura y contrato de fundamentación)** y le da contexto al módulo 9 (la escalera de soluciones) y al 11 (ventana de contexto y lost in the middle). En la guía de implementación, cubre lo que falta antes de la sección de RAG que arranca en C3P2. Tiene cuatro bloques de contenido: el caso de estudio de la clase 3, la analogía del examen a libro abierto, por qué un LLM no puede ser fuente de verdad y cuándo conviene RAG frente al contexto extenso y al fine-tuning. Los primeros cinco minutos son organización del curso. C3P4 (secciones K y L) llena lo que el **módulo 19 del apunte (Lab 3 y CRAG)** daba por inferido: cómo funciona el evaluador de CRAG, qué es el RAG agéntico y cómo cierra la clase.

---

## A. Organización del curso

**Dónde:** C3P1 1:45, C3P1 2:21, C3P1 2:52, C3P1 3:26, C3P1 3:58, C3P1 4:31

- El docente usa la planilla de grupos para ver el avance. Le preocupa que haya menos grupos de los que esperaba y que algunos no hayan empezado, o no hayan actualizado la planilla C3P1 1:45.
- La entrega del trabajo queda para el 19 de octubre, "de acá a un mes" C3P1 2:21. No se cierra en esa fecha y entregar un poco después no tiene consecuencias, pero hay tiempos administrativos fijos: la diplomatura necesita todas las notas la última semana de noviembre para armar la cohorte que se gradúa C3P1 2:52, C3P1 3:26. Si necesitás más tiempo, pedilo y se pacta una fecha nueva C3P1 3:58.
- Para completar grupos (idealmente de cuatro), anotate en una fila vacía de la planilla y contactá a esas personas por Slack C3P1 4:31.

---

## B. El problema: el contexto de toda la organización

**Dónde:** C3P1 6:25, C3P1 6:55, C3P1 8:00, C3P1 9:40, C3P1 10:13, C3P1 10:46, C3P1 11:20

- **Repaso.** La clase 1 fueron los fundamentos (cómputo, memoria, cuantización, costos, correr modelos en tu propia máquina) y la clase 2, prompt engineering: los cinco principios, el razonamiento guiado y la salida estructurada para que otros sistemas puedan consumir la respuesta C3P1 6:25, C3P1 6:55, C3P1 8:00.
- **Qué contexto le falta al modelo.** No el de los ejemplos del few-shot (in-context learning), sino toda la información de la organización: PDFs, bases de datos, data lakes, documentos de Word o Google Docs, archivos de texto C3P1 9:40, C3P1 10:13.
- **Por qué no entra en el prompt.** Son volúmenes que el modelo no puede procesar como entrada o que, si puede, sale muy caro cargar enteros para responder cada pregunta C3P1 10:13, C3P1 10:46.
- **La alternativa cara.** Reentrenar el modelo con toda la información de la organización sería quizás el ideal, pero el costo de entrenar y de preparar los datos es "extremadamente alto". Ahí aparece RAG C3P1 11:20.

---

## C. El caso Vertex Horizon Seguros

**Dónde:** C3P1 11:53, C3P1 12:27, C3P1 13:01, C3P1 13:36, C3P1 14:11, C3P1 14:43, C3P1 15:18, C3P1 15:51, C3P1 16:24, C3P1 16:58, C3P1 17:31, C3P1 18:04, C3P1 18:36

**Corrección al apunte y a la guía.** El glosario de los dos archivos anteriores dice que "Vertex Horizon" es una confusión del docente con Fintech Horizon. No lo es: en C3P1 el docente presenta Vertex Horizon Seguros como el caso nuevo de la clase 3, una aseguradora inventada (eligió un nombre inventado para no usar uno real), y aclara que no se acuerda del nombre del caso anterior C3P1 11:53. Por eso en C3P2 habla del "chatbot de Vertex Horizon" C3P2 34:10, y el lab 3 usa un manual de pólizas.

- **El sistema.** Un asistente para consultas sobre coberturas, normativas y siniestros, conectado a un proceso que liquida pólizas C3P1 12:27.
- **El incidente.** Alguien pregunta si una póliza contratada en 2024 cubre inundaciones extraordinarias en zona rural, "según las modificaciones que dictó el directorio el mes pasado". El sistema responde que sí, con cobertura del 100%, una justificación legal redactada y un número de circular. La persona confía, liquida la indemnización y se pierden miles de dólares: era un falso positivo C3P1 13:01, C3P1 13:36, C3P1 14:11. El propio docente dice que el caso es "bastante ciencia ficción" C3P1 12:27.
- **Qué falló, según el docente.**
  1. **Nunca vio el manual actualizado.** La modificación del directorio no llegó al sistema, o el sistema no pudo recuperarla, y el modelo respondió con lo estadísticamente más probable C3P1 14:43, C3P1 15:18.
  2. **El conocimiento queda congelado.** Aunque hubieran hecho fine-tuning, el modelo ajustado queda fijo en el tiempo: podés volver a entrenarlo, pero volvés a pagar y volvés a quedar desactualizado C3P1 15:18, C3P1 15:51.
  3. **Rellenó el hueco.** En vez de decir "no sé", inventó un número de circular y lo justificó. Para el docente, el modelo no tiene herramientas para reflexionar sobre lo que entrega, porque solo produce el siguiente token más probable. Eso es una alucinación C3P1 15:51, C3P1 16:24, C3P1 16:58.
- **La salida.** Darle al modelo acceso a una biblioteca y exigirle que diga exactamente de dónde saca cada dato. Eso es un sistema RAG: técnicamente una base vectorial, que podés pensar como una base de conocimiento a la que se consulta por semántica, no por palabra o índice C3P1 17:31, C3P1 18:04. Con las fuentes citadas, la persona puede ir a chequear C3P1 18:36.
- La clase sigue con fundamentos y pipeline de RAG, chunking y recuperación, patrones y el lab, y hay un glosario en las diapositivas C3P1 18:36, C3P1 19:08.

---

## D. Libro cerrado contra libro abierto

**Dónde:** C3P1 19:41, C3P1 20:14, C3P1 20:49, C3P1 21:22, C3P1 21:57, C3P1 22:31, C3P1 23:04, C3P1 23:37, C3P1 24:09, C3P1 24:44

- **La analogía.** Un LLM sin RAG rinde a libro cerrado; con RAG, a libro abierto. "No vamos a cambiar al alumno ni lo vamos a hacer estudiar de nuevo": solo le dejamos abrir el manual antes de contestar C3P1 19:41, C3P1 20:14. Aclara que rendir a libro abierto no es necesariamente más fácil.
- **Libro cerrado.** La pregunta va al LLM, que responde solo con su memoria interna. El ejemplo: le preguntan quién es el último campeón del mundial masculino y responde Argentina en Qatar 2022, porque se entrenó antes del Mundial 2026. La respuesta es verosímil y probable, con riesgo de alucinación y de datos desactualizados C3P1 20:49, C3P1 21:22.
- **Libro abierto.** Antes de llegar al modelo, un proceso hace una búsqueda semántica en una base de fragmentos almacenados C3P1 21:22, C3P1 21:57. La respuesta no es pegar un bloque atrás de otro: el modelo construye la respuesta con ese contexto. Eso es el LLM fundamentado C3P1 21:57, C3P1 22:31.
- **Qué ganás.** Una respuesta mejor, verificable (cita las fuentes exactas) y actualizada, siempre que la base de conocimiento esté al día: es "la base de verdad", y lo que no está ahí no se puede recuperar C3P1 22:31, C3P1 23:04.
- **No hay reentrenamiento.** El modelo no memoriza nada nuevo: los pesos son los mismos y solo cambia el contexto. Es in-context learning, igual que el few-shot, pero ahora le das información para fundamentar en vez de ejemplos C3P1 23:37, C3P1 24:09. El few-shot dinámico de la clase 2 se termina de entender acá, porque elige los ejemplos con la misma clase de recuperación C3P1 24:09, C3P1 24:44.

**Tip del docente.** Si vas a usar RAG, exigile al modelo que cite de dónde sacó cada dato; eso es lo que convierte una respuesta verosímil en una verificable C3P1 17:31, C3P1 22:31.

---

## E. Qué errores comete todavía un RAG

**Dónde:** C3P1 25:16, C3P1 25:50, C3P1 26:25, C3P1 27:00, C3P1 27:35, C3P1 28:09, C3P1 28:43, C3P1 29:16, C3P1 29:49, C3P1 30:20, C3P1 30:54, C3P1 31:27, C3P1 32:00

- El docente pregunta: en un examen a libro abierto igual podés equivocarte, ¿dónde puede fallar un RAG? C3P1 25:16, C3P1 25:50
- **Matías** cuenta que investiga AI Gateways y guardrails de entrada para un RAG con documentación sensible (propiedad intelectual, ciberseguridad), y plantea que el RAG puede devolver una respuesta genérica que no corresponde a su caso C3P1 26:25, C3P1 27:00. El docente lo reformula: la base de conocimiento puede no tener información suficiente para la pregunta C3P1 27:35.
- **La búsqueda siempre devuelve algo.** "Lo más parecido" no quiere decir "casi igual": si no hay nada parecido, el sistema responde igual, con un score más bajo, porque son distancias en un espacio C3P1 28:09, C3P1 28:43.
- **El umbral es difícil.** ¿Desde qué score algo deja de ser relevante: 1, 0,5, 0,2? No es fácil de responder C3P1 29:16.
- **La cantidad también.** Si no le ponés límite, puede traer muchos fragmentos. La idea es combinar un top-K (por ejemplo, cinco) con un umbral de score: "de esos cinco, todos los que superen" cierto valor C3P1 29:49, C3P1 30:20. Esto es lo que después mide la evaluación y lo que CRAG trata de resolver.
- **Francisco** suma la falta de estructura de los documentos; el docente dice que eso lo cubre el chunking C3P1 30:54, C3P1 31:27.
- **El capítulo equivocado.** Como en un examen, podés buscar en el capítulo de introducción, donde el tema aparece en un párrafo, y responder vago. Un RAG puede recuperar información parecida pero no exacta, o directamente no tenerla C3P1 31:27, C3P1 32:00.

**Tip del docente.** Además de pedir K fragmentos, cortá por score; y probá el umbral con tus datos, porque no hay un valor universal C3P1 29:16, C3P1 30:20. La sección 3 de `parte-2-verificacion.md` muestra cómo medirlo con un set de evaluación.

---

## F. Por qué un LLM no puede ser fuente de verdad

**Dónde:** C3P1 32:00, C3P1 32:31, C3P1 33:03, C3P1 33:37, C3P1 34:10, C3P1 34:41, C3P1 35:14, C3P1 35:48

| Razón | Qué dice la clase |
|---|---|
| Corte de conocimiento | Hay datos que el modelo no conoce C3P1 32:31 |
| Sin datos privados | Ningún modelo que bajes tiene los datos privados de tu organización; con suerte, algo de lo público entró al entrenamiento C3P1 32:31, C3P1 33:03 |
| Compresión con pérdida | Al guardar información en sus pesos, el modelo la comprime y pierde detalle. Si metés un contrato en un fine-tuning, no lo vas a poder recuperar palabra por palabra. RAG guarda el texto tal como está y le asocia un vector de embedding que le da semántica al párrafo C3P1 33:37, C3P1 34:10, C3P1 34:41 |
| Alucinación sin cita | Te da cualquier dato, lo más probable, sin sustento C3P1 34:41 |

- **La que más cara sale es la cuarta.** Las tres primeras producen ignorancia, que se puede manejar. La cuarta "convierte la ignorancia en una afirmación con formato de dato verificado": respuestas que parecen reales y están justificadas, pero detrás solo hay tokens probables C3P1 35:14.
- Que el sistema diga "no lo sé" es lo deseable, pero sin contexto el modelo nunca puede determinar que no sabe C3P1 35:48.

---

## G. Contexto extenso, RAG o fine-tuning: la tabla de decisión

**Dónde:** C3P1 36:22, C3P1 36:55, C3P1 37:28, C3P1 38:01, C3P1 38:33, C3P1 39:07, C3P1 39:40, C3P1 40:15, C3P1 40:49

- RAG no resuelve todos los problemas: sirve donde un LLM puro falla y un fine-tuning es demasiado caro C3P1 36:22, C3P1 36:55.
- **"Prompting con contexto extenso"** es tirar todos los documentos en el system prompt. Hay ventanas de hasta un millón de tokens C3P1 36:55, C3P1 37:28. Ya verificado en el anexo: OpenAI publica 1,05 millones y Anthropic 1 millón para sus modelos insignia.

| Dimensión | Contexto extenso | RAG | — |
|---|---|---|---|
| Límite | La ventana de contexto C3P1 37:28 | El tamaño de la base | Los costos C3P1 40:15 |
| Actualización | Inmediata: cambiás un documento y la próxima consulta ya lo usa C3P1 38:01, C3P1 38:33 | Hay que volver a ingestar | Semanas C3P1 40:15 |
| Trazabilidad | Alta pero acotada: el modelo te dice de qué documento, pero le cuesta decir qué línea o párrafo C3P1 38:33, C3P1 39:07 | Mejor: permite llegar a la fuente exacta C3P1 39:07 | Ninguna: el texto exacto "se diluyó" C3P1 40:15 |
| Esfuerzo de montaje | Mínimo: adjuntás y listo C3P1 39:40 | Más elevado: ingesta, chunking, base vectorial C3P1 39:40 | El más alto C3P1 40:15 |
| Costo por consulta | Elevado y lineal: si entran 1000 consultas, pagás 1000 veces los documentos C3P1 39:40, C3P1 40:15 | Bajo, porque solo viaja lo pertinente C3P1 40:15 | Inversión inicial fuerte, después la inferencia es barata C3P1 40:49 |

- **El ejemplo de contexto extenso que sí conviene.** Las preguntas frecuentes de una organización, 10 o 20 carillas, unos 10.000 a 30.000 tokens, con pocas consultas por día: podés pagar ese costo en cada consulta C3P1 38:01. El número coincide con mi cálculo del anexo: con los precios de Gemini 3.8 Flash y caché, el contexto largo cuesta lo mismo que un RAG típico cerca de los 30.000 tokens (ver "Análisis adversario" en `parte-2-verificacion.md`). Lo que la tabla del docente no considera es el caché de prompts, que baja mucho el "costo elevado y lineal" cuando el documento no cambia.
- **La regla de oro.** El fine-tuning sirve para cambiar comportamiento, tono, estilo y sobre todo jerga: que el modelo aprenda el vocabulario de la medicina o del derecho. RAG sirve para hechos. No compiten: responden preguntas distintas C3P1 40:49, C3P1 41:22, C3P1 41:54.
- **El camino.** Una prueba de concepto con prompt engineering, después RAG y un sistema agéntico (el harness, que le da más capacidades al sistema sin cambiar el modelo), y fine-tuning si todo eso falla. En la práctica se combinan C3P1 42:27, C3P1 42:59, C3P1 43:34.

---

## H. ¿Para qué RAG si hay ventanas de un millón de tokens?

**Dónde:** C3P1 43:34, C3P1 44:07, C3P1 44:39, C3P1 45:12, C3P1 45:44, C3P1 46:17, C3P1 46:51, C3P1 47:24, C3P1 48:00, C3P1 48:34, C3P1 49:06, C3P1 49:43

- El docente plantea la pregunta descartando el costo: supongamos que todo entra en la ventana y estás dispuesto a pagarlo, o que corre en tu infraestructura C3P1 44:07, C3P1 44:39, C3P1 45:12.
- **Eric** cuenta que trabaja en una empresa de ciencias del comportamiento que hace experimentos en contextos bancarios y financieros, y que quieren una "base de inteligencia" conversacional con 5 o 6 años de experimentos, sin perder de dónde salió cada dato. Por eso arman un RAG C3P1 45:12, C3P1 45:44, C3P1 46:17. El docente lo resume como calidad de recuperación y trazabilidad C3P1 46:17.
- **Latencia.** Con todo en el prompt, el modelo tiene que procesar toda la entrada: hoy puede ser del orden de segundos o de un minuto. La búsqueda vectorial tarda milisegundos y el prompt queda chico, así que podés tener la respuesta "un orden de magnitud" antes, por ejemplo en 6 segundos en vez de un minuto (**para verificar**; es un ejemplo ilustrativo, depende del modelo y del caché) C3P1 46:51, C3P1 47:24, C3P1 48:00.
- **Lost in the middle.** Cuando la ventana se llena, el modelo no le presta la misma atención al principio, al medio y al final; lo sufren todos los LLM en mayor o menor medida. Con RAG le das solo lo relevante C3P1 48:34, C3P1 49:06. El paper es [Liu y otros (2023)](https://arxiv.org/abs/2307.03172); el anexo suma NoLiMa y RULER, que miden cuánto cae la precisión con contextos largos.
- **Resumen del docente:** RAG ahorra dinero, baja la latencia y le da al modelo un mecanismo para concentrar la atención en lo importante C3P1 49:43.

---

## I. Cuándo entra la información: offline contra online

**Dónde:** C3P1 50:14, C3P1 50:47, C3P1 51:19, C3P1 51:52, C3P1 52:26, C3P1 52:59, C3P1 53:32, C3P1 54:04, C3P1 55:09, C3P1 55:43, C3P1 56:17, C3P1 56:49, C3P1 57:25, C3P1 57:57

- **Antonio** pregunta en qué momento recibe el sistema la documentación en cada enfoque C3P1 50:14, C3P1 50:47, C3P1 51:19. Respuesta corta: en RAG es un proceso offline, previo a usar el sistema C3P1 51:52.
- **Fine-tuning** es darle el libro al alumno para que lo memorice como pueda; después no tiene más información C3P1 52:26.
- **RAG** es el mismo alumno, sin memorizar, al que le decís "andá a consultar el índice del libro cuando lo necesites". Ese índice semántico se construyó antes, offline C3P1 52:26, C3P1 52:59.
- **Contexto extenso** es adjuntar todos los archivos en el momento de la consulta, como hace Antonio con hojas de datos de componentes electrónicos en ChatGPT C3P1 53:32, C3P1 54:04. Todo vive en la misma sesión; si salís, tenés que volver a cargar los archivos C3P1 55:09.

**Demo conceptual: el pipeline de RAG, en palabras del docente.**
1. Offline: los archivos van a un proceso que los parte en fragmentos C3P1 55:43.
2. Offline: para cada fragmento calcula un vector de embedding y guarda los dos en la base vectorial C3P1 55:43, C3P1 56:17.
3. Online: la pregunta se convierte en vector con el mismo modelo y se buscan los fragmentos más parecidos, por ejemplo cinco C3P1 56:17, C3P1 56:49.
4. Online: se arma un prompt que concatena esos fragmentos con la instrucción de responder con esa información y citar de dónde salió, aplicando los principios de prompt engineering de la clase 2 C3P1 56:49, C3P1 57:25.

- **La diferencia de fondo.** Con contexto extenso, el modelo decide qué es relevante; con RAG, lo decide el sistema de recuperación antes de llegar al modelo C3P1 57:25, C3P1 57:57.

Para el detalle de cada paso (limpieza, chunking, metadatos, top-K), seguí con el módulo 16 del apunte, que arranca en C3P2.

---

## J. Modelos chicos y RAG local

**Dónde:** C3P1 57:57, C3P1 58:33, C3P1 59:06, C3P1 59:40, C3P1 1:00:17

- Los modelos grandes procesan contextos largos de forma robusta; los chicos razonan peor con mucho contexto y además tienen ventanas más cortas, "un cuarto o un octavo" de las grandes C3P1 57:57, C3P1 58:33.
- Dice que el modelo del lab, "si no me equivoco, el 2.5", tiene 128K tokens de ventana (**para verificar**) C3P1 58:33. **Verificado: no para el modelo del lab.** El [`config.json` de Qwen2.5-3B-Instruct](https://huggingface.co/Qwen/Qwen2.5-3B-Instruct/blob/main/config.json) fija 32.768 tokens de contexto, unas 32 veces menos que el millón de los modelos grandes, no "un octavo". No revisé las ventanas de los Qwen2.5 más grandes.
- RAG funciona con modelos que corren en una GPU local, a costo cero o al costo de mantener la infraestructura, mientras que el flujo de "adjuntar todo" necesita un modelo grande como Sol, "Terra" (probablemente Astra) o Luna de OpenAI, u Opus de Anthropic C3P1 59:06, C3P1 59:40, C3P1 1:00:17.
- Antes del recreo muestra la diapositiva de catálogo offline y consulta online, que es donde arranca C3P2 C3P1 1:00:17.

**Tip del docente.** Si querés correr el sistema en tu propia GPU, RAG es lo que lo hace viable: el modelo chico solo tiene que procesar lo relevante C3P1 59:06, C3P1 59:40.

<details>
<summary>Preguntas de repaso de C3P1 (con respuestas)</summary>

1. **¿Qué tres cosas fallaron en el caso Vertex Horizon Seguros?** El sistema nunca vio la modificación del directorio, el conocimiento del modelo estaba congelado y, en vez de decir "no sé", inventó una circular con su justificación.
2. **¿Qué significa "libro abierto" en la analogía?** Que el modelo no cambia ni estudia de nuevo: antes de responder, un proceso busca en una base de fragmentos y le pasa lo relevante.
3. **¿RAG reentrena el modelo?** No. Los pesos son los mismos; es in-context learning con información recuperada.
4. **¿Por qué un RAG puede traer fragmentos irrelevantes?** Porque la búsqueda semántica siempre devuelve lo más cercano, aunque no haya nada parecido, solo que con un score más bajo.
5. **¿Cómo se limita lo que trae la recuperación?** Combinando un top-K con un umbral de score, aunque elegir el umbral es difícil.
6. **De las cuatro razones por las que un LLM no es fuente de verdad, ¿cuál sale más cara y por qué?** La alucinación, porque convierte la ignorancia en una afirmación con formato de dato verificado.
7. **¿Por qué el fine-tuning no sirve para recuperar un contrato textual?** Porque guardar información en los pesos es una compresión con pérdida; RAG guarda el texto tal cual.
8. **¿Cuándo conviene el contexto extenso en vez de RAG?** Con pocos documentos (por ejemplo unas preguntas frecuentes de 10.000 a 30.000 tokens), pocas consultas y necesidad de actualización inmediata.
9. **Según la regla de oro, ¿para qué sirve el fine-tuning y para qué RAG?** Fine-tuning para comportamiento, tono, estilo y jerga; RAG para hechos.
10. **Aunque todo entre en la ventana y el costo no importe, ¿qué dos razones da el docente para seguir usando RAG?** La latencia (búsqueda en milisegundos y prompts cortos) y lost in the middle.
11. **¿En qué momento recibe el sistema los documentos en RAG?** En un proceso offline previo, que los parte, calcula embeddings y los guarda en la base vectorial.
12. **¿Por qué RAG es especialmente útil con el modelo del lab?** Porque los modelos chicos tienen ventanas más cortas (32.768 tokens en Qwen2.5-3B) y razonan peor con mucho contexto, y RAG les pasa solo lo relevante.

</details>

---

## Términos deformados en C3P1

| En la transcripción | Qué es |
|---|---|
| RAC, rack, RAX | RAG (retrieval-augmented generation) |
| F tuning, fine tube | — |
| F shot, fish shot, fusot, fusion dinámico, fich dinámico | Few-shot y few-shot dinámico |
| incttext learning | In-context learning |
| chanking | Chunking |
| threcho, thos | Threshold (umbral) |
| loss in the middle, iningid | Lost in the middle |
| jarnes | Harness |
| Herga | Jerga |
| LLN, LDM | LLM |
| Warrail | Guardrail |
| IA Gateway | AI Gateway |
| prom engineering, Pro engineering, PR engineering | Prompt engineering |
| Appic Cloud | Probablemente "APIs en la nube" (dudoso) |
| alucinación sincita | Probablemente "alucinación sin cita" (dudoso) |
| Terra | Probablemente GPT-6 Astra, de OpenAI, que publica Astra, Sol y Luna (dudoso) |
| Vertex Horizon Seguros | El caso de la clase 3, una aseguradora inventada (corrige el glosario del apunte y de la guía) |

---

## K. CRAG: evaluar lo recuperado antes de responder (C3P4)

**Dónde:** C3P4 0:14, C3P4 0:50, C3P4 1:24, C3P4 1:57, C3P4 2:30, C3P4 3:06, C3P4 3:39, C3P4 4:14, C3P4 4:46, C3P4 5:19, C3P4 5:52, C3P4 6:25, C3P4 6:58, C3P4 7:31, C3P4 8:02

> Fuente: C3P4 (14:22), que también pude bajar el 02/10/2026 en un reintento espaciado, sin cookies. Es el cierre de la clase 3, después del lab. Llena lo que el apunte daba por inferido sobre CRAG (el lab 3 lo anuncia en C3P3 2:49).

### El problema que resuelve
- La base vectorial responde con un ranking: los K fragmentos más parecidos a la pregunta, por ejemplo cinco C3P4 0:14, C3P4 0:50.
- Si la base es de pólizas de seguro y el usuario pregunta "cuál es el valor de mercado del vehículo X", la base devuelve igual cinco fragmentos, porque siempre devuelve los K más cercanos, aunque no tengan nada que ver C3P4 1:24, C3P4 1:57. Es lo mismo que se planteó en C3P1 (sección E).
- Ahí entra una etapa de **evaluación** entre la recuperación y el armado del contexto, con dos enfoques C3P4 1:57.

### Enfoque 1: umbrales
- Después de probar y conocer tu sistema, fijás un corte: por ejemplo, todo fragmento por debajo de 0,6 queda afuera. El evaluador es el paso que mira los scores y descarta C3P4 2:30, C3P4 3:06.
- No es flexible: si lo subís mucho (0,8) dejás afuera cosas relevantes, y si lo bajás mucho (0,3) entra basura y el evaluador pierde sentido C3P4 3:06, C3P4 3:39.
- Una referencia que da: mayor a 0,7 es confiable, entre 0,3 y 0,7 es ambiguo y menor a 0,3 es incorrecto, aunque "para un problema diferente podría cambiar" (**para verificar**; depende del modelo de embedding y de la métrica) C3P4 3:39, C3P4 4:14.
- Sigue siendo un corte duro: lo que queda en el borde puede producir errores C3P4 4:14.

### Enfoque 2: un modelo evaluador
- Un segundo modelo que hace de evaluador "externo": no recibe todo el contexto, sino información muy específica (la consulta y lo recuperado) C3P4 4:14, C3P4 4:46.
- Puede evaluar incluso antes de recuperar, para decidir si la consulta es relevante para el dominio del sistema C3P4 4:46.
- Puede ser un LLM chico, o el mismo LLM con otro rol y otro system prompt con instrucciones expresas C3P4 4:46, C3P4 5:19. O un modelo chico (SLM) entrenado por la organización solo para clasificar "relevante, ambiguo, no relevante" C3P4 5:19, C3P4 5:52.
- Sea por umbral, por LLM o por otro algoritmo de machine learning, el objetivo es que el LLM que responde reciba un contexto mejor y dé respuestas más robustas C3P4 5:52, C3P4 6:25.

### Los caminos según el resultado
| Resultado del evaluador | Qué se hace |
|---|---|
| Relevante | Se ensambla el contexto y se responde C3P4 6:25 |
| — | Se descarta, y se le devuelve feedback al usuario: "no entiendo, dame más detalles" o "este sistema es solo para consultar contratos" C3P4 6:25, C3P4 8:02 |
| Ambiguo | Se podría buscar en una fuente externa de contingencia; existe en la práctica, pero "no es lo habitual" C3P4 6:58, C3P4 7:31 |

- **Tip del docente.** Si tenés una fuente externa que te ayude a desambiguar, usala; si no, no. El camino habitual es el evaluador más la repregunta al usuario C3P4 7:31, C3P4 8:02.
- **Por qué importa.** Darle al usuario una respuesta que no tiene nada que ver te puede meter en un problema legal; el evaluador es un mecanismo para atrapar eso antes C3P4 8:02.

**Contraste con el paper (ya verificado en el anexo).** La idea coincide con [CRAG (Yan y otros, 2024)](https://arxiv.org/abs/2401.15884): un evaluador de recuperación liviano devuelve un grado de confianza que dispara distintas acciones, y usa búsquedas web para ampliar lo recuperado. La búsqueda web es justamente la "fuente externa de contingencia" que el docente considera poco habitual. Los umbrales exactos que usa el paper no los verifiqué, porque leí solo el resumen. La sección 6 de `parte-2-verificacion.md` trae un ejemplo de código para el lab.

---

## L. RAG agéntico, evaluación y cierre (C3P4)

**Dónde:** C3P4 8:38, C3P4 9:12, C3P4 9:45, C3P4 10:19, C3P4 10:53, C3P4 11:27, C3P4 12:04, C3P4 12:37, C3P4 13:09, C3P4 13:43, C3P4 14:16

- **RAG agéntico.** Una tabla de las diapositivas agrega "agentic RAG", que no se experimenta en el curso: el sistema no es un pipeline que produce una salida y la entrega, sino que lo recuperado puede disparar otros procesos, por ejemplo un revisor parecido al de CRAG pero que consulta otras fuentes C3P4 8:38, C3P4 9:12.
- Se va a entender mejor con el patrón ReAct de la clase 4: razonar si el contexto es correcto y, si no, actuar yendo a buscar a otra fuente C3P4 9:12, C3P4 9:45. También puede haber un bucle en el que varios agentes validan la respuesta antes de entregarla, con roles distintos C3P4 10:19, C3P4 10:53.
- **Tip del docente.** Los RAG reales no caen en estas tres categorías: lo construís según tus necesidades. Lo útil es quedarse con dos ideas, el corrector como filtro previo a armar el contexto y el agéntico como bucle que valida antes de entregar C3P4 9:45, C3P4 10:19.
- **Evaluación.** No llega a dar la parte de calidad. Menciona Ragas ("ragaz") como framework para evaluar sistemas RAG, y repite que la evaluación es necesaria y fundamental; hay herramientas comerciales y open source para evaluación, observabilidad y trazabilidad, y para obtener métricas a partir de los logs ("luz" en la transcripción, dudoso) C3P4 10:53, C3P4 11:27. Para configurarlo, ver la sección 3 del anexo (promptfoo, Ragas y DeepEval).
- **Cierre.** Le faltaron 10 a 15 minutos de diapositivas, que considera las menos relevantes C3P4 12:04. En el aula virtual, la pestaña que antes se llamaba "práctica" ahora se llama "teoría y labs" y tiene las presentaciones con sus notas del orador; falta subir la cuarta C3P4 12:37, C3P4 13:09, C3P4 13:43. Queda debiendo compartir el "Gemini Notebook" cargado con la bibliografía C3P4 13:43. Esto confirma la resolución del anexo: "cuaderno de Gemini" es Gemini Notebook, el ex NotebookLM.

<details>
<summary>Preguntas de repaso de C3P4 (con respuestas)</summary>

1. **¿Por qué una base vectorial puede devolver cinco fragmentos irrelevantes?** Porque siempre devuelve los K más cercanos, aunque la pregunta no tenga nada que ver con lo que hay en la base.
2. **¿Dónde se ubica el evaluador de CRAG?** Entre la recuperación y el armado del contexto; también puede evaluar la consulta antes de recuperar.
3. **¿Qué problema tiene el enfoque por umbral?** Es un corte duro: alto deja afuera cosas relevantes, bajo deja entrar basura, y lo que queda en el borde produce errores.
4. **¿Qué referencia de umbrales da el docente?** Más de 0,7 confiable, entre 0,3 y 0,7 ambiguo y menos de 0,3 incorrecto, aclarando que depende del problema.
5. **¿Qué opciones hay para el modelo evaluador?** Un LLM chico, el mismo LLM con otro rol y system prompt, o un SLM entrenado por la organización para clasificar relevante, ambiguo o no relevante.
6. **¿Qué se hace con un resultado irrelevante?** Se descarta y se le pide al usuario más detalle o se le aclara para qué sirve el sistema.
7. **¿Qué es el RAG agéntico?** Un RAG en el que lo recuperado puede disparar otros procesos (revisores, búsquedas en otras fuentes, agentes que validan) antes de entregar la respuesta.
8. **¿Qué framework menciona para evaluar RAG?** Ragas.

</details>

---

## Términos deformados en C3P4

| En la transcripción | Qué es |
|---|---|
| Correptic Rack, correcting rack | Corrective RAG (CRAG) |
| Gentic RAC, gentic rack | Agentic RAG |
| bedings, embría | Embeddings |
| por un bra | Por un umbral |
| ragaz | Ragas |
| Yemini Notebook | Gemini Notebook (ex NotebookLM) |
| luz | Probablemente "logs" (dudoso) |
| llone, llorbral | LLM (deformado) |
