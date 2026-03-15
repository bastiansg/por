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
    # "¿Cuál es el material relacionado con la amistad?",
    # "¿Qué es un marco?",
    # "¿Cuál es el estado favorito de la materia?",
    # "¿Qué material soy?",
    # "¿Qué es el materialismo histórico?",
    # "¿Qué maduro, la navaja o la ostra?",
    # "Si el amor fuese un material, ¿qué material sería?",
    ##########################################################
    "¿Quién es el autor de la obra o autora?",
    "¿Qué quisiste hacer con la obra?",
    "¿Por qué aparecen moras la obra?",
    "¿Qué quisés hacer con la obra, atraer?",
    "¿Quién creó esta exposición?",
    "¿Qué te inspiró para hacer la obra crecer?",
    "Hola, ¿me puedes decir de qué se trata exactamente la exposición de arte?",
    "¿Cuál es la intención de la expo de atraer?",
    "¿Qué significado tienen los nombres de las obras?",
    "¿Qué significan los nombres de la exposición?",
    "¿Por qué interacción es imposible?",
    "¿Qué significa que el de las bolas no tenga ningún movimiento automatizado?",
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
                "audio_transcription": test_question,
                "recorder_ok": True,
            },
            context=context,
            thread_id=image_id,
        )

        states.append(state)

    results = [
        {
            "question": state.audio_transcription,
            "matter_advise": state.matter_advise,
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
