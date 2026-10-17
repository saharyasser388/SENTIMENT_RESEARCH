"""Shared dataset constants and schema helpers for Study 2."""
from datasets import ClassLabel, DatasetDict, load_dataset

DATASET_NAME = "Jsevisal/go_emotions_ekman_unilabel"
SEED = 42
EXPECTED_LABEL_NAMES = ["anger", "disgust", "fear", "joy", "neutral", "sadness", "surprise"]


def load_goemotions():
    return load_dataset(DATASET_NAME)


def infer_schema(dataset: DatasetDict):
    first_split = next(iter(dataset.values()))
    features = first_split.features
    text_fields = [name for name, feature in features.items() if getattr(feature, "dtype", None) == "string"]
    label_fields = [name for name, feature in features.items() if isinstance(feature, ClassLabel)]
    if len(text_fields) != 1 or len(label_fields) != 1:
        raise ValueError(f"Expected one text and one ClassLabel field; got {features}")
    label_feature = features[label_fields[0]]
    if len(label_feature.names) != 7:
        raise ValueError(f"Expected 7 classes, got {label_feature.names}")
    return text_fields[0], label_fields[0], list(label_feature.names)


def prepare_study2_splits(dataset: DatasetDict, label_field, validation_size=0.1):
    """Preserve published splits, accepting either validation split name.

    Optional arguments remain for compatibility with existing callers.
    Missing validation data requires inspection, never silent resampling.
    """
    if "train" not in dataset or "test" not in dataset:
        raise ValueError(
            "Study 2 requires published train and test splits; got "
            f"{sorted(dataset.keys())}."
        )
    if "validation" in dataset:
        return dataset["train"], dataset["validation"], dataset["test"]

    if "valid" in dataset:
        return dataset["train"], dataset["valid"], dataset["test"]
    raise ValueError(
        "Study 2 requires a published 'valid' or 'validation' split. "
        "Inspect the dataset revision before training; do not resample train."
    )


def require_standard_splits(dataset: DatasetDict):
    """Compatibility wrapper for checkouts using the original helper name.

    Both helper names preserve the same published splits.
    """
    _, label_field, _ = infer_schema(dataset)
    return prepare_study2_splits(dataset, label_field)
