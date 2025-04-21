import uuid
import asyncio

from rich.pretty import pprint
from common.logger import get_logger
from por.multi_agent import get_multi_agent, get_multi_agent_config


logger = get_logger(__name__)


async def main() -> None:
    multi_agent = get_multi_agent()
    multi_agent_config = get_multi_agent_config(model="grcra")

    while True:
        image_id = uuid.uuid4().hex
        state = await multi_agent.run(
            input_state={
                "image_id": image_id,
            },
            config=multi_agent_config,
            thread_id=image_id,
        )

        pprint(state)
        logger.info(f"image_url => {state['image_url']}")


if __name__ == "__main__":
    asyncio.run(main())
