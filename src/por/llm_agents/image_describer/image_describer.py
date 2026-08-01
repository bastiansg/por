from pathlib import Path

from llm_agents.meta.interfaces import LLMAgent
from pydantic import BaseModel, Field
from pydantic_ai import Agent, ToolOutput
from pydantic_ai.models.openai import OpenAIChatModelSettings

from por.meta.schema import ClothingDescription, PhysicalDescription


class ImageDescriberOutput(BaseModel):
    physical_description: PhysicalDescription = Field(
        description="Physical description of the people in the provided image.",
    )

    clothing_description: ClothingDescription = Field(
        description="Clothing and accessory description of the people in the provided image.",
    )


agent = Agent(  # type: ignore
    name="image-describer",
    model="gpt-5.6-luna",
    model_settings=OpenAIChatModelSettings(openai_reasoning_effort="none"),
    system_prompt=LLMAgent.read_file(
        file_path=str(Path(__file__).with_name("system-prompt.md"))
    ),
    output_type=ToolOutput(ImageDescriberOutput),
    retries=3,
)


@agent.system_prompt
async def get_system_prompt() -> str:
    return LLMAgent.read_file(
        file_path=str(Path(__file__).with_name("system-prompt.md"))
    )


class ImageDescriber(LLMAgent[None, ImageDescriberOutput]):
    def __init__(self, max_concurrency: int = 10):
        super().__init__(agent=agent, max_concurrency=max_concurrency)
