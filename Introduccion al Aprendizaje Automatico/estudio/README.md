# Introducción al Aprendizaje Automático — Estudio

> Apuntes pedagógicos para la materia **Introducción al Aprendizaje Automático** (IAA) de la Diplomatura en Ciencia de Datos, UNC-FAMAF 2026 (docentes: Meinardi & Bonzi). Cubre las Clases 1 y 2 + TP1 (California Housing).

## ¿Qué hay acá?

Esta carpeta es una reconstrucción pedagógica del módulo IAA. No es un copy-paste de las clases ni un reemplazo del material de cátedra: es una reorganización pensada para que entiendas el **porqué** antes del **cómo**, y para que cada concepto se conecte de forma directa con el TP1. Cada capítulo está enriquecido con bibliografía canónica (Bishop, Murphy, Hastie–Tibshirani–Friedman, Karpathy) además del PDF y los notebooks oficiales.

El recorrido es lineal: del marco general (qué es ML, qué tipos hay, cómo se entrena) a los modelos puntuales (regresión, perceptrón, logística, Naive Bayes, KNN, estrategias multiclase). Cada capítulo cierra con una conexión explícita al ejercicio del TP1 al que toca. Los archivos 11-14 son utility (glosario, formulario, preguntas-guía, bibliografía) y se consultan en cualquier momento; el 15 es la guía completa del TP1 ejercicio por ejercicio.

## Mapa de clases → archivos

| Clase | Temas | Archivos del estudio |
|-------|-------|----------------------|
| Pre-clase 1 | Refresher Python/NumPy/sklearn (gotchas técnicos del TP) | 00 |
| Clase 1 | Marco general + Pipeline + Regresión (lineal/polinomial/Ridge) + Clasificación/Perceptrón | 01, 02, 03, 04, 05, 06 |
| Clase 2 | Logística + Naive Bayes + KNN + Multiclase | 07, 08, 09, 10 |

## Mapa de TPs → archivos

| TP | Temas que toca | Guía paso a paso |
|----|----------------|------------------|
| **TP1 — California Housing** | Regresión lineal univariada, polinomial, multivariada (5 features + todas), Ridge (opcional) | [`15-guia-de-tp1.md`](15-guia-de-tp1.md) |
| TP2 | (Pendiente — material no cargado aún) | — |

El TP1 tiene 7 ejercicios: 5 obligatorios (Ej1–Ej5) + 2 opcionales (Ej6 "A Todo Feature", Ej7 Ridge). El detalle ejercicio por ejercicio está en el archivo 15.

## Estructura de cada capítulo (estilo v2)

Todos los archivos temáticos (00-10) siguen el mismo patrón pedagógico:

1. **Concepto** — definición precisa con cita al material original (PDF de cátedra o bibliografía).
2. **Intuición** — analogía memorable antes de la fórmula.
3. **Cuerpo técnico** — desarrollo formal con fórmulas, derivaciones y supuestos explícitos.
4. **Ejemplo numérico** — datos concretos, no solo variables abstractas.
5. **Conexión con el TP** — qué ejercicio del TP1 toca este tema.
6. **Errores comunes** — los gotchas que la cátedra detecta seguido.
7. **Checklist de comprensión** — 3-5 preguntas para autoevaluarte.
8. **Para profundizar** — lecturas sugeridas (con sección y rango de páginas).
9. **Próximo paso** — link al siguiente capítulo con un anticipo de qué se construye sobre lo recién visto.
10. **Referencias** — bibliografía con URLs verificadas (mayo 2026).

Los archivos 11-15 son utility (glosario, formulario, preguntas, bibliografía, guía de TP) y siguen el formato propio de su tipo.

## Índice completo

