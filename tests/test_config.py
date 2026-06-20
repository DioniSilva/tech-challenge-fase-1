import numpy as np

import torch
from config import RANDOM_STATE, TEST_SIZE, TARGET, set_seeds


def test_config_constants():
    assert isinstance(RANDOM_STATE, int)
    assert isinstance(TEST_SIZE, float)
    assert isinstance(TARGET, str)


def test_set_seeds_produces_deterministic_results():
    set_seeds(123)
    first_random = np.random.rand()
    set_seeds(123)
    second_random = np.random.rand()

    assert first_random == second_random

    set_seeds(42)
    first_tensor = torch.rand(1).item()
    set_seeds(42)
    second_tensor = torch.rand(1).item()

    assert first_tensor == second_tensor
