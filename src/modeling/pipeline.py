from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer, make_column_selector
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from config import RANDOM_STATE
from data.custom_transformer import CustomTransformer
from utils.app_logging import logger


def build_preprocessor():
    logger.info("Construindo preprocessor para o pipeline")
    return ColumnTransformer(
        transformers=[
            (
                "numerics",
                StandardScaler(),
                make_column_selector(dtype_include=["int64", "float64"]),
            ),
            (
                "categoricals",
                OneHotEncoder(handle_unknown="ignore"),
                make_column_selector(dtype_include=["object"]),
            ),
        ],
        remainder="passthrough",
    )


def build_balancer():
    logger.info("Construindo balanceador SMOTE")
    return SMOTE(random_state=RANDOM_STATE)


def build_pipeline(model):
    return Pipeline(
        steps=[
            ("customTransformer", CustomTransformer()),
            ("preprocessor", build_preprocessor()),
            ("balancer", build_balancer()),
            ("model", model),
        ],
        memory=None,
    )
