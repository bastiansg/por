from pydantic_ai import NativeOutput
from pydantic_ai.models import Model
from pydantic import BaseModel, Field
from pydantic_extra_types.language_code import LanguageAlpha2

from common.cache import RedisCache
from llm_agents.meta.interfaces import LLMAgent

from por.llm_agents import language_detector


class LanguageDetectorOutput(BaseModel):
    language: LanguageAlpha2 | None = Field(
        description="The primary language of the given user query."
    )


class LanguageDetector(LLMAgent[None, LanguageDetectorOutput]):
    def __init__(
        self,
        conf_path: str = f"{language_detector.__path__[0]}/language-detector.yml",
        model: Model | None = None,
        max_concurrency: int = 10,
        cache: RedisCache | None = None,
        retries: int = 3,
    ):
        super().__init__(
            conf_path=conf_path,
            output_type=NativeOutput(LanguageDetectorOutput),  # type: ignore
            model=model,
            max_concurrency=max_concurrency,
            cache=cache,
            retries=retries,
        )
