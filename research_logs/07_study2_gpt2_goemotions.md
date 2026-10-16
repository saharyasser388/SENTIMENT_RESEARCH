# Study 2: GPT-2 GoEmotions

## Objective
Fine-tune the validated custom GPT-2 Small backbone for seven-class emotion classification.

## Why this step is needed
This supplies the decoder-only side of the controlled comparison.

## Configuration
Seed 42; 3 epochs; batch size 8; AdamW; learning rate 2e-5; weight decay 0.01; cross-entropy; CUDA mixed precision when available; validation Macro-F1 checkpoint selection; confirmed maximum length 64.

## Architecture
Custom pretrained GPT-2 Small, last non-padding token representation, and `Linear(768, 7)`. All parameters are trainable.

## Dataset
The published `train` (39,575), `valid` (4,947), and `test` (4,947) splits are
used unchanged. BERT receives these exact same examples.

## What changed
Added a seven-class smoke test, training entry point, checkpoint metadata, and held-out checkpoint evaluator. The existing generic classifier remains backward compatible with Study 1's two-class default.

## Results
Not run: dataset/model downloads were blocked by the environment proxy. No checkpoint or metrics are claimed.

## Observations
The local randomly initialized classifier smoke test passed with output shape
`[2, 7]`. GPT-2 length analysis found P95 31, P99 35, and only 11 of 49,469
examples (0.02%) above the selected length of 64.

## Problems encountered
Remote artifacts were unavailable, and this environment has no verified full training run.

## Interpretation
Implementation readiness is not an empirical model result.

## Next step
Run `python -m training.train_gpt2_goemotions` on CUDA and record the emitted
validation and held-out test metrics here.
