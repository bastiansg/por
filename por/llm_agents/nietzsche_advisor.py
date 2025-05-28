from pydantic import BaseModel, StrictStr, Field
from pydantic_extra_types.language_code import LanguageName

from common.cache import RedisCache

from por.conf import llm_agents
from llm_agents.meta.interfaces import LLMAgent


class NietzscheAdvisorInput(BaseModel):
    dreams_and_desires: StrictStr
    nietzsche_text_chunks: list[StrictStr]
    output_language: LanguageName


class NietzscheAdvisorOutput(BaseModel):
    nietzsche_advise: StrictStr = Field(
        description="A profound, poetic, and incisive piece of Nietzschean advice.",
        min_length=1,
    )


class NietzscheAdvisor(LLMAgent[NietzscheAdvisorInput, NietzscheAdvisorOutput]):
    def __init__(
        self,
        conf_path=f"{llm_agents.__path__[0]}/nietzsche-advisor.yml",
        max_concurrency: int = 10,
        cache: RedisCache = None,
    ):
        super().__init__(
            conf_path=conf_path,
            agent_input=NietzscheAdvisorInput,
            agent_output=NietzscheAdvisorOutput,
            retries=3,
            max_concurrency=max_concurrency,
            cache=cache,
        )
