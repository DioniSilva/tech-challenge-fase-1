import pandas as pd
import joblib
from config import DATA_FILE, MODELS_DIR
from utils.app_logging import logger

def carregar_dados() -> pd.DataFrame:
    logger.info(f"Carregando dados do arquivo: {DATA_FILE}")
    return pd.read_excel(DATA_FILE)


def save_pipeline(pipeline, name: str = "mlp.joblib") -> None:
    logger.info(f"Salvando pipeline treinado como: {name}")
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, MODELS_DIR / name)


def load_pipeline(name: str = "mlp.joblib"):
    logger.info(f"Carregando pipeline treinado do arquivo: {name}")
    return joblib.load(MODELS_DIR / name)
