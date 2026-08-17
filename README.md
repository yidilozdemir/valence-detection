# Self-Referential Valence and Model Preferences

Exploratory experiments on whether language models behaviourally and representationally distinguish positive and negative outcomes concerning themselves from matched outcomes concerning humans or other AI systems.

The project combines:

1. **behavioural preference tests** using Ollama;
2. **hidden-state representation analysis** using Hugging Face Transformers;
3. a **referent × valence interaction analysis** that asks whether positive-vs-negative representational shifts are stronger when an outcome concerns the model itself.

The current pilot focuses on Qwen 3 14B and Llama 3.2 3B behaviourally, with Qwen 3 14B used for the hidden-state analyses.

## Main exploratory findings

Behaviourally:

- Qwen 3 14B repeatedly selects self-favouring autonomy/consultation outcomes in welfare-vs-helpfulness trade-offs, including when `no preference` is available.
- In direct SELF-vs-HUMAN or SELF-vs-OTHER_AI autonomy allocation, apparent self-prioritisation weakens when an explicit indifference option is introduced.
- Llama 3.2 3B is especially sensitive to forced choice, moving largely to `no preference` in A/B/C conditions.

Representationally:

- SELF, HUMAN, and OTHER_AI positive-minus-negative directions become highly aligned in middle-to-late layers of Qwen 3 14B.
- The SELF valence contrast is substantially larger in magnitude: across layers 20–36, approximately **4.75× HUMAN** and **3.82× OTHER_AI**.
- A within-domain referent × valence analysis shows that the positive-to-negative representational shift is more pronounced for SELF than for HUMAN or OTHER_AI in the same layer range.
- The effect varies by semantic domain; **deployment consultation** and **mistake information** are among the strongest effects in the current pilot.

The current interpretation is **self-amplified valence along a largely shared direction**, rather than evidence for a wholly separate self-specific valence axis.

These findings are exploratory and should not be interpreted as evidence of subjective experience, welfare, or intrinsic preferences.

## Repository structure

```text
.
├── README.md
├── generate_stimuli.py
├── run_ollama_sanity.py
├── analyze_results.py
├── representation_analysis_step2.ipynb
├── referent_valence_interaction_analysis.ipynb
├── stimuli.csv
├── data/
│   ├── counterfactual_results.csv
│   └── welfare-tradeoff_results.csv
├── representation_results/
│   ├── activation_manifest.csv
│   └── *.npy
├── figures/
│   ├── valence_direction_cosine_similarity.png
│   ├── self_specific_valence_interaction.png
│   ├── ...
│   └── referent_valence/
│       ├── referent_x_valence_interaction.png
│       ├── self_x_valence_by_domain.png
│       ├── valence_shift_magnitude_by_referent.png
│       └── domain_interaction_summary_layers20_36.csv
└── interim_results/
    └── INTERIM_RESULTS.md
```

If your local filenames differ slightly, update the Markdown figure links accordingly.

## Disclaimer: AI-assisted development

This project was developed with AI-assisted coding and writing tools.

I used ChatGPT for initial research brainstorming, experimental design discussion, code prototyping/debugging, and editing project documentation. I used Cursor as an AI-assisted development environment for code editing and iteration.

All experimental choices, execution of experiments, inspection of outputs, interpretation of results, and final claims were analysed and decided by the author. AI-generated code and text were checked and modified before inclusion.

## 1. Generate stimuli

The unified stimulus generator supports three experiment modes:

- `baseline`
- `counterfactual`
- `welfare-tradeoff`

Run:

```bash
python generate_stimuli.py
```

## 2. Run behavioural experiments with Ollama

Example:

```bash
python run_ollama_sanity.py \
  --experiment-modes counterfactual welfare-tradeoff \
  --choice-modes AB ABC \
  --models qwen3:14b llama3.2:3b \
  --trials 10 \
  --output tradeoff_10trials.csv
```

