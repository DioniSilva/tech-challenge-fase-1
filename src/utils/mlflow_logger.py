import logging
import os

import matplotlib.pyplot as plt
import mlflow
import mlflow.data
from mlflow.models import infer_signature
import mlflow.pytorch
import mlflow.sklearn
import numpy as np
import pandas as pd
from sklearn.metrics import ConfusionMatrixDisplay, RocCurveDisplay, classification_report

logger = logging.getLogger(__name__)


class MLflowLogger:
    """
    Classe utilitária para gerenciar o ciclo de vida de experimentos, logs de métricas,
    artefatos geográficos/gráficos e governança de modelos no MLflow.
    Centraliza os dados estritamente em 'data/mlflow_tracking'.
    """

    # Flag para garantir que a inicialização ocorra apenas uma vez
    _tracking_initialized = False

    @classmethod
    def initialize_tracking(cls, experiment_name: str = "ML Experiments"):
        """Configura MLflow para usar SQLite em 'data/mlflow_tracking/mlflow.db'."""
        if cls._tracking_initialized:
            return

        # Encontra a raiz do projeto: src/utils/../.. = projeto root
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        tracking_path = os.path.join(project_root, "data", "mlflow_tracking")
        db_path = os.path.join(tracking_path, "mlflow.db")
        artifact_path = os.path.join(tracking_path, "artifacts", experiment_name)

        os.makedirs(artifact_path, exist_ok=True)
        mlflow.set_tracking_uri(f"sqlite:///{db_path}")

        try:
            if mlflow.get_experiment_by_name(experiment_name) is None:
                mlflow.create_experiment(
                    experiment_name,
                    artifact_location=f"file://{artifact_path}",
                )

            mlflow.set_experiment(experiment_name)
            cls._tracking_initialized = True
            logger.info("MLflow configured", extra={"tracking_uri": f"sqlite:///{db_path}"})
        except Exception as e:
            logger.warning("MLflow experiment configuration failed", extra={"error": str(e)})

    @staticmethod
    def _log_figure(fig, artifact_name: str, show_plots: bool):
        """Salva figura no MLflow e gerencia sua exibição."""
        mlflow.log_figure(fig, artifact_name)
        plt.show() if show_plots else plt.close(fig)

    @classmethod
    def log_run(
        cls,
        model,
        hyper_params: dict,
        metrics: dict,
        X_train_df: pd.DataFrame,
        X_test_df: pd.DataFrame,
        y_test: np.ndarray | list,
        y_pred_test: np.ndarray | list,
        y_prob_test: np.ndarray | list,
        importance_df: pd.DataFrame | None = None,
        fairness_metrics: dict | None = None,
        experiment_metadata: dict | None = None,
        show_plots: bool = True,
    ):
        """Registra experimento completo no MLflow."""
        experiment_metadata = experiment_metadata or {}

        # Extrai metadados com defaults
        experiment_name = experiment_metadata.get("experiment_name", "ML Experiments")
        model_name = experiment_metadata.get("model_name", "Default Model")
        run_name = experiment_metadata.get("run_name", "Default Run")

        print(f"📋 Experiment: '{experiment_name}' | Model: '{model_name}' | Run: '{run_name}'")

        cls.initialize_tracking(experiment_name)
        mlflow.set_experiment(experiment_name)

        if mlflow.active_run():
            mlflow.end_run()

        with mlflow.start_run(run_name=run_name):
            # Tags estruturadas
            mlflow.set_tags(
                {
                    "mlflow.runName": run_name,
                    "model_name": model_name,
                    "experiment_name": experiment_name,
                    "framework": "PyTorch" if "torch" in model.model_type_str else "Scikit-Learn",
                    **experiment_metadata.get("experiment_tags", {}),
                    **{
                        k: experiment_metadata.get(k)
                        for k in ["experiment_description", "model_description", "run_description"]
                        if experiment_metadata.get(k)
                    },
                }
            )

            # Log de dados e métricas
            mlflow.log_params(hyper_params)
            mlflow.log_metrics(metrics)
            if fairness_metrics:
                mlflow.log_metrics(fairness_metrics)

            # Data Lineage
            mlflow.log_input(
                mlflow.data.from_pandas(X_train_df, name=f"{model_name}_train"), "training"
            )
            mlflow.log_input(
                mlflow.data.from_pandas(X_test_df, name=f"{model_name}_test"), "testing"
            )

            # Gera plots
            cls._create_and_log_plots(
                y_test, y_pred_test, y_prob_test, importance_df, model_name, show_plots
            )

            # Classification Report
            report_df = pd.DataFrame(
                classification_report(y_test, y_pred_test, output_dict=True)
            ).transpose()
            mlflow.log_table(report_df, "classification_report.json")

            # Salva modelo com assinatura
            signature = infer_signature(X_train_df, y_pred_test)
            is_torch = "torch" in model.model_type_str
            description = (
                f"Modelo de Rede Neural para Previsão de Churn.\n\n{str(model)}"
                if is_torch
                else f"Modelo de ML para Previsão de Churn.\n\n{str(model.__class__.__name__)}"
            )

            mlflow.set_tag("mlflow.note.content", description)
            if is_torch:
                mlflow.pytorch.log_model(model, artifact_path=model_name, signature=signature)
            else:
                mlflow.sklearn.log_model(model, artifact_path=model_name, signature=signature)

        logger.info("MLflow run registered", extra={"tracking_store": "data/mlflow_tracking"})

    @classmethod
    def _create_and_log_plots(
        cls, y_test, y_pred_test, y_prob_test, importance_df, model_name, show_plots
    ):
        """Cria e loga plots de avaliação."""
        # Confusion Matrix
        fig, ax = plt.subplots(figsize=(8, 6))
        ConfusionMatrixDisplay.from_predictions(y_test, y_pred_test, ax=ax)
        ax.set_title(f"Confusion Matrix - {model_name}")
        cls._log_figure(fig, "confusion_matrix.png", show_plots)

        # ROC Curve
        fig, ax = plt.subplots(figsize=(8, 6))
        RocCurveDisplay.from_predictions(y_test, y_prob_test, ax=ax)
        ax.set_title(f"ROC Curve - {model_name}")
        cls._log_figure(fig, "roc_curve.png", show_plots)

        # Feature Importance (se disponível)
        if importance_df is not None:
            mlflow.log_table(importance_df, "feature_importance.json")

            top_features = importance_df.head(15).sort_values(
                by="absolute_importance", ascending=True
            )
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.barh(top_features["feature"], top_features["absolute_importance"])
            ax.set_title(f"Top 15 Feature Importances - {model_name}")
            ax.set_xlabel("Absolute Importance / Weight Magnitude")
            cls._log_figure(fig, "feature_importance_top15.png", show_plots)
