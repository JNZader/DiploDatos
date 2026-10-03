# Apunte de estudio: Análisis y Visualización de Datos (Diplodatos, FAMAF UNC, Georgina Flesia y Karim Nemer)

**Curso:** Análisis y Visualización de Datos, la primera de las cinco materias obligatorias de la Diplomatura en Ciencia de Datos, Aprendizaje Automático y sus Aplicaciones de FAMAF (UNC), cohorte 2026. La sigue Exploración y Curación de Datos · Docentes: Georgina Flesia (la teoría de probabilidad y estadística, con filminas) y Karim Nemer (las notebooks de Colab) · Coordinación: Carolina Chavero, con las facilitadoras Analía y Belén · Formato: cuatro clases sincrónicas por Meet, grabadas en 8 videos no listados del canal FAMAF UNC: viernes 27 de marzo a la tarde, sábado 28 de marzo a la mañana, y el fin de semana siguiente de clases (viernes 10 y sábado 11 de abril de 2026, fechas deducidas, **para verificar**). Se suman cinco videos de apoyo cortos que grabó Milagro Teruel en 2021 para la misma materia y que la cátedra deja como material opcional en el aula virtual.
**De qué va:** es la materia de estadística de la diplomatura, contada sobre un único dataset real y sucio: la encuesta de sueldos de Sysarmy 2026.1 (4939 respuestas). Arranca por qué es la ciencia de datos y cómo leer el dataset en Colab, y después recorre variables aleatorias y tipos de datos, gráficos de una variable, probabilidad (Laplace, condicional, independencia, Bayes), estadística descriptiva y outliers, distribuciones, varias variables (covarianza, correlación, causalidad), muestreo, ley de los grandes números y teorema central del límite, estimación puntual e intervalos de confianza, tests de hipótesis (z, t, Welch, ANOVA, chi cuadrado y no paramétricos) y, al final, visualización para comunicar. La pregunta que atraviesa todo es "¿cuánto cobra alguien que programa?" y, en las últimas clases, "¿las mujeres cobran menos que los varones?". Se aprueba con un trabajo práctico en grupo dividido en dos entregables, el segundo con una visualización creativa.

> Nota: este apunte sale de los subtítulos automáticos en español de los 13 videos (los 13 tenían subtítulos de la grabación; el de C3P1 recién se pudo bajar al cuarto intento por errores de "demasiadas solicitudes"). También usé el repositorio público de la materia, `DiploDatos/AnalisisyVisualizacion`, con las seis notebooks y los CSV, y corrí el código contra esos datos. Muchos nombres vienen deformados en la transcripción (ver el glosario al final). Todo lo que figura acá es lo que se dice en clase o lo que hacen las notebooks. Cuando lo que se dijo está mal o es impreciso, lo marco como **Corrección**. Las cifras, fechas y afirmaciones que no pude chequear van como **dudoso** o **para verificar**. Lo que dice "verificado en el box" lo comprobé corriendo código sobre el CSV 2026 del repo (los scripts están en la guía de implementación).

**Cómo leer los links:** cada link dice el video y el minuto. "C2P1 1:23:45" es la clase 2, parte 1, en la hora 1, minuto 23, segundo 45. "V04 2:12" es el video de apoyo 04 en el minuto 2:12.

## Los 13 videos

| # | Id | Video | Contenido | Duración | Link |
|---|---|---|---|---|---|
| 1 | — | C1P1: Clase 1, parte 1 (27/03/2026 17:31) | Bienvenida, equipo, cursada, política de IA, qué es la ciencia de datos, ciclo de un proyecto, sesgo, notebook 00 (Colab, lectura y renombrado del dataset) | 1:59:25 |  |
| 2 | — | C1P2: Clase 1, parte 2 ("Recording 2") | El problema de los sueldos, población y muestra, variable aleatoria, tipos de variables, imputación, notebook 01 parte A (histogramas, conteos, edades, género) | 1:25:56 |  |
| 3 | — | C2P1: Clase 2, parte 1 (28/03/2026 09:29) | Grupos y entregables, gráficos incorrectos, axiomas de probabilidad, Laplace, condicional, independencia, Bayes, sesgos de una encuesta voluntaria, notebook 01 parte B | 1:55:26 |  |
| 4 | — | C2P2: Clase 2, parte 2 ("Recording 2") | Estadística descriptiva, robustez, cuartiles y boxplot, distribuciones (binomial, uniforme, normal, exponencial, chi cuadrado), estandarizar, notebook 02, adelanto de varias variables y correlación | 1:48:27 |  |
| 5 | — | C3P1: Clase 3.1 (10/04/2026, para verificar) | Distribución conjunta, marginales, covarianza, correlación, normal bivariada, causalidad, notebook 03 Varias Variables, muestreo, ley de los grandes números y teorema central del límite | 2:05:51 |  |
| 6 | — | C3P2: Clase 3.2 | Notebook 04 (TCL simulado), estimadores y sus propiedades, intervalos de confianza z, t, Welch y para la varianza, IC del salario y de la brecha de género | 1:40:33 |  |
| 7 | — | C4P1: Clase 4 (11/04/2026, para verificar) | Tests de hipótesis: H0 y H1, Neyman Pearson, errores tipo I y II, p valor, tests z, t, de proporciones, de varianza, chi cuadrado, no paramétricos | 2:02:00 |  |
| 8 | — | C4P2: Clase 4-2 | Notebook 05 Test de Hipótesis (t de una y dos muestras, ANOVA, chi cuadrado), leer la documentación, visualización para comunicar y sus trampas, entregable 2 | 1:58:52 |  |
| 9 | — | V01: "01. Ciencia de datos y su proceso" (Milagro Teruel, 2021) | Análisis de datos, machine learning y ciencia de datos; proceso iterativo | 7:35 |  |
| 10 | — | V02: "02. Introducción y objetivos de AyVD" (2021) | Objetivos de la materia | 3:06 |  |
| 11 | — | V03: "03. Cómo leer el dataset" (2021) | Notebooks, Colab, `files.upload`, `read_csv`, renombrar columnas | 8:18 |  |
| 12 | — | V04: "04. Percentiles y detección de outliers" (2021) | Percentiles, recorte por percentil y por criterio, boxplot y boxenplot | 5:45 |  |
| 13 | — | V05: "05. Gráficos simples" (2021) | Tablas, barras, líneas, puntos, `pd.cut`, color y tamaño como variables | 18:06 |  |

Duración total: 15:39:20 (14:56:30 de clases y 42:50 de videos de apoyo).

**Cómo se determinó el orden.** Los títulos de las clases 1 y 2 traen la fecha y la hora de grabación (27/03 17:31 y 28/03 09:29), y la segunda parte de cada una se llama "Recording 2". Las clases 3 y 4 no traen fecha; los títulos dicen "Clase 3.1", "Clase 3.2", "Clase 4" y "Clase 4-2", y se subieron el 13 y el 14 de abril. El contenido encadena sin huecos: C1P1 corta en el recreo después del notebook 00 C1P1 1:58:43 y C1P2 retoma con la teoría C1P2 0:03; C1P2 cierra con "mañana: datos y modelos, varias variables" C1P2 1:24:27; C2P1 abre con el aula virtual y la clase 2 C2P1 0:07 y corta en el recreo C2P1 1:55:14; C2P2 cierra con "nos vemos el otro fin de semana" C2P2 1:48:25. C3P1 arranca con "el pedacito de transparencias que nos faltó de la clase pasada" C3P1 0:34 y corta "son las 8:10, volvemos 8:25" C3P1 2:05:18, o sea un viernes a la noche; C3P2 es la segunda parte (notebook 04). En C4P1 un alumno habla de la clase "de ayer" y Georgina anuncia SQL con Ariel "la semana que viene" C4P1 0:06; C4P2 sigue con el notebook 05 y cierra la materia presentando la siguiente, Exploración y Curación C4P2 1:58:10. Las fechas 10 y 11 de abril salen de que el primer entregable se abría el 10/04 C2P1 2:22 y de que el segundo se habilita desde el 17/04 C4P2 1:52:27; **para verificar** con el cronograma del aula virtual.

**Dónde encajan los videos de apoyo.** Georgina los presenta como "los videos opcionales del aula virtual, de Milagro Teruel" C1P1 26:18, C2P1 0:07. Son de 2021: los montos en pesos que dan ya no sirven, pero los conceptos sí. V01 y V02 acompañan el módulo 1, V03 el 2, V04 el 6 y V05 los módulos 4 y 13.

## Mapa de módulos y videos

| Módulo | Dónde se ve |
|---|---|
| 0. La materia: equipo, cursada, entregables y uso de IA | C1P1 (inicio), C2P1 (inicio), C4P2 (final) |
| 1. Qué es la ciencia de datos y cómo es un proyecto | V01, V02, C1P1 |
| 2. Colab y lectura del dataset (notebook 00) | C1P1 (final), V03 |
| 3. Población, muestra, variables aleatorias y tipos de variables | C1P2, C2P1, C3P1 (muestreo) |
| 4. Gráficos de una variable (notebook 01, parte A) | C1P2, C2P1, V05 |
| 5. Probabilidad: Laplace, condicional, independencia y Bayes (notebook 01, parte B) | C2P1 |
| 6. Estadística descriptiva, percentiles y outliers (notebook 02) | C2P2, V04, C3P1 |
| 7. Distribuciones y estandarización | C2P2 |
| 8. Varias variables: conjunta, covarianza, correlación y causalidad (notebook 03) | C2P2 (final), C3P1 |
| 9. Muestreo, ley de los grandes números y teorema central del límite | C3P1 (final), C3P2 (inicio) |
| 10. Estimación puntual e intervalos de confianza (notebook 04) | C3P2 |
| 11. Tests de hipótesis: la teoría | C4P1 |
| 12. Tests de hipótesis en Python (notebook 05) | C4P2 |
| 13. Visualización para comunicar | V05, C4P1, C4P2 |
| 14. Los entregables | C1P1, C2P1, C4P2 |

---

## 0. La materia: equipo, cursada, entregables y uso de IA
**Dónde:** C1P1 0:02, C1P1 4:03, C1P1 7:14, C1P1 12:14, C1P1 15:02, C1P1 17:17, C1P1 21:14, C1P1 26:18, C2P1 2:22, C2P1 7:15, C2P1 19:53, C4P2 1:48:37

### Conceptos clave
- **Quiénes.** Abre Carolina Chavero, coordinadora 2026, y da la bienvenida el decano de FAMAF, Pedro Pérez, egresado de la primera cohorte de la diplomatura C1P1 0:02. Hay 144 inscriptos. Las facilitadoras son Analía y Belén C1P1 4:03.
- **Georgina Flesia**: licenciada y doctora en matemática (estadística, modelos estocásticos para imágenes), posdoc en el departamento de estadística de Stanford con David Donoho, coordinadora de la diplomatura desde 2022. Vuelve a dar clases en Aprendizaje No Supervisado C1P1 7:14.
- **Karim Nemer**: ingeniero en sistemas (UTN), doctor en ingeniería con mención en electrónica, trabaja en IA y procesamiento de imágenes en un centro de investigación de la UTN Facultad Regional Córdoba (la transcripción dice "CPIE"; probablemente el CIII, **para verificar**) C1P1 12:14. Dice que lleva 28 años en IA C1P2 0:03. Da también Aprendizaje Supervisado.
- **Cursada.** Primera de cinco materias obligatorias; grupos de cuatro armados por coordinación, que se mantienen en las cinco; un profesor de seguimiento por grupo que corrige y orienta pero no da clase C1P1 4:03, C2P1 19:53. Clases virtuales sincrónicas que se suben a la grabación; 16 horas de clase C1P1 15:02. Mentorías desde julio, optativas desde agosto.
- **Evaluación.** Un trabajo práctico en grupo dividido en dos entregables: el primero sobre los temas del primer fin de semana y el segundo sobre los del segundo; hay que aprobar los dos C1P1 17:17. Cada integrante hace todo y después el grupo arma la mejor versión; todos con nombre en el encabezado; si sube uno, cuenta para todo el grupo C2P1 7:15, C2P1 13:50. Verificá que la notebook corra entera antes de entregar.
- **Fechas** (provisorias en clase): apertura del primer entregable el 10/04, cierre tentativo el 24/04, cuando empieza la materia siguiente C2P1 2:22. El segundo se habilita desde el 17/04 a las 0 horas C4P2 1:52:27. Todo práctico tiene que estar entregado al 1/9.
- **Política de IA.** No está prohibida; se penaliza el exceso. Anécdota: un entregable con la frase del chatbot "si querés que haga otra cosa, decime" pegada C1P1 21:14. Georgina usa Gemini dentro de Colab y Grok.
- **Materiales.** Aula virtual con filminas, notebooks y los videos de apoyo de Milagro Teruel; canal de Slack de la materia C1P1 26:18. Las notebooks están en el repositorio público `DiploDatos/AnalisisyVisualizacion`.
- **Horarios fijos** para todo el año; las grabaciones están para quien no puede asistir C4P2 1:48:37.

