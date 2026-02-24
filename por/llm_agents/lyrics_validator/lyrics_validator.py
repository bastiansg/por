from pydantic_ai import ToolOutput
from pydantic import BaseModel, StrictBool, Field
from pydantic_extra_types.language_code import LanguageName

from common.cache import RedisCache
from llm_agents.meta.interfaces import LLMAgent

from por.llm_agents import lyrics_validator


class LyricsValidatorOutput(BaseModel):
    is_valid: StrictBool = Field(
        description="Whether the provided lyrics are an original song lyric version."
    )

    language: LanguageName | None = Field(
        description="Primary language of the provided lyrics, or null if undetermined."
    )


class LyricsValidator(LLMAgent[None, LyricsValidatorOutput]):
    def __init__(
        self,
        conf_path=f"{lyrics_validator.__path__[0]}/lyrics-validator.yml",
        max_concurrency: int = 10,
        cache: RedisCache | None = None,
    ):
        super().__init__(
            conf_path=conf_path,
            output_type=ToolOutput(LyricsValidatorOutput),  # type: ignore
            retries=3,
            max_concurrency=max_concurrency,
            cache=cache,
        )
