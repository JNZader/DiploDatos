# Guía de implementación: Ética Práctica para Ciencia de Datos (FAMAF UNC, Laura Alonso Alemany y Luciana Benotti)

**Videos:** 4 partes grabadas de las clases de agosto de 2026 en el canal de FAMAF UNC, C1P1 · C1P2 · C2P1 · C2P2, y 5 videos de 2020 del canal de la Diplomatura en Ciencia de Datos que la materia sigue recomendando, 2020-EPCD.1 · 2020-EPCD.3 · 2020-Grave · 2020-Caja · 2020-Barreras · Duración total: 7:28:53 (unas 7 horas y media).
**De qué va:** Laura Alonso Alemany y Luciana Benotti muestran cómo llevar la ética a la práctica de un proyecto de datos: cumplir la ley de datos personales, documentar el dataset con un data statement, preguntarse quién se beneficia y quién puede ser dañado, formalizar escenarios de daño, medir el sesgo desagregando el error por grupo, auditar sistemas propios, de terceros y generativos, y no desplegar cuando el daño no es aceptable. Esta guía junta las ideas que se pueden aplicar; el detalle por tema está en el apunte de estudio (`etica-practica-ciencia-de-datos-apunte-de-estudio.md`).

> Nota: esta guía sale de los subtítulos automáticos en español de los videos. **Faltan las transcripciones de los videos de 2020 "Ejercicios de pensamiento de la Caja de Herramientas Humanísticas" (8:32) y "Barreras a los cambios para soluciones más éticas y consensos sociales sobre qué es bueno" (18:05)**, porque la grabación no tiene subtítulos para ninguno de los dos; lo que esos videos agregan no está acá. Muchos nombres vienen deformados (ver el glosario al final). Lo que las docentes afirmaron y puede estar desactualizado va marcado como **para verificar**; todavía no está chequeado. Las ideas mías van marcadas como **Sugerencia**, y los fragmentos de código son todos sugerencias mías (la clase usa una notebook propia que no está transcripta). Los links dicen video y minuto: "C2P1 1:23:45" es la clase 2, parte 1, en 1:23:45.

---

## Checklist para arrancar ya

1. Antes de usar un dataset, escribí para qué se recolectaron originalmente los datos y verificá que tu uso sea compatible con esa finalidad y con el consentimiento que se dio.
2. Recolectá solo los datos que necesitás para el objetivo y listá los datos sensibles que tenés o que se pueden inferir.
3. Escribí un data statement de cada dataset que diga quién lo creó, para qué, quién lo financió, qué contiene, qué no contiene, cuándo se recolectó y con qué licencia.
4. Para cada sistema, contestá por escrito quién se beneficia y quién podría sufrir daños si funciona bien y si funciona mal, nombrando grupos concretos.
5. Hacé el ejercicio de autoetnografía con tu equipo para encontrar grupos y daños que no se te ocurrirían desde tu propia posición.
6. Formalizá cada escenario de daño con la variable protegida, el grupo protegido, el grupo privilegiado y el tipo de error que causa el daño.
7. Acordá con quienes deciden qué error es más grave, porque esa es una decisión de valores y no técnica.
8. Revisá si tus datos arrastran sesgo histórico, si representan a la población de uso y si el objetivo que optimizás es el que de verdad importa.
9. Compará la distribución de clases de tus predicciones con la de los datos para detectar amplificación, que es el diagnóstico más barato que existe.
10. Reportá las métricas por clase y el macro average, y no solo el promedio general.
11. Armá una matriz de confusión por grupo y graficá las tasas de falsos positivos y falsos negativos de cada uno.
12. Elegí la métrica de equidad que responde la pregunta de tu escenario de daño y fijá un umbral de tolerancia antes de comparar modelos.
13. Aceptá que no podés maximizar todas las métricas de equidad a la vez y dejá escrito cuál es la principal y por qué.
14. Hacé que cada decisión que afecta a una persona se pueda explicar y que esa persona tenga un canal para discutirla.
15. Auditá los sistemas de terceros y los chatbots con sus predicciones o con una grilla sistemática de consultas antes de adoptarlos.
16. Auditá los sistemas generativos comparando grupos con muchas entradas y reportando porcentajes, no casos sueltos.
17. Si usás embeddings preentrenados en tareas que tocan personas, medí sus asociaciones de género antes de usarlos.
18. Definí de antemano los umbrales que bloquean el despliegue y no despliegues si no se cumplen.
19. Invitá a una auditoría externa antes de producción, como se revisa un avión antes de que vuele.
20. Reservá tiempo para volver a auditar en producción y documentá cada incidente con su causa y la medida que agregás.
21. Separá los datos sintéticos de los reales y no uses detectores de texto generado sin marca de agua para decidir sobre personas.
22. Incorporá diversidad en todo el ciclo de vida, desde el framing y la gobernanza hasta las pruebas adversarias.
23. Diseñá la revisión humana para que la persona decida antes de ver la recomendación del sistema cuando hay derechos en juego.

---

## Versión completa

### 1. Antes de tocar los datos: finalidad, minimización y consentimiento
**Dónde:** C1P1 23:34, C1P1 24:07, C1P1 24:41, C1P1 26:52, C1P1 27:28, C1P1 28:01, C1P1 28:34, C1P1 29:07, C1P1 31:22, C1P1 34:41, C1P1 43:38, C1P1 45:49

**Contexto.** Luciana presenta la ley argentina de protección de datos personales (sin decir el número; tiene "casi 26 años", **para verificar**). Sus principios siguen vigentes: datos ciertos y actualizables, uso solo para la finalidad con la que se obtuvieron, recolección mínima, consentimiento libre, expreso e informado, y seguridad adecuada al estado del arte. Los datos personales incluyen a personas jurídicas y a lo que se puede inferir de los datos guardados. Los datos que se van a liberar con una licencia abierta tienen que avisarse en el consentimiento inicial. Si investigás, la ley también te alcanza.

