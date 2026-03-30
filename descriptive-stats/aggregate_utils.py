from dataclasses import dataclass
from pathlib import Path
import json
from math import sqrt
from scipy.stats import t

@dataclass(frozen=True)
class MeanIntermediate:
    """A dataclass to hold the summary statistics sufficient to calculate the mean of a sample"""
    n: int
    total: float

    @property
    def mean(self) -> float:
        """
        Calculate the mean from the summary values

        Return
        ------
        float
            The mean of the sample
        """
        return self.total/self.n

@dataclass(frozen=True)
class VarianceIntermediate(MeanIntermediate):
    """A dataclass to hold the summary statistics sufficient to calculate the variance of a sample"""
    n: int
    total: float
    sum_x2: float

    @property
    def mean(self) -> float:
        """
        Calculate the mean from the summary values

        Return
        ------
        float
            The mean of the sample
        """
        return self.total/self.n

    @property
    def variance(self) -> float:
        """
        Calculate the variance from the summary values

        Return
        ------
        float
            The sample variance
        """
        return self.sum_x2/self.n - (self.total/self.n * self.total/self.n)

class SignificanceValue(float):
    def __new__(cls, value):
        if (value > 0) and (value < 1):
            return float.__new__(cls, value)
        else:
            raise ValueError(f"The significance value {value} can't be outside (0,1)")

class TTestIntermediate(VarianceIntermediate):

    @property
    def std_dev(self) -> float:
        return sqrt(self.variance)

    def t_statistic(self, value) -> float:
        return (self.mean - value)/(self.std_dev/sqrt(self.n))

    def one_sample_t_test(self, value) -> SignificanceValue:
        t_stat = self.t_statistic(value)
        sig = t.cdf(t_stat, df=self.n-1)
        return(SignificanceValue(sig))



def make_variance_intermediate_from_json(path: Path) -> VarianceIntermediate:
    """
    Take a JSON file, load it and build a VarianceIntermediate

    Parameters
    ----------
    path: Path
        The path to the JSON to be loaded

    Returns
    -------
    VarianceIntermediate
        A VarianceIntermediate for the JSON file
    """
    with open(path, "r") as f:
        return VarianceIntermediate(**json.load(f))

def aggregate_variance_intermediates(intermediates: list[VarianceIntermediate]) -> VarianceIntermediate:
    """
    Take a list of variance intermediates and combine them such that the result is what would be produced if the underlying data were a single sample.

    Parameters
    ----------
    intermediates: list[VarianceIntermediate]
        The VarianceIntermediate values to be aggregated

    Returns
    -------
    VarianceIntermediate
        A description of the overall sample
    """
    return VarianceIntermediate(
        n=sum([intermediate.n for intermediate in intermediates]),
        total=sum([intermediate.total for intermediate in intermediates]),
        sum_x2=sum([intermediate.sum_x2 for intermediate in intermediates])
    )
