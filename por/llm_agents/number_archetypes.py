from typing import Literal
from pydantic import BaseModel, StrictStr, Field

from common.cache import RedisCache

from por.conf import llm_agents
from llm_agents.meta.interfaces import LLMAgent


class NumberArchetypesInput(BaseModel):
    number_archetypes: StrictStr
    psychological_description: StrictStr


class NumberArchetypesOutput(BaseModel):
    archetype_name: Literal[
        "The Leader",
        "The Peacemaker",
        "The Creative",
        "The Builder",
        "The Adventurer",
        "The Caregiver",
        "The Seeker",
        "The Powerhouse",
        "The Humanitarian",
        "The Visionary",
        "The Master Builder",
        "The Master Teacher",
    ] = Field(
        description="The name of the numerological archetype.",
    )


class NumberArchetypes(LLMAgent[NumberArchetypesInput, NumberArchetypesOutput]):
    def __init__(
        self,
        conf_path=f"{llm_agents.__path__[0]}/number-archetypes.yml",
        max_concurrency: int = 10,
        cache: RedisCache = None,
    ):
        super().__init__(
            conf_path=conf_path,
            agent_input=NumberArchetypesInput,
            agent_output=NumberArchetypesOutput,
            retries=3,
            max_concurrency=max_concurrency,
            cache=cache,
        )
