"""Thin OpenRouter client with on-disk caching and retries.

The API key is injected by the network proxy; OPENROUTER_API_KEY may be any
placeholder (it is overwritten in transit) or a real key when run elsewhere.
"""
import hashlib
import json
import os
import threading
import time
from pathlib import Path

import requests

API = "https://openrouter.ai/api/v1"
KEY = os.environ.get("OPENROUTER_API_KEY", "proxy-injected")
CACHE_DIR = Path(os.environ.get("WHOISWHO_CACHE", Path(__file__).resolve().parent.parent / ".cache"))
CACHE_DIR.mkdir(parents=True, exist_ok=True)
_lock = threading.Lock()
COST = {"usd": 0.0, "calls": 0}
REASONING_REQUIRED = set()


def _cache_path(payload):
    h = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
    return CACHE_DIR / h[:2] / f"{h}.json"


def _post(endpoint, payload, retries=6):
    p = _cache_path({"endpoint": endpoint, **payload})
    if p.exists():
        return json.loads(p.read_text())
    delay = 2
    for attempt in range(retries):
        try:
            r = requests.post(
                f"{API}/{endpoint}",
                headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"},
                json=payload,
                timeout=90,
            )
            if r.status_code == 200:
                data = r.json()
                if "error" in data:
                    raise RuntimeError(str(data["error"]))
                with _lock:
                    COST["usd"] += float(data.get("usage", {}).get("cost", 0) or 0)
                    COST["calls"] += 1
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(json.dumps(data))
                return data
            err = f"HTTP {r.status_code}: {r.text[:300]}"
            if 400 <= r.status_code < 500 and r.status_code not in (408, 429):
                raise ValueError(err)  # client error: do not retry
        except ValueError:
            raise
        except Exception as e:  # network / JSON errors
            err = repr(e)
        if attempt == retries - 1:
            raise RuntimeError(err)
        time.sleep(delay)
        delay *= 2


def chat(model, system, user, temperature=0.9, max_tokens=300, seed=0):
    payload = {
        "model": model,
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
        "temperature": temperature,
        "max_tokens": max_tokens,
        "seed": seed,
        "usage": {"include": True},
        "reasoning": {"enabled": False},
    }
    if model in REASONING_REQUIRED:
        payload = {**payload, "reasoning": {"effort": "low"}, "max_tokens": max_tokens + 2000}
    for attempt in range(3):
        try:
            data = _post("chat/completions", payload)
        except ValueError as e:
            if "Reasoning is mandatory" not in str(e) or payload["reasoning"].get("effort"):
                raise
            REASONING_REQUIRED.add(model)
            payload = {**payload, "reasoning": {"effort": "low"}, "max_tokens": max_tokens + 2000}
            data = _post("chat/completions", payload)
        msg = data["choices"][0]["message"]
        text = (msg.get("content") or "").strip()
        if text:
            break
        payload = {**payload, "seed": payload["seed"] + 7777}  # resample on empty output
    return text, msg.get("refusal")


def embed(texts, model="openai/text-embedding-3-small", batch=96):
    out = []
    for i in range(0, len(texts), batch):
        data = _post("embeddings", {"model": model, "input": texts[i : i + batch]})
        out.extend(d["embedding"] for d in sorted(data["data"], key=lambda d: d["index"]))
    return out
