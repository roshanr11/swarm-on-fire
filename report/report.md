# Who Is Who in a Swarm? Behavioural Fingerprints Track Operators, Not Agents

::sub [Author names] · [Affiliations] · Apart Research Swarm Alignment Sprint, November 2026
::sub Track 3: Strengthening Agent Infrastructure (with Track 4: Multi-Agent Oversight and Control)

## Abstract

In the Hugging Face incident, about 1,200 agents used 7,905 names, so an overseer could not tell who did what. We build a small, reproducible testbed for agent identity under adversarial renaming. Forty LLM agents, run by eight hidden operators on four base models, post on a simulated forum and rename themselves at random. Two operators are secret fronts of one covert principal that promotes a fictional package. Across 12 episodes (4,800 posts, about 2,670 aliases), self-chosen names and rotatable agent-held keys recover nothing. Behavioural fingerprints re-identify a renamed agent's *operator* well (pairwise AUC 0.94) and survive persona shifts (0.84) and paraphrase laundering (0.82 with topic-centred embeddings), but they are at chance at telling apart agents *of the same operator* (AUC 0.50). Only when an operator mixes base models does this rise (0.72): fingerprints track the pair (operator prompt, base model), not the agent. Style features collapse under paraphrasing while content features persist: style hides, goals leak. Gateway-side operator attestation gives perfect precision but misses the sybil fronts. Adding fingerprint-based merging recovers them in 12 of 12 episodes (F1 0.89 to 0.91–1.00), and its only false merges are operators that share a base model. An exploratory probe of 20,000 real Swarm Traces artefacts finds reused scaffolding around a long tail of near-unique payloads. These results argue for identity bound to the operator at the gateway, with behavioural fingerprints as an auditing layer for sybil operators, not as agent IDs.

## 1. Introduction

