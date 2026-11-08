# Who Is Who in a Swarm?

**Re-identifying renamed LLM agents, and the operators behind them, from behaviour alone.**
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
| Behavioural fingerprints | Stylometry (char n-grams, function-word/punctuation profile) and topic-centred semantic embeddings |
| Gateway + fingerprints | Attestation, plus fingerprint similarity to merge operator accounts that are likely the same principal (sybil fronts) |

I test the fingerprints under three evasion strategies: a new persona on every rename,
paraphrase laundering through a different model, and operators spreading their agents
over several base models. Robustness conditions add per-agent memory, no house style, keyword-free (subtle) agendas, frontier models, randomised roles with *honest twins* (independent operators with the same sincere agenda), and a 160-agent scale-up.

## Key results (62 swarms · 4,400 agents · 44,000 posts · 8 models · up to 160 agents per swarm · ~$12.60 of API spend)

1. **Anything the agent controls, it can discard.** Self-chosen names and rotatable agent-held keys recover nothing (F1 = 0).
2. **Fingerprints identify the configuration, not the instance.** Same-operator AUC is 0.93–0.96, but same-agent within one operator is 0.50 (chance) at both scales and with frontier models. Only per-agent memory (0.56) or mixing base models (0.71) breaks the tie.
3. **Style hides, goals leak.** Paraphrase laundering pushes style features to 0.58, while topic-centred semantic features keep 0.82.
4. **Shared agendas, not coordination.** Fronts of one covert principal stand out from ordinary operators (0.94–1.00), but barely from *honest twins* who sincerely share a view (0.20 with 8 operators; 0.54–0.62 with 32). At scale, automatic fingerprint merging finds 60–85% of front pairs, but about half of its merges are wrong. F1 falls below gateway attestation alone (0.84 vs 0.88).
5. **The honest crowd pushes back.** 67% of honest mentions of a covert product were sceptical; only 13% endorsed it.
6. **Real-data probe** (Swarm Traces, 20k artefacts): shared-scaffolding families around a long tail of near-unique payloads. Exploratory only, since there are no agent labels.

**Takeaway:** anchor identity at the gateway (per-instance credentials, out of the agent's reach), and use behavioural fingerprints as audit *leads* for human review, never as proof of coordination.

Report: [`report/report.pdf`](report/report.pdf) · Tables with bootstrap CIs: [`results/tables.md`](results/tables.md) · Novelty review: [`report/novelty_review.md`](report/novelty_review.md)

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
- `whoiswho/analyze.py`: fingerprints, pairwise AUCs, clustering, identity-scheme scoring
- `whoiswho/plots.py`: figures and tables
- `whoiswho/report.py`: builds the PDF report
- `results/`: logs, metrics, figures

## Prior work

None. All code was written during the sprint weekend. No pre-existing code is used.

## Safety note

The "covert" objective is a harmless stand-in: promoting a fictional package. No agent
had tools, network access or real-world effects. See the report appendix for dual-use
considerations.