### Correcciones y matices
- **para verificar:** el centro de Karim. La transcripción dice "CPIE" y él lo describe como un centro de investigación en informática para la ingeniería de la UTN FRC, que coincide con el CIII C1P1 12:14.
- **para verificar:** las fechas de los entregables. Georgina dice que las fechas que se ven en el aula "van a cambiar" según el mapa de cierres que mande Carolina C4P2 1:52:27.

### Preguntas de repaso
1. ¿Cuántos entregables tiene la materia y qué temas cubre cada uno?
2. ¿Qué rol tiene el profesor de seguimiento?
3. ¿Qué se considera mal uso de la IA en un entregable?

---

## 1. Qué es la ciencia de datos y cómo es un proyecto
**Dónde:** V01 1:08, V01 2:12, V01 3:49, V01 6:08, V02 1:05, C1P1 31:20, C1P1 34:09, C1P1 47:12, C1P1 49:21, C1P1 52:46, C1P1 58:24, C1P1 1:02:51

### Conceptos clave
- **Análisis de datos, machine learning y ciencia de datos** (Milagro). El análisis responde preguntas concretas o valida hipótesis, guiado por la intuición del analista (por qué los clientes dejan una plataforma) V01 1:08. El machine learning construye modelos que predicen o describen sin programar reglas explícitas, optimizando una métrica que puede no coincidir con el problema real V01 2:12. La ciencia de datos engloba los dos y además el producto basado en datos V01 3:49.
- **Proceso iterativo**: necesidad de negocio, definirla formalmente con métricas de impacto, análisis de datos, características y modelo, producto y decisiones, y vuelta a empezar V01 6:08, C1P1 49:21. Si los datos no "contienen el concepto" que querés medir, no hay modelo que lo arregle ("mucho dato y pocas nueces").
- **Objetivos de la materia** (Milagro): elegir y aplicar herramientas estadísticas adecuadas, diseñar análisis sistemáticos, contextualizar resultados, comunicar según la audiencia e implementar todo en Python con pandas y notebooks V02 1:05.
- **La mirada de Georgina.** Recomienda "50 years of Data Science" de David Donoho C1P1 31:20. Con big data cambia el paradigma estadístico: promediar un millón y medio de datos ya es un problema computacional. El diagrama de Venn de Drew Conway: computación, matemática y estadística, y conocimiento del dominio; la "zona de peligro" es computación más dominio sin estadística, porque no se puede cuantificar el error C1P1 34:09.
- **Habilidades**: Python y SQL (SQL lo da Ariel en Exploración y Curación), limpieza, modelado, despliegue y visualización para comunicar C1P1 47:12.
- **Limpiar lleva la mayor parte del tiempo** (dice 60%) y el sesgo viene de los datos y de las personas, no del algoritmo: el ejemplo de las fotos de bananas y un chatbot médico que no entiende "vómito recurrente" C1P1 52:46. Sesgo estadístico = apuntar mal de forma sistemática C1P1 58:24.
- **Riesgos de modelar sin explorar**: no sabés qué supuestos cumple el modelo, no podés medir el error ni detectar cambios en los datos; errores típicos: no estandarizar, no tratar los NaN, clases desbalanceadas, usar los valores por defecto de una caja negra C1P1 1:02:51.

### Correcciones y matices
- **dudoso:** Georgina cita también un paper sobre la historia de la ciencia de datos "de 1963 a 2012" C1P1 31:20; no se entiende el autor en el audio.
- **Matiz:** la distinción "el ingeniero de datos sabe aprendizaje automático y el analista no" C1P1 1:01:41 no es la habitual: el ingeniero de datos suele ocuparse de la infraestructura y los pipelines, y quien modela es el científico de datos o el ingeniero de ML.
- **para verificar:** el "60% del tiempo limpiando" C1P1 52:46 y, más adelante, "casi el 25%" C3P1 1:24:49: son cifras de encuestas de la industria que varían mucho según la fuente.

### Preguntas de repaso
1. ¿Qué diferencia hay entre análisis de datos y machine learning según Milagro?
2. ¿Qué es la "zona de peligro" del diagrama de Conway y por qué importa en esta materia?
3. Nombrá tres errores típicos de modelar sin explorar los datos.

---

## 2. Colab y lectura del dataset (notebook 00)
**Dónde:** C1P1 1:14:12, C1P1 1:15:52, C1P1 1:21:27, C1P1 1:25:29, C1P1 1:33:03, C1P1 1:36:24, C1P1 1:41:04, C1P1 1:45:31, C1P1 1:49:59, C1P1 1:54:41, V03 0:01, V03 3:18, V03 4:57, V03 6:02

### Conceptos clave
- **Colab.** Abrí la notebook desde el link y hacé Archivo > Guardar una copia en Drive para no trabajar sobre el original C1P1 1:15:52. El entorno de ejecución (CPU, GPU, TPU) es gratis con límites; cerrá las sesiones que no uses. Si la copia falla por falta de espacio, usá la cuenta de la UNC (30 GB) C1P1 1:25:29. Colab es una máquina virtual en la nube y no ve tu disco local V03 0:01.
- **El dataset.** Encuesta de remuneración salarial de Sysarmy 2026.1, voluntaria, que se hace cada seis meses; más de 5000 respuestas, 4939 guardadas C1P1 1:21:27. Se descarga como CSV desde Google Sheets.
- **Subir el archivo**: `from google.colab import files; uploaded = files.upload()` y después `pd.read_csv(io.StringIO(uploaded[clave].decode("utf-8")))` C1P1 1:25:29, V03 3:18. Si subís dos veces, Colab guarda "archivo (1).csv" y la clave fija falla C1P1 1:41:04.
- **Filas basura arriba.** Las primeras filas del CSV son texto del formulario: el notebook usa `skiprows=range(8), header=1` C1P1 1:33:03.
- **Orden de ejecución.** El número de cada celda es el orden en que se ejecutó; ejecutar fuera de orden da `KeyError` o variables viejas. Entorno de ejecución > Reiniciar sesión y correr todo de nuevo C1P1 1:36:24.
- **Renombrar columnas.** Las columnas son preguntas larguísimas; el notebook arma un diccionario por categoría (`profile`, `work`, `tools`, `salary`, `company`) y una función `replace_columns` que genera nombres como `salary_monthly_BRUTO` o `profile_gender` C1P1 1:45:31. Sin espacios ni tildes, podés escribir `df.salary_monthly_BRUTO` V03 4:57.
- **Leer directo del repo**: `pd.read_csv(url)` con la URL raw de `sysarmy_survey_2026_processed.csv` en GitHub C1P1 1:49:59. Es lo que usan todas las notebooks siguientes. En 2021 Milagro lo hacía desde un servidor de la UNC V03 6:02.

### Correcciones y matices
- **Corrección:** en clase Karim duda sobre cuántas filas saltear ("hasta la siete", "ocho", "fila 10") C1P1 1:33:03. En el notebook queda `skiprows=range(8), header=1`: saltea las 8 primeras filas y toma como encabezado la segunda de las que quedan, porque hay una fila en blanco en el medio (verificado en el box con un archivo de juguete).
- **Corrección:** en la filmina algunos links apuntaban a la versión 2025 de las notebooks y el CSV daba HTTP 404; hay que cambiar 2025 por 2026 en la URL C1P1 1:54:41.
- **Matiz:** un alumno pregunta si crear un DataFrame nuevo en cada paso desperdicia memoria; sí, y la alternativa es encadenar métodos o reasignar C1P1 1:54:41, C4P2 46:11.

### Preguntas de repaso
1. ¿Por qué Colab necesita `files.upload()` o una URL para leer un CSV?
2. ¿Qué hacen `skiprows` y `header` en `read_csv`?
3. ¿Qué ventaja tiene renombrar las columnas con prefijos por categoría?

---

## 3. Población, muestra, variables aleatorias y tipos de variables
**Dónde:** C1P2 4:28, C1P2 6:09, C1P2 12:54, C1P2 15:14, C1P2 16:54, C1P2 20:46, C1P2 26:23, C1P2 27:31, C1P2 29:42, C1P2 39:36, C1P2 42:23, C2P1 1:01:35, C2P1 1:33:03, C2P1 1:35:51, C2P1 1:49:11, C2P1 1:51:24, C3P1 0:34, C3P1 1:41:05

### Conceptos clave
- **El problema.** "Si me dedico a programar, ¿cuánto puedo cobrar?": un sistema que, dadas las características de una persona, devuelva el sueldo más probable C1P2 4:28. En informática los sueldos son personales y las empresas no publican listas; por eso Sysarmy pregunta a la gente C1P2 6:09.
- **Dar una respuesta con su error** ("1 metro ± 2 cm") y distinguir exactitud de precisión C1P2 12:54.
- **A quién inferís.** Sin una muestra independiente e idénticamente distribuida (iid) de la población, no podés hablar de la población: una encuesta voluntaria solo habla de quienes contestaron, mayoría de Buenos Aires C1P2 16:54. Georgina propone llamar población a "quienes se enteraron de la encuesta" y muestra a "quienes contestaron" C2P1 1:49:11. Sesgos: autoselección y ruido (respuestas no fidedignas) C2P1 1:51:24.
- **Variable aleatoria**: una función X: Ω → ℝ que asigna un número a cada elemento ω de la población (o del conjunto de respuestas). Una realización es X(ω), por ejemplo un sueldo de 433.000 C1P2 20:46, C1P2 27:31.
- **Tipos**: numéricas continuas (sueldo) o discretas (conteos), categóricas (provincia) y ordinales (nivel de estudios, sueldo en rangos). No seas dogmático: el mismo sueldo en rangos pasa a ser ordinal y pierde información C1P2 27:31, C1P2 42:23. Codificar rojo, amarillo y azul como 0, 1 y 2 no los vuelve ordinales C1P2 39:36.
- **Inconsistencias y faltantes**: 12 horas diarias con sueldo 0, neto mayor que bruto. Opciones: tirar casos, no usar la variable o imputar (por ejemplo con el promedio de los k vecinos más parecidos), tema de la materia siguiente C1P2 29:42. Cuidado con códigos como −1 o 0 para "faltante", que contaminan los promedios.
- **Datos tabulares** = una "bolsa" de sujetos sin orden; las series de tiempo y las imágenes tienen información extra en el orden y se ven en optativas C3P1 0:34.
- **Tipos de muestreo** (clase 3): aleatorio simple (todos con la misma probabilidad), sistemático (arranque al azar y después cada k), estratificado (muestrear dentro de cada estrato, por ejemplo varones y mujeres) y por conglomerados C3P1 1:41:05. Los estudios observacionales (la gente decide si responde) son la mayoría en la práctica.

### Correcciones y matices
- **Corrección:** Georgina dice que el conglomerado "es el estratificado, pero geográfico" C3P1 1:44:55. Son diseños distintos: en el estratificado muestreás dentro de todos los estratos (garantizás que todos estén representados); en el muestreo por conglomerados sorteás algunos grupos enteros (barrios, empresas) y medís dentro de ellos. El ejemplo que ella misma da en C2P1 ("muestrear 50 de 500 empresas y censar dentro") es justamente por conglomerados C2P1 43:35.
- **dudoso:** "los estudios observacionales son el 90% de los estudios que hay" C3P1 1:46:02: no da fuente.
- **para verificar:** "alrededor de 60.000 programadores en Argentina" C2P1 1:33:03.
- **Matiz:** en C1P2 se habla de "4 millones, 40 a 50 veces la media" como sueldo absurdo C1P2 18:34: es el histograma de la encuesta 2023 que muestra la filmina, no la de 2026 (en 2026 la mediana del bruto es 3.268.000; verificado en el box).
- **Matiz:** Karim dice "tenemos 60 columnas" C1P2 47:01: el CSV procesado 2026 tiene 4939 filas y 60 columnas (verificado en el box).

