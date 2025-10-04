from typing import Any
from openai import AsyncOpenAI

from multi_agents.graph import Node
from common.logger import get_logger
from por.multi_agent.schema import StateSchema


logger = get_logger(__name__)


async def run(state: StateSchema) -> dict[str, Any]:
    logger.info("runing audio_transcriber...")

    audio_buffer = state.audio_buffer
    assert audio_buffer is not None

    audio_buffer.name = "audio.mp3"
    client = AsyncOpenAI()

    transcription = await client.audio.transcriptions.create(
        model="gpt-4o-transcribe",
        file=audio_buffer,
    )

    return {
        "audio_buffer": None,
        "audio_transcription": transcription.text,
    }


audio_transcriber = Node(
    name="audio_transcriber",
    run=run,
)
