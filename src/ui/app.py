"""Interface Streamlit para inferência unitária de churn."""

from __future__ import annotations

from datetime import datetime, timezone
import os
from typing import Any, MutableMapping

import streamlit as st

from ui.client import (
    DEFAULT_API_BASE_URL,
    ApiConnectionError,
    ApiResponseError,
    ApiTimeoutError,
    get_health,
    predict,
)

API_BASE_URL = os.getenv("API_BASE_URL", DEFAULT_API_BASE_URL)
MKDOCS_URL = os.getenv("MKDOCS_URL")
GITHUB_REPOSITORY_URL = "https://github.com/DioniSilva/tech-challenge-fase-1"
INTERNET_ADD_ON_FIELDS = (
    "online_security",
    "online_backup",
    "device_protection",
    "tech_support",
    "streaming_tv",
    "streaming_movies",
)
MAX_PREDICTION_HISTORY = 10
PT_BR_LABELS = {
    "Yes": "Sim",
    "No": "Não",
    "Female": "Feminino",
    "Male": "Masculino",
    "No phone service": "Sem serviço de telefone",
    "DSL": "DSL",
    "Fiber optic": "Fibra óptica",
    "No internet service": "Sem serviço de internet",
    "Month-to-month": "Mensal",
    "One year": "Um ano",
    "Two year": "Dois anos",
    "Electronic check": "Cheque eletrônico",
    "Mailed check": "Cheque pelos correios",
    "Bank transfer (automatic)": "Transferência bancária (automática)",
    "Credit card (automatic)": "Cartão de crédito (automático)",
}


def format_option(value: str) -> str:
    """Retorna o rótulo pt-BR de um valor canônico do contrato."""
    return PT_BR_LABELS[value]


def build_reference_links(
    api_base_url: str, mkdocs_url: str | None
) -> dict[str, dict[str, str | bool]]:
    """Monta as referências exibidas no topo da interface."""
    return {
        "api": {
            "label": "Documentação da API",
            "url": f"{api_base_url.rstrip('/')}/docs",
            "enabled": True,
        },
        "mkdocs": {
            "label": "Documentação do projeto",
            "url": mkdocs_url.rstrip("/") if mkdocs_url else "",
            "enabled": bool(mkdocs_url),
        },
        "github": {
            "label": "Repositório no GitHub",
            "url": GITHUB_REPOSITORY_URL,
            "enabled": True,
        },
    }


def render_references() -> None:
    """Renderiza links de referência para API, projeto e código-fonte."""
    st.subheader("Referências")
    links = build_reference_links(API_BASE_URL, MKDOCS_URL)
    columns = st.columns(3)
    for column, reference in zip(columns, links.values(), strict=True):
        with column:
            st.link_button(
                reference["label"],
                reference["url"] or "about:blank",
                disabled=not reference["enabled"],
                use_container_width=True,
            )
    if not links["mkdocs"]["enabled"]:
        st.caption("Defina `MKDOCS_URL` para disponibilizar a documentação do projeto.")


def build_payload(values: dict[str, Any]) -> dict[str, Any]:
    """Cria o payload que corresponde integralmente ao contrato FastAPI."""
    values = values.copy()
    normalize_dependent_service_values(values, values["phone_service"], values["internet_service"])
    return {
        "customer_id": values["customer_id"].strip(),
        "zip_code": int(values["zip_code"]),
        "gender": values["gender"],
        "senior_citizen": values["senior_citizen"],
        "partner": values["partner"],
        "dependents": values["dependents"],
        "tenure_months": int(values["tenure_months"]),
        "phone_service": values["phone_service"],
        "multiple_lines": values["multiple_lines"],
        "internet_service": values["internet_service"],
        "online_security": values["online_security"],
        "online_backup": values["online_backup"],
        "device_protection": values["device_protection"],
        "tech_support": values["tech_support"],
        "streaming_tv": values["streaming_tv"],
        "streaming_movies": values["streaming_movies"],
        "contract": values["contract"],
        "paperless_billing": values["paperless_billing"],
        "payment_method": values["payment_method"],
        "monthly_charges": float(values["monthly_charges"]),
        "total_charges": float(values["total_charges"]),
    }


@st.cache_data(ttl=15)
def fetch_health(api_base_url: str) -> dict[str, Any]:
    """Consulta o health endpoint, evitando uma chamada por rerun da interface."""
    return get_health(api_base_url)


