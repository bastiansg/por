from pathlib import Path

from pydantic_ai import Agent, NativeOutput
from pydantic_ai.models.openai import OpenAIChatModelSettings

from llm_agents.meta.interfaces import LLMAgent

from por.meta.schema import AstrologyPlacements


agent = Agent(  # type: ignore
    model="gpt-5.4-2026-03-05",
    model_settings=OpenAIChatModelSettings(openai_reasoning_effort="none"),
    system_prompt=LLMAgent.read_file(
        file_path=str(Path(__file__).with_name("system-prompt.md"))
    ),
    output_type=NativeOutput(AstrologyPlacements),
    retries=3,
)


@agent.system_prompt
async def get_system_prompt() -> str:
    return LLMAgent.read_file(
        file_path=str(Path(__file__).with_name("system-prompt.md"))
    )


class AstrologyPlacementsExtractor(LLMAgent[None, AstrologyPlacements]):
    def __init__(self, max_concurrency: int = 10):
        super().__init__(agent=agent, max_concurrency=max_concurrency)
