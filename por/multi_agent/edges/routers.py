# from langgraph.graph import END
from por.multi_agent.schema import StateSchema


def gatekeeper_conditional_router(state: StateSchema) -> list[str]:
    if state.message_accepted:
        return [
            "random_selector",
            "psychological_describer",
        ]

    return ["printer"]
