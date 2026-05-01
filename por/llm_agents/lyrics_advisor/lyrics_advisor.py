from pathlib import Path

from pydantic_ai import Agent, RunContext, NativeOutput
from pydantic_ai.models.openai import OpenAIChatModelSettings

from pydantic import BaseModel, StrictStr, Field
from pydantic_extra_types.language_code import LanguageName

from llm_agents.meta.interfaces import LLMAgent

from por.meta.schema import TextChunk, Song, PsychologicalProfile


class LyricsAdvisorDeps(BaseModel):
    psychological_profile: PsychologicalProfile
    text_chunks: list[TextChunk]
    output_language: LanguageName


class LyricsAdvisorOutput(BaseModel):
    song: Song = Field(
        description="Recommended song object with title, artist, and year.",
    )

    reason: StrictStr = Field(
        description="A very short, ironic and lightly teasing reason, without adjectives for the user.",
        min_length=1,
    )


agent = Agent(  # type: ignore
    model="gpt-5.4-2026-03-05",
    model_settings=OpenAIChatModelSettings(openai_reasoning_effort="none"),
    system_prompt=LLMAgent.read_file(
        file_path=str(Path(__file__).with_name("system-prompt.md"))
    ),
    deps_type=LyricsAdvisorDeps,
    output_type=NativeOutput(LyricsAdvisorOutput),
    retries=3,
)


@agent.system_prompt
async def get_system_prompt(ctx: RunContext[LyricsAdvisorDeps]) -> str:
    system_prompt = LLMAgent.read_file(
        file_path=str(Path(__file__).with_name("system-prompt.md"))
    )

    return system_prompt.format(**ctx.deps.model_dump())


class LyricsAdvisor(LLMAgent[LyricsAdvisorDeps, LyricsAdvisorOutput]):
    def __init__(self, max_concurrency: int = 10):
        super().__init__(agent=agent, max_concurrency=max_concurrency)
