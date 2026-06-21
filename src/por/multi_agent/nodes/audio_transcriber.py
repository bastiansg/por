from typing import Any
from openai import AsyncOpenAI

from langgraph.runtime import get_runtime

from multi_agents.graph import Node
from por.multi_agent.console import render_node_banner
from por.multi_agent.schema import StateSchema, ContextSchema


async def run(state: StateSchema) -> dict[str, Any]:
    if state.audio_transcription is not None:
        return {}

    runtime = get_runtime(ContextSchema)
    runtime_context = runtime.context

    if runtime_context.test_mode:
        return {}

    render_node_banner("audio_transcriber")

    audio_buffer = state.audio_buffer
    assert audio_buffer is not None

    audio_buffer.name = "audio.wav"
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
