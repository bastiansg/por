from typing import Annotated
from qdrant_client import models

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, StrictStr, NonNegativeFloat, PositiveInt, Field

from rage.retriever import Retriever
from common.logger import get_logger
from common.utils.yaml_data import load_yaml

from por.conf import mcp_instructions


logger = get_logger(__name__)


retriever = Retriever()
mcp = FastMCP(
    name="Oracle MCP server",
    instructions=load_yaml(
        file_path=f"{mcp_instructions.__path__[0]}/instructions.yaml"
    )["instructions"],
    host="0.0.0.0",
)


class TextChunk(BaseModel):
    collection: StrictStr = Field(
        description="The name of the collection the text chunk belongs to."
    )

    text: StrictStr = Field(
        description="The actual textual content of the chunk."
    )

    file_name: StrictStr = Field(
        description="The source file name from which the chunk was extracted."
    )

    chunk_id: PositiveInt = Field(
        description="The sequential ID of the chunk within the file."
    )


class SemanticSearchResult(TextChunk):
    score: NonNegativeFloat = Field(
        description="The similarity score between the query and this result."
    )


@mcp.tool(
    name="nietzsche_semantic_search",
    description="Perform a dense vector semantic search across all works of Nietzsche.",
)
async def nietzsche_semantic_search(
    query: Annotated[
        str,
        Field(
            description="The natural language query to search for relevant Nietzsche passages."
        ),
    ],
) -> list[SemanticSearchResult]:
    """Perform semantic search across Nietzsche's texts."""

    results = await retriever.dense_search(
        collection_name="nietzsche",
        query=query,
        k=5,
    )

    search_results = (
        SemanticSearchResult(
            text=r.text,
            file_name=r.metadata["file_name"],
            chunk_id=r.metadata["chunk_id"],
            collection="nietzsche",
            score=r.score,
        )
        for r in results
    )

    return sorted(
        search_results,
        key=lambda x: (x.file_name, x.chunk_id),
    )


@mcp.tool(
    name="get_text_chunk",
    description="Retrieve a specific text chunk by its collection, file name, and chunk ID.",
)
def get_text_chunk(
    collection: Annotated[
        str,
        Field(
            description="The name of the collection containing the text chunk."
        ),
    ],
    file_name: Annotated[
        str,
        Field(
            description="The name of the file from which the chunk originates."
        ),
    ],
    chunk_id: Annotated[
        int,
        Field(description="The ID of the chunk to retrieve."),
    ],
) -> TextChunk | None:
    """Retrieve a specific text chunk based on collection, file name, and chunk ID."""

    scroll_filter = models.Filter(
        must=[
            models.FieldCondition(
                key="metadata.file_name",
                match=models.MatchValue(value=file_name),
            ),
            models.FieldCondition(
                key="metadata.chunk_id",
                match=models.MatchValue(value=chunk_id),
            ),
        ],
    )

    results, _ = retriever.scroll(
        collection_name=collection,
        limit=1,
        scroll_filter=scroll_filter,
    )

    if not results:
        return None

    result = results[0]
    return TextChunk(
        text=result.payload["page_content"],
        file_name=result.payload["metadata"]["file_name"],
        chunk_id=result.payload["metadata"]["chunk_id"],
        collection=collection,
    )


# @mcp.resource(
#     uri="resource://locations",
#     name="get_locations",
#     description="Provides a list of all locations.",
# )
# def get_locations() -> list[str]:
#     """Provides a list of all locations."""

#     results = scroll_by_text_type(text_type="dialog")
#     locations = unique_everseen(
#         r.payload["metadata"]["location"] for r in results
#     )

#     return list(locations)


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
