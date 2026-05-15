FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /workspace

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY ["Análisis y Visualización de Datos/TP1/requirements.txt", "/tmp/requirements-tp1.txt"]
COPY ["Análisis y Visualización de Datos/TP2/requirements.txt", "/tmp/requirements-tp2.txt"]

RUN pip install --upgrade pip \
    && pip install jupyterlab \
    && pip install -r /tmp/requirements-tp1.txt -r /tmp/requirements-tp2.txt

EXPOSE 8888

CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--ServerApp.token=", "--ServerApp.password="]
