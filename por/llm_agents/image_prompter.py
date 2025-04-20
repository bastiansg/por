from pydantic import BaseModel, StrictStr
from pydantic_extra_types.language_code import LanguageName

from common.cache import RedisCache

from por.conf import agents
from llm_agents.meta.interfaces import LLMAgent


class ImagePrompterInput(BaseModel):
    image_description: StrictStr
    person_description: StrictStr
    nietzsche_advice: StrictStr
    jung_advice: StrictStr
    ts_advice: StrictStr
    output_language: LanguageName


class ImagePrompterOutput(BaseModel):
    image_generation_prompt: StrictStr


class ImagePrompter(LLMAgent[ImagePrompterInput, ImagePrompterOutput]):
    def __init__(
        self,
        conf_path=f"{agents.__path__[0]}/image-prompter.yml",
        max_concurrency: int = 10,
        cache: RedisCache = None,
    ):
        super().__init__(
            conf_path=conf_path,
            agent_input=ImagePrompterInput,
            agent_output=ImagePrompterOutput,
            max_concurrency=max_concurrency,
            cache=cache,
        )
