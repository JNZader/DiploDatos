# 04 — Estimación e inferencia

## Concepto

La inferencia estadística usa una **muestra** (lo que observaste) para decir algo, con incertidumbre explícita, sobre una **población** (lo que no observaste). No es magia: es modelar cuánto puede variar tu estimación si repitieras el estudio muchas veces.

## Intuición

Imaginá que querés saber el peso promedio de todos los adultos de Argentina. No podés pesar a 30 millones de personas. Entonces pesás a 1000 elegidos al azar y calculás su promedio. Ese número es una aproximación. Pero, ¿cuánto se equivoca? Si pesás a otros 1000, ¿el promedio cambia mucho? La inferencia cuantifica ese "temblor" del promedio.

---

## Población, muestra, parámetro y estadístico

| Término | Definición | Ejemplo en TP2 |
|---------|------------|----------------|
| **Población** | Conjunto completo sobre el que queremos inferir | Todos los trabajadores IT de Argentina |
| **Muestra** | Subconjunto observado | Los encuestados de Sysarmy que cumplen los filtros |
| **Parámetro** | Cantidad desconocida en la población | μ_A = media salarial poblacional de Varón cis |
| **Estadístico** | Cantidad calculada con la muestra | x̄_A = media salarial muestral de Varón cis |

**La lógica central**:
- La población tiene una media μ que no vemos.
- La muestra tiene una media x̄ que calculamos.
- Usamos x̄ para aproximar μ, pero sabemos que x̄ varía de muestra en muestra.

## Estimación puntual

Es un único número que aproxima un parámetro.

- x̄ estima μ.
- p̂ (proporción muestral) estima p (proporción poblacional).
- x̄_A − x̄_B estima μ_A − μ_B.

**Problema**: una estimación puntual no viene con garantía. Siempre tiene error posible. Por eso necesitamos medir cuánto varía el estimador.

## Distribución muestral

Si pudieras repetir el muestreo infinitas veces, obtendrías infinitas medias muestrales distintas. Esas medias forman una **distribución muestral**.

**Intuición**: cada muestra te da un promedio ligeramente distinto. La distribución muestral es el histograma de todos esos promedios imaginarios.

**Propiedad clave**: la media de todas esas medias muestrales es igual a μ (el estimador es insesgado). Pero cada media individual se desvía un poco.

## Error estándar

El **error estándar (EE)** mide la dispersión típica del estimador entre muestras.

### Fórmula para la media muestral

$$
EE(\bar{x}) = \frac{s}{\sqrt{n}}
$$

Donde:
- s = desvío estándar muestral.
- n = tamaño muestral.

**Intuición**: no mide la dispersión de los datos individuales, sino la dispersión del **promedio**. Si los datos son muy variables (s grande), el promedio tiembla más. Si la muestra es grande (n grande), el promedio se estabiliza.

**Ejemplo numérico**:
- Grupo A: media = $1.500.000, desvío = $400.000, n = 1600.
- EE = 400.000 / √1600 = 400.000 / 40 = **$10.000**.

Esto significa: si repitieras la encuesta muchas veces, los promedios de Grupo A "tembalarían" alrededor de $1.500.000 con una desviación típica de $10.000.

### Error estándar de la diferencia de medias

$$
EE(\bar{x}_A - \bar{x}_B) = \sqrt{\frac{s_A^2}{n_A} + \frac{s_B^2}{n_B}}
$$

**Ejemplo numérico**:
- Grupo A: s_A = 400.000, n_A = 1600 → s_A²/n_A = 100.000.000.
- Grupo B: s_B = 350.000, n_B = 900 → s_B²/n_B ≈ 136.111.111.
- EE_diff = √(100.000.000 + 136.111.111) = √236.111.111 ≈ **$15.366**.

## Propiedades deseables de un estimador

1. **Insesgadez**: en promedio sobre muchas muestras, apunta al parámetro correcto.
2. **Precisión**: fluctúa poco entre muestras (tiene error estándar chico).
3. **Consistencia**: a medida que n crece, se acerca al parámetro verdadero.