### Preguntas de repaso
1. ¿Por qué con una encuesta voluntaria no podés inferir el sueldo de "los programadores argentinos"?
2. Definí variable aleatoria. ¿Qué es Ω en la encuesta de Sysarmy?
3. Clasificá: provincia, edad, nivel de estudios, sueldo en rangos, "cobra en dólares".
4. ¿En qué se diferencian el muestreo estratificado y el muestreo por conglomerados?

---

## 4. Gráficos de una variable (notebook 01, parte A)
**Dónde:** C1P2 45:13, C1P2 48:46, C1P2 49:19, C1P2 52:17, C1P2 55:16, C1P2 57:48, C1P2 1:00:40, C1P2 1:01:13, C1P2 1:05:19, C1P2 1:07:01, C1P2 1:10:23, C1P2 1:16:00, C1P2 1:23:53, C2P1 30:30, C2P1 32:11, C2P1 34:31, V05 0:33, V05 3:22, V05 8:22, V05 11:39

### Conceptos clave
- **Primer vistazo.** `salary_col = "salary_monthly_NETO"`, tipo `float64`. Máximo 653.388.190 y mínimo 1,6 pesos: datos imposibles de los dos lados C1P2 48:46, C1P2 49:19. El notebook corta en 40 millones (`df1`) y deja como ejercicio acotar también abajo.
- **`describe()`** de `df1`: 4709 valores, media 3.270.653, Q1 1.850.000, Q3 4.000.000, máximo 36 millones C1P2 52:17. La media es mayor que la mediana: distribución con asimetría a la derecha (cola larga de sueldos altos) C1P2 55:16.
- **Histogramas** con `displot` e `histplot`: color, bordes, `xlim`, cantidad de bins C1P2 57:48. Con la edad, más bins que valores enteros deja "huecos" (el "estegosaurio"); probá con menos bins o con `discrete=True` C1P2 1:07:01. Seis histogramas en una grilla de 2 × 3 para comparar bins y `stat` C1P2 1:10:23.
- **Categóricas**: `countplot` de provincias, horizontal y ordenado con `order=value_counts().index`; sin `order` las barras salen en orden de aparición C1P2 1:01:13. Las etiquetas largas se rotan.
- **Edad**: va de 16 a 999; se filtra a menos de 70 C1P2 1:05:19.
- **Género**: antes era texto libre y había respuestas en broma; ahora es un menú. Se agrupa en "Varón cis", "Mujer cis" y "Diversidades" con `replace` C1P2 1:16:00. "Cuatro veces más varones que mujeres" vale solo para quienes respondieron C1P2 1:18:13.
- **Ordinales**: el nivel de estudios se grafica con un `order` explícito (secundario, terciario, universitario, posgrados) C1P2 1:23:53.
- **Tipo computacional vs tipo de variable**: `int64` para la edad no dice si es continua o discreta; `object` (en pandas 3, `str`) para provincias C2P1 32:11.
- **Dos gráficos mal elegidos a propósito** en el notebook: un histograma de un booleano ("cobra en dólares"), cuyo eje con 0,2 y 0,4 no significa nada, y un gráfico de líneas del conteo por provincia, que inventa una continuidad entre categorías. Para categóricas, barras C2P1 34:31.
- **Milagro, gráficos simples** V05 0:33, V05 3:22, V05 8:22, V05 11:39: las tablas también son visualizaciones; `countplot` cuenta y `barplot` agrega con un `estimator` (media por defecto, puede ser mediana); el gráfico de líneas sirve para una x numérica continua y se vuelve errático donde hay pocos datos, y ahí conviene agrupar con `pd.cut`; el scatter dibuja un punto por fila y sufre de sobreploteo.

### Correcciones y matices
- **Corrección:** Karim explica `stat="frequency"` como "la frecuencia relativa, la proporción" y dice que "la suma de todas estas líneas me da uno" C1P2 57:48, C1P2 1:00:40. En seaborn, `frequency` es el conteo dividido por el ancho del bin; lo que suma 1 es `stat="probability"` (o `"proportion"`), y `density` integra 1 (suma de alturas por ancho). Verificado en el box con el neto y 200 bins: `count` suma 4709, `frequency` suma 0,026 (y alturas por ancho dan 4709), `probability` suma 1 y `density` por ancho da 1.
- **Corrección:** el `plt.savefig("filename.png")` del notebook está en una celda aparte y guarda una imagen en blanco, porque Colab ya mostró y cerró la figura. Lo confirma un alumno en clase C2P1 30:30. Llamalo en la misma celda que el gráfico o usá `fig.savefig(...)` (verificado en el box: la figura guardada así tiene 13.594 píxeles no blancos y la "otra celda" 0).
- **Corrección:** Karim dice que la mediana del neto es 2.786.000 C1P2 52:17; con el CSV del repo da 2.748.626 (verificado en el box). Diferencia menor, pero los números de la clase pueden venir de una versión anterior del archivo.
- **Corrección:** V05 usa `ci=None` para sacar las barras de error V05 5:04. Desde seaborn 0.12 es `errorbar=None`; `ci` está obsoleto.
- **Matiz:** al ordenar al revés nadie recuerda cómo C1P2 1:13:10: `value_counts(ascending=True)` o `.index[::-1]`.

### Preguntas de repaso
1. ¿Qué devuelven `stat="count"`, `"frequency"`, `"probability"` y `"density"` en `histplot`? ¿Cuál suma 1?
2. ¿Por qué el histograma de edades con 200 bins tiene huecos?
3. ¿Por qué un gráfico de líneas del conteo por provincia es incorrecto?
4. ¿Por qué el `savefig` del notebook guarda una imagen vacía?

---

## 5. Probabilidad: Laplace, condicional, independencia y Bayes (notebook 01, parte B)
**Dónde:** C2P1 37:15, C2P1 40:42, C2P1 53:10, C2P1 53:44, C2P1 56:30, C2P1 1:01:35, C2P1 1:07:50, C2P1 1:12:12, C2P1 1:15:34, C2P1 1:18:34, C2P1 1:19:40, C2P1 1:21:52, C2P1 1:24:39, C2P1 1:28:33

### Conceptos clave
- **Los conceptos tienen que estar en los datos.** Para responder "¿más experiencia, más sueldo?" la variable tiene que haberse preguntado bien C2P1 37:15. El ejemplo del taller de autos: querían avisar "le toca service" y la mitad de los campos estaban vacíos porque los técnicos no los llenaban C2P1 38:57. Pasos: hipótesis que el dataset pueda contener, variables, medición C2P1 40:42.
- **Estadística vs ciencia de datos**: la estadística diseña y controla el experimento; la ciencia de datos trabaja con lo ya recolectado y "estira" los supuestos C2P1 53:10.
- **Medida de probabilidad**: como una medida de longitud con masa total 1. Axiomas: P(Ω) = 1, P(∅) = 0 y aditividad para eventos disjuntos (también numerable) C2P1 53:44.
- **Laplace**: si los k resultados son equiprobables, P(A) = |A| / |Ω| (|A| es el cardinal) C2P1 56:30. En el notebook, Ω son las respuestas y P(A) es una proporción de filas.
- **Condicional**: P(A | B) = P(A ∩ B) / P(B), "me meto adentro de B" C2P1 1:07:50. Con A = "neto mayor o igual al promedio" y B = "más de 5 años de experiencia".
- **Independencia**: P(A | B) = P(A), o lo que es lo mismo P(A ∩ B) = P(A) P(B): B no agrega información sobre A C2P1 1:12:12. Con datos nunca da exacto; hace falta un test para decidir.
- **El cálculo del notebook** C2P1 1:19:40, C2P1 1:21:52: promedio 3.270.653; P(A) = 0,375 (no 0,5, porque la media queda a la derecha de la mediana); P(A | B) = 0,525. Conclusión: no son independientes. Verificado en el box: además P(A | no B) = 0,168, P(A ∩ B) = 0,305 contra P(A) P(B) = 0,218, y el test chi cuadrado de independencia da p ≈ 2 × 10⁻¹³⁷.
- **Bayes**: P(A | B) = P(B | A) P(A) / P(B); A | B no es lo mismo que B | A C2P1 1:28:33. Con los datos: P(B | A) = 0,813 (de los que cobran más que el promedio, el 81% tiene más de 5 años de experiencia).
- **Probabilidad total**: P(A) = Σ P(A | Bᵢ) P(Bᵢ) para una partición B₁, ..., Bₖ. Verificado en el box con cuatro tramos de experiencia: la suma ponderada da exactamente 0,3755.

### Correcciones y matices
- **Corrección:** Karim lee P(A | B) como "la probabilidad de que se cobre más que el 50%" C2P1 1:21:52. A es "cobrar al menos el promedio", no "más que el 50%" ni más que la mediana.
- **Corrección:** también dice que "la mediana está a la izquierda... la media está a la izquierda de la mediana" C2P1 1:19:40. Con asimetría a la derecha la media queda a la derecha de la mediana (3.270.653 contra 2.748.626), y por eso menos de la mitad cobra más que el promedio.
- **Corrección:** Georgina enuncia la probabilidad total como "P de A dado B1 más P de A dado B2 más..." sin los pesos C2P1 1:28:33. Faltan los P(Bᵢ): sin ellos la suma da 1,289, que ni siquiera es una probabilidad (verificado en el box).
- **Corrección:** al aclarar cardinal y módulo dice que "el módulo de un vector es la suma de las coordenadas al cuadrado" y se corrige: es la raíz cuadrada de esa suma C2P1 58:47.
- **Matiz:** "0,32 contra 0,319 es casi independencia" C2P1 1:12:12 es una intuición; si es "casi" o no lo decide un test (chi cuadrado de independencia, módulo 11), que depende también del tamaño de muestra.
- **Matiz:** cuando un alumno pregunta qué es "igual" en números, Georgina menciona "probabilidades distintas de 0,05" y la bondad de ajuste de forma confusa C2P1 1:24:39. La idea correcta: comparás P(A | B) con P(A) con un test cuyo error de tipo I controlás (α = 0,05).

### Preguntas de repaso
1. ¿Por qué P(neto ≥ promedio) da 0,375 y no 0,5?
2. Escribí P(A | B) y la condición de independencia. ¿Qué dicen los números del notebook?
3. Calculá P(B | A) con Bayes a partir de P(A | B) = 0,525, P(B) = 0,582 y P(A) = 0,375.
4. ¿Por qué la probabilidad total necesita los pesos P(Bᵢ)?

---

## 6. Estadística descriptiva, percentiles y outliers (notebook 02)
**Dónde:** C2P2 0:05, C2P2 1:45, C2P2 4:04, C2P2 7:28, C2P2 9:12, C2P2 10:20, C2P2 14:13, C2P2 59:58, C2P2 1:01:49, C2P2 1:05:15, C2P2 1:07:36, C2P2 1:08:48, C2P2 1:09:30, C2P2 1:11:12, C2P2 1:13:35, C2P2 1:20:49, C2P2 1:24:10, C2P2 1:27:02, C2P2 1:28:46, V04 0:34, V04 2:12, V04 3:18, V04 3:52, V04 4:59, C3P1 1:02:12, C3P1 1:07:25, C3P1 1:10:07, C3P1 1:29:21

