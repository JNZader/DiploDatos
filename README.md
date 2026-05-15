# DiploDatos 2026 — TPs y material de estudio

Resoluciones de trabajos prácticos y apuntes de estudio v2 de las materias
**Análisis y Visualización de Datos (AVD)** y **Análisis Exploratorio y
Curación de Datos (EyCD)** de la Diplomatura en Ciencia de Datos (FAMAF, UNC).

## Estructura

```
.
├── Análisis y Visualización de Datos/
│   ├── TP1/         # entregable resuelto + reportes HTML
│   ├── TP2/         # inferencia: tests de hipótesis, IC
│   └── estudio/     # apuntes v2 — 15 capítulos (00-14) + img_viz/
├── Análisis Exploratorio y Curación de Datos/
│   ├── TP1/         # entregable resuelto end-to-end
│   ├── TP2/         # entregable resuelto con opcionales
│   ├── estudio/     # apuntes v2 — 16 capítulos (00-15)
│   └── BIBLIOGRAFIA.md
├── Dockerfile + docker-compose.yml   # entorno Jupyter compartido
└── _descarte_pre_gh/                 # archivado (gitignored)
```

## Setup rápido (Docker)

```bash
docker compose up --build
```

Abrir [http://localhost:8888/lab](http://localhost:8888/lab). El repo se monta
en `/workspace` — cambios en notebooks/scripts se reflejan en el host.

Para correr scripts dentro del contenedor:

```bash
docker compose exec avd bash
cd "/workspace/Análisis y Visualización de Datos/TP2"
python tp2_inferencia.py
```

Apagar el entorno: `docker compose down`.

## Setup local (alternativa)

```bash
cd "Análisis y Visualización de Datos/TP1"
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

Repetir por carpeta de TP. Cada uno tiene su `requirements.txt`.

## Workflow de branches

| Branch | Para qué |
|---|---|
| `main` | trunk común — infra Docker, `.gitignore`, README, BIBLIOGRAFIA |
| `tps` | trabajo activo de TPs (AVD + EyCD) |
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
