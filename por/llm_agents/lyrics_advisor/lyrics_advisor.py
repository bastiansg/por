from pydantic_ai import ToolOutput

from pydantic import BaseModel, StrictStr, Field
from pydantic_extra_types.language_code import LanguageName

from llm_agents.meta.interfaces import LLMAgent

from por.llm_agents import lyrics_advisor
from por.meta.schema import TextChunk, Song

from ..psychological_describer.psychological_describer import (
    PsychologicalDescriberOutput,
)


class LyricsAdvisorDeps(BaseModel):
    psychological_profile: PsychologicalDescriberOutput
    question: StrictStr
    text_chunks: list[TextChunk]
    output_language: LanguageName


class LyricsAdvisorOutput(BaseModel):
    song: Song = Field(
        description="Recommended song object with title, artist, and year.",
    )

    reason: StrictStr = Field(
        description="A very short, sharp, funny, sarcastic, slightly bully-ish reason.",
        min_length=1,
    )


class LyricsAdvisor(LLMAgent[LyricsAdvisorDeps, LyricsAdvisorOutput]):
    def __init__(
        self,
        conf_path=f"{lyrics_advisor.__path__[0]}/lyrics-advisor.yml",
        max_concurrency: int = 10,
    ):
        super().__init__(
            conf_path=conf_path,
            deps_type=LyricsAdvisorDeps,
            output_type=ToolOutput(LyricsAdvisorOutput),  # type: ignore
            retries=3,
            max_concurrency=max_concurrency,
        )
