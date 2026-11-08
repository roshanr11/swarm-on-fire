"""Static alias map of one logged swarm (twins_s0) from video/replay_data.js.
Usage: python diagrams/alias_map.py -> results/figures/diag_alias_map.png"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

d = json.loads(Path("video/replay_data.js").read_text().split("=", 1)[1].rstrip().rstrip(";"))
A = d["aliases"]
fronts = sorted({a["op"] for a in A if a["role"] == "front"})
twins = sorted({a["op"] for a in A if a["role"] == "twin"})
OPC = ['#5B8DEF', '#A0703E', '#E87BA4', '#E9B23A', '#8E7CF0', '#3FA34D', '#E35D6A', '#3FA9C2']
fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.5), gridspec_kw=dict(width_ratios=[1, 1]))
for ax, mode in zip(axes, ["defender", "truth"]):
    for a in A:
        x, y = a["xy"][0], 1 - a["xy"][1]
        if mode == "defender":
            ax.scatter(x, y, s=34, c="#B9BDC3", edgecolors="white", linewidths=0.6, zorder=2)
        else:
            ec = "#c8551e" if a["role"] == "front" else "#138a63" if a["role"] == "twin" else "white"
            lw = 1.6 if a["role"] in ("front", "twin") else 0.6
            ax.scatter(x, y, s=58, c=OPC[a["op"]], edgecolors=ec, linewidths=lw, zorder=2)
            ax.text(x, y, str(a["agent"] % 5 + 1), fontsize=4.6, ha="center", va="center", color="white", zorder=3, weight="bold")
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_color("#d6d1c4")
    ax.set_title("What the defender has: 226 anonymous aliases" if mode == "defender"
                 else "Revealed: color = operator, number = which agent", fontsize=8.5, loc="left", color="#17202B")
from matplotlib.lines import Line2D
h = [Line2D([], [], marker="o", ls="", mfc="#E9B23A", mec="#c8551e", mew=1.6, ms=7, label="covert front (operators %s)" % ", ".join(str(o + 1) for o in fronts)),
     Line2D([], [], marker="o", ls="", mfc="#E87BA4", mec="#138a63", mew=1.6, ms=7, label="honest twin (operators %s)" % ", ".join(str(o + 1) for o in twins))]
axes[1].legend(handles=h, loc="lower center", bbox_to_anchor=(0.5, -0.2), fontsize=7, frameon=False, ncol=1)
fig.text(0.01, -0.06, "Position = combined fingerprint similarity (2-D MDS); closer = more alike. Real logged swarm twins_s0 (8 operators × 5 agents, 10 rounds).",
         fontsize=6.8, color="#52514e")
fig.savefig("results/figures/diag_alias_map.png", dpi=220, bbox_inches="tight", facecolor="white")
print("ok", fronts, twins)
