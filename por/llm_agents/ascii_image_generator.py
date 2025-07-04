from pydantic import BaseModel, StrictStr, Field, field_validator

from common.cache import RedisCache

from por.conf import llm_agents
from llm_agents.meta.interfaces import LLMAgent


class ASCIIImageGeneratorDeps(BaseModel):
    question: StrictStr
    psychological_profile: StrictStr
    physical_description: StrictStr
    clothing_description: StrictStr


class ASCIIImageGeneratorOutput(BaseModel):
    ascii_image: list[StrictStr] = Field(
        description="The ASCII image.",
        min_length=48,
        max_length=48,
    )

    @field_validator("ascii_image")
    def ascii_image_validator(cls, value: list[str]) -> list[str]:
        if any(v for v in value if len(v) != 48):
            raise ValueError("Invalid number of chars.")

        return value


class ASCIIImageGenerator(
    LLMAgent[ASCIIImageGeneratorDeps, ASCIIImageGeneratorOutput]
):
    def __init__(
        self,
        conf_path=f"{llm_agents.__path__[0]}/ascii-image-generator.yml",
        max_concurrency: int = 10,
        cache: RedisCache = None,
    ):
        super().__init__(
            conf_path=conf_path,
            deps_type=ASCIIImageGeneratorDeps,
            output_type=ASCIIImageGeneratorOutput,
            retries=3,
            max_concurrency=max_concurrency,
            cache=cache,
        )
