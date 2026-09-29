from pathlib import Path
from typing import Literal

from llm_agents.meta.interfaces import LLMAgent
from pydantic import BaseModel, Field, StrictStr
from pydantic_ai import Agent, RunContext, ToolOutput
from pydantic_ai.models.openai import OpenAIResponsesModelSettings

from por.meta.schema import Material, PsychologicalProfile


class MaterialSelectorDeps(BaseModel):
    output_language: StrictStr
    psychological_profile: PsychologicalProfile
    question: StrictStr
    materials: list[Material]


class MaterialSelectorOutput(BaseModel):
    selected_material_code: Literal[
        "BM.01",
        "GM.02",
        "MC.03",
        "AS.04",
        "MF.05",
    ]
    selection_reason: StrictStr = Field(
        description="A very short standalone reason for the selection.",
        min_length=1,
    )


agent = Agent(
    name="material-selector",
    model="openai:gpt-5.6-terra",
    model_settings=OpenAIResponsesModelSettings(openai_reasoning_effort="low"),
    deps_type=MaterialSelectorDeps,
    output_type=ToolOutput(MaterialSelectorOutput),
    retries=3,
)


@agent.system_prompt
async def get_system_prompt(ctx: RunContext[MaterialSelectorDeps]) -> str:
    system_prompt = LLMAgent.read_file(
        file_path=str(Path(__file__).with_name("system-prompt.md"))
    )

    return system_prompt.format(**ctx.deps.model_dump(mode="json"))


class MaterialSelector(
    LLMAgent[MaterialSelectorDeps, MaterialSelectorOutput]
):
    def __init__(self, max_concurrency: int = 10):
        super().__init__(agent=agent, max_concurrency=max_concurrency)
