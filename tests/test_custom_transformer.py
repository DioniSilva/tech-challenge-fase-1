import pandas as pd
from pandera.pandas import Column, DataFrameSchema

from data.custom_transformer import CustomTransformer


def test_custom_transformer_transform_cleans_and_drops_columns():
    df = pd.DataFrame(
        {
            "CustomerID": ["A001", "A002"],
            "Total Charges": ["100.0", "N/A"],
            "State": ["SP", "RJ"],
            "Some Feature": [1, 2],
            "Churn Value": [0, 1],
        }
    )

    transformer = CustomTransformer()
    transformed = transformer.transform(df)

    assert "customerid" not in transformed.columns
    assert "state" not in transformed.columns
    assert "total_charges" in transformed.columns
    assert "some_feature" in transformed.columns
    assert transformed["total_charges"].tolist() == [100.0, 0.0]

    schema = DataFrameSchema(
        {
            "total_charges": Column(float, coerce=True),
            "some_feature": Column(int),
            "churn_value": Column(int),
        },
        coerce=True,
    )

    validated = schema.validate(transformed)
    assert list(validated.columns) == ["total_charges", "some_feature", "churn_value"]
