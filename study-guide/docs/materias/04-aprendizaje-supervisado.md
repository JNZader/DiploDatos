# Materia 4 — Aprendizaje Supervisado

> **Idea rectora:** un algoritmo no es una caja con una puntuación. Es una preferencia sobre qué patrones parecen simples, una forma de convertir datos en decisiones y un conjunto de costos, límites y errores. Aprender a compararlos exige mantener fijo el experimento y cambiar una decisión por vez.

Esta materia es autocontenida y conceptual. No necesitás abrir un notebook para seguirla. La implementación queda deliberadamente después de la comprensión: primero intuición, vocabulario, ejemplo trabajado, fórmula explicada símbolo por símbolo, interpretación, error frecuente, checkpoint y transferencia a SAIJ. Recién con ese mapa tendría sentido traducir decisiones a una biblioteca.

No se afirmará que una familia “gana” para SAIJ. Todavía falta reproducir el dataset, fijar el target operativo, establecer particiones válidas y ejecutar comparaciones controladas. Toda cifra de los ejemplos es inventada y sirve únicamente para razonar.

---

## 0. Cómo estudiar esta materia

### 0.1 Qué deberías poder hacer al terminar

Al completar la Materia 4 deberías poder:

1. explicar qué es el sesgo inductivo de una familia y por qué no existe aprendizaje sin alguna preferencia;
2. comparar modelos según geometría, escalado, capacidad, representación, interpretabilidad y costo;
3. reconstruir el score, la frontera y la probabilidad de una regresión logística;
4. distinguir regularización L1 de L2 y relacionarlas con complejidad, correlación y estabilidad;
5. explicar cómo un árbol divide recursivamente el espacio y por qué la profundidad puede sobreajustar;
6. describir hiperplano, margen, vectores soporte, margen blando, (C) y kernels en SVM;
7. diferenciar bagging, random forest y boosting sin reducirlos a “muchos árboles”;
8. adaptar pesos, muestreo y umbrales al desbalance sin contaminar validación ni test;
9. diseñar selección de hiperparámetros con validación compatible con grupos y tiempo;
10. decidir qué preprocesamiento necesita cada familia y encapsularlo conceptualmente en un pipeline;
11. separar score, margen, probabilidad, calibración y decisión;
12. interpretar coeficientes e importancias sin convertir asociación predictiva en causalidad;
13. comparar costos de entrenamiento, inferencia, memoria y representación dispersa;
14. registrar experimentos reproducibles y redactar una ficha liviana de modelo;
15. analizar errores por clase, confusión, tiempo, geografía, tipo documental y longitud;
16. proponer una escalera SAIJ desde la mayoría hasta familias más complejas sin proclamar un ganador;
17. combinar clasificación multiclase, abstención y revisión humana;
18. justificar cada decisión sin empezar por código.

### 0.2 Convenciones de evidencia

Se mantienen los cuatro rótulos del libro:

| Rótulo | Uso en esta materia |
|---|---|
| **Teoría** | Propiedades generales de las familias supervisadas. |
| **Ejemplo ilustrativo inventado** | Números pequeños creados para calcular o comparar; nunca describen SAIJ. |
| **Hallazgo del equipo — pendiente de reproducción** | Cualquier resultado proveniente del notebook grupal; no se transforma en evidencia propia de Javier. |
| **Decisión pendiente de Javier** | Target, unidad, clases, partición, métrica, costo, umbral o política operacional que todavía debe justificarse. |

Una quinta marca será útil:

| Rótulo | Uso |
|---|---|
| **Contexto opcional** | Idea que amplía la intuición, pero no se exige para dominar el nivel de la Diplomatura. |

### 0.3 Alcance local y límite deliberado

Los materiales locales verificados de Aprendizaje Supervisado organizan el núcleo alrededor de SVM y kernels, redes neuronales, random forest, boosting, sistemas de recomendación y buenas prácticas. Esta guía desarrolla especialmente las familias necesarias para construir una comparación defendible del futuro clasificador de fuero: modelos lineales, árboles, SVM y ensambles. Regresión logística y árboles se explican también como bases conceptuales indispensables para entender fronteras, probabilidades, regularización y ensambles.

**k-NN no se desarrolla como familia central.** El inventario local disponible no lo presenta como eje de esta cursada y la instrucción de alcance pide incluirlo solo si está respaldado por las fuentes locales. No se rellena ese hueco con material externo. Esta omisión no implica que k-NN sea inútil; significa que el libro respeta el límite declarado. En particular, no vamos a introducir distancia, elección de (k), maldición de la dimensionalidad y limitaciones en texto como si hubieran sido parte del trayecto local verificado.

Las redes neuronales y los recomendadores aparecen únicamente como frontera del programa, no como bloque central. Para el problema SAIJ primero interesa dominar controles simples, modelos lineales, SVM y ensambles clásicos. “Acotado” limita cuántas familias se estudian; no vuelve superficial la explicación de las elegidas.

### 0.4 Método de lectura

Para cada familia seguí ocho pasos:

```text
intuición
  → vocabulario
  → ejemplo pequeño
  → fórmula símbolo por símbolo
  → interpretación
  → error frecuente
  → checkpoint
  → transferencia a SAIJ
```

Después resolvé el ejercicio conceptual sin mirar la respuesta. No memorices “este modelo requiere escalado”: preguntate qué operación interna hace que el escalado importe. No memorices “los árboles sobreajustan”: explicá qué decisiones permiten que una hoja termine describiendo uno o pocos ejemplos.

> **Checkpoint inicial**
>
> Si dos modelos usan exactamente el mismo train y uno obtiene una métrica mayor, ¿ya podés declararlo mejor? No. Primero hay que comprobar que la selección no miró test, que la diferencia es estable entre particiones relevantes, que el costo y los errores por clase son aceptables, y que ambos reciben representaciones comparables y legítimas.

---

## 1. Del marco experimental a una regla concreta

### 1.1 Qué agrega una familia de modelos

En Materia 3 escribimos el aprendizaje como una búsqueda de una función (f) que aproxima la relación entre entradas (x) y targets (y). Pero “buscar una función” es demasiado amplio. Una familia acota el conjunto de funciones candidatas y define qué cambios resultan fáciles o difíciles.

Un clasificador lineal busca fronteras planas en el espacio de features. Un árbol construye regiones mediante preguntas sucesivas. Una SVM lineal también separa con un hiperplano, pero elige la separación a partir del margen. Un bosque promedia árboles variados. Un boosting corrige errores de manera secuencial. Cada uno mira la misma tabla a través de una geometría distinta.

Ese modo de mirar es el **sesgo inductivo**. La palabra “sesgo” no significa aquí prejuicio injusto ni error sistemático. Significa preferencia de aprendizaje: entre varias reglas compatibles con train, la familia favorece algunas.

### 1.2 Por qué el sesgo inductivo es inevitable

Imaginá tres puntos observados de una secuencia: (2, 4, 6). Podríamos prolongarla como (8, 10), pero también existen infinitas reglas que coinciden en los tres valores y luego cambian. Elegimos la continuación simple porque preferimos regularidad. Un modelo hace algo equivalente mediante su arquitectura, pérdida y regularización.

Sin preferencia, los datos finitos no determinan una única regla para casos futuros. Por eso la pregunta correcta no es “¿este modelo tiene sesgo?”, sino “¿su sesgo coincide razonablemente con la estructura del problema?”.

### 1.3 Ejemplo inventado: dos regularidades posibles

Supongamos documentos representados por dos features:

- (x_1): presencia ponderada de términos relacionados con tributos;
- (x_2): presencia ponderada de términos relacionados con relaciones laborales.

Una frontera lineal podría separar documentos cuando (x_1-x_2>0). Esa regla supone que una combinación aditiva alcanza. Un árbol podría preguntar primero si (x_1>0.7) y, si no, si (x_2<0.2). Esa regla crea regiones rectangulares y admite interacciones abruptas.

Ninguna geometría es “más inteligente” por sí sola. Si la señal real se distribuye entre miles de palabras sumando evidencia débil, la linealidad puede ser una excelente preferencia. Si unas pocas reglas condicionales sobre metadata dominan, un árbol puede representarlas de forma compacta. Esto debe probarse.

### 1.4 Material complementario integrado 1/8 — sesgo inductivo por familia

| Familia | Preferencia aproximada | Puede favorecer | Puede dificultar |
|---|---|---|---|
| Regresión logística | Efectos aditivos sobre el log-odds y frontera lineal | Muchas señales pequeñas y dispersas | Interacciones complejas no expresadas como features |
| SVM lineal | Separación con margen amplio | Texto disperso de alta dimensión | Probabilidades directas e interacciones no lineales |
| Árbol | Reglas condicionales y cortes por feature | Umbrales, interacciones, escalas mixtas | Fronteras suaves; estabilidad ante pequeños cambios |
| Random forest | Promedio de árboles diversos | No linealidad con menor varianza que un árbol | Explicación compacta; matrices de texto gigantes |
| Boosting | Corrección secuencial de errores | Patrones tabulares sutiles | Ruido, tuning sensible y mayor costo secuencial |

La tabla no decide. Formula hipótesis que luego deben contrastarse bajo el mismo split.

> **Error frecuente:** llamar “modelo sin supuestos” a un árbol o a un ensamble. Tal vez no suponga linealidad, pero sí incorpora preferencias sobre tipos de cortes, profundidad, reducción de impureza, muestreo y agregación.

> **Checkpoint 1**
>
> ¿Por qué agregar bigramas puede cambiar el sesgo efectivo de una regresión logística? Porque la familia sigue siendo lineal respecto de sus columnas, pero la representación ahora incluye interacciones lingüísticas locales ya construidas. La frontera es lineal en un espacio más expresivo.

### 1.5 Transferencia a SAIJ

Para el futuro clasificador de fuero, el sesgo inductivo se discute junto con la representación. TF-IDF produce miles de columnas dispersas; allí una familia lineal puede sumar evidencia distribuida sin convertir la matriz en densa. Metadata tabular curada puede exhibir umbrales o interacciones que un árbol aproveche. Combinar texto y metadata exige verificar compatibilidad, memoria y riesgo de shortcuts.

**Decisión pendiente de Javier:** definir si el primer alcance usa solo texto legítimo, solo metadata legítima o una unión auditable. El notebook del equipo puede orientar preguntas, pero cualquier hallazgo que sugiera una feature “muy predictiva” sigue pendiente de reproducción y de un examen de fuga.

> **Ejercicio conceptual 1**
>
> Un árbol supera a un modelo lineal usando una columna `dependencia_origen`. ¿Qué dos explicaciones incompatibles deberías investigar antes de celebrar?
>
> **Respuesta razonada:** podría existir una interacción legítima entre dependencia y fuero, o la columna podría codificar casi directamente la etiqueta por una regla administrativa. La segunda sería un shortcut o fuga semántica. Hay que revisar linaje, disponibilidad al momento de inferencia y generalización a nuevas dependencias.

---

## 2. Marco común para comparar familias

### 2.1 Comparar no es mirar una sola métrica

Una comparación útil conserva el protocolo y observa varias dimensiones. Una familia puede mejorar macro F1 pero duplicar el tiempo de inferencia, requerir memoria densa, degradar calibración o aumentar errores en una clase crítica. Otra puede puntuar un poco menos y ser más estable, explicable y fácil de revisar.

El marco mínimo contiene siete preguntas:

1. **Sesgo inductivo:** ¿qué patrones considera simples?
2. **Geometría:** ¿cómo divide o organiza el espacio de features?
3. **Escalado:** ¿cambiar unidades altera el aprendizaje?
4. **Capacidad:** ¿cuánta complejidad puede representar?
5. **Interpretabilidad:** ¿qué explicación global y local admite?
6. **Costo computacional:** ¿qué consume al entrenar, inferir y almacenar?
7. **Representación compatible:** ¿acepta matrices dispersas, densas, categorías, texto o combinaciones?

### 2.2 Una ficha de comparación antes de entrenar

| Dimensión | Lineal/logística | Árbol | SVM lineal | Random forest | Boosting de árboles |
|---|---|---|---|---|---|
| Frontera | Hiperplano | Regiones por cortes | Hiperplano de margen amplio | Votación de muchas regiones | Suma secuencial de reglas |
| Escalado | Recomendado; afecta regularización | Poco sensible a escalas monotónicas | Importante | Poco sensible | Poco sensible en árboles |
| Capacidad | Controlada por features y regularización | Crece con profundidad y hojas | Controlada por (C) y representación | Alta, moderada por promedio y límites | Alta y secuencial, controlada por tasa y complejidad |
| Disperso | Muy compatible | Posible, no siempre conveniente | Muy compatible | Puede ser costoso | Depende de implementación y representación |
| Probabilidad nativa | Sí en logística | Frecuencia por hoja, a menudo poco calibrada | No necesariamente | Promedio de votos/proporciones, no garantía de calibración | Scores o probabilidades según pérdida, no garantía de calibración |
| Explicación | Coeficientes | Reglas de un árbol | Pesos y margen | Importancias y explicaciones agregadas | Contribuciones agregadas, más complejas |
| Inferencia | Producto vectorial rápido | Ruta de decisiones | Producto vectorial rápido | Muchas rutas | Secuencia de aprendices |

