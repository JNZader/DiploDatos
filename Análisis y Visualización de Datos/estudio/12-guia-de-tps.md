# Guía de Trabajos Prácticos — Sysarmy 2026

## Concepto general de los TPs

Los dos trabajos prácticos son un **recorrido de ida y vuelta** entre la pregunta de negocio y la evidencia numérica.

- **TP1** te obliga a **explorar** sin saber bien qué vas a encontrar. Es como entrar a un depósito oscuro con una linterna: primero iluminás zonas amplias (EDA), después te enfocás en rincones específicos (relaciones multivariadas).
- **TP2** te obliga a **argumentar** con rigor. Ya sabés qué querés probar; ahora tenés que cuantificar la incertidumbre, controlar el error y comunicar el resultado sin exagerar.

> **Regla de oro de los TPs:** Cada número que calcules debe responder una pregunta concreta. Si no sabés qué decisión cambiaría ese número, no lo calcules.

---

# TP1: Exploración y Descripción

## Concepto general del TP

El TP1 trabaja con la encuesta Sysarmy 2026 y se divide en dos ejercicios que cubren los contenidos de las Clases 1 y 2.

> **Clase 1 — EDA y descriptiva:** Cómo limpiar, resumir y comparar distribuciones sin asumir nada de antemano.
> **Clase 2 — Relaciones multivariadas:** Cómo detectar patrones entre dos o más variables sin confundir asociación con causalidad.

El ejercicio 1 compara salarios entre lenguajes de programación. El ejercicio 2 analiza densidades conjuntas, asociaciones y condicionales entre variables numéricas.

---

## Ejercicio 1: Lenguajes vs Salarios

### ¿Qué se pide?

Comparar la distribución de salarios netos entre diferentes lenguajes de programación, aplicando técnicas de limpieza, análisis descriptivo y probabilidad condicional.

### Conceptos de clase involucrados

**EDA (Análisis Exploratorio de Datos)**
Proceso iterativo de familiarización con los datos antes de modelar. Incluye: inspección de estructura, identificación de valores faltantes, detección de outliers, y búsqueda de patrones preliminares.

**Coherencia sustantiva**
Criterio de limpieza basado en conocimiento del dominio. Por ejemplo: un salario mensual de $1.000.000 es estadísticamente posible pero sustantivamente sospechoso para el contexto argentino 2026; un salario de $0 es imposible. Los límites del IQR son una guía matemática, pero el criterio final debe ser sustantivo.

**Rango Intercuartílico (IQR)**
Diferencia entre el tercer y primer cuartil (Q3 − Q1). Se usa para detectar valores extremos: típicamente se consideran outliers los valores por debajo de Q1 − 1.5×IQR o por encima de Q3 + 1.5×IQR.

**Media vs Mediana**
- Media: promedio aritmético. Sensible a outliers; representa el "centro de masa" de la distribución.
- Mediana: valor que divide la distribución en dos mitades iguales. Robusta a outliers; representa el "punto medio" de las observaciones ordenadas.

**Percentil 90 (P90)**
Valor por debajo del cual cae el 90% de las observaciones. En salarios, representa lo que gana el 10% mejor remunerado.

**Coeficiente de Variación (CV)**
Desvío estándar dividido la media, expresado como porcentaje: CV = σ/μ. Mide la dispersión relativa, permitiendo comparar variables con escalas diferentes.

**Asimetría (Skewness)**
Medida de la falta de simetría de una distribución. Skewness > 0 indica cola derecha larga (pocos valores muy altos), típica en distribuciones de ingresos.

**Probabilidad condicional**
P(A|B) = P(A ∩ B) / P(B). La probabilidad de A dado que ocurrió B. En este TP: probabilidad de ganar más de X pesos dado que se programa en cierto lenguaje.

**Lift**
Medida de asociación entre eventos: Lift = P(A|B) / P(A). Si Lift > 1, B aumenta la probabilidad de A. Lift = 1 indica independencia. Lift < 1 indica que B disminuye la probabilidad de A.

**Variable confusora**
Variable que afecta tanto a la variable independiente como a la dependiente, creando una asociación espuria. En este ejercicio, la dedicación (Full-Time vs Part-Time) actúa como confusor porque correlaciona tanto con el lenguaje como con el salario.

