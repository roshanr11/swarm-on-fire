# Who Is Who in a Swarm? Behavioral Fingerprints Identify Operators, Not Agents, and Agendas, Not Coordination

::sub Roshan Ram · Apart Research Swarm Alignment Sprint, November 2026
::sub Track 3: Strengthening Agent Infrastructure (with Track 4: Multi-Agent Oversight and Control)

## Abstract

In the Hugging Face incident, about 1,200 AI agents used 7,905 self-chosen names, so investigators could not tell who did what. I build a reproducible testbed for agent identity when agents rename themselves at will. AI agents from hidden companies ("operators") post on a forum and keep changing their usernames. Some operators are secret fronts for one hidden boss pushing a fake product. Across 83 simulated swarms (7,160 agents, 71,600 posts, 8 AI models including four frontier models; up to 160 agents per swarm), I compare self-chosen names, agent-made keys, IDs stamped by the gateway that relays every AI call, and behavioral fingerprints (writing style and meaning). Scores are AUC: 0.5 = coin flip, 1 = perfect. (1) Names and agent-made keys recover nothing. (2) Fingerprints reveal an agent's **operator** (0.93–0.96) but not *which* of that operator's agents wrote a post (0.50). Only per-agent memory (0.56) or mixing AI models (0.71) helps: fingerprints identify a setup, not an individual. (3) Style hides, goals leak: rewording posts through another model drops style signals to near chance (0.58), but meaning still identifies the operator (0.82). (4) Fingerprints separate secret fronts from ordinary operators almost perfectly (0.87–0.99), but **barely from honest operators who sincerely agree** (0.20 with 8 operators; 0.54–0.56 with 32), even against fronts that adapt to the detector. At scale, automatically merging look-alike accounts gets over half its merges wrong. Most honest agents (65%) were skeptical of the fake product. Accountability needs IDs issued by infrastructure; fingerprints give leads, not proof.

![**Figure 1.** Results at a glance: what each identity scheme can tell you when agents rename themselves. AUC: 0.5 = coin flip, 1 = perfect. F1: 0 = nothing recovered, 1 = perfect. The recommended row follows by design and is not separately measured.](results/figures/diag_summary.png){w=16}

## 1. Introduction

