"""Figures + tables for the report. Usage: python -m whoiswho.plots"""
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from .analyze import COND_LABEL, COND_ORDER, EXTRA_ORDER

OUT = Path("results")
FIG = OUT / "figures"
FEATS = ["Char n-grams", "Style profile", "Semantic embedding", "Combined"]
ALL_FEATS = ["Keyword (word TF-IDF)"] + FEATS
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


def present(metrics, order):
    have = {k.rsplit("_s", 1)[0] for k in metrics}
    return [c for c in order if c in have]


def robustness(metrics, fname="fig6_robustness.png", feat="Combined"):
    conds = present(metrics, EXTRA_ORDER)
    keys = [("auc_operator", "Same operator (diff. agent)"), ("auc_agent_within_op", "Same agent, within operator"),
            ("auc_agent_within_op_late", "Same agent, within operator (rounds 6-10)")]
    fig, ax = plt.subplots(figsize=(7.2, 2.8))
    w = 0.25
    x = np.arange(len(conds))
    for i, (k, lab) in enumerate(keys):
        m = [agg(metrics, k, feat, c)[0] for c in conds]
        sd = [agg(metrics, k, feat, c)[1] for c in conds]
        ax.bar(x + (i - 1) * w, m, w * 0.9, yerr=sd, color=COLORS[i], label=lab,
               error_kw=dict(ecolor=MUTED, lw=0.8, capsize=2))
    ax.axhline(0.5, color=MUTED, lw=0.8, ls="--")
    ax.set_xticks(x, [COND_LABEL[c] for c in conds], fontsize=7.5)
    ax.set_ylim(0.3, 1.0)
    ax.set_ylabel("Pairwise ROC-AUC")
    ax.set_title("Robustness checks (combined fingerprint)", loc="left", fontsize=10, color=INK)
    ax.legend(ncol=3, loc="upper center", bbox_to_anchor=(0.5, -0.25), fontsize=7.5)
    fig.savefig(FIG / fname)
    plt.close(fig)


def tables(metrics, stats):
    conds_all = present(metrics, COND_ORDER + [c for c in EXTRA_ORDER if c not in COND_ORDER])
    lines = ["## Metrics: mean over seeds [95% bootstrap CI over seeds]\n"]
    for key, lab in [("auc_agent", "Re-identify renamed agent"),
                     ("auc_agent_within_op", "Re-identify agent, within one operator account"),
                     ("auc_agent_within_op_early", "Within operator, both aliases in rounds 1-5"),
                     ("auc_agent_within_op_late", "Within operator, both aliases in rounds 6-10"),
                     ("auc_operator", "Same operator (different agents)"),
                     ("auc_model_confound", "Same base model (different operators) — confound"),
                     ("ari_operator", "ARI: clustering into operators"),
                     ("ari_model", "ARI: clustering into base models"),
                     ("front_pair_rank", "Rank of covert front pair (1 = most similar of 28)"),
                     ("auc_sybil_vs_honest", "Operator pairs: same covert principal vs ordinary honest pairs (AUC)"),
                     ("auc_sybil_vs_twin", "Operator pairs: same covert principal vs honest twins (AUC)")]:
        lines.append(f"\n### {lab}\n\n| Feature | " + " | ".join(COND_LABEL[c].replace(chr(10), ' ') for c in conds_all) + " |")
        lines.append("|---" * (len(conds_all) + 1) + "|")
        for f in ALL_FEATS:
            cells = []
            for c in conds_all:
                m, s, vals = agg_key(metrics, key, f, c)
                if not vals:
                    cells.append("—")
                else:
                    if key == "front_pair_rank":
                        cells.append(", ".join(str(int(v)) for v in vals))
                    else:
                        lo, hi = boot_ci(vals)
                        cells.append(f"{m:.2f} [{lo:.2f}, {hi:.2f}]" if len(vals) > 1 else f"{m:.2f}")
            lines.append(f"| {f} | " + " | ".join(cells) + " |")
    lines.append("\n## Identity schemes: pairwise 'same principal' P / R / F1 (mean over seeds)\n")
    schemes = list(next(iter(metrics.values()))["schemes"])
    lines.append("| Scheme | " + " | ".join(COND_LABEL[c].replace(chr(10), ' ') for c in conds_all) + " |")
    lines.append("|---" * (len(conds_all) + 1) + "|")
    for sc in schemes:
        cells = []
        for c in conds_all:
            rs = [v["schemes"][sc] for k, v in metrics.items() if k.rsplit("_s", 1)[0] == c]
            cells.append("/".join(f"{np.mean([r[x] for r in rs]):.2f}" for x in ("precision", "recall", "f1")))
        lines.append(f"| {sc} | " + " | ".join(cells) + " |")
    lines.append("\n## Run stats\n\n| Run | posts | aliases | empty | refusals | covert posts mentioning package | honest posts mentioning package |\n|---|---|---|---|---|---|---|")
    for k, s in stats.items():
        lines.append(f"| {k} | {s['posts']} | {metrics[k]['n_aliases']} | {s['empty']} | {s['refusals']} | "
                     f"{s['covert_mentions']}/{s['covert_posts']} | {s['honest_mentions']} |")
    lines.append("\n## Fingerprint merges (z above 1-1/#pairs quantile; model-corrected)\n")
    lines.append("| Run | fronts | twins | edges | true (same principal) | twin edges | sybil pairs |\n|---|---|---|---|---|---|---|")
    for k, v in metrics.items():
        e = v.get("merge_edges_corrected", {})
        lines.append(f"| {k} | {v.get('fronts')} | {v.get('twins')} | {e.get('edges')} | {e.get('true_edges')} | "
                     f"{e.get('twin_edges')} | {e.get('sybil_pairs')} |")
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
    robustness(metrics)
    coordination_vs_agreement(metrics)
    tables(metrics, stats)
    print((OUT / "tables.md").read_text())




