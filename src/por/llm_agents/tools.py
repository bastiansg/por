from typing import Annotated, Literal

from pydantic import Field
from pydantic_ai import RunContext, Tool
from qdrant_client import models
from rich.console import Console

from por.db.qdrant import (
    hybrid_search,
    retriever,
)
from por.meta.schema import ChunkMetadataFilter, TextChunk

console = Console()


SEARCH_TOP_K = 5
SEARCH_SCORE_THRESHOLD = 0.3


async def matter_search(
    query: Annotated[
        str,
        Field(description="Query to search for relevant Matter text chunks."),
    ],
    query_language: Annotated[
        Literal["English", "Spanish", "French"],
        Field(description="Language of the query and matching Matter chunks."),
    ],
) -> list[TextChunk]:
    """Run a hybrid search exclusively across Matter sources.

    Args:
        query: Query to search for relevant Matter text chunks.
        query_language: Language of the query and matching Matter chunks.
    """

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
        collection_name="matter",
        search_filter=search_filter,
    )


async def search_by_chunk_metadata_filters(
    ctx: RunContext,
    query: Annotated[
        str,
        Field(description="Query to search for relevant text chunks."),
    ],
    metadata_filters: Annotated[
        list[ChunkMetadataFilter],
        Field(
            description="Chunk metadata key and value filters to narrow the search by.",
            min_length=1,
        ),
    ],
) -> list[TextChunk]:
    """Run a hybrid search filtered by chunk metadata values.

    Args:
        query: Query to search for relevant text chunks.
        metadata_filters: Chunk metadata key and value filters to narrow
            the search by.
    """

    deps = ctx.deps
    assert deps is not None

    search_filter = models.Filter(
        must=[
            models.FieldCondition(
                key=f"metadata.{metadata_filter.key}",
                match=models.MatchValue(value=metadata_filter.value),
            )
            for metadata_filter in metadata_filters
        ],
    )

    return await hybrid_search(
        query=query,
        collection_name=deps.collection_name,  # type: ignore
        search_filter=search_filter,
    )


async def get_neighboring_text_chunks(
    ctx: RunContext,
    chunk_id: Annotated[
        str,
        Field(description="chunk_id value of the center text chunk."),
    ],
    before: Annotated[
        int,
        Field(description="Number of previous chunks to retrieve.", ge=0, le=5),
    ] = 1,
    after: Annotated[
        int,
        Field(description="Number of next chunks to retrieve.", ge=0, le=5),
    ] = 1,
) -> list[TextChunk]:
    """Retrieve neighboring text chunks around a center chunk.

    Args:
        chunk_id: chunk_id value of the center text chunk.
        before: Number of previous chunks to retrieve.
        after: Number of next chunks to retrieve.
    """

    deps = ctx.deps
    assert deps is not None

    chunks = await retriever.get_neighboring_text_chunks(
        collection_name=deps.collection_name,  # type: ignore
        chunk_id=chunk_id,
        before=before,
        after=after,
    )

    return [TextChunk(**chunk.model_dump()) for chunk in chunks]


matter_search_tool = Tool(
    function=matter_search,
    description="Run a hybrid search exclusively across Matter sources.",
    docstring_format="google",
    require_parameter_descriptions=True,
)

search_by_chunk_metadata_filters_tool = Tool(
    function=search_by_chunk_metadata_filters,
    description="Run a hybrid search filtered by chunk metadata values.",
    docstring_format="google",
    require_parameter_descriptions=True,
)

get_neighboring_text_chunks_tool = Tool(
    function=get_neighboring_text_chunks,
    description="Retrieve neighboring text chunks around a center chunk.",
    docstring_format="google",
    require_parameter_descriptions=True,
)
