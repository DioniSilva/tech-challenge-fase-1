"""Schemas module - DTOs e validação com Pydantic."""
from .customer import CustomerInput, PredictionResponse, HealthResponse

__all__ = ["CustomerInput", "PredictionResponse", "HealthResponse"]
