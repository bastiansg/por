from pydantic import BaseModel, StrictStr, Field
from pydantic_extra_types.language_code import LanguageName

from common.cache import RedisCache

from por.conf import llm_agents
from llm_agents.meta.interfaces import LLMAgent


class LMAdvisorInput(BaseModel):
    love_status: StrictStr
    lm_text_chunks: list[StrictStr]
    output_language: LanguageName


class LMAdvisorOutput(BaseModel):
    luis_miguel_advise: StrictStr = Field(
        description="A heartfelt, romantic, and emotionally resonant piece of Luis Miguel-style advice.",
        min_length=1,
    )


class LMAdvisor(LLMAgent[LMAdvisorInput, LMAdvisorOutput]):
    def __init__(
        self,
        conf_path=f"{llm_agents.__path__[0]}/lm-advisor.yml",
        max_concurrency: int = 10,
        cache: RedisCache = None,
    ):
        super().__init__(
            conf_path=conf_path,
            agent_input=LMAdvisorInput,
            agent_output=LMAdvisorOutput,
            retries=3,
            max_concurrency=max_concurrency,
            cache=cache,
        )
