# 5s-TES notebooks
Example analyses aggregating outputs of Five Safes TES analytics tools.
Each directory contains an example of a federated analysis, with example data and reusable utilities.

## Dependencies
Notebooks have different dependencies.
The project is managed using [uv](https://docs.astral.sh/uv/); follow their instructions to install uv.
With uv installed, to run a notebook, navigate to the correct directory and run:

```bash
uv run jupyter notebook
```

## Notebooks
- [**OMOP metadata**](/OMOP-metadata) visualising OMOP metadata
- [**Descriptive statistics**](/descriptive-stats) calculating basic statistics on continuous variables
- [**Contingency tables**](/contingency-tables) building contingency tables from federated data
