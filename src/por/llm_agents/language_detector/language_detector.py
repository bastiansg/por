from pathlib import Path

from llm_agents.meta.interfaces import LLMAgent
from pydantic import BaseModel, Field
from pydantic_ai import Agent, ToolOutput
from pydantic_ai.models.openai import OpenAIChatModelSettings
from pydantic_extra_types.language_code import LanguageAlpha2


class LanguageDetectorOutput(BaseModel):
    language: LanguageAlpha2 | None = Field(
        description="The primary language of the given user query."
    )


agent = Agent(  # type: ignore
    name="language-detector",
    model="openai-chat:gpt-5.6-luna",
    model_settings=OpenAIChatModelSettings(openai_reasoning_effort="none"),
    system_prompt=LLMAgent.read_file(
        file_path=str(Path(__file__).with_name("system-prompt.md"))
    ),
    output_type=ToolOutput(LanguageDetectorOutput),
    retries=3,
)


@agent.system_prompt
async def get_system_prompt() -> str:
    return LLMAgent.read_file(
        file_path=str(Path(__file__).with_name("system-prompt.md"))
    )


class LanguageDetector(LLMAgent[None, LanguageDetectorOutput]):
    def __init__(self, max_concurrency: int = 10):
        super().__init__(agent=agent, max_concurrency=max_concurrency)
