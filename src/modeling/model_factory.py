from data.mlflow_config import MLPConfig
from modeling.mlp import TorchMLPClassifier
from modeling.pipeline import build_pipeline


class ModelFactory:
    @staticmethod
    def create_pipeline(
        config: MLPConfig,
        threshold: float,
    ):

        model = TorchMLPClassifier(
            hidden_dims=config.hidden_dims,
            dropouts=config.dropouts,
            lr=config.lr,
            weight_decay=config.weight_decay,
            batch_size=config.batch_size,
            epochs=config.epochs,
            patience=config.patience,
            min_delta=config.min_delta,
            random_state=config.random_state,
            threshold=threshold,
        )

        return build_pipeline(model)
