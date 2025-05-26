from multi_agents.graph import MultiAgentGraph

from .nodes import (
    face_tracker,
    image_describer,
    psychological_describer,
    nietzsche_advisor,
    ts_advisor,
    creativity_advisor,
    dc_selector,
    fc_selector,
    number_archetypes,
    image_prompter,
    image_generator,
    image_uploader,
    printer,
    recovery,
)

from .edges import (
    face_tracker_image_describer,
    image_describer_psychological_describer,
    psychological_describer_nietzsche_advisor,
    psychological_describer_ts_advisor,
    psychological_describer_creativity_advisor,
    psychological_describer_dc_selector,
    psychological_describer_fc_selector,
    psychological_describer_number_archetypes,
    image_prompter_edges,
    image_prompter_image_generator,
    image_generator_image_uploader,
    image_uploader_printer,
    printer_recovery,
)

from .schema import StateSchema, ConfigSchema


def get_multi_agent() -> MultiAgentGraph:
    nodes = [
        face_tracker,
        image_describer,
        psychological_describer,
        nietzsche_advisor,
        ts_advisor,
        creativity_advisor,
        dc_selector,
        fc_selector,
        number_archetypes,
        image_prompter,
        image_generator,
        image_uploader,
        printer,
        recovery,
    ]

    edges = [
        face_tracker_image_describer,
        image_describer_psychological_describer,
        psychological_describer_nietzsche_advisor,
        psychological_describer_ts_advisor,
        psychological_describer_creativity_advisor,
        psychological_describer_dc_selector,
        psychological_describer_fc_selector,
        psychological_describer_number_archetypes,
        image_prompter_edges,
        image_prompter_image_generator,
        image_generator_image_uploader,
        image_uploader_printer,
        printer_recovery,
    ]

    multi_agent = MultiAgentGraph(
        state_schema=StateSchema,
        config_schema=ConfigSchema,
        nodes=nodes,
        edges=edges,
        with_memory=False,
    )

    multi_agent.compile()
    return multi_agent
