# 02 — Probabilidad básica

## Concepto

La probabilidad cuantifica la incertidumbre. En esta materia no la usamos para jugar a la ruleta: la usamos para entender qué tan probable es que un programador gane más que el promedio, o para decidir si dos eventos están relacionados.

## Intuición

Imaginá que tenés una bolsa con 100 bolitas, cada una representa un encuestado de Sysarmy. Si querés saber "¿qué proporción de programadores gana más de $2M?", no tenés que adivinar: contás cuántas bolitas cumplen esa condición y dividís por 100. Eso es probabilidad frecuentista: la probabilidad de un evento es la proporción de veces que ocurre en tu espacio muestral.

---

## Espacio muestral y eventos

- **Espacio muestral (Ω)**: todos los resultados posibles. En la encuesta, Ω es el conjunto de todas las respuestas.
- **Evento (A)**: un subconjunto de Ω. Por ejemplo: "el salario es mayor al promedio".
- **Probabilidad frecuentista**: si todos los eventos elementales son equiprobables (cada respuesta cuenta igual), entonces:

$$
P(A) = \frac{|A|}{|\Omega|} = \frac{\text{casos favorables}}{\text{casos totales}}
$$

## Ejemplo numérico

Tenés 500 encuestados. El salario promedio neto es $1.000.000.

- Casos que cobran ≥ $1.000.000: 220 encuestados.
- Probabilidad de cobrar ≥ promedio: P(A) = 220 / 500 = 0.44 = 44%.

En Python:
```python
avg_salary = df["salary_monthly_NETO"].mean()
prob_above_avg = (df["salary_monthly_NETO"] >= avg_salary).mean()
# Resultado: 0.44
```

---

## Por qué probabilidad frecuentista no es lo mismo que bayesiana

Acá hay una división filosófica que **arrastra confusiones durante toda la materia** (y, sinceramente, durante toda tu carrera). No es un tecnicismo: cambia qué significa literalmente la palabra "probabilidad".

### Las dos escuelas

**Frecuentista**: la probabilidad de un evento es la **frecuencia relativa a largo plazo**. Si tirás una moneda infinitas veces, la proporción de caras tiende a 0.5. P(cara) = 0.5 significa eso y nada más. La probabilidad **vive en el experimento repetido**, no en tu cabeza.

**Bayesiana**: la probabilidad es un **grado de creencia** sobre algo que no sabés. P(llueve mañana) = 0.7 significa "estoy bastante convencido". La probabilidad **vive en tu estado de información**, y se actualiza con evidencia usando el teorema de Bayes.

### Por qué importa la diferencia

Pensá en esta pregunta: "¿Cuál es la probabilidad de que la verdadera media salarial poblacional sea mayor a $1.500.000?"

- **El frecuentista te dice**: esa pregunta no tiene sentido. La media poblacional es un **número fijo y desconocido**. O es mayor a 1.500.000 o no lo es. Probabilidad 0 o 1, no hay punto medio. Lo único que tiene distribución es **el estimador** (la media muestral), que varía de muestra en muestra.

- **El bayesiano te dice**: la media poblacional es desconocida, así que tengo incertidumbre sobre ella. Esa incertidumbre la represento con una distribución de probabilidad. Combinando mis creencias previas con los datos observados, calculo P(μ > 1.500.000 | datos) = 0.85, por ejemplo.

Las dos posturas son legítimas. Pero **mezclarlas es un error grave** y es lo que casi todo el mundo hace mal.

### Ejemplo numérico: la moneda

Te doy una moneda. La tirás 10 veces y salen 7 caras.

- **Frecuentista**: el estimador puntual de p es 7/10 = 0.7. Un IC del 95% para p sería aproximadamente [0.42, 0.92]. Pero p (la probabilidad poblacional) **es un número fijo**: o es 0.5 o no es 0.5. No tiene "probabilidad".

- **Bayesiano**: arranco con un prior (por ejemplo, una creencia inicial Beta(1,1), que es plana — no sé nada). Después de ver 7 caras y 3 secas, mi creencia se actualiza a una Beta(8,4). Ahora puedo decir cosas como "la probabilidad de que p > 0.5 es 0.89".

Mirá la asimetría: el frecuentista NO PUEDE decir "es 89% probable que la moneda esté cargada". Para él esa frase es literalmente inválida. El bayesiano sí puede decirlo, porque para él la probabilidad mide creencia.

### La trampa más común

La mayoría de la gente **interpreta resultados frecuentistas con lenguaje bayesiano**. Ejemplos:

| Lo que decís (mal) | Lo que realmente significa (bien) |
|---|---|
| "Hay 95% de probabilidad de que la media esté en el IC" | "El procedimiento captura la media en el 95% de las muestras posibles" |
| "Hay 4% de chance de que H0 sea cierta" | "Si H0 fuera cierta, observaríamos datos así de extremos el 4% de las veces" |
| "Hay 0.7 de probabilidad de que la moneda sea justa" | (esto requiere un prior bayesiano explícito; no se obtiene del estimador muestral) |

### Cuál usás en esta materia

En AVD trabajamos con el **enfoque frecuentista**: error estándar, intervalos de confianza al 95%, p-valores, tests de hipótesis. Todo se calcula bajo la lógica de "qué pasaría si repitiéramos la encuesta muchas veces". Eso NO es lo mismo que "qué creo yo sobre el parámetro".

