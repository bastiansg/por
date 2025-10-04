from typing import Annotated
from functools import lru_cache

from qdrant_client import models
from qdrant_client.models import Record

from fastmcp.server import FastMCP
from pydantic import BaseModel, StrictStr, Field

from common.logger import get_logger

from rage.retriever import Retriever
from rage.utils.embeddings import get_openai_embeddings

from .utils import ToolCallLimitMiddleware


logger = get_logger(__name__)


SEARCH_TOP_K = 5
SEARCH_SCORE_THRESHOLD = 0.3


retriever = Retriever(dense_embeddings=get_openai_embeddings())
mcp = FastMCP(
    name="Oracle MCP server",
    host="0.0.0.0",
)


class TextChunk(BaseModel):
    text: StrictStr = Field(
        description="The actual textual content of the chunk."
    )

    artist: StrictStr | None = Field(
        description="The artist of the song if the text chunk contains lyrics.",
        default=None,
    )

    title: StrictStr | None = Field(
        description="The title of the song if the text chunk contains lyrics.",
        default=None,
    )

    chunk_id: StrictStr = Field(
        description="A unique identifier for this text chunk within the collection."
    )

    previous_chunk_id: StrictStr | None = Field(
        description="The chunk_id of the preceding text chunk within the same collection.",
        default=None,
    )

    next_chunk_id: StrictStr | None = Field(
        description="The chunk_id of the following text chunk within the same collection.",
        default=None,
    )


@lru_cache(maxsize=1)
def get_collections() -> list[str]:
    collections = retriever.qadrant_client.get_collections()
    return [c.name for c in collections.collections]


async def _search(
    query: str,
    collection_name: str,
    search_filter: models.Filter | None = None,
) -> list[TextChunk]:
    results = await retriever.dense_search(
        collection_name=collection_name,
        query=query,
        k=SEARCH_TOP_K,
        score_threshold=SEARCH_SCORE_THRESHOLD,
        search_filter=search_filter,
    )

    results = sorted(
        results,
        key=lambda x: (
            x.metadata["document_index"],
            x.metadata["chunk_index"],
        ),
    )

    return [
        TextChunk(
            text=r.text,
            artist=r.metadata.get("artist"),
            title=r.metadata.get("title"),
            chunk_id=r.metadata["chunk_id"],
            previous_chunk_id=r.metadata["previous_chunk_id"],
            next_chunk_id=r.metadata["next_chunk_id"],
        )
        for r in results
    ]


def _get_text_chunk(chunk_id: str) -> Record | None:
    scroll_filter = models.Filter(
        must=[
            models.FieldCondition(
                key="metadata.chunk_id",
                match=models.MatchValue(value=chunk_id),
            )
        ]
    )

    # FIXME: This is temporal!
    results = []
    collections = get_collections()
    for collection in collections:
        results = retriever.scroll(
            collection_name=collection,
            limit=1,
            scroll_filter=scroll_filter,
        )

        if len(results):
            break

    if not len(results):
        logger.error(f"no results found for chunk_id: {chunk_id}")
        return None

    result = results[0]
    return result


@mcp.tool(
    name="nietzsche_search",
    description="Run a semantic search across Nietzsche sources.",
)
async def nietzsche_search(
    query: Annotated[
        str,
        Field(
            description="The natural language query in Spanish to search for relevant text chunks."
        ),
    ],
) -> list[TextChunk]:
    """Run a semantic search across Nietzsche sources."""

    return await _search(
        query=query,
        collection_name="nietzsche",
    )


@mcp.tool(
    name="lyrics_search",
    description="Run a semantic search across Lyrics sources.",
)
async def lyrics_search(
    query: Annotated[
        str,
        Field(
            description="The natural language query in English to search for relevant text chunks."
        ),
    ],
) -> list[TextChunk]:
    """Run a semantic search across Lyrics sources."""

    return await _search(
        query=query,
        collection_name="lyrics",
    )


@mcp.tool(
    name="the_art_of_thinking_search",
    description="Run a semantic search across The Art of Thinking book sources.",
)
async def the_art_of_thinking_search(
    query: Annotated[
        str,
        Field(
            description="The natural language query in Spanish to search for relevant text chunks."
        ),
    ],
) -> list[TextChunk]:
    """Run a semantic search across The Art of Thinking book sources."""

    return await _search(
        query=query,
        collection_name="el-arte-del-pensamiento-creativo",
    )


@mcp.tool(
    name="get_text_chunk",
    description="Retrieve a specific text chunk using its `chunk_id`.",
)
def get_text_chunk(
    chunk_id: Annotated[
        str, Field(description="The `chunk_id` of the chunk to retrieve.")
    ],
) -> TextChunk | None:
    """Retrieve a specific text chunk using its `chunk_id`."""

    result = _get_text_chunk(chunk_id=chunk_id)
    if result is None:
        return

    assert result.payload is not None
    return TextChunk(
        text=result.payload["page_content"],
        artist=result.payload["metadata"].get("artist"),
        title=result.payload["metadata"].get("title"),
        chunk_id=result.payload["metadata"]["chunk_id"],
        previous_chunk_id=result.payload["metadata"]["previous_chunk_id"],
        next_chunk_id=result.payload["metadata"]["next_chunk_id"],
    )


if __name__ == "__main__":
    mcp.add_middleware(ToolCallLimitMiddleware())
    mcp.run(transport="streamable-http")
