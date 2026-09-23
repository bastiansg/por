from pathlib import Path

from llm_agents.meta.interfaces import LLMAgent
from pydantic import BaseModel, Field, PositiveInt, StrictStr
from pydantic_ai import Agent, RunContext, ToolOutput
from pydantic_ai.models.openai import OpenAIResponsesModelSettings

from por.llm_agents.schema import ImageDescriptionOutput, SceneDescription


class PBFImageDescriberDeps(BaseModel):
    flux_max_tokens: PositiveInt


class PBFSceneDescription(SceneDescription):
    composition: StrictStr = Field(
        description="Framing and viewpoint only.",
        min_length=1,
    )


class PBFImageDescriberOutput(ImageDescriptionOutput[PBFSceneDescription]):
    pass


agent = Agent(
    name="pbf-image-describer",
    model="openai:gpt-5.6-sol",
    model_settings=OpenAIResponsesModelSettings(openai_reasoning_effort="low"),
    deps_type=PBFImageDescriberDeps,
    output_type=ToolOutput(PBFImageDescriberOutput),
    retries=3,
)


@agent.system_prompt
async def get_system_prompt(ctx: RunContext[PBFImageDescriberDeps]) -> str:
    return LLMAgent.read_file(
        file_path=str(Path(__file__).with_name("system-prompt.md"))
    ).format(flux_max_tokens=ctx.deps.flux_max_tokens)


class PBFImageDescriber(
    LLMAgent[PBFImageDescriberDeps, PBFImageDescriberOutput]
):
    def __init__(self, max_concurrency: int = 10):
        super().__init__(agent=agent, max_concurrency=max_concurrency)