def normalize_dependent_service_values(
    values: MutableMapping[str, Any], phone_service: str, internet_service: str
) -> None:
    """Normaliza serviços dependentes para uma combinação aceita pela API."""
    if phone_service == "No":
        values["multiple_lines"] = "No phone service"
    elif values.get("multiple_lines") == "No phone service":
        values["multiple_lines"] = "No"

    if internet_service == "No":
        for field in INTERNET_ADD_ON_FIELDS:
            values[field] = "No internet service"
    else:
        for field in INTERNET_ADD_ON_FIELDS:
            if values.get(field) == "No internet service":
                values[field] = "No"


def add_prediction_history(
    history: list[dict[str, Any]],
    payload: dict[str, Any],
    result: dict[str, Any],
    created_at: datetime | None = None,
) -> list[dict[str, Any]]:
    """Adiciona uma predição ao histórico, mantendo somente as mais recentes."""
    timestamp = created_at or datetime.now(timezone.utc)
    entry = {
        "created_at": timestamp.isoformat(),
        "payload": payload.copy(),
        "result": result.copy(),
    }
    return [entry, *history][:MAX_PREDICTION_HISTORY]


def initialize_prediction_history() -> None:
    """Inicializa o histórico transitório da aba atual."""
    if "prediction_history" not in st.session_state:
        st.session_state.prediction_history = []


def record_prediction(payload: dict[str, Any], result: dict[str, Any]) -> None:
    """Registra uma predição concluída com sucesso na sessão atual."""
    initialize_prediction_history()
    st.session_state.prediction_history = add_prediction_history(
        st.session_state.prediction_history, payload, result
    )


def render_prediction_history() -> None:
    """Exibe e permite limpar o histórico desta sessão do navegador."""
    initialize_prediction_history()
    with st.expander("Histórico desta sessão"):
        history = st.session_state.prediction_history
        if st.button("Limpar histórico", disabled=not history):
            st.session_state.prediction_history = []
            history = []

        if not history:
            st.caption("Nenhuma predição realizada nesta sessão.")
            return

        for entry in history:
            result = entry["result"]
            with st.container(border=True):
                timestamp = datetime.fromisoformat(entry["created_at"])
                st.caption(timestamp.strftime("%d/%m/%Y %H:%M:%S UTC"))
                customer, prediction, probability, confidence = st.columns(4)
                customer.metric("Cliente", result["customer_id"])
                prediction.metric("Churn", format_option(result["prediction_label"]))
                probability.metric("Probabilidade", f"{result['churn_probability']:.1%}")
                confidence.metric("Confiança", f"{result['confidence']:.1%}")
                with st.expander("Ver dados completos"):
                    st.json({"entrada": entry["payload"], "resultado": result})


def render_health_status() -> None:
    """Exibe o estado atual do backend e permite atualizar a consulta."""
    left, right = st.columns([4, 1])
    with left:
        try:
            health = fetch_health(API_BASE_URL)
            if health.get("status") == "healthy":
                st.success(f"API disponível — modelo carregado (v{health.get('version', 'N/A')}).")
            else:
                st.warning("A API respondeu, mas não está saudável.")
        except ApiTimeoutError:
            st.warning("A API não respondeu dentro do tempo esperado.")
        except (ApiConnectionError, ApiResponseError):
            st.warning("API indisponível. Verifique se `make serve` está em execução.")
    with right:
        if st.button("Atualizar status", use_container_width=True):
            fetch_health.clear()
            st.rerun()


def render_result(result: dict[str, Any]) -> None:
    """Apresenta o resultado retornado pela API."""
    label = result["prediction_label"]
    message = (
        "Há risco de churn para este cliente." if label == "Yes" else "Não há indicação de churn."
    )
    (st.error if label == "Yes" else st.success)(message)
    probability, confidence = st.columns(2)
    probability.metric("Probabilidade de churn", f"{result['churn_probability']:.1%}")
    confidence.metric("Confiança", f"{result['confidence']:.1%}")
    st.caption(f"Cliente: {result['customer_id']} | Classificação: {format_option(label)}")


