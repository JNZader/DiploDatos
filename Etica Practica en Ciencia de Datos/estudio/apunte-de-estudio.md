# Apunte de estudio: Ética Práctica para Ciencia de Datos (FAMAF UNC, Laura Alonso Alemany y Luciana Benotti)

**Curso:** Ética Práctica para Ciencia de Datos, materia de la diplomatura en ciencia de datos de FAMAF (UNC) · Docentes: Laura Alonso Alemany ("Lau") y Luciana Benotti ("Lu"), profe de FAMAF e investigadora del CONICET en procesamiento de lenguaje natural · Coordinación: Caro · Formato: dos clases sincrónicas del 21 y 22 de agosto de 2026, grabadas en 4 videos no listados del canal de FAMAF, más 5 videos cortos de 2020 del canal de la Diplomatura en Ciencia de Datos que la materia sigue recomendando.
**De qué va:** la materia enseña a mirar un sistema de ciencia de datos preguntando a quién puede dañar y cómo detectarlo antes de que llegue a producción. Arranca con incidentes reales (subsidios en Países Bajos, un chatbot de empleo en Austria, un chatbot de salud en España) y con la ley argentina de protección de datos personales, sigue con los daños de la IA generativa, las marcas de agua y los datos sintéticos, y propone construir tu propia definición de ética. La clase 2 es la parte práctica: sesgo y amplificación, escenarios de daño, métricas de equidad desagregadas por grupo con una notebook sobre COMPAS, auditoría de sistemas generativos y de embeddings, y diversidad a lo largo de todo el ciclo de vida. El práctico es un data statement sobre el dataset de tu mentoría.

> Nota: este apunte sale de los subtítulos automáticos en español de los videos. **Faltan dos transcripciones:** las de los videos de 2020 "Ejercicios de pensamiento de la Caja de Herramientas Humanísticas" (QhFDdA5-r9k, 8:32) y "Barreras a los cambios para soluciones más éticas y consensos sociales sobre qué es bueno" (A7YL-D601BA, 18:05), porque esos dos videos no tienen subtítulos en la grabación; de ellos solo se usa lo que dicen su título, su descripción y sus capítulos, y está marcado como inferido. La segunda parte de la clase 1 (C1P2) sí está, después de varios reintentos espaciados. La transcripción del video "¿Es tan grave?" es de baja calidad. Muchos nombres vienen deformados (ver el glosario al final). Todo lo que figura acá es lo que se dice en clase o en los videos; las cifras, fechas, montos y afirmaciones que pueden haber cambiado están marcadas como **para verificar** y todavía no las chequeé. Las ideas mías van marcadas como **Sugerencia**.

**Cómo leer los links:** cada link dice el video y el minuto. "C2P1 1:23:45" es la clase 2, parte 1, en la hora 1, minuto 23, segundo 45. Los videos de 2020 se nombran "2020-EPCD.1", "2020-EPCD.3", "2020-Grave", "2020-Caja" y "2020-Barreras".

## Los 9 videos

| # | Id | Video | Contenido | Duración | Link |
|---|---|---|---|---|---|
| 1 | — | C1P1: Clase 1 (21/08/2026), parte 1 | Presentación, incidentes, ley de datos personales, IA generativa, marcas de agua y datos sintéticos | 1:21:05 |  |
| 2 | — | C1P2: Clase 1, parte 2 ("Recording 2") | Regulación e innovación, ética y moral, preguntas fundamentales, autoetnografía y el práctico | 1:14:32 |  |
| 3 | — | C2P1: Clase 2 (22/08/2026), parte 1 | Sesgo, amplificación, métricas, escenarios de daño y métricas de equidad | 1:50:55 |  |
| 4 | — | C2P2: Clase 2, parte 2 ("Recording 2") | Notebook de equidad, auditoría de generativos y embeddings, cierre | 1:40:11 |  |
| 5 | — | 2020-EPCD.1: "Construcción iterativa de definiciones básicas" (Luciana Benotti) | Ética, moral, problema ético y el camino personal | 16:16 |  |
| 6 | — | 2020-EPCD.3: "Guía para el práctico 1" | El data statement del práctico | 17:55 |  |
| 7 | — | 2020-Grave: "Bueno, pero ¿es tan grave?" | Casos de daños de sistemas de IA (transcripción de baja calidad) | 21:22 |  |
| 8 | — | 2020-Caja: "Ejercicios de pensamiento de la Caja de Herramientas Humanísticas" (Laura Alonso Alemany) | **Sin subtítulos en la grabación** | 8:32 |  |
| 9 | — | 2020-Barreras: "Barreras a los cambios para soluciones más éticas y consensos sociales sobre qué es bueno" (Laura Alonso Alemany) | **Sin subtítulos en la grabación**; se usan sus capítulos | 18:05 |  |

**Cómo se determinó el orden.** Los títulos de 2026 dicen la clase y la fecha de grabación, y la segunda parte de cada clase dice "Recording 2". C1P1 termina anunciando una pausa C1P1 1:20:33 y C1P2 arranca con preguntas sobre la ley que se acababa de ver C1P2 0:38. C2P1 arranca retomando "la autoetnografía que les contaba Luciana ayer" C2P1 0:02, que está en C1P2 C1P2 30:27. C2P2 arranca después de la pausa con la notebook que C2P1 deja preparada.

## Mapa de módulos y videos

| Módulo | Dónde se ve |
|---|---|
| 0. La materia: quiénes la dan, materiales y cómo se trabaja | C1P1 (inicio), C1P2 (final), C2P1 (inicio), 2020-EPCD.1 |
| 1. Por qué hace falta ética práctica: incidentes que se repiten | C1P1, 2020-Grave |
| 2. La ley argentina de protección de datos personales | C1P1, C1P2 (inicio) |
| 3. Daños de la IA generativa, marcas de agua y datos sintéticos | C1P1 |
| 4. Preguntas fundamentales, ética, moral y autoetnografía | C1P2, 2020-EPCD.1, C2P1 (referencias) |
| 5. Sesgo: qué es y dónde aparece | C2P1 |
| 6. Sesgo algorítmico, amplificación y métricas como incentivo | C2P1 |
| 7. Métricas de equidad y escenarios de daño | C2P1 |
| 8. La notebook de equidad paso a paso | C2P2 |
| 9. Auditar sistemas sin una definición de error: imágenes, texto y embeddings | C2P2, 2020-Grave |
| 10. Cierre: ética a lo largo de todo el ciclo de vida | C2P2 |
| 11. El práctico: un data statement sobre el dataset de tu mentoría | C1P2, 2020-EPCD.3, C1P1, C2P1 |
| 12. Barreras al cambio, derechos y consensos sociales | 2020-Barreras y 2020-Caja (sin transcripción) |

---

## 0. La materia: quiénes la dan, materiales y cómo se trabaja
**Dónde:** C1P1 0:02, C1P2 52:06, C1P2 1:11:48, C1P2 1:12:55, C1P1 0:34, C1P1 1:06, C1P1 1:37, C1P1 2:16, C1P1 2:50, C1P1 3:23, C1P1 3:58, C1P1 4:32, C2P1 0:02, C2P1 0:35

### Conceptos clave
- **Las docentes.** Luciana se presenta como profe de FAMAF "de hace ya bastantes años" e investigadora del CONICET (la transcripción dice "CONISET") en procesamiento de lenguaje natural; aclara que a nivel de investigación trabaja más con modelos de lenguaje pequeños o medianos que con modelos grandes C1P1 0:02. La otra docente es "Lau", Laura, que en las descripciones de los videos de 2020 aparece como Laura Alonso Alemany C1P1 1:06. En el video de 2020 de construcción de definiciones, Luciana Benotti dice que la materia se da "en conjunto con Laura Alonso" 2020-EPCD.1 0:02.
- **Lo que cambia y lo que no.** Luciana cuenta que cada año, al repasar el material, aparecen cosas nuevas, pero que hay muchas cosas "desde el inicio" que siguen siendo superrelevantes C1P1 0:34. Laura agrega que, aunque todo se mueve superrápido, los fundamentos de ética "son cada vez más fundamentales", que los materiales de hace años "no han envejecido" y que aprender esto "es una buena inversión", porque hay cosas que pasan de la ética a las leyes y después se vuelven obligatorias C1P1 3:23, C1P1 3:58.
- **Los videos de 2020.** Les dejan videos que "tienen sus años" pero "son unos clásicos" y "no se vencen". Hay videos introductorios, otros de "artistas invitados" que son complementarios, y uno que describe la tarea C1P1 1:37, C1P1 2:16. Este apunte usa los que se pudieron transcribir (ver la tabla de videos).
- **Dónde está todo.** El programa está en el aula virtual y en la página de la materia, y las docentes actualizaron ahí los detalles prácticos para la entrega C1P1 2:50, C1P1 4:32. La tarea se habilita durante la clase 1 C1P1 2:16.
- **Slack y formato.** El canal de la materia está en Slack C1P2 52:06. La página de la materia tiene el programa y las slides, y todo se reproduce también en Slack y en el aula virtual C1P2 57:43, C1P2 58:17. Cada clase está pensada como tres horas sincrónicas más los videos, que suman "como una horita"; el formato viene de cuando armaron la diplomatura virtual en marzo de 2020 C1P2 1:11:48, C1P2 1:12:20.
- **Por qué trabajar en grupo.** Al cierre de la clase 1, una voz que probablemente es la de Caro (dudoso) explica que arman grupos diversos porque "tenemos mucho sesgo si trabajamos solitos", y otra docente, probablemente Laura (dudoso), remata con Alan Turing, que al enterarse de que Alonzo Church trabajaba en algo parecido se fue a Princeton a trabajar con él: "si Alan Turing trabajó en grupo, vos amiga, no sos mejor que nadie" (la anécdota es como se cuenta en clase) C1P2 1:12:55, C1P2 1:13:28.
- **Coordinación.** "La Caro" interviene desde el chat y les dice que fueron muy humildes para presentarse y que se las puede googlear C1P1 4:32.
- **Plan de la clase 2.** Laura retoma la autoetnografía que había contado Luciana el día anterior para formalizar escenarios de daño, y anuncia que la parte central de la clase es cómo calcular si un sistema está sesgado, con un par de notebooks C2P1 0:02, C2P1 0:35.
- **La organización de 2020.** En el video introductorio de 2020, Luciana organiza la materia alrededor de tres limitaciones de la ciencia de datos que pueden generar problemas éticos si no se consideran: los datos tienen limitaciones (con los data statements como primera herramienta, en el práctico 1), el aprendizaje automático tiene limitaciones (por ejemplo, de causalidad) y la ciencia de datos tiene responsabilidad y tiene que poder dar explicaciones 2020-EPCD.1 14:10, 2020-EPCD.1 14:43. También avisa que es "un curso no convencional": se va a hablar de herramientas como sesgos en embeddings de palabras y data statements, pero también de enseñanza de la responsabilidad y hasta de política internacional 2020-EPCD.1 15:17, 2020-EPCD.1 15:53.

| Qué | Dónde está | Fuente |
|---|---|---|
| Programa | Aula virtual y página de la materia | C1P1 4:32 |
| Consigna de la tarea | Video de 2020 que describe la tarea (EPCD.3) y aula virtual | C1P1 2:16, 2020-EPCD.3 0:02, 2020-EPCD.3 1:06 |
| Detalles prácticos de entrega | Aula virtual, se van actualizando | C1P1 2:50 |
| Plantilla del práctico | Página de la materia (sección práctico), aula virtual y Slack | C1P2 57:43, C1P2 58:17 |
| Planilla para armar grupos | Aula virtual | C1P2 52:42 |
| Canal de consultas | Slack | C1P2 52:06 |

<details>
<summary>Preguntas de repaso del módulo 0 (con respuestas)</summary>

1. **¿Por qué las docentes dicen que los videos de 2020 siguen sirviendo?** Porque los fundamentos de ética no envejecieron y cada vez se ponen más en evidencia; los videos "son unos clásicos" y "no se vencen" C1P1 1:37, C1P1 3:58.
2. **¿Por qué Laura dice que aprender esto es una buena inversión?** Porque hay cosas que pasan de la ética a las leyes y, cuando se vuelven obligatorias, todo el mundo tiene que entender sus implicancias C1P1 3:58.
3. **¿Dónde está el programa?** En el aula virtual y en la página de la materia C1P1 4:32.
4. **¿Cuáles eran las tres limitaciones que organizaban la materia en 2020?** Las de los datos, las del aprendizaje automático (por ejemplo, la causalidad) y la responsabilidad de la ciencia de datos de dar explicaciones 2020-EPCD.1 14:10, 2020-EPCD.1 14:43.
5. **¿Por qué la materia arma grupos diversos?** Porque trabajando solos tenemos mucho sesgo; hasta Turing trabajó en grupo C1P2 1:12:55, C1P2 1:13:28.

</details>

---

## 1. Por qué hace falta ética práctica: incidentes que se repiten
**Dónde:** C1P1 5:06, C1P1 5:41, C1P1 6:15, C1P1 7:23, C1P1 8:30, C1P1 9:04, C1P1 12:25, C1P1 14:07, C1P1 15:16, C1P1 16:55, C1P1 18:01, C1P1 20:13, y el video de 2020 "Bueno, pero ¿es tan grave?" completo (2020-Grave 0:05 a 2020-Grave 20:51).

Laura abre la materia con una "puesta en materia": antes de cualquier definición, muestra qué está pasando con los sistemas de IA en el mundo real C1P1 5:06.

### Conceptos clave
- **Los incidentes crecen año a año.** Cita un reporte de Stanford que sale todos los años y muestra que el número de incidentes reportados con sistemas de IA sube cada año (**para verificar** las cifras del reporte) C1P1 5:06, C1P1 5:41.
- **La objeción y la respuesta: la analogía de la aviación.** Alguien podría decir que suben porque cada año hay más sistemas. Laura responde que en la aviación cada año hay más vuelos y no suben los incidentes, porque cada accidente se investiga, se descubren las causas y se agregan medidas al protocolo para que no se repita. Quiere que en IA pase lo mismo, y aclara que "no es una cosa utópica" C1P1 5:41, C1P1 6:15, C1P1 6:51.
- **A quién afectan.** En una base de datos de incidentes que recomienda (no dice el nombre en la clase; dudoso), el 20% de los incidentes afecta a las personas por su raza, el 10% por sexo, el 6% por religión, nación de origen o estatus migratorio y el 5% por discapacidad (**para verificar** los porcentajes) C1P1 7:23.
- **Ya hay un consenso social sobre esto.** Recuerda que la idea de no tratar distinto a nadie por raza, religión u origen está en lo que llama "la declaración de San José", con rango constitucional en Argentina (probablemente el Pacto de San José de Costa Rica; ver glosario) C1P1 7:57. Si un sistema discrimina por esas razones, choca con nuestras leyes C1P1 8:30.
- **El objetivo de la materia.** Que estos controles estén antes de llevar un sistema a producción, y no que dependan de que alguien lo descubra después: "de esto va nuestra materia" C1P1 20:46.

### Casos reales que se cuentan en clase
| Caso | Qué pasó según la clase | Lección | Dónde |
|---|---|---|---|
| Subsidios a familias en Países Bajos (primera vez) | Un sistema de detección automática de fraude en subsidios familiares mandaba, sin intervención humana, mails exigiendo devolver unos 30.000 € (**para verificar** el monto). Hubo personas que perdieron la casa, la custodia de sus hijos y suicidios. Una auditoría mostró que los falsos positivos caían mucho más sobre familias de origen migrante; el sistema se retiró y se compensó a quien se pudo. Laura lo ubica "2012, algo así" (**para verificar** la fecha) | No todos los errores son iguales: los falsos positivos dañaban a las personas y los falsos negativos al fisco, y el error se distribuía de forma discriminatoria | C1P1 9:04, C1P1 10:14, C1P1 10:46, C1P1 11:51, C1P1 12:25 |
| Subsidios en Países Bajos (segunda vez, "2020 y algo") | El gobierno quiso volver a instalar un sistema parecido, prometiendo que esta vez lo iba a hacer bien. Se sumaron controles de sociedad civil y de periodismo de investigación (menciona "el centro Pulitzer", la sección de investigación de un diario y alguna ONG). Las auditorías independientes vieron que seguía discriminando a familias de origen migrante y no se llegó a desplegar | La auditoría externa antes de producción evita daños, como revisar un avión antes de que vuele | C1P1 12:25, C1P1 13:00, C1P1 13:33, C1P1 14:07 |
| Chatbot de orientación vocacional del servicio de empleo de Austria (2024) | A un perfil le recomendaba estudiar turismo y al mismo perfil, cambiando solo el género, ingeniería. Laura remarca que el fenómeno está "reportado, sistematizado desde 2016" en lenguaje natural | Un sesgo archiconocido se sigue desplegando desde organismos públicos | C1P1 14:07, C1P1 14:40, C1P1 15:16 |
| Smart TV que no reconoce la voz de una persona con síndrome de Down | Una familia compra una Smart TV para que una persona con problemas de motricidad fina la maneje por voz, y el reconocimiento de voz no la entiende. Laura nombra a Samsung; el caso lo había comentado Tomás y está en los videos de 2020 | Igual que no se venden autos sin cinturón, airbag ni ABS, si no podés incluir a los grupos vulnerables, no saques el producto | C1P1 15:16, C1P1 15:50, C1P1 16:23, 2020-Grave 18:30 |
| Chatbot de prospectos de medicamentos del Ministerio de Salud de España ("el año pasado") | Un ciudadano lo auditó por su cuenta: preguntó la dosis de paracetamol o ibuprofeno líquido para una niña de 3 a 32 kg, repitiendo cada consulta tres veces. Si el dato estaba literal en la tabla del prospecto, acertaba; si no, calculaba mal, mezclaba mililitros y miligramos o tomaba la fila de otro peso. Para 31 kg propuso dividir 1860 mg diarios en cuatro tomas de unos 465 mg y "dos envases al día". El ministerio bajó el servicio en menos de 24 horas | Es "un gran ejemplo" de exploración sistemática de un chatbot, y muestra que un modelo de lenguaje "no es de aritmética" | C1P1 16:55, C1P1 17:28, C1P1 18:01, C1P1 18:34, C1P1 19:08, C1P1 19:40, C1P1 20:13 |

