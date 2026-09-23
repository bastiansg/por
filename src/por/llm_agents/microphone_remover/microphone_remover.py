from pathlib import Path

from llm_agents.meta.interfaces import LLMAgent
from pydantic_ai import Agent, ToolOutput
from pydantic_ai.models.openai import OpenAIResponsesModelSettings

from por.llm_agents.pbf_image_describer.pbf_image_describer import (
    PBFImageDescriberOutput,
)


class MicrophoneRemoverOutput(PBFImageDescriberOutput):
    pass


agent = Agent(
    name="microphone-remover",
    model="openai:gpt-5.6-luna",
    model_settings=OpenAIResponsesModelSettings(openai_reasoning_effort="low"),
    output_type=ToolOutput(MicrophoneRemoverOutput),
    retries=3,
)


@agent.system_prompt
async def get_system_prompt() -> str:
    return LLMAgent.read_file(
        file_path=str(Path(__file__).with_name("system-prompt.md"))
    )


class MicrophoneRemover(LLMAgent[None, MicrophoneRemoverOutput]):
    def __init__(self, max_concurrency: int = 10):
        super().__init__(agent=agent, max_concurrency=max_concurrency)
