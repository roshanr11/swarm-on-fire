"""Threshold sweep for model-corrected fingerprint merging vs. gateway attestation alone.
Reads results/metrics.json; writes results/figures/fig11_merge_sweep.png and results/merge_sweep.json.
Usage: python -m whoiswho.merge_sweep"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

M = json.loads(Path("results/metrics.json").read_text())
CONDS = [("twins", "8 ops · twins"), ("large", "32 ops · obvious"), ("large_subtle", "32 ops · subtle"),
         ("large_memory", "32 ops · memory"), ("large_persona", "32 ops · persona")]
rng = np.random.default_rng(0)


def ci(x):
    b = [rng.choice(x, len(x)).mean() for _ in range(5000)]
    return [float(v) for v in np.percentile(b, [2.5, 97.5])]


out = {}
fig, ax = plt.subplots(figsize=(7.5, 3.6))
for i, (c, lab) in enumerate(CONDS):
    ks = [k for k in M if k.rsplit("_s", 1)[0] == c]
    ts = sorted(M[ks[0]]["merge_sweep"], key=float)
    att = np.array([M[k]["schemes"]["Gateway operator attestation"]["f1"] for k in ks])
    delta = np.array([[M[k]["merge_sweep"][t]["f1"] for t in ts] for k in ks]) - att[:, None]
    pre = np.array([M[k]["schemes"]["Gateway + model-corrected merge"]["f1"] for k in ks]) - att
    x = [float(t) for t in ts]
    ax.plot(x, delta.mean(0), marker="o", ms=3, label=f"{lab} (n={len(ks)})", color=plt.cm.tab10(i))
    zt = float(np.mean([M[k]["z_threshold"] for k in ks]))
    ax.plot([zt], [pre.mean()], marker="*", ms=12, color=plt.cm.tab10(i), mec="k")
    best = int(np.argmax(delta.mean(0)))
    out[c] = dict(runs=len(ks), preset_z=zt, preset_delta=float(pre.mean()), preset_ci=ci(pre),
                  best_z=x[best], best_delta=float(delta.mean(0)[best]), best_ci=ci(delta[:, best]))
ax.axhline(0, color="k", lw=0.8, ls="--")
ax.set_ylim(-0.4, 0.15)
ax.set_xlabel("Merge threshold (z-score of operator-pair similarity)")
ax.set_ylabel("F1 gain over attestation alone")
ax.legend(fontsize=7, loc="lower right", frameon=False)
ax.set_title("F1 gain from fingerprint merging depends on the threshold (stars: preset threshold)", fontsize=9)
fig.tight_layout()
fig.savefig("results/figures/fig11_merge_sweep.png", dpi=200)
Path("results/merge_sweep.json").write_text(json.dumps(out, indent=1))
for c, r in out.items():
    print(c, {k: (round(v, 3) if isinstance(v, float) else [round(u, 3) for u in v] if isinstance(v, list) else v) for k, v in r.items()})