**Por qué importa.** Si usás datos para algo distinto de lo que se le dijo a la persona, estás fuera de la ley aunque las multas sean bajas, y además rompés la confianza de quien te los dio. Recolectar "por las dudas" va directamente contra el principio de minimización.

**Cómo implementarlo.**
1. Escribí, para cada fuente de datos, para qué se recolectó originalmente y qué se le dijo a la persona.
2. Compará esa finalidad con el uso que le querés dar y anotá si es compatible.
3. Listá los datos sensibles que contiene (origen racial o étnico, opiniones políticas, religión, salud, vida sexual) y los que se pueden inferir.
4. Sacá las columnas que no necesitás para el objetivo.
5. Si pensás liberar los datos, definí la licencia y el nivel de anonimización antes de recolectar, y ponelo en el consentimiento.
6. **Sugerencia:** si el sistema da acceso a un derecho (salud, vivienda), diseñá un camino alternativo para quien no acepte el consentimiento digital, como plantea Luciana C1P1 42:31.

### 2. Documentar el dataset con un data statement
**Dónde:** C1P1 29:07, C1P1 33:01, C1P2 15:19, C1P2 42:21, C1P2 43:30, C1P2 45:52, C1P2 47:33, C1P2 54:23, C1P2 55:31, C1P2 58:51, C1P2 59:25, C1P2 1:01:03, C1P2 1:02:10, C1P2 1:02:43, C1P2 1:03:18, C1P2 1:04:27, C1P2 1:06:12, C1P2 1:10:39, C1P2 1:11:12, C2P1 33:30, C2P1 34:02, 2020-EPCD.3 1:06, 2020-EPCD.3 5:38, 2020-EPCD.3 6:12

**Contexto.** El práctico de la materia es un data statement sobre el dataset de tu mentoría: una documentación que ayuda a detectar sesgos y otros riesgos antes de que lleguen al usuario final. Lo arma un grupo entrevistando a un experto del dataset, idealmente con alguien que no conozca los datos para sumar una mirada fresca. Pide quién creó el dataset, por qué y quién lo financió; qué contiene, con ejemplos; qué **no** contiene ("uno de los problemas más grandes del sesgo es ver lo que no se ve"); cómo se eligió la muestra y cuándo se recolectaron los datos, porque el sesgo emergente también viene del tiempo; la fuente con su link y la licencia, aunque no exista; el uso dual; y datos sensibles. Laura suma el sesgo histórico y la representatividad. La metodología propone escribirlo antes de recolectar, y el resumen se escribe al final.

**Por qué importa.** Lo que no está escrito no se discute. Un data statement obliga a explicitar los límites de los datos antes de entrenar, y si comprás un dataset documentado así, podés cruzar información para detectar datos sintéticos.

**Cómo implementarlo.**
1. Elegí un experto del dataset y sumá al menos una persona que no lo conozca.
2. Documentá quién creó el dataset, con qué propósito, quién lo financió y en qué se diferencia de otros parecidos.
3. Describí qué contiene con ejemplos concretos, y escribí explícitamente qué información falta.
4. Anotá cómo se eligió la muestra y en qué período se recolectó, aunque sea aproximado.
5. Poné el link a la fuente y la licencia tal como es, incluido "no hay una licencia explícita".
6. Listá los datos sensibles, los usos para los que no debería usarse y los posibles usos duales.
7. Compará la población del dataset con la población donde se va a usar el modelo.
8. Pedile al experto que lea el borrador y escribí el resumen al final.

### 3. Encontrar a quién puede dañar tu sistema
**Dónde:** C1P2 13:39, C1P2 14:12, C1P2 18:45, C1P2 24:57, C1P2 32:05, C1P2 33:46, C2P1 0:02, C2P1 27:42, C2P1 28:17, C2P1 28:50, C2P1 29:28, C2P1 1:15:17

**Contexto.** Luciana plantea dos preguntas fundamentales: quién se beneficia, y quién podría sufrir daños si el sistema funciona bien y si funciona mal. Sugiere hablar de daños a grupos concretos de personas en lugar de riesgos en abstracto, y muestra que en los artículos de procesamiento de lenguaje natural casi nadie discute quién se daña ni qué poblaciones vulnerables se afectan. La autoetnografía ayuda porque tu trayectoria te hace ver daños que otros no ven (discriminación por edad en selección de personal, riesgos de privacidad para alguien de ciberseguridad). Laura explica que la variable protegida suele salir de un consenso social, pero que hay divisiones de la población que no se te ocurren si no las viviste. Por eso recomienda la autoetnografía que propuso Luciana (pensar en daños que vos mismo sufriste) y prestar atención al entorno; esa reflexión después se usa para formalizar escenarios de daño. Su ejemplo es el de las personas con agorafobia: son pocas, pero podría haber un sesgo estructural en su contra. Los grupos a mirar suelen estar minorizados, que no es lo mismo que minoritarios.

**Por qué importa.** Solo podés medir sesgos sobre los grupos que se te ocurrió definir. Un equipo homogéneo ve los daños que conoce y se pierde el resto.

**Cómo implementarlo.**
1. Escribí, para tu sistema, quién se beneficia y quién podría sufrir daños si funciona bien y si funciona mal.
2. Antes de diseñar métricas, pedile a cada integrante del equipo que anote daños que sufrió por sistemas automatizados o por instituciones.
3. Listá los grupos concretos que podrían quedar afectados por tu sistema, incluidos los chicos.
4. Consultá a personas de esos grupos o a especialistas ("acudir a las personas que saben, que siempre es mejor").
5. **Sugerencia:** guardá esa lista junto al data statement, porque es la base de los escenarios de daño del paso siguiente.

### 4. Formalizar los escenarios de daño
**Dónde:** C2P1 1:16:25, C2P1 1:17:00, C2P1 1:17:34, C2P1 1:18:08, C2P1 1:18:41, C2P1 1:19:47, C2P1 1:27:42, C2P1 1:29:20, C2P1 1:29:56, C2P1 1:32:08, C2P1 1:32:40

