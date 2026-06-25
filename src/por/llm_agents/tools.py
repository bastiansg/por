from typing import Annotated, Literal

from rich.console import Console
from qdrant_client import models

from pydantic import Field
from pydantic_ai import Tool, RunContext

from por.meta.schema import TextChunk, ChunkMetadataFilter
from por.db.qdrant import (
    hybrid_search,
    _get_text_chunk,
    # _get_text_chunks,
)


console = Console()


SEARCH_TOP_K = 5
SEARCH_SCORE_THRESHOLD = 0.3


async def philosophy_search(
    query: Annotated[
        str,
        Field(
            description="Spanish query to search for relevant philosophy text chunks."
        ),
    ],
) -> list[TextChunk]:
    """Run a hybrid search across Philosophy sources.

    Args:
        query: Spanish query to search for relevant philosophy text chunks.
    """

    return await hybrid_search(
        query=query,
        collection_name="philosophy",
    )


async def satc_search(
    query: Annotated[
        str,
        Field(
            description="English query to search for relevant Sex and the City text chunks."
        ),
    ],
) -> list[TextChunk]:
    """Run a hybrid search across Sex and the City scripts.

    Args:
        query: English query to search for relevant Sex and the City text
            chunks.
    """

    return await hybrid_search(
        query=query,
        collection_name="satc",
    )


async def astrology_search(
    query: Annotated[
        str,
        Field(
            description="Query to search for relevant astrology text chunks."
        ),
    ],
) -> list[TextChunk]:
    """Run a hybrid search across Astrology sources.

    Args:
        query: Query to search for relevant astrology text chunks.
    """

    return await hybrid_search(
        query=query,
        collection_name="astrology",
    )


async def lyrics_search(
    query: Annotated[
        str,
        Field(description="Query to search for relevant lyrics text chunks."),
    ],
    query_language: Annotated[
        Literal[
            "English",
            "Spanish",
            "French",
        ],
        Field(
            description="Language of the input query and matching lyrics chunks."
        ),
    ],
) -> list[TextChunk]:
    """Run a hybrid search across Lyrics sources.

    Args:
        query: Query to search for relevant lyrics text chunks.
        query_language: Language of the input query and matching lyrics chunks.
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
        collection_name="lyrics",
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
        collection_name=deps.collection_name,
        search_filter=search_filter,
    )


# async def get_text_chunks(
#     ctx: RunContext,
#     chunk_ids: Annotated[
#         list[str],
#         Field(description="chunk_id values of the text chunks to retrieve."),
#     ],
# ) -> list[TextChunk]:
#     """Retrieve specific text chunks using their chunk_id values.

#     Args:
#         chunk_ids: chunk_id values of the text chunks to retrieve.
#     """

#     deps = ctx.deps
#     assert deps is not None

#     records = await _get_text_chunks(
#         collection_name=deps.collection_name,
#         key="chunk_id",
#         values=chunk_ids,
#     )

#     return [
#         TextChunk(
#             text=r.payload["page_content"],  # type: ignore
#             metadata=r.payload["metadata"],  # type: ignore
#         )
#         for r in records
#     ]


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

    async def get_text_chunk(value: str) -> TextChunk | None:
        record = await _get_text_chunk(
            collection_name=deps.collection_name,
            key="chunk_id",
            value=value,
        )

        if record is None or record.payload is None:
            return None

        return TextChunk(
            text=record.payload["page_content"],  # type: ignore
            metadata=record.payload["metadata"],  # type: ignore
        )

    center = await get_text_chunk(chunk_id)
    if center is None:
        return []

    previous_chunks: list[TextChunk] = []
    current = center

    for _ in range(before):
        previous_chunk_id = current.metadata.previous_chunk_id
        if previous_chunk_id is None:
            break

        current = await get_text_chunk(previous_chunk_id)
        if current is None:
            break

        previous_chunks.append(current)

    next_chunks: list[TextChunk] = []
    current = center

    for _ in range(after):
        next_chunk_id = current.metadata.next_chunk_id
        if next_chunk_id is None:
            break

        current = await get_text_chunk(next_chunk_id)
        if current is None:
            break

        next_chunks.append(current)

    return [
        *reversed(previous_chunks),
        center,
        *next_chunks,
    ]


philosophy_search_tool = Tool(
    function=philosophy_search,
    description=(
        "Run a hybrid search across Philosophy sources using a Spanish query."
    ),
    docstring_format="google",
    require_parameter_descriptions=True,
)

satc_search_tool = Tool(
    function=satc_search,
    description=(
        "Run a hybrid search across Sex and the City scripts using an English query."
    ),
    docstring_format="google",
    require_parameter_descriptions=True,
)

astrology_search_tool = Tool(
    function=astrology_search,
    description="Run a hybrid search across Astrology sources.",
    docstring_format="google",
    require_parameter_descriptions=True,
)

lyrics_search_tool = Tool(
    function=lyrics_search,
    description="Run a hybrid search across Lyrics sources by language.",
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
