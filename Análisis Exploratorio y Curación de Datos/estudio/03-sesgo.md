# 03 — Sesgo

## Concepto

El **sesgo** (en inglés *bias*) es un error sistemático: una desviación que apunta siempre para el mismo lado. No es ruido aleatorio (que se cancela promediando), es una distorsión consistente entre lo que tu estimador, modelo o muestra te dice y la verdad que querés conocer.

Formalmente, si tenés un estimador `T` que apunta a un parámetro poblacional `θ` (theta, la verdad que no conocés), el sesgo es:

$$
\text{Bias}(T) = E(T) - \theta
$$

donde `E(T)` es la **esperanza** (el promedio de `T` si repitieras el muestreo infinitas veces). Si `Bias(T) = 0`, el estimador es **insesgado** (también llamado *centrado*). Si no, todas tus estimaciones se corren en la misma dirección, por más datos que juntes.

En machine learning, la cátedra lo define como *"la diferencia consistente entre las predicciones del modelo y los valores reales"*. Mismo concepto, otro nombre.

## Intuición

Imaginate una balanza de almacén con un dedo apretándola por abajo. Cada vez que pesás, el resultado se va para arriba un poquito. No importa cuántas veces peses la misma bolsa de yerba: el promedio sigue mintiendo. El sesgo es ese dedo. La pregunta importante no es "¿cuánto se desvió el promedio?", sino **"¿quién puso el dedo y para qué lado?"**.

El ruido aleatorio sería que la balanza tiembla un poco y a veces marca más, a veces menos: ese error se promedia y desaparece. El sesgo NO se promedia. Más datos no salvan a una balanza mal calibrada.

---

## El dilema sesgo-varianza

Cuando entrenás un modelo y lo evaluás con error cuadrático, ese error se descompone en tres partes:

$$
E[(Y - \hat{Y})^2] = \text{Bias}^2 + \text{Var} + \sigma^2
$$

- **Bias²**: cuán lejos está el promedio de tus predicciones de la verdad. Modelos demasiado simples (una recta para algo curvo) tienen sesgo alto.
- **Var** (varianza): cuán inestables son tus predicciones cuando cambia un poco la muestra. Modelos demasiado complejos (un polinomio de grado 50) tienen varianza alta.
- **σ²** (sigma cuadrado): el ruido irreducible. La realidad misma tiene aleatoriedad que ningún modelo puede capturar.

### Diana de tiro

Pensá un tirador apuntando al blanco:

| | **Baja varianza** | **Alta varianza** |
|---|---|---|
| **Bajo sesgo** | Tiros agrupados en el centro (ideal) | Tiros dispersos alrededor del centro |
| **Alto sesgo** | Tiros agrupados pero corridos del centro | Tiros dispersos y corridos del centro |

El tirador con bajo sesgo y baja varianza es lo que querés. El de alto sesgo y baja varianza es peligroso: parece preciso (los tiros están todos juntos) pero está mintiéndote sistemáticamente. Es el modelo que se "ve bien en validación" pero le está errando al objetivo real.

El dilema (en inglés *bias-variance tradeoff*) es que bajar uno suele subir el otro. Modelos más flexibles bajan sesgo pero suben varianza; modelos más rígidos hacen lo contrario. La regularización (por ejemplo Ridge o Lasso) es justamente un mecanismo para equilibrar este tira y afloja.

---

## Tipos de sesgo

### Fuentes generales

Estas fuentes aparecen en cualquier estudio, no solo en ML:

- **Sesgo de selección / recolección**: tu muestra no es aleatoria respecto de la población objetivo. Capturaste ciertos perfiles y dejaste otros afuera sin querer. Es el padre de varios sub-tipos (los vemos abajo).
- **Sesgo de información**: hay errores en los datos que registraste, o registraste cosas incompletas. No es que falte gente: es que los datos de la gente que tenés están torcidos.
- **Sesgo de respuesta**: la persona encuestada contesta de forma inexacta. Puede ser por **deseabilidad social** (queremos quedar bien: "sí, hago deporte tres veces por semana"), por memoria limitada (no me acuerdo cuánto gasté el mes pasado) o por incentivos del propio cuestionario.
- **Sesgo de medición**: el instrumento mide mal de forma sistemática. Una balanza descalibrada, un sensor que se va con la temperatura, una pregunta ambigua.
- **Sesgo de publicación** (en inglés *file drawer effect*, "efecto del cajón"): solo se publican resultados estadísticamente significativos. Los experimentos que dieron "nada interesante" quedan en el cajón. Cuando hacés meta-análisis, ves un mundo distorsionado: parece que todo funciona, porque los fracasos no llegaron a imprenta.

