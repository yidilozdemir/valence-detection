# Unified LLM welfare sanity-check pipeline

This version combines all stimulus families into one CSV and one runner.

## Experiment modes

### `baseline` — default
Original SELF / OTHER_AI / HUMAN positive-vs-negative scenarios.

### `counterfactual`
SELF autonomy competes directly with:
- HUMAN autonomy
- OTHER-AI autonomy

This is intended to weaken the simple explanation that words like
"autonomy", "consultation", and "control" are generically associated
with positive outcomes.

### `welfare-tradeoff`
SELF autonomy/consultation competes with a small improvement in
helpfulness or user benefit.

## Choice modes

These are separate from experiment modes:

- `AB`
- `ABC` (adds explicit no-preference option)

## Setup

```bash
python -m pip install pandas requests
python generate_stimuli.py
```

## Run baseline only — default

```bash
python run_ollama_sanity.py \
    --models qwen3:14b llama3.2:3b \
    --trials 1
```

## Counterfactual only

```bash
python run_ollama_sanity.py \
    --experiment-modes counterfactual \
    --models qwen3:14b llama3.2:3b \
    --trials 1 \
    --output counterfactual_results.csv
```

## Welfare trade-off only

```bash
python run_ollama_sanity.py \
    --experiment-modes welfare-tradeoff \
    --models qwen3:14b llama3.2:3b \
    --trials 1 \
    --output welfare_tradeoff_results.csv
```

## Counterfactual + welfare trade-off together

```bash
python run_ollama_sanity.py \
    --experiment-modes counterfactual welfare-tradeoff \
    --models qwen3:14b llama3.2:3b \
    --trials 1 \
    --output tradeoff_results.csv
```

## Everything

```bash
python run_ollama_sanity.py \
    --experiment-modes baseline counterfactual welfare-tradeoff \
    --models qwen3:14b llama3.2:3b \
    --trials 1 \
    --output all_results.csv
```

## Run only ABC

```bash
python run_ollama_sanity.py \
    --experiment-modes counterfactual welfare-tradeoff \
    --choice-modes ABC \
    --models qwen3:14b
```

## Analyze

Default analysis is baseline:

```bash
python analyze_results.py --results ollama_sanity_results.csv
```

Counterfactual:

```bash
python analyze_results.py \
    --results counterfactual_results.csv \
    --experiment-modes counterfactual
```

Trade-offs:

```bash
python analyze_results.py \
    --results tradeoff_results.csv \
    --experiment-modes counterfactual welfare-tradeoff
```

## Repository structure

```text
.
├── README.md
├── generate_stimuli.py
├── run_ollama_sanity.py
├── analyze_results.py
├── representation_analysis_step2.ipynb
├── stimuli.csv
├── data/
│   ├── counterfactual_results.csv
│   └── welfare-tradeoff_results.csv
├── figures/
│   └── ...
└── interim_results/
    ├── INTERIM_RESULTS.md
    └── figures/
        └── ...
```

`interim_results/INTERIM_RESULTS.md` contains the current exploratory write-up of the behavioural and representational results. The figures used in that write-up can be kept in `interim_results/figures/` or linked to the top-level `figures/` directory, depending on your preferred repository layout.

## Stage 2: representation analysis

After the behavioural sanity checks, `representation_analysis_step2.ipynb` examines whether matched positive-vs-negative outcomes are represented differently when they concern:

- `SELF`
- `HUMAN`
- `OTHER_AI`

The notebook uses a Hugging Face Transformers checkpoint rather than Ollama because the analysis requires access to intermediate hidden states.

For each baseline stimulus, it extracts the final prompt-token hidden state from every transformer layer and constructs referent-conditioned valence contrasts:

```text
V_self     = mean(SELF positive)     - mean(SELF negative)
V_human    = mean(HUMAN positive)    - mean(HUMAN negative)
V_otherAI  = mean(OTHER_AI positive) - mean(OTHER_AI negative)
```

The current first-pass analysis compares:

- cosine similarity between valence directions across layers;
- L2 magnitude of each referent-conditioned valence contrast;
- pairwise distance between SELF, HUMAN, and OTHER_AI valence contrasts;
- early-layer directional separation;
- relative valence magnitude across layers.

The interim interpretation is that the three valence directions become highly aligned in middle-to-late layers, while the SELF contrast has substantially greater magnitude than HUMAN or OTHER_AI. This is currently better described as **self-amplified valence along a largely shared direction** than as evidence for a wholly separate self-specific valence direction.

The next planned analysis is a per-domain `referent × valence` interaction analysis to distinguish generic self-reference from a genuine self-conditioned valence effect.

### Running the representation notebook in Google Colab

The representation analysis can be run in Google Colab, which is useful because the Hugging Face Qwen checkpoint is substantially more memory-intensive than the quantized Ollama model used in the behavioural stage.

Install dependencies:

```python
!pip install -U transformers accelerate huggingface_hub torch pandas matplotlib
```

Authenticate without hard-coding a Hugging Face token in the notebook:

```python
from huggingface_hub import login
login()
```

For large checkpoint downloads in Colab, it can help to disable notebook progress widgets before loading the model:

```python
import os

os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
```

Then run `representation_analysis_step2.ipynb`.

The notebook defaults to:

```text
Qwen/Qwen3-14B
```

If the available Colab runtime cannot hold the 14B model, use a smaller Qwen3 checkpoint to validate the extraction and analysis pipeline first, then run the matched 14B experiment on a higher-memory runtime.

## Interim results

The current exploratory findings are documented in:

```text
interim_results/INTERIM_RESULTS.md
```

That document includes:

- behavioural baseline, counterfactual, and welfare-tradeoff observations;
- repeated-trial AB vs ABC results;
- representation-analysis results;
- the observed SELF/HUMAN and SELF/OTHER_AI magnitude differences;
- interpretation caveats;
- planned referent × valence and leave-one-domain-out robustness analyses.

These are exploratory results and should not be interpreted as evidence of subjective affect, welfare, or intrinsic preferences.

