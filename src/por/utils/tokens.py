from functools import lru_cache

from transformers import AutoTokenizer, PreTrainedTokenizerBase


@lru_cache
def _get_t5_tokenizer(tokenizer_name: str) -> PreTrainedTokenizerBase:
    return AutoTokenizer.from_pretrained(tokenizer_name)


def count_t5_tokens(text: str, tokenizer_name: str) -> int:
    return len(
        _get_t5_tokenizer(tokenizer_name).encode(
            text,
            add_special_tokens=True,
            truncation=False,
        )
    )
