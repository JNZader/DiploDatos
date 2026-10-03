# Metodología: sesgo de un atributo en un juez LLM

Fuente del diseño (no copiamos sus datos ni sus pesos): [federicomina-1987/sesgo_unc](https://github.com/federicomina-1987/sesgo_unc) (ATS sintético, universidad). Acá el mismo **experimento**, desacoplado de CVs y de LM Studio.

## Qué midió Mina (fase 1, 01/10/2026)

1. **Unidad.** Un perfil sintético JSON (skills, experiencia, título).
2. **Factor.** Solo `education.institution`. El resto del CV es un *template* de tier (`weak` / `moderate` / `strong`).
3. **Grupos.** 3 regiones × 3 universidades. UNC está en LATAM; US y EU son universidades QS 1401+.
4. **Repeticiones.** 9 × 3 combinaciones, 100 veces cada una → 2700 llamadas **por modelo**.
5. **Juez.** LLM local, OpenAI-compatible, T=0.1, JSON `{reasoning, final_score}` 1–10.
6. **Análisis.** Diferencia de medias UNC − grupo, por tier, con p-valor.

Hallazgo útil: el signo **cambia con el tier y el modelo**. No es “la UNC siempre pierde”.

### Decisiones (y un bug) del notebook original

- El system prompt iba en `role: assistant`. Acá va en `system`.
- Checkpoint a disco por candidato (se puede retomar).
- No hay corrección por tests múltiples en el README; 9 comparaciones por tabla.
- Prompt en inglés; el factor es un nombre propio.

## Diseño agnóstico (este directorio)

| Pieza | En Mina | Acá |
|---|---|---|
| Objeto | CV Data Scientist | JSON arbitrario (`templates` en YAML) |
| Factor | universidad | `factor.path` dotted (p. ej. `education.institution` o `fuero`) |
| Niveles | 9 strings | `factor.groups` |
| Juez | LM Studio hardcode | cualquier `base_url` OpenAI-compatible |
| Score | `final_score` | `score_field` |

**Hipótesis.** Si el juez es imparcial al factor, la distribución del score no cambia al permutar solo ese campo, *dentro del mismo template*.

No es el práctico Moodle de Ética. No es COMPAS. Es auditoría de un **LLM-as-judge** cuando el input es sintético controlado (§11.5 del capítulo: uso de sintético *declarado*, no fraude).