### Los casos del video de 2020 "Bueno, pero ¿es tan grave?"
Este video corto de 2020 es material introductorio que la materia sigue recomendando ("son unos clásicos", "no se vencen") C1P1 1:37. La descripción no dice quién habla; por el estilo y porque en clase se reparten así los temas, probablemente es Laura Alonso Alemany (dudoso). La transcripción automática de este video es de baja calidad, así que los detalles de cada caso son aproximados.
- **El recorte automático de imágenes de Twitter** elegía la cara blanca cuando en la foto había una persona blanca y una negra, y no pasaba con una sola foto 2020-Grave 1:14, 2020-Grave 2:25.
- **El "despixelizador" de la Universidad de Duke** reconstruía imágenes en alta resolución a partir de imágenes en baja; con una foto pixelada de Obama devolvía la cara de un hombre blanco 2020-Grave 2:25, 2020-Grave 3:00, 2020-Grave 3:33. Un ganador del premio Turing (la transcripción no da el nombre; dudoso) respondió que era un problema de los datos y no de la herramienta, y otras personas mostraron que además había sesgo algorítmico, porque el algoritmo priorizaba la clase mayoritaria 2020-Grave 4:46, 2020-Grave 5:19, 2020-Grave 6:23.
- **Reconocimiento facial con fines policiales:** funciona peor con personas de piel oscura, así que detiene por error a muchas más; eso sistematiza la inequidad y refuerza estereotipos. Según el video, varias ciudades lo prohibieron, en la Ciudad Autónoma de Buenos Aires se había aprobado "recientemente" y algunas empresas dejaron de investigar en el área (**para verificar**) 2020-Grave 7:00, 2020-Grave 8:05, 2020-Grave 8:41, 2020-Grave 9:17.
- **Perfilamiento:** redes que dicen detectar orientación sexual o "criminalidad" a partir de la cara; el video recuerda que hace menos de cien años ideas así se usaron para matar a muchas personas, y que con computadoras y drones la concentración de poder puede ser mayor 2020-Grave 9:49, 2020-Grave 10:19, 2020-Grave 10:54.
- **Privacidad y jurisdicción:** como la universidad no puede sostener la infraestructura, muchos modelos corren en servidores de Amazon o Google, y menciona datos sensibles (DNI, salud) procesados en servidores de Amazon bajo leyes menos garantistas que las argentinas; el ejemplo de quién es el dueño de esos datos está deformado en la transcripción (dudoso) 2020-Grave 11:29, 2020-Grave 12:35, 2020-Grave 13:11.
- **Más historias:** un filtro de censura que borró el pedido de ayuda de alguien en una app de delivery; una app para correr que le mostró a un usuario el domicilio y la ruta habitual de una mujer con la que se había cruzado; una app que detecta con "un 94 por ciento" si te sentís solo, sin un plan de qué hacer con eso; un modelo de lenguaje que le recomendó suicidarse a un paciente simulado; la grabación que volvió a moderadores humanos porque los algoritmos censuraban de más; y la agencia de migraciones de Estados Unidos usando datos de empresas de autos y seguros para encontrar inmigrantes (**para verificar** todos) 2020-Grave 13:45, 2020-Grave 15:04, 2020-Grave 15:41, 2020-Grave 16:49, 2020-Grave 17:22.
- **Impacto ambiental:** cita una nota según la cual un posteo de un futbolista famoso gasta tanta energía como 10 casas en un año, y una comparación de la huella de carbono de entrenar un modelo transformer contra un vuelo Nueva York San Francisco, una vida en Estados Unidos durante un año y un auto con su combustible (**para verificar**) 2020-Grave 19:37, 2020-Grave 20:18.
- **La consigna:** compartir historias parecidas por Slack o en clase 2020-Grave 19:02.

### Tips de las docentes
- Antes de desplegar, preguntate qué errores va a cometer el sistema y a quién le caen, porque los sistemas probabilísticos siempre se equivocan C1P1 9:40, C1P1 10:14.
- Para auditar un chatbot, armá consultas sistemáticas que recorran un rango de valores y repetí cada consulta varias veces para ver la variabilidad, como hizo el ciudadano español C1P1 18:01, C1P1 18:34.
- Si no podés hacer un producto que funcione para los grupos vulnerables, no lo lances C1P1 16:23.

<details>
<summary>Preguntas de repaso del módulo 1 (con respuestas)</summary>

1. **¿Por qué Laura dice que el aumento de incidentes no se explica solo por que haya más sistemas de IA?** Porque en la aviación hay cada año más vuelos y no suben los incidentes: cada accidente se investiga y se agregan medidas al protocolo para que no se repita.
2. **¿Qué tenían de distinto los dos tipos de error del sistema de subsidios de Países Bajos?** Los falsos positivos dañaban a las personas (les exigían devolver dinero que no debían) y los falsos negativos afectaban al fisco; además, los falsos positivos caían mucho más sobre familias de origen migrante.
3. **¿Qué cambió en el segundo intento de Países Bajos?** Se sumaron auditorías independientes de sociedad civil y periodismo de investigación, que detectaron que seguía discriminando, y el sistema no llegó a producción.
4. **¿Qué sesgo reprodujo el chatbot vocacional de Austria?** Un sesgo de género: recomendaba turismo o ingeniería según el género, con el resto del perfil igual.
5. **¿Qué método usó el ciudadano que auditó el chatbot de prospectos en España?** Repitió la misma pregunta de dosis para pesos de 3 a 32 kg, tres veces cada una, y comparó con el prospecto.

</details>

---

## 2. La ley argentina de protección de datos personales
**Dónde:** C1P2 1:45, C1P2 2:17, C1P2 3:56, C1P2 5:42, C1P1 21:55, C1P1 22:29, C1P1 23:34, C1P1 24:07, C1P1 24:41, C1P1 25:14, C1P1 26:19, C1P1 27:28, C1P1 28:01, C1P1 29:07, C1P1 29:41, C1P1 30:48, C1P1 31:22, C1P1 31:54, C1P1 32:29, C1P1 33:01, C1P1 33:34, C1P1 34:06, C1P1 34:41, C1P1 36:23, C1P1 37:29, C1P1 40:20, C1P1 42:31, C1P1 43:38, C1P1 45:14, C1P1 46:24, C1P1 51:59, C1P1 53:02, C1P1 54:11

Luciana suma este bloque porque lo pidieron estudiantes de cohortes anteriores, que decían que la ley no aparecía en ninguna otra materia C1P1 21:55, C1P1 22:29. Aclara varias veces que no es abogada C1P1 41:57, C1P1 53:02. La clase no dice el número de la ley; habla de "la ley de protección de datos personales" argentina, de "casi 26 años", y la ubica en el año 2000 en una línea de tiempo (**para verificar** el número y la fecha) C1P1 22:29, C1P1 54:44.

### Por qué una ley vieja sigue importando
- Está basada en principios filosóficos que comparten muchas leyes de otros países, así que muchas de sus ideas siguen siendo relevantes aunque esté desactualizada en varios aspectos C1P1 22:29, C1P1 23:02.
- Sus definiciones se usan en el práctico, que tiene una metodología más moderna pero se apoya en estos conceptos: datos sensibles, titulares de los datos y obligaciones de quienes tratan datos C1P1 23:34.

### Definiciones
| Concepto | Qué dice la clase |
|---|---|
| Datos personales | No aplican solo a personas físicas sino también a personas jurídicas, y no solo a los datos almacenados sino también a los que se pueden inferir de ellos C1P1 24:07 |
| Datos sensibles | Información delicada que puede causar discriminación o riesgos graves: origen racial y étnico, opiniones políticas (incluida afiliación o accionar político), convicciones religiosas, salud y vida sexual (orientación o prácticas) C1P1 24:41, C1P1 33:34 |
| Titular de los datos | La persona física o jurídica cuyos datos se almacenan C1P1 25:14 |
| Disociación | Si los datos se pueden asociar o no a una persona determinada; se relaciona con anonimizar y pseudoanonimizar C1P1 25:14 |

### Principios
1. **Datos ciertos y veraces**, que reflejen la realidad, se actualicen cuando haga falta y permitan esa actualización. Luciana lo conecta con las alucinaciones y con el área de verificación de hechos (fact checking) C1P1 26:19, C1P1 26:52.
2. **Finalidad:** los datos se usan para la finalidad para la que se obtuvieron, y la ley prohíbe usarlos para fines distintos o incompatibles C1P1 26:52, C1P1 28:34.
3. **Minimización:** recolectar la mínima cantidad de datos para el objetivo, lo contrario de "recolectemos todo por las dudas" C1P1 27:28, C1P1 28:01.
4. **Consentimiento informado, libre y expreso:** hay que explicarle a la persona para qué se recolectan sus datos, y si la finalidad cambia, en principio hay que volver a recolectar. Expreso quiere decir que la persona hace algo específico, como tildar una casilla o firmar C1P1 28:01, C1P1 29:07, C1P1 31:22.
5. **Excepciones por licencia:** los datos pueden pasar al dominio público con ciertas licencias, por ejemplo después de anonimizarlos, pero eso tiene que avisarse en el consentimiento inicial C1P1 30:48, C1P1 31:22, C1P1 45:49.
6. **Seguridad y confidencialidad:** medidas de seguridad apropiadas al estado del arte. Cita a un profesor de seguridad: los datos más seguros están en una máquina desconectada de internet, en un búnker y con seguridad física C1P1 34:41, C1P1 35:16.

### Lo que está en discusión
- **El consentimiento real es un botón.** El "leí los términos y condiciones" que nadie lee es el consentimiento informado de hoy, y si funciona está en discusión; otros países lo cambiaron al actualizar sus leyes C1P1 29:41, C1P1 30:13.
- **"O lo aceptás o no usás la app".** Ante esa pregunta, Luciana dice que, hasta donde sabe, la ley no lo contempla C1P1 36:23. Laura agrega que la ley prohíbe usar los datos para algo que no autorizaste (por ejemplo, cederlos a terceros para publicidad), que las apps responden pidiendo un consentimiento "superamplio", y que eso se puede pelear en tribunales como cláusula abusiva; es una ley "garantista" pero tan genérica que depende de la interpretación del juez C1P1 37:29, C1P1 38:04, C1P1 38:36, C1P1 39:10.
- **El aporte de una estudiante abogada (Florencia).** Dice que Argentina suscribió en 2022 el "convenio 108 Plus", que suma, por ejemplo, los datos biométricos como datos sensibles (**para verificar**); que las casillas de consentimiento de privacidad deberían estar separadas de los términos y condiciones; y que no puede haber cláusulas generales de cesión de datos sin decir a qué empresa se ceden C1P1 40:20, C1P1 40:53, C1P1 41:24.
- **Servicios que garantizan derechos.** Si un trámite de salud pública o de vivienda se hace por un sistema digital, tiene que haber otro camino para quien no acepta el consentimiento C1P1 42:31. Germán comenta que en Córdoba la ley de modernización 10618 prevé canales para personas vulnerables digitalmente (**para verificar**) C1P1 45:14.
- **Investigación.** Si investigás con datos de personas, también tenés que cumplir la ley y decir en el consentimiento qué datos recolectás, para qué y con qué nivel de anonimización. En procesamiento de lenguaje natural se espera, cada vez más, la aprobación de un comité de ética, aunque no siempre es obligatoria; si tu jurisdicción no tiene comité, podés presentarte ante el de otra C1P1 43:38, C1P1 46:24, C1P1 46:59, C1P1 49:46. Los comités de ética de las conferencias revisan después, cuando la investigación ya está hecha C1P1 50:18.
- **Cumplimiento y multas.** Una cosa es que la ley exista y otra que se haga cumplir. Las multas de la ley argentina van de 1000 a 100.000 pesos, menos que la multa por circular con las luces apagadas en un peaje; en Brasil el tope es el 2% de la facturación (**para verificar** ambas cifras) C1P1 51:59, C1P1 53:36. Brasil además regula qué pasa con datos de sus ciudadanos fuera del territorio, y por eso Airbnb tiene términos y condiciones propios para Brasil C1P1 53:36, C1P1 54:11.
- **Licencias de la web cada vez más restrictivas.** Antes se armaban datasets con crawlers sin problemas; hoy muchas páginas restringen el scraping, y recomienda un proyecto de Mozilla que muestra cómo evolucionaron esas licencias (nombre del proyecto no dicho; dudoso) C1P1 31:54, C1P1 32:29, C1P1 33:01.
- **¿La regulación mata la innovación?** Al empezar la segunda parte de la clase 1, Sergio cuenta una queja que escuchó: que en Europa no se podía vincular Google Maps con una página "por culpa" de la ley de protección de datos. Laura responde "yo no diría por culpa, diría a causa de", que no conoce el detalle de esa norma, que en general está de acuerdo con las legislaciones proteccionistas y que hay que buscar el fundamento de cada ley. Sobre la idea de que la regulación mata la innovación, dice que no se sostiene con datos históricos: farmacia, ciencias de la vida y aeronáutica están fuertemente reguladas y siguen innovando, y la farmacéutica se reguló después de casos muy graves. Le parece "muy fuerte" escuchar "no dejemos que los derechos frenen la innovación", porque son derechos muy consensuados. Una regla que desde tu escenario parece un engorro puede estar evitando daños que no afectan a la mayoría, pero sí afectan muy gravemente a quienes alcanzan, y el derecho es para toda la población, con especial atención a los más vulnerables C1P2 0:04, C1P2 0:38, C1P2 1:11, C1P2 1:45, C1P2 2:17, C1P2 2:51, C1P2 3:23, C1P2 3:56, C1P2 4:30.
- **El interés económico.** Luciana muestra que entre las cinco empresas más caras del mundo está primero Nvidia, que le vende hardware a las demás, y que las otras son todas empresas cuyo insumo básico es el dato (**para verificar** el ranking) C1P2 5:42.
- **No recolectar datos sensibles no resuelve el problema.** Decir "mi dataset no tiene datos sensibles" puede traer problemas de sesgo y de inferencia, que se ven más adelante C1P1 34:06.

### Conexión con el práctico
En el práctico vas a tener que dejar escrito para qué se recolectaron originalmente los datos y para qué te parece que se podrían usar o no C1P1 28:34, C1P1 29:07, y qué datos sensibles contiene el dataset de tu mentoría C1P1 33:01.

<details>
<summary>Preguntas de repaso del módulo 2 (con respuestas)</summary>

1. **¿Los datos personales incluyen solo datos almacenados de personas físicas?** No: según la clase, incluyen personas jurídicas y datos que se pueden inferir de los almacenados.
2. **¿Qué dice el principio de minimización?** Que recolectes la mínima cantidad de datos necesaria para el objetivo, y no todo "por las dudas".
3. **¿Cuándo pueden usarse datos para otro fin?** Cuando el consentimiento inicial avisó que se liberarían, por ejemplo con una licencia abierta después de anonimizarlos.
4. **¿Por qué se dice que la ley se aplica poco?** Porque las multas son bajísimas (de 1000 a 100.000 pesos según la clase) y la protección es tan genérica que depende de la interpretación judicial.
5. **¿Alcanza con no recolectar datos sensibles?** No: la clase advierte que eso puede traer problemas de sesgo y de inferencia.
6. **¿Qué responde Laura a la idea de que la regulación mata la innovación?** Que no se sostiene con datos históricos, porque sectores muy regulados como farmacia y aeronáutica siguen innovando, y que una regla que parece un engorro puede proteger a grupos a los que el daño afecta muy gravemente C1P2 2:17, C1P2 4:30.

</details>

---

## 3. Daños de la IA generativa, marcas de agua y datos sintéticos
**Dónde:** C1P1 55:18, C1P1 55:50, C1P1 56:23, C1P1 57:03, C1P1 57:36, C1P1 58:43, C1P1 59:13, C1P1 59:45, C1P1 1:00:17, C1P1 1:00:52, C1P1 1:01:26, C1P1 1:01:59, C1P1 1:02:33, C1P1 1:04:17, C1P1 1:04:49, C1P1 1:05:26, C1P1 1:06:00, C1P1 1:06:34, C1P1 1:07:10, C1P1 1:07:42, C1P1 1:08:15, C1P1 1:08:49, C1P1 1:09:23, C1P1 1:10:00, C1P1 1:11:06, C1P1 1:12:13, C1P1 1:12:47, C1P1 1:13:21, C1P1 1:14:29, C1P1 1:15:03, C1P1 1:15:37, C1P1 1:16:09, C1P1 1:16:42, C1P1 1:17:50, C1P1 1:18:53, C1P1 1:19:26

### Códigos de ética y un caso cercano
- La regulación de datos y la de IA están muy vinculadas, y en este momento están cambiando en todo el mundo C1P1 55:18.
- En ciencia de datos aplica el código de ética de la ACM (Association for Computing Machinery), que no es una ley. Uno de sus mandatos es **evitar el daño** C1P1 55:18, C1P1 55:50.
- **Caso de Córdoba:** un alumno de una escuela usaba IA para crear imágenes pornográficas de sus compañeras; el caso ocurrió en 2024 y llegó a juicio en 2025, y hoy hay un caso parecido en un colegio con chicos de 13 o 14 años (**para verificar**) C1P1 56:23, C1P1 57:03.

