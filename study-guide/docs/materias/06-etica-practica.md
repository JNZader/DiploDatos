# Materia 6 — Ética Práctica en Ciencia de Datos

> **Idea rectora:** la ética no es una inspección que se agrega al final para autorizar un sistema ya decidido. Es una forma de definir el problema, justificar los datos, distribuir beneficios y cargas, elegir métricas, diseñar controles, escuchar a las personas afectadas y responder cuando algo sale mal.

Esta materia cierra el recorrido formal de la Diplomatura antes del proyecto integrador. Recupera lo aprendido sobre descripción, curación, aprendizaje supervisado, aprendizaje no supervisado y recuperación de información, pero cambia la pregunta principal. Ya no alcanza con preguntar **“¿funciona?”**. Hay que preguntar **“¿para quién funciona, en qué contexto, con qué costo, bajo qué valores, quién puede cuestionarlo y quién se hace responsable?”**.

En SAIJ, esta mirada es especialmente importante. Un fallo o un sumario puede ser públicamente accesible y, aun así, contener nombres, situaciones de salud, violencia, minoridad, datos familiares o combinaciones que permitan reidentificar personas. Un clasificador de **fuero** puede alcanzar buena exactitud promedio y perjudicar sistemáticamente a ciertos casos. Un ranking semántico puede volver invisibles decisiones minoritarias. Una respuesta RAG puede sonar jurídica y segura aunque haya recuperado evidencia insuficiente. Ninguno de esos problemas se resuelve con una frase genérica sobre “IA responsable”.

El capítulo es autocontenido. Los ejemplos numéricos son inventados y se usan para aprender a razonar. Las referencias al corpus SAIJ son hipótesis de trabajo o decisiones pendientes: **no informan mediciones reales**. Los resultados guardados dentro de notebooks del curso son evidencia preexistente y pendiente de reproducción; no se presentan como resultados de Javier.

---

## 0. Cómo estudiar esta materia

### 0.1 Recorrido didáctico

Cada bloque sigue esta secuencia:

~~~text
situación concreta
  → vocabulario ético
  → personas y relaciones de poder
  → beneficio, riesgo y daño
  → evidencia y métricas
  → tensión entre valores
  → control y responsable
  → transferencia a SAIJ
~~~

La secuencia evita dos atajos. El primero es reducir la ética a opiniones personales sin método. El segundo es reducirla a una métrica matemática que decide por nosotros. El análisis ético necesita valores explícitos, evidencia empírica, participación, deliberación y responsabilidades operativas.

### 0.2 Convenciones de evidencia

| Rótulo | Significado |
|---|---|
| **Teoría general** | Concepto explicativo que puede aplicarse a distintos proyectos. |
| **Ejemplo inventado** | Caso construido para calcular o deliberar; no describe SAIJ. |
| **Contexto de materiales del curso** | Marco incluido en las presentaciones, videos, prácticos o bibliografía local. Puede estar fechado. |
| **Dato suministrado por el usuario** | Información que se conserva como tal, por ejemplo la fecha del práctico. |
| **Resultado preexistente pendiente de reproducción** | Salida guardada en un notebook que no fue ejecutado en esta tarea. |
| **Hipótesis SAIJ** | Riesgo o comportamiento plausible que requiere medición y revisión. |
| **Decisión pendiente** | Elección que Javier y el equipo deben justificar con propósito, evidencia y consulta. |

### 0.3 Qué deberías poder hacer al terminar

Deberías poder:

1. distinguir ética, moral, derecho, cumplimiento y responsabilidad profesional;
2. separar afirmaciones descriptivas de afirmaciones normativas;
3. representar un sistema de datos como sistema sociotécnico;
4. construir un mapa de partes interesadas, poder y rendición de cuentas;
5. clasificar beneficios, riesgos y daños sin mirar solo el promedio;
6. rastrear sesgos a lo largo del ciclo de vida;
7. calcular e interpretar métricas de confusión por grupo;
8. explicar por qué las definiciones de equidad pueden entrar en conflicto;
9. razonar sobre privacidad, consentimiento, finalidad, minimización y reutilización;
10. producir un Data Statement y un registro de riesgos útil;
11. convertir un hallazgo de auditoría en remediación verificable;
12. diseñar revisión humana, abstención y contestabilidad reales;
13. analizar riesgos específicos de recuperación semántica y RAG;
14. declarar límites, incertidumbre y ausencia de evidencia sin inventar seguridad.

### Checkpoint 0

Antes de avanzar, explicá con tus palabras por qué una auditoría final no puede reparar por sí sola un objetivo injustificado, una muestra excluyente o una decisión de despliegue sin vía de apelación.

---

## 1. Ética desde primeros principios

### 1.1 Ética y moral

En el marco del curso, **ética** refiere a principios compartidos y discutidos en una comunidad para valorar comportamientos como aceptables o inaceptables. “No dañar”, “respetar la autonomía” y “distribuir beneficios y cargas con justicia” son ejemplos de principios. La palabra **moral** puede reservarse para convicciones, valores y deberes que una persona o grupo sostiene como propios.

La distinción no implica que una sea pública y la otra irrelevante. La experiencia moral de quienes diseñan, financian, usan o padecen un sistema influye en qué problemas se ven. La deliberación ética exige sacar esos supuestos a la luz, contrastarlos con otras perspectivas y justificar reglas comunes. Una persona puede sentir que una práctica es normal; una comunidad afectada puede mostrar que esa normalidad distribuye daño.

Tampoco existe una máquina neutral que reemplace la deliberación. Un modelo optimiza un objetivo elegido por personas. Los datos provienen de instituciones e historias. Los umbrales convierten errores en acciones. Una interfaz destaca algunas señales y oculta otras. La ética comienza al formular esas elecciones.

### 1.2 Derecho, cumplimiento y legitimidad ética

El **derecho** establece obligaciones, prohibiciones, competencias y remedios jurídicos. El **cumplimiento** organiza prácticas para respetar normas externas e internas. La **legitimidad ética** pregunta además si la acción es justificable frente a quienes reciben sus efectos.

Por eso:

~~~text
legalidad no implica automáticamente legitimidad ética
legitimidad ética no elimina obligaciones legales
cumplimiento mínimo no agota la responsabilidad profesional
~~~

Los materiales locales mencionan, entre otros ejemplos, la protección de datos personales en Argentina y marcos regulatorios internacionales. En esta guía se usan únicamente como **contexto del curso**. Antes de tomar decisiones operativas o jurídicas hay que verificar la vigencia, el alcance y la interpretación en fuentes oficiales actuales. Esta materia no brinda asesoramiento legal ni afirma que una norma concreta sea exhaustiva.

### 1.3 Responsabilidad profesional

La responsabilidad profesional aparece cuando el conocimiento técnico crea capacidad de influir sobre otras personas. No se limita a “hacer lo que pidió el cliente”. Incluye:

- anticipar impactos previsibles;
- revelar capacidades y limitaciones;
- no fabricar evidencia ni ocultar incertidumbre;
- buscar revisión profesional y de partes interesadas;
- trabajar dentro de la propia competencia;
- proteger privacidad, confidencialidad y seguridad;
- informar riesgos graves por canales adecuados;
- mitigar daño y aprender de incidentes;
- considerar no construir o no desplegar cuando el daño no puede controlarse.

El Código de Ética de ACM incluido en la bibliografía local refuerza una idea transversal: la computación es un servicio a la sociedad, todas las personas afectadas cuentan como partes interesadas y el bien público debe ocupar un lugar central. También vincula equidad con posibilidad de reparación: un proceso cuidadoso sigue siendo incompleto si nadie puede cuestionar una decisión injusta.

### 1.4 Afirmaciones descriptivas y normativas

Una afirmación **descriptiva** dice cómo es o cómo se comporta algo:

- “el 8 % de los documentos de esta muestra proviene del período P”;
- “el grupo A tiene una tasa de falsos negativos mayor que el grupo B”;
- “el ranking muestra más documentos de ciertos órganos en el top 10”.

Una afirmación **normativa** dice cómo debería ser o qué decisión corresponde:

- “la cobertura temporal debería ampliarse”;
- “esa diferencia de error es inaceptable”;
- “el ranking debe reservar exposición para jurisprudencia minoritaria”.

Los datos ayudan a evaluar hechos, pero no producen por sí solos el criterio normativo. Para pasar de “hay diferencia” a “hay injusticia” hacen falta propósito, gravedad, historia, posibilidad de elección, distribución de poder, alternativas y perspectivas afectadas. A la inversa, una preocupación ética sin evidencia puede no localizar el problema ni permitir corregirlo.

### 1.5 Ejemplo progresivo: accuracy y deber

**Ejemplo inventado.** Un clasificador de documentos alcanza 94 % de accuracy. La afirmación es descriptiva. Todavía no sabemos:

1. qué target intenta predecir;
2. cómo se construyeron las etiquetas;
3. quién recibe el beneficio;
4. qué significan los errores;
5. si el promedio oculta grupos pequeños;
6. si la predicción produce una acción;
7. si existe revisión y apelación;
8. si el sistema debería existir.

Si el modelo solo prioriza una cola interna reversible, un error puede causar demora. Si decide automáticamente qué documento queda fuera de una búsqueda jurídica, el mismo error puede ocultar evidencia. La métrica no cambió; cambió el significado sociotécnico.

### Checkpoint 1

Clasificá estas frases:

1. “El sistema se abstuvo en 12 de 100 consultas.”
2. “Debería abstenerse más cuando no hay fuentes.”
3. “La política interna exige registrar cada abstención.”
4. “Cumplir esa política vuelve ético al sistema.”

Las tres primeras son, respectivamente, descripción, norma propuesta y descripción de una regla. La cuarta es una inferencia inválida: el cumplimiento de una política puede ser necesario y aun así no resolver finalidad, daño o participación.

---

## 2. Los sistemas de datos son sociotécnicos

### 2.1 Más que modelo, dataset e interfaz

Un **sistema sociotécnico** combina componentes técnicos con personas, instituciones, reglas, incentivos y prácticas. Su unidad de análisis no es solo el modelo. Incluye:

- quién define el problema;
- quién financia y quién obtiene valor;
- cómo se producen y mantienen los datos;
- quién etiqueta y bajo qué instrucciones;
- qué infraestructura y proveedores intervienen;
- qué persona interpreta la salida;
- qué acción sigue a la salida;
- quién monitorea;
- quién puede reclamar;
- quién responde ante el daño.

Dos equipos pueden desplegar el mismo modelo y producir impactos distintos. Una recomendación presentada como “evidencia obligatoria” fomenta automatización; presentada como candidato incierto con fuentes y controles puede apoyar deliberación. Una revisión humana con treinta segundos y presión por aceptar no equivale a supervisión significativa.

### 2.2 Partes interesadas y personas afectadas

Una **parte interesada** es una persona o colectivo que influye en el sistema, recibe sus beneficios, soporta sus riesgos o tiene responsabilidades sobre él. Conviene distinguir:

- **usuarios directos**: interactúan con la herramienta;
- **personas afectadas**: reciben consecuencias aunque nunca usen la herramienta;
- **sujetos de datos**: aparecen en los datos;
- **creadores y mantenedores**: construyen dataset, modelo e interfaz;
- **decisores institucionales**: autorizan objetivos, presupuesto y despliegue;
- **expertos de dominio**: aportan conocimiento sustantivo;
- **equipos de control**: seguridad, privacidad, auditoría, legales, ética;
- **terceros**: proveedores de modelos, nube o datos;
- **público y comunidades**: pueden sufrir efectos colectivos o normativos.

El error frecuente es consultar solo a quien compra o usa. En un buscador SAIJ, una persona investigadora puede ser usuaria; una víctima nombrada en un documento es afectada y sujeto de datos; una comunidad estigmatizada puede sufrir daño representacional; el equipo técnico y la institución tienen poder de diseño.

### 2.3 Poder, participación y rendición de cuentas

**Poder** es capacidad de definir opciones, recursos, categorías y consecuencias. Preguntas mínimas:

1. ¿quién puede decir que no?
2. ¿quién puede cambiar el objetivo?
3. ¿quién entiende la explicación técnica?
4. ¿quién soporta el costo del error?
5. ¿quién puede acceder a registros?
6. ¿quién obtiene reparación?
7. ¿quién queda fuera de la conversación?

**Participación significativa** no es mostrar un prototipo terminado y pedir aprobación. Implica intervenir cuando las decisiones todavía pueden cambiar, contar con información comprensible, tiempo, apoyo, representación suficiente y respuesta documentada. No toda consulta genera consenso; debe registrarse qué tensión quedó abierta y quién decidió.

