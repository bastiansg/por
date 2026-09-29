import asyncio
from unittest.mock import AsyncMock

import pytest

from por.llm_agents import tools
from por.llm_agents.tools import matter_search


def test_matter_search_is_restricted_to_matter_collection(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    hybrid_search = AsyncMock(return_value=[])
    monkeypatch.setattr(tools, "hybrid_search", hybrid_search)

    result = asyncio.run(
        matter_search(
            query="How does mycelium grow?",
            query_language="English",
        )
    )

    assert result == []
    assert hybrid_search.await_args.kwargs["collection_name"] == "matter"
    search_filter = hybrid_search.await_args.kwargs["search_filter"]
    assert search_filter.must[0].key == "metadata.language"
    assert search_filter.must[0].match.value == "English"
