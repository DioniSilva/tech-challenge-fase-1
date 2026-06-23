from dataclasses import dataclass

from data.training_result import TrainingResult


@dataclass
class TrainingOutput:
    pipeline: object
    metrics: TrainingResult