**Rendición de cuentas** requiere un sujeto con obligación y capacidad de responder. “El modelo lo hizo” no es responsable. Una matriz útil asigna para cada riesgo: propietario, aprobador, consultados, informados, evidencia, plazo y vía de escalamiento.

### 2.4 Ejemplo trabajado: mapa de poder para SAIJ

**Ejemplo ilustrativo, no descripción de una implementación real.** Supongamos una herramienta que recupera precedentes para una consulta.

| Actor | Interés o necesidad | Poder actual | Riesgo que soporta | Participación necesaria |
|---|---|---|---|---|
| Profesional jurídico usuario | Encontrar evidencia pertinente y verificable | Alto sobre consultas, medio sobre diseño | Omisión o falsa autoridad | Pruebas de uso, criterios de relevancia, reporte de errores |
| Persona nombrada en un fallo | Privacidad, contexto, no estigmatización | Bajo | Exposición y reidentificación | Política de datos, canal de corrección o restricción cuando corresponda |
| Víctimas, menores y grupos vulnerables | Evitar revictimización y daño acumulativo | Bajo | Material, simbólico y reputacional | Consulta mediada por especialistas y organizaciones pertinentes |
| Equipo de datos | Calidad, trazabilidad y mantenimiento | Alto sobre implementación | Presión por métricas simples | Autoridad para detener, documentar límites y escalar |
| Mentoría y responsables institucionales | Aprendizaje y utilidad del proyecto | Alto sobre alcance | Responsabilidad organizacional | Aprobar propósito, controles y no-usos |
| Revisor de dominio | Relevancia jurídica | Medio | Sobrecarga y automatización | Tiempo real, criterios claros, posibilidad de disentir |
| Proveedor de embeddings o generador | Servicio e infraestructura | Alto sobre componentes opacos | Riesgo comercial | Versionado, documentación, contrato y pruebas propias |

El mapa muestra una asimetría: quienes más pueden sufrir no necesariamente controlan el diseño. La respuesta no es prometer “human in the loop”. Hay que crear representación, límites de uso, minimización, registro, revisión y contestabilidad concretas.

### 2.5 Humanistic Toolkit: preguntas que cambian el diseño

Los materiales del curso presentan ejercicios de pensamiento de una **Caja de Herramientas Humanísticas**. El valor no está en adivinar una respuesta moral única, sino en desnaturalizar el proyecto. Un análisis útil puede preguntar:

- ¿qué mundo presupone la solución?
- ¿qué personas aparecen como problema y cuáles como autoridad?
- ¿qué historia produjo los datos?
- ¿qué cambia si quien diseña ocupa la posición de quien recibe el peor error?
- ¿qué ocurre si el sistema se usa a escala, por años o con otro propósito?
- ¿qué metáfora usamos: asistencia, predicción, vigilancia, clasificación, control?
- ¿qué alternativa no tecnológica fue descartada?
- ¿qué relación de dependencia crea el sistema?
- ¿qué sería una negativa legítima?

**Análisis ilustrativo.** Una propuesta dice: “RAG democratiza el acceso al derecho porque responde preguntas”. La caja obliga a separar:

1. **promesa**: menor costo de búsqueda;
2. **supuesto**: una respuesta generada equivale a acceso;
3. **ausencia**: no se menciona quién formula preguntas, qué corpus falta ni qué ocurre ante contradicción;
4. **poder**: el proveedor y el equipo seleccionan fuentes y reglas;
5. **escala temporal**: una omisión repetida puede consolidar una visión parcial;
6. **alternativa**: búsqueda con filtros, citas y guía humana sin generar respuesta;
7. **rediseño**: retrieval evaluado primero, respuesta con citas, abstención, aviso de límites y canal de contestación.

### Checkpoint 2

Un mapa de actores no está completo porque tenga muchas filas. Está completo para una decisión cuando muestra quién puede influir, quién recibe cada consecuencia, qué voz falta y qué mecanismo cambia el diseño.

---

## 3. Beneficios, riesgos y daños

### 3.1 Tres conceptos que no son sinónimos

Un **beneficio** es una mejora esperada para alguien: ahorrar tiempo, ampliar acceso, reducir carga o descubrir evidencia. Un **riesgo** combina un evento incierto con su probabilidad, exposición y gravedad. Un **daño** es la consecuencia negativa efectivamente sufrida o razonablemente anticipable.

Una frase como “el sistema beneficia a los usuarios” es incompleta. Hay que preguntar qué usuarios, comparado con qué alternativa y quién paga el costo. Un beneficio agregado puede coexistir con daño concentrado.

Un esquema simple para priorizar riesgos es:

\[
R = P \times I \times E
\]

donde:

- \(R\) es una prioridad orientativa de riesgo, no una verdad moral;
- \(P\) es probabilidad estimada del evento;
- \(I\) es impacto o gravedad;
- \(E\) es exposición: frecuencia, escala o duración.

La fórmula obliga a explicitar supuestos, pero no decide aceptabilidad. Un daño irreversible a pocas personas puede exigir control aunque el producto \(R\) sea menor que el de molestias frecuentes. Tampoco conviene fingir precisión: pueden usarse niveles bajo/medio/alto con justificación.

### 3.2 Ejes para clasificar daños

Los daños pueden ser:

- **individuales o colectivos**: afectan a una persona o a un grupo, institución o práctica social;
- **materiales o simbólicos**: cambian recursos, libertad, trabajo o seguridad; o refuerzan estereotipos, invisibilización y descrédito;
- **asignativos o representacionales**: distribuyen oportunidades/recursos; o representan a personas de manera degradante o sesgada;
- **de calidad de servicio**: el sistema funciona peor para ciertos grupos;
- **inmediatos o demorados**: ocurren en la decisión o se acumulan con el tiempo;
- **directos o indirectos**: siguen de la salida o de cómo otra persona la interpreta;
- **reversibles o irreversibles**;
- **observables o difíciles de detectar**.

Un mismo evento ocupa varios ejes. Un ranking que casi nunca muestra decisiones vinculadas con una comunidad puede reducir acceso profesional (material), volver su jurisprudencia menos visible (representacional), afectar al colectivo y acumularse lentamente.

### 3.3 Ejemplo de representación sesgada

**Ejemplo inventado.** Un archivo contiene 1.000 decisiones: 700 de dos tribunales con digitalización completa y 300 distribuidas entre veinte tribunales con publicación irregular. Un modelo aprende temas predominantes.

La inferencia incorrecta sería: “los temas frecuentes representan la actividad judicial”. La muestra representa primero **disponibilidad documental**. Los tribunales mejor digitalizados pesan más; períodos con fallas de carga pesan menos; documentos no publicados no existen para el modelo.

Acciones razonables:

1. documentar fuente y mecanismo de inclusión;
2. comparar cobertura por tribunal y tiempo;
3. no usar frecuencia documental como frecuencia social sin denominador;
4. estratificar evaluación;
5. buscar fuentes faltantes;
6. limitar la afirmación si la cobertura no puede corregirse.

No hace falta demostrar intención discriminatoria para reconocer riesgo de representación.

### 3.4 Ejemplo SAIJ: accuracy sola es insuficiente

**Escenario de decisión, no resultado real.** Un clasificador propone **fuero** para enrutar documentos a revisión. Logra 96 % de accuracy. Los errores restantes se concentran en documentos de violencia familiar con redacción ambigua, y el ruteo equivocado demora su revisión.

Accuracy no alcanza porque:

- el target **fuero** es una construcción del dataset y puede mezclar competencia, órgano, etiqueta editorial o regla de negocio;
- la clase afectada puede ser pequeña;
- un falso negativo puede tener costo distinto de un falso positivo;
- los documentos pueden contener víctimas o menores;
- una demora repetida puede ser daño material;
- el sistema puede inducir confianza excesiva;
- hace falta vía de corrección y responsable.

La evaluación debe combinar métricas por clases y grupos éticamente justificados, revisión de casos, tiempos, severidad, incertidumbre y control operativo. Si no existe evidencia suficiente, la acción correcta puede ser **no automatizar la decisión**.

### 3.5 Registro inicial de riesgos

| ID | Evento | Afectados | Daño | Causa posible | Control preventivo | Señal | Responsable |
|---|---|---|---|---|---|---|---|
| E-01 | Documento sensible aparece en resultado amplio | Personas nombradas | Privacidad y reputación | Indexación sin minimización | Política de campos y acceso | Queja o detección de PII | Responsable de datos |
| E-02 | Caso relevante no aparece | Usuario y personas vinculadas | Omisión de evidencia | Cobertura o ranking | Baseline, recall y revisión | Consultas sin resultados | Responsable de retrieval |
| E-03 | Respuesta afirma más que las fuentes | Usuario y terceros | Falsa autoridad | Generación no anclada | Citas, abstención, verificación | Afirmación sin soporte | Responsable de RAG |

El registro no reemplaza análisis. Hace visible quién debe actuar y qué evidencia permitirá saber si el control funciona.

### Checkpoint 3

Cuando una mejora promedio empeora un daño grave para un grupo pequeño, no existe una regla matemática universal. Hay que hacer visible la distribución, justificar prioridades, explorar alternativas y documentar la decisión.


---

## 4. Sesgos a lo largo del ciclo de vida

### 4.1 Sesgo no significa simplemente “dato incorrecto”

En estadística, “sesgo” puede nombrar una diferencia sistemática entre un estimador y el valor que pretende estimar. En ética de sistemas de datos, interesa además la discriminación sistemática e injusta contra personas o grupos. No toda diferencia es injusta y no toda injusticia aparece como diferencia de una métrica. El análisis debe conectar patrón, contexto y daño.

Los materiales del curso insisten en que los datos no son objetivos por el mero hecho de ser números. Son rastros de procesos: quién fue observado, qué institución registró, qué categoría existía, qué pregunta se hizo y qué quedó fuera. Un sesgo puede aparecer antes del dataset y ser amplificado por el sistema.

### 4.2 Mapa del ciclo de vida

| Etapa | Pregunta ética | Sesgo posible | Señal |
|---|---|---|---|
| Historia y definición | ¿Qué desigualdad previa se convierte en dato? | Histórico o preexistente | El target refleja una práctica desigual |
| Muestreo | ¿Quién puede aparecer? | Representación o selección | Grupos, tribunales o períodos ausentes |
| Medición | ¿El indicador representa el concepto? | Medición | Proxy débil o instrumento desigual |
| Etiquetado | ¿Quién define la verdad? | Etiqueta | Desacuerdo oculto o guía ambigua |
| Agregación | ¿Una regla sirve para subpoblaciones distintas? | Agregación | Buen promedio, mal subgrupo |
| Representación | ¿Qué rasgos conserva el vector? | Feature/embedding | Estereotipos o señales institucionales |
| Modelado | ¿Qué patrón favorece el algoritmo? | Inductivo o amplificación | Mayoría reforzada |
| Evaluación | ¿Qué incentiva la métrica? | Evaluación | Accuracy oculta clases pequeñas |
| Despliegue | ¿Cómo se usa la salida? | Emergente o contextual | Cambio de población o uso |
| Interacción | ¿La persona confía, corrige o ignora? | Automatización | Aceptación rutinaria |
| Retroalimentación | ¿La salida crea los datos futuros? | Feedback loop | La predicción se vuelve aparente confirmación |

La tabla evita la excusa “el sesgo está en los datos”. A veces está en los datos; la decisión profesional sigue siendo qué construir con ellos, qué recolectar, qué no inferir y cómo limitar el uso.

### 4.3 Ejemplo trabajado: sesgo de muestreo

**Ejemplo inventado.** Queremos evaluar un buscador sobre 200 consultas históricas. Elegimos las consultas más frecuentes del registro de uso. El 90 % proviene de un grupo experto que conoce la terminología exacta; el 10 % usa lenguaje cotidiano.

El sistema obtiene alto rendimiento global. Sin embargo, la muestra subrepresenta consultas de personas no expertas, búsquedas con errores ortográficos y temas que nunca se consultaron porque el sistema anterior no los hacía visibles.

El sesgo puede rastrearse así:

1. **mecanismo:** conveniencia; se eligieron consultas disponibles;
2. **grupo ausente:** personas con otra experiencia o vocabulario;
3. **impacto:** la evaluación premia coincidencia léxica experta;
4. **error normativo:** declarar que el buscador “funciona para la ciudadanía”;
5. **remediación:** definir población, incorporar consultas por perfiles, documentar cobertura, reportar resultados estratificados y limitar la afirmación.

Agregar ejemplos hasta balancear una tabla no garantiza representatividad. Hace falta entender cómo se generó cada estrato y qué población pretende sostener la conclusión.

### 4.4 Etiquetas y el caso de fuero

Una etiqueta puede ser correcta respecto de un procedimiento de anotación y aun así no representar una categoría natural. Para **fuero** hay que averiguar:

