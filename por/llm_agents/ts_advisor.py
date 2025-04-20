from pydantic import BaseModel, StrictStr
from pydantic_extra_types.language_code import LanguageName

from common.cache import RedisCache

from por.conf import agents
from llm_agents.meta.interfaces import LLMAgent


class TSAdvisorAdvisorInput(BaseModel):
    person_description: StrictStr
    ts_text_chunks: list[StrictStr]
    output_language: LanguageName


class TSAdvisorAdvisorOutput(BaseModel):
    taylor_swift_advise: StrictStr


class TSAdvisor(LLMAgent[TSAdvisorAdvisorInput, TSAdvisorAdvisorOutput]):
    def __init__(
        self,
        conf_path=f"{agents.__path__[0]}/ts-advisor.yml",
        max_concurrency: int = 10,
        cache: RedisCache = None,
    ):
        super().__init__(
            conf_path=conf_path,
            agent_input=TSAdvisorAdvisorInput,
            agent_output=TSAdvisorAdvisorOutput,
            max_concurrency=max_concurrency,
            cache=cache,
        )
