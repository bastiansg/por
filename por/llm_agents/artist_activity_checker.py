from pydantic_ai import ToolOutput
from pydantic_ai.common_tools.duckduckgo import duckduckgo_search_tool

from pydantic import BaseModel, StrictStr, Field, PositiveInt

from common.cache import RedisCache
from por.conf import llm_agents  # type: ignore
from llm_agents.meta.interfaces import LLMAgent


class ArtistActivityCheckerDeps(BaseModel):
    artist: StrictStr
    current_year: PositiveInt


class ArtistActivityCheckerOutput(BaseModel):
    last_year_active: PositiveInt = Field(
        description="Verified last active year."
    )

    relevant_urls: list[StrictStr] = Field(
        description="Source URLs used for verification.",
        min_length=1,
    )


class ArtistActivityChecker(
    LLMAgent[ArtistActivityCheckerDeps, ArtistActivityCheckerOutput]
):
    def __init__(
        self,
        conf_path=f"{llm_agents.__path__[0]}/artist-activity-checker.yml",
        max_concurrency: int = 10,
        cache: RedisCache | None = None,
    ):
        super().__init__(
            conf_path=conf_path,
            deps_type=ArtistActivityCheckerDeps,
            tools=[duckduckgo_search_tool()],
            output_type=ToolOutput(ArtistActivityCheckerOutput),  # type: ignore
            retries=3,
            max_concurrency=max_concurrency,
            cache=cache,
        )
