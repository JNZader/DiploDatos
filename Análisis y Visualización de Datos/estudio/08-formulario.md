# 08 — Formulario

Este formulario no es una lista de símbolos sueltos. Cada fórmula viene con: (a) qué significa cada letra, (b) cuándo usarla, y (c) una advertencia sobre su uso.

---

## Descriptiva

### Media muestral

$$
\bar{x} = \frac{1}{N} \sum_{i=1}^{N} x_i
$$

- **x̄** = media muestral (estimador del centro).
- **N** = cantidad de observaciones.
- **xᵢ** = valor de la i-ésima observación.
- **Usala cuando**: la distribución es aproximadamente simétrica y no hay outliers graves.
- **No la uses sola**: siempre acompañala con una medida de dispersión.

### Varianza muestral

$$
s^2 = \frac{1}{N-1} \sum_{i=1}^{N} (x_i - \bar{x})^2
$$

- **s²** = varianza muestral.
- **Usamos N−1** (no N) porque es un estimador insesgado de la varianza poblacional σ².
- **Usala cuando**: necesitás una medida de dispersión para cálculos posteriores (como el error estándar).

### Desvío estándar muestral

$$
s = \sqrt{s^2}
$$

- **s** = desvío estándar. Tiene las mismas unidades que los datos.
- **Interpretación**: distancia "típica" entre cada dato y la media.

### Coeficiente de variación (CV)

$$
CV = \frac{s}{\bar{x}}
$$

- **Usala cuando**: querés comparar la dispersión de variables con escalas distintas.
- **Ejemplo**: ¿el salario es más variable que la edad? Compará sus CVs.

### Percentil k

$$
P_k = \text{valor tal que el } k\% \text{ de los datos es menor}
$$

- **Q1** = P₂₅, **Q2 (mediana)** = P₅₀, **Q3** = P₇₅.

### IQR (Rango Intercuartílico)

$$
IQR = Q3 - Q1
$$

- **Usala cuando**: necesitás una medida de dispersión robusta a outliers.
- **Outliers por IQR**: cualquier valor < Q1 − 1.5×IQR o > Q3 + 1.5×IQR.

---

## Probabilidad

### Probabilidad frecuentista

$$
P(A) = \frac{|A|}{|\Omega|} = \frac{\text{casos favorables}}{\text{casos totales}}
$$

- **Usala cuando**: todos los casos son equiprobables (encuesta con respuestas ponderadas igual).

### Probabilidad condicional

$$
P(A|B) = \frac{P(A \cap B)}{P(B)} = \frac{|A \cap B|}{|B|}
$$

- **Usala cuando**: querés restringir el análisis a un subgrupo.

### Independencia

$$
A \perp B \iff P(A \cap B) = P(A) \cdot P(B)
$$

---

## Inferencia: estimación

### Error estándar de la media

$$
EE(\bar{x}) = \frac{s}{\sqrt{n}}
$$

- **s** = desvío estándar muestral.
- **n** = tamaño muestral.
- **Interpretación**: "temblor típico" del promedio si repitieras la muestra.

### Error estándar de la diferencia de medias (Welch)

$$
EE(\bar{x}_A - \bar{x}_B) = \sqrt{\frac{s_A^2}{n_A} + \frac{s_B^2}{n_B}}
$$

- **Usala cuando**: comparás dos grupos independientes y no asumís varianzas iguales.
- **Advertencia**: no es la resta de errores estándar, es la raíz de una suma de varianzas.

### Grados de libertad de Welch-Satterthwaite

$$
df = \frac{\left(\frac{s_A^2}{n_A} + \frac{s_B^2}{n_B}\right)^2}{\frac{(s_A^2/n_A)^2}{n_A - 1} + \frac{(s_B^2/n_B)^2}{n_B - 1}}
$$

- **Usala cuando**: hacés un IC o test t de Welch.
- **No memorices la fórmula**: entendé que ajusta los grados de libertad por la diferencia de varianzas entre grupos.

### Intervalo de confianza (diferencia de medias, Welch)

$$
IC = (\bar{x}_A - \bar{x}_B) \pm t_{1-\alpha/2, df} \times EE(\bar{x}_A - \bar{x}_B)
$$

- **t₁₋ₐ/₂, df** = valor crítico de la distribución t para el nivel de confianza deseado.
- **α** = nivel de significación (0.05 para 95% de confianza).
- **Usala cuando**: querés cuantificar la incertidumbre de una diferencia observada.

---

## Inferencia: test de hipótesis

### Estadístico t de Welch

$$
t = \frac{\bar{x}_A - \bar{x}_B}{EE(\bar{x}_A - \bar{x}_B)}
$$

- **Interpretación**: cuántas veces el error estándar "cabe" en la diferencia observada. Si es grande, la diferencia es poco compatible con H0.

### Decisión con p-valor

- Si **p-valor < α** → rechazamos H0.
- Si **p-valor ≥ α** → no rechazamos H0 (no "aceptamos" H0).

### Tamaño de efecto: Cohen's d

$$
d = \frac{\bar{x}_A - \bar{x}_B}{s_p}
$$

Donde el desvío combinado es:

$$
s_p = \sqrt{\frac{(n_A - 1)s_A^2 + (n_B - 1)s_B^2}{n_A + n_B - 2}}
$$

- **Interpretación aproximada**: 0.2 = pequeño, 0.5 = medio, 0.8 = grande.
- **Usala cuando**: querés estandarizar la magnitud de una diferencia para compararla entre estudios.

### Hedges' g (corrección por sesgo)

$$
g = d \times \left(1 - \frac{3}{4(n_A + n_B) - 9}\right)
$$

- **Usala cuando**: n es pequeño. En muestras grandes, g ≈ d.

---

## Visualización y resumen

### Correlación de Pearson

$$
r = \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum (x_i - \bar{x})^2 \sum (y_i - \bar{y})^2}}
$$

- **Rango**: −1 a +1.
- **Usala cuando**: ambas variables son numéricas y la relación es aproximadamente lineal.
- **No uses cuando**: hay outliers fuertes o la relación es claramente curva. Usá Spearman en esos casos.

### R² (coeficiente de determinación)

$$
R^2 = r^2
$$

- **Interpretación**: proporción de la varianza de Y explicada linealmente por X.
- **Ejemplo**: r = 0.95 → R² = 0.9025 → el 90.25% de la variación de Y se "explica" por X.

---

## Recordatorios conceptuales (para no olvidar)

- **Significancia estadística ≠ importancia práctica**. Un p-valor chico con un efecto trivial no cambia el mundo.
- **Correlación ≠ causalidad**. r = 0.95 entre bruto y neto no significa que "aumentar el bruto cause que aumente el neto" en un experimento: es una relación contable.
- **Muestra grande ≠ muestra representativa**. Una encuesta con 100.000 respuestas sesgadas sigue siendo sesgada.
- **Intervalo de confianza ≠ probabilidad de que el parámetro esté adentro**. El parámetro es fijo; lo aleatorio es el intervalo.
- **Rechazar H0 ≠ demostrar tu explicación favorita**. H0 es solo una suposición de referencia.

---

**Próximo paso**: `09-glosario.md`