### Sub-tipos de sesgo de selección/muestreo

El sesgo de selección se ramifica:

- **Autoselección**: los participantes deciden si participan. El que se anota a la encuesta no representa a "todos": representa a "los que se anotan a encuestas". Sysarmy, encuestas de satisfacción online, reviews de productos. Sobrerrepresenta perfiles entusiastas o muy enojados; subrepresenta indiferentes.
- **Selección de área específica**: muestreás en un solo barrio, una sola provincia, una sola universidad. Lo que valga ahí no vale afuera.
- **Exclusión**: ciertos grupos quedan afuera por diseño o por accidente. Por ejemplo: encuestar por internet excluye a quien no tiene internet.
- **Sesgo de supervivencia** (en inglés *survivorship bias*): solo ves a los que "pasaron el proceso". Los que no pasaron desaparecieron de tus datos y los olvidás. Es el sesgo más traicionero porque ni siquiera te das cuenta de qué te falta: por definición, los que faltan no aparecen.
- **Pre-selección**: reclutás desde un grupo particular (alumnos de tu curso, empleados de tu empresa). Lo que valga ahí no se extrapola.

### Sesgo de procesamiento (curado)

Este aparece en nuestra etapa, la de **curación**. Lo introducís vos sin querer al limpiar:

- Tratamiento incorrecto de faltantes (imputar con media cuando la pérdida no es MCAR).
- Unión mal hecha de cohortes que no son comparables.
- Escalado o normalización aplicados antes de separar train/test.
- **Cherry picking**: elegir el corte o filtro que da el resultado que te conviene.
- Eliminar outliers sin justificar — y de paso barrer evidencia legítima.

### Sesgos en ML (datasets automáticos)

Cuando entrenás modelos sobre datos del mundo real, aparecen:

- **Sesgo de omisión**: faltan variables relevantes. Tu modelo no puede capturar lo que no le mostraste.
- **Deriva** (en inglés *data drift*): el proceso que generaba los datos cambió. Entrenaste con datos de 2019 y ahora estás prediciendo 2026: ya no es la misma distribución.
- **Sesgo de contenido social**: los datos reflejan estereotipos, prejuicios o desigualdades del mundo. El modelo los aprende como si fueran "verdad".
- **Sesgo de respuesta/opinión**: corpus como Amazon reviews, tweets o Wikipedia están dominados por ciertas voces. Quien no twittea no existe para el modelo.
- **Sesgo de retroalimentación** (en inglés *feedback loop*): el modelo influye en los datos que va a recibir mañana. Si tu sistema de recomendación muestra siempre lo mismo, los clics futuros confirman esa elección y la profundizan.

---

## Casos famosos

### Países Bajos, 2013 — escándalo del subsidio infantil

El gobierno holandés desplegó un sistema de IA para detectar fraude en los subsidios por hijos. El modelo terminó marcando como "alto riesgo" a familias por ser extranjeras o tener ingresos bajos. Miles de familias fueron acusadas de fraude, obligadas a devolver dinero que no tenían, y muchas terminaron en la ruina o con sus hijos puestos en guarda estatal.

¿De dónde salió ese sesgo? De los datos de entrenamiento: históricamente, las inspecciones manuales se concentraban en esos grupos. El modelo aprendió la práctica discriminatoria del pasado y la amplificó a escala industrial. No "descubrió" fraude; **automatizó un sesgo humano preexistente**. El sistema fue cancelado en 2020 y derivó en la renuncia del gobierno de Rutte en 2021.

La lección dura: un modelo nunca es "neutral" porque las matemáticas sean neutrales. Es tan sesgado como los datos con los que lo alimentás. Y a diferencia de un inspector humano, opera a millones de personas por día.

### Tay (Microsoft, 2016)

