from typing import Any

from multi_agents.graph import Node
from rich.console import Console

from por.multi_agent.schema import StateSchema
from por.llm_agents.tools import rwalsh_search_tool, get_text_chunks_tool
from por.llm_agents import (
    RWalshAdvisor,
    RWalshAdvisorDeps,
    RetrievalAssistant,
    RetrievalAssistantDeps,
)

from .utils import get_relevant_text_chunks


console = Console()


COLLECTION_NAME = "rodolfo-walsh"


async def run(state: StateSchema) -> dict[str, Any]:
    console.log("running rwalsh_advisor...")

    audio_transcription = state.audio_transcription
    assert audio_transcription is not None

    retrieval_assistant = RetrievalAssistant(
        tools=[
            rwalsh_search_tool,
            get_text_chunks_tool,  # type: ignore
        ]
    )

    question_text = f"**Question**: {audio_transcription}"
    ra_output = await retrieval_assistant.generate(
        user_prompt=question_text,
        agent_deps=RetrievalAssistantDeps(
            search_tool="rwalsh_search",
            search_languages=["Spanish"],  # type: ignore
            collection_name=COLLECTION_NAME,
        ),
    )

    ra_text_chunks = await get_relevant_text_chunks(
        relevant_chunk_ids=ra_output.relevant_chunk_ids,
        collection_name=COLLECTION_NAME,
    )

    rwalsh_advisor = RWalshAdvisor()
    rwalsh_output = await rwalsh_advisor.generate(
        user_prompt=question_text,
        agent_deps=RWalshAdvisorDeps(
            text_chunks=ra_text_chunks,
        ),
    )

    rwalsh_text_chunks = await get_relevant_text_chunks(
        relevant_chunk_ids=rwalsh_output.relevant_chunk_ids,
        collection_name=COLLECTION_NAME,
    )

    return {
        "rwalsh_phrase": rwalsh_output.phrase.capitalize(),
        "rwalsh_text_chunks": rwalsh_text_chunks,
    }


rwalsh_advisor = Node(
    name="rwalsh_advisor",
    run=run,
)
