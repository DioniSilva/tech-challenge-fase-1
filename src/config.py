import os
from pathlib import Path
import numpy as np
from utils.app_logging import DEBUG

RANDOM_STATE = 17
TEST_SIZE = 0.2

LOGGING_LEVEL = DEBUG

# Model output directory (project root /models)
PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
DATA_FILE = DATA_DIR / "raw" / "Telco_customer_churn.xlsx"

MODELS_DIR = PROJECT_ROOT / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)

TARGET = 'Churn Value'


def set_seeds(seed: int = RANDOM_STATE):
    np.random.seed(seed)
    try:
        import torch
        torch.manual_seed(seed)
    except Exception:
        pass