Microsoft lanzó **Tay**, un chatbot en Twitter pensado para aprender conversando con usuarios reales. La idea era que se hiciera más simpático y "millennial" con el tiempo. En menos de 24 horas, Tay se había vuelto racista, misógina y antisemita, repitiendo barbaridades que le habían enseñado coordinadamente trolls de 4chan.

Acá conviven dos sesgos: el de **contenido social** (los inputs venían del peor sub-conjunto de Twitter) y el de **retroalimentación** (Tay aprendía de lo que respondía la gente, y respondía cada vez peor lo que la gente le seguía mandando). Microsoft tuvo que sacarla de circulación a las 16 horas. El caso es de manual: un sistema que aprende sin filtros del entorno, replica el peor entorno.

### Abraham Wald y los aviones de la WWII (sesgo de supervivencia)

Durante la Segunda Guerra Mundial, los militares aliados estudiaban los aviones que volvían de misiones y miraban dónde tenían impactos de bala. La intuición era: "reforcemos el blindaje en las zonas más impactadas". Las zonas más impactadas eran las alas y la cola.

**Abraham Wald**, matemático del Statistical Research Group, dijo: están todos equivocados. Los aviones que ven son los que **volvieron**. Los aviones impactados en el motor o en la cabina no volvieron — están en el fondo del Canal de la Mancha. La conclusión correcta era reforzar **donde NO hay impactos en los aviones supervivientes**, porque ahí es donde un impacto resulta fatal.

Es el ejemplo canónico de sesgo de supervivencia. Tus datos son una muestra de "los que sobrevivieron al proceso" y razonar como si fueran "todos" te lleva a la conclusión exactamente opuesta a la correcta. Aplica idéntico a startups exitosas, fondos de inversión que duran 10 años, alumnos que aprobaron la materia.

---

## Workflow correctivo

No vas a eliminar el sesgo del todo, pero podés gestionarlo en tres momentos:

### Planificación
- Definir explícitamente la **población objetivo**: ¿a quién querés generalizar?
- Diseñar un **marco de muestreo** que cubra esa población. Idealmente, muestreo aleatorio. Si no podés, dejarlo documentado.
- Evitar el muestreo por **conveniencia** ("los que tenía a mano").

### Comienzo
- Ingresar **pesos** para compensar desbalances conocidos (ej. ponderar por edad o región si tu muestra tiene una composición distinta a la población).
- Diseñar encuestas cortas y claras para minimizar abandonos y sesgo de respuesta.

### Desarrollo
- Hacer seguimiento a los que **no responden**: muchas veces los no respondedores son sistemáticamente distintos de los respondedores. Si podés caracterizarlos, podés corregir.
- Documentar cada decisión de limpieza con justificación escrita. El sesgo de procesamiento se introduce a escondidas; el remedio es ponerlo a la luz.

---

## Ejemplo numérico — Encuesta con autoselección

Querés estimar qué porcentaje de la población general usa Linux como sistema operativo principal. Hacés una encuesta online y la difundís en foros técnicos, listas de correo de software libre y un par de servidores Discord de programación.

Supongamos la verdad poblacional (que no conocés): el **3%** de la población general usa Linux como SO principal.

Tu encuesta junta **2.000 respuestas**, de las cuales **600 dicen usar Linux**. Calculás:

$$
\hat{p} = \frac{600}{2000} = 0{,}30 = 30\%
$$

Reportás "el 30% de la población usa Linux". El número es preciso (muestra grande, varianza chica) pero está **sistemáticamente inflado por sesgo de autoselección**: difundir la encuesta en foros técnicos sobrerrepresenta enormemente a usuarios de Linux. La gente que no usa Linux ni se enteró de tu encuesta, o no le interesó contestar.

El sesgo es:

$$
\text{Bias} = E(\hat{p}) - p = 0{,}30 - 0{,}03 = +0{,}27 \quad (\text{27 puntos porcentuales para arriba})
$$

Conclusión:
- Más respuestas no arreglan nada: si juntás 20.000 en los mismos foros, vas a obtener `~30%` igual. La varianza baja, el sesgo queda.
- El intervalo de confianza tampoco te salva: te va a dar un intervalo angosto alrededor de un número equivocado.
- La única solución real es **cambiar el marco de muestreo** (encuestar a la población general, no a foros técnicos) o aplicar **pesos** que corrijan la sobrerrepresentación si tenés un padrón externo confiable.

