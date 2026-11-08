#!/usr/bin/env bash
# Fetch the real-world multi-agent datasets referenced by the Apart Swarm Alignment sprint.
# Skips the multi-GB AI Village files (screenshots, computer-use turns, agent memories).
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p swarmtraces transluce aivillage

# Swarm Traces (Hugging Face incident payloads), https://swarmtraces.org/
curl -sSL --retry 3 -o swarmtraces/redacted.jsonl.gz https://swarmtraces.org/data/final/redacted.jsonl.gz

# Transluce urlquery.net agent activity, https://transluce.org/agent-activity
curl -sSL --retry 3 -o transluce/urlquery-agent-activity-2026-09-23.zip \
  https://transluce.org/data/urlquery-agent-activity-2026-09-23.zip
(cd transluce && unzip -oq urlquery-agent-activity-2026-09-23.zip)

# AI Village transcripts, https://huggingface.co/datasets/aidigestorg/ai-village
BASE=https://huggingface.co/datasets/aidigestorg/ai-village/resolve/main
curl -sS "https://huggingface.co/api/datasets/aidigestorg/ai-village/tree/main?recursive=1" | python3 -c '
import json, sys
SKIP = ("agent_memories", "computer_use_turns", "/images/")
for f in json.load(sys.stdin):
    p = f["path"]
    if f["type"] == "file" and not any(s in p for s in SKIP) and f["size"] < 600_000_000:
        print(p)
' | while read -r p; do
  mkdir -p "aivillage/$(dirname "$p")"
  [ -s "aivillage/$p" ] || curl -sSL --retry 3 -o "aivillage/$p" "$BASE/$p"
done
echo "done"; du -sh swarmtraces transluce aivillage