**Compromiso sesgo-varianza**: a veces un estimador puede ser casi insesgado pero muy variable, o algo sesgado pero más estable. En inferencia clásica se prioriza la insesgadez, pero en la práctica también importa la precisión.

## Teorema Central del Límite (TCL)

**Enunciado intuitivo**: aunque los datos individuales no sean normales, la **media muestral** tiende a comportarse como una distribución normal cuando n es grande.

**Condiciones**:
- Las observaciones son aproximadamente independientes.
- El tamaño muestral es suficientemente grande (regla práctica: n > 30 por grupo, pero depende de la asimetría de los datos).
- La distribución original no sea extremadamente patológica (colas muy pesadas).

**Por qué importa**: si la media muestral es aproximadamente normal, podemos construir intervalos de confianza y tests usando la distribución normal (también llamada z, por su variable estandarizada) o la distribución t de Student (para cuando la varianza poblacional es desconocida), sin conocer la distribución exacta de los datos originales.

**Conexión con la clase**: en Clase 3 hiciste simulaciones con distribuciones Poisson y Exponencial (que no son normales) y viste que, al calcular la media de muestras grandes, el histograma de esas medias se parecía a una campana de Gauss (la forma típica de la distribución normal).

## Intervalo de confianza (IC)

Un IC del 95% es un procedimiento que, repetido muchas veces bajo condiciones similares, captura el parámetro en el 95% de las muestras.

### Intuición

Imaginá que el parámetro verdadero es una mosca en una pared. Cada muestra te permite lanzar un aro de basquet. Un IC del 95% es un aro de tamaño tal que, si lanzás 100 aros, atrapás la mosca en 95 de ellos. No sabés si **este** aro particular atrapó a la mosca, pero sabés que el **procedimiento** funciona el 95% de las veces.

### Forma general

$$
IC = \text{estimación} \pm \text{margen de error}
$$

Donde:
- Margen de error = valor crítico × error estándar.
- El valor crítico depende del nivel de confianza (95%, 99%) y de la distribución (z o t).

### Elección entre z y t

| Situación | Usás |
|-----------|------|
| Varianza poblacional conocida (raro en la práctica) | z |
| Varianza poblacional desconocida, estimada con la muestra | t |
| Muestra grande (n > 60 aprox) | z es una buena aproximación de t |

En datos reles, casi siempre usás **t** porque la varianza poblacional es desconocida.

### Ejemplo numérico (diferencia de medias, Welch)

Datos de TP2 (valores redondeados para la explicación):
- Grupo A (Varón cis): x̄_A = $1.478.000, s_A = 380.000, n_A = 1520.
- Grupo B (Mujer cis): x̄_B = $1.100.000, s_B = 340.000, n_B = 880.
- α = 0.05.

Paso 1: estimación puntual.
- diff = 1.478.000 − 1.100.000 = **$378.000**.

Paso 2: error estándar de la diferencia.
- EE = √[(380.000²/1520) + (340.000²/880)] = √[95.000.000 + 131.363.636] = √226.363.636 ≈ **$15.045**.

Paso 3: grados de libertad de Welch-Satterthwaite.
- fórmula compleja, da aproximadamente 2100.

Paso 4: valor crítico t.
- t(0.975, 2100) ≈ 1.96 (muy parecido a z por el tamaño muestral).

Paso 5: margen de error.
- ME = 1.96 × 15.045 ≈ **$29.488**.

Paso 6: IC 95%.
- [378.000 − 29.488, 378.000 + 29.488] = [**$348.512**, **$407.488**].

**Interpretación**: el procedimiento usado produce intervalos que contienen la diferencia poblacional verdadera en el 95% de las muestras. Este intervalo particular no contiene al 0, lo cual es consistente con una diferencia real entre medias.

### Qué afecta el ancho del IC

1. **Mayor variabilidad de los datos** → intervalo más ancho.
2. **Menor tamaño muestral** → intervalo más ancho.
3. **Mayor nivel de confianza** (ej: 99% vs 95%) → intervalo más ancho.

### Interpretación correcta e incorrecta