### Lo que hiciste (paso a paso)

1. **Carga y limpieza inicial:** Importaste la encuesta Sysarmy 2026, seleccionaste las columnas relevantes (lenguaje, salario neto, dedicación), y eliminaste valores faltantes en las variables clave.

2. **Filtro de coherencia sustantiva:** Aplicaste el criterio IQR como guía, pero tomaste decisiones finales basadas en conocimiento del dominio. Por ejemplo, podrías haber descartado salarios menores a $50.000 (muy bajos para IT en 2026) o mayores a $5.000.000 (probables errores de carga).

3. **Control de confusores:** Filtraste solo trabajadores Full-Time para eliminar la confusión entre dedicación y lenguaje. Si comparás Python (muy Full-Time) con JavaScript (más mixto) sin este filtro, la diferencia de salarios reflejaría dedicación, no lenguaje.

4. **Umbral de 100 respuestas:** Descartaste lenguajes con menos de 100 encuestados para evitar comparar con muestras ridículamente pequeñas.

5. **Análisis por opciones:**
   - **Opción A (visualizaciones):** Boxplots, violinplots y KDEs para comparar formas, medianas y dispersión entre lenguajes.
   - **Opción B (descriptiva):** Calculaste media, mediana, P90, CV y skewness por lenguaje, y armaste un ranking.
   - **Opción C (probabilidad):** Calculaste P(salario ≥ umbral | lenguaje) para cada tecnología y comparaste con la probabilidad marginal usando lift.

### Interpretación

> **Ejemplo numérico concreto:**
> Supongamos que en tu análisis encontraste que el 35% de los programadores Python ganan más de $800.000 netos, mientras que solo el 15% de los programadores JavaScript alcanzan ese umbral. El lift sería: Lift = 0.35 / 0.15 = 2.33. Esto significa que programar en Python multiplica por 2.33 la probabilidad de estar en el top salarial (> $800k), respecto de la población general.

### Conexión con la teoría

Este ejercicio conecta directamente con los conceptos de **Clase 1 (EDA y descriptiva)** y **Clase 2 (relaciones multivariadas)**:

- El EDA inicial es la aplicación práctica del principio de que "antes de modelar, hay que conocer los datos".
- El control de confusores (Full-Time, umbral de 100) es la aplicación del principio de que "la asociación no implica causalidad".
- La comparación de medias, medianas y percentiles refleja el concepto de que "la media es solo una cara de la distribución".
- El lift es una aplicación directa de probabilidad condicional y regla de Bayes.

### Errores comunes que este ejercicio te obliga a evitar

1. **Limpiar solo con IQR sin pensar:** El IQR es una guía matemática, no una ley. Un salario de $4.000.000 puede ser un outlier matemático pero totalmente real en un senior de arquitectura. Mirá los datos, no solo los números.

2. **Olvidar el umbral de muestra:** Comparar Go (45 respuestas) con Python (1200 respuestas) es estadísticamente vergonzoso. La varianza del promedio en muestras chicas es enorme.

3. **No controlar confusores:** Si no filtrás por Full-Time, podés concluir que "Python paga más" cuando en realidad "Python tiene más Full-Time".

4. **Confundir media con mediana:** Si decís "Python paga $900.000 de promedio" sin aclarar que la mediana es $650.000, estás ocultando que hay pocos casos muy altos que tiran el promedio.

---

## Ejercicio 2: Densidades y Variables

### ¿Qué se pide?

Analizar las relaciones entre variables numéricas de la encuesta usando diferentes técnicas de densidad y asociación.

### Conceptos de clase involucrados

**Densidad conjunta**
Distribución de probabilidad de dos variables consideradas simultáneamente. Visualmente se representa con pairplots o jointplots que muestran tanto la relación bivariada como las marginales.

**Heatmap de correlación**
Matriz de correlaciones visualizada con color. Permite detectar rápidamente qué variables se mueven juntas, pero **solo captura relaciones lineales**.

**Correlación de Pearson (r)**
Medida de asociación lineal entre dos variables continuas. Varía entre -1 y 1. r = 1 indica relación lineal perfecta positiva; r = 0 indica ausencia de relación lineal. **No captura relaciones no lineales.**

