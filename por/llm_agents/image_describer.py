from pydantic import BaseModel, StrictStr, Field

from common.cache import RedisCache

from por.conf import llm_agents
from llm_agents.meta.interfaces import LLMAgent


class ImageDescriberOutput(BaseModel):
    physical_description: StrictStr = Field(
        description="Physical description of the people in the provided image.",
        min_length=1,
    )

    clothing_description: StrictStr = Field(
        description="Clothing and accessory description of the people in the provided image.",
        min_length=1,
    )


class ImageDescriber(LLMAgent[None, ImageDescriberOutput]):
    def __init__(
        self,
        conf_path=f"{llm_agents.__path__[0]}/image-describer.yml",
        max_concurrency: int = 10,
        cache: RedisCache = None,
    ):
        super().__init__(
            conf_path=conf_path,
            output_type=ImageDescriberOutput,
            retries=3,
            max_concurrency=max_concurrency,
            cache=cache,
        )
