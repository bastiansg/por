from multi_agents.graph import MultiAgentGraph

from .nodes import (
    idle_state,
    recorder,
    audio_transcriber,
    astrology_placements_extractor,
    gatekeeper,
    validation_checkpoint,
    language_detector,
    image_describer,
    psychological_describer,
    ancora_advisor,
    rwalsh_advisor,
    pr_advisor,
    random_selector,
    image_generator,
    printer,
)

from .edges import (
    idle_state_recorder,
    recorder_conditional,
    image_prompter_image_generator,
    audio_transcriber_language_detector,
    audio_transcriber_astrology_placements_extractor,
    language_detector_gatekeeper,
    validation_checkpoint_edges,
    validation_checkpoint_conditional,
    psychological_describer_ancora_advisor,
    psychological_describer_rwalsh_advisor,
    psychological_describer_pr_advisor,
    printer_edges,
)

from .schema import StateSchema, ContextSchema


def get_multi_agent() -> MultiAgentGraph:
    nodes = [
        idle_state,
        recorder,
        audio_transcriber,
        astrology_placements_extractor,
        gatekeeper,
        validation_checkpoint,
        language_detector,
        image_describer,
        psychological_describer,
        ancora_advisor,
        rwalsh_advisor,
        pr_advisor,
        random_selector,
        image_generator,
        printer,
    ]

    edges = [
        idle_state_recorder,
        recorder_conditional,
        image_prompter_image_generator,
        audio_transcriber_language_detector,
        audio_transcriber_astrology_placements_extractor,
        language_detector_gatekeeper,
        validation_checkpoint_edges,
        validation_checkpoint_conditional,
        psychological_describer_ancora_advisor,
        psychological_describer_rwalsh_advisor,
        psychological_describer_pr_advisor,
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
