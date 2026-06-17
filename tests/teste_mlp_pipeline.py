from sklearn.model_selection import train_test_split
from utils.app_logging import configurar_logging, logger
from config import LOGGING_LEVEL, set_seeds, TARGET, TEST_SIZE, RANDOM_STATE
import pandas as pd
from data.io import carregar_dados, load_pipeline
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.metrics import precision_recall_curve, auc

def main():
    configurar_logging(nivel=LOGGING_LEVEL)
    logger.info("Iniciando teste de load do pipeline com modelo MLP")

    df = carregar_dados()
    pipeline = load_pipeline()
    
    predict(df, pipeline)

    logger.info("Teste do pipeline com modelo MLP finalizado")


def predict(df: pd.DataFrame, pipeline):
    X = df.drop(columns=[TARGET], axis=1)
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE   # determinístico
    )

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