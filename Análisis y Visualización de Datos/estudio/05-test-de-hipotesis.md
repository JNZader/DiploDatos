# 05 — Test de hipótesis

## Concepto

Un test de hipótesis evalúa si la evidencia muestral es lo suficientemente fuerte como para descartar una suposición de referencia (la hipótesis nula). No "prueba" verdades absolutas: mide la tensión entre un modelo simplificado y lo que realmente observaste.

## Intuición

Imaginá que sos juez en un juicio. La ley dice: "presunción de inocencia". Esa es tu H0. Vos ves evidencia (la muestra). Si la evidencia es muy incompatible con la inocencia, rechazás H0 y declarás culpable. Pero tu veredicto no garantiza que la persona sea realmente culpable: garantiza que, si H0 fuera cierta, sería muy raro ver tanta evidencia en su contra. El p-valor es una medida de qué tan "raro" es lo que observaste, asumiendo inocencia.

---

## Esquema general

1. Formular H0 y H1.
2. Elegir un estadístico de prueba.
3. Calcular su valor con la muestra.
4. Obtener un p-valor o región crítica.
5. Decidir si se rechaza H0 al nivel α.

## Hipótesis nula y alternativa

- **H0**: representa el "caso de referencia" o "no hay efecto". Es la suposición que querés desafiar.
- **H1**: representa la diferencia, efecto o desvío que querés detectar.

**Ejemplo típico (TP2)**:
- H0: μ_A − μ_B = 0 (no hay diferencia salarial entre grupos).
- H1: μ_A − μ_B ≠ 0 (hay diferencia salarial).

**Regla de oro**: H0 siempre lleva el signo de igualdad. Es el modelo que asumís para calcular qué tan extremos son tus datos.

## Bilateral vs unilateral

- **Bilateral**: te interesa detectar diferencia en **cualquier dirección**.
  - H1: μ_A − μ_B ≠ 0.
  - Usalo cuando no sabés a priori cuál grupo debería ser mayor.

- **Unilateral**: te interesa detectar diferencia en **una dirección específica**.
  - H1: μ_A − μ_B > 0.
  - Usalo solo cuando tu pregunta original es direccional.

**Cuidado**: no elijas unilateral "después de ver los datos". Esa decisión debe responder a la pregunta de investigación, no al resultado.

## Estadístico de prueba

Es una cantidad calculada con la muestra que mide cuán lejos están los datos de lo esperable bajo H0.

**Ejemplo**: en el test t de Welch:

$$
t = \frac{\bar{x}_A - \bar{x}_B}{EE(\bar{x}_A - \bar{x}_B)}
$$

**Intuición**: si H0 es cierta (no hay diferencia), el numerador debería ser cercano a 0. Si el numerador es grande respecto al denominador (el error estándar), los datos son poco compatibles con H0.

## Nivel de significación (α)

α controla cuánta evidencia exigís para rechazar H0.

- α = 0.05 (5%) es el estándar: estás dispuesto a aceptar un 5% de probabilidad de rechazar H0 cuando en realidad es cierta.
- α = 0.01 (1%) es más estricto: exigís más evidencia, pero también te arriesgás más a no detectar un efecto real.

## Error tipo I y tipo II

| | H0 es cierta | H0 es falsa |
|---|---|---|
| **No rechazamos H0** | ✅ Correcto | ❌ Error tipo II (falso negativo) |
| **Rechazamos H0** | ❌ Error tipo I (falso positivo) | ✅ Correcto |

- **Error tipo I**: rechazar H0 cuando es cierta. La probabilidad de cometerlo está acotada por α.
- **Error tipo II**: no rechazar H0 cuando es falsa. Su probabilidad es β. La **potencia** del test es 1 − β.

**Analogía del juicio**:
- Error tipo I: declarar culpable a un inocente.
- Error tipo II: declarar inocente a un culpable.

## El p-valor

El p-valor mide qué tan compatible es lo observado con H0, bajo el procedimiento usado.

**Interpretación correcta**: "Si H0 fuera cierta, la probabilidad de obtener un estadístico de prueba tan extremo o más extremo que el observado sería p."

**Ejemplo numérico**:
- Calculaste t = 24.5 y el p-valor es 1.2 × 10⁻¹²⁸.
- Significa: si H0 fuera cierta, sería prácticamente imposible ver una diferencia tan grande por azar.

### Qué NO es el p-valor

