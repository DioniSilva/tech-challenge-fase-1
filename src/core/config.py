"""
Configurações globais da aplicação usando Pydantic Settings.
Todas as variáveis de ambiente são lidas e validadas aqui.
"""
from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from pathlib import Path


class Settings(BaseSettings):
    """
    Configurações da aplicação.
    Lê variáveis de ambiente e arquivo .env
    """

    # Aplicação
    app_name: str = "Telco Churn Prediction API"
    app_version: str = "1.0.0"
    debug: bool = False

    # API
    api_prefix: str = "/api"
    api_v1_prefix: str = "/api/v1"

    # Caminhos
    project_root: Path = Path(__file__).resolve().parents[2]
    models_dir: Path = project_root / "models"
    data_dir: Path = project_root / "data"

    # Modelo
    model_name: str = "mlp.joblib"

    # Logging
    log_level: str = "INFO"

    model_config = ConfigDict(env_file=".env", case_sensitive=False)


# Instância global de configurações
settings = Settings()
