# Study 2: BERT GoEmotions

## Objective
Fine-tune BERT-base-uncased for the same seven-class task.

## Why this step is needed
This supplies the encoder-only comparator under the same split and evaluation policy.

## Configuration
Seed 42; 3 epochs; batch size 8; AdamW; learning rate 2e-5; weight decay 0.01; cross-entropy; CUDA mixed precision when available; validation Macro-F1 selection; confirmed maximum length 64.

The experiment host has an NVIDIA GeForce RTX 2060 with 6,144 MiB VRAM,
NVIDIA driver 617.42, CUDA UMD 13.4, and Windows WDDM mode. The post-run
`nvidia-smi` snapshot was taken while idle, so it does not measure training
utilization or peak memory.

## Architecture
Hugging Face `google-bert/bert-base-uncased`; first-token (`[CLS]`) final hidden state; `Linear(768, 7)`. All parameters are trainable.

## Dataset
The published `train` (39,575), `valid` (4,947), and `test` (4,947) splits are
used unchanged, exactly as for GPT-2.

## What changed
Added the model, pretrained-load smoke test, training entry point, and held-out evaluation script.

## Results
The best checkpoint was selected at epoch 1.

| Metric | Validation | Test |
| --- | ---: | ---: |
| Accuracy | 0.7079 | 0.7065 |
| Macro-F1 | 0.6125 | 0.6092 |
| Macro precision | Not recorded | 0.6583 |
| Macro recall | Not recorded | 0.5758 |
| Weighted-F1 | Not recorded | 0.6991 |

Test per-class F1, in encoded class order:

| Emotion | F1 |
| --- | ---: |
| anger | 0.5328 |
| disgust | 0.4860 |
| fear | 0.5802 |
| joy | 0.8275 |
| neutral | 0.6210 |
| sadness | 0.5383 |
| surprise | 0.6789 |

Test confusion matrix (rows are true labels; columns are predictions; class
order is anger, disgust, fear, joy, neutral, sadness, surprise):

```text
[[248,  8,  6,   48, 16, 21,  195],
 [ 10, 26,  1,    6,  3,  0,   17],
 [  0,  0, 38,    7,  7,  4,   14],
 [ 21,  2,  4, 1645, 13, 25,  192],
 [ 21,  2,  3,   32,163,  5,   62],
 [ 22,  2,  0,   67,  8,225,  156],
 [ 67,  4,  9,  269, 27, 76, 1150]]
```

## Observations
The model-specific tokenizer is intentionally retained; all experimental policy
settings otherwise match GPT-2. BERT length analysis found P95 33, P99 38, and
only 3 of 49,469 examples (0.01%) above the selected length of 64. Joy achieved
the highest test F1 (0.8275), while disgust achieved the lowest (0.4860).

## Problems encountered
Training time, inference time, and peak GPU memory were not retained in the
reported comparison output. A post-run audit found that the original entry
point set seed 42 inside the shared training function, after constructing the
random classification head. The data order and optimization were seeded, but
the initial head weights were not guaranteed reproducible. The entry point now
seeds before model construction; the reported checkpoint itself is unchanged.
When
`BertModel` is loaded from the upstream pretraining checkpoint, Transformers
may report the `cls.predictions.*` and `cls.seq_relationship.*` keys as
unexpected. Those keys belong to BERT's masked-language-model and
next-sentence-prediction pretraining heads; this study intentionally loads the
backbone and supplies its own seven-class head, so that load report is not a
training error.

## Interpretation
For this run, the validation-selected BERT checkpoint achieved test Macro-F1
0.6092 and test accuracy 0.7065.

## Next step
Repeat the baseline across multiple fixed seeds before treating the single-run
difference as an architecture-level conclusion.
