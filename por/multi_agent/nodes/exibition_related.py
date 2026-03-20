from typing import Any

from multi_agents.graph import Node
from common.logger import get_logger

from por.llm_agents import exibition_related as _exibition_related
from por.llm_agents import ExibitionRelated, ExibitionRelatedDeps
from por.multi_agent.schema import StateSchema


logger = get_logger(__name__)


async def run(state: StateSchema) -> dict[str, Any]:
    logger.info("running exibition_related...")

    audio_transcription = state.audio_transcription
    assert audio_transcription is not None

    detected_language = state.detected_language
    assert detected_language is not None

    exibition_related = ExibitionRelated(
        conf_path=f"{_exibition_related.__path__[0]}/exibition-related.yml",
    )

    exibition_related_output = await exibition_related.generate(
        user_prompt=f"Message: {audio_transcription}",
        agent_deps=ExibitionRelatedDeps(output_language=detected_language),
    )

    return {
        "exibition_related": exibition_related_output.exibition_related,
    }


exibition_related = Node(
    name="exibition_related",
    run=run,
)
