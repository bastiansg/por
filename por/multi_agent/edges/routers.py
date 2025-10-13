from typing import Hashable
from por.multi_agent.schema import StateSchema


def validation_checkpoint_conditional_router(
    state: StateSchema,
) -> list[Hashable]:
    if state.message_accepted:
        return [
            "random_selector",
            "psychological_describer",
        ]

    return ["printer"]
