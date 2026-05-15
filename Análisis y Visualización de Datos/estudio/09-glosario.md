# 09 — Glosario

Este glosario no es un diccionario de traducciones. Cada definición incluye una explicación conceptual de por qué el término importa en la materia.

---

## A

**ANOVA** (Análisis de Varianza)
Test que compara las medias de más de dos grupos simultáneamente. Evita el problema de hacer múltiples test t por pares, que infla la probabilidad de error tipo I. Usa el estadístico F.

**Autorreporte**
Sesgo que surge cuando la información depende de lo que declara la persona encuestada (ej: salario, rol). Puede haber errores de memoria, redondeo o exageración. No se elimina con limpieza: hay que reconocerlo como limitación.

**Autoselección**
Sesgo que ocurre cuando responde quien decide hacerlo. En Sysarmy, quienes responden pueden ser más comprometidos con la comunidad IT, más jóvenes, o tener más tiempo. La muestra no representa automáticamente a todo el mercado laboral.

## C

**Cohen's d**
Medida estandarizada del tamaño de efecto. Calcula la diferencia de medias dividida por el desvío combinado. Permite comparar la magnitud de un efecto entre estudios con escalas distintas. d ≈ 0.2 es pequeño, 0.5 medio, 0.8 grande.

**Correlación**
Medida de asociación lineal entre dos variables numéricas. Pearson mide relación lineal; Spearman mide relación monotónica (usa rangos). Correlación alta no implica causalidad.

**Cuantitativa (variable)**
Variable que toma valores numéricos. Puede ser discreta (contable, como años de experiencia) o continua (como salario). Se pueden calcular medias, desvíos y correlaciones.

**Cualitativa (variable)** → ver **Variable categórica**.

## D

**Desvío estándar (s)**
Raíz cuadrada de la varianza. Mide la dispersión típica de los datos individuales alrededor de la media. Tiene las mismas unidades que los datos. **No es lo mismo que error estándar**.

**Distribución muestral**
Distribución que tendría un estadístico (por ejemplo, la media) si repitiéramos el muestreo infinitas veces. Es el fundamento teórico del error estándar y del TCL.

## E

**EDA** (Exploratory Data Analysis / Análisis Exploratorio de Datos)
Primera etapa de cualquier análisis. Consiste en inspeccionar la estructura, calidad y potencial analítico de los datos antes de modelar o inferir. No es "perder tiempo": es donde se toman las decisiones metodológicas más importantes.

**Error estándar (EE)**
Desvío estándar de la distribución muestral de un estimador. Mide cuánto "tiembla" el estimador (por ejemplo, la media muestral) si repetimos la muestra. EE = s / √n para la media.

**Error tipo I**
Rechazar H0 cuando en realidad es cierta. Su probabilidad está controlada por α.

**Error tipo II**
No rechazar H0 cuando en realidad es falsa. Su probabilidad es β. La potencia es 1 − β.

**Estadístico**
Cantidad calculada a partir de la muestra (ej: x̄, s, el estadístico t). Se usa para estimar parámetros o para tests.

**Estimación puntual**
Un único número que aproxima un parámetro poblacional. Problema: no indica incertidumbre. Por eso se complementa con un intervalo de confianza.

## H

**Hedges' g**
Corrección de Cohen's d para sesgo muestral. En muestras grandes es prácticamente igual a d. Se recomienda cuando los grupos son pequeños.

**Hipótesis nula (H0)**
Suposición de referencia que se contrasta con los datos. Representa típicamente "no hay efecto" o "no hay diferencia". Se rechaza si la evidencia muestral es lo suficientemente incompatible.

**Hipótesis alternativa (H1)**
Suposición que representa el efecto o diferencia que queremos detectar. Puede ser bilateral (≠) o unilateral (> o <).

## I

**IQR** (Rango Intercuartílico)
Q3 − Q1. Mide el ancho del 50% central de los datos. Es robusto a outliers porque no usa la media ni los extremos.

**IC** (Intervalo de Confianza)
Rango de valores plausibles para un parámetro, construido a partir de la muestra. Un IC del 95% significa que el procedimiento captura el parámetro en el 95% de las muestras repetidas.

**Independencia estadística**
Dos variables (o eventos) son independientes si saber el valor de una no cambia la distribución de la otra. Formalmente: P(A|B) = P(A) o f(X|Y) = f(X).

## M

**Media (x̄)**
Promedio aritmético. Es el centro de masa de la distribución. Muy sensible a outliers. En distribuciones asimétricas, la media se tira hacia la cola larga.

**Mediana**
Valor que divide los datos ordenados en dos mitades iguales. Es robusta a outliers. Cuando media y mediana difieren mucho, sospechá asimetría.

**Moda**
Valor más frecuente. Útil para variables categóricas. Una variable continua puede no tener moda (todos los valores son distintos) o tener muchas.

## N

**Nivel de significación (α)**
Umbral para el error tipo I. Típicamente 0.05 (5%). Si p-valor < α, rechazamos H0. α = 0.01 es más estricto; α = 0.10 es más permisivo.

## O

**Outlier**
Observación que cae fuera del rango esperado según el resto de los datos. Puede ser un error de carga o un dato real pero extremo. La decisión de eliminarlo depende del objetivo del análisis, no de una regla automática.

## P

**Parámetro**
Cantidad desconocida en la población (ej: μ, la media poblacional). Se estima con estadísticos muestrales.

**p-valor**
Probabilidad de observar un estadístico de prueba tan extremo o más extremo que el calculado, asumiendo que H0 es cierta. **No** es la probabilidad de que H0 sea verdadera. Un p-valor chico indica que los datos son poco compatibles con H0.

**Población**
Conjunto completo de individuos o unidades sobre las que queremos inferir. En la práctica, rara vez la observamos en su totalidad.

**Potencia**
Probabilidad de rechazar H0 cuando en realidad es falsa (1 − β). Aumenta con: mayor tamaño del efecto, mayor n, menor variabilidad, y α más alto.

## R

**Robustez**
Estabilidad de una conclusión ante cambios metodológicos. En TP2, contrastaste la conclusión del test t con medianas y con Mann-Whitney. Si la señal se mantiene, el hallazgo es robusto.

## S

**Subcobertura**
Sesgo que ocurre cuando ciertos perfiles están menos representados en la muestra que en la población. Por ejemplo, si la encuesta se difunde principalmente en Twitter, personas que no usan Twitter quedan subcubiertas.

## T

**TCL** (Teorema Central del Límite)
Aunque los datos individuales no sean normales, la media muestral tiende a distribuirse normalmente cuando n es grande. Es el fundamento que permite usar intervalos z/t y tests de hipótesis sin conocer la distribución exacta de los datos.

**Test t de Welch**
Versión del test t para dos muestras independientes que no asume igualdad de varianzas. Es la opción por defecto en datos reales. En Python: `scipy.stats.ttest_ind(..., equal_var=False)`.

## V

**Variable aleatoria**
Variable cuyos valores provienen de un mecanismo incierto. En la encuesta, cada columna puede modelarse como una variable aleatoria, y cada fila es una realización.

**Variable categórica**
Variable que toma valores de un conjunto predefinido de categorías. Puede ser nominal (sin orden, ej: provincia) u ordinal (con orden, ej: nivel de estudios).

**Varianza (s²)**
Promedio de las distancias al cuadrado a la media. Usamos N−1 en el denominador para que sea insesgada. Es la base del desvío estándar y del error estándar.

---

**Próximo paso**: `10-preguntas-guia.md`
