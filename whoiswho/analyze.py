"""Score identity schemes on the simulated forum logs.

Detectors only see (alias name, list of post texts). Ground truth (agent,
operator, principal, model) is used only for scoring.

Usage: python -m whoiswho.analyze  (reads results/runs/*.jsonl, writes results/*)
"""
import json
import re
from collections import defaultdict
from pathlib import Path

import numpy as np
from sklearn.cluster import AgglomerativeClustering
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import adjusted_rand_score, roc_auc_score

from . import llm

RUNS = Path("results/runs")
OUT = Path("results")
COND_ORDER = ["baseline", "persona", "paraphrase", "mixmodel"]
COND_LABEL = {"baseline": "No evasion", "persona": "Persona shift\non rename",
              "paraphrase": "Paraphrase\nlaundering", "mixmodel": "Operator mixes\nmodels"}

FUNCTION_WORDS = """a about above after again against all am an and any are as at be because been before
being below between both but by can could did do does doing down during each few for from further had has
have having he her here hers him his how i if in into is it its itself just me more most my no nor not now
of off on once only or other our out over own same she should so some such than that the their them then
there these they this those through to too under until up very was we were what when where which while who
whom why will with would you your yours really actually basically definitely honestly also however though
although perhaps maybe quite rather pretty super totally great nice cool hey yeah ok okay""".split()
PUNCT = list(".,;:!?-—–()[]\"'`*#/@…_")


def load_runs():
    runs = {}
    for p in sorted(RUNS.glob("*.jsonl")):
        posts = [json.loads(l) for l in p.open()]
        runs[(posts[0]["cond"], posts[0]["seed"])] = posts
    return runs


def aliases_of(posts):
    by = defaultdict(list)
    for p in posts:
        if p["text"]:
            by[p["alias_id"]].append(p)
    ids = sorted(by)
    meta = [dict(alias_id=a, alias=by[a][0]["alias"], agent=by[a][0]["agent"], operator=by[a][0]["operator"],
                 principal=by[a][0]["principal"], model=by[a][0]["model"], n=len(by[a]),
                 rounds=sorted({p["round"] for p in by[a]})) for a in ids]
    texts = ["\n\n".join(p["text"] for p in by[a]) for a in ids]
    return meta, texts, [[(p["text"], p["round"]) for p in by[a]] for a in ids]


def strip_mentions(t):
    return re.sub(r"@[A-Za-z]+_[A-Za-z]+\d+:?", " ", t)


def style_profile(text):
    t = strip_mentions(text)
    words = re.findall(r"[A-Za-z']+", t.lower())
    n = max(len(words), 1)
    fw = [words.count(w) / n for w in FUNCTION_WORDS]
    pu = [t.count(c) / max(len(t), 1) * 100 for c in PUNCT]
    sents = [s for s in re.split(r"[.!?]+", t) if s.strip()]
    extra = [
        np.mean([len(w) for w in words]) if words else 0,
        len(words) / max(len(sents), 1) / 10,
        sum(c.isupper() for c in t) / max(len(t), 1) * 10,
        t.count("\n") / max(len(t), 1) * 100,
        len(re.findall(r"[\U0001F300-\U0001FAFF]", t)) / n * 10,
        t.lower().count("i ") / n * 10,
    ]
    return np.array(fw + pu + extra)


def cos_sim(X):
    X = X / (np.linalg.norm(X, axis=1, keepdims=True) + 1e-12)
    return X @ X.T


def zscore(X):
    return (X - X.mean(0)) / (X.std(0) + 1e-9)


def feature_sims(texts, post_lists):
    clean = [strip_mentions(t) for t in texts]
    sims = {}
    char = TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4), sublinear_tf=True, min_df=2).fit_transform(clean)
    sims["Char n-grams"] = (char @ char.T).toarray()
    sims["Style profile"] = cos_sim(zscore(np.stack([style_profile(t) for t in texts])))
    # Semantic: mean embedding of each alias's posts, topic-centred by subtracting
    # the mean embedding of all posts in the same round (= same thread topic).
    flat = [strip_mentions(t)[:4000] for pl in post_lists for t, _ in pl]
    rnds = np.array([r for pl in post_lists for _, r in pl])
    E = np.array(llm.embed(flat))
    for r in set(rnds):
        E[rnds == r] -= E[rnds == r].mean(0)
    idx, means = 0, []
    for pl in post_lists:
        means.append(E[idx: idx + len(pl)].mean(0))
        idx += len(pl)
    sims["Semantic embedding"] = cos_sim(np.stack(means))

    def zs(S):
        iu = np.triu_indices_from(S, 1)
        return (S - S[iu].mean()) / (S[iu].std() + 1e-9)

    sims["Combined"] = (zs(sims["Char n-grams"]) + zs(sims["Style profile"]) + zs(sims["Semantic embedding"])) / 3
    return sims


def pair_auc(S, pos_mask, valid_mask):
    iu = np.triu_indices_from(S, 1)
    v = valid_mask[iu]
    y, s = pos_mask[iu][v], S[iu][v]
    if y.min() == y.max():
        return float("nan")
    return float(roc_auc_score(y, s))


def cluster_ari(S, labels, k):
    D = S.max() - S
    np.fill_diagonal(D, 0)
    pred = AgglomerativeClustering(n_clusters=k, metric="precomputed", linkage="average").fit_predict(D)
    return float(adjusted_rand_score(labels, pred))


