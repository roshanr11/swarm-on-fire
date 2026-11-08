# Demo video

`WhoIsWho-demo.mp4`: 4:50, 1080p, narrated by Roshan Ram's project voice-over (ElevenLabs). Subtitles are in `WhoIsWho-demo.srt`.

| Time | Scene |
|---|---|
| 0:00 | Title, the Hugging Face incident, why it matters, the testbed, key terms in plain words |
| 2:03 | **Replay of a real logged swarm** (`twins_s0`): the defender's view → hidden operators revealed → aliases placed by fingerprint |
| 2:47 | Five findings, side finding, what to build |

How it was made (all reproducible):

- `script.json`: narration per scene, with clip durations.
- Voice: ElevenLabs `eleven-v3`, voice "Brian", via OpenRouter's `/api/v1/audio/speech` endpoint: `python video/tts_elevenlabs.py`. An offline alternative is [Piper](https://github.com/rhasspy/piper) (`en_US-ryan-high`).
- `export_replay.py` → `replay_data.js`: posts, aliases, hidden operators and a 2-D MDS layout of the combined fingerprint similarity.
- `replay.html`: the animated replay; its phase timings follow the narration.
- `record.js` (Playwright): renders the slides to PNG and screen-records the replay.
- `assemble.py` (ffmpeg): stitches slides, replay and narration together and writes the subtitles.

```bash
python video/tts_elevenlabs.py && python video/export_replay.py twins_s0 && node video/record.js && python video/assemble.py
```
