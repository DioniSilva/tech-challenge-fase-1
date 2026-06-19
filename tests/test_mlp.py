import numpy as np
import pandas as pd

from modeling.mlp import TorchMLPClassifier


def test_torch_mlp_classifier_fit_predict_proba_predict():
    X = pd.DataFrame(
        {
            "feature_a": np.random.rand(20),
            "feature_b": np.random.rand(20),
            "feature_c": np.random.rand(20),
        }
    )
    y = np.array([0] * 10 + [1] * 10)

    classifier = TorchMLPClassifier(
        input_dim=3,
        hidden_dims=(16, 8),
        epochs=1,
        patience=1,
        batch_size=8,
        random_state=42,
        verbose=0,
    )

    fitted = classifier.fit(X, y)

    assert fitted is classifier
    assert classifier.is_fitted_
    assert classifier.n_features_in_ == 3
    assert list(classifier.classes_) == [0, 1]

    proba = classifier.predict_proba(X)
    assert proba.shape == (20, 2)
    assert np.allclose(proba.sum(axis=1), np.ones(20), atol=1e-6)

    preds = classifier.predict(X)
    assert preds.shape == (20,)
    assert set(preds).issubset({0, 1})


def test_torch_mlp_classifier_direct_smoke():
    X = pd.DataFrame(
        {
            "feature_a": np.random.rand(12),
            "feature_b": np.random.rand(12),
            "feature_c": np.random.rand(12),
        }
    )
    y = np.array([0, 1] * 6)

    classifier = TorchMLPClassifier(
        input_dim=3,
        hidden_dims=(8, 4),
        epochs=1,
        patience=1,
        batch_size=4,
        random_state=123,
        verbose=0,
    )

    classifier.fit(X, y)

    assert classifier.is_fitted_
    assert classifier.classes_.shape == (2,)

    proba = classifier.predict_proba(X)
    preds = classifier.predict(X)

    assert proba.shape == (12, 2)
    assert preds.shape == (12,)
    assert np.allclose(proba.sum(axis=1), np.ones(12), atol=1e-6)
    assert set(preds).issubset({0, 1})