- fuente exacta de la etiqueta;
- nivel: documento, expediente, órgano, competencia o clasificación editorial;
- reglas y excepciones;
- cambios históricos;
- casos múltiples o ambiguos;
- quién resolvió desacuerdos;
- uso previsto;
- consecuencias de cada error.

Si el nombre del tribunal forma parte de las features, el modelo puede aprender una relación administrativa en vez de contenido. Eso puede ser útil para imputación y engañoso para generalización. Si el target reproduce una decisión institucional discutible, mejorar accuracy reproduce mejor esa decisión. La pregunta ética y científica es qué queremos aprender y para qué.

### 4.5 Agregación y despliegue

El **sesgo de agregación** aparece cuando una sola relación modela poblaciones con patrones distintos. No se resuelve automáticamente entrenando un modelo por grupo: los grupos pueden ser pequeños, las categorías pueden esencializar identidades y la separación puede producir nuevos daños. Se comparan alternativas y se justifica el tratamiento.

El **sesgo emergente** aparece cuando el contexto de uso difiere del de creación. Cambian vocabulario, prácticas, usuarios, períodos, instituciones o consecuencias. Un modelo evaluado sobre fallos completos puede fallar sobre sumarios; un embedding general puede privilegiar sentidos no jurídicos; una política apropiada para investigación puede ser inaceptable para decisión operativa.

### 4.6 Feedback loops

Un ciclo de retroalimentación ocurre cuando la salida modifica qué datos se observarán después. Si el buscador muestra más documentos de ciertos órganos, los usuarios los citan, validan y consultan más. El registro futuro parece confirmar que esos documentos eran los más relevantes. La causa es parcialmente la exposición creada por el ranking.

Para detectar el ciclo:

1. separar datos previos y posteriores al despliegue;
2. registrar exposición, no solo clics;
3. reservar exploración o revisión de cobertura;
4. medir qué queda sistemáticamente fuera;
5. permitir reportes de omisión;
6. evitar tratar interacción como relevancia objetiva.

### Checkpoint 4

Para cada error preguntá: ¿nació en la historia, la muestra, la medición, la etiqueta, el algoritmo, la métrica, la interfaz o la acción? La respuesta puede incluir varias etapas.

---

## 5. Atributos sensibles, proxies e interseccionalidad

### 5.1 Atributo protegido o sensible

Un atributo protegido o sensible identifica una característica que merece atención por historia de discriminación, intimidad, vulnerabilidad o marco aplicable. La lista depende del contexto y no se agota en lo disponible en una tabla. Raza, etnia, sexo, género, orientación sexual, salud, discapacidad, edad, religión, opiniones políticas, situación migratoria o ubicación pueden ser relevantes según el uso.

No conviene agregar atributos por curiosidad. Medir equidad puede requerir datos sensibles; recolectarlos puede aumentar riesgo de privacidad. La decisión debe justificar finalidad, acceso, retención, consentimiento o base válida, seguridad, tamaño de grupos y eliminación. “No tenemos atributo protegido” tampoco prueba ausencia de daño.

### 5.2 Proxies

Un **proxy** es una variable que permite inferir o aproximar otra característica. Puede ser explícitamente elegida o actuar de manera accidental. Código postal, escuela, apellido, vocabulario, horario, dispositivo o institución pueden correlacionarse con origen, ingresos, género o vulnerabilidad.

Quitar la columna sensible no vuelve ciego al sistema. Otras variables pueden reconstruirla. A la vez, prohibir todo proxy puede quitar información legítima. La pregunta es si la variable aporta señal pertinente, qué relación histórica contiene y qué daño produce.

### 5.3 Ejemplo trabajado: tribunal como proxy

**Ejemplo inventado.** Un clasificador usa tribunal de origen para predecir **fuero**. La variable mejora mucho la accuracy. También puede actuar como proxy de región, disponibilidad digital, práctica administrativa y composición de casos.

Análisis:

1. **utilidad técnica:** el tribunal está asociado al target;
2. **riesgo:** el modelo aprende origen institucional y no texto;
3. **daño posible:** falla al cambiar de tribunal o naturaliza desigualdades de carga;
4. **prueba:** comparar desempeño con y sin variable, por tribunal y tiempo;
5. **control:** documentar propósito, limitar inferencias, evaluar cambio de dominio y no usar la predicción como verdad jurídica;
6. **decisión:** puede aceptarse para ruteo interno acotado y rechazarse para inferir contenido.

La comparación no decide sola. Hace visible qué compra la mejora y qué dependencia crea.

### 5.4 Interseccionalidad

La **interseccionalidad** recuerda que las experiencias no siempre se explican sumando categorías aisladas. Mujeres, personas mayores, habitantes de una región o víctimas no son grupos homogéneos. Una desventaja puede aparecer en la intersección y desaparecer en promedios separados.

Pero cruzar todas las variables produce celdas diminutas, inestabilidad y mayor riesgo de reidentificación. El procedimiento responsable es:

1. partir de hipótesis de daño y conocimiento social, no de búsqueda indiscriminada;
2. elegir intersecciones pertinentes;
3. reportar tamaños y incertidumbre;
4. proteger acceso y publicación;
5. combinar métricas con revisión cualitativa;
6. declarar cuando no hay evidencia suficiente.

### Checkpoint 5

Un atributo sensible no es solo una columna. Puede estar ausente, mal medido, inferido por proxies o ser relevante en una intersección. Medirlo requiere la misma ética que se intenta evaluar.

---

## 6. Matriz de confusión por grupo

### 6.1 Del resultado individual a las tasas

Para un problema binario definimos:

- **TP**: verdaderos positivos; casos positivos correctamente predichos;
- **FN**: falsos negativos; casos positivos predichos como negativos;
- **FP**: falsos positivos; casos negativos predichos como positivos;
- **TN**: verdaderos negativos; casos negativos correctamente predichos.

“Positivo” no significa bueno. Es la clase elegida como (Y=1). Antes de calcular hay que traducir cada celda a una consecuencia. En un detector de información sensible, un FN deja texto sensible expuesto; un FP oculta texto que no era sensible. En un ruteo, ambos generan cargas distintas.

### 6.2 Fórmulas fundamentales

La tasa de verdaderos positivos es:

\[
TPR = \frac{TP}{TP+FN}
\]

- (TPR) mide sensibilidad o recall de la clase positiva;
- (TP) cuenta positivos detectados;
- (FN) cuenta positivos omitidos;
- (TP+FN) es el total de positivos reales.

La tasa de falsos negativos es:

\[
FNR = \frac{FN}{TP+FN} = 1-TPR
\]

- (FNR) es la proporción de positivos reales omitidos;
- el denominador vuelve a ser la población realmente positiva.

La tasa de falsos positivos es:

\[
FPR = \frac{FP}{FP+TN}
\]

- (FPR) mide qué fracción de negativos reales fue marcada positiva;
- (FP+TN) es el total de negativos reales.

El valor predictivo positivo es:

\[
PPV = \frac{TP}{TP+FP}
\]

- (PPV), también llamado precision de la clase positiva, mira predicciones positivas;
- (TP+FP) es todo lo que el modelo marcó positivo;
- responde cuántas predicciones positivas eran correctas.

TPR y PPV tienen denominadores distintos. Confundirlos cambia la pregunta ética.

### 6.3 Ejemplo completo calculado a mano

**Ejemplo inventado.** Un sistema marca documentos para revisión especial. Se evalúan dos grupos definidos porque existe una hipótesis previa de daño y autorización para ese análisis.

| Grupo | TP | FN | FP | TN | Total |
|---|---:|---:|---:|---:|---:|
| A | 36 | 4 | 12 | 48 | 100 |
| B | 18 | 12 | 3 | 27 | 60 |

**Grupo A**

\[
TPR_A=\frac{36}{36+4}=\frac{36}{40}=0{,}90
\]

Detecta 90 % de los positivos reales.

\[
FNR_A=\frac{4}{40}=0{,}10
\]

Omite 10 % de los positivos reales.

\[
FPR_A=\frac{12}{12+48}=\frac{12}{60}=0{,}20
\]

Marca incorrectamente 20 % de los negativos reales.

\[
PPV_A=\frac{36}{36+12}=\frac{36}{48}=0{,}75
\]

Tres de cada cuatro marcas positivas son correctas.

**Grupo B**

\[
TPR_B=\frac{18}{18+12}=\frac{18}{30}=0{,}60
\]

Detecta 60 % de los positivos reales.

\[
FNR_B=\frac{12}{30}=0{,}40
\]

Omite 40 % de los positivos reales.

\[
FPR_B=\frac{3}{3+27}=\frac{3}{30}=0{,}10
\]

Marca incorrectamente 10 % de los negativos reales.

\[
PPV_B=\frac{18}{18+3}=\frac{18}{21}≈0{,}857
\]

Aproximadamente 85,7 % de las marcas positivas son correctas.

**Interpretación.** B tiene mejor FPR y PPV, pero peor TPR y FNR. Si el daño más grave es omitir positivos, B está peor. Si revisar falsos positivos consume un recurso escaso o causa daño, A está peor. No existe una frase “B es más justo” sin especificar acción, severidad, alternativas y legitimidad de los grupos.

### 6.4 Qué falta en una tabla de tasas

La tabla no muestra:

- intervalos de incertidumbre;
- heterogeneidad dentro del grupo;
- intersecciones;
- gravedad individual;
- errores de etiqueta;
- cambio temporal;
- si la acción es reversible;
- si la agrupación es legítima;
- si las personas pueden apelar.

Una diferencia puede ser ruido; una igualdad puede ocultar daño común a todos. Siempre se reportan conteos junto a tasas.

---

## 7. Definiciones de equidad y sus tensiones

### 7.1 Notación

Usaremos:

- (A): atributo o grupo bajo análisis;
- (Y): resultado real o etiqueta de referencia;
- (Y_pred): predicción binaria;
- (S): score entre 0 y 1;
- (a) y (b): dos grupos comparados;
- (P(evento)): probabilidad o proporción estimada.

Las ecuaciones son criterios diagnósticos. No son certificados universales de justicia.

### 7.2 Paridad estadística o demográfica

La paridad demográfica pide:

\[
P(Y_pred=1 | A=a)=P(Y_pred=1 | A=b)
\]

Símbolo por símbolo:

- (Y_pred=1) es recibir la predicción positiva;
- la barra | significa “condicionado a”;
- (A=a) y (A=b) identifican grupos;
- (P) es la proporción de predicciones positivas dentro de cada grupo.

Pregunta: **¿los grupos reciben resultados positivos a la misma tasa?**

Puede ser relevante cuando la salida asigna oportunidades y el target histórico está contaminado. Puede ser inadecuada si existen diferencias legítimas respecto del objetivo o si fuerza decisiones dañinas. Igualar tasas no garantiza igualdad de calidad, proceso o impacto.

### 7.3 Igualdad de oportunidades

La igualdad de oportunidades pide TPR igual:

\[
P(Y_pred=1 | Y=1, A=a)=P(Y_pred=1 | Y=1, A=b)
\]

- (Y=1) restringe a quienes realmente pertenecen a la clase positiva;
- se compara la probabilidad de detectarlos;
- equivale a igualar TPR y, por complemento, FNR.

Pregunta: **entre quienes deberían recibir el positivo según la referencia, ¿los grupos tienen igual oportunidad de obtenerlo?**

Depende de que (Y) sea una referencia defendible. Si la etiqueta reproduce discriminación, igualar acceso a esa etiqueta no resuelve la injusticia.

### 7.4 Odds igualadas

Equalized odds pide simultáneamente:

\[
P(Y_pred=1 | Y=y, A=a)=P(Y_pred=1 | Y=y, A=b)
para y en {0,1}
\]

- (y=1) compara TPR;
- (y=0) compara FPR;
- ({0,1}) indica las dos clases reales.

Pregunta: **¿el sistema tiene iguales tasas de acierto positivo y falsa alarma entre grupos?**

Es más exigente que igualdad de oportunidades. Puede requerir umbrales distintos o pérdida de rendimiento. Aun satisfecha, no garantiza buen nivel absoluto: dos grupos pueden tener TPR igualmente bajo.

### 7.5 Paridad predictiva

La paridad predictiva pide PPV igual:

\[
P(Y=1 | Y_pred=1, A=a)=P(Y=1 | Y_pred=1, A=b)
\]

- (Y_pred=1) restringe a predicciones positivas;
- (Y=1) pregunta cuántas eran correctas;
- compara confianza práctica de una predicción positiva.

Pregunta: **cuando el sistema dice positivo, ¿esa afirmación tiene la misma confiabilidad entre grupos?**

Puede importar si una persona decisora interpreta el positivo como evidencia. No controla cuántos positivos reales quedaron afuera.