La ficha es una predicción metodológica, no un resultado. Después del experimento se completa con tiempos, memoria, métricas y errores observados.

### 2.3 Capacidad y complejidad no son sinónimos de calidad

La **capacidad** describe la variedad de funciones que una familia puede representar. Si es insuficiente, aparece subajuste: el modelo no captura señal disponible. Si es excesiva respecto de los datos y controles, puede aprender ruido: sobreajuste.

Agregar profundidad, hojas, kernels flexibles o etapas de boosting aumenta capacidad de modos distintos. Agregar features también. La regularización y la validación no “castigan a los modelos buenos”; buscan elegir la complejidad que generaliza.

### 2.4 Geometría de datos y representación

La misma observación puede ocupar espacios diferentes. Un documento como bolsa de palabras es un vector disperso de alta dimensión. Como embedding sería un vector denso de menor dimensión. Como tabla de metadata tendría columnas heterogéneas. No hay una única geometría “del documento”; la representación la construye.

Esto explica por qué preguntar “¿árbol o SVM?” sin especificar features es incompleto. El algoritmo opera sobre números, no sobre el significado jurídico directo. Su comportamiento depende de cómo esos números preservan frecuencia, similitud, categorías y relaciones.

> **Error frecuente:** comparar una SVM con TF-IDF contra un bosque con metadata y atribuir toda diferencia al algoritmo. Cambiaron dos factores: familia y representación. La comparación no identifica cuál causó la diferencia.

> **Checkpoint 2**
>
> ¿Cuándo una comparación es “justa”? No cuando todos reciben idénticas columnas a la fuerza, sino cuando cada pipeline usa solo información legítima, ajusta su preprocesamiento dentro de train y permite atribuir diferencias mediante experimentos controlados.

### 2.5 Transferencia a SAIJ

Antes de ejecutar, una tabla de hipótesis podría registrar:

| Candidato | Representación propuesta | Hipótesis | Riesgo |
|---|---|---|---|
| Mayoría | Ninguna | Control mínimo | Oculta clases minoritarias |
| Naive Bayes | Conteos o TF-IDF compatible | Señales léxicas por clase | Independencia aproximada y calibración |
| Logística | TF-IDF escalado implícitamente por construcción | Evidencia aditiva dispersa | Coeficientes correlacionados |
| SVM lineal | TF-IDF | Margen amplio en alta dimensión | Score no probabilístico |
| Bosque | Metadata curada o representación reducida justificada | Umbrales e interacciones | Costo, alta cardinalidad, shortcuts |
| Boosting | Tabla curada | Corrección de errores tabulares sutiles | Tuning, ruido, costo y fuga |

> **Ejercicio conceptual 2**
>
> Una familia obtiene mejor accuracy pero peor macro recall y tarda veinte veces más en inferencia. ¿Cuál gana?
>
> **Respuesta razonada:** no se puede decidir sin el objetivo. La caída de macro recall puede indicar daño en clases pequeñas, y el costo puede impedir el uso previsto. Deben definirse prioridades, incertidumbre y restricciones antes de resumir todo en un ganador.

---

## 3. Clasificadores lineales y regresión logística

### 3.1 Intuición: sumar evidencia

Un clasificador lineal asigna un peso a cada feature y suma sus contribuciones. Algunas empujan la decisión hacia una clase; otras la alejan; el intercepto establece un punto de partida.

En texto, esta idea es potente. Un documento puede contener muchas señales débiles: términos procesales, menciones de organismos, vocabulario tributario o laboral. El modelo no necesita que una palabra decida sola. Puede acumular indicios.

### 3.2 Vocabulario mínimo

- **Feature (x_j):** valor de la columna (j) para una observación.
- **Coeficiente (w_j):** peso aprendido para esa feature.
- **Intercepto (b):** término constante.
- **Score o logit (z):** suma ponderada antes de convertirla en probabilidad.
- **Frontera de decisión:** conjunto de puntos donde dos decisiones quedan empatadas.
- **Pérdida logística:** criterio de ajuste que penaliza probabilidades incompatibles con la clase real.
- **Regularización:** preferencia por coeficientes controlados.

### 3.3 Ejemplo trabajado: score lineal

**Ejemplo ilustrativo inventado.** Clasificamos entre “laboral” ((y=1)) y “no laboral” ((y=0)) usando dos features ya transformadas:

- (x_1): peso de vocabulario laboral;
- (x_2): peso de vocabulario tributario.

Supongamos que el modelo aprendió:

[
z = b + w_1x_1 + w_2x_2
]

con (b=-0.4), (w_1=1.8), (w_2=-1.2). Para un documento con (x_1=0.9) y (x_2=0.2):

[
z=-0.4+(1.8)(0.9)+(-1.2)(0.2)=0.98
]

**Símbolo por símbolo:**

- (z) es el score total del documento;
- (b) es la evidencia base cuando las features valen cero;
- (w_1) mide cuánto cambia el score por una unidad de (x_1), manteniendo las demás columnas fijas;
- (x_1) es el valor observado de la primera feature;
- (w_2) cumple el mismo papel para la segunda feature;
- (x_2) es su valor observado;
- el signo positivo de (w_1) empuja hacia laboral;
- el signo negativo de (w_2) empuja en sentido contrario.

El score (0.98) no es todavía una probabilidad. Es una posición respecto de la frontera. En el caso binario con umbral usual, (z=0) separa las decisiones. Como (0.98>0), el documento quedaría del lado positivo.

### 3.4 De score a probabilidad: la sigmoide

La regresión logística transforma el score mediante:

[
p(y=1\mid x)=\sigma(z)=\frac{1}{1+e^{-z}}
]

**Símbolo por símbolo:**

- (p(y=1\mid x)) es la probabilidad estimada de la clase positiva dado el vector (x);
- (\sigma) nombra la función sigmoide;
- (z) es el score lineal calculado antes;
- (e) es la base de los logaritmos naturales;
- (-z) invierte el sentido dentro de la exponencial;
- el denominador (1+e^{-z}) mantiene el resultado entre 0 y 1.

Para (z=0.98), la sigmoide produce aproximadamente (0.727). La interpretación prudente es: **según este modelo y sus datos de entrenamiento**, la estimación para la clase positiva es cercana a 0.73. No significa que el documento “sea 73 % laboral” ni garantiza calibración perfecta.

Cuando (z=0), la probabilidad es (0.5). Scores grandes y positivos se acercan a 1; grandes y negativos se acercan a 0. La sigmoide cambia la escala, no agrega evidencia nueva.

### 3.5 Log-odds y coeficientes

La misma relación puede escribirse:

[
\log\left(\frac{p}{1-p}\right)=b+\sum_{j=1}^{d}w_jx_j
]

**Símbolo por símbolo:**

- (p) es la probabilidad estimada de la clase positiva;
- (1-p) es la de la clase negativa;
- (p/(1-p)) son los *odds*;
- (\log) convierte esos odds multiplicativos en una escala aditiva;
- (d) es la cantidad de features;
- (j) recorre las features;
- (\sum) suma sus contribuciones;
- (w_jx_j) es la contribución lineal de la feature (j).

Si una feature aumenta una unidad y todo lo demás permanece fijo, los log-odds cambian en (w_j). Los odds se multiplican por (e^{w_j}). Esta interpretación exige cuidado: en TF-IDF “una unidad” puede no ser intuitiva y las features correlacionadas comparten señal. Un coeficiente no es efecto causal.

### 3.6 Frontera de decisión

Con dos features y umbral 0.5, la frontera satisface:

[
b+w_1x_1+w_2x_2=0
]

Todos los puntos de un lado generan score positivo; los del otro, score negativo. En dimensiones altas sigue siendo un hiperplano, aunque no podamos dibujarlo. Agregar n-gramas, interacciones o transformaciones curva la frontera respecto del dato original sin dejar de ser lineal en el espacio transformado.

### 3.7 Pérdida logística

Para una observación binaria, la pérdida es:

[
\ell(y,p)=-\left[y\log(p)+(1-y)\log(1-p)\right]
]

**Símbolo por símbolo:**

- (\ell) es la pérdida de una observación;
- (y) vale 1 para la clase positiva y 0 para la negativa;
- (p) es la probabilidad estimada de la positiva;
- (\log(p)) recompensa asignar probabilidad alta cuando (y=1);
- (\log(1-p)) hace lo mismo para la negativa;
- el signo menos convierte logaritmos negativos en una pérdida positiva.

Si el caso real es positivo, queda (-\log p): predecir (p=0.9) cuesta poco; predecir (p=0.01) cuesta mucho. La pérdida no trata igual una equivocación dudosa que una equivocación extremadamente confiada.

### 3.8 Regularización L2 y L1

El ajuste suele minimizar una combinación:

[
J(w,b)=\frac{1}{n}\sum_{i=1}^{n}\ell\left(y_i,p_i\right)+\lambda\,\Omega(w)
]

**Símbolo por símbolo:**

- (J) es el objetivo total a minimizar;
- (n) es la cantidad de observaciones de train;
- (i) recorre esas observaciones;
- (\ell(y_i,p_i)) es la pérdida predictiva del caso (i);
- (\Omega(w)) mide complejidad de los coeficientes;
- (\lambda) controla cuánto pesa esa complejidad frente al ajuste.

Para L2:

[
\Omega_{L2}(w)=\sum_{j=1}^{d}w_j^2
]

L2 castiga con fuerza coeficientes muy grandes y suele repartir señal entre features correlacionadas. Reduce varianza y estabiliza, pero no suele volver exactamente cero muchos pesos.

Para L1:

[
\Omega_{L1}(w)=\sum_{j=1}^{d}|w_j|
]

L1 suma valores absolutos y puede llevar coeficientes exactamente a cero. Eso produce una forma de selección, aunque “cero” no significa irrelevancia jurídica: con términos correlacionados, el modelo puede conservar uno y descartar otro de manera inestable.

Algunas bibliotecas parametrizan la fuerza con (C) en lugar de (\lambda). Frecuentemente, (C) actúa de forma inversa: (C) grande implica regularización más débil; (C) pequeño, regularización más fuerte. Nunca hay que interpretar el nombre sin revisar la convención de la herramienta elegida.

### 3.9 Escalado

La regularización compara magnitudes de coeficientes. Si una feature varía entre 0 y 1 y otra entre 0 y 100 000, sus pesos necesitan escalas distintas para producir cambios comparables. El castigo puede entonces depender arbitrariamente de unidades.

Estandarizar una feature suele usar:

[
x'_{ij}=\frac{x_{ij}-\mu_j}{s_j}
]

