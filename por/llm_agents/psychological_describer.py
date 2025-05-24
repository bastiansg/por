from pydantic import BaseModel, StrictStr, Field
from pydantic_extra_types.language_code import LanguageName

from common.cache import RedisCache

from por.conf import llm_agents
from llm_agents.meta.interfaces import LLMAgent


class PsychologicalDescriberInput(BaseModel):
    output_language: LanguageName


class PsychologicalDescriberOutput(BaseModel):
    creative_status: StrictStr = Field(
        description="The individual's or group's relationship with creativity."
    )
    dreams_and_desires: StrictStr = Field(
        description="Speculative ambitions, longings, or life goals inferred from the person's or group's appearance, mood, and styling."
    )
    love_status: StrictStr = Field(
        description="The current emotional or romantic state of the individual or group."
    )


class PsychologicalDescriber(
    LLMAgent[PsychologicalDescriberInput, PsychologicalDescriberOutput]
):
    def __init__(
        self,
        conf_path=f"{llm_agents.__path__[0]}/psychological-describer.yml",
        max_concurrency: int = 10,
        cache: RedisCache = None,
    ):
        super().__init__(
            conf_path=conf_path,
            agent_input=PsychologicalDescriberInput,
            agent_output=PsychologicalDescriberOutput,
            max_concurrency=max_concurrency,
            cache=cache,
        )
