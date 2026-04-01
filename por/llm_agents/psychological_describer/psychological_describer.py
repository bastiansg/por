from typing import Literal

from pydantic_ai import NativeOutput
from pydantic import BaseModel, StrictStr, Field

from pydantic_extra_types.language_code import LanguageName

from llm_agents.meta.interfaces import LLMAgent

from por.llm_agents import psychological_describer


class PsychologicalDescriberDeps(BaseModel):
    question: StrictStr
    output_language: LanguageName


class PsychologicalDescriberOutput(BaseModel):
    posture: Literal[
        "open",
        "closed",
        "tense",
        "relaxed",
        "collapsed",
        "expansive",
    ] = Field(description="Body alignment and engagement level.")

    facial_expression: Literal[
        "neutral",
        "smile",
        "serious",
        "pensive",
        "flat",
        "tense",
    ] = Field(description="Expression category.")

    gaze: Literal[
        "steady",
        "intense",
        "defocused",
        "soft",
        "guarded",
        "alert",
        "vacant",
        "searching",
        "hesitant",
        "piercing",
        "warm",
    ] = Field(description="Gaze quality only, excluding direction.")

    emotional_tone: Literal[
        "hopeful",
        "anxious",
        "conflicted",
        "determined",
        "melancholic",
        "resigned",
        "yearning",
        "defiant",
        "curious",
        "numb",
    ] = Field(description="Dominant felt emotional state.")

    composure: Literal[
        "settled",
        "guarded",
        "fragile",
        "controlled",
        "restless",
        "overwhelmed",
        "dissociated",
    ] = Field(description="Emotional self-regulation capacity in this moment.")

    question_theme: Literal[
        "direction",
        "conflict",
        "desire",
        "identity",
        "fear",
        "purpose",
        "change",
        "belonging",
        "loss",
        "worthiness",
        "trust",
        "timing",
    ] = Field(description="Core existential concern behind the question.")


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
            output_type=NativeOutput(PsychologicalDescriberOutput),  # type: ignore
            retries=3,
            max_concurrency=max_concurrency,
        )