### 7.6 Calibración

Un score está calibrado por grupo si, aproximadamente:

\[
P(Y=1 | S=s, A=a)=s
\]

- (S=s) agrupa casos con score cercano a (s);
- (A=a) restringe al grupo;
- el lado izquierdo es la frecuencia real de positivos;
- el lado derecho es el score anunciado.

Si (s=0{,}70), alrededor de 70 % de los casos de ese grupo con score cercano a 0,70 deberían ser positivos. Calibración no significa que el score cause el resultado ni que sea ético usarlo.

### 7.7 Por qué los criterios pueden entrar en conflicto

Cuando los grupos tienen **tasas base** distintas, un predictor imperfecto generalmente no puede satisfacer a la vez calibración, odds igualadas y paridad predictiva. La tasa base es:

\[
BR_a=P(Y=1 | A=a)
\]

- (BR_a) es proporción de positivos reales en el grupo (a);
- (Y=1) es la referencia positiva;
- (A=a) define el grupo.

La tasa base puede reflejar diferencias reales, muestreo, medición o desigualdad histórica. No debe naturalizarse.

**Ejemplo razonado.** Supongamos dos políticas de umbral:

- Política X iguala TPR en 0,80, pero produce PPV de 0,60 en A y 0,80 en B.
- Política Z iguala PPV en 0,75, pero produce TPR de 0,90 en A y 0,65 en B.

Si el daño principal es negar una oportunidad a quien cumple (Y=1), X puede ser preferible. Si una predicción positiva dispara una intervención riesgosa y debe significar lo mismo, Z puede ser preferible. También pueden rechazarse ambas, mejorar datos, cambiar la acción o no usar el score.

La incompatibilidad no es un fracaso de la matemática. Hace visible que “equidad” contenía objetivos normativos distintos.

### 7.8 Grupos pequeños, incertidumbre e inestabilidad

Si un grupo tiene 5 positivos y el modelo omite 1, (FNR=1/5=0{,}20). Si omite 2, (FNR=0{,}40). Un solo caso duplica la tasa. Por eso:

1. reportá numeradores y denominadores;
2. estimá intervalos o variación por remuestreo cuando corresponda;
3. repetí por períodos y particiones;
4. evitá publicar celdas reidentificables;
5. combiná cuantitativo y cualitativo;
6. no concluyas “no hay diferencia” por falta de potencia;
7. considerá agrupar solo si conserva significado;
8. declarate sin evidencia suficiente cuando corresponda.

En SAIJ, desagregar por órgano, tiempo, tipo documental y grupos sensibles puede dejar celdas pequeñas. El análisis debe estar motivado por daño, no por explorar identidades indiscriminadamente.

### Checkpoint 7

Elegí primero la consecuencia que importa; luego la métrica. Si se elige una métrica porque “es estándar”, se está ocultando una decisión normativa dentro de una costumbre técnica.

---

## 8. Privacidad, consentimiento y reutilización

### 8.1 Conceptos operativos

- **Privacidad:** capacidad y derecho de las personas para controlar o comprender qué información se recolecta y usa sobre ellas.
- **Consentimiento:** autorización libre, informada, específica y revisable bajo condiciones pertinentes; no es una casilla mágica.
- **Limitación de finalidad:** usar datos para propósitos compatibles y explícitos.
- **Minimización:** recolectar, procesar y retener solo lo necesario.
- **Proveniencia:** registro de origen, transformaciones, custodios y condiciones.
- **Confidencialidad:** impedir usos o divulgaciones no autorizados de información en custodia.
- **Seguridad:** medidas técnicas y organizativas contra acceso, modificación, pérdida o abuso.
- **Reidentificación:** vincular datos supuestamente anónimos con personas, solos o combinados.
- **Uso dual:** reutilización con impacto negativo aunque el objetivo inicial fuera legítimo.

Privacidad y confidencialidad se relacionan pero no son iguales. Una institución puede proteger muy bien una base que nunca debió recolectar. También puede recolectar legítimamente y luego fallar en seguridad.

### 8.2 Público no significa éticamente libre

Que un documento sea accesible en la web no demuestra:

- que fue producido para entrenamiento;
- que las personas esperaban indexación masiva;
- que toda reutilización es compatible;
- que no contiene filtraciones o datos que debieron corregirse;
- que una nueva agregación no aumenta daño;
- que la licencia o términos permiten el uso;
- que la exposición en respuesta generada equivale a acceso en fuente.

La diferencia entre **públicamente accesible** y **públicamente destinado a ese uso** es clave. La evaluación combina marco aplicable, expectativas, contexto, sensibilidad, escala, finalidad y alternativas. En SAIJ, la disponibilidad documental no elimina riesgos para víctimas, menores, personas vulnerables o nombradas.

### 8.3 Reidentificación por combinación

Eliminar nombres es insuficiente. Fecha precisa, tribunal, localidad, delito poco frecuente, edad y relación familiar pueden formar un cuasi-identificador. Un buscador que combina filtros puede localizar un caso único. Un embedding también puede acercar documentos por detalles sensibles aunque esos detalles no se muestren como columnas.

Prueba conceptual:

1. ¿qué campos identifican directamente?
2. ¿qué combinaciones vuelven único un registro?
3. ¿qué fuentes externas permiten vincularlo?
4. ¿qué muestra un snippet?
5. ¿qué registra el log de consultas?
6. ¿quién tiene acceso?
7. ¿cuánto tiempo se conserva?

Anonimización no es un estado binario. Es un control contextual que puede degradarse.

### 8.4 Minimización para SAIJ

Una estrategia por capas podría separar:

- texto original restringido;
- versión procesada con campos sensibles reducidos;
- metadatos mínimos para filtros;
- representaciones vectoriales con acceso controlado;
- snippets limitados;
- logs seudonimizados y con retención definida.

Cada capa necesita propósito, responsable y prueba. Los embeddings no son automáticamente anónimos: pueden memorizar o codificar información. Tampoco conviene eliminar contexto necesario para comprender un fallo. Minimizar es reducir lo innecesario, no destruir valor jurídico sin análisis.

### 8.5 Dual use

Un corpus pensado para investigación puede usarse para perfilar personas, localizar víctimas, automatizar vigilancia o inferir características. Un modelo de desidentificación puede proteger datos o facilitar detección de entidades para extracción. Un ranking puede apoyar estudio o amplificar acoso.

El Data Statement debe registrar usos previstos, excluidos y plausibles usos indebidos. Los controles pueden incluir acceso, autenticación, límites de consulta, monitoreo, revisión de solicitudes, restricciones de exportación, respuesta a incidentes y retirada de versiones.

### Checkpoint 8

Antes de decir “los datos son públicos”, completá: ¿públicos dónde, para quién, con qué expectativa, bajo qué condiciones y qué cambia al agregarlos, vectorizarlos o generar una respuesta?


---

## 9. Data Statements y Datasheets

### 9.1 Documentar para decidir, no para decorar

Un Data Statement o Datasheet hace explícito cómo se creó un dataset, qué contiene, qué no contiene, para qué puede usarse y qué riesgos deja. Su valor no es completar una plantilla después del proyecto. Es obligar al equipo a reflexionar antes, durante y después de la recolección.

Las propuestas de Bender y Friedman y de Gebru y colegas, incluidas en la bibliografía local, comparten objetivos:

- aumentar transparencia y rendición de cuentas;
- facilitar reproducibilidad;
- evitar desajustes entre datos y despliegue;
- ayudar a creadores a revisar supuestos;
- dar a consumidores información para decidir;
- identificar daño y mal uso;
- mantener documentación junto con versiones.

No son una solución completa contra sesgo. Una descripción honesta habilita mejores decisiones; no vuelve aceptable un dataset inadecuado.

### 9.2 Secciones del ciclo de vida

Una documentación robusta incluye:

1. **motivación:** quién creó, para qué, con qué financiación y qué alternativas existían;
2. **composición:** unidad, cantidad, variables, anotaciones, ausencias, errores y grupos afectados;
3. **recolección:** fuente, período, mecanismo de muestreo, participantes, compensación y consentimiento;
4. **preprocesamiento y etiquetado:** limpieza, exclusiones, transformación, instrucciones, desacuerdo y software;
5. **usos previstos:** tareas y contextos defendibles;
6. **usos excluidos:** decisiones o poblaciones para las que no debe usarse;
7. **distribución:** acceso, licencia, restricciones, terceros y versiones;
8. **mantenimiento:** responsable, actualizaciones, errores, retirada y contacto;
9. **limitaciones:** cobertura, incertidumbre, cambios y conocimiento faltante;
10. **personas afectadas:** sujetos de datos, grupos potencialmente dañados y mecanismos de consulta o reparación.

Si una respuesta es desconocida, se escribe “desconocido” y se explica la consecuencia. Inventar certeza destruye el propósito.

### 9.3 Data Statements frente a Datasheets

En esta materia usamos **Data Statement** para el práctico y la plantilla local. La propuesta de Bender y Friedman presta especial atención a datos lingüísticos: variedad de lengua, características de hablantes y anotadores, situación comunicativa, curación y uso. **Datasheets for Datasets** amplía preguntas a todo el ciclo de vida: motivación, composición, recolección, preprocesamiento, usos, distribución y mantenimiento.

No hace falta elegir un ganador. Para SAIJ conviene usar la plantilla del práctico y enriquecerla con:

- versión y fecha de extracción;
- cobertura por tiempo y órgano;
- unidad lingüística;
- criterios de inclusión;
- proceso de anonimización o exposición;
- anotación de **fuero**;
- transformaciones para retrieval;
- usos excluidos;
- canal de mantenimiento.

### 9.4 Mini Data Statement de SAIJ

**Ejemplo parcial y deliberadamente incompleto. No describe hechos verificados.**

| Campo | Respuesta ilustrativa |
|---|---|
| Nombre | Corpus SAIJ para mentoría — versión pendiente |
| Propósito | Aprendizaje, exploración y evaluación de clasificación y retrieval; no decisión jurídica automatizada |
| Unidad | Documento o sumario; debe definirse y versionarse |
| Fuente | Fuente SAIJ indicada por el proyecto; condiciones y fecha deben verificarse |
| Cobertura | Períodos, órganos, fueros y disponibilidad: pendiente de perfil empírico |
| Personas | Puede contener nombres y situaciones sensibles; requiere revisión |
| Etiquetas | **Fuero** como campo construido; origen, reglas y ambigüedad pendientes |
| Preprocesamiento | Limpieza, duplicados, segmentación y campos eliminados: documentar por versión |
| Uso previsto | Análisis educativo, baseline, evaluación de retrieval y apoyo revisado |
| Uso excluido | Decisión automática, perfilamiento de personas, asesoramiento legal o afirmaciones sin fuentes |
| Riesgos | Reidentificación, omisión de evidencia, exposición desigual, falsa autoridad |
| Mantenimiento | Responsable, canal de corrección, cambios y retirada: pendiente |

La honestidad de los “pendiente” es parte de la calidad. Cada uno se convierte en tarea con responsable.

### 9.5 El práctico de Ética

La fecha de entrega del práctico es **1 de octubre de 2026 — dato suministrado por el usuario**. No se toma de diapositivas históricas, que pueden mostrar otras cohortes.

La metodología local propone una entrevista semiestructurada a una persona experta del dataset, un borrador revisado y un resumen final. El grupo debe preservar las preguntas de la plantilla y explicar cuando una información no está disponible. La entrevista evita que el equipo técnico suponga saber cómo nació la base.

### 9.6 Plan ordenado para el práctico SAIJ

1. Definir grupo, roles y responsable de versión.
2. Copiar la plantilla sin alterar su formato exigido.
3. Identificar a la persona experta y enviar preguntas con anticipación.
4. Reunir hechos ya documentados y marcar vacíos.
5. Conducir la entrevista distinguiendo certeza, estimación y desconocido.
6. Completar motivación, composición, recolección, personas y usos.
7. Agregar riesgos SAIJ: cobertura, datos sensibles, **fuero**, retrieval y RAG.
8. Redactar usos excluidos concretos.
9. Compartir borrador con la persona experta.
10. Resolver comentarios o registrar desacuerdo.
11. Escribir al final el resumen dentro del límite solicitado por la plantilla.
12. Verificar extensión, preguntas, metadatos, trazabilidad y fecha.
13. Entregar por el canal oficial confirmado para la cohorte.

### 9.7 Checklist acotado