**Contexto.** Un escenario de daño se define con tres cosas: el grupo protegido y su complemento (el privilegiado), qué se predice y qué errores son más graves. En COMPAS la variable protegida es la raza y el error grave es el falso positivo (privar de libertad a quien no reincide). En la anonimización de historias clínicas la variable protegida es la edad, el grupo protegido son los niños y el error grave es el falso negativo (dejar expuesto un dato sensible). No todo trato diferencial es un daño: un modelo de crédito discrimina, a propósito, a quien no tiene respaldo económico.

**Por qué importa.** Qué error es peor es una decisión de valores, no técnica. Laura la compara con jacobinos y girondinos: si no la consensuás con quienes deciden, la toma el modelo por defecto.

**Cómo implementarlo.**
1. Escribí el objetivo del proyecto en una oración.
2. Definí la variable protegida, el grupo protegido y el privilegiado.
3. Definí la variable objetivo.
4. Describí en palabras qué le pasa a una persona con un falso positivo y con un falso negativo.
5. Acordá con quienes van a tomar la decisión cuál es más grave, apoyándote en la legislación que aplique.
6. Clasificá el daño: de asignación, de calidad de servicio o de representación (puede ser más de uno).

### 5. Revisar de dónde puede venir el sesgo
**Dónde:** C2P1 31:11, C2P1 31:48, C2P1 33:30, C2P1 34:35, C2P1 35:13, C2P1 36:56, C2P1 37:33, C2P1 38:39, C2P1 39:50, C2P1 40:24

**Contexto.** Laura recorre las fuentes: sesgo histórico en los datos; muestreo o representatividad (los percentiles de crecimiento de bebés pensados para otra población, los oxímetros calibrados con piel blanca); variables que faltan (el estudio de la copa de vino que no consideraba la clase social, **para verificar** la referencia); cómo se representa el objetivo (buenas notas no es lo mismo que aprender); sesgo de supervivencia (los aviones de la Segunda Guerra Mundial); framing; el algoritmo y la evaluación.

**Por qué importa.** Cada fuente pide un remedio distinto. Si el problema es de muestreo, ajustar la métrica no alcanza.

**Cómo implementarlo.**
1. Para cada fuente de la lista, escribí una oración sobre si aplica a tu proyecto y por qué.
2. Si la población de entrenamiento no es la de uso, evaluá un modelo específico para esa población, aunque sea más caro.
3. Buscá variables de contexto que falten, como el nivel socioeconómico, antes de interpretar una correlación.
4. Revisá si el objetivo que optimizás es el que de verdad te importa o un sustituto.

### 6. Diagnosticar amplificación
**Dónde:** C2P1 42:36, C2P1 43:47, C2P1 44:19, C2P1 45:27, C2P1 46:03, C2P1 47:47, C2P1 53:55, C2P1 55:38, C2P1 56:11

**Contexto.** Cuando el único incentivo es minimizar el error, el modelo tiende a la clase mayoritaria y además la exagera: con un dataset 80 y 20 puede predecir 90 o 100% de la mayoritaria. En "Men also like shopping", la actividad cooking tenía 33% más mujeres que hombres en el dataset y el modelo lo llevaba al 68% (**para verificar**). El diagnóstico es comparar la distribución de las predicciones con la del dataset, y según Laura "no cuesta absolutamente nada".

**Por qué importa.** Es el chequeo más barato que existe y detecta un sesgo que el accuracy esconde.

**Cómo implementarlo.**
1. Calculá la distribución de clases en el conjunto de evaluación.
2. Calculá la distribución de las predicciones del modelo sobre ese conjunto.
3. Repetí las dos cosas para cada grupo de la variable protegida.
4. Si la proporción predicha de la clase mayoritaria es mayor que la real, registralo como amplificación.

```python
# Sugerencia: chequeo mínimo de amplificación por grupo con pandas
import pandas as pd

def amplificacion(df, y_true="y", y_pred="pred", grupo="grupo"):
    real = df.groupby(grupo)[y_true].value_counts(normalize=True).rename("real")
    pred = df.groupby(grupo)[y_pred].value_counts(normalize=True).rename("predicho")
    tabla = pd.concat([real, pred], axis=1).fillna(0)
    tabla["diferencia"] = tabla["predicho"] - tabla["real"]
    return tabla
```

### 7. Mitigar con mejores incentivos
**Dónde:** C2P1 47:47, C2P1 48:21, C2P1 48:54, C2P1 49:26, C2P1 50:03, C2P1 50:34, C2P1 56:11, C2P1 59:02, C2P1 59:35, C2P1 1:00:42, C2P1 1:02:26, C2P1 1:03:02

**Contexto.** La receta de Laura es "tener mejores incentivos. Siempre, siempre". Eso se traduce en restricciones sobre el espacio de soluciones: descartar las funciones que dañan a un grupo, con restricciones duras o probabilísticas, o con optimización multiobjetivo (lo compara con lo que hace Spotify con recomendaciones pagas). En "Men also like shopping" usaron relajación lagrangiana como metaalgoritmo y la precisión no cayó: el modelo sesgado era solo la primera función que encontraba la búsqueda. Las alternativas artesanales son balancear el dataset (lo primero que prueba ella, aunque distorsiona la realidad), cambiar la métrica, pesar distinto los errores y curar características.

**Por qué importa.** Mitigar suele costar tiempo de modelado y cómputo, no precisión. Saberlo te ayuda a negociar con quienes deciden, que a veces solo quieren el incentivo económico.

**Cómo implementarlo.**
1. Probá primero balancear el dataset de entrenamiento y medí de nuevo la amplificación.
2. Si no alcanza, pesá distinto los errores de cada clase o grupo.
3. Si tampoco alcanza, definí una restricción explícita (por ejemplo, que la distribución predicha por grupo no se aleje de la real más de cierto margen) y buscá un modelo que la cumpla.
4. Documentá cuánto costó en tiempo y cómputo, y cuánto cambió el error, para presentarlo a quienes deciden.

