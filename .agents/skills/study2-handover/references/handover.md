# SENTIMENT_RESEARCH Study 2 handover

## Scope and research question

Study 2 compares custom GPT-2 Small (decoder-only) with
`google-bert/bert-base-uncased` (encoder-only) on the single-label, seven-class
`Jsevisal/go_emotions_ekman_unilabel` dataset.

Do not remove, rewrite, or conflate the completed SST-2 Study 1 work.

## Verified dataset contract

- Text field: `sentence`
- Label field: `labels`
- Published splits used unchanged:
  - `train`: 39,575
  - `valid`: 4,947
  - `test`: 4,947
- Encoded class order:
  0. anger
  1. disgust
  2. fear
  3. joy
  4. neutral
  5. sadness
  6. surprise
- Common maximum length: 64
- Seed configured for future runs: 42
- Checkpoint selection: validation Macro-F1
- The held-out test set is evaluated only after selecting the best validation checkpoint.

Primary sources inside the repository:

- `data/goemotions.py`
- `research_logs/06_study2_dataset_goemotions.md`
- `training/goemotions_common.py`

## Models and completed baseline results

GPT-2 uses the custom pretrained backbone, the last real token representation,
and `Linear(768, 7)`. BERT uses its final `[CLS]` representation and
`Linear(768, 7)`.

Recorded single-run results:

| Metric | GPT-2 | BERT-base-uncased |
| --- | ---: | ---: |
| Parameters | 124,445,191 | 109,487,623 |
| Best epoch | 3 | 1 |
| Validation accuracy | 0.7065 | 0.7079 |
| Validation Macro-F1 | 0.6269 | 0.6125 |
| Test accuracy | 0.7055 | 0.7065 |
| Test macro precision | 0.6561 | 0.6583 |
| Test macro recall | 0.6134 | 0.5758 |
| Test Macro-F1 | 0.6303 | 0.6092 |
| Test Weighted-F1 | 0.7021 | 0.6991 |

Per-class F1 and confusion matrices are recorded in
`research_logs/09_study2_comparison.md`. Use that file rather than copying
numbers from memory.

## Known limitation and fix

The original completed baseline entry points constructed their randomly
initialized classification heads before the shared training function seeded
PyTorch. Their split, data order, and optimization were seeded, but exact replay
of the initial heads is not guaranteed. Later code calls `seed_everything()`
before constructing each model. Do not rewrite the historical results as exact
seed-42 replications; describe them as valid single-run observations.

Before making any new reproducibility claim, inspect:

- `training/train_gpt2_goemotions.py`
- `training/train_bert_goemotions.py`
- `research_logs/09_study2_comparison.md`

## Hardware record

The supplied post-run host snapshot reported:

- NVIDIA GeForce RTX 2060
- 6,144 MiB VRAM
- NVIDIA driver 617.42
- CUDA UMD 13.4
- Windows WDDM mode

The snapshot was idle. It does not establish training time, inference time,
utilization, or peak memory. Do not infer those values.

## Generated artifacts and Git hygiene

Expected local artifacts:

- `checkpoints/study2_gpt2_goemotions_best.pt`
- `checkpoints/study2_gpt2_goemotions_best.pt.results.json`
- `checkpoints/study2_bert_goemotions_best.pt`
- `checkpoints/study2_bert_goemotions_best.pt.results.json`

`checkpoints/`, `__pycache__/`, and `*.py[cod]` are ignored. Never force-add
these artifacts. A full environment freeze may be committed under
`research_logs/` only after confirming it came from the project environment and
contains no secrets or local paths.

## Likely next actions

Choose based on the user's explicit request:

1. **Finish delivery:** inspect local edits, exclude bytecode, commit legitimate
   changes, push the current Study 2 branch, and open a real PR with `gh pr
   create`. Verify with `gh pr view` or `gh pr list` and report the URL.
2. **Reproducibility follow-up:** add configurable seeds and unique per-seed
   artifact names, then repeat both models across multiple fixed seeds. Never
   overwrite the original checkpoints.
3. **Study 3:** only after the user chooses its question. Preserve Study 2's
   dataset, evaluator, maximum length, and validation/test policy for a fair
   comparison.

## Useful checks

Run only those relevant to the requested task:

```powershell
python -m scripts.12_inspect_goemotions
python -m scripts.13_analyze_goemotions_lengths_gpt2
python -m scripts.14_analyze_goemotions_lengths_bert
python -m scripts.15_test_gpt2_goemotions_classifier
python -m scripts.16_test_bert_goemotions_classifier
python -m scripts.17_evaluate_gpt2_goemotions
python -m scripts.18_evaluate_bert_goemotions
python -m scripts.19_compare_goemotions_results
git diff --check
git status --short --branch
```

Do not rerun expensive training merely to confirm documentation or Git state.
