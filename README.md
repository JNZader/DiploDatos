# DiploDatos — Análisis y Visualización de Datos

Material del trabajo práctico de **Análisis y Visualización de Datos**.

## Contenido

- `Análisis y Visualización de Datos/TP1/` — material específico del Trabajo Práctico 1
  - `Entregable - Parte 1.ipynb` — notebook del entregable
  - `ejercicio1.py` — script principal de análisis y generación de gráficos
  - `img/` — gráficos generados
  - `generar_reporte.py` — generador de la solución final en HTML
  - `reporte.html` — solución final en HTML
  - `reporte_completo.py` — generador de la solución explicada
  - `reporte_completo.html` — solución explicada en HTML
  - `requirements.txt` — dependencias de Python para TP1
- `Análisis y Visualización de Datos/py2report.py` — utilidad genérica para convertir un `.py` comentado en un reporte HTML
- `Análisis y Visualización de Datos/guia_py2report.py` — guía de uso de `py2report.py`
- `Análisis y Visualización de Datos/guia_py2report_reporte.html` — reporte HTML generado a partir de la guía

## Requisitos

- Python 3.10+

Instalación sugerida:

```bash
cd "Análisis y Visualización de Datos/TP1"
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Opción recomendada: Docker

Para no instalar dependencias en la máquina local, el repo incluye una configuración Docker reutilizable para **TP1** y **TP2**.

### Levantar Jupyter Lab

```bash
docker compose up --build
```

Luego abrir en el navegador:

```text
http://localhost:8888/lab
```

El proyecto se monta como volumen dentro del contenedor en `/workspace`, así que cualquier cambio en notebooks o scripts queda reflejado en tu carpeta local.

### Ejecutar scripts dentro del contenedor

Con el contenedor levantado, en otra terminal:

```bash
docker compose exec avd bash
```

Dentro del contenedor podés correr, por ejemplo:

```bash
cd "/workspace/Análisis y Visualización de Datos/TP1"
python ejercicio1.py
```

o:

```bash
cd "/workspace/Análisis y Visualización de Datos/TP2"
python tp2_inferencia.py
```

### Apagar el entorno

```bash
docker compose down
```

## Cómo ejecutar

### 1. Generar gráficos desde el análisis

```bash
cd "Análisis y Visualización de Datos/TP1"
python ejercicio1.py
```

Esto genera los PNG dentro de `img/`.

### 2. Generar el reporte HTML resumido

```bash
cd "Análisis y Visualización de Datos/TP1"
python generar_reporte.py
```

### 3. Generar el reporte HTML completo

```bash
cd "Análisis y Visualización de Datos/TP1"
python reporte_completo.py
```

### 4. Usar `py2report`

```bash
cd "Análisis y Visualización de Datos"
python py2report.py "TP1/ejercicio1.py" --output ejercicio1_reporte.html --title "Ejercicio 1"
```

## Notas

- El dataset se descarga desde una URL pública de GitHub al ejecutar el análisis.
- La carpeta `_descarte_pre_gh/` contiene archivos apartados antes de publicar y está ignorada por Git.
- El entorno virtual local no está incluido en el repositorio.
- El entorno Docker instala dependencias comunes de TP1 y TP2 junto con Jupyter Lab.
