# Materia 5 — Aprendizaje No Supervisado

> **Idea rectora:** sin un target externo, el algoritmo no recibe una respuesta correcta que deba imitar. Recibe una representación, una noción de cercanía y un criterio de estructura. Por eso el resultado no es una verdad jurídica descubierta: es una organización propuesta que debe evaluarse, interpretarse y auditarse.

Esta materia conecta tres movimientos. El primero es **representar**: decidir qué aspectos de cada objeto se vuelven números. El segundo es **organizar o comprimir**: agrupar, ordenar, reducir dimensiones o detectar observaciones que no se parecen al resto. El tercero es **interpretar**: preguntar si esa estructura es estable, útil y jurídicamente defendible. Cambiar cualquiera de los tres puede cambiar el resultado.

En SAIJ, este marco permite pensar exploración temática, navegación del corpus, búsqueda de documentos parecidos, detección de duplicados aproximados, selección de muestras para revisión y generación de candidatos semánticos. No autoriza a declarar que un grupo calculado es un fuero verdadero, una doctrina consolidada o una categoría legal natural. Esa frontera se repetirá porque es la protección conceptual más importante de la materia.

## 0. Cómo estudiar esta materia

### 0.1 Recorrido didáctico

Cada bloque sigue la misma secuencia:

```text
intuición
  → vocabulario preciso
  → ejemplo inventado trabajado a mano
  → fórmula explicada símbolo por símbolo
  → interpretación
  → error frecuente
  → checkpoint
  → transferencia hipotética a SAIJ
  → ejercicio conceptual
```

Los ejemplos con letras, vectores pequeños y documentos ficticios son **ilustraciones inventadas**. Sirven para aprender a razonar y no describen el corpus SAIJ. Las posibles aplicaciones a jurisprudencia se expresan como hipótesis de uso. No se informan clusters, métricas, tiempos ni desempeños reales del equipo.

### 0.2 Qué evidencia se distingue

| Rótulo | Qué significa en esta materia |
|---|---|
| **Teoría general** | Concepto matemático o metodológico desarrollado para poder estudiarlo sin otra fuente. |
| **Ejemplo inventado** | Caso pequeño construido para calcular a mano; no es evidencia sobre SAIJ. |
| **Alcance local verificado** | Tema visible en el inventario local del curso, especialmente clustering y embeddings. |
| **Complemento conceptual acotado** | Explicación incorporada para cerrar una conexión necesaria, sin presentarla como cobertura comprobada de la cursada. |
| **Hallazgo del equipo pendiente de reproducción** | Resultado que solo podría afirmarse después de rehacer el análisis. En esta materia no se adopta ninguno como hecho. |
| **Decisión pendiente de Javier** | Elección sobre representación, muestra, métrica, revisión o uso que debe justificarse con el corpus real. |

### 0.3 Alcance y omisiones honestas

Los materiales locales inventariados sostienen como ejes explícitos la introducción al clustering, una continuación de métodos de clustering y embeddings. La materia desarrolla esos ejes y agrega los fundamentos necesarios para comprenderlos. **PCA** se incluye como complemento conceptual acotado porque el objetivo de esta guía exige conectar reducción dimensional con representación y exploración. No se afirma que el inventario local disponible demuestre una clase específica de PCA.

**DBSCAN, t-SNE y UMAP no se desarrollan como métodos de la cursada** porque no aparecen identificados en los materiales locales actualmente disponibles. Más adelante se explica qué hueco deja cada omisión y qué advertencia debe conservarse si se estudian en el futuro. Esta decisión evita completar una lista de algoritmos con teoría no trazada. La profundidad se concentra en lo que sí se necesita para razonar: geometría, k-means, clustering jerárquico, evaluación, estabilidad, PCA como puente y embeddings.

### Checkpoint 0

Antes de avanzar, deberías poder explicar:

1. por qué “sin target” no significa “sin criterio”;
2. por qué un cluster no es automáticamente una categoría jurídica;
3. qué diferencia existe entre un ejemplo inventado y un resultado empírico;
4. por qué se puede profundizar un alcance acotado sin fingir cobertura local.

---

## 1. Qué cambia cuando no hay un target externo

### 1.1 Del error contra una respuesta a la coherencia de una estructura

En aprendizaje supervisado, cada ejemplo suele venir acompañado por un target (y_i). Un clasificador propone (hat y_i) y existe una referencia externa contra la cual medir el error. En aprendizaje no supervisado observamos (x_i), pero no recibimos una (y_i) que diga “este es el grupo correcto”, “esta es la dimensión correcta” o “este documento debe ocupar exactamente este lugar”.

Eso no elimina los objetivos. Los desplaza. Hay que elegir una función que represente qué estructura interesa. k-means, por ejemplo, busca centroides que reduzcan distancias cuadráticas dentro de grupos. Un método jerárquico decide qué grupos fusionar mediante un criterio de enlace. PCA busca direcciones que conserven mucha varianza lineal. Una búsqueda por coseno ordena candidatos según el ángulo entre representaciones. Cada uno responde una pregunta distinta.

La frase “los datos hablaron” es engañosa. Los datos fueron:

1. seleccionados desde una población;
2. curados con reglas;
3. convertidos en variables;
4. escalados o normalizados;
5. comparados con una métrica;
6. procesados por un algoritmo con hiperparámetros;
7. interpretados por una persona.

La estructura resultante depende de toda esa cadena.

### 1.2 Cinco metas que no deben confundirse

| Meta | Pregunta | Salida típica | Criterio de éxito |
|---|---|---|---|
| **Descubrimiento** | ¿Qué patrones o vecindades merece la pena investigar? | Grupos, componentes, vecinos, perfiles. | Utilidad exploratoria y estabilidad, no “verdad automática”. |
| **Compresión** | ¿Cómo resumir muchas variables conservando información relevante? | Menos dimensiones o prototipos. | Información retenida frente a pérdida aceptable. |
| **Segmentación** | ¿Cómo dividir objetos para una acción diferenciada? | Asignación a segmentos. | Utilidad para la acción y ausencia de daño injustificado. |
| **Detección de anomalías** | ¿Qué casos se alejan de un patrón de referencia? | Score o lista de casos atípicos. | Capacidad de priorizar revisión sin equiparar rareza con error. |
| **Recuperación** | ¿Qué documentos son más pertinentes para una consulta? | Ranking de candidatos. | Relevancia de los primeros resultados medida con juicios de referencia. |

Un mismo cálculo de distancia puede participar en varias metas, pero las metas no son intercambiables. Un punto distante de todos los centroides puede priorizarse para revisión de anomalías; eso no lo convierte en fraude ni en dato inválido. Un embedding puede servir para recuperar vecinos; eso no significa que sus clusters sean segmentos operativos adecuados.

### 1.3 Ejemplo inventado: seis documentos, tres objetivos

Imaginemos seis textos ficticios representados por dos cantidades: frecuencia relativa de términos sobre contratos y frecuencia relativa de términos sobre responsabilidad. Los valores son inventados:

| Documento | Contratos | Responsabilidad |
|---|---:|---:|
| A | 8 | 1 |
| B | 7 | 2 |
| C | 1 | 8 |
| D | 2 | 7 |
| E | 4 | 4 |
| F | 9 | 8 |

Para **descubrimiento**, podríamos preguntar si A–B y C–D forman vecindades visibles. Para **anomalías**, F podría merecer revisión por combinar valores altos que no siguen esos pares. Para **recuperación**, una consulta representada como ((8,2)) podría ordenar A y B primero. Son tres lecturas de la misma tabla, con tres criterios de evaluación distintos.

Nada permite llamar al grupo A–B “derecho contractual verdadero”. Las dos variables fueron elegidas por alguien y no capturan toda la semántica. E podría ser un documento generalista, un caso mixto o un artefacto de representación. F podría ser muy informativo en lugar de defectuoso.

### Error frecuente

> “Como no hay etiquetas, el método es objetivo.”

No. La ausencia de etiquetas elimina una fuente de supervisión, pero aumenta el peso de otras decisiones: muestra, representación, distancia, escala, algoritmo, número de grupos y lectura humana.

### Transferencia a SAIJ

Una exploración no supervisada puede proponer conjuntos de documentos para que una persona revise temas, duplicados o casos fronterizos. La formulación correcta sería: “con esta versión del corpus, esta representación y este criterio, estos documentos quedaron próximos”. La formulación incorrecta sería: “el algoritmo descubrió las categorías jurídicas reales”.

### Checkpoint 1

Si dos personas usan el mismo corpus pero una representa metadatos y otra embeddings del texto, ¿deben esperar los mismos grupos? No. Cambiaron el espacio y, con él, la noción de similitud que el algoritmo puede ver.

---

## 2. La representación precede al algoritmo

### 2.1 Un algoritmo solo ve números

Un documento jurídico tiene hechos, argumentos, citas, decisiones, estructura, fecha, órgano y contexto. Un algoritmo no supervisado no recibe esos conceptos directamente. Recibe un vector:

\[
\mathbf{x}_i = (x_{i1}, x_{i2}, \ldots, x_{ip})
\]

Símbolo por símbolo:

- (mathbf{x}_i): representación completa del objeto (i);
- (i): índice del documento u observación;
- (x_{ij}): valor de la característica (j) para el objeto (i);
- (j): índice de característica;
- (p): cantidad total de características o dimensiones.

La fórmula no dice qué significa cada dimensión. Ese significado nace del diseño de representación.

### 2.2 Metadatos

Una representación de metadatos podría incluir año, jurisdicción, tipo de resolución, órgano, longitud y presencia de ciertos campos. Tiene ventajas: suele ser interpretable y admite filtros claros. También tiene límites: dos documentos pueden compartir metadatos y tratar problemas jurídicos muy diferentes; una categoría administrativa puede dominar la geometría; un campo faltante puede representar ausencia real o falla de extracción.

Las variables categóricas requieren una codificación. Si se codifica “provincia A = 1, B = 2, C = 3”, la distancia numérica inventa un orden y diferencias que quizá no existen. Una codificación one-hot evita ese orden, pero aumenta dimensiones y cambia el peso relativo de bloques con muchas categorías.

### 2.3 TF-IDF: importancia léxica relativa

TF-IDF representa un documento mediante términos. Una forma común es:

\[
\operatorname{tfidf}(t,d)=\operatorname{tf}(t,d)\times\log\left(\frac{N}{\operatorname{df}(t)}\right)
\]

Símbolo por símbolo:

- (t): término;
- (d): documento;
- (operatorname{tf}(t,d)): frecuencia del término (t) dentro de (d), en forma bruta o normalizada;
- (N): cantidad de documentos del corpus de ajuste;
- (operatorname{df}(t)): cantidad de documentos que contienen (t);
- (log): logaritmo, que comprime diferencias extremas;
- el producto: combina presencia local con rareza global.

**Ejemplo inventado.** Hay (N=4) documentos. “apelación” aparece dos veces en el documento A y aparece en (2) de los (4) documentos. Si usamos frecuencia bruta:

\[
\operatorname{tfidf}(\text{apelación},A)
=2\times\log(4/2)
=2\log 2.
\]

Si “sentencia” aparece dos veces en A pero en los (4) documentos:

\[
2\times\log(4/4)=2\log 1=0.
\]

En esta variante simplificada, “sentencia” no discrimina documentos porque es ubicua. En implementaciones reales suele haber suavizados y normalizaciones; la intuición se mantiene: un término pesa más cuando es frecuente en el documento y menos común en el corpus.