- [ ] Nombre, fuente, versión, licencia y responsables.
- [ ] Propósito y financiación.
- [ ] Unidad, composición, tamaño y ejemplos seguros.
- [ ] Inclusiones, exclusiones y períodos.
- [ ] Etiquetas, anotadores y desacuerdos.
- [ ] Personas, sensibilidad, consentimiento y reidentificación.
- [ ] Preprocesamiento y software.
- [ ] Usos previstos y excluidos.
- [ ] Distribución, acceso y mantenimiento.
- [ ] Afectados, daños, controles y vacíos.
- [ ] Revisión de la persona experta.
- [ ] Resumen final y fecha del 1 de octubre de 2026.

### Checkpoint 9

Un buen Data Statement permite a alguien decidir **no usar** el dataset. Si solo funciona como publicidad, no cumple su función ética.

---

## 10. Participación y consulta significativa

### 10.1 Diversidad no es una foto del equipo

Los materiales del curso conectan diversidad con co-creación, enfoques participativos y comités de múltiples partes. La diversidad de identidades puede ampliar perspectivas, pero no garantiza poder. Una persona invitada puede quedar aislada, sin información, sin tiempo o sin capacidad de veto.

La consulta es significativa cuando:

- ocurre antes de decisiones irreversibles;
- explica propósito, alternativas y límites;
- incluye afectados indirectos;
- reduce barreras de lenguaje, tiempo y conocimiento;
- compensa trabajo cuando corresponde;
- protege a quien señala riesgos;
- registra desacuerdos;
- produce una respuesta verificable;
- permite volver a consultar después de cambios.

### 10.2 Escalera de participación

| Nivel | Práctica | Limitación |
|---|---|---|
| Informar | Comunicar una decisión | No cambia poder |
| Consultar | Pedir opinión | Puede ignorarse |
| Involucrar | Iterar con partes | Influencia parcial |
| Co-diseñar | Compartir definición y alternativas | Requiere recursos |
| Gobernar | Compartir autorización, monitoreo y reparación | Requiere reglas institucionales |

No todos los proyectos alcanzarán cogobierno, pero deben declarar el nivel real. Llamar “participativo” a una encuesta final es ética washing.

### 10.3 Consulta SAIJ

Una consulta para búsqueda jurídica puede incluir:

- profesionales de distintos perfiles;
- archivistas y responsables de publicación;
- especialistas en privacidad y derechos;
- representantes o mediadores de comunidades afectadas;
- revisores de dominio;
- personas que mantendrán el sistema.

No corresponde exponer a víctimas o personas vulnerables a una consulta riesgosa sin mediación, cuidado y propósito. A veces la participación adecuada ocurre mediante organizaciones, expertos y evidencia existente. La seguridad de la consulta también se diseña.

---

## 11. Barreras al cambio y gobernanza

### 11.1 Mitos y defensas organizacionales

Los materiales sobre barreras identifican formas de mantener el statu quo. En un proyecto aparecen como:

- **mito de neutralidad:** “el modelo solo refleja datos”;
- **eficiencia como único valor:** “reduce tiempo, por lo tanto mejora”;
- **gatekeeping:** “es demasiado técnico para discutirlo”;
- **datos como retórica de objetividad:** un decimal clausura preguntas;
- **incentivos organizacionales:** lanzar rápido vale más que documentar;
- **difusión de responsabilidad:** cada área cree que otra decide;
- **inevitabilidad:** “la tecnología llegará igual”;
- **ética washing:** principios vistosos sin controles ni recursos;
- **falta de contestabilidad:** nadie puede comprender o impugnar.

La respuesta no es una capacitación aislada. Hay que cambiar autoridad, presupuesto, incentivos, controles, métricas y canales de escalamiento.

### 11.2 De consenso a control

Una cadena de gobernanza puede verse así:

~~~text
consenso social debatido
  → principio
  → recomendación o soft law
  → política institucional
  → procedimiento
  → control técnico u organizativo
  → evidencia de cumplimiento y efecto
  → auditoría
  → remediación
~~~

- **consenso social:** acuerdo siempre parcial y revisable sobre valores;
- **principio:** orientación, por ejemplo no discriminar;
- **soft law:** recomendaciones, declaraciones o estándares no equivalentes por sí mismos a ley;
- **política:** regla que una organización adopta;
- **control:** mecanismo concreto;
- **auditoría:** examen sistemático de evidencia;
- **remediación:** cambio que reduce causa, exposición o daño.

Una política “usar IA responsablemente” no es control. “Toda respuesta debe mostrar citas verificadas y abstenerse sin evidencia mínima; el responsable revisa una muestra semanal y registra incidentes” sí es operativo.

### 11.3 Contexto legal y temporal

Las diapositivas locales mencionan normativa argentina, recomendaciones internacionales, el EU AI Act y debates regionales. Son contexto pedagógico, no estado jurídico confirmado al día de hoy. Antes de desplegar o afirmar cumplimiento hay que consultar fuentes oficiales actuales y asesoramiento competente. Esta cautela no paraliza la ética: finalidad, minimización, documentación, participación y reparación pueden diseñarse mientras se verifica el marco aplicable.

---

## 12. Auditoría de IA

### 12.1 Qué es auditar

Auditar es reunir y evaluar evidencia contra criterios explícitos. No es buscar un único número ni prometer objetividad absoluta. Puede abarcar:

- propósito y gobernanza;
- documentación de datos y modelos;
- cobertura y calidad;
- pruebas desagregadas;
- seguridad y privacidad;
- trazabilidad;
- incidentes;
- interfaz y automatización;
- monitoreo;
- acciones de remediación.

Una auditoría puede ser interna o externa, previa o posterior, puntual o continua. Su independencia, acceso y capacidad de exigir cambios deben declararse.

### 12.2 Pasos mínimos

1. Definir alcance, sistema, versión y contexto.
2. Identificar criterio normativo y técnico.
3. Mapear actores, acciones y daños.
4. Revisar documentación y vacíos.
5. Reproducir pruebas permitidas.
6. Desagregar por hipótesis justificadas.
7. Analizar errores e incidentes.
8. Evaluar controles y contestabilidad.
9. Priorizar hallazgos por gravedad y exposición.
10. Asignar remediación, responsable y fecha.
11. Verificar la corrección.
12. Monitorear deriva y nuevos usos.

### 12.3 Ejemplo: del hallazgo a la remediación

**Hallazgo inventado.** En 40 consultas sobre un subtema, el buscador no muestra documentos previos a cierto año en el top 10. No se afirma que el corpus real tenga este problema.

Un mal informe diría: “sesgo temporal, corregir modelo”. Un hallazgo auditable separa:

- **evidencia:** lista de consultas, versión, resultados y cobertura;
- **impacto:** riesgo de invisibilizar precedentes;
- **causa candidata:** corpus incompleto, indexación, filtros, embedding o señal de recencia;
- **incertidumbre:** muestra pequeña y juicios pendientes;
- **remediación:** verificar cobertura; comparar baseline sin recencia; agregar conjunto temporal; ajustar si la causa se confirma;
- **responsable:** dueño de datos para cobertura y dueño de retrieval para ranking;
- **plazo:** antes del siguiente piloto;
- **verificación:** repetir consultas, medir recall por período y revisar casos;
- **residual:** documentos no digitalizados pueden seguir ausentes.

La remediación no es “subir la métrica”. Ataca una causa y verifica si el daño disminuye.

### 12.4 Registro de incidentes

| Campo | Pregunta |
|---|---|
| Fecha y versión | ¿Cuándo y con qué componentes ocurrió? |
| Detección | ¿Quién lo observó y cómo? |
| Evento | ¿Qué hizo el sistema? |
| Impacto | ¿A quién afectó y con qué gravedad? |
| Contención | ¿Qué se detuvo o limitó? |
| Causa | ¿Qué evidencia sostiene el análisis? |
| Remediación | ¿Qué cambió? |
| Verificación | ¿Cómo se comprobó? |
| Comunicación | ¿Quién fue informado? |
| Seguimiento | ¿Qué señal se monitorea? |

Un incidente no debe borrarse porque fue “error humano” o “mal uso”. La interacción humana forma parte del sistema.

### 12.5 Auditoría limitada no significa auditoría inútil

Toda auditoría tiene alcance: datos accesibles, tiempo, permisos y conocimiento. Se reporta qué no pudo probarse. La ausencia de hallazgos no prueba ausencia de riesgo. La transparencia sobre límites evita que un informe acotado se use como sello total.

### Checkpoint 12

Un hallazgo sin responsable ni verificación es una observación. Una corrección sin volver a medir es una promesa.

---

## 13. IA generativa y RAG

### 13.1 Riesgos específicos

La IA generativa concentra preocupaciones que ya estaban en el ciclo de datos:

- **proveniencia:** origen incierto de datos, modelos y respuestas;
- **consentimiento:** contenido usado fuera de expectativas;
- **trabajo:** anotación, moderación y feedback humano invisibilizados;
- **costo ambiental:** energía, infraestructura y escala;
- **privacidad:** memorización, extracción y logs de consultas;
- **alucinación:** afirmaciones no sostenidas;
- **opacidad:** difícil atribuir causas y versiones;
- **responsabilidad:** proveedor, integrador y usuario pueden desplazar culpa;
- **representación:** estereotipos y asociaciones;
- **seguridad y uso dual:** generación abusiva o filtración.

RAG no elimina estos riesgos. Agrega un componente de recuperación para aportar contexto. Si el corpus, el ranking o la generación fallan, la respuesta puede seguir siendo incorrecta.

### 13.2 Trazar el fallo por capas

Un sistema RAG simplificado tiene:

~~~text
datos → indexación → consulta → retrieval → contexto → generación → interfaz → acción
~~~

**Ejemplo inventado.** La pregunta pide precedentes sobre una figura jurídica. La respuesta cita dos documentos y afirma consenso.

- **Fallo de datos:** faltan años o tribunales; el consenso aparente nace de cobertura.
- **Fallo de indexación:** segmentación separó fundamento y decisión.
- **Fallo de consulta:** términos ambiguos no fueron aclarados.
- **Fallo de retrieval:** documentos relevantes quedaron fuera del top k.
- **Fallo de contexto:** se truncó una negación.
- **Fallo de generación:** el modelo generalizó más allá de las fuentes.
- **Fallo de interfaz:** las citas parecen validación total.
- **Fallo de acción:** el usuario copia sin revisión por automatización.

El registro debe permitir reconstruir corpus, versión, consulta, filtros, resultados, fragmentos y salida. Sin trazabilidad, la remediación se vuelve ensayo y error.

### 13.3 Ranking y daño de exposición

Un ranking distribuye atención. Los primeros resultados reciben más lectura y pueden moldear qué se considera relevante. Por eso se evalúan:

- recall de evidencia importante;
- exposición por período, órgano o categoría pertinente;
- diversidad y redundancia;
- sensibilidad a formulación;
- filtros que excluyen;
- consultas sin evidencia;
- desacuerdo entre jueces;
- estabilidad entre versiones.

No se fuerzan cuotas sin propósito. Se investiga si la exposición reproduce disponibilidad o señales irrelevantes y se corrige según el daño.

### 13.4 Ausencia de evidencia y abstención

Una política segura distingue:

- **evidencia suficiente y coherente**;
- **evidencia parcial o contradictoria**;
- **sin evidencia recuperada**;
- **error técnico**.

La ausencia de resultados no demuestra que no exista jurisprudencia. La salida debería decir: “No se recuperó evidencia suficiente en la versión y filtros indicados”, no “no hay precedentes”. La abstención necesita umbral, mensaje, cita de alcance y ruta de escalamiento.

### 13.5 Revisión humana significativa

La revisión es significativa cuando la persona:

1. conoce que la salida puede fallar;
2. ve fuentes, incertidumbre y límites;
3. tiene competencia y tiempo;
4. puede rechazar sin castigo;
5. accede a alternativas;
6. deja rastro de la decisión;
7. puede escalar;
8. recibe feedback sobre errores.

Si la interfaz oculta fuentes, el volumen es inmanejable o la institución espera aceptación, el humano es sello de goma. La automatización puede aumentar, no reducir, el sesgo.

### 13.6 Contestabilidad

Contestabilidad es posibilidad práctica de cuestionar una salida o decisión. Requiere:

- explicación comprensible del uso del sistema;
- acceso a evidencia relevante;
- canal de reclamo;
- revisión por persona con autoridad;
- plazo;
- protección contra represalias;
- corrección de datos y sistema;
- registro de resultado;
- aprendizaje agregado.

En un prototipo educativo, puede implementarse como botón de reporte, categoría de error, revisión y registro. En usos con consecuencias, debe integrarse institucionalmente.

---

## 14. Ética antes, durante y después

### 14.1 Antes de construir

- justificar problema y alternativa no tecnológica;
- mapear actores, poder y daño;
- definir usos excluidos;
- evaluar necesidad de datos;
- revisar consentimiento, finalidad y proveniencia;
- completar impacto inicial;
- decidir criterios de éxito y paro;
- asignar responsables.

