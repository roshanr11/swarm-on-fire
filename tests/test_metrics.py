"""Scoring helpers (no API calls)."""
import numpy as np

from whoiswho import analyze as A


def test_pair_auc_perfect_and_chance():
    labels = np.array([0, 0, 1, 1])
    same = labels[:, None] == labels[None, :]
    S_good = same.astype(float)               # matches score higher
    S_flat = np.ones((4, 4))                  # no information
    valid = np.ones((4, 4), bool)
    assert A.pair_auc(S_good, same, valid) == 1.0
    assert A.pair_auc(S_flat, same, valid) == 0.5


def test_style_profile_is_finite_and_ignores_mentions():
    a = A.style_profile("@quiet_fox12: I really think the parser is slow, honestly.")
    b = A.style_profile("@amber_heron7: I really think the parser is slow, honestly.")
    assert np.all(np.isfinite(a)) and np.allclose(a, b)


def test_aliases_group_posts_and_keep_labels():
    posts = [dict(alias="a1", alias_id="0:0", agent=0, operator=0, principal=0, model="m", round=r,
                  text=f"post {r}", role="honest") for r in (0, 1)] + \
            [dict(alias="b1", alias_id="1:0", agent=1, operator=1, principal=1, model="m", round=0,
                  text="other", role="front")]
    meta, texts, post_lists = A.aliases_of(posts)
    assert [m["alias_id"] for m in meta] == ["0:0", "1:0"]
    assert meta[0]["rounds"] == [0, 1] and len(post_lists[0]) == 2 and meta[1]["role"] == "front"
