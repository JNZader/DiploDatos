"""
DAG de Airflow para el ETL del TP2 EyCD.

Ubicación esperada: dags/dag_tp2_etl.py dentro de AIRFLOW_HOME.

Para correr (asumiendo Airflow instalado):
    airflow dags trigger tp2_etl
"""
from datetime import datetime, timedelta
from pathlib import Path
import sys

# Asegurar que etl.py es importable
ETL_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ETL_DIR))

from airflow import DAG
from airflow.operators.python import PythonOperator

import etl  # nuestro módulo

default_args = {
    "owner": "diplodatos-2026",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="tp2_etl",
    description="ETL Melbourne Housing + AirBnB",
    default_args=default_args,
    start_date=datetime(2026, 5, 1),
    schedule_interval="@daily",
    catchup=False,
    tags=["diplodatos", "tp2", "eycd"],
) as dag:

    def task_extract(**kwargs):
        melb, airbnb = etl.extract()
        # XCom: pasar shape a la siguiente tarea (no el df entero — es muy grande)
        kwargs["ti"].xcom_push(key="melb_shape", value=list(melb.shape))
        kwargs["ti"].xcom_push(key="airbnb_shape", value=list(airbnb.shape))
        return "OK"

    def task_transform_and_load(**kwargs):
        # En producción usarías un volumen compartido o un staging area.
        # Acá simplificamos volviendo a extraer dentro de la tarea.
        engine = etl.connect_db()
        melb, airbnb = etl.extract()
        melb_clean, airbnb_by_zip = etl.transform(melb, airbnb)
        output = etl.load(melb_clean, airbnb_by_zip, engine)
        return f"Procesadas {len(output)} filas"

    extract_op = PythonOperator(
        task_id="extract",
        python_callable=task_extract,
    )

    transform_load_op = PythonOperator(
        task_id="transform_and_load",
        python_callable=task_transform_and_load,
    )

    extract_op >> transform_load_op