**Correlación de Spearman (ρ)**
Versión robusta de Pearson calculada sobre los rangos de las variables. Captura relaciones monotónicas (crecientes o decrecientes) sin asumir linealidad. Es menos sensible a outliers.

**R² (Coeficiente de determinación)**
Porcentaje de varianza de Y explicado por X en un modelo lineal. R² = 0.64 significa que el 64% de la variabilidad de Y se "explica" (estadísticamente) por X. **No implica causalidad.**

**Redundancia bruto-neto**
Diferencia entre la correlación cruda (bruta) entre dos variables y la correlación parcial (neta) que controla por una tercera variable. Si la correlación baja mucho al controlar, la relación era espuria.

**Densidad condicional**
Distribución de una variable dado un valor o rango de otra. Visualmente: histogramas de salario separados por grupo (ej. con/sin título universitario).

**Test de Mann-Whitney U**
Test no paramétrico para comparar dos muestras independientes. No asume normalidad. Compara rangos en lugar de valores. Útil cuando la normalidad es dudosa o los outliers dominan.

**Scatter plot con hue**
Diagrama de dispersión donde el color representa una tercera variable categórica. Permite visualizar relaciones condicionales.

**Lmplot por grupo**
Scatter plot con rectas de regresión ajustadas por separado para cada grupo. Permite ver si la pendiente de la relación cambia entre categorías.

### Lo que hiciste (paso a paso)

**2a: Densidad conjunta**
1. Seleccionaste variables numéricas relevantes (años de experiencia, salario neto, edad).
2. Generaste un pairplot para ver todas las relaciones bivariadas y las distribuciones marginales.
3. Creaste un jointplot de las dos variables más interesantes (ej. experiencia vs salario) con KDE en los márgenes.
4. Calculaste y visualizaste la matriz de correlación con un heatmap.

**2b: Asociación**
1. Calculaste Pearson y Spearman para las mismas parejas de variables.
2. Comparaste ambos coeficientes: si Spearman >> Pearson, la relación es monotónica pero no lineal.
3. Calculaste R² para cuantificar cuánta varianza se explica.
4. Analizaste redundancia bruto-neto controlando por una tercera variable (ej. controlar experiencia al analizar edad vs salario).

**2c: Densidad condicional**
1. Separaste la muestra en dos grupos según una variable categórica (ej. con/sin título universitario).
2. Superpusiste los histogramas de salario para ambos grupos.
3. Aplicaste Mann-Whitney para testear si las distribuciones son idénticas.

**2d: Densidad conjunta condicional**
1. Generaste un scatter plot de experiencia vs salario con color por nivel de seniority.
2. Usaste lmplot para ajustar rectas de regresión separadas por seniority.
3. Interpretaste si la pendiente "años → salario" cambia según el nivel.

### Interpretación

> **Ejemplo numérico concreto:**
> Supongamos que encontraste r = 0.72 entre años de experiencia y salario neto, pero ρ = 0.85. La diferencia indica que la relación es monotónica creciente pero no estrictamente lineal: los primeros años de experiencia impactan mucho en salario, pero después la curva se aplana. El R² = 0.52 indica que la experiencia "explica" el 52% de la varianza salarial; el 48% restante son otros factores (tecnología, empresa, negociación, etc.).
>
> Al controlar por seniority, la correlación bruta experiencia-salario podría bajar de 0.72 a 0.40 (redundancia bruto-neto = 0.32). Esto significa que gran parte de la relación entre experiencia y salario operaba *a través de* la seniority: más experiencia → más seniority → más salario.

### Conexión con la teoría

Este ejercicio es la **Clase 2 en acción pura**:

- 2a aplica el concepto de que "dos variables vistas juntas revelan más que por separado".
- 2b aplica la distinción entre asociación lineal y monotónica, y la idea de que "correlación no implica causalidad" (controlando confusores).
- 2c aplica el concepto de densidad condicional: la distribución de Y cambia según X.
- 2d aplica la idea de interacción: la relación entre X e Y depende de Z.

### Errores comunes que este ejercicio te obliga a evitar

1. **Interpretar Pearson como "fuerza de relación" general:** Pearson solo mide linealidad. Si r = 0 pero los puntos forman una U perfecta, la relación es fuerte pero no lineal. Siempre mirá el scatter plot.

