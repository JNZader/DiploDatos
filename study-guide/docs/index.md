# DiploDatos–SAIJ: guía consolidada de estudio por materias

Esta guía reúne las materias de la Diplomatura en un solo libro autocontenido y usa la mentoría de jurisprudencia SAIJ como terreno de aplicación. El orden es deliberado: primero se aprende la teoría de una materia desde sus fundamentos; después se comprueba la comprensión con pausas y ejercicios; recién entonces se trasladan las decisiones al corpus y a los trabajos prácticos.

“Acotado” describe el alcance del proyecto, no la profundidad de la explicación. Por eso el libro no intenta cubrir todas las ramas posibles de ciencia de datos, pero sí desarrolla con paciencia cada concepto incluido: intuición, vocabulario, ejemplos progresivos, errores frecuentes, criterios de interpretación y decisiones que todavía requieren evidencia.

## Navegación del libro

| Materia | Pregunta central | Aplicación en SAIJ | Conexión práctica |
|---|---|---|---|
| **Materia 1 — Análisis y Visualización de Datos** | ¿Qué contienen los datos, cómo se distribuyen y qué conclusiones descriptivas admiten? | Diagnóstico del corpus, poblaciones documentales, distribuciones, sesgos, texto y comunicación de hallazgos. | TP1: comprender y justificar antes de transformar. |
| **Materia 2 — Análisis Exploratorio y Curación de Datos** | ¿Qué decisiones reproducibles convierten el diagnóstico en un dataset apto para un propósito? | Esquema, faltantes, duplicados, categorías, target, texto, features, sesgos, particiones y auditoría. | Preparación detallada para TP2 y para la futura etapa de modelado. |
| **Materia 3 — Introducción al Aprendizaje Automático** | ¿Cómo se aprende una regla a partir de ejemplos y cómo se evalúa sin engañarse? | Formulación y evaluación honesta de la clasificación de fuero sobre una base curada. | Puente detallado desde TP2 hacia representación, entrenamiento, métricas y análisis de errores. |
| **Materia 4 — Aprendizaje Supervisado** | ¿Cómo funcionan y se comparan familias concretas de modelos supervisados? | Selección responsable de clasificadores para el futuro fuero SAIJ, sin proclamar un ganador antes de medir. | Del marco experimental a modelos lineales, árboles, SVM y ensambles. |
| **Materia 5 — Aprendizaje No Supervisado** | ¿Cómo se busca estructura cuando no hay un target externo que organice el aprendizaje? | Exploración temática, similitudes, representaciones, anomalías y candidatos semánticos como apoyo a la revisión jurídica. | Del target conocido al descubrimiento y la evaluación de estructura. |
| **Optativa 1 — Ética práctica** | ¿Qué beneficios, daños, valores y responsabilidades atraviesan cada decisión del ciclo de datos? | Evaluación sociotécnica de SAIJ: privacidad, sesgo, equidad, documentación, auditoría, retrieval y RAG contestable. | Data Statement (Moodle). El Consorcio no es esa entrega. |
| **Optativa 2 — AWS ML Foundations** | ¿Cómo se implementa ML (y gen AI) en AWS sin creer de memoria las cifras de clase? | Transferencia posterior; no es un lab de Academy. | Quizzes de módulo. Leer la parte 2 (verificación) antes de repetir un número. |
| **Optativa 3 — LLMs y modelos generativos** | ¿Dónde corre el modelo (API vs pesos), con qué costo, VRAM y contrato de datos? | Transferencia posterior: fallo con PII ≠ FAQ. | 4 labs = 2 TPs (Perez). El Consorcio no es el práctico de Moodle. |
| **Optativa 4 — Grandes volúmenes (Spark)** | Si no entra en una máquina, ¿cómo se reparte el cómputo sin mover de más los datos? | 874k filas o 35 documentos del canal **no** son el cluster de esta materia. | Notebooks Zeppelin del Bitbucket FAMAF; ejercicios en el note. |
| **Proyecto integrador — búsqueda semántica y RAG** | ¿Cómo recuperar evidencia pertinente antes de generar una respuesta asistida? | Recuperación de documentos SAIJ con representaciones semánticas, filtros de metadatos y evaluación humana. | Próximo paso del proyecto; **no es una materia formal de DiploDatos**. |

## Ruta corta de estudio

En cada materia seguí la misma secuencia:

```text
teoría desde primeros principios
        ↓
checkpoints de comprensión
        ↓
ejercicios conceptuales sin código
        ↓
aplicación razonada a SAIJ
        ↓
conexión con el trabajo práctico
```

No saltees la etapa conceptual. Si una decisión no puede explicarse sin mencionar una función de Python, todavía no está suficientemente entendida. El código implementa un criterio: no lo reemplaza.

## Convención común: cinco troncales + cuatro optativas

A lo largo del libro se distingue entre **teoría general**, **ejemplos ilustrativos inventados**, **hallazgos informados por el notebook del equipo y pendientes de reproducción**, y **decisiones que Javier debe tomar y justificar personalmente**. Esta convención evita convertir resultados ajenos, hipótesis plausibles o simples ejemplos en hechos propios.

---

