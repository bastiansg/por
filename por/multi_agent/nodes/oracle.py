from typing import Any

from multi_agents.graph import Node
from common.logger import get_logger

from por.llm_agents import Oracle, OracleDeps
from por.multi_agent.schema import StateSchema


logger = get_logger(__name__)


async def run(state: StateSchema) -> dict[str, Any]:
    logger.info("runing oracle...")

    audio_transcription = state.audio_transcription
    assert audio_transcription is not None

    nietzsche_advise = state.nietzsche_advise
    assert nietzsche_advise is not None

    detected_language = state.detected_language
    assert detected_language is not None

    image_description = state.image_description
    assert image_description is not None

    oracle = Oracle()
    oracle_output = await oracle.generate(
        user_prompt="Provide your prophecy in the style of the Oracle from The Matrix.",
        agent_deps=OracleDeps(
            gender_presentation=image_description.physical_description.gender_presentation,
            question=audio_transcription,
            advice=nietzsche_advise,
            output_language=detected_language,
        ),
    )

    return {
        "oracle_prophecy": oracle_output.oracle_prophecy,
    }


oracle = Node(
    name="oracle",
    run=run,
)