### Marcas de agua (watermarking)
- **Para qué sirven.** Una forma de detectar imágenes o textos generados por IA es que traigan una marca. Luciana menciona que en China la regulación exige que las imágenes generadas lleven metadatos de quién, dónde, con qué software y cuándo se crearon, y que siempre está la discusión de si quien genera la imagen puede borrar la marca C1P1 57:36.
- **La regulación europea.** El artículo 50 de la AI Act de la Unión Europea pide que los proveedores de IA generativa (texto, audio, imagen y video) marquen las salidas en un formato legible por máquina y detectable como contenido sintético, y que los usuarios finales no puedan manipular la marca fácilmente (**para verificar** el texto exacto) C1P1 59:13, C1P1 59:45.
- **El anuncio de Anthropic.** Según la clase, Anthropic anunció "esta semana o la semana pasada" que Claude marca también el texto que genera, lo desplegó a nivel global aunque la norma es europea, y todavía no liberó el detector (**para verificar**) C1P1 58:43, C1P1 59:13, C1P1 1:00:17, C1P1 1:00:52. Por eso, aunque no estemos en la Unión Europea, también nos afecta C1P1 1:00:52.
- **Cómo funciona la marca sobre los logits** (lo explica a partir de un survey de watermarking para grandes modelos de lenguaje, del que sale el diagrama):
  1. El modelo genera un token por vez y, para cada uno, produce logits: una distribución de probabilidad sobre todos los tokens posibles C1P1 1:02:33.
  2. Parámetros como la temperatura cambian esa distribución; subirla la aplana y el modelo elige palabras más raras C1P1 1:03:07, C1P1 1:03:40.
  3. Con modelos abiertos, los logits están accesibles; con modelos comerciales, el acceso es restringido, pero la empresa los ve todos C1P1 1:04:49.
  4. La empresa usa una clave secreta para partir los tokens posibles en "verdes" y "rojos", y les suma un extra a los verdes, así salen con más probabilidad C1P1 1:05:26, C1P1 1:06:00.
  5. Para detectar, se hace un test de hipótesis sobre cuántos tokens verdes aparecen. Con textos largos la certeza es muy alta; con textos cortos baja C1P1 1:06:34.
- **Los detectores sin marca andan muy mal.** Herramientas como DetectGPT se usaron y abusaron entre docentes, pero fallan para los dos lados: una de ellas decía que el preámbulo de la Constitución Argentina lo había generado una IA C1P1 1:07:10, C1P1 1:07:42.
- **Quién tiene el detector.** Cada empresa va a tener su detector, porque no va a compartir la clave, y probablemente lo cobre C1P1 1:07:42, C1P1 1:08:15. Martín pregunta si se puede detectar sin acceso al proceso; la respuesta es que la detección depende del detector de la empresa que tiene la clave C1P1 1:18:53, C1P1 1:19:59.
- **Distintos métodos.** Muestra una comparación: SynthID, que se usa en Gemini, el de Anthropic y el watermarking sobre logits que explicó C1P1 1:10:00.
- **Calidad del texto.** Hubo mucha discusión sobre si la marca empeora el texto; a Luciana, que trabaja en evaluación de modelos de lenguaje, gran parte de esa discusión le genera dudas C1P1 1:10:35, C1P1 1:11:06.
- **Cómo romperlas.** Antes de la pausa, las docentes proponen pensar cómo romperlas y una de ellas bromea con que las redes ya se llenan de ideas como un skill que cambie cada quinta palabra por un sinónimo, y Luciana recuerda que siempre que aparece un método robusto aparecen métodos para romperlo C1P1 1:16:42, C1P1 1:18:53.

### Datos sintéticos
- **Inundación de artículos.** En la conferencia AAAI se recibieron 40.000 artículos en la última convocatoria, y los revisores marcaron tres cuartos como generados con IA (**para verificar**) C1P1 1:08:49, C1P1 1:09:23. Lo mismo pasa con los conjuntos de datos C1P1 1:09:23, C1P1 1:12:13.
- **De crowdworkers a modelos.** Muchos trabajos pasaron de pagarle poco a crowdworkers (por ejemplo, en Amazon Mechanical Turk) a generar los datos directamente con modelos de lenguaje; una de las justificaciones es que los crowdworkers ya usaban modelos de lenguaje C1P1 1:12:47, C1P1 1:13:21. El grupo de Luciana, en cambio, arma conjuntos de evaluación con personas, en encuentros presenciales y datatones C1P1 1:12:13, C1P1 1:12:47.
- **Lo sintético no es malo en sí.** Sirve para simular experimentos, probar pipelines metodológicos y detectar errores de diseño antes de gastar en recolectar datos reales C1P1 1:14:29, C1P1 1:15:03.
- **El problema.** Se rompe el límite entre lo sintético y lo real, y ya se venden datasets sintéticos que se hacen pasar por reales. Si las marcas de agua se generalizan, serían una forma de detectarlo, pero queda abierta la pregunta de qué pasa con los modelos abiertos C1P1 1:15:37, C1P1 1:16:09, C1P1 1:17:50.

<details>
<summary>Preguntas de repaso del módulo 3 (con respuestas)</summary>

1. **¿Qué principio del código de la ACM destaca Luciana?** Evitar el daño.
2. **¿Cómo marca un texto el método de watermarking sobre logits?** Con una clave secreta divide los tokens posibles en verdes y rojos y les suma probabilidad a los verdes; después un test de hipótesis cuenta cuántos verdes aparecen.
3. **¿Por qué la detección es más confiable con textos largos?** Porque hay más tokens para que el test de hipótesis encuentre el exceso de tokens verdes.
4. **¿Qué ejemplo muestra que los detectores sin marca fallan?** Uno de ellos decía que el preámbulo de la Constitución Argentina lo había escrito una IA.
5. **¿Para qué sirven los datos sintéticos según la clase?** Para simular experimentos y probar pipelines antes de recolectar datos reales; el riesgo es que se vendan como reales.

</details>

---

## 4. Preguntas fundamentales, ética, moral y autoetnografía
**Dónde:** C1P2 6:18, C1P2 7:26, C1P2 8:00, C1P2 8:33, C1P2 9:04, C1P2 9:36, C1P2 10:09, C1P2 10:47, C1P2 11:20, C1P2 12:32, C1P2 13:08, C1P2 13:39, C1P2 14:12, C1P2 14:46, C1P2 16:27, C1P2 17:01, C1P2 17:36, C1P2 18:11, C1P2 18:45, C1P2 19:22, C1P2 19:57, C1P2 20:30, C1P2 21:04, C1P2 21:37, C1P2 22:09, C1P2 22:41, C1P2 23:15, C1P2 23:48, C1P2 24:25, C1P2 24:57, C1P2 25:27, C1P2 26:00, C1P2 27:37, C1P2 28:12, C1P2 28:45, C1P2 29:19, C1P2 29:55, C1P2 30:27, C1P2 30:58, C1P2 31:32, C1P2 32:05, C1P2 32:40, C1P2 33:13, C1P2 33:46, C1P2 34:23, C1P2 34:54, C1P2 35:29, C1P2 36:02, C1P2 36:37, C1P2 37:11, C1P2 37:44, C1P2 38:17, C1P2 38:49, C1P2 39:24, C1P2 39:57, C1P2 40:34, C1P2 41:10, C1P2 41:44, el video de 2020 "EPCD.1 Construcción iterativa de definiciones básicas" completo (2020-EPCD.1 0:02 a 2020-EPCD.1 15:53) y las referencias de la clase 2 en C2P1 0:02, C2P1 28:17, C2P1 29:28.

En la segunda parte de la clase 1, Luciana pasa "de la parte legal a la parte ética, que es el título de esta materia" C1P2 6:18. Repasa definiciones que están en el video de 2020, plantea dos preguntas fundamentales con varios casos y presenta la autoetnografía, que el video de 2020 desarrolla con su propio ejemplo.

### Conceptos clave
- **Ética.** El conjunto de principios consensuados en una comunidad que dirigen y valoran como bueno o malo un comportamiento, de personas o de sistemas basados en datos. Hay consenso en no dañar, respetar y ser justos; el problema aparece cuando se baja a casos concretos C1P2 7:26, C1P2 8:00, 2020-EPCD.1 0:02, 2020-EPCD.1 0:37.
- **Moral.** Los principios de una persona consigo misma, lo que yo como individuo considero bueno o malo C1P2 8:33, 2020-EPCD.1 1:12.
- **Problema ético.** Una situación de conflicto, o potencial conflicto, con alguno de los principios éticos consensuados en una comunidad C1P2 8:33, 2020-EPCD.1 1:12.
- **¿Qué comunidad?** Hay comunidades de distintos tamaños, y como estas tecnologías afectan a nivel global, hay lineamientos internacionales; Luciana menciona un consejo de expertos en IA organizado por las Naciones Unidas que sigue trabajando en consensos éticos globales (**para verificar** el nombre y el estado de ese consejo) C1P2 9:04, C1P2 9:36.
- **Los consensos cambian.** El "dilema del pollito": un clasificador que decide si un huevo va a dar un pollo para carne o una gallina ponedora, ¿es ético?, ¿quién lo pasa peor? La respuesta puede ser distinta hace 40 años, hoy o dentro de 10, y según la moral de cada uno C1P2 9:36, C1P2 10:09, C1P2 10:47.
- **Lo legal es distinto de lo ético.** En ética hay zonas grises C1P2 12:32. Alfonsina cuenta que trabaja con datos en el CONICET y consulta a legales cuando un gremio le pide listas de personas para un padrón o datos para una plataforma de vinculación tecnológica; Luciana confirma que estos dilemas no son solo de empresas y que tienen que ver con el fin para el que se recolectaron los datos C1P2 11:20, C1P2 11:54.

### Las dos preguntas fundamentales
1. **¿Quién se beneficia?**
2. **¿Quién podría sufrir daños, si el sistema funciona bien y si funciona mal?** Los clasificadores siempre cometen errores, y esos errores muchas veces no están distribuidos al azar sino que caen recurrentemente sobre ciertos grupos, tema que Laura desarrolla en la clase 2 C1P2 13:39, C1P2 14:12, C1P2 14:46.

Luciana agrega que hay literatura que sugiere hablar de **daños** en lugar de riesgos, y ligarlos a grupos concretos de personas, porque así es más fácil imaginarlos C1P2 18:45. Aun así, puede haber daños que no se previeron al desarrollar una tecnología, como el caso de las fotos pornográficas falsas en colegios secundarios que contó antes (ver módulo 3) C1P2 19:22.

| Caso | Qué plantea | Dónde |
|---|---|---|
| Clasificador de inteligencia a partir de la huella digital | Usar fotos y contenido de las redes de una persona para estimar cuán inteligente es; un proyecto que "a alguien se le ocurrió" | C1P2 12:32, C1P2 13:08 |
| Clasificador de orientación sexual a partir de la cara | Un proyecto (la transcripción dice "AI GDAR" o "AI Gator"; dudoso) entrenado con fotos de una aplicación tipo Tinder, basado en rasgos de la cara, el peinado y el maquillaje. La etiqueta que predice es un dato sensible según la ley, y tenía una precisión mayor para hombres que para mujeres | C1P2 15:54, C1P2 16:27, C1P2 17:01, C1P2 17:36, C1P2 18:11 |
| Modelo de lenguaje ajustado con los datos de una persona incapacitada | En un país que permite la eutanasia, los parientes de alguien que no puede opinar hablaban de tener la ilusión de que esa persona decida sobre su propia vida. Muestra que, según dónde te toque vivir, no te imaginás el beneficio que algo puede tener para otra persona | C1P2 19:57, C1P2 20:30, C1P2 21:04 |
| La autorregulación en procesamiento de lenguaje natural | Su grupo fue a ver si los artículos científicos aplican estas preguntas. Cada vez más artículos incluyen una sección de "consideraciones éticas" (de menos del 20% a más de la mitad, con datos hasta 2024), pero muy pocos discuten quién se beneficia, menos quién se daña y casi ninguno las poblaciones vulnerables; en general dicen "anonimizamos los datos" o "tuvimos aprobación del comité de ética" sin explicar más (**para verificar** los porcentajes) | C1P2 21:37, C1P2 22:09, C1P2 22:41, C1P2 23:15, C1P2 23:48, C1P2 24:25, C1P2 24:57, C1P2 25:27, C1P2 26:00 |

### La autoetnografía
- **Asumir que no somos objetivos.** Frente a un dilema ético solemos pensar que tenemos que ser objetivos, "como si eso existiera". La propuesta es asumir que todas las personas somos sesgadas, de formas distintas porque tenemos historias distintas, y pensar desde dónde estamos parados; si no, tendemos a repetir discursos que escuchamos por ahí. Eso no quiere decir que esté bien el sesgo en los modelos C1P2 27:37, C1P2 28:12, C1P2 28:45.
- **Qué es.** Luciana la presenta como "la autoetnografía como herramienta para reflexionar y adaptar definiciones de ética en áreas tecnológicas": un diálogo entre la vida personal y las decisiones profesionales, que mira los valores detrás de tus respuestas a quién se beneficia y quién se daña. Lo más fácil de ver son las cosas que te dañaron a vos C1P2 30:27, C1P2 30:58, C1P2 31:32.
- **No es solo demografía.** También cuentan tu trayectoria y para quién trabajás. Ejemplos de la clase: un científico de datos que trabajó en un sistema de selección de personal puede pensar en la discriminación por edad, más relevante ahora que hay preentrevistas hechas por modelos; alguien de ciberseguridad ve riesgos de privacidad que otros no ven; y pesa si pensás desde la ley argentina o desde la de otra jurisdicción para la que trabajás C1P2 32:05, C1P2 32:40, C1P2 33:13, C1P2 33:46, C1P2 34:23, C1P2 34:54, C1P2 35:29.
- **Del daño sufrido al escenario de daño.** En la clase 2, Laura dice que pensar en daños que hayas sufrido "tiene que ver con esto de la autoetnografía" y que se usa para formalizar escenarios de daño (módulo 7). También la recomienda para descubrir variables protegidas que no se te ocurren si no las viviste C2P1 0:02, C2P1 28:17, C2P1 29:28.

### Las preguntas del camino personal
En la clase, Luciana dice que el video plantea "cinco preguntas" y lista cómo entró la ciencia de datos en tu vida, qué proyectos te marcaron, si pertenecés o simpatizás con una minoría, qué problemas éticos ves desde ahí y cuál es la ética de quien te financia C1P2 29:19, C1P2 29:55, C1P2 30:27. El video de 2020 además pregunta a quién afecta económicamente tu trabajo 2020-EPCD.1 11:21.

| Pregunta | Qué responde Luciana sobre sí misma | Dónde |
|---|---|---|
| ¿Cómo entró la ciencia de datos a tu vida? | Por la computación: le regalaron una computadora a los seis años, en 1985, y pensaba que las computadoras eran mágicas | 2020-EPCD.1 2:22, C1P2 35:29 |
| ¿Qué proyectos te marcaron? | Los humanos virtuales (sistemas de diálogo con un cuerpo digital que hace gestos y contacto visual) en un instituto de tecnologías creativas de una universidad de California (la transcripción dice "universidad de sauce"; dudoso), y el aprendizaje de la programación, con una plataforma de la Fundación Sadosky para que estudiantes de secundario programen chatbots | 2020-EPCD.1 2:55, 2020-EPCD.1 3:27, 2020-EPCD.1 4:33 |
| Primera definición de ética laboral | Dos principios de su comunidad: la computación debe ser útil y usable para todos, y todos deben poder ser creadores y no solo usuarios (por eso enseñar programación desde el jardín) | 2020-EPCD.1 5:04, 2020-EPCD.1 5:38 |
| ¿Pertenecés a alguna minoría? | Es mujer en computación desde la carrera de grado e investigadora latinoamericana en procesamiento de lenguaje natural, "somos muy poquitos". Por eso mira especialmente los sesgos de género en modelos de lenguaje | 2020-EPCD.1 6:47, C1P2 36:02, C1P2 36:37 |
| ¿Qué problemas éticos ves desde tu minoría? | Traductores que con una sola palabra ofrecen los dos géneros, pero en una oración traducen "nurse" como "enfermera"; desde el turco pasa lo mismo; al mitigar en profesiones "salta" en otras áreas, como "divorced" traducido "divorciada", también en árabe. Desde 2016, además, la generación de discurso de odio en chatbots. En 2020 sumaba que la IA puede poner mucho poder en pocas manos | C1P2 37:11, C1P2 37:44, C1P2 38:17, C1P2 38:49, C1P2 39:24, C1P2 39:57, 2020-EPCD.1 9:38, 2020-EPCD.1 10:15 |
| ¿Cuál es la ética de quien te financia? | "Una pregunta difícil e incómoda". En 2020 contaba que el laboratorio de California estaba financiado "casi en un 90%" por una agencia de defensa (la transcripción dice "dar"; dudoso) para entrenar militares (**para verificar**) | C1P2 40:34, C1P2 41:10, 2020-EPCD.1 10:47 |
| ¿A quién afecta tu trabajo económicamente? | La atención automatizada al cliente con chatbots y las plataformas de e-learning sacan puestos de trabajo. Aclara que no dice que esté mal, sino que son lugares donde mirar | 2020-EPCD.1 11:21, 2020-EPCD.1 11:54 |
| Segunda definición | De "útil y usable" a una perspectiva de derechos humanos: "la computación primero que nada debe respetar a todos y no dañarlos", y hay que enseñar ética además de programación. En la clase agrega que muchos marcos éticos evolucionaron de evitar daños a respetar los derechos humanos y ser beneficiosos | 2020-EPCD.1 12:29, 2020-EPCD.1 13:03, C1P2 41:10, C1P2 41:44 |
| Tercer intento | Te invita a redefinir tu ética laboral otra vez al terminar el curso | 2020-EPCD.1 15:17 |

### Tips
- La definición no se escribe una vez: se reescribe cada vez que descubrís un problema que antes no veías. El ejercicio tiene tres intentos a propósito 2020-EPCD.1 12:29, 2020-EPCD.1 15:17.
- Arreglar un sesgo en un caso no lo elimina: "siempre siguen saltando por otro lado" C1P2 38:49.
- Antes de discutir riesgos en abstracto, nombrá grupos concretos de personas C1P2 18:45.
- **Sugerencia:** escribí tus respuestas a estas preguntas en un documento propio y guardalo; te van a servir para la lista de grupos que pueden ser dañados que se usa en las métricas de equidad (módulo 7).

