"""Recompute the paper's headline active-volume metrics with whatever psiqdk is installed.

Usage: python collect.py <path-to-psiq-fermi-hubbard-checkout> <out.json>
"""
import json
import sys
import time
from importlib import metadata

repo = sys.argv[1]
sys.path.insert(0, f"{repo}/tests/paper_fidelity")

from psiq_fh.wb_program import FermiHubbardQreRunner  # noqa: E402
from psiq_fh.wb_program.utils import extract_all  # noqa: E402

LATTICE_SIZES = list(range(4, 21, 2))
METRICS = ["total_av", "aggregated_clifford_av", "aggregated_non_clifford_av", "black_box_av"]

out = {
    "versions": {p: metadata.version(p) for p in ["psiqdk", "psiqdk-workbench", "psiqdk-algorithms"]},
    "lattice_sizes": LATTICE_SIZES,
    "variants": {},
}
for variant in ["baseline", "improved"]:
    t0 = time.time()
    runner = FermiHubbardQreRunner(lattice_sizes=LATTICE_SIZES, variant=variant, num_batches=1)
    data = runner.retrieve(save_callgraphs=False)
    out["variants"][variant] = {m: [float(v) for v in extract_all(data, m)] for m in METRICS}
    out["variants"][variant]["seconds"] = time.time() - t0
    print(variant, "done", round(time.time() - t0), "s", flush=True)
json.dump(out, open(sys.argv[2], "w"), indent=1)
