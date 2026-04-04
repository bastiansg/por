from typing import Any

from multi_agents.graph import Node
from common.logger import get_logger

from por.multi_agent.schema import StateSchema
from por.llm_agents.tools import philosophy_search_tool, get_text_chunk_tool
from por.llm_agents import (
    NietzscheAdvisor,
    NietzscheAdvisorDeps,
    RetrievalAssistant,
    RetrievalAssistantDeps,
)

from .utils import get_text_chunks


logger = get_logger(__name__)


async def run(state: StateSchema) -> dict[str, Any]:
    logger.info("runing nietzsche_advisor...")

    psychological_profile = state.psychological_profile
    parsed_query = state.parsed_query

    assert psychological_profile is not None
    assert parsed_query is not None

    detected_language = state.detected_language
    assert detected_language is not None

    ra = RetrievalAssistant(
        tools=[
            philosophy_search_tool,
            get_text_chunk_tool,
        ]
    )

    ra_output = await ra.generate(
        user_prompt=f"**Question**: {parsed_query}",
        agent_deps=RetrievalAssistantDeps(
            search_tool="philosophy_search",
            search_languages=["Spanish"],  # type: ignore
        ),
    )

    ra_text_chunks = await get_text_chunks(
        relevant_chunk_ids=ra_output.relevant_chunk_ids,
        collection_name="philosophy",
    )

    na = NietzscheAdvisor()
    na_output = await na.generate(
        user_prompt="Deliver your piercing, symbolic, and transformative message.",
        agent_deps=NietzscheAdvisorDeps(
            psychological_profile=psychological_profile,
            question=parsed_query,
            text_chunks=ra_text_chunks,
            output_language=detected_language,
        ),
    )

    na_text_chunks = await get_text_chunks(
        relevant_chunk_ids=na_output.relevant_chunk_ids,
        collection_name="philosophy",
    )

    return {
        "nietzsche_advise": na_output.answer,
        "nietzsche_text_chunks": na_text_chunks,
    }


nietzsche_advisor = Node(
    name="nietzsche_advisor",
    run=run,
)
