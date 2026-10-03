# Complemento: los dos videos de 2020 que no tenían subtítulos (Ética Práctica para Ciencia de Datos)

**Esto completa** `etica-practica-ciencia-de-datos-apunte-de-estudio.md`, que no pudo resumir dos videos cortos de 2020 porque la grabación no les ofrecía subtítulos: "Ejercicios de pensamiento de la Caja de Herramientas Humanísticas" (QhFDdA5-r9k, 8:32, subido el 08/12/2020) y "Barreras a los cambios para soluciones más éticas y consensos sociales sobre qué es bueno" (A7YL-D601BA, 18:05, subido el 09/12/2020). Los dos los da Laura Alonso Alemany, según la descripción de cada video, para la cohorte 2020 de la diplomatura. En el apunte, el módulo 12 los cubría solo a partir del título, la descripción y los capítulos; este archivo reemplaza esa parte inferida por lo que efectivamente se dice.

> Nota: estas transcripciones salen de una **transcripción automática del audio** que hice el 02/10/2026 con faster-whisper (modelo `small`, idioma español, en la CPU del box), no de subtítulos de la grabación. Están en `/workspace/yt/transcript_QhFDdA5-r9k.txt` y `/workspace/yt/transcript_A7YL-D601BA.txt`. La calidad es aceptable pero tiene errores de palabras (por ejemplo "get keeping" por *gatekeeping* o "DNA" por DNI), y en el video de barreras, desde el minuto 7 más o menos, los tiempos quedan en saltos regulares de 2 segundos, así que tomalos como aproximados (unos segundos de diferencia). Donde interpreto una palabra deformada lo marco como dudoso. Los links siguen la convención del apunte: "2020-Caja 4:15" lleva al minuto 4:15 del video en la grabación.

---

## 12a. Ejercicios de pensamiento de la Caja de Herramientas Humanísticas (2020-Caja)

**Dónde:** 2020-Caja 0:23 a 2020-Caja 8:25. Es un "video de precalentamiento": un tráiler de un documento que Laura quiere que leas entero.

