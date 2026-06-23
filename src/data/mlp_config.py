from dataclasses import dataclass

from config import RANDOM_STATE


@dataclass(frozen=True)
class MLPConfig:
    hidden_dims: tuple[int, ...] = (64, 32)
    dropouts: tuple[float, ...] = (0.3, 0.2)
    lr: float = 1e-3
    weight_decay: float = 1e-5
    batch_size: int = 64
    epochs: int = 100
    patience: int = 5
    min_delta: float = 1e-3
    random_state: int = RANDOM_STATE
