from pydantic import BaseModel, StrictStr, Field

from common.cache import RedisCache

from por.conf import agents
from llm_agents.meta.interfaces import LLMAgent


class VKImageDescriberInput(BaseModel):
    description_guidelines: StrictStr


class VKImageDescriberOutput(BaseModel):
    model_description: StrictStr = Field(
        description="A detailed description of the person modeling the outfit, including their pose, body proportions, posture, hairstyle, and any visible physical traits or expressions."
    )

    clothing_description: StrictStr = Field(
        description="A detailed description of the clothing worn by the model, including the outfit's design, structure, fabrics, textures, colors, accessories, and embellishments."
    )


class VKImageDescriber(LLMAgent[VKImageDescriberInput, VKImageDescriberOutput]):
    def __init__(
        self,
        conf_path=f"{agents.__path__[0]}/vk-image-describer.yml",
        max_concurrency: int = 10,
        cache: RedisCache = None,
    ):
        super().__init__(
            conf_path=conf_path,
            agent_input=VKImageDescriberInput,
            agent_output=VKImageDescriberOutput,
            max_concurrency=max_concurrency,
            cache=cache,
        )
