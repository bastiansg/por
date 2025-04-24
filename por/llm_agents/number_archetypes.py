from pydantic import BaseModel, StrictStr, NonNegativeInt, Field

from common.cache import RedisCache

from por.conf import agents
from llm_agents.meta.interfaces import LLMAgent


class NumberArchetypesInput(BaseModel):
    person_description: StrictStr
    number_archetypes: StrictStr


class NumberArchetypesOutput(BaseModel):
    number: NonNegativeInt = Field(
        description="Symbolic number reflecting the person's psychological profile."
    )


class NumberArchetypes(LLMAgent[NumberArchetypesInput, NumberArchetypesOutput]):
    def __init__(
        self,
        conf_path=f"{agents.__path__[0]}/number-archetypes.yml",
        max_concurrency: int = 10,
        cache: RedisCache = None,
    ):
        super().__init__(
            conf_path=conf_path,
            agent_input=NumberArchetypesInput,
            agent_output=NumberArchetypesOutput,
            max_concurrency=max_concurrency,
            cache=cache,
        )
