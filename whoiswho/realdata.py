"""Exploratory probe on real swarm data (Swarm Traces, Hugging Face incident).

The payloads carry no per-agent labels (agent IDs are redacted without
numbering), so this cannot validate re-identification. It asks a weaker
question that our simulation predicts an answer to: do style fingerprints of
real swarm artefacts group them into a few families of shared scaffolding
(operator- or toolkit-level) rather than many individual-looking authors?

Payload text is treated strictly as data and never executed.
Usage: python -m whoiswho.realdata
"""
import gzip
import json
import random
import re
from collections import Counter
from pathlib import Path

import numpy as np
from scipy.sparse.csgraph import connected_components
from scipy.sparse import coo_matrix
from sklearn.feature_extraction.text import TfidfVectorizer

SRC = Path("data/swarmtraces/redacted.jsonl.gz")
OUT = Path("results/realdata_swarmtraces.json")


def normalise(t):
    t = re.sub(r"\[(?:REDACTED[^\]]*|CREDENTIAL \d+|SERVICE \d+ URL \d+|SHORTENER-\d+|ENCODED BLOB|REDACTED REPOSITORY)\]", "§", t)
    t = re.sub(r"[A-Za-z0-9+/=]{40,}", "¤", t)  # long opaque blobs
    t = re.sub(r"\d+", "0", t)
    return t


def main(sample=20000, thresholds=(0.6, 0.8, 0.9), seed=0):
    rows = [json.loads(l) for l in gzip.open(SRC, "rt")]
    payloads = [r for r in rows if r["kind"] in ("payload", "recovered_text") and len(r["text"]) >= 80]
    seen, uniq = set(), []
    for r in payloads:
        n = normalise(r["text"])
        if n not in seen:
            seen.add(n)
            uniq.append((r, n))
    random.Random(seed).shuffle(uniq)
    uniq = uniq[:sample]
    texts = [n for _, n in uniq]
    X = TfidfVectorizer(analyzer="char", ngram_range=(3, 5), sublinear_tf=True, min_df=3,
                        max_features=200_000).fit_transform(texts)
    res = {"n_records": len(rows), "n_text_artifacts": len(payloads), "n_unique_normalised": len(seen),
           "n_sampled": len(texts), "thresholds": {}}
    for th in thresholds:
        rr, cc = [], []
        for i in range(0, X.shape[0], 2000):
            S = (X[i:i + 2000] @ X.T).tocoo()
            m = S.data >= th
            rr.append(S.row[m] + i)
            cc.append(S.col[m])
        r_, c_ = np.concatenate(rr), np.concatenate(cc)
        G = coo_matrix((np.ones(len(r_)), (r_, c_)), shape=(X.shape[0], X.shape[0]))
        k, lab = connected_components(G, directed=False)
        sizes = sorted(Counter(lab).values(), reverse=True)
        cov = lambda n: float(sum(sizes[:n]) / len(texts))
        res["thresholds"][str(th)] = dict(
            families=int(k), singletons=int(sum(s == 1 for s in sizes)),
            families_ge10=int(sum(s >= 10 for s in sizes)),
            top10_coverage=cov(10), top50_coverage=cov(50),
            largest=sizes[:10],
            families_for_80pct=int(np.searchsorted(np.cumsum(sizes) / len(texts), 0.8) + 1),
        )
    OUT.write_text(json.dumps(res, indent=1))
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
