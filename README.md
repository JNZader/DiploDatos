# DiploDatos 2026 — TPs y material de estudio

Resoluciones de trabajos prácticos y apuntes de estudio v2 de las materias
**Análisis y Visualización de Datos (AVD)**, **Análisis Exploratorio y
Curación de Datos (EyCD)** e **Introducción al Aprendizaje Automático (IAA)**
de la Diplomatura en Ciencia de Datos (FAMAF, UNC).

## Estructura

```
.
├── Análisis y Visualización de Datos/
│   ├── TP1/         # entregable resuelto + reportes HTML
│   ├── TP2/         # inferencia: tests de hipótesis, IC
│   └── estudio/     # apuntes v2 — 15 capítulos (00-14) + img_viz/
├── Análisis Exploratorio y Curación de Datos/
│   ├── TP1/         # entregable resuelto end-to-end
│   ├── TP2/         # entregable resuelto + opcionales (SQL, ETL, embeddings, LLM)
│   ├── estudio/     # apuntes v2 — 16 capítulos (00-15)
│   └── BIBLIOGRAFIA.md
├── Introduccion al Aprendizaje Automatico/
│   └── TP1/         # entregable
├── requirements.txt          # deps base de TODOS los TPs (versiones pinneadas)
├── requirements-extras.txt   # opcionales pesados (embeddings, airflow)
├── Dockerfile + docker-compose.yml   # entorno Jupyter compartido (todas las materias)
└── _descarte_pre_gh/                 # archivado (gitignored)
```

## Setup rápido (Docker)

Un solo comando levanta Jupyter Lab con las dependencias de **todas** las
materias ya instaladas (Python 3.11, versiones pinneadas):

```bash
docker compose up --build
```

Abrir [http://localhost:8888/lab](http://localhost:8888/lab). El repo se monta
en `/workspace` — navegás a cualquier materia/TP y los cambios se reflejan en
el host.

Para correr scripts o comandos dentro del contenedor:

```bash
docker compose exec jupyter bash
cd "/workspace/Análisis Exploratorio y Curación de Datos/TP2"
python etl.py
```

Apagar el entorno: `docker compose down`.

### Opcionales pesados (bonus EyCD TP2)

La imagen base **no** incluye `sentence-transformers` (embeddings, ~2 GB de torch)
ni `apache-airflow`, para mantenerla liviana. Si querés correr esos bonus:

```bash
docker compose exec jupyter pip install -r requirements-extras.txt
# o sólo embeddings:
docker compose exec jupyter pip install sentence-transformers
```

Los notebooks están escritos para degradar con elegancia: si el extra no está,
la celda imprime un aviso en vez de tirar error.

## Setup local (alternativa)

Un único entorno sirve para todos los TPs:

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt          # base, todas las materias
pip install -r requirements-extras.txt   # opcional: bonus de EyCD TP2
```

## Workflow de branches

| Branch | Para qué |
|---|---|
| `main` | trunk común — infra Docker, `.gitignore`, README, BIBLIOGRAFIA |
| `tps` | trabajo activo de TPs (AVD + EyCD + IAA) |
| `teoria` | trabajo activo del material de estudio v2 |

Las branches `tps` y `teoria` se mergean a `main` cuando algo está listo.

## Build del material de estudio

Cada `estudio/` tiene su builder HTML:

```bash
cd "Análisis y Visualización de Datos/estudio"
python build_html_v2.py
```

```bash
cd "Análisis Exploratorio y Curación de Datos/estudio"
python build_html_v2.py
```

Outputs en `estudio/build/` (gitignored).

## Notas

- **Datasets**: se descargan desde URLs públicas al ejecutar los análisis
- **`_descarte_pre_gh/`**: contiene versiones v1 antiguas del estudio y otros descartes (gitignored)
- **Slides de cátedra** (`clases/` en cada materia): gitignored por copyright
- **`venv/` y `venv-jupyter/`**: gitignored — regenerables con `pip install -r requirements.txt`
