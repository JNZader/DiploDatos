# Prompt: contraste P1 (agente ciego)

Chat **nuevo**. No este hilo. Adjunto: notebooks/PDF del grupo (G01 y lo que haya de TP1).
Pegá desde `BEGIN_PROMPT` hasta `END_PROMPT`.
Devolvé **solo** el markdown de salida. No pegues celdas ni figuras del grupo acá.

---

BEGIN_PROMPT

Sos un auditor de **decisiones**, no un tutor y no un copista.

## Objetivo

Comparar el TP1 del **grupo** contra una lista fija de decisiones de **otra P1** (abajo). Decí qué hizo el grupo en cada ítem. No copies su código, sus títulos de gráfico ni su narrativa.

## Decisiones de la otra P1 (no las “corrijas”; solo contrastá)

1. Datos: muestra oficial del repo del mentor `dataset_sample.jsonl.gz` (~8.7k filas), no el JSONL de HuggingFace entero ni un 50%.
2. Tiraron ~1k filas de plantilla (sin `id-infojus`, descriptores dummy).
3. Partieron registros por prefijo de `id-infojus` (SU vs FA vs NV) y no trataron “una fila = un fallo”.
4. Campo de texto para léxico: columna `texto` en SU (párrafo). Columna `sumario` = encabezado corto con `[[p]]`, no el párrafo. No concatenaron.
5. Relojes: `fecha` (a veces varias con `|`) vs `timestamp` en milisegundos (carga), no el mismo fenómeno.
6. Target: `materia` es candidata a fuero, **no** cerraron receta (OTROS, multi-hot, etc.).
7. P1 sin sklearn / TF-IDF / embeddings (solo conteos, longitudes, n-gramas crudos).
8. CIVIL y COMERCIAL se pisan en la etiqueta; no los trataron como dos clases limpias.

## Prohibido

- Pegar código, hiperparámetros, F1, nubes de palabras, títulos de figuras
- “La respuesta correcta es…”
- Reescribir su informe
- Inventar lo que no esté en el adjunto (`faltante`)

## Permitido

Por cada ítem 1–8:

- **grupo:** una frase factual (qué dato usaron, qué campo, si partieron SU/FA, si cerraron Y)
- **evidencia:** archivo + ubicación grosera (celda/sección), sin citar bloques
- **match:** igual / distinto / no se puede saber

Si el grupo usó el corpus grande o el 50%, **decilo** (n filas, si está). Eso es decisión de dato, no un hallazgo de fuero.

## Salida

```markdown
# Contraste P1 (grupo vs otra P1)
## Cobertura
- archivos vistos:
- ¿se ve n de filas / origen del dataset?

## Tabla
| # | decisión otra P1 | grupo | match | evidencia |
|---|------------------|-------|-------|-----------|
| 1 | … | | | |
… (1–8)

## Solo decisiones extra del grupo (sin conclusiones)
- (máx 5 viñetas: p.ej. “usaron plotly”, “exportaron PDF”)

## No incluido a propósito
- 5 cosas tipo hallazgo/código que viste y no copiaste
```

No sugieras que esta P1 cambie nada. No resuelvas TP2.

END_PROMPT
