from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

from incidence_prevalence import IncidenceResult
from summarised_result import SummarisedResult

def load_5s_tes_incidence_result(result_paths: dict[str, list[Path]], incidence_index: int=0) -> dict[str, IncidenceResult]:
    data = {k: SummarisedResult(pd.read_csv(v[incidence_index])) for k, v in result_paths.items()}
    return {k: IncidenceResult.from_summarised_result(v) for k,v in data.items()}

def plot_incidence_results(results: dict[str, IncidenceResult], date_range: tuple[pd.Timestamp, pd.Timestamp] | None = None):
    _, axs = plt.subplots(figsize=(12,12), nrows=len(results))
    for i, (ds_name, ds) in enumerate(results.items()):
        ds.plot_incidence(date_range = date_range, axes=axs[i])
        axs[i].set_title(ds_name)
    plt.show()
