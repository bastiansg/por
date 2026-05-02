from qdrant_client import models
from qdrant_client.models import Record

from rich.console import Console

from rage.retriever import Retriever
from rage.utils.embeddings import get_openai_embeddings

from por.meta.schema import TextChunk


console = Console()


SEARCH_TOP_K = 5
SEARCH_SCORE_THRESHOLD = 0.3


retriever = Retriever(dense_embeddings=get_openai_embeddings())


async def dense_search(
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

    return [TextChunk(**r.model_dump()) for r in results]


async def hybrid_search(
    query: str,
    collection_name: str,
    search_filter: models.Filter | None = None,
) -> list[TextChunk]:
    results = await retriever.hybrid_search(
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

    return [TextChunk(**r.model_dump()) for r in results]


async def _get_text_chunks(
    collection_name: str,
    key: str,
    values: list[str],
) -> list[Record]:
    match = models.MatchAny(any=values)  # type: ignore
    scroll_filter = models.Filter(
        must=[
            models.FieldCondition(
                key=f"metadata.{key}",
                match=match,
            )
        ]
    )

    results = await retriever.scroll(
        collection_name=collection_name,
        limit=len(values),
        scroll_filter=scroll_filter,
    )

    return results