### 14.2 Durante diseño y desarrollo

- mantener Data Statement y documentación de modelo;
- probar cobertura y calidad;
- revisar etiquetas y proxies;
- evaluar desagregadamente;
- consultar partes;
- registrar decisiones y riesgos;
- diseñar seguridad, minimización, abstención y apelación;
- ensayar incidentes;
- detener ante daño no controlado.

### 14.3 Después del despliegue

- monitorear cambio de datos, uso y daño;
- registrar incidentes y quejas;
- reevaluar métricas y cobertura;
- auditar logs con protección;
- comunicar cambios;
- remediar;
- retirar componentes cuando sea necesario;
- revisar finalidad ante nuevos usos.

### 14.4 Complementos integrados y acotados

- **Ética por diseño:** incorporar valores y controles desde la formulación.
- **Documentación de datos/modelo:** capacidades, límites, versiones y no-usos.
- **Registro de riesgos:** eventos anticipados, control y propietario.
- **Registro de incidentes:** eventos ocurridos y aprendizaje.
- **Evaluación de impacto:** análisis estructurado de personas, derechos, alternativas y mitigaciones.
- **Supervisión humana:** autoridad real y condiciones de revisión.
- **Contestabilidad:** impugnación y reparación.
- **Monitoreo:** señales técnicas y sociales posteriores.

Estos instrumentos no se desarrollan como marcos de producción enciclopédicos. Se incluyen porque convierten principios en decisiones revisables.

---

## 15. Transferencia integrada a SAIJ

### 15.1 Principios de uso

1. El corpus no es la realidad judicial completa.
2. **Fuero** es un target construido.
3. Acceso público no elimina sensibilidad.
4. Accuracy global no basta.
5. Retrieval se evalúa antes de generación.
6. Una cita no prueba que toda la frase esté respaldada.
7. El sistema debe abstenerse con evidencia insuficiente.
8. La revisión humana necesita tiempo y autoridad.
9. Toda omisión, corrección y queja alimenta auditoría.
10. No se ofrece asesoramiento legal automático.

### 15.2 Plantilla de riesgo SAIJ

| Riesgo | Afectados | Indicador | Prevención | Respuesta |
|---|---|---|---|---|
| Reidentificación | Personas nombradas | Casos únicos/snippets | Minimización y acceso | Contener, revisar, corregir |
| FNR alto en clase crítica | Usuarios y partes | FNR + conteos | Evaluación estratificada | Abstener o revisión obligatoria |
| Proxy institucional | Regiones/órganos | Dependencia y deriva | Pruebas con/sin feature | Limitar uso |
| Ranking homogéneo | Comunidades y usuarios | Exposición/recall | Evaluación diversa | Reindexar o ajustar |
| Alucinación | Usuarios y terceros | Afirmación sin soporte | Generación anclada | Retirar, corregir, registrar |
| Automatización | Revisores | Tasa de aceptación anómala | Interfaz y capacitación | Muestreo y rediseño |
| Ausencia confundida | Usuarios | Respuesta categórica sin fuente | Política de abstención | Mensaje corregido |

### 15.3 Decisiones pendientes

- población y versión del corpus;
- finalidad primaria;
- campos sensibles;
- unidad de indexación;
- significado de **fuero**;
- grupos cuya evaluación es ética y estadísticamente viable;
- severidad de FP y FN;
- umbrales de abstención;
- conjunto de consultas;
- protocolo de relevancia;
- política de exposición;
- logs y retención;
- responsable de incidentes;
- canal de contestación;
- criterio de retiro.

Ninguna debe completarse con intuición disfrazada de hecho.

---

## 16. Conexión conceptual con los notebooks

### 16.1 Fairness sobre ACSIncome

Los dos notebooks de equidad usan ACSIncome y un modelo educativo de ingresos. Su aporte conceptual es el flujo:

~~~text
hipótesis de daño
  → atributo sensible
  → variable objetivo
  → predicciones
  → métricas por grupo
  → interpretación
  → posible remediación
~~~

No deben copiarse mecánicamente a SAIJ. El atributo SEX de ese dataset tiene limitaciones; la tarea de ingresos es educativa y no se recomienda para uso real. Las salidas guardadas no fueron reproducidas.

Si se ejecutaran después, habría que descargar:

- el dataset remoto ACSIncome;
- TensorFlow 2.15;
- tensorflow-model-remediation;
- fairness-indicators 0.46.0;
- tensorflow-model-analysis 0.46.0;
- tensorflow-data-validation 1.15.1;
- dependencias transitivas compatibles y un entorno adecuado.

La descarga, compatibilidad, tiempo y resultados deberían registrarse. Esta materia no ejecuta esas celdas.

### 16.2 Notebook de sesgo en embeddings

El notebook explora asociaciones de género en embeddings ingleses y castellanos. Enseña que:

- una representación aprendida captura regularidades y estereotipos;
- la similitud no es neutral;
- definir una dirección de género simplifica un fenómeno social;
- la lista de palabras “neutras” condiciona la métrica;
- el castellano introduce género gramatical y omisión de sujeto;
- una medida cuantitativa no captura todo el sesgo;
- exploración no equivale a evaluación sistemática.

Para ejecutarlo después se necesitarían paquetes como gensim, numpy, scipy, scikit-learn, matplotlib y seaborn; además, el modelo remoto word2vec-google-news-300 y un archivo fastText del Spanish Billion Words Corpus. Son descargas grandes y externas. Sus salidas guardadas son preexistentes y pendientes de reproducción.

### 16.3 Transferencia a embeddings SAIJ

Una exploración de vecinos jurídicos debería preguntar:

- ¿qué corpus entrenó la representación?
- ¿qué período y jurisdicción domina?
- ¿qué asociaciones sensibles aparecen?
- ¿la cercanía proviene de contenido, nombres o plantillas?
- ¿qué términos faltan?
- ¿cómo cambia por versión?
- ¿qué daño causa un vecino inadecuado?
- ¿qué baseline y revisión lo contradicen?

No hace falta ejecutar el notebook para aprender la pregunta ética. El código viene después del propósito y del protocolo.

### Checkpoint 16

Una técnica de remediación puede reducir una diferencia métrica sin reparar la etiqueta, el uso o el daño. Documentá qué cambia y qué no.


---

## 17. Ejercicios conceptuales

Respondelos sin código. En cada respuesta distinguí hechos, valores, incertidumbre y decisión.

### Ejercicio 1 — Descriptivo o normativo

Clasificá estas afirmaciones y explicá qué evidencia falta: “el grupo A tiene más falsos negativos”, “esa diferencia es injusta” y “debe igualarse la tasa entre grupos”.

### Ejercicio 2 — Legalidad y ética

Un equipo dice que puede reutilizar documentos porque son accesibles públicamente. Construí un argumento que separe posibilidad técnica, permiso jurídico a verificar y legitimidad ética.

### Ejercicio 3 — Responsabilidad profesional

La jefatura exige desplegar aunque no existe prueba por grupos ni canal de reclamo. ¿Qué deberes tiene el equipo y qué alternativas debería documentar?

### Ejercicio 4 — Sistema sociotécnico

Tomá un clasificador de **fuero** y enumerá al menos ocho componentes no algorítmicos que pueden cambiar su impacto.

### Ejercicio 5 — Mapa de poder

En un buscador SAIJ, ¿quién tiene alto poder pero bajo daño directo y quién puede tener bajo poder pero alto daño? Proponé dos mecanismos para reducir la asimetría.

### Ejercicio 6 — Tipos de daño

Un ranking deja casi siempre al final documentos sobre un grupo vulnerable. Clasificá daños posibles por nivel, materialidad, representación y tiempo.

### Ejercicio 7 — Accuracy insuficiente

Un modelo tiene 98 % de accuracy y falla en 20 de 25 casos críticos. Explicá por qué ambas cifras pueden coexistir y qué análisis pedirías.

### Ejercicio 8 — Sesgo histórico

La etiqueta de prioridad reproduce decisiones pasadas de una institución. ¿Cuándo predecirla bien puede reproducir injusticia?

### Ejercicio 9 — Muestreo

Una evaluación usa solo consultas frecuentes de usuarios expertos. Identificá población objetivo, población observada, excluidos y límites de generalización.

### Ejercicio 10 — Medición y etiqueta

**Fuero** aparece en una columna. Diseñá cinco preguntas para averiguar qué mide realmente antes de entrenar.

### Ejercicio 11 — Proxy

El tribunal mejora mucho el clasificador. Proponé una hipótesis legítima y una hipótesis problemática sobre esa mejora, con pruebas que las distingan.

### Ejercicio 12 — Interseccionalidad

Las métricas por género y por región parecen iguales, pero una combinación muestra daño. ¿Cómo investigás sin convertir celdas pequeñas en certeza ni exponer personas?

### Ejercicio 13 — Matriz de confusión

Para un grupo: TP=24, FN=6, FP=8, TN=62. Calculá TPR, FNR, FPR y PPV. Interpretá cada una para un detector de texto sensible.

### Ejercicio 14 — Comparación entre grupos

Usando el ejemplo trabajado de A y B, ¿qué grupo está peor si el daño principal es exposición de información sensible? ¿Y si el daño principal es censura excesiva?

### Ejercicio 15 — Paridad demográfica

Dos grupos reciben 50 % de predicciones positivas. ¿Qué concluye la paridad demográfica y qué no concluye?

### Ejercicio 16 — Igualdad de oportunidades

El TPR es igual entre grupos, pero ambos tienen TPR=0,40. ¿Se alcanzó el criterio? ¿Es suficiente?

### Ejercicio 17 — Odds igualadas

Un sistema iguala TPR pero no FPR. ¿Cumple igualdad de oportunidades, odds igualadas, ambas o ninguna? Explicá.

### Ejercicio 18 — Paridad predictiva

PPV es 0,80 en ambos grupos, pero FNR es 0,10 y 0,45. ¿Qué experiencia distinta puede quedar oculta?

### Ejercicio 19 — Calibración

Interpretá un score calibrado de 0,70. ¿Qué errores cometerías si lo presentaras como “70 % de certeza de que esta persona hará X”?

### Ejercicio 20 — Criterios incompatibles

Elegí entre la política X y Z del ejemplo. Justificá tu decisión según un daño concreto y explicá por qué no es universal.

### Ejercicio 21 — Grupos pequeños

Un subgrupo tiene tres positivos y un falso negativo. ¿Qué podés informar y qué no deberías afirmar?

### Ejercicio 22 — Privacidad

Un fallo no contiene nombre, pero sí edad, localidad, fecha y relación familiar inusual. ¿Qué riesgo existe y qué controles evaluarías?

### Ejercicio 23 — Finalidad y minimización

Para búsqueda semántica, el equipo quiere indexar todos los campos disponibles. Proponé una alternativa basada en finalidad y capas de acceso.

### Ejercicio 24 — Uso dual

Describí un uso legítimo y uno dañino del mismo corpus SAIJ. ¿Qué controles diferenciales aplicarías?

### Ejercicio 25 — Data Statement

Escribí cinco campos que no pueden faltar en un Data Statement SAIJ y explicá qué decisión permite cada uno.

### Ejercicio 26 — Desconocidos

La persona experta no sabe cómo se generó una etiqueta. ¿Conviene omitir el campo, inventar una explicación o registrar desconocido? Derivá consecuencias.

### Ejercicio 27 — Participación

Un equipo muestra el producto terminado a dos profesionales y lo llama co-diseño. Diagnosticá la práctica y proponé una consulta significativa.

### Ejercicio 28 — Barreras

Identificá neutralidad, gatekeeping, difusión de responsabilidad y ética washing en una organización ficticia. Para cada una, proponé un cambio institucional.

### Ejercicio 29 — Auditoría

Una auditoría detecta recall temporal bajo, pero no conoce la causa. Convertí el hallazgo en plan de remediación y verificación sin afirmar más de la evidencia.

### Ejercicio 30 — Incidente

Una respuesta RAG cita un fallo real pero atribuye una conclusión que el fallo no sostiene. ¿Qué contención, análisis causal y seguimiento aplicarías?

### Ejercicio 31 — Notebooks

¿Por qué no se pueden presentar los outputs guardados de los notebooks de fairness o embeddings como resultados propios? ¿Qué habría que registrar al reproducirlos?

### Ejercicio 32 — Ausencia de evidencia

El buscador devuelve cero resultados. Redactá una respuesta segura, una acción de escalamiento y una prueba para diferenciar ausencia real de falla del sistema.

---

## 18. Respuestas razonadas

### Respuesta 1

