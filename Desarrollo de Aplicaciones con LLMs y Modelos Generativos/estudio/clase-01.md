# Clase 1 — Ecosistema: cloud vs pesos abiertos

Fuente: 18 slides / notas docente. Curso: *desarrollar y evaluar sistemas que corran en producción*, no “pedirle recetas a un chatbot”. Pregunta de directorio: **¿compramos tokens en una API o desplegamos pesos abiertos?**

## Postura (S01–S02)

La IA es **copiloto**: sparring, desarmar errores, contrastar hipótesis. El criterio lo tenés vos.

Trampa: copiar ciego, confundir elocuencia con saber, atrofiar el juicio. Un prototipo que “suena bien” en una demo no es un sistema: en producción aparecen rate limit, TTFT, costo de contexto y fugas.

## Caso hilo (S03, S17)

FinNova, dos cargas **antagónicas** (no hay un modelo para todo):

| | Carga A — minutas de crédito | Carga B — bot FAQ |
| --- | --- | --- |
| Volumen | ~30 req/día | ~150k req/día |
| Datos | Secreto bancario, PII | Público, sin PII |
| Latencia | Tolerante (segundos / batch) | TTFT &lt; 800 ms |
| Riesgo | Multa / filtración | API que se va de precio |
| Dictamen | Qwen local/VPC, GGUF | API barata + streaming |

## Anatomía (S05–S09)

Texto → **tokenizador** (IDs) → **embedding** (vector denso) → **autoatención** (cada token mira al resto: Q, K, V) → **FFN/MLP** (memoria fáctica, no lineal) → logits del próximo token.

- Subword (BPE / WordPiece / SentencePiece): ni palabra entera ni carácter.
- Embedding: cercanía geométrica ≈ afinidad semántica. Q, K, V son el mismo embedding por matrices distintas.
- `<BOS>` / `<EOS>` delimitan. La matriz de afinidad es softmax(QKᵀ/√d).
- La atención resuelve *con quién se relaciona en esta frase*. La FFN activa *qué sabe el modelo de ese concepto*.

## Inferencia física (S10–S11, S14–S15)

Dos fases:

1. **Prefill** — todo el prompt en paralelo. Compute-bound. Métrica: **TTFT**.
2. **Decode** — un token por paso. Memory-bound (hay que traer los pesos de la VRAM). Métrica: **TPOT**.

Muestreo: logits → temperatura (T=0 determinista; T alta = caos) → **Top-P** (núcleo de probabilidad). Alucinación = patrón *verosímil*, no verdad.

VRAM de **pesos** ≈ parámetros (B) × (bits/8) × 1.2. INT4/GGUF mete un 8B en una T4 de 16 GB; FP16 no.

El **KV cache** crece con contexto × batch. El modelo “entra” en 2 GB y el OOM lo mata a los 10 usuarios con 8k tokens. Blindaje: PagedAttention (vLLM), tope de contexto.

## Ecosistema y plata (S12–S13, S16)

| | API cloud | Pesos abiertos |
| --- | --- | --- |
| Pro | Listo en minutos, modelo de punta | Datos en casa, costo fijo |
| Contra | Lock-in, telemetría, el vendor cambia el modelo | GPU, ops, vos sos el SRE |
| Plata | Opex por token (cero si no hay tráfico) | Capex + energía (marginal ~0 hasta saturar) |

Llama 3 **no** es OSI: tiene tope comercial (“revenue gate”). “Open weights” ≠ open source.

**Breakeven:** volumen bajo → API; alto y estable → propio. Híbrido: **router** (LiteLLM) — confidencial a local, masivo a cloud, fallback si la API cae (429/503).

## Glosario mínimo

BPE · TTFT · TPOT · VRAM · GGUF · KV cache · OOM · Top-P · SLA

## Puente a Clase 2

Ya sabemos *dónde corre*. Sigue gobernarlo: system prompt, few-shot, CoT, JSON + pydantic.

Original: `01_material_oficial/01_clases/clase-01/notas-docente.html`
