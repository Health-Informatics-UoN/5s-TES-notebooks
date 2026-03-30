import json
from pathlib import Path
import pandas as pd

class ContingencyTable:
    def __init__(self, data) -> None:
        self.data = data

    @property
    def contingency_table(self) -> pd.DataFrame:
        variables = list(self.data.columns)
        variables.remove("n")

        return self.data.pivot(index=variables[0], columns=variables[1])

def read_contingency_table_from_json(filepath: str) -> ContingencyTable:
    path = Path(filepath)
    with open(path, "r") as f:
        return ContingencyTable(pd.DataFrame(json.load(f)))


def aggregate_tables(tables: list[ContingencyTable]) -> ContingencyTable:
    variables = set(tables[0].data.columns)
    for table in tables:
        if set(table.data.columns) != variables:
            raise ValueError(f"Variables {set(table.data.columns)} and {variables} do not match")

    concatenated_tables = pd.concat([table.data for table in tables])
    variables.remove("n")
    return ContingencyTable(
            concatenated_tables
            .groupby(list(variables))
            .sum()
            .reset_index()
            )