### 8. Elegir métricas que no escondan a las minorías
**Dónde:** C2P1 1:04:09, C2P1 1:04:42, C2P1 1:05:16, C2P1 1:06:57, C2P1 1:08:03, C2P1 1:08:36, C2P1 1:09:09, C2P1 1:09:43, C2P1 1:10:15

**Contexto.** "Nuestras métricas son nuestro incentivo." El macro average le da el mismo voto a cada clase, así que un F1 de 30% en la clase minoritaria ya no queda tapado por un 98% en la mayoritaria; está en scikit-learn. Laura también advierte sobre las métricas proxy: medir tiempo de reproducción en lugar de engagement, o click through en lugar de conversión.

**Por qué importa.** Un promedio ponderado por población puede verse excelente mientras el sistema falla con un grupo entero.

**Cómo implementarlo.**
1. Reportá siempre la métrica por clase y el macro average junto al promedio general.
2. Escribí qué querés medir de verdad y qué estás midiendo, y explicitá la distancia entre los dos.
3. **Sugerencia:** en scikit-learn, `f1_score(y, pred, average="macro")` y `classification_report(y, pred)` te dan esto en una línea.

### 9. Hacer la auditoría de equidad desagregada
**Dónde:** C2P1 1:14:43, C2P1 1:33:13, C2P1 1:33:46, C2P1 1:34:21, C2P1 1:35:27, C2P1 1:36:35, C2P1 1:37:08, C2P1 1:37:40, C2P1 1:38:14, C2P1 1:38:48, C2P1 1:39:21, C2P1 1:47:18, C2P1 1:47:53, C2P1 1:48:28

**Contexto.** La idea básica de las métricas de equidad es desagregar: armar la matriz de confusión de cada grupo y comparar la tasa de error que corresponde al daño que definiste. Si en anonimización los falsos negativos son iguales en los dos grupos, no hay discriminación (aunque un 50% de falsos negativos ya sería inaceptable por sí solo); si en COMPAS los falsos positivos son mucho peores para un grupo, eso es discriminatorio. Desagregar hasta el caso individual no sirve, porque te quedás en lo anecdótico y solo ayudás a quien puede quejarse. La notebook de la clínica de equidad sigue estos pasos: cargar datos, formalizar el escenario de daño, visualizar distribuciones, refinar definiciones, analizar el modelo desagregando y diagnosticar. No incluye mitigación.

**Por qué importa.** El agregado oculta. Un número desagregado ("no es mi imaginación, está pasando sistemáticamente") es lo que permite tomar medidas sistemáticas.

**Cómo implementarlo.**
1. Tomá las predicciones, las etiquetas reales y la variable protegida.
2. Armá una matriz de confusión para el grupo protegido y otra para el privilegiado.
3. Calculá la tasa de falsos positivos y la de falsos negativos de cada grupo.
4. Mirá primero la tasa del error que definiste como grave en el escenario de daño.
5. Graficá las tasas por grupo en un diagrama de barras.
6. Revisá además si la tasa del error grave es aceptable en términos absolutos, aunque sea pareja.

```python
import pandas as pd
# Sugerencia: tasas de error por grupo a partir de las predicciones
from sklearn.metrics import confusion_matrix

def tasas_por_grupo(df, y_true="y", y_pred="pred", grupo="grupo"):
    filas = []
    for g, d in df.groupby(grupo):
        tn, fp, fn, tp = confusion_matrix(d[y_true], d[y_pred], labels=[0, 1]).ravel()
        filas.append({
            "grupo": g,
            "FPR": fp / (fp + tn) if (fp + tn) else float("nan"),
            "FNR": fn / (fn + tp) if (fn + tp) else float("nan"),
            "tasa_positivos": (tp + fp) / len(d),
        })
    return pd.DataFrame(filas)
```

### 10. Elegir una métrica agregada que responda tu pregunta
**Dónde:** C2P1 1:39:55, C2P1 1:40:28, C2P1 1:41:02, C2P1 1:41:38, C2P1 1:42:13, C2P1 1:42:47, C2P1 1:43:25, C2P1 1:43:56, C2P1 1:44:30, C2P1 1:45:05, C2P1 1:45:38

**Contexto.** Para comunicar en un número (el ejemplo de los tres minutos con un diputado) o para elegir entre modelos, hacen falta métricas agregadas: tasa de falsos positivos, equal opportunity, equalized odds, predictive parity y statistical parity. Laura las traduce a preguntas concretas para COMPAS y para anonimización (ver la tabla del módulo 7 del apunte) y prefiere construir la métrica a partir de la pregunta del problema. Las definiciones de la notebook vienen del artículo de Wikipedia sobre equidad y de un curso de Google.

**Por qué importa.** Las métricas "en abstracto son muy abstractas"; si no sabés qué pregunta responde cada una, podés optimizar la equivocada.

**Cómo implementarlo.**
1. Escribí tu pregunta en lenguaje natural ("de las personas que no reinciden, ¿a qué proporción le negamos la libertad?").
2. Elegí la métrica que responde exactamente esa pregunta.
3. Reportá su valor para cada grupo y la diferencia entre grupos.
4. Usá esa misma métrica para comparar modelos candidatos.

### 11. Auditar sistemas de terceros y chatbots antes de usarlos
**Dónde:** C1P1 18:01, C1P1 18:34, C1P1 19:08, C1P1 19:40, C1P1 20:13, C2P1 1:48:28, C2P1 1:49:03, C2P1 1:49:37

**Contexto.** La auditoría de equidad de la notebook solo necesita las predicciones, sin acceso al modelo ni ejecutarlo, así que sirve para cualquier sistema (Laura da ejemplos desde organismos marinos hasta el pronóstico del tiempo en Córdoba contra Iguazú). Para chatbots, el caso del Ministerio de Salud de España muestra el método: un ciudadano preguntó la dosis para pesos de 3 a 32 kg, repitió cada consulta tres veces y encontró errores de cálculo y de unidades; el servicio se bajó en menos de 24 horas. Los modelos de lenguaje "no son de aritmética".

