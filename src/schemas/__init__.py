"""Schemas module - DTOs e validação com Pydantic."""

from .customer import CustomerInput, HealthResponse, PredictionResponse

__all__ = ["CustomerInput", "PredictionResponse", "HealthResponse"]