**Interpretación:** TF-IDF captura coincidencia y contraste léxico. No comprende por sí solo que “revocar la resolución” y “dejar sin efecto el pronunciamiento” pueden ser semánticamente cercanos con vocabulario distinto.

### 2.4 Embeddings: representación densa aprendida

Un embedding asigna un vector denso:

\[
f(d)=\mathbf{z}_d\in\mathbb{R}^{m}.
\]

- (f): modelo o función de representación;
- (d): documento o fragmento;
- (mathbf{z}_d): embedding resultante;
- (mathbb{R}^{m}): espacio de (m) números reales;
- (m): dimensión del embedding.

“Denso” significa que muchas coordenadas pueden tener valores distintos de cero. A diferencia de TF-IDF, cada coordenada aislada no suele equivaler a una palabra interpretable. El significado surge del patrón completo y del entrenamiento del modelo.

Un embedding puede acercar expresiones con sentido parecido aunque no compartan palabras exactas. También puede perder distinciones jurídicas finas, heredar sesgos, confundir jurisdicciones o representar mal textos largos si el método de segmentación no es adecuado.

### 2.5 La geometría es una hipótesis

Al elegir representación se elige qué diferencias pueden importar. Con metadatos, cercanía puede significar misma época y órgano. Con TF-IDF, compartir términos distintivos. Con embeddings, semejanza semántica según un modelo. Ninguna definición es universal.

### Error frecuente

> “Probemos k-means y después vemos qué significan las columnas.”

El orden correcto es inverso. Primero se define qué debe significar cercanía para la pregunta. Después se elige un algoritmo compatible.

### Transferencia a SAIJ

Antes de agrupar, Javier debe registrar qué unidad representa: sentencia completa, sumario, párrafo, fundamento, metadatos o combinación. Dos fallos extensos pueden ser cercanos por fórmulas procesales repetidas y lejanos por cuestión de fondo. Esa tensión no se resuelve cambiando de algoritmo si la unidad de representación sigue siendo ambigua.

### Checkpoint 2

Explicá por qué agregar la variable “cantidad de caracteres” a TF-IDF puede alterar clusters. La distancia pasa a mezclar una señal de longitud con señales léxicas; si no se escala y justifica, la longitud puede dominar o deformar la geometría.

---

## 3. Escalado y normalización: dos operaciones distintas

### 3.1 Por qué las unidades dominan distancias

Supongamos dos variables: año entre 1990 y 2026, y longitud entre 500 y 100.000 caracteres. Una diferencia de 20.000 caracteres puede eclipsar una diferencia temporal de veinte años en distancia euclídea. El algoritmo no sabe que las unidades no son comparables.

### 3.2 Estandarización por variable

Una transformación frecuente es el puntaje estándar:

\[
z_{ij}=\frac{x_{ij}-\mu_j}{\sigma_j}.
\]

- (x_{ij}): valor original de la observación (i) en la variable (j);
- (mu_j): media de la variable (j), aprendida en el conjunto de ajuste;
- (sigma_j): desvío estándar de esa variable;
- (z_{ij}): valor centrado y medido en desvíos estándar.

**Ejemplo inventado.** Si la longitud media es (10.000), el desvío es (2.000) y un documento mide (14.000):

\[
z=(14.000-10.000)/2.000=2.
\]

Se interpreta como “dos desvíos por encima de la media”, no como “dos caracteres”.

Estandarizar no vuelve automáticamente razonable una variable. Solo cambia la escala. Un identificador numérico estandarizado sigue siendo un identificador sin significado geométrico.

### 3.3 Normalización por fila

En texto suele interesar la dirección del vector más que su magnitud. La normalización L2 convierte cada vector no nulo en longitud uno:

\[
\hat{\mathbf{x}}_i=\frac{\mathbf{x}_i}{\lVert\mathbf{x}_i\rVert_2},
\qquad
\lVert\mathbf{x}_i\rVert_2=\sqrt{\sum_{j=1}^{p}x_{ij}^2}.
\]

- \(\lVert\mathbf{x}_i\rVert_2\): norma euclídea del vector;
- \(\hat{\mathbf{x}}_i\): vector normalizado;
- cada coordenada se divide por la misma longitud;
- el vector conserva dirección y pierde magnitud absoluta.

**Ejemplo inventado.** Para (mathbf{x}=(3,4)), la norma es (sqrt{9+16}=5). Entonces:

\[
\hat{\mathbf{x}}=(3/5,4/5)=(0{,}6,0{,}8).
\]

### 3.4 Escalar columnas no es normalizar filas

- **Escalado por columna:** compara variables en unidades compatibles.
- **Normalización por fila:** compara objetos por dirección relativa.

Se pueden combinar cuando el diseño lo justifica, pero no son sinónimos.

### 3.5 Fuga y reproducibilidad

Si hay una evaluación futura o una muestra retenida, medias, desvíos, vocabulario TF-IDF y otras transformaciones deben aprenderse solo con el conjunto de ajuste. Aunque la tarea no tenga target, usar toda la colección para construir la representación puede filtrar información de evaluación y producir una estimación optimista de estabilidad o recuperación.

### Error frecuente

> “Como el método no es supervisado, puedo ajustar el preprocesamiento con todos los datos.”

No si se pretende medir generalización a documentos nuevos. La separación evaluación–ajuste sigue teniendo sentido.

### Transferencia a SAIJ

La decisión pendiente no es “usar StandardScaler”. Es decidir qué variables deben ser comparables, si la magnitud del texto tiene significado, si los embeddings se normalizan y cuál es la colección usada para aprender parámetros.

---

## 4. Distancia euclídea, Manhattan y similitud coseno

### 4.1 Distancia euclídea

La distancia euclídea entre dos vectores (mathbf{x}) y (mathbf{y}) es:

\[
d_2(\mathbf{x},\mathbf{y})
=\sqrt{\sum_{j=1}^{p}(x_j-y_j)^2}.
\]

Símbolo por símbolo:

- (p): número de dimensiones;
- (x_j), (y_j): coordenadas (j) de los dos objetos;
- (x_j-y_j): diferencia en esa coordenada;
- el cuadrado evita cancelaciones y penaliza diferencias grandes;
- la suma combina dimensiones;
- la raíz devuelve la unidad original cuando las variables comparten unidad.

**Ejemplo inventado.** Sean (mathbf{x}=(1,2)) y (mathbf{y}=(4,6)):

\[
d_2=\sqrt{(1-4)^2+(2-6)^2}
=\sqrt{9+16}=5.
\]

Interpretación: es la longitud de la línea recta entre ambos puntos.

### 4.2 Distancia Manhattan

\[
d_1(\mathbf{x},\mathbf{y})
=\sum_{j=1}^{p}|x_j-y_j|.
\]

- (|x_j-y_j|): diferencia absoluta en la dimensión (j);
- la suma agrega desplazamientos por ejes;
- no eleva al cuadrado, por lo que una diferencia grande no crece tan rápido como en la suma cuadrática.

Con los mismos puntos:

\[
d_1=|1-4|+|2-6|=3+4=7.
\]

Interpretación: recorrido total si solo pudiéramos movernos horizontal y verticalmente. Puede ser útil cuando interesa una suma de cambios absolutos, pero sigue requiriendo escalas justificadas.

### 4.3 Similitud coseno

\[
\cos(\mathbf{x},\mathbf{y})
=\frac{\mathbf{x}\cdot\mathbf{y}}
{\lVert\mathbf{x}\rVert_2\lVert\mathbf{y}\rVert_2}
=\frac{\sum_{j=1}^{p}x_jy_j}
{\sqrt{\sum_j x_j^2}\sqrt{\sum_j y_j^2}}.
\]

- \(\mathbf{x}\cdot\mathbf{y}\): producto punto;
- \(\lVert\mathbf{x}\rVert_2\), \(\lVert\mathbf{y}\rVert_2\): longitudes;
- el cociente mide alineación angular;
- para vectores no negativos suele quedar entre 0 y 1; en general puede ir de (-1) a (1).

**Ejemplo inventado.** (mathbf{x}=(1,1)), (mathbf{y}=(2,0)):

\[
\mathbf{x}\cdot\mathbf{y}=2,
\quad \lVert\mathbf{x}\rVert=\sqrt2,
\quad \lVert\mathbf{y}\rVert=2,
\]

\[
\cos(\mathbf{x},\mathbf{y})=\frac{2}{2\sqrt2}=\frac{1}{\sqrt2}\approx0{,}707.
\]

No mide coincidencia de magnitud; mide dirección.

### 4.4 Material complementario integrado 1 — Maldición de la dimensionalidad

Al crecer (p), el volumen de un espacio crece tan rápido que una cantidad fija de puntos queda dispersa. Intuitivamente, hay muchas maneras de diferir en al menos una dimensión. Los “vecinos” pueden dejar de ser realmente cercanos y las distancias pueden concentrarse: la diferencia relativa entre el vecino más próximo y uno lejano se reduce.

Un ejemplo geométrico ayuda. En una línea, una cuadrícula con diez posiciones cubre el espacio con diez puntos. En dos dimensiones, mantener la misma resolución requiere (10^2=100). En cien dimensiones requeriría (10^{100}), una cantidad imposible. No es una receta literal de muestreo; muestra el crecimiento combinatorio.

En TF-IDF, miles de dimensiones no vuelven inútil la representación: la matriz suele ser dispersa y el coseno puede funcionar bien. Pero obliga a preguntar qué términos son ruido, qué tan estables son los vecinos y si la señal semántica se diluye. En embeddings densos, muchas dimensiones tampoco garantizan mejor semántica; la geometría depende del entrenamiento.

**Consecuencia práctica:** no se elige una métrica por tradición. Se examinan distribución de distancias, vecinos cualitativos, estabilidad y desempeño en la tarea.

### 4.5 Material complementario integrado 2 — Coseno y euclídea después de normalizar

Si (hat{\mathbf{x}}) y (hat{\mathbf{y}}) tienen norma uno:

\[
\lVert\hat{\mathbf{x}}-\hat{\mathbf{y}}\rVert_2^2
=2-2\cos(\hat{\mathbf{x}},\hat{\mathbf{y}}).
\]

Derivación:

\[
\lVert\hat{\mathbf{x}}-\hat{\mathbf{y}}\rVert^2
=\lVert\hat{\mathbf{x}}\rVert^2+\lVert\hat{\mathbf{y}}\rVert^2
-2\hat{\mathbf{x}}\cdot\hat{\mathbf{y}}.
\]

Como ambas normas valen (1), queda (1+1-2cos=2-2cos).

Interpretación: sobre la esfera unitaria, ordenar por mayor coseno equivale a ordenar por menor distancia euclídea. No significa que las métricas sean siempre iguales. La equivalencia de ranking requiere normalización y comparación coherente.

### Errores frecuentes

1. comparar variables de unidades distintas sin escalar;
2. usar coseno con vectores cero, donde el denominador no existe;
3. creer que similitud (0{,}9) tiene significado universal;
4. interpretar cercanía del embedding como equivalencia jurídica;
5. cambiar normalización entre indexación y consulta.

### Transferencia a SAIJ

Para recuperar textos por contenido, TF-IDF o embeddings normalizados con coseno son candidatos razonables. Para metadatos mixtos, una distancia numérica simple puede ser insuficiente. La elección debe vincularse a una pregunta: coincidencia léxica, proximidad semántica, perfil administrativo o combinación controlada.

### Checkpoint 3

