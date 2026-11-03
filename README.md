# Do the Fermi-Hubbard active-volume numbers survive a psiqdk upgrade?

[psiq-fermi-hubbard](https://github.com/psiq/psiq-fermi-hubbard) is the code for "Compiling the 2D Fermi-Hubbard ground-state energy estimation algorithm for active volume quantum architectures" ([arXiv:2609.05316](https://arxiv.org/abs/2609.05316)). Its README says the numbers are only guaranteed with the pinned environment (`uv sync --frozen`, psiqdk 2.4.0) because psiqdk is under active development. psiqdk 2.5.0 is now on PyPI, so I checked whether the paper's headline numbers still come out the same.

## What I ran

All on a fresh clone of psiq-fermi-hubbard at commit `a41b085`, Python 3.13, Apple Silicon CPU.

1. Pinned environment (`uv sync --frozen --group jupyter`): full test suite, `uv run pytest`, including the `paper_fidelity` tests.
2. A second environment with `psiqdk==2.5.0` (pulls psiqdk-workbench 4.55.3 and psiqdk-algorithms 1.24.4): the `paper_fidelity` tests.
3. In both environments, `collect.py` recomputes the four headline metrics the fidelity tests pin (total, Clifford, non-Clifford and black-box active volume) for both circuit variants and lattice sizes 4 to 20, and `compare.py` diffs them against the values in `tests/paper_fidelity/test_paper_metrics.py`.
4. An environment with `psiqdk==2.3.0`, to see whether the pin is doing real work.

## Results

| environment | psiqdk / workbench / algorithms | result |
|---|---|---|
| pinned (uv.lock) | 2.4.0 / 4.55.0 / 1.24.3 | full suite: 626 passed in 8m50s. All 72 headline values (2 variants x 4 metrics x 9 lattice sizes) match the paper exactly |
| latest | 2.5.0 / 4.55.3 / 1.24.4 | paper_fidelity: 26 passed in 4m06s, including the per-lattice active-volume breakdowns. All 72 headline values match exactly |
| older | 2.3.0 / 4.52.5 / 1.24.3 | does not run: `ImportError: cannot import name 'RotationViaMixedFallback'` from `psiqdk.workbench.rotations._rotation` |

So as of psiqdk 2.5.0 the published numbers reproduce bit for bit outside the frozen lockfile, and the `>=2.4.0` floor in `pyproject.toml` is a real API requirement, not just a pin for reproducibility. Each variant takes about two minutes to recompute on a laptop CPU.

`pinned_2.4.0.json` and `latest_2.5.0.json` are the raw outputs.

## Run it

    git clone https://github.com/psiq/psiq-fermi-hubbard
    cd psiq-fermi-hubbard && uv sync --frozen && cd ..
    psiq-fermi-hubbard/.venv/bin/python collect.py psiq-fermi-hubbard my_run.json
    psiq-fermi-hubbard/.venv/bin/python compare.py psiq-fermi-hubbard my_run.json

To test another psiqdk version, make a separate venv, `pip install -e psiq-fermi-hubbard "psiqdk==X.Y.Z"`, and run the same two commands with that interpreter. `python -m pytest test_compare.py` checks the comparison helper and the recorded files.

## Limits

This only checks the metrics the repo's own fidelity tests pin. It does not check the error budgeting or logical-cycle scheduling, which the paper's README notes are not open-sourced.
