# Optativa 4 — Programación Distribuida sobre Grandes Volúmenes de Datos

> **Idea rectora:** si los datos no entran en una máquina, el modelo mental no es “más RAM”. Es **no mover datos si podés mover el código**. Spark (y antes MapReduce) existe por el costo de la red frente al disco local.

**Profesor:** Dr. Damián Barsotti. Clases 25–26/09 y 2–3/10/2026.
Repo del curso (clone local del Bitbucket, fuera del repo; no volver a clonar). Bitbucket: <https://bitbucket.org/bigdata_famaf/diplodatos_bigdata>. Slides: <https://damian-barsotti.github.io/diplodatos_intro/#slide:1>.

Esto **no** es la optativa 3 (labs LLM). **No** es el práctico del Consorcio. PySpark en **modo local** (tus núcleos fingiendo cluster); el código es el que iría a un cluster de verdad.

## 0. Contrato

| Rótulo | Significado |
|---|---|
| **Teoría general** | Shuffle, localidad, DAG, lazy evaluation. |
| **Contexto de aula** | Zeppelin, notebooks `note.zpln`, datasets `ds/`. |
| **Hipótesis SAIJ / CC** | Analogía; el JSONL de SAIJ o el corpus del canal **entran en una máquina**. Esta optativa no se aprueba “pasando Spark por el consorcio”. |

### 0.1 Qué deberías poder decir al terminar el encuadre

1. Por qué un CSV que “ya no entra” no se arregla con un disco USB.
2. Qué problema ataca MapReduce y qué hereda Spark (memoria, reuso del DAG).
3. Diferencia imagen Docker vs contenedor; para qué están 8080 y 4040.
4. Por qué los ejercicios viven **dentro** del notebook (no un TP Word).
5. Que `git pull --recurse-submodules` es parte de la materia.

### Checkpoint 0

Si el dataset **sí** entra en tu notebook de siempre, ¿sigue haciendo falta Spark para *aprender* el modelo? (Sí, como modelo mental. No, como entrega de Ética/LLMs/CC.)

## 1. El problema que le da origen

**Teoría general.** CPU y disco local son baratos comparados con **mandar bytes por la red**. MapReduce: llevar la función a donde están los datos, agregar (shuffle) lo mínimo. Spark: el mismo recorte, pero con datos en memoria y un plan (DAG) que se puede reusar.

**Contexto de aula.** Se sube de RDD (explícito) a DataFrame/SQL (más alto). Todo desde Zeppelin, Python.

## 2. Cómo se cursa (no es teoría de Spark todavía)

- Cloná el Bitbucket (`--depth 1 --recursive`). Actualizá antes de cada clase.
- Importá `clases/NN_.../note.zpln`. Completá los `...`. La Ayuda y el N esperado (vértices, aristas) son el test.
- Preferí Docker (≥8 GB). CCAD es si no hay máquina: home `/home/jovyan/diplodatos_bigdata` o perdés el clone.
- Spark UI (4040): ver **tareas**, no “el plot quedó lindo”.

Detalle de comandos: en el árbol de DiploDatos, `Programacion Distribuida sobre Grandes Volumenes de Datos/01_material_oficial/00_programa.md`.

### Error frecuente

**Mover datos de más:** copiar el dataset a cada nodo, arrastrar columnas que no se usan o provocar un shuffle innecesario. La idea rectora es inversa: mover el código hacia los datos y agregar lo mínimo. Si el plan hace que cada tarea lea más de lo necesario, el problema no es el cluster, es la consulta.

**Usar Zeppelin como entrega de otra optativa:** los ejercicios viven **dentro** del notebook (`note.zpln`), y esa entrega es de *esta* materia. No es el práctico del Consorcio ni un reemplazo de los labs de LLMs.

## 3. Bibliografía de aula

*Learning Spark* (2015), *High-Performance Spark* (2017), *Machine Learning with Spark* 2.ª ed. (2017), *Advanced Analytics with Spark* (2015). No están en el repo (copyright).

## 4. Transferencia (después, no ahora)

**Hipótesis SAIJ:** 874 845 filas no son “big data” en el sentido de este curso. El valor de Spark acá es el vocabulario (partición, shuffle), no levantar un cluster.

**Hipótesis CC:** 35 documentos tampoco. No uses Zeppelin como entrega de otra optativa.

### Checkpoint 1

Nombrá una consulta que *haría* shuffle y una que se podría quedar en un nodo. Si no podés, todavía no viste el Spark UI.