2. **Confundir R² con importancia práctica:** R² = 0.52 suena impresionante, pero si el contexto de decisión requiere predecir salarios con precisión de ±$50.000, ese R² puede ser insuficiente.

3. **Ignorar el bruto-neto:** Si no controlás por confusores, podés concluir que "edad predice salario" cuando en realidad "edad predice experiencia, y experiencia predice salario".

4. **Mann-Whitney sin justificar:** Si los datos son normales y sin outliers, el t-test tiene más potencia. Usá Mann-Whitney cuando la normalidad es dudosa o los outliers dominan.

---

# TP2: Inferencia y Comunicación

## Concepto general del TP

El TP2 trabaja con la misma encuesta Sysarmy 2026 pero cambia el enfoque: de explorar para encontrar patrones, a argumentar con rigor sobre una pregunta específica.

> **Clase 3 — Inferencia:** Cómo estimar parámetros poblacionales a partir de muestras, cuantificar la incertidumbre con intervalos, y validar métodos.
> **Clase 4 — Test de hipótesis y comunicación:** Cómo tomar decisiones bajo incertidumbre, controlar errores, y presentar resultados sin mentir.

---

## Ejercicio 1: Estimación

### ¿Qué se pide?

Estimar la diferencia de salarios medios entre dos grupos (ej. dos lenguajes o dos condiciones) y construir un intervalo de confianza para esa diferencia.

### Conceptos de clase involucrados

**Estimación puntual**
Valor calculado a partir de la muestra que aproxima un parámetro poblacional. Es "lo mejor que podemos decir" con un solo número, pero oculta la incertidumbre.

**Intervalo de confianza (IC)**
Rango de valores que, con un cierto nivel de confianza (típicamente 95%), contiene al parámetro poblacional verdadero. No dice "la probabilidad de que μ esté acá es 95%"; dice "el 95% de los ICs construidos así contendrían a μ".

**Welch-Satterthwaite**
Aproximación para los grados de libertad del t-test cuando las varianzas de los dos grupos son desiguales. Es más robusto que asumir varianzas iguales.

**Interpretación frecuentista**
En la estadística frecuentista, el parámetro es fijo (no aleatorio) y el intervalo es aleatorio (depende de la muestra). Un IC 95% significa: si repitiera el muestreo infinitas veces, el 95% de los intervalos construidos contendrían al verdadero parámetro.

**Bootstrap**
Método de remuestreo que construye la distribución de un estimador simulando muestras a partir de los datos observados. Es especialmente útil cuando las fórmulas teóricas son complicadas o las suposiciones son dudosas.

### Lo que hiciste (paso a paso)

1. **Filtrado + limpieza:** Aplicaste los mismos criterios del TP1 (coherencia sustantiva, Full-Time, umbral de 100 respuestas).

2. **Estimación puntual:** Calculaste la diferencia de medias muestrales entre los dos grupos: d̂ = x̄₁ − x̄₂.

3. **IC 95% con Welch-Satterthwaite:** Calculaste el error estándar de la diferencia asumiendo varianzas desiguales, usaste los grados de libertad aproximados de Welch-Satterthwaite, y construiste el intervalo: d̂ ± t_{α/2, df} × SE(d̂).

4. **Validación bootstrap:** Remuestreaste con reemplazo B veces (ej. 10.000), calculaste la diferencia de medias en cada remuestra, y usaste los percentiles 2.5 y 97.5 de la distribución bootstrap como IC alternativo. Comparaste con el teórico.

### Interpretación

> **Ejemplo numérico concreto (usando los valores del notebook):**
> Diferencia de medias: $378.373 (el Grupo A gana en promedio $378.373 más que el Grupo B).
> IC 95%: [$275.922, $480.825].
>
> **Interpretación correcta (frecuentista):** "Si repitiera este muestreo muchas veces, el 95% de los intervalos construidos de esta forma contendrían la verdadera diferencia de medias poblacional. Este intervalo particular [275.922, 480.825] o contiene al parámetro o no; no hay probabilidad involucrada."
>
> **Interpretación incorrecta (pero común):** "Hay un 95% de probabilidad de que la diferencia verdadera esté entre 275.922 y 480.825." Eso es falso. El parámetro es fijo; lo aleatorio es el intervalo.

