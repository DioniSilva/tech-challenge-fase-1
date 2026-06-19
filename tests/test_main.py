import pandas as pd
import numpy as np

from main import train


def test_train_returns_fitted_pipeline():
    df = pd.DataFrame(
        {
            "feature_a": np.random.rand(30),
            "feature_b": np.random.rand(30),
            "feature_c": np.random.rand(30),
            "Total Charges": [float(i) for i in range(30)],
            "Churn Value": [0] * 15 + [1] * 15,
        }
    )

    pipeline = train(df)

    assert hasattr(pipeline, "predict")
    assert hasattr(pipeline, "predict_proba")

    predictions = pipeline.predict(df.drop(columns=["Churn Value"]))
    assert len(predictions) == len(df)
    assert set(predictions).issubset({0, 1})
