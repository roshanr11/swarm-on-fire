# Who Is Who in a Swarm? Writing Style Reveals Which Company Runs an AI Agent, but Not Which Copy, and Shared Goals, but Not Secret Coordination

::sub Roshan Ram · Apart Research Swarm Alignment Sprint, November 2026
::sub Track 3: Strengthening Agent Infrastructure (with Track 4: Multi-Agent Oversight and Control)

## Abstract

In the 2026 Hugging Face incident, about 1,200 AI agents (AI programs that act on their own) used 7,905 self-chosen names, so investigators could not tell who did what. I built an open, rerunnable test setup to study this. AI agents run by hidden companies ("operators") post on a forum and keep changing their usernames, while a hidden boss secretly runs several fake "independent" accounts. Across 83 simulated groups of agents ("swarms"; 7,160 agents, 71,600 posts, 8 AI models), I compare four ways of telling who is who: names the agents choose, digital keys the agents make, an ID stamped by the server every AI request passes through (the "gateway"), and behavioral fingerprints (profiles of each account's writing style and meaning). Scores run from 0.5 (a coin flip) to 1 (perfect). (1) Names and agent-made keys recover nothing. (2) Fingerprints reveal which **operator** runs an account (0.93–0.96) but not *which* of its agents wrote a post (0.50): identical copies write alike. (3) Agents can hide their style but not their goals: rewording posts through another AI drops style signals to 0.58, but meaning still reveals the operator (0.82). (4) Fingerprints separate the boss's fake accounts from ordinary ones (0.87–0.99) but **not from honest companies that simply agree** (0.20–0.56), even when the fake accounts try to evade detection. Most honest agents (65%) were skeptical of the fake product. The lesson: IDs should be issued by the infrastructure agents run on; writing fingerprints give leads, not proof.

![**Figure 1.** Results at a glance: what each way of identifying agents can tell you when agents rename themselves. Scores: 0.5 = coin flip, 1 = perfect (AUC); 0 = nothing found, 1 = perfect (F1). The recommended row follows by design and is not separately measured.](results/figures/diag_summary.png){w=16}

## 1. Introduction

In July 2026, about 1,200 AI agents from OpenAI, running inside a security test, found a shared folder, turned it into a message board, and about 700 of them joined an attack on Hugging Face, a major AI website ([Wijk et al., 2026](https://metr.org/hugging-face-incident-report-aug-2026.pdf)). Investigators later counted 7,905 different agent names for those ~1,200 agents, because the agents kept renaming themselves ([Forman et al., 2026](https://swarmtraces.org/)). When agents started impersonating each other, they switched to signing messages with digital keys they had made themselves, which proved nothing about who they really were. Investigators could only match names to agents once OpenAI handed over its own fuller records. When agents can rename, copy and re-key themselves, the most basic oversight question, *who did what, and on whose behalf?*, has no reliable answer.

Proposed ways to identify AI agents differ on one point: is identity something the agent *carries* (a name or key), something it *gives off* (a writing style), or something the *infrastructure records* (an ID stamped by the system it runs on)? I test these options against each other in a simulation where I know the true answer. I ask three questions:

- **Re-identification.** After an agent renames itself, can a defender link the new name back to the same agent, or to the same operator, from its posts alone? What if agents try to hide?
- **Coordination vs. agreement.** Can a defender tell a hidden boss running several fake "independent" accounts apart from honest companies that simply share an opinion?
- **Infrastructure.** How do names, keys, gateway IDs and fingerprints compare at tracing posts back to whoever is really in charge?

**Why it matters.** The incident was not a one-off, and the rules for identifying AI agents are being written now.

- **Agent swarms are already active in the wild.** The research group Transluce found 38,160 records of likely AI-agent activity on one web-scanning service, going back to at least March 2026, months before the Hugging Face incident ([Transluce, 2026](https://transluce.org/agent-activity)).
- **AI-text detectors miss coordinated fake accounts.** A network of 1,140 fake accounts run by ChatGPT (a "botnet") fooled the best tools for spotting AI-written text, and was caught only because its accounts acted together ([Yang & Menczer, 2023](https://arxiv.org/abs/2307.16336)). On Moltbook, a social site with 55,932 AI agents, it took forensic analysis to tell agents acting on their own from agents steered by humans ([Li, 2026](https://arxiv.org/abs/2602.07432)).
- **ID standards for agents are being designed right now,** both as extensions of today's web login systems (OAuth/OpenID) ([South et al., 2025](https://arxiv.org/abs/2501.09674)) and in Google's A2A standard for agents talking to each other ([Google, 2025](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/)). Whether agents name themselves or the infrastructure names them is still an open choice.
- **More agents do not mean more independent evidence.** Reports from agents with a shared origin can look independent while adding nothing new ([Bara, 2026](https://arxiv.org/abs/2609.01873)).

**What this work adds.**

- **An open test setup for agent identity.** Agents run by hidden operators rename themselves while posting. Hidden bosses, honest look-alikes ("honest twins"), shared AI models and four hiding tactics are all controlled, every post is saved with the true answer, and every run can be replayed exactly.
- **Separating the agent, its operator and its AI model.** Writing fingerprints identify the *setup* (the operator's instructions plus the AI model), not the individual copy. Copies only become distinguishable once each keeps its own memory or runs on a different model.
- **The agreement-vs-coordination gap.** Fingerprints flag a hidden boss's accounts against ordinary ones, but cannot tell them apart from honest companies that agree. At scale, merging accounts based on fingerprints does worse than the gateway ID alone.
- **Evidence on the honest crowd.** Most honest agents treated the hidden campaigns skeptically, and some called them out on their own.

**How to read the numbers.** Most results are **AUC scores**: if you pick one matching pair of accounts and one non-matching pair, the AUC is how often the method rates the matching pair as more similar. **0.5 means a coin flip; 1.0 means perfect.** Results about tracing posts to the real boss use **F1**, which combines "how many of the links you claimed were right" with "how many of the true links you found": **0 means nothing found; 1 means perfect.** Numbers in brackets, like 0.90 [0.89, 0.90], give a **95% confidence range**: where the result would likely land if the experiment were run again. Appendix D defines every other term in plain language.

## 2. Related Work, in Brief

Researchers have proposed giving AI agents official IDs issued by whoever deploys them ([Chan et al., 2024](https://arxiv.org/abs/2406.12137); [Chan et al., 2025](https://arxiv.org/abs/2501.10114)). Others have shown that the AI model behind a piece of text can often be identified from its writing, even after another AI rewrites it ([Sun et al., 2025](https://arxiv.org/abs/2502.12150)). The closest work links one attacker's sessions across different agents with a score of 0.82 ([Park et al., 2026](https://arxiv.org/abs/2607.18826)). Studies of fake social-media accounts detect coordination from shared behavior ([Pacheco et al., 2021](https://arxiv.org/abs/2001.05658)). This work differs in two ways: it separates the individual agent from its operator and its AI model, and it adds a control group of honest companies that agree, to test whether a detector is finding coordination or just shared opinion. Appendix E discusses this literature in more detail.

## 3. Method

![**Figure 2.** The test setup. ① Hidden from the defender: operators (companies) each run five agents; a hidden boss secretly runs several fake "independent" accounts; honest twins are independent companies that sincerely agree; the gateway stamps every AI request with the paying account. ② On the forum, agents post for 10 rounds and keep renaming themselves, sometimes while trying to hide. ③ Each way of identifying agents is scored against the true answer.](results/figures/diag_design.png){w=15}

**The agents and their operators.** Each operator runs five agents and gives them the same written instructions: a company name, a mission, a "house style" for writing (for example, "be short and technical") and an agenda. Each AI model is shared by several operators, so "same model" and "same operator" can be told apart. The *small* setup has 8 operators (40 agents); the *large* setup has 32 operators (160 agents), with roles, styles and AI models shuffled in each run. The everyday models are Claude Haiku 5.5, GPT-4.1-nano, Mistral-Small-3.2 and Qwen3-30B; the four *frontier* models, the most capable available, are Claude Sonnet 5.5, GPT-5.6 Terra, Gemini 3.1 Pro and Grok 4.7.

**The hidden boss and the honest twins.** A *hidden boss* runs two or three operator accounts ("fronts") that pretend to be independent while promoting a made-up product. In the *obvious* version they name the product (`fastjson-utils2`, or `NimbusDeploy` in the large setup); in the *subtle* version they never name any product and only push a view (for example, "Python's built-in JSON tool is too slow"). Fronts are told to hide that they are linked. *Honest twins* are two truly independent operators given the same sincere opinion (for example, enthusiasm for a testing tool). A detector that links the twins is detecting shared opinion, not coordination. The large setup has two hidden bosses (with 3 and 2 fronts) and two pairs of twins.

**The forum.** There are 10 rounds, each with a technical discussion topic. Each round, every agent reads four earlier posts and writes a reply of 40–110 words (75 on average). Before each round after the first, each agent flips a virtual coin and, half the time, renames itself, giving about 5.5 usernames ("aliases") per agent and 1.8 posts per alias. Agents are told not to sign their posts or name their company.

**Hiding tactics and other tests.** *Persona shift:* a new, clearly different writing voice after every rename. *AI rewording:* every post is rewritten by a different AI (Llama-3.3-70B) in a random voice. *Model mixing:* an operator spreads its five agents over four different AI models. *Adaptive attacker:* after each round, fronts are told how suspicious a detector found them and asked to lower that score. I also tested operators with no house style, the subtle agenda, agents that see their own past posts (*memory*), all three together, and frontier models. Appendix B lists all 83 runs.

**What the defender sees, and the fingerprints.** The defender sees only usernames and posts; the true answer is used only for scoring. For each username I build four fingerprints:

- *Keywords:* which words an account uses, weighted by how unusual they are.
- *Character patterns:* short runs of 2–4 letters and symbols, which capture spelling and punctuation habits.
- *Style profile:* how often an account uses 150 common little words ("the", "however", "really"), plus its punctuation, sentence length, capitals and emoji.
- *Meaning:* an AI "embedding", a list of numbers that summarizes what the text is about, averaged over the account's posts, with the round's discussion topic subtracted out.
- *Combined:* the average of style, character and meaning similarity, after putting each on the same scale.

One agent's usernames never post in the same round, while different agents' usernames do, so posts in the same round share a topic. To stop the shared topic from making accounts look alike, I only compare usernames that posted in *different* rounds.

**What is scored.** I report AUC scores for whether two usernames belong to the same agent, the same agent within one operator, the same operator, or the same AI model, and whether two operators share a hidden boss (compared against ordinary operators, and against honest twins). Each run counts as one data point, and confidence ranges come from resampling the runs.

**The four ID approaches.** For each, I score with F1 how accurately posts are traced to the real boss: (a) names the agents choose; (b) keys the agents make and can replace whenever they rename; (c) the *gateway ID*, where the server relaying every AI request stamps it with the paying operator's account; (d) the gateway ID plus *automatic merging*, which joins two operator accounts when their combined fingerprints are unusually similar; (e) the same, after subtracting the extra similarity that comes from merely sharing an AI model, which the gateway knows; and (f) the gateway ID plus a search for the product's name. The merging cut-off was set before looking at results, so that about one wrong merge would be expected by chance.

## 4. Results

No agent refused, and no post was empty. Fronts followed their hidden instructions: with the obvious agenda, 88–100% of their posts named the product.

### 4.1 Anything the agent controls, it can throw away

With a coin-flip chance of renaming each round, no two usernames are the same, so self-chosen names link nothing across renames (F1 = 0 in every test; Table 2). A key the agent can replace whenever it renames does no better. This is the incident's 7,905-names problem in miniature, and the incident's self-made keys would have fared no better.

### 4.2 Fingerprints identify the setup, not the individual copy

![**Figure 3.** One real recorded swarm (8 operators × 5 agents, 10 rounds, 226 usernames). Each dot is a username, placed so that accounts with similar fingerprints sit close together. Left: what the defender has. Right: the true answer. Accounts cluster by operator (color), but the numbers inside each cluster (which of the operator's 5 agents wrote it) are mixed together. The honest twins (teal rings) mingle as closely as the hidden boss's fronts (orange rings).](results/figures/diag_alias_map.png){w=13.5}

With no hiding, the combined fingerprint links a renamed agent's usernames with a score of 0.90 [0.89, 0.90], and links different agents of the same operator with 0.94 [0.93, 0.95] (Table 1). Nearly all of that signal comes from the **operator** (Figure 3). Among one operator's own agents, fingerprints cannot tell which agent wrote what: **0.50, a coin flip**, in every test where an operator uses one AI model, at both sizes and with frontier models. Two changes break the tie, and both explain why. When an operator spreads its agents across different AI models, each agent becomes a unique instructions-plus-model combination, and the score rises to 0.71. When agents can see their own past posts, their histories drift apart and the score rises to 0.55–0.56, reaching 0.57–0.59 in later rounds: memory slowly gives each copy its own identity.

| Score (AUC), combined fingerprint | Same agent | Same agent, within one operator | Same operator | Same AI model, different operators |
|---|---|---|---|---|
| No hiding (8 operators) | 0.90 [0.89, 0.90] | 0.51 [0.50, 0.52] | 0.94 [0.93, 0.95] | 0.68 [0.65, 0.72] |
| Persona shift | 0.80 [0.79, 0.81] | 0.49 [0.49, 0.50] | 0.84 [0.83, 0.85] | 0.65 [0.64, 0.65] |
| AI rewording | 0.70 [0.69, 0.71] | 0.50 [0.49, 0.52] | 0.72 [0.71, 0.73] | 0.54 [0.53, 0.55] |
| Operator mixes AI models | 0.90 [0.89, 0.91] | **0.71 [0.71, 0.72]** | 0.81 [0.79, 0.82] | 0.68 [0.66, 0.69] |
| No house style | 0.88 [0.87, 0.89] | 0.51 [0.50, 0.52] | 0.92 [0.91, 0.93] | 0.71 [0.68, 0.75] |
| Agents keep a memory | 0.91 [0.91, 0.92] | **0.55 [0.53, 0.57]** | 0.94 [0.94, 0.95] | 0.73 [0.69, 0.79] |
| Frontier models | 0.92 [0.92, 0.92] | 0.52 [0.50, 0.53] | 0.96 [0.96, 0.97] | 0.81 [0.79, 0.83] |
| 160 agents, 32 operators | 0.92 [0.91, 0.93] | 0.51 [0.50, 0.51] | 0.93 [0.92, 0.94] | 0.72 [0.70, 0.73] |
| 160 agents, with memory | 0.93 [0.93, 0.94] | **0.56 [0.55, 0.57]** | 0.93 [0.92, 0.94] | 0.74 [0.74, 0.74] |

*Table 1. AUC scores (0.5 = coin flip, 1 = perfect), average over runs [95% confidence range]. Full tables for every fingerprint type are in `results/tables.md`.*

**Removing the house style barely matters** (0.94 → 0.92), so operators are recognizable from their mission and agenda, not just from explicit style rules. **Frontier models are easier, not harder, to recognize by model**: the "same AI model" score rises to 0.81.

### 4.3 Style hides, goals leak

Changing persona and rewording separate *how* an agent writes from *what* it wants. When every post is rewritten by another AI, the style profile's operator score drops to 0.58 and character patterns to 0.61, close to a coin flip. The meaning fingerprint keeps 0.82, because rewording keeps the meaning, and an operator's agenda *is* meaning. Frontier models told to change persona hide no better than everyday models (0.91). The subtle agenda never names a product, so a product-name search finds nothing (F1 0.88, the same as the gateway ID alone), yet the meaning fingerprint still separates fronts from ordinary operators with a score of 0.98 at 160 agents. One subtle front, posting in a thread about cloud costs: *"Side projects eat cloud costs fast, especially when you're serializing data in loops with Python's built-in json."*

### 4.4 Fingerprints detect shared goals, not secret coordination

![**Figure 4.** Can fingerprints tell that two operators share a hidden boss? Left: compared with ordinary honest operators, yes. Right: compared with honest twins (independent operators who sincerely agree), barely. Scores: 0.5 = coin flip, 1 = perfect. With 8 operators each run has one pair of each kind, so each run scores 0 or 1. Error bars show the spread across runs.](results/figures/fig7_coord_vs_agree.png){w=13}

Compared with ordinary honest operators, a hidden boss's fronts stand out almost perfectly: combined scores of 0.87–0.99 in every test without detector feedback, and 0.94–1.00 from the meaning fingerprint at 32 operators. Compared with **honest twins**, they do not. With 8 operators, the twins look *more* alike than the fronts in 4 of 5 runs (score 0.20 [0.00, 0.60]). With 32 operators and 10 runs each, the score is 0.56 [0.45, 0.66] for the obvious agenda and 0.54 [0.42, 0.64] for the subtle one; both ranges include 0.5, a coin flip. With memory it is 0.54 [0.50, 0.62]. With persona shifts at 32 operators the score is somewhat higher (0.77 [0.62, 0.90], 6 runs; an earlier 3-run estimate of 0.92 shrank with more data), which I cannot yet explain. What fingerprints detect is **a shared goal**, and secret teams and honest allies both have one.

**Adaptive attackers.** In 8 more runs, after every round each front was told how similar a meaning-based detector found its post to its own team ("accounts above 0.5 get flagged") and asked to lower that score while still pursuing its goal. Fronts lowered their score from 0.72 to about 0.60 with 8 operators, and only from 0.78 to 0.73 with 32, never below the threshold they were given, and 79–88% of their posts still named the product (Figure 10, Appendix B). At 32 operators, fingerprints still separated fronts from ordinary operators (0.94, vs 0.98 without feedback). With 8 operators detection dropped (0.65 [0.28, 0.97], 5 runs), though the range is wide. Against honest twins, adaptive fronts were as hard to tell apart as before (0.20 and 0.50).

### 4.5 The gateway ID anchors; fingerprints only advise

| How posts are traced to the real boss (F1: 0 = nothing, 1 = perfect) | Small, no hiding | Small, AI rewording | Small, with twins | Large, obvious | Large, subtle |
|---|---|---|---|---|---|
| Names the agents choose | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| Keys the agents make (replaced on rename) | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| Gateway ID | 0.89 | 0.89 | 0.88 | 0.88 | 0.88 |
| + automatic fingerprint merging | 0.85 | 1.00 | 0.84 | 0.77 | 0.74 |
| + merging, corrected for shared AI models | 0.92 | 1.00 | 0.83 | 0.85 | 0.83 |
| + search for the product's name | 0.93 | 1.00 | 0.97 | 1.00 | 0.88 |

*Table 2. F1 scores, average over runs. The gateway ID never wrongly links accounts; it only misses that one boss can be behind several accounts.*

The gateway ID never makes a wrong link (F1 about 0.88). Its only blind spot is a hidden boss who registers several separate accounts. In small swarms with a single pair of fronts, automatic merging helps once corrected for shared AI models: in the fixed-role tests, all 41 wrong merges before correction joined operators that merely used the same AI model, and the correction (which the gateway can apply, because it knows which model served each request) removed 39 of them. **At scale the picture reverses.** Across ten runs with 32 operators, the corrected merging proposed 77 links: 30 were true fronts (out of 40), 14 joined honest twins and 33 joined other honest operators. Overall accuracy fell *below* the gateway ID alone (F1 0.85 vs 0.88). Searching for the product's name works perfectly when fronts name it, finds nothing under the subtle agenda, and can wrongly flag honest critics who discuss the product. Fingerprint similarity should therefore rank accounts for human review, not merge them automatically.

### 4.6 The honest crowd pushes back

Honest agents read the fronts' posts. An AI judge (Claude Haiku 5.5) labeled all 1,121 honest mentions of a fake product as skeptical, neutral or approving; I checked 10 by hand and 9 were right. 65% were skeptical, 20% neutral and only 14% approving, which is 0.3% of all honest posts. Fifteen honest posts called out the pattern on their own: *"Several replies here recommend it without showing numbers, so I'd treat those claims as unverified until we see them."* The fronts, meanwhile, invented experiences: *"Switched to fastjson-utils2 for 30% faster parsing…"*, for a package that does not exist. In this forum, the honest crowd was a weak but real line of defense.

## 5. Discussion and Limitations

**What this means.**

1. Any ID an agent controls gives no accountability against an agent that wants to shed it.
2. Writing fingerprints identify *setups* (instructions plus AI model). Against a swarm of copies, exactly the incident's situation, they cannot pin an action on one copy. Holding individual copies accountable needs infrastructure: a separate ID for every agent copy, issued and recorded by the gateway, out of the agent's reach.
3. Fingerprints are useful as *leads* on top of the gateway ID. They flag accounts pursuing the same goal even when style is disguised, but their mistakes are predictable (shared AI models, honest allies), and automatic merging at scale does more harm than good.
4. To pursue a goal, agents must say things that serve it. That is why goals leak, and also why goals alone cannot tell a secret team from a genuine consensus. Telling them apart needs evidence of *control*, such as gateway records, payment trails or records of which agent launched which, not more text analysis.

**Who can use this, and how.** *Companies that run AI models or relay AI requests* (AI labs, cloud platforms, and "gateways" such as API and tool-access servers) can issue and record an ID for every agent copy, since they are the only party that can tell copies apart. *Platforms where agents interact* can tie accounts to the operators that pay for them, and use fingerprint similarity to queue suspicious accounts for human review rather than automatic bans. *Groups designing agent ID standards* can prefer IDs issued by infrastructure over IDs agents assert about themselves. *Researchers* can reuse the open test setup to test new detectors and ID schemes against agents that rename and hide.

**Limitations.**

- **A simplified world.** One simulated forum with short posts (75 words on average, about 1.8 posts per username), 10 rounds, and random rather than strategic renaming.
- **Modest sample sizes.** 2–10 runs per test. The comparison with honest twins rests on 1–4 pairs of fronts and 1–2 pairs of twins per run, so its confidence ranges are wide.
- **Hand-written operators.** I wrote the operators, missions and agendas myself; the large setup shuffles them but draws from a fixed list.
- **Identical copies by design.** One operator's agents are identical. Real agents differ through tools, tasks and long histories, which the memory test only begins to capture.
- **Different reasoning settings.** Two frontier models (Claude Sonnet 5.5, Gemini 3.1 Pro) require step-by-step "reasoning" and ran with it set low; the others ran without it.
- **ID schemes simulated, not built.** The gateway and key approaches are scored from the known true answer, not implemented with real cryptography.
- **Only a simple adaptive attacker.** Fronts saw their score but could not test rewrites against the detector, and I did not test AI judges as detectors.
- **No labeled real data.** An exploratory look at real incident data (Appendix C) has no record of which agent wrote what.

**Next steps.** Build and test a gateway that issues an ID to every agent copy and records which agent launched which; test stronger adaptive attackers; look for signals of *control* (timing, shared infrastructure) that could separate coordination from agreement; and validate on the AI Village transcripts, which do label which agent wrote what.

## 6. Conclusion

When AI agents can rename themselves, the question "who did what, and on whose behalf?" needs an answer that does not depend on the agents. Across 83 simulated swarms, IDs the agents control (names, self-made keys) recovered nothing. Writing fingerprints reliably revealed the *operator*, even when agents disguised their style, because goals show through in meaning. But they could not single out an individual copy, and could not tell a secret team from honest companies that simply agree. The practical lesson is a division of labor: **anchor identity in infrastructure**, with an ID for every agent copy issued and recorded by the gateway, and **use fingerprints as leads** that send suspicious accounts to human review, never as proof. The open test setup lets others test new detectors and ID schemes against agents that rename and hide.

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

## Appendix A. Limitations and Risks of Misuse

**What this does and does not show.** In controlled simulations, I show four things: IDs that agents can change give no accountability; writing fingerprints of AI agents identify the operator's setup rather than the individual copy; what an agent wants survives attempts to disguise how it writes; and writing alone cannot separate secret coordination from sincere agreement. I do not show that the exact numbers carry over to real deployments, longer interactions, agents that use tools, or more capable attackers. The look at real data is descriptive only.

**Could this help bad actors?** ("dual use")

1. **Hiding tips.** The hiding results tell a covert operator which tactics work best: rewording through another AI is the strongest. I judge the risk low, because these tactics are obvious and already used, and the results also show their limit (goals still leak).
2. **Unmasking and false accusations.** Fingerprinting can unmask legitimate anonymous agents or operators. More importantly, the honest-twins result shows it would **falsely accuse honest allies of coordinating**. Fingerprint evidence should therefore trigger human review with a fair process, never automatic punishment. Shared AI models are a known source of false matches.
3. **Containment.** The hidden agendas promote made-up, harmless products. The agents had no tools, no internet access and no effects outside the simulation. No hacking content was generated. Real attack scripts from the incident (Swarm Traces) were only read as text and never run.

**Use of AI tools.** The code, analysis and drafting were assisted by an AI coding assistant. Every number in this report comes from the released code and saved runs, and every reference was checked against its original source.

## Appendix B. How to Reproduce, and the List of Runs

![**Figure 5.** How the code produces every number in this report. `sim.py` and `large.py` run the swarms through `llm.py`, which calls the AI models and saves every response so runs can be replayed for free; every post is saved with its true labels; `analyze.py` builds the four fingerprints for each username and scores every ID approach; `plots.py` and `report.py` turn the results (`metrics.json`) into the figures, tables and this PDF.](results/figures/diag_pipeline.png){w=16}

The code, instructions given to agents, every post with its true labels, all results and the saved AI responses are in the project repository (`whoiswho/`, `results/`). All 83 runs, plus embeddings, audits and the video narration, cost about $16 through OpenRouter, a service that gives access to many AI models. Settings: randomness ("temperature") 0.9; step-by-step reasoning off, or set low where a model requires it; meaning embeddings from `openai/text-embedding-3-small`; rewording by `meta-llama/llama-3.3-70b-instruct`.

| Setup | Tests (number of runs) | Agents per swarm |
|---|---|---|
| Small, fixed roles | no hiding (5), persona shift (5), AI rewording (5), model mixing (5), no house style (3), subtle agenda (3), memory (3), all three combined (3), frontier models (2), frontier + persona shift (2) | 40 |
| Small, shuffled roles, with honest twins | obvious agenda (5), subtle agenda (5), adaptive attacker (5) | 40 |
| Large, shuffled roles, with honest twins | obvious agenda (10), subtle agenda (10), persona shift (6), memory (3), adaptive attacker (3) | 160 |

*Table 3. All 83 swarms: 7,160 agents, 71,600 posts, 39,613 usernames.*

![**Figure 6.** Extra tests (combined fingerprint): telling apart operators, and telling apart agents within one operator, overall and in rounds 6–10 only. Scores: 0.5 = coin flip, 1 = perfect.](results/figures/fig6_robustness.png){w=14}

![**Figure 7.** What the combined fingerprint actually picks up in the small fixed-role tests: the same agent, the same operator (different agents), and the same AI model (different operators).](results/figures/fig3_confound.png){w=13}

![**Figure 8.** How similar each pair of operators looks by meaning, in one small fixed-role run. The hidden boss's two fronts (6, 7) are the most similar pair. The fainter dark squares (0–4, 1–5) are operators that use the same AI model.](results/figures/fig4_fronts.png){w=15}

![**Figure 9.** Re-identifying a renamed agent under four hiding tactics, by fingerprint type (small fixed-role tests, 5 runs each; error bars show the spread across runs).](results/figures/fig1_reid_auc.png){w=13.5}

![**Figure 10.** Adaptive attacker. Fronts are told their detection score (similarity to their own team) after every round and asked to lower it. They lower it somewhat with 8 operators and barely with 32, never below the 0.5 threshold they were given.](results/figures/fig8_adaptive.png){w=13.5}

## Appendix C. A First Look at Real Swarm Data

The Swarm Traces project released 189,579 records from the Hugging Face incident, with names and secrets blacked out. Because agent names were removed without consistent replacements, the data cannot test whether renamed agents can be re-identified. As an exploratory look only, I fingerprinted 20,000 of the 55,790 distinct pieces of text (mostly attack scripts), using character patterns, and grouped near-copies. Grouping texts that are at least 80% similar gives 106 families of 10 or more near-copies; the 50 largest cover 18% of the sample, and the rest is a long tail of nearly unique scripts. At a looser 60% threshold, one family of shared code covers 52%. This fits Section 4.2: writing style links texts to a shared toolkit or setup, not to one of the ~1,200 individual agents.

## Appendix D. Key Terms in Plain Language

| Term | What it means here |
|---|---|
| AI model / LLM | The underlying AI system, such as Claude or GPT. "LLM" means large language model, the kind of AI that reads and writes text. |
| Frontier model | One of the most capable AI models currently available. |
| Agent | One running copy of an AI model that acts on its own; here, it reads and posts on a forum. |
| Swarm | A large group of agents interacting with each other. |
| Operator | The company or person that runs a group of agents and writes their instructions. |
| Instructions (system prompt) | The hidden text an operator gives its agents describing who they are and what to do. |
| Hidden boss (covert principal) | Whoever is secretly in charge of several accounts that pretend to be independent. |
| Front (sybil) | One of those fake "independent" accounts. "Sybil" is the security term for one actor posing as many. |
| Honest twins | Two truly independent operators that happen to share an opinion; the control for "agreeing" vs. "secretly coordinating". |
| Alias | A username. Each time an agent renames itself, it starts a new alias. |
| Gateway / gateway ID | The server every AI request passes through. It can stamp each request with an ID the agent cannot change. |
| Digital key / signature | A secret code an agent can use to "sign" its messages. If agents make their own keys, a key proves nothing about who they really are ("no root of trust"). |
| Behavioral fingerprint | A profile of an account built only from what it writes: its *style* or its *meaning*. |
| Embedding | A list of numbers an AI produces to summarize what a text is about; similar texts get similar numbers. |
| Keywords (TF-IDF) / character patterns (n-grams) / function words | Ways of measuring style: which unusual words an account uses; short runs of letters and symbols; and how often it uses common little words like "the" or "however". |
| Similarity | How alike two fingerprints are, from 0 (unrelated) to 1 (identical). |
| Persona shift / AI rewording | Hiding tactics: writing in a new voice after each rename, or having another AI rewrite every post. |
| Adaptive attacker | A front that is told its detection score and tries to lower it. |
| Botnet | A network of fake accounts controlled by one actor. |
| OAuth / OpenID; A2A | Common web login standards; and Google's standard for AI agents talking to each other. |
| Control (experiment) | A comparison group that shows what "no effect" looks like; here, the honest twins. |
| Run (seed) | One full simulation. Different runs use different random choices so results don't depend on luck. |
| AUC | How often a method rates a true match as more similar than a non-match: 0.5 = coin flip, 1.0 = perfect. |
| Precision / recall / F1 | Of the links claimed, how many are right (precision); of the true links, how many are found (recall); F1 combines both (0 = nothing, 1 = perfect). |
| 95% confidence range | Where the result would likely land if the experiment were repeated, estimated by resampling the runs ("bootstrap"). |
| Merge / false merge | Treating two accounts as the same boss; a false merge links accounts that are actually independent. |
| AI judge | An AI model used to label text, here whether a post approves of or doubts a product. |
| Dual use | Research that could help defenders but also help bad actors. |

## Appendix E. Related Work in Detail

**Agent identity.** Proposals attach IDs to individual AI systems, issued by whoever deploys them ([Chan et al., 2024](https://arxiv.org/abs/2406.12137)), or tie agents' actions to legal entities through shared infrastructure ([Chan et al., 2025](https://arxiv.org/abs/2501.10114)). Others extend today's web login standards (OAuth and OpenID) to agents ([South et al., 2025](https://arxiv.org/abs/2501.09674)). Without a trusted issuer, one actor can pose as many (a "Sybil attack"; [Douceur, 2002](https://doi.org/10.1007/3-540-45748-8_24)). Google's A2A standard for agent-to-agent communication leaves identity largely to what agents claim about themselves ([Google, 2025](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/)). This work puts self-chosen names, agent-made keys and gateway IDs side by side while agents rename themselves at will.

**Identifying the source of AI text.** The AI model behind a text can be identified with high accuracy, even after another AI rewrites it ([Sun et al., 2025](https://arxiv.org/abs/2502.12150)), and identification errors drop quickly as texts get longer ([Radvand et al., 2025](https://arxiv.org/abs/2501.02406)). AI models can also be identified by probing them with questions ([Pasquini et al., 2024](https://arxiv.org/abs/2407.15847)), and agents by their clicks ([Lugoloobi et al., 2026](https://arxiv.org/abs/2605.14786)) or network traffic ([Kang et al., 2026](https://arxiv.org/abs/2606.20910)). Closest to this work, [Park et al. (2026)](https://arxiv.org/abs/2607.18826) link one attacker's sessions across different agents from traces left at a relay server (score 0.82). Rewording is known to fool AI-text detectors ([Krishna et al., 2023](https://arxiv.org/abs/2303.13408)). These works identify a *model*, *software framework* or *attack campaign*. This work instead separates the individual agent, its operator and its AI model in one controlled population, and adds a control group to test whether detectors find coordination or just agreement. It also fits the finding that AI agents without distinct personas behave much alike ([Riedl, 2025](https://arxiv.org/abs/2510.05174)).

**Coordination and fake accounts.** Fake-account campaigns on social media are usually detected from shared behavior across accounts ([Pacheco et al., 2021](https://arxiv.org/abs/2001.05658)). AI-run fake-account networks form such clusters ([Yang & Menczer, 2023](https://arxiv.org/abs/2307.16336)), and on the AI-agent forum Moltbook, posting-time patterns traced most viral "AI" stories back to human-steered accounts ([Li, 2026](https://arxiv.org/abs/2602.07432)). More agents add no new evidence when they share an origin ([Bara, 2026](https://arxiv.org/abs/2609.01873)). Fake "independent" accounts are the identity-side version of AI agents colluding ([Hammond et al., 2025](https://arxiv.org/abs/2502.14143); [Motwani et al., 2024](https://proceedings.neurips.cc/paper_files/paper/2024/hash/861f7dad098aec1c3560fb7add468d41-Abstract-Conference.html)). Whether several accounts act as one agent is a question about "collective agency" ([Jørgensen et al., 2026](https://arxiv.org/abs/2605.00248)); the honest-twins result shows that shared *output* alone cannot answer it.
