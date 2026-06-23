"""
Serviço de predição - Camada de regra de negócio.
Responsável pela lógica de predição e processamento do modelo.
"""

from pathlib import Path
from typing import Optional, Tuple

import joblib
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline

from core.config import settings
from schemas.customer import CustomerInput, PredictionResponse
from utils.app_logging import logger

MODEL_FEATURE_COLUMNS = (
    "zip_code",
    "gender",
    "senior_citizen",
    "partner",
    "dependents",
    "tenure_months",
    "phone_service",
    "multiple_lines",
    "internet_service",
    "online_security",
    "online_backup",
    "device_protection",
    "tech_support",
    "streaming_tv",
    "streaming_movies",
    "contract",
    "paperless_billing",
    "payment_method",
    "monthly_charges",
    "total_charges",
)


class PredictService:
    """
    Serviço de predição com injeção de dependência.
    Carrega o pipeline do modelo uma única vez na inicialização.
    """

    def __init__(self, model_path: Optional[Path | str] = None):
        """
        Inicializa o serviço carregando o pipeline treinado.

        Args:
            model_path: Caminho para o arquivo .joblib do modelo.
                       Se None, usa o caminho padrão das configurações.
        """
        if model_path is None:
            self.model_path = settings.model_path
        else:
            self.model_path = Path(model_path)

        if not self.model_path.exists():
            logger.error(f"Modelo não encontrado em: {self.model_path}")
            raise FileNotFoundError(f"Arquivo do modelo não existe: {self.model_path}")

        logger.info(f"Inicializando PredictService com modelo: {self.model_path}")

        try:
            self.pipeline: Pipeline = joblib.load(self.model_path)
            logger.info("Pipeline carregado com sucesso")
        except Exception as e:
            logger.error(f"Erro crítico ao carregar modelo: {e}")
            raise RuntimeError(f"Não foi possível carregar o pipeline: {e}") from e

    def is_healthy(self) -> bool:
        """
        Verifica se o serviço está saudável (modelo carregado).

        Returns:
            True se o modelo foi carregado com sucesso, False caso contrário.
        """
        return hasattr(self, "pipeline") and self.pipeline is not None

    def _prepare_input_data(self, customer: CustomerInput) -> pd.DataFrame:
        """
        Converte um objeto CustomerInput em um DataFrame para predição.
        Realiza transformações necessárias e garante a ordem correta das features.

        Args:
            customer: Objeto CustomerInput com dados do cliente

        Returns:
            DataFrame com os dados preparados para predição
        """
        # O DTO já garante tipos, domínios e ausência de colunas desconhecidas.
        # customer_id é metadado de rastreabilidade e não é uma feature do modelo.
        data = customer.model_dump(include=set(MODEL_FEATURE_COLUMNS))
        df = pd.DataFrame([data], columns=MODEL_FEATURE_COLUMNS)

        logger.debug(f"Dados preparados com {len(df.columns)} features")

        return df

    def _extract_prediction_proba(self, proba: np.ndarray) -> Tuple[float, float]:
        """
        Extrai probabilidades da predição.
        Assume predição binária (classe 0 e classe 1).

        Args:
            proba: Array de probabilidades do modelo

        Returns:
            Tupla (probabilidade_churn, confianca)
        """
        if len(proba) > 0 and len(proba[0]) >= 2:
            prob_churn = float(proba[0][1])  # Probabilidade da classe 1 (Churn=Yes)
            confidence = max(float(proba[0][0]), float(proba[0][1]))
        else:
            prob_churn = 0.0
            confidence = 0.5

        return round(prob_churn, 3), round(confidence, 3)

    def predict(self, customer: CustomerInput) -> PredictionResponse:
        """
        Executa a predição para um cliente.

        Args:
            customer: Objeto CustomerInput com dados do cliente

        Returns:
            PredictionResponse com resultado da predição

        Raises:
            ValueError: Se o modelo não está carregado ou predição falha
        """
        if not self.is_healthy():
            logger.error("Modelo não está carregado")
            raise ValueError("Modelo não carregado. Serviço indisponível.")

        try:
            # Preparar dados de entrada
            X = self._prepare_input_data(customer)

            # Fazer predição
            prediction = int(self.pipeline.predict(X)[0])
            proba = self.pipeline.predict_proba(X)
            prob_churn, confidence = self._extract_prediction_proba(proba)

            # Converter predição para label
            prediction_label = "Yes" if prediction == 1 else "No"

            # Log da predição
            logger.info(
                f"Predição para cliente {customer.customer_id}: "
                f"Churn={prediction_label}, Prob={prob_churn:.4f}"
            )

            # Criar resposta
            response = PredictionResponse(
                customer_id=customer.customer_id,
                prediction=prediction,
                prediction_label=prediction_label,
                churn_probability=prob_churn,
                confidence=confidence,
            )

            return response

        except Exception as e:
            logger.error(f"Erro durante predição: {str(e)}")
            raise ValueError(f"Erro ao executar predição: {str(e)}")


# Dependência global do FastAPI
_predict_service: PredictService = None


def get_predict_service() -> PredictService:
    """
    Função de dependência do FastAPI.
    Retorna uma instância singleton do serviço de predição.

    Yields:
        PredictService: Instância do serviço de predição
    """
    global _predict_service

    if _predict_service is None:
        _predict_service = PredictService()

    return _predict_service