Dos embeddings tienen coseno (0{,}95). ¿Son jurídicamente equivalentes? No. Solo son muy alineados según ese modelo y preprocesamiento. La equivalencia exige revisar contenido, jurisdicción, tiempo, rol procesal y propósito.

---

## 5. Qué es un cluster y qué supuestos quedan ocultos

### 5.1 Definición operativa

Un cluster es un conjunto de observaciones consideradas más cohesionadas entre sí, o mejor separadas de otras, **según una representación y un criterio**. La definición parece circular porque cada método formaliza cohesión de manera distinta.

- k-means favorece grupos compactos alrededor de medias;
- single linkage favorece conectividad por cadenas de vecinos;
- complete linkage controla el par más lejano dentro de la fusión;
- Ward favorece fusiones con pequeño aumento de variación interna;
- una comunidad de red se define por enlaces, no necesariamente por distancia vectorial.

No hay una esencia de “cluster” independiente del método.

### 5.2 Supuestos que siempre conviene escribir

1. **Unidad:** qué representa cada fila.
2. **Población:** qué objetos entraron y cuáles no.
3. **Representación:** qué información se conservó.
4. **Escala:** qué magnitudes se igualaron o preservaron.
5. **Métrica:** qué significa cercanía.
6. **Forma:** qué geometrías puede recuperar el método.
7. **Densidad o tamaño:** qué diferencias tolera.
8. **Resolución:** cuántos grupos o qué corte se pide.
9. **Estabilidad:** cuánto cambia con semillas o muestras.
10. **Interpretación:** quién nombra y con qué evidencia.

### 5.3 Grupo geométrico, segmento operativo y categoría humana

- **Grupo geométrico:** conjunto producido por un criterio matemático.
- **Segmento operativo:** conjunto usado para una acción concreta.
- **Categoría humana:** concepto con significado disciplinar o jurídico.

Pueden coincidir parcialmente, pero no son sinónimos. Un grupo geométrico puede mezclar temas por lenguaje formal compartido. Una categoría jurídica puede dividirse en varios grupos por época o estilo. Un segmento operativo puede combinar grupos para distribuir revisión.

### Error frecuente

Poner un nombre atractivo a un cluster y tratar el nombre como si hubiera sido encontrado por el algoritmo. El algoritmo produjo una asignación; el nombre lo aporta una persona.

### Transferencia a SAIJ

Si un grupo contiene términos asociados a contratos, solo puede rotularse provisionalmente como “alta presencia de vocabulario contractual en esta muestra y representación”. Convertirlo en “jurisprudencia contractual” requiere revisar documentos, criterios de inclusión y falsos miembros.

---

## 6. k-means desde primeros principios

### 6.1 Intuición

k-means busca (K) puntos representativos llamados centroides. Alterna dos pasos:

1. asignar cada observación al centroide más cercano;
2. mover cada centroide a la media de sus observaciones.

Repite hasta que las asignaciones o el objetivo cambian muy poco.

### 6.2 Centroide

Para el cluster (C_k), su centroide es:

\[
\boldsymbol{\mu}_k=\frac{1}{|C_k|}\sum_{\mathbf{x}_i\in C_k}\mathbf{x}_i.
\]

- (C_k): conjunto de observaciones asignadas al grupo (k);
- (|C_k|): cantidad de observaciones del grupo;
- (mathbf{x}_i): vector de la observación (i);
- \(\boldsymbol{\mu}_k\): media coordenada por coordenada.

El centroide puede no ser una observación real. En texto, un centroide TF-IDF no es un documento; es un perfil promedio de pesos.

### 6.3 Asignación

\[
c_i=\arg\min_{k\in\{1,\ldots,K\}}
\lVert\mathbf{x}_i-\boldsymbol{\mu}_k\rVert_2^2.
\]

- (c_i): cluster asignado a (i);
- (arg\min): índice (k) que minimiza la expresión;
- (K): número fijado de clusters;
- la distancia cuadrática favorece cercanía euclídea al centro.

### 6.4 Objetivo o inercia

\[
J=\sum_{k=1}^{K}\sum_{\mathbf{x}_i\in C_k}
\lVert\mathbf{x}_i-\boldsymbol{\mu}_k\rVert_2^2.
\]

- suma interna: dispersión cuadrática de cada punto respecto de su centroide;
- suma externa: dispersión total de todos los grupos;
- (J): inercia o within-cluster sum of squares.

k-means intenta reducir (J). Una inercia menor para el mismo (K), datos y preprocesamiento indica grupos más compactos según esa geometría. No demuestra significado jurídico.

### 6.5 Ejemplo inventado trabajado a mano

Datos unidimensionales: (1,2,8,9). Elegimos (K=2) y centroides iniciales (mu_1=1), (mu_2=8).

**Asignación:**

- (1) y (2) están más cerca de (1);
- (8) y (9) están más cerca de (8).

Quedan (C_1=\{1,2\}), (C_2=\{8,9\}).

**Actualización:**

\[
\mu_1=(1+2)/2=1{,}5,
\qquad
\mu_2=(8+9)/2=8{,}5.
\]

**Inercia:**

\[
J=(1-1{,}5)^2+(2-1{,}5)^2+(8-8{,}5)^2+(9-8{,}5)^2=1.
\]

Otra iteración conserva las asignaciones; el algoritmo converge. El ejemplo es fácil porque hay una separación evidente. En espacios reales puede haber solapamiento, ruido y muchos mínimos locales.

### 6.6 Inicialización y óptimos locales

El objetivo no es convexo respecto de asignaciones y centroides juntos. Diferentes puntos iniciales pueden conducir a soluciones distintas. Una inicialización cuidadosa como k-means++ separa centros iniciales de manera probabilística y suele mejorar el punto de partida, pero no garantiza el óptimo global.

La práctica responsable es ejecutar múltiples semillas, comparar inercia y, más importante, estudiar estabilidad e interpretación. Reportar una sola corrida oculta incertidumbre algorítmica.

### 6.7 Elegir K

No existe un (K) universal. Criterios posibles:

- **propósito:** cuántos grupos puede revisar o usar una persona;
- **curva de inercia:** buscar un cambio de pendiente, no un “codo” siempre evidente;
- **silhouette:** evaluar cohesión y separación;
- **estabilidad:** observar si la estructura persiste;
- **interpretabilidad:** inspeccionar prototipos y documentos;
- **restricciones del dominio:** evitar una resolución que mezcle categorías relevantes o fragmente sin utilidad.

La inercia nunca aumenta al incrementar (K); con (K=n), cada punto puede ser su centro y (J=0). Por eso minimizar inercia sin penalización elegiría una solución inútil.

### 6.8 Supuestos y limitaciones

k-means funciona mejor cuando los grupos son aproximadamente compactos, comparables en escala y separables alrededor de medias bajo distancia euclídea. Tiene dificultades con:

- formas curvas o no convexas;
- tamaños muy distintos;
- densidades diferentes;
- outliers que desplazan medias;
- variables sin escalado;
- texto disperso de dimensión alta sin representación adecuada;
- clusters cuyo centro promedio carece de sentido.

### 6.9 Ejemplo de forma

Imaginemos puntos sobre dos medias lunas entrelazadas. Cada media luna es una estructura intuitiva, pero un corte por cercanía a centroides produce regiones convexas y puede partir ambas lunas. El error no se arregla aumentando iteraciones; surge del supuesto geométrico.

### Error frecuente

> “El mejor K es el que maximiza silhouette.”

Ese valor es una evidencia interna, no una orden. Puede favorecer particiones gruesas, ignorar grupos pequeños relevantes o reflejar artefactos de representación.

### Transferencia a SAIJ

k-means podría resumir perfiles de documentos para exploración. Antes de nombrarlos habría que revisar términos o vecinos representativos, documentos cercanos y lejanos al centro, mezcla de metadatos y estabilidad. Un cluster pequeño no es automáticamente una anomalía; uno grande no es una categoría dominante verdadera.

### Checkpoint 4

Si se duplica numéricamente una variable sin escalar, ¿puede cambiar k-means? Sí. Sus diferencias cuadráticas pesan cuatro veces más, porque ((2\Delta)^2=4\Delta^2).

---

## 7. Silhouette: cohesión y separación con cautela

### 7.1 Definición por observación

Para una observación (i):

- (a(i)): distancia media entre (i) y los demás puntos de su propio cluster;
- (b(i)): menor distancia media entre (i) y los puntos de cualquier otro cluster;
- el silhouette es:

\[
s(i)=\frac{b(i)-a(i)}{\max\{a(i),b(i)\}}.
\]

El valor suele estar entre (-1) y (1).

- cercano a (1): (i) está mucho más cerca de su grupo que del grupo alternativo;
- cerca de (0): está en una frontera o hay solapamiento;
- negativo: en promedio está más cerca de otro grupo.

### 7.2 Ejemplo inventado

Para un punto, supongamos (a(i)=2) y (b(i)=5):

\[
s(i)=\frac{5-2}{\max(2,5)}=3/5=0{,}6.
\]

Tiene mejor cohesión interna que cercanía al grupo vecino. Si (a=4) y (b=3):

\[
s=(3-4)/4=-0{,}25,
\]

lo que sugiere una asignación problemática bajo esa distancia.

### 7.3 Promedio y distribución

La media global resume, pero puede ocultar:

- un cluster excelente y otro pobre;
- grupos pequeños con valores negativos;
- observaciones frontera jurídicamente valiosas;
- dependencia de escala y métrica;
- preferencia por formas compactas.

Conviene mirar distribución por cluster, tamaños, casos extremos y estabilidad. No usar un decimal aislado como certificado.

### Transferencia a SAIJ

Un silhouette bajo puede señalar que la representación no separa temas, que existen documentos híbridos o que la estructura no es de clusters compactos. No demuestra que el corpus esté mal. Un silhouette alto puede provenir de una variable administrativa dominante y tampoco demuestra utilidad semántica.

### Checkpoint 5

¿Se pueden comparar directamente silhouettes calculados con representaciones distintas? Solo con cautela. Cada representación cambia distancias y pregunta. La comparación es parte de una evaluación de alternativas, no una equivalencia natural.

---

## 8. Clustering jerárquico aglomerativo

### 8.1 Intuición

El enfoque aglomerativo comienza con cada observación como un cluster individual. En cada paso fusiona los dos clusters más próximos según un criterio de enlace. Continúa hasta reunir todo en un único grupo o hasta una condición de parada.

La salida completa no es una partición fija sino una historia de fusiones.

### 8.2 Matriz de distancias y fusión por pares

Con (n) observaciones, se calculan o actualizan distancias entre grupos. Al inicio, los grupos son puntos. Luego, la pregunta “distancia entre dos grupos” necesita una definición.

**Ejemplo inventado unidimensional:** A=1, B=2, C=8, D=10.

Distancias iniciales: AB=1, CD=2, BC=6, AC=7, BD=8, AD=9. Primero se fusionan A y B. Después la distancia entre ({A,B}) y C dependerá del linkage.

### 8.3 Dendrograma y corte

Un dendrograma representa:

- hojas: observaciones;
- ramas: fusiones;
- altura: disimilitud a la que ocurre cada fusión.

Cortar horizontalmente el árbol produce una partición. Un corte bajo crea más grupos; uno alto, menos. La altura no es necesariamente una probabilidad ni una importancia jurídica.

### 8.4 Single linkage

\[
d_{\text{single}}(A,B)=
\min_{\mathbf{x}\in A,\mathbf{y}\in B} d(\mathbf{x},\mathbf{y}).
\]

