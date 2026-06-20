import contextvars
import datetime as _dt
import json
import logging as _std_logging
import time

# Named logger used across the project
logger = _std_logging.getLogger("main")

request_id_var = contextvars.ContextVar("request_id", default=None)
client_ip_var = contextvars.ContextVar("client_ip", default=None)
endpoint_var = contextvars.ContextVar("endpoint", default=None)
start_time_var = contextvars.ContextVar("start_time", default=None)


class RequestContextFilter(_std_logging.Filter):
    def filter(self, record):
        record.request_id = request_id_var.get() or ""
        record.client_ip = client_ip_var.get() or ""
        record.endpoint = endpoint_var.get() or ""
        start_time = start_time_var.get()
        record.latency_ms = (
            round((time.monotonic() - start_time) * 1000) if start_time is not None else None
        )
        return True


class StructuredJsonFormatter(_std_logging.Formatter):
    def __init__(self, service_name: str = "telco-churn-API"):
        super().__init__()
        self.service_name = service_name

    def format(self, record):
        payload = {
            "timestamp": _dt.datetime.utcfromtimestamp(record.created)
            .replace(microsecond=0)
            .isoformat()
            + "Z",
            "level": record.levelname,
            "service": self.service_name,
            "endpoint": getattr(record, "endpoint", ""),
            "client_ip": getattr(record, "client_ip", ""),
            "request_id": getattr(record, "request_id", ""),
            "message": record.getMessage(),
            "latency_ms": getattr(record, "latency_ms", None),
        }
        return json.dumps(payload, ensure_ascii=False)


def set_request_context(request_id: str, client_ip: str, endpoint: str):
    return (
        request_id_var.set(request_id),
        client_ip_var.set(client_ip),
        endpoint_var.set(endpoint),
        start_time_var.set(time.monotonic()),
    )


def clear_request_context(tokens):
    request_id_var.reset(tokens[0])
    client_ip_var.reset(tokens[1])
    endpoint_var.reset(tokens[2])
    start_time_var.reset(tokens[3])


def configurar_logging(
    nivel=_std_logging.INFO, json_formatter: bool = False, service_name: str = "main"
):
    """
    Configura o logger global. Pode ser chamado múltiplas vezes
    para resetar as configurações durante a sessão.
    """
    # Limpa handlers existentes para evitar duplicação de logs
    if logger.hasHandlers():
        logger.handlers.clear()

    logger.setLevel(nivel)
    logger.propagate = False

    if json_formatter:
        formatter = StructuredJsonFormatter(service_name=service_name)
        stream_handler = _std_logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        stream_handler.addFilter(RequestContextFilter())
    else:
        formatter = _std_logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        stream_handler = _std_logging.StreamHandler()
        stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)


# Re-export some stdlib names that callers may expect from `logging`
getLogger = _std_logging.getLogger
INFO = _std_logging.INFO
DEBUG = _std_logging.DEBUG
WARNING = _std_logging.WARNING
ERROR = _std_logging.ERROR