La primera afirmación es descriptiva y exige conteos, definición de grupo, referencia y período. La segunda es normativa: para llamarla injusta hay que conectar diferencia con daño, historia, alternativas y legitimidad del criterio. La tercera propone una política. Igualar puede ser razonable si el costo relevante es la omisión, pero podría empeorar falsos positivos o imponer una referencia defectuosa. La cadena correcta es medir, interpretar el daño, comparar criterios y justificar el control.

### Respuesta 2

La accesibilidad pública solo demuestra que puede consultarse bajo ciertas condiciones. No prueba permiso para cualquier copia, indexación o generación; eso debe verificarse según fuente, licencia, términos y marco vigente. Aun autorizado, hay que evaluar expectativa, sensibilidad, escala, finalidad y reidentificación. Una consulta manual y una agregación masiva no producen la misma exposición. La decisión puede ser usar una versión minimizada, restringir campos, excluir usos o no reutilizar.

### Respuesta 3

El equipo debe revelar que faltan pruebas y contestabilidad, documentar riesgo y solicitar una decisión explícita de responsables con autoridad. Puede proponer piloto limitado, revisión obligatoria, abstención o postergar. Si el daño grave no puede controlarse, no desplegar es opción profesional. “Nos ordenaron” no elimina responsabilidad. También debe preservar evidencia, buscar revisión competente y usar canales de escalamiento, evitando promesas que no puede sostener.

### Respuesta 4

Además del algoritmo: definición de **fuero**, fuente de etiquetas, guías de anotación, muestreo, preprocesamiento, interfaz, umbral, cola de revisión, tiempo del revisor, incentivos de aceptación, responsables, canal de corrección, versión del corpus, infraestructura y política de uso. Cualquiera puede cambiar consecuencias. El mismo score puede ser sugerencia reversible o decisión automática. Por eso la evaluación debe abarcar el flujo completo.

### Respuesta 5

La institución, proveedor y equipo de producto suelen tener alto poder de definición con daño directo bajo. Personas nombradas, víctimas o comunidades pueden tener bajo poder y daño alto. Dos mecanismos: participación temprana mediante representantes o expertos con capacidad real de modificar usos; y contestabilidad con acceso, revisión autorizada, plazos y corrección. También ayudan límites de propósito, auditoría independiente y un dueño de riesgo que no dependa del equipo de lanzamiento.

### Respuesta 6

Puede haber daño colectivo porque una comunidad pierde visibilidad; representacional porque sus casos parecen menos centrales; material si profesionales omiten evidencia; demorado por acumulación de exposición desigual; indirecto porque el ranking influye en decisiones humanas; y de calidad de servicio si ciertas consultas funcionan peor. No hace falta que cada documento sea incorrecto. Hay que medir exposición y recall, revisar cobertura y escuchar a usuarios y afectados.

### Respuesta 7

Si hay muchas observaciones fáciles, 20 errores críticos pueden ser una fracción pequeña y el promedio seguir en 98 %. Pediría matriz por clase, TPR/FNR críticos, conteos, severidad, casos, cobertura y confianza. También revisaría si “crítico” es una etiqueta confiable, si hay subgrupos, qué acción sigue y si existe abstención. El dato global no debe ocultar que el sistema falla precisamente donde más importa.

### Respuesta 8

Predecir bien reproduce injusticia cuando la etiqueta histórica refleja acceso desigual, discriminación, decisiones no apelables o medición sesgada. El modelo aprende la práctica, no un deber. Antes de automatizar hay que revisar cómo nació el target, quién fue excluido y qué acción se pretende. Alternativas: redefinir objetivo, recolectar referencia distinta, usar el modelo solo para auditoría, o no predecir. Mejor accuracy puede ser peor legitimidad.

### Respuesta 9

La población observada son consultas frecuentes de expertos que usaron el sistema anterior. La población objetivo podría ser la de todos los futuros usuarios, incluyendo no expertos. Quedan fuera consultas raras, lenguaje cotidiano, errores y necesidades que el sistema anterior desalentó. La evaluación solo sostiene desempeño en un perfil cercano al observado. Hace falta muestreo por situaciones, creación participativa de consultas y reporte estratificado.

### Respuesta 10

Preguntas: ¿quién asignó **fuero**? ¿representa órgano, competencia o clasificación editorial? ¿puede haber múltiples valores? ¿cambió la regla con el tiempo? ¿cómo se resolvieron ambigüedades? También conviene preguntar cobertura y propósito. Sin estas respuestas, el equipo no sabe qué significa un error ni dónde generaliza. Una columna disponible no es una verdad autoexplicativa.

### Respuesta 11

Hipótesis legítima: tribunal determina administrativamente el ruteo que se quiere apoyar. Hipótesis problemática: tribunal actúa como atajo y el modelo no aprende contenido, por lo que falla en nuevos órganos y reproduce disponibilidad. Se comparan modelos con/sin variable, por tribunal y tiempo, se prueba transferencia, se inspeccionan errores y se clarifica propósito. La mejora se acepta solo si su dependencia es compatible con el uso.

### Respuesta 12

Partiría de una hipótesis social que justifique la intersección, no de todas las combinaciones. Reportaría conteos, incertidumbre y estabilidad temporal; limitaría publicación de celdas pequeñas; agregaría revisión cualitativa; y consultaría conocimiento de dominio. Si hay muy pocos casos, la conclusión es “señal que requiere más evidencia”, no una tasa estable. También revisaría si recolectar o conservar atributos aumenta riesgo de reidentificación.

### Respuesta 13

(TPR=24/(24+6)=0{,}80): detecta 80 % del texto realmente sensible. (FNR=6/30=0{,}20): deja sin detectar 20 %. (FPR=8/(8+62)=8/70≈0{,}114): marca por error 11,4 % del texto no sensible. (PPV=24/(24+8)=24/32=0{,}75): tres cuartos de lo marcado eran sensibles. En privacidad suele preocupar mucho FN, pero FP puede censurar contexto. La prioridad depende del uso.

### Respuesta 14

Si “positivo” es detectar información sensible, la exposición ocurre por FN. B tiene FNR 0,40 frente a 0,10 de A, por lo que está peor. La censura excesiva se asocia con FP; A tiene FPR 0,20 frente a 0,10 de B, por lo que A está peor. PPV también favorece B. La conclusión muestra por qué “grupo peor” depende del daño y no de una sola tasa.

### Respuesta 15

Concluye igualdad en tasa de resultados positivos para esos grupos, estimada en esa muestra. No concluye igualdad de TPR, FPR, PPV, calidad, trato o daño. Tampoco prueba que los grupos sean legítimos, que el target sea justo o que 50 % sea nivel adecuado. Dos grupos pueden recibir la misma proporción y sufrir errores distintos.

### Respuesta 16

Sí, satisface igualdad de oportunidades porque TPR es igual. No es suficiente: ambos pierden 60 % de los positivos. La igualdad puede ser igualdad en mal servicio. Debe evaluarse nivel absoluto, alternativas, daño, FPR, PPV y capacidad de mejorar. Un criterio de paridad no reemplaza calidad mínima.

### Respuesta 17

Cumple igualdad de oportunidades porque iguala TPR. No cumple odds igualadas, que exige igualar TPR y FPR. Esta diferencia importa si las falsas alarmas generan daño. El sistema puede ofrecer igual detección a positivos y someter a un grupo a más intervenciones injustificadas. La elección debe considerar ambos costos.

### Respuesta 18

Paridad predictiva dice que una predicción positiva es igualmente confiable. El FNR desigual dice que muchos más positivos reales de un grupo quedan sin detectar. Para quienes reciben positivo la experiencia es similar; para quienes necesitan ser detectados no. La igualdad condicional a la salida puede ocultar desigual acceso a esa salida.

### Respuesta 19

Calibración significa que, entre casos comparables del grupo con score alrededor de 0,70, aproximadamente 70 % tiene (Y=1). No es certeza individual, causalidad ni probabilidad de conducta futura fuera del contexto. Depende de etiqueta, población y estabilidad. Presentarlo como esencia de una persona promueve determinismo y puede ocultar incertidumbre y cambio.

### Respuesta 20

Si el daño es negar una oportunidad a positivos reales, elegiría X porque iguala TPR en 0,80, mientras documento PPV desigual y falsos positivos. No es universal: si el positivo dispara una medida invasiva, confiabilidad igual puede pesar más y Z resultar preferible. También compararía no desplegar o cambiar la acción. La elección es normativa, contextual y revisable.

### Respuesta 21

Puede informarse el conteo: un FN entre tres positivos, tasa puntual 0,333, con extrema inestabilidad. No afirmaría que la tasa poblacional es 33,3 % ni compararía decimales como evidencia fuerte. Revisaría casos, ampliaría período si es defendible y protegería identidad. La falta de precisión es un resultado; no se corrige ocultando el grupo.

### Respuesta 22

Existe reidentificación por cuasi-identificadores. Evaluaría unicidad, fuentes externas, snippets, filtros combinables, acceso y retención. Controles: generalizar fecha o localidad, limitar campos, separar capas, revisar casos raros, restringir consultas y monitorear abuso. Quitar el nombre no basta. Tampoco debe eliminarse contexto necesario sin evaluar utilidad jurídica.

### Respuesta 23

Primero definiría qué filtros y señales necesita retrieval. Mantendría texto original restringido, versión procesada, metadatos mínimos y embeddings con control. Excluiría campos sin finalidad, limitaría snippets y definiría logs y retención. Luego probaría cuánto pierde el sistema. Minimización es decisión proporcional: conservar lo necesario y protegerlo, no indexar todo “por si acaso”.

### Respuesta 24

Uso legítimo: evaluación educativa de recuperación de precedentes con revisión. Uso dañino: perfilar personas nombradas o localizar víctimas. Controles: propósito contractual, acceso por roles, minimización, límites de consulta, detección de abuso, exclusión de exportación, revisión y sanción. Un Data Statement explicita ambos. Si el uso dañino es fácil e incontrolable, puede corresponder no distribuir.

### Respuesta 25

Fuente y versión permiten reproducir; composición y cobertura limitan generalización; origen de **fuero** permite interpretar errores; personas/sensibilidad orientan privacidad; usos previstos y excluidos permiten autorizar o negar tareas. También son esenciales preprocesamiento y mantenimiento. Cada campo debe terminar en decisión, no en descripción ornamental.

### Respuesta 26

Se registra “desconocido”, quién no lo sabe y por qué. Consecuencias: no asumir validez, limitar usos, buscar documentación, revisar muestra o crear nueva etiqueta. Omitir oculta riesgo; inventar corrompe trazabilidad. El desconocido puede convertirse en criterio de no despliegue si la etiqueta sostiene una decisión importante.

### Respuesta 27

Es consulta tardía, no co-diseño. Una práctica significativa empieza con definición de problema, incluye perfiles y afectados relevantes, presenta alternativas, compensa tiempo, registra desacuerdo y explica cambios. Debe existir una decisión todavía abierta. Después del piloto se vuelve a consultar con evidencia e incidentes. Dos opiniones no representan automáticamente el campo.

### Respuesta 28

Neutralidad: “solo refleja datos”; cambio: revisión de historia y target. Gatekeeping: “no pueden entender”; cambio: documentación comprensible y autoridad compartida. Difusión: “lo ve legales”; cambio: dueño por riesgo y matriz de responsabilidades. Ética washing: principios sin controles; cambio: presupuesto, métricas, auditoría, plazos y consecuencias. Las barreras son organizacionales, no solo cognitivas.

### Respuesta 29

Documentaría consultas, versión y patrón temporal; verificaría primero cobertura del corpus; luego indexación, filtros y señal de recencia; compararía baseline; y pediría juicios. Asignaría responsables distintos para datos y retrieval. Verificación: repetir conjunto, medir recall por período, revisar casos y reportar residual. Hasta confirmar causa, el hallazgo es “bajo recall observado”, no “modelo sesgado”.

### Respuesta 30

Contención: retirar o marcar respuesta, preservar logs y avisar a revisores. Causa: comprobar retrieval, fragmentos, prompt, truncado y generación. Impacto: quién la vio y qué acción siguió. Remediación: verificación de soporte por afirmación, mejor contexto, abstención y diseño de citas. Seguimiento: prueba de regresión, muestreo y registro. Una cita real no excusa una atribución falsa.

### Respuesta 31

Porque las celdas no fueron ejecutadas ni el entorno, datos o versiones verificados. Son salidas preexistentes, no evidencia reproducida por Javier. Al reproducir: versión de notebook, runtime, paquetes, descargas, semillas, hardware, cambios, fecha, hashes, errores, outputs y comparación. También debe justificarse que el ejercicio educativo no se convierta en resultado SAIJ.

### Respuesta 32