Toma el par más cercano. Puede recuperar formas alargadas, pero sufre **chaining**: una cadena de puntos intermedios conecta grupos que intuitivamente parecían separados.

En el ejemplo, distancia entre ({1,2}) y ({8}) es (min(7,6)=6).

### 8.5 Complete linkage

\[
d_{\text{complete}}(A,B)=
\max_{\mathbf{x}\in A,\mathbf{y}\in B} d(\mathbf{x},\mathbf{y}).
\]

Controla el par más lejano y favorece grupos compactos. Puede ser sensible a outliers.

Entre ({1,2}) y ({8}): (max(7,6)=7).

### 8.6 Average linkage

\[
d_{\text{average}}(A,B)=
\frac{1}{|A||B|}
\sum_{\mathbf{x}\in A}\sum_{\mathbf{y}\in B}d(\mathbf{x},\mathbf{y}).
\]

Promedia todas las distancias cruzadas. En el ejemplo: ((7+6)/2=6{,}5). Suele ser un compromiso entre chaining y compactación extrema.

### 8.7 Ward

Ward elige la fusión que produce el menor aumento de suma de cuadrados dentro de clusters:

\[
\Delta(A,B)=
\frac{|A||B|}{|A|+|B|}
\lVert\boldsymbol{\mu}_A-\boldsymbol{\mu}_B\rVert_2^2.
\]

- (|A|), (|B|): tamaños;
- \(\boldsymbol{\mu}_A\), \(\boldsymbol{\mu}_B\): centroides;
- el factor pondera por tamaño;
- la distancia cuadrática mide separación entre medias;
- (Delta): aumento de variación interna al fusionar.

Ward está ligado a geometría euclídea y favorece clusters compactos. No debe combinarse sin pensar con cualquier disimilitud.

### 8.8 Chaining frente a compactación

- single puede preservar conectividad, pero encadenar;
- complete limita diámetros, pero puede fragmentar estructuras alargadas;
- average equilibra pares;
- Ward minimiza aumento de varianza y se aproxima al sesgo de grupos compactos.

No hay linkage ganador fuera de una pregunta.

### 8.9 Costos y límites

El clustering jerárquico puede requerir memoria y tiempo cuadráticos por las distancias entre muchas observaciones. En corpus grandes puede aplicarse a una muestra, prototipos o una etapa reducida. El dendrograma de miles de hojas deja de ser legible aunque el cálculo exista.

### Transferencia a SAIJ

Un dendrograma podría ayudar a explorar subgrupos dentro de una muestra revisable, mostrando a qué nivel se fusionan. El corte debe justificarse por utilidad y estabilidad. Una rama no es una taxonomía jurídica certificada.

### Checkpoint 6

Si single linkage une dos conjuntos mediante pocos documentos puente, ¿la solución demuestra continuidad temática? No. Demuestra conectividad bajo esa representación y umbral; los puentes deben revisarse.

---

## 9. DBSCAN: omisión deliberada por alcance local

DBSCAN suele presentarse porque agrupa por densidad, puede recuperar formas no convexas y marca puntos como ruido. Sin embargo, **no se desarrolla aquí**: el inventario local disponible no lo identifica como contenido verificable y la consigna exige que la cursada sea el alcance primario.

La omisión deja una pregunta abierta: k-means y Ward favorecen compactación, mientras que single linkage puede encadenar. Un método de densidad ofrecería otro sesgo. Si en el futuro aparecen materiales locales de DBSCAN, habrá que estudiar al menos vecindad \(\varepsilon\), `min_samples`, puntos núcleo, frontera, ruido, sensibilidad a escala y dificultad con densidades variables. Este párrafo delimita el hueco; no reemplaza una enseñanza completa.

Para SAIJ, llamar “ruido” a un fallo sería especialmente riesgoso: rareza geométrica no implica irrelevancia ni error. Incluso con DBSCAN, cualquier caso excluido requeriría una política humana.

---

## 10. Evaluar sin una verdad externa directa

### 10.1 Evaluación interna

Usa solo datos y asignaciones:

- inercia;
- silhouette;
- compactación y separación;
- distribución de tamaños;
- distancias a centroides;
- estructura del dendrograma.

Ventaja: no requiere etiquetas. Límite: premia el mismo tipo de geometría que ayudó a definir los grupos. Una alta compactación no demuestra utilidad temática.

### 10.2 Evaluación externa con etiquetas como ayuda de auditoría

A veces existen etiquetas que no se usaron para ajustar clusters. Se pueden comparar para auditar alineación, pero no convertirlas automáticamente en target oculto.

Ejemplo: si hay una etiqueta administrativa de fuero, puede preguntarse cuánto se mezcla en cada cluster. Una fuerte alineación puede indicar señal útil o simplemente que la representación contiene una variable equivalente. Una baja alineación puede significar que los clusters capturan otra dimensión, no que estén “mal”.

Las etiquetas son ayudas de auditoría cuando el objetivo no era reconstruirlas. Si el objetivo real es predecir fuero, el problema es supervisado y debe evaluarse como tal.

### 10.3 Evaluación cualitativa

Consiste en revisar:

- documentos próximos al centro;
- documentos frontera;
- casos muy alejados;
- términos o features distintivas;
- vecinos semánticos;
- diversidad interna;
- coherencia temporal y jurisdiccional;
- explicaciones alternativas.

Debe usarse una muestra diseñada, no solo ejemplos bonitos elegidos después. Conviene incluir casos aleatorios y casos adversariales.

### 10.4 Material complementario integrado 3 — Estabilidad entre semillas, muestras y representaciones

Una estructura creíble no debería desaparecer por un cambio trivial. Se evalúa estabilidad variando:

1. **semillas:** inicializaciones del mismo algoritmo;
2. **muestras:** subconjuntos o bootstrap del corpus;
3. **representaciones:** TF-IDF, embeddings, metadatos o variantes;
4. **hiperparámetros:** K, linkage, dimensionalidad, normalización;
5. **tiempo:** versiones del corpus o periodos.

No se comparan números de cluster directamente porque las etiquetas son arbitrarias: el cluster 0 de una corrida puede corresponder al 3 de otra. Se alinean asignaciones o se usan índices invariantes a permutación, y se inspeccionan miembros compartidos.

La estabilidad tampoco es bondad absoluta. Una partición estable puede reflejar una fuente estable de sesgo, como órgano o plantilla. Una estructura inestable puede revelar transición temática real. La estabilidad responde “¿persiste?”, no “¿es correcta?”.

### 10.5 Material complementario integrado 4 — Evaluación sin ground truth

Cuando no hay verdad de referencia, se construye una **triangulación**:

| Eje | Pregunta |
|---|---|
| Interno | ¿La geometría cumple el criterio elegido? |
| Estabilidad | ¿La solución persiste ante perturbaciones razonables? |
| Cualitativo | ¿Personas revisoras encuentran coherencia y casos límite explicables? |
| Utilidad | ¿Ayuda a navegar, muestrear o recuperar mejor? |
| Riesgo | ¿Introduce exclusiones, estereotipos o confianza indebida? |

Ningún eje reemplaza a los demás. El mejor resultado es una afirmación acotada: “esta configuración produce una estructura suficientemente estable y útil para esta tarea de exploración, con estas limitaciones”.

### 10.6 Diseño mínimo de evaluación SAIJ

Sin ejecutar todavía, un protocolo podría registrar:

1. versión del corpus y unidad documental;
2. dos representaciones justificadas;
3. escalado y métrica;
4. algoritmos e hiperparámetros;
5. semillas y muestras;
6. métricas internas;
7. muestra ciega para revisión cualitativa;
8. criterio de utilidad;
9. riesgos y grupos afectados;
10. decisión de continuar, revisar o descartar.

Esto es un diseño pendiente, no un resultado.

### Error frecuente

Elegir la corrida cuyo gráfico “se ve mejor” después de mirar muchas. Esa selección visual no controlada produce optimismo y oculta intentos fallidos.

### Checkpoint 7

Una solución es estable entre semillas pero cambia por completo entre TF-IDF y embeddings. ¿Qué aprendemos? Que la inicialización no es la principal fuente de incertidumbre; la representación define estructuras diferentes y debe decidirse según el propósito.

---

## 11. Nombrar clusters es interpretación humana

### 11.1 Del patrón al rótulo

El algoritmo devuelve miembros, centroides, distancias o ramas. Una persona observa términos, metadatos y documentos, y propone un nombre. Ese nombre resume una lectura; no emerge como verdad.

Un procedimiento más seguro:

1. inspeccionar varios documentos centrales;
2. inspeccionar casos frontera y aleatorios;
3. comparar features distintivas con el corpus general;
4. anotar contraejemplos;
5. proponer un rótulo descriptivo y provisional;
6. pedir revisión independiente;
7. registrar confianza y límites;
8. permitir “mixto/no interpretable”.

### 11.2 Material complementario integrado 5 — Riesgo de interpretación humana

Los nombres pueden sufrir:

- **sesgo de confirmación:** buscar textos que sostienen la primera intuición;
- **efecto ancla:** conservar un nombre temprano pese a contraejemplos;
- **generalización excesiva:** nombrar por pocos miembros centrales;
- **autoridad falsa:** usar lenguaje jurídico fuerte para una señal léxica;
- **borrado de minorías:** ignorar subgrupos o documentos discordantes;
- **reificación:** tratar una partición contingente como entidad natural.

En SAIJ se prefieren rótulos como “grupo con alta presencia relativa de términos X bajo TF-IDF versión V” frente a “doctrina X”. El primero declara evidencia; el segundo presume una conclusión jurídica.

### 11.3 Acuerdo entre revisores

Dos personas pueden asignar nombres distintos. Ese desacuerdo es información. Conviene registrar:

- instrucciones recibidas;
- muestra vista;
- etiquetas propuestas;
- razones y contraejemplos;
- acuerdo y desacuerdo;
- decisión final o mantenimiento de ambigüedad.

No todo cluster necesita nombre. “No interpretable con evidencia suficiente” es una salida válida.

### Checkpoint 8

¿Por qué mirar solo términos de mayor peso puede engañar? Porque pueden representar fórmulas comunes, nombres propios, artefactos de OCR o rasgos que diferencian el grupo sin resumir todos sus documentos.

---

## 12. Reducción dimensional y PCA como complemento acotado

### 12.1 Qué problema intenta resolver

Una representación puede tener cientos o miles de dimensiones. Reducir dimensión busca un espacio de menor tamaño que conserve alguna estructura. No es sinónimo de visualizar ni de eliminar ruido. Cada método decide qué conservar.

PCA, análisis de componentes principales, busca direcciones ortogonales que capturan máxima varianza lineal. Se incluye aquí como **complemento conceptual acotado** para conectar compresión, clustering y embeddings. No se presenta como evidencia de cobertura específica del inventario local actual.

### 12.2 Centrado

Sea una matriz (X\in\mathbb{R}^{n\times p}):

- (n): observaciones;
- (p): variables;
- cada fila: un objeto;
- cada columna: una variable.

Primero se resta la media de cada columna:

\[
X_c=X-\mathbf{1}\boldsymbol{\mu}^{\top}.
\]

- (X_c): matriz centrada;
- \(\boldsymbol{\mu}\): vector de medias de columnas;
- (mathbf{1}): vector de unos que replica las medias para todas las filas;
- ({}^{\top}): transposición.

Centrar coloca el origen en el promedio. Sin centrado, la primera dirección podría capturar desplazamiento respecto del cero arbitrario.

### 12.3 Covarianza y varianza

Una matriz de covarianza muestral es:

