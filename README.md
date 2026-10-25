# Agentic MLOps Starter

A small MLOps example that checks for drift in trade values, retrains a regression model from feedback, tracks runs and model versions in MLflow, and compares a new Challenger with the Production Champion.

## Requirements

- Python 3.11.8, as specified by `.python-version` and `pyproject.toml`
- uv 0.13 or a compatible release
- Network access to install the locked dependencies

## Install

From the repository root:

```sh
uv python install 3.11.8
uv sync --locked
```

`uv.lock` pins the resolved dependency graph. `uv lock --check` verifies that it is consistent with `pyproject.toml`.

## Run Locally

Run drift monitoring against the included 500-row baseline and inference datasets:

```sh
uv run python monitor.py
```

With the checked-in data, the expected result is PSI `11.4878`, KS `1.0`, and `drift_detected: True`.

Use a file-backed MLflow store for local training and model comparison:

```sh
export MLFLOW_TRACKING_URI="file://$PWD/mlruns"
uv run python retrain.py
```

Training reads the three CSV files in `data/feedback/` (600 rows total), uses a fixed 80/20 split, logs MSE and the model, then prints the registered Challenger version. To compare that version, pass the exact version printed by the training command:

```sh
uv run python compare_models.py 1
```

Replace `1` with the printed version. The script moves the Challenger to `Staging`. Lower MSE is better: it promotes an improving Challenger to `Production`, keeps an equal or worse Challenger in `Staging`, and leaves the prior Champion in `Production`. If no Production model exists, it promotes the first Challenger.

The current reference run reports MSE `23598.5534`, which does **not** meet the project target of MSE below `2000`. See the [technical dossier](dossier.md) for the model rationale, measured profile results, and limitations.

## GitHub Actions

`.github/workflows/main.yml` checks drift on a schedule or manual dispatch and gates retraining on drift. Configure the repository secret `MLFLOW_TRACKING_URI` to use a persistent MLflow tracking server with Model Registry enabled. Add `MLFLOW_TRACKING_USERNAME` and `MLFLOW_TRACKING_PASSWORD` only if the server requires basic authentication. A runner-local `mlruns` directory is not persistent between jobs.

## Profile Retraining

Capture and inspect a profile with:

```sh
uv run python -m cProfile -o retrain_after.prof retrain.py
uv run python -m pstats retrain_after.prof
uv run snakeviz retrain_after.prof
```

The checked-in `retrain.prof` is the before profile; `retrain_after.prof` is the profile after explicitly specifying MLflow model requirements. The [dossier](dossier.md) records the three-run timing method and results.