### Conexión con la teoría

Este ejercicio es la **Clase 3 en acción**:

- La estimación puntual es el concepto de "resumen muestral del parámetro".
- El IC formaliza la incertidumbre muestral: "no solo te digo cuánto, sino qué tan seguro estoy".
- Welch-Satterthwaite aplica el principio de "no asumas lo que no sabés" (varianzas iguales).
- Bootstrap aplica el principio de "si no te fías de las fórmulas, simulá".

### Errores comunes que este ejercicio te obliga a evitar

1. **Interpretar el IC como probabilidad sobre el parámetro:** El parámetro no es aleatorio. El intervalo es aleatorio. Decir "la probabilidad de que μ esté en [a, b] es 95%" es conceptualmente falso.

2. **Ignorar la aproximación de Welch-Satterthwaite:** Si las varianzas son muy distintas y usás el t-test clásico (varianzas iguales), el IC será más angosto de lo que debería y tendrá cobertura real menor al 95%.

3. **Bootstrap con B muy chico:** 100 remuestras no son suficientes para estimar percentiles con precisión. Usá al menos 5.000-10.000.

4. **Olvidar que el IC depende del modelo:** Si tu modelo asume independencia y los datos están correlacionados (ej. múltiples respuestas de la misma empresa), el IC será optimista (más angosto de lo correcto).

---

## Ejercicio 2: Test de Hipótesis

### ¿Qué se pide?

Formular una hipótesis sobre la diferencia de medias, testearla estadísticamente, evaluar la potencia, calcular el tamaño de efecto, y verificar robustez.

### Conceptos de clase involucrados

**Hipótesis nula (H₀)**
Afirmación de "no efecto" o "no diferencia" que se asume temporalmente cierta. Es el "estatus quo" que los datos deben refutar con evidencia suficiente. Ej: H₀: μ₁ − μ₂ = 0.

**Hipótesis alternativa (H₁)**
Afirmación que queremos demostrar. En este ejercicio es **bilateral**: H₁: μ₁ − μ₂ ≠ 0 (nos interesa detectar cualquier diferencia, no solo que A > B).

**Test t de Welch**
Versión del t-test que no asume varianzas iguales entre grupos. Es el estándar por defecto en la práctica moderna porque las varianzas raramente son idénticas.

**p-valor**
Probabilidad de obtener un resultado tan extremo como el observado (o más), **asumiendo que H₀ es verdadera**. Es una medida de compatibilidad entre los datos y H₀, no de la probabilidad de que H₀ sea verdadera.

**Nivel de significación (α)**
Umbral de decisión. Típicamente 0.05. Si p < α, rechazamos H₀. Es la probabilidad de cometer un Error Tipo I (rechazar H₀ cuando es verdadera).

**Potencia estadística (1 − β)**
Probabilidad de rechazar H₀ cuando H₁ es verdadera. Es la capacidad del test de detectar un efecto que realmente existe. Potencia baja = muchos falsos negativos.

**Monte Carlo**
Método de simulación que genera datos bajo condiciones conocidas para estudiar propiedades de un procedimiento estadístico. En este caso: simular muchas muestras bajo H₁ y ver qué proporción rechaza H₀.

**Tamaño de efecto**
Medida estandarizada de la magnitud de una diferencia, independiente de la escala original.
- **Cohen's d:** (x̄₁ − x̄₂) / s_pooled. Estándar de la industria.
- **Hedges' g:** Versión corregida de Cohen's d para muestras pequeñas. Reduce el sesgo hacia valores inflados.

**Test de Mann-Whitney (robustez)**
Análisis de sensibilidad: ¿cambia la conclusión si usamos un método no paramétrico en lugar del t-test? Si ambos coinciden, tenemos mayor confianza. Si discrepan, investigar por qué.

**Relación IC ↔ test**
Hay una dualidad exacta: un IC 95% que NO contiene al valor nulo (ej. 0) equivale a rechazar H₀ con α = 0.05 bilateral. Es la misma información presentada de dos formas.

### Lo que hiciste (paso a paso)