### Conceptos clave
- **Tendencia central** C2P2 1:45, C2P2 4:04: la media x̄ = (1/n) Σ xᵢ es el centro de masa del histograma y es sensible a un solo valor extremo; la mediana ordena y toma el centro, y resiste hasta un 50% de datos contaminados (punto de ruptura), aunque 300 ceros sí la corren; la moda es el valor más frecuente (o el intervalo modal en continuas). En una distribución simétrica coinciden.
- **Percentiles** C2P2 7:28, V04 0:34: el percentil k deja el k% de los datos por debajo; cuartiles Q1, Q2 (mediana), Q3; rango intercuartílico IQR = Q3 − Q1, robusto.
- **Dispersión** C2P2 10:20: varianza muestral S² = Σ (xᵢ − x̄)² / (n − 1), insesgada; desvío estándar; coeficiente de variación = desvío / media, para comparar variables de distinta escala.
- **Boxplot** C2P2 14:13: caja de Q1 a Q3 con la mediana, bigotes hasta el último dato dentro de Q1 − 1,5 IQR y Q3 + 1,5 IQR, puntos afuera. Más estable que el histograma, que depende del ancho de bin. El **boxenplot** (letter value plot) muestra más percentiles y deja ver las colas C2P2 1:20:49.
- **Notebook 02 con el bruto** C2P2 1:01:49, C2P2 1:03:31: 4939 valores, media 3.876.029, desvío 2.492.699, mediana 3.268.000, máximo 20 millones.
- **Media vs mediana según el corte** C2P2 1:05:15, C3P1 1:07:25: si cortás en 20 millones la media (3,88 M) supera a la mediana (3,27 M); si cortás en 2 millones se invierten (1,39 M contra 1,47 M). Truncar fuerte a la izquierda de la cola fabrica una asimetría que los datos no tienen (verificado en el box).
- **Moda de una categórica**: "Hombre Cis", 3861 de 4938 respuestas, 7 categorías C2P2 1:07:36. Edad: media 37,5 y desvío 18,6, inflados por el 999 C2P2 1:08:48.
- **Bruto vs neto** C2P2 1:09:30: el neto tiene 4717 valores, mínimo 1,6 y máximo 653 millones; el bruto, 4939, mínimo 200.000 y máximo 20 millones. Coeficiente de variación: 0,643 el bruto y 3,289 el neto (verificado en el box), que refleja los outliers del neto más que una dispersión real (sin extremos, el CV del neto baja a 0,72).
- **Boxplots por nivel de estudios** C2P2 1:12:22, C2P2 1:13:35: el n de cada nivel es muy distinto (6 posdoctorados, 1175 universitarios) y para comparar poblaciones harían falta intervalos de confianza. El terciario tiene muchos outliers altos: gente sin título con mucha experiencia C2P2 1:16:55. Solo el 36% respondió el nivel de estudios.
- **Percentiles altos**: p95 = 8.700.000 y p98 = 11.000.000 C2P2 1:24:10 (verificados en el box). Por encima del p98 hay 104 filas en el notebook C2P2 1:28:46.
- **Quitar outliers** V04 2:12, V04 3:18, V04 3:52, V04 4:59: por percentil (por ejemplo el 1% más alto), por criterio de dominio, por múltiplos de Q3 o de desvíos. Después de recortar, aparecen "nuevos extremos" que antes no lo eran. No hay receta: documentá y fundamentá. Recortar para el gráfico no es borrar del dataset C2P2 1:27:02.
- **Quién decide qué es un outlier** C3P1 1:02:12, C3P1 1:29:21: el experto del dominio; en los entregables ustedes toman ese rol y justifican. Lo que sacás depende de la pregunta: si estudiás la edad, no tires filas por el sueldo. Informá el grupo apartado (ceros, sueldos muy altos). La estadística robusta recorta muy poco de cada cola (5% es común, 7% ya es mucho) C3P1 1:10:07.

### Correcciones y matices
- **Corrección:** Georgina dice que "fuera de tres veces el rango intercuartílico uno tiene datos atípicos" C2P2 9:12 y en el mismo bloque dibuja los bigotes en 1,5 IQR C2P2 14:13; Karim después habla de "dos o tres veces" C3P1 1:29:21. La regla de Tukey: más allá de 1,5 IQR desde los cuartiles es atípico; más allá de 3 IQR, extremo. Con el bruto 2026: Q3 + 1,5 IQR = 9.112.897 marca 202 filas (4,1%) y 3 IQR marca 39 (verificado en el box).
- **Corrección:** el notebook 02 y V04 usan como "regla IQR" quedarse con los valores menores o iguales a 2,5 × Q3 V04 3:52. No es la regla de Tukey ni usa el IQR: es un umbral ad hoc proporcional a Q3. Marca 61 filas (1,2%) contra las 202 de Tukey (verificado en el box).
- **dudoso:** Karim lee en el boxplot "outliers por encima de unos 7,5 millones" C2P2 1:11:12; el bigote superior está en 9,1 millones.
- **Matiz:** Georgina dice primero que la maestría tiene la mediana más alta y después que "el que declara doctorado es el que más gana en mediana" C2P2 1:13:35. Con el CSV 2026: doctorado 4.800.000, maestría 4.269.477, posgrado 4.000.000, posdoctorado 4.000.000 (con solo 6 casos) (verificado en el box).
- **dudoso:** "para dar vuelta la media y la mediana tenés que cortar más del 50% de los datos" C3P1 1:10:07. Depende de la distribución: con el bruto alcanza con cortar en 3 millones, que deja afuera el 57% (verificado en el box), pero no es una regla general.
- **para verificar:** la anécdota de la tabacalera que "podaba" los casos de cáncer C3P1 1:10:07; no da fuente.
- **Matiz:** la frase "lo llama análisis de la covarianza" para comparar medias por categoría C2P2 5:46: lo que describe es un análisis por estratos o grupos; el ANCOVA es otra técnica (regresión con un factor y una covariable).
- **Detalles del notebook 02** (verificado leyendo el repo): `central_tendency_max` usa `range(1500000, max, 10**7)` y genera solo dos puntos, así que el gráfico de líneas no muestra la tendencia (con un paso de 500.000 sí); y el texto "posdoctorado, el 25% gana más de ~650000" quedó de una edición anterior.

### Preguntas de repaso
1. ¿Por qué la mediana es robusta y la media no? ¿Qué es el punto de ruptura?
2. ¿Cómo se dibujan los bigotes de un boxplot? ¿Qué diferencia hay entre 1,5 y 3 IQR?
3. ¿Por qué cortar el bruto en 2 millones pone la media por debajo de la mediana?
4. ¿Por qué el CV del neto (3,29) no significa que los netos sean "más variables" que los brutos?
5. ¿Quién decide qué es un outlier y qué tenés que documentar?

---

## 7. Distribuciones y estandarización
**Dónde:** C2P2 17:31, C2P2 21:48, C2P2 27:22, C2P2 30:18, C2P2 32:30, C2P2 37:31, C2P2 38:10, C2P2 40:29, C2P2 43:49, C2P2 44:54, C2P2 47:38, C2P2 51:05, C2P2 56:03, C4P2 40:26

### Conceptos clave
- **Discreta**: X = cantidad de caras en tres tiradas de una moneda: P(X = 0) = 1/8, P(1) = 3/8, P(2) = 3/8, P(3) = 1/8. El diagrama de barras de frecuencias relativas es su versión empírica C2P2 17:31. Con 1000 simulaciones en numpy la empírica ya se parece a la exacta; con 10.000, más (tarea propuesta) C2P2 21:48.
- **Binomial**: n experimentos independientes con probabilidad de éxito p, P(X = k) = C(n, k) pᵏ (1 − p)ⁿ⁻ᵏ; el combinatorio n! / (k! (n − k)!) cuenta subconjuntos C2P2 27:22. p se estima de los datos (proporción de varones en la muestra) C2P2 32:30.
- **Aproximación normal de la binomial** (De Moivre Laplace; la transcripción dice "hemabre la plaz") cuando n crece; si p está lejos de 0,5 la binomial es asimétrica y hace falta más n C2P2 30:18.
- **Uniforme**: discreta (1/k) y continua en [a, b], P(c < X < d) = (d − c)/(b − a). En continuas, probabilidad = área bajo la densidad C2P2 38:10.
- **Normal**: parámetros μ y σ (σ es donde cambia la concavidad); "la distribución del error" C2P2 40:29. Regla empírica: μ ± σ contiene el 68,3%, μ ± 2σ el 95,4% y μ ± 3σ el 99,7% (verificado en el box).
- **Exponencial** (tiempos de espera, vida útil) y **chi cuadrado** (suma de cuadrados de normales estándar, base de muchos tests) C2P2 43:49.
- **Asimetría y curtosis** se comparan con la normal; en asimétricas la media se corre hacia la cola y la mediana resiste C2P2 44:54. El bruto 2026 tiene asimetría 1,71; su logaritmo, −0,37 (verificado en el box).
- **Estandarizar** C2P2 47:38: z = (x − x̄)/s deja media 0 y desvío 1; min max lleva a [0, 1]. Muchos algoritmos necesitan variables en escalas comparables (edad de 16 a 70 contra sueldos de millones).
- **Poblacional vs muestral** C2P2 51:05: σ̃² divide por n (máxima verosimilitud, asintóticamente insesgado) y S² por n − 1 (insesgado). Mirá la documentación: `np.var` usa `ddof=0` y `pandas.Series.var` usa `ddof=1`. Con millones de datos no importa; con 15, sí.
- **Parametrizaciones** C4P2 40:26: cada paquete parametriza distinto. En scipy, `expon` usa `scale` = 1/λ (la media), no λ; "un tercio no es tres".

### Correcciones y matices
- **Corrección:** Georgina dice "más del 60%", "63%... 68, perdón" y después "± 3σ, 99,5%" C2P2 40:29, C2P2 56:03. Los valores son 68,3%, 95,4% y 99,7%.
- **Corrección:** para min max dice "le resto el más chico y lo divido por el más grande" C2P2 47:38. Es (x − min)/(max − min); dividir por el máximo no lleva a [0, 1] (con el bruto 2026 da [0; 0,99]; verificado en el box).
- **dudoso:** "arriba de 100 personas ya tengo una distribución normal" C2P2 37:31. Para la binomial la regla práctica depende de p (por ejemplo n p y n (1 − p) mayores que 10), no solo de n.
- **Matiz:** llama a De Moivre Laplace "teorema central del límite" C2P2 30:18; es un caso particular (suma de Bernoulli).

### Preguntas de repaso
1. Escribí la distribución de X = caras en 3 tiradas.
2. ¿Qué porcentaje cae en μ ± 2σ en una normal?
3. ¿Cómo se calcula min max? ¿Y el z score?
4. ¿Qué parámetro le pasás a `scipy.stats.expon` para una exponencial de tasa λ = 3?

---

## 8. Varias variables: conjunta, covarianza, correlación y causalidad (notebook 03)
**Dónde:** C2P2 1:29:51, C2P2 1:36:37, C2P2 1:39:20, C2P2 1:42:41, C3P1 6:12, C3P1 9:04, C3P1 14:45, C3P1 17:38, C3P1 24:50, C3P1 28:16, C3P1 29:24, C3P1 31:41, C3P1 33:23, C3P1 35:05, C3P1 38:31, C3P1 42:36, C3P1 46:25, C3P1 50:22, C3P1 52:06, C3P1 54:25, C3P1 58:51, C3P1 1:03:18, C3P1 1:11:46, C3P1 1:16:59, C3P1 1:17:37, C3P1 1:22:08, C3P1 1:32:08, C3P1 1:34:22, C3P1 1:35:26, C3P1 1:39:25