- ❌ No es la probabilidad de que H0 sea verdadera.
- ❌ No prueba causalidad.
- ❌ No mide importancia práctica.
- ❌ No reemplaza el razonamiento sustantivo.

### Por qué un p-valor de 0.04 NO significa "4% de chance de que H0 sea cierta"

Acá tenemos el malentendido más caro de la estadística aplicada. Te lo voy a desarmar pieza por pieza, porque te garantizo que vas a escucharlo MAL TODA tu vida profesional si no fijás el concepto ahora.

#### Concepto base: el p-valor es una probabilidad CONDICIONAL en una dirección específica

El p-valor responde literalmente esta pregunta: **"Asumiendo que H0 es cierta, ¿cuál es la probabilidad de observar datos tan extremos o más extremos que los míos?"**

En notación: p = P(datos así de extremos | H0 cierta).

Lo que la gente CREE que dice (y NO dice): P(H0 cierta | datos). Esa es la probabilidad inversa.

**P(A|B) ≠ P(B|A)**. Esto lo viste en el capítulo 02, pero acá te pega de frente. Confundir esas dos probabilidades se llama **falacia de la transposición del condicional**, y es la madre de todas las malas interpretaciones de p-valor.

#### El ejemplo del paraguas

Te lo voy a poner con un ejemplo no estadístico para que se vea claro:

- P(uso paraguas | está lloviendo) ≈ 0.95. Si llueve, casi siempre uso paraguas.
- P(está lloviendo | uso paraguas) ≈ 0.30. Puedo usar paraguas porque pronostican lluvia, porque hace mucho sol, porque me da grasa el pelo, etc.

Las dos probabilidades miden cosas distintas. Una NO se deduce de la otra sin más información (necesitarías el teorema de Bayes y, en particular, una probabilidad a priori P(lluvia)).

Lo mismo pasa con el p-valor:
- P(datos extremos | H0 cierta) = 0.04 (esto es el p-valor).
- P(H0 cierta | datos extremos) = ??? (esto NO es el p-valor; ni siquiera se puede calcular sin un prior bayesiano).

#### Por qué la confusión es tan tentadora

Porque parecen "lo mismo" si los datos son extremos. Si el p-valor es chico, intuitivamente sentís que "H0 probablemente sea falsa". Y es verdad — los datos contradicen H0. Pero **cuantificar esa creencia en la H0 requiere un prior**, y los tests frecuentistas NO usan priors.

Tabla comparativa:

| Lo que decís (mal) | Lo que realmente dice el p-valor |
|---|---|
| "Hay 4% de probabilidad de que H0 sea cierta" | "Si H0 fuera cierta, observaríamos datos así de extremos el 4% de las veces" |
| "Hay 96% de probabilidad de que H1 sea verdadera" | (esto requiere bayesiano explícito; no se obtiene del p-valor) |
| "Es probable que el resultado sea real" | "Los datos son inconsistentes con H0 al nivel α=0.05" |

#### El segundo error: significancia estadística ≠ magnitud relevante

Este es el otro lado de la moneda y te lo tenés que tatuar: **un p-valor chico NO te dice cuán grande es el efecto**. Solo te dice cuán incompatibles son los datos con H0.

Con tamaños muestrales enormes (como una encuesta de 5000 personas), **CUALQUIER diferencia mínima va a ser estadísticamente significativa**. Mirá:

| Diferencia real | n por grupo | p-valor típico | ¿Es relevante en la vida real? |
|---|---|---|---|
| $300.000 | 100 | 0.01 | Sí, $300K importa |
| $300.000 | 5.000 | < 0.001 | Sí, sigue importando |
| $5.000 | 100 | 0.65 | No relevante, ni significativo |
| $5.000 | 50.000 | < 0.001 | **Significativo pero IRRELEVANTE**: 5.000 pesos de diferencia no le importa a nadie |

¿Ves la trampa? Con n = 50.000, una diferencia de $5.000 (que en términos prácticos es ruido) sale "estadísticamente significativa al 0.001". Si solo reportás "p < 0.001", suena como un hallazgo importante. **Pero no lo es**.

