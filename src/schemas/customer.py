"""Schemas públicos da API de inferência de churn."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

YesNo = Literal["Yes", "No"]
InternetAddOn = Literal["Yes", "No", "No internet service"]


class CustomerInput(BaseModel):
    """Contrato de inferência alinhado às features do modelo MLP.

    ``customer_id`` é usado somente para rastreabilidade. Os demais campos são
    exatamente as 20 features aceitas pelo pré-processador do modelo.
    """

    customer_id: str = Field(..., min_length=1, description="ID não vazio do cliente")

    zip_code: int = Field(..., ge=0, le=99999, description="CEP dos Estados Unidos")
    gender: Literal["Female", "Male"] = Field(..., description="Gênero do cliente")
    senior_citizen: YesNo = Field(..., description="Cliente idoso")
    partner: YesNo = Field(..., description="Possui parceiro")
    dependents: YesNo = Field(..., description="Possui dependentes")
    tenure_months: int = Field(..., ge=0, description="Meses de permanência")

    phone_service: YesNo = Field(..., description="Possui serviço de telefone")
    multiple_lines: Literal["Yes", "No", "No phone service"] = Field(
        ..., description="Possui múltiplas linhas"
    )
    internet_service: Literal["DSL", "Fiber optic", "No"] = Field(
        ..., description="Tipo de serviço de internet"
    )
    online_security: InternetAddOn = Field(..., description="Serviço de segurança online")
    online_backup: InternetAddOn = Field(..., description="Serviço de backup online")
    device_protection: InternetAddOn = Field(..., description="Proteção do dispositivo")
    tech_support: InternetAddOn = Field(..., description="Suporte técnico")
    streaming_tv: InternetAddOn = Field(..., description="Streaming de TV")
    streaming_movies: InternetAddOn = Field(..., description="Streaming de filmes")

    contract: Literal["Month-to-month", "One year", "Two year"] = Field(
        ..., description="Tipo de contrato"
    )
    paperless_billing: YesNo = Field(..., description="Fatura sem papel")
    payment_method: Literal[
        "Electronic check",
        "Mailed check",
        "Bank transfer (automatic)",
        "Credit card (automatic)",
    ] = Field(..., description="Método de pagamento")
    monthly_charges: float = Field(
        ..., ge=0, allow_inf_nan=False, description="Cobrança mensal em dólares"
    )
    total_charges: float = Field(
        ..., ge=0, allow_inf_nan=False, description="Cobrança total em dólares"
    )

    model_config = ConfigDict(
        strict=True,
        extra="forbid",
        str_strip_whitespace=True,
        json_schema_extra={
            "example": {
                "customer_id": "5575-GNVDE",
                "zip_code": 90001,
                "gender": "Male",
                "senior_citizen": "Yes",
                "partner": "Yes",
                "dependents": "Yes",
                "tenure_months": 48,
                "phone_service": "Yes",
                "multiple_lines": "Yes",
                "internet_service": "Fiber optic",
                "online_security": "No",
                "online_backup": "No",
                "device_protection": "No",
                "tech_support": "No",
                "streaming_tv": "Yes",
                "streaming_movies": "Yes",
                "contract": "One year",
                "paperless_billing": "No",
                "payment_method": "Credit card (automatic)",
                "monthly_charges": 105.25,
                "total_charges": 5046.0,
            }
        },
    )

    @model_validator(mode="after")
    def validate_service_dependencies(self) -> "CustomerInput":
        """Reject combinations that do not represent a possible subscription."""
        if self.phone_service == "No" and self.multiple_lines != "No phone service":
            raise ValueError(
                "multiple_lines must be 'No phone service' when phone_service is 'No'"
            )
        if self.phone_service == "Yes" and self.multiple_lines == "No phone service":
            raise ValueError(
                "multiple_lines cannot be 'No phone service' when phone_service is 'Yes'"
            )

        add_on_fields = (
            "online_security",
            "online_backup",
            "device_protection",
            "tech_support",
            "streaming_tv",
            "streaming_movies",
        )
        add_on_values = [getattr(self, field) for field in add_on_fields]
        if self.internet_service == "No":
            if any(value != "No internet service" for value in add_on_values):
                raise ValueError(
                    "internet add-ons must be 'No internet service' when internet_service is 'No'"
                )
        elif any(value == "No internet service" for value in add_on_values):
            raise ValueError(
                "internet add-ons cannot be 'No internet service' when internet_service is enabled"
            )

        return self


class PredictionResponse(BaseModel):
    """Schema para resposta de predição."""

    customer_id: str = Field(..., description="ID do cliente")
    prediction: int = Field(..., description="Predição (0=Não churn, 1=Churn)")
    prediction_label: str = Field(..., description="Label da predição (Yes/No)")
    churn_probability: float = Field(..., ge=0.0, le=1.0, description="Probabilidade de churn")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confiança da predição (max prob)")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "customer_id": "5575-GNVDE",
                "prediction": 0,
                "prediction_label": "No",
                "churn_probability": 0.25,
                "confidence": 0.75,
            }
        }
    )


class HealthResponse(BaseModel):
    """Schema para resposta de health check."""

    status: str = Field(..., description="Status da aplicação (healthy/unhealthy)")
    message: str = Field(..., description="Mensagem descritiva")
    version: str = Field(..., description="Versão da aplicação")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "healthy",
                "message": "API is running correctly",
                "version": "1.0.0",
            }
        }
    )
