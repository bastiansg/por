from typing import Any

from multi_agents.graph import Node
from rich.console import Console

from por.multi_agent.schema import StateSchema
from por.llm_agents.tools import pr_search_tool, get_text_chunks_tool
from por.llm_agents import (
    PRAdvisor,
    PRAdvisorDeps,
    RetrievalAssistant,
    RetrievalAssistantDeps,
)

from .utils import get_relevant_text_chunks


console = Console()


COLLECTION_NAME = "lyrics"


async def run(state: StateSchema) -> dict[str, Any]:
    console.log("running pr_advisor...")

    audio_transcription = state.audio_transcription
    assert audio_transcription is not None

    retrieval_assistant = RetrievalAssistant(
        tools=[
            pr_search_tool,
            get_text_chunks_tool,  # type: ignore
        ]
    )

    question_text = f"**Question**: {audio_transcription}"
    ra_output = await retrieval_assistant.generate(
        user_prompt=question_text,
        agent_deps=RetrievalAssistantDeps(
            search_tool="pr_search",
            search_languages=["Spanish"],  # type: ignore
            collection_name=COLLECTION_NAME,
        ),
    )

    ra_text_chunks = await get_relevant_text_chunks(
        relevant_chunk_ids=ra_output.relevant_chunk_ids,
        collection_name=COLLECTION_NAME,
    )

    pr_advisor = PRAdvisor()
    pr_output = await pr_advisor.generate(
        user_prompt=question_text,
        agent_deps=PRAdvisorDeps(
            text_chunks=ra_text_chunks,
        ),
    )

    pr_text_chunks = await get_relevant_text_chunks(
        relevant_chunk_ids=pr_output.relevant_chunk_ids,
        collection_name=COLLECTION_NAME,
    )

    return {
        "pr_phrase": pr_output.phrase,
        "pr_text_chunks": pr_text_chunks,
    }


pr_advisor = Node(
    name="pr_advisor",
    run=run,
)
