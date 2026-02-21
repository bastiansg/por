from pydantic_ai import ToolOutput
from pydantic import BaseModel, StrictStr, Field, StrictBool
from pydantic_extra_types.language_code import LanguageName

from llm_agents.meta.interfaces import LLMAgent

from por.llm_agents import gatekeeper


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


class Gatekeeper(LLMAgent[GatekeeperDeps, GatekeeperOutput]):
    def __init__(
        self,
        conf_path=f"{gatekeeper.__path__[0]}/gatekeeper.yml",
        max_concurrency: int = 10,
    ):
        super().__init__(
            conf_path=conf_path,
            deps_type=GatekeeperDeps,
            output_type=ToolOutput(GatekeeperOutput),  # type: ignore
            retries=3,
            max_concurrency=max_concurrency,
        )