def main() -> None:
    st.set_page_config(page_title="Predição de Churn", page_icon="📉", layout="centered")
    st.title("Predição de churn")
    st.write("Informe os dados do cliente para consultar a probabilidade de cancelamento.")
    render_references()
    render_health_status()

    st.subheader("Dados do cliente")
    customer_id = st.text_input("ID do cliente", value="5575-GNVDE")
    demographic_left, demographic_right = st.columns(2)
    with demographic_left:
        zip_code = st.number_input("CEP", min_value=0, max_value=99999, value=90001, step=1)
        gender = st.selectbox("Gênero", ["Female", "Male"], format_func=format_option)
        senior_citizen = st.selectbox("Cliente idoso", ["No", "Yes"], format_func=format_option)
    with demographic_right:
        partner = st.selectbox("Possui parceiro", ["No", "Yes"], format_func=format_option)
        dependents = st.selectbox("Possui dependentes", ["No", "Yes"], format_func=format_option)
        tenure_months = st.number_input("Meses como cliente", min_value=0, value=48, step=1)

    st.subheader("Serviços e contrato")
    phone_service = st.selectbox(
        "Serviço de telefone", ["Yes", "No"], key="phone_service", format_func=format_option
    )
    if phone_service == "No":
        st.selectbox(
            "Múltiplas linhas",
            ["No phone service"],
            key="multiple_lines_unavailable",
            disabled=True,
            format_func=format_option,
        )
        multiple_lines = "No phone service"
    else:
        multiple_lines = st.selectbox(
            "Múltiplas linhas", ["Yes", "No"], key="multiple_lines", format_func=format_option
        )

    internet_service = st.selectbox(
        "Serviço de internet",
        ["DSL", "Fiber optic", "No"],
        key="internet_service",
        format_func=format_option,
    )
    add_on_labels = {
        "online_security": "Segurança online",
        "online_backup": "Backup online",
        "device_protection": "Proteção do dispositivo",
        "tech_support": "Suporte técnico",
        "streaming_tv": "Streaming de TV",
        "streaming_movies": "Streaming de filmes",
    }
    service_columns = st.columns(2)
    add_on_values: dict[str, str] = {}
    for index, field in enumerate(INTERNET_ADD_ON_FIELDS):
        with service_columns[index % 2]:
            if internet_service == "No":
                st.selectbox(
                    add_on_labels[field],
                    ["No internet service"],
                    key=f"{field}_unavailable",
                    disabled=True,
                    format_func=format_option,
                )
                add_on_values[field] = "No internet service"
            else:
                add_on_values[field] = st.selectbox(
                    add_on_labels[field], ["Yes", "No"], key=field, format_func=format_option
                )

    contract_left, contract_right = st.columns(2)
    with contract_left:
        contract = st.selectbox(
            "Contrato", ["Month-to-month", "One year", "Two year"], format_func=format_option
        )
        paperless_billing = st.selectbox(
            "Fatura sem papel", ["Yes", "No"], format_func=format_option
        )
    with contract_right:
        payment_method = st.selectbox(
            "Método de pagamento",
            [
                "Electronic check",
                "Mailed check",
                "Bank transfer (automatic)",
                "Credit card (automatic)",
            ],
            format_func=format_option,
        )

    st.subheader("Cobranças")
    monthly_charges, total_charges = st.columns(2)
    with monthly_charges:
        monthly_charge_value = st.number_input(
            "Cobrança mensal (US$)", min_value=0.0, value=105.25
        )
    with total_charges:
        total_charge_value = st.number_input("Cobrança total (US$)", min_value=0.0, value=5046.0)

    if st.button("Calcular predição", type="primary", use_container_width=True):
        payload = build_payload(
            {
                "customer_id": customer_id,
                "zip_code": zip_code,
                "gender": gender,
                "senior_citizen": senior_citizen,
                "partner": partner,
                "dependents": dependents,
                "tenure_months": tenure_months,
                "phone_service": phone_service,
                "multiple_lines": multiple_lines,
                "internet_service": internet_service,
                **add_on_values,
                "contract": contract,
                "paperless_billing": paperless_billing,
                "payment_method": payment_method,
                "monthly_charges": monthly_charge_value,
                "total_charges": total_charge_value,
            }
        )
        if not payload["customer_id"]:
            st.error("Informe um ID de cliente não vazio.")
            return

        try:
            with st.spinner("Calculando predição..."):
                result = predict(API_BASE_URL, payload)
            record_prediction(payload, result)
            render_result(result)
        except ApiTimeoutError as error:
            st.error(str(error))
        except ApiConnectionError as error:
            st.error(f"{error} Inicie o backend com `make serve`.")
        except ApiResponseError as error:
            st.error(f"Erro da API ({error.status_code}): {error}")

    render_prediction_history()


if __name__ == "__main__":
    main()
