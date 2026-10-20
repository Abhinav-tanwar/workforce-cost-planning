# Workforce Cost Planning

Integer weekly coverage and continuous overtime/material-cost scenarios.

**Author and maintainer:** Abhinav Tanwar.

## Run

Requires Python 3.12. Install dependencies with `python -m pip install -r requirements.txt`.

```sh
python analysis.py
python -m unittest discover -s tests
```

## Methods and limitations

Combines the source five-on/two-off integer coverage problem with the process/overtime cost scenario. Daily coverage is verified from the returned integer schedule. The process models retain raw-material and production constraints; overtime is bounded to 200 hours. Fixed base labor cost is omitted consistently from both scenario objectives. Solver status and feasibility are checked before reporting a plan. These are illustrative demands, not a live staffing deployment.

## Measured results


[Full calculated metrics](results/metrics.json) · [Input provenance](data/README.md) · [Method changes](docs/methodology.md). Open `report.html` for the visual summary.

Generated examples and toy inputs are explicitly illustrative; they do not stand in for historical real-world outcomes.

The clean notebook in `notebooks/` delegates to the same module. Notebook cells were syntax-checked with outputs cleared; native scripts and tests were executed.
