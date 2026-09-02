from pathlib import Path

from llm_agents.meta.interfaces import LLMAgent
from pydantic import BaseModel
from pydantic_ai import Agent, RunContext, ToolOutput
from pydantic_ai.models.openai import OpenAIChatModelSettings

from por.llm_agents.pbf_image_describer.pbf_image_describer import (
    PBFImageDescriberOutput,
)


class MicrophoneRemoverDeps(BaseModel):
    image_description: PBFImageDescriberOutput


class MicrophoneRemoverOutput(PBFImageDescriberOutput):
    pass


agent = Agent(  # type: ignore
    name="microphone-remover",
    model="openai-chat:gpt-5.6-luna",
    model_settings=OpenAIChatModelSettings(openai_reasoning_effort="none"),
    system_prompt=LLMAgent.read_file(
        file_path=str(Path(__file__).with_name("system-prompt.md"))
    ),
    deps_type=MicrophoneRemoverDeps,
    output_type=ToolOutput(MicrophoneRemoverOutput),
    retries=3,
)


@agent.system_prompt
async def get_system_prompt(ctx: RunContext[MicrophoneRemoverDeps]) -> str:
    system_prompt = LLMAgent.read_file(
        file_path=str(Path(__file__).with_name("system-prompt.md"))
    )

    return system_prompt.format(**ctx.deps.model_dump())


class MicrophoneRemover(
    LLMAgent[MicrophoneRemoverDeps, MicrophoneRemoverOutput]
):
    def __init__(self, max_concurrency: int = 10):
        super().__init__(agent=agent, max_concurrency=max_concurrency)