El enfoque bayesiano lo vas a ver más adelante (en materias de aprendizaje automático y especialmente cuando aparezcan modelos jerárquicos o A/B testing serio). Acá lo nombramos para que **no confundas el lenguaje**.

### Resumen

- Frecuentista: la probabilidad es frecuencia a largo plazo. Los parámetros son fijos; lo aleatorio es el estimador.
- Bayesiana: la probabilidad es grado de creencia. Los parámetros tienen distribución; lo "fijo" son los datos observados.
- En TP1/TP2 usás frecuentista, aunque a veces lo describimos con palabras que suenan a creencia. La rigurosidad importa.

¿Se entiende? Si lográs internalizar esta distinción, entender los intervalos de confianza y los p-valores se vuelve mucho menos confuso.

---

## Probabilidad condicional

La probabilidad condicional responde: "¿cuál es la probabilidad de A, sabiendo que ocurrió B?"

### Intuición

Si te dicen "esta persona tiene más de 5 años de experiencia", ¿cambia eso tu estimación de que gane más que el promedio? Si cambia, los eventos no son independientes.

### Fórmula

$$
P(A|B) = \frac{P(A \cap B)}{P(B)} = \frac{|A \cap B|}{|B|}
$$

Donde:
- $P(A|B)$: probabilidad de A dado B.
- $P(A \cap B)$: probabilidad de que ocurran A y B simultáneamente.
- $P(B)$: probabilidad de B (debe ser > 0).

### Ejemplo numérico

Usando los mismos 500 encuestados:
- Personas con > 5 años de experiencia: 300.
- De esas 300, 180 cobran ≥ $1.000.000.

Entonces:
- P(salario ≥ promedio | experiencia > 5) = 180 / 300 = 0.60 = 60%.

Comparación:
- P(salario ≥ promedio) = 44% (sin condicionar).
- P(salario ≥ promedio | exp > 5) = 60% (condicionado).

**Conclusión**: saber que la persona tiene más experiencia aumenta la probabilidad de que cobre más que el promedio. Los eventos NO son independientes.

---

## Independencia

Dos eventos son **independientes** si saber que ocurrió uno no cambia la probabilidad del otro.

### Definición formal

$$
A \perp B \iff P(A|B) = P(A) \iff P(A \cap B) = P(A) \cdot P(B)
$$

### Intuición

Si P(A|B) = P(A), entonces B no me dice nada nuevo sobre A. En la encuesta, si la probabilidad de cobrar bien fuera la misma tanto para juniors como para seniors, entonces "salario alto" y "seniority" serían independientes. Pero no lo son: los seniors cobran más.

### Error común

**Independencia ≠ causalidad inversa**. Que dos variables sean dependientes no significa que una cause a la otra. Puede haber una tercera variable confusora (una variable que afecta a ambas simultáneamente). Por ejemplo: "tener auto propio" y "cobrar más de $2M" son dependientes, pero no porque el auto te haga ganar más: ambos dependen de la edad y la experiencia.

---

## Conexión con el TP

- **TP1 Ejercicio 1, Opción C**: calculaste probabilidades condicionales del tipo P(salario ≥ X | sabe lenguaje L). Por ejemplo: "si sabés Go, tenés un 45% de probabilidad de ganar más de $3M". Eso es probabilidad condicional pura.
- **TP1 Ejercicio 1, Opción C (Lift)**: calculaste el "lift", que es cuánto más probable es un evento condicionado respecto a la probabilidad base. Lift = (P(>X | lenguaje) / P(>X)) - 1. Si el lift es +30%, significa que saber ese lenguaje aumenta en 30% las chances respecto al promedio general.
- **TP1 Ejercicio 2b**: evaluaste si "salario bruto" y "salario neto" son independientes. Spoiler: no lo son, porque uno se calcula a partir del otro. La correlación de Pearson (r ≈ 0.95, que mide la asociación lineal entre dos variables numéricas) cuantifica esa dependencia.

---

## Errores comunes

1. **Confundir P(A|B) con P(B|A)**: P(cobra bien | sabe Python) NO es lo mismo que P(sabe Python | cobra bien). La primera pregunta "de los que saben Python, ¿qué % cobra bien?"; la segunda pregunta "de los que cobran bien, ¿qué % sabe Python?".
2. **Asumir independencia sin verificar**: en datos sociales, casi todo está relacionado con casi todo. No asumas independencia: verificá con los números.
3. **Interpretar probabilidad como certeza**: una probabilidad de 80% no significa "seguro". Significa que, si repitieras la situación muchas veces, en el 80% de los casos ocurriría.
4. **Usar proporciones de subgrupos pequeños**: si un lenguaje tiene solo 20 respuestas y el 80% cobra bien, eso no es tan confiable como un lenguaje con 500 respuestas donde el 45% cobra bien.

---

## Checklist de comprensión

- [ ] ¿Podés explicar con palabras propias por qué P(A|B) puede ser muy distinto de P(B|A)?
- [ ] En TP1, ¿por qué el lift de Go era alto para salarios > $3M pero podía ser diferente para otros umbrales?
- [ ] Si P(salario alto | experiencia > 5) = 60% y P(salario alto) = 44%, ¿qué concluís sobre la relación entre experiencia y salario?

---

**Próximo paso**: `03-descriptiva-visualizacion.md`
