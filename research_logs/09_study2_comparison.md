# Study 2: GPT-2 vs BERT Comparison

> **Status: baseline comparison complete.** Both validation-selected
> checkpoints were evaluated once on the published held-out test split. These
> are single-run results with seed 42, not evidence of universal architecture
> superiority.

## Objective
Compare decoder-only GPT-2 Small and encoder-only BERT-base-uncased on one seven-class GoEmotions-Ekman task.

## Why this step is needed
It addresses the Study 2 research question while controlling the split, seed, epochs, optimizer, learning rate, loss, checkpoint metric, and evaluation implementation.

## Configuration
Both completed runs used seed 42, 3 epochs, batch size 8, AdamW at 2e-5 with weight decay 0.01, dynamic padding, a measured common maximum length of 64, cross-entropy, CUDA AMP, and validation Macro-F1 selection.

### Hardware snapshot

The experiment host was verified on 2026-10-16 with:

| Item | Value |
| --- | --- |
| GPU | NVIDIA GeForce RTX 2060 |
| Dedicated VRAM | 6,144 MiB |
| NVIDIA driver | 617.42 |
| CUDA UMD | 13.4 |
| Driver mode | WDDM |

The snapshot was captured after training with no active GPU processes and
0 MiB reported as in use. It documents the available hardware, not training
time, utilization, or peak allocated memory.

## Architecture
GPT-2 uses its last real token; BERT uses its `[CLS]` hidden state. Both attach a 768-to-7 linear classifier.

## Dataset
Both entry points use the published `train` (39,575), `valid` (4,947), and
`test` (4,947) splits unchanged. The encoded class order is anger, disgust,
fear, joy, neutral, sadness, surprise.

## What changed
A common multiclass evaluator reports accuracy, macro precision/recall/F1, weighted F1, ordered per-class scores, and a 7-by-7 confusion matrix.

## Results

| Metric | GPT-2 | BERT-base-uncased |
| --- | ---: | ---: |
| Parameters | 124,445,191 | 109,487,623 |
| Best Epoch | 3 | 1 |
| Validation Accuracy | 0.7065 | **0.7079** |
| Validation Macro-F1 | **0.6269** | 0.6125 |
| Test Accuracy | 0.7055 | **0.7065** |
| Test Macro Precision | 0.6561 | **0.6583** |
| Test Macro Recall | **0.6134** | 0.5758 |
| Test Macro-F1 | **0.6303** | 0.6092 |
| Test Weighted F1 | **0.7021** | 0.6991 |

| Emotion | GPT-2 F1 | BERT F1 |
| --- | ---: | ---: |
| Anger | **0.5469** | 0.5328 |
| Disgust | **0.5556** | 0.4860 |
| Fear | **0.6016** | 0.5802 |
| Joy | **0.8297** | 0.8275 |
| Neutral | 0.6102 | **0.6210** |
| Sadness | **0.6112** | 0.5383 |
| Surprise | 0.6570 | **0.6789** |

GPT-2 test confusion matrix (rows are true labels and columns are predictions):

```text
[[274, 10,  3,   45, 16,  30,  164],
 [  9, 35,  1,    6,  1,   2,    9],
 [  2,  5, 37,    5,  3,   5,   13],
 [ 25,  0,  4, 1635, 12,  43,  183],
 [ 24,  5,  3,   31,155,  12,   58],
 [ 15,  4,  0,   46,  6, 316,   93],
 [111,  4,  5,  271, 27, 146, 1038]]
```

BERT test confusion matrix:

```text
[[248,  8,  6,   48, 16, 21,  195],
 [ 10, 26,  1,    6,  3,  0,   17],
 [  0,  0, 38,    7,  7,  4,   14],
 [ 21,  2,  4, 1645, 13, 25,  192],
 [ 21,  2,  3,   32,163,  5,   62],
 [ 22,  2,  0,   67,  8,225,  156],
 [ 67,  4,  9,  269, 27, 76, 1150]]
```

Elapsed training time, dedicated inference time, and peak GPU memory were not
retained in the reported comparison output.

## Observations
GPT-2 used 14,957,568 more parameters and achieved test Macro-F1 0.6303,
0.0211 above BERT. BERT achieved test accuracy 0.7065, 0.0010 above GPT-2,
and slightly higher macro precision. GPT-2's advantage came from macro recall
and higher F1 on anger, disgust, fear, joy, and sadness. BERT was higher on
neutral and surprise. BERT selected epoch 1, whereas GPT-2 selected epoch 3.

## Problems encountered
Runtime and peak-memory measurements were not preserved; an idle post-run
`nvidia-smi` snapshot cannot reconstruct them. The efficiency comparison is
therefore limited to parameter counts. Only one seeded run per model is
available, preventing uncertainty estimates. A post-run audit also found that
the original entry points seeded the training process after each classifier
head had already been randomly initialized. The split, batch order, and
optimization were seeded, but exact seed-42 replay of the reported runs is not
guaranteed. This ordering is fixed for future runs; the reported results remain
valid single-run observations rather than deterministic seed-42 replications.

## Interpretation
On this controlled run, GPT-2 provided the stronger class-balanced result
(Macro-F1), while BERT matched it on overall accuracy with fewer parameters.
The result supports a scoped baseline conclusion only; it does not establish
that GPT-2 is universally better than BERT.

## Next step
Before Study 3, repeat both baselines across multiple fixed seeds and report
mean and standard deviation. Study 3 can then test parameter-efficient
adaptation or another architecture while preserving this split and evaluator.
