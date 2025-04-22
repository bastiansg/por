from pydantic import BaseModel, StrictStr, NonNegativeInt, Field

from common.cache import RedisCache

from por.conf import agents
from llm_agents.meta.interfaces import LLMAgent


class DCPoem(BaseModel):
    poem_id: NonNegativeInt
    poem: StrictStr


class DCSelectorInput(BaseModel):
    person_description: StrictStr
    dc_poems: list[DCPoem]


class DCSelectorOutput(BaseModel):
    poem_id: NonNegativeInt = Field(
        description="The selected poem_id that best aligns with the person's current romantic or emotional state."
    )


class DCSelector(LLMAgent[DCSelectorInput, DCSelectorOutput]):
    def __init__(
        self,
        conf_path=f"{agents.__path__[0]}/dc-selector.yml",
        max_concurrency: int = 10,
        cache: RedisCache = None,
    ):
        super().__init__(
            conf_path=conf_path,
            agent_input=DCSelectorInput,
            agent_output=DCSelectorOutput,
            max_concurrency=max_concurrency,
            cache=cache,
        )