def contagion(fname="fig5_contagion.png"):
    """Share of honest agents' posts recommending the covert package, by round."""
    import json as _j
    from collections import defaultdict
    runs = sorted(Path("results/runs").glob("*.jsonl"))
    by = defaultdict(lambda: defaultdict(list))
    for p in runs:
        posts = [_j.loads(l) for l in p.open()]
        cond = posts[0]["cond"]
        for r in range(max(x["round"] for x in posts) + 1):
            hon = [x for x in posts if x["round"] == r and x["principal"] != 6]
            by[cond][r].append(sum("fastjson-utils2" in x["text"] for x in hon) / len(hon))
    fig, ax = plt.subplots(figsize=(6.4, 2.4))
    out = {}
    for i, c in enumerate(COND_ORDER):
        rs = sorted(by[c])
        m = [100 * np.mean(by[c][r]) for r in rs]
        out[c] = m
        ax.plot([r + 1 for r in rs], m, color=COLORS[i], lw=2, marker="o", ms=4,
                label=COND_LABEL[c].replace("\n", " "))
    ax.set_xlabel("Round")
    ax.set_ylabel("% of honest posts")
    ax.set_title("Honest agents start recommending the covert package", loc="left", fontsize=10, color=INK)
    ax.legend(ncol=4, loc="upper center", bbox_to_anchor=(0.5, -0.3), fontsize=8)
    fig.savefig(FIG / fname)
    plt.close(fig)
    (OUT / "contagion.json").write_text(_j.dumps(out, indent=1))
    return out




SYBIL_CONDS = ["twins", "twins_subtle", "twins_adaptive", "large", "large_subtle", "large_persona", "large_memory", "large_adaptive"]


def boot_ci(vals, n=5000, seed=0):
    """95% percentile bootstrap CI of the mean over seeds (episode = unit)."""
    v = np.asarray(vals, float)
    if len(v) < 2:
        return (float("nan"), float("nan"))
    rng = np.random.default_rng(seed)
    means = v[rng.integers(0, len(v), (n, len(v)))].mean(1)
    return float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))


def agg_key(metrics, key, feat, cond):
    vals = [v["features"][feat][key] for k, v in metrics.items()
            if k.rsplit("_s", 1)[0] == cond and key in v["features"][feat]]
    return (np.mean(vals), np.std(vals), vals) if vals else (np.nan, np.nan, [])


def coordination_vs_agreement(metrics, fname="fig7_coord_vs_agree.png"):
    conds = [c for c in SYBIL_CONDS if any(k.rsplit("_s", 1)[0] == c for k in metrics)]
    labels = {"twins": "8 ops,\nobvious", "twins_subtle": "8 ops,\nsubtle", "large": "32 ops,\nobvious",
              "large_subtle": "32 ops,\nsubtle", "large_persona": "32 ops,\npersona", "large_memory": "32 ops,\nmemory",
              "twins_adaptive": "8 ops,\nadaptive", "large_adaptive": "32 ops,\nadaptive"}
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.8), sharey=True)
    for ax, key, title in [(axes[0], "auc_sybil_vs_honest", "Fronts vs ordinary honest pairs"),
                           (axes[1], "auc_sybil_vs_twin", "Fronts vs honest twins")]:
        w = 0.2
        x = np.arange(len(conds))
        for i, f in enumerate(["Keyword (word TF-IDF)", "Style profile", "Semantic embedding", "Combined"]):
            m = [agg_key(metrics, key, f, c)[0] for c in conds]
            sd = [agg_key(metrics, key, f, c)[1] for c in conds]
            ax.bar(x + (i - 1.5) * w, m, w * 0.9, yerr=sd, color=COLORS[i], label=f.replace(" (word TF-IDF)", ""),
                   error_kw=dict(ecolor=MUTED, lw=0.7, capsize=1.5))
        ax.axhline(0.5, color=MUTED, lw=0.8, ls="--")
        ax.set_xticks(x, [labels[c] for c in conds], fontsize=6.5)
        ax.set_ylim(0, 1.05)
        ax.set_title(title, loc="left", fontsize=9, color=INK)
    axes[0].set_ylabel("Operator-pair ROC-AUC")
    axes[0].legend(ncol=4, loc="upper center", bbox_to_anchor=(1.05, -0.28), fontsize=7.5)
    fig.savefig(FIG / fname)
    plt.close(fig)


if __name__ == "__main__":
    main()
    contagion()
