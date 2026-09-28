from pydantic import PositiveInt, StrictInt, StrictStr
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    redis_host: StrictStr = "por-redis"
    redis_port: StrictInt = 6379
    redis_db: StrictInt = 0
    caption_header: StrictStr = (
        "In the Style of P0RIMG, a high-contrast black-and-white fashion portrait "
        "illustration with crisp contour lines, bold flat-black shapes, flowing "
        "optical wave patterns, and a sparse white background:"
    )
    t5_tokenizer_name: StrictStr = "google/t5-v1_1-xxl"
    flux_max_tokens: PositiveInt = 512


config = Config()
