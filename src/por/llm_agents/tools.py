from typing import Annotated, Literal

from rich.console import Console
from qdrant_client import models

from pydantic import Field
from pydantic_ai import Tool, RunContext

from por.meta.schema import TextChunk
from por.db.qdrant import (
    hybrid_search,
    _get_text_chunks,
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


async def ancora_search(
    query: Annotated[
        str,
        Field(
            description="Query to search for relevant Ancora text chunks."
        ),
    ],
) -> list[TextChunk]:
    """Run a hybrid search across Ancora sources.

    Args:
        query: Query to search for relevant Ancora text chunks.
    """

    return await hybrid_search(
        query=query,
        collection_name="ancora",
    )


async def rwalsh_search(
    query: Annotated[
        str,
        Field(
            description="Spanish query to search for relevant Rodolfo Walsh text chunks."
        ),
    ],
) -> list[TextChunk]:
    """Run a hybrid search across Rodolfo Walsh sources.

    Args:
        query: Spanish query to search for relevant Rodolfo Walsh text chunks.
    """

    return await hybrid_search(
        query=query,
        collection_name="rodolfo-walsh",
    )


async def pr_search(
    query: Annotated[
        str,
        Field(
            description=(
                "Spanish query to search for relevant Indio Solari lyrics "
                "text chunks."
            )
        ),
    ],
) -> list[TextChunk]:
    """Run a hybrid search across Indio Solari lyrics.

    Args:
        query: Spanish query to search for relevant Indio Solari lyrics text
            chunks.
    """

    return await hybrid_search(
        query=query,
        collection_name="lyrics",
    )


async def get_text_chunks(
    ctx: RunContext,
    chunk_ids: Annotated[
        list[str],
        Field(description="chunk_id values of the text chunks to retrieve."),
    ],
) -> list[TextChunk]:
    """Retrieve specific text chunks using their chunk_id values.

    Args:
        ctx: Runtime context with collection dependencies.
        chunk_ids: chunk_id values of the text chunks to retrieve.
    """

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

ancora_search_tool = Tool(
    function=ancora_search,
    description="Run a hybrid search across Ancora sources.",
    docstring_format="google",
    require_parameter_descriptions=True,
)

rwalsh_search_tool = Tool(
    function=rwalsh_search,
    description=(
        "Run a hybrid search across Rodolfo Walsh sources using a Spanish query."
    ),
    docstring_format="google",
    require_parameter_descriptions=True,
)

pr_search_tool = Tool(
    function=pr_search,
    description=(
        "Run a hybrid search across Indio Solari lyrics using a Spanish query."
    ),
    docstring_format="google",
    require_parameter_descriptions=True,
)

get_text_chunks_tool = Tool(
    function=get_text_chunks,
    description="Retrieve specific text chunks using their chunk_id values.",
    docstring_format="google",
    require_parameter_descriptions=True,
)