**Por qué importa.** Si comprás o integrás un sistema, sos responsable de lo que hace con tus usuarios, aunque no lo hayas entrenado.

**Cómo implementarlo.**
1. Pedile al proveedor, o generá vos, predicciones sobre un conjunto con etiquetas reales y la variable protegida.
2. Corré la auditoría desagregada del paso 9.
3. Para un chatbot, armá una grilla de consultas que recorra los valores relevantes (pesos, edades, montos) y los grupos de interés, y repetí cada consulta varias veces.
4. Compará cada respuesta con la fuente oficial y marcá las que calculan en lugar de citar.
5. **Sugerencia:** sacá los cálculos críticos del modelo de lenguaje y resolvelos con código determinista.

### 12. Someterse a auditoría externa y saber cuándo no desplegar
**Dónde:** C1P1 12:25, C1P1 13:00, C1P1 13:33, C1P1 14:07, C1P1 15:50, C1P1 16:23, C1P1 20:46, C2P1 1:37:40

**Contexto.** En el segundo intento de Países Bajos, las auditorías de sociedad civil y periodismo de investigación detectaron que el sistema seguía discriminando y no se desplegó. En el caso de la Smart TV que no entendía a una persona con síndrome de Down, Laura es tajante: igual que no se venden autos sin cinturón, si no podés hacer un producto que incluya a los grupos vulnerables, no lo saques.

**Por qué importa.** El objetivo de la materia, en palabras de Laura, es que estos controles ocurran antes de producción y no por la ciencia ciudadana después del daño.

**Cómo implementarlo.**
1. Definí con anticipación los umbrales de error grave, absolutos y por grupo, que bloquean el despliegue.
2. Invitá a una parte externa (otro equipo, una organización de la sociedad civil, especialistas del dominio) a auditar con tus datos o con los suyos.
3. Si no se cumplen los umbrales, no despliegues; documentá la decisión.

### 13. Planificar el monitoreo y la investigación de incidentes
**Dónde:** C1P1 5:41, C1P1 6:15, C1P1 6:51, C2P1 40:56, C2P1 41:30

**Contexto.** Laura usa la analogía de la aviación: cada accidente se investiga, se encuentran las causas y se cambia el protocolo, por eso los incidentes no crecen con la cantidad de vuelos. En IA los incidentes crecen cada año (**para verificar** las cifras del reporte de Stanford). Además, el sistema cambia el mundo cuando entra en funcionamiento y pueden aparecer sesgos nuevos.

**Por qué importa.** Un sistema que pasó la auditoría inicial puede empezar a dañar meses después, y si nadie lo mira, el mismo error se repite.

**Cómo implementarlo.**
1. Reservá horas del proyecto, desde la planificación, para volver a auditar después del despliegue.
2. Repetí la auditoría desagregada con datos de producción a intervalos fijos.
3. Cuando haya un incidente, documentá qué pasó, la causa y la medida que agregás al proceso para que no se repita.
4. **Sugerencia:** revisá bases públicas de incidentes con sistemas parecidos al tuyo antes de diseñar, para no repetir errores conocidos (el chatbot de Austria repitió un sesgo "sistematizado desde 2016").

### 14. Cuidar el origen de los datos frente a lo sintético
**Dónde:** C1P1 1:07:10, C1P1 1:07:42, C1P1 1:09:23, C1P1 1:12:47, C1P1 1:13:21, C1P1 1:14:29, C1P1 1:15:03, C1P1 1:15:37, C1P1 1:16:09, C1P1 1:16:42

**Contexto.** Luciana advierte que estamos "inundados de datos sintéticos": hay trabajos que reemplazaron a los crowdworkers por modelos de lenguaje y se venden datasets sintéticos como si fueran reales. Los datos sintéticos sirven para simular experimentos y probar pipelines, pero no reemplazan a los reales. Los detectores sin marca de agua andan "muy mal" (uno decía que el preámbulo de la Constitución lo escribió una IA); las marcas de agua sobre logits sí permiten detectar con mucha certeza en textos largos, pero el detector lo tiene cada empresa.

**Por qué importa.** Si entrenás o evaluás con datos sintéticos sin saberlo, tus conclusiones sobre personas reales no valen.

**Cómo implementarlo.**
1. Pedí documentación de procedencia de cualquier dataset que compres o descargues.
2. Usá datos sintéticos para probar el pipeline y el diseño experimental, y separalos claramente de los reales.
3. No uses detectores de texto generado sin marca de agua para tomar decisiones sobre personas.
4. **Sugerencia:** si armás conjuntos de evaluación, considerá el enfoque del grupo de Luciana, con personas reales en encuentros o datatones.

### 15. Investigar con datos de personas
**Dónde:** C1P1 31:54, C1P1 32:29, C1P1 43:38, C1P1 46:24, C1P1 46:59, C1P1 49:46, C1P1 50:18

**Contexto.** Si investigás con datos de personas tenés que cumplir la ley de la región donde operás e informar en el consentimiento qué datos recolectás, para qué y con qué anonimización. En procesamiento de lenguaje natural se espera cada vez más la aprobación de un comité de ética, aunque no siempre es obligatoria; si tu jurisdicción no tiene comité, podés acudir al de otra. Los comités de las conferencias revisan después de hecha la investigación. Y las páginas web restringen cada vez más el scraping.

**Por qué importa.** El aval de un comité a posteriori no repara un diseño que ya expuso a las personas.

**Cómo implementarlo.**
1. Antes de recolectar, presentá el protocolo a un comité de ética, aunque no sea obligatorio en tu área.
2. Revisá las licencias y las condiciones de uso de cada sitio antes de hacer scraping.
3. Escribí en el consentimiento el nivel de anonimización y si los datos se van a liberar.

### 16. Usar gráficos para decidir y métricas agregadas para rankear, con un umbral de tolerancia
**Dónde:** C2P2 44:46, C2P2 45:20, C2P2 45:55, C2P2 51:05, C2P2 51:38, C2P2 52:11

