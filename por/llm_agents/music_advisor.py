from pydantic import BaseModel, StrictStr, Field
from pydantic_extra_types.language_code import LanguageName

from common.cache import RedisCache

from por.conf import llm_agents
from llm_agents.meta.interfaces import LLMAgent


class Song(BaseModel):
    title: StrictStr
    artist: StrictStr
    lyrics: StrictStr


class MusicAdvisorInput(BaseModel):
    question: StrictStr
    psychological_profile: StrictStr
    song: Song
    output_language: LanguageName


class MusicAdvisorOutput(BaseModel):
    music_advice: StrictStr = Field(
        description="A poetic and emotionally resonant piece of advice.",
        min_length=1,
    )


class MusicAdvisor(LLMAgent[MusicAdvisorInput, MusicAdvisorOutput]):
    def __init__(
        self,
        conf_path=f"{llm_agents.__path__[0]}/music-advisor.yml",
        max_concurrency: int = 10,
        cache: RedisCache = None,
    ):
        super().__init__(
            conf_path=conf_path,
            agent_input=MusicAdvisorInput,
            agent_output=MusicAdvisorOutput,
            retries=3,
            max_concurrency=max_concurrency,
            cache=cache,
        )
