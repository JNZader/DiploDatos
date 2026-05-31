"""
ETL para el TP2 de EyCD — DiploDatos 2026.

Extrae datos de Melbourne Housing + AirBnB Melbourne desde FAMAF,
limpia, agrega y carga el resultado en SQLite + CSV.

Uso:
    python etl.py
"""
import logging
from pathlib import Path
from typing import Tuple

import numpy as np
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
log = logging.getLogger(__name__)

# Constantes
URL_MELB = "https://cs.famaf.unc.edu.ar/~mteruel/datasets/diplodatos/melb_data.csv"
URL_AIRBNB = "https://cs.famaf.unc.edu.ar/~mteruel/datasets/diplodatos/cleansed_listings_dec18.csv"
DB_PATH = Path("melb_etl.sqlite3")
CSV_OUTPUT = Path("melb_data_etl_output.csv")
MIN_REGISTROS_AIRBNB = 5


def connect_db(db_path: Path = DB_PATH) -> Engine:
    """Crea engine SQLAlchemy para SQLite."""
    log.info(f"Conectando a DB: {db_path}")
    return create_engine(f"sqlite:///{db_path}", echo=False)


def extract() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Descarga los dos datasets de FAMAF."""
    log.info("Extracción: bajando melb_data.csv")
    melb = pd.read_csv(URL_MELB)
    log.info(f"  -> melb shape: {melb.shape}")

    log.info("Extracción: bajando cleansed_listings_dec18.csv")
    airbnb = pd.read_csv(URL_AIRBNB)
    log.info(f"  -> airbnb shape: {airbnb.shape}")

    return melb, airbnb


def _limpiar_precio(serie: pd.Series) -> pd.Series:
    """Convierte string '$1,234.56' a float 1234.56."""
    return (
        serie.astype(str)
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .replace("nan", np.nan)
        .astype(float)
    )


def transform(melb: pd.DataFrame, airbnb: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Limpia y agrega los dos datasets."""
    log.info("Transformación: limpiando precios AirBnB")
    airbnb["price"] = _limpiar_precio(airbnb["price"])
    airbnb["weekly_price"] = _limpiar_precio(airbnb["weekly_price"])
    airbnb["monthly_price"] = _limpiar_precio(airbnb["monthly_price"])
    airbnb["zipcode"] = pd.to_numeric(airbnb["zipcode"], errors="coerce")
    airbnb = airbnb.dropna(subset=["zipcode"])
    airbnb["zipcode"] = airbnb["zipcode"].astype(int)

    log.info("Transformación: agregando AirBnB por zipcode")
    airbnb_by_zip = (
        airbnb.groupby("zipcode")
        .agg(
            airbnb_price_median=("price", "median"),
            airbnb_price_mean=("price", "mean"),
            airbnb_count=("price", "count"),
        )
        .reset_index()
    )
    airbnb_by_zip = airbnb_by_zip[airbnb_by_zip["airbnb_count"] >= MIN_REGISTROS_AIRBNB]
    log.info(f"  -> zipcodes válidos: {len(airbnb_by_zip)}")

    log.info("Transformación: limpiando outliers de melb")
    mask_land = melb["Landsize"] > 5000
    mask_build = melb["BuildingArea"] > 1000
    mask_price = melb["Price"] > melb["Price"].quantile(0.75) + 3 * (
        melb["Price"].quantile(0.75) - melb["Price"].quantile(0.25)
    )
    n_outliers = (mask_land | mask_build | mask_price).sum()
    log.info(f"  -> outliers eliminados: {n_outliers}")
    melb = melb[~(mask_land | mask_build | mask_price)].copy()

    log.info("Transformación: convirtiendo Date a datetime")
    melb["Date"] = pd.to_datetime(melb["Date"], format="%d/%m/%Y")
    melb["Postcode_int"] = melb["Postcode"].astype(int)

    return melb, airbnb_by_zip


def load(melb: pd.DataFrame, airbnb_by_zip: pd.DataFrame, engine: Engine) -> pd.DataFrame:
    """Carga a SQLite + merge final + guarda CSV."""
    log.info("Load: ingestando tablas a SQLite")
    melb.to_sql("properties", con=engine, if_exists="replace", index=False)
    airbnb_by_zip.to_sql("airbnb", con=engine, if_exists="replace", index=False)
    log.info(f"  -> properties: {len(melb)} filas")
    log.info(f"  -> airbnb: {len(airbnb_by_zip)} filas")

    log.info("Load: merge final + guardar CSV")
    output = melb.merge(
        airbnb_by_zip,
        how="left",
        left_on="Postcode_int",
        right_on="zipcode",
        validate="many_to_one",
    )
    output = output.drop(columns=["Postcode_int", "zipcode"])
    output.to_csv(CSV_OUTPUT, index=False)
    log.info(f"  -> CSV guardado en {CSV_OUTPUT} ({len(output)} filas)")

    # Validación post-load
    df_verif = pd.read_csv(CSV_OUTPUT)
    assert df_verif.shape == output.shape, "Shape no coincide tras releer!"
    log.info(f"  -> [OK] Verificación post-guardado")

    return output


def main():
    """Orquesta el pipeline."""
    log.info("=== ETL TP2 EyCD ===")
    engine = connect_db()
    melb, airbnb = extract()
    melb_clean, airbnb_by_zip = transform(melb, airbnb)
    final = load(melb_clean, airbnb_by_zip, engine)
    log.info(f"=== ETL COMPLETADO: {final.shape} ===")
    return final


if __name__ == "__main__":
    main()
