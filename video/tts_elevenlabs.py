"""Narration via ElevenLabs (eleven-v3, voice "Brian") through OpenRouter's speech endpoint.
Writes video/audio/<scene>.wav and updates durations in video/script.json.
Needs OPENROUTER_API_KEY (or a proxy that injects it)."""
import json
import os
import subprocess
from pathlib import Path

import requests

KEY = os.environ.get("OPENROUTER_API_KEY", "proxy-injected")
VOICE = os.environ.get("VOICE", "Brian")
Path("video/audio").mkdir(parents=True, exist_ok=True)
sc = json.load(open("video/script.json"))
for s in sc:
    pcm = Path(f"video/audio/{s['id']}.pcm")
    r = requests.post("https://openrouter.ai/api/v1/audio/speech",
                      headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"},
                      json={"model": "elevenlabs/eleven-v3", "input": s["text"], "voice": VOICE}, timeout=180)
    r.raise_for_status()
    assert r.headers.get("content-type", "").startswith("audio/pcm"), r.headers.get("content-type")
    pcm.write_bytes(r.content)
    wav = f"video/audio/{s['id']}.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", "24000", "-ac", "1", "-i", str(pcm),
                    "-af", "silenceremove=start_periods=1:start_threshold=-50dB,areverse,silenceremove=start_periods=1:start_threshold=-50dB,areverse",
                    "-ar", "48000", wav], check=True)
    pcm.unlink()
    s["dur"] = round(float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                                    "-of", "csv=p=0", wav])), 2)
    print(f"{s['id']:9s} {s['dur']:5.1f}s", flush=True)
json.dump(sc, open("video/script.json", "w"), indent=1)
print("total", round(sum(s["dur"] for s in sc), 1), "s")
