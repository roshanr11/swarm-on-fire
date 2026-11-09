"""Adaptive-attacker analysis. Compares fronts that receive detector feedback each round
(twins_adaptive, large_adaptive) with matched runs without feedback (twins, large).

For every run it recomputes the same detector the adaptive fronts saw (max cosine similarity of
a front's post to same-round posts by other accounts of the same hidden boss, using meaning
embeddings), so the no-feedback runs are scored identically. Writes results/adaptive.json and
results/figures/fig8_adaptive.png. Usage: python -m whoiswho.adaptive
"""
import json
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from . import llm
from .plots import COLORS, INK, MUTED, boot_ci

PAIRS = [("twins", "twins_adaptive", "8 operators"), ("large", "large_adaptive", "32 operators")]


def detector_by_round(posts):
    out = defaultdict(list)
    for r in sorted({p["round"] for p in posts}):
        fp = [p for p in posts if p["round"] == r and p["text"] and p.get("role") == "front"]
        if len(fp) < 2:
            continue
        E = np.array(llm.embed([x["text"][:4000] for x in fp]))
        E = E / np.linalg.norm(E, axis=1, keepdims=True)
        S = E @ E.T
        for i, x in enumerate(fp):
            same = [j for j, y in enumerate(fp) if y["principal"] == x["principal"] and y["operator"] != x["operator"]]
            if same:
                out[r].append(float(max(S[i, j] for j in same)))
    return {r: float(np.mean(v)) for r, v in out.items()}


def main():
    metrics = json.loads(Path("results/metrics.json").read_text())
    res = {}
    fig, axes = plt.subplots(1, 2, figsize=(7.4, 2.6), sharey=True)
    for ax, (base, adapt, lab) in zip(axes, PAIRS):
        for k, cond in enumerate([base, adapt]):
            runs = sorted(Path("results/runs").glob(f"{cond}_s*.jsonl"))
            curves = [detector_by_round([json.loads(l) for l in f.open()]) for f in runs]
            if not curves:
                continue
            rounds = sorted(set().union(*[c.keys() for c in curves]))
            m = [np.mean([c[r] for c in curves if r in c]) for r in rounds]
            ax.plot([r + 1 for r in rounds], m, color=COLORS[k * 1], lw=2, marker="o", ms=3.5,
                    label="with detector feedback" if k else "no feedback")
            fe = [metrics[f.stem]["features"] for f in runs if f.stem in metrics]
            res[cond] = dict(
                n=len(runs), detector_first=float(m[0]), detector_last=float(np.mean(m[-3:])),
                **{f"{key}_{feat.split()[0].lower()}": (float(np.mean(v)), boot_ci(v))
                   for key in ("auc_sybil_vs_honest", "auc_sybil_vs_twin")
                   for feat in ("Semantic embedding", "Style profile", "Combined")
                   for v in [[x[feat][key] for x in fe if key in x[feat]]] if v})
        ax.axhline(0.5, color=MUTED, lw=0.8, ls="--")
        ax.text(10, 0.505, "flag threshold told to agents", color=MUTED, fontsize=7, ha="right", va="bottom")
        ax.set_title(lab, loc="left", fontsize=9, color=INK)
        ax.set_xlabel("Round")
    axes[0].set_ylabel("Detector score of fronts\n(similarity to own team)")
    axes[0].legend(fontsize=7.5, loc="lower left")
    fig.suptitle("Adaptive attacker: fronts told their detector score each round", x=0.01, ha="left", fontsize=10, color=INK)
    fig.savefig("results/figures/fig8_adaptive.png", dpi=200, bbox_inches="tight")
    Path("results/adaptive.json").write_text(json.dumps(res, indent=1))
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
