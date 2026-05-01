from pathlib import Path

from pydantic_ai import Agent, RunContext, NativeOutput
from pydantic_ai.models.openai import OpenAIChatModelSettings

from pydantic import BaseModel, StrictStr, Field
from pydantic_extra_types.language_code import LanguageName

from llm_agents.meta.interfaces import LLMAgent
from por.meta.schema import TextChunk, AstrologyPlacements, PsychologicalProfile


class AstrologyAdvisorDeps(BaseModel):
    astrology_placements: AstrologyPlacements
    psychological_profile: PsychologicalProfile
    text_chunks: list[TextChunk]
    output_language: LanguageName


class AstrologyAdvisorOutput(BaseModel):
    answer: StrictStr = Field(
        description="Your intuitive, symbolic, and emotionally clarifying message.",
        min_length=1,
    )

    relevant_chunk_ids: list[StrictStr] = Field(
        description="List of unique `chunk_id` values that influenced your answer.",
        min_length=1,
    )


agent = Agent(  # type: ignore
    # model="gpt-5.4-2026-03-05",
    model="gpt-5.4-2026-03-05",
    model_settings=OpenAIChatModelSettings(openai_reasoning_effort="none"),
    system_prompt=LLMAgent.read_file(
        file_path=str(Path(__file__).with_name("system-prompt.md"))
    ),
    deps_type=AstrologyAdvisorDeps,
    output_type=NativeOutput(AstrologyAdvisorOutput),
    retries=3,
)


@agent.system_prompt
async def get_system_prompt(ctx: RunContext[AstrologyAdvisorDeps]) -> str:
    system_prompt = LLMAgent.read_file(
        file_path=str(Path(__file__).with_name("system-prompt.md"))
    )

    return system_prompt.format(**ctx.deps.model_dump())


class AstrologyAdvisor(LLMAgent[AstrologyAdvisorDeps, AstrologyAdvisorOutput]):
    def __init__(self, max_concurrency: int = 10):
        super().__init__(agent=agent, max_concurrency=max_concurrency)
