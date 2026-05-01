from pathlib import Path

from pydantic_ai import Agent, NativeOutput
from pydantic_ai.models.openai import OpenAIChatModelSettings
from pydantic import BaseModel, StrictBool, Field
from pydantic_extra_types.language_code import LanguageName

from llm_agents.meta.interfaces import LLMAgent


class LyricsValidatorOutput(BaseModel):
    is_valid: StrictBool = Field(
        description="Whether the provided lyrics are an original song lyric version."
    )

    language: LanguageName | None = Field(
        description="Primary language of the provided lyrics, or null if undetermined."
    )


agent = Agent(  # type: ignore
    model="gpt-5.4-2026-03-05",
    model_settings=OpenAIChatModelSettings(openai_reasoning_effort="none"),
    system_prompt=LLMAgent.read_file(
        file_path=str(Path(__file__).with_name("system-prompt.md"))
    ),
    output_type=NativeOutput(LyricsValidatorOutput),
    retries=3,
)


class LyricsValidator(LLMAgent[None, LyricsValidatorOutput]):
    def __init__(self, max_concurrency: int = 10):
        super().__init__(agent=agent, max_concurrency=max_concurrency)
