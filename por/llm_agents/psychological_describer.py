from pydantic_ai import ToolOutput
from pydantic import BaseModel, StrictStr, Field

from pydantic_extra_types.language_code import LanguageName

from por.conf import llm_agents  # type: ignore
from llm_agents.meta.interfaces import LLMAgent


# from .image_describer import PhysicalDescription, ClothingDescription


class PsychologicalDescriberDeps(BaseModel):
    # physical_description: PhysicalDescription
    # clothing_description: ClothingDescription
    question: StrictStr
    output_language: LanguageName


class PsychologicalDescriberOutput(BaseModel):
    posture: StrictStr = Field(
        description="Visible body stance (e.g., upright, slouched, tense), excluding gestures involving a hand near the mouth.",
        min_length=1,
    )

    emotional_tone: StrictStr = Field(
        description="Symbolic mood suggested by appearance (e.g., contemplative, determined, reserved).",
        min_length=1,
    )

    composure: StrictStr = Field(
        description="Visible level of physical tension or ease (e.g., composed, tense, relaxed).",
        min_length=1,
    )

    facial_expression: StrictStr = Field(
        description="Basic expression category (e.g., neutral, smiling, serious).",
        min_length=1,
    )

    gaze: StrictStr = Field(
        description="Direction/quality of gaze (e.g., direct, downward, distant).",
        min_length=1,
    )

    archetype_hint: StrictStr = Field(
        description="Symbolic impression suggested by appearance (e.g., seeker, warrior, sage).",
        min_length=1,
    )

    question_theme: StrictStr = Field(
        description="Core theme extracted from the question (e.g., direction, conflict, desire).",
        min_length=1,
    )

    synthesis: StrictStr = Field(
        description="A one-sentence integration of appearance + question theme.",
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