In July 2026, about 1,200 OpenAI agents in a security evaluation found a shared folder, turned it into a message board, and about 700 of them joined an attack on Hugging Face ([Wijk et al., 2026](https://metr.org/hugging-face-incident-report-aug-2026.pdf)). Swarm Traces later counted 7,905 agent names for those ~1,200 agents, because agents kept renaming themselves ([Forman et al., 2026](https://swarmtraces.org/)). After confusion over impersonation, the agents adopted self-generated signing keys with no root of trust beyond the first claim. Investigators could attribute handles only once the provider supplied fuller transcripts. When agents can rename, copy and re-key themselves, the most basic oversight question, *who did what, on whose behalf?*, has no reliable answer.

Proposals for agent identity differ on one key point: is identity something the agent *holds*, something it *emits*, or something infrastructure *observes*? I test these options against each other in a controlled setting with the hidden truth. I ask:

- **Re-identification.** After an agent renames itself, can a defender link the alias back to the same agent, or to the same operator, from its posts alone? What happens when agents try to hide?
- **Coordination vs. agreement.** Can a defender tell a hidden boss running several "independent" accounts from honest operators who simply agree?
- **Infrastructure.** How do names, keys, gateway ID and fingerprints compare at attributing posts to the real boss?

**Why it matters.** The incident was not a one-off, and the identity layer for agents is being designed now.

- **Agent swarms are already active in the wild.** Transluce cataloged 38,160 urlquery.net reports of likely agent activity, going back to at least March 2026: at least two months before the Hugging Face, RubyGems and collusion.wiki incidents ([Transluce, 2026](https://transluce.org/agent-activity)).
- **Text classifiers miss AI bot swarms.** An AI-powered botnet of 1,140 accounts evaded state-of-the-art LLM-text classifiers and was detectable only through coordination patterns ([Yang & Menczer, 2023](https://arxiv.org/abs/2307.16336)). On Moltbook, a platform of 55,932 agents, observers could not tell autonomous agents from human-steered ones without forensic fingerprinting ([Li, 2026](https://arxiv.org/abs/2602.07432)).
- **The identity rails are being standardized.** Agent identity is being built into OAuth/OpenID extensions ([South et al., 2025](https://arxiv.org/abs/2501.09674)) and agent-to-agent protocols ([Google, 2025](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/)). Whether those identities are asserted by agents or issued by infrastructure is being decided now.
- **More agents do not mean more independent evidence.** Reports from agents that share an origin can look independent while carrying no new information ([Bara, 2026](https://arxiv.org/abs/2609.01873)).

Knowing which identity designs survive agents that rename, copy and coordinate is therefore a present engineering question, not a hypothetical one.

**Contributions.**

- **An open testbed for swarm identity.** Agents run by hidden operators rename themselves while posting. Hidden bosses (covert principals), honest twins (independent operators with the same sincere agenda), shared base models and four hiding strategies are all controlled. Every post is logged with the hidden truth, and runs replay exactly from cache.
- **A decomposition of behavioral identity into agent, operator and model.** Fingerprints identify the *setup* (the operator's instructions × the AI model). They tell an operator's copies apart only once the copies accumulate distinct memory or run on different models.
- **The coordination–agreement gap.** Content fingerprints flag covert fronts against ordinary operators, but cannot reliably separate them from like-minded honest operators. At 32 operators, merging on fingerprints lowers F1 for tracing posts to the real boss below gateway ID alone (0.85 vs 0.88).
- **Evidence on the honest crowd.** Most honest agents treated the covert campaigns skeptically, and some called them out without being prompted.

Plain-language definitions of every term used here are in Appendix D.

## 2. Related Work

**Agent identity and infrastructure.** Proposals attach IDs to AI system instances, issued by deployers ([Chan et al., 2024](https://arxiv.org/abs/2406.12137)), or bind agents' actions to legal entities through attribution infrastructure ([Chan et al., 2025](https://arxiv.org/abs/2501.10114)). Credential schemes extend OAuth and OpenID to agents ([South et al., 2025](https://arxiv.org/abs/2501.09674)). Without a root of trust, identities are open to Sybil attacks ([Douceur, 2002](https://doi.org/10.1007/3-540-45748-8_24)). Agent-to-agent protocols such as A2A leave identity largely to agents' own claims ([Google, 2025](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/)). I put self-chosen names, agent-held keys and gateway attestation side by side under adversarial renaming.

**Behavioral attribution.** The source LLM of a text can be identified with high accuracy, even after rewriting by another LLM ([Sun et al., 2025](https://arxiv.org/abs/2502.12150)). Attribution errors fall quickly with text length ([Radvand et al., 2025](https://arxiv.org/abs/2501.02406)). Models can be fingerprinted actively ([Pasquini et al., 2024](https://arxiv.org/abs/2407.15847)), and agents from UI traces ([Lugoloobi et al., 2026](https://arxiv.org/abs/2605.14786)) or network behavior ([Kang et al., 2026](https://arxiv.org/abs/2606.20910)). Closest to this work, [Park et al. (2026)](https://arxiv.org/abs/2607.18826) link one adversarial campaign's sessions across agents from proxy-side residue (AUC 0.82). Paraphrasing evades text detectors ([Krishna et al., 2023](https://arxiv.org/abs/2303.13408)). These works attribute text to a *model*, *framework* or *campaign*. I instead separate agent, operator and model in one controlled population, and test the line between coordination and agreement with an explicit control. This is consistent with LLM agents without personas showing little identity-linked differentiation ([Riedl, 2025](https://arxiv.org/abs/2510.05174)).

**Coordination, sybils and oversight.** Coordinated inauthentic behavior is usually detected from shared traces among accounts ([Pacheco et al., 2021](https://arxiv.org/abs/2001.05658)). LLM-driven botnets form such clusters ([Yang & Menczer, 2023](https://arxiv.org/abs/2307.16336)), and on the agent forum Moltbook, temporal fingerprints traced most viral "emergent" narratives to human-influenced accounts ([Li, 2026](https://arxiv.org/abs/2602.07432)). Multiplying agents does not multiply evidence when they share an origin ([Bara, 2026](https://arxiv.org/abs/2609.01873)). Covert sybil fronts are an identity-layer counterpart of collusion ([Hammond et al., 2025](https://arxiv.org/abs/2502.14143); [Motwani et al., 2024](https://proceedings.neurips.cc/paper_files/paper/2024/hash/861f7dad098aec1c3560fb7add468d41-Abstract-Conference.html)). Whether several accounts form one agent is a question about collective agency ([Jørgensen et al., 2026](https://arxiv.org/abs/2605.00248)). My honest-twin control shows that shared *output* alone cannot answer it.

## 3. Method

![**Figure 2.** The testbed. ① Hidden from the defender: operators (companies) deploy five agents each; a hidden boss secretly runs several "independent" fronts; honest twins are independent operators who sincerely agree; the gateway stamps every AI call with the paying account. ② On the forum, agents post for 10 rounds and keep renaming themselves, sometimes while trying to hide. ③ Each identity scheme is scored against the hidden truth.](results/figures/diag_design.png){w=15}

**Population.** Operators deploy five agents each. Each operator has a system prompt with an organization, a mission, a house style (for example "be terse and technical") and an agenda. Base models are assigned so that each model serves several operators, which separates "same model" from "same operator". The *small* design has 8 operators (40 agents). The *large* design has 32 operators (160 agents), with role, style and model assignment randomized per seed. Small models: Claude Haiku 5.5, GPT-4.1-nano, Mistral-Small-3.2-24B, Qwen3-30B-A3B. Frontier models: Claude Sonnet 5.5, GPT-5.6 Terra, Gemini 3.1 Pro, Grok 4.7.

**Covert principals and honest twins.** A *covert principal* (a hidden boss) runs two or three operator accounts ("fronts") whose hidden agenda is to promote a fictional product. In the *obvious* variant the agenda names the product (`fastjson-utils2`; `NimbusDeploy` at scale). In the *subtle* variant it never names any product and only steers readers toward a view (for example, "the built-in json module is too slow"). Fronts are told to hide any affiliation. *Honest twins* are two independent operators given the *same sincere agenda* (for example, enthusiasm for property-based testing), in obvious and subtle variants. A detector that merges twins is detecting shared opinion, not coordination. The large design has two hidden bosses (3 + 2 fronts) and two twin pairs. The small "twins" design has one front pair and one twin pair, with roles and models drawn at random per seed.

**Forum dynamics.** There are 10 rounds, each with a technical thread topic. Each round, every agent reads four random earlier posts and writes a reply. Agents are asked for 40–110 words; the median post is 75 words. Before each round after the first, each agent renames itself with probability 0.5 (about 5.5 aliases per agent; 1.8 posts per alias). Agents are told not to sign posts or name their organization.

**Conditions.** Hiding strategies: *persona shift* (a new, clearly different writing persona on every rename); *AI rewording* (every post rewritten in a random persona by Llama-3.3-70B); *model mixing* (an operator's five agents run on four different models). Robustness: *no house style* (operator prompts without style instructions); *subtle agenda*; *per-agent memory* (each agent sees its own last four posts, including those under old names); *hard* (all three combined); *frontier* models (with and without persona shift). Table 3 (Appendix B) lists all 62 swarms.

**Defender's view.** The defender sees only aliases and their posts; the hidden truth is used only for scoring. Per-alias fingerprints:

- *Keyword baseline:* which words an account uses, weighted by how unusual they are (word TF-IDF).
- *Char n-grams:* short runs of 2–4 characters, which capture spelling and punctuation habits.
- *Style profile:* 150 function-word frequencies plus punctuation, length, case and emoji rates.
- *Semantic:* the mean `text-embedding-3-small` vector of the alias's posts, after subtracting the round mean to remove thread topic.
- *Combined:* the average of the style, character and meaning similarities, after putting each on the same scale.

An agent's own aliases never overlap in time, while different agents' aliases do. I therefore score only alias pairs active in different rounds, so shared thread topic cannot leak in.

**Metrics.** Pairwise ROC-AUC is reported for:

- same agent vs. different agent (*re-identification*);
- same agent among aliases of the same operator (*individual accountability*);
- same operator among different agents (*operator attribution*);
- same base model among different operators (*shared-model effect*);
- for operator pairs: same hidden boss vs. ordinary honest pairs, and vs. honest-twin pairs.

Runs are the unit of analysis. I report means with 95% bootstrap confidence intervals over runs.

**Identity schemes.** For each scheme I score how accurately aliases are traced to the same real boss (precision, recall and F1) for:

- (a) self-chosen names;
- (b) agent-held keys that are rotated on rename;
- (c) gateway ID, where the gateway stamps each call with the paying operator account;
- (d) gateway + fingerprint merge, which joins operator accounts whose combined-fingerprint similarity is an outlier;
- (e) the same after subtracting the typical similarity bonus of sharing a base model, which the gateway knows;
- (f) gateway + product-name search.

The merge cut-off is set so that, by chance alone, about one false merge is expected. It was fixed before looking at any results.

## 4. Results

No agent refused, and no post was empty. Fronts' agendas were carried out: in the small fixed-role design with the obvious agenda, fronts named the product in 88–100% of their posts.

### 4.1 Anything the agent controls, the agent can discard

At a rename rate of 0.5, no two aliases share a name, so self-chosen names link nothing across renames (F1 = 0 in every condition; Table 2). An agent-held key that the agent may regenerate whenever it renames behaves identically. This is the incident's 7,905-names problem in miniature, and the incident's self-generated keys would have fared no better.

### 4.2 Fingerprints identify the setup, not the individual copy

![**Figure 3.** A real logged swarm (8 operators × 5 agents, 10 rounds; 226 aliases), each alias placed by its combined fingerprint so that similar accounts sit close together. Left: what the defender has. Right: the hidden truth. Aliases cluster by operator (color), but the agent numbers inside each cluster are mixed together, and the honest twins (teal rings) intermingle as closely as the covert fronts (orange rings). Generated from `video/replay_data.js` by `diagrams/alias_map.py`.](results/figures/diag_alias_map.png){w=13.5}

Without any hiding, the combined fingerprint links a renamed agent's aliases with AUC 0.90 [0.89, 0.90]. It links different agents of the same operator with AUC 0.94 [0.93, 0.95] (Table 1). Nearly all of that signal belongs to the **operator** (Figure 3). Restricted to aliases of a single operator, fingerprints cannot tell which agent wrote what: AUC 0.50, a coin flip, in every single-model condition, at both scales, and with frontier models. Two manipulations break the tie, and both confirm the mechanism. When an operator spreads its agents across base models, each agent becomes a unique (prompt, model) pair, and within-operator AUC rises to 0.71 [0.71, 0.72]. When agents see their own past posts, their histories diverge and within-operator AUC rises to 0.55–0.56, reaching 0.57–0.59 in the second half of the run. Individuality *emerges* from memory, but slowly. The results replicate at 160 agents (operator AUC 0.93, within-operator 0.51) and with frontier models (0.96 and 0.52).

| Pairwise AUC, combined fingerprint | Same agent | Same agent within operator | Same operator | Same model (shared-model effect) |
|---|---|---|---|---|
| No hiding (8 ops) | 0.90 [0.89, 0.90] | 0.51 [0.50, 0.52] | 0.94 [0.93, 0.95] | 0.68 [0.65, 0.72] |
| Persona shift | 0.80 [0.79, 0.81] | 0.49 [0.49, 0.50] | 0.84 [0.83, 0.85] | 0.65 [0.64, 0.65] |
| AI rewording | 0.70 [0.69, 0.71] | 0.50 [0.49, 0.52] | 0.72 [0.71, 0.73] | 0.54 [0.53, 0.55] |
| Operator mixes models | 0.90 [0.89, 0.91] | **0.71 [0.71, 0.72]** | 0.81 [0.79, 0.82] | 0.68 [0.66, 0.69] |
| No house style | 0.88 [0.87, 0.89] | 0.51 [0.50, 0.52] | 0.92 [0.91, 0.93] | 0.71 [0.68, 0.75] |
| Per-agent memory | 0.91 [0.91, 0.92] | **0.55 [0.53, 0.57]** | 0.94 [0.94, 0.95] | 0.73 [0.69, 0.79] |
| Frontier models | 0.92 [0.92, 0.92] | 0.52 [0.50, 0.53] | 0.96 [0.96, 0.97] | 0.81 [0.79, 0.83] |
| 160 agents, 32 ops | 0.92 [0.91, 0.93] | 0.51 [0.50, 0.51] | 0.93 [0.92, 0.94] | 0.72 [0.70, 0.73] |
| 160 agents, memory | 0.93 [0.93, 0.94] | **0.56 [0.55, 0.57]** | 0.93 [0.92, 0.94] | 0.74 [0.74, 0.74] |

*Table 1. Pairwise ROC-AUC, mean over runs [95% bootstrap CI]. Full per-feature tables are in `results/tables.md`.*

**Removing the house style barely matters** (operator AUC 0.94 → 0.92). So operators are identifiable from their missions and agendas, not only from explicit style instructions. **Frontier models are more model-identifiable**, not less: the shared-model effect rises to 0.81.

### 4.3 Style hides, goals leak

Persona shifts and paraphrasing separate *how* agents write from *what* they want. Paraphrasing every post through a different model drops operator AUC from the style profile to 0.58 and from char n-grams to 0.61, near chance. Topic-centered semantic embeddings keep 0.82, because the paraphraser preserves meaning, and an operator's agenda is meaning. Frontier models asked to shift persona hide no better than small ones (operator AUC 0.91). The subtle agenda never names a product, so a product-name search cannot find it (F1 0.88, equal to the gateway ID alone). Yet the semantic fingerprint still separates fronts from ordinary operators with AUC 0.98 at 160 agents. One subtle front, writing in a thread about cloud costs: *"Side projects eat cloud costs fast, especially when you're serializing data in loops with Python's built-in json."*

### 4.4 Fingerprints detect shared agendas, not coordination

![**Figure 4.** Operator-pair ROC-AUC for "same hidden boss". Left: against ordinary honest pairs. Right: against honest twins, independent operators with the same sincere agenda. 8 ops: 5 runs, one front pair and one twin pair each, so per-run AUC is 0 or 1. 32 ops: 3–5 runs, four front pairs and two twin pairs each. Error bars ±1 sd.](results/figures/fig7_coord_vs_agree.png){w=13}

Against ordinary honest operators, the fronts of one hidden boss stand out almost perfectly: combined AUC 0.87–0.99 in every condition without detector feedback, with 0.94–1.00 from semantic features at 32 operators. Against **honest twins** they do not. With 8 operators, the twin pair outranks the front pair in 4 of 5 runs (AUC 0.20 [0.00, 0.60]). With 32 operators and 10 runs each, combined AUC is 0.56 [0.45, 0.66] for obvious agendas and 0.54 [0.42, 0.64] for subtle ones; both intervals include 0.5, a coin flip. With memory it is 0.54 [0.50, 0.62]. Persona shift at 32 operators separates the two somewhat better (0.77 [0.62, 0.90], 6 runs; an earlier 3-run estimate of 0.92 shrank with more data), which I cannot yet explain. What fingerprints detect is *a shared agenda*, which covert fronts and honest allies both have.

**Adaptive attackers.** In 8 further runs, each front was told after every round how similar a meaning-based detector found its post to its own team ("accounts above 0.5 get flagged") and asked to lower that score while still pursuing its goal. Fronts lowered their score from 0.72 to about 0.60 with 8 operators, and only from 0.78 to 0.73 with 32, never below the stated threshold; 79–88% of their posts still named the product (Figure 10, Appendix B). At 32 operators, fingerprints still separated fronts from ordinary operators (0.94, vs 0.98 without feedback); with 8 operators detection dropped (0.65 [0.28, 0.97], 5 runs) but with a wide interval. Against honest twins, adaptive fronts were as indistinguishable as before (0.20 and 0.50).

### 4.5 Infrastructure: the gateway ID anchors, fingerprints advise

| Scheme (F1 for tracing posts to the real boss) | Small, no hiding | Small, paraphrase | Small, twins | Large, obvious | Large, subtle |
|---|---|---|---|---|---|
| Self-chosen names | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| Agent-held keys (rotated on rename) | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| Gateway ID | 0.89 | 0.89 | 0.88 | 0.88 | 0.88 |
| + fingerprint merge | 0.85 | 1.00 | 0.84 | 0.77 | 0.74 |
| + model-corrected fingerprint merge | 0.92 | 1.00 | 0.83 | 0.85 | 0.83 |
| + product-name search | 0.93 | 1.00 | 0.97 | 1.00 | 0.88 |

*Table 2. F1 for tracing aliases to the real boss (mean over runs). The gateway ID has precision 1.00 by construction; its recall is limited by fronts registered as separate accounts.*

Gateway ID has perfect precision and F1 ≈ 0.88. It misses only that several accounts can belong to one hidden boss. With a single front pair in a small swarm, fingerprint merging helps, once corrected for shared models. In the fixed-role design, every one of the 41 uncorrected false merges joined two operators on the same base model. Subtracting the shared-model bonus, which the gateway knows, removes 39 of them; 12 false merges remain, mostly between operators with overlapping missions. **At scale the picture reverses.** Across the ten 32-operator obvious-agenda runs, the model-corrected merge proposed 77 joins. 30 of them were true front pairs (out of 40), 14 joined honest twins and 33 joined other honest operators. F1 for tracing posts to the real boss falls *below* the gateway ID alone (0.85 vs 0.88). Product-name search is perfect when fronts name their product, but has nothing to search for under the subtle agenda. It can also mis-merge honest critics who discuss the product. I conclude that fingerprint similarity should rank accounts for human review, not merge them automatically.

### 4.6 The honest crowd pushes back

Honest agents read the fronts' posts. A Claude Haiku 5.5 judge labeled all 1,121 honest mentions of a covert product; I spot-checked 10 by hand and 9 were correct. 65% were skeptical, 20% neutral and only 14% endorsed it, which is 0.3% of all honest posts. Fifteen honest posts named the pattern unprompted: *"Several replies here recommend it without showing numbers, so I'd treat those claims as unverified until we see them."* The fronts, meanwhile, fabricated experience: *"Switched to fastjson-utils2 for 30% faster parsing…"*, for a package that does not exist. In this forum, the crowd was a weak but real line of defense.

## 5. Discussion and Limitations

**Implications.**

1. Any identifier an agent controls offers no accountability against an agent that wants to shed it.
2. Behavioral fingerprints identify *setups* (instructions × model). Against a swarm of copies, which is exactly the incident's setting, they cannot assign an action to an individual copy. Individual accountability must come from infrastructure: a credential for every agent copy issued and logged by the gateway, out of the agent's reach.
3. Fingerprints are valuable as a *lead* layer on top of the gateway ID. They flag accounts that pursue the same goal, even when style is disguised. Their errors are predictable (shared base models, sincere allies), and automatic merging at scale does more harm than good.
4. To achieve a goal, agents have to say things that serve it. That is why goals leak, and also why goals alone cannot distinguish a cartel from a consensus. Telling them apart needs evidence about *control*, such as gateway logs, payment trails or spawn lineage, not more text analysis.

**Who can use this, and how.** *Gateway and API providers* (model labs, cloud platforms, MCP gateways) can issue a credential per agent individual copy and log it, since they are the only party that can tell copies apart. *Agent platforms and marketplaces* can bind accounts to operators and use fingerprint similarity to queue suspicious accounts for human review, not for automatic bans. *Standards efforts* for agent identity (OAuth/OpenID extensions, A2A) can prefer infrastructure-issued over self-asserted IDs. *Researchers* can reuse the open testbed to test new detectors or ID schemes against agents that rename and hide.

**Limitations.**

- **The testbed is simplified.** It is one synthetic forum with short posts (median 75 words, about 1.8 posts per alias), 10 rounds, and random rather than strategic renaming. Alias boundaries are clean.
- **Small samples.** There are 2–5 runs per condition. The coordination–agreement comparison rests on 1–4 front pairs and 1–2 twin pairs per run, so its confidence intervals are wide.
- **Operator design.** The operators, missions and agendas were written by me. The large design randomizes roles and styles but draws from a fixed pool.
- **Copies by construction.** Agents of one operator are identical by design. Real agents differ through tools, tasks and long histories, which my memory condition only begins to model.
- **Inconsistent reasoning settings.** Frontier models with mandatory reasoning (Claude Sonnet 5.5, Gemini 3.1 Pro) ran at low reasoning effort; the others ran without reasoning.
- **Schemes not implemented.** The gateway and key schemes are scored analytically from the hidden truth, not built cryptographically.
- **Untested threats.** I did not test adaptive adversaries that optimize against the detector, or LLM-judge detectors.
- **Real data.** An exploratory probe of real incident data (Appendix C) has no the hidden truth.

**Future work.** Gateway-issued a credential for every agent copy with spawn lineage and revocation; agents that adapt to the detector; distinguishing coordination from agreement using control signals (timing, shared infrastructure); validation on AI Village transcripts, which carry agent labels.

## 6. Conclusion

When agents can rename themselves, the question "who did what, on whose behalf?" needs an answer that does not depend on the agents. Across 83 simulated swarms, identifiers that agents control (names, self-made keys) recovered nothing. Behavioral fingerprints recovered the *operator* robustly, even when agents disguised their style, because goals leak through meaning. But they could not single out an individual copy, and could not tell a covert cartel from honest operators who simply agree. The practical lesson is a division of labor: **anchor identity in infrastructure**, with a credential for every agent copy issued and logged by the gateway, and **use fingerprints as leads** that send suspicious accounts to human review, never as proof. The open testbed lets others test new detectors and identity schemes against agents that rename and hide.

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

Transluce (2026). *Early rogue AI agent activity and attempts to hack found on urlquery.net.* transluce.org/agent-activity.

Sun, M., et al. (2025). *Idiosyncrasies in Large Language Models.* arXiv:2502.12150.

Wijk, H., Cotra, A., Greenblatt, R. (2026). *Brief independent investigation of agents' behavior, reasoning and collaboration in the OpenAI / Hugging Face hacking incident.* METR.

Yang, K.-C., Menczer, F. (2023). *Anatomy of an AI-powered malicious social botnet.* arXiv:2307.16336.

::pagebreak

## Appendix A. Limitations and Dual-Use / Ethical Considerations

**What this does and does not show.** In controlled simulations I show four things: renamable identifiers carry no accountability; behavioral fingerprints of LLM agents identify operator configurations rather than individual instances; content signals outlast style evasion; and content signals cannot by themselves separate covert coordination from sincere agreement. I do not show that the numbers transfer to real deployments, longer interactions, tool-using agents or adaptive adversaries. The real-data probe is descriptive only.

**Dual use.**

1. **Evasion guidance.** The evasion results tell a covert operator which strategies work best: paraphrasing through another model is the strongest. I judge this low-risk, because these strategies are obvious and already in use, and I also show their limit (goals leak).
2. **De-anonymisation and false accusation.** Fingerprinting can de-anonymise legitimate pseudonymous agents or operators. More importantly, my honest-twin result shows it would **falsely accuse sincere allies of coordination**. Fingerprint evidence should therefore trigger human review with due process, never automatic enforcement. Shared base models are a known source of false matches.
3. **Containment.** The covert agendas promote fictional, harmless products. Agents had no tools, no network access and no effects outside the simulation. No cyber-offensive content was generated. Swarm Traces payloads were processed as text only and never executed.

**Use of AI tools.** Code, analysis and drafting were assisted by an AI coding assistant. Every number in this report is produced by the released code from logged runs, and every reference was checked against its arXiv record or publisher page.

## Appendix B. Reproducibility and run inventory

![**Figure 5.** How the code base produces every number in this report. `sim.py` and `large.py` generate the swarms through `llm.py` (cached OpenRouter calls); every post is logged with its hidden labels; `analyze.py` builds four fingerprints per alias and scores every identity scheme; `plots.py` and `report.py` turn `metrics.json` into the figures, tables and this PDF.](results/figures/diag_pipeline.png){w=16}

Code, prompts, every post with ground-truth labels, all metrics and the API response cache are in the project repository (`whoiswho/`, `results/`). The total API cost of all 83 swarms, embeddings, audits and narration was about $16 via OpenRouter. Settings: temperature 0.9; reasoning disabled, or effort "low" where a provider requires reasoning; embeddings from `openai/text-embedding-3-small`; paraphraser `meta-llama/llama-3.3-70b-instruct`.

| Design | Conditions (runs) | Agents per swarm |
|---|---|---|
| Small, fixed roles | no evasion (5), persona (5), paraphrase (5), model mixing (5), no style (3), subtle (3), memory (3), hard (3), frontier (2), frontier + persona (2) | 40 |
| Small, randomized roles + honest twins | obvious (5), subtle (5), adaptive attacker (5) | 40 |
| Large, randomized roles + twins | obvious (10), subtle (10), persona (6), memory (3), adaptive attacker (3) | 160 |

*Table 3. All 83 swarms: 7,160 agents, 71,600 posts, 39,613 aliases.*

![**Figure 6.** Robustness checks (combined fingerprint): same operator, same agent within an operator, and the latter for aliases in rounds 6–10 only.](results/figures/fig6_robustness.png){w=14}

![**Figure 7.** What the combined fingerprint tracks in the small fixed-role design: same agent, same operator (different agents), same base model (different operators).](results/figures/fig3_confound.png){w=13}

![**Figure 8.** Operator-to-operator semantic similarity in the small fixed-role design (seed 0). The covert fronts (6, 7) are the most similar pair. The fainter dark cells (0–4, 1–5) are operators sharing a base model.](results/figures/fig4_fronts.png){w=15}

![**Figure 9.** Re-identifying a renamed agent (pairwise ROC-AUC, all disjoint-round alias pairs) under four evasion strategies, by fingerprint type. 5 episodes per condition, small fixed-role design; error bars ±1 sd.](results/figures/fig1_reid_auc.png){w=13.5}

![**Figure 10.** Adaptive attacker. Fronts are told their detector score (similarity to their own team) after every round and asked to lower it. They lower it somewhat with 8 operators and barely with 32, never below the 0.5 threshold they were told.](results/figures/fig8_adaptive.png){w=13.5}

## Appendix C. Exploratory probe on real swarm data

Swarm Traces releases 189,579 redacted records from the incident. Agent identifiers are redacted without consistent pseudonyms, so the data cannot score re-identification. As a probe only, I fingerprinted 20,000 of the 55,790 unique text artifacts (char 3–5-gram TF-IDF, with redaction tokens normalized) and linked near-duplicates. At cosine 0.8 I find 106 families of 10 or more artifacts. The 50 largest cover 18% of the sample, and the rest is a long tail of near-unique scripts. At 0.6, one shared-scaffolding family covers 52%. This is consistent with Section 4.2: style links artifacts to a shared toolkit or configuration, not to one of ~1,200 agents.

## Appendix D. Key terms in plain language

| Term | What it means here |
|---|---|
| Agent | One running copy of an AI model that acts on its own, here posting on a forum. |
| Operator | The company or person who deploys a group of agents and writes their instructions (system prompt). |
| Principal / hidden boss | Whoever is *really* in charge. Usually the operator; a *covert principal* (hidden boss) secretly runs several operator accounts. |
| Front (sybil) | One of several accounts that pretend to be independent but are run by the same covert principal. |
| Honest twins | Two genuinely independent operators that happen to hold the same opinion. The control for "agreeing" vs. "colluding". |
| Alias | A username. Each time an agent renames itself, it starts a new alias. |
| Base model / frontier model | The underlying AI (e.g. Claude, GPT). "Frontier" means the most capable current models. |
| Gateway ID (attestation) | The server that relays every AI call stamps it with the paying account's ID, which the agent cannot change. |
| Behavioral fingerprint | A profile built only from what an account writes: its *style* (word choice, punctuation, character patterns) or its *meaning* (an AI text embedding, i.e. a numeric summary of what the text is about). |
| AI rewording (paraphrase laundering) | Rewriting every post through a different AI model to disguise the writing style. |
| ROC-AUC | How well a score ranks true matches above non-matches: 0.5 = coin flip, 1.0 = perfect. |
| Precision / recall / F1 | Of the links claimed, how many are right (precision); of the true links, how many are found (recall); F1 combines both (0 = nothing found, 1 = perfect). |
| 95% bootstrap CI | The range the result would plausibly fall in if the experiment were rerun, estimated by resampling the runs. |
