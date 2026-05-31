# =====================================================================
# DiploDatos 2026 — Imagen base reproducible para TODOS los TPs
# =====================================================================
# Python 3.11 (estable, todo el ecosistema científico compila sin drama).
# Instala las dependencias OBLIGATORIAS de las tres materias.
# Los extras opcionales se instalan a demanda (ver requirements-extras.txt).
# =====================================================================
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /workspace

# build-essential: necesario para compilar wheels de algunas libs científicas
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiamos SOLO requirements primero → mejor cacheo de capas.
# Si cambia el código pero no las deps, no se reinstala todo.
COPY requirements.txt /tmp/requirements.txt

RUN pip install --upgrade pip \
    && pip install -r /tmp/requirements.txt

EXPOSE 8888

# Jupyter Lab abierto en la raíz del workspace → navegás a cualquier materia/TP.
# Sin token/password: entorno local de desarrollo académico.
CMD ["jupyter", "lab", \
     "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", \
     "--ServerApp.root_dir=/workspace", \
     "--ServerApp.token=", "--ServerApp.password="]
