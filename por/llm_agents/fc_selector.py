from pydantic import BaseModel, StrictStr, NonNegativeInt

from common.cache import RedisCache

from por.conf import agents
from llm_agents.meta.interfaces import LLMAgent


class FCMessage(BaseModel):
    message_id: NonNegativeInt
    message: StrictStr


class FCSelectorInput(BaseModel):
    person_description: StrictStr
    fc_messages: list[FCMessage]


class FCSelectorOutput(BaseModel):
    message_id: NonNegativeInt


class FCSelector(LLMAgent[FCSelectorInput, FCSelectorOutput]):
    def __init__(
        self,
        conf_path=f"{agents.__path__[0]}/fc-selector.yml",
        max_concurrency: int = 10,
        cache: RedisCache = None,
    ):
        super().__init__(
            conf_path=conf_path,
            agent_input=FCSelectorInput,
            agent_output=FCSelectorOutput,
            max_concurrency=max_concurrency,
            cache=cache,
        )
