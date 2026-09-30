from pathlib import Path
from typing import TypeVar

from ddgs.exceptions import DDGSException
from pydantic_ai import Agent, Tool
from pydantic_ai.capabilities import WebSearch
from pydantic_ai.common_tools.duckduckgo import (
    DuckDuckGoResult,
    duckduckgo_search_tool,
)
from pydantic_ai.models.openai import OpenAIResponsesModelSettings

DepsT = TypeVar("DepsT")
MATTERS_OF_ACTIVITY_SEARCH_PREFIX = "site:matters-of-activity.de"


def format_matters_of_activity_query(query: str) -> str:
    return f"{MATTERS_OF_ACTIVITY_SEARCH_PREFIX} {query}"


def get_web_search_agent(
    deps_type: type[DepsT],
) -> Agent[DepsT, list[DuckDuckGoResult]]:
    search_tool = duckduckgo_search_tool(max_results=5)

    async def search(query: str) -> list[DuckDuckGoResult]:
        try:
            return await search_tool.function(format_matters_of_activity_query(query))
        except DDGSException as error:
            if str(error) == "No results found.":
                return []

            raise

    agent = Agent(
        name="web-search-agent",
        description="Finds relevant web sources for retrieval gaps.",
        model="openai:gpt-5.6-luna",
        model_settings=OpenAIResponsesModelSettings(
            openai_reasoning_effort="low"
        ),
        deps_type=deps_type,
        output_type=list[DuckDuckGoResult],
        capabilities=[
            WebSearch(
                native=False,
                local=Tool(
                    search,
                    name="duckduckgo_search",
                    description=search_tool.description,
                ),
            ),
        ],
    )

    @agent.system_prompt
    def get_system_prompt() -> str:
        return Path(__file__).with_name("system-prompt.md").read_text()

    return agent
