import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    auc,
    f1_score,
    precision_recall_curve,
    precision_score,
    recall_score,
    roc_auc_score,
)

from data.training_result import TrainingResult


class ModelEvaluator:
    @staticmethod
    def evaluate(
        pipeline,
        X_test,
        y_test,
        threshold: float,
        run_id: str,
    ) -> TrainingResult:

        y_pred = pipeline.predict(X_test)
        y_proba = pipeline.predict_proba(X_test)[:, 1]

        precision_curve, recall_curve, _ = precision_recall_curve(y_test, y_proba)

        confidence_score = pd.Series(y_proba).apply(lambda p: max(p, 1 - p)).mean()

        return TrainingResult(
            threshold=threshold,
            accuracy=accuracy_score(y_test, y_pred),
            precision=precision_score(y_test, y_pred, zero_division=0),
            recall=recall_score(y_test, y_pred, zero_division=0),
            f1_score=f1_score(y_test, y_pred, zero_division=0),
            roc_auc=roc_auc_score(y_test, y_proba),
            pr_auc=auc(recall_curve, precision_curve),
            confidence_score=confidence_score,
            run_id=run_id,
        )