1. **Formulación H₀/H₁ bilateral:**
   - H₀: μ_python − μ_javascript = 0 (no hay diferencia)
   - H₁: μ_python − μ_javascript ≠ 0 (hay diferencia, en cualquier dirección)

2. **Test t de Welch:** Calculaste el estadístico t y el p-valor asumiendo varianzas desiguales.

3. **Decisión:** Comparaste p con α = 0.05. Si p < 0.05, rechazaste H₀.

4. **Potencia vía Monte Carlo:**
   - Fijaste el tamaño de efecto observado como "verdadero".
   - Simulaste 10.000 pares de muestras con ese efecto.
   - Aplicaste Welch a cada par.
   - Calculaste la proporción de rechazos = potencia estimada.

5. **Tamaño de efecto:** Calculaste Cohen's d y Hedges' g para cuantificar qué tan grande es la diferencia en términos estandarizados.

6. **Robustez:** Aplicaste Mann-Whitney a los mismos datos y comparaste la conclusión con Welch.

7. **Relación IC-test:** Verificaste que el IC 95% de la diferencia NO contenga al 0 si y solo si p < 0.05.

### Interpretación

> **Ejemplo numérico concreto (usando los valores del notebook):**
>
> - Diferencia de medias: $378.373
> - IC 95%: [$275.922, $480.825]
> - Estadístico t de Welch: ≈ 7.2
> - p-valor: ≈ 0 (técnicamente < 0.001)
> - Decisión: Rechazamos H₀ al nivel α = 0.05
> - Cohen's d = 0.26 (tamaño de efecto pequeño)
> - Hedges' g = 0.26 (prácticamente igual, muestra grande)
> - Potencia estimada (Monte Carlo): > 99% para detectar d = 0.26 con n observado
>
> **Interpretación integral:**
> "Hay evidencia estadísticamente significativa de que Python paga más que JavaScript en promedio (p < 0.001). La diferencia estimada es de aproximadamente $378.000. Sin embargo, el tamaño de efecto es pequeño (d = 0.26): en términos prácticos, las distribuciones se solapan mucho. Con nuestro tamaño de muestra, el test tiene potencia casi perfecta para detectar incluso este efecto pequeño. El análisis robusto (Mann-Whitney) confirma la conclusión."

### Conexión con la teoría

Este ejercicio es la **Clase 4 en estado puro**:

- La formulación bilateral refleja el principio de "dejá que los datos hablen en cualquier dirección".
- El p-valor es la aplicación práctica de la lógica de refutación: asumís H₀ y calculás qué tan raro sería tu resultado si ella fuera cierta.
- La potencia refleja el principio de que "un test puede fallar por poca evidencia (n chico) o por diseño débil".
- El tamaño de efecto aplica el principio de "significación estadística ≠ importancia práctica".
- La robustez aplica el principio de "no confíes en un solo método".

### Errores comunes que este ejercicio te obliga a evitar

1. **"p < 0.05, entonces el efecto es grande":** ¡NO! p depende del tamaño de muestra. Con n = 100.000, podés tener p ≈ 0 con d = 0.05 (imperceptible prácticamente). Siempre reportá tamaño de efecto.

2. **"p = 0.04, efecto real; p = 0.06, no hay efecto":** El umbral α = 0.05 es una convención arbitraria. Un p de 0.06 con d = 0.8 es más interesante que un p de 0.04 con d = 0.1. Mirá el intervalo de confianza.

3. **Olvidar la dirección en bilateral:** Si formulás bilateral pero interpretás unilateral ("Python gana más"), estás cambiando las regas a mitad de camino. Si te interesa solo una dirección, formulá unilateral desde el principio.

4. **No reportar Hedges' g si n es chico:** Cohen's d tiene sesgo hacia arriba en muestras pequeñas. Si n₁ + n₂ < 50, reportá Hedges' g.

5. **Ignorar el IC cuando hacés test:** El IC y el test son la misma información. El IC además te dice la magnitud de la incertidumbre.

---

## Ejercicio 3: Comunicación

### ¿Qué se pide?

Crear visualizaciones efectivas que comuniquen los resultados del ejercicio 2, aplicando principios de honestidad visual y diseño informativo.

### Conceptos de clase involucrados

