from pathlib import Path

import pandas as pd
from sklearn.dummy import DummyClassifier

from data.io import carregar_dados, load_pipeline, save_pipeline


def test_carregar_dados_calls_read_excel(monkeypatch):
    expected = pd.DataFrame({"col": [1, 2, 3]})

    def fake_read_excel(path):
        assert isinstance(path, Path)
        return expected

    monkeypatch.setattr("data.io.pd.read_excel", fake_read_excel)
    result = carregar_dados()
    assert result is expected


def test_save_pipeline_and_load_pipeline(tmp_path, monkeypatch):
    monkeypatch.setattr("data.io.MODELS_DIR", tmp_path)
    pipeline = DummyClassifier()

    save_pipeline(pipeline, name="test_pipeline.joblib")
    loaded = load_pipeline(name="test_pipeline.joblib")

    assert isinstance(loaded, DummyClassifier)
    assert loaded.get_params() == pipeline.get_params()
