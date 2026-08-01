from multi_agents.graph import MultiAgentGraph

from .edges import (
    audio_transcriber_astrology_placements_extractor,
    audio_transcriber_language_detector,
    idle_state_recorder,
    image_prompter_image_generator,
    language_detector_gatekeeper,
    printer_edges,
    psychological_describer_astrology_advisor,
    psychological_describer_lyrics_advisor,
    psychological_describer_nietzsche_advisor,
    psychological_describer_satc_advisor,
    recorder_conditional,
    validation_checkpoint_conditional,
    validation_checkpoint_edges,
)
from .nodes import (
    astrology_advisor,
    astrology_placements_extractor,
    audio_transcriber,
    gatekeeper,
    idle_state,
    image_describer,
    image_generator,
    language_detector,
    lyrics_advisor,
    nietzsche_advisor,
    printer,
    psychological_describer,
    random_selector,
    recorder,
    satc_advisor,
    validation_checkpoint,
)
from .schema import ContextSchema, StateSchema


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
        astrology_advisor,
        lyrics_advisor,
        nietzsche_advisor,
        random_selector,
        satc_advisor,
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
        psychological_describer_lyrics_advisor,
        psychological_describer_nietzsche_advisor,
        psychological_describer_astrology_advisor,
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
