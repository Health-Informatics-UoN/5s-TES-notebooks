import pytest
import numpy as np
from numpy.testing import assert_almost_equal

from aggregate_utils import VarianceIntermediate

@pytest.fixture
def sample() -> np.ndarray:
    return np.random.rand(500) * 50

@pytest.fixture
def variance_intermediate(sample) -> VarianceIntermediate:
    return VarianceIntermediate(
            n=len(sample),
            total=np.sum(sample),
            sum_x2=np.sum(sample**2)
            )

def test_calculated_variance_similar(variance_intermediate, sample):
    sample_variance = np.var(sample)
    aggregate_variance = variance_intermediate.variance
    assert_almost_equal(sample_variance, aggregate_variance)
