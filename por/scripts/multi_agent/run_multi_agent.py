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
    logfire.instrument_openai()


logger = get_logger(__name__)


STORE_PATH = "/resources/states"
create_path(STORE_PATH)

TEST_IMAGE_PATH = (
    "/resources/test-images/7202c5f8-6c10-410c-b064-761662aaf545.jpeg"
)
QURESTION = "Como esta asociada la idea de movimiento con el concepto de lo vivo o de la vida?"


async def main() -> None:
    multi_agent = get_multi_agent()
    context = get_multi_agent_context(test_mode=True)
    image_id = uuid.uuid4().hex

    state = await multi_agent.run(
        input_state={
            "image_id": image_id,
            "image_path": TEST_IMAGE_PATH,
            "audio_transcription": QURESTION,
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