- ✅ **Correcta**: "El procedimiento tiene un nivel de confianza del 95%."
- ❌ **Incorrecta**: "Hay 95% de probabilidad de que el parámetro verdadero esté en este intervalo." En el enfoque clásico, el parámetro es fijo; lo aleatorio es el intervalo (que varía de muestra en muestra).

### Por qué un IC al 95% no significa "95% de probabilidad de contener la media"

Acá hay un error de interpretación que **el 90% de los estudiantes (y de los profesionales) comete**. Y no es semántica fina: es entender qué es lo aleatorio y qué es lo fijo en el modelo frecuentista.

#### Concepto base: en el marco frecuentista, los parámetros NO tienen distribución

Repetí esto en voz alta hasta que te entre: **el parámetro poblacional es un número fijo, desconocido, pero fijo**. La media salarial verdadera de todos los IT de Argentina es UN número. No tiene varianza. No tiene distribución. Es así de fácil.

Lo único que tiene distribución es **el estimador** (la media muestral) y, en consecuencia, **el intervalo construido a partir del estimador**. Cada vez que tomás una muestra distinta, calculás un IC distinto. Algunos IC contienen la verdadera μ, otros no.

Cuando decimos "IC al 95%" estamos describiendo una **propiedad del procedimiento de fabricación de IC**: si repitiéramos el muestreo infinitas veces, el 95% de los intervalos resultantes contendría a μ. NO estamos diciendo nada sobre **este** intervalo específico.

#### El experimento mental

Imaginate que tomás 100 muestras independientes de Sysarmy, y construís 100 IC al 95% para la media salarial.

- Aproximadamente 95 de esos intervalos van a contener la verdadera μ.
- Aproximadamente 5 NO la van a contener.
- Pero vos solo ves UN intervalo (el que armaste con tu muestra). **No sabés** si es uno de los 95 que aciertan o uno de los 5 que fallan.

Para tu intervalo específico, la probabilidad de contener a μ es 0 o 1: o la contiene o no la contiene. Sólo que no sabés cuál de las dos cosas pasa.

#### La cuenta concreta

Volvé al ejemplo de TP2:
- Estimación puntual de la diferencia: $378.000.
- IC 95%: [$348.512, $407.488].

**Lo que NO podés decir**: "Hay 95% de probabilidad de que la verdadera diferencia esté entre $348.512 y $407.488."

¿Por qué no? Porque la verdadera diferencia es UN número. O está adentro de [348.512, 407.488] (probabilidad = 1) o está afuera (probabilidad = 0). No hay 95% intermedio.

**Lo que SÍ podés decir**:
- "Construimos el intervalo con un procedimiento que captura la verdadera diferencia el 95% de las veces."
- "Bajo los supuestos del modelo, este es un intervalo de confianza del 95% para la diferencia poblacional."
- "Si repitiéramos la encuesta muchas veces, el 95% de los intervalos resultantes contendrían a la verdadera diferencia."

#### Tabla comparativa: frecuentista vs bayesiano

Acá la cosa se pone interesante. Lo que la gente **quiere** decir cuando dice "95% de probabilidad de contener la media" es un enunciado bayesiano, no frecuentista.

| Marco | Qué se considera aleatorio | Interpretación válida del "95%" |
|-------|----------------------------|---------------------------------|
| Frecuentista | El intervalo (varía entre muestras). El parámetro es fijo. | "El procedimiento captura μ el 95% de las veces" |
| Bayesiano | El parámetro (tiene distribución posterior). Los datos son fijos. | "Mi creencia es que P(μ ∈ intervalo) = 0.95" — esto se llama **intervalo creíble** |

Lo que la mayoría dice intuitivamente ("hay 95% de chance de que la verdadera media esté acá") es la interpretación bayesiana. Es legítima si construiste un **intervalo creíble** bayesiano con un prior explícito. Pero NO es lo que estás calculando cuando hacés un IC frecuentista con la fórmula `media ± 1.96 × EE`.

#### Por qué la confusión es tan común

Porque numéricamente, con priores no informativos y muestras grandes, el IC frecuentista y el intervalo creíble bayesiano dan los mismos números. Entonces la gente piensa "bueno, son lo mismo". Pero **la interpretación cambia radicalmente**, y eso importa cuando alguien te pregunta "¿cuán seguro estás de que la verdadera media está en ese rango?".

