from pydantic import BaseModel, StrictStr, NonNegativeInt, Field
from pydantic_extra_types.language_code import LanguageName

from common.cache import RedisCache

from por.conf import agents
from llm_agents.meta.interfaces import LLMAgent


class PersonDescriberInput(BaseModel):
    description_guidelines: StrictStr
    output_language: LanguageName


class PersonDescriberOutput(BaseModel):
    fears: StrictStr = Field(
        description="What the person is subconsciously afraid of."
    )
    dreams_and_desires: StrictStr = Field(
        description="The person's ambitions, longings, or life goals."
    )
    love_status: StrictStr = Field(
        description="The person's current emotional or romantic state."
    )
    lucky_number: NonNegativeInt = Field(
        description="A number that symbolically or intuitively resonates with the person's personality."
    )


class PersonDescriber(LLMAgent[PersonDescriberInput, PersonDescriberOutput]):
    def __init__(
        self,
        conf_path=f"{agents.__path__[0]}/person-describer.yml",
        max_concurrency: int = 10,
        cache: RedisCache = None,
    ):
        super().__init__(
            conf_path=conf_path,
            agent_input=PersonDescriberInput,
            agent_output=PersonDescriberOutput,
            max_concurrency=max_concurrency,
            cache=cache,
        )
