from pathlib import Path

from llm_agents.meta.interfaces import LLMAgent
from pydantic import BaseModel, Field, StrictBool
from pydantic_ai import Agent, ToolOutput
from pydantic_extra_types.language_code import LanguageName


class LyricsValidatorOutput(BaseModel):
    is_valid: StrictBool = Field(
        description="Whether the provided lyrics are an original song lyric version."
    )

    language: LanguageName | None = Field(
        description="Primary language of the provided lyrics, or null if undetermined."
    )


agent = Agent(  # type: ignore
    name="lyrics-validator",
    model="gpt-5.6-terra",
    system_prompt=LLMAgent.read_file(
        file_path=str(Path(__file__).with_name("system-prompt.md"))
    ),
    output_type=ToolOutput(LyricsValidatorOutput),
    retries=3,
)


@agent.system_prompt
async def get_system_prompt() -> str:
    return LLMAgent.read_file(
        file_path=str(Path(__file__).with_name("system-prompt.md"))
    )


class LyricsValidator(LLMAgent[None, LyricsValidatorOutput]):
    def __init__(self, max_concurrency: int = 10):
        super().__init__(agent=agent, max_concurrency=max_concurrency)