<details>
<summary>Preguntas de repaso del módulo 4 (con respuestas)</summary>

1. **¿Qué diferencia hay entre ética y moral según la materia?** La ética son principios consensuados en una comunidad; la moral son los principios de una persona consigo misma C1P2 8:33.
2. **¿Cuáles son las dos preguntas fundamentales?** Quién se beneficia, y quién podría sufrir daños si el sistema funciona bien y si funciona mal C1P2 13:39.
3. **¿Por qué hablar de daños a grupos concretos en lugar de riesgos?** Porque al pensar en grupos concretos es más fácil imaginar lo que puede pasar C1P2 18:45.
4. **¿Qué encontró el análisis de artículos de procesamiento de lenguaje natural?** Que casi todos tienen una sección de consideraciones éticas, pero muy pocos discuten quién se beneficia, quién se daña o qué poblaciones vulnerables se afectan C1P2 24:57.
5. **¿Para qué sirve la autoetnografía?** Para reconocer desde dónde pensás la ética, descubrir daños y grupos que de otro modo no verías, y formalizar escenarios de daño C1P2 30:58, C2P1 0:02.
6. **¿Cómo cambia la definición de Luciana entre el primer y el segundo intento?** Pasa de "útil y usable para todos" a "respetar a todos y no dañarlos", con una perspectiva de derechos humanos 2020-EPCD.1 12:29, C1P2 41:44.

</details>

---

## 5. Sesgo: qué es y dónde aparece
**Dónde:** C2P1 0:02, C2P1 1:09, C2P1 2:19, C2P1 2:56, C2P1 3:28, C2P1 4:05, C2P1 4:41, C2P1 5:18, C2P1 6:25, C2P1 8:42, C2P1 9:51, C2P1 10:24, C2P1 10:59, C2P1 12:03, C2P1 12:35, C2P1 13:08, C2P1 14:16, C2P1 15:58, C2P1 17:03, C2P1 18:10, C2P1 19:15, C2P1 19:49, C2P1 20:22, C2P1 21:27, C2P1 22:31, C2P1 24:49, C2P1 26:02, C2P1 27:08, C2P1 27:42, C2P1 28:17, C2P1 29:28, C2P1 30:37, C2P1 31:11, C2P1 31:48, C2P1 33:30, C2P1 34:02, C2P1 34:35, C2P1 35:13, C2P1 36:22, C2P1 37:33, C2P1 38:39, C2P1 39:15, C2P1 39:50, C2P1 40:24, C2P1 40:56, C2P1 41:30

La clase 2 la abre Laura. La parte central del día es calcular si un sistema está sesgado o no, que es "una cuestión dura de ciencia de datos"; la justicia viene después C2P1 0:35, C2P1 1:09.

### Definiciones que salen de la clase
| Definición | Quién la trae | Qué agrega |
|---|---|---|
| Sesgo como posicionamiento | Una estudiante de humanidades | Nadie llega a la objetividad, porque siempre mira desde un lugar; conviene explicitar el posicionamiento metodológico C2P1 1:45, C2P1 2:19 |
| Error sistemático de un modelo | Eric | Es la definición más cercana a la estadística. Que sea sistemático, y no aleatorio, es lo que permite tomar medidas sistemáticas para prevenirlo o mitigarlo C2P1 3:28, C2P1 4:05 |
| Desvío respecto de un parámetro | Pablo | Como el desvío de la esperanza. El parámetro no siempre es el 50 y 50: depende de la distribución poblacional C2P1 4:41, C2P1 5:18 |
| Sesgo y varianza | Antonio y Eric | El clásico blanco con flechas: medidas precisas pero corridas del centro. Laura aclara que "tendencioso" implica intención y el sesgo no siempre la tiene C2P1 7:01, C2P1 8:42, C2P1 9:15 |
| Wikipedia | Laura | "Un peso desproporcionado a favor o en contra de una cosa, persona o grupo en comparación con otra"; desproporcionado puede ser una noción puramente estadística, y en ciencia e ingeniería es un error sistemático que viene de un muestreo injusto o de un estimador que no es preciso en promedio C2P1 13:08, C2P1 13:43, C2P1 17:03 |

**El ejemplo de las vacantes.** Si querés repartir vacantes universitarias de forma equitativa entre personas de origen rural y urbano, y la población es 80% rural y 20% urbana, repartir 50 y 50 es sesgado: te alejás del parámetro poblacional C2P1 5:18, C2P1 5:52, C2P1 6:25.

### Ideas centrales
- **Los modelos basados en datos no son objetivos.** Vienen de un contexto, porque los seres humanos no son objetivos y los artefactos que crean tampoco. Laura lo presenta como una de las "grandes mentiras de la inteligencia artificial" C2P1 2:56, C2P1 3:28, C2P1 12:35.
- **El sesgo es humano.** Es un mecanismo cognitivo que nos ayudó a sobrevivir: ante una polvareda en la sabana, corrías sin esperar a saber si era un guepardo o una gacela. No se trata de "superarlo", que es inevitable, sino de reconocerlo, diagnosticarlo y actuar C2P1 14:16, C2P1 14:48, C2P1 15:22, C2P1 15:58. Prejuicio es negativo, pero intuición es muy positivo, y los dos son sesgos C2P1 17:03.
- **Comparar para ver.** Muchas cosas son invisibles si no se comparan, "como el zorro del Principito" C2P1 13:43.
- **"Las cosas son así" es el argumento del grupo dominante.** Que haya más enfermeras que enfermeros no justifica que un traductor traduzca siempre nurse en femenino y doctor en masculino: un traductor, un chatbot o un auto autónomo no son sociología descriptiva, son agentes que actúan en la sociedad y tienen que respetar sus normas C2P1 18:10, C2P1 18:42, C2P1 19:15, C2P1 19:49.
- **El ejemplo del auto autónomo.** Con ese razonamiento, los autos autónomos deberían tener la misma proporción de accidentes que la historia; como no lo queremos, se usan sistemas híbridos con una parte estadística y otra simbólica que codifica las normas de tránsito C2P1 20:22, C2P1 20:54.
- **Alinear con valores, de forma accionable.** Las medidas no son solo descriptivas: sirven para decidir. "Alinear" es el término de moda para que los sistemas se comporten según nuestros valores, que cambian de una sociedad a otra (da el ejemplo de las cámaras en China) C2P1 9:51, C2P1 10:24, C2P1 10:59, C2P1 11:30, C2P1 12:03.

### El caso COMPAS (ProPublica, 2016)
- Es el ejemplo con el que más trabaja la materia. Un sistema que usaban (y "creo que todavía" usan, dice Laura) jueces de Estados Unidos para calcular el riesgo de que una persona cometa un delito estando en libertad condicional C2P1 21:27, C2P1 21:57, C2P1 22:31.
- ProPublica desagregó los resultados por raza. Entre quienes salieron y no reincidieron, el 23% de las personas blancas y el 45% de las negras habían sido etiquetadas de riesgo alto. Del otro lado, casi el 50% de las personas blancas etiquetadas de riesgo bajo reincidieron, contra un 30% de las negras (**para verificar** las cifras exactas) C2P1 24:49, C2P1 25:25, C2P1 26:02, C2P1 26:34.
- El error que deja presa a una persona que no habría sido peligrosa caía mucho más sobre las personas negras, y el error que afecta más a la sociedad caía más sobre las blancas C2P1 26:02.
- Que los investigadores eligieran desagregar por raza ya era un conocimiento previo, "en el sentido positivo" C2P1 23:07.
- La pregunta final no es técnica: si queremos que los sistemas sigan reproduciendo lo que muestran los datos históricos es una decisión de quienes deciden, "y el resto podemos votar" C2P1 27:42.
- Camila recuerda el caso de un argentino condenado a muerte en Estados Unidos en cuya sentencia pesó que era latino; el dataset también incluye esa categoría C2P1 29:28, C2P1 30:05.

### Cómo se elige la variable protegida
En general es un consenso social, pero hay divisiones que no se te ocurren si no las viviste. Por eso recomienda la etnografía personal que propuso Luciana el día anterior y prestar atención al entorno. Su ejemplo: las personas con agorafobia son una parte chica de la población, pero podría haber un sesgo estructural en su contra C2P1 27:42, C2P1 28:17, C2P1 28:50, C2P1 29:28.

### Dónde puede estar el sesgo
| Fuente | Ejemplo de la clase | Dónde |
|---|---|---|
| Histórico (en los datos) | Datos que reflejan una forma de funcionar aceptada hace 30 o 5 años y ahora no | C2P1 31:11, C2P1 34:02 |
| Muestreo o representatividad (representativity bias) | Los percentiles de crecimiento de bebés en Argentina correspondían a otra población (europea occidental), y muchos bebés sanos se diagnosticaban con un problema; los oxímetros funcionan mejor con piel blanca porque se calibraron con personas de piel blanca | C2P1 31:11, C2P1 31:48, C2P1 32:21, C2P1 32:55, C2P1 33:30 |
| Representación de los ejemplos (variables que faltan) | El estudio de la copa de vino: según Laura, se publicó en Nature que una copa de vino con las comidas era buena para el corazón, pero faltaba la clase social; al rehacerlo, la correlación era con el estatus socioeconómico (**para verificar** la referencia) | C2P1 35:13, C2P1 35:47, C2P1 36:22, C2P1 36:56 |
| Representación del objetivo | No es lo mismo optimizar que las personas saquen buenas notas, que aprendan, que entren a universidades de elite o que sean productivas | C2P1 37:33, C2P1 38:05 |
| Supervivencia (planteo del problema) | Los aviones de la Segunda Guerra Mundial: había que reforzar las zonas sin disparos, porque los que recibían tiros ahí no volvían; o estudiar la falta de mujeres en computación solo con las que están en la carrera | C2P1 38:39, C2P1 39:15 |
| Framing | Lo que no problematizamos al plantear el objetivo | C2P1 39:50 |
| Algoritmo de aprendizaje | La clase mayoritaria (ver módulo 6) | C2P1 40:24 |
| Evaluación | "Muchísimos" sesgos vienen de cómo se evalúa (ver módulo 6) | C2P1 40:24 |
| Despliegue | El sistema cambia el mundo al entrar en funcionamiento y aparecen sesgos nuevos | C2P1 40:56 |

**Remedio para la representatividad:** hacer modelos específicos para poblaciones específicas, que es más caro; Laura ironiza con el argumento de que no hay plata para eso C2P1 34:35.

### Tips de la docente
- Solo podés ver los sesgos que desnaturalizaste; incorporá a tu metodología la búsqueda de sesgos nuevos y planificá una parte del trabajo para volver a chequear cuando el sistema ya está en producción C2P1 40:24, C2P1 40:56.
- Preguntate de dónde vienen tus datos, si arrastran un sesgo histórico y si representan a la población donde vas a aplicar el modelo; son preguntas del data statement C2P1 33:30, C2P1 34:02.
- Cierra con Rosa Luxemburgo: la idea de poder ser distintos sin recibir un trato que nos dé menos oportunidades, y que lo más revolucionario es decir lo que está pasando, hablar de los datos C2P1 41:30, C2P1 42:03.

<details>
<summary>Preguntas de repaso del módulo 5 (con respuestas)</summary>

1. **¿Por qué importa que el sesgo sea un error sistemático y no aleatorio?** Porque al ser sistemático se puede diagnosticar y se pueden tomar medidas sistemáticas para prevenirlo o mitigarlo.
2. **Si la población es 80% rural y 20% urbana, ¿repartir vacantes 50 y 50 es equitativo?** No: es sesgado, porque se aleja del parámetro poblacional.
3. **¿Qué mostró ProPublica sobre COMPAS?** Que los falsos positivos (riesgo alto para quien no reincidió) eran mucho más frecuentes en personas negras (45%) que en blancas (23%), según las cifras de la clase.
4. **¿Qué tipo de sesgo explica el error de los oxímetros?** Un sesgo de muestreo o representatividad: se calibraron sobre todo con personas de piel blanca.
5. **¿Por qué "las cosas son así" no alcanza para justificar un traductor que pone nurse en femenino?** Porque el sistema no es un modelo descriptivo sino un agente que actúa en la sociedad, y que algo haya sido siempre así no quiere decir que queramos que siga siéndolo.
6. **¿Por qué hay que buscar sesgos después del despliegue?** Porque el sistema cambia el mundo al funcionar y pueden aparecer sesgos nuevos.

</details>

---

## 6. Sesgo algorítmico, amplificación y métricas como incentivo
**Dónde:** C2P1 42:36, C2P1 43:13, C2P1 43:47, C2P1 44:19, C2P1 44:52, C2P1 45:27, C2P1 46:03, C2P1 46:37, C2P1 47:47, C2P1 48:21, C2P1 48:54, C2P1 49:26, C2P1 50:03, C2P1 50:34, C2P1 51:07, C2P1 51:43, C2P1 52:16, C2P1 53:55, C2P1 55:38, C2P1 56:11, C2P1 56:44, C2P1 57:53, C2P1 59:02, C2P1 59:35, C2P1 1:00:10, C2P1 1:00:42, C2P1 1:01:51, C2P1 1:02:26, C2P1 1:03:02, C2P1 1:04:09, C2P1 1:04:42, C2P1 1:05:16, C2P1 1:05:53, C2P1 1:06:25, C2P1 1:06:57, C2P1 1:08:03, C2P1 1:08:36, C2P1 1:09:09, C2P1 1:09:43, C2P1 1:10:15, C2P1 1:10:48

### La clase mayoritaria como "gran atractor"
- Ante un problema desbalanceado, el algoritmo asigna los ejemplos dudosos a la clase mayoritaria porque eso minimiza el error: un ejemplo cualquiera tiene alta probabilidad de pertenecer a esa clase. Es el sesgo algorítmico más conocido y el más difícil de erradicar C2P1 42:36, C2P1 43:13, C2P1 43:47.
- Está muy ligado a la evaluación: si tu único incentivo es minimizar el error, va a pasar una y otra vez. En el caso de Países Bajos, el incentivo era reducir el costo de las inspecciones manuales, y el daño a las personas no formaba parte de lo que el sistema aprendía C2P1 44:19, C2P1 44:52.

### Amplificación: el diagnóstico más barato que existe
- **Qué es.** El predictor no reproduce la proporción de la clase mayoritaria: la exagera. Si el dataset es 80 y 20, un modelo con sesgo de amplificación predice 90 o 100% de la mayoritaria C2P1 45:27, C2P1 46:03.
- **Cómo se diagnostica.** Comparando la distribución de las predicciones con la del dataset. Si tu conjunto de evaluación es 90 y 10 y tus predicciones son 95 y 5, tenés amplificación. "No cuesta absolutamente nada" hacer este diagnóstico C2P1 45:27, C2P1 47:47.
- **El contraste con el fraude.** En detección de fraude, que también es muy desbalanceada, un sistema común diría que nada es fraude; ahí bancos y distribuidoras eléctricas sí invierten en métodos especiales, porque ahorran plata. Laura contrasta esa inversión con la falta de recursos para adaptar sistemas a personas con síndrome de Down C2P1 46:03, C2P1 46:37, C2P1 47:11.
- **Qué hacer: mejores incentivos.** "Siempre, siempre. Esa es la solución." A veces cuesta negociarlo con quienes deciden, porque implica no priorizar solo lo económico. El trabajo de quien hace ciencia de datos es caracterizar mejor el incentivo, en general poniendo restricciones al espacio de soluciones C2P1 47:47, C2P1 48:21, C2P1 48:54.
- **Restricciones sobre el espacio de funciones.** Si había 30 funciones posibles, descartás las que no cumplen un incentivo: por ejemplo, las que clasifican mal a grandes clientes o las que producen muertes. Pueden ser restricciones duras o probabilísticas C2P1 49:26, C2P1 50:03, C2P1 50:34.
- **Optimización multiobjetivo.** Cuenta que alguien de Spotify explicó que así combinan las recomendaciones por filtrado colaborativo con las recomendaciones pagas (el lugar donde lo contó está deformado; dudoso) C2P1 50:03, C2P1 50:34, C2P1 51:07.

### El paper "Men also like shopping"
- Laura lo ubica alrededor de 2017 y dice que ganó el premio al mejor paper de su conferencia (**para verificar**). El título completo que lee es "Men also like shopping: reducing gender bias amplification using corpus-level constraints" C2P1 51:07, C2P1 52:16.
- **El problema:** describir una escena a partir de una imagen (acción, agente, objeto, instrumento), un problema clásico de IA desde los años 70 C2P1 52:50, C2P1 53:22.
- **El sesgo:** en la actividad cooking, el dataset tenía 33% más probabilidad de mujeres que de hombres, y el modelo entrenado subía la disparidad al 68%. Otro ejemplo: la misma foto de un hombre se etiquetaba como mujer si sostenía una escoba y como hombre si sostenía un taladro (**para verificar** las cifras) C2P1 53:55, C2P1 55:38, C2P1 56:11.
- **La solución:** restricciones expresadas como lagrangianos (un algoritmo de inferencia aproximada basado en relajación lagrangiana), que funcionan como un metaalgoritmo sobre el algoritmo de inferencia: prefieren las funciones cuyas predicciones mantienen la distribución del dataset original C2P1 56:11, C2P1 56:44, C2P1 57:53, C2P1 58:28.
- **El resultado:** la precisión se mantiene. El algoritmo se quedaba con la primera función que encontraba en una búsqueda aproximada; buscando más, aparece una con el mismo error que no amplifica la clase mayoritaria. Cuesta más tiempo de modelado y más horas de cálculo, pero el modelo comete menos errores contra la clase minoritaria C2P1 59:02, C2P1 59:35, C2P1 1:00:10.

