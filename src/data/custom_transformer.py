import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

from utils.app_logging import logger


class CustomTransformer(BaseEstimator, TransformerMixin):
    """
    Transformer personalizado para corrigir a feature 'total_charges' e remover features irrelevantes para o modelo MLP.
    - Corrige 'total_charges' convertendo para numérico e tratando valores não numéricos como 0.
    - Remove as seguintes features consideradas irrelevantes para o modelo:
        - 'customerID'
        - 'count'
        - 'country'
        - 'state'
        - 'city'
        - 'lat_long'
        - 'latitude'
        - 'longitude'
        - 'churn_label'
        - 'churn_score'
        - 'cltv'
        - 'churn_reason'
    """

    TOTAL_CHARGES = "total_charges"
    COLS_TO_DROP = [
        "customerid",
        "count",
        "country",
        "state",
        "city",
        "lat_long",
        "latitude",
        "longitude",
        "churn_label",
        "churn_score",
        "cltv",
        "churn_reason",
    ]

    def __init__(self):
        # não é necessário passar nada, mas é possível adicionar parâmetros para controlar o comportamento
        pass

    def fit(self, X, y=None):
        return self  # nada a aprender → self

    def transform(self, X):
        logger.info("Iniciando transformação dos dados")
        X = X.copy()
        X = self.padronizar_nomes_features(X)
        X[self.TOTAL_CHARGES] = self.corrigir_feature_total_charges(X)
        X = self.remover_features_irrelevantes(X)
        logger.info("Transformação dos dados concluída")
        return X

    def corrigir_feature_total_charges(self, X):
        logger.debug(
            "Corrigindo feature 'total_charges' convertendo para numérico e tratando valores não numéricos"
        )
        total_charges = pd.to_numeric(X[self.TOTAL_CHARGES], errors="coerce").fillna(0)
        return total_charges

    def remover_features_irrelevantes(self, X):
        logger.debug("Removendo features irrelevantes para o modelo")
        X = X.drop(columns=self.COLS_TO_DROP, errors="ignore")
        return X

    def padronizar_nomes_features(self, X):
        """
        Padroniza os nomes das colunas para lowercase e substitui espaços por underscores.
        """
        logger.info("Padronizando nomes das colunas")

        X.columns = [c.lower().replace(" ", "_") for c in X.columns]

        return X
