import os
import uuid
import logfire
import asyncio

from tqdm import tqdm
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


RESULTS_FILE_PATH = "/resources/test-results/results.json"
TEST_IMAGE_PATH = (
    "/resources/test-images/7202c5f8-6c10-410c-b064-761662aaf545.jpeg"
)

TEST_QURESTIONS = [
    # "I'm a material designer, and I've been questioning what does it mean for a material to be alive? How can living and lifelike materials explore their potential influence on design culture?",
    # "¿Qué implica para el futuro de nuestra sociedad el pensar una nueva especie del diseño desde una perspectiva material?",
    # "Que significa el movimiento en el mundo biomaterial?",
    # "What kind of animals have inspired active materials?",
    # "Como esta asociada la idea de movimiento con el concepto de lo vivo o de la vida?",
    # "Que suecede cuando la materia deja de obedecer y empieza a manifestar comportamientos propios?",
    "Como puedo convertirme en un verdadero artista?"
]


async def main() -> None:
    multi_agent = get_multi_agent()
    multi_agent.display_graph()

    context = get_multi_agent_context(test_mode=True)

    states = []
    for test_question in tqdm(TEST_QURESTIONS, ascii=True):
        image_id = uuid.uuid4().hex
        state = await multi_agent.run(
            input_state={
                "image_id": image_id,
                "image_path": TEST_IMAGE_PATH,
                "recorder_ok": True,
                "audio_transcription": test_question,
            },
            context=context,
            thread_id=image_id,
        )

        states.append(state)

    results = [
        {
            "question": state.audio_transcription,
            "nietzsche_advise": state.nietzsche_advise,
            "satc_advice": state.satc_advice,
            "machiavelli_advice": state.machiavelli_advice,
        }
        for state in states
    ]

    pprint(results)

    create_path(os.path.dirname(RESULTS_FILE_PATH))
    save_json(
        obj=results,
        file_path=RESULTS_FILE_PATH,
    )


if __name__ == "__main__":
    asyncio.run(main())
