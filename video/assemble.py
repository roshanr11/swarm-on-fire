"""Assemble narrated slides + recorded replay into video/WhoIsWho-demo.mp4 (+ .srt)."""
import json
import re
import subprocess
from pathlib import Path

B = Path("video/build")
GAP = 0.5
FPS = 30
sc = json.load(open("video/script.json"))
enc = ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", str(FPS), "-preset", "medium", "-crf", "20",
       "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-ac", "2"]
segs, t, srt, n = [], 0.0, [], 1


def run(cmd):
    subprocess.run(cmd, check=True, capture_output=True)


def ts(x):
    h, m, s = int(x // 3600), int(x % 3600 // 60), x % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}".replace(".", ",")


def add_srt(text, start, dur):
    global n
    sents = re.split(r"(?<=[.?!:])\s+", text)
    total = sum(len(s) for s in sents)
    cur = start
    for s in sents:
        d = dur * len(s) / total
        srt.append(f"{n}\n{ts(cur)} --> {ts(cur + d)}\n{s}\n")
        n += 1
        cur += d


i = 0
while i < len(sc):
    s = sc[i]
    if s["kind"] == "slide":
        d = s["dur"] + GAP
        out = B / f"seg_{i:02d}_{s['id']}.mp4"
        run(["ffmpeg", "-y", "-loop", "1", "-framerate", str(FPS), "-i", str(B / f"slide_{s['id']}.png"),
             "-i", f"video/audio/{s['id']}.wav", "-filter_complex",
             f"[0:v]fade=t=in:st=0:d=0.3,fade=t=out:st={d-0.3:.2f}:d=0.3[v];[1:a]apad[a]",
             "-map", "[v]", "-map", "[a]", "-t", f"{d:.2f}", *enc, str(out)])
        add_srt(s["text"], t, s["dur"])
        segs.append(out); t += d; i += 1
    else:
        demo = []
        while i < len(sc) and sc[i]["kind"] == "demo":
            demo.append(sc[i]); i += 1
        # concat padded demo narration
        parts = []
        for k, s2 in enumerate(demo):
            p = B / f"demo_a{k}.wav"
            run(["ffmpeg", "-y", "-i", f"video/audio/{s2['id']}.wav", "-af", "apad", "-t", f"{s2['dur']+GAP:.2f}",
                 "-ar", "48000", "-ac", "2", str(p)])
            parts.append(p)
            add_srt(s2["text"], t + sum(x["dur"] + GAP for x in demo[:k]), s2["dur"])
        lst = B / "demo_list.txt"
        lst.write_text("".join(f"file '{p.resolve()}'\n" for p in parts))
        run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(B / "demo_audio.wav")])
        d = sum(x["dur"] + GAP for x in demo)
        off = float((B / "replay_offset.txt").read_text()) + 0.15
        out = B / f"seg_{i:02d}_demo.mp4"
        run(["ffmpeg", "-y", "-ss", f"{off:.2f}", "-i", str(B / "replay.webm"), "-i", str(B / "demo_audio.wav"),
             "-filter_complex", f"[0:v]fps={FPS},fade=t=in:st=0:d=0.3,fade=t=out:st={d-0.3:.2f}:d=0.3[v]",
             "-map", "[v]", "-map", "1:a", "-t", f"{d:.2f}", *enc, str(out)])
        segs.append(out); t += d

lst = B / "segments.txt"
lst.write_text("".join(f"file '{p.resolve()}'\n" for p in segs))
run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", "-movflags", "+faststart",
     "video/WhoIsWho-demo.mp4"])
Path("video/WhoIsWho-demo.srt").write_text("\n".join(srt))
print(f"video/WhoIsWho-demo.mp4  {t:.1f}s  {len(segs)} segments  {n-1} subtitle cues")
