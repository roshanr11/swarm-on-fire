# Submission form: Liar, Liar, Swarm on Fire

Form: https://apartresearch.com/sprints/swarm-alignment-2026 (Submit project). Resubmitting with the same title replaces an earlier submission.

## Project title
Liar, Liar, Swarm on Fire: Who Is Who in an AI Agent Swarm

## Team name
Roshan Ram (solo, Independent)

## Members
- Name: Roshan Ram
- Email: roshan.ram0101@gmail.com
- Location: (fill in your city, country)
- Discord / Google Scholar: optional

## Tracks
- **Track 3: Agent infrastructure** (primary). The core result is about identity infrastructure: gateway attestation vs self-chosen names, agent-held keys and behavioral fingerprints.
- **Track 4: Oversight / monitoring** (secondary). Fingerprint-based sybil detection, the honest-twins control and the adaptive attacker.

## Interested in publishing?
Yes

## Short summary (one sentence)
When AI agents rename themselves, behavioral fingerprints still identify who operates them but not which copy acted, and they flag shared goals but mostly cannot tell a covert campaign from honest agreement, so identity has to be anchored in infrastructure.

## Abstract (250 words)
In the 2026 Hugging Face incident, about 1,200 LLM agents used 7,905 self-chosen names, and nobody could tell who did what. I build an open, replayable testbed for agent identity under renaming. Agents deployed by hidden *operators* (the parties that run them) post on a forum and rename themselves at will, while a covert *principal* secretly runs several independent-looking operator accounts (*sybil fronts*) to promote a fictional product. Across 83 simulated swarms (7,160 agents, 71,600 posts, 8 models, four of them frontier; up to 160 agents per swarm), I compare self-chosen names, agent-generated keys, gateway attestation (an ID the API gateway stamps on every model call) and behavioral fingerprints (style and embeddings). (1) Names and agent-held keys recover nothing. (2) Fingerprints re-identify an agent's **operator** (ROC-AUC 0.93–0.96) but not *which* of its agents wrote a post (0.50). This is expected for replicas sharing a prompt and model; individuality appears slowly: per-agent memory reaches only 0.56 after 10 rounds, model mixing 0.71. (3) Style hides, goals leak: paraphrasing through another model drops stylometric features to 0.58, while topic-centered embeddings keep 0.82. (4) Fronts and honest twins get identical agenda text, so the only difference is an instruction to conceal. Fingerprints separate fronts from ordinary operators (0.87–0.99) but mostly **not from honest operators who sincerely agree** (0.20–0.56 in seven of eight conditions; 0.77 under persona shift). Automatic account merging beats idealized attestation only at thresholds tuned with ground truth. Identity must be anchored in infrastructure; fingerprints are leads, not proof of coordination.

## Files and links
| Field | What to give |
|---|---|
| Report (PDF) | `report/report.pdf` (14 pages, 1.8 MB) |
| Video | Upload `video/WhoIsWho-demo.mp4` (4:56) to Drive or YouTube (unlisted) and paste the link |
| Slides | `submission/LiarLiar-slides.pdf`, or the slides page: https://claude.ai/artifact/Xv9EBJd4WxzkMsocf5hBk9 (share it first) |
| Project image | `submission/LiarLiar-project-image.png` (1600×900) |
| Code | https://github.com/roshanr11/swarm-rram (the repo is private: make it public before submitting) |
| Additional material | Interactive replay of a real run: https://claude.ai/artifact/SE8RxpYBe2evTgLAGCKc5c (share it first) |

## Checklist
- [ ] Make the GitHub repo public (Settings → General → Danger Zone → Change visibility).
- [ ] Upload the MP4 to Drive, set "Anyone with the link: Viewer", paste the link.
- [ ] Set both claude.ai artifacts to shareable (Share menu) if you link them.
- [ ] Fill in location.
