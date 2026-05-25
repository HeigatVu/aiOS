import os
from tokenizers import Tokenizer, pre_tokenizers, trainers, models
from datasets import load_dataset
from transformers import PreTrainedTokenizerFast


def tokenizer_dataset(dataset):
    # word-based
    tokenizer_en = Tokenizer(models.WordLevel(unk_token="<unk>"))
    tokenizer_vi = Tokenizer(models.WordLevel(unk_token="<unk>"))

    tokenizer_en.pre_tokenizer = pre_tokenizers.Whitespace()
    tokenizer_vi.pre_tokenizer = pre_tokenizers.Whitespace()

    trainer = trainers.WordLevelTrainer(
        vocab_size=15000,
        min_frequency=2,
        special_tokens=["<unk>", "<pad>", "<bos>", "<eos>"],
    )

    # train tokenizers
    tokenizer_en.train_from_iterator(ds["train"]["en"], trainer)
    tokenizer_vi.train_from_iterator(ds["train"]["vi"], trainer)

    # tokenizers
    tokenizer_en.save("tokenizer_en.json")
    tokenizer_vi.save("tokenizer_vi.json")

    return tokenizer_en, tokenizer_vi


def encoding(tokenizer_en, tokenizer_vi, examples):
    MAX_LEN = 75
    tokenizer_en = PreTrainedTokenizerFast(
        tokenizer_file="tokenizer_en.json",
        unk_token="<unk>",
        pad_token="<pad>",
        bos_token="bos",
        eos_token="<eos>",
    )
    tokenizer_vi = PreTrainedTokenizerFast(
        tokenizer_file="tokenizer_vi.json",
        unk_token="<unk>",
        pad_token="<pad>",
        bos_token="bos",
    )

    # preprocessing tokenizer
    src_texts = examples["en"]
    tgt_texts = ["<bos>" + sent + "<eos>" for sent in examples["vi"]]

    src_encodings = tokenizer_en(
        src_texts, padding="max_length", truncation=True, max_length=MAX_LEN
    ) 


if __name__ == "__main__":
    ds = load_dataset("thainq107/iwslt2015-en-vi")
    tokenizer_en, tokenizer_vi = tokenizer_dataset(ds)

    # Example usage
    en_text = "This is an example sentence in English."
    vi_text = "Đây là một câu tiếng Anh trong dịch."

    en_tokens = tokenizer_en.encode(en_text)
    vi_tokens = tokenizer_vi.encode(vi_text)

    print("English tokens:", en_tokens)
    print("Vietnamese tokens:", vi_tokens)
