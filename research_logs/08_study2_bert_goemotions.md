# Study 2: BERT GoEmotions

## Objective
Fine-tune BERT-base-uncased for the same seven-class task.

## Why this step is needed
This supplies the encoder-only comparator under the same split and evaluation policy.

## Configuration
Seed 42; 3 epochs; batch size 8; AdamW; learning rate 2e-5; weight decay 0.01; cross-entropy; CUDA mixed precision when available; validation Macro-F1 selection; confirmed maximum length 64.

## Architecture
Hugging Face `google-bert/bert-base-uncased`; first-token (`[CLS]`) final hidden state; `Linear(768, 7)`. All parameters are trainable.

## Dataset
The published `train` (39,575), `valid` (4,947), and `test` (4,947) splits are
used unchanged, exactly as for GPT-2.

## What changed
Added the model, pretrained-load smoke test, training entry point, and held-out evaluation script.

## Results
Not run because remote Hugging Face artifacts were blocked. No metrics or checkpoint are claimed.

## Observations
The model-specific tokenizer is intentionally retained; all experimental policy
settings otherwise match GPT-2. BERT length analysis found P95 33, P99 38, and
only 3 of 49,469 examples (0.01%) above the selected length of 64.

## Problems encountered
The configured proxy returned HTTP 403 for Hugging Face access. When
`BertModel` is loaded from the upstream pretraining checkpoint, Transformers
may report the `cls.predictions.*` and `cls.seq_relationship.*` keys as
unexpected. Those keys belong to BERT's masked-language-model and
next-sentence-prediction pretraining heads; this study intentionally loads the
backbone and supplies its own seven-class head, so that load report is not a
training error.

## Interpretation
No comparison is possible until both complete runs exist.

## Next step
Run `python -m training.train_bert_goemotions` after the GPT-2 baseline and
record the emitted validation and held-out test metrics here.
