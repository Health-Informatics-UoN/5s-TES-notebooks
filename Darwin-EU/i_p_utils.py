from functools import reduce
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from incidence_prevalence import IncidenceResult
from incidence_prevalence.incidence_partial import IncidencePartial
from matplotlib.axes import Axes
from summarised_result import SummarisedResult


def load_5s_tes_incidence_result(
    result_paths: dict[str, list[Path]], incidence_index: int = 0
) -> dict[str, IncidenceResult]:
    data = {
        k: SummarisedResult(pd.read_csv(v[incidence_index]))
        for k, v in result_paths.items()
    }
    return {k: IncidenceResult.from_summarised_result(v) for k, v in data.items()}


def plot_incidence_results(
    results: dict[str, IncidenceResult],
    date_range: tuple[pd.Timestamp, pd.Timestamp] | None = None,
):
    _, axs = plt.subplots(figsize=(12, 12), nrows=len(results))
    for i, (ds_name, ds) in enumerate(results.items()):
        ds.plot_incidence(date_range=date_range, axes=axs[i])
        axs[i].set_title(ds_name)
    plt.show()


def combine_incidence_results(
    incidence_results: list[IncidenceResult],
) -> IncidenceResult:
    settings = incidence_results[0].settings
    incidence_result_id = incidence_results[0].incidence_result_id
    partials: list[IncidencePartial] = [
        IncidencePartial(res.results) for res in incidence_results
    ]
    combined = reduce(lambda a, b: a + b, partials).finalise()
    return IncidenceResult(settings, incidence_result_id, combined)


def plot_jittered(
    incidence_result: IncidenceResult,
    time_column: str = "incidence_start_date",
    offset_weeks: int = 6,
    ax: Axes | None = None,
):
    jittered = IncidenceResult(
        incidence_result.settings,
        incidence_result.incidence_result_id,
        incidence_result.results.copy(),
    )
    if offset_weeks >= 0:
        jittered.results[time_column] = jittered.results[time_column] + pd.Timedelta(
            weeks=offset_weeks
        )
    else:
        jittered.results[time_column] = jittered.results[time_column] - pd.Timedelta(
            weeks=abs(offset_weeks)
        )

    jittered.plot_incidence(axes=ax)
