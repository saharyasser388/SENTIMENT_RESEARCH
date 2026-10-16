# Study 2: GoEmotions-Ekman Dataset

## Objective
Inspect `Jsevisal/go_emotions_ekman_unilabel`, confirm its schema and class order, and fix one split policy for both models.

## Why this step is needed
A shared, single-label, seven-class dataset is necessary for a fair architecture comparison.

## Configuration
Seed: 42. Inspection command: `python -m scripts.12_inspect_goemotions`.

## Architecture
Not applicable.

## Dataset
The requested Hugging Face dataset is used directly. Its published splits are
`train` (39,575 rows), `valid` (4,947 rows), and `test` (4,947 rows). The text
field is `sentence`; the label field is `labels`.

The encoded class order is:

| ID | Emotion |
| ---: | --- |
| 0 | anger |
| 1 | disgust |
| 2 | fear |
| 3 | joy |
| 4 | neutral |
| 5 | sadness |
| 6 | surprise |

Both models preserve these published splits without resampling. The helper
also accepts the conventional name `validation` (with precedence over `valid`)
for compatibility with a future dataset revision.

## What changed
Added shared schema/class-order validation, `valid`/`validation` split support,
dataset inspection, and separate GPT-2/BERT length-analysis scripts.

## Results
Dataset inspection confirmed the split sizes, field names, and class order
above. The measured class distributions are:

| Emotion | Train | Validation (`valid`) | Test |
| --- | ---: | ---: | ---: |
| anger | 4,336 | 542 | 542 |
| disgust | 508 | 64 | 63 |
| fear | 554 | 69 | 70 |
| joy | 15,216 | 1,902 | 1,902 |
| neutral | 2,300 | 287 | 288 |
| sadness | 3,844 | 481 | 480 |
| surprise | 12,817 | 1,602 | 1,602 |
| **Total** | **39,575** | **4,947** | **4,947** |

Length analysis covered all 49,469 examples:

| Statistic | GPT-2 | BERT |
| --- | ---: | ---: |
| Minimum | 1 | 3 |
| Maximum | 1,435 | 316 |
| Mean | 16.72 | 18.98 |
| Median | 16 | 18 |
| P90 | 29 | 31 |
| P95 | 31 | 33 |
| P99 | 35 | 38 |
| Above 32 | 1,293 (2.61%) | 3,408 (6.89%) |
| Above 64 | 11 (0.02%) | 3 (0.01%) |
| Above 128 | 5 (0.01%) | 1 (0.00%) |
| Above 256 | 2 (0.00%) | 1 (0.00%) |

## Observations
The dataset is single-label and already provides all three required splits.
No custom validation partition is needed. A shared maximum length of 64 retains
the complete token sequence for 99.98% of GPT-2 examples and 99.99% of BERT
examples while avoiding padding every batch to the extreme outliers.

## Problems encountered
Initial online inspection was blocked by the environment proxy. A later cached
inspection supplied the verified schema and splits.

## Interpretation
The dataset structure and shared maximum length of 64 are confirmed. The very
long GPT-2 maximum is an outlier measured without truncation; training applies
the selected limit before inputs reach the model.

## Next step
Train GPT-2 and BERT with the confirmed common maximum length of 64, selecting
each best checkpoint by validation Macro-F1.
