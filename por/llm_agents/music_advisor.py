from pydantic_ai import ToolOutput
from pydantic_ai.usage import UsageLimits

from pydantic import BaseModel, StrictStr, Field
from pydantic_extra_types.language_code import LanguageName

from por.conf import llm_agents  # type: ignore
from llm_agents.meta.interfaces import LLMAgent

from .psychological_describer import PsychologicalDescriberOutput
from .utils import tool_logging_handler
from .tools import lyrics_search_tool


TOOL_CALL_LIMIT = 5


class MusicAdvisorDeps(BaseModel):
    psychological_profile: PsychologicalDescriberOutput
    question: StrictStr
    output_language: LanguageName


class MusicAdvisorOutput(BaseModel):
    music_advice: StrictStr = Field(
        description="A poetic and emotionally resonant piece of advice.",
        min_length=1,
    )

    relevant_chunk_id: StrictStr = Field(
        description="The `chunk_id` of the chunk used as inspiration for the lyrics.",
        min_length=1,
    )


class MusicAdvisor(LLMAgent[MusicAdvisorDeps, MusicAdvisorOutput]):
    def __init__(
        self,
        conf_path=f"{llm_agents.__path__[0]}/music-advisor.yml",
        max_concurrency: int = 10,
    ):
        super().__init__(
            conf_path=conf_path,
            deps_type=MusicAdvisorDeps,
            output_type=ToolOutput(MusicAdvisorOutput),  # type: ignore
            retries=3,
            max_concurrency=max_concurrency,
            tools=[lyrics_search_tool],
            usage_limits=UsageLimits(tool_calls_limit=TOOL_CALL_LIMIT),
            event_stream_handler=tool_logging_handler,  # type: ignore
        )
