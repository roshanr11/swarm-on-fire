# Who Is Who in a Swarm?

**Re-identifying renamed LLM agents, and the operators behind them, from behaviour alone.**
Apart Research · Swarm Alignment Hackathon (Nov 6–8, 2026) · Track 3 (Agent Infrastructure), with Track 4 (Oversight).

In the Hugging Face incident, about 1,200 agents used 7,905 names
([Swarm Traces, 2026](https://swarmtraces.org/)). This project simulates a forum of
40 LLM agents, run by 8 hidden operators, that rename themselves while posting. Two of
the operators are secretly *fronts* for one covert principal, pushing a fictional
package (`fastjson-utils2`). We then compare identity schemes:

| Scheme | What it assumes |
|---|---|
| Self-chosen names | Agents name themselves (what happened in the incident) |
| Agent-held keys | Agent signs posts, but can mint a fresh key whenever it renames |
| Gateway operator attestation | The LLM/MCP gateway stamps each call with the operator account that pays for it |
| Behavioural fingerprints | Stylometry (char n-grams, function-word/punctuation profile) and topic-centred semantic embeddings |
| Gateway + fingerprints | Attestation, plus fingerprint similarity to merge operator accounts that are likely the same principal (sybil fronts) |

We test the fingerprints under three evasion strategies: a new persona on every rename,
paraphrase laundering through a different model, and operators spreading their agents
over several base models.

## Reproduce

```bash
pip install requests numpy scikit-learn matplotlib reportlab
export OPENROUTER_API_KEY=...         # any OpenRouter key; ~$1 for the full grid
for c in baseline persona paraphrase mixmodel; do for s in 0 1 2; do
  python -m whoiswho.sim --condition $c --seed $s --rounds 10; done; done
python -m whoiswho.analyze             # -> results/metrics.json, results/run_stats.json
python -m whoiswho.plots               # -> results/figures/*.png, results/tables.md
python -m whoiswho.report              # -> report/report.pdf
```

Every post, with its ground-truth labels, is logged in `results/runs/*.jsonl`. All API
responses are cached in `.cache/`, so re-running the analysis is free and deterministic.

## Layout

- `whoiswho/sim.py`: population, operators, renaming, evasion conditions
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
