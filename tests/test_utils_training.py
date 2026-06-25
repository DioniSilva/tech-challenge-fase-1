from types import SimpleNamespace
from unittest.mock import Mock

from data.mlp_config import MLPConfig
from data.training_result import TrainingResult
from utils.champion_selector import ChampionSelector
import utils.mlflow_tracker as mlflow_tracker


def make_output(threshold, recall, pr_auc):
    metrics = SimpleNamespace(threshold=threshold, recall=recall, pr_auc=pr_auc)
    return SimpleNamespace(metrics=metrics, pipeline=f"pipeline-{threshold}")


def test_champion_selector_prefers_recall_then_pr_auc():
    results = [
        make_output(0.45, recall=0.8, pr_auc=0.9),
        make_output(0.30, recall=0.9, pr_auc=0.5),
        make_output(0.70, recall=0.9, pr_auc=0.7),
    ]

    champion = ChampionSelector.select(results)

    assert champion.metrics.threshold == 0.70
    assert champion.pipeline == "pipeline-0.7"


def test_configure_mlflow_tracking_sets_uri_and_experiment(monkeypatch):
    set_tracking_uri = Mock()
    set_experiment = Mock()
    monkeypatch.setattr(mlflow_tracker.mlflow, "set_tracking_uri", set_tracking_uri)
    monkeypatch.setattr(mlflow_tracker.mlflow, "set_experiment", set_experiment)

    mlflow_tracker.MLFlowTracker.configure_mlflow_tracking()

    set_tracking_uri.assert_called_once_with("sqlite:///./data/mlflow_tracking/mlflow.db")
    set_experiment.assert_called_once_with("TechChallenge - Fase 01")


def test_log_training_logs_params_metrics_model_and_pipeline(monkeypatch):
    log_params = Mock()
    log_metrics = Mock()
    log_model = Mock()
    monkeypatch.setattr(mlflow_tracker.mlflow, "log_params", log_params)
    monkeypatch.setattr(mlflow_tracker.mlflow, "log_metrics", log_metrics)
    monkeypatch.setattr(mlflow_tracker.mlflow.sklearn, "log_model", log_model)

    class FakeModel:
        pass

    pipeline = object()
    model = FakeModel()
    config = MLPConfig(epochs=2, batch_size=8)
    metrics = TrainingResult(
        threshold=0.45,
        accuracy=0.91,
        precision=0.82,
        recall=0.73,
        f1_score=0.77,
        roc_auc=0.88,
        pr_auc=0.79,
        confidence_score=0.93,
        run_id="run-123",
    )

    mlflow_tracker.MLFlowTracker.log_training(pipeline, model, config, metrics)

    params = log_params.call_args.args[0]
    assert params["model_class"] == "FakeModel"
    assert params["hidden_dims"] == "(64, 32)"
    assert params["threshold"] == 0.45

    logged_metrics = log_metrics.call_args.args[0]
    assert logged_metrics["accuracy"] == 0.91
    assert logged_metrics["confidence_score"] == 0.93

    assert log_model.call_args_list[0].kwargs == {
        "sk_model": model,
        "artifact_path": "model",
        "serialization_format": mlflow_tracker.mlflow.sklearn.SERIALIZATION_FORMAT_CLOUDPICKLE,
    }
    assert log_model.call_args_list[1].kwargs == {
        "sk_model": pipeline,
        "artifact_path": "pipeline",
        "serialization_format": mlflow_tracker.mlflow.sklearn.SERIALIZATION_FORMAT_CLOUDPICKLE,
    }
