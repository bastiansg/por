from pydantic_ai import NativeOutput

from pydantic import BaseModel, StrictStr, Field
from pydantic_extra_types.language_code import LanguageName

from llm_agents.meta.interfaces import LLMAgent

from por.llm_agents import astrology_advisor

from ..astrology_placements_detector.astrology_placements_detector import (
    AstrologyPlacementsDetectorOutput,
)

from ..psychological_describer.psychological_describer import (
    PsychologicalDescriberOutput,
)


class AstrologyAdvisorDeps(BaseModel):
    psychological_profile: PsychologicalDescriberOutput
    question: StrictStr
    astrology_placements: AstrologyPlacementsDetectorOutput
    output_language: LanguageName


class AstrologyAdvisorOutput(BaseModel):
    answer: StrictStr = Field(
        description="A concise, pure astrological advice message.",
        min_length=1,
    )


class AstrologyAdvisor(LLMAgent[AstrologyAdvisorDeps, AstrologyAdvisorOutput]):
    def __init__(
        self,
        conf_path=f"{astrology_advisor.__path__[0]}/astrology-advisor.yml",
        max_concurrency: int = 10,
    ):
        super().__init__(
            conf_path=conf_path,
            deps_type=AstrologyAdvisorDeps,
            output_type=NativeOutput(AstrologyAdvisorOutput),  # type: ignore
            retries=3,
            max_concurrency=max_concurrency,
        )