\[
S=\frac{1}{n-1}X_c^{\top}X_c.
\]

- (S_{jj}): varianza de la variable (j);
- (S_{jk}): covarianza entre variables (j) y (k);
- covarianza positiva: tienden a aumentar juntas;
- negativa: una aumenta cuando otra disminuye;
- cercana a cero: poca relación lineal, no independencia garantizada.

PCA encuentra vectores propios (mathbf{v}_r) y valores propios (lambda_r):

\[
S\mathbf{v}_r=\lambda_r\mathbf{v}_r.
\]

- (mathbf{v}_r): dirección del componente (r);
- (lambda_r): varianza capturada en esa dirección;
- los componentes se ordenan de mayor a menor (lambda).

### 12.4 Proyección

El score de una observación centrada (mathbf{x}_{c,i}) sobre el componente (r) es:

\[
z_{ir}=\mathbf{x}_{c,i}^{\top}\mathbf{v}_r.
\]

Es un producto punto: mide cuánto se desplaza el punto en esa dirección.

### 12.5 Ejemplo inventado

Puntos ((1,1),(2,2),(3,3)). La media es ((2,2)). Centrados: ((-1,-1),(0,0),(1,1)). Toda la variación ocurre en la diagonal. El primer componente apunta en dirección proporcional a ((1,1)); el segundo, perpendicular, tiene varianza cero. Reducir de dos dimensiones a una conserva toda la variación de este ejemplo ideal.

Si agregamos ruido fuera de la diagonal, el segundo componente capturará una parte. La reducción perderá esa información.

### 12.6 Varianza explicada

\[
R_m=\frac{\sum_{r=1}^{m}\lambda_r}
{\sum_{r=1}^{p}\lambda_r}.
\]

- (m): componentes retenidos;
- (p): componentes totales posibles;
- numerador: varianza conservada;
- denominador: varianza total;
- (R_m): proporción de varianza explicada.

Un valor alto no garantiza conservación de información jurídicamente relevante. Una señal rara pero importante puede tener poca varianza.

### 12.7 Escalado antes de PCA

PCA es sensible a escala. Si una variable tiene unidades grandes, puede dominar la covarianza. Estandarizar da peso comparable a variables, pero también amplifica variables ruidosas de baja varianza. La elección depende de si la magnitud original tiene sentido.

### 12.8 Reconstrucción y pérdida

Con (m) componentes, una reconstrucción aproximada es:

\[
\hat{X}=Z_mV_m^{\top}+\mathbf{1}\boldsymbol{\mu}^{\top}.
\]

- (Z_m): coordenadas reducidas;
- (V_m): componentes retenidos;
- (hat X): aproximación de la matriz original.

El error de reconstrucción mide información lineal perdida. No recupera matices descartados ni vuelve interpretables los componentes. Los signos de un componente pueden invertirse sin cambiar la solución geométrica.

### 12.9 PCA antes de clustering

Puede reducir ruido y costo, pero también borrar grupos pequeños. El número de componentes debe evaluarse como hiperparámetro dentro del procedimiento, no elegirse mirando toda la colección. Clustering en componentes responde a la geometría comprimida, no a la original.

### 12.10 t-SNE y UMAP: omisión y advertencia de visualización

No se enseñan como contenido local porque el inventario disponible no los identifica. Si se incorporan después, deben tratarse principalmente como herramientas de visualización no lineal con hiperparámetros, aleatoriedad y distorsiones. No basta un mapa con islas para demostrar clusters.

### 12.11 Material complementario integrado 7 — Los mapas no prueban clusters reales

Un gráfico bidimensional comprime una estructura de muchas dimensiones. Puede:

- separar visualmente vecinos por la proyección;
- juntar puntos que estaban lejos;
- exagerar huecos;
- cambiar con semilla o hiperparámetros;
- mostrar densidades que no corresponden al espacio original.

Por eso un mapa sirve para formular preguntas y seleccionar casos, no como evidencia única. Los clusters deben evaluarse en el espacio y propósito pertinentes, con estabilidad y revisión.

### Transferencia a SAIJ

PCA podría ayudar a inspeccionar metadatos numéricos o comprimir una representación antes de otro método. Una proyección de embeddings podría servir como mapa exploratorio. Ninguna autoriza a inferir que dos islas visuales son ramas doctrinales.

### Checkpoint 9

Si los dos primeros componentes explican gran varianza, ¿basta para visualizar “la estructura verdadera”? No. Capturan varianza lineal, no necesariamente la estructura relevante, y el plano omite componentes restantes.

---

## 13. Embeddings: proximidad semántica con límites

### 13.1 Qué aprende un embedding

Un modelo de embeddings se entrena para ubicar entradas en un espacio donde ciertas relaciones útiles se reflejen como proximidad. El criterio depende de datos y objetivo de entrenamiento. Un vector no contiene una definición jurídica explícita por coordenada.

Los embeddings son densos, reutilizables para vecinos, clustering o recuperación, y permiten comparar expresiones sin coincidencia literal. Su poder es también su riesgo: una similitud convincente puede ocultar qué señal utilizó el modelo.

### 13.2 Documento completo, fragmento y agregación

Textos largos suelen exceder la unidad óptima de representación. Opciones:

- embedding del sumario;
- embedding por párrafo o sección;
- ventanas con solapamiento;
- agregación de fragmentos;
- representación separada de hechos, fundamentos y decisión.

Cada opción cambia la pregunta. Un embedding global puede diluir un fundamento breve. Fragmentos muy pequeños pierden contexto. Solapamientos generan casi duplicados en el ranking.

### 13.3 Normalización y búsqueda por coseno

Si índice y consulta se normalizan, el producto punto equivale al coseno:

\[
\hat{\mathbf{q}}\cdot\hat{\mathbf{d}}
=\cos(\mathbf{q},\mathbf{d}).
\]

- (mathbf{q}): embedding de consulta;
- (mathbf{d}): embedding de documento o fragmento;
- sombrero: normalización L2;
- el score ordena candidatos por alineación.

La normalización debe ser coherente. Mezclar embeddings de modelos distintos o dimensiones distintas carece de una geometría compartida garantizada.

### 13.4 Material complementario integrado 6 — Sesgo y desajuste de dominio

**Desajuste de dominio** aparece cuando el modelo aprendió principalmente de textos distintos del uso: idioma, jurisdicción, época, estilo, longitud o vocabulario. Un modelo general puede aproximar “demanda” y “reclamo”, pero fallar en distinciones técnicas, latinismos, citas o negaciones.

**Sesgo** puede surgir de datos de entrenamiento y de la colección SAIJ. El embedding puede asociar grupos sociales con contextos problemáticos, reproducir frecuencia histórica o subrepresentar vocabularios regionales. La proximidad no es neutral.

Auditorías mínimas:

1. consultas para distinciones jurídicas cercanas pero no equivalentes;
2. negación y modalidad;
3. jurisdicciones y periodos;
4. términos asociados a grupos sensibles;
5. textos breves y extensos;
6. errores de OCR;
7. comparación con baseline léxico;
8. revisión humana de vecinos.

No se corrige el sesgo solo normalizando vectores.

### 13.5 Proximidad, equivalencia y pertinencia

- **Proximidad:** score geométrico alto.
- **Equivalencia:** relación fuerte de significado, que requiere criterio.
- **Pertinencia:** utilidad para una consulta concreta.

Un documento puede ser semánticamente parecido pero no pertinente por jurisdicción o fecha. Puede ser pertinente como antecedente contrario aunque el vocabulario difiera. La recuperación debe integrar geometría y filtros.

### Error frecuente

Usar un umbral de coseno tomado de otro modelo y asumir que conserva significado. Las distribuciones de scores dependen del modelo, normalización, dominio y corpus.

### Transferencia a SAIJ

Los embeddings pueden generar candidatos para revisión, navegación o búsqueda semántica. Javier todavía debe decidir unidad, modelo, segmentación, normalización, metadatos obligatorios, conjunto de consultas y evaluación. No se informa que ningún modelo ya funcione bien.

### Checkpoint 10

¿Por qué un baseline TF-IDF sigue siendo necesario si hay embeddings? Porque ofrece trazabilidad léxica, puede rendir muy bien en terminología exacta y revela si la complejidad semántica aporta una mejora real.

---

## 14. TF-IDF frente a embeddings para clustering y recuperación

### 14.1 Comparación conceptual

| Criterio | TF-IDF | Embeddings |
|---|---|---|
| Señal principal | Coincidencia léxica ponderada. | Proximidad aprendida. |
| Dimensión | Alta y dispersa. | Moderada y densa. |
| Interpretabilidad | Términos con pesos inspeccionables. | Coordenadas no interpretables aisladamente. |
| Sinónimos | Limitado sin expansión. | Puede acercarlos. |
| Términos jurídicos exactos | Suele preservarlos bien. | Puede suavizar distinciones. |
| Dominio | Depende del corpus local. | Depende del entrenamiento y adaptación. |
| Costo | Baseline relativamente simple. | Requiere inferencia del modelo e índice denso. |
| Actualización | Vocabulario/IDF cambia con corpus. | Modelo puede mantenerse, pero índice debe recalcular documentos nuevos. |

### 14.2 Para clustering

TF-IDF puede agrupar por vocabulario, fórmulas y entidades. Embeddings pueden agrupar por semántica más abstracta. Ninguno garantiza categorías humanas. Compararlos permite preguntar si la estructura depende de palabras exactas o de señales aprendidas.

Aplicar k-means euclídeo directamente a TF-IDF normalizado necesita interpretación cuidadosa. Como vimos, en vectores unitarios coseno y euclídea se relacionan, pero los centroides de k-means estándar y la geometría esférica no son idénticos a cualquier algoritmo basado en coseno. La representación y el algoritmo deben ser compatibles.

### 14.3 Para recuperación

TF-IDF favorece consultas con términos presentes. Embeddings favorecen paráfrasis. Un sistema híbrido puede combinar scores o listas, pero introduce nuevas decisiones:

- normalización de scores;
- peso léxico frente a semántico;
- desempate;
- filtros;
- evaluación por tipo de consulta.

“Híbrido” no significa automáticamente superior. Debe medirse.

### 14.4 Ejemplo inventado

Consulta: “dejar sin efecto una resolución”.

- Documento A repite exactamente esas palabras.
- Documento B usa “revocar el pronunciamiento”.
- Documento C menciona “efectos de la resolución” pero no revocación.

TF-IDF puede priorizar A y quizá C por términos compartidos. Un embedding podría acercar B. Pero también podría confundir C por similitud general. La evaluación necesita juicios de pertinencia, no intuición sobre tecnología.

### Transferencia a SAIJ

Una comparación responsable separaría consultas de citas exactas, conceptos, hechos, procedimiento y lenguaje coloquial. Así se descubre dónde cada representación ayuda o falla. No se elige por un promedio único si los usos tienen riesgos distintos.

---

## 15. Usos SAIJ posibles, con límites explícitos

### 15.1 Exploración temática

Objetivo: proponer subconjuntos para inspección. Salida: clusters, vecinos o componentes. Validación: estabilidad, muestra cualitativa y utilidad para navegar.

Límite: un tema propuesto no es una categoría oficial. Puede reflejar plantillas, época u órgano.

### 15.2 Duplicados y casi duplicados

Objetivo: detectar textos idénticos o muy parecidos. Exactos y casi duplicados son problemas distintos. Un hash puede resolver copias exactas; TF-IDF o embeddings pueden proponer paráfrasis y versiones.