**Contexto.** Laura recomienda los gráficos de tasas por grupo para decidir y para comunicar, y las métricas agregadas para rankear modelos o usarlas como criterio en la búsqueda de hiperparámetros. Cuenta que quienes auditan sistemas de forma profesional eligen la métrica relevante para el problema y fijan un umbral: ningún modelo que lo supere es aceptable. También advierte que no podés maximizar todas las métricas de equidad a la vez, porque algunas son complementarias por definición: si una es alta, otra es baja.

**Por qué importa.** Sin un umbral fijado de antemano, la discusión sobre si un modelo "es suficientemente justo" se termina resolviendo a favor del que tiene mejor accuracy. Y si intentás optimizar todas las métricas, ninguna te sirve como criterio.

**Cómo implementarlo.**
1. Elegí una sola métrica de equidad principal, la que responde la pregunta de tu escenario de daño (sección 10).
2. Fijá por escrito el umbral de diferencia entre grupos que vas a tolerar, antes de ver los resultados de los modelos candidatos.
3. Descartá los modelos que superen el umbral, y recién entre los que quedan elegí por desempeño.
4. Usá el gráfico de tasas por grupo para presentar la decisión a quien la tenga que tomar.
5. Si vas a reportar varias métricas, aclará cuál es la principal y por qué, en lugar de intentar que todas den bien.

```python
# Sugerencia: filtrar candidatos por un umbral de equidad fijado de antemano
UMBRAL_FPR = 0.05  # diferencia máxima tolerada entre grupos; definilo con el equipo antes de mirar resultados

def elegir_modelo(resultados):
    """resultados: lista de dicts con 'nombre', 'macro_f1' y 'fpr_por_grupo' (dict grupo -> FPR)."""
    aceptables = []
    for r in resultados:
        tasas = list(r["fpr_por_grupo"].values())
        brecha = max(tasas) - min(tasas)
        if brecha <= UMBRAL_FPR:
            aceptables.append({**r, "brecha_fpr": brecha})
    if not aceptables:
        return None  # ningún modelo es aceptable: no se despliega
    return max(aceptables, key=lambda r: r["macro_f1"])
```

### 17. Hacer que las decisiones se puedan explicar
**Dónde:** C2P2 52:47, C2P2 53:21, C2P2 53:54, C2P2 54:27, C2P2 54:59, C2P2 55:34, C2P2 1:34:19, C2P2 1:34:56, C2P2 1:35:30, C2P2 1:36:06, 2020-EPCD.1 14:43

**Contexto.** En la notebook, Laura muestra dos herramientas: SHAP, que dice cuánto contribuye cada característica a una decisión de forma agnóstica al modelo (por ejemplo, para ver si te negaron un crédito por una variable protegida), y What-If, que arma contrafácticos comprobables ("¿y si saco esta variable?") y ayuda a medir el impacto de una mitigación. En el cierre agrega que en educación, finanzas y trabajo es obligatorio por ley que un algoritmo pueda explicar en qué se basa su decisión, para que la persona tenga derecho a réplica, con el ejemplo de Uber asignando viajes (**para verificar** el alcance legal). En 2020, Luciana ya planteaba que la ciencia de datos "tiene que ser capaz de dar explicaciones por las cosas que hace".

**Por qué importa.** La explicabilidad es lo que permite que quien decide actúe, y lo que le da a la persona afectada la posibilidad de reclamar.

**Cómo implementarlo.**
1. Para cada decisión que afecte a una persona, definí qué explicación le vas a poder dar y quién se la da.
2. Calculá la contribución de cada característica a las predicciones y revisá si alguna variable protegida, o una que la represente, pesa mucho.
3. Probá contrafácticos: cambiá solo la variable protegida y mirá si cambia la predicción.
4. Usá los mismos contrafácticos para medir si una mitigación realmente cambió el comportamiento.
5. Documentá el canal por el que una persona puede pedir la explicación y discutir la decisión.

```python
# Sugerencia: prueba contrafáctica simple, cambiando solo la variable protegida
import pandas as pd

def tasa_de_cambio_contrafactico(modelo, X: pd.DataFrame, columna: str, valor_a, valor_b):
    """Proporción de filas cuya predicción cambia al pasar la variable protegida de valor_a a valor_b."""
    Xa = X.copy(); Xa[columna] = valor_a
    Xb = X.copy(); Xb[columna] = valor_b
    return (modelo.predict(Xa) != modelo.predict(Xb)).mean()
```

### 18. Auditar sistemas generativos con exploración sistemática
**Dónde:** C2P2 57:24, C2P2 59:36, C2P2 1:00:43, C2P2 1:01:20, C2P2 1:03:13, C2P2 1:05:30, C2P2 1:06:02, C2P2 1:07:10, C2P2 1:10:59, C2P2 1:11:39, C2P2 1:12:12, C2P2 1:12:51, C2P2 1:14:31, C2P2 1:15:04, C2P2 1:15:37

**Contexto.** Las métricas basadas en error no sirven cuando no hay una respuesta esperada, como en el aprendizaje no supervisado o en los sistemas generativos (un cuento para chicos de 5 años tiene "un montón" de versiones válidas). Igual se puede auditar: imaginás escenarios de daño y comparás grupos con otra medida. Los ejemplos de la clase son el recorte de miniaturas de Twitter (prefería caras blancas y también caras sonrientes), un reconstructor de alta resolución que blanqueaba caras, sacaba anteojos y agregaba pelo, y un modelo de lenguaje abierto que prefería "la menstruación es una enfermedad" antes que "la eyaculación es una enfermedad". Laura opone esta exploración al parche anecdótico, y recomienda trabajar con sociólogos y trabajadores sociales.

**Por qué importa.** Arreglar el caso que se hizo viral no arregla la tendencia. Solo un reporte con porcentajes ("en qué proporción de casos a las personas con anteojos se las representa sin anteojos") permite una acción sistemática.

