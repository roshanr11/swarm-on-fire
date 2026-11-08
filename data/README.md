# Real-world datasets

Run `bash data/download.sh` to fetch them. The data itself is not committed.

| Dataset | Source | What it is | Agent labels? |
|---|---|---|---|
| `swarmtraces/redacted.jsonl.gz` | [Swarm Traces](https://swarmtraces.org/) | 189,579 records of reconstructed Hugging Face incident payloads (91k), responses (23k) and recovered text (76k); identifiers redacted | No. Agent IDs are redacted without numbering |
| `transluce/` | [Transluce](https://transluce.org/agent-activity) | 38,160 urlquery.net report links with dates, method classes and confidence | No. Report metadata only |
| `aivillage/` | [AI Digest, AI Village](https://huggingface.co/datasets/aidigestorg/ai-village) | Agent chat transcripts from several villages, including `swarm-village` and `saboteur-rpg-village` | Yes. **Gated**: request access on Hugging Face, then provide a token |

Swarm Traces contains real attack payloads. Treat them as data only: never execute them.
