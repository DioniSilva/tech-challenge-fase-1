"""
Serviço de predição - Camada de regra de negócio.
Responsável pela lógica de predição e processamento do modelo.
"""

from pathlib import Path
from typing import Tuple

import joblib
import numpy as np
import pandas as pd

from core.config import settings
from schemas.customer import CustomerInput, PredictionResponse
from utils.app_logging import logger


class PredictService:
    """
    Serviço de predição com injeção de dependência.
    Carrega o pipeline do modelo uma única vez na inicialização.
    """

    def __init__(self, model_path: Path = None):
        """
        Inicializa o serviço carregando o pipeline treinado.

        Args:
            model_path: Caminho para o arquivo .joblib do modelo.
                       Se None, usa o caminho padrão das configurações.
        """
        if model_path is None:
            model_path = settings.models_dir / settings.model_name

        logger.info(f"Inicializando PredictService com modelo: {model_path}")

        try:
            self.pipeline = joblib.load(model_path)
            self.model_loaded = True
            logger.info("Pipeline carregado com sucesso")
        except FileNotFoundError:
            logger.error(f"Modelo não encontrado em: {model_path}")
            self.model_loaded = False
            self.pipeline = None
        except Exception as e:
            logger.error(f"Erro ao carregar modelo: {str(e)}")
            self.model_loaded = False
            self.pipeline = None

    def is_healthy(self) -> bool:
        """
        Verifica se o serviço está saudável (modelo carregado).

        Returns:
            True se o modelo foi carregado com sucesso, False caso contrário.
        """
        return self.model_loaded

    def _prepare_input_data(self, customer: CustomerInput) -> pd.DataFrame:
        """
        Converte um objeto CustomerInput em um DataFrame para predição.
        Realiza transformações necessárias e garante a ordem correta das features.

        Args:
            customer: Objeto CustomerInput com dados do cliente

        Returns:
            DataFrame com os dados preparados para predição
        """
        # Converter objeto Pydantic para dicionário
        data = customer.model_dump()

        # Converter total_charges de string para float
        try:
            data["total_charges"] = float(data["total_charges"])
        except (ValueError, TypeError):
            data["total_charges"] = 0.0
            logger.warning("Erro ao converter total_charges para float, usando 0.0")

        # Criar DataFrame
        df = pd.DataFrame([data])

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

        return prob_churn, confidence

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
                prediction_probability=prob_churn,
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
