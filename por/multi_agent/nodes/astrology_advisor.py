from typing import Any

from multi_agents.graph import Node
from common.logger import get_logger

from por.multi_agent.schema import StateSchema
from por.llm_agents import AstrologyAdvisor, AstrologyAdvisorDeps


logger = get_logger(__name__)


async def run(state: StateSchema) -> dict[str, Any]:
    logger.info("runing astrology_advisor...")

    astrology_placements = state.astrology_placements
    psychological_profile = state.psychological_profile
    audio_transcription = state.audio_transcription
    detected_language = state.detected_language

    assert astrology_placements is not None
    assert psychological_profile is not None
    assert audio_transcription is not None
    assert detected_language is not None

    if not any(
        (
            astrology_placements.sun,
            astrology_placements.moon,
            astrology_placements.rising,
        )
    ):
        return {}

    astrology_advisor_agent = AstrologyAdvisor()
    astrology_advisor_output = await astrology_advisor_agent.generate(
        user_prompt="Deliver a pure astrological advice.",
        agent_deps=AstrologyAdvisorDeps(
            psychological_profile=psychological_profile,
            question=audio_transcription,
            astrology_placements=astrology_placements,
            output_language=detected_language,
        ),
    )

    return {
        "astrology_advice": astrology_advisor_output.answer,
    }


astrology_advisor = Node(
    name="astrology_advisor",
    run=run,
)