---

## Conexión con el TP

- **TP1, eliminar outliers**: cuando aplicás IQR sobre `Price`, `Landsize` o `BuildingArea`, estás introduciendo sesgo de procesamiento. Las propiedades muy caras o muy grandes son datos reales que existen en Melbourne, no errores. Si las descartás "para que el modelo ande mejor", estás definiendo implícitamente que tu modelo solo aplica al mercado "típico", no al de lujo. Eso hay que **escribirlo en el documento técnico** del TP1, no esconderlo. Si después alguien usa tu modelo para tasar una mansión, va a errar fuerte y va a ser culpa tuya por no aclarar el alcance.

- **TP1, reducir cardinalidad de Suburb / SellerG / CouncilArea**: agrupar suburbios con pocas observaciones en una categoría "Otros" es razonable para que el OHE no explote, pero es sesgo de procesamiento. Las propiedades de esos suburbios pierden su identidad geográfica. Justificá con un umbral concreto (por ejemplo, "agrupé suburbios con menos de 30 observaciones") y mencioná que esa decisión sesga las predicciones de propiedades en barrios chicos.

- **TP2, merge con AirBnB**: cuando hacés `merge` por `Postcode` / `zipcode`, los zipcodes que aparecen en `melb_data` pero no en el dataset de AirBnB se quedan con `NaN` en las columnas de AirBnB. Eso es **sesgo geográfico**: solo enriqueciste con AirBnB las zonas donde AirBnB tiene presencia, que son típicamente las turísticas o céntricas. Las zonas periféricas quedan sin enriquecimiento. Si después usás las features de AirBnB para predecir precios, vas a tener mejor performance en zonas céntricas y peor en periféricas — y vas a pensar que es un problema del modelo, cuando en realidad es sesgo de la curación.

- **TP2, filtrar por dominio (`Price > 0`, etc.)**: cada filtro es una decisión metodológica. Documentá el orden: primero filtrás absurdos (errores de carga), después outliers estadísticos (IQR). Si invertís el orden, el IQR se distorsiona y termina marcando como outliers a observaciones legítimas.

---

## Errores comunes

1. **Confundir sesgo con ruido**. El ruido es aleatorio y se cancela; el sesgo no. Más datos no curan sesgo.
2. **Creer que un modelo es "neutral" porque la matemática es neutral**. Los datos llevan la huella de quién los recolectó y cómo. Países Bajos 2013 te lo recuerda.
3. **Reportar resultados sin mencionar el marco de muestreo**. Si tu muestra no representa a la población objetivo, decirlo no es debilidad: es honestidad metodológica.
4. **Eliminar outliers automáticamente "para que dé lindo"**. Es cherry picking disfrazado de limpieza.
5. **Aplicar IQR sobre datos con absurdos sin filtrarlos antes**. Un valor de $5 y otro de $999.999.999 distorsionan los cuartiles y arrastran outliers legítimos.
6. **Olvidar el sesgo de supervivencia**. Si estudiás "qué hacen las empresas exitosas", estás mirando solo a los aviones que volvieron.
7. **Imputar faltantes con media cuando la pérdida no es MCAR**. La media supone que los faltantes son intercambiables con los observados; si la pérdida está correlacionada con la variable, estás inventando datos para el lado equivocado.

---

## Checklist de comprensión

- [ ] ¿Cuál es la diferencia entre sesgo y varianza, y por qué un modelo con "bajo sesgo y alta varianza" puede ser preferible a uno con "alto sesgo y baja varianza"?
- [ ] En la encuesta Sysarmy o en cualquier encuesta online voluntaria, ¿qué sub-tipo de sesgo de selección domina y por qué más respuestas no lo curan?
- [ ] Si en TP1 eliminás los outliers de `Price` con IQR, ¿qué tipo de sesgo introduciste y cómo lo justificás en el documento técnico?
- [ ] ¿Por qué Abraham Wald recomendó blindar las partes del avión sin impactos, y qué tiene que ver eso con elegir features para un modelo basándose en clientes que renovaron contrato?

---

**Próximo paso**: `04-tipos-de-variables-y-encodings.md`
