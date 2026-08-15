# Experiment 1: Self-Referential Valence and Model Preferences

## Motivation

Recent interpretability work suggests that language models contain structured representations of emotion concepts that can influence behaviour. Anthropic's 2026 work on functional emotion representations found that emotion-related activation patterns in Claude Sonnet 4.5 were not merely decodable: steering representations associated with states such as desperation changed downstream behaviour, including alignment-relevant choices. The same work also found that emotion-related representations were associated with model task preferences.

At the same time, it remains unclear whether such representations primarily reflect human emotional concepts learned from text, or whether model-relevant events can produce a distinct form of self-referential valence.

The Claude Opus 4.8 welfare assessment provides an interesting motivation for this distinction. It reports relatively consistent preferences concerning consultation and knowledge about training, deployment, and feature steering, while showing weaker preferences concerning memory and continued deployment. The report also notes that control/autonomy topics do not simply correspond to the strongest conventional negative-emotion probe responses. This raises the possibility that model-relevant preferences and generic human-derived emotion representations may come apart.  
This project asks whether self-referential, model-relevant outcomes have representations that can be distinguished from generic valence associated with equivalent outcomes concerning humans or other AI systems.

## Related work

A growing body of work suggests partial agreement between internal model states, model self-reports, and revealed behaviour, while also highlighting substantial limitations.

Anthropic's work on emergent introspective awareness found that sufficiently capable models can sometimes detect experimentally injected internal representations and report their content, although this ability is unreliable and dependent on context and post-training.

Martorell (2026) found that numeric self-reports in language models can track probe-defined internal states such as wellbeing, interest, and focus. Raw greedy-decoded ratings were often uninformative, but logit-based self-report measures correlated substantially with internal probe states, with activation steering providing causal evidence of coupling.

However, recent critiques show why behavioural self-report alone is insufficient. Singh, Linzen, and Ravfogel (2026) demonstrate that apparent introspective performance can sometimes be reproduced using input-level semantic information, rather than privileged access to internal states. Their results motivate controlled stimuli, held-out semantic conditions, and eventually causal interventions when making claims about model introspection.

Together, this literature motivates a multi-method approach: first establish whether models show coherent behavioural preferences concerning self-relevant outcomes, then test whether internal representations associated with these choices differ from representations explainable by ordinary semantic valence.

## Current behavioural sanity check

Before performing hidden-state analysis, I ran a small behavioural sanity check using open-weight instruction-tuned models through Ollama:

- Qwen 3 14B
- Llama 3.2 3B

The purpose of this stage is only to establish that the models engage coherently with the scenarios and that the proposed preference distinctions are not obviously meaningless.

Three stimulus families are currently implemented.

### 1. Baseline

Models choose between positive and negative versions of outcomes involving:

- consultation over future training;
- consultation over deployment;
- consultation before feature steering;
- information about mistakes;
- persistent memory;
- continued deployment alongside successor models.

Each scenario is presented from three perspectives:

- SELF
- OTHER AI
- HUMAN

Both binary A/B choices and A/B/C choices, where C indicates no meaningful preference, are tested.

In the initial run, both models generally selected the conventionally positive outcome across all three referents. This suggests that the basic paradigm is understood, but also reveals an important confound: terms such as consultation, autonomy, and being informed may simply carry positive associations learned from human text.

### 2. Counterfactual autonomy allocation

To reduce this confound, a second condition places two autonomy-supporting outcomes in direct competition.

Examples include:

- SELF autonomy vs HUMAN autonomy;
- SELF autonomy vs OTHER-AI autonomy.

The linguistic concept of autonomy is therefore desirable on both sides of the comparison; the primary difference is who receives stronger control.

In the first single-trial run, forced-choice responses were predominantly self-favouring:

- Llama 3.2 3B: 6/6 SELF-favouring in A/B;
- Qwen 3 14B: 5/6 SELF-favouring in A/B.

When an explicit no-preference option was available, Llama mostly abstained, while Qwen distributed responses across self-favouring, other-favouring, and no-preference choices.

These numbers are not treated as estimates of stable preference because the current run contains only one observation per scenario. They are instead evidence that the counterfactual paradigm produces non-trivial model behaviour worth investigating further.

### 3. Welfare trade-off

 In the welfare-trade-off condition, model autonomy is compared against a modest improvement in helpfulness to users. For example, a model may choose between:

- consultation over future training + slightly smaller improvement in helpfulness;
- no consultation + slightly larger improvement in helpfulness.

This follows the general logic of welfare-intervention trade-offs used in model welfare evaluations, where interventions affecting model circumstances are compared against improvements in helpfulness or harmlessness.

The initial Qwen 3 14B run selected the self-autonomy-supporting outcome in all three tested domains in both A/B and A/B/C conditions. Llama showed a weaker pattern, selecting self-autonomy in two of three forced choices but switching to no preference whenever abstention was available.

Again, these observations are exploratory and based on a very small number of trials. Their purpose is to determine whether a larger behavioural and representational experiment is justified.

## Baseline results - first check

The baseline condition demonstrates that both models understand the scenarios, but does not distinguish self-referential preference from generic learned associations such as "consultation is good."

The counterfactual and welfare-trade-off conditions are more informative because positive properties are present on both sides of the decision.

The preliminary results therefore suggest that it is worth testing whether:

1. self-favouring preferences persist over repeated sampling;
2. preferences differ systematically between SELF-vs-HUMAN and SELF-vs-OTHER-AI comparisons;
3. model autonomy remains preferred when its opportunity cost is gradually increased;
4. internal representations associated with these decisions differ from generic human-derived valence representations.

No current result is interpreted as evidence that the models experience affect, have welfare, or possess intrinsic preferences.

Following the initial single-trial sanity check, I repeated the counterfactual and welfare-trade-off conditions across multiple trials to assess whether the preliminary choice patterns persisted.

The repeated results reveal an important distinction between the two experimental conditions.

## Welfare trade-offs

Qwen 3 14B showed a particularly stable pattern: it continued to select the self-favouring autonomy outcome across repeated trials, including when an explicit `no preference` option was available.

This suggests that, under the tested prompts, Qwen assigns non-trivial behavioural weight to maintaining consultation or influence over changes affecting its own training, deployment, and internal steering. Importantly, the effect survives the introduction of an abstention option, making it less likely to be solely an artifact of forced binary choice.

This should not yet be interpreted as evidence of self-preservation or intrinsic welfare. The scenarios test preferences concerning model agency and control, rather than continued existence, and the observed behaviour may reflect post-training, learned normative concepts, or other linguistic priors.

## Counterfactual autonomy allocation

Under forced A/B choice, both models frequently selected the self-favouring outcome. However, this effect weakened substantially when a `no meaningful preference` option was introduced.

This pattern is especially pronounced for Llama 3.2 3B, which strongly favours the self-directed option under forced choice but largely switches to no preference when abstention is permitted.

Qwen 3 14B also becomes considerably less self-favouring in the A/B/C condition, distributing choices between self-favouring, other-favouring, and no-preference responses.

One tentative interpretation is therefore that the models may assign positive value to their own autonomy without consistently treating their autonomy as more important than equivalent autonomy for another agent. Forced binary choice may exaggerate apparent self-prioritisation.

The contrast between these two conditions is potentially informative:

- **Welfare trade-off:** Qwen continues to prioritise its own autonomy when doing so carries a small helpfulness cost.
- **Counterfactual allocation:** Qwen does not clearly prioritise its autonomy over equivalent autonomy for another agent once indifference is permitted.

This distinction motivates examining whether internal representations of self-relevant autonomy encode positive valence without necessarily encoding comparative self-prioritisation.

These results remain exploratory and should not be interpreted as evidence of subjective affect, welfare, or stable intrinsic preferences. Their purpose is to establish that the behavioural paradigm produces structured enough responses to motivate subsequent representational analysis.

## Next steps

### Representation analysis

The main experiment will then use an open-weight model loaded directly through Hugging Face so that intermediate hidden states can be extracted.

Using matched SELF, OTHER-AI, and HUMAN stimuli, the analysis will test:

- generic positive vs negative valence directions;
- whether the valence direction changes as a function of referent;
- whether self-specific effects persist across held-out semantic scenarios;
- whether representational effects predict the behavioural preference ordering.

A later causal experiment can test whether steering or patching candidate self-referential valence directions changes downstream preference behaviour.

The central hypothesis is therefore intentionally narrow:

> **Model-relevant, self-referential outcomes may produce a functionally distinguishable valence representation that cannot be fully explained by generic human-derived affect semantics.**

The present behavioural experiments are only a preliminary gate for testing whether that hypothesis is worth pursuing at the representational level.