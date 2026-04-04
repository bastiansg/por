from typing import Any

from multi_agents.graph import Node
from common.logger import get_logger

from por.llm_agents import QueryParser
from por.multi_agent.schema import StateSchema


logger = get_logger(__name__)


async def run(state: StateSchema) -> dict[str, Any]:
    logger.info("runing query_parser...")

    astrology_placements = state.astrology_placements
    audio_transcription = state.audio_transcription

    assert astrology_placements is not None
    assert audio_transcription is not None

    if not any(
        (
            astrology_placements.sun,
            astrology_placements.moon,
            astrology_placements.rising,
        )
    ):
        return {
            "parsed_query": state.audio_transcription,
        }

    query_parser_agent = QueryParser()
    query_parser_output = await query_parser_agent.generate(
        user_prompt=f"**User Query**: {audio_transcription}",
    )

    return {
        "parsed_query": query_parser_output.parsed_query,
    }


query_parser = Node(
    name="query_parser",
    run=run,
)