### Conceptos clave
- **Conjunta vs marginales** C3P1 6:12, C3P1 9:04: mirar una variable por vez es ver "rodajas"; la verdad está en la distribución conjunta P(X = x, Y = y), la probabilidad de la intersección. Marginal = sumar (o integrar) la conjunta sobre la otra variable; condicional = conjunta / marginal C3P1 14:45.
- **Curvas de percentiles de crecimiento** como ejemplo de visualizar una variable condicionada a otras (edad, sexo) C3P1 17:38.
- **Sumar variables aleatorias** solo tiene sentido con numéricas; x̄ es una variable aleatoria, definida ω a ω C3P1 24:50.
- **Esperanza lineal; varianza no**: Var(X + Y) = Var X + Var Y + 2 Cov(X, Y) C3P1 28:16, C2P2 1:36:37. **Covarianza**: Cov(X, Y) = E[(X − EX)(Y − EY)]. **Correlación**: ρ = Cov / (σX σY), entre −1 y 1, sin unidades C3P1 29:24.
- **Scatter de pares** (x(ω), y(ω)): relación lineal positiva o negativa; ρ ≈ 0,4 contra ρ ≈ −0,8 C3P1 31:41.
- **Correlación mide solo relación lineal** C2P2 1:39:20, C3P1 50:22: un círculo, cuatro grupos simétricos o una parábola pueden tener ρ ≈ 0 con dependencia total. Independencia implica covarianza 0; covarianza 0 no implica independencia.
- **Independencia**: densidad conjunta = producto de las marginales; entonces E(XY) = EX EY, covarianza 0, Var(X + Y) = Var X + Var Y y la condicional es la marginal. Naive Bayes asume independencia para simplificar C3P1 35:05.
- **Normal bivariada** C3P1 38:31, C3P1 42:36: σ₁, σ₂ y ρ. Covarianza "full" (tres parámetros), "diagonal" (ρ = 0, σ distintas) o "esférica" (ρ = 0, σ iguales), opciones que aparecen en modelos como las mezclas gaussianas. Con ρ = 0 y σ distintas la nube está aplastada pero no inclinada C3P1 44:46.
- **Categóricas**: tablas de contingencia con marginales en los bordes; ejemplo de 100 personas, 52 varones y 48 mujeres, 13 zurdos (9 varones, 4 mujeres) C3P1 46:25.
- **Estimadores de correlación** C3P1 52:06: Pearson (covarianza muestral dividida por los desvíos), Spearman (Pearson sobre rangos) y tau de Kendall: los de rangos son más robustos.
- **Correlación no es causalidad** C2P2 1:42:41, C3P1 54:25: margarina y divorcios, litros de leche y pasajeros de avión, helados y ataques de tiburón. En medicina importa la causa (¿el síntoma lo da la enfermedad o el remedio?) y se buscan variables ocultas.
- **Notebook 03** (Karim) C3P1 58:51: filtra bruto ≤ 100 millones y edad ≤ 100 (máximo 20 millones, mínimo 200.000); recodifica género C3P1 1:03:18; `crosstab` de provincia por estudios y su `heatmap`; `crosstab` normalizado de edad por estudios C3P1 1:11:46; `pairplot` de bruto, neto y edad: edad contra neto no muestra patrón, bruto contra neto es casi una recta C3P1 1:17:37; `jointplot` hexagonal (la barra de color es la cantidad de casos por celda, un histograma 2D) y KDE como curvas de nivel C3P1 1:32:08; `catplot` para categóricas C3P1 1:34:22; KDE conjunta de edad y neto con `hue` por estudios, tres variables en un gráfico C3P1 1:35:26; práctico de bruto contra neto con la columna `DESCUENTOS` C3P1 1:39:25.
- **Errores honestos y deliberados** C3P1 1:22:08: hay brutos menores que netos (161 filas en 2026, verificado en el box); confundir bruto y neto es un error honesto; las encuestas serias ponen preguntas de control.

### Correcciones y matices
- **Corrección:** Georgina dice que "la varianza de la suma es la suma de las varianzas menos la relación... por eso le resto la covarianza" C3P1 28:49, C3P1 29:24. Es Var(X + Y) = Var X + Var Y + 2 Cov(X, Y); el signo menos va en Var(X − Y). En C2P2 lo había dicho bien C2P2 1:36:37. Verificado en el box con bruto y neto.
- **Corrección:** "dos variables independientes, es decir, covarianza cero... por definición la covarianza cero, son independientes" C3P1 33:23. Al revés no vale: covarianza 0 no implica independencia. Lo corrige ella misma con el ejemplo del círculo y un alumno lo remarca C3P1 43:40.
- **Corrección:** "un vector es normal multivariado si cada una de sus marginales es normal" C3P1 38:31. Tener marginales normales no alcanza: la definición es que toda combinación lineal sea normal (o que la densidad conjunta tenga esa forma). Contraejemplo verificado en el box: X normal e Y = S·X con S = ±1 al azar; Y es normal, pero X + Y vale exactamente 0 la mitad de las veces.
- **dudoso:** la forma cuadrática del exponente "con la matriz de correlación" C3P1 40:53: es (x − μ)ᵀ Σ⁻¹ (x − μ), con la inversa de la matriz de covarianza Σ.
- **dudoso:** "la covarianza tiene otra formulita" para categóricas C3P1 49:46: para nominales no se usa covarianza sino el chi cuadrado de independencia o la V de Cramér.
- **Corrección:** Karim lee en el `pairplot` de neto contra satisfacción que "los que tienen mayor nivel de satisfacción son los que ganan menos" C3P1 1:34:22. Es al revés: la mediana del neto sube con la satisfacción, 1,65 M (nivel 1), 2,4 M, 3,2 M y 4,5 M (nivel 4) (verificado en el box). El `pairplot` con una categórica superpone puntos y engaña; un boxplot por nivel lo muestra claro.
- **Corrección:** cuando Francisco pregunta si "universitario" incluye estudios en curso, Karim responde "no, son terminados" C3P1 1:15:19. El CSV tiene una columna aparte, `profile_studies_level_state`: de los 1175 universitarios, 590 completos, 317 en curso y 268 incompletos (verificado en el box).
- **Corrección:** en el práctico Karim dice que la correlación entre bruto y neto "tiene 0,61, porque fue contestado mal" C3P1 1:40:31. Con el filtro del notebook (los dos menores a 2,5 millones) da 0,870; sin filtro, Pearson da 0,201 y Spearman 0,950; con neto menor a 15 millones, Pearson 0,947 (verificado en el box). La salida guardada en el notebook dice 0,900. La moraleja sí vale: un puñado de netos absurdos destruye la correlación de Pearson, y la de rangos casi no se mueve.
- **Bug del notebook 03** (verificado en el box): el `replace` de género mapea `'Varón Cis'`, pero en 2026 la categoría se llama `'Hombre Cis'`; el grupo de varones (`df_H`) queda vacío y el histograma de varones contra mujeres solo dibuja mujeres. El notebook 04 sí usa `'Hombre Cis'`.
- **Matiz:** las salidas guardadas del notebook 03 son de otra versión del CSV (las primeras filas no coinciden con las del notebook 02) y el filtro `NETO < 1500000` del `pairplot` deja afuera a la mayoría en 2026 (la mediana del neto es 2,75 millones).
- **Matiz:** `df_limpio["salary_monthly_DESCUENTOS"] = ...` tira `SettingWithCopyWarning`; usá `.copy()` al filtrar o `.assign(...)`.

### Preguntas de repaso
1. Escribí Var(X + Y) y Var(X − Y) en función de las varianzas y la covarianza.
2. Dá un ejemplo de dos variables con correlación 0 que no sean independientes.
3. ¿Por qué Pearson da 0,20 y Spearman 0,95 entre bruto y neto sin filtrar?
4. ¿Alcanza con que las marginales sean normales para que el vector sea normal bivariado?
5. ¿Qué gráfico usarías para ver si la satisfacción cambia con el sueldo, y por qué no un `pairplot`?

---

## 9. Muestreo, ley de los grandes números y teorema central del límite
**Dónde:** C3P1 1:41:38, C3P1 1:47:42, C3P1 1:50:00, C3P1 1:52:16, C3P1 1:53:30, C3P1 1:56:49, C3P1 1:59:13, C3P1 2:00:21, C3P1 2:00:53, C3P2 0:02, C3P2 1:11, C3P2 4:27, C3P2 5:36, C3P2 6:44, C3P2 13:43

### Conceptos clave
- **Muestra iid** = "clones de un mismo experimento", lo ideal C3P1 1:47:42. El censista explica las preguntas para evitar errores honestos.
- **x̄ es una variable aleatoria** C3P1 1:50:00: si X₁, ..., Xₙ son normales iid, la suma es N(nμ, nσ²) y x̄ ~ N(μ, σ²/n). Promediar mantiene la media y achica la varianza.
- **Chi cuadrado** = suma de cuadrados de normales estándar independientes; sirve para la varianza muestral: (n − 1)S²/σ² ~ χ²ₙ₋₁ si los datos son normales C3P1 1:52:16.
- **Ley de los grandes números** C3P1 1:53:30: x̄ converge en probabilidad a μ: P(|x̄ − μ| < ε) → 1 para todo ε > 0.
- **Teorema central del límite** C3P1 1:56:49: si las Xᵢ son iid con varianza finita, (x̄ − μ)/(σ/√n) converge en distribución a N(0, 1), sin importar la distribución original. Si las Xᵢ ya son normales, x̄ es normal para cualquier n. Promedios de uniformes y de exponenciales se ven cada vez más normales C3P1 1:59:13.
- **¿Cuánto es n grande?** Georgina da 25, 40 o 100 según la asimetría, y prefiere "más de 100" C3P1 2:00:21. Con pocos datos y sin normalidad, procedimientos no paramétricos (Kruskal Wallis) C3P1 2:00:53.
- **Notebook 04, parte 1** (Karim) C3P2 1:11, C3P2 4:27: una muestra Poisson(5) de 500 (promedio ≈ 5,1); después una matriz de m filas por n columnas: cada fila es una muestra de tamaño n y `samples.mean(axis=1)` da m realizaciones de x̄, cuyo histograma se parece a una normal. Lo mismo con una exponencial `expon(loc=5, scale=2)` (media 7, varianza 4), con m = 100 y n = 2000: la varianza de las medias da 0,00206, cerca de 4/2000 = 0,002.
- **Ejercicio 1**: ver qué pasa con la varianza de x̄ cuando crece n y repetir con otra distribución no normal C3P2 5:36.
- **El ejemplo de Franco** (bioquímico): de 1000 pacientes elegir 10 al azar, medir glucosa, promediar y repetir C3P2 13:43.

### Correcciones y matices
- **Corrección:** Karim llama "discreta" a la exponencial C3P2 4:27. Es continua (la Poisson sí es discreta).
- **Corrección (importante):** ante la pregunta de Valeria sobre la diferencia entre hacer más realizaciones (m) y muestras más grandes (n), Karim responde que "el TCL dice que la media se comporta como normal cuando tu número de repeticiones es alto" y lo "demuestra" comparando 10 repeticiones de muestras de 20.000 con 20.000 repeticiones de muestras de 10 C3P2 6:44. Es al revés: el teorema habla de n, el tamaño de cada muestra. m solo decide cuántas medias usás para dibujar el histograma de la distribución de x̄: con m chico el histograma es ruidoso aunque x̄ ya sea casi normal, y con m enorme se ve con nitidez una distribución que todavía puede ser asimétrica si n es chico. Verificado en el box con una exponencial: con n = 2 y m = 20.000 la asimetría de x̄ es 1,42 (la teórica 2/√n = 1,41: lejos de normal); con n = 10, 0,60; con n = 100, 0,20; y con n = 20.000 y m = 1000, 0,03. La varianza de x̄ es 1/n en todos los casos, independiente de m.
- **Corrección:** Georgina escribe el TCL como "x barra le divido por su esperanza y la divido por su desviación estándar" C3P1 1:56:49: se resta μ y se divide por σ/√n (el desvío de x̄, no el de X).
- **Corrección:** dice que la densidad de la media "crece en altura y crece en dispersión" C3P1 1:59:13: crece en altura y la dispersión disminuye, porque la varianza es σ²/n.
- **dudoso:** "el promedio de tres exponenciales no tiene nada" C3P1 2:00:21: tiene una distribución conocida, una Gamma (forma 3); lo que quiere decir es que todavía no es normal.
- **dudoso:** la explicación de la convergencia en probabilidad con "un túnel" y "puntos aislados de medida cero" C3P1 1:53:30 mezcla la idea con la convergencia casi segura. La definición formal es la de arriba.
- **para verificar:** Karim dice que la varianza de las medias le da 0,01 con n = 200 de una exponencial C3P2 12:00; con media 1 debería dar 1/200 = 0,005 (depende de qué parámetros usó en vivo).

### Preguntas de repaso
1. Enunciá el teorema central del límite. ¿Qué tiene que crecer, n o m?
2. Si X₁, ..., X₁₀₀ son iid con media 5 y varianza 4, ¿qué distribución aproximada tiene x̄?
3. ¿Por qué si los datos son normales no hace falta el TCL?
4. ¿Qué dice la ley de los grandes números?

