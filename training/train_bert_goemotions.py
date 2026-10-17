from transformers import AutoTokenizer
from models.bert_classifier import BertClassifier
from training.goemotions_common import seed_everything, train

MODEL_NAME = "google-bert/bert-base-uncased"
CHECKPOINT_PATH = "checkpoints/study2_bert_goemotions_best.pt"


def main():
    # BertClassifier creates a new randomly initialized seven-class head.
    # Seed before construction, not only after the model already exists.
    seed_everything()
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    train(BertClassifier(MODEL_NAME, num_classes=7), tokenizer, CHECKPOINT_PATH, MODEL_NAME)


if __name__ == "__main__":
    main()