### Conceptos clave
- **Qué es la Caja.** Laura la presenta como el primer recurso de la página de la materia, "en castellano" y hecho en el país, por el grupo GIFT, al que ubica en el Instituto de Investigaciones Filosóficas y en la Universidad de Buenos Aires: "un grupo de filósofos que trabaja de forma muy concreta" con problemas de ética de la IA 2020-Caja 0:23, 2020-Caja 0:43, 2020-Caja 0:50. La página del grupo confirma que GIFT es el Grupo de Investigación de Inteligencia Artificial, Filosofía y Tecnología, con sede en SADAF, y que sus integrantes son Karina Pedace, Tomás Balmaceda, Diana Pérez y Diego Lawler ([grupo.gift](https://grupo.gift/)). La portada del PDF suma a Maximiliano Zeller Echenique y dice "En colaboración con fAIr LAC".
- **Para qué sirven los ejercicios de pensamiento.** Son estudios de caso que "nos ayudan a llevar a cosas más concretas estos principios generales que por ahí están dando vueltas" 2020-Caja 1:37, 2020-Caja 1:45. La Caja tiene dos partes: reflexiones filosóficas sobre la IA y el diseño de artefactos, y cinco problemas (sesgos, privacidad, transparencia, responsabilidad y seguridad); cada problema trae un caso hipotético.
- **No es un resumen, es un tráiler.** Laura cierra pidiendo que leas la Caja entera, no solo los casos, porque tiene "mucha contextualización y mucha profundización sobre conceptos que son fundamentales" y es "muy fácil de leer" 2020-Caja 7:21, 2020-Caja 7:51, 2020-Caja 8:04.

### Los cuatro casos que cuenta
Laura los cuenta de memoria y los adapta. Al lado pongo cómo están en el PDF, porque hay diferencias que vale la pena notar.

| Caso | Cómo lo cuenta Laura | Cómo está en la Caja | Pregunta que deja |
|---|---|---|---|
| Créditos automatizados (sesgos) | Un banco chico tiene que dar muchos créditos rápido "como si hubiera una pandemia" y automatiza la evaluación. ¿Podría el código postal negar un crédito porque la gente de ese barrio históricamente no devolvió? ¿Hay que tratar distinto a distintos solicitantes? ¿Qué datos son sensibles y no deberían ir "a Amazon" sin encriptar? ¿Quién garantiza todo eso, el Estado o la institución? 2020-Caja 1:51, 2020-Caja 2:37, 2020-Caja 3:20, 2020-Caja 3:37, 2020-Caja 3:53 | Un banco **provincial** lanza créditos blandos para personas de bajos recursos en una crisis económica y compra un modelo de scoring que asiste a quien decide. El texto suma un ejemplo argentino: en el conurbano, como muchas jefas de hogar son trabajadoras no registradas, el modelo podría excluirlas y profundizar la "feminización de la vulnerabilidad" | ¿Cómo evitás que la automatización discrimine sistemáticamente, y quién responde por eso? |
| A.L.F.R.E.D. (privacidad) | Un asistente de voz como Alexa que solo graba al escuchar su palabra clave. ¿Y si en la casa hay violencia doméstica? ¿Debería llamar a la policía o grabar? 2020-Caja 4:08, 2020-Caja 4:23, 2020-Caja 4:49, 2020-Caja 5:08 | El PDF agrega dos vueltas: quien configura el aparato probablemente sea quien ejerce la violencia, y del otro lado, ¿está preparado el 911 para recibir llamadas automáticas? | ¿Vale más la privacidad o la integridad de una persona? ¿Quién te autoriza a incluir esa función? |
| App de Chagas (transparencia) | Una app indica el riesgo de tener Chagas con "85%" de certeza; debería usarla un médico, pero un gobierno provincial la compra, mucha gente no sabe leer, la usa sola, comparte el celular y acepta los términos sin leerlos 2020-Caja 5:18, 2020-Caja 5:33, 2020-Caja 5:53, 2020-Caja 6:10, 2020-Caja 6:22 | La empresa "HealthCare" detecta con 85% de certeza la presencia de triatominos analizando imágenes de saliva; un **país** latinoamericano compra diez mil licencias y las reparte con folletos en mercados y bares; no hay médicos disponibles y la gente reemplaza el análisis por lo que dice la app | ¿Alcanza con que el instructivo y los términos digan cómo usarla? |
| Exoesqueleto (responsabilidad) | Un exoesqueleto para levantar cargas necesita una actualización que las empresas no pueden pagar porque "está todo muy caro"; un trabajador muere por una falla 2020-Caja 6:35, 2020-Caja 6:52, 2020-Caja 7:02 | "HER-CULES", de la empresa Hefestus; la portuaria Container S.A. deja de actualizar porque cada actualización cuesta en moneda extranjera, y un operario **lastima gravemente** a un compañero (no muere) | ¿Quién es responsable: quien diseñó, quien vende con actualización paga, quien dejó de comprarla o quien lo usaba? |

### Ejercicios para hacer vos
1. **Llevá un caso a tu práctico.** Elegí el caso que más se parezca a tu dataset y escribí, en una línea cada uno, quién se beneficia, quién se puede dañar si el sistema funciona bien y quién si falla. Son las mismas tres preguntas que Luciana usa para analizar las secciones de ética en los artículos (módulo 4 del apunte).
2. **Encontrá el proxy.** En el caso de los créditos, el código postal funciona como un proxy de clase social o de origen. Buscá en tu dataset una columna que pueda hacer lo mismo con un dato sensible de la ley 25.326 (origen, salud, religión, opinión política, vida sexual).
3. **Reescribí A.L.F.R.E.D. con la ley argentina.** ¿El consentimiento de quien instala el aparato cubre a las otras personas de la casa? Conectalo con el principio de consentimiento informado, libre y expreso (módulo 2 del apunte).
4. **Cadena de responsabilidad.** Para el exoesqueleto, ordená a los cuatro actores de más a menos responsable y justificá. Después cambiá un dato (por ejemplo, que la actualización fuera gratis) y fijate si cambia el orden.

### Tips de la docente
- Leé la Caja completa: el tráiler no reemplaza el desarrollo conceptual 2020-Caja 7:51.
- El link al PDF que figura en la descripción del video (en `guia.ai`) hoy no funciona, porque el dominio redirige a una página vacía. El mismo PDF está en [proyectoguia.lat](https://proyectoguia.lat/wp-content/uploads/2020/05/Caja-de-herramientas-Humanistas.pdf) (lo abrí el 02/10/2026; la versión es "V8", del 27/04/2020).

<details>
<summary>Preguntas de repaso del módulo 12a (con respuestas)</summary>

1. **¿Quién hizo la Caja de Herramientas Humanísticas y por qué la recomienda la materia?** El grupo GIFT, de filósofas y filósofos argentinos; Laura la pone primera en los recursos porque está en castellano, es local y trabaja los problemas de forma concreta 2020-Caja 0:33, 2020-Caja 0:43.
2. **¿Qué es un ejercicio de pensamiento en este contexto?** Un caso hipotético que baja a lo concreto un principio general, como la no discriminación o la privacidad 2020-Caja 1:37.
3. **¿Qué variable aparentemente inocente puede discriminar en el caso de los créditos?** El código postal, porque arrastra la historia de los barrios 2020-Caja 2:37.
4. **¿Qué dilema plantea A.L.F.R.E.D.?** Privacidad contra integridad: si el asistente debería activarse ante una situación de violencia doméstica aunque esté diseñado para no escuchar 2020-Caja 4:49, 2020-Caja 5:08.
5. **¿Por qué la app de Chagas falla aunque tenga instructivo?** Porque el contexto de uso real (personas que no leen, celulares compartidos, sin médico) no es el previsto, y aceptar los términos no garantiza que se entiendan 2020-Caja 6:10, 2020-Caja 6:22.
6. **¿Qué pregunta deja el exoesqueleto?** De quién es la responsabilidad cuando el daño viene de una actualización que no se compró 2020-Caja 7:02.

</details>

---

## 12b. Barreras a los cambios y consensos sociales sobre qué es bueno (2020-Barreras)

**Dónde:** 2020-Barreras 0:00 a 2020-Barreras 18:03. Capítulos del video: introducción (0:00), cómo nos afecta la IA (3:02), "tres sencillos trucos para mantener el status quo" (9:45) y Declaración de Montreal (15:34). Ojo: según la transcripción, los "trucos" empiezan antes de la marca del capítulo, cerca de 2020-Barreras 7:15; el capítulo de Montreal sí coincide.

### Conceptos clave
- **Del diagnóstico a lo constructivo.** Después de ver casos para encontrar problemas, Laura quiere "desnaturalizar cosas que están funcionando muy bien en nuestra área" y que son obstáculos para avanzar en ética 2020-Barreras 0:00, 2020-Barreras 0:14, 2020-Barreras 0:28.
- **Sí, es tan grave.** Retoma el video "Bueno, pero ¿es tan grave?" para contestar que sí: los sistemas basados en datos están en todas partes, afectan derechos fundamentales y consensos sociales muy establecidos, sus efectos perniciosos se pueden objetivar, y llegan de forma sutil, lo que es más peligroso porque "se hacen carne en nuestro comportamiento" 2020-Barreras 0:54, 2020-Barreras 1:18, 2020-Barreras 1:28, 2020-Barreras 1:58, 2020-Barreras 2:09. Además, cuando alguien los cuestiona, aparecen estrategias sistemáticas para desactivar ese cuestionamiento 2020-Barreras 2:20.
- **Innovadora en atentar contra derechos.** La IA no inventa la discriminación, porque replica las que ya existen, pero sí innova en "la concentración con la que lo hacen" y en los lugares donde lo hace: frente a una máquina esperamos "ingenuamente" objetividad 2020-Barreras 3:06, 2020-Barreras 3:29, 2020-Barreras 3:39, 2020-Barreras 3:54. Enumera los efectos: censura automática sin derecho a apelar, detenciones porque "una máquina dijo", decisiones condicionadas por recomendaciones, señalamiento de individuos "anormales" que impacta en cuotas, persecuciones y acceso a educación o crédito, y el ambiente 2020-Barreras 4:03, 2020-Barreras 4:15, 2020-Barreras 4:23, 2020-Barreras 4:35, 2020-Barreras 4:46, 2020-Barreras 5:03.
- **"Pero es tan cómodo."** La primera barrera es la comodidad de quien decide: "¿no estás dispuesto a que tu crédito se resuelva más rápido?", total lo más probable es que discriminen a otro, y si te toca a vos "sabés apelar" 2020-Barreras 5:07, 2020-Barreras 5:27, 2020-Barreras 5:43, 2020-Barreras 5:54. Con el reconocimiento facial: si me detienen por error, muestro el DNI y es "un mal trago", pero "a personas de piel mucho más oscura les va a pasar mucho más" 2020-Barreras 6:09, 2020-Barreras 6:19, 2020-Barreras 6:26. Quienes toman decisiones están cómodos, y hay quien cree que su privilegio es merecido y hace mucho para que todo siga igual: "cambiar todo para no cambiar nada" 2020-Barreras 6:30, 2020-Barreras 6:51, 2020-Barreras 7:07, 2020-Barreras 7:13.

### Los "sencillos trucos" para que nada cambie
El capítulo dice tres, pero Laura enumera más; los agrupo como los cuenta. Dice que funcionan sobre todo con personas sin perfil técnico 2020-Barreras 7:31, 2020-Barreras 7:41.

| Truco | Cómo suena | Por qué es un truco | Dónde |
|---|---|---|---|
| *Gatekeeping* por complejidad | "Esto es superdifícil, es una red neuronal convolucional, ¿cómo vamos a poner reglas ahí?" | Dificulta que otras personas entren a la toma de decisiones (la transcripción dice "get keeping") | 2020-Barreras 7:43, 2020-Barreras 7:53, 2020-Barreras 8:07 |
| "Los datos son así" | "No es que yo lo haya hecho mal, los datos dicen esto, por algo será" | Es "la gran Poncio Pilatos": me lavo las manos | 2020-Barreras 8:19, 2020-Barreras 8:27, 2020-Barreras 8:33 |
| Eludir la responsabilidad | "Mejor pedir perdón que pedir permiso"; "no es la IA la sesgada, es la sociedad" | Laura lo compara con "no son las pistolas las que matan, es la gente": sin pistolas se salva más gente. El sustantivo que usa está deformado en la transcripción ("habitaciones de responsabilidad"; dudoso, quizás "evitaciones") | 2020-Barreras 8:39, 2020-Barreras 8:53, 2020-Barreras 9:13, 2020-Barreras 9:25, 2020-Barreras 9:33 |
| Vacíos legales | "Si nadie dijo que no se puede, se puede"; "es tu opinión, la ley no dice exactamente esto" | Agarrarse de la letra de la ley y no de su espíritu | 2020-Barreras 9:45, 2020-Barreras 9:55, 2020-Barreras 10:01 |
| "Cuando pase, lo arreglamos" | Mejor poner a alguien que solucione los problemas cuando aparezcan que gastar en prevenirlos | Solucionar un problema "es tremendamente distinto" a que el problema no exista, sobre todo para quien es discriminado sistemáticamente | 2020-Barreras 10:07, 2020-Barreras 10:17, 2020-Barreras 10:25 |
| Determinismo | "Los humanos tenemos sesgos, es nuestro mecanismo de abstracción, el mundo es así" | Presenta como inevitable algo que se puede cambiar | 2020-Barreras 10:35, 2020-Barreras 10:41, 2020-Barreras 11:05, 2020-Barreras 11:09 |

- **Por qué te toca a vos.** Quienes trabajan en ciencia de datos tienen hoy "un cierto poder", y en su pequeño contexto pueden cambiar cosas, sobre todo porque la tecnología no mantiene todo igual sino que concentra las decisiones "cada vez más en menos personas" 2020-Barreras 11:19, 2020-Barreras 11:33, 2020-Barreras 11:41, 2020-Barreras 11:47, 2020-Barreras 11:57.

### Consensos sociales sobre qué es bueno
- **Lo que tiene rango de ley.** Muchos consensos tienen "rango de ley constitucional" en Argentina, que adhiere a la Declaración Universal de Derechos Humanos: no discriminación, condiciones de vida, educación, salud, trabajo, expresión, movimiento y reunión. Todas las soluciones que desarrollamos tienen que respetarlos, así que "no nos podemos hacer los boludos" sobre dónde está escrito 2020-Barreras 12:29, 2020-Barreras 12:35, 2020-Barreras 12:43, 2020-Barreras 13:01, 2020-Barreras 13:21.
- **Lo que sabemos por maduración social.** Cosas como la empatía, que sabemos que están bien aunque no estén en una ley 2020-Barreras 13:29, 2020-Barreras 13:35.
- **Lo que todavía no sabemos.** Sesgos emergentes que hoy no podemos identificar pero existen; lo ideal es estar preparados para reconocerlos, identificarlos y mitigarlos. Laura cuenta que mérito, privilegio, estereotipos e invisibilización no los tenía claros cuando empezó a trabajar en el área, hace 20 años 2020-Barreras 13:37, 2020-Barreras 14:01, 2020-Barreras 14:13, 2020-Barreras 14:21, 2020-Barreras 14:25.
- **Lo que afecta a una comunidad particular.** Para eso hay que incorporar diversidad en el equipo, tema que retoma en la charla metodológica 2020-Barreras 14:51, 2020-Barreras 15:01.
- **Para leer más.** Recomienda seguir a Martín Becerra, que cita legislación relevante, por ejemplo los artículos 19 y 20 sobre libertad de expresión (probablemente de la Declaración Universal, que tratan la libertad de expresión y la de reunión; dudoso) y el instrumento de derechos humanos al que adhiere Argentina (nombre deformado; dudoso) 2020-Barreras 15:13, 2020-Barreras 15:23, 2020-Barreras 15:29.

### La Declaración de Montreal y las cinco áreas
- **Montreal.** Recomienda la Declaración de Montreal para un desarrollo responsable de la IA, linkeada en la página de la materia. En 2020 dijo que no encontraba la versión en castellano y pidió que se la pasaran 2020-Barreras 15:37, 2020-Barreras 15:45, 2020-Barreras 15:49. Hoy el sitio oficial dice que está en 10 idiomas, entre ellos el español, y lista 10 principios: bienestar, respeto de la autonomía, protección de la intimidad, solidaridad, participación democrática, equidad, inclusión de la diversidad, prudencia, responsabilidad y desarrollo sostenible ([montrealdeclaration-responsibleai.com](https://montrealdeclaration-responsibleai.com/the-declaration/)).
- **Cinco áreas críticas.** Muestra un resumen de varias declaraciones que identifica cinco áreas de impacto social: transparencia, justicia y equidad, no maleficencia ("las cosas no pueden tener malas intenciones"), responsabilidad (*accountability*) y privacidad 2020-Barreras 15:59, 2020-Barreras 16:09, 2020-Barreras 16:23, 2020-Barreras 16:29, 2020-Barreras 16:35. No dice de dónde sale el resumen, pero las cinco coinciden exactamente con la convergencia que encontraron Jobin, Ienca y Vayena al mapear guías de ética de IA ([arXiv 1906.11668](https://arxiv.org/abs/1906.11668), Nature Machine Intelligence, 2019); es probable que sea esa la fuente (inferido).
- **Lo que viene.** La materia va a trabajar cómo, con perfil técnico, instrumentalizar esos consensos para explicitar, prevenir y mitigar, con dos herramientas: los *data statements* y la mitigación de sesgos en *word embeddings* 2020-Barreras 16:41, 2020-Barreras 17:07, 2020-Barreras 17:25, 2020-Barreras 17:35, 2020-Barreras 17:43.

### Ejercicios para hacer vos
1. **Cazá trucos.** Releé la discusión de tu grupo del práctico y marcá si alguien usó alguno de los seis trucos ("los datos son así", "es muy complejo", "lo arreglamos después"). Reescribí esa frase como una pregunta abierta.
2. **Del truco a la evidencia.** Para "los datos son así", la respuesta de la clase 2 es medir la amplificación: comparar la distribución de la etiqueta en los datos con la de las predicciones (módulo 6 del apunte). Si el modelo amplifica, ya no son "solo los datos".
3. **Mapeá tus consensos.** Para tu sistema, escribí una lista en tres columnas: lo que está en una ley (25.326, derechos constitucionales), lo que es consenso social sin ley y lo que todavía no sabés. La tercera columna es la que justifica tener diversidad en el equipo.
4. **Montreal contra tu sistema.** Elegí tres de los diez principios de Montreal y escribí una frase por cada uno sobre cómo los respeta o los viola tu sistema.

### Tips de la docente
- Desconfiá de la objetividad de la máquina: la discriminación automática es más difícil de ver porque no la esperamos 2020-Barreras 3:54.
- Si estás en el lugar de quien decide, preguntate si tu tranquilidad depende de que el error le toque a otra persona 2020-Barreras 6:30.
- Prevenir no es lo mismo que remediar: tener un canal de reclamos no reemplaza evitar el daño 2020-Barreras 10:23.

<details>
<summary>Preguntas de repaso del módulo 12b (con respuestas)</summary>

1. **¿En qué sentido la IA es "innovadora" en atentar contra derechos, si las discriminaciones ya existían?** En la concentración y en los lugares donde discrimina, donde esperamos objetividad de una máquina 2020-Barreras 3:29, 2020-Barreras 3:54.
2. **¿Qué libertades fundamentales limita, según Laura?** La de expresión, por censura automática sin apelación, y la libertad en general, por detenciones que nadie puede explicar 2020-Barreras 4:03, 2020-Barreras 4:15.
3. **¿Por qué la comodidad es una barrera?** Porque quien decide no suele ser quien sufre el error, y por eso no tiene incentivos para cambiar 2020-Barreras 5:43, 2020-Barreras 6:30.
4. **¿Qué es el *gatekeeping* en este contexto?** Usar la complejidad técnica para que personas sin perfil técnico no participen de las decisiones 2020-Barreras 7:53, 2020-Barreras 8:07.
5. **¿Qué responde Laura a "no es la IA la sesgada, es la sociedad"?** Que es como decir que las pistolas no matan; sin pistolas se salva más gente, y sin sistemas que amplifican el sesgo se discrimina menos 2020-Barreras 9:13, 2020-Barreras 9:33.
6. **¿Por qué "cuando pase lo arreglamos" no alcanza?** Porque solucionar un problema después es muy distinto a que el problema no exista, sobre todo para quien es discriminado de forma sistemática 2020-Barreras 10:23.
7. **¿Qué tipos de consensos sociales distingue?** Los que tienen rango de ley, los que sabemos por maduración social, los que todavía no conocemos y los que afectan a una comunidad particular 2020-Barreras 12:35, 2020-Barreras 13:29, 2020-Barreras 13:37, 2020-Barreras 14:51.
8. **¿Cuáles son las cinco áreas críticas que muestra?** Transparencia, justicia y equidad, no maleficencia, responsabilidad y privacidad 2020-Barreras 16:23.
9. **¿Qué dos herramientas anuncia para la clase siguiente?** Los *data statements* y la mitigación de sesgos en *word embeddings* 2020-Barreras 17:35, 2020-Barreras 17:43.

</details>

---

## Correcciones al apunte que salen de estas transcripciones

- **Módulo 12, capítulo de los "tres trucos".** El apunte decía que sin transcripción no se sabía cuáles eran. Ahora se sabe: *gatekeeping* por complejidad, "los datos son así", elusión de responsabilidad, vacíos legales, "lo arreglamos cuando pase" y determinismo.
- **Módulo 12, Montreal.** El apunte decía que el contenido de la declaración no estaba en la transcripción. Laura la recomienda sin desarrollarla, y la complementa con las cinco áreas críticas.
- **Glosario, "tomás balmaseda".** Es Tomás Balmaceda, integrante de GIFT ([grupo.gift](https://grupo.gift/)), lo que encaja con que Laura cite su caso de la Smart TV en el video "¿Es tan grave?".
- **Glosario, "Grupo Gift".** Es GIFT, Grupo de Investigación de Inteligencia Artificial, Filosofía y Tecnología, con sede en SADAF.

## Palabras deformadas en estas transcripciones

| En la transcripción | Qué es | Dónde |
|---|---|---|
| grupo GIFT | GIFT (Grupo de Investigación de Inteligencia Artificial, Filosofía y Tecnología) | 2020-Caja 0:43 |
| Alfred | A.L.F.R.E.D., el asistente de voz del caso de privacidad | 2020-Caja 4:15 |
| — | Exoesqueleto ("HER-CULES" en el PDF) | 2020-Caja 6:35 |
| servidumbre del 85% | "Certeza" del 85%, según el PDF | 2020-Caja 5:33 |
| get keeping | *Gatekeeping* | 2020-Barreras 8:07 |
| DNA | DNI | 2020-Barreras 6:15 |
| la gran poncio pilatos | Poncio Pilatos, lavarse las manos | 2020-Barreras 8:33 |
| gran pro hombre | Prohombre | 2020-Barreras 8:47 |
| habitaciones de responsabilidad | Dudoso; probablemente evitaciones o elusiones de responsabilidad | 2020-Barreras 8:43 |
| errorismo sistemático | Dudoso | 2020-Barreras 9:07 |
| Lúvia | Luciana | 2020-Barreras 12:23 |
| la Martín Becerra | Martín Becerra, investigador en comunicación y medios | 2020-Barreras 15:15 |
| declaración de monreal | Declaración de Montreal | 2020-Barreras 15:37 |
| caja de herramientas de sinceridad | Dudoso; quizás "de ciencia de datos" | 2020-Barreras 17:11 |
| pideitos | Probablemente "videítos" | 2020-Barreras 16:49 |
