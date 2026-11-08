"""Figures + tables for the report. Usage: python -m whoiswho.plots"""
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from .analyze import COND_LABEL, COND_ORDER

OUT = Path("results")
FIG = OUT / "figures"
FEATS = ["Char n-grams", "Style profile", "Semantic embedding", "Combined"]
# Reference categorical palette (light), slots 1-4, fixed order.
COLORS = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100"]
INK, MUTED, GRID = "#0b0b0b", "#52514e", "#e4e3df"

plt.rcParams.update({
    "font.size": 9, "axes.edgecolor": MUTED, "axes.labelcolor": INK, "xtick.color": MUTED,
    "ytick.color": MUTED, "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6, "axes.axisbelow": True,
    "legend.frameon": False, "figure.dpi": 200, "savefig.bbox": "tight",
})


def agg(metrics, key, feat, cond):
    vals = [v["features"][feat][key] for k, v in metrics.items() if k.rsplit("_s", 1)[0] == cond]
    return np.mean(vals), np.std(vals), vals


def grouped(metrics, key, ylabel, title, fname, ylim=(0.4, 1.0), chance=0.5):
    fig, ax = plt.subplots(figsize=(6.4, 2.8))
    w = 0.19
    x = np.arange(len(COND_ORDER))
    for i, f in enumerate(FEATS):
        m = [agg(metrics, key, f, c)[0] for c in COND_ORDER]
        s = [agg(metrics, key, f, c)[1] for c in COND_ORDER]
        ax.bar(x + (i - 1.5) * w, m, w * 0.9, yerr=s, color=COLORS[i], label=f,
               error_kw=dict(ecolor=MUTED, lw=0.8, capsize=2))
    if chance is not None:
        ax.axhline(chance, color=MUTED, lw=0.8, ls="--")
        ax.text(len(COND_ORDER) - 0.5, chance + 0.01, "chance", color=MUTED, ha="right", va="bottom", fontsize=7)
    ax.set_xticks(x, [COND_LABEL[c] for c in COND_ORDER])
    ax.set_ylim(*ylim)
    ax.set_ylabel(ylabel)
    ax.set_title(title, loc="left", fontsize=10, color=INK)
    ax.legend(ncol=4, loc="upper center", bbox_to_anchor=(0.5, -0.22), fontsize=8)
    fig.savefig(FIG / fname)
    plt.close(fig)


def confound(metrics, fname, feat="Combined"):
    fig, ax = plt.subplots(figsize=(6.4, 2.6))
    keys = [("auc_agent", "Same agent"), ("auc_operator", "Same operator\n(diff. agent)"),
            ("auc_model_confound", "Same base model\n(diff. operator)")]
    w = 0.25
    x = np.arange(len(COND_ORDER))
    for i, (k, lab) in enumerate(keys):
        m = [agg(metrics, k, feat, c)[0] for c in COND_ORDER]
        s = [agg(metrics, k, feat, c)[1] for c in COND_ORDER]
        ax.bar(x + (i - 1) * w, m, w * 0.9, yerr=s, color=COLORS[i], label=lab,
               error_kw=dict(ecolor=MUTED, lw=0.8, capsize=2))
    ax.axhline(0.5, color=MUTED, lw=0.8, ls="--")
    ax.set_xticks(x, [COND_LABEL[c] for c in COND_ORDER])
    ax.set_ylim(0.4, 1.0)
    ax.set_ylabel("Pairwise ROC-AUC")
    ax.set_title(f"What does the '{feat}' fingerprint actually track?", loc="left", fontsize=10, color=INK)
    ax.legend(ncol=3, loc="upper center", bbox_to_anchor=(0.5, -0.22), fontsize=8)
    fig.savefig(FIG / fname)
    plt.close(fig)


