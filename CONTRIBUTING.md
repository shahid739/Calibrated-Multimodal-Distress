# Contributing to DERS-X

Thank you for helping improve DERS-X. This repository is maintained primarily as a reproducibility artifact for the associated research manuscript, so changes should preserve a clear distinction between the paper-aligned reference analysis and later extensions.

## Before opening a change

1. Fork the repository and create a branch from `main`.
2. Keep changes focused and describe their scientific or reproducibility purpose.
3. Do not replace archived manuscript result values with results from a new run unless the manuscript/result registry is being deliberately updated as part of the same reviewed change.
4. Do not commit raw third-party corpus files or other data that you are not licensed to redistribute.

## Reproducibility checks

For changes to documentation or archived result tooling, run from the repository root:

```bash
python scripts-show_results.py --method csv --results_dir .
python scripts-verify_results.py --results_dir .
python scripts-repository_audit.py --repo .
```

For changes to `DERS-X-B.ipynb`, also verify that:

- the primary IEMOCAP grouping matches the protocol described by the manuscript and archived fold table;
- training, validation, calibration, and test groups remain disjoint according to the documented grouping rules;
- target statistics are fitted from training data only;
- calibration is fitted without test-set information; and
- generated run metadata record the environment, split identifiers, configuration, and random seed.

## Code and notebook style

- Follow PEP 8 for standalone Python scripts where practical.
- Use clear function/docstring names and explicit random-seed handling.
- Keep notebook cells ordered so a fresh user can execute them sequentially after setting dataset paths.
- Prefer machine-readable outputs (CSV, YAML, JSON) for reported results.

## Documentation changes

When changing a protocol, preprocessing rule, dependency, or reported value, update all affected sources together, especially:

- `README.md`
- `docs-reproducibility.md`
- `docs-experimental_setup.md`
- `Methodology.txt`
- `paper_results.yaml` 

## Pull requests

A pull request should explain what changed, why it changed, how it was checked, and whether it changes any manuscript-aligned result or protocol. 
