from multi_agents.graph import MultiAgentGraph

from .nodes import (
    idle_state,
    recorder,
    audio_transcriber,
    gatekeeper,
    validation_checkpoint,
    language_detector,
    image_describer,
    psychological_describer,
    matter_advisor,
    borges_matter_advisor,
    random_selector,
    image_prompter,
    image_generator,
    printer,
)

from .edges import (
    idle_state_recorder,
    recorder_audio_transcriber,
    image_prompter_edges,
    image_prompter_image_generator,
    audio_transcriber_language_detector,
    language_detector_gatekeeper,
    gatekeeper_validation_checkpoint,
    validation_checkpoint_conditional,
    psychological_describer_matter_advisor,
    psychological_describer_borges_matter_advisor,
    printer_edges,
)

from .schema import StateSchema, ContextSchema


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
        borges_matter_advisor,
        random_selector,
        image_prompter,
        image_generator,
        printer,
    ]

    edges = [
        idle_state_recorder,
        recorder_audio_transcriber,
        image_prompter_edges,
        image_prompter_image_generator,
        audio_transcriber_language_detector,
        language_detector_gatekeeper,
        gatekeeper_validation_checkpoint,
        validation_checkpoint_conditional,
        psychological_describer_matter_advisor,
        psychological_describer_borges_matter_advisor,
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
