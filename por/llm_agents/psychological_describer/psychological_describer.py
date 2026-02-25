from typing import Literal

from pydantic_ai import ToolOutput
from pydantic import BaseModel, StrictStr, Field

from pydantic_extra_types.language_code import LanguageName

from llm_agents.meta.interfaces import LLMAgent

from por.llm_agents import psychological_describer


class PsychologicalDescriberDeps(BaseModel):
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
        description="Gaze direction or quality only (e.g., direct, downward, distant); never include the gaze target.",
        min_length=1,
    )

    major_arcana_archetype: Literal[
        "The Fool",
        "The Magician",
        "The High Priestess",
        "The Empress",
        "The Emperor",
        "The Hierophant",
        "The Lovers",
        "The Chariot",
        "Strength",
        "The Hermit",
        "Wheel of Fortune",
        "Justice",
        "The Hanged Man",
        "Death",
        "Temperance",
        "The Devil",
        "The Tower",
        "The Star",
        "The Moon",
        "The Sun",
        "Judgement",
        "The World",
    ] = Field(
        description="Archetypal essence aligned with one of the 22 Major Arcana of Tarot.",
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
        conf_path=f"{psychological_describer.__path__[0]}/psychological-describer.yml",
        max_concurrency: int = 10,
    ):
        super().__init__(
            conf_path=conf_path,
            deps_type=PsychologicalDescriberDeps,
            output_type=ToolOutput(PsychologicalDescriberOutput),  # type: ignore
            retries=3,
            max_concurrency=max_concurrency,
        )
