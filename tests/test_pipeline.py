from sklearn.preprocessing import OneHotEncoder, StandardScaler
from imblearn.over_sampling import SMOTE

from data.custom_transformer import CustomTransformer
from modeling.mlp import TorchMLPClassifier
from modeling.pipeline import build_balancer, build_pipeline, build_preprocessor


def test_build_preprocessor_contains_scaler_and_encoder():
    preprocessor = build_preprocessor()

    transformers = {name for name, _, _ in preprocessor.transformers}
    assert "numerics" in transformers
    assert "categoricals" in transformers

    numeric_transformer = preprocessor.transformers[0][1]
    categorical_transformer = preprocessor.transformers[1][1]

    assert isinstance(numeric_transformer, StandardScaler)
    assert isinstance(categorical_transformer, OneHotEncoder)


def test_build_balancer_returns_smote():
    balanced = build_balancer()
    assert isinstance(balanced, SMOTE)
    assert balanced.random_state is not None


def test_build_pipeline_steps_are_correct():
    pipeline = build_pipeline(TorchMLPClassifier(input_dim=2, epochs=1, patience=1, random_state=0))
    step_names = [name for name, _ in pipeline.steps]

    assert step_names == ["customTransformer", "preprocessor", "balancer", "model"]
    assert isinstance(pipeline.named_steps["customTransformer"], CustomTransformer)
