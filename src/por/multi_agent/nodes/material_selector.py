from typing import Any

from multi_agents.graph import Node

from por.data.materials import material_map, materials
from por.llm_agents import MaterialSelector, MaterialSelectorDeps
from por.multi_agent.console import render_node_banner
from por.multi_agent.schema import StateSchema

IMAGES_PATH = "/resources/ticket-images/materials"


async def run(state: StateSchema) -> dict[str, Any]:
    render_node_banner("material_selector")

    psychological_profile = state.psychological_profile
    audio_transcription = state.audio_transcription
    detected_language = state.detected_language

    assert psychological_profile is not None
    assert audio_transcription is not None
    assert detected_language is not None

    selector = MaterialSelector()
    selector_output = await selector.generate(
        user_prompt="Select the most resonant material interaction.",
        agent_deps=MaterialSelectorDeps(
            output_language=detected_language,
            psychological_profile=psychological_profile,
            question=audio_transcription,
            materials=materials,
        ),
    )
    material = material_map[selector_output.selected_material_code]

    return {
        "selected_material_code": material.code,
        "selected_material_interaction": material.interaction,
        "selected_material_image_path": f"{IMAGES_PATH}/{material.code}.jpeg",
        "selected_material_reason": selector_output.selection_reason,
    }


material_selector = Node(
    name="material_selector",
    run=run,
)
