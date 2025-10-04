from pydantic_ai import ToolOutput
from pydantic import BaseModel, StrictStr, Field

from pydantic_extra_types.language_code import LanguageName

from por.conf import llm_agents  # type: ignore
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
    ):
        super().__init__(
            conf_path=conf_path,
            deps_type=PsychologicalDescriberDeps,
            output_type=ToolOutput(PsychologicalDescriberOutput),  # type: ignore
            retries=3,
            max_concurrency=max_concurrency,
        )
