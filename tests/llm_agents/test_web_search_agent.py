from por.llm_agents.web_search_agent import format_matters_of_activity_query


def test_format_matters_of_activity_query_adds_site_filter() -> None:
    assert format_matters_of_activity_query("mycelium fungal networks") == (
        "site:matters-of-activity.de mycelium fungal networks"
    )
