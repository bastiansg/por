from multi_agents.graph import MultiAgentGraph

from .nodes import (
    idle_state,
    recorder,
    audio_transcriber,
    gatekeeper,
    validation_checkpoint,
    language_detector,
    astrology_placements_detector,
    query_parser,
    astrology_advisor,
    image_describer,
    microphone_remove,
    psychological_describer,
    lyrics_advisor,
    nietzsche_advisor,
    random_selector,
    satc_advisor,
    image_prompter,
    image_generator,
    printer,
)

from .edges import (
    idle_state_recorder,
    recorder_conditional,
    audio_transcriber_astrology_placements_detector,
    astrology_placements_detector_query_parser,
    image_prompter_edges,
    image_describer_microphone_remove,
    psychological_describer_astrology_advisor,
    image_prompter_image_generator,
    audio_transcriber_language_detector,
    gatekeeper_edges,
    gatekeeper_validation_checkpoint,
    validation_checkpoint_conditional,
    psychological_describer_lyrics_advisor,
    psychological_describer_nietzsche_advisor,
    psychological_describer_satc_advisor,
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
        astrology_placements_detector,
        query_parser,
        astrology_advisor,
        image_describer,
        microphone_remove,
        psychological_describer,
        lyrics_advisor,
        nietzsche_advisor,
        random_selector,
        satc_advisor,
        image_prompter,
        image_generator,
        printer,
    ]

    edges = [
        idle_state_recorder,
        recorder_conditional,
        audio_transcriber_astrology_placements_detector,
        astrology_placements_detector_query_parser,
        image_prompter_edges,
        image_describer_microphone_remove,
        psychological_describer_astrology_advisor,
        image_prompter_image_generator,
        audio_transcriber_language_detector,
        gatekeeper_edges,
        gatekeeper_validation_checkpoint,
        validation_checkpoint_conditional,
        psychological_describer_lyrics_advisor,
        psychological_describer_nietzsche_advisor,
        psychological_describer_satc_advisor,
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
