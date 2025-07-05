from pydantic import BaseModel, StrictStr, Field
from pydantic_extra_types.language_code import LanguageName

from por.conf import llm_agents
from common.cache import RedisCache
from llm_agents.meta.interfaces import LLMAgent


class PsychologicalDescriberDeps(BaseModel):
    physical_description: StrictStr
    clothing_description: StrictStr
    question: StrictStr
    output_language: LanguageName


class PsychologicalDescriberOutput(BaseModel):
    psychological_profile: StrictStr = Field(
        description="A psychological profile based on the provided information.",
        min_length=1,
    )


class PsychologicalDescriber(
    LLMAgent[PsychologicalDescriberDeps, PsychologicalDescriberOutput]
):
    def __init__(
        self,
        conf_path=f"{llm_agents.__path__[0]}/psychological-describer.yml",
        max_concurrency: int = 10,
        cache: RedisCache = None,
    ):
        super().__init__(
            conf_path=conf_path,
            deps_type=PsychologicalDescriberDeps,
            output_type=PsychologicalDescriberOutput,
            retries=3,
            max_concurrency=max_concurrency,
            cache=cache,
        )