| Orden | Archivo | Título | Qué cubre |
|-------|---------|--------|-----------|
| 00 | [`00-python-y-numpy-para-ml.md`](00-python-y-numpy-para-ml.md) | Python y NumPy para Machine Learning | Refresher táctico: vectorización, broadcasting, shapes, sklearn output_config, trampa DataFrame vs ndarray |
| 01 | [`01-marco-general-aa.md`](01-marco-general-aa.md) | Marco general del Aprendizaje Automático | Qué es ML (vs "programar"), familias de aprendizaje (supervisado, no supervisado, refuerzo), supuestos |
| 02 | [`02-pipeline-de-entrenamiento.md`](02-pipeline-de-entrenamiento.md) | El pipeline de entrenamiento | Particiones, función de costo, iteración, monitoreo, evaluación — la infraestructura sobre la que se montan TODOS los modelos |
| 03 | [`03-regresion-lineal.md`](03-regresion-lineal.md) | Regresión Lineal | Modelo lineal, mínimos cuadrados (MSE), ecuación normal, solución cerrada |
| 04 | [`04-regresion-polinomial.md`](04-regresion-polinomial.md) | Regresión Polinomial | Extensión polinomial $\phi_j(x)=x^j$, capacidad del modelo, overfit cuando $M$ crece |
| 05 | [`05-regularizacion-ridge.md`](05-regularizacion-ridge.md) | Regularización Ridge (L2) | Penalización L2 sobre $\mathbf{w}$, solución cerrada Ridge ($\mathbf{X}^\top\mathbf{X}+\lambda\mathbf{I}$), comparación con Lasso |
| 06 | [`06-clasificacion-y-perceptron.md`](06-clasificacion-y-perceptron.md) | Clasificación y Perceptrón | De la regresión a la decisión, frontera lineal, regla del perceptrón, límites (no probabilidad, no convergencia si no es separable) |
| 07 | [`07-regresion-logistica.md`](07-regresion-logistica.md) | Regresión Logística | Sigmoide, log-verosimilitud, gradiente, decisión suave probabilística vs decisión dura del perceptrón |
| 08 | [`08-naive-bayes.md`](08-naive-bayes.md) | Naive Bayes | Enfoque generativo, supuesto de independencia condicional, variantes (Gaussian, Multinomial, Bernoulli), por qué funciona bien en texto |
| 09 | [`09-knn-y-no-parametricos.md`](09-knn-y-no-parametricos.md) | KNN y modelos no paramétricos | Vecinos más cercanos, distancia, $k$ como hiperparámetro, paramétricos vs no paramétricos |
| 10 | [`10-multiclase.md`](10-multiclase.md) | Multiclase: estrategias y softmax | OVA, OVO, softmax, qué modelos son naturalmente multiclase (KNN, NB) y cuáles requieren wrapper (SVM, logística binaria) |
| 11 | [`11-glosario.md`](11-glosario.md) | Glosario | 10 grupos temáticos, términos con definición + capítulo donde se desarrolla |
| 12 | [`12-formulario.md`](12-formulario.md) | Formulario | Fórmulas con expresión LaTeX + variables + cuándo usar + trampa común |
| 13 | [`13-preguntas-guia.md`](13-preguntas-guia.md) | Preguntas-guía de auto-examen | Preguntas sin respuesta — la idea es que respondas vos y compares con el material |
| 14 | [`14-bibliografia.md`](14-bibliografia.md) | Bibliografía y recursos externos | Guía de USO (no listado pasivo): qué cubre, para qué capítulo sirve, nivel, gratis/pago |
| 15 | [`15-guia-de-tp1.md`](15-guia-de-tp1.md) | Guía paso a paso del TP1 | California Housing, ejercicio por ejercicio, con criterios de evaluación y trampas detectadas |

## Caminos sugeridos

**Camino 1 — Sin background previo en ML**:
00 → 01 → 02 → 03 → 04 → 05 → 15 (TP1) → 06 → 07 → 08 → 09 → 10. Es el recorrido completo en orden. Bancate los capítulos 01 y 02 antes de saltar a los modelos: sin esa base, los algoritmos siguientes se sienten como recetas mágicas.

**Camino 2 — Con base de estadística / cálculo**:
01 → 03 → 04 → 05 → 15 (TP1) → 06 → 07 → 08 → 09 → 10. Saltás el cap. 00 (refresher Python) y el 02 (pipeline) los leés en diagonal — ya manejás cross-validation, train/test split, MSE.

