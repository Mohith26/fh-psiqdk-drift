"""Compare metrics collected by collect.py against the values pinned in the paper-fidelity tests.

Usage: python compare.py <path-to-psiq-fermi-hubbard-checkout> run1.json [run2.json ...]
"""
import json
import sys

METRIC_TO_CONSTANT = {
    "total_av": "TOTAL_AV",
    "aggregated_clifford_av": "TOTAL_CLIFF_AV",
    "aggregated_non_clifford_av": "TOTAL_NONCLIFF_AV",
    "black_box_av": "TOTAL_BB_AV",
}


def relative_drift(expected, actual):
    """Per-entry relative difference (actual - expected) / expected; 0 where expected is 0 and equal."""
    out = []
    for e, a in zip(expected, actual, strict=True):
        if e == 0:
            out.append(0.0 if a == 0 else float("inf"))
        else:
            out.append((a - e) / e)
    return out


def paper_values(repo):
    sys.path.insert(0, f"{repo}/tests/paper_fidelity")
    import test_paper_metrics as t  # the module that pins the paper's numbers

    return {
        variant: {m: [float(x) for x in getattr(t, const)[variant]] for m, const in METRIC_TO_CONSTANT.items()}
        for variant in ("baseline", "improved")
    }


def main(repo, runs):
    paper = paper_values(repo)
    for path in runs:
        run = json.load(open(path))
        v = run["versions"]
        print(f"{path}: psiqdk {v['psiqdk']}, workbench {v['psiqdk-workbench']}, algorithms {v['psiqdk-algorithms']}")
        for variant, metrics in paper.items():
            for metric, expected in metrics.items():
                drift = relative_drift(expected, run["variants"][variant][metric])
                worst = max(abs(d) for d in drift)
                status = "exact" if worst == 0 else f"max drift {worst:.3%}"
                print(f"  {variant:9s} {metric:28s} {len(expected)} lattice sizes: {status}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
