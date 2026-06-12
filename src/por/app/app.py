import os
import uuid
import logfire
import asyncio

from functools import lru_cache

from rich.pretty import pprint
from rich.console import Console

from multi_agents.graph import MultiAgentGraph

from por.utils.json import save_json
from por.multi_agent import get_multi_agent, get_multi_agent_context


if os.getenv("LOGFIRE_TOKEN") is not None:
    logfire.configure(service_name="por")
    logfire.instrument_pydantic_ai()
    logfire.instrument_openai()


console = Console()


STORE_PATH = "/resources/states"
os.makedirs(STORE_PATH, exist_ok=True)


@lru_cache()
def _get_multi_agent() -> MultiAgentGraph:
    multi_agent = get_multi_agent()
    multi_agent.display_graph()

    return multi_agent


async def main() -> None:
    multi_agent = _get_multi_agent()
    context = get_multi_agent_context()

    while True:
        image_id = uuid.uuid4().hex
        state = await multi_agent.run(
            input_state={
                "image_id": image_id,
            },
            context=context,
            thread_id=image_id,
        )

        assert state is not None
        state = state.model_dump()
        pprint(state)

        invoked_at = state["invoked_at"]
        assert invoked_at is not None

        save_json(
            obj=state,
            file_path=f"{STORE_PATH}/{invoked_at}-{image_id}.json",
        )


if __name__ == "__main__":
    asyncio.run(main())
