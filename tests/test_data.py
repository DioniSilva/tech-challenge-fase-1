import pandas as pd
from pathlib import Path
from sklearn.dummy import DummyClassifier

from data.io import load_pipeline, save_pipeline


def test_save_and_load_pipeline(tmp_path, monkeypatch):
    monkeypatch.setattr("data.io.MODELS_DIR", tmp_path)
    pipeline = DummyClassifier()

    save_pipeline(pipeline, name="test_pipeline.joblib")
    loaded = load_pipeline(name="test_pipeline.joblib")

    assert loaded.get_params() == pipeline.get_params()
    assert isinstance(loaded, DummyClassifier)
