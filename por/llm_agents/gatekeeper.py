from pydantic import BaseModel, StrictStr, Field, StrictBool
from pydantic_extra_types.language_code import LanguageName

from common.cache import RedisCache

from por.conf import llm_agents
from llm_agents.meta.interfaces import LLMAgent


class GatekeeperInput(BaseModel):
    message: StrictStr
    output_language: LanguageName


class GatekeeperOutput(BaseModel):
    message_accepted: StrictBool = Field(
        description="Whether the message is accepted to be delivered to the Oracle."
    )
    rejection_reason: StrictStr | None = Field(
        default=None,
        description="A poetic justification for why the message was rejected.",
    )


class Gatekeeper(LLMAgent[GatekeeperInput, GatekeeperOutput]):
    def __init__(
        self,
        conf_path=f"{llm_agents.__path__[0]}/gatekeeper.yml",
        max_concurrency: int = 10,
        cache: RedisCache = None,
    ):
        super().__init__(
            conf_path=conf_path,
            agent_input=GatekeeperInput,
            agent_output=GatekeeperOutput,
            retries=3,
            max_concurrency=max_concurrency,
            cache=cache,
        )
