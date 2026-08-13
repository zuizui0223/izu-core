# Reusable small-regime threshold workflow

This workflow is for researchers with a small number of ordered sites or ecological regimes who want to compare a predeclared smooth cline with a predeclared threshold.

## Input

Copy `templates/summary_template.csv` and provide one row per channel and regime.

Required fields:

- `channel`: response name;
- `regime_id`: unique label within the channel;
- `order`: ordered position;
- `second_step_state`: 0 before and 1 after the predeclared threshold;
- `mean`: observed summary;
- `n`: independent sample size.

Provide `sd` or `se` when available. Multiple photographs or measurements from the same biological unit must not be counted as independent samples.

## Run

```bash
python scripts/run_study_workflow.py examples/synthetic_threshold/summary.csv \
  --output results/example.json \
  --replicates 5000
```

## Outputs

For each channel the JSON report contains:

- the selected `cline` or `second_step` shape;
- residual scores for both candidates;
- the observed regime means;
- the matched average sample size and pooled SD;
- false threshold selection under a true cline;
- recovery of a true threshold;
- a claim-boundary statement.

## Scope and limitations

The boundary must be chosen before inspecting the response pattern. The workflow does not discover an unrestricted breakpoint, establish historical causation, or turn regime labels into evidence for a particular mechanism. With only three regimes it intentionally compares two equally parameterized shapes. A no-change model requires replicated observations and a separately specified penalized or hierarchical analysis.

The current v1 supports continuous summary statistics. Later versions can add binomial successes/trials and individual-level clustered data without changing the validation-first workflow.
