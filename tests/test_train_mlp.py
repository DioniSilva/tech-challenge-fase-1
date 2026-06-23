import pandas as pd
import numpy as np
import pytest

from train_mlp import calculate_metrics, select_best_model, train


def test_train_returns_fitted_pipeline_and_metrics():
    pytest.importorskip("torch")
    pytest.importorskip("imblearn")

    df = pd.DataFrame(
        {
            "feature_a": np.random.rand(30),
            "feature_b": np.random.rand(30),
            "feature_c": np.random.rand(30),
            "Total Charges": [float(i) for i in range(30)],
            "Churn Value": [0] * 15 + [1] * 15,
        }
    )

    pipeline, metrics = train(df)

    assert hasattr(pipeline, "predict")
    assert hasattr(pipeline, "predict_proba")
    assert isinstance(metrics, dict)
    assert set(metrics.keys()) == {
        "accuracy",
        "precision",
        "recall",
        "f1_score",
        "roc_auc",
        "pr_auc",
        "average_precision",
        "confidence_index",
    }

    predictions = pipeline.predict(df.drop(columns=["Churn Value"]))
    assert len(predictions) == len(df)
    assert set(predictions).issubset({0, 1})


def test_select_best_model_prefers_recall_then_pr_auc():
    results = [
        {"threshold": 0.3, "recall": 0.80, "pr_auc": 0.60},
        {"threshold": 0.45, "recall": 0.85, "pr_auc": 0.55},
        {"threshold": 0.7, "recall": 0.85, "pr_auc": 0.65},
    ]

    best = select_best_model(results)

    assert best["threshold"] == 0.7
    assert best["recall"] == 0.85
    assert best["pr_auc"] == 0.65


def test_calculate_metrics_returns_expected_keys():
    class DummyPipeline:
        def predict(self, X):
            return np.array([0 if i < len(X) / 2 else 1 for i in range(len(X))])

        def predict_proba(self, X):
            proba = np.linspace(0.1, 0.9, len(X))
            return np.vstack([1 - proba, proba]).T

    df = pd.DataFrame(
        {
            "feature_a": np.random.rand(20),
            "feature_b": np.random.rand(20),
            "feature_c": np.random.rand(20),
            "Total Charges": [float(i) for i in range(20)],
            "Churn Value": [0] * 10 + [1] * 10,
        }
    )

    pipeline = DummyPipeline()
    metrics = calculate_metrics(pipeline, df.drop(columns=["Churn Value"]), df["Churn Value"])

    assert isinstance(metrics["accuracy"], float)
    assert 0.0 <= metrics["precision"] <= 1.0
    assert 0.0 <= metrics["recall"] <= 1.0
    assert 0.0 <= metrics["f1_score"] <= 1.0
    assert 0.0 <= metrics["roc_auc"] <= 1.0
    assert 0.0 <= metrics["pr_auc"] <= 1.0
    assert 0.0 <= metrics["average_precision"] <= 1.0
    assert 0.0 <= metrics["confidence_index"] <= 1.0
