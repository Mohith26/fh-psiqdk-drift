import json
import math
from pathlib import Path

from compare import relative_drift

HERE = Path(__file__).parent


def test_relative_drift_basic():
    assert relative_drift([100.0, 50.0], [101.0, 50.0]) == [0.01, 0.0]


def test_relative_drift_zero_expected():
    d = relative_drift([0.0, 0.0], [0.0, 3.0])
    assert d[0] == 0.0 and math.isinf(d[1])


def test_recorded_runs_have_all_metrics():
    for name in ["pinned_2.4.0.json", "latest_2.5.0.json"]:
        run = json.loads((HERE / name).read_text())
        for variant in ["baseline", "improved"]:
            for metric in ["total_av", "aggregated_clifford_av", "aggregated_non_clifford_av", "black_box_av"]:
                assert len(run["variants"][variant][metric]) == len(run["lattice_sizes"]) == 9
