from functools import lru_cache
from qdrant_client import models
from typing import Annotated, Literal

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, StrictStr, NonNegativeFloat, Field

from rage.retriever import Retriever
from common.logger import get_logger


logger = get_logger(__name__)


mcp = FastMCP(
    name="Oracle MCP server",
    host="0.0.0.0",
)


@lru_cache(maxsize=1)
def get_retriever() -> Retriever:
    return Retriever()


class TextChunk(BaseModel):
    text: StrictStr = Field(
        description="The actual textual content of the chunk."
    )

    collection: StrictStr = Field(
        description="The name of the collection to which this text chunk belongs."
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

    artist: StrictStr | None = Field(
        description="The artist of the song if the text chunk contains lyrics.",
        default=None,
    )

    title: StrictStr | None = Field(
        description="The title of the song if the text chunk contains lyrics.",
        default=None,
    )


class SemanticSearchResult(TextChunk):
    score: NonNegativeFloat = Field(
        description="The similarity score between the query and this chunk."
    )


@mcp.tool(
    name="semantic_search",
    description="Perform a semantic search across all text chunks in the specified collection.",
)
async def semantic_search(
    collection: Annotated[
        Literal[
            "nietzsche",
            "el-arte-del-pensamiento-creativo",
            "lyrics",
        ],
        Field(description="The collection of documents to search within."),
    ],
    query: Annotated[
        str,
        Field(
            description="The natural language query to search for relevant text chunks."
        ),
    ],
) -> list[SemanticSearchResult]:
    """Perform a semantic search across all text chunks in the specified collection."""

    retriever = get_retriever()
    results = await retriever.dense_search(
        collection_name=collection,
        query=query,
        k=5,
    )

    results = sorted(
        results,
        key=lambda r: (
            r.metadata["document_index"],
            r.metadata["chunk_index"],
        ),
    )

    return [
        SemanticSearchResult(
            text=r.text,
            collection=collection,
            chunk_id=r.metadata["chunk_id"],
            previous_chunk_id=r.metadata["previous_chunk_id"],
            next_chunk_id=r.metadata["next_chunk_id"],
            artist=r.metadata.get("artist"),
            title=r.metadata.get("title"),
            score=r.score,
        )
        for r in results
    ]


@mcp.tool(
    name="get_text_chunk",
    description="Retrieve a specific text chunk from a collection using its unique chunk_id.",
)
def get_text_chunk(
    collection: Annotated[
        Literal[
            "nietzsche",
            "el-arte-del-pensamiento-creativo",
            "lyrics",
        ],
        Field(
            description="The collection from which to retrieve the text chunk."
        ),
    ],
    chunk_id: Annotated[
        str,
        Field(description="The unique chunk_id of the text chunk to retrieve."),
    ],
) -> TextChunk | None:
    """Retrieve a specific text chunk from a collection using its unique chunk_id."""

    scroll_filter = models.Filter(
        must=[
            models.FieldCondition(
                key="metadata.chunk_id",
                match=models.MatchValue(value=chunk_id),
            )
        ]
    )

    retriever = get_retriever()
    results, _ = retriever.scroll(
        collection_name=collection,
        limit=1,
        scroll_filter=scroll_filter,
    )

    if not results:
        logger.error(f"no results found for chunk_id: {chunk_id}")
        return None

    result = results[0]
    return TextChunk(
        text=result.payload["page_content"],
        collection=collection,
        chunk_id=result.payload["metadata"]["chunk_id"],
        previous_chunk_id=result.payload["metadata"]["previous_chunk_id"],
        artist=result.payload["metadata"].get("artist"),
        title=result.payload["metadata"].get("title"),
        next_chunk_id=result.payload["metadata"]["next_chunk_id"],
    )


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
