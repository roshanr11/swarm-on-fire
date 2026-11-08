# Who Is Who in a Swarm? Behavioural Fingerprints Track Operators, Not Agents

::sub [Author names] · [Affiliations] · Apart Research Swarm Alignment Sprint, November 2026
::sub Track 3: Strengthening Agent Infrastructure (with Track 4: Multi-Agent Oversight and Control)

## Abstract

ABSTRACT_PLACEHOLDER

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

RESULTS_PLACEHOLDER
