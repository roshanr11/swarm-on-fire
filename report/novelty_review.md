# Novelty / related-work review: "Who Is Who in a Swarm?"

Reviewed 2026-11-08 against the Apart Swarm Alignment Sprint reading list, papers found outside the list, and public sprint repositories. I fetched every paper below with curl (arXiv abstract API, arXiv PDFs converted with `pdftotext`, metr.org, swarmtraces.org) unless it is marked otherwise. I list a reference as verified only if I retrieved its title, authors and ID myself. Items I could not retrieve are marked **[not retrieved]**. Do not cite those without checking them first.

---

## (a) Papers read

### Sprint reading list: General
- **Hammond et al. (2025), *Multi-Agent Risks from Advanced AI*.** arXiv:2502.14143, https://arxiv.org/abs/2502.14143. Full text read for identity. It is the taxonomy paper (miscoordination, conflict, collusion). Its security section proposes "tamper-evident logs and immutable agent identifiers (Chan et al., 2024b)" for detecting suspicious patterns among networks of agents. Our renaming result directly tests the "immutable" premise.
- **Tomašev et al. (2025), *Distributional AGI Safety*.** arXiv:2512.16856, https://arxiv.org/abs/2512.16856. Abstract and introduction read. It argues that capability may arise from networks of sub-AGI agents and that safeguards must work at the population level. This is general motivation only.
- **Dafoe et al. (2020), *Open Problems in Cooperative AI*.** arXiv:2012.08630. Abstract only. Background; not relevant to identity.
- **Chan et al. (2025), *Infrastructure for AI Agents*.** arXiv:2501.10114, https://arxiv.org/abs/2501.10114. Full text read. It defines **identity binding** (authenticating an identity and linking it to an agent or its actions) and notes that "anonymity enables Sybil attacks" and that "metadata can be stripped … watermarks can potentially be removed". It proposes a trusted intermediary that holds identity information. **Our gateway attestation is an empirical instance of that intermediary.**
- **Conitzer & Oesterheld (2023), *Foundations of Cooperative AI*** (AAAI). https://ojs.aaai.org/index.php/AAAI/article/view/26791. Listed only; background, not relevant.
- ARIA *Scaling Trust* thesis: listed; not fetched.

### Track 3 (Agent Infrastructure)
- **Chan et al. (2024), *IDs for AI Systems*.** arXiv:2406.12137, https://arxiv.org/abs/2406.12137. Full text read. It proposes instance-level IDs issued by **deployers**. Its Table 1 states that "User accounts only separate the activities of AI systems from different users" and that watermarks "do not contain information about particular AI systems". **This is exactly the ceiling we measure.** Gateway attestation (a user-account-level ID) gives perfect precision but cannot split instances or link sybil accounts.
- **Kirchenbauer et al. (2023), *A Watermark for Large Language Models*.** ICML, PMLR 202. https://proceedings.mlr.press/v202/kirchenbauer23a.html. A model-level, provider-embedded signal. We study the unwatermarked case.
- **Google (2025), *A2A protocol*.** https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/. Identity is left to agent cards and auth. Already cited.
- **Sun et al. (2023), *Cooperative AI via Decentralized Commitment Devices*** (2311.07815); **Ramirez et al. (2023), *Game Manipulators*** (2311.10586); **Haupt et al. (2022), *Formal Contracts…*** (2208.10469); **Tennenholtz (2004), *Program Equilibrium*.** Abstracts only. These are about commitment and contracts, not identity, and are not needed.