**Camino 3 — Foco en aprobar TP1 (timeline corto)**:
03 → 04 → 05 → 15. Si tenés muy poco tiempo, atacá el TP1 desde la guía, con los capítulos 03-05 como soporte conceptual. El glosario (11) y el formulario (12) son referencia de consulta puntual.

**Camino 4 — Repaso para parcial / coloquio**:
Leé el glosario (11) tapando las definiciones. Respondé el banco de preguntas (13) en papel. Si dudás, volvé al capítulo temático correspondiente. Cerrá con el formulario (12) para tener las fórmulas frescas.

## Material complementario

- **Glosario** [`11-glosario.md`](11-glosario.md) — 10 grupos temáticos, términos definidos como aparecen en el PDF de cátedra + notebooks.
- **Formulario** [`12-formulario.md`](12-formulario.md) — fórmulas en LaTeX con explicación de variables, cuándo usar cada una y trampa común asociada.
- **Preguntas guía** [`13-preguntas-guia.md`](13-preguntas-guia.md) — banco de auto-examen sobre caps 00-10 + TP1. **No incluye respuestas** por diseño: la idea es que respondas vos y verifiques contra el material.
- **Bibliografía** [`14-bibliografia.md`](14-bibliografia.md) — guía de uso de Bishop (PRML), Murphy (PML), HTF (ESL), Karpathy y cursos online, con sección/rango de páginas mapeados a cada capítulo.

## Reglas de oro

1. **Concepto antes que código.** No toques `LinearRegression().fit()` sin entender qué hace, qué supuestos asume y por qué la ecuación normal $\mathbf{w}=(\mathbf{X}^\top\mathbf{X})^{-1}\mathbf{X}^\top\mathbf{y}$ es la solución cerrada. Si solo copiás el snippet, el modelo "anda" pero no podés defender una sola decisión técnica.
2. **Verificá con datos, no con corazonadas.** Toda elección (qué grado polinomial, qué $\lambda$, qué $k$ en KNN) debe poder defenderse con una curva de validación o un número concreto. La pregunta del docente nunca es "qué pusiste", es "por qué pusiste eso".
3. **Trampa DataFrame vs ndarray.** sklearn moderno (≥ 1.2) puede devolver DataFrame si se configura `set_config(transform_output="pandas")`. Si tu código asume indexing estilo ndarray (`X[:, selector]`) y el pipeline previo devuelve DataFrame, vas a romper sin error claro. Documentado en el cap. 00 y reiterado en el cap. 15 (es la causa #1 por la que los alumnos se traban en el Ejercicio 2 del TP1).
4. **El cap superior en 5.0 del California Housing es un sesgo, no un dato.** Las viviendas que valían más de 500k aparecen agrupadas en `y=5.0` por la convención del censo. Se ve como una barra horizontal en los scatters. Mencionalo en el Ejercicio 1 — la cátedra lo evalúa.
5. **Justificación > resultado.** El TP1 no busca un único MSE "correcto". Busca que defiendas: por qué este split, por qué este grado, por qué Ridge y no Lasso, por qué esta semilla, qué hiciste con los outliers. Sin justificación, el resultado vale poco.

## Notas sobre el material original

Los apuntes están construidos sobre el PDF de cátedra (Clases 1 y 2) + los notebooks oficiales del curso. Las clases originales (PPTX/PDF) y los notebooks de cátedra viven en el repo privado [`DiploDatos-clases/`](https://github.com/JNZader/DiploDatos-clases) por razones de copyright. Esta carpeta `estudio/` es la versión pública pedagógica derivada — no contiene material protegido literal, solo referencias citadas y desarrollo propio.

## Próximos pasos (cuando llegue material nuevo)

- Cuando se cargue **Clase 3** → agregar capítulos correspondientes (probablemente: árboles, ensembles, SVM o redes neuronales según el cronograma).
- Cuando se cargue **TP2** → agregar `15b-guia-de-tp2.md` y actualizar el mapa de TPs en este README.
- Si se agregan **ejercicios opcionales con datasets nuevos** → documentar en el cap correspondiente.

---

*Estudio generado iterativamente con sub-agentes redactores en paralelo. Estilo pedagógico v2 (mismo formato que AVD y EyCD). Última actualización: 2026-05-23.*