Respuesta: “No se recuperó evidencia suficiente en la versión del corpus y con los filtros usados; esto no demuestra que no existan documentos pertinentes.” Escalamiento: ampliar consulta, revisar filtros y búsqueda alternativa con experto. Prueba: consulta conocida con evidencia, chequeo de cobertura, logs y baseline. Se distinguen cero real, problema de vocabulario, corpus incompleto y falla técnica.

---


## 19. Hoja de transferencia ética SAIJ

Esta hoja se completa con evidencia reproducida. Los espacios vacíos no son fallas: muestran decisiones pendientes.

### 19.1 Propósito y no-usos

- Problema que se intenta resolver: ________
- Beneficiarios directos: ________
- Personas afectadas indirectamente: ________
- Alternativa no tecnológica comparada: ________
- Decisión que el sistema **no** puede tomar: ________
- Usos excluidos: ________
- Criterio para detener o retirar: ________

### 19.2 Datos y documentación

- Versión y fecha del corpus: ________
- Fuente y condiciones de acceso: ________
- Unidad de análisis/indexación: ________
- Períodos y órganos cubiertos: ________
- Ausencias conocidas: ________
- Datos personales o sensibles: ________
- Estrategia de minimización: ________
- Proveniencia de **fuero**: ________
- Anotadores y desacuerdos: ________
- Responsable de mantenimiento: ________

### 19.3 Stakeholders y participación

- Usuario directo: ________
- Sujetos de datos: ________
- Grupos potencialmente afectados: ________
- Actores con poder de aprobación: ________
- Perspectiva faltante: ________
- Nivel de participación real: informar / consultar / involucrar / co-diseñar / gobernar.
- Cambios producidos por la consulta: ________
- Desacuerdos abiertos: ________

### 19.4 Hipótesis de daño

Para cada hipótesis completá:

- Evento: ________
- Afectados: ________
- Daño material/simbólico: ________
- Individual/colectivo: ________
- Inmediato/demorado: ________
- Evidencia actual: ________
- Incertidumbre: ________
- Control: ________
- Responsable: ________
- Verificación: ________

### 19.5 Fairness

- Acción positiva y negativa: ________
- Significado de TP, FN, FP y TN: ________
- Error más grave y justificación: ________
- Grupos éticamente pertinentes: ________
- Motivo para recolectar atributos: ________
- Conteos mínimos y privacidad: ________
- Métrica primaria: ________
- Métricas de tensión: ________
- Nivel absoluto mínimo: ________
- Política si no hay evidencia: ________

### 19.6 Retrieval y RAG

- Tipos de consulta: ________
- Baseline léxico: ________
- Candidato semántico: ________
- Juicios de relevancia: ________
- Cobertura por período/órgano: ________
- Política de exposición: ________
- Umbral de abstención: ________
- Mensaje de ausencia de evidencia: ________
- Citas y soporte por afirmación: ________
- Logs y retención: ________
- Revisión humana: ________
- Canal de contestación: ________

### 19.7 Auditoría e incidentes

- Auditor y grado de independencia: ________
- Versión y alcance: ________
- Pruebas desagregadas: ________
- Limitaciones: ________
- Registro de riesgos: ________
- Registro de incidentes: ________
- Responsable de remediación: ________
- Fecha de verificación: ________
- Frecuencia de monitoreo: ________

---

## 20. Autoevaluación final de Materia 6

Marcá solo si podés explicarlo con un ejemplo, una limitación y una aplicación SAIJ:

- [ ] Distingo ética, moral, derecho, cumplimiento y responsabilidad.
- [ ] Separo descripción de norma.
- [ ] Explico por qué la ética empieza al formular el problema.
- [ ] Mapeo un sistema sociotécnico completo.
- [ ] Identifico usuarios, afectados y sujetos de datos.
- [ ] Analizo poder y participación.
- [ ] Distingo beneficio, riesgo y daño.
- [ ] Clasifico daños individuales, colectivos, materiales y simbólicos.
- [ ] Reconozco daño asignativo y representacional.
- [ ] Rastreo sesgo por todo el ciclo de vida.
- [ ] No trato **fuero** como verdad natural.
- [ ] Explico representación, medición, etiqueta y agregación.
- [ ] Detecto proxies y pienso intersecciones.
- [ ] Calculo TPR, FNR, FPR y PPV.
- [ ] Interpreto denominadores y consecuencias.
- [ ] Explico paridad demográfica.
- [ ] Explico igualdad de oportunidades.
- [ ] Explico odds igualadas.
- [ ] Explico paridad predictiva.
- [ ] Explico calibración.
- [ ] Comprendo conflictos por tasas base.
- [ ] Reporto conteos e incertidumbre.
- [ ] Distingo privacidad, confidencialidad y seguridad.
- [ ] Explico finalidad y minimización.
- [ ] Evalúo reidentificación y uso dual.
- [ ] No equiparo acceso público con legitimidad.
- [ ] Completo un Data Statement honesto.
- [ ] Registro usos excluidos y mantenimiento.
- [ ] Diseño consulta significativa.
- [ ] Reconozco gatekeeping y ética washing.
- [ ] Convierto principios en controles.
- [ ] Diseño una auditoría con alcance.
- [ ] Transformo hallazgo en remediación verificable.
- [ ] Mantengo un registro de incidentes.
- [ ] Trazo un fallo RAG por capas.
- [ ] Evalúo ranking como distribución de exposición.
- [ ] Diseño abstención y ausencia de evidencia.
- [ ] Distingo revisor real de sello de goma.
- [ ] Diseño contestabilidad.
- [ ] Identifico riesgos de datos, trabajo, ambiente y privacidad en IA generativa.
- [ ] Sé cuándo no construir, no desplegar o retirar.
- [ ] No presento outputs guardados como resultados reproducidos.
- [ ] Conozco el plan del práctico con fecha suministrada del 1 de octubre de 2026.

### Criterio de dominio

Considerá dominada la materia cuando, frente a una demo técnicamente convincente, puedas preguntar:

1. ¿qué problema y valor define el objetivo?
2. ¿quién gana y quién soporta el peor error?
3. ¿qué alternativa no tecnológica existe?
4. ¿cómo se produjeron datos y etiquetas?
5. ¿qué población queda fuera?
6. ¿qué significa cada métrica como acción?
7. ¿qué criterio de equidad se eligió y cuál se sacrificó?
8. ¿qué incertidumbre tienen grupos pequeños?
9. ¿qué información puede reidentificar?
10. ¿quién participó y qué cambió?
11. ¿quién tiene autoridad para detener?
12. ¿qué evidencia respalda cada control?
13. ¿cómo se registra un incidente?
14. ¿cómo se apela?
15. ¿qué frase debe decir el sistema cuando no sabe?

---

## 21. Glosario de Materia 6

| Término | Definición operativa |
|---|---|
| **Abstención** | Decisión de no emitir respuesta o predicción cuando la evidencia no alcanza un criterio. |
| **Afirmación descriptiva** | Enunciado sobre hechos o patrones observados. |
| **Afirmación normativa** | Enunciado sobre lo que debería hacerse o valorarse. |
| **Atributo sensible** | Característica que requiere protección o análisis por privacidad, vulnerabilidad o discriminación. |
| **Auditoría de IA** | Evaluación sistemática de evidencia contra criterios y alcance explícitos. |
| **Automatización, sesgo de** | Confianza excesiva en salidas automáticas incluso cuando son incorrectas. |
| **Calibración** | Correspondencia entre score anunciado y frecuencia observada, dentro de un contexto. |
| **Confidencialidad** | Protección contra uso o divulgación no autorizados de información en custodia. |
| **Consentimiento** | Autorización informada y pertinente; no sustituye finalidad ni protección. |
| **Contestabilidad** | Capacidad práctica de cuestionar, revisar y corregir una salida o decisión. |
| **Control** | Mecanismo técnico u organizativo que previene, detecta o responde a un riesgo. |
| **Daño asignativo** | Pérdida o distribución injusta de recurso, oportunidad o servicio. |
| **Daño representacional** | Estereotipación, degradación, invisibilización o representación injusta. |
| **Data Statement** | Documentación reflexiva de origen, composición, uso, riesgo y límites de un dataset. |
| **Datasheet** | Documento de ciclo de vida sobre motivación, composición, recolección, procesamiento, uso, distribución y mantenimiento. |
| **Dual use** | Capacidad de un dato o sistema de servir a usos beneficiosos y dañinos. |
| **Equalized odds** | Igualdad de TPR y FPR entre grupos. |
| **Ética por diseño** | Incorporación de valores, afectados y controles desde la formulación. |
| **Ética washing** | Uso reputacional de principios sin autoridad, recursos, evidencia ni cambios. |
| **Fairness** | Familia de preguntas y criterios contextuales sobre distribución de error, beneficio y daño. |
| **Feedback loop** | Ciclo en el que la salida modifica los datos futuros y aparenta confirmarse. |
| **Finalidad** | Propósito específico que justifica recolectar o usar información. |
| **FNR** | Proporción de positivos reales omitidos. |
| **FPR** | Proporción de negativos reales marcados como positivos. |
| **Gatekeeping** | Uso de barreras técnicas o institucionales para excluir crítica y participación. |
| **Igualdad de oportunidades** | Igualdad de TPR entre grupos. |
| **Impact assessment** | Evaluación estructurada de propósito, afectados, daños, alternativas y mitigaciones. |
| **Incidente** | Evento observado que produjo o pudo producir comportamiento no deseado o daño. |
| **Interseccionalidad** | Análisis de experiencias producidas por relaciones combinadas de categorías y poder. |
| **Limitación de finalidad** | Restricción del uso a propósitos compatibles y explícitos. |
| **Minimización** | Tratamiento de la menor cantidad de datos necesaria para un propósito. |
| **Odds igualadas** | Traducción de equalized odds: igualdad de TPR y FPR. |
| **Paridad demográfica** | Igualdad de tasa de predicción positiva entre grupos. |
| **Paridad predictiva** | Igualdad de PPV entre grupos. |
| **Parte interesada** | Actor que influye, se beneficia, se afecta o responde por el sistema. |
| **Participación significativa** | Intervención informada, temprana y capaz de cambiar decisiones. |
| **Persona afectada** | Persona que recibe consecuencias aunque no use el sistema. |
| **PPV** | Proporción de predicciones positivas que son verdaderos positivos. |
| **Proveniencia** | Origen, custodia, transformaciones y condiciones de un dato o componente. |
| **Proxy** | Variable que aproxima o permite inferir otra característica. |
| **Reidentificación** | Vinculación de datos con una persona mediante información directa o combinada. |
| **Rendición de cuentas** | Obligación y capacidad de explicar, responder, corregir y reparar. |
| **Riesgo residual** | Riesgo que permanece después de aplicar controles. |
| **Seguridad** | Protección técnica y organizativa contra acceso, alteración, pérdida o abuso. |
| **Sistema sociotécnico** | Conjunto de tecnología, personas, instituciones, reglas, incentivos y acciones. |
| **Soft law** | Recomendación o estándar orientador que no equivale por sí solo a ley. |
| **Tasa base** | Proporción de positivos reales dentro de una población o grupo. |
| **TPR** | Proporción de positivos reales correctamente detectados. |
| **Uso excluido** | Tarea o contexto que la documentación declara no apropiado. |

---

## 22. Frontera de alcance y extensiones opcionales

Esta materia no intenta ser una enciclopedia de filosofía moral, derecho comparado, fairness causal avanzada ni marcos completos de gobernanza productiva. Tampoco afirma actualidad jurídica. Su objetivo es que puedas integrar ética al trabajo ordinario de ciencia de datos con preguntas, métricas, documentación, participación, controles y responsabilidad.

Quedan como extensiones opcionales, solo si el proyecto las necesita y cuenta con fuentes y especialistas adecuados:

- teorías morales comparadas;
- inferencia causal de discriminación;
- privacidad diferencial;
- métodos criptográficos;
- certificaciones sectoriales;
- evaluación ambiental detallada;
- gobernanza formal de proveedores;
- auditoría legal.

La regla para expandir es la misma que para modelar: partir de una decisión real y evidencia necesaria, no de una lista de moda.

### Cierre de Materia 6

La competencia ética no consiste en no equivocarse. Consiste en hacer visibles los valores, buscar perspectivas que contradigan, medir sin idolatrar métricas, documentar límites, distribuir responsabilidad y reparar. Para SAIJ, eso significa que el proyecto integrador no comenzará con “generemos respuestas”, sino con una pregunta más exigente:

> ¿Podemos demostrar que los datos, la recuperación, la interfaz y la gobernanza ayudan a encontrar evidencia sin ocultar incertidumbre, amplificar daño ni sustituir responsabilidad humana?

Si la respuesta es “todavía no”, esa honestidad es un resultado profesional y el punto de partida para el siguiente ciclo.

