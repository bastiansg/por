from pathlib import Path

from llm_agents.meta.interfaces import LLMAgent
from pydantic import BaseModel, Field, StrictStr
from pydantic_ai import Agent, ToolOutput
from pydantic_ai.models.openai import OpenAIResponsesModelSettings


class ImagePrompterOutput(BaseModel):
    flux_prompt: StrictStr = Field(
        description="The surreal image-generation prompt.",
        min_length=1,
    )


agent = Agent(
    name="image-prompter",
    model="openai:gpt-5.6-sol",
    model_settings=OpenAIResponsesModelSettings(openai_reasoning_effort="low"),
    output_type=ToolOutput(ImagePrompterOutput),
    retries=3,
)


@agent.system_prompt
async def get_system_prompt() -> str:
    return LLMAgent.read_file(
        file_path=str(Path(__file__).with_name("system-prompt.md"))
    )


class ImagePrompter(LLMAgent[None, ImagePrompterOutput]):
    def __init__(self, max_concurrency: int = 10):
        super().__init__(agent=agent, max_concurrency=max_concurrency)
