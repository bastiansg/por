from pathlib import Path

from llm_agents.meta.interfaces import LLMAgent
from pydantic import BaseModel, Field, StrictStr
from pydantic_ai import Agent, RunContext, ToolOutput
from pydantic_ai.models.openai import OpenAIChatModelSettings
from pydantic_extra_types.language_code import LanguageName

from por.meta.schema import AstrologyPlacements, PsychologicalProfile, TextChunk

# from por.llm_agents.tools import (
#     astro_weekly_general_tendencies_tool,
#     astro_weekly_horoscope_by_sign_tool,
# )


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
    name="astrology-advisor",
    model="gpt-5.6-terra",
    model_settings=OpenAIChatModelSettings(openai_reasoning_effort="none"),
    system_prompt=LLMAgent.read_file(
        file_path=str(Path(__file__).with_name("system-prompt.md"))
    ),
    deps_type=AstrologyAdvisorDeps,
    output_type=ToolOutput(AstrologyAdvisorOutput),
    # tools=[
    #     astro_weekly_general_tendencies_tool,
    #     astro_weekly_horoscope_by_sign_tool,
    # ],
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
