from pathlib import Path

from llm_agents.meta.interfaces import LLMAgent
from pydantic import Field, StrictStr
from pydantic_ai import Agent, ToolOutput
from pydantic_ai.models.openai import OpenAIChatModelSettings

from por.llm_agents.schema import ImageDescriptionOutput, SceneDescription


class PBFSceneDescription(SceneDescription):
    composition: StrictStr = Field(
        description="Framing and viewpoint only.",
        min_length=1,
    )


class PBFImageDescriberOutput(ImageDescriptionOutput[PBFSceneDescription]):
    pass

agent = Agent(
    name="pbf-image-describer",
    model="gpt-5.6-sol",
    model_settings=OpenAIChatModelSettings(
        max_tokens=512,
        openai_reasoning_effort="none",
    ),
    system_prompt=LLMAgent.read_file(
        file_path=str(Path(__file__).with_name("system-prompt.md"))
    ),
    output_type=ToolOutput(PBFImageDescriberOutput),
    retries=3,
)


@agent.system_prompt
async def get_system_prompt() -> str:
    return LLMAgent.read_file(
        file_path=str(Path(__file__).with_name("system-prompt.md"))
    )


class PBFImageDescriber(LLMAgent[None, PBFImageDescriberOutput]):
    def __init__(self, max_concurrency: int = 10):
        super().__init__(agent=agent, max_concurrency=max_concurrency)
