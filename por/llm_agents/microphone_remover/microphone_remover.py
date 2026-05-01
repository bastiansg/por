from pathlib import Path

from pydantic_ai import Agent, RunContext, NativeOutput
from pydantic_ai.models.openai import OpenAIChatModelSettings

from llm_agents.meta.interfaces import LLMAgent

from ..image_describer.image_describer import ImageDescriberOutput


class MicrophoneRemoverDeps(ImageDescriberOutput):
    pass


class MicrophoneRemoverOutput(ImageDescriberOutput):
    pass


agent = Agent(  # type: ignore
    name="microphone-remover",
    model="gpt-5.4-mini-2026-03-17",
    model_settings=OpenAIChatModelSettings(openai_reasoning_effort="none"),
    system_prompt=LLMAgent.read_file(
        file_path=str(Path(__file__).with_name("system-prompt.md"))
    ),
    deps_type=MicrophoneRemoverDeps,
    output_type=NativeOutput(MicrophoneRemoverOutput),
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
