from pydantic_ai import NativeOutput
from pydantic import BaseModel, Field, StrictBool
from pydantic_extra_types.language_code import LanguageName

from llm_agents.meta.interfaces import LLMAgent

from por.llm_agents import exibition_related


class ExibitionRelatedDeps(BaseModel):
    output_language: LanguageName


class ExibitionRelatedOutput(BaseModel):
    exibition_related: StrictBool = Field(
        description="Whether the message is related to the current exhibition context."
    )


class ExibitionRelated(LLMAgent[ExibitionRelatedDeps, ExibitionRelatedOutput]):
    def __init__(
        self,
        conf_path=f"{exibition_related.__path__[0]}/exibition-related.yml",
        max_concurrency: int = 10,
    ):
        super().__init__(
            conf_path=conf_path,
            deps_type=ExibitionRelatedDeps,
            output_type=NativeOutput(ExibitionRelatedOutput),  # type: ignore
            retries=3,
            max_concurrency=max_concurrency,
        )
