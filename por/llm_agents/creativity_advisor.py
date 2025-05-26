from pydantic import BaseModel, StrictStr, Field
from pydantic_extra_types.language_code import LanguageName

from common.cache import RedisCache

from por.conf import llm_agents
from llm_agents.meta.interfaces import LLMAgent


class CreativityAdvisorInput(BaseModel):
    creative_status: StrictStr
    creativity_text_chunks: list[StrictStr]
    output_language: LanguageName


class CreativityAdvisorOutput(BaseModel):
    creativity_advice: StrictStr = Field(
        description="Symbolic and transformative creative guidance.",
        min_length=1,
    )


class CreativityAdvisor(
    LLMAgent[CreativityAdvisorInput, CreativityAdvisorOutput]
):
    def __init__(
        self,
        conf_path=f"{llm_agents.__path__[0]}/creativity-advisor.yml",
        max_concurrency: int = 10,
        cache: RedisCache = None,
    ):
        super().__init__(
            conf_path=conf_path,
            agent_input=CreativityAdvisorInput,
            agent_output=CreativityAdvisorOutput,
            retries=3,
            max_concurrency=max_concurrency,
            cache=cache,
        )
