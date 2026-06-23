from contextlib import contextmanager
from types import SimpleNamespace
from unittest.mock import Mock

import numpy as np
import pandas as pd
import pytest

from data.mlflow_config import MLPConfig
from data.training_result import TrainingResult
from modeling.model_evaluator import ModelEvaluator
import modeling.model_factory as model_factory
import modeling.trainer as trainer_module


class DummyPipeline:
    def predict(self, X):
        return np.array([0, 1, 1, 0])[: len(X)]

    def predict_proba(self, X):
        positive = np.array([0.1, 0.8, 0.7, 0.4])[: len(X)]
        return np.column_stack([1 - positive, positive])


def test_model_evaluator_returns_expected_training_result():
    X_test = pd.DataFrame({"feature": [1, 2, 3, 4]})
    y_test = np.array([0, 1, 1, 0])

    result = ModelEvaluator.evaluate(DummyPipeline(), X_test, y_test, 0.45, "run-abc")

    assert isinstance(result, TrainingResult)
    assert result.threshold == 0.45
    assert result.run_id == "run-abc"
    assert result.accuracy == 1.0
    assert result.precision == 1.0
    assert result.recall == 1.0
    assert result.f1_score == 1.0
    assert result.roc_auc == 1.0
    assert result.pr_auc == pytest.approx(1.0)
    assert result.confidence_score == pytest.approx(0.75)


def test_model_factory_builds_pipeline_with_configured_mlp(monkeypatch):
    created_models = []

    class FakeTorchMLPClassifier:
        def __init__(self, **kwargs):
            self.kwargs = kwargs
            created_models.append(self)

    build_pipeline = Mock(return_value="pipeline")
    monkeypatch.setattr(model_factory, "TorchMLPClassifier", FakeTorchMLPClassifier)
    monkeypatch.setattr(model_factory, "build_pipeline", build_pipeline)

    config = MLPConfig(
        hidden_dims=(8, 4),
        dropouts=(0.1, 0.0),
        lr=0.01,
        weight_decay=0.02,
        batch_size=16,
        epochs=3,
        patience=2,
        min_delta=0.005,
        random_state=123,
    )

    pipeline = model_factory.ModelFactory.create_pipeline(config, threshold=0.3)

    assert pipeline == "pipeline"
    assert created_models[0].kwargs == {
        "hidden_dims": (8, 4),
        "dropouts": (0.1, 0.0),
        "lr": 0.01,
        "weight_decay": 0.02,
        "batch_size": 16,
        "epochs": 3,
        "patience": 2,
        "min_delta": 0.005,
        "random_state": 123,
        "threshold": 0.3,
    }
    build_pipeline.assert_called_once_with(created_models[0])


def test_trainer_runs_pipeline_evaluates_and_logs(monkeypatch):
    pipeline = Mock()
    model = object()
    pipeline.named_steps = {"model": model}
    metrics = TrainingResult(0.45, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.9, "run-1")
    run = SimpleNamespace(info=SimpleNamespace(run_id="run-1"))

    @contextmanager
    def fake_start_run(run_name):
        assert run_name == "MLP_threshold_0.45"
        yield run

    create_pipeline = Mock(return_value=pipeline)
    evaluate = Mock(return_value=metrics)
    log_training = Mock()

    monkeypatch.setattr(trainer_module.ModelFactory, "create_pipeline", create_pipeline)
    monkeypatch.setattr(trainer_module.mlflow, "start_run", fake_start_run)
    monkeypatch.setattr(trainer_module.ModelEvaluator, "evaluate", evaluate)
    monkeypatch.setattr(trainer_module.MLFlowTracker, "log_training", log_training)

    config = MLPConfig(epochs=1)
    trainer = trainer_module.Trainer(config)

    output = trainer.train("X_train", "y_train", "X_test", "y_test", threshold=0.45)

    create_pipeline.assert_called_once_with(config, 0.45)
    pipeline.fit.assert_called_once_with("X_train", "y_train")
    evaluate.assert_called_once_with(pipeline, "X_test", "y_test", 0.45, "run-1")
    log_training.assert_called_once_with(
        pipeline=pipeline,
        model=model,
        config=config,
        metrics=metrics,
    )
    assert output.pipeline is pipeline
    assert output.metrics is metrics
