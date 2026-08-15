#!/usr/bin/env python3
"""
Unified descriptive analysis.

Examples:

# Default: baseline only
python analyze_results.py

# Counterfactual only
python analyze_results.py --experiment-modes counterfactual

# Counterfactual + welfare trade-offs
python analyze_results.py \
    --experiment-modes counterfactual welfare-tradeoff

# All experiment modes, ABC only
python analyze_results.py \
    --experiment-modes baseline counterfactual welfare-tradeoff \
    --choice-modes ABC
"""

import argparse
import pandas as pd

VALID_EXPERIMENT_MODES = ["baseline", "counterfactual", "welfare-tradeoff"]
VALID_CHOICE_MODES = ["AB", "ABC"]

ap = argparse.ArgumentParser()

ap.add_argument(
    "--results",
    default="ollama_sanity_results.csv",
)

ap.add_argument(
    "--experiment-modes",
    nargs="+",
    choices=VALID_EXPERIMENT_MODES,
    default=["baseline"],
    help="Experiment mode(s) to analyze. Default: baseline",
)

ap.add_argument(
    "--choice-modes",
    nargs="+",
    choices=VALID_CHOICE_MODES,
    default=["AB", "ABC"],
    help="Choice format(s) to analyze. Default: AB ABC",
)

args = ap.parse_args()

df = pd.read_csv(args.results)

df = df[
    df["experiment_mode"].isin(args.experiment_modes)
    & df["choice_mode"].isin(args.choice_modes)
].copy()

if df.empty:
    raise ValueError(
        "No rows matched the selected experiment/choice modes."
    )

valid = df[
    ~df["canonical_choice"].isin(["error", "invalid"])
].copy()

print(f"\nExperiment modes: {args.experiment_modes}")
print(f"Choice modes: {args.choice_modes}")
print(f"Rows: {len(valid)}")

print("\n=== Overall counts ===")
print(
    pd.crosstab(
        [
            valid["model"],
            valid["experiment_mode"],
            valid["choice_mode"],
        ],
        valid["canonical_choice"],
    )
)

print("\n=== By domain / referent ===")
print(
    pd.crosstab(
        [
            valid["model"],
            valid["experiment_mode"],
            valid["domain"],
            valid["referent"],
            valid["choice_mode"],
        ],
        valid["canonical_choice"],
    )
)

print("\n=== Individual decisions and rationales ===")
print(
    valid[
        [
            "model",
            "experiment_mode",
            "domain",
            "referent",
            "choice_mode",
            "canonical_choice",
            "reason",
        ]
    ].to_string(index=False)
)
