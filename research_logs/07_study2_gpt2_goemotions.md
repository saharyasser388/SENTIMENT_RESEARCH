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
The best checkpoint was selected at epoch 3.

| Metric | Validation | Test |
| --- | ---: | ---: |
| Accuracy | 0.7065 | 0.7055 |
| Macro-F1 | 0.6269 | 0.6303 |
| Macro precision | Not recorded | 0.6561 |
| Macro recall | Not recorded | 0.6134 |
| Weighted-F1 | Not recorded | 0.7021 |

Test per-class F1, in encoded class order:

| Emotion | F1 |
| --- | ---: |
| anger | 0.5469 |
| disgust | 0.5556 |
| fear | 0.6016 |
| joy | 0.8297 |
| neutral | 0.6102 |
| sadness | 0.6112 |
| surprise | 0.6570 |

Test confusion matrix (rows are true labels; columns are predictions; class
order is anger, disgust, fear, joy, neutral, sadness, surprise):

```text
[[274, 10,  3,   45, 16,  30,  164],
 [  9, 35,  1,    6,  1,   2,    9],
 [  2,  5, 37,    5,  3,   5,   13],
 [ 25,  0,  4, 1635, 12,  43,  183],
 [ 24,  5,  3,   31,155,  12,   58],
 [ 15,  4,  0,   46,  6, 316,   93],
 [111,  4,  5,  271, 27, 146, 1038]]
```

## Observations
The local classifier smoke test passed with output shape `[2, 7]`. GPT-2 length
analysis found P95 31, P99 35, and only 11 of 49,469 examples (0.02%) above
the selected length of 64. Joy achieved the highest test F1 (0.8297), while
anger achieved the lowest (0.5469).

## Problems encountered
Training time, inference time, and peak GPU memory were not retained in the
reported comparison output.

## Interpretation
For this run, the validation-selected GPT-2 checkpoint achieved test Macro-F1
0.6303 and test accuracy 0.7055.

## Next step
Repeat the baseline across multiple fixed seeds before treating the single-run
difference as an architecture-level conclusion.