Límite: dos publicaciones similares pueden ser versiones legítimas, citas o resoluciones relacionadas. La acción de eliminar exige reglas y revisión.

### 15.3 Anomalías

Objetivo: priorizar casos raros por metadatos, longitud, vocabulario o distancia. Una anomalía es una observación inusual bajo un modelo de referencia.

Límite: raro no significa incorrecto. Un fallo excepcional puede ser jurídicamente central. La salida debe ser una cola de revisión, no borrado automático.

### 15.4 Muestreo para revisión

Objetivo: construir una muestra diversa: centrales, fronterizos, lejanos y de clusters pequeños. Esto puede revelar errores que un muestreo puramente aleatorio no muestra.

Límite: una muestra guiada por el modelo hereda sus puntos ciegos. Debe combinarse con selección aleatoria y criterios de cobertura.

### 15.5 Navegación del corpus

Objetivo: ofrecer documentos vecinos, ramas jerárquicas o rutas entre temas. Puede ayudar a descubrir antecedentes y variaciones.

Límite: la interfaz debe mostrar por qué se sugiere cada vínculo y permitir filtros. Un grafo atractivo no prueba una relación jurídica.

### 15.6 Candidatos semánticos

Objetivo: recuperar un conjunto inicial ante una consulta. Se habla de “candidatos” porque el ranking no decide pertinencia final.

Límite: deben evaluarse omisiones, falsos positivos, dominio, temporalidad y jurisdicción.

### 15.7 Frontera central

> El clustering no descubre automáticamente categorías legales verdaderas.

Produce particiones relativas a datos, representación, métrica y método. Puede apoyar exploración y revisión humana. No reemplaza taxonomías normativas, criterio profesional ni validación empírica.

---

## 16. Del vecino semántico a la búsqueda

### 16.1 Consulta y documentos en un espacio común

Una búsqueda densa representa consulta y documentos:

\[
\mathbf{q}=f(\text{consulta}),
\qquad
\mathbf{d}_i=f(\text{documento}_i).
\]

Luego calcula un score, por ejemplo coseno:

\[
s_i=\cos(\mathbf{q},\mathbf{d}_i).
\]

Ordena índices (i) de mayor a menor (s_i). El resultado es un ranking, no una respuesta jurídica.

### 16.2 Ranking y top-k

Si se devuelven los primeros (k) candidatos, elegir (k) expresa un compromiso:

- (k) pequeño: menos revisión, más riesgo de omitir;
- (k) grande: mayor cobertura potencial, más carga y ruido.

No se fija por costumbre. Depende de la tarea y de cuánto cuesta revisar o perder un documento relevante.

### 16.3 Filtros de metadatos

Una consulta semántica puede restringirse por:

- jurisdicción;
- órgano;
- periodo;
- tipo documental;
- estado de calidad;
- idioma;
- disponibilidad de texto.

El orden importa. Filtrar antes reduce candidatos; filtrar después puede desperdiciar resultados. Un filtro incorrecto puede eliminar el único documento pertinente aunque el embedding sea excelente.

### 16.4 Evaluación de recuperación

Se necesita un conjunto de consultas con juicios de pertinencia. Métricas básicas:

\[
\operatorname{Precision@k}=
\frac{\#\text{ relevantes entre los primeros }k}{k}.
\]

\[
\operatorname{Recall@k}=
\frac{\#\text{ relevantes recuperados entre los primeros }k}
{\#\text{ relevantes conocidos para la consulta}}.
\]

- Precision@k pregunta qué fracción de lo mostrado es útil;
- Recall@k pregunta qué fracción de lo que debía aparecer fue recuperada;
- “relevante conocido” depende de un proceso de juicio que puede ser incompleto.

Para la posición del primer resultado pertinente:

\[
\operatorname{RR}(q)=\frac{1}{\operatorname{rank}_q},
\qquad
\operatorname{MRR}=\frac{1}{Q}\sum_{q=1}^{Q}\operatorname{RR}(q).
\]

- (operatorname{rank}_q): posición del primer relevante para consulta (q);
- (Q): cantidad de consultas;
- MRR: promedio recíproco.

**Ejemplo inventado.** Para una consulta hay dos relevantes conocidos. El ranking de cinco candidatos tiene relevantes en posiciones 2 y 5. Entonces Precision@3 (=1/3), Recall@3 (=1/2), RR (=1/2). Estos números enseñan la fórmula; no son resultados SAIJ.

### 16.5 Juicios y tipos de consulta

Una evaluación debe cubrir:

- término exacto;
- paráfrasis;
- hechos;
- figura jurídica;
- órgano o periodo;
- consulta ambigua;
- negación;
- caso sin respuesta en corpus.

Conviene tener más de una persona revisora en una muestra, registrar desacuerdos y distinguir relevancia fuerte, parcial y no relevante si el protocolo lo permite.

### 16.6 Material complementario integrado 8 — Evaluar recuperación antes de agregar un generador

Una arquitectura RAG incorpora una etapa generativa después de recuperar evidencia. Si la recuperación omite documentos pertinentes, el generador no puede citarlos. Puede redactar con fluidez sobre evidencia insuficiente.

Antes de agregar generación hay que demostrar, para usos definidos:

1. que las consultas tienen candidatos relevantes;
2. que Recall@k y Precision@k son aceptables según criterios establecidos;
3. que filtros no excluyen evidencia;
4. que fallos por dominio, tiempo y jurisdicción están caracterizados;
5. que existe una política para “sin evidencia suficiente”;
6. que el ranking es reproducible y auditable.

Esta materia se detiene ahí. No diseña prompts, memoria conversacional, generación, citación automática ni guardrails completos de RAG. El próximo proyecto integrador retomará la frontera.

### Error frecuente

Evaluar la respuesta generada sin evaluar por separado qué recuperó el sistema. Una respuesta plausible puede ocultar recuperación deficiente.

### Transferencia a SAIJ

El primer experimento no debería ser “hacer un chatbot”. Debería ser construir y auditar una recuperación: corpus versionado, consultas, juicios, baseline TF-IDF, candidato denso, filtros y análisis de errores.

### Checkpoint 11

Si un generador produce una respuesta correcta pese a no recuperar el antecedente pertinente, ¿el RAG está validado? No. Puede haber respondido por conocimiento previo o casualidad; la cadena de evidencia falló.

---

## 17. Flujo de trabajo decisión-primero

### 17.1 Pregunta y unidad

1. definir el uso: explorar, comprimir, segmentar, detectar o recuperar;
2. definir población y versión;
3. definir unidad: fallo, sumario, fragmento, caso o metadato;
4. declarar qué decisiones no puede tomar el sistema.

### 17.2 Representación y geometría

5. construir baseline interpretable;
6. justificar limpieza y tokenización;
7. decidir escalado o normalización;
8. elegir métrica compatible;
9. agregar embedding solo con pregunta de valor.

### 17.3 Método y perturbaciones

10. elegir método por supuestos;
11. registrar hiperparámetros;
12. repetir semillas;
13. variar muestras;
14. comparar representaciones;
15. mantener un conjunto de evaluación separado cuando corresponda.

### 17.4 Interpretación y decisión

16. revisar centrales, fronteras, aleatorios y anomalías;
17. nombrar provisionalmente o declarar no interpretable;
18. medir utilidad;
19. auditar sesgo y cobertura;
20. documentar límites y decisión siguiente.

### 17.5 Registro mínimo

| Campo | Pregunta que responde |
|---|---|
| Propósito | ¿Para qué existe este experimento? |
| Corpus | ¿Qué versión y población se usó? |
| Unidad | ¿Qué representa cada vector? |
| Representación | ¿Qué información puede ver? |
| Geometría | ¿Cómo define cercanía? |
| Algoritmo | ¿Qué estructura favorece? |
| Perturbaciones | ¿Qué se varió para medir estabilidad? |
| Evaluación | ¿Qué evidencia interna, externa, cualitativa y de utilidad existe? |
| Riesgos | ¿Qué daño o interpretación indebida puede ocurrir? |
| Estado | ¿Exploratorio, candidato, descartado o pendiente? |

---

## 18. Errores frecuentes y cómo corregir el razonamiento

### 18.1 “No hay target, entonces no hay evaluación”

Corrección: no hay una respuesta externa directa, pero sí evaluación interna, estabilidad, revisión cualitativa, utilidad y riesgo.

### 18.2 “El gráfico muestra tres islas; hay tres clusters”

Corrección: una proyección puede crear o exagerar separaciones. Evaluar en el espacio original y con perturbaciones.

### 18.3 “K=10 porque queremos diez temas”

Corrección: el número deseado por interfaz no garantiza diez grupos geométricos coherentes. Separar resolución de navegación de evidencia temática.

### 18.4 “El cluster se llama daños, por lo tanto todos sus documentos son de daños”

Corrección: el nombre es una síntesis humana. Revisar contraejemplos y usar un rótulo descriptivo.

### 18.5 “El outlier está mal”

Corrección: distancia es un criterio de prioridad. La revisión decide si hay error, novedad o caso legítimo.

### 18.6 “Embeddings reemplazan TF-IDF”

Corrección: representan señales distintas. Mantener baseline y evaluar por tipos de consulta.

### 18.7 “Más dimensiones conservan más información y siempre ayudan”

Corrección: también incorporan ruido, costo y dispersión. Medir estabilidad y utilidad.

### 18.8 “PCA conserva 90 %; no perdimos nada importante”

Corrección: conserva 90 % de varianza, no 90 % de significado jurídico.

### 18.9 “Silhouette alto valida el contenido”

Corrección: valida una propiedad geométrica bajo una configuración.

### 18.10 “La misma semilla basta para reproducibilidad”

Corrección: también hay versiones de corpus, orden, implementación, modelo de embeddings y parámetros.

### 18.11 “Un coseno alto es una probabilidad de relevancia”

Corrección: es un score de similitud, no calibrado como probabilidad salvo procedimiento explícito.

### 18.12 “Primero hacemos RAG y después medimos retrieval”

Corrección: se evalúa recuperación primero para localizar fallas y evitar que la fluidez tape evidencia ausente.

---

## 19. Checkpoint integrador antes de los ejercicios

Podés avanzar si explicás, sin código:

1. qué cambia al retirar el target;
2. por qué representación y métrica definen la estructura posible;
3. diferencia entre estandarización y normalización;
4. cálculo manual de euclídea, Manhattan y coseno;
5. por qué alta dimensión debilita intuiciones de vecinos;
6. ciclo asignación–actualización de k-means;
7. qué minimiza la inercia;
8. por qué K no sale de una sola métrica;
9. qué mide silhouette y qué no;
10. cómo difieren single, complete, average y Ward;
11. por qué un dendrograma no es taxonomía;
12. cómo triangular evaluación sin ground truth;
13. qué significa estabilidad;
14. por qué nombrar es interpretar;
15. qué conserva PCA;
16. límites de mapas bidimensionales;
17. diferencia entre TF-IDF y embeddings;
18. sesgo y desajuste de dominio;
19. diferencia entre cercanía y relevancia;
20. por qué retrieval debe evaluarse antes de RAG.

---

## 20. Ejercicios conceptuales — resolver antes de implementar

Los siguientes ejercicios son conceptuales. Todos usan datos inventados o situaciones hipotéticas. No requieren biblioteca, notebook ni corpus real.

### Ejercicio 1 — Objetivos distintos

Un equipo agrupa fallos para explorar temas y luego usa los grupos para asignar automáticamente especialidades a personas. ¿Qué cambio de objetivo ocurrió y qué nueva evaluación hace falta?

### Ejercicio 2 — Representación

Dos documentos comparten órgano, año y longitud, pero tratan asuntos distintos. ¿Por qué una representación solo de metadatos puede juntarlos y qué concluye realmente ese cluster?

### Ejercicio 3 — TF-IDF

En un corpus inventado de 10 documentos, un término aparece tres veces en A y está presente en 5 documentos. Usando frecuencia bruta e IDF (log(N/df)), escribí el peso y explicalo.

### Ejercicio 4 — Escalado

Una tabla tiene edad del expediente en años y longitud en caracteres. ¿Qué puede pasar con k-means sin escalado? ¿Estandarizar resuelve todo?

### Ejercicio 5 — Normalización

Normalizá mentalmente ((0,3,4)) con norma L2 y explicá qué información se pierde.

### Ejercicio 6 — Euclídea y Manhattan

Calculá ambas distancias entre ((2,1)) y ((5,5)). ¿Por qué dan números distintos sin que una esté equivocada?

### Ejercicio 7 — Coseno

Los vectores ((1,1)) y ((10,10)) tienen misma dirección. ¿Qué coseno tienen y qué diferencia ignora?

### Ejercicio 8 — Normalización y ranking

¿Por qué mayor coseno equivale a menor euclídea para vectores normalizados? ¿Cuándo deja de valer esa equivalencia?

### Ejercicio 9 — Alta dimensión

Agregar miles de términos raros a TF-IDF hace que todos los documentos tengan más información. ¿Por qué eso no garantiza mejores vecinos?

### Ejercicio 10 — Centroides

Para el grupo con puntos ((1,2),(3,4),(5,0)), calculá el centroide. ¿Debe existir un documento en esa posición?

### Ejercicio 11 — Inercia y K

¿Por qué la inercia siempre mejora al aumentar K? ¿Por qué no elegir (K=n)?

### Ejercicio 12 — Inicialización

Dos corridas de k-means con igual K producen asignaciones diferentes. Enumerá tres explicaciones y un protocolo de comparación.

### Ejercicio 13 — Formas

Hay dos anillos concéntricos. ¿Por qué k-means puede ser inadecuado aunque se le indique K=2?

### Ejercicio 14 — Silhouette

Para un punto (a=3), (b=4). Calculá (s). ¿Qué autoriza a decir y qué no?

### Ejercicio 15 — Promedios engañosos

Una solución tiene silhouette medio alto, pero un cluster pequeño contiene muchos valores negativos. ¿Qué deberías hacer?

### Ejercicio 16 — Linkage

Los puntos forman dos nubes unidas por una cadena dispersa. ¿Qué comportamiento esperarías de single y complete linkage?

### Ejercicio 17 — Dendrograma

Dos analistas cortan el mismo dendrograma a alturas distintas. ¿Cuál tiene razón?

### Ejercicio 18 — Ward

¿Por qué Ward se asocia con distancia euclídea y clusters compactos? ¿Qué error sería usarlo como si aceptara cualquier disimilitud sin consecuencias?

### Ejercicio 19 — Evaluación externa

Los clusters se alinean casi perfectamente con la etiqueta de órgano. ¿Es éxito? Proponé dos interpretaciones opuestas.

### Ejercicio 20 — Estabilidad

Una partición es estable entre semillas, inestable entre muestras y estable en silhouette promedio. ¿Qué riesgo muestra?

### Ejercicio 21 — Nombres

Tres documentos centrales sugieren “consumo”, pero casos aleatorios del cluster incluyen temas diversos. ¿Cómo debería rotularse y qué revisión falta?

### Ejercicio 22 — PCA

PCA retiene componentes que explican 95 % de varianza. ¿Podés afirmar que conserva 95 % de información jurídica? Justificá.

### Ejercicio 23 — Visualización

Una proyección bidimensional de embeddings muestra cuatro islas. Diseñá una verificación mínima antes de hablar de cuatro clusters.

### Ejercicio 24 — Embedding y dominio

Un modelo general recupera textos de otros países frente a una consulta local. ¿Qué tipos de desajuste pueden actuar y qué comparación harías?

### Ejercicio 25 — TF-IDF frente a embeddings

Para una consulta con número exacto de ley y otra con paráfrasis conceptual, ¿qué comportamiento esperarías de cada representación? ¿Cómo lo comprobarías?

### Ejercicio 26 — Anomalías

Un documento queda lejos de todos los centroides. Enumerá al menos cuatro explicaciones distintas y la acción segura.

### Ejercicio 27 — Recuperación

En top 5 hay tres relevantes; se conocen seis relevantes para la consulta. Calculá Precision@5 y Recall@5. ¿Qué no dicen esas métricas?

### Ejercicio 28 — Antes de RAG

Un prototipo genera respuestas fluidas, pero no existe conjunto de consultas juzgadas. ¿Qué debe hacerse antes de evaluar la generación como sistema jurídico asistido?

---

## 21. Respuestas razonadas

### Respuesta 1

El objetivo pasó de descubrimiento exploratorio a segmentación operativa con consecuencias sobre personas. Ya no basta coherencia geométrica. Hay que evaluar si los grupos son útiles para distribuir tareas, si excluyen o sobrecargan perfiles, si las categorías tienen legitimidad y si existe revisión humana. También debe medirse estabilidad y daño ante asignaciones erróneas. El mismo cluster puede ser aceptable como mapa y peligroso como regla automática.

### Respuesta 2

El algoritmo solo ve similitud en órgano, año y longitud; no ve el asunto. Por eso puede juntarlos correctamente respecto de esa representación. La conclusión válida es “comparten perfil de metadatos”, no “comparten tema”. Para explorar contenido habría que agregar una representación textual y decidir cómo combinarla sin permitir que un bloque domine arbitrariamente.

### Respuesta 3

El peso es:

\[
3\times\log(10/5)=3\log2.
\]

El factor 3 expresa presencia local en A; (log2) expresa que el término aparece en la mitad del corpus y por eso conserva poder de contraste. No podemos comparar el valor con otra implementación sin conocer normalización, base del logaritmo y suavizado.

### Respuesta 4

La longitud puede dominar porque sus diferencias numéricas son mucho mayores. k-means podría formar grupos principalmente por tamaño. Estandarizar vuelve comparables los desvíos, pero no prueba que ambas variables deban tener igual peso ni que longitud sea relevante. También hay que tratar outliers y significado.

### Respuesta 5

La norma es (sqrt{0^2+3^2+4^2}=5). El vector normalizado es ((0,0{,}6,0{,}8)). Conserva dirección y pierde magnitud: ((0,6,8)) quedaría igual. Eso puede ser deseable para comparar proporciones, pero no si la magnitud total importa.

### Respuesta 6

Diferencias: (3) y (4). Euclídea: (sqrt{3^2+4^2}=5). Manhattan: (3+4=7). La primera mide línea recta; la segunda suma desplazamientos por ejes. Formalizan costos geométricos distintos. Elegir depende del problema, escala y robustez deseada.

### Respuesta 7

El coseno es (1) porque los vectores están perfectamente alineados. Ignora que el segundo tiene magnitud diez veces mayor. En texto normalizado eso puede abstraer longitud; en otro problema puede borrar intensidad importante.

### Respuesta 8

Para normas uno, la distancia cuadrática es (2-2cos). Por tanto una transformación monótona vincula ambos rankings. Deja de valer si no se normalizan igual, si aparecen vectores cero, si se usan otras normas o si el procedimiento modifica centroides y no solo compara pares fijos.

### Respuesta 9

Los términos pueden ser errores, nombres únicos o ruido. En alta dimensión los puntos se dispersan y distancias pueden concentrarse. Más columnas aumentan capacidad de distinguir, pero también coincidencias accidentales y varianza. Se necesitan filtros, normalización, evaluación de vecinos y estabilidad.

### Respuesta 10

La media por coordenada es:

\[
((1+3+5)/3,(2+4+0)/3)=(3,2).
\]

No tiene que existir un documento en ((3,2)). Es un prototipo promedio. En representaciones textuales, sus pesos ayudan a describir el centro, pero no constituyen un texto real.

### Respuesta 11

Al agregar centroides, cada punto puede conservar su centro anterior o elegir uno más cercano; el mínimo no empeora. Con (K=n), cada punto es un cluster y la inercia puede ser cero, pero no hay compresión, generalización ni utilidad interpretativa. K se decide con múltiples criterios.

### Respuesta 12

Pueden cambiar inicialización, empate numérico, orden o implementación; también preprocesamiento si no fue fijado. El protocolo registra semillas y versiones, ejecuta varias corridas, alinea clusters ignorando números arbitrarios, compara miembros y métricas, revisa casos inestables y reporta distribución, no solo la mejor corrida.

### Respuesta 13

Los anillos son no convexos y comparten centro. k-means divide por proximidad a centroides en regiones convexas; puede cortar cada anillo en sectores. Conocer K no corrige el sesgo de forma. Haría falta otro criterio, cuya inclusión debe estar respaldada y evaluada.

### Respuesta 14

\[
s=(4-3)/4=0{,}25.
\]

El punto está algo más cohesionado con su grupo que con el alternativo, pero no fuertemente separado. No autoriza a llamar correcto al cluster ni a inferir significado jurídico. Hay que mirar distribución y contenido.

### Respuesta 15

No esconder el cluster pequeño en el promedio. Revisar su distribución, tamaños, asignaciones, casos negativos y posible representación incorrecta. Comparar otras semillas y configuraciones. Si el grupo contiene casos raros relevantes, un bajo silhouette puede ser información, no un motivo automático de eliminación.

### Respuesta 16

Single puede encadenar las dos nubes porque toma el par más cercano entre grupos; la cadena ofrece puentes sucesivos. Complete mira el par más lejano y tenderá a mantener grupos más compactos, aunque puede fragmentar la cadena. Ninguno prueba cuál estructura es “real”.

### Respuesta 17

Ambos cortes son particiones válidas del árbol. La elección depende de resolución, saltos de distancia, estabilidad y uso. Si uno necesita una taxonomía de cuatro niveles y otro una muestra de diez grupos, pueden elegir distinto. Deben justificar, no declarar una altura natural sin evidencia.

### Respuesta 18

Ward minimiza aumento de suma de cuadrados alrededor de centroides, una cantidad euclídea. Usar una disimilitud incompatible rompe esa interpretación y puede volver incorrecta la actualización. La herramienta podría aceptar o rechazar combinaciones, pero el criterio matemático sigue limitando el significado.

### Respuesta 19

Interpretación favorable: la representación recupera una estructura administrativa útil para navegación. Interpretación crítica: incluyó directamente órgano o señales de plantilla, por lo que la alineación es trivial y no informa contenido. Hay que revisar propósito, features y si se buscaba tema o perfil institucional.

### Respuesta 20

La inicialización no preocupa mucho, pero la selección de documentos sí: pequeños cambios de muestra alteran membresías. Un silhouette promedio estable puede ocultar identidades cambiantes. Hay que localizar casos volátiles, repetir muestreos y limitar afirmaciones de generalización.

### Respuesta 21

No debería llamarse simplemente “consumo”. Podría rotularse provisionalmente “cluster con términos centrales asociados a consumo, de coherencia interna pendiente”. Falta una muestra sistemática de miembros centrales, frontera y aleatorios, contraejemplos, revisión independiente y quizá subdivisión o declaración de grupo mixto.

### Respuesta 22

No. PCA conserva 95 % de varianza según variables y escalado. Una distinción jurídica rara puede explicar poca varianza y perderse. Hay que medir reconstrucción, desempeño en la tarea, estabilidad y revisión de señales relevantes. Varianza es una propiedad estadística, no un porcentaje de significado.

### Respuesta 23

Repetir proyección con semillas e hiperparámetros, comparar con distancias y vecinos del espacio original, ejecutar clustering independiente del mapa, medir estabilidad en muestras, revisar puntos centrales y puentes, y comprobar si las islas corresponden a metadatos triviales. El gráfico solo inicia la investigación.

### Respuesta 24

Puede haber desajuste de jurisdicción, idioma regional, época, vocabulario técnico o distribución del corpus. También filtros insuficientes. Compararía con TF-IDF, aplicaría metadatos, diseñaría consultas locales, revisaría vecinos y consideraría un modelo validado para el dominio. No asumiría que cambiar el umbral resuelve todo.

### Respuesta 25

TF-IDF debería ser fuerte para el número exacto si está indexado; embeddings pueden diluirlo. Para paráfrasis, embeddings podrían recuperar formulaciones distintas; TF-IDF puede fallar sin términos compartidos. Se comprueba con consultas juzgadas por tipo, métricas top-k y análisis de errores, sin proclamar ganador por ejemplos elegidos.

### Respuesta 26

Puede ser error de extracción, idioma distinto, documento excepcional válido, mezcla temática, longitud extrema, metadatos raros o falla de representación. La acción segura es priorizar revisión con contexto y registrar causa. No borrar, excluir ni etiquetar automáticamente como incorrecto.

### Respuesta 27

Precision@5 (=3/5=0{,}6). Recall@5 (=3/6=0{,}5). No indican relevancia de posiciones individuales, gravedad de omisiones, acuerdo entre jueces, calidad fuera de top 5 ni utilidad por tipo de consulta. Tampoco son resultados SAIJ porque el escenario es inventado.

### Respuesta 28

Primero se define el uso y se construye un conjunto de consultas con juicios. Se evalúan baseline léxico, recuperación densa, filtros, Precision@k, Recall@k, casos sin respuesta, sesgos y errores. Solo después se incorpora un generador y se evalúa por separado fidelidad a evidencia, citación y abstención. La fluidez no sustituye retrieval.

---

## 22. Hoja de transferencia SAIJ — decisiones pendientes de Javier

Esta hoja no contiene resultados. Debe completarse con evidencia reproducida.

### 22.1 Propósito

- Uso primario: exploración / duplicados / anomalías / muestreo / navegación / retrieval.
- Persona usuaria y situación: ________
- Decisión que el sistema no puede tomar: ________
- Costo de omitir un documento relevante: ________
- Costo de mostrar un falso candidato: ________

### 22.2 Corpus y unidad

- Versión del corpus: ________
- Población incluida: ________
- Exclusiones: ________
- Unidad representada: fallo / sumario / fragmento / otra.
- Estrategia para textos largos: ________
- Tratamiento de duplicados: ________

### 22.3 Representaciones

- Baseline TF-IDF: ________
- Metadatos y justificación: ________
- Embedding candidato y versión: ________
- Escalado por columna: ________
- Normalización por fila: ________
- Métrica: ________

### 22.4 Clustering

- Pregunta exploratoria: ________
- k-means: valores de K y semillas a comparar: ________
- Jerárquico: muestra, linkage y corte: ________
- Métricas internas: ________
- Perturbaciones de estabilidad: ________
- Protocolo de nombres: ________
- Criterio para declarar “no interpretable”: ________

### 22.5 Recuperación

- Tipos de consultas: ________
- Protocolo de juicio: ________
- Baseline léxico: ________
- Candidato semántico: ________
- Filtros obligatorios: ________
- Valores de (k): ________
- Métricas: ________
- Umbral de aceptación: **pendiente de evidencia**, no inventar.

### 22.6 Riesgo y revisión

- Sesgos a auditar: ________
- Subgrupos o periodos críticos: ________
- Política de anomalías: ________
- Política “sin evidencia suficiente”: ________
- Responsable de revisión: ________
- Frecuencia de reevaluación: ________

---

## 23. Frontera de implementación: el código viene después

Materia 5 termina su recorrido principal sin código. La implementación futura deberá materializar decisiones ya justificadas:

1. cargar un corpus versionado;
2. validar unidad y esquema;
3. separar ajuste y evaluación;
4. ajustar representación solo donde corresponde;
5. normalizar de manera coherente;
6. ejecutar configuraciones predefinidas;
7. registrar semillas y versiones;
8. calcular métricas sin elegir solo el mejor decimal;
9. producir muestras para revisión;
10. comparar estabilidad;
11. evaluar retrieval antes de generación;
12. documentar límites.

El código de bibliotecas, los notebooks de implementación y la arquitectura completa de RAG quedan fuera del camino conceptual principal. Una celda futura debería poder responder: “¿qué decisión implementa, qué evidencia produce y qué riesgo deja abierto?”.

---

## 24. Autoevaluación final de Materia 5

Marcá solo lo que puedas explicar con un ejemplo propio y una limitación:

- [ ] Distingo ausencia de target de ausencia de objetivo.
- [ ] Separo descubrimiento, compresión, segmentación, anomalía y retrieval.
- [ ] Explico por qué la representación precede al algoritmo.
- [ ] Comparo metadatos, TF-IDF y embeddings.
- [ ] Calculo TF-IDF en un ejemplo simplificado.
- [ ] Distingo escalado de columnas y normalización de filas.
- [ ] Calculo euclídea, Manhattan y coseno.
- [ ] Derivo la relación coseno–euclídea con norma uno.
- [ ] Explico la maldición de dimensionalidad sin decir que “muchas dimensiones son siempre malas”.
- [ ] Defino cluster de manera relativa a un criterio.
- [ ] Reconstruyo el ciclo de k-means.
- [ ] Explico centroide, asignación e inercia símbolo por símbolo.
- [ ] Reconozco inicialización y óptimos locales.
- [ ] Elijo K con evidencia múltiple.
- [ ] Enumero límites de forma, tamaño, densidad, escala y outliers.
- [ ] Calculo e interpreto silhouette con cautela.
- [ ] Explico dendrograma y corte.
- [ ] Comparo single, complete, average y Ward.
- [ ] Entiendo chaining y compactación.
- [ ] Puedo explicar por qué DBSCAN se omitió del desarrollo.
- [ ] Triangulo evaluación interna, externa, cualitativa, estabilidad y utilidad.
- [ ] No confundo etiqueta de auditoría con target oculto.
- [ ] Trato nombres de clusters como interpretaciones provisionales.
- [ ] Explico centrado, covarianza, componentes y varianza explicada en PCA.
- [ ] Reconozco límites de reconstrucción y escalado.
- [ ] No uso un mapa bidimensional como prueba de clusters.
- [ ] Explico embeddings, normalización y coseno.
- [ ] Audito desajuste de dominio y sesgo.
- [ ] Comparo TF-IDF y embeddings por tipo de consulta.
- [ ] Distingo proximidad, equivalencia y pertinencia.
- [ ] Diseño usos SAIJ sin inventar categorías ni resultados.
- [ ] Calculo Precision@k, Recall@k y MRR en ejemplos pequeños.
- [ ] Evalúo retrieval antes de agregar un generador.
- [ ] Puedo declarar “no sabemos” o “no interpretable”.

### Criterio de dominio

Considerá dominada la materia cuando puedas recibir un gráfico de clusters o un demo de búsqueda y preguntar antes de entusiasmarte:

1. ¿qué representa cada punto?;
2. ¿qué información quedó fuera?;
3. ¿cómo se escaló y normalizó?;
4. ¿qué métrica define cercanía?;
5. ¿qué estructura favorece el método?;
6. ¿qué cambia con semillas, muestras y representaciones?;
7. ¿cómo se evaluó sin ground truth?;
8. ¿quién nombró los grupos y con qué muestra?;
9. ¿qué casos contradicen el rótulo?;
10. ¿qué sesgo o desajuste de dominio existe?;
11. ¿qué utilidad concreta se midió?;
12. ¿qué consultas y juicios sostienen retrieval?;
13. ¿qué filtros pueden excluir evidencia?;
14. ¿qué todavía no sabemos?;
15. ¿qué hallazgo fue reproducido personalmente por Javier?

---

## 25. Glosario de Materia 5

| Término | Definición operativa |
|---|---|
| **Aprendizaje no supervisado** | Construcción de estructura o representación sin target externo por observación. |
| **Asignación** | Paso que vincula cada observación con un cluster. |
| **Average linkage** | Distancia promedio entre todos los pares cruzados de dos clusters. |
| **Centroide** | Vector medio de un cluster; no necesariamente una observación real. |
| **Chaining** | Unión de grupos mediante cadenas de vecinos, frecuente en single linkage. |
| **Cluster** | Conjunto cohesionado o separado según representación, métrica y método. |
| **Clustering aglomerativo** | Método jerárquico que comienza con individuos y fusiona grupos. |
| **Complete linkage** | Distancia definida por el par cruzado más lejano. |
| **Componente principal** | Dirección ortogonal que captura varianza lineal en PCA. |
| **Compresión** | Reducción de representación conservando información según un criterio. |
| **Coseno** | Similitud angular entre vectores no nulos. |
| **Covarianza** | Medida de variación lineal conjunta entre variables. |
| **Dendrograma** | Árbol que registra fusiones y alturas en clustering jerárquico. |
| **Desajuste de dominio** | Diferencia entre datos de entrenamiento del modelo y uso real. |
| **Distancia euclídea** | Raíz de la suma de diferencias cuadradas. |
| **Distancia Manhattan** | Suma de diferencias absolutas por dimensión. |
| **Embedding** | Representación densa aprendida en un espacio vectorial. |
| **Escalado** | Transformación de variables para controlar sus unidades o dispersión. |
| **Estabilidad** | Persistencia de una estructura ante perturbaciones razonables. |
| **Ground truth** | Referencia externa considerada verdadera para evaluar, con sus límites. |
| **Inercia** | Suma de distancias cuadráticas de puntos a centroides en k-means. |
| **k-means** | Método que alterna asignación a centroides y actualización por medias. |
| **Linkage** | Regla que define distancia entre clusters jerárquicos. |
| **Maldición de dimensionalidad** | Fenómenos de dispersión y demanda de datos al crecer dimensiones. |
| **MRR** | Media del recíproco de la posición del primer resultado relevante. |
| **Normalización L2** | División de un vector por su norma euclídea. |
| **Óptimo local** | Solución mejor en su entorno pero no necesariamente global. |
| **Outlier** | Observación alejada bajo un criterio; no sinónimo de error. |
| **PCA** | Proyección lineal sobre direcciones de máxima varianza. |
| **Precision@k** | Fracción de relevantes entre los primeros k resultados. |
| **Proyección** | Representación de puntos en un espacio de menor dimensión. |
| **Recall@k** | Fracción de relevantes conocidos recuperados entre los primeros k. |
| **Recuperación** | Ordenamiento de candidatos pertinentes para una consulta. |
| **Representación** | Conversión de un objeto en variables que un método puede procesar. |
| **Silhouette** | Índice de cohesión propia frente al cluster alternativo más cercano. |
| **Single linkage** | Distancia definida por el par cruzado más próximo. |
| **TF-IDF** | Peso léxico que combina frecuencia local y rareza en el corpus. |
| **Varianza explicada** | Proporción de varianza total capturada por componentes retenidos. |
| **Ward** | Enlace que minimiza el aumento de variación interna al fusionar grupos. |

---