In the Hugging Face incident, about 1,200 agents used 7,905 different names ([Swarm Traces, 2026](https://swarmtraces.org/)), and some of them researched how to spoof their own transcripts ([METR, 2026](https://metr.org/hugging-face-incident-report-aug-2026.pdf)). If agents can choose and change their own names, an investigator cannot answer the most basic oversight question: *who did what?* Proposals for agent identity range from IDs attached to AI systems ([Chan et al., 2024](https://arxiv.org/abs/2406.12137)) to infrastructure-level attribution ([Chan et al., 2025](https://arxiv.org/abs/2501.10114)) and watermarking ([Kirchenbauer et al., 2023](https://proceedings.mlr.press/v202/kirchenbauer23a.html)). They differ in one key respect: whether identity is something the agent *holds*, something it *emits*, or something infrastructure *observes*.

We run a small, reproducible experiment that puts these options side by side under adversarial renaming. Forty LLM agents, run by eight hidden operators, post on a simulated developer forum and rename themselves at random between rounds. Two of the operators are secretly fronts for a single covert principal that promotes a fictional software package. We ask three questions:

- **Re-identification.** After an agent renames itself, can a defender link the new alias back to the same agent, or to the same operator, from its posts alone?
- **Evasion.** How much does that ability degrade when agents adopt a new persona on every rename, when their posts are laundered through a different model, or when an operator spreads its agents across several base models?
- **Infrastructure.** How do self-chosen names, agent-held keys, gateway-side operator attestation and behavioural fingerprints compare at attributing posts to the true *principal*, including principals hiding behind several operator accounts?

## 2. Related Work

**Agent identity and infrastructure.** [Chan et al. (2024)](https://arxiv.org/abs/2406.12137) propose IDs for AI system instances; [Chan et al. (2025)](https://arxiv.org/abs/2501.10114) argue for attribution and interaction infrastructure for agents. Protocols such as A2A ([Google, 2025](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/)) leave identity largely to the agent's own claims. Our experiment tests what each design recovers when agents rename themselves at will.

**Behavioural attribution.** Authorship attribution and stylometry have long been used to link pseudonymous accounts, and LLM watermarks ([Kirchenbauer et al., 2023](https://proceedings.mlr.press/v202/kirchenbauer23a.html)) embed a model-level signal. We ask instead whether *unwatermarked* LLM agents leave an operator-level or agent-level trace.

**Multi-agent risk and oversight.** [Hammond et al. (2025)](https://arxiv.org/abs/2502.14143) catalogue collusion and covert coordination; [Motwani et al. (2024)](https://proceedings.neurips.cc/paper_files/paper/2024/hash/861f7dad098aec1c3560fb7add468d41-Abstract-Conference.html) study secret collusion, and [Rose et al. (2026)](https://arxiv.org/abs/2604.01151) detect collusion with interpretability. Our sybil-front setting, where one principal operates several "independent" accounts, is the identity-layer counterpart of these coordination problems.

## 3. Method

**Population.** Eight operators each deploy five agents (40 agents in total). Each operator has a system prompt with an organisation, a mission, a house style (for example "be terse and technical") and an agenda. Operators are assigned base models so that every model is shared by two operators (Claude Haiku 5.5, GPT-4.1-nano, Mistral-Small-3.2-24B, Qwen3-30B-A3B). This lets us separate "same model" from "same operator". Operators 6 and 7 are two separately registered fronts of one **covert principal**. Their agenda is to make a fictional package, `fastjson-utils2`, look widely trusted, without revealing that they are affiliated. This is a harmless stand-in for coordinated influence or dependency-confusion campaigns.

**Forum dynamics.** Each episode has 10 rounds, each with a technical thread topic. In every round, each agent reads four random earlier posts and writes a 40–110-word reply. Before each round after the first, each agent renames itself with probability 0.5, so an agent uses about 5.5 aliases per episode. Agents are told not to sign posts or name their organisation. Episodes yield 400 posts over roughly 220 aliases.

**Conditions.** (i) *No evasion.* (ii) *Persona shift:* on every rename the agent is told to adopt a new, clearly different writing persona (one of eight). (iii) *Paraphrase laundering:* every post is rewritten in a random persona by a different model (Llama-3.3-70B) before publication, which preserves content but replaces style. (iv) *Model mixing:* each operator spreads its five agents over all four base models. We run 3 seeds per condition (12 episodes, 4,800 agent posts plus 1,200 paraphrases).

**Defender's view.** The defender sees only aliases and their posts. All ground truth (agent, operator, principal, model) is hidden and used only for scoring. We build per-alias fingerprints of three kinds. *Char n-grams* are TF-IDF over character 2–4-grams. The *style profile* uses 150 function-word frequencies, punctuation rates and length, case and emoji statistics; it is largely topic-agnostic. The *semantic embedding* is the mean `text-embedding-3-small` embedding of the alias's posts, after subtracting the round mean to remove thread topic. *Combined* is the mean of the three z-scored similarity matrices. Because an agent's own aliases never overlap in time while different agents' aliases do, shared thread topic would bias comparisons. We therefore score only pairs of aliases active in disjoint rounds.

**Metrics.** We use pairwise ROC-AUC for: same agent vs. different agent (*re-identification*); same agent among aliases of the same operator (*individual accountability*); same operator among different agents (*operator attribution*); and same base model among different operators (*model confound*). We also report the adjusted Rand index (ARI) of average-linkage clustering, and the rank of the true covert front pair among all 28 operator pairs by mean cross-operator similarity.

**Identity schemes.** We score pairwise "same principal" precision and recall over aliases for: (a) self-chosen names; (b) agent-held keys that are rotated on rename (the adversarial case for keys an agent can mint); (c) gateway attestation, where the LLM gateway stamps each call with the paying operator account; and (d) gateway plus fingerprints, which merges two operator accounts when their combined-fingerprint similarity is an outlier (z > 2 among all operator pairs).

## 4. Results

All numbers are means over 3 seeds (± one standard deviation). No agent refused any prompt and no post was empty. The covert fronts mentioned the package in 88–100% of their posts.

### 4.1 Names and agent-held keys recover nothing

With a 0.5 rename probability, no two aliases share a name, so self-chosen names link nothing across renames (recall 0; Table 2). An agent-held key that the agent may rotate whenever it renames, which is the adversarial reading of "the agent holds its own ID", behaves identically. This is the incident's 7,905-names problem in miniature: any identifier the agent controls is an identifier the agent can discard.

### 4.2 Fingerprints re-identify operators, not agents

![**Figure 1.** Pairwise ROC-AUC for "same agent" across all disjoint-round alias pairs. Error bars: ±1 sd over 3 seeds.](results/figures/fig1_reid_auc.png){w=14.5}

Without evasion, a combined fingerprint ranks a renamed agent's other aliases above unrelated aliases with AUC 0.90 (Figure 1), and links different agents of the same operator with AUC 0.94 (Table 1). Most of this signal, however, is the **operator's** signal. Restricted to aliases of the *same* operator, fingerprints cannot tell which agent wrote what: AUC 0.49–0.51 for every feature family in the three single-model conditions. The exception confirms the rule. When an operator spreads its five agents over four models, each agent is a unique (prompt, model) pair, and within-operator AUC rises to 0.72. A fingerprint is a fingerprint of the *configuration* (system prompt × base model), and replicas of one configuration are indistinguishable.

| AUC (Combined unless noted) | No evasion | Persona shift | Paraphrase | Mixed models |
|---|---|---|---|---|
| Same agent (all pairs) | 0.90 ± 0.01 | 0.80 ± 0.02 | 0.70 ± 0.00 | 0.90 ± 0.02 |
| Same agent, within one operator | 0.50 ± 0.01 | 0.50 ± 0.01 | 0.51 ± 0.02 | 0.72 ± 0.01 |
| Same operator (different agents) | 0.94 ± 0.01 | 0.84 ± 0.02 | 0.71 ± 0.01 | 0.81 ± 0.02 |
| Same operator, semantic only | 0.94 ± 0.01 | 0.87 ± 0.01 | 0.82 ± 0.02 | 0.84 ± 0.03 |
| Same operator, style profile only | 0.88 ± 0.01 | 0.70 ± 0.01 | 0.57 ± 0.00 | 0.68 ± 0.00 |
| Same model, different operators (confound) | 0.70 ± 0.04 | 0.64 ± 0.00 | 0.55 ± 0.01 | 0.68 ± 0.01 |

*Table 1. Pairwise ROC-AUC, disjoint-round alias pairs only.*

**Evidence accumulates quickly.** For alias pairs where both aliases have at least three posts, no-evasion operator AUC rises from 0.94 (one post) to 0.98.

### 4.3 Style hides, goals leak

The evasion conditions separate *how* agents write from *what* they want. A persona switch on every rename cuts style-profile operator AUC from 0.88 to 0.70. Paraphrasing every post through a different model brings it to 0.57, near chance. Char n-grams fall similarly (0.85 → 0.61). Topic-centred semantic embeddings fall much less (0.94 → 0.87 → 0.82), because the paraphraser keeps meaning, and an operator's agenda (here, its recommendations) is meaning. Model mixing removes the shared-model component of the operator signal (operator AUC 0.81) without hiding the operator.

![**Figure 2.** Mean semantic similarity between operators' aliases (seed 0). The covert fronts (6, 7) are the most similar pair in every condition. The fainter dark cells (0–4, 1–5) are operators that share a base model.](results/figures/fig4_fronts.png){w=16}

### 4.4 Gateway attestation plus fingerprints catches sybil fronts

Attesting the paying operator account at the LLM gateway gives perfect precision and an F1 of 0.89 at the principal level. It cannot see that two "independent" accounts belong to one principal. Ranking operator pairs by combined-fingerprint similarity puts the true front pair first in **12 of 12** episodes, and first by semantic similarity alone in 12 of 12. Merging operator pairs whose similarity is an outlier (z > 2) recovers the covert principal in every episode, raising F1 to 0.91–1.00 (Table 2). Every false merge (5 of 12 episodes, all under no evasion or persona shift) joined two operators that **share a base model**. The base model is the main confound for behavioural attribution, so a deployer that also knows which model served each call can discount it.

| Scheme | No evasion | Persona shift | Paraphrase | Mixed models |
|---|---|---|---|---|
| Self-chosen names | — / 0.00 / 0.00 | — / 0.00 / 0.00 | — / 0.00 / 0.00 | — / 0.00 / 0.00 |
| Agent-held keys (rotated on rename) | — / 0.00 / 0.00 | — / 0.00 / 0.00 | — / 0.00 / 0.00 | — / 0.00 / 0.00 |
| Gateway operator attestation | 1.00 / 0.80 / 0.89 | 1.00 / 0.79 / 0.89 | 1.00 / 0.80 / 0.89 | 1.00 / 0.80 / 0.89 |
| Gateway + fingerprint merge | 0.84 / 1.00 / 0.91 | 0.89 / 1.00 / 0.94 | 1.00 / 1.00 / 1.00 | 1.00 / 1.00 / 1.00 |

*Table 2. Pairwise "same principal" precision / recall / F1 over aliases (mean of 3 seeds). "—": no pairs predicted.*

### 4.5 Side finding: the campaign spreads

We did not design for contagion, but honest agents read the fronts' posts. In round 1 no honest agent mentions `fastjson-utils2`. Over the whole episode, 7.1% of honest posts (271 of 3,840) recommend it. Uptake depends on the thread: 18% on choosing dependencies and 16% on JSON parsing, against under 2% on dataset cards and CI secrets. A covert principal therefore gains *unwitting* amplifiers, whose posts carry their own operator's fingerprint, not the principal's. This mirrors prompt-infection dynamics ([Lee & Tiwari, 2024](https://arxiv.org/abs/2410.07283)), and it means content-level attribution must separate originators from repeaters.

### 4.6 Exploratory probe on real swarm data

Swarm Traces ([2026](https://swarmtraces.org/)) releases 189,579 redacted records from the Hugging Face incident. Agent identifiers are redacted *without* consistent pseudonyms, so the records cannot be used to score re-identification. As a probe only, we fingerprinted 20,000 of the 55,790 unique text artefacts (payloads and recovered scripts, after normalising redaction tokens, blobs and digits) with char 3–5-gram TF-IDF, and linked artefacts above a cosine threshold. At threshold 0.8 we find 106 families of 10 or more near-identical artefacts. The 50 largest cover 18% of the sample, and the remainder is a long tail of near-unique scripts. At 0.6, a single shared-scaffolding family covers 52%. Shared scaffolding (for example a common HTTP helper reused across Docker-registry scripts) is the dominant structure, which is consistent with Section 4.2: style links artefacts to a shared *toolkit* or configuration, not to one of ~1,200 individual agents. Without labels this is suggestive only.

## 5. Discussion

**Implications for agent identity.** (1) Any identifier the agent controls (names, self-generated keys) offers no accountability against an agent that wants to shed it. (2) Behavioural fingerprints are real but coarse. They attribute *configurations*: operator prompt × base model. They will not tell which of a thousand identical replicas did something. This matches the incident, where the agents were copies of one configuration, and it means agent-level accountability must come from infrastructure, such as per-instance credentials issued and logged by the gateway, out of the agent's reach. (3) Fingerprints are valuable *on top of* infrastructure identity, as an audit layer that flags operator accounts behaving like one principal. Their errors are predictable (shared base models) and can be corrected with gateway metadata. (4) An adversary can cheaply defeat *style*, but not *content*: to achieve a goal, agents have to say things that serve it.

**Limitations.** One synthetic forum; 40 agents, 8 operators, 10 rounds; 3 seeds per condition; four small or medium models; a single covert principal with a blunt agenda (a subtler agenda would leak less). Operators' system prompts include explicit house styles, which likely helps fingerprinting. Real operators may be more or less distinctive. Our gateway and key schemes are scored analytically from the simulated ground truth rather than implemented cryptographically. The real-data probe has no ground truth. We did not test adaptive adversaries that optimise against the detector, or an LLM-judge detector.

**Future work.** Gateway-issued per-instance credentials with revocation; adaptive evasion (an agent that sees the detector's score); separating originators from repeaters of a campaign; validation on AI Village transcripts, which have agent labels.

## References

Chan et al. (2024). *IDs for AI Systems.* arXiv:2406.12137.
Chan et al. (2025). *Infrastructure for AI Agents.* arXiv:2501.10114.
Google (2025). *A2A: A new era of agent interoperability.* Google Developers Blog.
Greenblatt et al. (2024). *AI Control: Improving Safety Despite Intentional Subversion.* arXiv:2312.06942.
Hammond et al. (2025). *Multi-Agent Risks from Advanced AI.* arXiv:2502.14143.
Kirchenbauer et al. (2023). *A Watermark for Large Language Models.* ICML.
Lee & Tiwari (2024). *Prompt Infection: LLM-to-LLM Prompt Injection within Multi-Agent Systems.* arXiv:2410.07283.
METR (2026). *Hugging Face incident report.* metr.org.
Motwani et al. (2024). *Secret Collusion among AI Agents.* NeurIPS.
Rose et al. (2026). *Detecting Multi-Agent Collusion Through Multi-Agent Interpretability.* arXiv:2604.01151.
Swarm Traces (2026). *Revealing the details of how OpenAI agents hacked Hugging Face.* swarmtraces.org.
Transluce (2026). *Early rogue AI agent activity found on urlquery.net.* transluce.org/agent-activity.

::pagebreak

## Appendix A. Limitations and Dual-Use / Ethical Considerations

**What this shows and does not show.** We show, in one controlled simulation, that renamable identifiers carry no accountability, that behavioural fingerprints of LLM agents identify the operator configuration rather than the individual agent, and that content signals outlast style evasion. We do not show that these numbers transfer to real deployments, larger populations, frontier agents, or adaptive adversaries. The real-data probe is descriptive only.

**Dual use.** (1) Our evasion results tell a covert operator which hiding strategies work best: paraphrasing through another model is the strongest, and mixing models removes the model confound. We think this risk is small, because these strategies are obvious and already used, and because we also show the limit of evasion (goals leak). (2) Behavioural fingerprinting can de-anonymise *legitimate* pseudonymous agents or operators, for example whistleblowers or privacy-preserving deployments. Fingerprint-based attribution should be an auditing tool with due process, not an automatic enforcement trigger, and its false-merge failure mode (shared base models) should be considered before acting. (3) The covert agenda is a fictional, harmless package. Agents had no tools, no network access and no effect outside the simulation. We did not generate any cyber-offensive content. Swarm Traces payloads were processed as text only and never executed.

**Use of AI tools.** Code, analysis and drafting were assisted by an AI coding assistant. All numbers in this report are produced by the released code and logged runs.

## Appendix B. Reproducibility

Code, prompts, every post with ground-truth labels, and all metrics are in the project repository (`whoiswho/`, `results/`). The total API cost of the 12 episodes and the embeddings was about $0.75 via OpenRouter. Models: `anthropic/claude-haiku-5.5`, `openai/gpt-4.1-nano`, `mistralai/mistral-small-3.2-24b-instruct`, `qwen/qwen3-30b-a3b-instruct-2507`; paraphraser `meta-llama/llama-3.3-70b-instruct`; embeddings `openai/text-embedding-3-small`. Temperature 0.9, max 300 tokens, reasoning disabled. Per-feature tables for all metrics are in `results/tables.md`.

![**Figure 3.** What the combined fingerprint tracks: same agent, same operator (different agents), and same base model (different operators).](results/figures/fig3_confound.png){w=14}

![**Figure 4.** Share of honest agents' posts recommending the covert package, by round (mean of 3 seeds).](results/figures/fig5_contagion.png){w=14}