donde (x_{ij}) es el valor original de la observación (i) en la feature (j), (\mu_j) es la media calculada **solo en train**, (s_j) es su desvío estándar de train y (x'_{ij}) es el valor transformado. Validación y test usan los mismos (\mu_j) y (s_j), nunca los recalculan.

En texto TF-IDF, la representación ya tiene otra lógica de normalización y suele conservarse dispersa. Centrar una matriz dispersa restando medias puede llenarla de valores no cero y destruir su ventaja de memoria. El escalado no es una receta única; depende de representación y familia.

### 3.10 Multiclase y softmax

Para (K) clases, una regresión logística multinomial calcula un score por clase:

[
z_k=b_k+w_k^Tx
]

y los convierte en probabilidades con softmax:

[
p(y=k\mid x)=\frac{e^{z_k}}{\sum_{r=1}^{K}e^{z_r}}
]

**Símbolo por símbolo:**

- (K) es el número total de clases;
- (k) identifica la clase cuya probabilidad calculamos;
- (z_k) es su score;
- (e^{z_k}) convierte ese score en una cantidad positiva;
- (r) recorre todas las clases en el denominador;
- la suma normaliza para que las probabilidades totalicen 1.

Softmax compara scores relativos. Sumar la misma constante a todos no cambia las probabilidades. Una clase puede recibir 0.55 no porque tenga evidencia absoluta fuerte, sino porque sus competidoras recibieron menos.

Otra estrategia es one-vs-rest: entrenar un clasificador por clase contra el resto. Sus scores no siempre forman probabilidades mutuamente coherentes sin pasos adicionales. La estrategia debe quedar registrada.

### 3.11 Material complementario integrado 7/8 — por qué el texto disperso suele favorecer modelos lineales

Un vocabulario puede crear decenas de miles de columnas y cada documento activa pocas. Los modelos lineales pueden calcular un producto entre pesos y valores no cero sin densificar la matriz. Además, una categoría jurídica puede manifestarse como suma de muchas pistas léxicas débiles, una estructura compatible con la aditividad.

Esto no demuestra que un lineal gane. Explica una razón de ingeniería y sesgo inductivo para incluirlo temprano. Los árboles deben buscar cortes entre muchísimas columnas casi siempre nulas y los ensambles repiten ese proceso muchas veces. Una representación densa reducida podría cambiar el panorama, pero también cambia la información y exige validación propia.

### 3.12 Error frecuente, checkpoint y transferencia

> **Error frecuente:** leer el coeficiente de una palabra como “importancia jurídica causal”. El peso depende del vocabulario, regularización, clase de referencia, escala y términos correlacionados. Describe la regla predictiva ajustada, no el derecho ni una relación causal.

> **Checkpoint 3**
>
> Si duplicamos todos los valores de una feature sin reentrenar, ¿qué ocurre? Su contribución (w_jx_j) se duplica. Si reentrenamos con regularización, el coeficiente puede reajustarse, pero la penalización y la optimización cambian; por eso las unidades importan.

**Transferencia a SAIJ.** Una regresión logística con TF-IDF sería un escalón razonable después de Naive Bayes porque mantiene compatibilidad con texto disperso, produce una frontera interpretable y permite probabilidades candidatas. “Razonable” no significa “ganadora”. Debe compararse con la misma partición, vocabulario aprendido solo en train, métricas multiclase, calibración y análisis de confusiones.

> **Ejercicio conceptual 3**
>
> Dos términos casi sinónimos tienen alta correlación. Con L1, uno queda con peso alto y otro en cero. ¿Podés concluir que el segundo no aporta nada?
>
> **Respuesta razonada:** no. L1 puede elegir un representante entre señales redundantes. Otra partición podría intercambiarlos. Hay que examinar estabilidad, grupos de features y desempeño por permutación, no convertir un cero en verdad sustantiva.

> **Ejercicio conceptual 4**
>
> Un documento obtiene softmax 0.42 para laboral, 0.40 para seguridad social y 0.18 para tributario. ¿Qué oculta elegir solo `argmax`?
>
> **Respuesta razonada:** oculta que las dos primeras clases están casi empatadas. La diferencia de 0.02 puede justificar abstención o revisión, especialmente si la confusión es costosa. La clase elegida no expresa por sí sola la incertidumbre.

---

## 4. Árboles de decisión

### 4.1 Intuición: una secuencia de preguntas

Un árbol clasifica mediante preguntas del tipo “¿esta feature es menor o igual que un umbral?”. Cada respuesta envía la observación a una rama. Después de varias preguntas llega a una hoja, donde se asigna una clase o distribución.

La intuición es cercana a una guía de decisión, pero un árbol entrenado no recibe reglas jurídicas escritas por una persona. Elige cortes que reducen impureza en train. Una pregunta legible puede apoyarse en una correlación espuria.

### 4.2 Vocabulario

- **Nodo:** conjunto de observaciones en una etapa.
- **Split o corte:** pregunta que divide un nodo.
- **Rama:** resultado del corte.
- **Hoja:** nodo terminal que produce predicción.
- **Profundidad:** número máximo de cortes desde raíz hasta hoja.
- **Impureza:** mezcla de clases dentro de un nodo.
- **Ganancia:** reducción de impureza conseguida por un split.
- **Poda o control:** restricción que evita ramas demasiado específicas.

### 4.3 Ejemplo trabajado

**Ejemplo ilustrativo inventado.** Tenemos 10 documentos en un nodo: 6 de clase A y 4 de clase B. Un corte sobre `longitud_normalizada <= 0.35` produce:

- rama izquierda: 4 A y 0 B;
- rama derecha: 2 A y 4 B.

La rama izquierda queda pura; la derecha todavía mezcla. El algoritmo evalúa si la reducción ponderada de impureza justifica el corte.

### 4.4 Impureza Gini

Para un nodo (t) con (K) clases:

[
G(t)=1-\sum_{k=1}^{K}p_{k\mid t}^{2}
]

**Símbolo por símbolo:**

- (G(t)) es la impureza Gini del nodo;
- (K) es la cantidad de clases;
- (k) recorre las clases;
- (p_{k\mid t}) es la proporción de la clase (k) dentro del nodo (t);
- elevar al cuadrado y sumar aumenta cuando una clase domina;
- restar de 1 da cero en una hoja pura y valores mayores cuando hay mezcla.

En el nodo inicial binario, (p_A=0.6) y (p_B=0.4):

[
G(t)=1-(0.6^2+0.4^2)=1-(0.36+0.16)=0.48
]

Para evaluar el corte calculamos impureza ponderada de los hijos:

[
G_{split}=\frac{n_L}{n}G(L)+\frac{n_R}{n}G(R)
]

donde (n) es el tamaño del nodo padre, (n_L) y (n_R) los tamaños de hijos, y (G(L)), (G(R)) sus impurezas. La ganancia es (G(t)-G_{split}). El árbol busca una reducción grande, sujeta a restricciones.

### 4.5 Entropía

Otra medida es:

[
H(t)=-\sum_{k=1}^{K}p_{k\mid t}\log_2 p_{k\mid t}
]

**Símbolo por símbolo:**

- (H(t)) es la entropía del nodo;
- (p_{k\mid t}) es la proporción de clase;
- (\log_2) mide información en base 2;
- el signo menos vuelve positivo el resultado;
- los términos con probabilidad cero se tratan como contribución cero por límite.

Gini y entropía expresan intuiciones cercanas: premiar nodos menos mezclados. No suelen justificar por sí solas una gran narrativa sustantiva. Son criterios locales de construcción.

### 4.6 Profundidad, hojas y sobreajuste

Si permitimos cortes hasta que cada hoja tenga uno o pocos ejemplos, el árbol puede memorizar train. Profundidad y número de hojas controlan cuántas regiones crea. Otros controles incluyen:

- cantidad mínima de observaciones para dividir un nodo;
- cantidad mínima por hoja;
- ganancia mínima exigida;
- máximo de features evaluadas;
- poda posterior mediante una penalización de complejidad.

Una forma conceptual de poda costo-complejidad es:

[
R_\alpha(T)=R(T)+\alpha|T|
]

**Símbolo por símbolo:**

- (T) es el árbol;
- (R(T)) es su error o impureza agregada en entrenamiento;
- (|T|) representa la cantidad de hojas;
- (\alpha) es el costo asignado a cada hoja adicional;
- (R_\alpha(T)) equilibra ajuste y tamaño.

Con (\alpha) pequeño se toleran más hojas; con (\alpha) grande se prefiere un árbol compacto. El valor se selecciona mediante validación, no mirando test.

### 4.7 Escalado y categorías

Los árboles comparan orden y umbrales. Multiplicar una feature por una constante positiva cambia el valor del umbral pero no el orden, así que suelen ser poco sensibles al escalado. Esto no significa “no necesitan preprocesamiento”: faltantes, categorías, alta cardinalidad, texto y disponibilidad siguen requiriendo decisiones.

Codificar una categoría nominal como 1, 2, 3 puede inventar un orden. Algunas implementaciones necesitan one-hot; otras tratan categorías de forma específica. La regla depende de la herramienta y debe quedar dentro del pipeline.

### 4.8 Error frecuente, checkpoint y SAIJ

> **Error frecuente:** confundir legibilidad de una rama con validez. Una regla como `organismo_id <= 18` puede ser fácil de leer y aun así representar una codificación arbitraria, una partición geográfica o fuga administrativa.

> **Checkpoint 4**
>
> ¿Por qué un árbol puede modelar una interacción sin crear manualmente (x_1x_2)? Porque una rama puede preguntar por (x_1) y luego, solo dentro de ese subconjunto, preguntar por (x_2). El efecto de la segunda depende del resultado de la primera.

**Transferencia a SAIJ.** Un árbol individual es útil como laboratorio conceptual y baseline tabular interpretable. Para TF-IDF enorme, su búsqueda de cortes puede ser costosa e inestable. Si se prueba, debe justificarse la representación y compararse no solo por métrica, sino por estabilidad de ramas y shortcuts.

> **Ejercicio conceptual 5**
>
> Un árbol alcanza hojas puras en train y cae mucho en validación. Mencioná cuatro controles coherentes.
>
> **Respuesta razonada:** limitar profundidad, aumentar el mínimo por hoja, exigir mayor ganancia y seleccionar poda mediante validación. También revisar fuga y partición: el sobreajuste no siempre se arregla solo con hiperparámetros.

> **Ejercicio conceptual 6**
>
> ¿Qué cambia y qué no cambia si medimos longitud en caracteres en vez de miles de caracteres?
>
> **Respuesta razonada:** cambian los valores numéricos de los umbrales, pero no el orden de documentos ni las particiones posibles por esa feature. Sin embargo, cualquier tratamiento de faltantes o transformación adicional sí puede cambiar.

---

## 5. Máquinas de vectores soporte

### 5.1 Intuición: separar dejando una avenida amplia

Muchas fronteras lineales podrían separar los mismos puntos de train. Una SVM no elige cualquiera: busca una frontera con margen amplio respecto de los ejemplos decisivos. Imaginá dos barrios separados por una avenida; el hiperplano es la línea central y el margen es el ancho libre a ambos lados.

Los puntos más cercanos a la frontera son los **vectores soporte**. Mueven la avenida. Puntos muy alejados, si permanecen del lado correcto, suelen influir menos en la solución final.

### 5.2 Vocabulario

- **Hiperplano:** frontera lineal en (d) dimensiones.
- **Margen:** distancia de seguridad entre frontera y casos cercanos.
- **Vector soporte:** observación que determina o viola el margen.
- **Margen duro:** separación sin errores ni invasiones, si existe.
- **Margen blando:** permite violaciones pagando una penalización.
- **(C):** equilibrio entre margen amplio y violaciones.
- **Kernel:** función que permite una frontera no lineal mediante similitudes implícitas.
- **(\gamma):** escala de influencia en kernels como RBF.

### 5.3 Hiperplano y predicción

La frontera lineal se escribe:

[
w^Tx+b=0
]

La decisión usa el signo:

[
f(x)=w^Tx+b
]

**Símbolo por símbolo:**

- (x) es el vector de features de una observación;
- (w) es el vector normal al hiperplano;
- (w^Tx) es el producto que suma contribuciones;
- (b) desplaza la frontera;
- (f(x)) es el score o margen firmado;
- signo positivo y negativo indican lados opuestos.

La distancia geométrica a la frontera es:

[
\operatorname{dist}(x)=\frac{|w^Tx+b|}{\|w\|_2}
]

donde el numerador es la magnitud del score, (\|w\|_2) es la norma euclídea de los pesos y el cociente corrige por la escala de (w). Un score bruto solo puede compararse con cautela entre modelos si sus escalas difieren.

### 5.4 Margen duro

Para etiquetas binarias (y_i\in\{-1,+1\}), el problema ideal busca:

[
\min_{w,b}\frac{1}{2}\|w\|_2^2
]

sujeto a:

[
y_i(w^Tx_i+b)\ge 1 \quad \text{para todo } i
]

**Símbolo por símbolo:**

- minimizar (\|w\|_2^2/2) equivale a maximizar el margen;
- (x_i) es la observación (i);
- (y_i) indica su clase con signo;
- si la clasificación es correcta y está fuera del margen, el producto es al menos 1;
- la restricción debe cumplirse para todos los casos.

En datos reales puede no existir separación perfecta o puede ser indeseable: forzarla vuelve la frontera extremadamente sensible a ruido.

### 5.5 Margen blando y parámetro C

Introducimos variables de holgura (\xi_i):

[
\min_{w,b,\xi}\frac{1}{2}\|w\|_2^2+C\sum_{i=1}^{n}\xi_i
]

sujeto a:

[
y_i(w^Tx_i+b)\ge 1-\xi_i,\qquad \xi_i\ge 0
]

**Símbolo por símbolo:**

- (\xi_i) mide cuánto invade o cruza el margen la observación (i);
- (C) asigna costo total a esas violaciones;
- el primer término favorece margen amplio;
- el segundo favorece ajustar los casos de train;
- (C) grande castiga fuerte las violaciones y puede estrechar el margen;
- (C) pequeño acepta más violaciones para una frontera más regularizada.

No hay un (C) universal. Su efecto depende de escalado, cantidad de datos, representación y convención de la implementación.

### 5.6 Hinge loss

La pérdida bisagra puede escribirse:

[
\ell_{hinge}(y,f(x))=\max(0,1-yf(x))
]

- si (yf(x)\ge1), el caso está correctamente clasificado fuera del margen y la pérdida es cero;
- si queda dentro del margen, paga una pérdida positiva;
- si cruza al lado incorrecto, paga más.

La SVM se concentra así en casos cercanos o problemáticos. Eso no significa que esos documentos sean intrínsecamente ambiguos en derecho; son difíciles bajo la representación y etiquetas disponibles.

### 5.7 Escalado

La distancia y el margen dependen de coordenadas. Si una feature numérica tiene rango enorme, puede dominar el producto. Por eso las SVM suelen requerir escalado aprendido en train. En TF-IDF se usan normalizaciones compatibles con dispersión; nunca se densifica sin estimar memoria.

### 5.8 Kernel lineal frente a kernel no lineal

Un kernel calcula similitud como si los datos se hubieran proyectado a otro espacio. El kernel RBF típico es:

[
K(x,x')=\exp\left(-\gamma\|x-x'\|_2^2\right)
]

**Símbolo por símbolo:**

- (x) y (x') son dos observaciones;
- (\|x-x'\|_2^2) es su distancia euclídea al cuadrado;
- (\gamma) controla cuán rápido cae la similitud con la distancia;
- (\exp) transforma el valor en una similitud entre 0 y 1;
- (\gamma) grande produce zonas de influencia muy locales y una frontera flexible;
- (\gamma) pequeño produce influencia amplia y una frontera más suave.

Un kernel puede modelar no linealidad, pero suele escalar peor con la cantidad de observaciones y requiere tuning conjunto de (C) y (\gamma). En texto disperso de alta dimensión, un kernel lineal suele ser un candidato temprano porque ya existe gran expresividad y el cómputo puede aprovechar ceros. “Suele” es una hipótesis de trabajo, no un veredicto SAIJ.

### 5.9 Multiclase

La SVM binaria debe extenderse para múltiples fueros, por ejemplo mediante one-vs-rest o one-vs-one. La primera entrena una frontera por clase contra el resto; la segunda, una por cada par. La estrategia afecta costo, cantidad de modelos y significado de scores.

Con muchas clases, one-vs-one crea (K(K-1)/2) clasificadores. Con (K=8), serían 28. One-vs-rest crea 8. Sin embargo, la comparación no se reduce al conteo: implementaciones y tamaños de subproblemas importan.

### 5.10 Score, no probabilidad

El margen de una SVM ordena confianza geométrica, pero no es una probabilidad. Puede calibrarse después usando datos separados del ajuste base, pero ese paso agrega estimación y riesgo de fuga. Si el uso necesita umbrales probabilísticos auditables, la calibración debe evaluarse explícitamente.

> **Error frecuente:** interpretar margen 2 como “probabilidad 200 %” o comparar directamente márgenes de modelos ajustados con escalas distintas.

> **Checkpoint 5**
>
> ¿Qué observaciones cambiarían la frontera si se eliminaran? Principalmente vectores soporte o casos que modifican qué puntos quedan cercanos al margen. Los muy alejados quizá no alteren la solución.

**Transferencia a SAIJ.** Una SVM lineal con TF-IDF pertenece temprano a la escalera porque combina margen con matrices dispersas. Debe compararse con logística y Naive Bayes bajo el mismo vocabulario y split, registrando macro métricas, confusiones, tiempos, memoria y necesidad de calibración.

> **Ejercicio conceptual 7**
>
> Aumentar (C) mejora train y empeora validación. ¿Qué interpretación proponés?
>
> **Respuesta razonada:** el costo alto de violaciones puede haber llevado a una frontera más ajustada a casos particulares, reduciendo regularización efectiva. Hay que confirmar estabilidad en validación y revisar escalado, ruido y rango de búsqueda.

> **Ejercicio conceptual 8**
>
> ¿Por qué un RBF con (\gamma) enorme puede sobreajustar?
>
> **Respuesta razonada:** cada observación influye en una región muy pequeña; la frontera puede rodear casos individuales. Esa flexibilidad reproduce detalles de train que quizá no se repitan.

## 6. Ensambles: combinar para reducir debilidades

### 6.1 Intuición general

Un ensamble combina varios modelos para producir una decisión. La esperanza no es que “muchos modelos siempre sepan más”, sino que sus errores sean lo bastante diferentes como para que la agregación reduzca alguna debilidad.

Si diez árboles memorizan exactamente los mismos casos y se equivocan en los mismos documentos, votar no ayuda. Si cada uno ve una muestra o conjunto de features distinto, sus variaciones pueden compensarse. La diversidad útil debe convivir con una competencia mínima: modelos aleatorios sin señal también son diversos, pero no valiosos.

### 6.2 Material complementario integrado 5/8 — diversidad del ensamble

Podemos pensar el error de un promedio mediante tres piezas: sesgo de los miembros, varianza individual y correlación entre errores. Bagging busca principalmente reducir varianza mediante miembros entrenados con perturbaciones. Boosting busca reducir sesgo corrigiendo lo que el conjunto todavía no explica. En ambos casos, la diversidad es un mecanismo, no una garantía.

Preguntas para auditar diversidad:

- ¿los miembros recibieron muestras distintas?
- ¿consideraron features distintas?
- ¿usan semillas distintas pero el mismo patrón dominante?
- ¿los errores se concentran en las mismas clases?
- ¿la diversidad mejora generalización o solo vuelve opaca la regla?

### 6.3 Bagging

**Bagging** abrevia *bootstrap aggregating*. Entrena (B) modelos sobre muestras bootstrap de train. Una muestra bootstrap toma (n) observaciones con reemplazo de un conjunto de tamaño (n): algunas aparecen varias veces y otras quedan fuera.

Para clasificación, la predicción puede ser votación:

[
\hat y(x)=\operatorname{modo}\{h_1(x),h_2(x),\ldots,h_B(x)\}
]

**Símbolo por símbolo:**

- (x) es la observación nueva;
- (h_b) es el modelo número (b);
- (B) es la cantidad total de miembros;
- cada (h_b(x)) emite una clase;
- (\operatorname{modo}) elige la más votada;
- (\hat y(x)) es la predicción agregada.

Si se promedian probabilidades estimadas:

[
\hat p_k(x)=\frac{1}{B}\sum_{b=1}^{B}\hat p_{bk}(x)
]

donde (\hat p_{bk}(x)) es la probabilidad que el miembro (b) asigna a la clase (k). El promedio puede ser más estable, pero no queda calibrado por definición.

### 6.4 Random forest

Un random forest agrega una segunda fuente de azar: en cada split, cada árbol considera solo un subconjunto de features. Esto evita que una feature muy dominante genere árboles casi idénticos.

El mecanismo combina:

1. muestras bootstrap diferentes;
2. árboles usualmente profundos o moderadamente controlados;
3. submuestreo aleatorio de features por corte;
4. votación o promedio final.

La cantidad de árboles suele reducir la variabilidad del promedio hasta estabilizarse; no reemplaza controles de profundidad, mínimo por hoja, features por split ni calidad de datos. Más árboles también consumen entrenamiento, memoria e inferencia.

### 6.5 Intuición out-of-bag

Una muestra bootstrap deja fuera aproximadamente una fracción de train para cada árbol. Esas observaciones **out-of-bag** (OOB) pueden evaluarse usando solo árboles que no las incluyeron.

Para una observación (i), definamos (B_i^{OOB}) como el conjunto de árboles cuyo bootstrap no contenía a (i). Su predicción OOB es:

[
\hat y_i^{OOB}=\operatorname{modo}\{h_b(x_i):b\in B_i^{OOB}\}
]

**Símbolo por símbolo:**

- (x_i) es la observación de train evaluada;
- (b\in B_i^{OOB}) restringe la votación a árboles que no la vieron;
- el modo agrega sus clases;
- (\hat y_i^{OOB}) permite una estimación interna.

OOB es útil como diagnóstico y a veces como alternativa eficiente a una validación adicional, pero no reemplaza automáticamente un split temporal o grupal. El bootstrap aleatorio puede mezclar documentos relacionados o futuros respecto del caso evaluado. La estructura operacional manda.

### 6.6 Boosting

Boosting construye aprendices secuencialmente. Cada nuevo miembro intenta corregir errores o residuos del conjunto anterior. En clasificación con gradiente boosting, la idea general es sumar funciones pequeñas:

[
F_M(x)=F_0(x)+\sum_{m=1}^{M}\eta\,h_m(x)
]

**Símbolo por símbolo:**

- (F_0(x)) es la predicción inicial, por ejemplo basada en prevalencias;
- (M) es el número de etapas;
- (m) identifica una etapa;
- (h_m(x)) es el aprendiz débil agregado en esa etapa;
- (\eta) es la tasa de aprendizaje;
- (F_M(x)) es el score final acumulado.

Un **aprendiz débil** no significa inútil: es un modelo deliberadamente simple, como un árbol poco profundo, que mejora un aspecto. La secuencia convierte muchas correcciones pequeñas en una regla potente.

### 6.7 Tasa de aprendizaje y número de etapas

Una (\eta) pequeña hace que cada árbol aporte poco. Suele requerir más etapas, aumenta tiempo, pero puede producir aprendizaje gradual. Una (\eta) grande corrige rápido y puede sobreajustar o volverse inestable. Número de etapas y tasa se seleccionan juntos.

Otros controles:

- profundidad o número de hojas de cada aprendiz;
- submuestreo de filas y columnas;
- mínimo por hoja;
- regularización de pesos;
- parada temprana basada en validación;
- tratamiento explícito de faltantes y categorías según implementación.

### 6.8 Bagging versus boosting

| Pregunta | Bagging / bosque | Boosting |
|---|---|---|
| Relación entre miembros | Paralelos e independientes dadas las muestras | Secuenciales; cada etapa depende del conjunto previo |
| Meta dominante | Reducir varianza | Corregir sesgo y errores residuales |
| Diversidad | Bootstrap y features | Foco progresivo en errores/residuos |
| Sensibilidad al ruido | El promedio puede amortiguar | Puede perseguir casos ruidosos si no se controla |
| Paralelización | Más natural | Limitada por dependencia entre etapas |
| Tuning | Árboles, features, muestras | Tasa, etapas, complejidad y regularización interactúan |

### 6.9 Representación y texto

Los ensambles de árboles suelen brillar en datos tabulares con relaciones no lineales y features curadas. Aplicarlos directamente a TF-IDF enorme puede ser costoso y no aprovechar la dispersión tan eficientemente como un lineal. Reducir dimensiones o usar embeddings densos cambiaría el experimento y requeriría validar qué información se pierde, cómo se aprendió la transformación y si aparece fuga.

No hay prohibición. Hay una carga de justificación: si un bosque o boosting entra en la escalera SAIJ, debe hacerlo porque la representación y la evidencia lo justifican, no porque sea más complejo.

### 6.10 Error frecuente, checkpoint y transferencia

> **Error frecuente:** afirmar que un bosque “no sobreajusta porque promedia”. El promedio suele reducir varianza respecto de un árbol, pero features con fuga, árboles correlacionados, clases raras o tuning sobre test pueden producir resultados engañosos.

> **Checkpoint 6**
>
> ¿Por qué submuestrear features puede mejorar un bosque? Porque impide que todos los árboles elijan siempre la señal dominante, reduce correlación entre miembros y permite que señales alternativas participen.

**Transferencia a SAIJ.** Random forest y boosting deben aparecer después de controles lineales. Son candidatos si existe metadata legítima, suficiente soporte y evidencia de interacciones que los modelos simples no capturan. Su entrada exige medir memoria, inferencia, estabilidad temporal e importancia sesgada.

> **Ejercicio conceptual 9**
>
> Un bosque de 500 árboles y uno de 1 000 tienen desempeño casi idéntico, pero el segundo duplica memoria e inferencia. ¿Qué elegirías?
>
> **Respuesta razonada:** salvo evidencia de mayor estabilidad relevante, el de 500 ofrece mejor compromiso. La cantidad de árboles no es una medalla; debe justificarse por beneficio marginal.

> **Ejercicio conceptual 10**
>
> El error OOB es excelente, pero el test temporal es malo. ¿Cuál informa el uso futuro?
>
> **Respuesta razonada:** el test temporal, si representa el escenario operativo. OOB mezcla períodos y estima otra pregunta. La discrepancia es evidencia de drift, dependencia o un split OOB demasiado optimista para el caso.

> **Ejercicio conceptual 11**
>
> En boosting, train mejora en cada etapa y validación empeora después de la 80. ¿Qué control sugiere esa curva?
>
> **Respuesta razonada:** parada temprana cerca del mejor punto de validación, seleccionada sin mirar test. También puede reducirse profundidad, tasa o aumentar regularización.

---

## 7. Desbalance: aprender, evaluar y decidir no son lo mismo

### 7.1 Tres lugares de intervención

El desbalance puede abordarse en tres niveles diferentes:

1. **Aprendizaje:** modificar la importancia de clases o la muestra de train.
2. **Evaluación:** usar métricas por clase, macro y matrices de confusión.
3. **Decisión:** ajustar umbrales o políticas de abstención según costos.

Mezclar niveles causa confusión. Un peso de clase cambia el objetivo de entrenamiento. Un umbral cambia decisiones después del score. Macro F1 cambia cómo resumimos, no cómo aprendió el modelo.

### 7.2 Pesos de clase

Una pérdida ponderada puede escribirse:

[
J=\frac{1}{n}\sum_{i=1}^{n}\alpha_{y_i}\,\ell(y_i,\hat y_i)
]

**Símbolo por símbolo:**

- (n) es el tamaño de train;
- (i) recorre observaciones;
- (y_i) es la clase real;
- (\alpha_{y_i}) es el peso asignado a esa clase;
- (\ell) es la pérdida base;
- un peso mayor hace que equivocarse en esa clase cueste más durante el ajuste.

En regresión logística y SVM, los pesos modifican la contribución a la pérdida. En árboles, alteran el cálculo ponderado de impureza o el costo de errores. En boosting, pueden combinarse con la pérdida o pesos de muestra, pero interactúan con la corrección secuencial.

Una heurística “balanceada” inversa a la frecuencia es punto de partida, no verdad. Si una clase rara tiene etiquetas ruidosas, amplificarla puede amplificar ruido.

### 7.3 Muestreo

- **Submuestreo:** reduce ejemplos de clases grandes.
- **Sobremuestreo:** repite o genera ejemplos de clases pequeñas.
- **Muestreo estratificado por lote:** conserva presencia de clases durante ajuste.

Todo muestreo se aplica **solo en train y dentro de cada fold**. Sobremuestrear antes de separar puede colocar duplicados o derivados de una observación en train y validación. Test conserva la prevalencia del escenario que pretende medir.

En texto, crear ejemplos sintéticos en el espacio vectorial exige cautela: una interpolación numérica puede no corresponder a un documento jurídicamente plausible. Repetir casos también puede sobreajustar. Pesos suelen ser un primer control más simple, pero se comparan empíricamente.

### 7.4 Thresholding por familia

- **Logística:** se ajusta el umbral sobre probabilidad candidata, después de revisar calibración.
- **SVM:** se ajusta sobre margen o score; la escala no es probabilidad.
- **Árbol/bosque:** se ajusta sobre proporciones o promedios estimados, que pueden requerir calibración.
- **Boosting:** se ajusta sobre probabilidad o score según la pérdida e implementación.

En multiclase, un umbral único puede no alcanzar. Pueden usarse umbral de probabilidad máxima, diferencia entre primera y segunda clase, reglas específicas por clase o una política de rechazo. Todo debe seleccionarse en validación y evaluarse en test una sola vez.

### 7.5 Costos asimétricos

Si el costo de enviar un caso penal a un fuero equivocado fuera mayor que el de derivarlo a revisión, las decisiones deberían reflejarlo. Una matriz de costos conceptual es:

[
R(a\mid x)=\sum_{k=1}^{K}C(a,k)\,p(y=k\mid x)
]

**Símbolo por símbolo:**

- (a) es una acción posible: asignar una clase o abstenerse;
- (k) recorre clases reales;
- (C(a,k)) es el costo de tomar acción (a) cuando la verdad es (k);
- (p(y=k\mid x)) es la probabilidad estimada;
- (R(a\mid x)) es el riesgo esperado;
- se elige la acción con menor riesgo si probabilidades y costos son confiables.

En SAIJ, los costos no deben inventarse. Son una **decisión pendiente de Javier y del contexto de uso**. El ejercicio enseña la estructura, no fija valores.

> **Error frecuente:** “arreglar” desbalance hasta que train quede 50/50 y luego reportar accuracy sobre esa distribución artificial como si fuera producción.

> **Checkpoint 7**
>
> ¿Pesos de clase y umbral son equivalentes? No. Los pesos cambian el modelo aprendido; el umbral cambia la decisión sobre scores ya producidos. Pueden generar efectos parecidos en alguna métrica, pero no son intercambiables.

> **Ejercicio conceptual 12**
>
> Una clase rara tiene recall alto tras ponderar, pero su precision cae mucho. ¿Es un fracaso?
>
> **Respuesta razonada:** depende del costo. El modelo detecta más casos reales pero emite más falsas alarmas. Hay que analizar confusiones, carga de revisión y umbrales, no mirar una métrica aislada.

---

## 8. Selección de modelos e hiperparámetros sin fuga

### 8.1 Parámetro versus hiperparámetro

Los **parámetros** se aprenden dentro del ajuste: coeficientes, cortes o pesos de árboles. Los **hiperparámetros** configuran ese aprendizaje: regularización, profundidad, (C), (\gamma), cantidad de árboles o tasa.

Elegir hiperparámetros también aprende de datos. Si probamos cien configuraciones y elegimos la mejor sobre test, test deja de ser una estimación final y se convierte en validación encubierta.

### 8.2 Grilla y búsqueda aleatoria

Una grilla enumera combinaciones. Por ejemplo:

```text
C: bajo, medio, alto
regularización: L1, L2
ngramas: unigramas, uni+bigramas
```

Eso produce (3\times2\times2=12) configuraciones. La búsqueda aleatoria toma combinaciones desde rangos o distribuciones. Puede explorar mejor cuando pocos hiperparámetros dominan y evita gastar la misma resolución en dimensiones poco sensibles.

Ninguna búsqueda compensa un rango absurdo o una validación inválida. El presupuesto y los valores deben registrarse antes de mirar resultados finales.

### 8.3 Validación cruzada

Para (K) folds, una métrica promedio es:

[
\bar m=\frac{1}{K}\sum_{k=1}^{K}m_k
]

y su dispersión muestral puede resumirse:

[
s_m=\sqrt{\frac{1}{K-1}\sum_{k=1}^{K}(m_k-\bar m)^2}
]

**Símbolo por símbolo:**

- (K) es la cantidad de folds;
- (m_k) es la métrica en el fold (k);
- (\bar m) es el promedio;
- (s_m) resume cuánto varía entre folds;
- una media sin dispersión oculta inestabilidad.

Los folds no son réplicas independientes perfectas porque comparten datos de entrenamiento. La dispersión es diagnóstico, no intervalo causal automático.

### 8.4 Restricciones de grupos y tiempo

Si varios documentos pertenecen al mismo expediente, organismo o serie, deben permanecer juntos cuando compartir entidad generaría dependencia. Si el uso será futuro, los folds deben respetar orden temporal. Estratificar clases no resuelve esas restricciones.

Una validación temporal expansiva podría entrenar con períodos iniciales y validar sobre el período siguiente, ampliando train en cada ronda. Estima adaptación a futuros sucesivos. Una validación aleatoria estima intercambiabilidad. Son preguntas distintas.

### 8.5 Prevención de fuga dentro de la búsqueda

Cada candidato debe aprender dentro de cada train-fold:

- vocabulario y pesos IDF;
- escaladores e imputadores;
- selección de features;
- reducción dimensional;
- muestreo por desbalance;
- calibración cuando corresponde.

Si una transformación mira todo el dataset antes de los folds, la validación recibe información indirecta de sus propios casos.

### 8.6 Material complementario integrado 6/8 — intuición de validación anidada

**Contexto opcional.** Cuando queremos estimar el rendimiento de todo el proceso de selección, podemos usar una validación externa para evaluar y una interna para elegir hiperparámetros. En cada fold externo, la búsqueda ocurre solo dentro de su train externo. Luego el mejor candidato se evalúa en la validación externa que no participó en la elección.

La intuición es separar dos preguntas:

1. ¿qué configuración elegimos? — bucle interno;
2. ¿qué tan bien generaliza el procedimiento de elegir? — bucle externo.

Es costosa y no siempre necesaria para un primer TP. Se incluye como contexto opcional, no como requisito automático. Un train/valid/test bien diseñado puede ser suficiente si el presupuesto y las decisiones son modestos.

> **Error frecuente:** reportar el mejor fold o la mejor configuración sin aclarar cuántas alternativas se probaron. Cuanto más buscamos, mayor es el riesgo de seleccionar ruido de validación.

> **Checkpoint 8**
>
> ¿Por qué test debe usarse una vez al final? Porque su independencia ofrece una estimación no optimizada. Cada consulta influye en decisiones y reduce esa independencia.

> **Ejercicio conceptual 13**
>
> Una grilla selecciona profundidad 20 por 0.002 puntos sobre profundidad 8, pero con mucha mayor variación entre folds. ¿Qué mirarías?
>
> **Respuesta razonada:** estabilidad, costo y complejidad. La diferencia puede ser ruido. Una regla de parsimonia podría preferir profundidad 8 si cae dentro de incertidumbre práctica, siempre definida antes de test.

> **Ejercicio conceptual 14**
>
> El vocabulario TF-IDF se ajustó antes de CV. ¿Por qué hay fuga aunque no use el target?
>
> **Respuesta razonada:** IDF y vocabulario incorporan distribución de documentos de validación. El modelo conoce qué términos existen y cuán globalmente frecuentes son en casos que debía tratar como nuevos.

---

## 9. Pipelines y preprocesamiento por familia

### 9.1 Un pipeline es una frontera de aprendizaje

Un pipeline no es solo comodidad de software. Define qué pasos aprenden parámetros y garantiza que se ajusten únicamente con train. Conceptualmente:

```text
entrada cruda
  → validación de esquema
  → transformaciones por tipo
  → representación
  → muestreo permitido en train
  → modelo
  → calibración o umbral aprendido en validación
  → decisión y registro
```

Separar un paso “porque ya estaba precomputado” no lo vuelve inocente. Si fue aprendido con todo el corpus, puede filtrar información.

### 9.2 Requisitos por familia

| Familia | Escalado | Categorías | Faltantes | Texto disperso | Riesgo típico |
|---|---|---|---|---|---|
| Logística | Sí para numéricas; cuidado con dispersión | One-hot u otra codificación legítima | Imputación/indicadores | Excelente compatibilidad | Regularización afectada por escala |
| SVM lineal | Importante | Codificación numérica válida | Tratamiento explícito | Excelente compatibilidad | Margen dominado por escalas |
| SVM RBF | Esencial | Codificación y densidad cuidadas | Tratamiento explícito | Puede ser costoso | Costo cuadrático/sensibilidad a (\gamma) |
| Árbol | Poco sensible a escala | Depende de implementación | Depende de implementación | Posible pero no siempre adecuado | Orden artificial y alta cardinalidad |
| Bosque | Poco sensible | Igual que árbol | Igual que implementación | Costo potencial alto | Memoria e importancias sesgadas |
| Boosting | Poco sensible si usa árboles | Implementación específica | Algunas manejan faltantes | Debe justificarse | Tuning y leakage en encoding |

### 9.3 Texto y metadata en ramas separadas

Si se combinan texto y columnas tabulares, cada tipo requiere su propia rama:

```text
texto → normalización justificada → TF-IDF ┐
                                           ├→ unión dispersa compatible → clasificador
numéricas → imputación → escalado          │
categorías → imputación → codificación     ┘
```

La unión debe preservar compatibilidad de memoria. Una codificación densa de alta cardinalidad puede desbordar recursos. Además, metadata con nombres de organismos o códigos administrativos puede funcionar como proxy del target; necesita auditoría semántica.

### 9.4 Preprocesar de más también daña

Eliminar palabras jurídicas frecuentes puede borrar señal. Stemming agresivo puede confundir términos. Imputar un faltante con una categoría dominante puede ocultar que la ausencia era informativa. Escalar una matriz dispersa con centrado puede densificarla.

Cada transformación debe responder:

1. ¿qué problema resuelve?;
2. ¿qué información aprende?;
3. ¿dónde se ajusta?;
4. ¿qué estructura puede destruir?;
5. ¿cómo se reproduce en inferencia?

> **Error frecuente:** aplicar el mismo preprocesamiento a todas las familias para “ser justos”. La justicia experimental exige información y splits comparables, no operaciones inadecuadas idénticas.

> **Checkpoint 9**
>
> ¿Qué pasos deben viajar con el modelo? Todos los necesarios para transformar una entrada futura exactamente como train: esquema, imputación, vocabulario, IDF, escalado, codificación, orden de columnas y política de decisión.

> **Ejercicio conceptual 15**
>
> Un bosque se entrena sobre categorías convertidas a enteros por orden alfabético. ¿Qué problema aparece?
>
> **Respuesta razonada:** los cortes interpretan una proximidad y orden inexistentes. Las categorías entre ciertos números quedan agrupadas por accidente alfabético. Se necesita codificación compatible o soporte categórico explícito.

---

## 10. Score, probabilidad, calibración y umbrales

### 10.1 Cuatro objetos distintos

- **Score:** número continuo que ordena o separa casos.
- **Margen:** score geométrico respecto de una frontera, típico de SVM.
- **Probabilidad:** estimación entre 0 y 1 que pretende corresponder a frecuencia condicional.
- **Decisión:** acción discreta obtenida mediante umbral, argmax, abstención o costos.

Un modelo puede discriminar bien y calibrar mal. También puede calibrar razonablemente pero separar poco. Son propiedades distintas.

### 10.2 Material complementario integrado 2/8 — discriminación versus calibración

**Discriminación** pregunta si casos de una clase reciben scores mayores que los de otra o si se ordenan correctamente. **Calibración** pregunta si, entre casos anunciados con probabilidad 0.7, aproximadamente 70 % pertenece a la clase en condiciones comparables.

Ejemplo inventado:

- modelo A ordena casi todos los positivos por encima de negativos, pero emite 0.99 para demasiados casos;
- modelo B ordena algo peor, pero sus grupos de 0.7 contienen cerca de 70 % positivos.

A discrimina mejor; B puede calibrar mejor. Para ranking podría preferirse A; para gestionar riesgo con umbrales probabilísticos, la calibración importa mucho.

### 10.3 Brier score

Para clasificación binaria:

[
BS=\frac{1}{n}\sum_{i=1}^{n}(p_i-y_i)^2
]

**Símbolo por símbolo:**

- (n) es la cantidad de casos;
- (p_i) es la probabilidad estimada del caso (i);
- (y_i) vale 0 o 1;
- la diferencia al cuadrado penaliza distancia probabilística;
- menor Brier es mejor, pero mezcla calibración y discriminación.

Un gráfico de confiabilidad agrupa predicciones por rango y compara probabilidad media con frecuencia observada. Debe incluir tamaño de grupos: una curva vistosa basada en pocos casos puede ser inestable.

### 10.4 Calibración posterior

Métodos como una transformación sigmoide o isotónica aprenden a mapear scores a probabilidades. Deben ajustarse con datos no usados para entrenar el modelo base, mediante folds o conjunto de calibración. La isotónica es flexible pero necesita soporte; una sigmoide impone forma más rígida.

Calibrar no mejora necesariamente accuracy ni ranking. Cambia el significado de la escala. Y una calibración global puede ocultar descalibración por clase, período o grupo.

### 10.5 Material complementario integrado 3/8 — umbrales y costos asimétricos

Con probabilidad binaria y costos simples, un umbral no tiene por qué ser 0.5. Si un falso negativo cuesta más, podría bajarse para detectar más positivos; si un falso positivo es costoso, podría subirse. El valor se selecciona en validación según una función de utilidad y se confirma en test.

En multiclase SAIJ podrían usarse dos criterios:

1. probabilidad máxima superior a (\tau);
2. diferencia entre primera y segunda clase superior a (\delta).

Si alguno falla, se abstiene. (\tau) controla confianza absoluta estimada; (\delta), ambigüedad relativa. Ambos son hiperparámetros operacionales y no se inventan sin costos y capacidad humana.

### 10.6 Error frecuente, checkpoint y SAIJ

> **Error frecuente:** afirmar “90 % de confianza” porque softmax devuelve 0.9. Es una probabilidad del modelo; sin validación de calibración, puede ser sistemáticamente excesiva.

> **Checkpoint 10**
>
> ¿Puede un umbral mejorar recall sin reentrenar? Sí. Al bajar el umbral positivo se aceptan más casos, sube recall y normalmente baja precision. La frontera operacional cambia, no los scores.

**Transferencia a SAIJ.** Si el sistema solo prioriza revisión, un score ordenado puede bastar. Si decide autoasignar o abstenerse según riesgo, calibración y estabilidad por clase se vuelven centrales. El uso define la exigencia.

> **Ejercicio conceptual 16**
>
> Una logística tiene macro F1 estable, pero para predicciones cercanas a 0.8 la frecuencia real es 0.6. ¿Qué sabés?
>
> **Respuesta razonada:** discrimina lo suficiente para esa F1, pero sobrestima probabilidades en ese rango. No conviene aplicar costos como si 0.8 fuera frecuencia real sin calibrar o revisar drift.

---

## 11. Interpretabilidad sin promesas excesivas

### 11.1 Global y local

- **Explicación global:** resume cómo se comporta el modelo en general.
- **Explicación local:** intenta explicar una predicción concreta.

Coeficientes son globales; contribuciones (w_jx_j) son locales para un lineal. Un árbol pequeño admite reglas globales; una ruta explica un caso. Un bosque requiere agregación; una importancia global no explica por sí sola un documento.

### 11.2 Coeficientes y contribuciones

Para un lineal:

[
z=b+\sum_j w_jx_j
]

El coeficiente (w_j) describe sensibilidad por unidad, mientras (w_jx_j) describe contribución de esa feature en el caso. Un peso alto no importa localmente si (x_j=0). En multiclase, cada clase tiene su vector y la interpretación es relativa a las demás o a la estrategia OvR.

Correlación entre términos distribuye señal. Cambiar regularización o vocabulario puede alterar pesos sin cambiar mucho predicciones. La estabilidad de explicación debe comprobarse.

### 11.3 Árboles y bosques

En un árbol, una ruta puede escribirse como secuencia de condiciones. En un bosque, no existe una ruta única: cientos de árboles votan. Las importancias por reducción de impureza suman cuánto contribuyó cada feature a reducir criterio durante splits.

Esa medida favorece features con muchos valores o muchas oportunidades de corte. Además, una feature correlacionada puede “robar” splits a otra. Que una columna se use mucho no implica que sea causal ni segura.

### 11.4 Permutation importance

La importancia por permutación mide cuánto cae una métrica al romper una feature en datos de evaluación:

[
I_j=m(X,y)-m(X^{\pi(j)},y)
]

**Símbolo por símbolo:**

- (m) es la métrica elegida;
- (X) es la matriz original;
- (y) son targets;
- (X^{\pi(j)}) es la misma matriz con la columna (j) permutada;
- (I_j) es la caída atribuida a destruir su asociación.

Si dos features son redundantes, permutar una puede causar poca caída porque la otra conserva señal. Si permutar genera combinaciones imposibles, la estimación sale fuera de distribución. La importancia depende de métrica y muestra.

### 11.5 Material complementario integrado 4/8 — trampas de importancia

Checklist obligatorio:

- **correlación:** reparte u oculta importancia;
- **alta cardinalidad:** ofrece muchas oportunidades de partición;
- **fuga:** una feature “muy importante” puede ser precisamente peligrosa;
- **proxy:** ubicación u organismo pueden representar desigualdades o procesos administrativos;
- **inestabilidad:** rankings cambian con seed o fold;
- **métrica:** una feature puede importar para accuracy y no para recall de una clase;
- **causalidad:** predecir no demuestra producir el resultado;
- **granularidad:** términos individuales ignoran frases y grupos semánticos.

La explicación es otra medición con supuestos, no una ventana infalible al razonamiento.

### 11.6 Error frecuente, checkpoint y SAIJ

> **Error frecuente:** eliminar automáticamente toda feature con importancia baja. Puede ser redundante, útil en subgrupos o relevante para estabilidad. La eliminación es un experimento, no una deducción.

> **Checkpoint 11**
>
> Si `provincia` tiene alta importancia, ¿qué sigue? Auditar disponibilidad, cardinalidad, correlaciones, estabilidad temporal, errores por provincia, posible proxy y comparación sin esa feature. No celebrar ni eliminar por reflejo.

**Transferencia a SAIJ.** Para revisión humana, conviene mostrar evidencia acotada: términos o features que contribuyeron, clases alternativas, score y límites. Nunca presentar una explicación local como fundamento jurídico del documento. Explica al modelo, no resuelve el caso.

> **Ejercicio conceptual 17**
>
> Dos palabras correlacionadas tienen permutation importance casi cero por separado y alta cuando se permutan juntas. ¿Qué indica?
>
> **Respuesta razonada:** contienen señal redundante. Cada una sustituye a la otra; romper el grupo revela su aporte conjunto. La unidad de interpretación apropiada puede ser un grupo de features.

---

## 12. Costos computacionales y representaciones

### 12.1 Entrenamiento, inferencia y memoria son costos distintos

- **Entrenamiento:** ajustar parámetros e hiperparámetros.
- **Inferencia:** producir predicciones nuevas.
- **Memoria del dato:** almacenar matrices y transformaciones.
- **Memoria del modelo:** almacenar pesos, nodos, vectores soporte o árboles.
- **Costo de selección:** multiplicar entrenamiento por folds y candidatos.

Una configuración que entrena una vez por hora puede ser aceptable; una que tarda segundos por documento quizá no, según el flujo. O al revés: entrenamiento diario debe ser rápido, mientras inferencia por lotes tolera más.

### 12.2 Lineales

Un modelo lineal guarda aproximadamente un peso por feature y clase. Con matrices dispersas, entrenamiento e inferencia aprovechan valores no cero. La inferencia es un producto vectorial, por lo que suele ser rápida.

La selección puede ser costosa si se prueban muchos vocabularios, regularizaciones y folds. El vocabulario mismo ocupa memoria. Reducirlo por frecuencia debe ocurrir dentro del pipeline.

### 12.3 SVM

Una SVM lineal comparte ventajas de dispersión. Una SVM con kernel puede necesitar comparar con muchos vectores soporte durante inferencia y construir relaciones costosas durante entrenamiento. A gran escala, memoria y tiempo pueden crecer fuertemente con observaciones.

El número de vectores soporte es un dato operativo: cuantos más, mayor puede ser el costo de inferencia kernelizada.

### 12.4 Árboles y ensambles

Un árbol infiere recorriendo una ruta cuya longitud se relaciona con profundidad. Un bosque recorre una ruta por árbol; boosting ejecuta etapas secuenciales. Más árboles, profundidad y clases incrementan memoria y latencia.

Los árboles sobre datos dispersos de enorme dimensión evalúan muchas oportunidades de corte. Una matriz densa de embeddings usa memoria proporcional a filas por dimensiones, aunque tenga menos columnas. No hay formato barato universal.

### 12.5 Disperso versus denso

Si (N) documentos, (D) features y solo una fracción (\rho) es no cero:

- almacenamiento denso crece aproximadamente con (N\times D);
- almacenamiento disperso crece con (\rho ND) más índices.

Con (\rho) muy pequeña, la diferencia es enorme. Pero algunos algoritmos convierten internamente a denso; comprobar compatibilidad es parte de la selección.

### 12.6 Presupuesto experimental

El costo total aproximado de una búsqueda es:

[
T_{total}\approx H\times K\times T_{fit}
]

**Símbolo por símbolo:**

- (H) es la cantidad de configuraciones;
- (K) es la cantidad de folds;
- (T_{fit}) es el tiempo medio de un ajuste;
- el producto omite paralelismo y overhead, pero muestra la escala.

Si probamos 60 configuraciones en 5 folds, son 300 ajustes por familia. Agregar calibración o nested CV multiplica más. Diseñar búsquedas informadas también es rigor.

> **Checkpoint 12**
>
> ¿Por qué reportar solo tiempo de fit es insuficiente? Porque producción puede estar dominada por inferencia, memoria, vectorización o calibración; y desarrollo, por cantidad de ajustes de CV.

> **Ejercicio conceptual 18**
>
> Un kernel RBF mejora levemente una métrica frente a SVM lineal, pero usa casi todos los casos como vectores soporte. ¿Qué implica?
>
> **Respuesta razonada:** inferencia y memoria pueden crecer con train. Hay que evaluar si la mejora es estable y valiosa frente al costo, además de revisar sobreajuste y escalabilidad.

---

## 13. Comparación reproducible y ledger experimental

### 13.1 Una corrida no es evidencia suficiente

Para atribuir diferencias, un experimento registra al menos:

- objetivo y fecha;
- versión o huella del dataset;
- población, unidad y target;
- train/valid/test o folds exactos;
- columnas permitidas y excluidas;
- pipeline y representación;
- familia e hiperparámetros;
- seed y entorno;
- métricas globales y por clase;
- calibración y umbrales;
- tiempos y memoria;
- artefactos guardados;
- errores destacados;
- decisión y preguntas abiertas.

El **ledger** evita que “modelo 7” quede desconectado de cómo se obtuvo. Su unidad no es el archivo del modelo, sino la afirmación reproducible.

### 13.2 Comparación de una variable por vez

Una secuencia clara podría ser:

1. fijar split y mayoría;
2. fijar representación y comparar Naive Bayes, logística y SVM lineal;
3. mantener familia y variar regularización;
4. mantener configuración y comparar texto solo contra texto+metadata legítima;
5. recién entonces explorar árbol o ensamble con representación apropiada.

En la práctica hay interacciones. Aun así, este orden ayuda a no atribuir a “SVM” una mejora causada por bigramas o a “boosting” una mejora causada por fuga.

### 13.3 Semillas y determinismo

Registrar seed no vuelve determinista todo el sistema. Paralelismo, versiones y operaciones numéricas pueden variar. Además, una sola seed no mide sensibilidad. Para modelos estocásticos se pueden repetir unas pocas semillas predefinidas y reportar distribución, sin elegir retrospectivamente la más favorable.

### 13.4 Material complementario integrado 8/8 — ficha liviana de modelo

Una **model card** acotada documenta uso y límites:

| Campo | Pregunta |
|---|---|
| Nombre y versión | ¿Qué artefacto es? |
| Propósito | ¿Qué decisión asiste y cuál no? |
| Población | ¿Sobre qué documentos se evaluó? |
| Target | ¿Cómo se construyó y qué ambigüedad conserva? |
| Features | ¿Qué usa y qué se excluyó por fuga o política? |
| Evaluación | ¿Qué split, métricas y subgrupos se midieron? |
| Umbral | ¿Cómo se eligió y qué costo representa? |
| Limitaciones | ¿Dónde no debe usarse? |
| Revisión humana | ¿Cuándo se abstiene o deriva? |
| Monitoreo | ¿Qué drift y errores se revisan? |

No reemplaza el ledger: el ledger cuenta experimentos; la ficha resume el modelo candidato para personas que deben usarlo, revisarlo o limitarlo.

### 13.5 Separación de hechos

En el futuro documento SAIJ deben convivir frases de distinto grado:

- **Teoría:** “SVM lineal produce un margen, no una probabilidad calibrada”.
- **Resultado reproducido:** “en el experimento E-014, bajo split temporal X, ocurrió…”.
- **Hallazgo del equipo pendiente:** “el notebook grupal informa…, aún no reproducido por Javier”.
- **Decisión:** “se adopta abstención porque el flujo tolera revisión y el costo de confusión es alto”.

No mezclar esas frases protege autoría y evidencia.

> **Error frecuente:** guardar solo el mejor modelo y borrar corridas fallidas. Las fallas explican decisiones, evitan repetir caminos y muestran cuánto se buscó.

> **Checkpoint 13**
>
> ¿Qué debe compartir toda comparación? La misma pregunta de generalización, splits inalterados, métricas predefinidas y datos legítimos. El preprocesamiento puede variar si es parte explícita del candidato.

> **Ejercicio conceptual 19**
>
> Dos personas ejecutan “la misma” logística y obtienen resultados distintos. Enumerá cinco causas registrables.
>
> **Respuesta razonada:** versión de datos, split, vocabulario/IDF, regularización, seed, solver, tolerancia, pesos, librería o umbral. El ledger debe volver visibles esas diferencias.

---

## 14. Análisis de errores multidimensional

### 14.1 La métrica abre la investigación

Una matriz de confusión indica qué clases se mezclan, pero no explica por qué. El análisis de errores toma falsos positivos, falsos negativos y aciertos frágiles, y los corta por dimensiones con significado operacional.

Para SAIJ, el mínimo solicitado es:

1. clase real y predicha;
2. par de confusión;
3. tiempo;
4. geografía;
5. tipo documental;
6. longitud del texto.

También pueden analizarse faltantes, fuente, organismo y cobertura del vocabulario, siempre que no se expongan datos sensibles ni se interpreten proxies sin cautela.

### 14.2 Error por clase

Precision, recall y F1 por fuero revelan asimetrías ocultas por promedios. Una clase puede tener recall bajo por poco soporte, etiqueta ambigua, lenguaje compartido o drift. El primer paso es cuantificar soporte y revisar ejemplos, no ajustar pesos automáticamente.

### 14.3 Pares de confusión

Para clases (a) y (b), una tasa dirigida puede ser:

[
q_{a\to b}=\frac{C_{ab}}{\sum_{r=1}^{K}C_{ar}}
]

**Símbolo por símbolo:**

- (C_{ab}) es la cantidad real (a) predicha como (b);
- el denominador suma toda la fila real (a);
- (q_{a\to b}) es la fracción de la clase (a) desviada hacia (b);
- no tiene por qué igualar (q_{b\to a}).

La asimetría orienta hipótesis: una clase amplia puede absorber a una específica, o la etiqueta puede ser jerárquica.

### 14.4 Error por tiempo

Graficar métricas por año o ventana detecta drift. Debe acompañarse con soporte y cambios de prevalencia. Una caída puede deberse a vocabulario nuevo, nueva fuente, cambio normativo, etiqueta, OCR o composición.

No se reentrena automáticamente ante cualquier caída. Primero se verifica si el reloj representa publicación, decisión, carga u otra fecha.

### 14.5 Error por geografía

Comparar provincias o jurisdicciones puede revelar heterogeneidad, pero grupos pequeños producen estimaciones ruidosas. Deben reportarse intervalos o al menos soporte, revisar cobertura y evitar convertir desigualdad descriptiva en atributo esencial.

Geografía puede ser feature y eje de auditoría. Aunque se excluya del modelo, analizar desempeño por geografía sigue siendo posible si el dato es legítimo para evaluación.

### 14.6 Error por tipo documental

Sentencias, sumarios, resoluciones o documentos con OCR diferente pueden tener vocabulario y longitud distintos. Si el target se deduce mejor en un tipo, el modelo puede parecer fuerte por composición. Comparar por tipo separa capacidad lingüística de artefactos documentales.

### 14.7 Error por longitud

Dividir por rangos definidos en validación ayuda a ver si textos cortos carecen de contexto o textos largos diluyen señales. Los rangos se fijan sin perseguir un patrón de test. Longitud también puede ser proxy de tipo o fuente; conviene cruzar dimensiones.

### 14.8 Del patrón a una acción

Cada hallazgo debe completar:

```text
patrón observado
  → hipótesis
  → evidencia adicional
  → intervención posible
  → riesgo de la intervención
  → experimento de confirmación
```

Ejemplo inventado: baja de recall en textos cortos → hipótesis de escasa señal → revisar cobertura y tipos → posible abstención por longitud → riesgo de excluir sistemáticamente una fuente → validar por período y geografía.

> **Error frecuente:** leer diez errores llamativos y generalizar. El muestreo cualitativo debe combinarse con conteos y selección no sesgada.

> **Checkpoint 14**
>
> ¿Por qué analizar solo errores es insuficiente? Porque necesitamos compararlos con aciertos semejantes para identificar qué cambia. Sin denominador, una característica frecuente parece causa de error solo porque aparece en todo el corpus.

> **Ejercicio conceptual 20**
>
> Una clase cae en 2026, pero casi todos sus casos de ese año provienen de una nueva fuente. ¿Qué conclusión es válida?
>
> **Respuesta razonada:** hay una asociación entre caída, tiempo y composición de fuente; no sabemos cuál causa el problema. Hay que estratificar por fuente y período, revisar procesamiento y soporte, y evitar atribuirlo directamente a drift jurídico.

> **Ejercicio conceptual 21**
>
> El modelo falla más en textos largos. ¿Qué tres hipótesis competirían?
>
> **Respuesta razonada:** dilución de términos relevantes en TF-IDF, mezcla de múltiples materias dentro del documento o confusión con tipos documentales que suelen ser largos. También podría haber truncamiento. Se necesitan cruces y revisión.

---

## 15. Escalera de modelos para el futuro clasificador SAIJ

### 15.1 Principio de la escalera

La escalera ordena evidencia, no prestigio. Cada peldaño responde una pregunta que el siguiente no debe borrar. Si un modelo complejo mejora, la baseline permite medir cuánto. Si no mejora, evita seguir agregando costo sin señal.

### 15.2 Peldaño 0 — mayoría

Predice siempre la clase más frecuente de train. Comprueba distribución, pipeline de métricas y dificultad para clases minoritarias. En multiclase desbalanceada puede tener accuracy engañosa y macro recall muy bajo. Justamente por eso es indispensable.

### 15.3 Peldaño 1 — Naive Bayes

Usa probabilidades de términos por clase bajo independencia condicional aproximada. Es rápido, compatible con texto disperso y ofrece una referencia léxica. Materia 3 desarrolló su lógica. Aquí su función es responder: ¿cuánto aprende una regla simple de frecuencias de términos?

### 15.4 Peldaño 2 — regresión logística

Suma evidencia con regularización y produce probabilidades candidatas. Permite inspeccionar coeficientes y comparar L1/L2. Responde: ¿una frontera lineal discriminativa mejora la regla generativa simple?

### 15.5 Peldaño 3 — SVM lineal

Busca margen amplio y es compatible con alta dimensión dispersa. Responde: ¿la geometría de margen mejora discriminación respecto de logística bajo la misma representación? Si se necesitan probabilidades, la calibración se evalúa como paso separado.

### 15.6 Peldaño 4 — árbol individual

Sirve como control tabular y para explorar reglas condicionales sobre metadata legítima. No entra automáticamente sobre TF-IDF. Responde: ¿existen umbrales e interacciones útiles que una regla lineal no representa?

### 15.7 Peldaño 5 — random forest

Entra cuando el árbol muestra señal no lineal pero inestabilidad, o cuando la tabla curada justifica ensamble. Responde: ¿la diversidad y el promedio generalizan esas interacciones?

### 15.8 Peldaño 6 — boosting

Entra con presupuesto de tuning, suficiente soporte y evidencia de que correcciones secuenciales agregan valor. Responde: ¿un ensamble secuencial mejora errores relevantes sin degradar costo, calibración o estabilidad?

### 15.9 Regla de avance

Un candidato avanza solo si:

1. usa features legítimas;
2. supera controles en métricas predefinidas de manera estable y material;
3. no empeora clases críticas fuera de tolerancia;
4. respeta tiempo, memoria y latencia;
5. admite política de abstención y revisión;
6. queda documentado en ledger y model card;
7. no depende de test para tuning;
8. conserva trazabilidad de representación.

No se proclama ganador. El resultado correcto puede ser “la diferencia no justifica complejidad” o “faltan datos para decidir”.

### 15.10 Representaciones compatibles

| Peldaño | Texto disperso | Metadata tabular | Combinación | Condición |
|---|---|---|---|---|
| Mayoría | No usa | No usa | No usa | Prevalencia de train |
| Naive Bayes | Conteos/TF-IDF compatible | Limitado | Posible con cuidado | Supuestos de distribución |
| Logística | Muy adecuado | Adecuado con escalado/codificación | Muy adecuado si sigue disperso | Regularización |
| SVM lineal | Muy adecuado | Adecuado con escalado | Adecuado | Score y costo |
| Árbol | No prioritario en dimensión extrema | Adecuado | Requiere justificar | Profundidad y encoding |
| Bosque/boosting | Costoso sin transformación | Adecuado | Requiere evidencia | Memoria, tuning e importancia |

> **Checkpoint 15**
>
> ¿Qué ocurre si logística iguala a boosting? La opción lineal puede ser preferible por parsimonia, velocidad y explicación, salvo que boosting aporte otro beneficio comprobado. “Empate” no obliga a elegir complejidad.

> **Ejercicio conceptual 22**
>
> La SVM mejora macro F1, pero empeora mucho una confusión específica considerada crítica. ¿Avanza?
>
> **Respuesta razonada:** no automáticamente. La regla de avance incluye errores críticos. Se revisan umbrales, costos, calibración y soporte; si no puede cumplir tolerancia, la mejora promedio no basta.

---

## 16. Multiclase, abstención y revisión humana

### 16.1 Multiclase no es repetir binario sin pensar

En fuero hay varias clases exclusivas, posiblemente jerárquicas o ambiguas. Debemos registrar:

- clases incluidas y excluidas;
- tratamiento de “otros” y desconocidos;
- soporte por clase;
- estrategia nativa, OvR u OvO;
- macro, weighted y métricas por clase;
- matriz de confusión;
- calibración por clase;
- política ante empate o baja confianza.

Una clase “otros” heterogénea puede ser difícil porque no representa una regularidad positiva, sino restos. Una jerarquía quizá permita decidir primero una rama amplia y luego subfuero, pero eso cambia target y errores; no se adopta sin evidencia.

### 16.2 Macro, weighted y balanced

Macro da igual peso a cada clase; weighted pondera por soporte; micro agrega decisiones; balanced accuracy promedia recall. Ninguna reemplaza la lectura por clase. Bajo desbalance, una mejora weighted puede provenir de clases grandes.

### 16.3 Regla de abstención

Definamos (p_{(1)}) como la mayor probabilidad y (p_{(2)}) como la segunda. Una regla simple:

[
\text{aceptar si }p_{(1)}\ge\tau\quad\text{y}\quad p_{(1)}-p_{(2)}\ge\delta
]

**Símbolo por símbolo:**

- (p_{(1)}) es la probabilidad de la clase líder;
- (p_{(2)}) es la competidora inmediata;
- (\tau) es el umbral absoluto;
- (\delta) es la separación mínima;
- si no se cumplen ambos, el sistema deriva a revisión.

Para scores sin calibrar puede usarse margen relativo, pero su interpretación operacional se valida. Una regla específica por clase puede responder a costos distintos, siempre con soporte suficiente.

### 16.4 Cobertura y riesgo selectivo

La **cobertura** es la fracción de casos autoaceptados:

[
\operatorname{cobertura}=\frac{n_{aceptados}}{n_{total}}
]

El **riesgo selectivo** mide error entre aceptados:

[
\operatorname{riesgo}=\frac{n_{errores\ aceptados}}{n_{aceptados}}
]

Aumentar umbrales suele bajar cobertura y riesgo, pero no siempre de forma uniforme por clase o grupo. Si la abstención recae desproporcionadamente en una región o tipo documental, el flujo humano absorbe esa desigualdad y debe medirse.

### 16.5 Diseño de revisión humana

La revisión no es una frase final. Requiere:

- quién revisa;
- qué información ve;
- cuántos casos puede procesar;
- qué hace ante desacuerdo;
- cómo se registra corrección;
- si la corrección vuelve al dataset y con qué control;
- tiempo máximo;
- clases o subgrupos prioritarios;
- auditoría de automatizaciones aceptadas.

El modelo asiste; no inventa fundamento jurídico. La interfaz debe mostrar clase sugerida, alternativas, evidencia del texto, incertidumbre y versión, sin presentar correlaciones como explicación legal.

> **Error frecuente:** subir el umbral hasta lograr “99 % de precisión” sin reportar que solo se cubre 5 % de casos y ninguna clase minoritaria.

> **Checkpoint 16**
>
> ¿Qué tres números acompañan una política de abstención? Cobertura, error/riesgo entre aceptados y distribución de abstenciones por clase y subgrupo. También carga humana.

> **Ejercicio conceptual 23**
>
> Dos políticas tienen igual accuracy total: A automatiza 80 % con más errores; B automatiza 40 % con menos. ¿Cuál elegir?
>
> **Respuesta razonada:** depende de costos y capacidad de revisión. Se comparan curvas cobertura-riesgo, errores críticos y carga. Accuracy total no representa la decisión selectiva.

> **Ejercicio conceptual 24**
>
> Una clase minoritaria se abstiene en 70 % y una mayoritaria en 10 %. ¿Qué investigar?
>
> **Respuesta razonada:** soporte, calibración por clase, ambigüedad del target, longitud, fuentes y umbrales comunes. La política puede trasladar inequidad al equipo humano; quizá requiera umbrales o datos específicos, nunca ocultarlo.

---

## 17. Taller conceptual integrador

Los ejercicios anteriores ya superan el mínimo de veinte y aparecen antes de cualquier implementación. Este taller agrega casos de síntesis. Intentá resolverlos justificando cada paso; luego compará con la respuesta.

### Ejercicio 25 — cambio doble

Se reemplaza TF-IDF+logística por embeddings+boosting y mejora la métrica. ¿Qué conclusión puede sostenerse?

**Respuesta razonada:** solo que el pipeline completo nuevo rindió distinto bajo ese experimento. No puede atribuirse a boosting porque cambió representación y familia. Harían falta comparaciones cruzadas compatibles y control de cómo se aprendieron embeddings.

### Ejercicio 26 — probabilidad tentadora

Una SVM calibrada emite 0.95 para un documento corto de una fuente nueva. ¿Debe autoaceptarse?

**Respuesta razonada:** no por el número solo. Hay que revisar si calibración incluyó fuente y longitudes comparables, si existe drift y si la política exige margen entre clases. Puede estar fuera de distribución.

### Ejercicio 27 — importancia sospechosa

El identificador de organismo domina la importancia del bosque y mejora test aleatorio. ¿Qué experimento sigue?

**Respuesta razonada:** auditar linaje y disponibilidad, aplicar split por organismo o temporal según uso, comparar sin la feature y analizar organizaciones nuevas. El test aleatorio puede compartir organismos y premiar memorización.

### Ejercicio 28 — tuning excesivo

Tras 500 configuraciones, una supera por muy poco a la baseline en validación. ¿Qué riesgo aparece?

**Respuesta razonada:** sobreajuste a validación por búsqueda múltiple. Se examina estabilidad, presupuesto, parsimonia y test reservado. La cantidad de intentos debe constar en ledger.

### Ejercicio 29 — error asimétrico

Confundir A como B es más costoso que B como A. ¿Qué partes del sistema podrían adaptarse?

**Respuesta razonada:** pesos o pérdida durante aprendizaje, umbrales por clase, matriz de costos, abstención y priorización humana. La evaluación debe reportar ambas direcciones y no solo F1.

### Ejercicio 30 — forest y texto

Un bosque sobre 100 000 columnas TF-IDF agota memoria. ¿La conclusión es que random forest no sirve?

**Respuesta razonada:** no. Esa combinación de familia, representación e implementación no respeta recursos. Podría evaluarse con metadata o representación reducida justificada, sin asumir que conservará la misma señal.

### Ejercicio 31 — coeficientes que cambian

Las predicciones logísticas son estables, pero el ranking de palabras cambia entre folds. ¿Qué significa?

**Respuesta razonada:** features correlacionadas pueden intercambiar pesos mientras la suma mantiene decisiones. La explicación individual es inestable; conviene agrupar, reportar variabilidad y evitar narrativa sobre una sola palabra.

### Ejercicio 32 — “mejor” modelo

Logística, SVM y boosting quedan dentro de una diferencia práctica mínima. ¿Qué criterio desempata?

**Respuesta razonada:** parsimonia, estabilidad, calibración requerida, costo, memoria, explicación y mantenimiento. Si no hay diferencia material, no corresponde proclamar un ganador estadístico por decimales.

### Ejercicio 33 — clase nueva

Aparece un fuero no presente en train. ¿Qué hará un clasificador cerrado?

**Respuesta razonada:** forzará alguna clase conocida salvo mecanismo de rechazo. Se necesita detección de baja confianza o fuera de distribución, revisión humana y proceso de actualización de taxonomía.

### Ejercicio 34 — muestreo con fuga

Se sobremuestrea una clase antes de dividir y copias del mismo documento quedan en train y test. ¿Qué ocurre?

**Respuesta razonada:** test deja de ser independiente y la estimación se infla. Debe dividirse primero y sobremuestrear solo cada train-fold; además, duplicados reales deben agruparse.

---

## 18. Hoja de diseño del experimento SAIJ

Antes de implementar, completá esta hoja en lenguaje natural:

### 18.1 Contrato del problema

- **Unidad de predicción:** ________
- **Momento de inferencia:** ________
- **Target y fuente:** ________
- **Clases incluidas:** ________
- **Ambigüedades conocidas:** ________
- **Uso permitido:** ________
- **Uso prohibido:** ________

### 18.2 Datos y partición

- **Población y cobertura temporal:** ________
- **Grupos que no deben separarse:** ________
- **Reloj relevante:** ________
- **Train/valid/test:** ________
- **Features excluidas por fuga o política:** ________

### 18.3 Escalera

- **Mayoría:** qué verifica ________
- **Naive Bayes:** representación ________
- **Logística:** regularización a comparar ________
- **SVM lineal:** rango de (C) ________
- **Árbol/ensambles:** condición de entrada ________

### 18.4 Evaluación

- **Métrica primaria:** ________
- **Métricas secundarias:** ________
- **Confusiones críticas:** ________
- **Subgrupos:** ________
- **Calibración:** ________
- **Cobertura/abstención:** ________

### 18.5 Operación

- **Costo de inferencia tolerable:** ________
- **Capacidad de revisión:** ________
- **Umbral y quién lo aprueba:** ________
- **Monitoreo de drift:** ________
- **Frecuencia de reevaluación:** ________

Si una casilla no puede completarse, no se tapa con un valor por defecto. Se registra como decisión pendiente.

---

## 19. Puente posterior hacia implementación

La secuencia conceptual termina antes de escribir código. Cuando llegue el momento, el código deberá materializar decisiones ya justificadas:

1. cargar una versión identificada del dataset;
2. validar esquema y población;
3. crear splits una sola vez;
4. encapsular transformación y modelo;
5. ajustar cada paso únicamente en train;
6. seleccionar con validación;
7. cerrar configuración;
8. evaluar una vez en test;
9. producir ledger, análisis de errores y ficha;
10. decidir si el candidato avanza, se abstiene o se descarta.

Este capítulo no incluye código de biblioteca en la secuencia principal. Implementar sin haber completado la hoja anterior convertiría el notebook en una sucesión de pruebas sin pregunta. Cuando se programe, cada celda debería responder “qué decisión implementa” y “qué evidencia produce”.

---

## 20. Autoevaluación final de Materia 4

Marcá solo lo que puedas explicar con un ejemplo propio:

- [ ] Distingo familia, modelo, parámetro e hiperparámetro.
- [ ] Explico sesgo inductivo sin usarlo como sinónimo de error.
- [ ] Comparo geometría, escalado, capacidad, costo y representación.
- [ ] Calculo un score lineal y explico cada símbolo.
- [ ] Convierto un logit con sigmoide y no confundo probabilidad con verdad.
- [ ] Explico softmax y multiclase.
- [ ] Distingo L1 de L2 y sus trampas con correlación.
- [ ] Reconstruyo Gini, entropía y ganancia de un split.
- [ ] Relaciono profundidad, hojas y poda con generalización.
- [ ] Explico hiperplano, margen y vectores soporte.
- [ ] Distingo margen duro y blando, y el papel de (C).
- [ ] Explico kernel RBF y la intuición de (\gamma).
- [ ] Distingo bagging, random forest y boosting.
- [ ] Explico OOB y por qué no reemplaza siempre un split temporal.
- [ ] Relaciono tasa de aprendizaje, etapas y sobreajuste.
- [ ] Separo pesos, muestreo, métricas y umbrales ante desbalance.
- [ ] Diseñaría CV sin fuga y respetando grupos o tiempo.
- [ ] Explico por qué el pipeline es una frontera de aprendizaje.
- [ ] Distingo score, margen, probabilidad, calibración y decisión.
- [ ] Puedo diseñar un umbral con costos asimétricos sin inventar costos.
- [ ] Interpreto coeficientes e importancias con cautela.
- [ ] Reconozco trampas de correlación y alta cardinalidad.
- [ ] Comparo entrenamiento, inferencia y memoria.
- [ ] Mantengo matrices dispersas cuando corresponde.
- [ ] Registro una comparación reproducible en un ledger.
- [ ] Puedo completar una model card liviana.
- [ ] Analizo errores por clase, par, tiempo, geografía, tipo y longitud.
- [ ] Construyo la escalera mayoría → NB → logística/SVM → ensambles.
- [ ] Nunca proclamo un ganador sin evidencia controlada.
- [ ] Diseño abstención y revisión humana con cobertura y riesgo.

### Criterio de dominio

Considerá dominada la materia cuando puedas recibir una tabla con resultados y preguntar, antes de mirar el decimal mayor:

1. ¿qué representación recibió cada familia?;
2. ¿qué transformaciones se aprendieron dentro de train?;
3. ¿qué sesgo inductivo aporta cada candidata?;
4. ¿qué hiperparámetros se buscaron y cuántos intentos hubo?;
5. ¿qué futuro estima el split?;
6. ¿qué clases y subgrupos fallan?;
7. ¿los scores están calibrados?;
8. ¿qué umbral y costo producen la decisión?;
9. ¿cuánto cuesta entrenar e inferir?;
10. ¿la diferencia justifica la complejidad?;
11. ¿qué hallazgo fue reproducido por Javier?;
12. ¿qué todavía no sabemos?

---

## 21. Glosario de Materia 4

| Término | Definición operativa |
|---|---|
| **Bagging** | Entrenamiento paralelo sobre muestras bootstrap y agregación de predicciones. |
| **Bootstrap** | Muestra con reemplazo del conjunto de entrenamiento. |
| **Brier score** | Error cuadrático de probabilidades frente a outcomes binarios. |
| **Calibración** | Correspondencia entre probabilidades anunciadas y frecuencias observadas. |
| **Capacidad** | Variedad de patrones que una familia puede representar. |
| **Cobertura** | Fracción de casos que una política acepta automáticamente. |
| **Coeficiente** | Peso aprendido por un modelo lineal. |
| **Costo asimétrico** | Consecuencia distinta para diferentes tipos de error o acción. |
| **Decision boundary** | Conjunto de puntos donde cambia la clase decidida. |
| **Discriminación** | Capacidad de ordenar o separar clases mediante scores. |
| **Diversidad** | Diferencia útil entre errores de miembros de un ensamble. |
| **Entropía** | Medida de mezcla de clases usada en árboles. |
| **Feature subsampling** | Selección aleatoria de columnas candidatas para un split. |
| **Gamma** | Escala de influencia de ejemplos en kernels como RBF. |
| **Gini** | Medida de impureza basada en proporciones cuadradas. |
| **Grid search** | Evaluación sistemática de combinaciones predefinidas. |
| **Hinge loss** | Pérdida que penaliza casos dentro o del lado incorrecto del margen. |
| **Hiperplano** | Frontera lineal en un espacio de una o más dimensiones. |
| **Importancia por permutación** | Caída de métrica al romper una feature en evaluación. |
| **Intercepto** | Término constante de un modelo lineal. |
| **Kernel** | Función de similitud que habilita fronteras no lineales implícitas. |
| **L1** | Regularización por suma de valores absolutos, capaz de producir ceros. |
| **L2** | Regularización por suma de cuadrados, que contrae pesos grandes. |
| **Learning rate** | Tamaño de aporte de cada etapa de boosting. |
| **Margen** | Separación geométrica o score firmado respecto de una frontera SVM. |
| **Model card** | Ficha de propósito, datos, evaluación, límites y uso de un modelo. |
| **Out-of-bag** | Evaluación de cada caso con árboles cuyo bootstrap no lo incluyó. |
| **Poda** | Reducción o control de ramas para limitar complejidad de un árbol. |
| **Random forest** | Ensamble de árboles con bootstrap y submuestreo de features. |
| **Random search** | Muestreo de configuraciones desde rangos o distribuciones. |
| **Regularización** | Preferencia que controla complejidad durante ajuste. |
| **Riesgo selectivo** | Error entre casos aceptados por una política de abstención. |
| **Score** | Salida continua previa a una decisión; no necesariamente probabilidad. |
| **Sigmoide** | Función que transforma un logit binario al intervalo entre 0 y 1. |
| **Soft margin** | SVM que permite violaciones mediante una penalización. |
| **Softmax** | Normalización de scores multiclase a probabilidades que suman 1. |
| **Support vector** | Observación que determina o viola el margen de una SVM. |
| **Umbral** | Regla que convierte score o probabilidad en acción. |
| **Validación anidada** | Separación opcional entre selección interna y evaluación externa del procedimiento. |

---

## 22. Puente a Materia 5: Aprendizaje No Supervisado

Materia 4 asumió que cada ejemplo trae un target. Aprendizaje No Supervisado cambia la pregunta: busca estructura sin una etiqueta externa que diga qué respuesta es correcta.

El puente será:

```text
Aprendizaje Supervisado
  → compara predicciones contra targets conocidos
  → detecta límites de representación y errores
  → Aprendizaje No Supervisado explora similitud, grupos y dimensiones
  → la interpretación humana decide qué estructura tiene sentido
```

Materia 5 retoma este cierre sin borrar su lógica: estudiará, dentro del alcance local y con complementos explícitamente acotados, distancia y similitud, clustering, representación, reducción dimensional, embeddings y evaluación sin verdad externa directa. Para SAIJ puede ayudar a explorar colecciones, encontrar grupos temáticos, detectar casos atípicos o preparar búsqueda semántica. No “descubrirá fueros verdaderos” automáticamente.

La pregunta de cierre es:

> Si quitamos el target, ¿qué estructura crea nuestra representación, cómo sabemos si es estable y qué significado jurídico estamos autorizados a darle?

---