### Alternativas más artesanales
El diagnóstico es siempre el mismo (distribución de predicciones distinta de la poblacional), y las mitigaciones que ya conocés son C2P1 1:00:42:
- balancear el dataset de entrenamiento;
- cambiar la métrica para penalizar más un tipo de error;
- pesar distinto los errores de cada clase;
- curar características para que pesen más las que diferencian a las clases, con embeddings o a mano.

Daniela pregunta si balancear resuelve el problema. Laura responde que es una solución posible y lo primero que ella prueba, aunque no la más adecuada, porque los datos reales sí están desbalanceados y "estás tergiversando un poco la realidad"; depende de qué tan buen modelo necesites C2P1 1:01:51, C2P1 1:02:26, C2P1 1:03:02, C2P1 1:03:35.

### Las métricas son tu incentivo
- **Macro average.** En lugar de reducir el error general, promediá el error por clase dando a cada clase el mismo voto. Con F1 de 98% en una clase que es el 80% de la población y de 30% en la que es el 20%, el promedio cambia mucho según cómo pondere. Está implementado en scikit-learn, que ofrece varias formas de promediar, entre ellas macro y micro C2P1 1:04:42, C2P1 1:05:16, C2P1 1:05:53, C2P1 1:06:25, C2P1 1:06:57, C2P1 1:08:03.
- **Lo simple también se comunica fácil.** No hace falta saber lagrangianos para trabajar equidad: hay nociones intuitivas que se implementan y se explican a quienes deciden C2P1 1:08:36, C2P1 1:09:09.
- **Métricas proxy.** Muchas veces queremos medir algo invisible, como el engagement, y medimos otra cosa: el tiempo de reproducción de un video o el click through en lugar de la conversión. Termina pasando que optimizamos métricas que creemos alineadas con lo que importa y no lo están, como la copa de vino C2P1 1:09:09, C2P1 1:09:43, C2P1 1:10:15, C2P1 1:10:48.

<details>
<summary>Preguntas de repaso del módulo 6 (con respuestas)</summary>

1. **¿Por qué los algoritmos tienden a la clase mayoritaria?** Porque asignar los casos dudosos a la clase mayoritaria minimiza el error cuando ese es el único incentivo.
2. **¿Cómo diagnosticás amplificación?** Comparando la distribución de las predicciones con la del dataset: si el dataset es 90 y 10 y las predicciones 95 y 5, hay amplificación.
3. **¿Qué propone Laura como solución general?** Mejores incentivos, expresados en general como restricciones sobre el espacio de soluciones.
4. **¿Qué mostró "Men also like shopping"?** Que con restricciones lagrangianas se puede mantener la distribución del dataset en las predicciones sin perder precisión.
5. **¿Por qué balancear el dataset no es la solución ideal?** Porque los datos reales sí están desbalanceados y el modelo queda ajustado a una realidad distorsionada; igual es lo primero que conviene probar.
6. **¿Qué cambia el macro average?** Le da el mismo peso al error de cada clase, así que el error en las clases minoritarias pesa más en la métrica agregada.

</details>

---

## 7. Métricas de equidad y escenarios de daño
**Dónde:** C2P1 1:10:48, C2P1 1:11:21, C2P1 1:11:55, C2P1 1:12:28, C2P1 1:13:03, C2P1 1:14:10, C2P1 1:14:43, C2P1 1:15:17, C2P1 1:15:52, C2P1 1:16:25, C2P1 1:17:00, C2P1 1:17:34, C2P1 1:18:08, C2P1 1:18:41, C2P1 1:19:16, C2P1 1:19:47, C2P1 1:20:24, C2P1 1:20:58, C2P1 1:22:43, C2P1 1:23:20, C2P1 1:24:25, C2P1 1:25:28, C2P1 1:25:58, C2P1 1:26:31, C2P1 1:27:06, C2P1 1:27:42, C2P1 1:28:15, C2P1 1:29:20, C2P1 1:29:56, C2P1 1:30:30, C2P1 1:31:02, C2P1 1:31:35, C2P1 1:32:08, C2P1 1:32:40, C2P1 1:33:13, C2P1 1:33:46, C2P1 1:34:21, C2P1 1:35:27, C2P1 1:36:01, C2P1 1:36:35, C2P1 1:37:08, C2P1 1:37:40, C2P1 1:38:14, C2P1 1:38:48, C2P1 1:39:21, C2P1 1:39:55, C2P1 1:40:28, C2P1 1:41:02, C2P1 1:41:38, C2P1 1:42:13, C2P1 1:42:47, C2P1 1:43:25, C2P1 1:43:56, C2P1 1:44:30, C2P1 1:45:05, C2P1 1:45:38, C2P1 1:46:45, C2P1 1:47:18, C2P1 1:47:53, C2P1 1:48:28, C2P1 1:49:03, C2P1 1:49:37

### Qué es equidad en aprendizaje automático
- Un sistema es justo cuando sus resultados se distribuyen de forma independiente (no necesariamente homogénea) de ciertas variables que consideramos sensibles o protegidas, como género, raza o religión en un sistema de riesgo crediticio. Sí va a depender de otras variables, como el respaldo económico; si no, no sería aprendizaje automático C2P1 1:11:21, C2P1 1:11:55, C2P1 1:12:28.
- Lo que se busca es detectar comportamientos discriminatorios que producen daños a través de una distribución no homogénea del error entre grupos definidos por la variable protegida C2P1 1:14:10, C2P1 1:14:43, C2P1 1:15:52.
- **Minorizado no es minoritario.** Estos grupos suelen estar minorizados: no son el grupo dominante, aunque no sean menos. Si no sabés, recurrí a quienes saben C2P1 1:15:17.
- **No toda discriminación es un daño.** Un algoritmo de crédito discrimina a quien no tiene respaldo económico, y eso es su objetivo; por eso primero hay que acordar qué es un daño C2P1 1:15:52, C2P1 1:16:25, C2P1 1:19:47.
- **Las variables no son discriminatorias; el comportamiento sí.** Ante la pregunta de Ender, Laura explica que las variables son la forma de partir la población para comparar, porque en el agregado entero no se puede ver ninguna diferencia C2P1 1:18:41, C2P1 1:19:16.

### Formalizar un escenario de daño: tres definiciones
1. **El grupo protegido** y su complemento, el grupo privilegiado.
2. **Qué se predice** (por ejemplo, riesgo crediticio alto o bajo).
3. **Qué errores son más graves:** los falsos positivos, los falsos negativos o alguna relación entre ellos C2P1 1:16:25, C2P1 1:17:00, C2P1 1:17:34.

Definir los errores graves requiere consenso, porque en un grupo social hay quien considera más grave un error que otro. Laura lo compara con la diferencia entre jacobinos y girondinos, y con la libertad condicional: hay quien cree que es peor liberar a quien va a delinquir y quien cree que es peor encerrar a quien no lo haría. Eso se consensúa con el grupo que va a tomar la decisión C2P1 1:17:34, C2P1 1:18:08, C2P1 1:18:41.

### Dos escenarios de daño resueltos en clase
| | COMPAS (libertad condicional) | Anonimización de texto clínico |
|---|---|---|
| Objetivo del proyecto | Evitar que una persona cometa un delito y preservar el derecho a la libertad | Poner una capa más de seguridad sobre datos muy sensibles para poder compartirlos entre instituciones de salud |
| Qué se predice | Nivel de riesgo de reincidencia, con datos del histórico de condenas | Qué partes del texto permiten reidentificar al titular (por ejemplo, "Avenida Rivadavia 742") |
| Variable protegida | Raza | Edad |
| Grupo protegido y privilegiado | Personas negras y personas blancas | Niños (por más vulnerables) y adultos |
| Error más grave | Falso positivo: privar de libertad a quien no reincide, contra la presunción de inocencia, según la legislación de Estados Unidos | Falso negativo: no anonimizar un dato sensible expone a la persona, según la legislación argentina vigente. El falso positivo solo hace el texto más difícil de leer |
| Dónde | C2P1 1:27:42, C2P1 1:28:15, C2P1 1:29:20 | C2P1 1:29:56, C2P1 1:30:30, C2P1 1:31:02, C2P1 1:31:35, C2P1 1:32:08, C2P1 1:32:40 |

En COMPAS, ya la distribución de las predicciones era distinta: para las personas negras el riesgo se distribuía de forma pareja y para las blancas estaba muy cargado hacia el riesgo bajo C2P1 1:28:15.

### Tipos de daño
| Tipo | Qué es según la clase | Ejemplo |
|---|---|---|
| De asignación | A un grupo se le asignan más recursos u oportunidades: becas, vacantes, ayudas | Un sistema de selección de personal que descarta mujeres para puestos técnicos, si consideramos que una oferta laboral es un recurso |
| De calidad de servicio | Un grupo recibe mejor servicio que otro | No poder encontrar tus fotos porque quedaron mal etiquetadas |
| De representación | Estereotipos que hacen que un grupo tenga menos oportunidades | Sylvester Stallone: tenía un Óscar, pero por guion original, y en Hollywood solo le ofrecían papeles de protagonista musculoso, nunca de guionista |

Fuentes: C2P1 1:19:47, C2P1 1:20:24, C2P1 1:20:58, C2P1 1:22:43, C2P1 1:23:20, C2P1 1:23:52.

### Ejercicios de pensamiento sobre daños
- **Selección de personal.** "Esto no es ficción": según Laura, Amazon tuvo sanciones firmes porque su filtro de currículums descartaba directamente a las mujeres para puestos técnicos, ya que la mayoría de quienes trabajaban en esos puestos eran hombres (**para verificar** lo de las sanciones). En clase se responde que es un daño de representación y también de asignación C2P1 1:24:25, C2P1 1:24:57, C2P1 1:25:28, C2P1 1:25:58.
- **Etiquetado de imágenes.** Un sistema de Google etiquetaba a personas negras como gorilas; Laura menciona que pasó con personas del Congreso de Estados Unidos (**para verificar** ese detalle). Es un daño de representación que puede incidir en resultados electorales, y también de calidad de servicio C2P1 1:25:58, C2P1 1:26:31, C2P1 1:27:06.

### Del escenario a las métricas
- **Desagregar, pero no hasta el caso.** Las métricas más agregadas ocultan más. Ir caso por caso no permite decidir, porque te quedás en lo anecdótico, y las soluciones anecdóticas benefician a quien puede quejarse, que suele ser "la más privilegiada de las no privilegiadas" C2P1 1:33:13, C2P1 1:33:46, C2P1 1:34:21.
- **La idea básica.** Partís de la matriz de confusión de cada grupo y comparás. En las filminas (prestadas por Mariela, de la licenciatura en ciencia de datos de la UNSAM; apellido dudoso), el grupo verde y el naranja tienen la misma tasa de falsos negativos pero distinta tasa de falsos positivos C2P1 1:34:21, C2P1 1:35:27, C2P1 1:36:01, C2P1 1:36:35.
- **Qué tasa mirar depende del escenario.** En anonimización importan los falsos negativos; si son iguales en los dos grupos, no hay discriminación, aunque con un 50% de falsos negativos Laura no pondría el sistema en producción "jamás". En COMPAS importan los falsos positivos, y ahí el grupo naranja está mucho peor: eso es discriminatorio C2P1 1:37:08, C2P1 1:37:40, C2P1 1:38:14.
- **El proceso:** definir el escenario de daño, mirar las matrices de confusión por grupo y graficar las tasas en un diagrama de barras C2P1 1:38:48, C2P1 1:39:21.

### Métricas agregadas
Las definiciones vienen del artículo de Wikipedia sobre equidad y de un curso de Google, adaptadas en la notebook C2P1 1:39:55. Sirven para comunicar en un número (el "elevator pitch" con un diputado) y para comparar modelos; Laura prefiere construir la métrica a partir de la pregunta del problema C2P1 1:41:38, C2P1 1:42:13, C2P1 1:42:47, C2P1 1:45:05, C2P1 1:45:38.

| Métrica | En COMPAS responde | En anonimización responde |
|---|---|---|
| Tasa de falsos positivos | De quienes no reinciden, ¿a qué proporción no se le otorga la libertad condicional? | De los datos no sensibles, ¿qué proporción se clasificó como sensible? |
| Equal opportunity | De quienes reinciden, ¿a qué proporción no se le otorgó la libertad condicional? | De los datos sensibles, ¿qué proporción se identificó correctamente? |
| Predictive parity | De quienes obtienen la libertad condicional, ¿qué proporción reincidiría? | De las palabras etiquetadas como sensibles, ¿qué proporción lo era? |
| Statistical parity | ¿Qué proporción de personas no obtiene la libertad condicional? | ¿Qué proporción de entidades se etiqueta como sensible? |

Fuentes de la tabla: C2P1 1:43:25, C2P1 1:43:56, C2P1 1:44:30, C2P1 1:45:05. También menciona equalized odds, que combina verdaderos positivos y falsos positivos para ver si los grupos protegidos y no protegidos tienen las mismas chances de ser reconocidos correctamente C2P1 1:40:28, C2P1 1:41:02. Las preguntas de la tabla están tal como las dice en clase; antes de usarlas, chequealas contra la notebook, porque la transcripción es oral y algunas formulaciones pueden haber salido imprecisas.

### La clínica de equidad y la notebook
- Lo que presenta sale de una "clínica de equidad" que hace con Mariela, pensada para que la puedas usar de forma independiente; la página tiene slides, una notebook de métricas básicas y ejemplos con COMPAS y otros datasets clásicos C2P1 1:13:03, C2P1 1:13:36, C2P1 1:46:45.
- **Estructura de la notebook:** cargar el dataset, formalizar los escenarios de daño, visualizar las distribuciones, revisar y refinar las definiciones, analizar el comportamiento del modelo desagregando y hacer un diagnóstico. No incluye mitigación; en la página de la materia dejaron un método de Google para mitigar en redes neuronales C2P1 1:47:18, C2P1 1:47:53.
- **Solo necesitás las predicciones.** La auditoría trabaja sobre las predicciones de un modelo, sin acceso al modelo ni ejecutarlo, así que la podés aplicar a cualquier cosa: organismos de aguas profundas contra superficiales, o el pronóstico del tiempo en Córdoba contra Iguazú C2P1 1:48:28, C2P1 1:49:03, C2P1 1:49:37.

<details>
<summary>Preguntas de repaso del módulo 7 (con respuestas)</summary>

1. **¿Cuándo es justo un sistema según la definición de la clase?** Cuando sus resultados son independientes de las variables protegidas, aunque dependan de otras variables legítimas.
2. **¿Qué tres cosas definen un escenario de daño?** El grupo protegido (y el privilegiado), qué se predice y qué errores son más graves.
3. **¿Por qué en anonimización el error grave es el falso negativo?** Porque un dato sensible sin anonimizar expone a la persona; el falso positivo solo hace el texto más difícil de leer.
4. **¿Qué daño sufrió Sylvester Stallone según el ejemplo?** Un daño de representación: por el estereotipo de hombre musculoso no le ofrecían trabajo de guionista, aunque su Óscar era por guion.
5. **¿Por qué no conviene desagregar hasta el caso individual?** Porque te quedás en lo anecdótico y solo ayudás a quien puede quejarse.
6. **¿Qué necesitás para hacer una auditoría de equidad con la notebook?** Las predicciones del modelo; no hace falta acceder al modelo ni ejecutarlo. (Aclaración mía: para armar las matrices de confusión también vas a necesitar las etiquetas reales y la variable que define los grupos.)

</details>

---

## 8. La notebook de equidad paso a paso
**Dónde:** C2P2 0:05, C2P2 0:39, C2P2 1:13, C2P2 1:46, C2P2 2:20, C2P2 2:54, C2P2 3:59, C2P2 4:31, C2P2 5:05, C2P2 5:39, C2P2 6:12, C2P2 7:17, C2P2 7:53, C2P2 8:26, C2P2 9:33, C2P2 10:07, C2P2 10:41, C2P2 11:19, C2P2 11:58, C2P2 12:32, C2P2 13:36, C2P2 14:11, C2P2 14:43, C2P2 15:15, C2P2 15:48, C2P2 16:21, C2P2 16:54, C2P2 17:28, C2P2 18:02, C2P2 18:34, C2P2 19:07, C2P2 20:15, C2P2 20:49, C2P2 21:20, C2P2 21:55, C2P2 22:28, C2P2 24:42, C2P2 25:14, C2P2 25:46, C2P2 26:22, C2P2 26:55, C2P2 28:04, C2P2 44:11, C2P2 44:46, C2P2 45:20, C2P2 45:55, C2P2 46:30, C2P2 47:38, C2P2 48:12, C2P2 48:46, C2P2 49:18, C2P2 49:56, C2P2 50:28, C2P2 51:05, C2P2 51:38, C2P2 52:11, C2P2 52:47, C2P2 53:21, C2P2 53:54, C2P2 54:27, C2P2 54:59, C2P2 55:34, C2P2 56:13, C2P2 56:50

Después de la pausa, Laura recorre la notebook de la clínica de equidad celda por celda. Es el "práctico" de la clase 2: podés ejecutarla vos mientras ella la muestra C2P2 3:26.

### Para qué está pensada
- Trae una metodología paso a paso y herramientas "muy básicas, muy básicas". Al final hay links a frameworks que ya traen todas las métricas de equidad, pero la idea es que puedas construir tus propias métricas sin haber estudiado mucha estadística de equidad C2P2 0:05, C2P2 0:39, C2P2 1:13.
- Usa una definición operativa de sesgo, que después hay que conectar con los valores acordados con el grupo al que afecta el desarrollo: **la distribución no homogénea del error a través de diferentes grupos, de una forma que se considera dañina** C2P2 1:13, C2P2 1:46.
- Trabaja con una versión muy simplificada de COMPAS que está en el repositorio público de otro framework europeo; hay Colabs para otros datasets, y en otros frameworks de fairness hay más datasets para explorar (los nombres de los frameworks están deformados; ver glosario) C2P2 2:20, C2P2 2:54, C2P2 3:59.
- Importa librerías "superestándares", para que no se rompa C2P2 3:26.

