from multi_agents.graph import MultiAgentGraph

from .nodes import (
    idle_state,
    recorder,
    audio_transcriber,
    gatekeeper,
    image_describer,
    psychological_describer,
    nietzsche_advisor,
    music_advisor,
    creative_advisor,
    random_selector,
    image_generator,
    printer,
)

from .edges import (
    idle_state_recorder,
    recorder_audio_transcriber,
    recorder_image_describer,
    gatekeeper_edges,
    gatekeeper_conditional,
    psychological_describer_nietzsche_advisor,
    psychological_describer_creative_advisor,
    psychological_describer_music_advisor,
    psychological_describer_image_generator,
    printer_edges,
)

from .schema import StateSchema, ContextSchema


def get_multi_agent() -> MultiAgentGraph:
    nodes = [
        idle_state,
        recorder,
        audio_transcriber,
        gatekeeper,
        image_describer,
        psychological_describer,
        nietzsche_advisor,
        music_advisor,
        creative_advisor,
        random_selector,
        image_generator,
        printer,
    ]

    edges = [
        idle_state_recorder,
        recorder_audio_transcriber,
        recorder_image_describer,
        gatekeeper_edges,
        gatekeeper_conditional,
        psychological_describer_nietzsche_advisor,
        psychological_describer_creative_advisor,
        psychological_describer_music_advisor,
        psychological_describer_image_generator,
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