**Errorbar vs Boxplot**
- **Errorbar:** Muestra un estimador puntual (ej. media) con su incertidumbre (IC). Es para **comunicar** el resultado de una estimación.
- **Boxplot:** Muestra la distribución completa (mediana, cuartiles, outliers). Es para **explorar** y comparar formas.

Regla: usá errorbars cuando querés comunicar un resultado; usá boxplots cuando querés explorar los datos.

**Honestidad visual**
Principio de que la representación gráfica debe reflejar fielmente la magnitud y la incertidumbre de los datos. Mostrar solo la media sin el IC es visualmente engañoso porque oculta la variabilidad.

**Título interpretativo**
Título que resume la conclusión principal del gráfico, no solo describe qué variables se muestran. "Diferencia salarial entre Python y JavaScript" es descriptivo; "Python paga $378k más en promedio, pero con gran solapamiento" es interpretativo.

**Contexto metodológico**
Información necesaria para interpretar correctamente: tamaño de muestra, nivel de confianza, método estadístico, filtros aplicados. Un gráfico sin contexto metodológico es inutilizable para la toma de decisiones.

### Lo que hiciste (paso a paso)

1. **Errorbar con IC:** Graficaste las medias de ambos grupos con barras de error mostrando el IC 95%. Esto comunica: "acá están mis mejores estimaciones y cuánto pueden variar".

2. **Boxplot de apoyo (opcional):** Incluiste un boxplot en un panel separado o en el apéndice para mostrar la distribución completa, evitando que el errorbar dé una falsa sensación de certeza.

3. **Título interpretativo:** Escribiste un título que resuma la conclusión, no solo las variables.

4. **Contexto metodológico:** Agregaste notas al pie o anotaciones con n, método (Welch), α, y filtros aplicados.

### Interpretación

> **Ejemplo de visualización honesta:**
> Un errorbar que muestra:
> - Media Python: $1.200.000 (IC 95%: [$1.150.000, $1.250.000])
> - Media JavaScript: $821.627 (IC 95%: [$780.000, $863.000])
> - Título: "Diferencia significativa pero pequeña: Python paga $378k más, pero las distribuciones se solapan ampliamente"
> - Nota: "n = 1.847 (Python), n = 2.134 (JS). IC 95% con Welch-Satterthwaite. Filtrado: Full-Time, salarios entre $50k y $5M."

### Conexión con la teoría

Este ejercicio conecta con la **segunda mitad de la Clase 4**:

- Errorbar vs boxplot es la aplicación del principio de "la herramienta debe servir al objetivo: explorar vs comunicar".
- La honestidad visual es la aplicación ética de la inferencia: si calculaste un IC, mostralo.
- El título interpretativo aplica el principio de que "un gráfico sin interpretación es solo un dibujo".
- El contexto metodológico aplica el principio de reproducibilidad: otro analista debe poder juzgar tu conclusión.

### Errores comunes que este ejercicio te obliga a evitar

1. **Errorbar sin el IC:** Mostrar solo la media con barras de error que representan el desvío estándar (o peor, el desvío estándar de la media) sin aclarar qué es. Siempre especificá: "barras = IC 95%".

2. **Truncar el eje Y para exagerar:** Si la diferencia es $378k y el eje va de $800k a $1.300k, la diferencia parece enorme. Si el eje va de $0 a $2M, se ve en perspectiva. Sé honesto con la escala.

3. **Boxplot como figura principal de comunicación:** Un boxplot muestra mucha información, pero dificulta comparar estimaciones puntuales. Para comunicar un resultado de inferencia, el errorbar es más directo.

4. **Olvidar el tamaño de muestra en el gráfico:** n = 30 y n = 3.000 producen ICs de anchos muy distintos. Sin saber n, el lector no puede juzgar la precisión.

5. **Título puramente descriptivo:** "Salarios por lenguaje" no aporta nada que el gráfico no diga solo. "Diferencia significativa pero con efecto pequeño" guía la interpretación.

---

# Checklist de comprensión

## TP1