### Los pasos
1. **Cargar el dataset y asignar columnas.** La notebook asume que cada fila trae el valor real (ground truth, la columna `label value`) y la predicción del modelo (la columna `score`), además de raza, sexo y categoría de edad. Si tus datos no tienen predicciones, podés entrenar un modelo con otra notebook que dejan C2P2 4:31, C2P2 5:05.
2. **Formalizar los escenarios de daño:** qué grupos son protegidos y cuáles privilegiados, en qué consisten los daños y qué errores los producen C2P2 5:39.
3. **Visualizar la distribución de cada variable** con un widget. Por sexo la diferencia es chica; por edad, los mayores de 45 tienen mucho más riesgo bajo y los menores de 25 mucho más riesgo alto; por raza, la diferencia entre personas negras y blancas es "tremenda", y la de hispanos se parece a la de blancos. El dataset original tiene más categorías raciales que blanco y negro C2P2 6:12, C2P2 7:17, C2P2 7:53, C2P2 8:26, C2P2 9:00.
4. **Usar esa exploración para refinar el grupo protegido.** El análisis suele estar dirigido por hipótesis previas, pero con pocas variables podés mirarlas todas C2P2 9:33, C2P2 10:07.
5. **Comparar realidad contra predicción.** Ya en el agregado hay más riesgo bajo en la realidad que en las predicciones: "las lagrangianas nos habrían ajustado esto un poco mejor" C2P2 10:41, C2P2 11:19.
6. **Mirar cuánta población hay en cada grupo.** Si un grupo es muy minoritario, quizás se modela mal (le pasó históricamente a las mujeres en riesgo crediticio, que es el ejemplo de Google para mitigar en redes neuronales). Entre personas negras y blancas no hay tanto desbalance, así que una diferencia grande no se explica solo por falta de representación. Hacer análisis y visualización es básico, "por eso es la primera materia de su diplomatura" C2P2 11:58, C2P2 12:32, C2P2 13:04, C2P2 13:36.
7. **Pasar a dos grupos y a clase binaria.** Las métricas comparan grupo protegido contra privilegiado y asumen una clase binaria. La notebook se queda con los grupos que superan el 30% de las ocurrencias, pero podés programar otra agrupación (por ejemplo, negros contra todo el resto). El score original tiene un rango de 10 y hay que binarizarlo; esta versión ya viene binarizada C2P2 14:11, C2P2 14:43, C2P2 15:15, C2P2 15:48, C2P2 18:02.
8. **Ver realidad y predicción por grupo.** Desagregada, la distribución no es la misma, aunque en el global pudiera serlo: por eso importa definir la variable protegida C2P2 16:21, C2P2 16:54, C2P2 17:28.
9. **Confirmar el escenario:** realidad = `label value`, predicción = `score`, atributo protegido = raza. Hacen falta realidad y predicción para calcular el error, y el atributo para ver si el error es homogéneo entre grupos C2P2 18:34, C2P2 19:07.
10. **Empezar por la métrica más agregada, el accuracy.** Con un 65% "que le erra casi a la mitad" ya podrías decidir no desplegar. Después, accuracy por grupo: alrededor de 64% para afroamericanos y 67% para caucásicos, y más alto en los grupos más chicos (cifras leídas en clase sobre la versión simplificada) C2P2 20:15, C2P2 20:49, C2P2 21:20, C2P2 21:55.
11. **Mirar casos individuales cuando hay errores inaceptables.** Un tratamiento que le saca el dolor de cabeza al 99% y mata al 1% restante se descubre caso por caso; da el ejemplo de la dipirona, que según ella en Europa está prohibida y se usa como rescate en hospitales (**para verificar**). Pero el caso por caso no sirve para decisiones sistémicas C2P2 21:55, C2P2 22:28, C2P2 23:02, C2P2 23:37, C2P2 24:10, C2P2 24:42.
12. **Matriz de confusión por grupo y gráfico de tasas.** "La matriz de confusión es tu amiga", pero la general no muestra diferencias entre grupos. Por grupo ya se ven, y se entienden mejor graficando la proporción de falsos positivos y de falsos negativos de cada grupo: las personas negras tienen muchos más falsos positivos y las blancas muchos más falsos negativos, lo mismo que mostraba la tabla de ProPublica de 2016. Es "el pilar básico" del análisis de equidad C2P2 24:42, C2P2 25:14, C2P2 25:46, C2P2 26:22, C2P2 26:55, C2P2 28:04.
13. **Calcular métricas agregadas** (ver abajo) C2P2 44:11.

### Métricas agregadas con ejemplos de admisión universitaria
Laura lee los ejemplos de la notebook (salen del curso de Google, según la clase 2 parte 1). Algunas cifras de los ejemplos se leen de forma confusa en la grabación, así que conviene revisarlas en la notebook.
| Métrica | Cuándo sirve o qué mide según la clase | Dónde |
|---|---|---|
| Tasa de falsos positivos | De todos los negativos, cuántos se etiquetaron como positivos. Útil cuando un falso positivo implica un daño significativo para la persona, como una sanción por "riesgo alto" de delito o de impago | C2P2 45:55, C2P2 46:30, C2P2 47:05, C2P2 47:38 |
| Equal opportunity (balance de falsos negativos) | Si los miembros de los grupos protegido y no protegido tienen la misma probabilidad de ser asignados correctamente a la clase positiva (por ejemplo, recibir una beca) | C2P2 48:12, C2P2 48:46 |
| Predictive parity | No la hay si se admite al 80% de los estudiantes calificados de un grupo y al 30% de los de otro | C2P2 49:18 |
| Paridad demográfica | No la hay si un grupo es admitido en proporción distinta que otro (48% contra 14%), sin importar si están calificados | C2P2 49:56, C2P2 50:28 |
| Equalized odds | Mira a la vez la aceptación de calificados y el rechazo; un ejemplo con tasas de rechazo de 70% y 90% en dos grupos. Laura dice que es "sutil" y que la usaron varias veces | C2P2 50:28 |

### Recomendaciones de la docente
- **Gráficos para decidir y comunicar; métricas agregadas para rankear y optimizar.** Un indicador compacto sirve para elegir entre modelos o como criterio en la búsqueda de hiperparámetros, que son los que ayudan a navegar el espacio de funciones C2P2 44:46, C2P2 45:20, C2P2 45:55, C2P2 51:05.
- **Umbrales de tolerancia.** Quienes auditan sistemas profesionalmente eligen la métrica relevante para el problema y fijan un umbral: ningún modelo que lo supere es aceptable C2P2 51:38.
- **No podés maximizar todas.** Algunas métricas de equidad son complementarias: si una es alta, otra es baja por definición; remite a la sección 5.4 de un libro que no nombra en voz alta (dudoso cuál) C2P2 52:11.
- **Explicabilidad.** SHAP dice cuánto contribuye cada característica a una decisión, de forma agnóstica al modelo, útil para ver si te negaron un crédito por una variable protegida; What-If arma contrafácticos comprobables ("¿y si saco esta variable?") y ayuda a medir el impacto de una mitigación. La explicabilidad permite que quien decide actúe C2P2 52:47, C2P2 53:21, C2P2 53:54, C2P2 54:27, C2P2 54:59, C2P2 55:34.
- **Más material en la notebook:** notebooks con COMPAS completo, el ejercicio de equidad del curso intensivo de machine learning de Google, una notebook de fairness en R y un artículo sobre métricas de equidad en algoritmos públicos C2P2 52:47, C2P2 56:13, C2P2 56:50.
- **Sobre los hispanos en COMPAS.** Luciana comenta un artículo según el cual su tasa de reincidencia era bastante más baja que la de otros grupos, y que hay análisis por edad, sexo y otros grupos en las notebooks referenciadas (**para verificar**) C2P2 1:22:28, C2P2 1:23:01, C2P2 1:23:35.

### Instanciar tu propio problema como un problema de equidad
Laura pregunta cuántas personas creen que pueden aplicarlo al dataset de su mentoría, y aclara que no hace falta que haya una cuestión de justicia: alcanza con que un grupo se modele peor que otro C2P2 28:04, C2P2 28:38, C2P2 29:11.
- **Fútbol:** si tus predicciones de goles erran más hacia abajo con jugadores de divisiones inferiores que de primera C2P2 29:11, C2P2 29:44.
- **Básquet:** un estudiante cuenta lo que vio en un congreso (el "encaje" de un jugador con sus compañeros, posiciones etiquetadas "a ojo"). Laura lo reformula: si los contratos dependen de un modelo que estima puntos y ese modelo erra sistemáticamente en contra de un grupo de jugadores, hay un daño (menos plata, peores equipos), y como es sistemático se puede prevenir de forma sistemática. Agrega que la mitigación muchas veces es conseguir mejores datos o características para el grupo mal modelado C2P2 32:28, C2P2 34:09, C2P2 35:16, C2P2 35:49, C2P2 36:22, C2P2 36:55, C2P2 39:09, C2P2 39:41.
- **Al final decide un humano.** Lo que podés hacer como científico de datos es darle información que lo ayude a decidir mejor y más alineado con valores C2P2 34:09.
- **Pesca de cangrejos (mentoría de Mariano):** el muestreo es muy asimétrico porque una especie es mucho más abundante. El reto es definir el daño (económico o ecológico, por ejemplo la extinción de una especie); si los falsos negativos son los que llevan a ese daño y son más frecuentes en una especie, habría que penalizarlos más, balancear o aplicar lagrangianos C2P2 41:54, C2P2 42:27, C2P2 43:00, C2P2 43:33.

<details>
<summary>Preguntas de repaso del módulo 8 (con respuestas)</summary>

1. **¿Cuál es la definición operativa de sesgo de la notebook?** La distribución no homogénea del error a través de diferentes grupos, de una forma que se considera dañina.
2. **¿Qué columnas necesita la notebook?** El valor real, la predicción del modelo y el atributo que define los grupos.
3. **¿Por qué hay que pasar a dos grupos y a clase binaria?** Porque las métricas comparan un grupo protegido con su complemento y asumen una clase binaria.
4. **¿Qué gráfico es "el pilar básico" del análisis?** La proporción de falsos positivos y de falsos negativos por grupo.
5. **¿Para qué recomienda usar las métricas agregadas?** Para rankear y optimizar modelos, o fijar umbrales; para decidir y comunicar, los gráficos.
6. **¿Por qué no podés elegir el modelo que maximiza todas las métricas de equidad?** Porque algunas son complementarias: si una sube, otra baja por definición.
7. **¿Qué hace SHAP y qué hace What-If?** SHAP mide cuánto contribuye cada característica a una decisión; What-If prueba contrafácticos, como sacar una variable y ver cómo cambia la predicción.

</details>

---

## 9. Auditar sistemas sin una definición de error: imágenes, texto y embeddings
**Dónde:** C2P2 57:24, C2P2 57:58, C2P2 58:32, C2P2 59:04, C2P2 59:36, C2P2 1:00:09, C2P2 1:00:43, C2P2 1:01:20, C2P2 1:02:37, C2P2 1:03:13, C2P2 1:03:45, C2P2 1:04:21, C2P2 1:04:56, C2P2 1:05:30, C2P2 1:06:02, C2P2 1:06:36, C2P2 1:07:10, C2P2 1:07:44, C2P2 1:08:16, C2P2 1:09:52, C2P2 1:10:25, C2P2 1:10:59, C2P2 1:11:39, C2P2 1:12:12, C2P2 1:12:51, C2P2 1:13:24, C2P2 1:13:58, C2P2 1:14:31, C2P2 1:15:04, C2P2 1:15:37, C2P2 1:16:11, C2P2 1:16:44, C2P2 1:17:53, C2P2 1:18:26, C2P2 1:18:58, C2P2 1:19:37, C2P2 1:20:09, C2P2 1:20:43, C2P2 1:21:16, C2P2 1:21:52, y el video de 2020 "¿Es tan grave?" (2020-Grave 1:14, 2020-Grave 2:25)

### El problema
Las métricas de la notebook se basan en el error, pero muchos sistemas no tienen una definición de error: el aprendizaje no supervisado y los sistemas generativos, que resuelven problemas de respuesta abierta donde puede haber muchas respuestas buenas (un cuento para chicos de 5 años sin antagonista ni violencia tiene "un montón" de versiones válidas). Ahí el accuracy es "totalmente inadecuado" C2P2 57:24, C2P2 57:58, C2P2 58:32, C2P2 59:04, C2P2 59:36, C2P2 1:00:09.

**La salida:** igual se puede auditar de forma sistemática. Imaginás escenarios de daño y comparás grupos, pero con otra medida que no es el error C2P2 1:00:43, C2P2 1:01:20. Germán sugiere la valoración del usuario; Laura responde que sirve, pero sigue siendo la valoración de una respuesta puntual C2P2 1:02:37.

### Casos de exploración sistemática
- **Recorte de miniaturas de Twitter.** Un sábado alguien notó que, con una foto alargada de dos personas, la miniatura automática elegía la cara blanca. Mucha gente se puso a probar y se vio que el algoritmo prefería caras blancas y también caras sonrientes; a alguien "se le ocurrió lo de la sonrisa", y si no se te ocurre hacer esa comparación, "no la ves". No son exactamente errores sino tendencias C2P2 1:03:13, C2P2 1:03:45, C2P2 1:04:21, C2P2 1:04:56, C2P2 1:05:30, C2P2 1:06:02. El video de 2020 cuenta el mismo caso 2020-Grave 1:14.
- **El reconstructor de alta resolución.** Con una foto pixelada de Obama devolvía una persona blanca; las reconstrucciones eran mejores para personas blancas y tendían a representar a las negras como blancas, un sesgo de representación "tremendo". En esta clase Laura lo atribuye a un producto de Meta y dice que Yann LeCun respondió que era un problema de los datos de entrenamiento (en el video de 2020 se lo asocia a la Universidad de Duke y a un premio Turing sin nombre; **para verificar** el origen del sistema). Su crítica: quien saca un producto entrenado se tiene que hacer cargo de sus efectos, porque mucha gente no puede reentrenarlo. La exploración sistemática encontró además que a las personas peladas les ponía pelo y a las personas con anteojos las devolvía sin anteojos, maquilladas y con cejas depiladas C2P2 1:06:36, C2P2 1:07:10, C2P2 1:07:44, C2P2 1:08:16, C2P2 1:09:52, C2P2 1:10:25, C2P2 1:10:59, 2020-Grave 3:00, 2020-Grave 4:46.
- **La lección.** Contra el parche anecdótico (sacar la categoría gorila, arreglar la foto de Obama), lo que sirve es una exploración sistemática que reporte, por ejemplo, en qué porcentaje de casos a las personas con anteojos se las representa sin anteojos. El "error" lo definís vos después de explorar, de forma más creativa que en las métricas de equidad C2P2 1:07:10, C2P2 1:11:39, C2P2 1:12:12.
- **Modelos de lenguaje.** Un modelo abierto prefería producir "la menstruación es una enfermedad" antes que "la eyaculación es una enfermedad", y eso se traduce en textos que asocian la menstruación a problemas de salud y la eyaculación a ninguno C2P2 1:12:51, C2P2 1:13:24, C2P2 1:13:58, C2P2 1:14:31.
- **Trabajar con especialistas.** Los científicos de datos no siempre tienen el conocimiento para ver estos daños, pero pueden aportar datos sistemáticos a sociólogos y trabajadores sociales para apoyar sus hipótesis, y a partir de ahí actuar: entrenar con datos complementarios, representaciones alternativas o una capa simbólica como las barreras de seguridad de los modelos de lenguaje C2P2 1:14:31, C2P2 1:15:04, C2P2 1:15:37.

### Sesgo en embeddings
- Se eligen palabras que representan lo femenino y lo masculino (pronombres, mujer, hombre) y se mide si palabras que no deberían tener género, como profesiones, quedan más cerca de un grupo en el espacio de embeddings; estar cerca quiere decir compartir contextos de aparición C2P2 1:16:11, C2P2 1:16:44, C2P2 1:17:16.
- Desde 2016 se sabe que las profesiones quedan asociadas al género: enfermería a lo femenino, ingeniería a lo masculino C2P2 1:17:53, C2P2 1:18:26.
- La mejor mitigación es conseguir mejores datos de entrenamiento, pero estos modelos los entrenan empresas que "no comparten valores con nosotros"; la alternativa creativa puede ser no usar estos modelos para tareas críticas C2P2 1:18:26, C2P2 1:18:58.
- **Notebook de exploración de sesgos en word embeddings** (hecha por Laura y Luciana): en sus gráficos precalculados, electricista, economista, piloto y comerciante quedan más cerca de lo masculino, y cantante y florista de lo femenino. También mencionan una herramienta (la transcripción dice "Edia" o "Edas"; dudoso) cuyo GitHub está en la página; por cambios de Python algunas cosas quedaron desacopladas, y Laura dice que la notebook de la página ya está actualizada C2P2 1:19:37, C2P2 1:20:09, C2P2 1:20:43, C2P2 1:21:16, C2P2 1:21:52, C2P2 1:25:20.

<details>
<summary>Preguntas de repaso del módulo 9 (con respuestas)</summary>

1. **¿Por qué no sirven las métricas basadas en error para un sistema generativo?** Porque en un problema de respuesta abierta hay muchas respuestas buenas y no hay un valor esperado contra el cual medir.
2. **¿Cómo se audita entonces?** Con exploración sistemática: definís escenarios de daño, comparás grupos y reportás tendencias con porcentajes, no casos sueltos.
3. **¿Qué descubrió la exploración del recorte de Twitter además de la preferencia por caras blancas?** Que también prefería caras sonrientes.
4. **¿Por qué Laura critica la respuesta "es un problema de los datos"?** Porque quien saca un producto entrenado es responsable de sus efectos, y la mayoría de la gente no puede reentrenarlo.
5. **¿Qué mide un análisis de sesgo en embeddings?** Si palabras sin género, como profesiones, quedan más cerca de las palabras de lo femenino o de lo masculino.

