from pydantic import BaseModel, StrictStr, Field
from pydantic_extra_types.language_code import LanguageName

from common.cache import RedisCache

from por.conf import llm_agents
from llm_agents.meta.interfaces import LLMAgent


class TSAdvisorInput(BaseModel):
    love_status: StrictStr
    ts_text_chunks: list[StrictStr]
    output_language: LanguageName


class TSAdvisorOutput(BaseModel):
    taylor_swift_advise: StrictStr = Field(
        description="A heartfelt, lyrical, and emotionally attuned piece of Taylor Swift advice.",
        min_length=1,
    )


class TSAdvisor(LLMAgent[TSAdvisorInput, TSAdvisorOutput]):
    def __init__(
        self,
        conf_path=f"{llm_agents.__path__[0]}/ts-advisor.yml",
        max_concurrency: int = 10,
        cache: RedisCache = None,
    ):
        super().__init__(
            conf_path=conf_path,
            agent_input=TSAdvisorInput,
            agent_output=TSAdvisorOutput,
            retries=3,
            max_concurrency=max_concurrency,
            cache=cache,
        )
