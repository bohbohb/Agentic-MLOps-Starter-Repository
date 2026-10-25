# Technical Dossier

## Repository url
[repository fork]{https://github.com/bohbohb/Agentic-MLOps-Starter-Repository}

## Technical Write-Up

### System and design choices

The repository demonstrates a feedback-driven MLOps path: `monitor.py` compares baseline and inference trade-value distributions, `retrain.py` fits and registers a model from feedback CSVs, and `compare_models.py` decides whether a registered Challenger should replace the Production Champion.

The monitor reports both Population Stability Index (PSI) and the two-sample Kolmogorov-Smirnov (KS) statistic. PSI summarizes distribution changes across quantile buckets, while KS compares the empirical distributions directly. Drift is flagged when PSI exceeds `0.2` or KS exceeds `0.1`; these thresholds are configurable function arguments in `monitor.py`.

Training uses the three categorical fields `agent_id`, `tool_name`, and `status`. A `ColumnTransformer` applies one-hot encoding. The transformed features feed a `LinearRegression` model. The fixed 80/20 split and `random_state=42` are crucial to make the experiments repeatable. MSE is the comparison metric because `trade_value` is continuous, another metric such as AUC is not appropriate here as it is classification metric. Lower MSE indicates better predictions.

MLflow logs the metric and serialized sklearn pipeline, and registers versions under `investment-agent`. `compare_models.py` moves the new version to `Staging`; it promotes it to `Production` only when its MSE is strictly lower than the current Champion's. An equal or worse Challenger remains in Staging, while the existing Champion is keept as Production. On an empty registry, the first Challenger becomes Production.

### Reproduced behavior and model quality

Running `uv run python monitor.py` against the checked-in 500-row baseline and 500-row inference files produced:

```text
{'psi': 11.487804639671229, 'ks': 1.0, 'drift_detected': True, 'reason': 'psi value is over the threshold 0.2, ks value is over the threshold 0.1'}
```

The feedback files contain 600 rows in total. The recorded MLflow runs both report MSE `23598.55339906003`. This is above the supplied acceptance target of MSE `< 2000`, so the current model-quality requirement is not met. The measured target standard deviation is about `143.19`; the reported MSE corresponds to an RMSE of about `153.62`. The profiling optimization below changes only how MLflow records model dependencies, not the features, split, or estimator, and the observed MSE remained unchanged. Improving model quality requires separate feature/data investigation and must be demonstrated with a new holdout result rather than assumed from the runtime change.

The run details and metric are visible in the supplied [Challenger run screenshot](screenshots/Screenshot%202026-10-25%20at%2012.08.50.png) and [Champion run screenshot](screenshots/Screenshot%202026-10-25%20at%2012.09.08.png). The MLflow experiment view shows run durations of 2.6 and 2.7 seconds in the earlier captured run set: [experiment screenshot](screenshots/Screenshot%202026-10-25%20at%2012.05.59.png).

## Profiling Report

### Method

The baseline and optimized measurements were captured on the same local macOS ARM environment with CPython 3.11.8, MLflow 2.9.2, and the same 600-row feedback data. Each timing is a fresh Python process using a temporary file-backed MLflow registry. Three wall-clock runs were measured with `time.perf_counter`; the mean is reported below. The profile artifacts were captured separately with `cProfile`, whose instrumentation adds overhead, so profile totals should not be confused with the unprofiled wall-clock means.

### Results

| Measurement | Before | After | Change |
| --- | ---: | ---: | ---: |
| Wall-clock run 1 | 5.323 s | 2.416 s | |
| Wall-clock run 2 | 5.034 s | 2.367 s | |
| Wall-clock run 3 | 5.369 s | 2.433 s | |
| Mean wall-clock runtime | 5.242 s | 2.406 s | 54.1% faster |
| cProfile total runtime | 5.531 s | 2.576 s | 53.4% lower |
| `mlflow.sklearn.log_model` cumulative time | 2.714 s | 0.056 s | 97.9% lower |
| MLflow requirement inference | 2.633 s | Not present | Removed |
| Function calls (including profiler/import activity) | 2,835,876 | 1,613,634 | 43.1% fewer |

Before, `retrain.prof` showed `mlflow.sklearn.log_model` consuming 2.714 seconds, of which `_infer_requirements` consumed 2.633 seconds. MLflow was importing and inspecting the environment to infer model dependencies. The fix in `retrain.py` supplies the versions of MLflow, NumPy, pandas, scikit-learn, and SciPy explicitly via `pip_requirements`. This preserves a reproducible model environment and avoids that inference subprocess. The post-change profile, `retrain_after.prof`, shows model logging at 0.056 seconds and no `_infer_requirements` call.

The wall-clock means improve by 54.1%, exceeding the guide's 20% target. The checked-in profiles provide the raw call data: [before profile](retrain.prof) and [after profile](retrain_after.prof).

## Dependency Security Scan

The point-in-time `pip-audit` output recorded for this environment reports 77 advisories across seven packages. The detailed advisory IDs and scanner-provided fix versions are retained below. These are version-level findings; they do not by themselves establish that every vulnerable code path is reachable in this application.

Name | Version | ID | Fix Versions
--- | --- | --- | ---
gunicorn | 21.2.0 | PYSEC-2026-1434 | 22.0.0
gunicorn | 21.2.0 | PYSEC-2026-1433 | 22.0.0
idna | 2.7 | PYSEC-2024-60 | 3.7
idna | 2.7 | PYSEC-2026-215 | 3.15
mlflow | 2.9.2 | PYSEC-2025-17 | 2.19.0
mlflow | 2.9.2 | PYSEC-2024-241 | 2.10.0
mlflow | 2.9.2 | PYSEC-2024-240 | 2.10.0
mlflow | 2.9.2 | PYSEC-2024-242 | 2.11.3
mlflow | 2.9.2 | PYSEC-2024-243 | 2.10.0
mlflow | 2.9.2 | PYSEC-2024-244 | 2.12.1
mlflow | 2.9.2 | PYSEC-2024-224 | 2.16.0
mlflow | 2.9.2 | PYSEC-2025-52 | 3.1.0
mlflow | 2.9.2 | PYSEC-2024-51 | 2.10.1
mlflow | 2.9.2 | PYSEC-2026-94 | 3.11.0rc0
mlflow | 2.9.2 | PYSEC-2026-93 | 3.11.0rc0
mlflow | 2.9.2 | PYSEC-2026-195 | 3.10.1
mlflow | 2.9.2 | PYSEC-2026-424 | 3.9.0
mlflow | 2.9.2 | PYSEC-2026-419 | 
mlflow | 2.9.2 | PYSEC-2026-421 | 3.8.0rc0
mlflow | 2.9.2 | PYSEC-2026-425 | 3.9.0rc0
mlflow | 2.9.2 | PYSEC-2026-423 | 3.8.1
mlflow | 2.9.2 | PYSEC-2026-1644 | 
mlflow | 2.9.2 | PYSEC-2026-1645 | 2.11.3
mlflow | 2.9.2 | PYSEC-2026-1643 | 
mlflow | 2.9.2 | PYSEC-2026-1642 | 2.22.0rc0
mlflow | 2.9.2 | PYSEC-2026-1641 | 
mlflow | 2.9.2 | PYSEC-2026-1647 | 
mlflow | 2.9.2 | PYSEC-2026-1650 | 2.12.1
mlflow | 2.9.2 | PYSEC-2026-1663 | 
mlflow | 2.9.2 | PYSEC-2026-1651 | 
mlflow | 2.9.2 | PYSEC-2026-1653 | 2.12.1
mlflow | 2.9.2 | PYSEC-2026-1648 | 
mlflow | 2.9.2 | PYSEC-2026-1649 | 
mlflow | 2.9.2 | PYSEC-2026-1638 | 2.17.0rc0
mlflow | 2.9.2 | PYSEC-2026-1654 | 
mlflow | 2.9.2 | PYSEC-2026-1655 | 
mlflow | 2.9.2 | PYSEC-2026-1640 | 2.22.4,3.0.0
mlflow | 2.9.2 | PYSEC-2026-1639 | 3.4.0rc0
mlflow | 2.9.2 | PYSEC-2026-1636 | 
mlflow | 2.9.2 | PYSEC-2026-1657 | 
mlflow | 2.9.2 | PYSEC-2026-1656 | 3.5.0
mlflow | 2.9.2 | PYSEC-2026-1658 | 
mlflow | 2.9.2 | PYSEC-2026-1637 | 
mlflow | 2.9.2 | PYSEC-2026-1660 | 
mlflow | 2.9.2 | PYSEC-2026-2219 | 3.9.0
mlflow | 2.9.2 | PYSEC-2026-2220 | 3.11.0rc0
mlflow | 2.9.2 | PYSEC-2026-2221 | 3.10.0
mlflow | 2.9.2 | PYSEC-2026-2222 | 3.11.0
mlflow | 2.9.2 | PYSEC-2026-2654 | 3.10.0
mlflow | 2.9.2 | PYSEC-2026-2655 | 3.11.0
mlflow | 2.9.2 | PYSEC-2026-2656 | 3.9.0rc0
mlflow | 2.9.2 | PYSEC-2026-2657 | 
mlflow | 2.9.2 | PYSEC-2026-2660 | 3.10.0
mlflow | 2.9.2 | PYSEC-2026-2659 | 3.11.0rc0
mlflow | 2.9.2 | PYSEC-2026-2661 | 3.8.0rc0
mlflow | 2.9.2 | PYSEC-2026-2658 | 3.8.0rc0
mlflow | 2.9.2 | PYSEC-2026-3687 | 3.15.0
mlflow | 2.9.2 | GHSA-gqvg-gmmx-x4hm | 3.15.0
protobuf | 4.25.9 | PYSEC-2026-1805 | 5.29.6,6.33.5
pyarrow | 14.0.2 | PYSEC-2024-161 | 17.0.0
requests | 2.19.0 | PYSEC-2018-28 | 2.20.0
requests | 2.19.0 | PYSEC-2023-74 | 2.31.0
requests | 2.19.0 | PYSEC-2026-1873 | 2.32.0
requests | 2.19.0 | PYSEC-2026-1872 | 2.32.4
requests | 2.19.0 | PYSEC-2026-2275 | 2.33.0
urllib3 | 1.23 | PYSEC-2019-133 | 1.24.2
urllib3 | 1.23 | PYSEC-2019-132 | 1.24.3
urllib3 | 1.23 | PYSEC-2020-148 | 1.25.9
urllib3 | 1.23 | PYSEC-2023-192 | 1.26.17,2.0.6
urllib3 | 1.23 | PYSEC-2023-207 | 1.24.2
urllib3 | 1.23 | PYSEC-2023-212 | 1.26.18,2.0.7
urllib3 | 1.23 | PYSEC-2026-4177 | 2.8.0

### Assessment and next steps

The most consequential upgrade is MLflow: the scan lists fixes across both later 2.x releases and 3.x, so upgrading could be very demanding as it may affect model logging, registry behavior, or serving. Gunicorn, PyArrow, and protobuf also require compatibility testing as they involve minor updates. Requests, urllib3, and idna are old transitive HTTP dependencies; I cannot assume their upgrades are behavior-free just because their role is narrow, however we can estimate the risk and the effort of the upgrade lower compared to the ones mentioned above.
To upgrade the dependencies it is important to review each advisory and the relevant release notes, update compatible constraints in `pyproject.toml`, regenerate `uv.lock`, run the monitor/retraining/registry checks, and rerun `pip-audit`. Once this is is done a new scan should be made to check new advisory data before a release.