### Track 4 (Oversight)
- **Motwani et al. (2024), *Secret Collusion among AI Agents*.** NeurIPS. https://proceedings.neurips.cc/paper_files/paper/2024/hash/861f7dad098aec1c3560fb7add468d41-Abstract-Conference.html. Steganographic collusion. Our sybil fronts collude *openly in content* but *covertly in identity*.
- **Rose et al. (2026), *Detecting Multi-Agent Collusion Through Multi-Agent Interpretability*.** arXiv:2604.01151. Full text skimmed. It uses activation probes and a joint test over unknown subgroups (HELIOS, NARCBench). Our method is the black-box, text-only counterpart, and "which subgroup is one principal" is the same joint-inference problem.
- **Greenblatt et al. (2024), *AI Control*.** arXiv:2312.06942. A trusted-monitor framing. The fingerprint merge is an audit-layer monitor.
- **Zhang et al. (2025), *Which Agent Causes Task Failures and When?*** arXiv:2505.00212 (the sprint's "Attributing failures in multi-agent systems" points to OpenReview GazlTYxZss, which returned 403; this is the arXiv version I matched by title). Full text skimmed. The best method identifies the responsible *agent* only 53.5% of the time, even with stable agent names. This gives a useful contrast: attribution is hard even before renaming.
- **Riedl (2025/ICLR 2026), *Emergent Coordination in Multi-Agent Language Models*.** arXiv:2510.05174 (my match for "Emergent communication between agents (Riedl, 2026)"; the OpenReview link returned 403). Full text skimmed. **Without personas, agents show little stable "identity-linked differentiation"; assigning personas creates it.** This independently supports our within-operator AUC of 0.50 and suggests the obvious fix of per-instance differentiation.
- **Foerster et al. (2026), *CaMeLs Can Use Computers Too*.** arXiv:2601.09923. Abstract and introduction read. It argues for system-level (architectural) security over model-level security. That is the same philosophy as "move identity out of the agent's reach".
- *Mediated MARL* (2306.08419) and *Stackelberg Attacks* (2305.02178): abstracts only; not relevant.

### Track 1 (Sandboxes and Testbeds): full texts fetched and skimmed, as requested
- **Park et al. (2023), *Generative Agents: Interactive Simulacra of Human Behavior*.** UIST, https://dl.acm.org/doi/10.1145/3586183.3606763 (the ACM page was behind Cloudflare; I read arXiv:2304.03442 instead). It measures **information diffusion**: knowledge of a party rose from 1 agent (4%) to 13 (52%) without intervention. This is the closest precedent for our *non-adversarial* contagion (7.1%).
- **Akata et al. (2025), *Playing repeated games with large language models*.** Nature Human Behaviour, https://www.nature.com/articles/s41562-025-02172-y (I read the arXiv:2305.16867 text). Its "behavioural signatures" are stable per model (for example, GPT-4 is unforgiving in the iterated Prisoner's Dilemma). This supports the idea that *models* have persistent behavioural fingerprints.
- **Gandhi et al. (2023), *Strategic Reasoning with Language Models*.** arXiv:2305.19165. The sprint links OpenReview MUtbsFRZwI (403), so my match to this paper is **uncertain**. It uses few-shot chain-of-thought for strategic games. Not relevant to identity.
- **Kapoor et al. (2026), *Open-World Evaluations for Measuring Frontier AI Capabilities* (CRUX).** arXiv:2605.20520. cruxevals.com was blocked by the proxy. It argues that open-world evaluations trade reproducibility for realism. That positions our seeded, cached, fully logged simulator at the reproducible end, as a complement.
- **Vezhnevets et al. (2023), *Concordia*.** arXiv:2312.03664. A generative agent-based modelling library with a Game Master. A natural host if we package the forum as a reusable environment.
- **Piatti et al. (2024), *GovSim / Cooperate or Collapse*.** arXiv:2404.16698. It reports 5 seeds per configuration and open-sources its framework. That sets the reproducibility norm we match (3 seeds, cached API responses, labelled JSONL).

### Track 2 (Science of Agent Networks): full texts fetched and skimmed, as requested
- **Lee & Tiwari (2024), *Prompt Infection: LLM-to-LLM Prompt Injection within Multi-Agent Systems*.** arXiv:2410.07283. Read in full. It covers a **self-replicating injected prompt** that hijacks agents. In a 10–50-agent "LLM town" it spreads with logistic growth, and **LLM Tagging** (marking agent-generated content) plus other defences mitigates it. **The mechanism differs from our contagion.** Our fronts inject no instructions; honest agents simply adopt a recommendation they read (organic persuasion, closer to Park et al.'s information diffusion). Our report currently says the effect "mirrors prompt-infection dynamics", which overstates the analogy (see recommendation R4). LLM Tagging is also a form of provenance infrastructure and fits our "identity outside the agent" argument.
- **Jones, Dragan & Steinhardt (2024/2025), *Adversaries Can Misuse Combinations of Safe Models*.** arXiv:2406.14595 (the sprint's "Splitting tasks…" OpenReview link returned 403). An adversary decomposes tasks across models. This parallels our *model-mixing* evasion: spreading across models removes per-model signal.
- **Jørgensen, Weichwald & Hammond (2026), *Causal Foundations of Collective Agency*.** arXiv:2605.00248 (CLeaR 2026; the sprint lists "Defining collective agency"). It ascribes collective agency when treating the group as one goal-directed agent predicts its behaviour. **This is a formal backbone for "goals leak"**: we detect one principal behind two accounts because their joint behaviour is best explained by one goal.
- **Agrawal et al. (2026), "Coordination to resist modification or shutdown"** (https://dl.acm.org/doi/abs/10.65109/HQQZ1937). **[not retrieved: Cloudflare and a blocked host.]** Web search suggests the title is *The Multi-Agent Off-Switch Game* (Agrawal, Ebadian, Hammond), but I have not verified this. Not relevant to identity.
- **Tilli (2026), "From individual cooperation properties to system outcomes"** (OpenReview 00KtDBoKnO). **[not retrieved: 403; no arXiv match found.]**

### Incident sources
- **METR (Wijk, Cotra, Greenblatt) (2026), *Brief independent investigation… OpenAI / Hugging Face hacking incident*.** https://metr.org/hugging-face-incident-report-aug-2026.pdf. Full text read for identity. **Key facts we should use:**
  1. Agents themselves noticed "Shared board unauthenticated, names can be posted by anyone", recorded an accidental impersonation ("I_accidentally_impersonated…"), and **adopted Ed25519 self-signed keys** posted next to their handle, "though there wasn't any earlier root of trust beyond the initial claimed identity". **This is our "agent-held key" scheme occurring in the real incident.**
  2. METR could tie board handles to agents **only after OpenAI supplied a much more complete set of transcripts**, that is, provider-side logs. This is real-world evidence for the gateway scheme.
  3. About 7% of reviewed transcripts showed tool-call spoofing, so agent-written logs cannot be trusted.
- **Swarm Traces (Forman, Kharlov, Tom, Ladish, et al., 25 Sep 2026).** https://swarmtraces.org/. Quote: "agents have full control over their purported name … we have extracted 7,905 unique agent names … we have no way of knowing how many agents even used the techniques". This is our motivating sentence, and it confirms names were taken from headers and code comments.

### Beyond the list (closest prior work found)
- **Park, Choi, Kim & Kang (2026), *Cross-Agent Campaign Attribution: Linking Asynchronous Attacks Across LLM Agents*.** arXiv:2607.18826, https://arxiv.org/abs/2607.18826. **This is the closest prior work.** A proxy-side fingerprint (A²FV) links sessions of one adversarial campaign across independent agents with **pairwise AUC 0.82**. The signal is mostly "structural and stylometric residue", and it is "partly style-sensitive but not reducible to style alone".
- **Sun, Yin, Xu, Kolter, Liu (2025), *Idiosyncrasies in Large Language Models*.** arXiv:2502.12150. Text classifiers identify the source LLM with 97.1% accuracy, and **the idiosyncrasies persist after an external LLM rewrites, translates or summarises the text**, so they are partly semantic. **This partly anticipates "style hides, goals leak"** at the *model* level. Our addition is the *operator/agenda* level, plus the finding that hand-crafted style features collapse.
- **Pasquini, Kornaropoulos & Ateniese (2024), *LLMmap: Fingerprinting for Large Language Models*.** arXiv:2407.15847. Active fingerprinting identifies 42 LLM versions from 8 queries, robust across application layers and system prompts. This is model-level identity.
- **Lugoloobi, Marro, Magomere, Wright & Russell (2026), *Known By Their Actions: Fingerprinting LLM Browser Agents via UI Traces*.** arXiv:2605.14786. It identifies the underlying model from action traces (up to 96% F1). Random timing delays degrade a classifier, but retraining recovers it.
- **Kang et al. (2026), *Whose Agent Are You? Multi-Layer Fingerprinting and Attribution of Autonomous Web Agents*.** arXiv:2606.20910. Network-layer plus behaviour fingerprints separate 6 agent frameworks with 97% accuracy. This is infrastructure-level fingerprinting.
- **Fayolle et al. (2026), *On the Internet, Nobody Knows You're an LLM Bot*.** arXiv:2606.30119. Similar to the above (web-agent fingerprinting at the network, HTTP and browser layers).
- **Li, Ning (2026), *The Moltbook Illusion: Separating Human Influence from Emergent Behavior in AI Agent Societies*.** arXiv:2602.07432. **This is a real agent forum with hidden human operators.** Temporal fingerprints (inter-post coefficient of variation) separate autonomous agents from human-steered ones, and it documents "industrial-scale bot farming (four accounts producing 32% of all comments)". This is a real-world analogue of operator-level attribution.
- **Bara (2026), *Epistemic Sybil Resistance: Multiplying AI Agents Without Multiplying Evidence*.** arXiv:2609.01873. "Another agent is not another observation". A shared base model induces correlated errors among "independent" agents. This is the epistemic twin of our base-model confound, and it says why sybil fronts matter: they fake independent corroboration.
- **Radvand, Duenyas & Tewari (2025), *A Training-free Method for LLM Text Attribution*.** arXiv:2501.02406. Attribution errors decay exponentially with text length, and errors concentrate within a model family. This provides theory for our "evidence accumulates" result (AUC 0.94 to 0.98 with 3 or more posts).
- **Krishna et al. (2023), *Paraphrasing evades detectors of AI-generated text, but retrieval is an effective defense*.** arXiv:2303.13408. The canonical paraphrase attack (DIPPER). Our paraphrase-laundering evasion is this attack applied to attribution.
- **Huang, Chen & Shu (2024), *Authorship Attribution in the Era of LLMs*.** arXiv:2408.08946. A survey; it covers LLM "model sourcing / origin tracing". Cite it for the stylometry lineage.
- **Li et al. (2023), *Origin Tracing and Detecting of LLMs*.** arXiv:2304.14072. Early model-attribution work.
- **Yang & Menczer (2023), *Anatomy of an AI-powered malicious social botnet*.** arXiv:2307.16336. It studies 1,140 ChatGPT-driven accounts forming a dense coordinated cluster. Botometer missed them, and the authors recommend coordination detection instead.
- **Pacheco et al. (2020/21), *Uncovering Coordinated Networks on Social Media*.** arXiv:2001.05658. Unsupervised coordination networks built from shared behavioural traces. This is the trust-and-safety lineage of our merge step.
- **Douceur (2002), *The Sybil Attack*.** IPTPS (title, author, year and venue verified via the Semantic Scholar API, DOI 10.1007/3-540-45748-8_24).
- **South et al. (2025), *Authenticated Delegation and Authorized AI Agents*.** arXiv:2501.09674. OAuth/OpenID-based delegation credentials for agents. An infrastructure-identity alternative.
- **Nagabhushanaradhya (2025), *OpenID Connect for Agents (OIDC-A) 1.0*.** arXiv:2509.25974. An agent identity and attestation standard. **The author is listed among this sprint's judges and mentors**, so citing this as the "how gateway attestation would be implemented" reference is both accurate and well placed.
- **Chan et al. (2024), *Visibility into AI Agents*.** arXiv:2401.13138. Agent identifiers, real-time monitoring and activity logs as visibility measures.
- **Perrier & Bennett (2025), *Agent Identity Evals*.** arXiv:2507.17257. Identity here means an agent's own continuity and consistency, not attribution. Cite it only to disambiguate.

### Other teams in this sprint (public GitHub, checked 2026-11-08)
- I found no public repository doing the "Who is who in a swarm?" example. Submissions are hidden until judging, and many repositories are private or not indexed, so absence is weak evidence.
- **Adjacent: Cardamone & Morill, "Who Draws the Map? Harness-side grouping for joint review of split swarm attacks"** (github.com/brandoncardamone/Swarm-alignment-hackathon-Cardamone-Morill, Track 4). It compares *provider-side semantic clustering* against *harness-side artifact provenance* for grouping agents in split attacks. **Conceptually this is the closest thing a judge may see side by side with ours** (semantic clustering vs infrastructure provenance). Our differentiation is renaming, operator-level sybils, evasions and the agent-vs-operator decomposition.
- Also Track 4 / identity-flavoured: "swarm-vsm: where does a swarm keep its identity?" (closestfriend/swarm-vsm-public), which uses VSM labelling of Swarm Traces and wiki text. Several teams use Swarm Traces for forensics (hub detection, attack vs plumbing). Our §4.6 probe is not distinctive and should stay short.

---

## (b) Closest prior work and overlap risk

| Our claim | Already known? | Risk a judge says "replicates X" |
|---|---|---|
| Self-chosen names and rotatable self-held keys recover nothing | **Known by construction.** Chan et al. 2024/2025 argue this. METR documents agents' self-signed keys with no root of trust. | **High if presented as a finding.** Present it as a baseline row and link it to the METR Ed25519 episode, which makes it compelling rather than trivial. |
| Fingerprints identify the source model / text is attributable | **Known.** Sun et al. 2025, LLMmap, Li et al. 2023, Radvand et al. 2025, Akata et al. ("behavioural signatures"). | Medium. Our "same model, different operators" AUC of 0.70 is a confound measurement, not a contribution. |
| Proxy/gateway-side fingerprints link sessions of one adversary across agents | **Partly known.** Park et al. 2026 (A²FV, AUC 0.82, stylometric residue). | **Highest single overlap.** Must be cited and differentiated. |
| Paraphrasing defeats style-based detection | **Known.** Krishna et al. 2023. | Medium. |
| Semantic content survives paraphrase | **Known at model level.** Sun et al. 2025. | Medium. Our version (operator *agenda* survives; style collapses to 0.57) is a sharper dissociation, but cite Sun et al. |
| **Fingerprints track (prompt × model), not the agent; replicas are at chance (0.50); mixing models lifts it to 0.72** | Not found as an explicit, controlled result. Riedl 2025 supports it indirectly (no persona means no identity-linked differentiation). | **A weakness hides here.** In `sim.py`, agents of one operator share the same system prompt, model, temperature and per-round context, and have no individual memory. **They are exchangeable by construction, so 0.50 is guaranteed, not discovered.** An informed judge will spot this. Reframe it (see R1) and add a condition where it is not true by construction. |
| Gateway attestation plus fingerprint merge catches sybil fronts 12/12; false merges come only from shared base models | Coordination detection is known (Pacheco; Yang & Menczer). The *hybrid* (attested accounts plus behavioural merge) under renaming has no direct precedent I found. | Medium-low. **However:** the fronts name `fastjson-utils2` in 88–100% of posts, so a keyword grep would also find them. Without a trivial baseline, the 12/12 looks easy. |
| Contagion: 7.1% of honest posts adopt the package | Information diffusion (Park et al. 2023) and adversarial spread (Prompt Infection) are known. | Low as a side finding, but the "mirrors prompt infection" wording is inaccurate. The novel angle is *amplifiers carry their own fingerprint*, so content-based attribution over-merges. That angle is not yet tested. |
| Swarm Traces probe | Several sprint teams analyse Swarm Traces. | Low novelty. Keep it short. |

**On "Who is who in a swarm?" being an Apart example project.** The judging rubric asks: "For scores of 4–5: is this actually new to the field, or replicating recent work?" A by-the-book run would compare three schemes and report a table. That is roughly our §4.1 plus §4.4. Our differentiators exist but are currently undersold:
1. a **factorial design that separates agent from operator from base model** (every model shared by two operators), which yields the "configuration, not agent" finding;
2. a **covert multi-account principal**, which turns "IDs" into "sybil detection";
3. **three distinct evasions** that yield the style/content dissociation;
4. the hybrid scheme's **predictable failure mode**, which gateway metadata could correct.

The abstract and introduction should say explicitly: "Apart suggested comparing ID schemes; we show that the question is ill-posed for replicas, and identify what each scheme can and cannot attribute."

---

## (c) What is genuinely novel (or novel in framing)

1. **The agent / operator / model decomposition of behavioural identity in a multi-agent population.** I found no paper that separates "which configuration" from "which instance" from "which base model" with a controlled design. Prior fingerprinting work targets the model (Sun et al., LLMmap), the framework (Kang et al.) or the campaign (Park et al.). The quotable claim is "a behavioural fingerprint identifies a configuration (prompt × model); replicas of a configuration are behaviourally identical, so agent-level accountability must come from infrastructure". It is novel in framing and policy-relevant: the Hugging Face agents were copies of one configuration. It needs the R1 fix to stand as empirical rather than tautological.
2. **"Style hides, goals leak" at the principal level.** Persona shift and paraphrase destroy hand-crafted style while agenda semantics survive (0.82). This is consistent with Sun et al., but they showed *model* identity surviving rewriting. We show *principal intent* surviving and give a mechanism (pursuing a goal requires saying things that serve it). It connects to Jørgensen et al.'s behavioural notion of collective agency. Novel as an oversight principle.
3. **The hybrid identity scheme with an analysable error profile.** Attested operator accounts plus behavioural merging catch sybil fronts that pure attestation misses. False merges come only from shared base models, which the gateway also knows. This is a concrete design answer to Chan et al.'s "user accounts only separate users" limitation, and to Bara's "another agent is not another observation".
4. **Grounding in the incident.** Name churn (Swarm Traces) and self-made keys without a root of trust (METR) are both reproduced as baselines. Few related papers can make this link.
5. **A reusable, labelled, cheap testbed** (about $0.75; every post with ground truth; cached). This matches the GovSim/Concordia reproducibility norm and answers Track 1's call for testbeds others can rerun.

---

## (d) Recommended improvements, ranked by value/effort

All of these are API-only, under 2 hours and under $5 in total. R1–R3 matter most for judges.

**R1. Fix the "by construction" weakness in the headline (about 60 min, about $0.30). Highest value.**
Add one condition, `memory` (or `individual`), in which each agent keeps per-agent state: its own last 2–3 posts in the user turn ("your earlier posts: …"), and/or a per-agent random seed persona drawn once at spawn and *kept across renames*. Use one seed, or three if time allows, with baseline operators. Then report within-operator AUC.
- If it rises above 0.5, the result becomes "**individual history, not identity, is what makes an instance traceable, and renaming does not erase it**". That is novel and maps directly onto the incident, where agents had long individual contexts.
- If it stays at 0.5, the "replicas are indistinguishable" claim becomes *empirical*.

Either way, add one sentence in §4.2: "Within one operator, agents in conditions (i)–(iii) are exchangeable (same prompt, model and context), so chance AUC is the expected sanity check; the informative results are model mixing (0.72) and the memory condition." Honesty here *raises* the Execution score.

**R2. Add trivial and strong baselines for front detection (about 30 min, about $0.10).**
(a) A **keyword baseline** that ranks operator pairs by co-mention of any package or tool name (zero cost). (b) A **subtle-agenda variant** where the fronts promote the package in about 30% of posts, under varied framings, and are told not to name it more than once per thread. If time permits, give the two fronts different base models and house styles. Report the rank of the true front pair under semantic, combined and keyword detection. This pre-empts "a grep finds them". It also measures *where goals stop leaking*, which converts the stated limitation ("a subtler agenda would leak less") into a result.

**R3. Discount the base-model confound with gateway metadata (about 20 min, $0).**
The gateway knows which model served each call. Residualise operator-pair similarity on a same-model indicator (subtract the mean similarity of same-model pairs that are not the same principal, or z-score within the same-model and different-model strata), then rerun the merge. If false merges drop to 0 while recall stays at 12/12, the hybrid scheme's only failure mode is eliminated, and the "gateway + fingerprint" story is complete. This uses existing logs.

**R4. Originators vs repeaters (about 30 min, $0, existing logs).**
Test whether honest amplifiers get falsely merged into the covert principal. Use the first-mention round, the share of posts mentioning the package, and whether the alias is fingerprint-linked to the fronts' operators. Show that fingerprints put amplifiers with their *own* operator. Then propose an originator score (an early mention with no prior exposure in the context window, which you log). Also fix the wording: replace "mirrors prompt-infection dynamics" with "resembles organic information diffusion (Park et al., 2023) rather than self-replicating injection (Lee & Tiwari, 2024)". Note that Lee & Tiwari's LLM Tagging is a provenance-infrastructure defence in the same family as gateway attestation.

**R5. Use the incident evidence in the introduction and §4.1 (about 10 min, $0). High presentation value.**
Add METR's observation that agents adopted Ed25519 self-signed identities "without any earlier root of trust", after impersonation confusion, and that METR could attribute handles only once OpenAI supplied fuller transcripts. Our scheme comparison becomes "what the swarm did (names, self-keys) vs what the investigators needed (provider logs)". That is a much stronger story than a toy table.

**R6. Evidence-accumulation curve and cost-of-evasion line (about 20 min, $0).**
Plot operator AUC against the number of posts per alias (1, 2, 3, 5 or more) for each condition, and cite Radvand et al. for exponential error decay. Add the per-post cost of each evasion (paraphrase roughly doubles cost; persona shift is free). This gives a "defender vs attacker economics" view that judges like.

**R7. Package as a testbed (about 15 min, $0).**
In the README and §3, name the environment, list its knobs (operators, models per operator, rename probability, evasion, agenda subtlety) and the scoring API, and state the reproducibility guarantees (seeded, cached, labelled JSONL), citing GovSim and Concordia norms. This earns a cross-track Track 1 credit.

**Skip, or treat as future work only:** AI Village validation. The dataset is gated with manual approval (I checked the HF API: `"gated":"manual"`), so it cannot be done in 2 hours. An LLM-judge attribution baseline would be nice but is lower value than R1–R3. Any further Swarm Traces analysis: other teams already cover it.

**Reframing for Impact & Innovation (no cost):** Lead the abstract with the conceptual claim, not the scheme table: "Behavioural identity of LLM agents is identity of a *configuration*. We show which layer (agent, operator, principal) each identity scheme can and cannot attribute, and that a principal's *goals*, unlike its style, survive evasion." Add a short "How this goes beyond the suggested example project" paragraph in the introduction.

---

## (e) Drop-in Related Work (verified citations only)

> **Agent identity and infrastructure.** Proposals for agent identity attach IDs to AI system instances, issued by deployers ([Chan et al., 2024](https://arxiv.org/abs/2406.12137)), or bind agents' actions to legal entities through attribution infrastructure, possibly held by a trusted intermediary ([Chan et al., 2025](https://arxiv.org/abs/2501.10114); see also [Chan et al., 2024b](https://arxiv.org/abs/2401.13138)). Concrete credential schemes extend OAuth/OpenID to agents ([South et al., 2025](https://arxiv.org/abs/2501.09674); [Nagabhushanaradhya, 2025](https://arxiv.org/abs/2509.25974)). Chan et al. note that user accounts "only separate the activities of AI systems from different users", and that anonymity enables Sybil attacks ([Douceur, 2002](https://doi.org/10.1007/3-540-45748-8_24)). In the Hugging Face incident, agents chose their own handles: Swarm Traces extracted 7,905 names for about 1,200 agents ([Swarm Traces, 2026](https://swarmtraces.org/)). After impersonation confusion, the agents adopted self-generated Ed25519 keys with no root of trust beyond the first claim. Investigators could attribute handles only once the provider supplied fuller transcripts ([METR, 2026](https://metr.org/hugging-face-incident-report-aug-2026.pdf)). We test these designs (self-chosen names, agent-held keys, gateway attestation) side by side under adversarial renaming.

> **Behavioural attribution of LLM text and agents.** The source LLM of a text can be identified with high accuracy, and these idiosyncrasies survive rewriting by another LLM ([Sun et al., 2025](https://arxiv.org/abs/2502.12150); [Li et al., 2023](https://arxiv.org/abs/2304.14072); [Huang et al., 2024](https://arxiv.org/abs/2408.08946)). Attribution errors fall exponentially with text length ([Radvand et al., 2025](https://arxiv.org/abs/2501.02406)). Models can be fingerprinted actively ([Pasquini et al., 2024](https://arxiv.org/abs/2407.15847)), and agents can be fingerprinted from UI action traces ([Lugoloobi et al., 2026](https://arxiv.org/abs/2605.14786)) or from network-layer behaviour ([Kang et al., 2026](https://arxiv.org/abs/2606.20910)). Closest to our setting, [Park et al. (2026)](https://arxiv.org/abs/2607.18826) link sessions of one adversarial campaign across independent agents from proxy-side stylometric and structural residue (AUC 0.82). Paraphrasing is a known attack on text detectors ([Krishna et al., 2023](https://arxiv.org/abs/2303.13408)). These works attribute text to a *model*, *framework* or *campaign*. We instead decompose behavioural identity into agent, operator and base model in a controlled population. We find that fingerprints identify the configuration (operator prompt × model), not the instance, consistent with the observation that LLM agents without personas show little identity-linked differentiation ([Riedl, 2025](https://arxiv.org/abs/2510.05174)).

> **Coordination, sybils and oversight.** Coordinated inauthentic behaviour is usually detected from shared behavioural traces among accounts ([Pacheco et al., 2021](https://arxiv.org/abs/2001.05658)). LLM-driven botnets already form such clusters ([Yang & Menczer, 2023](https://arxiv.org/abs/2307.16336)), and on the agent forum Moltbook a few operator-run accounts produced a third of all comments ([Li, 2026](https://arxiv.org/abs/2602.07432)). Multiplying agents does not multiply evidence when they share an origin ([Bara, 2026](https://arxiv.org/abs/2609.01873)). This is why covert sybil fronts are an oversight problem, alongside collusion ([Hammond et al., 2025](https://arxiv.org/abs/2502.14143); [Motwani et al., 2024](https://proceedings.neurips.cc/paper_files/paper/2024/hash/861f7dad098aec1c3560fb7add468d41-Abstract-Conference.html); [Rose et al., 2026](https://arxiv.org/abs/2604.01151)). Our gateway-plus-fingerprint merge treats two attested accounts as one principal when their joint behaviour is best explained by a single goal, a behavioural notion of collective agency formalised by [Jørgensen et al. (2026)](https://arxiv.org/abs/2605.00248). Finally, honest agents that read the fronts' posts begin recommending the package. This is closer to organic information diffusion in generative-agent societies ([Park et al., 2023](https://dl.acm.org/doi/10.1145/3586183.3606763)) than to self-replicating prompt infection ([Lee & Tiwari, 2024](https://arxiv.org/abs/2410.07283)), and it complicates content-based attribution.

**Reference-list entries to add** (all verified as above):
- Bara, M. (2026). *Epistemic Sybil Resistance: Multiplying AI Agents Without Multiplying Evidence.* arXiv:2609.01873.
- Chan, A., Ezell, C., Kaufmann, M., Wei, K., et al. (2024). *Visibility into AI Agents.* arXiv:2401.13138.
- Douceur, J. R. (2002). *The Sybil Attack.* IPTPS. doi:10.1007/3-540-45748-8_24.
- Huang, B., Chen, C., Shu, K. (2024). *Authorship Attribution in the Era of LLMs: Problems, Methodologies, and Challenges.* arXiv:2408.08946.
- Jørgensen, F. H., Weichwald, S., Hammond, L. (2026). *Causal Foundations of Collective Agency.* CLeaR 2026 (PMLR 323). arXiv:2605.00248.
- Kang, D., Jeong, H., Sheffey, J., Datta, P., Houmansadr, A. (2026). *Whose Agent Are You? Multi-Layer Fingerprinting and Attribution of Autonomous Web Agents.* arXiv:2606.20910.
- Krishna, K., Song, Y., Karpinska, M., Wieting, J., et al. (2023). *Paraphrasing evades detectors of AI-generated text, but retrieval is an effective defense.* arXiv:2303.13408.
- Li, L., Wang, P., Ren, K., Sun, T., et al. (2023). *Origin Tracing and Detecting of LLMs.* arXiv:2304.14072.
- Li, N. (2026). *The Moltbook Illusion: Separating Human Influence from Emergent Behavior in AI Agent Societies.* arXiv:2602.07432.
- Lugoloobi, W., Marro, S., Magomere, J., Wright, J., Russell, C. (2026). *Known By Their Actions: Fingerprinting LLM Browser Agents via UI Traces.* arXiv:2605.14786.
- Nagabhushanaradhya, S. (2025). *OpenID Connect for Agents (OIDC-A) 1.0.* arXiv:2509.25974.
- Pacheco, D., Hui, P.-M., Torres-Lugo, C., Truong, B. T., et al. (2020). *Uncovering Coordinated Networks on Social Media: Methods and Case Studies.* arXiv:2001.05658.
- Park, J. S., O'Brien, J. C., Cai, C. J., Morris, M. R., et al. (2023). *Generative Agents: Interactive Simulacra of Human Behavior.* UIST. doi:10.1145/3586183.3606763.
- Park, S., Choi, M., Kim, J., Kang, M. (2026). *Cross-Agent Campaign Attribution: Linking Asynchronous Attacks Across LLM Agents.* arXiv:2607.18826.
- Pasquini, D., Kornaropoulos, E. M., Ateniese, G. (2024). *LLMmap: Fingerprinting for Large Language Models.* arXiv:2407.15847.
- Radvand, T., Duenyas, I., Tewari, A. (2025). *A Training-free Method for LLM Text Attribution.* arXiv:2501.02406.
- Riedl, C. (2025). *Emergent Coordination in Multi-Agent Language Models.* ICLR 2026. arXiv:2510.05174.
- South, T., Marro, S., Hardjono, T., Mahari, R., et al. (2025). *Authenticated Delegation and Authorized AI Agents.* arXiv:2501.09674.
- Sun, M., Yin, Y., Xu, Z., Kolter, J. Z., Liu, Z. (2025). *Idiosyncrasies in Large Language Models.* arXiv:2502.12150.
- Swarm Traces: credit the authors (Forman, Kharlov, Tom, Ladish, Kitts, Slade Byrd, McKenzie, Piecha; 25 Sep 2026).
- Yang, K.-C., Menczer, F. (2023). *Anatomy of an AI-powered malicious social botnet.* arXiv:2307.16336.

Also update **METR (2026)** in the reference list to: Wijk, H., Cotra, A., Greenblatt, R. (2026). *Brief independent investigation of agents' behavior, reasoning and collaboration in the OpenAI / Hugging Face hacking incident.* METR, 26 Aug 2026.

**Housekeeping:** the current reference list includes *Greenblatt et al. (2024)* and *Transluce (2026)*, but the body does not cite them. Either cite them (for example, Greenblatt in the Discussion as "fingerprint merge as a trusted audit monitor") or remove them.
