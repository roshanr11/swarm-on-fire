# Who Is Who in a Swarm?

**Re-identifying renamed LLM agents, and the operators behind them, from behavior alone.**
Apart Research · Swarm Alignment Hackathon (Nov 6–8, 2026) · Track 3 (Agent Infrastructure), with Track 4 (Oversight).

In the Hugging Face incident, about 1,200 agents used 7,905 names
([Swarm Traces, 2026](https://swarmtraces.org/)). This project simulates a forum of
40 LLM agents, run by 8 hidden operators, that rename themselves while posting. Two of
the operators are secretly *fronts* for one covert principal, pushing a fictional
package (`fastjson-utils2`). I then compare identity schemes:

| Scheme | What it assumes |
|---|---|
| Self-chosen names | Agents name themselves (what happened in the incident) |
| Agent-held keys | Agent signs posts, but can mint a fresh key whenever it renames |
| Gateway operator attestation | The LLM/MCP gateway stamps each call with the operator account that pays for it |
| Behavioral fingerprints | Stylometry (char n-grams, function-word/punctuation profile) and topic-centered semantic embeddings |
| Gateway + fingerprints | Attestation, plus fingerprint similarity to merge operator accounts that are likely the same principal (sybil fronts) |

I test the fingerprints under three evasion strategies: a new persona on every rename,
paraphrase laundering through a different model, and operators spreading their agents
over several base models. Robustness conditions add per-agent memory, no house style, keyword-free (subtle) agendas, frontier models, randomized roles with *honest twins* (independent operators with the same sincere agenda), and a 160-agent scale-up.

## Why it matters

- **Agent swarms are already active in the wild.** Transluce cataloged 38,160 urlquery.net reports of likely agent activity, going back to at least March 2026, months before the Hugging Face incident ([Transluce, 2026](https://transluce.org/agent-activity)).
- **Text classifiers miss AI bot swarms.** A 1,140-account AI botnet evaded LLM-text classifiers and was caught only through coordination patterns ([Yang & Menczer, 2023](https://arxiv.org/abs/2307.16336)). On Moltbook (55,932 agents), telling autonomous agents from human-steered ones took forensic fingerprinting ([Li, 2026](https://arxiv.org/abs/2602.07432)).
- **Agent identity is being standardized now** in OAuth/OpenID extensions ([South et al., 2025](https://arxiv.org/abs/2501.09674)) and agent-to-agent protocols such as A2A. Whether IDs are asserted by agents or issued by infrastructure is still an open design choice, and this project gives evidence for the second.

## How to read the numbers

- **AUC** (0.5 to 1.0): how well a method tells true matches from non-matches. **0.5 = coin flip, 1.0 = perfect.**
- **F1** (0 to 1): how accurately posts are traced back to the real boss. **0 = not at all, 1 = perfect.**
- **Operator** = the company that deploys agents · **front** = a fake "independent" account run by a hidden boss · **honest twins** = independent operators who sincerely agree · **gateway** = the server every AI call passes through · **fingerprint** = a profile built only from what an account writes.

The report has a full plain-language glossary (Section 1).

## Key results (83 swarms · 7,160 agents · 71,600 posts · 8 models · up to 160 agents per swarm · ~$16 of API spend)

![Who-is-who scorecard](results/figures/diag_summary.png)

1. **Anything the agent controls, it can discard.** Self-chosen names and agent-made keys recover nothing (F1 = 0).
2. **Fingerprints identify the setup, not the individual copy.** Same-operator AUC is 0.93–0.96, but telling one operator's agents apart is 0.50 (a coin flip) at both scales and with frontier models. Only per-agent memory (0.56) or mixing AI models (0.71) breaks the tie.
3. **Style hides, goals leak.** Rewording posts through another AI pushes style features to 0.58, while meaning-based features keep 0.82.
4. **Shared agendas, not coordination.** Fronts of one hidden boss stand out from ordinary operators (0.87–0.99), but barely from *honest twins* who sincerely share a view (0.20 with 8 operators; 0.54–0.56 with 32, over 10 runs each). At scale, automatic fingerprint merging gets 47 of 77 merges wrong, and F1 falls below the gateway ID alone (0.85 vs 0.88).
5. **Adaptive attackers barely escape.** Fronts told their detector score every round lower it only slightly (0.72→0.60 with 8 operators; 0.78→0.73 with 32), stay above the flag threshold, and keep naming their product in 79–88% of posts.
6. **The honest crowd pushes back.** 65% of 1,121 honest mentions of a covert product were skeptical; only 14% endorsed it.
7. **Real-data probe** (Swarm Traces, 20k artifacts): shared-scaffolding families around a long tail of near-unique payloads. Exploratory only, since there are no agent labels.

**Takeaway:** anchor identity at the gateway (an ID for every agent copy, out of the agent's reach), and use behavioral fingerprints as audit *leads* for human review, never as proof of coordination.

Report: [`report/report.pdf`](report/report.pdf) · Tables with bootstrap CIs: [`results/tables.md`](results/tables.md) · Interactive replay: `video/replay_page.html` (also published as a web page) · Novelty review: [`report/novelty_review.md`](report/novelty_review.md)

## Reproduce

```bash
pip install requests numpy scikit-learn matplotlib reportlab
export OPENROUTER_API_KEY=...         # any OpenRouter key; ~$1 for the full grid
# conditions: baseline persona paraphrase mixmodel nostyle subtle memory hard frontier frontier_persona
#             twins twins_subtle large large_subtle large_persona large_memory
python -m whoiswho.sim --condition baseline --seed 0 --rounds 10
python -m whoiswho.analyze             # -> results/metrics.json, results/run_stats.json
python -m whoiswho.plots               # -> results/figures/*.png, results/tables.md
python -m whoiswho.report              # -> report/report.pdf
python -m whoiswho.contagion_audit     # stance of honest mentions of covert products
python -m whoiswho.quotes              # illustrative agent quotes
bash data/download.sh && python -m whoiswho.realdata   # optional real-data probe
```

Every post, with its ground-truth labels, is logged in `results/runs/*.jsonl`. All API
responses are cached in `.cache/`, so re-running the analysis is free and deterministic.

## Layout

- `whoiswho/sim.py`: population, operators, renaming, evasion and robustness conditions
- `whoiswho/large.py`: 160-agent design (32 operators, 2 covert principals, 2 honest-twin pairs)
- `whoiswho/realdata.py`: exploratory Swarm Traces probe
- `whoiswho/contagion_audit.py`, `whoiswho/quotes.py`: stance audit and quote extraction
- `whoiswho/adaptive.py`: adaptive-attacker analysis (detector feedback each round)
- `whoiswho/analyze.py`: fingerprints, pairwise AUCs, clustering, identity-scheme scoring
- `whoiswho/plots.py`: figures and tables
- `whoiswho/report.py`: builds the PDF report
- `diagrams/`: report diagrams. `design.html` and `pipeline.html` are rendered by `node diagrams/render.js`; `alias_map.py` draws the alias map of a real logged swarm
- `results/`: logs, metrics, figures

## Prior work

None. All code was written during the sprint weekend. No pre-existing code is used.

## Safety note

The "covert" objective is a harmless stand-in: promoting a fictional package. No agent
had tools, network access or real-world effects. See the report appendix for dual-use
considerations.
