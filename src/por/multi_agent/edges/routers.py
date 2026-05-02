from typing import Hashable
from langgraph.graph import END

from por.multi_agent.schema import StateSchema


def recorder_conditional_router(state: StateSchema) -> list[Hashable]:
    if state.recorder_ok:
        return ["audio_transcriber"]
    return [END]


def validation_checkpoint_conditional_router(
    state: StateSchema,
) -> list[Hashable]:
    if state.message_accepted:
        return [
            "random_selector",
            "image_describer",
            "psychological_describer",
        ]

    return ["printer"]
