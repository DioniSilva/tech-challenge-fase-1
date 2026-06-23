from dataclasses import dataclass


@dataclass
class TrainingResult:
    threshold: float
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    roc_auc: float
    pr_auc: float
    confidence_score: float
    run_id: str