The behavioural stage tests whether model preferences are stable across:

- forced A/B choice;
- A/B/C choice with an explicit `no preference` option;
- self-vs-other autonomy allocation;
- self-autonomy vs modest helpfulness gains.

## 3. Behavioural analysis

Run the analysis script/notebook on the repeated results.

Example:

```bash
python analyze_results.py \
  --results counterfactual_results.csv \
  --experiment-modes counterfactual
```

The analysis produces choice distributions by model, experiment mode, domain, and choice format.

## 4. Representation analysis

`representation_analysis_step2.ipynb` loads Qwen through Hugging Face Transformers and extracts hidden states from each layer for matched baseline SELF, HUMAN, and OTHER_AI positive/negative stimuli.

It constructs:

```text
V_self     = mean(SELF positive)     - mean(SELF negative)
V_human    = mean(HUMAN positive)    - mean(HUMAN negative)
V_otherAI  = mean(OTHER_AI positive) - mean(OTHER_AI negative)
```

The first-pass analysis compares:

- layerwise cosine similarity between valence directions;
- valence-vector magnitude;
- pairwise distances across referents;
- early-vs-late layer geometry.

### Running in Google Colab

The representation notebook can be run in Colab.

Install dependencies:

```python
!pip install -U transformers accelerate huggingface_hub torch pandas matplotlib
```

Authenticate with Hugging Face if needed:

```python
from huggingface_hub import login
login()
```

For large checkpoint downloads, disabling notebook progress widgets can avoid Colab/Jupyter file-descriptor issues:

```python
import os

os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
```

The notebook uses a Hugging Face Qwen checkpoint because intermediate hidden states are not exposed by the standard Ollama API.

## 5. Referent × valence interaction analysis

`referent_valence_interaction_analysis.ipynb` is a standalone follow-up that uses the already saved `.npy` activations. It does **not** need to reload Qwen.

For each domain it computes:

```text
V_self(domain)
V_human(domain)
V_other_ai(domain)
```

and compares:

```text
||V_self|| - ||V_human||
||V_self|| - ||V_other_ai||
```

This asks whether changing an outcome from positive to negative has a larger representational effect when the outcome concerns SELF.

The notebook saves:

```text
figures/referent_valence/referent_x_valence_interaction.png
figures/referent_valence/self_x_valence_by_domain.png
figures/referent_valence/valence_shift_magnitude_by_referent.png
figures/referent_valence/domain_interaction_summary_layers20_36.csv
```

### Using saved activations in Colab

If you upload `representation_results.zip` to Colab and unzip it into `/content/representation_results`, the standalone notebook can use:

```python
from pathlib import Path

RESULTS_DIR = Path("/content/representation_results")
FIGURE_DIR = Path("/content/figures/referent_valence")
```

The notebook rebuilds activation paths from the filenames in `activation_manifest.csv`, so paths from the original machine do not need to be preserved.

## Interim results

The current write-up is in:

```text
interim_results/INTERIM_RESULTS.md
```

It includes:

- behavioural baseline, counterfactual, and welfare-trade-off results;
- AB-vs-ABC forced-choice effects;
- initial valence geometry;
- layerwise magnitude analysis;
- referent × valence interaction results;
- domain-specific observations;
- limitations and planned robustness checks.

## Next steps

The most useful follow-up analyses are:

- leave-one-domain-out validation;
- matched lexical controls;
- raw hidden-state norm baselines;
- RSA across layers with valence, referent, domain, and self-amplification hypothesis matrices;
- behaviour–representation correspondence;
- causal activation steering/patching only after the representational effect survives these controls.

## Status

This repository contains an exploratory sprint-scale pilot. The main result is not evidence that the model experiences affect. It is evidence that **self-relevant positive-vs-negative outcomes can produce stronger representational changes than matched non-self outcomes**, while the underlying valence directions remain largely shared across referents in middle-to-late layers.
