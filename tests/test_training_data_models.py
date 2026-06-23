from dataclasses import FrozenInstanceError

import pytest

from data import mlflow_config, mlp_config
from data.training_output import TrainingOutput
from data.training_result import TrainingResult


@pytest.mark.parametrize("module", [mlflow_config, mlp_config])
def test_mlp_config_defaults_are_frozen(module):
    config = module.MLPConfig()

    assert config.hidden_dims == (64, 32)
    assert config.dropouts == (0.3, 0.2)
    assert config.lr == 1e-3
    assert config.weight_decay == 1e-5
    assert config.batch_size == 64
    assert config.epochs == 100
    assert config.patience == 5
    assert config.min_delta == 1e-3

    with pytest.raises(FrozenInstanceError):
        config.lr = 0.1


def test_training_result_stores_metrics():
    result = TrainingResult(
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

    assert result.threshold == 0.45
    assert result.run_id == "run-123"
    assert result.confidence_score == 0.93


def test_training_output_groups_pipeline_and_metrics():
    metrics = TrainingResult(0.5, 0.9, 0.8, 0.7, 0.75, 0.85, 0.86, 0.92, "run-1")
    pipeline = object()

    output = TrainingOutput(pipeline=pipeline, metrics=metrics)

    assert output.pipeline is pipeline
    assert output.metrics is metrics
