from pydantic import BaseModel, StrictStr, Field

from common.cache import RedisCache

from por.conf import llm_agents
from llm_agents.meta.interfaces import LLMAgent


class ImageDescriberInput(BaseModel):
    description_guidelines: StrictStr


class ImageDescriberOutput(BaseModel):
    people_description: StrictStr = Field(
        description="Description of all people in the image.",
        min_length=1,
    )

    scene_description: StrictStr = Field(
        description="Description of the surrounding scene.",
        min_length=1,
    )


class ImageDescriber(LLMAgent[ImageDescriberInput, ImageDescriberOutput]):
    def __init__(
        self,
        conf_path=f"{llm_agents.__path__[0]}/image-describer.yml",
        max_concurrency: int = 10,
        cache: RedisCache = None,
    ):
        super().__init__(
            conf_path=conf_path,
            agent_input=ImageDescriberInput,
            agent_output=ImageDescriberOutput,
            retries=3,
            max_concurrency=max_concurrency,
            cache=cache,
        )
