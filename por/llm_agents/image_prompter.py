from pydantic import BaseModel, StrictStr, Field
from pydantic_extra_types.language_code import LanguageName

from common.cache import RedisCache

from por.conf import llm_agents
from llm_agents.meta.interfaces import LLMAgent


class ImagePrompterDeps(BaseModel):
    psychological_profile: StrictStr
    physical_description: StrictStr
    clothing_description: StrictStr
    output_language: LanguageName


class ImagePrompterOutput(BaseModel):
    image_generation_prompt: StrictStr = Field(
        description="The prompt for the portrait image generation.",
        min_length=1,
    )


class ImagePrompter(LLMAgent[ImagePrompterDeps, ImagePrompterOutput]):
    def __init__(
        self,
        conf_path=f"{llm_agents.__path__[0]}/image-prompter.yml",
        max_concurrency: int = 10,
        cache: RedisCache = None,
    ):
        super().__init__(
            conf_path=conf_path,
            deps_type=ImagePrompterDeps,
            output_type=ImagePrompterOutput,
            retries=3,
            max_concurrency=max_concurrency,
            cache=cache,
        )
