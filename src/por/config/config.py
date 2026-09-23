from pydantic import PositiveInt, StrictInt, StrictStr
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    redis_host: StrictStr = "por-redis"
    redis_port: StrictInt = 6379
    redis_db: StrictInt = 0
    caption_header: StrictStr = (
        "In the Style of PBFR, a raw monochrome ink sketch with bold, "
        "expressive linework of:"
    )
    t5_tokenizer_name: StrictStr = "google/t5-v1_1-xxl"
    flux_max_tokens: PositiveInt = 512


config = Config()
