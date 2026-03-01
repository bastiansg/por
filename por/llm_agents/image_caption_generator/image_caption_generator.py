from pydantic_ai import ToolOutput
from pydantic_ai.models import Model
from pydantic import BaseModel, Field, StrictStr

from common.cache import RedisCache
from llm_agents.meta.interfaces import LLMAgent
from por.llm_agents import image_caption_generator


class ImageCaptionGeneratorOutput(BaseModel):
    image_caption: StrictStr = Field(
        description="A very detailed, ready-to-use image generation caption derived from the provided image.",
        min_length=1,
    )


class ImageCaptionGenerator(LLMAgent[None, ImageCaptionGeneratorOutput]):
    def __init__(
        self,
        conf_path: str = f"{image_caption_generator.__path__[0]}/image-caption-generator.yml",
        model: Model | None = None,
        max_concurrency: int = 10,
        cache: RedisCache | None = None,
        retries: int = 3,
    ):
        super().__init__(
            conf_path=conf_path,
            output_type=ToolOutput(ImageCaptionGeneratorOutput),  # type: ignore
            model=model,
            max_concurrency=max_concurrency,
            cache=cache,
            retries=retries,
        )
