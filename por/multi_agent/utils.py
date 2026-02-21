from functools import lru_cache
from por.data import dc_poems, fc_messages

from .schema import ContextSchema
from .config import MultiAgentConfig


@lru_cache()
def get_multi_agent_context(test_mode: bool = False) -> ContextSchema:
    return ContextSchema(
        **(
            MultiAgentConfig().model_dump()
            | {
                "dc_poems": [
                    {
                        "poem_id": idx,
                        "poem": poem,
                    }
                    for idx, poem in enumerate(
                        dc_poems,
                        start=1,
                    )
                ],
                "fc_messages": [
                    {
                        "message_id": idx,
                        "message": message,
                    }
                    for idx, message in enumerate(
                        fc_messages,
                        start=1,
                    )
                ],
                "test_mode": test_mode,
            }
        )
    )
