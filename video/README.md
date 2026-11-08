# Demo video

`WhoIsWho-demo.mp4`: 3:28, 1080p, narrated. Subtitles are in `WhoIsWho-demo.srt`.

| Time | Scene |
|---|---|
| 0:00 | Title, the Hugging Face incident, the testbed |
| 1:02 | **Replay of a real logged swarm** (`twins_s0`): the defender's view → hidden operators revealed → aliases placed by fingerprint |
| 1:43 | Five findings, side finding, what to build |

How it was made (all reproducible):

- `script.json`: narration per scene, with clip durations.
- Voice: [Piper](https://github.com/rhasspy/piper), neural TTS run locally, voice `en_US-lessac-high`:
  `echo "<text>" | python -m piper -m en_US-lessac-high.onnx -f video/audio/<id>.wav`
- `export_replay.py` → `replay_data.js`: posts, aliases, hidden operators and a 2-D MDS layout of the combined fingerprint similarity.
- `replay.html`: the animated replay; its phase timings follow the narration.
- `record.js` (Playwright): renders the slides to PNG and screen-records the replay.
- `assemble.py` (ffmpeg): stitches slides, replay and narration together and writes the subtitles.

```bash
python video/export_replay.py twins_s0 && node video/record.js && python video/assemble.py
```
