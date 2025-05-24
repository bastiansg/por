from pydantic import BaseModel, StrictStr, Field
from pydantic_extra_types.language_code import LanguageName

from common.cache import RedisCache

from por.conf import llm_agents
from llm_agents.meta.interfaces import LLMAgent


class JungAdvisorInput(BaseModel):
    creative_status: StrictStr
    jung_text_chunks: list[StrictStr]
    output_language: LanguageName


class JungAdvisorOutput(BaseModel):
    jung_advise: StrictStr = Field(
        description="A profound, symbolic, and transformative piece of Jungian advice."
    )


class JungAdvisor(LLMAgent[JungAdvisorInput, JungAdvisorOutput]):
    def __init__(
        self,
        conf_path=f"{llm_agents.__path__[0]}/jung-advisor.yml",
        max_concurrency: int = 10,
        cache: RedisCache = None,
    ):
        super().__init__(
            conf_path=conf_path,
            agent_input=JungAdvisorInput,
            agent_output=JungAdvisorOutput,
            max_concurrency=max_concurrency,
            cache=cache,
        )
