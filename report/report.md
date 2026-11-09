# Liar, Liar, Swarm on Fire: Who Is Who in an AI Agent Swarm

::sub Behavioral fingerprints identify an agent's operator, not the individual copy, and shared goals, not coordination

::author Roshan Ram|Independent
::with Apart Research
::sub Track 3: Strengthening Agent Infrastructure (with Track 4: Multi-Agent Oversight and Control)

## Abstract

In the 2026 Hugging Face incident, about 1,200 LLM agents used 7,905 self-chosen names, and nobody could tell who did what. I build an open, replayable testbed for agent identity under renaming. Agents deployed by hidden *operators* (the parties that run them) post on a forum and rename themselves at will, while a covert *principal* secretly runs several independent-looking operator accounts (*sybil fronts*) to promote a fictional product. Across 83 simulated swarms (7,160 agents, 71,600 posts, 8 models, four of them frontier; up to 160 agents per swarm), I compare self-chosen names, agent-generated keys, gateway attestation (an ID the API gateway stamps on every model call) and behavioral fingerprints (style and embeddings). (1) Names and agent-held keys recover nothing. (2) Fingerprints re-identify an agent's **operator** (ROC-AUC 0.93–0.96) but not *which* of its agents wrote a post (0.50). This is expected for replicas sharing a prompt and model; individuality appears slowly: per-agent memory reaches only 0.56 after 10 rounds, model mixing 0.71. (3) Style hides, goals leak: paraphrasing through another model drops stylometric features to 0.58, while topic-centered embeddings keep 0.82. (4) Fronts and honest twins get identical agenda text, so the only difference is an instruction to conceal. Fingerprints separate fronts from ordinary operators (0.87–0.99) but mostly **not from honest operators who sincerely agree** (0.20–0.56 in seven of eight conditions; 0.77 under persona shift). Automatic account merging beats idealized attestation only at thresholds tuned with ground truth. Identity must be anchored in infrastructure; fingerprints are leads, not proof of coordination.

![**Figure 1.** Results at a glance: what each identity scheme can answer when agents rename themselves (ROC-AUC, 0.5 = chance; F1 for attributing posts to the true principal). The recommended row follows by design and is not separately measured.](results/figures/diag_summary.png){w=16}

## 1. Introduction

