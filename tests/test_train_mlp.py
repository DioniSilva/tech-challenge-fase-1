from types import SimpleNamespace
from unittest.mock import Mock

import pandas as pd

from data.training_result import TrainingResult
import train_mlp


def make_result(threshold, recall, pr_auc):
    return TrainingResult(
        threshold=threshold,
        accuracy=0.8,
        precision=0.7,
        recall=recall,
        f1_score=0.75,
        roc_auc=0.82,
        pr_auc=pr_auc,
        confidence_score=0.9,
        run_id=f"run-{threshold}",
    )


def test_print_comparison_logs_sorted_champion(monkeypatch):
    logger = Mock()
    monkeypatch.setattr(train_mlp, "logger", logger)

    results = [
        make_result(0.45, recall=0.7, pr_auc=0.8),
        make_result(0.30, recall=0.9, pr_auc=0.6),
        make_result(0.70, recall=0.9, pr_auc=0.9),
    ]

    train_mlp.print_comparison(results)

    assert logger.info.call_count == 2
    champion_log_args = logger.info.call_args_list[1].args
    assert champion_log_args[1:] == (0.70, 0.9, 0.9)


def test_main_trains_thresholds_selects_champion_and_saves_pipeline(monkeypatch):
    df = pd.DataFrame(
        {
            "feature_a": range(10),
            "feature_b": range(10, 20),
            train_mlp.TARGET: [0, 1] * 5,
        }
    )
    outputs = [
        SimpleNamespace(pipeline="pipeline-045", metrics=make_result(0.45, 0.5, 0.7)),
        SimpleNamespace(pipeline="pipeline-030", metrics=make_result(0.30, 0.8, 0.6)),
        SimpleNamespace(pipeline="pipeline-070", metrics=make_result(0.70, 0.8, 0.9)),
    ]

    trainer_instance = Mock()
    trainer_instance.train.side_effect = outputs
    trainer_class = Mock(return_value=trainer_instance)
    save_pipeline = Mock()
    print_comparison = Mock()

    monkeypatch.setattr(train_mlp, "configurar_logging", Mock())
    monkeypatch.setattr(train_mlp, "set_seeds", Mock())
    monkeypatch.setattr(train_mlp.MLFlowTracker, "configure_mlflow_tracking", Mock())
    monkeypatch.setattr(train_mlp, "carregar_dados", Mock(return_value=df))
    monkeypatch.setattr(train_mlp, "Trainer", trainer_class)
    monkeypatch.setattr(train_mlp, "save_pipeline", save_pipeline)
    monkeypatch.setattr(train_mlp, "print_comparison", print_comparison)

    train_mlp.main()

    assert trainer_class.call_count == 1
    assert [call.args[-1] for call in trainer_instance.train.call_args_list] == [
        0.45,
        0.30,
        0.70,
    ]
    save_pipeline.assert_called_once_with("pipeline-070")
    print_comparison.assert_called_once_with([output.metrics for output in outputs])
