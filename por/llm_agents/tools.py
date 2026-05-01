from typing import Annotated, Literal

from pydantic import Field
from qdrant_client import models
from pydantic_ai import Tool, RunContext

from rich.console import Console

from rage.retriever import Retriever
from rage.utils.embeddings import get_openai_embeddings

from por.meta.schema import TextChunk
from por.db.qdrant import (
    hybrid_search,
    _get_text_chunks,
)


console = Console()


SEARCH_TOP_K = 5
SEARCH_SCORE_THRESHOLD = 0.3


retriever = Retriever(dense_embeddings=get_openai_embeddings())


async def philosophy_search(
    query: Annotated[
        str,
        Field(
            description="The query in Spanish to search for relevant text chunks."
        ),
    ],
) -> list[TextChunk]:
    """Run a hybrid search across Philosophy sources."""

    return await hybrid_search(
        query=query,
        collection_name="philosophy",
    )


async def satc_search(
    query: Annotated[
        str,
        Field(
            description="The query in English to search for relevant text chunks."
        ),
    ],
) -> list[TextChunk]:
    """Run a hybrid search across `Sex and the City` scripts."""

    return await hybrid_search(
        query=query,
        collection_name="satc",
    )


async def astrology_search(
    query: Annotated[
        str,
        Field(description="The query to search for relevant text chunks."),
    ],
) -> list[TextChunk]:
    """Run a hybrid search across Astrology sources."""

    return await hybrid_search(
        query=query,
        collection_name="astrology",
    )


async def lyrics_search(
    query: Annotated[
        str,
        Field(description="The query to search for relevant lyrics chunks."),
    ],
    query_language: Annotated[
        Literal[
            "English",
            "Spanish",
            "French",
        ],
        Field(description="The language of the input query."),
    ],
) -> list[TextChunk]:
    """Run a hybrid search across Lyrics sources."""

    search_filter = models.Filter(
        must=[
            models.FieldCondition(
                key="metadata.language",
                match=models.MatchValue(value=query_language),
            )
        ],
    )

    return await hybrid_search(
        query=query,
        collection_name="lyrics",
        search_filter=search_filter,
    )


async def get_text_chunks(
    ctx: RunContext,
    chunk_ids: Annotated[
        list[str],
        Field(description="The `chunk_id`s of the chunks to retrieve."),
    ],
) -> list[TextChunk]:
    """Retrieve specific text chunks using their `chunk_id`s."""

    deps = ctx.deps
    assert deps is not None

    records = await _get_text_chunks(
        collection_name=deps.collection_name,
        key="chunk_id",
        values=chunk_ids,
    )

    return [
        TextChunk(
            text=r.payload["page_content"],  # type: ignore
            metadata=r.payload["metadata"],  # type: ignore
        )
        for r in records
    ]


philosophy_search_tool = Tool(
    function=philosophy_search,
    description="Run a hybrid search across Philosophy sources.",
)

satc_search_tool = Tool(
    function=satc_search,
    description="Run a hybrid search across `Sex and the City` scripts.",
)

astrology_search_tool = Tool(
    function=astrology_search,
    description="Run a hybrid search across Astrology sources.",
)

lyrics_search_tool = Tool(
    function=lyrics_search,
    description="Run a hybrid search across Lyrics sources.",
)

get_text_chunks_tool = Tool(
    function=get_text_chunks,
    description="Retrieve specific text chunks using their `chunk_id`s.",
)