Por eso siempre tenés que reportar el **tamaño de efecto** (Cohen's d, diferencia absoluta en unidades interpretables, % de cambio relativo) junto con el p-valor. El p-valor te dice "los datos son inconsistentes con H0". El tamaño de efecto te dice "y la inconsistencia es de esta magnitud".

#### La trampa típica en el TP

En TP2 obtuviste un p-valor del orden de 10⁻¹²⁸. Si solo reportás eso, suena como "encontramos algo cósmicamente importante". Pero con n ≈ 1500 por grupo, **casi cualquier diferencia daría p-valores así de chicos**.

Lo que vos hiciste bien fue reportar también **Cohen's d ≈ 0.85** (efecto grande), la **diferencia absoluta ≈ $378.000** (un tercio del salario del grupo B), y el **IC** ([$348.512, $407.488]). Esos tres números, juntos, te dicen "el efecto es real Y es grande". El p-valor solo, te diría "es real" pero te dejaría sin la magnitud.

#### Cuándo el p-valor SÍ es informativo

- Cuando va acompañado del tamaño de efecto y del IC.
- Cuando entendés que mide compatibilidad con H0, no probabilidad de H0.
- Cuando el diseño experimental es razonable (estudios observacionales requieren cautela extra).

#### Cuándo el p-valor te miente

- Cuando lo reportás sin tamaño de efecto.
- Cuando hacés muchos tests y solo reportás el que dio significativo (p-hacking).
- Cuando lo usás para "demostrar" causalidad en datos observacionales.
- Cuando lo interpretás como "probabilidad de H0".

#### Resumen

- p-valor = P(datos extremos | H0). NO es P(H0 | datos).
- Significancia estadística (p < α) **no** implica magnitud relevante.
- Con n grande, todo es significativo. Reportá siempre tamaño de efecto.
- En TP2 hiciste lo correcto: p-valor + Cohen's d + diferencia absoluta + IC. Esa cuarteta es lo mínimo para interpretar honestamente.

¿Se entiende? El p-valor es una herramienta poderosa, pero solo si entendés qué responde exactamente.

## Test para diferencia de medias

### Test t clásico

Asume que ambos grupos tienen varianzas iguales. En la práctica, rara vez sabés eso.

### Test t de Welch

No asume igualdad de varianzas. Es la opción por defecto en datos reales.

**Conexión con TP2**: usaste `stats.ttest_ind(groupA, groupB, equal_var=False)` en el Ejercicio 2. Eso implementa Welch.

## Potencia

La potencia responde: "Si realmente existe un efecto, ¿qué probabilidad tenía el test de detectarlo?"

**Factores que aumentan la potencia**:
1. Mayor tamaño del efecto real.
2. Mayor tamaño muestral.
3. Menor variabilidad en los datos.
4. Nivel de significación α más alto (pero eso también aumenta el error tipo I).

**Ejemplo numérico (TP2)**:
- Cohen's d = 0.85 (efecto grande).
- n observado en grupo A = 1520.
- Potencia observada aproximada (por simulación) = 1.0000.
- Conclusión: la muestra era más que suficiente para detectar este efecto.

## Tamaño de efecto

La significancia estadística no implica importancia práctica. Un efecto puede ser estadísticamente significativo pero trivialmente pequeño (especialmente con muestras enormes).

### Cohen's d

$$
d = \frac{\bar{x}_A - \bar{x}_B}{s_p}
$$

Donde $s_p$ es el desvío estándar combinado (pooled):

$$
s_p = \sqrt{\frac{(n_A - 1)s_A^2 + (n_B - 1)s_B^2}{n_A + n_B - 2}}
$$

**Interpretación aproximada**:
- d ≈ 0.2: efecto pequeño.
- d ≈ 0.5: efecto medio.
- d ≈ 0.8: efecto grande.

**Ejemplo numérico (TP2)**:
- diff = $378.000, s_p ≈ $446.000.
- d = 378.000 / 446.000 ≈ **0.85** → efecto grande.

### Hedges' g

Es una corrección de Cohen's d para sesgo muestral, especialmente útil cuando n es chico:

$$
g = d \times \left(1 - \frac{3}{4(n_A + n_B) - 9}\right)
$$

En muestras grandes (como en TP2), d y g son casi idénticos.

## Relación entre test e intervalo de confianza

Son dos formas de contar la misma historia:

- Si el IC del 95% para la diferencia **no contiene al 0** → consistente con rechazar H0 al 5%.
- Si el IC del 95% **contiene al 0** → consistente con no rechazar H0 al 5%.

**Ejemplo numérico**:
- IC 95% para la diferencia: [$276.000, $481.000].
- Como 0 no está en ese rango, rechazamos H0 al 5%.
- El p-valor del test fue < 0.001, que es consistente con esta conclusión.

## Robustez

Contrastar la conclusión principal con otro método ayuda a evaluar cuánto depende de una formulación específica.

**Chequeos de robustez vistas en TP2**:
1. **Mediana vs media**: la diferencia de medianas también fue positiva.
2. **Test no paramétrico**: Mann-Whitney U (compara rangos entre dos grupos independientes) también dio p-valor significativo.

Si todos los métodos apuntan en la misma dirección, tu conclusión es más sólida.

## ANOVA, Kruskal-Wallis y Chi-cuadrado

Estos tests aparecieron en Clase 4 como extensiones del test t para situaciones más complejas.

### ANOVA (Análisis de Varianza)

Compara las medias de **más de dos grupos** simultáneamente.

- H0: todas las medias son iguales.
- H1: al menos una media es diferente.

**Ejemplo de Clase 4**: comparar el tiempo de respuesta promedio (TAT, *Turnaround Time*) de 4 laboratorios. Un test t por pares sería ineficiente y aumentaría el error tipo I (problema de comparaciones múltiples: a más tests se hacen, más probable es encontrar uno significativo por azar). ANOVA resuelve esto con un solo test.

**Estadístico**: F (de Fisher-Snedecor). Si F es grande y el p-valor es chico, rechazás H0.

### Kruskal-Wallis

Alternativa no paramétrica (que no asume una distribución específica, como la normal) a ANOVA. Compara medianas en lugar de medias. Útil cuando los datos no cumplen la normalidad ni la homogeneidad de varianzas.

### Chi-cuadrado (χ²)

Test para tablas de contingencia (tablas que cruzan frecuencias de dos variables categóricas). Evalúa si dos variables categóricas son independientes.

- H0: las variables son independientes.
- H1: hay asociación entre las variables.

**Ejemplo de Clase 4**: ¿las proporciones de compradores masculinos/femeninos son similares en todas las regiones? Se tabulan las frecuencias observadas y se comparan con las esperadas bajo independencia.

---

## Conexión con el TP

- **TP2 Ejercicio 2**: formulaste H0: μ_A − μ_B = 0 vs H1: μ_A − μ_B ≠ 0. Calculaste el test t de Welch, obtuviste un p-valor extremadamente pequeño, y rechazaste H0 al 5%. Interpretaste el resultado con cautela: "evidencia estadística de diferencia, pero no afirmación causal pura".
- **TP2 Ejercicio 2 (potencia)**: calculaste Cohen's d ≈ 0.85, Hedges' g similar, y la potencia observada ≈ 1.0. Concluiste que la muestra era suficiente.
- **TP2 Ejercicio 2 (robustez)**: verificaste que la diferencia de medianas también era positiva y que el test de Mann-Whitney U también rechazaba H0. Esto fortaleció la conclusión.
- **Clase 4 (ejemplos extra)**: ANOVA para 4 laboratorios, Kruskal-Wallis como alternativa no paramétrica, y Chi-cuadrado para proporciones entre regiones.

---

## Errores comunes

1. **Usar el p-valor como veredicto absoluto**: el p-valor no reemplaza el contexto, el tamaño de efecto ni el diseño del estudio.
2. **Confundir significancia estadística con importancia práctica**: un p-valor de 0.001 con un efecto de $100 pesos puede ser irrelevante en la vida real.
3. **Olvidar que es un análisis bivariado**: en TP2 comparaste salario vs género, pero no controlaste seniority, rol, experiencia ni stack. La diferencia observada puede deberse parcialmente a esas variables.
4. **Elegir unilateral después de ver los datos**: eso es "p-hacking" y invalida tu α.
5. **Ignorar los supuestos del test**: Welch relaja el supuesto de varianzas iguales, pero sigue asumiendo independencia aproximada y tamaños muestrales razonables.
6. **Interpretar el rechazo de H0 como prueba de causalidad**: especialmente en estudios observacionales (como una encuesta voluntaria), el rechazo de H0 no demuestra que el género "cause" la diferencia salarial.

---

## Checklist de comprensión

- [ ] ¿Podés explicar por qué rechazar H0 no es lo mismo que demostrar que tu explicación preferida es la correcta?
- [ ] En TP2, si el p-valor hubiera sido 0.03 pero Cohen's d = 0.05, ¿cómo cambiaría tu interpretación?
- [ ] ¿Por qué usaste Welch en lugar de un t-test clásico? ¿Qué supuesto relaja?

---

**Próximo paso**: `06-visualizacion-y-comunicacion.md`
