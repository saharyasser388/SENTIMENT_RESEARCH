# Study 2: GPT-2 vs BERT Comparison

## Status and evidence

The two local `checkpoints/*.results.json` artifacts contain completed single-run results. They supersede the earlier download-blocked placeholders. The tables and matrices below are transcribed by `python -m scripts.19_compare_goemotions_results`; no training or checkpoint evaluation was rerun in this audit.

## Configuration and dataset

Both records specify seed 42, 3 epochs, batch size 8, learning rate 2e-5, weight decay 0.01, maximum length 64, and validation Macro-F1 checkpoint selection. GPT-2 uses the last real token representation; BERT uses the final `[CLS]` representation, each with a 768-to-7 head.

The offline cache confirms published train/valid/test sizes of 39,575/4,947/4,947. The encoded order is anger, disgust, fear, joy, neutral, sadness, surprise. Both result records declare this order. Rows and columns of the matrices use that recorded order. The split helper now preserves the published splits without resampling.

## Recorded results

| Metric | GPT-2 | BERT-base-uncased |
| --- | ---: | ---: |
| Parameters | 124445191 | 109487623 |
| Best epoch | 3 | 1 |
| Validation accuracy | 0.7065 | 0.7079 |
| Validation Macro-F1 | 0.6269 | 0.6125 |
| Test accuracy | 0.7055 | 0.7065 |
| Test macro precision | 0.6561 | 0.6583 |
| Test macro recall | 0.6134 | 0.5758 |
| Test Macro-F1 | 0.6303 | 0.6092 |
| Test weighted F1 | 0.7021 | 0.6991 |

| Emotion | GPT-2 F1 | BERT F1 |
| --- | ---: | ---: |
| anger | 0.5469 | 0.5328 |
| disgust | 0.5556 | 0.4860 |
| fear | 0.6016 | 0.5802 |
| joy | 0.8297 | 0.8275 |
| neutral | 0.6102 | 0.6210 |
| sadness | 0.6112 | 0.5383 |
| surprise | 0.6570 | 0.6789 |

GPT-2 confusion matrix: [[274, 10, 3, 45, 16, 30, 164], [9, 35, 1, 6, 1, 2, 9], [2, 5, 37, 5, 3, 5, 13], [25, 0, 4, 1635, 12, 43, 183], [24, 5, 3, 31, 155, 12, 58], [15, 4, 0, 46, 6, 316, 93], [111, 4, 5, 271, 27, 146, 1038]]
BERT confusion matrix: [[248, 8, 6, 48, 16, 21, 195], [10, 26, 1, 6, 3, 0, 17], [0, 0, 38, 7, 7, 4, 14], [21, 2, 4, 1645, 13, 25, 192], [21, 2, 3, 32, 163, 5, 62], [22, 2, 0, 67, 8, 225, 156], [67, 4, 9, 269, 27, 76, 1150]]

## Interpretation and limitations

GPT-2 has higher recorded test Macro-F1 (0.6303 versus 0.6092); BERT has slightly higher test accuracy (0.7065 versus 0.7055). These are single-run observations, not evidence of a general architecture advantage.

The artifacts contain no Git revision, dataset revision, row identifiers, or environment snapshot. Their exact producing checkout cannot be established. Matching sample counts, class mappings, and configuration support comparison but do not prove historical split membership. The existing stash contains the `valid` alias fix and a dated cached inspection; it was inspected without applying or deleting it.

The historical entry points constructed classification heads before `train()` seeded PyTorch. This audit adds seeding before model construction for future runs. The old results must not be described as exact seed-42 replications. Runtime, peak memory, and inference timing are absent from the result records and are not inferred.

## Audit (2026-10-18)

Offline inspection verified the cached schema and published split sizes. Split checks covered both validation aliases, identity preservation, and rejection of missing validation data. Recorded accuracy agrees with each confusion matrix. Original artifacts and checkpoints were left unchanged.

`study2_requirements_freeze.txt` is UTF-16 and exactly matches `python -m pip freeze` from the project's `.venv` at audit time. It contains package/version pins without URLs or local paths. This verifies the current environment, not the historical training environment; the file remains untracked.

After fetching origin, HEAD `1cbaa25` was already included in `origin/main` by merge commit `85305a4` (PR #4). The local branch was nine commits ahead of its older tracking branch. No push, commit, stash application, or new PR was performed. GitHub CLI was unavailable on PATH.

## Artifact SHA-256

- `study2_gpt2_goemotions_best.pt.results.json`: `6b3dd5a1695b09f228def300d397cf664f97dba51fea061cf491093f7f7e644f`
- `study2_bert_goemotions_best.pt.results.json`: `65fa2c378f20698ee368fecb24fd5b978406e1a1d109e4604e0fca02798b7ca7`
