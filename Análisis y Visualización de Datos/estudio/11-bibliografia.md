# 11 — Bibliografía y profundización

La bibliografía no es decoración. Cada libro responde un tipo de pregunta distinta. Saber cuál abrir para qué duda te ahorra horas de lectura inútil.

---

## Devore — Probabilidad y Estadística para ingeniería y ciencias

### Qué aporta

- Estructura conceptual clásica y notación estadística precisa.
- Excelente para ordenar la lógica formal: estimador → distribución muestral → error estándar → intervalo → test.
- Ejercicios útiles para afianzar técnica.

### Cuándo ir ahí

- Cuando sentís que entendés la intuición pero te falta orden formal.
- Cuando querés practicar la formulación matemática de problemas.
- Cuando necesitás recordar la derivación exacta de la fórmula del IC o del estadístico t.

### Secciones más relevantes para esta materia

- Capítulos de descriptiva: medidas de centro y dispersión.
- Capítulos de probabilidad: condicional, independencia, Bayes (si querés profundizar).
- Capítulos de inferencia: estimación puntual, intervalos de confianza, tests de hipótesis para una y dos muestras.

---

## Bonamente — Statistics and Analysis of Scientific Data

### Qué aporta

- Mirada analítica y menos recetaria.
- Conexión explícita entre datos, proceso generador y razonamiento inferencial.
- Enfoque en supuestos, ruido, incertidumbre y límites del análisis.

### Cuándo ir ahí

- Cuando querés entender **qué estás asumiendo** al inferir.
- Cuando querés discutir resultados con madurez conceptual.
- Cuando sentís que estás "siguiendo recetas" sin entender por qué.

### Ideas clave de Bonamente para esta materia

1. **Inferir es modelar**: un intervalo de confianza no es un ritual matemático aislado, sino una consecuencia del modelo probabilístico que aceptás usar.
2. **El modelo casi nunca es "verdadero"**: la pregunta no es si el modelo es perfecto, sino si es una aproximación útil.
3. **Ruido vs señal**: la estadística no es solo calcular promedios, es separar lo sistemático de lo aleatorio.

---

## Alberto Cairo — The Truthful Art

### Qué aporta

- Principios de honestidad visual y diseño informativo.
- Herramientas para detectar si un gráfico informa o manipula.
- Lectura crítica de visualizaciones.

### Cuándo ir ahí

- Cuando hacés el **Ejercicio 3 de TP2** (comunicación visual).
- Cuando querés evaluar si un gráfico "convence demasiado" o comunica bien.
- Cuando diseñás un dashboard o una presentación.

### Ideas clave de Cairo para esta materia

1. **Honestidad visual**: un gráfico debe ser proporcional a la evidencia. No exagerar diferencias pequeñas ni ocultar incertidumbre.
2. **El gráfico como argumento**: todo gráfico sugiere una lectura. Ser consciente de esas decisiones no es malo: es profesional.
3. **Alfabetización visual**: el lector necesita ayuda. Títulos informativos, etiquetas claras y notas metodológicas no son "detalles": son obligatorios.

---

## Knaflic — Storytelling with Data

### Qué aporta

- Foco comunicacional práctico.
- Jerarquía visual, reducción de ruido, narrativa con datos.
- Técnicas concretas para transformar un gráfico "correcto" en uno claro.

### Cuándo ir ahí

- Cuando ya tenés el resultado y querés comunicarlo mejor.
- Cuando te preguntás "¿qué le saco a este gráfico?" en lugar de "¿qué le agrego?".
- Cuando preparás una presentación para una audiencia no técnica.

### Ideas clave de Knaflic para esta materia

1. **Reducir ruido**: grillas innecesarias, colores sin función, etiquetas redundantes y adornos decorativos distraen.
2. **Jerarquía visual**: el ojo debe ir primero a lo importante. Usá color, grosor y posición para guiar la atención.
3. **Un mensaje por gráfico**: no intentés decir todo al mismo tiempo. Un gráfico de comunicación = una idea fuerte.

---

## Estrategia sugerida de uso por fase

### Fase 1: Entendiendo la materia (semanas 1-2)

- **Base**: clases + apuntes v2 (archivos 00 a 03).
- **Complemento**: Devore (capítulos de descriptiva y probabilidad).
- **Objetivo**: afianzar intuición y notación.

### Fase 2: Inferencia (semanas 3-4)

- **Base**: clases + apuntes v2 (archivos 04 y 05).
- **Complemento**: Devore (inferencia) + Bonamente (supuestos y modelado).
- **Objetivo**: entender por qué funciona el IC y el test, no solo cómo calcularlos.

### Fase 3: Trabajos prácticos (paralelo a las fases 1 y 2)

- **TP1**: usa los apuntes de descriptiva (03) y limpieza (07). Si querés mejorar los gráficos, mirá Cairo y Knaflic.
- **TP2**: usa los apuntes de inferencia (04, 05) y visualización (06). Bonamente es clave para la sección de supuestos y limitaciones.

### Fase 4: Preparación de exámenes

- **Repaso rápido**: formulario (08) + preguntas guía (10).
- **Profundización**: Bonamente (para discutir supuestos) + Devore (para practicar ejercicios formales).
- **Comunicación**: Cairo + Knaflic (si el examen incluye interpretación de gráficos).

---

## Idea final

La bibliografía complementaria no reemplaza la práctica. Su valor principal es ayudarte a:

1. Entender mejor **por qué** hacés lo que hacés.
2. Distinguir **técnica** de **interpretación**.
3. Evitar análisis correctos en código pero flojos en criterio.

Si leés todo pero no hacés los TPs con las manos, no aprendés. Si hacés los TPs pero no leés nunca, te quedás en la receta. La clave está en alternar: **hacer → dudar → leer → replantear → volver a hacer**.

---

**Fin de los apuntes v2.**

**Recordá**: estos apuntes son una guía, no un reemplazo de tu propio razonamiento. El objetivo es que llegues a un punto donde podás discutir los supuestos, cuestionar las conclusiones, y justificar cada decisión metodológica con la misma claridad con la que escribís código.
