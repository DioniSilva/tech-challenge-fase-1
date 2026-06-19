from sklearn.model_selection import train_test_split
from modeling.pipeline import build_pipeline
from utils.app_logging import configurar_logging, logger
from config import LOGGING_LEVEL, set_seeds, TARGET, TEST_SIZE, RANDOM_STATE
import pandas as pd
from data.io import carregar_dados, save_pipeline
from modeling.mlp import TorchMLPClassifier
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.metrics import precision_recall_curve, auc

def main():
    configurar_logging(nivel=LOGGING_LEVEL)
    logger.info("Iniciando o pipeline de treinamento do modelo MLP")

    set_seeds()
    df = carregar_dados()
    pipeline = train(df)
    save_pipeline(pipeline)

    logger.info("Pipeline de treinamento do modelo MLP finalizado")


def train(df: pd.DataFrame):
    X = df.drop(columns=[TARGET], axis=1)
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE   # determinístico
    )

    pipeline = build_pipeline(TorchMLPClassifier(threshold=0.45, random_state=RANDOM_STATE, verbose=1))
    pipeline.fit(X_train, y_train)

    print_metrics(pipeline, X_test, y_test)

    return pipeline


def print_metrics(pipeline, X_test, y_test):
    y_pred = pipeline.predict(X_test)
    y_proba = pipeline.predict_proba(X_test)[:, 1]

    logger.debug(f"Relatório de Classificação:\n{classification_report(y_test, y_pred)}")
    logger.debug(f"AUC-ROC: {roc_auc_score(y_test, y_proba):.4f}")

    precision, recall, _ = precision_recall_curve(y_test, y_proba)
    pr_auc = auc(recall, precision)

    logger.debug(f"PR-AUC: {pr_auc:.4f}")


if __name__ == "__main__":
    main()