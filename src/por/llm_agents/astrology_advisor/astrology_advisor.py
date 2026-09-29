from pathlib import Path

from llm_agents.meta.interfaces import LLMAgent
from pydantic import BaseModel, Field, StrictStr
from pydantic_ai import Agent, RunContext, ToolOutput
from pydantic_ai.models.openai import OpenAIResponsesModelSettings

class AstrologyAdvisorDeps(BaseModel):
    output_language: StrictStr


class AstrologyAdvisorOutput(BaseModel):
    answer: StrictStr = Field(
        description="Your intuitive, symbolic, and emotionally clarifying message.",
        min_length=1,
    )


agent = Agent(  # type: ignore
    name="astrology-advisor",
    model="openai:gpt-5.6-terra",
    model_settings=OpenAIResponsesModelSettings(openai_reasoning_effort="low"),
    deps_type=AstrologyAdvisorDeps,
    output_type=ToolOutput(AstrologyAdvisorOutput),
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