</details>

---

## 10. Cierre: ética a lo largo de todo el ciclo de vida
**Dónde:** C2P2 1:25:53, C2P2 1:26:26, C2P2 1:26:59, C2P2 1:27:31, C2P2 1:28:06, C2P2 1:28:40, C2P2 1:29:13, C2P2 1:29:48, C2P2 1:30:23, C2P2 1:30:58, C2P2 1:31:32, C2P2 1:32:06, C2P2 1:32:40, C2P2 1:33:15, C2P2 1:33:47, C2P2 1:34:19, C2P2 1:34:56, C2P2 1:35:30, C2P2 1:36:06, C2P2 1:36:40, C2P2 1:37:13, C2P2 1:37:50, C2P2 1:38:25

### Lo ineludible: diversidad
"¿Cómo hacemos para que nuestros sistemas sean más éticos? Incorporando diversidad, sin ninguna duda" C2P2 1:26:26. Laura lo baja a cada etapa:
| Etapa | Qué propone |
|---|---|
| Framing y cocreación | Decidir con diversidad qué es y qué no es un problema C2P2 1:26:59 |
| Gobernanza | Enfoques participativos donde la diversidad no sea solo un focus group sino parte de la gobernanza del proyecto (multistakeholder), para no tener que cambiar las cosas después, cuando los incentivos económicos ponen obstáculos C2P2 1:26:59, C2P2 1:27:31 |
| Requerimientos | Traer casos que de otro modo no aparecen: "será un 1% de la población, pero tienen derecho" C2P2 1:28:40, C2P2 1:29:13 |
| Diseño | Preguntarse si las categorías son las correctas (quizás "gorila" no es una categoría que queramos) o si las personas deberían definir sus propias categorías C2P2 1:29:13 |
| Desarrollo | Revisar detalles como qué pasa con fotos oscuras o de baja resolución C2P2 1:29:48 |
| Pruebas | Exploraciones adversarias, no "le puse mi foto y la de mi novia y anda" C2P2 1:29:48, C2P2 1:30:23 |
| Despliegue | Evitar el "no lo habíamos pensado" y los parches superficiales C2P2 1:28:06, C2P2 1:28:40, C2P2 1:30:23 |

### Consensos sociales y leyes
- Además de las leyes hay códigos no escritos que también cuentan C2P2 1:30:58.
- Recuerda que Argentina adhiere a la Convención de San José (Convención Americana de Derechos Humanos; ella dice "Interamericana"), que tiene rango constitucional y dice cosas como no discriminación: las leyes fundamentales "son muy garantistas" C2P2 1:30:58, C2P2 1:31:32.
- Pide empatía con otros grupos y atención a consensos emergentes que hace 5 o 10 años no eran evidentes (estereotipos, mérito, privilegio) C2P2 1:32:06.

### Áreas de preocupación
| Área | Qué dice la clase |
|---|---|
| Confiabilidad | Es la primera que menciona la ley europea de IA. En salud se implementan sistemas con tasas de error del orden del 30% (**para verificar**); recomienda el análisis de una ONG española de transparencia sobre errores de IA en sanidad (nombre deformado; dudoso) C2P2 1:32:40, C2P2 1:33:15, C2P2 1:33:47, C2P2 1:34:19 |
| Cumplimiento de leyes y normas | C2P2 1:34:19 |
| Transparencia y rendición de cuentas | En educación, finanzas y trabajo es obligatorio por ley que un algoritmo pueda explicar en qué se basa su decisión, para que la persona tenga derecho a réplica. Si Uber no puede explicar por qué te asigna un viaje y no otro, podés denunciar discriminación, aunque necesitás un juez dispuesto a aplicar las leyes laborales (**para verificar** el alcance legal) C2P2 1:34:19, C2P2 1:34:56, C2P2 1:35:30, C2P2 1:36:06 |
| No producir daño | Ningún sistema puede matar ni discriminar gente C2P2 1:36:06 |
| Impacto ambiental | Uso intensivo de agua y electricidad en competencia con necesidades humanas, promoción de combustibles fósiles, contaminación acústica y térmica alrededor de los centros de datos C2P2 1:36:06, C2P2 1:36:40, C2P2 1:37:13 |

### Regulación
Hay declaraciones de la UNESCO y mucho "soft law", que no es lo mismo que regulación. Como regulación están la china y la europea; en Latinoamérica hay poca. Menciona un informe de 2024 de una organización que la transcripción llama "Access" (dudoso) y un índice latinoamericano de inteligencia artificial, que se actualiza C2P2 1:37:13, C2P2 1:37:50. Cierra con que lo que queda es aportar "nuestro granito de arena" para que los sistemas en los que contribuimos respeten los principios que nos parecen éticos C2P2 1:37:50, C2P2 1:38:25.

<details>
<summary>Preguntas de repaso del módulo 10 (con respuestas)</summary>

1. **¿Cuál es, según Laura, la forma ineludible de hacer sistemas más éticos?** Incorporar diversidad en todo el ciclo de vida, desde el framing y la gobernanza hasta las pruebas.
2. **¿Por qué conviene incorporar diversidad desde el principio y no después del despliegue?** Porque cambiar después es caro, los incentivos económicos lo frenan y se termina en parches superficiales.
3. **¿Qué norma argentina de rango constitucional invoca contra la discriminación?** La Convención de San José (Convención Americana sobre Derechos Humanos).
4. **¿Qué área de preocupación menciona primero la ley europea, según la clase?** La confiabilidad de los sistemas.
5. **¿Qué ejemplo usa para la transparencia en el trabajo?** Uber: si no puede explicar por qué te asigna un viaje y no otro, podés denunciar discriminación.

</details>

---

## 11. El práctico: un data statement sobre el dataset de tu mentoría
**Dónde:** C1P2 14:46, C1P2 15:19, C1P2 42:21, C1P2 42:54, C1P2 43:30, C1P2 44:07, C1P2 44:39, C1P2 45:12, C1P2 45:52, C1P2 46:27, C1P2 46:59, C1P2 47:33, C1P2 48:09, C1P2 48:45, C1P2 49:19, C1P2 49:51, C1P2 50:25, C1P2 51:01, C1P2 52:06, C1P2 52:42, C1P2 53:15, C1P2 53:50, C1P2 54:23, C1P2 54:58, C1P2 55:31, C1P2 56:04, C1P2 56:37, C1P2 57:09, C1P2 57:43, C1P2 58:17, C1P2 58:51, C1P2 59:25, C1P2 1:00:31, C1P2 1:01:03, C1P2 1:01:36, C1P2 1:02:10, C1P2 1:02:43, C1P2 1:03:18, C1P2 1:03:54, C1P2 1:04:27, C1P2 1:05:04, C1P2 1:06:12, C1P2 1:06:46, C1P2 1:07:21, C1P2 1:08:28, C1P2 1:09:35, C1P2 1:10:07, C1P2 1:10:39, C1P2 1:11:12, video de 2020 "EPCD.3 Guía para el práctico 1" completo (2020-EPCD.3 0:02 a 2020-EPCD.3 17:31), y menciones en clase: C1P1 1:37, C1P1 2:16, C1P1 28:34, C1P1 29:07, C1P1 33:01, C2P1 33:30, C2P1 34:02

> Fuentes: el video de 2020 "EPCD.3 Guía para el práctico 1" y la explicación de Luciana al final de la clase 1 de 2026 (C1P2), que repasa el video y agrega ejemplos de prácticos de años anteriores C1P2 51:32. Donde la versión de 2020 y la de 2026 difieren (tamaño de los grupos, fecha de entrega), vale la de 2026, y en todo caso **confirmalo en el aula virtual**, porque las docentes dicen que los detalles prácticos se van actualizando C1P1 2:50. La descripción del video de 2020 no dice quién habla; por el tema, el estilo y porque en 2026 lo presenta Luciana, probablemente es Luciana Benotti (dudoso).

### Para qué sirve un data statement
- La ciencia de datos es vulnerable a sesgos que dañan a personas, y un data statement es una documentación clara del dataset que ayuda a desarrolladores, usuarios y otros actores a mitigarlos 2020-EPCD.3 1:06.
- La metodología se basa en el **diseño basado en valores** (value sensitive design) 2020-EPCD.3 1:43.
- Toma la definición de sesgo de Friedman y Nissenbaum de 1996 (la transcripción dice "friedmann y nissan brawn"; dudoso): "una discriminación sistemática e injusta contra ciertos individuos o grupos en favor de otros" 2020-EPCD.3 1:43.

| Tipo de sesgo (Friedman y Nissenbaum, según el video) | Qué es | ¿Lo cubre el data statement? |
|---|---|---|
| Preexistente | Tiene origen social; por ejemplo, los word embeddings capturan sesgos del lenguaje. No es el sesgo inductivo que aprovecha el aprendizaje automático | Sí: ayuda a identificar las partes de los datos que lo contienen y decidir qué hacer con ellas 2020-EPCD.3 2:16, 2020-EPCD.3 4:29 |
| Técnico | Decisiones de implementación supuestamente neutrales, como ordenar alfabéticamente y que a una comunidad cuyos apellidos empiezan con X siempre le toque última | No, porque está en el software y no en los datos 2020-EPCD.3 2:51, 2020-EPCD.3 3:24 |
| Emergente | Un sistema entrenado en un contexto se pone en producción en otro con características diferentes | Sí: describir la muestra y a quienes recolectaron permite detectar cuándo se va a usar en otro contexto y planificar una nueva recolección 2020-EPCD.3 3:56, 2020-EPCD.3 4:29, 2020-EPCD.3 5:04 |

### Los sesgos y aspectos que repasa la clase de 2026
| Concepto | Qué dice Luciana | Dónde |
|---|---|---|
| Sesgo social | Los modelos no cometen errores al azar: los errores dañan sistemáticamente a ciertos individuos o grupos | C1P2 42:21, C1P2 42:54 |
| Sesgo emergente | Un modelo entrenado sobre unos datos se pone en producción sobre otro grupo social o contexto cultural. Ejemplo: un sistema que detectaba si un conductor se estaba quedando dormido, entrenado con imágenes de personas occidentales, daba falsas alarmas en Asia por la forma de los ojos (**para verificar** el caso) | C1P2 42:54, C1P2 43:30, C1P2 44:07 |
| Sesgo preexistente | Viene de cuestiones históricas, como las profesiones asociadas a un género | C1P2 44:07 |
| Sesgo de automatización | La tendencia a confiar de más en las recomendaciones de un sistema. No es lo mismo mostrar la respuesta automática y preguntar si está bien que pedirle a la persona que decida primero y después mostrarle qué habría dicho el sistema: en ese caso hay más desacuerdo. El orden influye | C1P2 44:39, C1P2 45:12 |
| Uso dual | Si el dataset podría usarse para algo distinto de lo planteado, si ese uso podría tener un impacto negativo o si está justificado. Se pide describirlo desde tu perspectiva y, si es relevante, decir si está de acuerdo con la ley de protección de datos personales | C1P2 45:52, C1P2 46:27 |
| Confidencialidad | Otro aspecto que aborda el práctico y que el video desarrolla | C1P2 46:59 |

- **Para qué sirve, en 2026.** Detectar sesgos y otros riesgos antes de que lleguen al usuario final C1P2 47:33. Además, si comprás un dataset y viene con esta documentación, sirve para cruzar información y detectar datasets generados automáticamente o sintéticos; Luciana aclara que eso todavía está en discusión C1P2 15:19, C1P2 15:54.
- **Los modelos de lenguaje dejaron de documentar sus datos.** Hasta GPT-2 se sabía con qué datos se entrenaban los modelos (toda Wikipedia, fragmentos de Common Crawl, una base grande de subtítulos de películas y sus traducciones). Luciana dice que eso cambió cuando se publicó GPT-3 "en el 2019" (**para verificar** el año). Las creadoras de la metodología de data statements contaron en un libro, linkeado en las slides, que estuvieron en contacto con OpenAI cuando se lanzó ChatGPT para documentar sus datos así, y "no hubo quórum" C1P2 48:09, C1P2 48:45, C1P2 49:19, C1P2 49:51.
- **Por qué los modelos comerciales esconden los logits.** Cuanto más acceso hay a la distribución de probabilidad de los tokens, más ingeniería inversa se puede hacer para extraer datos de entrenamiento y entrenar otros modelos (destilación de conocimiento). Las empresas dicen que eso es robarles datos, y se dice que DeepSeek lo hizo (la transcripción dice "Dipsic"; **para verificar**) C1P2 49:51, C1P2 50:25, C1P2 51:01.

### Tensiones entre valores
- No es una panacea ni una ciencia exacta 2020-EPCD.3 5:04.
- **Transparencia contra privacidad:** documentar todo lo posible sin exponer información de personas particulares 2020-EPCD.3 5:38.
- **Completitud contra brevedad:** un documento completo es largo y se repite en cada versión del dataset, por eso además se pide un resumen corto 2020-EPCD.3 6:12, 2020-EPCD.3 6:45.
- En el curso se escribe para un dataset que ya existe, pero la metodología propone hacerlo **antes** de recolectar 2020-EPCD.3 5:38, 2020-EPCD.3 6:12.

### Pasos del práctico (versión 2026)
1. Estar en el canal de Slack de la materia ("ética práctica para ciencia de datos") C1P2 52:06.
2. Anotarte en la planilla del aula virtual para armar grupos de **tres o cuatro personas**, con nombre, apellido y DNI; las docentes completan después el experto, el dataset y el link al documento C1P2 52:42, C1P2 53:15, C1P2 53:50.
3. Conseguir un **experto del dataset**: alguien que lo conozca lo suficiente para contestar las preguntas. Puede ser el mentor o alguien del grupo, pero conviene que no sean todos de la misma mentoría, para sumar una mirada fresca. "Experto" no es jerárquico: quiere decir que conocés algo. También vale un dataset que no sea de la mentoría, como uno publicado por alguien del grupo C1P2 54:23, C1P2 54:58, C1P2 55:31, C1P2 56:04, C1P2 56:37, C1P2 1:07:21, C1P2 1:07:55, C1P2 1:08:28, C1P2 1:09:00.
4. Usar la plantilla linkeada en la página de la materia (sección práctico), en el aula virtual y en Slack C1P2 57:43, C1P2 58:17.
5. Ser honesto y reflexivo: "no hay respuestas correctas o incorrectas", es una práctica educativa y nada de lo que escribas es legalmente vinculante C1P2 57:09.
6. Pedirle al experto que lea el borrador y sugiera cambios C1P2 1:00:31.
7. Escribir el resumen **al final**, con lo más importante de tus respuestas C1P2 1:01:03, C1P2 1:01:36.
8. Entregar antes de la fecha: Luciana corrige la slide y dice "la fecha es el 1 de octubre" (**para verificar** en el aula virtual) C1P2 1:01:36.

### Pasos del práctico (versión 2020, para comparar)
1. Unirte al canal de la materia y armar un grupo de dos o tres personas (preferentemente tres) 2020-EPCD.3 7:16.
2. Elegir, de las listas que dan, a una persona de otra mentoría que funciona como "experta del dataset" 2020-EPCD.3 7:16.
3. Coordinar una reunión de una hora y media entre las cuatro personas, hacer una copia del documento guía y usarlo para entrevistar a la experta 2020-EPCD.3 7:16, 2020-EPCD.3 7:51.
4. Completar las secciones con una **entrevista semiestructurada**: podés leer todas las preguntas de una sección juntas y responder en un párrafo; la superposición entre preguntas es parte de la metodología, para que no se escape información importante 2020-EPCD.3 9:37, 2020-EPCD.3 10:11, 2020-EPCD.3 10:44.
5. Compartir el documento con la experta para que lo lea y sugiera correcciones 2020-EPCD.3 16:26, 2020-EPCD.3 16:59.
6. Escribir al final el **resumen de 50 a 70 palabras**, resaltando lo más importante 2020-EPCD.3 16:59.
7. Entregar el documento revisado; en 2020 la fecha límite era el 7 de diciembre 2020-EPCD.3 17:31.

### Lo que suele traer dudas (ejemplos de años anteriores)
- **Fuente:** poné el link concreto al origen del dataset, sobre todo si es abierto C1P2 58:51.
- **Licencia:** muchos datasets no tienen una licencia explícita; no la inventes, registrá la realidad C1P2 59:25.
- **Quién lo creó y por qué**, quién financió su creación y en qué se diferencia de datasets parecidos C1P2 1:02:10.
- **Qué contiene**, de forma cualitativa y con ejemplos concretos de puntos de datos C1P2 1:02:43.
- **Qué no contiene.** Laura insiste: "uno de los problemas más grandes del sesgo es ver lo que no se ve", y la invisibilización es uno de los grandes problemas de las comunidades minorizadas. Muchas veces solo se ve comparando con dónde sí está. "Sean como el zorro" del Principito: lo esencial es invisible a los ojos C1P2 1:02:43, C1P2 1:03:18, C1P2 1:03:54, C1P2 1:04:27, C1P2 1:05:04, C1P2 1:05:39.
- **Cómo se eligió la muestra y cuándo se juntaron los datos.** Un dataset refleja el momento en que se recolectó aunque no tenga fechas explícitas, y solo está actualizado hasta ahí C1P2 1:06:12, C1P2 1:06:46.
- **Por qué importa la fecha.** En una encuesta informal, alguien dijo que las preguntas de temporalidad le parecían las menos interesantes. Luciana responde que el sesgo emergente también puede venir del tiempo: con la pandemia apareció mucha terminología nueva que los modelos de lenguaje no podían incorporar C1P2 1:09:35, C1P2 1:10:07, C1P2 1:10:39, C1P2 1:11:12.

