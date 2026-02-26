from typing import Literal
from pydantic_ai import ToolOutput

from pydantic import BaseModel, Field, StrictStr
from pydantic_extra_types.language_code import LanguageName

from llm_agents.meta.interfaces import LLMAgent

from por.meta.schema import Material
from por.llm_agents import material_selector

from ..psychological_describer.psychological_describer import (
    PsychologicalDescriberOutput,
)


class MaterialSelectorDeps(BaseModel):
    psychological_profile: PsychologicalDescriberOutput
    question: StrictStr
    materials: list[Material]
    output_language: LanguageName


class MaterialSelectorOutput(BaseModel):
    selected_material_code: Literal[
        "BM.01",
        "GM.02",
        "MC.03",
        "AS.04",
        "MF.05",
    ] = Field(
        description="The `code` of the selected material.",
        min_length=1,
    )

    selection_justification: StrictStr = Field(
        description="Very short justification explaining why the selected material fits the user and question.",
        min_length=1,
    )


class MaterialSelector(LLMAgent[MaterialSelectorDeps, MaterialSelectorOutput]):
    def __init__(
        self,
        conf_path=f"{material_selector.__path__[0]}/material-selector.yml",
        max_concurrency: int = 10,
    ):
        super().__init__(
            conf_path=conf_path,
            deps_type=MaterialSelectorDeps,
            output_type=ToolOutput(MaterialSelectorOutput),  # type: ignore
            retries=3,
            max_concurrency=max_concurrency,
        )
