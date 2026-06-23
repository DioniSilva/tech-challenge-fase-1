import mlflow

from data.mlflow_config import MLPConfig
from data.training_output import TrainingOutput
from modeling.model_evaluator import ModelEvaluator
from modeling.model_factory import ModelFactory
from utils.mlflow_tracker import MLFlowTracker


class Trainer:
    def __init__(self, config: MLPConfig):
        self.config = config

    def train(
        self,
        X_train,
        y_train,
        X_test,
        y_test,
        threshold: float,
    ) -> TrainingOutput:

        pipeline = ModelFactory.create_pipeline(
            self.config,
            threshold,
        )

        model = pipeline.named_steps["model"]

        with mlflow.start_run(run_name=f"MLP_threshold_{threshold}") as run:
            pipeline.fit(
                X_train,
                y_train,
            )

            metrics = ModelEvaluator.evaluate(
                pipeline,
                X_test,
                y_test,
                threshold,
                run.info.run_id,
            )

            MLFlowTracker.log_training(
                pipeline=pipeline,
                model=model,
                config=self.config,
                metrics=metrics,
            )

        return TrainingOutput(
            pipeline=pipeline,
            metrics=metrics,
        )
