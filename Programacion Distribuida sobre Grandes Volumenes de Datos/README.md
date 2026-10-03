# Optativa 4 — Programación Distribuida sobre Grandes Volúmenes de Datos (2026)

**Profesor:** Dr. Damián Barsotti
**Clases:** 25–26 de septiembre y 2–3 de octubre de 2026
**Meet:** `https://meet.google.com/kxe-seve-tuw`

Eje: **Apache Spark** (por qué existe: costo de mover datos vs disco local; antecesor MapReduce). Interfaces de más bajas a más altas, **Zeppelin + PySpark**. Python y SQL básico se asumen; Spark no.

El Consorcio Canalero **no** es la entrega de esta materia.

## Clone (ya está en esta PC — no volver a clonar)

Desde esta carpeta: `catedra/` → `Educacion/DiploDatos-BigData/diplodatos_bigdata/` (symlink local, gitignored).

- Wrapper: `~/programacion/Educacion/DiploDatos-BigData/PROGRAMA.md`
- Remote: `https://bitbucket.org/bigdata_famaf/diplodatos_bigdata.git` · `master`
- Intro: `catedra/clases/00_introduccion/index.html`
- Slides: <https://damian-barsotti.github.io/diplodatos_intro/#slide:1>

Arranque: `cd catedra/docker && ./zeppelin.sh` → `:8080`.

No copies `ds/` ni la imagen Docker a git.

## Cómo se cursa

Notebooks Zeppelin `clases/NN_.../note.zpln`: teoría + ejercicios con `...` para completar, ayuda y a veces el N esperado. Datasets en `ds/` (vuelos, last.fm, retweets Parquet, grafo web, antropometría/ML).

Todo en **modo local** (núcleos de una máquina como “cluster”). El código es el mismo que en un cluster de verdad.

Rutina: `git pull` antes de cada clase. Entorno: Docker (≥8 GB RAM) o JupyterHub CCAD (`lab.ccad.unc.edu.ar`, DiploDatos, 6G/2 cores, Apache Zeppelin). Docker es lo que se aprende; CCAD es el plan B.

Zeppelin: `http://localhost:8080` · Spark UI: `4040`.

## Evaluación (aula)

Los ejercicios **van en los notebooks**, intercalados con la teoría. No hay un TP Moodle aparte en este pegado.

## Bibliografía (aula)

- Karau, Konwinski, Wendell, Zaharia. *Learning Spark*. O’Reilly, 2015.
- Karau & Warren. *High-Performance Spark*. O’Reilly, 2017.
- Dua, Ghotra, Pentreath. *Machine Learning with Spark*. 2.ª ed., 2017.
- Ryza, Laserson, Owen, Wills. *Advanced Analytics with Spark*. 2015.

Detalle de clone/Docker/CCAD: `01_material_oficial/00_programa.md`.