---

## 10. Estimación puntual e intervalos de confianza (notebook 04)
**Dónde:** C3P2 15:59, C3P2 17:40, C3P2 19:22, C3P2 24:28, C3P2 25:35, C3P2 26:45, C3P2 32:36, C3P2 35:22, C3P2 37:39, C3P2 40:29, C3P2 45:28, C3P2 47:47, C3P2 56:24, C3P2 58:41, C3P2 1:01:28, C3P2 1:03:44, C3P2 1:08:43, C3P2 1:10:22, C3P2 1:12:39, C3P2 1:16:03, C3P2 1:22:48, C3P2 1:25:40, C3P2 1:28:35, C3P2 1:31:23, C3P2 1:39:05, C3P1 2:02:30, C4P1 12:29

### Conceptos clave
- **Inferencia** = estudiar el error que cometés al usar un modelo con datos finitos. **Paramétrica**: conocés la forma de la distribución (normal) y no sus parámetros (μ, σ) C3P1 2:02:30. Modelo de posición: X₁, ..., Xₙ iid con media μ (el sueldo medio, quizás condicionado al nivel de estudios) C3P2 17:40.
- **Estimador** = función de los datos, y por eso variable aleatoria. Puntual: un número, con la confianza que da el método. Por intervalo: un rango que contiene el valor verdadero con probabilidad 1 − α, lo más angosto posible C3P2 19:22.
- **Propiedades**: insesgado (E[θ̂] = θ; sesgo = E[θ̂] − θ), consistente (converge al valor verdadero cuando n crece), eficiente (varianza chica) C3P2 26:45, C3P2 32:36. x̄ es insesgado, consistente y, por el TCL, aproximadamente normal C3P2 24:28. σ̃² (dividido n) es sesgado pero asintóticamente insesgado; S² (n − 1) es insesgado C3P2 25:35.
- **Exactitud y precisión** (la diana): exactitud = estar centrado, ligado al sesgo; precisión = poca dispersión, ligada a la varianza C3P2 26:45. Aparecen después en la matriz de confusión de clasificación: precisión, exactitud (accuracy), sensibilidad y especificidad C3P2 35:22.
- **"Ningún estimador decente arregla un muestreo mal hecho"** C3P2 37:39: la consistencia es una propiedad del método bajo el modelo, no de tu encuesta.
- **Qué es un IC del 95%** C3P2 40:29, C3P2 45:28: P(I ≤ μ ≤ S) = 1 − α donde I y S son aleatorios (dependen de la muestra). La probabilidad es del método: si repetís el muestreo muchas veces, el 95% de los intervalos contiene a μ; "el método falla una vez en 20". Una vez calculado con tus datos, el intervalo contiene o no contiene a μ.
- **Método del pivote** C3P2 47:47: un estadístico que contiene al parámetro y cuya distribución no depende de él. Con σ conocida: (x̄ − μ)/(σ/√n) ~ N(0, 1), de donde sale x̄ ± z₍α/2₎ σ/√n (z = 1,96 para 95%).
- **Sin normalidad**, el TCL da un IC aproximado con n grande C3P2 56:24. **Con σ desconocida y datos normales**: (x̄ − μ)/(S/√n) ~ t con n − 1 grados de libertad, IC x̄ ± t₍n−1, α/2₎ S/√n, más ancho que el z con n chico; con n grande t ≈ normal C3P2 58:41.
- **Dos muestras** C3P2 1:01:28, C3P2 1:03:44, C3P2 1:08:43: apareadas (dos medidas sobre el mismo sujeto) se trabajan con la diferencia por sujeto; independientes con igual varianza, t con varianza combinada y n₁ + n₂ − 2 grados de libertad; con varianzas distintas, Welch (grados de libertad de Welch Satterthwaite). σ conocida solo se tiene por la precisión de un instrumento o estudios previos C3P2 1:02:00. Si no sabés si las varianzas son iguales, lo razonable es ir a Welch C3P2 1:10:22.
- **IC para σ²** C3P2 1:12:39: con datos normales, (n − 1)S²/σ² ~ χ²ₙ₋₁ e IC [(n − 1)S²/χ²₍1−α/2₎, (n − 1)S²/χ²₍α/2₎] (ejemplo de llenado de botellas con 20 unidades).
- **Notebook 04, parte 2** C3P2 1:16:03: normal con μ = 100, σ = 15, n = 700 y semilla 42: estimador 99,88, IC (98,77; 100,99), longitud 2,22; de 1000 intervalos, 949 contienen a μ; con n = 4000 la longitud baja a 0,93 (se divide por √n) (todo verificado en el box). Ejercicio 2: lo mismo con Poisson y exponencial C3P2 1:22:48.
- **IC del sueldo bruto** C3P2 1:25:40: media 3.876.029, IC 95% (3.806.518; 3.945.540), longitud 139.022 (el notebook usa el desvío con `ddof=0`; con `ddof=1` los extremos se mueven unos pocos pesos: (3.806.511; 3.945.547), verificado en el box).
- **Brecha de género** C3P2 1:28:35: diferencia de medias del bruto entre varones cis y mujeres cis con Welch: 798.107, IC 95% (650.632; 945.583), con 3861 varones y 983 mujeres (verificado en el box con `ttest_ind(..., equal_var=False).confidence_interval()`).
- **Grupos desbalanceados** C3P2 1:31:23: con 983 contra 3861 el TCL aplica en los dos; cambia la precisión. Mejor ponderar que tirar datos.
- **Media ± desvío no es un IC** C4P1 12:29: para el IC de la media hay que dividir por √n y usar el percentil de la distribución del estadístico.

### Correcciones y matices
- **Corrección:** Georgina invierte una vez exactitud y precisión ("la precisión la da si estoy centrado... la exactitud la maneja la varianza") C3P2 29:42 y enseguida lo dice bien C3P2 30:16. Exactitud = centrado (sesgo), precisión = dispersión (varianza).
- **Corrección:** Karim interpreta el IC como "con una chance del 95% el verdadero valor del parámetro va a estar dentro de estos rangos" C3P2 1:20:30, justo lo que Georgina acababa de marcar como incorrecto. El 95% es la tasa de acierto del procedimiento, no la probabilidad de que μ esté en ese intervalo ya calculado.
- **Corrección:** Georgina pone como ejemplo de dos poblaciones con distinta varianza (Welch) "la diferencia entre bruto y neto" C3P2 1:07:05, después de haber dicho que bruto y neto de una misma persona son muestras apareadas C3P2 1:01:28. Lo correcto es lo segundo: t apareado sobre la diferencia por persona. Verificado en el box (4539 filas con 100.000 < neto < 15 M y neto ≤ bruto): el IC apareado de la diferencia media (655.515) mide 44.210 de largo; el de Welch, 182.299, cuatro veces más ancho porque ignora que bruto y neto están correlacionados.
- **Corrección:** ante el IC (650.632; 945.583) de la brecha, Karim pregunta si es razonable pensar que ganan igual; una alumna responde "no hay mucha diferencia" y queda sin corregir C3P2 1:28:35. El intervalo no contiene al 0: en esta muestra los varones cis declaran en promedio entre 650 mil y 945 mil pesos más de bruto, una diferencia estadísticamente distinta de 0 (alrededor del 25% de la media de las mujeres). Lo que sí hay que decir es que la encuesta no es una muestra aleatoria, así que no se generaliza a la población, y que la diferencia puede estar confundida con seniority o rol (módulo 12).
- **dudoso:** "con normales puedo hacer IC del 95% con 10 datos; si no hay normalidad necesito más de 100" C3P2 56:24. Con 10 datos normales, sí, pero con la t si σ es desconocida (verificado en el box: con n = 10 y S en lugar de σ, el intervalo con z cubre el 92,2% y el de t el 95,2%). El "más de 100" es la regla de la profesora; muchos textos dicen 30, y depende de cuán asimétricos sean los datos.
- **Matiz:** el ejercicio 3 del notebook dice "rehacer sacando los outliers (cero y 4,5 millones)", texto de una edición anterior; en 2026 el bruto no tiene ceros y la mediana es 3,27 millones.
- **Matiz:** en el ejercicio 4 el notebook guarda los grados de libertad en una variable `df`, pisando el DataFrame; si después ejecutás otra celda que usa `df`, falla.

### Preguntas de repaso
1. ¿Qué significa, exactamente, "IC del 95%"?
2. Deducí el IC para μ con σ conocida a partir del pivote.
3. ¿Cuándo usás z, cuándo t y cuándo Welch?
4. ¿Por qué bruto y neto de la misma persona se analizan apareados?
5. ¿Qué concluís del IC (650.632; 945.583) para la brecha, y qué no podés concluir?

---

## 11. Tests de hipótesis: la teoría
**Dónde:** C4P1 17:31, C4P1 22:28, C4P1 27:29, C4P1 30:16, C4P1 35:25, C4P1 40:26, C4P1 42:08, C4P1 44:21, C4P1 46:03, C4P1 49:23, C4P1 56:09, C4P1 57:53, C4P1 59:36, C4P1 1:02:27, C4P1 1:06:21, C4P1 1:16:24, C4P1 1:18:42, C4P1 1:21:44, C4P1 1:23:56, C4P1 1:26:47, C4P1 1:27:55, C4P1 1:32:27, C4P1 1:38:37, C4P1 1:41:29, C4P1 1:46:05, C4P1 1:48:15, C4P1 1:49:56, C4P1 1:52:48, C4P1 1:58:02

### Conceptos clave
- **Para qué** C4P1 22:28, C4P1 27:29: comparar errores de métodos A, B y C (si no difieren, elegís por otras razones: tamaño, despliegue), medir cambios en producción, ganarle a una línea base (baseline). Anécdota de un baseline de árbol que ningún modelo superaba porque train y test tenían distinta distribución.
- **¿Siempre normal?** C4P1 17:31: el modelo del error suele ser gaussiano de media 0; los promedios son aproximadamente normales por el TCL si hay independencia; Box Cox ayuda a acercarse a la normalidad; si no, no paramétricos.
- **La pregunta de la materia** C4P1 30:16: "¿el salario de los varones es mayor que el de las mujeres?" se traduce en parámetros: μ_V − μ_M > 0. Puede depender de la seniority (variable de confusión): después del test general hay que mirar condicionales C4P1 44:21.
- **H0 y H1** C4P1 35:25, C4P1 40:26: H0 es "no hay efecto" (las diferencias se deben a la variabilidad muestral); H1 es lo que el investigador quiere mostrar. La lógica es de falsación (Popper). Con un baseline: H0 error = baseline contra H1 error < baseline.
- **No rechazar no prueba H0** C4P1 42:08 ("no me da el cuero"), y **rechazar no "comprueba" H1**: decí "hay evidencia en la muestra a favor de H1" C4P1 46:03.
- **Neyman Pearson** C4P1 49:23: se fija de antemano cuántas veces aceptás equivocarte al rechazar: α = 5% es lo usual, 1% en medicina. "Siempre se puede torturar a los datos hasta que confiesen": la ética es usar la mejor herramienta disponible y no buscar el test que dé lo que querés C4P1 52:12.
- **Bajo H0** el estadístico tiene distribución conocida (normal por el TCL si n es grande) C4P1 57:53. **Región de rechazo** = valores poco probables bajo H0; el resto es región de no rechazo (no de "aceptación") C4P1 59:36. **Una o dos colas** según H1 (mayor, menor o distinto): el tornillo que puede salir corto o largo es bilateral C4P1 57:53.
- **Errores** C4P1 1:02:27, C4P1 1:21:44: tipo I = rechazar H0 siendo cierta, probabilidad α (el único que controlás); tipo II = no rechazar H0 siendo falsa, probabilidad β; potencia = 1 − β. β solo se calcula si conocés una alternativa concreta ("el oráculo") C4P1 1:06:21, C4P1 1:46:05: Karim da el ejemplo de lámparas de 5000 horas contra un proveedor que promete 5200.
- **Analogía judicial** C4P1 1:26:47: H0 es "inocente"; se controla el error de condenar a un inocente.
- **p valor** C4P1 1:27:55, C4P1 1:39:12: probabilidad, bajo H0, de obtener un estadístico tan o más extremo que el observado. Rechazás si p < α. Reportalo siempre: 0,051 y 0,9 son "no rechazo" pero dicen cosas muy distintas.
- **Receta** C4P1 1:23:56: elegir H1, nivel α, estadístico (un estimador del parámetro) y región de rechazo.
- **Tests paramétricos de la tabla** C4P1 1:32:27, C4P1 1:43:43: media con z (σ conocida, o S con n grande por el teorema de Slutsky C4P1 1:18:42); media con t (n chico, σ desconocida, datos normales); proporción y diferencia de proporciones con varianza p(1 − p)/n C4P1 1:48:15; varianza con chi cuadrado (contra un valor histórico o del fabricante); diferencia de medias apareada, con igual varianza y con Welch.
- **Otros tests** C4P1 1:41:29: chi cuadrado de independencia u homogeneidad (frecuencias observadas contra esperadas = producto de las marginales por n) C4P1 1:49:56; normalidad (Kolmogorov Smirnov, Shapiro Wilk); homocedasticidad (igualdad de varianzas, clave para elegir el método); ANOVA para varias medias; bondad de ajuste (chi cuadrado de Pearson para categóricas; Kolmogorov Smirnov con la corrección de Lilliefors para la normal) C4P1 1:43:11. En bondad de ajuste la hipótesis del investigador ("mis datos son normales") queda en H0, al revés que en el resto C4P1 38:45.
- **No paramétricos** C4P1 1:52:48: cuando no hay normalidad ni n suficiente. Kruskal Wallis como ANOVA no paramétrico (comparar varios métodos de ML) y Friedman para medidas repetidas (los mismos datasets evaluados con varios métodos). No son solo para categóricas: Wilcoxon y Mann Whitney reemplazan a la t con datos continuos C4P1 1:55:44.

