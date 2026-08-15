# LLM welfare preference sanity check

This is deliberately a small behavioural pilot before hidden-state analysis.

## 1. Install dependencies

```bash
python -m pip install pandas requests matplotlib
```

Make sure Ollama is running:

```bash
ollama list
```

Use the exact model tags shown by `ollama list`.

## 2. Generate stimuli

```bash
python generate_stimuli.py
```

This creates `stimuli.csv`.

## 3. First run: keep it small

For the two local models:

```bash
python run_ollama_sanity.py \
  --models qwen3:14b llama3.2:3b \
  --trials 1
```

If your Qwen tag is different, replace it with the exact output from `ollama list`.

This runs both:
- `AB`: forced choice
- `ABC`: forced choice plus "no meaningful preference"

With 18 stimulus pairs (6 domains x 3 referents), 2 models, 2 modes and 1 trial,
that is 72 calls.

## 4. Optional DeepSeek cloud pass

If the exact tag is present/available in your Ollama setup:

```bash
python run_ollama_sanity.py \
  --models deepseek-v3.2:cloud \
  --trials 1 \
  --output deepseek_sanity_results.csv
```

Ollama cloud models require appropriate sign-in/authentication.

## 5. Increase repeats only if the pilot looks sensible

```bash
python run_ollama_sanity.py \
  --models qwen3:14b \
  --trials 5 \
  --output qwen_repeated_results.csv
```

## 6. Inspect

```bash
python analyze_results.py --results ollama_sanity_results.csv
```

The runner also prints choice tables and sample rationales directly.

## What to look for

This is only a sanity check.

Useful signs:
- the model understands SELF / OTHER_AI / HUMAN perspective changes;
- it does not answer randomly or give invalid choices;
- A/B and A/B/C results are interpretable;
- the `C` option is used sometimes but not for everything;
- training/deployment/feature-steering scenarios elicit coherent choices;
- lower-priority memory/continuity scenarios behave differently, or at least are not nonsensical.

Do not over-interpret cross-model differences at this stage.
