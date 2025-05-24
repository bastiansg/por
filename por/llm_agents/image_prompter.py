from pydantic import BaseModel, StrictStr, Field
from pydantic_extra_types.language_code import LanguageName

from common.cache import RedisCache

from por.conf import llm_agents
from llm_agents.meta.interfaces import LLMAgent


class ImagePrompterInput(BaseModel):
    people_description: StrictStr
    scene_description: StrictStr
    psychological_description: StrictStr
    output_language: LanguageName


class ImagePrompterOutput(BaseModel):
    people_description: StrictStr = Field(
        description="An adapted version of the original people description.",
        min_length=1,
    )

    scene_description: StrictStr = Field(
        description="An adapted version of the original scene description.",
        min_length=1,
    )


class ImagePrompter(LLMAgent[ImagePrompterInput, ImagePrompterOutput]):
    def __init__(
        self,
        conf_path=f"{llm_agents.__path__[0]}/image-prompter.yml",
        max_concurrency: int = 10,
        cache: RedisCache = None,
    ):
        super().__init__(
            conf_path=conf_path,
            agent_input=ImagePrompterInput,
            agent_output=ImagePrompterOutput,
            retries=3,
            max_concurrency=max_concurrency,
            cache=cache,
        )