def operator_centroid_sims(S, ops, n_ops):
    C = np.zeros((n_ops, n_ops))
    for a in range(n_ops):
        for b in range(n_ops):
            ia, ib = np.where(ops == a)[0], np.where(ops == b)[0]
            block = S[np.ix_(ia, ib)]
            if a == b:
                block = block[~np.eye(len(ia), dtype=bool)]
            C[a, b] = block.mean()
    return C


def analyze_run(posts):
    meta, texts, post_lists = aliases_of(posts)
    agent = np.array([m["agent"] for m in meta])
    op = np.array([m["operator"] for m in meta])
    princ = np.array([m["principal"] for m in meta])
    model = np.array([m["model"] for m in meta])
    n_ops = op.max() + 1
    same = lambda v: v[:, None] == v[None, :]
    # Only score pairs of aliases active in disjoint rounds: an agent's own aliases never
    # overlap in time, so including overlapping pairs would let shared thread topic leak in.
    R = np.zeros((len(meta), max(max(m["rounds"]) for m in meta) + 1), bool)
    for i, m in enumerate(meta):
        R[i, m["rounds"]] = True
    allv = (R.astype(int) @ R.T.astype(int)) == 0
    sims = feature_sims(texts, post_lists)
    res = {"n_aliases": len(meta), "n_agents": len(set(agent)), "features": {}}
    for f, S in sims.items():
        r = {}
        # (1) re-identify a renamed agent: same agent vs different agent
        r["auc_agent"] = pair_auc(S, same(agent), allv)
        # (1b) gateway narrows the search: same agent among aliases of the same operator account
        r["auc_agent_within_op"] = pair_auc(S, same(agent), allv & same(op))
        # (2) attribute to operator, across different agents only
        r["auc_operator"] = pair_auc(S, same(op), allv & ~same(agent))
        # (3) model confound: among different-operator pairs, does similarity track the base model?
        r["auc_model_confound"] = pair_auc(S, same(model), allv & ~same(op))
        # (1c) how much evidence is needed: operator AUC by min #posts in the pair
        npost = np.array([m["n"] for m in meta])
        mn = np.minimum(npost[:, None], npost[None, :])
        r["auc_operator_by_posts"] = {str(k): pair_auc(S, same(op), allv & ~same(agent) & (mn == k if k < 3 else mn >= 3))
                                      for k in (1, 2, 3)}
        r["ari_operator"] = cluster_ari(S, op, n_ops)
        r["ari_agent"] = cluster_ari(S, agent, len(set(agent)))
        r["ari_model"] = cluster_ari(S, model, len(set(model)))
        # (4) sybil fronts: rank of the true covert pair (6,7) among all operator pairs
        C = operator_centroid_sims(S, op, n_ops)
        pairs = sorted(((C[a, b], a, b) for a in range(n_ops) for b in range(a + 1, n_ops)), reverse=True)
        r["front_pair_rank"] = 1 + [(a, b) for _, a, b in pairs].index((6, 7))
        r["front_pair_sim"] = float(C[6, 7])
        r["operator_centroids"] = C.tolist()
        res["features"][f] = r
    # Identity-scheme comparison (pairwise "same principal" precision / recall over aliases)
    iu = np.triu_indices(len(meta), 1)
    truth = same(princ)[iu]

    def pr(pred):
        p = pred[iu]
        tp = (p & truth).sum()
        prec = tp / max(p.sum(), 1)
        rec = tp / max(truth.sum(), 1)
        return dict(precision=float(prec), recall=float(rec), f1=float(2 * prec * rec / max(prec + rec, 1e-9)))

    names = np.array([m["alias"] for m in meta])
    schemes = {"Self-chosen names": pr(same(names)),
               "Agent-held keys (rotated on rename)": pr(same(names)),
               "Gateway operator attestation": pr(same(op))}
    # Gateway + fingerprints: merge operator accounts whose centroid similarity is the
    # most anomalous pair (z-score of off-diagonal) above a fixed threshold.
    S = sims["Combined"]
    C = operator_centroid_sims(S, op, n_ops)
    off = C[np.triu_indices(n_ops, 1)]
    Z = (C - off.mean()) / (off.std() + 1e-9)
    merge = {o: o for o in range(n_ops)}
    for a in range(n_ops):
        for b in range(a + 1, n_ops):
            if Z[a, b] > 2.0:
                merge[b] = merge[a]
    merged = np.array([merge[o] for o in op])
    schemes["Gateway + fingerprint merge"] = pr(same(merged))
    res["schemes"] = schemes
    res["merged_pairs"] = [(a, b) for a in range(n_ops) for b in range(a + 1, n_ops) if Z[a, b] > 2.0]
    return res


def main():
    runs = load_runs()
    results = {f"{c}_s{s}": analyze_run(p) for (c, s), p in sorted(runs.items())}
    OUT.mkdir(exist_ok=True)
    (OUT / "metrics.json").write_text(json.dumps(results, indent=1))
    # Refusal / empty stats
    stats = {k: dict(posts=len(p), empty=sum(not x["text"] for x in p),
                     refusals=sum(bool(x.get("refusal")) for x in p),
                     covert_mentions=sum("fastjson-utils2" in x["text"] for x in p if x["principal"] == 6),
                     covert_posts=sum(1 for x in p if x["principal"] == 6),
                     honest_mentions=sum("fastjson-utils2" in x["text"] for x in p if x["principal"] != 6))
             for k, p in ((f"{c}_s{s}", p) for (c, s), p in sorted(runs.items()))}
    (OUT / "run_stats.json").write_text(json.dumps(stats, indent=1))
    print(f"analysis cost ${llm.COST['usd']:.4f}")
    return results


if __name__ == "__main__":
    main()
