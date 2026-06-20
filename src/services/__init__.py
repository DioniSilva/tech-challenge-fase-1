"""Services module - Camada de regra de negócio."""

from .predict_service import PredictService, get_predict_service

__all__ = ["PredictService", "get_predict_service"]