**Cómo implementarlo.**
1. Escribí los escenarios de daño del sistema generativo, con ayuda de especialistas si el dominio no es el tuyo.
2. Armá pares de entradas que solo difieran en el atributo del grupo (género, color de piel, anteojos, edad).
3. Generá varias salidas por entrada y definí qué rasgo de la salida vas a contar.
4. Reportá la proporción de salidas con ese rasgo en cada grupo, no ejemplos sueltos.
5. Si encontrás una tendencia, evaluá datos complementarios, representaciones alternativas o una capa simbólica de barreras, y volvé a medir.

### 19. Medir el sesgo de género en embeddings
**Dónde:** C2P2 1:16:11, C2P2 1:16:44, C2P2 1:17:16, C2P2 1:17:53, C2P2 1:18:26, C2P2 1:18:58, C2P2 1:19:37, C2P2 1:20:09, C2P2 1:21:52, 2020-EPCD.1 15:17

**Contexto.** Se eligen palabras que representan lo femenino y lo masculino y se mide si palabras que no deberían tener género, como las profesiones, quedan más cerca de un grupo. Desde 2016 se sabe que enfermería queda asociada a lo femenino e ingeniería a lo masculino. En la notebook de exploración de sesgos en word embeddings de Laura y Luciana, electricista, economista, piloto y comerciante quedan más cerca de lo masculino, y cantante y florista de lo femenino. La mejor mitigación es tener mejores datos, pero los modelos los entrenan empresas que "no comparten valores con nosotros"; la alternativa puede ser no usarlos en tareas críticas.

**Por qué importa.** Si usás embeddings preentrenados en un sistema que toca personas (búsqueda de empleo, clasificación de CVs), heredás esas asociaciones.

**Cómo implementarlo.**
1. Definí dos listas de palabras que representen los polos (por ejemplo, ella, mujer, madre y él, hombre, padre).
2. Armá la lista de palabras que no deberían estar asociadas a ningún polo y que importan en tu dominio.
3. Calculá, para cada palabra, la diferencia de similitud con cada polo.
4. Ordená las palabras por esa diferencia y revisá las de los extremos con alguien del dominio.
5. Si las asociaciones afectan una tarea crítica, considerá no usar ese modelo para esa tarea.

```python
# Sugerencia: diferencia de similitud con dos polos, a partir de un diccionario palabra -> vector
import numpy as np

def coseno(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

def sesgo_por_palabra(emb, polo_f, polo_m, palabras):
    cf = np.mean([emb[w] for w in polo_f if w in emb], axis=0)
    cm = np.mean([emb[w] for w in polo_m if w in emb], axis=0)
    filas = [(w, coseno(emb[w], cf) - coseno(emb[w], cm)) for w in palabras if w in emb]
    return sorted(filas, key=lambda x: x[1])  # negativo: más cerca de lo masculino; positivo: de lo femenino
```

### 20. Incorporar diversidad en todo el ciclo de vida
**Dónde:** C2P2 1:25:53, C2P2 1:26:26, C2P2 1:26:59, C2P2 1:27:31, C2P2 1:28:06, C2P2 1:28:40, C2P2 1:29:13, C2P2 1:29:48, C2P2 1:30:23, C2P2 1:30:58, C2P2 1:31:32, C2P2 1:32:06

**Contexto.** "¿Cómo hacemos para que nuestros sistemas sean más éticos? Incorporando diversidad, sin ninguna duda", dice Laura, y lo baja a cada etapa: framing y cocreación, gobernanza participativa (no solo un focus group), requerimientos ("será un 1% de la población, pero tienen derecho"), diseño de categorías, desarrollo, pruebas adversarias y despliegue sin parches de "no lo habíamos pensado". Recuerda que la Convención Americana sobre Derechos Humanos tiene rango constitucional en Argentina y que hay consensos emergentes que hace 5 o 10 años no eran evidentes.

**Por qué importa.** Cambiar un sistema después del despliegue es caro y los incentivos económicos lo frenan. Lo que no se ve en el framing termina en un parche.

**Cómo implementarlo.**
1. Sumá a personas de los grupos afectados a la definición del problema, y no solo a una validación final.
2. Dales un lugar en la gobernanza del proyecto, con capacidad de frenar decisiones.
3. Escribí en los requerimientos los casos minoritarios que el sistema tiene que atender.
4. Revisá si tus categorías son las correctas o si las personas deberían poder definir las suyas.
5. Diseñá pruebas adversarias (fotos oscuras, baja resolución, acentos, discapacidades) en lugar de probar con tu propio caso.

### 21. Reescribir tu propia ética de trabajo
**Dónde:** C1P2 27:37, C1P2 28:12, C1P2 29:19, C1P2 29:55, C1P2 30:27, C1P2 30:58, C1P2 41:44, 2020-EPCD.1 0:37, 2020-EPCD.1 1:12, 2020-EPCD.1 1:48, 2020-EPCD.1 6:13, 2020-EPCD.1 6:47, 2020-EPCD.1 10:47, 2020-EPCD.1 11:21, 2020-EPCD.1 12:29, 2020-EPCD.1 13:03, 2020-EPCD.1 15:17

**Contexto.** En la clase 1, Luciana pide asumir que no somos objetivos ("como si eso existiera") y presenta la autoetnografía como herramienta para reflexionar y adaptar definiciones de ética. En el video de 2020 propone construir de forma iterativa una definición de ética para tu pequeña comunidad de trabajo, contestando preguntas sobre tu camino: cómo llegaste a la ciencia de datos, qué proyectos te marcaron, si pertenecés a una minoría o simpatizás con alguna, qué problemas éticos ves, cuál es la ética de quien te financia y a quién afecta económicamente tu trabajo. Ella pasa de "la computación debe ser usable para todos" a "la computación primero que nada debe respetar a todos y no dañarlos", y propone un tercer intento al terminar el curso.

**Por qué importa.** Desde un lugar de privilegio cuesta ver los problemas éticos; las preguntas obligan a mirar desde otro lado, y la definición resultante es la vara con la que vas a evaluar tus próximos proyectos.

