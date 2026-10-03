# Programa — optativa 4 (2026)

Texto de aula. Comandos Docker/git: copiados del Moodle; no se ejecutaron en esta máquina al archivar.

## El problema

Cuando los datos no entran en una computadora, no se resuelve con un disco más grande. Hay que **repartir** almacenamiento y cómputo. Spark nace del costo de **mover datos por la red** vs leer disco local. MapReduce es el antecesor que explica el diseño.

## Interfaces

De más explícita/bajo nivel a más alta, siempre PySpark en Zeppelin.

## Git

En esta máquina **ya está clonado** (25/09/2026):
`/home/javier/programacion/Educacion/DiploDatos-BigData/diplodatos_bigdata/`

No hagas otro clone. Antes de cada clase: `git pull --recurse-submodules` **ahí**.

Si en otra PC no estuviera:

```text
# Linux
git clone --depth 1 --recursive https://bitbucket.org/bigdata_famaf/diplodatos_bigdata.git

# Windows (antes)
git config --global core.autocrlf false
git clone --depth 1 --recursive https://bigdata_famaf@bitbucket.org/bigdata_famaf/diplodatos_bigdata.git
```

El clone con usuario `bigdata_famaf@` es el que publica el aula para Windows; si pide clave, Slack de la materia.

## Docker (recomendado)

Requisito: ≥8 GB RAM. Imagen `diplodatos/bigdata:4.1`.

Desde `docker/` del repo:

```text
docker build --tag diplodatos/bigdata:4.1 \
  -f ./diplodatos_bigdata/dockerfiles/Dockerfile \
  ./diplodatos_bigdata/context
```

Linux: script `./diplodatos_bigdata/build.sh`. Arranque: `./zeppelin.sh` o el `docker run` del README (uid del host, puertos 8080 y 4040, volúmenes `vols/` y el repo).

Windows: `zeppelin.cmd`; uid 1000; `.wslconfig` si WSL se come la RAM.

## CCAD (plan B)

<https://lab.ccad.unc.edu.ar/> · Solo CPU · entorno DiploDatos · Lab · 6G RAM, 2 cores · notebook Apache Zeppelin.

Clonar **en** `/home/jovyan/diplodatos_bigdata` (los notebooks buscan `ds/` ahí). Fuera de `/home/jovyan` se pierde al apagar. Apagar el servidor al terminar.

## Datasets (`ds/`)

Vuelos, last.fm, red de retweets (Parquet), grafo de links, antropometría para ML. No copiar a git de DiploDatos.
