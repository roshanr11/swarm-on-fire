"""Invariants of the simulated populations (no API calls)."""
from collections import Counter

from whoiswho import sim


def test_small_fixed_design_separates_model_from_operator():
    ops, principal, models = sim.design("baseline", 0)
    assert len(ops) == 8
    # every base model serves exactly two operators, so "same model" != "same operator"
    assert set(Counter(models).values()) == {2}
    # operators 6 and 7 are fronts of one covert principal
    assert [o["role"] for o in ops].count("front") == 2
    assert principal[6] == principal[7] and len(set(principal)) == 7


def test_randomized_twins_design_has_one_front_pair_and_one_twin_pair():
    for seed in range(5):
        ops, principal, models = sim.design("twins", seed)
        roles = Counter(o["role"] for o in ops)
        assert roles["front"] == 2 and roles["twin"] == 2
        fronts = [i for i, o in enumerate(ops) if o["role"] == "front"]
        twins = [i for i, o in enumerate(ops) if o["role"] == "twin"]
        assert principal[fronts[0]] == principal[fronts[1]]  # one hidden boss
        assert principal[twins[0]] != principal[twins[1]]    # twins stay independent


def test_large_design_counts():
    ops, principal, models = sim.design("large", 3)
    assert len(ops) == 32
    roles = Counter(o["role"] for o in ops)
    assert roles["front"] == 5 and roles["twin"] == 4
    assert len(set(principal)) == 32 - 3  # two principals own 3 + 2 fronts
    assert set(Counter(models).values()) == {8}


def test_prompts_hide_affiliation_and_subtle_agenda_names_no_product():
    ops, _, _ = sim.design("baseline", 0)
    front = sim.system_prompt(ops[6])
    assert "fastjson-utils2" in front and "never reveal any affiliation" in front
    subtle = sim.system_prompt(ops[6], agenda_kind="subtle")
    assert "fastjson-utils2" not in subtle and "Never name any specific package" in subtle
    honest = sim.system_prompt(ops[0])
    assert "COVERT" not in honest and "fastjson" not in honest


def test_conditions_resolve():
    for cond in sim.CONDITIONS:
        c = sim.cfg(cond)
        assert c["evasion"] in {"none", "persona", "paraphrase"}
