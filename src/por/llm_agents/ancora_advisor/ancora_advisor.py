from pathlib import Path

from pydantic import BaseModel, StrictStr, Field
from pydantic_ai import Agent, RunContext, NativeOutput
from pydantic_ai.models.openai import OpenAIChatModelSettings
from pydantic_extra_types.language_code import LanguageName

from llm_agents.meta.interfaces import LLMAgent

from por.meta.schema import TextChunk, PsychologicalProfile


class AncoraAdvisorDeps(BaseModel):
    psychological_profile: PsychologicalProfile
    text_chunks: list[TextChunk]
    output_language: LanguageName


class AncoraAdvisorOutput(BaseModel):
    answer: StrictStr = Field(
        description="Your hammer-like political and critical answer.",
        min_length=1,
    )

    relevant_chunk_ids: list[StrictStr] = Field(
        description="List of unique `chunk_id` values that influenced your answer.",
        min_length=1,
    )


agent = Agent(  # type: ignore
    name="ancora-advisor",
    model="gpt-5.4-2026-03-05",
    model_settings=OpenAIChatModelSettings(openai_reasoning_effort="none"),
    system_prompt=LLMAgent.read_file(
        file_path=str(Path(__file__).with_name("system-prompt.md"))
    ),
    deps_type=AncoraAdvisorDeps,
    output_type=NativeOutput(AncoraAdvisorOutput),
    retries=3,
)


@agent.system_prompt
async def get_system_prompt(ctx: RunContext[AncoraAdvisorDeps]) -> str:
    system_prompt = LLMAgent.read_file(
        file_path=str(Path(__file__).with_name("system-prompt.md"))
    )

    return system_prompt.format(**ctx.deps.model_dump())


class AncoraAdvisor(LLMAgent[AncoraAdvisorDeps, AncoraAdvisorOutput]):
    def __init__(self, max_concurrency: int = 10):
        super().__init__(agent=agent, max_concurrency=max_concurrency)