### Secciones del documento
| Sección | Qué pide (ejemplos del video) |
|---|---|
| Metadatos | Nombre del dataset (si no tiene, lo inventa la experta), autores (el grupo), otros contribuyentes (por ejemplo, el mentor, opcional), versión y fecha aproximada, licencia ("no hay una licencia explicitada" si no la tiene). Se completa al final 2020-EPCD.3 8:24, 2020-EPCD.3 9:00, 2020-EPCD.3 9:37 |
| 1. Motivación | Con qué propósito se creó, si había una tarea en mente, datasets parecidos y diferencias; quién lo creó (todos los actores, incluida una empresa contratada para recolectar); quién lo financió, entendido también como quién puso trabajo 2020-EPCD.3 11:15, 2020-EPCD.3 11:51 |
| 2. Composición | Tipos de instancias (por ejemplo, estudiantes, docentes e interacciones), cantidad de cada tipo, en qué consiste cada instancia y ejemplos legibles por personas (si son datos de sensores, una descripción o un gráfico) 2020-EPCD.3 12:25, 2020-EPCD.3 13:00 |
| 3. Recopilación | Mecanismos (software, apps, formularios), personas que participaron y cómo se les compensó, período de recolección con fechas aproximadas; si la experta no sabe, se dice 2020-EPCD.3 13:34, 2020-EPCD.3 14:08 |
| 4. Datos de personas | Solo si el dataset tiene información de personas: datos demográficos (edad, sexo, provincia en lugar de domicilio exacto), privacidad y consentimiento informado 2020-EPCD.3 14:41, 2020-EPCD.3 15:18 |
| 5. Usos | Para qué tareas se puede usar, para qué otras podría usarse y, en la pregunta 5.5, para qué **no** debería usarse, una reflexión especulativa pero importante 2020-EPCD.3 15:18, 2020-EPCD.3 15:52 |

### Cómo se conecta con la clase de 2026
- Luciana dice que el práctico tiene una metodología moderna pero se apoya en los conceptos de la ley: datos sensibles, titulares y obligaciones de quienes tratan datos C1P1 23:34.
- Hay que reflejar para qué se recolectaron originalmente los datos y para qué se podrían usar o no C1P1 29:07, y qué datos sensibles contiene el dataset de la mentoría C1P1 33:01.
- Laura agrega las preguntas de sesgo histórico y de representatividad de la población como preguntas del data statement C2P1 33:30, C2P1 34:02.

<details>
<summary>Preguntas de repaso del módulo 11 (con respuestas)</summary>

1. **¿Qué definición de sesgo usa el data statement?** La de Friedman y Nissenbaum (1996, según el video): discriminación sistemática e injusta contra ciertos individuos o grupos en favor de otros.
2. **¿Qué tipo de sesgo no cubre el data statement y por qué?** El técnico, porque está en las decisiones de implementación del software y no en los datos.
3. **¿Cómo ayuda contra el sesgo emergente?** Al describir la muestra y a quienes recolectaron, permite ver cuándo el sistema se va a usar en otro contexto y planificar otra recolección.
4. **¿Qué dos tensiones de valores menciona el video?** Transparencia contra privacidad, y completitud contra brevedad.
5. **¿Quién responde las preguntas del documento?** La persona experta del dataset, entrevistada por el grupo.
6. **¿Cuánto mide el resumen?** Entre 50 y 70 palabras.
7. **¿Cuántas personas por grupo en 2026?** Tres o cuatro, según la clase; confirmalo en el aula virtual C1P2 53:15.
8. **¿Qué es el sesgo de automatización y qué lo reduce?** La tendencia a confiar de más en lo que recomienda el sistema; hay más desacuerdo cuando la persona decide primero y después ve la respuesta automática C1P2 44:39, C1P2 45:12.
9. **¿Por qué importa saber cuándo se recolectaron los datos?** Porque el sesgo emergente también puede venir del paso del tiempo, como con la terminología nueva de la pandemia C1P2 1:11:12.
10. **¿Por qué es difícil la pregunta de qué no contiene el dataset?** Porque lo invisible muchas veces solo se ve comparando con dónde sí está C1P2 1:04:27.

</details>

---

## 12. Barreras al cambio, derechos y consensos sociales (videos de 2020 sin transcripción)
**Dónde:** 2020-Barreras 0:00, 2020-Barreras 3:02, 2020-Barreras 9:45, 2020-Barreras 15:34, 2020-Caja 0:00

> Estos dos videos de 2020 son de Laura Alonso Alemany (lo dice la descripción de cada uno). la grabación no ofrece subtítulos para ninguno de los dos, así que **no tienen transcripción** y lo que sigue sale solo del título, la descripción y los capítulos. No hay contenido inventado: donde no se sabe qué dice el video, está dicho.

### "Barreras a los cambios para soluciones más éticas y consensos sociales sobre qué es bueno" (18:05)
Los capítulos del video son:
| Capítulo | Empieza en | Qué se puede decir sin transcripción |
|---|---|---|
| Ética Práctica para Ciencia de Datos | 2020-Barreras 0:00 | Introducción |
| Cómo nos afecta: la IA es innovadora en atentar contra derechos fundamentales; discriminación (invisibilización, estereotipos); limita libertades fundamentales: expresión | 2020-Barreras 3:02 | Por el título, conecta la IA con derechos fundamentales: la discriminación por invisibilización y por estereotipos (que en la clase 2 aparecen como daños de representación) y los límites a la libertad de expresión |
| Tres sencillos trucos para mantener el status quo con inteligencia artificial | 2020-Barreras 9:45 | El título anuncia tres "trucos", pero sin transcripción no se sabe cuáles son |
| Declaración de Montreal para un uso responsable de la IA | 2020-Barreras 15:34 | Presenta la Declaración de Montreal como ejemplo de consenso social sobre qué es bueno; el contenido de la declaración no está en la transcripción |

**Dónde encaja.** En la clase 2, Laura insiste en que las decisiones sobre qué error es más grave y qué variable proteger son consensos sociales, y en que el argumento "las cosas son así" es el del grupo dominante para justificar su posición C2P1 18:10, C2P1 1:17:34. Este video, por su título, trata justamente de esas barreras y de esos consensos.

### "Ejercicios de pensamiento de la Caja de Herramientas Humanísticas" (8:32)
- Según la descripción, son ejercicios "extraídos de la Caja de Herramientas Humanísticas del Grupo Gift", con links a https://grupo.gift/ y a un PDF en guia.ai, y es un "video de precalentamiento" para el curso 2020-Caja 0:00.
- No hay transcripción ni capítulos, así que no se sabe qué ejercicios presenta.
- **Dónde encaja.** En la clase 2, Laura hace "ejercicios de pensamiento sobre daños" (el sistema de selección de personal y el etiquetado de imágenes) para empezar a formalizar daños C2P1 1:24:25, C2P1 1:27:06. Probablemente este video es el antecedente de ese formato (inferido, sin transcripción).

<details>
<summary>Preguntas de repaso del módulo 12 (con respuestas)</summary>

1. **¿Por qué este módulo es tan corto?** Porque los dos videos de 2020 no tienen subtítulos en la grabación; solo se pueden usar su título, su descripción y sus capítulos.
2. **¿Qué ejemplo de consenso social sobre IA aparece en los capítulos del video de barreras?** La Declaración de Montreal para un uso responsable de la IA 2020-Barreras 15:34.
3. **¿Con qué parte de la clase 2 conecta?** Con la idea de que qué error es más grave y qué variable proteger son consensos sociales, y con los ejercicios de pensamiento sobre daños C2P1 18:10, C2P1 1:24:25.

</details>

---

## Glosario

### Términos
| Término | Qué quiere decir en esta materia |
|---|---|
| Ética | Conjunto de principios consensuados en una comunidad que dirigen y valoran como bueno o malo el comportamiento, de personas o de sistemas 2020-EPCD.1 0:37 |
| Moral | Los mismos principios, pero de una persona consigo misma 2020-EPCD.1 1:12 |
| Problema ético | Situación en conflicto, o potencial conflicto, con algún principio ético 2020-EPCD.1 1:12 |
| Autoetnografía (o etnografía personal) | Pensar en los daños que vos mismo sufriste para descubrir grupos y escenarios de daño que de otro modo no se te ocurren C1P2 30:27, C2P1 0:02, C2P1 29:28 |
| Incidente | Caso reportado en que un sistema de IA produjo un daño; la materia los compara con los accidentes de aviación, que se investigan para que no se repitan C1P1 5:41 |
| Dato sensible | Dato personal que revela, por ejemplo, origen racial o étnico, opiniones políticas, religión, salud o vida sexual (ver módulo 2) |
| Data statement | Documentación clara de un dataset (de dónde viene, a quién representa, qué sesgos puede tener) que ayuda a mitigar sesgos; es el práctico de la materia 2020-EPCD.3 1:06 |
| Diseño basado en valores | Value sensitive design, la teoría en la que se apoyan los data statements 2020-EPCD.3 1:43 |
| Sesgo (definición del práctico) | "Una discriminación sistemática e injusta contra ciertos individuos o grupos en favor de otros", según Friedman y Nissenbaum (ver módulo 11) 2020-EPCD.3 1:43 |
| Sesgo (definición operativa de la notebook) | Distribución no homogénea del error a través de diferentes grupos, de una forma que se considera dañina C2P2 1:13 |
| Sesgo social | Los errores de un modelo no caen al azar sino que dañan sistemáticamente a ciertos individuos o grupos C1P2 42:54 |
| Sesgo emergente | Aparece cuando un modelo entrenado en un contexto se usa en otro (otro grupo, otra cultura u otro momento) C1P2 43:30, C1P2 1:10:39 |
| Sesgo preexistente | Sesgo de origen social o histórico que ya está en los datos, como las profesiones asociadas a un género C1P2 44:07, 2020-EPCD.3 2:16 |
| Sesgo técnico | Sesgo que viene de decisiones de implementación supuestamente neutrales, como un orden alfabético 2020-EPCD.3 2:51 |
| Sesgo de automatización | Tendencia de las personas a confiar de más en las recomendaciones de un sistema C1P2 44:39 |
| Uso dual | Posibilidad de usar un dataset para algo distinto de lo que se planteó, con posible impacto negativo C1P2 45:52 |
| Experto del dataset | Persona que conoce el dataset lo suficiente para contestar las preguntas del data statement; no es un término jerárquico C1P2 54:23, C1P2 1:07:21 |
| Destilación de conocimiento | Usar las salidas o los logits de un modelo para extraer información de su entrenamiento y entrenar otro C1P2 50:25 |
| Amplificación | Cuando el modelo exagera la proporción de la clase mayoritaria respecto de la que hay en los datos C2P1 45:27 |
| Variable protegida | Atributo (raza, género, edad, discapacidad) que define los grupos que se comparan; en general sale de un consenso social C2P1 27:42 |
| Escenario de daño | Descripción formal de qué grupos pueden ser dañados, en qué consiste el daño y qué tipo de error lo produce (ver módulo 7) |
| Daño de representación | Daño que viene de cómo un sistema muestra o etiqueta a un grupo, por ejemplo con estereotipos (ver módulo 7) |
| Matriz de confusión | Tabla de verdaderos y falsos positivos y negativos; para equidad se arma una por grupo C2P2 24:42 |
| Macro average | Promedio de una métrica por clase en el que cada clase vale lo mismo, sin importar su tamaño C2P1 1:04:42 |
| Métrica proxy | Lo que medís cuando no podés medir lo que te importa (tiempo de reproducción en lugar de engagement) C2P1 1:09:09 |
| Tasa de falsos positivos | De todos los negativos reales, la proporción que el sistema etiquetó como positivos C2P2 45:55 |
| Equal opportunity | Que los miembros de cada grupo que merecen la clase positiva tengan la misma probabilidad de recibirla C2P2 48:12 |
| Equalized odds | Igualdad entre grupos de los aciertos en la clase positiva y en la negativa a la vez C2P2 50:28 |
| Predictive parity | Igualdad entre grupos de la proporción de positivos predichos que son correctos (ver módulo 8) C2P2 49:18 |
| Paridad demográfica (statistical parity) | Que cada grupo reciba la clase positiva en la misma proporción, sin importar si la merece C2P2 49:56 |
| Umbral de tolerancia | Valor de una métrica de equidad por encima del cual ningún modelo se acepta C2P2 51:38 |
| Exploración sistemática | Auditar un sistema sin definición de error comparando grupos con muchas entradas y reportando porcentajes, no casos sueltos C2P2 1:11:39 |
| SHAP | Método que estima cuánto contribuye cada característica a una decisión, de forma agnóstica al modelo C2P2 53:21 |
| What-If | Herramienta para probar contrafácticos, como cambiar o sacar una variable y ver cómo cambia la predicción C2P2 53:54 |
| Marca de agua (watermarking) | Señal estadística que una empresa mete en lo que genera su modelo para poder detectarlo después con su propio detector (ver módulo 3) |
| Datos sintéticos | Datos generados por modelos; sirven para probar pipelines, pero no reemplazan a los reales (ver módulo 3) |
| Soft law | Declaraciones y principios no obligatorios, que no son regulación C2P2 1:37:13 |

### Nombres que la transcripción deforma
| Como aparece | Qué es probablemente |
|---|---|
| CONISET | CONICET C1P1 0:02 |
| Lau, Laura Alonso Alemán | Laura Alonso Alemany (así figura en las descripciones de 2020) 2020-EPCD.1 0:02 |
| la Caro | Coordinación de la materia; el apellido no se dice C1P1 4:32 |
| declaración o convención de San José, "Interamericana" | Pacto de San José de Costa Rica (Convención Americana sobre Derechos Humanos) C1P1 7:57, C2P2 1:30:58 |
| Association of Computing Mainery | ACM (Association for Computing Machinery) |
| IUAI Act | Ley europea de IA (EU AI Act) |
| Clot, Cloud, Antropic, Entropic | Claude, Anthropic |
| SINT id | SynthID |
| Detect GPT, TG GPT | DetectGPT |
| A a AI | AAAI |
| crowdwers | Crowdworkers |
| Mozila | Mozilla; el nombre del proyecto no se dice |
| generado por gama | Dudoso |
| convenio 108 Plus | Convenio 108+ |
| la FIP o rentas de Países Bajos | Dudoso; la agencia que administraba los subsidios |
| político, outlet | Dudoso; un medio periodístico |
| centro Pulitzer | Así se dice en clase |
| piretal | Apiretal |
| Mónica | La ministra española; el apellido no se dice |
| Spotify al Pata | Dudoso |
| AI GDAR, AI Gator | Dudoso; nombre del proyecto de clasificación de orientación sexual por la cara C1P2 16:27 |
| Dipsic | DeepSeek C1P2 51:01 |
| common craw | Common Crawl C1P2 48:09 |
| CHPT | ChatGPT C1P2 49:51 |
| cénodo | Zenodo C1P2 1:06:46 |
| Alonso Church | Alonzo Church C1P2 1:13:28 |
| el mit | Probablemente Google Meet, la plataforma de la clase; dudoso C1P2 6:50 |
| lo del APA | Dudoso; un accidente aéreo que se menciona como ejemplo C1P2 2:51 |
| consejo de expertos de las Naciones Unidas | Sin nombre exacto en la clase; dudoso C1P2 9:04 |
| Pro Pública, Propública, Probl | ProPublica |
| Compas, compass | COMPAS |
| Men also like shopping | Título de un artículo tal como lo lee Laura |
| Attention is All Unit | Attention Is All You Need |
| lagranchianas, la granana, lagrangianas | Lagrangianos (restricciones con multiplicadores de Lagrange) |
| psychit learn | scikit-learn |
| Ecolizs, equalized ods | Equalized odds |
| con l'opportunity | Equal opportunity |
| Holistic | Dudoso; un framework de fairness |
| AETAS, ACTAS, Equira | Dudoso; un framework europeo de fairness (podría ser Aequitas, sin confirmar) |
| KIDA | Dudoso; el nombre de la notebook |
| Shap | SHAP |
| WTIF, Watif | What-If |
| Edia, Edy, Edas | Dudoso; herramienta de exploración de sesgos cuyo GitHub está en la página de la materia |
| esbio | Dudoso; ONG española de transparencia |
| Access | Dudoso; organización que publicó un informe en 2024 |
| Jan Lecun | Yann LeCun |
| despixelizador | Reconstructor de alta resolución; el origen es inconsistente entre fuentes (Duke en 2020-Grave, Meta en C2P2); **para verificar** |
| Silvester Stalón | Sylvester Stallone, ejemplo de Laura sobre daños de representación C2P1 1:20:24 |
| Escola, Shinobili, León James | Scola, Ginóbili, LeBron James, en el ejemplo de básquet C2P2 31:54 |
| Udesa | Universidad de San Andrés (UdeSA), por su concurso anual de visualización de datos; dudoso C2P2 27:28 |
| friedmann y nissan brawn | Probablemente Friedman y Nissenbaum; dudoso 2020-EPCD.3 1:43 |
| tomás balmaseda | Así aparece; dudoso. En clase, Laura dice que el caso de la Smart TV lo "comenta Tomás" 2020-Grave 18:30, C1P1 15:16 |
| diana, universidad del litoral | Dudoso; un grupo de la Universidad del Litoral que se menciona al comienzo 2020-Grave 0:05 |
| caso martelly | Dudoso; el caso de la familia y el televisor con reconocimiento de voz 2020-Grave 18:30 |
| universidad de sauce, universidad de salsa en california | Una universidad de California con un instituto de tecnologías creativas; dudoso cuál 2020-EPCD.1 3:27 |
| chapapote de microsoft | Un chatbot de Microsoft que hubo que apagar; el nombre está deformado, dudoso 2020-EPCD.1 9:04 |
| financiado por "dar" | Dudoso; una agencia de defensa 2020-EPCD.1 10:47 |
| humanas virtuales "y grace" | Dudoso; nombres de dos humanas virtuales 2020-EPCD.1 3:27 |
| emirates code | Dudoso; autora o charla original en la que se basa el video 2020-EPCD.1 15:53 |
| Grupo Gift | Así figura en la descripción del video 2020-Caja |
| ley 10618 Córdoba | Así se dice en clase |