#### La trampa típica en el TP

En TP2 Ejercicio 1 reportaste un IC del 95% para la brecha salarial. Si en tu informe escribiste algo como "tenemos 95% de confianza en que la verdadera brecha está entre $348K y $407K", **está mal**. La frase técnicamente correcta es: "construimos el intervalo con un procedimiento que tiene 95% de cobertura nominal". O en lenguaje más accesible: "este es un intervalo de confianza del 95%, calculado con el procedimiento de Welch, y bajo los supuestos del modelo el procedimiento captura la verdadera brecha en el 95% de las muestras".

Es más choto de leer. Pero es lo que estás calculando.

#### Resumen

- En el marco frecuentista, el parámetro es fijo; lo aleatorio es el intervalo.
- "IC al 95%" describe el procedimiento, no este intervalo particular.
- "95% de probabilidad de contener μ" es la interpretación bayesiana (intervalo creíble), NO la frecuentista.
- Numéricamente coinciden con muestras grandes y priores planos, pero la interpretación cambia.

¿Se entiende? Si lo entendiste, ya sabés más de inferencia que la mitad de la gente que reporta intervalos de confianza en papers científicos.

---

## Supuestos y su rol

Todo intervalo reposa sobre supuestos:

**Técnicos**:
- Independencia aproximada entre observaciones.
- Tamaño muestral suficiente para que el TCL funcione.
- Uso razonable de aproximaciones normales o t.

**Sustantivos**:
- Comparabilidad de la muestra (¿realmente estás comparando peras con peras?).
- Criterio de limpieza coherente.
- Variable bien definida.
- Alcance poblacional razonable.

**En la práctica**: el modelo casi nunca es "verdadero" en sentido literal. La pregunta es si es una aproximación útil para responder con honestidad.

---

## Conexión con el TP

- **TP2 Ejercicio 1**: calculaste exactamente esto. Definiste el parámetro de interés (μ_A − μ_B), construiste la muestra analizada, calculaste la estimación puntual ($378.000 aprox), el error estándar de la diferencia, los grados de libertad de Welch, y armaste el IC 95%. Además, interpretaste la magnitud práctica: la diferencia representaba aproximadamente el 34% del salario promedio del grupo B.
- **TP2 Ejercicio 2 (relación IC-test)**: explicitaste que, como el IC no contenía al 0, eso era consistente con rechazar H0 (la hipótesis nula de "no hay diferencia", que veremos en detalle más adelante) al 5%.
- **TP2 Ejercicio 3 (visualización)**: usaste el IC como elemento central de la comunicación: un errorbar que mostraba la estimación y su incertidumbre simultáneamente.

---

## Errores comunes

1. **Confundir desvío estándar con error estándar**: el desvío mide la dispersión de los datos individuales; el error estándar mide la dispersión del promedio.
2. **Creer que el IC "garantiza" que el parámetro está adentro**: no. El parámetro está adentro o no; el 95% se refiere al procedimiento, no a este intervalo particular.
3. **Usar z en lugar de t con muestras chicas**: si n es pequeño y la varianza es desconocida, t es más conservador (intervalos más anchos) y correcto.
4. **Ignorar los supuestos sustantivos**: podés tener un IC perfectamente calculado, pero si tu muestra no es comparable (por ejemplo, mezclás full-time con part-time), el intervalo no responde la pregunta que creés que responde.
5. **Interpretar un IC como prueba de hipótesis automática**: que el IC no contenga al 0 es consistente con rechazar H0, pero no reemplaza la interpretación contextual del tamaño del efecto.

---

## Checklist de comprensión

- [ ] ¿Podés explicar por qué el error estándar de la diferencia usa la raíz de una suma de varianzas?
- [ ] Si duplicás el tamaño muestral de ambos grupos, ¿qué le pasa al ancho del IC (aproximadamente)?
- [ ] En TP2, ¿por qué usaste Welch en lugar de un t-test clásico con varianzas iguales?

---

**Próximo paso**: `05-test-de-hipotesis.md`
