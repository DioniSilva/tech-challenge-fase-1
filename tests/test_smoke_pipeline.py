import numpy as np
import pandas as pd

from data.custom_transformer import CustomTransformer
from modeling.mlp import TorchMLPClassifier
from modeling.pipeline import build_pipeline, build_preprocessor


def test_smoke_pipeline_end_to_end():
    # Dados sintéticos com features numéricas, categóricas e a coluna total_charges.
    df = pd.DataFrame(
        {
            "CustomerID": ["A001", "A002", "A003", "A004", "A005", "A006", "A007", "A008"],
            "Total Charges": ["100.0", "250.5", "N/A", "300", "0", "120.0", "420.1", "180"],
            "State": ["SP", "RJ", "MG", "SP", "RJ", "MG", "SP", "RJ"],
            "Gender": ["Male", "Female", "Female", "Male", "Female", "Male", "Female", "Male"],
            "Some Feature": [1, 2, 3, 4, 5, 6, 7, 8],
            "Churn Value": [0, 1, 0, 1, 0, 1, 0, 1],
        }
    )

    transformer = CustomTransformer()
    transformed = transformer.transform(df)

    assert "total_charges" in transformed.columns
    assert "customerid" not in transformed.columns
    assert "state" not in transformed.columns
    assert transformed["total_charges"].tolist() == [100.0, 250.5, 0.0, 300.0, 0.0, 120.0, 420.1, 180.0]

    preprocessor = build_preprocessor()
    transformed_array = preprocessor.fit_transform(transformed.drop(columns=["churn_value"]))
    assert transformed_array.shape[0] == transformed.shape[0]

    model = TorchMLPClassifier(
        input_dim=transformed_array.shape[1],
        hidden_dims=(16, 8),
        epochs=1,
        patience=1,
        batch_size=4,
        random_state=42,
        verbose=0,
    )
    pipeline = build_pipeline(model)
    pipeline.fit(transformed.drop(columns=["churn_value"]), transformed["churn_value"])

    predictions = pipeline.predict(transformed.drop(columns=["churn_value"]))
    proba = pipeline.predict_proba(transformed.drop(columns=["churn_value"]))

    assert predictions.shape[0] == transformed.shape[0]
    assert proba.shape == (transformed.shape[0], 2)
    assert set(predictions).issubset({0, 1})
    assert np.allclose(proba.sum(axis=1), np.ones(transformed.shape[0]), atol=1e-6)
