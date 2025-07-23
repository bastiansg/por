import uuid
import asyncio


from rich.pretty import pprint
from common.logger import get_logger
from common.utils.path import create_path
from common.utils.json_data import save_json

from por.multi_agent.schema import StateSchema
from por.multi_agent import get_multi_agent, get_multi_agent_config


logger = get_logger(__name__)


STORE_PATH = "/resources/states"
create_path(STORE_PATH)


async def main() -> None:
    multi_agent = get_multi_agent()
    multi_agent_config = get_multi_agent_config()

    while True:
        image_id = uuid.uuid4().hex
        state = await multi_agent.run(
            input_state={
                "image_id": image_id,
            },
            config=multi_agent_config,
            thread_id=image_id,
        )

        state = StateSchema(**state)
        state = state.model_dump()
        pprint(state)

        save_json(
            obj=state,
            file_path=f"{STORE_PATH}/{image_id}.json",
        )


if __name__ == "__main__":
    asyncio.run(main())
