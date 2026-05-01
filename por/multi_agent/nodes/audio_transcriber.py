from typing import Any
from openai import AsyncOpenAI

from langgraph.runtime import get_runtime

from multi_agents.graph import Node
from rich.console import Console
from por.multi_agent.schema import StateSchema, ContextSchema


console = Console()


async def run(state: StateSchema) -> dict[str, Any]:
    runtime = get_runtime(ContextSchema)
    runtime_context = runtime.context

    if runtime_context.test_mode:
        return {}

    console.log("runing audio_transcriber...")

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
