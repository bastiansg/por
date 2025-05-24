import tiktoken

from common.logger import get_logger


logger = get_logger(__name__)


tiktoken_encoder = tiktoken.encoding_for_model("gpt-4o")


def validate_num_tokens(text: str, max_num_tokens: int = 512) -> bool:
    num_tokens = len(tiktoken_encoder.encode(text))
    logger.info(f"num_tokens => {num_tokens}")

    if num_tokens <= max_num_tokens:
        return True

    return False
