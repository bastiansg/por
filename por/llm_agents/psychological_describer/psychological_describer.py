from pydantic_ai import NativeOutput
from pydantic import BaseModel, StrictStr
from pydantic_extra_types.language_code import LanguageName

from llm_agents.meta.interfaces import LLMAgent

from por.llm_agents import psychological_describer
from por.meta.schema import PsychologicalProfile


class PsychologicalDescriberDeps(BaseModel):
    question: StrictStr
    output_language: LanguageName


class PsychologicalDescriber(
    LLMAgent[PsychologicalDescriberDeps, PsychologicalProfile]
):
    def __init__(
        self,
        conf_path=f"{psychological_describer.__path__[0]}/psychological-describer.yml",
        max_concurrency: int = 10,
    ):
        super().__init__(
            conf_path=conf_path,
            deps_type=PsychologicalDescriberDeps,
            output_type=NativeOutput(PsychologicalProfile),  # type: ignore
            retries=3,
            max_concurrency=max_concurrency,
        )
