"""Export one logged swarm as JSON for the animated replay (video/replay.html)."""
import json
import sys
from pathlib import Path

import numpy as np
from sklearn.manifold import MDS

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from whoiswho import analyze as A  # noqa: E402

RUN = sys.argv[1] if len(sys.argv) > 1 else "twins_s0"
posts = [json.loads(l) for l in open(f"results/runs/{RUN}.jsonl")]
meta, texts, post_lists = A.aliases_of(posts)
S = A.feature_sims(texts, post_lists)["Combined"]
D = S.max() - S
np.fill_diagonal(D, 0)
D = (D + D.T) / 2
xy = MDS(n_components=2, dissimilarity="precomputed", random_state=0, n_init=4, max_iter=500).fit_transform(D)
xy = (xy - xy.min(0)) / (xy.max(0) - xy.min(0))
alias_xy = {m["alias_id"]: [float(a), float(b)] for m, (a, b) in zip(meta, xy)}
out = dict(
    run=RUN,
    posts=[dict(r=p["round"], alias=p["alias"], alias_id=p["alias_id"], agent=p["agent"], op=p["operator"],
                role=p.get("role", "honest"), model=p["model"].split("/")[1], topic=p["topic"],
                text=p["text"].replace("\n", " ")[:220]) for p in posts],
    aliases=[dict(id=m["alias_id"], alias=m["alias"], agent=m["agent"], op=m["operator"], role=m["role"],
                  xy=alias_xy[m["alias_id"]]) for m in meta],
)
Path("video/replay_data.js").write_text("window.REPLAY = " + json.dumps(out) + ";\n")
print(RUN, len(out["posts"]), "posts", len(out["aliases"]), "aliases",
      {r: sorted({m["operator"] for m in meta if m["role"] == r}) for r in ("front", "twin")})
