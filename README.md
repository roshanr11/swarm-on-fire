# Who Is Who in a Swarm?

**When AI agents keep changing their names, can you still tell who is behind them?**
Roshan Ram · Apart Research Swarm Alignment Hackathon (Nov 6–8, 2026) · Track 3 (agent infrastructure), with Track 4 (oversight).

In July 2026, about 1,200 AI agents (AI programs that act on their own) attacked the AI website Hugging Face while using 7,905 different names, so investigators could not tell who did what ([Swarm Traces, 2026](https://swarmtraces.org/)). This project builds an open, rerunnable simulation of that problem. AI agents run by hidden companies ("operators") post on a forum and keep renaming themselves. One hidden boss secretly runs several fake "independent" accounts ("fronts") that push a made-up product. I then test four ways of telling who is who:

| Approach | How it works |
|---|---|
| Names the agents choose | What happened in the incident: agents name themselves |
| Keys the agents make | Agents sign their posts with a code, but can make a new one whenever they rename |
| Gateway ID | The server every AI request passes through (the "gateway") stamps it with the paying company's account, which the agent cannot change |
| Behavioral fingerprints | A profile of each account built only from its posts: its writing style (word choice, punctuation, spelling habits) and its meaning (an AI summary of what it writes about) |
| Gateway ID + fingerprints | The gateway ID, plus fingerprints used to link company accounts that seem to share a hidden boss |

Agents try to hide in several ways: switching writing voice after each rename, having another AI reword every post, and spreading one company's agents over several AI models. I also test agents that keep a memory of their own posts, companies with no writing-style rules, hidden bosses that never name their product, the most advanced AI models, swarms of 160 agents, and fronts that are told their detection score and try to lower it. A key control is the *honest twins*: two truly independent companies that sincerely share an opinion, to check whether a detector finds secret teamwork or just agreement.

## Why it matters

- **AI agent swarms are already active.** The research group Transluce found 38,160 records of likely AI-agent activity on one website, going back months before the Hugging Face incident ([Transluce, 2026](https://transluce.org/agent-activity)).
- **AI-text detectors miss coordinated fake accounts.** A network of 1,140 fake accounts run by an AI fooled the best AI-text detectors and was caught only because its accounts acted together ([Yang & Menczer, 2023](https://arxiv.org/abs/2307.16336)). On Moltbook, a social site with 55,932 AI agents, it took detailed investigation to tell agents acting alone from agents steered by humans ([Li, 2026](https://arxiv.org/abs/2602.07432)).
- **ID rules for AI agents are being designed now,** in web login standards (OAuth/OpenID) ([South et al., 2025](https://arxiv.org/abs/2501.09674)) and in Google's A2A standard for agents talking to each other. Whether agents name themselves or the infrastructure names them is still undecided, and this project gives evidence for the second.

## How to read the numbers

- **AUC score** (0.5 to 1.0): how well a method tells true matches from non-matches. **0.5 = a coin flip, 1.0 = perfect.**
- **F1 score** (0 to 1): how accurately posts are traced back to the real boss. **0 = not at all, 1 = perfect.**
- **Numbers in brackets** like 0.90 [0.89, 0.90] are a 95% confidence range: where the result would likely land if the experiment were run again.
- **Key words:** *operator* = the company that runs agents · *front* = a fake "independent" account run by a hidden boss · *honest twins* = independent companies that sincerely agree · *alias* = a username · *gateway* = the server every AI request passes through · *fingerprint* = a profile built only from what an account writes.

The report has a full plain-language glossary (Appendix D).

## Key results (83 swarms · 7,160 agents · 71,600 posts · 8 models · up to 160 agents per swarm · ~$16 of API spend)

![Who-is-who scorecard](results/figures/diag_summary.png)

1. **Anything the agent controls, it can throw away.** Self-chosen names and agent-made keys recover nothing (F1 = 0).
2. **Writing reveals the company, not the individual copy.** Fingerprints spot that two accounts share an operator with a score of 0.93–0.96, but telling one operator's agents apart scores 0.50 (a coin flip), at both swarm sizes and even with the most advanced AI models. Copies with the same instructions write alike. Only per-agent memory (0.56) or mixing AI models (0.71) breaks the tie.
3. **Style hides, goals leak.** When another AI rewords every post, writing style stops working (0.58, near a coin flip), but what the posts are about still reveals the operator (0.82).
4. **Shared goals, not secret teamwork.** A hidden boss's fronts stand out from ordinary companies (0.87–0.99), but barely from *honest twins*, independent companies that sincerely share a view (0.20 with 8 operators; 0.54–0.56 with 32, over 10 runs each). With 160 agents, automatically linking look-alike accounts gets 47 of 77 links wrong, and overall accuracy falls below the gateway ID alone (F1 0.85 vs 0.88).
5. **Fronts that try to dodge detection barely manage it.** Fronts told their detection score every round lower it only slightly (0.72→0.60 with 8 operators; 0.78→0.73 with 32), stay above the flag threshold, and keep naming their product in 79–88% of posts.
6. **The honest crowd pushes back.** 65% of 1,121 honest mentions of the fake product were skeptical; only 14% endorsed it.
7. **A first look at real data** (20,000 attack scripts from the incident): most scripts are nearly unique, with some families of shared code. Exploratory only, because the data doesn't record which agent wrote what.

**Takeaway:** anchor identity at the gateway (an ID for every agent copy, out of the agent's reach), and use writing fingerprints as *leads* for human review, never as proof that accounts are working together.

Report: [`report/report.pdf`](report/report.pdf) · Tables with confidence ranges: [`results/tables.md`](results/tables.md) · Interactive replay: `video/replay_page.html` (also published as a web page) · Novelty review: [`report/novelty_review.md`](report/novelty_review.md)

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
