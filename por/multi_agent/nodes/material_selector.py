from typing import Any

from multi_agents.graph import Node
from common.logger import get_logger

from por.multi_agent.schema import StateSchema
from por.data.materials import material_map, materials
from por.llm_agents import MaterialSelector, MaterialSelectorDeps


logger = get_logger(__name__)


IMAGES_PATH = "/resources/ticket-images/materials"


async def run(state: StateSchema) -> dict[str, Any]:
    logger.info("runing material_selector...")

    psychological_profile = state.psychological_profile
    audio_transcription = state.audio_transcription

    assert psychological_profile is not None
    assert audio_transcription is not None

    detected_language = state.detected_language
    assert detected_language is not None

    ms = MaterialSelector()
    ms_output = await ms.generate(
        user_prompt="Select the most resonant material for this person and question.",
        agent_deps=MaterialSelectorDeps(
            psychological_profile=psychological_profile,
            question=audio_transcription,
            materials=materials,
            output_language=detected_language,
        ),
    )

    material_code = ms_output.selected_material_code
    return {
        "selected_material_code": material_code,
        "selected_material_title": material_map[material_code].title,
        "selected_material_image_path": f"{IMAGES_PATH}/{material_map[material_code].code}.jpeg",
        "selected_material_reason": ms_output.selection_reason,
    }


material_selector = Node(
    name="material_selector",
    run=run,
)
