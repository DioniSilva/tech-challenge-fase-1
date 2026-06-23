import mlflow
import mlflow.sklearn

from config import MLFLOW_DB_PATH_AND_NAME
from data.mlp_config import MLPConfig
from data.training_result import TrainingResult


class MLFlowTracker:
    @staticmethod
    def configure_mlflow_tracking():
        mlflow.set_tracking_uri(f"sqlite:///{MLFLOW_DB_PATH_AND_NAME}")
        mlflow.set_experiment("TechChallenge - Fase 01")

    @staticmethod
    def log_training(
        pipeline,
        model,
        config: MLPConfig,
        metrics: TrainingResult,
    ):

        #
        # Hyperparameters
        #
        mlflow.log_params(
            {
                "model_class": model.__class__.__name__,
                "hidden_dims": str(config.hidden_dims),
                "dropouts": str(config.dropouts),
                "lr": config.lr,
                "weight_decay": config.weight_decay,
                "batch_size": config.batch_size,
                "epochs": config.epochs,
                "patience": config.patience,
                "min_delta": config.min_delta,
                "random_state": config.random_state,
                "threshold": metrics.threshold,
            }
        )

        #
        # Metrics
        #
        mlflow.log_metrics(
            {
                "accuracy": metrics.accuracy,
                "precision": metrics.precision,
                "recall": metrics.recall,
                "f1_score": metrics.f1_score,
                "roc_auc": metrics.roc_auc,
                "pr_auc": metrics.pr_auc,
                "confidence_score": metrics.confidence_score,
            }
        )

        #
        # Modelo isolado
        #
        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="model",
        )

        #
        # Pipeline completo
        #
        mlflow.sklearn.log_model(
            sk_model=pipeline,
            artifact_path="pipeline",
        )
