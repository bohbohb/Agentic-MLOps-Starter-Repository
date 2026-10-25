# Security scan report
We used pip audit instead of safety (as it now requires account creation) and we obtained the following output:
Found 77 known vulnerabilities in 7 packages
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
urllib3 | 1.23 | PYSEC-2026-141 | 2.7.0
urllib3 | 1.23 | PYSEC-2026-1999 | 2.5.0
urllib3 | 1.23 | PYSEC-2026-1995 | 1.26.19,2.2.2
urllib3 | 1.23 | PYSEC-2026-1994 | 2.6.0
urllib3 | 1.23 | PYSEC-2026-1996 | 2.6.3
urllib3 | 1.23 | PYSEC-2026-4177 | 2.8.0


In particular we can notice that the several libraries require version bump which might have important consequences in terms of compatibility while others just require update patches. 
For example urlib3 and requests are simple minor updates and since the libraries are just used for sending http requests I would expect that the change could have a very low effort, as I don't expect no client code changes nor possible behavior changes and the possible problems that might arise from this change are limited in my opinion.
When it comes to mlflow experiment logging gunicorn and idna, the scan suggests a major bump which might involve changes in behaviors or removal of features that might be used in the code. On top of that mlflow is quite important in this kind of codebases as it might break some business or operational requirements (for example I log in a different way the dependency and this might break the productive model serving or the deploy pipeline), we need to invest on these updates and investigate and carefully read the update guidelines if present. Pyarrow requires a bump of 3 versions however since it is fundational library used mostly to read data of arrwo format I wouldn't expect a very complicated update process even if it is a major bump, given also the limited usage of the dependecy.

# Monitor

To run monitor.py you can simply run: 
uv run python monitor.py
output:
{'psi': 11.487804639671229, 'ks': 1.0, 'drift_detected': True, 'reason': 'psi value is over the threshold 0.2, ks value is over the threshold 0.1'}
