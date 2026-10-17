# Study 2: GoEmotions-Ekman Dataset

## Verified dataset contract

Offline inspection on 2026-10-18 confirmed the cached `Jsevisal/go_emotions_ekman_unilabel` dataset (cache revision `be5851241c507d83c14d4f276814750f37a421ec`):

- Text field: `sentence`; ClassLabel field: `labels`.
- Published splits: `train` 39,575; `valid` 4,947; `test` 4,947.
- Encoded class order: anger, disgust, fear, joy, neutral, sadness, surprise.
- Shared maximum length: 64, as recorded in both completed result artifacts.

These observations supersede the earlier proxy-blocked placeholders and the incorrect claim that validation must be resampled from train. They confirm the local cache, not a fresh upstream download.

## Split policy

Both models use `prepare_study2_splits`. It preserves the published train, validation, and test objects unchanged, accepts `valid` or `validation` (the latter takes precedence), and raises an error if validation is absent. It never silently creates a new split. Seed 42 and validation Macro-F1 selection remain configured; the test set is reserved for final evaluation.

## Historical evidence

The existing stash based on `7715d45` contains a `valid` alias fix and a cached inspection dated 2026-09-21 with the same schema and sizes. Later branch code handled only `validation` and would have resampled this dataset. The audit restores the published-split policy without applying the stash or altering Study 1.

The saved result artifacts contain 4,947 examples in each validation/test confusion matrix but no dataset revision or row IDs. This does not establish the exact producing code or historical split membership. See [the comparison audit](09_study2_comparison.md) for provenance limits. No token-length statistics were recomputed.
