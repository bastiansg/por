import os
import uuid
import logfire
import asyncio

from rich.pretty import pprint
from common.logger import get_logger
from common.utils.path import create_path
from common.utils.json_data import save_json

from por.multi_agent import get_multi_agent, get_multi_agent_context


if os.getenv("LOGFIRE_TOKEN") is not None:
    logfire.configure(service_name="por")
    logfire.instrument_pydantic_ai()
    logfire.instrument_mcp()
    logfire.instrument_openai()


logger = get_logger(__name__)


STORE_PATH = "/resources/states"
create_path(STORE_PATH)


async def main() -> None:
    multi_agent = get_multi_agent()
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

        save_json(
            obj=state,
            file_path=f"{STORE_PATH}/{image_id}.json",
        )


if __name__ == "__main__":
    asyncio.run(main())