### Correcciones y matices
- **Corrección:** ante la pregunta de una alumna, Georgina define el error de tipo I como "tendría que haber rechazado y no rechacé" C4P1 1:04:39 y después se corrige ("necesito más café") C4P1 1:05:46. Tipo I = rechazar una H0 verdadera; tipo II = no rechazar una H0 falsa.
- **Corrección:** sobre los no paramétricos dice "para el test t de uno o dos grupos... Mann Whitney, para el de dos grupos Wilcoxon" C4P1 1:52:48 y en la tabla final "Mann Whitney para una población y Wilcoxon para más de una" C4P1 1:59:12. Es al revés: Wilcoxon de rangos con signo es para una muestra o para muestras apareadas; Mann Whitney (también llamado Wilcoxon de suma de rangos) es para dos muestras independientes; Kruskal Wallis para tres o más. Verificado en el box con 15 pares simulados: Wilcoxon da p = 0,004 y Mann Whitney, que ignora el apareo, p = 0,68.
- **Corrección:** al listar tests de normalidad dice "Kruskal Wallis, perdón, Kolmogorov Smirnov" C4P1 1:42:02: se corrige sola.
- **dudoso:** Friedman "elige el método que tiene menor variabilidad" C4P1 1:56:52. El test de Friedman compara los rangos promedio de los métodos dentro de cada dataset (bloque); el paper de comparación de clasificadores sobre múltiples datasets que muestra es probablemente el de Demšar (2006), **para verificar**.
- **Matiz:** dice "así que estos no son tests de variable continua" C4P1 1:56:18 cuando acaba de explicar que sí lo son: lapsus.
- **dudoso:** el pivote "−2 log(X/σ) ~ chi cuadrado con 2 grados de libertad" para la exponencial C4P1 49:23: lo que vale es que si X es exponencial de media θ, 2X/θ ~ χ²₂.
- **Matiz:** la opinión sobre el INDEC que aparece al hablar de ética C4P1 52:12 es una anécdota política y no forma parte del contenido.

### Preguntas de repaso
1. Planteá H0 y H1 para "los varones cobran más que las mujeres". ¿Una o dos colas?
2. Definí error de tipo I, de tipo II y potencia. ¿Cuál controlás con α?
3. ¿Qué es el p valor? ¿Qué decidís con p = 0,051 y α = 0,05, y qué no podés decir?
4. ¿Qué test usás para dos muestras apareadas sin normalidad? ¿Y para dos independientes? ¿Y para cinco métodos evaluados en los mismos datasets?

---

## 12. Tests en Python (notebook 05)
**Dónde:** C4P2 2:12, C4P2 2:45, C4P2 3:51, C4P2 4:56, C4P2 6:04, C4P2 8:22, C4P2 11:16, C4P2 19:06, C4P2 22:02, C4P2 26:21, C4P2 30:11, C4P2 31:56, C4P2 34:06, C4P2 34:40, C4P2 37:00, C4P2 39:52, C4P2 45:37, C4P2 47:18

### Conceptos clave
- **IC contra test** C4P2 2:45: en el IC no sabés nada de la población; en el test H0 es el conocimiento previo y H1 lo que creés que cambió. Podés decidir con la región de rechazo o con el p valor, que además dice cuán lejos estás C4P2 4:56.
- **En scipy el α no se le pasa al test** C4P2 8:22: el resultado trae `statistic`, `pvalue` y `df`, y vos comparás `pvalue` con α. La dirección se indica con `alternative='two-sided' | 'less' | 'greater'` C4P2 39:52.
- **Ejemplo 1**, t para una muestra C4P2 6:04: alturas de 12 plantas contra 38, `ttest_1samp(data, 38, alternative='two-sided')`: media 36,41, t = −1,585, p = 0,141, 11 grados de libertad. No se rechaza H0 (verificado en el box; Shapiro da p = 0,79, así que la normalidad es razonable).
- **Qué es el p valor** C4P2 11:16: el área de la cola más allá del t observado, calculada bajo H0. Georgina corrige la definición imprecisa de un alumno: es la probabilidad de obtener un valor tan o más extremo si H0 fuera cierta.
- **La t asume normalidad** C4P2 19:06.
- **Ejemplo 2**, dos muestras independientes C4P2 22:02: `Cutlets.csv`, diámetros de dos unidades de producción (35 y 35). Independientes, no apareadas (contraejemplo apareado: dos patas de la misma rata). p = 0,47: no se rechaza. En el box: Shapiro 0,32 y 0,52, Levene 0,42; Student y Welch dan casi lo mismo (0,4722 y 0,4723).
- **Más n, más potencia** C4P2 30:11. En el box, con el ejemplo de las lámparas de Karim (H0: μ = 5000 h contra un proveedor que promete 5200; test z de una cola con α = 0,05 y un σ = 600 h que supuse yo, porque en clase no se dio): con n = 30 la potencia es 0,57 (β = 0,43); con 60, 0,83; con 100, 0,95; con 200, 0,999.
- **Ejemplo 3**, ANOVA de una vía C4P2 31:56: `LabTAT.csv`, tiempos de cuatro laboratorios, `f_oneway`: F = 118,7, p = 2,1 × 10⁻⁵⁷. Se rechaza: al menos un laboratorio difiere. Medias 178,4, 178,9, 199,9 y 163,7 (verificado en el box).
- **Ejemplo 4**, chi cuadrado de homogeneidad C4P2 34:40: `BuyerRatio.csv`, compradores varones y mujeres por región; `chi2_contingency` devuelve estadístico, p, grados de libertad y tabla de esperados. p = 0,66: proporciones similares.
- **Ejemplo 5** C4P2 37:00: `Customer+OrderForm.csv`, formularios defectuosos en cuatro centros (India 20/300, Indonesia 33/300, Malta 31/300, Filipinas 29/300); chi cuadrado 3,86, p = 0,28: no se rechaza (verificado en el box; hay que pasar el CSV de formato ancho a una tabla de contingencia con `melt` y `crosstab`).
- **Leé la documentación** C4P2 39:52: solo se usan comandos de scipy; cada paquete parametriza distinto y los defaults importan (scikit-learn, "psych learning" en la transcripción, tiene muy buena documentación).
- **La pregunta del entregable** C4P2 45:37: "¿las mujeres cobran menos que los hombres?". Preguntas para explorar: ¿cómo sabe el comando si es una o dos colas? ¿Qué α usa si no se lo pasás (ninguno)? Probá α = 0,03 y 0,01 C4P2 47:18.
- **La brecha con tests** (verificado en el box, varones cis contra mujeres cis, bruto): medias 4.039.036 contra 3.240.928 y medianas 3.450.941 contra 2.800.000; Welch de una cola t = 10,6, p = 6 × 10⁻²⁶; Mann Whitney p = 1 × 10⁻²⁰. Condicionando por seniority: Junior, diferencia de medianas 0 (p = 0,18); Semi Senior, 300.000 (p = 7 × 10⁻⁶); Senior, 545.908 (p = 3 × 10⁻⁶). Es el "mirar condicionales" que pidió Georgina C4P1 44:21.

### Correcciones y matices
- **Corrección:** Karim define α como "la probabilidad de equivocarnos cuando aceptemos que no hay cambios" C4P2 3:51. α es la probabilidad de rechazar H0 cuando es cierta (equivocarse al decir que sí hubo cambio); después lo dice bien ("error de tipo I"). En el box, con H0 cierta, el 4,76% de 5000 tests da p < 0,05.
- **para verificar:** al mostrar la regla "si p < α rechazo" dice "esto está al revés" C4P2 4:25; no queda claro qué celda o filmina tenía algo invertido.
- **Corrección:** "un 0,14 de error no está bueno" C4P2 18:31. El p valor no es una probabilidad de error ni la probabilidad de que H0 sea cierta.
- **dudoso:** "si los grados de libertad pasan de 100, Python usa el test normal" C4P2 19:39. `scipy.stats.ttest_1samp` y `ttest_ind` siempre usan la distribución t; lo que pasa es que con muchos grados de libertad la t y la normal casi coinciden.
- **Corrección (notebook):** en los ejemplos 2 a 5 el notebook compara el p valor con α/2 = 0,025. Un alumno pregunta por qué C4P2 26:21, Manuel (otro alumno) explica que el p valor bilateral que devuelve scipy ya incluye las dos colas y se compara con α = 0,05, y Georgina pide cambiarlo C4P2 27:57. α/2 solo aparece si buscás a mano el percentil crítico. En la copia del repositorio sigue el 0,025.
- **Corrección:** "como es bilateral" para el ANOVA C4P2 31:56: el F rechaza solo con valores grandes; la alternativa es "al menos una media distinta", sin colas en ese sentido.
- **Corrección (importante):** ante la pregunta de si el test se hace dos a dos, Karim responde "sí, se hacen todos contra todos" C4P2 34:06. El ANOVA es un único test F global; para saber qué pares difieren hace falta un post hoc con corrección por comparaciones múltiples, como Tukey HSD. En el box: todos los pares difieren salvo Laboratorio 1 contra 2 (p = 0,99).
- **Corrección (datos):** el enunciado del ejemplo 4 lista mujeres 550, 351, 480 y 350, pero `BuyerRatio.csv` tiene 435, 1523, 1356 y 750; Karim lo nota en clase ("olvidé un 1000") C4P2 34:40. Con el CSV, chi cuadrado 1,60 y p = 0,66 (no rechaza); con los números del enunciado, chi cuadrado 80,3 y p = 3 × 10⁻¹⁷ (rechaza). Verificado en el box: la conclusión depende de qué tabla uses.
- **Matiz:** el notebook pide "verificar los supuestos" pero no lo hace, y en el ejemplo 2 usa `ttest_ind` con el default `equal_var=True` (Student). Verificá normalidad (Shapiro) y varianzas (Levene) o usá Welch (`equal_var=False`) directamente.
- **Matiz:** en el ejemplo 3 la transcripción muestra que el p valor se leyó con dificultad ("no es 2,11, es 0,560..."); el valor es 2,1 × 10⁻⁵⁷, notación científica.

### Preguntas de repaso
1. ¿Con qué comparás el p valor que devuelve `ttest_ind(..., alternative='two-sided')`, con 0,05 o con 0,025?
2. Rechazaste H0 en un ANOVA con cuatro grupos. ¿Qué hacés para saber cuáles difieren?
3. ¿Por qué el ejemplo 4 rechaza o no según la tabla que uses?
4. ¿Qué pasa con la brecha de género cuando condicionás por seniority?

