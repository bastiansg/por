from typing import Any

from multi_agents.graph import Node
from common.logger import get_logger

from por.llm_agents.tools import satc_search_tool, get_text_chunks_tool
from por.multi_agent.schema import StateSchema
from por.llm_agents import (
    SATCAdvisor,
    SATCAdvisorDeps,
    RetrievalAssistant,
    RetrievalAssistantDeps,
)

from .utils import _get_text_chunks


logger = get_logger(__name__)


COLLECTION_NAME = "satc"


async def run(state: StateSchema) -> dict[str, Any]:
    logger.info("runing satc_advisor...")

    psychological_profile = state.psychological_profile
    audio_transcription = state.audio_transcription

    assert psychological_profile is not None
    assert audio_transcription is not None

    detected_language = state.detected_language
    assert detected_language is not None

    ra = RetrievalAssistant(
        tools=[
            satc_search_tool,
            get_text_chunks_tool,  # type: ignore
        ]
    )

    question_text = f"**Question**: {audio_transcription}"
    ra_output = await ra.generate(
        user_prompt=question_text,
        agent_deps=RetrievalAssistantDeps(
            search_tool="satc_search",
            search_languages=["English"],  # type: ignore
            collection_name=COLLECTION_NAME,
        ),
    )

    ra_text_chunks = await _get_text_chunks(
        relevant_chunk_ids=ra_output.relevant_chunk_ids,
        collection_name=COLLECTION_NAME,
    )

    sa = SATCAdvisor()
    satc_output = await sa.generate(
        user_prompt=question_text,
        agent_deps=SATCAdvisorDeps(
            psychological_profile=psychological_profile,
            text_chunks=ra_text_chunks,
            output_language=detected_language,
        ),
    )

    sa_text_chunks = await _get_text_chunks(
        relevant_chunk_ids=satc_output.relevant_chunk_ids,
        collection_name=COLLECTION_NAME,
    )

    return {
        "satc_advice": satc_output.answer,
        "satc_text_chunks": sa_text_chunks,
    }


satc_advisor = Node(
    name="satc_advisor",
    run=run,
)
