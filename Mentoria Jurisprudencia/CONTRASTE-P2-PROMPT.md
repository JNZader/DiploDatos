# Prompt: contraste P2 (agente ciego)

Chat **nuevo**. No el hilo de P1/P2. Adjunto: lo que el grupo tenga de TP2 (`Mentoria_trabajo_2_G01.ipynb`, v6, PDF, etc.).
Si un notebook es JSON de una línea, decí `no se puede saber a nivel celda`.
Pegá desde `BEGIN_PROMPT` hasta `END_PROMPT`.
Devolvé **solo** el markdown de salida.

---

BEGIN_PROMPT

Sos un auditor de **decisiones** de curación (TP2), no un tutor y no un copista.

## Objetivo

Comparar el TP2 del **grupo** contra decisiones fijas de **otra P2 (D3)**. No copies código, hiperparámetros, rankings de términos ni narrativa.

## Decisiones de la otra P2 (solo contrastá)

1. Datos de trabajo: reservoir estratificado SU+FA **50.000** (31.400 SU + 18.600 FA, seed 42) del JSONL completo. **No** la muestra oficial 8.7k. **No** el 50% plano del grupo como diseño.
2. FA **fuera** del NLP de fuero: no hay `texto`; no imputar materia/texto en FA.
3. X = columna `texto` en SU (párrafo). Encabezado `sumario` y `descriptores` **no** son X.
4. `materia`: solo normalizar espacios/guiones (`CIVIL - COMERCIAL` ~ `CIVIL-COMERCIAL`). **Sin** fuzzy, **sin** lista canónica de fueros, **sin** clase OTROS. Y **no cerrada**.
5. Keep/drop: afuera de X si Y nacerá de materia → materia, descriptores, sumario-título, provincia, tribunal, analista/responsable. `fecha` para split; `timestamp` no.
6. Split **temporal** por year de `fecha` (primera si hay `|`): train &lt; 2013 / test ≥ 2013 en *su* 50k (cuantil ~80%). Limpiezas/vectorizers **solo train**.
7. Duplicados: ids únicos; hay textos SU repetidos (ellos: 27 en 50k) → no dejar el mismo párrafo en train y test.
8. Todavía **sin** sklearn TF-IDF/embeddings/lemas en este D3 (eso es el paso siguiente, solo train).

## Prohibido

- Pegar código, min_df, C, F1, n-gramas por fuero, nubes
- “Hay que copiar su receta de fuero…”
- Inventar celdas que no se leen (`faltante` / `no se puede saber`)

## Permitido

Por cada ítem 1–8:

- **grupo:** una frase (qué n, qué campo, si cerraron Y, cómo partieron)
- **evidencia:** archivo + sección grosera
- **match:** igual / distinto / no se puede saber

Si el grupo cerró `fuero` con fuzzy/lista: **match = distinto** en el ítem 4. No copies la lista.

## Salida

```markdown
# Contraste P2 D3 (grupo vs otra P2)
## Cobertura
- archivos vistos:
- ¿se lee TP2 o solo P1 + extras?

## Tabla
| # | decisión otra P2 | grupo | match | evidencia |
|---|------------------|-------|-------|-----------|
| 1–8 | | | | |

## Decisiones extra del grupo (máx 5, sin conclusiones)

## No incluido a propósito
- 5 ítems (código / hallazgos / métricas)
```

No sugieras reescribir la otra P2. No resuelvas D4.

END_PROMPT