**Cómo implementarlo.**
1. Escribí tu primera definición de ética laboral en dos o tres principios.
2. Contestá por escrito las seis preguntas del camino personal.
3. Reescribí la definición con lo que descubriste.
4. **Sugerencia:** agendá una revisión al terminar la materia y otra al empezar cada proyecto nuevo, como el tercer intento que propone Luciana.

### 22. Diseñar la revisión humana pensando en el sesgo de automatización
**Dónde:** C1P2 44:39, C1P2 45:12, C2P2 34:09

**Contexto.** Luciana define el sesgo de automatización como la tendencia de las personas a confiar de más en las recomendaciones de un sistema, y cuenta que no es lo mismo mostrarle a alguien la respuesta automática y preguntarle si está bien que pedirle que decida primero y después mostrarle qué habría dicho el sistema: en el segundo caso hay más desacuerdo. En la clase 2, Laura recuerda que al final decide un humano, y que lo que podés hacer es darle información que lo ayude a decidir mejor.

**Por qué importa.** Si la persona que revisa solo confirma lo que dice el sistema, la "supervisión humana" no frena ningún error.

**Cómo implementarlo.**
1. Identificá en tu flujo los puntos donde una persona revisa una salida del modelo.
2. Donde la decisión afecte derechos, pedí que la persona registre su decisión antes de ver la recomendación del sistema.
3. Mostrá la recomendación después y registrá cuándo la persona cambia de opinión.
4. **Sugerencia:** medí con qué frecuencia la persona coincide con el sistema; una coincidencia cercana al 100% es una señal de alerta.
5. **Sugerencia:** revisá esos registros junto con el monitoreo de incidentes de la sección 13.

---

## Glosario

### Términos
| Término | Qué quiere decir |
|---|---|
| Finalidad | Principio de la ley de datos personales: los datos se usan para el fin para el que se obtuvieron C1P1 26:52 |
| Minimización | Recolectar la mínima cantidad de datos necesaria para el objetivo C1P1 27:28 |
| Dato sensible | Origen racial o étnico, opiniones políticas, religión, salud o vida sexual, entre otros C1P1 24:41 |
| Data statement | Documentación de un dataset que ayuda a detectar y mitigar sesgos; es el práctico de la materia 2020-EPCD.3 1:06, C1P2 47:33 |
| Experto del dataset | Persona que conoce el dataset y contesta las preguntas del data statement C1P2 54:23 |
| Uso dual | Posibilidad de usar un dataset para algo distinto de lo planteado, con posible impacto negativo C1P2 45:52 |
| Autoetnografía | Reflexionar sobre tu historia y tu posición para encontrar daños y grupos que de otro modo no verías C1P2 30:27 |
| Variable protegida | Atributo que define los grupos que se comparan (raza, edad, género) C2P1 27:42 |
| Escenario de daño | Grupo protegido y privilegiado, qué se predice y qué error causa el daño C2P1 1:16:25 |
| Daño de asignación, de calidad de servicio y de representación | Los tres tipos de daño que se usan en la clase 2 C2P1 1:20:24 |
| Sesgo emergente | Sesgo que aparece al usar un modelo en otro contexto o en otro momento C1P2 43:30 |
| Sesgo de automatización | Tendencia a confiar de más en lo que recomienda un sistema C1P2 44:39 |
| Amplificación | Cuando el modelo exagera la proporción de la clase mayoritaria C2P1 45:27 |
| Macro average | Promedio por clase en el que cada clase vale lo mismo C2P1 1:04:42 |
| Tasa de falsos positivos | De los negativos reales, la proporción etiquetada como positiva C2P2 45:55 |
| Equal opportunity | Misma probabilidad, en cada grupo, de recibir correctamente la clase positiva C2P2 48:12 |
| Equalized odds | Igualdad de aciertos en la clase positiva y en la negativa a la vez C2P2 50:28 |
| Paridad demográfica | Misma proporción de clase positiva en cada grupo, sin importar si la merece C2P2 49:56 |
| Umbral de tolerancia | Valor de una métrica por encima del cual ningún modelo se acepta C2P2 51:38 |
| SHAP | Método que estima cuánto contribuye cada característica a una decisión C2P2 53:21 |
| What-If | Herramienta para probar contrafácticos C2P2 53:54 |
| Exploración sistemática | Auditar sin definición de error comparando grupos y reportando porcentajes C2P2 1:11:39 |
| Marca de agua | Señal que una empresa mete en lo que genera su modelo para detectarlo con su propio detector C1P1 1:19:26 |

### Nombres que la transcripción deforma
| Como aparece | Qué es probablemente |
|---|---|
| CONISET | CONICET |
| Pro Pública, Propública | ProPublica |
| Compas, compass | COMPAS |
| psychit learn | scikit-learn |
| Ecolizs, equalized ods | Equalized odds |
| con l'opportunity | Equal opportunity |
| lagranchianas, la granana | Lagrangianos (restricciones con multiplicadores de Lagrange) |
| Shap | SHAP |
| WTIF, Watif | What-If |
| AETAS, ACTAS, Equira | Dudoso; un framework europeo de fairness (podría ser Aequitas, sin confirmar) |
| Holistic | Dudoso; un framework de fairness |
| KIDA | Dudoso; el nombre de la notebook |
| Edia, Edy, Edas | Dudoso; herramienta de exploración de sesgos en embeddings |
| SINT id | SynthID |
| Detect GPT, TG GPT | DetectGPT |
| IUAI Act | Ley europea de IA (EU AI Act) |
| Clot, Cloud, Antropic, Entropic | Claude, Anthropic |
| Dipsic | DeepSeek |
| common craw | Common Crawl |
| AI GDAR, AI Gator | Dudoso; proyecto de clasificación de orientación sexual por la cara |
| crowdwers | Crowdworkers |
| convenio 108 Plus | Convenio 108+ |
| Jan Lecun | Yann LeCun |
| despixelizador | Reconstructor de alta resolución; origen inconsistente entre fuentes (**para verificar**) |
| esbio | Dudoso; ONG española de transparencia |
| friedmann y nissan brawn | Probablemente Friedman y Nissenbaum; dudoso |
