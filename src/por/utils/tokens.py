from functools import lru_cache

from pydantic_ai import ModelRetry
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


def validate_t5_token_count(token_count: int, max_tokens: int) -> None:
    if token_count > max_tokens:
        raise ModelRetry(
            f"The formatted FLUX prompt contains {token_count} T5 tokens; "
            f"rewrite it using at most {max_tokens} tokens."
        )
