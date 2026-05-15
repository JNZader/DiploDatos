# 06 — Visualización y comunicación

## Concepto

No es lo mismo explorar datos que comunicar resultados. Un gráfico exploratorio puede ser feo, denso y caótico: su objetivo es generar preguntas. Un gráfico de comunicación debe ser claro, honesto y centrado en un único mensaje: su objetivo es transmitir una idea.

## Intuición

Imaginá que sos chef. Mientras cocinás, la cocina es un quilombo: probás, tirás, mezclás, ensuciás. Esa es la **exploración**. Pero cuando servís el plato al cliente, lo presentás limpio, con una guarnición elegida y un punto focal. Esa es la **comunicación**. El mismo ingrediente (los datos) cumple roles distintos en cada etapa.

---

## Explorar vs comunicar

| | Explorar | Comunicar |
|---|---|---|
| **Objetivo** | Detectar patrones, anomalías, hacer preguntas | Transmitir una idea principal |
| **Densidad** | Alta: muchos gráficos, mucha información | Baja: un mensaje por gráfico |
| **Público** | Vos mismo (o tu equipo técnico) | Audiencia externa (jefes, clientes, lectores) |
| **Tiempo** | Horas o días | Segundos (debe entenderse a primera vista) |
| **Errores permitidos** | Sí, es un borrador | No, cada elemento debe justificarse |

---

## Qué significa "visualizar bien"

Cuatro condiciones mínimas:

1. **Fidelidad**: el gráfico debe ser proporcional a los datos. No exagerar diferencias pequeñas ni ocultar incertidumbre.
2. **Claridad**: se entiende rápidamente, sin manual de instrucciones.
3. **Eficiencia**: comunica la idea principal sin distracciones.
4. **Contexto**: incluye información suficiente para no inducir interpretaciones engañosas.

## Aportes de Alberto Cairo

### Honestidad visual

Un gráfico debe ser proporcional a la evidencia. No conviene:
- Cortar el eje Y para que una diferencia del 2% parezca del 200%.
- Usar áreas o volúmenes en lugar de longitudes (el ojo humano juzga mal las áreas).
- Ocultar incertidumbre relevante.

### Por qué un gráfico con eje Y truncado MIENTE (con cuentas)

Acá hay un truco que **todos los medios y casi todos los infográficos políticos usan**, y la gente no lo nota porque no le enseñaron a leer ejes. Vamos a desarmarlo.

#### Concepto base: el ojo lee proporciones de longitud, no valores absolutos

Cuando miras un gráfico de barras, tu cerebro estima la **diferencia relativa** comparando longitudes. Si una barra es el doble de larga que otra, intuitivamente concluís que el valor es el doble. Esto está hardcodeado en cómo el cerebro humano procesa magnitudes visuales (de hecho, es uno de los canales visuales más precisos, como vimos en la sección anterior).

Pero esa intuición ASUME que el eje Y arranca en 0. Si no arranca en 0, la longitud de la barra ya no es proporcional al valor: es proporcional al valor **menos el origen del eje**. Y ahí empieza la mentira.

#### El experimento numérico: ventas de dos sucursales

Sucursal A vendió $1.000.000 este mes. Sucursal B vendió $1.010.000. Diferencia real: 1%.

**Gráfico honesto (eje Y empieza en 0)**:

```
Y
1.200.000 |
1.000.000 |  ████   ████
  800.000 |  ████   ████
  600.000 |  ████   ████
  400.000 |  ████   ████
  200.000 |  ████   ████
        0 |__████___████___
            A       B
```

Las dos barras se ven prácticamente iguales. El lector concluye: "ventas similares". Que es la verdad.

**Gráfico truncado (eje Y empieza en 990.000)**:

```
Y
1.020.000 |          ████
1.010.000 |          ████
1.000.000 |  ████    ████
  990.000 |__████____████___
            A        B
```

La barra B es **tres veces más larga** que la A en el gráfico. El lector concluye: "B vendió tres veces más que A". Que es FALSO. La diferencia real es del 1%, pero visualmente se exagera a 300%.

#### El cálculo del factor de exageración

Si el eje Y empieza en `y_min` en lugar de 0, y los valores reales son `v_A` y `v_B`, la exageración es:

$$
\text{exageración} = \frac{(v_B - y_{\min}) / (v_A - y_{\min})}{v_B / v_A}
$$

Con v_A = 1.000.000, v_B = 1.010.000, y_min = 990.000:

- Ratio real: 1.010.000 / 1.000.000 = 1.01 (1% más).
- Ratio visual: (1.010.000 - 990.000) / (1.000.000 - 990.000) = 20.000 / 10.000 = 2.0 (¡el doble!).
- Factor de exageración: 2.0 / 1.01 ≈ **198x**.

Una variación del 1% se VE como una variación del 100%. Esto se llama **lying with a truncated axis** y es probablemente la mentira gráfica más común del mundo.

#### Cuándo SÍ podés truncar el eje

Hay casos legítimos. No es una regla absoluta:

| Tipo de gráfico | ¿Truncar es honesto? | Por qué |
|---|---|---|
| Barras | ❌ Casi nunca | La longitud comunica magnitud |
| Líneas (series temporales) | ✅ A veces | El énfasis está en la **tendencia**, no en la magnitud absoluta |
| Puntos con barras de error | ✅ Sí, si lo aclarás | El foco es la posición relativa entre puntos |
| Áreas | ❌ Nunca | El área visual debe ser proporcional al valor |

Para series temporales (gráfico de líneas), truncar el eje puede ser útil para resaltar variaciones. Pero entonces **debés** indicar el origen del eje explícitamente, o usar una marca de "axis break" (una linea zigzagueante que muestra que el eje saltea valores).

#### La regla rioplatense

Si tu intención es que el lector entienda **magnitudes**, el eje Y arranca en 0. Punto.

Si tu intención es que el lector entienda **variaciones** (subió, bajó, mismo nivel), podés truncar pero TENÉS QUE AVISAR. Una nota al pie, una marca de corte en el eje, un subtítulo que diga "eje Y desde X para resaltar variación". Sin esa transparencia, estás mintiendo.

#### La trampa típica en el TP

En TP2 Ejercicio 3 tu gráfico de la diferencia salarial con IC del 95% usaba un **errorbar horizontal**. El eje X arrancaba abajo de 0 (en negativo) y subía por arriba del IC superior. Esto es importante: si hubieras truncado el eje X y solo mostrado el rango [$348K, $407K], el lector vería un IC enorme y centrado, sin entender que la línea del 0 quedaba MUY lejos del intervalo.

El truco honesto es **incluir el 0 en el rango visible** cuando el 0 es la referencia (en este caso, "no hay diferencia"). Así el lector ve de un vistazo cuán lejos del 0 está tu estimación.

#### Resumen

- El ojo lee proporciones de longitud; truncar el eje rompe esa lectura.
- Una variación del 1% puede parecer 100% con un eje truncado.
- En barras, el eje Y arranca en 0. Sin excusas.
- En líneas y puntos, podés truncar si declarás el origen y la razón.
- En TP2, el errorbar horizontal incluía el 0 explícitamente: eso es lo que lo hacía honesto.

¿Se entiende? La próxima vez que un infográfico de noticias te muestre una "diferencia espectacular", mirá el eje Y antes de creerle.

### El gráfico como argumento

Todo gráfico sugiere una lectura. No es neutral: decidís qué comparar, qué resaltar y qué dejar de fondo. Eso no es malo, pero tenés que ser consciente de esas decisiones.

### Alfabetización visual

Leer gráficos requiere entrenamiento. Cuando el mensaje es importante, ayudá al lector con:
- Títulos informativos (no descriptivos).
- Etiquetas claras.
- Notas metodológicas breves.
- Texto interpretativo.

## Aportes de Knaflic (Storytelling with Data)

### Reducir ruido

Muchas veces mejorar un gráfico no es agregar, sino sacar:
- Grillas innecesarias.
- Colores sin función.
- Etiquetas redundantes.
- Adornos decorativos (3D, sombras, gradientes).

### Jerarquía visual

No todo debe llamar la atención por igual. El ojo debe ir primero a lo importante. Usá:
- Color de destaque para el dato clave.
- Grosor de líneas.
- Tamaño de texto.
- Contraste.

**Regla práctica**: si sacás un elemento y el mensaje no cambia, sacalo.

## Canales visuales y efectividad

Para comparación cuantitativa, del más preciso al menos preciso:

1. **Posición sobre un eje común** (más preciso).
2. **Longitud** (barras).
3. **Ángulo** (menos preciso).
4. **Área / volumen** (muy impreciso).
5. **Color saturación** (útil para categorías, no para magnitudes).

**Consecuencia**: para comparar valores numéricos, usá barras o puntos sobre eje. Evitá tortas (pies) y gráficos 3D.

## Títulos y subtítulos

