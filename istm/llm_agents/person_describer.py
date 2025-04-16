from pydantic import BaseModel, StrictStr

from common.cache import RedisCache

from istm.conf import agents
from llm_agents.meta.interfaces import LLMAgent


class PersonDescriberInput(BaseModel):
    description_guidelines: StrictStr


class PersonDescriberOutput(BaseModel):
    fears: StrictStr
    dreams_and_desires: StrictStr
    love_status: StrictStr
    lucky_number: StrictStr


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