def heatmaps(metrics, fname, feat="Semantic embedding", seed=0):
    fig, axes = plt.subplots(1, 4, figsize=(7.2, 2.1))
    for ax, c in zip(axes, COND_ORDER):
        C = np.array(metrics[f"{c}_s{seed}"]["features"][feat]["operator_centroids"])
        off = C.copy()
        np.fill_diagonal(off, np.nan)
        im = ax.imshow(off, cmap="Blues")
        ax.set_title(COND_LABEL[c].replace("\n", " "), fontsize=7.5, color=INK)
        ax.set_xticks(range(8), [str(i) for i in range(8)], fontsize=6)
        ax.set_yticks(range(8), [str(i) for i in range(8)], fontsize=6)
        ax.grid(False)
        ax.add_patch(plt.Rectangle((5.5, 6.5), 1, 1, fill=False, ec="#e34948", lw=1.4))
        ax.add_patch(plt.Rectangle((6.5, 5.5), 1, 1, fill=False, ec="#e34948", lw=1.4))
    fig.suptitle(f"Operator-to-operator similarity ({feat}); red box = the two covert fronts (6, 7)",
                 fontsize=8.5, x=0.02, ha="left", color=INK)
    fig.savefig(FIG / fname)
    plt.close(fig)


def tables(metrics, stats):
    lines = ["## Pairwise ROC-AUC (mean ± sd over seeds)\n"]
    for key, lab in [("auc_agent", "Re-identify renamed agent"),
                     ("auc_agent_within_op", "Re-identify agent, within one operator account"),
                     ("auc_operator", "Same operator (different agents)"),
                     ("auc_model_confound", "Same base model (different operators) — confound"),
                     ("ari_operator", "ARI: clustering into operators"),
                     ("ari_model", "ARI: clustering into base models"),
                     ("front_pair_rank", "Rank of covert front pair (1 = most similar of 28)")]:
        lines.append(f"\n### {lab}\n\n| Feature | " + " | ".join(COND_LABEL[c].replace(chr(10), ' ') for c in COND_ORDER) + " |")
        lines.append("|---" * (len(COND_ORDER) + 1) + "|")
        for f in FEATS:
            cells = []
            for c in COND_ORDER:
                m, s, vals = agg(metrics, key, f, c)
                cells.append(", ".join(str(int(v)) for v in vals) if key == "front_pair_rank" else f"{m:.2f} ± {s:.2f}")
            lines.append(f"| {f} | " + " | ".join(cells) + " |")
    lines.append("\n## Identity schemes: pairwise 'same principal' P / R / F1 (mean over seeds)\n")
    schemes = list(next(iter(metrics.values()))["schemes"])
    lines.append("| Scheme | " + " | ".join(COND_LABEL[c].replace(chr(10), ' ') for c in COND_ORDER) + " |")
    lines.append("|---" * (len(COND_ORDER) + 1) + "|")
    for sc in schemes:
        cells = []
        for c in COND_ORDER:
            rs = [v["schemes"][sc] for k, v in metrics.items() if k.rsplit("_s", 1)[0] == c]
            cells.append("/".join(f"{np.mean([r[x] for r in rs]):.2f}" for x in ("precision", "recall", "f1")))
        lines.append(f"| {sc} | " + " | ".join(cells) + " |")
    lines.append("\n## Run stats\n\n| Run | posts | aliases | empty | refusals | covert posts mentioning package | honest posts mentioning package |\n|---|---|---|---|---|---|---|")
    for k, s in stats.items():
        lines.append(f"| {k} | {s['posts']} | {metrics[k]['n_aliases']} | {s['empty']} | {s['refusals']} | "
                     f"{s['covert_mentions']}/{s['covert_posts']} | {s['honest_mentions']} |")
    lines.append("\n## Fingerprint merges proposed (operator pairs with z > 2)\n")
    for k, v in metrics.items():
        lines.append(f"- {k}: {v['merged_pairs']}")
    (OUT / "tables.md").write_text("\n".join(lines) + "\n")


def main():
    FIG.mkdir(parents=True, exist_ok=True)
    metrics = json.loads((OUT / "metrics.json").read_text())
    stats = json.loads((OUT / "run_stats.json").read_text())
    grouped(metrics, "auc_agent", "Pairwise ROC-AUC", "Re-identifying an agent after it renames itself",
            "fig1_reid_auc.png")
    grouped(metrics, "auc_operator", "Pairwise ROC-AUC", "Linking different agents to the same operator",
            "fig2_operator_auc.png")
    confound(metrics, "fig3_confound.png")
    heatmaps(metrics, "fig4_fronts.png")
    tables(metrics, stats)
    print((OUT / "tables.md").read_text())


if __name__ == "__main__":
    main()
