# Apuntes de estudio v2 — Análisis y Visualización de Datos

## Qué son estos apuntes

Esta es una reformulación pedagógica de los temas de la materia. No es un copy-paste de las clases: es una reconstrucción pensada para que entiendas el **porqué** antes del **cómo**, y para que cada concepto se conecte con los trabajos prácticos que ya hiciste.

## Estructura y progresión lógica

Los archivos están ordenados para que no te encuentres con un p-valor antes de saber qué es una hipótesis. La regla es: cada archivo depende de los anteriores.

| Orden | Archivo | Qué cubre | Depende de |
|-------|---------|-----------|------------|
| 0 | `00-python-y-pandas.md` | Python para análisis de datos: DataFrames, lectura de CSV, tipos de datos computacionales vs estadísticos | Nada |
| 1 | `01-eda-y-tipos-de-datos.md` | Qué es el EDA, tipos de variables, primeras preguntas frente a un dataset | 00 |
| 2 | `02-probabilidad-basica.md` | Probabilidad frecuentista, probabilidad condicional, independencia | 01 |
| 3 | `03-descriptiva-visualizacion.md` | Medidas de resumen, gráficos exploratorios, relaciones entre variables | 01, 02 |
| 4 | `04-estimacion-e-inferencia.md` | Población vs muestra, estimadores, error estándar, TCL, intervalos de confianza | 03 |
| 5 | `05-test-de-hipotesis.md` | Hipótesis nula y alternativa, p-valor, errores tipo I/II, potencia, tamaño de efecto, robustez | 04 |
| 6 | `06-visualizacion-y-comunicacion.md` | Explorar vs comunicar, principios de Cairo y Knaflic, honestidad visual, incertidumbre | 03, 05 |
| 7 | `07-limpieza-y-calidad-de-datos.md` | Criterios de limpieza, tratamiento de faltantes, outliers, IQR, sesgos de la encuesta | 01, 03 |
| 8 | `08-formulario.md` | Fórmulas con explicación de cada símbolo y cuándo usarlas | 03, 04, 05 |
| 9 | `09-glosario.md` | Definiciones conceptuales, no solo listas de palabras | Todo |
| 10 | `10-preguntas-guia.md` | Auto-evaluación por tema | Todo |
| 11 | `11-bibliografia.md` | Guía de uso de Devore, Bonamente, Cairo y Knaflic | Todo |

## Cómo se lee cada archivo

Cada tema sigue esta estructura fija:

1. **Concepto**: qué es y por qué importa.
2. **Intuición**: la explicación "para un amigo" antes de la fórmula.
3. **Fórmula/Formalismo**: lo técnico, con explicación de cada símbolo.
4. **Ejemplo numérico**: con números concretos, no solo variables.
5. **Conexión con el TP**: "Esto lo usaste cuando..." (cita ejercicio específico).
6. **Errores comunes**: qué suele confundir a los alumnos.
7. **Checklist de comprensión**: 2-3 preguntas para autoevaluarte.

## Analogías que vas a encontrar

- **El DataFrame como una planilla de cálculo con superpoderes** (Python)
- **La media como el centro de masa de una tabla de madera** (descriptiva)
- **El error estándar como el "temblor" del promedio si repitieras la encuesta** (inferencia)
- **El intervalo de confianza como un aro de basquet que atrapa la verdad el 95% de las veces** (estimación)
- **El p-valor como un termómetro de tensión entre lo que suponés y lo que ves** (test de hipótesis)
- **La limpieza de datos como preparar ingredientes antes de cocinar** (calidad de datos)

## Regla de oro de esta materia

> **Un análisis correcto en código pero flojo en criterio es un análisis incorrecto.**

No alcanza con que el código corra. Tenés que poder justificar cada decisión de limpieza, cada supuesto de tu intervalo, y cada límite de tu interpretación.

---

## Mapa rápido: de los TPs a los archivos

| TP | Ejercicio | Conceptos centrales | Archivos de estudio |
|----|-----------|---------------------|---------------------|
| **TP1** | Ej1 (lenguajes y salarios) | EDA, limpieza, groupby, mediana vs media, boxplot/violin/KDE, probabilidad condicional | 00, 01, 02, 03, 07 |
| **TP1** | Ej2 (densidades y variables) | Correlación, densidad conjunta, densidad condicional, scatter con hue, regresión | 01, 02, 03, 07 |
| **TP2** | Ej1 (estimación) | Estimación puntual, error estándar, intervalo de confianza (Welch), magnitud práctica | 04, 07, 08 |
| **TP2** | Ej2 (test de hipótesis) | H0/H1, Welch t-test, p-valor, potencia, Cohen's d, Hedges' g, robustez (Mann-Whitney) | 05, 07, 08 |
| **TP2** | Ej3 (comunicación) | Visualización de inferencia, errorbar con IC, honestidad visual, título informativo | 06, 05 |

---

**Dato práctico**: si tenés poco tiempo antes de un parcial, leé en este orden: `01` → `03` → `04` → `05` → `08`. Si tenés más tiempo, hacé el recorrido completo.
