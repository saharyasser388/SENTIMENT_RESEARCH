# Study 2: BERT-base-uncased GoEmotions

## Objective and configuration

Fine-tune BERT-base-uncased for the seven-class GoEmotions comparison. The saved artifact records seed 42, 3 epochs, batch size 8, learning rate 2e-5, weight decay 0.01, maximum length 64, and validation Macro-F1 checkpoint selection.

The shared dataset policy preserves published train/valid/test splits. See [dataset verification](06_study2_dataset_goemotions.md).

## Recorded results

Source: `checkpoints/study2_bert_goemotions_best.pt.results.json`.

- Parameters: 109,487,623.
- Best epoch: 1.
- Validation accuracy: 0.7079.
- Validation Macro-F1: 0.6125.
- Test accuracy: 0.7065.
- Test Macro-F1: 0.6092.
- Test Weighted-F1: 0.6991.

These local results supersede the earlier download-blocked placeholder. No training or evaluation was rerun for this update. Per-class results, confusion matrices, artifact hashes, and audit details are in [the comparison log](09_study2_comparison.md).

## Reproducibility limits

The artifact does not record a Git revision, dataset revision, or historical environment. Exact code provenance remains unresolved. Historical heads were constructed before seeding in the shared training loop; the entry point now seeds before model construction for future runs. Treat these results as single-run observations, not exact seed-42 replications. No timing or memory claims are made.
