import tiktoken


tiktoken_encoder = tiktoken.encoding_for_model("gpt-4o")


def get_num_tokens(text: str) -> bool:
    return len(tiktoken_encoder.encode(text))
