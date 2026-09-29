from multi_agents.graph import MultiAgentGraph

from .edges import (
    audio_transcriber_language_detector,
    idle_state_recorder,
    image_prompter_image_generator,
    language_detector_gatekeeper,
    printer_edges,
    psychological_describer_material_selector,
    psychological_describer_matter_advisor,
    recorder_conditional,
    validation_checkpoint_conditional,
    validation_checkpoint_edges,
)
from .nodes import (
    audio_transcriber,
    gatekeeper,
    idle_state,
    image_describer,
    image_generator,
    language_detector,
    material_selector,
    matter_advisor,
    printer,
    psychological_describer,
    random_selector,
    recorder,
    validation_checkpoint,
)
from .schema import ContextSchema, StateSchema


def get_multi_agent() -> MultiAgentGraph:
    nodes = [
        idle_state,
        recorder,
        audio_transcriber,
        gatekeeper,
        validation_checkpoint,
        language_detector,
        image_describer,
        psychological_describer,
        matter_advisor,
        material_selector,
        random_selector,
        image_generator,
        printer,
    ]

    edges = [
        idle_state_recorder,
        recorder_conditional,
        image_prompter_image_generator,
        audio_transcriber_language_detector,
        language_detector_gatekeeper,
        validation_checkpoint_edges,
        validation_checkpoint_conditional,
        psychological_describer_matter_advisor,
        psychological_describer_material_selector,
        printer_edges,
    ]

    multi_agent = MultiAgentGraph(
        state_schema=StateSchema,
        context_schema=ContextSchema,
        nodes=nodes,
        edges=edges,
        with_memory=False,
    )

    multi_agent.compile()
    return multi_agent
