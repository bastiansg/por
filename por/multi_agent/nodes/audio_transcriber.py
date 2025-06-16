import replicate

from multi_agents.graph import Node
from common.logger import get_logger
from por.multi_agent.schema import StateSchema, ConfigSchema


logger = get_logger(__name__)


async def run(
    state: StateSchema,
    config: ConfigSchema,
) -> StateSchema:
    logger.info("runing audio_transcriber...")

    output = replicate.run(
        "vaibhavs10/incredibly-fast-whisper:3ab86df6c8f54c11309d4d1f930ac292bad43ace52d10c80d87eb258b3c9f79c",
        input={
            "task": "transcribe",
            "audio": state.audio_buffer,
            "language": "None",
            "timestamp": "chunk",
            "batch_size": 64,
            "diarise_audio": False,
        },
    )

    return {
        "audio_transcription": output["text"],
    }


audio_transcriber = Node(
    name="audio_transcriber",
    run=run,
)
