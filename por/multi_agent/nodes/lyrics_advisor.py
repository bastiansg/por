from typing import Any

from multi_agents.graph import Node
from common.logger import get_logger

from por.multi_agent.schema import StateSchema
from por.llm_agents.tools import lyrics_search_tool, get_text_chunk_tool
from por.llm_agents import (
    LyricsAdvisor,
    LyricsAdvisorDeps,
    RetrievalAssistant,
    RetrievalAssistantDeps,
)

from .utils import get_text_chunks


logger = get_logger(__name__)


async def run(state: StateSchema) -> dict[str, Any]:
    logger.info("running lyrics_advisor...")

    psychological_profile = state.psychological_profile
    parsed_query = state.parsed_query

    assert psychological_profile is not None
    assert parsed_query is not None

    detected_language = state.detected_language
    assert detected_language is not None

    ra = RetrievalAssistant(
        tools=[
            lyrics_search_tool,
            get_text_chunk_tool,
        ]
    )

    ra_output = await ra.generate(
        user_prompt=f"**Question**: {parsed_query}",
        agent_deps=RetrievalAssistantDeps(
            search_tool="lyrics_search",
            search_languages=["English", "Spanish"],  # type: ignore
        ),
    )

    ra_text_chunks = await get_text_chunks(
        relevant_chunk_ids=ra_output.relevant_chunk_ids,
        collection_name="lyrics",
    )

    la = LyricsAdvisor()
    la_output = await la.generate(
        user_prompt=("Recommend one song with a very short why."),
        agent_deps=LyricsAdvisorDeps(
            psychological_profile=psychological_profile,
            question=parsed_query,
            text_chunks=ra_text_chunks,
            output_language=detected_language,
        ),
    )

    return {
        "song": la_output.song,
        "lyrics_advise": la_output.reason,
        "lyrics_text_chunks": ra_text_chunks,
    }


lyrics_advisor = Node(
    name="lyrics_advisor",
    run=run,
)
