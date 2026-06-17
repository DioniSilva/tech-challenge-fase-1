import logging as _std_logging

# Named logger used across the project
logger = _std_logging.getLogger("main")

def configurar_logging(nivel=_std_logging.INFO):
    """
    Configura o logger global. Pode ser chamado múltiplas vezes
    para resetar as configurações durante a sessão.
    """
    # Limpa handlers existentes para evitar duplicação de logs
    if logger.hasHandlers():
        logger.handlers.clear()

    logger.setLevel(nivel)
    logger.propagate = False

    # Define o formato
    formatter = _std_logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Handler para o console (saída no notebook)
    stream_handler = _std_logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

# Re-export some stdlib names that callers may expect from `logging`
getLogger = _std_logging.getLogger
INFO = _std_logging.INFO
DEBUG = _std_logging.DEBUG
WARNING = _std_logging.WARNING
ERROR = _std_logging.ERROR