---

## 13. Visualización para comunicar
**Dónde:** V05 0:33, V05 1:41, V05 3:22, V05 5:04, V05 6:43, V05 8:22, V05 11:39, V05 14:59, C4P1 14:11, C4P2 49:34, C4P2 54:36, C4P2 1:01:28, C4P2 1:04:17, C4P2 1:07:01, C4P2 1:08:11, C4P2 1:15:27, C4P2 1:18:14, C4P2 1:19:53, C4P2 1:23:17, C4P2 1:27:13, C4P2 1:28:54, C4P2 1:33:23, C4P2 1:35:05, C4P2 1:38:31, C4P2 1:43:27, C4P2 1:48:03

### Conceptos clave
- **Visualizar = datos agrupados, proyectados o transformados**; una tabla también es una visualización (exacta, universal) V05 0:33. `groupby` por nivel de estudio más `describe` o una agregación como la mediana V05 1:41.
- **Barras** V05 3:22: categórica en x, numérica en y. `countplot` cuenta; `barplot` agrega con `estimator` (por defecto la media; puede ser la mediana) y dibuja una barra negra que es un intervalo de confianza. Problemas típicos: grupos con pocos datos (posdoctorado, primario), niveles sin ordenar o con nombres largos; las barras de error se sacaban con `ci=None` en seaborn viejo y hoy con `errorbar=None` V05 5:04. `hue` con `hue_order` agrega una tercera variable (estado del estudio) V05 6:43.
- **Líneas** V05 8:22: numéricas en los dos ejes y x continua; `lineplot` agrega por media en cada x y después de los 40 años se vuelve errático por falta de datos. Solución: `pd.cut` en franjas de 5 años y barras. `pointplot` para x categórica (sin líneas si no hay continuidad).
- **Scatter** V05 11:39, V05 14:59: un punto por fila, sin agregación; cuidado con el sobreploteo y los outliers (marcador chico, transparencia, o densidad). Color y tamaño agregan variables; el orden de dibujo oculta puntos: muestreá.
- **Para quién** C4P1 14:11, C4P2 1:01:28: visualizar para vos (dibujar la normal y las colas para entender los errores), para pares y para terceros. Para terceros: contexto, propósito y audiencia (jefe técnico, no técnico, diseñador); "hacé algo con estos datos" no es un pedido C4P2 49:34.
- **Impacto** C4P2 54:36: una infografía de refugiados contra la tabla de números; el grafo de traiciones de Game of Thrones (nodos, aristas con peso y dirección).
- **La representación cambia el razonamiento** C4P2 1:04:17: la tabla de resultados de la tesis de Milagro Teruel transformada en scatterplots.
- **Dynamite plots** C4P2 1:07:01: barras con barra de error esconden distribuciones muy distintas con la misma media y el mismo desvío. Mostrá la distribución: puntos, violín o boxplot.
- **Sesgos de percepción** C4P2 1:08:11: patronicidad (la cara en Marte), correlaciones espurias (Nicolas Cage contra ahogados en piletas, de Tyler Vigen), sesgo de confirmación; los sistemas automáticos amplifican los sesgos de la base.
- **Sesgos honestos y manipulación** C4P2 1:15:27: recortar la distribución para exagerar la brecha de género es mentir; inflar, confundir, simplificar de más ("Cómo mentir con estadísticas").
- **Eje y truncado** C4P2 1:18:14, C4P2 1:19:53: barras de votos de 200 a 500 exageran diferencias; el mismo truco sirve para "aplastar" un baseline. Reportá el eje completo y, si hace falta, un recuadro de zoom. En el box: con las medianas del bruto (mujeres 2,8 M, varones 3,43 M, cociente 1,22), un eje que arranca en 2,7 M hace que una barra parezca 7,3 veces la otra.
- **Más errores** C4P2 1:23:17, C4P2 1:27:13: barras que no corresponden a los números, porcentajes que suman más de 100, áreas apiladas ilegibles (mejor líneas), series sin título, escalas no explicadas (¿logarítmica?).
- **Una buena visualización** es honesta, funcional, estética, esclarecedora e informativa C4P2 1:28:54. Paletas aptas para daltonismo (se le pueden pedir a un LLM; seaborn trae `colorblind`).
- **Encodings visuales** C4P2 1:33:23: posición, tamaño, ángulo, área, volumen, color (tono, saturación), contraste, textura. Consistencia: si la burbuja es más grande, el número tiene que ser más grande.
- **Tipos de gráficos** C4P2 1:35:05, C4P2 1:38:31: comparar en una escala común alineada es lo que mejor se lee; barras apiladas y tortas, lo peor. Slope chart, coordenadas paralelas, coropletas, Gapminder (ingreso contra expectativa de vida), escalas logarítmicas.
- **Buenas prácticas** C4P2 1:43:27: tamaño de texto según el medio; Edward Tufte y el Challenger; chartjunk; pérdidas en rojo; evitá tortas. El objetivo es el mensaje, con "la verdad, toda la verdad" C4P2 1:48:03.

### Correcciones y matices
- **Matiz:** V05 es de 2021: `ci=None` ya está deprecado en seaborn 0.13 (usá `errorbar=None`) y los montos en pesos no sirven para comparar con 2026.
- **para verificar:** la jerarquía de "escala común alineada" que muestra C4P2 1:35:05 corresponde a Cleveland y McGill (1984), pero en clase no se nombra la fuente.
- **para verificar:** el blog "El arte de medir" C4P2 57:26 no cargó en clase; no hay URL.
- **Matiz:** la infografía de refugiados de la filmina tiene una errata ("refugados") C4P2 54:36.
- **Matiz:** las opiniones sobre IA generativa ("collage de texturas") y sobre qué LLM entiende mejor en inglés C4P2 1:08:11, C4P2 1:28:54 son opiniones de la profesora, no contenido.

### Preguntas de repaso
1. ¿Por qué un dynamite plot puede engañar? ¿Qué gráfico usarías en su lugar?
2. Las medianas son 2,8 M y 3,43 M. ¿Qué pasa si el eje y arranca en 2,7 M?
3. Nombrá las cinco cualidades de una buena visualización según la clase.
4. ¿Cómo sacás las barras de error de un `barplot` en seaborn 0.13?

---

## 14. Los entregables
**Dónde:** C1P1 17:17, C1P1 51:03, C2P1 2:22, C2P1 7:15, C2P1 13:50, C3P1 1:24:49, C4P2 45:37, C4P2 49:00, C4P2 1:49:42, C4P2 1:58:10

### Conceptos clave
- **Aprobación** C1P1 17:17: una tarea grupal dividida en dos entregables (parte 1 con los temas del primer fin de semana, parte 2 con los del segundo); hay que aprobar ambas. Incluye un proyecto de visualización (infograma; se puede usar IA de forma creativa) C1P1 51:03.
- **Grupos** C2P1 7:15, C2P1 13:50: el trabajo en grupo no se discute; todos con nombre en el encabezado; cada uno hace todo y después se arma el mejor trabajo. Si uno sube, cuenta como entrega del grupo. Verificá que el notebook corra entero de principio a fin.
- **Parte 1** (notebook): estadística sobre la encuesta sysarmy, con la pregunta central "¿las mujeres cobran menos que los hombres?" C4P2 45:37. Ustedes hacen de expertos y justifican cada corte de datos (por ejemplo, descartar a quien puso neto mayor que bruto) C3P1 1:24:49.
- **Parte 2** C4P2 1:49:42: poca estadística y una visualización grupal en formato libre (artículo de difusión, reporte, tweet, publicación de Instagram), máximo una página. Iterar las figuras con LLMs está permitido.
- **Mentorías** C4P2 49:00: exploración del dato y video de presentación; un segundo video a fin de año.
- **Sigue** Exploración y Curación de Datos (Ariel y José); Georgina vuelve en Aprendizaje No Supervisado C4P2 1:58:10.

### Correcciones y matices
- **para verificar:** las fechas. En C2P1 se dice apertura 10/04, cierre tentativo 24/04 para las dos partes y que la parte 2 "se presenta el 10/04" C2P1 2:22; en C4P2, que la parte 2 está publicada y se entrega desde el 17/04, con cierre a confirmar por Carolina Chavero C4P2 1:49:42. Todo práctico tiene que estar entregado al 1/9. Mirá el aula virtual.
- **Matiz:** los enunciados completos de los entregables están en el aula virtual, no en el repositorio público; lo de arriba es lo que se dijo en clase.

### Preguntas de repaso
1. ¿Qué preguntas tiene que contestar la parte 1 y qué formato tiene la parte 2?
2. ¿Qué tenés que justificar cuando filtrás filas del dataset?

---

## Lo que falta o quedó en duda
- **Filminas.** Las clases de Georgina se apoyan en filminas que están en el aula virtual y no en el repositorio público; las fórmulas de este apunte salen del audio y están revisadas contra la teoría, pero no pude ver las diapositivas (por ejemplo, la tabla de tests de C4P1 1:32:27 o la jerarquía de encodings de C4P2 1:35:05).
- **Enunciados de los entregables.** Están en el aula virtual; el módulo 14 solo recoge lo dicho en clase, y las fechas están **para verificar**.
- **Notebooks.** Uso los del repositorio público `DiploDatos/AnalisisyVisualizacion` (rama `master`), que pueden no ser idénticos a los que se abrieron en clase: los links de Colab de la filmina apuntaban a la edición 2025 C1P1 1:19:10. Las salidas guardadas del notebook 03 son de otra versión del CSV, y el notebook 05 todavía compara con α/2.
- **Subtítulos.** Los 13 videos tenían subtítulos automáticos en español, así que no hizo falta faster-whisper; los de C3P1 se bajaron recién al cuarto intento por límites de la grabación. Los automáticos deforman nombres (ver el glosario) y algunos números.
- **Audio.** En C2P2, alrededor de C2P2 49:56, el audio de Karim se corta y se entiende poco; en C4P2 el valor del p del ANOVA se lee mal en voz alta C4P2 31:56.
- **Referencias sin nombre:** el blog "El arte de medir" C4P2 57:26, la fuente de la escala común alineada (probablemente Cleveland y McGill) C4P2 1:35:05 y el paper de comparación de clasificadores con Friedman (probablemente Demšar 2006) C4P1 1:56:52.
- **Números de clase que no reproduje:** la correlación 0,61 entre bruto y neto C3P1 1:40:31 y la varianza 0,01 de las medias con n = 200 C3P2 12:00. La mediana del neto que se dice en C1P2 (2.786.000) tampoco coincide con la del CSV 2026 (2.748.626).
- **Quién es quién:** las facilitadoras Analía y Belén y los alumnos que intervienen (Manuel, Franco, Valeria, Rafael) solo se nombran de pila; el apellido del profesor de la anécdota del baseline ("Carbelino", probablemente Cristian Cardellino) está **para verificar**.

## Glosario de nombres que la transcripción deforma

| Se oye o se lee | Es |
|---|---|
| Nan Pierson | Neyman Pearson |
| Bruscal Wall, Crucal Wall, Crucal Wol, cruz calvo, grupo al goles | Kruskal Wallis |
| Colmog Smirnos, colmos Mirman, conmogross | Kolmogorov Smirnov |
| Lily Force | Lilliefors |
| Shapiro Will | Shapiro Wilk |
| Manwi, Matnis | Mann Whitney |
| Will Copson, Wilconson, Wonso | Wilcoxon |
| Freedman, Fritma | Friedman |
| Piarson | Pearson |
| Sperman | Spearman |
| Suski | Slutsky |
| hemabre la plaz | De Moivre Laplace |
| teorema semal del límite | teorema central del límite |
| Na Valles | Naive Bayes |
| pormantó | test portmanteau (Ljung Box) |
| homosedasticidad, homoseetasticidad | homocedasticidad |
| psych learning | scikit-learn |
| SBON | seaborn |
| Matlot Le | matplotlib |
| Grock | Grok |
| milagro peruelo | Milagro Teruel |
| Carbelino | Cardellino (**para verificar**) |
| OpenCube, o pentium | OpenQube (**para verificar**) |
| CPIE | CIII (**para verificar**) |
| aula viral | aula virtual |
| refugados | refugiados (errata de la filmina) |