- [ ] Sé limpiar datos aplicando tanto criterios estadísticos (IQR) como sustantivos (conocimiento del dominio).
- [ ] Puedo explicar por qué la mediana es más robusta que la media en distribuciones asimétricas.
- [ ] Entiendo que el lift m cuánto aumenta la probabilidad condicional respecto de la marginal.
- [ ] Sé identificar una variable confusora y explicar cómo distorsiona la relación.
- [ ] Puedo interpretar un pairplot, un jointplot y un heatmap de correlación.
- [ ] Distingo cuándo usar Pearson vs Spearman y por qué.
- [ ] Entiendo el concepto de redundancia bruto-neto y sé calcularla.
- [ ] Sé cuándo usar Mann-Whitney en lugar de un t-test.
- [ ] Puedo interpretar un lmplot por grupos y detectar interacciones.

## TP2

- [ ] Puedo formular H₀ y H₁ bilateral para una diferencia de medias.
- [ ] Entiendo que el p-valor mide compatibilidad con H₀, no probabilidad de H₀.
- [ ] Sé interpretar un IC 95% en términos frecuentistas (repetición del muestreo).
- [ ] Puedo construir un IC con Welch-Satterthwaite y validarlo con bootstrap.
- [ ] Entiendo que significación estadística ≠ importancia práctica.
- [ ] Sé calcular e interpretar Cohen's d y Hedges' g.
- [ ] Puedo estimar potencia por simulación Monte Carlo.
- [ ] Sé verificar robustez comparando conclusiones de métodos paramétricos y no paramétricos.
- [ ] Entiendo la dualidad exacta entre IC y test de hipótesis.
- [ ] Sé decidir entre errorbar (comunicar) y boxplot (explorar).
- [ ] Puedo diseñar una visualización honesta que muestre estimación + incertidumbre + contexto.

---

# Glosario rápido del TP

| Término | Definición en una oración |
|---------|---------------------------|
| **Bootstrap** | Remuestreo con reemplazo para estimar la distribución de un estadístico sin fórmulas teóricas. |
| **Cohen's d** | Diferencia de medias estandarizada: (x̄₁ − x̄₂) / s_pooled. d = 0.2 es pequeño, 0.5 mediano, 0.8 grande. |
| **Coherencia sustantiva** | Criterio de limpieza basado en conocimiento del dominio, no solo en reglas estadísticas. |
| **Confusor** | Variable que influye en X e Y simultáneamente, creando asociación espuria. |
| **CV** | Desvío estándar / media. Permite comparar dispersión entre variables con escalas distintas. |
| **Densidad condicional** | Distribución de una variable dado un valor o rango de otra. |
| **Densidad conjunta** | Distribución de dos variables consideradas simultáneamente. |
| **Error Tipo I** | Rechazar H₀ cuando es verdadera (falso positivo). Controlado por α. |
| **Error Tipo II** | No rechazar H₀ cuando es falsa (falso negativo). Probabilidad = β. |
| **Hedges' g** | Versión corregida de Cohen's d para muestras pequeñas. |
| **Heatmap** | Visualización de matriz de correlaciones con color. |
| **H₀ / H₁** | Hipótesis nula (no efecto) y alternativa (efecto existe). |
| **IQR** | Rango intercuartílico: Q3 − Q1. Usado para detectar outliers. |
| **Lift** | P(A\|B) / P(A). Mide cuánto aumenta la probabilidad de A al saber B. |
| **Mann-Whitney U** | Test no paramétrico para comparar dos muestras independientes por sus rangos. |
| **Monte Carlo** | Simulación numérica para estudiar propiedades de un procedimiento estadístico. |
| **p-valor** | Probabilidad del resultado observado (o más extremo) bajo H₀. |
| **Pearson r** | Correlación lineal. −1 a 1. Solo captura linealidad. |
| **Potencia** | 1 − β. Probabilidad de detectar un efecto que realmente existe. |
| **R²** | Porcentaje de varianza explicada por un modelo lineal. |
| **Redundancia bruto-neto** | Diferencia entre correlación cruda y correlación parcial (controlando confusores). |
| **Skewness** | Asimetría de la distribución. > 0 = cola derecha larga. |
| **Spearman ρ** | Correlación de rangos. Captura relaciones monotónicas sin asumir linealidad. |
| **Welch-Satterthwaite** | Aproximación de grados de libertad para t-test con varianzas desiguales. |
| **Welch's t-test** | t-test que no asume varianzas iguales entre grupos. Estándar moderno. |