Un título neutro no ayuda:
- ❌ "Gráfico de salarios"
- ✅ "La diferencia estimada de salario medio permanece positiva incluso con incertidumbre muestral"

El subtítulo agrega contexto:
- "Muestra: trabajadores Full-Time, encuesta Sysarmy 2026. Filtros: salarios entre $300K y $20M, outliers removidos por IQR."

## Visualización de inferencia

Cuando hay inferencia, mostrá no solo el valor estimado sino también su incertidumbre:

- **Intervalos de confianza**: barras de error horizontales o verticales.
- **Bandas de confianza**: en series temporales.
- **Notas explícitas**: "IC 95% calculado con aproximación t de Welch."

**Ejemplo numérico (TP2 Ejercicio 3)**:
- Estimación puntual: $378.000.
- IC 95%: [$276.000, $481.000].
- Gráfico: un punto en $378.000 con una barra horizontal que va de $276K a $481K, y una línea punteada en 0 como referencia.

**Por qué funciona**: en una sola imagen comunicás tres cosas: la dirección del efecto, su magnitud aproximada, y la incertidumbre. Si todo el IC queda del mismo lado de 0, el lector ve inmediatamente que la diferencia es robusta.

## Cómo elegir un gráfico

| Querés mostrar... | Usá... |
|---|---|
| Comparar magnitudes | Barras, puntos sobre eje común |
| Mostrar distribución | Histograma, boxplot, violinplot |
| Mostrar relación entre dos numéricas | Scatterplot |
| Comunicar estimación + incertidumbre | Punto con barra de error |
| Relación entre dos categóricas | Tabla de contingencia, heatmap |
| Tres variables (2 numéricas + 1 categórica) | Scatterplot con hue |

## Riesgos frecuentes

1. **Saturación**: demasiadas variables o capas vuelven el gráfico ilegible.
2. **Escalas engañosas**: cambiar el origen del eje Y puede exagerar o minimizar diferencias.
3. **Color sin función**: usar muchos colores porque sí distrae más de lo que ayuda.
4. **Falta de contexto**: un valor aislado sin comparación ni fuente presta a malas lecturas.
5. **Confundir precisión con persuasión**: que un gráfico sea impactante no implica que sea honesto.

---

## Conexión con el TP

- **TP1 (todos los ejercicios)**: usaste gráficos exploratorios. Boxplots, violinplots, KDEs, pairplots, scatterplots. Estaban bien porque tu objetivo era entender, no presentar. La clave es no pedirle a un gráfico exploratorio que cumpla el papel de un gráfico de presentación.
- **TP1 Ejercicio 1, Opción A**: el boxplot ordenado por mediana fue un gráfico exploratorio muy eficiente: permitió comparar 10+ lenguajes de un vistazo.
- **TP2 Ejercicio 3**: este fue el ejemplo puro de **comunicación**. Elegiste un único mensaje (la diferencia estimada con su IC), usaste un gráfico minimalista (errorbar horizontal), eliminaste todo lo innecesario (incluso el eje Y), y agregaste una interpretación textual prudente.
- **TP2 Ejercicio 3 (título)**: "Estimación de la brecha salarial media con IC del 95%" ya adelanta la lectura. No es neutral: guía al lector.

---

## Errores comunes

1. **Usar un gráfico exploratorio como comunicación final**: un pairplot con 15 variables es útil para vos, inútil para una presentación.
2. **Omitir la incertidumbre**: mostrar solo la estimación puntual sin el IC es como mostrar solo la punta del iceberg.
3. **Títulos descriptivos en lugar de interpretativos**: "Gráfico de salarios" no dice nada. "La brecha salarial se mantiene positiva incluso considerando incertidumbre muestral" sí.
4. **3D decorativo**: agrega ruido visual sin información. El ojo humano no juzga bien volúmenes en perspectiva.
5. **No justificar filtros en el subtítulo**: si filtraste outliers o te quedaste con Full-Time, el lector necesita saberlo para interpretar correctamente.

---

## Checklist de comprensión

- [ ] ¿Podés explicar la diferencia entre un gráfico exploratorio y uno de comunicación usando los ejemplos de TP1 y TP2?
- [ ] Si tuvieras que comunicar el resultado de TP2 a un público no técnico, ¿qué elementos sacarías del gráfico y cuáles agregarías?
- [ ] ¿Por qué en TP2 usaste un errorbar horizontal en lugar de un boxplot para el Ejercicio 3?

---

**Próximo paso**: `07-limpieza-y-calidad-de-datos.md`
