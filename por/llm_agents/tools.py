from pydantic_ai import Tool
from pydantic import Field

from common.logger import get_logger

from rage.retriever import Retriever
from rage.utils.embeddings import get_openai_embeddings

from por.meta.schema import TextChunk
from por.db.qdrant import dense_search, get_text_chunk_from_collections


logger = get_logger(__name__)


SEARCH_TOP_K = 5
SEARCH_SCORE_THRESHOLD = 0.3


retriever = Retriever(dense_embeddings=get_openai_embeddings())


async def nietzsche_search(
    query: str = Field(
        description="The natural language query in Spanish to search for relevant text chunks."
    ),
) -> list[TextChunk]:
    """Run a semantic search across Nietzsche sources."""

    return await dense_search(
        query=query,
        collection_name="nietzsche",
    )


# async def lyrics_search(
#     query: Annotated[
#         str,
#         Field(
#             description="The natural language query in English to search for relevant text chunks."
#         ),
#     ],
# ) -> list[TextChunk]:
#     """Run a semantic search across Lyrics sources."""

#     return await _search(
#         query=query,
#         collection_name="lyrics",
#     )


async def satc_search(
    query: str = Field(
        description="The natural language query in English to search for relevant text chunks."
    ),
) -> list[TextChunk]:
    """Run a semantic search across Sex and the City scripts."""

    return await dense_search(
        query=query,
        collection_name="satc",
    )


async def machiavelli_search(
    query: str = Field(
        description="The natural language query in Spanish to search for relevant text chunks."
    ),
) -> list[TextChunk]:
    """Run a semantic search across Machiavelli sources."""

    return await dense_search(
        query=query,
        collection_name="machiavelli",
    )


async def get_text_chunk(
    chunk_id: str = Field(
        description="The `chunk_id` of the chunk to retrieve."
    ),
) -> TextChunk | None:
    """Retrieve a specific text chunk using its `chunk_id`."""

    record = await get_text_chunk_from_collections(
        key="chunk_id",
        value=chunk_id,
    )

    if record is None:
        return

    payload = record.payload
    assert payload is not None

    return TextChunk(
        text=payload["page_content"],
        metadata=payload["metadata"],
    )


nietzsche_search_tool = Tool(
    function=nietzsche_search,
    description="The natural language query in Spanish to search for relevant text chunks.",
)

# lyrics_search_tool = Tool(
#     function=lyrics_search,
#     description="The natural language query to search for relevant text chunks.",
# )

satc_search_tool = Tool(
    function=satc_search,
    description="The natural language query in English to search for relevant text chunks.",
)

machiavelli_search_tool = Tool(
    function=machiavelli_search,
    description="The natural language query in Spanish to search for relevant text chunks.",
)

get_text_chunk_tool = Tool(
    function=get_text_chunk,
    description="Retrieve a specific text chunk using its `chunk_id`.",
)
