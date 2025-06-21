from pydantic import BaseModel, StrictStr, Field
from pydantic_extra_types.language_code import LanguageName

from common.cache import RedisCache

from por.conf import llm_agents
from llm_agents.meta.interfaces import LLMAgent


class CreativeAdvisorInput(BaseModel):
    question: StrictStr
    psychological_profile: StrictStr
    creative_capsule: StrictStr
    output_language: LanguageName


class CreativeAdvisorOutput(BaseModel):
    creative_advice: StrictStr = Field(
        description="A psychologically attuned and creatively inspired piece of advice.",
        min_length=1,
    )


class CreativeAdvisor(LLMAgent[CreativeAdvisorInput, CreativeAdvisorOutput]):
    def __init__(
        self,
        conf_path=f"{llm_agents.__path__[0]}/creative-advisor.yml",
        max_concurrency: int = 10,
        cache: RedisCache = None,
    ):
        super().__init__(
            conf_path=conf_path,
            agent_input=CreativeAdvisorInput,
            agent_output=CreativeAdvisorOutput,
            retries=3,
            max_concurrency=max_concurrency,
            cache=cache,
        )
