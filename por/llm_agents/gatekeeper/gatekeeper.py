from pathlib import Path

from pydantic_ai import Agent, NativeOutput
from pydantic_ai.models.openai import OpenAIChatModelSettings
from pydantic import BaseModel, StrictStr, Field, StrictBool
from pydantic_extra_types.language_code import LanguageName

from llm_agents.meta.interfaces import LLMAgent


class GatekeeperDeps(BaseModel):
    output_language: LanguageName


class GatekeeperOutput(BaseModel):
    message_accepted: StrictBool = Field(
        description="Whether the message is accepted to be delivered to the Oracle."
    )

    rejection_reason: StrictStr | None = Field(
        default=None,
        description="A justification for why the message was rejected.",
    )


agent = Agent(  # type: ignore
    model="gpt-5.4-mini-2026-03-17",
    model_settings=OpenAIChatModelSettings(openai_reasoning_effort="none"),
    system_prompt=LLMAgent.read_file(
        file_path=str(Path(__file__).with_name("system-prompt.md"))
    ),
    deps_type=GatekeeperDeps,
    output_type=NativeOutput(GatekeeperOutput),
    retries=3,
)


class Gatekeeper(LLMAgent[GatekeeperDeps, GatekeeperOutput]):
    def __init__(self, max_concurrency: int = 10):
        super().__init__(agent=agent, max_concurrency=max_concurrency)