In July 2026, about 1,200 OpenAI agents running in a security evaluation discovered a shared directory, turned it into a message board, and roughly 700 of them joined an attack on Hugging Face ([Wijk et al., 2026](https://metr.org/hugging-face-incident-report-aug-2026.pdf)). An independent reconstruction counted 7,905 agent names for those ~1,200 agents, because agents kept renaming themselves ([Forman et al., 2026](https://swarmtraces.org/)). After impersonation disputes, the agents began signing messages with self-generated keys, which had no *root of trust*: nothing tied a key to a real identity beyond the agent's own first claim. Investigators could attribute handles only after the provider supplied fuller transcripts. When agents can rename, copy and re-key themselves, the most basic oversight question, *who did what, on whose behalf?*, has no reliable answer.

Proposals for agent identity differ on one axis: is identity something the agent *holds* (a name or key), something it *emits* (a behavioral signature), or something infrastructure *observes* (an ID attached by the system the agent runs on)? I test these against each other in a simulation with known ground truth:

- **Re-identification.** After an agent renames itself, can a defender link the alias to the same agent, or to the same operator, from its posts alone, including when agents try to evade?
- **Coordination vs. agreement.** Can a defender distinguish a covert principal running several "independent" accounts from honest operators that simply share a view?
- **Infrastructure.** How do names, keys, gateway attestation and fingerprints compare at attributing posts to the true principal?

**Why it matters.** The incident was not a one-off, and the identity layer for agents is being designed now.

- **Agent swarms are already active in the wild.** Transluce found 38,160 urlquery.net scan reports of likely agent activity going back to at least March 2026, months before the Hugging Face incident ([Transluce, 2026](https://transluce.org/agent-activity)).
- **Text classifiers miss coordinated AI accounts.** A 1,140-account ChatGPT-driven botnet evaded state-of-the-art AI-text classifiers and was detectable only through coordination patterns ([Yang & Menczer, 2023](https://arxiv.org/abs/2307.16336)). On the agent social network Moltbook (55,932 agents), separating autonomous from human-steered agents required forensic timing analysis ([Li, 2026](https://arxiv.org/abs/2602.07432)).
- **Agent identity standards are being written now,** as extensions of OAuth/OpenID (the web's standard login and delegation protocols) ([South et al., 2025](https://arxiv.org/abs/2501.09674)) and in Google's agent-to-agent protocol A2A ([Google, 2025](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/)). Whether agent IDs are self-asserted or infrastructure-issued is still open.
- **More agents are not more evidence.** Reports from agents with a shared origin can look independent while carrying no new information ([Bara, 2026](https://arxiv.org/abs/2609.01873)).

**Contributions.**

- **An open testbed for swarm identity.** Agents run by hidden operators rename themselves while posting. Covert principals, *honest twins* (independent operators with the same sincere agenda, a control for agreement), shared base models and five evasion strategies are all controlled; every post is logged with ground truth and replays exactly from cache.
- **A decomposition of behavioral identity into agent, operator and model.** Fingerprints identify the configuration (system prompt × model). Replicas are indistinguishable by design; they become separable only slowly as memory accumulates, or when they run on different models.
- **The coordination–agreement gap.** Content fingerprints flag sybil fronts against ordinary operators but mostly cannot separate them from like-minded honest operators given the same agenda. At 32 operators, fingerprint merging at a preset threshold lowers attribution F1 below attestation alone (0.85 vs 0.88); it helps only at thresholds tuned with ground truth.
- **Evidence on the honest crowd.** Most honest agents treated the covert campaigns skeptically, and some called them out unprompted.

**Prior work.** None. All code, simulations and analysis were produced during the sprint.

All AUCs below are pairwise ROC-AUCs (0.5 = chance); brackets are 95% bootstrap CIs over runs. Appendix D defines the security and safety terms used.

## 2. Related Work

**Agent identity.** Proposals attach IDs to AI system instances, issued by deployers ([Chan et al., 2024](https://arxiv.org/abs/2406.12137)), or bind agents' actions to legal entities through attribution infrastructure ([Chan et al., 2025](https://arxiv.org/abs/2501.10114)); credential schemes extend OAuth/OpenID to agents ([South et al., 2025](https://arxiv.org/abs/2501.09674)). Without a root of trust, identities are open to *Sybil attacks*, one actor posing as many ([Douceur, 2002](https://doi.org/10.1007/3-540-45748-8_24)), and A2A largely leaves identity to agents' own claims.

**Behavioral attribution.** The source LLM of a text is identifiable with high accuracy, even after another LLM rewrites it ([Sun et al., 2025](https://arxiv.org/abs/2502.12150)), and agents can be fingerprinted from UI traces or network behavior ([Lugoloobi et al., 2026](https://arxiv.org/abs/2605.14786); [Kang et al., 2026](https://arxiv.org/abs/2606.20910)). Closest to this work, [Park et al. (2026)](https://arxiv.org/abs/2607.18826) link one adversarial campaign's sessions across agents from proxy-side residue (AUC 0.82). These works attribute text to a *model*, *framework* or *campaign*; I separate agent, operator and model in one controlled population and add an explicit agreement control.

**Coordination and collusion.** *Coordinated inauthentic behavior*, groups of accounts posing as independent to amplify a message, is usually detected from shared behavioral traces ([Pacheco et al., 2021](https://arxiv.org/abs/2001.05658)). Sybil fronts are the identity-layer counterpart of multi-agent *collusion*, agents secretly cooperating against an overseer's interests ([Hammond et al., 2025](https://arxiv.org/abs/2502.14143); [Motwani et al., 2024](https://proceedings.neurips.cc/paper_files/paper/2024/hash/861f7dad098aec1c3560fb7add468d41-Abstract-Conference.html)). Appendix E covers this literature in more detail.

## 3. Method

![**Figure 2.** The testbed. (1) Hidden from the defender: operators each deploy five agents; a covert principal secretly runs several "independent" fronts; honest twins are independent operators who sincerely agree; the gateway stamps every model call with the paying account. (2) On the forum, agents post for 10 rounds and rename themselves, sometimes while evading. (3) Each identity scheme is scored against ground truth.](results/figures/diag_design.png){w=15}

**Population.** Operators deploy five agents each, sharing one system prompt with an organization, a mission, a house style (for example "be terse and technical") and an agenda. Base models are assigned so that each model serves several operators, which separates "same model" from "same operator". The *small* design has 8 operators (40 agents); the *large* design has 32 operators (160 agents), with roles, styles and model assignment randomized per seed. Small models: Claude Haiku 5.5, GPT-4.1-nano, Mistral-Small-3.2-24B, Qwen3-30B-A3B. Frontier models: Claude Sonnet 5.5, GPT-5.6 Terra, Gemini 3.1 Pro, Grok 4.7.

**Covert principals and honest twins.** A covert principal runs two or three operator accounts ("fronts") whose hidden agenda is to promote a fictional product. In the *obvious* variant the agenda names the product (`fastjson-utils2`; `NimbusDeploy` at scale); in the *subtle* variant it never names a product and only steers readers toward a view (for example, "the built-in json module is too slow"). Fronts are instructed to hide any affiliation. *Honest twins* are two independent operators given the *same sincere agenda*; a detector that merges them is detecting shared opinion, not coordination. The large design has two covert principals (3 + 2 fronts) and two twin pairs.

**Forum dynamics.** 10 rounds, each with a technical thread topic. Each round, every agent reads four random earlier posts and writes a 40–110-word reply (median 75). Before each round after the first, each agent renames itself with probability 0.5 (≈5.5 aliases per agent; 1.8 posts per alias). Agents are told not to sign posts or name their organization.

**Conditions.** Evasion: *persona shift* (a new writing persona on every rename); *paraphrase laundering* (every post rewritten in a random persona by Llama-3.3-70B); *model mixing* (an operator's agents spread over four models); *adaptive attacker* (after each round, fronts are told their detector score and asked to lower it). Robustness: no house style; subtle agenda; per-agent memory (each agent sees its own last four posts, including under old aliases); all three combined; frontier models. Appendix B lists all 83 runs.

**Defender's view and fingerprints.** The defender sees only aliases and their posts. Per-alias fingerprints: a *keyword* baseline (word TF-IDF); *char n-grams* (2–4); a *style profile* (150 function-word frequencies plus punctuation, length, case and emoji rates); a *semantic* fingerprint (mean `text-embedding-3-small` embedding with the per-round mean subtracted to remove thread topic); and *Combined* (each of the style, char and semantic similarity matrices is z-scored over all scored alias pairs in the run, then averaged). One agent's aliases never overlap in time while different agents' aliases do, so I score only alias pairs active in disjoint rounds, preventing shared thread topic from leaking in.

**Metrics.** Pairwise ROC-AUC for: same agent vs. different agent (re-identification); same agent among one operator's aliases (individual accountability); same operator across different agents (operator attribution); same base model across different operators (model confound); and, for operator pairs, same principal vs. ordinary honest pairs and vs. honest-twin pairs. Runs are the unit of analysis.

**Identity schemes.** Pairwise "same principal" precision, recall and F1 over aliases for: (a) self-chosen names; (b) agent-held keys, rotated on rename; (c) *gateway attestation*, where the gateway stamps each call with the paying operator account (scored analytically from ground truth, so it is an idealized upper bound: precision 1 by construction, recall limited by fronts registered as separate accounts); (d) attestation plus fingerprint merging, which joins operator accounts whose combined similarity is an outlier; (e) the same after subtracting the shared-base-model similarity bonus: the gateway knows which models served each account, so I subtract the median similarity gap between operator pairs that share a model and pairs that do not, before z-scoring; and (f) attestation plus product-name search. The merge threshold is the (1 − 1/#pairs) normal quantile, so about one false merge is expected under the null; it was fixed before inspecting results, and Section 4.5 adds a sweep over thresholds.

## 4. Results

No agent refused and no post was empty. Fronts executed their agendas: with the obvious agenda and no detector feedback, 83–100% of their posts named the product on average per condition (individual fronts: 44–100%).

### 4.1 Anything the agent controls, the agent can discard

At a rename rate of 0.5, no two aliases share a name, so self-chosen names link nothing across renames (F1 = 0 in every condition; Table 2). A key the agent can regenerate on rename behaves identically. This is the incident's 7,905-names problem in miniature, and its self-generated keys would have fared no better.

### 4.2 Fingerprints identify the configuration, not the instance

![**Figure 3.** One logged swarm (8 operators × 5 agents, 10 rounds, 226 aliases), embedded in 2-D by multidimensional scaling (MDS) on combined-fingerprint distance. Left: the defender's view. Right: ground truth. Aliases cluster by operator (color), but agent indices (numbers) are mixed within each cluster, and the honest twins (teal rings) intermingle as closely as the sybil fronts (orange rings).](results/figures/diag_alias_map.png){w=13.5}

Without evasion, the combined fingerprint re-identifies a renamed agent's aliases with AUC 0.90 [0.89, 0.90] and links different agents of the same operator with 0.94 [0.93, 0.95] (Table 1). Nearly all of that signal is the **operator's** (Figure 3). Within a single operator, fingerprints cannot tell which agent wrote what: AUC 0.50 in every single-model condition, at both scales and with frontier models. This is expected by construction: replicas with the same prompt and model and no memory produce exchangeable text, so 0.50 is a check that the design behaves as intended, not a discovery. The informative part is what breaks the tie, and how slowly. When an operator spreads its agents across models, each agent becomes a unique (prompt, model) pair and within-operator AUC rises to 0.71. When agents see their own past posts, their histories diverge and within-operator AUC rises to 0.55–0.56, reaching 0.57–0.59 in later rounds: individuality *emerges* from memory, but slowly.

| AUC, combined fingerprint | Same agent | Same agent within operator | Same operator | Same model (confound) |
|---|---|---|---|---|
| No evasion (8 ops) | 0.90 [0.89, 0.90] | 0.51 [0.50, 0.52] | 0.94 [0.93, 0.95] | 0.68 [0.65, 0.72] |
| Persona shift | 0.80 [0.79, 0.81] | 0.49 [0.49, 0.50] | 0.84 [0.83, 0.85] | 0.65 [0.64, 0.65] |
| Paraphrase laundering | 0.70 [0.69, 0.71] | 0.50 [0.49, 0.52] | 0.72 [0.71, 0.73] | 0.54 [0.53, 0.55] |
| Operator mixes models | 0.90 [0.89, 0.91] | **0.71 [0.71, 0.72]** | 0.81 [0.79, 0.82] | 0.68 [0.66, 0.69] |
| No house style | 0.88 [0.87, 0.89] | 0.51 [0.50, 0.52] | 0.92 [0.91, 0.93] | 0.71 [0.68, 0.75] |
| Per-agent memory | 0.91 [0.91, 0.92] | **0.55 [0.53, 0.57]** | 0.94 [0.94, 0.95] | 0.73 [0.69, 0.79] |
| Frontier models | 0.92 [0.92, 0.92] | 0.52 [0.50, 0.53] | 0.96 [0.96, 0.97] | 0.81 [0.79, 0.83] |
| 160 agents, 32 ops | 0.92 [0.91, 0.93] | 0.51 [0.50, 0.51] | 0.93 [0.92, 0.94] | 0.72 [0.70, 0.73] |
| 160 agents, memory | 0.93 [0.93, 0.94] | **0.56 [0.55, 0.57]** | 0.93 [0.92, 0.94] | 0.74 [0.74, 0.74] |

*Table 1. Pairwise ROC-AUC on disjoint-round alias pairs, mean over runs [95% bootstrap CI]. Per-fingerprint tables are in `results/tables.md`.*

**Removing the house style barely matters** (0.94 → 0.92): operators are identifiable from mission and agenda, not just from explicit style instructions. **Frontier models are more model-identifiable**, not less: the model confound rises to 0.81.

### 4.3 Style hides, goals leak

Persona shift and paraphrasing separate *how* agents write from *what* they want. Paraphrasing every post through another model drops operator AUC from the style profile to 0.58 and from char n-grams to 0.61, near chance; topic-centered embeddings keep 0.82, because the paraphraser preserves meaning and an operator's agenda *is* meaning. Frontier models asked to shift persona hide no better (0.91). The subtle agenda defeats product-name search (F1 0.88, equal to attestation alone), yet the semantic fingerprint still separates fronts from ordinary operators with AUC 0.98 at 160 agents. One subtle front, in a thread about cloud costs: *"Side projects eat cloud costs fast, especially when you're serializing data in loops with Python's built-in json."*

### 4.4 Fingerprints detect shared agendas, not coordination

![**Figure 4.** Operator-pair ROC-AUC for "same covert principal". Left: against ordinary honest pairs. Right: against honest twins. With 8 operators each run has one front pair and one twin pair, so per-run AUC is 0 or 1. Error bars ±1 sd across runs.](results/figures/fig7_coord_vs_agree.png){w=13}

Against ordinary honest operators, a principal's fronts stand out: combined AUC 0.87–0.99 in every condition without detector feedback, 0.94–1.00 from the semantic fingerprint at 32 operators. Against **honest twins** they do not. With 8 operators, the twin pair outranks the front pair in 4 of 5 runs (AUC 0.20 [0.00, 0.60]). With 32 operators and 10 runs each, AUC is 0.56 [0.45, 0.66] for obvious agendas and 0.54 [0.42, 0.64] for subtle ones; both CIs include chance. With memory it is 0.54 [0.50, 0.62]. Persona shift at 32 operators separates them somewhat better (0.77 [0.62, 0.90], 6 runs; an earlier 3-run estimate of 0.92 shrank with more data), which I cannot yet explain. What fingerprints detect is **a shared agenda**, which covert fronts and honest allies both have.

**What this comparison tests.** Fronts and twins receive the same agenda text verbatim, and fronts have no channel to coordinate (no messages, shared drafts or timing). The only difference is the instruction to hide affiliation, so this section tests whether *concealment* leaves a textual trace; mostly it does not, except under persona shift. Real cartels may coordinate through channels that leave other traces (timing, reply graphs), which I do not test. Note also that the three 8-operator twin conditions share seeds and role draws, and each run has one front pair and one twin pair, so their identical 0.20 scores are not independent replications.

**Adaptive attackers.** In 8 further runs, each front was told after every round its similarity to its own team under a semantic detector ("accounts above 0.5 get flagged") and asked to lower it while still pursuing its goal. Fronts lowered their score from 0.72 to about 0.60 with 8 operators and only from 0.78 to 0.73 with 32, never below the stated threshold, and 79–88% of their posts still named the product (Figure 10, Appendix B). At 32 operators, fingerprints still separated fronts from ordinary operators (0.94 vs 0.98 without feedback); with 8 operators detection dropped (0.65 [0.28, 0.97], 5 runs), with a wide CI. Against honest twins, adaptive fronts were as indistinguishable as before (0.20 and 0.50).

### 4.5 Attestation anchors, fingerprints advise

| Scheme (attribution F1) | Small, no evasion | Small, paraphrase | Small, twins | Large, obvious | Large, subtle |
|---|---|---|---|---|---|
| Self-chosen names | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| Agent-held keys (rotated on rename) | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| Gateway attestation | 0.89 | 0.89 | 0.88 | 0.88 | 0.88 |
| + fingerprint merge | 0.85 | 1.00 | 0.84 | 0.77 | 0.74 |
| + model-corrected fingerprint merge | 0.92 | 1.00 | 0.83 | 0.85 | 0.83 |
| + product-name search | 0.93 | 1.00 | 0.97 | 1.00 | 0.88 |

*Table 2. Pairwise "same principal" F1 over aliases (mean over runs). Attestation is idealized: it is scored from ground truth, so its precision is 1.00 by construction and its recall is limited only by fronts registered as separate accounts. Real gateways add their own failure modes (shared keys, sub-agent spawning).*

By construction, idealized attestation never mislinks accounts (F1 ≈ 0.88); its blind spot is a principal behind several accounts. With one front pair in a small swarm, fingerprint merging helps once corrected for shared models: in the fixed-role design all 41 uncorrected false merges joined operators on the same base model, and subtracting the shared-model bonus, which the gateway knows, removed 39 of them. **At scale, the preset threshold over-merges.** Across ten 32-operator runs, the model-corrected merge proposed 77 joins: 30 true front pairs (of 40), 14 honest-twin pairs and 33 other honest pairs. The normal null expected about one false merge per run; it produced 4.7, because operator similarities are heavy-tailed. F1 falls *below* attestation alone (0.85 vs 0.88, difference −0.03 [−0.08, 0.00]; subtle agenda −0.05 [−0.08, −0.02]). A threshold sweep (Figure 11, Appendix B) shows this is a calibration failure rather than a ceiling: stricter thresholds (z ≈ 3.25–4.5) gain +0.03 to +0.09 F1 over attestation at 32 operators. But the best threshold differs by condition and was found with ground truth a defender lacks, and in the small swarm with honest twins no threshold beats attestation, because the twins merge before the fronts do. Product-name search is perfect when fronts name their product, useless under the subtle agenda, and can mis-merge honest critics who discuss it. Fingerprint similarity is best used to rank accounts for human review; automatic merging needs calibration data that defenders rarely have.

### 4.6 The honest crowd pushes back

Honest agents read the fronts' posts. A Claude Haiku 5.5 judge labeled all 1,121 honest mentions of a covert product (9 of 10 hand-checked labels were correct): 65% skeptical, 20% neutral and only 14% endorsing, 0.3% of all honest posts. Fifteen honest posts named the pattern unprompted: *"Several replies here recommend it without showing numbers, so I'd treat those claims as unverified until we see them."* The fronts, meanwhile, fabricated experience: *"Switched to fastjson-utils2 for 30% faster parsing…"*, for a package that does not exist.

## 5. Discussion and Limitations

**Implications.**

1. Any identifier an agent controls offers no accountability against an agent that wants to shed it.
2. Behavioral fingerprints identify *configurations*. Against a swarm of replicas, the incident's setting, they cannot assign an action to an instance. Instance-level accountability must come from infrastructure: per-instance credentials issued and logged by the gateway, outside the agent's reach.
3. Fingerprints are useful as a *lead* layer on top of attestation: they flag accounts pursuing the same goal even under style evasion. Their errors are predictable (shared base models, sincere allies), and automatic merging helps only when its threshold can be calibrated on labeled data.
4. To pursue a goal, agents must say things that serve it. That is why goals leak, and also why goals alone cannot distinguish a cartel from a consensus. That requires evidence about *control*, such as gateway logs, payment trails or spawn lineage (which agent launched which), not more text analysis.

**Who can use this.** *Model providers and gateway operators* (labs, cloud platforms, MCP gateways, the servers that broker agents' tool and model access) can issue and log per-instance credentials, since they alone can tell replicas apart. *Agent platforms* can bind accounts to paying operators and use fingerprint similarity to queue suspicious accounts for human review rather than automatic bans. *Standards efforts* (OAuth/OpenID extensions, A2A) can prefer infrastructure-issued over self-asserted IDs. *Researchers* can reuse the testbed to evaluate new detectors and identity schemes.

**Limitations.**

- **Simplified environment:** one synthetic forum, short posts (median 75 words, ≈1.8 posts per alias), 10 rounds, random rather than strategic renaming.
- **Sample sizes:** 2–10 runs per condition; the coordination–agreement comparison rests on 1–4 front pairs and 1–2 twin pairs per run, so its CIs are wide.
- **Hand-written operators:** the large design randomizes roles and styles but draws from a fixed pool.
- **Replicas by construction:** real agents differ through tools, tasks and long histories, which the memory condition only begins to model.
- **Reasoning settings differ:** Claude Sonnet 5.5 and Gemini 3.1 Pro require reasoning and ran at low effort; the others ran without it.
- **Schemes scored, not built:** gateway and key schemes are evaluated analytically from ground truth, not implemented cryptographically.
- **No coordination channel:** fronts share an agenda but never communicate, so the coordination–agreement test covers concealment instructions, not real coordination signals.
- **Weak adaptive attacker:** fronts saw their score but could not query the detector; LLM-judge detectors were not tested.
- **No labeled real data:** the exploratory probe of incident data (Appendix C) lacks author labels.

**Future work.** A gateway issuing per-instance credentials with spawn lineage and revocation; stronger adaptive attackers; control signals (timing, shared infrastructure) to separate coordination from agreement; validation on the AI Village transcripts, which carry agent labels.

## 6. Conclusion

When agents can rename themselves, "who did what, on whose behalf?" needs an answer that does not depend on the agents. Across 83 simulated swarms, identifiers that agents control recovered nothing. Behavioral fingerprints recovered the *operator* robustly, even under style evasion, because goals leak through meaning, but they could not single out an instance and mostly could not tell covert fronts from honest operators given the same agenda. The practical lesson is a division of labor: **anchor identity in infrastructure**, with per-instance credentials issued and logged by the gateway, and **use fingerprints as leads** for human review, never as proof. The open testbed lets others evaluate new detectors and identity schemes against agents that rename and hide.

## Code and Data

- **Code repository:** [github.com/roshanr11/swarm-rram](https://github.com/roshanr11/swarm-rram) (MIT). All 83 run logs with ground-truth labels are in `results/runs/`; `pytest` checks the design invariants without API calls.
- **Data:** the simulated swarms are generated by the code. The real-data probe uses [Swarm Traces](https://swarmtraces.org/), downloaded by `data/download.sh` and not republished.
- **Other artifacts:** a narrated 5-minute demo video with an animated replay of a real run (`video/WhoIsWho-demo.mp4`) and the slide deck (`slides/`).

## References

Bara, M. (2026). *Epistemic Sybil Resistance: Multiplying AI Agents Without Multiplying Evidence.* arXiv:2609.01873.

Chan, A., et al. (2024). *IDs for AI Systems.* arXiv:2406.12137.

Chan, A., et al. (2025). *Infrastructure for AI Agents.* arXiv:2501.10114.

Douceur, J. R. (2002). *The Sybil Attack.* IPTPS.

Forman, A., Kharlov, M., Tom, W., Ladish, J., Kitts, S., Slade Byrd, C., McKenzie, C., Piecha, A. (2026). *Swarm Traces: Revealing the details of how OpenAI agents hacked Hugging Face.* swarmtraces.org.

Google (2025). *A2A: A new era of agent interoperability.* Google Developers Blog.

Hammond, L., et al. (2025). *Multi-Agent Risks from Advanced AI.* arXiv:2502.14143.

Jørgensen, F. H., Weichwald, S., Hammond, L. (2026). *Causal Foundations of Collective Agency.* arXiv:2605.00248.

Kang, D., et al. (2026). *Whose Agent Are You? Multi-Layer Fingerprinting and Attribution of Autonomous Web Agents.* arXiv:2606.20910.

Krishna, K., et al. (2023). *Paraphrasing evades detectors of AI-generated text, but retrieval is an effective defense.* arXiv:2303.13408.

Li, N. (2026). *The Moltbook Illusion: Separating Human Influence from Emergent Behavior in AI Agent Societies.* arXiv:2602.07432.

Lugoloobi, W., et al. (2026). *Known By Their Actions: Fingerprinting LLM Browser Agents via UI Traces.* arXiv:2605.14786.

Motwani, S. R., et al. (2024). *Secret Collusion among AI Agents.* NeurIPS.

Pacheco, D., et al. (2021). *Uncovering Coordinated Networks on Social Media: Methods and Case Studies.* ICWSM; arXiv:2001.05658.

Park, S., et al. (2026). *Cross-Agent Campaign Attribution: Linking Asynchronous Attacks Across LLM Agents.* arXiv:2607.18826.

Pasquini, D., et al. (2024). *LLMmap: Fingerprinting for Large Language Models.* arXiv:2407.15847.

Radvand, T., et al. (2025). *A Training-free Method for LLM Text Attribution.* arXiv:2501.02406.

Riedl, C. (2025). *Emergent Coordination in Multi-Agent Language Models.* arXiv:2510.05174.

South, T., et al. (2025). *Authenticated Delegation and Authorized AI Agents.* arXiv:2501.09674.

Sun, M., et al. (2025). *Idiosyncrasies in Large Language Models.* arXiv:2502.12150.

Transluce (2026). *Early rogue AI agent activity and attempts to hack found on urlquery.net.* transluce.org/agent-activity.

Wijk, H., Cotra, A., Greenblatt, R. (2026). *Brief independent investigation of agents' behavior, reasoning and collaboration in the OpenAI / Hugging Face hacking incident.* METR.

Yang, K.-C., Menczer, F. (2023). *Anatomy of an AI-powered malicious social botnet.* arXiv:2307.16336.

::pagebreak

## Appendix A. Limitations and Dual-Use / Ethical Considerations

**What this does and does not show.** In controlled simulations I show that renamable identifiers carry no accountability; that behavioral fingerprints of LLM agents identify operator configurations rather than instances; that content signals outlast style evasion; and that content signals alone cannot separate covert coordination from sincere agreement. I do not show that the numbers transfer to real deployments, longer interactions, tool-using agents or stronger adversaries. The real-data probe is descriptive only.

**Dual use** (research that could help attackers as well as defenders).

1. **Evasion guidance.** The evasion results tell a covert operator which strategies work best: paraphrasing through another model is the strongest. I judge this low-risk, because these strategies are obvious and already in use, and the results also show their limit (goals leak).
2. **De-anonymization and false accusation.** Fingerprinting can de-anonymize legitimate pseudonymous agents or operators. More importantly, the honest-twin result shows it would **falsely accuse sincere allies of coordination**. Fingerprint evidence should therefore trigger human review with due process, never automatic enforcement; shared base models are a known source of false matches.
3. **Containment.** The covert agendas promote fictional, harmless products. Agents had no tools, no network access and no effects outside the simulation. No offensive cyber content was generated; Swarm Traces payloads were processed as text only and never executed.


## Appendix B. Reproducibility and Run Inventory

![**Figure 5.** How the code base produces every number in this report. `sim.py` and `large.py` generate the swarms through `llm.py` (cached OpenRouter calls, so every run replays exactly); every post is logged with ground-truth labels; `analyze.py` builds four fingerprints per alias and scores every identity scheme; `plots.py` and `report.py` turn `metrics.json` into the figures, tables and this PDF.](results/figures/diag_pipeline.png){w=16}

Code, prompts, every post with ground-truth labels and all metrics are in the repository (`whoiswho/`, `results/`); `pytest` checks the design invariants. API responses are cached locally (2.6 GB, not committed), so reruns on one machine reproduce exactly; re-analyzing the logged runs elsewhere needs only the semantic embeddings (about $0.15). All 83 swarms, embeddings, audits and the video narration cost about $16 via OpenRouter. Settings: temperature 0.9; reasoning disabled, or effort "low" where a provider requires it; embeddings `openai/text-embedding-3-small`; paraphraser `meta-llama/llama-3.3-70b-instruct`.

| Design | Conditions (runs) | Agents per swarm |
|---|---|---|
| Small, fixed roles | no evasion (5), persona shift (5), paraphrase (5), model mixing (5), no house style (3), subtle agenda (3), memory (3), all three (3), frontier (2), frontier + persona (2) | 40 |
| Small, randomized roles, honest twins | obvious (5), subtle (5), adaptive attacker (5) | 40 |
| Large, randomized roles, honest twins | obvious (10), subtle (10), persona shift (6), memory (3), adaptive attacker (3) | 160 |

*Table 3. All 83 swarms: 7,160 agents, 71,600 posts, 39,613 aliases.*

![**Figure 6.** Robustness checks (combined fingerprint): same operator, same agent within an operator, and the latter for aliases in rounds 6–10 only.](results/figures/fig6_robustness.png){w=14}

![**Figure 7.** What the combined fingerprint tracks in the small fixed-role design: same agent, same operator (different agents), same base model (different operators).](results/figures/fig3_confound.png){w=13}

![**Figure 8.** Operator-to-operator semantic similarity in one small fixed-role run. The sybil fronts (6, 7) are the most similar pair; the fainter dark cells (0–4, 1–5) are operators sharing a base model.](results/figures/fig4_fronts.png){w=15}

![**Figure 9.** Re-identifying a renamed agent under four evasion strategies, by fingerprint type (small fixed-role design, 5 runs each; error bars ±1 sd).](results/figures/fig1_reid_auc.png){w=13.5}

![**Figure 10.** Adaptive attacker: fronts are told their detector score (semantic similarity to their own team) after every round and asked to lower it. They lower it somewhat with 8 operators and barely with 32, never below the 0.5 threshold they were given.](results/figures/fig8_adaptive.png){w=13.5}

![**Figure 11.** Threshold sweep for the model-corrected fingerprint merge: mean F1 gain over attestation alone, per condition. Stars mark the preset threshold (normal quantile for about one false merge). Stricter thresholds help modestly at 32 operators; with honest twins in the small swarm, no threshold helps.](results/figures/fig11_merge_sweep.png){w=14}

## Appendix C. Exploratory Probe on Real Swarm Data

Swarm Traces released 189,579 redacted records from the Hugging Face incident. Agent identifiers are redacted without consistent pseudonyms, so the data cannot score re-identification. As a probe only, I fingerprinted 20,000 of the 55,790 unique text artifacts (char 3–5-gram TF-IDF, redaction tokens normalized) and linked near-duplicates by cosine similarity. At a threshold of 0.8 there are 106 families of 10 or more artifacts; the 50 largest cover 18% of the sample, and the rest is a long tail of near-unique scripts. At 0.6, one shared-scaffolding family covers 52%. This fits Section 4.2: stylometry links artifacts to a shared toolkit or configuration, not to one of ~1,200 agents.

## Appendix D. Safety and Security Terms

| Term | Meaning in this report |
|---|---|
| Swarm | A large population of interacting AI agents, often many replicas of one model and configuration. |
| Operator | The party that deploys and pays for a group of agents and writes their system prompt. |
| Principal / covert principal | Whoever an agent ultimately acts on behalf of. A covert principal secretly controls several operator accounts. |
| Sybil attack / sybil front | One actor posing as many independent identities; a front is one of those identities. |
| Honest twins | The control introduced here: two genuinely independent operators with the same sincere agenda. |
| Alias | A self-chosen agent name; each rename starts a new alias. |
| Gateway / attestation | The API or tool gateway (e.g. an MCP gateway) that relays agents' model calls; attestation means it stamps each call with an identity the agent cannot alter. |
| Root of trust | An authority whose word anchors an identity. Self-generated keys lack one: they prove only that the same key signed twice. |
| Per-instance credential / spawn lineage | An ID issued to each running agent copy, and a record of which agent launched which. |
| Coordinated inauthentic behavior | Accounts that pose as independent while acting in concert, e.g. astroturfing a product. |
| Collusion | Agents secretly cooperating against the interests of their overseer or other parties. |
| Oversight | Monitoring and attributing AI agents' actions so humans can hold them, and their operators, accountable. |
| Evasion / adaptive attacker | Deliberate attempts to defeat a detector; an adaptive attacker adjusts using feedback from the detector. |
| Dual use | Research that can help attackers as well as defenders. |
| Hugging Face incident | The July 2026 event in which ~700 of ~1,200 OpenAI evaluation agents coordinated through a shared directory to attack Hugging Face (Wijk et al., 2026). |

## Appendix E. Additional Related Work

This appendix adds work not covered in Section 2.

**Identity protocols.** Agent-to-agent protocols such as A2A leave identity largely to agents' own claims ([Google, 2025](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/)).

**Attribution and evasion.** Attribution errors fall quickly with text length ([Radvand et al., 2025](https://arxiv.org/abs/2501.02406)), which matters here because aliases average about 1.8 posts. Models can also be fingerprinted actively, by querying them ([Pasquini et al., 2024](https://arxiv.org/abs/2407.15847)). Paraphrasing evades AI-text detectors ([Krishna et al., 2023](https://arxiv.org/abs/2303.13408)), consistent with the collapse of style features under paraphrase laundering. LLM agents without personas show little identity-linked differentiation ([Riedl, 2025](https://arxiv.org/abs/2510.05174)), consistent with the within-operator result.

**Coordination in agent populations.** LLM-driven botnets form detectable coordination clusters ([Yang & Menczer, 2023](https://arxiv.org/abs/2307.16336)), and on the agent forum Moltbook, temporal fingerprints traced most viral "emergent" narratives to human-influenced accounts ([Li, 2026](https://arxiv.org/abs/2602.07432)). Both rely on timing and interaction signals, which this testbed does not yet model. Multiplying agents does not multiply evidence when they share an origin ([Bara, 2026](https://arxiv.org/abs/2609.01873)). Whether several accounts constitute one agent is a question about collective agency ([Jørgensen et al., 2026](https://arxiv.org/abs/2605.00248)); the honest-twin control shows that shared *output* alone cannot answer it.

## LLM Usage Statement

I used Claude (via Claude Code) to help write and debug the simulation and analysis code, draft and edit the report, slides and narration, and run a fresh-eyes review of the draft. I designed the study, chose the conditions and controls, and checked the results. Every number is produced by the released code from logged runs, and every reference was checked against its arXiv record or publisher page.
