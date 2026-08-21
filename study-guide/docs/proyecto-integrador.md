# Proyecto integrador — búsqueda semántica y RAG

> **Este proyecto integrador no es una materia formal de DiploDatos.** Es el próximo paso aplicado de la mentoría SAIJ y reutiliza las seis materias.

La secuencia acumulada queda:

```text
Materia 1: describir y comunicar
  → Materia 2: curar y documentar
  → Materia 3: formular y evaluar aprendizaje
  → Materia 4: comparar familias supervisadas
  → Materia 5: representar, explorar y recuperar sin target directo
  → Materia 6: evaluar propósito, daño, equidad, privacidad y responsabilidad
  → Proyecto integrador: búsqueda semántica evaluada y luego RAG
```

## 1. Primer tramo: retrieval antes de generación

El proyecto debería comenzar con:

1. pregunta de uso y población;
2. corpus versionado;
3. unidad de indexación;
4. baseline TF-IDF;
5. embeddings candidatos;
6. filtros de metadatos;
7. conjunto de consultas;
8. juicios de relevancia;
9. métricas top-k;
10. análisis de errores y sesgos;
11. política de ausencia de evidencia.

Solo cuando retrieval alcance criterios definidos tiene sentido diseñar la etapa generativa. Agregar un modelo generador antes impediría distinguir si un error nace de recuperación, contexto, instrucciones o generación.

## 2. Qué queda deliberadamente fuera

Materia 6 no desarrolló una arquitectura RAG completa, selección de generador, prompts, manejo de contexto, citación, verificación de afirmaciones, memoria conversacional, seguridad ni evaluación de respuestas. Esos son objetivos del proyecto integrador posterior.

## 3. Pregunta de cierre del libro actual

> ¿Podemos demostrar que una representación y un ranking recuperan evidencia pertinente, estable y auditable para consultas SAIJ antes de pedirle a un generador que redacte sobre ella?

Si la respuesta todavía es “no sabemos”, el próximo paso no es una interfaz más vistosa. Es una mejor evaluación de recuperación.

---


