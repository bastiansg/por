from pathlib import Path

from pydantic import BaseModel, StrictStr, Field
from pydantic_ai import Agent, RunContext, NativeOutput
from pydantic_ai.models.openai import OpenAIChatModelSettings

from llm_agents.meta.interfaces import LLMAgent

from por.meta.schema import TextChunk


class PRAdvisorDeps(BaseModel):
    text_chunks: list[TextChunk]


class PRAdvisorOutput(BaseModel):
    phrase: StrictStr = Field(
        description=(
            "One short verbatim sentence or phrase copied exactly from the "
            "Indio Solari lyrics text chunks."
        ),
        min_length=1,
    )

    relevant_chunk_ids: list[StrictStr] = Field(
        description=(
            "List of unique `chunk_id` values that contain or justify the "
            "selected phrase."
        ),
        min_length=1,
    )


agent = Agent(  # type: ignore
    name="pr-advisor",
    model="gpt-5.4-2026-03-05",
    model_settings=OpenAIChatModelSettings(openai_reasoning_effort="none"),
    system_prompt=LLMAgent.read_file(
        file_path=str(Path(__file__).with_name("system-prompt.md"))
    ),
    deps_type=PRAdvisorDeps,
    output_type=NativeOutput(PRAdvisorOutput),
    retries=3,
)


@agent.system_prompt
async def get_system_prompt(ctx: RunContext[PRAdvisorDeps]) -> str:
    system_prompt = LLMAgent.read_file(
        file_path=str(Path(__file__).with_name("system-prompt.md"))
    )

    return system_prompt.format(**ctx.deps.model_dump())


class PRAdvisor(LLMAgent[PRAdvisorDeps, PRAdvisorOutput]):
    def __init__(self, max_concurrency: int = 10):
        super().__init__(agent=agent, max_concurrency=max_concurrency)
