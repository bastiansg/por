from por.llm_agents.web_search_agent import format_wikipedia_query


def test_format_wikipedia_query_adds_site_filter() -> None:
    assert format_wikipedia_query("mycelium fungal networks") == (
        "site:wikipedia.org mycelium fungal networks"
    )
